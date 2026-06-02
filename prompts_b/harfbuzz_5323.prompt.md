==== BLOCKER ====
Target: harfbuzz
Branch ID: 5323
Location: /src/harfbuzz/src/hb-common.cc:594:5
Enclosing function: hb_script_get_horizontal_direction
Source line:     case HB_SCRIPT_THAANA:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive)
value_profile                    8        2          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             1        9          0  loser (I2S vs value_profile)
naive_ctx                        8        2          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             9        1          0  REFERENCE
minimizer                       10        0          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.70h  loser=21.30h
  avg hitcount on branch: winner=22  loser=1
  prob_div=0.80  dur_div=16.60h  hit_div=21
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=11.50h  loser=22.00h
  avg hitcount on branch: winner=12  loser=1
  prob_div=0.70  dur_div=10.50h  hit_div=12
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5323/{W,L}/branch_coverage_show.txt

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
[W]   594      case HB_SCRIPT_THAANA: <-- BLOCKER
[ ]   595  
[ ]   596      /* Unicode-4.0 additions */
[W]   597      case HB_SCRIPT_CYPRIOT:
[ ]   598  
[ ]   599      /* Unicode-4.1 additions */
[W]   600      case HB_SCRIPT_KHAROSHTHI:
[ ]   601  
[ ]   602      /* Unicode-5.0 additions */
[W]   603      case HB_SCRIPT_PHOENICIAN:
[W]   604      case HB_SCRIPT_NKO:
[ ]   605  
[ ]   606      /* Unicode-5.1 additions */
[W]   607      case HB_SCRIPT_LYDIAN:
[ ]   608  
[ ]   609      /* Unicode-5.2 additions */
[W]   610      case HB_SCRIPT_AVESTAN:
[W]   611      case HB_SCRIPT_IMPERIAL_ARAMAIC:
[W]   612      case HB_SCRIPT_INSCRIPTIONAL_PAHLAVI:
[W]   613      case HB_SCRIPT_INSCRIPTIONAL_PARTHIAN:
[W]   614      case HB_SCRIPT_OLD_SOUTH_ARABIAN:
[W]   615      case HB_SCRIPT_OLD_TURKIC:
[W]   616      case HB_SCRIPT_SAMARITAN:
[ ]   617  
[ ]   618      /* Unicode-6.0 additions */
[W]   619      case HB_SCRIPT_MANDAIC:
[ ]   620  
[ ]   621      /* Unicode-6.1 additions */
[W]   622      case HB_SCRIPT_MEROITIC_CURSIVE:
[W]   623      case HB_SCRIPT_MEROITIC_HIEROGLYPHS:
[ ]   624  
[ ]   625      /* Unicode-7.0 additions */
[W]   626      case HB_SCRIPT_MANICHAEAN:
[W]   627      case HB_SCRIPT_MENDE_KIKAKUI:
[W]   628      case HB_SCRIPT_NABATAEAN:
[W]   629      case HB_SCRIPT_OLD_NORTH_ARABIAN:
[W]   630      case HB_SCRIPT_PALMYRENE:
[W]   631      case HB_SCRIPT_PSALTER_PAHLAVI:
[ ]   632  
[ ]   633      /* Unicode-8.0 additions */
[W]   634      case HB_SCRIPT_HATRAN:
[ ]   635  
[ ]   636      /* Unicode-9.0 additions */
[W]   637      case HB_SCRIPT_ADLAM:
[ ]   638  
[ ]   639      /* Unicode-11.0 additions */
[W]   640      case HB_SCRIPT_HANIFI_ROHINGYA:
[W]   641      case HB_SCRIPT_OLD_SOGDIAN:
[W]   642      case HB_SCRIPT_SOGDIAN:
[ ]   643  
[ ]   644      /* Unicode-12.0 additions */
[W]   645      case HB_SCRIPT_ELYMAIC:
[ ]   646  
[ ]   647      /* Unicode-13.0 additions */
[W]   648      case HB_SCRIPT_CHORASMIAN:
[W]   649      case HB_SCRIPT_YEZIDI:
[ ]   650  
[ ]   651      /* Unicode-14.0 additions */
[W]   652      case HB_SCRIPT_OLD_UYGHUR:
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
      78         0  hb-ot-shape-fallback.cc:recategorize_combining_class(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:37-166)
      78         1  hb-ot-shape.cc:zero_mark_width(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:967-970)
      37         6  hb_buffer_t::merge_clusters_impl(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-buffer.cc:512-539)
      31         1  hb-ot-shape-fallback.cc:zero_mark_advances(hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:193-206)
      31         1  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409)
      17         0  hb_buffer_reverse  (/src/harfbuzz/src/hb-buffer.cc:1602-1604)
      19         2  hb_buffer_t::sort(unsigned int, unsigned int, int (*)(hb_glyph_info_t const*, hb_glyph_info_t const*))  (/src/harfbuzz/src/hb-buffer.cc:2044-2061)
       0         2  hb_buffer_get_empty  (/src/harfbuzz/src/hb-buffer.cc:795-797)
       0         1  hb_buffer_t::delete_glyphs_inplace(bool (*)(hb_glyph_info_t const*))  (/src/harfbuzz/src/hb-buffer.cc:610-653)
       0         1  _hb_options_init()  (/src/harfbuzz/src/hb-common.cc:75-103)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097) ---
  d=5   L1036  T=338 F=0  T=129 F=212  bool adjust_offsets_when_zeroing = c->plan->adjust_mark_p...
  d=5   L1050  T=338 F=0  T=339 F=2  if (c->plan->zero_marks)
  d=5   L1053  T=0 F=338  T=2 F=337  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_EARLY:
  d=5   L1059  T=338 F=0  T=337 F=2  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
  d=5   L1065  T=338 F=0  T=339 F=2  if (c->plan->zero_marks)
  d=5   L1068  T=338 F=0  T=337 F=2  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
  d=5   L1074  T=0 F=338  T=2 F=337  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_EARLY:
  d=5   L1094  T=338 F=0  T=127 F=214  if (c->plan->fallback_mark_positioning)
--- d=4  _hb_ot_shape_fallback_mark_position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:444-465) ---
  d=4   L 449  T=0 F=338  T=0 F=127  if (!buffer->message (font, "start fallback mark"))
  d=4   L 457  T=561 F=338  T=216 F=127  for (unsigned int i = 1; i < count; i++)
--- d=3  hb-ot-shape-fallback.cc:position_cluster(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:418-437) ---
  d=3   L 419  T=796 F=34  T=341 F=1  if (end - start < 2)
  d=3   L 424  T=41 F=34  T=1 F=1  for (unsigned int i = start; i < end; i++)
  d=3   L 425  T=31 F=10  T=1 F=0  if (!_hb_glyph_info_is_unicode_mark (&info[i]))
  d=3   L 429  T=62 F=31  T=1 F=1  for (j = i + 1; j < end; j++)
  d=3   L 430  T=0 F=62  T=0 F=1  if (!_hb_glyph_info_is_unicode_mark (&info[j]))
--- d=3  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195) ---
  d=3   L1177  T=0 F=338  T=3 F=338  if (c->plan->shaper->preprocess_text &&
  d=3   L1178  T=0 F=0  T=3 F=0  c->buffer->message(c->font, "start preprocess-text"))
--- d=2  hb-ot-shape-fallback.cc:position_around_base(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-fallback.cc:322-409) ---
  d=2   L 328  T=31 F=0  T=1 F=0  if (!font->get_glyph_extents (buffer->info[base].codepoint,
--- d=1  hb_script_get_horizontal_direction  (/src/harfbuzz/src/hb-common.cc:584-666) ---
  d=1   L 586  T=338 F=34  T=381 F=0  switch ((hb_tag_t) script)
  d=1   L 594  T=34 F=338  T=0 F=381  case HB_SCRIPT_THAANA:  <-- BLOCKER

[off-chain: 138 additional divergent branches across 29 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d4ae3009a925c920, size=2 bytes, fuzzer=naive, trial=1, discovered_at=2s, mutation_op=ByteInterestingMutator,ByteIncMutator,ByteFlipMutator):
  0000: 9b 07                                             ..
Seed 2 (id=c2e49be33dd06afe, size=64 bytes, fuzzer=naive, trial=1, discovered_at=554s, mutation_op=CrossoverInsertMutator,BytesDeleteMutator,ByteDecMutator,BytesSetMutator,ByteNegMutator):
  0000: 97 07 00 00 eb 00 01 00 00 97 97 ff 20 20 21 97   ............  !.
  0010: 97 00 00 01 00 00 97 97 ff 20 20 21 97 97 00 00   .........  !....
  0020: 01 01 01 01 01 01 fe 00 00 01 00 00 97 69 ff 1f   .............i..
  0030: 69 ff 1f 20 21 00 fe 69 96 17 00 00 00 0c 00 00   i.. !..i........
Seed 3 (id=97ce48a035fcab35, size=24 bytes, fuzzer=naive, trial=1, discovered_at=688s, mutation_op=ByteDecMutator,ByteDecMutator,BytesCopyMutator,BytesDeleteMutator):
  0000: b1 07 00 00 19 06 00 00 4e 06 00 00 1a 06 ff 00   ........N.......
  0010: 4e 06 00 b1 34 07 00 00                           N...4...
Seed 4 (id=08588872cd6a09f0, size=22 bytes, fuzzer=value_profile, trial=2, discovered_at=896s, mutation_op=ByteInterestingMutator,BytesSwapMutator):
  0000: 0e 00 00 f3 40 00 00 10 ab 07 00 00 ce 0e 00 00   ....@...........
  0010: dd 08 00 00 64 08                                 ....d.
Seed 5 (id=052c530d34748e36, size=53 bytes, fuzzer=value_profile, trial=2, discovered_at=2738s, mutation_op=BitFlipMutator,BitFlipMutator):
  0000: ab 07 00 00 4e 0a 00 00 ce 0e 00 00 4e 0e 00 00   ....N.......N...
  0010: ab 64 00 00 0e 00 01 4e 0e 00 00 ab 64 00 00 4e   .d.....N....d..N
  0020: 0e 00 00 cb 2e 00 64 00 00 00 00 ce 0e 00 00 dd   ......d.........
  0030: 08 69 64 65 6d                                    .idem

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
   0x0000  ab(.)x6 ed(.)x2 9b(.)x1 97(.)x1 +7u  00(.)x19 ff(.)x1                    DIFFER
   0x0001  07(.)x10 ed(.)x2 00(.)x1 ea(.)x1 +3u  01(.)x19 00(.)x1                    PARTIAL
   0x0002  00(.)x10 b7(.)x1 ea(.)x1 ed(.)x1 +3u  00(.)x19 0c(.)x1                    PARTIAL
   0x0003  00(.)x10 f3(.)x1 b7(.)x1 ea(.)x1 +3u  00(.)x20                            PARTIAL
   0x0004  4e(N)x2 eb(.)x1 19(.)x1 40(@)x1 +11u  00(.)x19 02(.)x1                    DIFFER
   0x0005  00(.)x2 ed(.)x2 0e(.)x2 07(.)x2 +8u  01(.)x14 02(.)x3 04(.)x2 00(.)x1    PARTIAL
   0x0008  00(.)x4 4e(N)x2 ab(.)x2 ce(.)x1 +7u  21(!)x9 00(.)x5 20( )x5 5a(Z)x1     PARTIAL
   0x0009  00(.)x4 07(.)x3 0e(.)x3 06(.)x2 +4u  20( )x13 30(0)x5 5a(Z)x1 ff(.)x1    PARTIAL
   0x000b  00(.)x11 ff(.)x2 ed(.)x1 f0(.)x1 +1u  20( )x19 5a(Z)x1                    DIFFER
   0x000c  ce(.)x3 00(.)x3 1a(.)x2 ab(.)x2 +6u  47(G)x19 4d(M)x1                    DIFFER
   0x000d  0e(.)x6 06(.)x2 07(.)x2 00(.)x2 +4u  50(P)x13 53(S)x5 0c(.)x1 41(A)x1    DIFFER
   0x000e  00(.)x11 21(!)x1 ff(.)x1 06(.)x1 +2u  4f(O)x13 55(U)x5 00(.)x1 54(T)x1    PARTIAL
   0x000f  00(.)x14 97(.)x1 10(.)x1            53(S)x13 42(B)x5 00(.)x1 48(H)x1    PARTIAL
   0x0010  4e(N)x4 00(.)x2 97(.)x1 dd(.)x1 +7u  00(.)x10 20( )x7 01(.)x2 47(G)x1    PARTIAL
   0x0012  00(.)x9 05(.)x1 72(r)x1 ed(.)x1 +3u  00(.)x11 20( )x5 1e(.)x4            PARTIAL
   0x0014  00(.)x3 ab(.)x3 34(4)x2 64(d)x1 +6u  00(.)x20                            PARTIAL
   0x0015  00(.)x5 07(.)x3 0e(.)x2 08(.)x1 +4u  00(.)x19 0c(.)x1                    PARTIAL
   0x0016  00(.)x9 97(.)x1 01(.)x1 05(.)x1 +2u  00(.)x20                            PARTIAL
   0x0017  00(.)x7 97(.)x1 4e(N)x1 89(.)x1 +4u  10(.)x10 00(.)x6 18(.)x4            PARTIAL
   0x0018  0e(.)x2 6e(n)x2 4e(N)x2 ff(.)x1 +6u  00(.)x17 ff(.)x2 f6(.)x1            PARTIAL
   0x001a  00(.)x7 06(.)x2 20( )x1 6e(n)x1 +2u  00(.)x18 02(.)x1 0c(.)x1            PARTIAL
   0x0028  00(.)x5 20( )x2 2e(.)x1 1b(.)x1 +4u  00(.)x13 20( )x5 ff(.)x1 18(.)x1    PARTIAL
   0x0030  00(.)x6 07(.)x2 69(i)x1 08(.)x1 +3u  00(.)x17 47(G)x1 6e(n)x1 72(r)x1    PARTIAL
   0x0038  ff(.)x2 96(.)x1 6d(m)x1 1b(.)x1 +6u  00(.)x13 1d(.)x3 ff(.)x2 06(.)x1    PARTIAL
   0x003d  00(.)x4 0c(.)x1 a0(.)x1 6d(m)x1     00(.)x8 a0(.)x4 10(.)x3 22(")x1 +3u  PARTIAL
   0x003e  00(.)x3 07(.)x2 c2(.)x1             00(.)x10 ab(.)x2 e2(.)x1 55(U)x1 +5u  PARTIAL
   0x003f  00(.)x5 22(")x1                     00(.)x5 10(.)x2 06(.)x2 17(.)x1 +9u  PARTIAL
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
  prompts_b/harfbuzz_5323.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5323,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5323 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5323 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5323 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).