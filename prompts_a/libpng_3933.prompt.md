==== BLOCKER ====
Target: libpng
Branch ID: 3933
Location: /src/libpng/pngrtran.c:4792:14
Enclosing function: OSS_FUZZ_png_do_read_transformations
Source line:          if (png_ptr->num_trans != 0 &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.80h  loser=24.00h
  avg hitcount on branch: winner=1609  loser=0
  prob_div=1.00  dur_div=23.20h  hit_div=1609
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3933/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_do_read_transformations (/src/libpng/pngrtran.c:4741-5041) ---
[ ]  4739  void /* PRIVATE */
[ ]  4740  png_do_read_transformations(png_structrp png_ptr, png_row_infop row_info)
[B]  4741  {
[B]  4742     png_debug(1, "in png_do_read_transformations");
[ ]  4743  
[B]  4744     if (png_ptr->row_buf == NULL)
[ ]  4745     {
[ ]  4746        /* Prior to 1.5.4 this output row/pass where the NULL pointer is, but this
[ ]  4747         * error is incredibly rare and incredibly easy to debug without this
[ ]  4748         * information.
[ ]  4749         */
[ ]  4750        png_error(png_ptr, "NULL row buffer");
[ ]  4751     }
[ ]  4752  
[ ]  4753     /* The following is debugging; prior to 1.5.4 the code was never compiled in;
[ ]  4754      * in 1.5.4 PNG_FLAG_DETECT_UNINITIALIZED was added and the macro
[ ]  4755      * PNG_WARN_UNINITIALIZED_ROW removed.  In 1.6 the new flag is set only for
[ ]  4756      * all transformations, however in practice the ROW_INIT always gets done on
[ ]  4757      * demand, if necessary.
[ ]  4758      */
[B]  4759     if ((png_ptr->flags & PNG_FLAG_DETECT_UNINITIALIZED) != 0 &&
[B]  4760         (png_ptr->flags & PNG_FLAG_ROW_INIT) == 0)
[ ]  4761     {
[ ]  4762        /* Application has failed to call either png_read_start_image() or
[ ]  4763         * png_read_update_info() after setting transforms that expand pixels.
[ ]  4764         * This check added to libpng-1.2.19 (but not enabled until 1.5.4).
[ ]  4765         */
[ ]  4766        png_error(png_ptr, "Uninitialized row");
[ ]  4767     }
[ ]  4768  
[B]  4769  #ifdef PNG_READ_EXPAND_SUPPORTED
[B]  4770     if ((png_ptr->transformations & PNG_EXPAND) != 0)
[B]  4771     {
[B]  4772        if (row_info->color_type == PNG_COLOR_TYPE_PALETTE)
[ ]  4773        {
[ ]  4774  #ifdef PNG_ARM_NEON_INTRINSICS_AVAILABLE
[ ]  4775           if ((png_ptr->num_trans > 0) && (png_ptr->bit_depth == 8))
[ ]  4776           {
[ ]  4777              if (png_ptr->riffled_palette == NULL)
[ ]  4778              {
[ ]  4779                 /* Initialize the accelerated palette expansion. */
[ ]  4780                 png_ptr->riffled_palette =
[ ]  4781                     (png_bytep)png_malloc(png_ptr, 256 * 4);
[ ]  4782                 png_riffle_palette_neon(png_ptr);
[ ]  4783              }
[ ]  4784           }
[ ]  4785  #endif
[ ]  4786           png_do_expand_palette(png_ptr, row_info, png_ptr->row_buf + 1,
[ ]  4787               png_ptr->palette, png_ptr->trans_alpha, png_ptr->num_trans);
[ ]  4788        }
[ ]  4789  
[B]  4790        else
[B]  4791        {
[B]  4792           if (png_ptr->num_trans != 0 && <-- BLOCKER
[B]  4793               (png_ptr->transformations & PNG_EXPAND_tRNS) != 0)
[W]  4794              png_do_expand(row_info, png_ptr->row_buf + 1,
[W]  4795                  &(png_ptr->trans_color));
[ ]  4796  
[L]  4797           else
[L]  4798              png_do_expand(row_info, png_ptr->row_buf + 1, NULL);
[B]  4799        }
[B]  4800     }
[B]  4801  #endif
[ ]  4802  
[B]  4803  #ifdef PNG_READ_STRIP_ALPHA_SUPPORTED
[B]  4804     if ((png_ptr->transformations & PNG_STRIP_ALPHA) != 0 &&
[B]  4805         (png_ptr->transformations & PNG_COMPOSE) == 0 &&
[B]  4806         (row_info->color_type == PNG_COLOR_TYPE_RGB_ALPHA ||
[ ]  4807         row_info->color_type == PNG_COLOR_TYPE_GRAY_ALPHA))
[ ]  4808        png_do_strip_channel(row_info, png_ptr->row_buf + 1,
[ ]  4809            0 /* at_start == false, because SWAP_ALPHA happens later */);
[B]  4810  #endif
[ ]  4811  
[B]  4812  #ifdef PNG_READ_RGB_TO_GRAY_SUPPORTED
[B]  4813     if ((png_ptr->transformations & PNG_RGB_TO_GRAY) != 0)
[ ]  4814     {
[ ]  4815        int rgb_error =
[ ]  4816            png_do_rgb_to_gray(png_ptr, row_info,
[ ]  4817                png_ptr->row_buf + 1);
[ ]  4818  
[ ]  4819        if (rgb_error != 0)
[ ]  4820        {
[ ]  4821           png_ptr->rgb_to_gray_status=1;
[ ]  4822           if ((png_ptr->transformations & PNG_RGB_TO_GRAY) ==
[ ]  4823               PNG_RGB_TO_GRAY_WARN)
[ ]  4824              png_warning(png_ptr, "png_do_rgb_to_gray found nongray pixel");
[ ]  4825  
[ ]  4826           if ((png_ptr->transformations & PNG_RGB_TO_GRAY) ==
[ ]  4827               PNG_RGB_TO_GRAY_ERR)
[ ]  4828              png_error(png_ptr, "png_do_rgb_to_gray found nongray pixel");
[ ]  4829        }
[ ]  4830     }
[B]  4831  #endif
[ ]  4832  
[ ]  4833  /* From Andreas Dilger e-mail to png-implement, 26 March 1998:
[ ]  4834   *
[ ]  4835   *   In most cases, the "simple transparency" should be done prior to doing
[ ]  4836   *   gray-to-RGB, or you will have to test 3x as many bytes to check if a
[ ]  4837   *   pixel is transparent.  You would also need to make sure that the
[ ]  4838   *   transparency information is upgraded to RGB.
[ ]  4839   *
[ ]  4840   *   To summarize, the current flow is:
[ ]  4841   *   - Gray + simple transparency -> compare 1 or 2 gray bytes and composite
[ ]  4842   *                                   with background "in place" if transparent,
[ ]  4843   *                                   convert to RGB if necessary
[ ]  4844   *   - Gray + alpha -> composite with gray background and remove alpha bytes,
[ ]  4845   *                                   convert to RGB if necessary
[ ]  4846   *
[ ]  4847   *   To support RGB backgrounds for gray images we need:
[ ]  4848   *   - Gray + simple transparency -> convert to RGB + simple transparency,
[ ]  4849   *                                   compare 3 or 6 bytes and composite with
[ ]  4850   *                                   background "in place" if transparent
[ ]  4851   *                                   (3x compare/pixel compared to doing
[ ]  4852   *                                   composite with gray bkgrnd)
[ ]  4853   *   - Gray + alpha -> convert to RGB + alpha, composite with background and
[ ]  4854   *                                   remove alpha bytes (3x float
[ ]  4855   *                                   operations/pixel compared with composite
[ ]  4856   *                                   on gray background)
[ ]  4857   *
[ ]  4858   *  Greg's change will do this.  The reason it wasn't done before is for
[ ]  4859   *  performance, as this increases the per-pixel operations.  If we would check
[ ]  4860   *  in advance if the background was gray or RGB, and position the gray-to-RGB
[ ]  4861   *  transform appropriately, then it would save a lot of work/time.
[ ]  4862   */
[ ]  4863  
[B]  4864  #ifdef PNG_READ_GRAY_TO_RGB_SUPPORTED
[ ]  4865     /* If gray -> RGB, do so now only if background is non-gray; else do later
[ ]  4866      * for performance reasons
[ ]  4867      */
[B]  4868     if ((png_ptr->transformations & PNG_GRAY_TO_RGB) != 0 &&
[B]  4869         (png_ptr->mode & PNG_BACKGROUND_IS_GRAY) == 0)
[B]  4870        png_do_gray_to_rgb(row_info, png_ptr->row_buf + 1);
[B]  4871  #endif
[ ]  4872  
[B]  4873  #if defined(PNG_READ_BACKGROUND_SUPPORTED) ||\
[B]  4874     defined(PNG_READ_ALPHA_MODE_SUPPORTED)
[B]  4875     if ((png_ptr->transformations & PNG_COMPOSE) != 0)
[ ]  4876        png_do_compose(row_info, png_ptr->row_buf + 1, png_ptr);
[B]  4877  #endif
[ ]  4878  
[B]  4879  #ifdef PNG_READ_GAMMA_SUPPORTED
[B]  4880     if ((png_ptr->transformations & PNG_GAMMA) != 0 &&
[B]  4881  #ifdef PNG_READ_RGB_TO_GRAY_SUPPORTED
[ ]  4882        /* Because RGB_TO_GRAY does the gamma transform. */
[B]  4883        (png_ptr->transformations & PNG_RGB_TO_GRAY) == 0 &&
[B]  4884  #endif
[B]  4885  #if defined(PNG_READ_BACKGROUND_SUPPORTED) ||\
[B]  4886     defined(PNG_READ_ALPHA_MODE_SUPPORTED)
[ ]  4887        /* Because PNG_COMPOSE does the gamma transform if there is something to
[ ]  4888         * do (if there is an alpha channel or transparency.)
[ ]  4889         */
[B]  4890         !((png_ptr->transformations & PNG_COMPOSE) != 0 &&
[ ]  4891         ((png_ptr->num_trans != 0) ||
[ ]  4892         (png_ptr->color_type & PNG_COLOR_MASK_ALPHA) != 0)) &&
[B]  4893  #endif
[ ]  4894        /* Because png_init_read_transformations transforms the palette, unless
[ ]  4895         * RGB_TO_GRAY will do the transform.
[ ]  4896         */
[B]  4897         (png_ptr->color_type != PNG_COLOR_TYPE_PALETTE))
[ ]  4898        png_do_gamma(row_info, png_ptr->row_buf + 1, png_ptr);
[B]  4899  #endif
[ ]  4900  
[B]  4901  #ifdef PNG_READ_STRIP_ALPHA_SUPPORTED
[B]  4902     if ((png_ptr->transformations & PNG_STRIP_ALPHA) != 0 &&
[B]  4903         (png_ptr->transformations & PNG_COMPOSE) != 0 &&
[B]  4904         (row_info->color_type == PNG_COLOR_TYPE_RGB_ALPHA ||
[ ]  4905         row_info->color_type == PNG_COLOR_TYPE_GRAY_ALPHA))
[ ]  4906        png_do_strip_channel(row_info, png_ptr->row_buf + 1,
[ ]  4907            0 /* at_start == false, because SWAP_ALPHA happens later */);
[B]  4908  #endif
[ ]  4909  
[B]  4910  #ifdef PNG_READ_ALPHA_MODE_SUPPORTED
[B]  4911     if ((png_ptr->transformations & PNG_ENCODE_ALPHA) != 0 &&
[B]  4912         (row_info->color_type & PNG_COLOR_MASK_ALPHA) != 0)
[ ]  4913        png_do_encode_alpha(row_info, png_ptr->row_buf + 1, png_ptr);
[B]  4914  #endif
[ ]  4915  
[B]  4916  #ifdef PNG_READ_SCALE_16_TO_8_SUPPORTED
[B]  4917     if ((png_ptr->transformations & PNG_SCALE_16_TO_8) != 0)
[B]  4918        png_do_scale_16_to_8(row_info, png_ptr->row_buf + 1);
[B]  4919  #endif
[ ]  4920  
[B]  4921  #ifdef PNG_READ_STRIP_16_TO_8_SUPPORTED
[ ]  4922     /* There is no harm in doing both of these because only one has any effect,
[ ]  4923      * by putting the 'scale' option first if the app asks for scale (either by
[ ]  4924      * calling the API or in a TRANSFORM flag) this is what happens.
[ ]  4925      */
[B]  4926     if ((png_ptr->transformations & PNG_16_TO_8) != 0)
[ ]  4927        png_do_chop(row_info, png_ptr->row_buf + 1);
[B]  4928  #endif
[ ]  4929  
[B]  4930  #ifdef PNG_READ_QUANTIZE_SUPPORTED
[B]  4931     if ((png_ptr->transformations & PNG_QUANTIZE) != 0)
[ ]  4932     {
[ ]  4933        png_do_quantize(row_info, png_ptr->row_buf + 1,
[ ]  4934            png_ptr->palette_lookup, png_ptr->quantize_index);
[ ]  4935  
[ ]  4936        if (row_info->rowbytes == 0)
[ ]  4937           png_error(png_ptr, "png_do_quantize returned rowbytes=0");
[ ]  4938     }
[B]  4939  #endif /* READ_QUANTIZE */
[ ]  4940  
[B]  4941  #ifdef PNG_READ_EXPAND_16_SUPPORTED
[ ]  4942     /* Do the expansion now, after all the arithmetic has been done.  Notice
[ ]  4943      * that previous transformations can handle the PNG_EXPAND_16 flag if this
[ ]  4944      * is efficient (particularly true in the case of gamma correction, where
[ ]  4945      * better accuracy results faster!)
[ ]  4946      */
[B]  4947     if ((png_ptr->transformations & PNG_EXPAND_16) != 0)
[ ]  4948        png_do_expand_16(row_info, png_ptr->row_buf + 1);
[B]  4949  #endif
[ ]  4950  
[B]  4951  #ifdef PNG_READ_GRAY_TO_RGB_SUPPORTED
[ ]  4952     /* NOTE: moved here in 1.5.4 (from much later in this list.) */
[B]  4953     if ((png_ptr->transformations & PNG_GRAY_TO_RGB) != 0 &&
[B]  4954         (png_ptr->mode & PNG_BACKGROUND_IS_GRAY) != 0)
[ ]  4955        png_do_gray_to_rgb(row_info, png_ptr->row_buf + 1);
[B]  4956  #endif
[ ]  4957  
[B]  4958  #ifdef PNG_READ_INVERT_SUPPORTED
[B]  4959     if ((png_ptr->transformations & PNG_INVERT_MONO) != 0)
[ ]  4960        png_do_invert(row_info, png_ptr->row_buf + 1);
[B]  4961  #endif
[ ]  4962  
[B]  4963  #ifdef PNG_READ_INVERT_ALPHA_SUPPORTED
[B]  4964     if ((png_ptr->transformations & PNG_INVERT_ALPHA) != 0)
[ ]  4965        png_do_read_invert_alpha(row_info, png_ptr->row_buf + 1);
[B]  4966  #endif
[ ]  4967  
[B]  4968  #ifdef PNG_READ_SHIFT_SUPPORTED
[B]  4969     if ((png_ptr->transformations & PNG_SHIFT) != 0)
[ ]  4970        png_do_unshift(row_info, png_ptr->row_buf + 1,
[ ]  4971            &(png_ptr->shift));
[B]  4972  #endif
[ ]  4973  
[B]  4974  #ifdef PNG_READ_PACK_SUPPORTED
[B]  4975     if ((png_ptr->transformations & PNG_PACK) != 0)
[L]  4976        png_do_unpack(row_info, png_ptr->row_buf + 1);
[B]  4977  #endif
[ ]  4978  
[B]  4979  #ifdef PNG_READ_CHECK_FOR_INVALID_INDEX_SUPPORTED
[ ]  4980     /* Added at libpng-1.5.10 */
[B]  4981     if (row_info->color_type == PNG_COLOR_TYPE_PALETTE &&
[B]  4982         png_ptr->num_palette_max >= 0)
[ ]  4983        png_do_check_palette_indexes(png_ptr, row_info);
[B]  4984  #endif
[ ]  4985  
[B]  4986  #ifdef PNG_READ_BGR_SUPPORTED
[B]  4987     if ((png_ptr->transformations & PNG_BGR) != 0)
[ ]  4988        png_do_bgr(row_info, png_ptr->row_buf + 1);
[B]  4989  #endif
[ ]  4990  
[B]  4991  #ifdef PNG_READ_PACKSWAP_SUPPORTED
[B]  4992     if ((png_ptr->transformations & PNG_PACKSWAP) != 0)
[ ]  4993        png_do_packswap(row_info, png_ptr->row_buf + 1);
[B]  4994  #endif
[ ]  4995  
[B]  4996  #ifdef PNG_READ_FILLER_SUPPORTED
[B]  4997     if ((png_ptr->transformations & PNG_FILLER) != 0)
[ ]  4998        png_do_read_filler(row_info, png_ptr->row_buf + 1,
[ ]  4999            (png_uint_32)png_ptr->filler, png_ptr->flags);
[B]  5000  #endif
[ ]  5001  
[B]  5002  #ifdef PNG_READ_SWAP_ALPHA_SUPPORTED
[B]  5003     if ((png_ptr->transformations & PNG_SWAP_ALPHA) != 0)
[ ]  5004        png_do_read_swap_alpha(row_info, png_ptr->row_buf + 1);
[B]  5005  #endif
[ ]  5006  
[B]  5007  #ifdef PNG_READ_16BIT_SUPPORTED
[B]  5008  #ifdef PNG_READ_SWAP_SUPPORTED
[B]  5009     if ((png_ptr->transformations & PNG_SWAP_BYTES) != 0)
[ ]  5010        png_do_swap(row_info, png_ptr->row_buf + 1);
[B]  5011  #endif
[B]  5012  #endif
[ ]  5013  
[B]  5014  #ifdef PNG_READ_USER_TRANSFORM_SUPPORTED
[B]  5015     if ((png_ptr->transformations & PNG_USER_TRANSFORM) != 0)
[ ]  5016     {
[ ]  5017        if (png_ptr->read_user_transform_fn != NULL)
[ ]  5018           (*(png_ptr->read_user_transform_fn)) /* User read transform function */
[ ]  5019               (png_ptr,     /* png_ptr */
[ ]  5020               row_info,     /* row_info: */
[ ]  5021                  /*  png_uint_32 width;       width of row */
[ ]  5022                  /*  size_t rowbytes;         number of bytes in row */
[ ]  5023                  /*  png_byte color_type;     color type of pixels */
[ ]  5024                  /*  png_byte bit_depth;      bit depth of samples */
[ ]  5025                  /*  png_byte channels;       number of channels (1-4) */
[ ]  5026                  /*  png_byte pixel_depth;    bits per pixel (depth*channels) */
[ ]  5027               png_ptr->row_buf + 1);    /* start of pixel data for row */
[ ]  5028  #ifdef PNG_USER_TRANSFORM_PTR_SUPPORTED
[ ]  5029        if (png_ptr->user_transform_depth != 0)
[ ]  5030           row_info->bit_depth = png_ptr->user_transform_depth;
[ ]  5031  
[ ]  5032        if (png_ptr->user_transform_channels != 0)
[ ]  5033           row_info->channels = png_ptr->user_transform_channels;
[ ]  5034  #endif
[ ]  5035        row_info->pixel_depth = (png_byte)(row_info->bit_depth *
[ ]  5036            row_info->channels);
[ ]  5037  
[ ]  5038        row_info->rowbytes = PNG_ROWBYTES(row_info->pixel_depth, row_info->width);
[ ]  5039     }
[B]  5040  #endif
[B]  5041  }

--- No 1-hop callers of OSS_FUZZ_png_do_read_transformations fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     181       702  pngrtran.c:png_do_scale_16_to_8  (/src/libpng/pngrtran.c:2390-2442)
     181       702  pngrtran.c:png_do_gray_to_rgb  (/src/libpng/pngrtran.c:2861-2942)
     181       702  pngrtran.c:png_do_expand  (/src/libpng/pngrtran.c:4385-4605)
     181       702  OSS_FUZZ_png_do_read_transformations  (/src/libpng/pngrtran.c:4741-5041)  <-- enclosing
       0        46  pngrtran.c:png_do_unpack  (/src/libpng/pngrtran.c:2153-2240)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_do_read_transformations  (/src/libpng/pngrtran.c:4741-5041) ---
  d=1   L4744  T=0 F=181  T=0 F=702  if (png_ptr->row_buf == NULL)
  d=1   L4759  T=181 F=0  T=702 F=0  if ((png_ptr->flags & PNG_FLAG_DETECT_UNINITIALIZED) != 0 &&
  d=1   L4760  T=0 F=181  T=0 F=702  (png_ptr->flags & PNG_FLAG_ROW_INIT) == 0)
  d=1   L4770  T=181 F=0  T=702 F=0  if ((png_ptr->transformations & PNG_EXPAND) != 0)
  d=1   L4772  T=0 F=181  T=0 F=702  if (row_info->color_type == PNG_COLOR_TYPE_PALETTE)
  d=1   L4792  T=181 F=0  T=0 F=702  if (png_ptr->num_trans != 0 &&  <-- BLOCKER
  d=1   L4793  T=181 F=0  T=0 F=0  (png_ptr->transformations & PNG_EXPAND_tRNS) != 0)
  d=1   L4804  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_STRIP_ALPHA) != 0 &&
  d=1   L4813  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_RGB_TO_GRAY) != 0)
  d=1   L4868  T=181 F=0  T=702 F=0  if ((png_ptr->transformations & PNG_GRAY_TO_RGB) != 0 &&
  d=1   L4869  T=181 F=0  T=702 F=0  (png_ptr->mode & PNG_BACKGROUND_IS_GRAY) == 0)
  d=1   L4875  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_COMPOSE) != 0)
  d=1   L4880  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_GAMMA) != 0 &&
  d=1   L4902  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_STRIP_ALPHA) != 0 &&
  d=1   L4911  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_ENCODE_ALPHA) != 0 &&
  d=1   L4917  T=181 F=0  T=702 F=0  if ((png_ptr->transformations & PNG_SCALE_16_TO_8) != 0)
  d=1   L4926  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_16_TO_8) != 0)
  d=1   L4931  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_QUANTIZE) != 0)
  d=1   L4947  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_EXPAND_16) != 0)
  d=1   L4953  T=181 F=0  T=702 F=0  if ((png_ptr->transformations & PNG_GRAY_TO_RGB) != 0 &&
  d=1   L4954  T=0 F=181  T=0 F=702  (png_ptr->mode & PNG_BACKGROUND_IS_GRAY) != 0)
  d=1   L4959  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_INVERT_MONO) != 0)
  d=1   L4964  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_INVERT_ALPHA) != 0)
  d=1   L4969  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_SHIFT) != 0)
  d=1   L4975  T=0 F=181  T=46 F=656  if ((png_ptr->transformations & PNG_PACK) != 0)
  d=1   L4981  T=0 F=181  T=0 F=702  if (row_info->color_type == PNG_COLOR_TYPE_PALETTE &&
  d=1   L4987  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_BGR) != 0)
  d=1   L4992  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_PACKSWAP) != 0)
  d=1   L4997  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_FILLER) != 0)
  d=1   L5003  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_SWAP_ALPHA) != 0)
  d=1   L5009  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_SWAP_BYTES) != 0)
  d=1   L5015  T=0 F=181  T=0 F=702  if ((png_ptr->transformations & PNG_USER_TRANSFORM) != 0)

[off-chain: 46 additional divergent branches across 6 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=230924cbdaa2cc5c, size=8774 bytes, fuzzer=cmplog, trial=1, discovered_at=18s, mutation_op=WordInterestingMutator,ByteDecMutator,WordInterestingMutator,BytesRandSetMutator,ByteDecMutator,BytesRandSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 02 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=1bced5c0274223ea, size=9194 bytes, fuzzer=cmplog, trial=1, discovered_at=455s, mutation_op=DwordAddMutator,BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 02 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=0ccd2e36a91a32e2, size=9209 bytes, fuzzer=cmplog, trial=1, discovered_at=1141s, mutation_op=BytesExpandMutator,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 20 00 00 00 01 08 02 00 00 01 52 ed aa   ... .........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=228f85d2366b8b60, size=9194 bytes, fuzzer=cmplog, trial=1, discovered_at=1488s, mutation_op=ByteInterestingMutator,CrossoverReplaceMutator,DwordInterestingMutator,TokenReplace,BytesCopyMutator,ByteRandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 03 00 00 00 01 08 02 00 00 01 52 ed aa   .............R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=1908a0cb5df50d33, size=9201 bytes, fuzzer=cmplog, trial=1, discovered_at=6097s, mutation_op=BytesCopyMutator,TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 01 08 02 00 00 01 52 ed aa   ...[.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
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
   0x0015  00(.)x9 0f(.)x1                     00(.)x10                            PARTIAL
   0x0016  00(.)x8 85(.)x1 42(B)x1             00(.)x4 a0(.)x3 80(.)x2 02(.)x1     PARTIAL
   0x0017  45(E)x4 01(.)x4 85(.)x1 40(@)x1     00(.)x3 86(.)x2 02(.)x1 03(.)x1 +3u  PARTIAL
   0x0018  08(.)x10                            10(.)x4 04(.)x3 02(.)x1 08(.)x1 +1u  PARTIAL
   0x0019  02(.)x10                            00(.)x8 04(.)x2                     DIFFER
   0x001d  52(R)x10                            7f(.)x5 00(.)x4 ff(.)x1             DIFFER
   0x001e  ed(.)x10                            ed(.)x6 ff(.)x2 00(.)x2             PARTIAL
   0x002d  0b(.)x10                            0b(.)x8 aa(.)x1 1b(.)x1             PARTIAL
   0x002e  fc(.)x10                            fc(.)x5 04(.)x4 56(V)x1             PARTIAL
   0x002f  61(a)x10                            61(a)x9 aa(.)x1                     PARTIAL
   0x0030  05(.)x9 00(.)x1                     05(.)x9 aa(.)x1                     PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3933.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3933,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3933 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3933 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3933 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).