/*
 * vp_gradient_chained_parse_depth — VP_pro synthetic harness.
 *
 * Cluster mechanism: value_profile's CMP_MAP records a (PC, operand-distance
 * bucket) entry on every intercepted byte-equality CMP. When the only path to
 * the objective is a CHAIN of sequential single-byte gates — each gate must
 * match its own distinct constant before the next gate is even reached — the
 * CMP_MAP accumulates partial-match reward gate-by-gate. That per-stage
 * gradient lets value_profile / value_profile_cmplog climb the chain one byte
 * at a time, while naive (edge-only) and cmplog (I2S substitution, but no
 * gradient) can only stochastically stumble onto each successive gate.
 *
 * The single -D knob CHAIN_DEPTH = the number of sequential single-byte gates
 * in the chain (= the program-feature axis). Deeper chain => longer the
 * gradient VP must climb but ALSO the larger VP's advantage over edge-only
 * search, whose probability of blindly satisfying all CHAIN_DEPTH bytes is
 * ~1/256^CHAIN_DEPTH.
 *
 * Per the VP-family contract the per-gate edges are INTENDED: the CMP_MAP
 * buckets per-gate progress, and that bucketed gradient IS the winning signal.
 * This is NOT a forbidden partial-match coverage ladder for an I2S/opaque
 * cluster — here the gradient is the mechanism under test.
 */
#include <stddef.h>
#include <stdint.h>
#include <string.h>

#ifndef CHAIN_DEPTH
#define CHAIN_DEPTH 8
#endif

/*
 * Distinct per-gate constants. Each gate i compares byte i to GATE_CONST(i),
 * so every gate is a different single-byte equality (a distinct CMP PC, like
 * the '<' / '"' / '[' / ']' / '>' state-transition characters in the libxml2
 * DOCTYPE state machine that seeded this cluster). Constants are spread across
 * the byte range so no two consecutive gates share a value.
 */
#define GATE_CONST(i) ((uint8_t)(0x41u + (((i) * 37u) & 0x7fu)))

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < CHAIN_DEPTH)
        return 0;

    uint8_t buf[CHAIN_DEPTH];
    memcpy(buf, data, CHAIN_DEPTH);

    /*
     * Sequential state machine: stage advances only when the current byte
     * matches the current gate's constant. Each comparison is a single-byte
     * equality the CMP_MAP can bucket; reaching stage == CHAIN_DEPTH (all
     * gates passed in order) is the SOLE objective.
     */
    size_t stage = 0;
    while (stage < (size_t)CHAIN_DEPTH) {
        if (buf[stage] != GATE_CONST(stage))
            break;
        stage++;
    }

    if (stage == (size_t)CHAIN_DEPTH)
        __builtin_trap();

    return 0;
}
