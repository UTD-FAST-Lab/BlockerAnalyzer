==== BLOCKER ====
Target: libxml2
Branch ID: 6835
Location: /src/libxml2/parser.c:11752:7
Enclosing function: parser.c:xmlParseTryOrFinish
Source line: 		    (ctxt->input->cur[6] == 'T') &&
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ngram_coverage vs naive_ngram4)
cmplog                           2        7          1  REFERENCE
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     9        1          0  winner (ngram_coverage vs naive)
mopt                             7        3          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ngram4']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ngram4 > naive  [delta: ngram_coverage] ---
  subject 36  (naive_ngram4 vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.40h  loser=13.70h
  avg hitcount on branch: winner=5  loser=1
  prob_div=0.70  dur_div=6.30h  hit_div=4
  subject-level: delta_AUC=-26852220.0  p_AUC=0.0173  delta_Final=-260.4  p_final=0.0312

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6835/{W,L}/branch_coverage_show.txt

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
[B] 11566  			ret += 5;
[ ] 11567  #ifdef DEBUG_PUSH
[ ] 11568  			xmlGenericError(xmlGenericErrorContext,
[ ] 11569  				"PP: Parsing XML Decl\n");
[ ] 11570  #endif
[B] 11571  			xmlParseXMLDecl(ctxt);
[B] 11572  			if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
[ ] 11573  			    /*
[ ] 11574  			     * The XML REC instructs us to stop parsing right
[ ] 11575  			     * here
[ ] 11576  			     */
[ ] 11577  			    xmlHaltParser(ctxt);
[ ] 11578  			    return(0);
[ ] 11579  			}
[B] 11580  			ctxt->standalone = ctxt->input->standalone;
[B] 11581  			if ((ctxt->encoding == NULL) &&
[B] 11582  			    (ctxt->input->encoding != NULL))
[ ] 11583  			    ctxt->encoding = xmlStrdup(ctxt->input->encoding);
[B] 11584  			if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[B] 11585  			    (!ctxt->disableSAX))
[B] 11586  			    ctxt->sax->startDocument(ctxt->userData);
[B] 11587  			ctxt->instate = XML_PARSER_MISC;
[ ] 11588  #ifdef DEBUG_PUSH
[ ] 11589  			xmlGenericError(xmlGenericErrorContext,
[ ] 11590  				"PP: entering MISC\n");
[ ] 11591  #endif
[B] 11592  		    } else {
[B] 11593  			ctxt->version = xmlCharStrdup(XML_DEFAULT_VERSION);
[B] 11594  			if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[B] 11595  			    (!ctxt->disableSAX))
[B] 11596  			    ctxt->sax->startDocument(ctxt->userData);
[B] 11597  			ctxt->instate = XML_PARSER_MISC;
[ ] 11598  #ifdef DEBUG_PUSH
[ ] 11599  			xmlGenericError(xmlGenericErrorContext,
[ ] 11600  				"PP: entering MISC\n");
[ ] 11601  #endif
[B] 11602  		    }
[B] 11603  		} else {
[B] 11604  		    if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
[B] 11605  			ctxt->sax->setDocumentLocator(ctxt->userData,
[B] 11606  						      &xmlDefaultSAXLocator);
[B] 11607  		    ctxt->version = xmlCharStrdup(XML_DEFAULT_VERSION);
[B] 11608  		    if (ctxt->version == NULL) {
[ ] 11609  		        xmlErrMemory(ctxt, NULL);
[ ] 11610  			break;
[ ] 11611  		    }
[B] 11612  		    if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[B] 11613  		        (!ctxt->disableSAX))
[B] 11614  			ctxt->sax->startDocument(ctxt->userData);
[B] 11615  		    ctxt->instate = XML_PARSER_MISC;
[ ] 11616  #ifdef DEBUG_PUSH
[ ] 11617  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11618  			    "PP: entering MISC\n");
[ ] 11619  #endif
[B] 11620  		}
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
[ ] 11642  		    spacePush(ctxt, -1);
[B] 11643  		else if (*ctxt->space == -2)
[B] 11644  		    spacePush(ctxt, -1);
[B] 11645  		else
[B] 11646  		    spacePush(ctxt, *ctxt->space);
[B] 11647  #ifdef LIBXML_SAX1_ENABLED
[B] 11648  		if (ctxt->sax2)
[B] 11649  #endif /* LIBXML_SAX1_ENABLED */
[B] 11650  		    name = xmlParseStartTag2(ctxt, &prefix, &URI, &tlen);
[B] 11651  #ifdef LIBXML_SAX1_ENABLED
[B] 11652  		else
[B] 11653  		    name = xmlParseStartTag(ctxt);
[B] 11654  #endif /* LIBXML_SAX1_ENABLED */
[B] 11655  		if (ctxt->instate == XML_PARSER_EOF)
[ ] 11656  		    goto done;
[B] 11657  		if (name == NULL) {
[B] 11658  		    spacePop(ctxt);
[B] 11659  		    xmlHaltParser(ctxt);
[B] 11660  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[B] 11661  			ctxt->sax->endDocument(ctxt->userData);
[B] 11662  		    goto done;
[B] 11663  		}
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
[W] 11728  		    ctxt->instate = XML_PARSER_END_TAG;
[W] 11729  		    break;
[B] 11730  	        } else if ((cur == '<') && (next == '?')) {
[W] 11731  		    if ((!terminate) &&
[W] 11732  		        (!xmlParseLookupString(ctxt, 2, "?>", 2)))
[ ] 11733  			goto done;
[W] 11734  		    xmlParsePI(ctxt);
[W] 11735  		    ctxt->instate = XML_PARSER_CONTENT;
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
[B] 11752  		    (ctxt->input->cur[6] == 'T') && <-- BLOCKER
[B] 11753  		    (ctxt->input->cur[7] == 'A') &&
[B] 11754  		    (ctxt->input->cur[8] == '[')) {
[L] 11755  		    SKIP(9);
[L] 11756  		    ctxt->instate = XML_PARSER_CDATA_SECTION;
[L] 11757  		    break;
[B] 11758  		} else if ((cur == '<') && (next == '!') &&
[B] 11759  		           (avail < 9)) {
[B] 11760  		    goto done;
[B] 11761  		} else if (cur == '<') {
[B] 11762  		    xmlFatalErr(ctxt, XML_ERR_INTERNAL_ERROR,
[B] 11763  		                "detected an error in element content\n");
[B] 11764                      SKIP(1);
[B] 11765  		} else if (cur == '&') {
[L] 11766  		    if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
[ ] 11767  			goto done;
[L] 11768  		    xmlParseReference(ctxt);
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
[W] 11793  		if (avail < 2)
[ ] 11794  		    goto done;
[W] 11795  		if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
[ ] 11796  		    goto done;
[W] 11797  		if (ctxt->sax2) {
[W] 11798  	            xmlParseEndTag2(ctxt, &ctxt->pushTab[ctxt->nameNr - 1]);
[W] 11799  		    nameNsPop(ctxt);
[W] 11800  		}
[ ] 11801  #ifdef LIBXML_SAX1_ENABLED
[ ] 11802  		  else
[ ] 11803  		    xmlParseEndTag1(ctxt, 0);
[W] 11804  #endif /* LIBXML_SAX1_ENABLED */
[W] 11805  		if (ctxt->instate == XML_PARSER_EOF) {
[ ] 11806  		    /* Nothing */
[W] 11807  		} else if (ctxt->nameNr == 0) {
[ ] 11808  		    ctxt->instate = XML_PARSER_EPILOG;
[W] 11809  		} else {
[W] 11810  		    ctxt->instate = XML_PARSER_CONTENT;
[W] 11811  		}
[W] 11812  		break;
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
[L] 11832  		    int tmp, size;
[ ] 11833  
[L] 11834                      if (terminate) {
[ ] 11835                          /* Unfinished CDATA section */
[L] 11836                          size = ctxt->input->end - ctxt->input->cur;
[L] 11837                      } else {
[L] 11838                          if (avail < XML_PARSER_BIG_BUFFER_SIZE + 2)
[L] 11839                              goto done;
[L] 11840                          ctxt->checkIndex = 0;
[ ] 11841                          /* XXX: Why don't we pass the full buffer? */
[L] 11842                          size = XML_PARSER_BIG_BUFFER_SIZE;
[L] 11843                      }
[L] 11844                      tmp = xmlCheckCdataPush(ctxt->input->cur, size, 0);
[L] 11845                      if (tmp <= 0) {
[L] 11846                          tmp = -tmp;
[L] 11847                          ctxt->input->cur += tmp;
[L] 11848                          goto encoding_error;
[L] 11849                      }
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
[B] 11919  		    if ((!terminate) &&
[B] 11920                          (!xmlParseLookupString(ctxt, 2, "?>", 2)))
[ ] 11921  			goto done;
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
[B] 12239          return(ctxt->errNo);
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
     289        93  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706)
      28        97  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      10        49  parser.c:xmlParseLookupString  (/src/libxml2/parser.c:11137-11161)
       0        30  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600)
       8        36  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752)
       8        33  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
       5        24  parser.c:xmlNsErr  (/src/libxml2/parser.c:688-700)
       3        18  xmlParseVersionInfo  (/src/libxml2/parser.c:10347-10378)
       3        18  xmlParseXMLDecl  (/src/libxml2/parser.c:10658-10766)
       0        15  parser.c:xmlCheckCdataPush  (/src/libxml2/parser.c:11338-11392)
       3        12  xmlParseVersionNum  (/src/libxml2/parser.c:10284-10329)
       2         9  xmlParseNmtoken  (/src/libxml2/parser.c:3687-3775)
       0         6  xmlParseEncodingDecl  (/src/libxml2/parser.c:10460-10558)
       0         6  xmlParseSDDecl  (/src/libxml2/parser.c:10594-10644)
       0         5  xmlParseCDSect  (/src/libxml2/parser.c:9862-9958)
... (8 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=2   L12141  T=0 F=13  T=0 F=26  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12152  T=0 F=28  T=2 F=41  (chunk[size - 1] == '\r')) {
  d=2   L12248  T=0 F=23  T=0 F=46  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12257  T=0 F=0  T=2 F=0  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=2   L12257  T=0 F=37  T=2 F=56  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=2   L12258  T=0 F=0  T=2 F=0  (ctxt->input->buf != NULL)) {
  d=2   L12274  T=6 F=0  T=12 F=0  if (ctxt->input != NULL) {
  d=2   L12275  T=0 F=6  T=0 F=12  if (ctxt->input->buf == NULL)
  d=2   L12283  T=6 F=0  T=12 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=2   L12284  T=6 F=0  T=12 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=2   L12287  T=0 F=6  T=0 F=12  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=2   L12290  T=6 F=0  T=12 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=2   L12291  T=6 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L12291  T=6 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
--- d=1  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=1   L11535  T=0 F=14  T=0 F=31  if (avail < 2)
  d=1   L11539  T=0 F=14  T=0 F=31  if (cur == 0) {
  d=1   L11553  T=6 F=6  T=25 F=6  if ((cur == '<') && (next == '?')) {
  d=1   L11553  T=12 F=2  T=31 F=0  if ((cur == '<') && (next == '?')) {
  d=1   L11555  T=0 F=6  T=0 F=25  if (avail < 5) goto done;
  d=1   L11556  T=6 F=0  T=22 F=3  if ((!terminate) &&
  d=1   L11557  T=0 F=6  T=9 F=13  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=1   L11559  T=6 F=0  T=16 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11559  T=6 F=0  T=16 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L11562  T=2 F=4  T=14 F=2  if ((ctxt->input->cur[2] == 'x') &&
  d=1   L11563  T=2 F=0  T=14 F=0  (ctxt->input->cur[3] == 'm') &&
  d=1   L11564  T=2 F=0  T=12 F=2  (ctxt->input->cur[4] == 'l') &&
  d=1   L11572  T=0 F=2  T=0 F=12  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=1   L11581  T=2 F=0  T=12 F=0  if ((ctxt->encoding == NULL) &&
  d=1   L11582  T=0 F=2  T=0 F=12  (ctxt->input->encoding != NULL))
  d=1   L11584  T=2 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11584  T=2 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11585  T=2 F=0  T=12 F=0  (!ctxt->disableSAX))
  d=1   L11639  T=28 F=78  T=6 F=31  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11660  T=4 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L11660  T=4 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L11678  T=0 F=0  T=0 F=1  if ((RAW == '/') && (NXT(1) == '>')) {
  d=1   L11678  T=0 F=92  T=1 F=59  if ((RAW == '/') && (NXT(1) == '>')) {
  d=1   L11727  T=3 F=110  T=0 F=79  if ((cur == '<') && (next == '/')) {
  d=1   L11730  T=2 F=108  T=0 F=79  } else if ((cur == '<') && (next == '?')) {
  d=1   L11731  T=0 F=2  T=0 F=0  if ((!terminate) &&
  d=1   L11750  T=12 F=0  T=22 F=1  (ctxt->input->cur[4] == 'D') &&
  d=1   L11752  T=0 F=12  T=21 F=1  (ctxt->input->cur[6] == 'T') &&  <-- BLOCKER
  d=1   L11753  T=0 F=0  T=21 F=0  (ctxt->input->cur[7] == 'A') &&
  d=1   L11754  T=0 F=0  T=17 F=4  (ctxt->input->cur[8] == '[')) {
  d=1   L11758  T=24 F=292  T=21 F=129  } else if ((cur == '<') && (next == '!') &&
  d=1   L11761  T=20 F=292  T=19 F=129  } else if (cur == '<') {
  d=1   L11765  T=0 F=292  T=1 F=128  } else if (cur == '&') {
  d=1   L11766  T=0 F=0  T=0 F=1  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=1   L11782  T=292 F=0  T=128 F=0  if ((ctxt->inputNr == 1) &&
  d=1   L11783  T=252 F=40  T=101 F=27  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=1   L11784  T=3 F=86  T=6 F=34  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=1   L11784  T=89 F=163  T=40 F=61  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=1   L11792  T=3 F=580  T=0 F=394  case XML_PARSER_END_TAG:
  d=1   L11793  T=0 F=3  T=0 F=0  if (avail < 2)
  d=1   L11795  T=0 F=3  T=0 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=1   L11795  T=3 F=0  T=0 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=1   L11797  T=3 F=0  T=0 F=0  if (ctxt->sax2) {
  d=1   L11805  T=0 F=3  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF) {
  d=1   L11807  T=0 F=3  T=0 F=0  } else if (ctxt->nameNr == 0) {
  d=1   L11813  T=0 F=583  T=34 F=360  case XML_PARSER_CDATA_SECTION: {
  d=1   L11820  T=0 F=0  T=11 F=23  if (terminate) {
  d=1   L11831  T=0 F=0  T=34 F=0  if (term == NULL) {
  d=1   L11834  T=0 F=0  T=11 F=23  if (terminate) {
  d=1   L11838  T=0 F=0  T=19 F=4  if (avail < XML_PARSER_BIG_BUFFER_SIZE + 2)
  d=1   L11845  T=0 F=0  T=15 F=0  if (tmp <= 0) {
  d=1   L11930  T=0 F=6  T=0 F=12  (ctxt->input->cur[2] == '-') &&
  d=1   L11944  T=6 F=0  T=12 F=0  (ctxt->input->cur[2] == 'D') &&
  d=1   L11945  T=6 F=0  T=12 F=0  (ctxt->input->cur[3] == 'O') &&
  d=1   L11946  T=6 F=0  T=12 F=0  (ctxt->input->cur[4] == 'C') &&
  d=1   L11947  T=6 F=0  T=12 F=0  (ctxt->input->cur[5] == 'T') &&
  d=1   L11948  T=6 F=0  T=12 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=1   L11949  T=6 F=0  T=12 F=0  (ctxt->input->cur[7] == 'P') &&
  d=1   L11950  T=6 F=0  T=12 F=0  (ctxt->input->cur[8] == 'E')) {
  d=1   L11951  T=6 F=0  T=12 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11951  T=0 F=6  T=0 F=12  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11959  T=0 F=6  T=0 F=12  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L11961  T=0 F=6  T=0 F=12  if (RAW == '[') {
  d=1   L11972  T=6 F=0  T=12 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L11972  T=6 F=0  T=12 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L11973  T=6 F=0  T=12 F=0  (ctxt->sax->externalSubset != NULL))

[off-chain: 462 additional divergent branches across 49 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=170e39f3164fa329, size=606 bytes, fuzzer=naive_ngram4, trial=1):
  0000: a9 a9 00 00 00 d9 0a 3c 61 3e 6d 00 78 78 00 00   .......<a>m.xx..
  0010: 31 32 37 37 37 cd 2e 78 6c 6c 5c 0a 3c 64 74 64   12777..xll\.<dtd
  0020: dd 3e 0a 0a 48 61 3e 09 20 20 3c 62 20 78 6c 69   .>..Ha>.  <b xli
  0030: 6e 6b 3a 68 72 65 b6 dd 20 20 3c 62 20 78 6c 69   nk:hre..  <b xli
Seed 2 (id=28c239943f64f894, size=654 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 27 68 74 74 4e 3a 2f 2f 77 21 45 4c 97 97 97 97   'httN://w!EL....
  0010: 97 97 97 97 97 ba 4d 45 ac ac ac ac ac ac ac ac   ......ME........
  0020: ac 54 ac 54 ac ac ac ac ac ac ac 54 ac ac 53 ac   .T.T.......T..S.
  0030: ac ac ac ac ac 54 ac ac ac ac 5b 5b 5b 5b 5b 78   .....T....[[[[[x
Seed 3 (id=6f453c99e506f0e2, size=171 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 6d 78 6d 5c 0a 3c 00 78 6d 6c 1f 76 c0 ff ff c2   mxm\.<.xml.v....
  0010: 0a 3c 54 54 54 54 54 54 57 54 54 54 54 54 54 54   .<TTTTTTWTTTTTTT
  0020: 21 41 54 54 4c 49 53 54 1f b7 54 54 54 54 54 54   !ATTLIST..TTTTTT
  0030: 54 54 54 54 54 54 54 b7 b7 b7 b7 b7 b7 b7 b7 d2   TTTTTTT.........
Seed 4 (id=708384bd4c086e5c, size=408 bytes, fuzzer=naive_ngram4, trial=1):
  0000: 97 f4 f4 8c 70 3a 2f 2f 57 77 41 53 43 61 10 05   ....p://WwASCa..
  0010: 04 2f 2f 2f bb 31 ef ff ff 3f 31 cd cd cd cd cd   .///.1...?1.....
  0020: cd 43 61 f0 05 02 5c 0a 3c 3f 54 45 4d 20 22 64   .Ca...\.<?TEM "d
  0030: 74 4d 20 22 64 74 64 73 2f 31 32 37 37 37 78 6d   tM "dtds/12777xm
Seed 5 (id=728cd4e6929e2170, size=135 bytes, fuzzer=naive_ngram4, trial=1):
  0000: ff ff 4e 06 00 00 d2 3c 39 3c bc 3c 3c 78 6d 6c   ..N....<9<.<<xml
  0010: 5c 0a 3c 6c 69 6e 6b 3a 78 4c d3 d2 3e 0a 35 35   \.<link:xL..>.55
  0020: 35 35 d5 d5 d5 00 3c 6c 69 6e 6b 3a 00 3c 6c 69   55....<link:.<li
  0030: 6e 6b 3a 68 4c d3 d2 3e 0a 1f 20 54 41 5b 00 78   nk:hL..>.. TA[.x

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0fe9594b7926be06, size=198 bytes, fuzzer=naive, trial=2, discovered_at=579s, mutation_op=ByteInterestingMutator,TokenInsert,ByteFlipMutator,DwordInterestingMutator):
  0000: 37 55 54 46 2d ce 36 00 37 32 2e 78 6d 6c 5c 0a   7UTF-.6.72.xml\.
  0010: 3c 74 45 4c 45 4d 45 4e 54 20 62 20 28 23 50 43   <tELEMENT b (#PC
  0020: 44 41 54 41 29 3e 0a 3c 21 61 3e 0a 20 20 3c 62   DATA)>.<!a>.  <b
  0030: 20 78 6c 69 6e 6b 3a 68 72 65 37 55 54 46 2d 3c    xlink:hre7UTF-<
Seed 2 (id=1b510a12d2cd6229, size=340 bytes, fuzzer=naive, trial=2, discovered_at=816s, mutation_op=TokenInsert,QwordAddMutator,WordAddMutator,BytesSetMutator,BytesDeleteMutator):
  0000: 29 00 00 00 80 3e 3e 3e 3e 3e 3e 3e 6d 6c 5c 0a   )....>>>>>>>ml\.
  0010: 3c 3f 78 6d 6c 20 64 65 72 73 69 6f 6e 53 54 45   <?xml dersionSTE
  0020: 4d 20 22 64 74 64 73 2f 31 33 37 37 37 32 2e 64   M "dtds/137772.d
  0030: 74 64 22 3e 0a 0a 3c 61 3e 0a 20 20 3c 21 5b 43   td">..<a>.  <![C
Seed 3 (id=21dca19767db2c4c, size=395 bytes, fuzzer=naive, trial=2, discovered_at=991s, mutation_op=BytesInsertMutator,TokenReplace,ByteIncMutator,BytesSwapMutator,BytesRandSetMutator):
  0000: 6b 27 0a 20 20 20 20 20 20 20 20 20 20 20 20 78   k'.            x
  0010: 6c 00 00 0e 00 20 20 20 44 41 54 41 20 20 20 20   l....   DATA    
  0020: 20 23 46 49 58 45 44 20 27 68 74 74 70 3a 2f 2f    #FIXED 'http://
  0030: 77 77 77 2e 77 33 37 37 32 2e 78 6d 6c 5c 0a 3c   www.w3772.xml\.<
Seed 4 (id=442ee7fadac1ec66, size=417 bytes, fuzzer=naive, trial=2, discovered_at=1775s, mutation_op=WordAddMutator,BytesCopyMutator,ByteAddMutator,CrossoverInsertMutator,WordAddMutator,BytesCopyMutator):
  0000: 4d 45 4e 54 20 61 20 28 62 2a 29 3e 0a 0a 3c 21   MENT a (b*)>..<!
  0010: 45 4c 45 4d 45 4e 54 20 62 20 28 23 50 43 44 41   ELEMENT b (#PCDA
  0020: 54 41 29 3e 0a 3c 21 41 54 54 4c 39 53 54 20 62   TA)>.<!ATTL9ST b
  0030: 20 78 6d 6c 6e 73 3a 78 6c 69 6e 6b 3c 21 5b 43    xmlns:xlink<![C
Seed 5 (id=1df12df0576b98c4, size=163 bytes, fuzzer=naive, trial=2, discovered_at=2403s, mutation_op=ByteDecMutator,ByteFlipMutator):
  0000: 19 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 77 20 75 65 72 73 69 6f 6e 3d 22 31   <?xmw uersion="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0004  00(.)x3 70(p)x2 4e(N)x1 0a(.)x1     20( )x2 34(4)x2 2d(-)x1 80(.)x1 +5u  DIFFER
   0x0005  3a(:)x3 d9(.)x2 3c(<)x1 00(.)x1     2e(.)x2 ce(.)x1 3e(>)x1 20( )x1 +6u  PARTIAL
   0x0006  2f(/)x3 0a(.)x2 00(.)x1 d2(.)x1     20( )x2 2e(.)x2 36(6)x1 3e(>)x1 +5u  DIFFER
   0x0007  3c(<)x3 2f(/)x3 78(x)x1             00(.)x2 20( )x2 2e(.)x2 3e(>)x1 +4u  DIFFER
   0x000d  78(x)x3 61(a)x2 97(.)x1 ff(.)x1     6c(l)x4 2f(/)x2 20( )x1 0a(.)x1 +3u  PARTIAL
   0x0023  0a(.)x2 54(T)x2 f0(.)x2 d5(.)x1     41(A)x2 3e(>)x2 64(d)x1 49(I)x1 +5u  DIFFER
   0x002a  54(T)x3 3c(<)x2 ac(.)x1 6b(k)x1     20( )x2 3e(>)x1 37(7)x1 74(t)x1 +6u  DIFFER
   0x002b  62(b)x2 54(T)x2 45(E)x2 3a(:)x1     0a(.)x1 37(7)x1 74(t)x1 39(9)x1 +7u  PARTIAL
   0x002e  6c(l)x3 22(")x2 53(S)x1 54(T)x1     20( )x2 2c(,)x2 3c(<)x1 2e(.)x1 +5u  PARTIAL
   0x002f  69(i)x3 64(d)x2 ac(.)x1 54(T)x1     62(b)x2 2f(/)x2 64(d)x1 20( )x1 +5u  PARTIAL
   0x0030  6e(n)x3 74(t)x2 ac(.)x1 54(T)x1     20( )x2 74(t)x1 77(w)x1 61(a)x1 +6u  PARTIAL
   0x0031  6b(k)x3 4d(M)x2 ac(.)x1 54(T)x1     78(x)x2 20( )x2 64(d)x1 77(w)x1 +5u  DIFFER
   0x0032  3a(:)x3 20( )x2 ac(.)x1 54(T)x1     22(")x2 6c(l)x1 77(w)x1 6d(m)x1 +6u  PARTIAL
   0x0033  68(h)x3 22(")x2 ac(.)x1 54(T)x1     69(i)x1 3e(>)x1 2e(.)x1 6c(l)x1 +7u  DIFFER
   0x0035  65(e)x2 54(T)x2 74(t)x2 d3(.)x1     6b(k)x1 0a(.)x1 33(3)x1 73(s)x1 +7u  PARTIAL
   0x003d  78(x)x2 5b([)x2 37(7)x2 b7(.)x1     21(!)x2 46(F)x1 5c(\)x1 73(s)x1 +6u  DIFFER
   0x003f  69(i)x2 78(x)x2 6d(m)x2 d2(.)x1     3c(<)x2 43(C)x2 31(1)x1 61(a)x1 +5u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6835.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6835,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ngram4>naive (ngram_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6835 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6835 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6835 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).