==== BLOCKER ====
Target: harfbuzz
Branch ID: 5353
Location: /src/harfbuzz/src/hb-common.cc:660:5
Enclosing function: hb_script_get_horizontal_direction
Source line:     case HB_SCRIPT_RUNIC:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            9        1          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive)
value_profile                    8        2          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)
naive_ctx                        5        5          0  REFERENCE
naive_ngram4                     6        4          0  REFERENCE
mopt                             6        4          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             8        2          0  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=13.90h  loser=22.80h
  avg hitcount on branch: winner=4  loser=1
  prob_div=0.70  dur_div=8.90h  hit_div=3
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.20h  loser=22.30h
  avg hitcount on branch: winner=9  loser=0
  prob_div=0.60  dur_div=11.10h  hit_div=9
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5353/{W,L}/branch_coverage_show.txt

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
[ ]   652      case HB_SCRIPT_OLD_UYGHUR:
[ ]   653  
[ ]   654        return HB_DIRECTION_RTL;
[ ]   655  
[ ]   656  
[ ]   657      /* https://github.com/harfbuzz/harfbuzz/issues/1000 */
[ ]   658      case HB_SCRIPT_OLD_HUNGARIAN:
[ ]   659      case HB_SCRIPT_OLD_ITALIC:
[W]   660      case HB_SCRIPT_RUNIC: <-- BLOCKER
[ ]   661  
[W]   662        return HB_DIRECTION_INVALID;
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
      86       683  hb_buffer_t::leave()  (/src/harfbuzz/src/hb-buffer.cc:329-335)
      82       662  hb_segment_properties_equal  (/src/harfbuzz/src/hb-buffer.cc:61-68)
     105       665  hb_buffer_t::add(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-buffer.cc:341-354)
      79       629  hb_buffer_set_length  (/src/harfbuzz/src/hb-buffer.cc:1451-1475)
      79       629  hb_buffer_append  (/src/harfbuzz/src/hb-buffer.cc:1903-1960)
      66       609  hb-ot-shape.cc:_hb_codepoint_is_regional_indicator(unsigned int)  (/src/harfbuzz/src/hb-ot-shape.cc:52-52)
      79       607  hb_segment_properties_overlay  (/src/harfbuzz/src/hb-buffer.cc:110-128)
      51       395  hb_buffer_t::clear()  (/src/harfbuzz/src/hb-buffer.cc:287-308)
      48       381  hb_script_get_horizontal_direction  (/src/harfbuzz/src/hb-common.cc:584-666)  <-- enclosing
      45       359  hb_buffer_set_flags  (/src/harfbuzz/src/hb-buffer.cc:1171-1176)
      44       356  hb_buffer_t::clear_positions()  (/src/harfbuzz/src/hb-buffer.cc:380-388)
      42       348  hb_buffer_t::clear_output()  (/src/harfbuzz/src/hb-buffer.cc:369-376)
      42       348  hb_buffer_t::sync()  (/src/harfbuzz/src/hb-buffer.cc:392-417)
      42       341  hb_buffer_get_glyph_positions  (/src/harfbuzz/src/hb-buffer.cc:1541-1554)
      42       341  hb_ot_shape_plan_t::substitute(hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-shape.cc:255-257)
... (73 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097) ---
  d=5   L1036  T=42 F=0  T=129 F=212  bool adjust_offsets_when_zeroing = c->plan->adjust_mark_p...
  d=5   L1042  T=0 F=42  T=0 F=341  if (c->font->has_glyph_h_origin_func ())
  d=5   L1050  T=42 F=0  T=339 F=2  if (c->plan->zero_marks)
  d=5   L1053  T=0 F=42  T=2 F=337  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_EARLY:
  d=5   L1057  T=0 F=42  T=0 F=339  default:
  d=5   L1058  T=0 F=42  T=0 F=339  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_NONE:
  d=5   L1059  T=42 F=0  T=337 F=2  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
  d=5   L1065  T=42 F=0  T=339 F=2  if (c->plan->zero_marks)
  d=5   L1068  T=42 F=0  T=337 F=2  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
  d=5   L1072  T=0 F=42  T=0 F=339  default:
  d=5   L1073  T=0 F=42  T=0 F=339  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_NONE:
  d=5   L1074  T=0 F=42  T=2 F=337  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_EARLY:
  d=5   L1082  T=0 F=42  T=0 F=341  if (c->plan->apply_morx)
  d=5   L1088  T=0 F=42  T=0 F=341  if (c->font->has_glyph_h_origin_func ())
  d=5   L1094  T=42 F=0  T=127 F=214  if (c->plan->fallback_mark_positioning)
--- d=4  _hb_ot_shape_fallback_mark_position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:444-465) ---
  d=4   L 449  T=0 F=42  T=0 F=127  if (!buffer->message (font, "start fallback mark"))
  d=4   L 457  T=66 F=42  T=216 F=127  for (unsigned int i = 1; i < count; i++)
--- d=3  hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:418-437) ---
  d=3   L 419  T=108 F=0  T=341 F=1  if (end - start < 2)
  d=3   L 424  T=0 F=0  T=1 F=1  for (unsigned int i = start; i < end; i++)
  d=3   L 425  T=0 F=0  T=1 F=0  if (!_hb_glyph_info_is_unicode_mark (&info[i]))
  d=3   L 429  T=0 F=0  T=1 F=1  for (j = i + 1; j < end; j++)
  d=3   L 430  T=0 F=0  T=0 F=1  if (!_hb_glyph_info_is_unicode_mark (&info[j]))
--- d=3  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195) ---
  d=3   L1177  T=0 F=42  T=3 F=338  if (c->plan->shaper->preprocess_text &&
  d=3   L1178  T=0 F=0  T=3 F=0  c->buffer->message(c->font, "start preprocess-text"))
--- d=2  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409) ---
  d=2   L 328  T=0 F=0  T=1 F=0  if (!font->get_glyph_extents (buffer->info[base].codepoint,
--- d=2  hb-ot-shape.cc:hb_ensure_native_direction(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:564-619) ---
  d=2   L 612  T=2 F=40  T=0 F=341  direction != horiz_dir && horiz_dir != HB_DIRECTION_INVAL...
  d=2   L 612  T=0 F=2  T=0 F=0  direction != horiz_dir && horiz_dir != HB_DIRECTION_INVAL...
--- d=1  hb_script_get_horizontal_direction  (/src/harfbuzz/src/hb-common.cc:584-666) ---
  d=1   L 586  T=43 F=5  T=381 F=0  switch ((hb_tag_t) script)
  d=1   L 589  T=0 F=48  T=0 F=381  case HB_SCRIPT_ARABIC:
  d=1   L 590  T=0 F=48  T=0 F=381  case HB_SCRIPT_HEBREW:
  d=1   L 593  T=0 F=48  T=0 F=381  case HB_SCRIPT_SYRIAC:
  d=1   L 594  T=0 F=48  T=0 F=381  case HB_SCRIPT_THAANA:
  d=1   L 597  T=0 F=48  T=0 F=381  case HB_SCRIPT_CYPRIOT:
  d=1   L 600  T=0 F=48  T=0 F=381  case HB_SCRIPT_KHAROSHTHI:
  d=1   L 603  T=0 F=48  T=0 F=381  case HB_SCRIPT_PHOENICIAN:
  d=1   L 604  T=0 F=48  T=0 F=381  case HB_SCRIPT_NKO:
  d=1   L 607  T=0 F=48  T=0 F=381  case HB_SCRIPT_LYDIAN:
  d=1   L 610  T=0 F=48  T=0 F=381  case HB_SCRIPT_AVESTAN:
  d=1   L 611  T=0 F=48  T=0 F=381  case HB_SCRIPT_IMPERIAL_ARAMAIC:
  d=1   L 612  T=0 F=48  T=0 F=381  case HB_SCRIPT_INSCRIPTIONAL_PAHLAVI:
  d=1   L 613  T=0 F=48  T=0 F=381  case HB_SCRIPT_INSCRIPTIONAL_PARTHIAN:
  d=1   L 614  T=0 F=48  T=0 F=381  case HB_SCRIPT_OLD_SOUTH_ARABIAN:
  d=1   L 615  T=0 F=48  T=0 F=381  case HB_SCRIPT_OLD_TURKIC:
  d=1   L 616  T=0 F=48  T=0 F=381  case HB_SCRIPT_SAMARITAN:
  d=1   L 619  T=0 F=48  T=0 F=381  case HB_SCRIPT_MANDAIC:
  d=1   L 622  T=0 F=48  T=0 F=381  case HB_SCRIPT_MEROITIC_CURSIVE:
  d=1   L 623  T=0 F=48  T=0 F=381  case HB_SCRIPT_MEROITIC_HIEROGLYPHS:
  d=1   L 626  T=0 F=48  T=0 F=381  case HB_SCRIPT_MANICHAEAN:
  d=1   L 627  T=0 F=48  T=0 F=381  case HB_SCRIPT_MENDE_KIKAKUI:
  d=1   L 628  T=0 F=48  T=0 F=381  case HB_SCRIPT_NABATAEAN:
  d=1   L 629  T=0 F=48  T=0 F=381  case HB_SCRIPT_OLD_NORTH_ARABIAN:
  d=1   L 630  T=0 F=48  T=0 F=381  case HB_SCRIPT_PALMYRENE:
  d=1   L 631  T=0 F=48  T=0 F=381  case HB_SCRIPT_PSALTER_PAHLAVI:
  d=1   L 634  T=0 F=48  T=0 F=381  case HB_SCRIPT_HATRAN:
  d=1   L 637  T=0 F=48  T=0 F=381  case HB_SCRIPT_ADLAM:
  d=1   L 640  T=0 F=48  T=0 F=381  case HB_SCRIPT_HANIFI_ROHINGYA:
  d=1   L 641  T=0 F=48  T=0 F=381  case HB_SCRIPT_OLD_SOGDIAN:
  d=1   L 642  T=0 F=48  T=0 F=381  case HB_SCRIPT_SOGDIAN:
  d=1   L 645  T=0 F=48  T=0 F=381  case HB_SCRIPT_ELYMAIC:
  d=1   L 648  T=0 F=48  T=0 F=381  case HB_SCRIPT_CHORASMIAN:
  d=1   L 649  T=0 F=48  T=0 F=381  case HB_SCRIPT_YEZIDI:
  d=1   L 652  T=0 F=48  T=0 F=381  case HB_SCRIPT_OLD_UYGHUR:
  d=1   L 658  T=0 F=48  T=0 F=381  case HB_SCRIPT_OLD_HUNGARIAN:
  d=1   L 659  T=0 F=48  T=0 F=381  case HB_SCRIPT_OLD_ITALIC:
  d=1   L 660  T=5 F=43  T=0 F=381  case HB_SCRIPT_RUNIC:  <-- BLOCKER

[off-chain: 184 additional divergent branches across 47 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=27fa0bdb2d06495c, size=2 bytes, fuzzer=value_profile, trial=1, discovered_at=16s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteNegMutator,BytesDeleteMutator,WordAddMutator):
  0000: f6 16                                             ..
Seed 2 (id=59e5a9e065e58987, size=58 bytes, fuzzer=naive, trial=1, discovered_at=238s, mutation_op=ByteDecMutator,BytesInsertMutator,TokenReplace,QwordAddMutator,ByteDecMutator):
  0000: e9 16 00 00 00 80 00 00 f7 00 e9 17 e9 17 00 00   ................
  0010: 00 80 00 00 00 95 17 00 13 ff 80 08 00 00 95 95   ................
  0020: 95 95 75 6b 66 64 95 95 95 95 95 95 95 95 95 95   ..ukfd..........
  0030: 95 95 95 96 95 95 00 00 0d 20                     ......... 
Seed 3 (id=1e45f4c58ba9ee62, size=13 bytes, fuzzer=naive, trial=1, discovered_at=240s, mutation_op=ByteDecMutator,BytesDeleteMutator,DwordAddMutator,ByteIncMutator):
  0000: 18 17 17 31 00 00 00 00 c6 16 00 00 e9            ...1.........

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
Seed 4 (id=000abe48ad9847bd, size=86 bytes, fuzzer=cmplog, trial=1, discovered_at=2302s, mutation_op=TokenReplace,CrossoverInsertMutator,ByteInterestingMutator,ByteNegMutator,ByteNegMutator,BytesRandInsertMutator):
  0000: 00 01 00 00 00 01 20 00 20 ff 20 20 4d 41 54 48   ...... . .  MATH
  0010: 00 01 00 00 00 00 00 10 00 10 00 22 01 01 01 00   ..........."....
  0020: 00 00 00 02 00 02 00 02 00 02 00 00 00 10 00 73   ...............s
  0030: 6e 2d 00 01 01 01 00 ff ff 00 00 17 00 00 e2 17   n-..............
Seed 5 (id=002c9ad92acce91b, size=171 bytes, fuzzer=cmplog, trial=1, discovered_at=2579s, mutation_op=BytesInsertMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 01 20 19 21 20 20 20 47 50 4f 53   ...... .!   GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 50 4f 00 00   ...........GPO..
  0020: 10 00 01 01 04 53 00 01 00 0d 00 14 01 ff fb 13   .....S..........
  0030: 72 f9 f0 01 4f 53 03 03 00 04 00 1a 43 22 55 41   r...OS......C"UA


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f6(.)x1 e9(.)x1 18(.)x1             00(.)x19 ff(.)x1                    DIFFER
   0x0001  16(.)x2 17(.)x1                     01(.)x19 00(.)x1                    DIFFER
   0x0002  00(.)x1 17(.)x1                     00(.)x19 0c(.)x1                    PARTIAL
   0x0003  00(.)x1 31(1)x1                     00(.)x20                            PARTIAL
   0x0004  00(.)x2                             00(.)x19 02(.)x1                    PARTIAL
   0x0005  80(.)x1 00(.)x1                     01(.)x14 02(.)x3 04(.)x2 00(.)x1    PARTIAL
   0x0006  00(.)x2                             20( )x7 07(.)x6 ee(.)x4 5a(Z)x1 +2u  PARTIAL
   0x0007  00(.)x2                             20( )x12 ff(.)x5 5a(Z)x1 00(.)x1 +1u  PARTIAL
   0x0008  f7(.)x1 c6(.)x1                     21(!)x9 00(.)x5 20( )x5 5a(Z)x1     DIFFER
   0x0009  00(.)x1 16(.)x1                     20( )x13 30(0)x5 5a(Z)x1 ff(.)x1    DIFFER
   0x000a  e9(.)x1 00(.)x1                     1e(.)x7 00(.)x5 20( )x5 5a(Z)x1 +2u  PARTIAL
   0x000b  17(.)x1 00(.)x1                     20( )x19 5a(Z)x1                    DIFFER
   0x000c  e9(.)x2                             47(G)x19 4d(M)x1                    DIFFER
   0x000d  17(.)x1                             50(P)x13 53(S)x5 0c(.)x1 41(A)x1    DIFFER
   0x000e  00(.)x1                             4f(O)x13 55(U)x5 00(.)x1 54(T)x1    PARTIAL
   0x000f  00(.)x1                             53(S)x13 42(B)x5 00(.)x1 48(H)x1    PARTIAL
   0x0010  00(.)x1                             00(.)x10 20( )x7 01(.)x2 47(G)x1    PARTIAL
   0x0011  80(.)x1                             01(.)x10 20( )x4 ff(.)x4 0c(.)x1 +1u  DIFFER
   0x0012  00(.)x1                             00(.)x11 20( )x5 1e(.)x4            PARTIAL
   0x0013  00(.)x1                             0d(.)x8 20( )x7 00(.)x2 27(')x1 +2u  PARTIAL
   0x0015  95(.)x1                             00(.)x19 0c(.)x1                    DIFFER
   0x0016  17(.)x1                             00(.)x20                            DIFFER
   0x0017  00(.)x1                             10(.)x10 00(.)x6 18(.)x4            PARTIAL
   0x0018  13(.)x1                             00(.)x17 ff(.)x2 f6(.)x1            DIFFER
   0x0019  ff(.)x1                             02(.)x9 ff(.)x5 01(.)x4 0c(.)x1 +1u  PARTIAL
   0x001a  80(.)x1                             00(.)x18 02(.)x1 0c(.)x1            DIFFER
   0x001b  08(.)x1                             47(G)x8 00(.)x7 ec(.)x2 22(")x1 +2u  DIFFER
   0x001c  00(.)x1                             00(.)x10 01(.)x2 ec(.)x2 02(.)x2 +4u  PARTIAL
   0x001d  00(.)x1                             00(.)x11 01(.)x3 ec(.)x2 20( )x1 +3u  PARTIAL
   0x001e  95(.)x1                             00(.)x14 ee(.)x2 ec(.)x2 01(.)x1 +1u  DIFFER
   0x001f  95(.)x1                             00(.)x8 0a(.)x3 03(.)x3 ff(.)x2 +4u  DIFFER
   0x0020  95(.)x1                             00(.)x13 10(.)x2 ff(.)x2 47(G)x1 +2u  DIFFER
   0x0021  95(.)x1                             00(.)x10 02(.)x3 30(0)x2 0c(.)x1 +4u  DIFFER
   0x0022  75(u)x1                             00(.)x10 18(.)x3 01(.)x2 0a(.)x1 +4u  DIFFER
   0x0023  6b(k)x1                             02(.)x4 e0(.)x3 08(.)x3 04(.)x2 +7u  DIFFER
   0x0024  66(f)x1                             00(.)x7 4f(O)x6 08(.)x1 04(.)x1 +5u  DIFFER
   0x0025  64(d)x1                             00(.)x7 02(.)x4 53(S)x3 ec(.)x2 +4u  DIFFER
   0x0026  95(.)x1                             00(.)x12 ab(.)x3 55(U)x2 08(.)x1 +2u  DIFFER
   0x0027  95(.)x1                             10(.)x7 42(B)x5 0c(.)x1 02(.)x1 +6u  DIFFER
   0x0028  95(.)x1                             00(.)x13 20( )x5 ff(.)x1 18(.)x1    DIFFER
   ... (17 more divergent offsets)
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
  prompts_b/harfbuzz_5353.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5353,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5353 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5353 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5353 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).