==== BLOCKER ====
Target: openthread
Branch ID: 8518
Location: /src/openthread/src/core/thread/mesh_forwarder.cpp:273:13
Enclosing function: ot::MeshForwarder::UpdateEcnOrDrop(ot::Message&, bool)
Source line:             case Ip6::kEcnCapable1:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            6        3          1  REFERENCE
cmplog                           6        4          0  REFERENCE
value_profile                    9        1          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 16  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=3.80h  loser=8.75h
  avg hitcount on branch: winner=6  loser=3
  prob_div=0.70  dur_div=4.95h  hit_div=2
  subject-level: delta_AUC=2557680.0  p_AUC=0.0002  delta_Final=165.0  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
[per-role coverage reports missing/empty — fell back to ±30 source window]
# /src/openthread/src/core/thread/mesh_forwarder.cpp (lines 243-303, blocker at line 273)
    // and returns `kErrorDrop`. This method returns `kErrorNone`
    // when the message is kept as is or ECN field is updated.

    Error    error         = kErrorNone;
    uint32_t timeInQueue   = TimerMilli::GetNow() - aMessage.GetTimestamp();
    bool     shouldMarkEcn = (timeInQueue >= kTimeInQueueMarkEcn);
    bool     isEcnCapable  = false;

    VerifyOrExit(aMessage.IsDirectTransmission() && (aMessage.GetOffset() == 0));

    if (aMessage.GetType() == Message::kTypeIp6)
    {
        Ip6::Header ip6Header;

        IgnoreError(aMessage.Read(0, ip6Header));

        VerifyOrExit(!Get<ThreadNetif>().HasUnicastAddress(ip6Header.GetSource()));

        isEcnCapable = (ip6Header.GetEcn() != Ip6::kEcnNotCapable);

        if ((shouldMarkEcn && !isEcnCapable) || (timeInQueue >= kTimeInQueueDropMsg))
        {
            ExitNow(error = kErrorDrop);
        }

        if (shouldMarkEcn)
        {
            switch (ip6Header.GetEcn())
            {
            case Ip6::kEcnCapable0:
            case Ip6::kEcnCapable1:
                ip6Header.SetEcn(Ip6::kEcnMarked);
                aMessage.Write(0, ip6Header);
                LogMessage(kMessageMarkEcn, aMessage);
                break;

            case Ip6::kEcnMarked:
            case Ip6::kEcnNotCapable:
                break;
            }
        }
    }
#if OPENTHREAD_FTD
    else if (aMessage.GetType() == Message::kType6lowpan)
    {
        uint16_t               headerLength = 0;
        uint16_t               offset;
        bool                   hasFragmentHeader = false;
        Lowpan::FragmentHeader fragmentHeader;
        Lowpan::MeshHeader     meshHeader;

        IgnoreError(meshHeader.ParseFrom(aMessage, headerLength));

        offset = headerLength;

        if (fragmentHeader.ParseFrom(aMessage, offset, headerLength) == kErrorNone)
        {
            hasFragmentHeader = true;
            offset += headerLength;
        }



==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=1959324d29f50233, size=92 bytes, fuzzer=cmplog, trial=3, discovered_at=2508s, mutation_op=QwordAddMutator):
  0000: 32 62 5c a0 80 00 33 00 52 08 80 08 e6 e4 30 74   2b\...3.R.....0t
  0010: 78 30 30 7c 78 8b 04 ff ef fe 80 07 07 f0 ff ff   x00|x...........
  0020: 7c 7c 7c 5f 7c 49 00 98 00 29 05 6d 00 6d 05 7f   |||_|I...).m.m..
  0030: 00 7f 00 00 6d 00 6d 06 78 33 78 33 62 a3 0a 00   ....m.m.x3x3b...
Seed 2 (id=0bbb9c6509642fae, size=92 bytes, fuzzer=cmplog, trial=3, discovered_at=2921s, mutation_op=ByteIncMutator,BytesSetMutator):
  0000: 33 62 5c a0 80 00 33 00 52 fd de ad 00 be ef 00   3b\...3.R.......
  0010: 00 00 00 00 00 fe 00 02 ef fe 80 07 07 f0 ff ff   ................
  0020: 7c 7c 7c 5f 7c 49 01 98 00 29 05 6d 00 6d 05 7f   |||_|I...).m.m..
  0030: 00 7f 00 00 6d 00 6d 06 78 33 78 33 62 a3 0a 00   ....m.m.x3x3b...
Seed 3 (id=2c4b7056b83ab622, size=92 bytes, fuzzer=cmplog, trial=3, discovered_at=3030s, mutation_op=ByteAddMutator,ByteAddMutator,ByteDecMutator,ByteDecMutator):
  0000: 32 62 5c a0 80 00 33 00 52 fd de ad 00 be ef 00   2b\...3.R.......
  0010: 00 00 00 3c b0 fe 00 02 ef ff 80 07 07 f0 ff ff   ...<............
  0020: 7c 7c 7c 5f 7c 49 02 98 fe 29 05 6d 00 6d 05 7f   |||_|I...).m.m..
  0030: 00 7f 00 00 6d 00 6d 06 78 33 78 33 62 a3 6d 00   ....m.m.x3x3b.m.
Seed 4 (id=2224147a05498672, size=92 bytes, fuzzer=cmplog, trial=3, discovered_at=3924s, mutation_op=ByteRandMutator,BytesSwapMutator,ByteInterestingMutator):
  0000: 72 62 5c a0 80 00 33 00 52 fd de ad 00 be ef 00   rb\...3.R.......
  0010: 00 00 00 00 ff fe 00 02 ef fe 80 07 07 f0 ff ff   ................
  0020: 7c 7c 7c 5f 7c 49 01 98 00 29 05 6d 00 6d 05 20   |||_|I...).m.m. 
  0030: 00 7f 00 00 6d 00 6d 06 78 33 78 33 62 a3 0a 00   ....m.m.x3x3b...
Seed 5 (id=26d4464766049521, size=92 bytes, fuzzer=cmplog, trial=3, discovered_at=3927s, mutation_op=BytesDeleteMutator,DwordInterestingMutator,ByteRandMutator,DwordAddMutator,ByteDecMutator):
  0000: 32 62 5c a0 80 00 33 00 52 fd de ad 00 be ef 00   2b\...3.R.......
  0010: 01 00 00 00 ff fe 00 7f 00 fe 80 07 07 f0 ff ff   ................
  0020: 7c 7c 7c 5f 7c 49 00 98 00 29 05 00 00 6d 05 7f   |||_|I...)...m..
  0030: 00 7f 00 00 6d 00 6d 06 78 33 78 33 62 a3 00 00   ....m.m.x3x3b...

==== Loser-blocking seeds (take false branch) ====
[no seeds available — run seed_bisect.py to populate]


==== BYTE DIFF (W vs L at common offsets) ====
[no readable seed bytes on at least one side]

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
  prompts/--RB/03_openthread_8518.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8518,
  "target": "openthread",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8518 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8518 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8518 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).