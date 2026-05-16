/*
 * i2s_inequality_anchor_trap v4 — REAL-CMP-MIMICKING SYNTHETIC.
 *
 * Real-target origin: lcms cmsio0.c:827 `if (TagCount > MAX_TABLE_TAG)`.
 * Backward-trace finding (2026-05-04): the on-disk vpc Side-A seed has
 * TagCount=10 in a 564B valid ICC profile; vpc 0/10 vs vp 10/10.
 *
 * v3 refutation diagnosis (2026-05-04 sweep): with ONLY the trap CMP
 * present, both fuzzers cross K trivially — random byte mutation walks
 * past K in microseconds because no other CMPs compete for I2S
 * substitution slots and CMP_MAP gradient is unobstructed. Identical
 * "3 crashes" at every gap × every fuzzer × every trial.
 *
 * v4 hypothesis: the lcms divergence requires an I2S DICTIONARY POPULATED
 * BY UPSTREAM CMPs that compete for splice-back budget AND CMP_MAP
 * gradient channels that distract vpc's queue-selection feedback. We
 * mirror the lcms _cmsReadHeader CMP catalog as faithfully as possible
 * in a synthetic harness:
 *
 *   - 'acsp' 4-byte magic check at offset 36 (1 wide-literal CMP).
 *   - 7-arm validDeviceClass switch at offset 12 (7 wide-literal CMPs).
 *   - version > 0x05000000 inequality at offset 8 (1 inequality CMP).
 *   - 80-entry tag-sig lookup loop reading offset 132 (80 wide-literal
 *     CMPs — mirrors _cmsSearchTag iterating the descriptor table).
 *   - THE TRAP at offset 128: TagCount > K (1 inequality CMP, K varies
 *     by SEED_GAP knob).
 *
 * Total wide-literal CMPs in the I2S dictionary: ~88. This recreates
 * the dictionary competition that v3's bare harness lacked.
 *
 * Knob: SEED_GAP = K - V (V=10 fixed via seed). N=80 tag-sigs FIXED.
 *   gap=1     K=11    floor case, both fuzzers crack with one random byte
 *   gap=10    K=20    short gradient path
 *   gap=90    K=100   the lcms-canonical case (MAX_TABLE_TAG)
 *   gap=1000  K=1010  long gradient ascent path
 *
 * Predicted dose-response (primary pair: A=value_profile, B=value_profile_cmplog):
 *   vp >= vpc at every gap; vp/vpc TIME-TO-FIRST-CRASH ratio peaks at
 *   gap=90 mirroring lcms br73. Mechanism: vpc's mutation budget is
 *   split across ~88 dictionary entries; only ~4/132 ≈ 3% of any single
 *   I2S substitution targets the trap-bytes range; meanwhile CMP_MAP
 *   gradient channels are split across the 88 upstream CMPs (each
 *   contributes Hamming-distance buckets that compete for queue weight
 *   with the trap CMP's gradient). vp lacks I2S; vp's CMP_MAP gradient
 *   on TagCount IS the only channel that matters for resolving the
 *   trap, so vp's progress is unobstructed.
 *
 * Headline metric: TIME-TO-FIRST-CRASH per trial.
 *
 * Acceptance: vp median TTFC < vpc median TTFC at gap=90 by at least 2×;
 *   vpc trial-failure-rate (no crash within budget) > 0 at gap=90.
 *
 * Falsifier: if vpc TTFC matches or beats vp at every gap, the
 *   mechanism family is bounded by libafl's scheduler/throughput
 *   dynamics regardless of dictionary size — joining strpres in the
 *   "real-target divergences that don't reproduce in trivial synthetics"
 *   catalog. This would be the 4th refutation in the family
 *   (strpres v1/v2/v3 + this v4) and would close the methodology-limit
 *   case for inequality-anchor mechanisms specifically.
 */

#include <stdint.h>
#include <stddef.h>

#ifndef SEED_GAP
#define SEED_GAP 90
#endif

#define TRAP_K ((uint32_t)(10u + (uint32_t)SEED_GAP))

/* ICC magic 'acsp' big-endian. */
#define MAGIC_ACSP   0x61637370u

/* 7 valid device classes (cmsio0.c:743 validDeviceClass). */
#define CLS_INPUT    0x73636E72u  /* 'scnr' */
#define CLS_DISPLAY  0x6D6E7472u  /* 'mntr' */
#define CLS_OUTPUT   0x70727472u  /* 'prtr' */
#define CLS_LINK     0x6C696E6Bu  /* 'link' */
#define CLS_ABSTRACT 0x61627374u  /* 'abst' */
#define CLS_SPACE    0x73706163u  /* 'spac' */
#define CLS_NAMED    0x6E6D636Cu  /* 'nmcl' */

/* 80 ICC tag signatures (cmstypes.c:5798 _cmsTagDescriptorTable). Each
 * entry compares the input's first tag-sig (at offset 132) against the
 * literal — mirrors _cmsSearchTag's iteration loop. Names are real ICC
 * tag-sig FOURCCs. */
static const uint32_t TAG_SIGS[80] = {
    0x41324230, 0x41324231, 0x41324232, 0x41324233, /* A2B0..A2B3 */
    0x42324130, 0x42324131, 0x42324132, 0x42324133, /* B2A0..B2A3 */
    0x44324230, 0x44324231, 0x44324232, 0x44324233, /* D2B0..D2B3 */
    0x42324430, 0x42324431, 0x42324432, 0x42324433, /* B2D0..B2D3 */
    0x6263726F, 0x77633030, 0x77633031, 0x77633032, /* bcro,wc00..wc02 */
    0x67616D74, 0x636C726F, 0x6379677A, 0x63727469, /* gamt,clro,cygz,crti */
    0x63327370, 0x6368616D, 0x63686164, 0x63686172, /* c2sp,cham,chad,char */
    0x636C7274, 0x636D7330, 0x636D7331, 0x636D7332, /* clrt,cms0..cms2 */
    0x63696973, 0x636C6F74, 0x636C726E, 0x636C726F, /* ciis,clot,clrn,clro */
    0x6473637A, 0x646D6464, 0x646D6E64, 0x646D6573, /* dscz,dmdd,dmnd,dmes */
    0x65696E66, 0x65786669, 0x65786C30, 0x65786C31, /* einf,exfi,exl0,exl1 */
    0x66756E63, 0x66756E69, 0x67616D6D, 0x67616D74, /* func,funi,gamm,gamt */
    0x6776646F, 0x687069, 0x6963696D, 0x69647076,   /* gvdo,hpi.,icim,idpv */
    0x6B547267, 0x6c756d69, 0x6D656173, 0x6D6F6432, /* kTrg,lumi,meas,mod2 */
    0x6E636C32, 0x6E636F6C, 0x6F757470, 0x70617261, /* ncl2,ncol,outp,para */
    0x70733273, 0x70733230, 0x70733031, 0x70733032, /* ps2s,ps20..ps02 */
    0x72584D5A, 0x72545243, 0x72697420, 0x72706273, /* rXMZ,rTRC,rit ,rpbs */
    0x73637264, 0x73637263, 0x73637269, 0x73726967, /* scrd,scrc,scri,srig */
    0x74617267, 0x74656368, 0x76636774, 0x76696577, /* targ,tech,vcgt,view */
    0x77747074, 0x6B545243, 0x67545243, 0x62545243  /* wtpt,kTRC,gTRC,bTRC */
};

static inline uint32_t read_be32(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

__attribute__((noinline))
static int validDeviceClass(uint32_t cls) {
    if (cls == 0) return 1; /* lcms allows zero */
    switch (cls) {
        case CLS_INPUT: case CLS_DISPLAY: case CLS_OUTPUT:
        case CLS_LINK: case CLS_ABSTRACT: case CLS_SPACE:
        case CLS_NAMED: return 1;
        default: return 0;
    }
}

__attribute__((noinline))
static int searchTag(uint32_t sig) {
    int found = -1;
    for (int i = 0; i < 80; i++) {
        if (sig == TAG_SIGS[i]) found = i;
    }
    return found;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    /* Mirror lcms _cmsReadHeader: require >= 132 bytes (128B header + 4B TagCount). */
    if (size < 136) return 0;

    /* Upstream gate 1: magic at offset 36 (1 wide-literal CMP). */
    if (read_be32(data + 36) != MAGIC_ACSP) return 0;

    /* Upstream gate 2: version <= 0x05000000 at offset 8 (1 inequality CMP). */
    if (read_be32(data + 8) > 0x05000000u) return 0;

    /* Upstream gate 3: validDeviceClass at offset 12 (7-arm switch). */
    if (!validDeviceClass(read_be32(data + 12))) return 0;

    /* Upstream gate 4: tag-sig lookup at offset 132 (80 wide-literal CMPs). */
    if (searchTag(read_be32(data + 132)) < 0) return 0;

    /* THE TRAP: TagCount > K at offset 128. cmplog logs (V=10, K) into
     * the I2S dictionary on every execution that reaches this CMP. */
    uint32_t tag_count = read_be32(data + 128);
    if (tag_count > TRAP_K) {
        __builtin_trap();
    }
    return 0;
}
