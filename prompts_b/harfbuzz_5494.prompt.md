==== BLOCKER ====
Target: harfbuzz
Branch ID: 5494
Location: /src/harfbuzz/src/hb-ot-layout-common.hh:3579:13
Enclosing function: OT::Device::get_y_delta(hb_font_t*, OT::VariationStore const&, float*) const
Source line:     case 1: case 2: case 3:
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
  avg duration blocked: winner=2.30h  loser=24.00h
  avg hitcount on branch: winner=21  loser=0
  prob_div=1.00  dur_div=21.70h  hit_div=21
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5494/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::Device::get_y_delta(hb_font_t*, OT::VariationStore const&, float*) const (/src/harfbuzz/src/hb-ot-layout-common.hh:3576-3590) ---
[ ]  3574  			     const VariationStore &store=Null (VariationStore),
[ ]  3575  			     VariationStore::cache_t *store_cache = nullptr) const
[B]  3576    {
[B]  3577      switch (u.b.format)
[B]  3578      {
[W]  3579      case 1: case 2: case 3: <-- BLOCKER
[W]  3580  #ifndef HB_NO_HINTING
[W]  3581        return u.hinting.get_y_delta (font);
[ ]  3582  #endif
[ ]  3583  #ifndef HB_NO_VAR
[ ]  3584      case 0x8000:
[ ]  3585        return u.variation.get_y_delta (font, store, store_cache);
[ ]  3586  #endif
[B]  3587      default:
[B]  3588        return 0;
[B]  3589      }
[B]  3590    }

--- Caller (1 hop): OT::MathValueRecord::get_y_value(hb_font_t*, void const*) const (/src/harfbuzz/src/hb-ot-math-table.hh:42-42, calls OT::Device::get_y_delta(hb_font_t*, OT::VariationStore const&, float*) const at line 42) (full body — short) ---
[B]    42    { return font->em_scale_y (value) + (base+deviceTable).get_y_delta (font); } <-- CALL

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::BaseCoordFormat3::get_coord(hb_font_t*, OT::VariationStore const&, hb_direction_t) const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:91-97, calls OT::Device::get_y_delta(hb_font_t*, OT::VariationStore const&, float*) const at line 95)
hop 2  OT::MathValueRecord::get_y_value(hb_font_t*, void const*) const  (/src/harfbuzz/src/hb-ot-math-table.hh:42-42, calls OT::Device::get_y_delta(hb_font_t*, OT::VariationStore const&, float*) const at line 42)
hop 3  OT::BaseCoord::get_coord(hb_font_t*, OT::VariationStore const&, hb_direction_t) const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:125-132, calls OT::BaseCoordFormat3::get_coord(hb_font_t*, OT::VariationStore const&, hb_direction_t) const at line 127)
hop 3  OT::MathConstants::get_value(hb_ot_math_constant_t, hb_font_t*) const  (/src/harfbuzz/src/hb-ot-math-table.hh:115-187, calls OT::MathValueRecord::get_y_value(hb_font_t*, void const*) const at line 179)
hop 3  OT::MathKern::get_value(int, hb_font_t*) const  (/src/harfbuzz/src/hb-ot-math-table.hh:343-370, calls OT::MathValueRecord::get_y_value(hb_font_t*, void const*) const at line 361)
hop 4  OT::BASE::get_baseline(hb_font_t*, unsigned int, hb_direction_t, unsigned int, unsigned int, int*) const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:464-474, calls OT::BaseCoord::get_coord(hb_font_t*, OT::VariationStore const&, hb_direction_t) const at line 471)
hop 4  OT::BASE::get_min_max(hb_font_t*, hb_direction_t, unsigned int, unsigned int, unsigned int, int*, int*)  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:484-494, calls OT::BaseCoord::get_coord(hb_font_t*, OT::VariationStore const&, hb_direction_t) const at line 491)
hop 4  OT::AxisValueFormat1::get_value() const  (/src/harfbuzz/src/hb-ot-stat-table.hh:88-88, calls OT::MathConstants::get_value(hb_ot_math_constant_t, hb_font_t*) const at line 88)
hop 4  OT::AxisValueFormat1::keep_axis_value(hb_array_t<OT::StatAxisRecord const>, hb_hashmap_t<unsigned int, float, false> const*) const  (/src/harfbuzz/src/hb-ot-stat-table.hh:100-109, calls OT::MathConstants::get_value(hb_ot_math_constant_t, hb_font_t*) const at line 102)
hop 5  OT::BaseLangSysRecord::get_min_max() const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:271-271, calls OT::BASE::get_min_max(hb_font_t*, hb_direction_t, unsigned int, unsigned int, unsigned int, int*, int*) at line 271)
hop 5  OT::MinMax::get_min_max(unsigned int, OT::BaseCoord const**, OT::BaseCoord const**) const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:198-207, calls OT::BASE::get_min_max(hb_font_t*, hb_direction_t, unsigned int, unsigned int, unsigned int, int*, int*) at line 201)
hop 5  hb_ot_layout_get_baseline  (/src/harfbuzz/src/hb-ot-layout.cc:2122-2124, calls OT::BASE::get_baseline(hb_font_t*, unsigned int, hb_direction_t, unsigned int, unsigned int, int*) const at line 2123)
hop 5  OT::AxisValueFormat1::subset(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const>) const  (/src/harfbuzz/src/hb-ot-stat-table.hh:113-121, calls OT::AxisValueFormat1::keep_axis_value(hb_array_t<OT::StatAxisRecord const>, hb_hashmap_t<unsigned int, float, false> const*) const at line 117)
hop 5  OT::AxisValueFormat2::get_value() const  (/src/harfbuzz/src/hb-ot-stat-table.hh:147-147, calls OT::AxisValueFormat1::get_value() const at line 147)
hop 5  OT::AxisValueFormat2::subset(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const>) const  (/src/harfbuzz/src/hb-ot-stat-table.hh:172-180, calls OT::AxisValueFormat1::keep_axis_value(hb_array_t<OT::StatAxisRecord const>, hb_hashmap_t<unsigned int, float, false> const*) const at line 176)
hop 6  OT::cff2::subset(hb_subset_context_t*) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:526-526, calls OT::AxisValueFormat1::subset(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const>) const at line 526)
hop 6  OT::BaseScript::get_min_max(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:292-295, calls OT::MinMax::get_min_max(unsigned int, OT::BaseCoord const**, OT::BaseCoord const**) const at line 294)
hop 6  hb_ot_layout_get_baseline_with_fallback  (/src/harfbuzz/src/hb-ot-layout.cc:2147-2346, calls hb_ot_layout_get_baseline at line 2148)
hop 6  OT::HVAR::subset(hb_subset_context_t*) const  (/src/harfbuzz/src/hb-ot-var-hvar-table.hh:360-360, calls OT::AxisValueFormat1::subset(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const>) const at line 360)
hop 7  OT::VVAR::subset(hb_subset_context_t*) const  (/src/harfbuzz/src/hb-ot-var-hvar-table.hh:392-392, calls OT::cff2::subset(hb_subset_context_t*) const at line 392)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     128      1300  OT::RecordArrayOf<OT::Script>::get_offset(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:888-888)
     128      1300  OT::RecordArrayOf<OT::Feature>::get_offset(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:888-888)
     128      1300  OT::RecordListOf<OT::Script>::operator[](unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:916-916)
     128      1300  OT::RecordListOf<OT::Feature>::operator[](unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:916-916)
     112      1160  OT::Script::get_lang_sys(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1090-1093)
     110      1150  OT::Script::get_default_lang_sys() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1098-1098)
     106      1110  OT::LangSys::get_feature_count() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:970-970)
     112       560  OT::MathConstants::get_value(hb_ot_math_constant_t, hb_font_t*) const  (/src/harfbuzz/src/hb-ot-math-table.hh:115-187)
     112       560  OT::MATH::get_constant(hb_ot_math_constant_t, hb_font_t*) const  (/src/harfbuzz/src/hb-ot-math-table.hh:1116-1116)
     108       540  OT::GDEF::get_glyph_class_def() const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:688-696)
     108       540  OT::GDEF::get_glyph_class(unsigned int) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:801-801)
     108       540  OT::GDEF::get_glyph_props(unsigned int) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:831-846)
     108       540  OT::ClassDef::get_class(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1994-2004)
      94       470  OT::Device::get_y_delta(hb_font_t*, OT::VariationStore const&, float*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:3576-3590)  <-- enclosing
      94       470  OT::MathValueRecord::get_y_value(hb_font_t*, void const*) const  (/src/harfbuzz/src/hb-ot-math-table.hh:42-42)
... (65 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  OT::MathConstants::get_value(hb_ot_math_constant_t, hb_font_t*) const  (/src/harfbuzz/src/hb-ot-math-table.hh:115-187) ---
  d=3   L 118  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SCRIPT_PERCENT_SCALE_DOWN:
  d=3   L 119  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SCRIPT_SCRIPT_PERCENT_SCALE_DOWN:
  d=3   L 122  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_DELIMITED_SUB_FORMULA_MIN_HEIGHT:
  d=3   L 123  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_DISPLAY_OPERATOR_MIN_HEIGHT:
  d=3   L 126  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_RADICAL_KERN_AFTER_DEGREE:
  d=3   L 127  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_RADICAL_KERN_BEFORE_DEGREE:
  d=3   L 128  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SKEWED_FRACTION_HORIZONTAL_GAP:
  d=3   L 129  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SPACE_AFTER_SCRIPT:
  d=3   L 132  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_ACCENT_BASE_HEIGHT:
  d=3   L 133  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_AXIS_HEIGHT:
  d=3   L 134  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FLATTENED_ACCENT_BASE_HEIGHT:
  d=3   L 135  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FRACTION_DENOMINATOR_DISPLAY_STY...
  d=3   L 136  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FRACTION_DENOMINATOR_GAP_MIN:
  d=3   L 137  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FRACTION_DENOMINATOR_SHIFT_DOWN:
  d=3   L 138  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FRACTION_DENOM_DISPLAY_STYLE_GAP...
  d=3   L 139  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FRACTION_NUMERATOR_DISPLAY_STYLE...
  d=3   L 140  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FRACTION_NUMERATOR_GAP_MIN:
  d=3   L 141  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FRACTION_NUMERATOR_SHIFT_UP:
  d=3   L 142  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FRACTION_NUM_DISPLAY_STYLE_GAP_MIN:
  d=3   L 143  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_FRACTION_RULE_THICKNESS:
  d=3   L 144  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_LOWER_LIMIT_BASELINE_DROP_MIN:
  d=3   L 145  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_LOWER_LIMIT_GAP_MIN:
  d=3   L 146  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_MATH_LEADING:
  d=3   L 147  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_OVERBAR_EXTRA_ASCENDER:
  d=3   L 148  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_OVERBAR_RULE_THICKNESS:
  d=3   L 149  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_OVERBAR_VERTICAL_GAP:
  d=3   L 150  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_RADICAL_DISPLAY_STYLE_VERTICAL_GAP:
  d=3   L 151  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_RADICAL_EXTRA_ASCENDER:
  d=3   L 152  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_RADICAL_RULE_THICKNESS:
  d=3   L 153  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_RADICAL_VERTICAL_GAP:
  d=3   L 154  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SKEWED_FRACTION_VERTICAL_GAP:
  d=3   L 155  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STACK_BOTTOM_DISPLAY_STYLE_SHIFT...
  d=3   L 156  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STACK_BOTTOM_SHIFT_DOWN:
  d=3   L 157  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STACK_DISPLAY_STYLE_GAP_MIN:
  d=3   L 158  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STACK_GAP_MIN:
  d=3   L 159  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STACK_TOP_DISPLAY_STYLE_SHIFT_UP:
  d=3   L 160  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STACK_TOP_SHIFT_UP:
  d=3   L 161  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STRETCH_STACK_BOTTOM_SHIFT_DOWN:
  d=3   L 162  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STRETCH_STACK_GAP_ABOVE_MIN:
  d=3   L 163  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STRETCH_STACK_GAP_BELOW_MIN:
  d=3   L 164  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_STRETCH_STACK_TOP_SHIFT_UP:
  d=3   L 165  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SUBSCRIPT_BASELINE_DROP_MIN:
  d=3   L 166  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SUBSCRIPT_SHIFT_DOWN:
  d=3   L 167  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SUBSCRIPT_TOP_MAX:
  d=3   L 168  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SUB_SUPERSCRIPT_GAP_MIN:
  d=3   L 169  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SUPERSCRIPT_BASELINE_DROP_MAX:
  d=3   L 170  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SUPERSCRIPT_BOTTOM_MAX_WITH_SUBS...
  d=3   L 171  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SUPERSCRIPT_BOTTOM_MIN:
  d=3   L 172  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SUPERSCRIPT_SHIFT_UP:
  d=3   L 173  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_SUPERSCRIPT_SHIFT_UP_CRAMPED:
  d=3   L 174  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_UNDERBAR_EXTRA_DESCENDER:
  d=3   L 175  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_UNDERBAR_RULE_THICKNESS:
  d=3   L 176  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_UNDERBAR_VERTICAL_GAP:
  d=3   L 177  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_UPPER_LIMIT_BASELINE_RISE_MIN:
  d=3   L 178  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_UPPER_LIMIT_GAP_MIN:
  d=3   L 181  T=2 F=110  T=10 F=550  case HB_OT_MATH_CONSTANT_RADICAL_DEGREE_BOTTOM_RAISE_PERC...
  d=3   L 184  T=0 F=112  T=0 F=560  default:
--- d=3  OT::MathKern::get_value(int, hb_font_t*) const  (/src/harfbuzz/src/hb-ot-math-table.hh:343-370) ---
  d=3   L 346  T=0 F=2  T=0 F=10  int sign = font->y_scale < 0 ? -1 : +1;
  d=3   L 358  T=0 F=2  T=0 F=10  while (count > 0)
--- d=1  OT::Device::get_y_delta(hb_font_t*, OT::VariationStore const&, float*) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:3576-3590) ---
  d=1   L3579  T=6 F=88  T=0 F=470  case 1: case 2: case 3:  <-- BLOCKER
  d=1   L3579  T=0 F=94  T=0 F=470  case 1: case 2: case 3:  <-- BLOCKER
  d=1   L3579  T=2 F=92  T=0 F=470  case 1: case 2: case 3:  <-- BLOCKER
  d=1   L3584  T=0 F=94  T=0 F=470  case 0x8000:
  d=1   L3587  T=86 F=8  T=470 F=0  default:

[off-chain: 56 additional divergent branches across 24 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=108c82e4ea676143, size=275 bytes, fuzzer=cmplog, trial=1, discovered_at=2511s, mutation_op=BytesSetMutator,BytesExpandMutator,BytesSetMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 4d 41 54 48   ......      MATH
  0010: 00 01 20 80 00 00 00 00 ff 00 00 00 00 00 03 04   .. .............
  0020: 43 50 41 4c 9c 00 01 00 80 00 00 00 10 00 10 03   CPAL............
  0030: 00 03 10 00 41 41 41 00 20 00 01 04 00 00 00 00   ....AAA. .......
Seed 2 (id=ebd9243d6aea2a6a, size=270 bytes, fuzzer=cmplog, trial=1, discovered_at=2801s, mutation_op=QwordAddMutator):
  0000: 00 01 00 00 00 01 20 00 20 20 20 20 4d 41 54 48   ...... .    MATH
  0010: 00 00 04 02 00 00 00 00 00 10 00 22 00 01 01 02   ..........."....
  0020: 00 04 01 00 0c 02 00 03 00 10 01 00 73 6e 2d 00   ............sn-.
  0030: 01 01 01 00 04 e8 03 0c 01 00 0d 00 02 13 00 fe   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003817559785f774, size=6 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteDecMutator,WordAddMutator):
  0000: 87 0e 0d 0e 22 0e                                 ....".
Seed 2 (id=002edec370c771cf, size=35 bytes, fuzzer=naive, trial=1, discovered_at=47s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteNegMutator,TokenInsert,ByteIncMutator,ByteRandMutator):
  0000: 00 00 00 00 00 00 00 00 00 00 00 00 20 00 64 6f   ............ .do
  0010: 2d 68 0a 6f 74 00 0e 00 20 00 0c 00 0c 09 00 00   -h.ot... .......
  0020: 00 0c 00                                          ...
Seed 3 (id=0016e7ecc5a956f6, size=64 bytes, fuzzer=naive, trial=1, discovered_at=308s, mutation_op=BytesRandInsertMutator,ByteRandMutator):
  0000: 00 75 fe 2d 68 67 68 77 72 75 75 75 80 17 00 00   .u.-hghwruuu....
  0010: 00 20 00 00 23 91 01 9f 9f 9f 9f f3 00 00 00 00   . ..#...........
  0020: 00 00 02 02 02 02 02 02 02 02 00 00 00 00 00 00   ................
  0030: fe fc fe ff 01 20 00 00 00 00 10 00 00 a7 00 00   ..... ..........
Seed 4 (id=0002ee9aae2b9bef, size=54 bytes, fuzzer=naive, trial=1, discovered_at=470s, mutation_op=WordInterestingMutator,TokenInsert,BytesExpandMutator,ByteInterestingMutator):
  0000: 00 ff 00 00 1d 20 00 00 c8 0a 01 00 70 78 2d 68   ..... ......px-h
  0010: 61 6e 74 2d 68 6b 00 74 40 01 00 00 00 20 01 00   ant-hk.t@.... ..
  0020: c8 0a 01 00 40 62 91 6d 00 00 00 20 01 00 c8 7f   ....@b.m... ....
  0030: 01 00 40 62 91 6d                                 ..@b.m
Seed 5 (id=0030c881e05b69bb, size=56 bytes, fuzzer=naive, trial=1, discovered_at=4302s, mutation_op=BytesExpandMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesDeleteMutator,WordAddMutator,ByteIncMutator):
  0000: 6d 6d 6e 2d 68 61 6e 74 00 19 19 6d 01 00 9a 19   mmn-hant...m....
  0010: 00 73 6e 2d 68 61 6e 74 00 19 90 76 6c 67 70 90   .sn-hant...vlgp.
  0020: 6e 74 61 6c 90 00 a6 06 65 65 6d 00 3c 0b 00 00   ntal....eem.<...
  0030: 00 19 00 00 52 06 00 00                           ....R...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x2                             00(.)x3 05(.)x2 87(.)x1 6d(m)x1 +3u  PARTIAL
   0x0001  01(.)x2                             00(.)x2 07(.)x2 0e(.)x1 75(u)x1 +4u  DIFFER
   0x0002  00(.)x2                             00(.)x5 0d(.)x1 fe(.)x1 6e(n)x1 +2u  PARTIAL
   0x0003  00(.)x2                             00(.)x5 2d(-)x2 0e(.)x1 cb(.)x1 +1u  PARTIAL
   0x0004  00(.)x2                             00(.)x2 68(h)x2 70(p)x2 22(")x1 +3u  PARTIAL
   0x0005  01(.)x2                             0e(.)x1 00(.)x1 67(g)x1 20( )x1 +6u  DIFFER
   0x0006  20( )x2                             00(.)x4 68(h)x1 6e(n)x1 ff(.)x1 +2u  DIFFER
   0x0007  20( )x1 00(.)x1                     00(.)x4 77(w)x1 74(t)x1 cc(.)x1 +2u  PARTIAL
   0x0008  20( )x2                             00(.)x2 72(r)x1 c8(.)x1 5b([)x1 +4u  DIFFER
   0x0009  20( )x2                             00(.)x1 75(u)x1 0a(.)x1 19(.)x1 +5u  PARTIAL
   0x000a  20( )x2                             00(.)x4 75(u)x1 01(.)x1 19(.)x1 +2u  DIFFER
   0x000b  20( )x2                             00(.)x5 75(u)x1 6d(m)x1 ff(.)x1 +1u  DIFFER
   0x000c  4d(M)x2                             20( )x1 80(.)x1 70(p)x1 01(.)x1 +5u  DIFFER
   0x000d  41(A)x2                             00(.)x3 17(.)x1 78(x)x1 3f(?)x1 +3u  DIFFER
   0x000e  54(T)x2                             00(.)x2 64(d)x1 2d(-)x1 9a(.)x1 +4u  DIFFER
   0x000f  48(H)x2                             00(.)x2 6f(o)x1 68(h)x1 19(.)x1 +4u  DIFFER
   0x0010  00(.)x2                             00(.)x3 2d(-)x1 61(a)x1 0a(.)x1 +3u  PARTIAL
   0x0011  01(.)x1 00(.)x1                     20( )x2 68(h)x1 6e(n)x1 73(s)x1 +4u  PARTIAL
   0x0012  20( )x1 04(.)x1                     00(.)x4 0a(.)x1 74(t)x1 6e(n)x1 +2u  DIFFER
   0x0013  80(.)x1 02(.)x1                     00(.)x4 2d(-)x2 6f(o)x1 20( )x1 +1u  DIFFER
   0x0014  00(.)x2                             68(h)x3 74(t)x1 23(#)x1 18(.)x1 +3u  PARTIAL
   0x0015  00(.)x2                             00(.)x3 91(.)x1 6b(k)x1 61(a)x1 +3u  PARTIAL
   0x0016  00(.)x2                             00(.)x4 0e(.)x1 01(.)x1 6e(n)x1 +2u  PARTIAL
   0x0017  00(.)x2                             00(.)x2 74(t)x2 9f(.)x1 ff(.)x1 +3u  PARTIAL
   0x0018  ff(.)x1 00(.)x1                     20( )x2 00(.)x2 9f(.)x1 40(@)x1 +3u  PARTIAL
   0x0019  00(.)x1 10(.)x1                     00(.)x2 9f(.)x1 01(.)x1 19(.)x1 +4u  PARTIAL
   0x001a  00(.)x2                             00(.)x3 0c(.)x1 9f(.)x1 90(.)x1 +3u  PARTIAL
   0x001b  00(.)x1 22(")x1                     00(.)x4 ff(.)x2 f3(.)x1 76(v)x1 +1u  PARTIAL
   0x001c  00(.)x2                             00(.)x4 0c(.)x1 6c(l)x1 a9(.)x1 +2u  PARTIAL
   0x001d  00(.)x1 01(.)x1                     00(.)x2 09(.)x1 20( )x1 67(g)x1 +4u  PARTIAL
   0x001e  03(.)x1 01(.)x1                     00(.)x4 01(.)x2 70(p)x1 ff(.)x1 +1u  PARTIAL
   0x001f  04(.)x1 02(.)x1                     00(.)x4 90(.)x1 34(4)x1 57(W)x1 +1u  DIFFER
   0x0020  43(C)x1 00(.)x1                     00(.)x2 c8(.)x1 6e(n)x1 0e(.)x1 +3u  PARTIAL
   0x0021  50(P)x1 04(.)x1                     00(.)x2 0c(.)x1 0a(.)x1 74(t)x1 +3u  DIFFER
   0x0022  41(A)x1 01(.)x1                     00(.)x2 01(.)x2 02(.)x1 61(a)x1 +1u  PARTIAL
   0x0023  4c(L)x1 00(.)x1                     00(.)x2 02(.)x1 6c(l)x1 cb(.)x1 +1u  PARTIAL
   0x0024  9c(.)x1 0c(.)x1                     02(.)x1 40(@)x1 90(.)x1 0c(.)x1 +2u  PARTIAL
   0x0025  00(.)x1 02(.)x1                     00(.)x2 02(.)x1 62(b)x1 25(%)x1 +1u  PARTIAL
   0x0026  01(.)x1 00(.)x1                     02(.)x1 91(.)x1 a6(.)x1 0c(.)x1 +2u  PARTIAL
   0x0027  00(.)x1 03(.)x1                     02(.)x1 6d(m)x1 06(.)x1 20( )x1 +2u  DIFFER
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
  prompts_b/harfbuzz_5494.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5494,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5494 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5494 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5494 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).