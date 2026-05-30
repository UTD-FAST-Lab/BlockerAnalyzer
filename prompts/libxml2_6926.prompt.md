==== BLOCKER ====
Target: libxml2
Branch ID: 6926
Location: /src/libxml2/tree.c:835:9
Enclosing function: xmlFreeNs
Source line:     if (cur->prefix != NULL) xmlFree((char *) cur->prefix);
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile); loser (ctx_coverage vs naive_ctx)
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog); loser (grimoire_structural vs grimoire)
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog)
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             3        7          0  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'naive', 'naive_ctx', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (4) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.00h  loser=19.70h
  avg hitcount on branch: winner=15  loser=1
  prob_div=0.80  dur_div=13.70h  hit_div=14
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 2: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=5.50h  loser=19.70h
  avg hitcount on branch: winner=1959  loser=1
  prob_div=0.80  dur_div=14.20h  hit_div=1958
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002
--- Pair 3: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=12.60h  loser=21.50h
  avg hitcount on branch: winner=89  loser=4
  prob_div=0.70  dur_div=8.90h  hit_div=85
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002
--- Pair 4: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=13.10h  loser=21.50h
  avg hitcount on branch: winner=79  loser=4
  prob_div=0.60  dur_div=8.40h  hit_div=75
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6926/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlFreeNs (/src/libxml2/tree.c:826-837) ---
[ ]   824   */
[ ]   825  void
[B]   826  xmlFreeNs(xmlNsPtr cur) {
[B]   827      if (cur == NULL) {
[ ]   828  #ifdef DEBUG_TREE
[ ]   829          xmlGenericError(xmlGenericErrorContext,
[ ]   830  		"xmlFreeNs : ns == NULL\n");
[ ]   831  #endif
[ ]   832  	return;
[ ]   833      }
[B]   834      if (cur->href != NULL) xmlFree((char *) cur->href);
[B]   835      if (cur->prefix != NULL) xmlFree((char *) cur->prefix); <-- BLOCKER
[B]   836      xmlFree(cur);
[B]   837  }

--- Caller (1 hop): xmlFreeNsList (/src/libxml2/tree.c:846-860, calls xmlFreeNs at line 857) (full body — short) ---
[B]   846  xmlFreeNsList(xmlNsPtr cur) {
[B]   847      xmlNsPtr next;
[B]   848      if (cur == NULL) {
[ ]   849  #ifdef DEBUG_TREE
[ ]   850          xmlGenericError(xmlGenericErrorContext,
[ ]   851  		"xmlFreeNsList : ns == NULL\n");
[ ]   852  #endif
[ ]   853  	return;
[ ]   854      }
[B]   855      while (cur != NULL) {
[B]   856          next = cur->next;
[B]   857          xmlFreeNs(cur); <-- CALL
[B]   858  	cur = next;
[B]   859      }
[B]   860  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  catalog.c:xmlDumpXMLCatalog  (/src/libxml2/catalog.c:654-706, calls xmlFreeNs at line 681)
hop 2  xmlreader.c:xmlTextReaderFreeNode  (/src/libxml2/xmlreader.c:386-451, calls xmlFreeNs at line 398)
hop 3  xmlACatalogDump  (/src/libxml2/catalog.c:2925-2934, calls catalog.c:xmlDumpXMLCatalog at line 2930)
hop 3  xmlTextReaderRead  (/src/libxml2/xmlreader.c:1219-1538, calls xmlreader.c:xmlTextReaderFreeNode at line 1364)
hop 3  xmlreader.c:xmlTextReaderValidateEntity  (/src/libxml2/xmlreader.c:1023-1101, calls xmlreader.c:xmlTextReaderFreeNode at line 1080)
hop 4  xmlCatalogDump  (/src/libxml2/catalog.c:3377-3385, calls xmlACatalogDump at line 3384)
hop 4  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlTextReaderRead at line 79)
hop 4  xmlTextReaderNext  (/src/libxml2/xmlreader.c:1589-1610, calls xmlTextReaderRead at line 1599)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     200         0  xmlSetNs  (/src/libxml2/tree.c:806-817)
     167         0  xmlNewNode  (/src/libxml2/tree.c:2259-2287)
     167         0  xmlNewDocNode  (/src/libxml2/tree.c:2352-2369)
     100        12  xmlreader.c:xmlTextReaderStartElementNs  (/src/libxml2/xmlreader.c:664-682)
      85        16  xmlBuildQName  (/src/libxml2/tree.c:223-247)
      50        12  xmlGetLastChild  (/src/libxml2/tree.c:3542-3551)
      27         6  xmlNewDocPI  (/src/libxml2/tree.c:2194-2228)
       0        15  xmlTextReaderNodeType  (/src/libxml2/xmlreader.c:2939-2997)
       0        12  xmlStringLenGetNodeList  (/src/libxml2/tree.c:1269-1487)
       0        10  xmlTextReaderReadAttributeValue  (/src/libxml2/xmlreader.c:2818-2849)
       0         8  xmlreader.c:xmlTextReaderFreeNode  (/src/libxml2/xmlreader.c:386-451)
       0         6  tree.c:xmlTreeEnsureXMLDecl  (/src/libxml2/tree.c:6095-6115)
       0         5  xmlIsBlankNode  (/src/libxml2/tree.c:7082-7097)
       0         5  xmlTextReaderMoveToAttributeNo  (/src/libxml2/xmlreader.c:2513-2549)
       0         5  xmlTextReaderAttributeCount  (/src/libxml2/xmlreader.c:2893-2926)
... (10 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  xmlTextReaderRead  (/src/libxml2/xmlreader.c:1219-1538) ---
  d=3   L1237  T=23 F=0  T=20 F=15  if (reader->mode == XML_TEXTREADER_MODE_INITIAL) {
  d=3   L1249  T=1 F=0  T=6 F=2  } while ((reader->ctxt->node == NULL) &&
  d=3   L1250  T=1 F=0  T=5 F=1  ((reader->mode != XML_TEXTREADER_MODE_EOF) &&
  d=3   L1251  T=1 F=0  T=5 F=0  (reader->state != XML_TEXTREADER_DONE)));
  d=3   L1252  T=0 F=0  T=1 F=2  if (reader->ctxt->node == NULL) {
  d=3   L1253  T=0 F=0  T=1 F=0  if (reader->ctxt->myDoc != NULL) {
  d=3   L1256  T=0 F=0  T=0 F=1  if (reader->node == NULL){
  d=3   L1263  T=0 F=0  T=2 F=0  if (reader->ctxt->myDoc != NULL) {
  d=3   L1266  T=0 F=0  T=0 F=2  if (reader->node == NULL)
  d=3   L1279  T=0 F=0  T=0 F=15  if (reader->node == NULL) {
  d=3   L1291  T=0 F=0  T=7 F=8  while ((reader->node != NULL) && (reader->node->next == N...
  d=3   L1291  T=0 F=0  T=15 F=0  while ((reader->node != NULL) && (reader->node->next == N...
  d=3   L1292  T=0 F=0  T=7 F=0  (reader->ctxt->nodeNr == olddepth) &&
  d=3   L1293  T=0 F=0  T=1 F=6  ((oldstate == XML_TEXTREADER_BACKTRACK) ||
  d=3   L1294  T=0 F=0  T=4 F=2  (reader->node->children == NULL) ||
  d=3   L1295  T=0 F=0  T=0 F=2  (reader->node->type == XML_ENTITY_REF_NODE) ||
  d=3   L1296  T=0 F=0  T=2 F=0  ((reader->node->children != NULL) &&
  d=3   L1297  T=0 F=0  T=2 F=0  (reader->node->children->type == XML_TEXT_NODE) &&
  d=3   L1298  T=0 F=0  T=0 F=2  (reader->node->children->next == NULL)) ||
  d=3   L1299  T=0 F=0  T=0 F=2  (reader->node->type == XML_DTD_NODE) ||
  d=3   L1300  T=0 F=0  T=0 F=2  (reader->node->type == XML_DOCUMENT_NODE) ||
  d=3   L1301  T=0 F=0  T=0 F=2  (reader->node->type == XML_HTML_DOCUMENT_NODE)) &&
  d=3   L1302  T=0 F=0  T=3 F=2  ((reader->ctxt->node == NULL) ||
  d=3   L1303  T=0 F=0  T=1 F=1  (reader->ctxt->node == reader->node) ||
  d=3   L1304  T=0 F=0  T=0 F=1  (reader->ctxt->node == reader->node->parent)) &&
  d=3   L1305  T=0 F=0  T=1 F=3  (reader->ctxt->instate != XML_PARSER_EOF)) {
  d=3   L1307  T=0 F=0  T=1 F=0  if (val < 0){
  d=3   L1315  T=0 F=0  T=11 F=3  if (oldstate != XML_TEXTREADER_BACKTRACK) {
  d=3   L1316  T=0 F=0  T=4 F=7  if ((reader->node->children != NULL) &&
  d=3   L1317  T=0 F=0  T=4 F=0  (reader->node->type != XML_ENTITY_REF_NODE) &&
  d=3   L1318  T=0 F=0  T=4 F=0  (reader->node->type != XML_XINCLUDE_START) &&
  d=3   L1319  T=0 F=0  T=4 F=0  (reader->node->type != XML_DTD_NODE)) {
  d=3   L1326  T=0 F=0  T=6 F=4  if (reader->node->next != NULL) {
  d=3   L1327  T=0 F=0  T=4 F=2  if ((oldstate == XML_TEXTREADER_ELEMENT) &&
  d=3   L1328  T=0 F=0  T=0 F=4  (reader->node->type == XML_ELEMENT_NODE) &&
  d=3   L1339  T=0 F=0  T=3 F=3  if ((reader->validate) &&
  d=3   L1340  T=0 F=0  T=1 F=2  (reader->node->type == XML_ELEMENT_NODE))
  d=3   L1343  T=0 F=0  T=0 F=6  if ((reader->preserves > 0) &&
  d=3   L1352  T=0 F=0  T=6 F=0  if ((reader->preserves == 0) &&
  d=3   L1354  T=0 F=0  T=6 F=0  (reader->in_xinclude == 0) &&
  d=3   L1356  T=0 F=0  T=6 F=0  (reader->entNr == 0) &&
  d=3   L1357  T=0 F=0  T=6 F=0  (reader->node->prev != NULL) &&
  d=3   L1358  T=0 F=0  T=4 F=2  (reader->node->prev->type != XML_DTD_NODE)) {
  d=3   L1360  T=0 F=0  T=4 F=0  if ((tmp->extra & NODE_IS_PRESERVED) == 0) {
  d=3   L1361  T=0 F=0  T=4 F=0  if (oldnode == tmp)
  d=3   L1370  T=0 F=0  T=3 F=1  if ((oldstate == XML_TEXTREADER_ELEMENT) &&
  d=3   L1371  T=0 F=0  T=0 F=3  (reader->node->type == XML_ELEMENT_NODE) &&
  d=3   L1378  T=0 F=0  T=1 F=3  if ((reader->validate != XML_TEXTREADER_NOT_VALIDATE) && ...
  d=3   L1378  T=0 F=0  T=0 F=1  if ((reader->validate != XML_TEXTREADER_NOT_VALIDATE) && ...
  d=3   L1381  T=0 F=0  T=0 F=4  if ((reader->preserves > 0) &&
  d=3   L1385  T=0 F=0  T=0 F=4  if ((reader->node == NULL) ||
  d=3   L1386  T=0 F=0  T=1 F=3  (reader->node->type == XML_DOCUMENT_NODE) ||
  d=3   L1387  T=0 F=0  T=0 F=3  (reader->node->type == XML_HTML_DOCUMENT_NODE)) {
  d=3   L1388  T=0 F=0  T=0 F=1  if (reader->mode != XML_TEXTREADER_MODE_EOF) {
  d=3   L1400  T=0 F=0  T=1 F=0  if ((oldnode != NULL) && (reader->preserves == 0) &&
  d=3   L1400  T=0 F=0  T=1 F=0  if ((oldnode != NULL) && (reader->preserves == 0) &&
  d=3   L1402  T=0 F=0  T=1 F=0  (reader->in_xinclude == 0) &&
  d=3   L1404  T=0 F=0  T=1 F=0  (reader->entNr == 0) &&
  d=3   L1405  T=0 F=0  T=1 F=0  (oldnode->type != XML_DTD_NODE) &&
  d=3   L1406  T=0 F=0  T=1 F=0  ((oldnode->extra & NODE_IS_PRESERVED) == 0)) {
  d=3   L1413  T=0 F=0  T=3 F=0  if ((reader->preserves == 0) &&
  d=3   L1415  T=0 F=0  T=3 F=0  (reader->in_xinclude == 0) &&
  d=3   L1417  T=0 F=0  T=3 F=0  (reader->entNr == 0) &&
  d=3   L1418  T=0 F=0  T=3 F=0  (reader->node->last != NULL) &&
  d=3   L1419  T=0 F=0  T=3 F=0  ((reader->node->last->extra & NODE_IS_PRESERVED) == 0)) {
  d=3   L1433  T=0 F=0  T=16 F=0  if ((reader->node != NULL) &&
  d=3   L1434  T=0 F=0  T=8 F=8  (reader->node->next == NULL) &&
  d=3   L1435  T=0 F=0  T=4 F=4  ((reader->node->type == XML_TEXT_NODE) ||
  d=3   L1436  T=0 F=0  T=0 F=4  (reader->node->type == XML_CDATA_SECTION_NODE))) {
  d=3   L1437  T=0 F=0  T=1 F=3  if (xmlTextReaderExpand(reader) == NULL)
  d=3   L1445  T=0 F=0  T=0 F=15  if ((reader->xinclude) && (reader->in_xinclude == 0) &&
  d=3   L1464  T=0 F=0  T=0 F=15  if ((reader->node != NULL) && (reader->node->type == XML_...
  d=3   L1464  T=0 F=0  T=15 F=0  if ((reader->node != NULL) && (reader->node->type == XML_...
  d=3   L1468  T=0 F=0  T=15 F=0  if ((reader->node != NULL) && (reader->node->type == XML_...
  d=3   L1468  T=0 F=0  T=0 F=15  if ((reader->node != NULL) && (reader->node->type == XML_...
  d=3   L1476  T=0 F=0  T=15 F=0  if ((reader->node != NULL) &&
  d=3   L1477  T=0 F=0  T=0 F=15  (reader->node->type == XML_ENTITY_REF_NODE) &&
  d=3   L1487  T=0 F=0  T=15 F=0  } else if ((reader->node != NULL) &&
  d=3   L1488  T=0 F=0  T=0 F=15  (reader->node->type == XML_ENTITY_REF_NODE) &&
  d=3   L1493  T=0 F=0  T=15 F=0  if ((reader->node != NULL) &&
  d=3   L1494  T=0 F=0  T=0 F=15  (reader->node->type == XML_ENTITY_DECL) &&
  d=3   L1501  T=0 F=0  T=6 F=0  if ((reader->validate != XML_TEXTREADER_NOT_VALIDATE) && ...
  d=3   L1501  T=0 F=0  T=6 F=9  if ((reader->validate != XML_TEXTREADER_NOT_VALIDATE) && ...
  d=3   L1504  T=0 F=0  T=3 F=3  if ((node->type == XML_ELEMENT_NODE) &&
  d=3   L1505  T=0 F=0  T=3 F=0  ((reader->state != XML_TEXTREADER_END) &&
  d=3   L1506  T=0 F=0  T=2 F=1  (reader->state != XML_TEXTREADER_BACKTRACK))) {
  d=3   L1508  T=0 F=0  T=2 F=2  } else if ((node->type == XML_TEXT_NODE) ||
  d=3   L1509  T=0 F=0  T=0 F=2  (node->type == XML_CDATA_SECTION_NODE)) {
  d=3   L1516  T=0 F=0  T=0 F=15  if ((reader->patternNr > 0) && (reader->state != XML_TEXT...
  d=3   L1528  T=0 F=0  T=0 F=15  if ((reader->validate == XML_TEXTREADER_VALIDATE_XSD) &&
--- d=2  xmlreader.c:xmlTextReaderFreeNode  (/src/libxml2/xmlreader.c:386-451) ---
  d=2   L 389  T=0 F=0  T=8 F=0  if ((reader != NULL) && (reader->ctxt != NULL))
  d=2   L 389  T=0 F=0  T=8 F=0  if ((reader != NULL) && (reader->ctxt != NULL))
  d=2   L 393  T=0 F=0  T=0 F=8  if (cur->type == XML_DTD_NODE) {
  d=2   L 397  T=0 F=0  T=0 F=8  if (cur->type == XML_NAMESPACE_DECL) {
  d=2   L 401  T=0 F=0  T=0 F=8  if (cur->type == XML_ATTRIBUTE_NODE) {
  d=2   L 406  T=0 F=0  T=0 F=8  if ((cur->children != NULL) &&
  d=2   L 413  T=0 F=0  T=0 F=8  if ((__xmlRegisterCallbacks) && (xmlDeregisterNodeDefault...
  d=2   L 416  T=0 F=0  T=3 F=5  if (((cur->type == XML_ELEMENT_NODE) ||
  d=2   L 417  T=0 F=0  T=0 F=5  (cur->type == XML_XINCLUDE_START) ||
  d=2   L 418  T=0 F=0  T=0 F=5  (cur->type == XML_XINCLUDE_END)) &&
  d=2   L 419  T=0 F=0  T=2 F=1  (cur->properties != NULL))
  d=2   L 421  T=0 F=0  T=3 F=5  if ((cur->content != (xmlChar *) &(cur->properties)) &&
  d=2   L 422  T=0 F=0  T=0 F=3  (cur->type != XML_ELEMENT_NODE) &&
  d=2   L 428  T=0 F=0  T=3 F=5  if (((cur->type == XML_ELEMENT_NODE) ||
  d=2   L 429  T=0 F=0  T=0 F=5  (cur->type == XML_XINCLUDE_START) ||
  d=2   L 430  T=0 F=0  T=0 F=5  (cur->type == XML_XINCLUDE_END)) &&
  d=2   L 431  T=0 F=0  T=1 F=2  (cur->nsDef != NULL))
  d=2   L 437  T=0 F=0  T=3 F=5  if ((cur->type != XML_TEXT_NODE) &&
  d=2   L 438  T=0 F=0  T=3 F=0  (cur->type != XML_COMMENT_NODE))
  d=2   L 441  T=0 F=0  T=3 F=5  if (((cur->type == XML_ELEMENT_NODE) ||
  d=2   L 442  T=0 F=0  T=5 F=0  (cur->type == XML_TEXT_NODE)) &&
  d=2   L 443  T=0 F=0  T=8 F=0  (reader != NULL) && (reader->ctxt != NULL) &&
  d=2   L 443  T=0 F=0  T=8 F=0  (reader != NULL) && (reader->ctxt != NULL) &&
  d=2   L 444  T=0 F=0  T=8 F=0  (reader->ctxt->freeElemsNr < MAX_FREE_NODES)) {
--- d=1  xmlFreeNs  (/src/libxml2/tree.c:826-837) ---
  d=1   L 835  T=0 F=269  T=158 F=0  if (cur->prefix != NULL) xmlFree((char *) cur->prefix);  <-- BLOCKER

[off-chain: 231 additional divergent branches across 43 functions (see HIT-COUNT DIVERGENCE for which functions)]

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
Seed 1 (id=5f83308a4d472d74, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=10s, mutation_op=ByteRandMutator,ByteDecMutator,ByteInterestingMutator,ByteRandMutator,BytesSwapMutator,ByteAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=05f6a2e17ed1a7c1, size=156 bytes, fuzzer=cmplog, trial=1, discovered_at=1215s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,ByteRandMutator):
  0000: 69 6e 6b 6d 70 6c 65 29 20 20 23 46 49 58 45 44   inkmple)  #FIXED
  0010: 20 27 20 13 13 13 13 13 13 13 13 13 13 13 13 13    ' .............
  0020: 13 13 13 58 45 44 20 27 20 20 06 00 00 00 31 32   ...XED '  ....12
  0030: 0a 37 37 32 40 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   .772@xml\.<?xml 
Seed 3 (id=3f82a3daf8d36108, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3471s, mutation_op=BytesDeleteMutator,BytesSetMutator):
  0000: fa 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=51fd9b36079604e3, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=3541s, mutation_op=ByteAddMutator,DwordInterestingMutator):
  0000: ff 7f ff ff 31 32 c8 37 37 32 2e 78 6d 6c 5c 0a   ....12.772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=990e4190ea653e2d, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3590s, mutation_op=CrossoverReplaceMutator,QwordAddMutator,ByteDecMutator):
  0000: f9 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6926.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6926,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), grimoire>cmplog (grimoire_structural), value_profile>naive (value_profile), naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6926 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6926 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6926 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).