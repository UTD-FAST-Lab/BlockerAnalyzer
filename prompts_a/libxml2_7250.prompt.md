==== BLOCKER ====
Target: libxml2
Branch ID: 7250
Location: /src/libxml2/xmlreader.c:496:9
Enclosing function: xmlreader.c:xmlTextReaderFreeDoc
Source line:     if (cur->oldNs != NULL) xmlFreeNsList(cur->oldNs);
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    4        6          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     3        7          0  REFERENCE
mopt                             4        6          0  REFERENCE
minimizer                        6        4          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=13.40h  loser=23.10h
  avg hitcount on branch: winner=3  loser=0
  prob_div=0.70  dur_div=9.70h  hit_div=3
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7250/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlreader.c:xmlTextReaderFreeDoc (/src/libxml2/xmlreader.c:461-501) ---
[ ]   459   */
[ ]   460  static void
[B]   461  xmlTextReaderFreeDoc(xmlTextReaderPtr reader, xmlDocPtr cur) {
[B]   462      xmlDtdPtr extSubset, intSubset;
[ ]   463  
[B]   464      if (cur == NULL) return;
[ ]   465  
[B]   466      if ((__xmlRegisterCallbacks) && (xmlDeregisterNodeDefaultValue))
[ ]   467  	xmlDeregisterNodeDefaultValue((xmlNodePtr) cur);
[ ]   468  
[ ]   469      /*
[ ]   470       * Do this before freeing the children list to avoid ID lookups
[ ]   471       */
[B]   472      if (cur->ids != NULL) xmlFreeIDTable((xmlIDTablePtr) cur->ids);
[B]   473      cur->ids = NULL;
[B]   474      if (cur->refs != NULL) xmlFreeRefTable((xmlRefTablePtr) cur->refs);
[B]   475      cur->refs = NULL;
[B]   476      extSubset = cur->extSubset;
[B]   477      intSubset = cur->intSubset;
[B]   478      if (intSubset == extSubset)
[L]   479  	extSubset = NULL;
[B]   480      if (extSubset != NULL) {
[B]   481  	xmlUnlinkNode((xmlNodePtr) cur->extSubset);
[B]   482  	cur->extSubset = NULL;
[B]   483  	xmlFreeDtd(extSubset);
[B]   484      }
[B]   485      if (intSubset != NULL) {
[B]   486  	xmlUnlinkNode((xmlNodePtr) cur->intSubset);
[B]   487  	cur->intSubset = NULL;
[B]   488  	xmlFreeDtd(intSubset);
[B]   489      }
[ ]   490  
[B]   491      if (cur->children != NULL) xmlTextReaderFreeNodeList(reader, cur->children);
[ ]   492  
[B]   493      if (cur->version != NULL) xmlFree((char *) cur->version);
[B]   494      if (cur->name != NULL) xmlFree((char *) cur->name);
[B]   495      if (cur->encoding != NULL) xmlFree((char *) cur->encoding);
[B]   496      if (cur->oldNs != NULL) xmlFreeNsList(cur->oldNs); <-- BLOCKER
[B]   497      if (cur->URL != NULL) xmlFree((char *) cur->URL);
[B]   498      if (cur->dict != NULL) xmlDictFree(cur->dict);
[ ]   499  
[B]   500      xmlFree(cur);
[B]   501  }

--- Caller (1 hop): xmlTextReaderClose (/src/libxml2/xmlreader.c:2219-2254, calls xmlreader.c:xmlTextReaderFreeDoc at line 2245) (full body — short) ---
[B]  2219  xmlTextReaderClose(xmlTextReaderPtr reader) {
[B]  2220      if (reader == NULL)
[ ]  2221  	return(-1);
[B]  2222      reader->node = NULL;
[B]  2223      reader->curnode = NULL;
[B]  2224      reader->mode = XML_TEXTREADER_MODE_CLOSED;
[B]  2225      if (reader->faketext != NULL) {
[ ]  2226          xmlFreeNode(reader->faketext);
[ ]  2227          reader->faketext = NULL;
[ ]  2228      }
[B]  2229      if (reader->ctxt != NULL) {
[B]  2230  #ifdef LIBXML_VALID_ENABLED
[B]  2231  	if ((reader->ctxt->vctxt.vstateTab != NULL) &&
[B]  2232  	    (reader->ctxt->vctxt.vstateMax > 0)){
[W]  2233  #ifdef LIBXML_REGEXP_ENABLED
[W]  2234              while (reader->ctxt->vctxt.vstateNr > 0)
[W]  2235                  xmlValidatePopElement(&reader->ctxt->vctxt, NULL, NULL, NULL);
[W]  2236  #endif /* LIBXML_REGEXP_ENABLED */
[W]  2237  	    xmlFree(reader->ctxt->vctxt.vstateTab);
[W]  2238  	    reader->ctxt->vctxt.vstateTab = NULL;
[W]  2239  	    reader->ctxt->vctxt.vstateMax = 0;
[W]  2240  	}
[B]  2241  #endif /* LIBXML_VALID_ENABLED */
[B]  2242  	xmlStopParser(reader->ctxt);
[B]  2243  	if (reader->ctxt->myDoc != NULL) {
[B]  2244  	    if (reader->preserve == 0)
[B]  2245  		xmlTextReaderFreeDoc(reader, reader->ctxt->myDoc); <-- CALL
[B]  2246  	    reader->ctxt->myDoc = NULL;
[B]  2247  	}
[B]  2248      }
[B]  2249      if ((reader->input != NULL)  && (reader->allocs & XML_TEXTREADER_INPUT)) {
[B]  2250  	xmlFreeParserInputBuffer(reader->input);
[B]  2251  	reader->allocs -= XML_TEXTREADER_INPUT;
[B]  2252      }
[B]  2253      return(0);
[B]  2254  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlTextReaderClose  (/src/libxml2/xmlreader.c:2219-2254, calls xmlreader.c:xmlTextReaderFreeDoc at line 2245)
hop 2  xmlTextReaderGetRemainder  (/src/libxml2/xmlreader.c:2439-2473, calls xmlreader.c:xmlTextReaderFreeDoc at line 2454)
hop 3  xmlFreeTextReader  (/src/libxml2/xmlreader.c:2144-2202, calls xmlTextReaderClose at line 2186)
hop 4  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlFreeTextReader at line 88)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      14         2  xmlreader.c:xmlTextReaderFreeNodeList  (/src/libxml2/xmlreader.c:291-375)
      12         0  xmlTextReaderReadAttributeValue  (/src/libxml2/xmlreader.c:2818-2849)
      12         0  xmlTextReaderNodeType  (/src/libxml2/xmlreader.c:2939-2997)
      10         0  xmlreader.c:xmlTextReaderFreeProp  (/src/libxml2/xmlreader.c:238-262)
      15         5  xmlreader.c:xmlTextReaderCharacters  (/src/libxml2/xmlreader.c:721-731)
       6         0  xmlreader.c:xmlTextReaderFreeNode  (/src/libxml2/xmlreader.c:386-451)
       6         0  xmlTextReaderMoveToAttributeNo  (/src/libxml2/xmlreader.c:2513-2549)
       5         0  xmlreader.c:xmlTextReaderFreePropList  (/src/libxml2/xmlreader.c:272-280)
       4         0  xmlreader.c:xmlTextReaderValidatePush  (/src/libxml2/xmlreader.c:882-932)
       4         0  xmlreader.c:xmlTextReaderValidateCData  (/src/libxml2/xmlreader.c:944-963)
       4         0  xmlreader.c:xmlTextReaderGetSuccessor  (/src/libxml2/xmlreader.c:1114-1123)
       4         0  xmlreader.c:xmlTextReaderDoExpand  (/src/libxml2/xmlreader.c:1137-1158)
       4         0  xmlTextReaderExpand  (/src/libxml2/xmlreader.c:1566-1576)
       4         0  xmlTextReaderAttributeCount  (/src/libxml2/xmlreader.c:2893-2926)
       2         0  xmlreader.c:xmlTextReaderEndElementNs  (/src/libxml2/xmlreader.c:698-708)
... (1 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  xmlFreeTextReader  (/src/libxml2/xmlreader.c:2144-2202) ---
  d=3   L2145  T=0 F=4  T=0 F=10  if (reader == NULL)
  d=3   L2148  T=0 F=4  T=0 F=10  if (reader->rngSchemas != NULL) {
  d=3   L2152  T=0 F=4  T=0 F=10  if (reader->rngValidCtxt != NULL) {
  d=3   L2157  T=0 F=4  T=0 F=10  if (reader->xsdPlug != NULL) {
  d=3   L2161  T=0 F=4  T=0 F=10  if (reader->xsdValidCtxt != NULL) {
  d=3   L2166  T=0 F=4  T=0 F=10  if (reader->xsdSchemas != NULL) {
  d=3   L2172  T=0 F=4  T=0 F=10  if (reader->xincctxt != NULL)
  d=3   L2176  T=0 F=4  T=0 F=10  if (reader->patternTab != NULL) {
  d=3   L2185  T=4 F=0  T=10 F=0  if (reader->mode != XML_TEXTREADER_MODE_CLOSED)
  d=3   L2187  T=4 F=0  T=10 F=0  if (reader->ctxt != NULL) {
  d=3   L2188  T=4 F=0  T=10 F=0  if (reader->dict == reader->ctxt->dict)
  d=3   L2190  T=4 F=0  T=10 F=0  if (reader->allocs & XML_TEXTREADER_CTXT)
  d=3   L2193  T=4 F=0  T=10 F=0  if (reader->sax != NULL)
  d=3   L2195  T=4 F=0  T=10 F=0  if (reader->buffer != NULL)
  d=3   L2197  T=0 F=4  T=0 F=10  if (reader->entTab != NULL)
  d=3   L2199  T=0 F=4  T=0 F=10  if (reader->dict != NULL)
--- d=2  xmlTextReaderClose  (/src/libxml2/xmlreader.c:2219-2254) ---
  d=2   L2220  T=0 F=4  T=0 F=10  if (reader == NULL)
  d=2   L2225  T=0 F=4  T=0 F=10  if (reader->faketext != NULL) {
  d=2   L2229  T=4 F=0  T=10 F=0  if (reader->ctxt != NULL) {
  d=2   L2231  T=2 F=2  T=0 F=10  if ((reader->ctxt->vctxt.vstateTab != NULL) &&
  d=2   L2232  T=2 F=0  T=0 F=0  (reader->ctxt->vctxt.vstateMax > 0)){
  d=2   L2234  T=2 F=2  T=0 F=0  while (reader->ctxt->vctxt.vstateNr > 0)
  d=2   L2243  T=4 F=0  T=10 F=0  if (reader->ctxt->myDoc != NULL) {
  d=2   L2244  T=4 F=0  T=10 F=0  if (reader->preserve == 0)
  d=2   L2249  T=4 F=0  T=10 F=0  if ((reader->input != NULL)  && (reader->allocs & XML_TEX...
  d=2   L2249  T=4 F=0  T=10 F=0  if ((reader->input != NULL)  && (reader->allocs & XML_TEX...
--- d=1  xmlreader.c:xmlTextReaderFreeDoc  (/src/libxml2/xmlreader.c:461-501) ---
  d=1   L 464  T=0 F=4  T=0 F=10  if (cur == NULL) return;
  d=1   L 466  T=0 F=4  T=0 F=10  if ((__xmlRegisterCallbacks) && (xmlDeregisterNodeDefault...
  d=1   L 472  T=0 F=4  T=0 F=10  if (cur->ids != NULL) xmlFreeIDTable((xmlIDTablePtr) cur-...
  d=1   L 474  T=0 F=4  T=0 F=10  if (cur->refs != NULL) xmlFreeRefTable((xmlRefTablePtr) c...
  d=1   L 478  T=0 F=4  T=7 F=3  if (intSubset == extSubset)
  d=1   L 480  T=3 F=1  T=1 F=9  if (extSubset != NULL) {
  d=1   L 485  T=4 F=0  T=3 F=7  if (intSubset != NULL) {
  d=1   L 491  T=4 F=0  T=2 F=8  if (cur->children != NULL) xmlTextReaderFreeNodeList(read...
  d=1   L 493  T=4 F=0  T=10 F=0  if (cur->version != NULL) xmlFree((char *) cur->version);
  d=1   L 494  T=0 F=4  T=0 F=10  if (cur->name != NULL) xmlFree((char *) cur->name);
  d=1   L 495  T=0 F=4  T=0 F=10  if (cur->encoding != NULL) xmlFree((char *) cur->encoding);
  d=1   L 496  T=4 F=0  T=0 F=10  if (cur->oldNs != NULL) xmlFreeNsList(cur->oldNs);  <-- BLOCKER
  d=1   L 497  T=0 F=4  T=0 F=10  if (cur->URL != NULL) xmlFree((char *) cur->URL);
  d=1   L 498  T=3 F=1  T=3 F=7  if (cur->dict != NULL) xmlDictFree(cur->dict);

[off-chain: 287 additional divergent branches across 22 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=51fd9b36079604e3, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=3541s, mutation_op=ByteAddMutator,DwordInterestingMutator):
  0000: ff 7f ff ff 31 32 c8 37 37 32 2e 78 6d 6c 5c 0a   ....12.772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=b7122f8b6a26914d, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=20852s, mutation_op=ByteFlipMutator):
  0000: f9 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=f32dee7a138d773b, size=378 bytes, fuzzer=cmplog, trial=1, discovered_at=24520s, mutation_op=WordInterestingMutator):
  0000: 33 2e 6f 72 67 00 02 39 39 39 2f 78 3a 69 6e 6b   3.org..999/x:ink
  0010: 27 0a 20 20 20 20 20 20 20 20 78 6d 6c 6e 73 28   '.        xmlns(
  0020: 78 6c 69 6e 6b 20 20 43 44 41 54 41 20 20 20 20   xlink  CDATA    
  0030: 20 23 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65    #.xml\.<?xml ve
Seed 4 (id=9a01e60324bfc239, size=364 bytes, fuzzer=cmplog, trial=1, discovered_at=80129s, mutation_op=QwordAddMutator):
  0000: f9 00 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   ..7772.xml\.<?xm
  0010: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0020: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
  0030: 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37   STEM "dtds/12777

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003a9c177fd1ad1c, size=201 bytes, fuzzer=naive, trial=2, discovered_at=39s, mutation_op=ByteRandMutator,WordInterestingMutator,DwordInterestingMutator,BytesDeleteMutator):
  0000: 38 38 38 38 38 49 22 31 00 31 32 37 37 37 32 2e   88888I"1.127772.
  0010: 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69   xml\.<?xml versi
  0020: 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43   on="1.0"?>.<!DOC
  0030: 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22 64   TYPE a SYSTEM "d
Seed 2 (id=001ec54085f9ee0a, size=192 bytes, fuzzer=naive, trial=2, discovered_at=52s, mutation_op=BytesDeleteMutator,BytesInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=00229161e8eeb28b, size=284 bytes, fuzzer=naive, trial=2, discovered_at=277s, mutation_op=QwordAddMutator,BytesInsertCopyMutator,BytesRandSetMutator,TokenInsert):
  0000: 27 73 69 6d 70 6c 65 27 0a 20 20 20 20 7f 7f 7f   'simple'.    ...
  0010: 7f 20 20 20 20 20 ee ee ee ee ee 6c 6c 78 6c 69   .     .....llxli
  0020: 6e 6b 3a 68 72 65 66 20 20 20 43 44 41 54 41 06   nk:href   CDATA.
  0030: 00 00 00 31 32 37 37 37 32 2e 78 6d 86 5c 0a 3c   ...127772.xm.\.<
Seed 4 (id=00187c32cbdbd121, size=492 bytes, fuzzer=naive, trial=2, discovered_at=5331s, mutation_op=ByteNegMutator,ByteNegMutator,TokenInsert,ByteIncMutator,WordAddMutator,TokenInsert,BytesInsertMutator):
  0000: 74 74 70 3a 75 2f 2f 2f 2f 2b 2f 2f 2f 2f 2f 2f   ttp:u////+//////
  0010: 2f 2f 74 74 70 3a 2f 2f 2f 2f 2e 2b 2f 30 2f 2f   //ttp:////.+/0//
  0020: 2f 2f 2f 2f 2f 2f 2f 66 77 6b 65 3e 0a 3c 2f 61   ///////fwke>.</a
  0030: 5e 0a 0a 55 54 46 38 5c 0a 78 6c 69 6e 6b 3a 74   ^..UTF8\.xlink:t
Seed 5 (id=0009d2d8a40e2949, size=209 bytes, fuzzer=naive, trial=2, discovered_at=6150s, mutation_op=TokenInsert,BytesInsertMutator):
  0000: 27 2f 2f 2f 2f 2f 2f 2f 2f 2f 2f 68 74 74 70 3a   '//////////http:
  0010: 2f 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 33 2e   /'http://www.w3.
  0020: 6f 72 67 2f 25 39 3a 39 2f 78 6c 69 6e 6b 27 0a   org/%9:9/xlink'.
  0030: 20 fe 20 20 20 20 20 06 14 00 00 31 20 20 06 11    .     ....1  ..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f9(.)x2 ff(.)x1 33(3)x1             27(')x2 38(8)x1 06(.)x1 74(t)x1 +5u  DIFFER
   0x0001  00(.)x2 7f(.)x1 2e(.)x1             74(t)x3 38(8)x1 00(.)x1 73(s)x1 +4u  PARTIAL
   0x0002  ff(.)x1 00(.)x1 6f(o)x1 37(7)x1     38(8)x1 00(.)x1 69(i)x1 70(p)x1 +6u  PARTIAL
   0x0003  ff(.)x1 00(.)x1 72(r)x1 37(7)x1     3a(:)x2 38(8)x1 00(.)x1 6d(m)x1 +5u  PARTIAL
   0x0004  31(1)x2 67(g)x1 37(7)x1             70(p)x2 2f(/)x2 38(8)x1 31(1)x1 +4u  PARTIAL
   0x0005  32(2)x3 00(.)x1                     2f(/)x2 74(t)x2 49(I)x1 32(2)x1 +4u  PARTIAL
   0x0006  c8(.)x1 37(7)x1 02(.)x1 2e(.)x1     2f(/)x3 22(")x1 37(7)x1 65(e)x1 +4u  PARTIAL
   0x0007  37(7)x2 39(9)x1 78(x)x1             2f(/)x4 31(1)x1 37(7)x1 27(')x1 +3u  PARTIAL
   0x0008  37(7)x2 39(9)x1 6d(m)x1             2f(/)x3 0a(.)x2 00(.)x1 37(7)x1 +3u  PARTIAL
   0x0009  32(2)x2 39(9)x1 6c(l)x1             2f(/)x2 31(1)x1 32(2)x1 20( )x1 +5u  PARTIAL
   0x000a  2e(.)x2 2f(/)x1 5c(\)x1             2f(/)x5 32(2)x1 2e(.)x1 20( )x1 +2u  PARTIAL
   0x000b  78(x)x3 0a(.)x1                     37(7)x1 78(x)x1 20( )x1 2f(/)x1 +6u  PARTIAL
   0x000c  6d(m)x2 3a(:)x1 3c(<)x1             2d(-)x2 37(7)x1 6d(m)x1 20( )x1 +5u  PARTIAL
   0x000d  6c(l)x2 69(i)x1 3f(?)x1             37(7)x1 6c(l)x1 7f(.)x1 2f(/)x1 +6u  PARTIAL
   0x000e  5c(\)x2 6e(n)x1 78(x)x1             2f(/)x2 2d(-)x2 32(2)x1 5c(\)x1 +4u  PARTIAL
   0x000f  0a(.)x2 6b(k)x1 6d(m)x1             2e(.)x2 0a(.)x1 7f(.)x1 2f(/)x1 +5u  PARTIAL
   0x0010  3c(<)x2 27(')x1 6c(l)x1             2f(/)x4 3c(<)x2 78(x)x1 7f(.)x1 +2u  PARTIAL
   0x0011  3f(?)x2 0a(.)x1 20( )x1             6d(m)x1 3f(?)x1 20( )x1 2f(/)x1 +6u  PARTIAL
   0x0012  78(x)x2 20( )x1 76(v)x1             20( )x2 6c(l)x1 78(x)x1 74(t)x1 +5u  PARTIAL
   0x0013  6d(m)x2 20( )x1 65(e)x1             20( )x2 74(t)x2 5c(\)x1 6d(m)x1 +4u  PARTIAL
   0x0014  6c(l)x2 20( )x1 72(r)x1             20( )x2 0a(.)x1 6c(l)x1 70(p)x1 +5u  PARTIAL
   0x0015  20( )x3 73(s)x1                     20( )x3 2b(+)x2 3c(<)x1 3a(:)x1 +3u  PARTIAL
   0x0016  76(v)x2 20( )x1 69(i)x1             3f(?)x1 76(v)x1 ee(.)x1 2f(/)x1 +6u  PARTIAL
   0x0017  65(e)x2 20( )x1 6f(o)x1             2f(/)x3 78(x)x1 65(e)x1 ee(.)x1 +4u  PARTIAL
   0x0018  72(r)x2 20( )x1 6e(n)x1             2f(/)x2 6d(m)x1 72(r)x1 ee(.)x1 +5u  PARTIAL
   0x0019  73(s)x2 20( )x1 3d(=)x1             6c(l)x1 73(s)x1 ee(.)x1 2f(/)x1 +6u  PARTIAL
   0x001a  69(i)x2 78(x)x1 22(")x1             20( )x1 69(i)x1 ee(.)x1 2e(.)x1 +6u  PARTIAL
   0x001b  6f(o)x2 6d(m)x1 31(1)x1             6c(l)x2 76(v)x1 6f(o)x1 2b(+)x1 +5u  PARTIAL
   0x001c  6e(n)x2 6c(l)x1 2e(.)x1             65(e)x1 6e(n)x1 6c(l)x1 2f(/)x1 +6u  PARTIAL
   0x001d  3d(=)x2 6e(n)x1 30(0)x1             72(r)x1 3d(=)x1 78(x)x1 30(0)x1 +6u  PARTIAL
   0x001e  22(")x3 73(s)x1                     73(s)x1 22(")x1 6c(l)x1 2f(/)x1 +6u  PARTIAL
   0x001f  31(1)x2 28(()x1 3f(?)x1             69(i)x2 31(1)x1 2f(/)x1 2e(.)x1 +4u  PARTIAL
   0x0020  2e(.)x2 78(x)x1 3e(>)x1             6f(o)x2 2e(.)x1 6e(n)x1 2f(/)x1 +4u  PARTIAL
   0x0021  30(0)x2 6c(l)x1 0a(.)x1             6e(n)x1 30(0)x1 6b(k)x1 2f(/)x1 +5u  PARTIAL
   0x0022  22(")x2 69(i)x1 3c(<)x1             2f(/)x2 3d(=)x1 22(")x1 3a(:)x1 +4u  PARTIAL
   0x0023  3f(?)x2 6e(n)x1 21(!)x1             2f(/)x2 22(")x1 3f(?)x1 68(h)x1 +4u  PARTIAL
   0x0024  3e(>)x2 6b(k)x1 44(D)x1             31(1)x1 3e(>)x1 72(r)x1 2f(/)x1 +5u  PARTIAL
   0x0025  0a(.)x2 20( )x1 4f(O)x1             2f(/)x2 2e(.)x1 0a(.)x1 65(e)x1 +4u  PARTIAL
   0x0026  3c(<)x2 20( )x1 43(C)x1             30(0)x1 3c(<)x1 66(f)x1 2f(/)x1 +5u  PARTIAL
   0x0027  21(!)x2 43(C)x1 54(T)x1             22(")x1 21(!)x1 20( )x1 66(f)x1 +5u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7250.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7250,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7250 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7250 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7250 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).