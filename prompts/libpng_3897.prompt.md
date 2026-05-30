==== BLOCKER ====
Target: libpng
Branch ID: 3897
Location: /src/libpng/pngread.c:838:16
Enclosing function: OSS_FUZZ_png_read_end
Source line:       else if (chunk_name == png_PLTE)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog             9        1          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=5.70h  loser=24.00h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.90  dur_div=18.30h  hit_div=5
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3897/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_read_end (/src/libpng/pngread.c:767-935) ---
[ ]   765  void PNGAPI
[ ]   766  png_read_end(png_structrp png_ptr, png_inforp info_ptr)
[B]   767  {
[B]   768  #ifdef PNG_HANDLE_AS_UNKNOWN_SUPPORTED
[B]   769     int keep;
[B]   770  #endif
[ ]   771  
[B]   772     png_debug(1, "in png_read_end");
[ ]   773  
[B]   774     if (png_ptr == NULL)
[ ]   775        return;
[ ]   776  
[ ]   777     /* If png_read_end is called in the middle of reading the rows there may
[ ]   778      * still be pending IDAT data and an owned zstream.  Deal with this here.
[ ]   779      */
[B]   780  #ifdef PNG_HANDLE_AS_UNKNOWN_SUPPORTED
[B]   781     if (png_chunk_unknown_handling(png_ptr, png_IDAT) == 0)
[B]   782  #endif
[B]   783        png_read_finish_IDAT(png_ptr);
[ ]   784  
[B]   785  #ifdef PNG_READ_CHECK_FOR_INVALID_INDEX_SUPPORTED
[ ]   786     /* Report invalid palette index; added at libng-1.5.10 */
[B]   787     if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE &&
[B]   788         png_ptr->num_palette_max > png_ptr->num_palette)
[ ]   789        png_benign_error(png_ptr, "Read palette index exceeding num_palette");
[B]   790  #endif
[ ]   791  
[B]   792     do
[B]   793     {
[B]   794        png_uint_32 length = png_read_chunk_header(png_ptr);
[B]   795        png_uint_32 chunk_name = png_ptr->chunk_name;
[ ]   796  
[B]   797        if (chunk_name != png_IDAT)
[B]   798           png_ptr->mode |= PNG_HAVE_CHUNK_AFTER_IDAT;
[ ]   799  
[B]   800        if (chunk_name == png_IEND)
[L]   801           png_handle_IEND(png_ptr, info_ptr, length);
[ ]   802  
[B]   803        else if (chunk_name == png_IHDR)
[ ]   804           png_handle_IHDR(png_ptr, info_ptr, length);
[ ]   805  
[B]   806        else if (info_ptr == NULL)
[ ]   807           png_crc_finish(png_ptr, length);
[ ]   808  
[B]   809  #ifdef PNG_HANDLE_AS_UNKNOWN_SUPPORTED
[B]   810        else if ((keep = png_chunk_unknown_handling(png_ptr, chunk_name)) != 0)
[ ]   811        {
[ ]   812           if (chunk_name == png_IDAT)
[ ]   813           {
[ ]   814              if ((length > 0 && !(png_ptr->flags & PNG_FLAG_ZSTREAM_ENDED))
[ ]   815                  || (png_ptr->mode & PNG_HAVE_CHUNK_AFTER_IDAT) != 0)
[ ]   816                 png_benign_error(png_ptr, ".Too many IDATs found");
[ ]   817           }
[ ]   818           png_handle_unknown(png_ptr, info_ptr, length, keep);
[ ]   819           if (chunk_name == png_PLTE)
[ ]   820              png_ptr->mode |= PNG_HAVE_PLTE;
[ ]   821        }
[B]   822  #endif
[ ]   823  
[B]   824        else if (chunk_name == png_IDAT)
[B]   825        {
[ ]   826           /* Zero length IDATs are legal after the last IDAT has been
[ ]   827            * read, but not after other chunks have been read.  1.6 does not
[ ]   828            * always read all the deflate data; specifically it cannot be relied
[ ]   829            * upon to read the Adler32 at the end.  If it doesn't ignore IDAT
[ ]   830            * chunks which are longer than zero as well:
[ ]   831            */
[B]   832           if ((length > 0 && !(png_ptr->flags & PNG_FLAG_ZSTREAM_ENDED))
[B]   833               || (png_ptr->mode & PNG_HAVE_CHUNK_AFTER_IDAT) != 0)
[B]   834              png_benign_error(png_ptr, "..Too many IDATs found");
[ ]   835  
[B]   836           png_crc_finish(png_ptr, length);
[B]   837        }
[B]   838        else if (chunk_name == png_PLTE) <-- BLOCKER
[W]   839           png_handle_PLTE(png_ptr, info_ptr, length);
[ ]   840  
[B]   841  #ifdef PNG_READ_bKGD_SUPPORTED
[B]   842        else if (chunk_name == png_bKGD)
[B]   843           png_handle_bKGD(png_ptr, info_ptr, length);
[B]   844  #endif
[ ]   845  
[B]   846  #ifdef PNG_READ_cHRM_SUPPORTED
[B]   847        else if (chunk_name == png_cHRM)
[B]   848           png_handle_cHRM(png_ptr, info_ptr, length);
[B]   849  #endif
[ ]   850  
[B]   851  #ifdef PNG_READ_eXIf_SUPPORTED
[B]   852        else if (chunk_name == png_eXIf)
[B]   853           png_handle_eXIf(png_ptr, info_ptr, length);
[B]   854  #endif
[ ]   855  
[B]   856  #ifdef PNG_READ_gAMA_SUPPORTED
[B]   857        else if (chunk_name == png_gAMA)
[B]   858           png_handle_gAMA(png_ptr, info_ptr, length);
[B]   859  #endif
[ ]   860  
[B]   861  #ifdef PNG_READ_hIST_SUPPORTED
[B]   862        else if (chunk_name == png_hIST)
[W]   863           png_handle_hIST(png_ptr, info_ptr, length);
[B]   864  #endif
[ ]   865  
[B]   866  #ifdef PNG_READ_oFFs_SUPPORTED
[B]   867        else if (chunk_name == png_oFFs)
[B]   868           png_handle_oFFs(png_ptr, info_ptr, length);
[B]   869  #endif
[ ]   870  
[B]   871  #ifdef PNG_READ_pCAL_SUPPORTED
[B]   872        else if (chunk_name == png_pCAL)
[L]   873           png_handle_pCAL(png_ptr, info_ptr, length);
[B]   874  #endif
[ ]   875  
[B]   876  #ifdef PNG_READ_sCAL_SUPPORTED
[B]   877        else if (chunk_name == png_sCAL)
[B]   878           png_handle_sCAL(png_ptr, info_ptr, length);
[B]   879  #endif
[ ]   880  
[B]   881  #ifdef PNG_READ_pHYs_SUPPORTED
[B]   882        else if (chunk_name == png_pHYs)
[B]   883           png_handle_pHYs(png_ptr, info_ptr, length);
[B]   884  #endif
[ ]   885  
[B]   886  #ifdef PNG_READ_sBIT_SUPPORTED
[B]   887        else if (chunk_name == png_sBIT)
[B]   888           png_handle_sBIT(png_ptr, info_ptr, length);
[B]   889  #endif
[ ]   890  
[B]   891  #ifdef PNG_READ_sRGB_SUPPORTED
[B]   892        else if (chunk_name == png_sRGB)
[B]   893           png_handle_sRGB(png_ptr, info_ptr, length);
[B]   894  #endif
[ ]   895  
[B]   896  #ifdef PNG_READ_iCCP_SUPPORTED
[B]   897        else if (chunk_name == png_iCCP)
[W]   898           png_handle_iCCP(png_ptr, info_ptr, length);
[B]   899  #endif
[ ]   900  
[B]   901  #ifdef PNG_READ_sPLT_SUPPORTED
[B]   902        else if (chunk_name == png_sPLT)
[W]   903           png_handle_sPLT(png_ptr, info_ptr, length);
[B]   904  #endif
[ ]   905  
[B]   906  #ifdef PNG_READ_tEXt_SUPPORTED
[B]   907        else if (chunk_name == png_tEXt)
[B]   908           png_handle_tEXt(png_ptr, info_ptr, length);
[B]   909  #endif
[ ]   910  
[B]   911  #ifdef PNG_READ_tIME_SUPPORTED
[B]   912        else if (chunk_name == png_tIME)
[B]   913           png_handle_tIME(png_ptr, info_ptr, length);
[B]   914  #endif
[ ]   915  
[B]   916  #ifdef PNG_READ_tRNS_SUPPORTED
[B]   917        else if (chunk_name == png_tRNS)
[ ]   918           png_handle_tRNS(png_ptr, info_ptr, length);
[B]   919  #endif
[ ]   920  
[B]   921  #ifdef PNG_READ_zTXt_SUPPORTED
[B]   922        else if (chunk_name == png_zTXt)
[B]   923           png_handle_zTXt(png_ptr, info_ptr, length);
[B]   924  #endif
[ ]   925  
[B]   926  #ifdef PNG_READ_iTXt_SUPPORTED
[B]   927        else if (chunk_name == png_iTXt)
[B]   928           png_handle_iTXt(png_ptr, info_ptr, length);
[B]   929  #endif
[ ]   930  
[B]   931        else
[B]   932           png_handle_unknown(png_ptr, info_ptr, length,
[B]   933               PNG_HANDLE_CHUNK_AS_DEFAULT);
[B]   934     } while ((png_ptr->mode & PNG_HAVE_IEND) == 0);
[B]   935  }

--- No 1-hop callers of OSS_FUZZ_png_read_end fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_read_end  (/src/libpng/pngread.c:767-935) ---
  d=1   L 800  T=0 F=190  T=1 F=200  if (chunk_name == png_IEND)
  d=1   L 832  T=0 F=26  T=0 F=11  if ((length > 0 && !(png_ptr->flags & PNG_FLAG_ZSTREAM_EN...
  d=1   L 832  T=26 F=0  T=11 F=0  if ((length > 0 && !(png_ptr->flags & PNG_FLAG_ZSTREAM_EN...
  d=1   L 833  T=26 F=0  T=11 F=0  || (png_ptr->mode & PNG_HAVE_CHUNK_AFTER_IDAT) != 0)
  d=1   L 838  T=12 F=152  T=0 F=189  else if (chunk_name == png_PLTE)  <-- BLOCKER
  d=1   L 862  T=2 F=123  T=0 F=151  else if (chunk_name == png_hIST)
  d=1   L 872  T=0 F=100  T=12 F=137  else if (chunk_name == png_pCAL)
  d=1   L 897  T=1 F=74  T=0 F=80  else if (chunk_name == png_iCCP)
  d=1   L 902  T=9 F=65  T=0 F=80  else if (chunk_name == png_sPLT)

[off-chain: 10 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=f675a9b2ee4cf006, size=8759 bytes, fuzzer=cmplog, trial=1, discovered_at=166s, mutation_op=TokenInsert,BytesSwapMutator,DwordAddMutator,ByteIncMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=f49b3e384906edb9, size=8759 bytes, fuzzer=cmplog, trial=1, discovered_at=288s, mutation_op=ByteFlipMutator,BytesDeleteMutator,ByteRandMutator,BytesSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=db4e5be1a8536a01, size=9213 bytes, fuzzer=cmplog, trial=1, discovered_at=2546s, mutation_op=BytesInsertMutator,BytesSwapMutator,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 01 08 02 00 00 01 52 ed aa   ...[.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=ba7c8681c09a6693, size=8759 bytes, fuzzer=cmplog, trial=1, discovered_at=12544s, mutation_op=ByteDecMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=d217c2a16d668aa5, size=13363 bytes, fuzzer=cmplog, trial=1, discovered_at=44886s, mutation_op=BytesCopyMutator,BytesDeleteMutator,DwordAddMutator,WordInterestingMutator,BytesDeleteMutator,BytesInsertMutator,BytesRandSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 25 00 00 00 01 08 02 00 00 01 52 ed aa   ...%.........R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=48ef51fe8927b302, size=8763 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=BytesExpandMutator,ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=3258b36fd9493cdb, size=8759 bytes, fuzzer=naive, trial=1, discovered_at=2s, mutation_op=QwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=097b4c3d02b1b413, size=996 bytes, fuzzer=naive, trial=1, discovered_at=240s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteRandMutator,BytesInsertCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 ab 00 00 00 01 01 00 00 00 01 7f ed aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 1b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=021042b836a3f5aa, size=927 bytes, fuzzer=naive, trial=1, discovered_at=257s, mutation_op=ByteDecMutator,BytesSetMutator,ByteNegMutator,ByteFlipMutator,WordInterestingMutator,BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 00 00 02 04 00 00 00 01 00 00 aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=0c520ab1025d7f90, size=4561 bytes, fuzzer=naive, trial=1, discovered_at=342s, mutation_op=BytesRandSetMutator,DwordInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 04 00 00 00 03 04 00 00 00 01 00 00 aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0013  25(%)x6 5b([)x4                     05(.)x5 ab(.)x4 5b([)x2 04(.)x1 +2u  PARTIAL
   0x0017  01(.)x7 45(E)x3                     01(.)x5 03(.)x5 45(E)x3 02(.)x1     PARTIAL
   0x0018  08(.)x10                            04(.)x6 08(.)x4 01(.)x4             PARTIAL
   0x0019  02(.)x7 06(.)x3                     00(.)x10 06(.)x3 04(.)x1            PARTIAL
   0x001c  01(.)x10                            01(.)x13 00(.)x1                    PARTIAL
   0x001d  52(R)x10                            00(.)x6 7f(.)x4 52(R)x3 ff(.)x1     PARTIAL
   0x001e  ed(.)x10                            ed(.)x8 00(.)x6                     PARTIAL
   0x002d  0b(.)x10                            0b(.)x9 1b(.)x4 14(.)x1             PARTIAL
   0x002e  fc(.)x10                            fc(.)x8 04(.)x6                     PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3897.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3897,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3897 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3897 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3897 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).