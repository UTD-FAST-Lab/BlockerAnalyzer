==== BLOCKER ====
Target: libxml2
Branch ID: 9435
Location: /src/libxml2/parser.c:11687:8
Enclosing function: parser.c:xmlParseTryOrFinish
Source line: 			if (ctxt->nsNr - nsNr > 0)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            ?        ?          ?  REFERENCE
cmplog                           0        7          3  REFERENCE
value_profile                    0        8          2  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=8  unreached=2
  avg duration blocked: winner=7.40h  loser=17.62h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.80  dur_div=10.22h  hit_div=2
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/9435/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlParseTryOrFinish (/src/libxml2/parser.c:11404-12120) ---
[ ] 11402   */
[ ] 11403  static int
[B] 11404  xmlParseTryOrFinish(xmlParserCtxtPtr ctxt, int terminate) {
[B] 11405      int ret = 0;
[B] 11406      int avail, tlen;
[B] 11407      xmlChar cur, next;
[ ] 11408  
[B] 11409      if (ctxt->input == NULL)
[ ] 11410          return(0);
[ ] 11411  
[ ] 11412  #ifdef DEBUG_PUSH
[ ] 11413      switch (ctxt->instate) {
[ ] 11414  	case XML_PARSER_EOF:
[ ] 11415  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11416  		    "PP: try EOF\n"); break;
[ ] 11417  	case XML_PARSER_START:
[ ] 11418  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11419  		    "PP: try START\n"); break;
[ ] 11420  	case XML_PARSER_MISC:
[ ] 11421  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11422  		    "PP: try MISC\n");break;
[ ] 11423  	case XML_PARSER_COMMENT:
[ ] 11424  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11425  		    "PP: try COMMENT\n");break;
[ ] 11426  	case XML_PARSER_PROLOG:
[ ] 11427  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11428  		    "PP: try PROLOG\n");break;
[ ] 11429  	case XML_PARSER_START_TAG:
[ ] 11430  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11431  		    "PP: try START_TAG\n");break;
[ ] 11432  	case XML_PARSER_CONTENT:
[ ] 11433  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11434  		    "PP: try CONTENT\n");break;
[ ] 11435  	case XML_PARSER_CDATA_SECTION:
[ ] 11436  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11437  		    "PP: try CDATA_SECTION\n");break;
[ ] 11438  	case XML_PARSER_END_TAG:
[ ] 11439  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11440  		    "PP: try END_TAG\n");break;
[ ] 11441  	case XML_PARSER_ENTITY_DECL:
[ ] 11442  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11443  		    "PP: try ENTITY_DECL\n");break;
[ ] 11444  	case XML_PARSER_ENTITY_VALUE:
[ ] 11445  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11446  		    "PP: try ENTITY_VALUE\n");break;
[ ] 11447  	case XML_PARSER_ATTRIBUTE_VALUE:
[ ] 11448  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11449  		    "PP: try ATTRIBUTE_VALUE\n");break;
[ ] 11450  	case XML_PARSER_DTD:
[ ] 11451  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11452  		    "PP: try DTD\n");break;
[ ] 11453  	case XML_PARSER_EPILOG:
[ ] 11454  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11455  		    "PP: try EPILOG\n");break;
[ ] 11456  	case XML_PARSER_PI:
[ ] 11457  	    xmlGenericError(xmlGenericErrorContext,
[ ] 11458  		    "PP: try PI\n");break;
[ ] 11459          case XML_PARSER_IGNORE:
[ ] 11460              xmlGenericError(xmlGenericErrorContext,
[ ] 11461  		    "PP: try IGNORE\n");break;
[ ] 11462      }
[ ] 11463  #endif
[ ] 11464  
[B] 11465      if ((ctxt->input != NULL) &&
[B] 11466          (ctxt->input->cur - ctxt->input->base > 4096)) {
[ ] 11467          xmlParserInputShrink(ctxt->input);
[ ] 11468      }
[ ] 11469  
[B] 11470      while (ctxt->instate != XML_PARSER_EOF) {
[B] 11471  	if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
[L] 11472  	    return(0);
[ ] 11473  
[B] 11474  	if (ctxt->input == NULL) break;
[B] 11475  	if (ctxt->input->buf == NULL)
[ ] 11476  	    avail = ctxt->input->length -
[ ] 11477  	            (ctxt->input->cur - ctxt->input->base);
[B] 11478  	else {
[ ] 11479  	    /*
[ ] 11480  	     * If we are operating on converted input, try to flush
[ ] 11481  	     * remaining chars to avoid them stalling in the non-converted
[ ] 11482  	     * buffer. But do not do this in document start where
[ ] 11483  	     * encoding="..." may not have been read and we work on a
[ ] 11484  	     * guessed encoding.
[ ] 11485  	     */
[B] 11486  	    if ((ctxt->instate != XML_PARSER_START) &&
[B] 11487  	        (ctxt->input->buf->raw != NULL) &&
[B] 11488  		(xmlBufIsEmpty(ctxt->input->buf->raw) == 0)) {
[ ] 11489                  size_t base = xmlBufGetInputBase(ctxt->input->buf->buffer,
[ ] 11490                                                   ctxt->input);
[ ] 11491  		size_t current = ctxt->input->cur - ctxt->input->base;
[ ] 11492  
[ ] 11493  		xmlParserInputBufferPush(ctxt->input->buf, 0, "");
[ ] 11494                  xmlBufSetInputBaseCur(ctxt->input->buf->buffer, ctxt->input,
[ ] 11495                                        base, current);
[ ] 11496  	    }
[B] 11497  	    avail = xmlBufUse(ctxt->input->buf->buffer) -
[B] 11498  		    (ctxt->input->cur - ctxt->input->base);
[B] 11499  	}
[B] 11500          if (avail < 1)
[B] 11501  	    goto done;
[B] 11502          switch (ctxt->instate) {
[ ] 11503              case XML_PARSER_EOF:
[ ] 11504  	        /*
[ ] 11505  		 * Document parsing is done !
[ ] 11506  		 */
[ ] 11507  	        goto done;
[B] 11508              case XML_PARSER_START:
[B] 11509  		if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
[B] 11510  		    xmlChar start[4];
[B] 11511  		    xmlCharEncoding enc;
[ ] 11512  
[ ] 11513  		    /*
[ ] 11514  		     * Very first chars read from the document flow.
[ ] 11515  		     */
[B] 11516  		    if (avail < 4)
[ ] 11517  			goto done;
[ ] 11518  
[ ] 11519  		    /*
[ ] 11520  		     * Get the 4 first bytes and decode the charset
[ ] 11521  		     * if enc != XML_CHAR_ENCODING_NONE
[ ] 11522  		     * plug some encoding conversion routines,
[ ] 11523  		     * else xmlSwitchEncoding will set to (default)
[ ] 11524  		     * UTF8.
[ ] 11525  		     */
[B] 11526  		    start[0] = RAW;
[B] 11527  		    start[1] = NXT(1);
[B] 11528  		    start[2] = NXT(2);
[B] 11529  		    start[3] = NXT(3);
[B] 11530  		    enc = xmlDetectCharEncoding(start, 4);
[B] 11531  		    xmlSwitchEncoding(ctxt, enc);
[B] 11532  		    break;
[B] 11533  		}
[ ] 11534  
[B] 11535  		if (avail < 2)
[ ] 11536  		    goto done;
[B] 11537  		cur = ctxt->input->cur[0];
[B] 11538  		next = ctxt->input->cur[1];
[B] 11539  		if (cur == 0) {
[ ] 11540  		    if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
[ ] 11541  			ctxt->sax->setDocumentLocator(ctxt->userData,
[ ] 11542  						      &xmlDefaultSAXLocator);
[ ] 11543  		    xmlFatalErr(ctxt, XML_ERR_DOCUMENT_EMPTY, NULL);
[ ] 11544  		    xmlHaltParser(ctxt);
[ ] 11545  #ifdef DEBUG_PUSH
[ ] 11546  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11547  			    "PP: entering EOF\n");
[ ] 11548  #endif
[ ] 11549  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[ ] 11550  			ctxt->sax->endDocument(ctxt->userData);
[ ] 11551  		    goto done;
[ ] 11552  		}
[B] 11553  	        if ((cur == '<') && (next == '?')) {
[ ] 11554  		    /* PI or XML decl */
[B] 11555  		    if (avail < 5) goto done;
[B] 11556  		    if ((!terminate) &&
[B] 11557                          (!xmlParseLookupString(ctxt, 2, "?>", 2)))
[L] 11558  			goto done;
[B] 11559  		    if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
[B] 11560  			ctxt->sax->setDocumentLocator(ctxt->userData,
[B] 11561  						      &xmlDefaultSAXLocator);
[B] 11562  		    if ((ctxt->input->cur[2] == 'x') &&
[B] 11563  			(ctxt->input->cur[3] == 'm') &&
[B] 11564  			(ctxt->input->cur[4] == 'l') &&
[B] 11565  			(IS_BLANK_CH(ctxt->input->cur[5]))) {
[L] 11566  			ret += 5;
[ ] 11567  #ifdef DEBUG_PUSH
[ ] 11568  			xmlGenericError(xmlGenericErrorContext,
[ ] 11569  				"PP: Parsing XML Decl\n");
[ ] 11570  #endif
[L] 11571  			xmlParseXMLDecl(ctxt);
[L] 11572  			if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
[ ] 11573  			    /*
[ ] 11574  			     * The XML REC instructs us to stop parsing right
[ ] 11575  			     * here
[ ] 11576  			     */
[ ] 11577  			    xmlHaltParser(ctxt);
[ ] 11578  			    return(0);
[ ] 11579  			}
[L] 11580  			ctxt->standalone = ctxt->input->standalone;
[L] 11581  			if ((ctxt->encoding == NULL) &&
[L] 11582  			    (ctxt->input->encoding != NULL))
[ ] 11583  			    ctxt->encoding = xmlStrdup(ctxt->input->encoding);
[L] 11584  			if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[L] 11585  			    (!ctxt->disableSAX))
[L] 11586  			    ctxt->sax->startDocument(ctxt->userData);
[L] 11587  			ctxt->instate = XML_PARSER_MISC;
[ ] 11588  #ifdef DEBUG_PUSH
[ ] 11589  			xmlGenericError(xmlGenericErrorContext,
[ ] 11590  				"PP: entering MISC\n");
[ ] 11591  #endif
[B] 11592  		    } else {
[W] 11593  			ctxt->version = xmlCharStrdup(XML_DEFAULT_VERSION);
[W] 11594  			if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[W] 11595  			    (!ctxt->disableSAX))
[W] 11596  			    ctxt->sax->startDocument(ctxt->userData);
[W] 11597  			ctxt->instate = XML_PARSER_MISC;
[ ] 11598  #ifdef DEBUG_PUSH
[ ] 11599  			xmlGenericError(xmlGenericErrorContext,
[ ] 11600  				"PP: entering MISC\n");
[ ] 11601  #endif
[W] 11602  		    }
[B] 11603  		} else {
[L] 11604  		    if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
[L] 11605  			ctxt->sax->setDocumentLocator(ctxt->userData,
[L] 11606  						      &xmlDefaultSAXLocator);
[L] 11607  		    ctxt->version = xmlCharStrdup(XML_DEFAULT_VERSION);
[L] 11608  		    if (ctxt->version == NULL) {
[ ] 11609  		        xmlErrMemory(ctxt, NULL);
[ ] 11610  			break;
[ ] 11611  		    }
[L] 11612  		    if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[L] 11613  		        (!ctxt->disableSAX))
[L] 11614  			ctxt->sax->startDocument(ctxt->userData);
[L] 11615  		    ctxt->instate = XML_PARSER_MISC;
[ ] 11616  #ifdef DEBUG_PUSH
[ ] 11617  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11618  			    "PP: entering MISC\n");
[ ] 11619  #endif
[L] 11620  		}
[B] 11621  		break;
[B] 11622              case XML_PARSER_START_TAG: {
[B] 11623  	        const xmlChar *name;
[B] 11624  		const xmlChar *prefix = NULL;
[B] 11625  		const xmlChar *URI = NULL;
[B] 11626                  int line = ctxt->input->line;
[B] 11627  		int nsNr = ctxt->nsNr;
[ ] 11628  
[B] 11629  		if ((avail < 2) && (ctxt->inputNr == 1))
[ ] 11630  		    goto done;
[B] 11631  		cur = ctxt->input->cur[0];
[B] 11632  	        if (cur != '<') {
[ ] 11633  		    xmlFatalErr(ctxt, XML_ERR_DOCUMENT_EMPTY, NULL);
[ ] 11634  		    xmlHaltParser(ctxt);
[ ] 11635  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[ ] 11636  			ctxt->sax->endDocument(ctxt->userData);
[ ] 11637  		    goto done;
[ ] 11638  		}
[B] 11639  		if ((!terminate) && (!xmlParseLookupGt(ctxt)))
[B] 11640                      goto done;
[B] 11641  		if (ctxt->spaceNr == 0)
[L] 11642  		    spacePush(ctxt, -1);
[B] 11643  		else if (*ctxt->space == -2)
[L] 11644  		    spacePush(ctxt, -1);
[B] 11645  		else
[B] 11646  		    spacePush(ctxt, *ctxt->space);
[B] 11647  #ifdef LIBXML_SAX1_ENABLED
[B] 11648  		if (ctxt->sax2)
[B] 11649  #endif /* LIBXML_SAX1_ENABLED */
[B] 11650  		    name = xmlParseStartTag2(ctxt, &prefix, &URI, &tlen);
[ ] 11651  #ifdef LIBXML_SAX1_ENABLED
[ ] 11652  		else
[ ] 11653  		    name = xmlParseStartTag(ctxt);
[B] 11654  #endif /* LIBXML_SAX1_ENABLED */
[B] 11655  		if (ctxt->instate == XML_PARSER_EOF)
[ ] 11656  		    goto done;
[B] 11657  		if (name == NULL) {
[L] 11658  		    spacePop(ctxt);
[L] 11659  		    xmlHaltParser(ctxt);
[L] 11660  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[L] 11661  			ctxt->sax->endDocument(ctxt->userData);
[L] 11662  		    goto done;
[L] 11663  		}
[B] 11664  #ifdef LIBXML_VALID_ENABLED
[ ] 11665  		/*
[ ] 11666  		 * [ VC: Root Element Type ]
[ ] 11667  		 * The Name in the document type declaration must match
[ ] 11668  		 * the element type of the root element.
[ ] 11669  		 */
[B] 11670  		if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
[B] 11671  		    ctxt->node && (ctxt->node == ctxt->myDoc->children))
[ ] 11672  		    ctxt->valid &= xmlValidateRoot(&ctxt->vctxt, ctxt->myDoc);
[B] 11673  #endif /* LIBXML_VALID_ENABLED */
[ ] 11674  
[ ] 11675  		/*
[ ] 11676  		 * Check for an Empty Element.
[ ] 11677  		 */
[B] 11678  		if ((RAW == '/') && (NXT(1) == '>')) {
[B] 11679  		    SKIP(2);
[ ] 11680  
[B] 11681  		    if (ctxt->sax2) {
[B] 11682  			if ((ctxt->sax != NULL) &&
[B] 11683  			    (ctxt->sax->endElementNs != NULL) &&
[B] 11684  			    (!ctxt->disableSAX))
[B] 11685  			    ctxt->sax->endElementNs(ctxt->userData, name,
[B] 11686  			                            prefix, URI);
[B] 11687  			if (ctxt->nsNr - nsNr > 0) <-- BLOCKER
[W] 11688  			    nsPop(ctxt, ctxt->nsNr - nsNr);
[B] 11689  #ifdef LIBXML_SAX1_ENABLED
[B] 11690  		    } else {
[ ] 11691  			if ((ctxt->sax != NULL) &&
[ ] 11692  			    (ctxt->sax->endElement != NULL) &&
[ ] 11693  			    (!ctxt->disableSAX))
[ ] 11694  			    ctxt->sax->endElement(ctxt->userData, name);
[ ] 11695  #endif /* LIBXML_SAX1_ENABLED */
[ ] 11696  		    }
[B] 11697  		    if (ctxt->instate == XML_PARSER_EOF)
[ ] 11698  			goto done;
[B] 11699  		    spacePop(ctxt);
[B] 11700  		    if (ctxt->nameNr == 0) {
[L] 11701  			ctxt->instate = XML_PARSER_EPILOG;
[B] 11702  		    } else {
[B] 11703  			ctxt->instate = XML_PARSER_CONTENT;
[B] 11704  		    }
[B] 11705  		    break;
[B] 11706  		}
[B] 11707  		if (RAW == '>') {
[B] 11708  		    NEXT;
[B] 11709  		} else {
[B] 11710  		    xmlFatalErrMsgStr(ctxt, XML_ERR_GT_REQUIRED,
[B] 11711  					 "Couldn't find end of Start Tag %s\n",
[B] 11712  					 name);
[B] 11713  		    nodePop(ctxt);
[B] 11714  		    spacePop(ctxt);
[B] 11715  		}
[B] 11716                  nameNsPush(ctxt, name, prefix, URI, line, ctxt->nsNr - nsNr);
[ ] 11717  
[B] 11718  		ctxt->instate = XML_PARSER_CONTENT;
[B] 11719                  break;
[B] 11720  	    }
[B] 11721              case XML_PARSER_CONTENT: {
[B] 11722  		if ((avail < 2) && (ctxt->inputNr == 1))
[ ] 11723  		    goto done;
[B] 11724  		cur = ctxt->input->cur[0];
[B] 11725  		next = ctxt->input->cur[1];
[ ] 11726  
[B] 11727  		if ((cur == '<') && (next == '/')) {
[L] 11728  		    ctxt->instate = XML_PARSER_END_TAG;
[L] 11729  		    break;
[B] 11730  	        } else if ((cur == '<') && (next == '?')) {
[ ] 11731  		    if ((!terminate) &&
[ ] 11732  		        (!xmlParseLookupString(ctxt, 2, "?>", 2)))
[ ] 11733  			goto done;
[ ] 11734  		    xmlParsePI(ctxt);
[ ] 11735  		    ctxt->instate = XML_PARSER_CONTENT;
[B] 11736  		} else if ((cur == '<') && (next != '!')) {
[B] 11737  		    ctxt->instate = XML_PARSER_START_TAG;
[B] 11738  		    break;
[B] 11739  		} else if ((cur == '<') && (next == '!') &&
[B] 11740  		           (ctxt->input->cur[2] == '-') &&
[B] 11741  			   (ctxt->input->cur[3] == '-')) {
[ ] 11742  		    if ((!terminate) &&
[ ] 11743  		        (!xmlParseLookupString(ctxt, 4, "-->", 3)))
[ ] 11744  			goto done;
[ ] 11745  		    xmlParseComment(ctxt);
[ ] 11746  		    ctxt->instate = XML_PARSER_CONTENT;
[B] 11747  		} else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
[B] 11748  		    (ctxt->input->cur[2] == '[') &&
[B] 11749  		    (ctxt->input->cur[3] == 'C') &&
[B] 11750  		    (ctxt->input->cur[4] == 'D') &&
[B] 11751  		    (ctxt->input->cur[5] == 'A') &&
[B] 11752  		    (ctxt->input->cur[6] == 'T') &&
[B] 11753  		    (ctxt->input->cur[7] == 'A') &&
[B] 11754  		    (ctxt->input->cur[8] == '[')) {
[ ] 11755  		    SKIP(9);
[ ] 11756  		    ctxt->instate = XML_PARSER_CDATA_SECTION;
[ ] 11757  		    break;
[B] 11758  		} else if ((cur == '<') && (next == '!') &&
[B] 11759  		           (avail < 9)) {
[ ] 11760  		    goto done;
[B] 11761  		} else if (cur == '<') {
[L] 11762  		    xmlFatalErr(ctxt, XML_ERR_INTERNAL_ERROR,
[L] 11763  		                "detected an error in element content\n");
[L] 11764                      SKIP(1);
[B] 11765  		} else if (cur == '&') {
[W] 11766  		    if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
[W] 11767  			goto done;
[W] 11768  		    xmlParseReference(ctxt);
[B] 11769  		} else {
[ ] 11770  		    /* TODO Avoid the extra copy, handle directly !!! */
[ ] 11771  		    /*
[ ] 11772  		     * Goal of the following test is:
[ ] 11773  		     *  - minimize calls to the SAX 'character' callback
[ ] 11774  		     *    when they are mergeable
[ ] 11775  		     *  - handle an problem for isBlank when we only parse
[ ] 11776  		     *    a sequence of blank chars and the next one is
[ ] 11777  		     *    not available to check against '<' presence.
[ ] 11778  		     *  - tries to homogenize the differences in SAX
[ ] 11779  		     *    callbacks between the push and pull versions
[ ] 11780  		     *    of the parser.
[ ] 11781  		     */
[B] 11782  		    if ((ctxt->inputNr == 1) &&
[B] 11783  		        (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
[B] 11784  			if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
[B] 11785  			    goto done;
[B] 11786                      }
[B] 11787                      ctxt->checkIndex = 0;
[B] 11788  		    xmlParseCharData(ctxt, 0);
[B] 11789  		}
[B] 11790  		break;
[B] 11791  	    }
[B] 11792              case XML_PARSER_END_TAG:
[L] 11793  		if (avail < 2)
[ ] 11794  		    goto done;
[L] 11795  		if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
[ ] 11796  		    goto done;
[L] 11797  		if (ctxt->sax2) {
[L] 11798  	            xmlParseEndTag2(ctxt, &ctxt->pushTab[ctxt->nameNr - 1]);
[L] 11799  		    nameNsPop(ctxt);
[L] 11800  		}
[ ] 11801  #ifdef LIBXML_SAX1_ENABLED
[ ] 11802  		  else
[ ] 11803  		    xmlParseEndTag1(ctxt, 0);
[L] 11804  #endif /* LIBXML_SAX1_ENABLED */
[L] 11805  		if (ctxt->instate == XML_PARSER_EOF) {
[ ] 11806  		    /* Nothing */
[L] 11807  		} else if (ctxt->nameNr == 0) {
[L] 11808  		    ctxt->instate = XML_PARSER_EPILOG;
[L] 11809  		} else {
[L] 11810  		    ctxt->instate = XML_PARSER_CONTENT;
[L] 11811  		}
[L] 11812  		break;
[ ] 11813              case XML_PARSER_CDATA_SECTION: {
[ ] 11814  	        /*
[ ] 11815  		 * The Push mode need to have the SAX callback for
[ ] 11816  		 * cdataBlock merge back contiguous callbacks.
[ ] 11817  		 */
[ ] 11818  		const xmlChar *term;
[ ] 11819  
[ ] 11820                  if (terminate) {
[ ] 11821                      /*
[ ] 11822                       * Don't call xmlParseLookupString. If 'terminate'
[ ] 11823                       * is set, checkIndex is invalid.
[ ] 11824                       */
[ ] 11825                      term = BAD_CAST strstr((const char *) ctxt->input->cur,
[ ] 11826                                             "]]>");
[ ] 11827                  } else {
[ ] 11828  		    term = xmlParseLookupString(ctxt, 0, "]]>", 3);
[ ] 11829                  }
[ ] 11830  
[ ] 11831  		if (term == NULL) {
[ ] 11832  		    int tmp, size;
[ ] 11833  
[ ] 11834                      if (terminate) {
[ ] 11835                          /* Unfinished CDATA section */
[ ] 11836                          size = ctxt->input->end - ctxt->input->cur;
[ ] 11837                      } else {
[ ] 11838                          if (avail < XML_PARSER_BIG_BUFFER_SIZE + 2)
[ ] 11839                              goto done;
[ ] 11840                          ctxt->checkIndex = 0;
[ ] 11841                          /* XXX: Why don't we pass the full buffer? */
[ ] 11842                          size = XML_PARSER_BIG_BUFFER_SIZE;
[ ] 11843                      }
[ ] 11844                      tmp = xmlCheckCdataPush(ctxt->input->cur, size, 0);
[ ] 11845                      if (tmp <= 0) {
[ ] 11846                          tmp = -tmp;
[ ] 11847                          ctxt->input->cur += tmp;
[ ] 11848                          goto encoding_error;
[ ] 11849                      }
[ ] 11850                      if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) {
[ ] 11851                          if (ctxt->sax->cdataBlock != NULL)
[ ] 11852                              ctxt->sax->cdataBlock(ctxt->userData,
[ ] 11853                                                    ctxt->input->cur, tmp);
[ ] 11854                          else if (ctxt->sax->characters != NULL)
[ ] 11855                              ctxt->sax->characters(ctxt->userData,
[ ] 11856                                                    ctxt->input->cur, tmp);
[ ] 11857                      }
[ ] 11858                      if (ctxt->instate == XML_PARSER_EOF)
[ ] 11859                          goto done;
[ ] 11860                      SKIPL(tmp);
[ ] 11861  		} else {
[ ] 11862                      int base = term - CUR_PTR;
[ ] 11863  		    int tmp;
[ ] 11864  
[ ] 11865  		    tmp = xmlCheckCdataPush(ctxt->input->cur, base, 1);
[ ] 11866  		    if ((tmp < 0) || (tmp != base)) {
[ ] 11867  			tmp = -tmp;
[ ] 11868  			ctxt->input->cur += tmp;
[ ] 11869  			goto encoding_error;
[ ] 11870  		    }
[ ] 11871  		    if ((ctxt->sax != NULL) && (base == 0) &&
[ ] 11872  		        (ctxt->sax->cdataBlock != NULL) &&
[ ] 11873  		        (!ctxt->disableSAX)) {
[ ] 11874  			/*
[ ] 11875  			 * Special case to provide identical behaviour
[ ] 11876  			 * between pull and push parsers on enpty CDATA
[ ] 11877  			 * sections
[ ] 11878  			 */
[ ] 11879  			 if ((ctxt->input->cur - ctxt->input->base >= 9) &&
[ ] 11880  			     (!strncmp((const char *)&ctxt->input->cur[-9],
[ ] 11881  			               "<![CDATA[", 9)))
[ ] 11882  			     ctxt->sax->cdataBlock(ctxt->userData,
[ ] 11883  			                           BAD_CAST "", 0);
[ ] 11884  		    } else if ((ctxt->sax != NULL) && (base > 0) &&
[ ] 11885  			(!ctxt->disableSAX)) {
[ ] 11886  			if (ctxt->sax->cdataBlock != NULL)
[ ] 11887  			    ctxt->sax->cdataBlock(ctxt->userData,
[ ] 11888  						  ctxt->input->cur, base);
[ ] 11889  			else if (ctxt->sax->characters != NULL)
[ ] 11890  			    ctxt->sax->characters(ctxt->userData,
[ ] 11891  						  ctxt->input->cur, base);
[ ] 11892  		    }
[ ] 11893  		    if (ctxt->instate == XML_PARSER_EOF)
[ ] 11894  			goto done;
[ ] 11895  		    SKIPL(base + 3);
[ ] 11896  		    ctxt->instate = XML_PARSER_CONTENT;
[ ] 11897  #ifdef DEBUG_PUSH
[ ] 11898  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11899  			    "PP: entering CONTENT\n");
[ ] 11900  #endif
[ ] 11901  		}
[ ] 11902  		break;
[ ] 11903  	    }
[B] 11904              case XML_PARSER_MISC:
[B] 11905              case XML_PARSER_PROLOG:
[B] 11906              case XML_PARSER_EPILOG:
[B] 11907  		SKIP_BLANKS;
[B] 11908  		if (ctxt->input->buf == NULL)
[ ] 11909  		    avail = ctxt->input->length -
[ ] 11910  		            (ctxt->input->cur - ctxt->input->base);
[B] 11911  		else
[B] 11912  		    avail = xmlBufUse(ctxt->input->buf->buffer) -
[B] 11913  		            (ctxt->input->cur - ctxt->input->base);
[B] 11914  		if (avail < 2)
[ ] 11915  		    goto done;
[B] 11916  		cur = ctxt->input->cur[0];
[B] 11917  		next = ctxt->input->cur[1];
[B] 11918  	        if ((cur == '<') && (next == '?')) {
[B] 11919  		    if ((!terminate) &&
[B] 11920                          (!xmlParseLookupString(ctxt, 2, "?>", 2)))
[L] 11921  			goto done;
[ ] 11922  #ifdef DEBUG_PUSH
[ ] 11923  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11924  			    "PP: Parsing PI\n");
[ ] 11925  #endif
[B] 11926  		    xmlParsePI(ctxt);
[B] 11927  		    if (ctxt->instate == XML_PARSER_EOF)
[ ] 11928  			goto done;
[B] 11929  		} else if ((cur == '<') && (next == '!') &&
[B] 11930  		    (ctxt->input->cur[2] == '-') &&
[B] 11931  		    (ctxt->input->cur[3] == '-')) {
[ ] 11932  		    if ((!terminate) &&
[ ] 11933                          (!xmlParseLookupString(ctxt, 4, "-->", 3)))
[ ] 11934  			goto done;
[ ] 11935  #ifdef DEBUG_PUSH
[ ] 11936  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11937  			    "PP: Parsing Comment\n");
[ ] 11938  #endif
[ ] 11939  		    xmlParseComment(ctxt);
[ ] 11940  		    if (ctxt->instate == XML_PARSER_EOF)
[ ] 11941  			goto done;
[B] 11942  		} else if ((ctxt->instate == XML_PARSER_MISC) &&
[B] 11943                      (cur == '<') && (next == '!') &&
[B] 11944  		    (ctxt->input->cur[2] == 'D') &&
[B] 11945  		    (ctxt->input->cur[3] == 'O') &&
[B] 11946  		    (ctxt->input->cur[4] == 'C') &&
[B] 11947  		    (ctxt->input->cur[5] == 'T') &&
[B] 11948  		    (ctxt->input->cur[6] == 'Y') &&
[B] 11949  		    (ctxt->input->cur[7] == 'P') &&
[B] 11950  		    (ctxt->input->cur[8] == 'E')) {
[B] 11951  		    if ((!terminate) && (!xmlParseLookupGt(ctxt)))
[ ] 11952                          goto done;
[ ] 11953  #ifdef DEBUG_PUSH
[ ] 11954  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11955  			    "PP: Parsing internal subset\n");
[ ] 11956  #endif
[B] 11957  		    ctxt->inSubset = 1;
[B] 11958  		    xmlParseDocTypeDecl(ctxt);
[B] 11959  		    if (ctxt->instate == XML_PARSER_EOF)
[ ] 11960  			goto done;
[B] 11961  		    if (RAW == '[') {
[ ] 11962  			ctxt->instate = XML_PARSER_DTD;
[ ] 11963  #ifdef DEBUG_PUSH
[ ] 11964  			xmlGenericError(xmlGenericErrorContext,
[ ] 11965  				"PP: entering DTD\n");
[ ] 11966  #endif
[B] 11967  		    } else {
[ ] 11968  			/*
[ ] 11969  			 * Create and update the external subset.
[ ] 11970  			 */
[B] 11971  			ctxt->inSubset = 2;
[B] 11972  			if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
[B] 11973  			    (ctxt->sax->externalSubset != NULL))
[B] 11974  			    ctxt->sax->externalSubset(ctxt->userData,
[B] 11975  				    ctxt->intSubName, ctxt->extSubSystem,
[B] 11976  				    ctxt->extSubURI);
[B] 11977  			ctxt->inSubset = 0;
[B] 11978  			xmlCleanSpecialAttr(ctxt);
[B] 11979  			ctxt->instate = XML_PARSER_PROLOG;
[ ] 11980  #ifdef DEBUG_PUSH
[ ] 11981  			xmlGenericError(xmlGenericErrorContext,
[ ] 11982  				"PP: entering PROLOG\n");
[ ] 11983  #endif
[B] 11984  		    }
[B] 11985  		} else if ((cur == '<') && (next == '!') &&
[B] 11986  		           (avail <
[ ] 11987                              (ctxt->instate == XML_PARSER_MISC ? 9 : 4))) {
[ ] 11988  		    goto done;
[B] 11989  		} else if (ctxt->instate == XML_PARSER_EPILOG) {
[L] 11990  		    xmlFatalErr(ctxt, XML_ERR_DOCUMENT_END, NULL);
[L] 11991  		    xmlHaltParser(ctxt);
[ ] 11992  #ifdef DEBUG_PUSH
[ ] 11993  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11994  			    "PP: entering EOF\n");
[ ] 11995  #endif
[L] 11996  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[L] 11997  			ctxt->sax->endDocument(ctxt->userData);
[L] 11998  		    goto done;
[B] 11999                  } else {
[B] 12000  		    ctxt->instate = XML_PARSER_START_TAG;
[ ] 12001  #ifdef DEBUG_PUSH
[ ] 12002  		    xmlGenericError(xmlGenericErrorContext,
[ ] 12003  			    "PP: entering START_TAG\n");
[ ] 12004  #endif
[B] 12005  		}
[B] 12006  		break;
[B] 12007              case XML_PARSER_DTD: {
[ ] 12008                  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))
[ ] 12009                      goto done;
[ ] 12010  		xmlParseInternalSubset(ctxt);
[ ] 12011  		if (ctxt->instate == XML_PARSER_EOF)
[ ] 12012  		    goto done;
[ ] 12013  		ctxt->inSubset = 2;
[ ] 12014  		if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
[ ] 12015  		    (ctxt->sax->externalSubset != NULL))
[ ] 12016  		    ctxt->sax->externalSubset(ctxt->userData, ctxt->intSubName,
[ ] 12017  			    ctxt->extSubSystem, ctxt->extSubURI);
[ ] 12018  		ctxt->inSubset = 0;
[ ] 12019  		xmlCleanSpecialAttr(ctxt);
[ ] 12020  		if (ctxt->instate == XML_PARSER_EOF)
[ ] 12021  		    goto done;
[ ] 12022  		ctxt->instate = XML_PARSER_PROLOG;
[ ] 12023  #ifdef DEBUG_PUSH
[ ] 12024  		xmlGenericError(xmlGenericErrorContext,
[ ] 12025  			"PP: entering PROLOG\n");
[ ] 12026  #endif
[ ] 12027                  break;
[ ] 12028  	    }
[ ] 12029              case XML_PARSER_COMMENT:
[ ] 12030  		xmlGenericError(xmlGenericErrorContext,
[ ] 12031  			"PP: internal error, state == COMMENT\n");
[ ] 12032  		ctxt->instate = XML_PARSER_CONTENT;
[ ] 12033  #ifdef DEBUG_PUSH
[ ] 12034  		xmlGenericError(xmlGenericErrorContext,
[ ] 12035  			"PP: entering CONTENT\n");
[ ] 12036  #endif
[ ] 12037  		break;
[ ] 12038              case XML_PARSER_IGNORE:
[ ] 12039  		xmlGenericError(xmlGenericErrorContext,
[ ] 12040  			"PP: internal error, state == IGNORE");
[ ] 12041  	        ctxt->instate = XML_PARSER_DTD;
[ ] 12042  #ifdef DEBUG_PUSH
[ ] 12043  		xmlGenericError(xmlGenericErrorContext,
[ ] 12044  			"PP: entering DTD\n");
[ ] 12045  #endif
[ ] 12046  	        break;
[ ] 12047              case XML_PARSER_PI:
[ ] 12048  		xmlGenericError(xmlGenericErrorContext,
[ ] 12049  			"PP: internal error, state == PI\n");
[ ] 12050  		ctxt->instate = XML_PARSER_CONTENT;
[ ] 12051  #ifdef DEBUG_PUSH
[ ] 12052  		xmlGenericError(xmlGenericErrorContext,
[ ] 12053  			"PP: entering CONTENT\n");
[ ] 12054  #endif
[ ] 12055  		break;
[ ] 12056              case XML_PARSER_ENTITY_DECL:
[ ] 12057  		xmlGenericError(xmlGenericErrorContext,
[ ] 12058  			"PP: internal error, state == ENTITY_DECL\n");
[ ] 12059  		ctxt->instate = XML_PARSER_DTD;
[ ] 12060  #ifdef DEBUG_PUSH
[ ] 12061  		xmlGenericError(xmlGenericErrorContext,
[ ] 12062  			"PP: entering DTD\n");
[ ] 12063  #endif
[ ] 12064  		break;
[ ] 12065              case XML_PARSER_ENTITY_VALUE:
[ ] 12066  		xmlGenericError(xmlGenericErrorContext,
[ ] 12067  			"PP: internal error, state == ENTITY_VALUE\n");
[ ] 12068  		ctxt->instate = XML_PARSER_CONTENT;
[ ] 12069  #ifdef DEBUG_PUSH
[ ] 12070  		xmlGenericError(xmlGenericErrorContext,
[ ] 12071  			"PP: entering DTD\n");
[ ] 12072  #endif
[ ] 12073  		break;
[ ] 12074              case XML_PARSER_ATTRIBUTE_VALUE:
[ ] 12075  		xmlGenericError(xmlGenericErrorContext,
[ ] 12076  			"PP: internal error, state == ATTRIBUTE_VALUE\n");
[ ] 12077  		ctxt->instate = XML_PARSER_START_TAG;
[ ] 12078  #ifdef DEBUG_PUSH
[ ] 12079  		xmlGenericError(xmlGenericErrorContext,
[ ] 12080  			"PP: entering START_TAG\n");
[ ] 12081  #endif
[ ] 12082  		break;
[ ] 12083              case XML_PARSER_SYSTEM_LITERAL:
[ ] 12084  		xmlGenericError(xmlGenericErrorContext,
[ ] 12085  			"PP: internal error, state == SYSTEM_LITERAL\n");
[ ] 12086  		ctxt->instate = XML_PARSER_START_TAG;
[ ] 12087  #ifdef DEBUG_PUSH
[ ] 12088  		xmlGenericError(xmlGenericErrorContext,
[ ] 12089  			"PP: entering START_TAG\n");
[ ] 12090  #endif
[ ] 12091  		break;
[ ] 12092              case XML_PARSER_PUBLIC_LITERAL:
[ ] 12093  		xmlGenericError(xmlGenericErrorContext,
[ ] 12094  			"PP: internal error, state == PUBLIC_LITERAL\n");
[ ] 12095  		ctxt->instate = XML_PARSER_START_TAG;
[ ] 12096  #ifdef DEBUG_PUSH
[ ] 12097  		xmlGenericError(xmlGenericErrorContext,
[ ] 12098  			"PP: entering START_TAG\n");
[ ] 12099  #endif
[ ] 12100  		break;
[B] 12101  	}
[B] 12102      }
[B] 12103  done:
[ ] 12104  #ifdef DEBUG_PUSH
[ ] 12105      xmlGenericError(xmlGenericErrorContext, "PP: done %d\n", ret);
[ ] 12106  #endif
[B] 12107      return(ret);
[ ] 12108  encoding_error:
[ ] 12109      {
[ ] 12110          char buffer[150];
[ ] 12111  
[ ] 12112  	snprintf(buffer, 149, "Bytes: 0x%02X 0x%02X 0x%02X 0x%02X\n",
[ ] 12113  			ctxt->input->cur[0], ctxt->input->cur[1],
[ ] 12114  			ctxt->input->cur[2], ctxt->input->cur[3]);
[ ] 12115  	__xmlErrEncoding(ctxt, XML_ERR_INVALID_CHAR,
[ ] 12116  		     "Input is not proper UTF-8, indicate encoding !\n%s",
[ ] 12117  		     BAD_CAST buffer, NULL);
[ ] 12118      }
[ ] 12119      return(0);
[B] 12120  }

--- Caller (1 hop): xmlParseChunk (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12236) (±10 around call site) ---
[ ] 12226                      xmlHaltParser(ctxt);
[ ] 12227  		    return(XML_ERR_INVALID_ENCODING);
[ ] 12228  		}
[ ] 12229  	    }
[B] 12230  	}
[B] 12231      }
[ ] 12232  
[B] 12233      if (remain != 0) {
[ ] 12234          xmlParseTryOrFinish(ctxt, 0);
[B] 12235      } else {
[B] 12236          xmlParseTryOrFinish(ctxt, terminate); <-- CALL
[B] 12237      }
[B] 12238      if (ctxt->instate == XML_PARSER_EOF)
[L] 12239          return(ctxt->errNo);
[ ] 12240  
[B] 12241      if ((ctxt->input != NULL) &&
[B] 12242           (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_LIMIT) ||
[B] 12243           ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_LIMIT)) &&
[B] 12244          ((ctxt->options & XML_PARSE_HUGE) == 0)) {
[ ] 12245          xmlFatalErr(ctxt, XML_ERR_INTERNAL_ERROR, "Huge input lookup");
[ ] 12246          xmlHaltParser(ctxt);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 3  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     415      9200  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      58      1330  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      40      1030  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      39       656  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      27       611  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
      30       523  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
      15       381  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
      15       381  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774)
      15       376  parser.c:xmlGetNamespace  (/src/libxml2/parser.c:8856-8867)
      15       367  nodePush  (/src/libxml2/parser.c:1750-1776)
       8       322  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
      13       318  parser.c:nameNsPush  (/src/libxml2/parser.c:1820-1860)
       6       281  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
       6       270  nodePop  (/src/libxml2/parser.c:1788-1802)
      33       283  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
... (54 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=2   L12139  T=0 F=5  T=0 F=134  if (ctxt == NULL)
  d=2   L12141  T=0 F=3  T=16 F=17  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12141  T=3 F=2  T=33 F=101  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12143  T=0 F=5  T=0 F=118  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L12145  T=0 F=5  T=0 F=118  if (ctxt->input == NULL)
  d=2   L12149  T=2 F=3  T=89 F=29  if (ctxt->instate == XML_PARSER_START)
  d=2   L12151  T=4 F=0  T=75 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=2   L12151  T=4 F=1  T=75 F=43  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=2   L12151  T=4 F=0  T=75 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=2   L12152  T=0 F=4  T=0 F=75  (chunk[size - 1] == '\r')) {
  d=2   L12159  T=4 F=0  T=75 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=2   L12159  T=4 F=0  T=75 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=2   L12159  T=4 F=1  T=75 F=43  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=2   L12160  T=4 F=0  T=75 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=2   L12160  T=4 F=0  T=75 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=2   L12170  T=2 F=2  T=62 F=13  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=2   L12170  T=2 F=0  T=62 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=2   L12171  T=2 F=0  T=62 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=2   L12171  T=0 F=2  T=0 F=62  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=2   L12202  T=0 F=4  T=0 F=75  if (res < 0) {
  d=2   L12211  T=1 F=0  T=43 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=2   L12212  T=1 F=0  T=43 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=2   L12212  T=1 F=0  T=43 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=2   L12214  T=0 F=1  T=0 F=43  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=2   L12233  T=0 F=5  T=0 F=118  if (remain != 0) {
  d=2   L12238  T=0 F=5  T=20 F=98  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L12241  T=5 F=0  T=98 F=0  if ((ctxt->input != NULL) &&
  d=2   L12242  T=0 F=5  T=0 F=98  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=2   L12243  T=0 F=5  T=0 F=98  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=2   L12248  T=0 F=5  T=6 F=43  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12248  T=5 F=0  T=49 F=49  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12251  T=0 F=5  T=0 F=92  if (remain != 0) {
  d=2   L12257  T=0 F=5  T=0 F=92  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=2   L12268  T=1 F=4  T=22 F=70  if (terminate) {
  d=2   L12274  T=1 F=0  T=22 F=0  if (ctxt->input != NULL) {
  d=2   L12275  T=0 F=1  T=0 F=22  if (ctxt->input->buf == NULL)
  d=2   L12283  T=1 F=0  T=22 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=2   L12284  T=1 F=0  T=22 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=2   L12287  T=0 F=1  T=0 F=22  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=2   L12290  T=1 F=0  T=22 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=2   L12291  T=1 F=0  T=22 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L12291  T=1 F=0  T=22 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L12296  T=5 F=0  T=39 F=53  if (ctxt->wellFormed == 0)
--- d=1  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=1   L11409  T=0 F=5  T=0 F=118  if (ctxt->input == NULL)
  d=1   L11465  T=5 F=0  T=118 F=0  if ((ctxt->input != NULL) &&
  d=1   L11466  T=0 F=5  T=0 F=118  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=1   L11470  T=58 F=0  T=1190 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=1   L11471  T=0 F=52  T=6 F=943  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=1   L11471  T=52 F=6  T=949 F=249  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=1   L11474  T=0 F=58  T=0 F=1190  if (ctxt->input == NULL) break;
  d=1   L11475  T=0 F=58  T=0 F=1190  if (ctxt->input->buf == NULL)
  d=1   L11486  T=54 F=4  T=1070 F=121  if ((ctxt->instate != XML_PARSER_START) &&
  d=1   L11487  T=0 F=54  T=0 F=1070  (ctxt->input->buf->raw != NULL) &&
  d=1   L11500  T=1 F=57  T=22 F=1170  if (avail < 1)
  d=1   L11502  T=0 F=57  T=0 F=1170  switch (ctxt->instate) {
  d=1   L11503  T=0 F=57  T=0 F=1170  case XML_PARSER_EOF:
  d=1   L11508  T=4 F=53  T=121 F=1040  case XML_PARSER_START:
  d=1   L11509  T=2 F=2  T=32 F=89  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=1   L11516  T=0 F=2  T=0 F=32  if (avail < 4)
  d=1   L11535  T=0 F=2  T=0 F=89  if (avail < 2)
  d=1   L11539  T=0 F=2  T=0 F=89  if (cur == 0) {
  d=1   L11553  T=2 F=0  T=77 F=12  if ((cur == '<') && (next == '?')) {
  d=1   L11553  T=2 F=0  T=89 F=0  if ((cur == '<') && (next == '?')) {
  d=1   L11555  T=0 F=2  T=0 F=77  if (avail < 5) goto done;
  d=1   L11556  T=2 F=0  T=59 F=18  if ((!terminate) &&
  d=1   L11557  T=0 F=2  T=37 F=22  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=1   L11559  T=2 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11559  T=2 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11562  T=0 F=2  T=40 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=1   L11563  T=0 F=0  T=40 F=0  (ctxt->input->cur[3] == 'm') &&
  d=1   L11564  T=0 F=0  T=40 F=0  (ctxt->input->cur[4] == 'l') &&
  d=1   L11572  T=0 F=0  T=0 F=40  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=1   L11581  T=0 F=0  T=40 F=0  if ((ctxt->encoding == NULL) &&
  d=1   L11582  T=0 F=0  T=0 F=40  (ctxt->input->encoding != NULL))
  d=1   L11584  T=0 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11584  T=0 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11585  T=0 F=0  T=40 F=0  (!ctxt->disableSAX))
  d=1   L11594  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11594  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11595  T=2 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=1   L11604  T=0 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11604  T=0 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11608  T=0 F=0  T=0 F=12  if (ctxt->version == NULL) {
  d=1   L11612  T=0 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11612  T=0 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11613  T=0 F=0  T=12 F=0  (!ctxt->disableSAX))
  d=1   L11622  T=11 F=46  T=285 F=885  case XML_PARSER_START_TAG: {
  d=1   L11629  T=0 F=11  T=0 F=285  if ((avail < 2) && (ctxt->inputNr == 1))
  d=1   L11632  T=0 F=11  T=0 F=285  if (cur != '<') {
  d=1   L11639  T=1 F=10  T=19 F=70  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11639  T=11 F=0  T=89 F=196  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11641  T=0 F=10  T=6 F=260  if (ctxt->spaceNr == 0)
  d=1   L11643  T=0 F=10  T=46 F=214  else if (*ctxt->space == -2)
  d=1   L11648  T=10 F=0  T=266 F=0  if (ctxt->sax2)
  d=1   L11655  T=0 F=10  T=0 F=266  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L11657  T=0 F=10  T=4 F=262  if (name == NULL) {
  d=1   L11660  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L11660  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L11670  T=0 F=10  T=0 F=262  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=1   L11678  T=2 F=2  T=58 F=18  if ((RAW == '/') && (NXT(1) == '>')) {
  d=1   L11678  T=4 F=6  T=76 F=186  if ((RAW == '/') && (NXT(1) == '>')) {
  d=1   L11681  T=2 F=0  T=58 F=0  if (ctxt->sax2) {
  d=1   L11682  T=2 F=0  T=58 F=0  if ((ctxt->sax != NULL) &&
  d=1   L11683  T=2 F=0  T=58 F=0  (ctxt->sax->endElementNs != NULL) &&
  d=1   L11684  T=2 F=0  T=54 F=4  (!ctxt->disableSAX))
  d=1   L11687  T=2 F=0  T=0 F=58  if (ctxt->nsNr - nsNr > 0)  <-- BLOCKER
  d=1   L11697  T=0 F=2  T=0 F=58  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L11700  T=0 F=2  T=8 F=50  if (ctxt->nameNr == 0) {
  d=1   L11707  T=6 F=2  T=92 F=112  if (RAW == '>') {
  d=1   L11721  T=36 F=21  T=642 F=528  case XML_PARSER_CONTENT: {
  d=1   L11722  T=0 F=36  T=0 F=642  if ((avail < 2) && (ctxt->inputNr == 1))
  d=1   L11727  T=0 F=8  T=26 F=224  if ((cur == '<') && (next == '/')) {
  d=1   L11727  T=8 F=28  T=250 F=392  if ((cur == '<') && (next == '/')) {
  d=1   L11730  T=0 F=8  T=0 F=224  } else if ((cur == '<') && (next == '?')) {
  d=1   L11730  T=8 F=28  T=224 F=392  } else if ((cur == '<') && (next == '?')) {
  d=1   L11736  T=8 F=0  T=216 F=8  } else if ((cur == '<') && (next != '!')) {
  d=1   L11736  T=8 F=28  T=224 F=392  } else if ((cur == '<') && (next != '!')) {
  d=1   L11739  T=0 F=28  T=8 F=392  } else if ((cur == '<') && (next == '!') &&
  d=1   L11739  T=0 F=0  T=8 F=0  } else if ((cur == '<') && (next == '!') &&
  d=1   L11740  T=0 F=0  T=0 F=8  (ctxt->input->cur[2] == '-') &&
  d=1   L11747  T=0 F=0  T=8 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=1   L11747  T=0 F=28  T=8 F=392  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=1   L11748  T=0 F=0  T=0 F=8  (ctxt->input->cur[2] == '[') &&
  d=1   L11758  T=0 F=28  T=8 F=392  } else if ((cur == '<') && (next == '!') &&
  d=1   L11758  T=0 F=0  T=8 F=0  } else if ((cur == '<') && (next == '!') &&
  d=1   L11759  T=0 F=0  T=0 F=8  (avail < 9)) {
  d=1   L11761  T=0 F=28  T=8 F=392  } else if (cur == '<') {
  d=1   L11765  T=4 F=24  T=0 F=392  } else if (cur == '&') {
  d=1   L11766  T=2 F=2  T=0 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=1   L11766  T=2 F=0  T=0 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=1   L11782  T=24 F=0  T=392 F=0  if ((ctxt->inputNr == 1) &&
  d=1   L11783  T=24 F=0  T=382 F=10  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=1   L11784  T=1 F=12  T=10 F=64  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=1   L11784  T=13 F=11  T=74 F=308  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=1   L11792  T=0 F=57  T=26 F=1140  case XML_PARSER_END_TAG:
  d=1   L11793  T=0 F=0  T=0 F=26  if (avail < 2)
  d=1   L11795  T=0 F=0  T=0 F=16  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=1   L11795  T=0 F=0  T=16 F=10  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=1   L11797  T=0 F=0  T=26 F=0  if (ctxt->sax2) {
  d=1   L11805  T=0 F=0  T=0 F=26  if (ctxt->instate == XML_PARSER_EOF) {
  d=1   L11807  T=0 F=0  T=12 F=14  } else if (ctxt->nameNr == 0) {
  d=1   L11813  T=0 F=57  T=0 F=1170  case XML_PARSER_CDATA_SECTION: {
  d=1   L11904  T=4 F=53  T=52 F=1110  case XML_PARSER_MISC:
  d=1   L11905  T=2 F=55  T=22 F=1140  case XML_PARSER_PROLOG:
  d=1   L11906  T=0 F=57  T=22 F=1140  case XML_PARSER_EPILOG:
  d=1   L11908  T=0 F=6  T=0 F=96  if (ctxt->input->buf == NULL)
  d=1   L11914  T=0 F=6  T=0 F=96  if (avail < 2)
  d=1   L11918  T=6 F=0  T=86 F=10  if ((cur == '<') && (next == '?')) {
  d=1   L11918  T=2 F=4  T=6 F=80  if ((cur == '<') && (next == '?')) {
  d=1   L11919  T=2 F=0  T=4 F=2  if ((!terminate) &&
  d=1   L11920  T=0 F=2  T=4 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=1   L11929  T=2 F=2  T=22 F=58  } else if ((cur == '<') && (next == '!') &&
  d=1   L11929  T=4 F=0  T=80 F=10  } else if ((cur == '<') && (next == '!') &&
  d=1   L11930  T=0 F=2  T=0 F=22  (ctxt->input->cur[2] == '-') &&
  d=1   L11942  T=2 F=2  T=52 F=38  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=1   L11943  T=2 F=0  T=22 F=30  (cur == '<') && (next == '!') &&
  d=1   L11943  T=2 F=0  T=52 F=0  (cur == '<') && (next == '!') &&
  d=1   L11944  T=2 F=0  T=22 F=0  (ctxt->input->cur[2] == 'D') &&
  d=1   L11945  T=2 F=0  T=22 F=0  (ctxt->input->cur[3] == 'O') &&
  d=1   L11946  T=2 F=0  T=22 F=0  (ctxt->input->cur[4] == 'C') &&
  d=1   L11947  T=2 F=0  T=22 F=0  (ctxt->input->cur[5] == 'T') &&
  d=1   L11948  T=2 F=0  T=22 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=1   L11949  T=2 F=0  T=22 F=0  (ctxt->input->cur[7] == 'P') &&
  d=1   L11950  T=2 F=0  T=22 F=0  (ctxt->input->cur[8] == 'E')) {
  d=1   L11951  T=2 F=0  T=22 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11951  T=0 F=2  T=0 F=22  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11959  T=0 F=2  T=0 F=22  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L11961  T=0 F=2  T=0 F=22  if (RAW == '[') {
  d=1   L11972  T=2 F=0  T=22 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L11972  T=2 F=0  T=22 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L11973  T=2 F=0  T=22 F=0  (ctxt->sax->externalSubset != NULL))
  d=1   L11985  T=0 F=2  T=0 F=58  } else if ((cur == '<') && (next == '!') &&
  d=1   L11985  T=2 F=0  T=58 F=10  } else if ((cur == '<') && (next == '!') &&
  d=1   L11989  T=0 F=2  T=16 F=52  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=1   L11996  T=0 F=0  T=16 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L11996  T=0 F=0  T=16 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L12007  T=0 F=57  T=0 F=1170  case XML_PARSER_DTD: {
  d=1   L12029  T=0 F=57  T=0 F=1170  case XML_PARSER_COMMENT:
  d=1   L12038  T=0 F=57  T=0 F=1170  case XML_PARSER_IGNORE:
  d=1   L12047  T=0 F=57  T=0 F=1170  case XML_PARSER_PI:
  d=1   L12056  T=0 F=57  T=0 F=1170  case XML_PARSER_ENTITY_DECL:
  d=1   L12065  T=0 F=57  T=0 F=1170  case XML_PARSER_ENTITY_VALUE:
  d=1   L12074  T=0 F=57  T=0 F=1170  case XML_PARSER_ATTRIBUTE_VALUE:
  d=1   L12083  T=0 F=57  T=0 F=1170  case XML_PARSER_SYSTEM_LITERAL:
  d=1   L12092  T=0 F=57  T=0 F=1170  case XML_PARSER_PUBLIC_LITERAL:

[off-chain: 741 additional divergent branches across 67 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=f97f950fbd784430, size=398 bytes, fuzzer=value_profile_cmplog, trial=4, discovered_at=42018s, mutation_op=BytesSetMutator,ByteIncMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 73 69 6f 6e 00 22 31 2e 30 22 3f 3e 0a 3c 21 06   sion."1.0"?>.<!.
  0010: f7 ff ff ff 00 00 00 31 32 37 37 37 32 2e 78 6d   .......127772.xm
  0020: 6c 5c 0a 3c 3f 61 6d 6c ff 76 65 72 73 69 6f 6e   l\.<?aml.version
  0030: 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59   ="1.0"?>.<!DOCTY

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=4f47d39db586a9d9, size=296 bytes, fuzzer=value_profile, trial=4, discovered_at=1688s, mutation_op=WordAddMutator,DwordAddMutator,QwordAddMutator,QwordAddMutator,DwordAddMutator,CrossoverReplaceMutator,BytesInsertCopyMutator):
  0000: 45 4d 45 4e 54 20 62 20 28 43 44 41 54 41 29 3e   EMENT b (CDATA)>
  0010: 0a 3c 21 41 54 74 70 3a 2f 2f 77 77 00 31 32 37   .<!ATtp://ww.127
  0020: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0030: 65 72 73 69 6f 6e 3d dd 31 2e 30 22 3f 3e 0a 3c   ersion=.1.0"?>.<
Seed 2 (id=23a0fdd820d27e05, size=734 bytes, fuzzer=value_profile, trial=2, discovered_at=3407s, mutation_op=CrossoverInsertMutator,TokenReplace,WordInterestingMutator,BytesRandSetMutator):
  0000: 45 44 21 27 68 74 74 70 3a 2f 2f 77 77 40 2e 41   ED!'http://ww@.A
  0010: 20 20 30 20 20 23 46 49 58 45 44 20 27 68 74 74     0  #FIXED 'htt
  0020: 70 3a 2f 2f 77 77 77 2e 77 21 2e 6f 72 67 2f 31   p://www.w!.org/1
  0030: 39 39 39 2f 78 6c 69 6e 6b 65 66 20 20 20 50 45   999/xlinkef   PE
Seed 3 (id=7dbd63f906205f16, size=272 bytes, fuzzer=value_profile, trial=2, discovered_at=3584s, mutation_op=ByteDecMutator,BytesSwapMutator,WordAddMutator,BytesCopyMutator):
  0000: 65 29 20 20 23 46 49 58 45 32 37 37 06 31 32 37   e)  #FIXE277.127
  0010: 00 00 00 37 37 32 2e 78 6d 6c 5c 0a 3c 6c 20 76   ...772.xml\.<l v
  0020: 62 20 78 6d 6c 6e 73 3a 78 32 2e 64 74 64 62 20   b xmlns:x2.dtdb 
  0030: 78 79 69 6e 6b 2f 66 61 6b 65 75 6d 70 6c 65 29   xyink/fakeumple)
Seed 4 (id=945c8b9a7bfdc8a4, size=319 bytes, fuzzer=value_profile, trial=4, discovered_at=3723s, mutation_op=CrossoverInsertMutator,BytesInsertCopyMutator,ByteRandMutator,BytesExpandMutator,BytesInsertMutator,WordInterestingMutator,ByteIncMutator):
  0000: 23 50 43 44 41 54 41 29 3e 0a 3c 21 41 54 54 4c   #PCDATA)>.<!ATTL
  0010: 49 53 54 20 62 20 78 6d 6c 6e 73 3a 78 6c 69 6e   IST b xmlns:xlin
  0020: 6b 20 20 3e 0a 20 20 3c 62 20 78 6c 69 64 6b 3a   k  >.  <b xlidk:
  0030: 43 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20   C               
Seed 5 (id=3f2ee52d2cec061c, size=310 bytes, fuzzer=value_profile, trial=4, discovered_at=4091s, mutation_op=CrossoverReplaceMutator,BytesCopyMutator,BytesRandInsertMutator):
  0000: 45 4d 45 4e 54 20 62 20 28 43 44 41 54 41 29 3e   EMENT b (CDATA)>
  0010: 0a 3c 21 41 54 74 70 3a 2f 2f 77 77 00 31 32 37   .<!ATtp://ww.127
  0020: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 68   772.xml\.<?xml h
  0030: 68 68 68 68 68 68 68 68 68 68 68 68 68 76 65 72   hhhhhhhhhhhhhver


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  73(s)x1                             45(E)x9 69(i)x4 65(e)x3 31(1)x2 +8u  DIFFER
   0x0001  69(i)x1                             44(D)x6 69(i)x4 4d(M)x3 29())x3 +9u  PARTIAL
   0x0002  6f(o)x1                             20( )x7 45(E)x3 21(!)x3 39(9)x2 +9u  DIFFER
   0x0003  6e(n)x1                             27(')x6 20( )x4 4e(N)x3 39(9)x2 +9u  DIFFER
   0x0004  00(.)x1                             68(h)x6 23(#)x3 69(i)x3 54(T)x2 +11u  DIFFER
   0x0005  22(")x1                             74(t)x7 20( )x3 46(F)x3 69(i)x3 +8u  DIFFER
   0x0006  31(1)x1                             74(t)x6 6c(l)x4 49(I)x3 69(i)x3 +9u  DIFFER
   0x0007  2e(.)x1                             70(p)x6 58(X)x3 64(d)x3 20( )x2 +10u  DIFFER
   0x0008  30(0)x1                             3a(:)x6 74(t)x4 28(()x2 45(E)x2 +11u  DIFFER
   0x0009  22(")x1                             2f(/)x6 64(d)x3 43(C)x2 32(2)x2 +12u  DIFFER
   0x000a  3f(?)x1                             2f(/)x6 7d(})x3 44(D)x2 37(7)x2 +12u  PARTIAL
   0x000b  3e(>)x1                             77(w)x6 2e(.)x3 41(A)x2 37(7)x2 +11u  DIFFER
   0x000c  0a(.)x1                             77(w)x6 72(r)x4 54(T)x2 20( )x2 +11u  DIFFER
   0x000d  3c(<)x1                             72(r)x4 54(T)x3 77(w)x3 41(A)x2 +12u  PARTIAL
   0x000e  21(!)x1                             2e(.)x6 72(r)x4 29())x2 45(E)x2 +12u  DIFFER
   0x000f  06(.)x1                             41(A)x6 72(r)x4 3e(>)x2 37(7)x2 +10u  DIFFER
   0x0010  f7(.)x1                             20( )x8 72(r)x4 0a(.)x2 00(.)x1 +11u  DIFFER
   0x0011  ff(.)x1                             20( )x6 72(r)x4 22(")x3 3c(<)x2 +10u  DIFFER
   0x0012  ff(.)x1                             64(d)x4 72(r)x4 21(!)x3 30(0)x3 +9u  DIFFER
   0x0013  ff(.)x1                             20( )x7 72(r)x5 74(t)x3 41(A)x2 +9u  DIFFER
   0x0014  00(.)x1                             20( )x6 72(r)x4 64(d)x3 54(T)x2 +10u  DIFFER
   0x0015  00(.)x1                             23(#)x6 32(2)x3 74(t)x2 20( )x2 +10u  DIFFER
   0x0016  00(.)x1                             46(F)x6 20( )x4 70(p)x2 2e(.)x2 +10u  DIFFER
   0x0017  31(1)x1                             49(I)x6 3a(:)x3 f9(.)x3 78(x)x2 +10u  DIFFER
   0x0018  32(2)x1                             58(X)x6 2f(/)x3 0a(.)x3 f9(.)x3 +9u  DIFFER
   0x0019  37(7)x1                             45(E)x6 2f(/)x3 f9(.)x3 6c(l)x2 +11u  PARTIAL
   0x001a  37(7)x1                             44(D)x6 3e(>)x3 f9(.)x3 77(w)x2 +10u  DIFFER
   0x001b  37(7)x1                             20( )x6 0a(.)x3 f9(.)x3 77(w)x2 +11u  PARTIAL
   0x001c  32(2)x1                             27(')x6 e7(.)x4 00(.)x3 3c(<)x2 +10u  DIFFER
   0x001d  2e(.)x1                             68(h)x6 6c(l)x4 e7(.)x4 31(1)x2 +9u  DIFFER
   0x001e  78(x)x1                             74(t)x6 20( )x4 e7(.)x4 32(2)x3 +8u  DIFFER
   0x001f  6d(m)x1                             74(t)x7 e7(.)x4 37(7)x2 76(v)x2 +8u  DIFFER
   0x0020  6c(l)x1                             70(p)x6 e7(.)x4 37(7)x2 62(b)x2 +10u  DIFFER
   0x0021  5c(\)x1                             3a(:)x6 20( )x5 e7(.)x3 3f(?)x3 +7u  DIFFER
   0x0022  0a(.)x1                             2f(/)x6 32(2)x3 78(x)x3 20( )x3 +8u  PARTIAL
   0x0023  3c(<)x1                             2f(/)x7 20( )x4 6d(m)x3 32(2)x3 +8u  DIFFER
   0x0024  3f(?)x1                             77(w)x6 37(7)x4 6c(l)x3 78(x)x2 +9u  DIFFER
   0x0025  61(a)x1                             77(w)x6 37(7)x4 6d(m)x2 6e(n)x2 +10u  DIFFER
   0x0026  6d(m)x1                             77(w)x6 37(7)x3 6c(l)x2 73(s)x2 +11u  DIFFER
   0x0027  6c(l)x1                             2e(.)x7 5c(\)x3 32(2)x3 3a(:)x2 +10u  DIFFER
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_9435.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9435,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9435 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9435 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9435 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).