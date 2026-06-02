==== BLOCKER ====
Target: harfbuzz
Branch ID: 5992
Location: /src/harfbuzz/src/hb-ot-shaper-use.cc:394:7
Enclosing function: hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)
Source line:   if (info[start].use_category() == USE(R) && end - start > 1)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            9        1          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive); loser (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                    10        0          0  REFERENCE
mopt                             9        1          0  REFERENCE
minimizer                       10        0          0  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=7.50h  loser=23.60h
  avg hitcount on branch: winner=11  loser=0
  prob_div=0.90  dur_div=16.10h  hit_div=11
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=5.60h  loser=23.60h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.90  dur_div=18.00h  hit_div=2
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5992/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442) ---
[ ]   361  static void
[ ]   362  reorder_syllable_use (hb_buffer_t *buffer, unsigned int start, unsigned int end)
[B]   363  {
[B]   364    use_syllable_type_t syllable_type = (use_syllable_type_t) (buffer->info[start].syllable() & 0x0F);
[ ]   365    /* Only a few syllable types need reordering. */
[B]   366    if (unlikely (!(FLAG_UNSAFE (syllable_type) &
[B]   367  		  (FLAG (use_virama_terminated_cluster) |
[B]   368  		   FLAG (use_sakot_terminated_cluster) |
[B]   369  		   FLAG (use_standard_cluster) |
[B]   370  		   FLAG (use_symbol_cluster) |
[B]   371  		   FLAG (use_broken_cluster) |
[B]   372  		   0))))
[ ]   373      return;
[ ]   374  
[B]   375    hb_glyph_info_t *info = buffer->info;
[ ]   376  
[B]   377  #define POST_BASE_FLAGS64 (FLAG64 (USE(FAbv)) | \
[W]   378  			   FLAG64 (USE(FBlw)) | \
[W]   379  			   FLAG64 (USE(FPst)) | \
[W]   380  			   FLAG64 (USE(MAbv)) | \
[W]   381  			   FLAG64 (USE(MBlw)) | \
[W]   382  			   FLAG64 (USE(MPst)) | \
[W]   383  			   FLAG64 (USE(MPre)) | \
[W]   384  			   FLAG64 (USE(VAbv)) | \
[W]   385  			   FLAG64 (USE(VBlw)) | \
[W]   386  			   FLAG64 (USE(VPst)) | \
[W]   387  			   FLAG64 (USE(VPre)) | \
[W]   388  			   FLAG64 (USE(VMAbv)) | \
[W]   389  			   FLAG64 (USE(VMBlw)) | \
[W]   390  			   FLAG64 (USE(VMPst)) | \
[W]   391  			   FLAG64 (USE(VMPre)))
[ ]   392  
[ ]   393    /* Move things forward. */
[B]   394    if (info[start].use_category() == USE(R) && end - start > 1) <-- BLOCKER
[W]   395    {
[ ]   396      /* Got a repha.  Reorder it towards the end, but before the first post-base
[ ]   397       * glyph. */
[W]   398      for (unsigned int i = start + 1; i < end; i++)
[W]   399      {
[W]   400        bool is_post_base_glyph = (FLAG64_UNSAFE (info[i].use_category()) & POST_BASE_FLAGS64) ||
[W]   401  				is_halant_use (info[i]);
[W]   402        if (is_post_base_glyph || i == end - 1)
[W]   403        {
[ ]   404  	/* If we hit a post-base glyph, move before it; otherwise move to the
[ ]   405  	 * end. Shift things in between backward. */
[ ]   406  
[W]   407  	if (is_post_base_glyph)
[W]   408  	  i--;
[ ]   409  
[W]   410  	buffer->merge_clusters (start, i + 1);
[W]   411  	hb_glyph_info_t t = info[start];
[W]   412  	memmove (&info[start], &info[start + 1], (i - start) * sizeof (info[0]));
[W]   413  	info[i] = t;
[ ]   414  
[W]   415  	break;
[W]   416        }
[W]   417      }
[W]   418    }
[ ]   419  
[ ]   420    /* Move things back. */
[B]   421    unsigned int j = start;
[B]   422    for (unsigned int i = start; i < end; i++)
[B]   423    {
[B]   424      uint32_t flag = FLAG_UNSAFE (info[i].use_category());
[B]   425      if (is_halant_use (info[i]))
[ ]   426      {
[ ]   427        /* If we hit a halant, move after it; otherwise move to the beginning, and
[ ]   428         * shift things in between forward. */
[ ]   429        j = i + 1;
[ ]   430      }
[B]   431      else if (((flag) & (FLAG (USE(VPre)) | FLAG (USE(VMPre)))) &&
[ ]   432  	     /* Only move the first component of a MultipleSubst. */
[B]   433  	     0 == _hb_glyph_info_get_lig_comp (&info[i]) &&
[B]   434  	     j < i)
[ ]   435      {
[ ]   436        buffer->merge_clusters (j, i + 1);
[ ]   437        hb_glyph_info_t t = info[i];
[ ]   438        memmove (&info[j + 1], &info[j], (i - j) * sizeof (info[0]));
[ ]   439        info[j] = t;
[ ]   440      }
[B]   441    }
[B]   442  }

--- Caller (1 hop): hb-ot-shaper-use.cc:reorder_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-use.cc:448-467, calls hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) at line 459) (full body — short) ---
[B]   448  {
[B]   449    bool ret = false;
[B]   450    if (buffer->message (font, "start reordering USE"))
[B]   451    {
[B]   452      if (hb_syllabic_insert_dotted_circles (font, buffer,
[B]   453  					   use_broken_cluster,
[B]   454  					   USE(B),
[B]   455  					   USE(R)))
[ ]   456        ret = true;
[ ]   457  
[B]   458      foreach_syllable (buffer, start, end)
[B]   459        reorder_syllable_use (buffer, start, end); <-- CALL
[ ]   460  
[B]   461      (void) buffer->message (font, "end reordering USE");
[B]   462    }
[ ]   463  
[B]   464    HB_BUFFER_DEALLOCATE_VAR (buffer, use_category);
[ ]   465  
[B]   466    return ret;
[B]   467  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-use.cc:reorder_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:448-467, calls hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) at line 459)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       1        10  hb-ot-shaper-use.cc:compose_use(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:483-489)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442) ---
  d=1   L 394  T=5 F=2  T=0 F=0  if (info[start].use_category() == USE(R) && end - start > 1)  <-- BLOCKER
  d=1   L 394  T=7 F=67  T=0 F=135  if (info[start].use_category() == USE(R) && end - start > 1)  <-- BLOCKER
  d=1   L 398  T=6 F=0  T=0 F=0  for (unsigned int i = start + 1; i < end; i++)
  d=1   L 400  T=1 F=5  T=0 F=0  bool is_post_base_glyph = (FLAG64_UNSAFE (info[i].use_cat...
  d=1   L 401  T=0 F=5  T=0 F=0  is_halant_use (info[i]);
  d=1   L 402  T=4 F=1  T=0 F=0  if (is_post_base_glyph || i == end - 1)
  d=1   L 402  T=1 F=5  T=0 F=0  if (is_post_base_glyph || i == end - 1)
  d=1   L 407  T=1 F=4  T=0 F=0  if (is_post_base_glyph)

[off-chain: 7 additional divergent branches across 4 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=a4f16069d0368e4c, size=47 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=627s, mutation_op=BytesDeleteMutator,DwordInterestingMutator):
  0000: 00 01 01 01 00 00 01 92 92 99 92 92 92 0c fe 12   ................
  0010: 13 10 01 00 02 1f 01 00 00 18 00 00 00 00 00 00   ................
  0020: 00 05 72 6e 01 06 00 00 06 06 00 18 20 20 20      ..rn........   
Seed 2 (id=36b6befbb09de4d1, size=33 bytes, fuzzer=naive, trial=1, discovered_at=14007s, mutation_op=ByteAddMutator,BytesDeleteMutator,BitFlipMutator,BytesCopyMutator,ByteDecMutator,WordAddMutator,ByteIncMutator):
  0000: 64 a8 00 05 02 1f 01 00 63 a8 00 00 02 1f 01 00   d.......c.......
  0010: 4f a8 00 00 00 ff 23 32 32 32 ce b2 32 a8 00 05   O.....#222..2...
  0020: 32                                                2
Seed 3 (id=bbb55fe722c5d154, size=57 bytes, fuzzer=naive, trial=1, discovered_at=17558s, mutation_op=BytesExpandMutator,WordAddMutator,QwordAddMutator):
  0000: 64 a8 00 00 01 1b 0d 00 64 a8 00 00 02 1f 01 00   d.......d.......
  0010: 01 1b 01 00 64 a8 00 00 02 1f 01 00 4f a1 00 00   ....d.......O...
  0020: 00 ff 32 32 32 32 ce 32 32 32 ee 32 32 fe 00 00   ..2222.222.22...
  0030: 00 01 00 00 01 16 01 01 01                        .........
Seed 4 (id=a78f366679e05ffd, size=28 bytes, fuzzer=naive, trial=1, discovered_at=17713s, mutation_op=QwordAddMutator,BytesRandInsertMutator,BitFlipMutator,DwordInterestingMutator,BytesDeleteMutator,ByteDecMutator):
  0000: 64 a8 00 05 02 1f 01 00 67 a8 00 00 01 1f 01 00   d.......g.......
  0010: 4f a8 00 00 00 ff 23 32 32 32 ce b2               O.....#222..
Seed 5 (id=f98da6d9823a5f97, size=34 bytes, fuzzer=naive, trial=1, discovered_at=21332s, mutation_op=BytesSetMutator,ByteInterestingMutator,ByteIncMutator):
  0000: 64 a8 00 00 01 1b 01 00 64 a8 00 00 02 1f 01 00   d.......d.......
  0010: 65 a8 00 00 01 1b 01 00 64 a8 00 00 02 1f 01 01   e.......d.......
  0020: 01 01                                             ..

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0170cbbd7538578d, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=151s, mutation_op=BytesSetMutator,DwordAddMutator,BytesDeleteMutator,BytesDeleteMutator,WordInterestingMutator,TokenInsert):
  0000: 00 20 97 97 00 00 20 20 00 00 00 00 0c 00 00 02   . ....  ........
  0010: 00 0d 01 00 20 97 97 01 00 3b 3b 3b 3b 3b 73 6e   .... ....;;;;;sn
  0020: 2d 00 3b 3b 3b 3b 3b 02 09 61 72 74 00 01 03 00   -.;;;;;..art....
  0030: 0c 0a 01 02 00 0d 01 00 20                        ........ 
Seed 2 (id=02e04c9299b6e4e1, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=172s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,ByteAddMutator,TokenReplace):
  0000: 00 95 6b 95 20 24 01 03 00 01 00 40 00 03 00 00   ..k. $.....@....
  0010: e0 20 00 00 00 18 00 00 20 b8 48 b8 b8 b8 b8 b8   . ...... .H.....
  0020: b8 b8 b8 06 02 00 80 20 b8                        ....... .
Seed 3 (id=034b3a94b7d5b64d, size=62 bytes, fuzzer=cmplog, trial=1, discovered_at=199s, mutation_op=QwordAddMutator):
  0000: 74 72 75 65 00 00 04 02 65 7f 64 6f 2d 0c 04 02   true....e.do-...
  0010: 02 00 ec 03 03 01 00 02 00 ec ed 1f 20 70 78 2d   ............ px-
  0020: 0e 7c 65 72 20 18 00 00 00 00 0d 06 00 02 02 ff   .|er ...........
  0030: ec 0c 0c 0c 0c 0c 0c 0c 0c 0c ec 22 22 22         ..........."""
Seed 4 (id=02b51d5c1a8c70da, size=53 bytes, fuzzer=cmplog, trial=1, discovered_at=413s, mutation_op=ByteRandMutator,TokenReplace,ByteNegMutator,ByteAddMutator):
  0000: 00 ff 01 00 00 01 00 1a 00 01 00 70 77 63 66 63   ...........pwcfc
  0010: 10 0d 01 00 21 0d 01 00 fd 06 00 00 60 10 00 00   ....!.......`...
  0020: 06 18 00 00 20 10 00 00 52 06 10 00 00 06 20 00   .... ...R..... .
  0030: 00 06 20 00 00                                    .. ..
Seed 5 (id=0335bf1465b48090, size=28 bytes, fuzzer=cmplog, trial=1, discovered_at=859s, mutation_op=BytesSwapMutator,BytesRandInsertMutator):
  0000: 86 18 00 00 00 a6 a6 10 20 10 7f ff ff ff 01 00   ........ .......
  0010: 6e 70 1c c5 17 01 00 16 17 00 80 ff               np..........


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  64(d)x4 00(.)x1                     00(.)x7 74(t)x1 86(.)x1 4f(O)x1     PARTIAL
   0x0001  a8(.)x4 01(.)x1                     01(.)x4 20( )x1 95(.)x1 72(r)x1 +3u  PARTIAL
   0x0002  00(.)x4 01(.)x1                     00(.)x5 97(.)x1 6b(k)x1 75(u)x1 +2u  PARTIAL
   0x0003  05(.)x2 00(.)x2 01(.)x1             00(.)x6 97(.)x1 95(.)x1 65(e)x1 +1u  PARTIAL
   0x0004  02(.)x2 01(.)x2 00(.)x1             00(.)x9 20( )x1                     PARTIAL
   0x0005  1f(.)x2 1b(.)x2 00(.)x1             01(.)x5 00(.)x2 24($)x1 a6(.)x1 +1u  PARTIAL
   0x0006  01(.)x4 0d(.)x1                     20( )x3 07(.)x2 01(.)x1 04(.)x1 +3u  PARTIAL
   0x0007  00(.)x4 92(.)x1                     20( )x5 03(.)x1 02(.)x1 1a(.)x1 +2u  PARTIAL
   0x0008  64(d)x2 92(.)x1 63(c)x1 67(g)x1     00(.)x3 20( )x3 21(!)x3 65(e)x1     DIFFER
   0x0009  a8(.)x4 99(.)x1                     20( )x4 01(.)x2 00(.)x1 7f(.)x1 +2u  DIFFER
   0x000a  00(.)x4 92(.)x1                     00(.)x4 64(d)x1 7f(.)x1 20( )x1 +3u  PARTIAL
   0x000b  00(.)x4 92(.)x1                     20( )x4 00(.)x1 40(@)x1 6f(o)x1 +3u  PARTIAL
   0x000c  02(.)x3 92(.)x1 01(.)x1             47(G)x3 0c(.)x1 00(.)x1 2d(-)x1 +4u  DIFFER
   0x000d  1f(.)x4 0c(.)x1                     00(.)x2 50(P)x2 03(.)x1 0c(.)x1 +4u  PARTIAL
   0x000e  01(.)x4 fe(.)x1                     00(.)x2 4f(O)x2 04(.)x1 66(f)x1 +4u  PARTIAL
   0x000f  00(.)x4 12(.)x1                     02(.)x2 00(.)x2 53(S)x2 63(c)x1 +3u  PARTIAL
   0x0010  4f(O)x2 13(.)x1 01(.)x1 65(e)x1     00(.)x6 e0(.)x1 02(.)x1 10(.)x1 +1u  DIFFER
   0x0011  a8(.)x3 10(.)x1 1b(.)x1             01(.)x4 0d(.)x2 20( )x1 00(.)x1 +2u  DIFFER
   0x0012  00(.)x3 01(.)x2                     00(.)x5 01(.)x2 ec(.)x1 1c(.)x1 +1u  PARTIAL
   0x0013  00(.)x5                             00(.)x4 03(.)x1 c5(.)x1 0d(.)x1 +3u  PARTIAL
   0x0014  00(.)x2 02(.)x1 64(d)x1 01(.)x1     00(.)x5 20( )x1 03(.)x1 21(!)x1 +2u  PARTIAL
   0x0015  ff(.)x2 1f(.)x1 a8(.)x1 1b(.)x1     00(.)x5 01(.)x2 97(.)x1 18(.)x1 +1u  DIFFER
   0x0016  01(.)x2 23(#)x2 00(.)x1             00(.)x7 97(.)x1 01(.)x1 02(.)x1     PARTIAL
   0x0017  00(.)x3 32(2)x2                     10(.)x4 00(.)x2 02(.)x2 01(.)x1 +1u  PARTIAL
   0x0018  32(2)x2 00(.)x1 02(.)x1 64(d)x1     00(.)x7 20( )x1 fd(.)x1 17(.)x1     PARTIAL
   0x0019  32(2)x2 18(.)x1 1f(.)x1 a8(.)x1     02(.)x3 00(.)x2 3b(;)x1 b8(.)x1 +3u  DIFFER
   0x001a  00(.)x2 ce(.)x2 01(.)x1             00(.)x6 3b(;)x1 48(H)x1 ed(.)x1 +1u  PARTIAL
   0x001b  00(.)x3 b2(.)x2                     47(G)x3 3b(;)x1 b8(.)x1 1f(.)x1 +4u  PARTIAL
   0x001c  00(.)x1 32(2)x1 4f(O)x1 02(.)x1     00(.)x3 3b(;)x1 b8(.)x1 20( )x1 +3u  PARTIAL
   0x001d  00(.)x1 a8(.)x1 a1(.)x1 1f(.)x1     01(.)x2 00(.)x2 3b(;)x1 b8(.)x1 +3u  PARTIAL
   0x001e  00(.)x3 01(.)x1                     00(.)x3 73(s)x1 b8(.)x1 78(x)x1 +3u  PARTIAL
   0x001f  00(.)x2 05(.)x1 01(.)x1             00(.)x2 03(.)x2 6e(n)x1 b8(.)x1 +3u  PARTIAL
   0x0020  00(.)x2 32(2)x1 01(.)x1             00(.)x3 2d(-)x1 b8(.)x1 0e(.)x1 +3u  PARTIAL
   0x0021  05(.)x1 ff(.)x1 01(.)x1             00(.)x5 b8(.)x1 7c(|)x1 18(.)x1 +1u  PARTIAL
   0x0022  72(r)x1 32(2)x1                     00(.)x5 3b(;)x1 b8(.)x1 65(e)x1 +1u  DIFFER
   0x0023  6e(n)x1 32(2)x1                     02(.)x3 06(.)x2 3b(;)x1 72(r)x1 +2u  DIFFER
   0x0024  01(.)x1 32(2)x1                     4f(O)x3 20( )x2 00(.)x2 3b(;)x1 +1u  DIFFER
   0x0025  06(.)x1 32(2)x1                     00(.)x5 3b(;)x1 18(.)x1 10(.)x1 +1u  DIFFER
   0x0026  00(.)x1 ce(.)x1                     00(.)x7 3b(;)x1 80(.)x1             PARTIAL
   0x0027  00(.)x1 32(2)x1                     10(.)x3 02(.)x2 20( )x2 00(.)x2     PARTIAL
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
  prompts_b/harfbuzz_5992.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5992,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5992 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5992 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5992 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).