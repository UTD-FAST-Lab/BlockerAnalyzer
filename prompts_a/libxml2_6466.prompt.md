==== BLOCKER ====
Target: libxml2
Branch ID: 6466
Location: /src/libxml2/parser.c:2352:9
Enclosing function: xmlParseCharRef
Source line: 	while (RAW != ';') { /* loop blocked by count */
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (value_profile vs value_profile)
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog)
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=13.70h  loser=18.60h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=4.90h  hit_div=4
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.90h  loser=16.00h
  avg hitcount on branch: winner=8  loser=0
  prob_div=0.60  dur_div=8.10h  hit_div=8
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6466/{W,L}/branch_coverage_show.txt

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
[B]  2352  	while (RAW != ';') { /* loop blocked by count */ <-- BLOCKER
[B]  2353  	    if (count++ > 20) {
[W]  2354  		count = 0;
[W]  2355  		GROW;
[W]  2356                  if (ctxt->instate == XML_PARSER_EOF)
[ ]  2357                      return(0);
[W]  2358  	    }
[B]  2359  	    if ((RAW >= '0') && (RAW <= '9'))
[B]  2360  	        val = val * 10 + (CUR - '0');
[B]  2361  	    else {
[B]  2362  		xmlFatalErr(ctxt, XML_ERR_INVALID_DEC_CHARREF, NULL);
[B]  2363  		val = 0;
[B]  2364  		break;
[B]  2365  	    }
[B]  2366  	    if (val > 0x110000)
[W]  2367  	        val = 0x110000;
[ ]  2368  
[B]  2369  	    NEXT;
[B]  2370  	    count++;
[B]  2371  	}
[B]  2372  	if (RAW == ';') {
[ ]  2373  	    /* on purpose to avoid reentrancy problems with NEXT and SKIP */
[W]  2374  	    ctxt->input->col++;
[W]  2375  	    ctxt->input->cur++;
[W]  2376  	}
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
[W]  2393          return(val);
[B]  2394      } else {
[B]  2395          xmlFatalErrMsgInt(ctxt, XML_ERR_INVALID_CHAR,
[B]  2396                            "xmlParseCharRef: invalid xmlChar value %d\n",
[B]  2397  	                  val);
[B]  2398      }
[B]  2399      return(0);
[B]  2400  }

--- Caller (1 hop): xmlParseReference (/src/libxml2/parser.c:7173-7586, calls xmlParseCharRef at line 7191) (±10 around call site) ---
[B]  7181      if (RAW != '&')
[ ]  7182          return;
[ ]  7183  
[ ]  7184      /*
[ ]  7185       * Simple case of a CharRef
[ ]  7186       */
[B]  7187      if (NXT(1) == '#') {
[B]  7188  	int i = 0;
[B]  7189  	xmlChar out[16];
[B]  7190  	int hex = NXT(2);
[B]  7191  	int value = xmlParseCharRef(ctxt); <-- CALL
[ ]  7192  
[B]  7193  	if (value == 0)
[B]  7194  	    return;
[W]  7195  	if (ctxt->charset != XML_CHAR_ENCODING_UTF8) {
[ ]  7196  	    /*
[ ]  7197  	     * So we are using non-UTF-8 buffers
[ ]  7198  	     * Check that the char fit on 8bits, if not
[ ]  7199  	     * generate a CharRef.
[ ]  7200  	     */
[W]  7201  	    if (value <= 0xFF) {

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
     210       641  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
     209        60  parser.c:xmlParseLookupChar  (/src/libxml2/parser.c:11108-11124)
      14       123  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      14       109  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
     114        31  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600)
      12        75  parser.c:xmlGetNamespace  (/src/libxml2/parser.c:8856-8867)
      14        68  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774)
       0        50  parser.c:xmlSHRINK  (/src/libxml2/parser.c:2059-2066)
       6        53  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      12        59  parser.c:xmlParseLookupString  (/src/libxml2/parser.c:11137-11161)
       0        41  parser.c:xmlParseAttribute2  (/src/libxml2/parser.c:9225-9323)
      15        48  xmlParseVersionInfo  (/src/libxml2/parser.c:10347-10378)
      15        48  xmlParseXMLDecl  (/src/libxml2/parser.c:10658-10766)
       0        25  parser.c:xmlParseNameAndCompare  (/src/libxml2/parser.c:3549-3576)
       9        33  xmlParseVersionNum  (/src/libxml2/parser.c:10284-10329)
... (14 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=8   L7099  T=0 F=0  T=3 F=0  if ((ctxt->encoding == NULL) &&
  d=8   L7100  T=0 F=0  T=3 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=8   L7109  T=0 F=0  T=0 F=3  if (enc != XML_CHAR_ENCODING_NONE)
  d=8   L7123  T=0 F=0  T=0 F=3  if (ctxt->myDoc == NULL) {
  d=8   L7131  T=0 F=0  T=0 F=3  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=8   L7131  T=0 F=0  T=3 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=8   L7137  T=0 F=0  T=6 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=8   L7137  T=0 F=0  T=3 F=3  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=8   L7139  T=0 F=0  T=3 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=8   L7139  T=0 F=0  T=3 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=8   L7139  T=0 F=0  T=0 F=3  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=8   L7141  T=0 F=0  T=3 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=8   L7141  T=0 F=0  T=3 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=8   L7151  T=0 F=0  T=0 F=3  if (RAW != 0) {
--- d=7  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=7   L6952  T=0 F=0  T=3 F=0  if (CUR == '<') {
  d=7   L6953  T=0 F=0  T=3 F=0  if (NXT(1) == '!') {
  d=7   L6955  T=0 F=0  T=3 F=0  case 'E':
  d=7   L6956  T=0 F=0  T=3 F=0  if (NXT(3) == 'L')
  d=7   L6963  T=0 F=0  T=0 F=3  case 'A':
  d=7   L6966  T=0 F=0  T=0 F=3  case 'N':
  d=7   L6969  T=0 F=0  T=0 F=3  case '-':
  d=7   L6972  T=0 F=0  T=0 F=3  default:
  d=7   L6986  T=0 F=0  T=0 F=3  if (ctxt->instate == XML_PARSER_EOF)
--- d=6  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752) ---
  d=6   L8660  T=0 F=0  T=1 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=6   L8660  T=117 F=0  T=36 F=1  ((RAW != '/') || (NXT(1) != '>')) &&
  d=6   L8661  T=114 F=0  T=31 F=0  (IS_BYTE_CHAR(RAW))) && (ctxt->instate != XML_PARSER_EOF)) {
  d=6   L8663  T=67 F=47  T=10 F=21  if (attname == NULL) {
  d=6   L8668  T=14 F=33  T=15 F=6  if (attvalue != NULL) {
  d=6   L8684  T=11 F=3  T=15 F=0  if (atts == NULL) {
  d=6   L8696  T=0 F=3  T=0 F=0  } else if (nbatts + 4 > maxatts) {
  d=6   L8717  T=0 F=33  T=0 F=6  if (attvalue != NULL)
  d=6   L8724  T=0 F=44  T=0 F=8  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=6   L8724  T=3 F=44  T=13 F=8  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=6   L8726  T=44 F=0  T=8 F=0  if (SKIP_BLANKS == 0) {
  d=6   L8738  T=94 F=0  T=69 F=5  (!ctxt->disableSAX)) {
--- d=6  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226) ---
  d=6   L10162  T=0 F=0  T=0 F=2  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L10162  T=0 F=35  T=2 F=50  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L10170  T=0 F=0  T=1 F=2  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L10170  T=0 F=35  T=3 F=49  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L10172  T=0 F=0  T=1 F=0  if (ctxt->sax2) {
  d=6   L10173  T=0 F=0  T=1 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->endElementNs != NU...
  d=6   L10173  T=0 F=0  T=1 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->endElementNs != NU...
  d=6   L10174  T=0 F=0  T=1 F=0  (!ctxt->disableSAX))
  d=6   L10185  T=0 F=0  T=0 F=1  if (nsNr != ctxt->nsNr)
  d=6   L10187  T=0 F=0  T=1 F=0  if ( ret != NULL && ctxt->record_info ) {
  d=6   L10187  T=0 F=0  T=0 F=1  if ( ret != NULL && ctxt->record_info ) {
  d=6   L10215  T=23 F=0  T=13 F=5  if ( ret != NULL && ctxt->record_info ) {
--- d=5  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600) ---
  d=5   L8549  T=67 F=47  T=10 F=21  if (name == NULL) {
  d=5   L8559  T=14 F=33  T=15 F=6  if (RAW == '=') {
  d=5   L8575  T=0 F=14  T=0 F=0  if ((ctxt->pedantic) && (xmlStrEqual(name, BAD_CAST "xml:...
  d=5   L8575  T=14 F=0  T=0 F=15  if ((ctxt->pedantic) && (xmlStrEqual(name, BAD_CAST "xml:...
--- d=5  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774) ---
  d=5   L9369  T=0 F=14  T=0 F=68  if (RAW != '<') return(NULL);
  d=5   L9391  T=2 F=12  T=7 F=61  if (localname == NULL) {
  d=5   L9406  T=0 F=12  T=41 F=25  while (((RAW != '>') &&
  d=5   L9407  T=0 F=0  T=35 F=6  ((RAW != '/') || (NXT(1) != '>')) &&
  d=5   L9407  T=0 F=0  T=6 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=5   L9408  T=0 F=0  T=41 F=0  (IS_BYTE_CHAR(RAW))) && (ctxt->instate != XML_PARSER_EOF)) {
  d=5   L9413  T=0 F=0  T=14 F=27  if (attname == NULL) {
  d=5   L9418  T=0 F=0  T=11 F=16  if (attvalue == NULL)
  d=5   L9420  T=0 F=0  T=0 F=16  if (len < 0) len = xmlStrlen(attvalue);
  d=5   L9422  T=0 F=0  T=0 F=16  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
  d=5   L9475  T=0 F=0  T=0 F=16  } else if (aprefix == ctxt->str_xmlns) {
  d=5   L9548  T=0 F=0  T=0 F=2  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=5   L9548  T=0 F=0  T=14 F=2  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=5   L9549  T=0 F=0  T=0 F=14  if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
  d=5   L9564  T=0 F=0  T=13 F=3  if (alloc)
  d=5   L9574  T=0 F=0  T=13 F=3  if (alloc != 0) attval = 1;
  d=5   L9579  T=0 F=0  T=0 F=27  if ((attvalue != NULL) && (alloc != 0)) {
  d=5   L9585  T=0 F=0  T=0 F=27  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L9587  T=0 F=0  T=3 F=0  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=5   L9587  T=0 F=0  T=3 F=20  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=5   L9587  T=0 F=0  T=4 F=23  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=5   L9589  T=0 F=0  T=15 F=5  if (SKIP_BLANKS == 0) {
  d=5   L9597  T=0 F=12  T=0 F=61  if (ctxt->input->id != inputid) {
  d=5   L9605  T=0 F=12  T=16 F=61  for (i = 0, j = 0; j < nratts; i += 5, j++) {
  d=5   L9606  T=0 F=0  T=3 F=13  if (atts[i+2] != NULL) {
  d=5   L9621  T=0 F=12  T=0 F=61  if (ctxt->attsDefault != NULL) {
  d=5   L9704  T=0 F=12  T=16 F=61  for (i = 0; i < nbatts;i += 5) {
  d=5   L9708  T=0 F=0  T=14 F=2  if (atts[i + 1] != NULL) {
  d=5   L9710  T=0 F=0  T=14 F=0  if (nsname == NULL) {
  d=5   L9724  T=0 F=0  T=0 F=16  for (j = 0; j < i;j += 5) {
  d=5   L9741  T=0 F=12  T=0 F=61  if ((prefix != NULL) && (nsname == NULL)) {
  d=5   L9752  T=12 F=0  T=61 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=5   L9752  T=12 F=0  T=61 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=5   L9753  T=12 F=0  T=39 F=22  (!ctxt->disableSAX)) {
  d=5   L9754  T=0 F=12  T=0 F=39  if (nbNs > 0)
  d=5   L9767  T=0 F=12  T=13 F=48  if (attval != 0) {
  d=5   L9768  T=0 F=0  T=13 F=13  for (i = 3,j = 0; j < nratts;i += 5,j++)
  d=5   L9769  T=0 F=0  T=13 F=0  if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))
  d=5   L9769  T=0 F=0  T=13 F=0  if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10872  T=0 F=5  T=0 F=16  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=5   L10873  T=0 F=5  T=0 F=16  (ctxt->instate == XML_PARSER_EOF)) {
  d=5   L10884  T=13 F=0  T=21 F=3  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10888  T=13 F=0  T=21 F=3  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10907  T=0 F=5  T=0 F=14  if (RAW == '[') {
  d=5   L10918  T=5 F=0  T=14 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10918  T=5 F=0  T=14 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10919  T=5 F=0  T=13 F=1  (!ctxt->disableSAX))
  d=5   L10922  T=0 F=5  T=0 F=14  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10965  T=13 F=0  T=21 F=3  if ((ctxt->myDoc != NULL) &&
--- d=4  parser.c:xmlParseAttribute2  (/src/libxml2/parser.c:9225-9323) ---
  d=4   L9233  T=0 F=0  T=11 F=30  if (name == NULL) {
  d=4   L9242  T=0 F=0  T=0 F=30  if (ctxt->attsSpecial != NULL) {
  d=4   L9255  T=0 F=0  T=19 F=11  if (RAW == '=') {
  d=4   L9259  T=0 F=0  T=3 F=16  if (val == NULL)
  d=4   L9261  T=0 F=0  T=0 F=16  if (normalize) {
  d=4   L9286  T=0 F=0  T=0 F=16  if (*prefix == ctxt->str_xml) {
--- d=4  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=4   L10084  T=11 F=0  T=13 F=7  if (CUR == 0) {
--- d=4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=4   L12139  T=0 F=54  T=0 F=132  if (ctxt == NULL)
  d=4   L12141  T=0 F=28  T=19 F=28  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12141  T=28 F=26  T=47 F=85  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12143  T=0 F=54  T=0 F=113  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12145  T=0 F=54  T=0 F=113  if (ctxt->input == NULL)
  d=4   L12149  T=26 F=28  T=69 F=44  if (ctxt->instate == XML_PARSER_START)
  d=4   L12151  T=41 F=13  T=80 F=33  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12152  T=0 F=41  T=1 F=79  (chunk[size - 1] == '\r')) {
  d=4   L12159  T=41 F=13  T=80 F=33  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12170  T=26 F=0  T=54 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=4   L12171  T=26 F=0  T=54 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12171  T=0 F=26  T=0 F=54  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12211  T=13 F=0  T=33 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12212  T=13 F=0  T=33 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12212  T=13 F=0  T=33 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12214  T=0 F=13  T=0 F=33  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=4   L12233  T=0 F=54  T=0 F=113  if (remain != 0) {
  d=4   L12238  T=1 F=53  T=3 F=110  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12241  T=53 F=0  T=110 F=0  if ((ctxt->input != NULL) &&
  d=4   L12242  T=0 F=53  T=0 F=110  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=4   L12243  T=0 F=53  T=0 F=110  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=4   L12248  T=0 F=53  T=22 F=51  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12248  T=53 F=0  T=73 F=37  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12257  T=0 F=0  T=1 F=0  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=4   L12257  T=0 F=53  T=1 F=87  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=4   L12258  T=0 F=0  T=1 F=0  (ctxt->input->buf != NULL)) {
  d=4   L12284  T=12 F=0  T=11 F=3  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=4   L12287  T=0 F=0  T=0 F=3  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=4   L12287  T=0 F=12  T=3 F=11  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=4   L12296  T=53 F=0  T=44 F=44  if (ctxt->wellFormed == 0)
--- d=3  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203) ---
  d=3   L9063  T=14 F=0  T=8 F=26  int maxLength = (ctxt->options & XML_PARSE_HUGE) ?
  d=3   L9071  T=11 F=3  T=3 F=31  if (*in != '"' && *in != '\'') {
  d=3   L9071  T=0 F=11  T=3 F=0  if (*in != '"' && *in != '\'') {
  d=3   L9086  T=0 F=14  T=0 F=31  if (in >= end) {
  d=3   L9089  T=0 F=14  T=0 F=31  if (normalize) {
  d=3   L9165  T=68 F=0  T=284 F=0  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9165  T=54 F=11  T=275 F=0  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9165  T=65 F=3  T=275 F=9  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9166  T=54 F=0  T=253 F=2  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9166  T=54 F=0  T=258 F=17  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9166  T=54 F=0  T=255 F=3  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9169  T=0 F=54  T=0 F=253  if (in >= end) {
  d=3   L9179  T=0 F=14  T=0 F=31  if ((in - start) > maxLength) {
  d=3   L9184  T=11 F=3  T=22 F=9  if (*in != limit) goto need_complex;
  d=3   L9188  T=0 F=3  T=3 F=6  if (len != NULL) {
  d=3   L9189  T=0 F=0  T=3 F=0  if (alloc) *alloc = 0;
  d=3   L9193  T=0 F=3  T=0 F=6  if (alloc) *alloc = 1;
  d=3   L9201  T=0 F=11  T=13 F=9  if (alloc) *alloc = 1;
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9973  T=269 F=11  T=628 F=13  while ((RAW != 0) &&
  d=3   L9974  T=269 F=0  T=628 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L9980  T=33 F=236  T=75 F=553  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=4 F=29  T=3 F=72  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=29 F=236  T=72 F=553  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=5 F=24  T=27 F=45  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9996  T=0 F=5  T=0 F=27  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=3   L10004  T=29 F=236  T=72 F=553  else if (*cur == '<') {
  d=3   L10005  T=0 F=29  T=13 F=59  if (NXT(1) == '/') {
  d=3   L10006  T=0 F=0  T=7 F=6  if (ctxt->nameNr <= nameNr)
  d=3   L10019  T=85 F=151  T=306 F=247  else if (*cur == '&') {
--- d=3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=3   L11409  T=0 F=54  T=0 F=113  if (ctxt->input == NULL)
  d=3   L11465  T=54 F=0  T=113 F=0  if ((ctxt->input != NULL) &&
  d=3   L11466  T=0 F=54  T=0 F=113  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=3   L11471  T=0 F=772  T=22 F=678  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11509  T=21 F=26  T=32 F=69  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=3   L11535  T=0 F=26  T=0 F=69  if (avail < 2)
  d=3   L11539  T=0 F=26  T=0 F=69  if (cur == 0) {
  d=3   L11553  T=10 F=16  T=59 F=8  if ((cur == '<') && (next == '?')) {
  d=3   L11553  T=26 F=0  T=67 F=2  if ((cur == '<') && (next == '?')) {
  d=3   L11555  T=0 F=10  T=0 F=59  if (avail < 5) goto done;
  d=3   L11556  T=10 F=0  T=49 F=10  if ((!terminate) &&
  d=3   L11557  T=0 F=10  T=21 F=28  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11559  T=10 F=0  T=38 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11559  T=10 F=0  T=38 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11562  T=10 F=0  T=32 F=6  if ((ctxt->input->cur[2] == 'x') &&
  d=3   L11563  T=10 F=0  T=32 F=0  (ctxt->input->cur[3] == 'm') &&
  d=3   L11564  T=10 F=0  T=32 F=0  (ctxt->input->cur[4] == 'l') &&
  d=3   L11572  T=0 F=10  T=0 F=32  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=3   L11581  T=10 F=0  T=32 F=0  if ((ctxt->encoding == NULL) &&
  d=3   L11582  T=0 F=10  T=0 F=32  (ctxt->input->encoding != NULL))
  d=3   L11584  T=10 F=0  T=32 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11584  T=10 F=0  T=32 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11585  T=10 F=0  T=26 F=6  (!ctxt->disableSAX))
  d=3   L11594  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11594  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11595  T=0 F=0  T=6 F=0  (!ctxt->disableSAX))
  d=3   L11643  T=24 F=48  T=0 F=83  else if (*ctxt->space == -2)
  d=3   L11657  T=1 F=71  T=0 F=83  if (name == NULL) {
  d=3   L11660  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11660  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11678  T=0 F=0  T=2 F=5  if ((RAW == '/') && (NXT(1) == '>')) {
  d=3   L11678  T=0 F=71  T=7 F=76  if ((RAW == '/') && (NXT(1) == '>')) {
  d=3   L11681  T=0 F=0  T=2 F=0  if (ctxt->sax2) {
  d=3   L11682  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) &&
  d=3   L11683  T=0 F=0  T=2 F=0  (ctxt->sax->endElementNs != NULL) &&
  d=3   L11684  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=3   L11687  T=0 F=0  T=0 F=2  if (ctxt->nsNr - nsNr > 0)
  d=3   L11697  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11700  T=0 F=0  T=0 F=2  if (ctxt->nameNr == 0) {
  d=3   L11727  T=0 F=74  T=13 F=71  if ((cur == '<') && (next == '/')) {
  d=3   L11731  T=2 F=6  T=4 F=0  if ((!terminate) &&
  d=3   L11732  T=2 F=0  T=0 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11766  T=15 F=194  T=16 F=38  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11783  T=374 F=0  T=331 F=9  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=3   L11784  T=3 F=324  T=9 F=127  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=3   L11792  T=0 F=852  T=14 F=914  case XML_PARSER_END_TAG:
  d=3   L11793  T=0 F=0  T=0 F=14  if (avail < 2)
  d=3   L11795  T=0 F=0  T=2 F=4  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11795  T=0 F=0  T=6 F=8  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11797  T=0 F=0  T=3 F=9  if (ctxt->sax2) {
  d=3   L11805  T=0 F=0  T=0 F=12  if (ctxt->instate == XML_PARSER_EOF) {
  d=3   L11807  T=0 F=0  T=7 F=5  } else if (ctxt->nameNr == 0) {
  d=3   L11906  T=0 F=852  T=7 F=921  case XML_PARSER_EPILOG:
  d=3   L11908  T=0 F=36  T=0 F=79  if (ctxt->input->buf == NULL)
  d=3   L11914  T=0 F=36  T=4 F=75  if (avail < 2)
  d=3   L11918  T=36 F=0  T=72 F=3  if ((cur == '<') && (next == '?')) {
  d=3   L11918  T=0 F=36  T=6 F=66  if ((cur == '<') && (next == '?')) {
  d=3   L11919  T=0 F=0  T=6 F=0  if ((!terminate) &&
  d=3   L11920  T=0 F=0  T=0 F=6  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11927  T=0 F=0  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11929  T=36 F=0  T=66 F=3  } else if ((cur == '<') && (next == '!') &&
  d=3   L11930  T=0 F=10  T=0 F=26  (ctxt->input->cur[2] == '-') &&
  d=3   L11944  T=10 F=0  T=26 F=0  (ctxt->input->cur[2] == 'D') &&
  d=3   L11945  T=10 F=0  T=26 F=0  (ctxt->input->cur[3] == 'O') &&
  d=3   L11946  T=10 F=0  T=26 F=0  (ctxt->input->cur[4] == 'C') &&
  d=3   L11947  T=10 F=0  T=26 F=0  (ctxt->input->cur[5] == 'T') &&
  d=3   L11948  T=10 F=0  T=26 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=3   L11949  T=10 F=0  T=26 F=0  (ctxt->input->cur[7] == 'P') &&
  d=3   L11950  T=10 F=0  T=26 F=0  (ctxt->input->cur[8] == 'E')) {
  d=3   L11951  T=10 F=0  T=26 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11951  T=0 F=10  T=0 F=26  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11959  T=0 F=10  T=0 F=26  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11961  T=0 F=10  T=0 F=26  if (RAW == '[') {
  d=3   L11972  T=10 F=0  T=26 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11972  T=10 F=0  T=26 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11973  T=10 F=0  T=26 F=0  (ctxt->sax->externalSubset != NULL))
  d=3   L11985  T=26 F=0  T=40 F=3  } else if ((cur == '<') && (next == '!') &&
  d=3   L11989  T=0 F=26  T=3 F=40  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=3   L11996  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11996  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
--- d=2  parser.c:xmlParseAttValueComplex  (/src/libxml2/parser.c:3948-4190) ---
  d=2   L3954  T=11 F=0  T=2 F=20  size_t maxLength = (ctxt->options & XML_PARSE_HUGE) ?
  d=2   L3961  T=0 F=11  T=22 F=0  if (NXT(0) == '"') {
  d=2   L3965  T=11 F=0  T=0 F=0  } else if (NXT(0) == '\'') {
  d=2   L3979  T=0 F=11  T=0 F=22  if (buf == NULL) goto mem_error;
  d=2   L3985  T=148 F=0  T=760 F=13  while (((NXT(0) != limit) && /* checked */
  d=2   L3986  T=137 F=8  T=751 F=6  (IS_CHAR(c)) && (c != '<')) &&
  d=2   L3986  T=145 F=3  T=757 F=3  (IS_CHAR(c)) && (c != '<')) &&
  d=2   L3987  T=137 F=0  T=751 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L3988  T=3 F=134  T=226 F=525  if (c == '&') {
  d=2   L3990  T=0 F=3  T=21 F=205  if (NXT(1) == '#') {
  d=2   L3993  T=0 F=0  T=0 F=21  if (val == '&') {
  d=2   L4013  T=0 F=0  T=0 F=21  } else if (val != 0) {
  d=2   L4021  T=0 F=3  T=0 F=205  if ((ent != NULL) &&
  d=2   L4036  T=0 F=3  T=0 F=205  } else if ((ent != NULL) &&
  d=2   L4070  T=0 F=3  T=0 F=205  } else if (ent != NULL) {
  d=2   L4132  T=25 F=103  T=34 F=473  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4132  T=6 F=128  T=18 F=507  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4132  T=0 F=128  T=0 F=507  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4132  T=0 F=103  T=15 F=458  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4133  T=20 F=11  T=67 F=0  if ((len != 0) || (!normalize)) {
  d=2   L4133  T=11 F=0  T=0 F=0  if ((len != 0) || (!normalize)) {
  d=2   L4134  T=31 F=0  T=67 F=0  if ((!normalize) || (!in_space)) {
  d=2   L4136  T=0 F=31  T=0 F=67  while (len + 10 > buf_size) {
  d=2   L4145  T=0 F=103  T=0 F=458  if (len + 10 > buf_size) {
  d=2   L4153  T=0 F=137  T=0 F=751  if (len > maxLength) {
  d=2   L4159  T=0 F=11  T=0 F=22  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L4162  T=8 F=3  T=12 F=10  if ((in_space) && (normalize)) {
  d=2   L4166  T=8 F=3  T=6 F=16  if (RAW == '<') {
  d=2   L4168  T=3 F=0  T=3 F=13  } else if (RAW != limit) {
  d=2   L4169  T=3 F=0  T=0 F=0  if ((c != 0) && (!IS_CHAR(c))) {
  d=2   L4169  T=3 F=0  T=0 F=3  if ((c != 0) && (!IS_CHAR(c))) {
  d=2   L4179  T=0 F=11  T=13 F=9  if (attlen != NULL) *attlen = len;
--- d=2  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=2   L7193  T=49 F=39  T=56 F=0  if (value == 0)
  d=2   L7195  T=20 F=19  T=0 F=0  if (ctxt->charset != XML_CHAR_ENCODING_UTF8) {
  d=2   L7201  T=0 F=20  T=0 F=0  if (value <= 0xFF) {
  d=2   L7208  T=0 F=20  T=0 F=0  if ((hex == 'x') || (hex == 'X'))
  d=2   L7208  T=0 F=20  T=0 F=0  if ((hex == 'x') || (hex == 'X'))
  d=2   L7212  T=20 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->reference != NULL) &&
  d=2   L7212  T=20 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->reference != NULL) &&
  d=2   L7213  T=20 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=2   L7222  T=19 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->characters != NULL...
  d=2   L7222  T=19 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->characters != NULL...
  d=2   L7223  T=19 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=2   L7233  T=207 F=0  T=436 F=0  if (ent == NULL) return;
--- d=1  xmlParseCharRef  (/src/libxml2/parser.c:2309-2400) ---
  d=1   L2352  T=355 F=53  T=89 F=0  while (RAW != ';') { /* loop blocked by count */  <-- BLOCKER
  d=1   L2353  T=8 F=347  T=0 F=89  if (count++ > 20) {
  d=1   L2356  T=0 F=8  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L2359  T=320 F=24  T=12 F=42  if ((RAW >= '0') && (RAW <= '9'))
  d=1   L2359  T=344 F=11  T=54 F=35  if ((RAW >= '0') && (RAW <= '9'))
  d=1   L2366  T=48 F=272  T=0 F=12  if (val > 0x110000)
  d=1   L2372  T=53 F=35  T=0 F=77  if (RAW == ';') {

[off-chain: 410 additional divergent branches across 49 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=64a4b4422c19f87e, size=110 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=8330s, mutation_op=TokenReplace,BytesInsertCopyMutator,WordAddMutator,ByteRandMutator,ByteInterestingMutator):
  0000: 6b 27 0a 2f 2b 20 7e 20 20 20 20 20 2f 9f 20 78   k'./+ ~     /. x
  0010: 6c 69 6e 6b 3a 5c 0a 3c ff 45 3e 45 4d 45 4e 54   link:\.<.E>EMENT
  0020: 24 61 09 28 62 5f 29 3e 0d 09 24 21 45 30 73 5c   $a.(b_)>..$!E0s\
  0030: 6d 70 6c 65 27 09 5f 3c 27 3c 24 7e 09 2e 2a 40   mple'._<'<$~..*@
Seed 2 (id=00c3a873ee0130d6, size=221 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=12679s, mutation_op=BytesCopyMutator,CrossoverInsertMutator,ByteFlipMutator,DwordAddMutator):
  0000: 6b d8 0a 20 2b 20 7e 20 20 3a 20 20 20 9f 3a fc   k.. + ~  :   .:.
  0010: ff ff ff 6b 3a 5c 0a 3c f5 45 3e 45 4d 0f 00 20   ...k:\.<.E>EM.. 
  0020: 20 20 20 20 20 20 20 20 20 20 78 6c 69 6e 6b 3a             xlink:
  0030: 68 72 65 66 20 20 20 43 44 41 54 41 20 fa 00 45   href   CDATA ..E
Seed 3 (id=8c0d2a87de6f96f9, size=306 bytes, fuzzer=value_profile, trial=1, discovered_at=16448s, mutation_op=BytesInsertMutator,CrossoverInsertMutator,BytesRandSetMutator,BytesRandSetMutator):
  0000: 65 65 65 e3 e3 e1 3c 3c 3b 3c 3c 00 40 5c 0a 3c   eee...<<;<<.@\.<
  0010: 6d 6d 3e 2e 72 73 69 6f 3a 3d 26 31 2e 30 22 3f   mm>.rsio:=&1.0"?
  0020: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
  0030: 53 54 45 4d 20 3e 0a 30 0c 41 41 2f 2f 2f 2f 2f   STEM >.0.AA/////
Seed 4 (id=04f08d7e20b8f7f6, size=323 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=16682s, mutation_op=ByteAddMutator,DwordInterestingMutator,BytesDeleteMutator,CrossoverInsertMutator,BytesDeleteMutator):
  0000: ff ff ff ff 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c db f5 e1 e1 e1 e1 e1 e1 e1 e1 e1 20 20 eb ff   <...........  ..
  0020: ff ff 20 20 20 20 78 6c 69 45 4d 45 4e 54 20 ff   ..    xliEMENT .
  0030: ff 20 20 20 20 78 6c 69 6e 3c 3a 68 72 26 66 3d   .    xlin<:hr&f=
Seed 5 (id=099c979dc291fbf9, size=339 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=17393s, mutation_op=BytesCopyMutator,ByteAddMutator,BytesExpandMutator,BytesCopyMutator,ByteNegMutator):
  0000: ff ff ff ff 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c db f5 e1 e1 e1 e1 e1 e1 e1 e1 e1 20 20 eb ff   <...........  ..
  0020: ff ff 20 20 20 20 78 6c 69 45 4d 45 4e 54 20 ed   ..    xliEMENT .
  0030: ff 20 20 20 20 78 6c 69 6e 3c 3a 68 72 26 66 3d   .    xlin<:hr&f=

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=2000bf0582cbd247, size=368 bytes, fuzzer=naive, trial=1, discovered_at=105s, mutation_op=ByteAddMutator,QwordAddMutator,TokenReplace,ByteNegMutator,ByteInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 3b   a SYSTEM "dtds/;
Seed 2 (id=263019ca5e4e0e33, size=382 bytes, fuzzer=cmplog, trial=1, discovered_at=452s, mutation_op=BytesRandInsertMutator,ByteNegMutator,QwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=23b8cfe89890fc85, size=368 bytes, fuzzer=naive, trial=1, discovered_at=463s, mutation_op=ByteDecMutator,ByteInterestingMutator,TokenReplace):
  0000: 3f 42 0f 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ?B..127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 3b   a SYSTEM "dtds/;
Seed 4 (id=4356b6090c5bebf5, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=1435s, mutation_op=BytesDeleteMutator,DwordAddMutator,DwordAddMutator,DwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 0a 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?..<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2e 31   a SYSTEM "dtds.1
Seed 5 (id=087a0a05e3bb2f0e, size=67 bytes, fuzzer=naive, trial=1, discovered_at=1651s, mutation_op=ByteAddMutator,ByteDecMutator,BytesDeleteMutator,BytesRandInsertMutator):
  0000: 65 65 2f 61 3f 0a 0a 5c 0a 0a 3c 61 3e 0a 20 20   ee/a?..\..<a>.  
  0010: 3c 62 20 20 64 74 64 73 2f 3e 0a 20 20 3c 62 20   <b  dtds/>.  <b 
  0020: 78 6c 69 6e 6b 39 68 72 65 66 3d 22 68 26 23 49   xlink9href="h&#I
  0030: 4d 50 4c 4b 4b 4b 4b 4b 4b 4b 4b 4b 4b 49 45 44   MPLKKKKKKKKKKIED


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  ff(.)x7 6b(k)x3 65(e)x3             06(.)x6 59(Y)x6 65(e)x2 00(.)x2 +7u  PARTIAL
   0x0001  ff(.)x7 65(e)x3 27(')x2 d8(.)x1     00(.)x6 37(7)x2 50(P)x2 76(v)x2 +10u  PARTIAL
   0x0002  ff(.)x7 0a(.)x3 65(e)x3             00(.)x6 37(7)x2 45(E)x2 76(v)x2 +10u  PARTIAL
   0x0006  37(7)x7 7e(~)x3 3c(<)x2 16(.)x1     37(7)x7 32(2)x3 53(S)x2 76(v)x2 +9u  PARTIAL
   0x0007  37(7)x7 20( )x3 3c(<)x2 00(.)x1     37(7)x7 59(Y)x2 06(.)x2 2e(.)x2 +9u  PARTIAL
   0x000a  2e(.)x6 20( )x4 3c(<)x2 78(x)x1     2e(.)x7 6c(l)x4 3c(<)x3 45(E)x2 +6u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6466.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6466,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6466 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6466 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6466 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).