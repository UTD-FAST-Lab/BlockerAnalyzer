==== BLOCKER ====
Target: harfbuzz
Branch ID: 6181
Location: /src/harfbuzz/src/hb-ot-shaper.hh:331:5
Enclosing function: hb-ot-shape-normalize.cc:hb_ot_shaper_categorize(hb_ot_shape_planner_t const*)
Source line:     case HB_SCRIPT_GRANTHA:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            3        7          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        5        5          0  REFERENCE
naive_ngram4                     5        5          0  REFERENCE
mopt                             4        6          0  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 20  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=9.10h  loser=19.70h
  avg hitcount on branch: winner=4  loser=2
  prob_div=0.60  dur_div=10.60h  hit_div=2
  subject-level: delta_AUC=45443160.0  p_AUC=0.001  delta_Final=636.4  p_final=0.0006

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/6181/{W,L}/branch_coverage_show.txt

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
[ ]   231      case HB_SCRIPT_TELUGU:
[ ]   232  
[ ]   233        /* If the designer designed the font for the 'DFLT' script,
[ ]   234         * (or we ended up arbitrarily pick 'latn'), use the default shaper.
[ ]   235         * Otherwise, use the specific shaper.
[ ]   236         *
[ ]   237         * If it's indy3 tag, send to USE. */
[ ]   238        if (planner->map.chosen_script[0] == HB_TAG ('D','F','L','T') ||
[ ]   239  	  planner->map.chosen_script[0] == HB_TAG ('l','a','t','n'))
[ ]   240  	return &_hb_ot_shaper_default;
[ ]   241        else if ((planner->map.chosen_script[0] & 0x000000FF) == '3')
[ ]   242  	return &_hb_ot_shaper_use;
[ ]   243        else
[ ]   244  	return &_hb_ot_shaper_indic;
[ ]   245  
[ ]   246      case HB_SCRIPT_KHMER:
[ ]   247  	return &_hb_ot_shaper_khmer;
[ ]   248  
[ ]   249      case HB_SCRIPT_MYANMAR:
[ ]   250        /* If the designer designed the font for the 'DFLT' script,
[ ]   251         * (or we ended up arbitrarily pick 'latn'), use the default shaper.
[ ]   252         * Otherwise, use the specific shaper.
[ ]   253         *
[ ]   254         * If designer designed for 'mymr' tag, also send to default
[ ]   255         * shaper.  That's tag used from before Myanmar shaping spec
[ ]   256         * was developed.  The shaping spec uses 'mym2' tag. */
[ ]   257        if (planner->map.chosen_script[0] == HB_TAG ('D','F','L','T') ||
[ ]   258  	  planner->map.chosen_script[0] == HB_TAG ('l','a','t','n') ||
[ ]   259  	  planner->map.chosen_script[0] == HB_TAG ('m','y','m','r'))
[ ]   260  	return &_hb_ot_shaper_default;
[ ]   261        else
[ ]   262  	return &_hb_ot_shaper_myanmar;
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
[L]   278      case HB_SCRIPT_MONGOLIAN:
[L]   279      case HB_SCRIPT_SINHALA:
[ ]   280  
[ ]   281      /* Unicode-3.2 additions */
[L]   282      case HB_SCRIPT_BUHID:
[L]   283      case HB_SCRIPT_HANUNOO:
[L]   284      case HB_SCRIPT_TAGALOG:
[L]   285      case HB_SCRIPT_TAGBANWA:
[ ]   286  
[ ]   287      /* Unicode-4.0 additions */
[L]   288      case HB_SCRIPT_LIMBU:
[L]   289      case HB_SCRIPT_TAI_LE:
[ ]   290  
[ ]   291      /* Unicode-4.1 additions */
[L]   292      case HB_SCRIPT_BUGINESE:
[L]   293      case HB_SCRIPT_KHAROSHTHI:
[L]   294      case HB_SCRIPT_SYLOTI_NAGRI:
[L]   295      case HB_SCRIPT_TIFINAGH:
[ ]   296  
[ ]   297      /* Unicode-5.0 additions */
[L]   298      case HB_SCRIPT_BALINESE:
[L]   299      case HB_SCRIPT_NKO:
[L]   300      case HB_SCRIPT_PHAGS_PA:
[ ]   301  
[ ]   302      /* Unicode-5.1 additions */
[L]   303      case HB_SCRIPT_CHAM:
[L]   304      case HB_SCRIPT_KAYAH_LI:
[L]   305      case HB_SCRIPT_LEPCHA:
[L]   306      case HB_SCRIPT_REJANG:
[L]   307      case HB_SCRIPT_SAURASHTRA:
[L]   308      case HB_SCRIPT_SUNDANESE:
[ ]   309  
[ ]   310      /* Unicode-5.2 additions */
[L]   311      case HB_SCRIPT_EGYPTIAN_HIEROGLYPHS:
[L]   312      case HB_SCRIPT_JAVANESE:
[L]   313      case HB_SCRIPT_KAITHI:
[L]   314      case HB_SCRIPT_MEETEI_MAYEK:
[L]   315      case HB_SCRIPT_TAI_THAM:
[L]   316      case HB_SCRIPT_TAI_VIET:
[ ]   317  
[ ]   318      /* Unicode-6.0 additions */
[L]   319      case HB_SCRIPT_BATAK:
[L]   320      case HB_SCRIPT_BRAHMI:
[L]   321      case HB_SCRIPT_MANDAIC:
[ ]   322  
[ ]   323      /* Unicode-6.1 additions */
[L]   324      case HB_SCRIPT_CHAKMA:
[L]   325      case HB_SCRIPT_MIAO:
[L]   326      case HB_SCRIPT_SHARADA:
[L]   327      case HB_SCRIPT_TAKRI:
[ ]   328  
[ ]   329      /* Unicode-7.0 additions */
[L]   330      case HB_SCRIPT_DUPLOYAN:
[B]   331      case HB_SCRIPT_GRANTHA: <-- BLOCKER
[B]   332      case HB_SCRIPT_KHOJKI:
[B]   333      case HB_SCRIPT_KHUDAWADI:
[B]   334      case HB_SCRIPT_MAHAJANI:
[B]   335      case HB_SCRIPT_MANICHAEAN:
[B]   336      case HB_SCRIPT_MODI:
[B]   337      case HB_SCRIPT_PAHAWH_HMONG:
[B]   338      case HB_SCRIPT_PSALTER_PAHLAVI:
[B]   339      case HB_SCRIPT_SIDDHAM:
[B]   340      case HB_SCRIPT_TIRHUTA:
[ ]   341  
[ ]   342      /* Unicode-8.0 additions */
[B]   343      case HB_SCRIPT_AHOM:
[B]   344      case HB_SCRIPT_MULTANI:
[ ]   345  
[ ]   346      /* Unicode-9.0 additions */
[B]   347      case HB_SCRIPT_ADLAM:
[B]   348      case HB_SCRIPT_BHAIKSUKI:
[B]   349      case HB_SCRIPT_MARCHEN:
[B]   350      case HB_SCRIPT_NEWA:
[ ]   351  
[ ]   352      /* Unicode-10.0 additions */
[B]   353      case HB_SCRIPT_MASARAM_GONDI:
[B]   354      case HB_SCRIPT_SOYOMBO:
[B]   355      case HB_SCRIPT_ZANABAZAR_SQUARE:
[ ]   356  
[ ]   357      /* Unicode-11.0 additions */
[B]   358      case HB_SCRIPT_DOGRA:
[B]   359      case HB_SCRIPT_GUNJALA_GONDI:
[B]   360      case HB_SCRIPT_HANIFI_ROHINGYA:
[B]   361      case HB_SCRIPT_MAKASAR:
[B]   362      case HB_SCRIPT_MEDEFAIDRIN:
[B]   363      case HB_SCRIPT_OLD_SOGDIAN:
[B]   364      case HB_SCRIPT_SOGDIAN:
[ ]   365  
[ ]   366      /* Unicode-12.0 additions */
[B]   367      case HB_SCRIPT_ELYMAIC:
[B]   368      case HB_SCRIPT_NANDINAGARI:
[B]   369      case HB_SCRIPT_NYIAKENG_PUACHUE_HMONG:
[B]   370      case HB_SCRIPT_WANCHO:
[ ]   371  
[ ]   372      /* Unicode-13.0 additions */
[B]   373      case HB_SCRIPT_CHORASMIAN:
[B]   374      case HB_SCRIPT_DIVES_AKURU:
[B]   375      case HB_SCRIPT_KHITAN_SMALL_SCRIPT:
[B]   376      case HB_SCRIPT_YEZIDI:
[ ]   377  
[ ]   378      /* Unicode-14.0 additions */
[B]   379      case HB_SCRIPT_CYPRO_MINOAN:
[B]   380      case HB_SCRIPT_OLD_UYGHUR:
[B]   381      case HB_SCRIPT_TANGSA:
[B]   382      case HB_SCRIPT_TOTO:
[B]   383      case HB_SCRIPT_VITHKUQI:
[ ]   384  
[ ]   385      /* Unicode-15.0 additions */
[B]   386      case HB_SCRIPT_KAWI:
[B]   387      case HB_SCRIPT_NAG_MUNDARI:
[ ]   388  
[ ]   389        /* If the designer designed the font for the 'DFLT' script,
[ ]   390         * (or we ended up arbitrarily pick 'latn'), use the default shaper.
[ ]   391         * Otherwise, use the specific shaper.
[ ]   392         * Note that for some simple scripts, there may not be *any*
[ ]   393         * GSUB/GPOS needed, so there may be no scripts found! */
[B]   394        if (planner->map.chosen_script[0] == HB_TAG ('D','F','L','T') ||
[B]   395  	  planner->map.chosen_script[0] == HB_TAG ('l','a','t','n'))
[ ]   396  	return &_hb_ot_shaper_default;
[B]   397        else
[B]   398  	return &_hb_ot_shaper_use;
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
      20         6  hb-ot-shape.cc:adjust_mark_offsets(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:960-963)
      20         6  hb-ot-shape.cc:zero_mark_width(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:967-970)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
  (no divergent branches in chain functions; the split is off-chain)

[off-chain: 39 additional divergent branches across 11 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=4559e66c54a51f83, size=1472 bytes, fuzzer=grimoire, trial=2, discovered_at=3515s):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 63 6d 61 70   ......      cmap
  0010: 20 20 20 20 00 00 00 1a 00 01 00 00 00 01 00 00       ............
  0020: 00 01 00 00 00 7f 00 20 20 20 20 20 53 56 47 20   .......     SVG 
  0030: 03 02 00 1a 20 00 00 20 00 00 02 03 ff ff ff 0f   .... .. ........
Seed 2 (id=006481a39138b1b6, size=1019 bytes, fuzzer=grimoire, trial=2, discovered_at=5516s):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 44 45 46   ......      GDEF
  0010: 20 20 20 0f 00 00 00 1a 61 6e 00 01 00 10 00 01      .....an......
  0020: 00 02 01 03 00 00 00 00 92 00 06 02 00 04 00 00   ................
  0030: 20 20 20 20 06 04 01 04 00 00 00 13 0e 00 9e 9e       ............
Seed 3 (id=7b5a542c9485a4f8, size=744 bytes, fuzzer=grimoire, trial=2, discovered_at=5546s):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 63 6d 61 70   ......      cmap
  0010: 20 20 20 20 00 00 00 1a 00 01 00 00 00 01 00 00       ............
  0020: 00 01 00 00 00 7f 00 20 20 20 20 20 53 56 47 20   .......     SVG 
  0030: 03 02 00 1a 20 00 00 20 00 00 02 03 ff ff ff 0f   .... .. ........
Seed 4 (id=4a6cf612565c5d8b, size=596 bytes, fuzzer=grimoire, trial=2, discovered_at=7714s):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 63 6d 61 70   ......      cmap
  0010: 20 20 20 20 00 00 00 1a 00 04 00 00 00 01 00 00       ............
  0020: 00 01 00 00 00 10 20 20 20 20 00 04 55 4c 46 44   ......    ..ULFD
  0030: 00 68 61 6e 74 2d 6d 6f 00 b2 b2 b2 b2 b2 17 00   .hant-mo........
Seed 5 (id=2f65acf0bd58042a, size=4119 bytes, fuzzer=grimoire, trial=2, discovered_at=10885s):
  0000: 4f 54 54 4f 00 01 20 20 20 20 20 20 47 50 4f 53   OTTO..      GPOS
  0010: 20 20 df 20 00 00 00 20 14 7a 68 2d 68 61 6e 74     . ... .zh-hant
  0020: 00 01 00 00 01 02 0c 06 00 01 01 01 01 01 01 01   ................
  0030: 01 01 01 61 6e 73 02 00 20 00 00 04 00 c8 20 e0   ...ans.. ..... .

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=001576b87ec39bdb, size=72 bytes, fuzzer=cmplog, trial=2, discovered_at=600s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteNegMutator):
  0000: 69 69 69 b5 b5 00 00 01 0c 00 00 01 20 20 00 18   iii.........  ..
  0010: 00 00 00 8e 7d 00 20 20 20 20 1f 20 43 46 30 b5   ....}.    . CF0.
  0020: b5 b5 b5 b5 b5 b5 b5 b5 b5 b5 b5 18 18 18 00 00   ................
  0030: 18 18 00 01 30 b0 30 80 00 1e aa 00 00 1e 1e b5   ....0.0.........
Seed 2 (id=0011b6b57575fd99, size=77 bytes, fuzzer=cmplog, trial=2, discovered_at=727s, mutation_op=BytesDeleteMutator,WordAddMutator,BytesInsertMutator,ByteInterestingMutator,ByteNegMutator,BytesExpandMutator):
  0000: f8 19 00 0a 00 6b 61 72 20 20 20 01 01 00 80 01   .....kar   .....
  0010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0020: 00 1e ff ff 02 00 0e 02 00 20 00 02 00 00 04 53   ......... .....S
  0030: 56 47 0e 03 00 00 0e 02 00 20 00 20 02 40 04 53   VG....... . .@.S
Seed 3 (id=00393cf6f6cb63fe, size=132 bytes, fuzzer=cmplog, trial=2, discovered_at=1962s, mutation_op=BytesSwapMutator):
  0000: 2d 08 0e 04 00 00 20 00 15 21 20 20 20 6b 65 72   -..... ..!   ker
  0010: 6e 20 72 13 1f 03 02 00 20 00 43 43 43 43 43 43   n r..... .CCCCCC
  0020: 43 43 24 02 43 0e 0e 0e 0e 00 00 1a 0e 0e 0e 0e   CC$.C...........
  0030: 0e 0e 46 46 00 00 00 fe 00 00 20 00 68 61 6e 74   ..FF...... .hant
Seed 4 (id=0027d6e6ebbf3426, size=136 bytes, fuzzer=cmplog, trial=2, discovered_at=2601s, mutation_op=BytesSetMutator,BytesDeleteMutator,ByteRandMutator,BytesCopyMutator):
  0000: 00 01 00 00 00 01 20 20 20 21 df 2d 4d 41 54 48   ......   !.-MATH
  0010: 00 01 03 0a 00 00 00 10 00 61 67 4c 05 00 00 00   .........agL....
  0020: 00 00 00 03 00 04 00 02 00 80 00 4c 4c 00 00 03   ...........LL...
  0030: 00 03 00 04 00 02 ca 80 00 4c 4c 00 00 03 00 04   .........LL.....
Seed 5 (id=002904822b808df0, size=218 bytes, fuzzer=cmplog, trial=2, discovered_at=3330s, mutation_op=CrossoverReplaceMutator,BytesCopyMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 df 20 4d 41 54 48   ......    . MATH
  0010: 00 01 03 0a 00 00 00 10 6e 8d 2d 68 61 6e aa 10   ........n.-han..
  0020: 00 00 00 02 00 03 00 00 00 01 00 00 00 01 20 20   ..............  
  0030: 20 20 df 20 4d 41 54 48 00 01 03 0a 00 00 00 10     . MATH........


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x5 4f(O)x5                     00(.)x7 69(i)x1 f8(.)x1 2d(-)x1     PARTIAL
   0x0001  01(.)x5 54(T)x5                     01(.)x7 69(i)x1 19(.)x1 08(.)x1     PARTIAL
   0x0002  00(.)x5 54(T)x5                     00(.)x8 69(i)x1 0e(.)x1             PARTIAL
   0x0003  00(.)x5 4f(O)x5                     00(.)x7 b5(.)x1 0a(.)x1 04(.)x1     PARTIAL
   0x0004  00(.)x10                            00(.)x9 b5(.)x1                     PARTIAL
   0x0005  01(.)x10                            01(.)x4 00(.)x2 02(.)x2 6b(k)x1 +1u  PARTIAL
   0x0006  20( )x10                            00(.)x6 20( )x3 61(a)x1             PARTIAL
   0x0007  20( )x10                            00(.)x3 04(.)x3 20( )x2 01(.)x1 +1u  PARTIAL
   0x0008  20( )x10                            00(.)x5 20( )x3 0c(.)x1 15(.)x1     PARTIAL
   0x0009  20( )x10                            7b({)x3 20( )x2 21(!)x2 18(.)x2 +1u  PARTIAL
   0x000a  20( )x10                            df(.)x7 20( )x2 00(.)x1             PARTIAL
   0x000b  20( )x10                            20( )x6 01(.)x2 2d(-)x1 21(!)x1     PARTIAL
   0x000c  47(G)x6 63(c)x4                     47(G)x5 20( )x2 4d(M)x2 01(.)x1     PARTIAL
   0x000d  50(P)x5 6d(m)x4 44(D)x1             50(P)x4 41(A)x2 20( )x1 00(.)x1 +2u  PARTIAL
   0x000e  4f(O)x5 61(a)x4 45(E)x1             4f(O)x4 54(T)x2 00(.)x1 80(.)x1 +2u  PARTIAL
   0x000f  53(S)x5 70(p)x4 46(F)x1             53(S)x4 48(H)x2 18(.)x1 01(.)x1 +2u  PARTIAL
   0x0010  20( )x10                            00(.)x4 01(.)x3 02(.)x2 6e(n)x1     DIFFER
   0x0011  20( )x10                            00(.)x5 01(.)x2 20( )x1 03(.)x1 +1u  PARTIAL
   0x0012  20( )x5 df(.)x5                     03(.)x3 80(.)x3 00(.)x2 72(r)x1 +1u  DIFFER
   0x0013  20( )x9 0f(.)x1                     00(.)x3 0a(.)x2 8e(.)x1 13(.)x1 +3u  DIFFER
   0x0014  00(.)x10                            00(.)x8 7d(})x1 1f(.)x1             PARTIAL
   0x0015  00(.)x10                            00(.)x9 03(.)x1                     PARTIAL
   0x0016  00(.)x10                            00(.)x8 20( )x1 02(.)x1             PARTIAL
   0x0017  1a(.)x5 20( )x5                     00(.)x7 10(.)x2 20( )x1             PARTIAL
   0x0018  14(.)x5 00(.)x4 61(a)x1             00(.)x7 20( )x2 6e(n)x1             PARTIAL
   0x0019  7a(z)x5 01(.)x3 6e(n)x1 04(.)x1     00(.)x5 1d(.)x2 20( )x1 61(a)x1 +1u  DIFFER
   0x001a  00(.)x5 68(h)x5                     00(.)x5 1f(.)x1 43(C)x1 67(g)x1 +2u  PARTIAL
   0x001b  2d(-)x5 00(.)x4 01(.)x1             f8(.)x5 20( )x1 00(.)x1 43(C)x1 +2u  PARTIAL
   0x001c  00(.)x5 68(h)x5                     17(.)x4 43(C)x2 00(.)x1 05(.)x1 +2u  PARTIAL
   0x001d  61(a)x5 01(.)x4 10(.)x1             00(.)x5 46(F)x1 43(C)x1 6e(n)x1 +2u  DIFFER
   0x001e  00(.)x5 6e(n)x5                     20( )x3 00(.)x2 30(0)x1 43(C)x1 +3u  PARTIAL
   0x001f  74(t)x5 00(.)x4 01(.)x1             02(.)x3 00(.)x2 b5(.)x1 43(C)x1 +3u  PARTIAL
   0x0020  00(.)x10                            00(.)x6 b5(.)x1 43(C)x1 10(.)x1 +1u  PARTIAL
   0x0021  01(.)x9 02(.)x1                     ff(.)x3 00(.)x2 b5(.)x1 1e(.)x1 +3u  DIFFER
   0x0022  00(.)x6 01(.)x2 02(.)x2             ff(.)x4 00(.)x2 b5(.)x1 24($)x1 +2u  PARTIAL
   0x0023  00(.)x9 03(.)x1                     02(.)x2 01(.)x2 b5(.)x1 ff(.)x1 +4u  PARTIAL
   0x0024  00(.)x5 01(.)x5                     00(.)x5 b5(.)x1 02(.)x1 43(C)x1 +2u  PARTIAL
   0x0025  02(.)x5 7f(.)x3 00(.)x1 10(.)x1     1f(.)x3 b5(.)x1 00(.)x1 0e(.)x1 +4u  PARTIAL
   0x0026  0c(.)x5 00(.)x4 20( )x1             10(.)x3 0e(.)x2 00(.)x2 b5(.)x1 +2u  PARTIAL
   0x0027  20( )x4 00(.)x4 06(.)x2             00(.)x4 02(.)x2 b5(.)x1 0e(.)x1 +2u  PARTIAL
   ... (15 more divergent offsets)
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

--- grimoire ---
**Baseline relationship**: grimoire builds on the full cmplog stack —
it includes the `CmpLogObserver`, the `TracingStage`, and the
`I2SRandReplace` (i2s) stage — and ADDS a `GeneralizationStage` plus
Grimoire structural mutators. The single-technique delta is therefore
`grimoire` vs `cmplog` (both have I2S; grimoire adds generalization +
Grimoire mutators), not vs naive.

**Instrumentation**: cmplog's edge counters + per-execution CMP buffer
(`CmpLogObserver`).

**Feedback**: edge-bucket `MaxMapFeedback`.

**Mutators / stages**: stages are
`[generalization, tracing, i2s, havoc, grimoire]`. `GeneralizationStage`
replaces concrete byte runs in a corpus entry with `<GAP>` placeholders
(a generalised input) by repeatedly re-executing and checking that
coverage is preserved. The Grimoire mutators —
`GrimoireExtensionMutator`, `GrimoireRecursiveReplacementMutator`,
`GrimoireStringReplacementMutator`, `GrimoireRandomDeleteMutator` —
splice and recurse on these generalised token/gap structures
(string-based, grammar-free structural mutation). `I2SRandReplace` (the
cmplog i2s stage) also runs.

**Observed `mutation_op` in seed metadata**: all grimoire stages (i2s,
havoc, grimoire) are wrapped in `LineageMutatorWrap` with **no
per-operator name list**, so grimoire seeds appear nameless in lineage
(`mutation_op = -`). As with mopt, nameless rows are NOT an
I2S-exclusive signal here — and grimoire genuinely runs I2S too, so the
two are not separable from lineage names.

**Per-execution cost**: cmplog's per-CMP cost, plus extra executions
during generalization (each candidate gap is validated by a re-run).

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_6181.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6181,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6181 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6181 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6181 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).