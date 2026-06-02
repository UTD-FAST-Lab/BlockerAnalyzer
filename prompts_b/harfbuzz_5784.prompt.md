==== BLOCKER ====
Target: harfbuzz
Branch ID: 5784
Location: /src/harfbuzz/src/hb-ot-shaper-hebrew.cc:81:7
Enclosing function: hb-ot-shaper-hebrew.cc:compose_hebrew(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)
Source line:   if (!found && !c->plan->has_gpos_mark)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive)
value_profile                    9        1          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             0       10          0  loser (I2S vs value_profile)
naive_ctx                        9        1          0  REFERENCE
naive_ngram4                     9        1          0  REFERENCE
mopt                             8        2          0  REFERENCE
minimizer                       10        0          0  REFERENCE
fast                             9        1          0  REFERENCE
grimoire                         0       10          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.20h  loser=20.30h
  avg hitcount on branch: winner=8  loser=0
  prob_div=0.90  dur_div=13.10h  hit_div=8
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=8.60h  loser=21.80h
  avg hitcount on branch: winner=7  loser=0
  prob_div=0.90  dur_div=13.20h  hit_div=7
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5784/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-hebrew.cc:compose_hebrew(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*) (/src/harfbuzz/src/hb-ot-shaper-hebrew.cc:39-163) ---
[ ]    37  		hb_codepoint_t  b,
[ ]    38  		hb_codepoint_t *ab)
[B]    39  {
[ ]    40    /* Hebrew presentation-form shaping.
[ ]    41     * https://bugzilla.mozilla.org/show_bug.cgi?id=728866
[ ]    42     * Hebrew presentation forms with dagesh, for characters U+05D0..05EA;
[ ]    43     * Note that some letters do not have a dagesh presForm encoded.
[ ]    44     */
[B]    45    static const hb_codepoint_t sDageshForms[0x05EAu - 0x05D0u + 1] = {
[B]    46      0xFB30u, /* ALEF */
[B]    47      0xFB31u, /* BET */
[B]    48      0xFB32u, /* GIMEL */
[B]    49      0xFB33u, /* DALET */
[B]    50      0xFB34u, /* HE */
[B]    51      0xFB35u, /* VAV */
[B]    52      0xFB36u, /* ZAYIN */
[B]    53      0x0000u, /* HET */
[B]    54      0xFB38u, /* TET */
[B]    55      0xFB39u, /* YOD */
[B]    56      0xFB3Au, /* FINAL KAF */
[B]    57      0xFB3Bu, /* KAF */
[B]    58      0xFB3Cu, /* LAMED */
[B]    59      0x0000u, /* FINAL MEM */
[B]    60      0xFB3Eu, /* MEM */
[B]    61      0x0000u, /* FINAL NUN */
[B]    62      0xFB40u, /* NUN */
[B]    63      0xFB41u, /* SAMEKH */
[B]    64      0x0000u, /* AYIN */
[B]    65      0xFB43u, /* FINAL PE */
[B]    66      0xFB44u, /* PE */
[B]    67      0x0000u, /* FINAL TSADI */
[B]    68      0xFB46u, /* TSADI */
[B]    69      0xFB47u, /* QOF */
[B]    70      0xFB48u, /* RESH */
[B]    71      0xFB49u, /* SHIN */
[B]    72      0xFB4Au /* TAV */
[B]    73    };
[ ]    74  
[B]    75    bool found = (bool) c->unicode->compose (a, b, ab);
[ ]    76  
[ ]    77  #ifdef HB_NO_OT_SHAPER_HEBREW_FALLBACK
[ ]    78    return found;
[ ]    79  #endif
[ ]    80  
[B]    81    if (!found && !c->plan->has_gpos_mark) <-- BLOCKER
[B]    82    {
[ ]    83        /* Special-case Hebrew presentation forms that are excluded from
[ ]    84         * standard normalization, but wanted for old fonts. */
[B]    85        switch (b) {
[B]    86        case 0x05B4u: /* HIRIQ */
[B]    87  	  if (a == 0x05D9u) { /* YOD */
[ ]    88  	      *ab = 0xFB1Du;
[ ]    89  	      found = true;
[ ]    90  	  }
[B]    91  	  break;
[L]    92        case 0x05B7u: /* PATAH */
[L]    93  	  if (a == 0x05F2u) { /* YIDDISH YOD YOD */
[ ]    94  	      *ab = 0xFB1Fu;
[ ]    95  	      found = true;
[L]    96  	  } else if (a == 0x05D0u) { /* ALEF */
[ ]    97  	      *ab = 0xFB2Eu;
[ ]    98  	      found = true;
[ ]    99  	  }
[L]   100  	  break;
[L]   101        case 0x05B8u: /* QAMATS */
[L]   102  	  if (a == 0x05D0u) { /* ALEF */
[ ]   103  	      *ab = 0xFB2Fu;
[ ]   104  	      found = true;
[ ]   105  	  }
[L]   106  	  break;
[L]   107        case 0x05B9u: /* HOLAM */
[L]   108  	  if (a == 0x05D5u) { /* VAV */
[ ]   109  	      *ab = 0xFB4Bu;
[ ]   110  	      found = true;
[ ]   111  	  }
[L]   112  	  break;
[L]   113        case 0x05BCu: /* DAGESH */
[L]   114  	  if (a >= 0x05D0u && a <= 0x05EAu) {
[ ]   115  	      *ab = sDageshForms[a - 0x05D0u];
[ ]   116  	      found = (*ab != 0);
[L]   117  	  } else if (a == 0xFB2Au) { /* SHIN WITH SHIN DOT */
[ ]   118  	      *ab = 0xFB2Cu;
[ ]   119  	      found = true;
[L]   120  	  } else if (a == 0xFB2Bu) { /* SHIN WITH SIN DOT */
[ ]   121  	      *ab = 0xFB2Du;
[ ]   122  	      found = true;
[ ]   123  	  }
[L]   124  	  break;
[L]   125        case 0x05BFu: /* RAFE */
[L]   126  	  switch (a) {
[ ]   127  	  case 0x05D1u: /* BET */
[ ]   128  	      *ab = 0xFB4Cu;
[ ]   129  	      found = true;
[ ]   130  	      break;
[ ]   131  	  case 0x05DBu: /* KAF */
[ ]   132  	      *ab = 0xFB4Du;
[ ]   133  	      found = true;
[ ]   134  	      break;
[ ]   135  	  case 0x05E4u: /* PE */
[ ]   136  	      *ab = 0xFB4Eu;
[ ]   137  	      found = true;
[ ]   138  	      break;
[L]   139  	  }
[L]   140  	  break;
[B]   141        case 0x05C1u: /* SHIN DOT */
[B]   142  	  if (a == 0x05E9u) { /* SHIN */
[ ]   143  	      *ab = 0xFB2Au;
[ ]   144  	      found = true;
[B]   145  	  } else if (a == 0xFB49u) { /* SHIN WITH DAGESH */
[ ]   146  	      *ab = 0xFB2Cu;
[ ]   147  	      found = true;
[ ]   148  	  }
[B]   149  	  break;
[L]   150        case 0x05C2u: /* SIN DOT */
[L]   151  	  if (a == 0x05E9u) { /* SHIN */
[ ]   152  	      *ab = 0xFB2Bu;
[ ]   153  	      found = true;
[L]   154  	  } else if (a == 0xFB49u) { /* SHIN WITH DAGESH */
[ ]   155  	      *ab = 0xFB2Du;
[ ]   156  	      found = true;
[ ]   157  	  }
[L]   158  	  break;
[B]   159        }
[B]   160    }
[ ]   161  
[B]   162    return found;
[B]   163  }

--- No 1-hop callers of hb-ot-shaper-hebrew.cc:compose_hebrew(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      16        48  hb-ot-shaper-hebrew.cc:reorder_marks_hebrew(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-hebrew.cc:170-190)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-hebrew.cc:compose_hebrew(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-hebrew.cc:39-163) ---
  d=1   L  81  T=14 F=0  T=67 F=0  if (!found && !c->plan->has_gpos_mark)  <-- BLOCKER
  d=1   L  81  T=14 F=12  T=67 F=0  if (!found && !c->plan->has_gpos_mark)  <-- BLOCKER
  d=1   L  85  T=11 F=3  T=27 F=40  switch (b) {
  d=1   L  86  T=1 F=13  T=7 F=60  case 0x05B4u: /* HIRIQ */
  d=1   L  87  T=0 F=1  T=0 F=7  if (a == 0x05D9u) { /* YOD */
  d=1   L  92  T=0 F=14  T=8 F=59  case 0x05B7u: /* PATAH */
  d=1   L  93  T=0 F=0  T=0 F=8  if (a == 0x05F2u) { /* YIDDISH YOD YOD */
  d=1   L  96  T=0 F=0  T=0 F=8  } else if (a == 0x05D0u) { /* ALEF */
  d=1   L 101  T=0 F=14  T=1 F=66  case 0x05B8u: /* QAMATS */
  d=1   L 102  T=0 F=0  T=0 F=1  if (a == 0x05D0u) { /* ALEF */
  d=1   L 107  T=0 F=14  T=6 F=61  case 0x05B9u: /* HOLAM */
  d=1   L 108  T=0 F=0  T=0 F=6  if (a == 0x05D5u) { /* VAV */
  d=1   L 113  T=0 F=14  T=2 F=65  case 0x05BCu: /* DAGESH */
  d=1   L 114  T=0 F=0  T=0 F=2  if (a >= 0x05D0u && a <= 0x05EAu) {
  d=1   L 114  T=0 F=0  T=2 F=0  if (a >= 0x05D0u && a <= 0x05EAu) {
  d=1   L 117  T=0 F=0  T=0 F=2  } else if (a == 0xFB2Au) { /* SHIN WITH SHIN DOT */
  d=1   L 120  T=0 F=0  T=0 F=2  } else if (a == 0xFB2Bu) { /* SHIN WITH SIN DOT */
  d=1   L 125  T=0 F=14  T=1 F=66  case 0x05BFu: /* RAFE */
  d=1   L 126  T=0 F=0  T=1 F=0  switch (a) {
  d=1   L 127  T=0 F=0  T=0 F=1  case 0x05D1u: /* BET */
  d=1   L 131  T=0 F=0  T=0 F=1  case 0x05DBu: /* KAF */
  d=1   L 135  T=0 F=0  T=0 F=1  case 0x05E4u: /* PE */
  d=1   L 141  T=2 F=12  T=1 F=66  case 0x05C1u: /* SHIN DOT */
  d=1   L 142  T=0 F=2  T=0 F=1  if (a == 0x05E9u) { /* SHIN */
  d=1   L 145  T=0 F=2  T=0 F=1  } else if (a == 0xFB49u) { /* SHIN WITH DAGESH */
  d=1   L 150  T=0 F=14  T=14 F=53  case 0x05C2u: /* SIN DOT */
  d=1   L 151  T=0 F=0  T=0 F=14  if (a == 0x05E9u) { /* SHIN */
  d=1   L 154  T=0 F=0  T=0 F=14  } else if (a == 0xFB49u) { /* SHIN WITH DAGESH */

[off-chain: 1 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=6b306d62da957568, size=59 bytes, fuzzer=naive, trial=1, discovered_at=636s, mutation_op=BytesSetMutator,BytesRandSetMutator):
  0000: ef 05 00 00 15 03 00 7a 68 2d 68 61 6e 74 2d 68   .......zh-hant-h
  0010: 74 00 00 00 27 03 00 00 ef 08 00 00 5e 03 00 00   t...'.......^...
  0020: 00 1a ff 05 00 00 00 00 cf e2 e6 15 00 15 80 00   ................
  0030: 00 00 08 00 00 15 06 00 00 00 10                  ...........
Seed 2 (id=daaa8a32d4fce5cb, size=119 bytes, fuzzer=value_profile, trial=1, discovered_at=2523s, mutation_op=BytesInsertMutator,TokenInsert,BytesCopyMutator,WordAddMutator,CrossoverInsertMutator):
  0000: 00 cd 1b 03 00 00 00 00 01 09 81 09 20 e0 17 9c   ............ ...
  0010: ff 49 92 24 09 7f df 05 00 00 4c 0e 00 00 4c 0e   .I.$......L...L.
  0020: 00 00 00 00 83 10 10 20 20 20 20 20 20 00 cd 1b   .......      ...
  0030: 03 00 00 00 00 01 09 81 09 20 cb 17 9c ff 49 92   ......... ....I.
Seed 3 (id=59f91776a173f489, size=133 bytes, fuzzer=naive, trial=1, discovered_at=2595s, mutation_op=BytesDeleteMutator,CrossoverInsertMutator,BytesRandInsertMutator):
  0000: a3 17 00 00 00 91 6a 04 76 03 03 f3 02 03 03 b0   ......j.v.......
  0010: 65 73 6d 63 46 46 46 4d 00 20 00 cb f3 00 00 00   esmcFFFM. ......
  0020: cc f2 00 cb 06 00 00 9a 06 00 00 4a f9 00 00 1a   ...........J....
  0030: 06 00 00 1f 1f 1f 1f 1f 1f 1f 1f 1f 1f 1f 1f 1f   ................
Seed 4 (id=d2f537251ba44f7c, size=49 bytes, fuzzer=naive, trial=1, discovered_at=14402s, mutation_op=BitFlipMutator,ByteInterestingMutator,BytesInsertCopyMutator,BytesDeleteMutator,ByteFlipMutator,TokenInsert):
  0000: ef 05 00 00 ea 7f 00 7a 68 2d 48 5b 6e 74 2d 68   .......zh-H[nt-h
  0010: 74 00 00 00 27 03 00 00 ef 08 00 68 74 00 00 00   t...'......ht...
  0020: 27 03 00 00 ef 08 00 00 70 6d 6a 76 5e 03 08 00   '.......pmjv^...
  0030: 00                                                .
Seed 5 (id=35ffb35dcf1a3710, size=46 bytes, fuzzer=naive, trial=1, discovered_at=21233s, mutation_op=BytesDeleteMutator,ByteNegMutator,BitFlipMutator,ByteIncMutator):
  0000: ef 05 00 00 ea 7f 00 7a 68 2d 48 5b 6e 74 2d 68   .......zh-H[nt-h
  0010: 74 00 00 00 27 03 00 00 ef 08 00 6c 74 00 00 00   t...'......lt...
  0020: 27 03 00 00 ef 08 00 00 70 6e 6a 76 5e 03         '.......pnjv^.

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=17e8cef306cf0609, size=12 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=124s, mutation_op=ByteIncMutator,TokenReplace,BytesDeleteMutator,BitFlipMutator):
  0000: 72 a4 ac ab 92 05 00 00 00 9b 01 00               r...........
Seed 2 (id=028c60a6bf99e5e5, size=90 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=637s, mutation_op=BitFlipMutator,BytesCopyMutator):
  0000: b2 b2 b2 b2 b2 b2 00 00 00 00 00 00 00 00 02 00   ................
  0010: 20 00 00 00 00 72 60 f1 f3 ff bf 05 00 00 ff bf    ....r`.........
  0020: 05 00 00 00 00 01 00 1e fa 67 76 5b 5b 5b 5b 5b   .........gv[[[[[
  0030: 5b 5b 5b 5b 5b 47 47 ff 08 00 05 72 20 f3 f3 f3   [[[[[GG....r ...
Seed 3 (id=0df913698e252353, size=18 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=805s, mutation_op=CrossoverInsertMutator,BytesRandSetMutator):
  0000: bf 05 00 00 bf 05 f1 f1 4a 0f 01 00 00 00 7c 7c   ........J.....||
  0010: 7c 00                                             |.
Seed 4 (id=27e1244b68be3ae8, size=69 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=817s, mutation_op=TokenReplace,DwordAddMutator,ByteDecMutator,BytesDeleteMutator):
  0000: 00 00 20 6a 04 00 6f 0b fe 00 19 1c 02 b1 05 00   .. j..o.........
  0010: 00 e3 10 01 00 b1 05 00 ff 6f 0a 73 72 75 62 00   .........o.srub.
  0020: 10 ff 20 10 72 61 66 63 06 06 65 04 00 ff d7 00   .. .rafc..e.....
  0030: 20 20 0c 01 00 06 06 65 04 00 ff d7 02 00 fb 10     .....e........
Seed 5 (id=35ff0eeb3ddbc06c, size=30 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1063s, mutation_op=QwordAddMutator,ByteInterestingMutator):
  0000: 16 00 1e fa 10 00 ab 05 01 02 00 9b 4f fa ff 20   ............O.. 
  0010: b8 05 00 00 00 9b 02 03 b7 05 00 00 b9 05         ..............


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  ef(.)x3 00(.)x2 a3(.)x1 a0(.)x1     00(.)x3 1b(.)x3 71(q)x2 72(r)x1 +11u  PARTIAL
   0x0002  00(.)x4 1b(.)x1 e0(.)x1 a0(.)x1     00(.)x4 06(.)x3 20( )x2 1e(.)x2 +8u  PARTIAL
   0x0003  00(.)x4 03(.)x1 ef(.)x1 a0(.)x1     00(.)x4 b9(.)x2 72(r)x2 ab(.)x1 +11u  PARTIAL
   0x0006  00(.)x5 6a(j)x1 01(.)x1             00(.)x7 71(q)x2 f1(.)x1 6f(o)x1 +9u  PARTIAL
   0x0011  00(.)x4 49(I)x1 73(s)x1 b6(.)x1     00(.)x5 05(.)x3 e3(.)x1 74(t)x1 +9u  PARTIAL
   0x0012  00(.)x4 92(.)x1 6d(m)x1 b6(.)x1     00(.)x7 03(.)x2 10(.)x1 74(t)x1 +7u  PARTIAL
   0x0013  00(.)x4 24($)x1 63(c)x1 b6(.)x1     00(.)x8 20( )x2 01(.)x1 74(t)x1 +6u  PARTIAL
   0x0016  00(.)x5 df(.)x1 46(F)x1             00(.)x7 71(q)x2 74(t)x2 60(`)x1 +6u  PARTIAL
   0x0017  00(.)x5 05(.)x1 4d(M)x1             00(.)x8 71(q)x2 61(a)x2 f1(.)x1 +5u  PARTIAL
   0x0018  00(.)x4 ef(.)x3                     00(.)x3 ff(.)x2 71(q)x2 f3(.)x1 +10u  PARTIAL
   0x001a  00(.)x4 4c(L)x1 7a(z)x1 03(.)x1     00(.)x5 05(.)x2 bf(.)x1 0a(.)x1 +8u  PARTIAL
   0x001d  00(.)x4 03(.)x1 7d(})x1 01(.)x1     00(.)x4 71(q)x4 05(.)x2 75(u)x1 +6u  PARTIAL
   0x001e  00(.)x4 4c(L)x1 31(1)x1 03(.)x1     71(q)x4 ff(.)x2 00(.)x2 62(b)x1 +7u  PARTIAL
   0x001f  00(.)x5 0e(.)x1 03(.)x1             00(.)x2 1e(.)x2 71(q)x2 bf(.)x1 +9u  PARTIAL
   0x0020  00(.)x4 27(')x2 cc(.)x1             00(.)x4 20( )x2 1e(.)x2 05(.)x1 +7u  PARTIAL
   0x0022  00(.)x4 ff(.)x1 31(1)x1 03(.)x1     00(.)x3 06(.)x2 71(q)x2 20( )x1 +8u  PARTIAL
   0x0023  00(.)x4 05(.)x1 cb(.)x1 0e(.)x1     00(.)x7 54(T)x2 71(q)x2 10(.)x1 +4u  PARTIAL
   0x0024  00(.)x3 ef(.)x2 83(.)x1 06(.)x1     00(.)x6 40(@)x2 71(q)x2 72(r)x1 +5u  PARTIAL
   0x0025  00(.)x4 08(.)x2 10(.)x1             05(.)x3 00(.)x3 55(U)x2 01(.)x1 +7u  PARTIAL
   0x0026  00(.)x4 10(.)x1 ff(.)x1 03(.)x1     00(.)x6 20( )x3 15(.)x2 66(f)x1 +4u  PARTIAL
   0x0027  00(.)x5 20( )x1 9a(.)x1             00(.)x4 1e(.)x1 63(c)x1 54(T)x1 +9u  PARTIAL
   0x002f  00(.)x3 1b(.)x1 1a(.)x1 03(.)x1     00(.)x4 71(q)x2 5b([)x1 82(.)x1 +7u  PARTIAL
   0x0030  00(.)x3 03(.)x1 06(.)x1 20( )x1     00(.)x5 5b([)x1 20( )x1 8f(.)x1 +7u  PARTIAL
   0x0031  00(.)x3 20( )x1 4d(M)x1             20( )x2 05(.)x2 00(.)x2 5b([)x1 +8u  PARTIAL
   0x0032  00(.)x2 08(.)x1 97(.)x1 03(.)x1     00(.)x3 71(q)x2 05(.)x2 5b([)x1 +7u  PARTIAL
   0x0033  00(.)x3 1f(.)x1 97(.)x1             00(.)x7 71(q)x2 5b([)x1 01(.)x1 +4u  PARTIAL
   0x0034  00(.)x3 1f(.)x1 69(i)x1             00(.)x6 71(q)x2 5b([)x1 03(.)x1 +5u  PARTIAL
   0x0037  00(.)x3 81(.)x1 1f(.)x1             00(.)x3 ff(.)x1 65(e)x1 06(.)x1 +7u  PARTIAL
   0x0038  00(.)x3 09(.)x1 1f(.)x1             00(.)x2 08(.)x1 04(.)x1 82(.)x1 +8u  PARTIAL
   0x003b  00(.)x2 17(.)x1 1f(.)x1             00(.)x5 20( )x2 72(r)x1 d7(.)x1 +4u  PARTIAL
   0x003c  00(.)x2 9c(.)x1 1f(.)x1             00(.)x3 1e(.)x2 20( )x1 02(.)x1 +6u  PARTIAL
   0x003d  ff(.)x1 1f(.)x1 7f(.)x1 00(.)x1     00(.)x4 c2(.)x2 f3(.)x1 01(.)x1 +5u  PARTIAL
   0x003e  49(I)x1 1f(.)x1 07(.)x1 03(.)x1     00(.)x4 05(.)x3 f3(.)x1 fb(.)x1 +4u  DIFFER
   0x003f  00(.)x2 92(.)x1 1f(.)x1             00(.)x6 10(.)x2 f3(.)x1 1e(.)x1 +3u  PARTIAL
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
  prompts_b/harfbuzz_5784.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5784,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5784 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5784 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5784 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).