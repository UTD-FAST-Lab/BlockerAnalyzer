==== BLOCKER ====
Target: libxml2
Branch ID: 6483
Location: /src/libxml2/parser.c:3013:21
Enclosing function: xmlSplitQName
Source line: 	while ((c != 0) && (c != ':')) { /* tested bigname.xml */
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ctx_coverage vs naive_ctx)
cmplog                           0        7          3  REFERENCE
value_profile                    3        7          0  REFERENCE
value_profile_cmplog             1        9          0  REFERENCE
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     4        6          0  REFERENCE
mopt                             2        7          1  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             5        5          0  REFERENCE
grimoire                         2        5          3  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=10.20h  loser=9.70h
  avg hitcount on branch: winner=4  loser=2
  prob_div=0.60  dur_div=0.50h  hit_div=3
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6483/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlSplitQName (/src/libxml2/parser.c:2970-3118) ---
[ ]  2968  
[ ]  2969  xmlChar *
[B]  2970  xmlSplitQName(xmlParserCtxtPtr ctxt, const xmlChar *name, xmlChar **prefix) {
[B]  2971      xmlChar buf[XML_MAX_NAMELEN + 5];
[B]  2972      xmlChar *buffer = NULL;
[B]  2973      int len = 0;
[B]  2974      int max = XML_MAX_NAMELEN;
[B]  2975      xmlChar *ret = NULL;
[B]  2976      const xmlChar *cur = name;
[B]  2977      int c;
[ ]  2978  
[B]  2979      if (prefix == NULL) return(NULL);
[B]  2980      *prefix = NULL;
[ ]  2981  
[B]  2982      if (cur == NULL) return(NULL);
[ ]  2983  
[ ]  2984  #ifndef XML_XML_NAMESPACE
[ ]  2985      /* xml: prefix is not really a namespace */
[ ]  2986      if ((cur[0] == 'x') && (cur[1] == 'm') &&
[ ]  2987          (cur[2] == 'l') && (cur[3] == ':'))
[ ]  2988  	return(xmlStrdup(name));
[ ]  2989  #endif
[ ]  2990  
[ ]  2991      /* nasty but well=formed */
[B]  2992      if (cur[0] == ':')
[ ]  2993  	return(xmlStrdup(name));
[ ]  2994  
[B]  2995      c = *cur++;
[B]  2996      while ((c != 0) && (c != ':') && (len < max)) { /* tested bigname.xml */
[B]  2997  	buf[len++] = c;
[B]  2998  	c = *cur++;
[B]  2999      }
[B]  3000      if (len >= max) {
[ ]  3001  	/*
[ ]  3002  	 * Okay someone managed to make a huge name, so he's ready to pay
[ ]  3003  	 * for the processing speed.
[ ]  3004  	 */
[B]  3005  	max = len * 2;
[ ]  3006  
[B]  3007  	buffer = (xmlChar *) xmlMallocAtomic(max);
[B]  3008  	if (buffer == NULL) {
[ ]  3009  	    xmlErrMemory(ctxt, NULL);
[ ]  3010  	    return(NULL);
[ ]  3011  	}
[B]  3012  	memcpy(buffer, buf, len);
[B]  3013  	while ((c != 0) && (c != ':')) { /* tested bigname.xml */ <-- BLOCKER
[B]  3014  	    if (len + 10 > max) {
[B]  3015  	        xmlChar *tmp;
[ ]  3016  
[B]  3017  		max *= 2;
[B]  3018  		tmp = (xmlChar *) xmlRealloc(buffer, max);
[B]  3019  		if (tmp == NULL) {
[ ]  3020  		    xmlFree(buffer);
[ ]  3021  		    xmlErrMemory(ctxt, NULL);
[ ]  3022  		    return(NULL);
[ ]  3023  		}
[B]  3024  		buffer = tmp;
[B]  3025  	    }
[B]  3026  	    buffer[len++] = c;
[B]  3027  	    c = *cur++;
[B]  3028  	}
[B]  3029  	buffer[len] = 0;
[B]  3030      }
[ ]  3031  
[B]  3032      if ((c == ':') && (*cur == 0)) {
[W]  3033          if (buffer != NULL)
[W]  3034  	    xmlFree(buffer);
[W]  3035  	*prefix = NULL;
[W]  3036  	return(xmlStrdup(name));
[W]  3037      }
[ ]  3038  
[B]  3039      if (buffer == NULL)
[W]  3040  	ret = xmlStrndup(buf, len);
[B]  3041      else {
[B]  3042  	ret = buffer;
[B]  3043  	buffer = NULL;
[B]  3044  	max = XML_MAX_NAMELEN;
[B]  3045      }
[ ]  3046  
[ ]  3047  
[B]  3048      if (c == ':') {
[B]  3049  	c = *cur;
[B]  3050          *prefix = ret;
[B]  3051  	if (c == 0) {
[ ]  3052  	    return(xmlStrndup(BAD_CAST "", 0));
[ ]  3053  	}
[B]  3054  	len = 0;
[ ]  3055  
[ ]  3056  	/*
[ ]  3057  	 * Check that the first character is proper to start
[ ]  3058  	 * a new name
[ ]  3059  	 */
[B]  3060  	if (!(((c >= 0x61) && (c <= 0x7A)) ||
[B]  3061  	      ((c >= 0x41) && (c <= 0x5A)) ||
[B]  3062  	      (c == '_') || (c == ':'))) {
[L]  3063  	    int l;
[L]  3064  	    int first = CUR_SCHAR(cur, l);
[ ]  3065  
[L]  3066  	    if (!IS_LETTER(first) && (first != '_')) {
[L]  3067  		xmlFatalErrMsgStr(ctxt, XML_NS_ERR_QNAME,
[L]  3068  			    "Name %s is not XML Namespace compliant\n",
[L]  3069  				  name);
[L]  3070  	    }
[L]  3071  	}
[B]  3072  	cur++;
[ ]  3073  
[B]  3074  	while ((c != 0) && (len < max)) { /* tested bigname2.xml */
[B]  3075  	    buf[len++] = c;
[B]  3076  	    c = *cur++;
[B]  3077  	}
[B]  3078  	if (len >= max) {
[ ]  3079  	    /*
[ ]  3080  	     * Okay someone managed to make a huge name, so he's ready to pay
[ ]  3081  	     * for the processing speed.
[ ]  3082  	     */
[W]  3083  	    max = len * 2;
[ ]  3084  
[W]  3085  	    buffer = (xmlChar *) xmlMallocAtomic(max);
[W]  3086  	    if (buffer == NULL) {
[ ]  3087  	        xmlErrMemory(ctxt, NULL);
[ ]  3088  		return(NULL);
[ ]  3089  	    }
[W]  3090  	    memcpy(buffer, buf, len);
[W]  3091  	    while (c != 0) { /* tested bigname2.xml */
[W]  3092  		if (len + 10 > max) {
[ ]  3093  		    xmlChar *tmp;
[ ]  3094  
[ ]  3095  		    max *= 2;
[ ]  3096  		    tmp = (xmlChar *) xmlRealloc(buffer, max);
[ ]  3097  		    if (tmp == NULL) {
[ ]  3098  			xmlErrMemory(ctxt, NULL);
[ ]  3099  			xmlFree(buffer);
[ ]  3100  			return(NULL);
[ ]  3101  		    }
[ ]  3102  		    buffer = tmp;
[ ]  3103  		}
[W]  3104  		buffer[len++] = c;
[W]  3105  		c = *cur++;
[W]  3106  	    }
[W]  3107  	    buffer[len] = 0;
[W]  3108  	}
[ ]  3109  
[B]  3110  	if (buffer == NULL)
[B]  3111  	    ret = xmlStrndup(buf, len);
[W]  3112  	else {
[W]  3113  	    ret = buffer;
[W]  3114  	}
[B]  3115      }
[ ]  3116  
[B]  3117      return(ret);
[B]  3118  }

--- Caller (1 hop): xmlSAX2StartElement (/src/libxml2/SAX2.c:1603-1806, calls xmlSplitQName at line 1639) (±10 around call site) ---
[B]  1629  	  (ctxt->myDoc->intSubset->entities == NULL)))) {
[B]  1630  	xmlErrValid(ctxt, XML_ERR_NO_DTD,
[B]  1631  	  "Validation failed: no DTD found !", NULL, NULL);
[B]  1632  	ctxt->validate = 0;
[B]  1633      }
[ ]  1634  
[ ]  1635  
[ ]  1636      /*
[ ]  1637       * Split the full name into a namespace prefix and the tag name
[ ]  1638       */
[B]  1639      name = xmlSplitQName(ctxt, fullname, &prefix); <-- CALL
[ ]  1640  
[ ]  1641  
[ ]  1642      /*
[ ]  1643       * Note : the namespace resolution is deferred until the end of the
[ ]  1644       *        attributes parsing, since local namespace can be defined as
[ ]  1645       *        an attribute at this level.
[ ]  1646       */
[B]  1647      ret = xmlNewDocNodeEatName(ctxt->myDoc, NULL, name, NULL);
[B]  1648      if (ret == NULL) {
[ ]  1649          if (prefix != NULL)

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438, calls xmlSplitQName at line 1113)
hop 2  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758, calls xmlSplitQName at line 728)
hop 3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     234        56  xmlParseName  (/src/libxml2/parser.c:3368-3412)
     182        20  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
     179        47  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
     113        16  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
     113        16  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
     104        12  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
      72         0  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
      69         9  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600)
      71        12  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706)
      54         0  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
      53        12  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
      51        10  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942)
      37         0  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
      28         6  parser.c:xmlFatalErrMsgInt  (/src/libxml2/parser.c:572-586)
      20         0  parser.c:xmlSHRINK  (/src/libxml2/parser.c:2059-2066)
... (28 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591) ---
  d=3   L1454  T=0 F=0  T=3 F=0  if (elemDecl == NULL) {
  d=3   L1461  T=0 F=0  T=0 F=3  if (elemDecl != NULL) {
--- d=3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806) ---
  d=3   L1624  T=18 F=0  T=3 F=0  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=3   L1625  T=18 F=0  T=3 F=0  ((ctxt->myDoc->intSubset == NULL) ||
  d=3   L1659  T=13 F=33  T=3 F=0  } else if (parent == NULL) {
  d=3   L1690  T=46 F=0  T=0 F=3  if (parent->type == XML_ELEMENT_NODE) {
  d=3   L1711  T=0 F=64  T=3 F=39  if ((ctxt->myDoc->intSubset != NULL) ||
  d=3   L1719  T=3 F=61  T=0 F=42  if (atts != NULL) {
  d=3   L1723  T=3 F=0  T=0 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1723  T=3 F=3  T=0 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1724  T=0 F=3  T=0 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1740  T=19 F=0  T=6 F=0  if ((prefix != NULL) && (ns == NULL)) {
  d=3   L1751  T=0 F=19  T=0 F=6  if ((ns != NULL) && (ns->href != NULL) &&
  d=3   L1759  T=3 F=61  T=0 F=42  if (atts != NULL) {
  d=3   L1763  T=0 F=3  T=0 F=0  if (ctxt->html) {
  d=3   L1770  T=3 F=3  T=0 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1770  T=3 F=0  T=0 F=0  while ((att != NULL) && (value != NULL)) {
  d=3   L1771  T=3 F=0  T=0 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
--- d=2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=2   L1105  T=0 F=3  T=0 F=0  if (ctxt->html) {
  d=2   L1114  T=3 F=0  T=0 F=0  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1114  T=0 F=3  T=0 F=0  if ((name != NULL) && (name[0] == 0)) {
  d=2   L1131  T=0 F=3  T=0 F=0  if (name == NULL) {
  d=2   L1139  T=0 F=3  T=0 F=0  if ((ctxt->html) &&
  d=2   L1156  T=0 F=3  T=0 F=0  if (ctxt->vctxt.valid != 1) {
  d=2   L1159  T=0 F=3  T=0 F=0  if (nval != NULL)
  d=2   L1169  T=3 F=0  T=0 F=0  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1169  T=3 F=0  T=0 F=0  if ((!ctxt->html) && (ns == NULL) &&
  d=2   L1170  T=0 F=3  T=0 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=2   L1234  T=3 F=0  T=0 F=0  if ((!ctxt->html) &&
  d=2   L1235  T=0 F=3  T=0 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1303  T=0 F=3  T=0 F=0  if (ns != NULL) {
  d=2   L1338  T=0 F=3  T=0 F=0  if (ret == NULL)
  d=2   L1341  T=0 F=3  T=0 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1352  T=3 F=0  T=0 F=0  } else if (value != NULL) {
  d=2   L1355  T=3 F=0  T=0 F=0  if (ret->children != NULL)
  d=2   L1360  T=0 F=3  T=0 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1360  T=3 F=0  T=0 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1403  T=3 F=0  T=0 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=2   L1404  T=0 F=3  T=0 F=0  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=2   L1405  T=3 F=0  T=0 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1405  T=3 F=0  T=0 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=2   L1407  T=3 F=0  T=0 F=0  (ret->children != NULL) &&
  d=2   L1408  T=3 F=0  T=0 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=2   L1409  T=3 F=0  T=0 F=0  (ret->children->next == NULL)) {
  d=2   L1415  T=0 F=3  T=0 F=0  if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
  d=2   L1427  T=0 F=3  T=0 F=0  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
  d=2   L1429  T=0 F=3  T=0 F=0  else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
  d=2   L1434  T=0 F=3  T=0 F=0  if (nval != NULL)
  d=2   L1436  T=0 F=3  T=0 F=0  if (ns != NULL)
--- d=1  xmlSplitQName  (/src/libxml2/parser.c:2970-3118) ---
  d=1   L2996  T=2040 F=18  T=4200 F=42  while ((c != 0) && (c != ':') && (len < max)) { /* tested...
  d=1   L2996  T=2060 F=6  T=4240 F=0  while ((c != 0) && (c != ':') && (len < max)) { /* tested...
  d=1   L2996  T=2060 F=43  T=4240 F=0  while ((c != 0) && (c != ':') && (len < max)) { /* tested...
  d=1   L3000  T=18 F=49  T=42 F=0  if (len >= max) {
  d=1   L3008  T=0 F=18  T=0 F=42  if (buffer == NULL) {
  d=1   L3013  T=889 F=3  T=1840 F=36  while ((c != 0) && (c != ':')) { /* tested bigname.xml */  <-- BLOCKER
  d=1   L3013  T=874 F=15  T=1830 F=6  while ((c != 0) && (c != ':')) { /* tested bigname.xml */  <-- BLOCKER
  d=1   L3014  T=3 F=871  T=6 F=1830  if (len + 10 > max) {
  d=1   L3019  T=0 F=3  T=0 F=6  if (tmp == NULL) {
  d=1   L3032  T=2 F=19  T=0 F=6  if ((c == ':') && (*cur == 0)) {
  d=1   L3033  T=2 F=0  T=0 F=0  if (buffer != NULL)
  d=1   L3039  T=49 F=16  T=0 F=42  if (buffer == NULL)
  d=1   L3051  T=0 F=19  T=0 F=6  if (c == 0) {
  d=1   L3060  T=18 F=1  T=0 F=6  if (!(((c >= 0x61) && (c <= 0x7A)) ||
  d=1   L3060  T=18 F=0  T=0 F=0  if (!(((c >= 0x61) && (c <= 0x7A)) ||
  d=1   L3061  T=0 F=1  T=0 F=6  ((c >= 0x41) && (c <= 0x5A)) ||
  d=1   L3062  T=1 F=0  T=3 F=3  (c == '_') || (c == ':'))) {
  d=1   L3062  T=0 F=1  T=0 F=6  (c == '_') || (c == ':'))) {
  d=1   L3066  T=0 F=0  T=3 F=0  if (!IS_LETTER(first) && (first != '_')) {
  d=1   L3074  T=750 F=6  T=129 F=0  while ((c != 0) && (len < max)) { /* tested bigname2.xml */
  d=1   L3074  T=756 F=13  T=129 F=6  while ((c != 0) && (len < max)) { /* tested bigname2.xml */
  d=1   L3078  T=6 F=13  T=0 F=6  if (len >= max) {
  d=1   L3086  T=0 F=6  T=0 F=0  if (buffer == NULL) {
  d=1   L3091  T=180 F=6  T=0 F=0  while (c != 0) { /* tested bigname2.xml */
  d=1   L3092  T=0 F=180  T=0 F=0  if (len + 10 > max) {
  d=1   L3110  T=13 F=6  T=6 F=0  if (buffer == NULL)

[off-chain: 754 additional divergent branches across 65 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=03e5576b2c37e929, size=474 bytes, fuzzer=naive_ctx, trial=2, discovered_at=10969s, mutation_op=DwordAddMutator,ByteRandMutator,QwordAddMutator,CrossoverReplaceMutator):
  0000: 37 37 f4 2d 78 6d 6c 5c 0a 3c 6d 6c 20 76 45 c0   77.-xml\.<ml vE.
  0010: c0 c0 c0 c0 c0 c0 78 78 d7 ff ff ff ff ff ff ff   ......xx........
  0020: b2 b2 b2 b2 b2 b2 b2 b2 b2 b2 b5 b5 b5 b5 b5 b5   ................
  0030: b5 b5 26 26 3b 26 26 26 d9 4e 4e 40 4e 4e 4e 26   ..&&;&&&.NN@NNN&
Seed 2 (id=032eb8f1c3be6e9c, size=464 bytes, fuzzer=naive_ctx, trial=2, discovered_at=10975s, mutation_op=BytesSetMutator,CrossoverReplaceMutator):
  0000: 37 37 f4 2d 78 6d 6c 5c 0a 3c 6d 6c 20 76 45 c0   77.-xml\.<ml vE.
  0010: c0 c0 c0 c0 c0 c0 78 78 78 78 c0 c0 3d 3b 26 26   ......xxxx..=;&&
  0020: 26 d9 4e 4e 40 4e 4e 4e 26 66 61 6b 44 54 59 2e   &.NN@NNN&fakDTY.
  0030: 43 66 59 59 6c 0a 3c 72 72 72 72 72 72 72 72 72   CfYYl.<rrrrrrrrr
Seed 3 (id=a34dcefcc6f4c173, size=420 bytes, fuzzer=naive_ctx, trial=2, discovered_at=11143s, mutation_op=BytesRandSetMutator):
  0000: 37 37 f4 2d 78 6d 6c 5c 0a 3c 49 53 4f b5 b5 26   77.-xml\.<ISO..&
  0010: 26 3b 26 26 66 32 37 37 44 54 59 6e 43 54 5a 2e   &;&&f277DTYnCTZ.
  0020: 2e 2e 2e 2e 2e 2e 2d 2e 2e d1 2e 2e 2e 2e 66 61   ......-.......fa
  0030: 2e 2e 2e 66 61 2e 2e 6c 2e 43 c0 c0 c0 c0 83 55   ...fa..l.C.....U
Seed 4 (id=f4de14c0bb25be46, size=501 bytes, fuzzer=naive_ctx, trial=2, discovered_at=19435s, mutation_op=CrossoverReplaceMutator,ByteIncMutator,BytesRandSetMutator):
  0000: 37 37 f4 2d 78 6d 6c 5c 0a 3c 49 53 4f 2d 31 30   77.-xml\.<ISO-10
  0010: 36 34 36 2d 55 43 53 2d 32 6d 6c 20 76 45 c0 c0   646-UCS-2ml vE..
  0020: c0 c0 c0 c0 c0 79 78 78 78 c0 c0 3d 22 68 5b b2   .....yxxx..="h[.
  0030: b2 b2 b2 b2 b2 b2 4e b2 b2 b5 b5 b5 b5 b5 b5 b5   ......N.........
Seed 5 (id=5474353acbade675, size=757 bytes, fuzzer=naive_ctx, trial=2, discovered_at=69917s, mutation_op=ByteNegMutator,BytesCopyMutator,ByteFlipMutator,BytesInsertMutator,BytesSetMutator):
  0000: 3d 22 68 c1 c1 c1 c1 c1 c1 c1 c1 c1 74 74 70 3a   ="h.........ttp:
  0010: 2f 2f 66 61 66 61 6b 65 75 26 26 26 d9 26 26 26   //fafakeu&&&.&&&
  0020: 26 26 3d 23 68 74 74 70 3a 2f 2f 75 61 00 0f 00   &&=#http://ua...
  0030: 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d   \.<?xml version=

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=1a3a3db8872967a2, size=171 bytes, fuzzer=naive, trial=1, discovered_at=9550s, mutation_op=BytesInsertCopyMutator):
  0000: 2e 2e 2e 2e 2e 2e 20 28 73 69 93 20 6f 6c 65 29   ...... (si. ole)
  0010: 2f 62 2f 61 3e 0a 0a 2e 2e 2e 2e 40 2e 2e 2e d1   /b/a>......@....
  0020: 5c 0a 3c 52 78 75 6c 2e 2e 2e 2e 2e 2e 2e 6c 32   \.<Rxul.......l2
  0030: 2e 2e 2e 72 72 72 72 72 2e 2e 2e 72 72 72 72 72   ...rrrrr...rrrrr
Seed 2 (id=75cc2c9dd2e7e420, size=168 bytes, fuzzer=naive, trial=1, discovered_at=9550s, mutation_op=BytesCopyMutator,BytesInsertMutator,ByteDecMutator):
  0000: 2e 2e 2e 2e 2e 2e 20 28 73 69 93 20 6f 6c 65 29   ...... (si. ole)
  0010: 2f 62 2f 61 3e 0a 0a 2e 2e 2e 2e 40 2e 2e 2e d1   /b/a>......@....
  0020: 5c 0a 3c 52 78 75 6c 2e 2e 2e 2e 2e 2e 2e 6c 48   \.<Rxul.......lH
  0030: 48 2e 2e 2e 2e 2e 2e 2e 72 2e 2e 2e 2e 2e 4d 50   H.......r.....MP
Seed 3 (id=37b88dfb49bc97d7, size=193 bytes, fuzzer=naive, trial=1, discovered_at=9830s, mutation_op=ByteDecMutator,WordAddMutator,BytesInsertMutator,ByteInterestingMutator,ByteIncMutator,BytesCopyMutator):
  0000: 2f 2e 2e 2e 2e 2e 20 28 73 69 93 20 6f 6c 65 29   /..... (si. ole)
  0010: 2f 62 2f 61 3e 0a 0a 2e 31 2e 2e 40 2e 2e 2e d1   /b/a>...1..@....
  0020: 5c 0a 3c 52 78 75 6c 2e 2e 2e 2e 2e 2e 2e 6c 32   \.<Rxul.......l2
  0030: 2e 2e 2e 2e 2e 2e 72 72 72 72 72 72 72 72 72 50   ......rrrrrrrrrP
Seed 4 (id=5a77d06300a88775, size=178 bytes, fuzzer=naive, trial=1, discovered_at=9830s, mutation_op=BytesCopyMutator,ByteIncMutator):
  0000: 2e 2e 2e 2e 2e 2e 20 28 73 69 93 20 6f 6d 65 29   ...... (si. ome)
  0010: 2f 62 2f 61 3e 0a 0a 2e 31 2e 2e 40 2e 2e 2e d1   /b/a>...1..@....
  0020: 5c 0a 3c 52 78 75 6c 2e 2e 2e 2e 2e 2e 2e 6c 32   \.<Rxul.......l2
  0030: 2e 2e 2e 2e 2e 2e 72 72 72 72 72 72 72 72 72 50   ......rrrrrrrrrP
Seed 5 (id=46c28dd5b181881e, size=148 bytes, fuzzer=naive, trial=1, discovered_at=9979s, mutation_op=DwordAddMutator,BytesInsertCopyMutator,BytesDeleteMutator,BytesSwapMutator):
  0000: 20 6f 6c 65 29 2f 62 2f 61 3e 0a 0a 2e 2e 2e 2e    ole)/b/a>......
  0010: 72 72 72 72 72 72 72 72 39 2e 2e 40 2e 2e 2e d1   rrrrrrrr9..@....
  0020: 5c 0a 3c 52 78 75 6c 2e 2e 48 2e 2e 2e 2e 2e 6c   \.<Rxul..H.....l
  0030: 32 2e 2e 2e 2e 2e 2e 72 72 72 72 72 72 72 72 72   2......rrrrrrrrr


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  37(7)x4 3d(=)x2                     2e(.)x6 2f(/)x2 20( )x2 0a(.)x1 +3u  PARTIAL
   0x0001  37(7)x4 22(")x2                     2e(.)x9 6f(o)x2 22(")x1 5f(_)x1 +1u  PARTIAL
   0x0002  f4(.)x4 68(h)x2                     2e(.)x9 6c(l)x2 69(i)x1 5f(_)x1 +1u  DIFFER
   0x0003  2d(-)x4 c1(.)x2                     2e(.)x9 65(e)x2 de(.)x1 5f(_)x1 +1u  DIFFER
   0x0004  78(x)x4 c1(.)x2                     2e(.)x9 29())x2 74(t)x1 5f(_)x1 +1u  DIFFER
   0x0005  6d(m)x4 c1(.)x2                     2e(.)x8 2f(/)x2 40(@)x1 70(p)x1 +2u  DIFFER
   0x0006  6c(l)x4 c1(.)x2                     20( )x8 62(b)x2 2e(.)x1 3a(:)x1 +2u  DIFFER
   0x0007  5c(\)x4 c1(.)x2                     28(()x8 2f(/)x3 2e(.)x1 c6(.)x1 +1u  DIFFER
   0x0008  0a(.)x4 c1(.)x2                     73(s)x8 61(a)x2 2e(.)x1 6e(n)x1 +2u  DIFFER
   0x0009  3c(<)x4 c1(.)x2                     69(i)x8 3e(>)x2 d1(.)x1 6b(k)x1 +2u  DIFFER
   0x000a  6d(m)x2 49(I)x2 c1(.)x2             93(.)x6 0a(.)x2 2e(.)x2 39(9)x1 +3u  DIFFER
   0x000b  6c(l)x2 53(S)x2 c1(.)x2             20( )x6 0a(.)x2 2e(.)x2 39(9)x1 +3u  DIFFER
   0x000c  20( )x2 4f(O)x2 74(t)x2             6f(o)x6 2e(.)x4 39(9)x1 72(r)x1 +2u  DIFFER
   0x000d  76(v)x2 74(t)x2 b5(.)x1 2d(-)x1     6c(l)x4 2e(.)x4 6d(m)x1 39(9)x1 +4u  PARTIAL
   0x000e  45(E)x2 70(p)x2 b5(.)x1 31(1)x1     65(e)x6 2e(.)x4 39(9)x1 66(f)x1 +2u  DIFFER
   0x000f  c0(.)x2 3a(:)x2 26(&)x1 30(0)x1     29())x6 2e(.)x4 39(9)x1 2f(/)x1 +2u  DIFFER
   0x0010  c0(.)x2 2f(/)x2 26(&)x1 36(6)x1     2f(/)x6 2e(.)x2 72(r)x1 39(9)x1 +4u  PARTIAL
   0x0011  c0(.)x2 2f(/)x2 3b(;)x1 34(4)x1     62(b)x6 2e(.)x3 72(r)x1 39(9)x1 +3u  DIFFER
   0x0012  c0(.)x2 66(f)x2 26(&)x1 36(6)x1     2f(/)x6 2e(.)x3 72(r)x1 39(9)x1 +3u  DIFFER
   0x0013  c0(.)x2 61(a)x2 26(&)x1 2d(-)x1     61(a)x6 2e(.)x3 72(r)x1 39(9)x1 +3u  PARTIAL
   0x0014  66(f)x3 c0(.)x2 55(U)x1             3e(>)x5 2e(.)x2 72(r)x1 39(9)x1 +5u  DIFFER
   0x0015  c0(.)x2 61(a)x2 32(2)x1 43(C)x1     0a(.)x6 2e(.)x2 72(r)x1 39(9)x1 +4u  PARTIAL
   0x0016  78(x)x2 6b(k)x2 37(7)x1 53(S)x1     0a(.)x7 2e(.)x2 72(r)x1 39(9)x1 +3u  DIFFER
   0x0017  78(x)x2 65(e)x2 37(7)x1 2d(-)x1     2e(.)x8 72(r)x1 39(9)x1 3c(<)x1 +3u  DIFFER
   0x001e  26(&)x3 ff(.)x1 5a(Z)x1 c0(.)x1     2e(.)x10 6c(l)x1 fe(.)x1 5f(_)x1 +1u  DIFFER
   0x001f  26(&)x3 ff(.)x1 2e(.)x1 c0(.)x1     d1(.)x9 2e(.)x2 ff(.)x1 74(t)x1 +1u  PARTIAL
   0x0020  26(&)x3 b2(.)x1 2e(.)x1 c0(.)x1     5c(\)x9 2e(.)x2 00(.)x1 65(e)x1 +1u  PARTIAL
   0x0026  74(t)x2 b2(.)x1 4e(N)x1 2d(-)x1 +1u  6c(l)x8 2e(.)x4 37(7)x1 75(u)x1     DIFFER
   0x0027  70(p)x2 b2(.)x1 4e(N)x1 2e(.)x1 +1u  2e(.)x11 20( )x1 37(7)x1 4c(L)x1    PARTIAL
   0x002a  2f(/)x2 b5(.)x1 61(a)x1 2e(.)x1 +1u  2e(.)x11 66(f)x1 65(e)x1 4c(L)x1    PARTIAL
   0x002b  75(u)x2 b5(.)x1 6b(k)x1 2e(.)x1 +1u  2e(.)x11 66(f)x1 5f(_)x1 70(p)x1    PARTIAL
   0x002c  61(a)x2 b5(.)x1 44(D)x1 2e(.)x1 +1u  2e(.)x11 66(f)x1 38(8)x1 3a(:)x1    PARTIAL
   0x003a  72(r)x3 4e(N)x1 c0(.)x1 b5(.)x1     2e(.)x6 72(r)x4 48(H)x1 66(f)x1 +2u  PARTIAL
==== MECHANISM CONTEXT (involved fuzzers only) ====
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6483.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6483,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6483 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6483 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6483 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).