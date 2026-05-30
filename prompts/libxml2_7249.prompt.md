==== BLOCKER ====
Target: libxml2
Branch ID: 7249
Location: /src/libxml2/xmlreader.c:472:9
Enclosing function: xmlreader.c:xmlTextReaderFreeDoc
Source line:     if (cur->ids != NULL) xmlFreeIDTable((xmlIDTablePtr) cur->ids);
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           4        6          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.60h  loser=24.00h
  avg hitcount on branch: winner=14  loser=0
  prob_div=1.00  dur_div=13.40h  hit_div=14
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7249/{W,L}/branch_coverage_show.txt

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
[B]   472      if (cur->ids != NULL) xmlFreeIDTable((xmlIDTablePtr) cur->ids); <-- BLOCKER
[B]   473      cur->ids = NULL;
[B]   474      if (cur->refs != NULL) xmlFreeRefTable((xmlRefTablePtr) cur->refs);
[B]   475      cur->refs = NULL;
[B]   476      extSubset = cur->extSubset;
[B]   477      intSubset = cur->intSubset;
[B]   478      if (intSubset == extSubset)
[B]   479  	extSubset = NULL;
[B]   480      if (extSubset != NULL) {
[ ]   481  	xmlUnlinkNode((xmlNodePtr) cur->extSubset);
[ ]   482  	cur->extSubset = NULL;
[ ]   483  	xmlFreeDtd(extSubset);
[ ]   484      }
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
[B]   496      if (cur->oldNs != NULL) xmlFreeNsList(cur->oldNs);
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
[ ]  2233  #ifdef LIBXML_REGEXP_ENABLED
[ ]  2234              while (reader->ctxt->vctxt.vstateNr > 0)
[ ]  2235                  xmlValidatePopElement(&reader->ctxt->vctxt, NULL, NULL, NULL);
[ ]  2236  #endif /* LIBXML_REGEXP_ENABLED */
[ ]  2237  	    xmlFree(reader->ctxt->vctxt.vstateTab);
[ ]  2238  	    reader->ctxt->vctxt.vstateTab = NULL;
[ ]  2239  	    reader->ctxt->vctxt.vstateMax = 0;
[ ]  2240  	}
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
       4        20  xmlreader.c:xmlTextReaderStartElementNs  (/src/libxml2/xmlreader.c:664-682)
       9         3  xmlreader.c:xmlTextReaderFreeNodeList  (/src/libxml2/xmlreader.c:291-375)
       5         0  xmlreader.c:xmlTextReaderFreeProp  (/src/libxml2/xmlreader.c:238-262)
       5         0  xmlreader.c:xmlTextReaderFreePropList  (/src/libxml2/xmlreader.c:272-280)

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
  d=2   L2231  T=0 F=4  T=0 F=10  if ((reader->ctxt->vctxt.vstateTab != NULL) &&
  d=2   L2243  T=4 F=0  T=10 F=0  if (reader->ctxt->myDoc != NULL) {
  d=2   L2244  T=4 F=0  T=10 F=0  if (reader->preserve == 0)
  d=2   L2249  T=4 F=0  T=10 F=0  if ((reader->input != NULL)  && (reader->allocs & XML_TEX...
  d=2   L2249  T=4 F=0  T=10 F=0  if ((reader->input != NULL)  && (reader->allocs & XML_TEX...
--- d=1  xmlreader.c:xmlTextReaderFreeDoc  (/src/libxml2/xmlreader.c:461-501) ---
  d=1   L 464  T=0 F=4  T=0 F=10  if (cur == NULL) return;
  d=1   L 466  T=0 F=4  T=0 F=10  if ((__xmlRegisterCallbacks) && (xmlDeregisterNodeDefault...
  d=1   L 472  T=4 F=0  T=0 F=10  if (cur->ids != NULL) xmlFreeIDTable((xmlIDTablePtr) cur-...  <-- BLOCKER
  d=1   L 474  T=0 F=4  T=0 F=10  if (cur->refs != NULL) xmlFreeRefTable((xmlRefTablePtr) c...
  d=1   L 478  T=1 F=3  T=9 F=1  if (intSubset == extSubset)
  d=1   L 480  T=0 F=4  T=0 F=10  if (extSubset != NULL) {
  d=1   L 485  T=3 F=1  T=1 F=9  if (intSubset != NULL) {
  d=1   L 491  T=4 F=0  T=3 F=7  if (cur->children != NULL) xmlTextReaderFreeNodeList(read...
  d=1   L 493  T=4 F=0  T=10 F=0  if (cur->version != NULL) xmlFree((char *) cur->version);
  d=1   L 494  T=0 F=4  T=0 F=10  if (cur->name != NULL) xmlFree((char *) cur->name);
  d=1   L 495  T=0 F=4  T=0 F=10  if (cur->encoding != NULL) xmlFree((char *) cur->encoding);
  d=1   L 496  T=4 F=0  T=0 F=10  if (cur->oldNs != NULL) xmlFreeNsList(cur->oldNs);
  d=1   L 497  T=0 F=4  T=0 F=10  if (cur->URL != NULL) xmlFree((char *) cur->URL);
  d=1   L 498  T=2 F=2  T=6 F=4  if (cur->dict != NULL) xmlDictFree(cur->dict);

[off-chain: 86 additional divergent branches across 9 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=31a0f4cf800d3991, size=133 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=53377s, mutation_op=BitFlipMutator,WordAddMutator,BytesExpandMutator,ByteRandMutator):
  0000: 73 69 7d 74 74 74 74 74 74 74 74 74 74 09 78 6d   si}tttttttttt.xm
  0010: 6c 3a 69 64 3d 22 20 3a 69 64 3d 22 26 26 73 69   l:id=" :id="&&si
  0020: 6d 70 6c 9b 29 20 e0 23 00 00 26 00 6b 3a 74 5c   mpl.) .#..&.k:t\
  0030: 0a 3c 74 f6 74 74 74 74 74 74 74 74 09 78 6d 6c   .<t.tttttttt.xml
Seed 2 (id=168e9a373a411e74, size=333 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=53552s, mutation_op=ByteRandMutator,BytesCopyMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   72.xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 5d 37 37 32 2e 64 3a    ".:d./12]772.d:
Seed 3 (id=c0f4fb619d9e55cd, size=345 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=53552s, mutation_op=WordAddMutator,ByteFlipMutator,WordInterestingMutator,WordInterestingMutator,ByteFlipMutator,BytesRandInsertMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   72.xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 5d 37 37 32 2e 64 3a    ".:d./12]772.d:
Seed 4 (id=73218d6bef4b5ebe, size=322 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=71226s, mutation_op=WordAddMutator,BytesSetMutator,ByteAddMutator,BytesSwapMutator,ByteInterestingMutator,ByteInterestingMutator):
  0000: 7f 00 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   ...xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0d 2f 31 32 26 37 37 32 2e 64 3a    ".:d./12&772.d:

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0033fc739d88a180, size=145 bytes, fuzzer=value_profile, trial=1, discovered_at=4748s, mutation_op=ByteInterestingMutator,BytesSetMutator,ByteInterestingMutator,TokenInsert):
  0000: 3e 0a 0a 5c 09 29 3c 21 45 4c 45 4d 45 4e 20 20   >..\.)<!ELEMEN  
  0010: 20 20 20 4c 4c 4c 4c 4c 4c 4c 4c 4c 20 78 f9 ff      LLLLLLLLL x..
  0020: ff ff 54 20 62 20 1e 23 50 43 44 44 20 27 73 5f   ..T b .#PCDD 's_
  0030: 10 70 6c 65 27 0a 5f 10 70 6c 65 27 0a 20 20 20   .ple'._.ple'.   
Seed 2 (id=002597db0252745e, size=95 bytes, fuzzer=value_profile, trial=1, discovered_at=6254s, mutation_op=ByteRandMutator,ByteAddMutator,ByteIncMutator,BytesCopyMutator):
  0000: 86 85 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 77   ..'http://www.ww
  0010: 77 2e 77 33 2e 6f 72 67 2f 31 39 39 39 2f 78 6c   w.w3.org/1999/xl
  0020: 69 6e 6b 27 0a 20 20 20 20 20 20 20 20 20 20 20   ink'.           
  0030: 20 77 33 59 cb ff ff 2f 31 39 7f 39 2f 78 2f 2f    w3Y.../19.9/x//
Seed 3 (id=0020e53b7ea9ef52, size=64 bytes, fuzzer=value_profile, trial=1, discovered_at=11270s, mutation_op=ByteNegMutator,WordInterestingMutator,ByteFlipMutator,BytesRandSetMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 23 49 4d 50 69 00 00 69 69 69 69 4d 42 45 44 3e   #IMPi..iiiiMBED>
  0010: 0a 0a 5c 0a 0a 0a 3c 61 3e 0a 20 20 3c 62 20 3a   ..\...<a>.  <b :
  0020: 23 49 4d 50 a1 5e 5e 5e 5e 5e 5e 5e 5e 5e 5e 5e   #IMP.^^^^^^^^^^^
  0030: 5e 5e 5e 5e 6b 20 20 3c 61 3e 0a 20 e0 3c 62 20   ^^^^k  <a>. .<b 
Seed 4 (id=002336d5b9efcfba, size=339 bytes, fuzzer=value_profile, trial=1, discovered_at=11827s, mutation_op=BytesDeleteMutator,BytesExpandMutator):
  0000: 43 43 43 43 43 00 00 00 31 20 42 20 20 20 32 37   CCCCC...1 B   27
  0010: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0020: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c   ersion="1.0"?>.<
  0030: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE
Seed 5 (id=003abf67f067c918, size=51 bytes, fuzzer=value_profile, trial=1, discovered_at=20486s, mutation_op=BitFlipMutator,ByteAddMutator,ByteInterestingMutator,BytesExpandMutator,QwordAddMutator,ByteIncMutator,BytesCopyMutator):
  0000: 77 77 78 6c 69 70 70 5a 3a 2f 2f 77 3f ff 77 77   wwxlippZ://w?.ww
  0010: 78 00 ef 06 6d 6c 5c 0a 3b 2f 77 40 3f fe ff 10   x...ml\.;/w@?...
  0020: 00 ef 06 6d 6c 5c 0a 3b 3f 3a 26 3a 5c 0a 3b 3f   ...ml\.;?:&:\.;?
  0030: 3a 26 3a                                          :&:


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  37(7)x2 73(s)x1 7f(.)x1             3e(>)x1 86(.)x1 23(#)x1 43(C)x1 +6u  DIFFER
   0x0001  32(2)x2 69(i)x1 00(.)x1             0a(.)x1 85(.)x1 49(I)x1 43(C)x1 +6u  DIFFER
   0x0002  2e(.)x3 7d(})x1                     27(')x3 0a(.)x1 4d(M)x1 43(C)x1 +4u  DIFFER
   0x0003  78(x)x3 74(t)x1                     68(h)x3 5c(\)x1 50(P)x1 43(C)x1 +4u  PARTIAL
   0x0004  6d(m)x3 74(t)x1                     74(t)x3 69(i)x2 09(.)x1 43(C)x1 +3u  PARTIAL
   0x0005  6c(l)x3 74(t)x1                     74(t)x3 00(.)x2 70(p)x2 29())x1 +2u  PARTIAL
   0x0006  5c(\)x3 74(t)x1                     70(p)x4 3c(<)x2 00(.)x2 3a(:)x1 +1u  DIFFER
   0x0007  0a(.)x3 74(t)x1                     3a(:)x3 21(!)x1 69(i)x1 00(.)x1 +4u  DIFFER
   0x0008  3c(<)x3 74(t)x1                     2f(/)x4 45(E)x1 69(i)x1 31(1)x1 +3u  PARTIAL
   0x0009  3f(?)x3 74(t)x1                     2f(/)x4 4c(L)x1 69(i)x1 20( )x1 +3u  DIFFER
   0x000a  78(x)x3 74(t)x1                     77(w)x3 45(E)x1 69(i)x1 42(B)x1 +4u  DIFFER
   0x000b  0a(.)x3 74(t)x1                     77(w)x4 4d(M)x2 20( )x1 6c(l)x1 +2u  DIFFER
   0x000c  6c(l)x3 74(t)x1                     77(w)x3 45(E)x1 42(B)x1 20( )x1 +4u  DIFFER
   0x000d  3a(:)x3 09(.)x1                     2e(.)x2 4e(N)x1 45(E)x1 20( )x1 +5u  DIFFER
   0x000e  76(v)x3 78(x)x1                     77(w)x2 20( )x1 44(D)x1 32(2)x1 +5u  DIFFER
   0x000f  65(e)x3 6d(m)x1                     20( )x2 77(w)x2 3e(>)x1 37(7)x1 +4u  DIFFER
   0x0010  72(r)x3 6c(l)x1                     20( )x2 77(w)x1 0a(.)x1 37(7)x1 +5u  DIFFER
   0x0011  73(s)x3 3a(:)x1                     20( )x1 2e(.)x1 0a(.)x1 37(7)x1 +6u  DIFFER
   0x0012  69(i)x4                             77(w)x2 20( )x1 5c(\)x1 32(2)x1 +5u  DIFFER
   0x0013  6f(o)x3 64(d)x1                     33(3)x2 2e(.)x2 4c(L)x1 0a(.)x1 +4u  DIFFER
   0x0014  6e(n)x3 3d(=)x1                     4c(L)x1 2e(.)x1 0a(.)x1 78(x)x1 +6u  PARTIAL
   0x0015  3d(=)x3 22(")x1                     0a(.)x2 7e(~)x2 4c(L)x1 6f(o)x1 +4u  DIFFER
   0x0016  22(")x3 20( )x1                     3c(<)x2 4c(L)x1 72(r)x1 6c(l)x1 +5u  DIFFER
   0x0017  31(1)x3 3a(:)x1                     68(h)x2 4c(L)x1 67(g)x1 61(a)x1 +5u  DIFFER
   0x0018  2e(.)x3 69(i)x1                     4c(L)x1 2f(/)x1 3e(>)x1 0a(.)x1 +6u  PARTIAL
   0x0019  30(0)x3 64(d)x1                     4c(L)x1 31(1)x1 0a(.)x1 3c(<)x1 +6u  DIFFER
   0x001a  3c(<)x3 3d(=)x1                     77(w)x2 4c(L)x1 39(9)x1 20( )x1 +5u  DIFFER
   0x001b  3f(?)x3 22(")x1                     39(9)x2 20( )x2 4c(L)x1 78(x)x1 +4u  DIFFER
   0x001c  3e(>)x3 26(&)x1                     20( )x2 39(9)x1 3c(<)x1 6d(m)x1 +5u  PARTIAL
   0x001d  0a(.)x3 26(&)x1                     78(x)x1 2f(/)x1 62(b)x1 6c(l)x1 +6u  PARTIAL
   0x001e  3c(<)x3 73(s)x1                     20( )x3 f9(.)x1 78(x)x1 ff(.)x1 +4u  DIFFER
   0x001f  21(!)x3 69(i)x1                     7e(~)x2 ff(.)x1 6c(l)x1 3a(:)x1 +5u  DIFFER
   0x0020  44(D)x3 6d(m)x1                     ff(.)x1 69(i)x1 23(#)x1 65(e)x1 +6u  DIFFER
   0x0021  4f(O)x3 70(p)x1                     ff(.)x1 6e(n)x1 49(I)x1 72(r)x1 +6u  DIFFER
   0x0022  43(C)x3 6c(l)x1                     54(T)x1 6b(k)x1 4d(M)x1 73(s)x1 +6u  PARTIAL
   0x0023  54(T)x3 9b(.)x1                     20( )x2 27(')x1 50(P)x1 69(i)x1 +5u  DIFFER
   0x0024  59(Y)x3 29())x1                     62(b)x1 0a(.)x1 a1(.)x1 6f(o)x1 +6u  DIFFER
   0x0025  50(P)x3 20( )x1                     20( )x2 5e(^)x1 6e(n)x1 5c(\)x1 +5u  PARTIAL
   0x0026  45(E)x3 e0(.)x1                     1e(.)x1 20( )x1 5e(^)x1 3d(=)x1 +6u  DIFFER
   0x0027  3a(:)x3 23(#)x1                     23(#)x1 20( )x1 5e(^)x1 22(")x1 +6u  PARTIAL
   ... (24 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7249.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7249,
  "target": "libxml2",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7249 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7249 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7249 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).