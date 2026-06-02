==== BLOCKER ====
Target: harfbuzz
Branch ID: 5827
Location: /src/harfbuzz/src/hb-ot-shaper-indic.cc:282:30
Enclosing function: indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const
Source line:       if (!config->virama || !font->get_nominal_glyph (config->virama, &glyph))
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           3        7          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=14.30h  loser=24.00h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=9.70h  hit_div=4
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5827/{W,L}/branch_coverage_show.txt

--- Enclosing function: indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const (/src/harfbuzz/src/hb-ot-shaper-indic.cc:278-294) ---
[ ]   276  {
[ ]   277    bool load_virama_glyph (hb_font_t *font, hb_codepoint_t *pglyph) const
[B]   278    {
[B]   279      hb_codepoint_t glyph = virama_glyph;
[B]   280      if (unlikely (glyph == (hb_codepoint_t) -1))
[B]   281      {
[B]   282        if (!config->virama || !font->get_nominal_glyph (config->virama, &glyph)) <-- BLOCKER
[L]   283  	glyph = 0;
[ ]   284        /* Technically speaking, the spec says we should apply 'locl' to virama too.
[ ]   285         * Maybe one day... */
[ ]   286  
[ ]   287        /* Our get_nominal_glyph() function needs a font, so we can't get the virama glyph
[ ]   288         * during shape planning...  Instead, overwrite it here. */
[B]   289        virama_glyph = (int) glyph;
[B]   290      }
[ ]   291  
[B]   292      *pglyph = glyph;
[B]   293      return glyph != 0;
[B]   294    }

--- Caller (1 hop): hb-ot-shaper-indic.cc:update_consonant_positions_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:443-459, calls indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const at line 447) (full body — short) ---
[B]   443  {
[B]   444    const indic_shape_plan_t *indic_plan = (const indic_shape_plan_t *) plan->data;
[ ]   445  
[B]   446    hb_codepoint_t virama;
[B]   447    if (indic_plan->load_virama_glyph (font, &virama)) <-- CALL
[W]   448    {
[W]   449      hb_face_t *face = font->face;
[W]   450      unsigned int count = buffer->len;
[W]   451      hb_glyph_info_t *info = buffer->info;
[W]   452      for (unsigned int i = 0; i < count; i++)
[W]   453        if (info[i].indic_position() == POS_BASE_C)
[ ]   454        {
[ ]   455  	hb_codepoint_t consonant = info[i].codepoint;
[ ]   456  	info[i].indic_position() = consonant_position_from_face (indic_plan, consonant, virama, face);
[ ]   457        }
[W]   458    }
[B]   459  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474, calls indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const at line 1027)
hop 2  hb-ot-shaper-indic.cc:update_consonant_positions_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:443-459, calls indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const at line 447)
hop 3  hb-ot-shaper-indic.cc:final_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1481-1495, calls hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int) at line 1487)
hop 3  hb-ot-shaper-indic.cc:initial_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:992-1011, calls hb-ot-shaper-indic.cc:update_consonant_positions_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) at line 997)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      16       160  hb-ot-shaper-indic.cc:set_indic_properties(hb_glyph_info_t&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:44-50)
      19       160  hb-ot-shaper-indic.cc:decompose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1513-1539)
      16       153  hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986)
      16       153  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474)
       8        54  hb-ot-shaper-indic.cc:is_one_of(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:55-59)
       5        50  hb_indic_would_substitute_feature_t::init(hb_ot_map_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:93-97)
       6        38  hb-ot-shaper-indic.cc:is_consonant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:72-74)
       2        23  hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:470-939)
       5        17  hb-ot-shaper-indic.cc:compose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1546-1555)
       2        13  hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:946-961)
       1        10  hb-ot-shaper-indic.cc:collect_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:241-265)
       1        10  hb-ot-shaper-indic.cc:override_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:269-272)
       1        10  indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:278-294)  <-- enclosing
       1        10  hb-ot-shaper-indic.cc:data_create_indic(hb_ot_shape_plan_t const*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:317-356)
       1        10  hb-ot-shaper-indic.cc:data_destroy_indic(void*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:360-362)
... (9 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  hb-ot-shaper-indic.cc:initial_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:992-1011) ---
  d=3   L 994  T=0 F=1  T=0 F=10  if (!buffer->message (font, "start reordering indic initi...
  d=3   L 998  T=1 F=0  T=0 F=10  if (hb_syllabic_insert_dotted_circles (font, buffer,
--- d=3  hb-ot-shaper-indic.cc:final_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1481-1495) ---
  d=3   L1485  T=1 F=0  T=10 F=0  if (buffer->message (font, "start reordering indic final"...
--- d=2  hb-ot-shaper-indic.cc:update_consonant_positions_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:443-459) ---
  d=2   L 447  T=1 F=0  T=0 F=10  if (indic_plan->load_virama_glyph (font, &virama))
  d=2   L 452  T=16 F=1  T=0 F=0  for (unsigned int i = 0; i < count; i++)
  d=2   L 453  T=0 F=16  T=0 F=0  if (info[i].indic_position() == POS_BASE_C)
--- d=2  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474) ---
  d=2   L1030  T=16 F=0  T=0 F=153  if (virama_glyph)
  d=2   L1032  T=18 F=16  T=0 F=0  for (unsigned int i = start; i < end; i++)
  d=2   L1033  T=17 F=1  T=0 F=0  if (info[i].codepoint == virama_glyph &&
  d=2   L1034  T=0 F=17  T=0 F=0  _hb_glyph_info_ligated (&info[i]) &&
  d=2   L1056  T=16 F=0  T=160 F=6  for (base = start; base < end; base++)
  d=2   L1057  T=16 F=0  T=147 F=13  if (info[base].indic_position() >= POS_BASE_C)
  d=2   L1059  T=0 F=16  T=0 F=147  if (try_pref && base + 1 < end)
  d=2   L1080  T=0 F=16  T=15 F=132  if (buffer->props.script == HB_SCRIPT_MALAYALAM)
  d=2   L1082  T=0 F=0  T=0 F=15  for (unsigned int i = base + 1; i < end; i++)
  d=2   L1099  T=0 F=16  T=0 F=147  if (start < base && info[base].indic_position() > POS_BAS...
  d=2   L1103  T=0 F=0  T=6 F=0  if (base == end && start < base &&
  d=2   L1103  T=0 F=16  T=6 F=147  if (base == end && start < base &&
  d=2   L1104  T=0 F=0  T=0 F=6  is_one_of (info[base - 1], FLAG (I_Cat(ZWJ))))
  d=2   L1106  T=16 F=0  T=147 F=6  if (base < end)
  d=2   L1107  T=0 F=16  T=0 F=147  while (start < base &&
  d=2   L1140  T=2 F=14  T=1 F=152  if (start + 1 < end && start < base) /* Otherwise there c...
  d=2   L1140  T=0 F=2  T=1 F=0  if (start + 1 < end && start < base) /* Otherwise there c...
  d=2   L1143  T=0 F=0  T=1 F=0  unsigned int new_pos = base == end ? base - 2 : base - 1;
  d=2   L1149  T=0 F=0  T=1 F=0  if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer...
  d=2   L1149  T=0 F=0  T=1 F=0  if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer...
  d=2   L1152  T=0 F=0  T=2 F=0  while (new_pos > start &&
  d=2   L1153  T=0 F=0  T=1 F=1  !(is_one_of (info[new_pos], (FLAG (I_Cat(M)) | FLAG (I_Ca...
  d=2   L1159  T=0 F=0  T=0 F=1  if (is_halant (info[new_pos]) &&
  d=2   L1193  T=0 F=0  T=0 F=1  if (start < new_pos && info[new_pos].indic_position () !=...
  d=2   L1214  T=0 F=0  T=2 F=0  for (unsigned int i = start; i < base; i++)
  d=2   L1215  T=0 F=0  T=1 F=1  if (info[i].indic_position () == POS_PRE_M) {
  d=2   L1241  T=2 F=14  T=1 F=152  if (start + 1 < end &&
  d=2   L1242  T=0 F=2  T=0 F=1  info[start].indic_position() == POS_RA_TO_BECOME_REPH &&
  d=2   L1383  T=0 F=16  T=0 F=153  if (try_pref && base + 1 < end) /* Otherwise there can't ...
  d=2   L1444  T=0 F=16  T=1 F=152  if (info[start].indic_position () == POS_PRE_M)
  d=2   L1446  T=0 F=0  T=0 F=1  if (!start ||
  d=2   L1447  T=0 F=0  T=1 F=0  !(FLAG_UNSAFE (_hb_glyph_info_get_general_category (&info...
  d=2   L1458  T=0 F=16  T=0 F=153  if (indic_plan->uniscribe_bug_compatible)
--- d=1  indic_shape_plan_t::load_virama_glyph(hb_font_t*, unsigned int*) const  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:278-294) ---
  d=1   L 282  T=0 F=1  T=10 F=0  if (!config->virama || !font->get_nominal_glyph (config->...  <-- BLOCKER
  d=1   L 282  T=0 F=1  T=0 F=10  if (!config->virama || !font->get_nominal_glyph (config->...  <-- BLOCKER

[off-chain: 76 additional divergent branches across 10 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=94ee6502f4aed8ba, size=346 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=83574s, mutation_op=TokenInsert,BytesCopyMutator,BytesRandSetMutator,ByteAddMutator,BytesInsertMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 1d 1d 00 01 00 00 00 21 11 fb 20 83 53 55 4e 20   .......!.. .SUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 00 20    ...........!.. 
  0030: 01 00 0f 00 00 00 08 00 00 00 21 00 01 20 6b 65   ..........!.. ke

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0097c8dd9cd41be2, size=31 bytes, fuzzer=value_profile, trial=1, discovered_at=8s, mutation_op=BitFlipMutator,BitFlipMutator,QwordAddMutator,WordInterestingMutator):
  0000: 10 09 00 00 00 10 0e 00 00 80 00 01 8a 8a 8a 8a   ................
  0010: 8a 8a 03 01 01 01 00 1a 20 20 20 20 01 00 00      ........    ...
Seed 2 (id=00982e3d94b5e098, size=79 bytes, fuzzer=value_profile, trial=1, discovered_at=168s, mutation_op=CrossoverInsertMutator,BytesExpandMutator):
  0000: 20 6e 74 00 6f 74 00 86 86 86 20 20 20 86 86 86    nt.ot....   ...
  0010: 00 86 86 20 00 00 00 1a 20 cd cc cc 0c 00 00 01   ... .... .......
  0020: 00 01 00 ff 19 00 55 55 15 01 00 55 15 01 00 55   ......UU...U...U
  0030: 55 01 00 ff 19 00 55 55 15 01 00 55 15 01 00 55   U.....UU...U...U
Seed 3 (id=007919f0d9af18e6, size=109 bytes, fuzzer=value_profile, trial=1, discovered_at=250s, mutation_op=BytesCopyMutator,WordInterestingMutator,ByteFlipMutator,CrossoverInsertMutator):
  0000: 02 02 02 02 02 02 02 02 02 0b 00 00 00 00 80 00   ................
  0010: 00 dd dd dd f0 80 ff 00 10 0b 00 00 80 20 ff f3   ............. ..
  0020: 00 01 e4 38 32 32 32 00 01 1a e6 1a 1a 00 00 ff   ...8222.........
  0030: e8 1a ce ce ce 1f 20 10 00 20 95 65 81 6e 00 20   ...... .. .e.n. 
Seed 4 (id=0148a08e11b87af8, size=144 bytes, fuzzer=value_profile, trial=1, discovered_at=2874s, mutation_op=CrossoverReplaceMutator,WordInterestingMutator,TokenReplace,TokenInsert):
  0000: 00 63 ca 08 00 00 d7 00 00 20 ff 20 20 00 cd c4   .c....... .  ...
  0010: cc 0c fe ff 7f 00 00 00 00 ff 7f 00 00 00 00 01   ................
  0020: 20 0c 08 08 08 08 08 08 08 08 d3 08 0f 00 d7 08    ...............
  0030: 08 00 00 ce 08 00 20 d7 08 00 00 e1 0c 00 00 19   ...... .........
Seed 5 (id=00de9724b738cefb, size=37 bytes, fuzzer=value_profile, trial=1, discovered_at=7821s, mutation_op=BytesSetMutator):
  0000: 00 00 00 68 80 31 00 01 00 00 61 6e ff 20 00 00   ...h.1....an. ..
  0010: df 1c 00 00 92 0b ff ff ff 20 00 00 df 1c 00 00   ......... ......
  0020: ff 0a 00 00 00                                    .....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x1                             20( )x2 00(.)x2 10(.)x1 02(.)x1 +4u  PARTIAL
   0x0001  01(.)x1                             00(.)x2 09(.)x1 6e(n)x1 02(.)x1 +5u  DIFFER
   0x0002  00(.)x1                             00(.)x4 74(t)x1 02(.)x1 ca(.)x1 +3u  PARTIAL
   0x0003  00(.)x1                             00(.)x3 02(.)x1 08(.)x1 68(h)x1 +4u  PARTIAL
   0x0004  00(.)x1                             00(.)x2 6f(o)x1 02(.)x1 80(.)x1 +5u  PARTIAL
   0x0005  07(.)x1                             00(.)x2 10(.)x1 74(t)x1 02(.)x1 +5u  DIFFER
   0x0006  ff(.)x1                             00(.)x6 0e(.)x1 02(.)x1 d7(.)x1 +1u  DIFFER
   0x0007  80(.)x1                             00(.)x6 86(.)x1 02(.)x1 01(.)x1 +1u  DIFFER
   0x0008  20( )x1                             00(.)x5 86(.)x1 02(.)x1 19(.)x1 +2u  DIFFER
   0x0009  3f(?)x1                             80(.)x1 86(.)x1 0b(.)x1 20( )x1 +6u  DIFFER
   0x000a  21(!)x1                             00(.)x4 20( )x1 ff(.)x1 61(a)x1 +3u  DIFFER
   0x000b  20( )x1                             00(.)x5 20( )x2 01(.)x1 6e(n)x1 +1u  PARTIAL
   0x000c  63(c)x1                             20( )x3 00(.)x2 8a(.)x1 ff(.)x1 +3u  DIFFER
   0x000d  6d(m)x1                             00(.)x4 20( )x3 8a(.)x1 86(.)x1 +1u  DIFFER
   0x000e  61(a)x1                             00(.)x4 8a(.)x1 86(.)x1 80(.)x1 +3u  DIFFER
   0x000f  70(p)x1                             00(.)x5 8a(.)x1 86(.)x1 c4(.)x1 +2u  DIFFER
   0x0010  1d(.)x1                             00(.)x5 df(.)x2 8a(.)x1 cc(.)x1 +1u  PARTIAL
   0x0011  1d(.)x1                             8a(.)x1 86(.)x1 dd(.)x1 0c(.)x1 +6u  DIFFER
   0x0012  00(.)x1                             00(.)x3 03(.)x1 86(.)x1 dd(.)x1 +4u  PARTIAL
   0x0013  01(.)x1                             00(.)x4 01(.)x1 20( )x1 dd(.)x1 +3u  PARTIAL
   0x0014  00(.)x1                             00(.)x4 01(.)x1 f0(.)x1 7f(.)x1 +3u  PARTIAL
   0x0015  00(.)x1                             00(.)x3 01(.)x1 80(.)x1 0b(.)x1 +4u  PARTIAL
   0x0016  00(.)x1                             00(.)x6 ff(.)x2 01(.)x1 61(a)x1     PARTIAL
   0x0017  21(!)x1                             00(.)x5 1a(.)x2 ff(.)x1 61(a)x1 +1u  DIFFER
   0x0018  11(.)x1                             20( )x4 00(.)x3 10(.)x1 ff(.)x1 +1u  DIFFER
   0x0019  fb(.)x1                             20( )x3 cd(.)x1 0b(.)x1 ff(.)x1 +4u  DIFFER
   0x001a  20( )x1                             00(.)x4 0a(.)x2 20( )x1 cc(.)x1 +2u  PARTIAL
   0x001b  83(.)x1                             00(.)x6 20( )x1 cc(.)x1 01(.)x1 +1u  DIFFER
   0x001c  53(S)x1                             00(.)x3 df(.)x2 01(.)x1 0c(.)x1 +3u  DIFFER
   0x001d  55(U)x1                             00(.)x4 20( )x3 a0(.)x2 1c(.)x1     DIFFER
   0x001e  4e(N)x1                             00(.)x9 ff(.)x1                     DIFFER
   0x001f  20( )x1                             00(.)x4 01(.)x2 f3(.)x1 6e(n)x1 +1u  DIFFER
   0x0020  20( )x1                             00(.)x5 20( )x1 ff(.)x1 2d(-)x1 +1u  PARTIAL
   0x0021  00(.)x1                             01(.)x2 00(.)x2 0c(.)x1 0a(.)x1 +3u  PARTIAL
   0x0022  00(.)x1                             00(.)x6 e4(.)x1 08(.)x1 7f(.)x1     PARTIAL
   0x0023  00(.)x1                             00(.)x2 ff(.)x1 38(8)x1 08(.)x1 +4u  PARTIAL
   0x0024  01(.)x1                             00(.)x3 19(.)x1 32(2)x1 08(.)x1 +3u  DIFFER
   0x0025  00(.)x1                             00(.)x4 32(2)x1 08(.)x1 25(%)x1 +1u  PARTIAL
   0x0026  00(.)x1                             00(.)x2 55(U)x1 32(2)x1 08(.)x1 +3u  PARTIAL
   0x0027  00(.)x1                             00(.)x2 55(U)x1 08(.)x1 68(h)x1 +3u  PARTIAL
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
  prompts_b/harfbuzz_5827.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5827,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5827 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5827 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5827 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).