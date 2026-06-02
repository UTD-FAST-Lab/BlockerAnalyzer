==== BLOCKER ====
Target: harfbuzz
Branch ID: 5602
Location: /src/harfbuzz/src/hb-ot-metrics.cc:82:13
Enclosing function: _hb_ot_metrics_get_position_common(hb_font_t*, hb_ot_metrics_tag_t, int*)
Source line:     return (face->table.OS2->use_typo_metrics () && GET_METRIC_Y (OS2, sTypoAscender)) ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (value_profile vs value_profile_cmplog)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile); winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         0       10          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=7.10h  loser=24.00h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.90  dur_div=16.90h  hit_div=4
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.10h  loser=22.10h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=15.00h  hit_div=4
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5602/{W,L}/branch_coverage_show.txt

--- Enclosing function: _hb_ot_metrics_get_position_common(hb_font_t*, hb_ot_metrics_tag_t, int*) (/src/harfbuzz/src/hb-ot-metrics.cc:63-102) ---
[ ]    61  				    hb_ot_metrics_tag_t  metrics_tag,
[ ]    62  				    hb_position_t       *position     /* OUT.  May be NULL. */)
[B]    63  {
[B]    64    hb_face_t *face = font->face;
[B]    65    switch ((unsigned) metrics_tag)
[B]    66    {
[ ]    67  #ifndef HB_NO_VAR
[W]    68  #define GET_VAR face->table.MVAR->get_var (metrics_tag, font->coords, font->num_coords)
[ ]    69  #else
[ ]    70  #define GET_VAR .0f
[ ]    71  #endif
[ ]    72  #define GET_METRIC_X(TABLE, ATTR) \
[ ]    73    (face->table.TABLE->has_data () && \
[ ]    74      ((void) (position && (*position = font->em_scalef_x (_fix_ascender_descender ( \
[ ]    75        face->table.TABLE->ATTR + GET_VAR, metrics_tag)))), true))
[ ]    76  #define GET_METRIC_Y(TABLE, ATTR) \
[B]    77    (face->table.TABLE->has_data () && \
[B]    78      ((void) (position && (*position = font->em_scalef_y (_fix_ascender_descender ( \
[W]    79        face->table.TABLE->ATTR + GET_VAR, metrics_tag)))), true))
[ ]    80  
[B]    81    case HB_OT_METRICS_TAG_HORIZONTAL_ASCENDER:
[B]    82      return (face->table.OS2->use_typo_metrics () && GET_METRIC_Y (OS2, sTypoAscender)) || <-- BLOCKER
[B]    83  	   GET_METRIC_Y (hhea, ascender);
[W]    84    case HB_OT_METRICS_TAG_HORIZONTAL_DESCENDER:
[W]    85      return (face->table.OS2->use_typo_metrics () && GET_METRIC_Y (OS2, sTypoDescender)) ||
[W]    86  	   GET_METRIC_Y (hhea, descender);
[W]    87    case HB_OT_METRICS_TAG_HORIZONTAL_LINE_GAP:
[W]    88      return (face->table.OS2->use_typo_metrics () && GET_METRIC_Y (OS2, sTypoLineGap)) ||
[W]    89  	   GET_METRIC_Y (hhea, lineGap);
[ ]    90  
[ ]    91  #ifndef HB_NO_VERTICAL
[ ]    92    case HB_OT_METRICS_TAG_VERTICAL_ASCENDER:  return GET_METRIC_X (vhea, ascender);
[ ]    93    case HB_OT_METRICS_TAG_VERTICAL_DESCENDER: return GET_METRIC_X (vhea, descender);
[ ]    94    case HB_OT_METRICS_TAG_VERTICAL_LINE_GAP:  return GET_METRIC_X (vhea, lineGap);
[ ]    95  #endif
[ ]    96  
[ ]    97  #undef GET_METRIC_Y
[ ]    98  #undef GET_METRIC_X
[ ]    99  #undef GET_VAR
[ ]   100    default:                               assert (0); return false;
[B]   101    }
[B]   102  }

--- Caller (1 hop): hb-ot-font.cc:hb_ot_get_font_h_extents(hb_font_t*, void*, hb_font_extents_t*, void*) (/src/harfbuzz/src/hb-ot-font.cc:439-443, calls _hb_ot_metrics_get_position_common(hb_font_t*, hb_ot_metrics_tag_t, int*) at line 440) (full body — short) ---
[B]   439  {
[B]   440    return _hb_ot_metrics_get_position_common (font, HB_OT_METRICS_TAG_HORIZONTAL_ASCENDER, &metrics->ascender) && <-- CALL
[B]   441  	 _hb_ot_metrics_get_position_common (font, HB_OT_METRICS_TAG_HORIZONTAL_DESCENDER, &metrics->descender) &&
[B]   442  	 _hb_ot_metrics_get_position_common (font, HB_OT_METRICS_TAG_HORIZONTAL_LINE_GAP, &metrics->line_gap);
[B]   443  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-font.cc:hb_ot_get_font_h_extents(hb_font_t*, void*, hb_font_extents_t*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:439-443, calls _hb_ot_metrics_get_position_common(hb_font_t*, hb_ot_metrics_tag_t, int*) at line 440)
hop 2  hb_ot_metrics_get_position  (/src/harfbuzz/src/hb-ot-metrics.cc:140-239, calls _hb_ot_metrics_get_position_common(hb_font_t*, hb_ot_metrics_tag_t, int*) at line 149)
hop 3  hb_ot_metrics_get_position_with_fallback  (/src/harfbuzz/src/hb-ot-metrics.cc:256-378, calls hb_ot_metrics_get_position at line 261)
hop 3  hb-shape-fuzzer.cc:test_font(hb_font_t*, unsigned int)  (/src/harfbuzz/test/api/test-ot-face.c:38-198, calls hb_ot_metrics_get_position at line 166)
hop 4  hb_ot_layout_get_baseline_with_fallback  (/src/harfbuzz/src/hb-ot-layout.cc:2147-2346, calls hb_ot_metrics_get_position_with_fallback at line 2180)
hop 4  LLVMFuzzerTestOneInput  (/src/harfbuzz/test/fuzzing/hb-shape-fuzzer.cc:13-64, calls hb-shape-fuzzer.cc:test_font(hb_font_t*, unsigned int) at line 51)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      56      2820  hb-ot-font.cc:hb_ot_get_nominal_glyph(hb_font_t*, void*, unsigned int, unsigned int*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:136-140)
      24       822  hb-ot-font.cc:hb_ot_get_glyph_h_advances(hb_font_t*, void*, unsigned int, unsigned int const*, unsigned int, int*, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:183-261)
      20       712  hb-ot-font.cc:hb_ot_get_nominal_glyphs(hb_font_t*, void*, unsigned int, unsigned int const*, unsigned int, unsigned int*, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:151-158)
       3       120  hb-ot-font.cc:_hb_ot_font_create(hb_font_t*)  (/src/harfbuzz/src/hb-ot-font.cc:81-116)
       3       120  hb_ot_font_set_funcs  (/src/harfbuzz/src/hb-ot-font.cc:570-579)
       3       120  hb_ot_metrics_get_variation  (/src/harfbuzz/src/hb-ot-metrics.cc:395-397)
       3       118  hb-ot-font.cc:_hb_ot_font_destroy(void*)  (/src/harfbuzz/src/hb-ot-font.cc:120-128)
       3       118  hb-ot-font.cc:_hb_ot_get_font_funcs()  (/src/harfbuzz/src/hb-ot-font.cc:555-557)
       7       120  _hb_ot_metrics_get_position_common(hb_font_t*, hb_ot_metrics_tag_t, int*)  (/src/harfbuzz/src/hb-ot-metrics.cc:63-102)  <-- enclosing
       2        80  hb-ot-font.cc:hb_ot_get_font_h_extents(hb_font_t*, void*, hb_font_extents_t*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:439-443)
       1        63  hb-ot-font.cc:hb_ot_get_glyph_extents(hb_font_t*, void*, unsigned int, hb_glyph_extents_t*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:379-397)
       1        48  hb-ot-font.cc:hb_ot_get_variation_glyph(hb_font_t*, void*, unsigned int, unsigned int, unsigned int*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:167-173)
       1        40  hb-ot-font.cc:hb_ot_get_glyph_v_advances(hb_font_t*, void*, unsigned int, unsigned int const*, unsigned int, int*, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:272-311)
       1        40  hb-ot-font.cc:hb_ot_get_glyph_v_origin(hb_font_t*, void*, unsigned int, int*, int*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:322-370)
       1        40  hb-ot-font.cc:hb_ot_get_glyph_name(hb_font_t*, void*, unsigned int, char*, unsigned int, void*)  (/src/harfbuzz/src/hb-ot-font.cc:406-415)
... (6 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb_ot_metrics_get_position  (/src/harfbuzz/src/hb-ot-metrics.cc:140-239) ---
  d=2   L 144  T=1 F=0  T=40 F=0  case HB_OT_METRICS_TAG_HORIZONTAL_ASCENDER:
  d=2   L 145  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_HORIZONTAL_DESCENDER:
  d=2   L 146  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_HORIZONTAL_LINE_GAP:
  d=2   L 147  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_VERTICAL_ASCENDER:
  d=2   L 148  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_VERTICAL_DESCENDER:
  d=2   L 149  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_VERTICAL_LINE_GAP:           retur...
  d=2   L 161  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_HORIZONTAL_CLIPPING_ASCENT:  retur...
  d=2   L 162  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_HORIZONTAL_CLIPPING_DESCENT: retur...
  d=2   L 164  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_HORIZONTAL_CARET_RISE:
  d=2   L 165  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_HORIZONTAL_CARET_RUN:
  d=2   L 205  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_HORIZONTAL_CARET_OFFSET:     retur...
  d=2   L 208  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_VERTICAL_CARET_RISE:         retur...
  d=2   L 209  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_VERTICAL_CARET_RUN:          retur...
  d=2   L 210  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_VERTICAL_CARET_OFFSET:       retur...
  d=2   L 212  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_X_HEIGHT:                    retur...
  d=2   L 213  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_CAP_HEIGHT:                  retur...
  d=2   L 214  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_SUBSCRIPT_EM_X_SIZE:         retur...
  d=2   L 215  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_SUBSCRIPT_EM_Y_SIZE:         retur...
  d=2   L 216  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_SUBSCRIPT_EM_X_OFFSET:       retur...
  d=2   L 217  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_SUBSCRIPT_EM_Y_OFFSET:       retur...
  d=2   L 218  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_SUPERSCRIPT_EM_X_SIZE:       retur...
  d=2   L 219  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_SUPERSCRIPT_EM_Y_SIZE:       retur...
  d=2   L 220  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_SUPERSCRIPT_EM_X_OFFSET:     retur...
  d=2   L 221  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_SUPERSCRIPT_EM_Y_OFFSET:     retur...
  d=2   L 222  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_STRIKEOUT_SIZE:              retur...
  d=2   L 223  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_STRIKEOUT_OFFSET:            retur...
  d=2   L 224  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_UNDERLINE_SIZE:              retur...
  d=2   L 225  T=0 F=1  T=0 F=40  case HB_OT_METRICS_TAG_UNDERLINE_OFFSET:            retur...
  d=2   L 228  T=0 F=1  T=0 F=40  case _HB_OT_METRICS_TAG_HORIZONTAL_ASCENDER_OS2:    retur...
  d=2   L 229  T=0 F=1  T=0 F=40  case _HB_OT_METRICS_TAG_HORIZONTAL_ASCENDER_HHEA:   retur...
  d=2   L 230  T=0 F=1  T=0 F=40  case _HB_OT_METRICS_TAG_HORIZONTAL_DESCENDER_OS2:   retur...
  d=2   L 231  T=0 F=1  T=0 F=40  case _HB_OT_METRICS_TAG_HORIZONTAL_DESCENDER_HHEA:  retur...
  d=2   L 232  T=0 F=1  T=0 F=40  case _HB_OT_METRICS_TAG_HORIZONTAL_LINE_GAP_OS2:    retur...
  d=2   L 233  T=0 F=1  T=0 F=40  case _HB_OT_METRICS_TAG_HORIZONTAL_LINE_GAP_HHEA:   retur...
  d=2   L 237  T=0 F=1  T=0 F=40  default:                                        return fa...
--- d=2  hb-ot-font.cc:hb_ot_get_font_h_extents(hb_font_t*, void*, hb_font_extents_t*, void*)  (/src/harfbuzz/src/hb-ot-font.cc:439-443) ---
  d=2   L 440  T=2 F=0  T=0 F=80  return _hb_ot_metrics_get_position_common (font, HB_OT_ME...
  d=2   L 441  T=2 F=0  T=0 F=0  _hb_ot_metrics_get_position_common (font, HB_OT_METRICS_T...
  d=2   L 442  T=2 F=0  T=0 F=0  _hb_ot_metrics_get_position_common (font, HB_OT_METRICS_T...
--- d=1  _hb_ot_metrics_get_position_common(hb_font_t*, hb_ot_metrics_tag_t, int*)  (/src/harfbuzz/src/hb-ot-metrics.cc:63-102) ---
  d=1   L  81  T=3 F=4  T=120 F=0  case HB_OT_METRICS_TAG_HORIZONTAL_ASCENDER:
  d=1   L  82  T=3 F=0  T=0 F=120  return (face->table.OS2->use_typo_metrics () && GET_METRI...  <-- BLOCKER
  d=1   L  84  T=2 F=5  T=0 F=120  case HB_OT_METRICS_TAG_HORIZONTAL_DESCENDER:
  d=1   L  85  T=2 F=0  T=0 F=0  return (face->table.OS2->use_typo_metrics () && GET_METRI...
  d=1   L  87  T=2 F=5  T=0 F=120  case HB_OT_METRICS_TAG_HORIZONTAL_LINE_GAP:
  d=1   L  88  T=2 F=0  T=0 F=0  return (face->table.OS2->use_typo_metrics () && GET_METRI...
  d=1   L  92  T=0 F=7  T=0 F=120  case HB_OT_METRICS_TAG_VERTICAL_ASCENDER:  return GET_MET...
  d=1   L  93  T=0 F=7  T=0 F=120  case HB_OT_METRICS_TAG_VERTICAL_DESCENDER: return GET_MET...
  d=1   L  94  T=0 F=7  T=0 F=120  case HB_OT_METRICS_TAG_VERTICAL_LINE_GAP:  return GET_MET...
  d=1   L 100  T=0 F=7  T=0 F=120  default:                               assert (0); return...

[off-chain: 27 additional divergent branches across 10 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=e49fea8459a181ff, size=165 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=1479s, mutation_op=WordInterestingMutator,QwordAddMutator,WordAddMutator,ByteNegMutator,QwordAddMutator):
  0000: 00 01 00 00 00 02 20 20 20 3f 21 20 4f 53 2f 32   ......   ?! OS/2
  0010: 20 20 00 06 00 00 00 21 20 6b 20 47 53 55 42 20     .....! k GSUB 
  0020: 20 00 01 00 10 00 02 00 d7 d7 d7 d7 d7 d7 d7 d7    ...............
  0030: d7 d7 d7 d7 d7 06 00 02 00 21 20 6b 61 72 00 00   .........! kar..

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 2 (id=002a5b2b8b5c414d, size=54 bytes, fuzzer=value_profile, trial=2, discovered_at=70s, mutation_op=TokenReplace,BytesCopyMutator,ByteAddMutator,BytesSetMutator):
  0000: 92 92 92 df 68 2d 68 81 6e 74 00 9a 9a 20 8e 8e   ....h-h.nt... ..
  0010: 8e 8e 79 8e 9a 17 00 00 00 01 20 20 44 46 ff 54   ..y.......  DF.T
  0020: 70 7f 70 70 70 70 70 52 9a 9a ff df 68 2d 68 61   p.pppppR....h-ha
  0030: 6e 74 00 9a 9a 74                                 nt...t
Seed 3 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 4 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i
Seed 5 (id=00167ff70704a0e0, size=23 bytes, fuzzer=value_profile, trial=1, discovered_at=120s, mutation_op=BytesInsertCopyMutator,CrossoverInsertMutator,ByteDecMutator):
  0000: 4c 0e 00 00 4c 0e 00 00 4c 16 00 00 00 18 18 00   L...L...L.......
  0010: 00 42 18 65 0e 00 ff                              .B.e...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x1                             00(.)x22 e0(.)x2 fe(.)x1 92(.)x1 +14u  PARTIAL
   0x0001  01(.)x1                             01(.)x20 00(.)x2 ff(.)x1 92(.)x1 +16u  PARTIAL
   0x0002  00(.)x1                             00(.)x27 ff(.)x2 6e(n)x2 92(.)x1 +8u  PARTIAL
   0x0003  00(.)x1                             00(.)x28 ff(.)x2 df(.)x1 6c(l)x1 +8u  PARTIAL
   0x0004  00(.)x1                             00(.)x20 df(.)x2 f4(.)x1 68(h)x1 +16u  PARTIAL
   0x0005  02(.)x1                             01(.)x13 02(.)x5 00(.)x4 20( )x3 +11u  PARTIAL
   0x0006  20( )x1                             00(.)x18 07(.)x6 20( )x5 02(.)x2 +9u  PARTIAL
   0x0007  20( )x1                             00(.)x18 20( )x10 01(.)x2 39(9)x2 +8u  PARTIAL
   0x0008  20( )x1                             00(.)x12 21(!)x9 20( )x5 10(.)x2 +12u  PARTIAL
   0x0009  3f(?)x1                             20( )x12 18(.)x7 00(.)x4 74(t)x1 +16u  DIFFER
   0x000a  21(!)x1                             00(.)x10 df(.)x9 1e(.)x7 20( )x5 +9u  DIFFER
   0x000b  20( )x1                             20( )x17 00(.)x9 9a(.)x1 29())x1 +12u  PARTIAL
   0x000c  4f(O)x1                             47(G)x17 00(.)x4 4d(M)x3 01(.)x1 +15u  DIFFER
   0x000d  53(S)x1                             50(P)x13 20( )x5 00(.)x5 53(S)x4 +9u  PARTIAL
   0x000e  2f(/)x1                             4f(O)x13 00(.)x8 55(U)x4 54(T)x2 +12u  DIFFER
   0x000f  32(2)x1                             53(S)x13 00(.)x7 42(B)x4 48(H)x2 +13u  DIFFER
   0x0010  20( )x1                             00(.)x16 02(.)x7 20( )x2 79(y)x1 +13u  PARTIAL
   0x0011  20( )x1                             01(.)x12 04(.)x5 00(.)x4 a9(.)x2 +15u  PARTIAL
   0x0012  00(.)x1                             00(.)x26 68(h)x1 79(y)x1 18(.)x1 +10u  PARTIAL
   0x0013  06(.)x1                             00(.)x10 0d(.)x8 06(.)x5 20( )x2 +14u  PARTIAL
   0x0014  00(.)x1                             00(.)x24 20( )x2 6e(n)x1 9a(.)x1 +11u  PARTIAL
   0x0015  00(.)x1                             00(.)x24 17(.)x2 20( )x2 74(t)x1 +10u  PARTIAL
   0x0016  00(.)x1                             00(.)x31 2d(-)x1 ff(.)x1 3d(=)x1 +5u  PARTIAL
   0x0017  21(!)x1                             00(.)x19 10(.)x11 68(h)x1 3d(=)x1 +6u  DIFFER
   0x0018  20( )x1                             00(.)x23 20( )x2 6b(k)x1 61(a)x1 +11u  PARTIAL
   0x0019  6b(k)x1                             02(.)x9 00(.)x5 1d(.)x4 10(.)x2 +15u  DIFFER
   0x001a  20( )x1                             00(.)x22 20( )x3 05(.)x2 69(i)x1 +10u  PARTIAL
   0x001b  47(G)x1                             00(.)x9 47(G)x8 f8(.)x6 20( )x2 +12u  PARTIAL
   0x001c  53(S)x1                             00(.)x8 17(.)x5 01(.)x2 02(.)x2 +20u  DIFFER
   0x001d  55(U)x1                             00(.)x14 20( )x3 01(.)x3 03(.)x3 +14u  DIFFER
   0x001e  42(B)x1                             00(.)x24 01(.)x3 ff(.)x2 20( )x2 +6u  DIFFER
   0x001f  20( )x1                             00(.)x17 53(S)x4 01(.)x2 54(T)x2 +11u  DIFFER
   0x0020  20( )x1                             00(.)x15 53(S)x6 10(.)x2 70(p)x1 +13u  DIFFER
   0x0021  00(.)x1                             00(.)x10 53(S)x6 07(.)x2 20( )x2 +15u  PARTIAL
   0x0022  01(.)x1                             00(.)x20 53(S)x7 70(p)x1 64(d)x1 +8u  PARTIAL
   0x0023  00(.)x1                             00(.)x9 53(S)x6 02(.)x3 08(.)x3 +14u  PARTIAL
   0x0024  10(.)x1                             00(.)x10 4f(O)x6 53(S)x6 20( )x2 +13u  PARTIAL
   0x0025  00(.)x1                             00(.)x7 53(S)x7 02(.)x4 03(.)x3 +13u  PARTIAL
   0x0026  02(.)x1                             00(.)x21 53(S)x6 20( )x2 70(p)x1 +7u  DIFFER
   0x0027  00(.)x1                             10(.)x8 00(.)x7 53(S)x5 20( )x3 +11u  PARTIAL
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
  prompts_b/harfbuzz_5602.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5602,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5602 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5602 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5602 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).