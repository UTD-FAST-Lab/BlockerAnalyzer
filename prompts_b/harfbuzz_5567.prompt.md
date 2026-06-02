==== BLOCKER ====
Target: harfbuzz
Branch ID: 5567
Location: /src/harfbuzz/src/hb-ot-layout.cc:1680:28
Enclosing function: hb_ot_layout_get_size_params
Source line:   for (unsigned int i = 0; i < num_features; i++)
Globally blocked side: T  (true branch)

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
  avg hitcount on branch: winner=357  loser=0
  prob_div=1.00  dur_div=22.10h  hit_div=357
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.70h  loser=24.00h
  avg hitcount on branch: winner=353  loser=0
  prob_div=1.00  dur_div=22.30h  hit_div=353
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5567/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb_ot_layout_get_size_params (/src/harfbuzz/src/hb-ot-layout.cc:1675-1707) ---
[ ]  1673  			      unsigned int    *range_start,       /* OUT.  May be NULL */
[ ]  1674  			      unsigned int    *range_end          /* OUT.  May be NULL */)
[B]  1675  {
[B]  1676    const GPOS &gpos = *face->table.GPOS->table;
[B]  1677    const hb_tag_t tag = HB_TAG ('s','i','z','e');
[ ]  1678  
[B]  1679    unsigned int num_features = gpos.get_feature_count ();
[B]  1680    for (unsigned int i = 0; i < num_features; i++) <-- BLOCKER
[W]  1681    {
[W]  1682      if (tag == gpos.get_feature_tag (i))
[ ]  1683      {
[ ]  1684        const OT::Feature &f = gpos.get_feature (i);
[ ]  1685        const OT::FeatureParamsSize &params = f.get_feature_params ().get_size_params (tag);
[ ]  1686  
[ ]  1687        if (params.designSize)
[ ]  1688        {
[ ]  1689  	if (design_size) *design_size = params.designSize;
[ ]  1690  	if (subfamily_id) *subfamily_id = params.subfamilyID;
[ ]  1691  	if (subfamily_name_id) *subfamily_name_id = params.subfamilyNameID;
[ ]  1692  	if (range_start) *range_start = params.rangeStart;
[ ]  1693  	if (range_end) *range_end = params.rangeEnd;
[ ]  1694  
[ ]  1695  	return true;
[ ]  1696        }
[ ]  1697      }
[W]  1698    }
[ ]  1699  
[B]  1700    if (design_size) *design_size = 0;
[B]  1701    if (subfamily_id) *subfamily_id = 0;
[B]  1702    if (subfamily_name_id) *subfamily_name_id = HB_OT_NAME_ID_INVALID;
[B]  1703    if (range_start) *range_start = 0;
[B]  1704    if (range_end) *range_end = 0;
[ ]  1705  
[B]  1706    return false;
[B]  1707  }

--- Caller (1 hop): hb-shape-fuzzer.cc:test_font(hb_font_t*, unsigned int) (/src/harfbuzz/test/api/test-ot-face.c:38-198, calls hb_ot_layout_get_size_params at line 112) (±10 around call site) ---
[ ]   102  
[B]   103    hb_ot_layout_has_glyph_classes (face);
[B]   104    hb_ot_layout_has_substitution (face);
[B]   105    hb_ot_layout_has_positioning (face);
[ ]   106  
[B]   107    hb_ot_layout_get_ligature_carets (font, HB_DIRECTION_LTR, cp, 0, NULL, NULL);
[ ]   108  
[B]   109    {
[B]   110      unsigned temp = 0, temp2 = 0;
[B]   111      hb_ot_name_id_t name = HB_OT_NAME_ID_FULL_NAME;
[B]   112      hb_ot_layout_get_size_params (face, &temp, &temp, &name, &temp, &temp); <-- CALL
[B]   113      hb_tag_t cv01 = HB_TAG ('c','v','0','1');
[B]   114      unsigned feature_index = 0;
[B]   115      hb_ot_layout_language_find_feature (face, HB_OT_TAG_GSUB, 0,
[B]   116  					HB_OT_LAYOUT_DEFAULT_LANGUAGE_INDEX,
[B]   117  					cv01, &feature_index);
[B]   118      hb_ot_layout_feature_get_name_ids (face, HB_OT_TAG_GSUB, feature_index,
[B]   119  				       &name, &name, &name, &temp, &name);
[B]   120      temp = 1;
[B]   121      hb_ot_layout_feature_get_characters (face, HB_OT_TAG_GSUB, feature_index, 0, &temp, &g);
[B]   122      temp = 1;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-shape-fuzzer.cc:test_font(hb_font_t*, unsigned int)  (/src/harfbuzz/test/api/test-ot-face.c:38-198, calls hb_ot_layout_get_size_params at line 112)
hop 3  LLVMFuzzerTestOneInput  (/src/harfbuzz/test/fuzzing/hb-shape-fuzzer.cc:13-64, calls hb-shape-fuzzer.cc:test_font(hb_font_t*, unsigned int) at line 51)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     400         0  GPOSProxy::GPOSProxy(hb_face_t*)  (/src/harfbuzz/src/hb-ot-layout.cc:1847-1848)
     400         0  hb_ot_map_t::position(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) const  (/src/harfbuzz/src/hb-ot-layout.cc:2011-2018)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb_ot_layout_get_size_params  (/src/harfbuzz/src/hb-ot-layout.cc:1675-1707) ---
  d=1   L1680  T=129 F=20  T=0 F=20  for (unsigned int i = 0; i < num_features; i++)  <-- BLOCKER
  d=1   L1682  T=0 F=129  T=0 F=0  if (tag == gpos.get_feature_tag (i))

[off-chain: 6 additional divergent branches across 3 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0119dc42c7db21ec, size=192 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1546s, mutation_op=QwordAddMutator,ByteIncMutator,CrossoverReplaceMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 20 ff 1f 20 00 00 00 18 00 01 00 0a 03 00 00 02    .. ............
  0020: 00 01 00 00 00 01 a8 a8 a8 ba 20 20 48 56 41 52   ..........  HVAR
  0030: 20 20 20 20 00 00 00 18 00 01 64 2d 04 00 03 ff       ......d-....
Seed 2 (id=07363f7c60619b96, size=209 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1549s, mutation_op=BitFlipMutator,BytesRandInsertMutator,TokenReplace,TokenInsert,CrossoverReplaceMutator,BytesDeleteMutator,ByteIncMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 20 47 50 4f 53   ......      GPOS
  0010: 20 ff 1f 20 00 00 00 18 00 01 00 0a 00 04 00 02    .. ............
  0020: 00 02 00 20 20 20 20 20 00 00 8e 8e 14 14 14 14   ...     ........
  0030: 14 14 14 14 01 00 20 20 20 20 1c 2d 00 00 00 04   ......    .-....
Seed 3 (id=07c59a766851e315, size=110 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2017s, mutation_op=BytesCopyMutator,BytesCopyMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 01 20 20 80 ff 20 20 47 50 4f 53   ......  ..  GPOS
  0010: 20 ff 1f 20 00 00 00 18 00 01 00 0a 00 02 00 02    .. ............
  0020: 00 02 00 20 e0 20 20 20 20 47 8e 01 00 02 00 20   ... .    G..... 
  0030: e0 20 20 20 20 47 8e 01 00 02 00 20 e0 20 20 20   .    G..... .   
Seed 4 (id=12f382d590b917a0, size=104 bytes, fuzzer=cmplog, trial=1, discovered_at=2386s, mutation_op=BytesRandInsertMutator,BytesRandSetMutator,BytesSetMutator,BytesRandSetMutator):
  0000: 00 01 00 00 00 01 20 20 20 20 20 df 47 50 4f 53   ......     .GPOS
  0010: 00 01 00 80 00 00 00 10 00 10 03 03 03 e8 03 10   ................
  0020: 00 02 00 10 00 10 02 03 03 10 03 20 00 01 00 02   ........... ....
  0030: 00 03 00 fa 03 00 ff ff 03 01 24 21 10 00 00 20   ..........$!... 
Seed 5 (id=083147813711d603, size=140 bytes, fuzzer=cmplog, trial=1, discovered_at=2599s, mutation_op=ByteAddMutator,BytesInsertMutator):
  0000: 00 01 00 00 00 01 07 20 21 20 1e 20 47 50 4f 53   ....... ! . GPOS
  0010: 00 01 00 0d 00 00 00 10 00 02 00 47 00 00 00 00   ...........G....
  0020: 00 02 00 07 4f 00 00 10 ff ff 00 00 6f 03 03 00   ....O.......o...
  0030: 00 00 00 02 00 44 00 01 00 0d 02 00 00 00 00 10   .....D..........

==== Loser-blocking seeds (take false branch) ====
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
   0x0000  00(.)x20                            00(.)x4 e0(.)x2 05(.)x2 87(.)x1 +11u  PARTIAL
   0x0001  01(.)x20                            00(.)x3 0e(.)x2 ff(.)x2 07(.)x2 +11u  PARTIAL
   0x0002  00(.)x20                            00(.)x10 ff(.)x3 0d(.)x1 0e(.)x1 +5u  PARTIAL
   0x0003  00(.)x20                            00(.)x11 ff(.)x2 2d(-)x2 0e(.)x1 +4u  PARTIAL
   0x0004  00(.)x20                            00(.)x2 df(.)x2 68(h)x2 70(p)x2 +12u  PARTIAL
   0x0005  01(.)x18 02(.)x2                    00(.)x4 20( )x4 0e(.)x3 06(.)x2 +7u  PARTIAL
   0x0007  20( )x19 8d(.)x1                    00(.)x11 e0(.)x1 55(U)x1 77(w)x1 +5u  DIFFER
   0x0009  20( )x17 ff(.)x1 00(.)x1 8d(.)x1    00(.)x3 0a(.)x2 2b(+)x1 17(.)x1 +12u  PARTIAL
   0x000c  47(G)x20                            00(.)x3 01(.)x2 20( )x2 2c(,)x1 +11u  DIFFER
   0x000d  50(P)x20                            20( )x4 00(.)x4 18(.)x1 17(.)x1 +8u  DIFFER
   0x000e  4f(O)x20                            00(.)x5 e0(.)x1 64(d)x1 18(.)x1 +10u  DIFFER
   0x000f  53(S)x20                            00(.)x5 6a(j)x1 6f(o)x1 fa(.)x1 +10u  DIFFER
   0x0010  20( )x10 00(.)x10                   00(.)x5 20( )x2 79(y)x1 2d(-)x1 +9u  PARTIAL
   0x0011  01(.)x10 ff(.)x9 fe(.)x1            20( )x4 00(.)x2 06(.)x2 2d(-)x1 +9u  DIFFER
   0x0012  00(.)x10 1e(.)x6 1f(.)x4            00(.)x8 68(h)x1 0a(.)x1 18(.)x1 +7u  PARTIAL
   0x0014  00(.)x20                            68(h)x3 00(.)x2 6e(n)x1 74(t)x1 +11u  PARTIAL
   0x0015  00(.)x20                            00(.)x4 06(.)x2 74(t)x1 17(.)x1 +10u  PARTIAL
   0x0016  00(.)x20                            00(.)x8 01(.)x2 2d(-)x1 0e(.)x1 +6u  PARTIAL
   0x0017  18(.)x10 10(.)x10                   00(.)x7 74(t)x2 68(h)x1 3d(=)x1 +6u  DIFFER
   0x0018  00(.)x20                            20( )x4 00(.)x3 6b(k)x1 61(a)x1 +8u  PARTIAL
   0x0019  01(.)x10 02(.)x9 10(.)x1            00(.)x3 20( )x3 9f(.)x2 19(.)x2 +7u  PARTIAL
   0x001a  00(.)x17 03(.)x1 31(1)x1 22(")x1    00(.)x5 20( )x2 9f(.)x2 0c(.)x1 +7u  PARTIAL
   0x001e  00(.)x17 03(.)x1 2f(/)x1 69(i)x1    00(.)x8 ff(.)x2 01(.)x2 80(.)x1 +3u  PARTIAL
   0x0020  00(.)x20                            00(.)x4 df(.)x1 c8(.)x1 37(7)x1 +8u  PARTIAL
   0x0022  00(.)x18 fe(.)x2                    00(.)x8 01(.)x2 02(.)x1 1b(.)x1 +2u  PARTIAL
   0x0032  00(.)x17 20( )x2 14(.)x1            00(.)x3 01(.)x2 fe(.)x1 40(@)x1 +5u  PARTIAL
   0x003e  00(.)x15 ff(.)x2 03(.)x1 20( )x1 +1u  00(.)x4 9f(.)x1 20( )x1 01(.)x1     PARTIAL
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
  prompts_b/harfbuzz_5567.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5567,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5567 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5567 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5567 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).