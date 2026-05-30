==== BLOCKER ====
Target: libpng
Branch ID: 3820
Location: /src/libpng/png.c:1007:7
Enclosing function: OSS_FUZZ_png_zstream_error
Source line:       case Z_OK:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        8          2  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=8  unreached=2
  avg duration blocked: winner=5.60h  loser=23.88h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.90  dur_div=18.27h  hit_div=5
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3820/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_zstream_error (/src/libpng/png.c:999-1061) ---
[ ]   997  void /* PRIVATE */
[ ]   998  png_zstream_error(png_structrp png_ptr, int ret)
[B]   999  {
[ ]  1000     /* Translate 'ret' into an appropriate error string, priority is given to the
[ ]  1001      * one in zstream if set.  This always returns a string, even in cases like
[ ]  1002      * Z_OK or Z_STREAM_END where the error code is a success code.
[ ]  1003      */
[B]  1004     if (png_ptr->zstream.msg == NULL) switch (ret)
[B]  1005     {
[ ]  1006        default:
[W]  1007        case Z_OK: <-- BLOCKER
[W]  1008           png_ptr->zstream.msg = PNGZ_MSG_CAST("unexpected zlib return code");
[W]  1009           break;
[ ]  1010  
[L]  1011        case Z_STREAM_END:
[ ]  1012           /* Normal exit */
[L]  1013           png_ptr->zstream.msg = PNGZ_MSG_CAST("unexpected end of LZ stream");
[L]  1014           break;
[ ]  1015  
[ ]  1016        case Z_NEED_DICT:
[ ]  1017           /* This means the deflate stream did not have a dictionary; this
[ ]  1018            * indicates a bogus PNG.
[ ]  1019            */
[ ]  1020           png_ptr->zstream.msg = PNGZ_MSG_CAST("missing LZ dictionary");
[ ]  1021           break;
[ ]  1022  
[ ]  1023        case Z_ERRNO:
[ ]  1024           /* gz APIs only: should not happen */
[ ]  1025           png_ptr->zstream.msg = PNGZ_MSG_CAST("zlib IO error");
[ ]  1026           break;
[ ]  1027  
[ ]  1028        case Z_STREAM_ERROR:
[ ]  1029           /* internal libpng error */
[ ]  1030           png_ptr->zstream.msg = PNGZ_MSG_CAST("bad parameters to zlib");
[ ]  1031           break;
[ ]  1032  
[ ]  1033        case Z_DATA_ERROR:
[ ]  1034           png_ptr->zstream.msg = PNGZ_MSG_CAST("damaged LZ stream");
[ ]  1035           break;
[ ]  1036  
[ ]  1037        case Z_MEM_ERROR:
[ ]  1038           png_ptr->zstream.msg = PNGZ_MSG_CAST("insufficient memory");
[ ]  1039           break;
[ ]  1040  
[L]  1041        case Z_BUF_ERROR:
[ ]  1042           /* End of input or output; not a problem if the caller is doing
[ ]  1043            * incremental read or write.
[ ]  1044            */
[L]  1045           png_ptr->zstream.msg = PNGZ_MSG_CAST("truncated");
[L]  1046           break;
[ ]  1047  
[ ]  1048        case Z_VERSION_ERROR:
[ ]  1049           png_ptr->zstream.msg = PNGZ_MSG_CAST("unsupported zlib version");
[ ]  1050           break;
[ ]  1051  
[ ]  1052        case PNG_UNEXPECTED_ZLIB_RETURN:
[ ]  1053           /* Compile errors here mean that zlib now uses the value co-opted in
[ ]  1054            * pngpriv.h for PNG_UNEXPECTED_ZLIB_RETURN; update the switch above
[ ]  1055            * and change pngpriv.h.  Note that this message is "... return",
[ ]  1056            * whereas the default/Z_OK one is "... return code".
[ ]  1057            */
[ ]  1058           png_ptr->zstream.msg = PNGZ_MSG_CAST("unexpected zlib return");
[ ]  1059           break;
[B]  1060     }
[B]  1061  }

--- No 1-hop callers of OSS_FUZZ_png_zstream_error fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     311      3790  OSS_FUZZ_png_get_io_ptr  (/src/libpng/png.c:687-692)
     214      2540  OSS_FUZZ_png_calculate_crc  (/src/libpng/png.c:140-187)
      97      1250  OSS_FUZZ_png_reset_crc  (/src/libpng/png.c:128-131)
      83      1220  OSS_FUZZ_png_handle_as_unknown  (/src/libpng/png.c:927-956)
      83      1220  OSS_FUZZ_png_chunk_unknown_handling  (/src/libpng/png.c:962-967)
       0       460  OSS_FUZZ_png_muldiv  (/src/libpng/png.c:3351-3461)
      12       301  OSS_FUZZ_png_zstream_error  (/src/libpng/png.c:999-1061)  <-- enclosing
      15       152  OSS_FUZZ_png_colorspace_sync_info  (/src/libpng/png.c:1170-1211)
      15       152  OSS_FUZZ_png_colorspace_sync  (/src/libpng/png.c:1216-1222)
      28       141  OSS_FUZZ_png_free_data  (/src/libpng/png.c:473-678)
      11       112  OSS_FUZZ_png_colorspace_set_gamma  (/src/libpng/png.c:1116-1166)
       0        59  OSS_FUZZ_png_reciprocal  (/src/libpng/png.c:3489-3503)
       0        46  OSS_FUZZ_png_check_fp_number  (/src/libpng/png.c:2714-2834)
       0        45  png.c:png_colorspace_endpoints_match  (/src/libpng/png.c:1593-1605)
      39         0  png.c:is_ICC_signature_char  (/src/libpng/png.c:1808-1811)
... (15 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_zstream_error  (/src/libpng/png.c:999-1061) ---
  d=1   L1004  T=12 F=0  T=225 F=76  if (png_ptr->zstream.msg == NULL) switch (ret)
  d=1   L1006  T=0 F=12  T=0 F=225  default:
  d=1   L1007  T=12 F=0  T=0 F=225  case Z_OK:  <-- BLOCKER
  d=1   L1011  T=0 F=12  T=216 F=9  case Z_STREAM_END:
  d=1   L1016  T=0 F=12  T=0 F=225  case Z_NEED_DICT:
  d=1   L1023  T=0 F=12  T=0 F=225  case Z_ERRNO:
  d=1   L1028  T=0 F=12  T=0 F=225  case Z_STREAM_ERROR:
  d=1   L1033  T=0 F=12  T=0 F=225  case Z_DATA_ERROR:
  d=1   L1037  T=0 F=12  T=0 F=225  case Z_MEM_ERROR:
  d=1   L1041  T=0 F=12  T=9 F=216  case Z_BUF_ERROR:
  d=1   L1048  T=0 F=12  T=0 F=225  case Z_VERSION_ERROR:
  d=1   L1052  T=0 F=12  T=0 F=225  case PNG_UNEXPECTED_ZLIB_RETURN:

[off-chain: 189 additional divergent branches across 26 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c7492b31f4f7e961, size=1492 bytes, fuzzer=cmplog, trial=1, discovered_at=5439s, mutation_op=ByteInterestingMutator,CrossoverInsertMutator,WordInterestingMutator,TokenInsert,BytesInsertCopyMutator,WordInterestingMutator,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 2 (id=bea073a062f92b7f, size=4870 bytes, fuzzer=cmplog, trial=1, discovered_at=5465s, mutation_op=QwordAddMutator,BytesExpandMutator,CrossoverInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 3 (id=1b45f30bf07bbd72, size=1544 bytes, fuzzer=cmplog, trial=1, discovered_at=9777s, mutation_op=ByteNegMutator,ByteNegMutator,ByteFlipMutator,ByteAddMutator,CrossoverInsertMutator,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 4 (id=aef7419be2d8cb2e, size=1559 bytes, fuzzer=cmplog, trial=1, discovered_at=9834s, mutation_op=BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 5 (id=0cc62a66ece8b8fe, size=1425 bytes, fuzzer=cmplog, trial=2, discovered_at=12287s, mutation_op=QwordAddMutator,BytesDeleteMutator,ByteAddMutator,BytesDeleteMutator,BytesInsertMutator,ByteNegMutator,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 6b 52 47 42 01 d9 c9 2c 7f 00 00   .....kRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=20af14ddc952c142, size=8759 bytes, fuzzer=naive, trial=2, discovered_at=0s, mutation_op=CrossoverReplaceMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=507be6b9a424336e, size=460 bytes, fuzzer=naive, trial=2, discovered_at=21s, mutation_op=BytesInsertMutator,BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=1f268348ff7b068a, size=8759 bytes, fuzzer=naive, trial=3, discovered_at=39s, mutation_op=BytesSetMutator,WordInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=7326a857c3077801, size=1294 bytes, fuzzer=naive, trial=2, discovered_at=135s, mutation_op=BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=0c17fcefbdaef321, size=1298 bytes, fuzzer=naive, trial=2, discovered_at=137s, mutation_op=DwordAddMutator,QwordAddMutator,ByteDecMutator,BitFlipMutator,ByteDecMutator,TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0013  5b([)x12                            5b([)x17 9d(.)x2 74(t)x1            PARTIAL
   0x0017  45(E)x12                            45(E)x17 02(.)x2 01(.)x1            PARTIAL
   0x0018  08(.)x12                            08(.)x17 04(.)x3                    PARTIAL
   0x0019  06(.)x12                            06(.)x17 00(.)x3                    PARTIAL
   0x0025  67(g)x11 74(t)x1                    67(g)x20                            PARTIAL
   0x0026  41(A)x11 45(E)x1                    41(A)x20                            PARTIAL
   0x0027  4d(M)x11 58(X)x1                    4d(M)x20                            PARTIAL
   0x0028  41(A)x11 74(t)x1                    41(A)x20                            PARTIAL
   0x002c  8f(.)x12                            8f(.)x14 90(.)x6                    PARTIAL
   0x002f  61(a)x12                            61(a)x19 9f(.)x1                    PARTIAL
   0x0035  69(i)x6 6b(k)x5 73(s)x1             73(s)x20                            PARTIAL
   0x0036  54(T)x6 52(R)x5 50(P)x1             52(R)x20                            PARTIAL
   0x0037  58(X)x6 47(G)x5 4c(L)x1             47(G)x20                            PARTIAL
   0x0038  74(t)x6 42(B)x5 54(T)x1             42(B)x20                            PARTIAL
   0x003e  00(.)x11 31(1)x1                    00(.)x20                            PARTIAL
   0x003f  00(.)x11 2e(.)x1                    00(.)x20                            PARTIAL
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libpng_3820.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3820,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3820 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3820 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3820 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).