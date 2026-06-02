==== BLOCKER ====
Target: harfbuzz
Branch ID: 5989
Location: /src/harfbuzz/src/hb-ot-shaper-use.cc:357:11
Enclosing function: hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&)
Source line:   return (info.use_category() == USE(H) || info.use_category() == USE(HVM) || info.use_category() == USE(IS)) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive)
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        9        1          0  REFERENCE
fast                            10        0          0  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.00h  loser=23.60h
  avg hitcount on branch: winner=18  loser=0
  prob_div=1.00  dur_div=20.60h  hit_div=18
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=1.60h  loser=21.60h
  avg hitcount on branch: winner=15  loser=0
  prob_div=0.80  dur_div=20.00h  hit_div=15
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5989/{W,L}/branch_coverage_show.txt

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
[B]   426      {
[ ]   427        /* If we hit a halant, move after it; otherwise move to the beginning, and
[ ]   428         * shift things in between forward. */
[B]   429        j = i + 1;
[B]   430      }
[B]   431      else if (((flag) & (FLAG (USE(VPre)) | FLAG (USE(VMPre)))) &&
[ ]   432  	     /* Only move the first component of a MultipleSubst. */
[B]   433  	     0 == _hb_glyph_info_get_lig_comp (&info[i]) &&
[B]   434  	     j < i)
[ ]   435      {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:363-442, calls hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&) at line 401)
hop 3  hb-ot-shaper-use.cc:reorder_use(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:448-467, calls hb-ot-shaper-use.cc:reorder_syllable_use(hb_buffer_t*, unsigned int, unsigned int) at line 459)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-use.cc:is_halant_use(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-use.cc:356-359) ---
  d=1   L 357  T=0 F=220  T=1 F=304  return (info.use_category() == USE(H) || info.use_categor...  <-- BLOCKER
  d=1   L 357  T=19 F=220  T=0 F=305  return (info.use_category() == USE(H) || info.use_categor...  <-- BLOCKER
  d=1   L 358  T=19 F=0  T=1 F=0  !_hb_glyph_info_ligated (&info);

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c0c8806e5fc13b63, size=40 bytes, fuzzer=naive, trial=1, discovered_at=15s, mutation_op=BitFlipMutator,BitFlipMutator,BytesDeleteMutator,DwordInterestingMutator,ByteIncMutator):
  0000: 00 00 01 ff 00 00 00 00 00 03 00 00 00 00 00 01   ................
  0010: fe ff 21 ec 66 ff ff ff 7f 2d 00 00 ff 08 00 00   ..!.f....-......
  0020: 00 ff 03 20 20 00 97 97                           ...  ...
Seed 2 (id=edde4d3b2b39acca, size=40 bytes, fuzzer=naive, trial=1, discovered_at=80s, mutation_op=BitFlipMutator):
  0000: 00 00 01 fb 00 00 00 10 f4 07 00 00 00 00 00 01   ................
  0010: fe ff 21 ec 66 ff 00 ff 7f 2d 00 00 ff 08 00 00   ..!.f....-......
  0020: 00 ff 03 20 20 00 97 97                           ...  ...
Seed 3 (id=f63bb91fc14480f0, size=95 bytes, fuzzer=naive, trial=1, discovered_at=80s, mutation_op=ByteAddMutator,BitFlipMutator,WordInterestingMutator,BytesRandInsertMutator,BytesCopyMutator,BytesExpandMutator):
  0000: ff 6e 20 00 00 00 00 97 97 97 97 97 00 0c 0c 00   .n .............
  0010: 11 00 00 80 00 15 00 01 ff 00 00 02 00 00 03 00   ................
  0020: 00 00 00 00 01 fe ff dd dd dd dd dd dd dd dd dd   ................
  0030: 00 00 dd 21 ec 66 ff ff 8a 8a 8a 20 00 8a ff 7f   ...!.f..... ....
Seed 4 (id=890855f856f6ca42, size=2 bytes, fuzzer=naive, trial=1, discovered_at=150s, mutation_op=ByteInterestingMutator,ByteRandMutator,ByteRandMutator,BytesDeleteMutator):
  0000: 7f 2d                                             .-
Seed 5 (id=94baf643047e5047, size=53 bytes, fuzzer=naive, trial=1, discovered_at=281s, mutation_op=QwordAddMutator,BytesDeleteMutator):
  0000: 4b e9 01 00 ee 1f 00 00 3f 16 01 00 ee 54 54 fd   K.......?....TT.
  0010: ff ff ff 54 54 73 73 73 73 77 03 03 54 54 54 54   ...TTssssw..TTTT
  0020: 54 3a 54 54 54 54 54 50 73 73 73 73 77 03 ff 64   T:TTTTTPssssw..d
  0030: 00 00 03 03 03                                    .....

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0406343f1fc9d531, size=19 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5s, mutation_op=WordAddMutator,BytesDeleteMutator,QwordAddMutator,TokenInsert,BytesSwapMutator):
  0000: 00 01 02 22 00 10 0e 00 20 1f 01 00 1a 20 02 00   ...".... .... ..
  0010: 20 20 89                                            .
Seed 2 (id=044f6bc4804646ac, size=45 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=18s, mutation_op=QwordAddMutator,BytesSwapMutator,BytesCopyMutator,BytesDeleteMutator,BytesInsertMutator,TokenInsert):
  0000: 00 01 ff 73 6e 2d 00 00 18 18 00 00 1a 20 20 20   ...sn-.......   
  0010: 20 00 01 20 20 20 20 20 20 20 20 20 6b e8 20 20    ..         k.  
  0020: 20 00 20 20 20 00 01 20 20 20 2c 20 20             .   ..   ,  
Seed 3 (id=0170cbbd7538578d, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=151s, mutation_op=BytesSetMutator,DwordAddMutator,BytesDeleteMutator,BytesDeleteMutator,WordInterestingMutator,TokenInsert):
  0000: 00 20 97 97 00 00 20 20 00 00 00 00 0c 00 00 02   . ....  ........
  0010: 00 0d 01 00 20 97 97 01 00 3b 3b 3b 3b 3b 73 6e   .... ....;;;;;sn
  0020: 2d 00 3b 3b 3b 3b 3b 02 09 61 72 74 00 01 03 00   -.;;;;;..art....
  0030: 0c 0a 01 02 00 0d 01 00 20                        ........ 
Seed 4 (id=02e04c9299b6e4e1, size=41 bytes, fuzzer=cmplog, trial=1, discovered_at=172s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,ByteAddMutator,TokenReplace):
  0000: 00 95 6b 95 20 24 01 03 00 01 00 40 00 03 00 00   ..k. $.....@....
  0010: e0 20 00 00 00 18 00 00 20 b8 48 b8 b8 b8 b8 b8   . ...... .H.....
  0020: b8 b8 b8 06 02 00 80 20 b8                        ....... .
Seed 5 (id=0456e276e0605002, size=45 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=198s, mutation_op=BytesDeleteMutator,ByteNegMutator,QwordAddMutator,ByteNegMutator,CrossoverReplaceMutator):
  0000: f3 f3 f3 f3 f3 20 20 20 00 18 00 00 00 0e 00 00   .....   ........
  0010: 01 0a 01 00 20 20 00 0f 20 20 01 00 01 0a 01 0d   ....  ..  ......
  0020: 20 20 00 00 00 fd 00 00 01 20 20 20 20              .......    


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0006  00(.)x10 01(.)x4                    00(.)x5 20( )x5 01(.)x2 ee(.)x2 +5u  PARTIAL
   0x0007  00(.)x10 97(.)x2 10(.)x1 ff(.)x1    00(.)x7 20( )x7 ff(.)x2 03(.)x1 +3u  PARTIAL
   0x001e  00(.)x7 03(.)x1 54(T)x1 01(.)x1     00(.)x5 01(.)x2 20( )x1 73(s)x1 +8u  PARTIAL
   0x002e  00(.)x3 dd(.)x1 ff(.)x1 45(E)x1     00(.)x3 20( )x2 03(.)x1 02(.)x1 +7u  PARTIAL
   0x0031  00(.)x4 45(E)x1                     00(.)x2 01(.)x2 10(.)x2 0a(.)x1 +7u  PARTIAL
   0x0032  00(.)x2 dd(.)x1 03(.)x1 45(E)x1     00(.)x7 01(.)x1 0c(.)x1 20( )x1 +4u  PARTIAL
   0x0035  00(.)x2 66(f)x1 45(E)x1             10(.)x3 00(.)x2 20( )x2 01(.)x2 +4u  PARTIAL
   0x0036  ff(.)x1 0a(.)x1 45(E)x1 00(.)x1     00(.)x7 20( )x2 01(.)x1 0c(.)x1 +2u  PARTIAL
   0x0037  ff(.)x1 4a(J)x1 af(.)x1 1a(.)x1     00(.)x6 0c(.)x1 12(.)x1 fe(.)x1 +4u  PARTIAL
   0x0038  8a(.)x1 0f(.)x1 51(Q)x1 1a(.)x1     00(.)x5 1d(.)x2 20( )x1 0c(.)x1 +4u  DIFFER
   0x0039  8a(.)x1 01(.)x1 7e(~)x1 00(.)x1     00(.)x3 43(C)x2 0c(.)x1 0f(.)x1 +4u  PARTIAL
   0x003a  00(.)x2 8a(.)x1 75(u)x1             00(.)x5 20( )x3 ec(.)x1 2c(,)x1 +1u  PARTIAL
   0x003b  20( )x1 ff(.)x1 75(u)x1 00(.)x1     10(.)x3 20( )x2 22(")x1 12(.)x1 +4u  PARTIAL
   0x003c  00(.)x1 f0(.)x1 2d(-)x1 10(.)x1     00(.)x7 01(.)x2 22(")x1 39(9)x1     PARTIAL
   0x003d  8a(.)x1 0e(.)x1 00(.)x1 3a(:)x1     00(.)x5 22(")x1 a0(.)x1 06(.)x1 +3u  PARTIAL
   0x003e  ff(.)x2 fd(.)x1 1a(.)x1             00(.)x6 0e(.)x1 e2(.)x1 06(.)x1 +1u  DIFFER
   0x003f  7f(.)x1 10(.)x1 ff(.)x1 1a(.)x1     12(.)x1 ff(.)x1 17(.)x1 01(.)x1 +6u  PARTIAL
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
  prompts_b/harfbuzz_5989.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5989,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5989 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5989 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5989 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).