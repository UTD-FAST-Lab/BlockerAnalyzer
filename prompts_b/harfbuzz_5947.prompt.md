==== BLOCKER ====
Target: harfbuzz
Branch ID: 5947
Location: /src/harfbuzz/src/hb-ot-shaper-myanmar.cc:280:9
Enclosing function: hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int)
Source line:     if (info[i].myanmar_position() == POS_PRE_M)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive); loser (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             9        1          0  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=2.80h  loser=19.10h
  avg hitcount on branch: winner=157  loser=1
  prob_div=0.80  dur_div=16.30h  hit_div=156
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=9.40h  loser=19.10h
  avg hitcount on branch: winner=6  loser=1
  prob_div=0.70  dur_div=9.70h  hit_div=5
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5947/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:181-301) ---
[ ]   179  initial_reordering_consonant_syllable (hb_buffer_t *buffer,
[ ]   180  				       unsigned int start, unsigned int end)
[B]   181  {
[B]   182    hb_glyph_info_t *info = buffer->info;
[ ]   183  
[B]   184    unsigned int base = end;
[B]   185    bool has_reph = false;
[ ]   186  
[B]   187    {
[B]   188      unsigned int limit = start;
[B]   189      if (start + 3 <= end &&
[B]   190  	info[start  ].myanmar_category() == M_Cat(Ra) &&
[B]   191  	info[start+1].myanmar_category() == M_Cat(As) &&
[B]   192  	info[start+2].myanmar_category() == M_Cat(H))
[ ]   193      {
[ ]   194        limit += 3;
[ ]   195        base = start;
[ ]   196        has_reph = true;
[ ]   197      }
[ ]   198  
[B]   199      {
[B]   200        if (!has_reph)
[B]   201  	base = limit;
[ ]   202  
[B]   203        for (unsigned int i = limit; i < end; i++)
[B]   204  	if (is_consonant_myanmar (info[i]))
[B]   205  	{
[B]   206  	  base = i;
[B]   207  	  break;
[B]   208  	}
[B]   209      }
[B]   210    }
[ ]   211  
[ ]   212    /* Reorder! */
[B]   213    {
[B]   214      unsigned int i = start;
[B]   215      for (; i < start + (has_reph ? 3 : 0); i++)
[ ]   216        info[i].myanmar_position() = POS_AFTER_MAIN;
[B]   217      for (; i < base; i++)
[W]   218        info[i].myanmar_position() = POS_PRE_C;
[B]   219      if (i < end)
[B]   220      {
[B]   221        info[i].myanmar_position() = POS_BASE_C;
[B]   222        i++;
[B]   223      }
[B]   224      myanmar_position_t pos = POS_AFTER_MAIN;
[ ]   225      /* The following loop may be ugly, but it implements all of
[ ]   226       * Myanmar reordering! */
[B]   227      for (; i < end; i++)
[B]   228      {
[B]   229        if (info[i].myanmar_category() == M_Cat(MR)) /* Pre-base reordering */
[ ]   230        {
[ ]   231  	info[i].myanmar_position() = POS_PRE_C;
[ ]   232  	continue;
[ ]   233        }
[B]   234        if (info[i].myanmar_category() == M_Cat(VPre)) /* Left matra */
[W]   235        {
[W]   236  	info[i].myanmar_position() = POS_PRE_M;
[W]   237  	continue;
[W]   238        }
[B]   239        if (info[i].myanmar_category() == M_Cat(VS))
[W]   240        {
[W]   241  	info[i].myanmar_position() = info[i - 1].myanmar_position();
[W]   242  	continue;
[W]   243        }
[ ]   244  
[B]   245        if (pos == POS_AFTER_MAIN && info[i].myanmar_category() == M_Cat(VBlw))
[ ]   246        {
[ ]   247  	pos = POS_BELOW_C;
[ ]   248  	info[i].myanmar_position() = pos;
[ ]   249  	continue;
[ ]   250        }
[ ]   251  
[B]   252        if (pos == POS_BELOW_C && info[i].myanmar_category() == M_Cat(A))
[ ]   253        {
[ ]   254  	info[i].myanmar_position() = POS_BEFORE_SUB;
[ ]   255  	continue;
[ ]   256        }
[B]   257        if (pos == POS_BELOW_C && info[i].myanmar_category() == M_Cat(VBlw))
[ ]   258        {
[ ]   259  	info[i].myanmar_position() = pos;
[ ]   260  	continue;
[ ]   261        }
[B]   262        if (pos == POS_BELOW_C && info[i].myanmar_category() != M_Cat(A))
[ ]   263        {
[ ]   264  	pos = POS_AFTER_SUB;
[ ]   265  	info[i].myanmar_position() = pos;
[ ]   266  	continue;
[ ]   267        }
[B]   268        info[i].myanmar_position() = pos;
[B]   269      }
[B]   270    }
[ ]   271  
[ ]   272    /* Sit tight, rock 'n roll! */
[B]   273    buffer->sort (start, end, compare_myanmar_order);
[ ]   274  
[ ]   275    /* Flip left-matra sequence. */
[B]   276    unsigned first_left_matra = end;
[B]   277    unsigned last_left_matra = end;
[B]   278    for (unsigned int i = start; i < end; i++)
[B]   279    {
[B]   280      if (info[i].myanmar_position() == POS_PRE_M) <-- BLOCKER
[W]   281      {
[W]   282        if (first_left_matra == end)
[W]   283  	first_left_matra = i;
[W]   284        last_left_matra = i;
[W]   285      }
[B]   286    }
[ ]   287    /* https://github.com/harfbuzz/harfbuzz/issues/3863 */
[B]   288    if (first_left_matra < last_left_matra)
[W]   289    {
[ ]   290      /* No need to merge clusters, done already? */
[W]   291      buffer->reverse_range (first_left_matra, last_left_matra + 1);
[ ]   292      /* Reverse back VS, etc. */
[W]   293      unsigned i = first_left_matra;
[W]   294      for (unsigned j = i; j <= last_left_matra; j++)
[W]   295        if (info[j].myanmar_category() == M_Cat(VPre))
[W]   296        {
[W]   297  	buffer->reverse_range (i, j + 1);
[W]   298  	i = j + 1;
[W]   299        }
[W]   300    }
[B]   301  }

--- Caller (1 hop): hb-ot-shaper-myanmar.cc:reorder_syllable_myanmar(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:308-320, calls hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int) at line 314) (full body — short) ---
[B]   308  {
[B]   309    myanmar_syllable_type_t syllable_type = (myanmar_syllable_type_t) (buffer->info[start].syllable() & 0x0F);
[B]   310    switch (syllable_type) {
[ ]   311  
[B]   312      case myanmar_broken_cluster: /* We already inserted dotted-circles, so just call the consonant_syllable. */
[B]   313      case myanmar_consonant_syllable:
[B]   314        initial_reordering_consonant_syllable  (buffer, start, end); <-- CALL
[B]   315        break;
[ ]   316  
[B]   317      case myanmar_non_myanmar_cluster:
[B]   318        break;
[B]   319    }
[B]   320  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:946-961, calls hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int) at line 960)
hop 2  hb-ot-shaper-myanmar.cc:reorder_syllable_myanmar(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:308-320, calls hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int) at line 314)
hop 3  hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986, calls hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 979)
hop 3  hb-ot-shaper-myanmar.cc:reorder_myanmar(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:326-344, calls hb-ot-shaper-myanmar.cc:reorder_syllable_myanmar(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 336)
hop 4  hb-ot-shaper-indic.cc:initial_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:992-1011, calls hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 1006)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      85         3  hb-ot-shaper-myanmar.cc:compare_myanmar_order(hb_glyph_info_t const*, hb_glyph_info_t const*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:167-172)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:181-301) ---
  d=1   L 189  T=13 F=21  T=1 F=16  if (start + 3 <= end &&
  d=1   L 190  T=0 F=13  T=0 F=1  info[start  ].myanmar_category() == M_Cat(Ra) &&
  d=1   L 200  T=34 F=0  T=17 F=0  if (!has_reph)
  d=1   L 203  T=54 F=14  T=20 F=4  for (unsigned int i = limit; i < end; i++)
  d=1   L 204  T=20 F=34  T=13 F=7  if (is_consonant_myanmar (info[i]))
  d=1   L 215  T=0 F=34  T=0 F=17  for (; i < start + (has_reph ? 3 : 0); i++)
  d=1   L 215  T=0 F=34  T=0 F=17  for (; i < start + (has_reph ? 3 : 0); i++)
  d=1   L 217  T=1 F=34  T=0 F=17  for (; i < base; i++)
  d=1   L 219  T=34 F=0  T=17 F=0  if (i < end)
  d=1   L 227  T=53 F=34  T=3 F=17  for (; i < end; i++)
  d=1   L 229  T=0 F=53  T=0 F=3  if (info[i].myanmar_category() == M_Cat(MR)) /* Pre-base ...
  d=1   L 234  T=46 F=7  T=0 F=3  if (info[i].myanmar_category() == M_Cat(VPre)) /* Left ma...
  d=1   L 239  T=5 F=2  T=0 F=3  if (info[i].myanmar_category() == M_Cat(VS))
  d=1   L 278  T=88 F=34  T=20 F=17  for (unsigned int i = start; i < end; i++)
  d=1   L 280  T=46 F=42  T=0 F=20  if (info[i].myanmar_position() == POS_PRE_M)  <-- BLOCKER
  d=1   L 282  T=19 F=27  T=0 F=0  if (first_left_matra == end)
  d=1   L 288  T=12 F=22  T=0 F=17  if (first_left_matra < last_left_matra)
  d=1   L 294  T=39 F=12  T=0 F=0  for (unsigned j = i; j <= last_left_matra; j++)
  d=1   L 295  T=39 F=0  T=0 F=0  if (info[j].myanmar_category() == M_Cat(VPre))

[off-chain: 1 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0e76e2806b7c2baf, size=20 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=675s, mutation_op=BytesDeleteMutator,BitFlipMutator):
  0000: 3b 10 00 00 84 10 00 00 1a 10 00 00 08 fe 00 00   ;...............
  0010: 84 10 82 d7                                       ....
Seed 2 (id=a17d8c60d6c37a97, size=46 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=675s, mutation_op=BitFlipMutator,WordInterestingMutator,CrossoverReplaceMutator,BytesExpandMutator):
  0000: 3b 10 00 00 84 10 00 00 1a 10 00 00 00 fe 00 00   ;...............
  0010: 84 10 a2 d7 d7 d7 d7 d7 d7 00 80 00 00 fe 00 00   ................
  0020: 84 10 a2 d7 d7 d7 d7 d7 d7 00 80 6e 74 1a         ...........nt.
Seed 3 (id=a80fc5dfdef828cb, size=55 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=789s, mutation_op=BytesExpandMutator,ByteDecMutator,QwordAddMutator):
  0000: 3b 10 00 00 84 10 00 00 31 10 00 00 84 10 00 00   ;.......1.......
  0010: 1a 10 00 00 00 fe 00 00 84 10 82 84 84 84 00 00   ................
  0020: 00 fe 00 00 84 10 82 84 84 84 84 83 d7 d7 d7 d7   ................
  0030: d7 d7 d7 d7 cb d7 1a                              .......
Seed 4 (id=98f4f71395a980f9, size=55 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=902s, mutation_op=TokenInsert,ByteIncMutator,BytesDeleteMutator,CrossoverInsertMutator,ByteAddMutator,TokenReplace):
  0000: 3b 10 00 00 84 10 00 00 31 10 00 00 84 10 00 00   ;.......1.......
  0010: 1a 10 00 00 00 fe 0c 00 84 10 82 84 84 84 00 00   ................
  0020: 00 fe 00 00 84 10 82 84 84 84 84 83 d7 d7 d7 d7   ................
  0030: d7 d7 d7 d7 cb d7 1a                              .......
Seed 5 (id=a838cde871a03f89, size=57 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=902s, mutation_op=ByteFlipMutator,BytesRandInsertMutator,BitFlipMutator):
  0000: 3f 10 00 00 84 10 00 00 31 10 00 00 84 ef 00 00   ?.......1.......
  0010: 1a 10 00 00 00 fe 00 00 84 10 82 84 84 84 00 00   ................
  0020: 00 fe 00 00 84 10 2f 2f 82 84 84 84 84 83 d7 d7   ......//........
  0030: d7 d7 d7 d7 d7 d7 cb d7 1a                        .........

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=04d8571de170df2e, size=77 bytes, fuzzer=cmplog, trial=1, discovered_at=28s, mutation_op=ByteInterestingMutator,TokenReplace,BytesDeleteMutator):
  0000: 00 01 02 00 01 00 f9 f9 f9 00 01 00 f9 f9 f9 f9   ................
  0010: f9 f0 00 10 00 00 20 f9 f9 f9 f9 f0 f9 f9 f9 f9   ...... .........
  0020: f9 00 10 00 00 20 06 00 00 02 08 01 01 01 01 01   ..... ..........
  0030: 01 00 01 00 00 00 01 20 00 1a 20 20 20 39 39 39   ....... ..   999
Seed 2 (id=02a49f927f1125e3, size=25 bytes, fuzzer=cmplog, trial=1, discovered_at=130s, mutation_op=DwordAddMutator,WordInterestingMutator,ByteRandMutator,TokenInsert,BytesDeleteMutator):
  0000: 6b 20 00 00 01 10 00 00 68 61 73 63 12 16 01 00   k ......hasc....
  0010: 00 80 00 00 0e 01 00 00 65                        ........e
Seed 3 (id=031a883624e0ba3f, size=40 bytes, fuzzer=cmplog, trial=1, discovered_at=384s, mutation_op=BytesInsertCopyMutator,BytesSetMutator,BytesCopyMutator,BitFlipMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesRandSetMutator):
  0000: a4 a4 a4 a4 a4 63 66 63 10 0d 0b 00 21 0d 10 00   .....cfc....!...
  0010: fd a9 00 00 60 20 63 73 61 68 ff ff ff 03 f0 00   ....` csah......
  0020: 71 0e 00 ff 03 f0 11 00                           q.......
Seed 4 (id=051c163734ad5d08, size=35 bytes, fuzzer=cmplog, trial=1, discovered_at=506s, mutation_op=ByteFlipMutator,BytesInsertMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesCopyMutator):
  0000: 1e 03 80 00 00 00 6b 67 10 00 71 0f 72 10 00 00   ......kg..q.r...
  0010: 8d 10 00 00 8d 10 00 00 73 10 00 00 8d 10 00 00   ........s.......
  0020: 73 10 00                                          s..
Seed 5 (id=04223d85d25f4e4e, size=76 bytes, fuzzer=cmplog, trial=1, discovered_at=987s, mutation_op=ByteDecMutator,ByteNegMutator,BytesRandInsertMutator,BytesSwapMutator,TokenReplace,BytesInsertMutator,BytesSwapMutator):
  0000: fa fa 00 6f 77 0d aa 00 00 00 00 9b fd a9 00 00   ...ow...........
  0010: 60 00 00 00 00 00 00 00 00 00 00 00 fd a9 00 00   `...............
  0020: 60 00 16 a9 00 22 60 aa aa 00 cd cd cd cd cd 00   `...."`.........
  0030: 00 60 21 0d 01 20 00 00 fd a9 00 00 f8 25 cd cd   .`!.. .......%..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  3b(;)x7 00(.)x7 3f(?)x1 61(a)x1     00(.)x6 6b(k)x1 a4(.)x1 1e(.)x1 +1u  PARTIAL
   0x0001  10(.)x12 00(.)x3 6e(n)x1            01(.)x6 20( )x1 a4(.)x1 03(.)x1 +1u  DIFFER
   0x0002  00(.)x14 01(.)x1 2e(.)x1            00(.)x7 02(.)x1 a4(.)x1 80(.)x1     PARTIAL
   0x0003  00(.)x14 01(.)x1 2e(.)x1            00(.)x8 a4(.)x1 6f(o)x1             PARTIAL
   0x0004  84(.)x12 00(.)x2 61(a)x1 d2(.)x1    00(.)x6 01(.)x2 a4(.)x1 77(w)x1     PARTIAL
   0x0005  10(.)x14 6e(n)x1 17(.)x1            01(.)x4 00(.)x2 10(.)x1 63(c)x1 +2u  PARTIAL
   0x0006  00(.)x14 2e(.)x1 ff(.)x1            20( )x2 07(.)x2 f9(.)x1 00(.)x1 +4u  PARTIAL
   0x0007  00(.)x15 2e(.)x1                    20( )x4 00(.)x3 f9(.)x1 63(c)x1 +1u  PARTIAL
   0x0009  10(.)x14 2e(.)x1 17(.)x1            00(.)x4 20( )x4 61(a)x1 0d(.)x1     DIFFER
   0x000a  00(.)x15 2e(.)x1                    20( )x3 1e(.)x2 01(.)x1 73(s)x1 +3u  PARTIAL
   0x000b  00(.)x15 61(a)x1                    20( )x5 00(.)x2 63(c)x1 0f(.)x1 +1u  PARTIAL
   0x000d  10(.)x12 fe(.)x2 ef(.)x1 06(.)x1    50(P)x3 41(A)x2 f9(.)x1 16(.)x1 +3u  PARTIAL
   0x000e  00(.)x15 06(.)x1                    4f(O)x3 00(.)x2 54(T)x2 f9(.)x1 +2u  PARTIAL
   0x000f  00(.)x15 06(.)x1                    00(.)x4 53(S)x3 48(H)x2 f9(.)x1     PARTIAL
   0x0011  10(.)x14 6e(n)x1 17(.)x1            01(.)x5 f0(.)x1 80(.)x1 a9(.)x1 +2u  PARTIAL
   0x0012  00(.)x11 82(.)x1 a2(.)x1 06(.)x1    00(.)x10                            PARTIAL
   0x0013  00(.)x11 d7(.)x2 06(.)x1            00(.)x4 80(.)x2 0d(.)x2 10(.)x1 +1u  PARTIAL
   0x0014  00(.)x5 84(.)x5 d7(.)x1 31(1)x1 +1u  00(.)x7 0e(.)x1 60(`)x1 8d(.)x1     PARTIAL
   0x0015  10(.)x6 fe(.)x4 d7(.)x1 73(s)x1 +1u  00(.)x7 01(.)x1 20( )x1 10(.)x1     PARTIAL
   0x0016  00(.)x11 d7(.)x1 0c(.)x1            00(.)x8 20( )x1 63(c)x1             PARTIAL
   0x0017  00(.)x11 d7(.)x1 06(.)x1            10(.)x5 00(.)x3 f9(.)x1 73(s)x1     PARTIAL
   0x001b  84(.)x5 00(.)x4 72(r)x1             00(.)x3 03(.)x2 47(G)x2 f0(.)x1 +1u  PARTIAL
   0x001e  00(.)x7 05(.)x1 10(.)x1 ff(.)x1     00(.)x6 f9(.)x1 f0(.)x1 30(0)x1     PARTIAL
   0x001f  00(.)x7 84(.)x1 dd(.)x1 c2(.)x1     00(.)x5 03(.)x2 f9(.)x1 30(0)x1     PARTIAL
   0x0024  84(.)x5 d7(.)x1 05(.)x1 1c(.)x1 +2u  00(.)x4 4f(O)x2 03(.)x1 01(.)x1     PARTIAL
   0x0028  84(.)x4 00(.)x2 d7(.)x1 82(.)x1 +1u  00(.)x4 aa(.)x1 ff(.)x1 03(.)x1     PARTIAL
   0x0029  84(.)x5 00(.)x3 0c(.)x1             00(.)x3 01(.)x2 02(.)x1 10(.)x1     PARTIAL
   0x002a  00(.)x5 84(.)x3 80(.)x1             00(.)x2 08(.)x1 cd(.)x1 6b(k)x1 +2u  PARTIAL
   0x002b  00(.)x4 83(.)x2 6e(n)x1 84(.)x1 +1u  01(.)x3 10(.)x2 cd(.)x1 61(a)x1     DIFFER
   0x002c  d7(.)x2 00(.)x2 74(t)x1 84(.)x1 +2u  00(.)x3 01(.)x2 cd(.)x1 72(r)x1     PARTIAL
   0x002e  00(.)x4 d7(.)x3                     01(.)x1 cd(.)x1 7f(.)x1 20( )x1 +3u  PARTIAL
   0x0030  d7(.)x3 ff(.)x1 84(.)x1 53(S)x1 +1u  00(.)x5 01(.)x1 20( )x1             DIFFER
   0x0032  d7(.)x3 00(.)x2 82(.)x1 53(S)x1     00(.)x3 01(.)x1 21(!)x1 e3(.)x1 +1u  PARTIAL
   0x0033  d7(.)x4 84(.)x1 53(S)x1 cf(.)x1     00(.)x3 0d(.)x1 e3(.)x1 01(.)x1 +1u  DIFFER
   0x0034  cb(.)x3 84(.)x2 d7(.)x1 17(.)x1     00(.)x3 01(.)x2 e3(.)x1 73(s)x1     DIFFER
   0x0035  d7(.)x4 84(.)x2 00(.)x1             00(.)x1 20( )x1 e3(.)x1 6e(n)x1 +3u  PARTIAL
   0x0036  1a(.)x3 cb(.)x1 46(F)x1 84(.)x1 +1u  00(.)x3 01(.)x2 e6(.)x1 2d(-)x1     PARTIAL
   0x0037  d7(.)x1 46(F)x1 83(.)x1 c8(.)x1     00(.)x3 20( )x1 1a(.)x1 68(h)x1 +1u  DIFFER
   0x0038  1a(.)x1 46(F)x1 d7(.)x1 17(.)x1     00(.)x2 01(.)x2 fd(.)x1 20( )x1 +1u  DIFFER
   0x0039  46(F)x1 d7(.)x1 00(.)x1             1a(.)x1 a9(.)x1 20( )x1 6e(n)x1 +3u  PARTIAL
   ... (6 more divergent offsets)
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
  prompts_b/harfbuzz_5947.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5947,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5947 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5947 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5947 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).