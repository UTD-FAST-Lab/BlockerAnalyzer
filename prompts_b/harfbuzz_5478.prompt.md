==== BLOCKER ====
Target: harfbuzz
Branch ID: 5478
Location: /src/harfbuzz/src/hb-ot-layout-common.hh:983:9
Enclosing function: OT::LangSys::get_required_feature_index() const
Source line:     if (reqFeatureIndex == 0xFFFFu)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.70h  loser=24.00h
  avg hitcount on branch: winner=26  loser=0
  prob_div=1.00  dur_div=19.30h  hit_div=26
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=7.00h  loser=24.00h
  avg hitcount on branch: winner=129  loser=0
  prob_div=0.90  dur_div=17.00h  hit_div=129
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5478/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::LangSys::get_required_feature_index() const (/src/harfbuzz/src/hb-ot-layout-common.hh:982-986) ---
[B]   980    bool has_required_feature () const { return reqFeatureIndex != 0xFFFFu; }
[ ]   981    unsigned int get_required_feature_index () const
[B]   982    {
[B]   983      if (reqFeatureIndex == 0xFFFFu) <-- BLOCKER
[B]   984        return Index::NOT_FOUND_INDEX;
[W]   985     return reqFeatureIndex;
[B]   986    }

--- Caller (1 hop): hb_ot_layout_language_get_required_feature (/src/harfbuzz/src/hb-ot-layout.cc:878-887, calls OT::LangSys::get_required_feature_index() const at line 882) (full body — short) ---
[B]   878  {
[B]   879    const OT::GSUBGPOS &g = get_gsubgpos_table (face, table_tag);
[B]   880    const OT::LangSys &l = g.get_script (script_index).get_lang_sys (language_index);
[ ]   881  
[B]   882    unsigned int index = l.get_required_feature_index (); <-- CALL
[B]   883    if (feature_index) *feature_index = index;
[B]   884    if (feature_tag) *feature_tag = g.get_feature_tag (index);
[ ]   885  
[B]   886    return l.has_required_feature ();
[B]   887  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-layout.cc:langsys_collect_features(hb_collect_features_context_t*, OT::LangSys const&)  (/src/harfbuzz/src/hb-ot-layout.cc:1169-1195, calls OT::LangSys::get_required_feature_index() const at line 1176)
hop 2  hb_ot_layout_language_get_required_feature  (/src/harfbuzz/src/hb-ot-layout.cc:878-887, calls OT::LangSys::get_required_feature_index() const at line 882)
hop 3  hb-ot-layout.cc:script_collect_features(hb_collect_features_context_t*, OT::Script const&, unsigned int const*)  (/src/harfbuzz/src/hb-ot-layout.cc:1201-1228, calls hb-ot-layout.cc:langsys_collect_features(hb_collect_features_context_t*, OT::LangSys const&) at line 1208)
hop 3  hb_ot_layout_language_get_required_feature_index  (/src/harfbuzz/src/hb-ot-layout.cc:845-852, calls hb_ot_layout_language_get_required_feature at line 846)
hop 3  hb_ot_map_builder_t::compile(hb_ot_map_t&, hb_ot_shape_plan_key_t const&)  (/src/harfbuzz/src/hb-ot-map.cc:186-381, calls hb_ot_layout_language_get_required_feature at line 205)
hop 4  hb_aat_layout_substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_feature_t const*, unsigned int)  (/src/harfbuzz/src/hb-aat-layout.cc:250-278, calls hb_ot_map_builder_t::compile(hb_ot_map_t&, hb_ot_shape_plan_key_t const&) at line 255)
hop 4  hb_ot_layout_collect_features  (/src/harfbuzz/src/hb-ot-layout.cc:1258-1280, calls hb-ot-layout.cc:script_collect_features(hb_collect_features_context_t*, OT::Script const&, unsigned int const*) at line 1265)
hop 4  hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&)  (/src/harfbuzz/src/hb-ot-shape.cc:103-213, calls hb_ot_map_builder_t::compile(hb_ot_map_t&, hb_ot_shape_plan_key_t const&) at line 106)
hop 5  hb_ot_layout_collect_lookups  (/src/harfbuzz/src/hb-ot-layout.cc:1310-1321, calls hb_ot_layout_collect_features at line 1314)
hop 5  hb-ot-shape.cc:hb_ot_substitute_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:904-919, calls hb_aat_layout_substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_feature_t const*, unsigned int) at line 914)
hop 5  hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:218-241, calls hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&) at line 228)
hop 6  hb_ot_face_t::init0(hb_face_t*)  (/src/harfbuzz/src/hb-ot-face.cc:47-52, calls hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*) at line 49)
hop 6  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934, calls hb-ot-shape.cc:hb_ot_substitute_plan(hb_ot_shape_context_t const*) at line 928)
hop 6  hb_shape_plan_create2  (/src/harfbuzz/src/hb-shape-plan.cc:228-275, calls hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*) at line 261)
hop 7  hb_face_create_for_tables  (/src/harfbuzz/src/hb-face.cc:121-140, calls hb_ot_face_t::init0(hb_face_t*) at line 136)
hop 7  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*) at line 1184)
hop 7  hb_shape_plan_create  (/src/harfbuzz/src/hb-shape-plan.cc:195-200, calls hb_shape_plan_create2 at line 196)
hop 7  hb_shape_plan_create_cached2  (/src/harfbuzz/src/hb-shape-plan.cc:521-578, calls hb_shape_plan_create2 at line 554)
hop 8  hb_face_create  (/src/harfbuzz/src/hb-face.cc:218-241, calls hb_face_create_for_tables at line 234)
hop 8  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)
hop 8  hb_shape_plan_create_cached  (/src/harfbuzz/src/hb-shape-plan.cc:487-492, calls hb_shape_plan_create_cached2 at line 488)
hop 8  hb_shape_full  (/src/harfbuzz/src/hb-shape.cc:130-171, calls hb_shape_plan_create_cached2 at line 143)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    7300         0  OT::LangSys::get_feature_index(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:972-972)
    6720         0  OT::RecordArrayOf<OT::LangSys>::get_tag(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:892-892)
    6720         0  OT::RecordArrayOf<OT::Script>::get_tag(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:892-892)
    6720         0  OT::RecordArrayOf<OT::Feature>::get_tag(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:892-892)
    6720         0  OT::RecordArrayOf<OT::JstfLangSys>::get_tag(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:892-892)
    6720         0  OT::RecordArrayOf<OT::JstfScript>::get_tag(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:892-892)
     383         0  OT::Record<OT::LangSys>::sanitize(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:870-874)
     383         0  OT::Record<OT::Script>::sanitize(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:870-874)
     383         0  OT::Record<OT::Feature>::sanitize(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:870-874)
     383         0  OT::Record<OT::JstfLangSys>::sanitize(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:870-874)
     383         0  OT::Record<OT::JstfScript>::sanitize(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:870-874)
     110       372  OT::RecordArrayOf<OT::LangSys>::find_index(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:907-909)
     110       372  OT::RecordArrayOf<OT::Script>::find_index(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:907-909)
     110       372  OT::RecordArrayOf<OT::Feature>::find_index(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:907-909)
     110       372  OT::RecordArrayOf<OT::JstfLangSys>::find_index(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:907-909)
... (46 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb_ot_layout_language_get_required_feature  (/src/harfbuzz/src/hb-ot-layout.cc:878-887) ---
  d=2   L 883  T=26 F=0  T=72 F=0  if (feature_index) *feature_index = index;
  d=2   L 884  T=26 F=0  T=72 F=0  if (feature_tag) *feature_tag = g.get_feature_tag (index);
--- d=1  OT::LangSys::get_required_feature_index() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:982-986) ---
  d=1   L 983  T=11 F=15  T=72 F=0  if (reqFeatureIndex == 0xFFFFu)  <-- BLOCKER

[off-chain: 105 additional divergent branches across 23 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=aa6f47881154f74f, size=186 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1641s, mutation_op=BytesExpandMutator,BitFlipMutator,DwordInterestingMutator,QwordAddMutator,WordAddMutator,BytesRandInsertMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 20 39 20 20 00 00 00 18 00 02 1f 08 00 00 39 20    9  ..........9 
  0020: 20 00 00 00 18 00 02 1f 08 00 00 00 20 00 80 04    ........... ...
  0030: ff ff ff ff 00 8d 5b 5b 5b 5b 5b 5b 5b 5b 5b 5b   ......[[[[[[[[[[
Seed 2 (id=3209219fbc11cc7c, size=86 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=12913s, mutation_op=ByteNegMutator):
  0000: 00 01 00 00 00 01 2f 1d 21 20 20 20 47 53 55 42   ....../.!   GSUB
  0010: 20 20 20 20 00 00 00 18 00 02 1f 08 00 00 08 00       ............
  0020: 00 08 00 00 08 00 80 02 20 00 00 00 00 1e 00 00   ........ .......
  0030: 02 00 ff ff 00 00 53 53 53 53 53 53 53 53 53 53   ......SSSSSSSSSS
Seed 3 (id=4ec0dd44afe30b8b, size=363 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=14893s, mutation_op=TokenInsert,BytesInsertCopyMutator,CrossoverInsertMutator,BytesCopyMutator,ByteInterestingMutator,TokenReplace,TokenReplace):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 53 55 42   ......      GSUB
  0010: 20 39 20 20 00 00 00 18 00 02 1f 08 00 00 39 20    9  ..........9 
  0020: 20 02 01 00 18 00 02 1f 08 01 01 00 e0 00 80 04    ...............
  0030: 20 02 00 00 18 00 02 1f 08 01 01 00 e0 00 80 04    ...............
Seed 4 (id=32f381bd655a37b8, size=255 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=20274s, mutation_op=BytesDeleteMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 21 03 1f 07 00 00 00 18 00 01 00 0a 00 02 00 05   !...............
  0020: 00 02 00 20 20 20 6d 20 01 0c 09 61 0d 00 c3 0a   ...   m ...a....
  0030: 01 00 00 20 04 00 8e 05 00 02 00 20 20 20 00 20   ... .......   . 
Seed 5 (id=41dcb27f1a0164d7, size=252 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=31008s, mutation_op=DwordAddMutator,BytesSetMutator,BytesSetMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 21 03 1f 07 00 00 00 18 00 01 00 0a 00 02 00 06   !...............
  0020: 00 02 00 20 20 20 6d 20 01 0c 09 61 0d 00 3d 0a   ...   m ...a..=.
  0030: 01 00 00 20 04 00 8e 05 00 02 00 20 20 20 00 20   ... .......   . 

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=003817559785f774, size=6 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteDecMutator,WordAddMutator):
  0000: 87 0e 0d 0e 22 0e                                 ....".
Seed 2 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 3 (id=002edec370c771cf, size=35 bytes, fuzzer=naive, trial=1, discovered_at=47s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteNegMutator,TokenInsert,ByteIncMutator,ByteRandMutator):
  0000: 00 00 00 00 00 00 00 00 00 00 00 00 20 00 64 6f   ............ .do
  0010: 2d 68 0a 6f 74 00 0e 00 20 00 0c 00 0c 09 00 00   -h.ot... .......
  0020: 00 0c 00                                          ...
Seed 4 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 5 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x7                             00(.)x4 e0(.)x2 05(.)x2 87(.)x1 +11u  PARTIAL
   0x0001  01(.)x7                             00(.)x3 0e(.)x2 ff(.)x2 07(.)x2 +11u  PARTIAL
   0x0002  00(.)x7                             00(.)x10 ff(.)x3 0d(.)x1 0e(.)x1 +5u  PARTIAL
   0x0003  00(.)x7                             00(.)x11 ff(.)x2 2d(-)x2 0e(.)x1 +4u  PARTIAL
   0x0004  00(.)x7                             00(.)x2 df(.)x2 68(h)x2 70(p)x2 +12u  PARTIAL
   0x0005  01(.)x6 0c(.)x1                     00(.)x4 20( )x4 0e(.)x3 06(.)x2 +7u  PARTIAL
   0x0006  20( )x6 2f(/)x1                     00(.)x12 e0(.)x1 68(h)x1 e5(.)x1 +4u  DIFFER
   0x0007  20( )x6 1d(.)x1                     00(.)x11 e0(.)x1 55(U)x1 77(w)x1 +5u  DIFFER
   0x0008  20( )x5 21(!)x1 07(.)x1             00(.)x4 20( )x2 29())x1 e0(.)x1 +11u  PARTIAL
   0x0009  20( )x6 04(.)x1                     00(.)x3 0a(.)x2 2b(+)x1 17(.)x1 +12u  PARTIAL
   0x000a  20( )x6 06(.)x1                     00(.)x9 01(.)x2 29())x1 aa(.)x1 +6u  DIFFER
   0x000b  20( )x6 00(.)x1                     00(.)x12 29())x1 13(.)x1 75(u)x1 +4u  PARTIAL
   0x000c  47(G)x6 00(.)x1                     00(.)x3 01(.)x2 20( )x2 2c(,)x1 +11u  PARTIAL
   0x000d  50(P)x4 53(S)x2 20( )x1             20( )x4 00(.)x4 18(.)x1 17(.)x1 +8u  PARTIAL
   0x000e  4f(O)x4 55(U)x2 20( )x1             00(.)x5 e0(.)x1 64(d)x1 18(.)x1 +10u  PARTIAL
   0x000f  53(S)x4 42(B)x2 7f(.)x1             00(.)x5 6a(j)x1 6f(o)x1 fa(.)x1 +10u  DIFFER
   0x0010  20( )x3 21(!)x3 fe(.)x1             00(.)x5 20( )x2 79(y)x1 2d(-)x1 +9u  PARTIAL
   0x0011  03(.)x3 39(9)x2 20( )x1 b9(.)x1     20( )x4 00(.)x2 06(.)x2 2d(-)x1 +9u  PARTIAL
   0x0012  20( )x3 1f(.)x3 b9(.)x1             00(.)x8 68(h)x1 0a(.)x1 18(.)x1 +7u  PARTIAL
   0x0013  20( )x3 07(.)x3 b9(.)x1             00(.)x6 2d(-)x2 20( )x2 61(a)x1 +7u  PARTIAL
   0x0014  00(.)x6 b9(.)x1                     68(h)x3 00(.)x2 6e(n)x1 74(t)x1 +11u  PARTIAL
   0x0015  00(.)x6 b9(.)x1                     00(.)x4 06(.)x2 74(t)x1 17(.)x1 +10u  PARTIAL
   0x0016  00(.)x7                             00(.)x8 01(.)x2 2d(-)x1 0e(.)x1 +6u  PARTIAL
   0x0017  18(.)x6 66(f)x1                     00(.)x7 74(t)x2 68(h)x1 3d(=)x1 +6u  DIFFER
   0x0018  00(.)x6 20( )x1                     20( )x4 00(.)x3 6b(k)x1 61(a)x1 +8u  PARTIAL
   0x0019  02(.)x3 01(.)x3 20( )x1             00(.)x3 20( )x3 9f(.)x2 19(.)x2 +7u  PARTIAL
   0x001a  1f(.)x3 00(.)x3 3c(<)x1             00(.)x5 20( )x2 9f(.)x2 0c(.)x1 +7u  PARTIAL
   0x001b  08(.)x3 0a(.)x3 62(b)x1             00(.)x8 20( )x2 ff(.)x2 3d(=)x1 +3u  DIFFER
   0x001c  00(.)x6 47(G)x1                     00(.)x6 0c(.)x1 3d(=)x1 4c(L)x1 +7u  PARTIAL
   0x001d  00(.)x3 02(.)x3 53(S)x1             00(.)x3 20( )x2 09(.)x1 3d(=)x1 +9u  PARTIAL
   0x001e  00(.)x3 39(9)x2 08(.)x1 55(U)x1     00(.)x8 ff(.)x2 01(.)x2 80(.)x1 +3u  PARTIAL
   0x0020  00(.)x4 20( )x2 f7(.)x1             00(.)x4 df(.)x1 c8(.)x1 37(7)x1 +8u  PARTIAL
   0x0021  02(.)x4 00(.)x1 08(.)x1 0a(.)x1     00(.)x3 20( )x2 0e(.)x2 07(.)x1 +7u  PARTIAL
   0x0022  00(.)x5 01(.)x1 03(.)x1             00(.)x8 01(.)x2 02(.)x1 1b(.)x1 +2u  PARTIAL
   0x0023  00(.)x4 20( )x3                     00(.)x7 02(.)x1 6d(m)x1 6c(l)x1 +3u  PARTIAL
   0x0024  20( )x3 18(.)x2 08(.)x1 00(.)x1     00(.)x4 01(.)x1 02(.)x1 40(@)x1 +6u  PARTIAL
   0x0025  00(.)x4 20( )x3                     00(.)x5 20( )x1 02(.)x1 62(b)x1 +5u  PARTIAL
   0x0026  6d(m)x3 02(.)x2 80(.)x1 00(.)x1     00(.)x2 01(.)x2 20( )x1 02(.)x1 +7u  PARTIAL
   0x0027  20( )x3 1f(.)x2 02(.)x1 00(.)x1     20( )x4 02(.)x1 6d(m)x1 9f(.)x1 +6u  PARTIAL
   0x0028  01(.)x3 08(.)x2 20( )x1 00(.)x1     00(.)x4 01(.)x1 20( )x1 02(.)x1 +6u  PARTIAL
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
  prompts_b/harfbuzz_5478.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5478,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5478 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5478 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5478 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).