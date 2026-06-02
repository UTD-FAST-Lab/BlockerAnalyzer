==== BLOCKER ====
Target: harfbuzz
Branch ID: 5302
Location: /src/harfbuzz/src/hb-buffer-verify.cc:124:3
Enclosing function: hb-buffer-verify.cc:buffer_verify_unsafe_to_break(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)
Source line: 	 info[end-(forward?0:1)].mask & HB_GLYPH_FLAG_UNSAFE_TO_BREAK))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile); loser (calibrated_energy vs minimizer); loser (ctx_coverage vs naive_ctx)
cmplog                           4        6          0  REFERENCE
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog             8        2          0  REFERENCE
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     2        8          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        9        1          0  winner (calibrated_energy vs naive)
fast                             9        1          0  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['minimizer', 'naive', 'naive_ctx', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'fast', 'grimoire']

==== DECISIVE PAIRS (3) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 12  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.30h  loser=21.50h
  avg hitcount on branch: winner=1317  loser=268
  prob_div=0.70  dur_div=10.20h  hit_div=1049
  subject-level: delta_AUC=17795340.0  p_AUC=0.0002  delta_Final=285.0  p_final=0.0002
--- Pair 2: minimizer > naive  [delta: calibrated_energy] ---
  subject 18  (minimizer vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.00h  loser=21.50h
  avg hitcount on branch: winner=3221  loser=268
  prob_div=0.70  dur_div=15.50h  hit_div=2953
  subject-level: delta_AUC=13277160.0  p_AUC=0.001  delta_Final=189.1  p_final=0.001
--- Pair 3: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 15  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=12.20h  loser=21.50h
  avg hitcount on branch: winner=2615  loser=268
  prob_div=0.60  dur_div=9.30h  hit_div=2347
  subject-level: delta_AUC=15634800.0  p_AUC=0.0003  delta_Final=258.3  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5302/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-buffer-verify.cc:buffer_verify_unsafe_to_break(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*) (/src/harfbuzz/src/hb-buffer-verify.cc:94-203) ---
[ ]    92  			       unsigned int        num_features,
[ ]    93  			       const char * const *shapers)
[B]    94  {
[B]    95    if (buffer->cluster_level != HB_BUFFER_CLUSTER_LEVEL_MONOTONE_GRAPHEMES &&
[B]    96        buffer->cluster_level != HB_BUFFER_CLUSTER_LEVEL_MONOTONE_CHARACTERS)
[ ]    97    {
[ ]    98      /* Cannot perform this check without monotone clusters. */
[ ]    99      return true;
[ ]   100    }
[ ]   101  
[ ]   102    /* Check that breaking up shaping at safe-to-break is indeed safe. */
[ ]   103  
[B]   104    hb_buffer_t *fragment = hb_buffer_create_similar (buffer);
[B]   105    hb_buffer_set_flags (fragment, (hb_buffer_flags_t (hb_buffer_get_flags (fragment) & ~HB_BUFFER_FLAG_VERIFY)));
[B]   106    hb_buffer_t *reconstruction = hb_buffer_create_similar (buffer);
[B]   107    hb_buffer_set_flags (reconstruction, (hb_buffer_flags_t (hb_buffer_get_flags (reconstruction) & ~HB_BUFFER_FLAG_VERIFY)));
[ ]   108  
[B]   109    unsigned int num_glyphs;
[B]   110    hb_glyph_info_t *info = hb_buffer_get_glyph_infos (buffer, &num_glyphs);
[ ]   111  
[B]   112    unsigned int num_chars;
[B]   113    hb_glyph_info_t *text = hb_buffer_get_glyph_infos (text_buffer, &num_chars);
[ ]   114  
[ ]   115    /* Chop text and shape fragments. */
[B]   116    bool forward = HB_DIRECTION_IS_FORWARD (hb_buffer_get_direction (buffer));
[B]   117    unsigned int start = 0;
[B]   118    unsigned int text_start = forward ? 0 : num_chars;
[B]   119    unsigned int text_end = text_start;
[B]   120    for (unsigned int end = 1; end < num_glyphs + 1; end++)
[B]   121    {
[B]   122      if (end < num_glyphs &&
[B]   123  	(info[end].cluster == info[end-1].cluster ||
[B]   124  	 info[end-(forward?0:1)].mask & HB_GLYPH_FLAG_UNSAFE_TO_BREAK)) <-- BLOCKER
[W]   125  	continue;
[ ]   126  
[ ]   127      /* Shape segment corresponding to glyphs start..end. */
[B]   128      if (end == num_glyphs)
[B]   129      {
[B]   130        if (forward)
[B]   131  	text_end = num_chars;
[ ]   132        else
[ ]   133  	text_start = 0;
[B]   134      }
[L]   135      else
[L]   136      {
[L]   137        if (forward)
[L]   138        {
[L]   139  	unsigned int cluster = info[end].cluster;
[L]   140  	while (text_end < num_chars && text[text_end].cluster < cluster)
[L]   141  	  text_end++;
[L]   142        }
[ ]   143        else
[ ]   144        {
[ ]   145  	unsigned int cluster = info[end - 1].cluster;
[ ]   146  	while (text_start && text[text_start - 1].cluster >= cluster)
[ ]   147  	  text_start--;
[ ]   148        }
[L]   149      }
[B]   150      assert (text_start < text_end);
[ ]   151  
[B]   152      if (0)
[ ]   153        printf("start %u end %u text start %u end %u\n", start, end, text_start, text_end);
[ ]   154  
[B]   155      hb_buffer_clear_contents (fragment);
[ ]   156  
[B]   157      hb_buffer_flags_t flags = hb_buffer_get_flags (fragment);
[B]   158      if (0 < text_start)
[L]   159        flags = (hb_buffer_flags_t) (flags & ~HB_BUFFER_FLAG_BOT);
[B]   160      if (text_end < num_chars)
[L]   161        flags = (hb_buffer_flags_t) (flags & ~HB_BUFFER_FLAG_EOT);
[B]   162      hb_buffer_set_flags (fragment, flags);
[ ]   163  
[B]   164      hb_buffer_append (fragment, text_buffer, text_start, text_end);
[B]   165      if (!hb_shape_full (font, fragment, features, num_features, shapers))
[ ]   166      {
[ ]   167        buffer_verify_error (buffer, font, BUFFER_VERIFY_ERROR "shaping failed while shaping fragment.");
[ ]   168        hb_buffer_destroy (reconstruction);
[ ]   169        hb_buffer_destroy (fragment);
[ ]   170        return false;
[ ]   171      }
[B]   172      else if (!fragment->successful || fragment->shaping_failed)
[ ]   173      {
[ ]   174        hb_buffer_destroy (reconstruction);
[ ]   175        hb_buffer_destroy (fragment);
[ ]   176        return true;
[ ]   177      }
[B]   178      hb_buffer_append (reconstruction, fragment, 0, -1);
[ ]   179  
[B]   180      start = end;
[B]   181      if (forward)
[B]   182        text_start = text_end;
[ ]   183      else
[ ]   184        text_end = text_start;
[B]   185    }
[ ]   186  
[B]   187    bool ret = true;
[B]   188    hb_buffer_diff_flags_t diff = hb_buffer_diff (reconstruction, buffer, (hb_codepoint_t) -1, 0);
[B]   189    if (diff & ~HB_BUFFER_DIFF_FLAG_GLYPH_FLAGS_MISMATCH)
[ ]   190    {
[ ]   191      buffer_verify_error (buffer, font, BUFFER_VERIFY_ERROR "unsafe-to-break test failed.");
[ ]   192      ret = false;
[ ]   193  
[ ]   194      /* Return the reconstructed result instead so it can be inspected. */
[ ]   195      hb_buffer_set_length (buffer, 0);
[ ]   196      hb_buffer_append (buffer, reconstruction, 0, -1);
[ ]   197    }
[ ]   198  
[B]   199    hb_buffer_destroy (reconstruction);
[B]   200    hb_buffer_destroy (fragment);
[ ]   201  
[B]   202    return ret;
[B]   203  }

--- Caller (1 hop): hb_buffer_t::verify(hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*) (/src/harfbuzz/src/hb-buffer-verify.cc:409-436, calls hb-buffer-verify.cc:buffer_verify_unsafe_to_break(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*) at line 413) (full body — short) ---
[B]   409  {
[B]   410    bool ret = true;
[B]   411    if (!buffer_verify_monotone (this, font))
[ ]   412      ret = false;
[B]   413    if (!buffer_verify_unsafe_to_break (this, text_buffer, font, features, num_features, shapers)) <-- CALL
[ ]   414      ret = false;
[B]   415    if ((flags & HB_BUFFER_FLAG_PRODUCE_UNSAFE_TO_CONCAT) != 0 &&
[B]   416        !buffer_verify_unsafe_to_concat (this, text_buffer, font, features, num_features, shapers))
[ ]   417      ret = false;
[B]   418    if (!ret)
[ ]   419    {
[ ]   420  #ifndef HB_NO_BUFFER_SERIALIZE
[ ]   421      unsigned len = text_buffer->len;
[ ]   422      hb_vector_t<char> bytes;
[ ]   423      if (likely (bytes.resize (len * 10 + 16)))
[ ]   424      {
[ ]   425        hb_buffer_serialize_unicode (text_buffer,
[ ]   426  				   0, len,
[ ]   427  				   bytes.arrayZ, bytes.length,
[ ]   428  				   &len,
[ ]   429  				   HB_BUFFER_SERIALIZE_FORMAT_TEXT,
[ ]   430  				   HB_BUFFER_SERIALIZE_FLAG_NO_CLUSTERS);
[ ]   431        buffer_verify_error (this, font, BUFFER_VERIFY_ERROR "text was: %s.", bytes.arrayZ);
[ ]   432      }
[ ]   433  #endif
[ ]   434    }
[B]   435    return ret;
[B]   436  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb_buffer_t::verify(hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:409-436, calls hb-buffer-verify.cc:buffer_verify_unsafe_to_break(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*) at line 413)
hop 3  hb_shape_full  (/src/harfbuzz/src/hb-shape.cc:130-171, calls hb_buffer_t::verify(hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*) at line 159)
hop 4  hb-buffer-verify.cc:buffer_verify_unsafe_to_concat(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:212-401, calls hb_shape_full at line 319)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      30        10  hb-buffer-verify.cc:buffer_verify_monotone(hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-buffer-verify.cc:65-85)
      30        10  hb-buffer-verify.cc:buffer_verify_unsafe_to_break(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:94-203)  <-- enclosing
      30        10  hb_buffer_t::verify(hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:409-436)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb_buffer_t::verify(hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:409-436) ---
  d=2   L 411  T=0 F=30  T=0 F=10  if (!buffer_verify_monotone (this, font))
  d=2   L 413  T=0 F=30  T=0 F=10  if (!buffer_verify_unsafe_to_break (this, text_buffer, fo...
  d=2   L 415  T=0 F=30  T=0 F=10  if ((flags & HB_BUFFER_FLAG_PRODUCE_UNSAFE_TO_CONCAT) != ...
  d=2   L 418  T=0 F=30  T=0 F=10  if (!ret)
--- d=1  hb-buffer-verify.cc:buffer_verify_unsafe_to_break(hb_buffer_t*, hb_buffer_t*, hb_font_t*, hb_feature_t const*, unsigned int, char const* const*)  (/src/harfbuzz/src/hb-buffer-verify.cc:94-203) ---
  d=1   L  95  T=0 F=30  T=0 F=10  if (buffer->cluster_level != HB_BUFFER_CLUSTER_LEVEL_MONO...
  d=1   L 118  T=30 F=0  T=10 F=0  unsigned int text_start = forward ? 0 : num_chars;
  d=1   L 120  T=570 F=30  T=190 F=10  for (unsigned int end = 1; end < num_glyphs + 1; end++)
  d=1   L 122  T=540 F=30  T=180 F=10  if (end < num_glyphs &&
  d=1   L 123  T=0 F=540  T=0 F=180  (info[end].cluster == info[end-1].cluster ||
  d=1   L 124  T=540 F=0  T=0 F=180  info[end-(forward?0:1)].mask & HB_GLYPH_FLAG_UNSAFE_TO_BR...  <-- BLOCKER
  d=1   L 124  T=540 F=0  T=180 F=0  info[end-(forward?0:1)].mask & HB_GLYPH_FLAG_UNSAFE_TO_BR...  <-- BLOCKER
  d=1   L 128  T=30 F=0  T=10 F=180  if (end == num_glyphs)
  d=1   L 130  T=30 F=0  T=10 F=0  if (forward)
  d=1   L 137  T=0 F=0  T=180 F=0  if (forward)
  d=1   L 140  T=0 F=0  T=360 F=0  while (text_end < num_chars && text[text_end].cluster < c...
  d=1   L 140  T=0 F=0  T=180 F=180  while (text_end < num_chars && text[text_end].cluster < c...
  d=1   L 158  T=0 F=30  T=180 F=10  if (0 < text_start)
  d=1   L 160  T=0 F=30  T=180 F=10  if (text_end < num_chars)
  d=1   L 165  T=0 F=30  T=0 F=190  if (!hb_shape_full (font, fragment, features, num_feature...
  d=1   L 172  T=0 F=30  T=0 F=190  else if (!fragment->successful || fragment->shaping_failed)
  d=1   L 172  T=0 F=30  T=0 F=190  else if (!fragment->successful || fragment->shaping_failed)
  d=1   L 181  T=30 F=0  T=190 F=0  if (forward)
  d=1   L 189  T=0 F=30  T=0 F=10  if (diff & ~HB_BUFFER_DIFF_FLAG_GLYPH_FLAGS_MISMATCH)

[off-chain: 4 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=24143f6a396cff64, size=133 bytes, fuzzer=minimizer, trial=1, discovered_at=2310s, mutation_op=CrossoverInsertMutator):
  0000: 00 01 00 00 00 01 46 20 20 20 28 f6 6b 65 72 6e   ......F   (.kern
  0010: 00 00 00 01 00 00 00 10 00 01 00 09 09 00 00 09   ................
  0020: 20 00 00 00 00 00 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e    ...............
  0030: 0e 0e 2c 0e 0e 0e 0e 0e 0e 0e 0e 0e 00 00 09 09   ..,.............
Seed 2 (id=0130d32717d6abb0, size=141 bytes, fuzzer=minimizer, trial=1, discovered_at=2656s, mutation_op=BytesDeleteMutator,ByteInterestingMutator,BytesInsertCopyMutator,WordInterestingMutator):
  0000: 00 01 00 00 00 01 46 20 20 20 28 f6 6b 65 72 6e   ......F   (.kern
  0010: 00 00 00 01 00 00 00 10 00 01 00 0f 01 00 20 92   .............. .
  0020: 92 2c 00 00 00 00 ff 07 00 00 00 03 6e 6e 6e 6e   .,..........nnnn
  0030: 6e 6e 04 67 74 32 32 32 10 00 00 20 20 00 00 b0   nn.gt222...  ...
Seed 3 (id=1cd5037762e739d2, size=99 bytes, fuzzer=minimizer, trial=1, discovered_at=2656s, mutation_op=BytesInsertCopyMutator):
  0000: 00 01 00 00 00 01 46 20 20 20 28 f6 6b 65 72 6e   ......F   (.kern
  0010: 00 00 00 01 00 00 00 10 00 01 00 09 09 09 20 09   .............. .
  0020: 20 00 00 00 00 00 0e 2c 0e 0e 0e 0e 0e 0e 00 00    ......,........
  0030: 00 00 00 66 76 62 61 0e 0e 0e 00 00 09 09 0e 20   ...fvba........ 
Seed 4 (id=0354073023471a2a, size=152 bytes, fuzzer=minimizer, trial=1, discovered_at=2960s, mutation_op=DwordInterestingMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 01 46 20 20 20 28 f6 6b 65 72 6e   ......F   (.kern
  0010: 00 00 00 01 00 00 00 10 00 01 00 0f 01 00 20 92   .............. .
  0020: 92 2c 00 00 00 00 ff 07 00 00 00 03 6e 6e 6e 6e   .,..........nnnn
  0030: 6e ff 07 00 00 00 03 6e 6e 6e 6e 6e 6e 04 67 74   n......nnnnnn.gt
Seed 5 (id=1fcad0f16ec207ea, size=140 bytes, fuzzer=minimizer, trial=1, discovered_at=3241s, mutation_op=ByteIncMutator):
  0000: 00 01 00 00 00 01 4d 20 20 20 00 64 6b 65 72 6e   ......M   .dkern
  0010: 00 00 00 01 00 00 00 10 00 7f 00 03 00 00 00 00   ................
  0020: 00 00 00 00 00 00 ff 00 00 00 ef 00 18 00 00 00   ................
  0030: e8 00 00 e8 0d 00 00 7f 18 64 00 80 80 80 80 80   .........d......

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
Seed 4 (id=0002ee9aae2b9bef, size=54 bytes, fuzzer=naive, trial=1, discovered_at=470s, mutation_op=WordInterestingMutator,TokenInsert,BytesExpandMutator,ByteInterestingMutator):
  0000: 00 ff 00 00 1d 20 00 00 c8 0a 01 00 70 78 2d 68   ..... ......px-h
  0010: 61 6e 74 2d 68 6b 00 74 40 01 00 00 00 20 01 00   ant-hk.t@.... ..
  0020: c8 0a 01 00 40 62 91 6d 00 00 00 20 01 00 c8 7f   ....@b.m... ....
  0030: 01 00 40 62 91 6d                                 ..@b.m
Seed 5 (id=0030c881e05b69bb, size=56 bytes, fuzzer=naive, trial=1, discovered_at=4302s, mutation_op=BytesExpandMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesDeleteMutator,WordAddMutator,ByteIncMutator):
  0000: 6d 6d 6e 2d 68 61 6e 74 00 19 19 6d 01 00 9a 19   mmn-hant...m....
  0010: 00 73 6e 2d 68 61 6e 74 00 19 90 76 6c 67 70 90   .sn-hant...vlgp.
  0020: 6e 74 61 6c 90 00 a6 06 65 65 6d 00 3c 0b 00 00   ntal....eem.<...
  0030: 00 19 00 00 52 06 00 00                           ....R...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x30                            00(.)x3 05(.)x2 87(.)x1 6d(m)x1 +3u  PARTIAL
   0x0001  01(.)x30                            00(.)x2 07(.)x2 0e(.)x1 75(u)x1 +4u  DIFFER
   0x0002  00(.)x30                            00(.)x5 0d(.)x1 fe(.)x1 6e(n)x1 +2u  PARTIAL
   0x0003  00(.)x30                            00(.)x5 2d(-)x2 0e(.)x1 cb(.)x1 +1u  PARTIAL
   0x0004  00(.)x30                            00(.)x2 68(h)x2 70(p)x2 22(")x1 +3u  PARTIAL
   0x0005  01(.)x19 04(.)x9 02(.)x1 03(.)x1    0e(.)x1 00(.)x1 67(g)x1 20( )x1 +6u  PARTIAL
   0x000a  20( )x10 28(()x9 01(.)x9 00(.)x2    00(.)x4 75(u)x1 01(.)x1 19(.)x1 +2u  PARTIAL
   0x000c  6b(k)x30                            20( )x1 80(.)x1 70(p)x1 01(.)x1 +5u  DIFFER
   0x000d  65(e)x30                            00(.)x3 17(.)x1 78(x)x1 3f(?)x1 +3u  DIFFER
   0x000e  72(r)x30                            00(.)x2 64(d)x1 2d(-)x1 9a(.)x1 +4u  DIFFER
   0x000f  6e(n)x30                            00(.)x2 6f(o)x1 68(h)x1 19(.)x1 +4u  DIFFER
   0x0010  00(.)x10 dd(.)x10 22(")x6 20( )x4   00(.)x3 2d(-)x1 61(a)x1 0a(.)x1 +3u  PARTIAL
   0x0011  00(.)x10 df(.)x10 20( )x9 fd(.)x1   20( )x2 68(h)x1 6e(n)x1 73(s)x1 +4u  PARTIAL
   0x0014  00(.)x30                            68(h)x3 74(t)x1 23(#)x1 18(.)x1 +3u  PARTIAL
   0x0015  00(.)x30                            00(.)x3 91(.)x1 6b(k)x1 61(a)x1 +3u  PARTIAL
   0x0016  00(.)x30                            00(.)x4 0e(.)x1 01(.)x1 6e(n)x1 +2u  PARTIAL
   0x0017  10(.)x10 1a(.)x10 35(5)x10          00(.)x2 74(t)x2 9f(.)x1 ff(.)x1 +3u  DIFFER
   0x0018  00(.)x16 35(5)x10 02(.)x4           20( )x2 00(.)x2 9f(.)x1 40(@)x1 +3u  PARTIAL
   0x001a  00(.)x22 56(V)x4 35(5)x3 34(4)x1    00(.)x3 0c(.)x1 9f(.)x1 90(.)x1 +3u  PARTIAL
   0x0024  00(.)x23 56(V)x6 61(a)x1            02(.)x1 40(@)x1 90(.)x1 0c(.)x1 +2u  PARTIAL
   0x002a  00(.)x19 7f(.)x4 0e(.)x2 01(.)x2 +3u  00(.)x3 6d(m)x1 5b([)x1 57(W)x1     PARTIAL
   0x0033  00(.)x15 66(f)x8 10(.)x2 0e(.)x1 +4u  ff(.)x2 00(.)x2 62(b)x1 b6(.)x1     PARTIAL
   0x0036  01(.)x9 00(.)x6 b5(.)x4 f0(.)x3 +7u  00(.)x2 ff(.)x1 57(W)x1 01(.)x1     PARTIAL
   0x0037  00(.)x7 04(.)x7 b4(.)x3 f0(.)x3 +8u  00(.)x3 ff(.)x1 57(W)x1             PARTIAL
   0x0038  69(i)x7 00(.)x4 01(.)x3 0e(.)x2 +11u  00(.)x1 ff(.)x1 57(W)x1 88(.)x1     PARTIAL
   0x0039  00(.)x10 b4(.)x3 09(.)x3 0e(.)x2 +10u  00(.)x1 ff(.)x1 05(.)x1 1f(.)x1     PARTIAL
   0x003a  00(.)x17 b4(.)x3 fd(.)x2 f0(.)x2 +6u  10(.)x1 cb(.)x1 00(.)x1 01(.)x1     PARTIAL
   0x003b  00(.)x15 b4(.)x4 01(.)x2 f0(.)x2 +7u  00(.)x2 0c(.)x1                     PARTIAL
   0x003c  01(.)x7 00(.)x4 4c(L)x4 14(.)x3 +9u  00(.)x1 0c(.)x1 bb(.)x1             PARTIAL
   0x003d  00(.)x13 b4(.)x4 02(.)x3 03(.)x2 +7u  a7(.)x1 00(.)x1 14(.)x1             PARTIAL
   0x003e  00(.)x15 b4(.)x4 7f(.)x3 f0(.)x2 +6u  00(.)x2 01(.)x1                     PARTIAL
   0x003f  00(.)x13 b4(.)x4 03(.)x2 f0(.)x2 +9u  00(.)x1 ff(.)x1                     PARTIAL
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- minimizer ---
**Instrumentation**: naive's edge counters only.

**Feedback**: naive's edge-bucket `MaxMapFeedback`, plus a
`CalibrationStage` that measures each new corpus entry's execution
time, edge-map fill, and stability into `SchedulerMetadata`/testcase
metadata.

**Mutators / stages**: havoc + token mutator (`LineageMutator`, names
captured) run inside a `StdPowerMutationalStage` rather than naive's
plain `StdMutationalStage`. Stages are `[calibration, power]`. The
power stage derives the number of havoc mutations per seed visit (the
"energy") from a calibration-based `perf_score` — faster, smaller,
more-stable seeds earn more mutations. PowerSchedule is `None`, so the
energy uses ONLY intrinsic calibration and is NOT weighted by how often
a region has been hit. Corpus selection is plain FIFO `QueueScheduler`
(same order as naive).

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge, plus a one-time
calibration burst per new corpus entry.

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

--- naive_ctx ---
**Instrumentation**: naive's SanitizerCoverage edge counters, but the
executor installs a `CtxHook` (`HookableInProcessExecutor`). The hook
keeps a running hash of the current call context (caller chain) and
folds it into the edge-map index, so the same basic-block edge is
recorded at different map slots depending on the call path that
reached it.

**Feedback**: the same `MaxMapFeedback` edge-bucket signal as naive,
computed over the context-indexed map — a "new bucket" is a new
(call-context, edge) pair rather than a bare edge.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`, no
CMP_MAP. Stages are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no ParentInfo-only / dash rows.

**Per-execution cost**: one edge-counter increment per executed edge
plus a context-hash update per call/return.

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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5302.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5302,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile), minimizer>naive (calibrated_energy), naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5302 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5302 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5302 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).