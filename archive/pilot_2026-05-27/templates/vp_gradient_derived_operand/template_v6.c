/**
 * vp_gradient_derived_operand v6: VP wins on additive byte-SUM trap
 * where I2S splice is mathematically prevented by sum-vs-max constraint.
 *
 * Why v6 exists.
 * v4 reproduced (vp, naive) primary pair but the full 4-fuzzer signature
 * was BRBR — same as i2s_magic_number_gate, cmp dominated 12-380x.
 * v5 attempted XOR-checksum to defeat I2S. v5 failed: with all-zero seed,
 * I2S substitution finds `00 00 00 00` everywhere in input, splices
 * TARGET (0xDEADBEEF) at bytes 0..3 → chunk0 = TARGET, other chunks
 * still 0 → checksum = TARGET XOR 0 = TARGET → trap. Trivial splice.
 * cmp produced 7000+ crashes per trial via I2S-stage refinement of
 * the initial seed alone.
 *
 * v6 uses ADDITIVE SUM-OF-BYTES with target near MAX. The constraint
 * is mathematical: any single 4-byte I2S splice produces ≤ 4*255 = 1020
 * sum contribution at those positions. To reach TARGET = SUM_WIDTH * 250
 * (close to max SUM_WIDTH*255), the OTHER bytes must sum to roughly
 * SUM_WIDTH*250 - 1020. At W=8 that's 980 from 4 other bytes (max 1020) —
 * tight; at W=4 the constraint is impossible (TARGET=1000, splice
 * contribution ≤ 1020 needed exactly). I2S splice cannot trivially
 * satisfy.
 *
 * Knob: SUM_WIDTH ∈ {4, 8, 16, 32} bytes summed.
 *   TARGET_SUM = SUM_WIDTH * 250 (98% of max).
 *
 *   W=4 control: TARGET=1000, max=1020. Splice would need exact 1000
 *      from 4 specific bytes — possible but specific.
 *   W=8: TARGET=2000, max=2040. Splice gives ≤1020; impossible to
 *      satisfy without coordinated mutation of other bytes.
 *   W=16: TARGET=4000, max=4080. Splice gives ≤1020; need other 12
 *      bytes summing to ≥2980 (avg ≥249/byte). Very tight.
 *   W=32: TARGET=8000, max=8160. Splice gives ≤1020; need other 28
 *      bytes summing to ≥6980 (avg ≥249/byte). Very tight.
 *
 * VP gradient: each byte mutation toward 0xFF increases sum by up to
 * +255. CMP_MAP retains seeds at smaller hamming(sum, TARGET) buckets.
 * Hamming distance is non-monotone with arithmetic distance (e.g. sum=2000
 * has popcount(2000)=6, sum=2040 has popcount(2040)=8) but the gradient
 * still produces corpus retention as bytes accumulate ones — VP walks
 * the corpus toward all-0xFF inputs.
 *
 * Predicted decisive shape: B-R-
 *   naive: B (random walk, density of solutions 0 at W≥8)
 *   cmp:   B (I2S splice mathematically impossible to satisfy alone)
 *   vp:    R (gradient walks bytes toward 0xFF)
 *   vpc:   R (vpc inherits vp's gradient; I2S adds nothing)
 */

#include <stdint.h>
#include <stddef.h>

#ifndef SUM_WIDTH
#define SUM_WIDTH 8
#endif

#if SUM_WIDTH != 4 && SUM_WIDTH != 8 && \
    SUM_WIDTH != 16 && SUM_WIDTH != 32
#error "SUM_WIDTH must be one of {4, 8, 16, 32}"
#endif

#define TARGET_SUM ((uint32_t)(SUM_WIDTH * 250))

__attribute__((noinline))
static uint32_t compute_sum(const uint8_t *data) {
    uint32_t sum = 0;
    for (int i = 0; i < SUM_WIDTH; i++) {
        sum += (uint32_t)data[i];
    }
    return sum;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < SUM_WIDTH) return 0;
    uint32_t sum = compute_sum(data);

    /* Single 32-bit literal-equality CMP at the trap. The operand
     * (sum) is the byte-sum of SUM_WIDTH input bytes. The literal
     * (TARGET_SUM) is SUM_WIDTH * 250, near max. I2S logs TARGET_SUM
     * but splicing its 4 bytes at any input position contributes only
     * ≤ 4*255 = 1020 to the sum — at W≥8 mathematically insufficient
     * to satisfy the trap without coordinated mutation of the other
     * SUM_WIDTH-4 bytes. cmp degenerates to naive. VP's CMP_MAP
     * gradient walks via hamming(sum, TARGET) bucket retention. */
    if (sum == TARGET_SUM) {
        __builtin_trap();
    }
    return 0;
}
