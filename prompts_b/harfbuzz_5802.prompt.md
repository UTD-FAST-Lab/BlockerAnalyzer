==== BLOCKER ====
Target: harfbuzz
Branch ID: 5802
Location: /src/harfbuzz/src/hb-ot-shaper-hebrew.cc:151:8
Enclosing function: hb-ot-shaper-hebrew.cc:compose_hebrew(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)
Source line: 	  if (a == 0x05E9u) { /* SHIN */
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            8        2          0  winner (I2S vs cmplog); winner (ctx_coverage vs naive_ctx)
cmplog                           0       10          0  loser (I2S vs naive)
value_profile                    4        6          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        1        9          0  loser (ctx_coverage vs naive)
naive_ngram4                     4        6          0  REFERENCE
mopt                             4        6          0  REFERENCE
minimizer                        8        2          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=12.30h  loser=19.90h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=7.60h  hit_div=4
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: naive > naive_ctx  [delta: ctx_coverage] ---
  subject 15  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=12.30h  loser=19.90h
  avg hitcount on branch: winner=4  loser=2
  prob_div=0.70  dur_div=7.60h  hit_div=2
  subject-level: delta_AUC=15634800.0  p_AUC=0.0003  delta_Final=258.3  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5802/{W,L}/branch_coverage_show.txt

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
[B]    81    if (!found && !c->plan->has_gpos_mark)
[B]    82    {
[ ]    83        /* Special-case Hebrew presentation forms that are excluded from
[ ]    84         * standard normalization, but wanted for old fonts. */
[B]    85        switch (b) {
[L]    86        case 0x05B4u: /* HIRIQ */
[L]    87  	  if (a == 0x05D9u) { /* YOD */
[ ]    88  	      *ab = 0xFB1Du;
[ ]    89  	      found = true;
[ ]    90  	  }
[L]    91  	  break;
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
[L]   141        case 0x05C1u: /* SHIN DOT */
[L]   142  	  if (a == 0x05E9u) { /* SHIN */
[ ]   143  	      *ab = 0xFB2Au;
[ ]   144  	      found = true;
[L]   145  	  } else if (a == 0xFB49u) { /* SHIN WITH DAGESH */
[ ]   146  	      *ab = 0xFB2Cu;
[ ]   147  	      found = true;
[ ]   148  	  }
[L]   149  	  break;
[B]   150        case 0x05C2u: /* SIN DOT */
[B]   151  	  if (a == 0x05E9u) { /* SHIN */ <-- BLOCKER
[W]   152  	      *ab = 0xFB2Bu;
[W]   153  	      found = true;
[B]   154  	  } else if (a == 0xFB49u) { /* SHIN WITH DAGESH */
[ ]   155  	      *ab = 0xFB2Du;
[ ]   156  	      found = true;
[ ]   157  	  }
[B]   158  	  break;
[B]   159        }
[B]   160    }
[ ]   161  
[B]   162    return found;
[B]   163  }

--- No 1-hop callers of hb-ot-shaper-hebrew.cc:compose_hebrew(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       8       106  hb-ot-shaper-hebrew.cc:compose_hebrew(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-hebrew.cc:39-163)  <-- enclosing
       9        76  hb-ot-shaper-hebrew.cc:reorder_marks_hebrew(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-hebrew.cc:170-190)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-hebrew.cc:compose_hebrew(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-hebrew.cc:39-163) ---
  d=1   L  81  T=8 F=0  T=105 F=0  if (!found && !c->plan->has_gpos_mark)
  d=1   L  81  T=8 F=0  T=105 F=1  if (!found && !c->plan->has_gpos_mark)
  d=1   L  85  T=1 F=7  T=43 F=62  switch (b) {
  d=1   L  86  T=0 F=8  T=1 F=104  case 0x05B4u: /* HIRIQ */
  d=1   L  87  T=0 F=0  T=0 F=1  if (a == 0x05D9u) { /* YOD */
  d=1   L  92  T=0 F=8  T=3 F=102  case 0x05B7u: /* PATAH */
  d=1   L  93  T=0 F=0  T=0 F=3  if (a == 0x05F2u) { /* YIDDISH YOD YOD */
  d=1   L  96  T=0 F=0  T=0 F=3  } else if (a == 0x05D0u) { /* ALEF */
  d=1   L 101  T=0 F=8  T=3 F=102  case 0x05B8u: /* QAMATS */
  d=1   L 102  T=0 F=0  T=0 F=3  if (a == 0x05D0u) { /* ALEF */
  d=1   L 107  T=0 F=8  T=4 F=101  case 0x05B9u: /* HOLAM */
  d=1   L 108  T=0 F=0  T=0 F=4  if (a == 0x05D5u) { /* VAV */
  d=1   L 113  T=0 F=8  T=3 F=102  case 0x05BCu: /* DAGESH */
  d=1   L 114  T=0 F=0  T=0 F=2  if (a >= 0x05D0u && a <= 0x05EAu) {
  d=1   L 114  T=0 F=0  T=2 F=1  if (a >= 0x05D0u && a <= 0x05EAu) {
  d=1   L 117  T=0 F=0  T=0 F=3  } else if (a == 0xFB2Au) { /* SHIN WITH SHIN DOT */
  d=1   L 120  T=0 F=0  T=0 F=3  } else if (a == 0xFB2Bu) { /* SHIN WITH SIN DOT */
  d=1   L 125  T=0 F=8  T=1 F=104  case 0x05BFu: /* RAFE */
  d=1   L 126  T=0 F=0  T=1 F=0  switch (a) {
  d=1   L 127  T=0 F=0  T=0 F=1  case 0x05D1u: /* BET */
  d=1   L 131  T=0 F=0  T=0 F=1  case 0x05DBu: /* KAF */
  d=1   L 135  T=0 F=0  T=0 F=1  case 0x05E4u: /* PE */
  d=1   L 141  T=0 F=8  T=1 F=104  case 0x05C1u: /* SHIN DOT */
  d=1   L 142  T=0 F=0  T=0 F=1  if (a == 0x05E9u) { /* SHIN */
  d=1   L 145  T=0 F=0  T=0 F=1  } else if (a == 0xFB49u) { /* SHIN WITH DAGESH */
  d=1   L 150  T=7 F=1  T=46 F=59  case 0x05C2u: /* SIN DOT */
  d=1   L 151  T=6 F=1  T=0 F=46  if (a == 0x05E9u) { /* SHIN */  <-- BLOCKER
  d=1   L 154  T=0 F=1  T=0 F=46  } else if (a == 0xFB49u) { /* SHIN WITH DAGESH */

[off-chain: 3 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d87fc4e9b56007ec, size=27 bytes, fuzzer=minimizer, trial=1, discovered_at=3348s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,BytesRandSetMutator,ByteFlipMutator,BytesDeleteMutator,BytesRandInsertMutator):
  0000: 23 cc cc cc cc e9 e9 e9 e9 e9 e9 e9 e9 05 00 00   #...............
  0010: c2 05 00 00 00 1b 00 00 00 03 00                  ...........
Seed 2 (id=655389a0b7b0bad2, size=47 bytes, fuzzer=minimizer, trial=1, discovered_at=22972s, mutation_op=TokenReplace,BytesDeleteMutator,DwordInterestingMutator,WordInterestingMutator):
  0000: c2 05 00 00 01 00 00 00 c2 05 00 00 00 1b 00 00   ................
  0010: 23 e5 e5 e5 e9 05 00 00 c2 05 00 00 e9 05 00 00   #...............
  0020: c2 05 00 00 00 1b 00 00 23 e5 e5 e5 00 4c 1b      ........#....L.
Seed 3 (id=646d1363a65d6f7d, size=131 bytes, fuzzer=naive, trial=3, discovered_at=71121s, mutation_op=BytesCopyMutator,TokenInsert,DwordAddMutator,ByteRandMutator,BytesCopyMutator):
  0000: 00 89 1c 07 00 00 00 15 00 00 00 0c 00 00 00 00   ................
  0010: 00 00 13 ab ff 7f ff ff 63 73 64 76 e1 00 00 28   ........csdv...(
  0020: 00 00 ff 00 40 00 00 00 a9 00 00 00 f3 00 a4 00   ....@...........
  0030: 00 00 ff ff b7 05 b0 0f a3 e9 e9 e9 e9 e9 fe 7f   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=26969e225b57dbd6, size=61 bytes, fuzzer=naive_ctx, trial=1, discovered_at=51s, mutation_op=ByteInterestingMutator,ByteFlipMutator,TokenInsert,QwordAddMutator,CrossoverReplaceMutator,BytesRandSetMutator):
  0000: 00 01 00 96 00 00 90 fa 08 c2 c2 c2 c2 00 fc ff   ................
  0010: 7e 00 00 ff 00 00 00 01 f4 0b c2 40 c2 05 00 00   ~..........@....
  0020: c2 c2 40 01 00 01 20 80 96 00 00 80 00 96 96 51   ..@... ........Q
  0030: 51 51 51 51 51 51 51 51 00 03 00 00 20            QQQQQQQQ.... 
Seed 2 (id=deda932d40fe798c, size=65 bytes, fuzzer=cmplog, trial=1, discovered_at=634s, mutation_op=BytesSetMutator):
  0000: b9 b9 c4 b9 b9 b9 b4 b4 b4 b4 a3 b9 f9 b9 05 04   ................
  0010: 00 c2 05 00 00 00 20 00 00 03 03 ff ff ff 03 01   ...... .........
  0020: 00 03 03 00 00 03 00 00 00 03 0c 01 00 80 00 ff   ................
  0030: 03 02 00 00 03 08 00 00 00 00 ff 03 00 24 21 0f   .............$!.
Seed 3 (id=2050675b271d7fa7, size=87 bytes, fuzzer=cmplog, trial=1, discovered_at=736s, mutation_op=BytesRandSetMutator):
  0000: 03 02 00 00 ff ff ff 03 00 24 21 10 00 20 20 20   .........$!..   
  0010: 02 00 b9 b9 b9 b9 b9 b9 05 7f 02 00 00 00 00 0a   ................
  0020: 00 00 00 00 00 ae ae b9 00 00 ff 00 ff ff ff 74   ...............t
  0030: 72 75 65 c2 05 00 00 00 fe 00 00 00 00 05 ff 00   rue.............
Seed 4 (id=7f55b0a951b22764, size=94 bytes, fuzzer=cmplog, trial=1, discovered_at=1082s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator,ByteFlipMutator,BytesSetMutator):
  0000: b9 b9 64 6f 2d 68 61 6e 74 2d 6d 6f 00 66 63 05   ..do-hant-mo.fc.
  0010: 04 04 00 03 00 00 20 03 00 00 00 03 00 00 b4 05   ...... .........
  0020: 00 00 00 03 00 00 b9 05 04 00 00 00 00 08 c2 05   ................
  0030: 00 00 20 03 0c 00 b9 05 00 00 00 03 10 00 b4 05   .. .............
Seed 5 (id=d4146b2f02ced40d, size=83 bytes, fuzzer=cmplog, trial=1, discovered_at=1164s, mutation_op=ByteNegMutator,BytesInsertCopyMutator):
  0000: 40 20 fe 00 07 b9 02 00 00 00 03 00 00 c2 05 b9   @ ..............
  0010: 02 00 00 00 03 00 00 c2 05 00 00 c2 05 00 00 c2   ................
  0020: 05 00 00 00 00 00 00 00 03 00 00 00 00 00 01 00   ................
  0030: 03 00 80 00 10 00 80 01 01 01 01 01 01 01 01 01   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  23(#)x1 c2(.)x1 00(.)x1             00(.)x10 b9(.)x6 40(@)x2 03(.)x1 +9u  PARTIAL
   0x0001  cc(.)x1 05(.)x1 89(.)x1             b9(.)x4 00(.)x3 01(.)x2 20( )x2 +15u  PARTIAL
   0x0002  cc(.)x1 00(.)x1 1c(.)x1             00(.)x9 66(f)x3 01(.)x2 04(.)x2 +12u  PARTIAL
   0x0003  cc(.)x1 00(.)x1 07(.)x1             00(.)x16 63(c)x2 96(.)x1 b9(.)x1 +8u  PARTIAL
   0x0004  cc(.)x1 01(.)x1 00(.)x1             00(.)x7 c2(.)x4 07(.)x3 ff(.)x2 +11u  PARTIAL
   0x0005  00(.)x2 e9(.)x1                     00(.)x5 05(.)x4 c2(.)x4 b9(.)x3 +12u  PARTIAL
   0x0006  00(.)x2 e9(.)x1                     00(.)x5 b4(.)x2 ff(.)x2 02(.)x2 +14u  PARTIAL
   0x0007  e9(.)x1 00(.)x1 15(.)x1             00(.)x11 b4(.)x2 03(.)x2 20( )x2 +10u  PARTIAL
   0x0008  e9(.)x1 c2(.)x1 00(.)x1             00(.)x8 20( )x3 b4(.)x2 05(.)x2 +11u  PARTIAL
   0x0009  e9(.)x1 05(.)x1 00(.)x1             00(.)x7 05(.)x4 c2(.)x3 b4(.)x2 +11u  PARTIAL
   0x000a  00(.)x2 e9(.)x1                     00(.)x9 03(.)x3 c2(.)x2 05(.)x2 +12u  PARTIAL
   0x000b  e9(.)x1 00(.)x1 0c(.)x1             00(.)x12 b9(.)x3 c2(.)x2 20( )x2 +9u  PARTIAL
   0x000c  00(.)x2 e9(.)x1                     00(.)x12 c2(.)x2 f9(.)x1 b9(.)x1 +12u  PARTIAL
   0x000d  05(.)x1 1b(.)x1 00(.)x1             00(.)x7 c2(.)x3 b9(.)x2 20( )x2 +14u  PARTIAL
   0x000e  00(.)x3                             00(.)x6 05(.)x4 20( )x2 72(r)x2 +14u  PARTIAL
   0x000f  00(.)x3                             00(.)x9 61(a)x2 6e(n)x2 ff(.)x1 +14u  PARTIAL
   0x0010  c2(.)x1 23(#)x1 00(.)x1             00(.)x7 c2(.)x3 02(.)x2 20( )x2 +14u  PARTIAL
   0x0011  05(.)x1 e5(.)x1 00(.)x1             00(.)x7 05(.)x5 c2(.)x3 04(.)x1 +12u  PARTIAL
   0x0012  00(.)x1 e5(.)x1 13(.)x1             00(.)x15 05(.)x3 1a(.)x2 2d(-)x2 +6u  PARTIAL
   0x0013  00(.)x1 e5(.)x1 ab(.)x1             00(.)x15 ff(.)x2 b9(.)x1 03(.)x1 +9u  PARTIAL
   0x0014  00(.)x1 e9(.)x1 ff(.)x1             00(.)x10 c2(.)x2 b6(.)x2 6f(o)x2 +12u  PARTIAL
   0x0015  1b(.)x1 05(.)x1 7f(.)x1             00(.)x12 05(.)x5 a7(.)x2 b9(.)x1 +8u  PARTIAL
   0x0016  00(.)x2 ff(.)x1                     00(.)x12 20( )x3 1a(.)x2 a7(.)x2 +9u  PARTIAL
   0x0017  00(.)x2 ff(.)x1                     00(.)x13 1a(.)x2 ff(.)x2 01(.)x1 +10u  PARTIAL
   0x0018  00(.)x1 c2(.)x1 63(c)x1             00(.)x10 05(.)x2 20( )x2 f4(.)x1 +13u  PARTIAL
   0x0019  03(.)x1 05(.)x1 73(s)x1             00(.)x10 7f(.)x2 05(.)x2 0b(.)x1 +13u  PARTIAL
   0x001a  00(.)x2 64(d)x1                     00(.)x8 05(.)x3 20( )x2 c2(.)x1 +14u  PARTIAL
   0x001b  00(.)x1 76(v)x1                     00(.)x13 c2(.)x3 ff(.)x2 20( )x2 +8u  PARTIAL
   0x001c  e9(.)x1 e1(.)x1                     00(.)x14 c2(.)x3 ff(.)x2 05(.)x1 +8u  DIFFER
   0x001d  05(.)x1 00(.)x1                     00(.)x12 05(.)x5 ff(.)x1 03(.)x1 +9u  PARTIAL
   0x001e  00(.)x2                             00(.)x14 05(.)x2 03(.)x1 b4(.)x1 +10u  PARTIAL
   0x001f  00(.)x1 28(()x1                     00(.)x12 01(.)x4 0a(.)x2 05(.)x1 +9u  PARTIAL
   0x0020  c2(.)x1 00(.)x1                     00(.)x13 b6(.)x3 c2(.)x2 05(.)x2 +8u  PARTIAL
   0x0021  05(.)x1 00(.)x1                     00(.)x11 05(.)x4 1a(.)x2 c2(.)x1 +10u  PARTIAL
   0x0022  00(.)x1 ff(.)x1                     00(.)x10 03(.)x2 60(`)x2 05(.)x2 +12u  PARTIAL
   0x0023  00(.)x2                             00(.)x13 ff(.)x3 aa(.)x3 01(.)x2 +6u  PARTIAL
   0x0024  00(.)x1 40(@)x1                     00(.)x17 1a(.)x2 1c(.)x1 20( )x1 +7u  PARTIAL
   0x0025  1b(.)x1 00(.)x1                     00(.)x10 03(.)x3 c2(.)x2 20( )x2 +10u  PARTIAL
   0x0026  00(.)x2                             00(.)x7 20( )x3 05(.)x3 1a(.)x2 +13u  PARTIAL
   0x0027  00(.)x2                             00(.)x12 20( )x3 05(.)x2 0b(.)x2 +8u  PARTIAL
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5802.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5802,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), naive>naive_ctx (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5802 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5802 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5802 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).