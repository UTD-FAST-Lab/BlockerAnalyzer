==== BLOCKER ====
Target: libxml2
Branch ID: 7287
Location: /src/libxml2/xmlreader.c:2540:11
Enclosing function: xmlTextReaderMoveToAttributeNo
Source line:     for (;i < no;i++) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        3        7          0  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=9.10h  loser=20.70h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.70  dur_div=11.60h  hit_div=4
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7287/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlTextReaderMoveToAttributeNo (/src/libxml2/xmlreader.c:2513-2549) ---
[ ]  2511   */
[ ]  2512  int
[B]  2513  xmlTextReaderMoveToAttributeNo(xmlTextReaderPtr reader, int no) {
[B]  2514      int i;
[B]  2515      xmlAttrPtr cur;
[B]  2516      xmlNsPtr ns;
[ ]  2517  
[B]  2518      if (reader == NULL)
[ ]  2519  	return(-1);
[B]  2520      if (reader->node == NULL)
[ ]  2521  	return(-1);
[ ]  2522      /* TODO: handle the xmlDecl */
[B]  2523      if (reader->node->type != XML_ELEMENT_NODE)
[ ]  2524  	return(-1);
[ ]  2525  
[B]  2526      reader->curnode = NULL;
[ ]  2527  
[B]  2528      ns = reader->node->nsDef;
[B]  2529      for (i = 0;(i < no) && (ns != NULL);i++) {
[L]  2530  	ns = ns->next;
[L]  2531      }
[B]  2532      if (ns != NULL) {
[L]  2533  	reader->curnode = (xmlNodePtr) ns;
[L]  2534  	return(1);
[L]  2535      }
[ ]  2536  
[B]  2537      cur = reader->node->properties;
[B]  2538      if (cur == NULL)
[ ]  2539  	return(0);
[B]  2540      for (;i < no;i++) { <-- BLOCKER
[W]  2541  	cur = cur->next;
[W]  2542  	if (cur == NULL)
[ ]  2543  	    return(0);
[W]  2544      }
[ ]  2545      /* TODO walk the DTD if present */
[ ]  2546  
[B]  2547      reader->curnode = (xmlNodePtr) cur;
[B]  2548      return(1);
[B]  2549  }

--- Caller (1 hop): LLVMFuzzerTestOneInput (/src/libxml2/fuzz/xml.c:28-94, calls xmlTextReaderMoveToAttributeNo at line 83) (±10 around call site) ---
[ ]    73  
[ ]    74      /* Reader */
[ ]    75  
[B]    76      reader = xmlReaderForMemory(docBuffer, docSize, NULL, NULL, opts);
[B]    77      if (reader == NULL)
[ ]    78          goto exit;
[B]    79      while (xmlTextReaderRead(reader) == 1) {
[B]    80          if (xmlTextReaderNodeType(reader) == XML_ELEMENT_NODE) {
[B]    81              int i, n = xmlTextReaderAttributeCount(reader);
[B]    82              for (i=0; i<n; i++) {
[B]    83                  xmlTextReaderMoveToAttributeNo(reader, i); <-- CALL
[B]    84                  while (xmlTextReaderReadAttributeValue(reader) == 1);
[B]    85              }
[B]    86          }
[B]    87      }
[B]    88      xmlFreeTextReader(reader);
[ ]    89  
[B]    90  exit:
[B]    91      xmlFuzzDataCleanup();
[B]    92      xmlResetLastError();
[B]    93      return(0);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlTextReaderMoveToAttributeNo at line 83)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      14        64  xmlTextReaderRead  (/src/libxml2/xmlreader.c:1219-1538)
      12        55  xmlTextReaderNodeType  (/src/libxml2/xmlreader.c:2939-2997)
       4        22  xmlTextReaderAttributeCount  (/src/libxml2/xmlreader.c:2893-2926)
       6        23  xmlreader.c:xmlTextReaderFreeNode  (/src/libxml2/xmlreader.c:386-451)
       6        23  xmlreader.c:xmlTextReaderCharacters  (/src/libxml2/xmlreader.c:721-731)
       4        20  xmlreader.c:xmlTextReaderStartElementNs  (/src/libxml2/xmlreader.c:664-682)
       4        18  xmlreader.c:xmlTextReaderPushData  (/src/libxml2/xmlreader.c:765-872)
       2        10  xmlreader.c:xmlTextReaderEndElementNs  (/src/libxml2/xmlreader.c:698-708)
       2         9  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94)
       2         9  xmlreader.c:xmlTextReaderFreePropList  (/src/libxml2/xmlreader.c:272-280)
       2         9  xmlreader.c:xmlTextReaderFreeDoc  (/src/libxml2/xmlreader.c:461-501)
       2         9  xmlNewTextReader  (/src/libxml2/xmlreader.c:2000-2103)
       2         9  xmlFreeTextReader  (/src/libxml2/xmlreader.c:2144-2202)
       2         9  xmlTextReaderClose  (/src/libxml2/xmlreader.c:2219-2254)
       2         9  xmlTextReaderSetup  (/src/libxml2/xmlreader.c:5048-5236)
... (2 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94) ---
  d=2   L  45  T=0 F=2  T=0 F=9  if (docBuffer == NULL)
  d=2   L  59  T=0 F=2  T=0 F=9  if (ctxt == NULL)
  d=2   L  63  T=2 F=2  T=15 F=9  for (consumed = 0; consumed < docSize; consumed += chunkS...
  d=2   L  65  T=0 F=2  T=6 F=9  if (chunkSize > maxChunkSize)
  d=2   L  77  T=0 F=2  T=0 F=9  if (reader == NULL)
  d=2   L  79  T=12 F=2  T=55 F=9  while (xmlTextReaderRead(reader) == 1) {
  d=2   L  80  T=4 F=8  T=22 F=33  if (xmlTextReaderNodeType(reader) == XML_ELEMENT_NODE) {
  d=2   L  82  T=6 F=4  T=10 F=22  for (i=0; i<n; i++) {
--- d=1  xmlTextReaderMoveToAttributeNo  (/src/libxml2/xmlreader.c:2513-2549) ---
  d=1   L2529  T=0 F=4  T=1 F=0  for (i = 0;(i < no) && (ns != NULL);i++) {
  d=1   L2532  T=0 F=6  T=1 F=9  if (ns != NULL) {
  d=1   L2540  T=6 F=6  T=0 F=9  for (;i < no;i++) {  <-- BLOCKER
  d=1   L2542  T=0 F=6  T=0 F=0  if (cur == NULL)

[off-chain: 290 additional divergent branches across 21 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=b7122f8b6a26914d, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=20852s, mutation_op=ByteFlipMutator):
  0000: f9 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=9a01e60324bfc239, size=364 bytes, fuzzer=cmplog, trial=1, discovered_at=80129s, mutation_op=QwordAddMutator):
  0000: f9 00 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   ..7772.xml\.<?xm
  0010: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0020: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
  0030: 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37   STEM "dtds/12777

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=8c7bd7ba6dfb824c, size=368 bytes, fuzzer=naive, trial=1):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=23b42457f8a90d31, size=195 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=BytesRandInsertMutator,BytesDeleteMutator):
  0000: 10 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=10729eaf975afc93, size=201 bytes, fuzzer=naive, trial=1, discovered_at=58s, mutation_op=BytesCopyMutator,BytesCopyMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 45 4d 45 4e 54 20 62 20 28 23 50 43 44 06 00 00   EMENT b (#PCD...
  0010: 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78   .127772.xml\.<?x
  0020: 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22   ml version="1.0"
  0030: 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53   ?>.<!DOCTYPE a S
Seed 4 (id=743a152cf53fd92e, size=258 bytes, fuzzer=naive, trial=1, discovered_at=204s, mutation_op=BytesDeleteMutator,BytesCopyMutator,ByteFlipMutator,ByteInterestingMutator,CrossoverInsertMutator):
  0000: 01 78 6e 6c 20 89 65 72 73 69 6f 6e 3d 22 31 2e   .xnl .ersion="1.
  0010: 80 00 06 00 00 00 31 06 00 00 00 31 32 37 37 37   ......1....12777
  0020: 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72   2.xml\.<?xml ver
  0030: 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44   sion="1.0"?>.<!D
Seed 5 (id=75e1cc6d5e857d8f, size=361 bytes, fuzzer=naive, trial=1, discovered_at=1619s, mutation_op=TokenInsert,BitFlipMutator,BytesRandInsertMutator,QwordAddMutator,BytesDeleteMutator,DwordInterestingMutator):
  0000: 68 74 74 48 74 74 70 3a 2f 2f 66 61 6b 65 75 72   httHttp://fakeur
  0010: 6c 2e 6e 65 74 22 55 fc ff ff ff 65 75 72 6c 2e   l.net"U....eurl.
  0020: 6e 65 74 65 74 22 3e 62 20 74 65 78 0a 3c 21 45   netet">b tex.<!E
  0030: 4c 45 4d 45 4e 54 20 61 ff 7f 62 2a 29 3e 0a 0a   LEMENT a..b*)>..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f9(.)x2                             06(.)x1 10(.)x1 45(E)x1 01(.)x1 +5u  DIFFER
   0x0001  00(.)x2                             00(.)x2 4d(M)x1 78(x)x1 74(t)x1 +4u  PARTIAL
   0x0002  00(.)x1 37(7)x1                     00(.)x2 45(E)x1 6e(n)x1 74(t)x1 +4u  PARTIAL
   0x0003  00(.)x1 37(7)x1                     00(.)x2 4e(N)x1 6c(l)x1 48(H)x1 +4u  PARTIAL
   0x0004  31(1)x1 37(7)x1                     31(1)x2 74(t)x2 54(T)x1 20( )x1 +3u  PARTIAL
   0x0005  32(2)x2                             32(2)x2 74(t)x2 20( )x1 89(.)x1 +3u  PARTIAL
   0x0006  37(7)x1 2e(.)x1                     37(7)x2 70(p)x2 62(b)x1 65(e)x1 +3u  PARTIAL
   0x0007  37(7)x1 78(x)x1                     37(7)x2 3a(:)x2 20( )x1 72(r)x1 +3u  PARTIAL
   0x0008  37(7)x1 6d(m)x1                     2f(/)x3 37(7)x2 28(()x1 73(s)x1 +2u  PARTIAL
   0x0009  32(2)x1 6c(l)x1                     2f(/)x3 32(2)x2 23(#)x1 69(i)x1 +2u  PARTIAL
   0x000a  2e(.)x1 5c(\)x1                     2e(.)x3 50(P)x1 6f(o)x1 66(f)x1 +3u  PARTIAL
   0x000b  78(x)x1 0a(.)x1                     78(x)x2 43(C)x1 6e(n)x1 61(a)x1 +4u  PARTIAL
   0x000c  6d(m)x1 3c(<)x1                     6d(m)x2 44(D)x1 3d(=)x1 6b(k)x1 +4u  PARTIAL
   0x000d  6c(l)x1 3f(?)x1                     6c(l)x2 2e(.)x2 06(.)x1 22(")x1 +3u  PARTIAL
   0x000e  5c(\)x1 78(x)x1                     5c(\)x2 00(.)x1 31(1)x1 75(u)x1 +4u  PARTIAL
   0x000f  0a(.)x1 6d(m)x1                     0a(.)x2 2e(.)x2 00(.)x1 72(r)x1 +3u  PARTIAL
   0x0010  3c(<)x1 6c(l)x1                     3c(<)x2 00(.)x1 80(.)x1 6c(l)x1 +4u  PARTIAL
   0x0011  3f(?)x1 20( )x1                     3f(?)x2 31(1)x1 00(.)x1 2e(.)x1 +4u  PARTIAL
   0x0012  78(x)x1 76(v)x1                     78(x)x2 32(2)x1 06(.)x1 6e(n)x1 +4u  PARTIAL
   0x0013  6d(m)x1 65(e)x1                     6d(m)x2 37(7)x1 00(.)x1 65(e)x1 +4u  PARTIAL
   0x0014  6c(l)x1 72(r)x1                     6c(l)x2 37(7)x1 00(.)x1 74(t)x1 +4u  PARTIAL
   0x0015  20( )x1 73(s)x1                     20( )x2 37(7)x1 00(.)x1 22(")x1 +4u  PARTIAL
   0x0016  76(v)x1 69(i)x1                     76(v)x2 32(2)x1 31(1)x1 55(U)x1 +4u  PARTIAL
   0x0017  65(e)x1 6f(o)x1                     2e(.)x3 65(e)x2 06(.)x1 fc(.)x1 +2u  PARTIAL
   0x0018  72(r)x1 6e(n)x1                     72(r)x2 78(x)x1 00(.)x1 ff(.)x1 +4u  PARTIAL
   0x0019  73(s)x1 3d(=)x1                     73(s)x2 6d(m)x1 00(.)x1 ff(.)x1 +4u  PARTIAL
   0x001a  69(i)x1 22(")x1                     69(i)x2 6c(l)x1 00(.)x1 ff(.)x1 +4u  PARTIAL
   0x001b  6f(o)x1 31(1)x1                     6f(o)x2 5c(\)x1 31(1)x1 65(e)x1 +4u  PARTIAL
   0x001c  6e(n)x1 2e(.)x1                     6e(n)x2 0a(.)x1 32(2)x1 75(u)x1 +4u  PARTIAL
   0x001d  3d(=)x1 30(0)x1                     3d(=)x2 3c(<)x1 37(7)x1 72(r)x1 +4u  PARTIAL
   0x001e  22(")x2                             22(")x2 3f(?)x1 37(7)x1 6c(l)x1 +4u  PARTIAL
   0x001f  31(1)x1 3f(?)x1                     31(1)x2 78(x)x1 37(7)x1 2e(.)x1 +4u  PARTIAL
   0x0020  2e(.)x1 3e(>)x1                     2e(.)x3 6d(m)x1 32(2)x1 6e(n)x1 +3u  PARTIAL
   0x0021  30(0)x1 0a(.)x1                     30(0)x2 6c(l)x1 2e(.)x1 65(e)x1 +4u  PARTIAL
   0x0022  22(")x1 3c(<)x1                     22(")x2 20( )x1 78(x)x1 74(t)x1 +4u  PARTIAL
   0x0023  3f(?)x1 21(!)x1                     3f(?)x2 76(v)x1 6d(m)x1 65(e)x1 +4u  PARTIAL
   0x0024  3e(>)x1 44(D)x1                     3e(>)x2 65(e)x1 6c(l)x1 74(t)x1 +4u  PARTIAL
   0x0025  0a(.)x1 4f(O)x1                     0a(.)x2 72(r)x1 5c(\)x1 22(")x1 +4u  PARTIAL
   0x0026  3c(<)x1 43(C)x1                     3c(<)x2 73(s)x1 0a(.)x1 3e(>)x1 +4u  PARTIAL
   0x0027  21(!)x1 54(T)x1                     21(!)x2 69(i)x1 3c(<)x1 62(b)x1 +4u  PARTIAL
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_7287.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7287,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7287 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7287 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7287 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).