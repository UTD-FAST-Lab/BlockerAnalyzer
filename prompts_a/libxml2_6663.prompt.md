==== BLOCKER ====
Target: libxml2
Branch ID: 6663
Location: /src/libxml2/parser.c:6728:13
Enclosing function: xmlParseElementDecl
Source line: 	} else if ((RAW == 'A') && (NXT(1) == 'N') &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           0       10          0  loser (value_profile vs value_profile_cmplog)
value_profile                    5        5          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=11.70h  loser=23.90h
  avg hitcount on branch: winner=3  loser=0
  prob_div=0.80  dur_div=12.20h  hit_div=3
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6663/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseElementDecl (/src/libxml2/parser.c:6693-6788) ---
[ ]  6691   */
[ ]  6692  int
[B]  6693  xmlParseElementDecl(xmlParserCtxtPtr ctxt) {
[B]  6694      const xmlChar *name;
[B]  6695      int ret = -1;
[B]  6696      xmlElementContentPtr content  = NULL;
[ ]  6697  
[B]  6698      if ((CUR != '<') || (NXT(1) != '!'))
[ ]  6699          return(ret);
[B]  6700      SKIP(2);
[ ]  6701  
[ ]  6702      /* GROW; done in the caller */
[B]  6703      if (CMP7(CUR_PTR, 'E', 'L', 'E', 'M', 'E', 'N', 'T')) {
[B]  6704  	int inputid = ctxt->input->id;
[ ]  6705  
[B]  6706  	SKIP(7);
[B]  6707  	if (SKIP_BLANKS == 0) {
[ ]  6708  	    xmlFatalErrMsg(ctxt, XML_ERR_SPACE_REQUIRED,
[ ]  6709  		           "Space required after 'ELEMENT'\n");
[ ]  6710  	    return(-1);
[ ]  6711  	}
[B]  6712          name = xmlParseName(ctxt);
[B]  6713  	if (name == NULL) {
[L]  6714  	    xmlFatalErrMsg(ctxt, XML_ERR_NAME_REQUIRED,
[L]  6715  			   "xmlParseElementDecl: no name for Element\n");
[L]  6716  	    return(-1);
[L]  6717  	}
[B]  6718  	if (SKIP_BLANKS == 0) {
[L]  6719  	    xmlFatalErrMsg(ctxt, XML_ERR_SPACE_REQUIRED,
[L]  6720  			   "Space required after the element name\n");
[L]  6721  	}
[B]  6722  	if (CMP5(CUR_PTR, 'E', 'M', 'P', 'T', 'Y')) {
[ ]  6723  	    SKIP(5);
[ ]  6724  	    /*
[ ]  6725  	     * Element must always be empty.
[ ]  6726  	     */
[ ]  6727  	    ret = XML_ELEMENT_TYPE_EMPTY;
[B]  6728  	} else if ((RAW == 'A') && (NXT(1) == 'N') && <-- BLOCKER
[B]  6729  	           (NXT(2) == 'Y')) {
[ ]  6730  	    SKIP(3);
[ ]  6731  	    /*
[ ]  6732  	     * Element is a generic container.
[ ]  6733  	     */
[ ]  6734  	    ret = XML_ELEMENT_TYPE_ANY;
[B]  6735  	} else if (RAW == '(') {
[B]  6736  	    ret = xmlParseElementContentDecl(ctxt, name, &content);
[B]  6737  	} else {
[ ]  6738  	    /*
[ ]  6739  	     * [ WFC: PEs in Internal Subset ] error handling.
[ ]  6740  	     */
[W]  6741  	    if ((RAW == '%') && (ctxt->external == 0) &&
[W]  6742  	        (ctxt->inputNr == 1)) {
[ ]  6743  		xmlFatalErrMsg(ctxt, XML_ERR_PEREF_IN_INT_SUBSET,
[ ]  6744  	  "PEReference: forbidden within markup decl in internal subset\n");
[W]  6745  	    } else {
[W]  6746  		xmlFatalErrMsg(ctxt, XML_ERR_ELEMCONTENT_NOT_STARTED,
[W]  6747  		      "xmlParseElementDecl: 'EMPTY', 'ANY' or '(' expected\n");
[W]  6748              }
[W]  6749  	    return(-1);
[W]  6750  	}
[ ]  6751  
[B]  6752  	SKIP_BLANKS;
[ ]  6753  
[B]  6754  	if (RAW != '>') {
[L]  6755  	    xmlFatalErr(ctxt, XML_ERR_GT_REQUIRED, NULL);
[L]  6756  	    if (content != NULL) {
[ ]  6757  		xmlFreeDocElementContent(ctxt->myDoc, content);
[ ]  6758  	    }
[B]  6759  	} else {
[B]  6760  	    if (inputid != ctxt->input->id) {
[ ]  6761  		xmlFatalErrMsg(ctxt, XML_ERR_ENTITY_BOUNDARY,
[ ]  6762                                 "Element declaration doesn't start and stop in"
[ ]  6763                                 " the same entity\n");
[ ]  6764  	    }
[ ]  6765  
[B]  6766  	    NEXT;
[B]  6767  	    if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
[B]  6768  		(ctxt->sax->elementDecl != NULL)) {
[L]  6769  		if (content != NULL)
[L]  6770  		    content->parent = NULL;
[L]  6771  	        ctxt->sax->elementDecl(ctxt->userData, name, ret,
[L]  6772  		                       content);
[L]  6773  		if ((content != NULL) && (content->parent == NULL)) {
[ ]  6774  		    /*
[ ]  6775  		     * this is a trick: if xmlAddElementDecl is called,
[ ]  6776  		     * instead of copying the full tree it is plugged directly
[ ]  6777  		     * if called from the parser. Avoid duplicating the
[ ]  6778  		     * interfaces or change the API/ABI
[ ]  6779  		     */
[ ]  6780  		    xmlFreeDocElementContent(ctxt->myDoc, content);
[ ]  6781  		}
[B]  6782  	    } else if (content != NULL) {
[L]  6783  		xmlFreeDocElementContent(ctxt->myDoc, content);
[L]  6784  	    }
[B]  6785  	}
[B]  6786      }
[B]  6787      return(ret);
[B]  6788  }

--- Caller (1 hop): xmlParseMarkupDecl (/src/libxml2/parser.c:6950-6990, calls xmlParseElementDecl at line 6957) (±10 around call site) ---
[B]  6950  xmlParseMarkupDecl(xmlParserCtxtPtr ctxt) {
[B]  6951      GROW;
[B]  6952      if (CUR == '<') {
[B]  6953          if (NXT(1) == '!') {
[B]  6954  	    switch (NXT(2)) {
[B]  6955  	        case 'E':
[B]  6956  		    if (NXT(3) == 'L')
[B]  6957  			xmlParseElementDecl(ctxt); <-- CALL
[ ]  6958  		    else if (NXT(3) == 'N')
[ ]  6959  			xmlParseEntityDecl(ctxt);
[ ]  6960                      else
[ ]  6961                          SKIP(2);
[B]  6962  		    break;
[L]  6963  	        case 'A':
[L]  6964  		    xmlParseAttributeListDecl(ctxt);
[L]  6965  		    break;
[ ]  6966  	        case 'N':
[ ]  6967  		    xmlParseNotationDecl(ctxt);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseElementDecl at line 6957)
hop 3  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 3  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 4  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 4  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 4  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 5  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 5  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)
hop 6  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseDocTypeDecl at line 11958)
hop 6  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 6  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 6  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)
hop 7  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 7  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 8  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 8  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 8  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     469      7030  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     118      5680  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     159      5040  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      42      1070  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       0       593  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      36       423  inputPop  (/src/libxml2/parser.c:1723-1738)
      13       390  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
       3       271  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
      13       277  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)  <-- enclosing
      22       281  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
      22       281  inputPush  (/src/libxml2/parser.c:1693-1712)
       0       253  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)
       1       240  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
       0       236  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
       0       211  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203)
... (82 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=7   L12139  T=0 F=12  T=0 F=145  if (ctxt == NULL)
  d=7   L12141  T=4 F=0  T=42 F=9  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12141  T=4 F=8  T=51 F=94  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12143  T=0 F=8  T=0 F=103  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L12145  T=0 F=8  T=0 F=103  if (ctxt->input == NULL)
  d=7   L12149  T=8 F=0  T=94 F=9  if (ctxt->instate == XML_PARSER_START)
  d=7   L12151  T=8 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=7   L12151  T=8 F=0  T=96 F=7  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=7   L12151  T=8 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=7   L12152  T=0 F=8  T=0 F=96  (chunk[size - 1] == '\r')) {
  d=7   L12159  T=8 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=7   L12159  T=8 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=7   L12159  T=8 F=0  T=96 F=7  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=7   L12160  T=8 F=0  T=96 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=7   L12160  T=8 F=0  T=96 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=7   L12170  T=8 F=0  T=94 F=2  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=7   L12170  T=8 F=0  T=94 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=7   L12171  T=8 F=0  T=94 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=7   L12171  T=0 F=8  T=0 F=94  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=7   L12202  T=0 F=8  T=0 F=96  if (res < 0) {
  d=7   L12211  T=0 F=0  T=7 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=7   L12212  T=0 F=0  T=7 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=7   L12212  T=0 F=0  T=7 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=7   L12214  T=0 F=0  T=0 F=7  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=7   L12233  T=0 F=8  T=0 F=103  if (remain != 0) {
  d=7   L12238  T=2 F=6  T=12 F=91  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L12241  T=6 F=0  T=91 F=0  if ((ctxt->input != NULL) &&
  d=7   L12242  T=0 F=6  T=0 F=91  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=7   L12243  T=0 F=6  T=0 F=91  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=7   L12248  T=6 F=0  T=73 F=18  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12248  T=6 F=0  T=91 F=0  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12251  T=0 F=0  T=0 F=18  if (remain != 0) {
  d=7   L12257  T=0 F=0  T=0 F=18  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=7   L12268  T=0 F=0  T=5 F=13  if (terminate) {
  d=7   L12274  T=0 F=0  T=5 F=0  if (ctxt->input != NULL) {
  d=7   L12275  T=0 F=0  T=0 F=5  if (ctxt->input->buf == NULL)
  d=7   L12283  T=0 F=0  T=5 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=7   L12284  T=0 F=0  T=1 F=4  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=7   L12287  T=0 F=0  T=0 F=4  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=7   L12287  T=0 F=0  T=4 F=1  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=7   L12290  T=0 F=0  T=5 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=7   L12291  T=0 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L12291  T=0 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L12296  T=0 F=0  T=13 F=5  if (ctxt->wellFormed == 0)
--- d=6  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=6   L11409  T=0 F=8  T=0 F=103  if (ctxt->input == NULL)
  d=6   L11465  T=8 F=0  T=103 F=0  if ((ctxt->input != NULL) &&
  d=6   L11466  T=0 F=8  T=0 F=103  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=6   L11470  T=45 F=0  T=574 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=6   L11471  T=6 F=3  T=73 F=150  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L11471  T=9 F=36  T=223 F=351  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L11474  T=0 F=39  T=0 F=501  if (ctxt->input == NULL) break;
  d=6   L11475  T=0 F=39  T=0 F=501  if (ctxt->input->buf == NULL)
  d=6   L11486  T=24 F=15  T=358 F=143  if ((ctxt->instate != XML_PARSER_START) &&
  d=6   L11487  T=0 F=24  T=0 F=358  (ctxt->input->buf->raw != NULL) &&
  d=6   L11500  T=0 F=39  T=6 F=495  if (avail < 1)
  d=6   L11502  T=0 F=39  T=0 F=495  switch (ctxt->instate) {
  d=6   L11503  T=0 F=39  T=0 F=495  case XML_PARSER_EOF:
  d=6   L11508  T=15 F=24  T=143 F=352  case XML_PARSER_START:
  d=6   L11509  T=7 F=8  T=49 F=94  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=6   L11516  T=0 F=7  T=0 F=49  if (avail < 4)
  d=6   L11535  T=0 F=8  T=0 F=94  if (avail < 2)
  d=6   L11539  T=0 F=8  T=0 F=94  if (cur == 0) {
  d=6   L11553  T=8 F=0  T=92 F=2  if ((cur == '<') && (next == '?')) {
  d=6   L11553  T=8 F=0  T=94 F=0  if ((cur == '<') && (next == '?')) {
  d=6   L11555  T=0 F=8  T=0 F=92  if (avail < 5) goto done;
  d=6   L11556  T=8 F=0  T=92 F=0  if ((!terminate) &&
  d=6   L11557  T=0 F=8  T=0 F=92  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=6   L11559  T=8 F=0  T=92 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11559  T=8 F=0  T=92 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11562  T=2 F=6  T=92 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=6   L11563  T=2 F=0  T=90 F=2  (ctxt->input->cur[3] == 'm') &&
  d=6   L11564  T=2 F=0  T=90 F=0  (ctxt->input->cur[4] == 'l') &&
  d=6   L11572  T=0 F=2  T=0 F=90  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=6   L11581  T=2 F=0  T=90 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L11582  T=0 F=2  T=0 F=90  (ctxt->input->encoding != NULL))
  d=6   L11584  T=2 F=0  T=90 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11584  T=2 F=0  T=90 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11585  T=2 F=0  T=90 F=0  (!ctxt->disableSAX))
  d=6   L11594  T=6 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11594  T=6 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11595  T=6 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=6   L11604  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11604  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11608  T=0 F=0  T=0 F=2  if (ctxt->version == NULL) {
  d=6   L11612  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11612  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11613  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=6   L11622  T=4 F=35  T=72 F=423  case XML_PARSER_START_TAG: {
  d=6   L11629  T=0 F=4  T=0 F=72  if ((avail < 2) && (ctxt->inputNr == 1))
  d=6   L11632  T=0 F=4  T=3 F=69  if (cur != '<') {
  d=6   L11635  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11635  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11639  T=0 F=4  T=3 F=64  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11639  T=4 F=0  T=67 F=2  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11641  T=0 F=4  T=0 F=66  if (ctxt->spaceNr == 0)
  d=6   L11643  T=0 F=4  T=4 F=62  else if (*ctxt->space == -2)
  d=6   L11648  T=2 F=2  T=48 F=18  if (ctxt->sax2)
  d=6   L11655  T=0 F=4  T=0 F=66  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11657  T=2 F=2  T=7 F=59  if (name == NULL) {
  d=6   L11660  T=2 F=0  T=7 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11660  T=2 F=0  T=7 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11670  T=0 F=0  T=8 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L11670  T=0 F=0  T=8 F=11  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L11670  T=0 F=2  T=19 F=40  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L11671  T=0 F=0  T=0 F=8  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=6   L11671  T=0 F=0  T=8 F=0  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=6   L11678  T=0 F=2  T=0 F=59  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L11707  T=2 F=0  T=48 F=11  if (RAW == '>') {
  d=6   L11721  T=4 F=35  T=120 F=375  case XML_PARSER_CONTENT: {
  d=6   L11722  T=0 F=4  T=0 F=120  if ((avail < 2) && (ctxt->inputNr == 1))
  d=6   L11727  T=0 F=2  T=20 F=35  if ((cur == '<') && (next == '/')) {
  d=6   L11727  T=2 F=2  T=55 F=65  if ((cur == '<') && (next == '/')) {
  d=6   L11730  T=0 F=2  T=0 F=35  } else if ((cur == '<') && (next == '?')) {
  d=6   L11730  T=2 F=2  T=35 F=65  } else if ((cur == '<') && (next == '?')) {
  d=6   L11736  T=2 F=0  T=35 F=0  } else if ((cur == '<') && (next != '!')) {
  d=6   L11736  T=2 F=2  T=35 F=65  } else if ((cur == '<') && (next != '!')) {
  d=6   L11739  T=0 F=2  T=0 F=65  } else if ((cur == '<') && (next == '!') &&
  d=6   L11747  T=0 F=2  T=0 F=65  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=6   L11758  T=0 F=2  T=0 F=65  } else if ((cur == '<') && (next == '!') &&
  d=6   L11761  T=0 F=2  T=0 F=65  } else if (cur == '<') {
  d=6   L11765  T=0 F=2  T=1 F=64  } else if (cur == '&') {
  d=6   L11766  T=0 F=0  T=0 F=1  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=6   L11782  T=2 F=0  T=64 F=0  if ((ctxt->inputNr == 1) &&
  d=6   L11783  T=2 F=0  T=64 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=6   L11784  T=0 F=2  T=2 F=60  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=6   L11784  T=2 F=0  T=62 F=2  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=6   L11792  T=0 F=39  T=20 F=475  case XML_PARSER_END_TAG:
  d=6   L11793  T=0 F=0  T=0 F=20  if (avail < 2)
  d=6   L11795  T=0 F=0  T=0 F=20  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=6   L11795  T=0 F=0  T=20 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=6   L11797  T=0 F=0  T=12 F=8  if (ctxt->sax2) {
  d=6   L11805  T=0 F=0  T=0 F=20  if (ctxt->instate == XML_PARSER_EOF) {
  d=6   L11807  T=0 F=0  T=8 F=12  } else if (ctxt->nameNr == 0) {
  d=6   L11813  T=0 F=39  T=0 F=495  case XML_PARSER_CDATA_SECTION: {
  d=6   L11904  T=14 F=25  T=96 F=399  case XML_PARSER_MISC:
  d=6   L11905  T=2 F=37  T=35 F=460  case XML_PARSER_PROLOG:
  d=6   L11906  T=0 F=39  T=9 F=486  case XML_PARSER_EPILOG:
  d=6   L11908  T=0 F=16  T=0 F=140  if (ctxt->input->buf == NULL)
  d=6   L11914  T=0 F=16  T=7 F=133  if (avail < 2)
  d=6   L11918  T=16 F=0  T=130 F=3  if ((cur == '<') && (next == '?')) {
  d=6   L11918  T=6 F=10  T=2 F=128  if ((cur == '<') && (next == '?')) {
  d=6   L11919  T=6 F=0  T=2 F=0  if ((!terminate) &&
  d=6   L11920  T=0 F=6  T=0 F=2  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=6   L11927  T=0 F=6  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11929  T=8 F=2  T=94 F=34  } else if ((cur == '<') && (next == '!') &&
  d=6   L11929  T=10 F=0  T=128 F=3  } else if ((cur == '<') && (next == '!') &&
  d=6   L11930  T=0 F=8  T=0 F=94  (ctxt->input->cur[2] == '-') &&
  d=6   L11942  T=8 F=2  T=94 F=37  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=6   L11943  T=8 F=0  T=94 F=0  (cur == '<') && (next == '!') &&
  d=6   L11943  T=8 F=0  T=94 F=0  (cur == '<') && (next == '!') &&
  d=6   L11944  T=8 F=0  T=94 F=0  (ctxt->input->cur[2] == 'D') &&
  d=6   L11945  T=8 F=0  T=94 F=0  (ctxt->input->cur[3] == 'O') &&
  d=6   L11946  T=8 F=0  T=94 F=0  (ctxt->input->cur[4] == 'C') &&
  d=6   L11947  T=8 F=0  T=94 F=0  (ctxt->input->cur[5] == 'T') &&
  d=6   L11948  T=8 F=0  T=94 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=6   L11949  T=8 F=0  T=94 F=0  (ctxt->input->cur[7] == 'P') &&
  d=6   L11950  T=8 F=0  T=94 F=0  (ctxt->input->cur[8] == 'E')) {
  d=6   L11951  T=8 F=0  T=94 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11951  T=0 F=8  T=0 F=94  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11959  T=0 F=8  T=0 F=94  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11961  T=0 F=8  T=0 F=94  if (RAW == '[') {
  d=6   L11972  T=8 F=0  T=94 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=6   L11972  T=8 F=0  T=94 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=6   L11973  T=8 F=0  T=94 F=0  (ctxt->sax->externalSubset != NULL))
  d=6   L11985  T=0 F=2  T=0 F=34  } else if ((cur == '<') && (next == '!') &&
  d=6   L11985  T=2 F=0  T=34 F=3  } else if ((cur == '<') && (next == '!') &&
  d=6   L11989  T=0 F=2  T=2 F=35  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=6   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12007  T=0 F=39  T=0 F=495  case XML_PARSER_DTD: {
  d=6   L12029  T=0 F=39  T=0 F=495  case XML_PARSER_COMMENT:
  d=6   L12038  T=0 F=39  T=0 F=495  case XML_PARSER_IGNORE:
  d=6   L12047  T=0 F=39  T=0 F=495  case XML_PARSER_PI:
  d=6   L12056  T=0 F=39  T=0 F=495  case XML_PARSER_ENTITY_DECL:
  d=6   L12065  T=0 F=39  T=0 F=495  case XML_PARSER_ENTITY_VALUE:
  d=6   L12074  T=0 F=39  T=0 F=495  case XML_PARSER_ATTRIBUTE_VALUE:
  d=6   L12083  T=0 F=39  T=0 F=495  case XML_PARSER_SYSTEM_LITERAL:
  d=6   L12092  T=0 F=39  T=0 F=495  case XML_PARSER_PUBLIC_LITERAL:
--- d=5  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=5   L8396  T=0 F=12  T=0 F=141  if (name == NULL) {
  d=5   L8409  T=12 F=0  T=141 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=5   L8420  T=12 F=0  T=141 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=5   L8420  T=12 F=0  T=141 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=5   L8421  T=12 F=0  T=141 F=0  (!ctxt->disableSAX))
  d=5   L8423  T=0 F=12  T=0 F=141  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L8430  T=0 F=12  T=0 F=141  if (RAW == '[')
  d=5   L8436  T=0 F=12  T=0 F=141  if (RAW != '>') {
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10816  T=0 F=4  T=0 F=47  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10816  T=0 F=4  T=0 F=47  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10829  T=4 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10829  T=4 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10831  T=0 F=4  T=0 F=47  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10834  T=4 F=0  T=47 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L10835  T=4 F=0  T=47 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=5   L10846  T=1 F=3  T=45 F=2  if (enc != XML_CHAR_ENCODING_NONE) {
  d=5   L10852  T=0 F=4  T=0 F=47  if (CUR == 0) {
  d=5   L10863  T=0 F=4  T=0 F=47  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=5   L10872  T=0 F=1  T=0 F=45  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=5   L10873  T=0 F=1  T=0 F=45  (ctxt->instate == XML_PARSER_EOF)) {
  d=5   L10884  T=4 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=4 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=4 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10886  T=0 F=4  T=0 F=47  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10888  T=4 F=0  T=47 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10888  T=4 F=0  T=47 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10889  T=4 F=0  T=47 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10889  T=0 F=4  T=0 F=47  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10907  T=0 F=4  T=0 F=47  if (RAW == '[') {
  d=5   L10918  T=4 F=0  T=47 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10918  T=4 F=0  T=47 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10919  T=4 F=0  T=47 F=0  (!ctxt->disableSAX))
  d=5   L10922  T=4 F=0  T=22 F=25  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10936  T=0 F=0  T=2 F=23  if (RAW != '<') {
  d=5   L10950  T=0 F=0  T=10 F=13  if (RAW != 0) {
  d=5   L10959  T=0 F=0  T=25 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10959  T=0 F=0  T=25 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10965  T=0 F=0  T=25 F=0  if ((ctxt->myDoc != NULL) &&
  d=5   L10966  T=0 F=0  T=0 F=25  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=5   L10971  T=0 F=0  T=1 F=24  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=5   L10971  T=0 F=0  T=1 F=0  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=5   L10973  T=0 F=0  T=1 F=0  if (ctxt->valid)
  d=5   L10975  T=0 F=0  T=0 F=1  if (ctxt->nsWellFormed)
  d=5   L10977  T=0 F=0  T=0 F=1  if (ctxt->options & XML_PARSE_OLD10)
  d=5   L10980  T=0 F=0  T=24 F=1  if (! ctxt->wellFormed) {
--- d=3  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=3   L7099  T=10 F=0  T=140 F=0  if ((ctxt->encoding == NULL) &&
  d=3   L7100  T=10 F=0  T=140 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=3   L7109  T=0 F=10  T=0 F=140  if (enc != XML_CHAR_ENCODING_NONE)
  d=3   L7123  T=0 F=10  T=0 F=140  if (ctxt->myDoc == NULL) {
  d=3   L7131  T=0 F=10  T=0 F=140  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=3   L7131  T=10 F=0  T=140 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=3   L7137  T=23 F=0  T=530 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=3   L7137  T=23 F=0  T=455 F=75  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=3   L7139  T=13 F=0  T=390 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=3   L7139  T=13 F=10  T=390 F=65  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=3   L7139  T=0 F=13  T=0 F=390  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=3   L7141  T=13 F=10  T=390 F=65  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=3   L7141  T=13 F=0  T=390 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=3   L7151  T=0 F=0  T=0 F=75  if (RAW != 0) {
--- d=2  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=2   L6952  T=13 F=0  T=390 F=0  if (CUR == '<') {
  d=2   L6953  T=13 F=0  T=390 F=0  if (NXT(1) == '!') {
  d=2   L6955  T=13 F=0  T=277 F=113  case 'E':
  d=2   L6956  T=13 F=0  T=277 F=0  if (NXT(3) == 'L')
  d=2   L6963  T=0 F=13  T=110 F=280  case 'A':
  d=2   L6966  T=0 F=13  T=0 F=390  case 'N':
  d=2   L6969  T=0 F=13  T=3 F=387  case '-':
  d=2   L6972  T=0 F=13  T=0 F=390  default:
  d=2   L6986  T=0 F=13  T=0 F=390  if (ctxt->instate == XML_PARSER_EOF)
--- d=1  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788) ---
  d=1   L6698  T=0 F=13  T=0 F=277  if ((CUR != '<') || (NXT(1) != '!'))
  d=1   L6698  T=0 F=13  T=0 F=277  if ((CUR != '<') || (NXT(1) != '!'))
  d=1   L6707  T=0 F=13  T=0 F=277  if (SKIP_BLANKS == 0) {
  d=1   L6713  T=0 F=13  T=6 F=271  if (name == NULL) {
  d=1   L6718  T=0 F=13  T=6 F=265  if (SKIP_BLANKS == 0) {
  d=1   L6728  T=3 F=7  T=0 F=0  } else if ((RAW == 'A') && (NXT(1) == 'N') &&  <-- BLOCKER
  d=1   L6728  T=10 F=3  T=0 F=271  } else if ((RAW == 'A') && (NXT(1) == 'N') &&  <-- BLOCKER
  d=1   L6729  T=0 F=3  T=0 F=0  (NXT(2) == 'Y')) {
  d=1   L6735  T=3 F=10  T=271 F=0  } else if (RAW == '(') {
  d=1   L6741  T=0 F=10  T=0 F=0  if ((RAW == '%') && (ctxt->external == 0) &&
  d=1   L6754  T=0 F=3  T=27 F=244  if (RAW != '>') {
  d=1   L6756  T=0 F=0  T=0 F=27  if (content != NULL) {
  d=1   L6760  T=0 F=3  T=0 F=244  if (inputid != ctxt->input->id) {
  d=1   L6767  T=3 F=0  T=244 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L6767  T=0 F=3  T=211 F=33  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L6768  T=0 F=0  T=211 F=0  (ctxt->sax->elementDecl != NULL)) {
  d=1   L6769  T=0 F=0  T=211 F=0  if (content != NULL)
  d=1   L6773  T=0 F=0  T=211 F=0  if ((content != NULL) && (content->parent == NULL)) {
  d=1   L6773  T=0 F=0  T=0 F=211  if ((content != NULL) && (content->parent == NULL)) {
  d=1   L6782  T=0 F=3  T=27 F=6  } else if (content != NULL) {

[off-chain: 927 additional divergent branches across 89 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=45e4b8e63840b1e3, size=368 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1464s, mutation_op=BytesSetMutator,ByteFlipMutator,QwordAddMutator,BytesDeleteMutator,ByteNegMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 0a   .0"?>.<!DOCTYPE.
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=1b02d5b399817610, size=432 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=6969s, mutation_op=ByteAddMutator,CrossoverInsertMutator,BytesInsertCopyMutator):
  0000: 3d 22 68 74 74 70 3a 2f 2f 66 61 6b 65 75 72 6c   ="http://fakeurl
  0010: 44 20 27 5f 2e 6e 65 74 22 5c 37 64 74 64 73 2f   D '_.net"\7dtds/
  0020: 2e 20 20 23 46 49 58 45 44 20 27 5f 69 6d 70 6c   .  #FIXED '_impl
  0030: 65 27 0a 20 20 2f 20 20 20 43 43 43 43 43 43 43   e'.  /   CCCCCCC
Seed 3 (id=c6deeb09ae369de2, size=494 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=7448s, mutation_op=BytesRandSetMutator,CrossoverInsertMutator,ByteAddMutator):
  0000: 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 33 2e 6f   'http://www.w3.o
  0010: 72 67 2f 31 39 39 39 2f 78 6c 69 6e 6b 27 0a 2a   rg/1999/xlink'.*
  0020: 20 20 20 20 20 20 20 20 20 20 20 78 6c 69 6e 6b              xlink
  0030: 3a 74 79 70 65 20 20 21 44 4f 0a 54 59 50 45 20   :type  !DO.TYPE 
Seed 4 (id=f753357b3c043f96, size=703 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=45870s, mutation_op=ByteRandMutator,DwordAddMutator,ByteNegMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 68 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?hml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00f7af173db700b0, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=0s, mutation_op=BytesExpandMutator,DwordAddMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=00fd268513ef89d3, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=1s, mutation_op=BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=239c7bb15678b33c, size=379 bytes, fuzzer=cmplog, trial=4, discovered_at=1s, mutation_op=TokenInsert,CrossoverReplaceMutator,WordInterestingMutator,TokenReplace,QwordAddMutator,ByteAddMutator,BytesSwapMutator):
  0000: 13 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30   .ml version="1.0
  0010: 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 41 53   "?>.<!DOCTYPE AS
  0020: 43 49 5e 2f 77 77 77 2e 77 33 2e 6f 72 67 2f 31   CI^/www.w3.org/1
  0030: 39 39 39 2f 78 6c 69 6e 6b 27 0a 20 20 20 20 20   999/xlink'.     
Seed 4 (id=0023d07679e4627f, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=2s, mutation_op=ByteInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=076df8c667aefde7, size=373 bytes, fuzzer=cmplog, trial=2, discovered_at=3s, mutation_op=TokenInsert):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x2 3d(=)x1 27(')x1             06(.)x32 31(1)x2 3c(<)x2 13(.)x1 +10u  PARTIAL
   0x0001  00(.)x2 22(")x1 68(h)x1             00(.)x30 32(2)x3 25(%)x2 6d(m)x1 +11u  PARTIAL
   0x0002  00(.)x2 68(h)x1 74(t)x1             00(.)x29 ff(.)x3 37(7)x2 6c(l)x1 +12u  PARTIAL
   0x0003  00(.)x2 74(t)x2                     00(.)x35 37(7)x3 20( )x1 64(d)x1 +7u  PARTIAL
   0x0004  31(1)x2 74(t)x1 70(p)x1             31(1)x35 37(7)x3 76(v)x1 64(d)x1 +7u  PARTIAL
   0x0005  32(2)x2 70(p)x1 3a(:)x1             32(2)x37 65(e)x1 64(d)x1 6c(l)x1 +7u  PARTIAL
   0x0006  37(7)x2 3a(:)x1 2f(/)x1             37(7)x36 2e(.)x2 72(r)x1 64(d)x1 +7u  PARTIAL
   0x0007  37(7)x2 2f(/)x2                     37(7)x36 78(x)x2 73(s)x1 64(d)x1 +7u  PARTIAL
   0x0008  37(7)x2 2f(/)x1 77(w)x1             37(7)x36 6d(m)x2 69(i)x1 55(U)x1 +7u  PARTIAL
   0x0009  32(2)x2 66(f)x1 77(w)x1             32(2)x36 6c(l)x2 6f(o)x1 54(T)x1 +7u  PARTIAL
   0x000a  2e(.)x2 61(a)x1 77(w)x1             2e(.)x36 5c(\)x2 6e(n)x1 46(F)x1 +7u  PARTIAL
   0x000b  78(x)x2 6b(k)x1 2e(.)x1             78(x)x36 0a(.)x2 3d(=)x1 2d(-)x1 +7u  PARTIAL
   0x000c  6d(m)x2 65(e)x1 77(w)x1             6d(m)x36 3c(<)x2 22(")x1 31(1)x1 +7u  PARTIAL
   0x000d  6c(l)x2 75(u)x1 33(3)x1             6c(l)x35 00(.)x3 3f(?)x2 31(1)x1 +6u  PARTIAL
   0x000e  5c(\)x2 72(r)x1 2e(.)x1             5c(\)x36 78(x)x2 2e(.)x1 37(7)x1 +7u  PARTIAL
   0x000f  0a(.)x2 6c(l)x1 6f(o)x1             0a(.)x36 32(2)x2 6d(m)x2 30(0)x1 +6u  PARTIAL
   0x0010  3c(<)x2 44(D)x1 72(r)x1             3c(<)x36 2e(.)x2 6c(l)x2 22(")x1 +6u  PARTIAL
   0x0011  3f(?)x2 20( )x1 67(g)x1             3f(?)x37 20( )x2 78(x)x1 73(s)x1 +6u  PARTIAL
   0x0012  78(x)x1 27(')x1 2f(/)x1 68(h)x1     78(x)x36 76(v)x2 3e(>)x1 6d(m)x1 +7u  PARTIAL
   0x0013  6d(m)x2 5f(_)x1 31(1)x1             6d(m)x36 65(e)x2 0a(.)x1 6c(l)x1 +7u  PARTIAL
   0x0014  6c(l)x2 2e(.)x1 39(9)x1             6c(l)x36 72(r)x2 65(e)x2 3c(<)x1 +6u  PARTIAL
   0x0015  20( )x2 6e(n)x1 39(9)x1             20( )x35 0a(.)x2 73(s)x2 21(!)x1 +7u  PARTIAL
   0x0016  76(v)x2 65(e)x1 39(9)x1             76(v)x36 69(i)x2 44(D)x1 3c(<)x1 +7u  PARTIAL
   0x0017  65(e)x2 74(t)x1 2f(/)x1             65(e)x36 6f(o)x2 20( )x2 4f(O)x1 +6u  PARTIAL
   0x0018  72(r)x2 22(")x1 78(x)x1             72(r)x36 78(x)x2 6e(n)x2 43(C)x1 +6u  PARTIAL
   0x0019  73(s)x2 5c(\)x1 6c(l)x1             73(s)x36 6d(m)x2 3d(=)x2 65(e)x2 +5u  PARTIAL
   0x001a  69(i)x3 37(7)x1                     69(i)x36 22(")x3 6c(l)x2 59(Y)x1 +5u  PARTIAL
   0x001b  6f(o)x2 64(d)x1 6e(n)x1             6f(o)x36 3f(?)x2 31(1)x2 50(P)x1 +6u  PARTIAL
   0x001c  6e(n)x2 74(t)x1 6b(k)x1             6e(n)x36 2e(.)x2 45(E)x1 76(v)x1 +7u  PARTIAL
   0x001d  3d(=)x2 64(d)x1 27(')x1             3d(=)x36 30(0)x2 2f(/)x2 20( )x1 +6u  PARTIAL
   0x001e  22(")x2 73(s)x1 0a(.)x1             22(")x38 41(A)x1 72(r)x1 3c(<)x1 +6u  PARTIAL
   0x001f  31(1)x2 2f(/)x1 2a(*)x1             31(1)x36 3f(?)x2 53(S)x1 73(s)x1 +7u  PARTIAL
   0x0020  2e(.)x3 20( )x1                     2e(.)x36 3e(>)x2 43(C)x1 69(i)x1 +7u  PARTIAL
   0x0021  30(0)x2 20( )x2                     30(0)x35 31(1)x2 0a(.)x2 49(I)x1 +7u  PARTIAL
   0x0022  22(")x2 20( )x2                     22(")x36 3c(<)x2 5e(^)x1 6e(n)x1 +7u  PARTIAL
   0x0023  3f(?)x2 23(#)x1 20( )x1             3f(?)x36 21(!)x2 2f(/)x1 3d(=)x1 +7u  PARTIAL
   0x0024  3e(>)x2 46(F)x1 20( )x1             3e(>)x37 22(")x2 44(D)x2 77(w)x1 +5u  PARTIAL
   0x0025  0a(.)x2 49(I)x1 20( )x1             0a(.)x35 4f(O)x2 77(w)x1 31(1)x1 +8u  PARTIAL
   0x0026  3c(<)x2 58(X)x1 20( )x1             3c(<)x36 2e(.)x2 43(C)x2 77(w)x1 +6u  PARTIAL
   0x0027  21(!)x2 45(E)x1 20( )x1             21(!)x36 54(T)x2 2e(.)x1 30(0)x1 +7u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6663.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6663,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6663 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6663 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6663 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).