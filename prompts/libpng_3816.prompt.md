==== BLOCKER ====
Target: libpng
Branch ID: 3816
Location: /src/libpng/png.c:640:8
Enclosing function: OSS_FUZZ_png_free_data
Source line:    if (((mask & PNG_FREE_HIST) & info_ptr->free_me) != 0)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           6        4          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 24  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.10h  loser=24.00h
  avg hitcount on branch: winner=3  loser=0
  prob_div=0.90  dur_div=20.90h  hit_div=3
  subject-level: delta_AUC=13087800.0  p_AUC=0.0002  delta_Final=135.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3816/{W,L}/branch_coverage_show.txt

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
[ ]   508     {
[ ]   509        info_ptr->valid &= ~PNG_INFO_tRNS;
[ ]   510        png_free(png_ptr, info_ptr->trans_alpha);
[ ]   511        info_ptr->trans_alpha = NULL;
[ ]   512        info_ptr->num_trans = 0;
[ ]   513     }
[B]   514  #endif
[ ]   515  
[B]   516  #ifdef PNG_sCAL_SUPPORTED
[ ]   517     /* Free any sCAL entry */
[B]   518     if (((mask & PNG_FREE_SCAL) & info_ptr->free_me) != 0)
[L]   519     {
[L]   520        png_free(png_ptr, info_ptr->scal_s_width);
[L]   521        png_free(png_ptr, info_ptr->scal_s_height);
[L]   522        info_ptr->scal_s_width = NULL;
[L]   523        info_ptr->scal_s_height = NULL;
[L]   524        info_ptr->valid &= ~PNG_INFO_sCAL;
[L]   525     }
[B]   526  #endif
[ ]   527  
[B]   528  #ifdef PNG_pCAL_SUPPORTED
[ ]   529     /* Free any pCAL entry */
[B]   530     if (((mask & PNG_FREE_PCAL) & info_ptr->free_me) != 0)
[L]   531     {
[L]   532        png_free(png_ptr, info_ptr->pcal_purpose);
[L]   533        png_free(png_ptr, info_ptr->pcal_units);
[L]   534        info_ptr->pcal_purpose = NULL;
[L]   535        info_ptr->pcal_units = NULL;
[ ]   536  
[L]   537        if (info_ptr->pcal_params != NULL)
[L]   538           {
[L]   539              int i;
[ ]   540  
[L]   541              for (i = 0; i < info_ptr->pcal_nparams; i++)
[L]   542                 png_free(png_ptr, info_ptr->pcal_params[i]);
[ ]   543  
[L]   544              png_free(png_ptr, info_ptr->pcal_params);
[L]   545              info_ptr->pcal_params = NULL;
[L]   546           }
[L]   547        info_ptr->valid &= ~PNG_INFO_pCAL;
[L]   548     }
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
[W]   567     {
[W]   568        if (num != -1)
[ ]   569        {
[ ]   570           png_free(png_ptr, info_ptr->splt_palettes[num].name);
[ ]   571           png_free(png_ptr, info_ptr->splt_palettes[num].entries);
[ ]   572           info_ptr->splt_palettes[num].name = NULL;
[ ]   573           info_ptr->splt_palettes[num].entries = NULL;
[ ]   574        }
[ ]   575  
[W]   576        else
[W]   577        {
[W]   578           int i;
[ ]   579  
[W]   580           for (i = 0; i < info_ptr->splt_palettes_num; i++)
[W]   581           {
[W]   582              png_free(png_ptr, info_ptr->splt_palettes[i].name);
[W]   583              png_free(png_ptr, info_ptr->splt_palettes[i].entries);
[W]   584           }
[ ]   585  
[W]   586           png_free(png_ptr, info_ptr->splt_palettes);
[W]   587           info_ptr->splt_palettes = NULL;
[W]   588           info_ptr->splt_palettes_num = 0;
[W]   589           info_ptr->valid &= ~PNG_INFO_sPLT;
[W]   590        }
[W]   591     }
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
[W]   630        {
[W]   631           png_free(png_ptr, info_ptr->exif);
[W]   632           info_ptr->exif = NULL;
[W]   633        }
[W]   634        info_ptr->valid &= ~PNG_INFO_eXIf;
[W]   635     }
[B]   636  #endif
[ ]   637  
[B]   638  #ifdef PNG_hIST_SUPPORTED
[ ]   639     /* Free any hIST entry */
[B]   640     if (((mask & PNG_FREE_HIST) & info_ptr->free_me) != 0) <-- BLOCKER
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
[B]   674     if (num != -1)
[W]   675        mask &= ~PNG_FREE_MUL;
[ ]   676  
[B]   677     info_ptr->free_me &= ~mask;
[B]   678  }

--- No 1-hop callers of OSS_FUZZ_png_free_data fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       1        28  OSS_FUZZ_png_check_fp_number  (/src/libpng/png.c:2714-2834)
       9        28  OSS_FUZZ_png_reciprocal  (/src/libpng/png.c:3489-3503)
       0        17  OSS_FUZZ_png_check_fp_string  (/src/libpng/png.c:2840-2849)
       7        23  png.c:png_colorspace_endpoints_match  (/src/libpng/png.c:1593-1605)
       0         8  OSS_FUZZ_png_zalloc  (/src/libpng/png.c:99-114)
       0         8  OSS_FUZZ_png_zfree  (/src/libpng/png.c:119-121)
       0         1  OSS_FUZZ_png_zstream_error  (/src/libpng/png.c:999-1061)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_free_data  (/src/libpng/png.c:473-678) ---
  d=1   L 482  T=3 F=0  T=5 F=1  ((mask & PNG_FREE_TEXT) & info_ptr->free_me) != 0)
  d=1   L 494  T=3 F=3  T=7 F=5  for (i = 0; i < info_ptr->num_text; i++)
  d=1   L 518  T=0 F=29  T=2 F=21  if (((mask & PNG_FREE_SCAL) & info_ptr->free_me) != 0)
  d=1   L 530  T=0 F=29  T=4 F=19  if (((mask & PNG_FREE_PCAL) & info_ptr->free_me) != 0)
  d=1   L 537  T=0 F=0  T=4 F=0  if (info_ptr->pcal_params != NULL)
  d=1   L 541  T=0 F=0  T=8 F=4  for (i = 0; i < info_ptr->pcal_nparams; i++)
  d=1   L 565  T=2 F=27  T=0 F=23  if (info_ptr->splt_palettes != NULL &&
  d=1   L 566  T=2 F=0  T=0 F=0  ((mask & PNG_FREE_SPLT) & info_ptr->free_me) != 0)
  d=1   L 568  T=0 F=2  T=0 F=0  if (num != -1)
  d=1   L 580  T=2 F=2  T=0 F=0  for (i = 0; i < info_ptr->splt_palettes_num; i++)
  d=1   L 620  T=3 F=26  T=0 F=23  if (((mask & PNG_FREE_EXIF) & info_ptr->free_me) != 0)
  d=1   L 623  T=0 F=3  T=0 F=0  if (info_ptr->eXIf_buf)
  d=1   L 629  T=3 F=0  T=0 F=0  if (info_ptr->exif)
  d=1   L 640  T=6 F=23  T=0 F=23  if (((mask & PNG_FREE_HIST) & info_ptr->free_me) != 0)  <-- BLOCKER
  d=1   L 649  T=6 F=23  T=0 F=23  if (((mask & PNG_FREE_PLTE) & info_ptr->free_me) != 0)
  d=1   L 674  T=12 F=17  T=0 F=23  if (num != -1)

[off-chain: 111 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=f5d9e6546b2de5f3, size=1111 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=49s, mutation_op=BytesInsertMutator,WordInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 00   .....gAMA.......
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=89471139d19201f2, size=1111 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=82s, mutation_op=BytesInsertCopyMutator,ByteRandMutator,TokenReplace,ByteNegMutator,CrossoverReplaceMutator,ByteAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=f44d0a9c8720b7ed, size=1013 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=12944s, mutation_op=WordAddMutator,DwordInterestingMutator,BytesDeleteMutator,ByteAddMutator,BytesRandSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 00   .....gAMA.......
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=2238994922e97474, size=1133 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=19199s, mutation_op=WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 00   .....gAMA.......
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=9d1967cef8f40482, size=1133 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=19830s, mutation_op=BytesDeleteMutator,ByteDecMutator,QwordAddMutator,TokenInsert,BytesInsertMutator,BytesDeleteMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 00   .....gAMA.......
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00c64a8985930929, size=433 bytes, fuzzer=value_profile, trial=1, discovered_at=0s, mutation_op=BytesSetMutator,QwordAddMutator,BytesCopyMutator,ByteFlipMutator,TokenReplace):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 74 52 47 42 01 d9 c9 2c 7f 00 00   .....tRGB...,...
Seed 2 (id=00793532ef09f446, size=269 bytes, fuzzer=value_profile, trial=1, discovered_at=14s, mutation_op=CrossoverReplaceMutator,ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 0f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 41 01 f5 c9 2c 7f 00 00   .....sRGA...,...
Seed 3 (id=009a34a8f7375590, size=2610 bytes, fuzzer=value_profile, trial=1, discovered_at=15s, mutation_op=DwordAddMutator,QwordAddMutator,CrossoverInsertMutator,BytesDeleteMutator,ByteInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=00240036e293ba45, size=8818 bytes, fuzzer=value_profile, trial=1, discovered_at=562s, mutation_op=DwordInterestingMutator,BytesInsertMutator,ByteIncMutator,TokenInsert,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 20 00 00 00 01 08 06 00 00 01 52 ed aa   ... .........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=005d3e4b5b80440b, size=9099 bytes, fuzzer=value_profile, trial=1, discovered_at=4461s, mutation_op=BytesSetMutator,QwordAddMutator,BytesCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 22 00 00 a1 86 02 00 00 00 01 52 ed aa   ...".........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0013  5b([)x6                             5b([)x6 51(Q)x2 20( )x1 22(")x1     PARTIAL
   0x0016  00(.)x6                             00(.)x7 a1(.)x2 80(.)x1             PARTIAL
   0x0017  45(E)x6                             45(E)x6 86(.)x2 01(.)x1 00(.)x1     PARTIAL
   0x0018  08(.)x6                             08(.)x7 02(.)x2 04(.)x1             PARTIAL
   0x0019  06(.)x6                             06(.)x7 00(.)x3                     PARTIAL
   0x002b  b1(.)x6                             b1(.)x9 b2(.)x1                     PARTIAL
   0x002c  8f(.)x6                             8f(.)x9 0f(.)x1                     PARTIAL
   0x002f  00(.)x5 61(a)x1                     61(a)x10                            PARTIAL
   0x0035  73(s)x6                             73(s)x9 74(t)x1                     PARTIAL
   0x0037  47(G)x6                             47(G)x9 64(d)x1                     PARTIAL
   0x0038  42(B)x6                             42(B)x9 41(A)x1                     PARTIAL
   0x003a  d9(.)x6                             d9(.)x9 f5(.)x1                     PARTIAL
==== MECHANISM CONTEXT (involved fuzzers only) ====
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3816.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3816,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3816 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3816 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3816 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).