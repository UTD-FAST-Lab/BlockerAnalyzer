==== BLOCKER ====
Target: harfbuzz
Branch ID: 5565
Location: /src/harfbuzz/src/hb-ot-layout.cc:1001:28
Enclosing function: hb_ot_layout_language_find_feature
Source line:   for (unsigned int i = 0; i < num_features; i++) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=5.30h  loser=24.00h
  avg hitcount on branch: winner=76930  loser=0
  prob_div=1.00  dur_div=18.70h  hit_div=76930
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.70h  loser=24.00h
  avg hitcount on branch: winner=11528  loser=0
  prob_div=1.00  dur_div=20.30h  hit_div=11528
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5565/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_ot_layout_language_find_feature (/src/harfbuzz/src/hb-ot-layout.cc:995-1012) ---
[ ]   993  				    hb_tag_t      feature_tag,
[ ]   994  				    unsigned int *feature_index /* OUT */)
[B]   995  {
[B]   996    static_assert ((OT::Index::NOT_FOUND_INDEX == HB_OT_LAYOUT_NO_FEATURE_INDEX), "");
[B]   997    const OT::GSUBGPOS &g = get_gsubgpos_table (face, table_tag);
[B]   998    const OT::LangSys &l = g.get_script (script_index).get_lang_sys (language_index);
[ ]   999  
[B]  1000    unsigned int num_features = l.get_feature_count ();
[B]  1001    for (unsigned int i = 0; i < num_features; i++) { <-- BLOCKER
[W]  1002      unsigned int f_index = l.get_feature_index (i);
[ ]  1003  
[W]  1004      if (feature_tag == g.get_feature_tag (f_index)) {
[ ]  1005        if (feature_index) *feature_index = f_index;
[ ]  1006        return true;
[ ]  1007      }
[W]  1008    }
[ ]  1009  
[B]  1010    if (feature_index) *feature_index = HB_OT_LAYOUT_NO_FEATURE_INDEX;
[B]  1011    return false;
[B]  1012  }

--- Caller (1 hop): hb_ot_map_builder_t::compile(hb_ot_map_t&, hb_ot_shape_plan_key_t const&) (/src/harfbuzz/src/hb-ot-map.cc:186-381, calls hb_ot_layout_language_find_feature at line 271) (±10 around call site) ---
[L]   261        continue; /* Feature disabled, or not enough bits. */
[ ]   262  
[ ]   263  
[B]   264      bool found = false;
[B]   265      unsigned int feature_index[2];
[B]   266      for (unsigned int table_index = 0; table_index < 2; table_index++)
[B]   267      {
[B]   268        if (required_feature_tag[table_index] == info->tag)
[ ]   269  	required_feature_stage[table_index] = info->stage[table_index];
[ ]   270  
[B]   271        found |= (bool) hb_ot_layout_language_find_feature (face, <-- CALL
[B]   272  							  table_tags[table_index],
[B]   273  							  script_index[table_index],
[B]   274  							  language_index[table_index],
[B]   275  							  info->tag,
[B]   276  							  &feature_index[table_index]);
[B]   277      }
[B]   278      if (!found && (info->flags & F_GLOBAL_SEARCH))
[ ]   279      {
[ ]   280        for (unsigned int table_index = 0; table_index < 2; table_index++)
[ ]   281        {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb_ot_map_builder_t::compile(hb_ot_map_t&, hb_ot_shape_plan_key_t const&)  (/src/harfbuzz/src/hb-ot-map.cc:186-381, calls hb_ot_layout_language_find_feature at line 271)
hop 2  hb_ot_map_builder_t::has_feature(unsigned int)  (/src/harfbuzz/src/hb-ot-map.cc:113-125, calls hb_ot_layout_language_find_feature at line 116)
hop 3  hb_aat_layout_substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_feature_t const*, unsigned int)  (/src/harfbuzz/src/hb-aat-layout.cc:250-278, calls hb_ot_map_builder_t::compile(hb_ot_map_t&, hb_ot_shape_plan_key_t const&) at line 255)
hop 3  hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&)  (/src/harfbuzz/src/hb-ot-shape.cc:103-213, calls hb_ot_map_builder_t::compile(hb_ot_map_t&, hb_ot_shape_plan_key_t const&) at line 106)
hop 3  hb-ot-shaper-arabic.cc:collect_features_arabic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-arabic.cc:185-254, calls hb_ot_map_builder_t::has_feature(unsigned int) at line 235)
hop 4  hb-ot-shape.cc:hb_ot_substitute_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:904-919, calls hb_aat_layout_substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_feature_t const*, unsigned int) at line 914)
hop 4  hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:218-241, calls hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&) at line 228)
hop 5  hb_ot_face_t::init0(hb_face_t*)  (/src/harfbuzz/src/hb-ot-face.cc:47-52, calls hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*) at line 49)
hop 5  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934, calls hb-ot-shape.cc:hb_ot_substitute_plan(hb_ot_shape_context_t const*) at line 928)
hop 5  hb_shape_plan_create2  (/src/harfbuzz/src/hb-shape-plan.cc:228-275, calls hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*) at line 261)
hop 6  hb_face_create_for_tables  (/src/harfbuzz/src/hb-face.cc:121-140, calls hb_ot_face_t::init0(hb_face_t*) at line 136)
hop 6  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*) at line 1184)
hop 6  hb_shape_plan_create  (/src/harfbuzz/src/hb-shape-plan.cc:195-200, calls hb_shape_plan_create2 at line 196)
hop 6  hb_shape_plan_create_cached2  (/src/harfbuzz/src/hb-shape-plan.cc:521-578, calls hb_shape_plan_create2 at line 554)
hop 7  hb_face_create  (/src/harfbuzz/src/hb-face.cc:218-241, calls hb_face_create_for_tables at line 234)
hop 7  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)
hop 7  hb_shape_plan_create_cached  (/src/harfbuzz/src/hb-shape-plan.cc:487-492, calls hb_shape_plan_create_cached2 at line 488)
hop 7  hb_shape_full  (/src/harfbuzz/src/hb-shape.cc:130-171, calls hb_shape_plan_create_cached2 at line 143)
hop 8  hb-buffer-verify.cc:buffer_verify_unsafe_to_break(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:94-203, calls hb_shape_full at line 165)
hop 8  hb-buffer-verify.cc:buffer_verify_unsafe_to_concat(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:212-401, calls hb_shape_full at line 319)
hop 8  hb_ot_shape_glyphs_closure  (/src/harfbuzz/src/hb-ot-shape.cc:1272-1291, calls hb_shape_plan_create_cached at line 1274)
hop 8  LLVMFuzzerTestOneInput  (/src/harfbuzz/test/fuzzing/hb-shape-fuzzer.cc:13-64, calls hb_face_create at line 18)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1100      3640  hb-ot-layout.cc:get_gsubgpos_table(hb_face_t*, unsigned int)  (/src/harfbuzz/src/hb-ot-layout.cc:416-422)
     674      2180  hb_ot_layout_language_find_feature  (/src/harfbuzz/src/hb-ot-layout.cc:995-1012)  <-- enclosing
     340      1150  hb_ot_map_builder_t::add_feature(unsigned int, hb_ot_map_feature_flags_t, unsigned int)  (/src/harfbuzz/src/hb-ot-map.cc:100-110)
     236       834  hb_ot_layout_table_find_feature_variations  (/src/harfbuzz/src/hb-ot-layout.cc:1399-1403)
     106       381  hb-ot-layout.cc:_hb_ot_layout_set_glyph_props(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:255-265)
     106       381  hb_ot_layout_substitute_start(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1510-1512)
     106       381  hb_ot_layout_position_start(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1611-1613)
     106       381  hb_ot_layout_position_finish_advances(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1626-1628)
     106       381  hb_ot_layout_position_finish_offsets(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1640-1642)
     106       381  GSUBProxy::GSUBProxy(hb_face_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1833-1834)
     106       381  hb_ot_map_t::substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:2001-2008)
      56       236  hb_ot_map_builder_t::add_pause(unsigned int, bool (*)(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*))  (/src/harfbuzz/src/hb-ot-map.cc:175-181)
      57       176  hb_ot_layout_table_get_lookup_count  (/src/harfbuzz/src/hb-ot-layout.cc:1066-1068)
      57       176  hb_ot_layout_feature_with_variations_get_lookups  (/src/harfbuzz/src/hb-ot-layout.cc:1434-1441)
      57       176  hb_ot_map_builder_t::add_lookups(hb_ot_map_t&, unsigned int, unsigned int, unsigned int, unsigned int, bool, bool, bool, bool, unsigned int)  (/src/harfbuzz/src/hb-ot-map.cc:138-171)
... (24 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb_ot_map_builder_t::has_feature(unsigned int)  (/src/harfbuzz/src/hb-ot-map.cc:113-125) ---
  d=2   L 114  T=0 F=0  T=10 F=5  for (unsigned int table_index = 0; table_index < 2; table...
  d=2   L 116  T=0 F=0  T=0 F=10  if (hb_ot_layout_language_find_feature (face,
--- d=2  hb_ot_map_builder_t::compile(hb_ot_map_t&, hb_ot_shape_plan_key_t const&)  (/src/harfbuzz/src/hb-ot-map.cc:186-381) ---
  d=2   L 200  T=22 F=11  T=72 F=36  for (unsigned int table_index = 0; table_index < 2; table...
  d=2   L 214  T=11 F=0  T=36 F=0  if (feature_infos.length)
  d=2   L 220  T=329 F=11  T=1100 F=36  for (unsigned int i = 1; i < count; i++)
  d=2   L 221  T=323 F=6  T=1040 F=60  if (f[i].tag != f[j].tag)
  d=2   L 224  T=6 F=0  T=60 F=0  if (f[i].flags & F_GLOBAL) {
  d=2   L 247  T=334 F=11  T=1080 F=36  for (unsigned int i = 0; i < count; i++)
  d=2   L 253  T=279 F=11  T=842 F=42  if ((info->flags & F_GLOBAL) && info->max_value == 1)
  d=2   L 253  T=290 F=44  T=884 F=197  if ((info->flags & F_GLOBAL) && info->max_value == 1)
  d=2   L 260  T=0 F=334  T=0 F=1070  if (!info->max_value || next_bit + bits_needed >= global_...
  d=2   L 260  T=0 F=334  T=6 F=1070  if (!info->max_value || next_bit + bits_needed >= global_...
  d=2   L 266  T=668 F=334  T=2150 F=1070  for (unsigned int table_index = 0; table_index < 2; table...
  d=2   L 268  T=0 F=668  T=0 F=2150  if (required_feature_tag[table_index] == info->tag)
  d=2   L 278  T=0 F=334  T=0 F=1070  if (!found && (info->flags & F_GLOBAL_SEARCH))
  d=2   L 278  T=334 F=0  T=1070 F=0  if (!found && (info->flags & F_GLOBAL_SEARCH))
  d=2   L 288  T=334 F=0  T=1070 F=0  if (!found && !(info->flags & F_HAS_FALLBACK))
  d=2   L 288  T=312 F=22  T=987 F=88  if (!found && !(info->flags & F_HAS_FALLBACK))
  d=2   L 303  T=22 F=0  T=76 F=12  if ((info->flags & F_GLOBAL) && info->max_value == 1) {
  d=2   L 303  T=22 F=0  T=76 F=0  if ((info->flags & F_GLOBAL) && info->max_value == 1) {
  d=2   L 322  T=22 F=11  T=72 F=36  for (unsigned int table_index = 0; table_index < 2; table...
  d=2   L 329  T=56 F=22  T=236 F=72  for (unsigned stage = 0; stage < current_stage[table_inde...
  d=2   L 331  T=18 F=38  T=0 F=236  if (required_feature_index[table_index] != HB_OT_LAYOUT_N...
  d=2   L 332  T=13 F=5  T=0 F=0  required_feature_stage[table_index] == stage)
  d=2   L 338  T=112 F=56  T=722 F=236  for (auto &feature : m.features)
  d=2   L 340  T=44 F=68  T=176 F=546  if (feature.stage[table_index] == stage)
  d=2   L 353  T=0 F=56  T=0 F=236  if (last_num_lookups < lookups.length)
  d=2   L 372  T=52 F=0  T=235 F=0  if (stage_index < stages[table_index].length && stages[ta...
  d=2   L 372  T=52 F=4  T=235 F=1  if (stage_index < stages[table_index].length && stages[ta...
--- d=1  hb_ot_layout_language_find_feature  (/src/harfbuzz/src/hb-ot-layout.cc:995-1012) ---
  d=1   L1001  T=7300 F=674  T=0 F=2180  for (unsigned int i = 0; i < num_features; i++) {  <-- BLOCKER
  d=1   L1004  T=0 F=7300  T=0 F=0  if (feature_tag == g.get_feature_tag (f_index)) {
  d=1   L1010  T=674 F=0  T=2170 F=10  if (feature_index) *feature_index = HB_OT_LAYOUT_NO_FEATU...

[off-chain: 82 additional divergent branches across 16 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=3209219fbc11cc7c, size=86 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=12913s, mutation_op=ByteNegMutator):
  0000: 00 01 00 00 00 01 2f 1d 21 20 20 20 47 53 55 42   ....../.!   GSUB
  0010: 20 20 20 20 00 00 00 18 00 02 1f 08 00 00 08 00       ............
  0020: 00 08 00 00 08 00 80 02 20 00 00 00 00 1e 00 00   ........ .......
  0030: 02 00 ff ff 00 00 53 53 53 53 53 53 53 53 53 53   ......SSSSSSSSSS
Seed 2 (id=4ec0dd44afe30b8b, size=363 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=14893s, mutation_op=TokenInsert,BytesInsertCopyMutator,CrossoverInsertMutator,BytesCopyMutator,ByteInterestingMutator,TokenReplace,TokenReplace):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 53 55 42   ......      GSUB
  0010: 20 39 20 20 00 00 00 18 00 02 1f 08 00 00 39 20    9  ..........9 
  0020: 20 02 01 00 18 00 02 1f 08 01 01 00 e0 00 80 04    ...............
  0030: 20 02 00 00 18 00 02 1f 08 01 01 00 e0 00 80 04    ...............
Seed 3 (id=32f381bd655a37b8, size=255 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=20274s, mutation_op=BytesDeleteMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 21 03 1f 07 00 00 00 18 00 01 00 0a 00 02 00 05   !...............
  0020: 00 02 00 20 20 20 6d 20 01 0c 09 61 0d 00 c3 0a   ...   m ...a....
  0030: 01 00 00 20 04 00 8e 05 00 02 00 20 20 20 00 20   ... .......   . 
Seed 4 (id=41dcb27f1a0164d7, size=252 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=31008s, mutation_op=DwordAddMutator,BytesSetMutator,BytesSetMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 21 03 1f 07 00 00 00 18 00 01 00 0a 00 02 00 06   !...............
  0020: 00 02 00 20 20 20 6d 20 01 0c 09 61 0d 00 3d 0a   ...   m ...a..=.
  0030: 01 00 00 20 04 00 8e 05 00 02 00 20 20 20 00 20   ... .......   . 
Seed 5 (id=04fa76806a500a81, size=298 bytes, fuzzer=cmplog, trial=1, discovered_at=60932s, mutation_op=BytesCopyMutator,BytesInsertMutator):
  0000: 00 01 00 00 00 0c 20 20 07 04 06 00 00 20 20 7f   ......  .....  .
  0010: fe b9 b9 b9 b9 b9 00 66 20 20 3c 62 47 53 55 42   .......f  <bGSUB
  0020: f7 0a 03 00 00 00 00 00 00 01 6b 6b 6b 6b 6b 6b   ..........kkkkkk
  0030: 6b 6b 6b 6b 6b 6b 6b 6b 00 20 20 20 18 18 18 18   kkkkkkkk.   ....

==== Loser-blocking seeds (take false branch) ====
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
   0x0000  00(.)x6                             00(.)x4 e0(.)x2 05(.)x2 87(.)x1 +11u  PARTIAL
   0x0001  01(.)x6                             00(.)x3 0e(.)x2 ff(.)x2 07(.)x2 +11u  PARTIAL
   0x0002  00(.)x6                             00(.)x10 ff(.)x3 0d(.)x1 0e(.)x1 +5u  PARTIAL
   0x0003  00(.)x6                             00(.)x11 ff(.)x2 2d(-)x2 0e(.)x1 +4u  PARTIAL
   0x0004  00(.)x6                             00(.)x2 df(.)x2 68(h)x2 70(p)x2 +12u  PARTIAL
   0x0005  01(.)x5 0c(.)x1                     00(.)x4 20( )x4 0e(.)x3 06(.)x2 +7u  PARTIAL
   0x0006  20( )x5 2f(/)x1                     00(.)x12 e0(.)x1 68(h)x1 e5(.)x1 +4u  DIFFER
   0x0007  20( )x5 1d(.)x1                     00(.)x11 e0(.)x1 55(U)x1 77(w)x1 +5u  DIFFER
   0x0008  20( )x4 21(!)x1 07(.)x1             00(.)x4 20( )x2 29())x1 e0(.)x1 +11u  PARTIAL
   0x0009  20( )x5 04(.)x1                     00(.)x3 0a(.)x2 2b(+)x1 17(.)x1 +12u  PARTIAL
   0x000a  20( )x5 06(.)x1                     00(.)x9 01(.)x2 29())x1 aa(.)x1 +6u  DIFFER
   0x000b  20( )x5 00(.)x1                     00(.)x12 29())x1 13(.)x1 75(u)x1 +4u  PARTIAL
   0x000c  47(G)x5 00(.)x1                     00(.)x3 01(.)x2 20( )x2 2c(,)x1 +11u  PARTIAL
   0x000d  50(P)x3 53(S)x2 20( )x1             20( )x4 00(.)x4 18(.)x1 17(.)x1 +8u  PARTIAL
   0x000e  4f(O)x3 55(U)x2 20( )x1             00(.)x5 e0(.)x1 64(d)x1 18(.)x1 +10u  PARTIAL
   0x000f  53(S)x3 42(B)x2 7f(.)x1             00(.)x5 6a(j)x1 6f(o)x1 fa(.)x1 +10u  DIFFER
   0x0010  21(!)x3 20( )x2 fe(.)x1             00(.)x5 20( )x2 79(y)x1 2d(-)x1 +9u  PARTIAL
   0x0011  03(.)x3 20( )x1 39(9)x1 b9(.)x1     20( )x4 00(.)x2 06(.)x2 2d(-)x1 +9u  PARTIAL
   0x0012  1f(.)x3 20( )x2 b9(.)x1             00(.)x8 68(h)x1 0a(.)x1 18(.)x1 +7u  PARTIAL
   0x0013  07(.)x3 20( )x2 b9(.)x1             00(.)x6 2d(-)x2 20( )x2 61(a)x1 +7u  PARTIAL
   0x0014  00(.)x5 b9(.)x1                     68(h)x3 00(.)x2 6e(n)x1 74(t)x1 +11u  PARTIAL
   0x0015  00(.)x5 b9(.)x1                     00(.)x4 06(.)x2 74(t)x1 17(.)x1 +10u  PARTIAL
   0x0016  00(.)x6                             00(.)x8 01(.)x2 2d(-)x1 0e(.)x1 +6u  PARTIAL
   0x0017  18(.)x5 66(f)x1                     00(.)x7 74(t)x2 68(h)x1 3d(=)x1 +6u  DIFFER
   0x0018  00(.)x5 20( )x1                     20( )x4 00(.)x3 6b(k)x1 61(a)x1 +8u  PARTIAL
   0x0019  01(.)x3 02(.)x2 20( )x1             00(.)x3 20( )x3 9f(.)x2 19(.)x2 +7u  PARTIAL
   0x001a  00(.)x3 1f(.)x2 3c(<)x1             00(.)x5 20( )x2 9f(.)x2 0c(.)x1 +7u  PARTIAL
   0x001b  0a(.)x3 08(.)x2 62(b)x1             00(.)x8 20( )x2 ff(.)x2 3d(=)x1 +3u  DIFFER
   0x001c  00(.)x5 47(G)x1                     00(.)x6 0c(.)x1 3d(=)x1 4c(L)x1 +7u  PARTIAL
   0x001d  02(.)x3 00(.)x2 53(S)x1             00(.)x3 20( )x2 09(.)x1 3d(=)x1 +9u  PARTIAL
   0x001e  00(.)x3 08(.)x1 39(9)x1 55(U)x1     00(.)x8 ff(.)x2 01(.)x2 80(.)x1 +3u  PARTIAL
   0x0020  00(.)x4 20( )x1 f7(.)x1             00(.)x4 df(.)x1 c8(.)x1 37(7)x1 +8u  PARTIAL
   0x0021  02(.)x4 08(.)x1 0a(.)x1             00(.)x3 20( )x2 0e(.)x2 07(.)x1 +7u  PARTIAL
   0x0022  00(.)x4 01(.)x1 03(.)x1             00(.)x8 01(.)x2 02(.)x1 1b(.)x1 +2u  PARTIAL
   0x0023  00(.)x3 20( )x3                     00(.)x7 02(.)x1 6d(m)x1 6c(l)x1 +3u  PARTIAL
   0x0024  20( )x3 08(.)x1 18(.)x1 00(.)x1     00(.)x4 01(.)x1 02(.)x1 40(@)x1 +6u  PARTIAL
   0x0025  00(.)x3 20( )x3                     00(.)x5 20( )x1 02(.)x1 62(b)x1 +5u  PARTIAL
   0x0026  6d(m)x3 80(.)x1 02(.)x1 00(.)x1     00(.)x2 01(.)x2 20( )x1 02(.)x1 +7u  PARTIAL
   0x0027  20( )x3 02(.)x1 1f(.)x1 00(.)x1     20( )x4 02(.)x1 6d(m)x1 9f(.)x1 +6u  PARTIAL
   0x0028  01(.)x3 20( )x1 08(.)x1 00(.)x1     00(.)x4 01(.)x1 20( )x1 02(.)x1 +6u  PARTIAL
   ... (22 more divergent offsets)
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
  prompts_b/harfbuzz_5565.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5565,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5565 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5565 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5565 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).