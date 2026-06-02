==== BLOCKER ====
Target: harfbuzz
Branch ID: 5697
Location: /src/harfbuzz/src/hb-ot-shape.cc:156:36
Enclosing function: hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&)
Source line:   bool has_gpos = !disable_gpos && hb_ot_layout_has_positioning (face);
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
  avg duration blocked: winner=0.30h  loser=24.00h
  avg hitcount on branch: winner=3430  loser=0
  prob_div=1.00  dur_div=23.70h  hit_div=3430
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.00h  loser=24.00h
  avg hitcount on branch: winner=2345  loser=0
  prob_div=1.00  dur_div=24.00h  hit_div=2345
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5697/{W,L}/branch_coverage_show.txt

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
[B]   156    bool has_gpos = !disable_gpos && hb_ot_layout_has_positioning (face); <-- BLOCKER
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
[L]   195  #ifndef HB_NO_OT_KERN
[L]   196  					       || !hb_ot_layout_has_cross_kerning (face)
[L]   197  #endif
[L]   198  					      );
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
[L]   231    {
[L]   232      data = shaper->data_create (this);
[L]   233      if (unlikely (!data))
[ ]   234      {
[ ]   235        map.fini ();
[ ]   236        return false;
[ ]   237      }
[L]   238    }
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
       0        30  hb-ot-shape.cc:zero_mark_width(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:967-970)
       0         9  hb-ot-shape.cc:adjust_mark_offsets(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:960-963)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195) ---
  d=5   L1177  T=0 F=322  T=7 F=374  if (c->plan->shaper->preprocess_text &&
  d=5   L1178  T=0 F=0  T=7 F=0  c->buffer->message(c->font, "start preprocess-text"))
--- d=2  hb_ot_shape_plan_t::init0(hb_face_t*, hb_shape_plan_key_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:218-241) ---
  d=2   L 230  T=0 F=20  T=13 F=23  if (shaper->data_create)
--- d=1  hb_ot_shape_planner_t::compile(hb_ot_shape_plan_t&, hb_ot_shape_plan_key_t const&)  (/src/harfbuzz/src/hb-ot-shape.cc:103-213) ---
  d=1   L 130  T=0 F=20  T=1 F=35  bool disable_gpos = plan.shaper->gpos_tag &&
  d=1   L 131  T=0 F=0  T=1 F=0  plan.shaper->gpos_tag != plan.map.chosen_script[1];
  d=1   L 156  T=20 F=0  T=35 F=1  bool has_gpos = !disable_gpos && hb_ot_layout_has_positio...  <-- BLOCKER
  d=1   L 156  T=20 F=0  T=0 F=35  bool has_gpos = !disable_gpos && hb_ot_layout_has_positio...  <-- BLOCKER
  d=1   L 165  T=20 F=0  T=0 F=36  else if (has_gpos)
  d=1   L 181  T=20 F=0  T=0 F=36  plan.apply_fallback_kern = !(plan.apply_gpos || plan.appl...
  d=1   L 181  T=0 F=0  T=0 F=36  plan.apply_fallback_kern = !(plan.apply_gpos || plan.appl...
  d=1   L 181  T=0 F=0  T=0 F=36  plan.apply_fallback_kern = !(plan.apply_gpos || plan.appl...
  d=1   L 183  T=20 F=0  T=30 F=6  plan.zero_marks = script_zero_marks &&
  d=1   L 192  T=0 F=20  T=36 F=0  plan.adjust_mark_positioning_when_zeroing = !plan.apply_g...
  d=1   L 193  T=0 F=0  T=36 F=0  !plan.apply_kerx &&
  d=1   L 194  T=0 F=0  T=36 F=0  (!plan.apply_kern
  d=1   L 200  T=0 F=20  T=36 F=0  plan.fallback_mark_positioning = plan.adjust_mark_positio...
  d=1   L 201  T=0 F=0  T=26 F=10  script_fallback_mark_positioning;
  d=1   L 211  T=19 F=1  T=36 F=0  plan.apply_trak = plan.requested_tracking && hb_aat_layou...

[off-chain: 39 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0046235e61b8f998, size=294 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1849s, mutation_op=BytesCopyMutator,ByteNegMutator,TokenReplace,BytesInsertCopyMutator,CrossoverReplaceMutator,DwordAddMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 20 ff 1f 5c 00 00 00 18 00 01 00 0a 20 ff ff 00    ..\........ ...
  0020: 00 02 00 12 12 12 14 00 00 20 00 00 00 04 00 00   ......... ......
  0030: 00 20 20 20 20 20 20 ff ff ff ff 20 6b 65 f2 8c   .      .... ke..
Seed 2 (id=002c9ad92acce91b, size=171 bytes, fuzzer=cmplog, trial=1, discovered_at=2579s, mutation_op=BytesInsertMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 01 20 19 21 20 20 20 47 50 4f 53   ...... .!   GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 50 4f 00 00   ...........GPO..
  0020: 10 00 01 01 04 53 00 01 00 0d 00 14 01 ff fb 13   .....S..........
  0030: 72 f9 f0 01 4f 53 03 03 00 04 00 1a 43 22 55 41   r...OS......C"UA
Seed 3 (id=003bfa8ebe690138, size=144 bytes, fuzzer=cmplog, trial=1, discovered_at=2770s, mutation_op=BytesInsertCopyMutator,TokenReplace,WordInterestingMutator,TokenInsert):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 03 01 0c 00   ...........G....
  0020: 00 00 00 07 4f 00 00 10 ff 7a 68 2d 68 61 6e 74   ....O....zh-hant
  0030: 00 00 00 02 00 44 00 10 00 ff ff ff 3f 0d 02 00   .....D......?...
Seed 4 (id=002e1500bcab55a2, size=174 bytes, fuzzer=cmplog, trial=1, discovered_at=3377s, mutation_op=BytesCopyMutator,ByteAddMutator):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 00 00 00 03   ...........G....
  0020: ff de 00 02 4f 00 00 10 00 01 00 10 00 06 00 06   ....O...........
  0030: 00 10 00 01 00 00 00 06 00 06 03 00 1d 00 e9 ff   ................
Seed 5 (id=005a8baafbd526f7, size=189 bytes, fuzzer=cmplog, trial=1, discovered_at=3630s, mutation_op=ByteNegMutator,BytesRandInsertMutator,BitFlipMutator):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 00 00 00 03   ...........G....
  0020: 01 00 00 02 4f 00 00 10 00 01 00 10 00 00 00 00   ....O...........
  0030: 00 01 00 00 00 00 00 00 10 01 00 10 00 06 00 06   ................

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
   0x0000  00(.)x20                            00(.)x4 e0(.)x2 05(.)x2 87(.)x1 +11u  PARTIAL
   0x0001  01(.)x20                            00(.)x3 0e(.)x2 ff(.)x2 07(.)x2 +11u  PARTIAL
   0x0002  00(.)x20                            00(.)x10 ff(.)x3 0d(.)x1 0e(.)x1 +5u  PARTIAL
   0x0003  00(.)x20                            00(.)x11 ff(.)x2 2d(-)x2 0e(.)x1 +4u  PARTIAL
   0x0004  00(.)x20                            00(.)x2 df(.)x2 68(h)x2 70(p)x2 +12u  PARTIAL
   0x0005  01(.)x13 02(.)x6 04(.)x1            00(.)x4 20( )x4 0e(.)x3 06(.)x2 +7u  PARTIAL
   0x0006  07(.)x7 20( )x6 ee(.)x6 ff(.)x1     00(.)x12 e0(.)x1 68(h)x1 e5(.)x1 +4u  PARTIAL
   0x0007  20( )x13 ff(.)x5 19(.)x1 01(.)x1    00(.)x11 e0(.)x1 55(U)x1 77(w)x1 +5u  PARTIAL
   0x0008  21(!)x9 00(.)x6 20( )x4 a1(.)x1     00(.)x4 20( )x2 29())x1 e0(.)x1 +11u  PARTIAL
   0x0009  20( )x14 30(0)x6                    00(.)x3 0a(.)x2 2b(+)x1 17(.)x1 +12u  PARTIAL
   0x000b  20( )x19 32(2)x1                    00(.)x12 29())x1 13(.)x1 75(u)x1 +4u  DIFFER
   0x000c  47(G)x20                            00(.)x3 01(.)x2 20( )x2 2c(,)x1 +11u  DIFFER
   0x000d  50(P)x20                            20( )x4 00(.)x4 18(.)x1 17(.)x1 +8u  DIFFER
   0x000e  4f(O)x20                            00(.)x5 e0(.)x1 64(d)x1 18(.)x1 +10u  DIFFER
   0x000f  53(S)x20                            00(.)x5 6a(j)x1 6f(o)x1 fa(.)x1 +10u  DIFFER
   0x0010  00(.)x10 20( )x9 01(.)x1            00(.)x5 20( )x2 79(y)x1 2d(-)x1 +9u  PARTIAL
   0x0011  01(.)x10 20( )x6 ff(.)x4            20( )x4 00(.)x2 06(.)x2 2d(-)x1 +9u  PARTIAL
   0x0012  00(.)x10 20( )x6 1e(.)x3 1f(.)x1    00(.)x8 68(h)x1 0a(.)x1 18(.)x1 +7u  PARTIAL
   0x0014  00(.)x20                            68(h)x3 00(.)x2 6e(n)x1 74(t)x1 +11u  PARTIAL
   0x0015  00(.)x20                            00(.)x4 06(.)x2 74(t)x1 17(.)x1 +10u  PARTIAL
   0x0016  00(.)x20                            00(.)x8 01(.)x2 2d(-)x1 0e(.)x1 +6u  PARTIAL
   0x0017  10(.)x10 00(.)x6 18(.)x4            00(.)x7 74(t)x2 68(h)x1 3d(=)x1 +6u  PARTIAL
   0x0018  00(.)x15 ff(.)x4 f6(.)x1            20( )x4 00(.)x3 6b(k)x1 61(a)x1 +8u  PARTIAL
   0x0019  02(.)x10 ff(.)x6 01(.)x4            00(.)x3 20( )x3 9f(.)x2 19(.)x2 +7u  PARTIAL
   0x0028  00(.)x12 18(.)x5 20( )x2 ff(.)x1    00(.)x4 01(.)x1 20( )x1 02(.)x1 +6u  PARTIAL
   0x0030  00(.)x18 72(r)x1 76(v)x1            00(.)x2 2c(,)x1 fe(.)x1 01(.)x1 +7u  PARTIAL
   0x003e  00(.)x12 f2(.)x1 55(U)x1 02(.)x1 +5u  00(.)x4 9f(.)x1 20( )x1 01(.)x1     PARTIAL
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
  prompts_b/harfbuzz_5697.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5697,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5697 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5697 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5697 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).