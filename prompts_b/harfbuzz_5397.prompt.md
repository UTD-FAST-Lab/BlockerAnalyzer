==== BLOCKER ====
Target: harfbuzz
Branch ID: 5397
Location: /src/harfbuzz/src/hb-open-type.hh:541:30
Enclosing function: bool OT::UnsizedArrayOf<AAT::FeatureName>::sanitize<AAT::feat const*>(hb_sanitize_context_t*, unsigned int, AAT::feat const*&&) const
Source line:     for (unsigned int i = 0; i < count; i++)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        9          1  REFERENCE
cmplog                           3        0          7  REFERENCE
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         2        1          7  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.60h  loser=17.20h
  avg hitcount on branch: winner=16  loser=4
  prob_div=0.80  dur_div=16.60h  hit_div=12
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5397/{W,L}/branch_coverage_show.txt

--- Enclosing function: bool OT::UnsizedArrayOf<AAT::FeatureName>::sanitize<AAT::feat const*>(hb_sanitize_context_t*, unsigned int, AAT::feat const*&&) const (/src/harfbuzz/src/hb-open-type.hh:537-545) ---
[ ]   535    template <typename ...Ts>
[ ]   536    bool sanitize (hb_sanitize_context_t *c, unsigned int count, Ts&&... ds) const
[B]   537    {
[B]   538      TRACE_SANITIZE (this);
[B]   539      if (unlikely (!sanitize_shallow (c, count))) return_trace (false);
[B]   540      if (!sizeof... (Ts) && hb_is_trivially_copyable(Type)) return_trace (true);
[B]   541      for (unsigned int i = 0; i < count; i++) <-- BLOCKER
[W]   542        if (unlikely (!c->dispatch (arrayZ[i], std::forward<Ts> (ds)...)))
[W]   543  	return_trace (false);
[B]   544      return_trace (true);
[B]   545    }

--- Caller (1 hop): OT::ArrayOf<OT::IntType<unsigned short, 2u>, OT::IntType<unsigned short, 2u> >::sanitize_shallow(hb_sanitize_context_t*) const (/src/harfbuzz/src/hb-open-type.hh:737-740, calls bool OT::UnsizedArrayOf<AAT::FeatureName>::sanitize<AAT::feat const*>(hb_sanitize_context_t*, unsigned int, AAT::feat const*&&) const at line 739) (full body — short) ---
[W]   737    {
[W]   738      TRACE_SANITIZE (this);
[W]   739      return_trace (len.sanitize (c) && c->check_array (arrayZ, len)); <-- CALL
[W]   740    }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:90-102, calls bool OT::UnsizedArrayOf<AAT::FeatureName>::sanitize<AAT::feat const*>(hb_sanitize_context_t*, unsigned int, AAT::feat const*&&) const at line 97)
hop 3  CFF::CFF2VariationStore::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:117-120, calls CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const at line 119)
hop 3  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:398-475, calls CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const at line 416)
hop 4  OT::cff2::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:515-515, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 515)
hop 4  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::~accelerator_templ_t()  (/src/harfbuzz/src/hb-ot-cff2-table.hh:476-476, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 476)
hop 5  OT::cff2_accelerator_t::cff2_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:538-538, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 538)
hop 5  OT::hmtx_accelerator_t::hmtx_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:449-449, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 449)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     580         0  OT::TableRecord::cmp(OT::Tag) const  (/src/harfbuzz/src/hb-open-file.hh:56-56)
     580         0  _ZNK2OT7IntTypeItLj2EE3cmpIjTnPN12hb_enable_ifIXsr3std14is_convertibleIT_tEE5valueEvE4typeELPv0EEEiS4_  (/src/harfbuzz/src/hb-open-type.hh:101-104)
     580         0  _ZNK2OT7IntTypeIjLj3EE3cmpIjTnPN12hb_enable_ifIXsr3std14is_convertibleIT_jEE5valueEvE4typeELPv0EEEiS4_  (/src/harfbuzz/src/hb-open-type.hh:101-104)
     580         0  _ZNK2OT7IntTypeIjLj4EE3cmpIjTnPN12hb_enable_ifIXsr3std14is_convertibleIT_jEE5valueEvE4typeELPv0EEEiS4_  (/src/harfbuzz/src/hb-open-type.hh:101-104)
     580         0  _ZNK2OT7IntTypeItLj2EE3cmpIS1_TnPN12hb_enable_ifIXsr3std14is_convertibleIT_tEE5valueEvE4typeELPv0EEEiS4_  (/src/harfbuzz/src/hb-open-type.hh:101-104)
     580         0  _ZNK2OT7IntTypeIjLj4EE3cmpINS_3TagETnPN12hb_enable_ifIXsr3std14is_convertibleIT_jEE5valueEvE4typeELPv0EEEiS5_  (/src/harfbuzz/src/hb-open-type.hh:101-104)
       0       390  OT::ResourceTypeRecord::is_sfnt() const  (/src/harfbuzz/src/hb-open-file.hh:328-328)
       0       390  OT::ResourceMap::get_type_record(unsigned int) const  (/src/harfbuzz/src/hb-open-file.hh:397-397)
       0       390  OT::ArrayOfM1<OT::ResourceTypeRecord, OT::IntType<unsigned short, 2u> >::operator[](int) const  (/src/harfbuzz/src/hb-open-type.hh:898-903)
       0       273  OT::ResourceMap::get_face(unsigned int, void const*) const  (/src/harfbuzz/src/hb-open-file.hh:371-382)
       0       273  OT::ResourceMap::get_type_count() const  (/src/harfbuzz/src/hb-open-file.hh:394-394)
       0       273  OT::ResourceForkHeader::get_face(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-open-file.hh:420-425)
     102        31  OT::OffsetTo<OT::ClassDef, OT::IntType<unsigned short, 2u>, true>::sanitize_shallow(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-open-type.hh:416-422)
     102        31  OT::OffsetTo<OT::AttachList, OT::IntType<unsigned short, 2u>, true>::sanitize_shallow(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-open-type.hh:416-422)
     102        31  OT::OffsetTo<OT::Layout::Common::Coverage, OT::IntType<unsigned short, 2u>, true>::sanitize_shallow(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-open-type.hh:416-422)
... (857 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
  (no divergent branches in chain functions; the split is off-chain)

[off-chain: 14 additional divergent branches across 10 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c62e53eef0209e96, size=89 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1388s, mutation_op=BytesDeleteMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 66 65 61 74   ......      feat
  0010: 20 20 20 20 00 00 00 18 00 01 1f 07 00 03 00 20       ........... 
  0020: 20 20 04 00 20 fe 06 ff ff ff a8 00 00 ff 00 00     .. ...........
  0030: 00 00 00 00 20 20 20 20 20 20 47 b0 31 53 20 20   ....      G.1S  
Seed 2 (id=9c804af094eab4e9, size=315 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1851s, mutation_op=BytesRandSetMutator,CrossoverReplaceMutator,BytesSwapMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 10 20 20 20 20 20 20 74 72 61 6b   ......      trak
  0010: 20 ff 1f 20 00 00 00 18 00 01 00 0a 56 4f 52 47    .. ........VORG
  0020: 00 01 00 20 20 20 20 20 20 47 8e 8e 14 ff ff ff   ...      G......
  0030: ff 00 00 14 00 00 20 20 20 20 1c 2d 00 01 ff 26   ......    .-...&
Seed 3 (id=732053130abf1016, size=330 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2033s, mutation_op=WordInterestingMutator):
  0000: 00 01 00 00 00 02 20 20 20 20 20 20 74 72 61 6b   ......      trak
  0010: 20 ff 1f 01 00 00 00 18 00 01 00 0a 00 00 00 02    ...............
  0020: 40 00 00 20 20 20 20 20 20 47 8e 8e 14 01 7f 00   @..      G......
  0030: 00 00 00 14 00 00 20 20 20 20 1c 2d 00 02 ff 26   ......    .-...&
Seed 4 (id=ee30a6f4bc045a32, size=92 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2860s, mutation_op=TokenReplace,TokenInsert,BitFlipMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 2c 6e 61 6d 65   ......     ,name
  0010: e0 20 20 20 00 00 00 18 00 01 00 02 00 00 00 18   .   ............
  0020: 00 01 74 6c 66 64 00 02 00 02 00 00 00 20 05 01   ..tlfd....... ..
  0030: 63 7f e1 68 00 25 49 92 04 01 20 08 01 04 a0 fa   c..h.%I... .....
Seed 5 (id=0595725099e8d103, size=313 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2953s, mutation_op=ByteRandMutator,BytesInsertCopyMutator,BytesSetMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 74 72 61 6b   ......      trak
  0010: 20 ff 1f e0 00 00 00 18 00 01 00 0a 00 02 00 eb    ...............
  0020: 00 02 00 12 12 12 14 00 00 20 00 00 00 05 00 00   ......... ......
  0030: 00 20 20 20 00 64 20 68 61 6e 74 00 65 72 6e 00   .   .d hant.ern.

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=6a9f1dbd630938ea, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=429s, mutation_op=WordInterestingMutator,TokenInsert,BytesDeleteMutator):
  0000: 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0010: 00 20 00 00 00 20 20 30 00 00 00 20 20 20 20 20   . ...  0...     
  0020: 20 30 00 00 00 00 09 00 00 00 09 00 00 20 20 30    0...........  0
  0030: 00 01 00 00 00 00 00 2b 00 00 01 00 00 20 00 00   .......+..... ..
Seed 2 (id=77f7b031448ffb45, size=98 bytes, fuzzer=value_profile, trial=1, discovered_at=429s, mutation_op=CrossoverReplaceMutator,BytesDeleteMutator,ByteNegMutator,CrossoverInsertMutator,BytesInsertMutator,TokenReplace):
  0000: 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0010: 00 20 00 00 00 20 20 30 00 00 00 00 00 00 00 00   . ...  0........
  0020: 00 00 20 20 20 20 20 20 30 00 00 00 00 09 01 10   ..      0.......
  0030: 00 00 00 01 97 1a 20 72 61 66 63 10 00 00 df fe   ...... rafc.....
Seed 3 (id=4d5c8a2a44512dba, size=40 bytes, fuzzer=value_profile, trial=1, discovered_at=526s, mutation_op=BytesDeleteMutator):
  0000: 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0010: 00 20 00 00 00 00 2b 00 00 01 00 00 20 00 00 30   . ....+..... ..0
  0020: 12 fe c5 c6 c6 c6 c6 c6                           ........
Seed 4 (id=240d645ec7d8c84a, size=105 bytes, fuzzer=value_profile, trial=1, discovered_at=614s, mutation_op=ByteDecMutator,TokenInsert,BytesCopyMutator,ByteNegMutator,ByteDecMutator,WordInterestingMutator):
  0000: 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0010: 00 e0 00 00 00 20 20 09 00 00 00 92 04 00 1f 00   .....  .........
  0020: 00 40 00 0e 00 00 4a 0e 00 00 ff 0e 00 00 4b 32   .@....J.......K2
  0030: 32 32 20 20 ef f0 f0 37 37 37 f0 f0 f0 f0 f0 f0   22  ...777......
Seed 5 (id=c51f39daa934c9e0, size=91 bytes, fuzzer=value_profile, trial=1, discovered_at=11574s, mutation_op=TokenReplace,ByteIncMutator,ByteFlipMutator,BytesInsertCopyMutator,BytesInsertMutator,QwordAddMutator):
  0000: 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
  0010: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 10 00   ................
  0020: 7a 01 e4 38 71 03 00 f0 0b 00 00 10 0b 00 00 00   z..8q...........
  0030: 00 80 00 00 dd dd dd f0 0b 00 00 10 0b 13 00 00   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  01(.)x10                            00(.)x7                             DIFFER
   0x0002  00(.)x10                            01(.)x7                             DIFFER
   0x0005  01(.)x8 10(.)x1 02(.)x1             00(.)x7                             DIFFER
   0x0006  20( )x6 db(.)x3 da(.)x1             00(.)x7                             DIFFER
   0x0007  20( )x6 da(.)x4                     00(.)x5 01(.)x2                     DIFFER
   0x0008  20( )x6 da(.)x4                     00(.)x7                             DIFFER
   0x0009  20( )x6 da(.)x4                     00(.)x7                             DIFFER
   0x000a  20( )x5 10(.)x4 06(.)x1             00(.)x7                             DIFFER
   0x000b  20( )x4 3a(:)x4 2c(,)x1 8d(.)x1     00(.)x5 03(.)x2                     DIFFER
   0x000c  74(t)x4 43(C)x4 66(f)x1 6e(n)x1     00(.)x5 20( )x2                     DIFFER
   0x000d  72(r)x4 42(B)x4 65(e)x1 61(a)x1     00(.)x5 21(!)x1 2e(.)x1             DIFFER
   0x000e  61(a)x5 4c(L)x4 6d(m)x1             00(.)x5 20( )x2                     DIFFER
   0x000f  6b(k)x4 43(C)x4 74(t)x1 65(e)x1     00(.)x5 20( )x2                     DIFFER
   0x0010  20( )x9 e0(.)x1                     00(.)x7                             DIFFER
   0x0011  00(.)x4 20( )x3 ff(.)x3             20( )x3 2b(+)x2 e0(.)x1 00(.)x1     PARTIAL
   0x0012  e2(.)x4 1f(.)x3 20( )x2 1e(.)x1     00(.)x7                             DIFFER
   0x0013  20( )x4 01(.)x3 00(.)x2 e0(.)x1     00(.)x7                             PARTIAL
   0x0014  00(.)x10                            00(.)x5 01(.)x2                     PARTIAL
   0x0015  00(.)x10                            00(.)x4 20( )x3                     PARTIAL
   0x0016  00(.)x10                            20( )x3 00(.)x3 2b(+)x1             PARTIAL
   0x0017  18(.)x10                            00(.)x4 30(0)x2 09(.)x1             DIFFER
   0x0019  01(.)x6 02(.)x4                     00(.)x6 01(.)x1                     PARTIAL
   0x001a  00(.)x9 1f(.)x1                     00(.)x7                             PARTIAL
   0x001b  0a(.)x7 07(.)x1 02(.)x1 10(.)x1     00(.)x5 20( )x1 92(.)x1             DIFFER
   0x001c  00(.)x9 56(V)x1                     20( )x2 00(.)x2 ff(.)x2 04(.)x1     PARTIAL
   0x001d  00(.)x6 03(.)x1 4f(O)x1 02(.)x1 +1u  00(.)x6 20( )x1                     PARTIAL
   0x001e  00(.)x8 52(R)x1 02(.)x1             00(.)x2 13(.)x2 20( )x1 1f(.)x1 +1u  PARTIAL
   0x001f  02(.)x4 20( )x1 47(G)x1 18(.)x1 +3u  00(.)x5 20( )x1 30(0)x1             PARTIAL
   0x0020  00(.)x8 20( )x1 40(@)x1             00(.)x4 20( )x1 12(.)x1 7a(z)x1     PARTIAL
   0x0021  00(.)x5 01(.)x2 02(.)x2 20( )x1     00(.)x3 30(0)x1 fe(.)x1 40(@)x1 +1u  PARTIAL
   0x0022  00(.)x8 04(.)x1 74(t)x1             00(.)x4 20( )x1 c5(.)x1 e4(.)x1     PARTIAL
   0x0024  00(.)x5 20( )x3 66(f)x1 12(.)x1     00(.)x4 20( )x1 c6(.)x1 71(q)x1     PARTIAL
   0x0025  02(.)x4 20( )x2 fe(.)x1 64(d)x1 +2u  00(.)x4 20( )x1 c6(.)x1 03(.)x1     PARTIAL
   0x0026  00(.)x6 20( )x2 06(.)x1 14(.)x1     00(.)x3 09(.)x1 20( )x1 c6(.)x1 +1u  PARTIAL
   0x0028  00(.)x7 20( )x2 ff(.)x1             00(.)x2 20( )x2 30(0)x1 0b(.)x1     PARTIAL
   0x0029  00(.)x4 47(G)x2 ff(.)x1 02(.)x1 +2u  00(.)x6                             PARTIAL
   0x002a  00(.)x7 8e(.)x2 a8(.)x1             00(.)x2 01(.)x2 09(.)x1 ff(.)x1     PARTIAL
   0x002b  02(.)x4 00(.)x3 8e(.)x2 04(.)x1     00(.)x2 d4(.)x2 0e(.)x1 10(.)x1     PARTIAL
   0x002c  00(.)x7 14(.)x2 fb(.)x1             00(.)x5 0b(.)x1                     PARTIAL
   0x002d  02(.)x4 ff(.)x2 01(.)x1 20( )x1 +2u  00(.)x4 20( )x1 09(.)x1             PARTIAL
   ... (16 more divergent offsets)
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
  prompts_b/harfbuzz_5397.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5397,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5397 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5397 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5397 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).