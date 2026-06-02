==== BLOCKER ====
Target: harfbuzz
Branch ID: 5866
Location: /src/harfbuzz/src/hb-ot-shaper-indic.cc:982:5
Enclosing function: hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)
Source line:     case indic_symbol_cluster:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive); loser (value_profile vs value_profile_cmplog); loser (grimoire_structural vs grimoire)
value_profile                   10        0          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'naive', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (3) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.80h  loser=22.50h
  avg hitcount on branch: winner=88  loser=0
  prob_div=0.90  dur_div=21.70h  hit_div=88
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 13  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.60h  loser=22.50h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.70  dur_div=14.90h  hit_div=4
  subject-level: delta_AUC=91657080.0  p_AUC=0.0002  delta_Final=1608.6  p_final=0.0002
--- Pair 3: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 20  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.60h  loser=22.50h
  avg hitcount on branch: winner=3  loser=0
  prob_div=0.70  dur_div=14.90h  hit_div=2
  subject-level: delta_AUC=45443160.0  p_AUC=0.001  delta_Final=636.4  p_final=0.0006

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5866/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986) ---
[ ]   966  				   hb_buffer_t *buffer,
[ ]   967  				   unsigned int start, unsigned int end)
[B]   968  {
[B]   969    indic_syllable_type_t syllable_type = (indic_syllable_type_t) (buffer->info[start].syllable() & 0x0F);
[B]   970    switch (syllable_type)
[B]   971    {
[W]   972      case indic_vowel_syllable: /* We made the vowels look like consonants.  So let's call the consonant logic! */
[B]   973      case indic_consonant_syllable:
[B]   974       initial_reordering_consonant_syllable (plan, face, buffer, start, end);
[B]   975       break;
[ ]   976  
[B]   977      case indic_broken_cluster: /* We already inserted dotted-circles, so just call the standalone_cluster. */
[B]   978      case indic_standalone_cluster:
[B]   979       initial_reordering_standalone_cluster (plan, face, buffer, start, end);
[B]   980       break;
[ ]   981  
[W]   982      case indic_symbol_cluster: <-- BLOCKER
[B]   983      case indic_non_indic_cluster:
[B]   984        break;
[B]   985    }
[B]   986  }

--- Caller (1 hop): hb-ot-shaper-indic.cc:initial_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:992-1011, calls hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 1006) (full body — short) ---
[B]   992  {
[B]   993    bool ret = false;
[B]   994    if (!buffer->message (font, "start reordering indic initial"))
[ ]   995      return ret;
[ ]   996  
[B]   997    update_consonant_positions_indic (plan, font, buffer);
[B]   998    if (hb_syllabic_insert_dotted_circles (font, buffer,
[B]   999  					 indic_broken_cluster,
[B]  1000  					 I_Cat(DOTTEDCIRCLE),
[B]  1001  					 I_Cat(Repha),
[B]  1002  					 POS_END))
[ ]  1003      ret = true;
[ ]  1004  
[B]  1005    foreach_syllable (buffer, start, end)
[B]  1006      initial_reordering_syllable_indic (plan, font->face, buffer, start, end); <-- CALL
[ ]  1007  
[B]  1008    (void) buffer->message (font, "end reordering indic initial");
[ ]  1009  
[B]  1010    return ret;
[B]  1011  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-indic.cc:initial_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:992-1011, calls hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int) at line 1006)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0         1  hb-ot-shaper-indic.cc:is_halant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:86-88)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986) ---
  d=1   L 972  T=2 F=194  T=0 F=156  case indic_vowel_syllable: /* We made the vowels look lik...
  d=1   L 982  T=30 F=166  T=0 F=156  case indic_symbol_cluster:  <-- BLOCKER

[off-chain: 37 additional divergent branches across 4 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=f15deb24521daa17, size=26 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=85s, mutation_op=BytesDeleteMutator,BitFlipMutator,BytesExpandMutator,ByteRandMutator):
  0000: 3d 0d 00 00 00 05 55 00 00 00 00 76 72 00 20 12   =.....U....vr. .
  0010: 20 20 20 20 20 12 20 20 20 20                          .    
Seed 2 (id=ce09bb2d97eac25b, size=14 bytes, fuzzer=grimoire, trial=1, discovered_at=827s):
  0000: f2 a8 00 00 00 fe 00 00 00 00 00 01 00 06         ..............
Seed 3 (id=68d1ae222de2c678, size=14 bytes, fuzzer=grimoire, trial=1, discovered_at=1173s):
  0000: f2 a8 00 00 f2 a8 00 00 dc 09 00 00 00 06         ..............
Seed 4 (id=0d2bd6067cf33275, size=32 bytes, fuzzer=naive, trial=1, discovered_at=2173s, mutation_op=DwordAddMutator,BytesInsertCopyMutator,ByteFlipMutator,BytesDeleteMutator):
  0000: f3 a8 00 00 f7 1c 00 00 9f a2 a2 a2 a2 a8 00 00   ................
  0010: f7 1c 00 00 a2 a2 a2 a2 a2 a2 a2 a2 5d a2 a2 a2   ............]...
Seed 5 (id=39a78dfab3b51ba9, size=109 bytes, fuzzer=naive, trial=1, discovered_at=2645s, mutation_op=DwordAddMutator,ByteInterestingMutator,BytesRandSetMutator,QwordAddMutator,TokenReplace,BytesDeleteMutator):
  0000: 01 73 69 7a 01 73 69 7a 65 0f 00 00 7a 6f 2d b5   .siz.size...zo-.
  0010: b0 00 10 00 2d 2d 96 00 ec 72 6e 2d 68 61 6e 73   ....--...rn-hans
  0020: 00 6a 40 0c 00 00 00 fe 00 00 e8 f1 f1 0c 0c 00   .j@.............
  0030: 00 00 0c 00 00 00 00 02 00 01 00 64 65 56 10 00   ...........deV..

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0237ec581d21f6c0, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=9s, mutation_op=BytesInsertMutator):
  0000: ff 20 20 20 20 6b 65 72 6e 20 df 10 20 0a 00 00   .    kern .. ...
  0010: 1a 20 00 1a 1a 1a 1a 1a 1a 1a 1a 1a 1a 1a 1a 1a   . ..............
  0020: 1a 1a 00 00 00 00 00 7f 20                        ........ 
Seed 2 (id=007e652bc601c59b, size=38 bytes, fuzzer=cmplog, trial=1, discovered_at=21s, mutation_op=TokenInsert,QwordAddMutator,BytesDeleteMutator):
  0000: df 6b 66 20 72 8b 20 20 20 20 0a 01 8a 00 1a fb   .kf r.    ......
  0010: 00 0d 00 00 ef 01 00 72 6d 75 6e 00 01 0d 00 00   .......rmun.....
  0020: ef 01 00 0f e4 20                                 ..... 
Seed 3 (id=00cc7bf7b8cade2f, size=48 bytes, fuzzer=cmplog, trial=1, discovered_at=289s, mutation_op=ByteAddMutator,TokenReplace,ByteRandMutator):
  0000: ff 22 20 20 20 6b 65 00 00 03 e8 10 20 0a 00 00   ."   ke..... ...
  0010: 6a 64 66 6d 5a 20 00 7f 00 00 d2 00 7f 20 00 00   jdfmZ ....... ..
  0020: 36 00 00 00 36 04 00 00 00 00 00 00 d2 00 6b 20   6...6.........k 
Seed 4 (id=0283ed93d64a4a34, size=39 bytes, fuzzer=cmplog, trial=1, discovered_at=297s, mutation_op=BytesRandSetMutator,BytesExpandMutator,BytesDeleteMutator,CrossoverReplaceMutator):
  0000: 17 00 00 00 00 20 20 00 00 01 20 2c 20 00 00 0c   .....  ... , ...
  0010: 00 0d 00 00 00 a0 00 00 00 00 00 00 00 a0 00 00   ................
  0020: 00 00 00 00 00 a0 00                              .......
Seed 5 (id=018af0e4aa381eaa, size=76 bytes, fuzzer=cmplog, trial=1, discovered_at=1353s, mutation_op=ByteDecMutator,WordAddMutator,BytesInsertMutator,WordAddMutator,ByteFlipMutator,WordAddMutator,DwordAddMutator):
  0000: 00 00 00 00 2b 0d 01 10 c0 0a 00 00 bf 0a 00 00   ....+...........
  0010: bf 0a 00 00 bf 0a 00 00 bf 0a 00 00 00 0c 05 05   ................
  0020: 04 f5 05 05 26 05 05 05 ff ff ff ff ff ff ff ff   ....&...........
  0030: ff ff ff 00 ff 05 05 05 05 05 f0 ff 00 30 ff ff   .............0..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f2(.)x2 35(5)x2 3d(=)x1 f3(.)x1 +7u  00(.)x5 ff(.)x3 df(.)x1 17(.)x1     DIFFER
   0x0002  00(.)x7 69(i)x1 a9(.)x1 c5(.)x1 +3u  00(.)x6 20( )x2 66(f)x1 7f(.)x1     PARTIAL
   0x0003  00(.)x6 64(d)x2 7a(z)x1 ff(.)x1 +3u  00(.)x6 20( )x4                     PARTIAL
   0x000d  06(.)x2 17(.)x2 00(.)x1 a8(.)x1 +7u  50(P)x4 0a(.)x3 00(.)x3             PARTIAL
   0x000e  00(.)x4 20( )x1 2d(-)x1 72(r)x1 +4u  00(.)x5 4f(O)x4 1a(.)x1             PARTIAL
   0x0012  00(.)x5 0c(.)x2 20( )x1 10(.)x1 +2u  00(.)x9 66(f)x1                     PARTIAL
   0x0013  00(.)x8 20( )x2 6a(j)x1             00(.)x4 0d(.)x2 1a(.)x1 6d(m)x1 +2u  PARTIAL
   0x0016  00(.)x3 20( )x1 a2(.)x1 96(.)x1 +5u  00(.)x8 1a(.)x1 20( )x1             PARTIAL
   0x001b  00(.)x4 a2(.)x1 2d(-)x1 ff(.)x1 +3u  00(.)x5 47(G)x3 1a(.)x1 01(.)x1     PARTIAL
   0x0022  00(.)x4 0c(.)x2 40(@)x1 80(.)x1 +1u  00(.)x8 05(.)x1 08(.)x1             PARTIAL
   0x0023  00(.)x6 0c(.)x2 20( )x1             00(.)x3 02(.)x2 0f(.)x1 05(.)x1 +3u  PARTIAL
   0x0025  00(.)x5 0c(.)x2 4c(L)x1 25(%)x1     00(.)x4 20( )x1 04(.)x1 a0(.)x1 +3u  PARTIAL
   0x0026  00(.)x6 0c(.)x2 ec(.)x1             00(.)x6 05(.)x1 1d(.)x1 ff(.)x1     PARTIAL
   0x0029  00(.)x5 0c(.)x2 dc(.)x1             00(.)x4 ff(.)x1 01(.)x1 22(")x1     PARTIAL
   0x002a  00(.)x4 e8(.)x1 bd(.)x1 0c(.)x1 +1u  00(.)x5 ff(.)x1 02(.)x1             PARTIAL
   0x002b  00(.)x3 f1(.)x1 f7(.)x1 bd(.)x1 +2u  10(.)x3 00(.)x2 ff(.)x1 6a(j)x1     PARTIAL
   0x002d  00(.)x4 0c(.)x2 17(.)x1 bd(.)x1     00(.)x2 ff(.)x1 66(f)x1 06(.)x1 +2u  PARTIAL
   0x002e  00(.)x4 0c(.)x3 bd(.)x1             00(.)x3 6b(k)x1 ff(.)x1 6d(m)x1 +1u  PARTIAL
   0x002f  00(.)x5 0c(.)x1 bd(.)x1 20( )x1     20( )x1 ff(.)x1 5a(Z)x1 06(.)x1 +3u  PARTIAL
   0x0030  00(.)x4 61(a)x1 cb(.)x1 bd(.)x1 +1u  00(.)x3 ff(.)x1 20( )x1 0f(.)x1     PARTIAL
   0x0032  00(.)x3 0c(.)x1 05(.)x1 bd(.)x1 +2u  00(.)x3 ff(.)x1 72(r)x1 64(d)x1     PARTIAL
   0x0034  00(.)x3 17(.)x2 45(E)x1 10(.)x1 +1u  00(.)x3 ff(.)x1 6e(n)x1 01(.)x1     PARTIAL
   0x0035  00(.)x6 05(.)x2                     05(.)x1 03(.)x1 00(.)x1 01(.)x1 +2u  PARTIAL
   0x0036  00(.)x4 1c(.)x1 05(.)x1 0c(.)x1 +1u  05(.)x2 00(.)x2 01(.)x1 fa(.)x1     PARTIAL
   0x0038  00(.)x3 1c(.)x1 f4(.)x1 05(.)x1 +2u  00(.)x3 05(.)x1 2a(*)x1 01(.)x1     PARTIAL
   0x0039  00(.)x4 1c(.)x2 01(.)x1 66(f)x1     06(.)x3 05(.)x1 24($)x1 01(.)x1     PARTIAL
   0x003b  64(d)x1 f7(.)x1 1c(.)x1 bd(.)x1 +3u  00(.)x2 10(.)x2 ff(.)x1 04(.)x1     PARTIAL
   0x003c  1c(.)x2 00(.)x2 65(e)x1 e2(.)x1 +1u  00(.)x3 1d(.)x1 01(.)x1 18(.)x1     PARTIAL
   0x003d  00(.)x5 56(V)x1 1c(.)x1             30(0)x1 d2(.)x1 00(.)x1 01(.)x1 +2u  PARTIAL
   0x003e  00(.)x4 10(.)x1 1c(.)x1 0c(.)x1     00(.)x2 ff(.)x1 e9(.)x1 01(.)x1 +1u  PARTIAL
   0x003f  00(.)x3 c2(.)x1 1c(.)x1 cb(.)x1 +1u  ff(.)x3 7f(.)x1 f0(.)x1 01(.)x1     DIFFER
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

--- grimoire ---
**Baseline relationship**: grimoire builds on the full cmplog stack —
it includes the `CmpLogObserver`, the `TracingStage`, and the
`I2SRandReplace` (i2s) stage — and ADDS a `GeneralizationStage` plus
Grimoire structural mutators. The single-technique delta is therefore
`grimoire` vs `cmplog` (both have I2S; grimoire adds generalization +
Grimoire mutators), not vs naive.

**Instrumentation**: cmplog's edge counters + per-execution CMP buffer
(`CmpLogObserver`).

**Feedback**: edge-bucket `MaxMapFeedback`.

**Mutators / stages**: stages are
`[generalization, tracing, i2s, havoc, grimoire]`. `GeneralizationStage`
replaces concrete byte runs in a corpus entry with `<GAP>` placeholders
(a generalised input) by repeatedly re-executing and checking that
coverage is preserved. The Grimoire mutators —
`GrimoireExtensionMutator`, `GrimoireRecursiveReplacementMutator`,
`GrimoireStringReplacementMutator`, `GrimoireRandomDeleteMutator` —
splice and recurse on these generalised token/gap structures
(string-based, grammar-free structural mutation). `I2SRandReplace` (the
cmplog i2s stage) also runs.

**Observed `mutation_op` in seed metadata**: all grimoire stages (i2s,
havoc, grimoire) are wrapped in `LineageMutatorWrap` with **no
per-operator name list**, so grimoire seeds appear nameless in lineage
(`mutation_op = -`). As with mopt, nameless rows are NOT an
I2S-exclusive signal here — and grimoire genuinely runs I2S too, so the
two are not separable from lineage names.

**Per-execution cost**: cmplog's per-CMP cost, plus extra executions
during generalization (each candidate gap is validated by a re-run).

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
  prompts_b/harfbuzz_5866.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5866,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile_cmplog>cmplog (value_profile), grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5866 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5866 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5866 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).