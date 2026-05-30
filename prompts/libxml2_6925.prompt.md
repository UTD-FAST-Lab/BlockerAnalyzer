==== BLOCKER ====
Target: libxml2
Branch ID: 6925
Location: /src/libxml2/tree.c:766:9
Enclosing function: xmlNewNs
Source line:     if (prefix != NULL)
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
Source: db/per_role_coverage/libxml2/6925/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlNewNs (/src/libxml2/tree.c:733-796) ---
[ ]   731   */
[ ]   732  xmlNsPtr
[B]   733  xmlNewNs(xmlNodePtr node, const xmlChar *href, const xmlChar *prefix) {
[B]   734      xmlNsPtr cur;
[ ]   735  
[B]   736      if ((node != NULL) && (node->type != XML_ELEMENT_NODE))
[ ]   737  	return(NULL);
[ ]   738  
[B]   739      if ((prefix != NULL) && (xmlStrEqual(prefix, BAD_CAST "xml"))) {
[ ]   740          /* xml namespace is predefined, no need to add it */
[ ]   741          if (xmlStrEqual(href, XML_XML_NAMESPACE))
[ ]   742              return(NULL);
[ ]   743  
[ ]   744          /*
[ ]   745           * Problem, this is an attempt to bind xml prefix to a wrong
[ ]   746           * namespace, which breaks
[ ]   747           * Namespace constraint: Reserved Prefixes and Namespace Names
[ ]   748           * from XML namespace. But documents authors may not care in
[ ]   749           * their context so let's proceed.
[ ]   750           */
[ ]   751      }
[ ]   752  
[ ]   753      /*
[ ]   754       * Allocate a new Namespace and fill the fields.
[ ]   755       */
[B]   756      cur = (xmlNsPtr) xmlMalloc(sizeof(xmlNs));
[B]   757      if (cur == NULL) {
[ ]   758  	xmlTreeErrMemory("building namespace");
[ ]   759  	return(NULL);
[ ]   760      }
[B]   761      memset(cur, 0, sizeof(xmlNs));
[B]   762      cur->type = XML_LOCAL_NAMESPACE;
[ ]   763  
[B]   764      if (href != NULL)
[B]   765  	cur->href = xmlStrdup(href);
[B]   766      if (prefix != NULL) <-- BLOCKER
[L]   767  	cur->prefix = xmlStrdup(prefix);
[ ]   768  
[ ]   769      /*
[ ]   770       * Add it at the end to preserve parsing order ...
[ ]   771       * and checks for existing use of the prefix
[ ]   772       */
[B]   773      if (node != NULL) {
[B]   774  	if (node->nsDef == NULL) {
[B]   775  	    node->nsDef = cur;
[B]   776  	} else {
[ ]   777  	    xmlNsPtr prev = node->nsDef;
[ ]   778  
[ ]   779  	    if (((prev->prefix == NULL) && (cur->prefix == NULL)) ||
[ ]   780  		(xmlStrEqual(prev->prefix, cur->prefix))) {
[ ]   781  		xmlFreeNs(cur);
[ ]   782  		return(NULL);
[ ]   783  	    }
[ ]   784  	    while (prev->next != NULL) {
[ ]   785  	        prev = prev->next;
[ ]   786  		if (((prev->prefix == NULL) && (cur->prefix == NULL)) ||
[ ]   787  		    (xmlStrEqual(prev->prefix, cur->prefix))) {
[ ]   788  		    xmlFreeNs(cur);
[ ]   789  		    return(NULL);
[ ]   790  		}
[ ]   791  	    }
[ ]   792  	    prev->next = cur;
[ ]   793  	}
[B]   794      }
[B]   795      return(cur);
[B]   796  }

--- Caller (1 hop): SAX2.c:xmlSAX2AttributeInternal (/src/libxml2/SAX2.c:1097-1438, calls xmlNewNs at line 1214) (±10 around call site) ---
[W]  1204  		if (uri->scheme == NULL) {
[W]  1205  		    if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
[ ]  1206  			ctxt->sax->warning(ctxt->userData,
[ ]  1207  			     "xmlns: URI %s is not absolute\n", val);
[W]  1208  		}
[W]  1209  		xmlFreeURI(uri);
[W]  1210  	    }
[W]  1211  	}
[ ]  1212  
[ ]  1213  	/* a default namespace definition */
[W]  1214  	nsret = xmlNewNs(ctxt->node, val, NULL); <-- CALL
[ ]  1215  
[W]  1216  #ifdef LIBXML_VALID_ENABLED
[ ]  1217  	/*
[ ]  1218  	 * Validate also for namespace decls, they are attributes from
[ ]  1219  	 * an XML-1.0 perspective
[ ]  1220  	 */
[W]  1221          if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
[W]  1222  	    ctxt->myDoc && ctxt->myDoc->intSubset)
[ ]  1223  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc,
[ ]  1224  					   ctxt->node, prefix, nsret, val);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438, calls xmlNewNs at line 1214)
hop 2  xmlschemas.c:xmlSchemaVAttributesComplex  (/src/libxml2/xmlschemas.c:25445-26046, calls xmlNewNs at line 25829)
hop 3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)
hop 3  xmlschemas.c:xmlSchemaValidateElem  (/src/libxml2/xmlschemas.c:27084-27269, calls xmlschemas.c:xmlSchemaVAttributesComplex at line 27242)
hop 4  xmlschemas.c:xmlSchemaSAXHandleStartElementNs  (/src/libxml2/xmlschemas.c:27544-27698, calls xmlschemas.c:xmlSchemaValidateElem at line 27682)
hop 5  xmlschemas.c:startElementNsSplit  (/src/libxml2/xmlschemas.c:28793-28808, calls xmlschemas.c:xmlSchemaSAXHandleStartElementNs at line 28804)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     248        30  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)
     200         0  xmlSetNs  (/src/libxml2/tree.c:806-817)
     167         0  xmlNewNode  (/src/libxml2/tree.c:2259-2287)
     167         0  xmlNewDocNode  (/src/libxml2/tree.c:2352-2369)
      99         6  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438)
     112        28  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591)
      85         6  xmlBuildQName  (/src/libxml2/tree.c:223-247)
      50        14  xmlGetLastChild  (/src/libxml2/tree.c:3542-3551)
       3        21  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199)
      27         9  xmlSAX2ProcessingInstruction  (/src/libxml2/SAX2.c:2717-2769)
      27         9  xmlNewDocPI  (/src/libxml2/tree.c:2194-2228)
      24         6  xmlDocGetRootElement  (/src/libxml2/tree.c:5057-5068)
       0         6  xmlStringLenGetNodeList  (/src/libxml2/tree.c:1269-1487)
       0         3  xmlIsBlankNode  (/src/libxml2/tree.c:7082-7097)
       2         0  xmlStringGetNodeList  (/src/libxml2/tree.c:1499-1693)
... (3 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591) ---
  d=3   L1454  T=112 F=0  T=28 F=0  if (elemDecl == NULL) {
  d=3   L1461  T=94 F=18  T=6 F=22  if (elemDecl != NULL) {
  d=3   L1467  T=0 F=94  T=0 F=6  if ((ctxt->myDoc->standalone == 1) &&
  d=3   L1523  T=81 F=94  T=3 F=6  while (attr != NULL) {
  d=3   L1529  T=72 F=9  T=3 F=0  if (attr->defaultValue != NULL) {
  d=3   L1538  T=0 F=72  T=3 F=0  if (((attr->prefix != NULL) &&
  d=3   L1539  T=0 F=0  T=3 F=0  (xmlStrEqual(attr->prefix, BAD_CAST "xmlns"))) ||
  d=3   L1540  T=72 F=0  T=0 F=0  ((attr->prefix == NULL) &&
  d=3   L1541  T=63 F=9  T=0 F=0  (xmlStrEqual(attr->name, BAD_CAST "xmlns"))) ||
  d=3   L1542  T=9 F=0  T=0 F=0  (ctxt->loadsubset & XML_COMPLETE_ATTRS)) {
  d=3   L1548  T=0 F=72  T=0 F=3  if ((tst == attr) || (tst == NULL)) {
  d=3   L1548  T=72 F=0  T=3 F=0  if ((tst == attr) || (tst == NULL)) {
  d=3   L1553  T=0 F=72  T=0 F=3  if (fulln == NULL) {
  d=3   L1563  T=7 F=65  T=3 F=0  if (atts != NULL) {
  d=3   L1566  T=7 F=7  T=3 F=3  while (att != NULL) {
  d=3   L1567  T=0 F=7  T=0 F=3  if (xmlStrEqual(att, fulln))
  d=3   L1573  T=72 F=0  T=3 F=0  if (att == NULL) {
  d=3   L1577  T=72 F=0  T=0 F=3  if ((fulln != fn) && (fulln != attr->name))
  d=3   L1577  T=0 F=72  T=0 F=0  if ((fulln != fn) && (fulln != attr->name))
  d=3   L1584  T=0 F=94  T=0 F=6  if (internal == 1) {
--- d=3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806) ---
  d=3   L1624  T=3 F=74  T=18 F=0  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L1625  T=3 F=0  T=12 F=6  ((ctxt->myDoc->intSubset == NULL) ||
  d=3   L1626  T=0 F=0  T=6 F=0  ((ctxt->myDoc->intSubset->notations == NULL) &&
  d=3   L1627  T=0 F=0  T=6 F=0  (ctxt->myDoc->intSubset->elements == NULL) &&
  d=3   L1628  T=0 F=0  T=6 F=0  (ctxt->myDoc->intSubset->attributes == NULL) &&
  d=3   L1629  T=0 F=0  T=6 F=0  (ctxt->myDoc->intSubset->entities == NULL)))) {
  d=3   L1723  T=27 F=0  T=3 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1723  T=27 F=27  T=3 F=3  while ((att != NULL) && (value != NULL)) {
  d=3   L1724  T=18 F=0  T=0 F=3  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1724  T=18 F=5  T=3 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1724  T=23 F=4  T=3 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1725  T=18 F=0  T=0 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=3   L1725  T=18 F=0  T=0 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=3   L1738  T=41 F=0  T=250 F=32  if ((ns == NULL) && (parent != NULL))
  d=3   L1738  T=41 F=234  T=282 F=0  if ((ns == NULL) && (parent != NULL))
  d=3   L1740  T=0 F=275  T=148 F=134  if ((prefix != NULL) && (ns == NULL)) {
  d=3   L1740  T=0 F=0  T=148 F=0  if ((prefix != NULL) && (ns == NULL)) {
  d=3   L1751  T=234 F=0  T=0 F=148  if ((ns != NULL) && (ns->href != NULL) &&
  d=3   L1752  T=200 F=34  T=0 F=0  ((ns->href[0] != 0) || (ns->prefix != NULL)))
  d=3   L1752  T=0 F=34  T=0 F=0  ((ns->href[0] != 0) || (ns->prefix != NULL)))
  d=3   L1763  T=0 F=27  T=0 F=3  if (ctxt->html) {
  d=3   L1770  T=27 F=27  T=3 F=3  while ((att != NULL) && (value != NULL)) {
  d=3   L1770  T=27 F=0  T=3 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1771  T=0 F=18  T=3 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1771  T=5 F=18  T=0 F=3  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1771  T=4 F=23  T=0 F=3  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1772  T=0 F=18  T=0 F=0  (att[3] != 'n') || (att[4] != 's'))
  d=3   L1772  T=0 F=18  T=0 F=0  (att[3] != 'n') || (att[4] != 's'))
  d=3   L1789  T=74 F=201  T=0 F=282  if ((ctxt->validate) &&
  d=3   L1790  T=15 F=59  T=0 F=0  ((ctxt->vctxt.flags & XML_VCTXT_DTD_VALIDATED) == 0)) {
  d=3   L1794  T=0 F=15  T=0 F=0  if (chk <= 0)
  d=3   L1796  T=0 F=15  T=0 F=0  if (chk < 0)
  d=3   L1803  T=0 F=275  T=148 F=134  if (prefix != NULL)
--- d=2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=2   L1105  T=0 F=99  T=0 F=6  if (ctxt->html) {
  d=2   L1114  T=99 F=0  T=6 F=0  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1114  T=0 F=99  T=0 F=6  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1131  T=0 F=99  T=0 F=6  if (name == NULL) {
  d=2   L1139  T=0 F=99  T=0 F=6  if ((ctxt->html) &&
  d=2   L1156  T=0 F=99  T=0 F=6  if (ctxt->vctxt.valid != 1) {
  d=2   L1159  T=9 F=90  T=0 F=6  if (nval != NULL)
  d=2   L1169  T=92 F=7  T=0 F=6  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1169  T=99 F=0  T=6 F=0  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1170  T=81 F=11  T=0 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1170  T=81 F=0  T=0 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1170  T=81 F=0  T=0 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1171  T=81 F=0  T=0 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
  d=2   L1171  T=81 F=0  T=0 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
  d=2   L1171  T=81 F=0  T=0 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
  d=2   L1178  T=41 F=40  T=0 F=0  if (!ctxt->replaceEntities) {
  d=2   L1183  T=0 F=41  T=0 F=0  if (val == NULL) {
  d=2   L1195  T=52 F=29  T=0 F=0  if (val[0] != 0) {
  d=2   L1199  T=24 F=28  T=0 F=0  if (uri == NULL) {
  d=2   L1200  T=12 F=12  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
  d=2   L1200  T=24 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
  d=2   L1204  T=6 F=22  T=0 F=0  if (uri->scheme == NULL) {
  d=2   L1205  T=6 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
  d=2   L1205  T=0 F=6  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
  d=2   L1221  T=43 F=38  T=0 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1221  T=0 F=43  T=0 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1221  T=81 F=0  T=0 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1226  T=81 F=0  T=0 F=0  if (name != NULL)
  d=2   L1228  T=0 F=81  T=0 F=0  if (nval != NULL)
  d=2   L1230  T=41 F=40  T=0 F=0  if (val != value)
  d=2   L1234  T=18 F=0  T=6 F=0  if ((!ctxt->html) &&
  d=2   L1235  T=0 F=5  T=6 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=0 F=0  T=3 F=3  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=7 F=11  T=6 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=5 F=2  T=6 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1236  T=0 F=0  T=3 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=2   L1236  T=0 F=0  T=3 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=2   L1236  T=0 F=0  T=3 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=2   L1243  T=0 F=0  T=0 F=3  if (!ctxt->replaceEntities) {
  d=2   L1261  T=0 F=0  T=0 F=3  if (val[0] == 0) {
  d=2   L1265  T=0 F=0  T=0 F=3  if ((ctxt->pedantic != 0) && (val[0] != 0)) {
  d=2   L1289  T=0 F=0  T=0 F=3  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1289  T=0 F=0  T=3 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1294  T=0 F=0  T=3 F=0  if (name != NULL)
  d=2   L1296  T=0 F=0  T=0 F=3  if (nval != NULL)
  d=2   L1298  T=0 F=0  T=0 F=3  if (val != value)
  d=2   L1303  T=7 F=11  T=3 F=0  if (ns != NULL) {
  d=2   L1306  T=7 F=0  T=3 F=0  if (namespace == NULL) {
  d=2   L1338  T=0 F=18  T=0 F=3  if (ret == NULL)
  d=2   L1341  T=2 F=0  T=0 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1341  T=2 F=16  T=0 F=3  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1346  T=0 F=2  T=0 F=0  while (tmp != NULL) {
  d=2   L1352  T=16 F=0  T=3 F=0  } else if (value != NULL) {
  d=2   L1355  T=16 F=0  T=3 F=0  if (ret->children != NULL)
  d=2   L1360  T=16 F=2  T=0 F=3  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1360  T=0 F=16  T=0 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1360  T=18 F=0  T=3 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1403  T=18 F=0  T=3 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=2   L1404  T=2 F=16  T=0 F=3  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=2   L1404  T=2 F=0  T=0 F=0  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=2   L1405  T=16 F=0  T=3 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1405  T=16 F=0  T=3 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1407  T=16 F=2  T=3 F=0  (ret->children != NULL) &&
  d=2   L1408  T=16 F=0  T=3 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=2   L1409  T=16 F=0  T=3 F=0  (ret->children->next == NULL)) {
  d=2   L1415  T=0 F=16  T=0 F=3  if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
  d=2   L1427  T=0 F=16  T=0 F=3  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
  d=2   L1429  T=0 F=16  T=0 F=3  else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
  d=2   L1434  T=9 F=9  T=0 F=3  if (nval != NULL)
  d=2   L1436  T=7 F=11  T=3 F=0  if (ns != NULL)
--- d=1  xmlNewNs  (/src/libxml2/tree.c:733-796) ---
  d=1   L 739  T=0 F=0  T=0 F=166  if ((prefix != NULL) && (xmlStrEqual(prefix, BAD_CAST "xm...
  d=1   L 739  T=0 F=269  T=166 F=0  if ((prefix != NULL) && (xmlStrEqual(prefix, BAD_CAST "xm...
  d=1   L 766  T=0 F=269  T=166 F=0  if (prefix != NULL)  <-- BLOCKER

[off-chain: 231 additional divergent branches across 38 functions (see HIT-COUNT DIVERGENCE for which functions)]

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
Seed 4 (id=990e4190ea653e2d, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3590s, mutation_op=CrossoverReplaceMutator,QwordAddMutator,ByteDecMutator):
  0000: f9 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=c591258076306549, size=377 bytes, fuzzer=cmplog, trial=1, discovered_at=7031s, mutation_op=ByteDecMutator,ByteRandMutator,TokenInsert):
  0000: 37 37 37 32 2e 00 6d 6c 5c 0a 3c 3f 78 6d 6c 3a   7772..ml\.<?xml:
  0010: 76 65 72 0a 69 6f 6e 3d ff 31 2e 30 22 3f 3e 0a   ver.ion=.1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 3c 26 31 32 3a 37 37 32 2e   EM "dtd<&12:772.


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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6925.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6925,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6925 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6925 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6925 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).