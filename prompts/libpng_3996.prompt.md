==== BLOCKER ====
Target: libpng
Branch ID: 3996
Location: /src/libpng/pngrutil.c:1932:9
Enclosing function: OSS_FUZZ_png_handle_bKGD
Source line:        (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog); loser (ctx_coverage vs naive_ctx); loser (value_profile vs value_profile)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     3        7          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'naive_ctx', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (3) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=1.00h  loser=21.60h
  avg hitcount on branch: winner=98  loser=0
  prob_div=0.90  dur_div=20.60h  hit_div=98
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002
--- Pair 2: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 25  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=2.00h  loser=21.60h
  avg hitcount on branch: winner=65  loser=0
  prob_div=0.90  dur_div=19.60h  hit_div=65
  subject-level: delta_AUC=6413040.0  p_AUC=0.0003  delta_Final=91.4  p_final=0.0002
--- Pair 3: value_profile > naive  [delta: value_profile] ---
  subject 22  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=8.60h  loser=21.60h
  avg hitcount on branch: winner=64  loser=0
  prob_div=0.70  dur_div=13.00h  hit_div=64
  subject-level: delta_AUC=16855020.0  p_AUC=0.0002  delta_Final=254.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3996/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_bKGD (/src/libpng/pngrutil.c:1921-2033) ---
[ ]  1919  void /* PRIVATE */
[ ]  1920  png_handle_bKGD(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  1921  {
[B]  1922     unsigned int truelen;
[B]  1923     png_byte buf[6];
[B]  1924     png_color_16 background;
[ ]  1925  
[B]  1926     png_debug(1, "in png_handle_bKGD");
[ ]  1927  
[B]  1928     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  1929        png_chunk_error(png_ptr, "missing IHDR");
[ ]  1930  
[B]  1931     else if ((png_ptr->mode & PNG_HAVE_IDAT) != 0 ||
[B]  1932         (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE && <-- BLOCKER
[B]  1933         (png_ptr->mode & PNG_HAVE_PLTE) == 0))
[W]  1934     {
[W]  1935        png_crc_finish(png_ptr, length);
[W]  1936        png_chunk_benign_error(png_ptr, "out of place");
[W]  1937        return;
[W]  1938     }
[ ]  1939  
[B]  1940     else if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_bKGD) != 0)
[L]  1941     {
[L]  1942        png_crc_finish(png_ptr, length);
[L]  1943        png_chunk_benign_error(png_ptr, "duplicate");
[L]  1944        return;
[L]  1945     }
[ ]  1946  
[B]  1947     if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
[W]  1948        truelen = 1;
[ ]  1949  
[L]  1950     else if ((png_ptr->color_type & PNG_COLOR_MASK_COLOR) != 0)
[L]  1951        truelen = 6;
[ ]  1952  
[L]  1953     else
[L]  1954        truelen = 2;
[ ]  1955  
[B]  1956     if (length != truelen)
[B]  1957     {
[B]  1958        png_crc_finish(png_ptr, length);
[B]  1959        png_chunk_benign_error(png_ptr, "invalid");
[B]  1960        return;
[B]  1961     }
[ ]  1962  
[L]  1963     png_crc_read(png_ptr, buf, truelen);
[ ]  1964  
[L]  1965     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  1966        return;
[ ]  1967  
[ ]  1968     /* We convert the index value into RGB components so that we can allow
[ ]  1969      * arbitrary RGB values for background when we have transparency, and
[ ]  1970      * so it is easy to determine the RGB values of the background color
[ ]  1971      * from the info_ptr struct.
[ ]  1972      */
[L]  1973     if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
[ ]  1974     {
[ ]  1975        background.index = buf[0];
[ ]  1976  
[ ]  1977        if (info_ptr != NULL && info_ptr->num_palette != 0)
[ ]  1978        {
[ ]  1979           if (buf[0] >= info_ptr->num_palette)
[ ]  1980           {
[ ]  1981              png_chunk_benign_error(png_ptr, "invalid index");
[ ]  1982              return;
[ ]  1983           }
[ ]  1984  
[ ]  1985           background.red = (png_uint_16)png_ptr->palette[buf[0]].red;
[ ]  1986           background.green = (png_uint_16)png_ptr->palette[buf[0]].green;
[ ]  1987           background.blue = (png_uint_16)png_ptr->palette[buf[0]].blue;
[ ]  1988        }
[ ]  1989  
[ ]  1990        else
[ ]  1991           background.red = background.green = background.blue = 0;
[ ]  1992  
[ ]  1993        background.gray = 0;
[ ]  1994     }
[ ]  1995  
[L]  1996     else if ((png_ptr->color_type & PNG_COLOR_MASK_COLOR) == 0) /* GRAY */
[ ]  1997     {
[ ]  1998        if (png_ptr->bit_depth <= 8)
[ ]  1999        {
[ ]  2000           if (buf[0] != 0 || buf[1] >= (unsigned int)(1 << png_ptr->bit_depth))
[ ]  2001           {
[ ]  2002              png_chunk_benign_error(png_ptr, "invalid gray level");
[ ]  2003              return;
[ ]  2004           }
[ ]  2005        }
[ ]  2006  
[ ]  2007        background.index = 0;
[ ]  2008        background.red =
[ ]  2009        background.green =
[ ]  2010        background.blue =
[ ]  2011        background.gray = png_get_uint_16(buf);
[ ]  2012     }
[ ]  2013  
[L]  2014     else
[L]  2015     {
[L]  2016        if (png_ptr->bit_depth <= 8)
[L]  2017        {
[L]  2018           if (buf[0] != 0 || buf[2] != 0 || buf[4] != 0)
[ ]  2019           {
[ ]  2020              png_chunk_benign_error(png_ptr, "invalid color");
[ ]  2021              return;
[ ]  2022           }
[L]  2023        }
[ ]  2024  
[L]  2025        background.index = 0;
[L]  2026        background.red = png_get_uint_16(buf);
[L]  2027        background.green = png_get_uint_16(buf + 2);
[L]  2028        background.blue = png_get_uint_16(buf + 4);
[L]  2029        background.gray = 0;
[L]  2030     }
[ ]  2031  
[L]  2032     png_set_bKGD(png_ptr, info_ptr, &background);
[L]  2033  }

--- No 1-hop callers of OSS_FUZZ_png_handle_bKGD fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     899         0  pngrutil.c:png_read_filter_row_avg  (/src/libpng/pngrutil.c:3968-3990)
     854       212  OSS_FUZZ_png_crc_read  (/src/libpng/pngrutil.c:197-203)
      49       336  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
     123        40  pngrutil.c:png_read_buffer  (/src/libpng/pngrutil.c:299-332)
      80         0  pngrutil.c:png_read_filter_row_paeth_1byte_pixel  (/src/libpng/pngrutil.c:3995-4041)
       6        57  pngrutil.c:png_read_filter_row_sub  (/src/libpng/pngrutil.c:3934-3947)
      19         0  OSS_FUZZ_png_handle_PLTE  (/src/libpng/pngrutil.c:913-1096)
      23         4  OSS_FUZZ_png_handle_pHYs  (/src/libpng/pngrutil.c:2156-2196)
      19         4  OSS_FUZZ_png_handle_tEXt  (/src/libpng/pngrutil.c:2517-2591)
      14         0  OSS_FUZZ_png_handle_zTXt  (/src/libpng/pngrutil.c:2598-2708)
      19         6  pngrutil.c:png_inflate_claim  (/src/libpng/pngrutil.c:342-443)
      19         6  OSS_FUZZ_png_read_start_row  (/src/libpng/pngrutil.c:4393-4680)
      13         4  pngrutil.c:png_init_filter_functions  (/src/libpng/pngrutil.c:4105-4129)
       8         2  OSS_FUZZ_png_handle_tIME  (/src/libpng/pngrutil.c:2471-2510)
       0         4  OSS_FUZZ_png_read_finish_IDAT  (/src/libpng/pngrutil.c:4280-4324)
... (2 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_bKGD  (/src/libpng/pngrutil.c:1921-2033) ---
  d=1   L1928  T=0 F=55  T=0 F=20  if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
  d=1   L1931  T=0 F=55  T=0 F=20  else if ((png_ptr->mode & PNG_HAVE_IDAT) != 0 ||
  d=1   L1932  T=55 F=0  T=0 F=20  (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE &&  <-- BLOCKER
  d=1   L1933  T=38 F=17  T=0 F=0  (png_ptr->mode & PNG_HAVE_PLTE) == 0))
  d=1   L1940  T=0 F=17  T=3 F=17  else if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_...
  d=1   L1947  T=17 F=0  T=0 F=17  if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
  d=1   L1950  T=0 F=0  T=5 F=12  else if ((png_ptr->color_type & PNG_COLOR_MASK_COLOR) != 0)
  d=1   L1956  T=17 F=0  T=12 F=5  if (length != truelen)
  d=1   L1965  T=0 F=0  T=0 F=5  if (png_crc_finish(png_ptr, 0) != 0)
  d=1   L1973  T=0 F=0  T=0 F=5  if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
  d=1   L1996  T=0 F=0  T=0 F=5  else if ((png_ptr->color_type & PNG_COLOR_MASK_COLOR) == ...
  d=1   L2016  T=0 F=0  T=5 F=0  if (png_ptr->bit_depth <= 8)
  d=1   L2018  T=0 F=0  T=0 F=5  if (buf[0] != 0 || buf[2] != 0 || buf[4] != 0)
  d=1   L2018  T=0 F=0  T=0 F=5  if (buf[0] != 0 || buf[2] != 0 || buf[4] != 0)
  d=1   L2018  T=0 F=0  T=0 F=5  if (buf[0] != 0 || buf[2] != 0 || buf[4] != 0)

[off-chain: 284 additional divergent branches across 38 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0598f1586c91784d, size=4276 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2f 7f 00 00   .....sRGB.../...
Seed 2 (id=22b61b5af3906383, size=3134 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=240dfbd337403f4a, size=4440 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2f 7f 00 00   .....sRGB.../...
Seed 4 (id=295db9e000239adc, size=2824 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed 55   ...[...E.....R.U
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2f 7f 00 00   .....sRGB.../...
Seed 5 (id=6caa491800dda4fa, size=3134 bytes, fuzzer=naive_ctx, trial=1):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00140bdb0aa48f31, size=2316 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator,CrossoverReplaceMutator,TokenInsert,DwordInterestingMutator,BytesExpandMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=0c62bbbc6c78b27e, size=547 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=WordInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 74 52 47 42 01 d9 c9 2c 7f 00 00   .....tRGB...,...
Seed 3 (id=03e0698c9a66f143, size=974 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=TokenReplace,BytesCopyMutator,BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 a0 86 01 00 00 00 01 52 ed aa   ...[.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 ff d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=04d321e22275fc78, size=1165 bytes, fuzzer=naive, trial=1, discovered_at=101s, mutation_op=ByteDecMutator,WordInterestingMutator,DwordAddMutator,BytesCopyMutator,ByteNegMutator,BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=0a877a7991153d24, size=9892 bytes, fuzzer=naive, trial=1, discovered_at=1831s, mutation_op=ByteIncMutator,BytesDeleteMutator,WordInterestingMutator,ByteAddMutator,ByteInterestingMutator,WordAddMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 23 00 00 00 01 08 06 00 00 01 52 ed aa   ...#.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x32 01(.)x1 10(.)x1            00(.)x14                            PARTIAL
   0x0015  00(.)x30 04(.)x2 01(.)x1 02(.)x1    00(.)x14                            PARTIAL
   0x0016  00(.)x31 0a(.)x1 01(.)x1 e8(.)x1    00(.)x7 a0(.)x4 01(.)x2 1d(.)x1     PARTIAL
   0x0017  45(E)x32 25(%)x1 ba(.)x1            45(E)x8 86(.)x4 01(.)x1 00(.)x1     PARTIAL
   0x0018  08(.)x21 02(.)x8 04(.)x3 01(.)x2    08(.)x10 01(.)x4                    PARTIAL
   0x0019  03(.)x34                            06(.)x5 04(.)x5 00(.)x4             DIFFER
   0x001d  52(R)x34                            52(R)x12 ff(.)x2                    PARTIAL
   0x001f  aa(.)x32 55(U)x2                    aa(.)x14                            PARTIAL
   0x0025  67(g)x32 69(i)x2                    67(g)x14                            PARTIAL
   0x0026  41(A)x32 54(T)x2                    41(A)x14                            PARTIAL
   0x0027  4d(M)x19 6d(m)x13 58(X)x2           4d(M)x14                            PARTIAL
   0x0028  41(A)x32 74(t)x2                    41(A)x14                            PARTIAL
   0x0029  00(.)x34                            00(.)x13 80(.)x1                    PARTIAL
   0x002a  00(.)x33 c2(.)x1                    00(.)x14                            PARTIAL
   0x002b  b1(.)x21 00(.)x13                   b1(.)x14                            PARTIAL
   0x002c  8f(.)x21 00(.)x13                   8f(.)x14                            PARTIAL
   0x002d  0b(.)x21 00(.)x13                   0b(.)x14                            PARTIAL
   0x002e  fc(.)x21 00(.)x13                   fc(.)x14                            PARTIAL
   0x002f  61(a)x21 00(.)x13                   61(a)x14                            PARTIAL
   0x0030  05(.)x21 00(.)x13                   05(.)x14                            PARTIAL
   0x0034  01(.)x21 ff(.)x13                   01(.)x14                            PARTIAL
   0x0035  73(s)x21 50(P)x13                   73(s)x13 74(t)x1                    PARTIAL
   0x0036  52(R)x21 4c(L)x13                   52(R)x14                            PARTIAL
   0x0037  47(G)x21 54(T)x13                   47(G)x14                            PARTIAL
   0x0038  42(B)x21 45(E)x13                   42(B)x14                            PARTIAL
   0x0039  01(.)x21 52(R)x13                   01(.)x13 ff(.)x1                    PARTIAL
   0x003a  d9(.)x21 01(.)x13                   d9(.)x14                            PARTIAL
   0x003b  c9(.)x21 76(v)x13                   c9(.)x14                            PARTIAL
   0x003c  2c(,)x15 76(v)x13 2f(/)x6           2c(,)x14                            PARTIAL
   0x003d  7f(.)x21 18(.)x13                   7f(.)x14                            PARTIAL
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libpng_3996.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3996,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), naive_ctx>naive (ctx_coverage), value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3996 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3996 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3996 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).