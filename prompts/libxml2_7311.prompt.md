==== BLOCKER ====
Target: libxml2
Branch ID: 7311
Location: /src/libxml2/xmlregexp.c:6340:9
Enclosing function: xmlAutomataNewEpsilon
Source line:     if (to == NULL)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        5          5  REFERENCE
cmplog                           1        9          0  loser (value_profile vs value_profile_cmplog)
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog); winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=8.50h  loser=17.70h
  avg hitcount on branch: winner=3  loser=0
  prob_div=0.70  dur_div=9.20h  hit_div=3
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=8.50h  loser=16.50h
  avg hitcount on branch: winner=3  loser=1
  prob_div=0.70  dur_div=8.00h  hit_div=2
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7311/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlAutomataNewEpsilon (/src/libxml2/xmlregexp.c:6336-6343) ---
[ ]  6334  xmlAutomataStatePtr
[ ]  6335  xmlAutomataNewEpsilon(xmlAutomataPtr am, xmlAutomataStatePtr from,
[B]  6336  		      xmlAutomataStatePtr to) {
[B]  6337      if ((am == NULL) || (from == NULL))
[ ]  6338  	return(NULL);
[B]  6339      xmlFAGenerateEpsilonTransition(am, from, to);
[B]  6340      if (to == NULL) <-- BLOCKER
[L]  6341  	return(am->state);
[W]  6342      return(to);
[B]  6343  }

--- Caller (1 hop): valid.c:xmlValidBuildAContentModel (/src/libxml2/valid.c:641-781, calls xmlAutomataNewEpsilon at line 674) (±10 around call site) ---
[ ]   664  	    }
[ ]   665  
[B]   666  	    switch (content->ocur) {
[ ]   667  		case XML_ELEMENT_CONTENT_ONCE:
[ ]   668  		    ctxt->state = xmlAutomataNewTransition(ctxt->am,
[ ]   669  			    ctxt->state, NULL, fullname, NULL);
[ ]   670  		    break;
[W]   671  		case XML_ELEMENT_CONTENT_OPT:
[W]   672  		    ctxt->state = xmlAutomataNewTransition(ctxt->am,
[W]   673  			    ctxt->state, NULL, fullname, NULL);
[W]   674  		    xmlAutomataNewEpsilon(ctxt->am, oldstate, ctxt->state); <-- CALL
[W]   675  		    break;
[ ]   676  		case XML_ELEMENT_CONTENT_PLUS:
[ ]   677  		    ctxt->state = xmlAutomataNewTransition(ctxt->am,
[ ]   678  			    ctxt->state, NULL, fullname, NULL);
[ ]   679  		    xmlAutomataNewTransition(ctxt->am, ctxt->state,
[ ]   680  			                     ctxt->state, fullname, NULL);
[ ]   681  		    break;
[L]   682  		case XML_ELEMENT_CONTENT_MULT:
[L]   683  		    ctxt->state = xmlAutomataNewEpsilon(ctxt->am,
[L]   684  					    ctxt->state, NULL);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  relaxng.c:xmlRelaxNGCompile  (/src/libxml2/relaxng.c:3046-3258, calls xmlAutomataNewEpsilon at line 3153)
hop 3  relaxng.c:xmlRelaxNGTryCompile  (/src/libxml2/relaxng.c:3272-3345, calls relaxng.c:xmlRelaxNGCompile at line 3284)
hop 4  xmlRelaxNGParse  (/src/libxml2/relaxng.c:7514-7638, calls relaxng.c:xmlRelaxNGTryCompile at line 7618)
hop 5  xmlreader.c:xmlTextReaderRelaxNGValidateInternal  (/src/libxml2/xmlreader.c:4277-4359, calls xmlRelaxNGParse at line 4323)
hop 6  xmlTextReaderRelaxNGValidate  (/src/libxml2/xmlreader.c:4555-4557, calls xmlreader.c:xmlTextReaderRelaxNGValidateInternal at line 4556)
hop 6  xmlTextReaderRelaxNGValidateCtxt  (/src/libxml2/xmlreader.c:4537-4539, calls xmlreader.c:xmlTextReaderRelaxNGValidateInternal at line 4538)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      48       192  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      18        72  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
      18        54  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883)
       6        36  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
       1        21  valid.c:xmlErrValidNode  (/src/libxml2/valid.c:139-159)
       9        27  valid.c:xmlFreeAttribute  (/src/libxml2/valid.c:1907-1939)
       9        27  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172)
       9        27  valid.c:xmlFreeAttributeTableEntry  (/src/libxml2/valid.c:2175-2177)
       9        27  valid.c:xmlGetDtdElementDesc2  (/src/libxml2/valid.c:3280-3334)
       6        24  valid.c:xmlValidateNmtokensValueInternal  (/src/libxml2/valid.c:3765-3810)
       9        27  xmlValidateAttributeDecl  (/src/libxml2/valid.c:4197-4288)
       3        21  xmlValidateOneAttribute  (/src/libxml2/valid.c:4431-4577)
       9        27  valid.c:xmlValidateAttributeCallback  (/src/libxml2/valid.c:6762-6830)
       6        21  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)
       6        21  valid.c:xmlFreeElement  (/src/libxml2/valid.c:1382-1395)
... (51 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlAutomataNewEpsilon  (/src/libxml2/xmlregexp.c:6336-6343) ---
  d=1   L6337  T=0 F=1  T=0 F=3  if ((am == NULL) || (from == NULL))
  d=1   L6337  T=0 F=1  T=0 F=3  if ((am == NULL) || (from == NULL))
  d=1   L6340  T=0 F=1  T=3 F=0  if (to == NULL)  <-- BLOCKER

[off-chain: 658 additional divergent branches across 69 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=4bed379e31cead31, size=523 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=32225s, mutation_op=TokenInsert,BytesRandSetMutator,TokenReplace,BytesInsertMutator,BytesDeleteMutator):
  0000: 32 00 20 20 20 20 20 20 20 20 20 20 20 20 ff 00   2.            ..
  0010: 31 31 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   117772.xml\.<?xm
  0020: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0030: 3e 0a 3c 21 44 4f 43 54 59 50 45 0a 61 20 53 59   >.<!DOCTYPE.a SY

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=3df972b457200ada, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=4456s, mutation_op=BytesSetMutator,CrossoverInsertMutator,BytesInsertCopyMutator,ByteFlipMutator,BytesDeleteMutator,TokenInsert,BytesInsertCopyMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c   ersion="1.0"?>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE
  0030: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
Seed 2 (id=b7122f8b6a26914d, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=20852s, mutation_op=ByteFlipMutator):
  0000: f9 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=9a01e60324bfc239, size=364 bytes, fuzzer=cmplog, trial=1, discovered_at=80129s, mutation_op=QwordAddMutator):
  0000: f9 00 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   ..7772.xml\.<?xm
  0010: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0020: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
  0030: 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37   STEM "dtds/12777


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  32(2)x1                             f9(.)x2 37(7)x1                     DIFFER
   0x0001  00(.)x1                             00(.)x2 37(7)x1                     PARTIAL
   0x0002  20( )x1                             32(2)x1 00(.)x1 37(7)x1             DIFFER
   0x0003  20( )x1                             2e(.)x1 00(.)x1 37(7)x1             DIFFER
   0x0004  20( )x1                             78(x)x1 31(1)x1 37(7)x1             DIFFER
   0x0005  20( )x1                             32(2)x2 6d(m)x1                     DIFFER
   0x0006  20( )x1                             6c(l)x1 37(7)x1 2e(.)x1             DIFFER
   0x0007  20( )x1                             5c(\)x1 37(7)x1 78(x)x1             DIFFER
   0x0008  20( )x1                             0a(.)x1 37(7)x1 6d(m)x1             DIFFER
   0x0009  20( )x1                             3c(<)x1 32(2)x1 6c(l)x1             DIFFER
   0x000a  20( )x1                             3f(?)x1 2e(.)x1 5c(\)x1             DIFFER
   0x000b  20( )x1                             78(x)x2 0a(.)x1                     DIFFER
   0x000c  20( )x1                             6d(m)x2 3c(<)x1                     DIFFER
   0x000d  20( )x1                             6c(l)x2 3f(?)x1                     DIFFER
   0x000e  ff(.)x1                             20( )x1 5c(\)x1 78(x)x1             DIFFER
   0x000f  00(.)x1                             76(v)x1 0a(.)x1 6d(m)x1             DIFFER
   0x0010  31(1)x1                             65(e)x1 3c(<)x1 6c(l)x1             DIFFER
   0x0011  31(1)x1                             72(r)x1 3f(?)x1 20( )x1             DIFFER
   0x0012  37(7)x1                             73(s)x1 78(x)x1 76(v)x1             DIFFER
   0x0013  37(7)x1                             69(i)x1 6d(m)x1 65(e)x1             DIFFER
   0x0014  37(7)x1                             6f(o)x1 6c(l)x1 72(r)x1             DIFFER
   0x0015  32(2)x1                             6e(n)x1 20( )x1 73(s)x1             DIFFER
   0x0016  2e(.)x1                             3d(=)x1 76(v)x1 69(i)x1             DIFFER
   0x0017  78(x)x1                             22(")x1 65(e)x1 6f(o)x1             DIFFER
   0x0018  6d(m)x1                             31(1)x1 72(r)x1 6e(n)x1             DIFFER
   0x0019  6c(l)x1                             2e(.)x1 73(s)x1 3d(=)x1             DIFFER
   0x001a  5c(\)x1                             30(0)x1 69(i)x1 22(")x1             DIFFER
   0x001b  0a(.)x1                             22(")x1 6f(o)x1 31(1)x1             DIFFER
   0x001c  3c(<)x1                             3f(?)x1 6e(n)x1 2e(.)x1             DIFFER
   0x001d  3f(?)x1                             3e(>)x1 3d(=)x1 30(0)x1             DIFFER
   0x001e  78(x)x1                             22(")x2 0a(.)x1                     DIFFER
   0x001f  6d(m)x1                             3c(<)x1 31(1)x1 3f(?)x1             DIFFER
   0x0020  6c(l)x1                             21(!)x1 2e(.)x1 3e(>)x1             DIFFER
   0x0021  20( )x1                             44(D)x1 30(0)x1 0a(.)x1             DIFFER
   0x0022  76(v)x1                             4f(O)x1 22(")x1 3c(<)x1             DIFFER
   0x0023  65(e)x1                             43(C)x1 3f(?)x1 21(!)x1             DIFFER
   0x0024  72(r)x1                             54(T)x1 3e(>)x1 44(D)x1             DIFFER
   0x0025  73(s)x1                             59(Y)x1 0a(.)x1 4f(O)x1             DIFFER
   0x0026  69(i)x1                             50(P)x1 3c(<)x1 43(C)x1             DIFFER
   0x0027  6f(o)x1                             45(E)x1 21(!)x1 54(T)x1             DIFFER
   ... (24 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7311.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7311,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7311 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7311 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7311 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).