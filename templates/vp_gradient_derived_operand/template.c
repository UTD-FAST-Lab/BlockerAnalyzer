/**
 * vp_gradient_derived_operand: parameterized harness for the
 * (value_profile, naive) primary pair where VP's CMP_MAP gradient wins
 * over naive's coverage-only baseline.
 *
 * Source: mbedtls/library/ssl_tls12_client.c branch 378,
 *   `if (ssl->tls_version > ssl->conf->max_tls_version) { ... }`
 * The `tls_version` field is computed via the bijective derivation
 *   tls_version = (255 - buf[0]) << 8 | (255 - buf[1])
 * so the runtime literal at the comparison site (e.g. 0x0303 for TLS1.2)
 * NEVER appears as bytes in the fuzzer's input — the input must contain
 * the pre-image (e.g. 0xFC 0xFC). cmplog's I2S substitution cannot bridge
 * this derivation: trace_const_cmp logs `tls_version` and `max_tls_version`
 * but I2SRandReplace looks for the LITERAL value (0x0303) in mutated
 * bytes — and 0x03 0x03 isn't there. Only VP wins, by recording
 *   popcount(tls_version XOR max_tls_version)
 * as a per-edge gradient. Bit-flip mutations on input bytes propagate
 * through the XOR-style bijection (Hamming-distance preserving) to
 * drive convergence. Naive has no such retention; it pays the full
 * geometric 1/2^MAGIC_WIDTH×8 cost.
 *
 * Empirical at the source pair (n=10): vp resolves 9/10, naive blocks
 * 10/10 (unreached or blocked); same pattern replicates as
 * value_profile_cmplog > cmplog (n_edges=2).
 *
 * Hypothesis. VP's CMP_MAP gradient is **depth-invariant** under
 * bijective bytewise XOR derivations because it operates on the
 * COMPARED value, not on input literals. We model this by chaining
 * DERIVATION_DEPTH XOR layers between input and the comparison.
 * Naive's geometric collapse to 1/2^32 per-attempt is also depth-
 * invariant (the literal-in-input changes per depth, but Hamming
 * distance to it is uniform-random for naive).
 *
 * Falsifier. The vp/naive ratio is predicted to be **FLAT across
 * DERIVATION_DEPTH**. If the ratio decays with depth, the gradient
 * is NOT depth-invariant and the mechanism story is wrong (a more
 * likely alternative would be the absence-of-literal-in-input being
 * what blocks naive — which would manifest as a depth-dependent
 * effect since at depth=0 the literal IS in input).
 *
 * Compile-time parameter:
 *   DERIVATION_DEPTH ∈ {0, 1, 2, 4} — number of bijective bytewise
 *     XOR layers applied between the input read and the equality CMP.
 *     Each layer is a noinline function so VP's CMP_MAP gets a distinct
 *     coverage edge per layer (gradient compounds per depth level on
 *     the coverage map).
 *
 * One trap site:
 *   __builtin_trap() when derive(read_u32_be(data)) == MAGIC.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef DERIVATION_DEPTH
#define DERIVATION_DEPTH 1
#endif

#if DERIVATION_DEPTH != 0 && DERIVATION_DEPTH != 1 && \
    DERIVATION_DEPTH != 2 && DERIVATION_DEPTH != 4
#error "DERIVATION_DEPTH must be one of {0, 1, 2, 4}"
#endif

#define MAGIC_WIDTH 4
#define MAGIC       0xDEADBEEFu

/* Eight distinct XOR keys for the bijection chain. We use only the
 * first DERIVATION_DEPTH keys at runtime; declaring all 8 keeps the
 * binary identical-shape across scan values for cleaner cross-scan
 * comparisons. */
static const uint32_t LAYER_KEYS[8] = {
    0x12345678u, 0xABCDEF01u, 0xCAFEBABEu, 0x55AA55AAu,
    0xF0F0F0F0u, 0x9876FEDCu, 0x0F0F0F0Fu, 0xDEADC0DEu,
};

static volatile uint32_t g_sink;

__attribute__((noinline))
static uint32_t read_u32_be(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] <<  8) | ((uint32_t)p[3]      );
}

/* Each derivation layer is a separate noinline function. VP's CMP_MAP
 * sees one edge per layer; the chain compounds Hamming-distance feedback
 * across all DERIVATION_DEPTH layers. The XOR-by-constant operation is
 * bijective and Hamming-distance preserving, so the gradient at any
 * intermediate layer maps directly to the input-bytes Hamming distance. */
#define DERIVE_LAYER(N)                                                  \
    __attribute__((noinline))                                            \
    static uint32_t derive_layer_##N(uint32_t v) {                       \
        v ^= LAYER_KEYS[N];                                              \
        g_sink ^= v;                                                     \
        return v;                                                        \
    }

DERIVE_LAYER(0)
DERIVE_LAYER(1)
DERIVE_LAYER(2)
DERIVE_LAYER(3)

__attribute__((noinline))
static uint32_t derive(uint32_t v) {
#if DERIVATION_DEPTH >= 1
    v = derive_layer_0(v);
#endif
#if DERIVATION_DEPTH >= 2
    v = derive_layer_1(v);
#endif
#if DERIVATION_DEPTH >= 4
    v = derive_layer_2(v);
    v = derive_layer_3(v);
#endif
    return v;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < MAGIC_WIDTH) return 0;
    uint32_t v = read_u32_be(data);
    uint32_t derived = derive(v);
    if (derived == MAGIC) {
        __builtin_trap();
    }
    return 0;
}
