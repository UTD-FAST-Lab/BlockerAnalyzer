==== BLOCKER ====
Target: harfbuzz
Branch ID: 5991
Location: /src/harfbuzz/src/hb-ot-shaper-use.cc:357:79
Enclosing function: hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&)
Source line:   return (info.use_category() == USE(H) || info.use_category() == USE(HVM) || info.use_category() == USE(IS)) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.90h  loser=23.60h
  avg hitcount on branch: winner=26  loser=0
  prob_div=1.00  dur_div=21.70h  hit_div=26
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5991/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&) (/src/harfbuzz/src/hb-ot-shaper-use.cc:356-359) ---
[ ]   354  static inline bool
[ ]   355  is_halant_use (const hb_glyph_info_t &info)
[B]   356  {
[B]   357    return (info.use_category() == USE(H) || info.use_category() == USE(HVM) || info.use_category() == USE(IS)) && <-- BLOCKER
[B]   358  	 !_hb_glyph_info_ligated (&info);
[B]   359  }

--- Caller (1 hop): hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442, calls hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&) at line 425) (±10 around call site) ---
[ ]   415  	break;
[ ]   416        }
[ ]   417      }
[ ]   418    }
[ ]   419  
[ ]   420    /* Move things back. */
[B]   421    unsigned int j = start;
[B]   422    for (unsigned int i = start; i < end; i++)
[B]   423    {
[B]   424      uint32_t flag = FLAG_UNSAFE (info[i].use_category());
[B]   425      if (is_halant_use (info[i])) <-- CALL
[W]   426      {
[ ]   427        /* If we hit a halant, move after it; otherwise move to the beginning, and
[ ]   428         * shift things in between forward. */
[W]   429        j = i + 1;
[W]   430      }
[B]   431      else if (((flag) & (FLAG (USE(VPre)) | FLAG (USE(VMPre)))) &&
[ ]   432  	     /* Only move the first component of a MultipleSubst. */
[B]   433  	     0 == _hb_glyph_info_get_lig_comp (&info[i]) &&
[B]   434  	     j < i)
[W]   435      {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442, calls hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&) at line 401)
hop 3  hb-ot-shaper-use.cc:reorder_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:448-467, calls hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) at line 459)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442) ---
  d=2   L 425  T=15 F=97  T=0 F=144  if (is_halant_use (info[i]))
  d=2   L 431  T=3 F=94  T=0 F=144  else if (((flag) & (FLAG (USE(VPre)) | FLAG (USE(VMPre)))...
  d=2   L 433  T=3 F=0  T=0 F=0  0 == _hb_glyph_info_get_lig_comp (&info[i]) &&
  d=2   L 434  T=3 F=0  T=0 F=0  j < i)
--- d=1  hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:356-359) ---
  d=1   L 357  T=15 F=97  T=0 F=144  return (info.use_category() == USE(H) || info.use_categor...  <-- BLOCKER
  d=1   L 358  T=15 F=0  T=0 F=0  !_hb_glyph_info_ligated (&info);

[off-chain: 4 additional divergent branches across 4 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=34826c70db3871cf, size=135 bytes, fuzzer=naive, trial=1, discovered_at=2049s, mutation_op=BytesExpandMutator):
  0000: 80 00 2a 2a 6f 2d 62 6f 6b 00 00 20 5f 5f 5f 5f   ..**o-bok.. ____
  0010: 00 00 5f 00 f7 1b 00 00 f7 1c 00 00 00 00 20 00   .._........... .
  0020: 00 e7 19 00 00 e6 e6 e6 00 30 00 00 00 0c 0c 70   .........0.....p
  0030: 78 2d 68 61 6e 74 64 80 00 0c 00 00 00 00 00 e9   x-hantd.........
Seed 2 (id=434dc23098154466, size=41 bytes, fuzzer=naive, trial=1, discovered_at=2691s, mutation_op=BitFlipMutator,ByteRandMutator,ByteNegMutator):
  0000: 00 02 08 00 ac 0f 00 00 00 fe 00 00 b2 05 00 00   ................
  0010: d2 17 00 00 ac 05 00 00 00 fe 00 00 b2 05 00 00   ................
  0020: d2 17 00 00 17 00 00 02 00                        .........
Seed 3 (id=c221404a517802af, size=84 bytes, fuzzer=naive, trial=1, discovered_at=5332s, mutation_op=ByteFlipMutator):
  0000: b4 00 00 ff ff 17 00 64 00 0c 00 00 00 18 18 18   .......d........
  0010: 18 10 00 00 2d 17 00 00 00 10 00 00 d2 17 00 00   ....-...........
  0020: 00 fe 00 00 00 00 00 00 01 fe 00 00 00 00 01 03   ................
  0030: e8 2d 68 00 00 00 00 00 00 00 06 10 00 76 61 73   .-h..........vas
Seed 4 (id=8da5060b4e424547, size=47 bytes, fuzzer=naive, trial=1, discovered_at=10960s, mutation_op=BytesSwapMutator,CrossoverInsertMutator):
  0000: 64 01 0e 00 00 1f 01 00 00 01 03 e2 ff 0a 00 00   d...............
  0010: 00 00 01 03 e8 b9 b9 98 ac 05 00 00 00 fe 00 00   ................
  0020: b7 05 00 00 d2 17 00 00 17 17 17 00 00 fe 00      ...............
Seed 5 (id=e96aafa10b761879, size=107 bytes, fuzzer=naive, trial=1, discovered_at=14429s, mutation_op=BytesRandInsertMutator,WordAddMutator,ByteIncMutator):
  0000: dc dc dc dc dd dc dc dc dc dc dc 0f ff e4 ff ff   ................
  0010: ff b6 b6 00 00 72 a8 00 10 80 00 d2 17 00 00 b6   .....r..........
  0020: 16 e7 00 00 10 00 00 d2 17 00 00 00 0f 00 00 00   ................
  0030: 10 00 00 d2 17 00 00 00 0f 54 f5 f5 f5 f5 f5 f5   .........T......

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0170cbbd7538578d, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=151s, mutation_op=BytesSetMutator,DwordAddMutator,BytesDeleteMutator,BytesDeleteMutator,WordInterestingMutator,TokenInsert):
  0000: 00 20 97 97 00 00 20 20 00 00 00 00 0c 00 00 02   . ....  ........
  0010: 00 0d 01 00 20 97 97 01 00 3b 3b 3b 3b 3b 73 6e   .... ....;;;;;sn
  0020: 2d 00 3b 3b 3b 3b 3b 02 09 61 72 74 00 01 03 00   -.;;;;;..art....
  0030: 0c 0a 01 02 00 0d 01 00 20                        ........ 
Seed 2 (id=02e04c9299b6e4e1, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=172s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,ByteAddMutator,TokenReplace):
  0000: 00 95 6b 95 20 24 01 03 00 01 00 40 00 03 00 00   ..k. $.....@....
  0010: e0 20 00 00 00 18 00 00 20 b8 48 b8 b8 b8 b8 b8   . ...... .H.....
  0020: b8 b8 b8 06 02 00 80 20 b8                        ....... .
Seed 3 (id=034b3a94b7d5b64d, size=62 bytes, fuzzer=cmplog, trial=1, discovered_at=199s, mutation_op=QwordAddMutator):
  0000: 74 72 75 65 00 00 04 02 65 7f 64 6f 2d 0c 04 02   true....e.do-...
  0010: 02 00 ec 03 03 01 00 02 00 ec ed 1f 20 70 78 2d   ............ px-
  0020: 0e 7c 65 72 20 18 00 00 00 00 0d 06 00 02 02 ff   .|er ...........
  0030: ec 0c 0c 0c 0c 0c 0c 0c 0c 0c ec 22 22 22         ..........."""
Seed 4 (id=02b51d5c1a8c70da, size=53 bytes, fuzzer=cmplog, trial=1, discovered_at=413s, mutation_op=ByteRandMutator,TokenReplace,ByteNegMutator,ByteAddMutator):
  0000: 00 ff 01 00 00 01 00 1a 00 01 00 70 77 63 66 63   ...........pwcfc
  0010: 10 0d 01 00 21 0d 01 00 fd 06 00 00 60 10 00 00   ....!.......`...
  0020: 06 18 00 00 20 10 00 00 52 06 10 00 00 06 20 00   .... ...R..... .
  0030: 00 06 20 00 00                                    .. ..
Seed 5 (id=0335bf1465b48090, size=28 bytes, fuzzer=cmplog, trial=1, discovered_at=859s, mutation_op=BytesSwapMutator,BytesRandInsertMutator):
  0000: 86 18 00 00 00 a6 a6 10 20 10 7f ff ff ff 01 00   ........ .......
  0010: 6e 70 1c c5 17 01 00 16 17 00 80 ff               np..........


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  b4(.)x3 80(.)x1 00(.)x1 64(d)x1 +1u  00(.)x7 74(t)x1 86(.)x1 4f(O)x1     PARTIAL
   0x0001  00(.)x4 02(.)x1 01(.)x1 dc(.)x1     01(.)x4 20( )x1 95(.)x1 72(r)x1 +3u  PARTIAL
   0x0003  ff(.)x3 00(.)x2 2a(*)x1 dc(.)x1     00(.)x6 97(.)x1 95(.)x1 65(e)x1 +1u  PARTIAL
   0x0004  fe(.)x2 6f(o)x1 ac(.)x1 ff(.)x1 +2u  00(.)x9 20( )x1                     PARTIAL
   0x0008  00(.)x3 e7(.)x2 6b(k)x1 dc(.)x1     00(.)x3 20( )x3 21(!)x3 65(e)x1     PARTIAL
   0x000a  00(.)x3 e7(.)x2 03(.)x1 dc(.)x1     00(.)x4 64(d)x1 7f(.)x1 20( )x1 +3u  PARTIAL
   0x0011  17(.)x3 00(.)x2 10(.)x1 b6(.)x1     01(.)x4 0d(.)x2 20( )x1 00(.)x1 +2u  PARTIAL
   0x0012  00(.)x4 5f(_)x1 01(.)x1 b6(.)x1     00(.)x5 01(.)x2 ec(.)x1 1c(.)x1 +1u  PARTIAL
   0x0013  00(.)x6 03(.)x1                     00(.)x4 03(.)x1 c5(.)x1 0d(.)x1 +3u  PARTIAL
   0x0016  00(.)x5 b9(.)x1 a8(.)x1             00(.)x7 97(.)x1 01(.)x1 02(.)x1     PARTIAL
   0x0017  00(.)x6 98(.)x1                     10(.)x4 00(.)x2 02(.)x2 01(.)x1 +1u  PARTIAL
   0x0018  00(.)x3 f7(.)x1 ac(.)x1 10(.)x1 +1u  00(.)x7 20( )x1 fd(.)x1 17(.)x1     PARTIAL
   0x001a  00(.)x7                             00(.)x6 3b(;)x1 48(H)x1 ed(.)x1 +1u  PARTIAL
   0x001b  00(.)x6 d2(.)x1                     47(G)x3 3b(;)x1 b8(.)x1 1f(.)x1 +4u  PARTIAL
   0x001c  d2(.)x3 00(.)x2 b2(.)x1 17(.)x1     00(.)x3 3b(;)x1 b8(.)x1 20( )x1 +3u  PARTIAL
   0x001d  17(.)x3 00(.)x2 05(.)x1 fe(.)x1     01(.)x2 00(.)x2 3b(;)x1 b8(.)x1 +3u  PARTIAL
   0x001e  00(.)x6 20( )x1                     00(.)x3 73(s)x1 b8(.)x1 78(x)x1 +3u  PARTIAL
   0x001f  00(.)x6 b6(.)x1                     00(.)x2 03(.)x2 6e(n)x1 b8(.)x1 +3u  PARTIAL
   0x0022  00(.)x6 19(.)x1                     00(.)x5 3b(;)x1 b8(.)x1 65(e)x1 +1u  PARTIAL
   0x0023  00(.)x7                             02(.)x3 06(.)x2 3b(;)x1 72(r)x1 +2u  PARTIAL
   0x0025  00(.)x3 17(.)x2 e6(.)x1 c0(.)x1     00(.)x5 3b(;)x1 18(.)x1 10(.)x1 +1u  PARTIAL
   0x0026  00(.)x5 e6(.)x1 c0(.)x1             00(.)x7 3b(;)x1 80(.)x1             PARTIAL
   0x0027  00(.)x3 e6(.)x1 02(.)x1 d2(.)x1 +1u  10(.)x3 02(.)x2 20( )x2 00(.)x2     PARTIAL
   0x0028  00(.)x3 17(.)x2 01(.)x1 80(.)x1     00(.)x5 09(.)x1 b8(.)x1 52(R)x1 +1u  PARTIAL
   0x002a  00(.)x4 17(.)x2                     00(.)x4 72(r)x2 0d(.)x1 10(.)x1     PARTIAL
   0x002b  00(.)x5 ff(.)x1                     10(.)x3 00(.)x2 74(t)x1 06(.)x1 +1u  PARTIAL
   0x002c  00(.)x3 0f(.)x1 d2(.)x1 f0(.)x1     00(.)x6 11(.)x1 20( )x1             PARTIAL
   0x002e  00(.)x3 0c(.)x1 01(.)x1 f0(.)x1     00(.)x2 03(.)x1 02(.)x1 20( )x1 +3u  PARTIAL
   0x002f  00(.)x2 70(p)x1 03(.)x1 f0(.)x1     00(.)x3 ff(.)x1 73(s)x1 6c(l)x1 +2u  PARTIAL
   0x0031  2d(-)x2 00(.)x1 10(.)x1 f0(.)x1     0a(.)x1 0c(.)x1 06(.)x1 2d(-)x1 +4u  PARTIAL
   0x0032  68(h)x2 00(.)x2 ff(.)x1             00(.)x4 01(.)x1 0c(.)x1 20( )x1 +1u  PARTIAL
   0x0034  00(.)x2 6e(n)x1 17(.)x1 05(.)x1     00(.)x6 0c(.)x1 01(.)x1             PARTIAL
   0x0035  00(.)x3 74(t)x1 f6(.)x1             10(.)x2 0d(.)x1 0c(.)x1 01(.)x1 +2u  PARTIAL
   0x0036  00(.)x3 64(d)x1 68(h)x1             00(.)x4 01(.)x1 0c(.)x1 20( )x1     PARTIAL
   0x0037  00(.)x3 80(.)x1 6c(l)x1             00(.)x2 0c(.)x1 ff(.)x1 01(.)x1 +2u  PARTIAL
   0x0038  00(.)x3 0f(.)x1 67(g)x1             00(.)x2 20( )x1 0c(.)x1 ff(.)x1 +2u  PARTIAL
   0x0039  00(.)x2 0c(.)x1 54(T)x1 70(p)x1     0c(.)x1 00(.)x1 01(.)x1 06(.)x1 +2u  PARTIAL
   0x003a  00(.)x2 06(.)x1 f5(.)x1 bb(.)x1     00(.)x4 ec(.)x1 20( )x1             PARTIAL
   0x003b  00(.)x2 10(.)x1 f5(.)x1 14(.)x1     10(.)x2 22(")x1 17(.)x1 e9(.)x1 +1u  PARTIAL
   0x003c  00(.)x3 f5(.)x1 01(.)x1             00(.)x5 22(")x1                     PARTIAL
   ... (2 more divergent offsets)
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
  prompts_b/harfbuzz_5991.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5991,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5991 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5991 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5991 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).