==== BLOCKER ====
Target: libxml2
Branch ID: 6475
Location: /src/libxml2/parser.c:2650:9
Enclosing function: parser.c:xmlStringDecodeEntitiesInt
Source line:     if (str < last)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (grimoire_structural vs grimoire)
value_profile                    2        8          0  REFERENCE
value_profile_cmplog             2        8          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0        8          2  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=4.30h  loser=16.80h
  avg hitcount on branch: winner=45  loser=0
  prob_div=0.90  dur_div=12.50h  hit_div=45
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6475/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlStringDecodeEntitiesInt (/src/libxml2/parser.c:2616-2809) ---
[ ]  2614  xmlStringDecodeEntitiesInt(xmlParserCtxtPtr ctxt, const xmlChar *str, int len,
[ ]  2615  		           int what, xmlChar end, xmlChar  end2, xmlChar end3,
[B]  2616                             int check) {
[B]  2617      xmlChar *buffer = NULL;
[B]  2618      size_t buffer_size = 0;
[B]  2619      size_t nbchars = 0;
[ ]  2620  
[B]  2621      xmlChar *current = NULL;
[B]  2622      xmlChar *rep = NULL;
[B]  2623      const xmlChar *last;
[B]  2624      xmlEntityPtr ent;
[B]  2625      int c,l;
[ ]  2626  
[B]  2627      if (str == NULL)
[ ]  2628          return(NULL);
[B]  2629      last = str + len;
[ ]  2630  
[B]  2631      if (((ctxt->depth > 40) &&
[B]  2632           ((ctxt->options & XML_PARSE_HUGE) == 0)) ||
[B]  2633  	(ctxt->depth > 100)) {
[ ]  2634  	xmlFatalErrMsg(ctxt, XML_ERR_ENTITY_LOOP,
[ ]  2635                         "Maximum entity nesting depth exceeded");
[ ]  2636  	return(NULL);
[ ]  2637      }
[ ]  2638  
[ ]  2639      /*
[ ]  2640       * allocate a translation buffer.
[ ]  2641       */
[B]  2642      buffer_size = XML_PARSER_BIG_BUFFER_SIZE;
[B]  2643      buffer = (xmlChar *) xmlMallocAtomic(buffer_size);
[B]  2644      if (buffer == NULL) goto mem_error;
[ ]  2645  
[ ]  2646      /*
[ ]  2647       * OK loop until we reach one of the ending char or a size limit.
[ ]  2648       * we are operating on already parsed values.
[ ]  2649       */
[B]  2650      if (str < last) <-- BLOCKER
[B]  2651  	c = CUR_SCHAR(str, l);
[W]  2652      else
[W]  2653          c = 0;
[B]  2654      while ((c != 0) && (c != end) && /* non input consuming loop */
[B]  2655             (c != end2) && (c != end3) &&
[B]  2656             (ctxt->instate != XML_PARSER_EOF)) {
[ ]  2657  
[B]  2658  	if (c == 0) break;
[B]  2659          if ((c == '&') && (str[1] == '#')) {
[ ]  2660  	    int val = xmlParseStringCharRef(ctxt, &str);
[ ]  2661  	    if (val == 0)
[ ]  2662                  goto int_error;
[ ]  2663  	    COPY_BUF(0,buffer,nbchars,val);
[ ]  2664  	    if (nbchars + XML_PARSER_BUFFER_SIZE > buffer_size) {
[ ]  2665  	        growBuffer(buffer, XML_PARSER_BUFFER_SIZE);
[ ]  2666  	    }
[B]  2667  	} else if ((c == '&') && (what & XML_SUBSTITUTE_REF)) {
[ ]  2668  	    if (xmlParserDebugEntities)
[ ]  2669  		xmlGenericError(xmlGenericErrorContext,
[ ]  2670  			"String decoding Entity Reference: %.30s\n",
[ ]  2671  			str);
[ ]  2672  	    ent = xmlParseStringEntityRef(ctxt, &str);
[ ]  2673  	    if ((ent != NULL) &&
[ ]  2674  		(ent->etype == XML_INTERNAL_PREDEFINED_ENTITY)) {
[ ]  2675  		if (ent->content != NULL) {
[ ]  2676  		    COPY_BUF(0,buffer,nbchars,ent->content[0]);
[ ]  2677  		    if (nbchars + XML_PARSER_BUFFER_SIZE > buffer_size) {
[ ]  2678  			growBuffer(buffer, XML_PARSER_BUFFER_SIZE);
[ ]  2679  		    }
[ ]  2680  		} else {
[ ]  2681  		    xmlFatalErrMsg(ctxt, XML_ERR_INTERNAL_ERROR,
[ ]  2682  			    "predefined entity has no content\n");
[ ]  2683                      goto int_error;
[ ]  2684  		}
[ ]  2685  	    } else if ((ent != NULL) && (ent->content != NULL)) {
[ ]  2686  	        if ((check) && (xmlParserEntityCheck(ctxt, ent->length)))
[ ]  2687                      goto int_error;
[ ]  2688  
[ ]  2689                  if (ent->flags & XML_ENT_EXPANDING) {
[ ]  2690  	            xmlFatalErr(ctxt, XML_ERR_ENTITY_LOOP, NULL);
[ ]  2691                      xmlHaltParser(ctxt);
[ ]  2692                      ent->content[0] = 0;
[ ]  2693                      goto int_error;
[ ]  2694                  }
[ ]  2695  
[ ]  2696                  ent->flags |= XML_ENT_EXPANDING;
[ ]  2697  		ctxt->depth++;
[ ]  2698  		rep = xmlStringDecodeEntitiesInt(ctxt, ent->content,
[ ]  2699                          ent->length, what, 0, 0, 0, check);
[ ]  2700  		ctxt->depth--;
[ ]  2701                  ent->flags &= ~XML_ENT_EXPANDING;
[ ]  2702  
[ ]  2703  		if (rep == NULL) {
[ ]  2704                      ent->content[0] = 0;
[ ]  2705                      goto int_error;
[ ]  2706                  }
[ ]  2707  
[ ]  2708                  current = rep;
[ ]  2709                  while (*current != 0) { /* non input consuming loop */
[ ]  2710                      buffer[nbchars++] = *current++;
[ ]  2711                      if (nbchars + XML_PARSER_BUFFER_SIZE > buffer_size) {
[ ]  2712                          growBuffer(buffer, XML_PARSER_BUFFER_SIZE);
[ ]  2713                      }
[ ]  2714                  }
[ ]  2715                  xmlFree(rep);
[ ]  2716                  rep = NULL;
[ ]  2717  	    } else if (ent != NULL) {
[ ]  2718  		int i = xmlStrlen(ent->name);
[ ]  2719  		const xmlChar *cur = ent->name;
[ ]  2720  
[ ]  2721  		buffer[nbchars++] = '&';
[ ]  2722  		if (nbchars + i + XML_PARSER_BUFFER_SIZE > buffer_size) {
[ ]  2723  		    growBuffer(buffer, i + XML_PARSER_BUFFER_SIZE);
[ ]  2724  		}
[ ]  2725  		for (;i > 0;i--)
[ ]  2726  		    buffer[nbchars++] = *cur++;
[ ]  2727  		buffer[nbchars++] = ';';
[ ]  2728  	    }
[B]  2729  	} else if (c == '%' && (what & XML_SUBSTITUTE_PEREF)) {
[ ]  2730  	    if (xmlParserDebugEntities)
[ ]  2731  		xmlGenericError(xmlGenericErrorContext,
[ ]  2732  			"String decoding PE Reference: %.30s\n", str);
[ ]  2733  	    ent = xmlParseStringPEReference(ctxt, &str);
[ ]  2734  	    if (ent != NULL) {
[ ]  2735                  if (ent->content == NULL) {
[ ]  2736  		    /*
[ ]  2737  		     * Note: external parsed entities will not be loaded,
[ ]  2738  		     * it is not required for a non-validating parser to
[ ]  2739  		     * complete external PEReferences coming from the
[ ]  2740  		     * internal subset
[ ]  2741  		     */
[ ]  2742  		    if (((ctxt->options & XML_PARSE_NOENT) != 0) ||
[ ]  2743  			((ctxt->options & XML_PARSE_DTDVALID) != 0) ||
[ ]  2744  			(ctxt->validate != 0)) {
[ ]  2745  			xmlLoadEntityContent(ctxt, ent);
[ ]  2746  		    } else {
[ ]  2747  			xmlWarningMsg(ctxt, XML_ERR_ENTITY_PROCESSING,
[ ]  2748  		  "not validating will not read content for PE entity %s\n",
[ ]  2749  		                      ent->name, NULL);
[ ]  2750  		    }
[ ]  2751  		}
[ ]  2752  
[ ]  2753  	        if ((check) && (xmlParserEntityCheck(ctxt, ent->length)))
[ ]  2754                      goto int_error;
[ ]  2755  
[ ]  2756                  if (ent->flags & XML_ENT_EXPANDING) {
[ ]  2757  	            xmlFatalErr(ctxt, XML_ERR_ENTITY_LOOP, NULL);
[ ]  2758                      xmlHaltParser(ctxt);
[ ]  2759                      if (ent->content != NULL)
[ ]  2760                          ent->content[0] = 0;
[ ]  2761                      goto int_error;
[ ]  2762                  }
[ ]  2763  
[ ]  2764                  ent->flags |= XML_ENT_EXPANDING;
[ ]  2765  		ctxt->depth++;
[ ]  2766  		rep = xmlStringDecodeEntitiesInt(ctxt, ent->content,
[ ]  2767                          ent->length, what, 0, 0, 0, check);
[ ]  2768  		ctxt->depth--;
[ ]  2769                  ent->flags &= ~XML_ENT_EXPANDING;
[ ]  2770  
[ ]  2771  		if (rep == NULL) {
[ ]  2772                      if (ent->content != NULL)
[ ]  2773                          ent->content[0] = 0;
[ ]  2774                      goto int_error;
[ ]  2775                  }
[ ]  2776                  current = rep;
[ ]  2777                  while (*current != 0) { /* non input consuming loop */
[ ]  2778                      buffer[nbchars++] = *current++;
[ ]  2779                      if (nbchars + XML_PARSER_BUFFER_SIZE > buffer_size) {
[ ]  2780                          growBuffer(buffer, XML_PARSER_BUFFER_SIZE);
[ ]  2781                      }
[ ]  2782                  }
[ ]  2783                  xmlFree(rep);
[ ]  2784                  rep = NULL;
[ ]  2785  	    }
[B]  2786  	} else {
[B]  2787  	    COPY_BUF(l,buffer,nbchars,c);
[B]  2788  	    str += l;
[B]  2789  	    if (nbchars + XML_PARSER_BUFFER_SIZE > buffer_size) {
[ ]  2790  	        growBuffer(buffer, XML_PARSER_BUFFER_SIZE);
[ ]  2791  	    }
[B]  2792  	}
[B]  2793  	if (str < last)
[B]  2794  	    c = CUR_SCHAR(str, l);
[B]  2795  	else
[B]  2796  	    c = 0;
[B]  2797      }
[B]  2798      buffer[nbchars] = 0;
[B]  2799      return(buffer);
[ ]  2800  
[ ]  2801  mem_error:
[ ]  2802      xmlErrMemory(ctxt, NULL);
[ ]  2803  int_error:
[ ]  2804      if (rep != NULL)
[ ]  2805          xmlFree(rep);
[ ]  2806      if (buffer != NULL)
[ ]  2807          xmlFree(buffer);
[ ]  2808      return(NULL);
[ ]  2809  }

--- Caller (1 hop): xmlStringDecodeEntities (/src/libxml2/parser.c:2864-2868, calls parser.c:xmlStringDecodeEntitiesInt at line 2866) (full body — short) ---
[B]  2864  		        xmlChar end, xmlChar  end2, xmlChar end3) {
[B]  2865      if ((ctxt == NULL) || (str == NULL)) return(NULL);
[B]  2866      return(xmlStringDecodeEntitiesInt(ctxt, str, xmlStrlen(str), what, <-- CALL
[B]  2867                                        end, end2, end3, 0));
[B]  2868  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlStringDecodeEntities  (/src/libxml2/parser.c:2864-2868, calls parser.c:xmlStringDecodeEntitiesInt at line 2866)
hop 2  xmlStringLenDecodeEntities  (/src/libxml2/parser.c:2835-2840, calls parser.c:xmlStringDecodeEntitiesInt at line 2838)
hop 3  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438, calls xmlStringDecodeEntities at line 1180)
hop 3  SAX2.c:xmlSAX2DecodeAttrEntities  (/src/libxml2/SAX2.c:1958-1973, calls xmlStringLenDecodeEntities at line 1969)
hop 3  xmlParseEntityValue  (/src/libxml2/parser.c:3793-3933, calls xmlStringDecodeEntities at line 3879)
hop 4  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 4  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199, calls SAX2.c:xmlSAX2DecodeAttrEntities at line 2099)
hop 4  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)
hop 4  xmlParseEntityDecl  (/src/libxml2/parser.c:5476-5721, calls xmlParseEntityValue at line 5529)
hop 5  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459, calls SAX2.c:xmlSAX2AttributeNs at line 2421)
hop 5  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseEntityDecl at line 6959)
hop 6  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 6  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 7  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 7  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 7  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 8  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 8  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 8  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1820       541  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     811       142  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     724       181  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
     253        45  xmlParseName  (/src/libxml2/parser.c:3368-3412)
     141        30  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
      80         0  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      66        21  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
      66        21  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752)
      65        21  nodePush  (/src/libxml2/parser.c:1750-1776)
      65        21  parser.c:nameNsPush  (/src/libxml2/parser.c:1820-1860)
      48         6  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
      36         0  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
      36         0  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)
      37         2  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
      44         9  parser.c:xmlStringDecodeEntitiesInt  (/src/libxml2/parser.c:2616-2809)  <-- enclosing
... (29 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=8   L8396  T=0 F=18  T=0 F=9  if (name == NULL) {
  d=8   L8409  T=18 F=0  T=9 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=8   L8420  T=18 F=0  T=9 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=8   L8420  T=18 F=0  T=9 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=8   L8421  T=18 F=0  T=9 F=0  (!ctxt->disableSAX))
  d=8   L8423  T=0 F=18  T=0 F=9  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L8430  T=0 F=18  T=0 F=9  if (RAW == '[')
  d=8   L8436  T=0 F=18  T=0 F=9  if (RAW != '>') {
--- d=8  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=8   L10816  T=0 F=7  T=0 F=3  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=8   L10816  T=0 F=7  T=0 F=3  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=8   L10829  T=7 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L10829  T=7 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L10831  T=0 F=7  T=0 F=3  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L10834  T=7 F=0  T=3 F=0  if ((ctxt->encoding == NULL) &&
  d=8   L10835  T=7 F=0  T=3 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=8   L10846  T=2 F=5  T=3 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=8   L10852  T=0 F=7  T=0 F=3  if (CUR == 0) {
  d=8   L10863  T=1 F=6  T=0 F=3  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=8   L10884  T=7 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=8   L10884  T=7 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=8   L10884  T=7 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=8   L10886  T=0 F=7  T=0 F=3  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L10888  T=7 F=0  T=3 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=8   L10888  T=7 F=0  T=3 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=8   L10889  T=7 F=0  T=3 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=8   L10889  T=0 F=7  T=0 F=3  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=8   L10907  T=0 F=6  T=0 F=3  if (RAW == '[') {
  d=8   L10918  T=6 F=0  T=3 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=8   L10918  T=6 F=0  T=3 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=8   L10919  T=6 F=0  T=3 F=0  (!ctxt->disableSAX))
  d=8   L10922  T=0 F=6  T=0 F=3  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L10936  T=0 F=7  T=0 F=3  if (RAW != '<') {
  d=8   L10950  T=0 F=7  T=0 F=3  if (RAW != 0) {
  d=8   L10959  T=7 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L10959  T=7 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L10965  T=7 F=0  T=3 F=0  if ((ctxt->myDoc != NULL) &&
  d=8   L10966  T=0 F=7  T=0 F=3  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=8   L10971  T=2 F=5  T=2 F=1  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=8   L10973  T=1 F=1  T=0 F=2  if (ctxt->valid)
  d=8   L10977  T=1 F=1  T=2 F=0  if (ctxt->options & XML_PARSE_OLD10)
  d=8   L10980  T=5 F=2  T=1 F=2  if (! ctxt->wellFormed) {
--- d=6  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=6   L7099  T=18 F=0  T=9 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L7100  T=18 F=0  T=9 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=6   L7109  T=0 F=18  T=0 F=9  if (enc != XML_CHAR_ENCODING_NONE)
  d=6   L7123  T=0 F=18  T=0 F=9  if (ctxt->myDoc == NULL) {
  d=6   L7131  T=0 F=18  T=0 F=9  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=6   L7131  T=18 F=0  T=9 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=6   L7137  T=66 F=0  T=15 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=6   L7137  T=48 F=18  T=6 F=9  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=6   L7139  T=48 F=0  T=6 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=6   L7139  T=48 F=0  T=6 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=6   L7139  T=0 F=48  T=0 F=6  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=6   L7141  T=48 F=0  T=6 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=6   L7141  T=48 F=0  T=6 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=6   L7151  T=0 F=18  T=0 F=9  if (RAW != 0) {
--- d=5  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=5   L6952  T=48 F=0  T=6 F=0  if (CUR == '<') {
  d=5   L6953  T=48 F=0  T=6 F=0  if (NXT(1) == '!') {
  d=5   L6955  T=30 F=18  T=3 F=3  case 'E':
  d=5   L6956  T=30 F=0  T=3 F=0  if (NXT(3) == 'L')
  d=5   L6963  T=18 F=30  T=0 F=6  case 'A':
  d=5   L6966  T=0 F=48  T=0 F=6  case 'N':
  d=5   L6969  T=0 F=48  T=0 F=6  case '-':
  d=5   L6972  T=0 F=48  T=3 F=3  default:
  d=5   L6986  T=0 F=48  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF)
--- d=2  xmlStringDecodeEntities  (/src/libxml2/parser.c:2864-2868) ---
  d=2   L2865  T=0 F=44  T=0 F=9  if ((ctxt == NULL) || (str == NULL)) return(NULL);
  d=2   L2865  T=0 F=44  T=0 F=9  if ((ctxt == NULL) || (str == NULL)) return(NULL);
--- d=1  parser.c:xmlStringDecodeEntitiesInt  (/src/libxml2/parser.c:2616-2809) ---
  d=1   L2627  T=0 F=44  T=0 F=9  if (str == NULL)
  d=1   L2631  T=0 F=44  T=0 F=9  if (((ctxt->depth > 40) &&
  d=1   L2633  T=0 F=44  T=0 F=9  (ctxt->depth > 100)) {
  d=1   L2644  T=0 F=44  T=0 F=9  if (buffer == NULL) goto mem_error;
  d=1   L2650  T=6 F=38  T=9 F=0  if (str < last)  <-- BLOCKER
  d=1   L2654  T=33 F=44  T=150 F=9  while ((c != 0) && (c != end) && /* non input consuming l...
  d=1   L2654  T=33 F=0  T=150 F=0  while ((c != 0) && (c != end) && /* non input consuming l...
  d=1   L2655  T=33 F=0  T=150 F=0  (c != end2) && (c != end3) &&
  d=1   L2655  T=33 F=0  T=150 F=0  (c != end2) && (c != end3) &&
  d=1   L2656  T=33 F=0  T=150 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=1   L2658  T=0 F=33  T=0 F=150  if (c == 0) break;
  d=1   L2659  T=0 F=33  T=0 F=150  if ((c == '&') && (str[1] == '#')) {
  d=1   L2667  T=0 F=33  T=0 F=150  } else if ((c == '&') && (what & XML_SUBSTITUTE_REF)) {
  d=1   L2729  T=0 F=33  T=0 F=150  } else if (c == '%' && (what & XML_SUBSTITUTE_PEREF)) {
  d=1   L2789  T=0 F=33  T=0 F=150  if (nbchars + XML_PARSER_BUFFER_SIZE > buffer_size) {
  d=1   L2793  T=27 F=6  T=141 F=9  if (str < last)

[off-chain: 684 additional divergent branches across 67 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=4dfb54980cf39827, size=155 bytes, fuzzer=grimoire, trial=1, discovered_at=4750s, mutation_op=GrimoireRecursiveReplacementMutator):
  0000: f8 ff ff ff ff 06 6d 6c 5c 0a 3c 3f 6c 20 3f 3e   ......ml\.<?l ?>
  0010: 3c 21 44 4f 43 54 59 50 45 61 20 53 59 53 54 45   <!DOCTYPEa SYSTE
  0020: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
  0030: 74 64 22 3e 3c 61 3e 3c 62 20 3a 51 3d 22 22 3e   td"><a><b :Q="">
Seed 2 (id=110e34e3a9cff266, size=416 bytes, fuzzer=grimoire, trial=1, discovered_at=4878s, mutation_op=GrimoireRecursiveReplacementMutator,GrimoireRecursiveReplacementMutator):
  0000: 55 36 e8 76 ad 9c f0 4c ff 37 37 32 6c 5c 0a 3c   U6.v...L.772l\.<
  0010: 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e   ?xml version="1.
  0020: 30 22 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20 53   0"?><!DOCTYPEa S
  0030: 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37   YSTEM "dtds/1277
Seed 3 (id=3ab4d97b081ac59f, size=173 bytes, fuzzer=grimoire, trial=1, discovered_at=6390s, mutation_op=GrimoireRandomDeleteMutator,GrimoireRandomDeleteMutator,GrimoireRecursiveReplacementMutator):
  0000: d8 3e 42 0f 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44   .>B.l\.<?l ?><!D
  0010: 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22   OCTYPEa SYSTEM "
  0020: 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22   dtds/127772.dtd"
  0030: 3e 3c 61 3e 3c 62 20 51 3d 22 22 3e 5c 0a 64 74   ><a><b Q="">\.dt
Seed 4 (id=282b5462beef8741, size=1059 bytes, fuzzer=grimoire, trial=1, discovered_at=7462s, mutation_op=GrimoireRecursiveReplacementMutator):
  0000: 49 53 4f 2d 38 38 35 39 2d 34 00 00 6d 6c 5c 0a   ISO-8859-4..ml\.
  0010: 3c 3f 78 6d 6c 20 3e 3c 62 20 78 6d 6c 6e 73 3a   <?xml ><b xmlns:
  0020: 66 3d 22 22 3e 74 64 5c 0a 9b 70 3a 2f 2f 6e 22   f="">td\..p://n"
  0030: 3e 7f 96 98 00 ff 78 6d 6c 5c 0a 3c 3f 6c 3f 3e   >.....xml\.<?l?>
Seed 5 (id=4c1ded53000f2888, size=328 bytes, fuzzer=grimoire, trial=1, discovered_at=11655s, mutation_op=GrimoireRecursiveReplacementMutator,GrimoireRandomDeleteMutator,GrimoireRandomDeleteMutator):
  0000: 9c ff ff ff 06 78 6d 6c 5c 0a 3c 3f 6c 20 3f 3e   .....xml\.<?l ?>
  0010: 3c 21 44 4f 43 54 59 50 45 61 20 53 59 53 54 45   <!DOCTYPEa SYSTE
  0020: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
  0030: 74 64 22 3e 3c 61 3e 3c 62 20 66 3d 22 22 3e 3c   td"><a><b f=""><

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=81df39141490a9f6, size=385 bytes, fuzzer=cmplog, trial=1, discovered_at=575s, mutation_op=BitFlipMutator,CrossoverReplaceMutator,ByteAddMutator,TokenInsert,BytesExpandMutator,BytesSwapMutator):
  0000: 70 3a 2f 74 06 00 00 74 31 32 37 37 37 32 43 78   p:/t...t127772Cx
  0010: 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f   ml\.<?xml versio
  0020: 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54   n="1.0"?>.<!DOCT
  0030: 59 50 45 20 61 20 53 59 53 54 45 4d 20 22 64 74   YPE a SYSTEM "dt
Seed 2 (id=3322bf57bcfff149, size=557 bytes, fuzzer=cmplog, trial=1, discovered_at=6314s, mutation_op=BytesInsertCopyMutator,ByteIncMutator,BytesDeleteMutator,BytesInsertCopyMutator,BytesRandSetMutator,BytesSetMutator,BytesDeleteMutator):
  0000: 31 32 37 37 37 32 2e 64 73 64 06 00 00 00 31 32   127772.dsd....12
  0010: 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7772.xml\.<?xml 
  0020: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0030: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
Seed 3 (id=b817581b4b71ba79, size=557 bytes, fuzzer=cmplog, trial=1, discovered_at=29843s, mutation_op=ByteIncMutator):
  0000: 31 32 37 37 37 32 2e 64 73 64 06 00 00 00 31 32   127772.dsd....12
  0010: 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7772.xml\.<?xml 
  0020: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0030: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f8(.)x1 55(U)x1 d8(.)x1 49(I)x1 +3u  31(1)x2 70(p)x1                     DIFFER
   0x0001  ff(.)x2 36(6)x1 3e(>)x1 53(S)x1 +2u  32(2)x2 3a(:)x1                     DIFFER
   0x0002  ff(.)x2 e8(.)x1 42(B)x1 4f(O)x1 +2u  37(7)x2 2f(/)x1                     DIFFER
   0x0003  ff(.)x3 76(v)x1 0f(.)x1 2d(-)x1 +1u  37(7)x2 74(t)x1                     DIFFER
   0x0004  ff(.)x2 06(.)x2 ad(.)x1 6c(l)x1 +1u  37(7)x2 06(.)x1                     PARTIAL
   0x0005  06(.)x1 9c(.)x1 5c(\)x1 38(8)x1 +3u  32(2)x2 00(.)x1                     PARTIAL
   0x0006  6d(m)x3 f0(.)x1 0a(.)x1 35(5)x1 +1u  2e(.)x2 00(.)x1                     DIFFER
   0x0007  6c(l)x3 4c(L)x1 3c(<)x1 39(9)x1 +1u  64(d)x2 74(t)x1                     DIFFER
   0x0008  5c(\)x3 ff(.)x1 3f(?)x1 2d(-)x1 +1u  73(s)x2 31(1)x1                     DIFFER
   0x0009  0a(.)x3 37(7)x1 6c(l)x1 34(4)x1 +1u  64(d)x2 32(2)x1                     DIFFER
   0x000a  3c(<)x3 37(7)x1 20( )x1 00(.)x1 +1u  06(.)x2 37(7)x1                     PARTIAL
   0x000b  3f(?)x4 32(2)x1 00(.)x1 6c(l)x1     00(.)x2 37(7)x1                     PARTIAL
   0x000c  6c(l)x4 3e(>)x1 6d(m)x1 5c(\)x1     00(.)x2 37(7)x1                     DIFFER
   0x000d  20( )x3 5c(\)x1 3c(<)x1 6c(l)x1 +1u  00(.)x2 32(2)x1                     DIFFER
   0x000e  3f(?)x3 0a(.)x1 21(!)x1 5c(\)x1 +1u  31(1)x2 43(C)x1                     DIFFER
   0x000f  3e(>)x3 3c(<)x1 44(D)x1 0a(.)x1 +1u  32(2)x2 78(x)x1                     DIFFER
   0x0010  3c(<)x4 3f(?)x1 4f(O)x1 6c(l)x1     37(7)x2 6d(m)x1                     DIFFER
   0x0011  21(!)x3 78(x)x1 43(C)x1 3f(?)x1 +1u  37(7)x2 6c(l)x1                     DIFFER
   0x0012  44(D)x3 6d(m)x1 54(T)x1 78(x)x1 +1u  37(7)x2 5c(\)x1                     DIFFER
   0x0013  4f(O)x3 6c(l)x1 59(Y)x1 6d(m)x1 +1u  32(2)x2 0a(.)x1                     DIFFER
   0x0014  43(C)x3 20( )x1 50(P)x1 6c(l)x1 +1u  2e(.)x2 3c(<)x1                     PARTIAL
   0x0015  54(T)x3 76(v)x1 45(E)x1 20( )x1 +1u  78(x)x2 3f(?)x1                     DIFFER
   0x0016  59(Y)x3 65(e)x1 61(a)x1 3e(>)x1 +1u  6d(m)x2 78(x)x1                     DIFFER
   0x0017  50(P)x3 72(r)x1 20( )x1 3c(<)x1 +1u  6c(l)x2 6d(m)x1                     DIFFER
   0x0018  45(E)x3 73(s)x1 53(S)x1 62(b)x1 +1u  5c(\)x2 6c(l)x1                     DIFFER
   0x0019  61(a)x3 69(i)x1 59(Y)x1 20( )x1 +1u  0a(.)x2 20( )x1                     PARTIAL
   0x001a  20( )x3 6f(o)x1 53(S)x1 78(x)x1 +1u  3c(<)x2 76(v)x1                     DIFFER
   0x001b  53(S)x3 6e(n)x1 54(T)x1 6d(m)x1 +1u  3f(?)x2 65(e)x1                     DIFFER
   0x001c  59(Y)x3 45(E)x2 3d(=)x1 6c(l)x1     78(x)x2 72(r)x1                     DIFFER
   0x001d  53(S)x3 22(")x1 4d(M)x1 6e(n)x1 +1u  6d(m)x2 73(s)x1                     DIFFER
   0x001e  54(T)x3 20( )x2 31(1)x1 73(s)x1     6c(l)x2 69(i)x1                     DIFFER
   0x001f  45(E)x3 2e(.)x1 22(")x1 3a(:)x1 +1u  20( )x2 6f(o)x1                     DIFFER
   0x0020  4d(M)x3 30(0)x1 64(d)x1 66(f)x1 +1u  76(v)x2 6e(n)x1                     DIFFER
   0x0021  20( )x3 22(")x1 74(t)x1 3d(=)x1 +1u  65(e)x2 3d(=)x1                     PARTIAL
   0x0022  22(")x4 3f(?)x1 64(d)x1 54(T)x1     72(r)x2 22(")x1                     PARTIAL
   0x0023  64(d)x3 3e(>)x1 73(s)x1 22(")x1 +1u  73(s)x2 31(1)x1                     PARTIAL
   0x0024  74(t)x3 3c(<)x1 2f(/)x1 3e(>)x1 +1u  69(i)x2 2e(.)x1                     DIFFER
   0x0025  64(d)x3 21(!)x1 31(1)x1 74(t)x1 +1u  6f(o)x2 30(0)x1                     DIFFER
   0x0026  73(s)x3 44(D)x1 32(2)x1 64(d)x1 +1u  6e(n)x2 22(")x1                     PARTIAL
   0x0027  2f(/)x3 4f(O)x1 37(7)x1 5c(\)x1 +1u  3d(=)x2 3f(?)x1                     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6475.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6475,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6475 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6475 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6475 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).