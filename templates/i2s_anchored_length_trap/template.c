/**
 * i2s_anchored_length_trap: parameterized harness for the
 * (value_profile_cmplog, cmplog) source pair where the value_profile
 * delta rescues cmp from an I2S-anchored corpus that pins long inputs
 * away from a length-fail trap.
 *
 * Source pair: libpcap savefile.c:512:
 *   if (amt_read != sizeof(magic)) { ... return NULL; }
 * where magic[4] and amt_read = fread(&magic, 1, sizeof(magic), fp).
 * The blocked T branch is taken when amt_read != 4, i.e. the input
 * file is shorter than 4 bytes. n=3 trial outcomes: vpc resolved 1/3
 * (winning seed 5 bytes, mutators BytesDeleteMutator x2 +
 * ByteInterestingMutator + ByteIncMutator); cmp resolved 0/3
 * (all blocking seeds 20 bytes carrying pcap-magic-like prefixes
 * 02 ?? 04 ?? at offsets 0..3).
 *
 * Hypothesis. Both vpc and cmp run I2S substitution. After any input
 * of size >= 4 passes the trap CMP, libpcap's check_headers[]
 * discriminator chain compares 4-byte file headers against literal
 * pcap magic numbers (0xa1b2c3d4, 0xa1b23c4d, 0xd4c3b2a1, ...).
 * I2SRandReplace logs each comparison's literal operand and splices
 * it back into mutated inputs at offsets where it currently appears.
 * Outputs that PRESERVE the magic-anchor at offsets 0..3 are favored.
 * BytesDeleteMutator descendants of size < 4 cannot preserve the
 * anchor and get out-competed in the queue — cmp's corpus
 * monocultures at size >= 4 with byte-anchored prefixes.
 *
 * The trap CMP itself (`amt_read != sizeof(magic)`) is NOT
 * I2S-substitutable — `amt_read` is the runtime fread() return, not
 * a value present in input bytes; I2S can log the literal `4` but
 * has no offset where amt_read currently appears in input to splice
 * 4 into. I2S helps neither vpc nor cmp at the trap CMP itself.
 *
 * vpc's value_profile delta opens a second feedback channel: CMP_MAP
 * records, per integer comparison, the smallest Hamming distance ever
 * observed between operands. At the trap CMP, an input of size 3
 * produces amt_read=3 (Hamming distance 1 from 4); size 2 produces
 * amt_read=2 (distance 2); etc. CMP_MAP exposes one bucket per
 * distinct distance and retains the size-3, size-2, size-1, size-0
 * seeds as best-distance bucket holders even when I2S has no anchor
 * for them. cmp lacks this gradient: short descendants produce no
 * new edge coverage, no new I2S entry, and no gradient bucket — the
 * shrink lineage dies before reaching size 0..3.
 *
 * Compile-time parameter:
 *   N_ANCHORS ∈ {0, 1, 4, 16}
 *     = number of distinct 4-byte literal-equality CMPs the harness
 *       runs on the input WHEN size >= 4. Each CMP populates one I2S
 *       dictionary entry pinning byte content at offsets 0..3.
 *
 * Predicted dose-response on SHORT_TRAP crash count:
 *   N_ANCHORS=0:  vpc ~ cmp parity. No upstream anchor; both
 *                    fuzzers' shrink lineages reach SHORT_TRAP at
 *                    similar rates.
 *   N_ANCHORS=1:  vpc >= cmp. One anchor mildly pins offset 0..3
 *                    in cmp's corpus; vpc's gradient holds shrink
 *                    descendants.
 *   N_ANCHORS=4:  vpc >> cmp. Four anchors monoculture cmp's
 *                    corpus at size >= 4; cmp's SHORT_TRAP count
 *                    drops near zero. vpc's gradient continues to
 *                    expose Hamming buckets for size 3, 2, 1, 0.
 *   N_ANCHORS=16: vpc >>> cmp. cmp's I2S dictionary saturates;
 *                    SHORT_TRAP count = 0. vpc degrades but never
 *                    reaches zero (gradient is anchor-immune; the
 *                    16 anchors do not touch the trap CMP's operand,
 *                    so gradient channel is unpolluted).
 *
 * Acceptance: vpc median > 0 at N_ANCHORS=16 AND cmp median = 0
 * at N_ANCHORS=16 AND cmp's curve monotone non-increasing AND
 * vpc/cmp ratio monotone non-decreasing.
 *
 * Distinct from i2s_corpus_pollution: COST_INNER pollutes I2S
 * dictionary across a literal-CMP CHAIN; the trap CMP IS itself
 * I2S-substitutable; failure is dilution. Here N_ANCHORS controls
 * upstream anchors that pin corpus length; the trap CMP is
 * non-substitutable; failure is corpus monoculture. Same pair
 * (vpc, cmp), same axis_differ (value_profile), different mechanism
 * subtype.
 *
 * Distinct from i2s_anchored_seed_deviation_trap: that template's
 * primary pair is (vp, vpc) where vp wins because it has no I2S
 * splice-back. Here the pair is (vpc, cmp) where vpc wins because
 * of CMP_MAP gradient at the trap CMP. The (vp, vpc) v3 refutation
 * (libafl scheduler weight log2-saturates, can't flip direction)
 * does NOT apply — vpc's rescue here comes from per-CMP gradient
 * buckets, not from bitmap-size weight inflation.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef N_ANCHORS
#define N_ANCHORS 0
#endif

#if N_ANCHORS != 0  && \
    N_ANCHORS != 1  && \
    N_ANCHORS != 4  && \
    N_ANCHORS != 16
#error "N_ANCHORS must be one of {0, 1, 4, 16}"
#endif

/* 16 distinct 4-byte literal anchors at offset 0..3 — modeled after
 * libpcap check_headers[] discriminators (pcap, pcapng, snoop, DOS
 * Sniffer, Microsoft NM, nsec variants). */
static const uint32_t ANCHOR_MAGICS[16] = {
    0xa1b2c3d4u, 0xa1b23c4du, 0xd4c3b2a1u, 0x4d3cb2a1u,
    0x0a0d0d0au, 0xa1b2cd34u, 0x34cdb2a1u, 0x736e6f6fu,
    0x6f6f6e73u, 0x52545049u, 0x69727470u, 0x4d4f5343u,
    0x4f53434du, 0xa1b2c3cdu, 0xcdc3b2a1u, 0x4356494eu
};

static volatile uint32_t g_anchor_sink;
static volatile uint32_t g_grad_sink;

__attribute__((noinline))
static uint32_t read_u32_be(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] <<  8) | ((uint32_t)p[3]      );
}

#define ANCHOR_LIST(M) \
    M( 0) M( 1) M( 2) M( 3) M( 4) M( 5) M( 6) M( 7) \
    M( 8) M( 9) M(10) M(11) M(12) M(13) M(14) M(15)

#define DEFINE_ANCHOR(I)                                           \
    __attribute__((noinline))                                      \
    static void anchor_##I(uint32_t v) {                           \
        if (v == ANCHOR_MAGICS[I]) {                               \
            g_anchor_sink += (uint32_t)((I) + 1);                  \
        } else {                                                   \
            g_anchor_sink ^= v ^ ANCHOR_MAGICS[I];                 \
        }                                                          \
    }
ANCHOR_LIST(DEFINE_ANCHOR)
#undef DEFINE_ANCHOR

typedef void (*anchor_fn_t)(uint32_t);
#define ANCHOR_NAME(I) anchor_##I,
static const anchor_fn_t ANCHOR_TABLE[16] = { ANCHOR_LIST(ANCHOR_NAME) };
#undef ANCHOR_NAME

/* Apply N_ANCHORS literal-equality CMPs against the first 4 input
 * bytes. Each CMP populates one I2S entry pinning offsets 0..3.
 * Only fires when size >= 4 — short inputs skip the anchor block,
 * mirroring libpcap's pcap_check_header() running only after the
 * length gate at savefile.c:512 passes. */
__attribute__((noinline))
static void apply_anchors(const uint8_t *data, size_t size) {
    if (size < 4) return;
    if (N_ANCHORS == 0) return;
    uint32_t v = read_u32_be(data);
    for (int i = 0; i < N_ANCHORS; i++) {
        ANCHOR_TABLE[i](v);
    }
}

/* The length-fail trap CMP. Models libpcap savefile.c:512:
 *   if (amt_read != sizeof(magic)) ...
 * Operand A (amt_read) = min(size, 4) — the runtime fread() return.
 * Operand B = the literal 4. I2S logs `4` but has no offset where
 * amt_read currently appears in input. CMP_MAP records Hamming
 * distance |amt_read - 4| and exposes one bucket per distance. */
__attribute__((noinline))
static int length_fail_cmp(size_t size) {
    uint32_t amt_read = (size < 4) ? (uint32_t)size : 4u;
    g_grad_sink ^= amt_read;
    return amt_read != 4u;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /* Upstream anchor block — only reachable when size >= 4. Pins
     * cmp's corpus at long inputs with byte-anchored prefixes. */
    apply_anchors(data, size);

    /* The length-fail trap CMP. */
    if (length_fail_cmp(size)) {
        /* SHORT_TRAP — headline metric for the primary-pair claim.
         * Reached only by inputs of size < 4 surviving the queue
         * past the I2S splice-back pressure of upstream anchors. */
        __builtin_trap();
    }

    /* Sink to prevent dead-code elimination. */
    if (size > 0) g_grad_sink ^= data[0];
    return 0;
}
