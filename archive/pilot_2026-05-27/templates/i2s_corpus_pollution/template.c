/**
 * i2s_corpus_pollution: parameterized harness for the (value_profile_cmplog,
 * cmplog) source pair — the synergy_cmplog_plus_vp pattern.
 *
 * Hypothesis. cmp's I2S substitution dictionary collects every CMP
 * constant the program executes. With K useful chain operands plus N
 * noise CMP sites, useful-substitution rate per attempt is K/(K+N);
 * over a K-step chain it compounds to (K/(K+N))^K. Exponential dilution
 * kills cmp at high N.
 *
 * vpc (cmplog + value_profile combined) does NOT suffer this dilution:
 *   - At low pollute, I2S still works and gives vpc cmp's normal yield.
 *   - At high pollute where I2S dies, vp's CMP_MAP gradient feedback
 *     tracks Hamming distance to chain operands directly. No dictionary,
 *     no substitution, no dilution. The gradient still steers the corpus
 *     toward the trap.
 *   - vpc therefore degrades gracefully while cmp drops to zero.
 *
 * Predicted: vpc resolves at every COST_INNER value; cmp's resolution
 * count decays exponentially in COST_INNER. Verified 2026-04-27 (5
 * trials × 600s × 4 COST_INNER points): cmp median 993 → 109 → 0 → 0,
 * vpc median 632 → 376 → 258 → 6.
 *
 * Mechanism (3 axes from round-9):
 *   1. Input-to-operand distance: state-machine accumulator means
 *      cmp's I2S can't substitute the trap operand directly.
 *   2. Substitute-chain length: trap requires 4 specific opcodes in
 *      4 specific positions; cmp must chain 4 successful substitutions.
 *   3. Metadata pollution: COST_INNER selects how many noise CMPs are
 *      logged per execution (saturates at 64 unique entries).
 *
 * COST_INNER is the program-side knob. value_profile and naive are
 * also reported as supporting context — vp is "slow but persistent"
 * (CMP_MAP gradient alone, no I2S), naive is bimodal (high-variance
 * stochastic at low pollute, blocks at higher pollute).
 */

#include <stdint.h>
#include <stddef.h>

#ifndef COST_INNER
#define COST_INNER 0
#endif

/* ── 64-entry pollute table (same as rounds 3/5) ── */

static volatile uint32_t g_cost_sink;

#define POLLUTE_LIST(M) \
  M( 0,0x10000001u) M( 1,0x10000002u) M( 2,0x10000003u) M( 3,0x10000004u) \
  M( 4,0x10000005u) M( 5,0x10000006u) M( 6,0x10000007u) M( 7,0x10000008u) \
  M( 8,0x10000009u) M( 9,0x1000000Au) M(10,0x1000000Bu) M(11,0x1000000Cu) \
  M(12,0x1000000Du) M(13,0x1000000Eu) M(14,0x1000000Fu) M(15,0x10000010u) \
  M(16,0x20000011u) M(17,0x20000012u) M(18,0x20000013u) M(19,0x20000014u) \
  M(20,0x20000015u) M(21,0x20000016u) M(22,0x20000017u) M(23,0x20000018u) \
  M(24,0x20000019u) M(25,0x2000001Au) M(26,0x2000001Bu) M(27,0x2000001Cu) \
  M(28,0x2000001Du) M(29,0x2000001Eu) M(30,0x2000001Fu) M(31,0x20000020u) \
  M(32,0x30000021u) M(33,0x30000022u) M(34,0x30000023u) M(35,0x30000024u) \
  M(36,0x30000025u) M(37,0x30000026u) M(38,0x30000027u) M(39,0x30000028u) \
  M(40,0x30000029u) M(41,0x3000002Au) M(42,0x3000002Bu) M(43,0x3000002Cu) \
  M(44,0x3000002Du) M(45,0x3000002Eu) M(46,0x3000002Fu) M(47,0x30000030u) \
  M(48,0x40000031u) M(49,0x40000032u) M(50,0x40000033u) M(51,0x40000034u) \
  M(52,0x40000035u) M(53,0x40000036u) M(54,0x40000037u) M(55,0x40000038u) \
  M(56,0x40000039u) M(57,0x4000003Au) M(58,0x4000003Bu) M(59,0x4000003Cu) \
  M(60,0x4000003Du) M(61,0x4000003Eu) M(62,0x4000003Fu) M(63,0x40000040u)

#define DEFINE_POLLUTE(I, K)                                  \
    __attribute__((noinline))                                 \
    static void pollute_##I(uint32_t v) {                     \
        if (v == (K)) g_cost_sink += (I);                     \
        else g_cost_sink ^= v ^ (K);                          \
    }
POLLUTE_LIST(DEFINE_POLLUTE)
#undef DEFINE_POLLUTE

typedef void (*pollute_fn_t)(uint32_t);
#define POLLUTE_NAME(I, K) pollute_##I,
static const pollute_fn_t pollute_table[] = { POLLUTE_LIST(POLLUTE_NAME) };
#undef POLLUTE_NAME
#define POLLUTE_TABLE_SIZE 64

__attribute__((noinline))
static uint32_t read_u32_be(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] <<  8) | ((uint32_t)p[3]      );
}

__attribute__((noinline))
static void apply_pollute(const uint8_t *data, size_t size) {
    if (COST_INNER == 0) return;
    if (size < 4) return;
    uint32_t v = read_u32_be(data);
    for (int j = 0; j < COST_INNER; j++) {
        pollute_table[j % POLLUTE_TABLE_SIZE](v);
    }
}

/* ── State-machine interpreter with chain-trap ── */

#define OP_NOP    0x00u
#define OP_LD_K   0x05u  /* CHAIN[0] — required at i=0 */
#define OP_MUL_K  0x24u  /* CHAIN[1] — required at i=1 */
#define OP_XOR_K  0x64u  /* CHAIN[2] — required at i=2 */
#define OP_ADD_K  0x04u  /* CHAIN[3] — required at i=3 */
#define OP_LDX_K  0x07u
#define OP_SUB_K  0x14u
#define OP_LSH_K  0x6cu
#define OP_RSH_K  0x74u
#define OP_OR_K   0x44u
#define OP_AND_K  0x54u
#define OP_NEG    0x84u

#define N_INSTR  8

static volatile uint32_t g_sink;

/* Per-opcode noinline handlers — distinct edges per case */
__attribute__((noinline)) static uint32_t op_nop_h(uint32_t A, uint8_t k)   { return A ^ k; }
__attribute__((noinline)) static uint32_t op_ld_h(uint32_t A, uint8_t k)    { (void)A; return (uint32_t)k * 0x101u; }
__attribute__((noinline)) static uint32_t op_mul_h(uint32_t A, uint8_t k)   { return A * ((uint32_t)k | 1u); }
__attribute__((noinline)) static uint32_t op_xor_h(uint32_t A, uint8_t k)   { return A ^ ((uint32_t)k << 8); }
__attribute__((noinline)) static uint32_t op_add_h(uint32_t A, uint8_t k)   { return A + k; }
__attribute__((noinline)) static uint32_t op_ldx_h(uint32_t A, uint8_t k)   { return A ^ ((uint32_t)k * 0x101u); }
__attribute__((noinline)) static uint32_t op_sub_h(uint32_t A, uint8_t k)   { return A - k; }
__attribute__((noinline)) static uint32_t op_lsh_h(uint32_t A, uint8_t k)   {
    unsigned s = k & 7u; return (A << s) | (A >> ((32u - s) & 31u));
}
__attribute__((noinline)) static uint32_t op_rsh_h(uint32_t A, uint8_t k)   {
    unsigned s = k & 7u; return (A >> s) | (A << ((32u - s) & 31u));
}
__attribute__((noinline)) static uint32_t op_or_h(uint32_t A, uint8_t k)    { return A | ((uint32_t)k << 16); }
__attribute__((noinline)) static uint32_t op_and_h(uint32_t A, uint8_t k)   { return A & ((uint32_t)k * 0x101u); }
__attribute__((noinline)) static uint32_t op_neg_h(uint32_t A, uint8_t k)   { (void)k; return ~A + 1u; }
__attribute__((noinline)) static uint32_t op_default_h(uint32_t A, uint8_t k) {
    return A + (uint32_t)k * 0x9E3779B9u;
}

__attribute__((noinline))
static int interp(const uint8_t *prog) {
    uint32_t A = 0;
    int hits = 0;

    for (int i = 0; i < N_INSTR; i++) {
        uint8_t op = prog[i*2];
        uint8_t k  = prog[i*2 + 1];

        switch (op) {
        case OP_NOP:   A = op_nop_h(A, k);    break;
        case OP_LD_K:
            A = op_ld_h(A, k);
            if (i == 0) hits |= 1;            /* CHAIN[0] */
            break;
        case OP_LDX_K: A = op_ldx_h(A, k);    break;
        case OP_ADD_K:
            A = op_add_h(A, k);
            if (i == 3) hits |= 8;            /* CHAIN[3] */
            break;
        case OP_SUB_K: A = op_sub_h(A, k);    break;
        case OP_MUL_K:
            A = op_mul_h(A, k);
            if (i == 1) hits |= 2;            /* CHAIN[1] */
            break;
        case OP_XOR_K:
            A = op_xor_h(A, k);
            if (i == 2) hits |= 4;            /* CHAIN[2] */
            break;
        case OP_LSH_K: A = op_lsh_h(A, k);    break;
        case OP_RSH_K: A = op_rsh_h(A, k);    break;
        case OP_OR_K:  A = op_or_h(A, k);     break;
        case OP_AND_K: A = op_and_h(A, k);    break;
        case OP_NEG:   A = op_neg_h(A, k);    break;
        default:       A = op_default_h(A, k); break;
        }

        g_sink ^= A;
    }

    return hits;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    apply_pollute(data, size);

    if (size < 16) return 0;

    int hits = interp(data);

    /* Trap requires the 4-step opcode chain at positions 0,1,2,3:
     *   OP_LD_K  at i=0
     *   OP_MUL_K at i=1
     *   OP_XOR_K at i=2
     *   OP_ADD_K at i=3
     *
     * Cmp must chain 4 substitutions; pollution makes each a 1/17 lottery.
     * Naive: each (op, position) match fires a distinct conditional → unique
     * coverage edge → seed retained → corpus accumulates partial chains. */
    if (hits == 0xF) {
        __builtin_trap();
    }
    return 0;
}
