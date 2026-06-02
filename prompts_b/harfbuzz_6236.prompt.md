==== BLOCKER ====
Target: harfbuzz
Branch ID: 6236
Location: /src/harfbuzz/src/hb-sanitize.hh:239:9
Enclosing function: hb_sanitize_context_t::check_range(void const*, unsigned int) const
Source line: 	       (this->max_ops -= len) > 0);
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
  avg duration blocked: winner=1.10h  loser=24.00h
  avg hitcount on branch: winner=1232  loser=0
  prob_div=1.00  dur_div=22.90h  hit_div=1232
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.00h  loser=24.00h
  avg hitcount on branch: winner=1091  loser=0
  prob_div=1.00  dur_div=23.00h  hit_div=1091
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/6236/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_sanitize_context_t::check_range(void const*, unsigned int) const (/src/harfbuzz/src/hb-sanitize.hh:233-249) ---
[ ]   231    bool check_range (const void *base,
[ ]   232  		    unsigned int len) const
[B]   233    {
[B]   234      const char *p = (const char *) base;
[B]   235      bool ok = !len ||
[B]   236  	      (this->start <= p &&
[B]   237  	       p <= this->end &&
[B]   238  	       (unsigned int) (this->end - p) >= len &&
[B]   239  	       (this->max_ops -= len) > 0); <-- BLOCKER
[ ]   240  
[B]   241      DEBUG_MSG_LEVEL (SANITIZE, p, this->debug_depth+1, 0,
[B]   242  		     "check_range [%p..%p]"
[B]   243  		     " (%u bytes) in [%p..%p] -> %s",
[B]   244  		     p, p + len, len,
[B]   245  		     this->start, this->end,
[B]   246  		     ok ? "OK" : "OUT-OF-RANGE");
[ ]   247  
[B]   248      return likely (ok);
[B]   249    }

--- Caller (1 hop): bool hb_sanitize_context_t::check_struct<OT::FixedVersion<OT::IntType<unsigned short, 2u> > >(OT::FixedVersion<OT::IntType<unsigned short, 2u> > const*) const (/src/harfbuzz/src/hb-sanitize.hh:300-300, calls hb_sanitize_context_t::check_range(void const*, unsigned int) const at line 300) (full body — short) ---
[B]   300    { return likely (this->check_range (obj, obj->min_size)); } <-- CALL

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  AAT::ChainSubtable<AAT::ExtendedTypes>::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-aat-layout-morx-table.hh:945-954, calls hb_sanitize_context_t::check_range(void const*, unsigned int) const at line 949)
hop 2  CFF::CFF2VariationStore::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:117-120, calls hb_sanitize_context_t::check_range(void const*, unsigned int) const at line 119)
hop 3  CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:90-102, calls CFF::CFF2VariationStore::sanitize(hb_sanitize_context_t*) const at line 97)
hop 4  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:398-475, calls CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const at line 416)
hop 5  OT::cff2::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:515-515, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 515)
hop 5  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::~accelerator_templ_t()  (/src/harfbuzz/src/hb-ot-cff2-table.hh:476-476, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 476)
hop 6  OT::cff2_accelerator_t::cff2_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:538-538, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 538)
hop 6  OT::hmtx_accelerator_t::hmtx_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:449-449, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 449)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
  267000     41200  OT::IntType<unsigned short, 2u>::operator unsigned int() const  (/src/harfbuzz/src/hb-open-type.hh:68-68)
  267000     41200  OT::IntType<short, 2u>::operator int() const  (/src/harfbuzz/src/hb-open-type.hh:68-68)
  267000     41200  OT::IntType<unsigned int, 4u>::operator unsigned int() const  (/src/harfbuzz/src/hb-open-type.hh:68-68)
  267000     41200  OT::IntType<unsigned int, 3u>::operator unsigned int() const  (/src/harfbuzz/src/hb-open-type.hh:68-68)
  267000     41200  OT::IntType<unsigned char, 1u>::operator unsigned int() const  (/src/harfbuzz/src/hb-open-type.hh:68-68)
  267000     41200  OT::IntType<int, 4u>::operator int() const  (/src/harfbuzz/src/hb-open-type.hh:68-68)
  267000     41200  OT::IntType<signed char, 1u>::operator int() const  (/src/harfbuzz/src/hb-open-type.hh:68-68)
  110000        20  hb_sanitize_context_t::check_range(void const*, unsigned int) const  (/src/harfbuzz/src/hb-sanitize.hh:233-249)  <-- enclosing
  118000      8570  OT::Offset<OT::IntType<unsigned short, 2u>, true>::is_null() const  (/src/harfbuzz/src/hb-open-type.hh:235-235)
  118000      8570  OT::Offset<OT::IntType<unsigned short, 2u>, false>::is_null() const  (/src/harfbuzz/src/hb-open-type.hh:235-235)
  118000      8570  OT::Offset<OT::IntType<unsigned int, 4u>, false>::is_null() const  (/src/harfbuzz/src/hb-open-type.hh:235-235)
  118000      8570  OT::Offset<OT::IntType<unsigned int, 4u>, true>::is_null() const  (/src/harfbuzz/src/hb-open-type.hh:235-235)
  118000      8570  OT::Offset<OT::IntType<unsigned int, 3u>, true>::is_null() const  (/src/harfbuzz/src/hb-open-type.hh:235-235)
  118000      8570  OT::Offset<OT::IntType<unsigned int, 3u>, false>::is_null() const  (/src/harfbuzz/src/hb-open-type.hh:235-235)
  118000      8570  OT::Offset<OT::IntType<unsigned char, 1u>, false>::is_null() const  (/src/harfbuzz/src/hb-open-type.hh:235-235)
... (1777 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb_sanitize_context_t::check_range(void const*, unsigned int) const  (/src/harfbuzz/src/hb-sanitize.hh:233-249) ---
  d=1   L 235  T=1470 F=108000  T=0 F=20  bool ok = !len ||
  d=1   L 236  T=108000 F=0  T=20 F=0  (this->start <= p &&
  d=1   L 237  T=108000 F=367  T=20 F=0  p <= this->end &&
  d=1   L 238  T=108000 F=64  T=20 F=0  (unsigned int) (this->end - p) >= len &&
  d=1   L 239  T=108000 F=79  T=20 F=0  (this->max_ops -= len) > 0);  <-- BLOCKER

[off-chain: 7 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=0183ae69d883d0e1, size=327 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5569s, mutation_op=TokenReplace,DwordAddMutator,CrossoverInsertMutator,WordAddMutator,DwordInterestingMutator,ByteRandMutator):
  0000: 00 01 00 00 00 01 ee ff 00 30 00 20 47 53 55 42   .........0. GSUB
  0010: 20 20 20 20 00 00 00 00 f6 ff 04 00 00 00 00 0a       ............
  0020: 00 01 18 e0 00 00 ab 42 20 3c 20 00 00 00 fd ff   .......B < .....
  0030: 00 12 00 0c 94 01 00 00 1d 43 20 20 01 00 00 00   .........C  ....
Seed 2 (id=00274477948eb8f0, size=323 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5758s, mutation_op=BytesRandInsertMutator,BytesSwapMutator,ByteIncMutator,ByteNegMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 01 ff 1e 20 00 00 00 18 00 01 00 00 00 01 ee ff   ... ............
  0020: 00 30 06 20 95 53 55 42 20 20 20 20 00 80 00 00   .0. .SUB    ....
  0030: 00 ff 02 4b 00 00 00 0a 00 00 18 e0 00 00 ab 42   ...K...........B
Seed 3 (id=02bcc5cdfb7e9955, size=177 bytes, fuzzer=cmplog, trial=1, discovered_at=6566s, mutation_op=TokenInsert,CrossoverReplaceMutator,CrossoverInsertMutator):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 21 00 00 00 10 00 02 00 47 00 00 00 03   ...!.......G....
  0020: 0d 01 00 05 4f 00 00 10 02 01 00 10 00 06 4f 00   ....O.........O.
  0030: 00 10 00 01 00 10 21 21 00 06 00 06 00 10 03 03   ......!!........
Seed 4 (id=00b2a12d39ae05f2, size=213 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=6679s, mutation_op=BytesSwapMutator,BytesSwapMutator,ByteInterestingMutator,BytesDeleteMutator,ByteInterestingMutator):
  0000: 00 01 00 00 00 02 ee ff 00 30 00 20 47 50 4f 53   .........0. GPOS
  0010: 20 20 20 20 00 00 00 00 ff ff 00 ec ec ec eb 7f       ............
  0020: 00 ec ec ec ec ec ec 18 18 18 20 04 01 00 fd ff   .......... .....
  0030: 00 11 01 00 94 01 00 00 ff 43 20 20 28 a0 00 00   .........C  (...
Seed 5 (id=010aab75f7fd71d8, size=251 bytes, fuzzer=cmplog, trial=1, discovered_at=6749s, mutation_op=ByteRandMutator,BytesSetMutator):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 1d 00 00 00 10 00 02 00 b9 00 00 00 03   ................
  0020: 00 00 00 06 4f 00 00 10 00 00 00 10 02 03 00 00   ....O...........
  0030: 00 10 00 02 00 06 00 ef 00 00 00 10 01 05 00 00   ................

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=003817559785f774, size=6 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteDecMutator,WordAddMutator):
  0000: 87 0e 0d 0e 22 0e                                 ....".
Seed 2 (id=002edec370c771cf, size=35 bytes, fuzzer=naive, trial=1, discovered_at=47s, mutation_op=BytesExpandMutator,BytesDeleteMutator,ByteNegMutator,TokenInsert,ByteIncMutator,ByteRandMutator):
  0000: 00 00 00 00 00 00 00 00 00 00 00 00 20 00 64 6f   ............ .do
  0010: 2d 68 0a 6f 74 00 0e 00 20 00 0c 00 0c 09 00 00   -h.ot... .......
  0020: 00 0c 00                                          ...
Seed 3 (id=0003cbd2b6f5fff8, size=13 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=BitFlipMutator,BytesDeleteMutator,WordAddMutator):
  0000: e0 17 00 00 1a 20 00 00 29 2b 29 29 2c            ..... ..)+)),
Seed 4 (id=00280212c7547f95, size=27 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=WordInterestingMutator,WordAddMutator,ByteAddMutator):
  0000: e0 e8 ff ff 20 00 00 55 e0 17 00 00 2b 20 00 fa   .... ..U....+ ..
  0010: 20 00 00 55 e0 17 00 00 61 2e 69                   ..U....a.i
Seed 5 (id=00167ff70704a0e0, size=23 bytes, fuzzer=value_profile, trial=1, discovered_at=120s, mutation_op=BytesInsertCopyMutator,CrossoverInsertMutator,ByteDecMutator):
  0000: 4c 0e 00 00 4c 0e 00 00 4c 16 00 00 00 18 18 00   L...L...L.......
  0010: 00 42 18 65 0e 00 ff                              .B.e...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x20                            00(.)x4 e0(.)x2 05(.)x2 20( )x2 +10u  PARTIAL
   0x0001  01(.)x20                            00(.)x3 0e(.)x2 07(.)x2 17(.)x1 +12u  PARTIAL
   0x0002  00(.)x20                            00(.)x10 ff(.)x2 0d(.)x1 0e(.)x1 +6u  PARTIAL
   0x0003  00(.)x20                            00(.)x12 2d(-)x2 0e(.)x1 ff(.)x1 +4u  PARTIAL
   0x0004  00(.)x20                            00(.)x3 df(.)x2 68(h)x2 70(p)x2 +11u  PARTIAL
   0x0005  01(.)x13 02(.)x7                    00(.)x5 20( )x4 0e(.)x3 06(.)x2 +6u  DIFFER
   0x0006  ee(.)x8 07(.)x8 20( )x3 05(.)x1     00(.)x12 68(h)x1 e5(.)x1 6e(n)x1 +4u  PARTIAL
   0x0007  20( )x12 ff(.)x6 01(.)x1 02(.)x1    00(.)x11 55(U)x1 77(w)x1 01(.)x1 +5u  PARTIAL
   0x0008  21(!)x9 00(.)x8 20( )x2 a1(.)x1     00(.)x4 29())x1 e0(.)x1 4c(L)x1 +12u  PARTIAL
   0x0009  20( )x12 30(0)x8                    00(.)x3 0a(.)x2 2b(+)x1 17(.)x1 +12u  PARTIAL
   0x000a  00(.)x9 1e(.)x9 20( )x2             00(.)x8 01(.)x2 29())x1 aa(.)x1 +7u  PARTIAL
   0x000b  20( )x17 e0(.)x1 00(.)x1 32(2)x1    00(.)x11 29())x1 13(.)x1 75(u)x1 +5u  PARTIAL
   0x000c  47(G)x20                            00(.)x4 20( )x2 2c(,)x1 2b(+)x1 +11u  DIFFER
   0x000d  50(P)x19 53(S)x1                    00(.)x5 20( )x3 18(.)x1 17(.)x1 +8u  DIFFER
   0x000e  4f(O)x19 55(U)x1                    00(.)x5 64(d)x1 18(.)x1 3d(=)x1 +10u  DIFFER
   0x000f  53(S)x19 42(B)x1                    00(.)x5 6f(o)x1 fa(.)x1 3d(=)x1 +10u  DIFFER
   0x0010  00(.)x10 20( )x8 01(.)x2            00(.)x5 20( )x2 2d(-)x1 3d(=)x1 +9u  PARTIAL
   0x0012  00(.)x10 20( )x7 1e(.)x2 98(.)x1    00(.)x8 0a(.)x1 18(.)x1 3d(=)x1 +7u  PARTIAL
   0x0014  00(.)x20                            68(h)x3 00(.)x2 74(t)x1 e0(.)x1 +11u  PARTIAL
   0x0015  00(.)x20                            00(.)x4 20( )x2 06(.)x2 17(.)x1 +9u  PARTIAL
   0x0016  00(.)x20                            00(.)x8 01(.)x2 20( )x2 0e(.)x1 +5u  PARTIAL
   0x0017  10(.)x10 00(.)x8 18(.)x2            00(.)x7 74(t)x2 20( )x2 3d(=)x1 +5u  PARTIAL
   0x0018  00(.)x12 ff(.)x6 f6(.)x1 76(v)x1    20( )x5 00(.)x3 61(a)x1 3d(=)x1 +7u  PARTIAL
   0x0019  02(.)x10 ff(.)x7 01(.)x2 76(v)x1    20( )x3 00(.)x2 9f(.)x2 19(.)x2 +8u  PARTIAL
   0x0028  00(.)x8 18(.)x7 20( )x3 02(.)x2     00(.)x5 20( )x1 02(.)x1 0e(.)x1 +5u  PARTIAL
   0x002a  20( )x10 00(.)x9 04(.)x1            00(.)x8 20( )x1 6d(m)x1 5b([)x1 +2u  PARTIAL
   0x002c  00(.)x13 02(.)x4 04(.)x2 01(.)x1    20( )x2 00(.)x2 01(.)x1 0e(.)x1 +7u  PARTIAL
   0x0030  00(.)x20                            2c(,)x1 fe(.)x1 01(.)x1 0e(.)x1 +8u  PARTIAL
   0x0032  00(.)x11 03(.)x5 02(.)x3 01(.)x1    00(.)x4 fe(.)x1 40(@)x1 9f(.)x1 +5u  PARTIAL
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
  prompts_b/harfbuzz_6236.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6236,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6236 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6236 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6236 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).