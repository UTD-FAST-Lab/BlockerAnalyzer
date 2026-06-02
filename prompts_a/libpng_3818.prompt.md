==== BLOCKER ====
Target: libpng
Branch ID: 3818
Location: /src/libpng/png.c:674:8
Enclosing function: OSS_FUZZ_png_free_data
Source line:    if (num != -1)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog); loser (value_profile vs value_profile)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                   10        0          0  winner (value_profile vs naive)
value_profile_cmplog             ?        ?          ?  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.00h  loser=24.00h
  avg hitcount on branch: winner=156  loser=0
  prob_div=1.00  dur_div=24.00h  hit_div=156
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002
--- Pair 2: value_profile > naive  [delta: value_profile] ---
  subject 22  (value_profile vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.90h  loser=24.00h
  avg hitcount on branch: winner=77  loser=0
  prob_div=1.00  dur_div=19.10h  hit_div=77
  subject-level: delta_AUC=16855020.0  p_AUC=0.0002  delta_Final=254.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3818/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_free_data (/src/libpng/png.c:473-678) ---
[ ]   471  png_free_data(png_const_structrp png_ptr, png_inforp info_ptr, png_uint_32 mask,
[ ]   472      int num)
[B]   473  {
[B]   474     png_debug(1, "in png_free_data");
[ ]   475  
[B]   476     if (png_ptr == NULL || info_ptr == NULL)
[ ]   477        return;
[ ]   478  
[B]   479  #ifdef PNG_TEXT_SUPPORTED
[ ]   480     /* Free text item num or (if num == -1) all text items */
[B]   481     if (info_ptr->text != NULL &&
[B]   482         ((mask & PNG_FREE_TEXT) & info_ptr->free_me) != 0)
[B]   483     {
[B]   484        if (num != -1)
[ ]   485        {
[ ]   486           png_free(png_ptr, info_ptr->text[num].key);
[ ]   487           info_ptr->text[num].key = NULL;
[ ]   488        }
[ ]   489  
[B]   490        else
[B]   491        {
[B]   492           int i;
[ ]   493  
[B]   494           for (i = 0; i < info_ptr->num_text; i++)
[B]   495              png_free(png_ptr, info_ptr->text[i].key);
[ ]   496  
[B]   497           png_free(png_ptr, info_ptr->text);
[B]   498           info_ptr->text = NULL;
[B]   499           info_ptr->num_text = 0;
[B]   500           info_ptr->max_text = 0;
[B]   501        }
[B]   502     }
[B]   503  #endif
[ ]   504  
[B]   505  #ifdef PNG_tRNS_SUPPORTED
[ ]   506     /* Free any tRNS entry */
[B]   507     if (((mask & PNG_FREE_TRNS) & info_ptr->free_me) != 0)
[W]   508     {
[W]   509        info_ptr->valid &= ~PNG_INFO_tRNS;
[W]   510        png_free(png_ptr, info_ptr->trans_alpha);
[W]   511        info_ptr->trans_alpha = NULL;
[W]   512        info_ptr->num_trans = 0;
[W]   513     }
[B]   514  #endif
[ ]   515  
[B]   516  #ifdef PNG_sCAL_SUPPORTED
[ ]   517     /* Free any sCAL entry */
[B]   518     if (((mask & PNG_FREE_SCAL) & info_ptr->free_me) != 0)
[B]   519     {
[B]   520        png_free(png_ptr, info_ptr->scal_s_width);
[B]   521        png_free(png_ptr, info_ptr->scal_s_height);
[B]   522        info_ptr->scal_s_width = NULL;
[B]   523        info_ptr->scal_s_height = NULL;
[B]   524        info_ptr->valid &= ~PNG_INFO_sCAL;
[B]   525     }
[B]   526  #endif
[ ]   527  
[B]   528  #ifdef PNG_pCAL_SUPPORTED
[ ]   529     /* Free any pCAL entry */
[B]   530     if (((mask & PNG_FREE_PCAL) & info_ptr->free_me) != 0)
[B]   531     {
[B]   532        png_free(png_ptr, info_ptr->pcal_purpose);
[B]   533        png_free(png_ptr, info_ptr->pcal_units);
[B]   534        info_ptr->pcal_purpose = NULL;
[B]   535        info_ptr->pcal_units = NULL;
[ ]   536  
[B]   537        if (info_ptr->pcal_params != NULL)
[B]   538           {
[B]   539              int i;
[ ]   540  
[B]   541              for (i = 0; i < info_ptr->pcal_nparams; i++)
[B]   542                 png_free(png_ptr, info_ptr->pcal_params[i]);
[ ]   543  
[B]   544              png_free(png_ptr, info_ptr->pcal_params);
[B]   545              info_ptr->pcal_params = NULL;
[B]   546           }
[B]   547        info_ptr->valid &= ~PNG_INFO_pCAL;
[B]   548     }
[B]   549  #endif
[ ]   550  
[B]   551  #ifdef PNG_iCCP_SUPPORTED
[ ]   552     /* Free any profile entry */
[B]   553     if (((mask & PNG_FREE_ICCP) & info_ptr->free_me) != 0)
[ ]   554     {
[ ]   555        png_free(png_ptr, info_ptr->iccp_name);
[ ]   556        png_free(png_ptr, info_ptr->iccp_profile);
[ ]   557        info_ptr->iccp_name = NULL;
[ ]   558        info_ptr->iccp_profile = NULL;
[ ]   559        info_ptr->valid &= ~PNG_INFO_iCCP;
[ ]   560     }
[B]   561  #endif
[ ]   562  
[B]   563  #ifdef PNG_sPLT_SUPPORTED
[ ]   564     /* Free a given sPLT entry, or (if num == -1) all sPLT entries */
[B]   565     if (info_ptr->splt_palettes != NULL &&
[B]   566         ((mask & PNG_FREE_SPLT) & info_ptr->free_me) != 0)
[ ]   567     {
[ ]   568        if (num != -1)
[ ]   569        {
[ ]   570           png_free(png_ptr, info_ptr->splt_palettes[num].name);
[ ]   571           png_free(png_ptr, info_ptr->splt_palettes[num].entries);
[ ]   572           info_ptr->splt_palettes[num].name = NULL;
[ ]   573           info_ptr->splt_palettes[num].entries = NULL;
[ ]   574        }
[ ]   575  
[ ]   576        else
[ ]   577        {
[ ]   578           int i;
[ ]   579  
[ ]   580           for (i = 0; i < info_ptr->splt_palettes_num; i++)
[ ]   581           {
[ ]   582              png_free(png_ptr, info_ptr->splt_palettes[i].name);
[ ]   583              png_free(png_ptr, info_ptr->splt_palettes[i].entries);
[ ]   584           }
[ ]   585  
[ ]   586           png_free(png_ptr, info_ptr->splt_palettes);
[ ]   587           info_ptr->splt_palettes = NULL;
[ ]   588           info_ptr->splt_palettes_num = 0;
[ ]   589           info_ptr->valid &= ~PNG_INFO_sPLT;
[ ]   590        }
[ ]   591     }
[B]   592  #endif
[ ]   593  
[B]   594  #ifdef PNG_STORE_UNKNOWN_CHUNKS_SUPPORTED
[B]   595     if (info_ptr->unknown_chunks != NULL &&
[B]   596         ((mask & PNG_FREE_UNKN) & info_ptr->free_me) != 0)
[ ]   597     {
[ ]   598        if (num != -1)
[ ]   599        {
[ ]   600            png_free(png_ptr, info_ptr->unknown_chunks[num].data);
[ ]   601            info_ptr->unknown_chunks[num].data = NULL;
[ ]   602        }
[ ]   603  
[ ]   604        else
[ ]   605        {
[ ]   606           int i;
[ ]   607  
[ ]   608           for (i = 0; i < info_ptr->unknown_chunks_num; i++)
[ ]   609              png_free(png_ptr, info_ptr->unknown_chunks[i].data);
[ ]   610  
[ ]   611           png_free(png_ptr, info_ptr->unknown_chunks);
[ ]   612           info_ptr->unknown_chunks = NULL;
[ ]   613           info_ptr->unknown_chunks_num = 0;
[ ]   614        }
[ ]   615     }
[B]   616  #endif
[ ]   617  
[B]   618  #ifdef PNG_eXIf_SUPPORTED
[ ]   619     /* Free any eXIf entry */
[B]   620     if (((mask & PNG_FREE_EXIF) & info_ptr->free_me) != 0)
[W]   621     {
[W]   622  # ifdef PNG_READ_eXIf_SUPPORTED
[W]   623        if (info_ptr->eXIf_buf)
[ ]   624        {
[ ]   625           png_free(png_ptr, info_ptr->eXIf_buf);
[ ]   626           info_ptr->eXIf_buf = NULL;
[ ]   627        }
[W]   628  # endif
[W]   629        if (info_ptr->exif)
[ ]   630        {
[ ]   631           png_free(png_ptr, info_ptr->exif);
[ ]   632           info_ptr->exif = NULL;
[ ]   633        }
[W]   634        info_ptr->valid &= ~PNG_INFO_eXIf;
[W]   635     }
[B]   636  #endif
[ ]   637  
[B]   638  #ifdef PNG_hIST_SUPPORTED
[ ]   639     /* Free any hIST entry */
[B]   640     if (((mask & PNG_FREE_HIST) & info_ptr->free_me) != 0)
[W]   641     {
[W]   642        png_free(png_ptr, info_ptr->hist);
[W]   643        info_ptr->hist = NULL;
[W]   644        info_ptr->valid &= ~PNG_INFO_hIST;
[W]   645     }
[B]   646  #endif
[ ]   647  
[ ]   648     /* Free any PLTE entry that was internally allocated */
[B]   649     if (((mask & PNG_FREE_PLTE) & info_ptr->free_me) != 0)
[W]   650     {
[W]   651        png_free(png_ptr, info_ptr->palette);
[W]   652        info_ptr->palette = NULL;
[W]   653        info_ptr->valid &= ~PNG_INFO_PLTE;
[W]   654        info_ptr->num_palette = 0;
[W]   655     }
[ ]   656  
[B]   657  #ifdef PNG_INFO_IMAGE_SUPPORTED
[ ]   658     /* Free any image bits attached to the info structure */
[B]   659     if (((mask & PNG_FREE_ROWS) & info_ptr->free_me) != 0)
[ ]   660     {
[ ]   661        if (info_ptr->row_pointers != NULL)
[ ]   662        {
[ ]   663           png_uint_32 row;
[ ]   664           for (row = 0; row < info_ptr->height; row++)
[ ]   665              png_free(png_ptr, info_ptr->row_pointers[row]);
[ ]   666  
[ ]   667           png_free(png_ptr, info_ptr->row_pointers);
[ ]   668           info_ptr->row_pointers = NULL;
[ ]   669        }
[ ]   670        info_ptr->valid &= ~PNG_INFO_IDAT;
[ ]   671     }
[B]   672  #endif
[ ]   673  
[B]   674     if (num != -1) <-- BLOCKER
[W]   675        mask &= ~PNG_FREE_MUL;
[ ]   676  
[B]   677     info_ptr->free_me &= ~mask;
[B]   678  }

--- No 1-hop callers of OSS_FUZZ_png_free_data fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     128        33  OSS_FUZZ_png_muldiv  (/src/libpng/png.c:3351-3461)
      10         3  png.c:png_colorspace_endpoints_match  (/src/libpng/png.c:1593-1605)
       8         2  png.c:png_XYZ_from_xy  (/src/libpng/png.c:1277-1539)
       8         2  png.c:png_colorspace_check_xy  (/src/libpng/png.c:1619-1638)
       8         2  OSS_FUZZ_png_colorspace_set_chromaticities  (/src/libpng/png.c:1722-1754)
       4         1  png.c:png_xy_from_XYZ  (/src/libpng/png.c:1234-1273)
       4         1  png.c:png_colorspace_set_xy_and_XYZ  (/src/libpng/png.c:1675-1717)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_free_data  (/src/libpng/png.c:473-678) ---
  d=1   L 476  T=0 F=67  T=0 F=23  if (png_ptr == NULL || info_ptr == NULL)
  d=1   L 476  T=0 F=67  T=0 F=23  if (png_ptr == NULL || info_ptr == NULL)
  d=1   L 481  T=25 F=42  T=8 F=15  if (info_ptr->text != NULL &&
  d=1   L 482  T=17 F=8  T=8 F=0  ((mask & PNG_FREE_TEXT) & info_ptr->free_me) != 0)
  d=1   L 484  T=0 F=17  T=0 F=8  if (num != -1)
  d=1   L 494  T=17 F=17  T=9 F=8  for (i = 0; i < info_ptr->num_text; i++)
  d=1   L 507  T=1 F=66  T=0 F=23  if (((mask & PNG_FREE_TRNS) & info_ptr->free_me) != 0)
  d=1   L 518  T=8 F=59  T=6 F=17  if (((mask & PNG_FREE_SCAL) & info_ptr->free_me) != 0)
  d=1   L 530  T=1 F=66  T=5 F=18  if (((mask & PNG_FREE_PCAL) & info_ptr->free_me) != 0)
  d=1   L 537  T=1 F=0  T=5 F=0  if (info_ptr->pcal_params != NULL)
  d=1   L 541  T=2 F=1  T=10 F=5  for (i = 0; i < info_ptr->pcal_nparams; i++)
  d=1   L 553  T=0 F=67  T=0 F=23  if (((mask & PNG_FREE_ICCP) & info_ptr->free_me) != 0)
  d=1   L 565  T=0 F=67  T=0 F=23  if (info_ptr->splt_palettes != NULL &&
  d=1   L 595  T=0 F=67  T=0 F=23  if (info_ptr->unknown_chunks != NULL &&
  d=1   L 620  T=1 F=66  T=0 F=23  if (((mask & PNG_FREE_EXIF) & info_ptr->free_me) != 0)
  d=1   L 623  T=0 F=1  T=0 F=0  if (info_ptr->eXIf_buf)
  d=1   L 629  T=0 F=1  T=0 F=0  if (info_ptr->exif)
  d=1   L 640  T=1 F=66  T=0 F=23  if (((mask & PNG_FREE_HIST) & info_ptr->free_me) != 0)
  d=1   L 649  T=19 F=48  T=0 F=23  if (((mask & PNG_FREE_PLTE) & info_ptr->free_me) != 0)
  d=1   L 659  T=0 F=67  T=0 F=23  if (((mask & PNG_FREE_ROWS) & info_ptr->free_me) != 0)
  d=1   L 674  T=21 F=46  T=0 F=23  if (num != -1)  <-- BLOCKER

[off-chain: 116 additional divergent branches across 21 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=013b9f2a08a04135, size=738 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=DwordInterestingMutator,BytesDeleteMutator,QwordAddMutator,ByteInterestingMutator,ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 82 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=04c4679d03b2cfec, size=995 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=BitFlipMutator,ByteInterestingMutator,TokenReplace,BytesRandSetMutator,ByteInterestingMutator,BytesSwapMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=074cbf90cbbef94f, size=710 bytes, fuzzer=cmplog, trial=1, discovered_at=744s, mutation_op=WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=01ecb96189493aa8, size=613 bytes, fuzzer=cmplog, trial=1, discovered_at=6338s, mutation_op=CrossoverReplaceMutator,BitFlipMutator,BytesCopyMutator,TokenReplace,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 00   .....gAMA.......
  0030: 05 00 00 00 01 74 45 58 74 01 d9 c9 2c 7f 00 00   .....tEXt...,...
Seed 5 (id=06e954d9dfde0384, size=764 bytes, fuzzer=cmplog, trial=1, discovered_at=11068s, mutation_op=WordAddMutator,ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 00   .....gAMA.......
  0030: 05 00 00 00 01 74 45 58 74 01 d9 c9 2c 7f 00 00   .....tEXt...,...

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
   0x0012  00(.)x20                            00(.)x9 05(.)x1                     PARTIAL
   0x0015  00(.)x19 0f(.)x1                    00(.)x10                            PARTIAL
   0x0016  00(.)x16 0a(.)x1 42(B)x1 ff(.)x1 +1u  a0(.)x4 00(.)x3 80(.)x2 02(.)x1     PARTIAL
   0x0018  08(.)x10 01(.)x4 02(.)x3 04(.)x3    10(.)x4 08(.)x2 04(.)x2 02(.)x1 +1u  PARTIAL
   0x0019  03(.)x11 06(.)x8 02(.)x1            00(.)x7 04(.)x2 06(.)x1             PARTIAL
   0x001d  52(R)x20                            7f(.)x4 00(.)x3 52(R)x2 ff(.)x1     PARTIAL
   0x001e  ed(.)x20                            ed(.)x7 ff(.)x2 00(.)x1             PARTIAL
   0x0027  4d(M)x10 6d(m)x10                   4d(M)x10                            PARTIAL
   0x0029  00(.)x20                            00(.)x9 80(.)x1                     PARTIAL
   0x002b  b1(.)x10 00(.)x10                   b1(.)x10                            PARTIAL
   0x002c  00(.)x10 8f(.)x9 82(.)x1            8f(.)x10                            PARTIAL
   0x002d  0b(.)x10 00(.)x10                   0b(.)x9 aa(.)x1                     PARTIAL
   0x002e  fc(.)x10 00(.)x10                   fc(.)x6 04(.)x3 56(V)x1             PARTIAL
   0x002f  00(.)x15 61(a)x5                    61(a)x9 aa(.)x1                     PARTIAL
   0x0030  05(.)x10 00(.)x10                   05(.)x9 aa(.)x1                     PARTIAL
   0x0034  01(.)x10 ff(.)x10                   01(.)x9 09(.)x1                     PARTIAL
   0x0035  50(P)x10 73(s)x5 74(t)x5            73(s)x9 74(t)x1                     PARTIAL
   0x0036  4c(L)x10 52(R)x5 45(E)x5            52(R)x9 45(E)x1                     PARTIAL
   0x0037  54(T)x10 47(G)x5 58(X)x5            47(G)x9 58(X)x1                     PARTIAL
   0x0038  45(E)x10 42(B)x5 74(t)x5            42(B)x9 74(t)x1                     PARTIAL
   0x0039  01(.)x10 52(R)x10                   01(.)x9 54(T)x1                     PARTIAL
   0x003a  d9(.)x10 01(.)x10                   d9(.)x9 69(i)x1                     PARTIAL
   0x003b  c9(.)x10 76(v)x10                   c9(.)x9 74(t)x1                     PARTIAL
   0x003c  2c(,)x10 76(v)x10                   2c(,)x9 6c(l)x1                     PARTIAL
   0x003d  7f(.)x10 18(.)x10                   7f(.)x9 65(e)x1                     PARTIAL
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libpng_3818.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3818,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3818 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3818 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3818 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).