/**
 * vp_gradient_derived_operand v5: VP wins on XOR-checksum traps where
 * I2S structurally cannot satisfy the comparison.
 *
 * Why v5. v4 reproduced the (vp, naive) primary pair but the broader
 * 4-fuzzer signature was BRBR — same as i2s_magic_number_gate. cmp
 * dominated by 12-380× because I2S could trivially splice the literal
 * TARGET into the direct-equality CMP. v4 doesn't actually demonstrate
 * the "VP wins where cmp can't" mechanism the catalog needs; it
 * demonstrates "VP also can solve magic-number gates, just less
 * efficiently than I2S."
 *
 * v5 uses an XOR-CHECKSUM trap. The cmp operand is a function of
 * CHECKSUM_WIDTH input bytes; the literal TARGET_CHECKSUM never
 * appears AS input bytes — it appears at the comparison after
 * computation. I2S logs the literal but splicing it into input bytes
 * doesn't make the computed checksum equal it (the spliced bytes are
 * one of multiple chunks XOR'd together). cmp degenerates toward
 * naive. VP's CMP_MAP retains seeds at progressively-better Hamming
 * distance to TARGET; byte mutations XOR predictable bits into the
 * checksum. The gradient walks.
 *
 * Knob: CHECKSUM_WIDTH ∈ {4, 8, 16, 32} bytes XOR'd into the checksum
 * (must be a multiple of 4).
 *
 *   W=4: ONE chunk = the chunk itself. Trap collapses to a direct
 *        equality on bytes 0..3 — same shape as i2s_magic_number_gate.
 *        Predicted: shape BRBR, cmp/vpc dominate (control case).
 *   W≥8: chunks XOR'd together. I2S splice gives no reliable
 *        advantage. Predicted: shape B-R-, vp/vpc dominate.
 *
 * The W=4 vs W=8 transition demonstrates exactly when I2S stops being
 * useful and VP gradient takes over. This is the canonical
 * demonstrator of "VP solves checksum-style cmps that I2S can't."
 *
 * Mapping to real targets. The 13 real-target branches in branch_index
 * assigned to this template are NOT literally checksums — they are
 * parser-cascade-gated equality CMPs where cmp's I2S dictionary is
 * diluted by upstream noise CMPs. v5's checksum is the SIMPLEST
 * synthetic that produces the same B-R- decisive shape as those
 * branches: a single CMP that I2S structurally cannot solve. Both
 * mechanisms (checksum and parser-cascade-dilution) result in cmp
 * degenerating toward naive while VP's gradient still bites.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef CHECKSUM_WIDTH
#define CHECKSUM_WIDTH 8
#endif

#if CHECKSUM_WIDTH != 4 && CHECKSUM_WIDTH != 8 && \
    CHECKSUM_WIDTH != 16 && CHECKSUM_WIDTH != 32
#error "CHECKSUM_WIDTH must be one of {4, 8, 16, 32}"
#endif

#define TARGET_CHECKSUM 0xDEADBEEFu

__attribute__((noinline))
static uint32_t compute_checksum(const uint8_t *data) {
    uint32_t checksum = 0;
    for (int i = 0; i < CHECKSUM_WIDTH; i += 4) {
        uint32_t chunk = ((uint32_t)data[i]      )       |
                         ((uint32_t)data[i + 1]) <<  8   |
                         ((uint32_t)data[i + 2]) << 16   |
                         ((uint32_t)data[i + 3]) << 24;
        checksum ^= chunk;
    }
    return checksum;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < CHECKSUM_WIDTH) return 0;
    uint32_t checksum = compute_checksum(data);

    /* Single 32-bit literal-equality CMP at the trap. The operand
     * (checksum) is a function of CHECKSUM_WIDTH input bytes; the
     * literal (TARGET_CHECKSUM) is a compile-time constant. trace_-
     * const_cmp_4 fires here. I2S can log TARGET_CHECKSUM and splice
     * it anywhere in input, but those bytes only contribute to the
     * checksum computation — they don't BE the checksum unless the
     * other chunks happen to XOR to zero. VP's CMP_MAP gradient walks
     * via best-Hamming-distance bucket retention. */
    if (checksum == TARGET_CHECKSUM) {
        __builtin_trap();
    }
    return 0;
}
