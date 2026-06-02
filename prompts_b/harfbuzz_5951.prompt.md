==== BLOCKER ====
Target: harfbuzz
Branch ID: 5951
Location: /src/harfbuzz/src/hb-ot-shaper-syllabic.cc:46:7
Enclosing function: hb_syllabic_insert_dotted_circles(hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, int, int)
Source line:   if (!font->get_nominal_glyph (0x25CCu, &dottedcircle_glyph))
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
  avg duration blocked: winner=14.80h  loser=24.00h
  avg hitcount on branch: winner=6  loser=0
  prob_div=0.80  dur_div=9.20h  hit_div=6
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5951/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_syllabic_insert_dotted_circles(hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, int, int) (/src/harfbuzz/src/hb-ot-shaper-syllabic.cc:39-88) ---
[ ]    37  				   int repha_category,
[ ]    38  				   int dottedcircle_position)
[B]    39  {
[B]    40    if (unlikely (buffer->flags & HB_BUFFER_FLAG_DO_NOT_INSERT_DOTTED_CIRCLE))
[ ]    41      return false;
[B]    42    if (likely (!(buffer->scratch_flags & HB_BUFFER_SCRATCH_FLAG_HAS_BROKEN_SYLLABLE)))
[ ]    43      return false;
[ ]    44  
[B]    45    hb_codepoint_t dottedcircle_glyph;
[B]    46    if (!font->get_nominal_glyph (0x25CCu, &dottedcircle_glyph)) <-- BLOCKER
[L]    47      return false;
[ ]    48  
[W]    49    hb_glyph_info_t dottedcircle = {0};
[W]    50    dottedcircle.codepoint = 0x25CCu;
[W]    51    dottedcircle.ot_shaper_var_u8_category() = dottedcircle_category;
[W]    52    if (dottedcircle_position != -1)
[W]    53      dottedcircle.ot_shaper_var_u8_auxiliary() = dottedcircle_position;
[W]    54    dottedcircle.codepoint = dottedcircle_glyph;
[ ]    55  
[W]    56    buffer->clear_output ();
[ ]    57  
[W]    58    buffer->idx = 0;
[W]    59    unsigned int last_syllable = 0;
[W]    60    while (buffer->idx < buffer->len && buffer->successful)
[W]    61    {
[W]    62      unsigned int syllable = buffer->cur().syllable();
[W]    63      if (unlikely (last_syllable != syllable && (syllable & 0x0F) == broken_syllable_type))
[W]    64      {
[W]    65        last_syllable = syllable;
[ ]    66  
[W]    67        hb_glyph_info_t ginfo = dottedcircle;
[W]    68        ginfo.cluster = buffer->cur().cluster;
[W]    69        ginfo.mask = buffer->cur().mask;
[W]    70        ginfo.syllable() = buffer->cur().syllable();
[ ]    71  
[ ]    72        /* Insert dottedcircle after possible Repha. */
[W]    73        if (repha_category != -1)
[W]    74        {
[W]    75  	while (buffer->idx < buffer->len && buffer->successful &&
[W]    76  	       last_syllable == buffer->cur().syllable() &&
[W]    77  	       buffer->cur().ot_shaper_var_u8_category() == (unsigned) repha_category)
[ ]    78  	  (void) buffer->next_glyph ();
[W]    79        }
[ ]    80  
[W]    81        (void) buffer->output_info (ginfo);
[W]    82      }
[W]    83      else
[W]    84        (void) buffer->next_glyph ();
[W]    85    }
[W]    86    buffer->sync ();
[W]    87    return true;
[B]    88  }

--- Caller (1 hop): hb-ot-shaper-indic.cc:initial_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:992-1011, calls hb_syllabic_insert_dotted_circles(hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, int, int) at line 998) (full body — short) ---
[B]   992  {
[B]   993    bool ret = false;
[B]   994    if (!buffer->message (font, "start reordering indic initial"))
[ ]   995      return ret;
[ ]   996  
[B]   997    update_consonant_positions_indic (plan, font, buffer);
[B]   998    if (hb_syllabic_insert_dotted_circles (font, buffer, <-- CALL
[B]   999  					 indic_broken_cluster,
[B]  1000  					 I_Cat(DOTTEDCIRCLE),
[B]  1001  					 I_Cat(Repha),
[B]  1002  					 POS_END))
[W]  1003      ret = true;
[ ]  1004  
[B]  1005    foreach_syllable (buffer, start, end)
[B]  1006      initial_reordering_syllable_indic (plan, font->face, buffer, start, end);
[ ]  1007  
[B]  1008    (void) buffer->message (font, "end reordering indic initial");
[ ]  1009  
[B]  1010    return ret;
[B]  1011  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-khmer.cc:reorder_khmer(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:311-328, calls hb_syllabic_insert_dotted_circles(hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, int, int) at line 315)
hop 2  hb-ot-shaper-myanmar.cc:reorder_myanmar(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:326-344, calls hb_syllabic_insert_dotted_circles(hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, int, int) at line 330)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      16        80  hb-ot-shaper-indic.cc:set_indic_properties(hb_glyph_info_t&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:44-50)
       0        64  hb-ot-shaper-myanmar.cc:set_myanmar_properties(hb_glyph_info_t&)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:69-74)
      19        81  hb-ot-shaper-indic.cc:decompose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1513-1539)
      16        73  hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986)
      16        73  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474)
       0        54  hb-ot-shaper-myanmar.cc:reorder_syllable_myanmar(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:308-320)
       8        40  hb-ot-shaper-indic.cc:is_one_of(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:55-59)
       5        25  hb_indic_would_substitute_feature_t::init(hb_ot_map_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:93-97)
       0        18  hb-ot-shaper-myanmar.cc:is_one_of_myanmar(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:79-83)
       0        18  hb-ot-shaper-myanmar.cc:is_consonant_myanmar(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:96-98)
       6        23  hb-ot-shaper-indic.cc:is_consonant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:72-74)
       0        16  hb-ot-shaper-khmer.cc:set_khmer_properties(hb_glyph_info_t&)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:85-90)
       0        16  hb-ot-shaper-khmer.cc:decompose_khmer(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:336-352)
       0        16  hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:181-301)
       0        15  hb-ot-shaper-khmer.cc:reorder_syllable_khmer(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:293-305)
... (33 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-khmer.cc:reorder_khmer(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:311-328) ---
  d=2   L 313  T=0 F=0  T=1 F=0  if (buffer->message (font, "start reordering khmer"))
  d=2   L 315  T=0 F=0  T=0 F=1  if (hb_syllabic_insert_dotted_circles (font, buffer,
--- d=2  hb-ot-shaper-myanmar.cc:reorder_myanmar(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:326-344) ---
  d=2   L 328  T=0 F=0  T=4 F=0  if (buffer->message (font, "start reordering myanmar"))
  d=2   L 330  T=0 F=0  T=0 F=4  if (hb_syllabic_insert_dotted_circles (font, buffer,
--- d=1  hb_syllabic_insert_dotted_circles(hb_font_t*, hb_buffer_t*, unsigned int, unsigned int, int, int)  (/src/harfbuzz/src/hb-ot-shaper-syllabic.cc:39-88) ---
  d=1   L  46  T=0 F=1  T=10 F=0  if (!font->get_nominal_glyph (0x25CCu, &dottedcircle_glyph))  <-- BLOCKER
  d=1   L  52  T=1 F=0  T=0 F=0  if (dottedcircle_position != -1)
  d=1   L  60  T=18 F=0  T=0 F=0  while (buffer->idx < buffer->len && buffer->successful)
  d=1   L  60  T=18 F=1  T=0 F=0  while (buffer->idx < buffer->len && buffer->successful)
  d=1   L  73  T=2 F=0  T=0 F=0  if (repha_category != -1)
  d=1   L  75  T=2 F=0  T=0 F=0  while (buffer->idx < buffer->len && buffer->successful &&
  d=1   L  75  T=2 F=0  T=0 F=0  while (buffer->idx < buffer->len && buffer->successful &&
  d=1   L  76  T=2 F=0  T=0 F=0  last_syllable == buffer->cur().syllable() &&
  d=1   L  77  T=0 F=2  T=0 F=0  buffer->cur().ot_shaper_var_u8_category() == (unsigned) r...

[off-chain: 168 additional divergent branches across 27 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=94ee6502f4aed8ba, size=346 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=83574s, mutation_op=TokenInsert,BytesCopyMutator,BytesRandSetMutator,ByteAddMutator,BytesInsertMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 1d 1d 00 01 00 00 00 21 11 fb 20 83 53 55 4e 20   .......!.. .SUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 00 20    ...........!.. 
  0030: 01 00 0f 00 00 00 08 00 00 00 21 00 01 20 6b 65   ..........!.. ke

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=00982e3d94b5e098, size=79 bytes, fuzzer=value_profile, trial=1, discovered_at=168s, mutation_op=CrossoverInsertMutator,BytesExpandMutator):
  0000: 20 6e 74 00 6f 74 00 86 86 86 20 20 20 86 86 86    nt.ot....   ...
  0010: 00 86 86 20 00 00 00 1a 20 cd cc cc 0c 00 00 01   ... .... .......
  0020: 00 01 00 ff 19 00 55 55 15 01 00 55 15 01 00 55   ......UU...U...U
  0030: 55 01 00 ff 19 00 55 55 15 01 00 55 15 01 00 55   U.....UU...U...U
Seed 2 (id=0181124f8674cb7d, size=35 bytes, fuzzer=value_profile, trial=1, discovered_at=466s, mutation_op=BytesDeleteMutator,ByteFlipMutator,ByteIncMutator):
  0000: 00 0c 00 00 f4 20 00 00 56 10 00 00 9c 69 61 68   ..... ..V....iah
  0010: 01 20 00 00 00 17 00 00 56 10 00 00 31 ff 00 00   . ......V...1...
  0020: 56 10 00                                          V..
Seed 3 (id=00c5be3207c3c94a, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=894s, mutation_op=BytesRandInsertMutator,ByteIncMutator,WordAddMutator,ByteNegMutator):
  0000: 97 00 ff 00 85 17 00 00 56 10 00 00 56 10 00 00   ........V...V...
  0010: 31 17 00 00 56 10 00 00 39 10 00 00 31 00 00 00   1...V...9...1...
  0020: 00 10 00 00 00 10 00 00 31 10 00 5e 5e 5e 5e 5e   ........1..^^^^^
  0030: 5e 5e 5e 5e 00 56 10 00 00                        ^^^^.V...
Seed 4 (id=00d53ef38741b3e6, size=108 bytes, fuzzer=value_profile, trial=1, discovered_at=961s, mutation_op=BitFlipMutator,BytesCopyMutator,BytesInsertMutator,QwordAddMutator):
  0000: 85 61 00 00 29 00 6c 6d 61 54 f6 01 0e 00 31 0d   .a..).lmaT....1.
  0010: 00 00 00 00 00 00 00 00 00 00 00 00 00 7e 7e 7e   .............~~~
  0020: 7e 7e 7e 7e 7e 80 10 00 00 00 00 6c 6d 61 54 f6   ~~~~~......lmaT.
  0030: 01 0e 00 31 0d 00 00 7e 7e 56 10 00 00 30 e6 00   ...1...~~V...0..
Seed 5 (id=00820f4dc302bcd4, size=68 bytes, fuzzer=value_profile, trial=1, discovered_at=2752s, mutation_op=ByteInterestingMutator,BytesInsertMutator):
  0000: 00 80 b5 00 00 10 00 00 56 10 00 00 32 10 00 ff   ........V...2...
  0010: 56 10 00 80 56 10 00 00 56 10 01 00 32 10 00 00   V...V...V...2...
  0020: 56 10 10 10 10 10 00 80 b5 00 00 00 56 10 00 1e   V...........V...
  0030: 40 10 00 00 32 10 00 00 56 10 00 00 64 10 00 00   @...2...V...d...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x1                             00(.)x6 20( )x1 97(.)x1 85(.)x1 +1u  PARTIAL
   0x0001  01(.)x1                             00(.)x2 80(.)x2 6e(n)x1 0c(.)x1 +4u  DIFFER
   0x0002  00(.)x1                             00(.)x3 b5(.)x2 74(t)x1 ff(.)x1 +3u  PARTIAL
   0x0003  00(.)x1                             00(.)x7 08(.)x1 68(h)x1 49(I)x1     PARTIAL
   0x0004  00(.)x1                             00(.)x4 6f(o)x1 f4(.)x1 85(.)x1 +3u  PARTIAL
   0x0005  07(.)x1                             00(.)x3 10(.)x2 74(t)x1 20( )x1 +3u  DIFFER
   0x0006  ff(.)x1                             00(.)x8 6c(l)x1 d7(.)x1             DIFFER
   0x0007  80(.)x1                             00(.)x6 86(.)x1 6d(m)x1 01(.)x1 +1u  DIFFER
   0x0008  20( )x1                             56(V)x5 00(.)x2 86(.)x1 61(a)x1 +1u  DIFFER
   0x0009  3f(?)x1                             10(.)x5 86(.)x1 54(T)x1 20( )x1 +2u  DIFFER
   0x000a  21(!)x1                             00(.)x5 20( )x1 f6(.)x1 ff(.)x1 +2u  DIFFER
   0x000b  20( )x1                             00(.)x6 20( )x2 01(.)x1 6e(n)x1     PARTIAL
   0x000c  63(c)x1                             20( )x2 32(2)x2 9c(.)x1 56(V)x1 +4u  DIFFER
   0x000d  6d(m)x1                             10(.)x3 00(.)x3 20( )x2 86(.)x1 +1u  DIFFER
   0x000e  61(a)x1                             00(.)x4 40(@)x2 86(.)x1 61(a)x1 +2u  PARTIAL
   0x000f  70(p)x1                             00(.)x3 ff(.)x2 86(.)x1 68(h)x1 +3u  DIFFER
   0x0010  1d(.)x1                             00(.)x3 56(V)x2 01(.)x1 31(1)x1 +3u  DIFFER
   0x0011  1d(.)x1                             10(.)x2 86(.)x1 20( )x1 17(.)x1 +5u  DIFFER
   0x0012  00(.)x1                             00(.)x6 86(.)x1 9a(.)x1 fe(.)x1 +1u  PARTIAL
   0x0013  01(.)x1                             00(.)x5 80(.)x2 20( )x1 9a(.)x1 +1u  DIFFER
   0x0014  00(.)x1                             00(.)x4 56(V)x3 9a(.)x1 7f(.)x1 +1u  PARTIAL
   0x0015  00(.)x1                             00(.)x4 10(.)x3 17(.)x1 9a(.)x1 +1u  PARTIAL
   0x0016  00(.)x1                             00(.)x8 9a(.)x1 ff(.)x1             PARTIAL
   0x0017  21(!)x1                             00(.)x6 1a(.)x1 9a(.)x1 ff(.)x1 +1u  DIFFER
   0x0018  11(.)x1                             20( )x2 56(V)x2 00(.)x2 39(9)x1 +3u  DIFFER
   0x0019  fb(.)x1                             10(.)x4 00(.)x2 ff(.)x2 cd(.)x1 +1u  DIFFER
   0x001a  20( )x1                             00(.)x5 01(.)x2 cc(.)x1 4c(L)x1 +1u  DIFFER
   0x001b  83(.)x1                             00(.)x7 cc(.)x1 4c(L)x1 47(G)x1     DIFFER
   0x001c  53(S)x1                             31(1)x2 00(.)x2 32(2)x2 0c(.)x1 +3u  DIFFER
   0x001d  55(U)x1                             00(.)x4 10(.)x2 ff(.)x1 7e(~)x1 +2u  DIFFER
   0x001e  4e(N)x1                             00(.)x8 7e(~)x1 4c(L)x1             DIFFER
   0x001f  20( )x1                             00(.)x5 01(.)x2 7e(~)x1 4c(L)x1 +1u  DIFFER
   0x0020  20( )x1                             56(V)x3 00(.)x2 7e(~)x1 4c(L)x1 +3u  PARTIAL
   0x0021  00(.)x1                             10(.)x4 01(.)x1 7e(~)x1 ff(.)x1 +3u  PARTIAL
   0x0022  00(.)x1                             00(.)x5 10(.)x2 7e(~)x1 ec(.)x1 +1u  PARTIAL
   0x0023  00(.)x1                             00(.)x2 10(.)x2 ff(.)x1 7e(~)x1 +3u  PARTIAL
   0x0024  01(.)x1                             00(.)x3 10(.)x2 19(.)x1 7e(~)x1 +2u  DIFFER
   0x0025  00(.)x1                             10(.)x3 00(.)x2 80(.)x1 48(H)x1 +1u  PARTIAL
   0x0026  00(.)x1                             00(.)x4 55(U)x1 10(.)x1 0e(.)x1 +1u  PARTIAL
   0x0027  00(.)x1                             00(.)x3 55(U)x1 80(.)x1 81(.)x1 +2u  PARTIAL
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
  prompts_b/harfbuzz_5951.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5951,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5951 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5951 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5951 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).