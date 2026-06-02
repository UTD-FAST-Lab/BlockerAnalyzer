==== BLOCKER ====
Target: libpng
Branch ID: 3909
Location: /src/libpng/pngrtran.c:1227:11
Enclosing function: pngrtran.c:png_init_rgb_transformations
Source line:       if (input_has_transparency == 0)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.20h  loser=24.00h
  avg hitcount on branch: winner=34  loser=0
  prob_div=1.00  dur_div=23.80h  hit_div=34
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3909/{W,L}/branch_coverage_show.txt

--- Enclosing function: pngrtran.c:png_init_rgb_transformations (/src/libpng/pngrtran.c:1207-1288) ---
[ ]  1205  static void /* PRIVATE */
[ ]  1206  png_init_rgb_transformations(png_structrp png_ptr)
[B]  1207  {
[ ]  1208     /* Added to libpng-1.5.4: check the color type to determine whether there
[ ]  1209      * is any alpha or transparency in the image and simply cancel the
[ ]  1210      * background and alpha mode stuff if there isn't.
[ ]  1211      */
[B]  1212     int input_has_alpha = (png_ptr->color_type & PNG_COLOR_MASK_ALPHA) != 0;
[B]  1213     int input_has_transparency = png_ptr->num_trans > 0;
[ ]  1214  
[ ]  1215     /* If no alpha we can optimize. */
[B]  1216     if (input_has_alpha == 0)
[B]  1217     {
[ ]  1218        /* Any alpha means background and associative alpha processing is
[ ]  1219         * required, however if the alpha is 0 or 1 throughout OPTIMIZE_ALPHA
[ ]  1220         * and ENCODE_ALPHA are irrelevant.
[ ]  1221         */
[B]  1222  #     ifdef PNG_READ_ALPHA_MODE_SUPPORTED
[B]  1223           png_ptr->transformations &= ~PNG_ENCODE_ALPHA;
[B]  1224           png_ptr->flags &= ~PNG_FLAG_OPTIMIZE_ALPHA;
[B]  1225  #     endif
[ ]  1226  
[B]  1227        if (input_has_transparency == 0) <-- BLOCKER
[L]  1228           png_ptr->transformations &= ~(PNG_COMPOSE | PNG_BACKGROUND_EXPAND);
[B]  1229     }
[ ]  1230  
[B]  1231  #if defined(PNG_READ_EXPAND_SUPPORTED) && defined(PNG_READ_BACKGROUND_SUPPORTED)
[ ]  1232     /* png_set_background handling - deals with the complexity of whether the
[ ]  1233      * background color is in the file format or the screen format in the case
[ ]  1234      * where an 'expand' will happen.
[ ]  1235      */
[ ]  1236  
[ ]  1237     /* The following code cannot be entered in the alpha pre-multiplication case
[ ]  1238      * because PNG_BACKGROUND_EXPAND is cancelled below.
[ ]  1239      */
[B]  1240     if ((png_ptr->transformations & PNG_BACKGROUND_EXPAND) != 0 &&
[B]  1241         (png_ptr->transformations & PNG_EXPAND) != 0 &&
[B]  1242         (png_ptr->color_type & PNG_COLOR_MASK_COLOR) == 0)
[ ]  1243         /* i.e., GRAY or GRAY_ALPHA */
[ ]  1244     {
[ ]  1245        {
[ ]  1246           /* Expand background and tRNS chunks */
[ ]  1247           int gray = png_ptr->background.gray;
[ ]  1248           int trans_gray = png_ptr->trans_color.gray;
[ ]  1249  
[ ]  1250           switch (png_ptr->bit_depth)
[ ]  1251           {
[ ]  1252              case 1:
[ ]  1253                 gray *= 0xff;
[ ]  1254                 trans_gray *= 0xff;
[ ]  1255                 break;
[ ]  1256  
[ ]  1257              case 2:
[ ]  1258                 gray *= 0x55;
[ ]  1259                 trans_gray *= 0x55;
[ ]  1260                 break;
[ ]  1261  
[ ]  1262              case 4:
[ ]  1263                 gray *= 0x11;
[ ]  1264                 trans_gray *= 0x11;
[ ]  1265                 break;
[ ]  1266  
[ ]  1267              default:
[ ]  1268  
[ ]  1269              case 8:
[ ]  1270                 /* FALLTHROUGH */ /*  (Already 8 bits) */
[ ]  1271  
[ ]  1272              case 16:
[ ]  1273                 /* Already a full 16 bits */
[ ]  1274                 break;
[ ]  1275           }
[ ]  1276  
[ ]  1277           png_ptr->background.red = png_ptr->background.green =
[ ]  1278              png_ptr->background.blue = (png_uint_16)gray;
[ ]  1279  
[ ]  1280           if ((png_ptr->transformations & PNG_EXPAND_tRNS) == 0)
[ ]  1281           {
[ ]  1282              png_ptr->trans_color.red = png_ptr->trans_color.green =
[ ]  1283                 png_ptr->trans_color.blue = (png_uint_16)trans_gray;
[ ]  1284           }
[ ]  1285        }
[ ]  1286     } /* background expand and (therefore) no alpha association. */
[B]  1287  #endif /* READ_EXPAND && READ_BACKGROUND */
[B]  1288  }

--- Caller (1 hop): OSS_FUZZ_png_init_read_transformations (/src/libpng/pngrtran.c:1292-1933, calls pngrtran.c:png_init_rgb_transformations at line 1497) (±10 around call site) ---
[ ]  1487      *
[ ]  1488      * NOTE: this is Not Yet Implemented, the code behaves as in 1.5.1 and
[ ]  1489      * earlier and the palette stuff is actually handled on the first row.  This
[ ]  1490      * leads to the reported bug that the palette returned by png_get_PLTE is not
[ ]  1491      * updated.
[ ]  1492      */
[B]  1493     if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
[ ]  1494        png_init_palette_transformations(png_ptr);
[ ]  1495  
[B]  1496     else
[B]  1497        png_init_rgb_transformations(png_ptr); <-- CALL
[ ]  1498  
[B]  1499  #if defined(PNG_READ_BACKGROUND_SUPPORTED) && \
[B]  1500     defined(PNG_READ_EXPAND_16_SUPPORTED)
[B]  1501     if ((png_ptr->transformations & PNG_EXPAND_16) != 0 &&
[B]  1502         (png_ptr->transformations & PNG_COMPOSE) != 0 &&
[B]  1503         (png_ptr->transformations & PNG_BACKGROUND_EXPAND) == 0 &&
[B]  1504         png_ptr->bit_depth != 16)
[ ]  1505     {
[ ]  1506        /* TODO: fix this.  Because the expand_16 operation is after the compose
[ ]  1507         * handling the background color must be 8, not 16, bits deep, but the

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OSS_FUZZ_png_init_read_transformations  (/src/libpng/pngrtran.c:1292-1933, calls pngrtran.c:png_init_rgb_transformations at line 1497)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     181       858  pngrtran.c:png_do_scale_16_to_8  (/src/libpng/pngrtran.c:2390-2442)
     181       858  pngrtran.c:png_do_gray_to_rgb  (/src/libpng/pngrtran.c:2861-2942)
     181       858  pngrtran.c:png_do_expand  (/src/libpng/pngrtran.c:4385-4605)
     181       858  OSS_FUZZ_png_do_read_transformations  (/src/libpng/pngrtran.c:4741-5041)
       0       278  pngrtran.c:png_do_unpack  (/src/libpng/pngrtran.c:2153-2240)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  pngrtran.c:png_init_rgb_transformations  (/src/libpng/pngrtran.c:1207-1288) ---
  d=1   L1227  T=0 F=10  T=10 F=0  if (input_has_transparency == 0)  <-- BLOCKER

[off-chain: 72 additional divergent branches across 6 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
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

==== Loser-blocking seeds (take true branch) ====
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
Seed 4 (id=0224df9af1e38cc7, size=732 bytes, fuzzer=naive, trial=1, discovered_at=611s, mutation_op=ByteNegMutator,ByteRandMutator,DwordAddMutator,ByteNegMutator,QwordAddMutator,BytesDeleteMutator,BitFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 15 00 00 80 00 04 00 00 00 01 00 ff aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=0266c1b60d998fe1, size=732 bytes, fuzzer=naive, trial=1, discovered_at=906s, mutation_op=DwordAddMutator,QwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 0a 00 00 80 00 04 00 00 00 01 00 ff aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x10                            00(.)x9 05(.)x1                     PARTIAL
   0x0015  00(.)x9 0f(.)x1                     00(.)x10                            PARTIAL
   0x0016  00(.)x8 85(.)x1 42(B)x1             80(.)x4 00(.)x3 a0(.)x2 02(.)x1     PARTIAL
   0x0017  45(E)x4 01(.)x4 85(.)x1 40(@)x1     00(.)x5 02(.)x1 86(.)x1 03(.)x1 +2u  PARTIAL
   0x0018  08(.)x10                            04(.)x5 10(.)x3 02(.)x1 01(.)x1     DIFFER
   0x0019  02(.)x10                            00(.)x10                            DIFFER
   0x001c  01(.)x8 00(.)x2                     01(.)x10                            PARTIAL
   0x001d  52(R)x10                            00(.)x6 7f(.)x4                     DIFFER
   0x001e  ed(.)x10                            ff(.)x4 ed(.)x4 00(.)x2             PARTIAL
   0x002d  0b(.)x10                            0b(.)x9 1b(.)x1                     PARTIAL
   0x002e  fc(.)x10                            04(.)x6 fc(.)x4                     PARTIAL
   0x0030  05(.)x9 00(.)x1                     05(.)x10                            PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3909.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3909,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3909 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3909 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3909 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).