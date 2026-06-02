==== BLOCKER ====
Target: libpng
Branch ID: 4031
Location: /src/libpng/pngrutil.c:2403:13
Enclosing function: OSS_FUZZ_png_handle_sCAL
Source line:    else if (length < 4)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=2.30h  loser=24.00h
  avg hitcount on branch: winner=18  loser=0
  prob_div=1.00  dur_div=21.70h  hit_div=18
  subject-level: delta_AUC=13087800.0  p_AUC=0.0002  delta_Final=135.8  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.70h  loser=24.00h
  avg hitcount on branch: winner=34  loser=0
  prob_div=0.90  dur_div=19.30h  hit_div=34
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/4031/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_sCAL (/src/libpng/pngrutil.c:2378-2465) ---
[ ]  2376  void /* PRIVATE */
[ ]  2377  png_handle_sCAL(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  2378  {
[B]  2379     png_bytep buffer;
[B]  2380     size_t i;
[B]  2381     int state;
[ ]  2382  
[B]  2383     png_debug(1, "in png_handle_sCAL");
[ ]  2384  
[B]  2385     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  2386        png_chunk_error(png_ptr, "missing IHDR");
[ ]  2387  
[B]  2388     else if ((png_ptr->mode & PNG_HAVE_IDAT) != 0)
[L]  2389     {
[L]  2390        png_crc_finish(png_ptr, length);
[L]  2391        png_chunk_benign_error(png_ptr, "out of place");
[L]  2392        return;
[L]  2393     }
[ ]  2394  
[B]  2395     else if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_sCAL) != 0)
[ ]  2396     {
[ ]  2397        png_crc_finish(png_ptr, length);
[ ]  2398        png_chunk_benign_error(png_ptr, "duplicate");
[ ]  2399        return;
[ ]  2400     }
[ ]  2401  
[ ]  2402     /* Need unit type, width, \0, height: minimum 4 bytes */
[B]  2403     else if (length < 4) <-- BLOCKER
[W]  2404     {
[W]  2405        png_crc_finish(png_ptr, length);
[W]  2406        png_chunk_benign_error(png_ptr, "invalid");
[W]  2407        return;
[W]  2408     }
[ ]  2409  
[B]  2410     png_debug1(2, "Allocating and reading sCAL chunk data (%u bytes)",
[B]  2411         length + 1);
[ ]  2412  
[B]  2413     buffer = png_read_buffer(png_ptr, length+1, 2/*silent*/);
[ ]  2414  
[B]  2415     if (buffer == NULL)
[ ]  2416     {
[ ]  2417        png_chunk_benign_error(png_ptr, "out of memory");
[ ]  2418        png_crc_finish(png_ptr, length);
[ ]  2419        return;
[ ]  2420     }
[ ]  2421  
[B]  2422     png_crc_read(png_ptr, buffer, length);
[B]  2423     buffer[length] = 0; /* Null terminate the last string */
[ ]  2424  
[B]  2425     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  2426        return;
[ ]  2427  
[ ]  2428     /* Validate the unit. */
[B]  2429     if (buffer[0] != 1 && buffer[0] != 2)
[B]  2430     {
[B]  2431        png_chunk_benign_error(png_ptr, "invalid unit");
[B]  2432        return;
[B]  2433     }
[ ]  2434  
[ ]  2435     /* Validate the ASCII numbers, need two ASCII numbers separated by
[ ]  2436      * a '\0' and they need to fit exactly in the chunk data.
[ ]  2437      */
[B]  2438     i = 1;
[B]  2439     state = 0;
[ ]  2440  
[B]  2441     if (png_check_fp_number((png_const_charp)buffer, length, &state, &i) == 0 ||
[B]  2442         i >= length || buffer[i++] != 0)
[B]  2443        png_chunk_benign_error(png_ptr, "bad width format");
[ ]  2444  
[L]  2445     else if (PNG_FP_IS_POSITIVE(state) == 0)
[ ]  2446        png_chunk_benign_error(png_ptr, "non-positive width");
[ ]  2447  
[L]  2448     else
[L]  2449     {
[L]  2450        size_t heighti = i;
[ ]  2451  
[L]  2452        state = 0;
[L]  2453        if (png_check_fp_number((png_const_charp)buffer, length,
[L]  2454            &state, &i) == 0 || i != length)
[L]  2455           png_chunk_benign_error(png_ptr, "bad height format");
[ ]  2456  
[L]  2457        else if (PNG_FP_IS_POSITIVE(state) == 0)
[ ]  2458           png_chunk_benign_error(png_ptr, "non-positive height");
[ ]  2459  
[L]  2460        else
[ ]  2461           /* This is the (only) success case. */
[L]  2462           png_set_sCAL_s(png_ptr, info_ptr, buffer[0],
[L]  2463               (png_charp)buffer+1, (png_charp)buffer+heighti);
[L]  2464     }
[B]  2465  }

--- No 1-hop callers of OSS_FUZZ_png_handle_sCAL fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0      5830  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
       2       810  OSS_FUZZ_png_zlib_inflate  (/src/libpng/pngrutil.c:454-467)
       0       784  OSS_FUZZ_png_read_IDAT_data  (/src/libpng/pngrutil.c:4152-4276)
       0       766  OSS_FUZZ_png_combine_row  (/src/libpng/pngrutil.c:3202-3681)
       0       764  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
       0       163  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
       0       154  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
      11        52  OSS_FUZZ_png_handle_unknown  (/src/libpng/pngrutil.c:2925-3120)
       2        20  OSS_FUZZ_png_handle_pHYs  (/src/libpng/pngrutil.c:2156-2196)
       0        18  OSS_FUZZ_png_read_start_row  (/src/libpng/pngrutil.c:4393-4680)
       2        19  pngrutil.c:png_inflate_claim  (/src/libpng/pngrutil.c:342-443)
      11         1  OSS_FUZZ_png_handle_iCCP  (/src/libpng/pngrutil.c:1363-1634)
       0        10  OSS_FUZZ_png_read_finish_IDAT  (/src/libpng/pngrutil.c:4280-4324)
       0         9  pngrutil.c:png_read_filter_row_sub  (/src/libpng/pngrutil.c:3934-3947)
       5         0  OSS_FUZZ_png_handle_sPLT  (/src/libpng/pngrutil.c:1641-1811)
... (6 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_sCAL  (/src/libpng/pngrutil.c:2378-2465) ---
  d=1   L2388  T=0 F=33  T=1 F=25  else if ((png_ptr->mode & PNG_HAVE_IDAT) != 0)
  d=1   L2403  T=18 F=15  T=0 F=25  else if (length < 4)  <-- BLOCKER
  d=1   L2429  T=4 F=0  T=1 F=0  if (buffer[0] != 1 && buffer[0] != 2)
  d=1   L2441  T=8 F=3  T=3 F=21  if (png_check_fp_number((png_const_charp)buffer, length, ...
  d=1   L2442  T=3 F=0  T=2 F=19  i >= length || buffer[i++] != 0)
  d=1   L2442  T=0 F=3  T=0 F=21  i >= length || buffer[i++] != 0)
  d=1   L2445  T=0 F=0  T=0 F=19  else if (PNG_FP_IS_POSITIVE(state) == 0)
  d=1   L2453  T=0 F=0  T=2 F=17  if (png_check_fp_number((png_const_charp)buffer, length,
  d=1   L2454  T=0 F=0  T=1 F=16  &state, &i) == 0 || i != length)
  d=1   L2457  T=0 F=0  T=0 F=16  else if (PNG_FP_IS_POSITIVE(state) == 0)

[off-chain: 294 additional divergent branches across 37 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=384ddb337e2d2818, size=8759 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1s, mutation_op=QwordAddMutator,BytesDeleteMutator,BytesRandInsertMutator,BytesRandSetMutator,ByteInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=34e4abf05f510261, size=8759 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5s, mutation_op=CrossoverInsertMutator,BytesRandInsertMutator,WordAddMutator,QwordAddMutator,BytesSwapMutator,BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=39c2113f02e12790, size=8759 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5s, mutation_op=CrossoverInsertMutator,BytesRandInsertMutator,WordAddMutator,QwordAddMutator,BytesSwapMutator,BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=049bb1d0ba1a05d4, size=6629 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=6s, mutation_op=BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=157d021b82dc9a66, size=6629 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=8s, mutation_op=TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00140bdb0aa48f31, size=2316 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator,CrossoverReplaceMutator,TokenInsert,DwordInterestingMutator,BytesExpandMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=024188c1a0b8a2c2, size=9727 bytes, fuzzer=value_profile, trial=1, discovered_at=15s, mutation_op=ByteNegMutator,ByteAddMutator,ByteNegMutator,BytesSetMutator,TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 10 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 3a 3a 3a   .....gAMA....:::
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
Seed 5 (id=021042b836a3f5aa, size=927 bytes, fuzzer=naive, trial=1, discovered_at=257s, mutation_op=ByteDecMutator,BytesSetMutator,ByteNegMutator,ByteFlipMutator,WordInterestingMutator,BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 00 00 02 04 00 00 00 01 00 00 aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x18                            00(.)x21 05(.)x1                    PARTIAL
   0x0013  5b([)x18                            5b([)x6 05(.)x2 51(Q)x2 21(!)x1 +11u  PARTIAL
   0x0016  00(.)x18                            00(.)x10 80(.)x5 a0(.)x4 a1(.)x2 +1u  PARTIAL
   0x0017  45(E)x18                            00(.)x6 86(.)x5 45(E)x4 01(.)x4 +3u  PARTIAL
   0x0018  08(.)x18                            08(.)x6 10(.)x5 04(.)x5 02(.)x3 +1u  PARTIAL
   0x0019  06(.)x18                            00(.)x14 06(.)x7 04(.)x1            PARTIAL
   0x001c  01(.)x13 00(.)x5                    01(.)x22                            PARTIAL
   0x001d  52(R)x18                            52(R)x14 00(.)x4 7f(.)x4            PARTIAL
   0x001e  ed(.)x18                            ed(.)x18 ff(.)x2 00(.)x2            PARTIAL
   0x0025  67(g)x15 69(i)x2 73(s)x1            67(g)x22                            PARTIAL
   0x0026  41(A)x15 54(T)x2 42(B)x1            41(A)x22                            PARTIAL
   0x0027  4d(M)x15 58(X)x2 49(I)x1            4d(M)x22                            PARTIAL
   0x0028  41(A)x15 74(t)x2 54(T)x1            41(A)x22                            PARTIAL
   0x0029  00(.)x15 03(.)x3                    00(.)x21 80(.)x1                    PARTIAL
   0x002b  b1(.)x15 00(.)x3                    b1(.)x21 b2(.)x1                    PARTIAL
   0x002c  8f(.)x15 00(.)x3                    8f(.)x22                            PARTIAL
   0x002d  0b(.)x18                            0b(.)x19 3a(:)x1 aa(.)x1 1b(.)x1    PARTIAL
   0x002e  fc(.)x18                            fc(.)x16 04(.)x4 3a(:)x1 56(V)x1    PARTIAL
   0x002f  61(a)x15 00(.)x3                    61(a)x20 3a(:)x1 aa(.)x1            PARTIAL
   0x0030  05(.)x17 00(.)x1                    05(.)x21 aa(.)x1                    PARTIAL
   0x0035  73(s)x16 74(t)x2                    73(s)x22                            PARTIAL
   0x0036  52(R)x12 43(C)x4 45(E)x2            52(R)x22                            PARTIAL
   0x0037  47(G)x12 41(A)x4 58(X)x2            47(G)x21 64(d)x1                    PARTIAL
   0x0038  42(B)x12 4c(L)x4 74(t)x2            42(B)x22                            PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_4031.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4031,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4031 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4031 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4031 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).