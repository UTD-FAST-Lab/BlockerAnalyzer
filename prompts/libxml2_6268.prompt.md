==== BLOCKER ====
Target: libxml2
Branch ID: 6268
Location: /src/libxml2/SAX2.c:2173:13
Enclosing function: SAX2.c:xmlSAX2AttributeNs
Source line:         if ((prefix == ctxt->str_xml) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.00h  loser=21.10h
  avg hitcount on branch: winner=22  loser=1
  prob_div=0.80  dur_div=14.10h  hit_div=22
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6268/{W,L}/branch_coverage_show.txt

--- Enclosing function: SAX2.c:xmlSAX2AttributeNs (/src/libxml2/SAX2.c:1996-2199) ---
[ ]  1994  		   const xmlChar * value,
[ ]  1995  		   const xmlChar * valueend)
[B]  1996  {
[B]  1997      xmlAttrPtr ret;
[B]  1998      xmlNsPtr namespace = NULL;
[B]  1999      xmlChar *dup = NULL;
[ ]  2000  
[ ]  2001      /*
[ ]  2002       * Note: if prefix == NULL, the attribute is not in the default namespace
[ ]  2003       */
[B]  2004      if (prefix != NULL)
[W]  2005  	namespace = xmlSearchNs(ctxt->myDoc, ctxt->node, prefix);
[ ]  2006  
[ ]  2007      /*
[ ]  2008       * allocate the node
[ ]  2009       */
[B]  2010      if (ctxt->freeAttrs != NULL) {
[ ]  2011          ret = ctxt->freeAttrs;
[ ]  2012  	ctxt->freeAttrs = ret->next;
[ ]  2013  	ctxt->freeAttrsNr--;
[ ]  2014  	memset(ret, 0, sizeof(xmlAttr));
[ ]  2015  	ret->type = XML_ATTRIBUTE_NODE;
[ ]  2016  
[ ]  2017  	ret->parent = ctxt->node;
[ ]  2018  	ret->doc = ctxt->myDoc;
[ ]  2019  	ret->ns = namespace;
[ ]  2020  
[ ]  2021  	if (ctxt->dictNames)
[ ]  2022  	    ret->name = localname;
[ ]  2023  	else
[ ]  2024  	    ret->name = xmlStrdup(localname);
[ ]  2025  
[ ]  2026          /* link at the end to preserve order, TODO speed up with a last */
[ ]  2027  	if (ctxt->node->properties == NULL) {
[ ]  2028  	    ctxt->node->properties = ret;
[ ]  2029  	} else {
[ ]  2030  	    xmlAttrPtr prev = ctxt->node->properties;
[ ]  2031  
[ ]  2032  	    while (prev->next != NULL) prev = prev->next;
[ ]  2033  	    prev->next = ret;
[ ]  2034  	    ret->prev = prev;
[ ]  2035  	}
[ ]  2036  
[ ]  2037  	if ((__xmlRegisterCallbacks) && (xmlRegisterNodeDefaultValue))
[ ]  2038  	    xmlRegisterNodeDefaultValue((xmlNodePtr)ret);
[B]  2039      } else {
[B]  2040  	if (ctxt->dictNames)
[B]  2041  	    ret = xmlNewNsPropEatName(ctxt->node, namespace,
[B]  2042  	                              (xmlChar *) localname, NULL);
[L]  2043  	else
[L]  2044  	    ret = xmlNewNsProp(ctxt->node, namespace, localname, NULL);
[B]  2045  	if (ret == NULL) {
[ ]  2046  	    xmlErrMemory(ctxt, "xmlSAX2AttributeNs");
[ ]  2047  	    return;
[ ]  2048  	}
[B]  2049      }
[ ]  2050  
[B]  2051      if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
[L]  2052  	xmlNodePtr tmp;
[ ]  2053  
[ ]  2054  	/*
[ ]  2055  	 * We know that if there is an entity reference, then
[ ]  2056  	 * the string has been dup'ed and terminates with 0
[ ]  2057  	 * otherwise with ' or "
[ ]  2058  	 */
[L]  2059  	if (*valueend != 0) {
[L]  2060  	    tmp = xmlSAX2TextNode(ctxt, value, valueend - value);
[L]  2061  	    ret->children = tmp;
[L]  2062  	    ret->last = tmp;
[L]  2063  	    if (tmp != NULL) {
[L]  2064  		tmp->doc = ret->doc;
[L]  2065  		tmp->parent = (xmlNodePtr) ret;
[L]  2066  	    }
[L]  2067  	} else {
[L]  2068  	    ret->children = xmlStringLenGetNodeList(ctxt->myDoc, value,
[L]  2069  						    valueend - value);
[L]  2070  	    tmp = ret->children;
[L]  2071  	    while (tmp != NULL) {
[L]  2072  	        tmp->doc = ret->doc;
[L]  2073  		tmp->parent = (xmlNodePtr) ret;
[L]  2074  		if (tmp->next == NULL)
[L]  2075  		    ret->last = tmp;
[L]  2076  		tmp = tmp->next;
[L]  2077  	    }
[L]  2078  	}
[B]  2079      } else if (value != NULL) {
[B]  2080  	xmlNodePtr tmp;
[ ]  2081  
[B]  2082  	tmp = xmlSAX2TextNode(ctxt, value, valueend - value);
[B]  2083  	ret->children = tmp;
[B]  2084  	ret->last = tmp;
[B]  2085  	if (tmp != NULL) {
[B]  2086  	    tmp->doc = ret->doc;
[B]  2087  	    tmp->parent = (xmlNodePtr) ret;
[B]  2088  	}
[B]  2089      }
[ ]  2090  
[B]  2091  #ifdef LIBXML_VALID_ENABLED
[B]  2092      if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
[B]  2093          ctxt->myDoc && ctxt->myDoc->intSubset) {
[ ]  2094  	/*
[ ]  2095  	 * If we don't substitute entities, the validation should be
[ ]  2096  	 * done on a value with replaced entities anyway.
[ ]  2097  	 */
[ ]  2098          if (!ctxt->replaceEntities) {
[ ]  2099  	    dup = xmlSAX2DecodeAttrEntities(ctxt, value, valueend);
[ ]  2100  	    if (dup == NULL) {
[ ]  2101  	        if (*valueend == 0) {
[ ]  2102  		    ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt,
[ ]  2103  				    ctxt->myDoc, ctxt->node, ret, value);
[ ]  2104  		} else {
[ ]  2105  		    /*
[ ]  2106  		     * That should already be normalized.
[ ]  2107  		     * cheaper to finally allocate here than duplicate
[ ]  2108  		     * entry points in the full validation code
[ ]  2109  		     */
[ ]  2110  		    dup = xmlStrndup(value, valueend - value);
[ ]  2111  
[ ]  2112  		    ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt,
[ ]  2113  				    ctxt->myDoc, ctxt->node, ret, dup);
[ ]  2114  		}
[ ]  2115  	    } else {
[ ]  2116  	        /*
[ ]  2117  		 * dup now contains a string of the flattened attribute
[ ]  2118  		 * content with entities substituted. Check if we need to
[ ]  2119  		 * apply an extra layer of normalization.
[ ]  2120  		 * It need to be done twice ... it's an extra burden related
[ ]  2121  		 * to the ability to keep references in attributes
[ ]  2122  		 */
[ ]  2123  		if (ctxt->attsSpecial != NULL) {
[ ]  2124  		    xmlChar *nvalnorm;
[ ]  2125  		    xmlChar fn[50];
[ ]  2126  		    xmlChar *fullname;
[ ]  2127  
[ ]  2128  		    fullname = xmlBuildQName(localname, prefix, fn, 50);
[ ]  2129  		    if (fullname != NULL) {
[ ]  2130  			ctxt->vctxt.valid = 1;
[ ]  2131  		        nvalnorm = xmlValidCtxtNormalizeAttributeValue(
[ ]  2132  			                 &ctxt->vctxt, ctxt->myDoc,
[ ]  2133  					 ctxt->node, fullname, dup);
[ ]  2134  			if (ctxt->vctxt.valid != 1)
[ ]  2135  			    ctxt->valid = 0;
[ ]  2136  
[ ]  2137  			if ((fullname != fn) && (fullname != localname))
[ ]  2138  			    xmlFree(fullname);
[ ]  2139  			if (nvalnorm != NULL) {
[ ]  2140  			    xmlFree(dup);
[ ]  2141  			    dup = nvalnorm;
[ ]  2142  			}
[ ]  2143  		    }
[ ]  2144  		}
[ ]  2145  
[ ]  2146  		ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt,
[ ]  2147  			        ctxt->myDoc, ctxt->node, ret, dup);
[ ]  2148  	    }
[ ]  2149  	} else {
[ ]  2150  	    /*
[ ]  2151  	     * if entities already have been substituted, then
[ ]  2152  	     * the attribute as passed is already normalized
[ ]  2153  	     */
[ ]  2154  	    dup = xmlStrndup(value, valueend - value);
[ ]  2155  
[ ]  2156  	    ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt,
[ ]  2157  	                             ctxt->myDoc, ctxt->node, ret, dup);
[ ]  2158  	}
[ ]  2159      } else
[B]  2160  #endif /* LIBXML_VALID_ENABLED */
[B]  2161             if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
[B]  2162  	       (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
[B]  2163  	        ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
[ ]  2164                 /* Don't create IDs containing entity references */
[B]  2165                 (ret->children != NULL) &&
[B]  2166                 (ret->children->type == XML_TEXT_NODE) &&
[B]  2167                 (ret->children->next == NULL)) {
[B]  2168          xmlChar *content = ret->children->content;
[ ]  2169          /*
[ ]  2170  	 * when validating, the ID registration is done at the attribute
[ ]  2171  	 * validation level. Otherwise we have to do specific handling here.
[ ]  2172  	 */
[B]  2173          if ((prefix == ctxt->str_xml) && <-- BLOCKER
[B]  2174  	           (localname[0] == 'i') && (localname[1] == 'd') &&
[B]  2175  		   (localname[2] == 0)) {
[ ]  2176  	    /*
[ ]  2177  	     * Add the xml:id value
[ ]  2178  	     *
[ ]  2179  	     * Open issue: normalization of the value.
[ ]  2180  	     */
[W]  2181  #if defined(LIBXML_SAX1_ENABLED) || defined(LIBXML_HTML_ENABLED) || defined(LIBXML_WRITER_ENABLED) || defined(LIBXML_LEGACY_ENABLED)
[W]  2182  #ifdef LIBXML_VALID_ENABLED
[W]  2183  	    if (xmlValidateNCName(content, 1) != 0) {
[W]  2184  	        xmlErrValid(ctxt, XML_DTD_XMLID_VALUE,
[W]  2185  		      "xml:id : attribute value %s is not an NCName\n",
[W]  2186  			    (const char *) content, NULL);
[W]  2187  	    }
[W]  2188  #endif
[W]  2189  #endif
[W]  2190  	    xmlAddID(&ctxt->vctxt, ctxt->myDoc, content, ret);
[B]  2191  	} else if (xmlIsID(ctxt->myDoc, ctxt->node, ret)) {
[ ]  2192  	    xmlAddID(&ctxt->vctxt, ctxt->myDoc, content, ret);
[L]  2193  	} else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret)) {
[ ]  2194  	    xmlAddRef(&ctxt->vctxt, ctxt->myDoc, content, ret);
[ ]  2195  	}
[B]  2196      }
[B]  2197      if (dup != NULL)
[ ]  2198  	xmlFree(dup);
[B]  2199  }

--- Caller (1 hop): xmlSAX2StartElementNs (/src/libxml2/SAX2.c:2228-2459, calls SAX2.c:xmlSAX2AttributeNs at line 2436) (±10 around call site) ---
[L]  2426  		    lname = xmlBuildQName(attributes[j], attributes[j+1],
[L]  2427  		                          NULL, 0);
[L]  2428  		    if (lname != NULL) {
[L]  2429  			xmlSAX2AttributeNs(ctxt, lname, NULL,
[L]  2430  			                   attributes[j+3], attributes[j+4]);
[L]  2431  			xmlFree(lname);
[L]  2432  		        continue;
[L]  2433  		    }
[L]  2434  		}
[L]  2435  	    }
[B]  2436  	    xmlSAX2AttributeNs(ctxt, attributes[j], attributes[j+1], <-- CALL
[B]  2437  			       attributes[j+3], attributes[j+4]);
[B]  2438  	}
[B]  2439      }
[ ]  2440  
[B]  2441  #ifdef LIBXML_VALID_ENABLED
[ ]  2442      /*
[ ]  2443       * If it's the Document root, finish the DTD validation and
[ ]  2444       * check the document root element for validity
[ ]  2445       */
[B]  2446      if ((ctxt->validate) &&

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459, calls SAX2.c:xmlSAX2AttributeNs at line 2421)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      29       112  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
      23        85  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)
       0        29  xmlSAX2EndElementNs  (/src/libxml2/SAX2.c:2476-2502)
      13        39  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199)  <-- enclosing
      25         0  SAX2.c:xmlErrValid  (/src/libxml2/SAX2.c:99-124)
       0        21  xmlSAX2ResolveEntity  (/src/libxml2/SAX2.c:514-538)
       0         9  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758)
       0         9  xmlSAX2IgnorableWhitespace  (/src/libxml2/SAX2.c:2698-2704)
       9         0  xmlSAX2ProcessingInstruction  (/src/libxml2/SAX2.c:2717-2769)
       0         6  xmlSAX2ElementDecl  (/src/libxml2/SAX2.c:772-807)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459) ---
  d=2   L2237  T=0 F=23  T=0 F=85  if (ctx == NULL) return;
  d=2   L2242  T=12 F=11  T=0 F=85  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=2   L2242  T=12 F=0  T=0 F=0  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=2   L2243  T=3 F=9  T=0 F=0  ((ctxt->myDoc->intSubset == NULL) ||
  d=2   L2244  T=9 F=0  T=0 F=0  ((ctxt->myDoc->intSubset->notations == NULL) &&
  d=2   L2245  T=9 F=0  T=0 F=0  (ctxt->myDoc->intSubset->elements == NULL) &&
  d=2   L2246  T=9 F=0  T=0 F=0  (ctxt->myDoc->intSubset->attributes == NULL) &&
  d=2   L2247  T=9 F=0  T=0 F=0  (ctxt->myDoc->intSubset->entities == NULL)))) {
  d=2   L2256  T=0 F=23  T=0 F=85  if ((prefix != NULL) && (URI == NULL)) {
  d=2   L2270  T=0 F=23  T=0 F=85  if (ctxt->freeElems != NULL) {
  d=2   L2293  T=23 F=0  T=82 F=3  if (ctxt->dictNames)
  d=2   L2296  T=0 F=0  T=3 F=0  else if (lname == NULL)
  d=2   L2301  T=0 F=23  T=0 F=85  if (ret == NULL) {
  d=2   L2306  T=23 F=0  T=85 F=0  if (ctxt->linenumbers) {
  d=2   L2307  T=23 F=0  T=85 F=0  if (ctxt->input != NULL) {
  d=2   L2308  T=23 F=0  T=85 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=2   L2315  T=13 F=10  T=36 F=49  if (parent == NULL) {
  d=2   L2321  T=0 F=23  T=3 F=85  for (i = 0,j = 0;j < nb_namespaces;j++) {
  d=2   L2325  T=0 F=0  T=3 F=0  if (ns != NULL) {
  d=2   L2326  T=0 F=0  T=3 F=0  if (last == NULL) {
  d=2   L2332  T=0 F=0  T=0 F=3  if ((URI != NULL) && (prefix == pref))
  d=2   L2343  T=0 F=0  T=0 F=3  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L2343  T=0 F=0  T=3 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L2355  T=0 F=23  T=0 F=85  if (nodePush(ctxt, ret) < 0) {
  d=2   L2364  T=10 F=13  T=49 F=36  if (parent != NULL) {
  d=2   L2365  T=10 F=0  T=49 F=0  if (parent->type == XML_ELEMENT_NODE) {
  d=2   L2375  T=0 F=23  T=3 F=82  if ((nb_defaulted != 0) &&
  d=2   L2376  T=0 F=0  T=0 F=3  ((ctxt->loadsubset & XML_COMPLETE_ATTRS) == 0))
  d=2   L2383  T=0 F=23  T=0 F=85  if ((URI != NULL) && (ret->ns == NULL)) {
  d=2   L2409  T=13 F=10  T=36 F=49  if (nb_attributes > 0) {
  d=2   L2410  T=13 F=13  T=39 F=36  for (j = 0,i = 0;i < nb_attributes;i++,j+=5) {
  d=2   L2414  T=0 F=13  T=35 F=0  if ((attributes[j+1] != NULL) && (attributes[j+2] == NULL...
  d=2   L2414  T=13 F=0  T=35 F=4  if ((attributes[j+1] != NULL) && (attributes[j+2] == NULL...
  d=2   L2415  T=0 F=0  T=32 F=3  if (ctxt->dictNames) {
  d=2   L2420  T=0 F=0  T=32 F=0  if (fullname != NULL) {
  d=2   L2428  T=0 F=0  T=3 F=0  if (lname != NULL) {
  d=2   L2446  T=0 F=23  T=0 F=85  if ((ctxt->validate) &&
--- d=1  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199) ---
  d=1   L2004  T=13 F=0  T=0 F=39  if (prefix != NULL)
  d=1   L2010  T=0 F=13  T=0 F=39  if (ctxt->freeAttrs != NULL) {
  d=1   L2040  T=13 F=0  T=36 F=3  if (ctxt->dictNames)
  d=1   L2045  T=0 F=13  T=0 F=39  if (ret == NULL) {
  d=1   L2051  T=0 F=13  T=13 F=26  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=1   L2051  T=0 F=0  T=13 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=1   L2059  T=0 F=0  T=7 F=6  if (*valueend != 0) {
  d=1   L2063  T=0 F=0  T=7 F=0  if (tmp != NULL) {
  d=1   L2071  T=0 F=0  T=6 F=6  while (tmp != NULL) {
  d=1   L2074  T=0 F=0  T=6 F=0  if (tmp->next == NULL)
  d=1   L2079  T=13 F=0  T=26 F=0  } else if (value != NULL) {
  d=1   L2085  T=13 F=0  T=26 F=0  if (tmp != NULL) {
  d=1   L2092  T=13 F=0  T=39 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L2092  T=0 F=13  T=0 F=39  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L2161  T=13 F=0  T=39 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=1   L2162  T=0 F=0  T=13 F=0  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=1   L2162  T=0 F=13  T=13 F=26  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=1   L2163  T=13 F=0  T=26 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L2163  T=13 F=0  T=26 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L2165  T=13 F=0  T=39 F=0  (ret->children != NULL) &&
  d=1   L2166  T=13 F=0  T=39 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=1   L2167  T=13 F=0  T=39 F=0  (ret->children->next == NULL)) {
  d=1   L2173  T=13 F=0  T=0 F=39  if ((prefix == ctxt->str_xml) &&  <-- BLOCKER
  d=1   L2174  T=13 F=0  T=0 F=0  (localname[0] == 'i') && (localname[1] == 'd') &&
  d=1   L2174  T=13 F=0  T=0 F=0  (localname[0] == 'i') && (localname[1] == 'd') &&
  d=1   L2175  T=13 F=0  T=0 F=0  (localname[2] == 0)) {
  d=1   L2183  T=13 F=0  T=0 F=0  if (xmlValidateNCName(content, 1) != 0) {
  d=1   L2191  T=0 F=0  T=0 F=39  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret)) {
  d=1   L2193  T=0 F=0  T=0 F=39  } else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret)) {
  d=1   L2197  T=0 F=13  T=0 F=39  if (dup != NULL)

[off-chain: 122 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=6325b1fe38e4d1ee, size=348 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=36414s, mutation_op=BytesRandInsertMutator,ByteRandMutator,ByteAddMutator,TokenReplace,DwordAddMutator):
  0000: 37 80 00 01 00 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   7....l\.<?x.l:ve
  0010: 72 73 64 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsdon="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 80 32 26 37 37 32 2e 64 3a    ".:d./.2&772.d:
Seed 2 (id=31a0f4cf800d3991, size=133 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=53377s, mutation_op=BitFlipMutator,WordAddMutator,BytesExpandMutator,ByteRandMutator):
  0000: 73 69 7d 74 74 74 74 74 74 74 74 74 74 09 78 6d   si}tttttttttt.xm
  0010: 6c 3a 69 64 3d 22 20 3a 69 64 3d 22 26 26 73 69   l:id=" :id="&&si
  0020: 6d 70 6c 9b 29 20 e0 23 00 00 26 00 6b 3a 74 5c   mpl.) .#..&.k:t\
  0030: 0a 3c 74 f6 74 74 74 74 74 74 74 74 09 78 6d 6c   .<t.tttttttt.xml
Seed 3 (id=47df83d1c8b0099f, size=317 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=70849s, mutation_op=BytesInsertMutator,BytesCopyMutator,ByteAddMutator,DwordAddMutator):
  0000: 7f 00 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   ...xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 26 37 37 32 2e 64 3a    ".:d./12&772.d:
Seed 4 (id=73218d6bef4b5ebe, size=322 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=71226s, mutation_op=WordAddMutator,BytesSetMutator,ByteAddMutator,BytesSwapMutator,ByteInterestingMutator,ByteInterestingMutator):
  0000: 7f 00 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   ...xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0d 2f 31 32 26 37 37 32 2e 64 3a    ".:d./12&772.d:

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=05a2233124360cc9, size=299 bytes, fuzzer=cmplog, trial=1, discovered_at=22s, mutation_op=BytesExpandMutator,TokenReplace,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2c 78 6d 6c 5c 0a   ....127772,xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 6b 6b   a SYSTEM "dtdskk
Seed 2 (id=01f8661e47872c51, size=437 bytes, fuzzer=cmplog, trial=1, discovered_at=1510s, mutation_op=CrossoverInsertMutator,ByteInterestingMutator):
  0000: 65 65 65 65 65 54 54 4c 49 53 54 20 62 20 78 6d   eeeeeTTLIST b xm
  0010: 6c 6e 73 3a 78 6c 69 6e 6b 28 2a 43 44 41 54 41   lns:xlink(*CDATA
  0020: 9f 20 20 20 20 23 06 00 00 00 31 32 37 37 37 32   .    #....127772
  0030: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
Seed 3 (id=047fe13ea3b05010, size=386 bytes, fuzzer=cmplog, trial=1, discovered_at=4456s, mutation_op=WordAddMutator,BytesDeleteMutator,CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 3b 31   a SYSTEM "dtds;1
Seed 4 (id=077f724a2edd0f02, size=346 bytes, fuzzer=cmplog, trial=1, discovered_at=4577s, mutation_op=BytesDeleteMutator,BytesInsertCopyMutator,ByteFlipMutator,ByteFlipMutator,CrossoverReplaceMutator,BytesRandSetMutator,BytesCopyMutator):
  0000: 41 54 54 4c 49 53 54 20 62 20 78 6d 6c 6e 73 3a   ATTLIST b xmlns:
  0010: 78 6c 69 6e 6b 20 20 43 44 41 54 41 20 20 20 20   xlink  CDATA    
  0020: 20 23 46 49 58 20 20 20 20 20 20 20 20 20 20 20    #FIX           
  0030: 20 78 6c 69 6e 6b 3a 74 79 70 65 20 20 20 28 73    xlink:type   (s
Seed 5 (id=0400712593575d9c, size=427 bytes, fuzzer=cmplog, trial=1, discovered_at=4800s, mutation_op=BytesInsertMutator,CrossoverInsertMutator,WordAddMutator,QwordAddMutator,BytesCopyMutator,BitFlipMutator,WordAddMutator):
  0000: 05 e5 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  7f(.)x2 37(7)x1 73(s)x1             06(.)x4 65(e)x1 41(A)x1 05(.)x1 +3u  DIFFER
   0x0001  00(.)x2 80(.)x1 69(i)x1             00(.)x6 65(e)x1 54(T)x1 e5(.)x1 +1u  PARTIAL
   0x0002  2e(.)x2 00(.)x1 7d(})x1             00(.)x7 65(e)x1 54(T)x1 4f(O)x1     PARTIAL
   0x0003  78(x)x2 01(.)x1 74(t)x1             00(.)x7 65(e)x1 4c(L)x1 43(C)x1     DIFFER
   0x0004  6d(m)x2 00(.)x1 74(t)x1             31(1)x6 65(e)x1 49(I)x1 54(T)x1 +1u  DIFFER
   0x0005  6c(l)x3 74(t)x1                     32(2)x6 54(T)x1 53(S)x1 59(Y)x1 +1u  DIFFER
   0x0006  5c(\)x3 74(t)x1                     37(7)x6 54(T)x2 50(P)x1 02(.)x1     DIFFER
   0x0007  0a(.)x3 74(t)x1                     37(7)x6 4c(L)x1 20( )x1 45(E)x1 +1u  DIFFER
   0x0008  3c(<)x3 74(t)x1                     37(7)x7 49(I)x1 62(b)x1 20( )x1     DIFFER
   0x0009  3f(?)x3 74(t)x1                     32(2)x7 53(S)x1 20( )x1 61(a)x1     DIFFER
   0x000a  78(x)x3 74(t)x1                     2e(.)x5 2c(,)x2 54(T)x1 78(x)x1 +1u  PARTIAL
   0x000b  0a(.)x3 74(t)x1                     78(x)x6 20( )x1 6d(m)x1 bb(.)x1 +1u  DIFFER
   0x000c  6c(l)x3 74(t)x1                     6d(m)x6 62(b)x1 6c(l)x1 8e(.)x1 +1u  PARTIAL
   0x000d  3a(:)x3 09(.)x1                     6c(l)x6 20( )x1 6e(n)x1 36(6)x1 +1u  DIFFER
   0x000e  76(v)x3 78(x)x1                     5c(\)x6 78(x)x1 73(s)x1 ef(.)x1 +1u  PARTIAL
   0x000f  65(e)x3 6d(m)x1                     0a(.)x6 6d(m)x1 3a(:)x1 53(S)x1 +1u  PARTIAL
   0x0010  72(r)x3 6c(l)x1                     3c(<)x6 6c(l)x1 78(x)x1 5c(\)x1 +1u  PARTIAL
   0x0011  73(s)x3 3a(:)x1                     3f(?)x6 6e(n)x1 6c(l)x1 32(2)x1 +1u  DIFFER
   0x0012  69(i)x3 64(d)x1                     78(x)x6 73(s)x1 69(i)x1 1a(.)x1 +1u  PARTIAL
   0x0013  6f(o)x3 64(d)x1                     6d(m)x7 3a(:)x1 6e(n)x1 64(d)x1     PARTIAL
   0x0014  6e(n)x3 3d(=)x1                     6c(l)x7 78(x)x1 6b(k)x1 74(t)x1     DIFFER
   0x0015  3d(=)x3 22(")x1                     20( )x7 6c(l)x1 2a(*)x1 64(d)x1     DIFFER
   0x0016  22(")x3 20( )x1                     76(v)x7 69(i)x1 20( )x1 06(.)x1     PARTIAL
   0x0017  31(1)x3 3a(:)x1                     65(e)x7 6e(n)x1 43(C)x1 00(.)x1     DIFFER
   0x0018  2e(.)x3 69(i)x1                     72(r)x7 6b(k)x1 44(D)x1 00(.)x1     DIFFER
   0x0019  30(0)x3 64(d)x1                     73(s)x7 28(()x1 41(A)x1 00(.)x1     DIFFER
   0x001a  3c(<)x3 3d(=)x1                     69(i)x6 2a(*)x1 54(T)x1 3e(>)x1 +1u  DIFFER
   0x001b  3f(?)x3 22(")x1                     6f(o)x7 43(C)x1 41(A)x1 32(2)x1     DIFFER
   0x001c  3e(>)x3 26(&)x1                     6e(n)x7 44(D)x1 20( )x1 37(7)x1     DIFFER
   0x001d  0a(.)x3 26(&)x1                     3d(=)x7 41(A)x1 20( )x1 00(.)x1     DIFFER
   0x001e  3c(<)x3 73(s)x1                     22(")x6 54(T)x1 20( )x1 29())x1 +1u  DIFFER
   0x001f  21(!)x3 69(i)x1                     31(1)x7 41(A)x1 20( )x1 00(.)x1     DIFFER
   0x0020  44(D)x3 6d(m)x1                     2e(.)x7 9f(.)x1 20( )x1 10(.)x1     DIFFER
   0x0021  4f(O)x3 70(p)x1                     30(0)x7 20( )x1 23(#)x1 0f(.)x1     DIFFER
   0x0022  43(C)x3 6c(l)x1                     22(")x7 20( )x1 46(F)x1 00(.)x1     DIFFER
   0x0023  54(T)x3 9b(.)x1                     3f(?)x7 20( )x1 49(I)x1 32(2)x1     DIFFER
   0x0024  59(Y)x3 29())x1                     3e(>)x7 20( )x1 58(X)x1 2e(.)x1     DIFFER
   0x0025  50(P)x3 20( )x1                     0a(.)x6 20( )x2 23(#)x1 78(x)x1     PARTIAL
   0x0026  45(E)x3 e0(.)x1                     3c(<)x6 06(.)x1 20( )x1 09(.)x1 +1u  DIFFER
   0x0027  3a(:)x3 23(#)x1                     21(!)x7 00(.)x1 20( )x1 6c(l)x1     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6268.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6268,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6268 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6268 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6268 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).