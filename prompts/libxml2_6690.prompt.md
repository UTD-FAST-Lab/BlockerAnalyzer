==== BLOCKER ====
Target: libxml2
Branch ID: 6690
Location: /src/libxml2/parser.c:7658:6
Enclosing function: xmlParseEntityRef
Source line: 	if ((ctxt->wellFormed == 1 ) && (ent == NULL) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog); loser (value_profile vs value_profile); loser (calibrated_energy vs minimizer)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog             8        2          0  REFERENCE
naive_ctx                        0        9          1  REFERENCE
naive_ngram4                     3        7          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        8        2          0  winner (calibrated_energy vs naive)
fast                             4        6          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'minimizer', 'naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'fast', 'grimoire']

==== DECISIVE PAIRS (3) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=3.70h  loser=16.80h
  avg hitcount on branch: winner=50  loser=3
  prob_div=0.80  dur_div=13.10h  hit_div=47
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001
--- Pair 2: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.50h  loser=16.80h
  avg hitcount on branch: winner=11  loser=3
  prob_div=0.70  dur_div=10.30h  hit_div=8
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002
--- Pair 3: minimizer > naive  [delta: calibrated_energy] ---
  subject 38  (minimizer vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.10h  loser=16.80h
  avg hitcount on branch: winner=52  loser=3
  prob_div=0.60  dur_div=12.70h  hit_div=48
  subject-level: delta_AUC=20906460.0  p_AUC=0.1041  delta_Final=371.4  p_final=0.0046

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6690/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseEntityRef (/src/libxml2/parser.c:7619-7769) ---
[ ]  7617   */
[ ]  7618  xmlEntityPtr
[B]  7619  xmlParseEntityRef(xmlParserCtxtPtr ctxt) {
[B]  7620      const xmlChar *name;
[B]  7621      xmlEntityPtr ent = NULL;
[ ]  7622  
[B]  7623      GROW;
[B]  7624      if (ctxt->instate == XML_PARSER_EOF)
[ ]  7625          return(NULL);
[ ]  7626  
[B]  7627      if (RAW != '&')
[ ]  7628          return(NULL);
[B]  7629      NEXT;
[B]  7630      name = xmlParseName(ctxt);
[B]  7631      if (name == NULL) {
[L]  7632  	xmlFatalErrMsg(ctxt, XML_ERR_NAME_REQUIRED,
[L]  7633  		       "xmlParseEntityRef: no name\n");
[L]  7634          return(NULL);
[L]  7635      }
[B]  7636      if (RAW != ';') {
[L]  7637  	xmlFatalErr(ctxt, XML_ERR_ENTITYREF_SEMICOL_MISSING, NULL);
[L]  7638  	return(NULL);
[L]  7639      }
[B]  7640      NEXT;
[ ]  7641  
[ ]  7642      /*
[ ]  7643       * Predefined entities override any extra definition
[ ]  7644       */
[B]  7645      if ((ctxt->options & XML_PARSE_OLDSAX) == 0) {
[B]  7646          ent = xmlGetPredefinedEntity(name);
[B]  7647          if (ent != NULL)
[ ]  7648              return(ent);
[B]  7649      }
[ ]  7650  
[ ]  7651      /*
[ ]  7652       * Ask first SAX for entity resolution, otherwise try the
[ ]  7653       * entities which may have stored in the parser context.
[ ]  7654       */
[B]  7655      if (ctxt->sax != NULL) {
[B]  7656  	if (ctxt->sax->getEntity != NULL)
[B]  7657  	    ent = ctxt->sax->getEntity(ctxt->userData, name);
[B]  7658  	if ((ctxt->wellFormed == 1 ) && (ent == NULL) && <-- BLOCKER
[B]  7659  	    (ctxt->options & XML_PARSE_OLDSAX))
[ ]  7660  	    ent = xmlGetPredefinedEntity(name);
[B]  7661  	if ((ctxt->wellFormed == 1 ) && (ent == NULL) &&
[B]  7662  	    (ctxt->userData==ctxt)) {
[W]  7663  	    ent = xmlSAX2GetEntity(ctxt, name);
[W]  7664  	}
[B]  7665      }
[B]  7666      if (ctxt->instate == XML_PARSER_EOF)
[ ]  7667  	return(NULL);
[ ]  7668      /*
[ ]  7669       * [ WFC: Entity Declared ]
[ ]  7670       * In a document without any DTD, a document with only an
[ ]  7671       * internal DTD subset which contains no parameter entity
[ ]  7672       * references, or a document with "standalone='yes'", the
[ ]  7673       * Name given in the entity reference must match that in an
[ ]  7674       * entity declaration, except that well-formed documents
[ ]  7675       * need not declare any of the following entities: amp, lt,
[ ]  7676       * gt, apos, quot.
[ ]  7677       * The declaration of a parameter entity must precede any
[ ]  7678       * reference to it.
[ ]  7679       * Similarly, the declaration of a general entity must
[ ]  7680       * precede any reference to it which appears in a default
[ ]  7681       * value in an attribute-list declaration. Note that if
[ ]  7682       * entities are declared in the external subset or in
[ ]  7683       * external parameter entities, a non-validating processor
[ ]  7684       * is not obligated to read and process their declarations;
[ ]  7685       * for such documents, the rule that an entity must be
[ ]  7686       * declared is a well-formedness constraint only if
[ ]  7687       * standalone='yes'.
[ ]  7688       */
[B]  7689      if (ent == NULL) {
[B]  7690  	if ((ctxt->standalone == 1) ||
[B]  7691  	    ((ctxt->hasExternalSubset == 0) &&
[B]  7692  	     (ctxt->hasPErefs == 0))) {
[L]  7693  	    xmlFatalErrMsgStr(ctxt, XML_ERR_UNDECLARED_ENTITY,
[L]  7694  		     "Entity '%s' not defined\n", name);
[B]  7695  	} else {
[B]  7696  	    xmlErrMsgStr(ctxt, XML_WAR_UNDECLARED_ENTITY,
[B]  7697  		     "Entity '%s' not defined\n", name);
[B]  7698  	    if ((ctxt->inSubset == 0) &&
[B]  7699  		(ctxt->sax != NULL) &&
[B]  7700  		(ctxt->sax->reference != NULL)) {
[B]  7701  		ctxt->sax->reference(ctxt->userData, name);
[B]  7702  	    }
[B]  7703  	}
[B]  7704  	ctxt->valid = 0;
[B]  7705      }
[ ]  7706  
[ ]  7707      /*
[ ]  7708       * [ WFC: Parsed Entity ]
[ ]  7709       * An entity reference must not contain the name of an
[ ]  7710       * unparsed entity
[ ]  7711       */
[ ]  7712      else if (ent->etype == XML_EXTERNAL_GENERAL_UNPARSED_ENTITY) {
[ ]  7713  	xmlFatalErrMsgStr(ctxt, XML_ERR_UNPARSED_ENTITY,
[ ]  7714  		 "Entity reference to unparsed entity %s\n", name);
[ ]  7715      }
[ ]  7716  
[ ]  7717      /*
[ ]  7718       * [ WFC: No External Entity References ]
[ ]  7719       * Attribute values cannot contain direct or indirect
[ ]  7720       * entity references to external entities.
[ ]  7721       */
[ ]  7722      else if ((ctxt->instate == XML_PARSER_ATTRIBUTE_VALUE) &&
[ ]  7723  	     (ent->etype == XML_EXTERNAL_GENERAL_PARSED_ENTITY)) {
[ ]  7724  	xmlFatalErrMsgStr(ctxt, XML_ERR_ENTITY_IS_EXTERNAL,
[ ]  7725  	     "Attribute references external entity '%s'\n", name);
[ ]  7726      }
[ ]  7727      /*
[ ]  7728       * [ WFC: No < in Attribute Values ]
[ ]  7729       * The replacement text of any entity referred to directly or
[ ]  7730       * indirectly in an attribute value (other than "&lt;") must
[ ]  7731       * not contain a <.
[ ]  7732       */
[ ]  7733      else if ((ctxt->instate == XML_PARSER_ATTRIBUTE_VALUE) &&
[ ]  7734  	     (ent->etype != XML_INTERNAL_PREDEFINED_ENTITY)) {
[ ]  7735  	if ((ent->flags & XML_ENT_CHECKED_LT) == 0) {
[ ]  7736              if ((ent->content != NULL) && (xmlStrchr(ent->content, '<')))
[ ]  7737                  ent->flags |= XML_ENT_CONTAINS_LT;
[ ]  7738              ent->flags |= XML_ENT_CHECKED_LT;
[ ]  7739          }
[ ]  7740          if (ent->flags & XML_ENT_CONTAINS_LT)
[ ]  7741              xmlFatalErrMsgStr(ctxt, XML_ERR_LT_IN_ATTRIBUTE,
[ ]  7742                      "'<' in entity '%s' is not allowed in attributes "
[ ]  7743                      "values\n", name);
[ ]  7744      }
[ ]  7745  
[ ]  7746      /*
[ ]  7747       * Internal check, no parameter entities here ...
[ ]  7748       */
[ ]  7749      else {
[ ]  7750  	switch (ent->etype) {
[ ]  7751  	    case XML_INTERNAL_PARAMETER_ENTITY:
[ ]  7752  	    case XML_EXTERNAL_PARAMETER_ENTITY:
[ ]  7753  	    xmlFatalErrMsgStr(ctxt, XML_ERR_ENTITY_IS_PARAMETER,
[ ]  7754  	     "Attempt to reference the parameter entity '%s'\n",
[ ]  7755  			      name);
[ ]  7756  	    break;
[ ]  7757  	    default:
[ ]  7758  	    break;
[ ]  7759  	}
[ ]  7760      }
[ ]  7761  
[ ]  7762      /*
[ ]  7763       * [ WFC: No Recursion ]
[ ]  7764       * A parsed entity must not contain a recursive reference
[ ]  7765       * to itself, either directly or indirectly.
[ ]  7766       * Done somewhere else
[ ]  7767       */
[B]  7768      return(ent);
[B]  7769  }

--- Caller (1 hop): xmlParseReference (/src/libxml2/parser.c:7173-7586, calls xmlParseEntityRef at line 7232) (±10 around call site) ---
[ ]  7222  	    if ((ctxt->sax != NULL) && (ctxt->sax->characters != NULL) &&
[ ]  7223  		(!ctxt->disableSAX))
[ ]  7224  		ctxt->sax->characters(ctxt->userData, out, i);
[ ]  7225  	}
[ ]  7226  	return;
[ ]  7227      }
[ ]  7228  
[ ]  7229      /*
[ ]  7230       * We are seeing an entity reference
[ ]  7231       */
[B]  7232      ent = xmlParseEntityRef(ctxt); <-- CALL
[B]  7233      if (ent == NULL) return;
[ ]  7234      if (!ctxt->wellFormed)
[ ]  7235  	return;
[ ]  7236      was_checked = ent->flags & XML_ENT_PARSED;
[ ]  7237  
[ ]  7238      /* special case of predefined entities */
[ ]  7239      if ((ent->name == NULL) ||
[ ]  7240          (ent->etype == XML_INTERNAL_PREDEFINED_ENTITY)) {
[ ]  7241  	val = ent->content;
[ ]  7242  	if (val == NULL) return;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseAttValueComplex  (/src/libxml2/parser.c:3948-4190, calls xmlParseEntityRef at line 4020)
hop 2  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls xmlParseEntityRef at line 7232)
hop 3  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203, calls parser.c:xmlParseAttValueComplex at line 9202)
hop 3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseReference at line 10020)
hop 3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseReference at line 11768)
hop 4  parser.c:xmlParseAttribute2  (/src/libxml2/parser.c:9225-9323, calls parser.c:xmlParseAttValueInternal at line 9258)
hop 4  xmlParseAttValue  (/src/libxml2/parser.c:4229-4232, calls parser.c:xmlParseAttValueInternal at line 4231)
hop 4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 4  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 4  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 5  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 5  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 5  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774, calls parser.c:xmlParseAttribute2 at line 9411)
hop 5  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600, calls xmlParseAttValue at line 8562)
hop 5  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785, calls xmlParseAttValue at line 5777)
hop 5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 5  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 6  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226, calls parser.c:xmlParseStartTag2 at line 10142)
hop 6  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169, calls xmlParseDefaultDecl at line 6118)
hop 6  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752, calls xmlParseAttribute at line 8662)
hop 6  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 6  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 6  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 7  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 7  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseAttributeListDecl at line 6964)
hop 7  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 8  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 8  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 8  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 8  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     155      3100  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      21       418  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      37       251  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
       9       213  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       6       209  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
       3       167  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
       3       167  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)  <-- enclosing
       0       116  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
       0        99  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       3        74  parser.c:xmlErrMsgStr  (/src/libxml2/parser.c:661-671)
       3        64  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
       3        62  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
       4        60  parser.c:xmlParseLookupCharData  (/src/libxml2/parser.c:11170-11184)
       3        58  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
       3        55  nodePush  (/src/libxml2/parser.c:1750-1776)
... (57 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=6  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752) ---
  d=6   L8641  T=0 F=0  T=0 F=22  if (RAW != '<') return(NULL);
  d=6   L8645  T=0 F=0  T=1 F=21  if (name == NULL) {
  d=6   L8659  T=0 F=0  T=12 F=12  while (((RAW != '>') &&
  d=6   L8660  T=0 F=0  T=12 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=6   L8661  T=0 F=0  T=12 F=0  (IS_BYTE_CHAR(RAW))) && (ctxt->instate != XML_PARSER_EOF)) {
  d=6   L8663  T=0 F=0  T=6 F=6  if (attname == NULL) {
  d=6   L8668  T=0 F=0  T=3 F=3  if (attvalue != NULL) {
  d=6   L8674  T=0 F=0  T=0 F=3  for (i = 0; i < nbatts;i += 2) {
  d=6   L8684  T=0 F=0  T=3 F=0  if (atts == NULL) {
  d=6   L8688  T=0 F=0  T=0 F=3  if (atts == NULL) {
  d=6   L8717  T=0 F=0  T=0 F=3  if (attvalue != NULL)
  d=6   L8724  T=0 F=0  T=0 F=3  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=6   L8724  T=0 F=0  T=3 F=3  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=6   L8726  T=0 F=0  T=3 F=0  if (SKIP_BLANKS == 0) {
  d=6   L8737  T=0 F=0  T=21 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElement != NU...
  d=6   L8737  T=0 F=0  T=21 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElement != NU...
  d=6   L8738  T=0 F=0  T=21 F=0  (!ctxt->disableSAX)) {
  d=6   L8739  T=0 F=0  T=3 F=18  if (nbatts > 0)
  d=6   L8745  T=0 F=0  T=12 F=9  if (atts != NULL) {
  d=6   L8747  T=0 F=0  T=3 F=12  for (i = 1;i < nbatts;i+=2)
  d=6   L8748  T=0 F=0  T=3 F=0  if (atts[i] != NULL)
--- d=6  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226) ---
  d=6   L10115  T=0 F=1  T=0 F=21  if (((unsigned int) ctxt->nameNr > xmlParserMaxDepth) &&
  d=6   L10125  T=0 F=1  T=0 F=21  if (ctxt->record_info) {
  d=6   L10131  T=0 F=1  T=0 F=21  if (ctxt->spaceNr == 0)
  d=6   L10133  T=0 F=1  T=1 F=20  else if (*ctxt->space == -2)
  d=6   L10140  T=1 F=0  T=13 F=8  if (ctxt->sax2)
  d=6   L10147  T=0 F=1  T=0 F=21  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10149  T=0 F=1  T=3 F=18  if (name == NULL) {
  d=6   L10162  T=0 F=1  T=0 F=18  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L10170  T=0 F=1  T=0 F=18  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L10196  T=1 F=0  T=11 F=7  if (RAW == '>') {
  d=6   L10209  T=0 F=0  T=0 F=7  if (nsNr != ctxt->nsNr)
  d=6   L10215  T=0 F=0  T=7 F=0  if ( ret != NULL && ctxt->record_info ) {
  d=6   L10215  T=0 F=0  T=0 F=7  if ( ret != NULL && ctxt->record_info ) {
--- d=5  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600) ---
  d=5   L8549  T=0 F=0  T=6 F=6  if (name == NULL) {
  d=5   L8559  T=0 F=0  T=6 F=0  if (RAW == '=') {
  d=5   L8575  T=0 F=0  T=0 F=6  if ((ctxt->pedantic) && (xmlStrEqual(name, BAD_CAST "xml:...
  d=5   L8586  T=0 F=0  T=0 F=6  if (xmlStrEqual(name, BAD_CAST "xml:space")) {
--- d=5  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774) ---
  d=5   L9369  T=0 F=3  T=0 F=36  if (RAW != '<') return(NULL);
  d=5   L9391  T=0 F=3  T=2 F=34  if (localname == NULL) {
  d=5   L9406  T=0 F=3  T=19 F=15  while (((RAW != '>') &&
  d=5   L9407  T=0 F=0  T=19 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=5   L9408  T=0 F=0  T=19 F=0  (IS_BYTE_CHAR(RAW))) && (ctxt->instate != XML_PARSER_EOF)) {
  d=5   L9413  T=0 F=0  T=16 F=3  if (attname == NULL) {
  d=5   L9418  T=0 F=0  T=0 F=3  if (attvalue == NULL)
  d=5   L9420  T=0 F=0  T=0 F=3  if (len < 0) len = xmlStrlen(attvalue);
  d=5   L9422  T=0 F=0  T=0 F=3  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
  d=5   L9475  T=0 F=0  T=0 F=3  } else if (aprefix == ctxt->str_xmlns) {
  d=5   L9548  T=0 F=0  T=3 F=0  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=5   L9549  T=0 F=0  T=0 F=3  if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
  d=5   L9564  T=0 F=0  T=0 F=3  if (alloc)
  d=5   L9574  T=0 F=0  T=0 F=3  if (alloc != 0) attval = 1;
  d=5   L9579  T=0 F=0  T=0 F=3  if ((attvalue != NULL) && (alloc != 0)) {
  d=5   L9585  T=0 F=0  T=0 F=3  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L9587  T=0 F=0  T=3 F=0  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=5   L9597  T=0 F=3  T=0 F=34  if (ctxt->input->id != inputid) {
  d=5   L9605  T=0 F=3  T=3 F=34  for (i = 0, j = 0; j < nratts; i += 5, j++) {
  d=5   L9606  T=0 F=0  T=3 F=0  if (atts[i+2] != NULL) {
  d=5   L9621  T=0 F=3  T=0 F=34  if (ctxt->attsDefault != NULL) {
  d=5   L9704  T=0 F=3  T=3 F=34  for (i = 0; i < nbatts;i += 5) {
  d=5   L9708  T=0 F=0  T=3 F=0  if (atts[i + 1] != NULL) {
  d=5   L9710  T=0 F=0  T=3 F=0  if (nsname == NULL) {
  d=5   L9724  T=0 F=0  T=0 F=3  for (j = 0; j < i;j += 5) {
  d=5   L9741  T=0 F=3  T=0 F=34  if ((prefix != NULL) && (nsname == NULL)) {
  d=5   L9752  T=3 F=0  T=34 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=5   L9752  T=3 F=0  T=34 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=5   L9753  T=3 F=0  T=34 F=0  (!ctxt->disableSAX)) {
  d=5   L9754  T=0 F=3  T=0 F=34  if (nbNs > 0)
  d=5   L9767  T=0 F=3  T=0 F=34  if (attval != 0) {
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10816  T=0 F=1  T=0 F=6  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10816  T=0 F=1  T=0 F=6  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10829  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10829  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10831  T=0 F=1  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10834  T=1 F=0  T=6 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L10835  T=1 F=0  T=6 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=5   L10846  T=1 F=0  T=6 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=5   L10852  T=0 F=1  T=0 F=6  if (CUR == 0) {
  d=5   L10863  T=0 F=1  T=0 F=6  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=5   L10872  T=0 F=1  T=0 F=6  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=5   L10873  T=0 F=1  T=0 F=6  (ctxt->instate == XML_PARSER_EOF)) {
  d=5   L10884  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10886  T=0 F=1  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10888  T=1 F=0  T=6 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10888  T=1 F=0  T=6 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10889  T=1 F=0  T=6 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10889  T=0 F=1  T=0 F=6  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10907  T=0 F=1  T=0 F=4  if (RAW == '[') {
  d=5   L10918  T=1 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10918  T=1 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10919  T=1 F=0  T=4 F=0  (!ctxt->disableSAX))
  d=5   L10922  T=0 F=1  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10936  T=0 F=1  T=0 F=6  if (RAW != '<') {
  d=5   L10950  T=1 F=0  T=1 F=5  if (RAW != 0) {
  d=5   L10959  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10959  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10965  T=1 F=0  T=6 F=0  if ((ctxt->myDoc != NULL) &&
  d=5   L10966  T=0 F=1  T=0 F=6  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=5   L10971  T=0 F=1  T=0 F=6  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=5   L10980  T=1 F=0  T=6 F=0  if (! ctxt->wellFormed) {
--- d=4  xmlParseAttValue  (/src/libxml2/parser.c:4229-4232) ---
  d=4   L4230  T=0 F=0  T=0 F=6  if ((ctxt == NULL) || (ctxt->input == NULL)) return(NULL);
  d=4   L4230  T=0 F=0  T=0 F=6  if ((ctxt == NULL) || (ctxt->input == NULL)) return(NULL);
--- d=4  parser.c:xmlParseAttribute2  (/src/libxml2/parser.c:9225-9323) ---
  d=4   L9233  T=0 F=0  T=13 F=6  if (name == NULL) {
  d=4   L9242  T=0 F=0  T=0 F=6  if (ctxt->attsSpecial != NULL) {
  d=4   L9255  T=0 F=0  T=6 F=0  if (RAW == '=') {
  d=4   L9259  T=0 F=0  T=3 F=3  if (val == NULL)
  d=4   L9261  T=0 F=0  T=0 F=3  if (normalize) {
  d=4   L9286  T=0 F=0  T=0 F=3  if (*prefix == ctxt->str_xml) {
--- d=4  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=4   L10077  T=0 F=1  T=1 F=5  if (xmlParseElementStart(ctxt) != 0)
  d=4   L10081  T=0 F=1  T=0 F=5  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10084  T=0 F=1  T=5 F=0  if (CUR == 0) {
--- d=4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=4   L12139  T=0 F=3  T=0 F=33  if (ctxt == NULL)
  d=4   L12141  T=1 F=0  T=0 F=11  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12141  T=1 F=2  T=11 F=22  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12143  T=0 F=2  T=0 F=33  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12145  T=0 F=2  T=0 F=33  if (ctxt->input == NULL)
  d=4   L12149  T=2 F=0  T=21 F=12  if (ctxt->instate == XML_PARSER_START)
  d=4   L12151  T=2 F=0  T=19 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12151  T=2 F=0  T=19 F=14  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12151  T=2 F=0  T=19 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12152  T=0 F=2  T=0 F=19  (chunk[size - 1] == '\r')) {
  d=4   L12159  T=2 F=0  T=19 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12159  T=2 F=0  T=19 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12159  T=2 F=0  T=19 F=14  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12160  T=2 F=0  T=19 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=4   L12160  T=2 F=0  T=19 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=4   L12170  T=2 F=0  T=15 F=4  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=4   L12170  T=2 F=0  T=15 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=4   L12171  T=2 F=0  T=15 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12171  T=0 F=2  T=0 F=15  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12202  T=0 F=2  T=0 F=19  if (res < 0) {
  d=4   L12211  T=0 F=0  T=14 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12212  T=0 F=0  T=14 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12212  T=0 F=0  T=14 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12214  T=0 F=0  T=0 F=14  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=4   L12233  T=0 F=2  T=0 F=33  if (remain != 0) {
  d=4   L12238  T=2 F=0  T=0 F=33  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12241  T=0 F=0  T=33 F=0  if ((ctxt->input != NULL) &&
  d=4   L12242  T=0 F=0  T=0 F=33  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=4   L12243  T=0 F=0  T=0 F=33  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=4   L12248  T=0 F=0  T=0 F=23  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12248  T=0 F=0  T=23 F=10  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12251  T=0 F=0  T=0 F=33  if (remain != 0) {
  d=4   L12257  T=0 F=0  T=0 F=33  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=4   L12268  T=0 F=0  T=10 F=23  if (terminate) {
  d=4   L12274  T=0 F=0  T=10 F=0  if (ctxt->input != NULL) {
  d=4   L12275  T=0 F=0  T=0 F=10  if (ctxt->input->buf == NULL)
  d=4   L12283  T=0 F=0  T=10 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=4   L12284  T=0 F=0  T=10 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=4   L12287  T=0 F=0  T=0 F=10  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=4   L12290  T=0 F=0  T=10 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12291  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12291  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12296  T=0 F=0  T=14 F=19  if (ctxt->wellFormed == 0)
--- d=3  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203) ---
  d=3   L9063  T=0 F=0  T=0 F=12  int maxLength = (ctxt->options & XML_PARSE_HUGE) ?
  d=3   L9071  T=0 F=0  T=6 F=6  if (*in != '"' && *in != '\'') {
  d=3   L9071  T=0 F=0  T=6 F=0  if (*in != '"' && *in != '\'') {
  d=3   L9086  T=0 F=0  T=0 F=6  if (in >= end) {
  d=3   L9089  T=0 F=0  T=0 F=6  if (normalize) {
  d=3   L9165  T=0 F=0  T=186 F=0  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9165  T=0 F=0  T=180 F=0  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9165  T=0 F=0  T=180 F=6  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9166  T=0 F=0  T=180 F=0  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9166  T=0 F=0  T=180 F=0  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9166  T=0 F=0  T=180 F=0  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9169  T=0 F=0  T=0 F=180  if (in >= end) {
  d=3   L9179  T=0 F=0  T=0 F=6  if ((in - start) > maxLength) {
  d=3   L9184  T=0 F=0  T=0 F=6  if (*in != limit) goto need_complex;
  d=3   L9188  T=0 F=0  T=3 F=3  if (len != NULL) {
  d=3   L9189  T=0 F=0  T=3 F=0  if (alloc) *alloc = 0;
  d=3   L9193  T=0 F=0  T=0 F=3  if (alloc) *alloc = 1;
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9973  T=4 F=0  T=121 F=5  while ((RAW != 0) &&
  d=3   L9974  T=4 F=0  T=121 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L9980  T=1 F=3  T=15 F=106  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=0 F=1  T=0 F=15  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=1 F=3  T=15 F=106  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=0 F=1  T=3 F=12  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9996  T=0 F=0  T=0 F=3  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=3   L10004  T=1 F=3  T=15 F=106  else if (*cur == '<') {
  d=3   L10005  T=1 F=0  T=0 F=15  if (NXT(1) == '/') {
  d=3   L10006  T=1 F=0  T=0 F=0  if (ctxt->nameNr <= nameNr)
  d=3   L10019  T=1 F=2  T=45 F=61  else if (*cur == '&') {
--- d=3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=3   L11409  T=0 F=2  T=0 F=33  if (ctxt->input == NULL)
  d=3   L11465  T=2 F=0  T=33 F=0  if ((ctxt->input != NULL) &&
  d=3   L11466  T=0 F=2  T=0 F=33  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=3   L11470  T=21 F=0  T=410 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=3   L11471  T=0 F=8  T=0 F=362  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11471  T=8 F=13  T=362 F=48  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11474  T=0 F=21  T=0 F=410  if (ctxt->input == NULL) break;
  d=3   L11475  T=0 F=21  T=0 F=410  if (ctxt->input->buf == NULL)
  d=3   L11486  T=18 F=3  T=383 F=27  if ((ctxt->instate != XML_PARSER_START) &&
  d=3   L11487  T=0 F=18  T=0 F=383  (ctxt->input->buf->raw != NULL) &&
  d=3   L11500  T=0 F=21  T=7 F=403  if (avail < 1)
  d=3   L11502  T=0 F=21  T=0 F=403  switch (ctxt->instate) {
  d=3   L11503  T=0 F=21  T=0 F=403  case XML_PARSER_EOF:
  d=3   L11508  T=3 F=18  T=27 F=376  case XML_PARSER_START:
  d=3   L11509  T=1 F=2  T=6 F=21  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=3   L11516  T=0 F=1  T=0 F=6  if (avail < 4)
  d=3   L11535  T=0 F=2  T=0 F=21  if (avail < 2)
  d=3   L11539  T=0 F=2  T=0 F=21  if (cur == 0) {
  d=3   L11553  T=2 F=0  T=21 F=0  if ((cur == '<') && (next == '?')) {
  d=3   L11553  T=2 F=0  T=21 F=0  if ((cur == '<') && (next == '?')) {
  d=3   L11555  T=0 F=2  T=0 F=21  if (avail < 5) goto done;
  d=3   L11556  T=2 F=0  T=17 F=4  if ((!terminate) &&
  d=3   L11557  T=0 F=2  T=9 F=8  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11559  T=2 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11559  T=2 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11562  T=2 F=0  T=12 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=3   L11563  T=2 F=0  T=12 F=0  (ctxt->input->cur[3] == 'm') &&
  d=3   L11564  T=2 F=0  T=12 F=0  (ctxt->input->cur[4] == 'l') &&
  d=3   L11572  T=0 F=2  T=0 F=12  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=3   L11581  T=2 F=0  T=12 F=0  if ((ctxt->encoding == NULL) &&
  d=3   L11582  T=0 F=2  T=0 F=12  (ctxt->input->encoding != NULL))
  d=3   L11584  T=2 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11584  T=2 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11585  T=2 F=0  T=12 F=0  (!ctxt->disableSAX))
  d=3   L11622  T=2 F=19  T=48 F=355  case XML_PARSER_START_TAG: {
  d=3   L11629  T=0 F=2  T=0 F=48  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11632  T=0 F=2  T=0 F=48  if (cur != '<') {
  d=3   L11639  T=0 F=2  T=11 F=14  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11639  T=2 F=0  T=25 F=23  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11641  T=0 F=2  T=0 F=37  if (ctxt->spaceNr == 0)
  d=3   L11643  T=0 F=2  T=2 F=35  else if (*ctxt->space == -2)
  d=3   L11648  T=2 F=0  T=23 F=14  if (ctxt->sax2)
  d=3   L11655  T=0 F=2  T=0 F=37  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11657  T=0 F=2  T=0 F=37  if (name == NULL) {
  d=3   L11670  T=0 F=2  T=0 F=37  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=3   L11678  T=0 F=2  T=0 F=37  if ((RAW == '/') && (NXT(1) == '>')) {
  d=3   L11707  T=2 F=0  T=22 F=15  if (RAW == '>') {
  d=3   L11721  T=8 F=13  T=307 F=96  case XML_PARSER_CONTENT: {
  d=3   L11722  T=0 F=8  T=3 F=304  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11722  T=0 F=0  T=3 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11727  T=2 F=0  T=0 F=32  if ((cur == '<') && (next == '/')) {
  d=3   L11727  T=2 F=6  T=32 F=272  if ((cur == '<') && (next == '/')) {
  d=3   L11730  T=0 F=0  T=0 F=32  } else if ((cur == '<') && (next == '?')) {
  d=3   L11730  T=0 F=6  T=32 F=272  } else if ((cur == '<') && (next == '?')) {
  d=3   L11736  T=0 F=0  T=26 F=6  } else if ((cur == '<') && (next != '!')) {
  d=3   L11736  T=0 F=6  T=32 F=272  } else if ((cur == '<') && (next != '!')) {
  d=3   L11739  T=0 F=6  T=6 F=272  } else if ((cur == '<') && (next == '!') &&
  d=3   L11739  T=0 F=0  T=6 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11740  T=0 F=0  T=0 F=6  (ctxt->input->cur[2] == '-') &&
  d=3   L11747  T=0 F=0  T=6 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11747  T=0 F=6  T=6 F=272  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11748  T=0 F=0  T=0 F=6  (ctxt->input->cur[2] == '[') &&
  d=3   L11758  T=0 F=6  T=6 F=272  } else if ((cur == '<') && (next == '!') &&
  d=3   L11758  T=0 F=0  T=6 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11759  T=0 F=0  T=0 F=6  (avail < 9)) {
  d=3   L11761  T=0 F=6  T=6 F=272  } else if (cur == '<') {
  d=3   L11765  T=2 F=4  T=122 F=150  } else if (cur == '&') {
  d=3   L11766  T=2 F=0  T=54 F=68  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11766  T=0 F=2  T=0 F=54  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11782  T=4 F=0  T=150 F=0  if ((ctxt->inputNr == 1) &&
  d=3   L11783  T=4 F=0  T=148 F=2  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=3   L11784  T=0 F=4  T=2 F=58  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=3   L11784  T=4 F=0  T=60 F=88  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=3   L11792  T=2 F=19  T=0 F=403  case XML_PARSER_END_TAG:
  d=3   L11793  T=0 F=2  T=0 F=0  if (avail < 2)
  d=3   L11795  T=0 F=2  T=0 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11795  T=2 F=0  T=0 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11797  T=2 F=0  T=0 F=0  if (ctxt->sax2) {
  d=3   L11805  T=0 F=2  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF) {
  d=3   L11807  T=2 F=0  T=0 F=0  } else if (ctxt->nameNr == 0) {
  d=3   L11813  T=0 F=21  T=0 F=403  case XML_PARSER_CDATA_SECTION: {
  d=3   L11904  T=2 F=19  T=13 F=390  case XML_PARSER_MISC:
  d=3   L11905  T=2 F=19  T=8 F=395  case XML_PARSER_PROLOG:
  d=3   L11906  T=2 F=19  T=0 F=403  case XML_PARSER_EPILOG:
  d=3   L11908  T=0 F=6  T=0 F=21  if (ctxt->input->buf == NULL)
  d=3   L11914  T=0 F=6  T=0 F=21  if (avail < 2)
  d=3   L11918  T=6 F=0  T=21 F=0  if ((cur == '<') && (next == '?')) {
  d=3   L11918  T=0 F=6  T=0 F=21  if ((cur == '<') && (next == '?')) {
  d=3   L11929  T=2 F=4  T=9 F=12  } else if ((cur == '<') && (next == '!') &&
  d=3   L11929  T=6 F=0  T=21 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11930  T=0 F=2  T=0 F=9  (ctxt->input->cur[2] == '-') &&
  d=3   L11942  T=2 F=4  T=13 F=8  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=3   L11943  T=2 F=0  T=9 F=4  (cur == '<') && (next == '!') &&
  d=3   L11943  T=2 F=0  T=13 F=0  (cur == '<') && (next == '!') &&
  d=3   L11944  T=2 F=0  T=9 F=0  (ctxt->input->cur[2] == 'D') &&
  d=3   L11945  T=2 F=0  T=9 F=0  (ctxt->input->cur[3] == 'O') &&
  d=3   L11946  T=2 F=0  T=9 F=0  (ctxt->input->cur[4] == 'C') &&
  d=3   L11947  T=2 F=0  T=9 F=0  (ctxt->input->cur[5] == 'T') &&
  d=3   L11948  T=2 F=0  T=9 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=3   L11949  T=2 F=0  T=9 F=0  (ctxt->input->cur[7] == 'P') &&
  d=3   L11950  T=2 F=0  T=9 F=0  (ctxt->input->cur[8] == 'E')) {
  d=3   L11951  T=2 F=0  T=9 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11951  T=0 F=2  T=1 F=8  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11959  T=0 F=2  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11961  T=0 F=2  T=0 F=8  if (RAW == '[') {
  d=3   L11972  T=2 F=0  T=8 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11972  T=2 F=0  T=8 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11973  T=2 F=0  T=8 F=0  (ctxt->sax->externalSubset != NULL))
  d=3   L11985  T=0 F=4  T=0 F=12  } else if ((cur == '<') && (next == '!') &&
  d=3   L11985  T=4 F=0  T=12 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11989  T=2 F=2  T=0 F=12  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=3   L11996  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11996  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L12007  T=0 F=21  T=0 F=403  case XML_PARSER_DTD: {
  d=3   L12029  T=0 F=21  T=0 F=403  case XML_PARSER_COMMENT:
  d=3   L12038  T=0 F=21  T=0 F=403  case XML_PARSER_IGNORE:
  d=3   L12047  T=0 F=21  T=0 F=403  case XML_PARSER_PI:
  d=3   L12056  T=0 F=21  T=0 F=403  case XML_PARSER_ENTITY_DECL:
  d=3   L12065  T=0 F=21  T=0 F=403  case XML_PARSER_ENTITY_VALUE:
  d=3   L12074  T=0 F=21  T=0 F=403  case XML_PARSER_ATTRIBUTE_VALUE:
  d=3   L12083  T=0 F=21  T=0 F=403  case XML_PARSER_SYSTEM_LITERAL:
  d=3   L12092  T=0 F=21  T=0 F=403  case XML_PARSER_PUBLIC_LITERAL:
--- d=2  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=2   L7181  T=0 F=3  T=0 F=167  if (RAW != '&')
  d=2   L7187  T=0 F=3  T=0 F=167  if (NXT(1) == '#') {
  d=2   L7233  T=3 F=0  T=167 F=0  if (ent == NULL) return;
--- d=1  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769) ---
  d=1   L7624  T=0 F=3  T=0 F=167  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L7627  T=0 F=3  T=0 F=167  if (RAW != '&')
  d=1   L7631  T=0 F=3  T=79 F=88  if (name == NULL) {
  d=1   L7636  T=0 F=3  T=2 F=86  if (RAW != ';') {
  d=1   L7645  T=3 F=0  T=77 F=9  if ((ctxt->options & XML_PARSE_OLDSAX) == 0) {
  d=1   L7647  T=0 F=3  T=0 F=77  if (ent != NULL)
  d=1   L7655  T=3 F=0  T=86 F=0  if (ctxt->sax != NULL) {
  d=1   L7656  T=3 F=0  T=86 F=0  if (ctxt->sax->getEntity != NULL)
  d=1   L7658  T=3 F=0  T=0 F=86  if ((ctxt->wellFormed == 1 ) && (ent == NULL) &&  <-- BLOCKER
  d=1   L7658  T=3 F=0  T=0 F=0  if ((ctxt->wellFormed == 1 ) && (ent == NULL) &&  <-- BLOCKER
  d=1   L7659  T=0 F=3  T=0 F=0  (ctxt->options & XML_PARSE_OLDSAX))
  d=1   L7661  T=3 F=0  T=0 F=86  if ((ctxt->wellFormed == 1 ) && (ent == NULL) &&
  d=1   L7661  T=3 F=0  T=0 F=0  if ((ctxt->wellFormed == 1 ) && (ent == NULL) &&
  d=1   L7662  T=3 F=0  T=0 F=0  (ctxt->userData==ctxt)) {
  d=1   L7666  T=0 F=3  T=0 F=86  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L7689  T=3 F=0  T=86 F=0  if (ent == NULL) {
  d=1   L7690  T=0 F=3  T=0 F=86  if ((ctxt->standalone == 1) ||
  d=1   L7691  T=0 F=3  T=12 F=74  ((ctxt->hasExternalSubset == 0) &&
  d=1   L7692  T=0 F=0  T=12 F=0  (ctxt->hasPErefs == 0))) {
  d=1   L7698  T=3 F=0  T=74 F=0  if ((ctxt->inSubset == 0) &&
  d=1   L7699  T=3 F=0  T=74 F=0  (ctxt->sax != NULL) &&
  d=1   L7700  T=3 F=0  T=74 F=0  (ctxt->sax->reference != NULL)) {

[off-chain: 537 additional divergent branches across 56 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=339ba30b2f9d5965, size=385 bytes, fuzzer=cmplog, trial=1, discovered_at=4379s, mutation_op=BytesDeleteMutator,ByteAddMutator):
  0000: 81 81 81 81 81 81 81 81 81 81 2e 78 6d 6c 5c 0a   ...........xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=38501a99c7a866aa, size=386 bytes, fuzzer=naive, trial=1, discovered_at=5008s, mutation_op=BytesInsertCopyMutator,QwordAddMutator,BytesInsertMutator,DwordAddMutator):
  0000: 3d 06 00 00 00 31 32 37 37 33 32 2e 78 6d 6c 5c   =....127732.xml\
  0010: 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22   .<?xml version="
  0020: 47 2e 22 64 74 64 73 2f 31 32 37 6b 65 75 72 6c   G."dtds/127keurl
  0030: 2e 6e 22 3e 0a 0a 3c 61 3e 0a 20 20 3c 64 64 64   .n">..<a>.  <ddd
Seed 2 (id=fa1197ec4c86a140, size=405 bytes, fuzzer=naive, trial=1, discovered_at=12585s, mutation_op=BytesRandSetMutator,TokenReplace,CrossoverReplaceMutator,BytesRandInsertMutator):
  0000: 45 4d 45 3d 06 00 00 00 31 32 37 37 33 32 2e 78   EME=....127732.x
  0010: 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f   ml\.<?xml versio
  0020: 6e 3d 22 47 2e 22 64 74 64 73 2f 31 32 37 6b 65   n="G."dtds/127ke
  0030: 75 72 6c 2e 6e 22 3e 0a 0a 3c 61 3e 0a 20 20 3c   url.n">..<a>.  <
Seed 3 (id=c4db5506cfb84099, size=258 bytes, fuzzer=naive, trial=1, discovered_at=62229s, mutation_op=BytesExpandMutator,CrossoverInsertMutator,BytesCopyMutator):
  0000: 5f 5f 5f 5f 77 75 06 00 00 00 31 32 37 37 37 32   ____wu....127772
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
Seed 4 (id=793608322986bf11, size=270 bytes, fuzzer=naive, trial=1, discovered_at=70094s, mutation_op=ByteInterestingMutator,ByteInterestingMutator,BytesCopyMutator):
  0000: 5f 10 00 5f 77 75 06 00 00 00 31 32 37 37 37 32   _.._wu....127772
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
Seed 5 (id=a56fdc38f3fdbfcb, size=257 bytes, fuzzer=naive, trial=1, discovered_at=70112s, mutation_op=WordAddMutator,ByteNegMutator,DwordAddMutator):
  0000: 5f 10 00 5f 77 75 06 00 00 00 31 32 37 37 37 32   _.._wu....127772
  0010: 00 40 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .@ml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  81(.)x1                             5f(_)x4 3d(=)x1 45(E)x1             DIFFER
   0x0001  81(.)x1                             10(.)x3 06(.)x1 4d(M)x1 5f(_)x1     DIFFER
   0x0002  81(.)x1                             00(.)x4 45(E)x1 5f(_)x1             DIFFER
   0x0003  81(.)x1                             5f(_)x4 00(.)x1 3d(=)x1             DIFFER
   0x0004  81(.)x1                             77(w)x4 00(.)x1 06(.)x1             DIFFER
   0x0005  81(.)x1                             75(u)x4 31(1)x1 00(.)x1             DIFFER
   0x0006  81(.)x1                             06(.)x3 32(2)x1 00(.)x1 9b(.)x1     DIFFER
   0x0007  81(.)x1                             00(.)x4 37(7)x1 ff(.)x1             DIFFER
   0x0008  81(.)x1                             00(.)x3 37(7)x1 31(1)x1 ff(.)x1     DIFFER
   0x0009  81(.)x1                             00(.)x3 33(3)x1 32(2)x1 ff(.)x1     DIFFER
   0x000a  2e(.)x1                             31(1)x4 32(2)x1 37(7)x1             DIFFER
   0x000b  78(x)x1                             32(2)x4 2e(.)x1 37(7)x1             DIFFER
   0x000c  6d(m)x1                             37(7)x4 78(x)x1 33(3)x1             DIFFER
   0x000d  6c(l)x1                             37(7)x4 6d(m)x1 32(2)x1             DIFFER
   0x000e  5c(\)x1                             37(7)x4 6c(l)x1 2e(.)x1             DIFFER
   0x000f  0a(.)x1                             32(2)x4 5c(\)x1 78(x)x1             DIFFER
   0x0010  3c(<)x1                             2e(.)x2 00(.)x2 0a(.)x1 6d(m)x1     DIFFER
   0x0011  3f(?)x1                             78(x)x2 40(@)x2 3c(<)x1 6c(l)x1     DIFFER
   0x0012  78(x)x1                             6d(m)x4 3f(?)x1 5c(\)x1             DIFFER
   0x0013  6d(m)x1                             6c(l)x4 78(x)x1 0a(.)x1             DIFFER
   0x0014  6c(l)x1                             5c(\)x4 6d(m)x1 3c(<)x1             DIFFER
   0x0015  20( )x1                             0a(.)x4 6c(l)x1 3f(?)x1             DIFFER
   0x0016  76(v)x1                             3c(<)x4 20( )x1 78(x)x1             DIFFER
   0x0017  65(e)x1                             3f(?)x4 76(v)x1 6d(m)x1             DIFFER
   0x0018  72(r)x1                             78(x)x4 65(e)x1 6c(l)x1             DIFFER
   0x0019  73(s)x1                             6d(m)x4 72(r)x1 20( )x1             DIFFER
   0x001a  69(i)x1                             6c(l)x4 73(s)x1 76(v)x1             DIFFER
   0x001b  6f(o)x1                             20( )x4 69(i)x1 65(e)x1             DIFFER
   0x001c  6e(n)x1                             76(v)x4 6f(o)x1 72(r)x1             DIFFER
   0x001d  3d(=)x1                             65(e)x4 6e(n)x1 73(s)x1             DIFFER
   0x001e  22(")x1                             72(r)x4 3d(=)x1 69(i)x1             DIFFER
   0x001f  31(1)x1                             73(s)x4 22(")x1 6f(o)x1             DIFFER
   0x0020  2e(.)x1                             69(i)x4 47(G)x1 6e(n)x1             DIFFER
   0x0021  30(0)x1                             6f(o)x4 2e(.)x1 3d(=)x1             DIFFER
   0x0022  22(")x1                             6e(n)x4 22(")x2                     PARTIAL
   0x0023  3f(?)x1                             3d(=)x4 64(d)x1 47(G)x1             DIFFER
   0x0024  3e(>)x1                             22(")x4 74(t)x1 2e(.)x1             DIFFER
   0x0025  0a(.)x1                             31(1)x4 64(d)x1 22(")x1             DIFFER
   0x0026  3c(<)x1                             2e(.)x4 73(s)x1 64(d)x1             DIFFER
   0x0027  21(!)x1                             30(0)x4 2f(/)x1 74(t)x1             DIFFER
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

--- minimizer ---
**Instrumentation**: naive's edge counters only.

**Feedback**: naive's edge-bucket `MaxMapFeedback`, plus a
`CalibrationStage` that measures each new corpus entry's execution
time, edge-map fill, and stability into `SchedulerMetadata`/testcase
metadata.

**Mutators / stages**: havoc + token mutator (`LineageMutator`, names
captured) run inside a `StdPowerMutationalStage` rather than naive's
plain `StdMutationalStage`. Stages are `[calibration, power]`. The
power stage derives the number of havoc mutations per seed visit (the
"energy") from a calibration-based `perf_score` — faster, smaller,
more-stable seeds earn more mutations. PowerSchedule is `None`, so the
energy uses ONLY intrinsic calibration and is NOT weighted by how often
a region has been hit. Corpus selection is plain FIFO `QueueScheduler`
(same order as naive).

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge, plus a one-time
calibration burst per new corpus entry.

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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6690.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6690,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile>naive (value_profile), minimizer>naive (calibrated_energy)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6690 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6690 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6690 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).