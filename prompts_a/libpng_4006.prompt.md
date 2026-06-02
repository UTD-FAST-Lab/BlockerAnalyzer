==== BLOCKER ====
Target: libpng
Branch ID: 4006
Location: /src/libpng/pngrutil.c:2047:8
Enclosing function: OSS_FUZZ_png_handle_eXIf
Source line:    if (length < 2)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.30h  loser=23.40h
  avg hitcount on branch: winner=29  loser=0
  prob_div=1.00  dur_div=20.10h  hit_div=29
  subject-level: delta_AUC=13087800.0  p_AUC=0.0002  delta_Final=135.8  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.30h  loser=23.10h
  avg hitcount on branch: winner=7  loser=0
  prob_div=0.90  dur_div=19.80h  hit_div=7
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/4006/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_eXIf (/src/libpng/pngrutil.c:2039-2097) ---
[ ]  2037  void /* PRIVATE */
[ ]  2038  png_handle_eXIf(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  2039  {
[B]  2040     unsigned int i;
[ ]  2041  
[B]  2042     png_debug(1, "in png_handle_eXIf");
[ ]  2043  
[B]  2044     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  2045        png_chunk_error(png_ptr, "missing IHDR");
[ ]  2046  
[B]  2047     if (length < 2) <-- BLOCKER
[W]  2048     {
[W]  2049        png_crc_finish(png_ptr, length);
[W]  2050        png_chunk_benign_error(png_ptr, "too short");
[W]  2051        return;
[W]  2052     }
[ ]  2053  
[L]  2054     else if (info_ptr == NULL || (info_ptr->valid & PNG_INFO_eXIf) != 0)
[L]  2055     {
[L]  2056        png_crc_finish(png_ptr, length);
[L]  2057        png_chunk_benign_error(png_ptr, "duplicate");
[L]  2058        return;
[L]  2059     }
[ ]  2060  
[L]  2061     info_ptr->free_me |= PNG_FREE_EXIF;
[ ]  2062  
[L]  2063     info_ptr->eXIf_buf = png_voidcast(png_bytep,
[L]  2064               png_malloc_warn(png_ptr, length));
[ ]  2065  
[L]  2066     if (info_ptr->eXIf_buf == NULL)
[L]  2067     {
[L]  2068        png_crc_finish(png_ptr, length);
[L]  2069        png_chunk_benign_error(png_ptr, "out of memory");
[L]  2070        return;
[L]  2071     }
[ ]  2072  
[L]  2073     for (i = 0; i < length; i++)
[L]  2074     {
[L]  2075        png_byte buf[1];
[L]  2076        png_crc_read(png_ptr, buf, 1);
[L]  2077        info_ptr->eXIf_buf[i] = buf[0];
[L]  2078        if (i == 1)
[L]  2079        {
[L]  2080           if ((buf[0] != 'M' && buf[0] != 'I') ||
[L]  2081               (info_ptr->eXIf_buf[0] != buf[0]))
[L]  2082           {
[L]  2083              png_crc_finish(png_ptr, length - 2);
[L]  2084              png_chunk_benign_error(png_ptr, "incorrect byte-order specifier");
[L]  2085              png_free(png_ptr, info_ptr->eXIf_buf);
[L]  2086              info_ptr->eXIf_buf = NULL;
[L]  2087              return;
[L]  2088           }
[L]  2089        }
[L]  2090     }
[ ]  2091  
[L]  2092     if (png_crc_finish(png_ptr, 0) == 0)
[L]  2093        png_set_eXIf_1(png_ptr, info_ptr, length, info_ptr->eXIf_buf);
[ ]  2094  
[L]  2095     png_free(png_ptr, info_ptr->eXIf_buf);
[L]  2096     info_ptr->eXIf_buf = NULL;
[L]  2097  }

--- No 1-hop callers of OSS_FUZZ_png_handle_eXIf fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     154      2420  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
     398      1630  OSS_FUZZ_png_crc_read  (/src/libpng/pngrutil.c:197-203)
      44       716  OSS_FUZZ_png_zlib_inflate  (/src/libpng/pngrutil.c:454-467)
      41       668  OSS_FUZZ_png_read_IDAT_data  (/src/libpng/pngrutil.c:4152-4276)
      39       663  OSS_FUZZ_png_combine_row  (/src/libpng/pngrutil.c:3202-3681)
       0       549  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
      29       493  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
       0       260  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
       0       165  pngrutil.c:png_read_filter_row_paeth_multibyte_pixel  (/src/libpng/pngrutil.c:4046-4092)
       0        74  pngrutil.c:png_read_filter_row_sub  (/src/libpng/pngrutil.c:3934-3947)
       0        50  pngrutil.c:png_read_filter_row_avg  (/src/libpng/pngrutil.c:3968-3990)
      55         7  OSS_FUZZ_png_handle_sPLT  (/src/libpng/pngrutil.c:1641-1811)
      16        61  OSS_FUZZ_png_handle_unknown  (/src/libpng/pngrutil.c:2925-3120)
      24         0  OSS_FUZZ_png_handle_iCCP  (/src/libpng/pngrutil.c:1363-1634)
      21         0  OSS_FUZZ_png_handle_hIST  (/src/libpng/pngrutil.c:2103-2150)
... (12 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_eXIf  (/src/libpng/pngrutil.c:2039-2097) ---
  d=1   L2047  T=23 F=0  T=0 F=35  if (length < 2)  <-- BLOCKER
  d=1   L2054  T=0 F=0  T=4 F=31  else if (info_ptr == NULL || (info_ptr->valid & PNG_INFO_...
  d=1   L2054  T=0 F=0  T=0 F=35  else if (info_ptr == NULL || (info_ptr->valid & PNG_INFO_...
  d=1   L2066  T=0 F=0  T=2 F=29  if (info_ptr->eXIf_buf == NULL)
  d=1   L2073  T=0 F=0  T=1290 F=23  for (i = 0; i < length; i++)
  d=1   L2078  T=0 F=0  T=29 F=1260  if (i == 1)
  d=1   L2080  T=0 F=0  T=6 F=23  if ((buf[0] != 'M' && buf[0] != 'I') ||
  d=1   L2080  T=0 F=0  T=6 F=0  if ((buf[0] != 'M' && buf[0] != 'I') ||
  d=1   L2081  T=0 F=0  T=0 F=23  (info_ptr->eXIf_buf[0] != buf[0]))
  d=1   L2092  T=0 F=0  T=23 F=0  if (png_crc_finish(png_ptr, 0) == 0)

[off-chain: 316 additional divergent branches across 41 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=db598a5afacbd5af, size=995 bytes, fuzzer=cmplog, trial=1, discovered_at=4s, mutation_op=DwordAddMutator,BytesExpandMutator,QwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=34c465bcdc21a928, size=995 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=BytesRandInsertMutator,ByteInterestingMutator,ByteNegMutator,BytesDeleteMutator,ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=42727b14b83c8457, size=995 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=BytesRandSetMutator,CrossoverInsertMutator,CrossoverReplaceMutator,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 74 52 4e 53 01 d9 c9 2c 7f 00 00   .....tRNS...,...
Seed 4 (id=44bd17a6473e3202, size=995 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=BytesRandInsertMutator,ByteInterestingMutator,ByteNegMutator,BytesDeleteMutator,ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=48971009bb3fc9d1, size=997 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=BytesInsertCopyMutator,ByteInterestingMutator,WordInterestingMutator,TokenReplace,BytesRandSetMutator,TokenReplace,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=94c47bff5687a0c9, size=8759 bytes, fuzzer=naive, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=3258b36fd9493cdb, size=8759 bytes, fuzzer=naive, trial=1, discovered_at=2s, mutation_op=QwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=cb279748c12908a9, size=863 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=BytesSetMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=2824e1c4bb6d0c25, size=868 bytes, fuzzer=naive, trial=1, discovered_at=25s, mutation_op=BytesInsertCopyMutator,ByteIncMutator,BitFlipMutator,BitFlipMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=012870f9afb207c8, size=8759 bytes, fuzzer=value_profile, trial=1, discovered_at=65s, mutation_op=TokenReplace,ByteFlipMutator,WordInterestingMutator,ByteFlipMutator,ByteNegMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 01 08 06 00 00 01 52 ed aa   ...[.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x23                            00(.)x24 02(.)x1                    PARTIAL
   0x0013  5b([)x21 02(.)x1 07(.)x1            5b([)x25                            PARTIAL
   0x0017  45(E)x21 0b(.)x2                    45(E)x23 01(.)x2                    PARTIAL
   0x0018  08(.)x21 02(.)x1 04(.)x1            08(.)x25                            PARTIAL
   0x0019  06(.)x20 00(.)x2 03(.)x1            06(.)x25                            PARTIAL
   0x001e  ed(.)x22 80(.)x1                    ed(.)x25                            PARTIAL
   0x0025  67(g)x22 7a(z)x1                    67(g)x25                            PARTIAL
   0x0026  41(A)x22 54(T)x1                    41(A)x25                            PARTIAL
   0x0027  4d(M)x22 58(X)x1                    4d(M)x25                            PARTIAL
   0x0028  41(A)x22 74(t)x1                    41(A)x25                            PARTIAL
   0x0029  00(.)x23                            00(.)x19 80(.)x6                    PARTIAL
   0x002a  00(.)x22 86(.)x1                    00(.)x25                            PARTIAL
   0x002b  b1(.)x22 86(.)x1                    b1(.)x25                            PARTIAL
   0x002c  8f(.)x22 86(.)x1                    8f(.)x25                            PARTIAL
   0x002d  0b(.)x22 86(.)x1                    0b(.)x25                            PARTIAL
   0x002e  fc(.)x22 86(.)x1                    fc(.)x25                            PARTIAL
   0x002f  61(a)x14 00(.)x8 86(.)x1            61(a)x25                            PARTIAL
   0x0030  05(.)x22 86(.)x1                    05(.)x25                            PARTIAL
   0x0035  73(s)x17 74(t)x3 68(h)x2 70(p)x1    73(s)x25                            PARTIAL
   0x0036  52(R)x18 49(I)x3 50(P)x1 43(C)x1    52(R)x25                            PARTIAL
   0x0037  47(G)x16 4e(N)x2 53(S)x2 4c(L)x1 +2u  47(G)x25                            PARTIAL
   0x0038  42(B)x16 54(T)x3 53(S)x2 45(E)x1 +1u  42(B)x13 54(T)x12                   PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_4006.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4006,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4006 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4006 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4006 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).