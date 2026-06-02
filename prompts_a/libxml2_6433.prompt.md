==== BLOCKER ====
Target: libxml2
Branch ID: 6433
Location: /src/libxml2/parser.c:340:9
Enclosing function: parser.c:xmlFatalErr
Source line:         case XML_ERR_NMTOKEN_REQUIRED:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ctx_coverage vs naive_ctx)
cmplog                           7        3          0  REFERENCE
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     2        8          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        6        4          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.90h  loser=19.60h
  avg hitcount on branch: winner=9  loser=2
  prob_div=0.60  dur_div=7.70h  hit_div=7
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6433/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlFatalErr (/src/libxml2/parser.c:249-453) ---
[ ]   247  static void
[ ]   248  xmlFatalErr(xmlParserCtxtPtr ctxt, xmlParserErrors error, const char *info)
[B]   249  {
[B]   250      const char *errmsg;
[ ]   251  
[B]   252      if ((ctxt != NULL) && (ctxt->disableSAX != 0) &&
[B]   253          (ctxt->instate == XML_PARSER_EOF))
[ ]   254  	return;
[B]   255      switch (error) {
[ ]   256          case XML_ERR_INVALID_HEX_CHARREF:
[ ]   257              errmsg = "CharRef: invalid hexadecimal value";
[ ]   258              break;
[ ]   259          case XML_ERR_INVALID_DEC_CHARREF:
[ ]   260              errmsg = "CharRef: invalid decimal value";
[ ]   261              break;
[ ]   262          case XML_ERR_INVALID_CHARREF:
[ ]   263              errmsg = "CharRef: invalid value";
[ ]   264              break;
[L]   265          case XML_ERR_INTERNAL_ERROR:
[L]   266              errmsg = "internal error";
[L]   267              break;
[ ]   268          case XML_ERR_PEREF_AT_EOF:
[ ]   269              errmsg = "PEReference at end of document";
[ ]   270              break;
[ ]   271          case XML_ERR_PEREF_IN_PROLOG:
[ ]   272              errmsg = "PEReference in prolog";
[ ]   273              break;
[ ]   274          case XML_ERR_PEREF_IN_EPILOG:
[ ]   275              errmsg = "PEReference in epilog";
[ ]   276              break;
[ ]   277          case XML_ERR_PEREF_NO_NAME:
[ ]   278              errmsg = "PEReference: no name";
[ ]   279              break;
[W]   280          case XML_ERR_PEREF_SEMICOL_MISSING:
[W]   281              errmsg = "PEReference: expecting ';'";
[W]   282              break;
[ ]   283          case XML_ERR_ENTITY_LOOP:
[ ]   284              errmsg = "Detected an entity reference loop";
[ ]   285              break;
[ ]   286          case XML_ERR_ENTITY_NOT_STARTED:
[ ]   287              errmsg = "EntityValue: \" or ' expected";
[ ]   288              break;
[ ]   289          case XML_ERR_ENTITY_PE_INTERNAL:
[ ]   290              errmsg = "PEReferences forbidden in internal subset";
[ ]   291              break;
[ ]   292          case XML_ERR_ENTITY_NOT_FINISHED:
[ ]   293              errmsg = "EntityValue: \" or ' expected";
[ ]   294              break;
[ ]   295          case XML_ERR_ATTRIBUTE_NOT_STARTED:
[ ]   296              errmsg = "AttValue: \" or ' expected";
[ ]   297              break;
[ ]   298          case XML_ERR_LT_IN_ATTRIBUTE:
[ ]   299              errmsg = "Unescaped '<' not allowed in attributes values";
[ ]   300              break;
[ ]   301          case XML_ERR_LITERAL_NOT_STARTED:
[ ]   302              errmsg = "SystemLiteral \" or ' expected";
[ ]   303              break;
[ ]   304          case XML_ERR_LITERAL_NOT_FINISHED:
[ ]   305              errmsg = "Unfinished System or Public ID \" or ' expected";
[ ]   306              break;
[ ]   307          case XML_ERR_MISPLACED_CDATA_END:
[ ]   308              errmsg = "Sequence ']]>' not allowed in content";
[ ]   309              break;
[ ]   310          case XML_ERR_URI_REQUIRED:
[ ]   311              errmsg = "SYSTEM or PUBLIC, the URI is missing";
[ ]   312              break;
[ ]   313          case XML_ERR_PUBID_REQUIRED:
[ ]   314              errmsg = "PUBLIC, the Public Identifier is missing";
[ ]   315              break;
[ ]   316          case XML_ERR_HYPHEN_IN_COMMENT:
[ ]   317              errmsg = "Comment must not contain '--' (double-hyphen)";
[ ]   318              break;
[L]   319          case XML_ERR_PI_NOT_STARTED:
[L]   320              errmsg = "xmlParsePI : no target name";
[L]   321              break;
[ ]   322          case XML_ERR_RESERVED_XML_NAME:
[ ]   323              errmsg = "Invalid PI name";
[ ]   324              break;
[ ]   325          case XML_ERR_NOTATION_NOT_STARTED:
[ ]   326              errmsg = "NOTATION: Name expected here";
[ ]   327              break;
[ ]   328          case XML_ERR_NOTATION_NOT_FINISHED:
[ ]   329              errmsg = "'>' required to close NOTATION declaration";
[ ]   330              break;
[ ]   331          case XML_ERR_VALUE_REQUIRED:
[ ]   332              errmsg = "Entity value required";
[ ]   333              break;
[ ]   334          case XML_ERR_URI_FRAGMENT:
[ ]   335              errmsg = "Fragment not allowed";
[ ]   336              break;
[ ]   337          case XML_ERR_ATTLIST_NOT_STARTED:
[ ]   338              errmsg = "'(' required to start ATTLIST enumeration";
[ ]   339              break;
[W]   340          case XML_ERR_NMTOKEN_REQUIRED: <-- BLOCKER
[W]   341              errmsg = "NmToken expected in ATTLIST enumeration";
[W]   342              break;
[ ]   343          case XML_ERR_ATTLIST_NOT_FINISHED:
[ ]   344              errmsg = "')' required to finish ATTLIST enumeration";
[ ]   345              break;
[ ]   346          case XML_ERR_MIXED_NOT_STARTED:
[ ]   347              errmsg = "MixedContentDecl : '|' or ')*' expected";
[ ]   348              break;
[ ]   349          case XML_ERR_PCDATA_REQUIRED:
[ ]   350              errmsg = "MixedContentDecl : '#PCDATA' expected";
[ ]   351              break;
[ ]   352          case XML_ERR_ELEMCONTENT_NOT_STARTED:
[ ]   353              errmsg = "ContentDecl : Name or '(' expected";
[ ]   354              break;
[W]   355          case XML_ERR_ELEMCONTENT_NOT_FINISHED:
[W]   356              errmsg = "ContentDecl : ',' '|' or ')' expected";
[W]   357              break;
[ ]   358          case XML_ERR_PEREF_IN_INT_SUBSET:
[ ]   359              errmsg =
[ ]   360                  "PEReference: forbidden within markup decl in internal subset";
[ ]   361              break;
[B]   362          case XML_ERR_GT_REQUIRED:
[B]   363              errmsg = "expected '>'";
[B]   364              break;
[ ]   365          case XML_ERR_CONDSEC_INVALID:
[ ]   366              errmsg = "XML conditional section '[' expected";
[ ]   367              break;
[W]   368          case XML_ERR_EXT_SUBSET_NOT_FINISHED:
[W]   369              errmsg = "Content error in the external subset";
[W]   370              break;
[ ]   371          case XML_ERR_CONDSEC_INVALID_KEYWORD:
[ ]   372              errmsg =
[ ]   373                  "conditional section INCLUDE or IGNORE keyword expected";
[ ]   374              break;
[ ]   375          case XML_ERR_CONDSEC_NOT_FINISHED:
[ ]   376              errmsg = "XML conditional section not closed";
[ ]   377              break;
[ ]   378          case XML_ERR_XMLDECL_NOT_STARTED:
[ ]   379              errmsg = "Text declaration '<?xml' required";
[ ]   380              break;
[L]   381          case XML_ERR_XMLDECL_NOT_FINISHED:
[L]   382              errmsg = "parsing XML declaration: '?>' expected";
[L]   383              break;
[ ]   384          case XML_ERR_EXT_ENTITY_STANDALONE:
[ ]   385              errmsg = "external parsed entities cannot be standalone";
[ ]   386              break;
[L]   387          case XML_ERR_ENTITYREF_SEMICOL_MISSING:
[L]   388              errmsg = "EntityRef: expecting ';'";
[L]   389              break;
[L]   390          case XML_ERR_DOCTYPE_NOT_FINISHED:
[L]   391              errmsg = "DOCTYPE improperly terminated";
[L]   392              break;
[ ]   393          case XML_ERR_LTSLASH_REQUIRED:
[ ]   394              errmsg = "EndTag: '</' not found";
[ ]   395              break;
[ ]   396          case XML_ERR_EQUAL_REQUIRED:
[ ]   397              errmsg = "expected '='";
[ ]   398              break;
[ ]   399          case XML_ERR_STRING_NOT_CLOSED:
[ ]   400              errmsg = "String not closed expecting \" or '";
[ ]   401              break;
[ ]   402          case XML_ERR_STRING_NOT_STARTED:
[ ]   403              errmsg = "String not started expecting ' or \"";
[ ]   404              break;
[ ]   405          case XML_ERR_ENCODING_NAME:
[ ]   406              errmsg = "Invalid XML encoding name";
[ ]   407              break;
[ ]   408          case XML_ERR_STANDALONE_VALUE:
[ ]   409              errmsg = "standalone accepts only 'yes' or 'no'";
[ ]   410              break;
[L]   411          case XML_ERR_DOCUMENT_EMPTY:
[L]   412              errmsg = "Document is empty";
[L]   413              break;
[L]   414          case XML_ERR_DOCUMENT_END:
[L]   415              errmsg = "Extra content at the end of the document";
[L]   416              break;
[ ]   417          case XML_ERR_NOT_WELL_BALANCED:
[ ]   418              errmsg = "chunk is not well balanced";
[ ]   419              break;
[ ]   420          case XML_ERR_EXTRA_CONTENT:
[ ]   421              errmsg = "extra content at the end of well balanced chunk";
[ ]   422              break;
[L]   423          case XML_ERR_VERSION_MISSING:
[L]   424              errmsg = "Malformed declaration expecting version";
[L]   425              break;
[ ]   426          case XML_ERR_NAME_TOO_LONG:
[ ]   427              errmsg = "Name too long";
[ ]   428              break;
[ ]   429  #if 0
[ ]   430          case:
[ ]   431              errmsg = "";
[ ]   432              break;
[ ]   433  #endif
[ ]   434          default:
[ ]   435              errmsg = "Unregistered error message";
[B]   436      }
[B]   437      if (ctxt != NULL)
[B]   438  	ctxt->errNo = error;
[B]   439      if (info == NULL) {
[B]   440          __xmlRaiseError(NULL, NULL, NULL, ctxt, NULL, XML_FROM_PARSER, error,
[B]   441                          XML_ERR_FATAL, NULL, 0, info, NULL, NULL, 0, 0, "%s\n",
[B]   442                          errmsg);
[B]   443      } else {
[L]   444          __xmlRaiseError(NULL, NULL, NULL, ctxt, NULL, XML_FROM_PARSER, error,
[L]   445                          XML_ERR_FATAL, NULL, 0, info, NULL, NULL, 0, 0, "%s: %s\n",
[L]   446                          errmsg, info);
[L]   447      }
[B]   448      if (ctxt != NULL) {
[B]   449  	ctxt->wellFormed = 0;
[B]   450  	if (ctxt->recovery == 0)
[B]   451  	    ctxt->disableSAX = 1;
[B]   452      }
[B]   453  }

--- Caller (1 hop): xmlParseEnumerationType (/src/libxml2/parser.c:5879-5930, calls parser.c:xmlFatalErr at line 5893) (±10 around call site) ---
[W]  5883      if (RAW != '(') {
[ ]  5884  	xmlFatalErr(ctxt, XML_ERR_ATTLIST_NOT_STARTED, NULL);
[ ]  5885  	return(NULL);
[ ]  5886      }
[W]  5887      SHRINK;
[W]  5888      do {
[W]  5889          NEXT;
[W]  5890  	SKIP_BLANKS;
[W]  5891          name = xmlParseNmtoken(ctxt);
[W]  5892  	if (name == NULL) {
[W]  5893  	    xmlFatalErr(ctxt, XML_ERR_NMTOKEN_REQUIRED, NULL); <-- CALL
[W]  5894  	    return(ret);
[W]  5895  	}
[W]  5896  	tmp = ret;
[W]  5897  	while (tmp != NULL) {
[ ]  5898  	    if (xmlStrEqual(name, tmp->name)) {
[ ]  5899  		xmlValidityError(ctxt, XML_DTD_DUP_TOKEN,
[ ]  5900  	  "standalone: attribute enumeration value token %s duplicated\n",
[ ]  5901  				 name, NULL);
[ ]  5902  		if (!xmlDictOwns(ctxt->dict, name))
[ ]  5903  		    xmlFree(name);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094, calls parser.c:xmlFatalErr at line 2081)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1640      9480  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
       9       417  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
      90       447  inputPop  (/src/libxml2/parser.c:1723-1738)
       0       267  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706)
       0       229  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942)
      69       286  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)  <-- enclosing
      30       214  xmlParseChunk  (/src/libxml2/parser.c:12135-12300)
      45       226  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
       6       169  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
      48       211  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       6       164  parser.c:xmlParseLookupCharData  (/src/libxml2/parser.c:11170-11184)
      21       179  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120)
       0       155  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
       0       145  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
       0       144  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
... (61 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094) ---
  d=2   L2076  T=0 F=1800  T=0 F=660  if (((curEnd > XML_MAX_LOOKUP_LIMIT) ||
  d=2   L2077  T=0 F=1800  T=0 F=660  (curBase > XML_MAX_LOOKUP_LIMIT)) &&
  d=2   L2086  T=0 F=1800  T=0 F=660  if ((ctxt->input->cur > ctxt->input->end) ||
  d=2   L2087  T=0 F=1800  T=0 F=660  (ctxt->input->cur < ctxt->input->base)) {
  d=2   L2092  T=1800 F=0  T=660 F=0  if ((ctxt->input->cur != NULL) && (*ctxt->input->cur == 0))
  d=2   L2092  T=4 F=1800  T=39 F=621  if ((ctxt->input->cur != NULL) && (*ctxt->input->cur == 0))
--- d=1  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453) ---
  d=1   L 252  T=48 F=21  T=21 F=265  if ((ctxt != NULL) && (ctxt->disableSAX != 0) &&
  d=1   L 252  T=69 F=0  T=286 F=0  if ((ctxt != NULL) && (ctxt->disableSAX != 0) &&
  d=1   L 253  T=0 F=48  T=0 F=21  (ctxt->instate == XML_PARSER_EOF))
  d=1   L 256  T=0 F=69  T=0 F=286  case XML_ERR_INVALID_HEX_CHARREF:
  d=1   L 259  T=0 F=69  T=0 F=286  case XML_ERR_INVALID_DEC_CHARREF:
  d=1   L 262  T=0 F=69  T=0 F=286  case XML_ERR_INVALID_CHARREF:
  d=1   L 265  T=0 F=69  T=26 F=260  case XML_ERR_INTERNAL_ERROR:
  d=1   L 268  T=0 F=69  T=0 F=286  case XML_ERR_PEREF_AT_EOF:
  d=1   L 271  T=0 F=69  T=0 F=286  case XML_ERR_PEREF_IN_PROLOG:
  d=1   L 274  T=0 F=69  T=0 F=286  case XML_ERR_PEREF_IN_EPILOG:
  d=1   L 277  T=0 F=69  T=0 F=286  case XML_ERR_PEREF_NO_NAME:
  d=1   L 280  T=6 F=63  T=0 F=286  case XML_ERR_PEREF_SEMICOL_MISSING:
  d=1   L 283  T=0 F=69  T=0 F=286  case XML_ERR_ENTITY_LOOP:
  d=1   L 286  T=0 F=69  T=0 F=286  case XML_ERR_ENTITY_NOT_STARTED:
  d=1   L 289  T=0 F=69  T=0 F=286  case XML_ERR_ENTITY_PE_INTERNAL:
  d=1   L 292  T=0 F=69  T=0 F=286  case XML_ERR_ENTITY_NOT_FINISHED:
  d=1   L 295  T=0 F=69  T=0 F=286  case XML_ERR_ATTRIBUTE_NOT_STARTED:
  d=1   L 298  T=0 F=69  T=0 F=286  case XML_ERR_LT_IN_ATTRIBUTE:
  d=1   L 301  T=0 F=69  T=0 F=286  case XML_ERR_LITERAL_NOT_STARTED:
  d=1   L 304  T=0 F=69  T=0 F=286  case XML_ERR_LITERAL_NOT_FINISHED:
  d=1   L 307  T=0 F=69  T=0 F=286  case XML_ERR_MISPLACED_CDATA_END:
  d=1   L 310  T=0 F=69  T=0 F=286  case XML_ERR_URI_REQUIRED:
  d=1   L 313  T=0 F=69  T=0 F=286  case XML_ERR_PUBID_REQUIRED:
  d=1   L 316  T=0 F=69  T=0 F=286  case XML_ERR_HYPHEN_IN_COMMENT:
  d=1   L 319  T=0 F=69  T=3 F=283  case XML_ERR_PI_NOT_STARTED:
  d=1   L 322  T=0 F=69  T=0 F=286  case XML_ERR_RESERVED_XML_NAME:
  d=1   L 325  T=0 F=69  T=0 F=286  case XML_ERR_NOTATION_NOT_STARTED:
  d=1   L 328  T=0 F=69  T=0 F=286  case XML_ERR_NOTATION_NOT_FINISHED:
  d=1   L 331  T=0 F=69  T=0 F=286  case XML_ERR_VALUE_REQUIRED:
  d=1   L 334  T=0 F=69  T=0 F=286  case XML_ERR_URI_FRAGMENT:
  d=1   L 337  T=0 F=69  T=0 F=286  case XML_ERR_ATTLIST_NOT_STARTED:
  d=1   L 340  T=30 F=39  T=0 F=286  case XML_ERR_NMTOKEN_REQUIRED:  <-- BLOCKER
  d=1   L 343  T=0 F=69  T=0 F=286  case XML_ERR_ATTLIST_NOT_FINISHED:
  d=1   L 346  T=0 F=69  T=0 F=286  case XML_ERR_MIXED_NOT_STARTED:
  d=1   L 349  T=0 F=69  T=0 F=286  case XML_ERR_PCDATA_REQUIRED:
  d=1   L 352  T=0 F=69  T=0 F=286  case XML_ERR_ELEMCONTENT_NOT_STARTED:
  d=1   L 355  T=3 F=66  T=0 F=286  case XML_ERR_ELEMCONTENT_NOT_FINISHED:
  d=1   L 358  T=0 F=69  T=0 F=286  case XML_ERR_PEREF_IN_INT_SUBSET:
  d=1   L 362  T=3 F=66  T=26 F=260  case XML_ERR_GT_REQUIRED:
  d=1   L 365  T=0 F=69  T=0 F=286  case XML_ERR_CONDSEC_INVALID:
  d=1   L 368  T=27 F=42  T=0 F=286  case XML_ERR_EXT_SUBSET_NOT_FINISHED:
  d=1   L 371  T=0 F=69  T=0 F=286  case XML_ERR_CONDSEC_INVALID_KEYWORD:
  d=1   L 375  T=0 F=69  T=0 F=286  case XML_ERR_CONDSEC_NOT_FINISHED:
  d=1   L 378  T=0 F=69  T=0 F=286  case XML_ERR_XMLDECL_NOT_STARTED:
  d=1   L 381  T=0 F=69  T=15 F=271  case XML_ERR_XMLDECL_NOT_FINISHED:
  d=1   L 384  T=0 F=69  T=0 F=286  case XML_ERR_EXT_ENTITY_STANDALONE:
  d=1   L 387  T=0 F=69  T=106 F=180  case XML_ERR_ENTITYREF_SEMICOL_MISSING:
  d=1   L 390  T=0 F=69  T=6 F=280  case XML_ERR_DOCTYPE_NOT_FINISHED:
  d=1   L 393  T=0 F=69  T=0 F=286  case XML_ERR_LTSLASH_REQUIRED:
  d=1   L 396  T=0 F=69  T=0 F=286  case XML_ERR_EQUAL_REQUIRED:
  d=1   L 399  T=0 F=69  T=0 F=286  case XML_ERR_STRING_NOT_CLOSED:
  d=1   L 402  T=0 F=69  T=0 F=286  case XML_ERR_STRING_NOT_STARTED:
  d=1   L 405  T=0 F=69  T=0 F=286  case XML_ERR_ENCODING_NAME:
  d=1   L 408  T=0 F=69  T=0 F=286  case XML_ERR_STANDALONE_VALUE:
  d=1   L 411  T=0 F=69  T=36 F=250  case XML_ERR_DOCUMENT_EMPTY:
  d=1   L 414  T=0 F=69  T=53 F=233  case XML_ERR_DOCUMENT_END:
  d=1   L 417  T=0 F=69  T=0 F=286  case XML_ERR_NOT_WELL_BALANCED:
  d=1   L 420  T=0 F=69  T=0 F=286  case XML_ERR_EXTRA_CONTENT:
  d=1   L 423  T=0 F=69  T=15 F=271  case XML_ERR_VERSION_MISSING:
  d=1   L 426  T=0 F=69  T=0 F=286  case XML_ERR_NAME_TOO_LONG:
  d=1   L 434  T=0 F=69  T=0 F=286  default:
  d=1   L 437  T=69 F=0  T=286 F=0  if (ctxt != NULL)
  d=1   L 439  T=69 F=0  T=260 F=26  if (info == NULL) {
  d=1   L 448  T=69 F=0  T=286 F=0  if (ctxt != NULL) {
  d=1   L 450  T=54 F=15  T=51 F=235  if (ctxt->recovery == 0)

[off-chain: 995 additional divergent branches across 85 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=00ea7e66e00573c5, size=519 bytes, fuzzer=naive_ctx, trial=1, discovered_at=0s, mutation_op=BytesExpandMutator,CrossoverInsertMutator,ByteNegMutator,BytesSetMutator,BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=adf73de9c553f571, size=756 bytes, fuzzer=naive_ctx, trial=1, discovered_at=712s, mutation_op=BytesCopyMutator,TokenReplace,ByteInterestingMutator,TokenInsert):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 06 00 00 00 31   ....127772.....1
  0010: 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c   27772.xml\.<?xml
  0020: 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e    version="1.0"?>
  0030: 0a 3c 21 44 4f 43 54 59 50 45 42 61 20 53 59 53   .<!DOCTYPEBa SYS
Seed 3 (id=7e5b8381a25e9da7, size=293 bytes, fuzzer=naive_ctx, trial=1, discovered_at=1219s, mutation_op=BytesDeleteMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
Seed 4 (id=5490d017a729e344, size=782 bytes, fuzzer=naive_ctx, trial=1, discovered_at=2627s, mutation_op=CrossoverInsertMutator,TokenReplace,BytesInsertCopyMutator,BytesRandSetMutator):
  0000: 06 00 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 5c 0a   ..............\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 42   .0"?>.<!DOCTYPEB
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=a04d19468f4fe66a, size=348 bytes, fuzzer=naive_ctx, trial=1, discovered_at=3528s, mutation_op=TokenReplace,ByteInterestingMutator,BytesSetMutator,DwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=000a8afebd4fd850, size=474 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=BytesSwapMutator,TokenReplace,BytesInsertCopyMutator,WordAddMutator,ByteInterestingMutator,ByteNegMutator,ByteIncMutator):
  0000: 4d 20 ff ff 74 64 73 2f 31 32 37 37 06 00 00 00   M ..tds/1277....
  0010: 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   127772.xml\.<?xm
  0020: 6c 20 76 65 72 41 53 43 49 49 22 31 2e 30 22 3f   l verASCII"1.0"?
  0030: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
Seed 2 (id=00269ca53cdf3bb2, size=119 bytes, fuzzer=naive, trial=2, discovered_at=1s, mutation_op=ByteDecMutator,DwordAddMutator,DwordInterestingMutator,BytesDeleteMutator):
  0000: 57 57 00 00 b1 32 37 37 37 32 2e 78 6d 6c 5c 0a   WW...27772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=0021f7e4ee3cbf8b, size=379 bytes, fuzzer=naive, trial=3, discovered_at=22s, mutation_op=WordInterestingMutator,WordInterestingMutator,ByteInterestingMutator,BytesDeleteMutator,CrossoverInsertMutator,BytesDeleteMutator):
  0000: 3a 2f 2f 66 61 6b 65 40 72 6c 2e 20 28 23 50 43   ://fake@rl. (#PC
  0010: 44 41 54 41 29 3e 0a 3c 21 41 54 54 4c 49 53 54   DATA)>.<!ATTLIST
  0020: 20 62 20 78 6d 94 6e 73 3a 78 6c 69 6e 6b 20 20    b xm.ns:xlink  
  0030: 43 44 41 54 41 20 20 20 20 20 23 46 49 58 45 44   CDATA     #FIXED
Seed 4 (id=0023aedf54362876, size=518 bytes, fuzzer=naive, trial=4, discovered_at=26s, mutation_op=BytesSetMutator,ByteIncMutator,CrossoverInsertMutator):
  0000: 01 00 70 3a 2f 2f 66 32 2e 64 74 64 5c 0a 3c 21   ..p://f2.dtd\.<!
  0010: 45 4c 45 4d 45 4e 54 20 61 20 28 62 2a 29 3e 0a   ELEMENT a (b*)>.
  0020: 0a 3c 21 45 4c 45 4d 45 4d 54 20 62 20 28 23 50   .<!ELEMEMT b (#P
  0030: 43 44 41 54 41 29 3e 0a 3c 21 41 54 54 4c 49 53   CDATA)>.<!ATTLIS
Seed 5 (id=001a7028635fd9f5, size=330 bytes, fuzzer=naive, trial=1, discovered_at=37s, mutation_op=BytesDeleteMutator,WordInterestingMutator,ByteNegMutator,BytesRandSetMutator):
  0000: 27 0a db db db 20 20 20 20 20 20 20 20 20 78 6c   '....         xl
  0010: 69 6e 6b 3a 74 79 70 65 20 20 20 28 73 69 6d 70   ink:type   (simp
  0020: 6c 65 29 20 20 23 46 49 58 45 44 20 27 73 69 6d   le)  #FIXED 'sim
  0030: e8 03 00 00 0a 20 20 20 20 20 20 20 20 20 20 20   .....           


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  32(2)x7 6c(l)x1 a3(.)x1 78(x)x1     70(p)x12 74(t)x9 32(2)x4 2f(/)x4 +18u  PARTIAL
   0x001a  69(i)x6 22(")x2 0a(.)x1 2e(.)x1     2e(.)x5 69(i)x3 45(E)x3 28(()x2 +32u  PARTIAL
   0x001e  22(")x7 6d(m)x1 3c(<)x1 3e(>)x1     2e(.)x5 22(")x4 6d(m)x3 29())x3 +31u  PARTIAL
   0x0029  4f(O)x6 20( )x2 22(")x1 50(P)x1     2f(/)x5 4f(O)x3 45(E)x3 78(x)x2 +33u  PARTIAL
   0x002b  54(T)x6 20( )x2 2e(.)x1 59(Y)x1     54(T)x4 20( )x4 2f(/)x4 2e(.)x4 +28u  PARTIAL
   0x002c  59(Y)x6 53(S)x2 30(0)x1 61(a)x1     2e(.)x4 59(Y)x4 20( )x4 27(')x3 +28u  PARTIAL
   0x002e  45(E)x7 53(S)x2 3f(?)x1             45(E)x4 20( )x4 3e(>)x3 23(#)x2 +33u  PARTIAL
   0x0034  53(S)x6 64(d)x2 4f(O)x1 20( )x1     53(S)x3 64(d)x3 21(!)x3 44(D)x2 +30u  PARTIAL
   0x0036  45(E)x6 64(d)x2 54(T)x1 2f(/)x1     20( )x5 45(E)x4 2f(/)x3 73(s)x3 +27u  PARTIAL
   0x003b  74(t)x6 37(7)x2 61(a)x1 31(1)x1     20( )x7 74(t)x5 2e(.)x5 37(7)x3 +23u  PARTIAL
   0x003c  64(d)x6 32(2)x2 20( )x1 37(7)x1     20( )x6 61(a)x4 64(d)x4 2f(/)x4 +23u  PARTIAL
   0x003d  73(s)x6 37(7)x2 53(S)x1 2e(.)x1     20( )x5 73(s)x3 32(2)x3 2f(/)x3 +27u  PARTIAL
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

--- naive_ctx ---
**Instrumentation**: naive's SanitizerCoverage edge counters, but the
executor installs a `CtxHook` (`HookableInProcessExecutor`). The hook
keeps a running hash of the current call context (caller chain) and
folds it into the edge-map index, so the same basic-block edge is
recorded at different map slots depending on the call path that
reached it.

**Feedback**: the same `MaxMapFeedback` edge-bucket signal as naive,
computed over the context-indexed map — a "new bucket" is a new
(call-context, edge) pair rather than a bare edge.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`, no
CMP_MAP. Stages are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no ParentInfo-only / dash rows.

**Per-execution cost**: one edge-counter increment per executed edge
plus a context-hash update per call/return.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6433.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6433,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6433 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6433 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6433 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).