==== BLOCKER ====
Target: libxml2
Branch ID: 6936
Location: /src/libxml2/tree.c:2125:31
Enclosing function: xmlFreeProp
Source line:     if ((cur->doc != NULL) && (cur->atype == XML_ATTRIBUTE_ID)) {
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
  avg duration blocked: winner=10.30h  loser=23.90h
  avg hitcount on branch: winner=34  loser=0
  prob_div=1.00  dur_div=13.60h  hit_div=34
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6936/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlFreeProp (/src/libxml2/tree.c:2115-2131) ---
[ ]  2113   */
[ ]  2114  void
[B]  2115  xmlFreeProp(xmlAttrPtr cur) {
[B]  2116      xmlDictPtr dict = NULL;
[B]  2117      if (cur == NULL) return;
[ ]  2118  
[B]  2119      if (cur->doc != NULL) dict = cur->doc->dict;
[ ]  2120  
[B]  2121      if ((__xmlRegisterCallbacks) && (xmlDeregisterNodeDefaultValue))
[ ]  2122  	xmlDeregisterNodeDefaultValue((xmlNodePtr)cur);
[ ]  2123  
[ ]  2124      /* Check for ID removal -> leading to invalid references ! */
[B]  2125      if ((cur->doc != NULL) && (cur->atype == XML_ATTRIBUTE_ID)) { <-- BLOCKER
[W]  2126  	    xmlRemoveID(cur->doc, cur);
[W]  2127      }
[B]  2128      if (cur->children != NULL) xmlFreeNodeList(cur->children);
[B]  2129      DICT_FREE(cur->name)
[B]  2130      xmlFree(cur);
[B]  2131  }

--- Caller (1 hop): xmlFreePropList (/src/libxml2/tree.c:2098-2106, calls xmlFreeProp at line 2103) (full body — short) ---
[B]  2098  xmlFreePropList(xmlAttrPtr cur) {
[B]  2099      xmlAttrPtr next;
[B]  2100      if (cur == NULL) return;
[B]  2101      while (cur != NULL) {
[B]  2102          next = cur->next;
[B]  2103          xmlFreeProp(cur); <-- CALL
[B]  2104  	cur = next;
[B]  2105      }
[B]  2106  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlFreePropList  (/src/libxml2/tree.c:2098-2106, calls xmlFreeProp at line 2103)
hop 2  xmlRemoveProp  (/src/libxml2/tree.c:2143-2182, calls xmlFreeProp at line 2164)
hop 3  tree.c:xmlAddPropSibling  (/src/libxml2/tree.c:3036-3071, calls xmlRemoveProp at line 3068)
hop 3  xmlFreeNode  (/src/libxml2/tree.c:3840-3897, calls xmlFreePropList at line 3877)
hop 3  xmlFreeNodeList  (/src/libxml2/tree.c:3757-3830, calls xmlFreePropList at line 3793)
hop 4  entities.c:xmlFreeEntity  (/src/libxml2/entities.c:119-146, calls xmlFreeNodeList at line 131)
hop 4  parser.c:xmlParseBalancedChunkMemoryInternal  (/src/libxml2/parser.c:13123-13298, calls xmlFreeNode at line 13269)
hop 4  xmlParseInNodeContext  (/src/libxml2/parser.c:13321-13526, calls xmlFreeNode at line 13510)
hop 4  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls xmlFreeNodeList at line 7318)
hop 4  xmlAddNextSibling  (/src/libxml2/tree.c:3090-3149, calls tree.c:xmlAddPropSibling at line 3134)
hop 4  xmlAddPrevSibling  (/src/libxml2/tree.c:3170-3230, calls tree.c:xmlAddPropSibling at line 3214)
hop 5  htmlSetMetaEncoding  (/src/libxml2/HTMLtree.c:162-295, calls xmlAddPrevSibling at line 277)
hop 5  entities.c:xmlAddEntity  (/src/libxml2/entities.c:203-285, calls entities.c:xmlFreeEntity at line 281)
hop 5  entities.c:xmlFreeEntityWrapper  (/src/libxml2/entities.c:933-936, calls entities.c:xmlFreeEntity at line 935)
hop 5  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseReference at line 10020)
hop 5  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseReference at line 11768)
hop 5  relaxng.c:xmlRelaxNGCleanupTree  (/src/libxml2/relaxng.c:7043-7472, calls xmlAddNextSibling at line 7389)
hop 5  xmlStringLenGetNodeList  (/src/libxml2/tree.c:1269-1487, calls xmlAddNextSibling at line 1402)
hop 6  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199, calls xmlStringLenGetNodeList at line 2068)
hop 6  xmlAddDocEntity  (/src/libxml2/entities.c:388-419, calls entities.c:xmlAddEntity at line 403)
hop 6  xmlAddDtdEntity  (/src/libxml2/entities.c:339-370, calls entities.c:xmlAddEntity at line 354)
hop 6  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 6  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 6  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 6  relaxng.c:xmlRelaxNGCleanupDoc  (/src/libxml2/relaxng.c:7486-7500, calls relaxng.c:xmlRelaxNGCleanupTree at line 7498)
hop 6  xmlNodeSetContentLen  (/src/libxml2/tree.c:5839-5894, calls xmlStringLenGetNodeList at line 5852)
hop 6  xmlsave.c:htmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:750-799, calls htmlSetMetaEncoding at line 771)
hop 6  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225, calls htmlSetMetaEncoding at line 1109)
hop 7  xmlSAX2EntityDecl  (/src/libxml2/SAX2.c:630-683, calls xmlAddDtdEntity at line 660)
hop 7  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459, calls SAX2.c:xmlSAX2AttributeNs at line 2421)
hop 7  xmlSAX2UnparsedEntityDecl  (/src/libxml2/SAX2.c:876-930, calls xmlAddDtdEntity at line 906)
hop 7  xmlNewEntity  (/src/libxml2/entities.c:441-457, calls xmlAddDocEntity at line 446)
hop 7  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 7  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 7  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 7  relaxng.c:xmlRelaxNGLoadExternalRef  (/src/libxml2/relaxng.c:1953-2027, calls relaxng.c:xmlRelaxNGCleanupDoc at line 2018)
hop 7  relaxng.c:xmlRelaxNGLoadInclude  (/src/libxml2/relaxng.c:1605-1765, calls relaxng.c:xmlRelaxNGCleanupDoc at line 1681)
hop 7  xmlSaveTree  (/src/libxml2/xmlsave.c:1860-1879, calls xmlsave.c:htmlNodeDumpOutputInternal at line 1873)
hop 7  xmlsave.c:xhtmlNodeDumpOutput  (/src/libxml2/xmlsave.c:1392-1700, calls xmlsave.c:xmlDocContentDumpOutput at line 1405)
hop 7  xmlsave.c:xmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:809-1068, calls xmlsave.c:xmlDocContentDumpOutput at line 825)
hop 8  xmlParseEntityDecl  (/src/libxml2/parser.c:5476-5721, calls xmlSAX2EntityDecl at line 5598)
hop 8  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 8  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 8  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 8  xmlsave.c:xmlDtdDumpOutput  (/src/libxml2/xmlsave.c:666-712, calls xmlsave.c:xmlNodeDumpOutputInternal at line 707)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      25         0  xmlValidateNCName  (/src/libxml2/tree.c:372-431)
      25         0  tree.c:xmlGetLineNoInternal  (/src/libxml2/tree.c:4744-4780)
      25         0  xmlGetLineNo  (/src/libxml2/tree.c:4794-4796)
      24         0  xmlNewDocPI  (/src/libxml2/tree.c:2194-2228)
      22         0  tree.c:xmlTreeEnsureXMLDecl  (/src/libxml2/tree.c:6095-6115)
      22         3  xmlFreeNs  (/src/libxml2/tree.c:826-837)
      22         3  xmlFreeNsList  (/src/libxml2/tree.c:846-860)
       0        16  xmlGetLastChild  (/src/libxml2/tree.c:3542-3551)
      15         3  xmlAddSibling  (/src/libxml2/tree.c:3248-3311)
       0         6  xmlNodeIsText  (/src/libxml2/tree.c:7065-7070)
       0         5  xmlStringLenGetNodeList  (/src/libxml2/tree.c:1269-1487)
       0         5  xmlStringGetNodeList  (/src/libxml2/tree.c:1499-1693)
       0         4  xmlSplitQName3  (/src/libxml2/tree.c:327-350)
       0         4  xmlNewDtd  (/src/libxml2/tree.c:876-913)
       0         3  xmlNewNs  (/src/libxml2/tree.c:733-796)
... (1 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  xmlStringLenGetNodeList  (/src/libxml2/tree.c:1269-1487) ---
  d=5   L1278  T=0 F=0  T=0 F=5  if (value == NULL) return(NULL);
  d=5   L1283  T=0 F=0  T=0 F=5  if (buf == NULL) return(NULL);
  d=5   L1287  T=0 F=0  T=104 F=5  while ((cur < end) && (*cur != 0)) {
  d=5   L1287  T=0 F=0  T=104 F=0  while ((cur < end) && (*cur != 0)) {
  d=5   L1288  T=0 F=0  T=0 F=104  if (cur[0] == '&') {
  d=5   L1462  T=0 F=0  T=5 F=0  if (cur != q) {
  d=5   L1466  T=0 F=0  T=0 F=5  if (xmlBufAdd(buf, q, cur - q))
  d=5   L1470  T=0 F=0  T=5 F=0  if (!xmlBufIsEmpty(buf)) {
  d=5   L1472  T=0 F=0  T=0 F=5  if (node == NULL) goto out;
  d=5   L1475  T=0 F=0  T=5 F=0  if (last == NULL) {
--- d=3  xmlFreeNodeList  (/src/libxml2/tree.c:3757-3830) ---
  d=3   L3771  T=16 F=0  T=35 F=0  (cur->type != XML_DOCUMENT_NODE) &&
  d=3   L3772  T=16 F=0  T=35 F=0  (cur->type != XML_HTML_DOCUMENT_NODE) &&
  d=3   L3773  T=16 F=0  T=35 F=0  (cur->type != XML_DTD_NODE) &&
  d=3   L3774  T=16 F=0  T=35 F=0  (cur->type != XML_ENTITY_REF_NODE)) {
  d=3   L3798  T=64 F=0  T=49 F=12  (cur->content != (xmlChar *) &(cur->properties))) {
  d=3   L3804  T=0 F=37  T=2 F=55  (cur->nsDef != NULL))
  d=3   L3823  T=0 F=16  T=0 F=35  if ((depth == 0) || (parent == NULL))
--- d=1  xmlFreeProp  (/src/libxml2/tree.c:2115-2131) ---
  d=1   L2125  T=20 F=0  T=0 F=19  if ((cur->doc != NULL) && (cur->atype == XML_ATTRIBUTE_ID...  <-- BLOCKER

[off-chain: 169 additional divergent branches across 24 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c20581314eb72916, size=307 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=36030s, mutation_op=ByteRandMutator,QwordAddMutator,BytesSwapMutator,WordInterestingMutator,BytesRandInsertMutator,ByteNegMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   72.xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 26 37 37 32 2e 64 3a    ".:d./12&772.d:
Seed 2 (id=6325b1fe38e4d1ee, size=348 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=36414s, mutation_op=BytesRandInsertMutator,ByteRandMutator,ByteAddMutator,TokenReplace,DwordAddMutator):
  0000: 37 80 00 01 00 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   7....l\.<?x.l:ve
  0010: 72 73 64 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsdon="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 80 32 26 37 37 32 2e 64 3a    ".:d./.2&772.d:
Seed 3 (id=31a0f4cf800d3991, size=133 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=53377s, mutation_op=BitFlipMutator,WordAddMutator,BytesExpandMutator,ByteRandMutator):
  0000: 73 69 7d 74 74 74 74 74 74 74 74 74 74 09 78 6d   si}tttttttttt.xm
  0010: 6c 3a 69 64 3d 22 20 3a 69 64 3d 22 26 26 73 69   l:id=" :id="&&si
  0020: 6d 70 6c 9b 29 20 e0 23 00 00 26 00 6b 3a 74 5c   mpl.) .#..&.k:t\
  0030: 0a 3c 74 f6 74 74 74 74 74 74 74 74 09 78 6d 6c   .<t.tttttttt.xml
Seed 4 (id=168e9a373a411e74, size=333 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=53552s, mutation_op=ByteRandMutator,BytesCopyMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   72.xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 5d 37 37 32 2e 64 3a    ".:d./12]772.d:
Seed 5 (id=c0f4fb619d9e55cd, size=345 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=53552s, mutation_op=WordAddMutator,ByteFlipMutator,WordInterestingMutator,WordInterestingMutator,ByteFlipMutator,BytesRandInsertMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   72.xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 5d 37 37 32 2e 64 3a    ".:d./12]772.d:

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=075f3886887037b7, size=369 bytes, fuzzer=value_profile, trial=1, discovered_at=1088s, mutation_op=DwordAddMutator,TokenInsert,ByteAddMutator,BitFlipMutator):
  0000: 77 77 2e 77 fe ff ff ff 33 2e 6f 72 67 2f 31 2f   ww.w....3.org/1/
  0010: 2f 2f 2f 2f 2f 2f 2f 2f 2f 2f 20 20 20 20 20 20   //////////      
  0020: 20 20 20 20 20 20 78 6c 69 6e 6b 3a 74 79 70 65         xlink:type
  0030: 20 20 20 28 73 69 6d 70 6c 65 29 20 20 23 46 49      (simple)  #FI
Seed 2 (id=0dbb09534c8db0ab, size=438 bytes, fuzzer=value_profile, trial=1, discovered_at=1116s, mutation_op=ByteDecMutator,ByteFlipMutator,ByteFlipMutator,CrossoverInsertMutator):
  0000: 31 32 37 37 37 32 2e 64 aa aa aa aa aa aa aa aa   127772.d........
  0010: 2f 31 32 37 37 37 32 2e 64 74 64 22 3e 0a 0a 3b   /127772.dtd">..;
  0020: 61 3e 0a 20 64 73 2f cf 32 64 00 00 00 2e 64 74   a>. ds/.2d....dt
  0030: 64 5c 0a 3c 6e 6b 3a 74 79 70 65 76 65 72 73 69   d\.<nk:typeversi
Seed 3 (id=0f4a31ffd5b4c31f, size=172 bytes, fuzzer=value_profile, trial=1, discovered_at=1124s, mutation_op=QwordAddMutator,ByteAddMutator,ByteIncMutator,ByteNegMutator):
  0000: 45 4c 45 4d 45 0a 3c 1f 78 4e 54 20 22 3f 3e 0a   ELEME.<.xNT "?>.
  0010: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0020: 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e   EM "dtds/127772.
  0030: 64 74 64 22 3e 0b ff ff ff ff 0a 20 20 3c 62 20   dtd">......  <b 
Seed 4 (id=0418896bc4e3a59f, size=508 bytes, fuzzer=value_profile, trial=1, discovered_at=1755s, mutation_op=BytesExpandMutator,BytesInsertMutator,ByteDecMutator):
  0000: 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43   on="1.0"?>.<!DOC
  0010: 54 59 50 45 e0 6d 6d 20 20 77 20 43 44 41 54 41   TYPE.mm  w CDATA
  0020: 20 20 20 20 20 23 49 4d 50 4c 49 45 44 3e 0a 0a        #IMPLIED>..
  0030: 5c 0a 3c 61 3e 0a 20 20 3c 62 20 78 6c 69 6e 6b   \.<a>.  <b xlink
Seed 5 (id=08aa863e68a012de, size=116 bytes, fuzzer=value_profile, trial=1, discovered_at=2742s, mutation_op=QwordAddMutator,BytesCopyMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c c3 78 6d 6c 20 76   772.xml\.<.xml v
  0010: 65 72 73 69 6f fa fa fa fa fa fa fa fa fa fa fa   ersio...........
  0020: fa fa fa 6e 6c 20 76 65 72 73 69 6f fa fa fa fa   ...nl versio....
  0030: fa fa fa fa fa fa fa fa fa fa 6e 3d 22 41 3e 0a   ..........n="A>.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  37(7)x6 7f(.)x2 73(s)x1             45(E)x3 6f(o)x2 37(7)x2 77(w)x1 +2u  PARTIAL
   0x0001  32(2)x5 00(.)x2 80(.)x1 69(i)x1     6e(n)x3 37(7)x2 44(D)x2 77(w)x1 +2u  PARTIAL
   0x0002  2e(.)x7 00(.)x1 7d(})x1             37(7)x2 3d(=)x2 20( )x2 2e(.)x1 +3u  PARTIAL
   0x0003  78(x)x7 01(.)x1 74(t)x1             22(")x2 27(')x2 77(w)x1 37(7)x1 +4u  DIFFER
   0x0004  6d(m)x7 00(.)x1 74(t)x1             31(1)x2 68(h)x2 fe(.)x1 37(7)x1 +4u  DIFFER
   0x0005  6c(l)x8 74(t)x1                     2e(.)x2 74(t)x2 ff(.)x1 32(2)x1 +4u  PARTIAL
   0x0006  5c(\)x8 74(t)x1                     30(0)x2 74(t)x2 ff(.)x1 2e(.)x1 +4u  PARTIAL
   0x0007  0a(.)x8 74(t)x1                     22(")x2 70(p)x2 ff(.)x1 64(d)x1 +4u  DIFFER
   0x0008  3c(<)x8 74(t)x1                     3f(?)x2 3a(:)x2 33(3)x1 aa(.)x1 +4u  DIFFER
   0x0009  3f(?)x8 74(t)x1                     2f(/)x3 3e(>)x2 2e(.)x1 aa(.)x1 +3u  DIFFER
   0x000a  78(x)x8 74(t)x1                     2f(/)x3 0a(.)x2 6f(o)x1 aa(.)x1 +3u  DIFFER
   0x000b  0a(.)x6 6d(m)x2 74(t)x1             3c(<)x2 77(w)x2 72(r)x1 aa(.)x1 +4u  DIFFER
   0x000c  6c(l)x8 74(t)x1                     21(!)x2 77(w)x2 67(g)x1 aa(.)x1 +4u  DIFFER
   0x000d  3a(:)x8 09(.)x1                     2f(/)x2 44(D)x2 77(w)x2 aa(.)x1 +3u  DIFFER
   0x000e  76(v)x8 78(x)x1                     4f(O)x2 2e(.)x2 31(1)x1 aa(.)x1 +4u  DIFFER
   0x000f  65(e)x8 6d(m)x1                     2f(/)x2 43(C)x2 77(w)x2 aa(.)x1 +3u  DIFFER
   0x0010  72(r)x8 6c(l)x1                     2f(/)x2 54(T)x2 3d(=)x2 3c(<)x1 +3u  DIFFER
   0x0011  73(s)x8 3a(:)x1                     59(Y)x2 2e(.)x2 2f(/)x1 31(1)x1 +4u  DIFFER
   0x0012  69(i)x7 64(d)x1 56(V)x1             50(P)x2 6f(o)x2 2f(/)x1 32(2)x1 +4u  DIFFER
   0x0013  6f(o)x8 64(d)x1                     45(E)x2 72(r)x2 2f(/)x1 37(7)x1 +4u  DIFFER
   0x0014  6e(n)x8 3d(=)x1                     e0(.)x2 67(g)x2 2f(/)x1 37(7)x1 +4u  DIFFER
   0x0015  3d(=)x8 22(")x1                     2f(/)x3 6d(m)x2 37(7)x1 54(T)x1 +3u  DIFFER
   0x0016  22(")x8 20( )x1                     6d(m)x2 31(1)x2 2f(/)x1 32(2)x1 +4u  DIFFER
   0x0017  31(1)x8 3a(:)x1                     20( )x2 39(9)x2 2f(/)x1 2e(.)x1 +4u  DIFFER
   0x0018  2e(.)x8 69(i)x1                     20( )x2 39(9)x2 2f(/)x1 64(d)x1 +4u  DIFFER
   0x0019  30(0)x8 64(d)x1                     77(w)x2 39(9)x2 2f(/)x1 74(t)x1 +4u  DIFFER
   0x001a  3c(<)x6 22(")x2 3d(=)x1             20( )x3 2f(/)x2 64(d)x1 61(a)x1 +3u  DIFFER
   0x001b  3f(?)x8 22(")x1                     20( )x2 43(C)x2 78(x)x2 22(")x1 +3u  PARTIAL
   0x001c  3e(>)x8 26(&)x1                     20( )x2 44(D)x2 6c(l)x2 3e(>)x1 +3u  PARTIAL
   0x001d  0a(.)x8 26(&)x1                     20( )x2 41(A)x2 69(i)x2 0a(.)x1 +3u  PARTIAL
   0x001e  3c(<)x8 73(s)x1                     54(T)x2 6e(n)x2 20( )x1 0a(.)x1 +4u  PARTIAL
   0x001f  21(!)x8 69(i)x1                     41(A)x2 6b(k)x2 20( )x1 3b(;)x1 +4u  DIFFER
   0x0020  44(D)x8 6d(m)x1                     20( )x4 72(r)x2 61(a)x1 45(E)x1 +2u  DIFFER
   0x0021  4f(O)x8 70(p)x1                     20( )x3 67(g)x2 3e(>)x1 4d(M)x1 +3u  DIFFER
   0x0022  43(C)x8 6c(l)x1                     20( )x4 2f(/)x2 0a(.)x1 fa(.)x1 +2u  PARTIAL
   0x0023  54(T)x8 9b(.)x1                     20( )x3 31(1)x2 22(")x1 6e(n)x1 +3u  DIFFER
   0x0024  59(Y)x8 29())x1                     20( )x3 64(d)x2 39(9)x2 6c(l)x1 +2u  DIFFER
   0x0025  50(P)x8 20( )x1                     20( )x2 23(#)x2 39(9)x2 73(s)x1 +3u  PARTIAL
   0x0026  45(E)x8 e0(.)x1                     39(9)x3 49(I)x2 78(x)x1 2f(/)x1 +3u  DIFFER
   0x0027  3a(:)x8 23(#)x1                     4d(M)x2 2f(/)x2 6c(l)x1 cf(.)x1 +4u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6936.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6936,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6936 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6936 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6936 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).