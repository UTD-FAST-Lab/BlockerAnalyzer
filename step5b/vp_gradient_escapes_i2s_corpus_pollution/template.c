/*
 * Synthetic harness for cluster: vp_gradient_escapes_i2s_corpus_pollution
 * Family: VP_pro
 * Mechanism label: gradient_overcomes_i2s_induced_corpus_bias
 *
 * Distinctive shape (from brief): I2S is the ACTIVE NEGATIVE.
 *   Decisive pairs, BOTH with cmplog as LOSER:
 *     - naive               > cmplog   [delta: I2S]            (I2S hurts)
 *     - value_profile_cmplog > cmplog   [delta: value_profile]  (VP rescues)
 *   The VP_pro-defining pair is value_profile_cmplog > cmplog: value_profile's
 *   CMP_MAP Hamming gradient keeps seeds that are making progress toward the
 *   target, even while I2S substitution actively biases the corpus away from it.
 *
 * Harness construction:
 *   (a) A target condition reachable by a VP-climbable gradient.
 *       `acc` is a derived 4-byte field built from input bytes. The SOLE
 *       objective is acc == TARGET, expressed as one full-width comparison so
 *       value_profile's CMP_MAP can bucket the Hamming distance and climb it.
 *       naive and cmplog see only the boolean outcome of that final compare.
 *
 *   (b) A competing literal that I2S keeps substituting, pushing the derived
 *       value AWAY from the target. Before the final compare we run a bank of
 *       DECOY_COUNT decoy equality gates over a sliding 4-byte window of the
 *       input. Each decoy gate is `if (window == DECOY[k]) acc ^= DECOY[k];`.
 *       Those comparisons populate the CmpLogObserver with DECOY[k] operands.
 *       cmplog's I2SRandReplace then harvests those decoy literals and
 *       substitutes them into the input window, which (i) re-triggers the decoy
 *       gate and (ii) XOR-corrupts `acc` away from TARGET -> corpus pollution.
 *       naive never harvests CMP operands, so it is not dragged toward decoys.
 *       value_profile_cmplog suffers the same I2S substitution but its CMP_MAP
 *       gradient on the final acc==TARGET compare retains the seeds still
 *       making Hamming progress, so it escapes the pollution.
 *
 * ONE -D knob: DECOY_COUNT = strength of the I2S misdirection (number of
 *   distinct competing literals I2S can latch onto). Larger => more decoy
 *   operands flood the CmpLogObserver => cmplog degrades more, while
 *   value_profile keeps climbing the unchanged target gradient.
 *
 * Self-contained: stdint/stddef/string only.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

/* ---- compile-time knob: strength of I2S misdirection ---- */
#ifndef DECOY_COUNT
#define DECOY_COUNT 4
#endif

/* The single target gradient endpoint. A non-round 4-byte value so the only
 * way to reach it is to climb the Hamming gradient on the final compare; it is
 * NOT one of the decoy literals, so I2S substitution never lands on it. */
#define TARGET 0x5A6B7C8Du

/* Bank of distinct decoy literals. Up to 8 are made available; DECOY_COUNT
 * selects how many of them are LIVE (each live one emits its own CMP operand
 * into the CmpLogObserver, and only live ones corrupt `acc`). These are
 * deliberately spread far from TARGET in value space so substituting any of
 * them drags the derived field away from the objective. */
static const uint32_t DECOY[8] = {
    0x11111111u, 0x22222222u, 0x33333333u, 0x44444444u,
    0xAABBCCDDu, 0xCAFEBABEu, 0xDEADBEEFu, 0xFEEDFACEu
};

#if DECOY_COUNT < 1
#error "DECOY_COUNT must be >= 1"
#endif
#if DECOY_COUNT > 8
#error "DECOY_COUNT must be <= 8 (only 8 decoy literals are defined)"
#endif

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /* window (4 bytes) feeds the I2S-harvestable decoy gates;
     * grad (4 bytes) is the raw material for the VP-climbable target. */
    if (size < 8)
        return 0;

    uint32_t window = 0, grad = 0;
    memcpy(&window, data, 4);
    memcpy(&grad, data + 4, 4);

    uint32_t acc = grad;

    /* (b) I2S misdirection bank. DECOY_COUNT controls how many decoy literals
     * are live. Each live comparison populates the CmpLogObserver with its
     * operand, giving I2SRandReplace something to harvest and substitute into
     * the input window -- which then matches here and XOR-perturbs acc away
     * from the unchanged target gradient. The loop bound is the compile-time
     * knob, so changing DECOY_COUNT changes the emitted code (live CMP count). */
    for (int k = 0; k < DECOY_COUNT; k++) {
        if (window == DECOY[k]) {
            acc ^= DECOY[k];   /* drag the derived field away from TARGET */
        }
    }

    /* (a) The SOLE objective: a single full-width comparison whose Hamming
     * distance value_profile's CMP_MAP can bucket and climb. naive/cmplog see
     * only the boolean. */
    if (acc == TARGET) {
        __builtin_trap();
    }

    return 0;
}
