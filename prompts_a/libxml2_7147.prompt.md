==== BLOCKER ====
Target: libxml2
Branch ID: 7147
Location: /src/libxml2/valid.c:4071:9
Enclosing function: xmlValidCtxtNormalizeAttributeValue
Source line:     if ((elem->ns != NULL) && (elem->ns->prefix != NULL)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        3        7          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.40h  loser=20.00h
  avg hitcount on branch: winner=414  loser=1
  prob_div=0.60  dur_div=8.60h  hit_div=413
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7147/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlValidCtxtNormalizeAttributeValue (/src/libxml2/valid.c:4061-4111) ---
[ ]  4059  xmlChar *
[ ]  4060  xmlValidCtxtNormalizeAttributeValue(xmlValidCtxtPtr ctxt, xmlDocPtr doc,
[B]  4061  	     xmlNodePtr elem, const xmlChar *name, const xmlChar *value) {
[B]  4062      xmlChar *ret;
[B]  4063      xmlAttributePtr attrDecl = NULL;
[B]  4064      int extsubset = 0;
[ ]  4065  
[B]  4066      if (doc == NULL) return(NULL);
[B]  4067      if (elem == NULL) return(NULL);
[B]  4068      if (name == NULL) return(NULL);
[B]  4069      if (value == NULL) return(NULL);
[ ]  4070  
[B]  4071      if ((elem->ns != NULL) && (elem->ns->prefix != NULL)) { <-- BLOCKER
[ ]  4072  	xmlChar fn[50];
[ ]  4073  	xmlChar *fullname;
[ ]  4074  
[ ]  4075  	fullname = xmlBuildQName(elem->name, elem->ns->prefix, fn, 50);
[ ]  4076  	if (fullname == NULL)
[ ]  4077  	    return(NULL);
[ ]  4078  	attrDecl = xmlGetDtdAttrDesc(doc->intSubset, fullname, name);
[ ]  4079  	if ((attrDecl == NULL) && (doc->extSubset != NULL)) {
[ ]  4080  	    attrDecl = xmlGetDtdAttrDesc(doc->extSubset, fullname, name);
[ ]  4081  	    if (attrDecl != NULL)
[ ]  4082  		extsubset = 1;
[ ]  4083  	}
[ ]  4084  	if ((fullname != fn) && (fullname != elem->name))
[ ]  4085  	    xmlFree(fullname);
[ ]  4086      }
[B]  4087      if ((attrDecl == NULL) && (doc->intSubset != NULL))
[B]  4088  	attrDecl = xmlGetDtdAttrDesc(doc->intSubset, elem->name, name);
[B]  4089      if ((attrDecl == NULL) && (doc->extSubset != NULL)) {
[B]  4090  	attrDecl = xmlGetDtdAttrDesc(doc->extSubset, elem->name, name);
[B]  4091  	if (attrDecl != NULL)
[W]  4092  	    extsubset = 1;
[B]  4093      }
[ ]  4094  
[B]  4095      if (attrDecl == NULL)
[B]  4096  	return(NULL);
[W]  4097      if (attrDecl->atype == XML_ATTRIBUTE_CDATA)
[W]  4098  	return(NULL);
[ ]  4099  
[ ]  4100      ret = xmlStrdup(value);
[ ]  4101      if (ret == NULL)
[ ]  4102  	return(NULL);
[ ]  4103      xmlValidNormalizeString(ret);
[ ]  4104      if ((doc->standalone) && (extsubset == 1) && (!xmlStrEqual(value, ret))) {
[ ]  4105  	xmlErrValidNode(ctxt, elem, XML_DTD_NOT_STANDALONE,
[ ]  4106  "standalone: %s on %s value had to be normalized based on external subset declaration\n",
[ ]  4107  	       name, elem->name, NULL);
[ ]  4108  	ctxt->valid = 0;
[ ]  4109      }
[ ]  4110      return(ret);
[ ]  4111  }

--- Caller (1 hop): SAX2.c:xmlSAX2AttributeInternal (/src/libxml2/SAX2.c:1097-1438, calls xmlValidCtxtNormalizeAttributeValue at line 1153) (±10 around call site) ---
[ ]  1143      } else
[B]  1144  #endif
[B]  1145      {
[B]  1146  #ifdef LIBXML_VALID_ENABLED
[ ]  1147          /*
[ ]  1148           * Do the last stage of the attribute normalization
[ ]  1149           * Needed for HTML too:
[ ]  1150           *   http://www.w3.org/TR/html4/types.html#h-6.2
[ ]  1151           */
[B]  1152          ctxt->vctxt.valid = 1;
[B]  1153          nval = xmlValidCtxtNormalizeAttributeValue(&ctxt->vctxt, <-- CALL
[B]  1154                                                 ctxt->myDoc, ctxt->node,
[B]  1155                                                 fullname, value);
[B]  1156          if (ctxt->vctxt.valid != 1) {
[ ]  1157              ctxt->valid = 0;
[ ]  1158          }
[B]  1159          if (nval != NULL)
[ ]  1160              value = nval;
[ ]  1161  #else
[ ]  1162          nval = NULL;
[ ]  1163  #endif /* LIBXML_VALID_ENABLED */

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438, calls xmlValidCtxtNormalizeAttributeValue at line 1153)
hop 2  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199, calls xmlValidCtxtNormalizeAttributeValue at line 2131)
hop 3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)
hop 3  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459, calls SAX2.c:xmlSAX2AttributeNs at line 2421)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      30       272  xmlGetDtdQElementDesc  (/src/libxml2/valid.c:3349-3357)
      15       157  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806)
      15       136  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591)
      15       113  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      15       113  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
       0        75  xmlSAX2IgnorableWhitespace  (/src/libxml2/SAX2.c:2698-2704)
       0        75  xmlIsMixedElement  (/src/libxml2/valid.c:3487-3511)
      12        79  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
      15        76  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
       4        40  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
       2        33  xmlIsID  (/src/libxml2/valid.c:2767-2816)
       2        33  xmlIsRef  (/src/libxml2/valid.c:3115-3143)
       2        30  SAX2.c:xmlNsErrMsg  (/src/libxml2/SAX2.c:1070-1080)
       3        30  xmlSAX2SetDocumentLocator  (/src/libxml2/SAX2.c:942-948)
       3        30  xmlSAX2StartDocument  (/src/libxml2/SAX2.c:958-1013)
... (22 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591) ---
  d=3   L1454  T=15 F=0  T=136 F=0  if (elemDecl == NULL) {
  d=3   L1461  T=15 F=0  T=2 F=134  if (elemDecl != NULL) {
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
  d=3   L1614  T=0 F=15  T=0 F=157  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=3   L1614  T=0 F=15  T=0 F=157  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=3   L1614  T=0 F=15  T=0 F=157  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=3   L1624  T=15 F=0  T=23 F=134  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L1624  T=0 F=15  T=19 F=4  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L1625  T=0 F=0  T=6 F=13  ((ctxt->myDoc->intSubset == NULL) ||
  d=3   L1626  T=0 F=0  T=13 F=0  ((ctxt->myDoc->intSubset->notations == NULL) &&
  d=3   L1627  T=0 F=0  T=13 F=0  (ctxt->myDoc->intSubset->elements == NULL) &&
  d=3   L1628  T=0 F=0  T=13 F=0  (ctxt->myDoc->intSubset->attributes == NULL) &&
  d=3   L1629  T=0 F=0  T=13 F=0  (ctxt->myDoc->intSubset->entities == NULL)))) {
  d=3   L1648  T=0 F=15  T=0 F=157  if (ret == NULL) {
  d=3   L1654  T=0 F=15  T=12 F=145  if (ctxt->myDoc->children == NULL) {
  d=3   L1659  T=3 F=12  T=22 F=123  } else if (parent == NULL) {
  d=3   L1663  T=15 F=0  T=157 F=0  if (ctxt->linenumbers) {
  d=3   L1664  T=15 F=0  T=157 F=0  if (ctxt->input != NULL) {
  d=3   L1665  T=15 F=0  T=157 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=3   L1678  T=0 F=15  T=0 F=157  if (nodePush(ctxt, ret) < 0) {
  d=3   L1689  T=15 F=0  T=145 F=12  if (parent != NULL) {
  d=3   L1690  T=12 F=3  T=127 F=18  if (parent->type == XML_ELEMENT_NODE) {
  d=3   L1706  T=15 F=0  T=157 F=0  if (!ctxt->html) {
  d=3   L1711  T=15 F=0  T=136 F=21  if ((ctxt->myDoc->intSubset != NULL) ||
  d=3   L1712  T=0 F=0  T=0 F=21  (ctxt->myDoc->extSubset != NULL)) {
  d=3   L1719  T=2 F=13  T=33 F=124  if (atts != NULL) {
  d=3   L1723  T=2 F=0  T=33 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1723  T=2 F=2  T=33 F=33  while ((att != NULL) && (value != NULL)) {
  d=3   L1724  T=0 F=0  T=0 F=3  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1724  T=0 F=2  T=3 F=24  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1724  T=2 F=0  T=27 F=6  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1738  T=5 F=0  T=145 F=12  if ((ns == NULL) && (parent != NULL))
  d=3   L1738  T=5 F=10  T=157 F=0  if ((ns == NULL) && (parent != NULL))
  d=3   L1740  T=0 F=15  T=0 F=157  if ((prefix != NULL) && (ns == NULL)) {
  d=3   L1751  T=10 F=5  T=0 F=157  if ((ns != NULL) && (ns->href != NULL) &&
  d=3   L1751  T=10 F=0  T=0 F=0  if ((ns != NULL) && (ns->href != NULL) &&
  d=3   L1752  T=10 F=0  T=0 F=0  ((ns->href[0] != 0) || (ns->prefix != NULL)))
  d=3   L1759  T=2 F=13  T=33 F=124  if (atts != NULL) {
  d=3   L1763  T=0 F=2  T=0 F=33  if (ctxt->html) {
  d=3   L1770  T=2 F=2  T=33 F=33  while ((att != NULL) && (value != NULL)) {
  d=3   L1770  T=2 F=0  T=33 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1771  T=0 F=0  T=3 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1771  T=2 F=0  T=24 F=3  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1771  T=0 F=2  T=6 F=27  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1789  T=15 F=0  T=4 F=153  if ((ctxt->validate) &&
  d=3   L1790  T=3 F=12  T=2 F=2  ((ctxt->vctxt.flags & XML_VCTXT_DTD_VALIDATED) == 0)) {
  d=3   L1803  T=0 F=15  T=0 F=157  if (prefix != NULL)
--- d=2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=2   L1105  T=0 F=12  T=0 F=33  if (ctxt->html) {
  d=2   L1114  T=12 F=0  T=33 F=0  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1114  T=0 F=12  T=0 F=33  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1131  T=0 F=12  T=0 F=33  if (name == NULL) {
  d=2   L1139  T=0 F=12  T=0 F=33  if ((ctxt->html) &&
  d=2   L1156  T=0 F=12  T=0 F=33  if (ctxt->vctxt.valid != 1) {
  d=2   L1159  T=0 F=12  T=0 F=33  if (nval != NULL)
  d=2   L1169  T=10 F=2  T=3 F=30  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1169  T=12 F=0  T=33 F=0  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1170  T=10 F=0  T=0 F=3  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
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
  d=2   L1234  T=2 F=0  T=33 F=0  if ((!ctxt->html) &&
  d=2   L1235  T=0 F=2  T=3 F=24  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=0 F=0  T=0 F=3  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=2 F=0  T=30 F=3  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=2 F=0  T=27 F=3  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1303  T=2 F=0  T=30 F=3  if (ns != NULL) {
  d=2   L1306  T=2 F=0  T=30 F=0  if (namespace == NULL) {
  d=2   L1338  T=0 F=2  T=0 F=33  if (ret == NULL)
  d=2   L1341  T=0 F=0  T=8 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1341  T=0 F=2  T=8 F=25  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1346  T=0 F=0  T=8 F=8  while (tmp != NULL) {
  d=2   L1348  T=0 F=0  T=8 F=0  if (tmp->next == NULL)
  d=2   L1352  T=2 F=0  T=25 F=0  } else if (value != NULL) {
  d=2   L1355  T=2 F=0  T=25 F=0  if (ret->children != NULL)
  d=2   L1360  T=2 F=0  T=2 F=31  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1360  T=2 F=0  T=33 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1403  T=2 F=0  T=33 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=2   L1404  T=0 F=2  T=8 F=25  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=2   L1404  T=0 F=0  T=8 F=0  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=2   L1405  T=2 F=0  T=25 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1405  T=2 F=0  T=25 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1407  T=2 F=0  T=33 F=0  (ret->children != NULL) &&
  d=2   L1408  T=2 F=0  T=33 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=2   L1409  T=2 F=0  T=33 F=0  (ret->children->next == NULL)) {
  d=2   L1415  T=0 F=2  T=0 F=33  if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
  d=2   L1427  T=0 F=2  T=0 F=33  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
  d=2   L1429  T=0 F=2  T=0 F=33  else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
  d=2   L1434  T=0 F=2  T=0 F=33  if (nval != NULL)
  d=2   L1436  T=2 F=0  T=30 F=3  if (ns != NULL)
--- d=1  xmlValidCtxtNormalizeAttributeValue  (/src/libxml2/valid.c:4061-4111) ---
  d=1   L4066  T=0 F=12  T=0 F=33  if (doc == NULL) return(NULL);
  d=1   L4067  T=0 F=12  T=0 F=33  if (elem == NULL) return(NULL);
  d=1   L4068  T=0 F=12  T=0 F=33  if (name == NULL) return(NULL);
  d=1   L4069  T=0 F=12  T=0 F=33  if (value == NULL) return(NULL);
  d=1   L4071  T=2 F=10  T=0 F=33  if ((elem->ns != NULL) && (elem->ns->prefix != NULL)) {  <-- BLOCKER
  d=1   L4071  T=0 F=2  T=0 F=0  if ((elem->ns != NULL) && (elem->ns->prefix != NULL)) {  <-- BLOCKER
  d=1   L4087  T=12 F=0  T=33 F=0  if ((attrDecl == NULL) && (doc->intSubset != NULL))
  d=1   L4087  T=12 F=0  T=20 F=13  if ((attrDecl == NULL) && (doc->intSubset != NULL))
  d=1   L4089  T=12 F=0  T=2 F=31  if ((attrDecl == NULL) && (doc->extSubset != NULL)) {
  d=1   L4089  T=12 F=0  T=33 F=0  if ((attrDecl == NULL) && (doc->extSubset != NULL)) {
  d=1   L4091  T=10 F=2  T=0 F=2  if (attrDecl != NULL)
  d=1   L4095  T=2 F=10  T=33 F=0  if (attrDecl == NULL)
  d=1   L4097  T=10 F=0  T=0 F=0  if (attrDecl->atype == XML_ATTRIBUTE_CDATA)

[off-chain: 299 additional divergent branches across 31 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c23096ec9dae2ed4, size=389 bytes, fuzzer=grimoire, trial=1, discovered_at=18912s, mutation_op=ByteNegMutator,BytesExpandMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0daca46eaa46b0ce, size=365 bytes, fuzzer=cmplog, trial=1, discovered_at=271s, mutation_op=TokenInsert,BitFlipMutator,BytesDeleteMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c   ersion="1.0"?>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE
  0030: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
Seed 2 (id=178c744c44296e51, size=372 bytes, fuzzer=cmplog, trial=1, discovered_at=587s, mutation_op=BytesSetMutator,TokenInsert):
  0000: 43 43 43 43 43 32 37 37 37 32 3d 00 6d 6c 5c 0a   CCCCC27772=.ml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c ff 44 4f 43 54 59 5c 45 20   .0"?>.<.DOCTY\E 
  0030: 61 20 22 59 53 54 45 ff 20 22 64 74 64 73 2f 31   a "YSTE. "dtds/1
Seed 3 (id=0f2b34c03deabc2a, size=496 bytes, fuzzer=cmplog, trial=1, discovered_at=1023s, mutation_op=CrossoverReplaceMutator,BytesDeleteMutator,WordAddMutator):
  0000: 45 4e 54 20 62 20 28 23 50 43 44 41 54 41 29 3e   ENT b (#PCDATA)>
  0010: 0a 3c 21 41 54 54 4c 49 53 54 20 62 20 78 6d 6c   .<!ATTLIST b xml
  0020: 6e 73 3a 78 6c 69 6e 6b 2a 29 43 44 41 54 41 20   ns:xlink*)CDATA 
  0030: 20 20 20 20 23 46 49 58 45 44 20 27 68 74 74 70       #FIXED 'http
Seed 4 (id=089cc2e922e50276, size=360 bytes, fuzzer=cmplog, trial=1, discovered_at=3014s, mutation_op=ByteIncMutator,BytesSwapMutator,DwordAddMutator,ByteNegMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 0d 22 31 2e 30 22 3f 3f 0a 3c 21   rsion."1.0"??.<!
  0020: 44 4f 43 54 59 50 45 20 61 31 32 37 37 37 32 2e   DOCTYPE a127772.
  0030: 64 74 64 22 3e 0a 0a 3c 61 3e 0a 20 20 3c 62 20   dtd">..<a>.  <b 
Seed 5 (id=01ce8fc7df8498a7, size=389 bytes, fuzzer=cmplog, trial=1, discovered_at=4075s, mutation_op=TokenReplace,CrossoverInsertMutator,BytesCopyMutator,ByteDecMutator,ByteAddMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 47 3e 0a 3c   ersion="1.0"G>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE
  0030: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  37(7)x1                             37(7)x4 43(C)x1 45(E)x1 27(')x1 +3u  PARTIAL
   0x0001  32(2)x1                             37(7)x3 32(2)x2 43(C)x1 4e(N)x1 +3u  PARTIAL
   0x0002  2e(.)x1                             32(2)x2 37(7)x2 43(C)x1 54(T)x1 +4u  PARTIAL
   0x0003  78(x)x1                             2e(.)x2 43(C)x1 20( )x1 78(x)x1 +5u  PARTIAL
   0x0004  6d(m)x1                             78(x)x2 43(C)x1 62(b)x1 6d(m)x1 +5u  PARTIAL
   0x0005  6c(l)x1                             6d(m)x2 32(2)x2 20( )x1 6c(l)x1 +4u  PARTIAL
   0x0006  5c(\)x1                             6c(l)x2 2f(/)x2 37(7)x1 28(()x1 +4u  PARTIAL
   0x0007  0a(.)x1                             5c(\)x2 37(7)x1 23(#)x1 0a(.)x1 +5u  PARTIAL
   0x0008  3c(<)x1                             0a(.)x2 37(7)x1 50(P)x1 3c(<)x1 +5u  PARTIAL
   0x0009  3f(?)x1                             3c(<)x2 32(2)x1 43(C)x1 3f(?)x1 +5u  PARTIAL
   0x000a  78(x)x1                             3f(?)x2 3d(=)x1 44(D)x1 78(x)x1 +5u  PARTIAL
   0x000b  6d(m)x1                             78(x)x2 00(.)x2 41(A)x1 6d(m)x1 +4u  PARTIAL
   0x000c  6c(l)x1                             6d(m)x3 54(T)x1 6c(l)x1 77(w)x1 +4u  PARTIAL
   0x000d  20( )x1                             6c(l)x3 00(.)x2 41(A)x1 20( )x1 +3u  PARTIAL
   0x000e  76(v)x1                             20( )x2 5c(\)x1 29())x1 76(v)x1 +5u  PARTIAL
   0x000f  65(e)x1                             76(v)x2 0a(.)x1 3e(>)x1 65(e)x1 +5u  PARTIAL
   0x0010  72(r)x1                             65(e)x2 72(r)x2 3c(<)x1 0a(.)x1 +4u  PARTIAL
   0x0011  73(s)x1                             72(r)x2 3f(?)x1 3c(<)x1 73(s)x1 +5u  PARTIAL
   0x0012  69(i)x1                             73(s)x2 78(x)x2 21(!)x1 69(i)x1 +4u  PARTIAL
   0x0013  6f(o)x1                             69(i)x2 6d(m)x2 41(A)x1 6f(o)x1 +4u  PARTIAL
   0x0014  6e(n)x1                             6f(o)x2 6c(l)x2 54(T)x1 6e(n)x1 +4u  PARTIAL
   0x0015  3d(=)x1                             6e(n)x2 20( )x1 54(T)x1 0d(.)x1 +5u  DIFFER
   0x0016  22(")x1                             3d(=)x2 76(v)x1 4c(L)x1 22(")x1 +5u  PARTIAL
   0x0017  31(1)x1                             22(")x2 65(e)x1 49(I)x1 31(1)x1 +5u  PARTIAL
   0x0018  2e(.)x1                             31(1)x2 72(r)x1 53(S)x1 2e(.)x1 +5u  PARTIAL
   0x0019  30(0)x1                             2e(.)x2 73(s)x1 54(T)x1 30(0)x1 +5u  PARTIAL
   0x001a  22(")x1                             30(0)x2 69(i)x2 20( )x1 22(")x1 +4u  PARTIAL
   0x001b  3f(?)x1                             22(")x2 3f(?)x2 6f(o)x1 62(b)x1 +4u  PARTIAL
   0x001c  3e(>)x1                             3f(?)x2 20( )x2 6e(n)x1 47(G)x1 +4u  DIFFER
   0x001d  0a(.)x1                             3e(>)x2 3d(=)x1 78(x)x1 0a(.)x1 +5u  PARTIAL
   0x001e  3c(<)x1                             0a(.)x2 22(")x1 6d(m)x1 3c(<)x1 +5u  PARTIAL
   0x001f  21(!)x1                             3c(<)x2 21(!)x2 20( )x2 31(1)x1 +3u  PARTIAL
   0x0020  44(D)x1                             21(!)x2 2e(.)x1 6e(n)x1 44(D)x1 +5u  PARTIAL
   0x0021  4f(O)x1                             44(D)x2 30(0)x1 73(s)x1 4f(O)x1 +5u  PARTIAL
   0x0022  43(C)x1                             4f(O)x2 22(")x1 3a(:)x1 43(C)x1 +5u  PARTIAL
   0x0023  54(T)x1                             43(C)x2 3f(?)x1 78(x)x1 54(T)x1 +5u  PARTIAL
   0x0024  59(Y)x1                             54(T)x2 3e(>)x1 6c(l)x1 59(Y)x1 +5u  PARTIAL
   0x0025  50(P)x1                             59(Y)x2 0a(.)x1 69(i)x1 50(P)x1 +5u  PARTIAL
   0x0026  45(E)x1                             50(P)x2 6e(n)x2 3c(<)x1 45(E)x1 +4u  PARTIAL
   0x0027  20( )x1                             45(E)x2 20( )x2 ff(.)x1 6b(k)x1 +4u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7147.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7147,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7147 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7147 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7147 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).