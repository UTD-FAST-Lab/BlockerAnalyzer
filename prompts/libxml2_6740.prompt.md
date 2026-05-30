==== BLOCKER ====
Target: libxml2
Branch ID: 6740
Location: /src/libxml2/parser.c:9633:7
Enclosing function: parser.c:xmlParseStartTag2
Source line: 		if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           3        7          0  REFERENCE
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        2        7          1  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=4.40h  loser=19.40h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.80  dur_div=15.00h  hit_div=5
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6740/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlParseStartTag2 (/src/libxml2/parser.c:9355-9774) ---
[ ]  9353  static const xmlChar *
[ ]  9354  xmlParseStartTag2(xmlParserCtxtPtr ctxt, const xmlChar **pref,
[B]  9355                    const xmlChar **URI, int *tlen) {
[B]  9356      const xmlChar *localname;
[B]  9357      const xmlChar *prefix;
[B]  9358      const xmlChar *attname;
[B]  9359      const xmlChar *aprefix;
[B]  9360      const xmlChar *nsname;
[B]  9361      xmlChar *attvalue;
[B]  9362      const xmlChar **atts = ctxt->atts;
[B]  9363      int maxatts = ctxt->maxatts;
[B]  9364      int nratts, nbatts, nbdef, inputid;
[B]  9365      int i, j, nbNs, attval;
[B]  9366      unsigned long cur;
[B]  9367      int nsNr = ctxt->nsNr;
[ ]  9368  
[B]  9369      if (RAW != '<') return(NULL);
[B]  9370      NEXT1;
[ ]  9371  
[ ]  9372      /*
[ ]  9373       * NOTE: it is crucial with the SAX2 API to never call SHRINK beyond that
[ ]  9374       *       point since the attribute values may be stored as pointers to
[ ]  9375       *       the buffer and calling SHRINK would destroy them !
[ ]  9376       *       The Shrinking is only possible once the full set of attribute
[ ]  9377       *       callbacks have been done.
[ ]  9378       */
[B]  9379      SHRINK;
[B]  9380      cur = ctxt->input->cur - ctxt->input->base;
[B]  9381      inputid = ctxt->input->id;
[B]  9382      nbatts = 0;
[B]  9383      nratts = 0;
[B]  9384      nbdef = 0;
[B]  9385      nbNs = 0;
[B]  9386      attval = 0;
[ ]  9387      /* Forget any namespaces added during an earlier parse of this element. */
[B]  9388      ctxt->nsNr = nsNr;
[ ]  9389  
[B]  9390      localname = xmlParseQName(ctxt, &prefix);
[B]  9391      if (localname == NULL) {
[L]  9392  	xmlFatalErrMsg(ctxt, XML_ERR_NAME_REQUIRED,
[L]  9393  		       "StartTag: invalid element name\n");
[L]  9394          return(NULL);
[L]  9395      }
[B]  9396      *tlen = ctxt->input->cur - ctxt->input->base - cur;
[ ]  9397  
[ ]  9398      /*
[ ]  9399       * Now parse the attributes, it ends up with the ending
[ ]  9400       *
[ ]  9401       * (S Attribute)* S?
[ ]  9402       */
[B]  9403      SKIP_BLANKS;
[B]  9404      GROW;
[ ]  9405  
[B]  9406      while (((RAW != '>') &&
[B]  9407  	   ((RAW != '/') || (NXT(1) != '>')) &&
[B]  9408  	   (IS_BYTE_CHAR(RAW))) && (ctxt->instate != XML_PARSER_EOF)) {
[B]  9409  	int len = -1, alloc = 0;
[ ]  9410  
[B]  9411  	attname = xmlParseAttribute2(ctxt, prefix, localname,
[B]  9412  	                             &aprefix, &attvalue, &len, &alloc);
[B]  9413          if (attname == NULL) {
[ ]  9414  	    xmlFatalErr(ctxt, XML_ERR_INTERNAL_ERROR,
[ ]  9415  	         "xmlParseStartTag: problem parsing attributes\n");
[ ]  9416  	    break;
[ ]  9417  	}
[B]  9418          if (attvalue == NULL)
[B]  9419              goto next_attr;
[L]  9420  	if (len < 0) len = xmlStrlen(attvalue);
[ ]  9421  
[L]  9422          if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
[ ]  9423              const xmlChar *URL = xmlDictLookup(ctxt->dict, attvalue, len);
[ ]  9424              xmlURIPtr uri;
[ ]  9425  
[ ]  9426              if (URL == NULL) {
[ ]  9427                  xmlErrMemory(ctxt, "dictionary allocation failure");
[ ]  9428                  if ((attvalue != NULL) && (alloc != 0))
[ ]  9429                      xmlFree(attvalue);
[ ]  9430                  localname = NULL;
[ ]  9431                  goto done;
[ ]  9432              }
[ ]  9433              if (*URL != 0) {
[ ]  9434                  uri = xmlParseURI((const char *) URL);
[ ]  9435                  if (uri == NULL) {
[ ]  9436                      xmlNsErr(ctxt, XML_WAR_NS_URI,
[ ]  9437                               "xmlns: '%s' is not a valid URI\n",
[ ]  9438                                         URL, NULL, NULL);
[ ]  9439                  } else {
[ ]  9440                      if (uri->scheme == NULL) {
[ ]  9441                          xmlNsWarn(ctxt, XML_WAR_NS_URI_RELATIVE,
[ ]  9442                                    "xmlns: URI %s is not absolute\n",
[ ]  9443                                    URL, NULL, NULL);
[ ]  9444                      }
[ ]  9445                      xmlFreeURI(uri);
[ ]  9446                  }
[ ]  9447                  if (URL == ctxt->str_xml_ns) {
[ ]  9448                      if (attname != ctxt->str_xml) {
[ ]  9449                          xmlNsErr(ctxt, XML_NS_ERR_XML_NAMESPACE,
[ ]  9450                       "xml namespace URI cannot be the default namespace\n",
[ ]  9451                                   NULL, NULL, NULL);
[ ]  9452                      }
[ ]  9453                      goto next_attr;
[ ]  9454                  }
[ ]  9455                  if ((len == 29) &&
[ ]  9456                      (xmlStrEqual(URL,
[ ]  9457                               BAD_CAST "http://www.w3.org/2000/xmlns/"))) {
[ ]  9458                      xmlNsErr(ctxt, XML_NS_ERR_XML_NAMESPACE,
[ ]  9459                           "reuse of the xmlns namespace name is forbidden\n",
[ ]  9460                               NULL, NULL, NULL);
[ ]  9461                      goto next_attr;
[ ]  9462                  }
[ ]  9463              }
[ ]  9464              /*
[ ]  9465               * check that it's not a defined namespace
[ ]  9466               */
[ ]  9467              for (j = 1;j <= nbNs;j++)
[ ]  9468                  if (ctxt->nsTab[ctxt->nsNr - 2 * j] == NULL)
[ ]  9469                      break;
[ ]  9470              if (j <= nbNs)
[ ]  9471                  xmlErrAttributeDup(ctxt, NULL, attname);
[ ]  9472              else
[ ]  9473                  if (nsPush(ctxt, NULL, URL) > 0) nbNs++;
[ ]  9474  
[L]  9475          } else if (aprefix == ctxt->str_xmlns) {
[ ]  9476              const xmlChar *URL = xmlDictLookup(ctxt->dict, attvalue, len);
[ ]  9477              xmlURIPtr uri;
[ ]  9478  
[ ]  9479              if (attname == ctxt->str_xml) {
[ ]  9480                  if (URL != ctxt->str_xml_ns) {
[ ]  9481                      xmlNsErr(ctxt, XML_NS_ERR_XML_NAMESPACE,
[ ]  9482                               "xml namespace prefix mapped to wrong URI\n",
[ ]  9483                               NULL, NULL, NULL);
[ ]  9484                  }
[ ]  9485                  /*
[ ]  9486                   * Do not keep a namespace definition node
[ ]  9487                   */
[ ]  9488                  goto next_attr;
[ ]  9489              }
[ ]  9490              if (URL == ctxt->str_xml_ns) {
[ ]  9491                  if (attname != ctxt->str_xml) {
[ ]  9492                      xmlNsErr(ctxt, XML_NS_ERR_XML_NAMESPACE,
[ ]  9493                               "xml namespace URI mapped to wrong prefix\n",
[ ]  9494                               NULL, NULL, NULL);
[ ]  9495                  }
[ ]  9496                  goto next_attr;
[ ]  9497              }
[ ]  9498              if (attname == ctxt->str_xmlns) {
[ ]  9499                  xmlNsErr(ctxt, XML_NS_ERR_XML_NAMESPACE,
[ ]  9500                           "redefinition of the xmlns prefix is forbidden\n",
[ ]  9501                           NULL, NULL, NULL);
[ ]  9502                  goto next_attr;
[ ]  9503              }
[ ]  9504              if ((len == 29) &&
[ ]  9505                  (xmlStrEqual(URL,
[ ]  9506                               BAD_CAST "http://www.w3.org/2000/xmlns/"))) {
[ ]  9507                  xmlNsErr(ctxt, XML_NS_ERR_XML_NAMESPACE,
[ ]  9508                           "reuse of the xmlns namespace name is forbidden\n",
[ ]  9509                           NULL, NULL, NULL);
[ ]  9510                  goto next_attr;
[ ]  9511              }
[ ]  9512              if ((URL == NULL) || (URL[0] == 0)) {
[ ]  9513                  xmlNsErr(ctxt, XML_NS_ERR_XML_NAMESPACE,
[ ]  9514                           "xmlns:%s: Empty XML namespace is not allowed\n",
[ ]  9515                                attname, NULL, NULL);
[ ]  9516                  goto next_attr;
[ ]  9517              } else {
[ ]  9518                  uri = xmlParseURI((const char *) URL);
[ ]  9519                  if (uri == NULL) {
[ ]  9520                      xmlNsErr(ctxt, XML_WAR_NS_URI,
[ ]  9521                           "xmlns:%s: '%s' is not a valid URI\n",
[ ]  9522                                         attname, URL, NULL);
[ ]  9523                  } else {
[ ]  9524                      if ((ctxt->pedantic) && (uri->scheme == NULL)) {
[ ]  9525                          xmlNsWarn(ctxt, XML_WAR_NS_URI_RELATIVE,
[ ]  9526                                    "xmlns:%s: URI %s is not absolute\n",
[ ]  9527                                    attname, URL, NULL);
[ ]  9528                      }
[ ]  9529                      xmlFreeURI(uri);
[ ]  9530                  }
[ ]  9531              }
[ ]  9532  
[ ]  9533              /*
[ ]  9534               * check that it's not a defined namespace
[ ]  9535               */
[ ]  9536              for (j = 1;j <= nbNs;j++)
[ ]  9537                  if (ctxt->nsTab[ctxt->nsNr - 2 * j] == attname)
[ ]  9538                      break;
[ ]  9539              if (j <= nbNs)
[ ]  9540                  xmlErrAttributeDup(ctxt, aprefix, attname);
[ ]  9541              else
[ ]  9542                  if (nsPush(ctxt, attname, URL) > 0) nbNs++;
[ ]  9543  
[L]  9544          } else {
[ ]  9545              /*
[ ]  9546               * Add the pair to atts
[ ]  9547               */
[L]  9548              if ((atts == NULL) || (nbatts + 5 > maxatts)) {
[L]  9549                  if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
[ ]  9550                      goto next_attr;
[ ]  9551                  }
[L]  9552                  maxatts = ctxt->maxatts;
[L]  9553                  atts = ctxt->atts;
[L]  9554              }
[L]  9555              ctxt->attallocs[nratts++] = alloc;
[L]  9556              atts[nbatts++] = attname;
[L]  9557              atts[nbatts++] = aprefix;
[ ]  9558              /*
[ ]  9559               * The namespace URI field is used temporarily to point at the
[ ]  9560               * base of the current input buffer for non-alloced attributes.
[ ]  9561               * When the input buffer is reallocated, all the pointers become
[ ]  9562               * invalid, but they can be reconstructed later.
[ ]  9563               */
[L]  9564              if (alloc)
[ ]  9565                  atts[nbatts++] = NULL;
[L]  9566              else
[L]  9567                  atts[nbatts++] = ctxt->input->base;
[L]  9568              atts[nbatts++] = attvalue;
[L]  9569              attvalue += len;
[L]  9570              atts[nbatts++] = attvalue;
[ ]  9571              /*
[ ]  9572               * tag if some deallocation is needed
[ ]  9573               */
[L]  9574              if (alloc != 0) attval = 1;
[L]  9575              attvalue = NULL; /* moved into atts */
[L]  9576          }
[ ]  9577  
[B]  9578  next_attr:
[B]  9579          if ((attvalue != NULL) && (alloc != 0)) {
[ ]  9580              xmlFree(attvalue);
[ ]  9581              attvalue = NULL;
[ ]  9582          }
[ ]  9583  
[B]  9584  	GROW
[B]  9585          if (ctxt->instate == XML_PARSER_EOF)
[ ]  9586              break;
[B]  9587  	if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
[L]  9588  	    break;
[B]  9589  	if (SKIP_BLANKS == 0) {
[B]  9590  	    xmlFatalErrMsg(ctxt, XML_ERR_SPACE_REQUIRED,
[B]  9591  			   "attributes construct error\n");
[B]  9592  	    break;
[B]  9593  	}
[ ]  9594          GROW;
[ ]  9595      }
[ ]  9596  
[B]  9597      if (ctxt->input->id != inputid) {
[ ]  9598          xmlFatalErr(ctxt, XML_ERR_INTERNAL_ERROR,
[ ]  9599                      "Unexpected change of input\n");
[ ]  9600          localname = NULL;
[ ]  9601          goto done;
[ ]  9602      }
[ ]  9603  
[ ]  9604      /* Reconstruct attribute value pointers. */
[B]  9605      for (i = 0, j = 0; j < nratts; i += 5, j++) {
[L]  9606          if (atts[i+2] != NULL) {
[ ]  9607              /*
[ ]  9608               * Arithmetic on dangling pointers is technically undefined
[ ]  9609               * behavior, but well...
[ ]  9610               */
[L]  9611              const xmlChar *old = atts[i+2];
[L]  9612              atts[i+2]  = NULL;    /* Reset repurposed namespace URI */
[L]  9613              atts[i+3] = ctxt->input->base + (atts[i+3] - old);  /* value */
[L]  9614              atts[i+4] = ctxt->input->base + (atts[i+4] - old);  /* valuend */
[L]  9615          }
[L]  9616      }
[ ]  9617  
[ ]  9618      /*
[ ]  9619       * The attributes defaulting
[ ]  9620       */
[B]  9621      if (ctxt->attsDefault != NULL) {
[B]  9622          xmlDefAttrsPtr defaults;
[ ]  9623  
[B]  9624  	defaults = xmlHashLookup2(ctxt->attsDefault, localname, prefix);
[B]  9625  	if (defaults != NULL) {
[B]  9626  	    for (i = 0;i < defaults->nbAttrs;i++) {
[B]  9627  	        attname = defaults->values[5 * i];
[B]  9628  		aprefix = defaults->values[5 * i + 1];
[ ]  9629  
[ ]  9630                  /*
[ ]  9631  		 * special work for namespaces defaulted defs
[ ]  9632  		 */
[B]  9633  		if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) { <-- BLOCKER
[ ]  9634  		    /*
[ ]  9635  		     * check that it's not a defined namespace
[ ]  9636  		     */
[W]  9637  		    for (j = 1;j <= nbNs;j++)
[ ]  9638  		        if (ctxt->nsTab[ctxt->nsNr - 2 * j] == NULL)
[ ]  9639  			    break;
[W]  9640  	            if (j <= nbNs) continue;
[ ]  9641  
[W]  9642  		    nsname = xmlGetNamespace(ctxt, NULL);
[W]  9643  		    if (nsname != defaults->values[5 * i + 2]) {
[W]  9644  			if (nsPush(ctxt, NULL,
[W]  9645  			           defaults->values[5 * i + 2]) > 0)
[W]  9646  			    nbNs++;
[W]  9647  		    }
[B]  9648  		} else if (aprefix == ctxt->str_xmlns) {
[ ]  9649  		    /*
[ ]  9650  		     * check that it's not a defined namespace
[ ]  9651  		     */
[L]  9652  		    for (j = 1;j <= nbNs;j++)
[ ]  9653  		        if (ctxt->nsTab[ctxt->nsNr - 2 * j] == attname)
[ ]  9654  			    break;
[L]  9655  	            if (j <= nbNs) continue;
[ ]  9656  
[L]  9657  		    nsname = xmlGetNamespace(ctxt, attname);
[L]  9658  		    if (nsname != defaults->values[5 * i + 2]) {
[L]  9659  			if (nsPush(ctxt, attname,
[L]  9660  			           defaults->values[5 * i + 2]) > 0)
[L]  9661  			    nbNs++;
[L]  9662  		    }
[L]  9663  		} else {
[ ]  9664  		    /*
[ ]  9665  		     * check that it's not a defined attribute
[ ]  9666  		     */
[L]  9667  		    for (j = 0;j < nbatts;j+=5) {
[L]  9668  			if ((attname == atts[j]) && (aprefix == atts[j+1]))
[ ]  9669  			    break;
[L]  9670  		    }
[L]  9671  		    if (j < nbatts) continue;
[ ]  9672  
[L]  9673  		    if ((atts == NULL) || (nbatts + 5 > maxatts)) {
[ ]  9674  			if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
[ ]  9675                              localname = NULL;
[ ]  9676                              goto done;
[ ]  9677  			}
[ ]  9678  			maxatts = ctxt->maxatts;
[ ]  9679  			atts = ctxt->atts;
[ ]  9680  		    }
[L]  9681  		    atts[nbatts++] = attname;
[L]  9682  		    atts[nbatts++] = aprefix;
[L]  9683  		    if (aprefix == NULL)
[ ]  9684  			atts[nbatts++] = NULL;
[L]  9685  		    else
[L]  9686  		        atts[nbatts++] = xmlGetNamespace(ctxt, aprefix);
[L]  9687  		    atts[nbatts++] = defaults->values[5 * i + 2];
[L]  9688  		    atts[nbatts++] = defaults->values[5 * i + 3];
[L]  9689  		    if ((ctxt->standalone == 1) &&
[L]  9690  		        (defaults->values[5 * i + 4] != NULL)) {
[ ]  9691  			xmlValidityError(ctxt, XML_DTD_STANDALONE_DEFAULTED,
[ ]  9692  	  "standalone: attribute %s on %s defaulted from external subset\n",
[ ]  9693  	                                 attname, localname);
[ ]  9694  		    }
[L]  9695  		    nbdef++;
[L]  9696  		}
[B]  9697  	    }
[B]  9698  	}
[B]  9699      }
[ ]  9700  
[ ]  9701      /*
[ ]  9702       * The attributes checkings
[ ]  9703       */
[B]  9704      for (i = 0; i < nbatts;i += 5) {
[ ]  9705          /*
[ ]  9706  	* The default namespace does not apply to attribute names.
[ ]  9707  	*/
[L]  9708  	if (atts[i + 1] != NULL) {
[L]  9709  	    nsname = xmlGetNamespace(ctxt, atts[i + 1]);
[L]  9710  	    if (nsname == NULL) {
[ ]  9711  		xmlNsErr(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[ ]  9712  		    "Namespace prefix %s for %s on %s is not defined\n",
[ ]  9713  		    atts[i + 1], atts[i], localname);
[ ]  9714  	    }
[L]  9715  	    atts[i + 2] = nsname;
[L]  9716  	} else
[ ]  9717  	    nsname = NULL;
[ ]  9718  	/*
[ ]  9719  	 * [ WFC: Unique Att Spec ]
[ ]  9720  	 * No attribute name may appear more than once in the same
[ ]  9721  	 * start-tag or empty-element tag.
[ ]  9722  	 * As extended by the Namespace in XML REC.
[ ]  9723  	 */
[L]  9724          for (j = 0; j < i;j += 5) {
[L]  9725  	    if (atts[i] == atts[j]) {
[ ]  9726  	        if (atts[i+1] == atts[j+1]) {
[ ]  9727  		    xmlErrAttributeDup(ctxt, atts[i+1], atts[i]);
[ ]  9728  		    break;
[ ]  9729  		}
[ ]  9730  		if ((nsname != NULL) && (atts[j + 2] == nsname)) {
[ ]  9731  		    xmlNsErr(ctxt, XML_NS_ERR_ATTRIBUTE_REDEFINED,
[ ]  9732  			     "Namespaced Attribute %s in '%s' redefined\n",
[ ]  9733  			     atts[i], nsname, NULL);
[ ]  9734  		    break;
[ ]  9735  		}
[ ]  9736  	    }
[L]  9737  	}
[L]  9738      }
[ ]  9739  
[B]  9740      nsname = xmlGetNamespace(ctxt, prefix);
[B]  9741      if ((prefix != NULL) && (nsname == NULL)) {
[ ]  9742  	xmlNsErr(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[ ]  9743  	         "Namespace prefix %s on %s is not defined\n",
[ ]  9744  		 prefix, localname, NULL);
[ ]  9745      }
[B]  9746      *pref = prefix;
[B]  9747      *URI = nsname;
[ ]  9748  
[ ]  9749      /*
[ ]  9750       * SAX: Start of Element !
[ ]  9751       */
[B]  9752      if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != NULL) &&
[B]  9753  	(!ctxt->disableSAX)) {
[B]  9754  	if (nbNs > 0)
[B]  9755  	    ctxt->sax->startElementNs(ctxt->userData, localname, prefix,
[B]  9756  			  nsname, nbNs, &ctxt->nsTab[ctxt->nsNr - 2 * nbNs],
[B]  9757  			  nbatts / 5, nbdef, atts);
[B]  9758  	else
[B]  9759  	    ctxt->sax->startElementNs(ctxt->userData, localname, prefix,
[B]  9760  	                  nsname, 0, NULL, nbatts / 5, nbdef, atts);
[B]  9761      }
[ ]  9762  
[B]  9763  done:
[ ]  9764      /*
[ ]  9765       * Free up attribute allocated strings if needed
[ ]  9766       */
[B]  9767      if (attval != 0) {
[ ]  9768  	for (i = 3,j = 0; j < nratts;i += 5,j++)
[ ]  9769  	    if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))
[ ]  9770  	        xmlFree((xmlChar *) atts[i]);
[ ]  9771      }
[ ]  9772  
[B]  9773      return(localname);
[B]  9774  }

--- Caller (1 hop): parser.c:xmlParseTryOrFinish (/src/libxml2/parser.c:11404-12120, calls parser.c:xmlParseStartTag2 at line 11650) (±10 around call site) ---
[L] 11640                      goto done;
[B] 11641  		if (ctxt->spaceNr == 0)
[ ] 11642  		    spacePush(ctxt, -1);
[B] 11643  		else if (*ctxt->space == -2)
[ ] 11644  		    spacePush(ctxt, -1);
[B] 11645  		else
[B] 11646  		    spacePush(ctxt, *ctxt->space);
[B] 11647  #ifdef LIBXML_SAX1_ENABLED
[B] 11648  		if (ctxt->sax2)
[B] 11649  #endif /* LIBXML_SAX1_ENABLED */
[B] 11650  		    name = xmlParseStartTag2(ctxt, &prefix, &URI, &tlen); <-- CALL
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

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226, calls parser.c:xmlParseStartTag2 at line 10142)
hop 2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls parser.c:xmlParseStartTag2 at line 11650)
hop 3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls parser.c:xmlParseElementStart at line 10010)
hop 3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 3  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseElementStart at line 10077)
hop 4  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 4  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 5  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 5  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 5  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 5  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 6  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 6  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 6  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 7  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 7  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 7  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        50  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
       3        15  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
       3        15  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)
       3        15  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203)
       3        12  parser.c:xmlAddSpecialAttr  (/src/libxml2/parser.c:1308-1325)
       3        12  parser.c:xmlCleanSpecialAttrCallback  (/src/libxml2/parser.c:1335-1341)
       3        12  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
       3        12  xmlParseAttValue  (/src/libxml2/parser.c:4229-4232)
       0         6  parser.c:xmlAttrNormalizeSpace  (/src/libxml2/parser.c:1102-1120)
       3         9  parser.c:xmlAddDefAttrs  (/src/libxml2/parser.c:1194-1292)
       0         6  xmlParseNmtoken  (/src/libxml2/parser.c:3687-3775)
       0         6  parser.c:xmlParseAttValueComplex  (/src/libxml2/parser.c:3948-4190)
       0         6  xmlParseEnumerationType  (/src/libxml2/parser.c:5879-5930)
       0         6  xmlParseEnumeratedType  (/src/libxml2/parser.c:5950-5965)
       1         5  parser.c:xmlHaltParser  (/src/libxml2/parser.c:12416-12441)
... (6 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=4   L10816  T=0 F=1  T=0 F=2  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10816  T=0 F=1  T=0 F=2  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10829  T=1 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10829  T=1 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10831  T=0 F=1  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10834  T=1 F=0  T=2 F=0  if ((ctxt->encoding == NULL) &&
  d=4   L10835  T=1 F=0  T=2 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=4   L10846  T=1 F=0  T=2 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=4   L10852  T=0 F=1  T=0 F=2  if (CUR == 0) {
  d=4   L10863  T=0 F=1  T=0 F=2  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=4   L10872  T=0 F=1  T=0 F=2  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=4   L10873  T=0 F=1  T=0 F=2  (ctxt->instate == XML_PARSER_EOF)) {
  d=4   L10884  T=1 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=1 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=1 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10886  T=0 F=1  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10888  T=1 F=0  T=2 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10888  T=1 F=0  T=2 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10889  T=1 F=0  T=2 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10889  T=0 F=1  T=0 F=2  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10907  T=0 F=1  T=0 F=2  if (RAW == '[') {
  d=4   L10918  T=1 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10918  T=1 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10919  T=1 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=4   L10922  T=0 F=1  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10936  T=0 F=1  T=0 F=2  if (RAW != '<') {
  d=4   L10950  T=1 F=0  T=2 F=0  if (RAW != 0) {
  d=4   L10959  T=1 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10959  T=1 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10965  T=1 F=0  T=2 F=0  if ((ctxt->myDoc != NULL) &&
  d=4   L10966  T=0 F=1  T=0 F=2  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=4   L10971  T=0 F=1  T=0 F=2  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10980  T=1 F=0  T=2 F=0  if (! ctxt->wellFormed) {
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9973  T=4 F=0  T=10 F=0  while ((RAW != 0) &&
  d=3   L9974  T=4 F=0  T=10 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L9980  T=2 F=2  T=5 F=5  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=0 F=2  T=0 F=5  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=2 F=2  T=5 F=5  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=0 F=2  T=0 F=5  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L10004  T=2 F=2  T=5 F=5  else if (*cur == '<') {
  d=3   L10005  T=1 F=1  T=3 F=2  if (NXT(1) == '/') {
  d=3   L10006  T=1 F=0  T=2 F=1  if (ctxt->nameNr <= nameNr)
  d=3   L10019  T=0 F=2  T=0 F=5  else if (*cur == '&') {
--- d=3  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=3   L10077  T=0 F=1  T=0 F=2  if (xmlParseElementStart(ctxt) != 0)
  d=3   L10081  T=0 F=1  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L10084  T=0 F=1  T=0 F=2  if (CUR == 0) {
--- d=3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=3   L12139  T=0 F=3  T=0 F=6  if (ctxt == NULL)
  d=3   L12141  T=0 F=1  T=1 F=1  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12141  T=1 F=2  T=2 F=4  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12151  T=2 F=0  T=4 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12151  T=2 F=0  T=4 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12152  T=0 F=2  T=0 F=4  (chunk[size - 1] == '\r')) {
  d=3   L12159  T=2 F=0  T=4 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12159  T=2 F=0  T=4 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12160  T=2 F=0  T=4 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=3   L12160  T=2 F=0  T=4 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=3   L12170  T=2 F=0  T=4 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12170  T=2 F=0  T=4 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12171  T=2 F=0  T=4 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12171  T=0 F=2  T=0 F=4  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12202  T=0 F=2  T=0 F=4  if (res < 0) {
  d=3   L12238  T=0 F=3  T=3 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L12268  T=1 F=2  T=0 F=2  if (terminate) {
  d=3   L12274  T=1 F=0  T=0 F=0  if (ctxt->input != NULL) {
  d=3   L12275  T=0 F=1  T=0 F=0  if (ctxt->input->buf == NULL)
  d=3   L12283  T=1 F=0  T=0 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=3   L12284  T=0 F=1  T=0 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=3   L12287  T=0 F=1  T=0 F=0  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=3   L12287  T=1 F=0  T=0 F=0  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=3   L12290  T=1 F=0  T=0 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=3   L12291  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L12291  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
--- d=2  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226) ---
  d=2   L10115  T=0 F=2  T=0 F=4  if (((unsigned int) ctxt->nameNr > xmlParserMaxDepth) &&
  d=2   L10125  T=0 F=2  T=0 F=4  if (ctxt->record_info) {
  d=2   L10131  T=0 F=2  T=0 F=4  if (ctxt->spaceNr == 0)
  d=2   L10133  T=0 F=2  T=0 F=4  else if (*ctxt->space == -2)
  d=2   L10140  T=2 F=0  T=4 F=0  if (ctxt->sax2)
  d=2   L10147  T=0 F=2  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L10149  T=0 F=2  T=0 F=4  if (name == NULL) {
  d=2   L10162  T=0 F=0  T=0 F=2  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L10162  T=0 F=2  T=2 F=2  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L10170  T=0 F=2  T=0 F=4  if ((RAW == '/') && (NXT(1) == '>')) {
  d=2   L10196  T=1 F=1  T=3 F=1  if (RAW == '>') {
--- d=2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=2   L11500  T=1 F=29  T=0 F=51  if (avail < 1)
  d=2   L11509  T=1 F=2  T=2 F=4  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=2   L11516  T=0 F=1  T=0 F=2  if (avail < 4)
  d=2   L11535  T=0 F=2  T=0 F=4  if (avail < 2)
  d=2   L11539  T=0 F=2  T=0 F=4  if (cur == 0) {
  d=2   L11553  T=2 F=0  T=4 F=0  if ((cur == '<') && (next == '?')) {
  d=2   L11553  T=2 F=0  T=4 F=0  if ((cur == '<') && (next == '?')) {
  d=2   L11555  T=0 F=2  T=0 F=4  if (avail < 5) goto done;
  d=2   L11556  T=2 F=0  T=4 F=0  if ((!terminate) &&
  d=2   L11557  T=0 F=2  T=0 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=2   L11559  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11559  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11562  T=2 F=0  T=4 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=2   L11563  T=2 F=0  T=4 F=0  (ctxt->input->cur[3] == 'm') &&
  d=2   L11564  T=2 F=0  T=4 F=0  (ctxt->input->cur[4] == 'l') &&
  d=2   L11572  T=0 F=2  T=0 F=4  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=2   L11581  T=2 F=0  T=4 F=0  if ((ctxt->encoding == NULL) &&
  d=2   L11582  T=0 F=2  T=0 F=4  (ctxt->input->encoding != NULL))
  d=2   L11584  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11584  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11585  T=2 F=0  T=4 F=0  (!ctxt->disableSAX))
  d=2   L11629  T=0 F=4  T=0 F=10  if ((avail < 2) && (ctxt->inputNr == 1))
  d=2   L11632  T=0 F=4  T=0 F=10  if (cur != '<') {
  d=2   L11639  T=0 F=4  T=2 F=6  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11639  T=4 F=0  T=8 F=2  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11641  T=0 F=4  T=0 F=8  if (ctxt->spaceNr == 0)
  d=2   L11643  T=0 F=4  T=0 F=8  else if (*ctxt->space == -2)
  d=2   L11648  T=4 F=0  T=8 F=0  if (ctxt->sax2)
  d=2   L11655  T=0 F=4  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11657  T=0 F=4  T=1 F=7  if (name == NULL) {
  d=2   L11660  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L11660  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L11670  T=0 F=0  T=0 F=3  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L11670  T=0 F=4  T=3 F=4  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L11730  T=0 F=2  T=0 F=5  } else if ((cur == '<') && (next == '?')) {
  d=2   L11736  T=2 F=0  T=5 F=0  } else if ((cur == '<') && (next != '!')) {
  d=2   L11784  T=6 F=0  T=8 F=2  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=2   L11795  T=4 F=0  T=4 F=1  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=2   L11914  T=2 F=4  T=0 F=10  if (avail < 2)
  d=2   L11918  T=4 F=0  T=8 F=2  if ((cur == '<') && (next == '?')) {
  d=2   L11918  T=0 F=4  T=0 F=8  if ((cur == '<') && (next == '?')) {
  d=2   L11929  T=2 F=2  T=4 F=4  } else if ((cur == '<') && (next == '!') &&
  d=2   L11929  T=4 F=0  T=8 F=2  } else if ((cur == '<') && (next == '!') &&
  d=2   L11930  T=0 F=2  T=0 F=4  (ctxt->input->cur[2] == '-') &&
  d=2   L11942  T=2 F=2  T=4 F=6  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=2   L11943  T=2 F=0  T=4 F=0  (cur == '<') && (next == '!') &&
  d=2   L11943  T=2 F=0  T=4 F=0  (cur == '<') && (next == '!') &&
  d=2   L11944  T=2 F=0  T=4 F=0  (ctxt->input->cur[2] == 'D') &&
  d=2   L11945  T=2 F=0  T=4 F=0  (ctxt->input->cur[3] == 'O') &&
  d=2   L11946  T=2 F=0  T=4 F=0  (ctxt->input->cur[4] == 'C') &&
  d=2   L11947  T=2 F=0  T=4 F=0  (ctxt->input->cur[5] == 'T') &&
  d=2   L11948  T=2 F=0  T=4 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=2   L11949  T=2 F=0  T=4 F=0  (ctxt->input->cur[7] == 'P') &&
  d=2   L11950  T=2 F=0  T=4 F=0  (ctxt->input->cur[8] == 'E')) {
  d=2   L11951  T=2 F=0  T=4 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11951  T=0 F=2  T=0 F=4  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11959  T=0 F=2  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11961  T=0 F=2  T=0 F=4  if (RAW == '[') {
  d=2   L11972  T=2 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L11972  T=2 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L11973  T=2 F=0  T=4 F=0  (ctxt->sax->externalSubset != NULL))
  d=2   L11985  T=0 F=2  T=0 F=4  } else if ((cur == '<') && (next == '!') &&
  d=2   L11985  T=2 F=0  T=4 F=2  } else if ((cur == '<') && (next == '!') &&
  d=2   L11989  T=0 F=2  T=2 F=4  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=2   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
--- d=1  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774) ---
  d=1   L9369  T=0 F=6  T=0 F=12  if (RAW != '<') return(NULL);
  d=1   L9391  T=0 F=6  T=1 F=11  if (localname == NULL) {
  d=1   L9418  T=3 F=0  T=2 F=3  if (attvalue == NULL)
  d=1   L9420  T=0 F=0  T=0 F=3  if (len < 0) len = xmlStrlen(attvalue);
  d=1   L9422  T=0 F=0  T=0 F=3  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
  d=1   L9475  T=0 F=0  T=0 F=3  } else if (aprefix == ctxt->str_xmlns) {
  d=1   L9548  T=0 F=0  T=3 F=0  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9549  T=0 F=0  T=0 F=3  if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
  d=1   L9564  T=0 F=0  T=0 F=3  if (alloc)
  d=1   L9574  T=0 F=0  T=0 F=3  if (alloc != 0) attval = 1;
  d=1   L9587  T=0 F=3  T=3 F=2  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=1   L9605  T=0 F=6  T=3 F=11  for (i = 0, j = 0; j < nratts; i += 5, j++) {
  d=1   L9606  T=0 F=0  T=3 F=0  if (atts[i+2] != NULL) {
  d=1   L9626  T=3 F=3  T=8 F=5  for (i = 0;i < defaults->nbAttrs;i++) {
  d=1   L9633  T=3 F=0  T=0 F=0  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {  <-- BLOCKER
  d=1   L9633  T=3 F=0  T=0 F=8  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {  <-- BLOCKER
  d=1   L9637  T=0 F=3  T=0 F=0  for (j = 1;j <= nbNs;j++)
  d=1   L9640  T=0 F=3  T=0 F=0  if (j <= nbNs) continue;
  d=1   L9643  T=3 F=0  T=0 F=0  if (nsname != defaults->values[5 * i + 2]) {
  d=1   L9644  T=3 F=0  T=0 F=0  if (nsPush(ctxt, NULL,
  d=1   L9648  T=0 F=0  T=5 F=3  } else if (aprefix == ctxt->str_xmlns) {
  d=1   L9652  T=0 F=0  T=0 F=5  for (j = 1;j <= nbNs;j++)
  d=1   L9655  T=0 F=0  T=0 F=5  if (j <= nbNs) continue;
  d=1   L9658  T=0 F=0  T=5 F=0  if (nsname != defaults->values[5 * i + 2]) {
  d=1   L9659  T=0 F=0  T=5 F=0  if (nsPush(ctxt, attname,
  d=1   L9667  T=0 F=0  T=3 F=3  for (j = 0;j < nbatts;j+=5) {
  d=1   L9668  T=0 F=0  T=0 F=3  if ((attname == atts[j]) && (aprefix == atts[j+1]))
  d=1   L9671  T=0 F=0  T=0 F=3  if (j < nbatts) continue;
  d=1   L9673  T=0 F=0  T=0 F=3  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9673  T=0 F=0  T=0 F=3  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9683  T=0 F=0  T=0 F=3  if (aprefix == NULL)
  d=1   L9689  T=0 F=0  T=0 F=3  if ((ctxt->standalone == 1) &&
  d=1   L9704  T=0 F=6  T=6 F=11  for (i = 0; i < nbatts;i += 5) {
  d=1   L9708  T=0 F=0  T=6 F=0  if (atts[i + 1] != NULL) {
  d=1   L9710  T=0 F=0  T=0 F=6  if (nsname == NULL) {
  d=1   L9724  T=0 F=0  T=3 F=6  for (j = 0; j < i;j += 5) {
  d=1   L9725  T=0 F=0  T=0 F=3  if (atts[i] == atts[j]) {

[off-chain: 510 additional divergent branches across 64 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=fc953d92fc9cf938, size=368 bytes, fuzzer=value_profile_cmplog, trial=3, discovered_at=3665s, mutation_op=ByteAddMutator,BytesSetMutator,ByteDecMutator,WordInterestingMutator):
  0000: 05 00 04 00 31 28 28 28 37 32 2e 78 6d 6c 5c 0a   ....1(((72.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=217ac7dcb8ad6589, size=368 bytes, fuzzer=value_profile, trial=3, discovered_at=146s, mutation_op=WordInterestingMutator,BytesSetMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=03f1b35383c4ff89, size=1040 bytes, fuzzer=value_profile, trial=2, discovered_at=61325s, mutation_op=WordInterestingMutator,DwordInterestingMutator):
  0000: db 20 3c 62 60 3e 0a 20 20 3c 61 3e 0a 20 20 3c   . <b`>.  <a>.  <
  0010: 62 20 87 6c 69 6e 6b 3a 68 72 3c 0a 0a 3c 61 3e   b .link:hr<..<a>
  0020: 0a 20 3c 0a 0a c3 61 3e 0a 20 20 3c 61 3e 0a 20   . <...a>.  <a>. 
  0030: 11 ff 7f 61 3e 0a 20 20 3c 61 3e 0a 20 20 20 0a   ...a>.  <a>.   .


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  05(.)x1                             06(.)x1 db(.)x1                     DIFFER
   0x0001  00(.)x1                             00(.)x1 20( )x1                     PARTIAL
   0x0002  04(.)x1                             00(.)x1 3c(<)x1                     DIFFER
   0x0003  00(.)x1                             00(.)x1 62(b)x1                     PARTIAL
   0x0004  31(1)x1                             31(1)x1 60(`)x1                     PARTIAL
   0x0005  28(()x1                             32(2)x1 3e(>)x1                     DIFFER
   0x0006  28(()x1                             37(7)x1 0a(.)x1                     DIFFER
   0x0007  28(()x1                             37(7)x1 20( )x1                     DIFFER
   0x0008  37(7)x1                             37(7)x1 20( )x1                     PARTIAL
   0x0009  32(2)x1                             32(2)x1 3c(<)x1                     PARTIAL
   0x000a  2e(.)x1                             2e(.)x1 61(a)x1                     PARTIAL
   0x000b  78(x)x1                             78(x)x1 3e(>)x1                     PARTIAL
   0x000c  6d(m)x1                             6d(m)x1 0a(.)x1                     PARTIAL
   0x000d  6c(l)x1                             6c(l)x1 20( )x1                     PARTIAL
   0x000e  5c(\)x1                             5c(\)x1 20( )x1                     PARTIAL
   0x000f  0a(.)x1                             0a(.)x1 3c(<)x1                     PARTIAL
   0x0010  3c(<)x1                             3c(<)x1 62(b)x1                     PARTIAL
   0x0011  3f(?)x1                             3f(?)x1 20( )x1                     PARTIAL
   0x0012  78(x)x1                             78(x)x1 87(.)x1                     PARTIAL
   0x0013  6d(m)x1                             6d(m)x1 6c(l)x1                     PARTIAL
   0x0014  6c(l)x1                             6c(l)x1 69(i)x1                     PARTIAL
   0x0015  20( )x1                             20( )x1 6e(n)x1                     PARTIAL
   0x0016  76(v)x1                             76(v)x1 6b(k)x1                     PARTIAL
   0x0017  65(e)x1                             65(e)x1 3a(:)x1                     PARTIAL
   0x0018  72(r)x1                             72(r)x1 68(h)x1                     PARTIAL
   0x0019  73(s)x1                             73(s)x1 72(r)x1                     PARTIAL
   0x001a  69(i)x1                             69(i)x1 3c(<)x1                     PARTIAL
   0x001b  6f(o)x1                             6f(o)x1 0a(.)x1                     PARTIAL
   0x001c  6e(n)x1                             6e(n)x1 0a(.)x1                     PARTIAL
   0x001d  3d(=)x1                             3d(=)x1 3c(<)x1                     PARTIAL
   0x001e  22(")x1                             22(")x1 61(a)x1                     PARTIAL
   0x001f  31(1)x1                             31(1)x1 3e(>)x1                     PARTIAL
   0x0020  2e(.)x1                             2e(.)x1 0a(.)x1                     PARTIAL
   0x0021  30(0)x1                             30(0)x1 20( )x1                     PARTIAL
   0x0022  22(")x1                             22(")x1 3c(<)x1                     PARTIAL
   0x0023  3f(?)x1                             3f(?)x1 0a(.)x1                     PARTIAL
   0x0024  3e(>)x1                             3e(>)x1 0a(.)x1                     PARTIAL
   0x0025  0a(.)x1                             0a(.)x1 c3(.)x1                     PARTIAL
   0x0026  3c(<)x1                             3c(<)x1 61(a)x1                     PARTIAL
   0x0027  21(!)x1                             21(!)x1 3e(>)x1                     PARTIAL
   ... (23 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6740.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6740,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6740 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6740 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6740 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).