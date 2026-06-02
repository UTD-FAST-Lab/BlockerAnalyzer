==== BLOCKER ====
Target: libxml2
Branch ID: 6674
Location: /src/libxml2/parser.c:6969:10
Enclosing function: xmlParseMarkupDecl
Source line: 	        case '-':
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (ctx_coverage vs naive_ctx); loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    4        6          0  REFERENCE
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.90h  loser=23.80h
  avg hitcount on branch: winner=616  loser=0
  prob_div=1.00  dur_div=21.90h  hit_div=616
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=16.50h  loser=23.80h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.80  dur_div=7.30h  hit_div=5
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6674/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseMarkupDecl (/src/libxml2/parser.c:6950-6990) ---
[ ]  6948   */
[ ]  6949  void
[B]  6950  xmlParseMarkupDecl(xmlParserCtxtPtr ctxt) {
[B]  6951      GROW;
[B]  6952      if (CUR == '<') {
[B]  6953          if (NXT(1) == '!') {
[B]  6954  	    switch (NXT(2)) {
[B]  6955  	        case 'E':
[B]  6956  		    if (NXT(3) == 'L')
[B]  6957  			xmlParseElementDecl(ctxt);
[L]  6958  		    else if (NXT(3) == 'N')
[ ]  6959  			xmlParseEntityDecl(ctxt);
[L]  6960                      else
[L]  6961                          SKIP(2);
[B]  6962  		    break;
[L]  6963  	        case 'A':
[L]  6964  		    xmlParseAttributeListDecl(ctxt);
[L]  6965  		    break;
[ ]  6966  	        case 'N':
[ ]  6967  		    xmlParseNotationDecl(ctxt);
[ ]  6968  		    break;
[W]  6969  	        case '-': <-- BLOCKER
[W]  6970  		    xmlParseComment(ctxt);
[W]  6971  		    break;
[W]  6972  		default:
[ ]  6973  		    /* there is an error but it will be detected later */
[W]  6974                      SKIP(2);
[W]  6975  		    break;
[B]  6976  	    }
[B]  6977  	} else if (NXT(1) == '?') {
[W]  6978  	    xmlParsePI(ctxt);
[W]  6979  	}
[B]  6980      }
[ ]  6981  
[ ]  6982      /*
[ ]  6983       * detect requirement to exit there and act accordingly
[ ]  6984       * and avoid having instate overridden later on
[ ]  6985       */
[B]  6986      if (ctxt->instate == XML_PARSER_EOF)
[ ]  6987          return;
[ ]  6988  
[B]  6989      ctxt->instate = XML_PARSER_DTD;
[B]  6990  }

--- Caller (1 hop): parser.c:xmlParseInternalSubset (/src/libxml2/parser.c:8452-8503, calls xmlParseMarkupDecl at line 8477) (±10 around call site) ---
[W]  8467                 (ctxt->instate != XML_PARSER_EOF)) {
[ ]  8468  
[ ]  8469              /*
[ ]  8470               * Conditional sections are allowed from external entities included
[ ]  8471               * by PE References in the internal subset.
[ ]  8472               */
[W]  8473              if ((ctxt->inputNr > 1) && (ctxt->input->filename != NULL) &&
[W]  8474                  (RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
[ ]  8475                  xmlParseConditionalSections(ctxt);
[W]  8476              } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) == '?'))) {
[W]  8477  	        xmlParseMarkupDecl(ctxt); <-- CALL
[W]  8478              } else if (RAW == '%') {
[W]  8479  	        xmlParsePEReference(ctxt);
[W]  8480              } else {
[W]  8481  		xmlFatalErr(ctxt, XML_ERR_INTERNAL_ERROR,
[W]  8482                          "xmlParseInternalSubset: error detected in"
[W]  8483                          " Markup declaration\n");
[W]  8484                  xmlHaltParser(ctxt);
[W]  8485                  return;
[W]  8486              }
[W]  8487  	    SKIP_BLANKS;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 2  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 3  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 3  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 3  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 4  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 4  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)
hop 5  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseDocTypeDecl at line 11958)
hop 5  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 5  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 5  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)
hop 6  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 6  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 7  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 7  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 7  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     179       729  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     280         2  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
     144        39  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
       0        60  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      18        57  inputPush  (/src/libxml2/parser.c:1693-1712)
      12        50  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
      12        45  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
       0        30  xmlParseSystemLiteral  (/src/libxml2/parser.c:4248-4326)
       0        30  xmlParseVersionNum  (/src/libxml2/parser.c:10284-10329)
       0        27  xmlPushInput  (/src/libxml2/parser.c:2265-2289)
       0        27  parser.c:xmlParseElementChildrenContentDeclPriv  (/src/libxml2/parser.c:6320-6589)
       0        27  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155)
       0        22  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203)
       0        21  parser.c:xmlCleanSpecialAttr  (/src/libxml2/parser.c:1353-1364)
      21         0  xmlParsePEReference  (/src/libxml2/parser.c:7999-8146)
... (51 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=6  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=6   L12141  T=0 F=8  T=10 F=3  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12211  T=12 F=0  T=2 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=6   L12212  T=12 F=0  T=2 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=6   L12212  T=12 F=0  T=2 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=6   L12214  T=0 F=12  T=0 F=2  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=6   L12248  T=0 F=11  T=15 F=6  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12248  T=11 F=14  T=21 F=0  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12251  T=0 F=25  T=0 F=6  if (remain != 0) {
  d=6   L12257  T=0 F=25  T=0 F=6  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=6   L12268  T=0 F=25  T=2 F=4  if (terminate) {
  d=6   L12274  T=0 F=0  T=2 F=0  if (ctxt->input != NULL) {
  d=6   L12275  T=0 F=0  T=0 F=2  if (ctxt->input->buf == NULL)
  d=6   L12283  T=0 F=0  T=2 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=6   L12284  T=0 F=0  T=0 F=2  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=6   L12287  T=0 F=0  T=0 F=2  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=6   L12287  T=0 F=0  T=2 F=0  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=6   L12290  T=0 F=0  T=2 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=6   L12291  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12291  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12296  T=11 F=14  T=6 F=0  if (ctxt->wellFormed == 0)
--- d=5  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=5   L11471  T=0 F=32  T=15 F=43  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L11487  T=0 F=34  T=0 F=69  (ctxt->input->buf->raw != NULL) &&
  d=5   L11500  T=0 F=66  T=2 F=97  if (avail < 1)
  d=5   L11556  T=21 F=5  T=20 F=0  if ((!terminate) &&
  d=5   L11557  T=14 F=7  T=0 F=20  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=5   L11564  T=10 F=2  T=20 F=0  (ctxt->input->cur[4] == 'l') &&
  d=5   L11572  T=0 F=10  T=0 F=20  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=5   L11581  T=10 F=0  T=20 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L11582  T=0 F=10  T=0 F=20  (ctxt->input->encoding != NULL))
  d=5   L11584  T=10 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11584  T=10 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11585  T=10 F=0  T=20 F=0  (!ctxt->disableSAX))
  d=5   L11594  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11594  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11595  T=2 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=5   L11622  T=0 F=66  T=9 F=88  case XML_PARSER_START_TAG: {
  d=5   L11629  T=0 F=0  T=0 F=9  if ((avail < 2) && (ctxt->inputNr == 1))
  d=5   L11632  T=0 F=0  T=2 F=7  if (cur != '<') {
  d=5   L11635  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11635  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11639  T=0 F=0  T=1 F=6  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=5   L11639  T=0 F=0  T=7 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=5   L11641  T=0 F=0  T=0 F=6  if (ctxt->spaceNr == 0)
  d=5   L11643  T=0 F=0  T=0 F=6  else if (*ctxt->space == -2)
  d=5   L11648  T=0 F=0  T=6 F=0  if (ctxt->sax2)
  d=5   L11655  T=0 F=0  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L11657  T=0 F=0  T=0 F=6  if (name == NULL) {
  d=5   L11670  T=0 F=0  T=0 F=6  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=5   L11678  T=0 F=0  T=0 F=6  if ((RAW == '/') && (NXT(1) == '>')) {
  d=5   L11707  T=0 F=0  T=4 F=2  if (RAW == '>') {
  d=5   L11721  T=0 F=66  T=24 F=73  case XML_PARSER_CONTENT: {
  d=5   L11722  T=0 F=0  T=0 F=24  if ((avail < 2) && (ctxt->inputNr == 1))
  d=5   L11727  T=0 F=0  T=6 F=3  if ((cur == '<') && (next == '/')) {
  d=5   L11727  T=0 F=0  T=9 F=15  if ((cur == '<') && (next == '/')) {
  d=5   L11730  T=0 F=0  T=0 F=3  } else if ((cur == '<') && (next == '?')) {
  d=5   L11730  T=0 F=0  T=3 F=15  } else if ((cur == '<') && (next == '?')) {
  d=5   L11736  T=0 F=0  T=3 F=0  } else if ((cur == '<') && (next != '!')) {
  d=5   L11736  T=0 F=0  T=3 F=15  } else if ((cur == '<') && (next != '!')) {
  d=5   L11739  T=0 F=0  T=0 F=15  } else if ((cur == '<') && (next == '!') &&
  d=5   L11747  T=0 F=0  T=0 F=15  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=5   L11758  T=0 F=0  T=0 F=15  } else if ((cur == '<') && (next == '!') &&
  d=5   L11761  T=0 F=0  T=0 F=15  } else if (cur == '<') {
  d=5   L11765  T=0 F=0  T=0 F=15  } else if (cur == '&') {
  d=5   L11782  T=0 F=0  T=15 F=0  if ((ctxt->inputNr == 1) &&
  d=5   L11783  T=0 F=0  T=15 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=5   L11784  T=0 F=0  T=0 F=15  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=5   L11784  T=0 F=0  T=15 F=0  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=5   L11792  T=0 F=66  T=6 F=91  case XML_PARSER_END_TAG:
  d=5   L11793  T=0 F=0  T=0 F=6  if (avail < 2)
  d=5   L11795  T=0 F=0  T=0 F=6  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=5   L11795  T=0 F=0  T=6 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=5   L11797  T=0 F=0  T=6 F=0  if (ctxt->sax2) {
  d=5   L11805  T=0 F=0  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF) {
  d=5   L11807  T=0 F=0  T=3 F=3  } else if (ctxt->nameNr == 0) {
  d=5   L11905  T=0 F=66  T=5 F=92  case XML_PARSER_PROLOG:
  d=5   L11906  T=0 F=66  T=3 F=94  case XML_PARSER_EPILOG:
  d=5   L11908  T=0 F=14  T=0 F=28  if (ctxt->input->buf == NULL)
  d=5   L11914  T=0 F=14  T=3 F=25  if (avail < 2)
  d=5   L11918  T=14 F=0  T=23 F=2  if ((cur == '<') && (next == '?')) {
  d=5   L11918  T=2 F=12  T=0 F=23  if ((cur == '<') && (next == '?')) {
  d=5   L11919  T=2 F=0  T=0 F=0  if ((!terminate) &&
  d=5   L11920  T=0 F=2  T=0 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=5   L11927  T=0 F=2  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L11929  T=12 F=0  T=20 F=3  } else if ((cur == '<') && (next == '!') &&
  d=5   L11929  T=12 F=0  T=23 F=2  } else if ((cur == '<') && (next == '!') &&
  d=5   L11942  T=12 F=0  T=20 F=5  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=5   L11951  T=7 F=5  T=20 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=5   L11951  T=0 F=7  T=0 F=20  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=5   L11961  T=12 F=0  T=0 F=20  if (RAW == '[') {
  d=5   L11972  T=0 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=5   L11972  T=0 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=5   L11973  T=0 F=0  T=20 F=0  (ctxt->sax->externalSubset != NULL))
  d=5   L11985  T=0 F=0  T=0 F=3  } else if ((cur == '<') && (next == '!') &&
  d=5   L11985  T=0 F=0  T=3 F=2  } else if ((cur == '<') && (next == '!') &&
  d=5   L11989  T=0 F=0  T=0 F=5  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=5   L12007  T=20 F=46  T=0 F=97  case XML_PARSER_DTD: {
  d=5   L12008  T=11 F=9  T=0 F=0  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))
  d=5   L12008  T=11 F=0  T=0 F=0  if ((!terminate) && (!xmlParseLookupInternalSubset(ctxt)))
  d=5   L12011  T=9 F=0  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
--- d=4  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=4   L8409  T=0 F=18  T=30 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=4   L8409  T=0 F=18  T=0 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=4   L8430  T=3 F=15  T=0 F=30  if (RAW == '[')
  d=4   L8436  T=15 F=0  T=0 F=30  if (RAW != '>') {
--- d=4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=4   L10872  T=0 F=5  T=0 F=10  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=4   L10873  T=0 F=5  T=0 F=10  (ctxt->instate == XML_PARSER_EOF)) {
  d=4   L10907  T=6 F=0  T=0 F=10  if (RAW == '[') {
  d=4   L10910  T=6 F=0  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10918  T=0 F=0  T=10 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10918  T=0 F=0  T=10 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10919  T=0 F=0  T=10 F=0  (!ctxt->disableSAX))
  d=4   L10922  T=0 F=0  T=9 F=1  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10936  T=0 F=0  T=0 F=1  if (RAW != '<') {
  d=4   L10950  T=0 F=0  T=0 F=1  if (RAW != 0) {
  d=4   L10959  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10959  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10965  T=0 F=0  T=1 F=0  if ((ctxt->myDoc != NULL) &&
  d=4   L10966  T=0 F=0  T=0 F=1  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=4   L10971  T=0 F=0  T=0 F=1  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10980  T=0 F=0  T=1 F=0  if (! ctxt->wellFormed) {
--- d=3  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503) ---
  d=3   L8456  T=15 F=0  T=0 F=0  if (RAW == '[') {
  d=3   L8466  T=69 F=0  T=0 F=0  while (((RAW != ']') || (ctxt->inputNr > baseInputNr)) &&
  d=3   L8467  T=69 F=0  T=0 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L8473  T=0 F=69  T=0 F=0  if ((ctxt->inputNr > 1) && (ctxt->input->filename != NULL...
  d=3   L8476  T=3 F=0  T=0 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=3   L8476  T=33 F=36  T=0 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=3   L8476  T=30 F=3  T=0 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=3   L8478  T=21 F=15  T=0 F=0  } else if (RAW == '%') {
--- d=2  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=2   L7099  T=0 F=0  T=27 F=0  if ((ctxt->encoding == NULL) &&
  d=2   L7100  T=0 F=0  T=27 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=2   L7109  T=0 F=0  T=0 F=27  if (enc != XML_CHAR_ENCODING_NONE)
  d=2   L7123  T=0 F=0  T=0 F=27  if (ctxt->myDoc == NULL) {
  d=2   L7131  T=0 F=0  T=0 F=27  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=2   L7131  T=0 F=0  T=27 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=2   L7137  T=0 F=0  T=94 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=2   L7137  T=0 F=0  T=91 F=3  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=2   L7139  T=0 F=0  T=67 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=2   L7139  T=0 F=0  T=67 F=24  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=2   L7139  T=0 F=0  T=0 F=67  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=2   L7141  T=0 F=0  T=67 F=24  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=2   L7141  T=0 F=0  T=67 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=2   L7151  T=0 F=0  T=0 F=3  if (RAW != 0) {
--- d=1  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=1   L6952  T=33 F=0  T=67 F=0  if (CUR == '<') {
  d=1   L6953  T=30 F=3  T=67 F=0  if (NXT(1) == '!') {
  d=1   L6955  T=12 F=18  T=52 F=15  case 'E':
  d=1   L6956  T=12 F=0  T=50 F=2  if (NXT(3) == 'L')
  d=1   L6958  T=0 F=0  T=0 F=2  else if (NXT(3) == 'N')
  d=1   L6963  T=0 F=30  T=15 F=52  case 'A':
  d=1   L6966  T=0 F=30  T=0 F=67  case 'N':
  d=1   L6969  T=15 F=15  T=0 F=67  case '-':  <-- BLOCKER
  d=1   L6972  T=3 F=27  T=0 F=67  default:
  d=1   L6977  T=3 F=0  T=0 F=0  } else if (NXT(1) == '?') {
  d=1   L6986  T=0 F=33  T=0 F=67  if (ctxt->instate == XML_PARSER_EOF)

[off-chain: 784 additional divergent branches across 75 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=4235fea0a8124089, size=353 bytes, fuzzer=naive_ctx, trial=1, discovered_at=32485s, mutation_op=ByteRandMutator,QwordAddMutator,ByteInterestingMutator,BytesDeleteMutator,ByteDecMutator,BytesRandSetMutator,BytesDeleteMutator):
  0000: 67 ff ff ff ff ff 6c 5c 0a 3c 3f 78 6d 6c 20 76   g.....l\.<?xml v
  0010: 65 be be be be be b6 72 73 69 6f 6e c3 22 7a 2e   e......rsion."z.
  0020: 30 22 3d 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61   0"=>.<!DOCTYPE a
  0030: 39 39 30 30 30 65 65 49 53 4f 2d 4c 41 54 49 4e   99000eeISO-LATIN
Seed 2 (id=34f2310e21fd75b1, size=227 bytes, fuzzer=naive_ctx, trial=1, discovered_at=35162s, mutation_op=BytesDeleteMutator,TokenReplace):
  0000: 41 20 20 20 41 54 41 20 20 20 21 20 00 d0 01 18   A   ATA   ! ....
  0010: 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e   l\.<?xml version
  0020: 3c 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59   <"1.0"?>.<!DOCTY
  0030: 50 45 20 61 20 53 5b 3c 21 45 4c 45 4d 45 4e 54   PE a S[<!ELEMENT
Seed 3 (id=30e7c6920ffe0afc, size=394 bytes, fuzzer=naive_ctx, trial=1, discovered_at=37826s, mutation_op=ByteIncMutator,ByteInterestingMutator):
  0000: 41 20 20 20 41 54 41 20 20 00 00 03 e8 d0 01 00   A   ATA  .......
  0010: 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e   l\.<?xml version
  0020: 3c 22 31 2e 30 22 40 3e 0a 3c 21 44 4f 43 54 59   <"1.0"@>.<!DOCTY
  0030: 50 45 20 61 20 53 5b 3c 21 45 4c 45 4d 45 4e 54   PE a S[<!ELEMENT
Seed 4 (id=05d51b958c9abd3f, size=385 bytes, fuzzer=naive_ctx, trial=1, discovered_at=62365s, mutation_op=CrossoverReplaceMutator,BytesSetMutator,ByteRandMutator,BytesDeleteMutator,CrossoverInsertMutator,BytesDeleteMutator):
  0000: 49 58 45 44 27 68 74 00 d1 01 22 2f 77 77 74 2e   IXED'ht..."/wwt.
  0010: 77 33 7b 6f 72 67 2f 31 39 41 20 00 00 10 00 41   w3{org/19A ....A
  0020: 20 20 20 21 20 00 d0 01 18 6c 5c 0a 3c 3f 78 6d      ! ....l\.<?xm
  0030: 6c 20 76 65 72 73 96 6f 6e 3c 22 31 2e 30 22 3f   l vers.on<"1.0"?
Seed 5 (id=4a393bf07b84b39a, size=453 bytes, fuzzer=naive_ctx, trial=1, discovered_at=71935s, mutation_op=ByteDecMutator,ByteAddMutator,CrossoverInsertMutator):
  0000: 27 09 09 09 00 08 01 00 20 78 6c 09 09 09 0a 09   '....... xl.....
  0010: 08 09 09 26 26 2c 2c 2c 26 26 26 26 26 26 26 26   ...&&,,,&&&&&&&&
  0020: 26 26 26 0a 09 09 09 09 20 3c 61 20 78 6b 3a 74   &&&..... <a xk:t
  0030: 79 70 20 3c 62 20 35 35 35 35 35 35 2c 2c 39 39   yp <b 555555,,99

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=028449a3e7659dfa, size=389 bytes, fuzzer=naive, trial=1, discovered_at=4s, mutation_op=BytesDeleteMutator,BitFlipMutator,BytesSwapMutator,TokenInsert,ByteNegMutator,CrossoverInsertMutator):
  0000: 74 64 22 3e 0a 0a 3c 61 3e 0a 20 20 3c 62 20 06   td">..<a>.  <b .
  0010: 00 00 00 31 32 37 37 37 32 4a 78 6d 6c 5c 0a 3c   ...127772Jxml\.<
  0020: 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e   ?xml version="1.
  0030: 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61   0"?>.<!DOCTYPE a
Seed 2 (id=022872fb8319f510, size=611 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=CrossoverInsertMutator,WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=013a786979d45920, size=375 bytes, fuzzer=naive, trial=1, discovered_at=59s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=02f665196242465b, size=328 bytes, fuzzer=naive, trial=1, discovered_at=108s, mutation_op=BytesDeleteMutator,ByteNegMutator,BytesDeleteMutator):
  0000: c9 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   .2.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
Seed 5 (id=089ad774f736d538, size=667 bytes, fuzzer=naive, trial=1, discovered_at=118s, mutation_op=WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 5a 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   Z SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  41(A)x3 67(g)x1 49(I)x1 27(')x1     06(.)x4 3d(=)x2 74(t)x1 c9(.)x1 +2u  DIFFER
   0x0001  20( )x3 ff(.)x1 58(X)x1 09(.)x1     00(.)x5 64(d)x1 32(2)x1 22(")x1 +2u  DIFFER
   0x0002  20( )x3 ff(.)x1 45(E)x1 09(.)x1     00(.)x5 22(")x1 2e(.)x1 74(t)x1 +2u  PARTIAL
   0x0003  20( )x3 ff(.)x1 44(D)x1 09(.)x1     00(.)x5 74(t)x2 3e(>)x1 78(x)x1 +1u  DIFFER
   0x0004  41(A)x3 ff(.)x1 27(')x1 00(.)x1     31(1)x5 74(t)x2 0a(.)x1 6d(m)x1 +1u  DIFFER
   0x0005  54(T)x3 ff(.)x1 68(h)x1 08(.)x1     32(2)x5 70(p)x2 0a(.)x1 6c(l)x1 +1u  DIFFER
   0x0006  41(A)x3 6c(l)x1 74(t)x1 01(.)x1     37(7)x5 3a(:)x2 3c(<)x1 5c(\)x1 +1u  PARTIAL
   0x0007  20( )x3 00(.)x2 5c(\)x1             37(7)x5 2f(/)x2 61(a)x1 0a(.)x1 +1u  DIFFER
   0x0008  20( )x4 0a(.)x1 d1(.)x1             37(7)x5 2f(/)x2 3e(>)x1 3c(<)x1 +1u  DIFFER
   0x000d  d0(.)x3 6c(l)x1 77(w)x1 09(.)x1     6c(l)x5 62(b)x1 20( )x1 b6(.)x1 +2u  PARTIAL
   0x000e  01(.)x3 20( )x1 74(t)x1 0a(.)x1     5c(\)x5 20( )x1 76(v)x1 b6(.)x1 +2u  PARTIAL
   0x0010  6c(l)x3 65(e)x1 77(w)x1 08(.)x1     3c(<)x5 00(.)x1 72(r)x1 b6(.)x1 +2u  DIFFER
   0x0011  5c(\)x3 be(.)x1 33(3)x1 09(.)x1     3f(?)x5 00(.)x1 73(s)x1 b6(.)x1 +2u  DIFFER
   0x0012  0a(.)x3 be(.)x1 7b({)x1 09(.)x1     78(x)x5 00(.)x1 69(i)x1 b6(.)x1 +2u  DIFFER
   0x0013  3c(<)x3 be(.)x1 6f(o)x1 26(&)x1     6d(m)x5 31(1)x1 6f(o)x1 b6(.)x1 +2u  PARTIAL
   0x0014  3f(?)x3 be(.)x1 72(r)x1 26(&)x1     6c(l)x5 32(2)x1 6e(n)x1 61(a)x1 +2u  DIFFER
   0x0015  78(x)x3 be(.)x1 67(g)x1 2c(,)x1     20( )x5 37(7)x1 3d(=)x1 6b(k)x1 +2u  DIFFER
   0x0016  6d(m)x3 b6(.)x1 2f(/)x1 2c(,)x1     76(v)x5 37(7)x1 22(")x1 65(e)x1 +2u  DIFFER
   0x0017  6c(l)x3 72(r)x1 31(1)x1 2c(,)x1     65(e)x5 37(7)x1 31(1)x1 75(u)x1 +2u  PARTIAL
   0x0018  20( )x3 73(s)x1 39(9)x1 26(&)x1     72(r)x5 32(2)x1 2e(.)x1 28(()x1 +2u  PARTIAL
   0x0019  76(v)x3 69(i)x1 41(A)x1 26(&)x1     73(s)x6 4a(J)x1 30(0)x1 39(9)x1 +1u  DIFFER
   0x001a  65(e)x3 6f(o)x1 20( )x1 26(&)x1     69(i)x6 78(x)x1 22(")x1 2f(/)x1 +1u  DIFFER
   0x001b  72(r)x3 6e(n)x1 00(.)x1 26(&)x1     6f(o)x5 6d(m)x2 3f(?)x1 78(x)x1 +1u  DIFFER
   0x001c  73(s)x3 c3(.)x1 00(.)x1 26(&)x1     6e(n)x6 6c(l)x2 3e(>)x2             DIFFER
   0x001d  69(i)x3 22(")x1 10(.)x1 26(&)x1     3d(=)x5 5c(\)x1 0a(.)x1 3e(>)x1 +2u  PARTIAL
   0x001e  6f(o)x3 7a(z)x1 00(.)x1 26(&)x1     22(")x5 0a(.)x1 3c(<)x1 3e(>)x1 +2u  DIFFER
   0x001f  6e(n)x3 2e(.)x1 41(A)x1 26(&)x1     31(1)x5 3c(<)x1 21(!)x1 3e(>)x1 +2u  DIFFER
   0x0020  3c(<)x3 30(0)x1 20( )x1 26(&)x1     2e(.)x5 3f(?)x1 44(D)x1 20( )x1 +2u  PARTIAL
   0x0021  22(")x4 20( )x1 26(&)x1             30(0)x5 78(x)x1 4f(O)x1 d6(.)x1 +2u  DIFFER
   0x0022  31(1)x3 3d(=)x1 20( )x1 26(&)x1     22(")x5 6d(m)x1 43(C)x1 23(#)x1 +2u  DIFFER
   0x0023  2e(.)x3 3e(>)x1 21(!)x1 0a(.)x1     3f(?)x5 6c(l)x1 54(T)x1 46(F)x1 +2u  DIFFER
   0x0024  30(0)x3 0a(.)x1 20( )x1 09(.)x1     3e(>)x6 20( )x1 59(Y)x1 49(I)x1 +1u  PARTIAL
   0x0025  22(")x3 3c(<)x1 00(.)x1 09(.)x1     0a(.)x5 76(v)x1 50(P)x1 58(X)x1 +2u  DIFFER
   0x0026  3f(?)x2 21(!)x1 40(@)x1 d0(.)x1 +1u  3c(<)x6 45(E)x2 65(e)x1 2f(/)x1     DIFFER
   0x0027  3e(>)x3 44(D)x1 01(.)x1 09(.)x1     21(!)x5 72(r)x1 20( )x1 44(D)x1 +2u  PARTIAL
   0x0028  0a(.)x3 4f(O)x1 18(.)x1 20( )x1     44(D)x5 73(s)x1 61(a)x1 30(0)x1 +2u  DIFFER
   0x0029  3c(<)x4 43(C)x1 6c(l)x1             4f(O)x5 20( )x2 69(i)x1 27(')x1 +1u  DIFFER
   0x002a  21(!)x3 54(T)x1 5c(\)x1 61(a)x1     43(C)x5 74(t)x2 6f(o)x1 53(S)x1 +1u  DIFFER
   0x002b  44(D)x3 59(Y)x1 0a(.)x1 20( )x1     54(T)x5 6e(n)x1 59(Y)x1 69(i)x1 +2u  PARTIAL
   0x002c  4f(O)x3 50(P)x1 3c(<)x1 78(x)x1     59(Y)x5 3d(=)x1 53(S)x1 6d(m)x1 +2u  PARTIAL
   ... (19 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6674.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6674,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6674 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6674 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6674 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).