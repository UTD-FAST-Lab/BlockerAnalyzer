==== BLOCKER ====
Target: harfbuzz
Branch ID: 5334
Location: /src/harfbuzz/src/hb-common.cc:615:5
Enclosing function: hb_script_get_horizontal_direction
Source line:     case HB_SCRIPT_OLD_TURKIC:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog             9        1          0  REFERENCE
naive_ctx                        5        5          0  REFERENCE
naive_ngram4                     5        5          0  REFERENCE
mopt                             5        5          0  REFERENCE
minimizer                        6        4          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.40h  loser=19.80h
  avg hitcount on branch: winner=16  loser=1
  prob_div=0.70  dur_div=13.40h  hit_div=15
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5334/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_script_get_horizontal_direction (/src/harfbuzz/src/hb-common.cc:584-666) ---
[ ]   582  hb_direction_t
[ ]   583  hb_script_get_horizontal_direction (hb_script_t script)
[B]   584  {
[ ]   585    /* https://docs.google.com/spreadsheets/d/1Y90M0Ie3MUJ6UVCRDOypOtijlMDLNNyyLk36T6iMu0o */
[B]   586    switch ((hb_tag_t) script)
[B]   587    {
[ ]   588      /* Unicode-1.1 additions */
[ ]   589      case HB_SCRIPT_ARABIC:
[L]   590      case HB_SCRIPT_HEBREW:
[ ]   591  
[ ]   592      /* Unicode-3.0 additions */
[L]   593      case HB_SCRIPT_SYRIAC:
[L]   594      case HB_SCRIPT_THAANA:
[ ]   595  
[ ]   596      /* Unicode-4.0 additions */
[L]   597      case HB_SCRIPT_CYPRIOT:
[ ]   598  
[ ]   599      /* Unicode-4.1 additions */
[L]   600      case HB_SCRIPT_KHAROSHTHI:
[ ]   601  
[ ]   602      /* Unicode-5.0 additions */
[L]   603      case HB_SCRIPT_PHOENICIAN:
[L]   604      case HB_SCRIPT_NKO:
[ ]   605  
[ ]   606      /* Unicode-5.1 additions */
[L]   607      case HB_SCRIPT_LYDIAN:
[ ]   608  
[ ]   609      /* Unicode-5.2 additions */
[L]   610      case HB_SCRIPT_AVESTAN:
[L]   611      case HB_SCRIPT_IMPERIAL_ARAMAIC:
[L]   612      case HB_SCRIPT_INSCRIPTIONAL_PAHLAVI:
[L]   613      case HB_SCRIPT_INSCRIPTIONAL_PARTHIAN:
[L]   614      case HB_SCRIPT_OLD_SOUTH_ARABIAN:
[B]   615      case HB_SCRIPT_OLD_TURKIC: <-- BLOCKER
[B]   616      case HB_SCRIPT_SAMARITAN:
[ ]   617  
[ ]   618      /* Unicode-6.0 additions */
[B]   619      case HB_SCRIPT_MANDAIC:
[ ]   620  
[ ]   621      /* Unicode-6.1 additions */
[B]   622      case HB_SCRIPT_MEROITIC_CURSIVE:
[B]   623      case HB_SCRIPT_MEROITIC_HIEROGLYPHS:
[ ]   624  
[ ]   625      /* Unicode-7.0 additions */
[B]   626      case HB_SCRIPT_MANICHAEAN:
[B]   627      case HB_SCRIPT_MENDE_KIKAKUI:
[B]   628      case HB_SCRIPT_NABATAEAN:
[B]   629      case HB_SCRIPT_OLD_NORTH_ARABIAN:
[B]   630      case HB_SCRIPT_PALMYRENE:
[B]   631      case HB_SCRIPT_PSALTER_PAHLAVI:
[ ]   632  
[ ]   633      /* Unicode-8.0 additions */
[B]   634      case HB_SCRIPT_HATRAN:
[ ]   635  
[ ]   636      /* Unicode-9.0 additions */
[B]   637      case HB_SCRIPT_ADLAM:
[ ]   638  
[ ]   639      /* Unicode-11.0 additions */
[B]   640      case HB_SCRIPT_HANIFI_ROHINGYA:
[B]   641      case HB_SCRIPT_OLD_SOGDIAN:
[B]   642      case HB_SCRIPT_SOGDIAN:
[ ]   643  
[ ]   644      /* Unicode-12.0 additions */
[B]   645      case HB_SCRIPT_ELYMAIC:
[ ]   646  
[ ]   647      /* Unicode-13.0 additions */
[B]   648      case HB_SCRIPT_CHORASMIAN:
[B]   649      case HB_SCRIPT_YEZIDI:
[ ]   650  
[ ]   651      /* Unicode-14.0 additions */
[B]   652      case HB_SCRIPT_OLD_UYGHUR:
[ ]   653  
[B]   654        return HB_DIRECTION_RTL;
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
       4        32  hb-ot-shape.cc:zero_mark_width(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:967-970)
       4        28  hb_buffer_t::merge_clusters_impl(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-buffer.cc:512-539)
       3        25  hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:37-166)
       0        20  hb_buffer_t::sort(unsigned int, unsigned int, int (*)(hb_glyph_info_t const*, hb_glyph_info_t const*))  (/src/harfbuzz/src/hb-buffer.cc:2044-2061)
       0        16  hb-ot-shape.cc:adjust_mark_offsets(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:960-963)
       3        13  hb-ot-shape-fallback.cc:zero_mark_advances(hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:193-206)
       3        13  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409)
       0         2  hb_buffer_t::delete_glyphs_inplace(bool (*)(hb_glyph_info_t const*))  (/src/harfbuzz/src/hb-buffer.cc:610-653)
       0         2  hb_buffer_get_empty  (/src/harfbuzz/src/hb-buffer.cc:795-797)
       0         1  _hb_options_init()  (/src/harfbuzz/src/hb-common.cc:75-103)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097) ---
  d=5   L1036  T=105 F=42  T=171 F=0  bool adjust_offsets_when_zeroing = c->plan->adjust_mark_p...
  d=5   L1050  T=147 F=0  T=168 F=3  if (c->plan->zero_marks)
  d=5   L1053  T=0 F=147  T=2 F=166  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_EARLY:
  d=5   L1059  T=147 F=0  T=166 F=2  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
  d=5   L1065  T=147 F=0  T=168 F=3  if (c->plan->zero_marks)
  d=5   L1068  T=147 F=0  T=166 F=2  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
  d=5   L1074  T=0 F=147  T=2 F=166  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_EARLY:
--- d=3  hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:418-437) ---
  d=3   L 424  T=3 F=3  T=16 F=14  for (unsigned int i = start; i < end; i++)
  d=3   L 425  T=3 F=0  T=13 F=3  if (!_hb_glyph_info_is_unicode_mark (&info[i]))
  d=3   L 429  T=3 F=3  T=22 F=13  for (j = i + 1; j < end; j++)
  d=3   L 430  T=0 F=3  T=0 F=22  if (!_hb_glyph_info_is_unicode_mark (&info[j]))
--- d=3  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195) ---
  d=3   L1177  T=0 F=147  T=3 F=168  if (c->plan->shaper->preprocess_text &&
  d=3   L1178  T=0 F=0  T=3 F=0  c->buffer->message(c->font, "start preprocess-text"))
--- d=2  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409) ---
  d=2   L 328  T=3 F=0  T=13 F=0  if (!font->get_glyph_extents (buffer->info[base].codepoint,
--- d=1  hb_script_get_horizontal_direction  (/src/harfbuzz/src/hb-common.cc:584-666) ---
  d=1   L 590  T=0 F=161  T=4 F=187  case HB_SCRIPT_HEBREW:
  d=1   L 594  T=0 F=161  T=2 F=189  case HB_SCRIPT_THAANA:
  d=1   L 615  T=14 F=147  T=0 F=191  case HB_SCRIPT_OLD_TURKIC:  <-- BLOCKER

[off-chain: 114 additional divergent branches across 21 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=ae1635cd677d2b15, size=96 bytes, fuzzer=cmplog, trial=1, discovered_at=1587s, mutation_op=BytesRandInsertMutator,QwordAddMutator,BytesDeleteMutator,ByteAddMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 4d 41 54 48   ......      MATH
  0010: 00 01 00 80 00 00 00 10 00 10 03 03 03 03 00 00   ................
  0020: 64 74 04 00 20 02 00 04 00 0b 00 00 1a 00 00 20   dt.. .......... 
  0030: 1a 1a 1a 1a 00 0c 01 00 20 04 00 04 00 00 20 00   ........ ..... .
Seed 2 (id=8571c5a32bcbccad, size=241 bytes, fuzzer=cmplog, trial=1, discovered_at=2904s, mutation_op=BytesExpandMutator):
  0000: 00 01 00 00 00 01 20 02 21 20 20 20 47 50 4f 53   ...... .!   GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 00 10 00 00 20   ............... 
  0020: 00 01 32 32 32 32 32 32 32 32 32 32 32 32 01 00   ..222222222222..
  0030: 00 00 00 01 0d 00 00 36 04 00 00 14 00 00 00 20   .......6....... 
Seed 3 (id=bd061a68ba011f14, size=237 bytes, fuzzer=cmplog, trial=1, discovered_at=2904s, mutation_op=ByteNegMutator,ByteIncMutator,BytesInsertMutator):
  0000: 00 01 00 00 00 01 20 02 21 20 20 20 47 50 4f 53   ...... .!   GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 00 10 00 00 20   ............... 
  0020: 00 01 32 32 32 32 32 32 32 32 32 32 32 32 01 00   ..222222222222..
  0030: 00 00 00 01 0d 00 00 36 04 00 00 14 00 00 00 20   .......6....... 
Seed 4 (id=b17e1cd761b640da, size=232 bytes, fuzzer=cmplog, trial=1, discovered_at=3342s, mutation_op=WordAddMutator,BytesCopyMutator):
  0000: 00 01 00 00 00 01 20 02 21 20 20 20 47 50 4f 53   ...... .!   GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 00 10 00 00 20   ............... 
  0020: 00 01 32 32 32 32 32 32 32 32 32 32 32 32 04 00   ..222222222222..
  0030: 00 00 00 02 0d 00 00 36 04 00 00 14 00 00 00 20   .......6....... 
Seed 5 (id=3bb66689483f6508, size=241 bytes, fuzzer=cmplog, trial=1, discovered_at=3343s, mutation_op=DwordInterestingMutator,BytesInsertCopyMutator,BytesDeleteMutator,BytesRandInsertMutator,BitFlipMutator):
  0000: 00 01 00 00 00 01 20 02 21 20 20 20 47 50 4f 53   ...... .!   GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 00 10 00 00 20   ............... 
  0020: 00 01 32 32 32 32 32 32 32 32 32 32 32 32 05 00   ..222222222222..
  0030: 00 00 00 08 0d 00 00 36 04 00 00 14 00 00 00 20   .......6....... 

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00435add4a9bbb2f, size=32 bytes, fuzzer=naive, trial=2, discovered_at=65s, mutation_op=BytesInsertCopyMutator,BytesDeleteMutator):
  0000: ef 01 0e 00 00 0d 00 00 04 20 00 00 00 80 1a 20   ......... ..... 
  0010: 20 20 20 20 a4 20 88 00 46 46 46 87 00 46 ff f3       . ..FFF..F..
Seed 2 (id=0018364f96c64566, size=73 bytes, fuzzer=naive, trial=2, discovered_at=192s, mutation_op=ByteIncMutator,BytesSetMutator,CrossoverInsertMutator,BytesDeleteMutator,ByteInterestingMutator,CrossoverInsertMutator):
  0000: ff 08 08 08 08 08 f4 19 0d 0d 0d 0d 0d 0d 0d 0d   ................
  0010: 0d 0d 0d 0c 00 01 00 00 6e 20 20 00 00 80 00 00   ........n  .....
  0020: 00 00 00 0d 00 00 0d 00 00 00 00 6f 00 00 02 00   ...........o....
  0030: 00 6f 07 00 20 00 00 00 00 00 00 01 20 20 20 20   .o.. .......    
Seed 3 (id=004cc5a768915e91, size=176 bytes, fuzzer=naive, trial=2, discovered_at=632s, mutation_op=BytesCopyMutator):
  0000: 99 b8 b8 b8 b8 b8 7f 00 b5 05 73 61 66 63 00 ff   ..........safc..
  0010: ff df 00 00 00 00 00 00 00 00 00 80 ff ff 01 00   ................
  0020: e5 ff 10 10 10 10 10 00 36 c9 36 36 b0 b0 b0 b0   ........6.66....
  0030: b0 b0 b0 b0 b0 ff ff df 00 00 00 00 00 00 00 00   ................
Seed 4 (id=0023983db7fa1f4a, size=47 bytes, fuzzer=naive, trial=2, discovered_at=741s, mutation_op=ByteInterestingMutator,QwordAddMutator,BytesSetMutator,QwordAddMutator,BytesSwapMutator):
  0000: e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 e1 00 b6 05 00 00   ................
  0010: bb e6 89 00 57 05 40 00 00 b6 05 00 00 05 05 00   ....W.@.........
  0020: 00 b6 05 00 b6 05 00 00 b6 f8 ff ff b5 0e 00      ...............
Seed 5 (id=00049f7244268386, size=86 bytes, fuzzer=naive, trial=2, discovered_at=962s, mutation_op=BitFlipMutator,BytesSwapMutator,BytesRandInsertMutator,ByteInterestingMutator,ByteFlipMutator):
  0000: b3 05 00 00 48 00 00 20 00 01 00 00 00 00 00 ff   ....H.. ........
  0010: 00 c9 c9 c9 c9 c9 c9 c9 c9 c9 c9 c9 c9 c9 c9 c9   ................
  0020: c9 00 b6 00 00 e2 1f 04 00 20 00 01 00 00 00 00   ......... ......
  0030: 00 00 49 0e 00 00 d0 1c 00 00 b3 05 00 00 49 f1   ..I...........I.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x7                             ff(.)x2 ef(.)x1 99(.)x1 e1(.)x1 +5u  PARTIAL
   0x0001  01(.)x7                             01(.)x1 08(.)x1 b8(.)x1 e1(.)x1 +6u  PARTIAL
   0x0002  00(.)x7                             00(.)x4 0e(.)x1 08(.)x1 b8(.)x1 +3u  PARTIAL
   0x0003  00(.)x7                             00(.)x5 08(.)x1 b8(.)x1 e1(.)x1 +2u  PARTIAL
   0x0004  00(.)x7                             00(.)x2 08(.)x1 b8(.)x1 e1(.)x1 +5u  PARTIAL
   0x0005  01(.)x7                             0d(.)x1 08(.)x1 b8(.)x1 e1(.)x1 +6u  DIFFER
   0x0006  20( )x7                             00(.)x4 f4(.)x1 7f(.)x1 e1(.)x1 +3u  DIFFER
   0x0007  02(.)x5 20( )x1 21(!)x1             00(.)x4 19(.)x1 e1(.)x1 20( )x1 +3u  PARTIAL
   0x0008  21(!)x6 20( )x1                     00(.)x2 04(.)x1 0d(.)x1 b5(.)x1 +5u  DIFFER
   0x0009  20( )x7                             20( )x1 0d(.)x1 05(.)x1 e1(.)x1 +6u  PARTIAL
   0x000a  20( )x7                             00(.)x4 0d(.)x1 73(s)x1 e1(.)x1 +3u  DIFFER
   0x000b  20( )x7                             00(.)x6 0d(.)x1 61(a)x1 6c(l)x1 +1u  DIFFER
   0x000c  47(G)x6 4d(M)x1                     00(.)x6 0d(.)x1 66(f)x1 b6(.)x1 +1u  DIFFER
   0x000d  50(P)x6 41(A)x1                     00(.)x2 0c(.)x2 80(.)x1 0d(.)x1 +4u  DIFFER
   0x000e  4f(O)x6 54(T)x1                     00(.)x6 1a(.)x1 0d(.)x1 b7(.)x1 +1u  DIFFER
   0x000f  53(S)x6 48(H)x1                     00(.)x5 ff(.)x2 20( )x1 0d(.)x1 +1u  DIFFER
   0x0010  00(.)x7                             00(.)x3 20( )x1 0d(.)x1 ff(.)x1 +4u  PARTIAL
   0x0011  01(.)x7                             20( )x1 0d(.)x1 df(.)x1 e6(.)x1 +6u  DIFFER
   0x0012  00(.)x7                             20( )x2 00(.)x2 0d(.)x1 89(.)x1 +4u  PARTIAL
   0x0013  0d(.)x5 80(.)x1 27(')x1             00(.)x6 20( )x1 0c(.)x1 c9(.)x1 +1u  DIFFER
   0x0014  00(.)x7                             00(.)x4 a4(.)x1 57(W)x1 c9(.)x1 +3u  PARTIAL
   0x0015  00(.)x7                             00(.)x3 20( )x1 01(.)x1 05(.)x1 +4u  PARTIAL
   0x0016  00(.)x7                             00(.)x3 88(.)x1 40(@)x1 c9(.)x1 +4u  PARTIAL
   0x0017  10(.)x7                             00(.)x8 c9(.)x1 7c(|)x1             DIFFER
   0x0018  00(.)x7                             00(.)x5 46(F)x1 6e(n)x1 c9(.)x1 +2u  PARTIAL
   0x0019  02(.)x6 10(.)x1                     00(.)x2 0c(.)x2 46(F)x1 20( )x1 +4u  DIFFER
   0x001a  00(.)x5 03(.)x1 10(.)x1             00(.)x3 20( )x2 46(F)x1 05(.)x1 +3u  PARTIAL
   0x001b  00(.)x6 03(.)x1                     00(.)x6 87(.)x1 80(.)x1 c9(.)x1 +1u  PARTIAL
   0x001c  10(.)x5 03(.)x1 30(0)x1             00(.)x5 ff(.)x1 c9(.)x1 a0(.)x1 +2u  DIFFER
   0x001d  00(.)x5 03(.)x1 30(0)x1             00(.)x2 46(F)x1 80(.)x1 ff(.)x1 +5u  PARTIAL
   0x001e  00(.)x6 30(0)x1                     00(.)x3 ff(.)x1 01(.)x1 05(.)x1 +4u  PARTIAL
   0x001f  20( )x5 00(.)x1 30(0)x1             00(.)x6 f3(.)x1 c9(.)x1 05(.)x1 +1u  PARTIAL
   0x0020  00(.)x5 64(d)x1 2f(/)x1             00(.)x5 e5(.)x1 c9(.)x1 01(.)x1 +1u  PARTIAL
   0x0021  01(.)x6 74(t)x1                     00(.)x3 ff(.)x1 b6(.)x1 0c(.)x1 +3u  DIFFER
   0x0022  32(2)x5 04(.)x1 01(.)x1             00(.)x3 05(.)x2 10(.)x1 b6(.)x1 +2u  PARTIAL
   0x0023  32(2)x5 00(.)x1 01(.)x1             00(.)x6 0d(.)x1 10(.)x1 05(.)x1     PARTIAL
   0x0024  32(2)x5 20( )x1 00(.)x1             00(.)x4 10(.)x1 b6(.)x1 05(.)x1 +2u  PARTIAL
   0x0025  32(2)x5 02(.)x1 ff(.)x1             00(.)x3 10(.)x2 05(.)x2 e2(.)x1 +1u  DIFFER
   0x0026  32(2)x5 00(.)x1 ff(.)x1             00(.)x3 0d(.)x1 10(.)x1 1f(.)x1 +3u  PARTIAL
   0x0027  32(2)x5 04(.)x1 ff(.)x1             00(.)x7 04(.)x1 6b(k)x1             PARTIAL
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5334.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5334,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5334 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5334 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5334 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).