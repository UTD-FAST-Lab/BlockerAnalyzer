==== BLOCKER ====
Target: libxml2
Branch ID: 7099
Location: /src/libxml2/valid.c:2143:7
Enclosing function: xmlAddAttributeDecl
Source line: 		   ((xmlStrEqual(tmp->name, BAD_CAST "xmlns")) ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    1        9          0  REFERENCE
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        8          1  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.50h  loser=17.70h
  avg hitcount on branch: winner=76  loser=2
  prob_div=0.80  dur_div=13.20h  hit_div=74
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7099/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlAddAttributeDecl (/src/libxml2/valid.c:1964-2172) ---
[ ]  1962                      const xmlChar *name, const xmlChar *ns,
[ ]  1963  		    xmlAttributeType type, xmlAttributeDefault def,
[B]  1964  		    const xmlChar *defaultValue, xmlEnumerationPtr tree) {
[B]  1965      xmlAttributePtr ret;
[B]  1966      xmlAttributeTablePtr table;
[B]  1967      xmlElementPtr elemDef;
[B]  1968      xmlDictPtr dict = NULL;
[ ]  1969  
[B]  1970      if (dtd == NULL) {
[ ]  1971  	xmlFreeEnumeration(tree);
[ ]  1972  	return(NULL);
[ ]  1973      }
[B]  1974      if (name == NULL) {
[ ]  1975  	xmlFreeEnumeration(tree);
[ ]  1976  	return(NULL);
[ ]  1977      }
[B]  1978      if (elem == NULL) {
[ ]  1979  	xmlFreeEnumeration(tree);
[ ]  1980  	return(NULL);
[ ]  1981      }
[B]  1982      if (dtd->doc != NULL)
[B]  1983  	dict = dtd->doc->dict;
[ ]  1984  
[B]  1985  #ifdef LIBXML_VALID_ENABLED
[ ]  1986      /*
[ ]  1987       * Check the type and possibly the default value.
[ ]  1988       */
[B]  1989      switch (type) {
[B]  1990          case XML_ATTRIBUTE_CDATA:
[B]  1991  	    break;
[ ]  1992          case XML_ATTRIBUTE_ID:
[ ]  1993  	    break;
[ ]  1994          case XML_ATTRIBUTE_IDREF:
[ ]  1995  	    break;
[ ]  1996          case XML_ATTRIBUTE_IDREFS:
[ ]  1997  	    break;
[ ]  1998          case XML_ATTRIBUTE_ENTITY:
[ ]  1999  	    break;
[ ]  2000          case XML_ATTRIBUTE_ENTITIES:
[ ]  2001  	    break;
[ ]  2002          case XML_ATTRIBUTE_NMTOKEN:
[ ]  2003  	    break;
[ ]  2004          case XML_ATTRIBUTE_NMTOKENS:
[ ]  2005  	    break;
[B]  2006          case XML_ATTRIBUTE_ENUMERATION:
[B]  2007  	    break;
[ ]  2008          case XML_ATTRIBUTE_NOTATION:
[ ]  2009  	    break;
[ ]  2010  	default:
[ ]  2011  	    xmlErrValid(ctxt, XML_ERR_INTERNAL_ERROR,
[ ]  2012  		    "Internal: ATTRIBUTE struct corrupted invalid type\n",
[ ]  2013  		    NULL);
[ ]  2014  	    xmlFreeEnumeration(tree);
[ ]  2015  	    return(NULL);
[B]  2016      }
[B]  2017      if ((defaultValue != NULL) &&
[B]  2018          (!xmlValidateAttributeValueInternal(dtd->doc, type, defaultValue))) {
[W]  2019  	xmlErrValidNode(ctxt, (xmlNodePtr) dtd, XML_DTD_ATTRIBUTE_DEFAULT,
[W]  2020  	                "Attribute %s of %s: invalid default value\n",
[W]  2021  	                elem, name, defaultValue);
[W]  2022  	defaultValue = NULL;
[W]  2023  	if (ctxt != NULL)
[W]  2024  	    ctxt->valid = 0;
[W]  2025      }
[B]  2026  #endif /* LIBXML_VALID_ENABLED */
[ ]  2027  
[ ]  2028      /*
[ ]  2029       * Check first that an attribute defined in the external subset wasn't
[ ]  2030       * already defined in the internal subset
[ ]  2031       */
[B]  2032      if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
[B]  2033  	(dtd->doc->intSubset != NULL) &&
[B]  2034  	(dtd->doc->intSubset->attributes != NULL)) {
[ ]  2035          ret = xmlHashLookup3(dtd->doc->intSubset->attributes, name, ns, elem);
[ ]  2036  	if (ret != NULL) {
[ ]  2037  	    xmlFreeEnumeration(tree);
[ ]  2038  	    return(NULL);
[ ]  2039  	}
[ ]  2040      }
[ ]  2041  
[ ]  2042      /*
[ ]  2043       * Create the Attribute table if needed.
[ ]  2044       */
[B]  2045      table = (xmlAttributeTablePtr) dtd->attributes;
[B]  2046      if (table == NULL) {
[B]  2047          table = xmlHashCreateDict(0, dict);
[B]  2048  	dtd->attributes = (void *) table;
[B]  2049      }
[B]  2050      if (table == NULL) {
[ ]  2051  	xmlVErrMemory(ctxt,
[ ]  2052              "xmlAddAttributeDecl: Table creation failed!\n");
[ ]  2053  	xmlFreeEnumeration(tree);
[ ]  2054          return(NULL);
[ ]  2055      }
[ ]  2056  
[ ]  2057  
[B]  2058      ret = (xmlAttributePtr) xmlMalloc(sizeof(xmlAttribute));
[B]  2059      if (ret == NULL) {
[ ]  2060  	xmlVErrMemory(ctxt, "malloc failed");
[ ]  2061  	xmlFreeEnumeration(tree);
[ ]  2062  	return(NULL);
[ ]  2063      }
[B]  2064      memset(ret, 0, sizeof(xmlAttribute));
[B]  2065      ret->type = XML_ATTRIBUTE_DECL;
[ ]  2066  
[ ]  2067      /*
[ ]  2068       * fill the structure.
[ ]  2069       */
[B]  2070      ret->atype = type;
[ ]  2071      /*
[ ]  2072       * doc must be set before possible error causes call
[ ]  2073       * to xmlFreeAttribute (because it's used to check on
[ ]  2074       * dict use)
[ ]  2075       */
[B]  2076      ret->doc = dtd->doc;
[B]  2077      if (dict) {
[L]  2078  	ret->name = xmlDictLookup(dict, name, -1);
[L]  2079  	ret->prefix = xmlDictLookup(dict, ns, -1);
[L]  2080  	ret->elem = xmlDictLookup(dict, elem, -1);
[B]  2081      } else {
[B]  2082  	ret->name = xmlStrdup(name);
[B]  2083  	ret->prefix = xmlStrdup(ns);
[B]  2084  	ret->elem = xmlStrdup(elem);
[B]  2085      }
[B]  2086      ret->def = def;
[B]  2087      ret->tree = tree;
[B]  2088      if (defaultValue != NULL) {
[B]  2089          if (dict)
[L]  2090  	    ret->defaultValue = xmlDictLookup(dict, defaultValue, -1);
[B]  2091  	else
[B]  2092  	    ret->defaultValue = xmlStrdup(defaultValue);
[B]  2093      }
[ ]  2094  
[ ]  2095      /*
[ ]  2096       * Validity Check:
[ ]  2097       * Search the DTD for previous declarations of the ATTLIST
[ ]  2098       */
[B]  2099      if (xmlHashAddEntry3(table, ret->name, ret->prefix, ret->elem, ret) < 0) {
[ ]  2100  #ifdef LIBXML_VALID_ENABLED
[ ]  2101  	/*
[ ]  2102  	 * The attribute is already defined in this DTD.
[ ]  2103  	 */
[ ]  2104  	xmlErrValidWarning(ctxt, (xmlNodePtr) dtd, XML_DTD_ATTRIBUTE_REDEFINED,
[ ]  2105  		 "Attribute %s of element %s: already defined\n",
[ ]  2106  		 name, elem, NULL);
[ ]  2107  #endif /* LIBXML_VALID_ENABLED */
[ ]  2108  	xmlFreeAttribute(ret);
[ ]  2109  	return(NULL);
[ ]  2110      }
[ ]  2111  
[ ]  2112      /*
[ ]  2113       * Validity Check:
[ ]  2114       * Multiple ID per element
[ ]  2115       */
[B]  2116      elemDef = xmlGetDtdElementDesc2(dtd, elem, 1);
[B]  2117      if (elemDef != NULL) {
[ ]  2118  
[B]  2119  #ifdef LIBXML_VALID_ENABLED
[B]  2120          if ((type == XML_ATTRIBUTE_ID) &&
[B]  2121  	    (xmlScanIDAttributeDecl(NULL, elemDef, 1) != 0)) {
[ ]  2122  	    xmlErrValidNode(ctxt, (xmlNodePtr) dtd, XML_DTD_MULTIPLE_ID,
[ ]  2123  	   "Element %s has too may ID attributes defined : %s\n",
[ ]  2124  		   elem, name, NULL);
[ ]  2125  	    if (ctxt != NULL)
[ ]  2126  		ctxt->valid = 0;
[ ]  2127  	}
[B]  2128  #endif /* LIBXML_VALID_ENABLED */
[ ]  2129  
[ ]  2130  	/*
[ ]  2131  	 * Insert namespace default def first they need to be
[ ]  2132  	 * processed first.
[ ]  2133  	 */
[B]  2134  	if ((xmlStrEqual(ret->name, BAD_CAST "xmlns")) ||
[B]  2135  	    ((ret->prefix != NULL &&
[B]  2136  	     (xmlStrEqual(ret->prefix, BAD_CAST "xmlns"))))) {
[B]  2137  	    ret->nexth = elemDef->attributes;
[B]  2138  	    elemDef->attributes = ret;
[B]  2139  	} else {
[B]  2140  	    xmlAttributePtr tmp = elemDef->attributes;
[ ]  2141  
[B]  2142  	    while ((tmp != NULL) &&
[B]  2143  		   ((xmlStrEqual(tmp->name, BAD_CAST "xmlns")) || <-- BLOCKER
[B]  2144  		    ((ret->prefix != NULL &&
[B]  2145  		     (xmlStrEqual(ret->prefix, BAD_CAST "xmlns")))))) {
[B]  2146  		if (tmp->nexth == NULL)
[B]  2147  		    break;
[B]  2148  		tmp = tmp->nexth;
[B]  2149  	    }
[B]  2150  	    if (tmp != NULL) {
[B]  2151  		ret->nexth = tmp->nexth;
[B]  2152  	        tmp->nexth = ret;
[B]  2153  	    } else {
[L]  2154  		ret->nexth = elemDef->attributes;
[L]  2155  		elemDef->attributes = ret;
[L]  2156  	    }
[B]  2157  	}
[B]  2158      }
[ ]  2159  
[ ]  2160      /*
[ ]  2161       * Link it to the DTD
[ ]  2162       */
[B]  2163      ret->parent = dtd;
[B]  2164      if (dtd->last == NULL) {
[ ]  2165  	dtd->children = dtd->last = (xmlNodePtr) ret;
[B]  2166      } else {
[B]  2167          dtd->last->next = (xmlNodePtr) ret;
[B]  2168  	ret->prev = dtd->last;
[B]  2169  	dtd->last = (xmlNodePtr) ret;
[B]  2170      }
[B]  2171      return(ret);
[B]  2172  }

--- Caller (1 hop): xmlSAX2AttributeDecl (/src/libxml2/SAX2.c:701-758, calls xmlAddAttributeDecl at line 735) (±10 around call site) ---
[ ]   725  	ctxt->valid = tmp;
[ ]   726      }
[ ]   727      /* TODO: optimize name/prefix allocation */
[B]   728      name = xmlSplitQName(ctxt, fullname, &prefix);
[B]   729      ctxt->vctxt.valid = 1;
[B]   730      if (ctxt->inSubset == 1)
[ ]   731  	attr = xmlAddAttributeDecl(&ctxt->vctxt, ctxt->myDoc->intSubset, elem,
[ ]   732  	       name, prefix, (xmlAttributeType) type,
[ ]   733  	       (xmlAttributeDefault) def, defaultValue, tree);
[B]   734      else if (ctxt->inSubset == 2)
[B]   735  	attr = xmlAddAttributeDecl(&ctxt->vctxt, ctxt->myDoc->extSubset, elem, <-- CALL
[B]   736  	   name, prefix, (xmlAttributeType) type,
[B]   737  	   (xmlAttributeDefault) def, defaultValue, tree);
[ ]   738      else {
[ ]   739          xmlFatalErrMsg(ctxt, XML_ERR_INTERNAL_ERROR,
[ ]   740  	     "SAX.xmlSAX2AttributeDecl(%s) called while not in subset\n",
[ ]   741  	               name, NULL);
[ ]   742  	xmlFree(name);
[ ]   743  	xmlFreeEnumeration(tree);
[ ]   744  	return;
[ ]   745      }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758, calls xmlAddAttributeDecl at line 731)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      24       280  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      18         0  xmlSAX2ProcessingInstruction  (/src/libxml2/SAX2.c:2717-2769)
      18         0  xmlGetDtdQAttrDesc  (/src/libxml2/valid.c:3410-3418)
       0        18  xmlValidateAttributeDecl  (/src/libxml2/valid.c:4197-4288)
      20         3  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438)
      20         3  xmlValidCtxtNormalizeAttributeValue  (/src/libxml2/valid.c:4061-4111)
       9         0  valid.c:xmlValidNormalizeString  (/src/libxml2/valid.c:2596-2616)
       3         9  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199)
       0         5  valid.c:xmlValidGetElemDecl  (/src/libxml2/valid.c:5744-5791)
       0         3  valid.c:nodeVPop  (/src/libxml2/valid.c:452-465)
       0         3  xmlValidateOneAttribute  (/src/libxml2/valid.c:4431-4577)
       0         3  valid.c:xmlValidateOneCdataElement  (/src/libxml2/valid.c:5607-5660)
       0         3  xmlValidateOneElement  (/src/libxml2/valid.c:6034-6380)
       2         0  SAX2.c:xmlNsWarnMsg  (/src/libxml2/SAX2.c:194-204)
       0         2  valid.c:vstateVPush  (/src/libxml2/valid.c:259-300)
... (6 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758) ---
  d=2   L 709  T=0 F=39  T=0 F=79  if ((ctxt == NULL) || (ctxt->myDoc == NULL))
  d=2   L 709  T=0 F=39  T=0 F=79  if ((ctxt == NULL) || (ctxt->myDoc == NULL))
  d=2   L 717  T=0 F=39  T=0 F=79  if ((xmlStrEqual(fullname, BAD_CAST "xml:id")) &&
  d=2   L 730  T=0 F=39  T=0 F=79  if (ctxt->inSubset == 1)
  d=2   L 734  T=39 F=0  T=79 F=0  else if (ctxt->inSubset == 2)
  d=2   L 747  T=15 F=24  T=0 F=79  if (ctxt->vctxt.valid == 0)
  d=2   L 749  T=0 F=33  T=18 F=0  if ((attr != NULL) && (ctxt->validate) && (ctxt->wellForm...
  d=2   L 749  T=39 F=0  T=79 F=0  if ((attr != NULL) && (ctxt->validate) && (ctxt->wellForm...
  d=2   L 749  T=33 F=6  T=18 F=61  if ((attr != NULL) && (ctxt->validate) && (ctxt->wellForm...
  d=2   L 750  T=0 F=0  T=18 F=0  (ctxt->myDoc->intSubset != NULL))
  d=2   L 754  T=0 F=39  T=73 F=6  if (prefix != NULL)
  d=2   L 756  T=39 F=0  T=79 F=0  if (name != NULL)
--- d=1  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172) ---
  d=1   L1970  T=0 F=39  T=0 F=79  if (dtd == NULL) {
  d=1   L1974  T=0 F=39  T=0 F=79  if (name == NULL) {
  d=1   L1978  T=0 F=39  T=0 F=79  if (elem == NULL) {
  d=1   L1982  T=39 F=0  T=79 F=0  if (dtd->doc != NULL)
  d=1   L1990  T=21 F=18  T=50 F=29  case XML_ATTRIBUTE_CDATA:
  d=1   L1992  T=0 F=39  T=0 F=79  case XML_ATTRIBUTE_ID:
  d=1   L1994  T=0 F=39  T=0 F=79  case XML_ATTRIBUTE_IDREF:
  d=1   L1996  T=0 F=39  T=0 F=79  case XML_ATTRIBUTE_IDREFS:
  d=1   L1998  T=0 F=39  T=0 F=79  case XML_ATTRIBUTE_ENTITY:
  d=1   L2000  T=0 F=39  T=0 F=79  case XML_ATTRIBUTE_ENTITIES:
  d=1   L2002  T=0 F=39  T=0 F=79  case XML_ATTRIBUTE_NMTOKEN:
  d=1   L2004  T=0 F=39  T=0 F=79  case XML_ATTRIBUTE_NMTOKENS:
  d=1   L2006  T=18 F=21  T=29 F=50  case XML_ATTRIBUTE_ENUMERATION:
  d=1   L2008  T=0 F=39  T=0 F=79  case XML_ATTRIBUTE_NOTATION:
  d=1   L2010  T=0 F=39  T=0 F=79  default:
  d=1   L2017  T=36 F=3  T=58 F=21  if ((defaultValue != NULL) &&
  d=1   L2018  T=15 F=21  T=0 F=58  (!xmlValidateAttributeValueInternal(dtd->doc, type, defau...
  d=1   L2023  T=15 F=0  T=0 F=0  if (ctxt != NULL)
  d=1   L2032  T=39 F=0  T=79 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=1   L2032  T=39 F=0  T=79 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=1   L2033  T=39 F=0  T=79 F=0  (dtd->doc->intSubset != NULL) &&
  d=1   L2034  T=0 F=39  T=0 F=79  (dtd->doc->intSubset->attributes != NULL)) {
  d=1   L2046  T=18 F=21  T=29 F=50  if (table == NULL) {
  d=1   L2050  T=0 F=39  T=0 F=79  if (table == NULL) {
  d=1   L2059  T=0 F=39  T=0 F=79  if (ret == NULL) {
  d=1   L2077  T=0 F=39  T=61 F=18  if (dict) {
  d=1   L2088  T=21 F=18  T=58 F=21  if (defaultValue != NULL) {
  d=1   L2089  T=0 F=21  T=46 F=12  if (dict)
  d=1   L2099  T=0 F=39  T=0 F=79  if (xmlHashAddEntry3(table, ret->name, ret->prefix, ret->...
  d=1   L2117  T=39 F=0  T=79 F=0  if (elemDef != NULL) {
  d=1   L2120  T=0 F=39  T=0 F=79  if ((type == XML_ATTRIBUTE_ID) &&
  d=1   L2134  T=18 F=21  T=3 F=76  if ((xmlStrEqual(ret->name, BAD_CAST "xmlns")) ||
  d=1   L2135  T=0 F=21  T=73 F=3  ((ret->prefix != NULL &&
  d=1   L2136  T=0 F=0  T=20 F=53  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns"))))) {
  d=1   L2142  T=24 F=0  T=53 F=6  while ((tmp != NULL) &&
  d=1   L2143  T=21 F=3  T=6 F=47  ((xmlStrEqual(tmp->name, BAD_CAST "xmlns")) ||  <-- BLOCKER
  d=1   L2144  T=0 F=3  T=47 F=0  ((ret->prefix != NULL &&
  d=1   L2145  T=0 F=0  T=0 F=47  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns")))))) {
  d=1   L2146  T=18 F=3  T=3 F=3  if (tmp->nexth == NULL)
  d=1   L2150  T=21 F=0  T=50 F=6  if (tmp != NULL) {
  d=1   L2164  T=0 F=39  T=0 F=79  if (dtd->last == NULL) {

[off-chain: 492 additional divergent branches across 48 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
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
Seed 4 (id=ed9377be9621bf39, size=189 bytes, fuzzer=grimoire, trial=1, discovered_at=1816s, mutation_op=GrimoireExtensionMutator):
  0000: 55 54 46 38 06 00 5c 0a 3c 3f 6c 20 3f 3e 3c 21   UTF8..\.<?l ?><!
  0010: 44 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d 20   DOCTYPEa SYSTEM 
  0020: 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64   "dtds/127772.dtd
  0030: 22 3e 3c 61 3e 20 3c 62 20 6b 3a 66 3d 22 22 3e   "><a> <b k:f="">
Seed 5 (id=e1d7963fe300eca8, size=180 bytes, fuzzer=grimoire, trial=1, discovered_at=6869s, mutation_op=I2SRandReplace):
  0000: 55 54 46 38 06 00 5c 0a 3c 3f 6c 20 3f 3e 3c 21   UTF8..\.<?l ?><!
  0010: 44 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d 20   DOCTYPEa SYSTEM 
  0020: 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64   "dtds/127772.dtd
  0030: 22 3e 3c 61 3e 20 3c 62 20 6b 3a 39 3c 3a 62 3e   "><a> <b k:9<:b>

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=2fc1276953baf917, size=370 bytes, fuzzer=cmplog, trial=1, discovered_at=2s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=0be939129cb3ca8a, size=377 bytes, fuzzer=cmplog, trial=1, discovered_at=3s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=0d5f26ea8b67d379, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=93s, mutation_op=DwordInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=01986dbadd87a561, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=128s, mutation_op=ByteDecMutator,CrossoverReplaceMutator,BytesRandInsertMutator,ByteAddMutator,ByteAddMutator,CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=1c65f70d71c9b113, size=370 bytes, fuzzer=cmplog, trial=1, discovered_at=241s, mutation_op=BytesSetMutator,BytesSetMutator,BytesExpandMutator):
  0000: 3d 3d 3d 3d 3d 32 37 37 37 32 2e 20 20 20 5c 0a   =====27772.   \.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  55(U)x4 45(E)x1 3f(?)x1             06(.)x5 3d(=)x1 37(7)x1 2b(+)x1 +2u  PARTIAL
   0x0001  54(T)x4 55(U)x1 3e(>)x1             00(.)x7 3d(=)x1 37(7)x1 44(D)x1     DIFFER
   0x0002  46(F)x4 43(C)x1 3e(>)x1             00(.)x7 3d(=)x1 32(2)x1 20( )x1     DIFFER
   0x0003  38(8)x4 2d(-)x1 06(.)x1             00(.)x7 3d(=)x1 2e(.)x1 27(')x1     DIFFER
   0x0004  06(.)x4 4a(J)x1 37(7)x1             31(1)x7 3d(=)x1 78(x)x1 68(h)x1     DIFFER
   0x0005  00(.)x4 50(P)x1 d7(.)x1             32(2)x8 6d(m)x1 74(t)x1             DIFFER
   0x0006  5c(\)x3 37(7)x1 55(U)x1 ff(.)x1     37(7)x8 6c(l)x1 74(t)x1             PARTIAL
   0x0007  0a(.)x3 37(7)x1 54(T)x1 ff(.)x1     37(7)x8 5c(\)x1 70(p)x1             PARTIAL
   0x0008  3c(<)x3 32(2)x1 46(F)x1 ff(.)x1     37(7)x8 0a(.)x1 3a(:)x1             DIFFER
   0x0009  3f(?)x3 2e(.)x1 38(8)x1 ff(.)x1     32(2)x8 3c(<)x1 2f(/)x1             DIFFER
   0x000a  6c(l)x3 78(x)x1 06(.)x1 ff(.)x1     2e(.)x8 3f(?)x1 2f(/)x1             DIFFER
   0x000b  20( )x3 6d(m)x1 00(.)x1 ff(.)x1     78(x)x8 20( )x1 21(!)x1             PARTIAL
   0x000c  3f(?)x3 6c(l)x1 5c(\)x1 ff(.)x1     6d(m)x8 20( )x1 44(D)x1             DIFFER
   0x000d  3e(>)x3 5c(\)x1 0a(.)x1 6d(m)x1     6c(l)x8 20( )x1 4f(O)x1             DIFFER
   0x000e  3c(<)x4 0a(.)x1 49(I)x1             5c(\)x8 20( )x1 65(e)x1             DIFFER
   0x000f  21(!)x3 3c(<)x1 3f(?)x1 49(I)x1     0a(.)x8 76(v)x1 72(r)x1             DIFFER
   0x0010  44(D)x3 3f(?)x1 6c(l)x1 49(I)x1     3c(<)x8 65(e)x1 73(s)x1             DIFFER
   0x0011  4f(O)x3 6c(l)x1 20( )x1 49(I)x1     3f(?)x8 72(r)x1 69(i)x1             DIFFER
   0x0012  43(C)x3 20( )x1 3f(?)x1 6c(l)x1     78(x)x8 73(s)x1 6f(o)x1             DIFFER
   0x0013  54(T)x3 3f(?)x1 3e(>)x1 5c(\)x1     6d(m)x8 69(i)x1 6e(n)x1             DIFFER
   0x0014  59(Y)x3 3e(>)x1 3c(<)x1 0a(.)x1     6c(l)x8 6f(o)x1 3d(=)x1             DIFFER
   0x0015  50(P)x3 3c(<)x2 21(!)x1             20( )x8 6e(n)x1 22(")x1             DIFFER
   0x0016  45(E)x3 21(!)x1 44(D)x1 3f(?)x1     76(v)x8 3d(=)x1 31(1)x1             DIFFER
   0x0017  61(a)x3 44(D)x1 4f(O)x1 6c(l)x1     65(e)x8 22(")x1 2e(.)x1             DIFFER
   0x0018  20( )x3 4f(O)x1 43(C)x1 3f(?)x1     72(r)x8 31(1)x1 30(0)x1             DIFFER
   0x0019  53(S)x3 43(C)x1 54(T)x1 3e(>)x1     73(s)x8 2e(.)x1 22(")x1             DIFFER
   0x001a  59(Y)x4 54(T)x1 3c(<)x1             69(i)x8 30(0)x1 3f(?)x1             DIFFER
   0x001b  53(S)x3 59(Y)x1 50(P)x1 21(!)x1     6f(o)x8 22(")x1 3e(>)x1             DIFFER
   0x001c  54(T)x3 50(P)x1 45(E)x1 44(D)x1     6e(n)x8 3f(?)x1 0a(.)x1             DIFFER
   0x001d  45(E)x4 61(a)x1 4f(O)x1             3d(=)x8 3e(>)x1 3c(<)x1             DIFFER
   0x001e  4d(M)x3 61(a)x1 20( )x1 43(C)x1     22(")x8 0a(.)x1 21(!)x1             DIFFER
   0x001f  20( )x4 53(S)x1 54(T)x1             31(1)x8 3c(<)x1 44(D)x1             DIFFER
   0x0020  22(")x3 59(Y)x2 53(S)x1             2e(.)x8 21(!)x1 4f(O)x1             DIFFER
   0x0021  64(d)x3 59(Y)x1 53(S)x1 50(P)x1     30(0)x8 44(D)x1 43(C)x1             DIFFER
   0x0022  74(t)x3 53(S)x1 54(T)x1 45(E)x1     22(")x8 4f(O)x1 54(T)x1             PARTIAL
   0x0023  64(d)x3 54(T)x1 45(E)x1 61(a)x1     3f(?)x8 43(C)x1 59(Y)x1             DIFFER
   0x0024  73(s)x3 45(E)x1 4d(M)x1 20( )x1     3e(>)x8 54(T)x1 50(P)x1             DIFFER
   0x0025  2f(/)x3 4d(M)x1 20( )x1 53(S)x1     0a(.)x8 59(Y)x1 45(E)x1             DIFFER
   0x0026  31(1)x3 20( )x1 22(")x1 59(Y)x1     3c(<)x8 50(P)x1 20( )x1             PARTIAL
   0x0027  32(2)x3 22(")x1 64(d)x1 53(S)x1     21(!)x8 45(E)x1 61(a)x1             DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7099.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7099,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7099 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7099 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7099 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).