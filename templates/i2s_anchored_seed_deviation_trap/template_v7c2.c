/*
 * i2s_anchored_seed_deviation_trap v7c2 — SUB-TYPE C trap shape, REVISED.
 *
 * v7c (16-site upstream block) was over-restrictive at high N: at
 * N_ARMS_PER_OFFSET=56 and 224 neither fuzzer could pass all 16 sites
 * within 600s, so the trap was unreachable and the predicted crossover
 * regime (vp > vpc at high anchor density) couldn't be observed.
 *
 * v7c2 reduces upstream block from 16 sites to 4 sites. The upstream
 * gate is now solvable at all doses (4 × N_ARMS entries instead of
 * 16 × N_ARMS), so the sub-type C trap at offset 128 is reachable
 * across the full sweep. The mechanism prediction stays the same:
 * vpc/vp ratio monotone-decreasing in N_ARMS as vpc's I2S dictionary
 * dilutes its substitution rate at the K=7 class literals.
 *
 * Compile-time parameter: N_ARMS_PER_OFFSET ∈ {1, 7, 56, 224}.
 *
 * Same trap shape as v7c: class field at offset 128 must NOT match
 * one of K=7 valid FOURCCs (modeled on lcms cmsSig*Class FOURCCs).
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
#define K_VALID      7
#define N_SITES      4              /* REDUCED from 16 */
#define MAX_ARMS     224

/* 4 anchor sites at offsets 0, 4, 8, 12 (instead of v7c's 16 sites at
 * 0..64). Smaller upstream block → tractable upstream navigation at
 * all doses, so trap is reachable in 600s for both fuzzers. */
static const size_t SITE_OFFSETS[N_SITES] = {0, 4, 8, 12};

static const uint32_t CLASS_LITERALS[K_VALID] = {
    0x73636E72u, 0x6D6E7472u, 0x70727472u, 0x6C696E6Bu,
    0x61627374u, 0x73706163u, 0x6E6D636Cu
};

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

__attribute__((noinline))
static int valid_at_site(int site, uint32_t v) {
    int found = 0;
    for (int i = 0; i < N_ARMS_PER_OFFSET; i++) {
        if (v == SIGS_TABLE[site * MAX_ARMS + i]) found = 1;
    }
    return found;
}

__attribute__((noinline))
static int valid_class(uint32_t cls) {
    int found = 0;
    for (int i = 0; i < K_VALID; i++) {
        if (cls == CLASS_LITERALS[i]) found = 1;
    }
    return found;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    setup_sigs();

    if (size < TRAP_OFFSET + 4) return 0;
    if (read_be32(data + MAGIC_OFFSET) != MAGIC_VALUE) return 0;
    for (int s = 0; s < N_SITES; s++) {
        if (!valid_at_site(s, read_be32(data + SITE_OFFSETS[s]))) return 0;
    }

    uint32_t cls = read_be32(data + TRAP_OFFSET);
    if (!valid_class(cls)) {
        __builtin_trap();
    }
    return 0;
}
