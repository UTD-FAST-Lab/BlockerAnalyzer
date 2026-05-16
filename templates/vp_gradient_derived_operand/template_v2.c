/**
 * vp_gradient_derived_operand v2: chain-of-narrow-CMPs harness.
 *
 * v1 design used a single 32-bit equality CMP plus optional bijective
 * XOR derivation layers. v1 refuted: with one CMP, VP's CMP_MAP retains
 * at most ~33 buckets (one per Hamming-distance step at 32-bit width),
 * which is too few for the gradient to systematically beat naive given
 * libafl's largely-byte-level mutator schedule. Each "best-distance"
 * advance is destroyed by the next BytesRandSetMutator before another
 * single-bit flip lands.
 *
 * v2 reframes the test: K narrow (1-byte) literal-equality CMPs in a
 * GATING CHAIN, each emitting its own coverage edge AND its own CMP_MAP
 * Hamming-distance bucket. VP retains seeds at progressively-better
 * distance per CMP independently; the gradient compounds across the
 * chain. Naive's per-attempt cost is 1/256^K (geometric collapse).
 *
 * Predicted dose-response on trap crashes (primary pair: vp vs naive):
 *   - naive:  geometric collapse at K>=4 (1/2^32 attempts; near-zero crashes)
 *   - vp:     ~linear scan time in K (each CMP's gradient walks
 *             independently to its TARGET byte; mutations on already-good
 *             bytes are stable because they're retained on prior-CMP
 *             coverage)
 *   - vp/naive ratio grows monotonically with CHAIN_DEPTH; predicted
 *     to exceed 100x at K>=4 and naive UNREACHABLE at K>=8.
 *
 * The same harness ALSO predicts cmp >> naive (I2S substitutes each
 * byte one-shot) and vpc ≈ cmp (vpc has cmp's I2S which solves K narrow
 * CMPs trivially), but the strict-2-fuzzer rule keeps this template
 * focused on the (vp, naive) primary pair. The (cmp, naive) corroboration
 * is essentially i2s_magic_number_gate with WIDTH=1 chained K times; not
 * re-claimed here.
 *
 * Falsifier. If vp/naive ratio is FLAT or DECAYS with CHAIN_DEPTH, VP's
 * gradient is NOT compounding across CMPs. Possible alternatives: (a)
 * libafl's CMP_MAP doesn't actually retain best-distance buckets the way
 * documentation suggests; (b) libafl's mutator schedule produces too few
 * single-bit flips for the gradient to walk effectively even at K=8.
 * Either is a substantive finding about libafl behavior.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef CHAIN_DEPTH
#define CHAIN_DEPTH 4
#endif

#if CHAIN_DEPTH != 2 && CHAIN_DEPTH != 4 && \
    CHAIN_DEPTH != 8 && CHAIN_DEPTH != 16
#error "CHAIN_DEPTH must be one of {2, 4, 8, 16}"
#endif

/* 16 distinct 1-byte targets — diverse enough that no two share popcount-0
 * with common input bytes (avoid degenerate cases where 0x00 or 0xFF inputs
 * are trivially closest by Hamming). */
static const uint8_t TARGETS[16] = {
    0x4D, 0x5A, 0xA9, 0x33, 0xC7, 0x1E, 0xB6, 0x91,
    0x52, 0xE3, 0x7C, 0x08, 0xDF, 0x65, 0xAB, 0x42,
};

static volatile uint8_t g_sink;

/* One noinline function per chain position. libafl's coverage map gets
 * one edge per position, CMP_MAP gets one Hamming-distance bucket per
 * position. VP retains best-distance seeds independently per edge so
 * the gradient compounds. */
#define CMP_FN(N)                                                            \
    __attribute__((noinline))                                                \
    static int cmp_##N(uint8_t v) {                                          \
        g_sink ^= v;                                                         \
        if (v != TARGETS[N]) return 0;                                       \
        return 1;                                                            \
    }

CMP_FN(0)  CMP_FN(1)  CMP_FN(2)  CMP_FN(3)
CMP_FN(4)  CMP_FN(5)  CMP_FN(6)  CMP_FN(7)
CMP_FN(8)  CMP_FN(9)  CMP_FN(10) CMP_FN(11)
CMP_FN(12) CMP_FN(13) CMP_FN(14) CMP_FN(15)

typedef int (*cmp_fn_t)(uint8_t);
static const cmp_fn_t CMP_TABLE[16] = {
    cmp_0,  cmp_1,  cmp_2,  cmp_3,
    cmp_4,  cmp_5,  cmp_6,  cmp_7,
    cmp_8,  cmp_9,  cmp_10, cmp_11,
    cmp_12, cmp_13, cmp_14, cmp_15,
};

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < CHAIN_DEPTH) return 0;
    for (int i = 0; i < CHAIN_DEPTH; i++) {
        if (!CMP_TABLE[i](data[i])) return 0;
    }
    __builtin_trap();
    return 0;
}
