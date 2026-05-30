==== BLOCKER ====
Target: libxml2
Branch ID: 7451
Location: /src/libxml2/SAX2.c:2332:10
Enclosing function: xmlSAX2StartElementNs
Source line: 	    if ((URI != NULL) && (prefix == pref))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           0       10          0  loser (value_profile vs value_profile_cmplog)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                        3        6          1  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             2        5          3  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=6.90h  loser=20.40h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.90  dur_div=13.50h  hit_div=5
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7451/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlSAX2StartElementNs (/src/libxml2/SAX2.c:2228-2459) ---
[ ]  2226  		      int nb_defaulted,
[ ]  2227  		      const xmlChar **attributes)
[B]  2228  {
[B]  2229      xmlParserCtxtPtr ctxt = (xmlParserCtxtPtr) ctx;
[B]  2230      xmlNodePtr ret;
[B]  2231      xmlNodePtr parent;
[B]  2232      xmlNsPtr last = NULL, ns;
[B]  2233      const xmlChar *uri, *pref;
[B]  2234      xmlChar *lname = NULL;
[B]  2235      int i, j;
[ ]  2236  
[B]  2237      if (ctx == NULL) return;
[B]  2238      parent = ctxt->node;
[ ]  2239      /*
[ ]  2240       * First check on validity:
[ ]  2241       */
[B]  2242      if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
[B]  2243          ((ctxt->myDoc->intSubset == NULL) ||
[ ]  2244  	 ((ctxt->myDoc->intSubset->notations == NULL) &&
[ ]  2245  	  (ctxt->myDoc->intSubset->elements == NULL) &&
[ ]  2246  	  (ctxt->myDoc->intSubset->attributes == NULL) &&
[ ]  2247  	  (ctxt->myDoc->intSubset->entities == NULL)))) {
[ ]  2248  	xmlErrValid(ctxt, XML_DTD_NO_DTD,
[ ]  2249  	  "Validation failed: no DTD found !", NULL, NULL);
[ ]  2250  	ctxt->validate = 0;
[ ]  2251      }
[ ]  2252  
[ ]  2253      /*
[ ]  2254       * Take care of the rare case of an undefined namespace prefix
[ ]  2255       */
[B]  2256      if ((prefix != NULL) && (URI == NULL)) {
[ ]  2257          if (ctxt->dictNames) {
[ ]  2258  	    const xmlChar *fullname;
[ ]  2259  
[ ]  2260  	    fullname = xmlDictQLookup(ctxt->dict, prefix, localname);
[ ]  2261  	    if (fullname != NULL)
[ ]  2262  	        localname = fullname;
[ ]  2263  	} else {
[ ]  2264  	    lname = xmlBuildQName(localname, prefix, NULL, 0);
[ ]  2265  	}
[ ]  2266      }
[ ]  2267      /*
[ ]  2268       * allocate the node
[ ]  2269       */
[B]  2270      if (ctxt->freeElems != NULL) {
[ ]  2271          ret = ctxt->freeElems;
[ ]  2272  	ctxt->freeElems = ret->next;
[ ]  2273  	ctxt->freeElemsNr--;
[ ]  2274  	memset(ret, 0, sizeof(xmlNode));
[ ]  2275          ret->doc = ctxt->myDoc;
[ ]  2276  	ret->type = XML_ELEMENT_NODE;
[ ]  2277  
[ ]  2278  	if (ctxt->dictNames)
[ ]  2279  	    ret->name = localname;
[ ]  2280  	else {
[ ]  2281  	    if (lname == NULL)
[ ]  2282  		ret->name = xmlStrdup(localname);
[ ]  2283  	    else
[ ]  2284  	        ret->name = lname;
[ ]  2285  	    if (ret->name == NULL) {
[ ]  2286  	        xmlSAX2ErrMemory(ctxt, "xmlSAX2StartElementNs");
[ ]  2287  		return;
[ ]  2288  	    }
[ ]  2289  	}
[ ]  2290  	if ((__xmlRegisterCallbacks) && (xmlRegisterNodeDefaultValue))
[ ]  2291  	    xmlRegisterNodeDefaultValue(ret);
[B]  2292      } else {
[B]  2293  	if (ctxt->dictNames)
[B]  2294  	    ret = xmlNewDocNodeEatName(ctxt->myDoc, NULL,
[B]  2295  	                               (xmlChar *) localname, NULL);
[L]  2296  	else if (lname == NULL)
[L]  2297  	    ret = xmlNewDocNode(ctxt->myDoc, NULL, localname, NULL);
[ ]  2298  	else
[ ]  2299  	    ret = xmlNewDocNodeEatName(ctxt->myDoc, NULL,
[ ]  2300  	                               (xmlChar *) lname, NULL);
[B]  2301  	if (ret == NULL) {
[ ]  2302  	    xmlSAX2ErrMemory(ctxt, "xmlSAX2StartElementNs");
[ ]  2303  	    return;
[ ]  2304  	}
[B]  2305      }
[B]  2306      if (ctxt->linenumbers) {
[B]  2307  	if (ctxt->input != NULL) {
[B]  2308  	    if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
[B]  2309  		ret->line = ctxt->input->line;
[ ]  2310  	    else
[ ]  2311  	        ret->line = USHRT_MAX;
[B]  2312  	}
[B]  2313      }
[ ]  2314  
[B]  2315      if (parent == NULL) {
[B]  2316          xmlAddChild((xmlNodePtr) ctxt->myDoc, (xmlNodePtr) ret);
[B]  2317      }
[ ]  2318      /*
[ ]  2319       * Build the namespace list
[ ]  2320       */
[B]  2321      for (i = 0,j = 0;j < nb_namespaces;j++) {
[B]  2322          pref = namespaces[i++];
[B]  2323  	uri = namespaces[i++];
[B]  2324  	ns = xmlNewNs(NULL, uri, pref);
[B]  2325  	if (ns != NULL) {
[B]  2326  	    if (last == NULL) {
[B]  2327  	        ret->nsDef = last = ns;
[B]  2328  	    } else {
[ ]  2329  	        last->next = ns;
[ ]  2330  		last = ns;
[ ]  2331  	    }
[B]  2332  	    if ((URI != NULL) && (prefix == pref)) <-- BLOCKER
[W]  2333  		ret->ns = ns;
[B]  2334  	} else {
[ ]  2335              /*
[ ]  2336               * any out of memory error would already have been raised
[ ]  2337               * but we can't be guaranteed it's the actual error due to the
[ ]  2338               * API, best is to skip in this case
[ ]  2339               */
[ ]  2340  	    continue;
[ ]  2341  	}
[B]  2342  #ifdef LIBXML_VALID_ENABLED
[B]  2343  	if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
[B]  2344  	    ctxt->myDoc && ctxt->myDoc->intSubset) {
[L]  2345  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc,
[L]  2346  	                                           ret, prefix, ns, uri);
[L]  2347  	}
[B]  2348  #endif /* LIBXML_VALID_ENABLED */
[B]  2349      }
[B]  2350      ctxt->nodemem = -1;
[ ]  2351  
[ ]  2352      /*
[ ]  2353       * We are parsing a new node.
[ ]  2354       */
[B]  2355      if (nodePush(ctxt, ret) < 0) {
[ ]  2356          xmlUnlinkNode(ret);
[ ]  2357          xmlFreeNode(ret);
[ ]  2358          return;
[ ]  2359      }
[ ]  2360  
[ ]  2361      /*
[ ]  2362       * Link the child element
[ ]  2363       */
[B]  2364      if (parent != NULL) {
[B]  2365          if (parent->type == XML_ELEMENT_NODE) {
[B]  2366  	    xmlAddChild(parent, ret);
[B]  2367  	} else {
[ ]  2368  	    xmlAddSibling(parent, ret);
[ ]  2369  	}
[B]  2370      }
[ ]  2371  
[ ]  2372      /*
[ ]  2373       * Insert the defaulted attributes from the DTD only if requested:
[ ]  2374       */
[B]  2375      if ((nb_defaulted != 0) &&
[B]  2376          ((ctxt->loadsubset & XML_COMPLETE_ATTRS) == 0))
[L]  2377  	nb_attributes -= nb_defaulted;
[ ]  2378  
[ ]  2379      /*
[ ]  2380       * Search the namespace if it wasn't already found
[ ]  2381       * Note that, if prefix is NULL, this searches for the default Ns
[ ]  2382       */
[B]  2383      if ((URI != NULL) && (ret->ns == NULL)) {
[ ]  2384          ret->ns = xmlSearchNs(ctxt->myDoc, parent, prefix);
[ ]  2385  	if ((ret->ns == NULL) && (xmlStrEqual(prefix, BAD_CAST "xml"))) {
[ ]  2386  	    ret->ns = xmlSearchNs(ctxt->myDoc, ret, prefix);
[ ]  2387  	}
[ ]  2388  	if (ret->ns == NULL) {
[ ]  2389  	    ns = xmlNewNs(ret, NULL, prefix);
[ ]  2390  	    if (ns == NULL) {
[ ]  2391  
[ ]  2392  	        xmlSAX2ErrMemory(ctxt, "xmlSAX2StartElementNs");
[ ]  2393  		return;
[ ]  2394  	    }
[ ]  2395              if (prefix != NULL)
[ ]  2396                  xmlNsWarnMsg(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[ ]  2397                               "Namespace prefix %s was not found\n",
[ ]  2398                               prefix, NULL);
[ ]  2399              else
[ ]  2400                  xmlNsWarnMsg(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[ ]  2401                               "Namespace default prefix was not found\n",
[ ]  2402                               NULL, NULL);
[ ]  2403  	}
[ ]  2404      }
[ ]  2405  
[ ]  2406      /*
[ ]  2407       * process all the other attributes
[ ]  2408       */
[B]  2409      if (nb_attributes > 0) {
[L]  2410          for (j = 0,i = 0;i < nb_attributes;i++,j+=5) {
[ ]  2411  	    /*
[ ]  2412  	     * Handle the rare case of an undefined attribute prefix
[ ]  2413  	     */
[L]  2414  	    if ((attributes[j+1] != NULL) && (attributes[j+2] == NULL)) {
[L]  2415  		if (ctxt->dictNames) {
[L]  2416  		    const xmlChar *fullname;
[ ]  2417  
[L]  2418  		    fullname = xmlDictQLookup(ctxt->dict, attributes[j+1],
[L]  2419  		                              attributes[j]);
[L]  2420  		    if (fullname != NULL) {
[L]  2421  			xmlSAX2AttributeNs(ctxt, fullname, NULL,
[L]  2422  			                   attributes[j+3], attributes[j+4]);
[L]  2423  		        continue;
[L]  2424  		    }
[L]  2425  		} else {
[ ]  2426  		    lname = xmlBuildQName(attributes[j], attributes[j+1],
[ ]  2427  		                          NULL, 0);
[ ]  2428  		    if (lname != NULL) {
[ ]  2429  			xmlSAX2AttributeNs(ctxt, lname, NULL,
[ ]  2430  			                   attributes[j+3], attributes[j+4]);
[ ]  2431  			xmlFree(lname);
[ ]  2432  		        continue;
[ ]  2433  		    }
[ ]  2434  		}
[L]  2435  	    }
[L]  2436  	    xmlSAX2AttributeNs(ctxt, attributes[j], attributes[j+1],
[L]  2437  			       attributes[j+3], attributes[j+4]);
[L]  2438  	}
[L]  2439      }
[ ]  2440  
[B]  2441  #ifdef LIBXML_VALID_ENABLED
[ ]  2442      /*
[ ]  2443       * If it's the Document root, finish the DTD validation and
[ ]  2444       * check the document root element for validity
[ ]  2445       */
[B]  2446      if ((ctxt->validate) &&
[B]  2447          ((ctxt->vctxt.flags & XML_VCTXT_DTD_VALIDATED) == 0)) {
[L]  2448  	int chk;
[ ]  2449  
[L]  2450  	chk = xmlValidateDtdFinal(&ctxt->vctxt, ctxt->myDoc);
[L]  2451  	if (chk <= 0)
[ ]  2452  	    ctxt->valid = 0;
[L]  2453  	if (chk < 0)
[ ]  2454  	    ctxt->wellFormed = 0;
[L]  2455  	ctxt->valid &= xmlValidateRoot(&ctxt->vctxt, ctxt->myDoc);
[L]  2456  	ctxt->vctxt.flags |= XML_VCTXT_DTD_VALIDATED;
[L]  2457      }
[B]  2458  #endif /* LIBXML_VALID_ENABLED */
[B]  2459  }

--- No 1-hop callers of xmlSAX2StartElementNs fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      16       146  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
       3        96  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758)
      24       112  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      24       112  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
       6        66  xmlSAX2ElementDecl  (/src/libxml2/SAX2.c:772-807)
      15        72  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)  <-- enclosing
       8        56  xmlSAX2EndElementNs  (/src/libxml2/SAX2.c:2476-2502)
       0        45  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199)
       8        44  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
       3        33  xmlSAX2InternalSubset  (/src/libxml2/SAX2.c:330-354)
       3        33  xmlSAX2ExternalSubset  (/src/libxml2/SAX2.c:368-496)
       3        33  xmlSAX2ResolveEntity  (/src/libxml2/SAX2.c:514-538)
       6        33  xmlSAX2SetDocumentLocator  (/src/libxml2/SAX2.c:942-948)
       6        33  xmlSAX2StartDocument  (/src/libxml2/SAX2.c:958-1013)
       4        26  xmlSAX2EndDocument  (/src/libxml2/SAX2.c:1023-1054)
... (1 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459) ---
  d=1   L2237  T=0 F=15  T=0 F=72  if (ctx == NULL) return;
  d=1   L2242  T=0 F=15  T=30 F=42  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=1   L2242  T=0 F=0  T=0 F=30  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=1   L2256  T=0 F=15  T=0 F=72  if ((prefix != NULL) && (URI == NULL)) {
  d=1   L2270  T=0 F=15  T=0 F=72  if (ctxt->freeElems != NULL) {
  d=1   L2293  T=15 F=0  T=60 F=12  if (ctxt->dictNames)
  d=1   L2296  T=0 F=0  T=12 F=0  else if (lname == NULL)
  d=1   L2301  T=0 F=15  T=0 F=72  if (ret == NULL) {
  d=1   L2306  T=15 F=0  T=72 F=0  if (ctxt->linenumbers) {
  d=1   L2307  T=15 F=0  T=72 F=0  if (ctxt->input != NULL) {
  d=1   L2308  T=15 F=0  T=72 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=1   L2315  T=6 F=9  T=33 F=39  if (parent == NULL) {
  d=1   L2321  T=6 F=15  T=33 F=72  for (i = 0,j = 0;j < nb_namespaces;j++) {
  d=1   L2325  T=6 F=0  T=33 F=0  if (ns != NULL) {
  d=1   L2326  T=6 F=0  T=33 F=0  if (last == NULL) {
  d=1   L2332  T=6 F=0  T=0 F=0  if ((URI != NULL) && (prefix == pref))  <-- BLOCKER
  d=1   L2332  T=6 F=0  T=0 F=33  if ((URI != NULL) && (prefix == pref))  <-- BLOCKER
  d=1   L2343  T=0 F=6  T=12 F=21  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L2343  T=0 F=0  T=9 F=3  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L2343  T=6 F=0  T=33 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L2344  T=0 F=0  T=9 F=0  ctxt->myDoc && ctxt->myDoc->intSubset) {
  d=1   L2344  T=0 F=0  T=9 F=0  ctxt->myDoc && ctxt->myDoc->intSubset) {
  d=1   L2355  T=0 F=15  T=0 F=72  if (nodePush(ctxt, ret) < 0) {
  d=1   L2364  T=9 F=6  T=39 F=33  if (parent != NULL) {
  d=1   L2365  T=9 F=0  T=39 F=0  if (parent->type == XML_ELEMENT_NODE) {
  d=1   L2375  T=0 F=15  T=30 F=42  if ((nb_defaulted != 0) &&
  d=1   L2376  T=0 F=0  T=15 F=15  ((ctxt->loadsubset & XML_COMPLETE_ATTRS) == 0))
  d=1   L2383  T=0 F=6  T=0 F=0  if ((URI != NULL) && (ret->ns == NULL)) {
  d=1   L2383  T=6 F=9  T=0 F=72  if ((URI != NULL) && (ret->ns == NULL)) {
  d=1   L2409  T=0 F=15  T=33 F=39  if (nb_attributes > 0) {
  d=1   L2410  T=0 F=0  T=45 F=33  for (j = 0,i = 0;i < nb_attributes;i++,j+=5) {
  d=1   L2414  T=0 F=0  T=18 F=21  if ((attributes[j+1] != NULL) && (attributes[j+2] == NULL...
  d=1   L2414  T=0 F=0  T=39 F=6  if ((attributes[j+1] != NULL) && (attributes[j+2] == NULL...
  d=1   L2415  T=0 F=0  T=18 F=0  if (ctxt->dictNames) {
  d=1   L2420  T=0 F=0  T=18 F=0  if (fullname != NULL) {
  d=1   L2446  T=0 F=15  T=30 F=42  if ((ctxt->validate) &&
  d=1   L2447  T=0 F=0  T=12 F=18  ((ctxt->vctxt.flags & XML_VCTXT_DTD_VALIDATED) == 0)) {
  d=1   L2451  T=0 F=0  T=0 F=12  if (chk <= 0)
  d=1   L2453  T=0 F=0  T=0 F=12  if (chk < 0)

[off-chain: 147 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=fc953d92fc9cf938, size=368 bytes, fuzzer=value_profile_cmplog, trial=3, discovered_at=3665s, mutation_op=ByteAddMutator,BytesSetMutator,ByteDecMutator,WordInterestingMutator):
  0000: 05 00 04 00 31 28 28 28 37 32 2e 78 6d 6c 5c 0a   ....1(((72.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=6d4e408dfb9b247b, size=277 bytes, fuzzer=value_profile_cmplog, trial=3, discovered_at=85665s, mutation_op=BytesDeleteMutator,CrossoverInsertMutator,BytesCopyMutator,BytesDeleteMutator,BytesInsertMutator,QwordAddMutator,WordAddMutator):
  0000: 45 44 20 27 73 69 6d 70 6c 65 27 0a 20 20 20 20   ED 'simple'.    
  0010: 20 20 20 20 20 20 20 20 00 6c 69 00 6b 2d 68 72           .li.k-hr
  0020: 65 66 20 20 20 43 44 41 54 41 20 20 20 20 78 6c   ef   CDATA    xl
  0030: 69 6e 6b 3a 68 72 65 66 25 20 20 43 44 41 54 41   ink:href%  CDATA

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00f7af173db700b0, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=0s, mutation_op=BytesExpandMutator,DwordAddMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=743a758b7f4e28eb, size=368 bytes, fuzzer=cmplog, trial=3, discovered_at=0s):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=5f83308a4d472d74, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=10s, mutation_op=ByteRandMutator,ByteDecMutator,ByteInterestingMutator,ByteRandMutator,BytesSwapMutator,ByteAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=a0f1e597ae5a2ec0, size=370 bytes, fuzzer=cmplog, trial=3, discovered_at=18s, mutation_op=BytesExpandMutator):
  0000: 06 00 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c   ......127772.xml
  0010: 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d   \.<?xml version=
  0020: 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50   "1.0"?>.<!DOCTYP
  0030: 45 20 61 20 53 59 53 54 45 4d 20 22 64 74 64 73   E a SYSTEM "dtds
Seed 5 (id=205285e62aa555ce, size=368 bytes, fuzzer=cmplog, trial=3, discovered_at=1952s, mutation_op=BytesDeleteMutator,TokenReplace,BytesExpandMutator,ByteInterestingMutator,ByteFlipMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  05(.)x1 45(E)x1                     06(.)x5 fa(.)x2 2b(+)x2 f9(.)x1 +1u  DIFFER
   0x0001  00(.)x1 44(D)x1                     00(.)x10 30(0)x1                    PARTIAL
   0x0002  04(.)x1 20( )x1                     00(.)x9 06(.)x1 30(0)x1             DIFFER
   0x0003  00(.)x1 27(')x1                     00(.)x10 30(0)x1                    PARTIAL
   0x0004  31(1)x1 73(s)x1                     31(1)x9 00(.)x1 30(0)x1             PARTIAL
   0x0005  28(()x1 69(i)x1                     32(2)x10 00(.)x1                    DIFFER
   0x0006  28(()x1 6d(m)x1                     37(7)x10 31(1)x1                    DIFFER
   0x0007  28(()x1 70(p)x1                     37(7)x10 32(2)x1                    DIFFER
   0x0008  37(7)x1 6c(l)x1                     37(7)x11                            PARTIAL
   0x0009  32(2)x1 65(e)x1                     32(2)x10 37(7)x1                    PARTIAL
   0x000a  2e(.)x1 27(')x1                     2e(.)x10 37(7)x1                    PARTIAL
   0x000b  78(x)x1 0a(.)x1                     78(x)x10 32(2)x1                    PARTIAL
   0x000c  6d(m)x1 20( )x1                     6d(m)x10 2e(.)x1                    PARTIAL
   0x000d  6c(l)x1 20( )x1                     6c(l)x10 78(x)x1                    PARTIAL
   0x000e  5c(\)x1 20( )x1                     5c(\)x10 6d(m)x1                    PARTIAL
   0x000f  0a(.)x1 20( )x1                     0a(.)x10 6c(l)x1                    PARTIAL
   0x0010  3c(<)x1 20( )x1                     3c(<)x10 5c(\)x1                    PARTIAL
   0x0011  3f(?)x1 20( )x1                     3f(?)x10 0a(.)x1                    PARTIAL
   0x0012  78(x)x1 20( )x1                     78(x)x10 3c(<)x1                    PARTIAL
   0x0013  6d(m)x1 20( )x1                     6d(m)x10 3f(?)x1                    PARTIAL
   0x0014  6c(l)x1 20( )x1                     6c(l)x10 78(x)x1                    PARTIAL
   0x0015  20( )x2                             20( )x10 6d(m)x1                    PARTIAL
   0x0016  76(v)x1 20( )x1                     76(v)x10 6c(l)x1                    PARTIAL
   0x0018  72(r)x1 00(.)x1                     72(r)x10 76(v)x1                    PARTIAL
   0x0019  73(s)x1 6c(l)x1                     73(s)x10 65(e)x1                    PARTIAL
   0x001a  69(i)x2                             69(i)x10 72(r)x1                    PARTIAL
   0x001b  6f(o)x1 00(.)x1                     6f(o)x10 73(s)x1                    PARTIAL
   0x001c  6e(n)x1 6b(k)x1                     6e(n)x10 69(i)x1                    PARTIAL
   0x001d  3d(=)x1 2d(-)x1                     3d(=)x10 6f(o)x1                    PARTIAL
   0x001e  22(")x1 68(h)x1                     22(")x10 6e(n)x1                    PARTIAL
   0x001f  31(1)x1 72(r)x1                     31(1)x10 3d(=)x1                    PARTIAL
   0x0020  2e(.)x1 65(e)x1                     2e(.)x10 22(")x1                    PARTIAL
   0x0021  30(0)x1 66(f)x1                     30(0)x10 31(1)x1                    PARTIAL
   0x0022  22(")x1 20( )x1                     22(")x10 2e(.)x1                    PARTIAL
   0x0023  3f(?)x1 20( )x1                     3f(?)x10 30(0)x1                    PARTIAL
   0x0024  3e(>)x1 20( )x1                     3e(>)x10 22(")x1                    PARTIAL
   0x0025  0a(.)x1 43(C)x1                     0a(.)x10 3f(?)x1                    PARTIAL
   0x0026  3c(<)x1 44(D)x1                     3c(<)x10 3e(>)x1                    PARTIAL
   0x0027  21(!)x1 41(A)x1                     21(!)x10 0a(.)x1                    PARTIAL
   0x0028  44(D)x1 54(T)x1                     44(D)x10 3c(<)x1                    PARTIAL
   ... (22 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7451.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7451,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7451 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7451 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7451 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).