/*
 * i2s_anchored_seed_deviation_trap v7a — SUB-TYPE A trap shape verification.
 *
 * Companion to v6 (which verified the mechanism on a sub-type B trap shape:
 * `tag_count > K` threshold). v7a tests whether the same upstream-anchor-
 * density mechanism produces vp > vpc divergence on a sub-type A trap
 * shape: pure LENGTH-FAIL (no literal at trap CMP).
 *
 * Trap shape:
 *   if (size < SHORT_TRAP) trap();
 * No literal target — I2SRandReplace cannot substitute a runtime size
 * value into input bytes. Both fuzzers have CMP_MAP gradient at the
 * length CMP. Differentiation comes purely from QUEUE LENGTH
 * DISTRIBUTION: vpc's queue is monocultured at long anchored inputs by
 * the upstream anchor block; mutations from long parents to size <
 * SHORT_TRAP require many BytesDeleteMutator hits in succession.
 * vp's queue has more length variety; mutations to short children are
 * proportionally more frequent.
 *
 * Mirrors lcms cmsio0.c:776 br68 trap (`io->Read != 1` length-fail).
 *
 * Compile-time parameter:
 *   N_ARMS_PER_OFFSET ∈ {1, 7, 56, 224} — same knob as v6, controls
 *   upstream I2S dictionary breadth.
 *
 * Predicted v7a dose-response: same crossover pattern as v6.
 *   - Low N: vpc wins (cmplog's I2S accelerates passing upstream gates,
 *     more total queue activity, more mutations including shrinking)
 *   - High N: vp wins (vpc's queue heavily monocultured at long
 *     anchored inputs, BytesDeleteMutator from those rarely reaches
 *     size < SHORT_TRAP)
 *
 * If the crossover is observed at v7a, it independently verifies that
 * the v6 mechanism is NOT specific to sub-type B trap shape — the
 * upstream-anchor-density → queue-monoculture pipeline operates on
 * sub-type A traps too.
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
#define ANCHOR_GATE  132          /* anchors only run when size >= 132 */
#define SHORT_TRAP   4            /* sub-type A trap: size < 4 */
#define N_SITES      16
#define MAX_ARMS     224

static const size_t SITE_OFFSETS[N_SITES] = {
    0,  4,  8,  12, 16, 20, 24, 28,
    32, 40, 44, 48, 52, 56, 60, 64
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

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    setup_sigs();

    /* === SUB-TYPE A TRAP === */
    /* Length-fail trap. No literal at the CMP — I2S cannot substitute
     * a size value into input bytes. Differentiation purely from queue
     * monoculture pressure on parent length. */
    if (size < (size_t)SHORT_TRAP) {
        __builtin_trap();
    }

    /* === UPSTREAM ANCHOR BLOCK === */
    /* Same shape as v6. Runs only when size >= ANCHOR_GATE (132 B).
     * Each successful gate emits one coverage edge. Each literal CMP
     * populates vpc's I2S dictionary; I2SRandReplace then biases
     * mutations to preserve these literals at offsets 0..64.
     * Effect: vpc's queue is monocultured at long anchored inputs;
     * vp's queue has more length variety. */
    if (size < (size_t)ANCHOR_GATE) return 0;

    if (read_be32(data + MAGIC_OFFSET) != MAGIC_VALUE) return 0;

    for (int s = 0; s < N_SITES; s++) {
        if (!valid_at_site(s, read_be32(data + SITE_OFFSETS[s]))) return 0;
    }

    return 0;
}
