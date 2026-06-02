==== BLOCKER ====
Target: libpng
Branch ID: 3913
Location: /src/libpng/pngrtran.c:1947:11
Enclosing function: OSS_FUZZ_png_read_transform_info
Source line:       if (info_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.30h  loser=24.00h
  avg hitcount on branch: winner=57  loser=0
  prob_div=0.90  dur_div=20.70h  hit_div=57
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3913/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_read_transform_info (/src/libpng/pngrtran.c:1941-2142) ---
[ ]  1939  void /* PRIVATE */
[ ]  1940  png_read_transform_info(png_structrp png_ptr, png_inforp info_ptr)
[B]  1941  {
[B]  1942     png_debug(1, "in png_read_transform_info");
[ ]  1943  
[B]  1944  #ifdef PNG_READ_EXPAND_SUPPORTED
[B]  1945     if ((png_ptr->transformations & PNG_EXPAND) != 0)
[B]  1946     {
[B]  1947        if (info_ptr->color_type == PNG_COLOR_TYPE_PALETTE) <-- BLOCKER
[W]  1948        {
[ ]  1949           /* This check must match what actually happens in
[ ]  1950            * png_do_expand_palette; if it ever checks the tRNS chunk to see if
[ ]  1951            * it is all opaque we must do the same (at present it does not.)
[ ]  1952            */
[W]  1953           if (png_ptr->num_trans > 0)
[W]  1954              info_ptr->color_type = PNG_COLOR_TYPE_RGB_ALPHA;
[ ]  1955  
[W]  1956           else
[W]  1957              info_ptr->color_type = PNG_COLOR_TYPE_RGB;
[ ]  1958  
[W]  1959           info_ptr->bit_depth = 8;
[W]  1960           info_ptr->num_trans = 0;
[ ]  1961  
[W]  1962           if (png_ptr->palette == NULL)
[ ]  1963              png_error (png_ptr, "Palette is NULL in indexed image");
[W]  1964        }
[L]  1965        else
[L]  1966        {
[L]  1967           if (png_ptr->num_trans != 0)
[ ]  1968           {
[ ]  1969              if ((png_ptr->transformations & PNG_EXPAND_tRNS) != 0)
[ ]  1970                 info_ptr->color_type |= PNG_COLOR_MASK_ALPHA;
[ ]  1971           }
[L]  1972           if (info_ptr->bit_depth < 8)
[L]  1973              info_ptr->bit_depth = 8;
[ ]  1974  
[L]  1975           info_ptr->num_trans = 0;
[L]  1976        }
[B]  1977     }
[B]  1978  #endif
[ ]  1979  
[B]  1980  #if defined(PNG_READ_BACKGROUND_SUPPORTED) ||\
[B]  1981     defined(PNG_READ_ALPHA_MODE_SUPPORTED)
[ ]  1982     /* The following is almost certainly wrong unless the background value is in
[ ]  1983      * the screen space!
[ ]  1984      */
[B]  1985     if ((png_ptr->transformations & PNG_COMPOSE) != 0)
[ ]  1986        info_ptr->background = png_ptr->background;
[B]  1987  #endif
[ ]  1988  
[B]  1989  #ifdef PNG_READ_GAMMA_SUPPORTED
[ ]  1990     /* The following used to be conditional on PNG_GAMMA (prior to 1.5.4),
[ ]  1991      * however it seems that the code in png_init_read_transformations, which has
[ ]  1992      * been called before this from png_read_update_info->png_read_start_row
[ ]  1993      * sometimes does the gamma transform and cancels the flag.
[ ]  1994      *
[ ]  1995      * TODO: this looks wrong; the info_ptr should end up with a gamma equal to
[ ]  1996      * the screen_gamma value.  The following probably results in weirdness if
[ ]  1997      * the info_ptr is used by the app after the rows have been read.
[ ]  1998      */
[B]  1999     info_ptr->colorspace.gamma = png_ptr->colorspace.gamma;
[B]  2000  #endif
[ ]  2001  
[B]  2002     if (info_ptr->bit_depth == 16)
[L]  2003     {
[L]  2004  #  ifdef PNG_READ_16BIT_SUPPORTED
[L]  2005  #     ifdef PNG_READ_SCALE_16_TO_8_SUPPORTED
[L]  2006           if ((png_ptr->transformations & PNG_SCALE_16_TO_8) != 0)
[L]  2007              info_ptr->bit_depth = 8;
[L]  2008  #     endif
[ ]  2009  
[L]  2010  #     ifdef PNG_READ_STRIP_16_TO_8_SUPPORTED
[L]  2011           if ((png_ptr->transformations & PNG_16_TO_8) != 0)
[ ]  2012              info_ptr->bit_depth = 8;
[L]  2013  #     endif
[ ]  2014  
[ ]  2015  #  else
[ ]  2016        /* No 16-bit support: force chopping 16-bit input down to 8, in this case
[ ]  2017         * the app program can chose if both APIs are available by setting the
[ ]  2018         * correct scaling to use.
[ ]  2019         */
[ ]  2020  #     ifdef PNG_READ_STRIP_16_TO_8_SUPPORTED
[ ]  2021           /* For compatibility with previous versions use the strip method by
[ ]  2022            * default.  This code works because if PNG_SCALE_16_TO_8 is already
[ ]  2023            * set the code below will do that in preference to the chop.
[ ]  2024            */
[ ]  2025           png_ptr->transformations |= PNG_16_TO_8;
[ ]  2026           info_ptr->bit_depth = 8;
[ ]  2027  #     else
[ ]  2028  
[ ]  2029  #        ifdef PNG_READ_SCALE_16_TO_8_SUPPORTED
[ ]  2030              png_ptr->transformations |= PNG_SCALE_16_TO_8;
[ ]  2031              info_ptr->bit_depth = 8;
[ ]  2032  #        else
[ ]  2033  
[ ]  2034              CONFIGURATION ERROR: you must enable at least one 16 to 8 method
[ ]  2035  #        endif
[ ]  2036  #    endif
[ ]  2037  #endif /* !READ_16BIT */
[L]  2038     }
[ ]  2039  
[B]  2040  #ifdef PNG_READ_GRAY_TO_RGB_SUPPORTED
[B]  2041     if ((png_ptr->transformations & PNG_GRAY_TO_RGB) != 0)
[B]  2042        info_ptr->color_type = (png_byte)(info_ptr->color_type |
[B]  2043           PNG_COLOR_MASK_COLOR);
[B]  2044  #endif
[ ]  2045  
[B]  2046  #ifdef PNG_READ_RGB_TO_GRAY_SUPPORTED
[B]  2047     if ((png_ptr->transformations & PNG_RGB_TO_GRAY) != 0)
[ ]  2048        info_ptr->color_type = (png_byte)(info_ptr->color_type &
[ ]  2049           ~PNG_COLOR_MASK_COLOR);
[B]  2050  #endif
[ ]  2051  
[B]  2052  #ifdef PNG_READ_QUANTIZE_SUPPORTED
[B]  2053     if ((png_ptr->transformations & PNG_QUANTIZE) != 0)
[ ]  2054     {
[ ]  2055        if (((info_ptr->color_type == PNG_COLOR_TYPE_RGB) ||
[ ]  2056            (info_ptr->color_type == PNG_COLOR_TYPE_RGB_ALPHA)) &&
[ ]  2057            png_ptr->palette_lookup != 0 && info_ptr->bit_depth == 8)
[ ]  2058        {
[ ]  2059           info_ptr->color_type = PNG_COLOR_TYPE_PALETTE;
[ ]  2060        }
[ ]  2061     }
[B]  2062  #endif
[ ]  2063  
[B]  2064  #ifdef PNG_READ_EXPAND_16_SUPPORTED
[B]  2065     if ((png_ptr->transformations & PNG_EXPAND_16) != 0 &&
[B]  2066         info_ptr->bit_depth == 8 &&
[B]  2067         info_ptr->color_type != PNG_COLOR_TYPE_PALETTE)
[ ]  2068     {
[ ]  2069        info_ptr->bit_depth = 16;
[ ]  2070     }
[B]  2071  #endif
[ ]  2072  
[B]  2073  #ifdef PNG_READ_PACK_SUPPORTED
[B]  2074     if ((png_ptr->transformations & PNG_PACK) != 0 &&
[B]  2075         (info_ptr->bit_depth < 8))
[ ]  2076        info_ptr->bit_depth = 8;
[B]  2077  #endif
[ ]  2078  
[B]  2079     if (info_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
[ ]  2080        info_ptr->channels = 1;
[ ]  2081  
[B]  2082     else if ((info_ptr->color_type & PNG_COLOR_MASK_COLOR) != 0)
[B]  2083        info_ptr->channels = 3;
[ ]  2084  
[ ]  2085     else
[ ]  2086        info_ptr->channels = 1;
[ ]  2087  
[B]  2088  #ifdef PNG_READ_STRIP_ALPHA_SUPPORTED
[B]  2089     if ((png_ptr->transformations & PNG_STRIP_ALPHA) != 0)
[ ]  2090     {
[ ]  2091        info_ptr->color_type = (png_byte)(info_ptr->color_type &
[ ]  2092           ~PNG_COLOR_MASK_ALPHA);
[ ]  2093        info_ptr->num_trans = 0;
[ ]  2094     }
[B]  2095  #endif
[ ]  2096  
[B]  2097     if ((info_ptr->color_type & PNG_COLOR_MASK_ALPHA) != 0)
[B]  2098        info_ptr->channels++;
[ ]  2099  
[B]  2100  #ifdef PNG_READ_FILLER_SUPPORTED
[ ]  2101     /* STRIP_ALPHA and FILLER allowed:  MASK_ALPHA bit stripped above */
[B]  2102     if ((png_ptr->transformations & PNG_FILLER) != 0 &&
[B]  2103         (info_ptr->color_type == PNG_COLOR_TYPE_RGB ||
[ ]  2104         info_ptr->color_type == PNG_COLOR_TYPE_GRAY))
[ ]  2105     {
[ ]  2106        info_ptr->channels++;
[ ]  2107        /* If adding a true alpha channel not just filler */
[ ]  2108        if ((png_ptr->transformations & PNG_ADD_ALPHA) != 0)
[ ]  2109           info_ptr->color_type |= PNG_COLOR_MASK_ALPHA;
[ ]  2110     }
[B]  2111  #endif
[ ]  2112  
[B]  2113  #if defined(PNG_USER_TRANSFORM_PTR_SUPPORTED) && \
[B]  2114  defined(PNG_READ_USER_TRANSFORM_SUPPORTED)
[B]  2115     if ((png_ptr->transformations & PNG_USER_TRANSFORM) != 0)
[ ]  2116     {
[ ]  2117        if (png_ptr->user_transform_depth != 0)
[ ]  2118           info_ptr->bit_depth = png_ptr->user_transform_depth;
[ ]  2119  
[ ]  2120        if (png_ptr->user_transform_channels != 0)
[ ]  2121           info_ptr->channels = png_ptr->user_transform_channels;
[ ]  2122     }
[B]  2123  #endif
[ ]  2124  
[B]  2125     info_ptr->pixel_depth = (png_byte)(info_ptr->channels *
[B]  2126         info_ptr->bit_depth);
[ ]  2127  
[B]  2128     info_ptr->rowbytes = PNG_ROWBYTES(info_ptr->pixel_depth, info_ptr->width);
[ ]  2129  
[ ]  2130     /* Adding in 1.5.4: cache the above value in png_struct so that we can later
[ ]  2131      * check in png_rowbytes that the user buffer won't get overwritten.  Note
[ ]  2132      * that the field is not always set - if png_read_update_info isn't called
[ ]  2133      * the application has to either not do any transforms or get the calculation
[ ]  2134      * right itself.
[ ]  2135      */
[B]  2136     png_ptr->info_rowbytes = info_ptr->rowbytes;
[ ]  2137  
[ ]  2138  #ifndef PNG_READ_EXPAND_SUPPORTED
[ ]  2139     if (png_ptr != NULL)
[ ]  2140        return;
[ ]  2141  #endif
[B]  2142  }

--- No 1-hop callers of OSS_FUZZ_png_read_transform_info fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0       702  pngrtran.c:png_do_expand  (/src/libpng/pngrtran.c:4385-4605)
     248         0  pngrtran.c:png_do_expand_palette  (/src/libpng/pngrtran.c:4212-4377)
      10         0  pngrtran.c:png_init_palette_transformations  (/src/libpng/pngrtran.c:1118-1203)
       0        10  pngrtran.c:png_init_rgb_transformations  (/src/libpng/pngrtran.c:1207-1288)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_read_transform_info  (/src/libpng/pngrtran.c:1941-2142) ---
  d=1   L1947  T=10 F=0  T=0 F=10  if (info_ptr->color_type == PNG_COLOR_TYPE_PALETTE)  <-- BLOCKER
  d=1   L1953  T=2 F=8  T=0 F=0  if (png_ptr->num_trans > 0)
  d=1   L1962  T=0 F=10  T=0 F=0  if (png_ptr->palette == NULL)
  d=1   L1967  T=0 F=0  T=0 F=10  if (png_ptr->num_trans != 0)
  d=1   L1972  T=0 F=0  T=5 F=5  if (info_ptr->bit_depth < 8)
  d=1   L2002  T=0 F=10  T=4 F=6  if (info_ptr->bit_depth == 16)
  d=1   L2006  T=0 F=0  T=4 F=0  if ((png_ptr->transformations & PNG_SCALE_16_TO_8) != 0)
  d=1   L2011  T=0 F=0  T=0 F=4  if ((png_ptr->transformations & PNG_16_TO_8) != 0)

[off-chain: 81 additional divergent branches across 8 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=282c4c4b85d3af6c, size=8764 bytes, fuzzer=cmplog, trial=1, discovered_at=7s, mutation_op=BitFlipMutator,ByteIncMutator,DwordAddMutator,BytesSetMutator,BytesDeleteMutator,WordInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=414b4a1157e93507, size=8568 bytes, fuzzer=cmplog, trial=1, discovered_at=27126s, mutation_op=BytesRandInsertMutator,BytesDeleteMutator,ByteDecMutator,WordInterestingMutator,BytesCopyMutator,ByteIncMutator,BytesRandSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 0f 42 40 08 03 00 00 00 52 ed aa   ......B@.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=04430d1404dcf240, size=8765 bytes, fuzzer=cmplog, trial=1, discovered_at=29940s, mutation_op=ByteInterestingMutator,WordInterestingMutator,ByteFlipMutator,WordInterestingMutator,CrossoverInsertMutator,TokenInsert,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 02 03 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=49a1380366efbf3e, size=8568 bytes, fuzzer=cmplog, trial=1, discovered_at=35373s, mutation_op=WordInterestingMutator,ByteAddMutator,BytesDeleteMutator,BytesSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 08 00 0f 42 40 08 03 00 00 00 52 ed aa   ......B@.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=1b177c559d885638, size=1016 bytes, fuzzer=cmplog, trial=1, discovered_at=48986s, mutation_op=ByteNegMutator,ByteNegMutator,QwordAddMutator,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 69 54 58 74 00 00 b1 8f 0b fc 61   .....iTXt......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0165867d1e996ed7, size=1672 bytes, fuzzer=naive, trial=1, discovered_at=205s, mutation_op=ByteIncMutator,ByteAddMutator,BitFlipMutator,BytesRandSetMutator,ByteRandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 21 00 00 80 00 04 00 00 00 01 00 ff aa   ...!............
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=021042b836a3f5aa, size=927 bytes, fuzzer=naive, trial=1, discovered_at=257s, mutation_op=ByteDecMutator,BytesSetMutator,ByteNegMutator,ByteFlipMutator,WordInterestingMutator,BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 00 00 02 04 00 00 00 01 00 00 aa   ................
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
   0x0013  5b([)x6 05(.)x3 08(.)x1             05(.)x2 21(!)x1 55(U)x1 0a(.)x1 +5u  PARTIAL
   0x0015  00(.)x6 0f(.)x4                     00(.)x10                            PARTIAL
   0x0016  00(.)x6 42(B)x4                     00(.)x4 a0(.)x3 80(.)x2 02(.)x1     PARTIAL
   0x0017  45(E)x6 40(@)x4                     00(.)x3 86(.)x2 02(.)x1 03(.)x1 +3u  PARTIAL
   0x0018  08(.)x7 02(.)x3                     10(.)x4 04(.)x3 02(.)x1 08(.)x1 +1u  PARTIAL
   0x0019  03(.)x10                            00(.)x8 04(.)x2                     DIFFER
   0x001d  52(R)x10                            7f(.)x5 00(.)x4 ff(.)x1             DIFFER
   0x001e  ed(.)x10                            ed(.)x6 ff(.)x2 00(.)x2             PARTIAL
   0x0025  67(g)x8 69(i)x2                     67(g)x10                            PARTIAL
   0x0026  41(A)x8 54(T)x2                     41(A)x10                            PARTIAL
   0x0027  4d(M)x8 58(X)x2                     4d(M)x10                            PARTIAL
   0x0028  41(A)x8 74(t)x2                     41(A)x10                            PARTIAL
   0x002d  0b(.)x10                            0b(.)x8 aa(.)x1 1b(.)x1             PARTIAL
   0x002e  fc(.)x10                            fc(.)x5 04(.)x4 56(V)x1             PARTIAL
   0x002f  61(a)x10                            61(a)x9 aa(.)x1                     PARTIAL
   0x0030  05(.)x10                            05(.)x9 aa(.)x1                     PARTIAL
   0x0034  01(.)x10                            01(.)x9 09(.)x1                     PARTIAL
   0x0035  73(s)x10                            73(s)x9 74(t)x1                     PARTIAL
   0x0036  52(R)x10                            52(R)x9 45(E)x1                     PARTIAL
   0x0037  47(G)x10                            47(G)x9 58(X)x1                     PARTIAL
   0x0038  42(B)x10                            42(B)x9 74(t)x1                     PARTIAL
   0x0039  01(.)x10                            01(.)x9 54(T)x1                     PARTIAL
   0x003a  d9(.)x10                            d9(.)x9 69(i)x1                     PARTIAL
   0x003b  c9(.)x10                            c9(.)x9 74(t)x1                     PARTIAL
   0x003c  2c(,)x10                            2c(,)x9 6c(l)x1                     PARTIAL
   0x003d  7f(.)x10                            7f(.)x9 65(e)x1                     PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3913.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3913,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3913 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3913 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3913 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).