==== BLOCKER ====
Target: libxml2
Branch ID: 6946
Location: /src/libxml2/tree.c:6141:2
Enclosing function: xmlSearchNs
Source line: 	(xmlStrEqual(nameSpace, (const xmlChar *)"xml"))) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    5        5          0  REFERENCE
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
  avg duration blocked: winner=11.90h  loser=23.10h
  avg hitcount on branch: winner=13  loser=0
  prob_div=0.70  dur_div=11.20h  hit_div=12
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6946/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlSearchNs (/src/libxml2/tree.c:6134-6207) ---
[ ]  6132   */
[ ]  6133  xmlNsPtr
[B]  6134  xmlSearchNs(xmlDocPtr doc, xmlNodePtr node, const xmlChar *nameSpace) {
[ ]  6135  
[B]  6136      xmlNsPtr cur;
[B]  6137      const xmlNode *orig = node;
[ ]  6138  
[B]  6139      if ((node == NULL) || (node->type == XML_NAMESPACE_DECL)) return(NULL);
[B]  6140      if ((nameSpace != NULL) &&
[B]  6141  	(xmlStrEqual(nameSpace, (const xmlChar *)"xml"))) { <-- BLOCKER
[W]  6142  	if ((doc == NULL) && (node->type == XML_ELEMENT_NODE)) {
[ ]  6143  	    /*
[ ]  6144  	     * The XML-1.0 namespace is normally held on the root
[ ]  6145  	     * element. In this case exceptionally create it on the
[ ]  6146  	     * node element.
[ ]  6147  	     */
[ ]  6148  	    cur = (xmlNsPtr) xmlMalloc(sizeof(xmlNs));
[ ]  6149  	    if (cur == NULL) {
[ ]  6150  		xmlTreeErrMemory("searching namespace");
[ ]  6151  		return(NULL);
[ ]  6152  	    }
[ ]  6153  	    memset(cur, 0, sizeof(xmlNs));
[ ]  6154  	    cur->type = XML_LOCAL_NAMESPACE;
[ ]  6155  	    cur->href = xmlStrdup(XML_XML_NAMESPACE);
[ ]  6156  	    cur->prefix = xmlStrdup((const xmlChar *)"xml");
[ ]  6157  	    cur->next = node->nsDef;
[ ]  6158  	    node->nsDef = cur;
[ ]  6159  	    return(cur);
[ ]  6160  	}
[W]  6161  	if (doc == NULL) {
[ ]  6162  	    doc = node->doc;
[ ]  6163  	    if (doc == NULL)
[ ]  6164  		return(NULL);
[ ]  6165  	}
[ ]  6166  	/*
[ ]  6167  	* Return the XML namespace declaration held by the doc.
[ ]  6168  	*/
[W]  6169  	if (doc->oldNs == NULL)
[W]  6170  	    return(xmlTreeEnsureXMLDecl(doc));
[ ]  6171  	else
[ ]  6172  	    return(doc->oldNs);
[W]  6173      }
[B]  6174      while (node != NULL) {
[B]  6175  	if ((node->type == XML_ENTITY_REF_NODE) ||
[B]  6176  	    (node->type == XML_ENTITY_NODE) ||
[B]  6177  	    (node->type == XML_ENTITY_DECL))
[ ]  6178  	    return(NULL);
[B]  6179  	if (node->type == XML_ELEMENT_NODE) {
[B]  6180  	    cur = node->nsDef;
[B]  6181  	    while (cur != NULL) {
[L]  6182  		if ((cur->prefix == NULL) && (nameSpace == NULL) &&
[L]  6183  		    (cur->href != NULL))
[ ]  6184  		    return(cur);
[L]  6185  		if ((cur->prefix != NULL) && (nameSpace != NULL) &&
[L]  6186  		    (cur->href != NULL) &&
[L]  6187  		    (xmlStrEqual(cur->prefix, nameSpace)))
[ ]  6188  		    return(cur);
[L]  6189  		cur = cur->next;
[L]  6190  	    }
[B]  6191  	    if (orig != node) {
[B]  6192  	        cur = node->ns;
[B]  6193  	        if (cur != NULL) {
[ ]  6194  		    if ((cur->prefix == NULL) && (nameSpace == NULL) &&
[ ]  6195  		        (cur->href != NULL))
[ ]  6196  		        return(cur);
[ ]  6197  		    if ((cur->prefix != NULL) && (nameSpace != NULL) &&
[ ]  6198  		        (cur->href != NULL) &&
[ ]  6199  		        (xmlStrEqual(cur->prefix, nameSpace)))
[ ]  6200  		        return(cur);
[ ]  6201  	        }
[B]  6202  	    }
[B]  6203  	}
[B]  6204  	node = node->parent;
[B]  6205      }
[B]  6206      return(NULL);
[B]  6207  }

--- Caller (1 hop): xmlSAX2StartElement (/src/libxml2/SAX2.c:1603-1806, calls xmlSearchNs at line 1737) (±10 around call site) ---
[ ]  1727  
[B]  1728  		att = atts[i++];
[B]  1729  		value = atts[i++];
[B]  1730  	    }
[B]  1731          }
[ ]  1732  
[ ]  1733          /*
[ ]  1734           * Search the namespace, note that since the attributes have been
[ ]  1735           * processed, the local namespaces are available.
[ ]  1736           */
[B]  1737          ns = xmlSearchNs(ctxt->myDoc, ret, prefix); <-- CALL
[B]  1738          if ((ns == NULL) && (parent != NULL))
[B]  1739              ns = xmlSearchNs(ctxt->myDoc, parent, prefix);
[B]  1740          if ((prefix != NULL) && (ns == NULL)) {
[L]  1741              ns = xmlNewNs(ret, NULL, prefix);
[L]  1742              xmlNsWarnMsg(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[L]  1743                           "Namespace prefix %s is not defined\n",
[L]  1744                           prefix, NULL);
[L]  1745          }
[ ]  1746  
[ ]  1747          /*

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  relaxng.c:xmlRelaxNGCleanupTree  (/src/libxml2/relaxng.c:7043-7472, calls xmlSearchNs at line 7299)
hop 2  xmlTextReaderGetAttribute  (/src/libxml2/xmlreader.c:2317-2374, calls xmlSearchNs at line 2365)
hop 3  relaxng.c:xmlRelaxNGCleanupDoc  (/src/libxml2/relaxng.c:7486-7500, calls relaxng.c:xmlRelaxNGCleanupTree at line 7498)
hop 4  relaxng.c:xmlRelaxNGLoadExternalRef  (/src/libxml2/relaxng.c:1953-2027, calls relaxng.c:xmlRelaxNGCleanupDoc at line 2018)
hop 4  relaxng.c:xmlRelaxNGLoadInclude  (/src/libxml2/relaxng.c:1605-1765, calls relaxng.c:xmlRelaxNGCleanupDoc at line 1681)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      60       252  xmlSearchNs  (/src/libxml2/tree.c:6134-6207)  <-- enclosing
     106         0  xmlSplitQName2  (/src/libxml2/tree.c:267-312)
      21       115  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806)
      42       134  xmlAddChild  (/src/libxml2/tree.c:3418-3532)
      33       115  xmlNewNodeEatName  (/src/libxml2/tree.c:2303-2332)
      33       115  xmlNewDocNodeEatName  (/src/libxml2/tree.c:2389-2407)
      21        88  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591)
      33         0  xmlSplitQName3  (/src/libxml2/tree.c:327-350)
      27         0  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758)
       0        27  xmlGetLastChild  (/src/libxml2/tree.c:3542-3551)
       3        27  xmlSAX2IgnorableWhitespace  (/src/libxml2/SAX2.c:2698-2704)
       6        28  SAX2.c:xmlNsErrMsg  (/src/libxml2/SAX2.c:1070-1080)
       6        26  xmlAddSibling  (/src/libxml2/tree.c:3248-3311)
      18         0  xmlSAX2ElementDecl  (/src/libxml2/SAX2.c:772-807)
      18         0  SAX2.c:xmlSAX2DecodeAttrEntities  (/src/libxml2/SAX2.c:1958-1973)
... (23 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlSearchNs  (/src/libxml2/tree.c:6134-6207) ---
  d=1   L6139  T=0 F=60  T=0 F=252  if ((node == NULL) || (node->type == XML_NAMESPACE_DECL))...
  d=1   L6139  T=0 F=60  T=0 F=252  if ((node == NULL) || (node->type == XML_NAMESPACE_DECL))...
  d=1   L6140  T=18 F=42  T=53 F=199  if ((nameSpace != NULL) &&
  d=1   L6141  T=12 F=6  T=0 F=53  (xmlStrEqual(nameSpace, (const xmlChar *)"xml"))) {  <-- BLOCKER
  d=1   L6142  T=0 F=12  T=0 F=0  if ((doc == NULL) && (node->type == XML_ELEMENT_NODE)) {
  d=1   L6161  T=0 F=12  T=0 F=0  if (doc == NULL) {
  d=1   L6169  T=12 F=0  T=0 F=0  if (doc->oldNs == NULL)
  d=1   L6174  T=135 F=48  T=751 F=252  while (node != NULL) {
  d=1   L6175  T=0 F=135  T=0 F=751  if ((node->type == XML_ENTITY_REF_NODE) ||
  d=1   L6176  T=0 F=135  T=0 F=751  (node->type == XML_ENTITY_NODE) ||
  d=1   L6177  T=0 F=135  T=0 F=751  (node->type == XML_ENTITY_DECL))
  d=1   L6179  T=81 F=54  T=473 F=278  if (node->type == XML_ELEMENT_NODE) {
  d=1   L6181  T=0 F=81  T=36 F=473  while (cur != NULL) {
  d=1   L6182  T=0 F=0  T=0 F=36  if ((cur->prefix == NULL) && (nameSpace == NULL) &&
  d=1   L6185  T=0 F=0  T=36 F=0  if ((cur->prefix != NULL) && (nameSpace != NULL) &&
  d=1   L6185  T=0 F=0  T=16 F=20  if ((cur->prefix != NULL) && (nameSpace != NULL) &&
  d=1   L6186  T=0 F=0  T=0 F=16  (cur->href != NULL) &&
  d=1   L6191  T=39 F=42  T=247 F=226  if (orig != node) {
  d=1   L6193  T=0 F=39  T=0 F=247  if (cur != NULL) {

[off-chain: 787 additional divergent branches across 73 functions (see HIT-COUNT DIVERGENCE for which functions)]

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
Seed 1 (id=471733a1ed95a29b, size=532 bytes, fuzzer=naive, trial=2, discovered_at=55s, mutation_op=CrossoverInsertMutator,BytesSwapMutator,BytesInsertCopyMutator,BytesInsertMutator,BytesCopyMutator,BytesRandSetMutator):
  0000: 69 6e 6b 27 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   ink'ml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 b7 32 2e 64 74    "dtds/1277.2.dt
Seed 2 (id=5845b62332235ff2, size=257 bytes, fuzzer=naive, trial=2, discovered_at=69s, mutation_op=BytesExpandMutator,ByteFlipMutator,BytesExpandMutator):
  0000: cf cf cf cf cf cf cf cf cf cf 2e 78 6d 6c 5c 0a   ...........xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 8b 64 73 2f 31   a SYSTEM "d.ds/1
Seed 3 (id=00a7446f358fd109, size=248 bytes, fuzzer=naive, trial=2, discovered_at=508s, mutation_op=BytesRandInsertMutator,BytesInsertCopyMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 e7 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   er.sion="1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37 37 32   EM "dtds/1277772
Seed 4 (id=244e66c16f769fa4, size=508 bytes, fuzzer=naive, trial=2, discovered_at=581s, mutation_op=CrossoverInsertMutator,BytesSwapMutator,BytesDeleteMutator,WordAddMutator):
  0000: 17 17 17 17 17 17 17 17 17 54 41 29 3e 37 37 37   .........TA)>777
  0010: 32 01 e0 ff ff 06 00 00 00 31 32 2b 44 41 54 41   2........12+DATA
  0020: 29 3e 37 37 00 00 00 31 32 37 37 37 32 2e 78 6d   )>77...127772.xm
  0030: 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e   l\.<?xml version
Seed 5 (id=349b58bc3124bdf2, size=710 bytes, fuzzer=naive, trial=2, discovered_at=1747s, mutation_op=BytesInsertCopyMutator,ByteRandMutator,ByteFlipMutator,BytesCopyMutator,CrossoverInsertMutator,TokenInsert,TokenInsert):
  0000: 3d 22 68 74 74 70 6e 6b 3a 68 72 65 66 3d 22 68   ="httpnk:href="h
  0010: 74 74 70 3a 2f 2f 66 61 6b 65 75 72 65 64 65 65   ttp://fakeuredee
  0020: 74 22 3e 62 20 74 28 62 2a 29 3e 0a 0a 3c 21 62   t">b t(b*)>..<!b
  0030: 3e 0a 3c 2f 92 92 92 92 92 92 92 92 61 3e 0a 20   >.</........a>. 


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f9(.)x2 ff(.)x1 33(3)x1             3d(=)x3 69(i)x1 cf(.)x1 37(7)x1 +4u  DIFFER
   0x0001  00(.)x2 7f(.)x1 2e(.)x1             22(")x3 6e(n)x1 cf(.)x1 37(7)x1 +4u  DIFFER
   0x0002  ff(.)x1 00(.)x1 6f(o)x1 37(7)x1     68(h)x3 6b(k)x1 cf(.)x1 32(2)x1 +4u  PARTIAL
   0x0003  ff(.)x1 00(.)x1 72(r)x1 37(7)x1     74(t)x3 27(')x1 cf(.)x1 2e(.)x1 +4u  PARTIAL
   0x0004  31(1)x2 67(g)x1 37(7)x1             74(t)x2 73(s)x2 6d(m)x1 cf(.)x1 +4u  DIFFER
   0x0005  32(2)x3 00(.)x1                     70(p)x3 6c(l)x1 cf(.)x1 6d(m)x1 +4u  DIFFER
   0x0006  c8(.)x1 37(7)x1 02(.)x1 2e(.)x1     3a(:)x2 5c(\)x1 cf(.)x1 6c(l)x1 +5u  DIFFER
   0x0007  37(7)x2 39(9)x1 78(x)x1             2f(/)x2 0a(.)x1 cf(.)x1 5c(\)x1 +5u  DIFFER
   0x0008  37(7)x2 39(9)x1 6d(m)x1             2f(/)x2 3c(<)x1 cf(.)x1 0a(.)x1 +5u  DIFFER
   0x0009  32(2)x2 39(9)x1 6c(l)x1             66(f)x2 3f(?)x1 cf(.)x1 3c(<)x1 +5u  PARTIAL
   0x000a  2e(.)x2 2f(/)x1 5c(\)x1             78(x)x1 2e(.)x1 3f(?)x1 41(A)x1 +6u  PARTIAL
   0x000b  78(x)x3 0a(.)x1                     78(x)x2 6d(m)x1 29())x1 65(e)x1 +5u  PARTIAL
   0x000c  6d(m)x2 3a(:)x1 3c(<)x1             6d(m)x2 6c(l)x1 3e(>)x1 66(f)x1 +5u  PARTIAL
   0x000d  6c(l)x2 69(i)x1 3f(?)x1             6c(l)x2 20( )x1 37(7)x1 3d(=)x1 +5u  PARTIAL
   0x000e  5c(\)x2 6e(n)x1 78(x)x1             76(v)x1 5c(\)x1 20( )x1 37(7)x1 +6u  PARTIAL
   0x000f  0a(.)x2 6b(k)x1 6d(m)x1             65(e)x1 0a(.)x1 76(v)x1 37(7)x1 +6u  PARTIAL
   0x0010  3c(<)x2 27(')x1 6c(l)x1             65(e)x2 2e(.)x2 72(r)x1 3c(<)x1 +4u  PARTIAL
   0x0011  3f(?)x2 0a(.)x1 20( )x1             73(s)x1 3f(?)x1 72(r)x1 01(.)x1 +6u  PARTIAL
   0x0012  78(x)x2 20( )x1 76(v)x1             69(i)x1 78(x)x1 e7(.)x1 e0(.)x1 +6u  PARTIAL
   0x0013  6d(m)x2 20( )x1 65(e)x1             0a(.)x2 6f(o)x1 6d(m)x1 73(s)x1 +5u  PARTIAL
   0x0014  6c(l)x2 20( )x1 72(r)x1             ff(.)x2 6e(n)x1 6c(l)x1 69(i)x1 +5u  PARTIAL
   0x0015  20( )x3 73(s)x1                     3d(=)x1 20( )x1 6f(o)x1 06(.)x1 +6u  PARTIAL
   0x0016  76(v)x2 20( )x1 69(i)x1             22(")x1 76(v)x1 6e(n)x1 00(.)x1 +6u  PARTIAL
   0x0017  65(e)x2 20( )x1 6f(o)x1             62(b)x2 31(1)x1 65(e)x1 3d(=)x1 +5u  PARTIAL
   0x0018  72(r)x2 20( )x1 6e(n)x1             20( )x2 2e(.)x1 72(r)x1 22(")x1 +5u  PARTIAL
   0x0019  73(s)x2 20( )x1 3d(=)x1             31(1)x2 65(e)x2 30(0)x1 73(s)x1 +4u  PARTIAL
   0x001a  69(i)x2 78(x)x1 22(")x1             22(")x1 69(i)x1 2e(.)x1 32(2)x1 +6u  PARTIAL
   0x001b  6f(o)x2 6d(m)x1 31(1)x1             3f(?)x1 6f(o)x1 30(0)x1 2b(+)x1 +6u  PARTIAL
   0x001c  6e(n)x2 6c(l)x1 2e(.)x1             3e(>)x1 6e(n)x1 22(")x1 44(D)x1 +6u  PARTIAL
   0x001d  3d(=)x2 6e(n)x1 30(0)x1             0a(.)x1 3d(=)x1 3f(?)x1 41(A)x1 +6u  PARTIAL
   0x001e  22(")x3 73(s)x1                     3c(<)x1 22(")x1 3e(>)x1 54(T)x1 +6u  PARTIAL
   0x001f  31(1)x2 28(()x1 3f(?)x1             0a(.)x2 21(!)x1 31(1)x1 41(A)x1 +5u  PARTIAL
   0x0020  2e(.)x2 78(x)x1 3e(>)x1             3c(<)x2 44(D)x1 2e(.)x1 29())x1 +5u  PARTIAL
   0x0021  30(0)x2 6c(l)x1 0a(.)x1             3e(>)x2 3c(<)x2 4f(O)x1 30(0)x1 +4u  PARTIAL
   0x0022  22(")x2 69(i)x1 3c(<)x1             43(C)x1 22(")x1 44(D)x1 37(7)x1 +6u  PARTIAL
   0x0023  3f(?)x2 6e(n)x1 21(!)x1             54(T)x1 3f(?)x1 4f(O)x1 37(7)x1 +6u  PARTIAL
   0x0024  3e(>)x2 6b(k)x1 44(D)x1             59(Y)x1 3e(>)x1 43(C)x1 00(.)x1 +6u  PARTIAL
   0x0025  0a(.)x2 20( )x1 4f(O)x1             0a(.)x2 20( )x2 50(P)x1 54(T)x1 +4u  PARTIAL
   0x0026  3c(<)x2 20( )x1 43(C)x1             3c(<)x2 45(E)x1 59(Y)x1 00(.)x1 +5u  PARTIAL
   0x0027  21(!)x2 43(C)x1 54(T)x1             20( )x2 65(e)x2 21(!)x1 50(P)x1 +4u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6946.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6946,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6946 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6946 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6946 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).