==== BLOCKER ====
Target: libpng
Branch ID: 3966
Location: /src/libpng/pngrutil.c:1182:8
Enclosing function: OSS_FUZZ_png_handle_sBIT
Source line:    if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog); loser (value_profile vs value_profile); loser (ctx_coverage vs naive_ctx)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        9        1          0  winner (ctx_coverage vs naive)
naive_ngram4                     3        7          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'naive_ctx', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (3) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=1.10h  loser=21.60h
  avg hitcount on branch: winner=74  loser=0
  prob_div=0.90  dur_div=20.50h  hit_div=74
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002
--- Pair 2: value_profile > naive  [delta: value_profile] ---
  subject 22  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=6.50h  loser=21.60h
  avg hitcount on branch: winner=37  loser=0
  prob_div=0.80  dur_div=15.10h  hit_div=36
  subject-level: delta_AUC=16855020.0  p_AUC=0.0002  delta_Final=254.7  p_final=0.0002
--- Pair 3: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 25  (naive_ctx vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=3.90h  loser=21.60h
  avg hitcount on branch: winner=39  loser=0
  prob_div=0.80  dur_div=17.70h  hit_div=38
  subject-level: delta_AUC=6413040.0  p_AUC=0.0003  delta_Final=91.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3966/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_handle_sBIT (/src/libpng/pngrutil.c:1158-1234) ---
[ ]  1156  void /* PRIVATE */
[ ]  1157  png_handle_sBIT(png_structrp png_ptr, png_inforp info_ptr, png_uint_32 length)
[B]  1158  {
[B]  1159     unsigned int truelen, i;
[B]  1160     png_byte sample_depth;
[B]  1161     png_byte buf[4];
[ ]  1162  
[B]  1163     png_debug(1, "in png_handle_sBIT");
[ ]  1164  
[B]  1165     if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
[ ]  1166        png_chunk_error(png_ptr, "missing IHDR");
[ ]  1167  
[B]  1168     else if ((png_ptr->mode & (PNG_HAVE_IDAT|PNG_HAVE_PLTE)) != 0)
[B]  1169     {
[B]  1170        png_crc_finish(png_ptr, length);
[B]  1171        png_chunk_benign_error(png_ptr, "out of place");
[B]  1172        return;
[B]  1173     }
[ ]  1174  
[B]  1175     if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_sBIT) != 0)
[ ]  1176     {
[ ]  1177        png_crc_finish(png_ptr, length);
[ ]  1178        png_chunk_benign_error(png_ptr, "duplicate");
[ ]  1179        return;
[ ]  1180     }
[ ]  1181  
[B]  1182     if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE) <-- BLOCKER
[W]  1183     {
[W]  1184        truelen = 3;
[W]  1185        sample_depth = 8;
[W]  1186     }
[ ]  1187  
[L]  1188     else
[L]  1189     {
[L]  1190        truelen = png_ptr->channels;
[L]  1191        sample_depth = png_ptr->bit_depth;
[L]  1192     }
[ ]  1193  
[B]  1194     if (length != truelen || length > 4)
[B]  1195     {
[B]  1196        png_chunk_benign_error(png_ptr, "invalid");
[B]  1197        png_crc_finish(png_ptr, length);
[B]  1198        return;
[B]  1199     }
[ ]  1200  
[L]  1201     buf[0] = buf[1] = buf[2] = buf[3] = sample_depth;
[L]  1202     png_crc_read(png_ptr, buf, truelen);
[ ]  1203  
[L]  1204     if (png_crc_finish(png_ptr, 0) != 0)
[ ]  1205        return;
[ ]  1206  
[L]  1207     for (i=0; i<truelen; ++i)
[L]  1208     {
[L]  1209        if (buf[i] == 0 || buf[i] > sample_depth)
[ ]  1210        {
[ ]  1211           png_chunk_benign_error(png_ptr, "invalid");
[ ]  1212           return;
[ ]  1213        }
[L]  1214     }
[ ]  1215  
[L]  1216     if ((png_ptr->color_type & PNG_COLOR_MASK_COLOR) != 0)
[L]  1217     {
[L]  1218        png_ptr->sig_bit.red = buf[0];
[L]  1219        png_ptr->sig_bit.green = buf[1];
[L]  1220        png_ptr->sig_bit.blue = buf[2];
[L]  1221        png_ptr->sig_bit.alpha = buf[3];
[L]  1222     }
[ ]  1223  
[ ]  1224     else
[ ]  1225     {
[ ]  1226        png_ptr->sig_bit.gray = buf[0];
[ ]  1227        png_ptr->sig_bit.red = buf[0];
[ ]  1228        png_ptr->sig_bit.green = buf[0];
[ ]  1229        png_ptr->sig_bit.blue = buf[0];
[ ]  1230        png_ptr->sig_bit.alpha = buf[1];
[ ]  1231     }
[ ]  1232  
[L]  1233     png_set_sBIT(png_ptr, info_ptr, &(png_ptr->sig_bit));
[L]  1234  }

--- No 1-hop callers of OSS_FUZZ_png_handle_sBIT fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     304      1990  OSS_FUZZ_png_read_finish_row  (/src/libpng/pngrutil.c:4328-4388)
     416       136  OSS_FUZZ_png_crc_read  (/src/libpng/pngrutil.c:197-203)
      11       247  OSS_FUZZ_png_do_read_interlace  (/src/libpng/pngrutil.c:3687-3928)
     209        35  pngrutil.c:png_get_fixed_point  (/src/libpng/pngrutil.c:42-53)
       0       173  pngrutil.c:png_read_filter_row_up  (/src/libpng/pngrutil.c:3952-3963)
      71         0  pngrutil.c:png_read_filter_row_paeth_1byte_pixel  (/src/libpng/pngrutil.c:3995-4041)
      59         0  pngrutil.c:png_read_filter_row_avg  (/src/libpng/pngrutil.c:3968-3990)
      49         9  OSS_FUZZ_png_handle_unknown  (/src/libpng/pngrutil.c:2925-3120)
      37         4  OSS_FUZZ_png_handle_bKGD  (/src/libpng/pngrutil.c:1921-2033)
       0        29  pngrutil.c:png_read_filter_row_sub  (/src/libpng/pngrutil.c:3934-3947)
      31         5  OSS_FUZZ_png_handle_oFFs  (/src/libpng/pngrutil.c:2202-2242)
      23         4  OSS_FUZZ_png_handle_cHRM  (/src/libpng/pngrutil.c:1240-1306)
      11         0  OSS_FUZZ_png_handle_PLTE  (/src/libpng/pngrutil.c:913-1096)
       5         0  OSS_FUZZ_png_handle_tRNS  (/src/libpng/pngrutil.c:1817-1915)
       5         0  OSS_FUZZ_png_handle_eXIf  (/src/libpng/pngrutil.c:2039-2097)
... (2 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_handle_sBIT  (/src/libpng/pngrutil.c:1158-1234) ---
  d=1   L1165  T=0 F=31  T=0 F=13  if ((png_ptr->mode & PNG_HAVE_IHDR) == 0)
  d=1   L1168  T=1 F=30  T=2 F=11  else if ((png_ptr->mode & (PNG_HAVE_IDAT|PNG_HAVE_PLTE)) ...
  d=1   L1175  T=30 F=0  T=11 F=0  if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_sBIT)...
  d=1   L1175  T=0 F=30  T=0 F=11  if (info_ptr != NULL && (info_ptr->valid & PNG_INFO_sBIT)...
  d=1   L1182  T=30 F=0  T=0 F=11  if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)  <-- BLOCKER
  d=1   L1194  T=30 F=0  T=10 F=1  if (length != truelen || length > 4)
  d=1   L1194  T=0 F=0  T=0 F=1  if (length != truelen || length > 4)
  d=1   L1204  T=0 F=0  T=0 F=1  if (png_crc_finish(png_ptr, 0) != 0)
  d=1   L1207  T=0 F=0  T=4 F=1  for (i=0; i<truelen; ++i)
  d=1   L1209  T=0 F=0  T=0 F=4  if (buf[i] == 0 || buf[i] > sample_depth)
  d=1   L1209  T=0 F=0  T=0 F=4  if (buf[i] == 0 || buf[i] > sample_depth)
  d=1   L1216  T=0 F=0  T=1 F=0  if ((png_ptr->color_type & PNG_COLOR_MASK_COLOR) != 0)

[off-chain: 206 additional divergent branches across 35 functions (see HIT-COUNT DIVERGENCE for which functions)]

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
Seed 2 (id=0165867d1e996ed7, size=1672 bytes, fuzzer=naive, trial=1, discovered_at=205s, mutation_op=ByteIncMutator,ByteAddMutator,BitFlipMutator,BytesRandSetMutator,ByteRandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 21 00 00 80 00 04 00 00 00 01 00 ff aa   ...!............
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
   0x0012  00(.)x25                            00(.)x9 05(.)x1                     PARTIAL
   0x0013  5b([)x21 05(.)x3 08(.)x1            5b([)x2 21(!)x1 55(U)x1 0a(.)x1 +5u  PARTIAL
   0x0015  00(.)x20 0f(.)x4 04(.)x1            00(.)x10                            PARTIAL
   0x0016  00(.)x21 42(B)x4                    a0(.)x4 00(.)x3 80(.)x3             PARTIAL
   0x0017  45(E)x20 40(@)x4 01(.)x1            00(.)x4 86(.)x3 45(E)x2 03(.)x1     PARTIAL
   0x0018  08(.)x22 02(.)x3                    04(.)x3 10(.)x3 08(.)x2 02(.)x1 +1u  PARTIAL
   0x0019  03(.)x25                            00(.)x7 04(.)x2 06(.)x1             DIFFER
   0x001d  52(R)x25                            00(.)x4 7f(.)x3 52(R)x2 ff(.)x1     PARTIAL
   0x001e  ed(.)x25                            ed(.)x6 ff(.)x3 00(.)x1             PARTIAL
   0x001f  aa(.)x23 55(U)x2                    aa(.)x10                            PARTIAL
   0x0029  00(.)x25                            00(.)x9 80(.)x1                     PARTIAL
   0x002a  00(.)x24 c2(.)x1                    00(.)x10                            PARTIAL
   0x002c  8f(.)x24 0f(.)x1                    8f(.)x10                            PARTIAL
   0x002d  0b(.)x25                            0b(.)x9 aa(.)x1                     PARTIAL
   0x002e  fc(.)x25                            fc(.)x5 04(.)x4 56(V)x1             PARTIAL
   0x002f  61(a)x25                            61(a)x9 aa(.)x1                     PARTIAL
   0x0030  05(.)x25                            05(.)x9 aa(.)x1                     PARTIAL
   0x003a  d9(.)x24 f5(.)x1                    d9(.)x10                            PARTIAL
   0x003c  2c(,)x19 2f(/)x6                    2c(,)x10                            PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3966.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3966,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3966 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3966 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3966 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).