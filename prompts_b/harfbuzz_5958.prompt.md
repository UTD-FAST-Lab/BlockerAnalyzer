==== BLOCKER ====
Target: harfbuzz
Branch ID: 5958
Location: /src/harfbuzz/src/hb-ot-shaper-thai.cc:57:23
Enclosing function: hb-ot-shaper-thai.cc:get_consonant_type(unsigned int)
Source line:   if (u == 0x0E0Eu || u == 0x0E0Fu)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive); loser (grimoire_structural vs grimoire)
value_profile                   10        0          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         9        1          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (3) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=2.50h  loser=20.10h
  avg hitcount on branch: winner=26  loser=0
  prob_div=0.90  dur_div=17.60h  hit_div=26
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002
--- Pair 2: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 14  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=2.80h  loser=17.30h
  avg hitcount on branch: winner=16  loser=0
  prob_div=0.80  dur_div=14.50h  hit_div=15
  subject-level: delta_AUC=128766960.0  p_AUC=0.0002  delta_Final=2136.4  p_final=0.0002
--- Pair 3: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 20  (grimoire vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=9.80h  loser=20.10h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=10.30h  hit_div=3
  subject-level: delta_AUC=45443160.0  p_AUC=0.001  delta_Final=636.4  p_final=0.0006

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5958/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-thai.cc:get_consonant_type(unsigned int) (/src/harfbuzz/src/hb-ot-shaper-thai.cc:52-62) ---
[ ]    50  static thai_consonant_type_t
[ ]    51  get_consonant_type (hb_codepoint_t u)
[B]    52  {
[B]    53    if (u == 0x0E1Bu || u == 0x0E1Du || u == 0x0E1Fu/* || u == 0x0E2Cu*/)
[W]    54      return AC;
[B]    55    if (u == 0x0E0Du || u == 0x0E10u)
[B]    56      return RC;
[B]    57    if (u == 0x0E0Eu || u == 0x0E0Fu) <-- BLOCKER
[B]    58      return DC;
[B]    59    if (hb_in_range<hb_codepoint_t> (u, 0x0E01u, 0x0E2Eu))
[L]    60      return NC;
[B]    61    return NOT_CONSONANT;
[B]    62  }

--- Caller (1 hop): hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) (/src/harfbuzz/src/hb-ot-shaper-thai.cc:224-261, calls hb-ot-shaper-thai.cc:get_consonant_type(unsigned int) at line 240) (full body — short) ---
[B]   224  {
[ ]   225  #ifdef HB_NO_OT_SHAPER_THAI_FALLBACK
[ ]   226    return;
[ ]   227  #endif
[ ]   228  
[B]   229    thai_above_state_t above_state = thai_above_start_state[NOT_CONSONANT];
[B]   230    thai_below_state_t below_state = thai_below_start_state[NOT_CONSONANT];
[B]   231    unsigned int base = 0;
[ ]   232  
[B]   233    hb_glyph_info_t *info = buffer->info;
[B]   234    unsigned int count = buffer->len;
[B]   235    for (unsigned int i = 0; i < count; i++)
[B]   236    {
[B]   237      thai_mark_type_t mt = get_mark_type (info[i].codepoint);
[ ]   238  
[B]   239      if (mt == NOT_MARK) {
[B]   240        thai_consonant_type_t ct = get_consonant_type (info[i].codepoint); <-- CALL
[B]   241        above_state = thai_above_start_state[ct];
[B]   242        below_state = thai_below_start_state[ct];
[B]   243        base = i;
[B]   244        continue;
[B]   245      }
[ ]   246  
[B]   247      const thai_above_state_machine_edge_t &above_edge = thai_above_state_machine[above_state][mt];
[B]   248      const thai_below_state_machine_edge_t &below_edge = thai_below_state_machine[below_state][mt];
[B]   249      above_state = above_edge.next_state;
[B]   250      below_state = below_edge.next_state;
[ ]   251  
[ ]   252      /* At least one of the above/below actions is NOP. */
[B]   253      thai_action_t action = above_edge.action != NOP ? above_edge.action : below_edge.action;
[ ]   254  
[B]   255      buffer->unsafe_to_break (base, i);
[B]   256      if (action == RD)
[W]   257        info[base].codepoint = thai_pua_shape (info[base].codepoint, action, font);
[B]   258      else
[B]   259        info[i].codepoint = thai_pua_shape (info[i].codepoint, action, font);
[B]   260    }
[B]   261  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:224-261, calls hb-ot-shaper-thai.cc:get_consonant_type(unsigned int) at line 240)
hop 3  hb-ot-shaper-thai.cc:preprocess_text_thai(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:268-372, calls hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*) at line 371)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-thai.cc:do_thai_pua_shaping(hb_ot_shape_plan_t const*, hb_buffer_t*, hb_font_t*)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:224-261) ---
  d=2   L 253  T=10 F=35  T=0 F=25  thai_action_t action = above_edge.action != NOP ? above_e...
  d=2   L 256  T=1 F=44  T=0 F=25  if (action == RD)
--- d=1  hb-ot-shaper-thai.cc:get_consonant_type(unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-thai.cc:52-62) ---
  d=1   L  53  T=4 F=400  T=0 F=298  if (u == 0x0E1Bu || u == 0x0E1Du || u == 0x0E1Fu/* || u =...
  d=1   L  53  T=2 F=404  T=0 F=298  if (u == 0x0E1Bu || u == 0x0E1Du || u == 0x0E1Fu/* || u =...
  d=1   L  55  T=9 F=391  T=0 F=298  if (u == 0x0E0Du || u == 0x0E10u)
  d=1   L  59  T=0 F=339  T=6 F=288  if (hb_in_range<hb_codepoint_t> (u, 0x0E01u, 0x0E2Eu))

[off-chain: 7 additional divergent branches across 1 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=5b2413d884cc2bab, size=7 bytes, fuzzer=value_profile, trial=1, discovered_at=36s, mutation_op=BytesExpandMutator,BytesDeleteMutator,BytesExpandMutator,BytesDeleteMutator):
  0000: 0f 0e 00 00 00 00 00                              .......
Seed 2 (id=d50e787269a5c51d, size=44 bytes, fuzzer=grimoire, trial=1, discovered_at=281s):
  0000: 6d 61 54 ff 0f 0e 00 00 03 61 54 ff 0f 0e 00 00   maT......aT.....
  0010: 16 01 00 b0 14 01 00 20 00 20 20 20 00 00 10 20   ....... .   ... 
  0020: 20 20 f9 ff 6e 74 61 6c 68 63 74 73                 ..ntalhcts
Seed 3 (id=3e996636433d9f07, size=55 bytes, fuzzer=grimoire, trial=1, discovered_at=334s):
  0000: 61 6e 69 66 ba 14 07 ff ff 08 01 70 61 74 69 62   anif.......patib
  0010: 6c fb fb 2c 12 01 00 f0 47 0e 00 00 01 04 00 02   l..,....G.......
  0020: 03 01 00 00 72 74 2d 6c 6f 01 00 69 64 65 6d 1d   ....rt-lo..idem.
  0030: fa 02 00 ff 0f 0e 00                              .......
Seed 4 (id=62e5ed8618b6203c, size=48 bytes, fuzzer=naive, trial=1, discovered_at=347s, mutation_op=WordAddMutator,BytesSetMutator,ByteFlipMutator):
  0000: 98 cb 0d 4e 0d 0e 00 00 4b 0e 00 00 0f 0e 00 00   ...N....K.......
  0010: 1e fa 02 00 ff ff ff ff 92 92 b3 cb cb 92 cb 92   ................
  0020: 92 6f 92 b0 64 7f c2 7a 6f d2 92 92 92 97 00 4c   .o..d..zo......L
Seed 5 (id=cf5020d01c7394ae, size=38 bytes, fuzzer=naive, trial=1, discovered_at=400s, mutation_op=BytesDeleteMutator,WordAddMutator,ByteRandMutator,CrossoverReplaceMutator,ByteNegMutator):
  0000: 98 cb 0d 4e 0d 0e 00 00 4b 0e 85 00 0f 0e 00 00   ...N....K.......
  0010: 1e fa 02 00 ff ff ff 01 92 92 64 6a c2 7a 6f 2c   ..........dj.zo,
  0020: 92 92 92 97 00 4c                                 .....L

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=20713fe6e4ea6e0a, size=30 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=64s, mutation_op=CrossoverReplaceMutator,BytesInsertCopyMutator,BytesCopyMutator):
  0000: 01 00 65 65 65 cb cb 35 01 0e 00 1a 03 03 00 65   ..eee..5.......e
  0010: 65 65 cb cb 35 01 01 00 20 20 20 20 01 0e         ee..5...    ..
Seed 2 (id=37f8e71ac2ac9677, size=21 bytes, fuzzer=cmplog, trial=1, discovered_at=163s, mutation_op=BytesInsertCopyMutator):
  0000: 05 0d 01 74 05 0d 01 74 ba c0 22 06 38 0e 00 00   ...t...t..".8...
  0010: 00 00 ff 40 20                                    ...@ 
Seed 3 (id=0568144a6b4b248e, size=57 bytes, fuzzer=cmplog, trial=1, discovered_at=246s, mutation_op=TokenInsert,QwordAddMutator,BytesSetMutator,ByteInterestingMutator,TokenInsert,WordAddMutator,WordAddMutator):
  0000: 00 01 40 9b 14 01 20 6e 6e 00 1b 1b 1b 1b 1b 1b   ..@... nn.......
  0010: 1b 1b 70 67 6c 73 1b 1b 20 20 20 6b 34 0e 00 00   ..pgls..   k4...
  0020: 05 65 72 6f 25 49 92 04 20 00 1b 1b 1b ff ff fb   .ero%I.. .......
  0030: 01 00 04 dd 0f 0e 00 00 05                        .........
Seed 4 (id=12c176717291bd3c, size=61 bytes, fuzzer=cmplog, trial=1, discovered_at=246s, mutation_op=WordInterestingMutator,ByteAddMutator,BytesRandInsertMutator):
  0000: 00 01 40 9b ff ff ff 1f 6e 1b 1b 1b 1b 1b 1b 1b   ..@.....n.......
  0010: 1b 1b 1b 1b 20 20 20 60 08 0e 00 00 05 65 72 6f   ....   `.....ero
  0020: 20 00 0f 20 cd cd cd cd ea 6e 70 2d 68 61 6e 74    .. .....np-hant
  0030: 00 ff ff fb 00 00 04 00 10 0e 00 00 05            .............
Seed 5 (id=06f6941f312fc011, size=54 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=249s, mutation_op=BytesSwapMutator,BytesSetMutator,ByteIncMutator,BytesSetMutator,BitFlipMutator,WordInterestingMutator):
  0000: ff ff 20 3f 33 0e 00 00 01 e3 38 8e 03 20 3f 72   .. ?3.....8.. ?r
  0010: ff ff ff 20 20 00 00 00 3a 6b 20 3f 33 80 ff 00   ...  ...:k ?3...
  0020: 66 ff 7d 65 65 3a 6b 66 73 6e 20 00 1d 20 8e 8e   f.}ee:kfsn .. ..
  0030: 8e 8e 11 11 11 11                                 ......


==== BYTE DIFF (W vs L at common offsets) ====
[no informative byte-level divergence — seeds look structurally similar across W and L at every offset, OR diverge only at high-entropy positions (noise)]

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
  prompts_b/harfbuzz_5958.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5958,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S), value_profile>value_profile_cmplog (I2S), grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5958 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5958 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5958 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).