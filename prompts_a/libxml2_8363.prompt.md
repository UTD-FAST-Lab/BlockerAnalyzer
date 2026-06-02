==== BLOCKER ====
Target: libxml2
Branch ID: 8363
Location: /src/libxml2/valid.c:2607:6
Enclosing function: valid.c:xmlValidNormalizeString
Source line: 	if (*src == 0x20) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        4          6  REFERENCE
cmplog                           0       10          0  loser (grimoire_structural vs grimoire)
value_profile                    2        6          2  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        3        5          2  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             1        2          7  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             0        6          4  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.00h  loser=16.90h
  avg hitcount on branch: winner=14  loser=0
  prob_div=0.80  dur_div=6.90h  hit_div=14
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/8363/{W,L}/branch_coverage_show.txt

--- Enclosing function: valid.c:xmlValidNormalizeString (/src/libxml2/valid.c:2596-2616) ---
[ ]  2594   */
[ ]  2595  static void
[B]  2596  xmlValidNormalizeString(xmlChar *str) {
[B]  2597      xmlChar *dst;
[B]  2598      const xmlChar *src;
[ ]  2599  
[B]  2600      if (str == NULL)
[ ]  2601          return;
[B]  2602      src = str;
[B]  2603      dst = str;
[ ]  2604  
[B]  2605      while (*src == 0x20) src++;
[B]  2606      while (*src != 0) {
[B]  2607  	if (*src == 0x20) { <-- BLOCKER
[W]  2608  	    while (*src == 0x20) src++;
[W]  2609  	    if (*src != 0)
[W]  2610  		*dst++ = 0x20;
[B]  2611  	} else {
[B]  2612  	    *dst++ = *src++;
[B]  2613  	}
[B]  2614      }
[B]  2615      *dst = 0;
[B]  2616  }

--- Caller (1 hop): xmlValidCtxtNormalizeAttributeValue (/src/libxml2/valid.c:4061-4111, calls valid.c:xmlValidNormalizeString at line 4103) (±10 around call site) ---
[B]  4093      }
[ ]  4094  
[B]  4095      if (attrDecl == NULL)
[L]  4096  	return(NULL);
[B]  4097      if (attrDecl->atype == XML_ATTRIBUTE_CDATA)
[B]  4098  	return(NULL);
[ ]  4099  
[B]  4100      ret = xmlStrdup(value);
[B]  4101      if (ret == NULL)
[ ]  4102  	return(NULL);
[B]  4103      xmlValidNormalizeString(ret); <-- CALL
[B]  4104      if ((doc->standalone) && (extsubset == 1) && (!xmlStrEqual(value, ret))) {
[ ]  4105  	xmlErrValidNode(ctxt, elem, XML_DTD_NOT_STANDALONE,
[ ]  4106  "standalone: %s on %s value had to be normalized based on external subset declaration\n",
[ ]  4107  	       name, elem->name, NULL);
[ ]  4108  	ctxt->valid = 0;
[ ]  4109      }
[B]  4110      return(ret);
[B]  4111  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlRemoveID  (/src/libxml2/valid.c:2828-2855, calls valid.c:xmlValidNormalizeString at line 2843)
hop 2  xmlValidCtxtNormalizeAttributeValue  (/src/libxml2/valid.c:4061-4111, calls valid.c:xmlValidNormalizeString at line 4103)
hop 3  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438, calls xmlValidCtxtNormalizeAttributeValue at line 1153)
hop 3  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199, calls xmlValidCtxtNormalizeAttributeValue at line 2131)
hop 3  xmlFreeProp  (/src/libxml2/tree.c:2115-2131, calls xmlRemoveID at line 2126)
hop 3  xmlSetTreeDoc  (/src/libxml2/tree.c:2862-2917, calls xmlRemoveID at line 2875)
hop 4  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 4  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)
hop 4  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459, calls SAX2.c:xmlSAX2AttributeNs at line 2421)
hop 4  xmlParseBalancedChunkMemoryRecover  (/src/libxml2/parser.c:13557-13695, calls xmlSetTreeDoc at line 13678)
hop 4  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls xmlSetTreeDoc at line 7340)
hop 4  xmlFreePropList  (/src/libxml2/tree.c:2098-2106, calls xmlFreeProp at line 2103)
hop 4  xmlRemoveProp  (/src/libxml2/tree.c:2143-2182, calls xmlFreeProp at line 2164)
hop 5  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseReference at line 10020)
hop 5  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseReference at line 11768)
hop 5  xmlParseBalancedChunkMemory  (/src/libxml2/parser.c:13094-13097, calls xmlParseBalancedChunkMemoryRecover at line 13095)
hop 5  tree.c:xmlAddPropSibling  (/src/libxml2/tree.c:3036-3071, calls xmlRemoveProp at line 3068)
hop 5  xmlFreeNode  (/src/libxml2/tree.c:3840-3897, calls xmlFreePropList at line 3877)
hop 5  xmlFreeNodeList  (/src/libxml2/tree.c:3757-3830, calls xmlFreePropList at line 3793)
hop 6  entities.c:xmlFreeEntity  (/src/libxml2/entities.c:119-146, calls xmlFreeNodeList at line 131)
hop 6  parser.c:xmlParseBalancedChunkMemoryInternal  (/src/libxml2/parser.c:13123-13298, calls xmlFreeNode at line 13269)
hop 6  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 6  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 6  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 6  xmlParseInNodeContext  (/src/libxml2/parser.c:13321-13526, calls xmlFreeNode at line 13510)
hop 6  xmlAddNextSibling  (/src/libxml2/tree.c:3090-3149, calls tree.c:xmlAddPropSibling at line 3134)
hop 6  xmlAddPrevSibling  (/src/libxml2/tree.c:3170-3230, calls tree.c:xmlAddPropSibling at line 3214)
hop 7  htmlSetMetaEncoding  (/src/libxml2/HTMLtree.c:162-295, calls xmlAddPrevSibling at line 277)
hop 7  entities.c:xmlAddEntity  (/src/libxml2/entities.c:203-285, calls entities.c:xmlFreeEntity at line 281)
hop 7  entities.c:xmlFreeEntityWrapper  (/src/libxml2/entities.c:933-936, calls entities.c:xmlFreeEntity at line 935)
hop 7  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 7  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 7  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 7  relaxng.c:xmlRelaxNGCleanupTree  (/src/libxml2/relaxng.c:7043-7472, calls xmlAddNextSibling at line 7389)
hop 7  xmlStringLenGetNodeList  (/src/libxml2/tree.c:1269-1487, calls xmlAddNextSibling at line 1402)
hop 8  xmlAddDocEntity  (/src/libxml2/entities.c:388-419, calls entities.c:xmlAddEntity at line 403)
hop 8  xmlAddDtdEntity  (/src/libxml2/entities.c:339-370, calls entities.c:xmlAddEntity at line 354)
hop 8  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 8  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 8  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 8  relaxng.c:xmlRelaxNGCleanupDoc  (/src/libxml2/relaxng.c:7486-7500, calls relaxng.c:xmlRelaxNGCleanupTree at line 7498)
hop 8  xmlNodeSetContentLen  (/src/libxml2/tree.c:5839-5894, calls xmlStringLenGetNodeList at line 5852)
hop 8  xmlsave.c:htmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:750-799, calls htmlSetMetaEncoding at line 771)
hop 8  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225, calls htmlSetMetaEncoding at line 1109)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      24       192  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
      48       210  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      12        90  xmlGetDtdQElementDesc  (/src/libxml2/valid.c:3349-3357)
       6        60  xmlGetDtdQAttrDesc  (/src/libxml2/valid.c:3410-3418)
       6        48  xmlValidCtxtNormalizeAttributeValue  (/src/libxml2/valid.c:4061-4111)
      12        51  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883)
       9        42  valid.c:xmlFreeAttribute  (/src/libxml2/valid.c:1907-1939)
       9        42  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172)
       9        42  valid.c:xmlFreeAttributeTableEntry  (/src/libxml2/valid.c:2175-2177)
       9        42  valid.c:xmlGetDtdElementDesc2  (/src/libxml2/valid.c:3280-3334)
      14        46  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
       6        33  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)
       6        30  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
       6        30  valid.c:xmlFreeElement  (/src/libxml2/valid.c:1382-1395)
       6        30  xmlAddElementDecl  (/src/libxml2/valid.c:1414-1620)
... (25 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlValidCtxtNormalizeAttributeValue  (/src/libxml2/valid.c:4061-4111) ---
  d=2   L4066  T=0 F=6  T=0 F=48  if (doc == NULL) return(NULL);
  d=2   L4067  T=0 F=6  T=0 F=48  if (elem == NULL) return(NULL);
  d=2   L4068  T=0 F=6  T=0 F=48  if (name == NULL) return(NULL);
  d=2   L4069  T=0 F=6  T=0 F=48  if (value == NULL) return(NULL);
  d=2   L4071  T=0 F=6  T=0 F=48  if ((elem->ns != NULL) && (elem->ns->prefix != NULL)) {
  d=2   L4087  T=6 F=0  T=48 F=0  if ((attrDecl == NULL) && (doc->intSubset != NULL))
  d=2   L4087  T=6 F=0  T=48 F=0  if ((attrDecl == NULL) && (doc->intSubset != NULL))
  d=2   L4089  T=6 F=0  T=48 F=0  if ((attrDecl == NULL) && (doc->extSubset != NULL)) {
  d=2   L4089  T=6 F=0  T=48 F=0  if ((attrDecl == NULL) && (doc->extSubset != NULL)) {
  d=2   L4091  T=6 F=0  T=45 F=3  if (attrDecl != NULL)
  d=2   L4095  T=0 F=6  T=3 F=45  if (attrDecl == NULL)
  d=2   L4097  T=3 F=3  T=24 F=21  if (attrDecl->atype == XML_ATTRIBUTE_CDATA)
  d=2   L4101  T=0 F=3  T=0 F=21  if (ret == NULL)
  d=2   L4104  T=0 F=3  T=0 F=21  if ((doc->standalone) && (extsubset == 1) && (!xmlStrEqua...
  d=2   L4104  T=3 F=0  T=21 F=0  if ((doc->standalone) && (extsubset == 1) && (!xmlStrEqua...
  d=2   L4104  T=3 F=0  T=21 F=0  if ((doc->standalone) && (extsubset == 1) && (!xmlStrEqua...
--- d=1  valid.c:xmlValidNormalizeString  (/src/libxml2/valid.c:2596-2616) ---
  d=1   L2600  T=0 F=3  T=0 F=21  if (str == NULL)
  d=1   L2605  T=0 F=3  T=0 F=21  while (*src == 0x20) src++;
  d=1   L2606  T=18 F=3  T=135 F=21  while (*src != 0) {
  d=1   L2607  T=3 F=15  T=0 F=135  if (*src == 0x20) {  <-- BLOCKER
  d=1   L2608  T=3 F=3  T=0 F=0  while (*src == 0x20) src++;
  d=1   L2609  T=3 F=0  T=0 F=0  if (*src != 0)

[off-chain: 458 additional divergent branches across 40 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=e473b10f560d34ac, size=207 bytes, fuzzer=grimoire, trial=3, discovered_at=16487s, mutation_op=I2SRandReplace,I2SRandReplace):
  0000: f9 ff ff 6c 5c 0a 3c 3f 6c 3f 3e 3c 21 44 4f 43   ...l\.<?l?><!DOC
  0010: 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64 74   TYPEa SYSTEM "dt
  0020: 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e 3c   ds/127772.dtd"><
  0030: 61 3e 3c 62 20 78 6c 69 6e 6b 3a 68 72 27 66 3d   a><b xlink:hr'f=

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=51fd9b36079604e3, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=3541s, mutation_op=ByteAddMutator,DwordInterestingMutator):
  0000: ff 7f ff ff 31 32 c8 37 37 32 2e 78 6d 6c 5c 0a   ....12.772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=4424d26cf5012e01, size=417 bytes, fuzzer=cmplog, trial=2, discovered_at=8861s, mutation_op=ByteFlipMutator):
  0000: 1f 0a 64 73 2f 31 32 2f 37 37 32 2e 64 74 64 22   ..ds/12/772.dtd"
  0010: 3e 09 0a 3c 61 3e 0a 20 20 3c 09 20 78 6c 69 ff   >..<a>.  <. xli.
  0020: 6b 0d 68 72 65 66 3d 22 68 ff 74 70 3a 2f 2f 66   k.href="h.tp://f
  0030: 06 00 00 00 31 32 37 37 37 cd 27 78 6d 6c 5c 0a   ....12777.'xml\.
Seed 3 (id=424617adc23850db, size=383 bytes, fuzzer=cmplog, trial=2, discovered_at=10387s, mutation_op=TokenReplace,DwordInterestingMutator,ByteFlipMutator,CrossoverReplaceMutator):
  0000: 6b 3a 74 79 70 06 00 00 00 31 32 37 37 37 32 2e   k:typ....127772.
  0010: 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69   xml\.<?xml versi
  0020: 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43   on="1.0"?>.<!DOC
  0030: 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22 64   TYPE a SYSTEM "d
Seed 4 (id=ce695176842cff63, size=368 bytes, fuzzer=cmplog, trial=3, discovered_at=60789s, mutation_op=BytesRandInsertMutator):
  0000: 7e 7e 7e 7e 7e 7e 7e 7e 7e 32 2e 78 6d 6c 5c 0a   ~~~~~~~~~2.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=d40b06119b1f9860, size=391 bytes, fuzzer=cmplog, trial=2, discovered_at=70768s, mutation_op=WordInterestingMutator):
  0000: 6b 3a 74 79 70 06 00 00 00 31 32 37 37 37 32 2e   k:typ....127772.
  0010: 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69   xml\.<?xml versi
  0020: 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43   on="1.0"?>.<!DOC
  0030: 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22 64   TYPE a SYSTEM "d


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f9(.)x1                             6b(k)x2 ff(.)x1 1f(.)x1 7e(~)x1     DIFFER
   0x0001  ff(.)x1                             3a(:)x2 7f(.)x1 0a(.)x1 7e(~)x1     DIFFER
   0x0002  ff(.)x1                             74(t)x2 ff(.)x1 64(d)x1 7e(~)x1     PARTIAL
   0x0003  6c(l)x1                             79(y)x2 ff(.)x1 73(s)x1 7e(~)x1     DIFFER
   0x0004  5c(\)x1                             70(p)x2 31(1)x1 2f(/)x1 7e(~)x1     DIFFER
   0x0005  0a(.)x1                             06(.)x2 32(2)x1 31(1)x1 7e(~)x1     DIFFER
   0x0006  3c(<)x1                             00(.)x2 c8(.)x1 32(2)x1 7e(~)x1     DIFFER
   0x0007  3f(?)x1                             00(.)x2 37(7)x1 2f(/)x1 7e(~)x1     DIFFER
   0x0008  6c(l)x1                             37(7)x2 00(.)x2 7e(~)x1             DIFFER
   0x0009  3f(?)x1                             32(2)x2 31(1)x2 37(7)x1             DIFFER
   0x000a  3e(>)x1                             32(2)x3 2e(.)x2                     DIFFER
   0x000b  3c(<)x1                             78(x)x2 37(7)x2 2e(.)x1             DIFFER
   0x000c  21(!)x1                             6d(m)x2 37(7)x2 64(d)x1             DIFFER
   0x000d  44(D)x1                             6c(l)x2 37(7)x2 74(t)x1             DIFFER
   0x000e  4f(O)x1                             5c(\)x2 32(2)x2 64(d)x1             DIFFER
   0x000f  43(C)x1                             0a(.)x2 2e(.)x2 22(")x1             DIFFER
   0x0010  54(T)x1                             3c(<)x2 78(x)x2 3e(>)x1             DIFFER
   0x0011  59(Y)x1                             3f(?)x2 6d(m)x2 09(.)x1             DIFFER
   0x0012  50(P)x1                             78(x)x2 6c(l)x2 0a(.)x1             DIFFER
   0x0013  45(E)x1                             6d(m)x2 5c(\)x2 3c(<)x1             DIFFER
   0x0014  61(a)x1                             6c(l)x2 0a(.)x2 61(a)x1             PARTIAL
   0x0015  20( )x1                             20( )x2 3c(<)x2 3e(>)x1             PARTIAL
   0x0016  53(S)x1                             76(v)x2 3f(?)x2 0a(.)x1             DIFFER
   0x0017  59(Y)x1                             65(e)x2 78(x)x2 20( )x1             DIFFER
   0x0018  53(S)x1                             72(r)x2 6d(m)x2 20( )x1             DIFFER
   0x0019  54(T)x1                             73(s)x2 6c(l)x2 3c(<)x1             DIFFER
   0x001a  45(E)x1                             69(i)x2 20( )x2 09(.)x1             DIFFER
   0x001b  4d(M)x1                             6f(o)x2 76(v)x2 20( )x1             DIFFER
   0x001c  20( )x1                             6e(n)x2 65(e)x2 78(x)x1             DIFFER
   0x001d  22(")x1                             3d(=)x2 72(r)x2 6c(l)x1             DIFFER
   0x001e  64(d)x1                             22(")x2 73(s)x2 69(i)x1             DIFFER
   0x001f  74(t)x1                             31(1)x2 69(i)x2 ff(.)x1             DIFFER
   0x0020  64(d)x1                             2e(.)x2 6f(o)x2 6b(k)x1             DIFFER
   0x0021  73(s)x1                             30(0)x2 6e(n)x2 0d(.)x1             DIFFER
   0x0022  2f(/)x1                             22(")x2 3d(=)x2 68(h)x1             DIFFER
   0x0023  31(1)x1                             3f(?)x2 22(")x2 72(r)x1             DIFFER
   0x0024  32(2)x1                             3e(>)x2 31(1)x2 65(e)x1             DIFFER
   0x0025  37(7)x1                             0a(.)x2 2e(.)x2 66(f)x1             DIFFER
   0x0026  37(7)x1                             3c(<)x2 30(0)x2 3d(=)x1             DIFFER
   0x0027  37(7)x1                             22(")x3 21(!)x2                     DIFFER
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_8363.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8363,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8363 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8363 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8363 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).