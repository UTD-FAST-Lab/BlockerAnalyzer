==== BLOCKER ====
Target: libxml2
Branch ID: 8161
Location: /src/libxml2/tree.c:774:6
Enclosing function: xmlNewNs
Source line: 	if (node->nsDef == NULL) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           0       10          0  loser (value_profile vs value_profile_cmplog)
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog); winner (I2S vs value_profile)
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=8.30h  loser=22.90h
  avg hitcount on branch: winner=6  loser=0
  prob_div=0.90  dur_div=14.60h  hit_div=6
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=8.30h  loser=20.80h
  avg hitcount on branch: winner=6  loser=1
  prob_div=0.70  dur_div=12.50h  hit_div=6
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/8161/{W,L}/branch_coverage_show.txt

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
[B]   766      if (prefix != NULL)
[B]   767  	cur->prefix = xmlStrdup(prefix);
[ ]   768  
[ ]   769      /*
[ ]   770       * Add it at the end to preserve parsing order ...
[ ]   771       * and checks for existing use of the prefix
[ ]   772       */
[B]   773      if (node != NULL) {
[B]   774  	if (node->nsDef == NULL) { <-- BLOCKER
[B]   775  	    node->nsDef = cur;
[B]   776  	} else {
[W]   777  	    xmlNsPtr prev = node->nsDef;
[ ]   778  
[W]   779  	    if (((prev->prefix == NULL) && (cur->prefix == NULL)) ||
[W]   780  		(xmlStrEqual(prev->prefix, cur->prefix))) {
[ ]   781  		xmlFreeNs(cur);
[ ]   782  		return(NULL);
[ ]   783  	    }
[W]   784  	    while (prev->next != NULL) {
[ ]   785  	        prev = prev->next;
[ ]   786  		if (((prev->prefix == NULL) && (cur->prefix == NULL)) ||
[ ]   787  		    (xmlStrEqual(prev->prefix, cur->prefix))) {
[ ]   788  		    xmlFreeNs(cur);
[ ]   789  		    return(NULL);
[ ]   790  		}
[ ]   791  	    }
[W]   792  	    prev->next = cur;
[W]   793  	}
[B]   794      }
[B]   795      return(cur);
[B]   796  }

--- Caller (1 hop): SAX2.c:xmlSAX2AttributeInternal (/src/libxml2/SAX2.c:1097-1438, calls xmlNewNs at line 1282) (±10 around call site) ---
[W]  1272  	    } else {
[W]  1273  		if (uri->scheme == NULL) {
[ ]  1274  		    xmlNsWarnMsg(ctxt, XML_WAR_NS_URI_RELATIVE,
[ ]  1275  			   "xmlns:%s: URI %s is not absolute\n", name, value);
[ ]  1276  		}
[W]  1277  		xmlFreeURI(uri);
[W]  1278  	    }
[W]  1279  	}
[ ]  1280  
[ ]  1281  	/* a standard namespace definition */
[B]  1282  	nsret = xmlNewNs(ctxt->node, val, name); <-- CALL
[B]  1283  	xmlFree(ns);
[B]  1284  #ifdef LIBXML_VALID_ENABLED
[ ]  1285  	/*
[ ]  1286  	 * Validate also for namespace decls, they are attributes from
[ ]  1287  	 * an XML-1.0 perspective
[ ]  1288  	 */
[B]  1289          if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
[B]  1290  	    ctxt->myDoc && ctxt->myDoc->intSubset)
[B]  1291  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc,
[B]  1292  					   ctxt->node, prefix, nsret, value);

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
      60      1290  xmlSearchNs  (/src/libxml2/tree.c:6134-6207)
      48      1000  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      48      1000  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
      29       844  xmlAddChild  (/src/libxml2/tree.c:3418-3532)
      30       708  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806)
      30       708  xmlNewNodeEatName  (/src/libxml2/tree.c:2303-2332)
      30       708  xmlNewDocNodeEatName  (/src/libxml2/tree.c:2389-2407)
      15       376  xmlFreeNsList  (/src/libxml2/tree.c:846-860)
      30       376  xmlNewNs  (/src/libxml2/tree.c:733-796)  <-- enclosing
      30       376  xmlFreeNs  (/src/libxml2/tree.c:826-837)
      12       347  SAX2.c:xmlNsWarnMsg  (/src/libxml2/SAX2.c:194-204)
      41       343  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
      20       284  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
      15       213  xmlSAX2SetDocumentLocator  (/src/libxml2/SAX2.c:942-948)
      15       213  xmlSAX2StartDocument  (/src/libxml2/SAX2.c:958-1013)
... (26 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591) ---
  d=3   L1454  T=30 F=0  T=83 F=0  if (elemDecl == NULL) {
  d=3   L1461  T=30 F=0  T=47 F=36  if (elemDecl != NULL) {
  d=3   L1538  T=18 F=0  T=40 F=6  if (((attr->prefix != NULL) &&
  d=3   L1539  T=18 F=0  T=23 F=17  (xmlStrEqual(attr->prefix, BAD_CAST "xmlns"))) ||
  d=3   L1540  T=0 F=0  T=6 F=17  ((attr->prefix == NULL) &&
  d=3   L1541  T=0 F=0  T=3 F=3  (xmlStrEqual(attr->name, BAD_CAST "xmlns"))) ||
  d=3   L1542  T=0 F=0  T=12 F=8  (ctxt->loadsubset & XML_COMPLETE_ATTRS)) {
  d=3   L1548  T=0 F=18  T=0 F=38  if ((tst == attr) || (tst == NULL)) {
  d=3   L1548  T=18 F=0  T=38 F=0  if ((tst == attr) || (tst == NULL)) {
  d=3   L1553  T=0 F=18  T=0 F=38  if (fulln == NULL) {
  d=3   L1563  T=12 F=6  T=30 F=8  if (atts != NULL) {
  d=3   L1566  T=12 F=12  T=30 F=30  while (att != NULL) {
  d=3   L1567  T=0 F=12  T=0 F=30  if (xmlStrEqual(att, fulln))
  d=3   L1573  T=18 F=0  T=38 F=0  if (att == NULL) {
  d=3   L1577  T=0 F=18  T=6 F=32  if ((fulln != fn) && (fulln != attr->name))
  d=3   L1577  T=0 F=0  T=0 F=6  if ((fulln != fn) && (fulln != attr->name))
--- d=3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806) ---
  d=3   L1614  T=0 F=30  T=0 F=708  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=3   L1614  T=0 F=30  T=0 F=708  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=3   L1614  T=0 F=30  T=0 F=708  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=3   L1624  T=30 F=0  T=146 F=562  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L1624  T=0 F=30  T=114 F=32  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L1625  T=0 F=0  T=108 F=6  ((ctxt->myDoc->intSubset == NULL) ||
  d=3   L1626  T=0 F=0  T=6 F=0  ((ctxt->myDoc->intSubset->notations == NULL) &&
  d=3   L1627  T=0 F=0  T=6 F=0  (ctxt->myDoc->intSubset->elements == NULL) &&
  d=3   L1628  T=0 F=0  T=6 F=0  (ctxt->myDoc->intSubset->attributes == NULL) &&
  d=3   L1629  T=0 F=0  T=6 F=0  (ctxt->myDoc->intSubset->entities == NULL)))) {
  d=3   L1648  T=0 F=30  T=0 F=708  if (ret == NULL) {
  d=3   L1654  T=0 F=30  T=170 F=538  if (ctxt->myDoc->children == NULL) {
  d=3   L1659  T=15 F=15  T=175 F=363  } else if (parent == NULL) {
  d=3   L1663  T=30 F=0  T=708 F=0  if (ctxt->linenumbers) {
  d=3   L1664  T=30 F=0  T=708 F=0  if (ctxt->input != NULL) {
  d=3   L1665  T=30 F=0  T=708 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=3   L1678  T=0 F=30  T=0 F=708  if (nodePush(ctxt, ret) < 0) {
  d=3   L1689  T=30 F=0  T=538 F=170  if (parent != NULL) {
  d=3   L1690  T=15 F=15  T=468 F=70  if (parent->type == XML_ELEMENT_NODE) {
  d=3   L1706  T=30 F=0  T=708 F=0  if (!ctxt->html) {
  d=3   L1711  T=30 F=0  T=83 F=625  if ((ctxt->myDoc->intSubset != NULL) ||
  d=3   L1712  T=0 F=0  T=0 F=625  (ctxt->myDoc->extSubset != NULL)) {
  d=3   L1719  T=12 F=18  T=77 F=631  if (atts != NULL) {
  d=3   L1723  T=12 F=0  T=79 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1723  T=12 F=12  T=79 F=77  while ((att != NULL) && (value != NULL)) {
  d=3   L1724  T=12 F=0  T=3 F=3  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1724  T=12 F=0  T=6 F=61  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1724  T=12 F=0  T=67 F=12  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1725  T=12 F=0  T=3 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=3   L1725  T=12 F=0  T=3 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=3   L1738  T=30 F=0  T=535 F=170  if ((ns == NULL) && (parent != NULL))
  d=3   L1738  T=30 F=0  T=705 F=3  if ((ns == NULL) && (parent != NULL))
  d=3   L1740  T=0 F=30  T=347 F=361  if ((prefix != NULL) && (ns == NULL)) {
  d=3   L1740  T=0 F=0  T=347 F=0  if ((prefix != NULL) && (ns == NULL)) {
  d=3   L1751  T=0 F=30  T=350 F=358  if ((ns != NULL) && (ns->href != NULL) &&
  d=3   L1751  T=0 F=0  T=3 F=347  if ((ns != NULL) && (ns->href != NULL) &&
  d=3   L1752  T=0 F=0  T=3 F=0  ((ns->href[0] != 0) || (ns->prefix != NULL)))
  d=3   L1759  T=12 F=18  T=77 F=631  if (atts != NULL) {
  d=3   L1763  T=0 F=12  T=0 F=77  if (ctxt->html) {
  d=3   L1770  T=12 F=12  T=79 F=77  while ((att != NULL) && (value != NULL)) {
  d=3   L1770  T=12 F=0  T=79 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1771  T=0 F=12  T=3 F=3  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1771  T=0 F=12  T=61 F=6  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1771  T=0 F=12  T=12 F=67  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1772  T=0 F=12  T=0 F=3  (att[3] != 'n') || (att[4] != 's'))
  d=3   L1772  T=0 F=12  T=0 F=3  (att[3] != 'n') || (att[4] != 's'))
  d=3   L1789  T=30 F=0  T=32 F=676  if ((ctxt->validate) &&
  d=3   L1803  T=0 F=30  T=347 F=361  if (prefix != NULL)
--- d=2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=2   L1105  T=0 F=30  T=0 F=117  if (ctxt->html) {
  d=2   L1114  T=30 F=0  T=117 F=0  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1114  T=0 F=30  T=0 F=117  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1131  T=0 F=30  T=0 F=117  if (name == NULL) {
  d=2   L1139  T=0 F=30  T=0 F=117  if ((ctxt->html) &&
  d=2   L1156  T=0 F=30  T=0 F=117  if (ctxt->vctxt.valid != 1) {
  d=2   L1159  T=3 F=27  T=12 F=105  if (nval != NULL)
  d=2   L1169  T=0 F=30  T=38 F=79  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1169  T=30 F=0  T=117 F=0  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1170  T=0 F=0  T=26 F=12  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1170  T=0 F=0  T=3 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1170  T=0 F=0  T=3 F=23  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1171  T=0 F=0  T=3 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
  d=2   L1171  T=0 F=0  T=3 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
  d=2   L1171  T=0 F=0  T=3 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
  d=2   L1178  T=0 F=0  T=0 F=3  if (!ctxt->replaceEntities) {
  d=2   L1195  T=0 F=0  T=3 F=0  if (val[0] != 0) {
  d=2   L1199  T=0 F=0  T=0 F=3  if (uri == NULL) {
  d=2   L1204  T=0 F=0  T=0 F=3  if (uri->scheme == NULL) {
  d=2   L1221  T=0 F=0  T=0 F=3  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1221  T=0 F=0  T=3 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1226  T=0 F=0  T=3 F=0  if (name != NULL)
  d=2   L1228  T=0 F=0  T=0 F=3  if (nval != NULL)
  d=2   L1230  T=0 F=0  T=0 F=3  if (val != value)
  d=2   L1234  T=30 F=0  T=114 F=0  if ((!ctxt->html) &&
  d=2   L1235  T=30 F=0  T=29 F=50  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=30 F=0  T=26 F=3  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=30 F=0  T=79 F=35  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=30 F=0  T=79 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1248  T=0 F=24  T=0 F=8  if (val == NULL) {
  d=2   L1265  T=24 F=0  T=0 F=0  if ((ctxt->pedantic != 0) && (val[0] != 0)) {
  d=2   L1265  T=24 F=6  T=0 F=26  if ((ctxt->pedantic != 0) && (val[0] != 0)) {
  d=2   L1269  T=12 F=12  T=0 F=0  if (uri == NULL) {
  d=2   L1273  T=0 F=12  T=0 F=0  if (uri->scheme == NULL) {
  d=2   L1289  T=30 F=0  T=17 F=9  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1290  T=18 F=0  T=6 F=0  ctxt->myDoc && ctxt->myDoc->intSubset)
  d=2   L1290  T=18 F=0  T=6 F=0  ctxt->myDoc && ctxt->myDoc->intSubset)
  d=2   L1296  T=3 F=27  T=0 F=26  if (nval != NULL)
  d=2   L1303  T=0 F=0  T=53 F=35  if (ns != NULL) {
  d=2   L1306  T=0 F=0  T=38 F=15  if (namespace == NULL) {
  d=2   L1314  T=0 F=0  T=6 F=15  while (prop != NULL) {
  d=2   L1315  T=0 F=0  T=6 F=0  if (prop->ns != NULL) {
  d=2   L1316  T=0 F=0  T=0 F=6  if ((xmlStrEqual(name, prop->name)) &&
  d=2   L1338  T=0 F=0  T=0 F=88  if (ret == NULL)
  d=2   L1341  T=0 F=0  T=35 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1341  T=0 F=0  T=35 F=53  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1346  T=0 F=0  T=35 F=35  while (tmp != NULL) {
  d=2   L1348  T=0 F=0  T=35 F=0  if (tmp->next == NULL)
  d=2   L1352  T=0 F=0  T=53 F=0  } else if (value != NULL) {
  d=2   L1355  T=0 F=0  T=53 F=0  if (ret->children != NULL)
  d=2   L1360  T=0 F=0  T=21 F=67  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1360  T=0 F=0  T=9 F=12  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1360  T=0 F=0  T=88 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1361  T=0 F=0  T=9 F=0  ctxt->myDoc && ctxt->myDoc->intSubset) {
  d=2   L1361  T=0 F=0  T=9 F=0  ctxt->myDoc && ctxt->myDoc->intSubset) {
  d=2   L1367  T=0 F=0  T=3 F=6  if (!ctxt->replaceEntities) {
  d=2   L1375  T=0 F=0  T=0 F=3  if (val == NULL)
  d=2   L1388  T=0 F=0  T=0 F=3  if (nvalnorm != NULL) {
  d=2   L1403  T=0 F=0  T=79 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=2   L1404  T=0 F=0  T=32 F=47  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=2   L1404  T=0 F=0  T=32 F=0  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=2   L1405  T=0 F=0  T=47 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1405  T=0 F=0  T=47 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1407  T=0 F=0  T=79 F=0  (ret->children != NULL) &&
  d=2   L1408  T=0 F=0  T=79 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=2   L1409  T=0 F=0  T=79 F=0  (ret->children->next == NULL)) {
  d=2   L1415  T=0 F=0  T=0 F=79  if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
  d=2   L1427  T=0 F=0  T=0 F=79  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
  d=2   L1429  T=0 F=0  T=0 F=79  else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
  d=2   L1434  T=0 F=0  T=12 F=76  if (nval != NULL)
  d=2   L1436  T=0 F=0  T=53 F=35  if (ns != NULL)
--- d=1  xmlNewNs  (/src/libxml2/tree.c:733-796) ---
  d=1   L 736  T=30 F=0  T=376 F=0  if ((node != NULL) && (node->type != XML_ELEMENT_NODE))
  d=1   L 736  T=0 F=30  T=0 F=376  if ((node != NULL) && (node->type != XML_ELEMENT_NODE))
  d=1   L 739  T=0 F=30  T=0 F=373  if ((prefix != NULL) && (xmlStrEqual(prefix, BAD_CAST "xm...
  d=1   L 739  T=30 F=0  T=373 F=3  if ((prefix != NULL) && (xmlStrEqual(prefix, BAD_CAST "xm...
  d=1   L 757  T=0 F=30  T=0 F=376  if (cur == NULL) {
  d=1   L 764  T=30 F=0  T=29 F=347  if (href != NULL)
  d=1   L 766  T=30 F=0  T=373 F=3  if (prefix != NULL)
  d=1   L 773  T=30 F=0  T=376 F=0  if (node != NULL) {
  d=1   L 774  T=15 F=15  T=376 F=0  if (node->nsDef == NULL) {  <-- BLOCKER
  d=1   L 779  T=0 F=15  T=0 F=0  if (((prev->prefix == NULL) && (cur->prefix == NULL)) ||
  d=1   L 780  T=0 F=15  T=0 F=0  (xmlStrEqual(prev->prefix, cur->prefix))) {
  d=1   L 784  T=0 F=15  T=0 F=0  while (prev->next != NULL) {

[off-chain: 329 additional divergent branches across 46 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=a425477316d1bc9c, size=381 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1682s, mutation_op=CrossoverInsertMutator,BytesExpandMutator,ByteAddMutator,TokenInsert):
  0000: f5 ff ff ff ff ff ff ff 06 00 00 00 31 32 37 37   ............1277
  0010: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 0a 61 20 53 59 53 54 45 4d   DOCTYPE.a SYSTEM
Seed 2 (id=8022c433e1cf131c, size=381 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=21097s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,DwordAddMutator):
  0000: f5 ff ff ff ff ff ff ff 06 00 00 00 31 32 37 37   ............1277
  0010: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 0a 61 20 53 59 53 54 45 4d   DOCTYPE.a SYSTEM
Seed 3 (id=fe67214245b40d4f, size=381 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=21097s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,DwordAddMutator):
  0000: f5 ff ff ff ff ff ff ff 06 00 00 00 31 32 37 37   ............1277
  0010: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 0a 61 20 53 59 53 54 45 4d   DOCTYPE.a SYSTEM
Seed 4 (id=e77944c783da000c, size=381 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=46283s, mutation_op=ByteAddMutator,ByteAddMutator):
  0000: f5 ff ff ff ff ff ff ff 06 5f 00 00 31 32 37 37   ........._..1277
  0010: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 0a 61 20 53 59 53 54 45 4d   DOCTYPE.a SYSTEM
Seed 5 (id=d44eec97c6b0e23a, size=398 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=70673s, mutation_op=BytesDeleteMutator,BytesInsertMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 0a 61 20 53 59 53 54 45 4d   DOCTYPE.a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=1435a2b24f018cc2, size=375 bytes, fuzzer=cmplog, trial=2, discovered_at=1s, mutation_op=BytesInsertCopyMutator,BytesDeleteMutator):
  0000: 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7772.xml\.<?xml 
  0010: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e   EM "dtds/127772.
Seed 2 (id=027913052b5d6b70, size=141 bytes, fuzzer=cmplog, trial=2, discovered_at=28s, mutation_op=ByteFlipMutator,BytesCopyMutator,ByteDecMutator,ByteRandMutator,BytesRandSetMutator,BytesDeleteMutator):
  0000: 6b 27 0a 20 20 20 20 20 20 20 20 20 20 20 20 78   k'.            x
  0010: 6c 69 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c   li....127772.xml
  0020: 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d   \.<?xml version=
  0030: 22 31 2e 30 22 3f 3e 0a 3c 6e 6b 3a 74 79 70 1f   "1.0"?>.<nk:typ.
Seed 3 (id=0113792fe5a5dc70, size=97 bytes, fuzzer=value_profile, trial=1, discovered_at=106s, mutation_op=BytesInsertCopyMutator,ByteAddMutator,DwordAddMutator,ByteFlipMutator,BytesDeleteMutator):
  0000: 49 53 54 20 55 54 20 62 20 78 6d 6c 6e 73 3a 78   IST UT b xmlns:x
  0010: 6c 51 54 6b 20 20 43 44 41 54 41 20 20 55 54 46   lQTk  CDATA  UTF
  0020: 38 20 20 20 78 6c 69 6e 6b 3a 68 72 65 66 20 20   8   xlink:href  
  0030: 20 43 74 64 73 2f f1 32 37 37 37 32 2e 64 74 64    Ctds/.27772.dtd
Seed 4 (id=0dbb09534c8db0ab, size=438 bytes, fuzzer=value_profile, trial=1, discovered_at=1116s, mutation_op=ByteDecMutator,ByteFlipMutator,ByteFlipMutator,CrossoverInsertMutator):
  0000: 31 32 37 37 37 32 2e 64 aa aa aa aa aa aa aa aa   127772.d........
  0010: 2f 31 32 37 37 37 32 2e 64 74 64 22 3e 0a 0a 3b   /127772.dtd">..;
  0020: 61 3e 0a 20 64 73 2f cf 32 64 00 00 00 2e 64 74   a>. ds/.2d....dt
  0030: 64 5c 0a 3c 6e 6b 3a 74 79 70 65 76 65 72 73 69   d\.<nk:typeversi
Seed 5 (id=05f6a2e17ed1a7c1, size=156 bytes, fuzzer=cmplog, trial=1, discovered_at=1215s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,ByteRandMutator):
  0000: 69 6e 6b 6d 70 6c 65 29 20 20 23 46 49 58 45 44   inkmple)  #FIXED
  0010: 20 27 20 13 13 13 13 13 13 13 13 13 13 13 13 13    ' .............
  0020: 13 13 13 58 45 44 20 27 20 20 06 00 00 00 31 32   ...XED '  ....12
  0030: 0a 37 37 32 40 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   .772@xml\.<?xml 


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f5(.)x4 37(7)x1                     37(7)x9 31(1)x4 5b([)x4 6b(k)x3 +33u  PARTIAL
   0x0001  ff(.)x4 32(2)x1                     32(2)x9 37(7)x7 ff(.)x7 2f(/)x5 +26u  PARTIAL
   0x0002  ff(.)x4 2e(.)x1                     ff(.)x8 37(7)x7 2e(.)x5 5b([)x4 +31u  PARTIAL
   0x0003  ff(.)x4 78(x)x1                     2e(.)x6 32(2)x5 37(7)x4 ff(.)x4 +37u  PARTIAL
   0x0004  ff(.)x4 6d(m)x1                     2e(.)x6 37(7)x5 70(p)x5 74(t)x4 +34u  PARTIAL
   0x0005  ff(.)x4 6c(l)x1                     32(2)x8 ff(.)x6 64(d)x5 00(.)x4 +32u  PARTIAL
   0x0006  ff(.)x4 5c(\)x1                     37(7)x7 ff(.)x6 2e(.)x5 00(.)x5 +27u  PARTIAL
   0x0007  ff(.)x4 0a(.)x1                     37(7)x9 ff(.)x6 2f(/)x6 6c(l)x4 +31u  PARTIAL
   0x0008  06(.)x4 3c(<)x1                     37(7)x13 0a(.)x6 5c(\)x5 2f(/)x4 +31u  PARTIAL
   0x0009  00(.)x3 5f(_)x1 3f(?)x1             32(2)x10 0a(.)x7 37(7)x4 20( )x3 +31u  PARTIAL
   0x000a  00(.)x4 78(x)x1                     2e(.)x10 3c(<)x6 2f(/)x5 20( )x3 +32u  PARTIAL
   0x000b  00(.)x4 6d(m)x1                     78(x)x12 2e(.)x7 0a(.)x5 3f(?)x4 +32u  PARTIAL
   0x000c  31(1)x4 6c(l)x1                     6d(m)x10 78(x)x5 00(.)x3 5c(\)x3 +32u  PARTIAL
   0x000d  32(2)x4 20( )x1                     6c(l)x11 20( )x5 2f(/)x5 6d(m)x4 +34u  PARTIAL
   0x000e  37(7)x4 76(v)x1                     5c(\)x12 6c(l)x4 20( )x4 3e(>)x4 +36u  PARTIAL
   0x000f  37(7)x4 65(e)x1                     0a(.)x16 2f(/)x4 20( )x3 6e(n)x3 +33u  PARTIAL
   0x0010  37(7)x4 72(r)x1                     3c(<)x13 2f(/)x7 0a(.)x6 20( )x4 +30u  PARTIAL
   0x0011  32(2)x4 73(s)x1                     3f(?)x8 3c(<)x5 65(e)x4 20( )x4 +35u  DIFFER
   0x0012  2e(.)x4 69(i)x1                     78(x)x8 74(t)x5 32(2)x4 20( )x4 +35u  DIFFER
   0x0013  78(x)x4 6f(o)x1                     6d(m)x8 37(7)x6 3a(:)x5 2f(/)x4 +35u  DIFFER
   0x0014  6d(m)x4 6e(n)x1                     6c(l)x8 2f(/)x6 20( )x5 37(7)x4 +34u  PARTIAL
   0x0015  6c(l)x4 3d(=)x1                     20( )x13 2f(/)x6 37(7)x4 0a(.)x4 +32u  PARTIAL
   0x0016  5c(\)x4 22(")x1                     20( )x10 76(v)x8 6e(n)x4 32(2)x4 +30u  PARTIAL
   0x0017  0a(.)x4 31(1)x1                     65(e)x11 2e(.)x5 2f(/)x4 3c(<)x4 +35u  PARTIAL
   0x0018  3c(<)x4 2e(.)x1                     72(r)x8 20( )x6 62(b)x4 78(x)x4 +33u  PARTIAL
   0x0019  3f(?)x4 30(0)x1                     73(s)x9 20( )x5 2f(/)x4 0a(.)x4 +36u  PARTIAL
   0x001a  78(x)x4 22(")x1                     69(i)x9 20( )x7 6c(l)x5 3a(:)x4 +33u  PARTIAL
   0x001b  6d(m)x4 3f(?)x1                     6f(o)x8 20( )x6 5c(\)x4 22(")x3 +35u  DIFFER
   0x001c  6c(l)x4 3e(>)x1                     20( )x9 6e(n)x8 3a(:)x3 45(E)x3 +33u  PARTIAL
   0x001d  20( )x4 0a(.)x1                     3d(=)x7 20( )x6 74(t)x5 37(7)x4 +34u  PARTIAL
   0x001e  76(v)x4 3c(<)x1                     22(")x8 20( )x7 3f(?)x5 3e(>)x4 +34u  PARTIAL
   0x001f  65(e)x4 21(!)x1                     0a(.)x7 20( )x5 31(1)x5 78(x)x4 +31u  PARTIAL
   0x0020  72(r)x4 44(D)x1                     20( )x6 2e(.)x6 0a(.)x4 3c(<)x3 +37u  DIFFER
   0x0021  73(s)x4 4f(O)x1                     30(0)x6 3c(<)x5 0a(.)x4 20( )x4 +31u  DIFFER
   0x0022  69(i)x4 43(C)x1                     20( )x8 22(")x6 0a(.)x4 44(D)x3 +36u  PARTIAL
   0x0023  6f(o)x4 54(T)x1                     20( )x10 3f(?)x4 54(T)x4 74(t)x3 +38u  PARTIAL
   0x0024  6e(n)x4 59(Y)x1                     20( )x7 3e(>)x7 54(T)x4 65(e)x4 +33u  PARTIAL
   0x0025  3d(=)x4 50(P)x1                     0a(.)x7 54(T)x4 20( )x4 37(7)x3 +41u  PARTIAL
   0x0026  22(")x4 45(E)x1                     54(T)x5 78(x)x4 3c(<)x4 59(Y)x3 +39u  DIFFER
   0x0027  31(1)x4 0a(.)x1                     20( )x7 45(E)x5 54(T)x4 6c(l)x3 +36u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_8161.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8161,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8161 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8161 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8161 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).