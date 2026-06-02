==== BLOCKER ====
Target: harfbuzz
Branch ID: 5745
Location: /src/harfbuzz/src/hb-ot-shaper-arabic-fallback.hh:131:9
Enclosing function: hb-ot-shaper-arabic.cc:OT::Layout::GSUB_impl::SubstLookup* arabic_fallback_synthesize_lookup_ligature<ligature_3_set_t [1]>(hb_ot_shape_plan_t const*, hb_font_t*, ligature_3_set_t const (&) [1], unsigned int)
Source line:     if (!hb_font_get_glyph (font, first_u, 0, &first_glyph))
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
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=14.10h  loser=24.00h
  avg hitcount on branch: winner=45  loser=0
  prob_div=0.80  dur_div=9.90h  hit_div=45
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5745/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-arabic.cc:OT::Layout::GSUB_impl::SubstLookup* arabic_fallback_synthesize_lookup_ligature<ligature_3_set_t [1]>(hb_ot_shape_plan_t const*, hb_font_t*, ligature_3_set_t const (&) [1], unsigned int) (/src/harfbuzz/src/hb-ot-shaper-arabic-fallback.hh:110-201) ---
[ ]   108  					    const T &ligature_table,
[ ]   109  					    unsigned lookup_flags)
[B]   110  {
[B]   111    OT::HBGlyphID16 first_glyphs[ARRAY_LENGTH_CONST (ligature_table)];
[B]   112    unsigned int first_glyphs_indirection[ARRAY_LENGTH_CONST (ligature_table)];
[B]   113    unsigned int ligature_per_first_glyph_count_list[ARRAY_LENGTH_CONST (first_glyphs)];
[B]   114    unsigned int num_first_glyphs = 0;
[ ]   115  
[ ]   116    /* We know that all our ligatures have the same number of components. */
[B]   117    OT::HBGlyphID16 ligature_list[ARRAY_LENGTH_CONST (first_glyphs) * ARRAY_LENGTH_CONST(ligature_table[0].ligatures)];
[B]   118    unsigned int component_count_list[ARRAY_LENGTH_CONST (ligature_list)];
[B]   119    OT::HBGlyphID16 component_list[ARRAY_LENGTH_CONST (ligature_list) *
[B]   120  				 ARRAY_LENGTH_CONST (ligature_table[0].ligatures[0].components)];
[B]   121    unsigned int num_ligatures = 0;
[B]   122    unsigned int num_components = 0;
[ ]   123  
[ ]   124    /* Populate arrays */
[ ]   125  
[ ]   126    /* Sort out the first-glyphs */
[B]   127    for (unsigned int first_glyph_idx = 0; first_glyph_idx < ARRAY_LENGTH (first_glyphs); first_glyph_idx++)
[B]   128    {
[B]   129      hb_codepoint_t first_u = ligature_table[first_glyph_idx].first;
[B]   130      hb_codepoint_t first_glyph;
[B]   131      if (!hb_font_get_glyph (font, first_u, 0, &first_glyph)) <-- BLOCKER
[B]   132        continue;
[W]   133      first_glyphs[num_first_glyphs] = first_glyph;
[W]   134      ligature_per_first_glyph_count_list[num_first_glyphs] = 0;
[W]   135      first_glyphs_indirection[num_first_glyphs] = first_glyph_idx;
[W]   136      num_first_glyphs++;
[W]   137    }
[B]   138    hb_stable_sort (&first_glyphs[0], num_first_glyphs,
[B]   139  		  (int(*)(const OT::HBUINT16*, const OT::HBUINT16 *)) OT::HBGlyphID16::cmp,
[B]   140  		  &first_glyphs_indirection[0]);
[ ]   141  
[ ]   142    /* Now that the first-glyphs are sorted, walk again, populate ligatures. */
[B]   143    for (unsigned int i = 0; i < num_first_glyphs; i++)
[W]   144    {
[W]   145      unsigned int first_glyph_idx = first_glyphs_indirection[i];
[ ]   146  
[W]   147      for (unsigned int ligature_idx = 0; ligature_idx < ARRAY_LENGTH (ligature_table[0].ligatures); ligature_idx++)
[W]   148      {
[W]   149        hb_codepoint_t ligature_u = ligature_table[first_glyph_idx].ligatures[ligature_idx].ligature;
[W]   150        hb_codepoint_t ligature_glyph;
[W]   151        if (!hb_font_get_glyph (font, ligature_u, 0, &ligature_glyph))
[W]   152  	continue;
[ ]   153  
[W]   154        const auto &components = ligature_table[first_glyph_idx].ligatures[ligature_idx].components;
[W]   155        unsigned component_count = ARRAY_LENGTH_CONST (components);
[ ]   156  
[W]   157        bool matched = true;
[W]   158        for (unsigned j = 0; j < component_count; j++)
[W]   159        {
[W]   160  	hb_codepoint_t component_u   = ligature_table[first_glyph_idx].ligatures[ligature_idx].components[j];
[W]   161  	hb_codepoint_t component_glyph;
[W]   162  	if (!component_u ||
[W]   163  	    !hb_font_get_nominal_glyph (font, component_u, &component_glyph))
[W]   164  	{
[W]   165  	  matched = false;
[W]   166  	  break;
[W]   167  	}
[ ]   168  
[W]   169  	component_list[num_components++] = component_glyph;
[W]   170        }
[W]   171        if (!matched)
[W]   172          continue;
[ ]   173  
[W]   174        component_count_list[num_ligatures] = 1 + component_count;
[W]   175        ligature_list[num_ligatures] = ligature_glyph;
[ ]   176  
[W]   177        ligature_per_first_glyph_count_list[i]++;
[ ]   178  
[W]   179        num_ligatures++;
[W]   180      }
[W]   181    }
[ ]   182  
[B]   183    if (!num_ligatures)
[B]   184      return nullptr;
[ ]   185  
[ ]   186  
[ ]   187    /* 16 bytes per ligature ought to be enough... */
[W]   188    char buf[ARRAY_LENGTH_CONST (ligature_list) * 16 + 128];
[W]   189    hb_serialize_context_t c (buf, sizeof (buf));
[W]   190    OT::SubstLookup *lookup = c.start_serialize<OT::SubstLookup> ();
[W]   191    bool ret = lookup->serialize_ligature (&c,
[W]   192  					 lookup_flags,
[W]   193  					 hb_sorted_array (first_glyphs, num_first_glyphs),
[W]   194  					 hb_array (ligature_per_first_glyph_count_list, num_first_glyphs),
[W]   195  					 hb_array (ligature_list, num_ligatures),
[W]   196  					 hb_array (component_count_list, num_ligatures),
[W]   197  					 hb_array (component_list, num_components));
[W]   198    c.end_serialize ();
[ ]   199  
[W]   200    return ret && !c.in_error () ? c.copy<OT::SubstLookup> () : nullptr;
[B]   201  }

--- No 1-hop callers of hb-ot-shaper-arabic.cc:OT::Layout::GSUB_impl::SubstLookup* arabic_fallback_synthesize_lookup_ligature<ligature_3_set_t [1]>(hb_ot_shape_plan_t const*, hb_font_t*, ligature_3_set_t const (&) [1], unsigned int) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       2        10  hb-ot-shaper-arabic.cc:arabic_fallback_plan_init_win1256(arabic_fallback_plan_t*, hb_ot_shape_plan_t const*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-arabic-fallback.hh:256-294)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-arabic.cc:OT::Layout::GSUB_impl::SubstLookup* arabic_fallback_synthesize_lookup_ligature<ligature_3_set_t [1]>(hb_ot_shape_plan_t const*, hb_font_t*, ligature_3_set_t const (&) [1], unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-arabic-fallback.hh:110-201) ---
  d=1   L 131  T=1 F=8  T=10 F=0  if (!hb_font_get_glyph (font, first_u, 0, &first_glyph))  <-- BLOCKER
  d=1   L 143  T=8 F=9  T=0 F=10  for (unsigned int i = 0; i < num_first_glyphs; i++)
  d=1   L 147  T=40 F=8  T=0 F=0  for (unsigned int ligature_idx = 0; ligature_idx < ARRAY_...
  d=1   L 151  T=10 F=30  T=0 F=0  if (!hb_font_get_glyph (font, ligature_u, 0, &ligature_gl...
  d=1   L 158  T=30 F=28  T=0 F=0  for (unsigned j = 0; j < component_count; j++)
  d=1   L 162  T=0 F=30  T=0 F=0  if (!component_u ||
  d=1   L 163  T=2 F=28  T=0 F=0  !hb_font_get_nominal_glyph (font, component_u, &component...
  d=1   L 171  T=2 F=28  T=0 F=0  if (!matched)
  d=1   L 183  T=3 F=6  T=10 F=0  if (!num_ligatures)
  d=1   L 200  T=6 F=0  T=0 F=0  return ret && !c.in_error () ? c.copy<OT::SubstLookup> ()...
  d=1   L 200  T=6 F=0  T=0 F=0  return ret && !c.in_error () ? c.copy<OT::SubstLookup> ()...

[off-chain: 17 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=9fc6580d81a8226f, size=501 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72635s, mutation_op=ByteNegMutator,CrossoverInsertMutator,WordInterestingMutator,WordAddMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 20 00 00 01 00 00 00 21 11 fb 20 47 53 55 4e 20    ......!.. GSUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 01 20    ...........!.. 
  0030: 01 00 0a 00 00 00 08 00 00 00 21 00 01 20 6b 65   ..........!.. ke
Seed 2 (id=89620742bf0f8c50, size=399 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72649s, mutation_op=TokenReplace,WordAddMutator,QwordAddMutator,QwordAddMutator,ByteRandMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 20 00 00 01 00 00 00 21 11 fb 20 47 53 55 4e 20    ......!.. GSUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 01 20    ...........!.. 
  0030: 01 00 0a 00 00 00 08 00 00 00 21 00 01 20 6b 65   ..........!.. ke
Seed 3 (id=b5116fa59c09afeb, size=371 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72664s, mutation_op=ByteIncMutator,BytesDeleteMutator,DwordInterestingMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 20 00 00 00 00 00 00 21 11 fb 20 47 53 55 4e 20    ......!.. GSUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 01 20    ...........!.. 
  0030: 01 00 0a 15 55 55 55 00 00 00 21 00 01 20 6b 65   ....UUU...!.. ke
Seed 4 (id=fb4413ea3a16747b, size=446 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72667s, mutation_op=QwordAddMutator,ByteInterestingMutator,BytesRandSetMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 20 01 00 01 00 00 00 21 11 fb 20 47 53 55 4e 20    ......!.. GSUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 01 20    ...........!.. 
  0030: 01 00 0a 00 00 00 08 00 00 00 21 00 fe 20 6b 65   ..........!.. ke
Seed 5 (id=266d08d2ce4d0b16, size=501 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72672s, mutation_op=BitFlipMutator,ByteRandMutator,BytesSwapMutator,DwordAddMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 20 00 00 01 00 00 00 21 11 fb 20 47 53 55 4e 20    ......!.. GSUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 01 20    ...........!.. 
  0030: 01 00 0a 00 00 00 08 00 00 00 21 00 01 20 6b 65   ..........!.. ke

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=000502d87c3cfa20, size=68 bytes, fuzzer=value_profile, trial=1, discovered_at=915s, mutation_op=BytesRandSetMutator):
  0000: f1 08 00 00 10 06 00 00 37 1c 00 00 f1 08 3b 3b   ........7.....;;
  0010: 3b 06 00 00 37 1c 00 00 4c 9f 9f 9f 4c 06 00 00   ;...7...L...L...
  0020: 37 0e 00 00 4c 9f 9f 9f 0e 17 00 36 0e 00 00 4c   7...L......6...L
  0030: 0e 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 91   ................
Seed 2 (id=001d239360d6d616, size=136 bytes, fuzzer=value_profile, trial=1, discovered_at=958s, mutation_op=BytesDeleteMutator):
  0000: 32 8a 8a 8a 8a 00 e5 01 20 e7 89 15 00 fb 20 20   2....... .....  
  0010: 20 20 20 20 20 20 20 20 20 20 20 20 20 7f 80 54                ..T
  0020: 54 6f 1b 6d 20 43 09 20 00 09 00 1b 6d 6d 6d 20   To.m C. ....mmm 
  0030: 2d 09 20 20 20 00 1b 6d 6d e3 e3 e3 e3 e3 20 20   -.   ..mm.....  
Seed 3 (id=007fc926cc3fda81, size=41 bytes, fuzzer=value_profile, trial=1, discovered_at=2290s, mutation_op=WordInterestingMutator,ByteNegMutator):
  0000: d6 08 00 00 4c 37 37 37 37 37 37 37 37 37 37 37   ....L77777777777
  0010: c9 0e 00 00 47 0e 00 00 37 0e 00 00 00 00 ff ff   ....G...7.......
  0020: 01 37 0d ff 10 ff ff f3 0e                        .7.......
Seed 4 (id=009ce74ea2538aab, size=45 bytes, fuzzer=value_profile, trial=1, discovered_at=2407s, mutation_op=BytesInsertMutator,BytesCopyMutator):
  0000: f5 08 00 00 ca 0e 00 00 f0 08 20 20 f5 08 00 00   ..........  ....
  0010: ca 0e 20 20 00 00 40 06 00 00 12 17 00 00 37 e0   ..  ..@.......7.
  0020: 62 9e 03 00 01 20 00 00 00 00 10 5b 1a            b.... .....[.
Seed 5 (id=00765468fb2ff0ae, size=49 bytes, fuzzer=value_profile, trial=1, discovered_at=5137s, mutation_op=ByteDecMutator,TokenInsert,ByteNegMutator,BytesSetMutator,ByteNegMutator,BytesSetMutator):
  0000: fa 08 00 00 68 61 8d 63 31 0e 00 00 c8 0e 00 00   ....ha.c1.......
  0010: 97 97 97 97 97 97 97 97 00 00 00 00 00 00 00 00   ................
  0020: 00 00 4c 4c 97 97 97 97 97 97 97 97 97 97 97 97   ..LL............
  0030: 97                                                .


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x9                             f1(.)x1 32(2)x1 d6(.)x1 f5(.)x1 +6u  PARTIAL
   0x0001  01(.)x9                             08(.)x4 8a(.)x1 f2(.)x1 70(p)x1 +3u  DIFFER
   0x0002  00(.)x9                             00(.)x6 8a(.)x1 e1(.)x1 c6(.)x1 +1u  PARTIAL
   0x0003  00(.)x9                             00(.)x5 8a(.)x1 40(@)x1 08(.)x1 +2u  PARTIAL
   0x0004  00(.)x9                             00(.)x2 10(.)x1 8a(.)x1 4c(L)x1 +5u  PARTIAL
   0x0005  07(.)x9                             00(.)x2 06(.)x1 37(7)x1 0e(.)x1 +5u  DIFFER
   0x0006  ff(.)x9                             00(.)x4 e5(.)x1 37(7)x1 8d(.)x1 +3u  DIFFER
   0x0007  80(.)x9                             00(.)x3 01(.)x1 37(7)x1 63(c)x1 +4u  DIFFER
   0x0008  20( )x9                             37(7)x2 00(.)x2 20( )x1 f0(.)x1 +4u  PARTIAL
   0x0009  3f(?)x9                             1c(.)x1 e7(.)x1 37(7)x1 08(.)x1 +6u  DIFFER
   0x000a  21(!)x9                             00(.)x5 89(.)x1 37(7)x1 20( )x1 +2u  DIFFER
   0x000b  20( )x9                             00(.)x4 15(.)x1 37(7)x1 20( )x1 +3u  PARTIAL
   0x000c  63(c)x9                             00(.)x2 f1(.)x1 37(7)x1 f5(.)x1 +5u  DIFFER
   0x000d  6d(m)x9                             08(.)x2 0e(.)x2 fb(.)x1 37(7)x1 +4u  DIFFER
   0x000e  61(a)x9                             00(.)x3 3b(;)x1 20( )x1 37(7)x1 +4u  DIFFER
   0x000f  70(p)x9                             00(.)x2 3b(;)x1 20( )x1 37(7)x1 +5u  DIFFER
   0x0010  20( )x9                             3b(;)x1 20( )x1 c9(.)x1 ca(.)x1 +6u  PARTIAL
   0x0011  00(.)x6 01(.)x3                     0e(.)x3 06(.)x1 20( )x1 97(.)x1 +4u  PARTIAL
   0x0012  00(.)x9                             00(.)x2 20( )x2 0e(.)x2 97(.)x1 +3u  PARTIAL
   0x0013  01(.)x7 00(.)x1 02(.)x1             00(.)x3 20( )x2 97(.)x1 e1(.)x1 +3u  PARTIAL
   0x0014  00(.)x9                             37(7)x1 20( )x1 47(G)x1 00(.)x1 +6u  PARTIAL
   0x0015  00(.)x9                             00(.)x3 0e(.)x2 1c(.)x1 20( )x1 +3u  PARTIAL
   0x0016  00(.)x9                             00(.)x2 20( )x2 40(@)x1 97(.)x1 +4u  PARTIAL
   0x0017  21(!)x9                             00(.)x3 20( )x1 06(.)x1 97(.)x1 +4u  DIFFER
   0x0018  11(.)x9                             00(.)x4 4c(L)x1 20( )x1 37(7)x1 +3u  DIFFER
   0x0019  fb(.)x9                             00(.)x3 9f(.)x1 20( )x1 0e(.)x1 +4u  DIFFER
   0x001a  20( )x9                             00(.)x3 ff(.)x2 9f(.)x1 20( )x1 +3u  PARTIAL
   0x001b  47(G)x9                             00(.)x4 9f(.)x1 20( )x1 17(.)x1 +3u  DIFFER
   0x001c  53(S)x9                             00(.)x5 20( )x2 4c(L)x1 e1(.)x1 +1u  DIFFER
   0x001d  55(U)x9                             00(.)x4 06(.)x1 7f(.)x1 4c(L)x1 +3u  DIFFER
   0x001e  4e(N)x9                             00(.)x3 80(.)x1 ff(.)x1 37(7)x1 +4u  DIFFER
   0x001f  20( )x9                             00(.)x3 ff(.)x2 54(T)x1 e0(.)x1 +3u  PARTIAL
   0x0020  20( )x8 00(.)x1                     00(.)x3 01(.)x2 37(7)x1 54(T)x1 +3u  PARTIAL
   0x0021  00(.)x9                             00(.)x4 0e(.)x1 6f(o)x1 37(7)x1 +3u  PARTIAL
   0x0022  00(.)x9                             00(.)x4 1b(.)x1 0d(.)x1 03(.)x1 +3u  PARTIAL
   0x0023  00(.)x9                             00(.)x4 6d(m)x1 ff(.)x1 4c(L)x1 +3u  PARTIAL
   0x0024  01(.)x9                             01(.)x2 00(.)x2 4c(L)x1 20( )x1 +4u  PARTIAL
   0x0025  00(.)x9                             00(.)x3 9f(.)x1 43(C)x1 ff(.)x1 +4u  PARTIAL
   0x0026  00(.)x9                             00(.)x3 9f(.)x1 09(.)x1 ff(.)x1 +4u  PARTIAL
   0x0027  00(.)x9                             00(.)x2 9f(.)x1 20( )x1 f3(.)x1 +5u  PARTIAL
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
  prompts_b/harfbuzz_5745.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5745,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5745 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5745 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5745 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).