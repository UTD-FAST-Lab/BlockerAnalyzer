/**
 * vp_rescues_i2s_derived_operand: parameterized harness for the
 * (value_profile_cmplog, cmplog) source pair on a state-accumulator
 * unlock — the I2S-blackout, VP-rescues sub-case of the
 * synergy_cmplog_plus_vp pattern.
 *
 * Design REVISED 2026-05-04 (round-14): adopted the DFA state-machine
 * design proposed by the br736 agent. Original br1077 design used a
 * bijective XOR chain abstraction; the DFA is more faithful to both
 * real-target origins (libpcap BPF optimizer bitmask + flex DFA
 * scanner) where the actual gating CMP is a TABLE LOOKUP whose
 * operands are runtime-derived array values, with NO literal target
 * appearing in the program's CMP space at all.
 *
 * Origins (BOTH at libpcap):
 *   br1077: optimize.c:650 `if (!ATOMELEM(use, atom))` — bit-test on
 *     a uint32 bitset runtime-accumulated by the BPF optimizer's
 *     compute_local_ud() walk. The `use` mask has no input-byte
 *     pre-image; cmplog's I2S has no literal to substitute.
 *   br736:  scanner.c:3514 `case 1: return DST` inside flex-generated
 *     yylex switch(yy_act). Reachable only after the DFA's transition
 *     CMP `yy_chk[yy_base[state]+c] != state` accepts the literal
 *     'dst' (3 chars). Both operands runtime-derived from yy_chk[]/
 *     yy_base[]/yy_def[]/yy_nxt[] tables; keyword bytes 'd','s','t'
 *     never appear as compile-time CMP literals.
 *
 * Hypothesis. A multi-byte equality unlock requires a sequence of
 * input bytes to drive a hand-rolled DFA into an accepting state.
 * The DFA transitions are table lookups: `next = TBL[state * 256 + c]`.
 * The gating CMP that controls forward progress is `next != REJECT`
 * — both operands are runtime-derived array values; the keyword
 * characters never appear as compile-time CMP literals. cmplog's I2S
 * therefore has NO useful constant to substitute (case (b) of the
 * canonical cmplog failure modes: "comparison is on a value derived
 * from input via a non-invertible function"). cmplog's CmpLogObserver
 * still logs the runtime values of `next` and `REJECT` (a sentinel
 * like 0xFF), but splicing 0xFF into input bytes does not advance the
 * DFA. cmplog effectively reduces to naive on this harness.
 *
 * value_profile's CMP_MAP records the Hamming distance between `next`
 * and `REJECT`. As input bytes drift toward keyword-recognising values,
 * the DFA transitions through intermediate non-reject states; new
 * Hamming-distance buckets retain the seeds that produced them. The
 * gradient propagates one character at a time through the DFA, which
 * is the same mechanism that lets vpc resolve flex-generated lex
 * scanners (libpcap scanner.c case-arms, observed branch 736).
 *
 * value_profile_cmplog's claim: it benefits from VP's gradient AND
 * cmplog's I2S. On this harness I2S contributes nothing (no literals
 * to substitute), so vpc's advantage over cmp comes entirely from the
 * VP component. The dose-response sweep over KEYWORD_LEN therefore
 * exposes the VP-rescues-I2S signal in isolation.
 *
 * Predicted dose-response (vpc vs cmp):
 *   KEYWORD_LEN=1 — both resolve trivially; ratio ~1
 *   KEYWORD_LEN=2 — cmp ≈ naive (~600s for 1/65k), vpc gradients in seconds; ratio ~10x
 *   KEYWORD_LEN=3 — cmp blocks (1/16M is below 600s naive budget), vpc still resolves; ratio diverges
 *   KEYWORD_LEN=5 — cmp = 0; vpc may struggle but should retain via deep gradient; ratio still vpc >> cmp
 *
 * STRICTLY TWO FUZZERS PER TEMPLATE. Pair = (vpc, cmplog) on the
 * value_profile axis. Other fuzzers' behavior is incidental.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef KEYWORD_LEN
#define KEYWORD_LEN 3
#endif

#if KEYWORD_LEN < 1 || KEYWORD_LEN > 5
#error "KEYWORD_LEN must be in [1, 5]"
#endif

#define REJECT 0xFFu
#define DFA_STATES (KEYWORD_LEN + 1)

static const uint8_t KEYWORD_BYTES[5] = { 0x64, 0x73, 0x74, 0x2A, 0x24 };

static volatile uint8_t g_dfa_sink;

/* dfa_table is initialised at runtime to discourage the compiler from
 * folding transitions into per-character literal CMPs. */
static uint8_t dfa_table[DFA_STATES][256];

__attribute__((noinline))
static void setup_dfa(void) {
    static int initialized = 0;
    if (initialized) return;
    initialized = 1;
    for (int s = 0; s < DFA_STATES; s++) {
        for (int c = 0; c < 256; c++) {
            dfa_table[s][c] = REJECT;
        }
    }
    for (int s = 0; s < KEYWORD_LEN; s++) {
        dfa_table[s][KEYWORD_BYTES[s]] = (uint8_t)(s + 1);
    }
}

__attribute__((noinline))
static uint8_t dfa_step(uint8_t state, uint8_t c) {
    /* Single transition: gating CMP is `next != REJECT` in the caller;
     * both operands are runtime-derived from dfa_table[]. */
    return dfa_table[state][c];
}

__attribute__((noinline))
static int recognise(const uint8_t *p, size_t n) {
    uint8_t state = 0;
    for (size_t i = 0; i < n; i++) {
        uint8_t next = dfa_step(state, p[i]);
        if (next == REJECT) {
            /* Dead-end: reset to start. cmplog logs `next` and `REJECT`
             * as cmp1 operands but neither is an input byte — splicing
             * 0xFF into input never advances the DFA. VP's CMP_MAP
             * records Hamming distance and retains seeds whose `next`
             * landed closer to a non-reject value. */
            state = 0;
            g_dfa_sink ^= next;
            continue;
        }
        state = next;
        g_dfa_sink ^= state;
        if (state == KEYWORD_LEN) {
            return 1;
        }
    }
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    setup_dfa();

    if (size < (size_t)KEYWORD_LEN) {
        return 0;
    }

    if (recognise(data, size)) {
        __builtin_trap();
    }
    return 0;
}
