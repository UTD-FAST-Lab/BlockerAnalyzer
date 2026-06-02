==== BLOCKER ====
Target: harfbuzz
Branch ID: 5708
Location: /src/harfbuzz/src/hb-ot-shape.cc:187:11
Enclosing function: hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&)
Source line: 		     || !hb_ot_layout_has_machine_kerning (face)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile); loser (ctx_coverage vs naive_ctx); loser (calibrated_energy vs minimizer)
cmplog                           2        7          1  REFERENCE
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog             2        7          1  REFERENCE
naive_ctx                        9        1          0  winner (ctx_coverage vs naive)
naive_ngram4                     2        8          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        9        1          0  winner (calibrated_energy vs naive)
fast                             9        1          0  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['minimizer', 'naive', 'naive_ctx', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'fast', 'grimoire']

==== DECISIVE PAIRS (3) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 12  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.40h  loser=15.40h
  avg hitcount on branch: winner=14  loser=40
  prob_div=0.70  dur_div=8.00h  hit_div=26
  subject-level: delta_AUC=17795340.0  p_AUC=0.0002  delta_Final=285.0  p_final=0.0002
--- Pair 2: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 15  (naive_ctx vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=10.50h  loser=15.40h
  avg hitcount on branch: winner=14  loser=40
  prob_div=0.70  dur_div=4.90h  hit_div=26
  subject-level: delta_AUC=15634800.0  p_AUC=0.0003  delta_Final=258.3  p_final=0.0002
--- Pair 3: minimizer > naive  [delta: calibrated_energy] ---
  subject 18  (minimizer vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=2.90h  loser=15.40h
  avg hitcount on branch: winner=92  loser=40
  prob_div=0.70  dur_div=12.50h  hit_div=52
  subject-level: delta_AUC=13277160.0  p_AUC=0.001  delta_Final=189.1  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5708/{W,L}/branch_coverage_show.txt

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
[B]   154    bool has_gsub = !apply_morx && hb_ot_layout_has_substitution (face);
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
[ ]   166      plan.apply_gpos = true;
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
[B]   177        plan.apply_kern = true;
[B]   178  #endif
[B]   179    }
[ ]   180  
[B]   181    plan.apply_fallback_kern = !(plan.apply_gpos || plan.apply_kerx || plan.apply_kern);
[ ]   182  
[B]   183    plan.zero_marks = script_zero_marks &&
[B]   184  		    !plan.apply_kerx &&
[B]   185  		    (!plan.apply_kern
[B]   186  #ifndef HB_NO_OT_KERN
[B]   187  		     || !hb_ot_layout_has_machine_kerning (face) <-- BLOCKER
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
[ ]   208      plan.adjust_mark_positioning_when_zeroing = false;
[ ]   209  
[ ]   210    /* Currently we always apply trak. */
[B]   211    plan.apply_trak = plan.requested_tracking && hb_aat_layout_has_tracking (face);
[B]   212  #endif
[B]   213  }

--- Caller (1 hop): hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*) (/src/harfbuzz/src/hb-ot-shape.cc:218-241, calls hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&) at line 228) (full body — short) ---
[B]   218  {
[B]   219    map.init ();
[ ]   220  
[B]   221    hb_ot_shape_planner_t planner (face,
[B]   222  				 key->props);
[ ]   223  
[B]   224    hb_ot_shape_collect_features (&planner,
[B]   225  				key->user_features,
[B]   226  				key->num_user_features);
[ ]   227  
[B]   228    planner.compile (*this, key->ot); <-- CALL
[ ]   229  
[B]   230    if (shaper->data_create)
[B]   231    {
[B]   232      data = shaper->data_create (this);
[B]   233      if (unlikely (!data))
[ ]   234      {
[ ]   235        map.fini ();
[ ]   236        return false;
[ ]   237      }
[B]   238    }
[ ]   239  
[B]   240    return true;
[B]   241  }

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
       0       146  hb-ot-shape.cc:zero_mark_widths_by_gdef(hb_buffer_t*, bool)  (/src/harfbuzz/src/hb-ot-shape.cc:974-984)
      21         7  hb_aat_layout_get_feature_types  (/src/harfbuzz/src/hb-aat-layout.cc:385-387)
      21         7  hb_aat_layout_feature_type_get_name_id  (/src/harfbuzz/src/hb-aat-layout.cc:403-405)
      21         7  hb_aat_layout_feature_type_get_selector_infos  (/src/harfbuzz/src/hb-aat-layout.cc:435-437)
      21         7  _hb_ot_shaper_face_data_create  (/src/harfbuzz/src/hb-ot-shape.cc:403-405)
      21         7  _hb_ot_shaper_face_data_destroy  (/src/harfbuzz/src/hb-ot-shape.cc:409-410)
      21         7  _hb_ot_shaper_font_data_create  (/src/harfbuzz/src/hb-ot-shape.cc:421-423)
      21         7  _hb_ot_shaper_font_data_destroy  (/src/harfbuzz/src/hb-ot-shape.cc:427-428)
       0         7  hb-ot-shape.cc:zero_mark_width(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:967-970)
       0         5  hb-ot-shape.cc:adjust_mark_offsets(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:960-963)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195) ---
  d=5   L1177  T=7 F=395  T=1 F=146  if (c->plan->shaper->preprocess_text &&
  d=5   L1178  T=7 F=0  T=1 F=0  c->buffer->message(c->font, "start preprocess-text"))
--- d=4  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934) ---
  d=4   L 931  T=0 F=402  T=0 F=147  if (c->plan->apply_morx && c->plan->apply_gpos)
--- d=3  hb-ot-shape.cc:hb_ot_substitute_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:904-919) ---
  d=3   L 909  T=402 F=0  T=147 F=0  if (c->plan->fallback_glyph_classes)
--- d=2  hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:218-241) ---
  d=2   L 230  T=5 F=38  T=4 F=11  if (shaper->data_create)
--- d=1  hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&)  (/src/harfbuzz/src/hb-ot-shape.cc:103-213) ---
  d=1   L 112  T=0 F=43  T=0 F=15  plan.has_frac = plan.frac_mask || (plan.numr_mask && plan...
  d=1   L 112  T=0 F=43  T=0 F=15  plan.has_frac = plan.frac_mask || (plan.numr_mask && plan...
  d=1   L 130  T=1 F=42  T=1 F=14  bool disable_gpos = plan.shaper->gpos_tag &&
  d=1   L 137  T=43 F=0  T=15 F=0  if (!hb_ot_layout_has_glyph_classes (face))
  d=1   L 154  T=43 F=0  T=15 F=0  bool has_gsub = !apply_morx && hb_ot_layout_has_substitut...
  d=1   L 154  T=0 F=43  T=0 F=15  bool has_gsub = !apply_morx && hb_ot_layout_has_substitut...
  d=1   L 156  T=42 F=1  T=14 F=1  bool has_gpos = !disable_gpos && hb_ot_layout_has_positio...
  d=1   L 156  T=0 F=42  T=0 F=14  bool has_gpos = !disable_gpos && hb_ot_layout_has_positio...
  d=1   L 162  T=0 F=43  T=0 F=15  else if (has_kerx && !(has_gsub && has_gpos))
  d=1   L 165  T=0 F=43  T=0 F=15  else if (has_gpos)
  d=1   L 168  T=43 F=0  T=15 F=0  if (!plan.apply_kerx && (!has_gpos_kern || !plan.apply_gp...
  d=1   L 168  T=43 F=0  T=15 F=0  if (!plan.apply_kerx && (!has_gpos_kern || !plan.apply_gp...
  d=1   L 171  T=0 F=43  T=0 F=15  if (has_kerx)
  d=1   L 176  T=43 F=0  T=15 F=0  if (hb_ot_layout_has_kerning (face))
  d=1   L 181  T=0 F=43  T=0 F=15  plan.apply_fallback_kern = !(plan.apply_gpos || plan.appl...
  d=1   L 181  T=43 F=0  T=15 F=0  plan.apply_fallback_kern = !(plan.apply_gpos || plan.appl...
  d=1   L 181  T=0 F=43  T=0 F=15  plan.apply_fallback_kern = !(plan.apply_gpos || plan.appl...
  d=1   L 183  T=40 F=3  T=14 F=1  plan.zero_marks = script_zero_marks &&
  d=1   L 184  T=40 F=0  T=14 F=0  !plan.apply_kerx &&
  d=1   L 185  T=0 F=40  T=0 F=14  (!plan.apply_kern
  d=1   L 187  T=0 F=40  T=14 F=0  || !hb_ot_layout_has_machine_kerning (face)  <-- BLOCKER
  d=1   L 192  T=43 F=0  T=15 F=0  plan.adjust_mark_positioning_when_zeroing = !plan.apply_g...
  d=1   L 193  T=43 F=0  T=15 F=0  !plan.apply_kerx &&
  d=1   L 194  T=0 F=43  T=0 F=15  (!plan.apply_kern
  d=1   L 196  T=21 F=22  T=15 F=0  || !hb_ot_layout_has_cross_kerning (face)
  d=1   L 200  T=21 F=22  T=15 F=0  plan.fallback_mark_positioning = plan.adjust_mark_positio...
  d=1   L 207  T=0 F=43  T=0 F=15  if (plan.apply_morx)
  d=1   L 211  T=0 F=34  T=0 F=14  plan.apply_trak = plan.requested_tracking && hb_aat_layou...
  d=1   L 211  T=34 F=9  T=14 F=1  plan.apply_trak = plan.requested_tracking && hb_aat_layou...

[off-chain: 74 additional divergent branches across 23 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=9c4c9afb9e3f0195, size=44 bytes, fuzzer=minimizer, trial=1, discovered_at=353s, mutation_op=TokenInsert,CrossoverReplaceMutator,ByteNegMutator):
  0000: 00 01 00 00 00 01 46 20 20 20 28 f6 6b 65 72 6e   ......F   (.kern
  0010: 00 00 00 01 00 00 00 10 01 7f 00 00 20 20 20 20   ............    
  0020: ff 0b 20 1a 20 20 70 67 6c 68 20 20               .. .  pglh  
Seed 2 (id=ca0d414591d32759, size=66 bytes, fuzzer=minimizer, trial=1, discovered_at=2313s, mutation_op=ByteNegMutator,BytesExpandMutator,DwordAddMutator,ByteDecMutator):
  0000: 00 01 00 00 00 01 46 20 24 0b 28 0a 6b 65 72 6e   ......F $.(.kern
  0010: 00 00 00 01 00 00 00 10 01 eb 00 21 00 00 00 00   ...........!....
  0020: 00 01 00 61 68 20 20 ff 00 01 46 e0 20 0b 28 0a   ...ah  ...F. .(.
  0030: 6b 65 72 6e 00 00 00 21 04 00 6e 00 00 00 21 04   kern...!..n...!.
Seed 3 (id=9c4c75cb9e2dc098, size=121 bytes, fuzzer=minimizer, trial=1, discovered_at=3236s, mutation_op=BytesInsertMutator):
  0000: 00 01 00 00 00 03 e8 20 20 20 28 f6 6b 65 72 6e   .......   (.kern
  0010: 00 00 00 02 00 00 00 10 01 89 00 00 e7 65 72 6e   .............ern
  0020: 00 00 00 02 00 00 00 10 00 7f 00 00 00 6f 6d 6a   .............omj
  0030: 74 00 ff 20 02 40 00 01 70 00 00 16 0f 2c 10 00   t.. .@..p....,..
Seed 4 (id=48a6949a560a36e8, size=104 bytes, fuzzer=minimizer, trial=1, discovered_at=3648s, mutation_op=TokenReplace,BytesSwapMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 02 46 20 20 b2 28 e5 6b 65 72 6e   ......F  .(.kern
  0010: 00 00 00 01 00 00 00 10 01 00 00 64 00 f8 1f 35   ...........d...5
  0020: 20 4d 77 cd 08 00 00 00 30 80 00 00 1b 09 00 00    Mw.....0.......
  0030: 30 00 00 00 00 00 00 c5 00 7f 76 00 f8 00 ab 0a   0.........v.....
Seed 5 (id=4b9de3b89a809d48, size=104 bytes, fuzzer=minimizer, trial=1, discovered_at=4049s, mutation_op=ByteFlipMutator,BytesRandSetMutator,BytesDeleteMutator,CrossoverReplaceMutator,ByteNegMutator,ByteInterestingMutator,QwordAddMutator):
  0000: 00 01 00 00 00 03 e8 20 20 20 28 f6 6b 65 72 6e   .......   (.kern
  0010: 00 00 00 02 00 00 00 10 00 41 00 00 00 65 72 6e   .........A...ern
  0020: ff 00 00 1e 00 00 00 10 01 00 00 00 17 80 00 00   ................
  0030: d9 20 00 00 00 f9 00 00 18 1f f2 00 e8 20 00 00   . ........... ..

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=d1945e96aad02f88, size=55 bytes, fuzzer=naive, trial=1, discovered_at=1068s, mutation_op=BytesExpandMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 6b 65 72 6e   ......      kern
  0010: 20 20 20 20 00 00 00 1a 20 20 20 20 20 20 20 00       ....       .
  0020: 00 00 20 20 00 00 00 1a 20 20 20 20 20 20 20 00   ..  ....       .
  0030: 00 00 1a 20 20 20 20                              ...    
Seed 2 (id=ff0804a1c59d4fe3, size=121 bytes, fuzzer=naive, trial=1, discovered_at=7971s, mutation_op=BytesSetMutator,TokenInsert):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 6b 65 72 6e   ......      kern
  0010: 20 20 05 00 00 00 00 01 20 20 20 20 20 20 2d 68     ......      -h
  0020: 61 6b 00 6b 65 72 6e 20 20 05 00 00 cb c5 e2 e0   ak.kern  .......
  0030: cc 0f 2d 6d 6f 00 1a 06 00 1e fa 02 00 6e 06 00   ..-mo........n..
Seed 3 (id=ea94d68c898648ce, size=144 bytes, fuzzer=naive, trial=1, discovered_at=8237s, mutation_op=ByteDecMutator,ByteNegMutator,ByteFlipMutator,DwordInterestingMutator,TokenInsert):
  0000: 00 01 00 00 00 01 20 20 20 20 20 e0 6b 65 72 6e   ......     .kern
  0010: 20 21 05 00 00 00 00 01 20 20 20 20 20 20 2d 68    !......      -h
  0020: 61 6b 00 6b 65 72 6e 20 20 05 00 00 cb c5 e2 e0   ak.kern  .......
  0030: cc 00 00 03 e8 00 1a 06 00 1e fa 02 00 6e 06 00   .............n..
Seed 4 (id=31d7eac26290c7f0, size=104 bytes, fuzzer=naive, trial=1, discovered_at=14202s, mutation_op=ByteIncMutator):
  0000: 00 01 00 00 00 02 20 20 20 7f 20 20 6b 65 72 6e   ......   .  kern
  0010: 20 20 05 00 00 00 00 01 20 20 20 20 20 20 6b 65     ......      ke
  0020: 72 6e 20 20 05 00 00 cb c5 e2 e0 cc 0f 2d 6d 6f   rn  .........-mo
  0030: 00 1a 06 00 1e fa 02 00 6e 06 00 00 64 0e 00 fd   ........n...d...
Seed 5 (id=c9c6660ddf7bf7c8, size=115 bytes, fuzzer=naive, trial=1, discovered_at=35885s, mutation_op=ByteNegMutator,BytesDeleteMutator,QwordAddMutator,WordAddMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 6b 65 72 6e   ......      kern
  0010: 20 20 05 00 00 00 00 01 20 20 20 20 20 20 6b 65     ......      ke
  0020: 72 6e 20 20 05 00 00 cb c5 e2 e0 cc 0f 2d 6d 6f   rn  .........-mo
  0030: 00 1a 06 00 1e fa fe 00 6e 06 00 00 64 0e 00 fd   ........n...d...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  01(.)x8 04(.)x7 03(.)x5 02(.)x1     01(.)x6 02(.)x1                     PARTIAL
   0x0006  20( )x10 e8(.)x5 46(F)x3 30(0)x3    20( )x7                             PARTIAL
   0x0007  20( )x11 21(!)x7 00(.)x3            20( )x7                             PARTIAL
   0x0008  20( )x12 81(.)x3 00(.)x3 1d(.)x2 +1u  20( )x7                             PARTIAL
   0x0009  20( )x13 f7(.)x3 00(.)x3 0b(.)x1 +1u  20( )x6 7f(.)x1                     PARTIAL
   0x000a  28(()x8 01(.)x7 20( )x3 10(.)x3     20( )x7                             PARTIAL
   0x000b  17(.)x7 f6(.)x6 20( )x6 0a(.)x1 +1u  20( )x6 e0(.)x1                     PARTIAL
   0x0010  00(.)x8 22(")x8 bb(.)x3 dd(.)x2     20( )x7                             DIFFER
   0x0011  00(.)x8 df(.)x7 20( )x6             20( )x5 21(!)x2                     PARTIAL
   0x0012  20( )x13 00(.)x8                    05(.)x6 20( )x1                     PARTIAL
   0x0013  e0(.)x7 01(.)x3 df(.)x3 20( )x3 +3u  00(.)x6 20( )x1                     PARTIAL
   0x0017  10(.)x8 35(5)x7 1a(.)x3 20( )x3     01(.)x5 1a(.)x1 6b(k)x1             PARTIAL
   0x0018  01(.)x7 35(5)x7 00(.)x5 6a(j)x2     20( )x6 61(a)x1                     DIFFER
   0x0019  35(5)x6 01(.)x3 ff(.)x3 7f(.)x2 +6u  20( )x6 72(r)x1                     DIFFER
   0x001a  00(.)x9 35(5)x7 ff(.)x3 2d(-)x2     20( )x6 74(t)x1                     DIFFER
   0x001b  00(.)x8 35(5)x7 ff(.)x3 21(!)x1 +2u  20( )x6 01(.)x1                     PARTIAL
   0x001c  00(.)x10 35(5)x6 fe(.)x3 20( )x1 +1u  20( )x7                             PARTIAL
   0x001d  00(.)x6 35(5)x6 65(e)x4 01(.)x2 +3u  20( )x7                             PARTIAL
   0x001e  fe(.)x6 00(.)x5 72(r)x4 01(.)x3 +3u  2d(-)x3 20( )x2 6b(k)x2             PARTIAL
   0x001f  00(.)x9 ff(.)x5 6e(n)x4 20( )x1 +2u  68(h)x3 65(e)x2 00(.)x1 20( )x1     PARTIAL
   0x0020  00(.)x11 ff(.)x8 20( )x1 06(.)x1    61(a)x3 72(r)x2 00(.)x1 20( )x1     PARTIAL
   0x0021  00(.)x8 ff(.)x4 01(.)x2 1a(.)x2 +4u  6e(n)x3 6b(k)x2 00(.)x1 20( )x1     PARTIAL
   0x0022  00(.)x10 7f(.)x4 01(.)x2 80(.)x2 +3u  20( )x3 00(.)x2 6b(k)x1 0c(.)x1     PARTIAL
   0x0023  00(.)x7 02(.)x4 04(.)x3 01(.)x2 +5u  20( )x3 6b(k)x2 65(e)x1 ff(.)x1     DIFFER
   0x0025  00(.)x17 20( )x2 01(.)x1 1a(.)x1    00(.)x4 72(r)x2 6b(k)x1             PARTIAL
   0x0026  00(.)x17 01(.)x2 70(p)x1 20( )x1    00(.)x4 6e(n)x2 6b(k)x1             PARTIAL
   0x0027  10(.)x8 00(.)x8 01(.)x3 67(g)x1 +1u  cb(.)x3 20( )x2 1a(.)x1 6b(k)x1     DIFFER
   0x0028  00(.)x13 20( )x4 01(.)x2 6c(l)x1 +1u  20( )x3 c5(.)x2 6b(k)x1 02(.)x1     PARTIAL
   0x002f  00(.)x5 7f(.)x5 2c(,)x3 5b([)x3 +4u  00(.)x2 e0(.)x2 6f(o)x2 6b(k)x1     PARTIAL
   0x0030  00(.)x8 10(.)x3 1a(.)x3 6b(k)x1 +5u  00(.)x3 cc(.)x2 6b(k)x1 0a(.)x1     PARTIAL
   0x0035  00(.)x14 20( )x3 40(@)x1 f9(.)x1 +1u  00(.)x3 20( )x2 fa(.)x2             PARTIAL
   0x0036  00(.)x18 0d(.)x1 07(.)x1            20( )x2 1a(.)x2 02(.)x1 fe(.)x1 +1u  PARTIAL
   0x0037  00(.)x10 20( )x4 10(.)x3 21(!)x1 +2u  06(.)x2 00(.)x2 05(.)x1 48(H)x1     PARTIAL
   0x0038  01(.)x12 00(.)x3 04(.)x1 70(p)x1 +3u  00(.)x3 6e(n)x2 92(.)x1             PARTIAL
   0x0039  00(.)x11 7f(.)x4 30(0)x3 1f(.)x1 +1u  1e(.)x2 06(.)x2 00(.)x1 0e(.)x1     PARTIAL
   0x003a  00(.)x15 6e(n)x1 76(v)x1 f2(.)x1 +2u  fa(.)x2 00(.)x2 cb(.)x1 ff(.)x1     PARTIAL
   0x003b  00(.)x14 68(h)x3 16(.)x1 13(.)x1 +1u  02(.)x2 00(.)x2 c5(.)x1 0e(.)x1     PARTIAL
   0x003c  14(.)x7 00(.)x5 2d(-)x3 20( )x2 +3u  00(.)x3 64(d)x2 e2(.)x1             PARTIAL
   0x003d  01(.)x7 6f(o)x3 68(h)x3 00(.)x2 +4u  6e(n)x2 0e(.)x2 e0(.)x1 00(.)x1     PARTIAL
   0x003e  1e(.)x4 00(.)x3 0f(.)x3 61(a)x3 +6u  06(.)x2 00(.)x2 80(.)x1 cb(.)x1     PARTIAL
   ... (1 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- minimizer ---
**Instrumentation**: naive's edge counters only.

**Feedback**: naive's edge-bucket `MaxMapFeedback`, plus a
`CalibrationStage` that measures each new corpus entry's execution
time, edge-map fill, and stability into `SchedulerMetadata`/testcase
metadata.

**Mutators / stages**: havoc + token mutator (`LineageMutator`, names
captured) run inside a `StdPowerMutationalStage` rather than naive's
plain `StdMutationalStage`. Stages are `[calibration, power]`. The
power stage derives the number of havoc mutations per seed visit (the
"energy") from a calibration-based `perf_score` — faster, smaller,
more-stable seeds earn more mutations. PowerSchedule is `None`, so the
energy uses ONLY intrinsic calibration and is NOT weighted by how often
a region has been hit. Corpus selection is plain FIFO `QueueScheduler`
(same order as naive).

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge, plus a one-time
calibration burst per new corpus entry.

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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5708.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5708,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile), naive_ctx>naive (ctx_coverage), minimizer>naive (calibrated_energy)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5708 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5708 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5708 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).