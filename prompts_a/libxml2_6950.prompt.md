==== BLOCKER ====
Target: libxml2
Branch ID: 6950
Location: /src/libxml2/tree.c:6185:7
Enclosing function: xmlSearchNs
Source line: 		if ((cur->prefix != NULL) && (nameSpace != NULL) &&
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                        3        7          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         9        1          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.40h  loser=19.50h
  avg hitcount on branch: winner=30  loser=1
  prob_div=0.70  dur_div=8.10h  hit_div=29
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6950/{W,L}/branch_coverage_show.txt

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
[B]  6141  	(xmlStrEqual(nameSpace, (const xmlChar *)"xml"))) {
[ ]  6142  	if ((doc == NULL) && (node->type == XML_ELEMENT_NODE)) {
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
[ ]  6161  	if (doc == NULL) {
[ ]  6162  	    doc = node->doc;
[ ]  6163  	    if (doc == NULL)
[ ]  6164  		return(NULL);
[ ]  6165  	}
[ ]  6166  	/*
[ ]  6167  	* Return the XML namespace declaration held by the doc.
[ ]  6168  	*/
[ ]  6169  	if (doc->oldNs == NULL)
[ ]  6170  	    return(xmlTreeEnsureXMLDecl(doc));
[ ]  6171  	else
[ ]  6172  	    return(doc->oldNs);
[ ]  6173      }
[B]  6174      while (node != NULL) {
[B]  6175  	if ((node->type == XML_ENTITY_REF_NODE) ||
[B]  6176  	    (node->type == XML_ENTITY_NODE) ||
[B]  6177  	    (node->type == XML_ENTITY_DECL))
[ ]  6178  	    return(NULL);
[B]  6179  	if (node->type == XML_ELEMENT_NODE) {
[B]  6180  	    cur = node->nsDef;
[B]  6181  	    while (cur != NULL) {
[B]  6182  		if ((cur->prefix == NULL) && (nameSpace == NULL) &&
[B]  6183  		    (cur->href != NULL))
[W]  6184  		    return(cur);
[B]  6185  		if ((cur->prefix != NULL) && (nameSpace != NULL) && <-- BLOCKER
[B]  6186  		    (cur->href != NULL) &&
[B]  6187  		    (xmlStrEqual(cur->prefix, nameSpace)))
[L]  6188  		    return(cur);
[B]  6189  		cur = cur->next;
[B]  6190  	    }
[B]  6191  	    if (orig != node) {
[B]  6192  	        cur = node->ns;
[B]  6193  	        if (cur != NULL) {
[W]  6194  		    if ((cur->prefix == NULL) && (nameSpace == NULL) &&
[W]  6195  		        (cur->href != NULL))
[ ]  6196  		        return(cur);
[W]  6197  		    if ((cur->prefix != NULL) && (nameSpace != NULL) &&
[W]  6198  		        (cur->href != NULL) &&
[W]  6199  		        (xmlStrEqual(cur->prefix, nameSpace)))
[ ]  6200  		        return(cur);
[W]  6201  	        }
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
      15        79  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      15        79  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
      15        45  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
       6        33  xmlSplitQName3  (/src/libxml2/tree.c:327-350)
       1        18  xmlreader.c:xmlTextReaderCharacters  (/src/libxml2/xmlreader.c:721-731)
      22         6  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591)
       6        21  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758)
       0        12  SAX2.c:xmlNsWarnMsg  (/src/libxml2/SAX2.c:194-204)
       6        18  xmlSAX2ElementDecl  (/src/libxml2/SAX2.c:772-807)
      18         6  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438)
       0        12  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)
       6        18  xmlFreeNodeList  (/src/libxml2/tree.c:3757-3830)
      10         0  xmlSetNs  (/src/libxml2/tree.c:806-817)
       0         9  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199)
       0         8  xmlSAX2EndElementNs  (/src/libxml2/SAX2.c:2476-2502)
... (16 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlSearchNs  (/src/libxml2/tree.c:6134-6207) ---
  d=1   L6139  T=0 F=34  T=0 F=79  if ((node == NULL) || (node->type == XML_NAMESPACE_DECL))...
  d=1   L6139  T=0 F=34  T=0 F=79  if ((node == NULL) || (node->type == XML_NAMESPACE_DECL))...
  d=1   L6140  T=4 F=30  T=34 F=45  if ((nameSpace != NULL) &&
  d=1   L6141  T=0 F=4  T=0 F=34  (xmlStrEqual(nameSpace, (const xmlChar *)"xml"))) {
  d=1   L6174  T=64 F=20  T=198 F=70  while (node != NULL) {
  d=1   L6175  T=0 F=64  T=0 F=198  if ((node->type == XML_ENTITY_REF_NODE) ||
  d=1   L6176  T=0 F=64  T=0 F=198  (node->type == XML_ENTITY_NODE) ||
  d=1   L6177  T=0 F=64  T=0 F=198  (node->type == XML_ENTITY_DECL))
  d=1   L6179  T=38 F=26  T=125 F=73  if (node->type == XML_ELEMENT_NODE) {
  d=1   L6181  T=20 F=24  T=35 F=116  while (cur != NULL) {
  d=1   L6182  T=20 F=0  T=0 F=35  if ((cur->prefix == NULL) && (nameSpace == NULL) &&
  d=1   L6182  T=14 F=6  T=0 F=0  if ((cur->prefix == NULL) && (nameSpace == NULL) &&
  d=1   L6183  T=14 F=0  T=0 F=0  (cur->href != NULL))
  d=1   L6185  T=0 F=6  T=35 F=0  if ((cur->prefix != NULL) && (nameSpace != NULL) &&  <-- BLOCKER
  d=1   L6185  T=0 F=0  T=20 F=15  if ((cur->prefix != NULL) && (nameSpace != NULL) &&  <-- BLOCKER
  d=1   L6186  T=0 F=0  T=12 F=8  (cur->href != NULL) &&
  d=1   L6187  T=0 F=0  T=9 F=3  (xmlStrEqual(cur->prefix, nameSpace)))
  d=1   L6191  T=10 F=14  T=49 F=67  if (orig != node) {
  d=1   L6193  T=2 F=8  T=0 F=49  if (cur != NULL) {
  d=1   L6194  T=2 F=0  T=0 F=0  if ((cur->prefix == NULL) && (nameSpace == NULL) &&
  d=1   L6194  T=0 F=2  T=0 F=0  if ((cur->prefix == NULL) && (nameSpace == NULL) &&
  d=1   L6197  T=0 F=2  T=0 F=0  if ((cur->prefix != NULL) && (nameSpace != NULL) &&

[off-chain: 545 additional divergent branches across 57 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=378eaab990ad2f1b, size=139 bytes, fuzzer=grimoire, trial=1, discovered_at=13781s, mutation_op=GrimoireRandomDeleteMutator,GrimoireExtensionMutator):
  0000: 09 96 98 00 06 00 6d 6c 5c 0a 3c 3f 6c 20 3f 3e   ......ml\.<?l ?>
  0010: 3c 21 44 4f 43 54 59 50 45 61 20 53 59 53 54 45   <!DOCTYPEa SYSTE
  0020: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
  0030: 74 64 22 3e 3c 61 3e 3c 62 3c 62 20 6b 3a 66 3d   td"><a><b<b k:f=
Seed 2 (id=c23096ec9dae2ed4, size=389 bytes, fuzzer=grimoire, trial=1, discovered_at=18912s, mutation_op=ByteNegMutator,BytesExpandMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=3f82a3daf8d36108, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3471s, mutation_op=BytesDeleteMutator,BytesSetMutator):
  0000: fa 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=990e4190ea653e2d, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3590s, mutation_op=CrossoverReplaceMutator,QwordAddMutator,ByteDecMutator):
  0000: f9 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=d511ef109f42d209, size=387 bytes, fuzzer=cmplog, trial=1, discovered_at=36458s, mutation_op=BytesSwapMutator,ByteDecMutator,BytesSetMutator):
  0000: 37 32 28 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 20 65   72(xml\.<?xml  e
  0010: 73 69 6f 6e 5f 22 31 2e 30 22 5c 5c 5c 5c 5c 5c   sion_"1.0"\\\\\\
  0020: 5c 5c 71 71 20 22 64 72 74 64 73 2f 31 32 ff 37   \\qq "drtds/12.7
  0030: 37 32 2e 64 74 64 ff 3e 0a 0a 3c 61 3e 0a 5c 20   72.dtd.>..<a>.\ 
Seed 4 (id=41e1bd5da4584637, size=519 bytes, fuzzer=cmplog, trial=1, discovered_at=45439s, mutation_op=BytesSwapMutator):
  0000: 0f 0f 0f 0f 0f 0f 0f 0f 0f 6e 73 78 78 6c 69 6e   .........nsxxlin
  0010: 6b 20 20 43 44 41 54 41 20 20 20 20 20 23 5c 49   k  CDATA     #\I
  0020: 58 45 44 20 27 68 74 74 26 3a af 2f 77 77 77 2e   XED 'htt&:./www.
  0030: 77 33 2e 6f 72 67 2f 31 39 39 39 77 77 77 2e 77   w3.org/1999www.w
Seed 5 (id=6f437bf6be6c86ba, size=557 bytes, fuzzer=cmplog, trial=1, discovered_at=80851s, mutation_op=DwordInterestingMutator,CrossoverInsertMutator):
  0000: 2f 2f 2b 27 2f 2a 3a 27 2a 66 66 28 2f 2f 2b 27   //+'/*:'*ff(//+'
  0010: 2f 2a 2a 3a 27 2a 66 66 2b 2f 2f 2b 27 2f 2a 2f   /**:'*ff+//+'/*/
  0020: 2f 2f 2b 27 2f 2a 3a 27 2a 66 66 28 2f 2f 2b 27   //+'/*:'*ff(//+'
  0030: 2f 2a 2a 3a 27 2a 66 66 2b 2f 2f 2b 27 2f 2a 2f   /**:'*ff+//+'/*/


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  09(.)x1 37(7)x1                     fa(.)x1 f9(.)x1 37(7)x1 0f(.)x1 +1u  PARTIAL
   0x0001  96(.)x1 32(2)x1                     00(.)x2 32(2)x1 0f(.)x1 2f(/)x1     PARTIAL
   0x0002  98(.)x1 2e(.)x1                     00(.)x2 28(()x1 0f(.)x1 2b(+)x1     DIFFER
   0x0003  00(.)x1 78(x)x1                     00(.)x2 78(x)x1 0f(.)x1 27(')x1     PARTIAL
   0x0004  06(.)x1 6d(m)x1                     31(1)x2 6d(m)x1 0f(.)x1 2f(/)x1     PARTIAL
   0x0005  00(.)x1 6c(l)x1                     32(2)x2 6c(l)x1 0f(.)x1 2a(*)x1     PARTIAL
   0x0006  6d(m)x1 5c(\)x1                     37(7)x2 5c(\)x1 0f(.)x1 3a(:)x1     PARTIAL
   0x0007  6c(l)x1 0a(.)x1                     37(7)x2 0a(.)x1 0f(.)x1 27(')x1     PARTIAL
   0x0008  5c(\)x1 3c(<)x1                     37(7)x2 3c(<)x1 0f(.)x1 2a(*)x1     PARTIAL
   0x0009  0a(.)x1 3f(?)x1                     32(2)x2 3f(?)x1 6e(n)x1 66(f)x1     PARTIAL
   0x000a  3c(<)x1 78(x)x1                     2e(.)x2 78(x)x1 73(s)x1 66(f)x1     PARTIAL
   0x000b  3f(?)x1 6d(m)x1                     78(x)x3 6d(m)x1 28(()x1             PARTIAL
   0x000c  6c(l)x2                             6d(m)x2 6c(l)x1 78(x)x1 2f(/)x1     PARTIAL
   0x000d  20( )x2                             6c(l)x3 20( )x1 2f(/)x1             PARTIAL
   0x000e  3f(?)x1 76(v)x1                     5c(\)x2 20( )x1 69(i)x1 2b(+)x1     DIFFER
   0x000f  3e(>)x1 65(e)x1                     0a(.)x2 65(e)x1 6e(n)x1 27(')x1     PARTIAL
   0x0010  3c(<)x1 72(r)x1                     3c(<)x2 73(s)x1 6b(k)x1 2f(/)x1     PARTIAL
   0x0011  21(!)x1 73(s)x1                     3f(?)x2 69(i)x1 20( )x1 2a(*)x1     DIFFER
   0x0012  44(D)x1 69(i)x1                     78(x)x2 6f(o)x1 20( )x1 2a(*)x1     DIFFER
   0x0013  4f(O)x1 6f(o)x1                     6d(m)x2 6e(n)x1 43(C)x1 3a(:)x1     DIFFER
   0x0014  43(C)x1 6e(n)x1                     6c(l)x2 5f(_)x1 44(D)x1 27(')x1     DIFFER
   0x0015  54(T)x1 3d(=)x1                     20( )x2 22(")x1 41(A)x1 2a(*)x1     DIFFER
   0x0016  59(Y)x1 22(")x1                     76(v)x2 31(1)x1 54(T)x1 66(f)x1     DIFFER
   0x0017  50(P)x1 31(1)x1                     65(e)x2 2e(.)x1 41(A)x1 66(f)x1     DIFFER
   0x0018  45(E)x1 2e(.)x1                     72(r)x2 30(0)x1 20( )x1 2b(+)x1     DIFFER
   0x0019  61(a)x1 30(0)x1                     73(s)x2 22(")x1 20( )x1 2f(/)x1     DIFFER
   0x001a  20( )x1 22(")x1                     69(i)x2 5c(\)x1 20( )x1 2f(/)x1     PARTIAL
   0x001b  53(S)x1 3f(?)x1                     6f(o)x2 5c(\)x1 20( )x1 2b(+)x1     DIFFER
   0x001c  59(Y)x1 3e(>)x1                     6e(n)x2 5c(\)x1 20( )x1 27(')x1     DIFFER
   0x001d  53(S)x1 0a(.)x1                     3d(=)x2 5c(\)x1 23(#)x1 2f(/)x1     DIFFER
   0x001e  54(T)x1 3c(<)x1                     22(")x2 5c(\)x2 2a(*)x1             DIFFER
   0x001f  45(E)x1 21(!)x1                     31(1)x2 5c(\)x1 49(I)x1 2f(/)x1     DIFFER
   0x0020  4d(M)x1 44(D)x1                     2e(.)x2 5c(\)x1 58(X)x1 2f(/)x1     DIFFER
   0x0021  20( )x1 4f(O)x1                     30(0)x2 5c(\)x1 45(E)x1 2f(/)x1     DIFFER
   0x0022  22(")x1 43(C)x1                     22(")x2 71(q)x1 44(D)x1 2b(+)x1     PARTIAL
   0x0023  64(d)x1 54(T)x1                     3f(?)x2 71(q)x1 20( )x1 27(')x1     DIFFER
   0x0024  74(t)x1 59(Y)x1                     3e(>)x2 20( )x1 27(')x1 2f(/)x1     DIFFER
   0x0025  64(d)x1 50(P)x1                     0a(.)x2 22(")x1 68(h)x1 2a(*)x1     DIFFER
   0x0026  73(s)x1 45(E)x1                     3c(<)x2 64(d)x1 74(t)x1 3a(:)x1     DIFFER
   0x0027  2f(/)x1 20( )x1                     21(!)x2 72(r)x1 74(t)x1 27(')x1     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6950.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6950,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6950 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6950 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6950 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).