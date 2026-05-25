==== BLOCKER ====
Target: harfbuzz
Branch ID: 9067
Location: /src/harfbuzz/src/hb-ot-layout-common.hh:2002:5
Enclosing function: OT::ClassDef::get_class(unsigned int) const
Source line:     default:return 0;
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           6        4          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 20  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=2.80h  loser=12.00h
  avg hitcount on branch: winner=271  loser=0
  prob_div=1.00  dur_div=9.20h  hit_div=271
  subject-level: delta_AUC=12333210.0  p_AUC=0.0002  delta_Final=1452.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/9067/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::ClassDef::get_class(unsigned int) const (/src/harfbuzz/src/hb-ot-layout-common.hh:1994-2004) ---
[ ]  1992    unsigned int get (hb_codepoint_t k) const { return get_class (k); }
[ ]  1993    unsigned int get_class (hb_codepoint_t glyph_id) const
[B]  1994    {
[B]  1995      switch (u.format) {
[W]  1996      case 1: return u.format1.get_class (glyph_id);
[W]  1997      case 2: return u.format2.get_class (glyph_id);
[ ]  1998  #ifndef HB_NO_BEYOND_64K
[W]  1999      case 3: return u.format3.get_class (glyph_id);
[W]  2000      case 4: return u.format4.get_class (glyph_id);
[ ]  2001  #endif
[L]  2002      default:return 0; <-- BLOCKER
[B]  2003      }
[B]  2004    }

--- Caller (1 hop): OT::GDEF::get_glyph_class(unsigned int) const (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:801-801, calls OT::ClassDef::get_class(unsigned int) const at line 801) (full body — short) ---
[B]   801    { return get_glyph_class_def ().get_class (glyph); } <-- CALL

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  AAT::ClassTable<OT::IntType<unsigned char, 1u> >::get_class(unsigned int, unsigned int, unsigned int) const  (/src/harfbuzz/src/hb-aat-layout-common.hh:682-684, calls OT::ClassDef::get_class(unsigned int) const at line 683)
hop 2  AAT::StateTable<AAT::ExtendedTypes, void>::get_class(unsigned int, unsigned int) const  (/src/harfbuzz/src/hb-aat-layout-common.hh:532-535, calls OT::ClassDef::get_class(unsigned int) const at line 534)
hop 3  void AAT::StateTableDriver<AAT::ExtendedTypes, void>::drive<AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t>(AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t*, AAT::hb_aat_apply_context_t*)  (/src/harfbuzz/src/hb-aat-layout-common.hh:782-905, calls AAT::StateTable<AAT::ExtendedTypes, void>::get_class(unsigned int, unsigned int) const at line 818)
hop 4  AAT::ContextualSubtable<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:322-331, calls void AAT::StateTableDriver<AAT::ExtendedTypes, void>::drive<AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t>(AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t*, AAT::hb_aat_apply_context_t*) at line 328)
hop 4  AAT::RearrangementSubtable<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:166-175, calls void AAT::StateTableDriver<AAT::ExtendedTypes, void>::drive<AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t>(AAT::RearrangementSubtable<AAT::ExtendedTypes>::driver_context_t*, AAT::hb_aat_apply_context_t*) at line 172)
hop 5  AAT::Chain<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:1017-1085, calls AAT::RearrangementSubtable<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const at line 1072)
hop 5  AAT::mortmorx<AAT::ExtendedTypes, 1836020344u>::apply(AAT::hb_aat_apply_context_t*, hb_aat_map_t const&) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:1156-1171, calls AAT::RearrangementSubtable<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const at line 1167)
hop 6  bool AAT::hb_aat_apply_context_t::dispatch<AAT::RearrangementSubtable<AAT::ExtendedTypes> >(AAT::RearrangementSubtable<AAT::ExtendedTypes> const&)  (/src/harfbuzz/src/hb-aat-layout-common.hh:50-50, calls AAT::Chain<AAT::ExtendedTypes>::apply(AAT::hb_aat_apply_context_t*) const at line 50)
hop 7  hb_subset_context_t::return_t OT::AxisValue::dispatch<hb_subset_context_t, hb_array_t<OT::StatAxisRecord const> const&>(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const> const&) const  (/src/harfbuzz/src/hb-ot-stat-table.hh:392-402, calls bool AAT::hb_aat_apply_context_t::dispatch<AAT::RearrangementSubtable<AAT::ExtendedTypes> >(AAT::RearrangementSubtable<AAT::ExtendedTypes> const&) at line 396)
hop 8  hb_sanitize_context_t::return_t AAT::ChainSubtable<AAT::ExtendedTypes>::dispatch<hb_sanitize_context_t>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:924-935, calls hb_subset_context_t::return_t OT::AxisValue::dispatch<hb_subset_context_t, hb_array_t<OT::StatAxisRecord const> const&>(hb_subset_context_t*, hb_array_t<OT::StatAxisRecord const> const&) const at line 928)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0      2390  OT::hb_intersects_context_t::return_t OT::ChainContext::dispatch<OT::hb_intersects_context_t>(OT::hb_intersects_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  OT::hb_ot_apply_context_t::return_t OT::ChainContext::dispatch<OT::hb_ot_apply_context_t>(OT::hb_ot_apply_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  OT::hb_collect_glyphs_context_t::return_t OT::ChainContext::dispatch<OT::hb_collect_glyphs_context_t>(OT::hb_collect_glyphs_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  OT::hb_closure_lookups_context_t::return_t OT::ChainContext::dispatch<OT::hb_closure_lookups_context_t>(OT::hb_closure_lookups_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  hb_subset_context_t::return_t OT::ChainContext::dispatch<hb_subset_context_t>(hb_subset_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  hb_sanitize_context_t::return_t OT::ChainContext::dispatch<hb_sanitize_context_t>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  OT::hb_collect_variation_indices_context_t::return_t OT::ChainContext::dispatch<OT::hb_collect_variation_indices_context_t>(OT::hb_collect_variation_indices_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  OT::hb_accelerate_subtables_context_t::return_t OT::ChainContext::dispatch<OT::hb_accelerate_subtables_context_t>(OT::hb_accelerate_subtables_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  OT::hb_have_non_1to1_context_t::return_t OT::ChainContext::dispatch<OT::hb_have_non_1to1_context_t>(OT::hb_have_non_1to1_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  OT::hb_closure_context_t::return_t OT::ChainContext::dispatch<OT::hb_closure_context_t>(OT::hb_closure_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  OT::hb_would_apply_context_t::return_t OT::ChainContext::dispatch<OT::hb_would_apply_context_t>(OT::hb_would_apply_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  hb_get_glyph_alternates_dispatch_t::return_t OT::ChainContext::dispatch<hb_get_glyph_alternates_dispatch_t, unsigned int&, unsigned int&, unsigned int*&, unsigned int*&>(hb_get_glyph_alternates_dispatch_t*, unsigned int&, unsigned int&, unsigned int*&, unsigned int*&) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2390  hb_position_single_dispatch_t::return_t OT::ChainContext::dispatch<hb_position_single_dispatch_t, hb_font_t*&, hb_direction_t&, unsigned int&, hb_glyph_position_t&>(hb_position_single_dispatch_t*, hb_font_t*&, hb_direction_t&, unsigned int&, hb_glyph_position_t&) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:3874-3887)
       0      2360  OT::ArrayOf<OT::OffsetTo<OT::Layout::GPOS_impl::PosLookupSubTable, OT::IntType<unsigned short, 2u>, true>, OT::IntType<unsigned short, 2u> > const& OT::Lookup::get_subtables<OT::Layout::GPOS_impl::PosLookupSubTable>() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1257-1257)
       0      2360  OT::ArrayOf<OT::OffsetTo<OT::Layout::GSUB_impl::SubstLookupSubTable, OT::IntType<unsigned short, 2u>, true>, OT::IntType<unsigned short, 2u> > const& OT::Lookup::get_subtables<OT::Layout::GSUB_impl::SubstLookupSubTable>() const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1257-1257)
... (167 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::ClassDef::get_class(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-common.hh:1994-2004) ---
  d=1   L1996  T=54 F=486  T=0 F=540  case 1: return u.format1.get_class (glyph_id);
  d=1   L1997  T=162 F=378  T=0 F=540  case 2: return u.format2.get_class (glyph_id);
  d=1   L1999  T=54 F=486  T=0 F=540  case 3: return u.format3.get_class (glyph_id);
  d=1   L2000  T=270 F=270  T=0 F=540  case 4: return u.format4.get_class (glyph_id);
  d=1   L2002  T=0 F=540  T=540 F=0  default:return 0;  <-- BLOCKER

[off-chain: 84 additional divergent branches across 29 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=a06f81d76c9bb1af, size=192 bytes, fuzzer=cmplog, trial=4, discovered_at=2021s, mutation_op=BytesInsertCopyMutator,ByteAddMutator,ByteDecMutator,ByteFlipMutator,BytesInsertMutator):
  0000: 00 01 00 00 00 02 80 00 00 00 22 10 01 01 00 00   ..........".....
  0010: 20 00 00 00 20 02 4f 54 54 02 00 00 47 44 45 46    ... .OTT...GDEF
  0020: fd 02 00 ff 00 00 00 04 00 00 10 01 01 00 00 02   ................
  0030: fe 00 00 00 10 01 ff ff 00 10 54 20 67 68 70 72   ..........T ghpr
Seed 2 (id=bbb929962f66e583, size=182 bytes, fuzzer=cmplog, trial=4, discovered_at=2021s, mutation_op=DwordInterestingMutator,BytesDeleteMutator,BytesDeleteMutator,ByteDecMutator,ByteIncMutator,BytesRandInsertMutator,CrossoverInsertMutator):
  0000: 00 01 00 00 00 02 80 0d 00 00 22 10 01 01 01 00   ..........".....
  0010: 20 00 00 00 20 02 4f 54 54 02 00 00 47 44 45 46    ... .OTT...GDEF
  0020: fd 02 00 ff 00 00 00 04 00 00 10 06 ff ff ff ff   ................
  0030: fe 02 00 00 10 01 ff ff 00 10 54 20 67 68 70 72   ..........T ghpr
Seed 3 (id=b742349b93ef260d, size=278 bytes, fuzzer=cmplog, trial=4, discovered_at=2029s, mutation_op=BytesRandSetMutator):
  0000: 00 01 00 00 00 05 00 01 04 00 00 04 00 00 00 3e   ...............>
  0010: 3e 3e 6a 00 7f 00 10 2e 00 f7 16 88 47 44 45 46   >>j.........GDEF
  0020: 02 fd 02 05 00 00 00 06 00 e2 ff 0d 00 00 2b 00   ..............+.
  0030: 10 01 00 0b 25 26 20 e0 20 20 70 78 66 65 61 74   ....%& .  pxfeat
Seed 4 (id=3c0e8380231588f6, size=311 bytes, fuzzer=cmplog, trial=4, discovered_at=2096s, mutation_op=BytesRandInsertMutator,DwordAddMutator,ByteNegMutator,BytesRandInsertMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 05 00 01 04 00 00 04 00 00 00 3e   ...............>
  0010: 3e 3e 6a 00 7f 00 10 2e 00 f7 16 88 47 44 45 46   >>j.........GDEF
  0020: 02 fd 02 05 00 00 00 06 00 e2 ff 0d 00 00 2b 00   ..............+.
  0030: 10 01 00 0b 25 26 20 e0 20 20 70 78 66 65 73 73   ....%& .  pxfess
Seed 5 (id=553d707e5364c814, size=899 bytes, fuzzer=cmplog, trial=4, discovered_at=2596s, mutation_op=WordInterestingMutator,BytesInsertMutator,ByteAddMutator):
  0000: 00 01 00 00 00 02 00 00 00 04 00 01 00 03 00 02   ................
  0010: 00 00 01 01 01 01 01 ca 00 f7 16 88 47 44 45 46   ............GDEF
  0020: 02 02 04 06 00 00 00 0a 00 d5 00 01 01 01 01 e9   ................
  0030: e9 e9 e9 e9 e9 e9 e9 e9 e9 e9 e9 e9 00 01 01 01   ................

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0007f1b8131011ce, size=59 bytes, fuzzer=cmplog, trial=1, discovered_at=17s, mutation_op=BytesDeleteMutator,BytesRandInsertMutator,DwordAddMutator,BytesInsertMutator,BytesInsertCopyMutator):
  0000: 01 00 00 00 00 20 20 20 20 06 00 00 00 00 00 00   .....    .......
  0010: 20 20 20 20 06 00 00 00 20 20 20 60 20 20 6b 65       ....   `  ke
  0020: 72 6e 00 64 20 20 00 00 22 ff ff ff 00 00 01 00   rn.d  ..".......
  0030: 00 20 00 00 00 00 00 00 ff 02 00                  . .........
Seed 2 (id=000805815c50d718, size=52 bytes, fuzzer=cmplog, trial=1, discovered_at=1096s, mutation_op=ByteNegMutator,ByteIncMutator):
  0000: b9 17 00 01 9c 1f 10 0f 10 00 00 00 e0 1c 00 00   ................
  0010: c5 17 17 00 e0 1c 00 00 c5 17 06 00 e0 06 00 00   ................
  0020: ce 20 00 00 e0 1c 00 00 c5 17 02 00 e0 1c 00 00   . ..............
  0030: c4 17 00 00                                       ....
Seed 3 (id=0009a8dcb2f65ed7, size=307 bytes, fuzzer=cmplog, trial=1, discovered_at=3908s, mutation_op=CrossoverInsertMutator,BytesDeleteMutator,BytesExpandMutator,WordInterestingMutator,BytesRandInsertMutator,DwordInterestingMutator):
  0000: 00 01 00 00 00 04 20 00 00 7f 00 20 20 20 56 56   ...... ....   VV
  0010: 41 51 b9 b9 b9 00 ff ff fe f2 1a 20 47 53 55 42   AQ......... GSUB
  0020: 02 00 03 20 00 00 00 00 ff ff 00 ff ff ff 03 00   ... ............
  0030: 00 00 02 00 00 78 78 78 78 78 78 78 78 78 20 17   .....xxxxxxxxx .
Seed 4 (id=00039e3b8e4285f5, size=281 bytes, fuzzer=cmplog, trial=1, discovered_at=5631s, mutation_op=ByteAddMutator,DwordAddMutator,WordInterestingMutator,BytesRandInsertMutator,TokenReplace,ByteDecMutator,BytesCopyMutator):
  0000: 00 01 00 00 00 04 20 03 00 7f 00 ff ff ff 03 56   ...... ........V
  0010: 41 51 b9 b9 b9 01 ff ff fe f2 1a 20 47 50 4f 53   AQ......... GPOS
  0020: 00 00 03 20 00 00 00 00 ff ff ff 10 00 00 00 80   ... ............
  0030: 04 00 6d 6e 2d 68 61 6e 74 2d 68 6b 00 78 78 78   ..mn-hant-hk.xxx
Seed 5 (id=00035b3a3e1b7ab0, size=749 bytes, fuzzer=cmplog, trial=1, discovered_at=5939s, mutation_op=CrossoverInsertMutator,ByteAddMutator,ByteNegMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 04 20 06 00 7f 00 20 20 20 56 56   ...... ....   VV
  0010: 41 51 b9 b9 b9 00 ff ff fe f2 1a 20 47 50 4f 53   AQ......... GPOS
  0020: 00 00 03 20 00 00 00 00 20 fe 00 10 00 00 00 00   ... .... .......
  0030: 00 00 00 00 00 78 78 78 78 78 00 00 00 51 51 78   .....xxxxx...QQx


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x10                            00(.)x8 01(.)x1 b9(.)x1             PARTIAL
   0x0001  01(.)x10                            01(.)x8 00(.)x1 17(.)x1             PARTIAL
   0x0003  00(.)x10                            00(.)x9 01(.)x1                     PARTIAL
   0x0004  00(.)x10                            00(.)x9 9c(.)x1                     PARTIAL
   0x0005  02(.)x8 05(.)x2                     04(.)x8 20( )x1 1f(.)x1             DIFFER
   0x0006  00(.)x7 80(.)x3                     20( )x6 10(.)x1 1f(.)x1 1b(.)x1 +1u  DIFFER
   0x0007  00(.)x7 01(.)x2 0d(.)x1             06(.)x3 00(.)x2 03(.)x2 20( )x1 +2u  PARTIAL
   0x0008  00(.)x8 04(.)x2                     00(.)x8 20( )x1 10(.)x1             PARTIAL
   0x0009  00(.)x6 04(.)x4                     7f(.)x8 06(.)x1 00(.)x1             PARTIAL
   0x000a  00(.)x7 22(")x3                     00(.)x10                            PARTIAL
   0x000b  01(.)x5 10(.)x3 04(.)x2             20( )x6 00(.)x2 ff(.)x2             DIFFER
   0x000c  00(.)x7 01(.)x3                     20( )x6 ff(.)x2 00(.)x1 e0(.)x1     PARTIAL
   0x000d  01(.)x3 03(.)x3 00(.)x2 02(.)x2     20( )x6 ff(.)x2 00(.)x1 1c(.)x1     PARTIAL
   0x000e  00(.)x7 01(.)x3                     56(V)x6 00(.)x2 03(.)x2             PARTIAL
   0x000f  00(.)x5 02(.)x3 3e(>)x2             56(V)x8 00(.)x2                     PARTIAL
   0x0010  00(.)x5 20( )x2 3e(>)x2 1f(.)x1     41(A)x8 20( )x1 c5(.)x1             PARTIAL
   0x0011  00(.)x7 3e(>)x2 f2(.)x1             51(Q)x6 20( )x1 17(.)x1 ff(.)x1 +1u  DIFFER
   0x0012  01(.)x5 00(.)x3 6a(j)x2             b9(.)x7 20( )x1 17(.)x1 5f(_)x1     DIFFER
   0x0013  00(.)x5 01(.)x5                     b9(.)x8 20( )x1 00(.)x1             PARTIAL
   0x0014  01(.)x4 20( )x3 7f(.)x2 00(.)x1     b9(.)x8 06(.)x1 e0(.)x1             DIFFER
   0x0015  01(.)x5 02(.)x3 00(.)x2             00(.)x7 01(.)x2 1c(.)x1             PARTIAL
   0x0016  01(.)x5 4f(O)x3 10(.)x2             ff(.)x7 00(.)x2 18(.)x1             DIFFER
   0x0017  ca(.)x5 54(T)x3 2e(.)x2             ff(.)x8 00(.)x2                     DIFFER
   0x0018  00(.)x7 54(T)x3                     fe(.)x8 20( )x1 c5(.)x1             DIFFER
   0x0019  f7(.)x7 02(.)x2 00(.)x1             f2(.)x8 20( )x1 17(.)x1             DIFFER
   0x001a  16(.)x7 00(.)x3                     1a(.)x8 20( )x1 06(.)x1             DIFFER
   0x001b  88(.)x7 00(.)x2 3f(?)x1             20( )x7 60(`)x1 00(.)x1 2b(+)x1     PARTIAL
   0x001c  47(G)x10                            47(G)x8 20( )x1 e0(.)x1             PARTIAL
   0x001d  44(D)x10                            50(P)x6 53(S)x2 20( )x1 06(.)x1     DIFFER
   0x001e  45(E)x10                            4f(O)x6 55(U)x2 6b(k)x1 00(.)x1     DIFFER
   0x001f  46(F)x10                            53(S)x6 42(B)x2 65(e)x1 00(.)x1     DIFFER
   0x0020  02(.)x7 fd(.)x3                     00(.)x5 02(.)x3 72(r)x1 ce(.)x1     PARTIAL
   0x0021  02(.)x8 fd(.)x2                     00(.)x7 6e(n)x1 20( )x1 03(.)x1     DIFFER
   0x0022  04(.)x5 00(.)x3 02(.)x2             03(.)x7 00(.)x3                     PARTIAL
   0x0023  06(.)x5 ff(.)x3 05(.)x2             20( )x7 64(d)x1 00(.)x1 13(.)x1     DIFFER
   0x0024  00(.)x10                            00(.)x8 20( )x1 e0(.)x1             PARTIAL
   0x0025  00(.)x10                            00(.)x8 20( )x1 1c(.)x1             PARTIAL
   0x0027  0a(.)x5 04(.)x3 06(.)x2             00(.)x10                            DIFFER
   0x0028  00(.)x10                            ff(.)x6 20( )x2 22(")x1 c5(.)x1     DIFFER
   0x0029  d5(.)x5 00(.)x3 e2(.)x2             ff(.)x8 17(.)x1 fe(.)x1             DIFFER
   ... (21 more divergent offsets)
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
  prompts/--BR/01_harfbuzz_9067.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9067,
  "target": "harfbuzz",
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
      // pick EXACTLY ONE of:
      //   "I2SRandReplace"     (cmplog / vpc input-to-state substitution)
      //   "CMP_MAP gradient"   (vp / vpc Hamming/prefix-distance feedback)
      //   "havoc-only"         (lucky havoc byte mutation, no CMP introspection)
      //   "token-replace"      (TokenInsert/TokenReplace dictionary mutations)
      //   "other"              (anything that does not fit the four above)
    "verified_in_lineage": true,
      // pick true or false
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9067 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9067 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9067 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).