==== BLOCKER ====
Target: harfbuzz
Branch ID: 5990
Location: /src/harfbuzz/src/hb-ot-shaper-use.cc:357:44
Enclosing function: hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&)
Source line:   return (info.use_category() == USE(H) || info.use_category() == USE(HVM) || info.use_category() == USE(IS)) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ctx_coverage vs naive_ctx)
cmplog                           0       10          0  REFERENCE
value_profile                    4        6          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     5        5          0  REFERENCE
mopt                             7        3          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 15  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=3.90h  loser=21.00h
  avg hitcount on branch: winner=76  loser=0
  prob_div=0.80  dur_div=17.10h  hit_div=76
  subject-level: delta_AUC=15634800.0  p_AUC=0.0003  delta_Final=258.3  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5990/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&) (/src/harfbuzz/src/hb-ot-shaper-use.cc:356-359) ---
[ ]   354  static inline bool
[ ]   355  is_halant_use (const hb_glyph_info_t &info)
[B]   356  {
[B]   357    return (info.use_category() == USE(H) || info.use_category() == USE(HVM) || info.use_category() == USE(IS)) && <-- BLOCKER
[B]   358  	 !_hb_glyph_info_ligated (&info);
[B]   359  }

--- Caller (1 hop): hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442, calls hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&) at line 425) (±10 around call site) ---
[ ]   415  	break;
[ ]   416        }
[ ]   417      }
[ ]   418    }
[ ]   419  
[ ]   420    /* Move things back. */
[B]   421    unsigned int j = start;
[B]   422    for (unsigned int i = start; i < end; i++)
[B]   423    {
[B]   424      uint32_t flag = FLAG_UNSAFE (info[i].use_category());
[B]   425      if (is_halant_use (info[i])) <-- CALL
[W]   426      {
[ ]   427        /* If we hit a halant, move after it; otherwise move to the beginning, and
[ ]   428         * shift things in between forward. */
[W]   429        j = i + 1;
[W]   430      }
[B]   431      else if (((flag) & (FLAG (USE(VPre)) | FLAG (USE(VMPre)))) &&
[ ]   432  	     /* Only move the first component of a MultipleSubst. */
[B]   433  	     0 == _hb_glyph_info_get_lig_comp (&info[i]) &&
[B]   434  	     j < i)
[W]   435      {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442, calls hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&) at line 401)
hop 3  hb-ot-shaper-use.cc:reorder_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:448-467, calls hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) at line 459)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442) ---
  d=2   L 425  T=33 F=116  T=0 F=146  if (is_halant_use (info[i]))
  d=2   L 431  T=2 F=114  T=0 F=146  else if (((flag) & (FLAG (USE(VPre)) | FLAG (USE(VMPre)))...
  d=2   L 433  T=2 F=0  T=0 F=0  0 == _hb_glyph_info_get_lig_comp (&info[i]) &&
  d=2   L 434  T=2 F=0  T=0 F=0  j < i)
--- d=1  hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:356-359) ---
  d=1   L 357  T=33 F=116  T=0 F=146  return (info.use_category() == USE(H) || info.use_categor...  <-- BLOCKER
  d=1   L 358  T=33 F=0  T=0 F=0  !_hb_glyph_info_ligated (&info);

[off-chain: 7 additional divergent branches across 4 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=26bf7268066ac7f7, size=61 bytes, fuzzer=naive_ctx, trial=1, discovered_at=1677s, mutation_op=ByteNegMutator,WordInterestingMutator,BytesExpandMutator):
  0000: 00 00 00 00 ca 0d 00 00 0c 00 00 00 00 0c 00 00   ................
  0010: 20 00 00 0d 20 00 c5 03 e8 00 01 00 00 6d 74 00    ... ........mt.
  0020: 09 00 00 00 00 00 00 00 00 00 00 00 aa aa 00 00   ................
  0030: 00 00 fe 00 00 00 00 00 00 c2 05 00 00            .............
Seed 2 (id=6a3b62babcd0dcce, size=70 bytes, fuzzer=naive_ctx, trial=1, discovered_at=2939s, mutation_op=BytesCopyMutator,BytesExpandMutator,CrossoverReplaceMutator):
  0000: 00 3d 00 00 00 00 10 00 00 00 00 00 00 00 00 00   .=..............
  0010: 00 00 ca 0d 00 00 0c 00 00 00 00 00 00 00 cd 08   ................
  0020: 00 00 ac 08 00 5c 60 1a 00 00 c2 00 00 00 00 00   .....\`.........
  0030: 00 00 00 00 00 00 00 00 00 00 00 fe 00 00 00 00   ................
Seed 3 (id=863b0d8b8f0e8853, size=53 bytes, fuzzer=naive_ctx, trial=1, discovered_at=6162s, mutation_op=CrossoverReplaceMutator,ByteIncMutator,WordAddMutator):
  0000: 6d 74 00 0a 00 00 0e 00 ca 0d 00 00 0c 10 10 00   mt..............
  0010: 00 09 00 00 cf 00 00 0d 00 00 00 08 00 00 10 00   ................
  0020: ff 00 20 00 c5 fe 0d 00 01 00 00 6d 74 00 00 0d   .. ........mt...
  0030: 01 00 00 00 00                                    .....
Seed 4 (id=72f07dc8fa7f32ec, size=95 bytes, fuzzer=naive_ctx, trial=1, discovered_at=6721s, mutation_op=BytesDeleteMutator,CrossoverInsertMutator,BytesInsertCopyMutator):
  0000: 00 3d e9 01 00 3d 06 00 00 3d e9 01 00 3d e9 01   .=...=...=...=..
  0010: 00 c6 20 00 00 1a 00 20 00 00 00 3d e9 01 00 c6   .. .... ...=....
  0020: 20 00 00 1a 00 20 00 00 0d 0d 20 00 00 ff ff ca    .... .... .....
  0030: 0d 00 00 c5 fe 1f 80 ff 00 20 20 20 20 20 20 20   .........       
Seed 5 (id=35497439afb9feef, size=70 bytes, fuzzer=naive_ctx, trial=1, discovered_at=11053s, mutation_op=ByteRandMutator):
  0000: 00 3d 00 06 06 06 6d 8b 00 f7 00 00 00 00 ca 0d   .=....m.........
  0010: 00 00 00 0d 00 00 ca 0d 7f 00 00 0d 00 00 ca 0d   ................
  0020: ff 06 0c 1c 00 00 20 20 20 20 20 20 01 00 00 c5   ......      ....
  0030: 00 09 00 00 00 00 ca 0d 00 00 f3 ff 00 00 ca 0d   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=011ee946350f9d8a, size=10 bytes, fuzzer=naive, trial=2, discovered_at=5s, mutation_op=ByteDecMutator,CrossoverInsertMutator,ByteAddMutator,BytesDeleteMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 20 20 b7 b7 b7 b7 b7 b7 18 18                       ........
Seed 2 (id=0085ead6b839c9ab, size=14 bytes, fuzzer=naive, trial=2, discovered_at=151s, mutation_op=BytesInsertCopyMutator):
  0000: 4b e9 01 00 ed e9 01 00 ed ed 01 00 ed 12         K.............
Seed 3 (id=012388c9fda877df, size=184 bytes, fuzzer=naive, trial=2, discovered_at=462s, mutation_op=BytesSwapMutator,ByteIncMutator,BytesDeleteMutator,DwordAddMutator,ByteDecMutator,BytesInsertMutator,ByteAddMutator):
  0000: 00 68 61 6e 74 2d 6d 61 21 21 21 21 21 21 21 6e   .hant-ma!!!!!!!n
  0010: 2d a8 00 00 00 e0 e0 e0 e0 be 11 01 20 20 2b 20   -...........  + 
  0020: 21 00 5a 20 1c 2e 00 e2 1a 1a 1a 1a 2e 12 01 00   !.Z ............
  0030: 26 36 36 36 05 00 df df df df df df df df df df   &666............
Seed 4 (id=0071175129a537b1, size=22 bytes, fuzzer=naive, trial=2, discovered_at=3689s, mutation_op=BytesExpandMutator):
  0000: 00 e9 01 00 00 01 00 00 01 0a 01 00 1c 23 00 00   .............#..
  0010: 01 0a 01 00 1c 23                                 .....#
Seed 5 (id=00b82255fa465af1, size=84 bytes, fuzzer=naive, trial=2, discovered_at=4937s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,BytesDeleteMutator,ByteNegMutator):
  0000: 72 31 32 32 75 75 00 01 00 00 74 2d 6d 6f 00 32   r122uu....t-mo.2
  0010: 18 ff 0d 18 00 00 72 ff 72 31 32 32 32 18 67 9b   ......r.r1222.g.
  0020: 03 0b 18 00 00 7a 6f 2d 68 61 6e 74 2d 6d 6f 00   .....zo-hant-mo.
  0030: 00 0d f7 f2 0a 18 00 00 e3 7f ff ff ff 8e f1 ff   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x6 6d(m)x3 68(h)x1             00(.)x2 2c(,)x2 0c(.)x2 20( )x1 +3u  PARTIAL
   0x0002  00(.)x6 e9(.)x2 6f(o)x2             01(.)x2 00(.)x2 b7(.)x1 61(a)x1 +4u  PARTIAL
   0x000a  00(.)x6 e9(.)x2 06(.)x1 76(v)x1     01(.)x2 00(.)x2 21(!)x1 74(t)x1 +3u  PARTIAL
   0x000c  00(.)x8 0c(.)x1 06(.)x1             ed(.)x1 21(!)x1 1c(.)x1 6d(m)x1 +5u  PARTIAL
   0x000e  00(.)x2 e9(.)x2 0e(.)x2 10(.)x1 +3u  00(.)x5 21(!)x1 18(.)x1 cd(.)x1     PARTIAL
   0x000f  00(.)x5 01(.)x2 0d(.)x1 20( )x1 +1u  00(.)x5 6e(n)x1 32(2)x1 cd(.)x1     PARTIAL
   0x0010  00(.)x6 ca(.)x2 20( )x1 8b(.)x1     0d(.)x2 00(.)x2 2d(-)x1 01(.)x1 +2u  PARTIAL
   0x0013  00(.)x7 0d(.)x3                     00(.)x6 18(.)x1 ff(.)x1             PARTIAL
   0x0014  00(.)x8 20( )x1 cf(.)x1             00(.)x4 1c(.)x1 0d(.)x1 a7(.)x1 +1u  PARTIAL
   0x0015  00(.)x7 1a(.)x2 e1(.)x1             00(.)x2 e0(.)x1 23(#)x1 17(.)x1 +3u  PARTIAL
   0x0019  00(.)x8 0d(.)x2                     20( )x2 be(.)x1 31(1)x1 00(.)x1 +2u  PARTIAL
   0x001a  00(.)x9 01(.)x1                     00(.)x3 11(.)x1 32(2)x1 67(g)x1 +1u  PARTIAL
   0x001b  00(.)x4 3d(=)x2 0d(.)x2 08(.)x1 +1u  00(.)x4 01(.)x1 32(2)x1 0b(.)x1     PARTIAL
   0x001c  00(.)x5 e9(.)x2 ca(.)x2 ff(.)x1     00(.)x3 20( )x1 32(2)x1 0c(.)x1 +1u  PARTIAL
   0x001d  00(.)x5 01(.)x2 0d(.)x2 6d(m)x1     00(.)x3 18(.)x2 20( )x1 0c(.)x1     PARTIAL
   0x001f  00(.)x4 c6(.)x2 08(.)x1 0d(.)x1 +2u  00(.)x4 20( )x1 9b(.)x1 93(.)x1     PARTIAL
   0x0023  00(.)x5 1a(.)x2 08(.)x1 1c(.)x1 +1u  00(.)x4 20( )x1 32(2)x1 ca(.)x1     PARTIAL
   0x0024  00(.)x6 0e(.)x2 c5(.)x1 0d(.)x1     00(.)x3 1c(.)x1 0c(.)x1 cd(.)x1 +1u  PARTIAL
   0x0025  00(.)x6 20( )x2 5c(\)x1 fe(.)x1     00(.)x2 2e(.)x1 7a(z)x1 18(.)x1 +2u  PARTIAL
   0x0027  00(.)x4 20( )x2 0d(.)x2 1a(.)x1 +1u  00(.)x4 e2(.)x1 2d(-)x1 18(.)x1     PARTIAL
   0x0028  00(.)x4 0d(.)x3 20( )x2 01(.)x1     00(.)x3 1a(.)x1 68(h)x1 aa(.)x1 +1u  PARTIAL
   0x0029  00(.)x5 0d(.)x2 20( )x2 ff(.)x1     1a(.)x1 61(a)x1 aa(.)x1 00(.)x1 +3u  PARTIAL
   0x002b  00(.)x6 20( )x2 6d(m)x1 0c(.)x1     00(.)x2 1a(.)x1 74(t)x1 0c(.)x1 +2u  PARTIAL
   0x002e  00(.)x7 ff(.)x2 e4(.)x1             00(.)x3 01(.)x1 6f(o)x1 67(g)x1 +1u  PARTIAL
   0x0030  00(.)x7 0d(.)x2 01(.)x1             0d(.)x2 26(&)x1 00(.)x1 69(i)x1 +2u  PARTIAL
   0x0031  00(.)x7 09(.)x2 20( )x1             00(.)x2 36(6)x1 0d(.)x1 18(.)x1 +2u  PARTIAL
   0x0032  00(.)x6 0e(.)x2 fe(.)x1 20( )x1     00(.)x3 36(6)x1 f7(.)x1 14(.)x1 +1u  PARTIAL
   0x0033  00(.)x7 c5(.)x2 20( )x1             00(.)x4 36(6)x1 f2(.)x1 01(.)x1     PARTIAL
   0x0034  00(.)x7 fe(.)x2 20( )x1             00(.)x3 0d(.)x2 05(.)x1 0a(.)x1     PARTIAL
   0x0035  00(.)x6 1f(.)x2 01(.)x1             00(.)x2 18(.)x1 17(.)x1 02(.)x1 +2u  PARTIAL
   0x0037  00(.)x5 ff(.)x2 0d(.)x2             00(.)x3 df(.)x1 01(.)x1 03(.)x1     PARTIAL
   0x0038  00(.)x6 ca(.)x2 c5(.)x1             00(.)x3 df(.)x1 e3(.)x1 0c(.)x1     PARTIAL
   0x0039  00(.)x4 20( )x2 0d(.)x2 c2(.)x1     0c(.)x2 df(.)x1 7f(.)x1 01(.)x1 +1u  PARTIAL
   0x003b  00(.)x4 20( )x2 fe(.)x1 ff(.)x1 +1u  00(.)x3 df(.)x1 ff(.)x1             PARTIAL
   0x003c  00(.)x5 20( )x2 ca(.)x1 35(5)x1     00(.)x3 df(.)x1 ff(.)x1             PARTIAL
   0x003d  00(.)x4 20( )x2 0d(.)x1 6b(k)x1     df(.)x1 8e(.)x1 66(f)x1 00(.)x1 +1u  PARTIAL
   0x003e  00(.)x4 20( )x2 ca(.)x1 65(e)x1     df(.)x1 f1(.)x1 68(h)x1 fe(.)x1 +1u  DIFFER
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- naive ---
**Instrumentation**: SanitizerCoverage edge counters
(`__sanitizer_cov_trace_pc_guard*` callbacks compiled in via clang
`-fsanitize-coverage=...`).

**Feedback**: per-edge hit-count bucket; a new bucket triggers a
corpus-add (LibAFL `MaxMapFeedback` over the edge map).

**Mutators**: havoc + token stack — `ByteFlipMutator`, `ByteRandMutator`,
`ByteIncMutator`, `ByteDecMutator`, `ByteAddMutator`, `WordAddMutator`,
`DwordAddMutator`, `QwordAddMutator`, `BytesDeleteMutator`,
`BytesInsertMutator`, `BytesInsertCopyMutator`, `BytesExpandMutator`,
`BytesRandInsertMutator`, `BytesRandSetMutator`, `BytesCopyMutator`,
`BytesSwapMutator`, `WordInterestingMutator`, `DwordInterestingMutator`,
`ByteInterestingMutator`, `CrossoverInsertMutator`,
`CrossoverReplaceMutator`, `TokenInsert`, `TokenReplace`.

**Observed `mutation_op` in seed metadata**: any of the above. No I2S.

**Per-execution cost**: one edge-counter increment per executed BB edge.

--- naive_ctx ---
**Instrumentation**: naive's SanitizerCoverage edge counters, but the
executor installs a `CtxHook` (`HookableInProcessExecutor`). The hook
keeps a running hash of the current call context (caller chain) and
folds it into the edge-map index, so the same basic-block edge is
recorded at different map slots depending on the call path that
reached it.

**Feedback**: the same `MaxMapFeedback` edge-bucket signal as naive,
computed over the context-indexed map — a "new bucket" is a new
(call-context, edge) pair rather than a bare edge.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`, no
CMP_MAP. Stages are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no ParentInfo-only / dash rows.

**Per-execution cost**: one edge-counter increment per executed edge
plus a context-hash update per call/return.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5990.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5990,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage)]
  "hypotheses": [
    {
      "covers_pairs": ["cmplog>naive (I2S)"],
        // labels MUST match exactly as in DECISIVE PAIRS (e.g. "cmplog>naive (I2S)")
      "what_input_feature": "concrete description of the bytes/structure required",
      "why_winner_satisfies": "what about the winner inputs meets the requirement",
      "why_loser_doesnt": "what is missing in the loser inputs",
      "mechanism_attribution": "free text — explain which fuzzer technique enables the winner; must agree with claimed_mechanism below"
    }
    // pair_decision="single_feature" => exactly 1 hypothesis whose covers_pairs lists ALL decisive pairs
    // pair_decision="multi_feature"  => 2+ hypotheses, each covers_pairs listing its subset
  ],
  "evidence_trail": [
    {
      "claim": "atomic factual claim (1 sentence)",
      "cited_section": "BLOCKER",
        // pick the canonical short name of the cited section, one of:
        //   BLOCKER | TRIAL VECTOR | DECISIVE PAIRS | SOURCE CONTEXT |
        //   HIT-COUNT DIVERGENCE | DIVERGENT BRANCHES | BRANCH SEEDS |
        //   BYTE DIFF | MECHANISM CONTEXT
        // validator accepts the full section header too (e.g. "BYTE DIFF (W vs L at common offsets)")
      "cited_locator": "offsets 0x06-0x0f | L1701 | seed_id ab12... | etc.",
      "exact_quote": "verbatim substring of the prompt — COPY-PASTE, do not paraphrase"
    }
    // at least ONE entry per hypothesis sub-field (what / why_winner / why_loser / mechanism)
  ],
  "mechanism_consistency_check": {
    "claimed_mechanism": "I2SRandReplace",
      // pick EXACTLY ONE — the technique that enables the WINNER:
      //   comparison-solving (roadblock dimension):
      //     "I2SRandReplace"     (cmplog / vpc input-to-state substitution)
      //     "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)
      //   coverage-granularity (feedback dimension):
      //     "context-sensitive coverage" (naive_ctx CtxHook: (call-context, edge) pairs are new coverage)
      //     "ngram coverage"            (naive_ngram4: N-gram edge tuples are new coverage)
      //   mutation/scheduling (mutation dimension):
      //     "grimoire structural"  (grimoire GeneralizationStage + structural/grammar recombination)
      //     "mopt mutation"        (mopt: MOpt-scheduled mutation-operator probabilities)
      //     "calibrated energy"    (minimizer/fast: corpus-minimization / calibrated power schedule)
      //     "aflfast rarity"       (fast: AFLFast rare-edge power schedule)
      //   baseline / fallback:
      //     "havoc-only"         (lucky havoc byte mutation, no CMP introspection)
      //     "token-replace"      (TokenInsert/TokenReplace dictionary mutations)
      //     "other"              (genuinely cannot classify — NOT a substitute for a known technique above)
    "verified_in_lineage": true,
      // pick true or false
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5990 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
    // TODO(i2s-logging-bug): the LibAFL cmplog harness does NOT log
    //   the literal "I2SRandReplace" string into seed metadata. Until
    //   that is fixed, the verification signal is the dash-row floor
    //   (ParentInfo-only entries; SQL NULL mutation_op). Confirmed
    //   2026-05-17: dash rows are exclusive to cmplog/vpc in the
    //   current data (zero occurrences in 6000 naive/vp samples).
    //   When the logging fix lands, revert this rule to require the
    //   literal "I2SRandReplace" name and treat the dash signal as
    //   secondary corroboration.
    // MANDATORY when claimed_mechanism="I2SRandReplace": invoke db_query.py lineage on >=1 winning seed
    //   - if you find at least one I2S-floor row in the ancestor chain (mutation_op = -
    //     for ancestors of a cmplog/vpc-discovered seed): verified_in_lineage=true,
    //     and cite the depth(s) in verification_method.
    //   - if the chain is all-havoc (no dash rows): verified_in_lineage=false; note that
    //     I2S contribution may still exist in the leaked havoc bucket, explain (>=20 chars).
    //   - if you could not run db_query (data missing, etc.): verified_in_lineage=false; explain what blocked you
  },
  "falsifiability": {
    "would_be_refuted_by": "ONE concrete observation that, if true, would kill this hypothesis (something a synthetic experiment could observe, not a story)"
  },
  "weakest_evidence_point": "one sentence naming your single most uncertain claim",
  "confidence": "medium"
    // pick EXACTLY ONE of: "high" | "medium" | "low"
}

RULES:
 - No reference to templates/ anywhere in your output. Classification is a separate later pass.
 - Every hypothesis sub-claim must be supported by >=1 evidence_trail entry.
 - exact_quote must be a LITERAL substring of this prompt — COPY-PASTE, do NOT paraphrase, abbreviate, or summarize. A script (tools/check_analysis.py) will reject quotes that do not appear verbatim (whitespace-tolerant).
 - cited_section: the validator accepts either the canonical short name (BLOCKER, BYTE DIFF, etc.) or the full section header from the prompt.
 - claimed_mechanism and mechanism_attribution must agree on the same technique.
 - When claimed_mechanism = "I2SRandReplace": you MUST invoke `python3 tools/db_query.py lineage` on >=1 winning seed BEFORE finalizing the analysis. Record what you observed in verification_method.


DEEP-DIVE QUERIES:
  python3 tools/db_query.py lineage --branch 5990 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5990 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).