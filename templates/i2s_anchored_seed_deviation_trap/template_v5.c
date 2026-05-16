/*
 * i2s_anchored_seed_deviation_trap v5 — REAL-LCMS-DENSITY MULTI-ANCHOR HARNESS.
 *
 * Real-target origin: 8 lcms cmsio0.c branches + bloaty br483 + br595, all
 * showing strict (naive ≈ vp resolve) ↔ (cmplog ≈ vpc block) on the I2S delta.
 *
 * Why v1-v4 plateaued without crossover (revisited):
 *   - v1/v2 strpres: SHRINK_TRAP at low anchor density (0..16 sites). Showed
 *     monotone-in-predicted-direction trend (vp/vpc 0.35→0.88) but didn't cross.
 *   - v3 strpres: queue-monoculture knob, same density range.
 *   - v4 ineq_anchor: 88 dict entries (1 magic + 7 class arms + 80 tag-sigs)
 *     but crash-count-dominated metric → vpc throughput advantage swamped
 *     the mechanism signal.
 *
 *   All 4 prior versions had FEWER ANCHORS than real lcms (which has ~200)
 *   AND used crash-count metric (throughput-dominated post-discovery).
 *
 * v5 fixes:
 *   1. DENSE MULTI-ANCHOR: each anchor site is a 7-arm switch (mirroring
 *      validDeviceClass), each emitting 7 trace_const_cmp4 dict entries.
 *      N_SITES=64 → ~448 dict entries, exceeding real-lcms density.
 *   2. WHITELIST ROTATION: at each multi-anchor site, I2SRandReplace can
 *      substitute the bytes with ANY of the 7 logged class-sigs. The
 *      mutator essentially rotates through valid values without leaving
 *      the valid set. This is structurally STRONGER than single-anchor.
 *   3. METRIC SEPARATION: the harness still uses __builtin_trap() so crash
 *      count is comparable to v3/v4. But the primary metric for v5 is
 *      CORPUS BYTE-DISTRIBUTION at offset 128 (TagCount field): fraction of
 *      queue seeds with TagCount ∈ {10, 100} (anchored) vs drifted.
 *      Throughput cancels out — both fuzzers run for fixed wall-clock time.
 *
 * Knob: N_SITES ∈ {4, 16, 64, 256}
 *   Each site is a 7-arm whitelist check at a distinct 4-byte offset.
 *   Total I2S dict entries ≈ 7×N_SITES + 2 (magic + trap).
 *
 * Predicted dose-response (corpus byte distribution):
 *   At low N (4): I2S substitution at offset 128 rare; both fuzzers
 *     produce drifted children freely. vp/vpc corpus distributions similar.
 *   At medium N (16-64): I2S effect builds. vpc's queue retains seeds
 *     with TagCount ∈ {10, 100} more reliably; vp drifts.
 *   At high N (256): real-lcms-like density. vpc's queue ~95% anchored;
 *     vp's queue ~5-20% anchored.
 *
 * Acceptance: vp's anchored-fraction at TagCount field is at most 50%
 *   of vpc's anchored-fraction at N≥64.
 *
 * Falsifier: if vpc's anchored-fraction matches vp's at every N, the
 *   mechanism is bounded by libafl's mutator-pipeline behavior in a way
 *   that doesn't scale with anchor density. This would be the cleanest
 *   refutation possible (corpus-level metric, not throughput-noise).
 */

#include <stdint.h>
#include <stddef.h>

#ifndef N_SITES
#define N_SITES 16
#endif

#define MAGIC_OFFSET 36
#define MAGIC_VALUE  0x61637370U  /* 'acsp' */
#define TRAP_OFFSET  128
#define TRAP_K       100

/* 7 valid signatures at each multi-anchor site.
 * Mirrors real lcms validDeviceClass switch (cmsio0.c:743-762):
 * cmsSigInputClass, cmsSigDisplayClass, cmsSigOutputClass, cmsSigLinkClass,
 * cmsSigAbstractClass, cmsSigColorSpaceClass, cmsSigNamedColorClass. */
static const uint32_t SIGS[7] = {
    0x73636E72U, 0x6D6E7472U, 0x70727472U, 0x6C696E6BU,
    0x61627374U, 0x73706163U, 0x6E6D636CU
};

static inline uint32_t read_be32(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

/* Reserved offsets that anchor sites must skip (magic + trap field). */
static inline int is_reserved(size_t off) {
    return (off == MAGIC_OFFSET) ||
           (off >= TRAP_OFFSET && off < TRAP_OFFSET + 4);
}

/* 7-arm whitelist check at one anchor site.
 * Each iteration emits one trace_const_cmp4 against SIGS[i] — populating
 * 7 I2S dict entries per call. */
__attribute__((noinline))
static int valid_at_site(uint32_t v) {
    int found = 0;
    for (int i = 0; i < 7; i++) {
        if (v == SIGS[i]) found = 1;
    }
    return found;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /* Compute required input size to fit N_SITES anchor sites + magic + trap. */
    size_t cur = 0;
    int placed = 0;
    size_t max_off = TRAP_OFFSET + 4;  /* trap region needs to be reachable */
    while (placed < N_SITES) {
        if (!is_reserved(cur)) {
            if (cur + 4 > max_off) max_off = cur + 4;
            placed++;
        }
        cur += 4;
    }
    if (size < max_off) return 0;

    /* Single-anchor magic at offset 36 */
    if (read_be32(data + MAGIC_OFFSET) != MAGIC_VALUE) return 0;

    /* N_SITES multi-anchor 7-arm whitelist sites */
    cur = 0;
    placed = 0;
    while (placed < N_SITES) {
        if (!is_reserved(cur)) {
            if (!valid_at_site(read_be32(data + cur))) return 0;
            placed++;
        }
        cur += 4;
    }

    /* The trap: anchored-seed-deviation. Inequality CMP at offset 128.
     * cmplog logs (TagCount_observed, 100) every cycle. I2SRandReplace can
     * substitute either operand at the recorded position, snapping bytes
     * 128-131 to {observed_value, 100}. Random byte mutation drifts freely
     * without I2S re-snap. */
    uint32_t tag_count = read_be32(data + TRAP_OFFSET);
    if (tag_count > TRAP_K) {
        __builtin_trap();
    }
    return 0;
}
