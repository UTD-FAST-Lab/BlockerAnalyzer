==== BLOCKER ====
Target: harfbuzz
Branch ID: 5683
Location: /src/harfbuzz/src/hb-ot-shape-normalize.cc:195:9
Enclosing function: hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool)
Source line:     if (space_type != hb_unicode_funcs_t::NOT_SPACE &&
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  REFERENCE
cmplog                           4        6          0  REFERENCE
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             0       10          0  loser (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.70h  loser=23.90h
  avg hitcount on branch: winner=38  loser=0
  prob_div=1.00  dur_div=20.20h  hit_div=38
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5683/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool) (/src/harfbuzz/src/hb-ot-shape-normalize.cc:168-218) ---
[ ]   166  static inline void
[ ]   167  decompose_current_character (const hb_ot_shape_normalize_context_t *c, bool shortest)
[B]   168  {
[B]   169    hb_buffer_t * const buffer = c->buffer;
[B]   170    hb_codepoint_t u = buffer->cur().codepoint;
[B]   171    hb_codepoint_t glyph = 0;
[ ]   172  
[B]   173    if (shortest && c->font->get_nominal_glyph (u, &glyph, c->not_found))
[ ]   174    {
[ ]   175      next_char (buffer, glyph);
[ ]   176      return;
[ ]   177    }
[ ]   178  
[B]   179    if (decompose (c, shortest, u))
[ ]   180    {
[ ]   181      skip_char (buffer);
[ ]   182      return;
[ ]   183    }
[ ]   184  
[B]   185    if (!shortest && c->font->get_nominal_glyph (u, &glyph, c->not_found))
[ ]   186    {
[ ]   187      next_char (buffer, glyph);
[ ]   188      return;
[ ]   189    }
[ ]   190  
[B]   191    if (_hb_glyph_info_is_unicode_space (&buffer->cur()))
[B]   192    {
[B]   193      hb_codepoint_t space_glyph;
[B]   194      hb_unicode_funcs_t::space_t space_type = buffer->unicode->space_fallback_type (u);
[B]   195      if (space_type != hb_unicode_funcs_t::NOT_SPACE && <-- BLOCKER
[B]   196  	(c->font->get_nominal_glyph (0x0020, &space_glyph) || (space_glyph = buffer->invisible)))
[ ]   197      {
[ ]   198        _hb_glyph_info_set_unicode_space_fallback_type (&buffer->cur(), space_type);
[ ]   199        next_char (buffer, space_glyph);
[ ]   200        buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_SPACE_FALLBACK;
[ ]   201        return;
[ ]   202      }
[B]   203    }
[ ]   204  
[B]   205    if (u == 0x2011u)
[ ]   206    {
[ ]   207      /* U+2011 is the only sensible character that is a no-break version of another character
[ ]   208       * and not a space.  The space ones are handled already.  Handle this lone one. */
[ ]   209      hb_codepoint_t other_glyph;
[ ]   210      if (c->font->get_nominal_glyph (0x2010u, &other_glyph))
[ ]   211      {
[ ]   212        next_char (buffer, other_glyph);
[ ]   213        return;
[ ]   214      }
[ ]   215    }
[ ]   216  
[B]   217    next_char (buffer, glyph); /* glyph is initialized in earlier branches. */
[B]   218  }

--- Caller (1 hop): _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) (/src/harfbuzz/src/hb-ot-shape-normalize.cc:294-482, calls hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool) at line 361) (±10 around call site) ---
[B]   351        if (might_short_circuit)
[B]   352        {
[B]   353  	unsigned int done = font->get_nominal_glyphs (end - buffer->idx,
[B]   354  						      &buffer->cur().codepoint,
[B]   355  						      sizeof (buffer->info[0]),
[B]   356  						      &buffer->cur().glyph_index(),
[B]   357  						      sizeof (buffer->info[0]));
[B]   358  	if (unlikely (!buffer->next_glyphs (done))) break;
[B]   359        }
[B]   360        while (buffer->idx < end && buffer->successful)
[B]   361  	decompose_current_character (&c, might_short_circuit); <-- CALL
[ ]   362  
[B]   363        if (buffer->idx == count || !buffer->successful)
[B]   364  	break;
[ ]   365  
[B]   366        all_simple = false;
[ ]   367  
[ ]   368        /* Find all the marks now. */
[B]   369        for (end = buffer->idx + 1; end < count; end++)
[B]   370  	if (!_hb_glyph_info_is_unicode_mark(&buffer->info[end]))
[B]   371  	  break;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:294-482, calls hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool) at line 361)
hop 2  hb-ot-shape-normalize.cc:decompose_multi_char_cluster(hb_ot_shape_normalize_context_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:267-277, calls hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool) at line 276)
hop 3  hb-ot-shape.cc:hb_ot_substitute_default(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:882-900, calls _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 889)
hop 4  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934, calls hb-ot-shape.cc:hb_ot_substitute_default(hb_ot_shape_context_t const*) at line 924)
hop 5  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*) at line 1184)
hop 6  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:294-482) ---
  d=2   L 316  T=3 F=109  T=0 F=210  plan->shaper->decompose ? plan->shaper->decompose : decom...
  d=2   L 369  T=8 F=0  T=11 F=1  for (end = buffer->idx + 1; end < count; end++)
  d=2   L 376  T=4 F=0  T=5 F=1  while (buffer->idx < count && buffer->successful);
  d=2   L 388  T=62 F=1  T=48 F=0  if (_hb_glyph_info_get_modified_combining_class (&buffer-...
  d=2   L 392  T=1 F=0  T=0 F=0  for (end = i + 1; end < count; end++)
  d=2   L 393  T=1 F=0  T=0 F=0  if (_hb_glyph_info_get_modified_combining_class (&buffer-...
  d=2   L 397  T=0 F=1  T=0 F=0  if (end - i > HB_OT_SHAPE_MAX_COMBINING_MARKS) {
  d=2   L 404  T=0 F=1  T=0 F=0  if (plan->shaper->reorder_marks)
  d=2   L 431  T=3 F=0  T=1 F=0  mode == HB_OT_SHAPE_NORMALIZATION_MODE_COMPOSED_DIACRITIC...
  d=2   L 477  T=59 F=1  T=45 F=0  if (info_cc (buffer->prev()) == 0)
--- d=1  hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:168-218) ---
  d=1   L 185  T=0 F=98  T=0 F=42  if (!shortest && c->font->get_nominal_glyph (u, &glyph, c...
  d=1   L 195  T=1 F=16  T=12 F=0  if (space_type != hb_unicode_funcs_t::NOT_SPACE &&  <-- BLOCKER
  d=1   L 196  T=0 F=1  T=0 F=12  (c->font->get_nominal_glyph (0x0020, &space_glyph) || (sp...
  d=1   L 196  T=0 F=1  T=0 F=12  (c->font->get_nominal_glyph (0x0020, &space_glyph) || (sp...

[off-chain: 4 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=631d87a766522a94, size=64 bytes, fuzzer=value_profile, trial=1, discovered_at=4s, mutation_op=WordAddMutator,QwordAddMutator):
  0000: 00 01 00 00 00 01 20 21 20 20 17 17 6b 65 72 6e   ...... !  ..kern
  0010: 20 20 20 e0 00 08 00 00 00 ec ff ff ff 7f 00 00      .............
  0020: 80 16 00 00 20 01 00 00 00 20 01 00 00 00 01 00   .... .... ......
  0030: 69 00 00 02 20 20 20 01 5b 1a 20 20 20 00 20 20   i...   .[.   .  
Seed 2 (id=4c7a30e38912aa36, size=113 bytes, fuzzer=value_profile, trial=1, discovered_at=1056s, mutation_op=CrossoverInsertMutator,ByteInterestingMutator,TokenReplace):
  0000: 00 01 00 00 00 01 20 21 20 20 17 17 6b 65 72 6e   ...... !  ..kern
  0010: 20 20 20 e0 68 00 ff 00 85 17 00 00 31 00 00 00      .h.......1...
  0020: 56 10 00 00 56 10 00 00 31 00 00 ff 56 10 00 00   V...V...1...V...
  0030: 00 10 00 ff 4a 00 08 00 00 00 ec ff ff ff 7f 00   ....J...........
Seed 3 (id=865b975b93a43970, size=25 bytes, fuzzer=value_profile, trial=1, discovered_at=1251s, mutation_op=ByteAddMutator,DwordInterestingMutator,ByteAddMutator,BytesRandInsertMutator):
  0000: 00 0d 00 00 00 0d ff ff ff 7f f2 00 80 16 00 00   ................
  0010: 00 00 07 7f 5f ff ff ff 7f                        ...._....
Seed 4 (id=7ec5078006e672c2, size=80 bytes, fuzzer=value_profile, trial=1, discovered_at=3002s, mutation_op=ByteDecMutator,BitFlipMutator,WordInterestingMutator):
  0000: 00 01 00 00 00 01 20 21 1f 20 17 17 6b 65 72 6e   ...... !. ..kern
  0010: 20 20 20 e0 40 08 00 00 00 ec ff ff ff 7f 00 00      .@...........
  0020: 80 16 00 00 20 01 00 00 00 20 01 00 00 00 01 00   .... .... ......
  0030: 69 7f 00 02 20 20 20 01 5b 1a 20 20 20 00 20 20   i...   .[.   .  
Seed 5 (id=ad85c1f94e0f24f8, size=61 bytes, fuzzer=value_profile, trial=1, discovered_at=3814s, mutation_op=CrossoverReplaceMutator):
  0000: 92 17 00 00 00 64 00 00 df 14 00 00 df 1c 00 00   .....d..........
  0010: 1a 1f fd 1c 00 00 df 1c 00 00 10 00 80 16 00 00   ................
  0020: 80 16 00 00 00 df 1c 00 00 1a 20 20 20 20 20 20   ..........      
  0030: fd 1c 00 00 1a 20 ff ff ff a0 a0 a0 28            ..... ......(

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=044f6bc4804646ac, size=45 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=18s, mutation_op=QwordAddMutator,BytesSwapMutator,BytesCopyMutator,BytesDeleteMutator,BytesInsertMutator,TokenInsert):
  0000: 00 01 ff 73 6e 2d 00 00 18 18 00 00 1a 20 20 20   ...sn-.......   
  0010: 20 00 01 20 20 20 20 20 20 20 20 20 6b e8 20 20    ..         k.  
  0020: 20 00 20 20 20 00 01 20 20 20 2c 20 20             .   ..   ,  
Seed 2 (id=0456e276e0605002, size=45 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=198s, mutation_op=BytesDeleteMutator,ByteNegMutator,QwordAddMutator,ByteNegMutator,CrossoverReplaceMutator):
  0000: f3 f3 f3 f3 f3 20 20 20 00 18 00 00 00 0e 00 00   .....   ........
  0010: 01 0a 01 00 20 20 00 0f 20 20 01 00 01 0a 01 0d   ....  ..  ......
  0020: 20 20 00 00 00 fd 00 00 01 20 20 20 20              .......    
Seed 3 (id=00d38771b6ed0d47, size=85 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=756s, mutation_op=QwordAddMutator,BytesCopyMutator,WordInterestingMutator,BitFlipMutator,ByteInterestingMutator):
  0000: 5a 5a 5a 17 00 00 00 5a 5a 5a 5a 5a 5a ff 00 80   ZZZ....ZZZZZZ...
  0010: 00 04 0a 00 00 02 01 00 04 02 01 24 47 ba 64 00   ...........$G.d.
  0020: 00 01 bb dc dc dc c7 dc dc dc dc dc 23 00 0c 00   ............#...
  0030: 00 00 00 00 00 00 20 00 00 47 0c 00 00 00 00 00   ...... ..G......
Seed 4 (id=01f2c25ed4c11ada, size=160 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4256s, mutation_op=BytesDeleteMutator,ByteDecMutator,WordInterestingMutator):
  0000: 00 01 00 00 00 01 ee ff 00 30 00 20 47 50 4f 53   .........0. GPOS
  0010: 20 20 20 04 00 00 00 00 00 ff 00 00 00 01 00 0a      .............
  0020: 00 01 18 e0 02 00 ab 42 20 3c 20 00 00 00 fd ff   .......B < .....
  0030: 00 20 47 00 94 01 01 00 18 18 18 18 0f 18 00 00   . G.............
Seed 5 (id=01702bf68569b81e, size=326 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4392s, mutation_op=ByteAddMutator):
  0000: 00 01 00 00 00 02 ee ff 00 30 00 20 47 53 55 42   .........0. GSUB
  0010: 20 20 20 20 00 00 00 00 00 ff 00 00 00 00 00 0a       ............
  0020: 00 00 18 e0 00 18 18 18 18 18 20 00 00 00 fd ff   .......... .....
  0030: 00 10 00 00 94 01 00 00 1d 43 20 20 28 a0 00 00   .........C  (...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x4 68(h)x2 92(.)x1 e0(.)x1 +1u  00(.)x8 f3(.)x1 5a(Z)x1             PARTIAL
   0x0001  01(.)x3 17(.)x2 00(.)x2 0d(.)x1 +1u  01(.)x8 f3(.)x1 5a(Z)x1             PARTIAL
   0x0002  00(.)x6 ff(.)x2 93(.)x1             00(.)x7 ff(.)x1 f3(.)x1 5a(Z)x1     PARTIAL
   0x0003  00(.)x6 68(h)x2 93(.)x1             00(.)x7 73(s)x1 f3(.)x1 17(.)x1     PARTIAL
   0x0004  00(.)x6 2c(,)x2 93(.)x1             00(.)x8 6e(n)x1 f3(.)x1             PARTIAL
   0x0006  00(.)x4 20( )x3 ff(.)x1 93(.)x1     ee(.)x6 00(.)x2 20( )x2             PARTIAL
   0x0008  20( )x2 21(!)x2 ff(.)x1 1f(.)x1 +3u  00(.)x7 18(.)x1 5a(Z)x1 20( )x1     PARTIAL
   0x0009  20( )x6 7f(.)x1 14(.)x1 9d(.)x1     30(0)x6 18(.)x2 5a(Z)x1 20( )x1     PARTIAL
   0x000a  17(.)x3 20( )x2 f2(.)x1 00(.)x1 +2u  00(.)x8 5a(Z)x1 20( )x1             PARTIAL
   0x000b  17(.)x5 00(.)x3 9d(.)x1             20( )x7 00(.)x2 5a(Z)x1             PARTIAL
   0x000c  6b(k)x3 17(.)x2 80(.)x1 df(.)x1 +2u  47(G)x7 1a(.)x1 00(.)x1 5a(Z)x1     PARTIAL
   0x000e  00(.)x4 72(r)x3 1e(.)x1 9d(.)x1     4f(O)x6 00(.)x2 20( )x1 55(U)x1     PARTIAL
   0x0010  20( )x3 00(.)x3 1a(.)x1 1e(.)x1 +1u  20( )x7 01(.)x2 00(.)x1             PARTIAL
   0x0011  00(.)x4 20( )x3 1f(.)x1 9d(.)x1     20( )x6 00(.)x1 0a(.)x1 04(.)x1 +1u  PARTIAL
   0x0012  20( )x3 00(.)x3 07(.)x1 fd(.)x1 +1u  20( )x6 01(.)x2 0a(.)x1 1e(.)x1     PARTIAL
   0x0013  e0(.)x3 56(V)x2 7f(.)x1 1c(.)x1 +2u  20( )x7 00(.)x2 04(.)x1             PARTIAL
   0x0014  00(.)x3 10(.)x2 68(h)x1 5f(_)x1 +2u  00(.)x8 20( )x2                     PARTIAL
   0x0015  00(.)x5 08(.)x2 ff(.)x1 9d(.)x1     00(.)x7 20( )x2 02(.)x1             PARTIAL
   0x0016  00(.)x5 ff(.)x2 df(.)x1 9d(.)x1     00(.)x8 20( )x1 01(.)x1             PARTIAL
   0x0017  00(.)x4 ff(.)x2 1c(.)x1 56(V)x1 +1u  00(.)x7 20( )x1 0f(.)x1 18(.)x1     PARTIAL
   0x0019  00(.)x4 ec(.)x2 17(.)x1 20( )x1     ff(.)x6 20( )x2 02(.)x1 01(.)x1     PARTIAL
   0x001b  00(.)x4 ff(.)x2 fb(.)x1 17(.)x1     00(.)x8 20( )x1 24($)x1             PARTIAL
   0x001c  00(.)x3 ff(.)x2 31(1)x1 80(.)x1 +1u  00(.)x7 6b(k)x1 01(.)x1 47(G)x1     PARTIAL
   0x001d  00(.)x4 7f(.)x2 16(.)x1 fb(.)x1     00(.)x5 01(.)x2 e8(.)x1 0a(.)x1 +1u  PARTIAL
   0x001f  00(.)x6 70(p)x1 fb(.)x1             0a(.)x6 20( )x1 0d(.)x1 00(.)x1 +1u  PARTIAL
   0x0020  80(.)x3 00(.)x3 56(V)x1 2d(-)x1     00(.)x8 20( )x2                     PARTIAL
   0x0021  16(.)x3 10(.)x1 1e(.)x1 68(h)x1 +2u  00(.)x5 01(.)x3 20( )x1 30(0)x1     PARTIAL
   0x0022  00(.)x5 1e(.)x1 60(`)x1 56(V)x1     18(.)x5 00(.)x2 20( )x1 bb(.)x1 +1u  PARTIAL
   0x0023  00(.)x6 6e(n)x1 10(.)x1             e0(.)x5 20( )x2 00(.)x1 dc(.)x1 +1u  PARTIAL
   0x0027  00(.)x6 7f(.)x1 10(.)x1             42(B)x3 18(.)x3 00(.)x2 20( )x1 +1u  PARTIAL
   0x0028  00(.)x5 31(1)x1 20( )x1 1a(.)x1     20( )x4 18(.)x2 01(.)x1 dc(.)x1 +2u  PARTIAL
   0x002a  00(.)x3 01(.)x2 20( )x1 80(.)x1 +1u  20( )x7 2c(,)x1 dc(.)x1 ef(.)x1     PARTIAL
   0x002b  00(.)x3 ff(.)x1 20( )x1 16(.)x1 +2u  00(.)x5 20( )x3 dc(.)x1 ff(.)x1     PARTIAL
   0x002c  00(.)x3 56(V)x1 20( )x1 4c(L)x1 +2u  00(.)x7 20( )x2 23(#)x1             PARTIAL
   0x002d  00(.)x3 10(.)x1 20( )x1 0e(.)x1 +2u  00(.)x6 10(.)x1 80(.)x1             PARTIAL
   0x002e  01(.)x2 00(.)x2 20( )x2 1c(.)x1 +1u  fd(.)x5 0c(.)x1 01(.)x1 00(.)x1     PARTIAL
   0x002f  00(.)x4 20( )x1 01(.)x1 07(.)x1 +1u  ff(.)x4 00(.)x3 17(.)x1             PARTIAL
   0x0030  00(.)x4 69(i)x2 fd(.)x1 20( )x1     00(.)x8                             PARTIAL
   0x0032  00(.)x6 01(.)x1 20( )x1             00(.)x4 47(G)x1 04(.)x1 01(.)x1 +1u  PARTIAL
   0x0033  00(.)x3 02(.)x2 ff(.)x1 10(.)x1 +1u  00(.)x5 0c(.)x2 4b(K)x1             PARTIAL
   ... (12 more divergent offsets)
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
  prompts_b/harfbuzz_5683.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5683,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5683 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5683 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5683 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).