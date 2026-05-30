==== BLOCKER ====
Target: libpng
Branch ID: 4145
Location: /src/libpng/png.c:1809:36
Enclosing function: png.c:is_ICC_signature_char
Source line:    return it == 32 || (it >= 48 && it <= 57) || (it >= 65 && it <= 90) ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        0         10  REFERENCE
cmplog                           0        9          1  loser (value_profile vs value_profile_cmplog)
value_profile                    6        1          3  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 23  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=9  unreached=1
  avg duration blocked: winner=2.80h  loser=18.78h
  avg hitcount on branch: winner=9  loser=0
  prob_div=0.90  dur_div=15.98h  hit_div=9
  subject-level: delta_AUC=7265340.0  p_AUC=0.0003  delta_Final=83.1  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/4145/{W,L}/branch_coverage_show.txt

--- Enclosing function: png.c:is_ICC_signature_char (/src/libpng/png.c:1808-1811) ---
[ ]  1806  static int
[ ]  1807  is_ICC_signature_char(png_alloc_size_t it)
[B]  1808  {
[B]  1809     return it == 32 || (it >= 48 && it <= 57) || (it >= 65 && it <= 90) || <-- BLOCKER
[B]  1810        (it >= 97 && it <= 122);
[B]  1811  }

--- Caller (1 hop): png.c:is_ICC_signature (/src/libpng/png.c:1815-1820, calls png.c:is_ICC_signature_char at line 1816) (full body — short) ---
[B]  1815  {
[B]  1816     return is_ICC_signature_char(it >> 24) /* checks all the top bits */ && <-- CALL
[B]  1817        is_ICC_signature_char((it >> 16) & 0xff) &&
[B]  1818        is_ICC_signature_char((it >> 8) & 0xff) &&
[B]  1819        is_ICC_signature_char(it & 0xff);
[B]  1820  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  png.c:is_ICC_signature  (/src/libpng/png.c:1815-1820, calls png.c:is_ICC_signature_char at line 1816)
hop 3  png.c:png_icc_profile_error  (/src/libpng/png.c:1825-1867, calls png.c:is_ICC_signature at line 1835)
hop 4  OSS_FUZZ_png_colorspace_set_sRGB  (/src/libpng/png.c:1874-1957, calls png.c:png_icc_profile_error at line 1909)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      65       209  OSS_FUZZ_png_get_io_ptr  (/src/libpng/png.c:687-692)
      47       142  OSS_FUZZ_png_calculate_crc  (/src/libpng/png.c:140-187)
      18        67  OSS_FUZZ_png_reset_crc  (/src/libpng/png.c:128-131)
      12        60  OSS_FUZZ_png_handle_as_unknown  (/src/libpng/png.c:927-956)
      12        60  OSS_FUZZ_png_chunk_unknown_handling  (/src/libpng/png.c:962-967)
       0         8  OSS_FUZZ_png_colorspace_sync_info  (/src/libpng/png.c:1170-1211)
       0         8  OSS_FUZZ_png_colorspace_sync  (/src/libpng/png.c:1216-1222)
       0         6  png.c:png_colorspace_check_gamma  (/src/libpng/png.c:1081-1111)
       0         6  OSS_FUZZ_png_colorspace_set_gamma  (/src/libpng/png.c:1116-1166)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  png.c:is_ICC_signature_char  (/src/libpng/png.c:1808-1811) ---
  d=1   L1809  T=8 F=16  T=0 F=24  return it == 32 || (it >= 48 && it <= 57) || (it >= 65 &&...  <-- BLOCKER

[off-chain: 23 additional divergent branches across 8 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=118a8977ecc28704, size=1827 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=9571s, mutation_op=BytesInsertCopyMutator,BytesSetMutator,CrossoverReplaceMutator,ByteAddMutator,BytesInsertMutator,ByteInterestingMutator,BytesInsertCopyMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 45 45 45 45 45 45 45 45 45   .....gAEEEEEEEEE
  0030: 45 45 45 45 01 69 43 43 50 01 d9 31 31 31 31 31   EEEE.iCCP..11111
Seed 2 (id=443ac0ca763587fd, size=1798 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=9571s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator,BytesExpandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 45 45 45 45 45 45 45 45 45   .....gAEEEEEEEEE
  0030: 45 45 45 45 01 69 43 43 50 01 d9 31 31 31 31 31   EEEE.iCCP..11111
Seed 3 (id=505622ff752238ae, size=1822 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=9613s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator,WordAddMutator,BytesSwapMutator,BytesDeleteMutator,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 45 45 45 45 45 45 45 45 45   .....gAEEEEEEEEE
  0030: 45 45 45 45 01 69 43 43 50 01 d9 31 31 31 31 31   EEEE.iCCP..11111
Seed 4 (id=d701c13694d875e6, size=2276 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=9778s, mutation_op=ByteAddMutator,CrossoverInsertMutator,BytesDeleteMutator,BytesRandSetMutator,BytesInsertMutator,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 45 45 45 45 45 45 45 45 45   .....gAEEEEEEEEE
  0030: 45 45 45 45 01 69 43 43 50 01 d9 31 31 31 31 31   EEEE.iCCP..11111
Seed 5 (id=50f98ddb72a155f4, size=1845 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=17365s, mutation_op=BytesRandSetMutator,BytesCopyMutator,BytesInsertMutator,BytesInsertMutator,BytesSwapMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 45 45 45 45 45 45 45 45 45   .....gAEEEEEEEEE
  0030: 45 45 45 45 01 69 43 43 50 01 d9 31 31 31 31 31   EEEE.iCCP..11111

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=c7492b31f4f7e961, size=1492 bytes, fuzzer=cmplog, trial=1, discovered_at=5439s, mutation_op=ByteInterestingMutator,CrossoverInsertMutator,WordInterestingMutator,TokenInsert,BytesInsertCopyMutator,WordInterestingMutator,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 2 (id=bea073a062f92b7f, size=4870 bytes, fuzzer=cmplog, trial=1, discovered_at=5465s, mutation_op=QwordAddMutator,BytesExpandMutator,CrossoverInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 3 (id=1b45f30bf07bbd72, size=1544 bytes, fuzzer=cmplog, trial=1, discovered_at=9777s, mutation_op=ByteNegMutator,ByteNegMutator,ByteFlipMutator,ByteAddMutator,CrossoverInsertMutator,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 4 (id=aef7419be2d8cb2e, size=1559 bytes, fuzzer=cmplog, trial=1, discovered_at=9834s, mutation_op=BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...
Seed 5 (id=109d1e25e2e5a747, size=2221 bytes, fuzzer=cmplog, trial=1, discovered_at=23169s, mutation_op=CrossoverInsertMutator,WordAddMutator,WordInterestingMutator,ByteIncMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 69 54 58 74 01 d9 c9 2c 7f 00 00   .....iTXt...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0027  45(E)x6                             4d(M)x6                             DIFFER
   0x0028  45(E)x6                             41(A)x6                             DIFFER
   0x0029  45(E)x6                             00(.)x6                             DIFFER
   0x002a  45(E)x6                             00(.)x6                             DIFFER
   0x002b  45(E)x6                             b1(.)x6                             DIFFER
   0x002c  45(E)x6                             8f(.)x6                             DIFFER
   0x002d  45(E)x6                             0b(.)x6                             DIFFER
   0x002e  45(E)x6                             fc(.)x6                             DIFFER
   0x002f  45(E)x6                             61(a)x6                             DIFFER
   0x0030  45(E)x6                             05(.)x6                             DIFFER
   0x0031  45(E)x6                             00(.)x6                             DIFFER
   0x0032  45(E)x6                             00(.)x6                             DIFFER
   0x0033  45(E)x6                             00(.)x6                             DIFFER
   0x0036  43(C)x6                             54(T)x6                             DIFFER
   0x0037  43(C)x6                             58(X)x6                             DIFFER
   0x0038  50(P)x6                             74(t)x6                             DIFFER
   0x003b  31(1)x6                             c9(.)x6                             DIFFER
   0x003c  31(1)x6                             2c(,)x6                             DIFFER
   0x003d  31(1)x6                             7f(.)x6                             DIFFER
   0x003e  31(1)x6                             00(.)x6                             DIFFER
   0x003f  31(1)x6                             00(.)x6                             DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libpng_4145.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 4145,
  "target": "libpng",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 4145 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 4145 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 4145 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).