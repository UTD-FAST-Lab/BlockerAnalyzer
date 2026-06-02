==== BLOCKER ====
Target: harfbuzz
Branch ID: 5564
Location: /src/harfbuzz/src/hb-ot-layout.cc:775:7
Enclosing function: hb_ot_layout_script_select_language2
Source line:   if (s.find_lang_sys_index (HB_OT_TAG_DEFAULT_LANGUAGE, language_index))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           6        4          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=9.20h  loser=24.00h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.80  dur_div=14.80h  hit_div=5
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5564/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_ot_layout_script_select_language2 (/src/harfbuzz/src/hb-ot-layout.cc:759-787) ---
[ ]   757  				     unsigned int   *language_index /* OUT */,
[ ]   758  				     hb_tag_t       *chosen_language /* OUT */)
[B]   759  {
[B]   760    static_assert ((OT::Index::NOT_FOUND_INDEX == HB_OT_LAYOUT_DEFAULT_LANGUAGE_INDEX), "");
[B]   761    const OT::Script &s = get_gsubgpos_table (face, table_tag).get_script (script_index);
[B]   762    unsigned int i;
[ ]   763  
[B]   764    for (i = 0; i < language_count; i++)
[ ]   765    {
[ ]   766      if (s.find_lang_sys_index (language_tags[i], language_index))
[ ]   767      {
[ ]   768        if (chosen_language)
[ ]   769          *chosen_language = language_tags[i];
[ ]   770        return true;
[ ]   771      }
[ ]   772    }
[ ]   773  
[ ]   774    /* try finding 'dflt' */
[B]   775    if (s.find_lang_sys_index (HB_OT_TAG_DEFAULT_LANGUAGE, language_index)) <-- BLOCKER
[W]   776    {
[W]   777      if (chosen_language)
[ ]   778        *chosen_language = HB_OT_TAG_DEFAULT_LANGUAGE;
[W]   779      return false;
[W]   780    }
[ ]   781  
[B]   782    if (language_index)
[B]   783      *language_index = HB_OT_LAYOUT_DEFAULT_LANGUAGE_INDEX;
[B]   784    if (chosen_language)
[ ]   785      *chosen_language = HB_TAG_NONE;
[B]   786    return false;
[B]   787  }

--- Caller (1 hop): hb_ot_layout_script_select_language (/src/harfbuzz/src/hb-ot-layout.cc:816-821, calls hb_ot_layout_script_select_language2 at line 817) (full body — short) ---
[B]   816  {
[B]   817    return hb_ot_layout_script_select_language2 (face, table_tag, <-- CALL
[B]   818  					       script_index,
[B]   819  					       language_count, language_tags,
[B]   820  					       language_index, nullptr);
[B]   821  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb_ot_layout_script_select_language  (/src/harfbuzz/src/hb-ot-layout.cc:816-821, calls hb_ot_layout_script_select_language2 at line 817)
hop 3  hb_ot_layout_script_find_language  (/src/harfbuzz/src/hb-ot-layout.cc:718-725, calls hb_ot_layout_script_select_language at line 719)
hop 3  hb_ot_map_builder_t::hb_ot_map_builder_t(hb_face_t*, hb_segment_properties_t const&)  (/src/harfbuzz/src/hb-ot-map.cc:47-88, calls hb_ot_layout_script_select_language at line 81)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     182      3720  hb-ot-layout.cc:get_gsubgpos_table(hb_face_t*, unsigned int)  (/src/harfbuzz/src/hb-ot-layout.cc:416-422)
     105      2250  hb_ot_layout_language_find_feature  (/src/harfbuzz/src/hb-ot-layout.cc:995-1012)
      46       836  hb_ot_layout_table_find_feature_variations  (/src/harfbuzz/src/hb-ot-layout.cc:1399-1403)
      21       381  hb-ot-layout.cc:_hb_ot_layout_set_glyph_props(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:255-265)
      21       381  hb_ot_layout_substitute_start(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1510-1512)
      21       381  hb_ot_layout_position_start(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1611-1613)
      21       381  hb_ot_layout_position_finish_advances(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1626-1628)
      21       381  hb_ot_layout_position_finish_offsets(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1640-1642)
      21       381  GSUBProxy::GSUBProxy(hb_face_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1833-1834)
      21       381  void hb_ot_map_t::apply<GSUBProxy>(GSUBProxy const&, hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:1948-1998)
      21       381  void hb_ot_map_t::apply<GPOSProxy>(GPOSProxy const&, hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:1948-1998)
      21       381  hb_ot_map_t::substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:2001-2008)
       8       178  hb_ot_layout_table_get_lookup_count  (/src/harfbuzz/src/hb-ot-layout.cc:1066-1068)
       8       178  hb_ot_layout_feature_with_variations_get_lookups  (/src/harfbuzz/src/hb-ot-layout.cc:1434-1441)
       4        74  hb_ot_layout_table_select_script  (/src/harfbuzz/src/hb-ot-layout.cc:550-591)
... (16 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb_ot_layout_script_select_language2  (/src/harfbuzz/src/hb-ot-layout.cc:759-787) ---
  d=1   L 764  T=0 F=4  T=0 F=74  for (i = 0; i < language_count; i++)
  d=1   L 775  T=2 F=2  T=0 F=74  if (s.find_lang_sys_index (HB_OT_TAG_DEFAULT_LANGUAGE, la...  <-- BLOCKER
  d=1   L 777  T=0 F=2  T=0 F=0  if (chosen_language)
  d=1   L 782  T=2 F=0  T=74 F=0  if (language_index)
  d=1   L 784  T=0 F=2  T=0 F=74  if (chosen_language)

[off-chain: 68 additional divergent branches across 10 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=ad81f9e09b6230b7, size=284 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=6108s, mutation_op=ByteIncMutator,ByteDecMutator):
  0000: 74 79 70 31 00 02 20 20 20 3f 21 20 47 53 55 42   typ1..   ?! GSUB
  0010: b2 b2 2d b2 00 00 00 21 20 6b 20 47 53 47 42 20   ..-....! k GSGB 
  0020: 03 00 01 00 10 00 2c 00 06 00 10 00 20 00 10 00   ......,..... ...
  0030: 06 00 00 00 0c fe 06 00 02 00 22 00 02 00 04 00   ..........".....

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 2 (id=002a5b2b8b5c414d, size=54 bytes, fuzzer=value_profile, trial=2, discovered_at=70s, mutation_op=TokenReplace,BytesCopyMutator,ByteAddMutator,BytesSetMutator):
  0000: 92 92 92 df 68 2d 68 81 6e 74 00 9a 9a 20 8e 8e   ....h-h.nt... ..
  0010: 8e 8e 79 8e 9a 17 00 00 00 01 20 20 44 46 ff 54   ..y.......  DF.T
  0020: 70 7f 70 70 70 70 70 52 9a 9a ff df 68 2d 68 61   p.pppppR....h-ha
  0030: 6e 74 00 9a 9a 74                                 nt...t
Seed 3 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 4 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i
Seed 5 (id=00167ff70704a0e0, size=23 bytes, fuzzer=value_profile, trial=1, discovered_at=120s, mutation_op=BytesInsertCopyMutator,CrossoverInsertMutator,ByteDecMutator):
  0000: 4c 0e 00 00 4c 0e 00 00 4c 16 00 00 00 18 18 00   L...L...L.......
  0010: 00 42 18 65 0e 00 ff                              .B.e...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  74(t)x1                             00(.)x3 e0(.)x2 fe(.)x1 92(.)x1 +13u  DIFFER
   0x0001  79(y)x1                             00(.)x2 ff(.)x1 92(.)x1 17(.)x1 +15u  DIFFER
   0x0002  70(p)x1                             00(.)x8 ff(.)x2 6e(n)x2 92(.)x1 +7u  DIFFER
   0x0003  31(1)x1                             00(.)x9 ff(.)x2 df(.)x1 6c(l)x1 +7u  DIFFER
   0x0004  00(.)x1                             df(.)x2 f4(.)x1 68(h)x1 1a(.)x1 +15u  PARTIAL
   0x0005  02(.)x1                             00(.)x4 20( )x3 01(.)x2 0e(.)x2 +9u  DIFFER
   0x0006  20( )x1                             00(.)x11 e0(.)x1 68(h)x1 73(s)x1 +6u  PARTIAL
   0x0007  20( )x1                             00(.)x11 39(9)x2 e0(.)x1 81(.)x1 +5u  PARTIAL
   0x0008  20( )x1                             00(.)x4 20( )x3 10(.)x2 6e(n)x1 +10u  PARTIAL
   0x0009  3f(?)x1                             00(.)x4 20( )x2 74(t)x1 2b(+)x1 +12u  DIFFER
   0x000a  21(!)x1                             00(.)x10 29())x1 aa(.)x1 61(a)x1 +7u  DIFFER
   0x000b  20( )x1                             00(.)x9 9a(.)x1 29())x1 13(.)x1 +8u  DIFFER
   0x000c  47(G)x1                             00(.)x4 01(.)x1 9a(.)x1 2c(,)x1 +13u  DIFFER
   0x000d  53(S)x1                             20( )x5 00(.)x5 18(.)x3 01(.)x1 +5u  DIFFER
   0x000e  55(U)x1                             00(.)x8 e0(.)x1 8e(.)x1 18(.)x1 +8u  DIFFER
   0x000f  42(B)x1                             00(.)x7 6a(j)x1 8e(.)x1 fa(.)x1 +9u  DIFFER
   0x0010  b2(.)x1                             00(.)x5 20( )x2 79(y)x1 8e(.)x1 +10u  DIFFER
   0x0011  b2(.)x1                             00(.)x3 a9(.)x2 20( )x2 2d(-)x1 +11u  DIFFER
   0x0012  2d(-)x1                             00(.)x10 68(h)x1 79(y)x1 18(.)x1 +6u  DIFFER
   0x0013  b2(.)x1                             00(.)x7 61(a)x1 8e(.)x1 55(U)x1 +9u  DIFFER
   0x0014  00(.)x1                             00(.)x5 6e(n)x1 9a(.)x1 e0(.)x1 +11u  PARTIAL
   0x0015  00(.)x1                             00(.)x5 17(.)x2 20( )x2 74(t)x1 +9u  PARTIAL
   0x0016  00(.)x1                             00(.)x12 2d(-)x1 ff(.)x1 3d(=)x1 +4u  PARTIAL
   0x0017  21(!)x1                             00(.)x11 68(h)x1 3d(=)x1 2d(-)x1 +4u  DIFFER
   0x0018  20( )x1                             00(.)x4 20( )x2 6b(k)x1 61(a)x1 +10u  PARTIAL
   0x0019  6b(k)x1                             00(.)x4 20( )x2 a8(.)x2 01(.)x1 +9u  DIFFER
   0x001a  20( )x1                             00(.)x8 20( )x3 69(i)x1 3d(=)x1 +5u  PARTIAL
   0x001b  47(G)x1                             00(.)x8 20( )x2 3d(=)x1 74(t)x1 +5u  DIFFER
   0x001c  53(S)x1                             00(.)x5 44(D)x1 3d(=)x1 e3(.)x1 +9u  DIFFER
   0x001d  47(G)x1                             00(.)x4 20( )x3 46(F)x1 3d(=)x1 +8u  DIFFER
   0x001e  42(B)x1                             00(.)x11 ff(.)x2 80(.)x1 6a(j)x1 +2u  DIFFER
   0x001f  20( )x1                             00(.)x8 54(T)x2 01(.)x1 ff(.)x1 +5u  DIFFER
   0x0020  03(.)x1                             00(.)x5 70(p)x1 df(.)x1 39(9)x1 +9u  DIFFER
   0x0021  00(.)x1                             07(.)x2 0e(.)x2 00(.)x2 7f(.)x1 +10u  PARTIAL
   0x0022  01(.)x1                             00(.)x10 70(p)x1 64(d)x1 1b(.)x1 +4u  DIFFER
   0x0023  00(.)x1                             00(.)x9 70(p)x1 73(s)x1 6d(m)x1 +5u  PARTIAL
   0x0024  10(.)x1                             00(.)x4 20( )x2 01(.)x1 70(p)x1 +9u  PARTIAL
   0x0025  00(.)x1                             00(.)x4 20( )x2 03(.)x2 0e(.)x2 +7u  PARTIAL
   0x0026  2c(,)x1                             00(.)x9 20( )x1 70(p)x1 ff(.)x1 +5u  DIFFER
   0x0027  00(.)x1                             00(.)x6 20( )x3 61(a)x2 52(R)x1 +5u  PARTIAL
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- value_profile ---
**Instrumentation**: naive's edge counters **plus** integer-CMP
interception, but instead of buffering operands per execution (cmplog),
each CMP callback writes into a `CMP_MAP` keyed by (PC, operand-distance
bucket). The distance bucket is a coarse encoding of how close the two
operands were (Hamming distance bucket for `trace_cmp*`; matching-prefix
length for string/memory CMPs).

**Feedback**: edge-bucket signal **plus** new-CMP_MAP-bucket signal
(both via `MaxMapFeedback`-style coverage). An input that produces a
CMP-operand pair closer to matching than any previously-seen pair
adds a new CMP_MAP bucket and is preserved as corpus.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`.

**Observed `mutation_op` in seed metadata**: havoc/token names only —
no ParentInfo-only entries (no `mutation_op = -` rows). Absence of
the dash signal is direct evidence the seed was found by naive or
value_profile, not by an I2S stage.
<!-- TODO(i2s-logging-bug): when the I2SRandReplace logging fix lands,
     this section becomes "Absence of `I2SRandReplace` is direct
     evidence ..." again. See the cmplog section above for the floor
     caveat. -->


**Per-execution cost**: edge increment + CMP_MAP update per intercepted
CMP per execution.

--- value_profile_cmplog ---
**Instrumentation**: union of cmplog and value_profile — edge counters,
per-execution CMP buffer (`CmpLogObserver`), and CMP_MAP gradient buckets.

**Feedback**: edge-bucket + CMP_MAP-bucket signals.

**Mutators**: naive's havoc + token stack **plus** `I2SRandReplace`.

**Observed `mutation_op` in seed metadata**: havoc/token names; **plus**
silent ParentInfo-only entries (`mutation_op = -` in lineage) — same
floor signal as cmplog. See the cmplog section's
`TODO(i2s-logging-bug)` note.

**Per-execution cost**: edge increment + CMP-buffer record + CMP_MAP
update per intercepted CMP per execution.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5564.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5564,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5564 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5564 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5564 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).