/**
 * i2s_runtime_bound_substitution: parameterized harness for the
 * (value_profile_cmplog, value_profile) source pair — the
 * "I2S-substitutes-runtime-input-length-into-bytecode-operand" mechanism.
 *
 * Originating real target: libpcap bpf_filter.c:191
 *   case BPF_LD|BPF_H|BPF_IND:
 *       k = X + pc->k;
 *       if (X > buflen || pc->k > buflen - X ||
 *           sizeof(int16_t) > buflen - k) {  // line 191 — blocked side T
 *           return 0;
 *       }
 *       A = EXTRACT_SHORT(&p[k]);
 *
 * `pc->k` is an immediate field read from a BPF program byte in the input
 * (the BPF filter program is itself input-derived in fuzz_both / fuzz_pcap).
 * `buflen` is the runtime input size — also input-derived but NOT a
 * compile-time constant. Both are "runtime values" that vary per execution.
 *
 * Hypothesis. cmplog's CmpLogObserver registers
 * __sanitizer_cov_trace_cmp{1,2,4,8} (the variable-vs-variable hooks)
 * at every integer comparison and records BOTH operands as logged
 * literals at run time. The I2SRandReplace mutator then splices either
 * operand into input byte windows where matching values currently appear.
 * For a CMP shaped `pc->k vs buflen` where:
 *   - pc->k is read from input bytes at a known offset (so I2S can
 *     locate it in the input and overwrite it)
 *   - buflen is the input size (so I2S can read it as a logged literal)
 * a single I2SRandReplace mutation that writes `buflen` into the pc->k
 * offset will satisfy `pc->k >= buflen` (or `buflen - k < SAFE_GAP`) and
 * flip the bound check to T in one step.
 *
 * value_profile lacks I2S. Its CMP_MAP gradient does record per-edge
 * Hamming distance between operands, but two factors make the gradient
 * weak here:
 *   (a) buflen varies per execution — the comparand is moving, so
 *       successive seeds cannot stably "climb" toward a fixed target.
 *   (b) the gradient must close ~W bytes of Hamming distance (8W bits)
 *       via random bit-flips, scaling exponentially in W when the
 *       comparand width grows.
 * I2S is width-invariant (one logged literal, one splice). VP scales in W.
 *
 * Predicted dose-response. vpc/vp ratio grows monotonically with the
 * width W of the bytecode operand (pc->k) read from input. At W=1, vp's
 * gradient closes 8 bits of Hamming distance reasonably; at W=8 the
 * gradient must close 64 bits while the target moves between executions.
 *
 * Compile-time parameter:
 *   K_WIDTH in {1, 2, 4, 8}
 *     1: pc->k is a uint8_t  — vp catches up via 1-byte gradient
 *     2: pc->k is a uint16_t — vp slow but feasible
 *     4: pc->k is a uint32_t — vp far behind vpc
 *     8: pc->k is a uint64_t — vp ~ 0; vpc still resolves via I2S
 *
 * STRICTLY TWO FUZZERS PER TEMPLATE. Primary pair: A=value_profile_cmplog,
 * B=value_profile.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef K_WIDTH
#define K_WIDTH 4
#endif

#if K_WIDTH != 1 && K_WIDTH != 2 && K_WIDTH != 4 && K_WIDTH != 8
#error "K_WIDTH must be one of {1, 2, 4, 8}"
#endif

#if   K_WIDTH == 1
typedef uint8_t  k_t;
#elif K_WIDTH == 2
typedef uint16_t k_t;
#elif K_WIDTH == 4
typedef uint32_t k_t;
#elif K_WIDTH == 8
typedef uint64_t k_t;
#endif

#define SAFE_GAP 2u
#define PREAMBLE_BYTES 16

static volatile uint64_t g_sink;

__attribute__((noinline))
static k_t read_k(const uint8_t *p) {
    k_t v;
    memcpy(&v, p, K_WIDTH);
    return v;
}

__attribute__((noinline))
static int bpf_ld_h_ind_check(uint64_t pc_k, uint64_t X, uint64_t buflen) {
    /* Three input-derived runtime CMPs — each emits a sancov
     * trace_cmp{4,8} (variable-vs-variable) hook. CmpLogObserver records
     * both operands. I2SRandReplace can splice EITHER operand back into
     * input byte windows. */
    if (X > buflen) return 1;
    if (pc_k > buflen - X) return 1;
    if ((uint64_t)SAFE_GAP > buflen - (X + pc_k)) return 1;
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /* buflen is the runtime input size — varies per execution, exactly
     * as in libpcap where buflen = packet length. */
    uint64_t buflen = (uint64_t)size;

    if (size < (size_t)(PREAMBLE_BYTES + K_WIDTH)) return 0;

    /* pc->k is read from a fixed offset inside the input — the BPF
     * program operand. Width K_WIDTH is the knob. */
    k_t k_field = read_k(data + PREAMBLE_BYTES);
    uint64_t pc_k = (uint64_t)k_field;

    /* X = 0 for simplicity — keeping X=0 gives ONE constraint to flip,
     * isolating the mechanism. */
    uint64_t X = 0;

    g_sink ^= pc_k ^ buflen;

    if (bpf_ld_h_ind_check(pc_k, X, buflen)) {
        /* Bound-fail branch — equivalent to libpcap's `return 0` path.
         * This is the "blocked side T" of the real branch. */
        __builtin_trap();
    }

    return 0;
}
