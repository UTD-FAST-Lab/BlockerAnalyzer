/**
 * i2s_structure_preservation_bias  v3 — feedback-richness queue monoculture.
 *
 * Background. Two prior verification rounds tested the mechanism "I2S
 * splice-back mutator pins bytes at logged offsets, suppressing length-
 * shrinking mutations". Both refuted: at all scan values the augmented
 * fuzzer (vpc) won SHRINK_TRAP, opposite to the prediction. v2 diagnosis
 * highlighted that a ~12-byte starting seed (`seed-mntr`) lets BOTH
 * fuzzers reach the short-input regime without any deletion having to
 * occur — the harness allowed random short inputs to satisfy the trap
 * predicate independently of any shrinking. So the prior harness never
 * actually tested whether vpc fails to PRODUCE shorter descendants from
 * a long parent.
 *
 * v3 mechanism (refined). The dose-response axis is RE-EXAMINED:
 *
 *   1. The seed corpus contains a SINGLE long input (256 bytes) shaped
 *      to traverse all upstream literal-equality CMPs successfully.
 *   2. Each upstream CMP fires only when input length >= a per-CMP
 *      threshold; short descendants do NOT fire any of them.
 *   3. The trap (SHRINK_TRAP) is reachable only when the input is
 *      shorter than a small threshold AND the input retains a specific
 *      byte (`MARKER_BYTE`) at offset 0 that comes from the seed —
 *      random short inputs from havoc cannot reach it without preserving
 *      the seed's leading byte content.
 *   4. SEED_FEEDBACK_RICHNESS is the compile-time knob: the count of
 *      4-byte literal-equality CMPs the harness fires when the seed
 *      traverses (each emitting one coverage edge + one CMP_MAP bucket
 *      + one I2S dictionary entry).
 *
 * Predicted dose-response (v3). The hypothesis is no longer about
 * splice-back PINNING bytes via mutation. Instead it is about QUEUE
 * SELECTION:
 *
 *   - When SEED_FEEDBACK_RICHNESS=K, the long seed earns K coverage
 *     edges + K CMP_MAP best-distance buckets + K I2S-bearing edges in
 *     vpc; in vp it earns K coverage + K CMP_MAP only. The libafl
 *     scheduler weights selection by a seed's count of "best-
 *     representative" slots in the feedback set. The long seed becomes
 *     the queue's monocultural center: it owns ~K slots in vpc, ~K
 *     slots in vp (the I2S coverage edges add ~K more in vpc only at
 *     the BIT-level when measured against I2S's dictionary).
 *   - A short descendant produced by BytesDeleteMutator on the long
 *     parent covers exactly ONE new edge (the early-fail return) and
 *     no CMP_MAP buckets and no I2S edges, because all the K upstream
 *     CMPs are gated on length >= threshold.
 *   - The short descendant therefore ranks LOW in the queue and is
 *     rarely re-selected for further mutation. The line of "shorter
 *     and shorter" descendants is starved — and the SHRINK_TRAP needs
 *     descendants that are simultaneously short AND content-preserving
 *     at offset 0, which is a narrow target requiring repeated mutation
 *     of the same descendant lineage.
 *   - vp has fewer feedback channels, so the long-seed monopoly is
 *     proportionally weaker. Short descendants in vp's queue retain a
 *     fairer share of mutation budget and reach SHRINK_TRAP more often.
 *   - As K grows, vpc's monoculture deepens and short-descendant
 *     starvation worsens. At K=0 the seeds are weighted by edge
 *     coverage only — minimal monoculture — and vp ~ vpc on SHRINK_TRAP.
 *
 * What this v3 changes from v2:
 *   - Provides a 256-byte SEED file (via Dockerfile), not a 12-byte one.
 *     This is the cardinal correction.
 *   - Gates SHRINK_TRAP on `data[0] == MARKER_BYTE && size <= 8`. Random
 *     short inputs from havoc only have 1/256 chance of preserving the
 *     marker; descendants of the seed that retain offset 0 reach it
 *     reliably.
 *   - All upstream literal CMPs fire only when `size >= 32`, ensuring
 *     short descendants emit no upstream feedback signals beyond the
 *     trap edge itself.
 *   - The seed is shaped so it traverses ALL upstream CMPs successfully
 *     (it earns all K feedback slots). This is the queue-monoculture
 *     center we need to test starvation against.
 *
 * Acceptance: vp median SHRINK_TRAP > vpc median SHRINK_TRAP at
 * SEED_FEEDBACK_RICHNESS=64; vp/vpc ratio is monotone non-decreasing in
 * SEED_FEEDBACK_RICHNESS; at SEED_FEEDBACK_RICHNESS=0 the ratio is
 * approximately 1.0 (parity, not a vpc-dominant outlier as in v2).
 *
 * Falsifier: if vpc still dominates SHRINK_TRAP at every scan value
 * (as in v2), the queue-monoculture mechanism is also wrong, and the
 * lcms cmsio0.c:776 finding does not generalize to a synthetic without
 * the specific shape of the cmsICCHeader / havoc-distribution divergence
 * on a real ICC seed. In that case append the verdict and stop —
 * refutation stands.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef SEED_FEEDBACK_RICHNESS
#define SEED_FEEDBACK_RICHNESS 16
#endif

#if SEED_FEEDBACK_RICHNESS != 0  && \
    SEED_FEEDBACK_RICHNESS != 4  && \
    SEED_FEEDBACK_RICHNESS != 16 && \
    SEED_FEEDBACK_RICHNESS != 64
#error "SEED_FEEDBACK_RICHNESS must be one of {0, 4, 16, 64}"
#endif

#define LONG_THRESHOLD   32u   /* upstream CMPs fire only on inputs >= this length */
#define SHRINK_LIMIT      8u   /* SHRINK_TRAP requires size <= this */
#define MARKER_BYTE     0xA5u  /* seed's offset 0; SHRINK_TRAP requires this */
#define FEEDBACK_OFFSET  32u   /* literal-CMP block starts here */

/*
 * 64 distinct 4-byte literals. Each one is a CMP_MAP edge + I2S entry +
 * coverage edge when traversed. The seed (256 bytes) must satisfy them.
 */
static const uint32_t FEEDBACK_LITERALS[64] = {
    0xDEADBEEFu, 0xCAFEBABEu, 0xFEEDFACEu, 0xBADDCAFEu,
    0x8BADF00Du, 0xABAD1DEAu, 0xC0DEBABEu, 0xDEADD00Du,
    0x1BADB002u, 0xB16B00B5u, 0xDEADBEAFu, 0xFACEFEEDu,
    0x0DEFACEDu, 0xC0FFEE00u, 0xBABE2BADu, 0xDEFACED1u,
    0x12345678u, 0x9ABCDEF0u, 0x55AA55AAu, 0xAA55AA55u,
    0x01020304u, 0x05060708u, 0x090A0B0Cu, 0x0D0E0F10u,
    0x11121314u, 0x15161718u, 0x191A1B1Cu, 0x1D1E1F20u,
    0x21222324u, 0x25262728u, 0x292A2B2Cu, 0x2D2E2F30u,
    0x31323334u, 0x35363738u, 0x393A3B3Cu, 0x3D3E3F40u,
    0x41424344u, 0x45464748u, 0x494A4B4Cu, 0x4D4E4F50u,
    0x51525354u, 0x55565758u, 0x595A5B5Cu, 0x5D5E5F60u,
    0x61626364u, 0x65666768u, 0x696A6B6Cu, 0x6D6E6F70u,
    0x71727374u, 0x75767778u, 0x797A7B7Cu, 0x7D7E7F80u,
    0x81828384u, 0x85868788u, 0x898A8B8Cu, 0x8D8E8F90u,
    0x91929394u, 0x95969798u, 0x999A9B9Cu, 0x9D9E9FA0u,
    0xA1A2A3A4u, 0xA5A6A7A8u, 0xA9AAABACu, 0xADAEAFB0u,
};

static volatile uint32_t g_sink;

__attribute__((noinline))
static uint32_t read_u32_be(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] <<  8) | ((uint32_t)p[3]      );
}

/*
 * Each feedback slot is a separate noinline function so the coverage
 * map gets a distinct edge per slot, the CMP_MAP gets a distinct
 * comparison site per slot, and the I2S logger sees K distinct
 * trace_const_cmp4 sites. Generated via X-macro fan-out.
 */
#define FEEDBACK_FN(N)                                                       \
    __attribute__((noinline))                                                \
    static int feedback_##N(const uint8_t *data, size_t size) {              \
        if (size < FEEDBACK_OFFSET + 4u * ((N) + 1u)) return 0;              \
        uint32_t v = read_u32_be(data + FEEDBACK_OFFSET + 4u * (N));         \
        uint32_t k = FEEDBACK_LITERALS[N];                                   \
        g_sink ^= v ^ k;                                                     \
        if (v == k) { g_sink += 1u; return 1; }                              \
        return 0;                                                            \
    }

#define APPLY_64(F) \
    F(0)  F(1)  F(2)  F(3)  F(4)  F(5)  F(6)  F(7)  \
    F(8)  F(9)  F(10) F(11) F(12) F(13) F(14) F(15) \
    F(16) F(17) F(18) F(19) F(20) F(21) F(22) F(23) \
    F(24) F(25) F(26) F(27) F(28) F(29) F(30) F(31) \
    F(32) F(33) F(34) F(35) F(36) F(37) F(38) F(39) \
    F(40) F(41) F(42) F(43) F(44) F(45) F(46) F(47) \
    F(48) F(49) F(50) F(51) F(52) F(53) F(54) F(55) \
    F(56) F(57) F(58) F(59) F(60) F(61) F(62) F(63)

APPLY_64(FEEDBACK_FN)

typedef int (*feedback_fn_t)(const uint8_t *, size_t);

#define FEEDBACK_PTR(N) feedback_##N,
static feedback_fn_t const FEEDBACK_FNS[64] = { APPLY_64(FEEDBACK_PTR) };
#undef FEEDBACK_PTR

__attribute__((noinline))
static int run_upstream_feedback(const uint8_t *data, size_t size) {
    /*
     * All upstream CMPs are gated on `size >= LONG_THRESHOLD`. A short
     * descendant skips this entire block, emitting no feedback signals
     * beyond the early-return edge.
     */
    if (size < LONG_THRESHOLD) return 0;
    int matched = 0;
    for (int i = 0; i < SEED_FEEDBACK_RICHNESS; i++) {
        matched += FEEDBACK_FNS[i](data, size);
    }
    return matched;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /*
     * Run the upstream feedback block. For the seed (size==256, offset
     * >=32 satisfies all 64 literals) this populates K coverage edges +
     * K CMP_MAP buckets + K I2S entries. For a short descendant the
     * gate skips the whole block.
     */
    int matched = run_upstream_feedback(data, size);
    g_sink ^= (uint32_t)matched;

    /*
     * SHRINK_TRAP — reachable only when the input is short AND retains
     * the seed's offset-0 marker. Descendants of the long seed produced
     * via BytesDeleteMutator (which preserves the leading byte by
     * default — it deletes from interior or end) reach this with
     * probability ~1 if shrunk far enough. Random short inputs from
     * havoc reach it with probability 1/256 per byte-randomization at
     * offset 0.
     */
    if (size <= SHRINK_LIMIT && size >= 1 && data[0] == MARKER_BYTE) {
        __builtin_trap();
    }
    return 0;
}
