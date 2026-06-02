==== BLOCKER ====
Target: harfbuzz
Branch ID: 5517
Location: /src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:716:7
Enclosing function: OT::hb_ot_apply_context_t::hb_ot_apply_context_t(unsigned int, hb_font_t*, hb_buffer_t*)
Source line: 					 table_index == 1 && font->num_coords ? var_store.create_cache () : nullptr
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog); loser (value_profile vs value_profile); loser (ctx_coverage vs naive_ctx); loser (calibrated_energy vs minimizer)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        9        1          0  winner (ctx_coverage vs naive)
naive_ngram4                     2        8          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        9        1          0  winner (calibrated_energy vs naive)
fast                             9        1          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'minimizer', 'naive', 'naive_ctx', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['value_profile_cmplog', 'naive_ngram4', 'mopt', 'fast', 'grimoire']

==== DECISIVE PAIRS (4) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.30h  loser=21.20h
  avg hitcount on branch: winner=46460  loser=469
  prob_div=0.80  dur_div=20.90h  hit_div=45991
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile > naive  [delta: value_profile] ---
  subject 12  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=9.10h  loser=21.20h
  avg hitcount on branch: winner=3565  loser=469
  prob_div=0.70  dur_div=12.10h  hit_div=3096
  subject-level: delta_AUC=17795340.0  p_AUC=0.0002  delta_Final=285.0  p_final=0.0002
--- Pair 3: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 15  (naive_ctx vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=10.80h  loser=21.20h
  avg hitcount on branch: winner=5066  loser=469
  prob_div=0.70  dur_div=10.40h  hit_div=4597
  subject-level: delta_AUC=15634800.0  p_AUC=0.0003  delta_Final=258.3  p_final=0.0002
--- Pair 4: minimizer > naive  [delta: calibrated_energy] ---
  subject 18  (minimizer vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=5.30h  loser=21.20h
  avg hitcount on branch: winner=6910  loser=469
  prob_div=0.70  dur_div=15.90h  hit_div=6441
  subject-level: delta_AUC=13277160.0  p_AUC=0.001  delta_Final=189.1  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5517/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::hb_ot_apply_context_t::hb_ot_apply_context_t(unsigned int, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:704-724) ---
[ ]   702  			 hb_font_t *font_,
[ ]   703  			 hb_buffer_t *buffer_) :
[B]   704  			table_index (table_index_),
[B]   705  			font (font_), face (font->face), buffer (buffer_),
[ ]   706  			gdef (
[ ]   707  #ifndef HB_NO_OT_LAYOUT
[B]   708  			      *face->table.GDEF->table
[ ]   709  #else
[ ]   710  			      Null (GDEF)
[ ]   711  #endif
[ ]   712  			     ),
[B]   713  			var_store (gdef.get_var_store ()),
[ ]   714  			var_store_cache (
[ ]   715  #ifndef HB_NO_VAR
[B]   716  					 table_index == 1 && font->num_coords ? var_store.create_cache () : nullptr <-- BLOCKER
[ ]   717  #else
[ ]   718  					 nullptr
[ ]   719  #endif
[ ]   720  					),
[B]   721  			digest (buffer_->digest ()),
[B]   722  			direction (buffer_->props.direction),
[B]   723  			has_glyph_classes (gdef.has_glyph_classes ())
[B]   724    { init_iters (); }

--- No 1-hop callers of OT::hb_ot_apply_context_t::hb_ot_apply_context_t(unsigned int, hb_font_t*, hb_buffer_t*) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    5320       422  OT::hb_ot_apply_context_t::matcher_t::set_ignore_zwnj(bool)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:414-414)
    5320       422  OT::hb_ot_apply_context_t::matcher_t::set_ignore_zwj(bool)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:415-415)
    5320       422  OT::hb_ot_apply_context_t::matcher_t::set_lookup_props(unsigned int)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:416-416)
    5320       422  OT::hb_ot_apply_context_t::matcher_t::set_mask(unsigned int)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:417-417)
    5320       422  OT::hb_ot_apply_context_t::matcher_t::set_per_syllable(bool)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:418-418)
    5320       422  OT::hb_ot_apply_context_t::matcher_t::set_match_func(bool (*)(hb_glyph_info_t&, unsigned int, void const*), void const*)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:422-422)
    5320       422  OT::hb_ot_apply_context_t::skipping_iterator_t::init(OT::hb_ot_apply_context_t*, bool)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:477-491)
    2920       422  OT::hb_ot_apply_context_t::matcher_t::matcher_t()  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:403-410)
    2660       211  OT::hb_ot_apply_context_t::init_iters()  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:734-737)
    1710         0  OT::hb_ot_apply_context_t::matcher_t::set_syllable(unsigned char)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:419-419)
    1710         0  OT::hb_ot_apply_context_t::skipping_iterator_t::reset(unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:518-523)
    1710         0  OT::hb_ot_apply_context_t::skipping_iterator_t::next(unsigned int*)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:536-572)
    1350         0  OT::hb_intersects_context_t::return_t OT::ChainContext::dispatch<OT::hb_intersects_context_t>(OT::hb_intersects_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
    1350         0  OT::hb_ot_apply_context_t::return_t OT::ChainContext::dispatch<OT::hb_ot_apply_context_t>(OT::hb_ot_apply_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
    1350         0  OT::hb_collect_glyphs_context_t::return_t OT::ChainContext::dispatch<OT::hb_collect_glyphs_context_t>(OT::hb_collect_glyphs_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
... (142 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::hb_ot_apply_context_t::hb_ot_apply_context_t(unsigned int, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:704-724) ---
  d=1   L 716  T=752 F=710  T=0 F=211  table_index == 1 && font->num_coords ? var_store.create_c...  <-- BLOCKER
  d=1   L 716  T=0 F=752  T=0 F=0  table_index == 1 && font->num_coords ? var_store.create_c...  <-- BLOCKER

[off-chain: 70 additional divergent branches across 26 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=08ad1f811c5d8829, size=179 bytes, fuzzer=minimizer, trial=1, discovered_at=2318s, mutation_op=ByteInterestingMutator,ByteFlipMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 01 46 20 20 20 28 f6 6b 65 72 6e   ......F   (.kern
  0010: 00 00 00 01 00 00 00 10 00 7f 00 03 00 00 00 00   ................
  0020: 00 01 00 00 00 10 00 7f 00 03 00 00 10 00 7f 00   ................
  0030: 00 4a 92 24 09 20 02 40 00 01 01 00 16 01 2c 10   .J.$. .@......,.
Seed 2 (id=002c9ad92acce91b, size=171 bytes, fuzzer=cmplog, trial=1, discovered_at=2579s, mutation_op=BytesInsertMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 01 20 19 21 20 20 20 47 50 4f 53   ...... .!   GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 50 4f 00 00   ...........GPO..
  0020: 10 00 01 01 04 53 00 01 00 0d 00 14 01 ff fb 13   .....S..........
  0030: 72 f9 f0 01 4f 53 03 03 00 04 00 1a 43 22 55 41   r...OS......C"UA
Seed 3 (id=0130d32717d6abb0, size=141 bytes, fuzzer=minimizer, trial=1, discovered_at=2656s, mutation_op=BytesDeleteMutator,ByteInterestingMutator,BytesInsertCopyMutator,WordInterestingMutator):
  0000: 00 01 00 00 00 01 46 20 20 20 28 f6 6b 65 72 6e   ......F   (.kern
  0010: 00 00 00 01 00 00 00 10 00 01 00 0f 01 00 20 92   .............. .
  0020: 92 2c 00 00 00 00 ff 07 00 00 00 03 6e 6e 6e 6e   .,..........nnnn
  0030: 6e 6e 04 67 74 32 32 32 10 00 00 20 20 00 00 b0   nn.gt222...  ...
Seed 4 (id=003bfa8ebe690138, size=144 bytes, fuzzer=cmplog, trial=1, discovered_at=2770s, mutation_op=BytesInsertCopyMutator,TokenReplace,WordInterestingMutator,TokenInsert):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 03 01 0c 00   ...........G....
  0020: 00 00 00 07 4f 00 00 10 ff 7a 68 2d 68 61 6e 74   ....O....zh-hant
  0030: 00 00 00 02 00 44 00 10 00 ff ff ff 3f 0d 02 00   .....D......?...
Seed 5 (id=0354073023471a2a, size=152 bytes, fuzzer=minimizer, trial=1, discovered_at=2960s, mutation_op=DwordInterestingMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 01 46 20 20 20 28 f6 6b 65 72 6e   ......F   (.kern
  0010: 00 00 00 01 00 00 00 10 00 01 00 0f 01 00 20 92   .............. .
  0020: 92 2c 00 00 00 00 ff 07 00 00 00 03 6e 6e 6e 6e   .,..........nnnn
  0030: 6e ff 07 00 00 00 03 6e 6e 6e 6e 6e 6e 04 67 74   n......nnnnnn.gt

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003817559785f774, size=6 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteDecMutator,WordAddMutator):
  0000: 87 0e 0d 0e 22 0e                                 ....".
Seed 2 (id=002edec370c771cf, size=35 bytes, fuzzer=naive, trial=1, discovered_at=47s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteNegMutator,TokenInsert,ByteIncMutator,ByteRandMutator):
  0000: 00 00 00 00 00 00 00 00 00 00 00 00 20 00 64 6f   ............ .do
  0010: 2d 68 0a 6f 74 00 0e 00 20 00 0c 00 0c 09 00 00   -h.ot... .......
  0020: 00 0c 00                                          ...
Seed 3 (id=0016e7ecc5a956f6, size=64 bytes, fuzzer=naive, trial=1, discovered_at=308s, mutation_op=BytesRandInsertMutator,ByteRandMutator):
  0000: 00 75 fe 2d 68 67 68 77 72 75 75 75 80 17 00 00   .u.-hghwruuu....
  0010: 00 20 00 00 23 91 01 9f 9f 9f 9f f3 00 00 00 00   . ..#...........
  0020: 00 00 02 02 02 02 02 02 02 02 00 00 00 00 00 00   ................
  0030: fe fc fe ff 01 20 00 00 00 00 10 00 00 a7 00 00   ..... ..........
Seed 4 (id=0002ee9aae2b9bef, size=54 bytes, fuzzer=naive, trial=1, discovered_at=470s, mutation_op=WordInterestingMutator,TokenInsert,BytesExpandMutator,ByteInterestingMutator):
  0000: 00 ff 00 00 1d 20 00 00 c8 0a 01 00 70 78 2d 68   ..... ......px-h
  0010: 61 6e 74 2d 68 6b 00 74 40 01 00 00 00 20 01 00   ant-hk.t@.... ..
  0020: c8 0a 01 00 40 62 91 6d 00 00 00 20 01 00 c8 7f   ....@b.m... ....
  0030: 01 00 40 62 91 6d                                 ..@b.m
Seed 5 (id=0030c881e05b69bb, size=56 bytes, fuzzer=naive, trial=1, discovered_at=4302s, mutation_op=BytesExpandMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesDeleteMutator,WordAddMutator,ByteIncMutator):
  0000: 6d 6d 6e 2d 68 61 6e 74 00 19 19 6d 01 00 9a 19   mmn-hant...m....
  0010: 00 73 6e 2d 68 61 6e 74 00 19 90 76 6c 67 70 90   .sn-hant...vlgp.
  0020: 6e 74 61 6c 90 00 a6 06 65 65 6d 00 3c 0b 00 00   ntal....eem.<...
  0030: 00 19 00 00 52 06 00 00                           ....R...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x40                            00(.)x3 05(.)x2 87(.)x1 6d(m)x1 +3u  PARTIAL
   0x0001  01(.)x40                            00(.)x2 07(.)x2 0e(.)x1 75(u)x1 +4u  DIFFER
   0x0002  00(.)x40                            00(.)x5 0d(.)x1 fe(.)x1 6e(n)x1 +2u  PARTIAL
   0x0003  00(.)x40                            00(.)x5 2d(-)x2 0e(.)x1 cb(.)x1 +1u  PARTIAL
   0x0004  00(.)x40                            00(.)x2 68(h)x2 70(p)x2 22(")x1 +3u  PARTIAL
   0x0005  01(.)x29 04(.)x10 03(.)x1           0e(.)x1 00(.)x1 67(g)x1 20( )x1 +6u  PARTIAL
   0x000c  6b(k)x30 47(G)x10                   20( )x1 80(.)x1 70(p)x1 01(.)x1 +5u  DIFFER
   0x000d  65(e)x30 50(P)x10                   00(.)x3 17(.)x1 78(x)x1 3f(?)x1 +3u  DIFFER
   0x000e  72(r)x30 4f(O)x10                   00(.)x2 64(d)x1 2d(-)x1 9a(.)x1 +4u  DIFFER
   0x000f  6e(n)x28 53(S)x10 78(x)x2           00(.)x2 6f(o)x1 68(h)x1 19(.)x1 +4u  DIFFER
   0x0012  00(.)x21 20( )x15 30(0)x3 df(.)x1   00(.)x4 0a(.)x1 74(t)x1 6e(n)x1 +2u  PARTIAL
   0x0014  00(.)x40                            68(h)x3 74(t)x1 23(#)x1 18(.)x1 +3u  PARTIAL
   0x0015  00(.)x40                            00(.)x3 91(.)x1 6b(k)x1 61(a)x1 +3u  PARTIAL
   0x0016  00(.)x40                            00(.)x4 0e(.)x1 01(.)x1 6e(n)x1 +2u  PARTIAL
   0x0017  10(.)x20 35(5)x12 1a(.)x8           00(.)x2 74(t)x2 9f(.)x1 ff(.)x1 +3u  DIFFER
   0x0018  00(.)x26 35(5)x9 02(.)x4 20( )x1    20( )x2 00(.)x2 9f(.)x1 40(@)x1 +3u  PARTIAL
   0x002a  00(.)x23 7f(.)x3 02(.)x2 10(.)x2 +9u  00(.)x3 6d(m)x1 5b([)x1 57(W)x1     PARTIAL
   0x0033  00(.)x14 66(f)x5 77(w)x4 01(.)x3 +10u  ff(.)x2 00(.)x2 62(b)x1 b6(.)x1     PARTIAL
   0x0036  00(.)x18 01(.)x11 03(.)x2 b5(.)x2 +6u  00(.)x2 ff(.)x1 57(W)x1 01(.)x1     PARTIAL
   0x0037  00(.)x19 04(.)x5 10(.)x3 b4(.)x2 +9u  00(.)x3 ff(.)x1 57(W)x1             PARTIAL
   0x0038  00(.)x15 0a(.)x5 69(i)x5 01(.)x5 +7u  00(.)x1 ff(.)x1 57(W)x1 88(.)x1     PARTIAL
   0x0039  00(.)x21 01(.)x5 b4(.)x2 06(.)x2 +9u  00(.)x1 ff(.)x1 05(.)x1 1f(.)x1     PARTIAL
   0x003a  00(.)x23 01(.)x3 03(.)x3 b4(.)x2 +8u  10(.)x1 cb(.)x1 00(.)x1 01(.)x1     PARTIAL
   0x003b  00(.)x23 20( )x3 b4(.)x2 10(.)x2 +9u  00(.)x2 0c(.)x1                     PARTIAL
   0x003c  00(.)x14 01(.)x7 14(.)x5 20( )x3 +9u  00(.)x1 0c(.)x1 bb(.)x1             PARTIAL
   0x003d  00(.)x20 01(.)x3 b4(.)x2 10(.)x2 +11u  a7(.)x1 00(.)x1 14(.)x1             PARTIAL
   0x003e  00(.)x18 01(.)x5 b4(.)x2 fe(.)x2 +13u  00(.)x2 01(.)x1                     PARTIAL
   0x003f  00(.)x16 10(.)x4 ff(.)x3 b4(.)x2 +13u  00(.)x1 ff(.)x1                     PARTIAL
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

--- minimizer ---
**Instrumentation**: naive's edge counters only.

**Feedback**: naive's edge-bucket `MaxMapFeedback`, plus a
`CalibrationStage` that measures each new corpus entry's execution
time, edge-map fill, and stability into `SchedulerMetadata`/testcase
metadata.

**Mutators / stages**: havoc + token mutator (`LineageMutator`, names
captured) run inside a `StdPowerMutationalStage` rather than naive's
plain `StdMutationalStage`. Stages are `[calibration, power]`. The
power stage derives the number of havoc mutations per seed visit (the
"energy") from a calibration-based `perf_score` — faster, smaller,
more-stable seeds earn more mutations. PowerSchedule is `None`, so the
energy uses ONLY intrinsic calibration and is NOT weighted by how often
a region has been hit. Corpus selection is plain FIFO `QueueScheduler`
(same order as naive).

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge, plus a one-time
calibration burst per new corpus entry.

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
  prompts_b/harfbuzz_5517.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5517,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile>naive (value_profile), naive_ctx>naive (ctx_coverage), minimizer>naive (calibrated_energy)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5517 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5517 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5517 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).