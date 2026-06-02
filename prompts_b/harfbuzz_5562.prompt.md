==== BLOCKER ====
Target: harfbuzz
Branch ID: 5562
Location: /src/harfbuzz/src/hb-ot-layout.cc:573:7
Enclosing function: hb_ot_layout_table_select_script
Source line:   if (g.find_script_index (HB_OT_TAG_DEFAULT_LANGUAGE, script_index)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    0       10          0  REFERENCE
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=9.70h  loser=24.00h
  avg hitcount on branch: winner=297  loser=0
  prob_div=0.80  dur_div=14.30h  hit_div=297
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5562/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_ot_layout_table_select_script (/src/harfbuzz/src/hb-ot-layout.cc:550-591) ---
[ ]   548  				  unsigned int   *script_index  /* OUT */,
[ ]   549  				  hb_tag_t       *chosen_script /* OUT */)
[B]   550  {
[B]   551    static_assert ((OT::Index::NOT_FOUND_INDEX == HB_OT_LAYOUT_NO_SCRIPT_INDEX), "");
[B]   552    const OT::GSUBGPOS &g = get_gsubgpos_table (face, table_tag);
[B]   553    unsigned int i;
[ ]   554  
[B]   555    for (i = 0; i < script_count; i++)
[B]   556    {
[B]   557      if (g.find_script_index (script_tags[i], script_index))
[ ]   558      {
[ ]   559        if (chosen_script)
[ ]   560  	*chosen_script = script_tags[i];
[ ]   561        return true;
[ ]   562      }
[B]   563    }
[ ]   564  
[ ]   565    /* try finding 'DFLT' */
[B]   566    if (g.find_script_index (HB_OT_TAG_DEFAULT_SCRIPT, script_index)) {
[ ]   567      if (chosen_script)
[ ]   568        *chosen_script = HB_OT_TAG_DEFAULT_SCRIPT;
[ ]   569      return false;
[ ]   570    }
[ ]   571  
[ ]   572    /* try with 'dflt'; MS site has had typos and many fonts use it now :( */
[B]   573    if (g.find_script_index (HB_OT_TAG_DEFAULT_LANGUAGE, script_index)) { <-- BLOCKER
[W]   574      if (chosen_script)
[W]   575        *chosen_script = HB_OT_TAG_DEFAULT_LANGUAGE;
[W]   576      return false;
[W]   577    }
[ ]   578  
[ ]   579    /* try with 'latn'; some old fonts put their features there even though
[ ]   580       they're really trying to support Thai, for example :( */
[B]   581    if (g.find_script_index (HB_OT_TAG_LATIN_SCRIPT, script_index)) {
[ ]   582      if (chosen_script)
[ ]   583        *chosen_script = HB_OT_TAG_LATIN_SCRIPT;
[ ]   584      return false;
[ ]   585    }
[ ]   586  
[B]   587    if (script_index) *script_index = HB_OT_LAYOUT_NO_SCRIPT_INDEX;
[B]   588    if (chosen_script)
[B]   589      *chosen_script = HB_TAG_NONE;
[B]   590    return false;
[B]   591  }

--- Caller (1 hop): hb_ot_map_builder_t::hb_ot_map_builder_t(hb_face_t*, hb_segment_properties_t const&) (/src/harfbuzz/src/hb-ot-map.cc:47-88, calls hb_ot_layout_table_select_script at line 75) (±10 around call site) ---
[B]    65    hb_ot_tags_from_script_and_language (props.script,
[B]    66  				       props.language,
[B]    67  				       &script_count,
[B]    68  				       script_tags,
[B]    69  				       &language_count,
[B]    70  				       language_tags);
[ ]    71  
[B]    72    for (unsigned int table_index = 0; table_index < 2; table_index++)
[B]    73    {
[B]    74      hb_tag_t table_tag = table_tags[table_index];
[B]    75      found_script[table_index] = (bool) hb_ot_layout_table_select_script (face, <-- CALL
[B]    76  									 table_tag,
[B]    77  									 script_count,
[B]    78  									 script_tags,
[B]    79  									 &script_index[table_index],
[B]    80  									 &chosen_script[table_index]);
[B]    81      hb_ot_layout_script_select_language (face,
[B]    82  					 table_tag,
[B]    83  					 script_index[table_index],
[B]    84  					 language_count,
[B]    85  					 language_tags,

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb_ot_layout_table_choose_script  (/src/harfbuzz/src/hb-ot-layout.cc:514-518, calls hb_ot_layout_table_select_script at line 517)
hop 2  hb_ot_map_builder_t::hb_ot_map_builder_t(hb_face_t*, hb_segment_properties_t const&)  (/src/harfbuzz/src/hb-ot-map.cc:47-88, calls hb_ot_layout_table_select_script at line 75)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     478      3880  hb-ot-layout.cc:get_gsubgpos_table(hb_face_t*, unsigned int)  (/src/harfbuzz/src/hb-ot-layout.cc:416-422)
     263      2280  hb_ot_layout_language_find_feature  (/src/harfbuzz/src/hb-ot-layout.cc:995-1012)
     130      1190  hb_ot_map_builder_t::add_feature(unsigned int, hb_ot_map_feature_flags_t, unsigned int)  (/src/harfbuzz/src/hb-ot-map.cc:100-110)
     136       914  hb_ot_layout_table_find_feature_variations  (/src/harfbuzz/src/hb-ot-layout.cc:1399-1403)
      63       420  hb-ot-layout.cc:_hb_ot_layout_set_glyph_props(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:255-265)
      63       420  hb_ot_layout_substitute_start(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1510-1512)
      63       420  hb_ot_layout_position_start(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1611-1613)
      63       420  hb_ot_layout_position_finish_advances(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1626-1628)
      63       420  hb_ot_layout_position_finish_offsets(hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1640-1642)
      63       420  GSUBProxy::GSUBProxy(hb_face_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1833-1834)
      63       420  hb_ot_map_t::substitute(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:2001-2008)
     105       420  void hb_ot_map_t::apply<GSUBProxy>(GSUBProxy const&, hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:1948-1998)
     105       420  void hb_ot_map_t::apply<GPOSProxy>(GPOSProxy const&, hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:1948-1998)
      15       241  hb_ot_map_builder_t::add_pause(unsigned int, bool (*)(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*))  (/src/harfbuzz/src/hb-ot-map.cc:175-181)
      20       202  hb_ot_layout_table_get_lookup_count  (/src/harfbuzz/src/hb-ot-layout.cc:1066-1068)
... (25 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb_ot_map_builder_t::hb_ot_map_builder_t(hb_face_t*, hb_segment_properties_t const&)  (/src/harfbuzz/src/hb-ot-map.cc:47-88) ---
  d=2   L  51  T=10 F=5  T=74 F=37  for (unsigned int table_index = 0; table_index < 2; table...
  d=2   L  72  T=10 F=5  T=74 F=37  for (unsigned int table_index = 0; table_index < 2; table...
--- d=1  hb_ot_layout_table_select_script  (/src/harfbuzz/src/hb-ot-layout.cc:550-591) ---
  d=1   L 555  T=10 F=10  T=78 F=74  for (i = 0; i < script_count; i++)
  d=1   L 557  T=0 F=10  T=0 F=78  if (g.find_script_index (script_tags[i], script_index))
  d=1   L 566  T=0 F=10  T=0 F=74  if (g.find_script_index (HB_OT_TAG_DEFAULT_SCRIPT, script...
  d=1   L 573  T=5 F=5  T=0 F=74  if (g.find_script_index (HB_OT_TAG_DEFAULT_LANGUAGE, scri...  <-- BLOCKER
  d=1   L 574  T=5 F=0  T=0 F=0  if (chosen_script)
  d=1   L 581  T=0 F=5  T=0 F=74  if (g.find_script_index (HB_OT_TAG_LATIN_SCRIPT, script_i...
  d=1   L 587  T=5 F=0  T=74 F=0  if (script_index) *script_index = HB_OT_LAYOUT_NO_SCRIPT_...
  d=1   L 588  T=5 F=0  T=74 F=0  if (chosen_script)

[off-chain: 98 additional divergent branches across 16 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=8566af241913059b, size=210 bytes, fuzzer=cmplog, trial=2, discovered_at=2758s, mutation_op=CrossoverInsertMutator,DwordAddMutator,WordInterestingMutator,BytesRandSetMutator):
  0000: 00 01 00 00 00 08 00 00 00 18 df 20 47 50 4f 53   ........... GPOS
  0010: 02 04 00 06 00 00 00 00 00 1d 00 f8 17 00 00 53   ...............S
  0020: 53 53 53 53 53 53 53 e8 e8 e8 e8 e8 e8 e8 e8 e8   SSSSSSS.........
  0030: 20 8e 8d 08 06 00 24 bd 92 04 4f 53 36 00 1f 01    .....$...OS6...
Seed 2 (id=3bde8534ed42652a, size=208 bytes, fuzzer=cmplog, trial=2, discovered_at=2784s, mutation_op=ByteFlipMutator,BytesSetMutator,QwordAddMutator,TokenInsert):
  0000: 00 01 00 00 00 08 00 00 00 18 df 20 47 53 55 42   ........... GSUB
  0010: 02 01 02 00 00 00 00 00 00 1d 00 f8 16 00 00 53   ...............S
  0020: 53 53 53 53 80 03 04 00 00 06 00 00 00 00 00 00   SSSS............
  0030: 00 d2 d2 00 00 02 00 00 06 64 00 0c 00 0c 00 1f   .........d......
Seed 3 (id=2bfee40d172f24c2, size=497 bytes, fuzzer=cmplog, trial=2, discovered_at=37463s, mutation_op=ByteInterestingMutator,ByteIncMutator,BytesDeleteMutator,BytesCopyMutator,BytesSetMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 02 02 00 00 18 df 20 47 50 4f 53   ........... GPOS
  0010: 02 04 00 06 00 00 00 f4 00 2c 2c 2c 17 00 00 a5   .........,,,....
  0020: a5 a5 53 53 54 53 53 53 00 06 00 80 00 20 7f 24   ..SSTSSS..... .$
  0030: 9a 92 02 4f 00 00 00 10 00 01 02 1e 02 00 00 10   ...O............

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003817559785f774, size=6 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteDecMutator,WordAddMutator):
  0000: 87 0e 0d 0e 22 0e                                 ....".
Seed 2 (id=002edec370c771cf, size=35 bytes, fuzzer=naive, trial=1, discovered_at=47s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteNegMutator,TokenInsert,ByteIncMutator,ByteRandMutator):
  0000: 00 00 00 00 00 00 00 00 00 00 00 00 20 00 64 6f   ............ .do
  0010: 2d 68 0a 6f 74 00 0e 00 20 00 0c 00 0c 09 00 00   -h.ot... .......
  0020: 00 0c 00                                          ...
Seed 3 (id=0016e7ecc5a956f6, size=64 bytes, fuzzer=naive, trial=1, discovered_at=308s, mutation_op=BytesRandInsertMutator,ByteRandMutator):
  0000: 00 75 fe 2d 68 67 68 77 72 75 75 75 80 17 00 00   .u.-hghwruuu....
  0010: 00 20 00 00 23 91 01 9f 9f 9f 9f f3 00 00 00 00   . ..#...........
  0020: 00 00 02 02 02 02 02 02 02 02 00 00 00 00 00 00   ................
  0030: fe fc fe ff 01 20 00 00 00 00 10 00 00 a7 00 00   ..... ..........
Seed 4 (id=004e0915513f9329, size=63 bytes, fuzzer=naive, trial=2, discovered_at=448s, mutation_op=BytesExpandMutator,ByteNegMutator):
  0000: 18 06 00 00 62 6e 69 66 34 80 fa ff ff 00 01 00   ....bnif4.......
  0010: 00 00 01 00 01 00 01 20 20 00 01 00 01 00 01 20   .......  ...... 
  0020: 20 20 fa ff ff 00 01 00 00 cd cc cc 0c 00 01 00     ..............
  0030: 53 53 01 20 20 20 ae ae 20 91 91 91 6f 05 01      SS.   .. ...o..
Seed 5 (id=0002ee9aae2b9bef, size=54 bytes, fuzzer=naive, trial=1, discovered_at=470s, mutation_op=WordInterestingMutator,TokenInsert,BytesExpandMutator,ByteInterestingMutator):
  0000: 00 ff 00 00 1d 20 00 00 c8 0a 01 00 70 78 2d 68   ..... ......px-h
  0010: 61 6e 74 2d 68 6b 00 74 40 01 00 00 00 20 01 00   ant-hk.t@.... ..
  0020: c8 0a 01 00 40 62 91 6d 00 00 00 20 01 00 c8 7f   ....@b.m... ....
  0030: 01 00 40 62 91 6d                                 ..@b.m


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x3                             00(.)x7 05(.)x2 87(.)x1 18(.)x1 +9u  PARTIAL
   0x0001  01(.)x3                             00(.)x3 f6(.)x2 18(.)x2 05(.)x2 +10u  PARTIAL
   0x0002  00(.)x3                             00(.)x12 ff(.)x3 0d(.)x1 fe(.)x1 +3u  PARTIAL
   0x0003  00(.)x3                             00(.)x12 2d(-)x2 0e(.)x1 71(q)x1 +4u  PARTIAL
   0x0004  00(.)x3                             00(.)x3 68(h)x2 70(p)x2 22(")x1 +12u  PARTIAL
   0x0005  08(.)x2 02(.)x1                     0e(.)x2 00(.)x2 20( )x2 67(g)x1 +13u  DIFFER
   0x0006  00(.)x2 02(.)x1                     00(.)x10 68(h)x1 69(i)x1 f6(.)x1 +6u  PARTIAL
   0x0007  00(.)x3                             00(.)x10 f6(.)x2 77(w)x1 66(f)x1 +5u  PARTIAL
   0x0008  00(.)x3                             00(.)x2 72(r)x1 34(4)x1 c8(.)x1 +14u  PARTIAL
   0x0009  18(.)x3                             20( )x2 ff(.)x2 00(.)x1 75(u)x1 +13u  DIFFER
   0x000a  df(.)x3                             00(.)x8 01(.)x2 75(u)x1 fa(.)x1 +7u  DIFFER
   0x000b  20( )x3                             00(.)x9 ff(.)x2 75(u)x1 1a(.)x1 +6u  DIFFER
   0x000c  47(G)x3                             ff(.)x2 00(.)x2 0f(.)x2 20( )x1 +12u  DIFFER
   0x000d  50(P)x2 53(S)x1                     00(.)x5 17(.)x1 78(x)x1 f6(.)x1 +11u  DIFFER
   0x000e  4f(O)x2 55(U)x1                     00(.)x9 01(.)x2 64(d)x1 2d(-)x1 +6u  DIFFER
   0x000f  53(S)x2 42(B)x1                     00(.)x8 19(.)x2 6f(o)x1 68(h)x1 +7u  DIFFER
   0x0010  02(.)x3                             00(.)x7 01(.)x2 2d(-)x1 61(a)x1 +8u  DIFFER
   0x0011  04(.)x2 01(.)x1                     00(.)x4 20( )x2 18(.)x2 68(h)x1 +10u  PARTIAL
   0x0012  00(.)x2 02(.)x1                     00(.)x11 05(.)x2 0a(.)x1 01(.)x1 +4u  PARTIAL
   0x0013  06(.)x2 00(.)x1                     00(.)x11 2d(-)x2 6f(o)x1 3b(;)x1 +4u  PARTIAL
   0x0014  00(.)x3                             68(h)x3 00(.)x2 74(t)x1 23(#)x1 +12u  PARTIAL
   0x0015  00(.)x3                             00(.)x4 01(.)x2 91(.)x1 6b(k)x1 +11u  PARTIAL
   0x0016  00(.)x3                             00(.)x7 0e(.)x2 01(.)x2 2d(-)x1 +7u  PARTIAL
   0x0017  00(.)x2 f4(.)x1                     00(.)x8 74(t)x2 9f(.)x1 20( )x1 +7u  PARTIAL
   0x0018  00(.)x3                             00(.)x4 20( )x3 9f(.)x1 40(@)x1 +10u  PARTIAL
   0x0019  1d(.)x2 2c(,)x1                     00(.)x3 01(.)x2 9f(.)x1 1a(.)x1 +12u  DIFFER
   0x001a  00(.)x2 2c(,)x1                     00(.)x5 01(.)x3 0c(.)x1 9f(.)x1 +9u  PARTIAL
   0x001b  f8(.)x2 2c(,)x1                     00(.)x8 ff(.)x3 f3(.)x1 1a(.)x1 +6u  DIFFER
   0x001c  17(.)x2 16(.)x1                     00(.)x7 0c(.)x1 01(.)x1 2d(-)x1 +9u  DIFFER
   0x001d  00(.)x3                             00(.)x6 09(.)x1 20( )x1 68(h)x1 +10u  PARTIAL
   0x001e  00(.)x3                             00(.)x8 01(.)x3 61(a)x1 70(p)x1 +6u  PARTIAL
   0x001f  53(S)x2 a5(.)x1                     00(.)x9 20( )x2 19(.)x1 6e(n)x1 +5u  DIFFER
   0x0020  53(S)x2 a5(.)x1                     00(.)x3 01(.)x2 20( )x1 c8(.)x1 +11u  DIFFER
   0x0021  53(S)x2 a5(.)x1                     00(.)x4 20( )x2 10(.)x2 ff(.)x2 +8u  DIFFER
   0x0022  53(S)x3                             00(.)x6 01(.)x3 02(.)x1 fa(.)x1 +6u  DIFFER
   0x0023  53(S)x3                             00(.)x5 02(.)x1 ff(.)x1 19(.)x1 +7u  DIFFER
   0x0024  53(S)x1 80(.)x1 54(T)x1             00(.)x3 02(.)x1 ff(.)x1 40(@)x1 +8u  DIFFER
   0x0025  53(S)x2 03(.)x1                     00(.)x4 02(.)x1 62(b)x1 74(t)x1 +7u  DIFFER
   0x0026  53(S)x2 04(.)x1                     00(.)x3 01(.)x2 61(a)x2 02(.)x1 +6u  DIFFER
   0x0027  e8(.)x1 00(.)x1 53(S)x1             00(.)x2 02(.)x1 6d(m)x1 30(0)x1 +9u  PARTIAL
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
  prompts_b/harfbuzz_5562.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5562,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5562 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5562 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5562 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).