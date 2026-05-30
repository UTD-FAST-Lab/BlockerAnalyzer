==== BLOCKER ====
Target: libpng
Branch ID: 3872
Location: /src/libpng/png.c:2751:14
Enclosing function: OSS_FUZZ_png_check_fp_number
Source line:          if ((state & PNG_FP_SAW_DOT) != 0) /* two dots */
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (ctx_coverage vs naive_ctx)
cmplog                           2        8          0  REFERENCE
value_profile                    1        9          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     3        7          0  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 25  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.60h  loser=24.00h
  avg hitcount on branch: winner=30  loser=0
  prob_div=1.00  dur_div=22.40h  hit_div=30
  subject-level: delta_AUC=6413040.0  p_AUC=0.0003  delta_Final=91.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3872/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_check_fp_number (/src/libpng/png.c:2714-2834) ---
[ ]  2712  png_check_fp_number(png_const_charp string, size_t size, int *statep,
[ ]  2713      size_t *whereami)
[B]  2714  {
[B]  2715     int state = *statep;
[B]  2716     size_t i = *whereami;
[ ]  2717  
[B]  2718     while (i < size)
[B]  2719     {
[B]  2720        int type;
[ ]  2721        /* First find the type of the next character */
[B]  2722        switch (string[i])
[B]  2723        {
[W]  2724        case 43:  type = PNG_FP_SAW_SIGN;                   break;
[B]  2725        case 45:  type = PNG_FP_SAW_SIGN + PNG_FP_NEGATIVE; break;
[B]  2726        case 46:  type = PNG_FP_SAW_DOT;                    break;
[B]  2727        case 48:  type = PNG_FP_SAW_DIGIT;                  break;
[B]  2728        case 49: case 50: case 51: case 52:
[B]  2729        case 53: case 54: case 55: case 56:
[B]  2730        case 57:  type = PNG_FP_SAW_DIGIT + PNG_FP_NONZERO; break;
[B]  2731        case 69:
[B]  2732        case 101: type = PNG_FP_SAW_E;                      break;
[B]  2733        default:  goto PNG_FP_End;
[B]  2734        }
[ ]  2735  
[ ]  2736        /* Now deal with this type according to the current
[ ]  2737         * state, the type is arranged to not overlap the
[ ]  2738         * bits of the PNG_FP_STATE.
[ ]  2739         */
[B]  2740        switch ((state & PNG_FP_STATE) + (type & PNG_FP_SAW_ANY))
[B]  2741        {
[W]  2742        case PNG_FP_INTEGER + PNG_FP_SAW_SIGN:
[W]  2743           if ((state & PNG_FP_SAW_ANY) != 0)
[ ]  2744              goto PNG_FP_End; /* not a part of the number */
[ ]  2745  
[W]  2746           png_fp_add(state, type);
[W]  2747           break;
[ ]  2748  
[B]  2749        case PNG_FP_INTEGER + PNG_FP_SAW_DOT:
[ ]  2750           /* Ok as trailer, ok as lead of fraction. */
[B]  2751           if ((state & PNG_FP_SAW_DOT) != 0) /* two dots */ <-- BLOCKER
[W]  2752              goto PNG_FP_End;
[ ]  2753  
[B]  2754           else if ((state & PNG_FP_SAW_DIGIT) != 0) /* trailing dot? */
[B]  2755              png_fp_add(state, type);
[ ]  2756  
[ ]  2757           else
[ ]  2758              png_fp_set(state, PNG_FP_FRACTION | type);
[ ]  2759  
[B]  2760           break;
[ ]  2761  
[B]  2762        case PNG_FP_INTEGER + PNG_FP_SAW_DIGIT:
[B]  2763           if ((state & PNG_FP_SAW_DOT) != 0) /* delayed fraction */
[L]  2764              png_fp_set(state, PNG_FP_FRACTION | PNG_FP_SAW_DOT);
[ ]  2765  
[B]  2766           png_fp_add(state, type | PNG_FP_WAS_VALID);
[ ]  2767  
[B]  2768           break;
[ ]  2769  
[B]  2770        case PNG_FP_INTEGER + PNG_FP_SAW_E:
[B]  2771           if ((state & PNG_FP_SAW_DIGIT) == 0)
[L]  2772              goto PNG_FP_End;
[ ]  2773  
[B]  2774           png_fp_set(state, PNG_FP_EXPONENT);
[ ]  2775  
[B]  2776           break;
[ ]  2777  
[ ]  2778     /* case PNG_FP_FRACTION + PNG_FP_SAW_SIGN:
[ ]  2779           goto PNG_FP_End; ** no sign in fraction */
[ ]  2780  
[ ]  2781     /* case PNG_FP_FRACTION + PNG_FP_SAW_DOT:
[ ]  2782           goto PNG_FP_End; ** Because SAW_DOT is always set */
[ ]  2783  
[L]  2784        case PNG_FP_FRACTION + PNG_FP_SAW_DIGIT:
[L]  2785           png_fp_add(state, type | PNG_FP_WAS_VALID);
[L]  2786           break;
[ ]  2787  
[L]  2788        case PNG_FP_FRACTION + PNG_FP_SAW_E:
[ ]  2789           /* This is correct because the trailing '.' on an
[ ]  2790            * integer is handled above - so we can only get here
[ ]  2791            * with the sequence ".E" (with no preceding digits).
[ ]  2792            */
[L]  2793           if ((state & PNG_FP_SAW_DIGIT) == 0)
[ ]  2794              goto PNG_FP_End;
[ ]  2795  
[L]  2796           png_fp_set(state, PNG_FP_EXPONENT);
[ ]  2797  
[L]  2798           break;
[ ]  2799  
[B]  2800        case PNG_FP_EXPONENT + PNG_FP_SAW_SIGN:
[B]  2801           if ((state & PNG_FP_SAW_ANY) != 0)
[ ]  2802              goto PNG_FP_End; /* not a part of the number */
[ ]  2803  
[B]  2804           png_fp_add(state, PNG_FP_SAW_SIGN);
[ ]  2805  
[B]  2806           break;
[ ]  2807  
[ ]  2808     /* case PNG_FP_EXPONENT + PNG_FP_SAW_DOT:
[ ]  2809           goto PNG_FP_End; */
[ ]  2810  
[B]  2811        case PNG_FP_EXPONENT + PNG_FP_SAW_DIGIT:
[B]  2812           png_fp_add(state, PNG_FP_SAW_DIGIT | PNG_FP_WAS_VALID);
[ ]  2813  
[B]  2814           break;
[ ]  2815  
[ ]  2816     /* case PNG_FP_EXPONEXT + PNG_FP_SAW_E:
[ ]  2817           goto PNG_FP_End; */
[ ]  2818  
[ ]  2819        default: goto PNG_FP_End; /* I.e. break 2 */
[B]  2820        }
[ ]  2821  
[ ]  2822        /* The character seems ok, continue. */
[B]  2823        ++i;
[B]  2824     }
[ ]  2825  
[B]  2826  PNG_FP_End:
[ ]  2827     /* Here at the end, update the state and return the correct
[ ]  2828      * return code.
[ ]  2829      */
[B]  2830     *statep = state;
[B]  2831     *whereami = i;
[ ]  2832  
[B]  2833     return (state & PNG_FP_SAW_DIGIT) != 0;
[B]  2834  }

--- No 1-hop callers of OSS_FUZZ_png_check_fp_number fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     160        34  OSS_FUZZ_png_muldiv  (/src/libpng/png.c:3351-3461)
      18         2  png.c:png_colorspace_endpoints_match  (/src/libpng/png.c:1593-1605)
       1        14  OSS_FUZZ_png_zalloc  (/src/libpng/png.c:99-114)
       1        14  OSS_FUZZ_png_zfree  (/src/libpng/png.c:119-121)
       9         2  png.c:png_XYZ_from_xy  (/src/libpng/png.c:1277-1539)
       9         2  png.c:png_colorspace_check_xy  (/src/libpng/png.c:1619-1638)
       9         2  OSS_FUZZ_png_colorspace_set_chromaticities  (/src/libpng/png.c:1722-1754)
       0         5  OSS_FUZZ_png_zstream_error  (/src/libpng/png.c:999-1061)
       6         1  png.c:png_xy_from_XYZ  (/src/libpng/png.c:1234-1273)
       6         1  png.c:png_colorspace_set_xy_and_XYZ  (/src/libpng/png.c:1675-1717)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_check_fp_number  (/src/libpng/png.c:2714-2834) ---
  d=1   L2724  T=1 F=298  T=0 F=385  case 43:  type = PNG_FP_SAW_SIGN;                   break;
  d=1   L2729  T=0 F=299  T=20 F=365  case 53: case 54: case 55: case 56:
  d=1   L2729  T=12 F=287  T=0 F=385  case 53: case 54: case 55: case 56:
  d=1   L2742  T=1 F=276  T=0 F=369  case PNG_FP_INTEGER + PNG_FP_SAW_SIGN:
  d=1   L2743  T=0 F=1  T=0 F=0  if ((state & PNG_FP_SAW_ANY) != 0)
  d=1   L2751  T=28 F=28  T=0 F=21  if ((state & PNG_FP_SAW_DOT) != 0) /* two dots */  <-- BLOCKER
  d=1   L2763  T=0 F=150  T=21 F=188  if ((state & PNG_FP_SAW_DOT) != 0) /* delayed fraction */
  d=1   L2771  T=0 F=21  T=2 F=32  if ((state & PNG_FP_SAW_DIGIT) == 0)
  d=1   L2784  T=0 F=277  T=15 F=354  case PNG_FP_FRACTION + PNG_FP_SAW_DIGIT:
  d=1   L2788  T=0 F=277  T=13 F=356  case PNG_FP_FRACTION + PNG_FP_SAW_E:
  d=1   L2793  T=0 F=0  T=0 F=13  if ((state & PNG_FP_SAW_DIGIT) == 0)

[off-chain: 81 additional divergent branches across 12 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=073c9d7c1c88a07b, size=957 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=08b35c5341d08fdb, size=449 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=293ebef9b4cb2e23, size=501 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=41c35fc0ab2764b6, size=1134 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=42d7d1cad4015f5c, size=1134 bytes, fuzzer=naive_ctx, trial=1):
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
Seed 3 (id=00c12f3d55212fd8, size=932 bytes, fuzzer=naive, trial=1, discovered_at=408s, mutation_op=QwordAddMutator,ByteInterestingMutator,BytesSetMutator,ByteIncMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 55 00 00 a0 86 10 00 00 00 01 7f ed aa   ...U............
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=00a0761917250025, size=768 bytes, fuzzer=naive, trial=1, discovered_at=1159s, mutation_op=DwordAddMutator,TokenReplace,BytesInsertCopyMutator,BytesRandInsertMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 05 0a 00 00 80 00 02 00 00 00 01 00 ff aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=004b9750af3eaa48, size=5109 bytes, fuzzer=naive, trial=1, discovered_at=1232s, mutation_op=ByteNegMutator,BytesDeleteMutator,CrossoverReplaceMutator,WordInterestingMutator,ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 00 00 03 04 00 00 00 01 00 00 aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x10                            00(.)x9 05(.)x1                     PARTIAL
   0x0013  5b([)x10                            5b([)x3 21(!)x1 55(U)x1 0a(.)x1 +4u  PARTIAL
   0x0016  00(.)x10                            a0(.)x5 00(.)x3 80(.)x2             PARTIAL
   0x0017  45(E)x10                            86(.)x4 00(.)x3 45(E)x1 03(.)x1 +1u  PARTIAL
   0x0018  08(.)x10                            10(.)x3 01(.)x3 04(.)x2 08(.)x1 +1u  PARTIAL
   0x0019  06(.)x10                            00(.)x8 06(.)x1 04(.)x1             PARTIAL
   0x001c  01(.)x9 00(.)x1                     01(.)x10                            PARTIAL
   0x001d  52(R)x9 ff(.)x1                     7f(.)x4 52(R)x3 00(.)x3             PARTIAL
   0x001e  ed(.)x10                            ed(.)x7 ff(.)x2 00(.)x1             PARTIAL
   0x0029  00(.)x10                            00(.)x9 80(.)x1                     PARTIAL
   0x002d  0b(.)x10                            0b(.)x8 aa(.)x1 1b(.)x1             PARTIAL
   0x002e  fc(.)x10                            fc(.)x6 04(.)x3 56(V)x1             PARTIAL
   0x002f  61(a)x10                            61(a)x9 aa(.)x1                     PARTIAL
   0x0030  05(.)x10                            05(.)x9 aa(.)x1                     PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3872.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3872,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3872 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3872 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3872 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).