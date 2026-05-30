==== BLOCKER ====
Target: libpng
Branch ID: 3974
Location: /src/libpng/pngrutil.c:1280:8
Enclosing function: OSS_FUZZ_png_handle_cHRM
Source line:        xy.redy   == PNG_FIXED_ERROR ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            9        1          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive); loser (value_profile vs value_profile_cmplog)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                    10        0          0  REFERENCE
mopt                            10        0          0  REFERENCE
minimizer                        8        2          0  REFERENCE
fast                            10        0          0  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=3.70h  loser=22.30h
  avg hitcount on branch: winner=11  loser=0
  prob_div=0.80  dur_div=18.60h  hit_div=11
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 23  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=11.10h  loser=22.30h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.70  dur_div=11.20h  hit_div=3
  subject-level: delta_AUC=7265340.0  p_AUC=0.0003  delta_Final=83.1  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3974/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_cHRM (/src/libpng/pngrutil.c:1240-1306) ---
[ ]  1238  void /* PRIVATE */
[ ]  1239  png_handle_cHRM(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  1240  {
[B]  1241     png_byte buf[32];
[B]  1242     png_xy xy;
[ ]  1243  
[B]  1244     png_debug(1, "in png_handle_cHRM");
[ ]  1245  
[B]  1246     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  1247        png_chunk_error(png_ptr, "missing IHDR");
[ ]  1248  
[B]  1249     else if ((png_ptr->mode & (PNG_HAVE_IDAT|PNG_HAVE_PLTE)) != 0)
[B]  1250     {
[B]  1251        png_crc_finish(png_ptr, length);
[B]  1252        png_chunk_benign_error(png_ptr, "out of place");
[B]  1253        return;
[B]  1254     }
[ ]  1255  
[B]  1256     if (length != 32)
[W]  1257     {
[W]  1258        png_crc_finish(png_ptr, length);
[W]  1259        png_chunk_benign_error(png_ptr, "invalid");
[W]  1260        return;
[W]  1261     }
[ ]  1262  
[B]  1263     png_crc_read(png_ptr, buf, 32);
[ ]  1264  
[B]  1265     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  1266        return;
[ ]  1267  
[B]  1268     xy.whitex = png_get_fixed_point(NULL, buf);
[B]  1269     xy.whitey = png_get_fixed_point(NULL, buf + 4);
[B]  1270     xy.redx   = png_get_fixed_point(NULL, buf + 8);
[B]  1271     xy.redy   = png_get_fixed_point(NULL, buf + 12);
[B]  1272     xy.greenx = png_get_fixed_point(NULL, buf + 16);
[B]  1273     xy.greeny = png_get_fixed_point(NULL, buf + 20);
[B]  1274     xy.bluex  = png_get_fixed_point(NULL, buf + 24);
[B]  1275     xy.bluey  = png_get_fixed_point(NULL, buf + 28);
[ ]  1276  
[B]  1277     if (xy.whitex == PNG_FIXED_ERROR ||
[B]  1278         xy.whitey == PNG_FIXED_ERROR ||
[B]  1279         xy.redx   == PNG_FIXED_ERROR ||
[B]  1280         xy.redy   == PNG_FIXED_ERROR || <-- BLOCKER
[B]  1281         xy.greenx == PNG_FIXED_ERROR ||
[B]  1282         xy.greeny == PNG_FIXED_ERROR ||
[B]  1283         xy.bluex  == PNG_FIXED_ERROR ||
[B]  1284         xy.bluey  == PNG_FIXED_ERROR)
[B]  1285     {
[B]  1286        png_chunk_benign_error(png_ptr, "invalid values");
[B]  1287        return;
[B]  1288     }
[ ]  1289  
[ ]  1290     /* If a colorspace error has already been output skip this chunk */
[B]  1291     if ((png_ptr->colorspace.flags & PNG_COLORSPACE_INVALID) != 0)
[B]  1292        return;
[ ]  1293  
[B]  1294     if ((png_ptr->colorspace.flags & PNG_COLORSPACE_FROM_cHRM) != 0)
[ ]  1295     {
[ ]  1296        png_ptr->colorspace.flags |= PNG_COLORSPACE_INVALID;
[ ]  1297        png_colorspace_sync(png_ptr, info_ptr);
[ ]  1298        png_chunk_benign_error(png_ptr, "duplicate");
[ ]  1299        return;
[ ]  1300     }
[ ]  1301  
[B]  1302     png_ptr->colorspace.flags |= PNG_COLORSPACE_FROM_cHRM;
[B]  1303     (void)png_colorspace_set_chromaticities(png_ptr, &png_ptr->colorspace, &xy,
[B]  1304         1/*prefer cHRM values*/);
[B]  1305     png_colorspace_sync(png_ptr, info_ptr);
[B]  1306  }

--- No 1-hop callers of OSS_FUZZ_png_handle_cHRM fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0      1860  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
       1       666  OSS_FUZZ_png_read_IDAT_data  (/src/libpng/pngrutil.c:4152-4276)
       1       665  OSS_FUZZ_png_zlib_inflate  (/src/libpng/pngrutil.c:454-467)
       0       661  OSS_FUZZ_png_combine_row  (/src/libpng/pngrutil.c:3202-3681)
       0       385  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
       0       313  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
       0       163  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
       0       104  pngrutil.c:png_read_filter_row_paeth_multibyte_pixel  (/src/libpng/pngrutil.c:4046-4092)
       0        70  pngrutil.c:png_read_filter_row_sub  (/src/libpng/pngrutil.c:3934-3947)
       0        48  pngrutil.c:png_read_filter_row_avg  (/src/libpng/pngrutil.c:3968-3990)
      64        20  OSS_FUZZ_png_handle_cHRM  (/src/libpng/pngrutil.c:1240-1306)  <-- enclosing
      48         5  OSS_FUZZ_png_handle_iCCP  (/src/libpng/pngrutil.c:1363-1634)
      60        19  OSS_FUZZ_png_handle_sBIT  (/src/libpng/pngrutil.c:1158-1234)
      45         9  OSS_FUZZ_png_handle_bKGD  (/src/libpng/pngrutil.c:1921-2033)
       0        12  OSS_FUZZ_png_handle_tEXt  (/src/libpng/pngrutil.c:2517-2591)
... (12 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_cHRM  (/src/libpng/pngrutil.c:1240-1306) ---
  d=1   L1246  T=0 F=64  T=0 F=20  if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
  d=1   L1249  T=4 F=60  T=1 F=19  else if ((png_ptr->mode & (PNG_HAVE_IDAT|PNG_HAVE_PLTE)) ...
  d=1   L1256  T=2 F=58  T=0 F=19  if (length != 32)
  d=1   L1265  T=0 F=58  T=0 F=19  if (png_crc_finish(png_ptr, 0) != 0)
  d=1   L1277  T=0 F=58  T=0 F=19  if (xy.whitex == PNG_FIXED_ERROR ||
  d=1   L1278  T=1 F=57  T=0 F=19  xy.whitey == PNG_FIXED_ERROR ||
  d=1   L1279  T=0 F=57  T=0 F=19  xy.redx   == PNG_FIXED_ERROR ||
  d=1   L1280  T=12 F=45  T=0 F=19  xy.redy   == PNG_FIXED_ERROR ||  <-- BLOCKER
  d=1   L1281  T=0 F=45  T=0 F=19  xy.greenx == PNG_FIXED_ERROR ||
  d=1   L1282  T=0 F=45  T=1 F=18  xy.greeny == PNG_FIXED_ERROR ||
  d=1   L1283  T=5 F=40  T=0 F=18  xy.bluex  == PNG_FIXED_ERROR ||
  d=1   L1284  T=0 F=40  T=0 F=18  xy.bluey  == PNG_FIXED_ERROR)
  d=1   L1291  T=29 F=11  T=2 F=16  if ((png_ptr->colorspace.flags & PNG_COLORSPACE_INVALID) ...

[off-chain: 263 additional divergent branches across 37 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=a41c948a968f79b4, size=1314 bytes, fuzzer=naive, trial=1, discovered_at=6108s, mutation_op=BytesDeleteMutator,TokenReplace,CrossoverReplaceMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 a0 86 01 00 00 00 01 52 ed aa   ...[.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=745346269ce74b2d, size=656 bytes, fuzzer=naive, trial=1, discovered_at=10113s, mutation_op=BytesInsertMutator,BitFlipMutator,BitFlipMutator,TokenInsert,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 a0 86 01 00 00 00 01 52 ed aa   ...[.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=b0fbbcd361299441, size=1235 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=62508s, mutation_op=QwordAddMutator,TokenReplace,ByteRandMutator,BytesRandSetMutator,DwordAddMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 43 43 50 01 d9 c9 2c 7f 00 00   .....iCCP...,...
Seed 4 (id=5553c5a241320f12, size=1235 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=68833s, mutation_op=WordAddMutator,BytesCopyMutator,ByteNegMutator,ByteInterestingMutator,BytesRandSetMutator,BytesSetMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 43 43 50 01 d9 c9 2c 7f 00 00   .....iCCP...,...
Seed 5 (id=a165f6e636b365ae, size=1235 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=69708s, mutation_op=BytesRandInsertMutator,ByteAddMutator,BytesDeleteMutator,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 43 43 50 01 d9 c9 2c 7f 00 00   .....iCCP...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00b32983a52ab23e, size=8759 bytes, fuzzer=cmplog, trial=1, discovered_at=0s):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=00dc0e5d945bd23b, size=8771 bytes, fuzzer=cmplog, trial=1, discovered_at=0s, mutation_op=ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=120d590179fa22e6, size=8759 bytes, fuzzer=cmplog, trial=2, discovered_at=0s, mutation_op=BytesExpandMutator,BytesSetMutator,ByteRandMutator,TokenInsert,WordInterestingMutator,ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=013b9f2a08a04135, size=738 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=DwordInterestingMutator,BytesDeleteMutator,QwordAddMutator,ByteInterestingMutator,ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 82 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=f7f3f3f62ab65740, size=4902 bytes, fuzzer=cmplog, trial=2, discovered_at=5s, mutation_op=ByteIncMutator,WordAddMutator,TokenReplace,ByteNegMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0013  5b([)x12                            5b([)x15 02(.)x1 07(.)x1            PARTIAL
   0x0015  00(.)x12                            00(.)x16 0f(.)x1                    PARTIAL
   0x0016  00(.)x10 a0(.)x2                    00(.)x16 42(B)x1                    PARTIAL
   0x0017  45(E)x10 86(.)x2                    45(E)x15 40(@)x1 bb(.)x1            PARTIAL
   0x0019  06(.)x10 00(.)x2                    06(.)x15 02(.)x1 00(.)x1            PARTIAL
   0x001c  01(.)x12                            01(.)x13 00(.)x4                    PARTIAL
   0x001d  52(R)x12                            52(R)x16 d9(.)x1                    PARTIAL
   0x001e  ed(.)x12                            ed(.)x16 c9(.)x1                    PARTIAL
   0x001f  aa(.)x12                            aa(.)x16 2c(,)x1                    PARTIAL
   0x0020  e4(.)x12                            e4(.)x16 7f(.)x1                    PARTIAL
   0x0025  67(g)x12                            67(g)x16 73(s)x1                    PARTIAL
   0x0026  41(A)x12                            41(A)x16 42(B)x1                    PARTIAL
   0x0027  4d(M)x12                            4d(M)x16 49(I)x1                    PARTIAL
   0x0028  41(A)x12                            41(A)x16 54(T)x1                    PARTIAL
   0x0029  00(.)x12                            00(.)x16 05(.)x1                    PARTIAL
   0x002a  00(.)x12                            00(.)x16 05(.)x1                    PARTIAL
   0x002b  b1(.)x12                            b1(.)x16 05(.)x1                    PARTIAL
   0x002c  8f(.)x12                            8f(.)x15 82(.)x1 05(.)x1            PARTIAL
   0x002d  0b(.)x12                            0b(.)x16 4d(M)x1                    PARTIAL
   0x002e  fc(.)x12                            fc(.)x16 a5(.)x1                    PARTIAL
   0x002f  61(a)x12                            61(a)x12 00(.)x4 2d(-)x1            PARTIAL
   0x0030  05(.)x12                            05(.)x16 f6(.)x1                    PARTIAL
   0x0034  01(.)x12                            01(.)x16 20( )x1                    PARTIAL
   0x0035  69(i)x10 73(s)x2                    73(s)x11 74(t)x4 69(i)x1 63(c)x1    PARTIAL
   0x0036  43(C)x10 52(R)x2                    52(R)x11 45(E)x4 43(C)x1 48(H)x1    PARTIAL
   0x0037  43(C)x10 47(G)x2                    47(G)x11 58(X)x4 43(C)x1 52(R)x1    PARTIAL
   0x0038  50(P)x10 42(B)x2                    42(B)x11 74(t)x4 50(P)x1 4d(M)x1    PARTIAL
   0x0039  01(.)x12                            01(.)x16 00(.)x1                    PARTIAL
   0x003a  d9(.)x12                            d9(.)x16 00(.)x1                    PARTIAL
   0x003b  c9(.)x12                            c9(.)x16 7a(z)x1                    PARTIAL
   0x003c  2c(,)x12                            2c(,)x16 26(&)x1                    PARTIAL
   0x003d  7f(.)x12                            7f(.)x16 00(.)x1                    PARTIAL
   0x003f  00(.)x12                            00(.)x16 80(.)x1                    PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3974.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3974,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3974 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3974 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3974 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).