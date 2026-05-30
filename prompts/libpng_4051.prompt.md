==== BLOCKER ====
Target: libpng
Branch ID: 4051
Location: /src/libpng/pngrutil.c:2767:30
Enclosing function: OSS_FUZZ_png_handle_iTXt
Source line:    if (prefix_length > 79 || prefix_length < 1)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    4        6          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        4        6          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.00h  loser=21.90h
  avg hitcount on branch: winner=86  loser=0
  prob_div=0.90  dur_div=21.90h  hit_div=86
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/4051/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_iTXt (/src/libpng/pngrutil.c:2715-2858) ---
[ ]  2713  void /* PRIVATE */
[ ]  2714  png_handle_iTXt(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  2715  {
[B]  2716     png_const_charp errmsg = NULL;
[B]  2717     png_bytep buffer;
[B]  2718     png_uint_32 prefix_length;
[ ]  2719  
[B]  2720     png_debug(1, "in png_handle_iTXt");
[ ]  2721  
[B]  2722  #ifdef PNG_USER_LIMITS_SUPPORTED
[B]  2723     if (png_ptr->user_chunk_cache_max != 0)
[B]  2724     {
[B]  2725        if (png_ptr->user_chunk_cache_max == 1)
[ ]  2726        {
[ ]  2727           png_crc_finish(png_ptr, length);
[ ]  2728           return;
[ ]  2729        }
[ ]  2730  
[B]  2731        if (--png_ptr->user_chunk_cache_max == 1)
[ ]  2732        {
[ ]  2733           png_crc_finish(png_ptr, length);
[ ]  2734           png_chunk_benign_error(png_ptr, "no space in chunk cache");
[ ]  2735           return;
[ ]  2736        }
[B]  2737     }
[B]  2738  #endif
[ ]  2739  
[B]  2740     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  2741        png_chunk_error(png_ptr, "missing IHDR");
[ ]  2742  
[B]  2743     if ((png_ptr->mode & PNG_HAVE_IDAT) != 0)
[L]  2744        png_ptr->mode |= PNG_AFTER_IDAT;
[ ]  2745  
[B]  2746     buffer = png_read_buffer(png_ptr, length+1, 1/*warn*/);
[ ]  2747  
[B]  2748     if (buffer == NULL)
[ ]  2749     {
[ ]  2750        png_crc_finish(png_ptr, length);
[ ]  2751        png_chunk_benign_error(png_ptr, "out of memory");
[ ]  2752        return;
[ ]  2753     }
[ ]  2754  
[B]  2755     png_crc_read(png_ptr, buffer, length);
[ ]  2756  
[B]  2757     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  2758        return;
[ ]  2759  
[ ]  2760     /* First the keyword. */
[B]  2761     for (prefix_length=0;
[B]  2762        prefix_length < length && buffer[prefix_length] != 0;
[B]  2763        ++prefix_length)
[B]  2764        /* Empty loop */ ;
[ ]  2765  
[ ]  2766     /* Perform a basic check on the keyword length here. */
[B]  2767     if (prefix_length > 79 || prefix_length < 1) <-- BLOCKER
[W]  2768        errmsg = "bad keyword";
[ ]  2769  
[ ]  2770     /* Expect keyword, compression flag, compression type, language, translated
[ ]  2771      * keyword (both may be empty but are 0 terminated) then the text, which may
[ ]  2772      * be empty.
[ ]  2773      */
[B]  2774     else if (prefix_length + 5 > length)
[B]  2775        errmsg = "truncated";
[ ]  2776  
[B]  2777     else if (buffer[prefix_length+1] == 0 ||
[B]  2778        (buffer[prefix_length+1] == 1 &&
[L]  2779        buffer[prefix_length+2] == PNG_COMPRESSION_TYPE_BASE))
[B]  2780     {
[B]  2781        int compressed = buffer[prefix_length+1] != 0;
[B]  2782        png_uint_32 language_offset, translated_keyword_offset;
[B]  2783        png_alloc_size_t uncompressed_length = 0;
[ ]  2784  
[ ]  2785        /* Now the language tag */
[B]  2786        prefix_length += 3;
[B]  2787        language_offset = prefix_length;
[ ]  2788  
[B]  2789        for (; prefix_length < length && buffer[prefix_length] != 0;
[B]  2790           ++prefix_length)
[L]  2791           /* Empty loop */ ;
[ ]  2792  
[ ]  2793        /* WARNING: the length may be invalid here, this is checked below. */
[B]  2794        translated_keyword_offset = ++prefix_length;
[ ]  2795  
[B]  2796        for (; prefix_length < length && buffer[prefix_length] != 0;
[B]  2797           ++prefix_length)
[L]  2798           /* Empty loop */ ;
[ ]  2799  
[ ]  2800        /* prefix_length should now be at the trailing '\0' of the translated
[ ]  2801         * keyword, but it may already be over the end.  None of this arithmetic
[ ]  2802         * can overflow because chunks are at most 2^31 bytes long, but on 16-bit
[ ]  2803         * systems the available allocation may overflow.
[ ]  2804         */
[B]  2805        ++prefix_length;
[ ]  2806  
[B]  2807        if (compressed == 0 && prefix_length <= length)
[B]  2808           uncompressed_length = length - prefix_length;
[ ]  2809  
[L]  2810        else if (compressed != 0 && prefix_length < length)
[L]  2811        {
[L]  2812           uncompressed_length = PNG_SIZE_MAX;
[ ]  2813  
[ ]  2814           /* TODO: at present png_decompress_chunk imposes a single application
[ ]  2815            * level memory limit, this should be split to different values for
[ ]  2816            * iCCP and text chunks.
[ ]  2817            */
[L]  2818           if (png_decompress_chunk(png_ptr, length, prefix_length,
[L]  2819               &uncompressed_length, 1/*terminate*/) == Z_STREAM_END)
[ ]  2820              buffer = png_ptr->read_buffer;
[ ]  2821  
[L]  2822           else
[L]  2823              errmsg = png_ptr->zstream.msg;
[L]  2824        }
[ ]  2825  
[L]  2826        else
[L]  2827           errmsg = "truncated";
[ ]  2828  
[B]  2829        if (errmsg == NULL)
[B]  2830        {
[B]  2831           png_text text;
[ ]  2832  
[B]  2833           buffer[uncompressed_length+prefix_length] = 0;
[ ]  2834  
[B]  2835           if (compressed == 0)
[B]  2836              text.compression = PNG_ITXT_COMPRESSION_NONE;
[ ]  2837  
[ ]  2838           else
[ ]  2839              text.compression = PNG_ITXT_COMPRESSION_zTXt;
[ ]  2840  
[B]  2841           text.key = (png_charp)buffer;
[B]  2842           text.lang = (png_charp)buffer + language_offset;
[B]  2843           text.lang_key = (png_charp)buffer + translated_keyword_offset;
[B]  2844           text.text = (png_charp)buffer + prefix_length;
[B]  2845           text.text_length = 0;
[B]  2846           text.itxt_length = uncompressed_length;
[ ]  2847  
[B]  2848           if (png_set_text_2(png_ptr, info_ptr, &text, 1) != 0)
[ ]  2849              errmsg = "insufficient memory";
[B]  2850        }
[B]  2851     }
[ ]  2852  
[L]  2853     else
[L]  2854        errmsg = "bad compression info";
[ ]  2855  
[B]  2856     if (errmsg != NULL)
[B]  2857        png_chunk_benign_error(png_ptr, errmsg);
[B]  2858  }

--- No 1-hop callers of OSS_FUZZ_png_handle_iTXt fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      86        13  pngrutil.c:png_get_fixed_point  (/src/libpng/pngrutil.c:42-53)
       0        42  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
      41        12  OSS_FUZZ_png_handle_pCAL  (/src/libpng/pngrutil.c:2249-2371)
       2        30  OSS_FUZZ_png_read_IDAT_data  (/src/libpng/pngrutil.c:4152-4276)
       0        24  OSS_FUZZ_png_combine_row  (/src/libpng/pngrutil.c:3202-3681)
       0        24  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
       0        13  OSS_FUZZ_png_handle_pHYs  (/src/libpng/pngrutil.c:2156-2196)
       0        12  OSS_FUZZ_png_read_finish_IDAT  (/src/libpng/pngrutil.c:4280-4324)
       9         0  OSS_FUZZ_png_handle_PLTE  (/src/libpng/pngrutil.c:913-1096)
       9         0  OSS_FUZZ_png_handle_oFFs  (/src/libpng/pngrutil.c:2202-2242)
       6         0  OSS_FUZZ_png_handle_sPLT  (/src/libpng/pngrutil.c:1641-1811)
       5         0  OSS_FUZZ_png_handle_iCCP  (/src/libpng/pngrutil.c:1363-1634)
       4         0  OSS_FUZZ_png_handle_tRNS  (/src/libpng/pngrutil.c:1817-1915)
       2         6  OSS_FUZZ_png_read_start_row  (/src/libpng/pngrutil.c:4393-4680)
       3         0  pngrutil.c:png_inflate_read  (/src/libpng/pngrutil.c:776-832)
... (2 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_iTXt  (/src/libpng/pngrutil.c:2715-2858) ---
  d=1   L2743  T=0 F=23  T=18 F=27  if ((png_ptr->mode & PNG_HAVE_IDAT) != 0)
  d=1   L2762  T=59 F=4  T=198 F=13  prefix_length < length && buffer[prefix_length] != 0;
  d=1   L2762  T=40 F=19  T=166 F=32  prefix_length < length && buffer[prefix_length] != 0;
  d=1   L2767  T=16 F=7  T=0 F=45  if (prefix_length > 79 || prefix_length < 1)  <-- BLOCKER
  d=1   L2774  T=4 F=3  T=15 F=30  else if (prefix_length + 5 > length)
  d=1   L2777  T=3 F=0  T=20 F=10  else if (buffer[prefix_length+1] == 0 ||
  d=1   L2778  T=0 F=0  T=5 F=5  (buffer[prefix_length+1] == 1 &&
  d=1   L2779  T=0 F=0  T=3 F=2  buffer[prefix_length+2] == PNG_COMPRESSION_TYPE_BASE))
  d=1   L2789  T=3 F=0  T=196 F=1  for (; prefix_length < length && buffer[prefix_length] != 0;
  d=1   L2789  T=0 F=3  T=174 F=22  for (; prefix_length < length && buffer[prefix_length] != 0;
  d=1   L2796  T=3 F=0  T=304 F=2  for (; prefix_length < length && buffer[prefix_length] != 0;
  d=1   L2796  T=0 F=3  T=283 F=21  for (; prefix_length < length && buffer[prefix_length] != 0;
  d=1   L2807  T=3 F=0  T=18 F=2  if (compressed == 0 && prefix_length <= length)
  d=1   L2807  T=3 F=0  T=20 F=3  if (compressed == 0 && prefix_length <= length)
  d=1   L2810  T=0 F=0  T=3 F=0  else if (compressed != 0 && prefix_length < length)
  d=1   L2810  T=0 F=0  T=3 F=2  else if (compressed != 0 && prefix_length < length)
  d=1   L2818  T=0 F=0  T=0 F=3  if (png_decompress_chunk(png_ptr, length, prefix_length,
  d=1   L2829  T=3 F=0  T=18 F=5  if (errmsg == NULL)
  d=1   L2835  T=3 F=0  T=18 F=0  if (compressed == 0)
  d=1   L2848  T=0 F=3  T=0 F=18  if (png_set_text_2(png_ptr, info_ptr, &text, 1) != 0)

[off-chain: 285 additional divergent branches across 34 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=08f4a8b1448642a9, size=995 bytes, fuzzer=cmplog, trial=1, discovered_at=133s, mutation_op=ByteAddMutator,ByteInterestingMutator,ByteFlipMutator,CrossoverReplaceMutator,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=015f9b31905f8499, size=1225 bytes, fuzzer=cmplog, trial=1, discovered_at=1100s, mutation_op=BytesDeleteMutator,BytesExpandMutator,QwordAddMutator,ByteFlipMutator,ByteRandMutator,ByteInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=038915e208a4e717, size=1225 bytes, fuzzer=cmplog, trial=1, discovered_at=1252s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,WordInterestingMutator,BytesInsertMutator,BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=10b5f5bcca4a6feb, size=780 bytes, fuzzer=cmplog, trial=1, discovered_at=6210s, mutation_op=BytesDeleteMutator,ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 5 (id=0d06acd2d6a6fbd2, size=613 bytes, fuzzer=cmplog, trial=1, discovered_at=8081s, mutation_op=BytesSetMutator,BitFlipMutator,BytesSwapMutator,TokenReplace,BytesRandInsertMutator,BytesDeleteMutator,ByteInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 69 54 58 74 00 00 b1 8f 0b fc 00   .....iTXt.......
  0030: 05 00 00 00 01 74 45 58 74 01 d9 c9 2c 7f 00 00   .....tEXt...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=201c391568c5f3e2, size=397 bytes, fuzzer=naive, trial=1, discovered_at=1105s, mutation_op=BytesExpandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=11310c37a65a7b2e, size=677 bytes, fuzzer=naive, trial=1, discovered_at=5943s, mutation_op=BytesExpandMutator,CrossoverInsertMutator,BytesDeleteMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=12a95c71ef9523b4, size=682 bytes, fuzzer=naive, trial=1, discovered_at=6254s, mutation_op=BytesRandSetMutator,WordInterestingMutator,ByteIncMutator,ByteNegMutator,ByteRandMutator,QwordAddMutator,BytesExpandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=2780959be3c39420, size=1101 bytes, fuzzer=naive, trial=1, discovered_at=8231s, mutation_op=BytesInsertCopyMutator,BytesCopyMutator,ByteRandMutator,CrossoverInsertMutator,CrossoverReplaceMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=2bf6d6947f3afdd7, size=483 bytes, fuzzer=naive, trial=1, discovered_at=9791s, mutation_op=BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 e4 aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 80 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0013  5b([)x16                            5b([)x7 ab(.)x6                     PARTIAL
   0x0017  45(E)x16                            45(E)x7 01(.)x6                     PARTIAL
   0x0018  08(.)x16                            08(.)x7 01(.)x6                     PARTIAL
   0x0019  06(.)x14 03(.)x2                    06(.)x7 00(.)x6                     PARTIAL
   0x001c  01(.)x15 00(.)x1                    01(.)x13                            PARTIAL
   0x001d  52(R)x16                            52(R)x7 7f(.)x6                     PARTIAL
   0x001e  ed(.)x16                            ed(.)x11 e4(.)x2                    PARTIAL
   0x0025  67(g)x8 69(i)x8                     67(g)x13                            PARTIAL
   0x0026  41(A)x8 54(T)x8                     41(A)x13                            PARTIAL
   0x0027  4d(M)x8 58(X)x8                     4d(M)x13                            PARTIAL
   0x0028  41(A)x8 74(t)x8                     41(A)x13                            PARTIAL
   0x0029  00(.)x16                            80(.)x7 00(.)x6                     PARTIAL
   0x002d  0b(.)x16                            0b(.)x7 1b(.)x6                     PARTIAL
   0x002f  61(a)x10 00(.)x6                    61(a)x13                            PARTIAL
   0x0035  74(t)x6 73(s)x5 69(i)x3 62(b)x2     73(s)x13                            PARTIAL
   0x0036  45(E)x6 52(R)x5 54(T)x3 4b(K)x2     52(R)x13                            PARTIAL
   0x0037  58(X)x9 47(G)x7                     47(G)x13                            PARTIAL
   0x0038  74(t)x9 42(B)x5 44(D)x2             42(B)x13                            PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_4051.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4051,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4051 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4051 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4051 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).