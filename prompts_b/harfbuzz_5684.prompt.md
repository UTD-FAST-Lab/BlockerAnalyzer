==== BLOCKER ====
Target: harfbuzz
Branch ID: 5684
Location: /src/harfbuzz/src/hb-ot-shape-normalize.cc:196:3
Enclosing function: hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool)
Source line: 	(c->font->get_nominal_glyph (0x0020, &space_glyph) || (space_glyph = buffer->invisible)))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (value_profile vs value_profile_cmplog)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile); winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.60h  loser=24.00h
  avg hitcount on branch: winner=9  loser=0
  prob_div=0.80  dur_div=13.40h  hit_div=9
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=10.60h  loser=21.60h
  avg hitcount on branch: winner=9  loser=0
  prob_div=0.70  dur_div=11.00h  hit_div=9
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5684/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool) (/src/harfbuzz/src/hb-ot-shape-normalize.cc:168-218) ---
[ ]   166  static inline void
[ ]   167  decompose_current_character (const hb_ot_shape_normalize_context_t *c, bool shortest)
[B]   168  {
[B]   169    hb_buffer_t * const buffer = c->buffer;
[B]   170    hb_codepoint_t u = buffer->cur().codepoint;
[B]   171    hb_codepoint_t glyph = 0;
[ ]   172  
[B]   173    if (shortest && c->font->get_nominal_glyph (u, &glyph, c->not_found))
[W]   174    {
[W]   175      next_char (buffer, glyph);
[W]   176      return;
[W]   177    }
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
[B]   195      if (space_type != hb_unicode_funcs_t::NOT_SPACE &&
[B]   196  	(c->font->get_nominal_glyph (0x0020, &space_glyph) || (space_glyph = buffer->invisible))) <-- BLOCKER
[W]   197      {
[W]   198        _hb_glyph_info_set_unicode_space_fallback_type (&buffer->cur(), space_type);
[W]   199        next_char (buffer, space_glyph);
[W]   200        buffer->scratch_flags |= HB_BUFFER_SCRATCH_FLAG_HAS_SPACE_FALLBACK;
[W]   201        return;
[W]   202      }
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
[L]   366        all_simple = false;
[ ]   367  
[ ]   368        /* Find all the marks now. */
[L]   369        for (end = buffer->idx + 1; end < count; end++)
[L]   370  	if (!_hb_glyph_info_is_unicode_mark(&buffer->info[end]))
[L]   371  	  break;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:294-482, calls hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool) at line 361)
hop 2  hb-ot-shape-normalize.cc:decompose_multi_char_cluster(hb_ot_shape_normalize_context_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:267-277, calls hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool) at line 276)
hop 3  hb-ot-shape.cc:hb_ot_substitute_default(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:882-900, calls _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 889)
hop 4  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934, calls hb-ot-shape.cc:hb_ot_substitute_default(hb_ot_shape_context_t const*) at line 924)
hop 5  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*) at line 1184)
hop 6  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      79      1060  hb-ot-shape-normalize.cc:decompose(hb_ot_shape_normalize_context_t const*, bool, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:126-164)
      94      1060  hb-ot-shape-normalize.cc:next_char(hb_buffer_t*, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:112-115)
      94      1060  hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:168-218)  <-- enclosing
      79       954  hb-ot-shape-normalize.cc:decompose_unicode(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:82-84)
      42       401  _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:294-482)
       0        10  hb-ot-shape-normalize.cc:decompose_multi_char_cluster(hb_ot_shape_normalize_context_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:267-277)
       0         4  hb-ot-shape-normalize.cc:compose_unicode(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:91-93)
       0         1  hb-ot-shape-normalize.cc:compare_combining_class(hb_glyph_info_t const*, hb_glyph_info_t const*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:282-287)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shape-normalize.cc:decompose_multi_char_cluster(hb_ot_shape_normalize_context_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:267-277) ---
  d=2   L 269  T=0 F=0  T=20 F=0  for (unsigned int i = buffer->idx; i < end && buffer->suc...
  d=2   L 269  T=0 F=0  T=20 F=10  for (unsigned int i = buffer->idx; i < end && buffer->suc...
  d=2   L 275  T=0 F=0  T=20 F=10  while (buffer->idx < end && buffer->successful)
  d=2   L 275  T=0 F=0  T=20 F=0  while (buffer->idx < end && buffer->successful)
--- d=2  _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:294-482) ---
  d=2   L 300  T=42 F=0  T=388 F=13  if (mode == HB_OT_SHAPE_NORMALIZATION_MODE_AUTO)
  d=2   L 302  T=0 F=42  T=0 F=388  if (plan->has_gpos_mark)
  d=2   L 316  T=0 F=42  T=7 F=394  plan->shaper->decompose ? plan->shaper->decompose : decom...
  d=2   L 317  T=0 F=42  T=11 F=390  plan->shaper->compose   ? plan->shaper->compose   : compo...
  d=2   L 321  T=0 F=42  T=0 F=401  bool might_short_circuit = always_short_circuit ||
  d=2   L 322  T=42 F=0  T=401 F=0  (mode != HB_OT_SHAPE_NORMALIZATION_MODE_DECOMPOSED &&
  d=2   L 323  T=42 F=0  T=388 F=13  mode != HB_OT_SHAPE_NORMALIZATION_MODE_COMPOSED_DIACRITIC...
  d=2   L 343  T=66 F=42  T=650 F=401  for (end = buffer->idx + 1; end < count; end++)
  d=2   L 344  T=0 F=66  T=10 F=640  if (_hb_glyph_info_is_unicode_mark (&buffer->info[end]))
  d=2   L 347  T=0 F=42  T=10 F=401  if (end < count)
  d=2   L 351  T=42 F=0  T=390 F=21  if (might_short_circuit)
  d=2   L 360  T=94 F=42  T=1040 F=411  while (buffer->idx < end && buffer->successful)
  d=2   L 360  T=94 F=0  T=1040 F=0  while (buffer->idx < end && buffer->successful)
  d=2   L 363  T=42 F=0  T=401 F=10  if (buffer->idx == count || !buffer->successful)
  d=2   L 363  T=0 F=0  T=0 F=10  if (buffer->idx == count || !buffer->successful)
  d=2   L 369  T=0 F=0  T=20 F=0  for (end = buffer->idx + 1; end < count; end++)
  d=2   L 370  T=0 F=0  T=10 F=10  if (!_hb_glyph_info_is_unicode_mark(&buffer->info[end]))
  d=2   L 376  T=0 F=0  T=10 F=0  while (buffer->idx < count && buffer->successful);
  d=2   L 376  T=0 F=0  T=10 F=0  while (buffer->idx < count && buffer->successful);
  d=2   L 383  T=0 F=42  T=6 F=395  if (!all_simple && buffer->message(font, "start reorder"))
  d=2   L 383  T=0 F=0  T=6 F=0  if (!all_simple && buffer->message(font, "start reorder"))
  d=2   L 386  T=0 F=0  T=93 F=6  for (unsigned int i = 0; i < count; i++)
  d=2   L 388  T=0 F=0  T=91 F=2  if (_hb_glyph_info_get_modified_combining_class (&buffer-...
  d=2   L 392  T=0 F=0  T=3 F=0  for (end = i + 1; end < count; end++)
  d=2   L 393  T=0 F=0  T=2 F=1  if (_hb_glyph_info_get_modified_combining_class (&buffer-...
  d=2   L 397  T=0 F=0  T=0 F=2  if (end - i > HB_OT_SHAPE_MAX_COMBINING_MARKS) {
  d=2   L 404  T=0 F=0  T=2 F=0  if (plan->shaper->reorder_marks)
  d=2   L 411  T=0 F=42  T=0 F=401  if (buffer->scratch_flags & HB_BUFFER_SCRATCH_FLAG_HAS_CGJ)
  d=2   L 428  T=0 F=42  T=6 F=395  if (!all_simple &&
  d=2   L 429  T=0 F=0  T=6 F=0  buffer->successful &&
  d=2   L 430  T=0 F=0  T=1 F=5  (mode == HB_OT_SHAPE_NORMALIZATION_MODE_COMPOSED_DIACRITI...
  d=2   L 431  T=0 F=0  T=5 F=0  mode == HB_OT_SHAPE_NORMALIZATION_MODE_COMPOSED_DIACRITIC...
  d=2   L 440  T=0 F=0  T=90 F=6  while (buffer->idx < count /* No need for: && buffer->suc...
  d=2   L 447  T=0 F=0  T=10 F=80  _hb_glyph_info_is_unicode_mark(&buffer->cur()))
  d=2   L 451  T=0 F=0  T=10 F=0  (starter == buffer->out_len - 1 ||
  d=2   L 454  T=0 F=0  T=0 F=10  c.compose (&c,
  d=2   L 477  T=0 F=0  T=88 F=2  if (info_cc (buffer->prev()) == 0)
--- d=1  hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:168-218) ---
  d=1   L 173  T=94 F=0  T=849 F=212  if (shortest && c->font->get_nominal_glyph (u, &glyph, c-...
  d=1   L 173  T=16 F=78  T=0 F=849  if (shortest && c->font->get_nominal_glyph (u, &glyph, c-...
  d=1   L 179  T=0 F=78  T=0 F=1060  if (decompose (c, shortest, u))
  d=1   L 185  T=0 F=0  T=0 F=212  if (!shortest && c->font->get_nominal_glyph (u, &glyph, c...
  d=1   L 185  T=0 F=78  T=212 F=849  if (!shortest && c->font->get_nominal_glyph (u, &glyph, c...
  d=1   L 191  T=5 F=73  T=27 F=1030  if (_hb_glyph_info_is_unicode_space (&buffer->cur()))
  d=1   L 195  T=5 F=0  T=27 F=0  if (space_type != hb_unicode_funcs_t::NOT_SPACE &&
  d=1   L 196  T=0 F=0  T=0 F=27  (c->font->get_nominal_glyph (0x0020, &space_glyph) || (sp...  <-- BLOCKER
  d=1   L 196  T=5 F=0  T=0 F=27  (c->font->get_nominal_glyph (0x0020, &space_glyph) || (sp...  <-- BLOCKER
  d=1   L 205  T=0 F=73  T=0 F=1060  if (u == 0x2011u)

[off-chain: 9 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c80ef2fb2e74fed4, size=485 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=50555s, mutation_op=DwordAddMutator,ByteRandMutator,WordInterestingMutator,BytesExpandMutator,WordAddMutator,TokenReplace):
  0000: 00 01 00 00 00 02 20 20 e0 3f 21 20 63 6d 61 70   ......  .?! cmap
  0010: 20 18 00 06 00 00 00 21 20 6b 20 47 53 55 43 20    ......! k GSUC 
  0020: 20 00 00 00 0c 00 00 00 00 00 00 00 18 56 56 56    ............VVV
  0030: 03 03 00 00 00 00 00 00 03 00 00 00 00 00 1c 25   ...............%
Seed 2 (id=ba976cfb96009e64, size=368 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=54954s, mutation_op=BytesExpandMutator):
  0000: 00 01 00 00 00 02 20 20 e0 3f 21 20 63 6d 61 70   ......  .?! cmap
  0010: 20 00 00 06 00 00 00 21 20 6b 20 47 53 55 42 20    ......! k GSUB 
  0020: 01 00 00 00 0e 00 00 00 06 00 00 00 01 00 1d 00   ................
  0030: 02 03 e8 00 04 03 03 20 02 18 00 00 2d 13 04 02   ....... ....-...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=050b9cb96487367d, size=17 bytes, fuzzer=cmplog, trial=1, discovered_at=0s, mutation_op=BytesCopyMutator,TokenReplace,ByteNegMutator):
  0000: 00 00 00 00 01 0d 01 00 20 20 20 20 6b 65 71 6e   ........    keqn
  0010: 20                                                 
Seed 2 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 3 (id=0509f37188b3277c, size=45 bytes, fuzzer=cmplog, trial=1, discovered_at=57s, mutation_op=DwordAddMutator,CrossoverReplaceMutator):
  0000: e2 17 00 00 01 e2 17 00 00 00 04 20 23 00 00 01   ........... #...
  0010: 20 2c 20 20 20 f6 e2 e2 e2 e2 e2 e2 e2 00 00 00    ,   ...........
  0020: 1e 0d 00 00 01 21 04 00 1a 20 e0 a0 20            .....!... .. 
Seed 4 (id=0170cbbd7538578d, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=151s, mutation_op=BytesSetMutator,DwordAddMutator,BytesDeleteMutator,BytesDeleteMutator,WordInterestingMutator,TokenInsert):
  0000: 00 20 97 97 00 00 20 20 00 00 00 00 0c 00 00 02   . ....  ........
  0010: 00 0d 01 00 20 97 97 01 00 3b 3b 3b 3b 3b 73 6e   .... ....;;;;;sn
  0020: 2d 00 3b 3b 3b 3b 3b 02 09 61 72 74 00 01 03 00   -.;;;;;..art....
  0030: 0c 0a 01 02 00 0d 01 00 20                        ........ 
Seed 5 (id=00982e3d94b5e098, size=79 bytes, fuzzer=value_profile, trial=1, discovered_at=168s, mutation_op=CrossoverInsertMutator,BytesExpandMutator):
  0000: 20 6e 74 00 6f 74 00 86 86 86 20 20 20 86 86 86    nt.ot....   ...
  0010: 00 86 86 20 00 00 00 1a 20 cd cc cc 0c 00 00 01   ... .... .......
  0020: 00 01 00 ff 19 00 55 55 15 01 00 55 15 01 00 55   ......UU...U...U
  0030: 55 01 00 ff 19 00 55 55 15 01 00 55 15 01 00 55   U.....UU...U...U


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x2                             00(.)x9 e2(.)x2 fe(.)x1 20( )x1 +7u  PARTIAL
   0x0001  01(.)x2                             01(.)x5 00(.)x3 17(.)x3 18(.)x2 +7u  PARTIAL
   0x0002  00(.)x2                             00(.)x15 ff(.)x1 97(.)x1 74(t)x1 +2u  PARTIAL
   0x0003  00(.)x2                             00(.)x16 ff(.)x1 97(.)x1 b7(.)x1 +1u  PARTIAL
   0x0004  00(.)x2                             00(.)x8 01(.)x4 f4(.)x2 6f(o)x1 +5u  PARTIAL
   0x0005  02(.)x2                             01(.)x6 00(.)x5 20( )x2 0d(.)x1 +6u  DIFFER
   0x0006  20( )x2                             00(.)x7 20( )x5 07(.)x2 01(.)x1 +5u  PARTIAL
   0x0007  20( )x2                             00(.)x8 20( )x6 e0(.)x1 86(.)x1 +4u  PARTIAL
   0x0008  e0(.)x2                             00(.)x6 21(!)x4 20( )x2 86(.)x1 +7u  DIFFER
   0x0009  3f(?)x2                             20( )x6 00(.)x6 86(.)x1 10(.)x1 +6u  DIFFER
   0x000a  21(!)x2                             00(.)x8 20( )x5 04(.)x2 1e(.)x2 +3u  DIFFER
   0x000b  20( )x2                             20( )x10 00(.)x8 01(.)x1 56(V)x1    PARTIAL
   0x000c  63(c)x2                             47(G)x5 23(#)x2 0c(.)x2 6b(k)x1 +10u  DIFFER
   0x000d  6d(m)x2                             00(.)x8 20( )x3 50(P)x3 53(S)x2 +4u  DIFFER
   0x000e  61(a)x2                             00(.)x9 4f(O)x3 55(U)x2 71(q)x1 +5u  PARTIAL
   0x000f  70(p)x2                             01(.)x3 00(.)x3 53(S)x3 42(B)x2 +9u  DIFFER
   0x0010  20( )x2                             00(.)x9 20( )x3 01(.)x2 79(y)x1 +5u  PARTIAL
   0x0011  18(.)x1 00(.)x1                     01(.)x5 20( )x3 2c(,)x2 00(.)x2 +7u  PARTIAL
   0x0012  00(.)x2                             00(.)x9 20( )x4 68(h)x1 01(.)x1 +4u  PARTIAL
   0x0013  06(.)x2                             00(.)x6 20( )x4 27(')x3 0d(.)x2 +4u  DIFFER
   0x0014  00(.)x2                             00(.)x11 20( )x3 6e(n)x1 a2(.)x1 +3u  PARTIAL
   0x0015  00(.)x2                             00(.)x9 f6(.)x2 74(t)x1 97(.)x1 +6u  PARTIAL
   0x0016  00(.)x2                             00(.)x12 e2(.)x2 2d(-)x1 97(.)x1 +3u  PARTIAL
   0x0017  21(!)x2                             10(.)x6 00(.)x5 e2(.)x2 68(h)x1 +5u  DIFFER
   0x0018  20( )x2                             00(.)x11 e2(.)x2 20( )x2 6b(k)x1 +3u  PARTIAL
   0x0019  6b(k)x2                             02(.)x5 00(.)x4 e2(.)x2 3b(;)x1 +7u  DIFFER
   0x001a  20( )x2                             00(.)x9 e2(.)x2 0a(.)x2 20( )x1 +4u  PARTIAL
   0x001b  47(G)x2                             00(.)x9 e2(.)x1 3b(;)x1 cc(.)x1 +6u  PARTIAL
   0x001c  53(S)x2                             00(.)x10 e2(.)x2 3b(;)x1 0c(.)x1 +4u  DIFFER
   0x001d  55(U)x2                             00(.)x10 a0(.)x2 3b(;)x1 1d(.)x1 +4u  DIFFER
   0x001e  43(C)x1 42(B)x1                     00(.)x8 01(.)x2 ff(.)x1 73(s)x1 +6u  DIFFER
   0x001f  20( )x2                             00(.)x6 01(.)x3 6e(n)x2 03(.)x2 +5u  PARTIAL
   0x0020  20( )x1 01(.)x1                     00(.)x8 2d(-)x2 30(0)x2 1e(.)x1 +5u  DIFFER
   0x0021  00(.)x2                             00(.)x7 07(.)x1 0d(.)x1 01(.)x1 +8u  PARTIAL
   0x0022  00(.)x2                             00(.)x12 3b(;)x1 30(0)x1 f6(.)x1 +3u  PARTIAL
   0x0023  00(.)x2                             00(.)x5 02(.)x2 3b(;)x1 ff(.)x1 +8u  PARTIAL
   0x0024  0c(.)x1 0e(.)x1                     00(.)x6 01(.)x3 3b(;)x1 19(.)x1 +6u  DIFFER
   0x0025  00(.)x2                             00(.)x4 20( )x2 02(.)x2 21(!)x1 +8u  PARTIAL
   0x0026  00(.)x2                             00(.)x7 20( )x1 04(.)x1 3b(;)x1 +7u  PARTIAL
   0x0027  00(.)x2                             00(.)x6 10(.)x3 20( )x2 02(.)x1 +5u  PARTIAL
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
  prompts_b/harfbuzz_5684.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5684,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5684 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5684 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5684 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).