==== BLOCKER ====
Target: libxml2
Branch ID: 6467
Location: /src/libxml2/parser.c:2353:10
Enclosing function: xmlParseCharRef
Source line: 	    if (count++ > 20) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ctx_coverage vs naive_ctx); loser (value_profile vs value_profile)
cmplog                           4        6          0  REFERENCE
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog             8        2          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     2        8          0  REFERENCE
mopt                             2        7          1  REFERENCE
minimizer                        2        7          1  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=3.20h  loser=15.80h
  avg hitcount on branch: winner=57  loser=1
  prob_div=0.80  dur_div=12.60h  hit_div=57
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001
--- Pair 2: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=13.40h  loser=15.80h
  avg hitcount on branch: winner=8  loser=1
  prob_div=0.70  dur_div=2.40h  hit_div=7
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6467/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseCharRef (/src/libxml2/parser.c:2309-2400) ---
[ ]  2307   */
[ ]  2308  int
[B]  2309  xmlParseCharRef(xmlParserCtxtPtr ctxt) {
[B]  2310      int val = 0;
[B]  2311      int count = 0;
[ ]  2312  
[ ]  2313      /*
[ ]  2314       * Using RAW/CUR/NEXT is okay since we are working on ASCII range here
[ ]  2315       */
[B]  2316      if ((RAW == '&') && (NXT(1) == '#') &&
[B]  2317          (NXT(2) == 'x')) {
[ ]  2318  	SKIP(3);
[ ]  2319  	GROW;
[ ]  2320  	while (RAW != ';') { /* loop blocked by count */
[ ]  2321  	    if (count++ > 20) {
[ ]  2322  		count = 0;
[ ]  2323  		GROW;
[ ]  2324                  if (ctxt->instate == XML_PARSER_EOF)
[ ]  2325                      return(0);
[ ]  2326  	    }
[ ]  2327  	    if ((RAW >= '0') && (RAW <= '9'))
[ ]  2328  	        val = val * 16 + (CUR - '0');
[ ]  2329  	    else if ((RAW >= 'a') && (RAW <= 'f') && (count < 20))
[ ]  2330  	        val = val * 16 + (CUR - 'a') + 10;
[ ]  2331  	    else if ((RAW >= 'A') && (RAW <= 'F') && (count < 20))
[ ]  2332  	        val = val * 16 + (CUR - 'A') + 10;
[ ]  2333  	    else {
[ ]  2334  		xmlFatalErr(ctxt, XML_ERR_INVALID_HEX_CHARREF, NULL);
[ ]  2335  		val = 0;
[ ]  2336  		break;
[ ]  2337  	    }
[ ]  2338  	    if (val > 0x110000)
[ ]  2339  	        val = 0x110000;
[ ]  2340  
[ ]  2341  	    NEXT;
[ ]  2342  	    count++;
[ ]  2343  	}
[ ]  2344  	if (RAW == ';') {
[ ]  2345  	    /* on purpose to avoid reentrancy problems with NEXT and SKIP */
[ ]  2346  	    ctxt->input->col++;
[ ]  2347  	    ctxt->input->cur++;
[ ]  2348  	}
[B]  2349      } else if  ((RAW == '&') && (NXT(1) == '#')) {
[B]  2350  	SKIP(2);
[B]  2351  	GROW;
[B]  2352  	while (RAW != ';') { /* loop blocked by count */
[B]  2353  	    if (count++ > 20) { <-- BLOCKER
[W]  2354  		count = 0;
[W]  2355  		GROW;
[W]  2356                  if (ctxt->instate == XML_PARSER_EOF)
[ ]  2357                      return(0);
[W]  2358  	    }
[B]  2359  	    if ((RAW >= '0') && (RAW <= '9'))
[W]  2360  	        val = val * 10 + (CUR - '0');
[B]  2361  	    else {
[B]  2362  		xmlFatalErr(ctxt, XML_ERR_INVALID_DEC_CHARREF, NULL);
[B]  2363  		val = 0;
[B]  2364  		break;
[B]  2365  	    }
[W]  2366  	    if (val > 0x110000)
[W]  2367  	        val = 0x110000;
[ ]  2368  
[W]  2369  	    NEXT;
[W]  2370  	    count++;
[W]  2371  	}
[B]  2372  	if (RAW == ';') {
[ ]  2373  	    /* on purpose to avoid reentrancy problems with NEXT and SKIP */
[ ]  2374  	    ctxt->input->col++;
[ ]  2375  	    ctxt->input->cur++;
[ ]  2376  	}
[B]  2377      } else {
[ ]  2378          if (RAW == '&')
[ ]  2379              SKIP(1);
[ ]  2380          xmlFatalErr(ctxt, XML_ERR_INVALID_CHARREF, NULL);
[ ]  2381      }
[ ]  2382  
[ ]  2383      /*
[ ]  2384       * [ WFC: Legal Character ]
[ ]  2385       * Characters referred to using character references must match the
[ ]  2386       * production for Char.
[ ]  2387       */
[B]  2388      if (val >= 0x110000) {
[ ]  2389          xmlFatalErrMsgInt(ctxt, XML_ERR_INVALID_CHAR,
[ ]  2390                  "xmlParseCharRef: character reference out of bounds\n",
[ ]  2391  	        val);
[B]  2392      } else if (IS_CHAR(val)) {
[ ]  2393          return(val);
[B]  2394      } else {
[B]  2395          xmlFatalErrMsgInt(ctxt, XML_ERR_INVALID_CHAR,
[B]  2396                            "xmlParseCharRef: invalid xmlChar value %d\n",
[B]  2397  	                  val);
[B]  2398      }
[B]  2399      return(0);
[B]  2400  }

--- Caller (1 hop): parser.c:xmlParseAttValueComplex (/src/libxml2/parser.c:3948-4190, calls xmlParseCharRef at line 3991) (±10 around call site) ---
[ ]  3981      /*
[ ]  3982       * OK loop until we reach one of the ending char or a size limit.
[ ]  3983       */
[W]  3984      c = CUR_CHAR(l);
[W]  3985      while (((NXT(0) != limit) && /* checked */
[W]  3986              (IS_CHAR(c)) && (c != '<')) &&
[W]  3987              (ctxt->instate != XML_PARSER_EOF)) {
[W]  3988  	if (c == '&') {
[W]  3989  	    in_space = 0;
[W]  3990  	    if (NXT(1) == '#') {
[W]  3991  		int val = xmlParseCharRef(ctxt); <-- CALL
[ ]  3992  
[W]  3993  		if (val == '&') {
[ ]  3994  		    if (ctxt->replaceEntities) {
[ ]  3995  			if (len + 10 > buf_size) {
[ ]  3996  			    growBuffer(buf, 10);
[ ]  3997  			}
[ ]  3998  			buf[len++] = '&';
[ ]  3999  		    } else {
[ ]  4000  			/*
[ ]  4001  			 * The reparsing will be done in xmlStringGetNodeList()

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseAttValueComplex  (/src/libxml2/parser.c:3948-4190, calls xmlParseCharRef at line 3991)
hop 2  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls xmlParseCharRef at line 7191)
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
      67        10  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      53         4  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      39         4  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
      37         4  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
      34         8  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
       0        20  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
       7        22  parser.c:xmlFatalErrMsgInt  (/src/libxml2/parser.c:572-586)
      18         3  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
      15         0  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600)
       7        22  parser.c:xmlParseLookupCharData  (/src/libxml2/parser.c:11170-11184)
      15         3  nodePush  (/src/libxml2/parser.c:1750-1776)
      15         3  parser.c:nameNsPush  (/src/libxml2/parser.c:1820-1860)
      15         3  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
      15         3  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752)
      11         0  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
... (16 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=6  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752) ---
  d=6   L8641  T=0 F=15  T=0 F=3  if (RAW != '<') return(NULL);
  d=6   L8645  T=0 F=15  T=0 F=3  if (name == NULL) {
  d=6   L8659  T=18 F=4  T=0 F=3  while (((RAW != '>') &&
  d=6   L8660  T=18 F=0  T=0 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=6   L8661  T=15 F=0  T=0 F=0  (IS_BYTE_CHAR(RAW))) && (ctxt->instate != XML_PARSER_EOF)) {
  d=6   L8663  T=5 F=10  T=0 F=0  if (attname == NULL) {
  d=6   L8668  T=3 F=7  T=0 F=0  if (attvalue != NULL) {
  d=6   L8674  T=0 F=3  T=0 F=0  for (i = 0; i < nbatts;i += 2) {
  d=6   L8684  T=3 F=0  T=0 F=0  if (atts == NULL) {
  d=6   L8688  T=0 F=3  T=0 F=0  if (atts == NULL) {
  d=6   L8717  T=0 F=7  T=0 F=0  if (attvalue != NULL)
  d=6   L8724  T=0 F=7  T=0 F=0  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=6   L8724  T=3 F=7  T=0 F=0  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=6   L8726  T=7 F=0  T=0 F=0  if (SKIP_BLANKS == 0) {
  d=6   L8737  T=15 F=0  T=3 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElement != NU...
  d=6   L8737  T=15 F=0  T=3 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElement != NU...
  d=6   L8738  T=15 F=0  T=3 F=0  (!ctxt->disableSAX)) {
  d=6   L8739  T=3 F=12  T=0 F=3  if (nbatts > 0)
  d=6   L8745  T=9 F=6  T=0 F=3  if (atts != NULL) {
  d=6   L8747  T=3 F=9  T=0 F=0  for (i = 1;i < nbatts;i+=2)
  d=6   L8748  T=3 F=0  T=0 F=0  if (atts[i] != NULL)
--- d=6  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226) ---
  d=6   L10115  T=0 F=3  T=0 F=1  if (((unsigned int) ctxt->nameNr > xmlParserMaxDepth) &&
  d=6   L10125  T=0 F=3  T=0 F=1  if (ctxt->record_info) {
  d=6   L10131  T=0 F=3  T=0 F=1  if (ctxt->spaceNr == 0)
  d=6   L10133  T=0 F=3  T=0 F=1  else if (*ctxt->space == -2)
  d=6   L10140  T=0 F=3  T=0 F=1  if (ctxt->sax2)
  d=6   L10147  T=0 F=3  T=0 F=1  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10149  T=0 F=3  T=0 F=1  if (name == NULL) {
  d=6   L10162  T=0 F=3  T=0 F=1  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L10170  T=0 F=3  T=0 F=1  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L10196  T=2 F=1  T=1 F=0  if (RAW == '>') {
  d=6   L10209  T=0 F=1  T=0 F=0  if (nsNr != ctxt->nsNr)
  d=6   L10215  T=1 F=0  T=0 F=0  if ( ret != NULL && ctxt->record_info ) {
  d=6   L10215  T=0 F=1  T=0 F=0  if ( ret != NULL && ctxt->record_info ) {
--- d=5  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600) ---
  d=5   L8549  T=5 F=10  T=0 F=0  if (name == NULL) {
  d=5   L8559  T=6 F=4  T=0 F=0  if (RAW == '=') {
  d=5   L8575  T=0 F=6  T=0 F=0  if ((ctxt->pedantic) && (xmlStrEqual(name, BAD_CAST "xml:...
  d=5   L8586  T=0 F=6  T=0 F=0  if (xmlStrEqual(name, BAD_CAST "xml:space")) {
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10846  T=0 F=1  T=1 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=5   L10872  T=0 F=0  T=0 F=1  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=5   L10873  T=0 F=0  T=0 F=1  (ctxt->instate == XML_PARSER_EOF)) {
  d=5   L10907  T=0 F=0  T=0 F=1  if (RAW == '[') {
  d=5   L10918  T=0 F=0  T=1 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10918  T=0 F=0  T=1 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10919  T=0 F=0  T=1 F=0  (!ctxt->disableSAX))
  d=5   L10922  T=0 F=0  T=0 F=1  if (ctxt->instate == XML_PARSER_EOF)
--- d=4  xmlParseAttValue  (/src/libxml2/parser.c:4229-4232) ---
  d=4   L4230  T=0 F=6  T=0 F=0  if ((ctxt == NULL) || (ctxt->input == NULL)) return(NULL);
  d=4   L4230  T=0 F=6  T=0 F=0  if ((ctxt == NULL) || (ctxt->input == NULL)) return(NULL);
--- d=4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=4   L12296  T=6 F=0  T=4 F=1  if (ctxt->wellFormed == 0)
--- d=3  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203) ---
  d=3   L9063  T=0 F=6  T=0 F=0  int maxLength = (ctxt->options & XML_PARSE_HUGE) ?
  d=3   L9071  T=3 F=3  T=0 F=0  if (*in != '"' && *in != '\'') {
  d=3   L9071  T=3 F=0  T=0 F=0  if (*in != '"' && *in != '\'') {
  d=3   L9086  T=0 F=3  T=0 F=0  if (in >= end) {
  d=3   L9089  T=0 F=3  T=0 F=0  if (normalize) {
  d=3   L9165  T=21 F=0  T=0 F=0  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9165  T=21 F=0  T=0 F=0  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9165  T=21 F=0  T=0 F=0  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9166  T=18 F=0  T=0 F=0  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9166  T=21 F=0  T=0 F=0  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9166  T=18 F=3  T=0 F=0  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9169  T=0 F=18  T=0 F=0  if (in >= end) {
  d=3   L9179  T=0 F=3  T=0 F=0  if ((in - start) > maxLength) {
  d=3   L9184  T=3 F=0  T=0 F=0  if (*in != limit) goto need_complex;
  d=3   L9201  T=0 F=3  T=0 F=0  if (alloc) *alloc = 1;
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9980  T=2 F=2  T=0 F=3  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=0 F=2  T=0 F=0  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=2 F=2  T=0 F=3  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=0 F=2  T=0 F=0  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L10004  T=2 F=2  T=0 F=3  else if (*cur == '<') {
  d=3   L10005  T=0 F=2  T=0 F=0  if (NXT(1) == '/') {
--- d=3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=3   L11470  T=99 F=0  T=42 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=3   L11471  T=0 F=91  T=0 F=33  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11471  T=91 F=8  T=33 F=9  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11474  T=0 F=99  T=0 F=42  if (ctxt->input == NULL) break;
  d=3   L11475  T=0 F=99  T=0 F=42  if (ctxt->input->buf == NULL)
  d=3   L11486  T=95 F=4  T=39 F=3  if ((ctxt->instate != XML_PARSER_START) &&
  d=3   L11487  T=0 F=95  T=0 F=39  (ctxt->input->buf->raw != NULL) &&
  d=3   L11500  T=1 F=98  T=1 F=41  if (avail < 1)
  d=3   L11502  T=0 F=98  T=0 F=41  switch (ctxt->instate) {
  d=3   L11503  T=0 F=98  T=0 F=41  case XML_PARSER_EOF:
  d=3   L11508  T=4 F=94  T=3 F=38  case XML_PARSER_START:
  d=3   L11516  T=0 F=2  T=0 F=1  if (avail < 4)
  d=3   L11553  T=0 F=2  T=2 F=0  if ((cur == '<') && (next == '?')) {
  d=3   L11555  T=0 F=0  T=0 F=2  if (avail < 5) goto done;
  d=3   L11556  T=0 F=0  T=2 F=0  if ((!terminate) &&
  d=3   L11557  T=0 F=0  T=0 F=2  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11559  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11559  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11562  T=0 F=0  T=2 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=3   L11563  T=0 F=0  T=2 F=0  (ctxt->input->cur[3] == 'm') &&
  d=3   L11564  T=0 F=0  T=2 F=0  (ctxt->input->cur[4] == 'l') &&
  d=3   L11572  T=0 F=0  T=0 F=2  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=3   L11581  T=0 F=0  T=2 F=0  if ((ctxt->encoding == NULL) &&
  d=3   L11582  T=0 F=0  T=0 F=2  (ctxt->input->encoding != NULL))
  d=3   L11584  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11584  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11585  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=3   L11604  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11604  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11608  T=0 F=2  T=0 F=0  if (ctxt->version == NULL) {
  d=3   L11612  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11612  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11613  T=2 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=3   L11622  T=13 F=85  T=2 F=39  case XML_PARSER_START_TAG: {
  d=3   L11629  T=0 F=13  T=0 F=2  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11632  T=0 F=13  T=0 F=2  if (cur != '<') {
  d=3   L11639  T=1 F=10  T=0 F=2  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11639  T=11 F=2  T=2 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11641  T=0 F=12  T=0 F=2  if (ctxt->spaceNr == 0)
  d=3   L11643  T=6 F=6  T=0 F=2  else if (*ctxt->space == -2)
  d=3   L11648  T=0 F=12  T=0 F=2  if (ctxt->sax2)
  d=3   L11655  T=0 F=12  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11657  T=0 F=12  T=0 F=2  if (name == NULL) {
  d=3   L11670  T=0 F=12  T=0 F=2  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=3   L11678  T=0 F=12  T=0 F=2  if ((RAW == '/') && (NXT(1) == '>')) {
  d=3   L11707  T=5 F=7  T=2 F=0  if (RAW == '>') {
  d=3   L11721  T=79 F=19  T=32 F=9  case XML_PARSER_CONTENT: {
  d=3   L11722  T=0 F=79  T=0 F=32  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11727  T=0 F=14  T=0 F=0  if ((cur == '<') && (next == '/')) {
  d=3   L11727  T=14 F=65  T=0 F=32  if ((cur == '<') && (next == '/')) {
  d=3   L11730  T=0 F=14  T=0 F=0  } else if ((cur == '<') && (next == '?')) {
  d=3   L11730  T=14 F=65  T=0 F=32  } else if ((cur == '<') && (next == '?')) {
  d=3   L11736  T=10 F=4  T=0 F=0  } else if ((cur == '<') && (next != '!')) {
  d=3   L11736  T=14 F=65  T=0 F=32  } else if ((cur == '<') && (next != '!')) {
  d=3   L11739  T=4 F=65  T=0 F=32  } else if ((cur == '<') && (next == '!') &&
  d=3   L11739  T=4 F=0  T=0 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11740  T=0 F=4  T=0 F=0  (ctxt->input->cur[2] == '-') &&
  d=3   L11747  T=4 F=0  T=0 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11747  T=4 F=65  T=0 F=32  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11748  T=0 F=4  T=0 F=0  (ctxt->input->cur[2] == '[') &&
  d=3   L11758  T=4 F=65  T=0 F=32  } else if ((cur == '<') && (next == '!') &&
  d=3   L11758  T=4 F=0  T=0 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11759  T=0 F=4  T=0 F=0  (avail < 9)) {
  d=3   L11761  T=4 F=65  T=0 F=32  } else if (cur == '<') {
  d=3   L11765  T=38 F=27  T=8 F=24  } else if (cur == '&') {
  d=3   L11766  T=4 F=34  T=8 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11766  T=4 F=0  T=0 F=8  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11783  T=22 F=5  T=24 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=3   L11784  T=0 F=7  T=4 F=18  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=3   L11792  T=0 F=98  T=0 F=41  case XML_PARSER_END_TAG:
  d=3   L11813  T=0 F=98  T=0 F=41  case XML_PARSER_CDATA_SECTION: {
  d=3   L11904  T=2 F=96  T=2 F=39  case XML_PARSER_MISC:
  d=3   L11905  T=0 F=98  T=2 F=39  case XML_PARSER_PROLOG:
  d=3   L11906  T=0 F=98  T=0 F=41  case XML_PARSER_EPILOG:
  d=3   L11908  T=0 F=2  T=0 F=4  if (ctxt->input->buf == NULL)
  d=3   L11914  T=0 F=2  T=0 F=4  if (avail < 2)
  d=3   L11918  T=2 F=0  T=4 F=0  if ((cur == '<') && (next == '?')) {
  d=3   L11918  T=0 F=2  T=0 F=4  if ((cur == '<') && (next == '?')) {
  d=3   L11929  T=0 F=2  T=2 F=2  } else if ((cur == '<') && (next == '!') &&
  d=3   L11929  T=2 F=0  T=4 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11930  T=0 F=0  T=0 F=2  (ctxt->input->cur[2] == '-') &&
  d=3   L11942  T=2 F=0  T=2 F=2  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=3   L11943  T=0 F=2  T=2 F=0  (cur == '<') && (next == '!') &&
  d=3   L11944  T=0 F=0  T=2 F=0  (ctxt->input->cur[2] == 'D') &&
  d=3   L11945  T=0 F=0  T=2 F=0  (ctxt->input->cur[3] == 'O') &&
  d=3   L11946  T=0 F=0  T=2 F=0  (ctxt->input->cur[4] == 'C') &&
  d=3   L11947  T=0 F=0  T=2 F=0  (ctxt->input->cur[5] == 'T') &&
  d=3   L11948  T=0 F=0  T=2 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=3   L11949  T=0 F=0  T=2 F=0  (ctxt->input->cur[7] == 'P') &&
  d=3   L11950  T=0 F=0  T=2 F=0  (ctxt->input->cur[8] == 'E')) {
  d=3   L11951  T=0 F=0  T=2 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11951  T=0 F=0  T=0 F=2  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11959  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11961  T=0 F=0  T=0 F=2  if (RAW == '[') {
  d=3   L11972  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11972  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11973  T=0 F=0  T=2 F=0  (ctxt->sax->externalSubset != NULL))
  d=3   L12007  T=0 F=98  T=0 F=41  case XML_PARSER_DTD: {
  d=3   L12029  T=0 F=98  T=0 F=41  case XML_PARSER_COMMENT:
  d=3   L12038  T=0 F=98  T=0 F=41  case XML_PARSER_IGNORE:
  d=3   L12047  T=0 F=98  T=0 F=41  case XML_PARSER_PI:
  d=3   L12056  T=0 F=98  T=0 F=41  case XML_PARSER_ENTITY_DECL:
  d=3   L12065  T=0 F=98  T=0 F=41  case XML_PARSER_ENTITY_VALUE:
  d=3   L12074  T=0 F=98  T=0 F=41  case XML_PARSER_ATTRIBUTE_VALUE:
  d=3   L12083  T=0 F=98  T=0 F=41  case XML_PARSER_SYSTEM_LITERAL:
  d=3   L12092  T=0 F=98  T=0 F=41  case XML_PARSER_PUBLIC_LITERAL:
--- d=2  parser.c:xmlParseAttValueComplex  (/src/libxml2/parser.c:3948-4190) ---
  d=2   L3954  T=0 F=3  T=0 F=0  size_t maxLength = (ctxt->options & XML_PARSE_HUGE) ?
  d=2   L3961  T=3 F=0  T=0 F=0  if (NXT(0) == '"') {
  d=2   L3979  T=0 F=3  T=0 F=0  if (buf == NULL) goto mem_error;
  d=2   L3985  T=33 F=0  T=0 F=0  while (((NXT(0) != limit) && /* checked */
  d=2   L3986  T=30 F=0  T=0 F=0  (IS_CHAR(c)) && (c != '<')) &&
  d=2   L3986  T=30 F=3  T=0 F=0  (IS_CHAR(c)) && (c != '<')) &&
  d=2   L3987  T=30 F=0  T=0 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L3988  T=6 F=24  T=0 F=0  if (c == '&') {
  d=2   L3990  T=3 F=3  T=0 F=0  if (NXT(1) == '#') {
  d=2   L3993  T=0 F=3  T=0 F=0  if (val == '&') {
  d=2   L4013  T=0 F=3  T=0 F=0  } else if (val != 0) {
  d=2   L4021  T=0 F=3  T=0 F=0  if ((ent != NULL) &&
  d=2   L4036  T=0 F=3  T=0 F=0  } else if ((ent != NULL) &&
  d=2   L4070  T=0 F=3  T=0 F=0  } else if (ent != NULL) {
  d=2   L4132  T=0 F=21  T=0 F=0  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4132  T=3 F=21  T=0 F=0  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4132  T=0 F=21  T=0 F=0  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4132  T=0 F=21  T=0 F=0  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4133  T=3 F=0  T=0 F=0  if ((len != 0) || (!normalize)) {
  d=2   L4134  T=3 F=0  T=0 F=0  if ((!normalize) || (!in_space)) {
  d=2   L4136  T=0 F=3  T=0 F=0  while (len + 10 > buf_size) {
  d=2   L4145  T=0 F=21  T=0 F=0  if (len + 10 > buf_size) {
  d=2   L4153  T=0 F=30  T=0 F=0  if (len > maxLength) {
  d=2   L4159  T=0 F=3  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L4162  T=0 F=3  T=0 F=0  if ((in_space) && (normalize)) {
  d=2   L4166  T=0 F=3  T=0 F=0  if (RAW == '<') {
  d=2   L4168  T=3 F=0  T=0 F=0  } else if (RAW != limit) {
  d=2   L4169  T=0 F=3  T=0 F=0  if ((c != 0) && (!IS_CHAR(c))) {
  d=2   L4179  T=0 F=3  T=0 F=0  if (attlen != NULL) *attlen = len;
--- d=2  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=2   L7181  T=0 F=34  T=0 F=8  if (RAW != '&')
  d=2   L7187  T=0 F=34  T=4 F=4  if (NXT(1) == '#') {
  d=2   L7193  T=0 F=0  T=4 F=0  if (value == 0)
  d=2   L7233  T=34 F=0  T=4 F=0  if (ent == NULL) return;
--- d=1  xmlParseCharRef  (/src/libxml2/parser.c:2309-2400) ---
  d=1   L2352  T=111 F=0  T=4 F=0  while (RAW != ';') { /* loop blocked by count */
  d=1   L2353  T=9 F=102  T=0 F=4  if (count++ > 20) {  <-- BLOCKER
  d=1   L2356  T=0 F=9  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L2359  T=108 F=3  T=0 F=4  if ((RAW >= '0') && (RAW <= '9'))
  d=1   L2359  T=111 F=0  T=4 F=0  if ((RAW >= '0') && (RAW <= '9'))
  d=1   L2366  T=87 F=21  T=0 F=0  if (val > 0x110000)

[off-chain: 277 additional divergent branches across 34 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=4fac3b798d4c9cd5, size=752 bytes, fuzzer=naive_ctx, trial=1, discovered_at=46111s, mutation_op=BytesRandInsertMutator,BytesSwapMutator,ByteRandMutator,BytesRandSetMutator):
  0000: 23 23 23 0e 26 39 39 20 59 30 22 5d 5d 5d 5d 5d   ###.&99 Y0"]]]]]
  0010: 5d 5d 5d 5d 5d 5d 5d 5d 61 20 53 59 53 54 45 4d   ]]]]]]]]a SYSTEM
  0020: 00 22 64 74 64 73 2f 31 32 66 3d 22 68 c8 c8 c8   ."dtds/12f="h...
  0030: c8 c8 d3 c8 61 6b 65 75 ff ff 73 2f 31 32 37 37   ....akeu..s/1277

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=4a69ca4177404ba8, size=304 bytes, fuzzer=naive, trial=1, discovered_at=5686s, mutation_op=ByteDecMutator,DwordInterestingMutator,ByteRandMutator,BytesDeleteMutator):
  0000: 59 76 76 76 76 76 76 06 00 00 00 31 32 43 37 3f   Yvvvvvv....12C7?
  0010: 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72   2.xml\.<?xml ver
  0020: 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44   sion="1.0"?>.<!D
  0030: 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20   OCTYPE a SYSTEM 


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  23(#)x1                             59(Y)x1                             DIFFER
   0x0001  23(#)x1                             76(v)x1                             DIFFER
   0x0002  23(#)x1                             76(v)x1                             DIFFER
   0x0003  0e(.)x1                             76(v)x1                             DIFFER
   0x0004  26(&)x1                             76(v)x1                             DIFFER
   0x0005  39(9)x1                             76(v)x1                             DIFFER
   0x0006  39(9)x1                             76(v)x1                             DIFFER
   0x0007  20( )x1                             06(.)x1                             DIFFER
   0x0008  59(Y)x1                             00(.)x1                             DIFFER
   0x0009  30(0)x1                             00(.)x1                             DIFFER
   0x000a  22(")x1                             00(.)x1                             DIFFER
   0x000b  5d(])x1                             31(1)x1                             DIFFER
   0x000c  5d(])x1                             32(2)x1                             DIFFER
   0x000d  5d(])x1                             43(C)x1                             DIFFER
   0x000e  5d(])x1                             37(7)x1                             DIFFER
   0x000f  5d(])x1                             3f(?)x1                             DIFFER
   0x0010  5d(])x1                             32(2)x1                             DIFFER
   0x0011  5d(])x1                             2e(.)x1                             DIFFER
   0x0012  5d(])x1                             78(x)x1                             DIFFER
   0x0013  5d(])x1                             6d(m)x1                             DIFFER
   0x0014  5d(])x1                             6c(l)x1                             DIFFER
   0x0015  5d(])x1                             5c(\)x1                             DIFFER
   0x0016  5d(])x1                             0a(.)x1                             DIFFER
   0x0017  5d(])x1                             3c(<)x1                             DIFFER
   0x0018  61(a)x1                             3f(?)x1                             DIFFER
   0x0019  20( )x1                             78(x)x1                             DIFFER
   0x001a  53(S)x1                             6d(m)x1                             DIFFER
   0x001b  59(Y)x1                             6c(l)x1                             DIFFER
   0x001c  53(S)x1                             20( )x1                             DIFFER
   0x001d  54(T)x1                             76(v)x1                             DIFFER
   0x001e  45(E)x1                             65(e)x1                             DIFFER
   0x001f  4d(M)x1                             72(r)x1                             DIFFER
   0x0020  00(.)x1                             73(s)x1                             DIFFER
   0x0021  22(")x1                             69(i)x1                             DIFFER
   0x0022  64(d)x1                             6f(o)x1                             DIFFER
   0x0023  74(t)x1                             6e(n)x1                             DIFFER
   0x0024  64(d)x1                             3d(=)x1                             DIFFER
   0x0025  73(s)x1                             22(")x1                             DIFFER
   0x0026  2f(/)x1                             31(1)x1                             DIFFER
   0x0027  31(1)x1                             2e(.)x1                             DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6467.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6467,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage), value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6467 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6467 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6467 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).