/**
 * i2s_pair_relational_lookup: parameterized harness for the
 * (value_profile_cmplog, value_profile) source pair where the I2S delta
 * is the per-branch winner.
 *
 * Real-target origin. lcms cmsio0.c:706, branch 56,
 *   `if (desc1->ElemCount != desc2->ElemCount) return FALSE;`
 * inside CompatibleTypes(desc1, desc2). The function is called from
 * _cmsReadHeader's tag-pair iteration: for each pair of tag-table
 * entries that share (offset, size), the static cmsTagDescriptor for
 * each tag-sig FOURCC is looked up; the pair must satisfy
 *   nSupportedTypes_A == nSupportedTypes_B  AND  ElemCount_A != ElemCount_B
 * for the True side to fire. The descriptor table (cmstypes.c:5798) is
 * binary-resident; the input controls which two tag-sig FOURCCs name
 * descriptors that get compared.
 *
 * Hypothesis. This is qualitatively distinct from the single-CMP
 * `i2s_magic_number_gate` family. Here the winning input must supply TWO
 * distinct multi-byte literals BOTH drawn from the same compile-time
 * dictionary, where the trap fires only on a RELATIONAL property of the
 * pair after a static lookup.
 *
 *   - cmplog (and vpc): I2S logs every constant the program compares —
 *     including each FOURCC the lookup_descriptor() helper checks
 *     against. The dictionary collects all DICT_SIZE FOURCCs. The
 *     mutator substitutes them into candidate input positions; with two
 *     tag slots in the input, two independent substitutions reach the
 *     relational test. cmp must chain TWO substitutions where each one
 *     individually does not fire the trap — so the search is
 *     pair-relational, not single-shot. Substitution rate per attempt
 *     is ~(1/DICT_SIZE) for landing each slot in the dictionary; per
 *     pair ~(1/DICT_SIZE)^2.
 *   - vp alone (no I2S): cannot get FOURCC bytes into the slots —
 *     each FOURCC is a 4-byte equality CMP against a literal, and
 *     CMP_MAP gradient over Hamming distance to a literal is a 256-step
 *     gradient per byte. With TWO independent slots required, the
 *     gradient compounds — vp is much slower than vpc and within the
 *     budget never reaches the relational test.
 *   - vpc (= cmplog + value_profile): I2S substitutes both slots; the
 *     extra CMP_MAP gradient does not change the qualitative outcome
 *     here because the dictionary substitution mechanism dominates.
 *
 * Compile-time parameter:
 *   DICT_SIZE in {4, 16, 64, 256}
 *     The number of distinct 4-byte literals the program compares
 *     against. Each literal becomes one I2S dictionary entry.
 *
 *   Predicted dose-response (vpc vs vp):
 *     - vp's resolution probability ≈ (1/2^32)^2 per attempt regardless
 *       of DICT_SIZE — geometric collapse, ~0 crashes everywhere.
 *     - vpc's resolution count ~ 1/DICT_SIZE^2 per attempt.
 *     - vpc/vp ratio grows monotonically in DICT_SIZE.
 *
 * Trap construction. The harness exposes a "tag table" of TWO slots,
 * each carrying a 4-byte FOURCC. Each FOURCC is looked up against a
 * compile-time dictionary of DICT_SIZE entries; the lookup returns a
 * (group_id, value) pair from a static descriptor table. Trap fires
 * iff:
 *   1. Both lookups succeed (fourcc is in dictionary).
 *   2. group_id_A == group_id_B  (mirrors nSupportedTypes equality).
 *   3. value_A != value_B        (mirrors ElemCount inequality).
 *
 * Dictionary entries (2k, 2k+1) share group_id=k but have distinct
 * value, so a valid trap-pair always exists.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef DICT_SIZE
#define DICT_SIZE 16
#endif

#if DICT_SIZE != 4 && DICT_SIZE != 16 && DICT_SIZE != 64 && DICT_SIZE != 256
#error "DICT_SIZE must be one of {4, 16, 64, 256}"
#endif

#define GROUP_COUNT (DICT_SIZE / 2)

typedef struct {
    uint32_t fourcc;
    uint32_t group_id;
    uint32_t value;
} dict_entry_t;

/* FOURCC builder: 3 ASCII letters + 1 digit, deterministic per index. */
#define MAKE_FOURCC(i) (uint32_t)( \
    (((uint32_t)('A' + ((i) / 26 / 26 % 26))) <<  0) | \
    (((uint32_t)('A' + ((i) / 26 % 26)))      <<  8) | \
    (((uint32_t)('A' + ((i) % 26)))           << 16) | \
    (((uint32_t)('0' + ((i) % 10)))           << 24))

#if DICT_SIZE == 4
#define DICT_LIST(M) M(0) M(1) M(2) M(3)
#elif DICT_SIZE == 16
#define DICT_LIST(M) \
    M(0) M(1) M(2) M(3) M(4) M(5) M(6) M(7) \
    M(8) M(9) M(10) M(11) M(12) M(13) M(14) M(15)
#elif DICT_SIZE == 64
#define DICT_LIST(M) \
    M(0) M(1) M(2) M(3) M(4) M(5) M(6) M(7) M(8) M(9) \
    M(10) M(11) M(12) M(13) M(14) M(15) M(16) M(17) M(18) M(19) \
    M(20) M(21) M(22) M(23) M(24) M(25) M(26) M(27) M(28) M(29) \
    M(30) M(31) M(32) M(33) M(34) M(35) M(36) M(37) M(38) M(39) \
    M(40) M(41) M(42) M(43) M(44) M(45) M(46) M(47) M(48) M(49) \
    M(50) M(51) M(52) M(53) M(54) M(55) M(56) M(57) M(58) M(59) \
    M(60) M(61) M(62) M(63)
#elif DICT_SIZE == 256
#define ROW32(B) \
    M(B+0)  M(B+1)  M(B+2)  M(B+3)  M(B+4)  M(B+5)  M(B+6)  M(B+7)  \
    M(B+8)  M(B+9)  M(B+10) M(B+11) M(B+12) M(B+13) M(B+14) M(B+15) \
    M(B+16) M(B+17) M(B+18) M(B+19) M(B+20) M(B+21) M(B+22) M(B+23) \
    M(B+24) M(B+25) M(B+26) M(B+27) M(B+28) M(B+29) M(B+30) M(B+31)
#define DICT_LIST(M) \
    ROW32(0) ROW32(32) ROW32(64) ROW32(96) \
    ROW32(128) ROW32(160) ROW32(192) ROW32(224)
#endif

#define DICT_ENTRY(I) { MAKE_FOURCC(I), (I) / 2u, (uint32_t)(I) },
static const dict_entry_t DICT[DICT_SIZE] = { DICT_LIST(DICT_ENTRY) };
#undef DICT_ENTRY

/* Linear scan with explicit literal compares: each iteration emits one
 * trace_const_cmp_4 (DICT[i].fourcc as the constant operand). I2S
 * collects every entry into the dictionary. No early break — match the
 * real-target where lookup walks the full descriptor table. */
__attribute__((noinline))
static int lookup_descriptor(uint32_t fourcc,
                             uint32_t *out_group, uint32_t *out_value) {
    int found = 0;
    uint32_t g = 0, v = 0;
    for (uint32_t i = 0; i < DICT_SIZE; i++) {
        if (fourcc == DICT[i].fourcc) {
            g = DICT[i].group_id;
            v = DICT[i].value;
            found = 1;
        }
    }
    *out_group = g;
    *out_value = v;
    return found;
}

__attribute__((noinline))
static uint32_t read_u32_le(const uint8_t *p) {
    return ((uint32_t)p[0]      ) |
           ((uint32_t)p[1] <<  8) |
           ((uint32_t)p[2] << 16) |
           ((uint32_t)p[3] << 24);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /* Two tag slots: 4-byte FOURCC each at offsets 0 and 8. */
    if (size < 12) return 0;

    uint32_t fA = read_u32_le(data + 0);
    uint32_t fB = read_u32_le(data + 8);

    if (fA == fB) return 0;  /* require two distinct dictionary entries */

    uint32_t gA = 0, vA = 0, gB = 0, vB = 0;
    int okA = lookup_descriptor(fA, &gA, &vA);
    int okB = lookup_descriptor(fB, &gB, &vB);

    if (!okA || !okB) return 0;
    if (gA != gB) return 0;        /* mirror nSupportedTypes equality   */
    if (vA == vB) return 0;        /* mirror ElemCount inequality       */

    __builtin_trap();
    return 0;
}
