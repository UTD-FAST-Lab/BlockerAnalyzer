==== BLOCKER ====
Target: harfbuzz
Branch ID: 5389
Location: /src/harfbuzz/src/hb-open-file.hh:487:5
Enclosing function: OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const
Source line:     case Typ1Tag:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.30h  loser=24.00h
  avg hitcount on branch: winner=9286  loser=0
  prob_div=1.00  dur_div=20.70h  hit_div=9286
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=8.50h  loser=24.00h
  avg hitcount on branch: winner=2263  loser=0
  prob_div=0.80  dur_div=15.50h  hit_div=2263
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5389/{W,L}/branch_coverage_show.txt

--- Enclosing function: OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const (/src/harfbuzz/src/hb-open-file.hh:478-493) ---
[ ]   476    }
[ ]   477    const OpenTypeFontFace& get_face (unsigned int i, unsigned int *base_offset = nullptr) const
[B]   478    {
[B]   479      if (base_offset)
[B]   480        *base_offset = 0;
[B]   481      switch (u.tag) {
[ ]   482      /* Note: for non-collection SFNT data we ignore index.  This is because
[ ]   483       * Apple dfont container is a container of SFNT's.  So each SFNT is a
[ ]   484       * non-TTC, but the index is more than zero. */
[ ]   485      case CFFTag:	/* All the non-collection tags */
[ ]   486      case TrueTag:
[W]   487      case Typ1Tag: <-- BLOCKER
[W]   488      case TrueTypeTag:	return u.fontFace;
[ ]   489      case TTCTag:	return u.ttcHeader.get_face (i);
[ ]   490      case DFontTag:	return u.rfHeader.get_face (i, base_offset);
[L]   491      default:		return Null (OpenTypeFontFace);
[B]   492      }
[B]   493    }

--- Caller (1 hop): hb-face.cc:_hb_face_for_data_reference_table(hb_face_t*, unsigned int, void*) (/src/harfbuzz/src/hb-face.cc:174-189, calls OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const at line 182) (full body — short) ---
[B]   174  {
[B]   175    hb_face_for_data_closure_t *data = (hb_face_for_data_closure_t *) user_data;
[ ]   176  
[B]   177    if (tag == HB_TAG_NONE)
[ ]   178      return hb_blob_reference (data->blob);
[ ]   179  
[B]   180    const OT::OpenTypeFontFile &ot_file = *data->blob->as<OT::OpenTypeFontFile> ();
[B]   181    unsigned int base_offset;
[B]   182    const OT::OpenTypeFontFace &ot_face = ot_file.get_face (data->index, &base_offset); <-- CALL
[ ]   183  
[B]   184    const OT::OpenTypeTable &table = ot_face.get_table_by_tag (tag);
[ ]   185  
[B]   186    hb_blob_t *blob = hb_blob_create_sub_blob (data->blob, base_offset + table.offset, table.length);
[ ]   187  
[B]   188    return blob;
[B]   189  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  OT::TTCHeader::get_face(unsigned int) const  (/src/harfbuzz/src/hb-open-file.hh:258-264, calls OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const at line 261)
hop 2  OT::TTCHeaderVersion1::get_face(unsigned int) const  (/src/harfbuzz/src/hb-open-file.hh:224-224, calls OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const at line 224)
hop 3  OT::ResourceRecord::sanitize(hb_sanitize_context_t*, void const*) const  (/src/harfbuzz/src/hb-open-file.hh:301-306, calls OT::TTCHeaderVersion1::get_face(unsigned int) const at line 305)
hop 4  CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:90-102, calls OT::ResourceRecord::sanitize(hb_sanitize_context_t*, void const*) const at line 97)
hop 5  CFF::CFF2VariationStore::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-ot-cff2-table.hh:117-120, calls CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const at line 119)
hop 5  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:398-475, calls CFF::CFF2FDSelect::sanitize(hb_sanitize_context_t*, unsigned int) const at line 416)
hop 6  OT::cff2::accelerator_t::accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:515-515, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 515)
hop 6  OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::~accelerator_templ_t()  (/src/harfbuzz/src/hb-ot-cff2-table.hh:476-476, calls OT::cff2::accelerator_templ_t<CFF::cff2_private_dict_opset_t, CFF::cff2_private_dict_values_base_t<CFF::dict_val_t> >::accelerator_templ_t(hb_face_t*) at line 476)
hop 7  OT::cff2_accelerator_t::cff2_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-cff2-table.hh:538-538, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 538)
hop 7  OT::hmtx_accelerator_t::hmtx_accelerator_t(hb_face_t*)  (/src/harfbuzz/src/hb-ot-hmtx-table.hh:449-449, calls OT::cff2::accelerator_t::accelerator_t(hb_face_t*) at line 449)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1170         0  OT::TableRecord::cmp(OT::Tag) const  (/src/harfbuzz/src/hb-open-file.hh:56-56)
      20         0  OT::OpenTypeOffsetTable::sanitize(hb_sanitize_context_t*) const  (/src/harfbuzz/src/hb-open-file.hh:201-204)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OT::OpenTypeFontFile::get_face(unsigned int, unsigned int*) const  (/src/harfbuzz/src/hb-open-file.hh:478-493) ---
  d=1   L 487  T=755 F=0  T=0 F=768  case Typ1Tag:  <-- BLOCKER
  d=1   L 491  T=0 F=755  T=768 F=0  default:		return Null (OpenTypeFontFace);

[off-chain: 2 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=15af638beaf4cc6d, size=31 bytes, fuzzer=cmplog, trial=1, discovered_at=5s, mutation_op=ByteAddMutator,BytesRandSetMutator,BytesInsertMutator,ByteRandMutator,BytesDeleteMutator,BytesRandSetMutator,CrossoverReplaceMutator):
  0000: 74 79 70 31 00 01 20 20 20 20 20 20 20 d7 01 00   typ1..       ...
  0010: 20 20 31 20 20 20 fb 00 00 e6 20 00 00 00 e6        1   .... ....
Seed 2 (id=1b60c7890eb3d5f9, size=28 bytes, fuzzer=cmplog, trial=1, discovered_at=25s, mutation_op=CrossoverReplaceMutator,BitFlipMutator,BytesDeleteMutator,BytesDeleteMutator,BytesDeleteMutator,BytesDeleteMutator,TokenReplace):
  0000: 74 79 70 31 00 01 20 20 20 20 20 20 47 50 4f 53   typ1..      GPOS
  0010: 20 20 20 20 0d 0c 00 1a 20 34 20 ff                   .... 4 .
Seed 3 (id=3dae963711c219d5, size=55 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=49s, mutation_op=BytesDeleteMutator,ByteFlipMutator,BytesSetMutator):
  0000: 74 79 70 31 00 00 20 20 20 20 1e 00 20 20 00 00   typ1..    ..  ..
  0010: 80 00 20 20 20 20 56 4f 52 47 20 20 20 20 20 20   ..    VORG      
  0020: 56 4f 52 47 20 20 20 20 20 20 00 01 99 99 99 99   VORG      ......
  0030: 99 99 99 20 20 20 df                              ...   .
Seed 4 (id=6389f9fa97b2b73f, size=28 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=98s, mutation_op=WordAddMutator,ByteDecMutator,BytesSwapMutator,BytesDeleteMutator):
  0000: 74 79 70 31 00 01 20 20 20 20 1c 20 6b 65 72 78   typ1..    . kerx
  0010: 20 20 20 20 18 04 00 1a 20 20 20 c6                   ....   .
Seed 5 (id=43ba9afc5fc6d9d1, size=44 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=166s, mutation_op=BytesExpandMutator,ByteAddMutator,BytesSetMutator,CrossoverReplaceMutator):
  0000: 74 79 70 31 00 02 20 20 20 20 20 20 43 50 41 4c   typ1..      CPAL
  0010: 20 80 20 20 17 7f 20 20 20 20 d3 d3 76 68 65 61    .  ..    ..vhea
  0020: 20 20 20 6b 65 d2 d3 d3 d3 d3 d3 d3                  ke.......

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
   0x0000  74(t)x20                            00(.)x4 e0(.)x2 05(.)x2 87(.)x1 +11u  DIFFER
   0x0001  79(y)x20                            00(.)x3 0e(.)x2 ff(.)x2 07(.)x2 +11u  DIFFER
   0x0002  70(p)x20                            00(.)x10 ff(.)x3 0d(.)x1 0e(.)x1 +5u  DIFFER
   0x0003  31(1)x20                            00(.)x11 ff(.)x2 2d(-)x2 0e(.)x1 +4u  DIFFER
   0x0004  00(.)x20                            00(.)x2 df(.)x2 68(h)x2 70(p)x2 +12u  PARTIAL
   0x0005  01(.)x14 02(.)x4 00(.)x1 09(.)x1    00(.)x4 20( )x4 0e(.)x3 06(.)x2 +7u  PARTIAL
   0x0006  20( )x18 00(.)x1 07(.)x1            00(.)x12 e0(.)x1 68(h)x1 e5(.)x1 +4u  PARTIAL
   0x0007  20( )x18 80(.)x1 02(.)x1            00(.)x11 e0(.)x1 55(U)x1 77(w)x1 +5u  DIFFER
   0x0008  20( )x17 21(!)x2 00(.)x1            00(.)x4 20( )x2 29())x1 e0(.)x1 +11u  PARTIAL
   0x000b  20( )x17 00(.)x1 ff(.)x1 01(.)x1    00(.)x12 29())x1 13(.)x1 75(u)x1 +4u  PARTIAL
   0x0010  20( )x10 00(.)x8 80(.)x1 06(.)x1    00(.)x5 20( )x2 79(y)x1 2d(-)x1 +9u  PARTIAL
   0x0034  00(.)x8 20( )x3 fc(.)x1 06(.)x1     ff(.)x2 64(d)x1 01(.)x1 91(.)x1 +7u  PARTIAL
   0x003e  00(.)x3 20( )x2 8e(.)x1 ff(.)x1 +5u  00(.)x4 9f(.)x1 20( )x1 01(.)x1     PARTIAL
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
  prompts_b/harfbuzz_5389.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5389,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5389 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5389 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5389 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).