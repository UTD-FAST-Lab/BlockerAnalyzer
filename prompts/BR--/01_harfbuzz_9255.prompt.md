==== BLOCKER ====
Target: harfbuzz
Branch ID: 9255
Location: /src/harfbuzz/src/hb-ot-shape.cc:274:12
Enclosing function: hb_ot_shape_plan_t::position(hb_font_t*, hb_buffer_t*) const
Source line:   else if (this->apply_fallback_kern)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 17  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.65h  loser=11.10h
  avg hitcount on branch: winner=33663  loser=2
  prob_div=0.90  dur_div=10.45h  hit_div=33661
  subject-level: delta_AUC=9064080.0  p_AUC=0.0002  delta_Final=796.1  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/9255/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_ot_shape_plan_t::position(hb_font_t*, hb_buffer_t*) const (/src/harfbuzz/src/hb-ot-shape.cc:262-281) ---
[ ]   260  hb_ot_shape_plan_t::position (hb_font_t   *font,
[ ]   261  			      hb_buffer_t *buffer) const
[B]   262  {
[B]   263    if (this->apply_gpos)
[W]   264      map.position (this, font, buffer);
[L]   265  #ifndef HB_NO_AAT_SHAPE
[L]   266    else if (this->apply_kerx)
[ ]   267      hb_aat_layout_position (this, font, buffer);
[B]   268  #endif
[ ]   269  
[B]   270  #ifndef HB_NO_OT_KERN
[B]   271    if (this->apply_kern)
[ ]   272      hb_ot_layout_kern (this, font, buffer);
[B]   273  #endif
[B]   274    else if (this->apply_fallback_kern) <-- BLOCKER
[L]   275      _hb_ot_shape_fallback_kern (this, font, buffer);
[ ]   276  
[B]   277  #ifndef HB_NO_AAT_SHAPE
[B]   278    if (this->apply_trak)
[ ]   279      hb_aat_layout_track (this, font, buffer);
[B]   280  #endif
[B]   281  }

--- Caller (1 hop): hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*) (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097, calls hb_ot_shape_plan_t::position(hb_font_t*, hb_buffer_t*) const at line 1063) (±10 around call site) ---
[L]  1053        case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_EARLY:
[L]  1054  	zero_mark_widths_by_gdef (c->buffer, adjust_offsets_when_zeroing);
[L]  1055  	break;
[ ]  1056  
[ ]  1057        default:
[ ]  1058        case HB_OT_SHAPE_ZERO_WIDTH_MARKS_NONE:
[B]  1059        case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
[B]  1060  	break;
[B]  1061      }
[ ]  1062  
[B]  1063    c->plan->position (c->font, c->buffer); <-- CALL
[ ]  1064  
[B]  1065    if (c->plan->zero_marks)
[B]  1066      switch (c->plan->shaper->zero_width_marks)
[B]  1067      {
[B]  1068        case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
[B]  1069  	zero_mark_widths_by_gdef (c->buffer, adjust_offsets_when_zeroing);
[B]  1070  	break;
[ ]  1071  
[ ]  1072        default:
[ ]  1073        case HB_OT_SHAPE_ZERO_WIDTH_MARKS_NONE:

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097, calls hb_ot_shape_plan_t::position(hb_font_t*, hb_buffer_t*) const at line 1063)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        16  hb-ot-shape.cc:zero_mark_width(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:967-970)
       0        13  hb-ot-shape.cc:adjust_mark_offsets(hb_glyph_position_t*)  (/src/harfbuzz/src/hb-ot-shape.cc:960-963)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shape.cc:hb_ot_position_plan(hb_ot_shape_context_t const*)  (/src/harfbuzz/src/hb-ot-shape.cc:1022-1097) ---
  d=2   L1036  T=0 F=210  T=131 F=0  bool adjust_offsets_when_zeroing = c->plan->adjust_mark_p...
  d=2   L1050  T=210 F=0  T=128 F=3  if (c->plan->zero_marks)
  d=2   L1053  T=0 F=210  T=1 F=127  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_EARLY:
  d=2   L1059  T=210 F=0  T=127 F=1  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
  d=2   L1065  T=210 F=0  T=128 F=3  if (c->plan->zero_marks)
  d=2   L1068  T=210 F=0  T=127 F=1  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_LATE:
  d=2   L1074  T=0 F=210  T=1 F=127  case HB_OT_SHAPE_ZERO_WIDTH_MARKS_BY_GDEF_EARLY:
  d=2   L1094  T=0 F=210  T=127 F=4  if (c->plan->fallback_mark_positioning)
--- d=1  hb_ot_shape_plan_t::position(hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-shape.cc:262-281) ---
  d=1   L 263  T=210 F=0  T=0 F=131  if (this->apply_gpos)
  d=1   L 266  T=0 F=0  T=0 F=131  else if (this->apply_kerx)
  d=1   L 274  T=0 F=210  T=131 F=0  else if (this->apply_fallback_kern)  <-- BLOCKER

[off-chain: 42 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=001af94af95ed053, size=333 bytes, fuzzer=cmplog, trial=1, discovered_at=4178s, mutation_op=BytesRandInsertMutator,BytesInsertCopyMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 04 20 00 00 7f 00 20 7f 20 56 56   ...... .... . VV
  0010: 41 51 b9 b9 01 01 ff ff fe f2 1a 20 47 50 4f 53   AQ......... GPOS
  0020: 00 22 03 20 00 00 00 00 ff ff ff 01 06 00 00 00   .". ............
  0030: 00 00 00 00 00 78 78 78 78 78 78 78 78 78 78 78   .....xxxxxxxxxxx
Seed 2 (id=000abbc88e443f45, size=305 bytes, fuzzer=cmplog, trial=1, discovered_at=4294s, mutation_op=BytesInsertMutator,QwordAddMutator,BytesDeleteMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 04 20 06 00 7f 00 20 20 20 56 56   ...... ....   VV
  0010: 41 51 b9 b9 b9 01 ff ff fe f2 1a 20 47 50 4f 53   AQ......... GPOS
  0020: 01 00 00 20 00 00 00 00 ff 83 ff 10 03 00 00 00   ... ............
  0030: 1e 00 00 00 00 78 78 78 78 78 78 78 78 78 79 78   .....xxxxxxxxxyx
Seed 3 (id=001aa99c1a5eb88c, size=483 bytes, fuzzer=cmplog, trial=1, discovered_at=4334s, mutation_op=BytesCopyMutator,BytesSwapMutator,BytesInsertMutator,ByteIncMutator,ByteAddMutator,WordInterestingMutator):
  0000: 00 01 00 00 00 04 20 06 00 7f 00 20 20 20 56 56   ...... ....   VV
  0010: 41 51 64 b9 b9 00 ff ff fe f2 1a 20 47 50 4f 53   AQd........ GPOS
  0020: 01 01 00 20 00 00 00 00 ff ff ff 00 ff 00 00 00   ... ............
  0030: c4 00 00 00 00 78 78 78 78 78 78 78 78 78 78 78   .....xxxxxxxxxxx
Seed 4 (id=0015871726123237, size=783 bytes, fuzzer=cmplog, trial=1, discovered_at=5245s, mutation_op=BytesRandInsertMutator,BytesInsertMutator,BytesDeleteMutator,ByteAddMutator,DwordInterestingMutator):
  0000: 00 01 00 00 00 04 20 00 00 7f 00 20 20 20 56 56   ...... ....   VV
  0010: 41 51 b9 b9 b9 01 7f ff fe f2 1a 27 47 50 4f 53   AQ.........'GPOS
  0020: 01 00 03 20 00 00 00 00 ff ff ff 10 03 02 04 00   ... ............
  0030: 00 03 00 00 00 78 78 78 78 78 78 78 78 78 78 78   .....xxxxxxxxxxx
Seed 5 (id=000fc4fb6ae07c71, size=564 bytes, fuzzer=cmplog, trial=1, discovered_at=5492s, mutation_op=WordAddMutator,BytesInsertCopyMutator,BytesDeleteMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 04 20 00 00 7f 00 20 20 20 56 56   ...... ....   VV
  0010: 41 51 b9 b9 b9 01 ff ff fe f2 1a 20 47 50 4f 53   AQ......... GPOS
  0020: 17 18 03 20 00 00 00 00 ff ff ff 10 03 00 00 00   ... ............
  0030: 00 00 00 00 00 78 78 78 78 78 78 78 78 78 78 78   .....xxxxxxxxxxx

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0011f576377302cd, size=32 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=BytesInsertMutator,BytesSetMutator,CrossoverInsertMutator):
  0000: 00 00 00 04 00 ff 00 00 00 66 72 6e 20 20 20 20   .........frn    
  0010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ff   ................
Seed 2 (id=000df35f3b4fe783, size=64 bytes, fuzzer=naive, trial=1, discovered_at=4s, mutation_op=ByteRandMutator,QwordAddMutator,BytesExpandMutator,WordInterestingMutator,WordAddMutator,ByteFlipMutator):
  0000: 01 20 7a 80 00 00 e9 ff 20 00 00 10 1a 20 21 71   . z..... .... !q
  0010: 67 20 20 00 00 07 00 00 20 e2 e2 e2 00 00 00 01   g  ..... .......
  0020: 20 6b 03 01 00 e7 ff ff 00 20 6b 65 72 6e 20 20    k....... kern  
  0030: 20 20 00 00 00 b6 b6 20 ad 00 00 00 b6 b6 20 ad     ..... ...... .
Seed 3 (id=000942ea696f94ed, size=41 bytes, fuzzer=naive, trial=1, discovered_at=7s, mutation_op=BytesDeleteMutator,ByteRandMutator):
  0000: 00 01 01 00 ff 01 20 20 20 20 47 20 00 10 00 00   ......    G ....
  0010: 94 65 72 6e 20 20 20 20 20 00 00 00 1a 20 20 3c   .ern     ....  <
  0020: df 20 00 00 00 b5 b5 b5 b5                        . .......
Seed 4 (id=000cb26662465dd2, size=64 bytes, fuzzer=naive, trial=1, discovered_at=79s, mutation_op=TokenInsert,BytesCopyMutator,ByteInterestingMutator,BytesDeleteMutator,WordInterestingMutator,ByteIncMutator,TokenInsert):
  0000: 00 47 00 47 47 47 47 47 fb fb fb 6f 2d 00 fb fb   .G.GGGGG...o-...
  0010: f0 fb fb fb fb fb fb 00 7f ff 00 fb 56 55 55 15   ............VUU.
  0020: b3 00 00 00 b3 17 00 00 e2 e2 e2 e2 a4 47 a4 a4   .............G..
  0030: a4 a4 a4 a4 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2 e2   ................
Seed 5 (id=00108eb819d24048, size=58 bytes, fuzzer=naive, trial=1, discovered_at=155s, mutation_op=ByteIncMutator,ByteFlipMutator,BitFlipMutator):
  0000: 00 00 1a 00 00 00 23 21 20 0a 00 00 00 1a 01 00   ......#! .......
  0010: 00 0a 00 00 00 23 00 00 0c a3 00 00 0c 0c 02 01   .....#..........
  0020: 00 10 00 0c 0c 12 8a 8a 8a 8a 8a 8a 8a 8a 8a 8a   ................
  0030: 8a 69 8a 1c e3 1c 1c 1c 1c 1c                     .i........


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x10                            00(.)x5 01(.)x1 4b(K)x1 6d(m)x1 +2u  PARTIAL
   0x0001  01(.)x10                            00(.)x2 20( )x1 01(.)x1 47(G)x1 +5u  PARTIAL
   0x0002  00(.)x10                            00(.)x6 7a(z)x1 01(.)x1 1a(.)x1 +1u  PARTIAL
   0x0003  00(.)x10                            00(.)x4 ff(.)x2 04(.)x1 80(.)x1 +2u  PARTIAL
   0x0004  00(.)x10                            00(.)x3 ff(.)x1 47(G)x1 03(.)x1 +4u  PARTIAL
   0x0005  04(.)x10                            00(.)x2 06(.)x2 ff(.)x1 01(.)x1 +4u  DIFFER
   0x0006  20( )x9 1b(.)x1                     00(.)x3 e9(.)x1 20( )x1 47(G)x1 +4u  PARTIAL
   0x0007  00(.)x5 06(.)x4 03(.)x1             00(.)x3 ff(.)x2 20( )x1 47(G)x1 +3u  PARTIAL
   0x0008  00(.)x10                            20( )x3 00(.)x2 fb(.)x1 70(p)x1 +3u  PARTIAL
   0x0009  7f(.)x10                            66(f)x1 00(.)x1 20( )x1 fb(.)x1 +6u  DIFFER
   0x000a  00(.)x10                            00(.)x7 72(r)x1 47(G)x1 fb(.)x1     PARTIAL
   0x000b  20( )x9 ff(.)x1                     00(.)x4 10(.)x2 6e(n)x1 20( )x1 +2u  PARTIAL
   0x000c  20( )x8 7f(.)x1 ff(.)x1             00(.)x2 20( )x1 1a(.)x1 2d(-)x1 +5u  PARTIAL
   0x000d  20( )x9 ff(.)x1                     20( )x2 06(.)x2 10(.)x1 00(.)x1 +4u  PARTIAL
   0x000e  56(V)x9 03(.)x1                     00(.)x3 20( )x1 21(!)x1 fb(.)x1 +4u  DIFFER
   0x000f  56(V)x10                            00(.)x5 20( )x1 71(q)x1 fb(.)x1 +2u  DIFFER
   0x0010  41(A)x10                            00(.)x2 67(g)x1 94(.)x1 f0(.)x1 +5u  DIFFER
   0x0011  51(Q)x10                            00(.)x1 20( )x1 65(e)x1 fb(.)x1 +6u  DIFFER
   0x0012  b9(.)x9 64(d)x1                     00(.)x4 20( )x1 72(r)x1 fb(.)x1 +3u  DIFFER
   0x0013  b9(.)x10                            00(.)x6 6e(n)x1 fb(.)x1 29())x1 +1u  DIFFER
   0x0014  b9(.)x9 01(.)x1                     00(.)x3 20( )x1 fb(.)x1 37(7)x1 +4u  DIFFER
   0x0015  01(.)x5 00(.)x5                     00(.)x1 07(.)x1 20( )x1 fb(.)x1 +6u  PARTIAL
   0x0016  ff(.)x8 7f(.)x1 18(.)x1             00(.)x5 20( )x1 fb(.)x1 ff(.)x1 +2u  PARTIAL
   0x0017  ff(.)x9 00(.)x1                     00(.)x6 20( )x1 ef(.)x1 0c(.)x1 +1u  PARTIAL
   0x0018  fe(.)x10                            00(.)x3 20( )x2 7f(.)x1 0c(.)x1 +3u  DIFFER
   0x0019  f2(.)x10                            00(.)x3 06(.)x2 e2(.)x1 ff(.)x1 +3u  DIFFER
   0x001a  1a(.)x10                            00(.)x8 e2(.)x1 09(.)x1             DIFFER
   0x001b  20( )x9 27(')x1                     00(.)x7 e2(.)x1 fb(.)x1 09(.)x1     DIFFER
   0x001c  47(G)x10                            00(.)x5 1a(.)x1 56(V)x1 0c(.)x1 +2u  DIFFER
   0x001d  50(P)x10                            00(.)x2 20( )x2 55(U)x1 0c(.)x1 +4u  DIFFER
   0x001e  4f(O)x10                            00(.)x4 20( )x1 55(U)x1 02(.)x1 +3u  DIFFER
   0x001f  53(S)x10                            00(.)x3 01(.)x2 ff(.)x1 3c(<)x1 +3u  DIFFER
   0x0020  00(.)x5 01(.)x3 17(.)x2             00(.)x4 20( )x1 df(.)x1 b3(.)x1 +2u  PARTIAL
   0x0021  00(.)x7 22(")x1 01(.)x1 18(.)x1     6b(k)x1 20( )x1 00(.)x1 10(.)x1 +5u  PARTIAL
   0x0022  03(.)x8 00(.)x2                     00(.)x6 03(.)x1 69(i)x1 09(.)x1     PARTIAL
   0x0023  20( )x9 13(.)x1                     00(.)x5 01(.)x1 0c(.)x1 69(i)x1 +1u  DIFFER
   0x0024  00(.)x10                            00(.)x3 b3(.)x1 0c(.)x1 b6(.)x1 +3u  PARTIAL
   0x0025  00(.)x10                            e7(.)x1 b5(.)x1 17(.)x1 12(.)x1 +5u  DIFFER
   0x0026  00(.)x10                            00(.)x2 ff(.)x1 b5(.)x1 8a(.)x1 +4u  PARTIAL
   0x0027  00(.)x10                            00(.)x4 ff(.)x1 b5(.)x1 8a(.)x1 +2u  PARTIAL
   ... (23 more divergent offsets)
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
rows are exclusive to cmplog and value_profile_cmplog; their
presence in a winning seed's ancestor chain is direct (lower-bound)
evidence of I2S contribution.

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
  prompts/BR--/01_harfbuzz_9255.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9255,
  "target": "harfbuzz",
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
      // pick EXACTLY ONE of:
      //   "I2SRandReplace"     (cmplog / vpc input-to-state substitution)
      //   "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)
      //   "havoc-only"         (lucky havoc byte mutation, no CMP introspection)
      //   "token-replace"      (TokenInsert/TokenReplace dictionary mutations)
      //   "other"              (anything that does not fit the four above)
    "verified_in_lineage": true,
      // pick true or false
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9255 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9255 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9255 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).