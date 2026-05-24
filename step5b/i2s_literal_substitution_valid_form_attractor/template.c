/*
 * i2s_literal_substitution_valid_form_attractor
 * ----------------------------------------------
 * Family: I2S_anti  (the I2S technique HURTS at this gate).
 *
 * Discovered mechanism (from step5a brief):
 *   I2S (I2SRandReplace) observes a gate-adjacent CMP literal and substitutes
 *   it into the input, actively steering the corpus toward the WELL-FORMED /
 *   matching state. But the target branch requires a DEVIATION from that
 *   literal (a malformed / boundary value). The wider the contiguous literal
 *   window I2S keeps re-pasting, the stronger the one-way attractor toward the
 *   all-matching state, and the harder it is to *hold* a deviating byte at the
 *   trap position. The I2S-LACKING fuzzer keeps random diversity at the
 *   deviating position and wins; the gap GROWS with the literal width.
 *
 *   This mirrors libxml2_2727 (`<![CDATA[` chain where cur[4] must NOT be 'D':
 *   I2S re-pastes the whole CDATA literal and "fixes" the deviating byte back),
 *   and libpng_7375 (3-way buf[i]!=0 disjunction where I2S substitutes the
 *   constant 0 into the operand bytes, pinning the input to the matching side).
 *
 * Harness shape:
 *   - A fixed VALID-FORM literal of ATTRACT_BYTES bytes (the literal that I2S
 *     observes at the equality CMP and re-substitutes).
 *   - GATE / TRAP: the input must reach the doorstep of the literal (match the
 *     first ATTRACT_BYTES-1 literal bytes exactly) BUT the byte at the final
 *     literal position must DEVIATE from the literal value (!=).  Only that
 *     deviating-but-anchored input trips __builtin_trap().
 *
 *   The single -D knob ATTRACT_BYTES is the program-feature axis: how wide the
 *   contiguous literal window is that I2S re-pastes. Wider literal => stronger
 *   valid-form attractor competing against the one deviating byte the trap
 *   needs => bigger I2S-hurts gap.
 *
 * Self-contained: stdint/stddef/string only. The trap is the SOLE objective.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

/* ONE compile-time knob = the program-feature axis (literal window width). */
#ifndef ATTRACT_BYTES
#define ATTRACT_BYTES 4
#endif

/* The fixed "valid form" literal I2S observes and re-pastes.
 * Distinctive, non-zero bytes so a CMP logs a clear operand at each position.
 * We use the first ATTRACT_BYTES bytes of this pattern. */
static const uint8_t VALID_FORM[8] = {
    0x43, 0x44, 0x41, 0x54, 0x41, 0x5b, 0x21, 0x3c  /* "CDATA[!<" */
};

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < ATTRACT_BYTES) return 0;

    uint8_t b[ATTRACT_BYTES];
    memcpy(b, data, ATTRACT_BYTES);

    /* Anchor: the first ATTRACT_BYTES-1 bytes must MATCH the valid-form literal
     * exactly. This is the contiguous literal chain I2S observes via the
     * per-position equality CMPs and re-substitutes -- the "valid form"
     * attractor that pulls the whole window toward matching. */
    int anchored = 1;
#if ATTRACT_BYTES > 1
    for (int i = 0; i < ATTRACT_BYTES - 1; i++) {
        if (b[i] != VALID_FORM[i]) { anchored = 0; break; }
    }
#endif

    /* Trap: at the FINAL literal position the byte must DEVIATE from the
     * literal (the malformed / boundary value the real branch requires).
     * I2S re-pastes VALID_FORM[ATTRACT_BYTES-1] here, "fixing" the deviation
     * back; the I2S-lacking fuzzer keeps it random and trips the trap. */
    if (anchored && b[ATTRACT_BYTES - 1] != VALID_FORM[ATTRACT_BYTES - 1]) {
        __builtin_trap();
    }

    return 0;
}
