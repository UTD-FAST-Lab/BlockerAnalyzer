/*
 * i2s_anchored_seed_deviation_trap v6 — FIXED-SEED-LENGTH MULTI-ANCHOR.
 *
 * Companion to v5 (NOT a replacement). v5 reproduced the mechanism
 * cleanly (vp/vpc ratio peak 27× at N=16) but the curve plateaued at
 * N=64+ because v5 GREW the seed length with N (132B → 264B → 1032B).
 * Two confounded effects in v5:
 *   (1) I2S dictionary breadth grows with N: per-mutation substitution
 *       rate at offset 128 drops to ~1/(7N+2). Boundary anchor weakens.
 *   (2) Seed length grows with N: random byte mutation hits offset 128
 *       less often. Both fuzzers' drift rate at the trap region drops.
 *
 * v6 isolates (1) from (2): seed length is FIXED at 132 bytes; the
 * number of UNIQUE 4-byte literals in the I2S dictionary varies via
 * N_ARMS_PER_OFFSET, with 16 anchor offsets all packed in bytes 0-64.
 *
 * Compile-time parameter:
 *   N_ARMS_PER_OFFSET ∈ {1, 7, 56, 224}
 *     Each anchor offset accepts N_ARMS_PER_OFFSET distinct sigs.
 *     Total I2S dict entries = 16 × N_ARMS_PER_OFFSET (each site uses
 *     a distinct slice of the SIGS_TABLE), plus 'acsp' magic + trap pair.
 *
 *   N=1:   16 dict entries (sparse)
 *   N=7:   112 dict entries (matches v5 N=16 design density)
 *   N=56:  896 dict entries
 *   N=224: 3584 dict entries (above real-lcms density)
 *
 * Predicted v6 dose-response (using corpus byte-distribution at offset 128):
 *   - vpc/vp anchored-fraction gap should INCREASE monotonically with
 *     N_ARMS_PER_OFFSET (cleaner than v5 because seed length is fixed).
 *   - At N_ARMS_PER_OFFSET=1: small gap (few I2S entries to maintain).
 *   - At N_ARMS_PER_OFFSET=224: maximum gap (dense dict → strong I2S
 *     substitution pressure on offset 128 too via the trap-CMP-logged
 *     (V=10, K=100) pair).
 *
 * If v6 shows MONOTONE gap (no peak-and-fall like v5), the seed-length
 * confound is confirmed. v5 + v6 together demonstrate that the
 * mechanism is real AND that the canonical-target real-lcms regime
 * (fixed-size 564B seed with ~200 logged CMPs) sits firmly within the
 * effect's productive range.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef N_ARMS_PER_OFFSET
#define N_ARMS_PER_OFFSET 7
#endif

#if N_ARMS_PER_OFFSET != 1   && N_ARMS_PER_OFFSET != 7   && \
    N_ARMS_PER_OFFSET != 56  && N_ARMS_PER_OFFSET != 224
#error "N_ARMS_PER_OFFSET must be one of {1, 7, 56, 224}"
#endif

#define MAGIC_OFFSET 36
#define MAGIC_VALUE  0x61637370U  /* 'acsp' */
#define TRAP_OFFSET  128
#define TRAP_K       100
#define N_SITES      16
#define MAX_ARMS     224  /* upper bound for SIGS_TABLE size */

/* 16 anchor offsets packed in [0, 64], skipping offset 36 (magic).
 * No offset >= 128 — keeps the trap-region (128-131) clear of anchors. */
static const size_t SITE_OFFSETS[N_SITES] = {
    0,  4,  8,  12, 16, 20, 24, 28,
    32, 40, 44, 48, 52, 56, 60, 64
};

/* SIGS_TABLE[N_SITES * MAX_ARMS]: each site uses a DISTINCT slice
 * SIGS_TABLE[site * MAX_ARMS .. site * MAX_ARMS + N_ARMS_PER_OFFSET - 1].
 * All values >= 0x10000000 to avoid collision with small TagCount values
 * at the trap (V=10, K=100 are below 0x100). Initialized at runtime to
 * keep the binary identical-shape across scan values. */
static uint32_t SIGS_TABLE[N_SITES * MAX_ARMS];

static void setup_sigs(void) {
    static int initialized = 0;
    if (initialized) return;
    for (size_t i = 0; i < (size_t)N_SITES * MAX_ARMS; i++) {
        SIGS_TABLE[i] = 0x10000000U + (uint32_t)i;
    }
    initialized = 1;
}

static inline uint32_t read_be32(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

/* Per-site whitelist check. Each iteration emits one trace_const_cmp_4
 * style hook (against the runtime SIGS_TABLE element). cmplog logs
 * each (input_value_at_site, table_value) pair. */
__attribute__((noinline))
static int valid_at_site(int site, uint32_t v) {
    int found = 0;
    for (int i = 0; i < N_ARMS_PER_OFFSET; i++) {
        if (v == SIGS_TABLE[site * MAX_ARMS + i]) found = 1;
    }
    return found;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    setup_sigs();

    /* Fixed minimum input: 132 bytes (header to TRAP_OFFSET + 4). */
    if (size < TRAP_OFFSET + 4) return 0;

    /* Single-anchor magic at offset 36 */
    if (read_be32(data + MAGIC_OFFSET) != MAGIC_VALUE) return 0;

    /* 16 multi-anchor sites, each with N_ARMS_PER_OFFSET valid sigs */
    for (int s = 0; s < N_SITES; s++) {
        if (!valid_at_site(s, read_be32(data + SITE_OFFSETS[s]))) return 0;
    }

    /* The trap: anchored-seed-deviation. Same as v5: TagCount > K. */
    uint32_t tag_count = read_be32(data + TRAP_OFFSET);
    if (tag_count > TRAP_K) {
        __builtin_trap();
    }
    return 0;
}
