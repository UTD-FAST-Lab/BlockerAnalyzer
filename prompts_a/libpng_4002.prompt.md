==== BLOCKER ====
Target: libpng
Branch ID: 4002
Location: /src/libpng/pngrutil.c:2018:14
Enclosing function: OSS_FUZZ_png_handle_bKGD
Source line:          if (buf[0] != 0 || buf[2] != 0 || buf[4] != 0)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            9        1          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             4        6          0  REFERENCE
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                     5        5          0  REFERENCE
mopt                             9        1          0  REFERENCE
minimizer                        8        2          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.40h  loser=24.00h
  avg hitcount on branch: winner=18  loser=0
  prob_div=0.90  dur_div=19.60h  hit_div=18
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/4002/{W,L}/branch_coverage_show.txt

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
[B]  1932         (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE &&
[B]  1933         (png_ptr->mode & PNG_HAVE_PLTE) == 0))
[ ]  1934     {
[ ]  1935        png_crc_finish(png_ptr, length);
[ ]  1936        png_chunk_benign_error(png_ptr, "out of place");
[ ]  1937        return;
[ ]  1938     }
[ ]  1939  
[B]  1940     else if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_bKGD) != 0)
[L]  1941     {
[L]  1942        png_crc_finish(png_ptr, length);
[L]  1943        png_chunk_benign_error(png_ptr, "duplicate");
[L]  1944        return;
[L]  1945     }
[ ]  1946  
[B]  1947     if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
[ ]  1948        truelen = 1;
[ ]  1949  
[B]  1950     else if ((png_ptr->color_type & PNG_COLOR_MASK_COLOR) != 0)
[B]  1951        truelen = 6;
[ ]  1952  
[ ]  1953     else
[ ]  1954        truelen = 2;
[ ]  1955  
[B]  1956     if (length != truelen)
[ ]  1957     {
[ ]  1958        png_crc_finish(png_ptr, length);
[ ]  1959        png_chunk_benign_error(png_ptr, "invalid");
[ ]  1960        return;
[ ]  1961     }
[ ]  1962  
[B]  1963     png_crc_read(png_ptr, buf, truelen);
[ ]  1964  
[B]  1965     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  1966        return;
[ ]  1967  
[ ]  1968     /* We convert the index value into RGB components so that we can allow
[ ]  1969      * arbitrary RGB values for background when we have transparency, and
[ ]  1970      * so it is easy to determine the RGB values of the background color
[ ]  1971      * from the info_ptr struct.
[ ]  1972      */
[B]  1973     if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
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
[B]  1996     else if ((png_ptr->color_type & PNG_COLOR_MASK_COLOR) == 0) /* GRAY */
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
[B]  2014     else
[B]  2015     {
[B]  2016        if (png_ptr->bit_depth <= 8)
[B]  2017        {
[B]  2018           if (buf[0] != 0 || buf[2] != 0 || buf[4] != 0) <-- BLOCKER
[W]  2019           {
[W]  2020              png_chunk_benign_error(png_ptr, "invalid color");
[W]  2021              return;
[W]  2022           }
[B]  2023        }
[ ]  2024  
[B]  2025        background.index = 0;
[B]  2026        background.red = png_get_uint_16(buf);
[B]  2027        background.green = png_get_uint_16(buf + 2);
[B]  2028        background.blue = png_get_uint_16(buf + 4);
[B]  2029        background.gray = 0;
[B]  2030     }
[ ]  2031  
[B]  2032     png_set_bKGD(png_ptr, info_ptr, &background);
[B]  2033  }

--- No 1-hop callers of OSS_FUZZ_png_handle_bKGD fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0      3960  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
       0      1040  OSS_FUZZ_png_zlib_inflate  (/src/libpng/pngrutil.c:454-467)
       0      1040  OSS_FUZZ_png_read_IDAT_data  (/src/libpng/pngrutil.c:4152-4276)
       0      1030  OSS_FUZZ_png_combine_row  (/src/libpng/pngrutil.c:3202-3681)
       0       854  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
       0       797  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
     136       608  OSS_FUZZ_png_crc_read  (/src/libpng/pngrutil.c:197-203)
       0       428  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
       0       245  pngrutil.c:png_read_filter_row_paeth_multibyte_pixel  (/src/libpng/pngrutil.c:4046-4092)
       0       110  pngrutil.c:png_read_filter_row_sub  (/src/libpng/pngrutil.c:3934-3947)
       0        71  pngrutil.c:png_read_filter_row_avg  (/src/libpng/pngrutil.c:3968-3990)
      32       101  pngrutil.c:png_read_buffer  (/src/libpng/pngrutil.c:299-332)
       6        34  OSS_FUZZ_png_handle_gAMA  (/src/libpng/pngrutil.c:1120-1152)
      11        34  OSS_FUZZ_png_handle_sRGB  (/src/libpng/pngrutil.c:1312-1356)
       2        18  OSS_FUZZ_png_handle_tEXt  (/src/libpng/pngrutil.c:2517-2591)
... (17 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_bKGD  (/src/libpng/pngrutil.c:1921-2033) ---
  d=1   L1940  T=0 F=14  T=5 F=19  else if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_...
  d=1   L2018  T=0 F=1  T=0 F=19  if (buf[0] != 0 || buf[2] != 0 || buf[4] != 0)  <-- BLOCKER
  d=1   L2018  T=0 F=1  T=0 F=19  if (buf[0] != 0 || buf[2] != 0 || buf[4] != 0)  <-- BLOCKER
  d=1   L2018  T=13 F=1  T=0 F=19  if (buf[0] != 0 || buf[2] != 0 || buf[4] != 0)  <-- BLOCKER

[off-chain: 295 additional divergent branches across 41 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=1f9d86858027e780, size=789 bytes, fuzzer=naive, trial=2, discovered_at=18s, mutation_op=ByteAddMutator,WordAddMutator,CrossoverReplaceMutator,ByteNegMutator,BytesExpandMutator,BytesRandSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=2acffb97d54aac8c, size=793 bytes, fuzzer=naive, trial=2, discovered_at=18s, mutation_op=ByteAddMutator,BytesInsertMutator,BytesInsertCopyMutator,BytesSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=0bb164c831b2787d, size=793 bytes, fuzzer=naive, trial=2, discovered_at=19s, mutation_op=ByteInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=2d6812871c8a6ced, size=579 bytes, fuzzer=naive, trial=2, discovered_at=19s, mutation_op=ByteAddMutator,ByteNegMutator,BytesInsertCopyMutator,TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: d8 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=0dcf60057526c12e, size=375 bytes, fuzzer=naive, trial=2, discovered_at=22s, mutation_op=BytesDeleteMutator,TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

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
Seed 4 (id=1ae8421144d1b23e, size=995 bytes, fuzzer=cmplog, trial=1, discovered_at=2s, mutation_op=BytesRandSetMutator,ByteFlipMutator,ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=1b93bc794e9358c8, size=8360 bytes, fuzzer=cmplog, trial=1, discovered_at=3s, mutation_op=BytesDeleteMutator,BitFlipMutator,QwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 00 00 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x001c  01(.)x10                            01(.)x18 00(.)x1                    PARTIAL
   0x001d  52(R)x6 ad(.)x4                     52(R)x19                            PARTIAL
   0x0020  e4(.)x9 d8(.)x1                     e4(.)x19                            PARTIAL
   0x0024  04(.)x6 12(.)x4                     04(.)x19                            PARTIAL
   0x0025  67(g)x6 73(s)x4                     67(g)x18 74(t)x1                    PARTIAL
   0x0026  41(A)x6 43(C)x4                     41(A)x18 45(E)x1                    PARTIAL
   0x0027  4d(M)x6 41(A)x4                     4d(M)x18 58(X)x1                    PARTIAL
   0x0028  41(A)x6 4c(L)x4                     41(A)x18 74(t)x1                    PARTIAL
   0x0029  00(.)x6 01(.)x4                     00(.)x19                            PARTIAL
   0x002a  00(.)x6 89(.)x4                     00(.)x19                            PARTIAL
   0x002b  b1(.)x6 50(P)x4                     b1(.)x18 00(.)x1                    PARTIAL
   0x002c  8f(.)x6 4e(N)x4                     8f(.)x18 00(.)x1                    PARTIAL
   0x002d  0b(.)x6 47(G)x4                     0b(.)x19                            PARTIAL
   0x002e  fc(.)x6 0d(.)x3 00(.)x1             fc(.)x19                            PARTIAL
   0x002f  61(a)x6 0a(.)x3 00(.)x1             61(a)x18 62(b)x1                    PARTIAL
   0x0030  05(.)x6 1a(.)x3 00(.)x1             05(.)x19                            PARTIAL
   0x0031  00(.)x9 ff(.)x1                     00(.)x19                            PARTIAL
   0x0032  00(.)x7 04(.)x3                     00(.)x19                            PARTIAL
   0x0033  00(.)x7 67(g)x3                     00(.)x19                            PARTIAL
   0x0034  01(.)x6 41(A)x3 00(.)x1             01(.)x19                            PARTIAL
   0x0035  73(s)x6 4d(M)x3 0d(.)x1             73(s)x19                            PARTIAL
   0x0036  52(R)x6 41(A)x3 49(I)x1             52(R)x19                            PARTIAL
   0x0037  47(G)x6 00(.)x3 48(H)x1             47(G)x19                            PARTIAL
   0x0038  42(B)x6 00(.)x3 44(D)x1             42(B)x19                            PARTIAL
   0x0039  01(.)x6 b1(.)x3 52(R)x1             01(.)x19                            PARTIAL
   0x003a  d9(.)x6 8f(.)x3 00(.)x1             d9(.)x19                            PARTIAL
   0x003b  c9(.)x6 0b(.)x3 6b(k)x1             c9(.)x19                            PARTIAL
   0x003c  2c(,)x6 fc(.)x3 a8(.)x1             2c(,)x19                            PARTIAL
   0x003d  7f(.)x6 61(a)x3 da(.)x1             7f(.)x19                            PARTIAL
   0x003e  00(.)x6 05(.)x3 20( )x1             00(.)x19                            PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_4002.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4002,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4002 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4002 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4002 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).