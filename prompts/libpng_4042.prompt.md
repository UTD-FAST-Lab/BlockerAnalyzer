==== BLOCKER ====
Target: libpng
Branch ID: 4042
Location: /src/libpng/pngrutil.c:2634:8
Enclosing function: OSS_FUZZ_png_handle_zTXt
Source line:    if (buffer == NULL)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (ctx_coverage vs naive_ctx)
cmplog                           2        8          0  REFERENCE
value_profile                    5        5          0  REFERENCE
value_profile_cmplog             2        8          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     1        9          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             5        5          0  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 25  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=1.20h  loser=21.50h
  avg hitcount on branch: winner=8  loser=0
  prob_div=0.90  dur_div=20.30h  hit_div=8
  subject-level: delta_AUC=6413040.0  p_AUC=0.0003  delta_Final=91.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/4042/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_zTXt (/src/libpng/pngrutil.c:2598-2708) ---
[ ]  2596  void /* PRIVATE */
[ ]  2597  png_handle_zTXt(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  2598  {
[B]  2599     png_const_charp errmsg = NULL;
[B]  2600     png_bytep       buffer;
[B]  2601     png_uint_32     keyword_length;
[ ]  2602  
[B]  2603     png_debug(1, "in png_handle_zTXt");
[ ]  2604  
[B]  2605  #ifdef PNG_USER_LIMITS_SUPPORTED
[B]  2606     if (png_ptr->user_chunk_cache_max != 0)
[B]  2607     {
[B]  2608        if (png_ptr->user_chunk_cache_max == 1)
[ ]  2609        {
[ ]  2610           png_crc_finish(png_ptr, length);
[ ]  2611           return;
[ ]  2612        }
[ ]  2613  
[B]  2614        if (--png_ptr->user_chunk_cache_max == 1)
[ ]  2615        {
[ ]  2616           png_crc_finish(png_ptr, length);
[ ]  2617           png_chunk_benign_error(png_ptr, "no space in chunk cache");
[ ]  2618           return;
[ ]  2619        }
[B]  2620     }
[B]  2621  #endif
[ ]  2622  
[B]  2623     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  2624        png_chunk_error(png_ptr, "missing IHDR");
[ ]  2625  
[B]  2626     if ((png_ptr->mode & PNG_HAVE_IDAT) != 0)
[B]  2627        png_ptr->mode |= PNG_AFTER_IDAT;
[ ]  2628  
[ ]  2629     /* Note, "length" is sufficient here; we won't be adding
[ ]  2630      * a null terminator later.
[ ]  2631      */
[B]  2632     buffer = png_read_buffer(png_ptr, length, 2/*silent*/);
[ ]  2633  
[B]  2634     if (buffer == NULL) <-- BLOCKER
[W]  2635     {
[W]  2636        png_crc_finish(png_ptr, length);
[W]  2637        png_chunk_benign_error(png_ptr, "out of memory");
[W]  2638        return;
[W]  2639     }
[ ]  2640  
[L]  2641     png_crc_read(png_ptr, buffer, length);
[ ]  2642  
[L]  2643     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  2644        return;
[ ]  2645  
[ ]  2646     /* TODO: also check that the keyword contents match the spec! */
[L]  2647     for (keyword_length = 0;
[L]  2648        keyword_length < length && buffer[keyword_length] != 0;
[L]  2649        ++keyword_length)
[L]  2650        /* Empty loop to find end of name */ ;
[ ]  2651  
[L]  2652     if (keyword_length > 79 || keyword_length < 1)
[L]  2653        errmsg = "bad keyword";
[ ]  2654  
[ ]  2655     /* zTXt must have some LZ data after the keyword, although it may expand to
[ ]  2656      * zero bytes; we need a '\0' at the end of the keyword, the compression type
[ ]  2657      * then the LZ data:
[ ]  2658      */
[L]  2659     else if (keyword_length + 3 > length)
[L]  2660        errmsg = "truncated";
[ ]  2661  
[L]  2662     else if (buffer[keyword_length+1] != PNG_COMPRESSION_TYPE_BASE)
[ ]  2663        errmsg = "unknown compression type";
[ ]  2664  
[L]  2665     else
[L]  2666     {
[L]  2667        png_alloc_size_t uncompressed_length = PNG_SIZE_MAX;
[ ]  2668  
[ ]  2669        /* TODO: at present png_decompress_chunk imposes a single application
[ ]  2670         * level memory limit, this should be split to different values for iCCP
[ ]  2671         * and text chunks.
[ ]  2672         */
[L]  2673        if (png_decompress_chunk(png_ptr, length, keyword_length+2,
[L]  2674            &uncompressed_length, 1/*terminate*/) == Z_STREAM_END)
[L]  2675        {
[L]  2676           png_text text;
[ ]  2677  
[L]  2678           if (png_ptr->read_buffer == NULL)
[ ]  2679             errmsg="Read failure in png_handle_zTXt";
[L]  2680           else
[L]  2681           {
[ ]  2682              /* It worked; png_ptr->read_buffer now looks like a tEXt chunk
[ ]  2683               * except for the extra compression type byte and the fact that
[ ]  2684               * it isn't necessarily '\0' terminated.
[ ]  2685               */
[L]  2686              buffer = png_ptr->read_buffer;
[L]  2687              buffer[uncompressed_length+(keyword_length+2)] = 0;
[ ]  2688  
[L]  2689              text.compression = PNG_TEXT_COMPRESSION_zTXt;
[L]  2690              text.key = (png_charp)buffer;
[L]  2691              text.text = (png_charp)(buffer + keyword_length+2);
[L]  2692              text.text_length = uncompressed_length;
[L]  2693              text.itxt_length = 0;
[L]  2694              text.lang = NULL;
[L]  2695              text.lang_key = NULL;
[ ]  2696  
[L]  2697              if (png_set_text_2(png_ptr, info_ptr, &text, 1) != 0)
[ ]  2698                 errmsg = "insufficient memory";
[L]  2699           }
[L]  2700        }
[ ]  2701  
[L]  2702        else
[L]  2703           errmsg = png_ptr->zstream.msg;
[L]  2704     }
[ ]  2705  
[L]  2706     if (errmsg != NULL)
[L]  2707        png_chunk_benign_error(png_ptr, errmsg);
[L]  2708  }

--- No 1-hop callers of OSS_FUZZ_png_handle_zTXt fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     117       409  OSS_FUZZ_png_get_uint_31  (/src/libpng/pngrutil.c:23-30)
      97       377  OSS_FUZZ_png_read_chunk_header  (/src/libpng/pngrutil.c:157-192)
      97       375  OSS_FUZZ_png_check_chunk_name  (/src/libpng/pngrutil.c:3136-3151)
     136       413  OSS_FUZZ_png_crc_read  (/src/libpng/pngrutil.c:197-203)
      87       362  OSS_FUZZ_png_crc_error  (/src/libpng/pngrutil.c:252-285)
      94       363  OSS_FUZZ_png_crc_finish  (/src/libpng/pngrutil.c:212-245)
      94       363  OSS_FUZZ_png_check_chunk_length  (/src/libpng/pngrutil.c:3155-3191)
      24       103  pngrutil.c:png_read_buffer  (/src/libpng/pngrutil.c:299-332)
      10        54  OSS_FUZZ_png_handle_sBIT  (/src/libpng/pngrutil.c:1158-1234)
       0        25  OSS_FUZZ_png_handle_iTXt  (/src/libpng/pngrutil.c:2715-2858)
       2        22  OSS_FUZZ_png_handle_bKGD  (/src/libpng/pngrutil.c:1921-2033)
       2        20  OSS_FUZZ_png_handle_pCAL  (/src/libpng/pngrutil.c:2249-2371)
       3        18  OSS_FUZZ_png_handle_cHRM  (/src/libpng/pngrutil.c:1240-1306)
       2        15  OSS_FUZZ_png_handle_pHYs  (/src/libpng/pngrutil.c:2156-2196)
       1        13  OSS_FUZZ_png_handle_tEXt  (/src/libpng/pngrutil.c:2517-2591)
... (11 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_zTXt  (/src/libpng/pngrutil.c:2598-2708) ---
  d=1   L2606  T=16 F=0  T=35 F=0  if (png_ptr->user_chunk_cache_max != 0)
  d=1   L2608  T=0 F=16  T=0 F=35  if (png_ptr->user_chunk_cache_max == 1)
  d=1   L2614  T=0 F=16  T=0 F=35  if (--png_ptr->user_chunk_cache_max == 1)
  d=1   L2623  T=0 F=16  T=0 F=35  if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
  d=1   L2626  T=2 F=14  T=17 F=18  if ((png_ptr->mode & PNG_HAVE_IDAT) != 0)
  d=1   L2634  T=16 F=0  T=0 F=35  if (buffer == NULL)  <-- BLOCKER
  d=1   L2643  T=0 F=0  T=0 F=35  if (png_crc_finish(png_ptr, 0) != 0)
  d=1   L2648  T=0 F=0  T=742 F=24  keyword_length < length && buffer[keyword_length] != 0;
  d=1   L2648  T=0 F=0  T=731 F=11  keyword_length < length && buffer[keyword_length] != 0;
  d=1   L2652  T=0 F=0  T=0 F=31  if (keyword_length > 79 || keyword_length < 1)
  d=1   L2652  T=0 F=0  T=4 F=31  if (keyword_length > 79 || keyword_length < 1)
  d=1   L2659  T=0 F=0  T=26 F=5  else if (keyword_length + 3 > length)
  d=1   L2662  T=0 F=0  T=0 F=5  else if (buffer[keyword_length+1] != PNG_COMPRESSION_TYPE...
  d=1   L2673  T=0 F=0  T=1 F=4  if (png_decompress_chunk(png_ptr, length, keyword_length+2,
  d=1   L2678  T=0 F=0  T=0 F=1  if (png_ptr->read_buffer == NULL)
  d=1   L2697  T=0 F=0  T=0 F=1  if (png_set_text_2(png_ptr, info_ptr, &text, 1) != 0)
  d=1   L2706  T=0 F=0  T=34 F=1  if (errmsg != NULL)

[off-chain: 250 additional divergent branches across 34 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=00569506a665b0d0, size=42469 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=2e9ba19d1b0d3bce, size=989 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=349085e4ac0e37e5, size=3162 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 f8 66 41 4d 41 00 00 b1 8f 0b fc 61   .....fAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=39916ba1260d95b1, size=765 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=661f55aa188d2db2, size=7133 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=48ef51fe8927b302, size=8763 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=BytesExpandMutator,ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=3258b36fd9493cdb, size=8759 bytes, fuzzer=naive, trial=1, discovered_at=2s, mutation_op=QwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=2824e1c4bb6d0c25, size=868 bytes, fuzzer=naive, trial=1, discovered_at=25s, mutation_op=BytesInsertCopyMutator,ByteIncMutator,BitFlipMutator,BitFlipMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=0f3a450906b2a776, size=611 bytes, fuzzer=naive, trial=1, discovered_at=58s, mutation_op=DwordAddMutator,BytesDeleteMutator,QwordAddMutator,TokenReplace,BytesDeleteMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=13867d02cde57c76, size=1197 bytes, fuzzer=naive, trial=1, discovered_at=428s, mutation_op=BytesSetMutator,ByteInterestingMutator,BytesDeleteMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0013  5b([)x10                            5b([)x10 ab(.)x6                    PARTIAL
   0x0017  45(E)x10                            45(E)x10 01(.)x6                    PARTIAL
   0x0018  08(.)x10                            08(.)x10 01(.)x6                    PARTIAL
   0x0019  06(.)x10                            06(.)x10 00(.)x6                    PARTIAL
   0x001d  52(R)x10                            52(R)x10 7f(.)x6                    PARTIAL
   0x001e  ed(.)x10                            ed(.)x13 e4(.)x3                    PARTIAL
   0x001f  aa(.)x10                            aa(.)x15 56(V)x1                    PARTIAL
   0x0024  04(.)x9 f8(.)x1                     04(.)x16                            PARTIAL
   0x0025  67(g)x9 66(f)x1                     67(g)x16                            PARTIAL
   0x0029  00(.)x10                            00(.)x8 80(.)x8                     PARTIAL
   0x002b  b1(.)x10                            b1(.)x15 98(.)x1                    PARTIAL
   0x002d  0b(.)x10                            0b(.)x10 1b(.)x6                    PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_4042.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4042,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4042 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4042 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4042 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).