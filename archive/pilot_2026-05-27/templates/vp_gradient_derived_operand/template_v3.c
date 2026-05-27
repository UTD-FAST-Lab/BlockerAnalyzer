/**
 * vp_gradient_derived_operand v3: faithful test of the bijective-transform-
 * derivation feature.
 *
 * v1 (refuted, 2026-05-03): single 32-bit equality CMP + optional XOR
 * derivation. Refuted because at 32-bit width, CMP_MAP retains only ~33
 * Hamming-distance buckets — too few stepping stones for VP's gradient
 * to systematically beat naive given LibAFL's byte-rand-heavy mutator
 * schedule. v1 never actually got to test depth-invariance because vp
 * couldn't even bootstrap at depth=0.
 *
 * v2 (reproduced, 2026-05-04): K independent narrow byte-CMPs with NO
 * transform — pivoted to a "chain-compounding gradient" mechanism that
 * is structurally distinct from the bijective-derivation feature this
 * template was created for. v2 has been moved to its own template
 * vp_chain_compounding_gradient (TODO if not split yet); the current
 * template returns to its original feature claim.
 *
 * v3 reframes v1's design with two changes:
 *   1. Operand widened from 32-bit to 64-bit. CMP_MAP now retains up
 *      to 65 best-distance buckets per cmp, giving VP roughly 2x more
 *      stepping stones to refine through. Still not many — the test
 *      may still fail to bootstrap at depth=0, in which case the
 *      verdict is "single-CMP gradient too narrow at any synth-budget
 *      width," NOT "bijective transform degrades gradient."
 *   2. Each derivation layer is a noinline call to a function-pointer
 *      table entry that writes to a volatile sink. This prevents
 *      clang -O2 from folding the XOR chain into a single XOR with the
 *      composed mask (which would erase the per-layer coverage edges
 *      and defeat depth-discrimination).
 *
 * Knob: DERIVATION_DEPTH ∈ {0, 1, 2, 4}
 *   = number of bijective XOR layers between input read and the CMP.
 *   Each layer XORs with a distinct 64-bit constant. Each is its own
 *   inverse: layer_N(layer_N(v)) == v. Composition of XORs is XOR
 *   with the cumulative mask, so the bit-for-bit Hamming distance
 *   between the layered output and the trap target equals the
 *   Hamming distance between the raw input and the "pre-image"
 *   (target XOR cumulative_mask). VP's gradient over input bytes is
 *   ISOMORPHIC to its gradient at the CMP site under any depth ≥ 0.
 *
 * Predicted dose-response on trap crashes (primary pair: vp vs naive):
 *   - naive: 1/2^64 per attempt regardless of DERIVATION_DEPTH.
 *           Essentially 0 crashes / 600s at every dose.
 *   - vp:    IF the 64-bit gradient is wide enough to bootstrap at
 *           depth=0, vp resolves with some non-zero rate. The ratio
 *           vp/naive at depth=0 is the floor for the depth-invariance
 *           test. At depth ≥ 1, vp's rate should be APPROXIMATELY
 *           FLAT — the bijective transform preserves the gradient.
 *           Predicted: vp_rate(depth=4) / vp_rate(depth=0) ∈ [0.5, 2.0]
 *           (within an order of magnitude — depth-invariance).
 *
 * Verdict criteria:
 *   - reproduced: vp >> naive at depth=0 AND vp_rate at depth ∈ {1,2,4}
 *     is within 2x of vp_rate at depth=0 (depth-invariance holds).
 *   - partially_reproduced: vp >> naive at depth=0 but rate degrades
 *     monotonically with depth (transform partially attenuates gradient
 *     — possibly because each layer adds noise that the gradient must
 *     re-traverse).
 *   - refuted_for_single_cmp_gradient_narrowness: vp ≈ naive at depth=0.
 *     Gradient too narrow even at 64-bit width. Mechanism untestable
 *     within this synthesis design — does NOT refute the bijective-
 *     derivation feature itself; refutes only this specific synthetic.
 *   - refuted: vp >> naive at depth=0 but collapses to ≈ naive at
 *     depth ≥ 1. Bijective transform actively destroys gradient —
 *     the load-bearing claim of the feature is wrong.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef DERIVATION_DEPTH
#define DERIVATION_DEPTH 0
#endif

#if DERIVATION_DEPTH != 0 && DERIVATION_DEPTH != 1 && \
    DERIVATION_DEPTH != 2 && DERIVATION_DEPTH != 4
#error "DERIVATION_DEPTH must be one of {0, 1, 2, 4}"
#endif

/* Per-layer XOR masks. Each is a distinct 64-bit constant chosen with
 * roughly balanced popcount (~32 ones each) so each layer flips
 * approximately half the bits — no degenerate "0 mask" or "all-ones"
 * shortcuts. Constants are FNV-style mixing constants, no algebraic
 * relationship that the compiler could exploit. */
static const uint64_t XOR_MASKS[4] = {
    0xC3A5C85C97CB3127ULL,
    0xB492B66FBE98F273ULL,
    0x9AE16A3B2F90404FULL,
    0xCBF29CE484222325ULL,
};

/* The trap target. Compared as a single 64-bit equality CMP (one
 * trace_const_cmp_8 site emitted by the sancov instrumentation). */
#define TRAP_TARGET 0xDEADBEEFCAFEBABEULL

/* Volatile sink — each layer writes to it before returning. Forces
 * the compiler to keep the layer call as a real side-effect, which
 * prevents folding the chain into a single XOR with the composed
 * mask (which would collapse all depths to depth=0 at the IR level). */
static volatile uint8_t g_sink;

/* One noinline function per layer index. Each emits one coverage edge
 * (entry pc-guard) and performs the XOR + sink write. */
#define LAYER_FN(N)                                                          \
    __attribute__((noinline))                                                \
    static uint64_t layer_##N(uint64_t v) {                                  \
        g_sink = (uint8_t)v;                                                 \
        return v ^ XOR_MASKS[N];                                             \
    }
LAYER_FN(0)
LAYER_FN(1)
LAYER_FN(2)
LAYER_FN(3)
#undef LAYER_FN

typedef uint64_t (*layer_fn_t)(uint64_t);
static const layer_fn_t LAYER_TABLE[4] = {
    layer_0, layer_1, layer_2, layer_3,
};

__attribute__((noinline))
static uint64_t read_u64_le(const uint8_t *p) {
    return ((uint64_t)p[0]      ) | ((uint64_t)p[1] <<  8) |
           ((uint64_t)p[2] << 16) | ((uint64_t)p[3] << 24) |
           ((uint64_t)p[4] << 32) | ((uint64_t)p[5] << 40) |
           ((uint64_t)p[6] << 48) | ((uint64_t)p[7] << 56);
}

/* Apply the chain via indirect call through a function-pointer table.
 * The compiler cannot constant-fold across an indirect call boundary
 * (without aggressive devirtualization that clang -O2 doesn't do here). */
__attribute__((noinline))
static uint64_t apply_chain(uint64_t v) {
    for (int i = 0; i < DERIVATION_DEPTH; i++) {
        v = LAYER_TABLE[i](v);
    }
    return v;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 8) return 0;
    uint64_t v = read_u64_le(data);

    /* DERIVATION_DEPTH bijective layers between the input read and
     * the CMP. depth=0 means the raw input is compared directly. */
    v = apply_chain(v);

    /* THE single equality CMP at the trap. One trace_const_cmp_8
     * hook fires here per execution. CMP_MAP records the smallest
     * Hamming distance ever seen between v and TRAP_TARGET. VP
     * retains the seed achieving each new best-distance bucket. */
    if (v == TRAP_TARGET) {
        __builtin_trap();
    }

    return 0;
}
