==== BLOCKER ====
Target: libxml2
Branch ID: 6429
Location: /src/libxml2/parser.c:256:9
Enclosing function: parser.c:xmlFatalErr
Source line:         case XML_ERR_INVALID_HEX_CHARREF:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (value_profile vs value_profile)
cmplog                           3        7          0  REFERENCE
value_profile                   10        0          0  winner (value_profile vs naive)
value_profile_cmplog             9        1          0  REFERENCE
naive_ctx                        6        4          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=10.90h  loser=23.80h
  avg hitcount on branch: winner=21  loser=0
  prob_div=0.90  dur_div=12.90h  hit_div=21
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6429/{W,L}/branch_coverage_show.txt

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
[W]   256          case XML_ERR_INVALID_HEX_CHARREF: <-- BLOCKER
[W]   257              errmsg = "CharRef: invalid hexadecimal value";
[W]   258              break;
[ ]   259          case XML_ERR_INVALID_DEC_CHARREF:
[ ]   260              errmsg = "CharRef: invalid decimal value";
[ ]   261              break;
[ ]   262          case XML_ERR_INVALID_CHARREF:
[ ]   263              errmsg = "CharRef: invalid value";
[ ]   264              break;
[B]   265          case XML_ERR_INTERNAL_ERROR:
[B]   266              errmsg = "internal error";
[B]   267              break;
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
[L]   298          case XML_ERR_LT_IN_ATTRIBUTE:
[L]   299              errmsg = "Unescaped '<' not allowed in attributes values";
[L]   300              break;
[ ]   301          case XML_ERR_LITERAL_NOT_STARTED:
[ ]   302              errmsg = "SystemLiteral \" or ' expected";
[ ]   303              break;
[L]   304          case XML_ERR_LITERAL_NOT_FINISHED:
[L]   305              errmsg = "Unfinished System or Public ID \" or ' expected";
[L]   306              break;
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
[L]   337          case XML_ERR_ATTLIST_NOT_STARTED:
[L]   338              errmsg = "'(' required to start ATTLIST enumeration";
[L]   339              break;
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
[ ]   352          case XML_ERR_ELEMCONTENT_NOT_STARTED:
[ ]   353              errmsg = "ContentDecl : Name or '(' expected";
[ ]   354              break;
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
[L]   368          case XML_ERR_EXT_SUBSET_NOT_FINISHED:
[L]   369              errmsg = "Content error in the external subset";
[L]   370              break;
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
[B]   387          case XML_ERR_ENTITYREF_SEMICOL_MISSING:
[B]   388              errmsg = "EntityRef: expecting ';'";
[B]   389              break;
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
[B]   414          case XML_ERR_DOCUMENT_END:
[B]   415              errmsg = "Extra content at the end of the document";
[B]   416              break;
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
[B]   444          __xmlRaiseError(NULL, NULL, NULL, ctxt, NULL, XML_FROM_PARSER, error,
[B]   445                          XML_ERR_FATAL, NULL, 0, info, NULL, NULL, 0, 0, "%s: %s\n",
[B]   446                          errmsg, info);
[B]   447      }
[B]   448      if (ctxt != NULL) {
[B]   449  	ctxt->wellFormed = 0;
[B]   450  	if (ctxt->recovery == 0)
[B]   451  	    ctxt->disableSAX = 1;
[B]   452      }
[B]   453  }

--- Caller (1 hop): xmlParseCharRef (/src/libxml2/parser.c:2309-2400, calls parser.c:xmlFatalErr at line 2334) (±10 around call site) ---
[ ]  2324                  if (ctxt->instate == XML_PARSER_EOF)
[ ]  2325                      return(0);
[ ]  2326  	    }
[W]  2327  	    if ((RAW >= '0') && (RAW <= '9'))
[ ]  2328  	        val = val * 16 + (CUR - '0');
[W]  2329  	    else if ((RAW >= 'a') && (RAW <= 'f') && (count < 20))
[ ]  2330  	        val = val * 16 + (CUR - 'a') + 10;
[W]  2331  	    else if ((RAW >= 'A') && (RAW <= 'F') && (count < 20))
[ ]  2332  	        val = val * 16 + (CUR - 'A') + 10;
[W]  2333  	    else {
[W]  2334  		xmlFatalErr(ctxt, XML_ERR_INVALID_HEX_CHARREF, NULL); <-- CALL
[W]  2335  		val = 0;
[W]  2336  		break;
[W]  2337  	    }
[ ]  2338  	    if (val > 0x110000)
[ ]  2339  	        val = 0x110000;
[ ]  2340  
[ ]  2341  	    NEXT;
[ ]  2342  	    count++;
[ ]  2343  	}
[W]  2344  	if (RAW == ';') {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094, calls parser.c:xmlFatalErr at line 2081)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     158       734  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      63       441  inputPop  (/src/libxml2/parser.c:1723-1738)
     376         0  parser.c:xmlSHRINK  (/src/libxml2/parser.c:2059-2066)
      21       165  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
      21       155  inputPush  (/src/libxml2/parser.c:1693-1712)
      59       188  xmlParseChunk  (/src/libxml2/parser.c:12135-12300)
      21       147  parser.c:xmlCtxtUseOptionsInternal  (/src/libxml2/parser.c:14842-14969)
      26       151  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120)
       7       129  parser.c:xmlHaltParser  (/src/libxml2/parser.c:12416-12441)
      32       147  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)  <-- enclosing
      14        98  xmlCreatePushParserCtxt  (/src/libxml2/parser.c:12329-12405)
      14        98  xmlCtxtUseOptions  (/src/libxml2/parser.c:14983-14985)
       0        75  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      30        98  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
       1        68  parser.c:xmlParseLookupString  (/src/libxml2/parser.c:11137-11161)
... (50 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094) ---
  d=2   L2076  T=0 F=276  T=0 F=772  if (((curEnd > XML_MAX_LOOKUP_LIMIT) ||
  d=2   L2077  T=0 F=276  T=0 F=772  (curBase > XML_MAX_LOOKUP_LIMIT)) &&
  d=2   L2086  T=0 F=276  T=0 F=772  if ((ctxt->input->cur > ctxt->input->end) ||
  d=2   L2087  T=0 F=276  T=0 F=772  (ctxt->input->cur < ctxt->input->base)) {
  d=2   L2092  T=276 F=0  T=772 F=0  if ((ctxt->input->cur != NULL) && (*ctxt->input->cur == 0))
  d=2   L2092  T=36 F=240  T=17 F=755  if ((ctxt->input->cur != NULL) && (*ctxt->input->cur == 0))
--- d=1  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453) ---
  d=1   L 252  T=4 F=28  T=24 F=123  if ((ctxt != NULL) && (ctxt->disableSAX != 0) &&
  d=1   L 252  T=32 F=0  T=147 F=0  if ((ctxt != NULL) && (ctxt->disableSAX != 0) &&
  d=1   L 253  T=0 F=4  T=0 F=24  (ctxt->instate == XML_PARSER_EOF))
  d=1   L 256  T=12 F=20  T=0 F=147  case XML_ERR_INVALID_HEX_CHARREF:  <-- BLOCKER
  d=1   L 259  T=0 F=32  T=0 F=147  case XML_ERR_INVALID_DEC_CHARREF:
  d=1   L 262  T=0 F=32  T=0 F=147  case XML_ERR_INVALID_CHARREF:
  d=1   L 265  T=10 F=22  T=18 F=129  case XML_ERR_INTERNAL_ERROR:
  d=1   L 268  T=0 F=32  T=0 F=147  case XML_ERR_PEREF_AT_EOF:
  d=1   L 271  T=0 F=32  T=0 F=147  case XML_ERR_PEREF_IN_PROLOG:
  d=1   L 274  T=0 F=32  T=0 F=147  case XML_ERR_PEREF_IN_EPILOG:
  d=1   L 277  T=0 F=32  T=0 F=147  case XML_ERR_PEREF_NO_NAME:
  d=1   L 280  T=0 F=32  T=0 F=147  case XML_ERR_PEREF_SEMICOL_MISSING:
  d=1   L 283  T=0 F=32  T=0 F=147  case XML_ERR_ENTITY_LOOP:
  d=1   L 286  T=0 F=32  T=0 F=147  case XML_ERR_ENTITY_NOT_STARTED:
  d=1   L 289  T=0 F=32  T=0 F=147  case XML_ERR_ENTITY_PE_INTERNAL:
  d=1   L 292  T=0 F=32  T=0 F=147  case XML_ERR_ENTITY_NOT_FINISHED:
  d=1   L 295  T=0 F=32  T=0 F=147  case XML_ERR_ATTRIBUTE_NOT_STARTED:
  d=1   L 298  T=0 F=32  T=3 F=144  case XML_ERR_LT_IN_ATTRIBUTE:
  d=1   L 301  T=0 F=32  T=0 F=147  case XML_ERR_LITERAL_NOT_STARTED:
  d=1   L 304  T=0 F=32  T=3 F=144  case XML_ERR_LITERAL_NOT_FINISHED:
  d=1   L 307  T=0 F=32  T=0 F=147  case XML_ERR_MISPLACED_CDATA_END:
  d=1   L 310  T=0 F=32  T=0 F=147  case XML_ERR_URI_REQUIRED:
  d=1   L 313  T=0 F=32  T=0 F=147  case XML_ERR_PUBID_REQUIRED:
  d=1   L 316  T=0 F=32  T=0 F=147  case XML_ERR_HYPHEN_IN_COMMENT:
  d=1   L 319  T=0 F=32  T=12 F=135  case XML_ERR_PI_NOT_STARTED:
  d=1   L 322  T=0 F=32  T=0 F=147  case XML_ERR_RESERVED_XML_NAME:
  d=1   L 325  T=0 F=32  T=0 F=147  case XML_ERR_NOTATION_NOT_STARTED:
  d=1   L 328  T=0 F=32  T=0 F=147  case XML_ERR_NOTATION_NOT_FINISHED:
  d=1   L 331  T=0 F=32  T=0 F=147  case XML_ERR_VALUE_REQUIRED:
  d=1   L 334  T=0 F=32  T=0 F=147  case XML_ERR_URI_FRAGMENT:
  d=1   L 337  T=0 F=32  T=3 F=144  case XML_ERR_ATTLIST_NOT_STARTED:
  d=1   L 340  T=0 F=32  T=0 F=147  case XML_ERR_NMTOKEN_REQUIRED:
  d=1   L 343  T=0 F=32  T=0 F=147  case XML_ERR_ATTLIST_NOT_FINISHED:
  d=1   L 346  T=0 F=32  T=0 F=147  case XML_ERR_MIXED_NOT_STARTED:
  d=1   L 349  T=0 F=32  T=0 F=147  case XML_ERR_PCDATA_REQUIRED:
  d=1   L 352  T=0 F=32  T=0 F=147  case XML_ERR_ELEMCONTENT_NOT_STARTED:
  d=1   L 355  T=0 F=32  T=0 F=147  case XML_ERR_ELEMCONTENT_NOT_FINISHED:
  d=1   L 358  T=0 F=32  T=0 F=147  case XML_ERR_PEREF_IN_INT_SUBSET:
  d=1   L 362  T=0 F=32  T=1 F=146  case XML_ERR_GT_REQUIRED:
  d=1   L 365  T=0 F=32  T=0 F=147  case XML_ERR_CONDSEC_INVALID:
  d=1   L 368  T=0 F=32  T=8 F=139  case XML_ERR_EXT_SUBSET_NOT_FINISHED:
  d=1   L 371  T=0 F=32  T=0 F=147  case XML_ERR_CONDSEC_INVALID_KEYWORD:
  d=1   L 375  T=0 F=32  T=0 F=147  case XML_ERR_CONDSEC_NOT_FINISHED:
  d=1   L 378  T=0 F=32  T=0 F=147  case XML_ERR_XMLDECL_NOT_STARTED:
  d=1   L 381  T=0 F=32  T=6 F=141  case XML_ERR_XMLDECL_NOT_FINISHED:
  d=1   L 384  T=0 F=32  T=0 F=147  case XML_ERR_EXT_ENTITY_STANDALONE:
  d=1   L 387  T=7 F=25  T=3 F=144  case XML_ERR_ENTITYREF_SEMICOL_MISSING:
  d=1   L 390  T=0 F=32  T=3 F=144  case XML_ERR_DOCTYPE_NOT_FINISHED:
  d=1   L 393  T=0 F=32  T=0 F=147  case XML_ERR_LTSLASH_REQUIRED:
  d=1   L 396  T=0 F=32  T=0 F=147  case XML_ERR_EQUAL_REQUIRED:
  d=1   L 399  T=0 F=32  T=0 F=147  case XML_ERR_STRING_NOT_CLOSED:
  d=1   L 402  T=0 F=32  T=0 F=147  case XML_ERR_STRING_NOT_STARTED:
  d=1   L 405  T=0 F=32  T=0 F=147  case XML_ERR_ENCODING_NAME:
  d=1   L 408  T=0 F=32  T=0 F=147  case XML_ERR_STANDALONE_VALUE:
  d=1   L 411  T=0 F=32  T=54 F=93  case XML_ERR_DOCUMENT_EMPTY:
  d=1   L 414  T=3 F=29  T=27 F=120  case XML_ERR_DOCUMENT_END:
  d=1   L 417  T=0 F=32  T=0 F=147  case XML_ERR_NOT_WELL_BALANCED:
  d=1   L 420  T=0 F=32  T=0 F=147  case XML_ERR_EXTRA_CONTENT:
  d=1   L 423  T=0 F=32  T=6 F=141  case XML_ERR_VERSION_MISSING:
  d=1   L 426  T=0 F=32  T=0 F=147  case XML_ERR_NAME_TOO_LONG:
  d=1   L 434  T=0 F=32  T=0 F=147  default:
  d=1   L 437  T=32 F=0  T=147 F=0  if (ctxt != NULL)
  d=1   L 439  T=22 F=10  T=129 F=18  if (info == NULL) {
  d=1   L 448  T=32 F=0  T=147 F=0  if (ctxt != NULL) {
  d=1   L 450  T=4 F=28  T=46 F=101  if (ctxt->recovery == 0)

[off-chain: 954 additional divergent branches across 82 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=46ff690cc5b8210e, size=1012 bytes, fuzzer=value_profile, trial=1, discovered_at=23560s, mutation_op=TokenInsert,BytesRandSetMutator,ByteDecMutator):
  0000: 6c 6e 73 3a 20 2f 2f 2f 2f 2f 2f 2f 2f 2f 2f 2f   lns: ///////////
  0010: 6d 6c 5c 74 64 5c 0a 3c 6e 6b 3e 0a 20 20 3c 62   ml\td\.<nk>.  <b
  0020: 20 3b 6c 69 6e 6b 39 68 72 65 66 3d 22 20 28 23    ;link9href=" (#
  0030: 50 43 44 6c 69 78 41 54 78 29 3e 2a 2a 2a 0a 20   PCDlixATx)>***. 
Seed 2 (id=d680ff0934ff1118, size=1020 bytes, fuzzer=value_profile, trial=1, discovered_at=23560s, mutation_op=ByteNegMutator,BytesSetMutator,BytesInsertCopyMutator,BytesSwapMutator):
  0000: 37 37 37 61 2f 31 32 37 37 37 32 2e 64 74 64 22   777a/127772.dtd"
  0010: 3e 0a 0a 20 43 2f 31 32 38 37 37 32 2e 64 74 64   >.. C/128772.dtd
  0020: 22 c2 0a 0a 20 3c 62 20 78 6c 69 6e 6b 39 68 72   "... <b xlink9hr
  0030: 65 66 3d 22 20 28 23 50 43 44 6c 69 7d 6c 6e 73   ef=" (#PCDli}lns
Seed 3 (id=ec47aafbeac0c149, size=1034 bytes, fuzzer=value_profile, trial=1, discovered_at=23604s, mutation_op=BytesExpandMutator,ByteRandMutator,ByteRandMutator,BytesInsertCopyMutator,BytesRandInsertMutator):
  0000: 6c 6e 73 3a 20 2f 2f 2f 2f 2f 2f 2f 2f 2f 2f 2f   lns: ///////////
  0010: 6d 6c 5c 74 64 5c 0a 3c 6e 6b 3e 0a 20 20 3c 62   ml\td\.<nk>.  <b
  0020: 20 3b 6c 69 6e 6b 39 68 72 65 66 3d 22 20 28 23    ;link9href=" (#
  0030: 50 43 44 6c 69 78 41 54 78 29 3e 2a 2a 2a 0a 20   PCDlixATx)>***. 
Seed 4 (id=c7c229096902818b, size=237 bytes, fuzzer=value_profile, trial=1, discovered_at=29692s, mutation_op=BytesRandSetMutator,ByteInterestingMutator,DwordAddMutator,CrossoverReplaceMutator,ByteInterestingMutator):
  0000: 3b 3c 3c 00 40 5c 0a 3c 6d 6d 3e 2e 30 0c 41 21   ;<<.@\.<mm>.0.A!
  0010: 44 72 67 26 2f 3a 2f 2f 2f 3b 3a 3a 3a 4a 3a 55   Drg&/:///;:::J:U
  0020: 53 2d 41 53 43 49 49 3a 6f 26 2f 2f 2f 3a 26 72   S-ASCII:o&///:&r
  0030: 67 26 2f 3a 6f 00 04 36 2d 55 43 53 2d 34 28 73   g&/:o..6-UCS-4(s
Seed 5 (id=5ebb9b6c047b4019, size=1016 bytes, fuzzer=value_profile, trial=1, discovered_at=42319s, mutation_op=TokenInsert,ByteDecMutator,BytesRandSetMutator,BytesSwapMutator,BytesCopyMutator,BitFlipMutator):
  0000: 6c 6e 73 3a 20 2f 2f 2f 2e 2f 2f 2f 2f 2f 2f 2f   lns: ///.///////
  0010: 6d 6c 5c 74 64 5c 0a 3c 6e 6b 3e 0a 20 20 3c 62   ml\td\.<nk>.  <b
  0020: 20 3b 6c 69 6e 6b 39 68 72 65 66 3d 22 20 28 23    ;link9href=" (#
  0030: 50 43 44 6c 69 78 41 54 78 29 3e 2a 2a 2a 0a 20   PCDlixATx)>***. 

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0357b7fe9410b932, size=404 bytes, fuzzer=naive, trial=3, discovered_at=0s, mutation_op=BytesCopyMutator,TokenReplace,BytesExpandMutator,BytesDeleteMutator):
  0000: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0010: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0020: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
  0030: 32 37 37 37 32 2e 64 74 64 22 3e 00 bf 91 00 3e   27772.dtd">....>
Seed 2 (id=03d78b3095fb6a26, size=388 bytes, fuzzer=naive, trial=4, discovered_at=0s, mutation_op=BitFlipMutator,BytesInsertMutator,CrossoverReplaceMutator,ByteRandMutator,ByteFlipMutator,BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=003a9c177fd1ad1c, size=201 bytes, fuzzer=naive, trial=2, discovered_at=39s, mutation_op=ByteRandMutator,WordInterestingMutator,DwordInterestingMutator,BytesDeleteMutator):
  0000: 38 38 38 38 38 49 22 31 00 31 32 37 37 37 32 2e   88888I"1.127772.
  0010: 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69   xml\.<?xml versi
  0020: 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43   on="1.0"?>.<!DOC
  0030: 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22 64   TYPE a SYSTEM "d
Seed 4 (id=001ec54085f9ee0a, size=192 bytes, fuzzer=naive, trial=2, discovered_at=52s, mutation_op=BytesDeleteMutator,BytesInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=00229161e8eeb28b, size=284 bytes, fuzzer=naive, trial=2, discovered_at=277s, mutation_op=QwordAddMutator,BytesInsertCopyMutator,BytesRandSetMutator,TokenInsert):
  0000: 27 73 69 6d 70 6c 65 27 0a 20 20 20 20 7f 7f 7f   'simple'.    ...
  0010: 7f 20 20 20 20 20 ee ee ee ee ee 6c 6c 78 6c 69   .     .....llxli
  0020: 6e 6b 3a 68 72 65 66 20 20 20 43 44 41 54 41 06   nk:href   CDATA.
  0030: 00 00 00 31 32 37 37 37 32 2e 78 6d 86 5c 0a 3c   ...127772.xm.\.<


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  6c(l)x4 3b(;)x2 37(7)x1             06(.)x3 65(e)x3 22(")x3 3d(=)x3 +28u  PARTIAL
   0x0001  6e(n)x4 3c(<)x2 37(7)x1             00(.)x5 2f(/)x5 68(h)x4 66(f)x3 +20u  PARTIAL
   0x0002  73(s)x4 3c(<)x2 37(7)x1             2f(/)x5 3d(=)x4 68(h)x3 64(d)x3 +28u  PARTIAL
   0x0003  3a(:)x4 00(.)x2 61(a)x1             68(h)x6 74(t)x6 2f(/)x4 00(.)x3 +23u  PARTIAL
   0x0004  20( )x4 40(@)x2 2f(/)x1             70(p)x10 74(t)x6 68(h)x4 2f(/)x4 +19u  PARTIAL
   0x0005  2f(/)x4 5c(\)x2 31(1)x1             74(t)x13 3a(:)x10 2f(/)x4 70(p)x3 +17u  PARTIAL
   0x0006  2f(/)x4 0a(.)x2 32(2)x1             2f(/)x13 74(t)x8 70(p)x6 3a(:)x4 +15u  PARTIAL
   0x0007  2f(/)x4 3c(<)x2 37(7)x1             2f(/)x16 70(p)x6 3a(:)x6 37(7)x2 +18u  PARTIAL
   0x0008  2f(/)x3 6d(m)x2 37(7)x1 2e(.)x1     2f(/)x15 3a(:)x7 77(w)x4 37(7)x3 +15u  PARTIAL
   0x0009  2f(/)x4 6d(m)x2 37(7)x1             2f(/)x16 73(s)x4 77(w)x3 32(2)x2 +20u  PARTIAL
   0x000a  2f(/)x4 3e(>)x2 32(2)x1             2f(/)x16 77(w)x5 2e(.)x2 32(2)x2 +21u  PARTIAL
   0x000b  2f(/)x4 2e(.)x3                     2f(/)x6 2e(.)x5 77(w)x4 78(x)x3 +25u  PARTIAL
   0x000c  2f(/)x4 30(0)x2 64(d)x1             77(w)x5 2f(/)x5 2d(-)x5 6d(m)x4 +25u  PARTIAL
   0x000d  2f(/)x4 0c(.)x2 74(t)x1             2f(/)x5 6c(l)x4 2e(.)x3 75(u)x3 +28u  PARTIAL
   0x000e  2f(/)x4 41(A)x2 64(d)x1             2f(/)x5 2e(.)x3 5c(\)x2 65(e)x2 +31u  PARTIAL
   0x000f  2f(/)x4 21(!)x2 22(")x1             2e(.)x4 0a(.)x3 2f(/)x3 2d(-)x3 +29u  PARTIAL
   0x0010  6d(m)x4 44(D)x2 3e(>)x1             2f(/)x6 2e(.)x4 72(r)x4 3c(<)x3 +26u  PARTIAL
   0x0011  6c(l)x4 72(r)x2 0a(.)x1             2f(/)x4 2e(.)x4 6c(l)x3 27(')x3 +30u  PARTIAL
   0x0012  5c(\)x4 67(g)x2 0a(.)x1             2e(.)x5 78(x)x3 28(()x3 6c(l)x2 +32u  PARTIAL
   0x0013  74(t)x4 26(&)x2 20( )x1             74(t)x4 6d(m)x3 2d(-)x3 5c(\)x2 +33u  PARTIAL
   0x0014  64(d)x4 2f(/)x2 43(C)x1             6c(l)x3 2d(-)x3 2e(.)x3 74(t)x3 +32u  PARTIAL
   0x0015  5c(\)x4 3a(:)x2 2f(/)x1             2f(/)x5 20( )x4 70(p)x3 6e(n)x2 +31u  PARTIAL
   0x0016  0a(.)x4 2f(/)x2 31(1)x1             2f(/)x5 3c(<)x2 76(v)x2 65(e)x2 +36u  PARTIAL
   0x0017  3c(<)x4 2f(/)x2 32(2)x1             2f(/)x6 65(e)x3 21(!)x2 74(t)x2 +32u  PARTIAL
   0x0018  6e(n)x4 2f(/)x2 38(8)x1             2f(/)x4 21(!)x3 72(r)x2 39(9)x2 +35u  PARTIAL
   0x0019  6b(k)x4 3b(;)x2 37(7)x1             73(s)x3 2f(/)x3 77(w)x3 2e(.)x3 +34u  PARTIAL
   0x001a  3e(>)x4 3a(:)x2 37(7)x1             77(w)x4 69(i)x2 6d(m)x2 2e(.)x2 +35u  DIFFER
   0x001b  0a(.)x4 3a(:)x2 32(2)x1             6c(l)x4 6f(o)x3 77(w)x3 2f(/)x3 +32u  DIFFER
   0x001c  20( )x4 3a(:)x2 2e(.)x1             2f(/)x4 6e(n)x3 2e(.)x3 28(()x3 +29u  PARTIAL
   0x001d  20( )x4 4a(J)x2 64(d)x1             3d(=)x3 2d(-)x3 72(r)x2 2e(.)x2 +36u  PARTIAL
   0x001e  3c(<)x4 3a(:)x2 74(t)x1             22(")x3 73(s)x3 2f(/)x3 2e(.)x3 +35u  PARTIAL
   0x001f  62(b)x4 55(U)x2 64(d)x1             31(1)x4 2f(/)x4 69(i)x3 2e(.)x3 +29u  PARTIAL
   0x0020  20( )x4 53(S)x2 22(")x1             2e(.)x5 31(1)x3 6f(o)x2 2f(/)x2 +31u  PARTIAL
   0x0021  3b(;)x4 2d(-)x2 c2(.)x1             2f(/)x3 28(()x3 20( )x2 30(0)x2 +35u  PARTIAL
   0x0022  6c(l)x4 41(A)x2 0a(.)x1             2f(/)x4 2d(-)x4 20( )x3 53(S)x2 +29u  PARTIAL
   0x0023  69(i)x4 0a(.)x1 53(S)x1 3a(:)x1     2f(/)x6 3f(?)x3 2d(-)x3 59(Y)x2 +30u  PARTIAL
   0x0024  6e(n)x4 43(C)x2 20( )x1             2f(/)x5 2e(.)x3 2d(-)x3 3b(;)x3 +29u  PARTIAL
   0x0025  6b(k)x4 49(I)x2 3c(<)x1             2d(-)x4 2f(/)x3 54(T)x2 0a(.)x2 +31u  PARTIAL
   0x0026  39(9)x4 49(I)x2 62(b)x1             2f(/)x8 2d(-)x4 45(E)x2 3c(<)x2 +26u  PARTIAL
   0x0027  68(h)x4 3a(:)x2 20( )x1             2d(-)x4 39(9)x3 4d(M)x2 21(!)x2 +29u  PARTIAL
   ... (24 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6429.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6429,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6429 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6429 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6429 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).