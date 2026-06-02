==== BLOCKER ====
Target: libxml2
Branch ID: 7476
Location: /src/libxml2/SAX2.c:2740:9
Enclosing function: xmlSAX2ProcessingInstruction
Source line:     if (ctxt->inSubset == 1) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (ctx_coverage vs naive_ctx)
cmplog                           0       10          0  REFERENCE
value_profile                    3        7          0  REFERENCE
value_profile_cmplog             4        6          0  REFERENCE
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=9.80h  loser=24.00h
  avg hitcount on branch: winner=341  loser=0
  prob_div=0.80  dur_div=14.20h  hit_div=341
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7476/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlSAX2ProcessingInstruction (/src/libxml2/SAX2.c:2717-2769) ---
[ ]  2715  xmlSAX2ProcessingInstruction(void *ctx, const xmlChar *target,
[ ]  2716                        const xmlChar *data)
[B]  2717  {
[B]  2718      xmlParserCtxtPtr ctxt = (xmlParserCtxtPtr) ctx;
[B]  2719      xmlNodePtr ret;
[B]  2720      xmlNodePtr parent;
[ ]  2721  
[B]  2722      if (ctx == NULL) return;
[B]  2723      parent = ctxt->node;
[ ]  2724  #ifdef DEBUG_SAX
[ ]  2725      xmlGenericError(xmlGenericErrorContext,
[ ]  2726  	    "SAX.xmlSAX2ProcessingInstruction(%s, %s)\n", target, data);
[ ]  2727  #endif
[ ]  2728  
[B]  2729      ret = xmlNewDocPI(ctxt->myDoc, target, data);
[B]  2730      if (ret == NULL) return;
[ ]  2731  
[B]  2732      if (ctxt->linenumbers) {
[B]  2733  	if (ctxt->input != NULL) {
[B]  2734  	    if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
[B]  2735  		ret->line = ctxt->input->line;
[ ]  2736  	    else
[ ]  2737  	        ret->line = USHRT_MAX;
[B]  2738  	}
[B]  2739      }
[B]  2740      if (ctxt->inSubset == 1) { <-- BLOCKER
[W]  2741  	xmlAddChild((xmlNodePtr) ctxt->myDoc->intSubset, ret);
[W]  2742  	return;
[B]  2743      } else if (ctxt->inSubset == 2) {
[ ]  2744  	xmlAddChild((xmlNodePtr) ctxt->myDoc->extSubset, ret);
[ ]  2745  	return;
[ ]  2746      }
[L]  2747      if (parent == NULL) {
[ ]  2748  #ifdef DEBUG_SAX_TREE
[ ]  2749  	    xmlGenericError(xmlGenericErrorContext,
[ ]  2750  		    "Setting PI %s as root\n", target);
[ ]  2751  #endif
[L]  2752          xmlAddChild((xmlNodePtr) ctxt->myDoc, (xmlNodePtr) ret);
[L]  2753  	return;
[L]  2754      }
[L]  2755      if (parent->type == XML_ELEMENT_NODE) {
[ ]  2756  #ifdef DEBUG_SAX_TREE
[ ]  2757  	xmlGenericError(xmlGenericErrorContext,
[ ]  2758  		"adding PI %s child to %s\n", target, parent->name);
[ ]  2759  #endif
[L]  2760  	xmlAddChild(parent, ret);
[L]  2761      } else {
[ ]  2762  #ifdef DEBUG_SAX_TREE
[ ]  2763  	xmlGenericError(xmlGenericErrorContext,
[ ]  2764  		"adding PI %s sibling to ", target);
[ ]  2765  	xmlDebugDumpOneNode(stderr, parent, 0);
[ ]  2766  #endif
[ ]  2767  	xmlAddSibling(parent, ret);
[ ]  2768      }
[L]  2769  }

--- No 1-hop callers of xmlSAX2ProcessingInstruction fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0       117  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
       0       117  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
       2        91  xmlSAX2ProcessingInstruction  (/src/libxml2/SAX2.c:2717-2769)  <-- enclosing
       0        70  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
       4        40  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
       0        32  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806)
       3        30  xmlSAX2SetDocumentLocator  (/src/libxml2/SAX2.c:942-948)
       3        30  xmlSAX2StartDocument  (/src/libxml2/SAX2.c:958-1013)
       0        22  xmlSAX2EndDocument  (/src/libxml2/SAX2.c:1023-1054)
       0        18  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591)
       0        14  xmlSAX2ExternalSubset  (/src/libxml2/SAX2.c:368-496)
       3        14  xmlSAX2InternalSubset  (/src/libxml2/SAX2.c:330-354)
       0        11  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)
       0         9  SAX2.c:xmlErrValid  (/src/libxml2/SAX2.c:99-124)
       0         9  xmlSAX2ResolveEntity  (/src/libxml2/SAX2.c:514-538)
... (3 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlSAX2ProcessingInstruction  (/src/libxml2/SAX2.c:2717-2769) ---
  d=1   L2722  T=0 F=2  T=0 F=91  if (ctx == NULL) return;
  d=1   L2730  T=0 F=2  T=0 F=91  if (ret == NULL) return;
  d=1   L2732  T=2 F=0  T=91 F=0  if (ctxt->linenumbers) {
  d=1   L2733  T=2 F=0  T=91 F=0  if (ctxt->input != NULL) {
  d=1   L2734  T=2 F=0  T=91 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=1   L2740  T=2 F=0  T=0 F=91  if (ctxt->inSubset == 1) {  <-- BLOCKER
  d=1   L2743  T=0 F=0  T=0 F=91  } else if (ctxt->inSubset == 2) {
  d=1   L2747  T=0 F=0  T=27 F=64  if (parent == NULL) {
  d=1   L2755  T=0 F=0  T=64 F=0  if (parent->type == XML_ELEMENT_NODE) {

[off-chain: 153 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=fbd4d48bc7f5a45b, size=345 bytes, fuzzer=naive_ctx, trial=1, discovered_at=4693s, mutation_op=BytesExpandMutator):
  0000: ff ff ff ff ff ff 31 32 37 37 37 32 2e 78 6d 6c   ......127772.xml
  0010: 5c 0a 3c 3f 78 6d 6c 20 76 65 be be be be be be   \.<?xml ve......
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 20 61 39 39 30 30 30 65 65   DOCTYPE a99000ee

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0069aaf9cd0a41e4, size=247 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteRandMutator,BytesRandInsertMutator,BytesDeleteMutator,BytesSwapMutator,ByteAddMutator,BytesCopyMutator,QwordAddMutator):
  0000: 4d 20 ff ff 74 64 73 2f 31 32 37 37 06 00 00 00   M ..tds/1277....
  0010: 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   127772.xml\.<?xm
  0020: 7c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   | version="1.0"?
  0030: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
Seed 2 (id=01a47cb938f3863b, size=396 bytes, fuzzer=naive, trial=1, discovered_at=5s, mutation_op=WordAddMutator,BytesDeleteMutator,ByteInterestingMutator,ByteInterestingMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 65 66 3d 22 68 74   72.xml\.<?ef="ht
  0010: 74 70 3a 2f 2f 3d 22 31 2e 30 22 3f 3e 0a 3c 21   tp://="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 fc ff   DOCTYPE a SYST..
  0030: ff ff ff ff ff ff 2f 31 32 37 37 37 32 2e 64 74   ....../127772.dt
Seed 3 (id=07a4a09ca39a736e, size=160 bytes, fuzzer=naive, trial=1, discovered_at=268s, mutation_op=WordAddMutator,BytesExpandMutator,ByteDecMutator,TokenInsert):
  0000: 06 00 00 00 31 32 37 37 37 37 37 37 37 38 37 37   ....127777777877
  0010: 37 37 37 37 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f   77777772.xml\.<?
  0020: 77 6d 6c 20 76 65 72 73 69 6f 6e 09 09 09 09 09   wml version.....
  0030: 09 09 09 09 09 09 09 31 2e 30 22 3f 3e 0a 3c 21   .......1.0"?>.<!
Seed 4 (id=15243bb40f46a284, size=96 bytes, fuzzer=naive, trial=1, discovered_at=1190s, mutation_op=BytesInsertCopyMutator,BytesDeleteMutator,BytesRandInsertMutator,BytesRandSetMutator,BytesExpandMutator):
  0000: 4f 4f 4f 4f 2d 38 73 2f 6c 5c 0a 3c 3f 78 3f 3e   OOOO-8s/l\.<?x?>
  0010: 0a 3c 65 72 73 69 6f 6e 54 4c f3 ff 3e 0a 78 3f   .<ersionTL..>.x?
  0020: 3e 0a 3c 65 72 73 69 6f 6e 54 4c f3 ff 3e 0a 3c   >.<ersionTL..>.<
  0030: 65 72 73 69 6f 64 69 6f 6e 54 4c f3 ff 3e 0a 3c   ersiodionTL..>.<
Seed 5 (id=0cfd65236af0dfcc, size=394 bytes, fuzzer=naive, trial=1, discovered_at=6119s, mutation_op=BytesDeleteMutator,BytesInsertCopyMutator,BytesRandSetMutator):
  0000: 77 77 68 74 74 70 3a 2f 2f 77 77 77 2e 1f 2b 2b   wwhttp://www..++
  0010: 2b 2b 2b 2b 77 33 2e 6f 8e 67 78 73 2f 31 32 37   ++++w3.o.gxs/127
  0020: 37 37 32 2e 64 74 64 22 3e 0a 0a 3e 2e 2e 2e 2e   772.dtd">..>....
  0030: 2e b5 b5 b5 b5 b5 b5 b5 b5 b5 b5 b5 b5 b5 b5 2e   ................


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  ff(.)x1                             4d(M)x1 37(7)x1 06(.)x1 4f(O)x1 +6u  DIFFER
   0x0001  ff(.)x1                             20( )x1 32(2)x1 00(.)x1 4f(O)x1 +6u  PARTIAL
   0x0002  ff(.)x1                             68(h)x3 ff(.)x2 74(t)x2 2e(.)x1 +2u  PARTIAL
   0x0003  ff(.)x1                             74(t)x4 ff(.)x2 78(x)x1 00(.)x1 +2u  PARTIAL
   0x0004  ff(.)x1                             74(t)x5 6d(m)x1 31(1)x1 2d(-)x1 +2u  PARTIAL
   0x0005  ff(.)x1                             70(p)x3 64(d)x1 6c(l)x1 32(2)x1 +4u  PARTIAL
   0x0006  31(1)x1                             3a(:)x3 73(s)x2 5c(\)x1 37(7)x1 +3u  DIFFER
   0x0007  32(2)x1                             2f(/)x6 0a(.)x1 37(7)x1 3a(:)x1 +1u  DIFFER
   0x0008  37(7)x1                             2f(/)x4 31(1)x1 3c(<)x1 37(7)x1 +3u  PARTIAL
   0x0009  37(7)x1                             77(w)x2 0a(.)x2 32(2)x1 3f(?)x1 +4u  PARTIAL
   0x000a  37(7)x1                             37(7)x2 77(w)x2 65(e)x1 0a(.)x1 +4u  PARTIAL
   0x000b  32(2)x1                             37(7)x2 77(w)x2 66(f)x1 3c(<)x1 +4u  DIFFER
   0x000c  2e(.)x1                             2e(.)x2 06(.)x1 3d(=)x1 37(7)x1 +5u  PARTIAL
   0x000d  78(x)x1                             00(.)x1 22(")x1 38(8)x1 78(x)x1 +6u  PARTIAL
   0x000e  6d(m)x1                             00(.)x1 68(h)x1 37(7)x1 3f(?)x1 +6u  DIFFER
   0x000f  6c(l)x1                             00(.)x1 74(t)x1 37(7)x1 3e(>)x1 +6u  DIFFER
   0x0010  5c(\)x1                             31(1)x1 74(t)x1 37(7)x1 0a(.)x1 +6u  DIFFER
   0x0011  0a(.)x1                             32(2)x1 70(p)x1 37(7)x1 3c(<)x1 +6u  DIFFER
   0x0012  3c(<)x1                             37(7)x2 3a(:)x1 65(e)x1 2b(+)x1 +5u  DIFFER
   0x0013  3f(?)x1                             37(7)x2 2f(/)x1 72(r)x1 2b(+)x1 +5u  DIFFER
   0x0014  78(x)x1                             37(7)x2 2f(/)x2 73(s)x1 77(w)x1 +4u  DIFFER
   0x0015  6d(m)x1                             32(2)x1 3d(=)x1 37(7)x1 69(i)x1 +6u  DIFFER
   0x0016  6c(l)x1                             2e(.)x2 22(")x1 37(7)x1 6f(o)x1 +5u  DIFFER
   0x0017  20( )x1                             78(x)x1 31(1)x1 32(2)x1 6e(n)x1 +6u  DIFFER
   0x0018  76(v)x1                             2e(.)x2 54(T)x2 6d(m)x1 8e(.)x1 +4u  DIFFER
   0x0019  65(e)x1                             6c(l)x1 30(0)x1 78(x)x1 4c(L)x1 +6u  DIFFER
   0x001a  be(.)x1                             20( )x2 5c(\)x1 22(")x1 6d(m)x1 +5u  DIFFER
   0x001b  be(.)x1                             0a(.)x2 3f(?)x1 6c(l)x1 ff(.)x1 +5u  DIFFER
   0x001c  be(.)x1                             3e(>)x2 2f(/)x2 0a(.)x2 3c(<)x1 +3u  DIFFER
   0x001d  be(.)x1                             0a(.)x3 3f(?)x1 31(1)x1 77(w)x1 +4u  DIFFER
   0x001e  be(.)x1                             78(x)x2 3c(<)x2 32(2)x1 77(w)x1 +4u  DIFFER
   0x001f  be(.)x1                             3f(?)x2 6d(m)x1 21(!)x1 37(7)x1 +5u  DIFFER
   0x0020  72(r)x1                             77(w)x2 7c(|)x1 44(D)x1 3e(>)x1 +5u  DIFFER
   0x0021  73(s)x1                             20( )x1 4f(O)x1 6d(m)x1 0a(.)x1 +6u  DIFFER
   0x0022  69(i)x1                             76(v)x1 43(C)x1 6c(l)x1 3c(<)x1 +6u  PARTIAL
   0x0023  6f(o)x1                             65(e)x2 54(T)x1 20( )x1 2e(.)x1 +5u  DIFFER
   0x0024  6e(n)x1                             72(r)x2 59(Y)x1 76(v)x1 64(d)x1 +5u  DIFFER
   0x0025  3d(=)x1                             73(s)x2 50(P)x1 65(e)x1 74(t)x1 +5u  DIFFER
   0x0026  22(")x1                             69(i)x2 45(E)x1 72(r)x1 64(d)x1 +5u  DIFFER
   0x0027  31(1)x1                             6f(o)x2 20( )x1 73(s)x1 22(")x1 +5u  DIFFER
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
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

--- naive_ctx ---
**Instrumentation**: naive's SanitizerCoverage edge counters, but the
executor installs a `CtxHook` (`HookableInProcessExecutor`). The hook
keeps a running hash of the current call context (caller chain) and
folds it into the edge-map index, so the same basic-block edge is
recorded at different map slots depending on the call path that
reached it.

**Feedback**: the same `MaxMapFeedback` edge-bucket signal as naive,
computed over the context-indexed map — a "new bucket" is a new
(call-context, edge) pair rather than a bare edge.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`, no
CMP_MAP. Stages are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no ParentInfo-only / dash rows.

**Per-execution cost**: one edge-counter increment per executed edge
plus a context-hash update per call/return.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_7476.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7476,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7476 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7476 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7476 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).