==== BLOCKER ====
Target: harfbuzz
Branch ID: 5474
Location: /src/harfbuzz/src/hb-ot-layout-common.hh:688:9
Enclosing function: OT::FeatureParams::sanitize(hb_sanitize_context_t*, unsigned int) const
Source line:     if (tag == HB_TAG ('s','i','z','e'))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        0         10  REFERENCE
cmplog                           1        9          0  loser (value_profile vs value_profile_cmplog)
value_profile                    0        0         10  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=5.00h  loser=20.10h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.80  dur_div=15.10h  hit_div=5
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5474/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::FeatureParams::sanitize(hb_sanitize_context_t*, unsigned int) const (/src/harfbuzz/src/hb-ot-layout-common.hh:683-695) ---
[ ]   681  {
[ ]   682    bool sanitize (hb_sanitize_context_t *c, hb_tag_t tag) const
[B]   683    {
[ ]   684  #ifdef HB_NO_LAYOUT_FEATURE_PARAMS
[ ]   685      return true;
[ ]   686  #endif
[B]   687      TRACE_SANITIZE (this);
[B]   688      if (tag == HB_TAG ('s','i','z','e')) <-- BLOCKER
[W]   689        return_trace (u.size.sanitize (c));
[L]   690      if ((tag & 0xFFFF0000u) == HB_TAG ('s','s','\0','\0')) /* ssXX */
[ ]   691        return_trace (u.stylisticSet.sanitize (c));
[L]   692      if ((tag & 0xFFFF0000u) == HB_TAG ('c','v','\0','\0')) /* cvXX */
[ ]   693        return_trace (u.characterVariants.sanitize (c));
[L]   694      return_trace (true);
[L]   695    }

--- Caller (1 hop): OT::Record<OT::LangSys>::sanitize(hb_sanitize_context_t*, void const*) const (/src/harfbuzz/src/hb-ot-layout-common.hh:870-874, calls OT::FeatureParams::sanitize(hb_sanitize_context_t*, unsigned int) const at line 873) (full body — short) ---
[B]   870    {
[B]   871      TRACE_SANITIZE (this);
[B]   872      const Record_sanitize_closure_t closure = {tag, base};
[B]   873      return_trace (c->check_struct (this) && offset.sanitize (c, base, &closure)); <-- CALL
[B]   874    }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:90-102, calls OT::FeatureParams::sanitize(hb_sanitize_context_t*, unsigned int) const at line 97)
hop 3  CFF::CFF2VariationStore::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:117-120, calls CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const at line 119)
hop 3  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:398-475, calls CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const at line 416)
hop 4  OT::cff2::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:515-515, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 515)
hop 4  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::~accelerator_templ_t()  (/src/harfbuzz/src/hb-ot-cff2-table.hh:476-476, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 476)
hop 5  OT::cff2_accelerator_t::cff2_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:538-538, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 538)
hop 5  OT::hmtx_accelerator_t::hmtx_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:449-449, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 449)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     120       940  OT::RecordArrayOf<OT::Script>::get_offset(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:888-888)
     120       940  OT::RecordArrayOf<OT::Feature>::get_offset(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:888-888)
     120       940  OT::RecordListOf<OT::Script>::operator[](unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:916-916)
     120       940  OT::RecordListOf<OT::Feature>::operator[](unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:916-916)
       0       768  OT::ArrayOf<OT::OffsetTo<OT::Layout::GPOS_impl::PosLookupSubTable, OT::IntType<unsigned short, 2u>, true>, OT::IntType<unsigned short, 2u> > const& OT::Lookup::get_subtables<OT::Layout::GPOS_impl::PosLookupSubTable>() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1257-1257)
       0       768  OT::ArrayOf<OT::OffsetTo<OT::Layout::GSUB_impl::SubstLookupSubTable, OT::IntType<unsigned short, 2u>, true>, OT::IntType<unsigned short, 2u> > const& OT::Lookup::get_subtables<OT::Layout::GSUB_impl::SubstLookupSubTable>() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1257-1257)
     110       830  OT::Script::get_lang_sys(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1090-1093)
     109       820  OT::Script::get_default_lang_sys() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1098-1098)
     105       790  OT::LangSys::get_feature_count() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:970-970)
       0       632  OT::Layout::GPOS_impl::PosLookupSubTable const& OT::Lookup::get_subtable<OT::Layout::GPOS_impl::PosLookupSubTable>(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1264-1264)
       0       632  OT::Layout::GSUB_impl::SubstLookupSubTable const& OT::Lookup::get_subtable<OT::Layout::GSUB_impl::SubstLookupSubTable>(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1264-1264)
      45       597  OT::VariationStore::destroy_cache(float*)  (/src/harfbuzz/src/hb-ot-layout-common.hh:2656-2656)
      54       540  OT::ClassDef::get_class(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1994-2004)
      47       470  OT::Device::get_y_delta(hb_font_t*, OT::VariationStore const&, float*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:3576-3590)
      46       450  OT::FeatureVariations::find_index(int const*, unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:3279-3292)
... (86 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:398-475) ---
  d=3   L 411  T=1 F=0  T=10 F=0  if (cff2 == &Null (OT::cff2))
--- d=1  OT::FeatureParams::sanitize(hb_sanitize_context_t*, unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:683-695) ---
  d=1   L 688  T=2 F=0  T=0 F=54  if (tag == HB_TAG ('s','i','z','e'))  <-- BLOCKER
  d=1   L 690  T=0 F=0  T=0 F=54  if ((tag & 0xFFFF0000u) == HB_TAG ('s','s','\0','\0')) /*...
  d=1   L 692  T=0 F=0  T=0 F=54  if ((tag & 0xFFFF0000u) == HB_TAG ('c','v','\0','\0')) /*...

[off-chain: 79 additional divergent branches across 23 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d45ebf40b01e6164, size=172 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=3164s, mutation_op=QwordAddMutator,BytesExpandMutator,BitFlipMutator):
  0000: 00 01 00 00 00 02 24 20 60 3f 21 20 47 53 55 42   ......$ `?! GSUB
  0010: 20 20 00 06 00 00 00 21 20 6b 20 47 53 48 42 20     .....! k GSHB 
  0020: 2e 00 01 00 01 00 00 00 10 00 02 00 21 00 02 00   ............!...
  0030: 10 00 02 00 10 00 02 00 21 73 69 7a 65 00 02 00   ........!size...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0bd0a4da89946062, size=235 bytes, fuzzer=cmplog, trial=1, discovered_at=4410s, mutation_op=CrossoverInsertMutator):
  0000: 00 01 00 00 00 01 20 02 21 20 20 20 47 53 55 42   ...... .!   GSUB
  0010: 00 01 00 0d 00 00 00 10 00 02 00 00 10 00 00 20   ............... 
  0020: 00 20 20 00 00 02 00 20 20 20 20 32 32 32 0a 00   .  ....    222..
  0030: 00 00 00 02 0d 00 00 36 00 00 00 14 00 00 00 20   .......6....... 
Seed 2 (id=05cfe0bf61744ee7, size=309 bytes, fuzzer=cmplog, trial=1, discovered_at=4553s, mutation_op=CrossoverInsertMutator,WordAddMutator,DwordAddMutator,TokenInsert,BytesDeleteMutator):
  0000: 00 01 00 00 00 01 07 20 21 1e 1e 5e 47 50 4f 53   ....... !..^GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 02 00 00 0a   ...........G....
  0020: 00 01 00 04 4f ff 00 10 00 10 21 20 1e 20 47 50   ....O.....! . GP
  0030: 4f 53 00 01 00 10 00 00 00 10 00 02 00 47 01 e7   OS...........G..
Seed 3 (id=0248328fc3de4993, size=149 bytes, fuzzer=cmplog, trial=1, discovered_at=4895s, mutation_op=ByteInterestingMutator,BytesCopyMutator,BytesDeleteMutator,CrossoverInsertMutator,ByteRandMutator):
  0000: 00 01 00 00 00 01 07 20 21 1f 1e 5e 47 50 4f 53   ....... !..^GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 02 01 00 0a   ...........G....
  0020: 00 01 00 04 4f ff 00 10 00 10 21 20 1e 20 47 50   ....O.....! . GP
  0030: 4f 53 00 01 00 10 0c 02 00 03 00 02 00 00 02 00   OS..............
Seed 4 (id=00218955463cc452, size=348 bytes, fuzzer=cmplog, trial=1, discovered_at=5194s, mutation_op=ByteDecMutator,DwordInterestingMutator,BytesDeleteMutator,QwordAddMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 01 00 00 00   ...........G....
  0020: 00 02 00 02 4f 00 00 10 00 02 00 10 00 50 50 00   ....O........PP.
  0030: 00 06 00 03 00 01 00 06 00 10 00 01 00 10 00 00   ................
Seed 5 (id=0ba806c58a8a711e, size=253 bytes, fuzzer=cmplog, trial=1, discovered_at=5926s, mutation_op=BytesSetMutator,BytesDeleteMutator,BytesDeleteMutator,DwordAddMutator):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 02 04 00 0a   ...........G....
  0020: 00 01 00 05 4f 00 00 10 00 10 21 00 00 10 00 50   ....O.....!....P
  0030: 4f 53 00 01 00 0d 01 00 00 10 00 02 00 02 00 02   OS..............


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  02(.)x1                             01(.)x8 02(.)x2                     PARTIAL
   0x0006  24($)x1                             07(.)x8 20( )x1 06(.)x1             DIFFER
   0x0007  20( )x1                             20( )x9 02(.)x1                     PARTIAL
   0x0008  60(`)x1                             21(!)x7 2d(-)x1 de(.)x1 25(%)x1     DIFFER
   0x0009  3f(?)x1                             20( )x7 1e(.)x1 1f(.)x1 de(.)x1     DIFFER
   0x000a  21(!)x1                             1e(.)x8 20( )x1 de(.)x1             DIFFER
   0x000b  20( )x1                             20( )x6 5e(^)x2 de(.)x1 df(.)x1     PARTIAL
   0x000d  53(S)x1                             50(P)x8 53(S)x2                     PARTIAL
   0x000e  55(U)x1                             4f(O)x8 55(U)x2                     PARTIAL
   0x000f  42(B)x1                             53(S)x8 42(B)x2                     PARTIAL
   0x0010  20( )x1                             00(.)x10                            DIFFER
   0x0011  20( )x1                             01(.)x10                            DIFFER
   0x0013  06(.)x1                             0d(.)x9 06(.)x1                     PARTIAL
   0x0017  21(!)x1                             10(.)x10                            DIFFER
   0x0018  20( )x1                             00(.)x10                            DIFFER
   0x0019  6b(k)x1                             02(.)x10                            DIFFER
   0x001a  20( )x1                             00(.)x9 22(")x1                     DIFFER
   0x001b  47(G)x1                             47(G)x9 00(.)x1                     PARTIAL
   0x001c  53(S)x1                             02(.)x3 10(.)x1 01(.)x1 fa(.)x1 +4u  DIFFER
   0x001d  48(H)x1                             00(.)x6 01(.)x1 04(.)x1 06(.)x1 +1u  DIFFER
   0x001e  42(B)x1                             00(.)x8 2f(/)x1 69(i)x1             DIFFER
   0x001f  20( )x1                             0a(.)x3 00(.)x2 20( )x1 02(.)x1 +3u  PARTIAL
   0x0020  2e(.)x1                             00(.)x10                            DIFFER
   0x0021  00(.)x1                             02(.)x5 01(.)x3 20( )x1 1b(.)x1     DIFFER
   0x0022  01(.)x1                             00(.)x9 20( )x1                     DIFFER
   0x0023  00(.)x1                             04(.)x2 02(.)x2 08(.)x2 00(.)x1 +3u  PARTIAL
   0x0024  01(.)x1                             4f(O)x8 00(.)x2                     DIFFER
   0x0025  00(.)x1                             00(.)x6 ff(.)x2 02(.)x1 04(.)x1     PARTIAL
   0x0027  00(.)x1                             10(.)x9 20( )x1                     DIFFER
   0x0028  10(.)x1                             00(.)x7 02(.)x2 20( )x1             DIFFER
   0x0029  00(.)x1                             10(.)x4 00(.)x3 02(.)x2 20( )x1     PARTIAL
   0x002a  02(.)x1                             00(.)x6 21(!)x3 20( )x1             DIFFER
   0x002b  00(.)x1                             10(.)x5 20( )x3 32(2)x1 00(.)x1     PARTIAL
   0x002c  21(!)x1                             00(.)x7 1e(.)x2 32(2)x1             DIFFER
   0x002d  00(.)x1                             10(.)x5 20( )x2 32(2)x1 50(P)x1 +1u  DIFFER
   0x002e  02(.)x1                             00(.)x4 47(G)x2 0a(.)x1 50(P)x1 +2u  DIFFER
   0x002f  00(.)x1                             50(P)x3 00(.)x2 01(.)x2 06(.)x2 +1u  PARTIAL
   0x0030  10(.)x1                             00(.)x7 4f(O)x3                     DIFFER
   0x0031  00(.)x1                             10(.)x4 53(S)x3 00(.)x1 06(.)x1 +1u  PARTIAL
   0x0032  02(.)x1                             00(.)x10                            DIFFER
   ... (13 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- cmplog ---
**Instrumentation**: naive's edge counters **plus** integer-CMP
interception (`__sanitizer_cov_trace_cmp1/2/4/8`) and
string/memory-CMP interception (`__sanitizer_weak_hook_strcmp`,
`__sanitizer_weak_hook_memcmp`, etc.). Each CMP callback records
both operands into a per-execution `CmpLogObserver` buffer keyed by
PC.

**Feedback**: same edge-bucket signal as naive. The CMP buffer is
consumed by the mutator, not by feedback.

**Mutators**: naive's havoc + token stack **plus** `I2SRandReplace`.
`I2SRandReplace` reads the post-execution `CmpLogObserver` buffer,
picks a CMP entry, scans the input for byte sequences matching one
operand, and substitutes the other operand at those offsets.

**Observed `mutation_op` in seed metadata**:
<!-- TODO(i2s-logging-bug): the current LibAFL fuzzbench build does NOT
     wrap I2SRandReplace in LogMutationMetadata, so the string
     "I2SRandReplace" never appears in `.metadata`. Instead, I2S finds
     surface as seeds whose metadata has ParentInfo but NO mutator-name
     list — these render as `mutation_op = -` in `db_query.py lineage`
     output and `resolving_seeds.mutation_op IS NULL` in SQL.
     Confirmed 2026-05-17: naive/vp produce ZERO such seeds in 6000
     samples; cmplog/vpc produce them at ~0.1–0.3%. This is a LOWER
     BOUND ("floor") — some I2S finds leak into the havoc bucket
     because other stages wrap I2S as a sub-mutator and tag the result
     with their own havoc/token list. When the logging fix lands,
     revert this caveat and require the literal `I2SRandReplace`
     string instead. -->
havoc/token names; **plus** silent ParentInfo-only entries
(`mutation_op = -` in lineage output) that — in cmplog/vpc only —
indicate an I2SRandReplace find under the current build. The dash
rows are exclusive to cmplog and value_profile_cmplog **within the
original 4-fuzzer canonical set**; there their presence in a winning
seed's ancestor chain is direct (lower-bound) evidence of I2S
contribution.
<!-- CAVEAT(10-fuzzer set, 2026-05-27): dash-row = I2S only holds when
     comparing against naive / value_profile. `mopt` and `grimoire`
     wrap their mutators in LineageMutatorWrap with an EMPTY names list,
     so they ALSO emit nameless (`mutation_op = -`) rows for non-I2S
     finds — see the mopt / grimoire sections. Against those two the
     dash signal is NOT I2S-exclusive. fast / minimizer / naive_ctx /
     naive_ngram4 use plain LineageMutator (names captured), so they do
     NOT emit dash rows and the signal stays clean against them. -->

**Per-execution cost**: edge increment + one callback per intercepted
CMP per execution + post-execution CMP-buffer processing.

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
  prompts_b/harfbuzz_5474.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5474,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5474 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5474 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5474 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).