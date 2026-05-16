/*
 * jump_table_opacity v3 — leak-resistant + active blocking via distractor CMPs.
 *
 * v2 had two confounds:
 *  1. TARGET_CASE = N_CASES / 2 was a small power of 2 at small N
 *     (2, 8, 32, 128). libafl-internal CMPs against these constants
 *     leaked into cmp's I2S dictionary; I2SRandReplace substituted the
 *     leaked constants into bytes 0-3, accidentally landing TARGET.
 *     The "regime transition" was actually "TARGET stops being a
 *     leaked common constant" — not jump-table opacity per se.
 *  2. v2 had no competing literal CMPs to monopolize cmp's I2S budget,
 *     so cmp at high N degraded only to "naive minus throughput tax",
 *     not to the libpcap-magnitude "actively blocked" regime.
 *
 * v3 fixes:
 *  1. TARGET_CASE = 23 (prime, not a small power of 2; 23 is unlikely
 *     to appear as a comparison literal in libafl's runtime).
 *  2. Adds N_DISTRACTORS (knob) noise literal CMPs at non-dispatch
 *     offsets. Each emits a coverage edge for "match"; cmp's queue
 *     accumulates seeds matching distractors via I2S substitution.
 *     At high N_DISTRACTORS, cmp's mutator budget is consumed
 *     substituting distractor literals at non-dispatch offsets;
 *     dispatch bytes (0-3) rarely get mutated; cmp blocks.
 *  3. Uses a function pointer table for dispatch (forces a true
 *     indirect call with NO compiler-introduced range CMP at any N).
 *     The dispatch is opaque at all N regardless of compiler heuristics.
 *
 * Compile-time parameters:
 *   N_CASES = 64 (fixed; jump-table by function-pointer-table design)
 *   N_DISTRACTORS ∈ {0, 16, 64, 4096} — controls cmp's I2S dictionary
 *   pollution level.
 *
 * Predicted dose-response on (cmp, naive) edge at fixed N_CASES=64:
 *   N_DISTRACTORS=0:    cmp ≈ naive minus throughput tax (~10-15%).
 *                       cmp's I2S empty; no help, no monopolize.
 *   N_DISTRACTORS=16:   cmp slightly < naive. Some I2S substitutions
 *                       fire; small mutator budget diversion.
 *   N_DISTRACTORS=64:   cmp ≪ naive. Substantial I2S budget on
 *                       distractors; dispatch bytes mutate less often.
 *   N_DISTRACTORS=4096: cmp ≈ 0 or far below naive. cmp's queue is
 *                       monocultured at distractor-matching seeds with
 *                       fixed dispatch byte distributions. Mirrors the
 *                       libpcap gen_linktype "cmp blocked at all 9
 *                       branches with one identical seed" pattern.
 *
 * 4-fuzzer comparison reported. Primary canonical pair: (cmplog, naive)
 * on I2S delta. cmp WINS at N_DISTRACTORS=0 (slightly, via residual
 * I2S effects) and LOSES at N_DISTRACTORS≥64 (active blocking).
 */

#include <stdint.h>
#include <stddef.h>

#ifndef N_DISTRACTORS
#define N_DISTRACTORS 64
#endif

#if N_DISTRACTORS != 0  && N_DISTRACTORS != 16  && \
    N_DISTRACTORS != 64 && N_DISTRACTORS != 4096
#error "N_DISTRACTORS must be one of {0, 16, 64, 4096}"
#endif

#define N_CASES      64
#define TARGET_CASE  23           /* PRIME — not a small power of 2 */
#define MAX_DISTRACTORS 4096

typedef void (*case_fn_t)(void);
static case_fn_t TABLE[N_CASES];

static volatile uint32_t g_sink;
static volatile uint32_t g_distractor_sink;
static uint32_t DISTRACTOR_LITERALS[MAX_DISTRACTORS];
static int g_setup_done = 0;

__attribute__((noinline))
static void case_default(void) { g_sink ^= 1; }

__attribute__((noinline))
static void case_target(void) { __builtin_trap(); }

static void setup(void) {
    if (g_setup_done) return;
    for (int i = 0; i < N_CASES; i++) TABLE[i] = case_default;
    TABLE[TARGET_CASE] = case_target;
    /* Distractor literals: pseudo-random 32-bit constants spanning a
     * wide range to fill cmp's I2S dictionary diversely. */
    for (int i = 0; i < MAX_DISTRACTORS; i++) {
        DISTRACTOR_LITERALS[i] = 0xCAFE0000U + (uint32_t)(i * 0x101);
    }
    g_setup_done = 1;
}

static inline uint32_t read_be32(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

/* Distractor block: N_DISTRACTORS noise literal CMPs at offsets
 * 16..15+4*N_DISTRACTORS. Each match emits a unique coverage edge via
 * a per-distractor branch outcome. cmp's I2S logs each (input, literal)
 * pair; I2SRandReplace can substitute literals into the input wherever
 * the current input value appears. Match seeds enter the queue and
 * dominate cmp's mutation budget. */
__attribute__((noinline))
static void distractors(const uint8_t *data, size_t size) {
    for (int i = 0; i < N_DISTRACTORS; i++) {
        size_t off = 16 + (size_t)((i * 4) % 256);  /* offsets 16..271, wrap */
        if (off + 4 > size) continue;
        uint32_t v = read_be32(data + off);
        if (v == DISTRACTOR_LITERALS[i]) {
            /* Match: emit a unique-per-distractor side effect for
             * coverage diversity. Each distractor's match path is its
             * own coverage edge. */
            g_distractor_sink ^= (uint32_t)(i + 1);
        }
    }
}

/* Dispatch via function pointer table — single indirect call, no
 * compiler-introduced range CMP at any N. Dispatch is opaque to cmp's
 * I2S regardless of compiler heuristics. */
__attribute__((noinline))
static void dispatch(uint32_t v) {
    uint32_t m = v % (uint32_t)N_CASES;
    TABLE[m]();
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    setup();
    /* Need enough bytes for dispatch (4) + distractor offsets. */
    if (size < 4 + 16 + 256) return 0;
    distractors(data, size);
    uint32_t v = read_be32(data);
    dispatch(v);
    return 0;
}
