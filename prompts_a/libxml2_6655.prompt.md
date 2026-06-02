==== BLOCKER ====
Target: libxml2
Branch ID: 6655
Location: /src/libxml2/parser.c:6524:9
Enclosing function: parser.c:xmlParseElementChildrenContentDeclPriv
Source line:     if (RAW == '?') {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (value_profile vs value_profile)
cmplog                           4        6          0  REFERENCE
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog             4        6          0  REFERENCE
naive_ctx                        4        6          0  REFERENCE
naive_ngram4                     3        7          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=10.20h  loser=21.70h
  avg hitcount on branch: winner=4  loser=1
  prob_div=0.70  dur_div=11.50h  hit_div=3
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6655/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlParseElementChildrenContentDeclPriv (/src/libxml2/parser.c:6320-6589) ---
[ ]  6318  static xmlElementContentPtr
[ ]  6319  xmlParseElementChildrenContentDeclPriv(xmlParserCtxtPtr ctxt, int inputchk,
[B]  6320                                         int depth) {
[B]  6321      xmlElementContentPtr ret = NULL, cur = NULL, last = NULL, op = NULL;
[B]  6322      const xmlChar *elem;
[B]  6323      xmlChar type = 0;
[ ]  6324  
[B]  6325      if (((depth > 128) && ((ctxt->options & XML_PARSE_HUGE) == 0)) ||
[B]  6326          (depth >  2048)) {
[ ]  6327          xmlFatalErrMsgInt(ctxt, XML_ERR_ELEMCONTENT_NOT_FINISHED,
[ ]  6328  "xmlParseElementChildrenContentDecl : depth %d too deep, use XML_PARSE_HUGE\n",
[ ]  6329                            depth);
[ ]  6330  	return(NULL);
[ ]  6331      }
[B]  6332      SKIP_BLANKS;
[B]  6333      GROW;
[B]  6334      if (RAW == '(') {
[ ]  6335  	int inputid = ctxt->input->id;
[ ]  6336  
[ ]  6337          /* Recurse on first child */
[ ]  6338  	NEXT;
[ ]  6339  	SKIP_BLANKS;
[ ]  6340          cur = ret = xmlParseElementChildrenContentDeclPriv(ctxt, inputid,
[ ]  6341                                                             depth + 1);
[ ]  6342          if (cur == NULL)
[ ]  6343              return(NULL);
[ ]  6344  	SKIP_BLANKS;
[ ]  6345  	GROW;
[B]  6346      } else {
[B]  6347  	elem = xmlParseName(ctxt);
[B]  6348  	if (elem == NULL) {
[L]  6349  	    xmlFatalErr(ctxt, XML_ERR_ELEMCONTENT_NOT_STARTED, NULL);
[L]  6350  	    return(NULL);
[L]  6351  	}
[B]  6352          cur = ret = xmlNewDocElementContent(ctxt->myDoc, elem, XML_ELEMENT_CONTENT_ELEMENT);
[B]  6353  	if (cur == NULL) {
[ ]  6354  	    xmlErrMemory(ctxt, NULL);
[ ]  6355  	    return(NULL);
[ ]  6356  	}
[B]  6357  	GROW;
[B]  6358  	if (RAW == '?') {
[ ]  6359  	    cur->ocur = XML_ELEMENT_CONTENT_OPT;
[ ]  6360  	    NEXT;
[B]  6361  	} else if (RAW == '*') {
[B]  6362  	    cur->ocur = XML_ELEMENT_CONTENT_MULT;
[B]  6363  	    NEXT;
[B]  6364  	} else if (RAW == '+') {
[ ]  6365  	    cur->ocur = XML_ELEMENT_CONTENT_PLUS;
[ ]  6366  	    NEXT;
[B]  6367  	} else {
[B]  6368  	    cur->ocur = XML_ELEMENT_CONTENT_ONCE;
[B]  6369  	}
[B]  6370  	GROW;
[B]  6371      }
[B]  6372      SKIP_BLANKS;
[B]  6373      SHRINK;
[B]  6374      while ((RAW != ')') && (ctxt->instate != XML_PARSER_EOF)) {
[ ]  6375          /*
[ ]  6376  	 * Each loop we parse one separator and one element.
[ ]  6377  	 */
[ ]  6378          if (RAW == ',') {
[ ]  6379  	    if (type == 0) type = CUR;
[ ]  6380  
[ ]  6381  	    /*
[ ]  6382  	     * Detect "Name | Name , Name" error
[ ]  6383  	     */
[ ]  6384  	    else if (type != CUR) {
[ ]  6385  		xmlFatalErrMsgInt(ctxt, XML_ERR_SEPARATOR_REQUIRED,
[ ]  6386  		    "xmlParseElementChildrenContentDecl : '%c' expected\n",
[ ]  6387  		                  type);
[ ]  6388  		if ((last != NULL) && (last != ret))
[ ]  6389  		    xmlFreeDocElementContent(ctxt->myDoc, last);
[ ]  6390  		if (ret != NULL)
[ ]  6391  		    xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6392  		return(NULL);
[ ]  6393  	    }
[ ]  6394  	    NEXT;
[ ]  6395  
[ ]  6396  	    op = xmlNewDocElementContent(ctxt->myDoc, NULL, XML_ELEMENT_CONTENT_SEQ);
[ ]  6397  	    if (op == NULL) {
[ ]  6398  		if ((last != NULL) && (last != ret))
[ ]  6399  		    xmlFreeDocElementContent(ctxt->myDoc, last);
[ ]  6400  	        xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6401  		return(NULL);
[ ]  6402  	    }
[ ]  6403  	    if (last == NULL) {
[ ]  6404  		op->c1 = ret;
[ ]  6405  		if (ret != NULL)
[ ]  6406  		    ret->parent = op;
[ ]  6407  		ret = cur = op;
[ ]  6408  	    } else {
[ ]  6409  	        cur->c2 = op;
[ ]  6410  		if (op != NULL)
[ ]  6411  		    op->parent = cur;
[ ]  6412  		op->c1 = last;
[ ]  6413  		if (last != NULL)
[ ]  6414  		    last->parent = op;
[ ]  6415  		cur =op;
[ ]  6416  		last = NULL;
[ ]  6417  	    }
[ ]  6418  	} else if (RAW == '|') {
[ ]  6419  	    if (type == 0) type = CUR;
[ ]  6420  
[ ]  6421  	    /*
[ ]  6422  	     * Detect "Name , Name | Name" error
[ ]  6423  	     */
[ ]  6424  	    else if (type != CUR) {
[ ]  6425  		xmlFatalErrMsgInt(ctxt, XML_ERR_SEPARATOR_REQUIRED,
[ ]  6426  		    "xmlParseElementChildrenContentDecl : '%c' expected\n",
[ ]  6427  				  type);
[ ]  6428  		if ((last != NULL) && (last != ret))
[ ]  6429  		    xmlFreeDocElementContent(ctxt->myDoc, last);
[ ]  6430  		if (ret != NULL)
[ ]  6431  		    xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6432  		return(NULL);
[ ]  6433  	    }
[ ]  6434  	    NEXT;
[ ]  6435  
[ ]  6436  	    op = xmlNewDocElementContent(ctxt->myDoc, NULL, XML_ELEMENT_CONTENT_OR);
[ ]  6437  	    if (op == NULL) {
[ ]  6438  		if ((last != NULL) && (last != ret))
[ ]  6439  		    xmlFreeDocElementContent(ctxt->myDoc, last);
[ ]  6440  		if (ret != NULL)
[ ]  6441  		    xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6442  		return(NULL);
[ ]  6443  	    }
[ ]  6444  	    if (last == NULL) {
[ ]  6445  		op->c1 = ret;
[ ]  6446  		if (ret != NULL)
[ ]  6447  		    ret->parent = op;
[ ]  6448  		ret = cur = op;
[ ]  6449  	    } else {
[ ]  6450  	        cur->c2 = op;
[ ]  6451  		if (op != NULL)
[ ]  6452  		    op->parent = cur;
[ ]  6453  		op->c1 = last;
[ ]  6454  		if (last != NULL)
[ ]  6455  		    last->parent = op;
[ ]  6456  		cur =op;
[ ]  6457  		last = NULL;
[ ]  6458  	    }
[ ]  6459  	} else {
[ ]  6460  	    xmlFatalErr(ctxt, XML_ERR_ELEMCONTENT_NOT_FINISHED, NULL);
[ ]  6461  	    if ((last != NULL) && (last != ret))
[ ]  6462  	        xmlFreeDocElementContent(ctxt->myDoc, last);
[ ]  6463  	    if (ret != NULL)
[ ]  6464  		xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6465  	    return(NULL);
[ ]  6466  	}
[ ]  6467  	GROW;
[ ]  6468  	SKIP_BLANKS;
[ ]  6469  	GROW;
[ ]  6470  	if (RAW == '(') {
[ ]  6471  	    int inputid = ctxt->input->id;
[ ]  6472  	    /* Recurse on second child */
[ ]  6473  	    NEXT;
[ ]  6474  	    SKIP_BLANKS;
[ ]  6475  	    last = xmlParseElementChildrenContentDeclPriv(ctxt, inputid,
[ ]  6476                                                            depth + 1);
[ ]  6477              if (last == NULL) {
[ ]  6478  		if (ret != NULL)
[ ]  6479  		    xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6480  		return(NULL);
[ ]  6481              }
[ ]  6482  	    SKIP_BLANKS;
[ ]  6483  	} else {
[ ]  6484  	    elem = xmlParseName(ctxt);
[ ]  6485  	    if (elem == NULL) {
[ ]  6486  		xmlFatalErr(ctxt, XML_ERR_ELEMCONTENT_NOT_STARTED, NULL);
[ ]  6487  		if (ret != NULL)
[ ]  6488  		    xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6489  		return(NULL);
[ ]  6490  	    }
[ ]  6491  	    last = xmlNewDocElementContent(ctxt->myDoc, elem, XML_ELEMENT_CONTENT_ELEMENT);
[ ]  6492  	    if (last == NULL) {
[ ]  6493  		if (ret != NULL)
[ ]  6494  		    xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6495  		return(NULL);
[ ]  6496  	    }
[ ]  6497  	    if (RAW == '?') {
[ ]  6498  		last->ocur = XML_ELEMENT_CONTENT_OPT;
[ ]  6499  		NEXT;
[ ]  6500  	    } else if (RAW == '*') {
[ ]  6501  		last->ocur = XML_ELEMENT_CONTENT_MULT;
[ ]  6502  		NEXT;
[ ]  6503  	    } else if (RAW == '+') {
[ ]  6504  		last->ocur = XML_ELEMENT_CONTENT_PLUS;
[ ]  6505  		NEXT;
[ ]  6506  	    } else {
[ ]  6507  		last->ocur = XML_ELEMENT_CONTENT_ONCE;
[ ]  6508  	    }
[ ]  6509  	}
[ ]  6510  	SKIP_BLANKS;
[ ]  6511  	GROW;
[ ]  6512      }
[B]  6513      if ((cur != NULL) && (last != NULL)) {
[ ]  6514          cur->c2 = last;
[ ]  6515  	if (last != NULL)
[ ]  6516  	    last->parent = cur;
[ ]  6517      }
[B]  6518      if (ctxt->input->id != inputchk) {
[ ]  6519  	xmlFatalErrMsg(ctxt, XML_ERR_ENTITY_BOUNDARY,
[ ]  6520                         "Element content declaration doesn't start and stop in"
[ ]  6521                         " the same entity\n");
[ ]  6522      }
[B]  6523      NEXT;
[B]  6524      if (RAW == '?') { <-- BLOCKER
[W]  6525  	if (ret != NULL) {
[W]  6526  	    if ((ret->ocur == XML_ELEMENT_CONTENT_PLUS) ||
[W]  6527  	        (ret->ocur == XML_ELEMENT_CONTENT_MULT))
[W]  6528  	        ret->ocur = XML_ELEMENT_CONTENT_MULT;
[ ]  6529  	    else
[ ]  6530  	        ret->ocur = XML_ELEMENT_CONTENT_OPT;
[W]  6531  	}
[W]  6532  	NEXT;
[B]  6533      } else if (RAW == '*') {
[ ]  6534  	if (ret != NULL) {
[ ]  6535  	    ret->ocur = XML_ELEMENT_CONTENT_MULT;
[ ]  6536  	    cur = ret;
[ ]  6537  	    /*
[ ]  6538  	     * Some normalization:
[ ]  6539  	     * (a | b* | c?)* == (a | b | c)*
[ ]  6540  	     */
[ ]  6541  	    while ((cur != NULL) && (cur->type == XML_ELEMENT_CONTENT_OR)) {
[ ]  6542  		if ((cur->c1 != NULL) &&
[ ]  6543  	            ((cur->c1->ocur == XML_ELEMENT_CONTENT_OPT) ||
[ ]  6544  		     (cur->c1->ocur == XML_ELEMENT_CONTENT_MULT)))
[ ]  6545  		    cur->c1->ocur = XML_ELEMENT_CONTENT_ONCE;
[ ]  6546  		if ((cur->c2 != NULL) &&
[ ]  6547  	            ((cur->c2->ocur == XML_ELEMENT_CONTENT_OPT) ||
[ ]  6548  		     (cur->c2->ocur == XML_ELEMENT_CONTENT_MULT)))
[ ]  6549  		    cur->c2->ocur = XML_ELEMENT_CONTENT_ONCE;
[ ]  6550  		cur = cur->c2;
[ ]  6551  	    }
[ ]  6552  	}
[ ]  6553  	NEXT;
[B]  6554      } else if (RAW == '+') {
[L]  6555  	if (ret != NULL) {
[L]  6556  	    int found = 0;
[ ]  6557  
[L]  6558  	    if ((ret->ocur == XML_ELEMENT_CONTENT_OPT) ||
[L]  6559  	        (ret->ocur == XML_ELEMENT_CONTENT_MULT))
[L]  6560  	        ret->ocur = XML_ELEMENT_CONTENT_MULT;
[ ]  6561  	    else
[ ]  6562  	        ret->ocur = XML_ELEMENT_CONTENT_PLUS;
[ ]  6563  	    /*
[ ]  6564  	     * Some normalization:
[ ]  6565  	     * (a | b*)+ == (a | b)*
[ ]  6566  	     * (a | b?)+ == (a | b)*
[ ]  6567  	     */
[L]  6568  	    while ((cur != NULL) && (cur->type == XML_ELEMENT_CONTENT_OR)) {
[ ]  6569  		if ((cur->c1 != NULL) &&
[ ]  6570  	            ((cur->c1->ocur == XML_ELEMENT_CONTENT_OPT) ||
[ ]  6571  		     (cur->c1->ocur == XML_ELEMENT_CONTENT_MULT))) {
[ ]  6572  		    cur->c1->ocur = XML_ELEMENT_CONTENT_ONCE;
[ ]  6573  		    found = 1;
[ ]  6574  		}
[ ]  6575  		if ((cur->c2 != NULL) &&
[ ]  6576  	            ((cur->c2->ocur == XML_ELEMENT_CONTENT_OPT) ||
[ ]  6577  		     (cur->c2->ocur == XML_ELEMENT_CONTENT_MULT))) {
[ ]  6578  		    cur->c2->ocur = XML_ELEMENT_CONTENT_ONCE;
[ ]  6579  		    found = 1;
[ ]  6580  		}
[ ]  6581  		cur = cur->c2;
[ ]  6582  	    }
[L]  6583  	    if (found)
[ ]  6584  		ret->ocur = XML_ELEMENT_CONTENT_MULT;
[L]  6585  	}
[L]  6586  	NEXT;
[L]  6587      }
[B]  6588      return(ret);
[B]  6589  }

--- Caller (1 hop): xmlParseElementContentDecl (/src/libxml2/parser.c:6647-6675, calls parser.c:xmlParseElementChildrenContentDeclPriv at line 6669) (full body — short) ---
[B]  6647                             xmlElementContentPtr *result) {
[ ]  6648  
[B]  6649      xmlElementContentPtr tree = NULL;
[B]  6650      int inputid = ctxt->input->id;
[B]  6651      int res;
[ ]  6652  
[B]  6653      *result = NULL;
[ ]  6654  
[B]  6655      if (RAW != '(') {
[ ]  6656  	xmlFatalErrMsgStr(ctxt, XML_ERR_ELEMCONTENT_NOT_STARTED,
[ ]  6657  		"xmlParseElementContentDecl : %s '(' expected\n", name);
[ ]  6658  	return(-1);
[ ]  6659      }
[B]  6660      NEXT;
[B]  6661      GROW;
[B]  6662      if (ctxt->instate == XML_PARSER_EOF)
[ ]  6663          return(-1);
[B]  6664      SKIP_BLANKS;
[B]  6665      if (CMP7(CUR_PTR, '#', 'P', 'C', 'D', 'A', 'T', 'A')) {
[B]  6666          tree = xmlParseElementMixedContentDecl(ctxt, inputid);
[B]  6667  	res = XML_ELEMENT_TYPE_MIXED;
[B]  6668      } else {
[B]  6669          tree = xmlParseElementChildrenContentDeclPriv(ctxt, inputid, 1); <-- CALL
[B]  6670  	res = XML_ELEMENT_TYPE_ELEMENT;
[B]  6671      }
[B]  6672      SKIP_BLANKS;
[B]  6673      *result = tree;
[B]  6674      return(res);
[B]  6675  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseElementChildrenContentDecl  (/src/libxml2/parser.c:6624-6627, calls parser.c:xmlParseElementChildrenContentDeclPriv at line 6626)
hop 2  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675, calls parser.c:xmlParseElementChildrenContentDeclPriv at line 6669)
hop 3  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788, calls xmlParseElementContentDecl at line 6736)
hop 4  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseElementDecl at line 6957)
hop 5  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 5  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 6  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 6  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 6  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 7  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 7  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)
hop 8  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseDocTypeDecl at line 11958)
hop 8  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 8  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 8  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     230      1470  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      24       796  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     143       845  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      30       165  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      18        90  inputPop  (/src/libxml2/parser.c:1723-1738)
      12        74  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
       0        60  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      11        58  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
      11        58  inputPush  (/src/libxml2/parser.c:1693-1712)
      10        54  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
      10        51  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
      10        43  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
       4        36  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
       7        37  parser.c:xmlHaltParser  (/src/libxml2/parser.c:12416-12441)
       6        33  xmlParseChunk  (/src/libxml2/parser.c:12135-12300)
... (70 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=8   L11409  T=0 F=4  T=0 F=22  if (ctxt->input == NULL)
  d=8   L11465  T=4 F=0  T=22 F=0  if ((ctxt->input != NULL) &&
  d=8   L11466  T=0 F=4  T=0 F=22  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=8   L11470  T=16 F=0  T=102 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=8   L11471  T=4 F=0  T=16 F=32  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L11471  T=4 F=12  T=48 F=54  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L11474  T=0 F=12  T=0 F=86  if (ctxt->input == NULL) break;
  d=8   L11475  T=0 F=12  T=0 F=86  if (ctxt->input->buf == NULL)
  d=8   L11486  T=6 F=6  T=56 F=30  if ((ctxt->instate != XML_PARSER_START) &&
  d=8   L11487  T=0 F=6  T=0 F=56  (ctxt->input->buf->raw != NULL) &&
  d=8   L11500  T=0 F=12  T=1 F=85  if (avail < 1)
  d=8   L11502  T=0 F=12  T=0 F=85  switch (ctxt->instate) {
  d=8   L11503  T=0 F=12  T=0 F=85  case XML_PARSER_EOF:
  d=8   L11508  T=6 F=6  T=30 F=55  case XML_PARSER_START:
  d=8   L11509  T=2 F=4  T=10 F=20  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=8   L11516  T=0 F=2  T=0 F=10  if (avail < 4)
  d=8   L11535  T=0 F=4  T=0 F=20  if (avail < 2)
  d=8   L11539  T=0 F=4  T=0 F=20  if (cur == 0) {
  d=8   L11553  T=4 F=0  T=20 F=0  if ((cur == '<') && (next == '?')) {
  d=8   L11553  T=4 F=0  T=20 F=0  if ((cur == '<') && (next == '?')) {
  d=8   L11555  T=0 F=4  T=0 F=20  if (avail < 5) goto done;
  d=8   L11556  T=4 F=0  T=20 F=0  if ((!terminate) &&
  d=8   L11557  T=0 F=4  T=0 F=20  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=8   L11559  T=4 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L11559  T=4 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L11562  T=4 F=0  T=20 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=8   L11563  T=4 F=0  T=20 F=0  (ctxt->input->cur[3] == 'm') &&
  d=8   L11564  T=4 F=0  T=20 F=0  (ctxt->input->cur[4] == 'l') &&
  d=8   L11572  T=0 F=4  T=0 F=20  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=8   L11581  T=4 F=0  T=20 F=0  if ((ctxt->encoding == NULL) &&
  d=8   L11582  T=0 F=4  T=0 F=20  (ctxt->input->encoding != NULL))
  d=8   L11584  T=4 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=8   L11584  T=4 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=8   L11585  T=4 F=0  T=20 F=0  (!ctxt->disableSAX))
  d=8   L11622  T=1 F=11  T=7 F=78  case XML_PARSER_START_TAG: {
  d=8   L11629  T=0 F=1  T=0 F=7  if ((avail < 2) && (ctxt->inputNr == 1))
  d=8   L11632  T=0 F=1  T=2 F=5  if (cur != '<') {
  d=8   L11635  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L11635  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L11639  T=0 F=1  T=1 F=4  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11639  T=1 F=0  T=5 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11641  T=0 F=1  T=0 F=4  if (ctxt->spaceNr == 0)
  d=8   L11643  T=0 F=1  T=0 F=4  else if (*ctxt->space == -2)
  d=8   L11648  T=0 F=1  T=4 F=0  if (ctxt->sax2)
  d=8   L11655  T=0 F=1  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L11657  T=0 F=1  T=0 F=4  if (name == NULL) {
  d=8   L11670  T=0 F=1  T=0 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=8   L11670  T=1 F=0  T=0 F=4  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=8   L11678  T=0 F=1  T=0 F=4  if ((RAW == '/') && (NXT(1) == '>')) {
  d=8   L11707  T=0 F=1  T=2 F=2  if (RAW == '>') {
  d=8   L11721  T=0 F=12  T=18 F=67  case XML_PARSER_CONTENT: {
  d=8   L11722  T=0 F=0  T=0 F=18  if ((avail < 2) && (ctxt->inputNr == 1))
  d=8   L11727  T=0 F=0  T=4 F=2  if ((cur == '<') && (next == '/')) {
  d=8   L11727  T=0 F=0  T=6 F=12  if ((cur == '<') && (next == '/')) {
  d=8   L11730  T=0 F=0  T=0 F=2  } else if ((cur == '<') && (next == '?')) {
  d=8   L11730  T=0 F=0  T=2 F=12  } else if ((cur == '<') && (next == '?')) {
  d=8   L11736  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (next != '!')) {
  d=8   L11736  T=0 F=0  T=2 F=12  } else if ((cur == '<') && (next != '!')) {
  d=8   L11739  T=0 F=0  T=0 F=12  } else if ((cur == '<') && (next == '!') &&
  d=8   L11747  T=0 F=0  T=0 F=12  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=8   L11758  T=0 F=0  T=0 F=12  } else if ((cur == '<') && (next == '!') &&
  d=8   L11761  T=0 F=0  T=0 F=12  } else if (cur == '<') {
  d=8   L11765  T=0 F=0  T=0 F=12  } else if (cur == '&') {
  d=8   L11782  T=0 F=0  T=12 F=0  if ((ctxt->inputNr == 1) &&
  d=8   L11783  T=0 F=0  T=12 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=8   L11784  T=0 F=0  T=0 F=12  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=8   L11784  T=0 F=0  T=12 F=0  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=8   L11792  T=0 F=12  T=4 F=81  case XML_PARSER_END_TAG:
  d=8   L11793  T=0 F=0  T=0 F=4  if (avail < 2)
  d=8   L11795  T=0 F=0  T=0 F=4  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=8   L11795  T=0 F=0  T=4 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=8   L11797  T=0 F=0  T=4 F=0  if (ctxt->sax2) {
  d=8   L11805  T=0 F=0  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF) {
  d=8   L11807  T=0 F=0  T=2 F=2  } else if (ctxt->nameNr == 0) {
  d=8   L11813  T=0 F=12  T=0 F=85  case XML_PARSER_CDATA_SECTION: {
  d=8   L11904  T=4 F=8  T=20 F=65  case XML_PARSER_MISC:
  d=8   L11905  T=1 F=11  T=4 F=81  case XML_PARSER_PROLOG:
  d=8   L11906  T=0 F=12  T=2 F=83  case XML_PARSER_EPILOG:
  d=8   L11908  T=0 F=5  T=0 F=26  if (ctxt->input->buf == NULL)
  d=8   L11914  T=0 F=5  T=2 F=24  if (avail < 2)
  d=8   L11918  T=5 F=0  T=22 F=2  if ((cur == '<') && (next == '?')) {
  d=8   L11918  T=0 F=5  T=0 F=22  if ((cur == '<') && (next == '?')) {
  d=8   L11929  T=4 F=1  T=20 F=2  } else if ((cur == '<') && (next == '!') &&
  d=8   L11929  T=5 F=0  T=22 F=2  } else if ((cur == '<') && (next == '!') &&
  d=8   L11930  T=0 F=4  T=0 F=20  (ctxt->input->cur[2] == '-') &&
  d=8   L11942  T=4 F=1  T=20 F=4  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=8   L11943  T=4 F=0  T=20 F=0  (cur == '<') && (next == '!') &&
  d=8   L11943  T=4 F=0  T=20 F=0  (cur == '<') && (next == '!') &&
  d=8   L11944  T=4 F=0  T=20 F=0  (ctxt->input->cur[2] == 'D') &&
  d=8   L11945  T=4 F=0  T=20 F=0  (ctxt->input->cur[3] == 'O') &&
  d=8   L11946  T=4 F=0  T=20 F=0  (ctxt->input->cur[4] == 'C') &&
  d=8   L11947  T=4 F=0  T=20 F=0  (ctxt->input->cur[5] == 'T') &&
  d=8   L11948  T=4 F=0  T=20 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=8   L11949  T=4 F=0  T=20 F=0  (ctxt->input->cur[7] == 'P') &&
  d=8   L11950  T=4 F=0  T=20 F=0  (ctxt->input->cur[8] == 'E')) {
  d=8   L11951  T=4 F=0  T=20 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11951  T=0 F=4  T=0 F=20  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11959  T=0 F=4  T=0 F=20  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L11961  T=0 F=4  T=0 F=20  if (RAW == '[') {
  d=8   L11972  T=4 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=8   L11972  T=4 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=8   L11973  T=4 F=0  T=20 F=0  (ctxt->sax->externalSubset != NULL))
  d=8   L11985  T=0 F=1  T=0 F=2  } else if ((cur == '<') && (next == '!') &&
  d=8   L11985  T=1 F=0  T=2 F=2  } else if ((cur == '<') && (next == '!') &&
  d=8   L11989  T=0 F=1  T=0 F=4  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=8   L12007  T=0 F=12  T=0 F=85  case XML_PARSER_DTD: {
  d=8   L12029  T=0 F=12  T=0 F=85  case XML_PARSER_COMMENT:
  d=8   L12038  T=0 F=12  T=0 F=85  case XML_PARSER_IGNORE:
  d=8   L12047  T=0 F=12  T=0 F=85  case XML_PARSER_PI:
  d=8   L12056  T=0 F=12  T=0 F=85  case XML_PARSER_ENTITY_DECL:
  d=8   L12065  T=0 F=12  T=0 F=85  case XML_PARSER_ENTITY_VALUE:
  d=8   L12074  T=0 F=12  T=0 F=85  case XML_PARSER_ATTRIBUTE_VALUE:
  d=8   L12083  T=0 F=12  T=0 F=85  case XML_PARSER_SYSTEM_LITERAL:
  d=8   L12092  T=0 F=12  T=0 F=85  case XML_PARSER_PUBLIC_LITERAL:
--- d=7  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=7   L8396  T=0 F=6  T=0 F=30  if (name == NULL) {
  d=7   L8409  T=6 F=0  T=30 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=7   L8420  T=6 F=0  T=30 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=7   L8420  T=6 F=0  T=30 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=7   L8421  T=6 F=0  T=30 F=0  (!ctxt->disableSAX))
  d=7   L8423  T=0 F=6  T=0 F=30  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L8430  T=0 F=6  T=0 F=30  if (RAW == '[')
  d=7   L8436  T=0 F=6  T=0 F=30  if (RAW != '>') {
--- d=7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=7   L10816  T=0 F=2  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=7   L10816  T=0 F=2  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=7   L10829  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L10829  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L10831  T=0 F=2  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10834  T=2 F=0  T=10 F=0  if ((ctxt->encoding == NULL) &&
  d=7   L10835  T=2 F=0  T=10 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=7   L10846  T=2 F=0  T=10 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=7   L10852  T=0 F=2  T=0 F=10  if (CUR == 0) {
  d=7   L10863  T=0 F=2  T=0 F=10  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=7   L10872  T=0 F=2  T=0 F=10  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=7   L10873  T=0 F=2  T=0 F=10  (ctxt->instate == XML_PARSER_EOF)) {
  d=7   L10884  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=7   L10884  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=7   L10884  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=7   L10886  T=0 F=2  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10888  T=2 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=7   L10888  T=2 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=7   L10889  T=2 F=0  T=10 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=7   L10889  T=0 F=2  T=0 F=10  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=7   L10907  T=0 F=2  T=0 F=10  if (RAW == '[') {
  d=7   L10918  T=2 F=0  T=10 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=7   L10918  T=2 F=0  T=10 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=7   L10919  T=2 F=0  T=10 F=0  (!ctxt->disableSAX))
  d=7   L10922  T=2 F=0  T=9 F=1  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10936  T=0 F=0  T=0 F=1  if (RAW != '<') {
  d=7   L10950  T=0 F=0  T=0 F=1  if (RAW != 0) {
  d=7   L10959  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L10959  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L10965  T=0 F=0  T=1 F=0  if ((ctxt->myDoc != NULL) &&
  d=7   L10966  T=0 F=0  T=0 F=1  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=7   L10971  T=0 F=0  T=0 F=1  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=7   L10980  T=0 F=0  T=1 F=0  if (! ctxt->wellFormed) {
--- d=5  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=5   L7099  T=5 F=0  T=28 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L7100  T=5 F=0  T=28 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=5   L7109  T=0 F=5  T=0 F=28  if (enc != XML_CHAR_ENCODING_NONE)
  d=5   L7123  T=0 F=5  T=0 F=28  if (ctxt->myDoc == NULL) {
  d=5   L7131  T=0 F=5  T=0 F=28  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=5   L7131  T=5 F=0  T=28 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=5   L7137  T=17 F=0  T=102 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=5   L7137  T=17 F=0  T=99 F=3  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=5   L7139  T=12 F=0  T=74 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=5   L7139  T=12 F=5  T=74 F=25  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=5   L7139  T=0 F=12  T=0 F=74  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=5   L7141  T=12 F=5  T=74 F=25  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=5   L7141  T=12 F=0  T=74 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=5   L7151  T=0 F=0  T=0 F=3  if (RAW != 0) {
--- d=4  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=4   L6952  T=12 F=0  T=74 F=0  if (CUR == '<') {
  d=4   L6953  T=12 F=0  T=74 F=0  if (NXT(1) == '!') {
  d=4   L6955  T=10 F=2  T=56 F=18  case 'E':
  d=4   L6956  T=10 F=0  T=54 F=2  if (NXT(3) == 'L')
  d=4   L6958  T=0 F=0  T=0 F=2  else if (NXT(3) == 'N')
  d=4   L6963  T=2 F=10  T=18 F=56  case 'A':
  d=4   L6966  T=0 F=12  T=0 F=74  case 'N':
  d=4   L6969  T=0 F=12  T=0 F=74  case '-':
  d=4   L6972  T=0 F=12  T=0 F=74  default:
  d=4   L6986  T=0 F=12  T=0 F=74  if (ctxt->instate == XML_PARSER_EOF)
--- d=3  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788) ---
  d=3   L6698  T=0 F=10  T=0 F=54  if ((CUR != '<') || (NXT(1) != '!'))
  d=3   L6698  T=0 F=10  T=0 F=54  if ((CUR != '<') || (NXT(1) != '!'))
  d=3   L6707  T=0 F=10  T=0 F=54  if (SKIP_BLANKS == 0) {
  d=3   L6713  T=0 F=10  T=0 F=54  if (name == NULL) {
  d=3   L6718  T=0 F=10  T=0 F=54  if (SKIP_BLANKS == 0) {
  d=3   L6728  T=0 F=10  T=0 F=54  } else if ((RAW == 'A') && (NXT(1) == 'N') &&
  d=3   L6735  T=10 F=0  T=51 F=3  } else if (RAW == '(') {
  d=3   L6741  T=0 F=0  T=0 F=3  if ((RAW == '%') && (ctxt->external == 0) &&
  d=3   L6754  T=5 F=5  T=8 F=43  if (RAW != '>') {
  d=3   L6756  T=5 F=0  T=6 F=2  if (content != NULL) {
  d=3   L6760  T=0 F=5  T=0 F=43  if (inputid != ctxt->input->id) {
  d=3   L6767  T=5 F=0  T=43 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L6767  T=0 F=5  T=40 F=3  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L6768  T=0 F=0  T=40 F=0  (ctxt->sax->elementDecl != NULL)) {
  d=3   L6769  T=0 F=0  T=40 F=0  if (content != NULL)
  d=3   L6773  T=0 F=0  T=40 F=0  if ((content != NULL) && (content->parent == NULL)) {
  d=3   L6773  T=0 F=0  T=0 F=40  if ((content != NULL) && (content->parent == NULL)) {
--- d=2  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675) ---
  d=2   L6655  T=0 F=10  T=0 F=51  if (RAW != '(') {
  d=2   L6662  T=0 F=10  T=0 F=51  if (ctxt->instate == XML_PARSER_EOF)
--- d=1  parser.c:xmlParseElementChildrenContentDeclPriv  (/src/libxml2/parser.c:6320-6589) ---
  d=1   L6325  T=0 F=8  T=0 F=30  if (((depth > 128) && ((ctxt->options & XML_PARSE_HUGE) =...
  d=1   L6326  T=0 F=8  T=0 F=30  (depth >  2048)) {
  d=1   L6334  T=0 F=8  T=0 F=30  if (RAW == '(') {
  d=1   L6348  T=0 F=8  T=2 F=28  if (elem == NULL) {
  d=1   L6353  T=0 F=8  T=0 F=28  if (cur == NULL) {
  d=1   L6358  T=0 F=8  T=0 F=28  if (RAW == '?') {
  d=1   L6361  T=5 F=3  T=24 F=4  } else if (RAW == '*') {
  d=1   L6374  T=0 F=8  T=0 F=28  while ((RAW != ')') && (ctxt->instate != XML_PARSER_EOF)) {
  d=1   L6513  T=8 F=0  T=28 F=0  if ((cur != NULL) && (last != NULL)) {
  d=1   L6513  T=0 F=8  T=0 F=28  if ((cur != NULL) && (last != NULL)) {
  d=1   L6518  T=0 F=8  T=0 F=28  if (ctxt->input->id != inputchk) {
  d=1   L6524  T=5 F=3  T=0 F=28  if (RAW == '?') {  <-- BLOCKER
  d=1   L6525  T=5 F=0  T=0 F=0  if (ret != NULL) {
  d=1   L6526  T=0 F=5  T=0 F=0  if ((ret->ocur == XML_ELEMENT_CONTENT_PLUS) ||
  d=1   L6527  T=5 F=0  T=0 F=0  (ret->ocur == XML_ELEMENT_CONTENT_MULT))
  d=1   L6533  T=0 F=3  T=0 F=28  } else if (RAW == '*') {
  d=1   L6554  T=0 F=3  T=3 F=25  } else if (RAW == '+') {
  d=1   L6555  T=0 F=0  T=3 F=0  if (ret != NULL) {
  d=1   L6558  T=0 F=0  T=0 F=3  if ((ret->ocur == XML_ELEMENT_CONTENT_OPT) ||
  d=1   L6559  T=0 F=0  T=3 F=0  (ret->ocur == XML_ELEMENT_CONTENT_MULT))
  d=1   L6568  T=0 F=0  T=3 F=0  while ((cur != NULL) && (cur->type == XML_ELEMENT_CONTENT...
  d=1   L6568  T=0 F=0  T=0 F=3  while ((cur != NULL) && (cur->type == XML_ELEMENT_CONTENT...
  d=1   L6583  T=0 F=0  T=0 F=3  if (found)

[off-chain: 734 additional divergent branches across 77 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=065805d908a7c637, size=452 bytes, fuzzer=value_profile, trial=1, discovered_at=5625s, mutation_op=WordInterestingMutator,BytesExpandMutator,QwordAddMutator,ByteInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=027cb3e7d96a4d95, size=609 bytes, fuzzer=value_profile, trial=1, discovered_at=8059s, mutation_op=QwordAddMutator,CrossoverReplaceMutator,ByteNegMutator,BytesInsertMutator,TokenReplace):
  0000: 3c 22 68 74 74 70 3a 2f 2f 66 5e 6b 65 75 72 6c   <"http://f^keurl
  0010: 2e 6e 65 74 22 3e 62 05 fd ff ff ff 2f 74 65 78   .net">b...../tex
  0020: 74 3c 2f 62 06 00 00 00 31 32 37 37 37 32 2e 78   t</b....127772.x
  0030: 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f   ml\.<?xml versio

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=028449a3e7659dfa, size=389 bytes, fuzzer=naive, trial=1, discovered_at=4s, mutation_op=BytesDeleteMutator,BitFlipMutator,BytesSwapMutator,TokenInsert,ByteNegMutator,CrossoverInsertMutator):
  0000: 74 64 22 3e 0a 0a 3c 61 3e 0a 20 20 3c 62 20 06   td">..<a>.  <b .
  0010: 00 00 00 31 32 37 37 37 32 4a 78 6d 6c 5c 0a 3c   ...127772Jxml\.<
  0020: 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e   ?xml version="1.
  0030: 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61   0"?>.<!DOCTYPE a
Seed 2 (id=022872fb8319f510, size=611 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=CrossoverInsertMutator,WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=013a786979d45920, size=375 bytes, fuzzer=naive, trial=1, discovered_at=59s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=02f665196242465b, size=328 bytes, fuzzer=naive, trial=1, discovered_at=108s, mutation_op=BytesDeleteMutator,ByteNegMutator,BytesDeleteMutator):
  0000: c9 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   .2.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
Seed 5 (id=089ad774f736d538, size=667 bytes, fuzzer=naive, trial=1, discovered_at=118s, mutation_op=WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 5a 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   Z SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x1 3c(<)x1                     06(.)x5 74(t)x1 c9(.)x1 3d(=)x1 +2u  PARTIAL
   0x0001  00(.)x1 22(")x1                     00(.)x6 64(d)x1 32(2)x1 22(")x1 +1u  PARTIAL
   0x0002  00(.)x1 68(h)x1                     00(.)x6 22(")x1 2e(.)x1 74(t)x1 +1u  PARTIAL
   0x0003  00(.)x1 74(t)x1                     00(.)x6 3e(>)x1 78(x)x1 74(t)x1 +1u  PARTIAL
   0x0004  31(1)x1 74(t)x1                     31(1)x6 0a(.)x1 6d(m)x1 74(t)x1 +1u  PARTIAL
   0x0005  32(2)x1 70(p)x1                     32(2)x6 0a(.)x1 6c(l)x1 70(p)x1 +1u  PARTIAL
   0x0006  37(7)x1 3a(:)x1                     37(7)x6 3c(<)x1 5c(\)x1 3a(:)x1 +1u  PARTIAL
   0x0007  37(7)x1 2f(/)x1                     37(7)x6 61(a)x1 0a(.)x1 2f(/)x1 +1u  PARTIAL
   0x0008  37(7)x1 2f(/)x1                     37(7)x6 3e(>)x1 3c(<)x1 2f(/)x1 +1u  PARTIAL
   0x0009  32(2)x1 66(f)x1                     32(2)x6 0a(.)x1 3f(?)x1 66(f)x1 +1u  PARTIAL
   0x000a  2e(.)x1 5e(^)x1                     2e(.)x6 20( )x1 78(x)x1 62(b)x1 +1u  PARTIAL
   0x000b  78(x)x1 6b(k)x1                     78(x)x6 20( )x1 6d(m)x1 3e(>)x1 +1u  PARTIAL
   0x000c  6d(m)x1 65(e)x1                     6d(m)x6 3c(<)x1 6c(l)x1 b6(.)x1 +1u  PARTIAL
   0x000d  6c(l)x1 75(u)x1                     6c(l)x6 62(b)x1 20( )x1 b6(.)x1 +1u  PARTIAL
   0x000e  5c(\)x1 72(r)x1                     5c(\)x6 20( )x1 76(v)x1 b6(.)x1 +1u  PARTIAL
   0x000f  0a(.)x1 6c(l)x1                     0a(.)x6 06(.)x1 65(e)x1 b6(.)x1 +1u  PARTIAL
   0x0010  3c(<)x1 2e(.)x1                     3c(<)x6 00(.)x1 72(r)x1 b6(.)x1 +1u  PARTIAL
   0x0011  3f(?)x1 6e(n)x1                     3f(?)x6 00(.)x1 73(s)x1 b6(.)x1 +1u  PARTIAL
   0x0012  78(x)x1 65(e)x1                     78(x)x6 00(.)x1 69(i)x1 b6(.)x1 +1u  PARTIAL
   0x0013  6d(m)x1 74(t)x1                     6d(m)x6 31(1)x1 6f(o)x1 b6(.)x1 +1u  PARTIAL
   0x0014  6c(l)x1 22(")x1                     6c(l)x6 32(2)x1 6e(n)x1 61(a)x1 +1u  PARTIAL
   0x0015  20( )x1 3e(>)x1                     20( )x6 37(7)x1 3d(=)x1 6b(k)x1 +1u  PARTIAL
   0x0016  76(v)x1 62(b)x1                     76(v)x6 37(7)x1 22(")x1 65(e)x1 +1u  PARTIAL
   0x0017  65(e)x1 05(.)x1                     65(e)x6 37(7)x1 31(1)x1 75(u)x1 +1u  PARTIAL
   0x0018  72(r)x1 fd(.)x1                     72(r)x6 32(2)x1 2e(.)x1 28(()x1 +1u  PARTIAL
   0x0019  73(s)x1 ff(.)x1                     73(s)x7 4a(J)x1 30(0)x1 39(9)x1     PARTIAL
   0x001a  69(i)x1 ff(.)x1                     69(i)x7 78(x)x1 22(")x1 2f(/)x1     PARTIAL
   0x001b  6f(o)x1 ff(.)x1                     6f(o)x6 6d(m)x2 3f(?)x1 78(x)x1     PARTIAL
   0x001c  6e(n)x1 2f(/)x1                     6e(n)x6 6c(l)x2 3e(>)x2             PARTIAL
   0x001d  3d(=)x1 74(t)x1                     3d(=)x6 5c(\)x1 0a(.)x1 3e(>)x1 +1u  PARTIAL
   0x001e  22(")x1 65(e)x1                     22(")x6 0a(.)x1 3c(<)x1 3e(>)x1 +1u  PARTIAL
   0x001f  31(1)x1 78(x)x1                     31(1)x6 3c(<)x1 21(!)x1 3e(>)x1 +1u  PARTIAL
   0x0020  2e(.)x1 74(t)x1                     2e(.)x6 3f(?)x1 44(D)x1 20( )x1 +1u  PARTIAL
   0x0021  30(0)x1 3c(<)x1                     30(0)x6 78(x)x1 4f(O)x1 d6(.)x1 +1u  PARTIAL
   0x0022  22(")x1 2f(/)x1                     22(")x6 6d(m)x1 43(C)x1 23(#)x1 +1u  PARTIAL
   0x0023  3f(?)x1 62(b)x1                     3f(?)x6 6c(l)x1 54(T)x1 46(F)x1 +1u  PARTIAL
   0x0024  3e(>)x1 06(.)x1                     3e(>)x7 20( )x1 59(Y)x1 49(I)x1     PARTIAL
   0x0025  0a(.)x1 00(.)x1                     0a(.)x6 76(v)x1 50(P)x1 58(X)x1 +1u  PARTIAL
   0x0026  3c(<)x1 00(.)x1                     3c(<)x6 45(E)x2 65(e)x1 2f(/)x1     PARTIAL
   0x0027  21(!)x1 00(.)x1                     21(!)x6 72(r)x1 20( )x1 44(D)x1 +1u  PARTIAL
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6655.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6655,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6655 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6655 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6655 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).