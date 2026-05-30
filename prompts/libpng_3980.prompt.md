==== BLOCKER ====
Target: libpng
Branch ID: 3980
Location: /src/libpng/pngrutil.c:1327:8
Enclosing function: OSS_FUZZ_png_handle_sRGB
Source line:    if (length != 1)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog); loser (ctx_coverage vs naive_ctx)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     3        7          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'naive_ctx', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (3) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.00h  loser=21.80h
  avg hitcount on branch: winner=80  loser=0
  prob_div=0.90  dur_div=21.80h  hit_div=80
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.20h  loser=21.80h
  avg hitcount on branch: winner=217  loser=0
  prob_div=0.90  dur_div=21.60h  hit_div=217
  subject-level: delta_AUC=13087800.0  p_AUC=0.0002  delta_Final=135.8  p_final=0.0002
--- Pair 3: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 25  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=2.50h  loser=21.80h
  avg hitcount on branch: winner=11  loser=0
  prob_div=0.90  dur_div=19.30h  hit_div=11
  subject-level: delta_AUC=6413040.0  p_AUC=0.0003  delta_Final=91.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3980/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_sRGB (/src/libpng/pngrutil.c:1312-1356) ---
[ ]  1310  void /* PRIVATE */
[ ]  1311  png_handle_sRGB(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  1312  {
[B]  1313     png_byte intent;
[ ]  1314  
[B]  1315     png_debug(1, "in png_handle_sRGB");
[ ]  1316  
[B]  1317     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  1318        png_chunk_error(png_ptr, "missing IHDR");
[ ]  1319  
[B]  1320     else if ((png_ptr->mode & (PNG_HAVE_IDAT|PNG_HAVE_PLTE)) != 0)
[L]  1321     {
[L]  1322        png_crc_finish(png_ptr, length);
[L]  1323        png_chunk_benign_error(png_ptr, "out of place");
[L]  1324        return;
[L]  1325     }
[ ]  1326  
[B]  1327     if (length != 1) <-- BLOCKER
[W]  1328     {
[W]  1329        png_crc_finish(png_ptr, length);
[W]  1330        png_chunk_benign_error(png_ptr, "invalid");
[W]  1331        return;
[W]  1332     }
[ ]  1333  
[B]  1334     png_crc_read(png_ptr, &intent, 1);
[ ]  1335  
[B]  1336     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  1337        return;
[ ]  1338  
[ ]  1339     /* If a colorspace error has already been output skip this chunk */
[B]  1340     if ((png_ptr->colorspace.flags & PNG_COLORSPACE_INVALID) != 0)
[B]  1341        return;
[ ]  1342  
[ ]  1343     /* Only one sRGB or iCCP chunk is allowed, use the HAVE_INTENT flag to detect
[ ]  1344      * this.
[ ]  1345      */
[B]  1346     if ((png_ptr->colorspace.flags & PNG_COLORSPACE_HAVE_INTENT) != 0)
[W]  1347     {
[W]  1348        png_ptr->colorspace.flags |= PNG_COLORSPACE_INVALID;
[W]  1349        png_colorspace_sync(png_ptr, info_ptr);
[W]  1350        png_chunk_benign_error(png_ptr, "too many profiles");
[W]  1351        return;
[W]  1352     }
[ ]  1353  
[B]  1354     (void)png_colorspace_set_sRGB(png_ptr, &png_ptr->colorspace, intent);
[B]  1355     png_colorspace_sync(png_ptr, info_ptr);
[B]  1356  }

--- No 1-hop callers of OSS_FUZZ_png_handle_sRGB fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      57       203  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
      56       173  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
      78        24  OSS_FUZZ_png_handle_sRGB  (/src/libpng/pngrutil.c:1312-1356)  <-- enclosing
       0        30  pngrutil.c:png_read_filter_row_sub  (/src/libpng/pngrutil.c:3934-3947)
      21         1  OSS_FUZZ_png_handle_zTXt  (/src/libpng/pngrutil.c:2598-2708)
      14         0  OSS_FUZZ_png_handle_tRNS  (/src/libpng/pngrutil.c:1817-1915)
      12         0  OSS_FUZZ_png_handle_iTXt  (/src/libpng/pngrutil.c:2715-2858)
      10         0  OSS_FUZZ_png_handle_sPLT  (/src/libpng/pngrutil.c:1641-1811)
       8         1  pngrutil.c:png_decompress_chunk  (/src/libpng/pngrutil.c:613-764)
       8         1  OSS_FUZZ_png_handle_eXIf  (/src/libpng/pngrutil.c:2039-2097)
       8         2  pngrutil.c:png_inflate  (/src/libpng/pngrutil.c:487-599)
       5         0  OSS_FUZZ_png_handle_PLTE  (/src/libpng/pngrutil.c:913-1096)
       4         0  OSS_FUZZ_png_handle_iCCP  (/src/libpng/pngrutil.c:1363-1634)
       0         1  OSS_FUZZ_png_handle_IEND  (/src/libpng/pngrutil.c:1100-1115)
       1         0  OSS_FUZZ_png_handle_hIST  (/src/libpng/pngrutil.c:2103-2150)
... (1 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_sRGB  (/src/libpng/pngrutil.c:1312-1356) ---
  d=1   L1317  T=0 F=78  T=0 F=24  if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
  d=1   L1320  T=0 F=78  T=2 F=22  else if ((png_ptr->mode & (PNG_HAVE_IDAT|PNG_HAVE_PLTE)) ...
  d=1   L1327  T=46 F=32  T=0 F=22  if (length != 1)  <-- BLOCKER
  d=1   L1346  T=2 F=27  T=0 F=20  if ((png_ptr->colorspace.flags & PNG_COLORSPACE_HAVE_INTE...

[off-chain: 249 additional divergent branches across 38 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=02383266bef90f18, size=1850 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=145aa5d72c190d92, size=662 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 ff ff ff 80 fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=22002e4f235928ae, size=1856 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=2bfd3e724b7474a4, size=15580 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 1d 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=36a40c39de0f6592, size=256 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 28 28 28 28 28   .....gAMA..(((((
  0030: 28 28 28 28 28 73 52 47 42 01 d9 c9 2c 7f 00 00   (((((sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00140bdb0aa48f31, size=2316 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator,CrossoverReplaceMutator,TokenInsert,DwordInterestingMutator,BytesExpandMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
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
   0x0012  00(.)x38 08(.)x1                    00(.)x20 05(.)x1                    PARTIAL
   0x0016  00(.)x33 31(1)x3 01(.)x1 06(.)x1 +1u  00(.)x9 80(.)x6 a0(.)x4 a1(.)x2     PARTIAL
   0x0017  45(E)x31 39(9)x5 01(.)x2 00(.)x1    00(.)x7 45(E)x6 86(.)x5 01(.)x2 +1u  PARTIAL
   0x0018  08(.)x24 01(.)x8 04(.)x4 02(.)x3    08(.)x8 04(.)x5 10(.)x3 02(.)x3 +1u  PARTIAL
   0x0019  06(.)x17 00(.)x17 03(.)x3 02(.)x2   00(.)x12 06(.)x7 04(.)x2            PARTIAL
   0x001d  52(R)x37 84(.)x2                    52(R)x13 00(.)x4 7f(.)x3 ff(.)x1    PARTIAL
   0x001e  ed(.)x37 1d(.)x2                    ed(.)x17 ff(.)x3 00(.)x1            PARTIAL
   0x001f  aa(.)x37 81(.)x2                    aa(.)x21                            PARTIAL
   0x0020  e4(.)x37 e6(.)x2                    e4(.)x21                            PARTIAL
   0x0024  04(.)x37 34(4)x2                    04(.)x21                            PARTIAL
   0x0025  67(g)x34 65(e)x2 69(i)x2 7a(z)x1    67(g)x21                            PARTIAL
   0x0026  41(A)x34 54(T)x3 58(X)x2            41(A)x20 59(Y)x1                    PARTIAL
   0x0027  4d(M)x34 58(X)x3 49(I)x2            4d(M)x21                            PARTIAL
   0x0028  41(A)x34 74(t)x3 66(f)x2            41(A)x21                            PARTIAL
   0x0029  00(.)x37 4d(M)x2                    00(.)x20 80(.)x1                    PARTIAL
   0x002a  00(.)x38 ff(.)x1                    00(.)x21                            PARTIAL
   0x002b  b1(.)x35 00(.)x2 ff(.)x1 28(()x1    b1(.)x21                            PARTIAL
   0x002c  8f(.)x35 00(.)x2 ff(.)x1 28(()x1    8f(.)x20 0f(.)x1                    PARTIAL
   0x002d  0b(.)x35 00(.)x2 80(.)x1 28(()x1    0b(.)x20 aa(.)x1                    PARTIAL
   0x002e  fc(.)x36 00(.)x2 28(()x1            fc(.)x16 04(.)x4 56(V)x1            PARTIAL
   0x002f  61(a)x33 00(.)x5 28(()x1            61(a)x20 aa(.)x1                    PARTIAL
   0x0030  05(.)x34 00(.)x2 07(.)x2 28(()x1    05(.)x20 aa(.)x1                    PARTIAL
   0x0031  00(.)x37 1d(.)x1 28(()x1            00(.)x21                            PARTIAL
   0x0032  00(.)x36 dd(.)x2 28(()x1            00(.)x21                            PARTIAL
   0x0033  00(.)x36 30(0)x2 28(()x1            00(.)x21                            PARTIAL
   0x0034  01(.)x34 28(()x3 86(.)x1 ef(.)x1    01(.)x21                            PARTIAL
   0x0035  73(s)x34 74(t)x3 92(.)x2            73(s)x21                            PARTIAL
   0x0036  52(R)x31 50(P)x3 45(E)x3 25(%)x2    52(R)x21                            PARTIAL
   0x0037  47(G)x31 4c(L)x3 58(X)x3 5c(\)x2    47(G)x21                            PARTIAL
   0x0038  42(B)x31 54(T)x3 74(t)x3 ff(.)x2    42(B)x21                            PARTIAL
   0x0039  01(.)x37 bf(.)x2                    01(.)x21                            PARTIAL
   0x003a  d9(.)x37 13(.)x2                    d9(.)x21                            PARTIAL
   0x003b  c9(.)x37 41(A)x2                    c9(.)x21                            PARTIAL
   0x003c  2c(,)x37 89(.)x2                    2c(,)x21                            PARTIAL
   0x003d  7f(.)x37 bc(.)x2                    7f(.)x21                            PARTIAL
   0x003e  00(.)x37 32(2)x2                    00(.)x21                            PARTIAL
   0x003f  00(.)x37 78(x)x2                    00(.)x21                            PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3980.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3980,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile_cmplog>value_profile (I2S), naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3980 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3980 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3980 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).