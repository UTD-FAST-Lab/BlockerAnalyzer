==== BLOCKER ====
Target: libpng
Branch ID: 3864
Location: /src/libpng/png.c:2636:9
Enclosing function: OSS_FUZZ_png_check_IHDR
Source line:    if (((color_type == PNG_COLOR_TYPE_PALETTE) && bit_depth > 8) ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog); loser (value_profile vs value_profile); loser (ctx_coverage vs naive_ctx)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                   10        0          0  winner (value_profile vs naive)
value_profile_cmplog             ?        ?          ?  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     3        7          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'naive_ctx', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (3) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.90h  loser=21.60h
  avg hitcount on branch: winner=144  loser=0
  prob_div=0.90  dur_div=20.70h  hit_div=144
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002
--- Pair 2: value_profile > naive  [delta: value_profile] ---
  subject 22  (value_profile vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=3.40h  loser=21.60h
  avg hitcount on branch: winner=103  loser=0
  prob_div=0.90  dur_div=18.20h  hit_div=103
  subject-level: delta_AUC=16855020.0  p_AUC=0.0002  delta_Final=254.7  p_final=0.0002
--- Pair 3: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 25  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=1.50h  loser=21.60h
  avg hitcount on branch: winner=7  loser=0
  prob_div=0.90  dur_div=20.10h  hit_div=7
  subject-level: delta_AUC=6413040.0  p_AUC=0.0003  delta_Final=91.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3864/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_check_IHDR (/src/libpng/png.c:2551-2700) ---
[ ]  2549      int color_type, int interlace_type, int compression_type,
[ ]  2550      int filter_type)
[B]  2551  {
[B]  2552     int error = 0;
[ ]  2553  
[ ]  2554     /* Check for width and height valid values */
[B]  2555     if (width == 0)
[ ]  2556     {
[ ]  2557        png_warning(png_ptr, "Image width is zero in IHDR");
[ ]  2558        error = 1;
[ ]  2559     }
[ ]  2560  
[B]  2561     if (width > PNG_UINT_31_MAX)
[ ]  2562     {
[ ]  2563        png_warning(png_ptr, "Invalid image width in IHDR");
[ ]  2564        error = 1;
[ ]  2565     }
[ ]  2566  
[B]  2567     if (png_gt(((width + 7) & (~7U)),
[B]  2568         ((PNG_SIZE_MAX
[B]  2569             - 48        /* big_row_buf hack */
[B]  2570             - 1)        /* filter byte */
[B]  2571             / 8)        /* 8-byte RGBA pixels */
[B]  2572             - 1))       /* extra max_pixel_depth pad */
[ ]  2573     {
[ ]  2574        /* The size of the row must be within the limits of this architecture.
[ ]  2575         * Because the read code can perform arbitrary transformations the
[ ]  2576         * maximum size is checked here.  Because the code in png_read_start_row
[ ]  2577         * adds extra space "for safety's sake" in several places a conservative
[ ]  2578         * limit is used here.
[ ]  2579         *
[ ]  2580         * NOTE: it would be far better to check the size that is actually used,
[ ]  2581         * but the effect in the real world is minor and the changes are more
[ ]  2582         * extensive, therefore much more dangerous and much more difficult to
[ ]  2583         * write in a way that avoids compiler warnings.
[ ]  2584         */
[ ]  2585        png_warning(png_ptr, "Image width is too large for this architecture");
[ ]  2586        error = 1;
[ ]  2587     }
[ ]  2588  
[B]  2589  #ifdef PNG_SET_USER_LIMITS_SUPPORTED
[B]  2590     if (width > png_ptr->user_width_max)
[ ]  2591  #else
[ ]  2592     if (width > PNG_USER_WIDTH_MAX)
[ ]  2593  #endif
[ ]  2594     {
[ ]  2595        png_warning(png_ptr, "Image width exceeds user limit in IHDR");
[ ]  2596        error = 1;
[ ]  2597     }
[ ]  2598  
[B]  2599     if (height == 0)
[ ]  2600     {
[ ]  2601        png_warning(png_ptr, "Image height is zero in IHDR");
[ ]  2602        error = 1;
[ ]  2603     }
[ ]  2604  
[B]  2605     if (height > PNG_UINT_31_MAX)
[ ]  2606     {
[ ]  2607        png_warning(png_ptr, "Invalid image height in IHDR");
[ ]  2608        error = 1;
[ ]  2609     }
[ ]  2610  
[B]  2611  #ifdef PNG_SET_USER_LIMITS_SUPPORTED
[B]  2612     if (height > png_ptr->user_height_max)
[ ]  2613  #else
[ ]  2614     if (height > PNG_USER_HEIGHT_MAX)
[ ]  2615  #endif
[ ]  2616     {
[ ]  2617        png_warning(png_ptr, "Image height exceeds user limit in IHDR");
[ ]  2618        error = 1;
[ ]  2619     }
[ ]  2620  
[ ]  2621     /* Check other values */
[B]  2622     if (bit_depth != 1 && bit_depth != 2 && bit_depth != 4 &&
[B]  2623         bit_depth != 8 && bit_depth != 16)
[ ]  2624     {
[ ]  2625        png_warning(png_ptr, "Invalid bit depth in IHDR");
[ ]  2626        error = 1;
[ ]  2627     }
[ ]  2628  
[B]  2629     if (color_type < 0 || color_type == 1 ||
[B]  2630         color_type == 5 || color_type > 6)
[ ]  2631     {
[ ]  2632        png_warning(png_ptr, "Invalid color type in IHDR");
[ ]  2633        error = 1;
[ ]  2634     }
[ ]  2635  
[B]  2636     if (((color_type == PNG_COLOR_TYPE_PALETTE) && bit_depth > 8) || <-- BLOCKER
[B]  2637         ((color_type == PNG_COLOR_TYPE_RGB ||
[B]  2638           color_type == PNG_COLOR_TYPE_GRAY_ALPHA ||
[B]  2639           color_type == PNG_COLOR_TYPE_RGB_ALPHA) && bit_depth < 8))
[ ]  2640     {
[ ]  2641        png_warning(png_ptr, "Invalid color type/bit depth combination in IHDR");
[ ]  2642        error = 1;
[ ]  2643     }
[ ]  2644  
[B]  2645     if (interlace_type >= PNG_INTERLACE_LAST)
[ ]  2646     {
[ ]  2647        png_warning(png_ptr, "Unknown interlace method in IHDR");
[ ]  2648        error = 1;
[ ]  2649     }
[ ]  2650  
[B]  2651     if (compression_type != PNG_COMPRESSION_TYPE_BASE)
[ ]  2652     {
[ ]  2653        png_warning(png_ptr, "Unknown compression method in IHDR");
[ ]  2654        error = 1;
[ ]  2655     }
[ ]  2656  
[B]  2657  #ifdef PNG_MNG_FEATURES_SUPPORTED
[ ]  2658     /* Accept filter_method 64 (intrapixel differencing) only if
[ ]  2659      * 1. Libpng was compiled with PNG_MNG_FEATURES_SUPPORTED and
[ ]  2660      * 2. Libpng did not read a PNG signature (this filter_method is only
[ ]  2661      *    used in PNG datastreams that are embedded in MNG datastreams) and
[ ]  2662      * 3. The application called png_permit_mng_features with a mask that
[ ]  2663      *    included PNG_FLAG_MNG_FILTER_64 and
[ ]  2664      * 4. The filter_method is 64 and
[ ]  2665      * 5. The color_type is RGB or RGBA
[ ]  2666      */
[B]  2667     if ((png_ptr->mode & PNG_HAVE_PNG_SIGNATURE) != 0 &&
[B]  2668         png_ptr->mng_features_permitted != 0)
[ ]  2669        png_warning(png_ptr, "MNG features are not allowed in a PNG datastream");
[ ]  2670  
[B]  2671     if (filter_type != PNG_FILTER_TYPE_BASE)
[ ]  2672     {
[ ]  2673        if (!((png_ptr->mng_features_permitted & PNG_FLAG_MNG_FILTER_64) != 0 &&
[ ]  2674            (filter_type == PNG_INTRAPIXEL_DIFFERENCING) &&
[ ]  2675            ((png_ptr->mode & PNG_HAVE_PNG_SIGNATURE) == 0) &&
[ ]  2676            (color_type == PNG_COLOR_TYPE_RGB ||
[ ]  2677            color_type == PNG_COLOR_TYPE_RGB_ALPHA)))
[ ]  2678        {
[ ]  2679           png_warning(png_ptr, "Unknown filter method in IHDR");
[ ]  2680           error = 1;
[ ]  2681        }
[ ]  2682  
[ ]  2683        if ((png_ptr->mode & PNG_HAVE_PNG_SIGNATURE) != 0)
[ ]  2684        {
[ ]  2685           png_warning(png_ptr, "Invalid filter method in IHDR");
[ ]  2686           error = 1;
[ ]  2687        }
[ ]  2688     }
[ ]  2689  
[ ]  2690  #else
[ ]  2691     if (filter_type != PNG_FILTER_TYPE_BASE)
[ ]  2692     {
[ ]  2693        png_warning(png_ptr, "Unknown filter method in IHDR");
[ ]  2694        error = 1;
[ ]  2695     }
[ ]  2696  #endif
[ ]  2697  
[B]  2698     if (error == 1)
[ ]  2699        png_error(png_ptr, "Invalid IHDR data");
[B]  2700  }

--- No 1-hop callers of OSS_FUZZ_png_check_IHDR fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1360       378  OSS_FUZZ_png_get_io_ptr  (/src/libpng/png.c:687-692)
     971       257  OSS_FUZZ_png_calculate_crc  (/src/libpng/png.c:140-187)
     368        33  OSS_FUZZ_png_muldiv  (/src/libpng/png.c:3351-3461)
     414       128  OSS_FUZZ_png_reset_crc  (/src/libpng/png.c:128-131)
     377       117  OSS_FUZZ_png_handle_as_unknown  (/src/libpng/png.c:927-956)
     377       117  OSS_FUZZ_png_chunk_unknown_handling  (/src/libpng/png.c:962-967)
      83        23  OSS_FUZZ_png_free_data  (/src/libpng/png.c:473-678)
      60        20  OSS_FUZZ_png_create_info_struct  (/src/libpng/png.c:355-375)
      60        20  OSS_FUZZ_png_destroy_info_struct  (/src/libpng/png.c:387-412)
      48        10  OSS_FUZZ_png_reciprocal  (/src/libpng/png.c:3489-3503)
      38         3  png.c:png_colorspace_endpoints_match  (/src/libpng/png.c:1593-1605)
      30        10  OSS_FUZZ_png_set_sig_bytes  (/src/libpng/png.c:48-63)
      30        10  OSS_FUZZ_png_sig_cmp  (/src/libpng/png.c:75-91)
      30        10  OSS_FUZZ_png_user_version_check  (/src/libpng/png.c:194-244)
      30        10  OSS_FUZZ_png_create_png_struct  (/src/libpng/png.c:253-350)
... (7 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_check_IHDR  (/src/libpng/png.c:2551-2700) ---
  d=1   L2555  T=0 F=45  T=0 F=17  if (width == 0)
  d=1   L2561  T=0 F=45  T=0 F=17  if (width > PNG_UINT_31_MAX)
  d=1   L2567  T=0 F=45  T=0 F=17  if (png_gt(((width + 7) & (~7U)),
  d=1   L2590  T=0 F=45  T=0 F=17  if (width > png_ptr->user_width_max)
  d=1   L2599  T=0 F=45  T=0 F=17  if (height == 0)
  d=1   L2605  T=0 F=45  T=0 F=17  if (height > PNG_UINT_31_MAX)
  d=1   L2612  T=0 F=45  T=0 F=17  if (height > png_ptr->user_height_max)
  d=1   L2622  T=37 F=8  T=16 F=1  if (bit_depth != 1 && bit_depth != 2 && bit_depth != 4 &&
  d=1   L2622  T=31 F=6  T=14 F=2  if (bit_depth != 1 && bit_depth != 2 && bit_depth != 4 &&
  d=1   L2622  T=25 F=6  T=11 F=3  if (bit_depth != 1 && bit_depth != 2 && bit_depth != 4 &&
  d=1   L2623  T=0 F=25  T=8 F=3  bit_depth != 8 && bit_depth != 16)
  d=1   L2623  T=0 F=0  T=0 F=8  bit_depth != 8 && bit_depth != 16)
  d=1   L2629  T=0 F=45  T=0 F=17  if (color_type < 0 || color_type == 1 ||
  d=1   L2629  T=0 F=45  T=0 F=17  if (color_type < 0 || color_type == 1 ||
  d=1   L2630  T=0 F=45  T=0 F=17  color_type == 5 || color_type > 6)
  d=1   L2630  T=0 F=45  T=0 F=17  color_type == 5 || color_type > 6)
  d=1   L2636  T=0 F=45  T=0 F=0  if (((color_type == PNG_COLOR_TYPE_PALETTE) && bit_depth ...  <-- BLOCKER
  d=1   L2636  T=45 F=0  T=0 F=17  if (((color_type == PNG_COLOR_TYPE_PALETTE) && bit_depth ...  <-- BLOCKER
  d=1   L2637  T=0 F=45  T=0 F=17  ((color_type == PNG_COLOR_TYPE_RGB ||
  d=1   L2638  T=0 F=45  T=4 F=13  color_type == PNG_COLOR_TYPE_GRAY_ALPHA ||
  d=1   L2639  T=0 F=0  T=0 F=5  color_type == PNG_COLOR_TYPE_RGB_ALPHA) && bit_depth < 8))
  d=1   L2639  T=0 F=45  T=1 F=12  color_type == PNG_COLOR_TYPE_RGB_ALPHA) && bit_depth < 8))
  d=1   L2645  T=0 F=45  T=0 F=17  if (interlace_type >= PNG_INTERLACE_LAST)
  d=1   L2651  T=0 F=45  T=0 F=17  if (compression_type != PNG_COMPRESSION_TYPE_BASE)
  d=1   L2667  T=0 F=45  T=0 F=17  if ((png_ptr->mode & PNG_HAVE_PNG_SIGNATURE) != 0 &&
  d=1   L2671  T=0 F=45  T=0 F=17  if (filter_type != PNG_FILTER_TYPE_BASE)
  d=1   L2698  T=0 F=45  T=0 F=17  if (error == 1)

[off-chain: 150 additional divergent branches across 27 functions (see HIT-COUNT DIVERGENCE for which functions)]

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
   0x0012  00(.)x30                            00(.)x9 05(.)x1                     PARTIAL
   0x0015  00(.)x27 0f(.)x2 04(.)x1            00(.)x10                            PARTIAL
   0x0016  00(.)x26 42(B)x2 ff(.)x1 01(.)x1    a0(.)x4 00(.)x3 80(.)x2 02(.)x1     PARTIAL
   0x0017  45(E)x24 1f(.)x3 40(@)x2 05(.)x1    86(.)x3 00(.)x3 45(E)x2 03(.)x1 +1u  PARTIAL
   0x0018  08(.)x20 01(.)x4 02(.)x3 04(.)x3    10(.)x4 08(.)x2 04(.)x2 02(.)x1 +1u  PARTIAL
   0x0019  03(.)x30                            00(.)x7 04(.)x2 06(.)x1             DIFFER
   0x001d  52(R)x30                            7f(.)x4 00(.)x3 52(R)x2 ff(.)x1     PARTIAL
   0x001e  ed(.)x30                            ed(.)x7 ff(.)x2 00(.)x1             PARTIAL
   0x001f  aa(.)x28 55(U)x2                    aa(.)x10                            PARTIAL
   0x0025  67(g)x28 69(i)x2                    67(g)x10                            PARTIAL
   0x0026  41(A)x28 54(T)x2                    41(A)x10                            PARTIAL
   0x0027  4d(M)x19 6d(m)x9 58(X)x2            4d(M)x10                            PARTIAL
   0x0028  41(A)x28 74(t)x2                    41(A)x10                            PARTIAL
   0x0029  00(.)x30                            00(.)x9 80(.)x1                     PARTIAL
   0x002a  00(.)x29 c2(.)x1                    00(.)x10                            PARTIAL
   0x002b  b1(.)x21 00(.)x9                    b1(.)x10                            PARTIAL
   0x002c  8f(.)x21 00(.)x9                    8f(.)x10                            PARTIAL
   0x002d  0b(.)x21 00(.)x9                    0b(.)x9 aa(.)x1                     PARTIAL
   0x002e  fc(.)x21 00(.)x9                    fc(.)x6 04(.)x3 56(V)x1             PARTIAL
   0x002f  61(a)x21 00(.)x9                    61(a)x9 aa(.)x1                     PARTIAL
   0x0030  05(.)x21 00(.)x9                    05(.)x9 aa(.)x1                     PARTIAL
   0x0034  01(.)x21 ff(.)x9                    01(.)x9 09(.)x1                     PARTIAL
   0x0035  73(s)x20 50(P)x10                   73(s)x9 74(t)x1                     PARTIAL
   0x0036  52(R)x20 4c(L)x10                   52(R)x9 45(E)x1                     PARTIAL
   0x0037  47(G)x20 54(T)x10                   47(G)x9 58(X)x1                     PARTIAL
   0x0038  42(B)x20 45(E)x10                   42(B)x9 74(t)x1                     PARTIAL
   0x0039  01(.)x21 52(R)x9                    01(.)x9 54(T)x1                     PARTIAL
   0x003a  d9(.)x21 01(.)x9                    d9(.)x9 69(i)x1                     PARTIAL
   0x003b  c9(.)x21 76(v)x9                    c9(.)x9 74(t)x1                     PARTIAL
   0x003c  2c(,)x15 76(v)x9 2f(/)x6            2c(,)x9 6c(l)x1                     PARTIAL
   0x003d  7f(.)x21 18(.)x9                    7f(.)x9 65(e)x1                     PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3864.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3864,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile>naive (value_profile), naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3864 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3864 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3864 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).