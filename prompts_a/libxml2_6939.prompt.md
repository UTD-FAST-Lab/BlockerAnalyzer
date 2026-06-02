==== BLOCKER ====
Target: libxml2
Branch ID: 6939
Location: /src/libxml2/tree.c:3421:9
Enclosing function: xmlAddChild
Source line:     if ((parent == NULL) || (parent->type == XML_NAMESPACE_DECL)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            9        1          0  winner (ngram_coverage vs naive_ngram4)
cmplog                           9        1          0  REFERENCE
value_profile                    9        1          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        6        4          0  REFERENCE
naive_ngram4                     1        9          0  loser (ngram_coverage vs naive)
mopt                             4        6          0  REFERENCE
minimizer                        9        1          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ngram4']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > naive_ngram4  [delta: ngram_coverage] ---
  subject 36  (naive_ngram4 vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=14.40h  loser=22.40h
  avg hitcount on branch: winner=67  loser=8
  prob_div=0.80  dur_div=8.00h  hit_div=59
  subject-level: delta_AUC=-26852220.0  p_AUC=0.0173  delta_Final=-260.4  p_final=0.0312

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6939/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlAddChild (/src/libxml2/tree.c:3418-3532) ---
[ ]  3416   */
[ ]  3417  xmlNodePtr
[B]  3418  xmlAddChild(xmlNodePtr parent, xmlNodePtr cur) {
[B]  3419      xmlNodePtr prev;
[ ]  3420  
[B]  3421      if ((parent == NULL) || (parent->type == XML_NAMESPACE_DECL)) { <-- BLOCKER
[ ]  3422  #ifdef DEBUG_TREE
[ ]  3423          xmlGenericError(xmlGenericErrorContext,
[ ]  3424  		"xmlAddChild : parent == NULL\n");
[ ]  3425  #endif
[W]  3426  	return(NULL);
[W]  3427      }
[ ]  3428  
[B]  3429      if ((cur == NULL) || (cur->type == XML_NAMESPACE_DECL)) {
[ ]  3430  #ifdef DEBUG_TREE
[ ]  3431          xmlGenericError(xmlGenericErrorContext,
[ ]  3432  		"xmlAddChild : child == NULL\n");
[ ]  3433  #endif
[ ]  3434  	return(NULL);
[ ]  3435      }
[ ]  3436  
[B]  3437      if (parent == cur) {
[ ]  3438  #ifdef DEBUG_TREE
[ ]  3439          xmlGenericError(xmlGenericErrorContext,
[ ]  3440  		"xmlAddChild : parent == cur\n");
[ ]  3441  #endif
[ ]  3442  	return(NULL);
[ ]  3443      }
[ ]  3444      /*
[ ]  3445       * If cur is a TEXT node, merge its content with adjacent TEXT nodes
[ ]  3446       * cur is then freed.
[ ]  3447       */
[B]  3448      if (cur->type == XML_TEXT_NODE) {
[L]  3449  	if ((parent->type == XML_TEXT_NODE) &&
[L]  3450  	    (parent->content != NULL) &&
[L]  3451  	    (parent->name == cur->name)) {
[ ]  3452  	    xmlNodeAddContent(parent, cur->content);
[ ]  3453  	    xmlFreeNode(cur);
[ ]  3454  	    return(parent);
[ ]  3455  	}
[L]  3456  	if ((parent->last != NULL) && (parent->last->type == XML_TEXT_NODE) &&
[L]  3457  	    (parent->last->name == cur->name) &&
[L]  3458  	    (parent->last != cur)) {
[ ]  3459  	    xmlNodeAddContent(parent->last, cur->content);
[ ]  3460  	    xmlFreeNode(cur);
[ ]  3461  	    return(parent->last);
[ ]  3462  	}
[L]  3463      }
[ ]  3464  
[ ]  3465      /*
[ ]  3466       * add the new element at the end of the children list.
[ ]  3467       */
[B]  3468      prev = cur->parent;
[B]  3469      cur->parent = parent;
[B]  3470      if (cur->doc != parent->doc) {
[ ]  3471  	xmlSetTreeDoc(cur, parent->doc);
[ ]  3472      }
[ ]  3473      /* this check prevents a loop on tree-traversions if a developer
[ ]  3474       * tries to add a node to its parent multiple times
[ ]  3475       */
[B]  3476      if (prev == parent)
[ ]  3477  	return(cur);
[ ]  3478  
[ ]  3479      /*
[ ]  3480       * Coalescing
[ ]  3481       */
[B]  3482      if ((parent->type == XML_TEXT_NODE) &&
[B]  3483  	(parent->content != NULL) &&
[B]  3484  	(parent != cur)) {
[ ]  3485  	xmlNodeAddContent(parent, cur->content);
[ ]  3486  	xmlFreeNode(cur);
[ ]  3487  	return(parent);
[ ]  3488      }
[B]  3489      if (cur->type == XML_ATTRIBUTE_NODE) {
[ ]  3490  		if (parent->type != XML_ELEMENT_NODE)
[ ]  3491  			return(NULL);
[ ]  3492  	if (parent->properties != NULL) {
[ ]  3493  	    /* check if an attribute with the same name exists */
[ ]  3494  	    xmlAttrPtr lastattr;
[ ]  3495  
[ ]  3496  	    if (cur->ns == NULL)
[ ]  3497  		lastattr = xmlHasNsProp(parent, cur->name, NULL);
[ ]  3498  	    else
[ ]  3499  		lastattr = xmlHasNsProp(parent, cur->name, cur->ns->href);
[ ]  3500  	    if ((lastattr != NULL) && (lastattr != (xmlAttrPtr) cur) && (lastattr->type != XML_ATTRIBUTE_DECL)) {
[ ]  3501  		/* different instance, destroy it (attributes must be unique) */
[ ]  3502  			xmlUnlinkNode((xmlNodePtr) lastattr);
[ ]  3503  		xmlFreeProp(lastattr);
[ ]  3504  	    }
[ ]  3505  		if (lastattr == (xmlAttrPtr) cur)
[ ]  3506  			return(cur);
[ ]  3507  
[ ]  3508  	}
[ ]  3509  	if (parent->properties == NULL) {
[ ]  3510  	    parent->properties = (xmlAttrPtr) cur;
[ ]  3511  	} else {
[ ]  3512  	    /* find the end */
[ ]  3513  	    xmlAttrPtr lastattr = parent->properties;
[ ]  3514  	    while (lastattr->next != NULL) {
[ ]  3515  		lastattr = lastattr->next;
[ ]  3516  	    }
[ ]  3517  	    lastattr->next = (xmlAttrPtr) cur;
[ ]  3518  	    ((xmlAttrPtr) cur)->prev = lastattr;
[ ]  3519  	}
[B]  3520      } else {
[B]  3521  	if (parent->children == NULL) {
[L]  3522  	    parent->children = cur;
[L]  3523  	    parent->last = cur;
[B]  3524  	} else {
[B]  3525  	    prev = parent->last;
[B]  3526  	    prev->next = cur;
[B]  3527  	    cur->prev = prev;
[B]  3528  	    parent->last = cur;
[B]  3529  	}
[B]  3530      }
[B]  3531      return(cur);
[B]  3532  }

--- Caller (1 hop): xmlSAX2Reference (/src/libxml2/SAX2.c:2513-2533, calls xmlAddChild at line 2530) (full body — short) ---
[W]  2513  {
[W]  2514      xmlParserCtxtPtr ctxt = (xmlParserCtxtPtr) ctx;
[W]  2515      xmlNodePtr ret;
[ ]  2516  
[W]  2517      if (ctx == NULL) return;
[ ]  2518  #ifdef DEBUG_SAX
[ ]  2519      xmlGenericError(xmlGenericErrorContext,
[ ]  2520  	    "SAX.xmlSAX2Reference(%s)\n", name);
[ ]  2521  #endif
[W]  2522      if (name[0] == '#')
[ ]  2523  	ret = xmlNewCharRef(ctxt->myDoc, name);
[W]  2524      else
[W]  2525  	ret = xmlNewReference(ctxt->myDoc, name);
[ ]  2526  #ifdef DEBUG_SAX_TREE
[ ]  2527      xmlGenericError(xmlGenericErrorContext,
[ ]  2528  	    "add xmlSAX2Reference %s to %s \n", name, ctxt->node->name);
[ ]  2529  #endif
[W]  2530      if (xmlAddChild(ctxt->node, ret) == NULL) { <-- CALL
[W]  2531          xmlFreeNode(ret);
[W]  2532      }
[W]  2533  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls xmlAddChild at line 7500)
hop 3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseReference at line 10020)
hop 3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseReference at line 11768)
hop 4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 4  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 4  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 5  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 5  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 5  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 6  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 6  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 6  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 7  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 7  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 8  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 8  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     591      5850  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
       3       617  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      32       383  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      32       383  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
      35       379  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      31       363  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
       5       272  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706)
      21       237  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      37       242  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       2       188  parser.c:xmlFatalErrMsgInt  (/src/libxml2/parser.c:572-586)
       3       176  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942)
      23       194  xmlAddChild  (/src/libxml2/tree.c:3418-3532)  <-- enclosing
       5       163  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
      14       168  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      20       171  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
... (108 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10816  T=0 F=1  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10816  T=0 F=1  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10829  T=1 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10829  T=1 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10831  T=0 F=1  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10834  T=1 F=0  T=10 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L10835  T=1 F=0  T=10 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=5   L10846  T=1 F=0  T=6 F=4  if (enc != XML_CHAR_ENCODING_NONE) {
  d=5   L10852  T=0 F=1  T=0 F=10  if (CUR == 0) {
  d=5   L10863  T=0 F=1  T=0 F=10  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=5   L10872  T=0 F=1  T=0 F=4  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=5   L10873  T=0 F=1  T=0 F=4  (ctxt->instate == XML_PARSER_EOF)) {
  d=5   L10884  T=1 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=1 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=1 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10886  T=0 F=1  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10888  T=1 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10888  T=1 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10889  T=1 F=0  T=10 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10889  T=0 F=1  T=0 F=10  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10907  T=0 F=1  T=0 F=3  if (RAW == '[') {
  d=5   L10918  T=1 F=0  T=3 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10918  T=1 F=0  T=3 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10919  T=1 F=0  T=3 F=0  (!ctxt->disableSAX))
  d=5   L10922  T=0 F=1  T=0 F=3  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10936  T=0 F=1  T=0 F=10  if (RAW != '<') {
  d=5   L10950  T=1 F=0  T=5 F=5  if (RAW != 0) {
  d=5   L10959  T=1 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10959  T=1 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10965  T=1 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) &&
  d=5   L10966  T=0 F=1  T=0 F=10  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=5   L10971  T=0 F=1  T=0 F=10  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=5   L10980  T=1 F=0  T=10 F=0  if (! ctxt->wellFormed) {
--- d=4  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=4   L10077  T=1 F=0  T=6 F=4  if (xmlParseElementStart(ctxt) != 0)
  d=4   L10081  T=0 F=0  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10084  T=0 F=0  T=4 F=0  if (CUR == 0) {
--- d=4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=4   L12139  T=0 F=4  T=0 F=65  if (ctxt == NULL)
  d=4   L12141  T=0 F=1  T=0 F=10  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12141  T=1 F=3  T=10 F=55  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12143  T=0 F=4  T=0 F=65  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12145  T=0 F=4  T=0 F=65  if (ctxt->input == NULL)
  d=4   L12149  T=2 F=2  T=29 F=36  if (ctxt->instate == XML_PARSER_START)
  d=4   L12151  T=3 F=0  T=41 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12151  T=3 F=1  T=41 F=24  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12151  T=3 F=0  T=41 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12152  T=0 F=3  T=1 F=40  (chunk[size - 1] == '\r')) {
  d=4   L12159  T=3 F=0  T=42 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12159  T=3 F=0  T=42 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12159  T=3 F=1  T=42 F=24  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12160  T=3 F=0  T=42 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=4   L12160  T=3 F=0  T=42 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=4   L12170  T=2 F=1  T=26 F=16  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=4   L12170  T=2 F=0  T=26 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=4   L12171  T=2 F=0  T=26 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12171  T=0 F=2  T=1 F=25  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12174  T=0 F=0  T=1 F=0  if ((xmlStrcasestr(BAD_CAST ctxt->input->buf->encoder->name,
  d=4   L12185  T=0 F=0  T=1 F=0  if (ctxt->input->buf->rawconsumed < len)
  d=4   L12193  T=0 F=0  T=1 F=0  if ((unsigned int) size > len) {
  d=4   L12202  T=0 F=3  T=0 F=42  if (res < 0) {
  d=4   L12211  T=1 F=0  T=24 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12212  T=1 F=0  T=24 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12212  T=1 F=0  T=24 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12214  T=0 F=1  T=3 F=21  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=4   L12214  T=0 F=0  T=3 F=0  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=4   L12215  T=0 F=0  T=3 F=0  (in->raw != NULL)) {
  d=4   L12222  T=0 F=0  T=0 F=3  if (nbchars < 0) {
  d=4   L12233  T=0 F=4  T=1 F=65  if (remain != 0) {
  d=4   L12238  T=0 F=4  T=2 F=64  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12241  T=4 F=0  T=64 F=0  if ((ctxt->input != NULL) &&
  d=4   L12242  T=0 F=4  T=0 F=64  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=4   L12243  T=0 F=4  T=0 F=64  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=4   L12248  T=0 F=3  T=0 F=28  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12248  T=3 F=1  T=28 F=36  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12251  T=0 F=4  T=1 F=63  if (remain != 0) {
  d=4   L12257  T=0 F=0  T=1 F=0  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=4   L12257  T=0 F=4  T=1 F=62  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=4   L12258  T=0 F=0  T=1 F=0  (ctxt->input->buf != NULL)) {
  d=4   L12268  T=1 F=3  T=15 F=48  if (terminate) {
  d=4   L12274  T=1 F=0  T=15 F=0  if (ctxt->input != NULL) {
  d=4   L12275  T=0 F=1  T=0 F=15  if (ctxt->input->buf == NULL)
  d=4   L12283  T=1 F=0  T=15 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=4   L12284  T=1 F=0  T=15 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=4   L12287  T=0 F=1  T=0 F=15  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=4   L12290  T=1 F=0  T=15 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12291  T=1 F=0  T=15 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12291  T=1 F=0  T=15 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12296  T=3 F=1  T=28 F=35  if (ctxt->wellFormed == 0)
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9973  T=0 F=0  T=88 F=4  while ((RAW != 0) &&
  d=3   L9974  T=0 F=0  T=88 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L9980  T=0 F=0  T=33 F=55  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=0 F=0  T=0 F=33  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=0 F=0  T=33 F=55  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=0 F=0  T=6 F=27  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9996  T=0 F=0  T=0 F=6  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=3   L10004  T=0 F=0  T=33 F=55  else if (*cur == '<') {
  d=3   L10005  T=0 F=0  T=0 F=33  if (NXT(1) == '/') {
  d=3   L10019  T=0 F=0  T=0 F=55  else if (*cur == '&') {
--- d=3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=3   L11409  T=0 F=4  T=0 F=66  if (ctxt->input == NULL)
  d=3   L11465  T=4 F=0  T=66 F=0  if ((ctxt->input != NULL) &&
  d=3   L11466  T=0 F=4  T=0 F=66  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=3   L11470  T=82 F=0  T=794 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=3   L11471  T=0 F=76  T=0 F=674  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11471  T=76 F=6  T=674 F=120  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11474  T=0 F=82  T=0 F=794  if (ctxt->input == NULL) break;
  d=3   L11475  T=0 F=82  T=0 F=794  if (ctxt->input->buf == NULL)
  d=3   L11486  T=79 F=3  T=751 F=43  if ((ctxt->instate != XML_PARSER_START) &&
  d=3   L11487  T=0 F=79  T=42 F=709  (ctxt->input->buf->raw != NULL) &&
  d=3   L11488  T=0 F=0  T=39 F=3  (xmlBufIsEmpty(ctxt->input->buf->raw) == 0)) {
  d=3   L11500  T=1 F=81  T=13 F=781  if (avail < 1)
  d=3   L11502  T=0 F=81  T=0 F=781  switch (ctxt->instate) {
  d=3   L11503  T=0 F=81  T=0 F=781  case XML_PARSER_EOF:
  d=3   L11508  T=3 F=78  T=43 F=738  case XML_PARSER_START:
  d=3   L11509  T=1 F=2  T=14 F=29  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=3   L11516  T=0 F=1  T=0 F=14  if (avail < 4)
  d=3   L11535  T=0 F=2  T=0 F=29  if (avail < 2)
  d=3   L11539  T=0 F=2  T=0 F=29  if (cur == 0) {
  d=3   L11553  T=2 F=0  T=21 F=8  if ((cur == '<') && (next == '?')) {
  d=3   L11553  T=2 F=0  T=29 F=0  if ((cur == '<') && (next == '?')) {
  d=3   L11555  T=0 F=2  T=0 F=21  if (avail < 5) goto done;
  d=3   L11556  T=2 F=0  T=19 F=2  if ((!terminate) &&
  d=3   L11557  T=0 F=2  T=9 F=10  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11559  T=2 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11559  T=2 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11562  T=2 F=0  T=10 F=2  if ((ctxt->input->cur[2] == 'x') &&
  d=3   L11563  T=2 F=0  T=10 F=0  (ctxt->input->cur[3] == 'm') &&
  d=3   L11564  T=2 F=0  T=8 F=2  (ctxt->input->cur[4] == 'l') &&
  d=3   L11572  T=0 F=2  T=0 F=8  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=3   L11581  T=2 F=0  T=8 F=0  if ((ctxt->encoding == NULL) &&
  d=3   L11582  T=0 F=2  T=0 F=8  (ctxt->input->encoding != NULL))
  d=3   L11584  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11584  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11585  T=2 F=0  T=8 F=0  (!ctxt->disableSAX))
  d=3   L11594  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11594  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11595  T=0 F=0  T=4 F=0  (!ctxt->disableSAX))
  d=3   L11604  T=0 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11604  T=0 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11608  T=0 F=0  T=0 F=8  if (ctxt->version == NULL) {
  d=3   L11612  T=0 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11612  T=0 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11613  T=0 F=0  T=8 F=0  (!ctxt->disableSAX))
  d=3   L11622  T=4 F=77  T=154 F=627  case XML_PARSER_START_TAG: {
  d=3   L11629  T=0 F=4  T=0 F=154  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11632  T=0 F=4  T=0 F=154  if (cur != '<') {
  d=3   L11639  T=0 F=4  T=34 F=55  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11639  T=4 F=0  T=89 F=65  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11641  T=0 F=4  T=0 F=120  if (ctxt->spaceNr == 0)
  d=3   L11643  T=0 F=4  T=51 F=69  else if (*ctxt->space == -2)
  d=3   L11648  T=4 F=0  T=67 F=53  if (ctxt->sax2)
  d=3   L11655  T=0 F=4  T=0 F=120  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11657  T=0 F=4  T=2 F=118  if (name == NULL) {
  d=3   L11660  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11660  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11670  T=0 F=4  T=0 F=118  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=3   L11678  T=0 F=0  T=0 F=8  if ((RAW == '/') && (NXT(1) == '>')) {
  d=3   L11678  T=0 F=4  T=8 F=110  if ((RAW == '/') && (NXT(1) == '>')) {
  d=3   L11707  T=0 F=4  T=44 F=74  if (RAW == '>') {
  d=3   L11721  T=69 F=12  T=552 F=229  case XML_PARSER_CONTENT: {
  d=3   L11722  T=0 F=69  T=1 F=551  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11722  T=0 F=0  T=1 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11727  T=0 F=2  T=2 F=124  if ((cur == '<') && (next == '/')) {
  d=3   L11727  T=2 F=67  T=126 F=425  if ((cur == '<') && (next == '/')) {
  d=3   L11730  T=0 F=2  T=0 F=124  } else if ((cur == '<') && (next == '?')) {
  d=3   L11730  T=2 F=67  T=124 F=425  } else if ((cur == '<') && (next == '?')) {
  d=3   L11736  T=2 F=0  T=102 F=22  } else if ((cur == '<') && (next != '!')) {
  d=3   L11736  T=2 F=67  T=124 F=425  } else if ((cur == '<') && (next != '!')) {
  d=3   L11739  T=0 F=67  T=22 F=425  } else if ((cur == '<') && (next == '!') &&
  d=3   L11739  T=0 F=0  T=22 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11740  T=0 F=0  T=0 F=22  (ctxt->input->cur[2] == '-') &&
  d=3   L11747  T=0 F=0  T=22 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11747  T=0 F=67  T=22 F=425  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11748  T=0 F=0  T=0 F=22  (ctxt->input->cur[2] == '[') &&
  d=3   L11758  T=0 F=67  T=22 F=425  } else if ((cur == '<') && (next == '!') &&
  d=3   L11758  T=0 F=0  T=22 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11759  T=0 F=0  T=2 F=20  (avail < 9)) {
  d=3   L11761  T=0 F=67  T=20 F=425  } else if (cur == '<') {
  d=3   L11765  T=34 F=33  T=112 F=313  } else if (cur == '&') {
  d=3   L11766  T=34 F=0  T=0 F=112  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11766  T=0 F=34  T=0 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11782  T=33 F=0  T=313 F=0  if ((ctxt->inputNr == 1) &&
  d=3   L11783  T=33 F=0  T=262 F=51  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=3   L11784  T=2 F=30  T=5 F=95  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=3   L11784  T=32 F=1  T=100 F=162  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=3   L11792  T=0 F=81  T=2 F=779  case XML_PARSER_END_TAG:
  d=3   L11793  T=0 F=0  T=0 F=2  if (avail < 2)
  d=3   L11795  T=0 F=0  T=0 F=2  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11795  T=0 F=0  T=2 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11797  T=0 F=0  T=0 F=2  if (ctxt->sax2) {
  d=3   L11805  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF) {
  d=3   L11807  T=0 F=0  T=0 F=2  } else if (ctxt->nameNr == 0) {
  d=3   L11813  T=0 F=81  T=0 F=781  case XML_PARSER_CDATA_SECTION: {
  d=3   L11904  T=3 F=78  T=24 F=757  case XML_PARSER_MISC:
  d=3   L11905  T=2 F=79  T=6 F=775  case XML_PARSER_PROLOG:
  d=3   L11906  T=0 F=81  T=0 F=781  case XML_PARSER_EPILOG:
  d=3   L11908  T=0 F=5  T=0 F=30  if (ctxt->input->buf == NULL)
  d=3   L11914  T=0 F=5  T=0 F=30  if (avail < 2)
  d=3   L11918  T=5 F=0  T=30 F=0  if ((cur == '<') && (next == '?')) {
  d=3   L11918  T=0 F=5  T=4 F=26  if ((cur == '<') && (next == '?')) {
  d=3   L11919  T=0 F=0  T=4 F=0  if ((!terminate) &&
  d=3   L11920  T=0 F=0  T=0 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11927  T=0 F=0  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11929  T=3 F=2  T=6 F=20  } else if ((cur == '<') && (next == '!') &&
  d=3   L11929  T=5 F=0  T=26 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11930  T=0 F=3  T=0 F=6  (ctxt->input->cur[2] == '-') &&
  d=3   L11942  T=3 F=2  T=20 F=6  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=3   L11943  T=3 F=0  T=6 F=14  (cur == '<') && (next == '!') &&
  d=3   L11943  T=3 F=0  T=20 F=0  (cur == '<') && (next == '!') &&
  d=3   L11944  T=3 F=0  T=6 F=0  (ctxt->input->cur[2] == 'D') &&
  d=3   L11945  T=3 F=0  T=6 F=0  (ctxt->input->cur[3] == 'O') &&
  d=3   L11946  T=3 F=0  T=6 F=0  (ctxt->input->cur[4] == 'C') &&
  d=3   L11947  T=3 F=0  T=6 F=0  (ctxt->input->cur[5] == 'T') &&
  d=3   L11948  T=3 F=0  T=6 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=3   L11949  T=3 F=0  T=6 F=0  (ctxt->input->cur[7] == 'P') &&
  d=3   L11950  T=3 F=0  T=6 F=0  (ctxt->input->cur[8] == 'E')) {
  d=3   L11951  T=3 F=0  T=6 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11951  T=1 F=2  T=0 F=6  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11959  T=0 F=2  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11961  T=0 F=2  T=0 F=6  if (RAW == '[') {
  d=3   L11972  T=2 F=0  T=6 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11972  T=2 F=0  T=6 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11973  T=2 F=0  T=6 F=0  (ctxt->sax->externalSubset != NULL))
  d=3   L11985  T=0 F=2  T=0 F=20  } else if ((cur == '<') && (next == '!') &&
  d=3   L11985  T=2 F=0  T=20 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11989  T=0 F=2  T=0 F=20  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=3   L12007  T=0 F=81  T=0 F=781  case XML_PARSER_DTD: {
  d=3   L12029  T=0 F=81  T=0 F=781  case XML_PARSER_COMMENT:
  d=3   L12038  T=0 F=81  T=0 F=781  case XML_PARSER_IGNORE:
  d=3   L12047  T=0 F=81  T=0 F=781  case XML_PARSER_PI:
  d=3   L12056  T=0 F=81  T=0 F=781  case XML_PARSER_ENTITY_DECL:
  d=3   L12065  T=0 F=81  T=0 F=781  case XML_PARSER_ENTITY_VALUE:
  d=3   L12074  T=0 F=81  T=0 F=781  case XML_PARSER_ATTRIBUTE_VALUE:
  d=3   L12083  T=0 F=81  T=0 F=781  case XML_PARSER_SYSTEM_LITERAL:
  d=3   L12092  T=0 F=81  T=0 F=781  case XML_PARSER_PUBLIC_LITERAL:
--- d=2  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=2   L7181  T=0 F=34  T=0 F=112  if (RAW != '&')
  d=2   L7187  T=0 F=34  T=0 F=112  if (NXT(1) == '#') {
  d=2   L7233  T=34 F=0  T=112 F=0  if (ent == NULL) return;
--- d=1  xmlAddChild  (/src/libxml2/tree.c:3418-3532) ---
  d=1   L3421  T=0 F=5  T=0 F=194  if ((parent == NULL) || (parent->type == XML_NAMESPACE_DE...  <-- BLOCKER
  d=1   L3421  T=18 F=5  T=0 F=194  if ((parent == NULL) || (parent->type == XML_NAMESPACE_DE...  <-- BLOCKER
  d=1   L3429  T=0 F=5  T=0 F=194  if ((cur == NULL) || (cur->type == XML_NAMESPACE_DECL)) {
  d=1   L3429  T=0 F=5  T=0 F=194  if ((cur == NULL) || (cur->type == XML_NAMESPACE_DECL)) {
  d=1   L3437  T=0 F=5  T=0 F=194  if (parent == cur) {
  d=1   L3448  T=0 F=5  T=42 F=152  if (cur->type == XML_TEXT_NODE) {
  d=1   L3449  T=0 F=0  T=0 F=42  if ((parent->type == XML_TEXT_NODE) &&
  d=1   L3456  T=0 F=0  T=42 F=0  if ((parent->last != NULL) && (parent->last->type == XML_...
  d=1   L3456  T=0 F=0  T=0 F=42  if ((parent->last != NULL) && (parent->last->type == XML_...
  d=1   L3470  T=0 F=5  T=0 F=194  if (cur->doc != parent->doc) {
  d=1   L3476  T=0 F=5  T=0 F=194  if (prev == parent)
  d=1   L3482  T=0 F=5  T=0 F=194  if ((parent->type == XML_TEXT_NODE) &&
  d=1   L3489  T=0 F=5  T=0 F=194  if (cur->type == XML_ATTRIBUTE_NODE) {
  d=1   L3521  T=0 F=5  T=34 F=160  if (parent->children == NULL) {

[off-chain: 1136 additional divergent branches across 110 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=511a87c77cd9db71, size=257 bytes, fuzzer=naive, trial=1, discovered_at=77043s, mutation_op=ByteDecMutator,BytesCopyMutator,ByteAddMutator,BitFlipMutator):
  0000: 5f 10 00 5f 77 75 9b ff ff ff 31 32 37 37 37 32   _.._wu....127772
  0010: 00 40 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .@ml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=6b43f30e5da2266a, size=210 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 65 66 3d 22 68 74 74 70 3a 2f 2f 66 64 6b 65 75   ef="http://fdkeu
  0010: 72 6c 2e 6e 65 74 22 3e 62 05 74 65 78 74 3c 2f   rl.net">b.text</
  0020: 22 3c 2f 22 22 22 22 22 22 62 3d 0a 3c 2f 61 3e   "</""""""b=.</a>
  0030: 48 54 4d b3 64 74 06 00 00 00 31 32 37 37 37 32   HTM.dt....127772
Seed 2 (id=6b44f27b961c5a26, size=760 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 37 29 50 50 50 45 45 78 93 6c 5c 0a 3c 3f 78 6d   7)PPPEEx.l\.<?xm
  0010: 2f 73 2f 31 32 37 37 37 32 3f 3f 3f 3f 3f 3e 0a   /s/127772?????>.
  0020: 0a 3c 61 3e 0a 20 b2 b2 20 3c 62 20 78 6c 63 6e   .<a>. .. <b xlcn
  0030: 6b c6 68 72 49 53 4f 2d 31 30 36 40 36 2d 55 43   k.hrISO-106@6-UC
Seed 3 (id=8c191a2e8023cd23, size=466 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 2d 36 20 61 20 53 59 53 54 45 4d 15 22 64 74 64   -6 a SYSTEM."dtd
  0010: 73 2f 31 32 37 56 3a 2f 2f 66 61 6b 65 06 00 00   s/127V://fake...
  0020: 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78   .127772.xml\.<?x
  0030: 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22   ml version="1.0"
Seed 4 (id=8c2a24dec53cc3e0, size=672 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 01 01 01 01 2d 29 6d 6c 5c 0a fe ff 00 3c 01 00   ....-)ml\....<..
  0010: ff 2e 79 2d 2d 24 48 2d 2d 2e 11 d3 3b 3a 3b 2d   ..y--$H--...;:;-
  0020: 2d 00 3c 01 00 ff 48 2d 2d 2e ff 00 3c 01 00 ff   -.<...H--...<...
  0030: 2e 2d 4d 00 31 31 31 31 3c 26 00 6d 45 31 00 3c   .-M.1111<&.mE1.<
Seed 5 (id=8c3e23ca72a2f987, size=208 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 4d 4d 0f c1 0f 0f 0f c1 c1 0f 0f 6c 6c 69 0a 69   MM.........lli.i
  0010: 78 78 78 06 95 00 00 31 2c 37 37 37 32 2e 78 6d   xxx....1,7772.xm
  0020: 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e   l\.<?xml version
  0030: 3d 22 31 2e 30 22 3f 3e 0a 3c de 44 4f 43 54 59   ="1.0"?>.<.DOCTY


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  5f(_)x1                             65(e)x1 37(7)x1 2d(-)x1 01(.)x1 +6u  DIFFER
   0x0001  10(.)x1                             66(f)x1 29())x1 36(6)x1 01(.)x1 +6u  DIFFER
   0x0002  00(.)x1                             0f(.)x2 74(t)x2 3d(=)x1 50(P)x1 +4u  DIFFER
   0x0003  5f(_)x1                             74(t)x2 22(")x1 50(P)x1 61(a)x1 +5u  DIFFER
   0x0004  77(w)x1                             0f(.)x2 70(p)x2 74(t)x2 68(h)x1 +3u  DIFFER
   0x0005  75(u)x1                             74(t)x2 0f(.)x2 3a(:)x2 45(E)x1 +3u  DIFFER
   0x0006  9b(.)x1                             0f(.)x2 2f(/)x2 74(t)x1 45(E)x1 +4u  DIFFER
   0x0007  ff(.)x1                             2f(/)x3 53(S)x2 70(p)x1 78(x)x1 +3u  DIFFER
   0x0008  ff(.)x1                             2f(/)x2 3a(:)x1 93(.)x1 54(T)x1 +5u  DIFFER
   0x0009  ff(.)x1                             0f(.)x2 2f(/)x1 6c(l)x1 45(E)x1 +5u  DIFFER
   0x000a  31(1)x1                             0f(.)x2 2f(/)x1 5c(\)x1 4d(M)x1 +5u  DIFFER
   0x000b  32(2)x1                             0a(.)x2 66(f)x1 15(.)x1 ff(.)x1 +5u  DIFFER
   0x000c  37(7)x1                             3c(<)x2 64(d)x1 22(")x1 00(.)x1 +5u  DIFFER
   0x000d  37(7)x1                             6b(k)x1 3f(?)x1 64(d)x1 3c(<)x1 +6u  DIFFER
   0x000e  37(7)x1                             65(e)x1 78(x)x1 74(t)x1 01(.)x1 +6u  DIFFER
   0x000f  32(2)x1                             75(u)x1 6d(m)x1 64(d)x1 00(.)x1 +6u  DIFFER
   0x0010  00(.)x1                             72(r)x1 2f(/)x1 73(s)x1 ff(.)x1 +6u  DIFFER
   0x0011  40(@)x1                             6c(l)x1 73(s)x1 2f(/)x1 2e(.)x1 +6u  DIFFER
   0x0012  6d(m)x1                             2e(.)x1 2f(/)x1 31(1)x1 79(y)x1 +6u  DIFFER
   0x0013  6c(l)x1                             6e(n)x1 31(1)x1 32(2)x1 2d(-)x1 +6u  DIFFER
   0x0014  5c(\)x1                             65(e)x1 32(2)x1 37(7)x1 2d(-)x1 +6u  DIFFER
   0x0015  0a(.)x1                             74(t)x1 37(7)x1 56(V)x1 24($)x1 +6u  DIFFER
   0x0016  3c(<)x1                             22(")x1 37(7)x1 3a(:)x1 48(H)x1 +6u  DIFFER
   0x0017  3f(?)x1                             3e(>)x1 37(7)x1 2f(/)x1 2d(-)x1 +6u  DIFFER
   0x0018  78(x)x1                             62(b)x1 32(2)x1 2f(/)x1 2d(-)x1 +6u  DIFFER
   0x0019  6d(m)x1                             05(.)x1 3f(?)x1 66(f)x1 2e(.)x1 +6u  DIFFER
   0x001a  6c(l)x1                             74(t)x1 3f(?)x1 61(a)x1 11(.)x1 +6u  DIFFER
   0x001b  20( )x1                             65(e)x1 3f(?)x1 6b(k)x1 d3(.)x1 +6u  DIFFER
   0x001c  76(v)x1                             78(x)x1 3f(?)x1 65(e)x1 3b(;)x1 +6u  DIFFER
   0x001d  65(e)x1                             74(t)x2 3f(?)x1 06(.)x1 3a(:)x1 +5u  DIFFER
   0x001e  72(r)x1                             3c(<)x1 3e(>)x1 00(.)x1 3b(;)x1 +6u  DIFFER
   0x001f  73(s)x1                             2f(/)x1 0a(.)x1 00(.)x1 2d(-)x1 +6u  DIFFER
   0x0020  69(i)x1                             00(.)x2 22(")x1 0a(.)x1 2d(-)x1 +5u  DIFFER
   0x0021  6f(o)x1                             3c(<)x2 00(.)x2 31(1)x1 5c(\)x1 +4u  DIFFER
   0x0022  6e(n)x1                             2f(/)x1 61(a)x1 32(2)x1 3c(<)x1 +6u  DIFFER
   0x0023  3d(=)x1                             0a(.)x2 22(")x1 3e(>)x1 37(7)x1 +5u  DIFFER
   0x0024  22(")x1                             0a(.)x2 22(")x1 37(7)x1 00(.)x1 +5u  PARTIAL
   0x0025  31(1)x1                             22(")x1 20( )x1 37(7)x1 ff(.)x1 +6u  PARTIAL
   0x0026  2e(.)x1                             22(")x2 b2(.)x1 32(2)x1 48(H)x1 +5u  PARTIAL
   0x0027  30(0)x1                             2e(.)x2 22(")x1 b2(.)x1 2d(-)x1 +5u  DIFFER
   ... (24 more divergent offsets)
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

--- naive_ngram4 ---
**Instrumentation**: naive's edge counters, but the executor installs
an `NgramHook` (`HookableInProcessExecutor`) that folds a rolling
history of the last 4 edge IDs into the map index. A map slot
therefore encodes a length-4 edge path (an n-gram of N=4) rather than
a single edge.

**Feedback**: `MaxMapFeedback` over the n-gram-indexed map — a "new
bucket" is a previously-unseen 4-edge path tuple.

**Mutators**: naive's havoc + token stack. No I2S, no CMP_MAP. Stages
are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no dash rows.

**Per-execution cost**: edge increment plus a rolling 4-edge-history
update per executed edge.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6939.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6939,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>naive_ngram4 (ngram_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6939 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6939 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6939 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).