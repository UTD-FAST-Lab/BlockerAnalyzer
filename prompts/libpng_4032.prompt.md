==== BLOCKER ====
Target: libpng
Branch ID: 4032
Location: /src/libpng/pngrutil.c:2415:8
Enclosing function: OSS_FUZZ_png_handle_sCAL
Source line:    if (buffer == NULL)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (ctx_coverage vs naive_ctx)
cmplog                           2        8          0  REFERENCE
value_profile                    1        9          0  REFERENCE
value_profile_cmplog             2        8          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     3        7          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 25  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.30h  loser=23.70h
  avg hitcount on branch: winner=14  loser=0
  prob_div=0.90  dur_div=23.40h  hit_div=14
  subject-level: delta_AUC=6413040.0  p_AUC=0.0003  delta_Final=91.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/4032/{W,L}/branch_coverage_show.txt

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
[B]  2403     else if (length < 4)
[ ]  2404     {
[ ]  2405        png_crc_finish(png_ptr, length);
[ ]  2406        png_chunk_benign_error(png_ptr, "invalid");
[ ]  2407        return;
[ ]  2408     }
[ ]  2409  
[B]  2410     png_debug1(2, "Allocating and reading sCAL chunk data (%u bytes)",
[B]  2411         length + 1);
[ ]  2412  
[B]  2413     buffer = png_read_buffer(png_ptr, length+1, 2/*silent*/);
[ ]  2414  
[B]  2415     if (buffer == NULL) <-- BLOCKER
[W]  2416     {
[W]  2417        png_chunk_benign_error(png_ptr, "out of memory");
[W]  2418        png_crc_finish(png_ptr, length);
[W]  2419        return;
[W]  2420     }
[ ]  2421  
[B]  2422     png_crc_read(png_ptr, buffer, length);
[B]  2423     buffer[length] = 0; /* Null terminate the last string */
[ ]  2424  
[B]  2425     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  2426        return;
[ ]  2427  
[ ]  2428     /* Validate the unit. */
[B]  2429     if (buffer[0] != 1 && buffer[0] != 2)
[L]  2430     {
[L]  2431        png_chunk_benign_error(png_ptr, "invalid unit");
[L]  2432        return;
[L]  2433     }
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
[ ]  2455           png_chunk_benign_error(png_ptr, "bad height format");
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
       0      1970  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
       0       265  OSS_FUZZ_png_read_IDAT_data  (/src/libpng/pngrutil.c:4152-4276)
       0       257  OSS_FUZZ_png_combine_row  (/src/libpng/pngrutil.c:3202-3681)
       9       265  OSS_FUZZ_png_zlib_inflate  (/src/libpng/pngrutil.c:454-467)
       0       255  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
     209        26  pngrutil.c:png_get_fixed_point  (/src/libpng/pngrutil.c:42-53)
       0       160  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
       0       153  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
      52        14  OSS_FUZZ_png_handle_unknown  (/src/libpng/pngrutil.c:2925-3120)
      29         0  OSS_FUZZ_png_handle_sPLT  (/src/libpng/pngrutil.c:1641-1811)
      32         6  OSS_FUZZ_png_handle_bKGD  (/src/libpng/pngrutil.c:1921-2033)
      24         6  OSS_FUZZ_png_handle_cHRM  (/src/libpng/pngrutil.c:1240-1306)
      16         4  OSS_FUZZ_png_handle_oFFs  (/src/libpng/pngrutil.c:2202-2242)
       0        10  OSS_FUZZ_png_handle_tIME  (/src/libpng/pngrutil.c:2471-2510)
       0        10  OSS_FUZZ_png_handle_tEXt  (/src/libpng/pngrutil.c:2517-2591)
... (8 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_sCAL  (/src/libpng/pngrutil.c:2378-2465) ---
  d=1   L2388  T=0 F=12  T=1 F=12  else if ((png_ptr->mode & PNG_HAVE_IDAT) != 0)
  d=1   L2415  T=11 F=1  T=0 F=12  if (buffer == NULL)  <-- BLOCKER
  d=1   L2425  T=0 F=1  T=0 F=12  if (png_crc_finish(png_ptr, 0) != 0)
  d=1   L2429  T=0 F=1  T=1 F=11  if (buffer[0] != 1 && buffer[0] != 2)
  d=1   L2429  T=0 F=0  T=1 F=0  if (buffer[0] != 1 && buffer[0] != 2)
  d=1   L2441  T=0 F=1  T=2 F=9  if (png_check_fp_number((png_const_charp)buffer, length, ...
  d=1   L2442  T=1 F=0  T=0 F=9  i >= length || buffer[i++] != 0)
  d=1   L2442  T=0 F=1  T=0 F=9  i >= length || buffer[i++] != 0)
  d=1   L2445  T=0 F=0  T=0 F=9  else if (PNG_FP_IS_POSITIVE(state) == 0)
  d=1   L2453  T=0 F=0  T=0 F=9  if (png_check_fp_number((png_const_charp)buffer, length,
  d=1   L2454  T=0 F=0  T=0 F=9  &state, &i) == 0 || i != length)
  d=1   L2457  T=0 F=0  T=0 F=9  else if (PNG_FP_IS_POSITIVE(state) == 0)

[off-chain: 263 additional divergent branches across 35 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=035b8411b522b74b, size=937 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=078f47cb6ea3e323, size=10501 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=09b0e4d8532d2f86, size=824 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 10 00 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=0b010d7ee810e3c4, size=1338 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 00 ff ed aa   ...[...E........
  0020: e4 00 00 00 04 67 41 4c 41 00 00 b1 8f 0b fc 61   .....gALA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=117667d1909fb467, size=777 bytes, fuzzer=naive_ctx, trial=1):
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
Seed 2 (id=0165867d1e996ed7, size=1672 bytes, fuzzer=naive, trial=1, discovered_at=205s, mutation_op=ByteIncMutator,ByteAddMutator,BitFlipMutator,BytesRandSetMutator,ByteRandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 21 00 00 80 00 04 00 00 00 01 00 ff aa   ...!............
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=021042b836a3f5aa, size=927 bytes, fuzzer=naive, trial=1, discovered_at=257s, mutation_op=ByteDecMutator,BytesSetMutator,ByteNegMutator,ByteFlipMutator,WordInterestingMutator,BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 00 00 02 04 00 00 00 01 00 00 aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=00c12f3d55212fd8, size=932 bytes, fuzzer=naive, trial=1, discovered_at=408s, mutation_op=QwordAddMutator,ByteInterestingMutator,BytesSetMutator,ByteIncMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 55 00 00 a0 86 10 00 00 00 01 7f ed aa   ...U............
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=00a0761917250025, size=768 bytes, fuzzer=naive, trial=1, discovered_at=1159s, mutation_op=DwordAddMutator,TokenReplace,BytesInsertCopyMutator,BytesRandInsertMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 05 0a 00 00 80 00 02 00 00 00 01 00 ff aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x11                            00(.)x9 05(.)x1                     PARTIAL
   0x0013  5b([)x11                            5b([)x2 05(.)x2 21(!)x1 55(U)x1 +4u  PARTIAL
   0x0016  00(.)x11                            00(.)x4 a0(.)x4 80(.)x2             PARTIAL
   0x0017  45(E)x11                            00(.)x3 86(.)x3 45(E)x1 02(.)x1 +2u  PARTIAL
   0x0018  08(.)x8 10(.)x3                     04(.)x3 10(.)x3 01(.)x2 08(.)x1 +1u  PARTIAL
   0x0019  06(.)x8 00(.)x3                     00(.)x8 06(.)x1 04(.)x1             PARTIAL
   0x001c  01(.)x10 00(.)x1                    01(.)x10                            PARTIAL
   0x001d  52(R)x10 ff(.)x1                    00(.)x4 7f(.)x4 52(R)x2             PARTIAL
   0x001e  ed(.)x11                            ed(.)x6 ff(.)x2 00(.)x2             PARTIAL
   0x001f  aa(.)x10 55(U)x1                    aa(.)x10                            PARTIAL
   0x0027  4d(M)x10 4c(L)x1                    4d(M)x10                            PARTIAL
   0x0029  00(.)x11                            00(.)x9 80(.)x1                     PARTIAL
   0x002d  0b(.)x11                            0b(.)x8 aa(.)x1 1b(.)x1             PARTIAL
   0x002e  fc(.)x11                            fc(.)x5 04(.)x4 56(V)x1             PARTIAL
   0x002f  61(a)x10 81(.)x1                    61(a)x9 aa(.)x1                     PARTIAL
   0x0030  05(.)x11                            05(.)x9 aa(.)x1                     PARTIAL
   0x0039  01(.)x10 00(.)x1                    01(.)x10                            PARTIAL
==== MECHANISM CONTEXT (involved fuzzers only) ====
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
  /home/miao/BlockerAnalyzer/prompts/libpng_4032.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4032,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4032 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4032 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4032 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).