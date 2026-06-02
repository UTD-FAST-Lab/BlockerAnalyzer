==== BLOCKER ====
Target: libxml2
Branch ID: 6605
Location: /src/libxml2/parser.c:5129:30
Enclosing function: xmlParsePITarget
Source line:         ((name[1] == 'm') || (name[1] == 'M')) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            8        2          0  winner (ctx_coverage vs naive_ctx)
cmplog                           9        1          0  REFERENCE
value_profile                    5        5          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        0       10          0  loser (ctx_coverage vs naive)
naive_ngram4                     8        2          0  REFERENCE
mopt                             9        1          0  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > naive_ctx  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=12.50h  loser=23.80h
  avg hitcount on branch: winner=6  loser=0
  prob_div=0.80  dur_div=11.30h  hit_div=6
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6605/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParsePITarget (/src/libxml2/parser.c:5123-5155) ---
[ ]  5121  
[ ]  5122  const xmlChar *
[B]  5123  xmlParsePITarget(xmlParserCtxtPtr ctxt) {
[B]  5124      const xmlChar *name;
[ ]  5125  
[B]  5126      name = xmlParseName(ctxt);
[B]  5127      if ((name != NULL) &&
[B]  5128          ((name[0] == 'x') || (name[0] == 'X')) &&
[B]  5129          ((name[1] == 'm') || (name[1] == 'M')) && <-- BLOCKER
[B]  5130          ((name[2] == 'l') || (name[2] == 'L'))) {
[W]  5131  	int i;
[W]  5132  	if ((name[0] == 'x') && (name[1] == 'm') &&
[W]  5133  	    (name[2] == 'l') && (name[3] == 0)) {
[ ]  5134  	    xmlFatalErrMsg(ctxt, XML_ERR_RESERVED_XML_NAME,
[ ]  5135  		 "XML declaration allowed only at the start of the document\n");
[ ]  5136  	    return(name);
[W]  5137  	} else if (name[3] == 0) {
[W]  5138  	    xmlFatalErr(ctxt, XML_ERR_RESERVED_XML_NAME, NULL);
[W]  5139  	    return(name);
[W]  5140  	}
[ ]  5141  	for (i = 0;;i++) {
[ ]  5142  	    if (xmlW3CPIs[i] == NULL) break;
[ ]  5143  	    if (xmlStrEqual(name, (const xmlChar *)xmlW3CPIs[i]))
[ ]  5144  	        return(name);
[ ]  5145  	}
[ ]  5146  	xmlWarningMsg(ctxt, XML_ERR_RESERVED_XML_NAME,
[ ]  5147  		      "xmlParsePITarget: invalid name prefix 'xml'\n",
[ ]  5148  		      NULL, NULL);
[ ]  5149      }
[L]  5150      if ((name != NULL) && (xmlStrchr(name, ':') != NULL)) {
[ ]  5151  	xmlNsErr(ctxt, XML_NS_ERR_COLON,
[ ]  5152  		 "colons are forbidden from PI names '%s'\n", name, NULL, NULL);
[ ]  5153      }
[L]  5154      return(name);
[B]  5155  }

--- Caller (1 hop): xmlParsePI (/src/libxml2/parser.c:5233-5371, calls xmlParsePITarget at line 5259) (±10 around call site) ---
[ ]  5249  	/*
[ ]  5250  	 * this is a Processing Instruction.
[ ]  5251  	 */
[B]  5252  	SKIP(2);
[B]  5253  	SHRINK;
[ ]  5254  
[ ]  5255  	/*
[ ]  5256  	 * Parse the target name and check for special support like
[ ]  5257  	 * namespace.
[ ]  5258  	 */
[B]  5259          target = xmlParsePITarget(ctxt); <-- CALL
[B]  5260  	if (target != NULL) {
[B]  5261  	    if ((RAW == '?') && (NXT(1) == '>')) {
[ ]  5262  		if (inputid != ctxt->input->id) {
[ ]  5263  		    xmlFatalErrMsg(ctxt, XML_ERR_ENTITY_BOUNDARY,
[ ]  5264  	                           "PI declaration doesn't start and stop in"
[ ]  5265                                     " the same entity\n");
[ ]  5266  		}
[ ]  5267  		SKIP(2);
[ ]  5268  
[ ]  5269  		/*

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParsePI  (/src/libxml2/parser.c:5233-5371, calls xmlParsePITarget at line 5259)
hop 3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParsePI at line 9981)
hop 3  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParsePI at line 6978)
hop 4  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 4  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 4  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 4  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 5  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 5  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 5  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 5  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 5  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 6  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 6  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 6  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 6  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 6  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 6  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 7  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseDocTypeDecl at line 11958)
hop 7  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 7  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 7  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)
hop 8  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 8  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 8  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        84  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      86         5  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      98        17  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      60         0  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600)
      55        11  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
      43         0  parser.c:xmlFatalErrMsgInt  (/src/libxml2/parser.c:572-586)
      43         5  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706)
      52        16  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
      32         0  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752)
      30         0  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
      36         8  parser.c:xmlParseLookupCharData  (/src/libxml2/parser.c:11170-11184)
       9        36  inputPop  (/src/libxml2/parser.c:1723-1738)
      29         5  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       0        23  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      26         8  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
... (35 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=8   L12139  T=0 F=5  T=0 F=21  if (ctxt == NULL)
  d=8   L12141  T=3 F=2  T=4 F=17  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L12143  T=0 F=5  T=0 F=21  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L12145  T=0 F=5  T=0 F=21  if (ctxt->input == NULL)
  d=8   L12149  T=2 F=3  T=14 F=7  if (ctxt->instate == XML_PARSER_START)
  d=8   L12151  T=4 F=0  T=9 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=8   L12151  T=4 F=1  T=9 F=12  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=8   L12151  T=4 F=0  T=9 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=8   L12152  T=0 F=4  T=0 F=9  (chunk[size - 1] == '\r')) {
  d=8   L12159  T=4 F=0  T=9 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=8   L12159  T=4 F=0  T=9 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=8   L12159  T=4 F=1  T=9 F=12  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=8   L12160  T=4 F=0  T=9 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=8   L12160  T=4 F=0  T=9 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=8   L12170  T=2 F=2  T=8 F=1  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=8   L12170  T=2 F=0  T=8 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=8   L12171  T=2 F=0  T=8 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=8   L12171  T=0 F=2  T=0 F=8  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=8   L12202  T=0 F=4  T=0 F=9  if (res < 0) {
  d=8   L12211  T=1 F=0  T=12 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=8   L12212  T=1 F=0  T=12 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=8   L12212  T=1 F=0  T=12 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=8   L12214  T=0 F=1  T=0 F=12  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=8   L12233  T=0 F=5  T=0 F=21  if (remain != 0) {
  d=8   L12238  T=1 F=4  T=4 F=17  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L12241  T=4 F=0  T=17 F=0  if ((ctxt->input != NULL) &&
  d=8   L12242  T=0 F=4  T=0 F=17  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=8   L12243  T=0 F=4  T=0 F=17  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=8   L12248  T=0 F=4  T=0 F=8  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L12248  T=4 F=0  T=8 F=9  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L12251  T=0 F=4  T=0 F=17  if (remain != 0) {
  d=8   L12257  T=0 F=4  T=0 F=17  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=8   L12268  T=0 F=4  T=4 F=13  if (terminate) {
  d=8   L12274  T=0 F=0  T=4 F=0  if (ctxt->input != NULL) {
  d=8   L12275  T=0 F=0  T=0 F=4  if (ctxt->input->buf == NULL)
  d=8   L12283  T=0 F=0  T=4 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=8   L12284  T=0 F=0  T=4 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=8   L12287  T=0 F=0  T=0 F=4  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=8   L12290  T=0 F=0  T=4 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=8   L12291  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L12291  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L12296  T=4 F=0  T=4 F=13  if (ctxt->wellFormed == 0)
--- d=7  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=7   L11409  T=0 F=5  T=0 F=21  if (ctxt->input == NULL)
  d=7   L11465  T=5 F=0  T=21 F=0  if ((ctxt->input != NULL) &&
  d=7   L11466  T=0 F=5  T=0 F=21  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=7   L11471  T=0 F=85  T=0 F=30  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L11500  T=0 F=91  T=4 F=75  if (avail < 1)
  d=7   L11509  T=2 F=2  T=8 F=14  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=7   L11516  T=0 F=2  T=0 F=8  if (avail < 4)
  d=7   L11535  T=0 F=2  T=0 F=14  if (avail < 2)
  d=7   L11539  T=0 F=2  T=0 F=14  if (cur == 0) {
  d=7   L11553  T=2 F=0  T=14 F=0  if ((cur == '<') && (next == '?')) {
  d=7   L11553  T=2 F=0  T=14 F=0  if ((cur == '<') && (next == '?')) {
  d=7   L11555  T=0 F=2  T=0 F=14  if (avail < 5) goto done;
  d=7   L11556  T=2 F=0  T=10 F=4  if ((!terminate) &&
  d=7   L11557  T=0 F=2  T=6 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=7   L11559  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L11559  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L11562  T=2 F=0  T=6 F=2  if ((ctxt->input->cur[2] == 'x') &&
  d=7   L11563  T=0 F=2  T=0 F=6  (ctxt->input->cur[3] == 'm') &&
  d=7   L11594  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=7   L11594  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=7   L11595  T=2 F=0  T=8 F=0  (!ctxt->disableSAX))
  d=7   L11632  T=0 F=25  T=4 F=11  if (cur != '<') {
  d=7   L11635  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11635  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11639  T=4 F=20  T=3 F=4  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=7   L11639  T=24 F=1  T=7 F=4  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=7   L11641  T=0 F=21  T=0 F=8  if (ctxt->spaceNr == 0)
  d=7   L11643  T=0 F=21  T=2 F=6  else if (*ctxt->space == -2)
  d=7   L11648  T=0 F=21  T=8 F=0  if (ctxt->sax2)
  d=7   L11655  T=0 F=21  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L11657  T=1 F=20  T=0 F=8  if (name == NULL) {
  d=7   L11660  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11660  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11670  T=0 F=20  T=0 F=8  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=7   L11678  T=0 F=20  T=0 F=8  if ((RAW == '/') && (NXT(1) == '>')) {
  d=7   L11707  T=4 F=16  T=4 F=4  if (RAW == '>') {
  d=7   L11722  T=0 F=56  T=0 F=18  if ((avail < 2) && (ctxt->inputNr == 1))
  d=7   L11727  T=0 F=20  T=2 F=4  if ((cur == '<') && (next == '/')) {
  d=7   L11727  T=20 F=36  T=6 F=12  if ((cur == '<') && (next == '/')) {
  d=7   L11730  T=0 F=20  T=0 F=4  } else if ((cur == '<') && (next == '?')) {
  d=7   L11730  T=20 F=36  T=4 F=12  } else if ((cur == '<') && (next == '?')) {
  d=7   L11736  T=20 F=0  T=4 F=0  } else if ((cur == '<') && (next != '!')) {
  d=7   L11736  T=20 F=36  T=4 F=12  } else if ((cur == '<') && (next != '!')) {
  d=7   L11739  T=0 F=36  T=0 F=12  } else if ((cur == '<') && (next == '!') &&
  d=7   L11747  T=0 F=36  T=0 F=12  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=7   L11758  T=0 F=36  T=0 F=12  } else if ((cur == '<') && (next == '!') &&
  d=7   L11761  T=0 F=36  T=0 F=12  } else if (cur == '<') {
  d=7   L11765  T=0 F=36  T=0 F=12  } else if (cur == '&') {
  d=7   L11782  T=36 F=0  T=12 F=0  if ((ctxt->inputNr == 1) &&
  d=7   L11783  T=36 F=0  T=12 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=7   L11784  T=0 F=36  T=4 F=4  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=7   L11784  T=36 F=0  T=8 F=4  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=7   L11792  T=0 F=91  T=2 F=73  case XML_PARSER_END_TAG:
  d=7   L11793  T=0 F=0  T=0 F=2  if (avail < 2)
  d=7   L11795  T=0 F=0  T=0 F=2  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=7   L11795  T=0 F=0  T=2 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=7   L11797  T=0 F=0  T=2 F=0  if (ctxt->sax2) {
  d=7   L11805  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF) {
  d=7   L11807  T=0 F=0  T=0 F=2  } else if (ctxt->nameNr == 0) {
  d=7   L11908  T=0 F=6  T=0 F=18  if (ctxt->input->buf == NULL)
  d=7   L11914  T=0 F=6  T=0 F=18  if (avail < 2)
  d=7   L11918  T=6 F=0  T=14 F=4  if ((cur == '<') && (next == '?')) {
  d=7   L11918  T=2 F=4  T=8 F=6  if ((cur == '<') && (next == '?')) {
  d=7   L11919  T=2 F=0  T=4 F=4  if ((!terminate) &&
  d=7   L11920  T=0 F=2  T=0 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=7   L11927  T=0 F=2  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L11929  T=4 F=0  T=6 F=4  } else if ((cur == '<') && (next == '!') &&
  d=7   L11942  T=2 F=2  T=8 F=2  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=7   L11943  T=2 F=0  T=2 F=2  (cur == '<') && (next == '!') &&
  d=7   L11943  T=2 F=0  T=4 F=4  (cur == '<') && (next == '!') &&
  d=7   L11985  T=0 F=2  T=0 F=4  } else if ((cur == '<') && (next == '!') &&
  d=7   L11985  T=2 F=0  T=4 F=4  } else if ((cur == '<') && (next == '!') &&
  d=7   L11989  T=0 F=2  T=0 F=8  } else if (ctxt->instate == XML_PARSER_EPILOG) {
--- d=6  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=6   L8436  T=3 F=0  T=0 F=3  if (RAW != '>') {
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10816  T=0 F=1  T=0 F=4  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10816  T=0 F=1  T=0 F=4  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10829  T=1 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10829  T=1 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10831  T=0 F=1  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10834  T=1 F=0  T=4 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L10835  T=1 F=0  T=4 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=5   L10846  T=0 F=1  T=0 F=4  if (enc != XML_CHAR_ENCODING_NONE) {
  d=5   L10852  T=0 F=1  T=0 F=4  if (CUR == 0) {
  d=5   L10863  T=0 F=1  T=0 F=4  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=5   L10884  T=1 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=1 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=1 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10886  T=0 F=1  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10888  T=1 F=0  T=4 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10888  T=1 F=0  T=4 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10889  T=1 F=0  T=4 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10889  T=0 F=1  T=0 F=4  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10936  T=0 F=1  T=2 F=2  if (RAW != '<') {
  d=5   L10950  T=0 F=1  T=1 F=1  if (RAW != 0) {
  d=5   L10959  T=1 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10959  T=1 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10965  T=1 F=0  T=4 F=0  if ((ctxt->myDoc != NULL) &&
  d=5   L10966  T=0 F=1  T=0 F=4  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=5   L10971  T=0 F=1  T=0 F=4  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=5   L10980  T=1 F=0  T=4 F=0  if (! ctxt->wellFormed) {
--- d=4  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=4   L10077  T=0 F=1  T=1 F=1  if (xmlParseElementStart(ctxt) != 0)
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9973  T=29 F=1  T=5 F=1  while ((RAW != 0) &&
  d=3   L9974  T=29 F=0  T=5 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L9980  T=10 F=19  T=2 F=3  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=0 F=10  T=0 F=2  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=10 F=19  T=2 F=3  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=0 F=10  T=0 F=2  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L10004  T=10 F=19  T=2 F=3  else if (*cur == '<') {
  d=3   L10005  T=0 F=10  T=1 F=1  if (NXT(1) == '/') {
  d=3   L10006  T=0 F=0  T=0 F=1  if (ctxt->nameNr <= nameNr)
  d=3   L10019  T=0 F=19  T=0 F=3  else if (*cur == '&') {
--- d=2  xmlParsePI  (/src/libxml2/parser.c:5233-5371) ---
  d=2   L5237  T=3 F=0  T=9 F=3  size_t maxLength = (ctxt->options & XML_PARSE_HUGE) ?
  d=2   L5245  T=3 F=0  T=12 F=0  if ((RAW == '<') && (NXT(1) == '?')) {
  d=2   L5245  T=3 F=0  T=12 F=0  if ((RAW == '<') && (NXT(1) == '?')) {
  d=2   L5260  T=3 F=0  T=12 F=0  if (target != NULL) {
  d=2   L5261  T=0 F=3  T=0 F=12  if ((RAW == '?') && (NXT(1) == '>')) {
  d=2   L5281  T=0 F=3  T=0 F=12  if (buf == NULL) {
  d=2   L5286  T=0 F=3  T=6 F=6  if (SKIP_BLANKS == 0) {
  d=2   L5292  T=0 F=3  T=3 F=6  ((cur != '?') || (NXT(1) != '>'))) {
  d=2   L5292  T=39 F=3  T=348 F=9  ((cur != '?') || (NXT(1) != '>'))) {
  d=2   L5293  T=0 F=39  T=0 F=351  if (len + 5 >= size) {
  d=2   L5307  T=0 F=39  T=3 F=348  if (count > 50) {
  d=2   L5310  T=0 F=0  T=0 F=3  if (ctxt->instate == XML_PARSER_EOF) {
  d=2   L5319  T=0 F=39  T=6 F=345  if (cur == 0) {
  d=2   L5324  T=0 F=39  T=0 F=351  if (len > maxLength) {
  d=2   L5333  T=0 F=3  T=6 F=6  if (cur != '?') {
  d=2   L5337  T=0 F=3  T=0 F=6  if (inputid != ctxt->input->id) {
  d=2   L5345  T=2 F=1  T=4 F=2  if (((state == XML_PARSER_MISC) ||
  d=2   L5346  T=1 F=0  T=2 F=0  (state == XML_PARSER_START)) &&
  d=2   L5347  T=0 F=3  T=0 F=6  (xmlStrEqual(target, XML_CATALOG_PI))) {
  d=2   L5359  T=3 F=0  T=6 F=0  if ((ctxt->sax) && (!ctxt->disableSAX) &&
  d=2   L5359  T=3 F=0  T=6 F=0  if ((ctxt->sax) && (!ctxt->disableSAX) &&
  d=2   L5360  T=3 F=0  T=6 F=0  (ctxt->sax->processingInstruction != NULL))
  d=2   L5368  T=3 F=0  T=12 F=0  if (ctxt->instate != XML_PARSER_EOF)
--- d=1  xmlParsePITarget  (/src/libxml2/parser.c:5123-5155) ---
  d=1   L5127  T=3 F=0  T=12 F=0  if ((name != NULL) &&
  d=1   L5128  T=0 F=0  T=3 F=0  ((name[0] == 'x') || (name[0] == 'X')) &&
  d=1   L5128  T=3 F=0  T=9 F=3  ((name[0] == 'x') || (name[0] == 'X')) &&
  d=1   L5129  T=3 F=0  T=0 F=12  ((name[1] == 'm') || (name[1] == 'M')) &&  <-- BLOCKER
  d=1   L5129  T=0 F=3  T=0 F=12  ((name[1] == 'm') || (name[1] == 'M')) &&  <-- BLOCKER
  d=1   L5130  T=3 F=0  T=0 F=0  ((name[2] == 'l') || (name[2] == 'L'))) {
  d=1   L5132  T=0 F=3  T=0 F=0  if ((name[0] == 'x') && (name[1] == 'm') &&
  d=1   L5132  T=3 F=0  T=0 F=0  if ((name[0] == 'x') && (name[1] == 'm') &&
  d=1   L5137  T=3 F=0  T=0 F=0  } else if (name[3] == 0) {
  d=1   L5150  T=0 F=0  T=12 F=0  if ((name != NULL) && (xmlStrchr(name, ':') != NULL)) {
  d=1   L5150  T=0 F=0  T=0 F=12  if ((name != NULL) && (xmlStrchr(name, ':') != NULL)) {

[off-chain: 566 additional divergent branches across 53 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=7487b63144c7c532, size=369 bytes, fuzzer=naive, trial=4, discovered_at=66093s, mutation_op=DwordAddMutator,BytesDeleteMutator):
  0000: 29 3e 0a 3b 4c 4c 4c 4c 4c 4c 31 32 37 37 37 32   )>.;LLLLLL127772
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 4d 6c 20 76 65 72 73   .xml\.<?xMl vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 0a 0a 0a 3c   ion="1.0"?>....<
  0030: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=3e162df03660718c, size=362 bytes, fuzzer=naive_ctx, trial=1, discovered_at=889s, mutation_op=BytesRandInsertMutator,ByteFlipMutator,BytesInsertCopyMutator,DwordAddMutator,ByteRandMutator,BytesInsertCopyMutator):
  0000: 21 45 4c 45 4d 45 4e 54 20 62 20 22 3e 28 23 50   !ELEMENT b ">(#P
  0010: 43 44 41 54 41 29 3e 0a 3c 21 41 54 54 4c 49 53   CDATA)>.<!ATTLIS
  0020: 54 20 62 20 78 6d 6c 74 70 3a 2f 2f 77 77 77 2e   T b xmltp://www.
  0030: 77 33 2e 6f 72 67 2f 31 39 39 39 2f 78 6c 69 6e   w3.org/1999/xlin
Seed 2 (id=2ae9a3625d8f1692, size=142 bytes, fuzzer=naive_ctx, trial=1, discovered_at=6797s, mutation_op=ByteNegMutator,BytesCopyMutator,BytesDeleteMutator,QwordAddMutator):
  0000: 2f 49 00 00 00 7f 38 35 39 2d 2f 49 00 00 00 7f   /I....859-/I....
  0010: 38 35 39 2d 37 2f 65 75 72 6c 2e 6e 3c 3c 3c 22   859-7/eurl.n<<<"
  0020: 48 54 4d 4c 3c 3c 2c 61 61 61 61 61 61 51 3c 54   HTML<<,aaaaaaQ<T
  0030: 2e 78 6d 6c 5c 0a 3c 3f 78 5f 6c 20 76 65 72 73   .xml\.<?x_l vers
Seed 3 (id=30e32927c802e948, size=154 bytes, fuzzer=naive_ctx, trial=1, discovered_at=7224s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,BytesDeleteMutator,BitFlipMutator,BytesSwapMutator):
  0000: 2d 2d 2d 2d 37 37 32 42 43 2d 2d 2e 2d 2d 2d 2d   ----772BC--.----
  0010: 74 2e 20 78 73 69 6d 00 48 b8 48 48 48 4d 48 48   t. xsim.H.HHHMHH
  0020: 48 48 48 0f 31 32 38 37 37 3f 42 43 2d 2d 2d 2d   HHH.12877?BC----
  0030: 2d 2d 2d 2d 2d 2d 2d 2d 2d 85 85 85 00 00 00 31   ---------......1
Seed 4 (id=4a7f9249b4a1ab68, size=219 bytes, fuzzer=naive_ctx, trial=1, discovered_at=13101s, mutation_op=BytesRandInsertMutator,BytesInsertCopyMutator):
  0000: 0f 66 3d 22 68 74 53 70 3a 2f 2f 66 61 6b 65 b9   .f="htSp://fake.
  0010: b9 b9 b9 b9 b9 66 61 6b 65 b9 b9 b9 b9 b9 b9 75   .....fake......u
  0020: 72 6c 2e 66 65 74 22 3e 62 3f 74 65 78 74 3c 2f   rl.fet">b?text</
  0030: 62 c2 0a 3c 2f 61 3e 0a 0a 5c 0f 0f 0f 0f 0f 0f   b..</a>..\......


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  29())x1                             21(!)x1 2f(/)x1 2d(-)x1 0f(.)x1     DIFFER
   0x0001  3e(>)x1                             45(E)x1 49(I)x1 2d(-)x1 66(f)x1     DIFFER
   0x0002  0a(.)x1                             4c(L)x1 00(.)x1 2d(-)x1 3d(=)x1     DIFFER
   0x0003  3b(;)x1                             45(E)x1 00(.)x1 2d(-)x1 22(")x1     DIFFER
   0x0004  4c(L)x1                             4d(M)x1 00(.)x1 37(7)x1 68(h)x1     DIFFER
   0x0005  4c(L)x1                             45(E)x1 7f(.)x1 37(7)x1 74(t)x1     DIFFER
   0x0006  4c(L)x1                             4e(N)x1 38(8)x1 32(2)x1 53(S)x1     DIFFER
   0x0007  4c(L)x1                             54(T)x1 35(5)x1 42(B)x1 70(p)x1     DIFFER
   0x0008  4c(L)x1                             20( )x1 39(9)x1 43(C)x1 3a(:)x1     DIFFER
   0x0009  4c(L)x1                             2d(-)x2 62(b)x1 2f(/)x1             DIFFER
   0x000a  31(1)x1                             2f(/)x2 20( )x1 2d(-)x1             DIFFER
   0x000b  32(2)x1                             22(")x1 49(I)x1 2e(.)x1 66(f)x1     DIFFER
   0x000c  37(7)x1                             3e(>)x1 00(.)x1 2d(-)x1 61(a)x1     DIFFER
   0x000d  37(7)x1                             28(()x1 00(.)x1 2d(-)x1 6b(k)x1     DIFFER
   0x000e  37(7)x1                             23(#)x1 00(.)x1 2d(-)x1 65(e)x1     DIFFER
   0x000f  32(2)x1                             50(P)x1 7f(.)x1 2d(-)x1 b9(.)x1     DIFFER
   0x0010  2e(.)x1                             43(C)x1 38(8)x1 74(t)x1 b9(.)x1     DIFFER
   0x0011  78(x)x1                             44(D)x1 35(5)x1 2e(.)x1 b9(.)x1     DIFFER
   0x0012  6d(m)x1                             41(A)x1 39(9)x1 20( )x1 b9(.)x1     DIFFER
   0x0013  6c(l)x1                             54(T)x1 2d(-)x1 78(x)x1 b9(.)x1     DIFFER
   0x0014  5c(\)x1                             41(A)x1 37(7)x1 73(s)x1 b9(.)x1     DIFFER
   0x0015  0a(.)x1                             29())x1 2f(/)x1 69(i)x1 66(f)x1     DIFFER
   0x0016  3c(<)x1                             3e(>)x1 65(e)x1 6d(m)x1 61(a)x1     DIFFER
   0x0017  3f(?)x1                             0a(.)x1 75(u)x1 00(.)x1 6b(k)x1     DIFFER
   0x0018  78(x)x1                             3c(<)x1 72(r)x1 48(H)x1 65(e)x1     DIFFER
   0x0019  4d(M)x1                             21(!)x1 6c(l)x1 b8(.)x1 b9(.)x1     DIFFER
   0x001a  6c(l)x1                             41(A)x1 2e(.)x1 48(H)x1 b9(.)x1     DIFFER
   0x001b  20( )x1                             54(T)x1 6e(n)x1 48(H)x1 b9(.)x1     DIFFER
   0x001c  76(v)x1                             54(T)x1 3c(<)x1 48(H)x1 b9(.)x1     DIFFER
   0x001d  65(e)x1                             4c(L)x1 3c(<)x1 4d(M)x1 b9(.)x1     DIFFER
   0x001e  72(r)x1                             49(I)x1 3c(<)x1 48(H)x1 b9(.)x1     DIFFER
   0x001f  73(s)x1                             53(S)x1 22(")x1 48(H)x1 75(u)x1     DIFFER
   0x0020  69(i)x1                             48(H)x2 54(T)x1 72(r)x1             DIFFER
   0x0021  6f(o)x1                             20( )x1 54(T)x1 48(H)x1 6c(l)x1     DIFFER
   0x0022  6e(n)x1                             62(b)x1 4d(M)x1 48(H)x1 2e(.)x1     DIFFER
   0x0023  3d(=)x1                             20( )x1 4c(L)x1 0f(.)x1 66(f)x1     DIFFER
   0x0024  22(")x1                             78(x)x1 3c(<)x1 31(1)x1 65(e)x1     DIFFER
   0x0025  31(1)x1                             6d(m)x1 3c(<)x1 32(2)x1 74(t)x1     DIFFER
   0x0026  2e(.)x1                             6c(l)x1 2c(,)x1 38(8)x1 22(")x1     DIFFER
   0x0027  30(0)x1                             74(t)x1 61(a)x1 37(7)x1 3e(>)x1     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6605.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6605,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>naive_ctx (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6605 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6605 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6605 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).