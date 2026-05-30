==== BLOCKER ====
Target: libxml2
Branch ID: 7317
Location: /src/libxml2/xmlsave.c:603:6
Enclosing function: xmlsave.c:xmlNsDumpOutput
Source line: 	if (cur->prefix != NULL) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile)
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog); loser (grimoire_structural vs grimoire)
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog)
naive_ctx                        7        3          0  REFERENCE
naive_ngram4                     0        9          1  REFERENCE
mopt                             0        8          2  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             3        7          0  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (3) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.90h  loser=17.80h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.80  dur_div=12.90h  hit_div=4
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 2: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=5.70h  loser=17.80h
  avg hitcount on branch: winner=625  loser=0
  prob_div=0.80  dur_div=12.10h  hit_div=624
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002
--- Pair 3: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=9.80h  loser=19.10h
  avg hitcount on branch: winner=10  loser=1
  prob_div=0.60  dur_div=9.30h  hit_div=8
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7317/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlsave.c:xmlNsDumpOutput (/src/libxml2/xmlsave.c:591-611) ---
[ ]   589   */
[ ]   590  static void
[B]   591  xmlNsDumpOutput(xmlOutputBufferPtr buf, xmlNsPtr cur, xmlSaveCtxtPtr ctxt) {
[B]   592      if ((cur == NULL) || (buf == NULL)) return;
[B]   593      if ((cur->type == XML_LOCAL_NAMESPACE) && (cur->href != NULL)) {
[B]   594  	if (xmlStrEqual(cur->prefix, BAD_CAST "xml"))
[ ]   595  	    return;
[ ]   596  
[B]   597  	if (ctxt != NULL && ctxt->format == 2)
[ ]   598  	    xmlOutputBufferWriteWSNonSig(ctxt, 2);
[B]   599  	else
[B]   600  	    xmlOutputBufferWrite(buf, 1, " ");
[ ]   601  
[ ]   602          /* Within the context of an element attributes */
[B]   603  	if (cur->prefix != NULL) { <-- BLOCKER
[L]   604  	    xmlOutputBufferWrite(buf, 6, "xmlns:");
[L]   605  	    xmlOutputBufferWriteString(buf, (const char *)cur->prefix);
[L]   606  	} else
[W]   607  	    xmlOutputBufferWrite(buf, 5, "xmlns");
[B]   608  	xmlOutputBufferWrite(buf, 1, "=");
[B]   609  	xmlBufWriteQuotedString(buf->buffer, cur->href);
[B]   610      }
[B]   611  }

--- Caller (1 hop): xmlsave.c:xmlNsListDumpOutputCtxt (/src/libxml2/xmlsave.c:635-640, calls xmlsave.c:xmlNsDumpOutput at line 637) (full body — short) ---
[B]   635  xmlNsListDumpOutputCtxt(xmlSaveCtxtPtr ctxt, xmlNsPtr cur) {
[B]   636      while (cur != NULL) {
[B]   637          xmlNsDumpOutput(ctxt->buf, cur, ctxt); <-- CALL
[B]   638  	cur = cur->next;
[B]   639      }
[B]   640  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlsave.c:xmlNsDumpOutputCtxt  (/src/libxml2/xmlsave.c:622-624, calls xmlsave.c:xmlNsDumpOutput at line 623)
hop 2  xmlsave.c:xmlNsListDumpOutputCtxt  (/src/libxml2/xmlsave.c:635-640, calls xmlsave.c:xmlNsDumpOutput at line 637)
hop 3  xmlsave.c:xhtmlNodeDumpOutput  (/src/libxml2/xmlsave.c:1392-1700, calls xmlsave.c:xmlNsDumpOutputCtxt at line 1409)
hop 3  xmlsave.c:xmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:809-1068, calls xmlsave.c:xmlNsDumpOutputCtxt at line 1018)
hop 4  xmlSaveTree  (/src/libxml2/xmlsave.c:1860-1879, calls xmlsave.c:xhtmlNodeDumpOutput at line 1866)
hop 4  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225, calls xmlsave.c:xmlNodeDumpOutputInternal at line 1206)
hop 4  xmlsave.c:xmlDtdDumpOutput  (/src/libxml2/xmlsave.c:666-712, calls xmlsave.c:xmlNodeDumpOutputInternal at line 707)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      43        11  xmlsave.c:xmlNsDumpOutput  (/src/libxml2/xmlsave.c:591-611)  <-- enclosing
      43        11  xmlsave.c:xmlNsListDumpOutputCtxt  (/src/libxml2/xmlsave.c:635-640)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225) ---
  d=4   L1190  T=11 F=10  T=11 F=0  if (dtd != NULL) {
--- d=3  xmlsave.c:xmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:809-1068) ---
  d=3   L 823  T=0 F=171  T=0 F=59  case XML_DOCUMENT_NODE:
  d=3   L 824  T=0 F=171  T=0 F=59  case XML_HTML_DOCUMENT_NODE:
  d=3   L 828  T=11 F=160  T=11 F=48  case XML_DTD_NODE:
  d=3   L 832  T=0 F=171  T=0 F=59  case XML_DOCUMENT_FRAG_NODE:
  d=3   L 841  T=0 F=171  T=0 F=59  case XML_ELEMENT_DECL:
  d=3   L 845  T=0 F=171  T=0 F=59  case XML_ATTRIBUTE_DECL:
  d=3   L 849  T=0 F=171  T=0 F=59  case XML_ENTITY_DECL:
  d=3   L 853  T=102 F=69  T=22 F=37  case XML_ELEMENT_NODE:
  d=3   L 854  T=81 F=21  T=11 F=11  if ((cur != root) && (ctxt->format == 1) &&
  d=3   L 854  T=0 F=81  T=0 F=11  if ((cur != root) && (ctxt->format == 1) &&
  d=3   L 866  T=0 F=102  T=0 F=22  if ((cur->parent != parent) && (cur->children != NULL)) {
  d=3   L 872  T=58 F=44  T=0 F=22  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=3   L 872  T=0 F=58  T=0 F=0  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=3   L 877  T=43 F=59  T=11 F=11  if (cur->nsDef)
  d=3   L 879  T=8 F=102  T=12 F=22  for (attr = cur->properties; attr != NULL; attr = attr->n...
  d=3   L 882  T=61 F=41  T=3 F=19  if (cur->children == NULL) {
  d=3   L 883  T=61 F=0  T=3 F=0  if ((ctxt->options & XML_SAVE_NO_EMPTY) == 0) {
  d=3   L 884  T=0 F=61  T=0 F=3  if (ctxt->format == 2)
  d=3   L 902  T=0 F=41  T=0 F=19  if (ctxt->format == 1) {
  d=3   L 915  T=0 F=41  T=0 F=19  if (ctxt->format == 2)
  d=3   L 918  T=0 F=41  T=0 F=19  if (ctxt->format == 1) xmlOutputBufferWrite(buf, 1, "\n");
  d=3   L 919  T=41 F=0  T=19 F=0  if (ctxt->level >= 0) ctxt->level++;
  d=3   L 927  T=49 F=122  T=25 F=34  case XML_TEXT_NODE:
  d=3   L 940  T=9 F=162  T=1 F=58  case XML_PI_NODE:
  d=3   L 941  T=0 F=9  T=0 F=1  if ((cur != root) && (ctxt->format == 1) && (xmlIndentTre...
  d=3   L 947  T=8 F=1  T=1 F=0  if (cur->content != NULL) {
  d=3   L 950  T=8 F=0  T=1 F=0  if (cur->content != NULL) {
  d=3   L 951  T=0 F=8  T=0 F=1  if (ctxt->format == 2)
  d=3   L 962  T=0 F=1  T=0 F=0  if (ctxt->format == 2)
  d=3   L 968  T=0 F=171  T=0 F=59  case XML_COMMENT_NODE:
  d=3   L 982  T=0 F=171  T=0 F=59  case XML_ENTITY_REF_NODE:
  d=3   L 988  T=0 F=171  T=0 F=59  case XML_CDATA_SECTION_NODE:
  d=3   L1013  T=0 F=171  T=0 F=59  case XML_ATTRIBUTE_NODE:
  d=3   L1017  T=0 F=171  T=0 F=59  case XML_NAMESPACE_DECL:
  d=3   L1021  T=0 F=171  T=0 F=59  default:
  d=3   L1026  T=41 F=130  T=23 F=36  if (cur == root)
  d=3   L1028  T=0 F=130  T=0 F=36  if ((ctxt->format == 1) &&
  d=3   L1032  T=89 F=41  T=17 F=19  if (cur->next != NULL) {
  d=3   L1041  T=41 F=0  T=19 F=0  if (cur->type == XML_ELEMENT_NODE) {
  d=3   L1042  T=41 F=0  T=19 F=0  if (ctxt->level > 0) ctxt->level--;
  d=3   L1043  T=41 F=0  T=19 F=0  if ((xmlIndentTreeOutput) && (ctxt->format == 1))
  d=3   L1043  T=0 F=41  T=0 F=19  if ((xmlIndentTreeOutput) && (ctxt->format == 1))
  d=3   L1050  T=0 F=22  T=0 F=0  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=3   L1050  T=22 F=19  T=0 F=19  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=3   L1057  T=0 F=41  T=0 F=19  if (ctxt->format == 2)
  d=3   L1061  T=0 F=41  T=0 F=19  if (cur == unformattedNode) {
--- d=2  xmlsave.c:xmlNsListDumpOutputCtxt  (/src/libxml2/xmlsave.c:635-640) ---
  d=2   L 636  T=43 F=43  T=11 F=11  while (cur != NULL) {
--- d=1  xmlsave.c:xmlNsDumpOutput  (/src/libxml2/xmlsave.c:591-611) ---
  d=1   L 592  T=0 F=43  T=0 F=11  if ((cur == NULL) || (buf == NULL)) return;
  d=1   L 592  T=0 F=43  T=0 F=11  if ((cur == NULL) || (buf == NULL)) return;
  d=1   L 593  T=43 F=0  T=11 F=0  if ((cur->type == XML_LOCAL_NAMESPACE) && (cur->href != N...
  d=1   L 593  T=43 F=0  T=11 F=0  if ((cur->type == XML_LOCAL_NAMESPACE) && (cur->href != N...
  d=1   L 594  T=0 F=43  T=0 F=11  if (xmlStrEqual(cur->prefix, BAD_CAST "xml"))
  d=1   L 597  T=0 F=43  T=0 F=11  if (ctxt != NULL && ctxt->format == 2)
  d=1   L 597  T=43 F=0  T=11 F=0  if (ctxt != NULL && ctxt->format == 2)
  d=1   L 603  T=0 F=43  T=11 F=0  if (cur->prefix != NULL) {  <-- BLOCKER

[off-chain: 53 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=8f8537181bfef3b5, size=234 bytes, fuzzer=grimoire, trial=1, discovered_at=1816s, mutation_op=I2SRandReplace,I2SRandReplace):
  0000: 55 54 46 38 06 00 37 37 32 2e 78 6d 6c 5c 0a 3c   UTF8..772.xml\.<
  0010: 3f 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20   ?l ?><!DOCTYPEa 
  0020: 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37   SYSTEM "dtds/127
  0030: 37 37 32 2e 64 74 64 22 3e 3c 61 3e 0a 20 20 3c   772.dtd"><a>.  <
Seed 2 (id=9ac54fe3dd9be284, size=216 bytes, fuzzer=grimoire, trial=1, discovered_at=1816s, mutation_op=GrimoireRecursiveReplacementMutator):
  0000: 45 55 43 2d 4a 50 55 54 46 38 06 00 5c 0a 3c 3f   EUC-JPUTF8..\.<?
  0010: 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20 53   l ?><!DOCTYPEa S
  0020: 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37   YSTEM "dtds/1277
  0030: 37 32 2e 64 74 64 22 3e 3c 61 3e 20 3c 62 20 6b   72.dtd"><a> <b k
Seed 3 (id=ddf4485d1f91e6ae, size=180 bytes, fuzzer=grimoire, trial=1, discovered_at=1816s, mutation_op=GrimoireRandomDeleteMutator):
  0000: 55 54 46 38 06 00 5c 0a 3c 3f 6c 20 3f 3e 3c 21   UTF8..\.<?l ?><!
  0010: 44 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d 20   DOCTYPEa SYSTEM 
  0020: 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64   "dtds/127772.dtd
  0030: 22 3e 3c 61 3e 20 3c 62 20 6b 3a 39 3c 2f 62 3e   "><a> <b k:9</b>
Seed 4 (id=e1d7963fe300eca8, size=180 bytes, fuzzer=grimoire, trial=1, discovered_at=6869s, mutation_op=I2SRandReplace):
  0000: 55 54 46 38 06 00 5c 0a 3c 3f 6c 20 3f 3e 3c 21   UTF8..\.<?l ?><!
  0010: 44 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d 20   DOCTYPEa SYSTEM 
  0020: 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64   "dtds/127772.dtd
  0030: 22 3e 3c 61 3e 20 3c 62 20 6b 3a 39 3c 3a 62 3e   "><a> <b k:9<:b>
Seed 5 (id=67f9a08bf1c7e0c1, size=362 bytes, fuzzer=grimoire, trial=1, discovered_at=9482s, mutation_op=I2SRandReplace,I2SRandReplace,I2SRandReplace):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=8c7bd7ba6dfb824c, size=368 bytes, fuzzer=naive, trial=1):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=5f83308a4d472d74, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=10s, mutation_op=ByteRandMutator,ByteDecMutator,ByteInterestingMutator,ByteRandMutator,BytesSwapMutator,ByteAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=671269cb256ddf38, size=289 bytes, fuzzer=naive, trial=1, discovered_at=58s, mutation_op=BytesDeleteMutator,ByteAddMutator):
  0000: 0d 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=e38b37912b0d39bb, size=407 bytes, fuzzer=naive, trial=1, discovered_at=342s, mutation_op=BytesDeleteMutator,WordInterestingMutator,BitFlipMutator,BytesDeleteMutator,BytesExpandMutator,TokenInsert):
  0000: 8b 22 3e 62 20 74 65 78 6d 6c 5c 0a 3c 3f 78 6d   .">b texml\.<?xm
  0010: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0020: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
  0030: 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37   STEM "dtds/12777
Seed 5 (id=b08cc06d8f5744dc, size=569 bytes, fuzzer=naive, trial=1, discovered_at=343s, mutation_op=BytesDeleteMutator,BytesInsertCopyMutator,TokenInsert,BytesExpandMutator,DwordInterestingMutator):
  0000: 65 78 6d 6c 5c 0a 3c 3f 78 6d 49 53 4f 2d 4c 41   exml\.<?xmISO-LA
  0010: 54 49 4e 2d 32 6c 20 76 65 72 73 69 6f 6e 3d 22   TIN-2l version="
  0020: 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45   1.0"?>.<!DOCTYPE
  0030: 20 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f    a SYSTEM "dtds/


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0003  38(8)x3 78(x)x3 00(.)x3 ff(.)x2 +9u  00(.)x8 62(b)x1 6c(l)x1 27(')x1     PARTIAL
   0x0004  06(.)x4 6d(m)x3 ef(.)x3 45(E)x3 +7u  31(1)x8 20( )x1 5c(\)x1 2f(/)x1     PARTIAL
   0x0005  00(.)x4 6c(l)x3 ff(.)x2 76(v)x2 +9u  32(2)x8 74(t)x1 0a(.)x1 2a(*)x1     PARTIAL
   0x0006  5c(\)x5 ff(.)x3 37(7)x2 76(v)x2 +8u  37(7)x8 65(e)x1 3c(<)x1 3a(:)x1     PARTIAL
   0x0007  0a(.)x5 ff(.)x3 37(7)x2 76(v)x2 +8u  37(7)x8 78(x)x1 3f(?)x1 27(')x1     PARTIAL
   0x0009  3f(?)x4 31(1)x2 76(v)x2 62(b)x2 +11u  32(2)x8 6c(l)x1 6d(m)x1 66(f)x1     PARTIAL
   0x000a  78(x)x3 6c(l)x2 6d(m)x2 ef(.)x2 +11u  2e(.)x8 5c(\)x1 49(I)x1 66(f)x1     PARTIAL
   0x000b  6d(m)x3 ef(.)x3 20( )x2 6c(l)x2 +10u  78(x)x8 0a(.)x1 53(S)x1 28(()x1     PARTIAL
   0x000c  6c(l)x4 5c(\)x3 21(!)x3 ef(.)x3 +7u  6d(m)x8 3c(<)x1 4f(O)x1 2f(/)x1     PARTIAL
   0x000d  20( )x4 0a(.)x3 ef(.)x3 3e(>)x2 +8u  6c(l)x8 3f(?)x1 2d(-)x1 2f(/)x1     DIFFER
   0x000e  3c(<)x5 ef(.)x3 76(v)x2 62(b)x2 +9u  5c(\)x8 78(x)x1 4c(L)x1 2b(+)x1     PARTIAL
   0x000f  3f(?)x3 ff(.)x3 21(!)x2 65(e)x2 +10u  0a(.)x8 6d(m)x1 41(A)x1 27(')x1     PARTIAL
   0x0010  6c(l)x4 44(D)x2 72(r)x2 3c(<)x2 +9u  3c(<)x8 6c(l)x1 54(T)x1 2f(/)x1     PARTIAL
   0x0011  20( )x3 73(s)x3 6d(m)x3 4f(O)x2 +9u  3f(?)x8 20( )x1 49(I)x1 2a(*)x1     PARTIAL
   0x0012  6c(l)x4 3f(?)x3 43(C)x2 69(i)x2 +9u  78(x)x8 76(v)x1 4e(N)x1 2a(*)x1     PARTIAL
   0x0013  3e(>)x4 5c(\)x4 54(T)x2 6f(o)x2 +8u  6d(m)x8 65(e)x1 2d(-)x1 3a(:)x1     PARTIAL
   0x0014  0a(.)x5 3c(<)x3 22(")x3 59(Y)x2 +7u  6c(l)x8 72(r)x1 32(2)x1 27(')x1     PARTIAL
   0x0015  3c(<)x6 21(!)x4 50(P)x2 3d(=)x2 +7u  20( )x8 73(s)x1 6c(l)x1 2a(*)x1     DIFFER
   0x0016  44(D)x3 21(!)x2 45(E)x2 22(")x2 +10u  76(v)x8 69(i)x1 20( )x1 66(f)x1     DIFFER
   0x0017  4f(O)x3 61(a)x2 31(1)x2 df(.)x2 +11u  65(e)x8 6f(o)x1 76(v)x1 66(f)x1     DIFFER
   0x0018  43(C)x3 20( )x2 2e(.)x2 76(v)x2 +12u  72(r)x8 6e(n)x1 65(e)x1 2b(+)x1     DIFFER
   0x0019  54(T)x3 53(S)x2 30(0)x2 ef(.)x2 +10u  73(s)x8 3d(=)x1 72(r)x1 2f(/)x1     DIFFER
   0x001a  59(Y)x5 20( )x4 ef(.)x3 22(")x2 +7u  69(i)x8 22(")x1 73(s)x1 2f(/)x1     PARTIAL
   0x001b  50(P)x3 53(S)x3 ef(.)x3 3f(?)x2 +9u  6f(o)x8 31(1)x1 69(i)x1 2b(+)x1     DIFFER
   0x001c  45(E)x3 54(T)x2 3e(>)x2 ef(.)x2 +10u  6e(n)x8 2e(.)x1 6f(o)x1 27(')x1     DIFFER
   0x001d  61(a)x4 45(E)x3 0a(.)x2 6c(l)x2 +10u  3d(=)x8 30(0)x1 6e(n)x1 2f(/)x1     PARTIAL
   0x001e  20( )x3 3c(<)x3 61(a)x2 4d(M)x2 +10u  22(")x9 3d(=)x1 2a(*)x1             DIFFER
   0x001f  20( )x4 53(S)x3 21(!)x2 73(s)x2 +10u  31(1)x8 3f(?)x1 22(")x1 2f(/)x1     DIFFER
   0x0020  59(Y)x4 22(")x2 44(D)x2 3d(=)x2 +11u  2e(.)x8 3e(>)x1 31(1)x1 2f(/)x1     PARTIAL
   0x0021  53(S)x3 64(d)x2 4f(O)x2 22(")x2 +12u  30(0)x8 0a(.)x1 2e(.)x1 2f(/)x1     DIFFER
   0x0022  54(T)x3 74(t)x3 43(C)x2 3d(=)x2 +10u  22(")x8 3c(<)x1 30(0)x1 2b(+)x1     PARTIAL
   0x0023  64(d)x4 54(T)x3 45(E)x3 22(")x2 +8u  3f(?)x8 21(!)x1 22(")x1 27(')x1     PARTIAL
   0x0024  4d(M)x3 73(s)x2 59(Y)x2 31(1)x2 +10u  3e(>)x8 44(D)x1 3f(?)x1 2f(/)x1     DIFFER
   0x0025  20( )x3 2f(/)x2 50(P)x2 2e(.)x2 +11u  0a(.)x8 4f(O)x1 3e(>)x1 2a(*)x1     PARTIAL
   0x0026  22(")x4 ef(.)x3 31(1)x2 45(E)x2 +9u  3c(<)x8 43(C)x1 0a(.)x1 3a(:)x1     PARTIAL
   0x0027  64(d)x3 32(2)x3 2f(/)x3 22(")x2 +8u  21(!)x8 54(T)x1 3c(<)x1 27(')x1     DIFFER
   0x0028  74(t)x3 37(7)x2 61(a)x2 2f(/)x2 +12u  44(D)x8 59(Y)x1 21(!)x1 2a(*)x1     DIFFER
   0x0029  64(d)x3 37(7)x2 20( )x2 40(@)x2 +12u  4f(O)x8 50(P)x1 44(D)x1 66(f)x1     DIFFER
   0x002a  73(s)x3 37(7)x3 53(S)x3 88(.)x2 +10u  43(C)x8 45(E)x1 4f(O)x1 66(f)x1     DIFFER
   0x002b  2f(/)x3 32(2)x2 59(Y)x2 20( )x2 +11u  54(T)x8 20( )x1 43(C)x1 28(()x1     PARTIAL
   ... (20 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7317.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7317,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), grimoire>cmplog (grimoire_structural), value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7317 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7317 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7317 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).