==== BLOCKER ====
Target: curl
Branch ID: 353
Location: /src/curl/lib/progress.c:354:6
Enclosing function: Curl_pgrsSetDownloadSize
Source line:   if(size >= 0) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           7        3          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=9.00h  loser=24.00h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.90  dur_div=15.00h  hit_div=2
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/353/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_pgrsSetDownloadSize (/src/curl/lib/progress.c:353-362) ---
[ ]   351  
[ ]   352  void Curl_pgrsSetDownloadSize(struct Curl_easy *data, curl_off_t size)
[B]   353  {
[B]   354    if(size >= 0) { <-- BLOCKER
[W]   355      data->progress.size_dl = size;
[W]   356      data->progress.flags |= PGRS_DL_SIZE_KNOWN;
[W]   357    }
[B]   358    else {
[B]   359      data->progress.size_dl = 0;
[B]   360      data->progress.flags &= ~PGRS_DL_SIZE_KNOWN;
[B]   361    }
[B]   362  }

--- Caller (1 hop): Curl_http_size (/src/curl/lib/http.c:3852-3867, calls Curl_pgrsSetDownloadSize at line 3863) (full body — short) ---
[W]  3852  {
[W]  3853    struct SingleRequest *k = &data->req;
[W]  3854    if(data->req.ignore_cl || k->chunk) {
[ ]  3855      k->size = k->maxdownload = -1;
[ ]  3856    }
[W]  3857    else if(k->size != -1) {
[W]  3858      if(data->set.max_filesize &&
[W]  3859         k->size > data->set.max_filesize) {
[ ]  3860        failf(data, "Maximum file size exceeded");
[ ]  3861        return CURLE_FILESIZE_EXCEEDED;
[ ]  3862      }
[W]  3863      Curl_pgrsSetDownloadSize(data, k->size); <-- CALL
[W]  3864      k->maxdownload = k->size;
[W]  3865    }
[W]  3866    return CURLE_OK;
[W]  3867  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  file.c:file_do  (/src/curl/lib/file.c:392-574, calls Curl_pgrsSetDownloadSize at line 479)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      18       126  progress.c:trspeed  (/src/curl/lib/progress.c:379-388)
       9        63  progress.c:progress_calc  (/src/curl/lib/progress.c:392-460)
       9        63  Curl_pgrsUpdate  (/src/curl/lib/progress.c:579-621)
       6        48  Curl_pgrsTime  (/src/curl/lib/progress.c:175-237)
       7        46  Curl_checkheaders  (/src/curl/lib/transfer.c:102-114)
       2        17  Curl_pgrsSetUploadSize  (/src/curl/lib/progress.c:365-374)
       2        14  Curl_pgrsSetUploadCounter  (/src/curl/lib/progress.c:348-350)
       1        10  Curl_pgrsResetTransferSizes  (/src/curl/lib/progress.c:162-165)
       1        10  Curl_pgrsStartNow  (/src/curl/lib/progress.c:240-253)
       1        10  Curl_ratelimit  (/src/curl/lib/progress.c:326-342)
       1        10  Curl_init_CONNECT  (/src/curl/lib/transfer.c:1392-1395)
       1        10  Curl_pretransfer  (/src/curl/lib/transfer.c:1403-1541)
       1        10  Curl_posttransfer  (/src/curl/lib/transfer.c:1547-1557)
       2        10  Curl_pgrsSetDownloadSize  (/src/curl/lib/progress.c:353-362)  <-- enclosing
       1         7  http.c:http_setup_conn  (/src/curl/lib/http.c:234-264)
... (40 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  Curl_pgrsSetDownloadSize  (/src/curl/lib/progress.c:353-362) ---
  d=1   L 354  T=1 F=1  T=0 F=10  if(size >= 0) {  <-- BLOCKER

[off-chain: 431 additional divergent branches across 47 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c2dff1c31a6fa435, size=130 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=67564s, mutation_op=CrossoverReplaceMutator):
  0000: 00 01 00 00 00 19 70 00 70 33 3a 2f 2f 31 32 37   ......p.p3://127
  0010: 2e 2f 2e 30 2e 31 3a 39 30 30 31 72 38 35 30 00   ./.0.1:9001r850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 65 6f   ....GHTTP/ me@eo
  0030: 6d 65 77 68 65 72 65 0d 0a 43 6f 6e 74 65 6e 74   mewhere..Content

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00225bc4819174d2, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=152s, mutation_op=BytesInsertMutator,ByteAddMutator,ByteIncMutator,BytesDeleteMutator,ByteDecMutator):
  0000: 00 01 00 00 00 43 64 55 43 25 25 25 25 21 25 65   .....CdUC%%%%!%e
  0010: 26 25 65 24 25 64 45 72 46 25 41 27 25 31 25 25   &%e$%dErF%A'%1%%
  0020: 65 25 44 d6 42 64 45 72 33 25 65 4b 25 43 25 25   e%D.BdEr3%eK%C%%
  0030: 25 25 25 25 25 25 25 25 25 25 25 25 26 25 40 e8   %%%%%%%%%%%%&%@.
Seed 2 (id=002bcaf632e31c2a, size=36 bytes, fuzzer=value_profile, trial=1, discovered_at=2534s, mutation_op=TokenReplace,BytesCopyMutator,ByteDecMutator,BytesSetMutator,BytesSetMutator):
  0000: 00 01 00 00 00 19 2d 70 2e 2e 2e 2d 2e 2e 2d 70   ......-p...-..-p
  0010: 2e 2e 2e 2e 3e 3e 42 0f 00 2e 2e 2e 2e 2e 2e 2e   ....>>B.........
  0020: 2e 2e 2e 2e                                       ....
Seed 3 (id=001607afc7f08ce7, size=74 bytes, fuzzer=value_profile, trial=1, discovered_at=3913s, mutation_op=BytesCopyMutator):
  0000: 00 01 00 00 00 44 64 55 43 db b5 25 45 66 25 66   .....DdUC..%Ef%f
  0010: 42 62 9e 62 9e 44 64 55 43 db b5 25 45 66 25 66   Bb.b.DdUC..%Ef%f
  0020: 42 62 9e 62 9e 43 41 27 db 31 25 25 25 25 26 55   Bb.b.CA'.1%%%%&U
  0030: 43 db b5 25 45 66 25 65 42 62 9e 66 52 66 25 65   C..%Ef%eBb.fRf%e
Seed 4 (id=00224975860e7d7e, size=36 bytes, fuzzer=value_profile, trial=1, discovered_at=4107s, mutation_op=DwordAddMutator,QwordAddMutator,CrossoverReplaceMutator):
  0000: 00 01 00 00 00 19 2e 2d 2b 47 2b 2b 2b 2e 4e 51   .......-+G+++.NQ
  0010: 37 2b 2b 2d 2b 2e 4e 41 59 2b 38 2d 2b 2e 46 25   7++-+.NAY+8-+.F%
  0020: 21 00 00 8d                                       !...
Seed 5 (id=001ce769b822a341, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=22931s, mutation_op=BytesCopyMutator):
  0000: 00 01 00 00 00 2e 2e 2e 2e 2b 2e 2d 2e 2e 2e 2e   .........+.-....
  0010: 2e 2d 6e 2e 2e 2d 6d 2e 2e 2d 6e 2e 2e 2d 6d 2e   .-n..-m..-n..-m.
  0020: 2e 2d 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e   .-..............
  0030: 2e 2e 2e 2e 2e 4f 4e 11 80                        .....ON..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x1                             43(C)x4 19(.)x2 44(D)x1 2e(.)x1 +2u  PARTIAL
   0x0006  70(p)x1                             64(d)x3 25(%)x3 2e(.)x2 2d(-)x1 +1u  DIFFER
   0x0007  00(.)x1                             55(U)x2 62(b)x2 70(p)x1 2d(-)x1 +4u  DIFFER
   0x0008  70(p)x1                             43(C)x3 2e(.)x2 2b(+)x1 25(%)x1 +3u  DIFFER
   0x0009  33(3)x1                             25(%)x2 2e(.)x1 db(.)x1 47(G)x1 +5u  DIFFER
   0x000a  3a(:)x1                             25(%)x3 2e(.)x2 b5(.)x1 2b(+)x1 +3u  DIFFER
   0x000b  2f(/)x1                             25(%)x3 2d(-)x2 2b(+)x1 bd(.)x1 +3u  DIFFER
   0x000c  2f(/)x1                             25(%)x3 2e(.)x2 45(E)x1 2b(+)x1 +3u  DIFFER
   0x000d  31(1)x1                             2e(.)x3 64(d)x2 21(!)x1 66(f)x1 +3u  PARTIAL
   0x000e  32(2)x1                             25(%)x6 2d(-)x1 4e(N)x1 2e(.)x1 +1u  DIFFER
   0x000f  37(7)x1                             65(e)x1 70(p)x1 66(f)x1 51(Q)x1 +6u  DIFFER
   0x0010  2e(.)x1                             2e(.)x2 42(B)x2 26(&)x1 37(7)x1 +4u  PARTIAL
   0x0011  2f(/)x1                             25(%)x4 2e(.)x1 62(b)x1 2b(+)x1 +3u  DIFFER
   0x0012  2e(.)x1                             65(e)x1 2e(.)x1 9e(.)x1 2b(+)x1 +6u  PARTIAL
   0x0013  30(0)x1                             2e(.)x2 62(b)x2 24($)x1 2d(-)x1 +4u  DIFFER
   0x0014  2e(.)x1                             25(%)x2 61(a)x2 3e(>)x1 9e(.)x1 +4u  PARTIAL
   0x0015  31(1)x1                             25(%)x2 64(d)x1 3e(>)x1 44(D)x1 +5u  DIFFER
   0x0016  3a(:)x1                             64(d)x3 45(E)x1 42(B)x1 4e(N)x1 +4u  DIFFER
   0x0017  39(9)x1                             72(r)x1 0f(.)x1 55(U)x1 41(A)x1 +6u  DIFFER
   0x0018  30(0)x1                             46(F)x1 00(.)x1 43(C)x1 59(Y)x1 +6u  DIFFER
   0x0019  30(0)x1                             25(%)x2 2e(.)x1 db(.)x1 2b(+)x1 +5u  DIFFER
   0x001a  31(1)x1                             41(A)x2 66(f)x2 2e(.)x1 b5(.)x1 +4u  DIFFER
   0x001b  72(r)x1                             25(%)x3 2e(.)x2 27(')x1 2d(-)x1 +3u  DIFFER
   0x001c  38(8)x1                             2e(.)x2 25(%)x1 45(E)x1 2b(+)x1 +5u  DIFFER
   0x001d  35(5)x1                             2e(.)x2 25(%)x2 62(b)x2 31(1)x1 +3u  DIFFER
   0x001e  30(0)x1                             25(%)x3 2e(.)x1 46(F)x1 6d(m)x1 +4u  DIFFER
   0x001f  00(.)x1                             25(%)x3 2e(.)x2 66(f)x1 62(b)x1 +3u  DIFFER
   0x0020  02(.)x1                             2e(.)x2 42(B)x2 65(e)x1 21(!)x1 +4u  DIFFER
   0x0021  00(.)x1                             62(b)x2 25(%)x1 2e(.)x1 00(.)x1 +5u  PARTIAL
   0x0022  00(.)x1                             2e(.)x2 44(D)x1 9e(.)x1 00(.)x1 +5u  PARTIAL
   0x0023  00(.)x1                             2e(.)x2 62(b)x2 d6(.)x1 8d(.)x1 +4u  DIFFER
   0x0024  47(G)x1                             42(B)x1 9e(.)x1 2e(.)x1 44(D)x1 +4u  DIFFER
   0x0025  48(H)x1                             25(%)x2 64(d)x1 43(C)x1 2e(.)x1 +3u  DIFFER
   0x0026  54(T)x1                             45(E)x2 41(A)x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x0027  54(T)x1                             72(r)x1 27(')x1 2e(.)x1 42(B)x1 +4u  DIFFER
   0x0028  50(P)x1                             25(%)x4 33(3)x1 db(.)x1 2e(.)x1 +1u  DIFFER
   0x0029  2f(/)x1                             41(A)x2 25(%)x1 31(1)x1 2e(.)x1 +3u  DIFFER
   0x002a  20( )x1                             25(%)x2 65(e)x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x002b  6d(m)x1                             25(%)x3 4b(K)x1 2e(.)x1 66(f)x1 +2u  DIFFER
   0x002c  65(e)x1                             25(%)x3 2e(.)x1 6e(n)x1 62(b)x1 +2u  PARTIAL
   ... (19 more divergent offsets)
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
  prompts_b/curl_353.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 353,
  "target": "curl",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 353 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 353 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 353 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).