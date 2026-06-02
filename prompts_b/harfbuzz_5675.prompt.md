==== BLOCKER ====
Target: harfbuzz
Branch ID: 5675
Location: /src/harfbuzz/src/hb-ot-shape-normalize.cc:132:13
Enclosing function: hb-ot-shape-normalize.cc:decompose(hb_ot_shape_normalize_context_t const*, bool, unsigned int)
Source line:       (b && !font->get_nominal_glyph (b, &b_glyph)))
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
  avg duration blocked: winner=13.10h  loser=24.00h
  avg hitcount on branch: winner=39  loser=0
  prob_div=0.80  dur_div=10.90h  hit_div=39
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5675/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shape-normalize.cc:decompose(hb_ot_shape_normalize_context_t const*, bool, unsigned int) (/src/harfbuzz/src/hb-ot-shape-normalize.cc:126-164) ---
[ ]   124  static inline unsigned int
[ ]   125  decompose (const hb_ot_shape_normalize_context_t *c, bool shortest, hb_codepoint_t ab)
[B]   126  {
[B]   127    hb_codepoint_t a = 0, b = 0, a_glyph = 0, b_glyph = 0;
[B]   128    hb_buffer_t * const buffer = c->buffer;
[B]   129    hb_font_t * const font = c->font;
[ ]   130  
[B]   131    if (!c->decompose (c, ab, &a, &b) ||
[B]   132        (b && !font->get_nominal_glyph (b, &b_glyph))) <-- BLOCKER
[B]   133      return 0;
[ ]   134  
[B]   135    bool has_a = (bool) font->get_nominal_glyph (a, &a_glyph);
[B]   136    if (shortest && has_a) {
[ ]   137      /* Output a and b */
[ ]   138      output_char (buffer, a, a_glyph);
[ ]   139      if (likely (b)) {
[ ]   140        output_char (buffer, b, b_glyph);
[ ]   141        return 2;
[ ]   142      }
[ ]   143      return 1;
[ ]   144    }
[ ]   145  
[B]   146    if (unsigned ret = decompose (c, shortest, a)) {
[W]   147      if (b) {
[W]   148        output_char (buffer, b, b_glyph);
[W]   149        return ret + 1;
[W]   150      }
[ ]   151      return ret;
[W]   152    }
[ ]   153  
[B]   154    if (has_a) {
[W]   155      output_char (buffer, a, a_glyph);
[W]   156      if (likely (b)) {
[W]   157        output_char (buffer, b, b_glyph);
[W]   158        return 2;
[W]   159      }
[ ]   160      return 1;
[W]   161    }
[ ]   162  
[B]   163    return 0;
[B]   164  }

--- Caller (1 hop): hb_unicode_funcs_t::decompose(unsigned int, unsigned int*, unsigned int*) (/src/harfbuzz/src/hb-unicode.hh:84-87, calls hb-ot-shape-normalize.cc:decompose(hb_ot_shape_normalize_context_t const*, bool, unsigned int) at line 86) (full body — short) ---
[B]    84    {
[B]    85      *a = ab; *b = 0;
[B]    86      return func.decompose (this, ab, a, b, user_data.decompose); <-- CALL
[B]    87    }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:168-218, calls hb-ot-shape-normalize.cc:decompose(hb_ot_shape_normalize_context_t const*, bool, unsigned int) at line 179)
hop 2  hb-ot-shape-normalize.cc:decompose_unicode(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:82-84, calls hb-ot-shape-normalize.cc:decompose(hb_ot_shape_normalize_context_t const*, bool, unsigned int) at line 83)
hop 3  _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:294-482, calls hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool) at line 361)
hop 3  hb-ot-shape-normalize.cc:decompose_multi_char_cluster(hb_ot_shape_normalize_context_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:267-277, calls hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool) at line 276)
hop 4  hb-ot-shape.cc:hb_ot_substitute_default(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:882-900, calls _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 889)
hop 5  hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:923-934, calls hb-ot-shape.cc:hb_ot_substitute_default(hb_ot_shape_context_t const*) at line 924)
hop 6  hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:1163-1195, calls hb-ot-shape.cc:hb_ot_substitute_pre(hb_ot_shape_context_t const*) at line 1184)
hop 7  _hb_ot_shape  (/src/harfbuzz/src/hb-ot-shape.cc:1204-1209, calls hb-ot-shape.cc:hb_ot_shape_internal(hb_ot_shape_context_t*) at line 1206)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     108       538  hb-ot-shape-normalize.cc:next_char(hb_buffer_t*, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:112-115)
     116       538  hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:168-218)
     118       539  hb-ot-shape-normalize.cc:decompose(hb_ot_shape_normalize_context_t const*, bool, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:126-164)  <-- enclosing
     118       539  hb_unicode_funcs_t::decompose(unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-unicode.hh:84-87)
      99       475  hb-ot-shape-normalize.cc:decompose_unicode(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:82-84)
       8        54  hb_unicode_funcs_t::is_variation_selector(unsigned int)  (/src/harfbuzz/src/hb-unicode.hh:120-126)
       0        32  hb-ot-shaper-khmer.cc:set_khmer_properties(hb_glyph_info_t&)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:85-90)
       0        32  hb-ot-shaper-khmer.cc:reorder_syllable_khmer(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:293-305)
       0        32  hb-ot-shaper-khmer.cc:decompose_khmer(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-khmer.cc:336-352)
      10        35  hb_unicode_funcs_t::modified_combining_class(unsigned int)  (/src/harfbuzz/src/hb-unicode.hh:107-116)
       7        26  hb_unicode_funcs_t::compose(unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-unicode.hh:76-80)
      18         0  hb-ot-shape-normalize.cc:output_char(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:103-108)
       4        21  hb-ot-shape-normalize.cc:decompose_multi_char_cluster(hb_ot_shape_normalize_context_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:267-277)
       2        18  hb-ot-shape-normalize.cc:compose_unicode(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:91-93)
       8         0  hb-ot-shape-normalize.cc:skip_char(hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:119-121)
... (15 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  hb-ot-shape-normalize.cc:decompose_multi_char_cluster(hb_ot_shape_normalize_context_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:267-277) ---
  d=3   L 269  T=8 F=0  T=53 F=0  for (unsigned int i = buffer->idx; i < end && buffer->suc...
  d=3   L 269  T=8 F=4  T=53 F=20  for (unsigned int i = buffer->idx; i < end && buffer->suc...
  d=3   L 275  T=8 F=4  T=52 F=20  while (buffer->idx < end && buffer->successful)
  d=3   L 275  T=8 F=0  T=52 F=0  while (buffer->idx < end && buffer->successful)
--- d=3  _hb_ot_shape_normalize(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:294-482) ---
  d=3   L 360  T=108 F=130  T=486 F=230  while (buffer->idx < end && buffer->successful)
  d=3   L 360  T=108 F=0  T=486 F=0  while (buffer->idx < end && buffer->successful)
  d=3   L 363  T=0 F=4  T=0 F=21  if (buffer->idx == count || !buffer->successful)
  d=3   L 369  T=8 F=0  T=53 F=1  for (end = buffer->idx + 1; end < count; end++)
  d=3   L 370  T=4 F=4  T=20 F=33  if (!_hb_glyph_info_is_unicode_mark(&buffer->info[end]))
  d=3   L 376  T=4 F=0  T=20 F=0  while (buffer->idx < count && buffer->successful);
  d=3   L 376  T=4 F=0  T=20 F=1  while (buffer->idx < count && buffer->successful);
  d=3   L 383  T=3 F=0  T=6 F=0  if (!all_simple && buffer->message(font, "start reorder"))
  d=3   L 392  T=5 F=0  T=15 F=0  for (end = i + 1; end < count; end++)
  d=3   L 393  T=5 F=0  T=12 F=3  if (_hb_glyph_info_get_modified_combining_class (&buffer-...
  d=3   L 397  T=0 F=5  T=0 F=12  if (end - i > HB_OT_SHAPE_MAX_COMBINING_MARKS) {
  d=3   L 404  T=0 F=5  T=9 F=3  if (plan->shaper->reorder_marks)
  d=3   L 429  T=3 F=0  T=6 F=0  buffer->successful &&
  d=3   L 430  T=2 F=1  T=5 F=1  (mode == HB_OT_SHAPE_NORMALIZATION_MODE_COMPOSED_DIACRITI...
  d=3   L 451  T=7 F=0  T=25 F=8  (starter == buffer->out_len - 1 ||
  d=3   L 452  T=0 F=0  T=2 F=6  info_cc (buffer->prev()) < info_cc (buffer->cur())) &&
  d=3   L 454  T=3 F=4  T=0 F=27  c.compose (&c,
  d=3   L 459  T=3 F=0  T=0 F=0  font->get_nominal_glyph (composed, &glyph))
--- d=2  hb-ot-shape-normalize.cc:decompose_current_character(hb_ot_shape_normalize_context_t const*, bool)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:168-218) ---
  d=2   L 173  T=64 F=52  T=429 F=109  if (shortest && c->font->get_nominal_glyph (u, &glyph, c-...
  d=2   L 173  T=9 F=55  T=0 F=429  if (shortest && c->font->get_nominal_glyph (u, &glyph, c-...
  d=2   L 179  T=8 F=99  T=0 F=538  if (decompose (c, shortest, u))
  d=2   L 185  T=42 F=2  T=0 F=109  if (!shortest && c->font->get_nominal_glyph (u, &glyph, c...
  d=2   L 185  T=44 F=55  T=109 F=429  if (!shortest && c->font->get_nominal_glyph (u, &glyph, c...
  d=2   L 191  T=0 F=57  T=4 F=534  if (_hb_glyph_info_is_unicode_space (&buffer->cur()))
  d=2   L 195  T=0 F=0  T=4 F=0  if (space_type != hb_unicode_funcs_t::NOT_SPACE &&
  d=2   L 196  T=0 F=0  T=0 F=4  (c->font->get_nominal_glyph (0x0020, &space_glyph) || (sp...
  d=2   L 196  T=0 F=0  T=0 F=4  (c->font->get_nominal_glyph (0x0020, &space_glyph) || (sp...
  d=2   L 205  T=0 F=57  T=0 F=538  if (u == 0x2011u)
--- d=1  hb-ot-shape-normalize.cc:decompose(hb_ot_shape_normalize_context_t const*, bool, unsigned int)  (/src/harfbuzz/src/hb-ot-shape-normalize.cc:126-164) ---
  d=1   L 131  T=107 F=11  T=527 F=12  if (!c->decompose (c, ab, &a, &b) ||
  d=1   L 132  T=11 F=0  T=11 F=1  (b && !font->get_nominal_glyph (b, &b_glyph)))  <-- BLOCKER
  d=1   L 132  T=0 F=11  T=11 F=0  (b && !font->get_nominal_glyph (b, &b_glyph)))  <-- BLOCKER
  d=1   L 136  T=1 F=10  T=0 F=1  if (shortest && has_a) {
  d=1   L 136  T=0 F=1  T=0 F=0  if (shortest && has_a) {
  d=1   L 146  T=2 F=9  T=0 F=1  if (unsigned ret = decompose (c, shortest, a)) {
  d=1   L 147  T=2 F=0  T=0 F=0  if (b) {
  d=1   L 154  T=8 F=1  T=0 F=1  if (has_a) {

[off-chain: 132 additional divergent branches across 24 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=ccf94a75d15faf4a, size=138 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72630s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,TokenInsert,ByteRandMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 20 00 ed 05 00 00 00 21 11 fb 20 47 53 55 4e 20    ......!.. GSUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 01 20    ...........!.. 
  0030: 01 00 0f 00 00 00 08 00 00 00 21 00 01 20 6b 65   ..........!.. ke
Seed 2 (id=ddcb3b0a21c8514d, size=413 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72630s, mutation_op=BytesRandInsertMutator,BitFlipMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 00 00 00 06 00 00 00 21 11 fb 20 47 53 aa 42 20   .......!.. GS.B 
  0020: 20 00 00 00 03 00 00 00 06 00 00 00 21 00 01 20    ...........!.. 
  0030: 01 00 0f 02 03 00 08 00 00 00 21 00 01 20 6b 65   ..........!.. ke
Seed 3 (id=565da61edb39fec8, size=426 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72659s, mutation_op=ByteIncMutator,ByteIncMutator,ByteDecMutator,BytesSetMutator,ByteFlipMutator,WordInterestingMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 20 00 00 01 00 00 00 21 11 fb 20 47 53 55 4e 00    ......!.. GSUN.
  0020: 7f 00 00 00 01 00 00 00 06 00 00 00 21 00 01 20   ............!.. 
  0030: 01 00 0f 00 00 00 08 00 00 00 21 00 01 20 6b 65   ..........!.. ke
Seed 4 (id=f955b6b966f597b4, size=132 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72659s, mutation_op=BytesDeleteMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 20 00 00 01 00 00 00 21 11 fb 20 47 53 55 4e 20    ......!.. GSUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 01 20    ...........!.. 
  0030: 01 00 0f 00 00 00 08 00 00 00 21 00 01 20 6b 65   ..........!.. ke
Seed 5 (id=9b1606f899f9a03a, size=426 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=72674s, mutation_op=ByteDecMutator,TokenReplace,BytesExpandMutator,ByteDecMutator):
  0000: 00 01 00 00 00 07 ff 80 20 3f 21 20 63 6d 61 70   ........ ?! cmap
  0010: 20 00 00 00 00 00 00 21 11 fb 20 47 53 55 4e 20    ......!.. GSUN 
  0020: 20 00 00 00 01 00 00 00 06 00 00 00 21 00 01 20    ...........!.. 
  0030: 01 00 0a 15 55 55 55 00 00 00 21 00 01 20 6b 65   ....UUU...!.. ke

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 2 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 3 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i
Seed 4 (id=0059bffc70552fa0, size=62 bytes, fuzzer=value_profile, trial=1, discovered_at=197s, mutation_op=DwordInterestingMutator,BytesRandInsertMutator,BytesInsertMutator):
  0000: 00 01 0e 00 df 20 00 00 00 00 aa 13 df 20 3d 3d   ..... ....... ==
  0010: 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 3d 00 ff   ==============..
  0020: df 20 00 00 00 00 00 20 20 20 20 20 20 20 20 20   . .....         
  0030: 2c 00 00 00 64 55 55 55 df 20 00 00 00 00         ,...dUUU. ....
Seed 5 (id=000502d87c3cfa20, size=68 bytes, fuzzer=value_profile, trial=1, discovered_at=915s, mutation_op=BytesRandSetMutator):
  0000: f1 08 00 00 10 06 00 00 37 1c 00 00 f1 08 3b 3b   ........7.....;;
  0010: 3b 06 00 00 37 1c 00 00 4c 9f 9f 9f 4c 06 00 00   ;...7...L...L...
  0020: 37 0e 00 00 4c 9f 9f 9f 0e 17 00 36 0e 00 00 4c   7...L......6...L
  0030: 0e 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 9f 91   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x6                             e0(.)x2 20( )x2 fe(.)x1 00(.)x1 +4u  PARTIAL
   0x0001  01(.)x6                             ff(.)x1 17(.)x1 e8(.)x1 01(.)x1 +6u  PARTIAL
   0x0002  00(.)x6                             00(.)x4 ff(.)x2 0e(.)x1 8a(.)x1 +2u  PARTIAL
   0x0003  00(.)x6                             00(.)x6 ff(.)x2 8a(.)x1 b7(.)x1     PARTIAL
   0x0004  00(.)x6                             df(.)x2 f4(.)x1 1a(.)x1 20( )x1 +5u  PARTIAL
   0x0005  07(.)x6                             00(.)x4 20( )x3 01(.)x1 06(.)x1 +1u  DIFFER
   0x0006  ff(.)x6                             00(.)x7 e0(.)x1 e5(.)x1 20( )x1     DIFFER
   0x0007  80(.)x6                             00(.)x6 e0(.)x1 55(U)x1 01(.)x1 +1u  DIFFER
   0x0008  20( )x6                             20( )x2 00(.)x2 29())x1 e0(.)x1 +4u  PARTIAL
   0x0009  3f(?)x6                             00(.)x3 2b(+)x1 17(.)x1 1c(.)x1 +4u  DIFFER
   0x000a  21(!)x6                             00(.)x4 29())x1 aa(.)x1 89(.)x1 +3u  DIFFER
   0x000b  20( )x6                             00(.)x6 29())x1 13(.)x1 15(.)x1 +1u  DIFFER
   0x000c  63(c)x6                             00(.)x2 01(.)x1 2c(,)x1 2b(+)x1 +5u  DIFFER
   0x000d  6d(m)x6                             20( )x4 00(.)x2 08(.)x1 fb(.)x1 +1u  DIFFER
   0x000e  61(a)x6                             00(.)x3 e0(.)x1 3d(=)x1 3b(;)x1 +3u  DIFFER
   0x000f  70(p)x6                             00(.)x2 6a(j)x1 fa(.)x1 3d(=)x1 +4u  DIFFER
   0x0010  20( )x4 00(.)x1 1d(.)x1             20( )x2 79(y)x1 3d(=)x1 3b(;)x1 +4u  PARTIAL
   0x0011  00(.)x5 1d(.)x1                     20( )x2 2d(-)x1 00(.)x1 3d(=)x1 +4u  PARTIAL
   0x0012  00(.)x5 ed(.)x1                     00(.)x4 68(h)x1 3d(=)x1 20( )x1 +2u  PARTIAL
   0x0013  01(.)x3 05(.)x1 06(.)x1 00(.)x1     00(.)x2 61(a)x1 55(U)x1 3d(=)x1 +4u  PARTIAL
   0x0014  00(.)x6                             6e(n)x1 e0(.)x1 3d(=)x1 37(7)x1 +5u  PARTIAL
   0x0015  00(.)x6                             20( )x2 74(t)x1 17(.)x1 3d(=)x1 +4u  DIFFER
   0x0016  00(.)x6                             00(.)x4 20( )x2 2d(-)x1 3d(=)x1 +1u  PARTIAL
   0x0017  21(!)x6                             00(.)x5 20( )x2 68(h)x1 3d(=)x1     DIFFER
   0x0018  11(.)x6                             20( )x3 6b(k)x1 61(a)x1 3d(=)x1 +3u  DIFFER
   0x0019  fb(.)x6                             20( )x2 00(.)x1 2e(.)x1 3d(=)x1 +4u  DIFFER
   0x001a  20( )x6                             20( )x2 00(.)x2 69(i)x1 3d(=)x1 +3u  PARTIAL
   0x001b  47(G)x5 83(.)x1                     00(.)x4 20( )x2 3d(=)x1 9f(.)x1     DIFFER
   0x001c  53(S)x6                             00(.)x2 3d(=)x1 4c(L)x1 20( )x1 +3u  DIFFER
   0x001d  55(U)x5 aa(.)x1                     00(.)x1 3d(=)x1 06(.)x1 7f(.)x1 +4u  DIFFER
   0x001e  4e(N)x5 42(B)x1                     00(.)x4 ff(.)x2 80(.)x1 13(.)x1     DIFFER
   0x001f  20( )x5 00(.)x1                     00(.)x3 01(.)x1 ff(.)x1 54(T)x1 +2u  PARTIAL
   0x0020  20( )x5 7f(.)x1                     00(.)x3 df(.)x1 37(7)x1 54(T)x1 +2u  DIFFER
   0x0021  00(.)x6                             0e(.)x2 00(.)x2 07(.)x1 20( )x1 +2u  PARTIAL
   0x0022  00(.)x6                             00(.)x6 1b(.)x1 0f(.)x1             PARTIAL
   0x0023  00(.)x6                             00(.)x5 6d(m)x1 2d(-)x1 fd(.)x1     PARTIAL
   0x0024  01(.)x5 03(.)x1                     00(.)x3 01(.)x1 4c(L)x1 20( )x1 +2u  PARTIAL
   0x0025  00(.)x6                             00(.)x3 20( )x1 9f(.)x1 43(C)x1 +2u  PARTIAL
   0x0026  00(.)x6                             00(.)x2 20( )x1 9f(.)x1 09(.)x1 +3u  PARTIAL
   0x0027  00(.)x6                             20( )x3 9f(.)x1 68(h)x1 61(a)x1 +2u  DIFFER
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
  prompts_b/harfbuzz_5675.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5675,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5675 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5675 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5675 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).