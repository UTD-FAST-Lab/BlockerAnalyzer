/*
 * vp_gradient_direct_literal  (family VP_pro)
 *
 * Discovered mechanism (step 5a):
 *   "direct_gradient_to_single_literal" — value_profile's CMP_MAP records a
 *   per-PC Hamming-distance bucket for an integer == comparison. Each input
 *   whose candidate word gets bit-by-bit closer to one fixed goal constant
 *   opens a new CMP_MAP bucket and is preserved as corpus, giving VP a
 *   monotone gradient toward the exact match. naive (edge-only feedback) and
 *   cmplog (I2S substitution, no distance feedback) have no fitness signal for
 *   partial matches.
 *
 * The gate is a SINGLE integer equality the CMP_MAP can bucket — NOT a memcmp
 * ladder and NOT an incremental per-byte if-chain — so partial-match progress
 * is the only rewarded thing and that reward is VP-specific.
 *
 * I2S-UNSUBSTITUTABILITY (this cluster's defining divergence is
 * value_profile_cmplog > cmplog, member harfbuzz_9584): the compared operand
 * must NOT be a plain compile-time literal that cmplog's CMP buffer can log and
 * paste verbatim. We achieve this with a per-execution runtime mask derived
 * from a SEPARATE input region: the equality is checked between
 *   (candidate ^ mask)  and  (GOAL ^ mask)
 * which is algebraically true iff candidate == GOAL (so the Hamming gradient on
 * the candidate is fully preserved for VP), but the two operands the CMP
 * callback actually observes both move with `mask` every execution. cmplog
 * therefore cannot capture a stable value to substitute — there is no fixed
 * literal at the CMP to paste. VP's bucketed distance feedback is the only edge.
 *
 *   ONE knob: OPERAND_WIDTH = number of bytes the candidate word spans (1..8).
 *   Wider operand => more bits the gradient must climb => bigger VP advantage
 *   over naive, and a wider I2S-blind gap for cmplog.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

/* ----- the single program-feature axis knob ----- */
#ifndef OPERAND_WIDTH
#define OPERAND_WIDTH 4
#endif

#if (OPERAND_WIDTH < 1) || (OPERAND_WIDTH > 8)
#error "OPERAND_WIDTH must be in [1, 8]"
#endif

/* The goal constant the gradient must climb toward. Truncated to the operand
 * width below so every scan value compiles and the gate stays satisfiable. */
#define GOAL_FULL 0x0A85u

/* Layout in the input buffer:
 *   [0, OPERAND_WIDTH)                     -> candidate word (LE)
 *   [OPERAND_WIDTH, OPERAND_WIDTH+8)       -> mask seed (LE u64)
 */
#define MASK_OFFSET   (OPERAND_WIDTH)
#define MIN_INPUT     (OPERAND_WIDTH + 8)

static inline uint64_t read_le(const uint8_t *p, size_t n) {
    uint64_t v = 0;
    for (size_t i = 0; i < n; i++)
        v |= (uint64_t)p[i] << (8 * i);
    return v;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < MIN_INPUT)
        return 0;

    /* width mask so the goal is representable in OPERAND_WIDTH bytes */
    const uint64_t width_mask =
        (OPERAND_WIDTH >= 8) ? ~(uint64_t)0
                             : (((uint64_t)1 << (8 * OPERAND_WIDTH)) - 1);

    uint64_t candidate = read_le(data, OPERAND_WIDTH) & width_mask;
    uint64_t goal      = ((uint64_t)GOAL_FULL) & width_mask;

    /* per-execution runtime mask derived from a separate input region; it
     * cancels in the equality but moves the operands the CMP callback sees, so
     * there is no stable literal for I2S to paste. */
    uint64_t mask = read_le(data + MASK_OFFSET, 8) & width_mask;

    uint64_t lhs = (candidate ^ mask) & width_mask;
    uint64_t rhs = (goal      ^ mask) & width_mask;

    /* SOLE objective: a single integer equality the CMP_MAP can bucket. */
    if (lhs == rhs) {
        __builtin_trap();
    }

    return 0;
}
