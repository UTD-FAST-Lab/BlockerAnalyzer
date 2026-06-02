==== BLOCKER ====
Target: harfbuzz
Branch ID: 5483
Location: /src/harfbuzz/src/hb-ot-layout-common.hh:2000:5
Enclosing function: OT::ClassDef::get_class(unsigned int) const
Source line:     case 4: return u.format4.get_class (glyph_id);
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  REFERENCE
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.40h  loser=24.00h
  avg hitcount on branch: winner=162  loser=0
  prob_div=1.00  dur_div=20.60h  hit_div=162
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5483/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::ClassDef::get_class(unsigned int) const (/src/harfbuzz/src/hb-ot-layout-common.hh:1994-2004) ---
[ ]  1992    unsigned int get (hb_codepoint_t k) const { return get_class (k); }
[ ]  1993    unsigned int get_class (hb_codepoint_t glyph_id) const
[B]  1994    {
[B]  1995      switch (u.format) {
[ ]  1996      case 1: return u.format1.get_class (glyph_id);
[ ]  1997      case 2: return u.format2.get_class (glyph_id);
[ ]  1998  #ifndef HB_NO_BEYOND_64K
[ ]  1999      case 3: return u.format3.get_class (glyph_id);
[W]  2000      case 4: return u.format4.get_class (glyph_id); <-- BLOCKER
[ ]  2001  #endif
[L]  2002      default:return 0;
[B]  2003      }
[B]  2004    }

--- Caller (1 hop): OT::GDEF::get_glyph_class(unsigned int) const (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:801-801, calls OT::ClassDef::get_class(unsigned int) const at line 801) (full body — short) ---
[B]   801    { return get_glyph_class_def ().get_class (glyph); } <-- CALL

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  AAT::ClassTable<OT::IntType<unsigned char, 1u> >::get_class(unsigned int, unsigned int, unsigned int) const  (/src/harfbuzz/src/hb-aat-layout-common.hh:682-684, calls OT::ClassDef::get_class(unsigned int) const at line 683)
hop 2  AAT::StateTable<AAT::ExtendedTypes, void>::get_class(unsigned int, unsigned int) const  (/src/harfbuzz/src/hb-aat-layout-common.hh:532-535, calls OT::ClassDef::get_class(unsigned int) const at line 534)
hop 3  void AAT::StateTableDriver<AAT::ExtendedTypes, void>::drive<AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t>(AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t*, AAT::hb_aat_apply_context_t*)  (/src/harfbuzz/src/hb-aat-layout-common.hh:782-905, calls AAT::StateTable<AAT::ExtendedTypes, void>::get_class(unsigned int, unsigned int) const at line 818)
hop 4  AAT::ContextualSubtable<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:322-331, calls void AAT::StateTableDriver<AAT::ExtendedTypes, void>::drive<AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t>(AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t*, AAT::hb_aat_apply_context_t*) at line 328)
hop 4  AAT::RearrangementSubtable<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:166-175, calls void AAT::StateTableDriver<AAT::ExtendedTypes, void>::drive<AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t>(AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t*, AAT::hb_aat_apply_context_t*) at line 172)
hop 5  AAT::Chain<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:1017-1085, calls AAT::RearrangementSubtable<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const at line 1072)
hop 5  AAT::mortmorx<AAT::ExtendedTypes, 1836020344u>::apply(AAT::hb_aat_apply_context_t*, hb_aat_map_t const&) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:1156-1171, calls AAT::RearrangementSubtable<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const at line 1167)
hop 6  bool AAT::hb_aat_apply_context_t::dispatch<AAT::RearrangementSubtable<AAT::ExtendedTypes> >(AAT::RearrangementSubtable<AAT::ExtendedTypes> const&)  (/src/harfbuzz/src/hb-aat-layout-common.hh:50-50, calls AAT::Chain<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const at line 50)
hop 7  hb_subset_context_t::return_t OT::AxisValue::dispatch<hb_subset_context_t, hb_array_t<OT::StatAxisRecord const> const&>(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const> const&) const  (/src/harfbuzz/src/hb-ot-stat-table.hh:392-402, calls bool AAT::hb_aat_apply_context_t::dispatch<AAT::RearrangementSubtable<AAT::ExtendedTypes> >(AAT::RearrangementSubtable<AAT::ExtendedTypes> const&) at line 396)
hop 8  hb_sanitize_context_t::return_t AAT::ChainSubtable<AAT::ExtendedTypes>::dispatch<hb_sanitize_context_t>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:924-935, calls hb_subset_context_t::return_t OT::AxisValue::dispatch<hb_subset_context_t, hb_array_t<OT::StatAxisRecord const> const&>(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const> const&) const at line 928)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     170      4080  OT::GSUBGPOS::get_script_list() const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:4237-4245)
     164      3980  OT::RecordArrayOf<OT::Script>::get_offset(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:888-888)
     164      3980  OT::RecordArrayOf<OT::Feature>::get_offset(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:888-888)
     164      3980  OT::RecordListOf<OT::Script>::operator[](unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:916-916)
     164      3980  OT::RecordListOf<OT::Feature>::operator[](unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:916-916)
     154      3630  OT::GSUBGPOS::get_script(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:4297-4297)
     150      3520  OT::Script::get_lang_sys(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1090-1093)
     149      3490  OT::Script::get_default_lang_sys() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1098-1098)
     145      3380  OT::LangSys::get_feature_count() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:970-970)
      54      1620  OT::GDEF::get_glyph_class_def() const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:688-696)
      54      1620  OT::GDEF::get_glyph_class(unsigned int) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:801-801)
      54      1620  OT::GDEF::get_glyph_props(unsigned int) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:831-846)
      54      1620  OT::ClassDef::get_class(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1994-2004)  <-- enclosing
      47      1410  OT::Device::get_y_delta(hb_font_t*, OT::VariationStore const&, float*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:3576-3590)
      46      1370  OT::FeatureVariations::find_index(int const*, unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:3279-3292)
... (65 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::ClassDef::get_class(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1994-2004) ---
  d=1   L1996  T=0 F=54  T=0 F=1620  case 1: return u.format1.get_class (glyph_id);
  d=1   L1997  T=0 F=54  T=0 F=1620  case 2: return u.format2.get_class (glyph_id);
  d=1   L1999  T=0 F=54  T=0 F=1620  case 3: return u.format3.get_class (glyph_id);
  d=1   L2000  T=54 F=0  T=0 F=1620  case 4: return u.format4.get_class (glyph_id);  <-- BLOCKER
  d=1   L2002  T=0 F=54  T=1620 F=0  default:return 0;

[off-chain: 72 additional divergent branches across 27 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=2b85cc197690055a, size=120 bytes, fuzzer=cmplog, trial=3, discovered_at=2264s, mutation_op=BytesSetMutator,DwordInterestingMutator,CrossoverReplaceMutator,WordAddMutator,BytesSetMutator):
  0000: 74 72 75 65 00 01 a0 20 19 20 0d 01 47 44 45 46   true... . ..GDEF
  0010: 20 20 20 07 00 00 00 20 00 00 fe 00 65 00 10 04      .... ....e...
  0020: 00 01 00 03 00 04 00 00 00 02 00 02 00 1c 96 01   ................
  0030: 03 00 00 00 03 00 00 00 00 00 00 dd 62 05 08 00   ............b...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003817559785f774, size=6 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteDecMutator,WordAddMutator):
  0000: 87 0e 0d 0e 22 0e                                 ....".
Seed 2 (id=002edec370c771cf, size=35 bytes, fuzzer=naive, trial=1, discovered_at=47s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteNegMutator,TokenInsert,ByteIncMutator,ByteRandMutator):
  0000: 00 00 00 00 00 00 00 00 00 00 00 00 20 00 64 6f   ............ .do
  0010: 2d 68 0a 6f 74 00 0e 00 20 00 0c 00 0c 09 00 00   -h.ot... .......
  0020: 00 0c 00                                          ...
Seed 3 (id=0037172fe96408cc, size=63 bytes, fuzzer=naive, trial=3, discovered_at=225s, mutation_op=TokenInsert,BytesDeleteMutator):
  0000: 00 fc 20 04 00 23 00 00 ea 19 00 00 00 0c 00 75   .. ..#.........u
  0010: 75 2d 68 61 6e 74 2d 6d 6f 00 00 80 00 00 01 00   u-hant-mo.......
  0020: 76 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00   v ..............
  0030: 00 20 20 20 20 20 20 20 20 20 20 20 20 20 61      .             a
Seed 4 (id=004233a9fffa6068, size=44 bytes, fuzzer=naive, trial=3, discovered_at=286s, mutation_op=QwordAddMutator,BytesExpandMutator):
  0000: 00 00 00 fc ff ff fe f0 00 fd ff ff ff 19 00 00   ................
  0010: c8 1e 01 00 02 0e 01 00 00 1e 01 00 02 0e 01 00   ................
  0020: 00 ff 00 00 00 a5 6d 6c 74 72 54 00               ......mltrT.
Seed 5 (id=0050b0108ec442e2, size=14 bytes, fuzzer=naive, trial=3, discovered_at=290s, mutation_op=DwordInterestingMutator):
  0000: 3d ff ff ff 7f 18 00 00 00 09 00 00 6e ac         =...........n.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  74(t)x1                             00(.)x13 05(.)x2 87(.)x1 3d(=)x1 +13u  DIFFER
   0x0001  72(r)x1                             00(.)x7 ff(.)x2 f6(.)x2 18(.)x2 +15u  DIFFER
   0x0002  75(u)x1                             00(.)x15 ff(.)x5 20( )x2 0d(.)x1 +7u  DIFFER
   0x0003  65(e)x1                             00(.)x15 2d(-)x2 0e(.)x1 04(.)x1 +11u  DIFFER
   0x0004  00(.)x1                             00(.)x7 68(h)x2 70(p)x2 22(")x1 +18u  PARTIAL
   0x0005  01(.)x1                             00(.)x6 0e(.)x3 18(.)x2 20( )x2 +17u  PARTIAL
   0x0006  a0(.)x1                             00(.)x17 fe(.)x1 68(h)x1 69(i)x1 +9u  DIFFER
   0x0007  20( )x1                             00(.)x17 f6(.)x2 f0(.)x1 77(w)x1 +8u  DIFFER
   0x0008  19(.)x1                             00(.)x7 ea(.)x1 72(r)x1 34(4)x1 +19u  DIFFER
   0x0009  20( )x1                             00(.)x5 19(.)x2 20( )x2 ff(.)x2 +18u  PARTIAL
   0x000a  0d(.)x1                             00(.)x12 01(.)x3 ff(.)x2 06(.)x2 +9u  DIFFER
   0x000b  01(.)x1                             00(.)x13 ff(.)x5 75(u)x1 1a(.)x1 +9u  PARTIAL
   0x000c  47(G)x1                             00(.)x5 ff(.)x5 0f(.)x2 20( )x1 +16u  DIFFER
   0x000d  44(D)x1                             00(.)x6 29())x2 20( )x2 0c(.)x1 +18u  DIFFER
   0x000e  45(E)x1                             00(.)x14 01(.)x2 64(d)x1 2d(-)x1 +10u  DIFFER
   0x000f  46(F)x1                             00(.)x14 19(.)x2 6f(o)x1 75(u)x1 +10u  DIFFER
   0x0010  20( )x1                             00(.)x12 01(.)x2 2d(-)x1 75(u)x1 +12u  DIFFER
   0x0011  20( )x1                             00(.)x5 01(.)x3 20( )x2 06(.)x2 +15u  PARTIAL
   0x0012  20( )x1                             00(.)x16 01(.)x2 05(.)x2 0a(.)x1 +7u  PARTIAL
   0x0013  07(.)x1                             00(.)x15 2d(-)x2 40(@)x2 6f(o)x1 +8u  DIFFER
   0x0014  00(.)x1                             00(.)x5 68(h)x3 74(t)x1 6e(n)x1 +18u  PARTIAL
   0x0015  00(.)x1                             00(.)x5 01(.)x3 06(.)x2 7c(|)x2 +16u  PARTIAL
   0x0016  00(.)x1                             00(.)x10 01(.)x3 0e(.)x2 2d(-)x2 +10u  PARTIAL
   0x0017  20( )x1                             00(.)x11 74(t)x2 64(d)x2 6d(m)x1 +12u  PARTIAL
   0x0018  00(.)x1                             00(.)x6 20( )x3 a8(.)x2 6f(o)x1 +16u  PARTIAL
   0x0019  00(.)x1                             00(.)x6 01(.)x2 0e(.)x2 1e(.)x1 +17u  PARTIAL
   0x001a  fe(.)x1                             00(.)x10 01(.)x5 0c(.)x1 9f(.)x1 +11u  DIFFER
   0x001b  00(.)x1                             00(.)x12 ff(.)x4 80(.)x1 f3(.)x1 +10u  PARTIAL
   0x001c  65(e)x1                             00(.)x9 19(.)x2 0c(.)x1 02(.)x1 +15u  DIFFER
   0x001d  00(.)x1                             00(.)x9 0e(.)x3 20( )x2 09(.)x1 +13u  PARTIAL
   0x001e  10(.)x1                             00(.)x12 01(.)x6 61(a)x1 70(p)x1 +8u  DIFFER
   0x001f  04(.)x1                             00(.)x15 20( )x3 19(.)x1 6e(n)x1 +7u  DIFFER
   0x0020  00(.)x1                             00(.)x7 20( )x2 01(.)x2 76(v)x1 +15u  PARTIAL
   0x0021  01(.)x1                             00(.)x5 20( )x4 ff(.)x3 10(.)x2 +13u  PARTIAL
   0x0022  00(.)x1                             00(.)x12 01(.)x3 02(.)x1 fa(.)x1 +9u  PARTIAL
   0x0023  03(.)x1                             00(.)x10 02(.)x1 ff(.)x1 19(.)x1 +11u  DIFFER
   0x0024  00(.)x1                             00(.)x6 40(@)x2 02(.)x1 ff(.)x1 +13u  PARTIAL
   0x0025  04(.)x1                             00(.)x6 01(.)x2 a5(.)x1 02(.)x1 +13u  DIFFER
   0x0026  00(.)x1                             00(.)x8 01(.)x3 61(a)x2 6d(m)x1 +9u  PARTIAL
   0x0027  00(.)x1                             00(.)x7 20( )x2 6c(l)x1 02(.)x1 +12u  PARTIAL
   ... (24 more divergent offsets)
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5483.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5483,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5483 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5483 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5483 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).