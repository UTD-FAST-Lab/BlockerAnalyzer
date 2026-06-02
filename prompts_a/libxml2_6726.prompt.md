==== BLOCKER ====
Target: libxml2
Branch ID: 6726
Location: /src/libxml2/parser.c:9422:13
Enclosing function: parser.c:xmlParseStartTag2
Source line:         if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
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
fast                             1        9          0  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=15.80h  loser=23.60h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.80  dur_div=7.80h  hit_div=5
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6726/{W,L}/branch_coverage_show.txt

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
[B]  9392  	xmlFatalErrMsg(ctxt, XML_ERR_NAME_REQUIRED,
[B]  9393  		       "StartTag: invalid element name\n");
[B]  9394          return(NULL);
[B]  9395      }
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
[B]  9419              goto next_attr;
[B]  9420  	if (len < 0) len = xmlStrlen(attvalue);
[ ]  9421  
[B]  9422          if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) { <-- BLOCKER
[W]  9423              const xmlChar *URL = xmlDictLookup(ctxt->dict, attvalue, len);
[W]  9424              xmlURIPtr uri;
[ ]  9425  
[W]  9426              if (URL == NULL) {
[ ]  9427                  xmlErrMemory(ctxt, "dictionary allocation failure");
[ ]  9428                  if ((attvalue != NULL) && (alloc != 0))
[ ]  9429                      xmlFree(attvalue);
[ ]  9430                  localname = NULL;
[ ]  9431                  goto done;
[ ]  9432              }
[W]  9433              if (*URL != 0) {
[W]  9434                  uri = xmlParseURI((const char *) URL);
[W]  9435                  if (uri == NULL) {
[W]  9436                      xmlNsErr(ctxt, XML_WAR_NS_URI,
[W]  9437                               "xmlns: '%s' is not a valid URI\n",
[W]  9438                                         URL, NULL, NULL);
[W]  9439                  } else {
[ ]  9440                      if (uri->scheme == NULL) {
[ ]  9441                          xmlNsWarn(ctxt, XML_WAR_NS_URI_RELATIVE,
[ ]  9442                                    "xmlns: URI %s is not absolute\n",
[ ]  9443                                    URL, NULL, NULL);
[ ]  9444                      }
[ ]  9445                      xmlFreeURI(uri);
[ ]  9446                  }
[W]  9447                  if (URL == ctxt->str_xml_ns) {
[ ]  9448                      if (attname != ctxt->str_xml) {
[ ]  9449                          xmlNsErr(ctxt, XML_NS_ERR_XML_NAMESPACE,
[ ]  9450                       "xml namespace URI cannot be the default namespace\n",
[ ]  9451                                   NULL, NULL, NULL);
[ ]  9452                      }
[ ]  9453                      goto next_attr;
[ ]  9454                  }
[W]  9455                  if ((len == 29) &&
[W]  9456                      (xmlStrEqual(URL,
[ ]  9457                               BAD_CAST "http://www.w3.org/2000/xmlns/"))) {
[ ]  9458                      xmlNsErr(ctxt, XML_NS_ERR_XML_NAMESPACE,
[ ]  9459                           "reuse of the xmlns namespace name is forbidden\n",
[ ]  9460                               NULL, NULL, NULL);
[ ]  9461                      goto next_attr;
[ ]  9462                  }
[W]  9463              }
[ ]  9464              /*
[ ]  9465               * check that it's not a defined namespace
[ ]  9466               */
[W]  9467              for (j = 1;j <= nbNs;j++)
[ ]  9468                  if (ctxt->nsTab[ctxt->nsNr - 2 * j] == NULL)
[ ]  9469                      break;
[W]  9470              if (j <= nbNs)
[ ]  9471                  xmlErrAttributeDup(ctxt, NULL, attname);
[W]  9472              else
[W]  9473                  if (nsPush(ctxt, NULL, URL) > 0) nbNs++;
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
[L]  9565                  atts[nbatts++] = NULL;
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
[B]  9588  	    break;
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
[L]  9622          xmlDefAttrsPtr defaults;
[ ]  9623  
[L]  9624  	defaults = xmlHashLookup2(ctxt->attsDefault, localname, prefix);
[L]  9625  	if (defaults != NULL) {
[L]  9626  	    for (i = 0;i < defaults->nbAttrs;i++) {
[L]  9627  	        attname = defaults->values[5 * i];
[L]  9628  		aprefix = defaults->values[5 * i + 1];
[ ]  9629  
[ ]  9630                  /*
[ ]  9631  		 * special work for namespaces defaulted defs
[ ]  9632  		 */
[L]  9633  		if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
[ ]  9634  		    /*
[ ]  9635  		     * check that it's not a defined namespace
[ ]  9636  		     */
[ ]  9637  		    for (j = 1;j <= nbNs;j++)
[ ]  9638  		        if (ctxt->nsTab[ctxt->nsNr - 2 * j] == NULL)
[ ]  9639  			    break;
[ ]  9640  	            if (j <= nbNs) continue;
[ ]  9641  
[ ]  9642  		    nsname = xmlGetNamespace(ctxt, NULL);
[ ]  9643  		    if (nsname != defaults->values[5 * i + 2]) {
[ ]  9644  			if (nsPush(ctxt, NULL,
[ ]  9645  			           defaults->values[5 * i + 2]) > 0)
[ ]  9646  			    nbNs++;
[ ]  9647  		    }
[L]  9648  		} else if (aprefix == ctxt->str_xmlns) {
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
[L]  9697  	    }
[L]  9698  	}
[L]  9699      }
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
[L]  9711  		xmlNsErr(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[L]  9712  		    "Namespace prefix %s for %s on %s is not defined\n",
[L]  9713  		    atts[i + 1], atts[i], localname);
[L]  9714  	    }
[L]  9715  	    atts[i + 2] = nsname;
[L]  9716  	} else
[L]  9717  	    nsname = NULL;
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
[L]  9768  	for (i = 3,j = 0; j < nratts;i += 5,j++)
[L]  9769  	    if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))
[L]  9770  	        xmlFree((xmlChar *) atts[i]);
[L]  9771      }
[ ]  9772  
[B]  9773      return(localname);
[B]  9774  }

--- Caller (1 hop): parser.c:xmlParseTryOrFinish (/src/libxml2/parser.c:11404-12120, calls parser.c:xmlParseStartTag2 at line 11650) (±10 around call site) ---
[B] 11640                      goto done;
[B] 11641  		if (ctxt->spaceNr == 0)
[ ] 11642  		    spacePush(ctxt, -1);
[B] 11643  		else if (*ctxt->space == -2)
[L] 11644  		    spacePush(ctxt, -1);
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
[B] 11658  		    spacePop(ctxt);
[B] 11659  		    xmlHaltParser(ctxt);
[B] 11660  		    if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))

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
     276      6030  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      28      1650  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      48      1440  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      18       456  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      18       367  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
       9       320  parser.c:xmlGetNamespace  (/src/libxml2/parser.c:8856-8867)
      16       284  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
       9       270  inputPop  (/src/libxml2/parser.c:1723-1738)
      12       251  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
      12       251  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774)  <-- enclosing
       9       220  parser.c:nameNsPush  (/src/libxml2/parser.c:1820-1860)
       3       212  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       9       186  nodePush  (/src/libxml2/parser.c:1750-1776)
       8       176  parser.c:xmlParseLookupGt  (/src/libxml2/parser.c:11194-11221)
       9       158  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
... (77 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=6  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=6   L7181  T=0 F=0  T=0 F=17  if (RAW != '&')
  d=6   L7187  T=0 F=0  T=0 F=17  if (NXT(1) == '#') {
  d=6   L7233  T=0 F=0  T=17 F=0  if (ent == NULL) return;
--- d=4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=4   L10816  T=0 F=1  T=0 F=30  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10816  T=0 F=1  T=0 F=30  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10829  T=1 F=0  T=30 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10829  T=1 F=0  T=30 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10831  T=0 F=1  T=0 F=30  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10834  T=1 F=0  T=30 F=0  if ((ctxt->encoding == NULL) &&
  d=4   L10835  T=1 F=0  T=30 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=4   L10846  T=0 F=1  T=27 F=3  if (enc != XML_CHAR_ENCODING_NONE) {
  d=4   L10852  T=0 F=1  T=0 F=30  if (CUR == 0) {
  d=4   L10863  T=0 F=1  T=0 F=30  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=4   L10872  T=0 F=0  T=0 F=27  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=4   L10873  T=0 F=0  T=0 F=27  (ctxt->instate == XML_PARSER_EOF)) {
  d=4   L10884  T=1 F=0  T=30 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=1 F=0  T=29 F=1  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=1 F=0  T=30 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10886  T=0 F=1  T=0 F=30  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10888  T=1 F=0  T=29 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10888  T=1 F=0  T=29 F=1  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10889  T=1 F=0  T=29 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10889  T=0 F=1  T=0 F=29  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10907  T=0 F=0  T=0 F=25  if (RAW == '[') {
  d=4   L10918  T=0 F=0  T=25 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10918  T=0 F=0  T=25 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10919  T=0 F=0  T=24 F=1  (!ctxt->disableSAX))
  d=4   L10922  T=0 F=0  T=0 F=25  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10936  T=0 F=1  T=0 F=30  if (RAW != '<') {
  d=4   L10950  T=0 F=1  T=7 F=23  if (RAW != 0) {
  d=4   L10959  T=1 F=0  T=30 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10959  T=1 F=0  T=30 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10965  T=1 F=0  T=29 F=1  if ((ctxt->myDoc != NULL) &&
  d=4   L10966  T=0 F=1  T=0 F=29  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=4   L10971  T=0 F=1  T=0 F=30  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10980  T=1 F=0  T=30 F=0  if (! ctxt->wellFormed) {
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9973  T=11 F=1  T=190 F=13  while ((RAW != 0) &&
  d=3   L9974  T=11 F=0  T=190 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L9980  T=5 F=6  T=99 F=91  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=0 F=5  T=1 F=98  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=5 F=6  T=98 F=91  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=1 F=4  T=8 F=90  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9996  T=0 F=1  T=0 F=8  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=3   L10004  T=5 F=6  T=98 F=91  else if (*cur == '<') {
  d=3   L10005  T=1 F=4  T=29 F=69  if (NXT(1) == '/') {
  d=3   L10006  T=0 F=1  T=14 F=15  if (ctxt->nameNr <= nameNr)
  d=3   L10019  T=0 F=6  T=3 F=88  else if (*cur == '&') {
--- d=3  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=3   L10077  T=0 F=1  T=3 F=27  if (xmlParseElementStart(ctxt) != 0)
  d=3   L10081  T=0 F=1  T=0 F=27  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L10084  T=1 F=0  T=13 F=14  if (CUR == 0) {
--- d=3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=3   L12139  T=0 F=4  T=0 F=140  if (ctxt == NULL)
  d=3   L12141  T=0 F=2  T=15 F=29  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12141  T=2 F=2  T=44 F=96  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12143  T=0 F=4  T=0 F=125  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L12145  T=0 F=4  T=0 F=125  if (ctxt->input == NULL)
  d=3   L12149  T=2 F=2  T=73 F=52  if (ctxt->instate == XML_PARSER_START)
  d=3   L12151  T=3 F=0  T=78 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12151  T=3 F=1  T=78 F=47  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12151  T=3 F=0  T=78 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12152  T=0 F=3  T=2 F=76  (chunk[size - 1] == '\r')) {
  d=3   L12159  T=3 F=0  T=78 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12159  T=3 F=0  T=78 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12159  T=3 F=1  T=78 F=47  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12160  T=3 F=0  T=78 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=3   L12160  T=3 F=0  T=78 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=3   L12170  T=2 F=1  T=67 F=11  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12170  T=2 F=0  T=67 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12171  T=2 F=0  T=67 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12171  T=0 F=2  T=0 F=67  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12202  T=0 F=3  T=0 F=78  if (res < 0) {
  d=3   L12211  T=1 F=0  T=47 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=3   L12212  T=1 F=0  T=47 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=3   L12212  T=1 F=0  T=47 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=3   L12214  T=0 F=1  T=0 F=47  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=3   L12233  T=0 F=4  T=0 F=125  if (remain != 0) {
  d=3   L12238  T=1 F=3  T=7 F=118  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L12241  T=3 F=0  T=118 F=0  if ((ctxt->input != NULL) &&
  d=3   L12242  T=0 F=3  T=0 F=118  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=3   L12243  T=0 F=3  T=0 F=118  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=3   L12248  T=0 F=3  T=36 F=46  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12248  T=3 F=0  T=82 F=36  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12251  T=0 F=3  T=0 F=82  if (remain != 0) {
  d=3   L12257  T=0 F=0  T=2 F=0  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=3   L12257  T=0 F=3  T=2 F=80  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=3   L12258  T=0 F=0  T=2 F=0  (ctxt->input->buf != NULL)) {
  d=3   L12268  T=0 F=3  T=9 F=73  if (terminate) {
  d=3   L12274  T=0 F=0  T=9 F=0  if (ctxt->input != NULL) {
  d=3   L12275  T=0 F=0  T=0 F=9  if (ctxt->input->buf == NULL)
  d=3   L12283  T=0 F=0  T=9 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=3   L12284  T=0 F=0  T=5 F=4  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=3   L12287  T=0 F=0  T=0 F=4  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=3   L12287  T=0 F=0  T=4 F=5  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=3   L12290  T=0 F=0  T=9 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=3   L12291  T=0 F=0  T=9 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L12291  T=0 F=0  T=9 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L12296  T=3 F=0  T=28 F=54  if (ctxt->wellFormed == 0)
--- d=2  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226) ---
  d=2   L10115  T=0 F=5  T=0 F=99  if (((unsigned int) ctxt->nameNr > xmlParserMaxDepth) &&
  d=2   L10125  T=0 F=5  T=0 F=99  if (ctxt->record_info) {
  d=2   L10131  T=0 F=5  T=0 F=99  if (ctxt->spaceNr == 0)
  d=2   L10133  T=0 F=5  T=1 F=98  else if (*ctxt->space == -2)
  d=2   L10140  T=5 F=0  T=99 F=0  if (ctxt->sax2)
  d=2   L10147  T=0 F=5  T=0 F=99  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L10149  T=2 F=3  T=26 F=73  if (name == NULL) {
  d=2   L10162  T=0 F=0  T=0 F=1  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L10162  T=0 F=3  T=1 F=72  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L10170  T=0 F=0  T=0 F=1  if ((RAW == '/') && (NXT(1) == '>')) {
  d=2   L10170  T=0 F=3  T=1 F=72  if ((RAW == '/') && (NXT(1) == '>')) {
  d=2   L10196  T=2 F=1  T=52 F=21  if (RAW == '>') {
  d=2   L10209  T=0 F=1  T=1 F=20  if (nsNr != ctxt->nsNr)
  d=2   L10215  T=1 F=0  T=19 F=2  if ( ret != NULL && ctxt->record_info ) {
  d=2   L10215  T=0 F=1  T=0 F=19  if ( ret != NULL && ctxt->record_info ) {
--- d=2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=2   L11409  T=0 F=4  T=0 F=125  if (ctxt->input == NULL)
  d=2   L11465  T=4 F=0  T=125 F=0  if ((ctxt->input != NULL) &&
  d=2   L11466  T=0 F=4  T=0 F=125  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=2   L11470  T=38 F=0  T=863 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=2   L11471  T=0 F=24  T=36 F=442  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L11471  T=24 F=14  T=478 F=385  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L11474  T=0 F=38  T=0 F=827  if (ctxt->input == NULL) break;
  d=2   L11475  T=0 F=38  T=0 F=827  if (ctxt->input->buf == NULL)
  d=2   L11486  T=34 F=4  T=721 F=106  if ((ctxt->instate != XML_PARSER_START) &&
  d=2   L11487  T=0 F=34  T=0 F=721  (ctxt->input->buf->raw != NULL) &&
  d=2   L11500  T=0 F=38  T=7 F=820  if (avail < 1)
  d=2   L11502  T=0 F=38  T=0 F=820  switch (ctxt->instate) {
  d=2   L11503  T=0 F=38  T=0 F=820  case XML_PARSER_EOF:
  d=2   L11508  T=4 F=34  T=106 F=714  case XML_PARSER_START:
  d=2   L11509  T=2 F=2  T=33 F=73  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=2   L11516  T=0 F=2  T=0 F=33  if (avail < 4)
  d=2   L11535  T=0 F=2  T=0 F=73  if (avail < 2)
  d=2   L11539  T=0 F=2  T=0 F=73  if (cur == 0) {
  d=2   L11553  T=0 F=2  T=69 F=4  if ((cur == '<') && (next == '?')) {
  d=2   L11553  T=2 F=0  T=73 F=0  if ((cur == '<') && (next == '?')) {
  d=2   L11555  T=0 F=0  T=0 F=69  if (avail < 5) goto done;
  d=2   L11556  T=0 F=0  T=65 F=4  if ((!terminate) &&
  d=2   L11557  T=0 F=0  T=13 F=52  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=2   L11559  T=0 F=0  T=56 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11559  T=0 F=0  T=56 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11562  T=0 F=0  T=56 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=2   L11563  T=0 F=0  T=54 F=2  (ctxt->input->cur[3] == 'm') &&
  d=2   L11564  T=0 F=0  T=54 F=0  (ctxt->input->cur[4] == 'l') &&
  d=2   L11572  T=0 F=0  T=0 F=54  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=2   L11581  T=0 F=0  T=54 F=0  if ((ctxt->encoding == NULL) &&
  d=2   L11582  T=0 F=0  T=0 F=54  (ctxt->input->encoding != NULL))
  d=2   L11584  T=0 F=0  T=54 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11584  T=0 F=0  T=54 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11585  T=0 F=0  T=52 F=2  (!ctxt->disableSAX))
  d=2   L11594  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11594  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11595  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=2   L11604  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11604  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11608  T=0 F=2  T=0 F=4  if (ctxt->version == NULL) {
  d=2   L11612  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11612  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11613  T=2 F=0  T=4 F=0  (!ctxt->disableSAX))
  d=2   L11622  T=9 F=29  T=178 F=642  case XML_PARSER_START_TAG: {
  d=2   L11629  T=0 F=9  T=0 F=178  if ((avail < 2) && (ctxt->inputNr == 1))
  d=2   L11632  T=0 F=9  T=0 F=178  if (cur != '<') {
  d=2   L11639  T=2 F=6  T=26 F=102  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11639  T=8 F=1  T=128 F=50  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11641  T=0 F=7  T=0 F=152  if (ctxt->spaceNr == 0)
  d=2   L11643  T=0 F=7  T=5 F=147  else if (*ctxt->space == -2)
  d=2   L11648  T=7 F=0  T=152 F=0  if (ctxt->sax2)
  d=2   L11655  T=0 F=7  T=0 F=152  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11657  T=1 F=6  T=5 F=147  if (name == NULL) {
  d=2   L11660  T=1 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L11660  T=1 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L11670  T=0 F=0  T=0 F=2  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L11670  T=0 F=6  T=2 F=145  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L11678  T=0 F=0  T=0 F=2  if ((RAW == '/') && (NXT(1) == '>')) {
  d=2   L11678  T=0 F=6  T=2 F=145  if ((RAW == '/') && (NXT(1) == '>')) {
  d=2   L11707  T=4 F=2  T=105 F=42  if (RAW == '>') {
  d=2   L11721  T=20 F=18  T=374 F=446  case XML_PARSER_CONTENT: {
  d=2   L11722  T=0 F=20  T=0 F=374  if ((avail < 2) && (ctxt->inputNr == 1))
  d=2   L11727  T=2 F=8  T=35 F=116  if ((cur == '<') && (next == '/')) {
  d=2   L11727  T=10 F=10  T=151 F=223  if ((cur == '<') && (next == '/')) {
  d=2   L11730  T=0 F=8  T=4 F=112  } else if ((cur == '<') && (next == '?')) {
  d=2   L11730  T=8 F=10  T=116 F=223  } else if ((cur == '<') && (next == '?')) {
  d=2   L11731  T=0 F=0  T=3 F=1  if ((!terminate) &&
  d=2   L11732  T=0 F=0  T=1 F=2  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=2   L11736  T=6 F=2  T=95 F=17  } else if ((cur == '<') && (next != '!')) {
  d=2   L11736  T=8 F=10  T=112 F=223  } else if ((cur == '<') && (next != '!')) {
  d=2   L11739  T=2 F=10  T=17 F=223  } else if ((cur == '<') && (next == '!') &&
  d=2   L11739  T=2 F=0  T=17 F=0  } else if ((cur == '<') && (next == '!') &&
  d=2   L11740  T=0 F=2  T=0 F=17  (ctxt->input->cur[2] == '-') &&
  d=2   L11747  T=2 F=0  T=17 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=2   L11747  T=2 F=10  T=17 F=223  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=2   L11748  T=0 F=2  T=0 F=17  (ctxt->input->cur[2] == '[') &&
  d=2   L11758  T=2 F=10  T=17 F=223  } else if ((cur == '<') && (next == '!') &&
  d=2   L11758  T=2 F=0  T=17 F=0  } else if ((cur == '<') && (next == '!') &&
  d=2   L11759  T=0 F=2  T=5 F=12  (avail < 9)) {
  d=2   L11761  T=2 F=10  T=12 F=223  } else if (cur == '<') {
  d=2   L11765  T=0 F=10  T=22 F=201  } else if (cur == '&') {
  d=2   L11766  T=0 F=0  T=14 F=8  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=2   L11766  T=0 F=0  T=8 F=6  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=2   L11782  T=10 F=0  T=201 F=0  if ((ctxt->inputNr == 1) &&
  d=2   L11783  T=10 F=0  T=187 F=14  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=2   L11784  T=0 F=10  T=5 F=128  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=2   L11784  T=10 F=0  T=133 F=54  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=2   L11792  T=3 F=35  T=44 F=776  case XML_PARSER_END_TAG:
  d=2   L11793  T=0 F=3  T=0 F=44  if (avail < 2)
  d=2   L11795  T=1 F=2  T=9 F=20  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=2   L11795  T=3 F=0  T=29 F=15  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=2   L11797  T=2 F=0  T=35 F=0  if (ctxt->sax2) {
  d=2   L11805  T=0 F=2  T=0 F=35  if (ctxt->instate == XML_PARSER_EOF) {
  d=2   L11807  T=0 F=2  T=12 F=23  } else if (ctxt->nameNr == 0) {
  d=2   L11813  T=0 F=38  T=0 F=820  case XML_PARSER_CDATA_SECTION: {
  d=2   L11904  T=2 F=36  T=60 F=760  case XML_PARSER_MISC:
  d=2   L11905  T=0 F=38  T=48 F=772  case XML_PARSER_PROLOG:
  d=2   L11906  T=0 F=38  T=10 F=810  case XML_PARSER_EPILOG:
  d=2   L11908  T=0 F=2  T=0 F=118  if (ctxt->input->buf == NULL)
  d=2   L11914  T=0 F=2  T=8 F=110  if (avail < 2)
  d=2   L11918  T=2 F=0  T=108 F=2  if ((cur == '<') && (next == '?')) {
  d=2   L11918  T=0 F=2  T=2 F=106  if ((cur == '<') && (next == '?')) {
  d=2   L11919  T=0 F=0  T=2 F=0  if ((!terminate) &&
  d=2   L11920  T=0 F=0  T=0 F=2  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=2   L11927  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11929  T=0 F=2  T=48 F=58  } else if ((cur == '<') && (next == '!') &&
  d=2   L11929  T=2 F=0  T=106 F=2  } else if ((cur == '<') && (next == '!') &&
  d=2   L11930  T=0 F=0  T=0 F=48  (ctxt->input->cur[2] == '-') &&
  d=2   L11942  T=2 F=0  T=58 F=50  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=2   L11943  T=0 F=2  T=48 F=10  (cur == '<') && (next == '!') &&
  d=2   L11943  T=2 F=0  T=58 F=0  (cur == '<') && (next == '!') &&
  d=2   L11944  T=0 F=0  T=48 F=0  (ctxt->input->cur[2] == 'D') &&
  d=2   L11945  T=0 F=0  T=48 F=0  (ctxt->input->cur[3] == 'O') &&
  d=2   L11946  T=0 F=0  T=48 F=0  (ctxt->input->cur[4] == 'C') &&
  d=2   L11947  T=0 F=0  T=48 F=0  (ctxt->input->cur[5] == 'T') &&
  d=2   L11948  T=0 F=0  T=48 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=2   L11949  T=0 F=0  T=48 F=0  (ctxt->input->cur[7] == 'P') &&
  d=2   L11950  T=0 F=0  T=48 F=0  (ctxt->input->cur[8] == 'E')) {
  d=2   L11951  T=0 F=0  T=48 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11951  T=0 F=0  T=0 F=48  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11959  T=0 F=0  T=0 F=48  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11961  T=0 F=0  T=0 F=48  if (RAW == '[') {
  d=2   L11972  T=0 F=0  T=48 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L11972  T=0 F=0  T=48 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L11973  T=0 F=0  T=48 F=0  (ctxt->sax->externalSubset != NULL))
  d=2   L11985  T=0 F=2  T=0 F=58  } else if ((cur == '<') && (next == '!') &&
  d=2   L11985  T=2 F=0  T=58 F=2  } else if ((cur == '<') && (next == '!') &&
  d=2   L11989  T=0 F=2  T=2 F=58  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=2   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L12007  T=0 F=38  T=0 F=820  case XML_PARSER_DTD: {
  d=2   L12029  T=0 F=38  T=0 F=820  case XML_PARSER_COMMENT:
  d=2   L12038  T=0 F=38  T=0 F=820  case XML_PARSER_IGNORE:
  d=2   L12047  T=0 F=38  T=0 F=820  case XML_PARSER_PI:
  d=2   L12056  T=0 F=38  T=0 F=820  case XML_PARSER_ENTITY_DECL:
  d=2   L12065  T=0 F=38  T=0 F=820  case XML_PARSER_ENTITY_VALUE:
  d=2   L12074  T=0 F=38  T=0 F=820  case XML_PARSER_ATTRIBUTE_VALUE:
  d=2   L12083  T=0 F=38  T=0 F=820  case XML_PARSER_SYSTEM_LITERAL:
  d=2   L12092  T=0 F=38  T=0 F=820  case XML_PARSER_PUBLIC_LITERAL:
--- d=1  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774) ---
  d=1   L9369  T=0 F=12  T=0 F=251  if (RAW != '<') return(NULL);
  d=1   L9391  T=3 F=9  T=31 F=220  if (localname == NULL) {
  d=1   L9406  T=6 F=3  T=117 F=103  while (((RAW != '>') &&
  d=1   L9407  T=6 F=0  T=117 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=1   L9408  T=6 F=0  T=116 F=0  (IS_BYTE_CHAR(RAW))) && (ctxt->instate != XML_PARSER_EOF)) {
  d=1   L9413  T=0 F=6  T=12 F=104  if (attname == NULL) {
  d=1   L9418  T=3 F=3  T=4 F=100  if (attvalue == NULL)
  d=1   L9420  T=0 F=3  T=0 F=100  if (len < 0) len = xmlStrlen(attvalue);
  d=1   L9422  T=3 F=0  T=0 F=100  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {  <-- BLOCKER
  d=1   L9422  T=3 F=0  T=0 F=0  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {  <-- BLOCKER
  d=1   L9426  T=0 F=3  T=0 F=0  if (URL == NULL) {
  d=1   L9433  T=3 F=0  T=0 F=0  if (*URL != 0) {
  d=1   L9435  T=3 F=0  T=0 F=0  if (uri == NULL) {
  d=1   L9447  T=0 F=3  T=0 F=0  if (URL == ctxt->str_xml_ns) {
  d=1   L9455  T=0 F=3  T=0 F=0  if ((len == 29) &&
  d=1   L9467  T=0 F=3  T=0 F=0  for (j = 1;j <= nbNs;j++)
  d=1   L9470  T=0 F=3  T=0 F=0  if (j <= nbNs)
  d=1   L9473  T=3 F=0  T=0 F=0  if (nsPush(ctxt, NULL, URL) > 0) nbNs++;
  d=1   L9475  T=0 F=0  T=0 F=100  } else if (aprefix == ctxt->str_xmlns) {
  d=1   L9548  T=0 F=0  T=0 F=14  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9548  T=0 F=0  T=86 F=14  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9549  T=0 F=0  T=0 F=86  if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
  d=1   L9564  T=0 F=0  T=44 F=56  if (alloc)
  d=1   L9574  T=0 F=0  T=44 F=56  if (alloc != 0) attval = 1;
  d=1   L9579  T=3 F=3  T=0 F=104  if ((attvalue != NULL) && (alloc != 0)) {
  d=1   L9579  T=0 F=3  T=0 F=0  if ((attvalue != NULL) && (alloc != 0)) {
  d=1   L9585  T=0 F=6  T=0 F=104  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L9587  T=0 F=0  T=0 F=3  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=1   L9587  T=0 F=3  T=3 F=47  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=1   L9587  T=3 F=3  T=54 F=50  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=1   L9589  T=3 F=0  T=50 F=0  if (SKIP_BLANKS == 0) {
  d=1   L9597  T=0 F=9  T=0 F=220  if (ctxt->input->id != inputid) {
  d=1   L9605  T=0 F=9  T=100 F=220  for (i = 0, j = 0; j < nratts; i += 5, j++) {
  d=1   L9606  T=0 F=0  T=56 F=44  if (atts[i+2] != NULL) {
  d=1   L9621  T=0 F=9  T=18 F=202  if (ctxt->attsDefault != NULL) {
  d=1   L9625  T=0 F=0  T=6 F=12  if (defaults != NULL) {
  d=1   L9626  T=0 F=0  T=12 F=6  for (i = 0;i < defaults->nbAttrs;i++) {
  d=1   L9633  T=0 F=0  T=0 F=12  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
  d=1   L9648  T=0 F=0  T=6 F=6  } else if (aprefix == ctxt->str_xmlns) {
  d=1   L9652  T=0 F=0  T=0 F=6  for (j = 1;j <= nbNs;j++)
  d=1   L9655  T=0 F=0  T=0 F=6  if (j <= nbNs) continue;
  d=1   L9658  T=0 F=0  T=6 F=0  if (nsname != defaults->values[5 * i + 2]) {
  d=1   L9659  T=0 F=0  T=6 F=0  if (nsPush(ctxt, attname,
  d=1   L9667  T=0 F=0  T=6 F=6  for (j = 0;j < nbatts;j+=5) {
  d=1   L9668  T=0 F=0  T=0 F=6  if ((attname == atts[j]) && (aprefix == atts[j+1]))
  d=1   L9671  T=0 F=0  T=0 F=6  if (j < nbatts) continue;
  d=1   L9673  T=0 F=0  T=0 F=6  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9673  T=0 F=0  T=0 F=6  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=1   L9683  T=0 F=0  T=0 F=6  if (aprefix == NULL)
  d=1   L9689  T=0 F=0  T=0 F=6  if ((ctxt->standalone == 1) &&
  d=1   L9704  T=0 F=9  T=106 F=220  for (i = 0; i < nbatts;i += 5) {
  d=1   L9708  T=0 F=0  T=88 F=18  if (atts[i + 1] != NULL) {
  d=1   L9710  T=0 F=0  T=82 F=6  if (nsname == NULL) {
  d=1   L9724  T=0 F=0  T=6 F=106  for (j = 0; j < i;j += 5) {
  d=1   L9725  T=0 F=0  T=0 F=6  if (atts[i] == atts[j]) {
  d=1   L9741  T=0 F=9  T=0 F=220  if ((prefix != NULL) && (nsname == NULL)) {
  d=1   L9752  T=9 F=0  T=220 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=1   L9752  T=9 F=0  T=220 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=1   L9753  T=9 F=0  T=186 F=34  (!ctxt->disableSAX)) {
  d=1   L9754  T=3 F=6  T=3 F=183  if (nbNs > 0)
  d=1   L9767  T=0 F=9  T=44 F=176  if (attval != 0) {
  d=1   L9768  T=0 F=0  T=44 F=44  for (i = 3,j = 0; j < nratts;i += 5,j++)
  d=1   L9769  T=0 F=0  T=44 F=0  if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))
  d=1   L9769  T=0 F=0  T=44 F=0  if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))

[off-chain: 847 additional divergent branches across 82 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=6d4e408dfb9b247b, size=277 bytes, fuzzer=value_profile_cmplog, trial=3, discovered_at=85665s, mutation_op=BytesDeleteMutator,CrossoverInsertMutator,BytesCopyMutator,BytesDeleteMutator,BytesInsertMutator,QwordAddMutator,WordAddMutator):
  0000: 45 44 20 27 73 69 6d 70 6c 65 27 0a 20 20 20 20   ED 'simple'.    
  0010: 20 20 20 20 20 20 20 20 00 6c 69 00 6b 2d 68 72           .li.k-hr
  0020: 65 66 20 20 20 43 44 41 54 41 20 20 20 20 78 6c   ef   CDATA    xl
  0030: 69 6e 6b 3a 68 72 65 66 25 20 20 43 44 41 54 41   ink:href%  CDATA

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0574a3903f63564c, size=198 bytes, fuzzer=cmplog, trial=2, discovered_at=0s, mutation_op=DwordInterestingMutator,BytesDeleteMutator,CrossoverReplaceMutator,QwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 ff 69 6f 6e 3d 22 31   <?xml ver.ion="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=08714a0d6b1c1aaa, size=425 bytes, fuzzer=cmplog, trial=2, discovered_at=3s, mutation_op=BitFlipMutator,ByteNegMutator,BytesExpandMutator,BitFlipMutator,CrossoverInsertMutator):
  0000: 07 00 00 00 31 32 37 37 37 70 6c 65 27 0a 20 20   ....12777ple'.  
  0010: 20 20 20 20 20 20 20 20 20 20 78 6c 69 6e 6b 3a             xlink:
  0020: 68 72 65 66 20 20 20 43 44 41 54 41 20 20 20 20   href   CDATA    
  0030: 20 23 49 4d 50 4c 49 32 2e 78 6d 6c 5c 0a 3c 3f    #IMPLI2.xml\.<?
Seed 3 (id=011bb1a41b201f9b, size=327 bytes, fuzzer=cmplog, trial=2, discovered_at=5s, mutation_op=BitFlipMutator,BytesDeleteMutator,ByteRandMutator,WordAddMutator,BytesInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2c 6c   a SYSTEM "dtds,l
Seed 4 (id=026d5e573bace2aa, size=368 bytes, fuzzer=cmplog, trial=3, discovered_at=10s, mutation_op=BytesRandSetMutator,CrossoverReplaceMutator,ByteInterestingMutator,ByteInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=188326f28c00684e, size=368 bytes, fuzzer=cmplog, trial=3, discovered_at=15s, mutation_op=BytesDeleteMutator,QwordAddMutator,QwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  45(E)x1                             06(.)x16 07(.)x2 65(e)x1 54(T)x1 +10u  PARTIAL
   0x0001  44(D)x1                             00(.)x21 54(T)x2 65(e)x1 20( )x1 +5u  DIFFER
   0x0002  20( )x1                             00(.)x20 65(e)x1 62(b)x1 45(E)x1 +7u  PARTIAL
   0x0003  27(')x1                             00(.)x20 65(e)x1 20( )x1 45(E)x1 +7u  DIFFER
   0x0004  73(s)x1                             31(1)x19 65(e)x1 28(()x1 45(E)x1 +8u  DIFFER
   0x0005  69(i)x1                             32(2)x19 78(x)x2 74(t)x2 54(T)x1 +6u  DIFFER
   0x0006  6d(m)x1                             37(7)x19 54(T)x2 6d(m)x2 50(P)x1 +6u  PARTIAL
   0x0007  70(p)x1                             37(7)x19 20( )x2 6c(l)x2 4c(L)x1 +6u  PARTIAL
   0x0008  6c(l)x1                             37(7)x19 49(I)x1 44(D)x1 45(E)x1 +8u  DIFFER
   0x0009  65(e)x1                             32(2)x18 70(p)x1 53(S)x1 41(A)x1 +9u  DIFFER
   0x000a  27(')x1                             2e(.)x17 54(T)x2 6c(l)x1 2c(,)x1 +9u  DIFFER
   0x000b  0a(.)x1                             78(x)x18 65(e)x1 20( )x1 06(.)x1 +9u  DIFFER
   0x000c  20( )x1                             6d(m)x17 6c(l)x2 27(')x1 62(b)x1 +9u  DIFFER
   0x000d  20( )x1                             6c(l)x18 20( )x2 37(7)x2 0a(.)x1 +7u  PARTIAL
   0x000e  20( )x1                             5c(\)x19 20( )x2 00(.)x2 78(x)x1 +6u  PARTIAL
   0x000f  20( )x1                             0a(.)x19 20( )x3 6d(m)x1 31(1)x1 +6u  PARTIAL
   0x0010  20( )x1                             3c(<)x19 20( )x3 32(2)x2 6c(l)x1 +5u  PARTIAL
   0x0011  20( )x1                             3f(?)x19 20( )x3 6c(l)x2 6e(n)x1 +5u  PARTIAL
   0x0012  20( )x1                             78(x)x20 20( )x1 73(s)x1 37(7)x1 +7u  PARTIAL
   0x0013  20( )x1                             6d(m)x19 6e(n)x2 20( )x1 3a(:)x1 +7u  PARTIAL
   0x0014  20( )x1                             6c(l)x20 20( )x1 78(x)x1 32(2)x1 +7u  PARTIAL
   0x0015  20( )x1                             20( )x20 6c(l)x1 2e(.)x1 37(7)x1 +7u  PARTIAL
   0x0016  20( )x1                             76(v)x19 20( )x2 78(x)x2 69(i)x1 +6u  PARTIAL
   0x0017  20( )x1                             65(e)x18 20( )x2 6e(n)x1 6d(m)x1 +8u  PARTIAL
   0x0018  00(.)x1                             72(r)x18 20( )x2 6c(l)x2 6b(k)x1 +7u  DIFFER
   0x0019  6c(l)x1                             73(s)x18 20( )x3 5c(\)x2 78(x)x2 +5u  DIFFER
   0x001a  69(i)x1                             69(i)x18 0a(.)x2 6d(m)x2 20( )x2 +6u  PARTIAL
   0x001b  00(.)x1                             6f(o)x18 6c(l)x3 3c(<)x2 43(C)x1 +6u  DIFFER
   0x001c  6b(k)x1                             6e(n)x18 3f(?)x2 20( )x2 69(i)x1 +7u  DIFFER
   0x001d  2d(-)x1                             3d(=)x17 78(x)x2 6e(n)x1 41(A)x1 +9u  DIFFER
   0x001e  68(h)x1                             22(")x18 6d(m)x2 6b(k)x1 54(T)x1 +8u  DIFFER
   0x001f  72(r)x1                             31(1)x18 6c(l)x2 3a(:)x1 41(A)x1 +8u  PARTIAL
   0x0020  65(e)x1                             2e(.)x18 20( )x3 68(h)x1 9f(.)x1 +7u  DIFFER
   0x0021  66(f)x1                             30(0)x17 76(v)x2 72(r)x1 20( )x1 +9u  DIFFER
   0x0022  20( )x1                             22(")x17 65(e)x3 20( )x2 55(U)x1 +7u  PARTIAL
   0x0023  20( )x1                             3f(?)x17 20( )x2 72(r)x2 66(f)x1 +8u  PARTIAL
   0x0024  20( )x1                             3e(>)x17 20( )x2 73(s)x2 2d(-)x1 +8u  PARTIAL
   0x0025  43(C)x1                             0a(.)x17 20( )x4 69(i)x2 23(#)x1 +6u  DIFFER
   0x0026  44(D)x1                             3c(<)x17 20( )x2 6f(o)x2 06(.)x1 +8u  DIFFER
   0x0027  41(A)x1                             21(!)x18 6e(n)x2 2e(.)x2 20( )x2 +6u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6726.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6726,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6726 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6726 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6726 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).