/**
 * i2s_grammar_chain_length v2 — AND-accumulator chain harness.
 *
 * Companion to v1 (REFUTED 2026-05-05). v1 used independent per-slot
 * memcmp calls in a short-circuit chain:
 *   for (i=0..CHAIN_LEN) { if (!lex_kw_i(...)) return 0; ... }
 * Each per-slot CMP had its own source-location PC + branch coverage
 * edge. CMP_MAP retained "slot 0 matched" seeds at slot 0's coverage
 * level; subsequent mutations on those seeds compounded forward
 * through the chain SEQUENTIALLY. The per-slot decoupling collapsed
 * the predicted exponential vp/vpc ratio to a flat ~5x.
 *
 * v2 redesigns the chain so:
 *   (a) all per-slot equality CMPs go through ONE noinline function,
 *       so all CMP source PCs collapse to one — cmp_map at that PC
 *       only retains the most-recent (operand-A, operand-B) pair, NOT
 *       per-slot buckets. vp's CMP_MAP cannot compound across slots.
 *   (b) the chain accumulates via AND (`&=`), not short-circuit `&&`,
 *       so every iteration runs and there are NO intermediate
 *       per-slot branches. Only ONE coverage-edge'd branch exists:
 *       `if (allmatch) trap()`.
 *   (c) per-slot literals (KEYWORDS[i]) are still logged by cmplog's
 *       __sanitizer_cov_trace_const_cmp_4 hook — vpc's I2S can
 *       substitute any of them at any input offset in O(1) per slot.
 *
 * Predicted v2 dose-response:
 *   - vp's gradient at the single CMP source-PC has only a few
 *     distance buckets (between the most-recent slot's value and its
 *     KEYWORD). Cannot compound across slots. vp must hit ALL slots
 *     by random byte mutation: ~1/256^(4*CHAIN_LEN) per input.
 *     Exponential decay in CHAIN_LEN.
 *   - vpc's I2S logs all CHAIN_LEN slot literals. I2SRandReplace
 *     splices any logged 4-byte literal into any input offset — 1
 *     per slot per substitution event. CHAIN_LEN slots in expectation
 *     within ~ CHAIN_LEN^2 attempts (linear-ish in CHAIN_LEN).
 *   - vpc/vp ratio diverges as ~256^(4*CHAIN_LEN), monotone-increasing
 *     in CHAIN_LEN. Predicted vp ~ 0 at CHAIN_LEN=4, vpc still
 *     resolves at CHAIN_LEN=8.
 *
 * Acceptance (revised from v1's broken rule):
 *   (1) vpc median > 0 at every CHAIN_LEN
 *   (2) vp median monotone non-increasing in CHAIN_LEN
 *   (3) vpc/vp ratio monotone non-decreasing
 *   (4) at CHAIN_LEN=8: vp median ~ 0 OR vpc/vp ratio >= 100
 *
 * Compile-time parameter:
 *   CHAIN_LEN ∈ {1, 2, 4, 8}; one Dockerfile per scan value.
 *
 * STRICTLY TWO FUZZERS PER TEMPLATE. Primary pair: (value_profile_cmplog,
 * value_profile). Same as v1 — same I2S axis_differ.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef CHAIN_LEN
#define CHAIN_LEN 4
#endif

#if CHAIN_LEN != 1 && CHAIN_LEN != 2 && CHAIN_LEN != 4 && CHAIN_LEN != 8
#error "CHAIN_LEN must be one of {1, 2, 4, 8}"
#endif

#define SLOT_WIDTH 4

/* 8 distinct 4-byte literals (big-endian ASCII). v1 used the same
 * keywords; preserved here so token identity isn't a confound. */
static const uint32_t KEYWORDS[8] = {
    0x74637066u,  /* 'tcpf' */
    0x75647071u,  /* 'udpq' */
    0x686f7374u,  /* 'host' */
    0x706f7274u,  /* 'port' */
    0x69707634u,  /* 'ipv4' */
    0x69707636u,  /* 'ipv6' */
    0x67726578u,  /* 'grex' */
    0x61727079u   /* 'arpy' */
};

static volatile uint32_t g_slot_sink;
static volatile int g_chain_len_runtime;

/* Single-PC slot check: ALL per-slot equality CMPs go through this
 * one source location. cmplog's __sanitizer_cov_trace_const_cmp_4
 * hook is inserted once at the `==` line; cmp_map indexes by PC and
 * stores the most-recent (slot, KEYWORDS[i]) operand pair. Across N
 * iterations, only the LAST pair survives in cmp_map. vp's CMP_MAP
 * gradient cannot compound per-slot Hamming-distance buckets. */
__attribute__((noinline))
static int check_one_slot(int slot_idx, const uint8_t *p) {
    /* Force the function not to be inlined back even at -O2 by adding
     * a volatile side-effect that aliases against the runtime store. */
    g_slot_sink ^= (uint32_t)slot_idx;
    uint32_t slot = ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
                    ((uint32_t)p[2] <<  8) |  (uint32_t)p[3];
    /* Single CMP source-location. Per-slot literal KEYWORDS[slot_idx]
     * is logged by cmplog as I2S dictionary entry. */
    return slot == KEYWORDS[slot_idx];
}

/* check_chain accumulates slot results via AND (not short-circuit).
 * No intermediate branches → no per-slot coverage edges. The volatile
 * runtime bound discourages compiler unrolling that would create
 * per-iteration call-site PCs. */
__attribute__((noinline))
static int check_chain(const uint8_t *data) {
    int allmatch = 1;
    int n = g_chain_len_runtime;  /* volatile read */
#pragma clang loop unroll(disable)
    for (int i = 0; i < n; i++) {
        /* Result is AND-accumulated, not branched. allmatch may go
         * 0 partway and stay 0; no early exit, no branch. */
        allmatch &= check_one_slot(i, data + i * SLOT_WIDTH);
    }
    return allmatch;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < (size_t)(CHAIN_LEN * SLOT_WIDTH)) return 0;

    /* Set the volatile chain length so the compiler can't constant-
     * fold it during unrolling decisions. */
    g_chain_len_runtime = CHAIN_LEN;

    /* The ONE coverage-edge'd branch in this harness. */
    if (check_chain(data)) {
        __builtin_trap();
    }
    return 0;
}
