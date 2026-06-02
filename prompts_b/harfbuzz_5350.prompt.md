==== BLOCKER ====
Target: harfbuzz
Branch ID: 5350
Location: /src/harfbuzz/src/hb-common.cc:652:5
Enclosing function: hb_script_get_horizontal_direction
Source line:     case HB_SCRIPT_OLD_UYGHUR:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  REFERENCE
cmplog                           4        6          0  REFERENCE
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             1        9          0  loser (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.70h  loser=22.10h
  avg hitcount on branch: winner=52  loser=0
  prob_div=0.90  dur_div=21.40h  hit_div=51
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5350/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_script_get_horizontal_direction (/src/harfbuzz/src/hb-common.cc:584-666) ---
[ ]   582  hb_direction_t
[ ]   583  hb_script_get_horizontal_direction (hb_script_t script)
[B]   584  {
[ ]   585    /* https://docs.google.com/spreadsheets/d/1Y90M0Ie3MUJ6UVCRDOypOtijlMDLNNyyLk36T6iMu0o */
[B]   586    switch ((hb_tag_t) script)
[B]   587    {
[ ]   588      /* Unicode-1.1 additions */
[ ]   589      case HB_SCRIPT_ARABIC:
[ ]   590      case HB_SCRIPT_HEBREW:
[ ]   591  
[ ]   592      /* Unicode-3.0 additions */
[ ]   593      case HB_SCRIPT_SYRIAC:
[ ]   594      case HB_SCRIPT_THAANA:
[ ]   595  
[ ]   596      /* Unicode-4.0 additions */
[ ]   597      case HB_SCRIPT_CYPRIOT:
[ ]   598  
[ ]   599      /* Unicode-4.1 additions */
[ ]   600      case HB_SCRIPT_KHAROSHTHI:
[ ]   601  
[ ]   602      /* Unicode-5.0 additions */
[ ]   603      case HB_SCRIPT_PHOENICIAN:
[ ]   604      case HB_SCRIPT_NKO:
[ ]   605  
[ ]   606      /* Unicode-5.1 additions */
[ ]   607      case HB_SCRIPT_LYDIAN:
[ ]   608  
[ ]   609      /* Unicode-5.2 additions */
[ ]   610      case HB_SCRIPT_AVESTAN:
[ ]   611      case HB_SCRIPT_IMPERIAL_ARAMAIC:
[ ]   612      case HB_SCRIPT_INSCRIPTIONAL_PAHLAVI:
[ ]   613      case HB_SCRIPT_INSCRIPTIONAL_PARTHIAN:
[ ]   614      case HB_SCRIPT_OLD_SOUTH_ARABIAN:
[ ]   615      case HB_SCRIPT_OLD_TURKIC:
[ ]   616      case HB_SCRIPT_SAMARITAN:
[ ]   617  
[ ]   618      /* Unicode-6.0 additions */
[ ]   619      case HB_SCRIPT_MANDAIC:
[ ]   620  
[ ]   621      /* Unicode-6.1 additions */
[ ]   622      case HB_SCRIPT_MEROITIC_CURSIVE:
[ ]   623      case HB_SCRIPT_MEROITIC_HIEROGLYPHS:
[ ]   624  
[ ]   625      /* Unicode-7.0 additions */
[ ]   626      case HB_SCRIPT_MANICHAEAN:
[ ]   627      case HB_SCRIPT_MENDE_KIKAKUI:
[ ]   628      case HB_SCRIPT_NABATAEAN:
[ ]   629      case HB_SCRIPT_OLD_NORTH_ARABIAN:
[ ]   630      case HB_SCRIPT_PALMYRENE:
[ ]   631      case HB_SCRIPT_PSALTER_PAHLAVI:
[ ]   632  
[ ]   633      /* Unicode-8.0 additions */
[ ]   634      case HB_SCRIPT_HATRAN:
[ ]   635  
[ ]   636      /* Unicode-9.0 additions */
[ ]   637      case HB_SCRIPT_ADLAM:
[ ]   638  
[ ]   639      /* Unicode-11.0 additions */
[ ]   640      case HB_SCRIPT_HANIFI_ROHINGYA:
[ ]   641      case HB_SCRIPT_OLD_SOGDIAN:
[ ]   642      case HB_SCRIPT_SOGDIAN:
[ ]   643  
[ ]   644      /* Unicode-12.0 additions */
[ ]   645      case HB_SCRIPT_ELYMAIC:
[ ]   646  
[ ]   647      /* Unicode-13.0 additions */
[ ]   648      case HB_SCRIPT_CHORASMIAN:
[ ]   649      case HB_SCRIPT_YEZIDI:
[ ]   650  
[ ]   651      /* Unicode-14.0 additions */
[W]   652      case HB_SCRIPT_OLD_UYGHUR: <-- BLOCKER
[ ]   653  
[W]   654        return HB_DIRECTION_RTL;
[ ]   655  
[ ]   656  
[ ]   657      /* https://github.com/harfbuzz/harfbuzz/issues/1000 */
[ ]   658      case HB_SCRIPT_OLD_HUNGARIAN:
[ ]   659      case HB_SCRIPT_OLD_ITALIC:
[ ]   660      case HB_SCRIPT_RUNIC:
[ ]   661  
[ ]   662        return HB_DIRECTION_INVALID;
[B]   663    }
[ ]   664  
[B]   665    return HB_DIRECTION_LTR;
[B]   666  }

--- Caller (1 hop): hb-ot-shape.cc:hb_ensure_native_direction(hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shape.cc:564-619, calls hb_script_get_horizontal_direction at line 566) (±10 around call site) ---
[B]   564  {
[B]   565    hb_direction_t direction = buffer->props.direction;
[B]   566    hb_direction_t horiz_dir = hb_script_get_horizontal_direction (buffer->props.script); <-- CALL
[ ]   567  
[ ]   568    /* Numeric runs in natively-RTL scripts are actually native-LTR, so we reset
[ ]   569     * the horiz_dir if the run contains at least one decimal-number char, and no
[ ]   570     * letter chars (ideally we should be checking for chars with strong
[ ]   571     * directionality but hb-unicode currently lacks bidi categories).
[ ]   572     *
[ ]   573     * This allows digit sequences in Arabic etc to be shaped in "native"
[ ]   574     * direction, so that features like ligatures will work as intended.
[ ]   575     *
[ ]   576     * https://github.com/harfbuzz/harfbuzz/issues/501

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409, calls hb_script_get_horizontal_direction at line 376)
hop 2  hb-ot-shape.cc:hb_ensure_native_direction(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:564-619, calls hb_script_get_horizontal_direction at line 566)
hop 3  hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:418-437, calls hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool) at line 433)
hop 3  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ensure_native_direction(hb_buffer_t*) at line 1175)
hop 4  _hb_ot_shape_fallback_mark_position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:444-465, calls hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool) at line 459)
hop 4  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)
hop 5  hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097, calls _hb_ot_shape_fallback_mark_position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, bool) at line 1095)
hop 6  hb-ot-shape.cc:hb_ot_position(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1101-1112, calls hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*) at line 1106)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     210        66  _hb_ot_shape_fallback_kern(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:494-522)
     200        65  _hb_ot_shape_fallback_mark_position_recategorize_marks(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:172-185)
     200        65  _hb_ot_shape_fallback_mark_position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:444-465)
      10         0  hb_buffer_reverse  (/src/harfbuzz/src/hb-buffer.cc:1602-1604)
       9         1  hb-ot-shape.cc:zero_mark_width(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:967-970)
       7         2  hb_buffer_t::sort(unsigned int, unsigned int, int (*)(hb_glyph_info_t const*, hb_glyph_info_t const*))  (/src/harfbuzz/src/hb-buffer.cc:2044-2061)
       3         1  hb_buffer_t::delete_glyphs_inplace(bool (*)(hb_glyph_info_t const*))  (/src/harfbuzz/src/hb-buffer.cc:610-653)
       0         1  _hb_options_init()  (/src/harfbuzz/src/hb-common.cc:75-103)
       0         1  hb-ot-shape-fallback.cc:zero_mark_advances(hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:193-206)
       0         1  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097) ---
  d=5   L1036  T=210 F=0  T=66 F=105  bool adjust_offsets_when_zeroing = c->plan->adjust_mark_p...
  d=5   L1050  T=210 F=0  T=170 F=1  if (c->plan->zero_marks)
  d=5   L1065  T=210 F=0  T=170 F=1  if (c->plan->zero_marks)
--- d=4  _hb_ot_shape_fallback_mark_position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:444-465) ---
  d=4   L 449  T=0 F=200  T=0 F=65  if (!buffer->message (font, "start fallback mark"))
--- d=3  hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:418-437) ---
  d=3   L 419  T=380 F=0  T=195 F=1  if (end - start < 2)
  d=3   L 424  T=0 F=0  T=1 F=1  for (unsigned int i = start; i < end; i++)
  d=3   L 425  T=0 F=0  T=1 F=0  if (!_hb_glyph_info_is_unicode_mark (&info[i]))
  d=3   L 429  T=0 F=0  T=1 F=1  for (j = i + 1; j < end; j++)
  d=3   L 430  T=0 F=0  T=0 F=1  if (!_hb_glyph_info_is_unicode_mark (&info[j]))
--- d=3  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195) ---
  d=3   L1178  T=10 F=0  T=1 F=0  c->buffer->message(c->font, "start preprocess-text"))
--- d=2  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409) ---
  d=2   L 328  T=0 F=0  T=1 F=0  if (!font->get_glyph_extents (buffer->info[base].codepoint,
--- d=1  hb_script_get_horizontal_direction  (/src/harfbuzz/src/hb-common.cc:584-666) ---
  d=1   L 586  T=210 F=20  T=191 F=0  switch ((hb_tag_t) script)
  d=1   L 652  T=20 F=210  T=0 F=191  case HB_SCRIPT_OLD_UYGHUR:  <-- BLOCKER

[off-chain: 55 additional divergent branches across 17 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=1390ee63592e3e2f, size=19 bytes, fuzzer=value_profile, trial=1, discovered_at=28s, mutation_op=ByteAddMutator,BytesDeleteMutator,ByteNegMutator):
  0000: 75 0f 01 00 00 00 00 01 20 20 e0 ed 5a 1a 20 39   u.......  ..Z. 9
  0010: 20 1e ff                                           ..
Seed 2 (id=040f38ebb4b5b1fb, size=10 bytes, fuzzer=value_profile, trial=1, discovered_at=68s, mutation_op=CrossoverReplaceMutator):
  0000: 88 0f 01 00 2d 20 00 00 00 20                     ....- ... 
Seed 3 (id=149c5dae05145ccf, size=26 bytes, fuzzer=value_profile, trial=1, discovered_at=119s, mutation_op=ByteDecMutator):
  0000: 75 0f 01 00 00 00 00 00 8a 0e 01 00 00 00 00 00   u...............
  0010: 00 00 00 00 24 09 4a 4a 3d 3d                     ....$.JJ==
Seed 4 (id=1ced7236f1cec3c8, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=525s, mutation_op=BytesExpandMutator,WordAddMutator,WordInterestingMutator,ByteIncMutator,ByteIncMutator,CrossoverInsertMutator,DwordInterestingMutator):
  0000: 00 e6 d2 08 80 00 01 20 20 01 00 00 00 00 00 00   .......  .......
  0010: 21 21 00 28 0d 0d 0d 0d 0d 0d 0d 0d 00 75 0f 01   !!.(.........u..
  0020: 00 00 00 00 01 20 20 e0 ed 5a 1a 20 39 d7 08 00   .....  ..Z. 9...
  0030: 00 00 fe 00 00 d7 08 00 00 01 00 00 00 d6 08 00   ................
Seed 5 (id=1fed305655293d8a, size=55 bytes, fuzzer=value_profile, trial=1, discovered_at=1411s, mutation_op=BitFlipMutator,BytesRandInsertMutator):
  0000: 80 0f 01 00 80 00 01 00 00 00 00 00 00 eb 01 00   ................
  0010: c0 0f 01 00 00 00 01 00 64 57 57 57 57 57 57 57   ........dWWWWWWW
  0020: 57 57 57 01 2d 68 61 6e 74 00 00 00 00 7b cc cc   WWW.-hant....{..
  0030: cb 0c 00 01 4a d6 3d                              ....J.=

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
   0x0000  75(u)x3 00(.)x2 88(.)x1 80(.)x1 +3u  00(.)x9 ff(.)x1                     PARTIAL
   0x0001  0f(.)x7 e6(.)x1 e0(.)x1 0c(.)x1     01(.)x9 00(.)x1                     DIFFER
   0x0002  01(.)x7 00(.)x2 d2(.)x1             00(.)x9 0c(.)x1                     PARTIAL
   0x0003  00(.)x7 08(.)x1 ed(.)x1 a4(.)x1     00(.)x10                            PARTIAL
   0x0004  00(.)x4 80(.)x2 2d(-)x1 ef(.)x1 +2u  00(.)x9 02(.)x1                     PARTIAL
   0x0005  00(.)x4 20( )x1 1a(.)x1 1b(.)x1 +3u  01(.)x4 02(.)x3 04(.)x2 00(.)x1     PARTIAL
   0x0006  00(.)x5 01(.)x3 0e(.)x1 92(.)x1     ee(.)x4 20( )x4 5a(Z)x1 00(.)x1     PARTIAL
   0x0007  00(.)x7 01(.)x1 20( )x1 04(.)x1     ff(.)x5 20( )x4 5a(Z)x1             PARTIAL
   0x0008  00(.)x5 20( )x2 8a(.)x1 75(u)x1 +1u  00(.)x5 20( )x4 5a(Z)x1             PARTIAL
   0x0009  20( )x2 0e(.)x1 01(.)x1 00(.)x1 +5u  30(0)x5 20( )x4 5a(Z)x1             PARTIAL
   0x000a  01(.)x5 00(.)x3 e0(.)x1             00(.)x5 20( )x2 5a(Z)x1 0f(.)x1 +1u  PARTIAL
   0x000b  00(.)x8 ed(.)x1                     20( )x9 5a(Z)x1                     DIFFER
   0x000c  00(.)x5 76(v)x2 5a(Z)x1 11(.)x1     47(G)x10                            DIFFER
   0x000d  00(.)x2 0f(.)x2 1a(.)x1 eb(.)x1 +3u  50(P)x6 53(S)x3 0c(.)x1             DIFFER
   0x000e  01(.)x4 00(.)x3 20( )x1 ff(.)x1     4f(O)x6 55(U)x3 00(.)x1             PARTIAL
   0x000f  00(.)x6 39(9)x1 20( )x1 a4(.)x1     53(S)x6 42(B)x3 00(.)x1             PARTIAL
   0x0010  00(.)x3 20( )x1 21(!)x1 c0(.)x1 +3u  20( )x7 01(.)x2 47(G)x1             PARTIAL
   0x0011  0f(.)x3 1e(.)x1 00(.)x1 21(!)x1 +3u  20( )x4 ff(.)x4 0c(.)x1 1f(.)x1     DIFFER
   0x0012  00(.)x3 01(.)x3 ff(.)x1 0e(.)x1 +1u  20( )x5 1e(.)x4 00(.)x1             PARTIAL
   0x0013  00(.)x7 28(()x1                     20( )x7 00(.)x1 04(.)x1 df(.)x1     PARTIAL
   0x0014  00(.)x4 24($)x1 0d(.)x1 75(u)x1 +1u  00(.)x10                            PARTIAL
   0x0015  09(.)x1 0d(.)x1 00(.)x1 10(.)x1 +4u  00(.)x9 0c(.)x1                     PARTIAL
   0x0016  01(.)x4 00(.)x2 4a(J)x1 0d(.)x1     00(.)x10                            PARTIAL
   0x0017  00(.)x6 4a(J)x1 0d(.)x1             00(.)x6 18(.)x4                     PARTIAL
   0x0018  3d(=)x1 0d(.)x1 64(d)x1 67(g)x1 +4u  00(.)x7 ff(.)x2 f6(.)x1             PARTIAL
   0x0019  e0(.)x2 3d(=)x1 0d(.)x1 57(W)x1 +3u  ff(.)x5 01(.)x4 0c(.)x1             DIFFER
   0x001a  01(.)x2 00(.)x2 0d(.)x1 57(W)x1 +1u  00(.)x8 02(.)x1 0c(.)x1             PARTIAL
   0x001b  00(.)x2 0d(.)x1 57(W)x1 06(.)x1 +2u  00(.)x6 ec(.)x2 20( )x1 0a(.)x1     PARTIAL
   0x001c  00(.)x2 76(v)x2 57(W)x1 ef(.)x1 +1u  00(.)x7 ec(.)x2 11(.)x1             PARTIAL
   0x001e  01(.)x3 0e(.)x2 0f(.)x1 57(W)x1     00(.)x6 ee(.)x2 ec(.)x2             DIFFER
   0x0020  00(.)x3 57(W)x1 75(u)x1 4b(K)x1     00(.)x6 47(G)x1 05(.)x1 ec(.)x1 +1u  PARTIAL
   0x0022  00(.)x3 01(.)x2 57(W)x1             18(.)x3 0a(.)x1 06(.)x1 01(.)x1 +4u  PARTIAL
   0x0023  00(.)x5 01(.)x1                     e0(.)x3 20( )x2 00(.)x1 02(.)x1 +3u  PARTIAL
   0x0025  00(.)x2 20( )x1 68(h)x1 10(.)x1     00(.)x4 53(S)x2 ec(.)x2 18(.)x1 +1u  PARTIAL
   0x0026  20( )x1 61(a)x1 01(.)x1 24($)x1     ab(.)x3 55(U)x2 00(.)x2 08(.)x1 +2u  DIFFER
   0x0027  e0(.)x1 6e(n)x1 00(.)x1             42(B)x5 0c(.)x1 80(.)x1 18(.)x1 +2u  PARTIAL
   0x0028  ed(.)x1 74(t)x1                     20( )x5 00(.)x4 18(.)x1             DIFFER
   0x0029  5a(Z)x1 00(.)x1                     20( )x3 00(.)x2 3c(<)x2 01(.)x1 +2u  PARTIAL
   0x002a  1a(.)x1 00(.)x1                     20( )x6 00(.)x2 5a(Z)x1 ff(.)x1     PARTIAL
   0x002b  20( )x1 00(.)x1                     00(.)x3 20( )x3 03(.)x2 18(.)x1 +1u  PARTIAL
   ... (20 more divergent offsets)
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
  prompts_b/harfbuzz_5350.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5350,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5350 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5350 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5350 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).