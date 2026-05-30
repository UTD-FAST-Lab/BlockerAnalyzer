==== BLOCKER ====
Target: libxml2
Branch ID: 6436
Location: /src/libxml2/parser.c:371:9
Enclosing function: parser.c:xmlFatalErr
Source line:         case XML_ERR_CONDSEC_INVALID_KEYWORD:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile)
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog)
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.80h  loser=19.20h
  avg hitcount on branch: winner=5  loser=1
  prob_div=0.60  dur_div=7.40h  hit_div=4
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.20h  loser=20.10h
  avg hitcount on branch: winner=4  loser=1
  prob_div=0.60  dur_div=8.90h  hit_div=4
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6436/{W,L}/branch_coverage_show.txt

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
[ ]   280          case XML_ERR_PEREF_SEMICOL_MISSING:
[ ]   281              errmsg = "PEReference: expecting ';'";
[ ]   282              break;
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
[W]   298          case XML_ERR_LT_IN_ATTRIBUTE:
[W]   299              errmsg = "Unescaped '<' not allowed in attributes values";
[W]   300              break;
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
[ ]   340          case XML_ERR_NMTOKEN_REQUIRED:
[ ]   341              errmsg = "NmToken expected in ATTLIST enumeration";
[ ]   342              break;
[ ]   343          case XML_ERR_ATTLIST_NOT_FINISHED:
[ ]   344              errmsg = "')' required to finish ATTLIST enumeration";
[ ]   345              break;
[ ]   346          case XML_ERR_MIXED_NOT_STARTED:
[ ]   347              errmsg = "MixedContentDecl : '|' or ')*' expected";
[ ]   348              break;
[ ]   349          case XML_ERR_PCDATA_REQUIRED:
[ ]   350              errmsg = "MixedContentDecl : '#PCDATA' expected";
[ ]   351              break;
[L]   352          case XML_ERR_ELEMCONTENT_NOT_STARTED:
[L]   353              errmsg = "ContentDecl : Name or '(' expected";
[L]   354              break;
[ ]   355          case XML_ERR_ELEMCONTENT_NOT_FINISHED:
[ ]   356              errmsg = "ContentDecl : ',' '|' or ')' expected";
[ ]   357              break;
[ ]   358          case XML_ERR_PEREF_IN_INT_SUBSET:
[ ]   359              errmsg =
[ ]   360                  "PEReference: forbidden within markup decl in internal subset";
[ ]   361              break;
[L]   362          case XML_ERR_GT_REQUIRED:
[L]   363              errmsg = "expected '>'";
[L]   364              break;
[ ]   365          case XML_ERR_CONDSEC_INVALID:
[ ]   366              errmsg = "XML conditional section '[' expected";
[ ]   367              break;
[ ]   368          case XML_ERR_EXT_SUBSET_NOT_FINISHED:
[ ]   369              errmsg = "Content error in the external subset";
[ ]   370              break;
[W]   371          case XML_ERR_CONDSEC_INVALID_KEYWORD: <-- BLOCKER
[W]   372              errmsg =
[W]   373                  "conditional section INCLUDE or IGNORE keyword expected";
[W]   374              break;
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
[L]   399          case XML_ERR_STRING_NOT_CLOSED:
[L]   400              errmsg = "String not closed expecting \" or '";
[L]   401              break;
[L]   402          case XML_ERR_STRING_NOT_STARTED:
[L]   403              errmsg = "String not started expecting ' or \"";
[L]   404              break;
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

--- Caller (1 hop): parser.c:xmlParseConditionalSections (/src/libxml2/parser.c:6804-6923, calls parser.c:xmlFatalErr at line 6893) (±10 around call site) ---
[ ]  6883  		    xmlFatalErr(ctxt, XML_ERR_CONDSEC_NOT_FINISHED, NULL);
[ ]  6884                      goto error;
[ ]  6885  		}
[ ]  6886                  if (ctxt->input->id != id) {
[ ]  6887                      xmlFatalErrMsg(ctxt, XML_ERR_ENTITY_BOUNDARY,
[ ]  6888                                     "All markup of the conditional section is"
[ ]  6889                                     " not in the same entity\n");
[ ]  6890                  }
[ ]  6891                  SKIP(3);
[W]  6892              } else {
[W]  6893                  xmlFatalErr(ctxt, XML_ERR_CONDSEC_INVALID_KEYWORD, NULL); <-- CALL
[W]  6894                  xmlHaltParser(ctxt);
[W]  6895                  goto error;
[W]  6896              }
[W]  6897          } else if ((depth > 0) &&
[ ]  6898                     (RAW == ']') && (NXT(1) == ']') && (NXT(2) == '>')) {
[ ]  6899              depth--;
[ ]  6900              if (ctxt->input->id != inputIds[depth]) {
[ ]  6901                  xmlFatalErrMsg(ctxt, XML_ERR_ENTITY_BOUNDARY,
[ ]  6902                                 "All markup of the conditional section is not"
[ ]  6903                                 " in the same entity\n");

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094, calls parser.c:xmlFatalErr at line 2081)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     457     15000  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     268      1350  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
     301      1180  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      36       888  inputPop  (/src/libxml2/parser.c:1723-1738)
       0       474  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
      42       474  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      18       401  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)  <-- enclosing
      12       389  xmlParseChunk  (/src/libxml2/parser.c:12135-12300)
       0       332  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706)
      24       338  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
       8       313  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120)
       6       299  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      12       296  parser.c:xmlCtxtUseOptionsInternal  (/src/libxml2/parser.c:14842-14969)
      24       302  inputPush  (/src/libxml2/parser.c:1693-1712)
       0       245  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942)
... (64 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094) ---
  d=2   L2076  T=0 F=301  T=0 F=1180  if (((curEnd > XML_MAX_LOOKUP_LIMIT) ||
  d=2   L2077  T=0 F=301  T=0 F=1180  (curBase > XML_MAX_LOOKUP_LIMIT)) &&
  d=2   L2086  T=0 F=301  T=0 F=1180  if ((ctxt->input->cur > ctxt->input->end) ||
  d=2   L2087  T=0 F=301  T=0 F=1180  (ctxt->input->cur < ctxt->input->base)) {
  d=2   L2092  T=301 F=0  T=1180 F=0  if ((ctxt->input->cur != NULL) && (*ctxt->input->cur == 0))
  d=2   L2092  T=0 F=301  T=79 F=1100  if ((ctxt->input->cur != NULL) && (*ctxt->input->cur == 0))
--- d=1  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453) ---
  d=1   L 252  T=9 F=9  T=60 F=341  if ((ctxt != NULL) && (ctxt->disableSAX != 0) &&
  d=1   L 252  T=18 F=0  T=401 F=0  if ((ctxt != NULL) && (ctxt->disableSAX != 0) &&
  d=1   L 253  T=0 F=9  T=0 F=60  (ctxt->instate == XML_PARSER_EOF))
  d=1   L 256  T=0 F=18  T=0 F=401  case XML_ERR_INVALID_HEX_CHARREF:
  d=1   L 259  T=0 F=18  T=0 F=401  case XML_ERR_INVALID_DEC_CHARREF:
  d=1   L 262  T=0 F=18  T=0 F=401  case XML_ERR_INVALID_CHARREF:
  d=1   L 265  T=0 F=18  T=35 F=366  case XML_ERR_INTERNAL_ERROR:
  d=1   L 268  T=0 F=18  T=0 F=401  case XML_ERR_PEREF_AT_EOF:
  d=1   L 271  T=0 F=18  T=0 F=401  case XML_ERR_PEREF_IN_PROLOG:
  d=1   L 274  T=0 F=18  T=0 F=401  case XML_ERR_PEREF_IN_EPILOG:
  d=1   L 277  T=0 F=18  T=0 F=401  case XML_ERR_PEREF_NO_NAME:
  d=1   L 280  T=0 F=18  T=0 F=401  case XML_ERR_PEREF_SEMICOL_MISSING:
  d=1   L 283  T=0 F=18  T=0 F=401  case XML_ERR_ENTITY_LOOP:
  d=1   L 286  T=0 F=18  T=0 F=401  case XML_ERR_ENTITY_NOT_STARTED:
  d=1   L 289  T=0 F=18  T=0 F=401  case XML_ERR_ENTITY_PE_INTERNAL:
  d=1   L 292  T=0 F=18  T=0 F=401  case XML_ERR_ENTITY_NOT_FINISHED:
  d=1   L 295  T=0 F=18  T=0 F=401  case XML_ERR_ATTRIBUTE_NOT_STARTED:
  d=1   L 298  T=6 F=12  T=0 F=401  case XML_ERR_LT_IN_ATTRIBUTE:
  d=1   L 301  T=0 F=18  T=0 F=401  case XML_ERR_LITERAL_NOT_STARTED:
  d=1   L 304  T=0 F=18  T=0 F=401  case XML_ERR_LITERAL_NOT_FINISHED:
  d=1   L 307  T=0 F=18  T=0 F=401  case XML_ERR_MISPLACED_CDATA_END:
  d=1   L 310  T=0 F=18  T=0 F=401  case XML_ERR_URI_REQUIRED:
  d=1   L 313  T=0 F=18  T=0 F=401  case XML_ERR_PUBID_REQUIRED:
  d=1   L 316  T=0 F=18  T=0 F=401  case XML_ERR_HYPHEN_IN_COMMENT:
  d=1   L 319  T=0 F=18  T=3 F=398  case XML_ERR_PI_NOT_STARTED:
  d=1   L 322  T=0 F=18  T=0 F=401  case XML_ERR_RESERVED_XML_NAME:
  d=1   L 325  T=0 F=18  T=0 F=401  case XML_ERR_NOTATION_NOT_STARTED:
  d=1   L 328  T=0 F=18  T=0 F=401  case XML_ERR_NOTATION_NOT_FINISHED:
  d=1   L 331  T=0 F=18  T=0 F=401  case XML_ERR_VALUE_REQUIRED:
  d=1   L 334  T=0 F=18  T=0 F=401  case XML_ERR_URI_FRAGMENT:
  d=1   L 337  T=0 F=18  T=0 F=401  case XML_ERR_ATTLIST_NOT_STARTED:
  d=1   L 340  T=0 F=18  T=0 F=401  case XML_ERR_NMTOKEN_REQUIRED:
  d=1   L 343  T=0 F=18  T=0 F=401  case XML_ERR_ATTLIST_NOT_FINISHED:
  d=1   L 346  T=0 F=18  T=0 F=401  case XML_ERR_MIXED_NOT_STARTED:
  d=1   L 349  T=0 F=18  T=0 F=401  case XML_ERR_PCDATA_REQUIRED:
  d=1   L 352  T=0 F=18  T=6 F=395  case XML_ERR_ELEMCONTENT_NOT_STARTED:
  d=1   L 355  T=0 F=18  T=0 F=401  case XML_ERR_ELEMCONTENT_NOT_FINISHED:
  d=1   L 358  T=0 F=18  T=0 F=401  case XML_ERR_PEREF_IN_INT_SUBSET:
  d=1   L 362  T=0 F=18  T=17 F=384  case XML_ERR_GT_REQUIRED:
  d=1   L 365  T=0 F=18  T=0 F=401  case XML_ERR_CONDSEC_INVALID:
  d=1   L 368  T=0 F=18  T=0 F=401  case XML_ERR_EXT_SUBSET_NOT_FINISHED:
  d=1   L 371  T=12 F=6  T=0 F=401  case XML_ERR_CONDSEC_INVALID_KEYWORD:  <-- BLOCKER
  d=1   L 375  T=0 F=18  T=0 F=401  case XML_ERR_CONDSEC_NOT_FINISHED:
  d=1   L 378  T=0 F=18  T=0 F=401  case XML_ERR_XMLDECL_NOT_STARTED:
  d=1   L 381  T=0 F=18  T=30 F=371  case XML_ERR_XMLDECL_NOT_FINISHED:
  d=1   L 384  T=0 F=18  T=0 F=401  case XML_ERR_EXT_ENTITY_STANDALONE:
  d=1   L 387  T=0 F=18  T=109 F=292  case XML_ERR_ENTITYREF_SEMICOL_MISSING:
  d=1   L 390  T=0 F=18  T=7 F=394  case XML_ERR_DOCTYPE_NOT_FINISHED:
  d=1   L 393  T=0 F=18  T=0 F=401  case XML_ERR_LTSLASH_REQUIRED:
  d=1   L 396  T=0 F=18  T=0 F=401  case XML_ERR_EQUAL_REQUIRED:
  d=1   L 399  T=0 F=18  T=6 F=395  case XML_ERR_STRING_NOT_CLOSED:
  d=1   L 402  T=0 F=18  T=3 F=398  case XML_ERR_STRING_NOT_STARTED:
  d=1   L 405  T=0 F=18  T=0 F=401  case XML_ERR_ENCODING_NAME:
  d=1   L 408  T=0 F=18  T=0 F=401  case XML_ERR_STANDALONE_VALUE:
  d=1   L 411  T=0 F=18  T=90 F=311  case XML_ERR_DOCUMENT_EMPTY:
  d=1   L 414  T=0 F=18  T=74 F=327  case XML_ERR_DOCUMENT_END:
  d=1   L 417  T=0 F=18  T=0 F=401  case XML_ERR_NOT_WELL_BALANCED:
  d=1   L 420  T=0 F=18  T=0 F=401  case XML_ERR_EXTRA_CONTENT:
  d=1   L 423  T=0 F=18  T=21 F=380  case XML_ERR_VERSION_MISSING:
  d=1   L 426  T=0 F=18  T=0 F=401  case XML_ERR_NAME_TOO_LONG:
  d=1   L 434  T=0 F=18  T=0 F=401  default:
  d=1   L 437  T=18 F=0  T=401 F=0  if (ctxt != NULL)
  d=1   L 439  T=18 F=0  T=366 F=35  if (info == NULL) {
  d=1   L 448  T=18 F=0  T=401 F=0  if (ctxt != NULL) {
  d=1   L 450  T=15 F=3  T=121 F=280  if (ctxt->recovery == 0)

[off-chain: 1060 additional divergent branches across 79 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c2ef14a3db44578b, size=368 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=134s, mutation_op=TokenReplace):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=52d6203fbc0f535a, size=368 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=1580s, mutation_op=ByteAddMutator,BytesRandSetMutator,BytesSwapMutator,ByteIncMutator,QwordAddMutator,QwordAddMutator,BytesSetMutator):
  0000: ff 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=e0238400d3b4fff4, size=368 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=2643s, mutation_op=ByteIncMutator,ByteRandMutator,DwordInterestingMutator,BytesSetMutator,ByteAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=fc1b1c8fd7dfad31, size=526 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=2880s, mutation_op=DwordInterestingMutator,BytesInsertCopyMutator,CrossoverInsertMutator,BytesExpandMutator,QwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=02b70991cfb81b44, size=338 bytes, fuzzer=cmplog, trial=4, discovered_at=0s, mutation_op=BytesCopyMutator,BytesRandInsertMutator,BytesInsertCopyMutator,ByteInterestingMutator,BytesInsertMutator,BytesDeleteMutator,BytesInsertCopyMutator):
  0000: 06 00 00 3d 31 32 37 37 37 32 26 78 6d 6c 5c 0a   ...=127772&xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 7f 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .."?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=000a8afebd4fd850, size=474 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=BytesSwapMutator,TokenReplace,BytesInsertCopyMutator,WordAddMutator,ByteInterestingMutator,ByteNegMutator,ByteIncMutator):
  0000: 4d 20 ff ff 74 64 73 2f 31 32 37 37 06 00 00 00   M ..tds/1277....
  0010: 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   127772.xml\.<?xm
  0020: 6c 20 76 65 72 41 53 43 49 49 22 31 2e 30 22 3f   l verASCII"1.0"?
  0030: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
Seed 3 (id=00269ca53cdf3bb2, size=119 bytes, fuzzer=naive, trial=2, discovered_at=1s, mutation_op=ByteDecMutator,DwordAddMutator,DwordInterestingMutator,BytesDeleteMutator):
  0000: 57 57 00 00 b1 32 37 37 37 32 2e 78 6d 6c 5c 0a   WW...27772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=0241c73c0a285696, size=284 bytes, fuzzer=cmplog, trial=5, discovered_at=10s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,ByteInterestingMutator,ByteDecMutator,BytesSwapMutator):
  0000: 05 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c ff 2f 62 3e 0a 3c 2f 61 3e 0a 0a   <?xml./b>.</a>..
  0020: 5c 0a 64 74 64 25 29 31 32 25 37 37 32 2e 64 74   \.dtd%)12%772.dt
  0030: 64 5c 0a 3c 21 45 4c 45 4d 45 4e 54 20 61 20 28   d\.<!ELEMENT a (
Seed 5 (id=02ad68c569326279, size=368 bytes, fuzzer=cmplog, trial=4, discovered_at=18s, mutation_op=ByteAddMutator,BytesDeleteMutator,DwordInterestingMutator,BytesInsertMutator,BytesDeleteMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 00 5c 0a   ....127772.xm.\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x3 ff(.)x1                     06(.)x12 27(')x11 65(e)x8 3d(=)x7 +37u  PARTIAL
   0x0001  00(.)x4                             00(.)x14 27(')x8 66(f)x8 2f(/)x7 +36u  PARTIAL
   0x0002  00(.)x4                             68(h)x15 00(.)x14 3d(=)x9 74(t)x8 +33u  PARTIAL
   0x0003  00(.)x4                             74(t)x23 00(.)x15 68(h)x13 22(")x9 +26u  PARTIAL
   0x0004  31(1)x4                             74(t)x33 31(1)x14 68(h)x9 2f(/)x6 +28u  PARTIAL
   0x0005  32(2)x4                             74(t)x23 70(p)x22 32(2)x15 3a(:)x7 +24u  PARTIAL
   0x0006  37(7)x4                             3a(:)x22 37(7)x15 74(t)x12 70(p)x11 +25u  PARTIAL
   0x0007  37(7)x4                             2f(/)x31 37(7)x14 3a(:)x12 70(p)x9 +26u  PARTIAL
   0x0008  37(7)x4                             2f(/)x35 37(7)x15 3a(:)x12 77(w)x7 +20u  PARTIAL
   0x0009  32(2)x4                             2f(/)x27 32(2)x16 77(w)x13 66(f)x6 +23u  PARTIAL
   0x000a  2e(.)x4                             2f(/)x19 77(w)x17 2e(.)x14 66(f)x5 +28u  PARTIAL
   0x000b  78(x)x4                             78(x)x15 77(w)x13 2f(/)x10 2e(.)x7 +30u  PARTIAL
   0x000c  6d(m)x4                             6d(m)x15 77(w)x13 61(a)x6 2e(.)x6 +33u  PARTIAL
   0x000d  6c(l)x4                             6c(l)x13 77(w)x8 2e(.)x6 33(3)x6 +35u  PARTIAL
   0x000e  5c(\)x4                             5c(\)x14 2f(/)x8 65(e)x5 33(3)x5 +37u  PARTIAL
   0x000f  0a(.)x4                             0a(.)x16 2e(.)x7 6c(l)x6 77(w)x5 +38u  PARTIAL
   0x0010  3c(<)x4                             3c(<)x17 72(r)x11 20( )x5 6f(o)x5 +39u  PARTIAL
   0x0011  3f(?)x4                             3f(?)x12 6c(l)x7 6e(n)x6 72(r)x5 +41u  PARTIAL
   0x0012  78(x)x4                             78(x)x14 2f(/)x12 2e(.)x8 28(()x5 +37u  PARTIAL
   0x0013  6d(m)x4                             6d(m)x13 2f(/)x9 31(1)x5 6e(n)x4 +45u  PARTIAL
   0x0014  6c(l)x4                             6c(l)x14 2f(/)x9 39(9)x6 29())x4 +49u  PARTIAL
   0x0015  20( )x4                             20( )x12 2f(/)x9 39(9)x8 31(1)x5 +38u  PARTIAL
   0x0016  76(v)x4                             76(v)x13 39(9)x9 2f(/)x7 2e(.)x3 +49u  PARTIAL
   0x0017  65(e)x4                             65(e)x14 39(9)x8 2f(/)x8 74(t)x4 +43u  PARTIAL
   0x0018  72(r)x4                             72(r)x12 2f(/)x8 39(9)x6 21(!)x4 +43u  PARTIAL
   0x0019  73(s)x4                             73(s)x12 6c(l)x6 2f(/)x6 74(t)x6 +37u  PARTIAL
   0x001a  69(i)x4                             69(i)x16 2e(.)x5 2f(/)x4 3a(:)x4 +45u  PARTIAL
   0x001b  6f(o)x4                             6f(o)x13 2f(/)x7 3d(=)x6 6e(n)x5 +42u  PARTIAL
   0x001c  6e(n)x4                             6e(n)x13 2f(/)x7 74(t)x6 20( )x5 +44u  PARTIAL
   0x001d  3d(=)x4                             3d(=)x11 6e(n)x5 28(()x5 74(t)x4 +46u  PARTIAL
   0x001e  22(")x4                             22(")x11 2e(.)x6 74(t)x5 2f(/)x5 +43u  PARTIAL
   0x001f  31(1)x4                             31(1)x11 74(t)x6 20( )x4 28(()x4 +51u  PARTIAL
   0x0020  2e(.)x4                             2e(.)x15 20( )x5 5f(_)x5 27(')x4 +54u  PARTIAL
   0x0021  30(0)x4                             30(0)x11 20( )x7 0a(.)x5 3e(>)x4 +45u  PARTIAL
   0x0022  22(")x4                             22(")x13 20( )x9 2f(/)x6 29())x5 +44u  PARTIAL
   0x0023  3f(?)x4                             3f(?)x12 20( )x8 2f(/)x5 41(A)x4 +47u  PARTIAL
   0x0024  3e(>)x4                             3e(>)x13 20( )x9 2f(/)x6 5f(_)x4 +45u  PARTIAL
   0x0025  0a(.)x4                             0a(.)x14 20( )x10 5f(_)x5 2f(/)x5 +48u  PARTIAL
   0x0026  3c(<)x4                             3c(<)x13 20( )x9 2f(/)x6 7e(~)x4 +43u  PARTIAL
   0x0027  21(!)x4                             21(!)x14 20( )x10 2f(/)x7 26(&)x5 +43u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6436.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6436,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile), value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6436 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6436 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6436 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).