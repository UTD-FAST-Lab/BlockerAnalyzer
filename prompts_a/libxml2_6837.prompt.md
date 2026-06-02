==== BLOCKER ====
Target: libxml2
Branch ID: 6837
Location: /src/libxml2/parser.c:11754:7
Enclosing function: parser.c:xmlParseTryOrFinish
Source line: 		    (ctxt->input->cur[8] == '[')) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            3        7          0  REFERENCE
cmplog                           0        9          1  REFERENCE
value_profile                    9        1          0  winner (I2S vs value_profile_cmplog)
value_profile_cmplog             2        8          0  loser (I2S vs value_profile)
naive_ctx                        5        5          0  REFERENCE
naive_ngram4                     7        3          0  REFERENCE
mopt                             7        3          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > value_profile_cmplog  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.10h  loser=19.20h
  avg hitcount on branch: winner=4  loser=1
  prob_div=0.70  dur_div=13.10h  hit_div=3
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6837/{W,L}/branch_coverage_show.txt

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
[ ] 11472  	    return(0);
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
[W] 11501  	    goto done;
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
[L] 11555  		    if (avail < 5) goto done;
[L] 11556  		    if ((!terminate) &&
[L] 11557                          (!xmlParseLookupString(ctxt, 2, "?>", 2)))
[ ] 11558  			goto done;
[L] 11559  		    if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
[L] 11560  			ctxt->sax->setDocumentLocator(ctxt->userData,
[L] 11561  						      &xmlDefaultSAXLocator);
[L] 11562  		    if ((ctxt->input->cur[2] == 'x') &&
[L] 11563  			(ctxt->input->cur[3] == 'm') &&
[L] 11564  			(ctxt->input->cur[4] == 'l') &&
[L] 11565  			(IS_BLANK_CH(ctxt->input->cur[5]))) {
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
[L] 11592  		    } else {
[ ] 11593  			ctxt->version = xmlCharStrdup(XML_DEFAULT_VERSION);
[ ] 11594  			if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[ ] 11595  			    (!ctxt->disableSAX))
[ ] 11596  			    ctxt->sax->startDocument(ctxt->userData);
[ ] 11597  			ctxt->instate = XML_PARSER_MISC;
[ ] 11598  #ifdef DEBUG_PUSH
[ ] 11599  			xmlGenericError(xmlGenericErrorContext,
[ ] 11600  				"PP: entering MISC\n");
[ ] 11601  #endif
[ ] 11602  		    }
[B] 11603  		} else {
[W] 11604  		    if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
[W] 11605  			ctxt->sax->setDocumentLocator(ctxt->userData,
[W] 11606  						      &xmlDefaultSAXLocator);
[W] 11607  		    ctxt->version = xmlCharStrdup(XML_DEFAULT_VERSION);
[W] 11608  		    if (ctxt->version == NULL) {
[ ] 11609  		        xmlErrMemory(ctxt, NULL);
[ ] 11610  			break;
[ ] 11611  		    }
[W] 11612  		    if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[W] 11613  		        (!ctxt->disableSAX))
[W] 11614  			ctxt->sax->startDocument(ctxt->userData);
[W] 11615  		    ctxt->instate = XML_PARSER_MISC;
[ ] 11616  #ifdef DEBUG_PUSH
[ ] 11617  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11618  			    "PP: entering MISC\n");
[ ] 11619  #endif
[W] 11620  		}
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
[W] 11640                      goto done;
[B] 11641  		if (ctxt->spaceNr == 0)
[ ] 11642  		    spacePush(ctxt, -1);
[B] 11643  		else if (*ctxt->space == -2)
[ ] 11644  		    spacePush(ctxt, -1);
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
[ ] 11658  		    spacePop(ctxt);
[ ] 11659  		    xmlHaltParser(ctxt);
[ ] 11660  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[ ] 11661  			ctxt->sax->endDocument(ctxt->userData);
[ ] 11662  		    goto done;
[ ] 11663  		}
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
[ ] 11679  		    SKIP(2);
[ ] 11680  
[ ] 11681  		    if (ctxt->sax2) {
[ ] 11682  			if ((ctxt->sax != NULL) &&
[ ] 11683  			    (ctxt->sax->endElementNs != NULL) &&
[ ] 11684  			    (!ctxt->disableSAX))
[ ] 11685  			    ctxt->sax->endElementNs(ctxt->userData, name,
[ ] 11686  			                            prefix, URI);
[ ] 11687  			if (ctxt->nsNr - nsNr > 0)
[ ] 11688  			    nsPop(ctxt, ctxt->nsNr - nsNr);
[ ] 11689  #ifdef LIBXML_SAX1_ENABLED
[ ] 11690  		    } else {
[ ] 11691  			if ((ctxt->sax != NULL) &&
[ ] 11692  			    (ctxt->sax->endElement != NULL) &&
[ ] 11693  			    (!ctxt->disableSAX))
[ ] 11694  			    ctxt->sax->endElement(ctxt->userData, name);
[ ] 11695  #endif /* LIBXML_SAX1_ENABLED */
[ ] 11696  		    }
[ ] 11697  		    if (ctxt->instate == XML_PARSER_EOF)
[ ] 11698  			goto done;
[ ] 11699  		    spacePop(ctxt);
[ ] 11700  		    if (ctxt->nameNr == 0) {
[ ] 11701  			ctxt->instate = XML_PARSER_EPILOG;
[ ] 11702  		    } else {
[ ] 11703  			ctxt->instate = XML_PARSER_CONTENT;
[ ] 11704  		    }
[ ] 11705  		    break;
[ ] 11706  		}
[B] 11707  		if (RAW == '>') {
[L] 11708  		    NEXT;
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
[ ] 11728  		    ctxt->instate = XML_PARSER_END_TAG;
[ ] 11729  		    break;
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
[B] 11754  		    (ctxt->input->cur[8] == '[')) { <-- BLOCKER
[L] 11755  		    SKIP(9);
[L] 11756  		    ctxt->instate = XML_PARSER_CDATA_SECTION;
[L] 11757  		    break;
[B] 11758  		} else if ((cur == '<') && (next == '!') &&
[B] 11759  		           (avail < 9)) {
[ ] 11760  		    goto done;
[B] 11761  		} else if (cur == '<') {
[B] 11762  		    xmlFatalErr(ctxt, XML_ERR_INTERNAL_ERROR,
[B] 11763  		                "detected an error in element content\n");
[B] 11764                      SKIP(1);
[B] 11765  		} else if (cur == '&') {
[ ] 11766  		    if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
[ ] 11767  			goto done;
[ ] 11768  		    xmlParseReference(ctxt);
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
[L] 11785  			    goto done;
[B] 11786                      }
[B] 11787                      ctxt->checkIndex = 0;
[B] 11788  		    xmlParseCharData(ctxt, 0);
[B] 11789  		}
[B] 11790  		break;
[B] 11791  	    }
[B] 11792              case XML_PARSER_END_TAG:
[ ] 11793  		if (avail < 2)
[ ] 11794  		    goto done;
[ ] 11795  		if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
[ ] 11796  		    goto done;
[ ] 11797  		if (ctxt->sax2) {
[ ] 11798  	            xmlParseEndTag2(ctxt, &ctxt->pushTab[ctxt->nameNr - 1]);
[ ] 11799  		    nameNsPop(ctxt);
[ ] 11800  		}
[ ] 11801  #ifdef LIBXML_SAX1_ENABLED
[ ] 11802  		  else
[ ] 11803  		    xmlParseEndTag1(ctxt, 0);
[ ] 11804  #endif /* LIBXML_SAX1_ENABLED */
[ ] 11805  		if (ctxt->instate == XML_PARSER_EOF) {
[ ] 11806  		    /* Nothing */
[ ] 11807  		} else if (ctxt->nameNr == 0) {
[ ] 11808  		    ctxt->instate = XML_PARSER_EPILOG;
[ ] 11809  		} else {
[ ] 11810  		    ctxt->instate = XML_PARSER_CONTENT;
[ ] 11811  		}
[ ] 11812  		break;
[L] 11813              case XML_PARSER_CDATA_SECTION: {
[ ] 11814  	        /*
[ ] 11815  		 * The Push mode need to have the SAX callback for
[ ] 11816  		 * cdataBlock merge back contiguous callbacks.
[ ] 11817  		 */
[L] 11818  		const xmlChar *term;
[ ] 11819  
[L] 11820                  if (terminate) {
[ ] 11821                      /*
[ ] 11822                       * Don't call xmlParseLookupString. If 'terminate'
[ ] 11823                       * is set, checkIndex is invalid.
[ ] 11824                       */
[L] 11825                      term = BAD_CAST strstr((const char *) ctxt->input->cur,
[L] 11826                                             "]]>");
[L] 11827                  } else {
[L] 11828  		    term = xmlParseLookupString(ctxt, 0, "]]>", 3);
[L] 11829                  }
[ ] 11830  
[L] 11831  		if (term == NULL) {
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
[L] 11861  		} else {
[L] 11862                      int base = term - CUR_PTR;
[L] 11863  		    int tmp;
[ ] 11864  
[L] 11865  		    tmp = xmlCheckCdataPush(ctxt->input->cur, base, 1);
[L] 11866  		    if ((tmp < 0) || (tmp != base)) {
[L] 11867  			tmp = -tmp;
[L] 11868  			ctxt->input->cur += tmp;
[L] 11869  			goto encoding_error;
[L] 11870  		    }
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
[L] 11903  	    }
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
[ ] 11919  		    if ((!terminate) &&
[ ] 11920                          (!xmlParseLookupString(ctxt, 2, "?>", 2)))
[ ] 11921  			goto done;
[ ] 11922  #ifdef DEBUG_PUSH
[ ] 11923  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11924  			    "PP: Parsing PI\n");
[ ] 11925  #endif
[ ] 11926  		    xmlParsePI(ctxt);
[ ] 11927  		    if (ctxt->instate == XML_PARSER_EOF)
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
[L] 11951  		    if ((!terminate) && (!xmlParseLookupGt(ctxt)))
[ ] 11952                          goto done;
[ ] 11953  #ifdef DEBUG_PUSH
[ ] 11954  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11955  			    "PP: Parsing internal subset\n");
[ ] 11956  #endif
[L] 11957  		    ctxt->inSubset = 1;
[L] 11958  		    xmlParseDocTypeDecl(ctxt);
[L] 11959  		    if (ctxt->instate == XML_PARSER_EOF)
[ ] 11960  			goto done;
[L] 11961  		    if (RAW == '[') {
[ ] 11962  			ctxt->instate = XML_PARSER_DTD;
[ ] 11963  #ifdef DEBUG_PUSH
[ ] 11964  			xmlGenericError(xmlGenericErrorContext,
[ ] 11965  				"PP: entering DTD\n");
[ ] 11966  #endif
[L] 11967  		    } else {
[ ] 11968  			/*
[ ] 11969  			 * Create and update the external subset.
[ ] 11970  			 */
[L] 11971  			ctxt->inSubset = 2;
[L] 11972  			if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
[L] 11973  			    (ctxt->sax->externalSubset != NULL))
[L] 11974  			    ctxt->sax->externalSubset(ctxt->userData,
[L] 11975  				    ctxt->intSubName, ctxt->extSubSystem,
[L] 11976  				    ctxt->extSubURI);
[L] 11977  			ctxt->inSubset = 0;
[L] 11978  			xmlCleanSpecialAttr(ctxt);
[L] 11979  			ctxt->instate = XML_PARSER_PROLOG;
[ ] 11980  #ifdef DEBUG_PUSH
[ ] 11981  			xmlGenericError(xmlGenericErrorContext,
[ ] 11982  				"PP: entering PROLOG\n");
[ ] 11983  #endif
[L] 11984  		    }
[B] 11985  		} else if ((cur == '<') && (next == '!') &&
[B] 11986  		           (avail <
[ ] 11987                              (ctxt->instate == XML_PARSER_MISC ? 9 : 4))) {
[ ] 11988  		    goto done;
[B] 11989  		} else if (ctxt->instate == XML_PARSER_EPILOG) {
[ ] 11990  		    xmlFatalErr(ctxt, XML_ERR_DOCUMENT_END, NULL);
[ ] 11991  		    xmlHaltParser(ctxt);
[ ] 11992  #ifdef DEBUG_PUSH
[ ] 11993  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11994  			    "PP: entering EOF\n");
[ ] 11995  #endif
[ ] 11996  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[ ] 11997  			ctxt->sax->endDocument(ctxt->userData);
[ ] 11998  		    goto done;
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
[L] 12108  encoding_error:
[L] 12109      {
[L] 12110          char buffer[150];
[ ] 12111  
[L] 12112  	snprintf(buffer, 149, "Bytes: 0x%02X 0x%02X 0x%02X 0x%02X\n",
[L] 12113  			ctxt->input->cur[0], ctxt->input->cur[1],
[L] 12114  			ctxt->input->cur[2], ctxt->input->cur[3]);
[L] 12115  	__xmlErrEncoding(ctxt, XML_ERR_INVALID_CHAR,
[L] 12116  		     "Input is not proper UTF-8, indicate encoding !\n%s",
[L] 12117  		     BAD_CAST buffer, NULL);
[L] 12118      }
[L] 12119      return(0);
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
[ ] 12239          return(ctxt->errNo);
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
      34         0  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
       8        41  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
       4        12  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
       8         1  parser.c:xmlIsNameStartChar  (/src/libxml2/parser.c:3152-3180)
       8         1  parser.c:xmlParseNCNameComplex  (/src/libxml2/parser.c:3415-3471)
       2         9  parser.c:xmlParseLookupCharData  (/src/libxml2/parser.c:11170-11184)
       0         5  parser.c:xmlParseLookupString  (/src/libxml2/parser.c:11137-11161)
       2         6  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706)
       0         4  parser.c:xmlCheckCdataPush  (/src/libxml2/parser.c:11338-11392)
       0         3  parser.c:xmlCleanSpecialAttr  (/src/libxml2/parser.c:1353-1364)
       0         3  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       0         3  xmlParseSystemLiteral  (/src/libxml2/parser.c:4248-4326)
       0         3  xmlParseExternalID  (/src/libxml2/parser.c:4733-4783)
       0         3  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440)
       0         3  xmlParseVersionNum  (/src/libxml2/parser.c:10284-10329)
... (7 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=2   L12141  T=0 F=1  T=0 F=3  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12151  T=2 F=0  T=4 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=2   L12151  T=2 F=0  T=4 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=2   L12152  T=0 F=2  T=0 F=4  (chunk[size - 1] == '\r')) {
  d=2   L12159  T=2 F=0  T=4 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=2   L12159  T=2 F=0  T=4 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=2   L12160  T=2 F=0  T=4 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=2   L12160  T=2 F=0  T=4 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=2   L12170  T=2 F=0  T=2 F=2  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=2   L12202  T=0 F=2  T=0 F=4  if (res < 0) {
--- d=1  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=1   L11471  T=0 F=11  T=0 F=25  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=1   L11500  T=1 F=18  T=0 F=30  if (avail < 1)
  d=1   L11516  T=0 F=2  T=0 F=1  if (avail < 4)
  d=1   L11553  T=0 F=2  T=2 F=0  if ((cur == '<') && (next == '?')) {
  d=1   L11555  T=0 F=0  T=0 F=2  if (avail < 5) goto done;
  d=1   L11556  T=0 F=0  T=2 F=0  if ((!terminate) &&
  d=1   L11557  T=0 F=0  T=0 F=2  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=1   L11559  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11559  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11562  T=0 F=0  T=2 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=1   L11563  T=0 F=0  T=2 F=0  (ctxt->input->cur[3] == 'm') &&
  d=1   L11564  T=0 F=0  T=2 F=0  (ctxt->input->cur[4] == 'l') &&
  d=1   L11572  T=0 F=0  T=0 F=2  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=1   L11581  T=0 F=0  T=2 F=0  if ((ctxt->encoding == NULL) &&
  d=1   L11582  T=0 F=0  T=0 F=2  (ctxt->input->encoding != NULL))
  d=1   L11584  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11584  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11585  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=1   L11604  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11604  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11608  T=0 F=2  T=0 F=0  if (ctxt->version == NULL) {
  d=1   L11612  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11612  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11613  T=2 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=1   L11639  T=2 F=2  T=0 F=4  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11639  T=4 F=1  T=4 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11707  T=0 F=3  T=2 F=2  if (RAW == '>') {
  d=1   L11722  T=0 F=7  T=0 F=15  if ((avail < 2) && (ctxt->inputNr == 1))
  d=1   L11727  T=0 F=3  T=0 F=6  if ((cur == '<') && (next == '/')) {
  d=1   L11727  T=3 F=4  T=6 F=9  if ((cur == '<') && (next == '/')) {
  d=1   L11730  T=0 F=3  T=0 F=6  } else if ((cur == '<') && (next == '?')) {
  d=1   L11730  T=3 F=4  T=6 F=9  } else if ((cur == '<') && (next == '?')) {
  d=1   L11736  T=2 F=1  T=2 F=4  } else if ((cur == '<') && (next != '!')) {
  d=1   L11736  T=3 F=4  T=6 F=9  } else if ((cur == '<') && (next != '!')) {
  d=1   L11739  T=1 F=4  T=4 F=9  } else if ((cur == '<') && (next == '!') &&
  d=1   L11739  T=1 F=0  T=4 F=0  } else if ((cur == '<') && (next == '!') &&
  d=1   L11740  T=0 F=1  T=0 F=4  (ctxt->input->cur[2] == '-') &&
  d=1   L11747  T=1 F=0  T=4 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=1   L11747  T=1 F=4  T=4 F=9  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=1   L11748  T=1 F=0  T=2 F=2  (ctxt->input->cur[2] == '[') &&
  d=1   L11749  T=1 F=0  T=2 F=0  (ctxt->input->cur[3] == 'C') &&
  d=1   L11750  T=1 F=0  T=2 F=0  (ctxt->input->cur[4] == 'D') &&
  d=1   L11751  T=1 F=0  T=2 F=0  (ctxt->input->cur[5] == 'A') &&
  d=1   L11752  T=1 F=0  T=2 F=0  (ctxt->input->cur[6] == 'T') &&
  d=1   L11753  T=1 F=0  T=2 F=0  (ctxt->input->cur[7] == 'A') &&
  d=1   L11754  T=0 F=1  T=2 F=0  (ctxt->input->cur[8] == '[')) {  <-- BLOCKER
  d=1   L11758  T=1 F=4  T=2 F=9  } else if ((cur == '<') && (next == '!') &&
  d=1   L11758  T=1 F=0  T=2 F=0  } else if ((cur == '<') && (next == '!') &&
  d=1   L11759  T=0 F=1  T=0 F=2  (avail < 9)) {
  d=1   L11761  T=1 F=4  T=2 F=9  } else if (cur == '<') {
  d=1   L11765  T=0 F=4  T=0 F=9  } else if (cur == '&') {
  d=1   L11782  T=4 F=0  T=9 F=0  if ((ctxt->inputNr == 1) &&
  d=1   L11783  T=4 F=0  T=9 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=1   L11784  T=0 F=2  T=1 F=8  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=1   L11784  T=2 F=2  T=9 F=0  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=1   L11813  T=0 F=18  T=4 F=26  case XML_PARSER_CDATA_SECTION: {
  d=1   L11820  T=0 F=0  T=1 F=3  if (terminate) {
  d=1   L11831  T=0 F=0  T=0 F=4  if (term == NULL) {
  d=1   L11866  T=0 F=0  T=2 F=2  if ((tmp < 0) || (tmp != base)) {
  d=1   L11866  T=0 F=0  T=2 F=0  if ((tmp < 0) || (tmp != base)) {
  d=1   L11905  T=0 F=18  T=2 F=28  case XML_PARSER_PROLOG:
  d=1   L11908  T=0 F=2  T=0 F=4  if (ctxt->input->buf == NULL)
  d=1   L11914  T=0 F=2  T=0 F=4  if (avail < 2)
  d=1   L11918  T=2 F=0  T=4 F=0  if ((cur == '<') && (next == '?')) {
  d=1   L11918  T=0 F=2  T=0 F=4  if ((cur == '<') && (next == '?')) {
  d=1   L11929  T=0 F=2  T=2 F=2  } else if ((cur == '<') && (next == '!') &&
  d=1   L11929  T=2 F=0  T=4 F=0  } else if ((cur == '<') && (next == '!') &&
  d=1   L11930  T=0 F=0  T=0 F=2  (ctxt->input->cur[2] == '-') &&
  d=1   L11942  T=2 F=0  T=2 F=2  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=1   L11943  T=0 F=2  T=2 F=0  (cur == '<') && (next == '!') &&
  d=1   L11944  T=0 F=0  T=2 F=0  (ctxt->input->cur[2] == 'D') &&
  d=1   L11945  T=0 F=0  T=2 F=0  (ctxt->input->cur[3] == 'O') &&
  d=1   L11946  T=0 F=0  T=2 F=0  (ctxt->input->cur[4] == 'C') &&
  d=1   L11947  T=0 F=0  T=2 F=0  (ctxt->input->cur[5] == 'T') &&
  d=1   L11948  T=0 F=0  T=2 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=1   L11949  T=0 F=0  T=2 F=0  (ctxt->input->cur[7] == 'P') &&
  d=1   L11950  T=0 F=0  T=2 F=0  (ctxt->input->cur[8] == 'E')) {
  d=1   L11951  T=0 F=0  T=2 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11951  T=0 F=0  T=0 F=2  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11959  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L11961  T=0 F=0  T=0 F=2  if (RAW == '[') {
  d=1   L11972  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L11972  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L11973  T=0 F=0  T=2 F=0  (ctxt->sax->externalSubset != NULL))

[off-chain: 262 additional divergent branches across 37 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=23d10f4e6c8a17d5, size=111 bytes, fuzzer=value_profile, trial=1, discovered_at=19190s, mutation_op=QwordAddMutator,ByteIncMutator,ByteIncMutator,ByteAddMutator,DwordAddMutator):
  0000: 4d 20 62 20 28 23 3b 78 6c 69 6e 6b 21 20 43 44   M b (#;xlink! CD
  0010: 41 54 41 20 20 20 20 20 54 41 29 3e 0a 3c 18 20   ATA     TA)>.<. 
  0020: 20 20 79 6c 87 6e 6b 3a 68 72 65 66 20 20 20 43     yl.nk:href   C
  0030: 74 64 73 2f cf 32 37 37 37 32 2e 64 74 64 5c 0a   tds/.27772.dtd\.

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=008ff29e17e42a70, size=339 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=63057s, mutation_op=QwordAddMutator,ByteIncMutator,BytesDeleteMutator):
  0000: cb 00 00 00 31 32 37 37 37 32 6e 78 6d 6c 5c 0a   ....127772nxml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 0a   .0"?>.<!DOCTYPE.
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 29 cf   a SYSTEM "dtds).


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  4d(M)x1                             cb(.)x1                             DIFFER
   0x0001  20( )x1                             00(.)x1                             DIFFER
   0x0002  62(b)x1                             00(.)x1                             DIFFER
   0x0003  20( )x1                             00(.)x1                             DIFFER
   0x0004  28(()x1                             31(1)x1                             DIFFER
   0x0005  23(#)x1                             32(2)x1                             DIFFER
   0x0006  3b(;)x1                             37(7)x1                             DIFFER
   0x0007  78(x)x1                             37(7)x1                             DIFFER
   0x0008  6c(l)x1                             37(7)x1                             DIFFER
   0x0009  69(i)x1                             32(2)x1                             DIFFER
   0x000b  6b(k)x1                             78(x)x1                             DIFFER
   0x000c  21(!)x1                             6d(m)x1                             DIFFER
   0x000d  20( )x1                             6c(l)x1                             DIFFER
   0x000e  43(C)x1                             5c(\)x1                             DIFFER
   0x000f  44(D)x1                             0a(.)x1                             DIFFER
   0x0010  41(A)x1                             3c(<)x1                             DIFFER
   0x0011  54(T)x1                             3f(?)x1                             DIFFER
   0x0012  41(A)x1                             78(x)x1                             DIFFER
   0x0013  20( )x1                             6d(m)x1                             DIFFER
   0x0014  20( )x1                             6c(l)x1                             DIFFER
   0x0016  20( )x1                             76(v)x1                             DIFFER
   0x0017  20( )x1                             65(e)x1                             DIFFER
   0x0018  54(T)x1                             72(r)x1                             DIFFER
   0x0019  41(A)x1                             73(s)x1                             DIFFER
   0x001a  29())x1                             69(i)x1                             DIFFER
   0x001b  3e(>)x1                             6f(o)x1                             DIFFER
   0x001c  0a(.)x1                             6e(n)x1                             DIFFER
   0x001d  3c(<)x1                             3d(=)x1                             DIFFER
   0x001e  18(.)x1                             22(")x1                             DIFFER
   0x001f  20( )x1                             31(1)x1                             DIFFER
   0x0020  20( )x1                             2e(.)x1                             DIFFER
   0x0021  20( )x1                             30(0)x1                             DIFFER
   0x0022  79(y)x1                             22(")x1                             DIFFER
   0x0023  6c(l)x1                             3f(?)x1                             DIFFER
   0x0024  87(.)x1                             3e(>)x1                             DIFFER
   0x0025  6e(n)x1                             0a(.)x1                             DIFFER
   0x0026  6b(k)x1                             3c(<)x1                             DIFFER
   0x0027  3a(:)x1                             21(!)x1                             DIFFER
   0x0028  68(h)x1                             44(D)x1                             DIFFER
   0x0029  72(r)x1                             4f(O)x1                             DIFFER
   ... (22 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6837.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6837,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>value_profile_cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6837 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6837 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6837 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).