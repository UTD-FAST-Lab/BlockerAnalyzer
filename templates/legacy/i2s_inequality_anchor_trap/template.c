/*
 * i2s_inequality_anchor_trap — vp BEATS vpc on inequality-CMP traps.
 *
 * Source pair (motivating real branch):
 *   lcms src/cmsio0.c:827  `if (TagCount > MAX_TABLE_TAG) { ... return FALSE; }`
 *   blocked side = T (TagCount > 100); vp resolves 10/10, vpc 0/10.
 *   sister branch br72 (read-fail at line 826) shows same direction.
 *
 * Why this is NOT i2s_structure_preservation_bias (refuted 3x).
 *   strpres targets UPSTREAM literal-equality CMPs polluting the
 *   I2S dictionary and starving descendants of unrelated traps.
 *   v1 (splice-back pinning), v2 (no-seed-tiny correction), v3
 *   (queue-monoculture) all REFUTED. Diagnosis (v3): libafl's
 *   log-scaled scheduler weight saturates at ~3-4x from K=0 to
 *   K=64, structurally below the K-fold flip threshold.
 *
 *   THIS template targets the trap-site CMP itself: a `>` comparison
 *   against a literal K. Different mechanism class.
 *
 * Mechanism (I2S inequality anchor trap).
 *   `if (X > K)` fires; sancov logs K as a 4-byte I2S dictionary
 *   entry every execution. I2SRandReplace mutator splices K back at
 *   offsets where bytes approximating K currently appear in offspring.
 *
 *   Pathology: a beneficial mutation bumps X from K-1 to K+1 (trap
 *   reachable, X>K). On the next selection of that offspring, splice-
 *   back finds the bytes encoding K+1 (one byte off from K) and
 *   rewrites them to K exactly. X==K, X>K is false; the offspring no
 *   longer hits the trap. CMP_MAP retains it as a "best Hamming
 *   distance" near-miss seed (distance 0 to K), so the corpus
 *   monocenters there. The narrow band (K, K+small) is exactly where
 *   splice-back is most aggressive.
 *
 *   value_profile has CMP_MAP gradient (same Hamming bucketing) but
 *   NO I2SRandReplace. vp's offspring drift past K freely; once X>K
 *   no mutator pulls it back. vp resolves the trap reliably.
 *
 * Knob: INEQ_CHAIN_LENGTH in {1, 2, 4, 8}.
 *   N independent `> K` checks, each on a different 4-byte input
 *   slot, all against the SAME literal K = 100. Trap fires only when
 *   ALL N succeed. Splice-back pressure on K compounds: each
 *   offspring has N candidate offsets where I2S can rewrite to K.
 *   vpc must evade splice-back simultaneously at all N. vp's gradient
 *   guides all N independently with no anchor reversion.
 *
 *   N=1 reproduces the lcms br73 minimum case. N=8 is the dose-
 *   response endpoint where vpc's splice-back combinatorial cost is
 *   acute.
 *
 * Predicted dose-response (primary pair vp vs vpc):
 *   vp > vpc on TRAP-crash count at every N >= 1.
 *   vp/vpc ratio MONOTONE NON-DECREASING in N.
 *   At N=1: vp moderately > vpc (single-anchor splice-back is weak).
 *   At N=8: vp >> vpc (compounded anchor pressure starves vpc).
 *
 * Acceptance: vp median > vpc median at N>=2, AND vp/vpc ratio at
 * N=8 is at least 2x the ratio at N=1, AND vpc median is bounded
 * above by vp median across the entire scan.
 *
 * Falsifier: if vpc dominates or matches vp at any scan value, the
 * mechanism is wrong. Most likely failure modes:
 *   - vpc dominates -> mechanism inverted (I2S anchor + CMP_MAP
 *     gradient might HELP vpc rather than trap it).
 *   - Curves flat -> both find trap via random byte mutation;
 *     gradient and I2S are both irrelevant.
 *   - vpc dominates regardless of N -> this would join the
 *     log-saturated refutation catalog with strpres v3.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef INEQ_CHAIN_LENGTH
#define INEQ_CHAIN_LENGTH 1
#endif

/* The literal K in `> K`. v2: use K=UINT32_MAX-1 so random-uint32 hit
 * rate is ~1/2^32 (vs v1's K=100 where ~99.99999% of random uint32s
 * already trip the trap immediately, leaving no time for splice-back to
 * act). At K=0xFFFFFFFE only X=0xFFFFFFFF satisfies, requiring vp's
 * gradient ascent to walk the operand near K — and splice-back's anchor
 * to K is what traps vpc when the operand reaches K+1=0x00000000 (one
 * bit off K=0xFFFFFFFE). */
#define INEQ_LITERAL 4294967294u  /* UINT32_MAX - 1 = 0xFFFFFFFE */

#define SLOT_LIST(M) \
  M(0,  0) \
  M(1,  4) \
  M(2,  8) \
  M(3, 12) \
  M(4, 16) \
  M(5, 20) \
  M(6, 24) \
  M(7, 28)

static inline uint32_t read_be32(const uint8_t *p) {
  return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
         ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

#define DEFINE_SLOT(idx, off)                              \
  __attribute__((noinline))                                \
  static int slot_##idx(const uint8_t *data, size_t size) {\
    if (size < (off) + 4) return 0;                        \
    uint32_t v = read_be32(data + (off));                  \
    if (v > INEQ_LITERAL) return 1;                        \
    return 0;                                              \
  }
SLOT_LIST(DEFINE_SLOT)
#undef DEFINE_SLOT

__attribute__((noinline))
static int chain_check(const uint8_t *data, size_t size) {
  int passed = 0;
#define CALL_SLOT(idx, off)                              \
  do {                                                   \
    if ((idx) < INEQ_CHAIN_LENGTH) {                     \
      if (!slot_##idx(data, size)) return 0;             \
      passed++;                                          \
    }                                                    \
  } while (0);
  SLOT_LIST(CALL_SLOT)
#undef CALL_SLOT
  return (passed == INEQ_CHAIN_LENGTH);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  if (size < 32) return 0;

  if (chain_check(data, size)) {
    __builtin_trap();
  }
  return 0;
}
