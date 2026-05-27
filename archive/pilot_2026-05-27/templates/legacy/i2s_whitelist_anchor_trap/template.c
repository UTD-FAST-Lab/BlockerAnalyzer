/*
 * i2s_whitelist_anchor_trap — vp BEATS vpc on switch-default whitelist traps.
 *
 * Source pair (motivating real branches):
 *   lcms src/cmsio0.c:805  `if (!validDeviceClass(Icc->DeviceClass)) {`
 *   lcms src/cmsio0.c:758  `default: return FALSE;` inside validDeviceClass
 *   Branches: br67 (default arm), br71 (call site), sister sub-paths in
 *     same function. Replicated cross-edge: subject 8 (vpc vs vp ΔAUC=23.5M,
 *     p=0.0002, vp 10/10 vs vpc 0/10) AND subject 5 (cmplog vs naive
 *     ΔAUC=18.0M, prob_diff=1.0). n_edges=2 cross-replication.
 *
 * Bloaty cross-target sub-path: macho.cc:152 br452 CPU_TYPE switch
 *   (cmplog>naive I2S loses, prob_diff=0.8) — same shape, different pair.
 *
 * Why this is a NEW template, not an extension.
 *   i2s_structure_preservation_bias (REFUTED 3x) — same primary pair
 *     (vp,vpc) but mechanism class is "upstream literal CMPs pollute
 *     I2S dictionary, starving descendants of an UNRELATED downstream
 *     length trap." The whitelist switch where the case arms ARE the
 *     trap CMPs is a structurally different harness shape.
 *
 *   i2s_inequality_anchor_trap (PENDING) — same primary pair (vp,vpc),
 *     different geometry: band (X==K is anchor, X>K trap-reachable)
 *     vs point-set (cl in {L_i} is anchor, cl not in {L_i} trap-reachable).
 *     Multiple attractors competing instead of one boundary; dose-
 *     response axis is POOL SIZE rather than chain length.
 *
 *   i2s_magic_number_gate (VERIFIED) — different primary pair (cmplog,naive),
 *     direction inverse (I2S HELPS on equality). The whitelist trap
 *     inverts that: equality ARMS exist but the trap is the DEFAULT.
 *     I2S helps cover the case arms but its splice-back keeps the
 *     operand stuck on a case arm, blocking the default.
 *
 * Mechanism (I2S whitelist anchor trap).
 *   Each `case L_i:` arm in a switch on integer `cl` emits a 4-byte
 *   equality CMP via sancov trace_const_cmp4 — every execution logs
 *   each L_i as an I2S dictionary entry. The default arm is reached
 *   iff `cl != L_i` for ALL i. I2SRandReplace at the offset where cl
 *   is read finds the bytes approximating ANY L_i (Hamming distance
 *   small) and rewrites to that L_i exactly — flipping back to a case
 *   arm and AWAY from default. CMP_MAP retains near-miss seeds at
 *   minimum Hamming distance to the nearest L_i, so the corpus
 *   monocenters at multiple "valid signature attractors" surrounding
 *   the default arm.
 *
 *   value_profile has CMP_MAP gradient (Hamming bucketing per case)
 *   but NO I2SRandReplace. Its offspring drift to off-literal values
 *   freely; once `cl != L_i for all i`, no mutator drags it back. vp
 *   resolves the default arm reliably.
 *
 *   value_profile_cmplog has CMP_MAP gradient PLUS I2SRandReplace.
 *   Each beneficial off-literal mutation is undone by splice-back on
 *   the next selection. Combined with N attractors competing, the
 *   corpus is anchored to the case arms; vpc starves at default.
 *
 * Knob: WHITELIST_SIZE in {1, 2, 4, 7}.
 *   N case arms in a switch on a 4-byte big-endian operand at offset 0.
 *   Trap fires on the default arm (operand matches no L_i and is not
 *   zero). N=1 minimum. N=7 mirrors lcms's validDeviceClass exactly
 *   (7 cmsSig*Class literals).
 *
 *   Whitelist literals chosen to mirror real ICC class signatures:
 *     L_1='mntr' (cmsSigDisplayClass)   = 0x6D6E7472
 *     L_2='scnr' (cmsSigInputClass)     = 0x73636E72
 *     L_3='prtr' (cmsSigOutputClass)    = 0x70727472
 *     L_4='link' (cmsSigLinkClass)      = 0x6C696E6B
 *     L_5='abst' (cmsSigAbstractClass)  = 0x61627374
 *     L_6='spac' (cmsSigColorSpaceClass)= 0x73706163
 *     L_7='nmcl' (cmsSigNamedColorClass)= 0x6E6D636C
 *
 * Predicted dose-response (primary pair vp vs vpc):
 *   vp > vpc on TRAP-crash count at every WHITELIST_SIZE >= 1.
 *   vp/vpc ratio MONOTONE NON-DECREASING in WHITELIST_SIZE.
 *
 * Acceptance: vp median > vpc median at WHITELIST_SIZE >= 2 AND
 *   (vp/vpc ratio at N=7) >= 1.5 * (vp/vpc ratio at N=1) AND
 *   vpc median <= vp median across the entire scan.
 *
 * Falsifier:
 *   - vpc dominates at all N -> mechanism inverted; would join
 *     strpres v3's log-saturation refutation catalog.
 *   - Curves flat -> harness is too easy (default is found by
 *     random walk before splice-back can act); v2 retry needed.
 */

#include <stdint.h>
#include <stddef.h>
#include <string.h>

#ifndef WHITELIST_SIZE
#define WHITELIST_SIZE 1
#endif

/* Mirror real lcms validDeviceClass case-arm literals (ICC class
 * signatures). 4-byte big-endian ASCII; ordered to match the case-arm
 * order in cmsio0.c lines 749-755. */
#define L1_MNTR  0x6D6E7472u  /* 'mntr' cmsSigDisplayClass     */
#define L2_SCNR  0x73636E72u  /* 'scnr' cmsSigInputClass       */
#define L3_PRTR  0x70727472u  /* 'prtr' cmsSigOutputClass      */
#define L4_LINK  0x6C696E6Bu  /* 'link' cmsSigLinkClass        */
#define L5_ABST  0x61627374u  /* 'abst' cmsSigAbstractClass    */
#define L6_SPAC  0x73706163u  /* 'spac' cmsSigColorSpaceClass  */
#define L7_NMCL  0x6E6D636Cu  /* 'nmcl' cmsSigNamedColorClass  */

static inline uint32_t read_be32(const uint8_t *p) {
  return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
         ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

/* validDeviceClass-style switch with WHITELIST_SIZE active arms.
 * Returns 1 iff cl matches any active L_i (i.e. is a "valid class").
 * Returns 0 iff cl matches none (default arm = trap-reachable side).
 *
 * Each `case L_i:` is a separate sancov-instrumented equality CMP. */
__attribute__((noinline))
static int valid_class(uint32_t cl) {
  /* Mirror lcms's special-case zero-allowance at line 745. Keeps the
   * synthetic predicate identical in shape to the real one. */
  if (cl == 0u) return 1;
  switch (cl) {
#if WHITELIST_SIZE >= 1
    case L1_MNTR: return 1;
#endif
#if WHITELIST_SIZE >= 2
    case L2_SCNR: return 1;
#endif
#if WHITELIST_SIZE >= 3
    case L3_PRTR: return 1;
#endif
#if WHITELIST_SIZE >= 4
    case L4_LINK: return 1;
#endif
#if WHITELIST_SIZE >= 5
    case L5_ABST: return 1;
#endif
#if WHITELIST_SIZE >= 6
    case L6_SPAC: return 1;
#endif
#if WHITELIST_SIZE >= 7
    case L7_NMCL: return 1;
#endif
    default: return 0;
  }
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  /* Match real cmsio0.c shape: an upstream gate (Header.magic check at
   * line 781) admits only correctly-magicked inputs to the
   * validDeviceClass site. Fixed 4-byte ICC magic check at offset 4.
   * I2S splices this trivially so it doesn't dominate the dose-response,
   * but its presence keeps the synthetic faithful. */
  if (size < 8) return 0;
  uint32_t magic = read_be32(data + 4);
  if (magic != 0x61637370u) return 0;  /* 'acsp' = cmsMagicNumber */

  uint32_t cl = read_be32(data + 0);

  /* Trap reached iff cl is NOT in {0} ∪ {L_1,...,L_WHITELIST_SIZE}. */
  if (!valid_class(cl)) {
    __builtin_trap();
  }
  return 0;
}
