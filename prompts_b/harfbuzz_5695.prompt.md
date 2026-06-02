==== BLOCKER ====
Target: harfbuzz
Branch ID: 5695
Location: /src/harfbuzz/src/hb-ot-shape.cc:154:19
Enclosing function: hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&)
Source line:   bool has_gsub = !apply_morx && hb_ot_layout_has_substitution (face);
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           5        5          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=7.90h  loser=24.00h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=16.10h  hit_div=4
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5695/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&) (/src/harfbuzz/src/hb-ot-shape.cc:103-213) ---
[ ]   101  hb_ot_shape_planner_t::compile (hb_ot_shape_plan_t           &plan,
[ ]   102  				const hb_ot_shape_plan_key_t &key)
[B]   103  {
[B]   104    plan.props = props;
[B]   105    plan.shaper = shaper;
[B]   106    map.compile (plan.map, key);
[ ]   107  
[B]   108  #ifndef HB_NO_OT_SHAPE_FRACTIONS
[B]   109    plan.frac_mask = plan.map.get_1_mask (HB_TAG ('f','r','a','c'));
[B]   110    plan.numr_mask = plan.map.get_1_mask (HB_TAG ('n','u','m','r'));
[B]   111    plan.dnom_mask = plan.map.get_1_mask (HB_TAG ('d','n','o','m'));
[B]   112    plan.has_frac = plan.frac_mask || (plan.numr_mask && plan.dnom_mask);
[B]   113  #endif
[ ]   114  
[B]   115    plan.rtlm_mask = plan.map.get_1_mask (HB_TAG ('r','t','l','m'));
[B]   116    plan.has_vert = !!plan.map.get_1_mask (HB_TAG ('v','e','r','t'));
[ ]   117  
[B]   118    hb_tag_t kern_tag = HB_DIRECTION_IS_HORIZONTAL (props.direction) ?
[B]   119  		      HB_TAG ('k','e','r','n') : HB_TAG ('v','k','r','n');
[B]   120  #ifndef HB_NO_OT_KERN
[B]   121    plan.kern_mask = plan.map.get_mask (kern_tag);
[B]   122    plan.requested_kerning = !!plan.kern_mask;
[B]   123  #endif
[B]   124  #ifndef HB_NO_AAT_SHAPE
[B]   125    plan.trak_mask = plan.map.get_mask (HB_TAG ('t','r','a','k'));
[B]   126    plan.requested_tracking = !!plan.trak_mask;
[B]   127  #endif
[ ]   128  
[B]   129    bool has_gpos_kern = plan.map.get_feature_index (1, kern_tag) != HB_OT_LAYOUT_NO_FEATURE_INDEX;
[B]   130    bool disable_gpos = plan.shaper->gpos_tag &&
[B]   131  		      plan.shaper->gpos_tag != plan.map.chosen_script[1];
[ ]   132  
[ ]   133    /*
[ ]   134     * Decide who provides glyph classes. GDEF or Unicode.
[ ]   135     */
[ ]   136  
[B]   137    if (!hb_ot_layout_has_glyph_classes (face))
[B]   138      plan.fallback_glyph_classes = true;
[ ]   139  
[ ]   140    /*
[ ]   141     * Decide who does substitutions. GSUB, morx, or fallback.
[ ]   142     */
[ ]   143  
[B]   144  #ifndef HB_NO_AAT_SHAPE
[B]   145    plan.apply_morx = apply_morx;
[B]   146  #endif
[ ]   147  
[ ]   148    /*
[ ]   149     * Decide who does positioning. GPOS, kerx, kern, or fallback.
[ ]   150     */
[ ]   151  
[B]   152  #ifndef HB_NO_AAT_SHAPE
[B]   153    bool has_kerx = hb_aat_layout_has_positioning (face);
[B]   154    bool has_gsub = !apply_morx && hb_ot_layout_has_substitution (face); <-- BLOCKER
[B]   155  #endif
[B]   156    bool has_gpos = !disable_gpos && hb_ot_layout_has_positioning (face);
[B]   157    if (false)
[ ]   158      ;
[B]   159  #ifndef HB_NO_AAT_SHAPE
[ ]   160    /* Prefer GPOS over kerx if GSUB is present;
[ ]   161     * https://github.com/harfbuzz/harfbuzz/issues/3008 */
[B]   162    else if (has_kerx && !(has_gsub && has_gpos))
[ ]   163      plan.apply_kerx = true;
[B]   164  #endif
[B]   165    else if (has_gpos)
[W]   166      plan.apply_gpos = true;
[ ]   167  
[B]   168    if (!plan.apply_kerx && (!has_gpos_kern || !plan.apply_gpos))
[B]   169    {
[B]   170  #ifndef HB_NO_AAT_SHAPE
[B]   171      if (has_kerx)
[ ]   172        plan.apply_kerx = true;
[B]   173      else
[B]   174  #endif
[B]   175  #ifndef HB_NO_OT_KERN
[B]   176      if (hb_ot_layout_has_kerning (face))
[ ]   177        plan.apply_kern = true;
[B]   178  #endif
[B]   179    }
[ ]   180  
[B]   181    plan.apply_fallback_kern = !(plan.apply_gpos || plan.apply_kerx || plan.apply_kern);
[ ]   182  
[B]   183    plan.zero_marks = script_zero_marks &&
[B]   184  		    !plan.apply_kerx &&
[B]   185  		    (!plan.apply_kern
[B]   186  #ifndef HB_NO_OT_KERN
[B]   187  		     || !hb_ot_layout_has_machine_kerning (face)
[B]   188  #endif
[B]   189  		    );
[B]   190    plan.has_gpos_mark = !!plan.map.get_1_mask (HB_TAG ('m','a','r','k'));
[ ]   191  
[B]   192    plan.adjust_mark_positioning_when_zeroing = !plan.apply_gpos &&
[B]   193  					      !plan.apply_kerx &&
[B]   194  					      (!plan.apply_kern
[B]   195  #ifndef HB_NO_OT_KERN
[B]   196  					       || !hb_ot_layout_has_cross_kerning (face)
[B]   197  #endif
[B]   198  					      );
[ ]   199  
[B]   200    plan.fallback_mark_positioning = plan.adjust_mark_positioning_when_zeroing &&
[B]   201  				   script_fallback_mark_positioning;
[ ]   202  
[B]   203  #ifndef HB_NO_AAT_SHAPE
[ ]   204    /* If we're using morx shaping, we cancel mark position adjustment because
[ ]   205       Apple Color Emoji assumes this will NOT be done when forming emoji sequences;
[ ]   206       https://github.com/harfbuzz/harfbuzz/issues/2967. */
[B]   207    if (plan.apply_morx)
[W]   208      plan.adjust_mark_positioning_when_zeroing = false;
[ ]   209  
[ ]   210    /* Currently we always apply trak. */
[B]   211    plan.apply_trak = plan.requested_tracking && hb_aat_layout_has_tracking (face);
[B]   212  #endif
[B]   213  }

--- Caller (1 hop): hb_aat_layout_substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_feature_t const*, unsigned int) (/src/harfbuzz/src/hb-aat-layout.cc:250-278, calls hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&) at line 255) (full body — short) ---
[W]   250  {
[W]   251    hb_aat_map_builder_t builder (font->face, plan->props);
[W]   252    for (unsigned i = 0; i < num_features; i++)
[ ]   253      builder.add_feature (features[i]);
[W]   254    hb_aat_map_t map;
[W]   255    builder.compile (map); <-- CALL
[ ]   256  
[W]   257    hb_blob_t *morx_blob = font->face->table.morx.get_blob ();
[W]   258    const AAT::morx& morx = *morx_blob->as<AAT::morx> ();
[W]   259    if (morx.has_data ())
[W]   260    {
[W]   261      AAT::hb_aat_apply_context_t c (plan, font, buffer, morx_blob);
[W]   262      if (!buffer->message (font, "start table morx")) return;
[W]   263      morx.apply (&c, map);
[W]   264      (void) buffer->message (font, "end table morx");
[W]   265      return;
[W]   266    }
[ ]   267  
[W]   268    hb_blob_t *mort_blob = font->face->table.mort.get_blob ();
[W]   269    const AAT::mort& mort = *mort_blob->as<AAT::mort> ();
[W]   270    if (mort.has_data ())
[W]   271    {
[W]   272      AAT::hb_aat_apply_context_t c (plan, font, buffer, mort_blob);
[W]   273      if (!buffer->message (font, "start table mort")) return;
[W]   274      mort.apply (&c, map);
[W]   275      (void) buffer->message (font, "end table mort");
[W]   276      return;
[W]   277    }
[W]   278  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb_aat_layout_substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_feature_t const*, unsigned int)  (/src/harfbuzz/src/hb-aat-layout.cc:250-278, calls hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&) at line 255)
hop 2  hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:218-241, calls hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&) at line 228)
hop 3  hb_ot_face_t::init0(hb_face_t*)  (/src/harfbuzz/src/hb-ot-face.cc:47-52, calls hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*) at line 49)
hop 3  hb-ot-shape.cc:hb_ot_substitute_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:904-919, calls hb_aat_layout_substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_feature_t const*, unsigned int) at line 914)
hop 3  hb_shape_plan_create2  (/src/harfbuzz/src/hb-shape-plan.cc:228-275, calls hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*) at line 261)
hop 4  hb_face_create_for_tables  (/src/harfbuzz/src/hb-face.cc:121-140, calls hb_ot_face_t::init0(hb_face_t*) at line 136)
hop 4  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934, calls hb-ot-shape.cc:hb_ot_substitute_plan(hb_ot_shape_context_t const*) at line 928)
hop 4  hb_shape_plan_create  (/src/harfbuzz/src/hb-shape-plan.cc:195-200, calls hb_shape_plan_create2 at line 196)
hop 4  hb_shape_plan_create_cached2  (/src/harfbuzz/src/hb-shape-plan.cc:521-578, calls hb_shape_plan_create2 at line 554)
hop 5  hb_face_create  (/src/harfbuzz/src/hb-face.cc:218-241, calls hb_face_create_for_tables at line 234)
hop 5  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*) at line 1184)
hop 5  hb_shape_plan_create_cached  (/src/harfbuzz/src/hb-shape-plan.cc:487-492, calls hb_shape_plan_create_cached2 at line 488)
hop 5  hb_shape_full  (/src/harfbuzz/src/hb-shape.cc:130-171, calls hb_shape_plan_create_cached2 at line 143)
hop 6  hb-buffer-verify.cc:buffer_verify_unsafe_to_break(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:94-203, calls hb_shape_full at line 165)
hop 6  hb-buffer-verify.cc:buffer_verify_unsafe_to_concat(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:212-401, calls hb_shape_full at line 319)
hop 6  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)
hop 6  hb_ot_shape_glyphs_closure  (/src/harfbuzz/src/hb-ot-shape.cc:1272-1291, calls hb_shape_plan_create_cached at line 1274)
hop 6  LLVMFuzzerTestOneInput  (/src/harfbuzz/test/fuzzing/hb-shape-fuzzer.cc:13-64, calls hb_face_create at line 18)
hop 7  hb_buffer_t::verify(hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:409-436, calls hb-buffer-verify.cc:buffer_verify_unsafe_to_break(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*) at line 413)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      66       312  hb-ot-shape.cc:_hb_codepoint_is_regional_indicator(unsigned int)  (/src/harfbuzz/src/hb-ot-shape.cc:52-52)
       0       190  hb_ot_shape_plan_t::substitute(hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-shape.cc:255-257)
      42       190  hb_ot_shape_plan_t::position(hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-shape.cc:262-281)
      42       190  hb-ot-shape.cc:hb_set_unicode_props(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:457-517)
      42       190  hb-ot-shape.cc:hb_insert_dotted_circle(hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:521-546)
      42       190  hb-ot-shape.cc:hb_form_clusters(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:550-560)
      42       190  hb-ot-shape.cc:hb_ensure_native_direction(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:564-619)
      42       190  hb-ot-shape.cc:hb_ot_rotate_chars(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:681-710)
      42       190  hb-ot-shape.cc:hb_ot_shape_setup_masks_fraction(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:714-764)
      42       190  hb-ot-shape.cc:hb_ot_shape_initialize_masks(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:768-774)
      42       190  hb-ot-shape.cc:hb_ot_shape_setup_masks(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:778-796)
      42       190  hb-ot-shape.cc:hb_ot_zero_width_default_ignorables(hb_buffer_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:800-813)
      42       190  hb-ot-shape.cc:hb_ot_hide_default_ignorables(hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:818-839)
      42       190  hb-ot-shape.cc:hb_ot_map_glyphs_fast(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:844-852)
      42       190  hb-ot-shape.cc:hb_synthesize_glyph_classes(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:856-878)
... (36 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195) ---
  d=5   L1177  T=0 F=42  T=3 F=187  if (c->plan->shaper->preprocess_text &&
  d=5   L1178  T=0 F=0  T=3 F=0  c->buffer->message(c->font, "start preprocess-text"))
--- d=4  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934) ---
  d=4   L 931  T=21 F=21  T=0 F=0  if (c->plan->apply_morx && c->plan->apply_gpos)
  d=4   L 931  T=42 F=0  T=0 F=190  if (c->plan->apply_morx && c->plan->apply_gpos)
--- d=3  hb-ot-shape.cc:hb_ot_substitute_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:904-919) ---
  d=3   L 909  T=42 F=0  T=190 F=0  if (c->plan->fallback_glyph_classes)
--- d=2  hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:218-241) ---
  d=2   L 230  T=0 F=2  T=7 F=11  if (shaper->data_create)
--- d=2  hb_aat_layout_substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, hb_feature_t const*, unsigned int)  (/src/harfbuzz/src/hb-aat-layout.cc:250-278) ---
  d=2   L 252  T=0 F=42  T=0 F=0  for (unsigned i = 0; i < num_features; i++)
  d=2   L 259  T=21 F=21  T=0 F=0  if (morx.has_data ())
  d=2   L 262  T=0 F=21  T=0 F=0  if (!buffer->message (font, "start table morx")) return;
  d=2   L 270  T=21 F=0  T=0 F=0  if (mort.has_data ())
  d=2   L 273  T=0 F=21  T=0 F=0  if (!buffer->message (font, "start table mort")) return;
--- d=1  hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&)  (/src/harfbuzz/src/hb-ot-shape.cc:103-213) ---
  d=1   L 112  T=0 F=2  T=0 F=18  plan.has_frac = plan.frac_mask || (plan.numr_mask && plan...
  d=1   L 112  T=0 F=2  T=0 F=18  plan.has_frac = plan.frac_mask || (plan.numr_mask && plan...
  d=1   L 130  T=0 F=2  T=0 F=18  bool disable_gpos = plan.shaper->gpos_tag &&
  d=1   L 137  T=2 F=0  T=18 F=0  if (!hb_ot_layout_has_glyph_classes (face))
  d=1   L 154  T=0 F=2  T=18 F=0  bool has_gsub = !apply_morx && hb_ot_layout_has_substitut...  <-- BLOCKER
  d=1   L 154  T=0 F=0  T=0 F=18  bool has_gsub = !apply_morx && hb_ot_layout_has_substitut...  <-- BLOCKER
  d=1   L 156  T=2 F=0  T=18 F=0  bool has_gpos = !disable_gpos && hb_ot_layout_has_positio...
  d=1   L 156  T=1 F=1  T=0 F=18  bool has_gpos = !disable_gpos && hb_ot_layout_has_positio...
  d=1   L 162  T=0 F=2  T=0 F=18  else if (has_kerx && !(has_gsub && has_gpos))
  d=1   L 165  T=1 F=1  T=0 F=18  else if (has_gpos)
  d=1   L 168  T=2 F=0  T=18 F=0  if (!plan.apply_kerx && (!has_gpos_kern || !plan.apply_gp...
  d=1   L 168  T=2 F=0  T=18 F=0  if (!plan.apply_kerx && (!has_gpos_kern || !plan.apply_gp...
  d=1   L 171  T=0 F=2  T=0 F=18  if (has_kerx)
  d=1   L 176  T=0 F=2  T=0 F=18  if (hb_ot_layout_has_kerning (face))
  d=1   L 181  T=1 F=1  T=0 F=18  plan.apply_fallback_kern = !(plan.apply_gpos || plan.appl...
  d=1   L 181  T=0 F=1  T=0 F=18  plan.apply_fallback_kern = !(plan.apply_gpos || plan.appl...
  d=1   L 181  T=0 F=1  T=0 F=18  plan.apply_fallback_kern = !(plan.apply_gpos || plan.appl...
  d=1   L 183  T=2 F=0  T=14 F=4  plan.zero_marks = script_zero_marks &&
  d=1   L 184  T=2 F=0  T=14 F=0  !plan.apply_kerx &&
  d=1   L 185  T=2 F=0  T=14 F=0  (!plan.apply_kern
  d=1   L 192  T=1 F=1  T=18 F=0  plan.adjust_mark_positioning_when_zeroing = !plan.apply_g...
  d=1   L 193  T=1 F=0  T=18 F=0  !plan.apply_kerx &&
  d=1   L 194  T=1 F=0  T=18 F=0  (!plan.apply_kern
  d=1   L 200  T=1 F=1  T=18 F=0  plan.fallback_mark_positioning = plan.adjust_mark_positio...
  d=1   L 201  T=1 F=0  T=13 F=5  script_fallback_mark_positioning;
  d=1   L 207  T=2 F=0  T=0 F=18  if (plan.apply_morx)
  d=1   L 211  T=0 F=2  T=0 F=18  plan.apply_trak = plan.requested_tracking && hb_aat_layou...
  d=1   L 211  T=2 F=0  T=18 F=0  plan.apply_trak = plan.requested_tracking && hb_aat_layou...

[off-chain: 78 additional divergent branches across 25 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=ae73a8c9233c3cb8, size=40 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1650s, mutation_op=ByteNegMutator,DwordAddMutator,ByteAddMutator,WordInterestingMutator,BytesRandSetMutator,BytesRandSetMutator):
  0000: 4f 54 54 4f 00 01 20 20 21 21 20 20 6d 6f 72 78   OTTO..  !!  morx
  0010: 20 40 00 20 00 00 00 20 40 00 20 00 00 00 18 00    @. ... @. .....
  0020: 02 1f 08 0d 00 00 00 00                           ........
Seed 2 (id=47909b1df33a210f, size=273 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=39935s, mutation_op=BytesInsertCopyMutator,ByteDecMutator,BytesDeleteMutator,BytesInsertMutator,BytesInsertCopyMutator,CrossoverReplaceMutator,WordAddMutator):
  0000: 00 01 00 00 00 02 ee ff 00 30 00 20 47 50 4f 53   .........0. GPOS
  0010: 20 28 20 03 00 00 00 00 ff ff 00 ec 6d 6f 72 74    ( .........mort
  0020: 00 10 16 36 00 00 00 10 ec 1e 1e 1e 1e 1e 1e 1e   ...6............
  0030: 1e 1e 1e 1e 1e 1e ec ec ec ec ec ec 18 18 e8 20   ............... 

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 2 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 3 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i
Seed 4 (id=00167ff70704a0e0, size=23 bytes, fuzzer=value_profile, trial=1, discovered_at=120s, mutation_op=BytesInsertCopyMutator,CrossoverInsertMutator,ByteDecMutator):
  0000: 4c 0e 00 00 4c 0e 00 00 4c 16 00 00 00 18 18 00   L...L...L.......
  0010: 00 42 18 65 0e 00 ff                              .B.e...
Seed 5 (id=0059bffc70552fa0, size=62 bytes, fuzzer=value_profile, trial=1, discovered_at=197s, mutation_op=DwordInterestingMutator,BytesRandInsertMutator,BytesInsertMutator):
  0000: 00 01 0e 00 df 20 00 00 00 00 aa 13 df 20 3d 3d   ..... ....... ==
  0010: 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 00 ff   ==============..
  0020: df 20 00 00 00 00 00 20 20 20 20 20 20 20 20 20   . .....         
  0030: 2c 00 00 00 64 55 55 55 df 20 00 00 00 00         ,...dUUU. ....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  4f(O)x1 00(.)x1                     e0(.)x2 fe(.)x1 4c(L)x1 00(.)x1 +5u  PARTIAL
   0x0001  54(T)x1 01(.)x1                     ff(.)x1 17(.)x1 e8(.)x1 0e(.)x1 +6u  PARTIAL
   0x0002  54(T)x1 00(.)x1                     00(.)x5 ff(.)x2 0e(.)x1 8a(.)x1 +1u  PARTIAL
   0x0003  4f(O)x1 00(.)x1                     00(.)x6 ff(.)x2 8a(.)x1 b7(.)x1     PARTIAL
   0x0004  00(.)x2                             df(.)x2 f4(.)x1 1a(.)x1 20( )x1 +5u  DIFFER
   0x0005  01(.)x1 02(.)x1                     20( )x3 00(.)x3 0e(.)x2 01(.)x1 +1u  PARTIAL
   0x0006  20( )x1 ee(.)x1                     00(.)x8 e0(.)x1 e5(.)x1             DIFFER
   0x0007  20( )x1 ff(.)x1                     00(.)x7 e0(.)x1 55(U)x1 01(.)x1     DIFFER
   0x0008  21(!)x1 00(.)x1                     20( )x2 00(.)x2 29())x1 e0(.)x1 +4u  PARTIAL
   0x0009  21(!)x1 30(0)x1                     00(.)x2 2b(+)x1 17(.)x1 16(.)x1 +5u  DIFFER
   0x000a  20( )x1 00(.)x1                     00(.)x5 29())x1 aa(.)x1 89(.)x1 +2u  PARTIAL
   0x000b  20( )x2                             00(.)x7 29())x1 13(.)x1 15(.)x1     DIFFER
   0x000c  6d(m)x1 47(G)x1                     00(.)x2 01(.)x1 2c(,)x1 2b(+)x1 +5u  DIFFER
   0x000d  6f(o)x1 50(P)x1                     20( )x4 18(.)x1 08(.)x1 fb(.)x1 +2u  DIFFER
   0x000e  72(r)x1 4f(O)x1                     00(.)x3 e0(.)x1 18(.)x1 3d(=)x1 +3u  DIFFER
   0x000f  78(x)x1 53(S)x1                     00(.)x3 6a(j)x1 fa(.)x1 3d(=)x1 +3u  DIFFER
   0x0010  20( )x2                             20( )x2 00(.)x2 79(y)x1 3d(=)x1 +3u  PARTIAL
   0x0011  40(@)x1 28(()x1                     20( )x2 2d(-)x1 00(.)x1 42(B)x1 +4u  DIFFER
   0x0012  00(.)x1 20( )x1                     00(.)x4 68(h)x1 18(.)x1 3d(=)x1 +2u  PARTIAL
   0x0013  20( )x1 03(.)x1                     00(.)x2 61(a)x1 55(U)x1 65(e)x1 +4u  PARTIAL
   0x0014  00(.)x2                             6e(n)x1 e0(.)x1 0e(.)x1 3d(=)x1 +5u  PARTIAL
   0x0015  00(.)x2                             74(t)x1 17(.)x1 00(.)x1 3d(=)x1 +5u  PARTIAL
   0x0016  00(.)x2                             00(.)x4 2d(-)x1 ff(.)x1 3d(=)x1 +2u  PARTIAL
   0x0017  20( )x1 00(.)x1                     00(.)x5 68(h)x1 3d(=)x1 20( )x1     PARTIAL
   0x0018  40(@)x1 ff(.)x1                     20( )x2 6b(k)x1 61(a)x1 3d(=)x1 +3u  DIFFER
   0x0019  00(.)x1 ff(.)x1                     20( )x2 00(.)x1 2e(.)x1 3d(=)x1 +3u  PARTIAL
   0x001a  20( )x1 00(.)x1                     20( )x2 00(.)x2 69(i)x1 3d(=)x1 +2u  PARTIAL
   0x001b  00(.)x1 ec(.)x1                     00(.)x4 3d(=)x1 9f(.)x1 20( )x1     PARTIAL
   0x001c  00(.)x1 6d(m)x1                     00(.)x2 3d(=)x1 4c(L)x1 20( )x1 +2u  PARTIAL
   0x001d  00(.)x1 6f(o)x1                     00(.)x1 3d(=)x1 06(.)x1 7f(.)x1 +3u  PARTIAL
   0x001e  18(.)x1 72(r)x1                     00(.)x4 ff(.)x1 80(.)x1 13(.)x1     DIFFER
   0x001f  00(.)x1 74(t)x1                     00(.)x2 01(.)x1 ff(.)x1 54(T)x1 +2u  PARTIAL
   0x0020  02(.)x1 00(.)x1                     00(.)x2 df(.)x1 37(7)x1 54(T)x1 +2u  PARTIAL
   0x0021  1f(.)x1 10(.)x1                     0e(.)x2 07(.)x1 20( )x1 6f(o)x1 +2u  DIFFER
   0x0022  08(.)x1 16(.)x1                     00(.)x6 1b(.)x1                     DIFFER
   0x0023  0d(.)x1 36(6)x1                     00(.)x5 6d(m)x1 2d(-)x1             DIFFER
   0x0024  00(.)x2                             00(.)x3 01(.)x1 4c(L)x1 20( )x1 +1u  PARTIAL
   0x0025  00(.)x2                             00(.)x3 20( )x1 9f(.)x1 43(C)x1 +1u  PARTIAL
   0x0026  00(.)x2                             00(.)x2 20( )x1 9f(.)x1 09(.)x1 +2u  PARTIAL
   0x0027  00(.)x1 10(.)x1                     20( )x3 9f(.)x1 68(h)x1 61(a)x1 +1u  DIFFER
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
  prompts_b/harfbuzz_5695.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5695,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5695 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5695 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5695 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).