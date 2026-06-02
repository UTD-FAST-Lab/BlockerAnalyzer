==== BLOCKER ====
Target: bloaty
Branch ID: 301
Location: /src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:659:9
Enclosing function: numbers.cc:absl::(anonymous namespace)::safe_parse_sign_and_base(std::basic_string_view<char, std::char_traits<char> >*, int*, bool*)
Source line:     if (start >= end) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            8        2          0  REFERENCE
cmplog                           4        6          0  REFERENCE
value_profile                    9        1          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)
naive_ctx                        9        1          0  REFERENCE
naive_ngram4                    10        0          0  REFERENCE
mopt                             8        2          0  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             9        1          0  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.70h  loser=18.20h
  avg hitcount on branch: winner=15  loser=2
  prob_div=0.70  dur_div=13.50h  hit_div=13
  subject-level: delta_AUC=49070700.0  p_AUC=0.0002  delta_Final=792.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/bloaty/301/{W,L}/branch_coverage_show.txt

--- Enclosing function: numbers.cc:absl::(anonymous namespace)::safe_parse_sign_and_base(std::basic_string_view<char, std::char_traits<char> >*, int*, bool*) (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:635-700) ---
[ ]   633  inline bool safe_parse_sign_and_base(absl::string_view* text /*inout*/,
[ ]   634                                       int* base_ptr /*inout*/,
[B]   635                                       bool* negative_ptr /*output*/) {
[B]   636    if (text->data() == nullptr) {
[ ]   637      return false;
[ ]   638    }
[ ]   639  
[B]   640    const char* start = text->data();
[B]   641    const char* end = start + text->size();
[B]   642    int base = *base_ptr;
[ ]   643  
[ ]   644    // Consume whitespace.
[B]   645    while (start < end && absl::ascii_isspace(start[0])) {
[B]   646      ++start;
[B]   647    }
[B]   648    while (start < end && absl::ascii_isspace(end[-1])) {
[L]   649      --end;
[L]   650    }
[B]   651    if (start >= end) {
[ ]   652      return false;
[ ]   653    }
[ ]   654  
[ ]   655    // Consume sign.
[B]   656    *negative_ptr = (start[0] == '-');
[B]   657    if (*negative_ptr || start[0] == '+') {
[B]   658      ++start;
[B]   659      if (start >= end) { <-- BLOCKER
[W]   660        return false;
[W]   661      }
[B]   662    }
[ ]   663  
[ ]   664    // Consume base-dependent prefix.
[ ]   665    //  base 0: "0x" -> base 16, "0" -> base 8, default -> base 10
[ ]   666    //  base 16: "0x" -> base 16
[ ]   667    // Also validate the base.
[L]   668    if (base == 0) {
[ ]   669      if (end - start >= 2 && start[0] == '0' &&
[ ]   670          (start[1] == 'x' || start[1] == 'X')) {
[ ]   671        base = 16;
[ ]   672        start += 2;
[ ]   673        if (start >= end) {
[ ]   674          // "0x" with no digits after is invalid.
[ ]   675          return false;
[ ]   676        }
[ ]   677      } else if (end - start >= 1 && start[0] == '0') {
[ ]   678        base = 8;
[ ]   679        start += 1;
[ ]   680      } else {
[ ]   681        base = 10;
[ ]   682      }
[L]   683    } else if (base == 16) {
[ ]   684      if (end - start >= 2 && start[0] == '0' &&
[ ]   685          (start[1] == 'x' || start[1] == 'X')) {
[ ]   686        start += 2;
[ ]   687        if (start >= end) {
[ ]   688          // "0x" with no digits after is invalid.
[ ]   689          return false;
[ ]   690        }
[ ]   691      }
[L]   692    } else if (base >= 2 && base <= 36) {
[ ]   693      // okay
[L]   694    } else {
[ ]   695      return false;
[ ]   696    }
[L]   697    *text = absl::string_view(start, end - start);
[L]   698    *base_ptr = base;
[L]   699    return true;
[L]   700  }

--- No 1-hop callers of numbers.cc:absl::(anonymous namespace)::safe_parse_sign_and_base(std::basic_string_view<char, std::char_traits<char> >*, int*, bool*) fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        24  numbers.cc:bool absl::(anonymous namespace)::safe_parse_positive_int<int>(std::basic_string_view<char, std::char_traits<char> >, int, int*)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:918-950)
       0        24  numbers.cc:bool absl::(anonymous namespace)::safe_parse_positive_int<long>(std::basic_string_view<char, std::char_traits<char> >, int, long*)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:918-950)
       0        24  numbers.cc:bool absl::(anonymous namespace)::safe_parse_positive_int<absl::int128>(std::basic_string_view<char, std::char_traits<char> >, int, absl::int128*)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:918-950)
       0        24  numbers.cc:bool absl::(anonymous namespace)::safe_parse_positive_int<unsigned int>(std::basic_string_view<char, std::char_traits<char> >, int, unsigned int*)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:918-950)
       0        24  numbers.cc:bool absl::(anonymous namespace)::safe_parse_positive_int<unsigned long>(std::basic_string_view<char, std::char_traits<char> >, int, unsigned long*)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:918-950)
       0        24  numbers.cc:bool absl::(anonymous namespace)::safe_parse_positive_int<absl::uint128>(std::basic_string_view<char, std::char_traits<char> >, int, absl::uint128*)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:918-950)
       6        24  numbers.cc:absl::(anonymous namespace)::safe_parse_sign_and_base(std::basic_string_view<char, std::char_traits<char> >*, int*, bool*)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:635-700)  <-- enclosing
       6        24  numbers.cc:bool absl::(anonymous namespace)::safe_uint_internal<unsigned int>(std::basic_string_view<char, std::char_traits<char> >, unsigned int*, int)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:1014-1021)
       6        24  numbers.cc:bool absl::(anonymous namespace)::safe_uint_internal<unsigned long>(std::basic_string_view<char, std::char_traits<char> >, unsigned long*, int)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:1014-1021)
       6        24  numbers.cc:bool absl::(anonymous namespace)::safe_uint_internal<absl::uint128>(std::basic_string_view<char, std::char_traits<char> >, absl::uint128*, int)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:1014-1021)
       6        24  absl::numbers_internal::safe_strtou64_base(std::basic_string_view<char, std::char_traits<char> >, unsigned long*, int)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:1083-1085)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  numbers.cc:absl::(anonymous namespace)::safe_parse_sign_and_base(std::basic_string_view<char, std::char_traits<char> >*, int*, bool*)  (/src/bloaty/third_party/abseil-cpp/absl/strings/numbers.cc:635-700) ---
  d=1   L 636  T=0 F=6  T=0 F=24  if (text->data() == nullptr) {
  d=1   L 645  T=60 F=0  T=126 F=0  while (start < end && absl::ascii_isspace(start[0])) {
  d=1   L 645  T=54 F=6  T=102 F=24  while (start < end && absl::ascii_isspace(start[0])) {
  d=1   L 648  T=6 F=0  T=36 F=0  while (start < end && absl::ascii_isspace(end[-1])) {
  d=1   L 648  T=0 F=6  T=12 F=24  while (start < end && absl::ascii_isspace(end[-1])) {
  d=1   L 651  T=0 F=6  T=0 F=24  if (start >= end) {
  d=1   L 657  T=0 F=0  T=12 F=12  if (*negative_ptr || start[0] == '+') {
  d=1   L 657  T=6 F=0  T=0 F=24  if (*negative_ptr || start[0] == '+') {
  d=1   L 659  T=6 F=0  T=0 F=12  if (start >= end) {  <-- BLOCKER
  d=1   L 668  T=0 F=0  T=0 F=24  if (base == 0) {
  d=1   L 683  T=0 F=0  T=0 F=24  } else if (base == 16) {
  d=1   L 692  T=0 F=0  T=24 F=0  } else if (base >= 2 && base <= 36) {
  d=1   L 692  T=0 F=0  T=24 F=0  } else if (base >= 2 && base <= 36) {

[off-chain: 6 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=431fd8feaed6a59a, size=117 bytes, fuzzer=value_profile, trial=4, discovered_at=22357s, mutation_op=BitFlipMutator,ByteInterestingMutator,ByteRandMutator,BytesSetMutator,BytesDeleteMutator,BytesSetMutator,CrossoverInsertMutator):
  0000: 21 3c 61 72 63 68 3e 0a 2b 2b 2b 2b 2b 01 01 01   !<arch>.+++++...
  0010: 01 01 01 01 00 00 02 01 01 01 ff 01 01 2b 2b 2b   .............+++
  0020: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 33 ff 02 01   ++++++++++++3...
  0030: ff ff 7f 00 ff 00 2d 00 0a 0a 0a 0a 0a 0a 0a 0a   ......-.........

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=40c07ad1f6818e08, size=147 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5817s, mutation_op=BytesInsertMutator,ByteAddMutator,ByteIncMutator,WordInterestingMutator,CrossoverReplaceMutator,BytesSwapMutator,DwordAddMutator):
  0000: 21 3c 61 72 63 68 3e 0a 00 65 6c 66 20 2d 34 34   !<arch>..elf -44
  0010: 34 34 34 34 34 34 30 02 00 20 20 25 20 20 20 20   4444440..  %    
  0020: ea ea ea ea c7 00 00 01 00 00 20 20 20 20 20 20   ..........      
  0030: 20 20 20 20 20 20 20 20 20 20 20 20 20 2b 34 34                +44
Seed 2 (id=000b869d4daa55f7, size=256 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=39354s, mutation_op=ByteRandMutator,BytesExpandMutator,DwordInterestingMutator,ByteIncMutator):
  0000: 21 3c 61 72 63 68 3e 0a 00 65 bd bd b4 bd bd bd   !<arch>..e......
  0010: bd bd bd bd 34 34 34 2f 92 7f 46 4c e6 01 02 00   ....444/..FL....
  0020: 20 20 20 20 20 20 20 ea ea ea ea ea ff 18 2d ff          .......-.
  0030: ff 20 20 20 20 20 20 20 20 20 20 20 20 20 30 30   .             00


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0008  2b(+)x1                             00(.)x2                             DIFFER
   0x0009  2b(+)x1                             65(e)x2                             DIFFER
   0x000a  2b(+)x1                             6c(l)x1 bd(.)x1                     DIFFER
   0x000b  2b(+)x1                             66(f)x1 bd(.)x1                     DIFFER
   0x000c  2b(+)x1                             20( )x1 b4(.)x1                     DIFFER
   0x000d  01(.)x1                             2d(-)x1 bd(.)x1                     DIFFER
   0x000e  01(.)x1                             34(4)x1 bd(.)x1                     DIFFER
   0x000f  01(.)x1                             34(4)x1 bd(.)x1                     DIFFER
   0x0010  01(.)x1                             34(4)x1 bd(.)x1                     DIFFER
   0x0011  01(.)x1                             34(4)x1 bd(.)x1                     DIFFER
   0x0012  01(.)x1                             34(4)x1 bd(.)x1                     DIFFER
   0x0013  01(.)x1                             34(4)x1 bd(.)x1                     DIFFER
   0x0014  00(.)x1                             34(4)x2                             DIFFER
   0x0015  00(.)x1                             34(4)x2                             DIFFER
   0x0016  02(.)x1                             30(0)x1 34(4)x1                     DIFFER
   0x0017  01(.)x1                             02(.)x1 2f(/)x1                     DIFFER
   0x0018  01(.)x1                             00(.)x1 92(.)x1                     DIFFER
   0x0019  01(.)x1                             20( )x1 7f(.)x1                     DIFFER
   0x001a  ff(.)x1                             20( )x1 46(F)x1                     DIFFER
   0x001b  01(.)x1                             25(%)x1 4c(L)x1                     DIFFER
   0x001c  01(.)x1                             20( )x1 e6(.)x1                     DIFFER
   0x001d  2b(+)x1                             20( )x1 01(.)x1                     DIFFER
   0x001e  2b(+)x1                             20( )x1 02(.)x1                     DIFFER
   0x001f  2b(+)x1                             20( )x1 00(.)x1                     DIFFER
   0x0020  2b(+)x1                             ea(.)x1 20( )x1                     DIFFER
   0x0021  2b(+)x1                             ea(.)x1 20( )x1                     DIFFER
   0x0022  2b(+)x1                             ea(.)x1 20( )x1                     DIFFER
   0x0023  2b(+)x1                             ea(.)x1 20( )x1                     DIFFER
   0x0024  2b(+)x1                             c7(.)x1 20( )x1                     DIFFER
   0x0025  2b(+)x1                             00(.)x1 20( )x1                     DIFFER
   0x0026  2b(+)x1                             00(.)x1 20( )x1                     DIFFER
   0x0027  2b(+)x1                             01(.)x1 ea(.)x1                     DIFFER
   0x0028  2b(+)x1                             00(.)x1 ea(.)x1                     DIFFER
   0x0029  2b(+)x1                             00(.)x1 ea(.)x1                     DIFFER
   0x002a  2b(+)x1                             20( )x1 ea(.)x1                     DIFFER
   0x002b  2b(+)x1                             20( )x1 ea(.)x1                     DIFFER
   0x002c  33(3)x1                             20( )x1 ff(.)x1                     DIFFER
   0x002d  ff(.)x1                             20( )x1 18(.)x1                     DIFFER
   0x002e  02(.)x1                             20( )x1 2d(-)x1                     DIFFER
   0x002f  01(.)x1                             20( )x1 ff(.)x1                     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/bloaty_301.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 301,
  "target": "bloaty",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 301 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 301 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 301 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).