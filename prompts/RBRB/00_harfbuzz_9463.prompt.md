==== BLOCKER ====
Target: harfbuzz
Branch ID: 9463
Location: /src/harfbuzz/src/hb-ot-shaper-myanmar.cc:217:12
Enclosing function: hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int)
Source line:     for (; i < base; i++)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive)
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             1        9          0  loser (I2S vs value_profile)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     []

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 17  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=3.35h  loser=11.15h
  avg hitcount on branch: winner=23  loser=0
  prob_div=0.90  dur_div=7.80h  hit_div=22
  subject-level: delta_AUC=9064080.0  p_AUC=0.0002  delta_Final=796.1  p_final=0.0002
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 20  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=2.05h  loser=11.55h
  avg hitcount on branch: winner=13  loser=0
  prob_div=0.90  dur_div=9.50h  hit_div=13
  subject-level: delta_AUC=12333210.0  p_AUC=0.0002  delta_Final=1452.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/9463/{W,L}/branch_coverage_show.txt

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
[B]   217      for (; i < base; i++) <-- BLOCKER
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
[W]   228      {
[W]   229        if (info[i].myanmar_category() == M_Cat(MR)) /* Pre-base reordering */
[ ]   230        {
[ ]   231  	info[i].myanmar_position() = POS_PRE_C;
[ ]   232  	continue;
[ ]   233        }
[W]   234        if (info[i].myanmar_category() == M_Cat(VPre)) /* Left matra */
[ ]   235        {
[ ]   236  	info[i].myanmar_position() = POS_PRE_M;
[ ]   237  	continue;
[ ]   238        }
[W]   239        if (info[i].myanmar_category() == M_Cat(VS))
[ ]   240        {
[ ]   241  	info[i].myanmar_position() = info[i - 1].myanmar_position();
[ ]   242  	continue;
[ ]   243        }
[ ]   244  
[W]   245        if (pos == POS_AFTER_MAIN && info[i].myanmar_category() == M_Cat(VBlw))
[ ]   246        {
[ ]   247  	pos = POS_BELOW_C;
[ ]   248  	info[i].myanmar_position() = pos;
[ ]   249  	continue;
[ ]   250        }
[ ]   251  
[W]   252        if (pos == POS_BELOW_C && info[i].myanmar_category() == M_Cat(A))
[ ]   253        {
[ ]   254  	info[i].myanmar_position() = POS_BEFORE_SUB;
[ ]   255  	continue;
[ ]   256        }
[W]   257        if (pos == POS_BELOW_C && info[i].myanmar_category() == M_Cat(VBlw))
[ ]   258        {
[ ]   259  	info[i].myanmar_position() = pos;
[ ]   260  	continue;
[ ]   261        }
[W]   262        if (pos == POS_BELOW_C && info[i].myanmar_category() != M_Cat(A))
[ ]   263        {
[ ]   264  	pos = POS_AFTER_SUB;
[ ]   265  	info[i].myanmar_position() = pos;
[ ]   266  	continue;
[ ]   267        }
[W]   268        info[i].myanmar_position() = pos;
[W]   269      }
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
[B]   280      if (info[i].myanmar_position() == POS_PRE_M)
[ ]   281      {
[ ]   282        if (first_left_matra == end)
[ ]   283  	first_left_matra = i;
[ ]   284        last_left_matra = i;
[ ]   285      }
[B]   286    }
[ ]   287    /* https://github.com/harfbuzz/harfbuzz/issues/3863 */
[B]   288    if (first_left_matra < last_left_matra)
[ ]   289    {
[ ]   290      /* No need to merge clusters, done already? */
[ ]   291      buffer->reverse_range (first_left_matra, last_left_matra + 1);
[ ]   292      /* Reverse back VS, etc. */
[ ]   293      unsigned i = first_left_matra;
[ ]   294      for (unsigned j = i; j <= last_left_matra; j++)
[ ]   295        if (info[j].myanmar_category() == M_Cat(VPre))
[ ]   296        {
[ ]   297  	buffer->reverse_range (i, j + 1);
[ ]   298  	i = j + 1;
[ ]   299        }
[ ]   300    }
[B]   301  }

--- No 1-hop callers of hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      40         0  hb-ot-shaper-myanmar.cc:compare_myanmar_order(hb_glyph_info_t const*, hb_glyph_info_t const*)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:167-172)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-myanmar.cc:initial_reordering_consonant_syllable(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-myanmar.cc:181-301) ---
  d=1   L 189  T=13 F=32  T=0 F=21  if (start + 3 <= end &&
  d=1   L 190  T=0 F=13  T=0 F=0  info[start  ].myanmar_category() == M_Cat(Ra) &&
  d=1   L 200  T=45 F=0  T=21 F=0  if (!has_reph)
  d=1   L 203  T=62 F=9  T=21 F=0  for (unsigned int i = limit; i < end; i++)
  d=1   L 204  T=36 F=26  T=21 F=0  if (is_consonant_myanmar (info[i]))
  d=1   L 215  T=0 F=45  T=0 F=21  for (; i < start + (has_reph ? 3 : 0); i++)
  d=1   L 215  T=0 F=45  T=0 F=21  for (; i < start + (has_reph ? 3 : 0); i++)
  d=1   L 217  T=17 F=45  T=0 F=21  for (; i < base; i++)  <-- BLOCKER
  d=1   L 219  T=45 F=0  T=21 F=0  if (i < end)
  d=1   L 227  T=23 F=45  T=0 F=21  for (; i < end; i++)
  d=1   L 229  T=0 F=23  T=0 F=0  if (info[i].myanmar_category() == M_Cat(MR)) /* Pre-base ...
  d=1   L 234  T=0 F=23  T=0 F=0  if (info[i].myanmar_category() == M_Cat(VPre)) /* Left ma...
  d=1   L 239  T=0 F=23  T=0 F=0  if (info[i].myanmar_category() == M_Cat(VS))
  d=1   L 245  T=0 F=23  T=0 F=0  if (pos == POS_AFTER_MAIN && info[i].myanmar_category() =...
  d=1   L 245  T=23 F=0  T=0 F=0  if (pos == POS_AFTER_MAIN && info[i].myanmar_category() =...
  d=1   L 252  T=0 F=23  T=0 F=0  if (pos == POS_BELOW_C && info[i].myanmar_category() == M...
  d=1   L 257  T=0 F=23  T=0 F=0  if (pos == POS_BELOW_C && info[i].myanmar_category() == M...
  d=1   L 262  T=0 F=23  T=0 F=0  if (pos == POS_BELOW_C && info[i].myanmar_category() != M...
  d=1   L 278  T=85 F=45  T=21 F=21  for (unsigned int i = start; i < end; i++)
  d=1   L 280  T=0 F=85  T=0 F=21  if (info[i].myanmar_position() == POS_PRE_M)
  d=1   L 288  T=0 F=45  T=0 F=21  if (first_left_matra < last_left_matra)

[off-chain: 2 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=28fc288a1cdeafa0, size=80 bytes, fuzzer=cmplog, trial=2, discovered_at=3657s, mutation_op=BytesRandSetMutator):
  0000: 99 20 99 b0 14 01 00 99 00 03 5a 31 cd e8 03 00   . ........Z1....
  0010: 00 10 00 00 ff 0a 0c 00 0a 01 00 6d 6f 73 69 99   ...........mosi.
  0020: cd 0a 00 00 00 10 00 00 ff 0a 00 00 cd 0a 00 00   ................
  0030: 00 10 00 00 ff f6 01 00 0a 01 00 00 cd 0a aa aa   ................
Seed 2 (id=96b4e6ba26862807, size=80 bytes, fuzzer=cmplog, trial=2, discovered_at=3657s, mutation_op=BytesCopyMutator):
  0000: 99 20 99 b0 14 01 00 99 00 03 5a 31 cd e8 03 00   . ........Z1....
  0010: 00 10 00 00 ff 0a 00 00 0a 01 00 6d 6f 73 69 99   ...........mosi.
  0020: cd 0a 00 00 00 10 00 00 ff 0a 00 01 cd 0a 00 00   ................
  0030: 00 01 00 6d 6f 73 69 99 cd 0a 00 00 00 10 00 00   ...mosi.........
Seed 3 (id=7cc7525f707414e7, size=80 bytes, fuzzer=cmplog, trial=2, discovered_at=4524s, mutation_op=ByteFlipMutator,ByteNegMutator,ByteRandMutator,ByteIncMutator,ByteNegMutator,BitFlipMutator):
  0000: 99 20 99 b0 14 01 00 99 00 03 5a 31 cd e8 03 00   . ........Z1....
  0010: 00 10 00 00 ff 0a 00 00 0a 01 00 6d 6f 73 69 99   ...........mosi.
  0020: cd 0a 00 00 00 10 00 00 ff 0a 00 00 cd 0a 00 00   ................
  0030: 00 00 00 6d 6f 73 69 99 cd 0a 04 04 00 10 00 00   ...mosi.........
Seed 4 (id=67a50c4c4bd51ed2, size=80 bytes, fuzzer=cmplog, trial=2, discovered_at=4583s, mutation_op=ByteInterestingMutator,DwordInterestingMutator,DwordInterestingMutator,BytesDeleteMutator,TokenInsert,BytesDeleteMutator):
  0000: 99 20 99 b0 14 01 00 99 00 03 5a 31 cd e8 03 00   . ........Z1....
  0010: 00 10 00 00 ff 0a 00 00 0a 01 00 6d 6f 73 69 99   ...........mosi.
  0020: cd 0a 00 00 00 10 00 00 ff 0a 00 00 cd 0a 00 00   ................
  0030: 02 00 00 6d 6f 73 69 99 cd 0a 00 04 00 10 00 00   ...mosi.........
Seed 5 (id=5f5fab089e20c862, size=84 bytes, fuzzer=cmplog, trial=2, discovered_at=4631s, mutation_op=BytesSwapMutator,ByteNegMutator,BitFlipMutator):
  0000: 99 20 99 b0 14 01 00 99 00 03 5a 31 cd e8 03 0a   . ........Z1....
  0010: 00 10 04 00 ff 0a 0a 00 0a 00 00 6d 6f 73 69 99   ...........mosi.
  0020: cd ff ff 00 00 10 00 00 94 0b 00 00 cd 0a 64 6e   ..............dn
  0030: 61 72 00 6d 6f 73 69 9b cd 0a 04 04 00 10 00 00   ar.mosi.........

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00293b686680cdda, size=66 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=BytesRandSetMutator,BytesCopyMutator,TokenInsert):
  0000: 00 00 01 10 00 00 00 20 20 20 20 20 20 6b 00 08   .......      k..
  0010: 00 00 01 20 20 20 04 00 00 01 00 7f 20 6b 65 7a   ...   ...... kez
  0020: 68 2d 68 61 6e 74 2d 6d 6f 00 72 6e 20 20 20 20   h-hant-mo.rn    
  0030: 00 02 00 20 00 02 00 20 20 20 20 60 00 1a 20 23   ... ...    `.. #
Seed 2 (id=0078665cd55688d0, size=23 bytes, fuzzer=cmplog, trial=1, discovered_at=93s, mutation_op=BytesDeleteMutator,ByteRandMutator,ByteNegMutator,BytesDeleteMutator):
  0000: 00 10 00 00 00 00 20 20 10 0a 00 00 00 00 00 20   ......  ....... 
  0010: 20 10 00 00 00 00 20                               ..... 
Seed 3 (id=012fd22e30076039, size=45 bytes, fuzzer=cmplog, trial=1, discovered_at=359s, mutation_op=BytesCopyMutator,ByteRandMutator,BytesInsertCopyMutator,ByteRandMutator,ByteDecMutator,WordAddMutator):
  0000: 74 70 78 2d 00 10 00 00 00 1f 16 01 00 a0 00 00   tpx-............
  0010: 00 a0 00 00 20 ff 00 00 00 26 00 00 74 70 20 2d   .... ....&..tp -
  0020: 00 10 20 05 64 6e c1 20 00 20 20 20 20            .. .dn. .    
Seed 4 (id=0045c9404813a29a, size=38 bytes, fuzzer=cmplog, trial=1, discovered_at=493s, mutation_op=ByteRandMutator,BytesDeleteMutator,TokenInsert,QwordAddMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 00 00 00 01 00 00 b1 b1 b1 00 00 00 00 10 00 00   ................
  0010: 00 00 00 00 00 20 20 20 20 00 b1 b1 b1 00 00 00   .....    .......
  0020: 00 10 00 00 00 00                                 ......
Seed 5 (id=002242b926005ecd, size=98 bytes, fuzzer=cmplog, trial=1, discovered_at=514s, mutation_op=WordAddMutator,BytesExpandMutator,CrossoverReplaceMutator):
  0000: 01 00 01 00 01 20 20 20 20 03 02 00 01 75 72 00   .....    ....ur.
  0010: 76 30 6c 6c 6c 6c 00 64 20 20 10 02 fb fb fb fb   v0llll.d  ......
  0020: fb 7f 06 00 00 00 80 10 00 00 00 02 00 00 80 10   ................
  0030: 00 00 00 02 00 00 20 10 01 00 01 00 00 00 20 10   ...... ....... .


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  99(.)x10                            00(.)x7 74(t)x1 01(.)x1 0a(.)x1     DIFFER
   0x0001  20( )x7 b2(.)x3                     00(.)x4 01(.)x3 10(.)x1 70(p)x1 +1u  DIFFER
   0x0002  99(.)x7 14(.)x3                     00(.)x6 01(.)x3 78(x)x1             DIFFER
   0x0003  b0(.)x7 01(.)x3                     00(.)x7 10(.)x1 2d(-)x1 01(.)x1     PARTIAL
   0x0004  14(.)x7 00(.)x3                     00(.)x8 01(.)x1 64(d)x1             PARTIAL
   0x0005  01(.)x7 99(.)x3                     00(.)x3 04(.)x2 10(.)x1 20( )x1 +3u  PARTIAL
   0x0006  00(.)x10                            20( )x5 00(.)x3 b1(.)x1 0d(.)x1     PARTIAL
   0x0007  99(.)x7 03(.)x3                     00(.)x4 20( )x3 b1(.)x1 06(.)x1 +1u  PARTIAL
   0x0008  00(.)x7 5a(Z)x3                     00(.)x5 20( )x2 10(.)x1 b1(.)x1 +1u  PARTIAL
   0x0009  03(.)x7 31(1)x3                     7f(.)x3 00(.)x2 20( )x1 0a(.)x1 +3u  PARTIAL
   0x000a  5a(Z)x7 cd(.)x3                     00(.)x7 20( )x1 16(.)x1 02(.)x1     DIFFER
   0x000b  31(1)x7 e8(.)x3                     00(.)x5 20( )x3 01(.)x1 ff(.)x1     DIFFER
   0x000c  cd(.)x7 03(.)x3                     00(.)x5 20( )x3 01(.)x1 ff(.)x1     DIFFER
   0x000d  e8(.)x7 0a(.)x3                     00(.)x2 20( )x2 6b(k)x1 a0(.)x1 +4u  DIFFER
   0x000e  03(.)x7 00(.)x3                     00(.)x4 56(V)x2 72(r)x1 c7(.)x1 +2u  PARTIAL
   0x000f  00(.)x5 6d(m)x3 0a(.)x2             00(.)x4 20( )x2 56(V)x2 08(.)x1 +1u  PARTIAL
   0x0010  00(.)x7 6f(o)x3                     00(.)x3 20( )x3 41(A)x2 76(v)x1 +1u  PARTIAL
   0x0011  10(.)x7 73(s)x3                     00(.)x3 10(.)x1 a0(.)x1 30(0)x1 +4u  PARTIAL
   0x0012  00(.)x5 69(i)x3 04(.)x2             00(.)x3 b9(.)x2 01(.)x1 6c(l)x1 +2u  PARTIAL
   0x0013  00(.)x7 9b(.)x3                     00(.)x3 20( )x2 b9(.)x2 6c(l)x1 +1u  PARTIAL
   0x0014  ff(.)x7 cd(.)x3                     20( )x3 00(.)x2 b9(.)x2 6c(l)x1 +1u  DIFFER
   0x0015  0a(.)x10                            20( )x3 01(.)x2 00(.)x1 ff(.)x1 +2u  DIFFER
   0x0016  00(.)x4 04(.)x3 0a(.)x2 0c(.)x1     20( )x3 00(.)x2 ff(.)x2 04(.)x1 +1u  PARTIAL
   0x0017  00(.)x7 04(.)x3                     00(.)x3 ff(.)x3 20( )x1 64(d)x1     PARTIAL
   0x0018  0a(.)x7 00(.)x3                     00(.)x3 fe(.)x3 20( )x2             PARTIAL
   0x0019  01(.)x5 10(.)x3 00(.)x1 02(.)x1     f2(.)x3 01(.)x2 26(&)x1 00(.)x1 +1u  PARTIAL
   0x001a  00(.)x10                            1a(.)x3 00(.)x2 b1(.)x1 10(.)x1 +1u  PARTIAL
   0x001b  6d(m)x7 00(.)x3                     20( )x3 7f(.)x1 00(.)x1 b1(.)x1 +2u  PARTIAL
   0x001c  6f(o)x7 de(.)x3                     47(G)x3 20( )x1 74(t)x1 b1(.)x1 +2u  DIFFER
   0x001d  73(s)x7 fe(.)x3                     50(P)x3 6b(k)x1 70(p)x1 00(.)x1 +2u  DIFFER
   0x001e  69(i)x7 ff(.)x3                     4f(O)x3 65(e)x1 20( )x1 00(.)x1 +2u  DIFFER
   0x001f  99(.)x7 10(.)x3                     53(S)x3 7a(z)x1 2d(-)x1 00(.)x1 +2u  DIFFER
   0x0020  cd(.)x7 00(.)x3                     00(.)x4 68(h)x1 fb(.)x1 02(.)x1 +1u  PARTIAL
   0x0021  0a(.)x8 ff(.)x2                     00(.)x3 10(.)x2 2d(-)x1 7f(.)x1 +1u  DIFFER
   0x0022  00(.)x6 ff(.)x2 06(.)x2             03(.)x3 20( )x2 68(h)x1 00(.)x1 +1u  PARTIAL
   0x0023  00(.)x9 03(.)x1                     00(.)x4 20( )x2 61(a)x1 05(.)x1     PARTIAL
   0x0024  00(.)x6 cd(.)x3 0a(.)x1             00(.)x5 6e(n)x1 64(d)x1 80(.)x1     PARTIAL
   0x0025  10(.)x6 0a(.)x3 00(.)x1             00(.)x5 74(t)x1 6e(n)x1 11(.)x1     PARTIAL
   0x0026  00(.)x10                            00(.)x3 2d(-)x1 c1(.)x1 80(.)x1 +1u  PARTIAL
   0x0027  00(.)x9 01(.)x1                     00(.)x3 10(.)x2 6d(m)x1 20( )x1     PARTIAL
   ... (23 more divergent offsets)
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
rows are exclusive to cmplog and value_profile_cmplog; their
presence in a winning seed's ancestor chain is direct (lower-bound)
evidence of I2S contribution.

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
  prompts/RBRB/00_harfbuzz_9463.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9463,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile>value_profile_cmplog (I2S)]
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
      // pick EXACTLY ONE of:
      //   "I2SRandReplace"     (cmplog / vpc input-to-state substitution)
      //   "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)
      //   "havoc-only"         (lucky havoc byte mutation, no CMP introspection)
      //   "token-replace"      (TokenInsert/TokenReplace dictionary mutations)
      //   "other"              (anything that does not fit the four above)
    "verified_in_lineage": true,
      // pick true or false
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9463 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9463 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9463 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).