==== BLOCKER ====
Target: libxml2
Branch ID: 7459
Location: /src/libxml2/SAX2.c:2383:9
Enclosing function: xmlSAX2StartElementNs
Source line:     if ((URI != NULL) && (ret->ns == NULL)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           0       10          0  loser (value_profile vs value_profile_cmplog)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                        3        7          0  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             3        7          0  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=9.60h  loser=24.00h
  avg hitcount on branch: winner=8  loser=0
  prob_div=0.90  dur_div=14.40h  hit_div=8
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7459/{W,L}/branch_coverage_show.txt

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
[L]  2244  	 ((ctxt->myDoc->intSubset->notations == NULL) &&
[L]  2245  	  (ctxt->myDoc->intSubset->elements == NULL) &&
[L]  2246  	  (ctxt->myDoc->intSubset->attributes == NULL) &&
[L]  2247  	  (ctxt->myDoc->intSubset->entities == NULL)))) {
[L]  2248  	xmlErrValid(ctxt, XML_DTD_NO_DTD,
[L]  2249  	  "Validation failed: no DTD found !", NULL, NULL);
[L]  2250  	ctxt->validate = 0;
[L]  2251      }
[ ]  2252  
[ ]  2253      /*
[ ]  2254       * Take care of the rare case of an undefined namespace prefix
[ ]  2255       */
[B]  2256      if ((prefix != NULL) && (URI == NULL)) {
[L]  2257          if (ctxt->dictNames) {
[L]  2258  	    const xmlChar *fullname;
[ ]  2259  
[L]  2260  	    fullname = xmlDictQLookup(ctxt->dict, prefix, localname);
[L]  2261  	    if (fullname != NULL)
[L]  2262  	        localname = fullname;
[L]  2263  	} else {
[L]  2264  	    lname = xmlBuildQName(localname, prefix, NULL, 0);
[L]  2265  	}
[L]  2266      }
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
[L]  2298  	else
[L]  2299  	    ret = xmlNewDocNodeEatName(ctxt->myDoc, NULL,
[L]  2300  	                               (xmlChar *) lname, NULL);
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
[B]  2332  	    if ((URI != NULL) && (prefix == pref))
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
[ ]  2345  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc,
[ ]  2346  	                                           ret, prefix, ns, uri);
[ ]  2347  	}
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
[B]  2383      if ((URI != NULL) && (ret->ns == NULL)) { <-- BLOCKER
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
[ ]  2436  	    xmlSAX2AttributeNs(ctxt, attributes[j], attributes[j+1],
[ ]  2437  			       attributes[j+3], attributes[j+4]);
[ ]  2438  	}
[L]  2439      }
[ ]  2440  
[B]  2441  #ifdef LIBXML_VALID_ENABLED
[ ]  2442      /*
[ ]  2443       * If it's the Document root, finish the DTD validation and
[ ]  2444       * check the document root element for validity
[ ]  2445       */
[B]  2446      if ((ctxt->validate) &&
[B]  2447          ((ctxt->vctxt.flags & XML_VCTXT_DTD_VALIDATED) == 0)) {
[ ]  2448  	int chk;
[ ]  2449  
[ ]  2450  	chk = xmlValidateDtdFinal(&ctxt->vctxt, ctxt->myDoc);
[ ]  2451  	if (chk <= 0)
[ ]  2452  	    ctxt->valid = 0;
[ ]  2453  	if (chk < 0)
[ ]  2454  	    ctxt->wellFormed = 0;
[ ]  2455  	ctxt->valid &= xmlValidateRoot(&ctxt->vctxt, ctxt->myDoc);
[ ]  2456  	ctxt->vctxt.flags |= XML_VCTXT_DTD_VALIDATED;
[ ]  2457      }
[B]  2458  #endif /* LIBXML_VALID_ENABLED */
[B]  2459  }

--- No 1-hop callers of xmlSAX2StartElementNs fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      24       327  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      24       327  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
      15       161  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)  <-- enclosing
       8       120  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
      16       127  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
       6        90  xmlSAX2SetDocumentLocator  (/src/libxml2/SAX2.c:942-948)
       6        90  xmlSAX2StartDocument  (/src/libxml2/SAX2.c:958-1013)
       4        62  xmlSAX2EndDocument  (/src/libxml2/SAX2.c:1023-1054)
       3        51  xmlSAX2InternalSubset  (/src/libxml2/SAX2.c:330-354)
       3        51  xmlSAX2ExternalSubset  (/src/libxml2/SAX2.c:368-496)
       3        48  xmlSAX2ResolveEntity  (/src/libxml2/SAX2.c:514-538)
       8        29  xmlSAX2EndElementNs  (/src/libxml2/SAX2.c:2476-2502)
       0        16  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199)
       3        18  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758)
       0        12  SAX2.c:xmlErrValid  (/src/libxml2/SAX2.c:99-124)
... (4 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459) ---
  d=1   L2237  T=0 F=15  T=0 F=161  if (ctx == NULL) return;
  d=1   L2242  T=0 F=15  T=12 F=149  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=1   L2242  T=0 F=0  T=12 F=0  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=1   L2243  T=0 F=0  T=6 F=6  ((ctxt->myDoc->intSubset == NULL) ||
  d=1   L2244  T=0 F=0  T=6 F=0  ((ctxt->myDoc->intSubset->notations == NULL) &&
  d=1   L2245  T=0 F=0  T=6 F=0  (ctxt->myDoc->intSubset->elements == NULL) &&
  d=1   L2246  T=0 F=0  T=6 F=0  (ctxt->myDoc->intSubset->attributes == NULL) &&
  d=1   L2247  T=0 F=0  T=6 F=0  (ctxt->myDoc->intSubset->entities == NULL)))) {
  d=1   L2256  T=0 F=0  T=9 F=0  if ((prefix != NULL) && (URI == NULL)) {
  d=1   L2256  T=0 F=15  T=9 F=152  if ((prefix != NULL) && (URI == NULL)) {
  d=1   L2257  T=0 F=0  T=6 F=3  if (ctxt->dictNames) {
  d=1   L2261  T=0 F=0  T=6 F=0  if (fullname != NULL)
  d=1   L2270  T=0 F=15  T=0 F=161  if (ctxt->freeElems != NULL) {
  d=1   L2293  T=15 F=0  T=131 F=30  if (ctxt->dictNames)
  d=1   L2296  T=0 F=0  T=27 F=3  else if (lname == NULL)
  d=1   L2301  T=0 F=15  T=0 F=161  if (ret == NULL) {
  d=1   L2306  T=15 F=0  T=161 F=0  if (ctxt->linenumbers) {
  d=1   L2307  T=15 F=0  T=161 F=0  if (ctxt->input != NULL) {
  d=1   L2308  T=15 F=0  T=161 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=1   L2315  T=6 F=9  T=98 F=63  if (parent == NULL) {
  d=1   L2321  T=6 F=15  T=3 F=161  for (i = 0,j = 0;j < nb_namespaces;j++) {
  d=1   L2325  T=6 F=0  T=3 F=0  if (ns != NULL) {
  d=1   L2326  T=6 F=0  T=3 F=0  if (last == NULL) {
  d=1   L2332  T=6 F=0  T=0 F=0  if ((URI != NULL) && (prefix == pref))
  d=1   L2332  T=6 F=0  T=0 F=3  if ((URI != NULL) && (prefix == pref))
  d=1   L2343  T=0 F=6  T=0 F=3  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L2343  T=6 F=0  T=3 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L2355  T=0 F=15  T=0 F=161  if (nodePush(ctxt, ret) < 0) {
  d=1   L2364  T=9 F=6  T=63 F=98  if (parent != NULL) {
  d=1   L2365  T=9 F=0  T=63 F=0  if (parent->type == XML_ELEMENT_NODE) {
  d=1   L2375  T=0 F=15  T=3 F=158  if ((nb_defaulted != 0) &&
  d=1   L2376  T=0 F=0  T=3 F=0  ((ctxt->loadsubset & XML_COMPLETE_ATTRS) == 0))
  d=1   L2383  T=0 F=6  T=0 F=0  if ((URI != NULL) && (ret->ns == NULL)) {  <-- BLOCKER
  d=1   L2383  T=6 F=9  T=0 F=161  if ((URI != NULL) && (ret->ns == NULL)) {  <-- BLOCKER
  d=1   L2409  T=0 F=15  T=16 F=145  if (nb_attributes > 0) {
  d=1   L2410  T=0 F=0  T=16 F=16  for (j = 0,i = 0;i < nb_attributes;i++,j+=5) {
  d=1   L2414  T=0 F=0  T=16 F=0  if ((attributes[j+1] != NULL) && (attributes[j+2] == NULL...
  d=1   L2414  T=0 F=0  T=16 F=0  if ((attributes[j+1] != NULL) && (attributes[j+2] == NULL...
  d=1   L2415  T=0 F=0  T=13 F=3  if (ctxt->dictNames) {
  d=1   L2420  T=0 F=0  T=13 F=0  if (fullname != NULL) {
  d=1   L2428  T=0 F=0  T=3 F=0  if (lname != NULL) {
  d=1   L2446  T=0 F=15  T=0 F=161  if ((ctxt->validate) &&

[off-chain: 159 additional divergent branches across 16 functions (see HIT-COUNT DIVERGENCE for which functions)]

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
Seed 2 (id=011bb1a41b201f9b, size=327 bytes, fuzzer=cmplog, trial=2, discovered_at=5s, mutation_op=BitFlipMutator,BytesDeleteMutator,ByteRandMutator,WordAddMutator,BytesInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2c 6c   a SYSTEM "dtds,l
Seed 3 (id=01072d783399b6ec, size=456 bytes, fuzzer=cmplog, trial=3, discovered_at=7s, mutation_op=BitFlipMutator,BytesRandSetMutator,ByteDecMutator,BytesDeleteMutator,WordInterestingMutator,WordInterestingMutator,BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=026d5e573bace2aa, size=368 bytes, fuzzer=cmplog, trial=3, discovered_at=10s, mutation_op=BytesRandSetMutator,CrossoverReplaceMutator,ByteInterestingMutator,ByteInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=01986dbadd87a561, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=128s, mutation_op=ByteDecMutator,CrossoverReplaceMutator,BytesRandInsertMutator,ByteAddMutator,ByteAddMutator,CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  05(.)x1 45(E)x1                     06(.)x11 4d(M)x4 45(E)x2 37(7)x1 +12u  PARTIAL
   0x0001  00(.)x1 44(D)x1                     00(.)x13 45(E)x2 54(T)x2 50(P)x2 +11u  PARTIAL
   0x0002  04(.)x1 20( )x1                     00(.)x13 45(E)x2 6c(l)x2 20( )x2 +10u  PARTIAL
   0x0003  00(.)x1 27(')x1                     00(.)x15 65(e)x2 62(b)x2 68(h)x2 +9u  PARTIAL
   0x0004  31(1)x1 73(s)x1                     31(1)x13 00(.)x3 20( )x2 45(E)x2 +9u  PARTIAL
   0x0005  28(()x1 69(i)x1                     32(2)x13 78(x)x3 74(t)x3 00(.)x3 +8u  DIFFER
   0x0006  28(()x1 6d(m)x1                     37(7)x13 20( )x2 6d(m)x2 70(p)x2 +10u  PARTIAL
   0x0007  28(()x1 70(p)x1                     37(7)x12 6c(l)x2 20( )x2 3a(:)x2 +11u  PARTIAL
   0x0008  37(7)x1 6c(l)x1                     37(7)x15 5c(\)x2 20( )x2 2f(/)x2 +9u  PARTIAL
   0x0009  32(2)x1 65(e)x1                     32(2)x13 2f(/)x3 37(7)x3 20( )x2 +9u  PARTIAL
   0x000a  2e(.)x1 27(')x1                     2e(.)x13 43(C)x2 20( )x2 77(w)x2 +10u  PARTIAL
   0x000b  78(x)x1 0a(.)x1                     78(x)x14 20( )x3 77(w)x2 32(2)x2 +9u  PARTIAL
   0x000c  6d(m)x1 20( )x1                     6d(m)x11 77(w)x3 78(x)x2 45(E)x2 +10u  PARTIAL
   0x000d  6c(l)x1 20( )x1                     6c(l)x13 20( )x3 78(x)x2 54(T)x1 +11u  PARTIAL
   0x000e  5c(\)x1 20( )x1                     5c(\)x13 20( )x3 6d(m)x2 41(A)x1 +11u  PARTIAL
   0x000f  0a(.)x1 20( )x1                     0a(.)x14 20( )x3 6c(l)x2 29())x1 +10u  PARTIAL
   0x0010  3c(<)x1 20( )x1                     3c(<)x13 20( )x3 6c(l)x2 27(')x2 +9u  PARTIAL
   0x0011  3f(?)x1 20( )x1                     3f(?)x12 0a(.)x4 20( )x3 2e(.)x2 +9u  PARTIAL
   0x0012  78(x)x1 20( )x1                     78(x)x13 3c(<)x3 72(r)x1 73(s)x1 +12u  PARTIAL
   0x0013  6d(m)x1 20( )x1                     6d(m)x12 3a(:)x2 64(d)x2 21(!)x1 +13u  PARTIAL
   0x0014  6c(l)x1 20( )x1                     6c(l)x12 78(x)x4 41(A)x2 69(i)x2 +9u  PARTIAL
   0x0015  20( )x2                             20( )x12 54(T)x2 6c(l)x2 00(.)x2 +10u  PARTIAL
   0x0016  76(v)x1 20( )x1                     76(v)x12 69(i)x2 6c(l)x2 54(T)x1 +13u  PARTIAL
   0x0017  65(e)x1 20( )x1                     65(e)x11 6e(n)x2 0d(.)x2 4c(L)x1 +14u  PARTIAL
   0x0018  72(r)x1 00(.)x1                     72(r)x11 20( )x2 f6(.)x2 49(I)x1 +14u  PARTIAL
   0x0019  73(s)x1 6c(l)x1                     73(s)x12 84(.)x2 3e(>)x1 31(1)x1 +14u  PARTIAL
   0x001a  69(i)x2                             69(i)x11 20( )x2 65(e)x2 84(.)x2 +13u  PARTIAL
   0x001b  6f(o)x1 00(.)x1                     6f(o)x11 20( )x2 2e(.)x2 3c(<)x2 +12u  PARTIAL
   0x001c  6e(n)x1 6b(k)x1                     6e(n)x11 20( )x2 74(t)x2 62(b)x1 +14u  PARTIAL
   0x001d  3d(=)x1 2d(-)x1                     3d(=)x11 20( )x2 41(A)x2 74(t)x2 +12u  PARTIAL
   0x001e  22(")x1 68(h)x1                     22(")x11 20( )x3 78(x)x1 3e(>)x1 +14u  PARTIAL
   0x001f  31(1)x1 72(r)x1                     31(1)x11 0a(.)x3 20( )x2 27(')x2 +12u  PARTIAL
   0x0020  2e(.)x1 65(e)x1                     2e(.)x12 3c(<)x2 2f(/)x2 20( )x2 +12u  PARTIAL
   0x0021  30(0)x1 66(f)x1                     30(0)x11 21(!)x3 6e(n)x2 20( )x1 +13u  PARTIAL
   0x0022  22(")x1 20( )x1                     22(")x11 44(D)x2 20( )x2 73(s)x1 +14u  PARTIAL
   0x0023  3f(?)x1 20( )x1                     3f(?)x11 72(r)x2 41(A)x2 3a(:)x1 +14u  PARTIAL
   0x0024  3e(>)x1 20( )x1                     3e(>)x11 20( )x2 06(.)x2 27(')x2 +13u  PARTIAL
   0x0025  0a(.)x1 43(C)x1                     0a(.)x11 23(#)x2 00(.)x2 3d(=)x2 +13u  PARTIAL
   0x0026  3c(<)x1 44(D)x1                     3c(<)x11 20( )x2 74(t)x2 69(i)x1 +14u  PARTIAL
   0x0027  21(!)x1 41(A)x1                     21(!)x12 00(.)x3 6e(n)x2 64(d)x2 +11u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7459.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7459,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7459 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7459 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7459 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).