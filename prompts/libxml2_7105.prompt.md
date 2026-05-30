==== BLOCKER ====
Target: libxml2
Branch ID: 7105
Location: /src/libxml2/valid.c:2791:18
Enclosing function: xmlIsID
Source line: 	fullelemname = (elem->ns != NULL && elem->ns->prefix != NULL) ?
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=13.10h  loser=20.30h
  avg hitcount on branch: winner=16  loser=1
  prob_div=0.60  dur_div=7.20h  hit_div=15
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7105/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlIsID (/src/libxml2/valid.c:2767-2816) ---
[ ]  2765   */
[ ]  2766  int
[B]  2767  xmlIsID(xmlDocPtr doc, xmlNodePtr elem, xmlAttrPtr attr) {
[B]  2768      if ((attr == NULL) || (attr->name == NULL)) return(0);
[B]  2769      if ((attr->ns != NULL) && (attr->ns->prefix != NULL) &&
[B]  2770          (!strcmp((char *) attr->name, "id")) &&
[B]  2771          (!strcmp((char *) attr->ns->prefix, "xml")))
[ ]  2772  	return(1);
[B]  2773      if (doc == NULL) return(0);
[B]  2774      if ((doc->intSubset == NULL) && (doc->extSubset == NULL) &&
[B]  2775          (doc->type != XML_HTML_DOCUMENT_NODE)) {
[ ]  2776  	return(0);
[B]  2777      } else if (doc->type == XML_HTML_DOCUMENT_NODE) {
[ ]  2778          if ((xmlStrEqual(BAD_CAST "id", attr->name)) ||
[ ]  2779  	    ((xmlStrEqual(BAD_CAST "name", attr->name)) &&
[ ]  2780  	    ((elem == NULL) || (xmlStrEqual(elem->name, BAD_CAST "a")))))
[ ]  2781  	    return(1);
[ ]  2782  	return(0);
[B]  2783      } else if (elem == NULL) {
[ ]  2784  	return(0);
[B]  2785      } else {
[B]  2786  	xmlAttributePtr attrDecl = NULL;
[ ]  2787  
[B]  2788  	xmlChar felem[50], fattr[50];
[B]  2789  	xmlChar *fullelemname, *fullattrname;
[ ]  2790  
[B]  2791  	fullelemname = (elem->ns != NULL && elem->ns->prefix != NULL) ? <-- BLOCKER
[ ]  2792  	    xmlBuildQName(elem->name, elem->ns->prefix, felem, 50) :
[B]  2793  	    (xmlChar *)elem->name;
[ ]  2794  
[B]  2795  	fullattrname = (attr->ns != NULL && attr->ns->prefix != NULL) ?
[ ]  2796  	    xmlBuildQName(attr->name, attr->ns->prefix, fattr, 50) :
[B]  2797  	    (xmlChar *)attr->name;
[ ]  2798  
[B]  2799  	if (fullelemname != NULL && fullattrname != NULL) {
[B]  2800  	    attrDecl = xmlGetDtdAttrDesc(doc->intSubset, fullelemname,
[B]  2801  		                         fullattrname);
[B]  2802  	    if ((attrDecl == NULL) && (doc->extSubset != NULL))
[B]  2803  		attrDecl = xmlGetDtdAttrDesc(doc->extSubset, fullelemname,
[B]  2804  					     fullattrname);
[B]  2805  	}
[ ]  2806  
[B]  2807  	if ((fullattrname != fattr) && (fullattrname != attr->name))
[ ]  2808  	    xmlFree(fullattrname);
[B]  2809  	if ((fullelemname != felem) && (fullelemname != elem->name))
[ ]  2810  	    xmlFree(fullelemname);
[ ]  2811  
[B]  2812          if ((attrDecl != NULL) && (attrDecl->atype == XML_ATTRIBUTE_ID))
[ ]  2813  	    return(1);
[B]  2814      }
[B]  2815      return(0);
[B]  2816  }

--- Caller (1 hop): tree.c:xmlNewPropInternal (/src/libxml2/tree.c:1871-1951, calls xmlIsID at line 1945) (±10 around call site) ---
[L]  1935              xmlAttrPtr prev = node->properties;
[ ]  1936  
[L]  1937              while (prev->next != NULL)
[ ]  1938                  prev = prev->next;
[L]  1939              prev->next = cur;
[L]  1940              cur->prev = prev;
[L]  1941          }
[B]  1942      }
[ ]  1943  
[B]  1944      if ((value != NULL) && (node != NULL) &&
[B]  1945          (xmlIsID(node->doc, node, cur) == 1)) <-- CALL
[ ]  1946          xmlAddID(NULL, node->doc, value, cur);
[ ]  1947  
[B]  1948      if ((__xmlRegisterCallbacks) && (xmlRegisterNodeDefaultValue))
[ ]  1949          xmlRegisterNodeDefaultValue((xmlNodePtr) cur);
[B]  1950      return (cur);
[B]  1951  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438, calls xmlIsID at line 1427)
hop 2  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199, calls xmlIsID at line 2191)
hop 3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)
hop 3  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459, calls SAX2.c:xmlSAX2AttributeNs at line 2421)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      33       116  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
      27       106  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      27       106  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
      15        78  xmlNewNodeEatName  (/src/libxml2/tree.c:2303-2332)
      15        78  xmlNewDocNodeEatName  (/src/libxml2/tree.c:2389-2407)
      12        66  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)
      21        65  xmlGetIntSubset  (/src/libxml2/tree.c:924-936)
       2        39  xmlNewNsPropEatName  (/src/libxml2/tree.c:2016-2027)
      12        46  xmlFreeNodeList  (/src/libxml2/tree.c:3757-3830)
       8        39  tree.c:xmlNewPropInternal  (/src/libxml2/tree.c:1871-1951)
       8        39  xmlIsID  (/src/libxml2/valid.c:2767-2816)  <-- enclosing
       8        39  xmlIsRef  (/src/libxml2/valid.c:3115-3143)
      12        40  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
       6        33  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199)
       9        30  xmlSAX2InternalSubset  (/src/libxml2/SAX2.c:330-354)
... (40 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591) ---
  d=3   L1461  T=15 F=0  T=2 F=10  if (elemDecl != NULL) {
  d=3   L1467  T=0 F=15  T=0 F=2  if ((ctxt->myDoc->standalone == 1) &&
  d=3   L1523  T=10 F=15  T=0 F=2  while (attr != NULL) {
  d=3   L1529  T=10 F=0  T=0 F=0  if (attr->defaultValue != NULL) {
  d=3   L1538  T=0 F=10  T=0 F=0  if (((attr->prefix != NULL) &&
  d=3   L1540  T=10 F=0  T=0 F=0  ((attr->prefix == NULL) &&
  d=3   L1541  T=10 F=0  T=0 F=0  (xmlStrEqual(attr->name, BAD_CAST "xmlns"))) ||
  d=3   L1548  T=0 F=10  T=0 F=0  if ((tst == attr) || (tst == NULL)) {
  d=3   L1548  T=10 F=0  T=0 F=0  if ((tst == attr) || (tst == NULL)) {
  d=3   L1553  T=0 F=10  T=0 F=0  if (fulln == NULL) {
  d=3   L1563  T=2 F=8  T=0 F=0  if (atts != NULL) {
  d=3   L1566  T=2 F=2  T=0 F=0  while (att != NULL) {
  d=3   L1567  T=0 F=2  T=0 F=0  if (xmlStrEqual(att, fulln))
  d=3   L1573  T=10 F=0  T=0 F=0  if (att == NULL) {
  d=3   L1577  T=10 F=0  T=0 F=0  if ((fulln != fn) && (fulln != attr->name))
  d=3   L1577  T=0 F=10  T=0 F=0  if ((fulln != fn) && (fulln != attr->name))
  d=3   L1584  T=0 F=15  T=0 F=2  if (internal == 1) {
--- d=3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806) ---
  d=3   L1624  T=15 F=0  T=8 F=4  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L1624  T=0 F=15  T=4 F=4  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L1625  T=0 F=0  T=0 F=4  ((ctxt->myDoc->intSubset == NULL) ||
  d=3   L1626  T=0 F=0  T=4 F=0  ((ctxt->myDoc->intSubset->notations == NULL) &&
  d=3   L1627  T=0 F=0  T=4 F=0  (ctxt->myDoc->intSubset->elements == NULL) &&
  d=3   L1628  T=0 F=0  T=4 F=0  (ctxt->myDoc->intSubset->attributes == NULL) &&
  d=3   L1629  T=0 F=0  T=4 F=0  (ctxt->myDoc->intSubset->entities == NULL)))) {
  d=3   L1723  T=2 F=0  T=6 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1723  T=2 F=2  T=6 F=6  while ((att != NULL) && (value != NULL)) {
  d=3   L1724  T=0 F=2  T=0 F=6  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1724  T=2 F=0  T=6 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1738  T=5 F=0  T=12 F=0  if ((ns == NULL) && (parent != NULL))
  d=3   L1738  T=5 F=10  T=12 F=0  if ((ns == NULL) && (parent != NULL))
  d=3   L1751  T=10 F=5  T=0 F=12  if ((ns != NULL) && (ns->href != NULL) &&
  d=3   L1751  T=10 F=0  T=0 F=0  if ((ns != NULL) && (ns->href != NULL) &&
  d=3   L1752  T=10 F=0  T=0 F=0  ((ns->href[0] != 0) || (ns->prefix != NULL)))
  d=3   L1763  T=0 F=2  T=0 F=6  if (ctxt->html) {
  d=3   L1770  T=2 F=2  T=6 F=6  while ((att != NULL) && (value != NULL)) {
  d=3   L1770  T=2 F=0  T=6 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1771  T=2 F=0  T=6 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1771  T=0 F=2  T=0 F=6  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1789  T=15 F=0  T=4 F=8  if ((ctxt->validate) &&
  d=3   L1790  T=3 F=12  T=2 F=2  ((ctxt->vctxt.flags & XML_VCTXT_DTD_VALIDATED) == 0)) {
--- d=3  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459) ---
  d=3   L2237  T=0 F=12  T=0 F=66  if (ctx == NULL) return;
  d=3   L2242  T=12 F=0  T=0 F=66  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L2242  T=0 F=12  T=0 F=0  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L2256  T=0 F=12  T=0 F=66  if ((prefix != NULL) && (URI == NULL)) {
  d=3   L2270  T=0 F=12  T=0 F=66  if (ctxt->freeElems != NULL) {
  d=3   L2293  T=0 F=12  T=66 F=0  if (ctxt->dictNames)
  d=3   L2296  T=12 F=0  T=0 F=0  else if (lname == NULL)
  d=3   L2301  T=0 F=12  T=0 F=66  if (ret == NULL) {
  d=3   L2306  T=12 F=0  T=66 F=0  if (ctxt->linenumbers) {
  d=3   L2307  T=12 F=0  T=66 F=0  if (ctxt->input != NULL) {
  d=3   L2308  T=12 F=0  T=66 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=3   L2315  T=6 F=6  T=26 F=40  if (parent == NULL) {
  d=3   L2321  T=6 F=12  T=3 F=66  for (i = 0,j = 0;j < nb_namespaces;j++) {
  d=3   L2325  T=6 F=0  T=3 F=0  if (ns != NULL) {
  d=3   L2326  T=6 F=0  T=3 F=0  if (last == NULL) {
  d=3   L2332  T=6 F=0  T=0 F=0  if ((URI != NULL) && (prefix == pref))
  d=3   L2332  T=6 F=0  T=0 F=3  if ((URI != NULL) && (prefix == pref))
  d=3   L2343  T=6 F=0  T=0 F=3  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=3   L2343  T=0 F=6  T=0 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=3   L2343  T=6 F=0  T=3 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=3   L2355  T=0 F=12  T=0 F=66  if (nodePush(ctxt, ret) < 0) {
  d=3   L2364  T=6 F=6  T=40 F=26  if (parent != NULL) {
  d=3   L2365  T=6 F=0  T=40 F=0  if (parent->type == XML_ELEMENT_NODE) {
  d=3   L2375  T=3 F=9  T=3 F=63  if ((nb_defaulted != 0) &&
  d=3   L2376  T=3 F=0  T=0 F=3  ((ctxt->loadsubset & XML_COMPLETE_ATTRS) == 0))
  d=3   L2383  T=0 F=6  T=0 F=0  if ((URI != NULL) && (ret->ns == NULL)) {
  d=3   L2383  T=6 F=6  T=0 F=66  if ((URI != NULL) && (ret->ns == NULL)) {
  d=3   L2409  T=6 F=6  T=30 F=36  if (nb_attributes > 0) {
  d=3   L2410  T=6 F=6  T=33 F=30  for (j = 0,i = 0;i < nb_attributes;i++,j+=5) {
  d=3   L2414  T=6 F=0  T=33 F=0  if ((attributes[j+1] != NULL) && (attributes[j+2] == NULL...
  d=3   L2414  T=6 F=0  T=33 F=0  if ((attributes[j+1] != NULL) && (attributes[j+2] == NULL...
  d=3   L2415  T=0 F=6  T=33 F=0  if (ctxt->dictNames) {
  d=3   L2420  T=0 F=0  T=33 F=0  if (fullname != NULL) {
  d=3   L2428  T=6 F=0  T=0 F=0  if (lname != NULL) {
  d=3   L2446  T=12 F=0  T=0 F=66  if ((ctxt->validate) &&
  d=3   L2447  T=6 F=6  T=0 F=0  ((ctxt->vctxt.flags & XML_VCTXT_DTD_VALIDATED) == 0)) {
  d=3   L2451  T=0 F=6  T=0 F=0  if (chk <= 0)
  d=3   L2453  T=0 F=6  T=0 F=0  if (chk < 0)
--- d=2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=2   L1105  T=0 F=12  T=0 F=6  if (ctxt->html) {
  d=2   L1114  T=12 F=0  T=6 F=0  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1114  T=0 F=12  T=0 F=6  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1131  T=0 F=12  T=0 F=6  if (name == NULL) {
  d=2   L1139  T=0 F=12  T=0 F=6  if ((ctxt->html) &&
  d=2   L1156  T=0 F=12  T=0 F=6  if (ctxt->vctxt.valid != 1) {
  d=2   L1159  T=0 F=12  T=0 F=6  if (nval != NULL)
  d=2   L1169  T=10 F=2  T=0 F=6  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1169  T=12 F=0  T=6 F=0  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1170  T=10 F=0  T=0 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1170  T=10 F=0  T=0 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1170  T=10 F=0  T=0 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1171  T=10 F=0  T=0 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
  d=2   L1171  T=10 F=0  T=0 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
  d=2   L1171  T=10 F=0  T=0 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
  d=2   L1178  T=0 F=10  T=0 F=0  if (!ctxt->replaceEntities) {
  d=2   L1195  T=10 F=0  T=0 F=0  if (val[0] != 0) {
  d=2   L1199  T=0 F=10  T=0 F=0  if (uri == NULL) {
  d=2   L1204  T=0 F=10  T=0 F=0  if (uri->scheme == NULL) {
  d=2   L1221  T=10 F=0  T=0 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1221  T=0 F=10  T=0 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1221  T=10 F=0  T=0 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1226  T=10 F=0  T=0 F=0  if (name != NULL)
  d=2   L1228  T=0 F=10  T=0 F=0  if (nval != NULL)
  d=2   L1230  T=0 F=10  T=0 F=0  if (val != value)
  d=2   L1234  T=2 F=0  T=6 F=0  if ((!ctxt->html) &&
  d=2   L1235  T=0 F=2  T=0 F=6  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=2 F=0  T=6 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=2 F=0  T=6 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1303  T=2 F=0  T=6 F=0  if (ns != NULL) {
  d=2   L1306  T=2 F=0  T=6 F=0  if (namespace == NULL) {
  d=2   L1338  T=0 F=2  T=0 F=6  if (ret == NULL)
  d=2   L1341  T=0 F=2  T=0 F=6  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1352  T=2 F=0  T=6 F=0  } else if (value != NULL) {
  d=2   L1355  T=2 F=0  T=6 F=0  if (ret->children != NULL)
  d=2   L1360  T=2 F=0  T=2 F=4  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1360  T=2 F=0  T=6 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1403  T=2 F=0  T=6 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=2   L1404  T=0 F=2  T=0 F=6  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=2   L1405  T=2 F=0  T=6 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1405  T=2 F=0  T=6 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1407  T=2 F=0  T=6 F=0  (ret->children != NULL) &&
  d=2   L1408  T=2 F=0  T=6 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=2   L1409  T=2 F=0  T=6 F=0  (ret->children->next == NULL)) {
  d=2   L1415  T=0 F=2  T=0 F=6  if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
  d=2   L1427  T=0 F=2  T=0 F=6  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
  d=2   L1429  T=0 F=2  T=0 F=6  else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
  d=2   L1434  T=0 F=2  T=0 F=6  if (nval != NULL)
  d=2   L1436  T=2 F=0  T=6 F=0  if (ns != NULL)
--- d=2  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199) ---
  d=2   L2004  T=0 F=6  T=0 F=33  if (prefix != NULL)
  d=2   L2010  T=0 F=6  T=0 F=33  if (ctxt->freeAttrs != NULL) {
  d=2   L2040  T=0 F=6  T=33 F=0  if (ctxt->dictNames)
  d=2   L2045  T=0 F=6  T=0 F=33  if (ret == NULL) {
  d=2   L2051  T=6 F=0  T=6 F=27  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L2059  T=6 F=0  T=3 F=3  if (*valueend != 0) {
  d=2   L2063  T=6 F=0  T=3 F=0  if (tmp != NULL) {
  d=2   L2071  T=0 F=0  T=3 F=3  while (tmp != NULL) {
  d=2   L2074  T=0 F=0  T=3 F=0  if (tmp->next == NULL)
  d=2   L2079  T=0 F=0  T=27 F=0  } else if (value != NULL) {
  d=2   L2085  T=0 F=0  T=27 F=0  if (tmp != NULL) {
  d=2   L2092  T=6 F=0  T=33 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L2092  T=6 F=0  T=0 F=33  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L2092  T=0 F=6  T=0 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L2161  T=6 F=0  T=33 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=2   L2162  T=6 F=0  T=6 F=27  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=2   L2163  T=0 F=0  T=27 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L2163  T=0 F=0  T=27 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L2165  T=6 F=0  T=33 F=0  (ret->children != NULL) &&
  d=2   L2166  T=6 F=0  T=33 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=2   L2167  T=6 F=0  T=33 F=0  (ret->children->next == NULL)) {
  d=2   L2173  T=0 F=6  T=0 F=33  if ((prefix == ctxt->str_xml) &&
  d=2   L2191  T=0 F=6  T=0 F=33  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret)) {
  d=2   L2193  T=0 F=6  T=0 F=33  } else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret)) {
  d=2   L2197  T=0 F=6  T=0 F=33  if (dup != NULL)
--- d=1  xmlIsID  (/src/libxml2/valid.c:2767-2816) ---
  d=1   L2768  T=0 F=8  T=0 F=39  if ((attr == NULL) || (attr->name == NULL)) return(0);
  d=1   L2768  T=0 F=8  T=0 F=39  if ((attr == NULL) || (attr->name == NULL)) return(0);
  d=1   L2769  T=0 F=8  T=0 F=39  if ((attr->ns != NULL) && (attr->ns->prefix != NULL) &&
  d=1   L2773  T=0 F=8  T=0 F=39  if (doc == NULL) return(0);
  d=1   L2774  T=0 F=8  T=0 F=39  if ((doc->intSubset == NULL) && (doc->extSubset == NULL) &&
  d=1   L2777  T=0 F=8  T=0 F=39  } else if (doc->type == XML_HTML_DOCUMENT_NODE) {
  d=1   L2783  T=0 F=8  T=0 F=39  } else if (elem == NULL) {
  d=1   L2791  T=0 F=8  T=0 F=0  fullelemname = (elem->ns != NULL && elem->ns->prefix != N...  <-- BLOCKER
  d=1   L2791  T=8 F=0  T=0 F=39  fullelemname = (elem->ns != NULL && elem->ns->prefix != N...  <-- BLOCKER
  d=1   L2795  T=0 F=8  T=0 F=39  fullattrname = (attr->ns != NULL && attr->ns->prefix != N...
  d=1   L2799  T=8 F=0  T=39 F=0  if (fullelemname != NULL && fullattrname != NULL) {
  d=1   L2799  T=8 F=0  T=39 F=0  if (fullelemname != NULL && fullattrname != NULL) {
  d=1   L2802  T=8 F=0  T=39 F=0  if ((attrDecl == NULL) && (doc->extSubset != NULL))
  d=1   L2802  T=8 F=0  T=11 F=28  if ((attrDecl == NULL) && (doc->extSubset != NULL))
  d=1   L2807  T=0 F=8  T=0 F=39  if ((fullattrname != fattr) && (fullattrname != attr->name))
  d=1   L2807  T=8 F=0  T=39 F=0  if ((fullattrname != fattr) && (fullattrname != attr->name))
  d=1   L2809  T=8 F=0  T=39 F=0  if ((fullelemname != felem) && (fullelemname != elem->name))
  d=1   L2809  T=0 F=8  T=0 F=39  if ((fullelemname != felem) && (fullelemname != elem->name))
  d=1   L2812  T=0 F=8  T=6 F=33  if ((attrDecl != NULL) && (attrDecl->atype == XML_ATTRIBU...
  d=1   L2812  T=0 F=0  T=0 F=6  if ((attrDecl != NULL) && (attrDecl->atype == XML_ATTRIBU...

[off-chain: 538 additional divergent branches across 72 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=ed9377be9621bf39, size=189 bytes, fuzzer=grimoire, trial=1, discovered_at=1816s, mutation_op=GrimoireExtensionMutator):
  0000: 55 54 46 38 06 00 5c 0a 3c 3f 6c 20 3f 3e 3c 21   UTF8..\.<?l ?><!
  0010: 44 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d 20   DOCTYPEa SYSTEM 
  0020: 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64   "dtds/127772.dtd
  0030: 22 3e 3c 61 3e 20 3c 62 20 6b 3a 66 3d 22 22 3e   "><a> <b k:f="">
Seed 2 (id=f953abe6839324e8, size=234 bytes, fuzzer=grimoire, trial=1, discovered_at=6863s, mutation_op=ByteInterestingMutator,ByteNegMutator):
  0000: 55 54 46 38 06 00 37 37 32 2e 78 6d 6c 5c 0a 3c   UTF8..772.xml\.<
  0010: 3f 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20   ?l ?><!DOCTYPEa 
  0020: 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37   SYSTEM "dtds/127
  0030: 37 37 32 2e 64 74 64 22 3e 3c 61 3e 0a 20 20 3c   772.dtd"><a>.  <
Seed 3 (id=c23096ec9dae2ed4, size=389 bytes, fuzzer=grimoire, trial=1, discovered_at=18912s, mutation_op=ByteNegMutator,BytesExpandMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=05a2233124360cc9, size=299 bytes, fuzzer=cmplog, trial=1, discovered_at=22s, mutation_op=BytesExpandMutator,TokenReplace,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2c 78 6d 6c 5c 0a   ....127772,xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 6b 6b   a SYSTEM "dtdskk
Seed 2 (id=0a4e2c0f734ba9de, size=400 bytes, fuzzer=cmplog, trial=1, discovered_at=454s, mutation_op=CrossoverReplaceMutator,TokenInsert,BitFlipMutator,BytesRandSetMutator,TokenInsert,BitFlipMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=01f8661e47872c51, size=437 bytes, fuzzer=cmplog, trial=1, discovered_at=1510s, mutation_op=CrossoverInsertMutator,ByteInterestingMutator):
  0000: 65 65 65 65 65 54 54 4c 49 53 54 20 62 20 78 6d   eeeeeTTLIST b xm
  0010: 6c 6e 73 3a 78 6c 69 6e 6b 28 2a 43 44 41 54 41   lns:xlink(*CDATA
  0020: 9f 20 20 20 20 23 06 00 00 00 31 32 37 37 37 32   .    #....127772
  0030: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
Seed 4 (id=01ce8fc7df8498a7, size=389 bytes, fuzzer=cmplog, trial=1, discovered_at=4075s, mutation_op=TokenReplace,CrossoverInsertMutator,BytesCopyMutator,ByteDecMutator,ByteAddMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 47 3e 0a 3c   ersion="1.0"G>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE
  0030: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
Seed 5 (id=047fe13ea3b05010, size=386 bytes, fuzzer=cmplog, trial=1, discovered_at=4456s, mutation_op=WordAddMutator,BytesDeleteMutator,CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 3b 31   a SYSTEM "dtds;1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  55(U)x2 37(7)x1                     06(.)x5 65(e)x1 37(7)x1 05(.)x1 +2u  PARTIAL
   0x0001  54(T)x2 32(2)x1                     00(.)x6 65(e)x1 37(7)x1 e5(.)x1 +1u  DIFFER
   0x0002  46(F)x2 2e(.)x1                     00(.)x7 65(e)x1 32(2)x1 3d(=)x1     DIFFER
   0x0003  38(8)x2 78(x)x1                     00(.)x7 65(e)x1 2e(.)x1 22(")x1     DIFFER
   0x0004  06(.)x2 6d(m)x1                     31(1)x6 65(e)x1 78(x)x1 2f(/)x1 +1u  DIFFER
   0x0005  00(.)x2 6c(l)x1                     32(2)x6 54(T)x1 6d(m)x1 2d(-)x1 +1u  DIFFER
   0x0006  5c(\)x2 37(7)x1                     37(7)x6 54(T)x1 6c(l)x1 02(.)x1 +1u  PARTIAL
   0x0007  0a(.)x2 37(7)x1                     37(7)x6 4c(L)x1 5c(\)x1 02(.)x1 +1u  PARTIAL
   0x0008  3c(<)x2 32(2)x1                     37(7)x7 49(I)x1 0a(.)x1 3a(:)x1     DIFFER
   0x0009  3f(?)x2 2e(.)x1                     32(2)x7 53(S)x1 3c(<)x1 2f(/)x1     DIFFER
   0x000a  78(x)x2 6c(l)x1                     2e(.)x5 2c(,)x2 54(T)x1 3f(?)x1 +1u  DIFFER
   0x000b  6d(m)x2 20( )x1                     78(x)x8 20( )x1 66(f)x1             PARTIAL
   0x000c  6c(l)x2 3f(?)x1                     6d(m)x8 62(b)x1 61(a)x1             DIFFER
   0x000d  3e(>)x1 5c(\)x1 20( )x1             6c(l)x8 20( )x1 6b(k)x1             PARTIAL
   0x000e  3c(<)x1 0a(.)x1 76(v)x1             5c(\)x7 78(x)x1 20( )x1 65(e)x1     DIFFER
   0x000f  21(!)x1 3c(<)x1 65(e)x1             0a(.)x7 6d(m)x1 76(v)x1 75(u)x1     DIFFER
   0x0010  44(D)x1 3f(?)x1 72(r)x1             3c(<)x7 6c(l)x1 65(e)x1 10(.)x1     DIFFER
   0x0011  4f(O)x1 6c(l)x1 73(s)x1             3f(?)x7 6e(n)x1 72(r)x1 10(.)x1     DIFFER
   0x0012  43(C)x1 20( )x1 69(i)x1             78(x)x7 73(s)x2 10(.)x1             DIFFER
   0x0013  54(T)x1 3f(?)x1 6f(o)x1             6d(m)x7 3a(:)x1 69(i)x1 04(.)x1     DIFFER
   0x0014  59(Y)x1 3e(>)x1 6e(n)x1             6c(l)x7 78(x)x1 6f(o)x1 10(.)x1     DIFFER
   0x0015  50(P)x1 3c(<)x1 3d(=)x1             20( )x7 6c(l)x1 6e(n)x1 21(!)x1     DIFFER
   0x0016  45(E)x1 21(!)x1 22(")x1             76(v)x7 69(i)x1 3d(=)x1 3e(>)x1     DIFFER
   0x0017  61(a)x1 44(D)x1 31(1)x1             65(e)x7 6e(n)x1 22(")x1 0a(.)x1     DIFFER
   0x0018  20( )x1 4f(O)x1 2e(.)x1             72(r)x7 6b(k)x1 31(1)x1 0a(.)x1     DIFFER
   0x0019  53(S)x1 43(C)x1 30(0)x1             73(s)x7 28(()x1 2e(.)x1 5c(\)x1     DIFFER
   0x001a  59(Y)x1 54(T)x1 22(")x1             69(i)x7 2a(*)x1 30(0)x1 5c(\)x1     DIFFER
   0x001b  53(S)x1 59(Y)x1 3f(?)x1             6f(o)x7 43(C)x1 22(")x1 64(d)x1     DIFFER
   0x001c  54(T)x1 50(P)x1 3e(>)x1             6e(n)x7 44(D)x1 47(G)x1 74(t)x1     DIFFER
   0x001d  45(E)x2 0a(.)x1                     3d(=)x7 41(A)x1 3e(>)x1 64(d)x1     DIFFER
   0x001e  4d(M)x1 61(a)x1 3c(<)x1             22(")x7 54(T)x1 0a(.)x1 ff(.)x1     DIFFER
   0x001f  20( )x2 21(!)x1                     31(1)x7 41(A)x1 3c(<)x1 21(!)x1     PARTIAL
   0x0020  22(")x1 53(S)x1 44(D)x1             2e(.)x7 9f(.)x1 21(!)x1 31(1)x1     DIFFER
   0x0021  64(d)x1 59(Y)x1 4f(O)x1             30(0)x7 20( )x1 44(D)x1 32(2)x1     DIFFER
   0x0022  74(t)x1 53(S)x1 43(C)x1             22(")x7 20( )x1 4f(O)x1 37(7)x1     DIFFER
   0x0023  54(T)x2 64(d)x1                     3f(?)x7 20( )x1 43(C)x1 28(()x1     DIFFER
   0x0024  73(s)x1 45(E)x1 59(Y)x1             3e(>)x7 20( )x1 54(T)x1 2b(+)x1     DIFFER
   0x0025  2f(/)x1 4d(M)x1 50(P)x1             0a(.)x7 23(#)x1 59(Y)x1 2a(*)x1     DIFFER
   0x0026  31(1)x1 20( )x1 45(E)x1             3c(<)x7 06(.)x1 50(P)x1 21(!)x1     DIFFER
   0x0027  32(2)x1 22(")x1 20( )x1             21(!)x8 00(.)x1 45(E)x1             DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7105.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7105,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7105 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7105 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7105 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).