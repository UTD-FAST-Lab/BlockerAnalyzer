/*
 * Template: i2s_keyword_anchoring_starves_runtime_accumulator
 * Family:   I2S_anti  (the I2S technique HURTS the fuzzer that has it)
 *
 * Mechanism being isolated (from the cluster brief, libxml2 #3121 & #2203):
 *   The blocking branch guards a RUNTIME ACCUMULATOR -- a counter that must
 *   exceed a compile-time cap (MAX_FREE_NODES / MAX_HASH_LEN) by way of many
 *   distinct executions / deep traversal, NOT by matching any single input
 *   literal. To reach the trap an input must carry DIVERSITY: many *distinct*
 *   tokens, each pushing the accumulator one step. There is no byte sequence
 *   I2S can substitute that flips the gate.
 *
 *   An EARLY KEYWORD CMP sits in front (an exact equality against a canonical
 *   literal -- the XML preamble "<?xml ver" stand-in). On any input the program
 *   compares the head bytes against this literal. cmplog/value_profile_cmplog
 *   carry I2SRandReplace, which reads that CMP from the CmpLogObserver buffer
 *   and rewrites the matching input offsets back to the canonical literal --
 *   ANCHORING those fuzzers' corpora on well-formed, structurally uniform
 *   inputs whose token stream collapses to the same few values. That uniform
 *   corpus never accumulates enough DISTINCT tokens to clear the cap. naive /
 *   value_profile lack I2SRandReplace, so their havoc drifts the token region
 *   into many distinct values and the accumulator overflows.
 *
 *   The token region spans up to ~247 bytes (256-byte buffer minus the 9-byte
 *   keyword), so every scan value below is reachable-in-principle for a
 *   sufficiently diverse input; only DIVERSITY (distinct byte values), never a
 *   single substituted literal, can clear the gate.
 *
 *   Knob = ACCUM_THRESHOLD: the number of DISTINCT tokens that must be
 *   accumulated before the trap fires. Higher threshold => the keyword-anchored
 *   I2S corpus (few distinct tokens) starves harder, while diversity-by-havoc
 *   still climbs. Predicted: the I2S-LACKING fuzzer wins, and the gap GROWS
 *   with ACCUM_THRESHOLD.
 *
 * Honesty caveat (see feature_spec.json:hypothesis.tradeoff_observation):
 *   "Anchoring" is a CORPUS-LEVEL / scheduler dynamic across many executions; a
 *   single-execution micro-harness cannot literally reproduce the cmplog corpus
 *   pollution. What this harness reproduces faithfully is the STRUCTURAL trap:
 *   (a) an early exact-literal CMP that I2SRandReplace will lock onto and keep
 *   re-satisfying with the SAME literal, and (b) a diversity-accumulator gate
 *   that no single-literal substitution can satisfy. The starvation emerges only
 *   if cmplog's substitution actually re-homogenizes the token region across the
 *   campaign; the acceptance rule is therefore conservative and an
 *   "inconclusive" verdict is an honest outcome.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

/* ---- The single program-feature knob: distinct-token accumulator cap. ---- */
#ifndef ACCUM_THRESHOLD
#define ACCUM_THRESHOLD 8
#endif

/*
 * Early keyword literal -- the I2S attractor. Exactly the kind of canonical
 * XML-preamble operand I2SRandReplace substitutes in the real bug. 10 bytes.
 */
static const uint8_t KEYWORD[10] = { '<','?','x','m','l',' ','v','e','r' , 0 };
#define KEYWORD_LEN 9

/*
 * Layout consumed from the input:
 *   [0 .. KEYWORD_LEN)            : must equal KEYWORD  (the early CMP gate)
 *   [KEYWORD_LEN .. )             : a stream of 1-byte tokens; we count how many
 *                                   DISTINCT token values appear. Reaching
 *                                   ACCUM_THRESHOLD distinct values trips the trap.
 *
 * The token loop is the runtime accumulator: nDistinct is built up over the
 * input the way freeElemsNr/nbi build up over a parse. No single byte value
 * (no I2S substitution) can carry it past the cap -- only DIVERSITY can.
 */

#define TOKEN_REGION_OFF KEYWORD_LEN
#define MIN_TOKENS       ACCUM_THRESHOLD          /* need at least this many bytes to even have a chance */
#define MIN_INPUT        (KEYWORD_LEN + MIN_TOKENS)

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < MIN_INPUT)
        return 0;

    uint8_t buf[256];
    size_t n = size < sizeof(buf) ? size : sizeof(buf);
    memcpy(buf, data, n);

    /* ---- Early keyword CMP: the I2S attractor (exact equality). ---- */
    if (memcmp(buf, KEYWORD, KEYWORD_LEN) != 0)
        return 0;

    /*
     * ---- Runtime diversity accumulator. ----
     * Walk the token region and count distinct byte values seen. This is the
     * counter-vs-cap gate; nDistinct is the analogue of freeElemsNr / nbi.
     */
    uint8_t seen[256];
    memset(seen, 0, sizeof(seen));
    unsigned int nDistinct = 0;

    for (size_t i = TOKEN_REGION_OFF; i < n; i++) {
        uint8_t tok = buf[i];
        if (!seen[tok]) {
            seen[tok] = 1;
            nDistinct++;
        }
    }

    /* ---- Blocking branch: accumulator must EXCEED the compile-time cap. ---- */
#if ACCUM_THRESHOLD > 0
    if (nDistinct > ACCUM_THRESHOLD) {
        __builtin_trap();   /* SOLE objective */
    }
#endif

    return 0;
}
