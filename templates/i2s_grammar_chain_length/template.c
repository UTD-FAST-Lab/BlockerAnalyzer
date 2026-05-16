/**
 * i2s_grammar_chain_length: parameterized harness for the
 * (value_profile_cmplog, value_profile) source pair on the I2S delta —
 * the per-branch winner is vpc, technique delta is I2S substitution.
 *
 * Real-target origin (libpcap, gencode.c:841, branch 799):
 *   `if (bpf_optimize(&cstate.ic, p->errbuf) == -1) {`
 * Side-A (vp, blocked) seeds carry filterSize=1 -> empty filter,
 * optimizer trivially returns 0, branch goes False. Side-B (vpc,
 * resolves) seeds carry filterSize=9 with ASCII filter "0=01%4*0" /
 * "0=00%4*0" -- a parseable pcap-filter expression that compiles to a
 * BPF program containing `BPF_MOD K==0`, which the optimizer's
 * constant-fold path (optimize.c:809) catches via
 * `opt_error("modulus by zero")` -> longjmp -> bpf_optimize returns -1
 * -> branch goes True.
 *
 * Hypothesis. Reaching the trap requires the input to lay out a chain
 * of CHAIN_LEN multi-byte tokens at fixed offsets, each drawn from a
 * compile-time dictionary, with separator bytes between them. Each
 * token check is one strncmp/memcmp call -- one I2S dictionary entry
 * per token. The trap fires only after ALL CHAIN_LEN tokens land
 * correctly AND a final divisor byte equals zero (mirroring libpcap's
 * "valid filter compiles AND optimizer hits a constant-fold zero
 * divisor" reachability gate).
 *
 *   - vpc (= cmplog + value_profile): cmplog's CmpLogObserver intercepts
 *     each strncmp dispatching against a dictionary entry, logs the
 *     literal token bytes into the I2S dictionary, and I2SRandReplace
 *     splices the logged token wholesale into a candidate input offset
 *     in ONE mutation. Each slot succeeds in O(1) attempts modulo
 *     dictionary size. Yield over CHAIN_LEN slots is roughly linear in
 *     CHAIN_LEN (each slot is one independent substitution).
 *
 *   - vp alone (no I2S): CMP_MAP records per-edge Hamming distance
 *     between input bytes and the keyword. The gradient at slot i is a
 *     SEPARATE coverage edge from slot j, so flipping bits in slot i
 *     gives no signal until slot 0..i-1 are correct. Each slot is an
 *     independent 4-byte equality CMP whose gradient costs
 *     ~256-per-byte useful mutations. Compound yield over CHAIN_LEN
 *     slots is (1/256)^(4*CHAIN_LEN) per random attempt, which decays
 *     exponentially.
 *
 *   - vpc/vp ratio therefore grows as ~256^(4*CHAIN_LEN) -- monotone
 *     increasing, divergent at large CHAIN_LEN.
 *
 * CHAIN_LEN is the program-side knob. KEYWORD_LEN is fixed (= 4) so
 * the curve isolates the chain-length axis. This is the orthogonal
 * complement to i2s_pair_relational_lookup, which fixes CHAIN_LEN=2
 * (pair) and varies DICT_SIZE: here we fix dictionary at 8 entries and
 * vary chain length.
 *
 * Predicted dose-response (CHAIN_LEN in {1, 2, 4, 8}):
 *   - L=1: trivial. vp's gradient on a single 4-byte equality CMP is
 *     hard but tractable in 600s at modest mutation rate. Both fuzzers
 *     resolve. Ratio ~1-3x.
 *   - L=2: vp must independently land 2 slots; each slot's CMP edge
 *     is independent. Ratio ~10-30x.
 *   - L=4: matches the libpcap real-target chain depth. vp ~ 0 within
 *     budget. Ratio ~100-1000x or vp completely blocked.
 *   - L=8: vp = 0. vpc still resolves at geometric rate. Ratio
 *     diverges.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef CHAIN_LEN
#define CHAIN_LEN 4
#endif

#ifndef KEYWORD_LEN
#define KEYWORD_LEN 4
#endif

#if CHAIN_LEN != 1 && CHAIN_LEN != 2 && CHAIN_LEN != 4 && CHAIN_LEN != 8
#error "CHAIN_LEN must be in {1,2,4,8}"
#endif

#if KEYWORD_LEN != 4
#error "KEYWORD_LEN is fixed at 4 to isolate the chain-length axis"
#endif

/* Per-slot keyword dictionary. Each slot has its own designated
 * 4-byte literal that must appear at the slot's offset. We use 8
 * distinct literals so all CHAIN_LEN<=8 slots can use unique
 * keywords. */

static const char g_kw_0[KEYWORD_LEN] = { 't','c','p','f' };
static const char g_kw_1[KEYWORD_LEN] = { 'u','d','p','q' };
static const char g_kw_2[KEYWORD_LEN] = { 'h','o','s','t' };
static const char g_kw_3[KEYWORD_LEN] = { 'p','o','r','t' };
static const char g_kw_4[KEYWORD_LEN] = { 'i','p','v','4' };
static const char g_kw_5[KEYWORD_LEN] = { 'i','p','v','6' };
static const char g_kw_6[KEYWORD_LEN] = { 'g','r','e','x' };
static const char g_kw_7[KEYWORD_LEN] = { 'a','r','p','y' };

#define SEP_CHAR '|'

#define SLOT_BYTES (KEYWORD_LEN + 1)
#define INPUT_FOOTPRINT (SLOT_BYTES * CHAIN_LEN + 1)

static volatile uint32_t g_sink;

#define DEFINE_LEX_KW(I)                                                  \
    __attribute__((noinline))                                             \
    static int lex_kw_##I(const uint8_t *p) {                             \
        return memcmp(p, g_kw_##I, KEYWORD_LEN) == 0;                     \
    }

DEFINE_LEX_KW(0)
DEFINE_LEX_KW(1)
DEFINE_LEX_KW(2)
DEFINE_LEX_KW(3)
DEFINE_LEX_KW(4)
DEFINE_LEX_KW(5)
DEFINE_LEX_KW(6)
DEFINE_LEX_KW(7)
#undef DEFINE_LEX_KW

typedef int (*lex_fn_t)(const uint8_t *);
static const lex_fn_t g_lex_table[8] = {
    lex_kw_0, lex_kw_1, lex_kw_2, lex_kw_3,
    lex_kw_4, lex_kw_5, lex_kw_6, lex_kw_7
};

__attribute__((noinline))
static int lex_sep(uint8_t b) {
    return b == (uint8_t)SEP_CHAR;
}

/* "Optimizer" stage: only reachable if all CHAIN_LEN slots matched.
 * Mirrors bpf_optimize's constant-fold path: we accumulate the slot
 * indices into an integer and check divisor==0 at the end. */
__attribute__((noinline))
static int opt_constant_fold(uint32_t accum, uint8_t divisor_byte) {
    g_sink ^= accum;
    if (divisor_byte == 0 && accum != 0) {
        return -1;  /* error path -- equivalent to bpf_optimize -1 */
    }
    return 0;
}

__attribute__((noinline))
static int driver_compile_and_optimize(const uint8_t *data, size_t size) {
    if (size < INPUT_FOOTPRINT) return 0;

    uint32_t accum = 0;

    /* Each slot must lex its designated keyword then the separator. */
    for (int i = 0; i < CHAIN_LEN; i++) {
        if (!g_lex_table[i](data + i * SLOT_BYTES)) return 0;
        if (!lex_sep(data[i * SLOT_BYTES + KEYWORD_LEN])) return 0;
        accum = (accum << 8) ^ (uint32_t)(0x11u + i * 0x11u);
    }

    /* Final byte = "divisor". Mirrors a `BPF_MOD K` instruction whose
     * K is constant-folded and checked against zero. */
    uint8_t divisor = data[CHAIN_LEN * SLOT_BYTES];
    return opt_constant_fold(accum, divisor);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    int rc = driver_compile_and_optimize(data, size);
    if (rc == -1) {
        __builtin_trap();
    }
    return 0;
}
