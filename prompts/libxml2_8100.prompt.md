==== BLOCKER ====
Target: libxml2
Branch ID: 8100
Location: /src/libxml2/parser.c:12008:37
Enclosing function: parser.c:xmlParseTryOrFinish
Source line:                 if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        7          3  REFERENCE
cmplog                           0        9          1  loser (value_profile vs value_profile_cmplog)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             1        4          5  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=9  unreached=1
  avg duration blocked: winner=8.40h  loser=18.11h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.80  dur_div=9.71h  hit_div=2
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/8100/{W,L}/branch_coverage_show.txt

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
[W] 11472  	    return(0);
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
[ ] 11501  	    goto done;
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
[ ] 11558  			goto done;
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
[L] 11593  			ctxt->version = xmlCharStrdup(XML_DEFAULT_VERSION);
[L] 11594  			if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[L] 11595  			    (!ctxt->disableSAX))
[L] 11596  			    ctxt->sax->startDocument(ctxt->userData);
[L] 11597  			ctxt->instate = XML_PARSER_MISC;
[ ] 11598  #ifdef DEBUG_PUSH
[ ] 11599  			xmlGenericError(xmlGenericErrorContext,
[ ] 11600  				"PP: entering MISC\n");
[ ] 11601  #endif
[L] 11602  		    }
[B] 11603  		} else {
[ ] 11604  		    if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
[ ] 11605  			ctxt->sax->setDocumentLocator(ctxt->userData,
[ ] 11606  						      &xmlDefaultSAXLocator);
[ ] 11607  		    ctxt->version = xmlCharStrdup(XML_DEFAULT_VERSION);
[ ] 11608  		    if (ctxt->version == NULL) {
[ ] 11609  		        xmlErrMemory(ctxt, NULL);
[ ] 11610  			break;
[ ] 11611  		    }
[ ] 11612  		    if ((ctxt->sax) && (ctxt->sax->startDocument) &&
[ ] 11613  		        (!ctxt->disableSAX))
[ ] 11614  			ctxt->sax->startDocument(ctxt->userData);
[ ] 11615  		    ctxt->instate = XML_PARSER_MISC;
[ ] 11616  #ifdef DEBUG_PUSH
[ ] 11617  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11618  			    "PP: entering MISC\n");
[ ] 11619  #endif
[ ] 11620  		}
[B] 11621  		break;
[B] 11622              case XML_PARSER_START_TAG: {
[W] 11623  	        const xmlChar *name;
[W] 11624  		const xmlChar *prefix = NULL;
[W] 11625  		const xmlChar *URI = NULL;
[W] 11626                  int line = ctxt->input->line;
[W] 11627  		int nsNr = ctxt->nsNr;
[ ] 11628  
[W] 11629  		if ((avail < 2) && (ctxt->inputNr == 1))
[ ] 11630  		    goto done;
[W] 11631  		cur = ctxt->input->cur[0];
[W] 11632  	        if (cur != '<') {
[W] 11633  		    xmlFatalErr(ctxt, XML_ERR_DOCUMENT_EMPTY, NULL);
[W] 11634  		    xmlHaltParser(ctxt);
[W] 11635  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[W] 11636  			ctxt->sax->endDocument(ctxt->userData);
[W] 11637  		    goto done;
[W] 11638  		}
[W] 11639  		if ((!terminate) && (!xmlParseLookupGt(ctxt)))
[ ] 11640                      goto done;
[W] 11641  		if (ctxt->spaceNr == 0)
[ ] 11642  		    spacePush(ctxt, -1);
[W] 11643  		else if (*ctxt->space == -2)
[ ] 11644  		    spacePush(ctxt, -1);
[W] 11645  		else
[W] 11646  		    spacePush(ctxt, *ctxt->space);
[W] 11647  #ifdef LIBXML_SAX1_ENABLED
[W] 11648  		if (ctxt->sax2)
[W] 11649  #endif /* LIBXML_SAX1_ENABLED */
[W] 11650  		    name = xmlParseStartTag2(ctxt, &prefix, &URI, &tlen);
[ ] 11651  #ifdef LIBXML_SAX1_ENABLED
[ ] 11652  		else
[ ] 11653  		    name = xmlParseStartTag(ctxt);
[W] 11654  #endif /* LIBXML_SAX1_ENABLED */
[W] 11655  		if (ctxt->instate == XML_PARSER_EOF)
[ ] 11656  		    goto done;
[W] 11657  		if (name == NULL) {
[ ] 11658  		    spacePop(ctxt);
[ ] 11659  		    xmlHaltParser(ctxt);
[ ] 11660  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[ ] 11661  			ctxt->sax->endDocument(ctxt->userData);
[ ] 11662  		    goto done;
[ ] 11663  		}
[W] 11664  #ifdef LIBXML_VALID_ENABLED
[ ] 11665  		/*
[ ] 11666  		 * [ VC: Root Element Type ]
[ ] 11667  		 * The Name in the document type declaration must match
[ ] 11668  		 * the element type of the root element.
[ ] 11669  		 */
[W] 11670  		if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
[W] 11671  		    ctxt->node && (ctxt->node == ctxt->myDoc->children))
[ ] 11672  		    ctxt->valid &= xmlValidateRoot(&ctxt->vctxt, ctxt->myDoc);
[W] 11673  #endif /* LIBXML_VALID_ENABLED */
[ ] 11674  
[ ] 11675  		/*
[ ] 11676  		 * Check for an Empty Element.
[ ] 11677  		 */
[W] 11678  		if ((RAW == '/') && (NXT(1) == '>')) {
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
[W] 11707  		if (RAW == '>') {
[ ] 11708  		    NEXT;
[W] 11709  		} else {
[W] 11710  		    xmlFatalErrMsgStr(ctxt, XML_ERR_GT_REQUIRED,
[W] 11711  					 "Couldn't find end of Start Tag %s\n",
[W] 11712  					 name);
[W] 11713  		    nodePop(ctxt);
[W] 11714  		    spacePop(ctxt);
[W] 11715  		}
[W] 11716                  nameNsPush(ctxt, name, prefix, URI, line, ctxt->nsNr - nsNr);
[ ] 11717  
[W] 11718  		ctxt->instate = XML_PARSER_CONTENT;
[W] 11719                  break;
[W] 11720  	    }
[ ] 11721              case XML_PARSER_CONTENT: {
[ ] 11722  		if ((avail < 2) && (ctxt->inputNr == 1))
[ ] 11723  		    goto done;
[ ] 11724  		cur = ctxt->input->cur[0];
[ ] 11725  		next = ctxt->input->cur[1];
[ ] 11726  
[ ] 11727  		if ((cur == '<') && (next == '/')) {
[ ] 11728  		    ctxt->instate = XML_PARSER_END_TAG;
[ ] 11729  		    break;
[ ] 11730  	        } else if ((cur == '<') && (next == '?')) {
[ ] 11731  		    if ((!terminate) &&
[ ] 11732  		        (!xmlParseLookupString(ctxt, 2, "?>", 2)))
[ ] 11733  			goto done;
[ ] 11734  		    xmlParsePI(ctxt);
[ ] 11735  		    ctxt->instate = XML_PARSER_CONTENT;
[ ] 11736  		} else if ((cur == '<') && (next != '!')) {
[ ] 11737  		    ctxt->instate = XML_PARSER_START_TAG;
[ ] 11738  		    break;
[ ] 11739  		} else if ((cur == '<') && (next == '!') &&
[ ] 11740  		           (ctxt->input->cur[2] == '-') &&
[ ] 11741  			   (ctxt->input->cur[3] == '-')) {
[ ] 11742  		    if ((!terminate) &&
[ ] 11743  		        (!xmlParseLookupString(ctxt, 4, "-->", 3)))
[ ] 11744  			goto done;
[ ] 11745  		    xmlParseComment(ctxt);
[ ] 11746  		    ctxt->instate = XML_PARSER_CONTENT;
[ ] 11747  		} else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
[ ] 11748  		    (ctxt->input->cur[2] == '[') &&
[ ] 11749  		    (ctxt->input->cur[3] == 'C') &&
[ ] 11750  		    (ctxt->input->cur[4] == 'D') &&
[ ] 11751  		    (ctxt->input->cur[5] == 'A') &&
[ ] 11752  		    (ctxt->input->cur[6] == 'T') &&
[ ] 11753  		    (ctxt->input->cur[7] == 'A') &&
[ ] 11754  		    (ctxt->input->cur[8] == '[')) {
[ ] 11755  		    SKIP(9);
[ ] 11756  		    ctxt->instate = XML_PARSER_CDATA_SECTION;
[ ] 11757  		    break;
[ ] 11758  		} else if ((cur == '<') && (next == '!') &&
[ ] 11759  		           (avail < 9)) {
[ ] 11760  		    goto done;
[ ] 11761  		} else if (cur == '<') {
[ ] 11762  		    xmlFatalErr(ctxt, XML_ERR_INTERNAL_ERROR,
[ ] 11763  		                "detected an error in element content\n");
[ ] 11764                      SKIP(1);
[ ] 11765  		} else if (cur == '&') {
[ ] 11766  		    if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
[ ] 11767  			goto done;
[ ] 11768  		    xmlParseReference(ctxt);
[ ] 11769  		} else {
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
[ ] 11782  		    if ((ctxt->inputNr == 1) &&
[ ] 11783  		        (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
[ ] 11784  			if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
[ ] 11785  			    goto done;
[ ] 11786                      }
[ ] 11787                      ctxt->checkIndex = 0;
[ ] 11788  		    xmlParseCharData(ctxt, 0);
[ ] 11789  		}
[ ] 11790  		break;
[ ] 11791  	    }
[ ] 11792              case XML_PARSER_END_TAG:
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
[L] 11919  		    if ((!terminate) &&
[L] 11920                          (!xmlParseLookupString(ctxt, 2, "?>", 2)))
[ ] 11921  			goto done;
[ ] 11922  #ifdef DEBUG_PUSH
[ ] 11923  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11924  			    "PP: Parsing PI\n");
[ ] 11925  #endif
[L] 11926  		    xmlParsePI(ctxt);
[L] 11927  		    if (ctxt->instate == XML_PARSER_EOF)
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
[B] 11962  			ctxt->instate = XML_PARSER_DTD;
[ ] 11963  #ifdef DEBUG_PUSH
[ ] 11964  			xmlGenericError(xmlGenericErrorContext,
[ ] 11965  				"PP: entering DTD\n");
[ ] 11966  #endif
[B] 11967  		    } else {
[ ] 11968  			/*
[ ] 11969  			 * Create and update the external subset.
[ ] 11970  			 */
[ ] 11971  			ctxt->inSubset = 2;
[ ] 11972  			if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
[ ] 11973  			    (ctxt->sax->externalSubset != NULL))
[ ] 11974  			    ctxt->sax->externalSubset(ctxt->userData,
[ ] 11975  				    ctxt->intSubName, ctxt->extSubSystem,
[ ] 11976  				    ctxt->extSubURI);
[ ] 11977  			ctxt->inSubset = 0;
[ ] 11978  			xmlCleanSpecialAttr(ctxt);
[ ] 11979  			ctxt->instate = XML_PARSER_PROLOG;
[ ] 11980  #ifdef DEBUG_PUSH
[ ] 11981  			xmlGenericError(xmlGenericErrorContext,
[ ] 11982  				"PP: entering PROLOG\n");
[ ] 11983  #endif
[ ] 11984  		    }
[B] 11985  		} else if ((cur == '<') && (next == '!') &&
[W] 11986  		           (avail <
[ ] 11987                              (ctxt->instate == XML_PARSER_MISC ? 9 : 4))) {
[ ] 11988  		    goto done;
[W] 11989  		} else if (ctxt->instate == XML_PARSER_EPILOG) {
[ ] 11990  		    xmlFatalErr(ctxt, XML_ERR_DOCUMENT_END, NULL);
[ ] 11991  		    xmlHaltParser(ctxt);
[ ] 11992  #ifdef DEBUG_PUSH
[ ] 11993  		    xmlGenericError(xmlGenericErrorContext,
[ ] 11994  			    "PP: entering EOF\n");
[ ] 11995  #endif
[ ] 11996  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[ ] 11997  			ctxt->sax->endDocument(ctxt->userData);
[ ] 11998  		    goto done;
[W] 11999                  } else {
[W] 12000  		    ctxt->instate = XML_PARSER_START_TAG;
[ ] 12001  #ifdef DEBUG_PUSH
[ ] 12002  		    xmlGenericError(xmlGenericErrorContext,
[ ] 12003  			    "PP: entering START_TAG\n");
[ ] 12004  #endif
[W] 12005  		}
[B] 12006  		break;
[B] 12007              case XML_PARSER_DTD: {
[B] 12008                  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt))) <-- BLOCKER
[L] 12009                      goto done;
[B] 12010  		xmlParseInternalSubset(ctxt);
[B] 12011  		if (ctxt->instate == XML_PARSER_EOF)
[B] 12012  		    goto done;
[W] 12013  		ctxt->inSubset = 2;
[W] 12014  		if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
[W] 12015  		    (ctxt->sax->externalSubset != NULL))
[W] 12016  		    ctxt->sax->externalSubset(ctxt->userData, ctxt->intSubName,
[W] 12017  			    ctxt->extSubSystem, ctxt->extSubURI);
[W] 12018  		ctxt->inSubset = 0;
[W] 12019  		xmlCleanSpecialAttr(ctxt);
[W] 12020  		if (ctxt->instate == XML_PARSER_EOF)
[W] 12021  		    goto done;
[W] 12022  		ctxt->instate = XML_PARSER_PROLOG;
[ ] 12023  #ifdef DEBUG_PUSH
[ ] 12024  		xmlGenericError(xmlGenericErrorContext,
[ ] 12025  			"PP: entering PROLOG\n");
[ ] 12026  #endif
[W] 12027                  break;
[W] 12028  	    }
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
[L] 12230  	}
[L] 12231      }
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
      16        69  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120)  <-- enclosing
      27         3  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      21         0  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      20         0  parser.c:xmlCleanSpecialAttr  (/src/libxml2/parser.c:1353-1364)
      18         0  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
      15         3  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
       9         0  nodePop  (/src/libxml2/parser.c:1788-1802)
       9         0  parser.c:nameNsPush  (/src/libxml2/parser.c:1820-1860)
       9         0  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
       9         0  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
       9         0  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       9         0  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
       9         0  parser.c:xmlGetNamespace  (/src/libxml2/parser.c:8856-8867)
       9         0  parser.c:xmlParseAttribute2  (/src/libxml2/parser.c:9225-9323)
       9         0  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774)
... (16 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=2   L12139  T=0 F=30  T=0 F=69  if (ctxt == NULL)
  d=2   L12141  T=14 F=0  T=0 F=6  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12141  T=14 F=16  T=6 F=63  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12143  T=0 F=16  T=0 F=69  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L12145  T=0 F=16  T=0 F=69  if (ctxt->input == NULL)
  d=2   L12149  T=16 F=0  T=26 F=43  if (ctxt->instate == XML_PARSER_START)
  d=2   L12151  T=16 F=0  T=38 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=2   L12151  T=16 F=0  T=38 F=31  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=2   L12151  T=16 F=0  T=38 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=2   L12152  T=0 F=16  T=0 F=38  (chunk[size - 1] == '\r')) {
  d=2   L12159  T=16 F=0  T=38 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=2   L12159  T=16 F=0  T=38 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=2   L12159  T=16 F=0  T=38 F=31  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=2   L12160  T=16 F=0  T=38 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=2   L12160  T=16 F=0  T=38 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=2   L12170  T=16 F=0  T=26 F=12  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=2   L12202  T=0 F=16  T=0 F=38  if (res < 0) {
  d=2   L12211  T=0 F=0  T=31 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=2   L12212  T=0 F=0  T=31 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=2   L12212  T=0 F=0  T=31 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=2   L12214  T=0 F=0  T=0 F=31  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=2   L12233  T=0 F=16  T=0 F=69  if (remain != 0) {
  d=2   L12238  T=10 F=6  T=22 F=47  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L12241  T=6 F=0  T=47 F=0  if ((ctxt->input != NULL) &&
  d=2   L12242  T=0 F=6  T=0 F=47  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=2   L12243  T=0 F=6  T=0 F=47  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=2   L12248  T=6 F=0  T=0 F=10  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12248  T=6 F=0  T=10 F=37  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L12251  T=0 F=0  T=0 F=47  if (remain != 0) {
  d=2   L12257  T=0 F=0  T=0 F=47  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=2   L12268  T=0 F=0  T=0 F=47  if (terminate) {
  d=2   L12296  T=0 F=0  T=10 F=37  if (ctxt->wellFormed == 0)
--- d=1  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=1   L11409  T=0 F=16  T=0 F=69  if (ctxt->input == NULL)
  d=1   L11465  T=16 F=0  T=69 F=0  if ((ctxt->input != NULL) &&
  d=1   L11466  T=0 F=16  T=0 F=69  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=1   L11471  T=6 F=12  T=0 F=18  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=1   L11594  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11594  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=1   L11595  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=1   L11622  T=12 F=68  T=0 F=136  case XML_PARSER_START_TAG: {
  d=1   L11629  T=0 F=12  T=0 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=1   L11632  T=6 F=6  T=0 F=0  if (cur != '<') {
  d=1   L11635  T=6 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L11635  T=6 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L11639  T=0 F=6  T=0 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11639  T=6 F=0  T=0 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=1   L11641  T=0 F=6  T=0 F=0  if (ctxt->spaceNr == 0)
  d=1   L11643  T=0 F=6  T=0 F=0  else if (*ctxt->space == -2)
  d=1   L11648  T=6 F=0  T=0 F=0  if (ctxt->sax2)
  d=1   L11655  T=0 F=6  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L11657  T=0 F=6  T=0 F=0  if (name == NULL) {
  d=1   L11670  T=0 F=6  T=0 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=1   L11678  T=0 F=6  T=0 F=0  if ((RAW == '/') && (NXT(1) == '>')) {
  d=1   L11707  T=0 F=6  T=0 F=0  if (RAW == '>') {
  d=1   L11905  T=12 F=68  T=0 F=136  case XML_PARSER_PROLOG:
  d=1   L11918  T=22 F=6  T=28 F=0  if ((cur == '<') && (next == '?')) {
  d=1   L11918  T=0 F=22  T=2 F=26  if ((cur == '<') && (next == '?')) {
  d=1   L11919  T=0 F=0  T=2 F=0  if ((!terminate) &&
  d=1   L11920  T=0 F=0  T=0 F=2  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=1   L11927  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L11929  T=16 F=6  T=26 F=0  } else if ((cur == '<') && (next == '!') &&
  d=1   L11929  T=22 F=6  T=26 F=0  } else if ((cur == '<') && (next == '!') &&
  d=1   L11942  T=16 F=12  T=26 F=0  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=1   L11985  T=0 F=6  T=0 F=0  } else if ((cur == '<') && (next == '!') &&
  d=1   L11985  T=6 F=6  T=0 F=0  } else if ((cur == '<') && (next == '!') &&
  d=1   L11989  T=0 F=12  T=0 F=0  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=1   L12008  T=16 F=0  T=47 F=22  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))  <-- BLOCKER
  d=1   L12008  T=0 F=16  T=47 F=0  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))  <-- BLOCKER
  d=1   L12011  T=2 F=14  T=22 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L12014  T=14 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L12014  T=14 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=1   L12015  T=14 F=0  T=0 F=0  (ctxt->sax->externalSubset != NULL))
  d=1   L12020  T=2 F=12  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)

[off-chain: 342 additional divergent branches across 46 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=e4810e547821e499, size=406 bytes, fuzzer=value_profile_cmplog, trial=3, discovered_at=7874s, mutation_op=DwordAddMutator,DwordInterestingMutator,BitFlipMutator,BytesInsertMutator,WordInterestingMutator,BytesInsertMutator,BytesRandInsertMutator):
  0000: 49 53 4f 2d 38 38 35 39 2d 39 2e 78 6d 6c 5c 0a   ISO-8859-9.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 28 2e 2e 2e 2e d2 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e   (...............
  0030: 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61   0"?>.<!DOCTYPE a
Seed 2 (id=10558da3e9f1b1c5, size=372 bytes, fuzzer=value_profile_cmplog, trial=3, discovered_at=11174s, mutation_op=BytesSetMutator,BytesDeleteMutator,BytesCopyMutator,BytesDeleteMutator,BytesRandInsertMutator,ByteFlipMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=36e56c94f8152ee7, size=368 bytes, fuzzer=value_profile_cmplog, trial=3, discovered_at=11379s, mutation_op=ByteIncMutator,CrossoverInsertMutator,BytesCopyMutator,ByteDecMutator,ByteAddMutator,DwordAddMutator):
  0000: 06 00 00 00 ff 32 37 37 37 32 2e 78 6d 6c 5c 0a   .....27772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 3a 2f 2f   a SYSTEM "dtd://
Seed 4 (id=bb2c83dd2141e9cb, size=406 bytes, fuzzer=value_profile_cmplog, trial=3, discovered_at=12419s, mutation_op=BytesSetMutator,TokenInsert,BytesDeleteMutator,CrossoverReplaceMutator,QwordAddMutator,ByteIncMutator,BytesDeleteMutator):
  0000: 49 53 4f 2d 38 38 35 39 2d 39 2e 78 6d 6c 5c 0a   ISO-8859-9.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 28 2e 2e 2e 2e d2 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e   (...............
  0030: 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 5f 61   0"?>.<!DOCTYPE_a
Seed 5 (id=556623055323f214, size=733 bytes, fuzzer=value_profile_cmplog, trial=3, discovered_at=16177s, mutation_op=BytesRandSetMutator,ByteDecMutator,TokenInsert,DwordAddMutator):
  0000: 44 20 27 68 74 74 70 3a 2f 2f 77 77 ff d7 ff ff   D 'http://ww....
  0010: 2e 6f 72 67 05 fd fc 39 39 2f 78 6c 69 6e 6b 27   .org...99/xlink'
  0020: 0a 20 20 20 20 62 20 20 20 20 20 20 39 39 39 2f   .    b      999/
  0030: 78 6c 69 6e 6b 27 0a 20 20 20 20 41 20 20 20 20   xlink'.    A    

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=024c5e8f763ecbb8, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=7s, mutation_op=ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 7e 31   a SYSTEM "dtds~1
Seed 2 (id=3b3da00795bdfae9, size=384 bytes, fuzzer=cmplog, trial=1, discovered_at=13s, mutation_op=ByteFlipMutator,BytesInsertMutator,BitFlipMutator):
  0000: 07 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 5b 53 54 45 4d 20 22 64 74 64 73 2f 31   a S[STEM "dtds/1
Seed 3 (id=2bdc02caf4641c89, size=273 bytes, fuzzer=cmplog, trial=1, discovered_at=14s, mutation_op=WordAddMutator,ByteNegMutator,WordAddMutator,BytesSwapMutator,DwordAddMutator,ByteNegMutator,BytesDeleteMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=276dd1ab222ed96d, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=235s, mutation_op=CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2d 78 6d 6c 5c 0a   ....127772-xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 0a   .0"?>.<!DOCTYPE.
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=0469ab6830ee2cdb, size=381 bytes, fuzzer=cmplog, trial=2, discovered_at=442s, mutation_op=BytesCopyMutator,BytesExpandMutator):
  0000: 06 00 28 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ..(.127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 0a 73 3d 31   a SYSTEM "dt.s=1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x4 49(I)x2 44(D)x2             06(.)x9 07(.)x2 37(7)x2             PARTIAL
   0x0001  00(.)x4 53(S)x2 20( )x2             00(.)x11 37(7)x2                    PARTIAL
   0x0002  00(.)x4 4f(O)x2 27(')x2             00(.)x10 28(()x1 37(7)x1 32(2)x1    PARTIAL
   0x0003  00(.)x4 2d(-)x2 68(h)x2             00(.)x9 80(.)x2 32(2)x1 2e(.)x1     PARTIAL
   0x0004  38(8)x2 31(1)x2 ff(.)x2 74(t)x2     31(1)x9 ff(.)x2 2e(.)x1 00(.)x1     PARTIAL
   0x0005  32(2)x4 38(8)x2 74(t)x2             32(2)x10 78(x)x1 4b(K)x1 6d(m)x1    PARTIAL
   0x0006  37(7)x4 35(5)x2 70(p)x2             37(7)x11 6d(m)x1 6c(l)x1            PARTIAL
   0x0007  37(7)x4 39(9)x2 3a(:)x2             37(7)x11 6c(l)x1 5c(\)x1            PARTIAL
   0x0008  37(7)x4 2d(-)x2 2f(/)x2             37(7)x11 5c(\)x1 0a(.)x1            PARTIAL
   0x0009  32(2)x4 39(9)x2 2f(/)x2             32(2)x10 0a(.)x1 5f(_)x1 3c(<)x1    PARTIAL
   0x000a  2e(.)x6 77(w)x2                     2e(.)x9 2d(-)x2 3c(<)x1 3f(?)x1     PARTIAL
   0x000b  78(x)x6 77(w)x2                     78(x)x11 3f(?)x1 d3(.)x1            PARTIAL
   0x000c  6d(m)x6 ff(.)x2                     6d(m)x11 78(x)x1 2d(-)x1            PARTIAL
   0x000d  6c(l)x6 d7(.)x2                     6c(l)x11 6d(m)x1 2d(-)x1            PARTIAL
   0x000e  5c(\)x6 ff(.)x2                     5c(\)x10 6c(l)x1 2d(-)x1 3a(:)x1    PARTIAL
   0x000f  0a(.)x6 ff(.)x2                     0a(.)x10 20( )x1 2d(-)x1 76(v)x1    PARTIAL
   0x0010  3c(<)x6 2e(.)x2                     3c(<)x10 76(v)x1 2d(-)x1 65(e)x1    PARTIAL
   0x0011  3f(?)x6 6f(o)x2                     3f(?)x10 65(e)x1 06(.)x1 72(r)x1    PARTIAL
   0x0012  78(x)x6 72(r)x2                     78(x)x10 72(r)x1 00(.)x1 73(s)x1    PARTIAL
   0x0013  6d(m)x6 67(g)x2                     6d(m)x10 73(s)x1 00(.)x1 69(i)x1    PARTIAL
   0x0014  6c(l)x6 05(.)x1 fc(.)x1             6c(l)x10 69(i)x1 00(.)x1 6f(o)x1    PARTIAL
   0x0015  20( )x6 fd(.)x1 fc(.)x1             20( )x9 6f(o)x1 31(1)x1 6e(n)x1 +1u  PARTIAL
   0x0016  76(v)x6 fc(.)x2                     76(v)x10 6e(n)x1 32(2)x1 3d(=)x1    PARTIAL
   0x0017  65(e)x6 39(9)x2                     65(e)x10 3d(=)x1 37(7)x1 22(")x1    PARTIAL
   0x0018  72(r)x6 39(9)x2                     72(r)x10 20( )x1 37(7)x1 31(1)x1    PARTIAL
   0x0019  73(s)x6 2f(/)x2                     73(s)x10 31(1)x1 37(7)x1 2e(.)x1    PARTIAL
   0x001a  69(i)x6 78(x)x2                     69(i)x10 2e(.)x1 32(2)x1 30(0)x1    PARTIAL
   0x001b  6f(o)x6 6c(l)x2                     6f(o)x10 30(0)x1 2e(.)x1 22(")x1    PARTIAL
   0x001c  6e(n)x6 69(i)x2                     6e(n)x10 22(")x1 78(x)x1 3f(?)x1    PARTIAL
   0x001d  3d(=)x6 6e(n)x2                     3d(=)x10 3f(?)x1 6d(m)x1 3e(>)x1    PARTIAL
   0x001e  22(")x6 6b(k)x2                     22(")x10 3e(>)x1 6c(l)x1 0a(.)x1    PARTIAL
   0x001f  31(1)x6 27(')x2                     31(1)x10 0a(.)x1 5c(\)x1 3c(<)x1    PARTIAL
   0x0020  2e(.)x4 28(()x2 0a(.)x2             2e(.)x10 3c(<)x1 0a(.)x1 21(!)x1    PARTIAL
   0x0021  30(0)x4 2e(.)x2 20( )x2             30(0)x10 21(!)x1 3c(<)x1 44(D)x1    PARTIAL
   0x0022  22(")x4 2e(.)x2 20( )x2             22(")x10 44(D)x1 3f(?)x1 4f(O)x1    PARTIAL
   0x0023  3f(?)x4 2e(.)x2 20( )x2             3f(?)x10 4f(O)x1 78(x)x1 43(C)x1    PARTIAL
   0x0024  3e(>)x4 2e(.)x2 20( )x2             3e(>)x10 43(C)x1 6d(m)x1 54(T)x1    PARTIAL
   0x0025  0a(.)x4 d2(.)x2 62(b)x2             0a(.)x10 54(T)x1 6c(l)x1 59(Y)x1    PARTIAL
   0x0026  3c(<)x4 2e(.)x2 20( )x2             3c(<)x10 59(Y)x1 20( )x1 50(P)x1    PARTIAL
   0x0027  21(!)x4 2e(.)x2 20( )x2             21(!)x10 50(P)x1 76(v)x1 45(E)x1    PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_8100.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8100,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8100 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8100 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8100 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).