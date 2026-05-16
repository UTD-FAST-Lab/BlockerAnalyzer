/*
 * i2s_inequality_anchor_trap v3 — SEED-INDUCED BOUNDARY ANCHOR.
 *
 * Real-target origin (unchanged): lcms cmsio0.c:827
 *   `if (TagCount > MAX_TABLE_TAG)` where MAX_TABLE_TAG = 100.
 *   blocked_side = T (error path); vp 10/10 resolved, vpc 0/10.
 *
 * Backward trace from the on-disk vpc Side-A seed (000cec6b...): 564B
 * ICC profile, magic='acsp', class='mntr', TagCount=10. The cmplog
 * trace_const_cmp4 at line 827 logs the OPERAND PAIR (10, 100) — NOT
 * (K, K) (v2's blunder) and NOT "upstream parser fields" (yesterday's
 * strpres remap). The seed corpus naturally carries TagCount=10 because
 * real ICC profiles encode small tag counts.
 *
 * Why v1/v2 failed.
 *   v1 (K=100, no seed corpus): random uint32 > 100 with prob ~99.99999%
 *     — trap fires on initial random input, both fuzzers crash at run_time=0.
 *     No anchor opportunity for I2S to act.
 *   v2 (K=UINT32_MAX-1, no seed corpus): random hit rate 1/2^32 — both
 *     fuzzers gradient-ascend via CMP_MAP regardless of I2S. Once one
 *     reaches all-0xFF, throughput dominates. cmplog tracing stage
 *     gives vpc more execs/sec post-discovery; vpc dominates. Gradient
 *     ascent overrides splice-back anchor.
 *
 * Both v1 and v2 lacked the LOAD-BEARING ingredient: a SEED CORPUS with
 * a value V at the comparison offset where V << K and the natural (V, K)
 * pair populates the I2S dictionary. V=10 (logged from seed's TagCount)
 * is what makes splice-back at offset 128 active — I2S substitutes any
 * `00 00 00 0a` byte sequence with `00 00 00 64` (K=100), locking
 * TagCount to 100, where `100 > 100` is false.
 *
 * v3 mechanism (re-anchored).
 *   1. Seed has bytes `00 00 00 0a` at offset 128 (V=10, big-endian).
 *   2. Harness reads u32-BE at offset 128 and tests `> K`.
 *   3. cmplog logs (10, K) pair into I2S dictionary.
 *   4. I2SRandReplace finds 4-byte sequences matching V=10 in offspring
 *      and substitutes with K. After substitution, value_at_offset = K,
 *      so `K > K` = false. Splice-back IS the anchor.
 *   5. CMP_MAP gradient (vp + vpc) climbs from V=10 toward K via
 *      Hamming-distance feedback. vp's gradient escapes the boundary
 *      monotonically. vpc's gradient escapes too — but each successful
 *      escape is randomly re-anchored back to K by I2S splice-back when
 *      the offspring is re-selected for mutation.
 *
 * Knob: SEED_GAP = K - V (V=10 fixed, K varies).
 *   K=11   (gap=1):    trivial 1-step random walk, both fuzzers crack
 *                      immediately. Floor case. Predicted parity.
 *   K=20   (gap=10):   short gradient path; splice-back weakly active.
 *   K=100  (gap=90):   the lcms-canonical case. Splice-back load-bearing.
 *                      Predicted vp >> vpc.
 *   K=1010 (gap=1000): long gradient ascent path; both fuzzers rely on
 *                      CMP_MAP feedback. Splice-back keeps re-anchoring
 *                      vpc whenever V→K substitution path is short.
 *                      Predicted vp >> vpc with smaller delta as gradient
 *                      paths saturate.
 *
 * Predicted dose-response (primary pair: A=value_profile, B=value_profile_cmplog):
 *   vp >= vpc at every gap; vp/vpc ratio peaks at intermediate gap
 *   (around gap=90 mirroring lcms br73), declines slightly at large
 *   gap as gradient ascent dominates both fuzzers.
 *
 * Headline metric: TIME-TO-FIRST-CRASH (not total crash count).
 *   Total crash count after first discovery is post-discovery throughput,
 *   dominated by vpc's higher cmplog tracing-stage throughput. The
 *   meaningful signal is whether vpc EVER escapes the K boundary.
 *
 * Acceptance: vp median time-to-first-crash < vpc median TTFC at gap=90;
 *   vpc trial-failure-rate (no crash within budget) > 0 at gap=90.
 *
 * Falsifier: if vpc TTFC matches or beats vp at every gap, the
 *   splice-back boundary anchor mechanism is also bounded by libafl's
 *   scheduler/throughput dynamics, joining strpres in the catalog of
 *   "real-target divergences that don't reproduce in trivial synthetic
 *   harnesses given libafl's saturation behavior".
 */

#include <stdint.h>
#include <stddef.h>

#ifndef SEED_GAP
#define SEED_GAP 90
#endif

/* V is fixed at 10, mirroring real-lcms TagCount=10 in vpc Side-A seeds. */
#define INEQ_LITERAL ((uint32_t)(10u + (uint32_t)SEED_GAP))

static inline uint32_t read_be32(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /* Input must be at least 132 bytes for a TagCount field at offset 128.
     * Mirrors the lcms _cmsReadHeader requirement (128B header + 4B TagCount). */
    if (size < 132) return 0;

    uint32_t tag_count = read_be32(data + 128);

    /* The trap CMP. cmplog logs (tag_count_value_in_seed, INEQ_LITERAL)
     * here. With seed corpus having tag_count=V=10, the logged operand
     * pair is (10, INEQ_LITERAL) — exactly the pair that makes
     * I2SRandReplace's splice-back snap V→K. */
    if (tag_count > INEQ_LITERAL) {
        __builtin_trap();
    }
    return 0;
}
