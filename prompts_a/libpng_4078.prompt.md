==== BLOCKER ====
Target: libpng
Branch ID: 4078
Location: /src/libpng/pngrutil.c:4457:11
Enclosing function: OSS_FUZZ_png_read_start_row
Source line:       if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
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
Source: db/per_role_coverage/libpng/4078/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_read_start_row (/src/libpng/pngrutil.c:4393-4680) ---
[ ]  4391  void /* PRIVATE */
[ ]  4392  png_read_start_row(png_structrp png_ptr)
[B]  4393  {
[ ]  4394     /* Arrays to facilitate easy interlacing - use pass (0 - 6) as index */
[ ]  4395  
[ ]  4396     /* Start of interlace block */
[B]  4397     static const png_byte png_pass_start[7] = {0, 4, 0, 2, 0, 1, 0};
[ ]  4398  
[ ]  4399     /* Offset to next interlace block */
[B]  4400     static const png_byte png_pass_inc[7] = {8, 8, 4, 4, 2, 2, 1};
[ ]  4401  
[ ]  4402     /* Start of interlace block in the y direction */
[B]  4403     static const png_byte png_pass_ystart[7] = {0, 0, 4, 0, 2, 0, 1};
[ ]  4404  
[ ]  4405     /* Offset to next interlace block in the y direction */
[B]  4406     static const png_byte png_pass_yinc[7] = {8, 8, 8, 4, 4, 2, 2};
[ ]  4407  
[B]  4408     unsigned int max_pixel_depth;
[B]  4409     size_t row_bytes;
[ ]  4410  
[B]  4411     png_debug(1, "in png_read_start_row");
[ ]  4412  
[B]  4413  #ifdef PNG_READ_TRANSFORMS_SUPPORTED
[B]  4414     png_init_read_transformations(png_ptr);
[B]  4415  #endif
[B]  4416     if (png_ptr->interlaced != 0)
[B]  4417     {
[B]  4418        if ((png_ptr->transformations & PNG_INTERLACE) == 0)
[ ]  4419           png_ptr->num_rows = (png_ptr->height + png_pass_yinc[0] - 1 -
[ ]  4420               png_pass_ystart[0]) / png_pass_yinc[0];
[ ]  4421  
[B]  4422        else
[B]  4423           png_ptr->num_rows = png_ptr->height;
[ ]  4424  
[B]  4425        png_ptr->iwidth = (png_ptr->width +
[B]  4426            png_pass_inc[png_ptr->pass] - 1 -
[B]  4427            png_pass_start[png_ptr->pass]) /
[B]  4428            png_pass_inc[png_ptr->pass];
[B]  4429     }
[ ]  4430  
[B]  4431     else
[B]  4432     {
[B]  4433        png_ptr->num_rows = png_ptr->height;
[B]  4434        png_ptr->iwidth = png_ptr->width;
[B]  4435     }
[ ]  4436  
[B]  4437     max_pixel_depth = (unsigned int)png_ptr->pixel_depth;
[ ]  4438  
[ ]  4439     /* WARNING: * png_read_transform_info (pngrtran.c) performs a simpler set of
[ ]  4440      * calculations to calculate the final pixel depth, then
[ ]  4441      * png_do_read_transforms actually does the transforms.  This means that the
[ ]  4442      * code which effectively calculates this value is actually repeated in three
[ ]  4443      * separate places.  They must all match.  Innocent changes to the order of
[ ]  4444      * transformations can and will break libpng in a way that causes memory
[ ]  4445      * overwrites.
[ ]  4446      *
[ ]  4447      * TODO: fix this.
[ ]  4448      */
[B]  4449  #ifdef PNG_READ_PACK_SUPPORTED
[B]  4450     if ((png_ptr->transformations & PNG_PACK) != 0 && png_ptr->bit_depth < 8)
[B]  4451        max_pixel_depth = 8;
[B]  4452  #endif
[ ]  4453  
[B]  4454  #ifdef PNG_READ_EXPAND_SUPPORTED
[B]  4455     if ((png_ptr->transformations & PNG_EXPAND) != 0)
[B]  4456     {
[B]  4457        if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE) <-- BLOCKER
[W]  4458        {
[W]  4459           if (png_ptr->num_trans != 0)
[W]  4460              max_pixel_depth = 32;
[ ]  4461  
[W]  4462           else
[W]  4463              max_pixel_depth = 24;
[W]  4464        }
[ ]  4465  
[L]  4466        else if (png_ptr->color_type == PNG_COLOR_TYPE_GRAY)
[L]  4467        {
[L]  4468           if (max_pixel_depth < 8)
[ ]  4469              max_pixel_depth = 8;
[ ]  4470  
[L]  4471           if (png_ptr->num_trans != 0)
[ ]  4472              max_pixel_depth *= 2;
[L]  4473        }
[ ]  4474  
[L]  4475        else if (png_ptr->color_type == PNG_COLOR_TYPE_RGB)
[ ]  4476        {
[ ]  4477           if (png_ptr->num_trans != 0)
[ ]  4478           {
[ ]  4479              max_pixel_depth *= 4;
[ ]  4480              max_pixel_depth /= 3;
[ ]  4481           }
[ ]  4482        }
[B]  4483     }
[B]  4484  #endif
[ ]  4485  
[B]  4486  #ifdef PNG_READ_EXPAND_16_SUPPORTED
[B]  4487     if ((png_ptr->transformations & PNG_EXPAND_16) != 0)
[ ]  4488     {
[ ]  4489  #  ifdef PNG_READ_EXPAND_SUPPORTED
[ ]  4490        /* In fact it is an error if it isn't supported, but checking is
[ ]  4491         * the safe way.
[ ]  4492         */
[ ]  4493        if ((png_ptr->transformations & PNG_EXPAND) != 0)
[ ]  4494        {
[ ]  4495           if (png_ptr->bit_depth < 16)
[ ]  4496              max_pixel_depth *= 2;
[ ]  4497        }
[ ]  4498        else
[ ]  4499  #  endif
[ ]  4500        png_ptr->transformations &= ~PNG_EXPAND_16;
[ ]  4501     }
[B]  4502  #endif
[ ]  4503  
[B]  4504  #ifdef PNG_READ_FILLER_SUPPORTED
[B]  4505     if ((png_ptr->transformations & (PNG_FILLER)) != 0)
[ ]  4506     {
[ ]  4507        if (png_ptr->color_type == PNG_COLOR_TYPE_GRAY)
[ ]  4508        {
[ ]  4509           if (max_pixel_depth <= 8)
[ ]  4510              max_pixel_depth = 16;
[ ]  4511  
[ ]  4512           else
[ ]  4513              max_pixel_depth = 32;
[ ]  4514        }
[ ]  4515  
[ ]  4516        else if (png_ptr->color_type == PNG_COLOR_TYPE_RGB ||
[ ]  4517           png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
[ ]  4518        {
[ ]  4519           if (max_pixel_depth <= 32)
[ ]  4520              max_pixel_depth = 32;
[ ]  4521  
[ ]  4522           else
[ ]  4523              max_pixel_depth = 64;
[ ]  4524        }
[ ]  4525     }
[B]  4526  #endif
[ ]  4527  
[B]  4528  #ifdef PNG_READ_GRAY_TO_RGB_SUPPORTED
[B]  4529     if ((png_ptr->transformations & PNG_GRAY_TO_RGB) != 0)
[B]  4530     {
[B]  4531        if (
[B]  4532  #ifdef PNG_READ_EXPAND_SUPPORTED
[B]  4533            (png_ptr->num_trans != 0 &&
[B]  4534            (png_ptr->transformations & PNG_EXPAND) != 0) ||
[B]  4535  #endif
[B]  4536  #ifdef PNG_READ_FILLER_SUPPORTED
[B]  4537            (png_ptr->transformations & (PNG_FILLER)) != 0 ||
[B]  4538  #endif
[B]  4539            png_ptr->color_type == PNG_COLOR_TYPE_GRAY_ALPHA)
[B]  4540        {
[B]  4541           if (max_pixel_depth <= 16)
[L]  4542              max_pixel_depth = 32;
[ ]  4543  
[B]  4544           else
[B]  4545              max_pixel_depth = 64;
[B]  4546        }
[ ]  4547  
[B]  4548        else
[B]  4549        {
[B]  4550           if (max_pixel_depth <= 8)
[L]  4551           {
[L]  4552              if (png_ptr->color_type == PNG_COLOR_TYPE_RGB_ALPHA)
[ ]  4553                 max_pixel_depth = 32;
[ ]  4554  
[L]  4555              else
[L]  4556                 max_pixel_depth = 24;
[L]  4557           }
[ ]  4558  
[B]  4559           else if (png_ptr->color_type == PNG_COLOR_TYPE_RGB_ALPHA)
[ ]  4560              max_pixel_depth = 64;
[ ]  4561  
[B]  4562           else
[B]  4563              max_pixel_depth = 48;
[B]  4564        }
[B]  4565     }
[B]  4566  #endif
[ ]  4567  
[B]  4568  #if defined(PNG_READ_USER_TRANSFORM_SUPPORTED) && \
[B]  4569  defined(PNG_USER_TRANSFORM_PTR_SUPPORTED)
[B]  4570     if ((png_ptr->transformations & PNG_USER_TRANSFORM) != 0)
[ ]  4571     {
[ ]  4572        unsigned int user_pixel_depth = png_ptr->user_transform_depth *
[ ]  4573           png_ptr->user_transform_channels;
[ ]  4574  
[ ]  4575        if (user_pixel_depth > max_pixel_depth)
[ ]  4576           max_pixel_depth = user_pixel_depth;
[ ]  4577     }
[B]  4578  #endif
[ ]  4579  
[ ]  4580     /* This value is stored in png_struct and double checked in the row read
[ ]  4581      * code.
[ ]  4582      */
[B]  4583     png_ptr->maximum_pixel_depth = (png_byte)max_pixel_depth;
[B]  4584     png_ptr->transformed_pixel_depth = 0; /* calculated on demand */
[ ]  4585  
[ ]  4586     /* Align the width on the next larger 8 pixels.  Mainly used
[ ]  4587      * for interlacing
[ ]  4588      */
[B]  4589     row_bytes = ((png_ptr->width + 7) & ~((png_uint_32)7));
[ ]  4590     /* Calculate the maximum bytes needed, adding a byte and a pixel
[ ]  4591      * for safety's sake
[ ]  4592      */
[B]  4593     row_bytes = PNG_ROWBYTES(max_pixel_depth, row_bytes) +
[B]  4594         1 + ((max_pixel_depth + 7) >> 3U);
[ ]  4595  
[ ]  4596  #ifdef PNG_MAX_MALLOC_64K
[ ]  4597     if (row_bytes > (png_uint_32)65536L)
[ ]  4598        png_error(png_ptr, "This image requires a row greater than 64KB");
[ ]  4599  #endif
[ ]  4600  
[B]  4601     if (row_bytes + 48 > png_ptr->old_big_row_buf_size)
[B]  4602     {
[B]  4603        png_free(png_ptr, png_ptr->big_row_buf);
[B]  4604        png_free(png_ptr, png_ptr->big_prev_row);
[ ]  4605  
[B]  4606        if (png_ptr->interlaced != 0)
[B]  4607           png_ptr->big_row_buf = (png_bytep)png_calloc(png_ptr,
[B]  4608               row_bytes + 48);
[ ]  4609  
[B]  4610        else
[B]  4611           png_ptr->big_row_buf = (png_bytep)png_malloc(png_ptr, row_bytes + 48);
[ ]  4612  
[B]  4613        png_ptr->big_prev_row = (png_bytep)png_malloc(png_ptr, row_bytes + 48);
[ ]  4614  
[B]  4615  #ifdef PNG_ALIGNED_MEMORY_SUPPORTED
[ ]  4616        /* Use 16-byte aligned memory for row_buf with at least 16 bytes
[ ]  4617         * of padding before and after row_buf; treat prev_row similarly.
[ ]  4618         * NOTE: the alignment is to the start of the pixels, one beyond the start
[ ]  4619         * of the buffer, because of the filter byte.  Prior to libpng 1.5.6 this
[ ]  4620         * was incorrect; the filter byte was aligned, which had the exact
[ ]  4621         * opposite effect of that intended.
[ ]  4622         */
[B]  4623        {
[B]  4624           png_bytep temp = png_ptr->big_row_buf + 32;
[B]  4625           size_t extra = (size_t)temp & 0x0f;
[B]  4626           png_ptr->row_buf = temp - extra - 1/*filter byte*/;
[ ]  4627  
[B]  4628           temp = png_ptr->big_prev_row + 32;
[B]  4629           extra = (size_t)temp & 0x0f;
[B]  4630           png_ptr->prev_row = temp - extra - 1/*filter byte*/;
[B]  4631        }
[ ]  4632  #else
[ ]  4633        /* Use 31 bytes of padding before and 17 bytes after row_buf. */
[ ]  4634        png_ptr->row_buf = png_ptr->big_row_buf + 31;
[ ]  4635        png_ptr->prev_row = png_ptr->big_prev_row + 31;
[ ]  4636  #endif
[B]  4637        png_ptr->old_big_row_buf_size = row_bytes + 48;
[B]  4638     }
[ ]  4639  
[ ]  4640  #ifdef PNG_MAX_MALLOC_64K
[ ]  4641     if (png_ptr->rowbytes > 65535)
[ ]  4642        png_error(png_ptr, "This image requires a row greater than 64KB");
[ ]  4643  
[ ]  4644  #endif
[B]  4645     if (png_ptr->rowbytes > (PNG_SIZE_MAX - 1))
[ ]  4646        png_error(png_ptr, "Row has too many bytes to allocate in memory");
[ ]  4647  
[B]  4648     memset(png_ptr->prev_row, 0, png_ptr->rowbytes + 1);
[ ]  4649  
[B]  4650     png_debug1(3, "width = %u,", png_ptr->width);
[B]  4651     png_debug1(3, "height = %u,", png_ptr->height);
[B]  4652     png_debug1(3, "iwidth = %u,", png_ptr->iwidth);
[B]  4653     png_debug1(3, "num_rows = %u,", png_ptr->num_rows);
[B]  4654     png_debug1(3, "rowbytes = %lu,", (unsigned long)png_ptr->rowbytes);
[B]  4655     png_debug1(3, "irowbytes = %lu",
[B]  4656         (unsigned long)PNG_ROWBYTES(png_ptr->pixel_depth, png_ptr->iwidth) + 1);
[ ]  4657  
[ ]  4658     /* The sequential reader needs a buffer for IDAT, but the progressive reader
[ ]  4659      * does not, so free the read buffer now regardless; the sequential reader
[ ]  4660      * reallocates it on demand.
[ ]  4661      */
[B]  4662     if (png_ptr->read_buffer != NULL)
[B]  4663     {
[B]  4664        png_bytep buffer = png_ptr->read_buffer;
[ ]  4665  
[B]  4666        png_ptr->read_buffer_size = 0;
[B]  4667        png_ptr->read_buffer = NULL;
[B]  4668        png_free(png_ptr, buffer);
[B]  4669     }
[ ]  4670  
[ ]  4671     /* Finally claim the zstream for the inflate of the IDAT data, use the bits
[ ]  4672      * value from the stream (note that this will result in a fatal error if the
[ ]  4673      * IDAT stream has a bogus deflate header window_bits value, but this should
[ ]  4674      * not be happening any longer!)
[ ]  4675      */
[B]  4676     if (png_inflate_claim(png_ptr, png_IDAT) != Z_OK)
[ ]  4677        png_error(png_ptr, png_ptr->zstream.msg);
[ ]  4678  
[B]  4679     png_ptr->flags |= PNG_FLAG_ROW_INIT;
[B]  4680  }

--- No 1-hop callers of OSS_FUZZ_png_read_start_row fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     297      6140  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
       7       588  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
     130       605  OSS_FUZZ_png_read_filter_row  (/src/libpng/pngrutil.c:4134-4146)
       0       391  pngrutil.c:png_read_filter_row_paeth_multibyte_pixel  (/src/libpng/pngrutil.c:4046-4092)
       0       184  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
      71         0  pngrutil.c:png_read_filter_row_paeth_1byte_pixel  (/src/libpng/pngrutil.c:3995-4041)
      59         1  pngrutil.c:png_read_filter_row_avg  (/src/libpng/pngrutil.c:3968-3990)
      72        18  pngrutil.c:png_get_fixed_point  (/src/libpng/pngrutil.c:42-53)
       0        29  pngrutil.c:png_read_filter_row_sub  (/src/libpng/pngrutil.c:3934-3947)
      10         0  OSS_FUZZ_png_handle_PLTE  (/src/libpng/pngrutil.c:913-1096)
      12         2  OSS_FUZZ_png_handle_oFFs  (/src/libpng/pngrutil.c:2202-2242)
       6         0  OSS_FUZZ_png_handle_tRNS  (/src/libpng/pngrutil.c:1817-1915)
       0         6  OSS_FUZZ_png_read_finish_IDAT  (/src/libpng/pngrutil.c:4280-4324)
       4         0  OSS_FUZZ_png_handle_eXIf  (/src/libpng/pngrutil.c:2039-2097)
       6         2  OSS_FUZZ_png_handle_zTXt  (/src/libpng/pngrutil.c:2598-2708)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_read_start_row  (/src/libpng/pngrutil.c:4393-4680) ---
  d=1   L4418  T=0 F=3  T=0 F=9  if ((png_ptr->transformations & PNG_INTERLACE) == 0)
  d=1   L4457  T=10 F=0  T=0 F=10  if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)  <-- BLOCKER
  d=1   L4459  T=2 F=8  T=0 F=0  if (png_ptr->num_trans != 0)
  d=1   L4466  T=0 F=0  T=8 F=2  else if (png_ptr->color_type == PNG_COLOR_TYPE_GRAY)
  d=1   L4468  T=0 F=0  T=0 F=8  if (max_pixel_depth < 8)
  d=1   L4471  T=0 F=0  T=0 F=8  if (png_ptr->num_trans != 0)
  d=1   L4475  T=0 F=0  T=0 F=2  else if (png_ptr->color_type == PNG_COLOR_TYPE_RGB)
  d=1   L4533  T=2 F=8  T=0 F=10  (png_ptr->num_trans != 0 &&
  d=1   L4534  T=2 F=0  T=0 F=0  (png_ptr->transformations & PNG_EXPAND) != 0) ||
  d=1   L4539  T=0 F=8  T=2 F=8  png_ptr->color_type == PNG_COLOR_TYPE_GRAY_ALPHA)
  d=1   L4541  T=0 F=2  T=1 F=1  if (max_pixel_depth <= 16)
  d=1   L4550  T=0 F=8  T=5 F=3  if (max_pixel_depth <= 8)
  d=1   L4552  T=0 F=0  T=0 F=5  if (png_ptr->color_type == PNG_COLOR_TYPE_RGB_ALPHA)
  d=1   L4559  T=0 F=8  T=0 F=3  else if (png_ptr->color_type == PNG_COLOR_TYPE_RGB_ALPHA)

[off-chain: 207 additional divergent branches across 36 functions (see HIT-COUNT DIVERGENCE for which functions)]

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
  /home/miao/BlockerAnalyzer/prompts/libpng_4078.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4078,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4078 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4078 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4078 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).