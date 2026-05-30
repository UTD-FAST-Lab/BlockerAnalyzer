==== BLOCKER ====
Target: libpng
Branch ID: 3883
Location: /src/libpng/pngread.c:119:19
Enclosing function: OSS_FUZZ_png_read_info
Source line:          else if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.90h  loser=24.00h
  avg hitcount on branch: winner=59  loser=0
  prob_div=1.00  dur_div=23.10h  hit_div=59
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3883/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_read_info (/src/libpng/pngread.c:93-262) ---
[ ]    91  void PNGAPI
[ ]    92  png_read_info(png_structrp png_ptr, png_inforp info_ptr)
[B]    93  {
[B]    94  #ifdef PNG_HANDLE_AS_UNKNOWN_SUPPORTED
[B]    95     int keep;
[B]    96  #endif
[ ]    97  
[B]    98     png_debug(1, "in png_read_info");
[ ]    99  
[B]   100     if (png_ptr == NULL || info_ptr == NULL)
[ ]   101        return;
[ ]   102  
[ ]   103     /* Read and check the PNG file signature. */
[B]   104     png_read_sig(png_ptr, info_ptr);
[ ]   105  
[B]   106     for (;;)
[B]   107     {
[B]   108        png_uint_32 length = png_read_chunk_header(png_ptr);
[B]   109        png_uint_32 chunk_name = png_ptr->chunk_name;
[ ]   110  
[ ]   111        /* IDAT logic needs to happen here to simplify getting the two flags
[ ]   112         * right.
[ ]   113         */
[B]   114        if (chunk_name == png_IDAT)
[B]   115        {
[B]   116           if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]   117              png_chunk_error(png_ptr, "Missing IHDR before IDAT");
[ ]   118  
[B]   119           else if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE && <-- BLOCKER
[B]   120               (png_ptr->mode & PNG_HAVE_PLTE) == 0)
[W]   121              png_chunk_error(png_ptr, "Missing PLTE before IDAT");
[ ]   122  
[B]   123           else if ((png_ptr->mode & PNG_AFTER_IDAT) != 0)
[ ]   124              png_chunk_benign_error(png_ptr, "Too many IDATs found");
[ ]   125  
[B]   126           png_ptr->mode |= PNG_HAVE_IDAT;
[B]   127        }
[ ]   128  
[B]   129        else if ((png_ptr->mode & PNG_HAVE_IDAT) != 0)
[ ]   130        {
[ ]   131           png_ptr->mode |= PNG_HAVE_CHUNK_AFTER_IDAT;
[ ]   132           png_ptr->mode |= PNG_AFTER_IDAT;
[ ]   133        }
[ ]   134  
[ ]   135        /* This should be a binary subdivision search or a hash for
[ ]   136         * matching the chunk name rather than a linear search.
[ ]   137         */
[B]   138        if (chunk_name == png_IHDR)
[B]   139           png_handle_IHDR(png_ptr, info_ptr, length);
[ ]   140  
[B]   141        else if (chunk_name == png_IEND)
[ ]   142           png_handle_IEND(png_ptr, info_ptr, length);
[ ]   143  
[B]   144  #ifdef PNG_HANDLE_AS_UNKNOWN_SUPPORTED
[B]   145        else if ((keep = png_chunk_unknown_handling(png_ptr, chunk_name)) != 0)
[ ]   146        {
[ ]   147           png_handle_unknown(png_ptr, info_ptr, length, keep);
[ ]   148  
[ ]   149           if (chunk_name == png_PLTE)
[ ]   150              png_ptr->mode |= PNG_HAVE_PLTE;
[ ]   151  
[ ]   152           else if (chunk_name == png_IDAT)
[ ]   153           {
[ ]   154              png_ptr->idat_size = 0; /* It has been consumed */
[ ]   155              break;
[ ]   156           }
[ ]   157        }
[B]   158  #endif
[B]   159        else if (chunk_name == png_PLTE)
[W]   160           png_handle_PLTE(png_ptr, info_ptr, length);
[ ]   161  
[B]   162        else if (chunk_name == png_IDAT)
[B]   163        {
[B]   164           png_ptr->idat_size = length;
[B]   165           break;
[B]   166        }
[ ]   167  
[B]   168  #ifdef PNG_READ_bKGD_SUPPORTED
[B]   169        else if (chunk_name == png_bKGD)
[B]   170           png_handle_bKGD(png_ptr, info_ptr, length);
[B]   171  #endif
[ ]   172  
[B]   173  #ifdef PNG_READ_cHRM_SUPPORTED
[B]   174        else if (chunk_name == png_cHRM)
[B]   175           png_handle_cHRM(png_ptr, info_ptr, length);
[B]   176  #endif
[ ]   177  
[B]   178  #ifdef PNG_READ_eXIf_SUPPORTED
[B]   179        else if (chunk_name == png_eXIf)
[W]   180           png_handle_eXIf(png_ptr, info_ptr, length);
[B]   181  #endif
[ ]   182  
[B]   183  #ifdef PNG_READ_gAMA_SUPPORTED
[B]   184        else if (chunk_name == png_gAMA)
[B]   185           png_handle_gAMA(png_ptr, info_ptr, length);
[B]   186  #endif
[ ]   187  
[B]   188  #ifdef PNG_READ_hIST_SUPPORTED
[B]   189        else if (chunk_name == png_hIST)
[ ]   190           png_handle_hIST(png_ptr, info_ptr, length);
[B]   191  #endif
[ ]   192  
[B]   193  #ifdef PNG_READ_oFFs_SUPPORTED
[B]   194        else if (chunk_name == png_oFFs)
[B]   195           png_handle_oFFs(png_ptr, info_ptr, length);
[B]   196  #endif
[ ]   197  
[B]   198  #ifdef PNG_READ_pCAL_SUPPORTED
[B]   199        else if (chunk_name == png_pCAL)
[B]   200           png_handle_pCAL(png_ptr, info_ptr, length);
[B]   201  #endif
[ ]   202  
[B]   203  #ifdef PNG_READ_sCAL_SUPPORTED
[B]   204        else if (chunk_name == png_sCAL)
[B]   205           png_handle_sCAL(png_ptr, info_ptr, length);
[B]   206  #endif
[ ]   207  
[B]   208  #ifdef PNG_READ_pHYs_SUPPORTED
[B]   209        else if (chunk_name == png_pHYs)
[B]   210           png_handle_pHYs(png_ptr, info_ptr, length);
[B]   211  #endif
[ ]   212  
[B]   213  #ifdef PNG_READ_sBIT_SUPPORTED
[B]   214        else if (chunk_name == png_sBIT)
[B]   215           png_handle_sBIT(png_ptr, info_ptr, length);
[B]   216  #endif
[ ]   217  
[B]   218  #ifdef PNG_READ_sRGB_SUPPORTED
[B]   219        else if (chunk_name == png_sRGB)
[B]   220           png_handle_sRGB(png_ptr, info_ptr, length);
[B]   221  #endif
[ ]   222  
[B]   223  #ifdef PNG_READ_iCCP_SUPPORTED
[B]   224        else if (chunk_name == png_iCCP)
[ ]   225           png_handle_iCCP(png_ptr, info_ptr, length);
[B]   226  #endif
[ ]   227  
[B]   228  #ifdef PNG_READ_sPLT_SUPPORTED
[B]   229        else if (chunk_name == png_sPLT)
[ ]   230           png_handle_sPLT(png_ptr, info_ptr, length);
[B]   231  #endif
[ ]   232  
[B]   233  #ifdef PNG_READ_tEXt_SUPPORTED
[B]   234        else if (chunk_name == png_tEXt)
[B]   235           png_handle_tEXt(png_ptr, info_ptr, length);
[B]   236  #endif
[ ]   237  
[B]   238  #ifdef PNG_READ_tIME_SUPPORTED
[B]   239        else if (chunk_name == png_tIME)
[B]   240           png_handle_tIME(png_ptr, info_ptr, length);
[B]   241  #endif
[ ]   242  
[B]   243  #ifdef PNG_READ_tRNS_SUPPORTED
[B]   244        else if (chunk_name == png_tRNS)
[W]   245           png_handle_tRNS(png_ptr, info_ptr, length);
[B]   246  #endif
[ ]   247  
[B]   248  #ifdef PNG_READ_zTXt_SUPPORTED
[B]   249        else if (chunk_name == png_zTXt)
[W]   250           png_handle_zTXt(png_ptr, info_ptr, length);
[B]   251  #endif
[ ]   252  
[B]   253  #ifdef PNG_READ_iTXt_SUPPORTED
[B]   254        else if (chunk_name == png_iTXt)
[W]   255           png_handle_iTXt(png_ptr, info_ptr, length);
[B]   256  #endif
[ ]   257  
[B]   258        else
[B]   259           png_handle_unknown(png_ptr, info_ptr, length,
[B]   260               PNG_HANDLE_CHUNK_AS_DEFAULT);
[B]   261     }
[B]   262  }

--- No 1-hop callers of OSS_FUZZ_png_read_info fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     287      6150  OSS_FUZZ_png_read_row  (/src/libpng/pngread.c:384-616)
       0         3  OSS_FUZZ_png_read_end  (/src/libpng/pngread.c:767-935)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_read_info  (/src/libpng/pngread.c:93-262) ---
  d=1   L 119  T=10 F=0  T=0 F=10  else if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE &&  <-- BLOCKER
  d=1   L 120  T=1 F=9  T=0 F=0  (png_ptr->mode & PNG_HAVE_PLTE) == 0)
  d=1   L 159  T=9 F=130  T=0 F=88  else if (chunk_name == png_PLTE)
  d=1   L 179  T=4 F=103  T=0 F=76  else if (chunk_name == png_eXIf)
  d=1   L 239  T=7 F=21  T=8 F=4  else if (chunk_name == png_tIME)
  d=1   L 244  T=6 F=15  T=0 F=4  else if (chunk_name == png_tRNS)
  d=1   L 249  T=6 F=9  T=0 F=4  else if (chunk_name == png_zTXt)
  d=1   L 254  T=2 F=7  T=0 F=4  else if (chunk_name == png_iTXt)

[off-chain: 77 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=14ddd5a497528d88, size=8764 bytes, fuzzer=cmplog, trial=1, discovered_at=2s, mutation_op=WordInterestingMutator,BytesSetMutator,ByteRandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=282c4c4b85d3af6c, size=8764 bytes, fuzzer=cmplog, trial=1, discovered_at=7s, mutation_op=BitFlipMutator,ByteIncMutator,DwordAddMutator,BytesSetMutator,BytesDeleteMutator,WordInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=414b4a1157e93507, size=8568 bytes, fuzzer=cmplog, trial=1, discovered_at=27126s, mutation_op=BytesRandInsertMutator,BytesDeleteMutator,ByteDecMutator,WordInterestingMutator,BytesCopyMutator,ByteIncMutator,BytesRandSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 0f 42 40 08 03 00 00 00 52 ed aa   ......B@.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=04430d1404dcf240, size=8765 bytes, fuzzer=cmplog, trial=1, discovered_at=29940s, mutation_op=ByteInterestingMutator,WordInterestingMutator,ByteFlipMutator,WordInterestingMutator,CrossoverInsertMutator,TokenInsert,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 02 03 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=49a1380366efbf3e, size=8568 bytes, fuzzer=cmplog, trial=1, discovered_at=35373s, mutation_op=WordInterestingMutator,ByteAddMutator,BytesDeleteMutator,BytesSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 08 00 0f 42 40 08 03 00 00 00 52 ed aa   ......B@.....R..
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
   0x0013  5b([)x6 05(.)x3 08(.)x1             05(.)x2 21(!)x1 55(U)x1 0a(.)x1 +5u  PARTIAL
   0x0015  00(.)x6 0f(.)x4                     00(.)x10                            PARTIAL
   0x0016  00(.)x6 42(B)x4                     00(.)x4 a0(.)x3 80(.)x2 02(.)x1     PARTIAL
   0x0017  45(E)x6 40(@)x4                     00(.)x3 86(.)x2 02(.)x1 03(.)x1 +3u  PARTIAL
   0x0018  08(.)x8 02(.)x2                     10(.)x4 04(.)x3 02(.)x1 08(.)x1 +1u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3883.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3883,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3883 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3883 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3883 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).