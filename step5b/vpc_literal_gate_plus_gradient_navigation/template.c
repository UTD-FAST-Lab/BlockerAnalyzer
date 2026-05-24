/*
 * vpc_literal_gate_plus_gradient_navigation
 * Family: synergy (i2s_literal_substitution_with_vp_upstream_gradient)
 *
 * Synthetic SYNERGY harness. The objective trap requires TWO components to
 * be solved together within budget:
 *
 *   (a) An UPSTREAM VP-climbable chain: CHAIN_DEPTH sequential single-byte
 *       equality gates. Each gate compares one input byte against a fixed
 *       constant. These are emitted as plain integer comparisons that the
 *       value-profile CMP_MAP can bucket by Hamming/closeness, so a fuzzer
 *       with VP gradient feedback can retain partial-prefix progress and
 *       climb the chain gate-by-gate. A pure-I2S fuzzer (cmplog) gets only
 *       a single coverage edge for the whole chain head and must blindly
 *       reproduce the whole sequence at once -> probability collapses as
 *       CHAIN_DEPTH grows.
 *
 *   (b) A TERMINAL exact multi-byte LITERAL gate (fixed TERM_BYTES wide,
 *       wide enough that blind/gradient search alone stalls). A single
 *       memcmp against a contiguous literal. This is the classic
 *       I2S-substitutable shape (I2SRandReplace plants the literal from
 *       intercepted CMP operands). A pure-VP fuzzer has no I2S substitution
 *       and cannot cheaply synthesize a wide contiguous literal.
 *
 * Only a fuzzer carrying BOTH techniques (value_profile_cmplog) can clear
 * the upstream gradient chain AND plant the terminal literal in the same
 * budget. Neither single technique suffices.
 *
 * The SINGLE compile-time knob is CHAIN_DEPTH: the number of sequential
 * upstream VP-climbable byte gates. The terminal literal width is held
 * FIXED (TERM_BYTES) and wide enough that pure-VP stalls on it regardless
 * of depth; pure-I2S stalls on the chain at high depth. So vpc's advantage
 * over the single-technique losers GROWS monotonically with CHAIN_DEPTH.
 *
 * The __builtin_trap() on the all-gates-true side is the SOLE objective;
 * there are no partial-match coverage edges other than the VP-bucketable
 * comparisons that ARE the gradient mechanism (the point of the chain).
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

/* ---- THE ONE KNOB: upstream VP-climbable chain depth ---- */
#ifndef CHAIN_DEPTH
#define CHAIN_DEPTH 4
#endif

/* Terminal exact-literal gate width, held fixed and wide enough that
 * neither pure-VP nor pure-I2S clears the whole structure alone. */
#ifndef TERM_BYTES
#define TERM_BYTES 4
#endif

/* The fixed terminal literal (TERM_BYTES contiguous bytes). */
static const uint8_t TERM_LITERAL[8] = {
    'C', 'F', 'F', '2', 'D', 'I', 'C', 'T'
};

/* Per-gate constants for the upstream chain. Distinct, non-degenerate
 * values so each gate is an independent climbable comparison. */
static const uint8_t CHAIN_CONST[16] = {
    0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88,
    0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0x0F, 0xF0
};

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    /* Layout: [ CHAIN_DEPTH chain bytes ][ TERM_BYTES terminal literal ] */
    const size_t need = (size_t)CHAIN_DEPTH + (size_t)TERM_BYTES;
    if (size < need)
        return 0;

    uint8_t chain[16];
    uint8_t term[8];
    memcpy(chain, data, (size_t)CHAIN_DEPTH);
    memcpy(term, data + CHAIN_DEPTH, (size_t)TERM_BYTES);

    /* (a) Upstream VP-climbable chain: CHAIN_DEPTH sequential single-byte
     * equality gates. Each comparison is value-profile-bucketable; the
     * gradient lets a VP fuzzer retain a seed that matches a longer prefix
     * of the chain. A short-circuited &&-fold means a non-VP fuzzer sees
     * essentially one head edge for the whole chain. */
    int chain_ok = 1;
    for (int i = 0; i < CHAIN_DEPTH; i++) {
        if (chain[i] != CHAIN_CONST[i]) {
            chain_ok = 0;
            break;
        }
    }
    if (!chain_ok)
        return 0;

    /* (b) Terminal exact multi-byte LITERAL gate (I2S-substitutable). */
    if (memcmp(term, TERM_LITERAL, (size_t)TERM_BYTES) == 0) {
        /* Both components solved together -> sole objective. */
        __builtin_trap();
    }

    return 0;
}
