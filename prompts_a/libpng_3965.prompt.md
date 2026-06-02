==== BLOCKER ====
Target: libpng
Branch ID: 3965
Location: /src/libpng/pngrutil.c:1136:8
Enclosing function: OSS_FUZZ_png_handle_gAMA
Source line:    if (length != 4)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog); loser (ctx_coverage vs naive_ctx)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     3        7          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.00h  loser=24.00h
  avg hitcount on branch: winner=111  loser=0
  prob_div=1.00  dur_div=24.00h  hit_div=111
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002
--- Pair 2: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 25  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.90h  loser=24.00h
  avg hitcount on branch: winner=14  loser=0
  prob_div=1.00  dur_div=23.10h  hit_div=14
  subject-level: delta_AUC=6413040.0  p_AUC=0.0003  delta_Final=91.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3965/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_gAMA (/src/libpng/pngrutil.c:1120-1152) ---
[ ]  1118  void /* PRIVATE */
[ ]  1119  png_handle_gAMA(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  1120  {
[B]  1121     png_fixed_point igamma;
[B]  1122     png_byte buf[4];
[ ]  1123  
[B]  1124     png_debug(1, "in png_handle_gAMA");
[ ]  1125  
[B]  1126     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  1127        png_chunk_error(png_ptr, "missing IHDR");
[ ]  1128  
[B]  1129     else if ((png_ptr->mode & (PNG_HAVE_IDAT|PNG_HAVE_PLTE)) != 0)
[L]  1130     {
[L]  1131        png_crc_finish(png_ptr, length);
[L]  1132        png_chunk_benign_error(png_ptr, "out of place");
[L]  1133        return;
[L]  1134     }
[ ]  1135  
[B]  1136     if (length != 4) <-- BLOCKER
[W]  1137     {
[W]  1138        png_crc_finish(png_ptr, length);
[W]  1139        png_chunk_benign_error(png_ptr, "invalid");
[W]  1140        return;
[W]  1141     }
[ ]  1142  
[B]  1143     png_crc_read(png_ptr, buf, 4);
[ ]  1144  
[B]  1145     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  1146        return;
[ ]  1147  
[B]  1148     igamma = png_get_fixed_point(NULL, buf);
[ ]  1149  
[B]  1150     png_colorspace_set_gamma(png_ptr, &png_ptr->colorspace, igamma);
[B]  1151     png_colorspace_sync(png_ptr, info_ptr);
[B]  1152  }

--- No 1-hop callers of OSS_FUZZ_png_handle_gAMA fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1340      5940  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
      58       605  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
     153       558  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
       0       391  pngrutil.c:png_read_filter_row_paeth_multibyte_pixel  (/src/libpng/pngrutil.c:4046-4092)
     500       130  OSS_FUZZ_png_crc_read  (/src/libpng/pngrutil.c:197-203)
     465       149  OSS_FUZZ_png_get_uint_31  (/src/libpng/pngrutil.c:23-30)
     413       129  OSS_FUZZ_png_read_chunk_header  (/src/libpng/pngrutil.c:157-192)
     411       128  OSS_FUZZ_png_check_chunk_name  (/src/libpng/pngrutil.c:3136-3151)
     393       120  OSS_FUZZ_png_crc_finish  (/src/libpng/pngrutil.c:212-245)
     399       126  OSS_FUZZ_png_check_chunk_length  (/src/libpng/pngrutil.c:3155-3191)
     387       119  OSS_FUZZ_png_crc_error  (/src/libpng/pngrutil.c:252-285)
     234        35  pngrutil.c:png_get_fixed_point  (/src/libpng/pngrutil.c:42-53)
      39       184  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
     122        40  pngrutil.c:png_read_buffer  (/src/libpng/pngrutil.c:299-332)
      59        13  OSS_FUZZ_png_handle_gAMA  (/src/libpng/pngrutil.c:1120-1152)  <-- enclosing
... (15 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_gAMA  (/src/libpng/pngrutil.c:1120-1152) ---
  d=1   L1126  T=0 F=59  T=0 F=13  if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
  d=1   L1129  T=0 F=59  T=2 F=11  else if ((png_ptr->mode & (PNG_HAVE_IDAT|PNG_HAVE_PLTE)) ...
  d=1   L1136  T=33 F=26  T=0 F=11  if (length != 4)  <-- BLOCKER
  d=1   L1145  T=0 F=26  T=0 F=11  if (png_crc_finish(png_ptr, 0) != 0)

[off-chain: 288 additional divergent branches across 43 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0d325a4e6804119a, size=9214 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 80 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=1994aa016d1b93dc, size=12961 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=1e5e894c2e322f55, size=1663 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 00 67 41 4d 41 00 00 aa e4 00 00 00   .....gAMA.......
  0030: 00 67 41 4d 41 00 00 b1 e4 00 00 00 00 67 41 4d   .gAMA........gAM
Seed 4 (id=3d994316fb991b92, size=2954 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 00 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=3ec59f6de19a56e3, size=1601 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 01 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 4b 55 55 15 52 47 42 01 d9 c9 4c 7f 00 00   ..KUU.RGB...L...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00140bdb0aa48f31, size=2316 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator,CrossoverReplaceMutator,TokenInsert,DwordInterestingMutator,BytesExpandMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=00c12f3d55212fd8, size=932 bytes, fuzzer=naive, trial=1, discovered_at=408s, mutation_op=QwordAddMutator,ByteInterestingMutator,BytesSetMutator,ByteIncMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 55 00 00 a0 86 10 00 00 00 01 7f ed aa   ...U............
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=00a0761917250025, size=768 bytes, fuzzer=naive, trial=1, discovered_at=1159s, mutation_op=DwordAddMutator,TokenReplace,BytesInsertCopyMutator,BytesRandInsertMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 05 0a 00 00 80 00 02 00 00 00 01 00 ff aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=004b9750af3eaa48, size=5109 bytes, fuzzer=naive, trial=1, discovered_at=1232s, mutation_op=ByteNegMutator,BytesDeleteMutator,CrossoverReplaceMutator,WordInterestingMutator,ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 00 00 03 04 00 00 00 01 00 00 aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=014d4a3ba385c013, size=1030 bytes, fuzzer=naive, trial=1, discovered_at=1748s, mutation_op=QwordAddMutator,CrossoverInsertMutator,ByteNegMutator,WordInterestingMutator,TokenReplace,ByteFlipMutator,ByteNegMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 10 00 00 a0 86 10 04 00 00 01 7f ed aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f aa 56 aa   .....gAMA.....V.
  0030: aa 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x26                            00(.)x9 05(.)x1                     PARTIAL
   0x0013  5b([)x22 03(.)x3 63(c)x1            5b([)x2 55(U)x1 0a(.)x1 05(.)x1 +5u  PARTIAL
   0x0015  00(.)x23 0f(.)x3                    00(.)x10                            PARTIAL
   0x0016  00(.)x23 42(B)x3                    a0(.)x4 00(.)x3 80(.)x2 02(.)x1     PARTIAL
   0x0017  45(E)x22 40(@)x3 15(.)x1            86(.)x3 00(.)x3 45(E)x2 03(.)x1 +1u  PARTIAL
   0x0018  08(.)x25 04(.)x1                    10(.)x4 08(.)x2 04(.)x2 02(.)x1 +1u  PARTIAL
   0x0019  06(.)x21 02(.)x3 00(.)x1 03(.)x1    00(.)x7 04(.)x2 06(.)x1             PARTIAL
   0x001d  52(R)x25 84(.)x1                    7f(.)x4 00(.)x3 52(R)x2 ff(.)x1     PARTIAL
   0x001e  ed(.)x25 1d(.)x1                    ed(.)x7 ff(.)x2 00(.)x1             PARTIAL
   0x001f  aa(.)x23 ab(.)x2 81(.)x1            aa(.)x10                            PARTIAL
   0x0020  e4(.)x25 e6(.)x1                    e4(.)x10                            PARTIAL
   0x0023  00(.)x21 80(.)x4 01(.)x1            00(.)x10                            PARTIAL
   0x0024  04(.)x22 00(.)x3 34(4)x1            04(.)x10                            PARTIAL
   0x0025  67(g)x25 65(e)x1                    67(g)x10                            PARTIAL
   0x0026  41(A)x25 58(X)x1                    41(A)x10                            PARTIAL
   0x0027  4d(M)x25 49(I)x1                    4d(M)x10                            PARTIAL
   0x0028  41(A)x25 66(f)x1                    41(A)x10                            PARTIAL
   0x0029  00(.)x25 4d(M)x1                    00(.)x9 80(.)x1                     PARTIAL
   0x002a  00(.)x25 4d(M)x1                    00(.)x10                            PARTIAL
   0x002b  b1(.)x23 aa(.)x2 00(.)x1            b1(.)x10                            PARTIAL
   0x002c  8f(.)x23 e4(.)x2 6d(m)x1            8f(.)x10                            PARTIAL
   0x002d  0b(.)x23 00(.)x2 e2(.)x1            0b(.)x9 aa(.)x1                     PARTIAL
   0x002e  fc(.)x23 00(.)x2 9d(.)x1            fc(.)x6 04(.)x3 56(V)x1             PARTIAL
   0x002f  61(a)x14 00(.)x11 10(.)x1           61(a)x9 aa(.)x1                     PARTIAL
   0x0030  05(.)x23 00(.)x2 1a(.)x1            05(.)x9 aa(.)x1                     PARTIAL
   0x0031  00(.)x23 67(g)x2 42(B)x1            00(.)x10                            PARTIAL
   0x0032  00(.)x22 41(A)x2 4b(K)x1 dd(.)x1    00(.)x10                            PARTIAL
   0x0033  00(.)x22 4d(M)x2 55(U)x1 30(0)x1    00(.)x10                            PARTIAL
   0x0034  01(.)x22 41(A)x2 55(U)x1 28(()x1    01(.)x9 09(.)x1                     PARTIAL
   0x0035  73(s)x13 74(t)x8 00(.)x2 15(.)x1 +2u  73(s)x9 74(t)x1                     PARTIAL
   0x0036  52(R)x14 45(E)x8 00(.)x2 25(%)x1 +1u  52(R)x9 45(E)x1                     PARTIAL
   0x0037  47(G)x14 58(X)x8 b1(.)x2 5c(\)x1 +1u  47(G)x9 58(X)x1                     PARTIAL
   0x0038  42(B)x14 74(t)x8 e4(.)x2 ff(.)x1 +1u  42(B)x9 74(t)x1                     PARTIAL
   0x0039  01(.)x23 00(.)x2 bf(.)x1            01(.)x9 54(T)x1                     PARTIAL
   0x003a  d9(.)x23 00(.)x2 13(.)x1            d9(.)x9 69(i)x1                     PARTIAL
   0x003b  c9(.)x23 00(.)x2 41(A)x1            c9(.)x9 74(t)x1                     PARTIAL
   0x003c  2c(,)x22 00(.)x2 4c(L)x1 89(.)x1    2c(,)x9 6c(l)x1                     PARTIAL
   0x003d  7f(.)x23 67(g)x2 bc(.)x1            7f(.)x9 65(e)x1                     PARTIAL
   0x003e  00(.)x23 41(A)x2 32(2)x1            00(.)x10                            PARTIAL
   0x003f  00(.)x23 4d(M)x2 78(x)x1            00(.)x10                            PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3965.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3965,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3965 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3965 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3965 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).