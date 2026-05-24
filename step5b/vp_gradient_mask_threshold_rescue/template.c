/*
 * vp_gradient_mask_threshold_rescue  (family VP_pro)
 *
 * Synthetic harness for the discovered cluster
 *   "mask_or_threshold_gradient_where_i2s_inapplicable".
 *
 * Mechanism under test
 * --------------------
 * The gate is a NUMERIC-THRESHOLD comparison: an input-derived unsigned
 * integer `x` (assembled big-endian from THRESHOLD_BYTES input bytes) must
 * reach a threshold K that sits one unit below the top of x's range:
 *
 *        x >= K        with   K = (max value of an N-byte int) - 1
 *
 * The trap fires on the >= side. Crucially:
 *
 *  - There is NO multi-byte magic literal to log/substitute. The winning
 *    side is satisfied by a RANGE of values ({K, K+1} = the two largest
 *    representable values), not a single constant, so I2S's
 *    I2SRandReplace has nothing exact to anchor on: substituting "the
 *    other operand" of the CMP would just paste K's bytes, but K is the
 *    operand's own near-maximum and does not occur as a recognizable byte
 *    sequence in a low-distance input, so I2S cannot reliably anchor the
 *    overwrite at the right offset.
 *
 *  - value_profile's CMP_MAP records the operand DISTANCE for the CMP and
 *    rewards every input whose `x` climbs closer to K. That monotone
 *    distance gradient is the ONLY guiding signal here, so the
 *    value_profile-bearing fuzzers climb it while naive/cmplog must
 *    blind-search the full 2^(8*THRESHOLD_BYTES) operand space.
 *
 * The gate is a SINGLE comparison (no partial-match coverage ladder): the
 * comparison itself is the gradient the CMP_MAP buckets, which is exactly
 * the mechanism the cluster claims. The wider the operand (larger
 * THRESHOLD_BYTES), the longer the distance VP must climb and the larger
 * the blind-search space naive/cmplog face -> bigger VP advantage.
 *
 * Knob (the ONE program-feature axis):
 *   THRESHOLD_BYTES = width in bytes of the input-derived integer, which
 *   sets both the threshold magnitude K and the size of the operand space.
 *   Larger => bigger VP gradient advantage over the I2S-only / naive loser.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef THRESHOLD_BYTES
#define THRESHOLD_BYTES 4
#endif

#if THRESHOLD_BYTES < 1 || THRESHOLD_BYTES > 8
#error "THRESHOLD_BYTES must be in [1,8]"
#endif

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    /* Need THRESHOLD_BYTES input bytes to assemble the integer. */
    if (size < THRESHOLD_BYTES)
        return 0;

    uint8_t buf[THRESHOLD_BYTES];
    memcpy(buf, data, THRESHOLD_BYTES);

    /* Assemble the input-derived unsigned integer, big-endian. */
    uint64_t x = 0;
    for (int i = 0; i < THRESHOLD_BYTES; i++)
        x = (x << 8) | (uint64_t)buf[i];

    /* Top of the operand's range for this width. */
#if THRESHOLD_BYTES == 8
    const uint64_t RANGE_MAX = (uint64_t)~0ULL;
#else
    const uint64_t RANGE_MAX = ((uint64_t)1 << (8 * THRESHOLD_BYTES)) - 1;
#endif

    /* Threshold sits one unit below the top of the range: a RANGE of
     * winning values {K, K+1}, so there is no single substitutable
     * constant for I2S. The CMP below is the gradient VP's CMP_MAP buckets. */
    const uint64_t K = RANGE_MAX - 1;

    if (x >= K)
        __builtin_trap();   /* SOLE objective: threshold crossed. */

    return 0;
}
