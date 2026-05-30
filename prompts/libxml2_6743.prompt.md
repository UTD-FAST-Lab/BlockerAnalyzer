==== BLOCKER ====
Target: libxml2
Branch ID: 6743
Location: /src/libxml2/parser.c:9668:8
Enclosing function: parser.c:xmlParseStartTag2
Source line: 			if ((attname == atts[j]) && (aprefix == atts[j+1]))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    1        9          0  REFERENCE
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             3        5          2  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.00h  loser=20.40h
  avg hitcount on branch: winner=18  loser=0
  prob_div=0.80  dur_div=14.40h  hit_div=18
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6743/{W,L}/branch_coverage_show.txt

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
[L]  9414  	    xmlFatalErr(ctxt, XML_ERR_INTERNAL_ERROR,
[L]  9415  	         "xmlParseStartTag: problem parsing attributes\n");
[L]  9416  	    break;
[L]  9417  	}
[B]  9418          if (attvalue == NULL)
[L]  9419              goto next_attr;
[B]  9420  	if (len < 0) len = xmlStrlen(attvalue);
[ ]  9421  
[B]  9422          if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
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
[B]  9475          } else if (aprefix == ctxt->str_xmlns) {
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
[B]  9544          } else {
[ ]  9545              /*
[ ]  9546               * Add the pair to atts
[ ]  9547               */
[B]  9548              if ((atts == NULL) || (nbatts + 5 > maxatts)) {
[B]  9549                  if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
[ ]  9550                      goto next_attr;
[ ]  9551                  }
[B]  9552                  maxatts = ctxt->maxatts;
[B]  9553                  atts = ctxt->atts;
[B]  9554              }
[B]  9555              ctxt->attallocs[nratts++] = alloc;
[B]  9556              atts[nbatts++] = attname;
[B]  9557              atts[nbatts++] = aprefix;
[ ]  9558              /*
[ ]  9559               * The namespace URI field is used temporarily to point at the
[ ]  9560               * base of the current input buffer for non-alloced attributes.
[ ]  9561               * When the input buffer is reallocated, all the pointers become
[ ]  9562               * invalid, but they can be reconstructed later.
[ ]  9563               */
[B]  9564              if (alloc)
[B]  9565                  atts[nbatts++] = NULL;
[L]  9566              else
[L]  9567                  atts[nbatts++] = ctxt->input->base;
[B]  9568              atts[nbatts++] = attvalue;
[B]  9569              attvalue += len;
[B]  9570              atts[nbatts++] = attvalue;
[ ]  9571              /*
[ ]  9572               * tag if some deallocation is needed
[ ]  9573               */
[B]  9574              if (alloc != 0) attval = 1;
[B]  9575              attvalue = NULL; /* moved into atts */
[B]  9576          }
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
[B]  9606          if (atts[i+2] != NULL) {
[ ]  9607              /*
[ ]  9608               * Arithmetic on dangling pointers is technically undefined
[ ]  9609               * behavior, but well...
[ ]  9610               */
[L]  9611              const xmlChar *old = atts[i+2];
[L]  9612              atts[i+2]  = NULL;    /* Reset repurposed namespace URI */
[L]  9613              atts[i+3] = ctxt->input->base + (atts[i+3] - old);  /* value */
[L]  9614              atts[i+4] = ctxt->input->base + (atts[i+4] - old);  /* valuend */
[L]  9615          }
[B]  9616      }
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
[B]  9633  		if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
[ ]  9634  		    /*
[ ]  9635  		     * check that it's not a defined namespace
[ ]  9636  		     */
[L]  9637  		    for (j = 1;j <= nbNs;j++)
[ ]  9638  		        if (ctxt->nsTab[ctxt->nsNr - 2 * j] == NULL)
[ ]  9639  			    break;
[L]  9640  	            if (j <= nbNs) continue;
[ ]  9641  
[L]  9642  		    nsname = xmlGetNamespace(ctxt, NULL);
[L]  9643  		    if (nsname != defaults->values[5 * i + 2]) {
[L]  9644  			if (nsPush(ctxt, NULL,
[L]  9645  			           defaults->values[5 * i + 2]) > 0)
[L]  9646  			    nbNs++;
[L]  9647  		    }
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
[B]  9663  		} else {
[ ]  9664  		    /*
[ ]  9665  		     * check that it's not a defined attribute
[ ]  9666  		     */
[B]  9667  		    for (j = 0;j < nbatts;j+=5) {
[B]  9668  			if ((attname == atts[j]) && (aprefix == atts[j+1])) <-- BLOCKER
[W]  9669  			    break;
[B]  9670  		    }
[B]  9671  		    if (j < nbatts) continue;
[ ]  9672  
[B]  9673  		    if ((atts == NULL) || (nbatts + 5 > maxatts)) {
[B]  9674  			if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
[ ]  9675                              localname = NULL;
[ ]  9676                              goto done;
[ ]  9677  			}
[B]  9678  			maxatts = ctxt->maxatts;
[B]  9679  			atts = ctxt->atts;
[B]  9680  		    }
[B]  9681  		    atts[nbatts++] = attname;
[B]  9682  		    atts[nbatts++] = aprefix;
[B]  9683  		    if (aprefix == NULL)
[B]  9684  			atts[nbatts++] = NULL;
[B]  9685  		    else
[B]  9686  		        atts[nbatts++] = xmlGetNamespace(ctxt, aprefix);
[B]  9687  		    atts[nbatts++] = defaults->values[5 * i + 2];
[B]  9688  		    atts[nbatts++] = defaults->values[5 * i + 3];
[B]  9689  		    if ((ctxt->standalone == 1) &&
[B]  9690  		        (defaults->values[5 * i + 4] != NULL)) {
[ ]  9691  			xmlValidityError(ctxt, XML_DTD_STANDALONE_DEFAULTED,
[ ]  9692  	  "standalone: attribute %s on %s defaulted from external subset\n",
[ ]  9693  	                                 attname, localname);
[ ]  9694  		    }
[B]  9695  		    nbdef++;
[B]  9696  		}
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
[B]  9708  	if (atts[i + 1] != NULL) {
[B]  9709  	    nsname = xmlGetNamespace(ctxt, atts[i + 1]);
[B]  9710  	    if (nsname == NULL) {
[B]  9711  		xmlNsErr(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[B]  9712  		    "Namespace prefix %s for %s on %s is not defined\n",
[B]  9713  		    atts[i + 1], atts[i], localname);
[B]  9714  	    }
[B]  9715  	    atts[i + 2] = nsname;
[B]  9716  	} else
[B]  9717  	    nsname = NULL;
[ ]  9718  	/*
[ ]  9719  	 * [ WFC: Unique Att Spec ]
[ ]  9720  	 * No attribute name may appear more than once in the same
[ ]  9721  	 * start-tag or empty-element tag.
[ ]  9722  	 * As extended by the Namespace in XML REC.
[ ]  9723  	 */
[B]  9724          for (j = 0; j < i;j += 5) {
[B]  9725  	    if (atts[i] == atts[j]) {
[W]  9726  	        if (atts[i+1] == atts[j+1]) {
[ ]  9727  		    xmlErrAttributeDup(ctxt, atts[i+1], atts[i]);
[ ]  9728  		    break;
[ ]  9729  		}
[W]  9730  		if ((nsname != NULL) && (atts[j + 2] == nsname)) {
[ ]  9731  		    xmlNsErr(ctxt, XML_NS_ERR_ATTRIBUTE_REDEFINED,
[ ]  9732  			     "Namespaced Attribute %s in '%s' redefined\n",
[ ]  9733  			     atts[i], nsname, NULL);
[ ]  9734  		    break;
[ ]  9735  		}
[W]  9736  	    }
[B]  9737  	}
[B]  9738      }
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
[L]  9755  	    ctxt->sax->startElementNs(ctxt->userData, localname, prefix,
[L]  9756  			  nsname, nbNs, &ctxt->nsTab[ctxt->nsNr - 2 * nbNs],
[L]  9757  			  nbatts / 5, nbdef, atts);
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
[B]  9768  	for (i = 3,j = 0; j < nratts;i += 5,j++)
[B]  9769  	    if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))
[B]  9770  	        xmlFree((xmlChar *) atts[i]);
[B]  9771      }
[ ]  9772  
[B]  9773      return(localname);
[B]  9774  }

--- Caller (1 hop): parser.c:xmlParseTryOrFinish (/src/libxml2/parser.c:11404-12120, calls parser.c:xmlParseStartTag2 at line 11650) (±10 around call site) ---
[B] 11640                      goto done;
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
     437      1720  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     356      1360  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      87       302  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      28       204  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      43       157  parser.c:xmlGetNamespace  (/src/libxml2/parser.c:8856-8867)
      20       107  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
       1        77  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
      24        90  parser.c:xmlCleanSpecialAttrCallback  (/src/libxml2/parser.c:1335-1341)
      24        90  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
      20        86  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
      27        90  parser.c:xmlAddSpecialAttr  (/src/libxml2/parser.c:1308-1325)
      27        90  inputPop  (/src/libxml2/parser.c:1723-1738)
      27        90  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
      27        90  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)
      24        80  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203)
... (58 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=6  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=6   L7181  T=0 F=0  T=0 F=1  if (RAW != '&')
  d=6   L7187  T=0 F=0  T=0 F=1  if (NXT(1) == '#') {
  d=6   L7233  T=0 F=0  T=1 F=0  if (ent == NULL) return;
--- d=4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=4   L10816  T=0 F=3  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10816  T=0 F=3  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10829  T=3 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10829  T=3 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10831  T=0 F=3  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10834  T=3 F=0  T=10 F=0  if ((ctxt->encoding == NULL) &&
  d=4   L10835  T=3 F=0  T=10 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=4   L10846  T=0 F=3  T=10 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=4   L10852  T=0 F=3  T=0 F=10  if (CUR == 0) {
  d=4   L10863  T=0 F=3  T=0 F=10  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=4   L10872  T=0 F=0  T=0 F=10  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=4   L10873  T=0 F=0  T=0 F=10  (ctxt->instate == XML_PARSER_EOF)) {
  d=4   L10884  T=3 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=3 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=3 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10886  T=0 F=3  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10888  T=3 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10888  T=3 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10889  T=3 F=0  T=10 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10889  T=0 F=3  T=0 F=10  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10907  T=0 F=3  T=0 F=10  if (RAW == '[') {
  d=4   L10918  T=3 F=0  T=10 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10918  T=3 F=0  T=10 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10919  T=3 F=0  T=10 F=0  (!ctxt->disableSAX))
  d=4   L10922  T=0 F=3  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10936  T=0 F=3  T=0 F=10  if (RAW != '<') {
  d=4   L10950  T=0 F=3  T=3 F=7  if (RAW != 0) {
  d=4   L10959  T=3 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10959  T=3 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10965  T=3 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) &&
  d=4   L10966  T=0 F=3  T=0 F=10  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=4   L10971  T=0 F=3  T=1 F=9  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10971  T=0 F=0  T=1 F=0  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10973  T=0 F=0  T=1 F=0  if (ctxt->valid)
  d=4   L10975  T=0 F=0  T=0 F=1  if (ctxt->nsWellFormed)
  d=4   L10977  T=0 F=0  T=0 F=1  if (ctxt->options & XML_PARSE_OLD10)
  d=4   L10980  T=3 F=0  T=9 F=1  if (! ctxt->wellFormed) {
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9973  T=4 F=3  T=62 F=2  while ((RAW != 0) &&
  d=3   L9974  T=4 F=0  T=62 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L9980  T=3 F=1  T=29 F=33  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=0 F=3  T=0 F=29  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=3 F=1  T=29 F=33  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=0 F=3  T=0 F=29  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L10004  T=3 F=1  T=29 F=33  else if (*cur == '<') {
  d=3   L10005  T=0 F=3  T=16 F=13  if (NXT(1) == '/') {
  d=3   L10006  T=0 F=0  T=8 F=8  if (ctxt->nameNr <= nameNr)
  d=3   L10019  T=0 F=1  T=1 F=32  else if (*cur == '&') {
--- d=3  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=3   L10077  T=0 F=3  T=0 F=10  if (xmlParseElementStart(ctxt) != 0)
  d=3   L10081  T=0 F=3  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L10084  T=3 F=0  T=2 F=8  if (CUR == 0) {
--- d=3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=3   L12139  T=0 F=13  T=0 F=36  if (ctxt == NULL)
  d=3   L12141  T=0 F=1  T=4 F=12  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12141  T=1 F=12  T=16 F=20  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12143  T=0 F=13  T=0 F=32  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L12145  T=0 F=13  T=0 F=32  if (ctxt->input == NULL)
  d=3   L12149  T=6 F=7  T=20 F=12  if (ctxt->instate == XML_PARSER_START)
  d=3   L12151  T=6 F=0  T=20 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12151  T=6 F=7  T=20 F=12  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12151  T=6 F=0  T=20 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12152  T=0 F=6  T=0 F=20  (chunk[size - 1] == '\r')) {
  d=3   L12159  T=6 F=0  T=20 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12159  T=6 F=0  T=20 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12159  T=6 F=7  T=20 F=12  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12160  T=6 F=0  T=20 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=3   L12160  T=6 F=0  T=20 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=3   L12170  T=6 F=0  T=20 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12170  T=6 F=0  T=20 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12171  T=6 F=0  T=20 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12171  T=0 F=6  T=0 F=20  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12202  T=0 F=6  T=0 F=20  if (res < 0) {
  d=3   L12233  T=0 F=13  T=0 F=32  if (remain != 0) {
  d=3   L12238  T=0 F=13  T=4 F=28  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L12241  T=13 F=0  T=28 F=0  if ((ctxt->input != NULL) &&
  d=3   L12242  T=0 F=13  T=0 F=28  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=3   L12243  T=0 F=13  T=0 F=28  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=3   L12248  T=2 F=5  T=8 F=20  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12248  T=7 F=6  T=28 F=0  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12284  T=3 F=0  T=1 F=4  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=3   L12287  T=0 F=0  T=0 F=4  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=3   L12287  T=0 F=3  T=4 F=1  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
--- d=2  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226) ---
  d=2   L10115  T=0 F=6  T=0 F=23  if (((unsigned int) ctxt->nameNr > xmlParserMaxDepth) &&
  d=2   L10125  T=0 F=6  T=0 F=23  if (ctxt->record_info) {
  d=2   L10131  T=0 F=6  T=0 F=23  if (ctxt->spaceNr == 0)
  d=2   L10133  T=0 F=6  T=0 F=23  else if (*ctxt->space == -2)
  d=2   L10140  T=6 F=0  T=23 F=0  if (ctxt->sax2)
  d=2   L10147  T=0 F=6  T=0 F=23  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L10149  T=0 F=6  T=2 F=21  if (name == NULL) {
  d=2   L10162  T=0 F=0  T=6 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L10162  T=0 F=0  T=6 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L10162  T=0 F=6  T=6 F=15  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L10163  T=0 F=0  T=6 F=0  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=2   L10163  T=0 F=0  T=0 F=6  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=2   L10170  T=0 F=6  T=0 F=21  if ((RAW == '/') && (NXT(1) == '>')) {
  d=2   L10196  T=3 F=3  T=18 F=3  if (RAW == '>') {
--- d=2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=2   L11409  T=0 F=13  T=0 F=32  if (ctxt->input == NULL)
  d=2   L11465  T=13 F=0  T=32 F=0  if ((ctxt->input != NULL) &&
  d=2   L11466  T=0 F=13  T=0 F=32  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=2   L11470  T=60 F=0  T=243 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=2   L11471  T=2 F=12  T=8 F=127  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L11471  T=14 F=46  T=135 F=108  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L11474  T=0 F=58  T=0 F=235  if (ctxt->input == NULL) break;
  d=2   L11475  T=0 F=58  T=0 F=235  if (ctxt->input->buf == NULL)
  d=2   L11486  T=46 F=12  T=205 F=30  if ((ctxt->instate != XML_PARSER_START) &&
  d=2   L11487  T=0 F=46  T=0 F=205  (ctxt->input->buf->raw != NULL) &&
  d=2   L11500  T=1 F=57  T=6 F=229  if (avail < 1)
  d=2   L11502  T=0 F=57  T=0 F=229  switch (ctxt->instate) {
  d=2   L11503  T=0 F=57  T=0 F=229  case XML_PARSER_EOF:
  d=2   L11508  T=12 F=45  T=30 F=199  case XML_PARSER_START:
  d=2   L11509  T=6 F=6  T=10 F=20  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=2   L11535  T=0 F=6  T=0 F=20  if (avail < 2)
  d=2   L11539  T=0 F=6  T=0 F=20  if (cur == 0) {
  d=2   L11553  T=6 F=0  T=20 F=0  if ((cur == '<') && (next == '?')) {
  d=2   L11553  T=6 F=0  T=20 F=0  if ((cur == '<') && (next == '?')) {
  d=2   L11555  T=0 F=6  T=0 F=20  if (avail < 5) goto done;
  d=2   L11556  T=6 F=0  T=20 F=0  if ((!terminate) &&
  d=2   L11557  T=0 F=6  T=0 F=20  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=2   L11559  T=6 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11559  T=6 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11562  T=0 F=6  T=20 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=2   L11563  T=0 F=0  T=20 F=0  (ctxt->input->cur[3] == 'm') &&
  d=2   L11564  T=0 F=0  T=20 F=0  (ctxt->input->cur[4] == 'l') &&
  d=2   L11572  T=0 F=0  T=0 F=20  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=2   L11581  T=0 F=0  T=20 F=0  if ((ctxt->encoding == NULL) &&
  d=2   L11582  T=0 F=0  T=0 F=20  (ctxt->input->encoding != NULL))
  d=2   L11584  T=0 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11584  T=0 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11585  T=0 F=0  T=20 F=0  (!ctxt->disableSAX))
  d=2   L11594  T=6 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11594  T=6 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11595  T=6 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=2   L11622  T=19 F=38  T=42 F=187  case XML_PARSER_START_TAG: {
  d=2   L11629  T=0 F=19  T=0 F=42  if ((avail < 2) && (ctxt->inputNr == 1))
  d=2   L11632  T=0 F=19  T=0 F=42  if (cur != '<') {
  d=2   L11639  T=8 F=6  T=6 F=32  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11639  T=14 F=5  T=38 F=4  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11641  T=0 F=11  T=0 F=36  if (ctxt->spaceNr == 0)
  d=2   L11643  T=0 F=11  T=0 F=36  else if (*ctxt->space == -2)
  d=2   L11648  T=11 F=0  T=36 F=0  if (ctxt->sax2)
  d=2   L11655  T=0 F=11  T=0 F=36  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11657  T=0 F=11  T=4 F=32  if (name == NULL) {
  d=2   L11660  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L11660  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L11670  T=0 F=0  T=12 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L11670  T=0 F=0  T=12 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L11670  T=0 F=11  T=12 F=20  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L11671  T=0 F=0  T=0 F=12  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=2   L11671  T=0 F=0  T=12 F=0  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=2   L11678  T=0 F=11  T=0 F=32  if ((RAW == '/') && (NXT(1) == '>')) {
  d=2   L11707  T=6 F=5  T=28 F=4  if (RAW == '>') {
  d=2   L11721  T=8 F=49  T=91 F=138  case XML_PARSER_CONTENT: {
  d=2   L11722  T=2 F=6  T=0 F=91  if ((avail < 2) && (ctxt->inputNr == 1))
  d=2   L11722  T=2 F=0  T=0 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=2   L11727  T=0 F=6  T=24 F=20  if ((cur == '<') && (next == '/')) {
  d=2   L11727  T=6 F=0  T=44 F=47  if ((cur == '<') && (next == '/')) {
  d=2   L11730  T=0 F=6  T=0 F=20  } else if ((cur == '<') && (next == '?')) {
  d=2   L11730  T=6 F=0  T=20 F=47  } else if ((cur == '<') && (next == '?')) {
  d=2   L11736  T=6 F=0  T=20 F=0  } else if ((cur == '<') && (next != '!')) {
  d=2   L11736  T=6 F=0  T=20 F=47  } else if ((cur == '<') && (next != '!')) {
  d=2   L11739  T=0 F=0  T=0 F=47  } else if ((cur == '<') && (next == '!') &&
  d=2   L11747  T=0 F=0  T=0 F=47  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=2   L11758  T=0 F=0  T=0 F=47  } else if ((cur == '<') && (next == '!') &&
  d=2   L11761  T=0 F=0  T=0 F=47  } else if (cur == '<') {
  d=2   L11765  T=0 F=0  T=0 F=47  } else if (cur == '&') {
  d=2   L11782  T=0 F=0  T=47 F=0  if ((ctxt->inputNr == 1) &&
  d=2   L11783  T=0 F=0  T=47 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=2   L11784  T=0 F=0  T=2 F=44  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=2   L11784  T=0 F=0  T=46 F=1  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=2   L11792  T=0 F=57  T=24 F=205  case XML_PARSER_END_TAG:
  d=2   L11793  T=0 F=0  T=0 F=24  if (avail < 2)
  d=2   L11795  T=0 F=0  T=0 F=24  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=2   L11795  T=0 F=0  T=24 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=2   L11797  T=0 F=0  T=24 F=0  if (ctxt->sax2) {
  d=2   L11805  T=0 F=0  T=0 F=24  if (ctxt->instate == XML_PARSER_EOF) {
  d=2   L11807  T=0 F=0  T=8 F=16  } else if (ctxt->nameNr == 0) {
  d=2   L11813  T=0 F=57  T=0 F=229  case XML_PARSER_CDATA_SECTION: {
  d=2   L11904  T=12 F=45  T=20 F=209  case XML_PARSER_MISC:
  d=2   L11905  T=6 F=51  T=16 F=213  case XML_PARSER_PROLOG:
  d=2   L11906  T=0 F=57  T=6 F=223  case XML_PARSER_EPILOG:
  d=2   L11908  T=0 F=18  T=0 F=42  if (ctxt->input->buf == NULL)
  d=2   L11914  T=0 F=18  T=6 F=36  if (avail < 2)
  d=2   L11918  T=18 F=0  T=36 F=0  if ((cur == '<') && (next == '?')) {
  d=2   L11918  T=6 F=12  T=0 F=36  if ((cur == '<') && (next == '?')) {
  d=2   L11919  T=6 F=0  T=0 F=0  if ((!terminate) &&
  d=2   L11920  T=0 F=6  T=0 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=2   L11927  T=0 F=6  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11929  T=6 F=6  T=20 F=16  } else if ((cur == '<') && (next == '!') &&
  d=2   L11929  T=12 F=0  T=36 F=0  } else if ((cur == '<') && (next == '!') &&
  d=2   L11930  T=0 F=6  T=0 F=20  (ctxt->input->cur[2] == '-') &&
  d=2   L11942  T=6 F=6  T=20 F=16  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=2   L11943  T=6 F=0  T=20 F=0  (cur == '<') && (next == '!') &&
  d=2   L11943  T=6 F=0  T=20 F=0  (cur == '<') && (next == '!') &&
  d=2   L11944  T=6 F=0  T=20 F=0  (ctxt->input->cur[2] == 'D') &&
  d=2   L11945  T=6 F=0  T=20 F=0  (ctxt->input->cur[3] == 'O') &&
  d=2   L11946  T=6 F=0  T=20 F=0  (ctxt->input->cur[4] == 'C') &&
  d=2   L11947  T=6 F=0  T=20 F=0  (ctxt->input->cur[5] == 'T') &&
  d=2   L11948  T=6 F=0  T=20 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=2   L11949  T=6 F=0  T=20 F=0  (ctxt->input->cur[7] == 'P') &&
  d=2   L11950  T=6 F=0  T=20 F=0  (ctxt->input->cur[8] == 'E')) {
  d=2   L11951  T=6 F=0  T=20 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11951  T=0 F=6  T=0 F=20  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11959  T=0 F=6  T=0 F=20  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11961  T=0 F=6  T=0 F=20  if (RAW == '[') {
  d=2   L11972  T=6 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L11972  T=6 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L11973  T=6 F=0  T=20 F=0  (ctxt->sax->externalSubset != NULL))
  d=2   L11985  T=0 F=6  T=0 F=16  } else if ((cur == '<') && (next == '!') &&
  d=2   L11985  T=6 F=0  T=16 F=0  } else if ((cur == '<') && (next == '!') &&
  d=2   L11989  T=0 F=6  T=0 F=16  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=2   L12007  T=0 F=57  T=0 F=229  case XML_PARSER_DTD: {
  d=2   L12029  T=0 F=57  T=0 F=229  case XML_PARSER_COMMENT:
  d=2   L12038  T=0 F=57  T=0 F=229  case XML_PARSER_IGNORE:
  d=2   L12047  T=0 F=57  T=0 F=229  case XML_PARSER_PI:
  d=2   L12056  T=0 F=57  T=0 F=229  case XML_PARSER_ENTITY_DECL:
  d=2   L12065  T=0 F=57  T=0 F=229  case XML_PARSER_ENTITY_VALUE:
  d=2   L12074  T=0 F=57  T=0 F=229  case XML_PARSER_ATTRIBUTE_VALUE:
  d=2   L12083  T=0 F=57  T=0 F=229  case XML_PARSER_SYSTEM_LITERAL:
  d=2   L12092  T=0 F=57  T=0 F=229  case XML_PARSER_PUBLIC_LITERAL:
--- d=1  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774) ---
  d=1   L9369  T=0 F=17  T=0 F=59  if (RAW != '<') return(NULL);
  d=1   L9391  T=0 F=17  T=6 F=53  if (localname == NULL) {
  d=1   L9406  T=8 F=9  T=27 F=26  while (((RAW != '>') &&
  d=1   L9407  T=8 F=0  T=27 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=1   L9408  T=3 F=0  T=27 F=0  (IS_BYTE_CHAR(RAW))) && (ctxt->instate != XML_PARSER_EOF)) {
  d=1   L9413  T=0 F=3  T=3 F=24  if (attname == NULL) {
  d=1   L9418  T=0 F=3  T=4 F=20  if (attvalue == NULL)
  d=1   L9420  T=0 F=3  T=0 F=20  if (len < 0) len = xmlStrlen(attvalue);
  d=1   L9422  T=0 F=3  T=0 F=20  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
  d=1   L9475  T=0 F=3  T=0 F=20  } else if (aprefix == ctxt->str_xmlns) {
  d=1   L9548  T=0 F=0  T=0 F=3  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9548  T=3 F=0  T=17 F=3  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9549  T=0 F=3  T=0 F=17  if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
  d=1   L9564  T=3 F=0  T=1 F=19  if (alloc)
  d=1   L9574  T=3 F=0  T=1 F=19  if (alloc != 0) attval = 1;
  d=1   L9579  T=0 F=3  T=0 F=24  if ((attvalue != NULL) && (alloc != 0)) {
  d=1   L9585  T=0 F=3  T=0 F=24  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L9587  T=0 F=3  T=20 F=4  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=1   L9597  T=0 F=17  T=0 F=53  if (ctxt->input->id != inputid) {
  d=1   L9605  T=3 F=17  T=20 F=53  for (i = 0, j = 0; j < nratts; i += 5, j++) {
  d=1   L9606  T=0 F=3  T=19 F=1  if (atts[i+2] != NULL) {
  d=1   L9621  T=17 F=0  T=53 F=0  if (ctxt->attsDefault != NULL) {
  d=1   L9625  T=8 F=9  T=27 F=26  if (defaults != NULL) {
  d=1   L9626  T=19 F=8  T=54 F=27  for (i = 0;i < defaults->nbAttrs;i++) {
  d=1   L9633  T=0 F=0  T=6 F=0  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
  d=1   L9633  T=0 F=19  T=6 F=48  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
  d=1   L9637  T=0 F=0  T=0 F=6  for (j = 1;j <= nbNs;j++)
  d=1   L9640  T=0 F=0  T=0 F=6  if (j <= nbNs) continue;
  d=1   L9643  T=0 F=0  T=3 F=3  if (nsname != defaults->values[5 * i + 2]) {
  d=1   L9644  T=0 F=0  T=3 F=0  if (nsPush(ctxt, NULL,
  d=1   L9648  T=0 F=19  T=10 F=38  } else if (aprefix == ctxt->str_xmlns) {
  d=1   L9652  T=0 F=0  T=0 F=10  for (j = 1;j <= nbNs;j++)
  d=1   L9655  T=0 F=0  T=0 F=10  if (j <= nbNs) continue;
  d=1   L9658  T=0 F=0  T=10 F=0  if (nsname != defaults->values[5 * i + 2]) {
  d=1   L9659  T=0 F=0  T=10 F=0  if (nsPush(ctxt, attname,
  d=1   L9667  T=17 F=16  T=38 F=38  for (j = 0;j < nbatts;j+=5) {
  d=1   L9668  T=3 F=5  T=0 F=0  if ((attname == atts[j]) && (aprefix == atts[j+1]))  <-- BLOCKER
  d=1   L9668  T=8 F=9  T=0 F=38  if ((attname == atts[j]) && (aprefix == atts[j+1]))  <-- BLOCKER
  d=1   L9671  T=3 F=16  T=0 F=38  if (j < nbatts) continue;
  d=1   L9673  T=0 F=11  T=0 F=31  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9673  T=5 F=11  T=7 F=31  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9683  T=3 F=13  T=4 F=34  if (aprefix == NULL)
  d=1   L9689  T=0 F=16  T=0 F=38  if ((ctxt->standalone == 1) &&
  d=1   L9704  T=19 F=17  T=58 F=53  for (i = 0; i < nbatts;i += 5) {
  d=1   L9708  T=13 F=6  T=54 F=4  if (atts[i + 1] != NULL) {
  d=1   L9710  T=10 F=3  T=38 F=16  if (nsname == NULL) {
  d=1   L9724  T=14 F=19  T=38 F=58  for (j = 0; j < i;j += 5) {
  d=1   L9725  T=5 F=9  T=0 F=38  if (atts[i] == atts[j]) {
  d=1   L9726  T=0 F=5  T=0 F=0  if (atts[i+1] == atts[j+1]) {
  d=1   L9730  T=0 F=5  T=0 F=0  if ((nsname != NULL) && (atts[j + 2] == nsname)) {
  d=1   L9741  T=0 F=17  T=0 F=53  if ((prefix != NULL) && (nsname == NULL)) {
  d=1   L9752  T=17 F=0  T=53 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=1   L9752  T=17 F=0  T=53 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=1   L9753  T=14 F=3  T=48 F=5  (!ctxt->disableSAX)) {
  d=1   L9754  T=0 F=14  T=12 F=36  if (nbNs > 0)
  d=1   L9767  T=3 F=14  T=1 F=52  if (attval != 0) {
  d=1   L9768  T=3 F=3  T=1 F=1  for (i = 3,j = 0; j < nratts;i += 5,j++)
  d=1   L9769  T=3 F=0  T=1 F=0  if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))
  d=1   L9769  T=3 F=0  T=1 F=0  if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))

[off-chain: 762 additional divergent branches across 80 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=75a0e7d3edec39d2, size=177 bytes, fuzzer=grimoire, trial=1, discovered_at=6311s, mutation_op=BytesExpandMutator):
  0000: 06 31 32 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   .12l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 3c 61 3e 3c 62 20 66 3d 22 5c 0a 64 74 64 73 2f   <a><b f="\.dtds/
Seed 2 (id=4746ff87ec78aeda, size=817 bytes, fuzzer=grimoire, trial=1, discovered_at=12169s, mutation_op=GrimoireRecursiveReplacementMutator,GrimoireRecursiveReplacementMutator,GrimoireRecursiveReplacementMutator):
  0000: 07 c0 ff ff 6c 00 32 6c 5c 0a 3c 3f 6c 3f 3e 3c   ....l.2l\.<?l?><
  0010: 21 44 4f 43 54 59 50 45 3a 20 53 59 53 54 45 4d   !DOCTYPE: SYSTEM
  0020: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
  0030: 64 22 3e 3c 61 3e 3c 62 5c 0a 64 74 64 73 2f 31   d"><a><b\.dtds/1
Seed 3 (id=a462c8eb848bc293, size=1443 bytes, fuzzer=grimoire, trial=1, discovered_at=20635s, mutation_op=DwordAddMutator,CrossoverInsertMutator):
  0000: 27 68 74 74 70 3a 2f 2f 28 28 28 28 28 28 28 28   'http://((((((((
  0010: 28 28 49 53 4f 28 38 38 35 39 2d 67 68 28 38 38   ((ISO(8859-gh(88
  0020: 35 39 2d 67 68 74 4f 28 38 38 35 39 2d 27 68 74   59-ghtO(8859-'ht
  0030: 74 70 3a 2f 2f 40 69 6e 6b 23 27 68 74 3a 70 3a   tp://@ink#'ht:p:

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=5f83308a4d472d74, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=10s, mutation_op=ByteRandMutator,ByteDecMutator,ByteInterestingMutator,ByteRandMutator,BytesSwapMutator,ByteAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=a56971c1aae49fd3, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=271s, mutation_op=ByteDecMutator,ByteIncMutator,DwordAddMutator,DwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=3f82a3daf8d36108, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3471s, mutation_op=BytesDeleteMutator,BytesSetMutator):
  0000: fa 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=2ac607b713951007, size=384 bytes, fuzzer=cmplog, trial=1, discovered_at=4789s, mutation_op=BytesRandInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=46f8f4fb7afd3e70, size=378 bytes, fuzzer=cmplog, trial=1, discovered_at=8257s, mutation_op=CrossoverInsertMutator,QwordAddMutator):
  0000: 06 00 eb ff 30 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....027772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x1 07(.)x1 27(')x1             06(.)x4 2b(+)x2 f9(.)x2 fa(.)x1 +1u  PARTIAL
   0x0001  31(1)x1 c0(.)x1 68(h)x1             00(.)x10                            DIFFER
   0x0002  32(2)x1 ff(.)x1 74(t)x1             00(.)x7 eb(.)x1 ff(.)x1 37(7)x1     PARTIAL
   0x0003  6c(l)x1 ff(.)x1 74(t)x1             00(.)x8 ff(.)x1 37(7)x1             PARTIAL
   0x0004  5c(\)x1 6c(l)x1 70(p)x1             31(1)x8 30(0)x1 37(7)x1             DIFFER
   0x0005  0a(.)x1 00(.)x1 3a(:)x1             32(2)x10                            DIFFER
   0x0006  3c(<)x1 32(2)x1 2f(/)x1             37(7)x9 2e(.)x1                     DIFFER
   0x0007  3f(?)x1 6c(l)x1 2f(/)x1             37(7)x9 78(x)x1                     DIFFER
   0x0008  6c(l)x1 5c(\)x1 28(()x1             37(7)x9 6d(m)x1                     DIFFER
   0x0009  20( )x1 0a(.)x1 28(()x1             32(2)x9 6c(l)x1                     DIFFER
   0x000a  3f(?)x1 3c(<)x1 28(()x1             2e(.)x9 5c(\)x1                     DIFFER
   0x000b  3e(>)x1 3f(?)x1 28(()x1             78(x)x9 0a(.)x1                     DIFFER
   0x000c  3c(<)x1 6c(l)x1 28(()x1             6d(m)x9 3c(<)x1                     PARTIAL
   0x000d  21(!)x1 3f(?)x1 28(()x1             6c(l)x9 3f(?)x1                     PARTIAL
   0x000e  44(D)x1 3e(>)x1 28(()x1             5c(\)x9 78(x)x1                     DIFFER
   0x000f  4f(O)x1 3c(<)x1 28(()x1             0a(.)x9 6d(m)x1                     DIFFER
   0x0010  43(C)x1 21(!)x1 28(()x1             3c(<)x9 6c(l)x1                     DIFFER
   0x0011  54(T)x1 44(D)x1 28(()x1             3f(?)x9 20( )x1                     DIFFER
   0x0012  59(Y)x1 4f(O)x1 49(I)x1             78(x)x9 76(v)x1                     DIFFER
   0x0013  50(P)x1 43(C)x1 53(S)x1             6d(m)x9 65(e)x1                     DIFFER
   0x0014  45(E)x1 54(T)x1 4f(O)x1             6c(l)x9 72(r)x1                     DIFFER
   0x0015  61(a)x1 59(Y)x1 28(()x1             20( )x9 73(s)x1                     DIFFER
   0x0016  20( )x1 50(P)x1 38(8)x1             76(v)x9 69(i)x1                     DIFFER
   0x0017  53(S)x1 45(E)x1 38(8)x1             65(e)x9 6f(o)x1                     DIFFER
   0x0018  59(Y)x1 3a(:)x1 35(5)x1             72(r)x9 6e(n)x1                     DIFFER
   0x0019  53(S)x1 20( )x1 39(9)x1             73(s)x9 3d(=)x1                     DIFFER
   0x001a  54(T)x1 53(S)x1 2d(-)x1             69(i)x9 22(")x1                     DIFFER
   0x001b  45(E)x1 59(Y)x1 67(g)x1             6f(o)x9 31(1)x1                     DIFFER
   0x001c  4d(M)x1 53(S)x1 68(h)x1             6e(n)x9 2e(.)x1                     DIFFER
   0x001d  20( )x1 54(T)x1 28(()x1             3d(=)x9 30(0)x1                     DIFFER
   0x001e  22(")x1 45(E)x1 38(8)x1             22(")x10                            PARTIAL
   0x001f  64(d)x1 4d(M)x1 38(8)x1             31(1)x9 3f(?)x1                     DIFFER
   0x0020  74(t)x1 20( )x1 35(5)x1             2e(.)x9 3e(>)x1                     DIFFER
   0x0021  64(d)x1 22(")x1 39(9)x1             30(0)x9 0a(.)x1                     DIFFER
   0x0022  73(s)x1 64(d)x1 2d(-)x1             22(")x9 3c(<)x1                     DIFFER
   0x0023  2f(/)x1 74(t)x1 67(g)x1             3f(?)x9 21(!)x1                     DIFFER
   0x0024  31(1)x1 64(d)x1 68(h)x1             3e(>)x9 44(D)x1                     DIFFER
   0x0025  32(2)x1 73(s)x1 74(t)x1             0a(.)x9 4f(O)x1                     DIFFER
   0x0026  37(7)x1 2f(/)x1 4f(O)x1             3c(<)x9 43(C)x1                     DIFFER
   0x0027  37(7)x1 31(1)x1 28(()x1             21(!)x9 54(T)x1                     DIFFER
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

--- grimoire ---
**Baseline relationship**: grimoire builds on the full cmplog stack —
it includes the `CmpLogObserver`, the `TracingStage`, and the
`I2SRandReplace` (i2s) stage — and ADDS a `GeneralizationStage` plus
Grimoire structural mutators. The single-technique delta is therefore
`grimoire` vs `cmplog` (both have I2S; grimoire adds generalization +
Grimoire mutators), not vs naive.

**Instrumentation**: cmplog's edge counters + per-execution CMP buffer
(`CmpLogObserver`).

**Feedback**: edge-bucket `MaxMapFeedback`.

**Mutators / stages**: stages are
`[generalization, tracing, i2s, havoc, grimoire]`. `GeneralizationStage`
replaces concrete byte runs in a corpus entry with `<GAP>` placeholders
(a generalised input) by repeatedly re-executing and checking that
coverage is preserved. The Grimoire mutators —
`GrimoireExtensionMutator`, `GrimoireRecursiveReplacementMutator`,
`GrimoireStringReplacementMutator`, `GrimoireRandomDeleteMutator` —
splice and recurse on these generalised token/gap structures
(string-based, grammar-free structural mutation). `I2SRandReplace` (the
cmplog i2s stage) also runs.

**Observed `mutation_op` in seed metadata**: all grimoire stages (i2s,
havoc, grimoire) are wrapped in `LineageMutatorWrap` with **no
per-operator name list**, so grimoire seeds appear nameless in lineage
(`mutation_op = -`). As with mopt, nameless rows are NOT an
I2S-exclusive signal here — and grimoire genuinely runs I2S too, so the
two are not separable from lineage names.

**Per-execution cost**: cmplog's per-CMP cost, plus extra executions
during generalization (each candidate gap is validated by a re-run).

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6743.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6743,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6743 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6743 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6743 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).