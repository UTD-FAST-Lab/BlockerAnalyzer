==== BLOCKER ====
Target: libxml2
Branch ID: 6654
Location: /src/libxml2/parser.c:6513:26
Enclosing function: parser.c:xmlParseElementChildrenContentDeclPriv
Source line:     if ((cur != NULL) && (last != NULL)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           0       10          0  loser (value_profile vs value_profile_cmplog)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=11.20h  loser=23.90h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=12.70h  hit_div=4
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6654/{W,L}/branch_coverage_show.txt

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
[W]  6378          if (RAW == ',') {
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
[W]  6418  	} else if (RAW == '|') {
[W]  6419  	    if (type == 0) type = CUR;
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
[W]  6434  	    NEXT;
[ ]  6435  
[W]  6436  	    op = xmlNewDocElementContent(ctxt->myDoc, NULL, XML_ELEMENT_CONTENT_OR);
[W]  6437  	    if (op == NULL) {
[ ]  6438  		if ((last != NULL) && (last != ret))
[ ]  6439  		    xmlFreeDocElementContent(ctxt->myDoc, last);
[ ]  6440  		if (ret != NULL)
[ ]  6441  		    xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6442  		return(NULL);
[ ]  6443  	    }
[W]  6444  	    if (last == NULL) {
[W]  6445  		op->c1 = ret;
[W]  6446  		if (ret != NULL)
[W]  6447  		    ret->parent = op;
[W]  6448  		ret = cur = op;
[W]  6449  	    } else {
[ ]  6450  	        cur->c2 = op;
[ ]  6451  		if (op != NULL)
[ ]  6452  		    op->parent = cur;
[ ]  6453  		op->c1 = last;
[ ]  6454  		if (last != NULL)
[ ]  6455  		    last->parent = op;
[ ]  6456  		cur =op;
[ ]  6457  		last = NULL;
[ ]  6458  	    }
[W]  6459  	} else {
[ ]  6460  	    xmlFatalErr(ctxt, XML_ERR_ELEMCONTENT_NOT_FINISHED, NULL);
[ ]  6461  	    if ((last != NULL) && (last != ret))
[ ]  6462  	        xmlFreeDocElementContent(ctxt->myDoc, last);
[ ]  6463  	    if (ret != NULL)
[ ]  6464  		xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6465  	    return(NULL);
[ ]  6466  	}
[W]  6467  	GROW;
[W]  6468  	SKIP_BLANKS;
[W]  6469  	GROW;
[W]  6470  	if (RAW == '(') {
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
[W]  6483  	} else {
[W]  6484  	    elem = xmlParseName(ctxt);
[W]  6485  	    if (elem == NULL) {
[ ]  6486  		xmlFatalErr(ctxt, XML_ERR_ELEMCONTENT_NOT_STARTED, NULL);
[ ]  6487  		if (ret != NULL)
[ ]  6488  		    xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6489  		return(NULL);
[ ]  6490  	    }
[W]  6491  	    last = xmlNewDocElementContent(ctxt->myDoc, elem, XML_ELEMENT_CONTENT_ELEMENT);
[W]  6492  	    if (last == NULL) {
[ ]  6493  		if (ret != NULL)
[ ]  6494  		    xmlFreeDocElementContent(ctxt->myDoc, ret);
[ ]  6495  		return(NULL);
[ ]  6496  	    }
[W]  6497  	    if (RAW == '?') {
[ ]  6498  		last->ocur = XML_ELEMENT_CONTENT_OPT;
[ ]  6499  		NEXT;
[W]  6500  	    } else if (RAW == '*') {
[ ]  6501  		last->ocur = XML_ELEMENT_CONTENT_MULT;
[ ]  6502  		NEXT;
[W]  6503  	    } else if (RAW == '+') {
[ ]  6504  		last->ocur = XML_ELEMENT_CONTENT_PLUS;
[ ]  6505  		NEXT;
[W]  6506  	    } else {
[W]  6507  		last->ocur = XML_ELEMENT_CONTENT_ONCE;
[W]  6508  	    }
[W]  6509  	}
[W]  6510  	SKIP_BLANKS;
[W]  6511  	GROW;
[W]  6512      }
[B]  6513      if ((cur != NULL) && (last != NULL)) { <-- BLOCKER
[W]  6514          cur->c2 = last;
[W]  6515  	if (last != NULL)
[W]  6516  	    last->parent = cur;
[W]  6517      }
[B]  6518      if (ctxt->input->id != inputchk) {
[ ]  6519  	xmlFatalErrMsg(ctxt, XML_ERR_ENTITY_BOUNDARY,
[ ]  6520                         "Element content declaration doesn't start and stop in"
[ ]  6521                         " the same entity\n");
[ ]  6522      }
[B]  6523      NEXT;
[B]  6524      if (RAW == '?') {
[ ]  6525  	if (ret != NULL) {
[ ]  6526  	    if ((ret->ocur == XML_ELEMENT_CONTENT_PLUS) ||
[ ]  6527  	        (ret->ocur == XML_ELEMENT_CONTENT_MULT))
[ ]  6528  	        ret->ocur = XML_ELEMENT_CONTENT_MULT;
[ ]  6529  	    else
[ ]  6530  	        ret->ocur = XML_ELEMENT_CONTENT_OPT;
[ ]  6531  	}
[ ]  6532  	NEXT;
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
[ ]  6555  	if (ret != NULL) {
[ ]  6556  	    int found = 0;
[ ]  6557  
[ ]  6558  	    if ((ret->ocur == XML_ELEMENT_CONTENT_OPT) ||
[ ]  6559  	        (ret->ocur == XML_ELEMENT_CONTENT_MULT))
[ ]  6560  	        ret->ocur = XML_ELEMENT_CONTENT_MULT;
[ ]  6561  	    else
[ ]  6562  	        ret->ocur = XML_ELEMENT_CONTENT_PLUS;
[ ]  6563  	    /*
[ ]  6564  	     * Some normalization:
[ ]  6565  	     * (a | b*)+ == (a | b)*
[ ]  6566  	     * (a | b?)+ == (a | b)*
[ ]  6567  	     */
[ ]  6568  	    while ((cur != NULL) && (cur->type == XML_ELEMENT_CONTENT_OR)) {
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
[ ]  6583  	    if (found)
[ ]  6584  		ret->ocur = XML_ELEMENT_CONTENT_MULT;
[ ]  6585  	}
[ ]  6586  	NEXT;
[ ]  6587      }
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
[L]  6666          tree = xmlParseElementMixedContentDecl(ctxt, inputid);
[L]  6667  	res = XML_ELEMENT_TYPE_MIXED;
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
     159      2950  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      96      2210  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     106      2140  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      18       454  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       0       225  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
       9       180  inputPop  (/src/libxml2/parser.c:1723-1738)
       6       164  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
       6       122  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
       6       119  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
       6       119  inputPush  (/src/libxml2/parser.c:1693-1712)
       6       119  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
       0        99  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)
       0        96  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
       0        93  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
       0        87  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
... (72 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=8   L11409  T=0 F=5  T=0 F=46  if (ctxt->input == NULL)
  d=8   L11465  T=5 F=0  T=46 F=0  if ((ctxt->input != NULL) &&
  d=8   L11466  T=0 F=5  T=0 F=46  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=8   L11470  T=32 F=0  T=265 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=8   L11471  T=0 F=17  T=26 F=94  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L11471  T=17 F=15  T=120 F=145  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L11474  T=0 F=32  T=0 F=239  if (ctxt->input == NULL) break;
  d=8   L11475  T=0 F=32  T=0 F=239  if (ctxt->input->buf == NULL)
  d=8   L11486  T=29 F=3  T=179 F=60  if ((ctxt->instate != XML_PARSER_START) &&
  d=8   L11487  T=0 F=29  T=0 F=179  (ctxt->input->buf->raw != NULL) &&
  d=8   L11500  T=3 F=29  T=5 F=234  if (avail < 1)
  d=8   L11502  T=0 F=29  T=0 F=234  switch (ctxt->instate) {
  d=8   L11503  T=0 F=29  T=0 F=234  case XML_PARSER_EOF:
  d=8   L11508  T=3 F=26  T=60 F=174  case XML_PARSER_START:
  d=8   L11509  T=1 F=2  T=20 F=40  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=8   L11516  T=0 F=1  T=0 F=20  if (avail < 4)
  d=8   L11535  T=0 F=2  T=0 F=40  if (avail < 2)
  d=8   L11539  T=0 F=2  T=0 F=40  if (cur == 0) {
  d=8   L11553  T=2 F=0  T=40 F=0  if ((cur == '<') && (next == '?')) {
  d=8   L11553  T=2 F=0  T=40 F=0  if ((cur == '<') && (next == '?')) {
  d=8   L11555  T=0 F=2  T=0 F=40  if (avail < 5) goto done;
  d=8   L11556  T=2 F=0  T=40 F=0  if ((!terminate) &&
  d=8   L11557  T=0 F=2  T=0 F=40  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=8   L11559  T=2 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L11559  T=2 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L11562  T=2 F=0  T=40 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=8   L11563  T=2 F=0  T=40 F=0  (ctxt->input->cur[3] == 'm') &&
  d=8   L11564  T=2 F=0  T=40 F=0  (ctxt->input->cur[4] == 'l') &&
  d=8   L11572  T=0 F=2  T=0 F=40  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=8   L11581  T=2 F=0  T=40 F=0  if ((ctxt->encoding == NULL) &&
  d=8   L11582  T=0 F=2  T=0 F=40  (ctxt->input->encoding != NULL))
  d=8   L11584  T=2 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=8   L11584  T=2 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=8   L11585  T=2 F=0  T=40 F=0  (!ctxt->disableSAX))
  d=8   L11622  T=4 F=25  T=32 F=202  case XML_PARSER_START_TAG: {
  d=8   L11629  T=0 F=4  T=0 F=32  if ((avail < 2) && (ctxt->inputNr == 1))
  d=8   L11632  T=0 F=4  T=2 F=30  if (cur != '<') {
  d=8   L11635  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L11635  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L11639  T=0 F=4  T=0 F=30  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11639  T=4 F=0  T=30 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11641  T=0 F=4  T=0 F=30  if (ctxt->spaceNr == 0)
  d=8   L11643  T=0 F=4  T=0 F=30  else if (*ctxt->space == -2)
  d=8   L11648  T=4 F=0  T=22 F=8  if (ctxt->sax2)
  d=8   L11655  T=0 F=4  T=0 F=30  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L11657  T=0 F=4  T=4 F=26  if (name == NULL) {
  d=8   L11660  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L11660  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L11670  T=4 F=0  T=1 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=8   L11670  T=4 F=0  T=1 F=7  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=8   L11670  T=4 F=0  T=8 F=18  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=8   L11671  T=0 F=4  T=0 F=1  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=8   L11671  T=4 F=0  T=1 F=0  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=8   L11678  T=0 F=4  T=0 F=26  if ((RAW == '/') && (NXT(1) == '>')) {
  d=8   L11707  T=4 F=0  T=22 F=4  if (RAW == '>') {
  d=8   L11721  T=12 F=17  T=60 F=174  case XML_PARSER_CONTENT: {
  d=8   L11722  T=0 F=12  T=0 F=60  if ((avail < 2) && (ctxt->inputNr == 1))
  d=8   L11727  T=4 F=2  T=16 F=14  if ((cur == '<') && (next == '/')) {
  d=8   L11727  T=6 F=6  T=30 F=30  if ((cur == '<') && (next == '/')) {
  d=8   L11730  T=0 F=2  T=0 F=14  } else if ((cur == '<') && (next == '?')) {
  d=8   L11730  T=2 F=6  T=14 F=30  } else if ((cur == '<') && (next == '?')) {
  d=8   L11736  T=2 F=0  T=14 F=0  } else if ((cur == '<') && (next != '!')) {
  d=8   L11736  T=2 F=6  T=14 F=30  } else if ((cur == '<') && (next != '!')) {
  d=8   L11739  T=0 F=6  T=0 F=30  } else if ((cur == '<') && (next == '!') &&
  d=8   L11747  T=0 F=6  T=0 F=30  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=8   L11758  T=0 F=6  T=0 F=30  } else if ((cur == '<') && (next == '!') &&
  d=8   L11761  T=0 F=6  T=0 F=30  } else if (cur == '<') {
  d=8   L11765  T=0 F=6  T=0 F=30  } else if (cur == '&') {
  d=8   L11782  T=6 F=0  T=30 F=0  if ((ctxt->inputNr == 1) &&
  d=8   L11783  T=6 F=0  T=30 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=8   L11784  T=0 F=6  T=0 F=30  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=8   L11784  T=6 F=0  T=30 F=0  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=8   L11792  T=4 F=25  T=17 F=217  case XML_PARSER_END_TAG:
  d=8   L11793  T=0 F=4  T=0 F=17  if (avail < 2)
  d=8   L11795  T=0 F=4  T=2 F=14  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=8   L11795  T=4 F=0  T=16 F=1  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=8   L11797  T=4 F=0  T=12 F=3  if (ctxt->sax2) {
  d=8   L11805  T=0 F=4  T=0 F=15  if (ctxt->instate == XML_PARSER_EOF) {
  d=8   L11807  T=2 F=2  T=7 F=8  } else if (ctxt->nameNr == 0) {
  d=8   L11813  T=0 F=29  T=0 F=234  case XML_PARSER_CDATA_SECTION: {
  d=8   L11904  T=2 F=27  T=40 F=194  case XML_PARSER_MISC:
  d=8   L11905  T=2 F=27  T=18 F=216  case XML_PARSER_PROLOG:
  d=8   L11906  T=2 F=27  T=7 F=227  case XML_PARSER_EPILOG:
  d=8   L11908  T=0 F=6  T=0 F=65  if (ctxt->input->buf == NULL)
  d=8   L11914  T=2 F=4  T=5 F=60  if (avail < 2)
  d=8   L11918  T=4 F=0  T=58 F=2  if ((cur == '<') && (next == '?')) {
  d=8   L11918  T=0 F=4  T=0 F=58  if ((cur == '<') && (next == '?')) {
  d=8   L11929  T=2 F=2  T=40 F=18  } else if ((cur == '<') && (next == '!') &&
  d=8   L11929  T=4 F=0  T=58 F=2  } else if ((cur == '<') && (next == '!') &&
  d=8   L11930  T=0 F=2  T=0 F=40  (ctxt->input->cur[2] == '-') &&
  d=8   L11942  T=2 F=2  T=40 F=20  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=8   L11943  T=2 F=0  T=40 F=0  (cur == '<') && (next == '!') &&
  d=8   L11943  T=2 F=0  T=40 F=0  (cur == '<') && (next == '!') &&
  d=8   L11944  T=2 F=0  T=40 F=0  (ctxt->input->cur[2] == 'D') &&
  d=8   L11945  T=2 F=0  T=40 F=0  (ctxt->input->cur[3] == 'O') &&
  d=8   L11946  T=2 F=0  T=40 F=0  (ctxt->input->cur[4] == 'C') &&
  d=8   L11947  T=2 F=0  T=40 F=0  (ctxt->input->cur[5] == 'T') &&
  d=8   L11948  T=2 F=0  T=40 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=8   L11949  T=2 F=0  T=40 F=0  (ctxt->input->cur[7] == 'P') &&
  d=8   L11950  T=2 F=0  T=40 F=0  (ctxt->input->cur[8] == 'E')) {
  d=8   L11951  T=2 F=0  T=40 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11951  T=0 F=2  T=0 F=40  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11959  T=0 F=2  T=0 F=40  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L11961  T=0 F=2  T=0 F=40  if (RAW == '[') {
  d=8   L11972  T=2 F=0  T=40 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=8   L11972  T=2 F=0  T=40 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=8   L11973  T=2 F=0  T=40 F=0  (ctxt->sax->externalSubset != NULL))
  d=8   L11985  T=0 F=2  T=0 F=18  } else if ((cur == '<') && (next == '!') &&
  d=8   L11985  T=2 F=0  T=18 F=2  } else if ((cur == '<') && (next == '!') &&
  d=8   L11989  T=0 F=2  T=2 F=18  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=8   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L12007  T=0 F=29  T=0 F=234  case XML_PARSER_DTD: {
  d=8   L12029  T=0 F=29  T=0 F=234  case XML_PARSER_COMMENT:
  d=8   L12038  T=0 F=29  T=0 F=234  case XML_PARSER_IGNORE:
  d=8   L12047  T=0 F=29  T=0 F=234  case XML_PARSER_PI:
  d=8   L12056  T=0 F=29  T=0 F=234  case XML_PARSER_ENTITY_DECL:
  d=8   L12065  T=0 F=29  T=0 F=234  case XML_PARSER_ENTITY_VALUE:
  d=8   L12074  T=0 F=29  T=0 F=234  case XML_PARSER_ATTRIBUTE_VALUE:
  d=8   L12083  T=0 F=29  T=0 F=234  case XML_PARSER_SYSTEM_LITERAL:
  d=8   L12092  T=0 F=29  T=0 F=234  case XML_PARSER_PUBLIC_LITERAL:
--- d=7  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=7   L8396  T=0 F=3  T=0 F=60  if (name == NULL) {
  d=7   L8409  T=3 F=0  T=60 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=7   L8420  T=3 F=0  T=60 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=7   L8420  T=3 F=0  T=60 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=7   L8421  T=3 F=0  T=60 F=0  (!ctxt->disableSAX))
  d=7   L8423  T=0 F=3  T=0 F=60  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L8430  T=0 F=3  T=0 F=60  if (RAW == '[')
  d=7   L8436  T=0 F=3  T=0 F=60  if (RAW != '>') {
--- d=7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=7   L10816  T=0 F=1  T=0 F=20  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=7   L10816  T=0 F=1  T=0 F=20  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=7   L10829  T=1 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L10829  T=1 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L10831  T=0 F=1  T=0 F=20  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10834  T=1 F=0  T=20 F=0  if ((ctxt->encoding == NULL) &&
  d=7   L10835  T=1 F=0  T=20 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=7   L10846  T=1 F=0  T=20 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=7   L10852  T=0 F=1  T=0 F=20  if (CUR == 0) {
  d=7   L10863  T=0 F=1  T=0 F=20  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=7   L10872  T=0 F=1  T=0 F=20  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=7   L10873  T=0 F=1  T=0 F=20  (ctxt->instate == XML_PARSER_EOF)) {
  d=7   L10884  T=1 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=7   L10884  T=1 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=7   L10884  T=1 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=7   L10886  T=0 F=1  T=0 F=20  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10888  T=1 F=0  T=20 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=7   L10888  T=1 F=0  T=20 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=7   L10889  T=1 F=0  T=20 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=7   L10889  T=0 F=1  T=0 F=20  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=7   L10907  T=0 F=1  T=0 F=20  if (RAW == '[') {
  d=7   L10918  T=1 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=7   L10918  T=1 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=7   L10919  T=1 F=0  T=20 F=0  (!ctxt->disableSAX))
  d=7   L10922  T=0 F=1  T=7 F=13  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10936  T=0 F=1  T=2 F=11  if (RAW != '<') {
  d=7   L10950  T=0 F=1  T=6 F=5  if (RAW != 0) {
  d=7   L10959  T=1 F=0  T=13 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L10959  T=1 F=0  T=13 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L10965  T=1 F=0  T=13 F=0  if ((ctxt->myDoc != NULL) &&
  d=7   L10966  T=0 F=1  T=0 F=13  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=7   L10971  T=1 F=0  T=1 F=12  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=7   L10973  T=0 F=1  T=1 F=0  if (ctxt->valid)
  d=7   L10980  T=0 F=1  T=12 F=1  if (! ctxt->wellFormed) {
--- d=5  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=5   L7099  T=3 F=0  T=59 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L7100  T=3 F=0  T=59 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=5   L7109  T=0 F=3  T=0 F=59  if (enc != XML_CHAR_ENCODING_NONE)
  d=5   L7123  T=0 F=3  T=0 F=59  if (ctxt->myDoc == NULL) {
  d=5   L7131  T=0 F=3  T=0 F=59  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=5   L7131  T=3 F=0  T=59 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=5   L7137  T=9 F=0  T=223 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=5   L7137  T=6 F=3  T=185 F=38  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=5   L7139  T=6 F=0  T=164 F=3  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=5   L7139  T=6 F=0  T=167 F=18  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=5   L7139  T=0 F=6  T=0 F=164  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=5   L7141  T=0 F=0  T=0 F=3  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=5   L7141  T=6 F=0  T=167 F=18  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=5   L7141  T=6 F=0  T=164 F=3  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=5   L7151  T=0 F=3  T=0 F=38  if (RAW != 0) {
--- d=4  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=4   L6952  T=6 F=0  T=164 F=0  if (CUR == '<') {
  d=4   L6953  T=6 F=0  T=164 F=0  if (NXT(1) == '!') {
  d=4   L6955  T=6 F=0  T=122 F=42  case 'E':
  d=4   L6956  T=6 F=0  T=122 F=0  if (NXT(3) == 'L')
  d=4   L6963  T=0 F=6  T=42 F=122  case 'A':
  d=4   L6966  T=0 F=6  T=0 F=164  case 'N':
  d=4   L6969  T=0 F=6  T=0 F=164  case '-':
  d=4   L6972  T=0 F=6  T=0 F=164  default:
  d=4   L6986  T=0 F=6  T=0 F=164  if (ctxt->instate == XML_PARSER_EOF)
--- d=3  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788) ---
  d=3   L6698  T=0 F=6  T=0 F=122  if ((CUR != '<') || (NXT(1) != '!'))
  d=3   L6698  T=0 F=6  T=0 F=122  if ((CUR != '<') || (NXT(1) != '!'))
  d=3   L6707  T=0 F=6  T=0 F=122  if (SKIP_BLANKS == 0) {
  d=3   L6713  T=0 F=6  T=3 F=119  if (name == NULL) {
  d=3   L6718  T=0 F=6  T=6 F=113  if (SKIP_BLANKS == 0) {
  d=3   L6728  T=0 F=6  T=0 F=119  } else if ((RAW == 'A') && (NXT(1) == 'N') &&
  d=3   L6735  T=6 F=0  T=119 F=0  } else if (RAW == '(') {
  d=3   L6754  T=0 F=6  T=15 F=104  if (RAW != '>') {
  d=3   L6756  T=0 F=0  T=3 F=12  if (content != NULL) {
  d=3   L6760  T=0 F=6  T=0 F=104  if (inputid != ctxt->input->id) {
  d=3   L6767  T=6 F=0  T=104 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L6767  T=6 F=0  T=83 F=21  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L6768  T=6 F=0  T=83 F=0  (ctxt->sax->elementDecl != NULL)) {
  d=3   L6769  T=6 F=0  T=83 F=0  if (content != NULL)
  d=3   L6773  T=6 F=0  T=83 F=0  if ((content != NULL) && (content->parent == NULL)) {
  d=3   L6773  T=0 F=6  T=0 F=83  if ((content != NULL) && (content->parent == NULL)) {
  d=3   L6782  T=0 F=0  T=21 F=0  } else if (content != NULL) {
--- d=2  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675) ---
  d=2   L6655  T=0 F=6  T=0 F=119  if (RAW != '(') {
  d=2   L6662  T=0 F=6  T=0 F=119  if (ctxt->instate == XML_PARSER_EOF)
--- d=1  parser.c:xmlParseElementChildrenContentDeclPriv  (/src/libxml2/parser.c:6320-6589) ---
  d=1   L6325  T=0 F=6  T=0 F=77  if (((depth > 128) && ((ctxt->options & XML_PARSE_HUGE) =...
  d=1   L6326  T=0 F=6  T=0 F=77  (depth >  2048)) {
  d=1   L6334  T=0 F=6  T=0 F=77  if (RAW == '(') {
  d=1   L6348  T=0 F=6  T=12 F=65  if (elem == NULL) {
  d=1   L6353  T=0 F=6  T=0 F=65  if (cur == NULL) {
  d=1   L6358  T=0 F=6  T=0 F=65  if (RAW == '?') {
  d=1   L6361  T=3 F=3  T=53 F=12  } else if (RAW == '*') {
  d=1   L6364  T=0 F=3  T=0 F=12  } else if (RAW == '+') {
  d=1   L6374  T=3 F=0  T=0 F=0  while ((RAW != ')') && (ctxt->instate != XML_PARSER_EOF)) {
  d=1   L6374  T=3 F=6  T=0 F=65  while ((RAW != ')') && (ctxt->instate != XML_PARSER_EOF)) {
  d=1   L6378  T=0 F=3  T=0 F=0  if (RAW == ',') {
  d=1   L6418  T=3 F=0  T=0 F=0  } else if (RAW == '|') {
  d=1   L6419  T=3 F=0  T=0 F=0  if (type == 0) type = CUR;
  d=1   L6437  T=0 F=3  T=0 F=0  if (op == NULL) {
  d=1   L6444  T=3 F=0  T=0 F=0  if (last == NULL) {
  d=1   L6446  T=3 F=0  T=0 F=0  if (ret != NULL)
  d=1   L6470  T=0 F=3  T=0 F=0  if (RAW == '(') {
  d=1   L6485  T=0 F=3  T=0 F=0  if (elem == NULL) {
  d=1   L6492  T=0 F=3  T=0 F=0  if (last == NULL) {
  d=1   L6497  T=0 F=3  T=0 F=0  if (RAW == '?') {
  d=1   L6500  T=0 F=3  T=0 F=0  } else if (RAW == '*') {
  d=1   L6503  T=0 F=3  T=0 F=0  } else if (RAW == '+') {
  d=1   L6513  T=6 F=0  T=65 F=0  if ((cur != NULL) && (last != NULL)) {  <-- BLOCKER
  d=1   L6513  T=3 F=3  T=0 F=65  if ((cur != NULL) && (last != NULL)) {  <-- BLOCKER
  d=1   L6515  T=3 F=0  T=0 F=0  if (last != NULL)
  d=1   L6518  T=0 F=6  T=0 F=65  if (ctxt->input->id != inputchk) {
  d=1   L6524  T=0 F=6  T=0 F=65  if (RAW == '?') {
  d=1   L6533  T=0 F=6  T=0 F=65  } else if (RAW == '*') {
  d=1   L6554  T=0 F=6  T=0 F=65  } else if (RAW == '+') {

[off-chain: 816 additional divergent branches across 80 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=ae2d760d094b65d2, size=348 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=48779s, mutation_op=BytesInsertCopyMutator,DwordInterestingMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 74 74 70 3a 40 2f 55 77 77 2b 77 33 2e 6f 72 67   ttp:@/Uww+w3.org
  0010: 2f 31 0a 39 39 2f 78 6c 69 6e 6b 27 0a 21 20 20   /1.99/xlink'.!  
  0020: 9f 20 28 20 20 20 20 20 20 78 9f 24 8c 8c 8c 8c   . (      x.$....
  0030: 8c 8c 8c 8c 8c 8c 8c 78 6d 6c 6e 73 3a 78 6c 69   .......xmlns:xli

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00f7af173db700b0, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=0s, mutation_op=BytesExpandMutator,DwordAddMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=076df8c667aefde7, size=373 bytes, fuzzer=cmplog, trial=2, discovered_at=3s, mutation_op=TokenInsert):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=1304b2db6f79e42f, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=9s, mutation_op=BytesInsertCopyMutator,ByteIncMutator,DwordAddMutator,BytesSetMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=0affb903cd14449e, size=374 bytes, fuzzer=cmplog, trial=2, discovered_at=10s, mutation_op=BytesInsertCopyMutator,BytesRandInsertMutator,BytesDeleteMutator):
  0000: 06 00 00 00 31 32 37 37 55 54 46 2d 31 36 37 32   ....1277UTF-1672
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
Seed 5 (id=09e016bbcb2dd021, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=15s, mutation_op=BytesDeleteMutator,BytesCopyMutator,QwordAddMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 09   .0"?>.<!DOCTYPE.
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  74(t)x1                             06(.)x15 5f(_)x1 31(1)x1 2b(+)x1 +2u  DIFFER
   0x0001  74(t)x1                             00(.)x15 5f(_)x1 7e(~)x1 32(2)x1 +2u  DIFFER
   0x0002  70(p)x1                             00(.)x14 5f(_)x1 23(#)x1 37(7)x1 +3u  DIFFER
   0x0003  3a(:)x1                             00(.)x17 23(#)x1 37(7)x1 22(")x1    DIFFER
   0x0004  40(@)x1                             31(1)x16 23(#)x1 37(7)x1 67(g)x1 +1u  DIFFER
   0x0005  2f(/)x1                             32(2)x17 27(')x1 74(t)x1 00(.)x1    DIFFER
   0x0006  55(U)x1                             37(7)x16 73(s)x1 2e(.)x1 74(t)x1 +1u  DIFFER
   0x0007  77(w)x1                             37(7)x16 69(i)x1 78(x)x1 70(p)x1 +1u  DIFFER
   0x0008  77(w)x1                             37(7)x16 6d(m)x2 55(U)x1 3a(:)x1    DIFFER
   0x0009  2b(+)x1                             32(2)x15 54(T)x1 70(p)x1 6c(l)x1 +2u  DIFFER
   0x000a  77(w)x1                             2e(.)x15 46(F)x1 6c(l)x1 5c(\)x1 +2u  DIFFER
   0x000b  33(3)x1                             78(x)x15 2d(-)x1 65(e)x1 0a(.)x1 +2u  DIFFER
   0x000c  2e(.)x1                             6d(m)x15 31(1)x1 27(')x1 3c(<)x1 +2u  PARTIAL
   0x000d  6f(o)x1                             6c(l)x15 36(6)x1 0a(.)x1 3f(?)x1 +2u  DIFFER
   0x000e  72(r)x1                             5c(\)x15 37(7)x1 20( )x1 78(x)x1 +2u  DIFFER
   0x000f  67(g)x1                             0a(.)x15 32(2)x1 20( )x1 6d(m)x1 +2u  DIFFER
   0x0010  2f(/)x1                             3c(<)x15 2e(.)x1 20( )x1 6c(l)x1 +2u  DIFFER
   0x0011  31(1)x1                             3f(?)x15 20( )x2 78(x)x1 10(.)x1 +1u  DIFFER
   0x0012  0a(.)x1                             78(x)x15 6d(m)x1 20( )x1 76(v)x1 +2u  DIFFER
   0x0013  39(9)x1                             6d(m)x15 6c(l)x1 20( )x1 65(e)x1 +2u  DIFFER
   0x0014  39(9)x1                             6c(l)x15 5c(\)x1 20( )x1 72(r)x1 +2u  DIFFER
   0x0015  2f(/)x1                             20( )x15 0a(.)x1 23(#)x1 73(s)x1 +2u  DIFFER
   0x0016  78(x)x1                             76(v)x15 3c(<)x1 23(#)x1 69(i)x1 +2u  DIFFER
   0x0017  6c(l)x1                             65(e)x15 3f(?)x1 23(#)x1 6f(o)x1 +2u  DIFFER
   0x0018  69(i)x1                             72(r)x15 78(x)x1 23(#)x1 6e(n)x1 +2u  DIFFER
   0x0019  6e(n)x1                             73(s)x15 6d(m)x1 23(#)x1 3d(=)x1 +2u  DIFFER
   0x001a  6b(k)x1                             69(i)x15 6c(l)x1 23(#)x1 22(")x1 +2u  DIFFER
   0x001b  27(')x1                             6f(o)x15 20( )x1 23(#)x1 31(1)x1 +2u  DIFFER
   0x001c  0a(.)x1                             6e(n)x15 76(v)x1 23(#)x1 2e(.)x1 +2u  DIFFER
   0x001d  21(!)x1                             3d(=)x15 65(e)x1 23(#)x1 30(0)x1 +2u  DIFFER
   0x001e  20( )x1                             22(")x16 72(r)x1 23(#)x1 ff(.)x1 +1u  DIFFER
   0x001f  20( )x1                             31(1)x15 73(s)x1 23(#)x1 3f(?)x1 +2u  DIFFER
   0x0020  9f(.)x1                             2e(.)x15 69(i)x1 00(.)x1 3e(>)x1 +2u  DIFFER
   0x0021  20( )x1                             30(0)x15 6f(o)x1 00(.)x1 0a(.)x1 +2u  DIFFER
   0x0022  28(()x1                             22(")x15 6e(n)x1 31(1)x1 3c(<)x1 +2u  DIFFER
   0x0023  20( )x1                             3f(?)x15 3d(=)x1 32(2)x1 21(!)x1 +2u  DIFFER
   0x0024  20( )x1                             3e(>)x15 22(")x2 37(7)x1 44(D)x1 +1u  DIFFER
   0x0025  20( )x1                             0a(.)x14 31(1)x1 37(7)x1 4f(O)x1 +3u  DIFFER
   0x0026  20( )x1                             3c(<)x15 2e(.)x1 37(7)x1 43(C)x1 +2u  DIFFER
   0x0027  20( )x1                             21(!)x16 30(0)x1 32(2)x1 54(T)x1 +1u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6654.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6654,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6654 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6654 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6654 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).