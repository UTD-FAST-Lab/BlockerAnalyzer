==== BLOCKER ====
Target: harfbuzz
Branch ID: 5232
Location: /src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:794:5
Enclosing function: OT::GDEF::get_var_store() const
Source line:     default: return Null(VariationStore);
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.90h  loser=24.00h
  avg hitcount on branch: winner=432  loser=0
  prob_div=1.00  dur_div=22.10h  hit_div=432
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=2.60h  loser=24.00h
  avg hitcount on branch: winner=841  loser=0
  prob_div=1.00  dur_div=21.40h  hit_div=841
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5232/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::GDEF::get_var_store() const (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:788-796) ---
[ ]   786    }
[ ]   787    const VariationStore &get_var_store () const
[B]   788    {
[B]   789      switch (u.version.major) {
[W]   790      case 1: return u.version.to_int () >= 0x00010003u ? this+u.version1.varStore : Null(VariationStore);
[ ]   791  #ifndef HB_NO_BEYOND_64K
[W]   792      case 2: return this+u.version2.varStore;
[ ]   793  #endif
[L]   794      default: return Null(VariationStore); <-- BLOCKER
[B]   795      }
[B]   796    }

--- Caller (1 hop): OT::hb_ot_apply_context_t::hb_ot_apply_context_t(unsigned int, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:704-724, calls OT::GDEF::get_var_store() const at line 713) (full body — short) ---
[B]   704  			table_index (table_index_),
[B]   705  			font (font_), face (font->face), buffer (buffer_),
[ ]   706  			gdef (
[ ]   707  #ifndef HB_NO_OT_LAYOUT
[B]   708  			      *face->table.GDEF->table
[ ]   709  #else
[ ]   710  			      Null (GDEF)
[ ]   711  #endif
[ ]   712  			     ),
[B]   713  			var_store (gdef.get_var_store ()), <-- CALL
[ ]   714  			var_store_cache (
[ ]   715  #ifndef HB_NO_VAR
[B]   716  					 table_index == 1 && font->num_coords ? var_store.create_cache () : nullptr
[ ]   717  #else
[ ]   718  					 nullptr
[ ]   719  #endif
[ ]   720  					),
[B]   721  			digest (buffer_->digest ()),
[B]   722  			direction (buffer_->props.direction),
[B]   723  			has_glyph_classes (gdef.has_glyph_classes ())
[B]   724    { init_iters (); }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::BASE::get_baseline(hb_font_t*, unsigned int, hb_direction_t, unsigned int, unsigned int, int*) const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:464-474, calls OT::GDEF::get_var_store() const at line 471)
hop 2  OT::BASE::get_min_max(hb_font_t*, hb_direction_t, unsigned int, unsigned int, unsigned int, int*, int*)  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:484-494, calls OT::GDEF::get_var_store() const at line 490)
hop 3  OT::BaseLangSysRecord::get_min_max() const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:271-271, calls OT::BASE::get_min_max(hb_font_t*, hb_direction_t, unsigned int, unsigned int, unsigned int, int*, int*) at line 271)
hop 3  OT::MinMax::get_min_max(unsigned int, OT::BaseCoord const**, OT::BaseCoord const**) const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:198-207, calls OT::BASE::get_min_max(hb_font_t*, hb_direction_t, unsigned int, unsigned int, unsigned int, int*, int*) at line 201)
hop 3  hb_ot_layout_get_baseline  (/src/harfbuzz/src/hb-ot-layout.cc:2122-2124, calls OT::BASE::get_baseline(hb_font_t*, unsigned int, hb_direction_t, unsigned int, unsigned int, int*) const at line 2123)
hop 4  OT::BaseScript::get_min_max(unsigned int) const  (/src/harfbuzz/src/hb-ot-layout-base-table.hh:292-295, calls OT::MinMax::get_min_max(unsigned int, OT::BaseCoord const**, OT::BaseCoord const**) const at line 294)
hop 4  hb_ot_layout_get_baseline_with_fallback  (/src/harfbuzz/src/hb-ot-layout.cc:2147-2346, calls hb_ot_layout_get_baseline at line 2148)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      65         0  OT::CaretValue::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:291-300)
      60         0  OT::GDEFVersion1_2<OT::Layout::SmallTypes>::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:577-586)
      60         0  OT::GDEFVersion1_2<OT::Layout::MediumTypes>::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:577-586)
      60         0  OT::GDEF::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:654-664)
      45         0  OT::AttachList::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:106-109)
      42         0  OT::LigGlyph::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:355-358)
      35         0  OT::LigCaretList::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:422-425)
      15         0  OT::MarkGlyphSets::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:507-514)
       4         0  OT::CaretValueFormat2::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:176-179)
       3         0  bool OT::GSUBGPOSVersion1_2<OT::Layout::SmallTypes>::sanitize<OT::Layout::GPOS_impl::PosLookup>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:4123-4137)
       3         0  bool OT::GSUBGPOSVersion1_2<OT::Layout::MediumTypes>::sanitize<OT::Layout::GPOS_impl::PosLookup>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:4123-4137)
       3         0  bool OT::GSUBGPOSVersion1_2<OT::Layout::SmallTypes>::sanitize<OT::Layout::GSUB_impl::SubstLookup>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:4123-4137)
       3         0  bool OT::GSUBGPOSVersion1_2<OT::Layout::MediumTypes>::sanitize<OT::Layout::GSUB_impl::SubstLookup>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:4123-4137)
       3         0  bool OT::GSUBGPOS::sanitize<OT::Layout::GPOS_impl::PosLookup>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:4212-4222)
       3         0  bool OT::GSUBGPOS::sanitize<OT::Layout::GSUB_impl::SubstLookup>(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-layout-gsubgpos.hh:4212-4222)
... (1 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::GDEF::get_var_store() const  (/src/harfbuzz/src/OT/Layout/GDEF/GDEF.hh:788-796) ---
  d=1   L 790  T=374 F=65  T=0 F=404  case 1: return u.version.to_int () >= 0x00010003u ? this+...
  d=1   L 790  T=132 F=242  T=0 F=0  case 1: return u.version.to_int () >= 0x00010003u ? this+...
  d=1   L 792  T=65 F=374  T=0 F=404  case 2: return this+u.version2.varStore;
  d=1   L 794  T=0 F=439  T=404 F=0  default: return Null(VariationStore);  <-- BLOCKER

[off-chain: 32 additional divergent branches across 11 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=12be95fb2b9448de, size=32 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=330s, mutation_op=CrossoverReplaceMutator,TokenReplace,BytesInsertCopyMutator,DwordInterestingMutator,BytesSetMutator,BitFlipMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 26 20 47 44 45 46   ......    & GDEF
  0010: 7f 20 20 20 00 00 00 00 00 20 00 00 00 00 00 00   .   ..... ......
Seed 2 (id=13b375b9eff5c760, size=36 bytes, fuzzer=cmplog, trial=1, discovered_at=683s, mutation_op=BytesExpandMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 44 45 46   ......      GDEF
  0010: 00 01 00 80 00 00 00 10 00 00 10 00 00 02 0d 00   ................
  0020: 00 01 01 00                                       ....
Seed 3 (id=0aae61433abcfb1c, size=89 bytes, fuzzer=cmplog, trial=1, discovered_at=1038s, mutation_op=DwordAddMutator,ByteAddMutator,TokenInsert,TokenReplace):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 44 45 46   ......      GDEF
  0010: 00 02 00 80 00 00 00 10 ff fe 02 f7 00 01 01 82   ................
  0020: 82 a5 82 82 82 ff fe 03 01 06 01 01 82 ef 01 0e   ................
  0030: 00 75 6e 69 73 63 72 69 62 65 2d 62 75 67 2d 63   .uniscribe-bug-c
Seed 4 (id=0641331eeb9db3a8, size=108 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1157s, mutation_op=BytesSetMutator,BytesDeleteMutator,BytesInsertMutator,BytesInsertMutator,BytesInsertMutator,ByteInterestingMutator):
  0000: 00 01 00 00 00 01 20 20 20 19 20 20 47 44 45 46   ......   .  GDEF
  0010: 20 e0 20 20 00 00 00 18 00 01 00 00 00 00 00 20    .  ........... 
  0020: 20 20 20 00 00 cd 20 20 20 20 20 20 20 cc 00 20      ...       .. 
  0030: 20 20 20 00 00 00 00 00 00 00 00 00 00 00 00 00      .............
Seed 5 (id=13b0bdc01cdb2c60, size=198 bytes, fuzzer=cmplog, trial=1, discovered_at=1328s, mutation_op=BytesInsertMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 44 45 46   ......      GDEF
  0010: 00 01 00 02 00 00 00 10 00 1b 00 00 01 01 01 00   ................
  0020: 02 00 00 20 04 10 00 00 12 00 02 ff 00 00 17 00   ... ............
  0030: 00 18 00 00 00 04 20 02 00 04 00 2e 20 01 00 ff   ...... ..... ...

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=003817559785f774, size=6 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteDecMutator,WordAddMutator):
  0000: 87 0e 0d 0e 22 0e                                 ....".
Seed 2 (id=00546490999c9c0b, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=13s, mutation_op=DwordAddMutator,BytesDeleteMutator,ByteInterestingMutator,TokenInsert,BytesCopyMutator,ByteNegMutator):
  0000: fe ff ff ff f4 01 e0 e0 20 00 00 00 01 20 e0 6a   ........ .... .j
  0010: 79 2d 68 61 6e 74 2d 68 6b 00 20 00 00 00 ff 01   y-hant-hk. .....
  0020: 00 07 00 00 01 20 20 20 01 5b 00 00 00 e0 20 00   .....   .[.... .
  0030: 00 00 01 20 ff 09 fd 20 ff                        ... ... .
Seed 3 (id=002edec370c771cf, size=35 bytes, fuzzer=naive, trial=1, discovered_at=47s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteNegMutator,TokenInsert,ByteIncMutator,ByteRandMutator):
  0000: 00 00 00 00 00 00 00 00 00 00 00 00 20 00 64 6f   ............ .do
  0010: 2d 68 0a 6f 74 00 0e 00 20 00 0c 00 0c 09 00 00   -h.ot... .......
  0020: 00 0c 00                                          ...
Seed 4 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 5 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x19 4f(O)x1                    00(.)x4 e0(.)x2 05(.)x2 87(.)x1 +11u  PARTIAL
   0x0001  01(.)x19 54(T)x1                    00(.)x3 0e(.)x2 ff(.)x2 07(.)x2 +11u  PARTIAL
   0x0002  00(.)x19 54(T)x1                    00(.)x10 ff(.)x3 0d(.)x1 0e(.)x1 +5u  PARTIAL
   0x0003  00(.)x19 4f(O)x1                    00(.)x11 ff(.)x2 2d(-)x2 0e(.)x1 +4u  PARTIAL
   0x0004  00(.)x20                            00(.)x2 df(.)x2 68(h)x2 70(p)x2 +12u  PARTIAL
   0x0005  01(.)x18 02(.)x1 04(.)x1            00(.)x4 20( )x4 0e(.)x3 06(.)x2 +7u  PARTIAL
   0x0006  20( )x18 ff(.)x1 ee(.)x1            00(.)x12 e0(.)x1 68(h)x1 e5(.)x1 +4u  PARTIAL
   0x0008  20( )x17 00(.)x1 01(.)x1 04(.)x1    00(.)x4 20( )x2 29())x1 e0(.)x1 +11u  PARTIAL
   0x000a  20( )x16 00(.)x2 26(&)x1 10(.)x1    00(.)x9 01(.)x2 29())x1 aa(.)x1 +6u  PARTIAL
   0x000b  20( )x18 26(&)x1 00(.)x1            00(.)x12 29())x1 13(.)x1 75(u)x1 +4u  PARTIAL
   0x000c  47(G)x20                            00(.)x3 01(.)x2 20( )x2 2c(,)x1 +11u  DIFFER
   0x000d  44(D)x20                            20( )x4 00(.)x4 18(.)x1 17(.)x1 +8u  DIFFER
   0x000e  45(E)x20                            00(.)x5 e0(.)x1 64(d)x1 18(.)x1 +10u  DIFFER
   0x000f  46(F)x20                            00(.)x5 6a(j)x1 6f(o)x1 fa(.)x1 +10u  DIFFER
   0x0014  00(.)x20                            68(h)x3 00(.)x2 6e(n)x1 74(t)x1 +11u  PARTIAL
   0x0015  00(.)x20                            00(.)x4 06(.)x2 74(t)x1 17(.)x1 +10u  PARTIAL
   0x0016  00(.)x20                            00(.)x8 01(.)x2 2d(-)x1 0e(.)x1 +6u  PARTIAL
   0x0017  10(.)x9 18(.)x8 00(.)x2 2e(.)x1     00(.)x7 74(t)x2 68(h)x1 3d(=)x1 +6u  PARTIAL
   0x0018  00(.)x17 ff(.)x3                    20( )x4 00(.)x3 6b(k)x1 61(a)x1 +8u  PARTIAL
   0x001c  00(.)x12 01(.)x6 47(G)x1 ff(.)x1    00(.)x6 0c(.)x1 3d(=)x1 4c(L)x1 +7u  PARTIAL
   0x003e  00(.)x9 69(i)x2 2d(-)x1 20( )x1 +3u  00(.)x4 9f(.)x1 20( )x1 01(.)x1     PARTIAL
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
  prompts_b/harfbuzz_5232.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5232,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5232 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5232 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5232 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).