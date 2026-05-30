==== BLOCKER ====
Target: libpng
Branch ID: 3877
Location: /src/libpng/png.c:3355:21
Enclosing function: OSS_FUZZ_png_muldiv
Source line:       if (a == 0 || times == 0)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile)
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=6.30h  loser=21.80h
  avg hitcount on branch: winner=11  loser=0
  prob_div=0.70  dur_div=15.50h  hit_div=11
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.30h  loser=21.20h
  avg hitcount on branch: winner=7  loser=0
  prob_div=0.60  dur_div=13.90h  hit_div=6
  subject-level: delta_AUC=13087800.0  p_AUC=0.0002  delta_Final=135.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3877/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_muldiv (/src/libpng/png.c:3351-3461) ---
[ ]  3349  png_muldiv(png_fixed_point_p res, png_fixed_point a, png_int_32 times,
[ ]  3350      png_int_32 divisor)
[B]  3351  {
[ ]  3352     /* Return a * times / divisor, rounded. */
[B]  3353     if (divisor != 0)
[B]  3354     {
[B]  3355        if (a == 0 || times == 0) <-- BLOCKER
[B]  3356        {
[B]  3357           *res = 0;
[B]  3358           return 1;
[B]  3359        }
[B]  3360        else
[B]  3361        {
[B]  3362  #ifdef PNG_FLOATING_ARITHMETIC_SUPPORTED
[B]  3363           double r = a;
[B]  3364           r *= times;
[B]  3365           r /= divisor;
[B]  3366           r = floor(r+.5);
[ ]  3367  
[ ]  3368           /* A png_fixed_point is a 32-bit integer. */
[B]  3369           if (r <= 2147483647. && r >= -2147483648.)
[B]  3370           {
[B]  3371              *res = (png_fixed_point)r;
[B]  3372              return 1;
[B]  3373           }
[ ]  3374  #else
[ ]  3375           int negative = 0;
[ ]  3376           png_uint_32 A, T, D;
[ ]  3377           png_uint_32 s16, s32, s00;
[ ]  3378  
[ ]  3379           if (a < 0)
[ ]  3380              negative = 1, A = -a;
[ ]  3381           else
[ ]  3382              A = a;
[ ]  3383  
[ ]  3384           if (times < 0)
[ ]  3385              negative = !negative, T = -times;
[ ]  3386           else
[ ]  3387              T = times;
[ ]  3388  
[ ]  3389           if (divisor < 0)
[ ]  3390              negative = !negative, D = -divisor;
[ ]  3391           else
[ ]  3392              D = divisor;
[ ]  3393  
[ ]  3394           /* Following can't overflow because the arguments only
[ ]  3395            * have 31 bits each, however the result may be 32 bits.
[ ]  3396            */
[ ]  3397           s16 = (A >> 16) * (T & 0xffff) +
[ ]  3398                             (A & 0xffff) * (T >> 16);
[ ]  3399           /* Can't overflow because the a*times bit is only 30
[ ]  3400            * bits at most.
[ ]  3401            */
[ ]  3402           s32 = (A >> 16) * (T >> 16) + (s16 >> 16);
[ ]  3403           s00 = (A & 0xffff) * (T & 0xffff);
[ ]  3404  
[ ]  3405           s16 = (s16 & 0xffff) << 16;
[ ]  3406           s00 += s16;
[ ]  3407  
[ ]  3408           if (s00 < s16)
[ ]  3409              ++s32; /* carry */
[ ]  3410  
[ ]  3411           if (s32 < D) /* else overflow */
[ ]  3412           {
[ ]  3413              /* s32.s00 is now the 64-bit product, do a standard
[ ]  3414               * division, we know that s32 < D, so the maximum
[ ]  3415               * required shift is 31.
[ ]  3416               */
[ ]  3417              int bitshift = 32;
[ ]  3418              png_fixed_point result = 0; /* NOTE: signed */
[ ]  3419  
[ ]  3420              while (--bitshift >= 0)
[ ]  3421              {
[ ]  3422                 png_uint_32 d32, d00;
[ ]  3423  
[ ]  3424                 if (bitshift > 0)
[ ]  3425                    d32 = D >> (32-bitshift), d00 = D << bitshift;
[ ]  3426  
[ ]  3427                 else
[ ]  3428                    d32 = 0, d00 = D;
[ ]  3429  
[ ]  3430                 if (s32 > d32)
[ ]  3431                 {
[ ]  3432                    if (s00 < d00) --s32; /* carry */
[ ]  3433                    s32 -= d32, s00 -= d00, result += 1<<bitshift;
[ ]  3434                 }
[ ]  3435  
[ ]  3436                 else
[ ]  3437                    if (s32 == d32 && s00 >= d00)
[ ]  3438                       s32 = 0, s00 -= d00, result += 1<<bitshift;
[ ]  3439              }
[ ]  3440  
[ ]  3441              /* Handle the rounding. */
[ ]  3442              if (s00 >= (D >> 1))
[ ]  3443                 ++result;
[ ]  3444  
[ ]  3445              if (negative != 0)
[ ]  3446                 result = -result;
[ ]  3447  
[ ]  3448              /* Check for overflow. */
[ ]  3449              if ((negative != 0 && result <= 0) ||
[ ]  3450                  (negative == 0 && result >= 0))
[ ]  3451              {
[ ]  3452                 *res = result;
[ ]  3453                 return 1;
[ ]  3454              }
[ ]  3455           }
[ ]  3456  #endif
[B]  3457        }
[B]  3458     }
[ ]  3459  
[ ]  3460     return 0;
[B]  3461  }

--- No 1-hop callers of OSS_FUZZ_png_muldiv fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      19        85  OSS_FUZZ_png_check_fp_number  (/src/libpng/png.c:2714-2834)
      17        57  OSS_FUZZ_png_check_fp_string  (/src/libpng/png.c:2840-2849)
       7        26  OSS_FUZZ_png_zalloc  (/src/libpng/png.c:99-114)
       7        26  OSS_FUZZ_png_zfree  (/src/libpng/png.c:119-121)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_muldiv  (/src/libpng/png.c:3351-3461) ---
  d=1   L3355  T=28 F=282  T=0 F=313  if (a == 0 || times == 0)  <-- BLOCKER

[off-chain: 78 additional divergent branches across 12 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=132765c0e5023686, size=8759 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=0s, mutation_op=BytesSwapMutator,BytesExpandMutator,BytesCopyMutator,ByteInterestingMutator,ByteIncMutator,BytesExpandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=2f6df521f3df2458, size=8759 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1s, mutation_op=BytesInsertMutator,ByteRandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=11227dcdaa14dff7, size=5327 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=7s, mutation_op=BytesDeleteMutator,BytesExpandMutator,BytesExpandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=1d744dabe22024b4, size=8782 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=7s, mutation_op=TokenReplace,WordAddMutator,ByteFlipMutator,BytesSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 74 52 47 42 01 d9 c9 2c 7f 00 00   .....tRGB...,...
Seed 5 (id=157d021b82dc9a66, size=6629 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=8s, mutation_op=TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00793532ef09f446, size=269 bytes, fuzzer=value_profile, trial=1, discovered_at=14s, mutation_op=CrossoverReplaceMutator,ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 0f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 41 01 f5 c9 2c 7f 00 00   .....sRGA...,...
Seed 2 (id=009a34a8f7375590, size=2610 bytes, fuzzer=value_profile, trial=1, discovered_at=15s, mutation_op=DwordAddMutator,QwordAddMutator,CrossoverInsertMutator,BytesDeleteMutator,ByteInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=012870f9afb207c8, size=8759 bytes, fuzzer=value_profile, trial=1, discovered_at=65s, mutation_op=TokenReplace,ByteFlipMutator,WordInterestingMutator,ByteFlipMutator,ByteNegMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 01 08 06 00 00 01 52 ed aa   ...[.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=0165867d1e996ed7, size=1672 bytes, fuzzer=naive, trial=1, discovered_at=205s, mutation_op=ByteIncMutator,ByteAddMutator,BitFlipMutator,BytesRandSetMutator,ByteRandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 21 00 00 80 00 04 00 00 00 01 00 ff aa   ...!............
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=00c12f3d55212fd8, size=932 bytes, fuzzer=naive, trial=1, discovered_at=408s, mutation_op=QwordAddMutator,ByteInterestingMutator,BytesSetMutator,ByteIncMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 55 00 00 a0 86 10 00 00 00 01 7f ed aa   ...U............
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x21                            00(.)x19 05(.)x1                    PARTIAL
   0x0013  5b([)x21                            5b([)x7 20( )x2 51(Q)x2 21(!)x1 +8u  PARTIAL
   0x0016  00(.)x21                            00(.)x8 80(.)x5 a0(.)x5 a1(.)x2     PARTIAL
   0x0017  45(E)x21                            00(.)x6 86(.)x6 45(E)x5 01(.)x2 +1u  PARTIAL
   0x0018  08(.)x21                            08(.)x7 04(.)x5 10(.)x3 02(.)x3 +1u  PARTIAL
   0x0019  06(.)x21                            00(.)x12 06(.)x6 04(.)x2            PARTIAL
   0x001d  52(R)x21                            52(R)x12 00(.)x4 7f(.)x3 ff(.)x1    PARTIAL
   0x001e  ed(.)x21                            ed(.)x16 ff(.)x3 00(.)x1            PARTIAL
   0x0025  67(g)x16 69(i)x3 74(t)x2            67(g)x20                            PARTIAL
   0x0026  41(A)x16 54(T)x3 49(I)x2            41(A)x20                            PARTIAL
   0x0027  4d(M)x18 58(X)x3                    4d(M)x20                            PARTIAL
   0x0028  41(A)x16 74(t)x3 45(E)x2            41(A)x20                            PARTIAL
   0x002c  8f(.)x21                            8f(.)x19 0f(.)x1                    PARTIAL
   0x002d  0b(.)x21                            0b(.)x19 aa(.)x1                    PARTIAL
   0x002e  fc(.)x21                            fc(.)x15 04(.)x4 56(V)x1            PARTIAL
   0x002f  61(a)x16 00(.)x5                    61(a)x19 aa(.)x1                    PARTIAL
   0x0030  05(.)x21                            05(.)x19 aa(.)x1                    PARTIAL
   0x0035  73(s)x13 74(t)x7 63(c)x1            73(s)x20                            PARTIAL
   0x0036  52(R)x13 45(E)x4 50(P)x2 48(H)x1 +1u  52(R)x20                            PARTIAL
   0x0037  47(G)x12 58(X)x4 4c(L)x2 4e(N)x1 +2u  47(G)x20                            PARTIAL
   0x0038  42(B)x12 74(t)x4 54(T)x2 53(S)x1 +2u  42(B)x19 41(A)x1                    PARTIAL
   0x003a  d9(.)x21                            d9(.)x19 f5(.)x1                    PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3877.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3877,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3877 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3877 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3877 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).