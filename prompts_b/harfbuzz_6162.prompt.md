==== BLOCKER ====
Target: harfbuzz
Branch ID: 6162
Location: /src/harfbuzz/src/hb-ot-shaper.hh:300:5
Enclosing function: hb-ot-shape-normalize.cc:hb_ot_shaper_categorize(hb_ot_shape_planner_t const*)
Source line:     case HB_SCRIPT_PHAGS_PA:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  REFERENCE
cmplog                           3        7          0  REFERENCE
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             1        9          0  loser (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=1.40h  loser=21.80h
  avg hitcount on branch: winner=34  loser=0
  prob_div=0.90  dur_div=20.40h  hit_div=33
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/6162/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shape-normalize.cc:hb_ot_shaper_categorize(hb_ot_shape_planner_t const*) (/src/harfbuzz/src/hb-ot-shaper.hh:178-400) ---
[ ]   176  static inline const hb_ot_shaper_t *
[ ]   177  hb_ot_shaper_categorize (const hb_ot_shape_planner_t *planner)
[B]   178  {
[B]   179    switch ((hb_tag_t) planner->props.script)
[B]   180    {
[B]   181      default:
[B]   182        return &_hb_ot_shaper_default;
[ ]   183  
[ ]   184  
[ ]   185      /* Unicode-1.1 additions */
[ ]   186      case HB_SCRIPT_ARABIC:
[ ]   187  
[ ]   188      /* Unicode-3.0 additions */
[ ]   189      case HB_SCRIPT_SYRIAC:
[ ]   190  
[ ]   191        /* For Arabic script, use the Arabic shaper even if no OT script tag was found.
[ ]   192         * This is because we do fallback shaping for Arabic script (and not others).
[ ]   193         * But note that Arabic shaping is applicable only to horizontal layout; for
[ ]   194         * vertical text, just use the generic shaper instead. */
[ ]   195        if ((planner->map.chosen_script[0] != HB_OT_TAG_DEFAULT_SCRIPT ||
[ ]   196  	   planner->props.script == HB_SCRIPT_ARABIC) &&
[ ]   197  	  HB_DIRECTION_IS_HORIZONTAL(planner->props.direction))
[ ]   198  	return &_hb_ot_shaper_arabic;
[ ]   199        else
[ ]   200  	return &_hb_ot_shaper_default;
[ ]   201  
[ ]   202  
[ ]   203      /* Unicode-1.1 additions */
[ ]   204      case HB_SCRIPT_THAI:
[ ]   205      case HB_SCRIPT_LAO:
[ ]   206  
[ ]   207        return &_hb_ot_shaper_thai;
[ ]   208  
[ ]   209  
[ ]   210      /* Unicode-1.1 additions */
[ ]   211      case HB_SCRIPT_HANGUL:
[ ]   212  
[ ]   213        return &_hb_ot_shaper_hangul;
[ ]   214  
[ ]   215  
[ ]   216      /* Unicode-1.1 additions */
[ ]   217      case HB_SCRIPT_HEBREW:
[ ]   218  
[ ]   219        return &_hb_ot_shaper_hebrew;
[ ]   220  
[ ]   221  
[ ]   222      /* Unicode-1.1 additions */
[ ]   223      case HB_SCRIPT_BENGALI:
[ ]   224      case HB_SCRIPT_DEVANAGARI:
[ ]   225      case HB_SCRIPT_GUJARATI:
[ ]   226      case HB_SCRIPT_GURMUKHI:
[ ]   227      case HB_SCRIPT_KANNADA:
[ ]   228      case HB_SCRIPT_MALAYALAM:
[ ]   229      case HB_SCRIPT_ORIYA:
[ ]   230      case HB_SCRIPT_TAMIL:
[L]   231      case HB_SCRIPT_TELUGU:
[ ]   232  
[ ]   233        /* If the designer designed the font for the 'DFLT' script,
[ ]   234         * (or we ended up arbitrarily pick 'latn'), use the default shaper.
[ ]   235         * Otherwise, use the specific shaper.
[ ]   236         *
[ ]   237         * If it's indy3 tag, send to USE. */
[L]   238        if (planner->map.chosen_script[0] == HB_TAG ('D','F','L','T') ||
[L]   239  	  planner->map.chosen_script[0] == HB_TAG ('l','a','t','n'))
[ ]   240  	return &_hb_ot_shaper_default;
[L]   241        else if ((planner->map.chosen_script[0] & 0x000000FF) == '3')
[ ]   242  	return &_hb_ot_shaper_use;
[L]   243        else
[L]   244  	return &_hb_ot_shaper_indic;
[ ]   245  
[ ]   246      case HB_SCRIPT_KHMER:
[ ]   247  	return &_hb_ot_shaper_khmer;
[ ]   248  
[L]   249      case HB_SCRIPT_MYANMAR:
[ ]   250        /* If the designer designed the font for the 'DFLT' script,
[ ]   251         * (or we ended up arbitrarily pick 'latn'), use the default shaper.
[ ]   252         * Otherwise, use the specific shaper.
[ ]   253         *
[ ]   254         * If designer designed for 'mymr' tag, also send to default
[ ]   255         * shaper.  That's tag used from before Myanmar shaping spec
[ ]   256         * was developed.  The shaping spec uses 'mym2' tag. */
[L]   257        if (planner->map.chosen_script[0] == HB_TAG ('D','F','L','T') ||
[L]   258  	  planner->map.chosen_script[0] == HB_TAG ('l','a','t','n') ||
[L]   259  	  planner->map.chosen_script[0] == HB_TAG ('m','y','m','r'))
[ ]   260  	return &_hb_ot_shaper_default;
[L]   261        else
[L]   262  	return &_hb_ot_shaper_myanmar;
[ ]   263  
[ ]   264  
[ ]   265  #ifndef HB_NO_OT_SHAPER_MYANMAR_ZAWGYI
[ ]   266  #define HB_SCRIPT_MYANMAR_ZAWGYI	((hb_script_t) HB_TAG ('Q','a','a','g'))
[ ]   267      case HB_SCRIPT_MYANMAR_ZAWGYI:
[ ]   268      /* https://github.com/harfbuzz/harfbuzz/issues/1162 */
[ ]   269  
[ ]   270        return &_hb_ot_shaper_myanmar_zawgyi;
[ ]   271  #endif
[ ]   272  
[ ]   273  
[ ]   274      /* Unicode-2.0 additions */
[ ]   275      case HB_SCRIPT_TIBETAN:
[ ]   276  
[ ]   277      /* Unicode-3.0 additions */
[ ]   278      case HB_SCRIPT_MONGOLIAN:
[ ]   279      case HB_SCRIPT_SINHALA:
[ ]   280  
[ ]   281      /* Unicode-3.2 additions */
[ ]   282      case HB_SCRIPT_BUHID:
[ ]   283      case HB_SCRIPT_HANUNOO:
[ ]   284      case HB_SCRIPT_TAGALOG:
[ ]   285      case HB_SCRIPT_TAGBANWA:
[ ]   286  
[ ]   287      /* Unicode-4.0 additions */
[ ]   288      case HB_SCRIPT_LIMBU:
[ ]   289      case HB_SCRIPT_TAI_LE:
[ ]   290  
[ ]   291      /* Unicode-4.1 additions */
[ ]   292      case HB_SCRIPT_BUGINESE:
[ ]   293      case HB_SCRIPT_KHAROSHTHI:
[ ]   294      case HB_SCRIPT_SYLOTI_NAGRI:
[ ]   295      case HB_SCRIPT_TIFINAGH:
[ ]   296  
[ ]   297      /* Unicode-5.0 additions */
[ ]   298      case HB_SCRIPT_BALINESE:
[ ]   299      case HB_SCRIPT_NKO:
[W]   300      case HB_SCRIPT_PHAGS_PA: <-- BLOCKER
[ ]   301  
[ ]   302      /* Unicode-5.1 additions */
[W]   303      case HB_SCRIPT_CHAM:
[W]   304      case HB_SCRIPT_KAYAH_LI:
[W]   305      case HB_SCRIPT_LEPCHA:
[W]   306      case HB_SCRIPT_REJANG:
[W]   307      case HB_SCRIPT_SAURASHTRA:
[W]   308      case HB_SCRIPT_SUNDANESE:
[ ]   309  
[ ]   310      /* Unicode-5.2 additions */
[W]   311      case HB_SCRIPT_EGYPTIAN_HIEROGLYPHS:
[W]   312      case HB_SCRIPT_JAVANESE:
[W]   313      case HB_SCRIPT_KAITHI:
[W]   314      case HB_SCRIPT_MEETEI_MAYEK:
[W]   315      case HB_SCRIPT_TAI_THAM:
[W]   316      case HB_SCRIPT_TAI_VIET:
[ ]   317  
[ ]   318      /* Unicode-6.0 additions */
[W]   319      case HB_SCRIPT_BATAK:
[W]   320      case HB_SCRIPT_BRAHMI:
[W]   321      case HB_SCRIPT_MANDAIC:
[ ]   322  
[ ]   323      /* Unicode-6.1 additions */
[W]   324      case HB_SCRIPT_CHAKMA:
[W]   325      case HB_SCRIPT_MIAO:
[W]   326      case HB_SCRIPT_SHARADA:
[W]   327      case HB_SCRIPT_TAKRI:
[ ]   328  
[ ]   329      /* Unicode-7.0 additions */
[W]   330      case HB_SCRIPT_DUPLOYAN:
[W]   331      case HB_SCRIPT_GRANTHA:
[W]   332      case HB_SCRIPT_KHOJKI:
[W]   333      case HB_SCRIPT_KHUDAWADI:
[W]   334      case HB_SCRIPT_MAHAJANI:
[W]   335      case HB_SCRIPT_MANICHAEAN:
[W]   336      case HB_SCRIPT_MODI:
[W]   337      case HB_SCRIPT_PAHAWH_HMONG:
[W]   338      case HB_SCRIPT_PSALTER_PAHLAVI:
[W]   339      case HB_SCRIPT_SIDDHAM:
[W]   340      case HB_SCRIPT_TIRHUTA:
[ ]   341  
[ ]   342      /* Unicode-8.0 additions */
[W]   343      case HB_SCRIPT_AHOM:
[W]   344      case HB_SCRIPT_MULTANI:
[ ]   345  
[ ]   346      /* Unicode-9.0 additions */
[W]   347      case HB_SCRIPT_ADLAM:
[W]   348      case HB_SCRIPT_BHAIKSUKI:
[W]   349      case HB_SCRIPT_MARCHEN:
[W]   350      case HB_SCRIPT_NEWA:
[ ]   351  
[ ]   352      /* Unicode-10.0 additions */
[W]   353      case HB_SCRIPT_MASARAM_GONDI:
[W]   354      case HB_SCRIPT_SOYOMBO:
[W]   355      case HB_SCRIPT_ZANABAZAR_SQUARE:
[ ]   356  
[ ]   357      /* Unicode-11.0 additions */
[W]   358      case HB_SCRIPT_DOGRA:
[W]   359      case HB_SCRIPT_GUNJALA_GONDI:
[W]   360      case HB_SCRIPT_HANIFI_ROHINGYA:
[W]   361      case HB_SCRIPT_MAKASAR:
[W]   362      case HB_SCRIPT_MEDEFAIDRIN:
[W]   363      case HB_SCRIPT_OLD_SOGDIAN:
[W]   364      case HB_SCRIPT_SOGDIAN:
[ ]   365  
[ ]   366      /* Unicode-12.0 additions */
[W]   367      case HB_SCRIPT_ELYMAIC:
[W]   368      case HB_SCRIPT_NANDINAGARI:
[W]   369      case HB_SCRIPT_NYIAKENG_PUACHUE_HMONG:
[W]   370      case HB_SCRIPT_WANCHO:
[ ]   371  
[ ]   372      /* Unicode-13.0 additions */
[W]   373      case HB_SCRIPT_CHORASMIAN:
[W]   374      case HB_SCRIPT_DIVES_AKURU:
[W]   375      case HB_SCRIPT_KHITAN_SMALL_SCRIPT:
[W]   376      case HB_SCRIPT_YEZIDI:
[ ]   377  
[ ]   378      /* Unicode-14.0 additions */
[W]   379      case HB_SCRIPT_CYPRO_MINOAN:
[W]   380      case HB_SCRIPT_OLD_UYGHUR:
[W]   381      case HB_SCRIPT_TANGSA:
[W]   382      case HB_SCRIPT_TOTO:
[W]   383      case HB_SCRIPT_VITHKUQI:
[ ]   384  
[ ]   385      /* Unicode-15.0 additions */
[W]   386      case HB_SCRIPT_KAWI:
[W]   387      case HB_SCRIPT_NAG_MUNDARI:
[ ]   388  
[ ]   389        /* If the designer designed the font for the 'DFLT' script,
[ ]   390         * (or we ended up arbitrarily pick 'latn'), use the default shaper.
[ ]   391         * Otherwise, use the specific shaper.
[ ]   392         * Note that for some simple scripts, there may not be *any*
[ ]   393         * GSUB/GPOS needed, so there may be no scripts found! */
[W]   394        if (planner->map.chosen_script[0] == HB_TAG ('D','F','L','T') ||
[W]   395  	  planner->map.chosen_script[0] == HB_TAG ('l','a','t','n'))
[ ]   396  	return &_hb_ot_shaper_default;
[W]   397        else
[W]   398  	return &_hb_ot_shaper_use;
[B]   399    }
[B]   400  }

--- Caller (1 hop): hb_ot_shape_planner_t::hb_ot_shape_planner_t(hb_face_t*, hb_segment_properties_t const&) (/src/harfbuzz/src/hb-ot-shape.cc:81-98, calls hb-ot-shape-normalize.cc:hb_ot_shaper_categorize(hb_ot_shape_planner_t const*) at line 88) (full body — short) ---
[B]    81  						face (face),
[B]    82  						props (props),
[B]    83  						map (face, props)
[ ]    84  #ifndef HB_NO_AAT_SHAPE
[B]    85  						, apply_morx (_hb_apply_morx (face, props))
[ ]    86  #endif
[B]    87  {
[B]    88    shaper = hb_ot_shaper_categorize (this); <-- CALL
[ ]    89  
[B]    90    script_zero_marks = shaper->zero_width_marks != HB_OT_SHAPE_ZERO_WIDTH_MARKS_NONE;
[B]    91    script_fallback_mark_positioning = shaper->fallback_position;
[ ]    92  
[B]    93  #ifndef HB_NO_AAT_SHAPE
[ ]    94    /* https://github.com/harfbuzz/harfbuzz/issues/1528 */
[B]    95    if (apply_morx && shaper != &_hb_ot_shaper_default)
[ ]    96      shaper = &_hb_ot_shaper_dumber;
[B]    97  #endif
[B]    98  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb_ot_shape_planner_t::hb_ot_shape_planner_t(hb_face_t*, hb_segment_properties_t const&)  (/src/harfbuzz/src/hb-ot-shape.cc:81-98, calls hb-ot-shape-normalize.cc:hb_ot_shaper_categorize(hb_ot_shape_planner_t const*) at line 88)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       4         0  hb-ot-shape.cc:adjust_mark_offsets(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:960-963)
       4         1  hb-ot-shape.cc:zero_mark_width(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:967-970)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
  (no divergent branches in chain functions; the split is off-chain)

[off-chain: 43 additional divergent branches across 10 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=55398e7406161361, size=119 bytes, fuzzer=value_profile, trial=1, discovered_at=277s, mutation_op=CrossoverReplaceMutator,BytesInsertMutator,DwordInterestingMutator,QwordAddMutator,BytesExpandMutator,BytesSwapMutator,ByteDecMutator):
  0000: 20 38 1f 10 00 00 30 20 00 00 01 20 06 64 06 00    8....0 ... .d..
  0010: 64 61 72 66 ff 6e 6e 6e 6e 6e 6e 6e 6e 6e 6e 20   darf.nnnnnnnnnn 
  0020: 20 0b 00 00 00 00 01 0b 06 06 64 06 01 06 06 06    .........d.....
  0030: 64 a8 00 00 00 6e 00 3e 06 64 06 01 06 06 06 64   d....n.>.d.....d
Seed 2 (id=dbcec530f6362dbb, size=104 bytes, fuzzer=value_profile, trial=1, discovered_at=292s, mutation_op=BytesInsertMutator,CrossoverInsertMutator,BytesCopyMutator,CrossoverInsertMutator,BytesExpandMutator,BitFlipMutator):
  0000: 02 01 00 00 00 1a 20 00 1a 00 00 00 00 01 20 06   ...... ....... .
  0010: 06 00 1a 00 00 00 00 01 20 06 06 00 4d 01 20 20   ........ ...M.  
  0020: 20 00 01 0b 06 06 64 06 01 06 06 06 64 a8 00 00    .....d.....d...
  0030: 00 00 00 01 0b 06 07 64 06 1a 20 20 12 01 00 00   .......d..  ....
Seed 3 (id=0e1b2672e1a172e9, size=61 bytes, fuzzer=value_profile, trial=1, discovered_at=1233s, mutation_op=CrossoverReplaceMutator,ByteInterestingMutator,DwordAddMutator,BytesDeleteMutator):
  0000: 64 a8 00 00 00 10 00 00 80 00 e2 ff a8 00 22 00   d.............".
  0010: 00 00 ff ff 74 2d 6d 4c 4c 6d 6e 34 0e 00 00 4d   ....t-mLLmn4...M
  0020: 0e 00 00 4c 0e 00 00 4c f1 0e 0e 34 0e 00 00 10   ...L...L...4....
  0030: 68 2d 68 61 6e 73 00 10 10 dd d0 dd 00            h-hans.......
Seed 4 (id=9eb3a7b97b628c7b, size=38 bytes, fuzzer=value_profile, trial=1, discovered_at=1678s, mutation_op=BytesDeleteMutator,BytesRandSetMutator,ByteAddMutator):
  0000: 06 06 64 a8 eb 00 00 68 2d 6d 69 6e 00 00 4d 01   ..d....h-min..M.
  0010: 20 20 20 00 01 0b 6f 2d a3 a3 a3 a3 a3 a3 a3 a3      ...o-........
  0020: 72 a8 00 00 00 00                                 r.....
Seed 5 (id=a940543bb744d1f3, size=91 bytes, fuzzer=value_profile, trial=1, discovered_at=3648s, mutation_op=DwordAddMutator,QwordAddMutator,DwordInterestingMutator,BytesDeleteMutator):
  0000: 20 38 1f 10 00 00 30 20 00 00 01 20 06 64 06 00    8....0 ... .d..
  0010: 64 61 72 66 ff 6e 56 6e 6e 6e 6e 6e 6e 6e 6e 20   darf.nVnnnnnnnn 
  0020: 20 0b 00 00 00 00 01 0b 06 06 64 06 01 06 fa 00    .........d.....
  0030: 00 fa 00 00 00 6e 00 3e 06 64 06 01 06 06 06 64   .....n.>.d.....d

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=002407bc92172463, size=56 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=869s, mutation_op=ByteDecMutator):
  0000: ff 00 0c 00 02 00 5a 5a 5a 5a 5a 5a 47 0c 00 00   ......ZZZZZZG...
  0010: 47 0c 00 00 00 0c 00 00 00 0c 00 00 11 20 00 00   G............ ..
  0020: 47 0c 0a 00 08 00 08 0c 00 00 5a 00 00 5a 5a 5a   G.........Z..ZZZ
  0030: 47 0c 00 00 47 0c 00 00                           G...G...
Seed 2 (id=00347ed302ef3460, size=125 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1426s, mutation_op=ByteInterestingMutator,ByteInterestingMutator,BytesRandInsertMutator,BytesSwapMutator):
  0000: 00 01 00 00 00 01 ee ff 00 30 00 20 47 53 55 42   .........0. GSUB
  0010: 20 20 20 20 00 00 00 00 00 ff 00 00 00 00 00 0a       ............
  0020: 05 00 18 e0 00 00 ab 42 20 20 20 03 00 00 fd ff   .......B   .....
  0030: 00 1d ff ff ff 03 00 00 00 00 00 00 00 00 00 00   ................
Seed 3 (id=001eeb5a047b00d0, size=188 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2277s, mutation_op=BytesInsertCopyMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 04 00 ff 00 30 00 20 47 53 55 42   .........0. GSUB
  0010: 20 20 20 20 00 00 00 00 00 ff 00 00 00 00 00 0a       ............
  0020: 00 00 18 e0 00 00 ab 42 20 3c 20 00 00 00 fd ff   .......B < .....
  0030: 00 10 00 00 94 02 00 00 1d 43 20 20 28 a0 00 00   .........C  (...
Seed 4 (id=0016080e315935c4, size=210 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4774s, mutation_op=DwordInterestingMutator,BitFlipMutator,QwordAddMutator):
  0000: 00 01 00 00 00 01 ee ff 00 30 00 20 47 50 4f 53   .........0. GPOS
  0010: 20 20 20 20 00 00 00 00 f6 ff 02 00 00 00 00 0a       ............
  0020: 00 01 18 e0 00 00 ab 42 20 3c 20 00 00 00 fd ff   .......B < .....
  0030: 00 10 00 0c 94 01 02 00 1d 43 20 20 28 a0 00 00   .........C  (...
Seed 5 (id=00274477948eb8f0, size=323 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5758s, mutation_op=BytesRandInsertMutator,BytesSwapMutator,ByteIncMutator,ByteNegMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 01 ff 1e 20 00 00 00 18 00 01 00 00 00 01 ee ff   ... ............
  0020: 00 30 06 20 95 53 55 42 20 20 20 20 00 80 00 00   .0. .SUB    ....
  0030: 00 ff 02 4b 00 00 00 0a 00 00 18 e0 00 00 ab 42   ...K...........B


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f2(.)x3 20( )x2 64(d)x2 02(.)x1 +2u  00(.)x9 ff(.)x1                     DIFFER
   0x0001  08(.)x3 38(8)x2 a8(.)x2 01(.)x1 +2u  01(.)x9 00(.)x1                     PARTIAL
   0x0002  00(.)x5 1f(.)x2 64(d)x1 06(.)x1 +1u  00(.)x9 0c(.)x1                     PARTIAL
   0x0003  00(.)x6 10(.)x2 a8(.)x1 06(.)x1     00(.)x10                            PARTIAL
   0x0004  00(.)x7 eb(.)x1 64(d)x1 4c(L)x1     00(.)x9 02(.)x1                     PARTIAL
   0x0005  00(.)x6 1a(.)x1 10(.)x1 06(.)x1 +1u  01(.)x4 02(.)x3 04(.)x2 00(.)x1     PARTIAL
   0x0006  00(.)x5 30(0)x2 01(.)x2 20( )x1     ee(.)x4 20( )x4 5a(Z)x1 00(.)x1     PARTIAL
   0x0007  00(.)x5 20( )x2 68(h)x1 06(.)x1 +1u  ff(.)x5 20( )x4 5a(Z)x1             PARTIAL
   0x0008  00(.)x3 4d(M)x2 1a(.)x1 80(.)x1 +3u  00(.)x5 20( )x4 5a(Z)x1             PARTIAL
   0x0009  00(.)x4 a8(.)x2 6d(m)x1 20( )x1 +2u  30(0)x5 20( )x4 5a(Z)x1             PARTIAL
   0x000b  00(.)x4 20( )x2 ff(.)x1 6e(n)x1 +2u  20( )x9 5a(Z)x1                     PARTIAL
   0x000c  00(.)x4 06(.)x2 f2(.)x2 a8(.)x1 +1u  47(G)x10                            DIFFER
   0x000d  00(.)x5 64(d)x2 01(.)x1 a9(.)x1 +1u  50(P)x6 53(S)x3 0c(.)x1             DIFFER
   0x000e  00(.)x4 06(.)x2 20( )x2 22(")x1 +1u  4f(O)x6 55(U)x3 00(.)x1             PARTIAL
   0x000f  00(.)x7 06(.)x1 01(.)x1 20( )x1     53(S)x6 42(B)x3 00(.)x1             PARTIAL
   0x0010  64(d)x2 00(.)x2 ff(.)x2 06(.)x1 +3u  20( )x7 01(.)x2 47(G)x1             PARTIAL
   0x0011  ff(.)x3 61(a)x2 00(.)x2 20( )x1 +2u  20( )x4 ff(.)x4 0c(.)x1 1f(.)x1     PARTIAL
   0x0012  ff(.)x3 20( )x3 72(r)x2 1a(.)x1 +1u  20( )x5 1e(.)x4 00(.)x1             PARTIAL
   0x0013  00(.)x4 66(f)x2 ff(.)x2 7f(.)x1 +1u  20( )x7 00(.)x1 04(.)x1 df(.)x1     PARTIAL
   0x0014  ff(.)x3 00(.)x2 74(t)x1 01(.)x1 +3u  00(.)x10                            PARTIAL
   0x0015  00(.)x4 6e(n)x2 2d(-)x1 0b(.)x1 +2u  00(.)x9 0c(.)x1                     PARTIAL
   0x0016  00(.)x3 6e(n)x1 6d(m)x1 6f(o)x1 +4u  00(.)x10                            PARTIAL
   0x0017  6e(n)x2 01(.)x2 00(.)x2 4c(L)x1 +2u  00(.)x6 18(.)x4                     PARTIAL
   0x0018  20( )x3 6e(n)x2 4c(L)x1 a3(.)x1 +2u  00(.)x7 ff(.)x2 f6(.)x1             DIFFER
   0x0019  6e(n)x2 20( )x2 06(.)x1 6d(m)x1 +3u  ff(.)x5 01(.)x4 0c(.)x1             DIFFER
   0x001a  6e(n)x3 06(.)x1 a3(.)x1 4d(M)x1 +3u  00(.)x8 02(.)x1 0c(.)x1             PARTIAL
   0x001b  00(.)x4 6e(n)x2 34(4)x1 a3(.)x1 +1u  00(.)x6 ec(.)x2 20( )x1 0a(.)x1     PARTIAL
   0x001c  6e(n)x2 4d(M)x1 0e(.)x1 a3(.)x1 +4u  00(.)x7 ec(.)x2 11(.)x1             DIFFER
   0x001e  00(.)x3 6e(n)x2 20( )x1 a3(.)x1 +2u  00(.)x6 ee(.)x2 ec(.)x2             PARTIAL
   0x0022  00(.)x7 01(.)x2                     18(.)x3 0a(.)x1 06(.)x1 01(.)x1 +4u  PARTIAL
   0x0024  00(.)x4 06(.)x2 0e(.)x2 4d(M)x1     00(.)x4 08(.)x1 95(.)x1 47(G)x1 +3u  PARTIAL
   0x0025  00(.)x5 06(.)x2 8b(.)x1 a8(.)x1     00(.)x4 53(S)x2 ec(.)x2 18(.)x1 +1u  PARTIAL
   0x0026  00(.)x3 01(.)x2 64(d)x2 f2(.)x1     ab(.)x3 55(U)x2 00(.)x2 08(.)x1 +2u  PARTIAL
   0x0028  06(.)x2 01(.)x1 f1(.)x1 20( )x1 +3u  20( )x5 00(.)x4 18(.)x1             PARTIAL
   0x002a  00(.)x3 64(d)x2 06(.)x1 0e(.)x1 +1u  20( )x6 00(.)x2 5a(Z)x1 ff(.)x1     PARTIAL
   0x002c  01(.)x2 00(.)x2 64(d)x1 0e(.)x1 +2u  00(.)x9 0d(.)x1                     PARTIAL
   0x002e  00(.)x3 06(.)x1 fa(.)x1 01(.)x1 +2u  fd(.)x4 00(.)x4 5a(Z)x1 04(.)x1     PARTIAL
   0x0030  00(.)x2 64(d)x1 68(h)x1 8b(.)x1 +3u  00(.)x9 47(G)x1                     PARTIAL
   0x0032  00(.)x5 68(h)x1 8b(.)x1 06(.)x1     00(.)x5 02(.)x2 ff(.)x1 08(.)x1 +1u  PARTIAL
   0x0036  00(.)x4 07(.)x1 8b(.)x1 31(1)x1 +1u  00(.)x7 02(.)x1 0c(.)x1 04(.)x1     PARTIAL
   ... (6 more divergent offsets)
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
  prompts_b/harfbuzz_6162.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6162,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6162 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6162 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6162 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).