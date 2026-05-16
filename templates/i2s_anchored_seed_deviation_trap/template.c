/**
 * i2s_structure_preservation_bias: parameterized harness for the
 * (value_profile_cmplog, value_profile) source pair where I2S HURTS.
 *
 * Source: lcms cmsio0.c:776 `_cmsReadHeader` — the early-fail T branch
 *   `if (io->Read(io, &Header, sizeof(cmsICCHeader), 1) != 1) return FALSE`.
 * The blocked side is reached only when the input is shorter than
 * sizeof(cmsICCHeader) = 128 bytes (incomplete read). Empirically, vp
 * resolves it 3/3 trials (winning seed = 57 bytes); vpc resolves 0/3
 * (all attempts >= 564 bytes). Adding I2S to vp HURTS at this branch.
 *
 * Hypothesis. I2S logs every literal-operand integer comparison via
 * sancov trace_const_cmp; I2SRandReplace splices logged constants back
 * into mutated inputs at byte positions where the constant matches.
 * If the upstream code path runs many literal-equality CMPs (e.g.
 * profile-magic, class, PCS, signature, vendor in the ICC header
 * validator), the I2S dictionary gets populated with those constants
 * and the I2S mutator preferentially produces inputs that PRESERVE
 * those constants in their original positions. To preserve constants,
 * the input must remain long enough to host them — biasing the corpus
 * AWAY from length-shrinking mutations. value_profile alone has no
 * such splice-back mutator (its CMP_MAP is feedback-only, not a
 * mutation source); BytesDeleteMutator can shrink freely. So a
 * length-fail branch (an early return triggered when input < N bytes)
 * is reachable for vp but invisible to vpc.
 *
 * Compile-time parameter:
 *   STRUCTURE_PAYLOAD_BYTES in {0, 4, 16, 64}
 *     = number of distinct 4-byte literal-equality CMPs the harness
 *       runs on a "structure" portion of the input (offsets >= 32).
 *       Each CMP populates one I2S dictionary entry. Higher values
 *       mean more splice-back targets pinning byte content far from
 *       offset 0, biasing I2S-equipped fuzzers toward inputs of
 *       length >= 32 + 4*STRUCTURE_PAYLOAD_BYTES.
 *
 * Two reachable trap branches, both via __builtin_trap():
 *   1. STRUCTURE_TRAP — input is long enough that the structure block
 *      passes; trips at offset 0 magic + first 4 bytes of structure
 *      block matching. I2S resolves this trivially; vp via gradient.
 *   2. SHRINK_TRAP   — input is shorter than SHRINK_THRESHOLD bytes
 *      (default 16). Symmetric for both fuzzers in principle, but
 *      I2S's corpus bias toward long inputs starves shrink mutations.
 *
 * Predicted dose-response on the SHRINK_TRAP crash count:
 *   - naive: stochastic; mostly hits via random short inputs;
 *     flat-ish across STRUCTURE_PAYLOAD_BYTES.
 *   - vp:    similar to naive on SHRINK_TRAP; no splice-back mutator,
 *     no length bias; hits the shrink trap consistently.
 *   - cmp:   I2S-locked into preserving structure magic; SHRINK_TRAP
 *     count decays as STRUCTURE_PAYLOAD_BYTES grows (more splice-back
 *     entries -> stronger bias against shrink mutations).
 *   - vpc:   same as cmp on SHRINK_TRAP — the I2S layer in vpc
 *     dominates length bias; CMP_MAP gradient does not pull toward
 *     short inputs.
 *
 * Acceptance: vp crashes the SHRINK_TRAP at every STRUCTURE_PAYLOAD_BYTES
 * value; vpc's SHRINK_TRAP count drops monotonically and is 0 (or
 * statistically << vp) at STRUCTURE_PAYLOAD_BYTES=64. vpc's STRUCTURE_TRAP
 * count is high (I2S helps); the trade-off (vpc gains structure but
 * loses shrink) is the I2S-hurts limitation we are demonstrating.
 *
 * The headline metric for the primary-pair finding (vpc LOSES to vp)
 * is the SHRINK_TRAP crash count, NOT total crashes. The harness emits
 * different __builtin_trap call sites so AFL++ counts them separately
 * via crash deduplication on PC.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef STRUCTURE_PAYLOAD_BYTES
#define STRUCTURE_PAYLOAD_BYTES 16
#endif

#if STRUCTURE_PAYLOAD_BYTES != 0  && \
    STRUCTURE_PAYLOAD_BYTES != 4  && \
    STRUCTURE_PAYLOAD_BYTES != 16 && \
    STRUCTURE_PAYLOAD_BYTES != 64
#error "STRUCTURE_PAYLOAD_BYTES must be one of {0, 4, 16, 64}"
#endif

#define SHRINK_THRESHOLD 16
#define STRUCTURE_OFFSET 32
#define MAGIC_OFFSET     0

static const uint32_t GATEWAY_MAGIC = 0x6D6E7472u; /* 'mntr' big-endian */

static const uint32_t STRUCTURE_MAGICS[64] = {
    0x52474220u, 0x58595A20u, 0x61637370u, 0x4150504Cu,
    0x4C434D53u, 0x70726F66u, 0x69636330u, 0x64657363u,
    0x77747074u, 0x626B7074u, 0x72545243u, 0x67545243u,
    0x62545243u, 0x6368726Du, 0x636C726Fu, 0x76636774u,
    0x76696577u, 0x6C756D69u, 0x6D656173u, 0x74656368u,
    0x70736571u, 0x70733273u, 0x70733067u, 0x70733167u,
    0x6D6D6F64u, 0x70736964u, 0x6373706Eu, 0x6263736Eu,
    0x73637072u, 0x73637363u, 0x73637773u, 0x6E63706Cu,
    0x6E636C72u, 0x6E63646Eu, 0x6E636C75u, 0x6E63616Bu,
    0x6E63726Bu, 0x646D6E64u, 0x646D6464u, 0x6D6E6473u,
    0x6D646473u, 0x6C756D6Au, 0x6D656174u, 0x74656369u,
    0x70736572u, 0x73663332u, 0x73663634u, 0x75693332u,
    0x6E693332u, 0x6F6E6431u, 0x6F756476u, 0x70747263u,
    0x4D533030u, 0x4D533031u, 0x4D533032u, 0x4D533033u,
    0x4D533034u, 0x4D533035u, 0x4D533036u, 0x4D533037u,
    0x4D533038u, 0x4D533039u, 0x4D53303Au, 0x4D53303Bu,
};

static volatile uint32_t g_sink;

__attribute__((noinline))
static uint32_t read_u32_be(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] <<  8) | ((uint32_t)p[3]      );
}

__attribute__((noinline))
static int check_structure_slot(const uint8_t *data, int slot) {
    uint32_t v = read_u32_be(data + STRUCTURE_OFFSET + 4 * slot);
    uint32_t k = STRUCTURE_MAGICS[slot];
    g_sink ^= v ^ k;
    return v == k;
}

__attribute__((noinline))
static int check_all_structure(const uint8_t *data, size_t size) {
    int matched = 0;
    for (int i = 0; i < STRUCTURE_PAYLOAD_BYTES; i++) {
        if ((size_t)(STRUCTURE_OFFSET + 4 * (i + 1)) > size) break;
        if (check_structure_slot(data, i)) matched++;
    }
    return matched;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < SHRINK_THRESHOLD) {
        if (size >= 1 && data[0] == 0xA5u) {
            __builtin_trap();
        }
        return 0;
    }

    if (size < 4) return 0;
    uint32_t hdr = read_u32_be(data + MAGIC_OFFSET);
    if (hdr != GATEWAY_MAGIC) return 0;

    int n_matched = check_all_structure(data, size);
#if STRUCTURE_PAYLOAD_BYTES == 0
    (void)n_matched;
    if (size >= 8 && data[4] == 0x5Au) {
        __builtin_trap();
    }
#else
    if (n_matched >= 1) {
        __builtin_trap();
    }
#endif
    return 0;
}
