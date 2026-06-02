==== BLOCKER ====
Target: harfbuzz
Branch ID: 6253
Location: /src/harfbuzz/src/hb-ucd.cc:98:26
Enclosing function: hb-ucd.cc:_hb_ucd_compose_hangul(unsigned int, unsigned int, unsigned int*)
Source line:   else if (a >= LBASE && a < (LBASE + LCOUNT) && b >= VBASE && b < (VBASE + VCOUNT))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            9        1          0  winner (I2S vs cmplog)
cmplog                           2        8          0  loser (I2S vs naive)
value_profile                    9        1          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             1        9          0  loser (I2S vs value_profile)
naive_ctx                        8        2          0  REFERENCE
naive_ngram4                    10        0          0  REFERENCE
mopt                             8        2          0  REFERENCE
minimizer                        9        1          0  REFERENCE
fast                             9        1          0  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=10.00h  loser=21.90h
  avg hitcount on branch: winner=8  loser=0
  prob_div=0.80  dur_div=11.90h  hit_div=8
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=8.20h  loser=20.00h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.70  dur_div=11.80h  hit_div=5
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/6253/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ucd.cc:_hb_ucd_compose_hangul(unsigned int, unsigned int, unsigned int*) (/src/harfbuzz/src/hb-ucd.cc:90-108) ---
[ ]    88  static inline bool
[ ]    89  _hb_ucd_compose_hangul (hb_codepoint_t a, hb_codepoint_t b, hb_codepoint_t *ab)
[B]    90  {
[B]    91    if (a >= SBASE && a < (SBASE + SCOUNT) && b > TBASE && b < (TBASE + TCOUNT) &&
[B]    92      !((a - SBASE) % TCOUNT))
[ ]    93    {
[ ]    94      /* LV,T */
[ ]    95      *ab = a + (b - TBASE);
[ ]    96      return true;
[ ]    97    }
[B]    98    else if (a >= LBASE && a < (LBASE + LCOUNT) && b >= VBASE && b < (VBASE + VCOUNT)) <-- BLOCKER
[ ]    99    {
[ ]   100      /* L,V */
[ ]   101      int li = a - LBASE;
[ ]   102      int vi = b - VBASE;
[ ]   103      *ab = SBASE + li * NCOUNT + vi * TCOUNT;
[ ]   104      return true;
[ ]   105    }
[B]   106    else
[B]   107      return false;
[B]   108  }

--- Caller (1 hop): hb-ucd.cc:hb_ucd_compose(hb_unicode_funcs_t*, unsigned int, unsigned int, unsigned int*, void*) (/src/harfbuzz/src/hb-ucd.cc:131-168, calls hb-ucd.cc:_hb_ucd_compose_hangul(unsigned int, unsigned int, unsigned int*) at line 133) (full body — short) ---
[B]   131  {
[ ]   132    // Hangul is handled algorithmically.
[B]   133    if (_hb_ucd_compose_hangul (a, b, ab)) return true; <-- CALL
[ ]   134  
[B]   135    hb_codepoint_t u = 0;
[ ]   136  
[B]   137    if ((a & 0xFFFFF800u) == 0x0000u && (b & 0xFFFFFF80) == 0x0300u)
[L]   138    {
[ ]   139      /* If "a" is small enough and "b" is in the U+0300 range,
[ ]   140       * the composition data is encoded in a 32bit array sorted
[ ]   141       * by "a,b" pair. */
[L]   142      uint32_t k = HB_CODEPOINT_ENCODE3_11_7_14 (a, b, 0);
[L]   143      const uint32_t *v = hb_bsearch (k,
[L]   144  				    _hb_ucd_dm2_u32_map,
[L]   145  				    ARRAY_LENGTH (_hb_ucd_dm2_u32_map),
[L]   146  				    sizeof (*_hb_ucd_dm2_u32_map),
[L]   147  				    _cmp_pair_11_7_14);
[L]   148      if (likely (!v)) return false;
[ ]   149      u = HB_CODEPOINT_DECODE3_11_7_14_3 (*v);
[ ]   150    }
[B]   151    else
[B]   152    {
[ ]   153      /* Otherwise it is stored in a 64bit array sorted by
[ ]   154       * "a,b" pair. */
[B]   155      uint64_t k = HB_CODEPOINT_ENCODE3 (a, b, 0);
[B]   156      const uint64_t *v = hb_bsearch (k,
[B]   157  				    _hb_ucd_dm2_u64_map,
[B]   158  				    ARRAY_LENGTH (_hb_ucd_dm2_u64_map),
[B]   159  				    sizeof (*_hb_ucd_dm2_u64_map),
[B]   160  				    _cmp_pair);
[B]   161      if (likely (!v)) return false;
[ ]   162      u = HB_CODEPOINT_DECODE3_3 (*v);
[ ]   163    }
[ ]   164  
[ ]   165    if (unlikely (!u)) return false;
[ ]   166    *ab = u;
[ ]   167    return true;
[ ]   168  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ucd.cc:hb_ucd_compose(hb_unicode_funcs_t*, unsigned int, unsigned int, unsigned int*, void*)  (/src/harfbuzz/src/hb-ucd.cc:131-168, calls hb-ucd.cc:_hb_ucd_compose_hangul(unsigned int, unsigned int, unsigned int*) at line 133)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      30       140  hb-ucd.cc:hb_ucd_script(hb_unicode_funcs_t*, unsigned int, void*)  (/src/harfbuzz/src/hb-ucd.cc:51-53)
       0        18  hb-ucd.cc:_cmp_pair_11_7_14(void const*, void const*)  (/src/harfbuzz/src/hb-ucd.cc:120-125)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ucd.cc:hb_ucd_compose(hb_unicode_funcs_t*, unsigned int, unsigned int, unsigned int*, void*)  (/src/harfbuzz/src/hb-ucd.cc:131-168) ---
  d=2   L 137  T=0 F=3  T=2 F=0  if ((a & 0xFFFFF800u) == 0x0000u && (b & 0xFFFFFF80) == 0...
--- d=1  hb-ucd.cc:_hb_ucd_compose_hangul(unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ucd.cc:90-108) ---
  d=1   L  91  T=0 F=3  T=0 F=26  if (a >= SBASE && a < (SBASE + SCOUNT) && b > TBASE && b ...
  d=1   L  98  T=0 F=4  T=0 F=0  else if (a >= LBASE && a < (LBASE + LCOUNT) && b >= VBASE...  <-- BLOCKER
  d=1   L  98  T=14 F=7  T=0 F=27  else if (a >= LBASE && a < (LBASE + LCOUNT) && b >= VBASE...  <-- BLOCKER
  d=1   L  98  T=4 F=10  T=0 F=0  else if (a >= LBASE && a < (LBASE + LCOUNT) && b >= VBASE...  <-- BLOCKER

[off-chain: 2 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=fe82b82a7d81f868, size=64 bytes, fuzzer=value_profile, trial=2, discovered_at=28s, mutation_op=BitFlipMutator):
  0000: 8e 08 00 00 1b 20 20 a2 a2 a2 20 00 00 11 00 00   .....  ... .....
  0010: 00 09 00 00 00 00 00 80 00 00 00 00 00 00 00 00   ................
  0020: 00 00 00 00 fa 02 00 00 e0 e0 e0 8e 08 00 00 1b   ................
  0030: 20 20 a2 a2 a2 20 20 20 00 e3 38 fa 02 00 20 e0     ...   ..8... .
Seed 2 (id=1e6dcbc42bf19a8e, size=21 bytes, fuzzer=value_profile, trial=2, discovered_at=174s, mutation_op=BytesSetMutator,ByteIncMutator,ByteDecMutator,WordInterestingMutator,BytesExpandMutator,ByteFlipMutator,BytesInsertCopyMutator):
  0000: 0f 0a 00 00 10 11 00 00 ff 0a 00 00 0f 0a 00 00   ................
  0010: 10 ee 00 00 ff                                    .....
Seed 3 (id=3da425e9f406ebc9, size=101 bytes, fuzzer=value_profile, trial=2, discovered_at=381s, mutation_op=DwordInterestingMutator,ByteIncMutator,TokenInsert,BitFlipMutator):
  0000: 0a 00 00 01 00 0a 00 00 00 04 00 00 00 00 20 20   ..............  
  0010: 6a 6e 6e 6e 6e 6e 6e 6e 6e 6e 6b 5f 72 20 20 20   jnnnnnnnnnk_r   
  0020: 20 2c 00 00 00 1a 15 20 20 20 00 00 ff 0a 0a 00    ,.....   ......
  0030: 00 65 7a 69 73 00 00 00 00 00 ff 00 00 20 00 00   .ezis........ ..
Seed 4 (id=fc1a8c9b0c4d1262, size=119 bytes, fuzzer=naive, trial=1, discovered_at=2050s, mutation_op=BytesCopyMutator):
  0000: 2a 2a e6 96 6f 2d 00 00 00 01 20 20 ff fe ea 00   **..o-....  ....
  0010: 00 ff 73 00 00 d3 d3 d3 d3 d3 2a 2a 2a 2a 2a 2a   ..s.......******
  0020: 2a 2a e6 96 00 56 1c 00 20 5f 5f 5f 1b 1b 1b 1b   **...V.. ___....
  0030: 1b 1b 1b 1b 1b 1b 5f 10 0c 00 00 0c 20 00 00 00   ......_..... ...
Seed 5 (id=ee51b8803791162c, size=55 bytes, fuzzer=naive, trial=1, discovered_at=2958s, mutation_op=WordAddMutator):
  0000: 5b 00 00 00 00 18 00 00 00 0c 00 00 00 10 00 00   [...............
  0010: 00 0c 00 00 00 04 00 00 00 0c 00 00 00 11 00 00   ................
  0020: 00 0c 00 00 00 11 00 00 00 0c 00 00 00 0c 00 ff   ................
  0030: 63 41 6e 73 00 ff 7f                              cAns...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=007e652bc601c59b, size=38 bytes, fuzzer=cmplog, trial=1, discovered_at=21s, mutation_op=TokenInsert,QwordAddMutator,BytesDeleteMutator):
  0000: df 6b 66 20 72 8b 20 20 20 20 0a 01 8a 00 1a fb   .kf r.    ......
  0010: 00 0d 00 00 ef 01 00 72 6d 75 6e 00 01 0d 00 00   .......rmun.....
  0020: ef 01 00 0f e4 20                                 ..... 
Seed 2 (id=01b234577f5340e6, size=138 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=97s, mutation_op=BytesInsertCopyMutator,BitFlipMutator,ByteDecMutator,BytesInsertMutator):
  0000: 74 72 75 65 ff ff b9 b9 00 02 00 00 6a 79 2d 68   true........jy-h
  0010: 61 6e 73 02 00 20 20 24 21 00 18 6b 65 20 7f ff   ans..  $!..ke ..
  0020: ff 72 6e 20 00 1d 20 20 20 20 20 20 f1 f1 f1 f1   .rn ..      ....
  0030: f1 6e 20 7f ff ff ff 01 00 1a 20 20 20 20 00 00   .n .......    ..
Seed 3 (id=0097df216c0adf41, size=50 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=312s, mutation_op=ByteRandMutator,BytesSwapMutator):
  0000: 0a 0a 0a 0a 0a 0a 0a 0a e7 1c 00 00 1e e1 1e 1e   ................
  0010: e7 e7 e7 e7 e7 06 00 00 e8 06 00 00 00 03 e8 00   ................
  0020: 06 00 00 00 03 e8 00 42 ff 00 00 fb 00 0a 0a 49   .......B.......I
  0030: 40 ff                                             @.
Seed 4 (id=0112b2f715cadaf2, size=89 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=736s, mutation_op=BytesInsertMutator,ByteNegMutator,DwordInterestingMutator,BytesCopyMutator,ByteRandMutator):
  0000: 20 20 20 21 42 01 0e 00 1a 61 6b 2d 63 61 72 99      !B....ak-car.
  0010: 20 20 00 06 06 06 06 06 06 06 00 04 00 00 ff 00     ..............
  0020: 61 00 80 02 00 00 b9 7f ff ff 55 ff b9 b9 f0 0d   a.........U.....
  0030: 21 7a 5e 55 55 55 6a 65 72 06 00 00 00 06 00 00   !z^UUUjer.......
Seed 5 (id=00dcad947c9f5389, size=94 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=1113s, mutation_op=BytesExpandMutator,BytesSwapMutator,BytesInsertMutator,BytesRandSetMutator,BytesSetMutator,BytesExpandMutator,ByteNegMutator):
  0000: 00 61 63 00 00 00 00 00 00 00 00 00 6b 03 00 00   .ac.........k...
  0010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff f0   ................
  0020: 00 ff f0 f0 f0 00 1a 02 00 e8 06 00 05 00 00 b4   ................
  0030: 05 00 00 e7 fb 00 00 1d 03 00 00 e7 06 00 02 00   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0006  00(.)x9 20( )x1 10(.)x1             20( )x10 07(.)x2 b9(.)x1 0a(.)x1 +6u  PARTIAL
   0x000b  00(.)x9 20( )x1 0c(.)x1             20( )x14 00(.)x3 01(.)x1 2d(-)x1 +1u  PARTIAL
   0x000f  00(.)x9 20( )x1 17(.)x1             53(S)x5 42(B)x5 fb(.)x1 68(h)x1 +8u  PARTIAL
   0x0013  00(.)x10 6e(n)x1                    0d(.)x6 06(.)x4 00(.)x3 02(.)x1 +6u  PARTIAL
   0x0016  00(.)x6 10(.)x2 6e(n)x1 d3(.)x1     00(.)x16 20( )x1 06(.)x1 f0(.)x1 +1u  PARTIAL
   0x0017  00(.)x7 80(.)x1 6e(n)x1 d3(.)x1     10(.)x8 21(!)x4 00(.)x2 72(r)x1 +5u  PARTIAL
   0x001f  00(.)x7 20( )x1 2a(*)x1 40(@)x1     20( )x8 00(.)x5 03(.)x2 ff(.)x1 +4u  PARTIAL
   0x0022  00(.)x7 e6(.)x1 10(.)x1 0e(.)x1     00(.)x8 01(.)x4 32(2)x3 6e(n)x1 +4u  PARTIAL
   0x0023  00(.)x9 96(.)x1                     00(.)x6 32(2)x3 02(.)x2 07(.)x2 +7u  PARTIAL
   0x0027  00(.)x7 20( )x1 ff(.)x1             32(2)x5 00(.)x4 10(.)x2 20( )x1 +7u  PARTIAL
   0x002b  00(.)x7 8e(.)x1 5f(_)x1             32(2)x5 00(.)x3 10(.)x3 0c(.)x2 +6u  PARTIAL
   0x002f  00(.)x5 1b(.)x2 ff(.)x1 36(6)x1     00(.)x5 02(.)x3 03(.)x2 f1(.)x1 +8u  PARTIAL
   0x0039  00(.)x3 e3(.)x1 fe(.)x1 33(3)x1     00(.)x10 06(.)x2 1a(.)x1 01(.)x1 +4u  PARTIAL
   0x003b  00(.)x3 fa(.)x1 0c(.)x1             00(.)x6 14(.)x3 ff(.)x2 10(.)x2 +5u  PARTIAL
   0x003c  00(.)x2 02(.)x1 20( )x1 39(9)x1     00(.)x6 06(.)x2 20( )x1 0c(.)x1 +8u  PARTIAL
   0x003d  00(.)x3 20( )x1 8f(.)x1             00(.)x10 20( )x3 06(.)x1 02(.)x1 +3u  PARTIAL
   0x003e  00(.)x2 20( )x1 10(.)x1 ff(.)x1     00(.)x11 02(.)x1 72(r)x1 3f(?)x1 +4u  PARTIAL
   0x003f  00(.)x3 e0(.)x1 ff(.)x1             00(.)x6 20( )x4 b9(.)x1 dc(.)x1 +6u  PARTIAL
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
  prompts_b/harfbuzz_6253.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6253,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>value_profile_cmplog (I2S), naive>cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6253 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6253 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6253 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).