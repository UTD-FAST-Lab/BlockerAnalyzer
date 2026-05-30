==== BLOCKER ====
Target: libxml2
Branch ID: 6461
Location: /src/libxml2/parser.c:2317:9
Enclosing function: xmlParseCharRef
Source line:         (NXT(2) == 'x')) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (value_profile vs value_profile)
cmplog                           3        7          0  REFERENCE
value_profile                   10        0          0  winner (value_profile vs naive)
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        6        4          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0        9          1  REFERENCE
minimizer                        1        8          1  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=8.50h  loser=18.40h
  avg hitcount on branch: winner=22  loser=0
  prob_div=0.90  dur_div=9.90h  hit_div=22
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6461/{W,L}/branch_coverage_show.txt

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
[B]  2317          (NXT(2) == 'x')) { <-- BLOCKER
[W]  2318  	SKIP(3);
[W]  2319  	GROW;
[W]  2320  	while (RAW != ';') { /* loop blocked by count */
[W]  2321  	    if (count++ > 20) {
[ ]  2322  		count = 0;
[ ]  2323  		GROW;
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
[W]  2334  		xmlFatalErr(ctxt, XML_ERR_INVALID_HEX_CHARREF, NULL);
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
[ ]  2345  	    /* on purpose to avoid reentrancy problems with NEXT and SKIP */
[ ]  2346  	    ctxt->input->col++;
[ ]  2347  	    ctxt->input->cur++;
[ ]  2348  	}
[B]  2349      } else if  ((RAW == '&') && (NXT(1) == '#')) {
[L]  2350  	SKIP(2);
[L]  2351  	GROW;
[L]  2352  	while (RAW != ';') { /* loop blocked by count */
[L]  2353  	    if (count++ > 20) {
[ ]  2354  		count = 0;
[ ]  2355  		GROW;
[ ]  2356                  if (ctxt->instate == XML_PARSER_EOF)
[ ]  2357                      return(0);
[ ]  2358  	    }
[L]  2359  	    if ((RAW >= '0') && (RAW <= '9'))
[L]  2360  	        val = val * 10 + (CUR - '0');
[L]  2361  	    else {
[L]  2362  		xmlFatalErr(ctxt, XML_ERR_INVALID_DEC_CHARREF, NULL);
[L]  2363  		val = 0;
[L]  2364  		break;
[L]  2365  	    }
[L]  2366  	    if (val > 0x110000)
[L]  2367  	        val = 0x110000;
[ ]  2368  
[L]  2369  	    NEXT;
[L]  2370  	    count++;
[L]  2371  	}
[L]  2372  	if (RAW == ';') {
[ ]  2373  	    /* on purpose to avoid reentrancy problems with NEXT and SKIP */
[ ]  2374  	    ctxt->input->col++;
[ ]  2375  	    ctxt->input->cur++;
[ ]  2376  	}
[L]  2377      } else {
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
[ ]  7195  	if (ctxt->charset != XML_CHAR_ENCODING_UTF8) {
[ ]  7196  	    /*
[ ]  7197  	     * So we are using non-UTF-8 buffers
[ ]  7198  	     * Check that the char fit on 8bits, if not
[ ]  7199  	     * generate a CharRef.
[ ]  7200  	     */
[ ]  7201  	    if (value <= 0xFF) {

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
    3280     17800  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     228      2780  xmlParseName  (/src/libxml2/parser.c:3368-3412)
     199      2520  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
     132      2420  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
      48      2300  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
     276      2430  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      51      1150  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
     158       644  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      32       350  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
     118       418  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
      85       358  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226)
     112       362  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752)
      90       322  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
       6        99  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      33       122  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942)
... (31 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=6  xmlParseStartTag  (/src/libxml2/parser.c:8632-8752) ---
  d=6   L8641  T=0 F=112  T=0 F=362  if (RAW != '<') return(NULL);
  d=6   L8645  T=38 F=74  T=211 F=151  if (name == NULL) {
  d=6   L8660  T=3 F=0  T=0 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=6   L8660  T=68 F=3  T=101 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=6   L8668  T=9 F=10  T=15 F=23  if (attvalue != NULL) {
  d=6   L8696  T=0 F=3  T=0 F=6  } else if (nbatts + 4 > maxatts) {
  d=6   L8717  T=0 F=10  T=0 F=23  if (attvalue != NULL)
  d=6   L8724  T=0 F=3  T=0 F=0  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=6   L8724  T=3 F=16  T=0 F=30  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=6   L8724  T=0 F=19  T=8 F=30  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=6   L8737  T=74 F=0  T=151 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElement != NU...
  d=6   L8737  T=74 F=0  T=151 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElement != NU...
  d=6   L8738  T=34 F=40  T=56 F=95  (!ctxt->disableSAX)) {
  d=6   L8745  T=33 F=41  T=31 F=120  if (atts != NULL) {
--- d=6  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226) ---
  d=6   L10115  T=0 F=85  T=0 F=358  if (((unsigned int) ctxt->nameNr > xmlParserMaxDepth) &&
  d=6   L10125  T=0 F=85  T=0 F=358  if (ctxt->record_info) {
  d=6   L10131  T=0 F=85  T=0 F=358  if (ctxt->spaceNr == 0)
  d=6   L10133  T=14 F=71  T=288 F=70  else if (*ctxt->space == -2)
  d=6   L10140  T=2 F=83  T=41 F=317  if (ctxt->sax2)
  d=6   L10147  T=0 F=85  T=0 F=358  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10149  T=38 F=47  T=219 F=139  if (name == NULL) {
  d=6   L10162  T=0 F=0  T=0 F=56  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L10162  T=0 F=47  T=56 F=83  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L10170  T=0 F=3  T=0 F=0  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L10170  T=3 F=44  T=0 F=139  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L10196  T=12 F=35  T=80 F=59  if (RAW == '>') {
--- d=5  xmlParseAttribute  (/src/libxml2/parser.c:8542-8600) ---
  d=5   L8559  T=9 F=10  T=15 F=23  if (RAW == '=') {
--- d=5  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774) ---
  d=5   L9369  T=0 F=6  T=0 F=56  if (RAW != '<') return(NULL);
  d=5   L9391  T=0 F=6  T=11 F=45  if (localname == NULL) {
  d=5   L9406  T=0 F=6  T=28 F=20  while (((RAW != '>') &&
  d=5   L9407  T=0 F=0  T=28 F=0  ((RAW != '/') || (NXT(1) != '>')) &&
  d=5   L9408  T=0 F=0  T=28 F=0  (IS_BYTE_CHAR(RAW))) && (ctxt->instate != XML_PARSER_EOF)) {
  d=5   L9413  T=0 F=0  T=10 F=18  if (attname == NULL) {
  d=5   L9418  T=0 F=0  T=4 F=14  if (attvalue == NULL)
  d=5   L9420  T=0 F=0  T=0 F=14  if (len < 0) len = xmlStrlen(attvalue);
  d=5   L9422  T=0 F=0  T=0 F=14  if ((attname == ctxt->str_xmlns) && (aprefix == NULL)) {
  d=5   L9475  T=0 F=0  T=0 F=14  } else if (aprefix == ctxt->str_xmlns) {
  d=5   L9548  T=0 F=0  T=14 F=0  if ((atts == NULL) || (nbatts + 5 > maxatts)) {
  d=5   L9549  T=0 F=0  T=0 F=14  if (xmlCtxtGrowAttrs(ctxt, nbatts + 5) < 0) {
  d=5   L9564  T=0 F=0  T=14 F=0  if (alloc)
  d=5   L9574  T=0 F=0  T=14 F=0  if (alloc != 0) attval = 1;
  d=5   L9579  T=0 F=0  T=0 F=18  if ((attvalue != NULL) && (alloc != 0)) {
  d=5   L9585  T=0 F=0  T=0 F=18  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L9587  T=0 F=0  T=0 F=18  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=5   L9587  T=0 F=0  T=0 F=18  if ((RAW == '>') || (((RAW == '/') && (NXT(1) == '>'))))
  d=5   L9589  T=0 F=0  T=15 F=3  if (SKIP_BLANKS == 0) {
  d=5   L9597  T=0 F=6  T=0 F=45  if (ctxt->input->id != inputid) {
  d=5   L9605  T=0 F=6  T=14 F=45  for (i = 0, j = 0; j < nratts; i += 5, j++) {
  d=5   L9606  T=0 F=0  T=0 F=14  if (atts[i+2] != NULL) {
  d=5   L9621  T=0 F=6  T=0 F=45  if (ctxt->attsDefault != NULL) {
  d=5   L9704  T=0 F=6  T=14 F=45  for (i = 0; i < nbatts;i += 5) {
  d=5   L9708  T=0 F=0  T=11 F=3  if (atts[i + 1] != NULL) {
  d=5   L9710  T=0 F=0  T=11 F=0  if (nsname == NULL) {
  d=5   L9724  T=0 F=0  T=0 F=14  for (j = 0; j < i;j += 5) {
  d=5   L9741  T=0 F=0  T=1 F=0  if ((prefix != NULL) && (nsname == NULL)) {
  d=5   L9741  T=0 F=6  T=1 F=44  if ((prefix != NULL) && (nsname == NULL)) {
  d=5   L9752  T=6 F=0  T=45 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=5   L9752  T=6 F=0  T=45 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->startElementNs != ...
  d=5   L9753  T=6 F=0  T=15 F=30  (!ctxt->disableSAX)) {
  d=5   L9754  T=0 F=6  T=0 F=15  if (nbNs > 0)
  d=5   L9767  T=0 F=6  T=14 F=31  if (attval != 0) {
  d=5   L9768  T=0 F=0  T=14 F=14  for (i = 3,j = 0; j < nratts;i += 5,j++)
  d=5   L9769  T=0 F=0  T=14 F=0  if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))
  d=5   L9769  T=0 F=0  T=14 F=0  if ((ctxt->attallocs[j] != 0) && (atts[i] != NULL))
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10816  T=0 F=7  T=0 F=15  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10816  T=0 F=7  T=0 F=15  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10829  T=7 F=0  T=15 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10829  T=7 F=0  T=15 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10831  T=0 F=7  T=0 F=15  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10834  T=7 F=0  T=15 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L10835  T=7 F=0  T=15 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=5   L10846  T=0 F=7  T=11 F=4  if (enc != XML_CHAR_ENCODING_NONE) {
  d=5   L10852  T=0 F=7  T=0 F=15  if (CUR == 0) {
  d=5   L10863  T=0 F=7  T=1 F=14  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=5   L10872  T=0 F=0  T=0 F=11  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=5   L10873  T=0 F=0  T=0 F=11  (ctxt->instate == XML_PARSER_EOF)) {
  d=5   L10884  T=7 F=0  T=15 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=7 F=0  T=13 F=2  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=7 F=0  T=15 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10886  T=0 F=7  T=0 F=15  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10888  T=7 F=0  T=13 F=2  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10907  T=0 F=0  T=0 F=7  if (RAW == '[') {
  d=5   L10918  T=0 F=0  T=7 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10918  T=0 F=0  T=7 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10919  T=0 F=0  T=7 F=0  (!ctxt->disableSAX))
  d=5   L10922  T=0 F=0  T=0 F=7  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10936  T=0 F=7  T=0 F=15  if (RAW != '<') {
  d=5   L10950  T=0 F=7  T=4 F=11  if (RAW != 0) {
  d=5   L10959  T=7 F=0  T=15 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10959  T=7 F=0  T=15 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10965  T=7 F=0  T=13 F=2  if ((ctxt->myDoc != NULL) &&
  d=5   L10971  T=0 F=7  T=0 F=15  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=5   L10980  T=7 F=0  T=15 F=0  if (! ctxt->wellFormed) {
--- d=4  parser.c:xmlParseAttribute2  (/src/libxml2/parser.c:9225-9323) ---
  d=4   L9233  T=0 F=0  T=7 F=21  if (name == NULL) {
  d=4   L9242  T=0 F=0  T=0 F=21  if (ctxt->attsSpecial != NULL) {
  d=4   L9255  T=0 F=0  T=17 F=4  if (RAW == '=') {
  d=4   L9259  T=0 F=0  T=3 F=14  if (val == NULL)
  d=4   L9261  T=0 F=0  T=0 F=14  if (normalize) {
  d=4   L9286  T=0 F=0  T=0 F=14  if (*prefix == ctxt->str_xml) {
--- d=4  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=4   L10077  T=0 F=7  T=5 F=10  if (xmlParseElementStart(ctxt) != 0)
--- d=4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=4   L12139  T=0 F=59  T=0 F=120  if (ctxt == NULL)
  d=4   L12141  T=45 F=14  T=33 F=87  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12143  T=0 F=26  T=0 F=102  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12145  T=0 F=26  T=0 F=102  if (ctxt->input == NULL)
  d=4   L12149  T=14 F=12  T=64 F=38  if (ctxt->instate == XML_PARSER_START)
  d=4   L12151  T=23 F=0  T=71 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12151  T=23 F=3  T=71 F=31  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12151  T=23 F=0  T=71 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12152  T=0 F=23  T=0 F=71  (chunk[size - 1] == '\r')) {
  d=4   L12159  T=23 F=0  T=71 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12159  T=23 F=0  T=71 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12159  T=23 F=3  T=71 F=31  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12160  T=23 F=0  T=71 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=4   L12160  T=23 F=0  T=71 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=4   L12170  T=14 F=9  T=52 F=19  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=4   L12170  T=14 F=0  T=52 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=4   L12171  T=14 F=0  T=52 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12171  T=0 F=14  T=0 F=52  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12202  T=0 F=23  T=0 F=71  if (res < 0) {
  d=4   L12211  T=3 F=0  T=31 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12212  T=3 F=0  T=31 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12212  T=3 F=0  T=31 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12214  T=0 F=3  T=0 F=31  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=4   L12233  T=0 F=26  T=0 F=102  if (remain != 0) {
  d=4   L12238  T=0 F=26  T=5 F=97  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12241  T=26 F=0  T=97 F=0  if ((ctxt->input != NULL) &&
  d=4   L12242  T=0 F=26  T=0 F=97  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=4   L12243  T=0 F=26  T=0 F=97  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=4   L12248  T=26 F=0  T=40 F=57  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12251  T=0 F=18  T=0 F=85  if (remain != 0) {
  d=4   L12257  T=0 F=18  T=0 F=85  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=4   L12268  T=3 F=15  T=9 F=76  if (terminate) {
  d=4   L12274  T=3 F=0  T=9 F=0  if (ctxt->input != NULL) {
  d=4   L12275  T=0 F=3  T=0 F=9  if (ctxt->input->buf == NULL)
  d=4   L12283  T=3 F=0  T=9 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=4   L12284  T=3 F=0  T=9 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=4   L12287  T=0 F=3  T=0 F=9  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=4   L12290  T=3 F=0  T=9 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12291  T=3 F=0  T=9 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12291  T=3 F=0  T=9 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12296  T=18 F=0  T=20 F=65  if (ctxt->wellFormed == 0)
--- d=3  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203) ---
  d=3   L9063  T=0 F=9  T=14 F=18  int maxLength = (ctxt->options & XML_PARSE_HUGE) ?
  d=3   L9071  T=0 F=9  T=3 F=29  if (*in != '"' && *in != '\'') {
  d=3   L9071  T=0 F=0  T=3 F=0  if (*in != '"' && *in != '\'') {
  d=3   L9086  T=0 F=9  T=0 F=29  if (in >= end) {
  d=3   L9089  T=0 F=9  T=0 F=29  if (normalize) {
  d=3   L9165  T=162 F=0  T=746 F=0  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9165  T=153 F=6  T=740 F=0  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9165  T=159 F=3  T=740 F=6  while ((in < end) && (*in != limit) && (*in >= 0x20) &&
  d=3   L9166  T=153 F=0  T=717 F=0  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9166  T=153 F=0  T=737 F=3  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9166  T=153 F=0  T=717 F=20  (*in <= 0x7f) && (*in != '&') && (*in != '<')) {
  d=3   L9169  T=0 F=153  T=0 F=717  if (in >= end) {
  d=3   L9179  T=0 F=9  T=0 F=29  if ((in - start) > maxLength) {
  d=3   L9184  T=6 F=3  T=23 F=6  if (*in != limit) goto need_complex;
  d=3   L9188  T=0 F=3  T=0 F=6  if (len != NULL) {
  d=3   L9193  T=0 F=3  T=0 F=6  if (alloc) *alloc = 1;
  d=3   L9201  T=0 F=6  T=14 F=9  if (alloc) *alloc = 1;
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9973  T=260 F=7  T=1740 F=10  while ((RAW != 0) &&
  d=3   L9974  T=260 F=0  T=1740 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L9980  T=80 F=180  T=347 F=1400  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=2 F=78  T=0 F=347  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=78 F=180  T=347 F=1400  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=38 F=40  T=8 F=339  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9996  T=0 F=38  T=0 F=8  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=3   L10004  T=78 F=180  T=347 F=1400  else if (*cur == '<') {
  d=3   L10005  T=0 F=78  T=4 F=343  if (NXT(1) == '/') {
  d=3   L10006  T=0 F=0  T=0 F=4  if (ctxt->nameNr <= nameNr)
  d=3   L10019  T=22 F=158  T=983 F=419  else if (*cur == '&') {
--- d=3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=3   L11409  T=0 F=26  T=0 F=102  if (ctxt->input == NULL)
  d=3   L11465  T=26 F=0  T=102 F=0  if ((ctxt->input != NULL) &&
  d=3   L11466  T=0 F=26  T=0 F=102  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=3   L11470  T=258 F=0  T=617 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=3   L11471  T=8 F=170  T=12 F=423  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11471  T=178 F=80  T=435 F=182  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11474  T=0 F=250  T=0 F=605  if (ctxt->input == NULL) break;
  d=3   L11475  T=0 F=250  T=0 F=605  if (ctxt->input->buf == NULL)
  d=3   L11486  T=222 F=28  T=522 F=83  if ((ctxt->instate != XML_PARSER_START) &&
  d=3   L11487  T=0 F=222  T=0 F=522  (ctxt->input->buf->raw != NULL) &&
  d=3   L11500  T=1 F=249  T=9 F=596  if (avail < 1)
  d=3   L11502  T=0 F=249  T=0 F=596  switch (ctxt->instate) {
  d=3   L11503  T=0 F=249  T=0 F=596  case XML_PARSER_EOF:
  d=3   L11508  T=28 F=221  T=83 F=513  case XML_PARSER_START:
  d=3   L11509  T=14 F=14  T=19 F=64  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=3   L11535  T=0 F=14  T=0 F=64  if (avail < 2)
  d=3   L11539  T=0 F=14  T=0 F=64  if (cur == 0) {
  d=3   L11553  T=0 F=14  T=56 F=2  if ((cur == '<') && (next == '?')) {
  d=3   L11553  T=14 F=0  T=58 F=6  if ((cur == '<') && (next == '?')) {
  d=3   L11555  T=0 F=0  T=0 F=56  if (avail < 5) goto done;
  d=3   L11556  T=0 F=0  T=48 F=8  if ((!terminate) &&
  d=3   L11557  T=0 F=0  T=34 F=14  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11559  T=0 F=0  T=22 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11559  T=0 F=0  T=22 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11562  T=0 F=0  T=22 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=3   L11563  T=0 F=0  T=22 F=0  (ctxt->input->cur[3] == 'm') &&
  d=3   L11564  T=0 F=0  T=22 F=0  (ctxt->input->cur[4] == 'l') &&
  d=3   L11572  T=0 F=0  T=0 F=22  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=3   L11581  T=0 F=0  T=22 F=0  if ((ctxt->encoding == NULL) &&
  d=3   L11582  T=0 F=0  T=0 F=22  (ctxt->input->encoding != NULL))
  d=3   L11584  T=0 F=0  T=22 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11584  T=0 F=0  T=22 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11585  T=0 F=0  T=18 F=4  (!ctxt->disableSAX))
  d=3   L11622  T=39 F=210  T=88 F=508  case XML_PARSER_START_TAG: {
  d=3   L11629  T=0 F=39  T=0 F=88  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11632  T=0 F=39  T=0 F=88  if (cur != '<') {
  d=3   L11639  T=39 F=0  T=72 F=16  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11657  T=0 F=33  T=3 F=57  if (name == NULL) {
  d=3   L11660  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11660  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11721  T=168 F=81  T=375 F=221  case XML_PARSER_CONTENT: {
  d=3   L11722  T=2 F=166  T=0 F=375  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11722  T=2 F=0  T=0 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11727  T=0 F=33  T=8 F=49  if ((cur == '<') && (next == '/')) {
  d=3   L11727  T=33 F=133  T=57 F=318  if ((cur == '<') && (next == '/')) {
  d=3   L11730  T=2 F=31  T=0 F=49  } else if ((cur == '<') && (next == '?')) {
  d=3   L11730  T=33 F=133  T=49 F=318  } else if ((cur == '<') && (next == '?')) {
  d=3   L11731  T=1 F=1  T=0 F=0  if ((!terminate) &&
  d=3   L11732  T=1 F=0  T=0 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11736  T=31 F=133  T=49 F=318  } else if ((cur == '<') && (next != '!')) {
  d=3   L11739  T=11 F=133  T=14 F=318  } else if ((cur == '<') && (next == '!') &&
  d=3   L11747  T=11 F=133  T=14 F=318  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11758  T=11 F=133  T=14 F=318  } else if ((cur == '<') && (next == '!') &&
  d=3   L11759  T=1 F=10  T=0 F=14  (avail < 9)) {
  d=3   L11761  T=10 F=133  T=14 F=318  } else if (cur == '<') {
  d=3   L11765  T=35 F=98  T=179 F=139  } else if (cur == '&') {
  d=3   L11766  T=32 F=3  T=8 F=171  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11766  T=6 F=26  T=8 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11792  T=0 F=249  T=8 F=588  case XML_PARSER_END_TAG:
  d=3   L11793  T=0 F=0  T=0 F=8  if (avail < 2)
  d=3   L11795  T=0 F=0  T=0 F=6  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11795  T=0 F=0  T=6 F=2  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11797  T=0 F=0  T=2 F=6  if (ctxt->sax2) {
  d=3   L11805  T=0 F=0  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF) {
  d=3   L11807  T=0 F=0  T=2 F=6  } else if (ctxt->nameNr == 0) {
  d=3   L11813  T=0 F=249  T=0 F=596  case XML_PARSER_CDATA_SECTION: {
  d=3   L11904  T=14 F=235  T=26 F=570  case XML_PARSER_MISC:
  d=3   L11905  T=0 F=249  T=14 F=582  case XML_PARSER_PROLOG:
  d=3   L11906  T=0 F=249  T=2 F=594  case XML_PARSER_EPILOG:
  d=3   L11908  T=0 F=14  T=0 F=42  if (ctxt->input->buf == NULL)
  d=3   L11914  T=0 F=14  T=0 F=42  if (avail < 2)
  d=3   L11918  T=14 F=0  T=40 F=2  if ((cur == '<') && (next == '?')) {
  d=3   L11918  T=0 F=14  T=0 F=40  if ((cur == '<') && (next == '?')) {
  d=3   L11929  T=0 F=14  T=14 F=26  } else if ((cur == '<') && (next == '!') &&
  d=3   L11929  T=14 F=0  T=40 F=2  } else if ((cur == '<') && (next == '!') &&
  d=3   L11930  T=0 F=0  T=0 F=14  (ctxt->input->cur[2] == '-') &&
  d=3   L11942  T=14 F=0  T=26 F=16  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=3   L11943  T=0 F=14  T=14 F=12  (cur == '<') && (next == '!') &&
  d=3   L11944  T=0 F=0  T=14 F=0  (ctxt->input->cur[2] == 'D') &&
  d=3   L11945  T=0 F=0  T=14 F=0  (ctxt->input->cur[3] == 'O') &&
  d=3   L11946  T=0 F=0  T=14 F=0  (ctxt->input->cur[4] == 'C') &&
  d=3   L11947  T=0 F=0  T=14 F=0  (ctxt->input->cur[5] == 'T') &&
  d=3   L11948  T=0 F=0  T=14 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=3   L11949  T=0 F=0  T=14 F=0  (ctxt->input->cur[7] == 'P') &&
  d=3   L11950  T=0 F=0  T=14 F=0  (ctxt->input->cur[8] == 'E')) {
  d=3   L11951  T=0 F=0  T=14 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11951  T=0 F=0  T=0 F=14  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11959  T=0 F=0  T=0 F=14  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11961  T=0 F=0  T=0 F=14  if (RAW == '[') {
  d=3   L11972  T=0 F=0  T=14 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11972  T=0 F=0  T=14 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11973  T=0 F=0  T=14 F=0  (ctxt->sax->externalSubset != NULL))
  d=3   L11985  T=14 F=0  T=26 F=2  } else if ((cur == '<') && (next == '!') &&
  d=3   L11989  T=0 F=14  T=2 F=26  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=3   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L12007  T=0 F=249  T=0 F=596  case XML_PARSER_DTD: {
  d=3   L12029  T=0 F=249  T=0 F=596  case XML_PARSER_COMMENT:
  d=3   L12038  T=0 F=249  T=0 F=596  case XML_PARSER_IGNORE:
  d=3   L12047  T=0 F=249  T=0 F=596  case XML_PARSER_PI:
  d=3   L12056  T=0 F=249  T=0 F=596  case XML_PARSER_ENTITY_DECL:
  d=3   L12065  T=0 F=249  T=0 F=596  case XML_PARSER_ENTITY_VALUE:
  d=3   L12074  T=0 F=249  T=0 F=596  case XML_PARSER_ATTRIBUTE_VALUE:
  d=3   L12083  T=0 F=249  T=0 F=596  case XML_PARSER_SYSTEM_LITERAL:
  d=3   L12092  T=0 F=249  T=0 F=596  case XML_PARSER_PUBLIC_LITERAL:
--- d=2  parser.c:xmlParseAttValueComplex  (/src/libxml2/parser.c:3948-4190) ---
  d=2   L3954  T=0 F=6  T=11 F=12  size_t maxLength = (ctxt->options & XML_PARSE_HUGE) ?
  d=2   L3961  T=6 F=0  T=23 F=0  if (NXT(0) == '"') {
  d=2   L3979  T=0 F=6  T=0 F=23  if (buf == NULL) goto mem_error;
  d=2   L3985  T=1310 F=0  T=3110 F=9  while (((NXT(0) != limit) && /* checked */
  d=2   L3986  T=1300 F=0  T=3090 F=5  (IS_CHAR(c)) && (c != '<')) &&
  d=2   L3986  T=1300 F=6  T=3100 F=9  (IS_CHAR(c)) && (c != '<')) &&
  d=2   L3987  T=1300 F=0  T=3090 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L3988  T=9 F=1290  T=1230 F=1860  if (c == '&') {
  d=2   L3990  T=3 F=6  T=69 F=1160  if (NXT(1) == '#') {
  d=2   L3993  T=0 F=3  T=0 F=69  if (val == '&') {
  d=2   L4013  T=0 F=3  T=0 F=69  } else if (val != 0) {
  d=2   L4021  T=0 F=6  T=0 F=1160  if ((ent != NULL) &&
  d=2   L4036  T=0 F=6  T=0 F=1160  } else if ((ent != NULL) &&
  d=2   L4070  T=0 F=6  T=0 F=1160  } else if (ent != NULL) {
  d=2   L4132  T=47 F=726  T=12 F=1700  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4132  T=0 F=773  T=0 F=1710  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4132  T=0 F=726  T=0 F=1700  if ((c == 0x20) || (c == 0xD) || (c == 0xA) || (c == 0x9)) {
  d=2   L4133  T=569 F=0  T=159 F=0  if ((len != 0) || (!normalize)) {
  d=2   L4134  T=569 F=0  T=159 F=0  if ((!normalize) || (!in_space)) {
  d=2   L4136  T=6 F=569  T=0 F=159  while (len + 10 > buf_size) {
  d=2   L4145  T=4 F=722  T=8 F=1690  if (len + 10 > buf_size) {
  d=2   L4153  T=0 F=1300  T=0 F=3090  if (len > maxLength) {
  d=2   L4159  T=0 F=6  T=0 F=23  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L4162  T=6 F=0  T=11 F=12  if ((in_space) && (normalize)) {
  d=2   L4166  T=0 F=6  T=5 F=18  if (RAW == '<') {
  d=2   L4168  T=6 F=0  T=9 F=9  } else if (RAW != limit) {
  d=2   L4169  T=6 F=0  T=3 F=0  if ((c != 0) && (!IS_CHAR(c))) {
  d=2   L4169  T=6 F=0  T=3 F=6  if ((c != 0) && (!IS_CHAR(c))) {
  d=2   L4179  T=0 F=6  T=14 F=9  if (attlen != NULL) *attlen = len;
--- d=2  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=2   L7181  T=0 F=51  T=0 F=1150  if (RAW != '&')
  d=2   L7187  T=9 F=42  T=15 F=1130  if (NXT(1) == '#') {
  d=2   L7233  T=42 F=0  T=1130 F=0  if (ent == NULL) return;
--- d=1  xmlParseCharRef  (/src/libxml2/parser.c:2309-2400) ---
  d=1   L2316  T=12 F=0  T=84 F=0  if ((RAW == '&') && (NXT(1) == '#') &&
  d=1   L2316  T=12 F=0  T=84 F=0  if ((RAW == '&') && (NXT(1) == '#') &&
  d=1   L2317  T=12 F=0  T=0 F=84  (NXT(2) == 'x')) {  <-- BLOCKER
  d=1   L2320  T=12 F=0  T=0 F=0  while (RAW != ';') { /* loop blocked by count */
  d=1   L2321  T=0 F=12  T=0 F=0  if (count++ > 20) {
  d=1   L2327  T=0 F=11  T=0 F=0  if ((RAW >= '0') && (RAW <= '9'))
  d=1   L2327  T=11 F=1  T=0 F=0  if ((RAW >= '0') && (RAW <= '9'))
  d=1   L2329  T=7 F=5  T=0 F=0  else if ((RAW >= 'a') && (RAW <= 'f') && (count < 20))
  d=1   L2329  T=0 F=7  T=0 F=0  else if ((RAW >= 'a') && (RAW <= 'f') && (count < 20))
  d=1   L2331  T=10 F=2  T=0 F=0  else if ((RAW >= 'A') && (RAW <= 'F') && (count < 20))
  d=1   L2331  T=0 F=10  T=0 F=0  else if ((RAW >= 'A') && (RAW <= 'F') && (count < 20))
  d=1   L2344  T=0 F=12  T=0 F=0  if (RAW == ';') {
  d=1   L2349  T=0 F=0  T=84 F=0  } else if  ((RAW == '&') && (NXT(1) == '#')) {
  d=1   L2349  T=0 F=0  T=84 F=0  } else if  ((RAW == '&') && (NXT(1) == '#')) {
  d=1   L2352  T=0 F=0  T=111 F=0  while (RAW != ';') { /* loop blocked by count */
  d=1   L2353  T=0 F=0  T=0 F=111  if (count++ > 20) {
  d=1   L2359  T=0 F=0  T=27 F=6  if ((RAW >= '0') && (RAW <= '9'))
  d=1   L2359  T=0 F=0  T=33 F=78  if ((RAW >= '0') && (RAW <= '9'))
  d=1   L2366  T=0 F=0  T=9 F=18  if (val > 0x110000)
  d=1   L2372  T=0 F=0  T=0 F=84  if (RAW == ';') {
  d=1   L2388  T=0 F=12  T=0 F=84  if (val >= 0x110000) {

[off-chain: 532 additional divergent branches across 53 functions (see HIT-COUNT DIVERGENCE for which functions)]

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
Seed 1 (id=244e66c16f769fa4, size=508 bytes, fuzzer=naive, trial=2, discovered_at=581s, mutation_op=CrossoverInsertMutator,BytesSwapMutator,BytesDeleteMutator,WordAddMutator):
  0000: 17 17 17 17 17 17 17 17 17 54 41 29 3e 37 37 37   .........TA)>777
  0010: 32 01 e0 ff ff 06 00 00 00 31 32 2b 44 41 54 41   2........12+DATA
  0020: 29 3e 37 37 00 00 00 31 32 37 37 37 32 2e 78 6d   )>77...127772.xm
  0030: 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e   l\.<?xml version
Seed 2 (id=f645e9fd574ae269, size=297 bytes, fuzzer=naive, trial=5, discovered_at=15390s, mutation_op=BytesDeleteMutator,BytesCopyMutator):
  0000: 3d de 68 74 74 70 3a 2f 2f 5f 5f 5f 5f 6c 5f 5f   =.http://____l__
  0010: 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 5f 5f 60 5f   ml version="__`_
  0020: 5f 5f 5f 5f 66 61 6b 65 75 72 6c 2e 6e 65 74 22   ____fakeurl.net"
  0030: 3e 62 20 74 65 78 74 3c 2f 62 20 2a 3c 88 61 3e   >b text</b *<.a>
Seed 3 (id=62f3d2fb86713c7d, size=407 bytes, fuzzer=naive, trial=2, discovered_at=15766s, mutation_op=ByteRandMutator,ByteIncMutator,WordAddMutator,QwordAddMutator,BytesRandInsertMutator,CrossoverReplaceMutator):
  0000: 22 68 74 74 70 3a 2f 2f 66 69 6d 78 78 78 78 78   "http://fimxxxxx
  0010: 78 78 78 78 78 78 44 21 27 73 69 6d 70 ff ff ff   xxxxxxD!'simp...
  0020: ff ff ff ff ff 6c 65 27 4a 20 20 20 20 e0 20 6c   .....le'J    . l
  0030: 69 6e 6b 3a 68 72 65 66 20 20 20 3a 68 72 65 66   ink:href   :href
Seed 4 (id=47207ddd78048477, size=291 bytes, fuzzer=naive, trial=2, discovered_at=21000s, mutation_op=CrossoverInsertMutator):
  0000: 20 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73    xml\.<?xml vers
  0010: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0020: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
  0030: 64 74 64 73 2f 31 32 37 37 37 37 32 2e 64 74 64   dtds/1277772.dtd
Seed 5 (id=57caa18a283ae665, size=303 bytes, fuzzer=naive, trial=4, discovered_at=22246s, mutation_op=ByteIncMutator,BytesExpandMutator,WordInterestingMutator):
  0000: f9 4e 78 78 63 78 78 78 78 78 78 3a 2f 2f 66 7e   .Nxxcxxxxxx://f~
  0010: 7e 7e 7e 7e 7e 49 53 4f 2d 4c 26 54 49 4e 2d 31   ~~~~~ISO-L&TIN-1
  0020: 7e 7e 2d 4c 41 54 49 4e 2d 31 7e 7e 7e 49 53 4f   ~~-LATIN-1~~~ISO
  0030: 2d 4c 41 54 49 4e 2d 31 7e 7e 7e 7e 53 2d 74 2d   -LATIN-1~~~~S-t-


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  6c(l)x4 3b(;)x2 37(7)x1             30(0)x3 17(.)x1 3d(=)x1 22(")x1 +9u  PARTIAL
   0x0001  6e(n)x4 3c(<)x2 37(7)x1             68(h)x2 4e(N)x2 37(7)x2 ff(.)x2 +7u  PARTIAL
   0x0002  73(s)x4 3c(<)x2 37(7)x1             68(h)x2 74(t)x2 32(2)x2 17(.)x1 +8u  DIFFER
   0x0003  3a(:)x4 00(.)x2 61(a)x1             74(t)x4 2e(.)x2 77(w)x2 17(.)x1 +6u  DIFFER
   0x0004  20( )x4 40(@)x2 2f(/)x1             70(p)x4 74(t)x2 78(x)x2 17(.)x1 +6u  DIFFER
   0x0005  2f(/)x4 5c(\)x2 31(1)x1             70(p)x2 3a(:)x2 6d(m)x2 26(&)x2 +7u  DIFFER
   0x0006  2f(/)x4 0a(.)x2 32(2)x1             26(&)x3 3a(:)x2 2f(/)x2 6c(l)x2 +6u  PARTIAL
   0x0007  2f(/)x4 3c(<)x2 37(7)x1             2f(/)x4 00(.)x3 5c(\)x2 17(.)x1 +5u  PARTIAL
   0x0008  2f(/)x3 6d(m)x2 37(7)x1 2e(.)x1     78(x)x3 0a(.)x3 3e(>)x3 2f(/)x2 +4u  PARTIAL
   0x0009  2f(/)x4 6d(m)x2 37(7)x1             3c(<)x3 3e(>)x3 6d(m)x2 54(T)x1 +6u  PARTIAL
   0x000a  2f(/)x4 3e(>)x2 32(2)x1             3e(>)x4 6c(l)x2 3f(?)x2 41(A)x1 +6u  PARTIAL
   0x000b  2f(/)x4 2e(.)x3                     78(x)x3 3e(>)x3 29())x1 5f(_)x1 +7u  PARTIAL
   0x000c  2f(/)x4 30(0)x2 64(d)x1             3e(>)x4 0a(.)x3 2f(/)x2 6d(m)x2 +4u  PARTIAL
   0x000d  2f(/)x4 0c(.)x2 74(t)x1             6c(l)x3 3e(>)x3 3c(<)x2 37(7)x1 +6u  PARTIAL
   0x000e  2f(/)x4 41(A)x2 64(d)x1             80(.)x3 20( )x2 37(7)x1 5f(_)x1 +8u  DIFFER
   0x000f  2f(/)x4 21(!)x2 22(")x1             78(x)x2 3c(<)x2 37(7)x1 5f(_)x1 +9u  DIFFER
   0x0010  6d(m)x4 44(D)x2 3e(>)x1             6d(m)x2 65(e)x2 2f(/)x2 32(2)x1 +8u  PARTIAL
   0x0011  6c(l)x4 72(r)x2 0a(.)x1             6c(l)x2 61(a)x2 01(.)x1 78(x)x1 +9u  PARTIAL
   0x0012  5c(\)x4 67(g)x2 0a(.)x1             20( )x4 3e(>)x2 e0(.)x1 78(x)x1 +7u  DIFFER
   0x0013  74(t)x4 26(&)x2 20( )x1             76(v)x2 0a(.)x2 ff(.)x1 78(x)x1 +9u  PARTIAL
   0x0014  64(d)x4 2f(/)x2 43(C)x1             65(e)x2 64(d)x2 ff(.)x1 78(x)x1 +9u  PARTIAL
   0x0015  5c(\)x4 3a(:)x2 2f(/)x1             6e(n)x2 20( )x2 64(d)x2 06(.)x1 +8u  DIFFER
   0x0016  0a(.)x4 2f(/)x2 31(1)x1             64(d)x2 00(.)x1 73(s)x1 44(D)x1 +10u  PARTIAL
   0x0017  3c(<)x4 2f(/)x2 32(2)x1             4f(O)x2 20( )x2 64(d)x2 00(.)x1 +8u  DIFFER
   0x0018  6e(n)x4 2f(/)x2 38(8)x1             20( )x4 64(d)x2 00(.)x1 6f(o)x1 +7u  DIFFER
   0x0019  6b(k)x4 3b(;)x2 37(7)x1             6e(n)x2 64(d)x2 31(1)x1 73(s)x1 +9u  DIFFER
   0x001a  3e(>)x4 3a(:)x2 37(7)x1             64(d)x2 32(2)x1 3d(=)x1 69(i)x1 +10u  PARTIAL
   0x001b  0a(.)x4 3a(:)x2 32(2)x1             20( )x2 74(t)x2 64(d)x2 2b(+)x1 +8u  PARTIAL
   0x001c  20( )x4 3a(:)x2 2e(.)x1             64(d)x2 44(D)x1 5f(_)x1 70(p)x1 +10u  DIFFER
   0x001d  20( )x4 4a(J)x2 64(d)x1             20( )x2 6c(l)x2 32(2)x2 41(A)x1 +8u  PARTIAL
   0x001e  3c(<)x4 3a(:)x2 74(t)x1             54(T)x2 60(`)x1 ff(.)x1 44(D)x1 +10u  PARTIAL
   0x001f  62(b)x4 55(U)x2 64(d)x1             20( )x2 41(A)x1 5f(_)x1 ff(.)x1 +10u  PARTIAL
   0x0020  20( )x4 53(S)x2 22(")x1             2f(/)x2 29())x1 5f(_)x1 ff(.)x1 +10u  DIFFER
   0x0021  3b(;)x4 2d(-)x2 c2(.)x1             20( )x2 3e(>)x1 5f(_)x1 ff(.)x1 +10u  DIFFER
   0x0022  6c(l)x4 41(A)x2 0a(.)x1             78(x)x2 37(7)x1 5f(_)x1 ff(.)x1 +10u  DIFFER
   0x0023  69(i)x4 0a(.)x1 53(S)x1 3a(:)x1     37(7)x2 5f(_)x1 ff(.)x1 50(P)x1 +10u  DIFFER
   0x0024  6e(n)x4 43(C)x2 20( )x1             00(.)x2 37(7)x2 66(f)x1 ff(.)x1 +9u  PARTIAL
   0x0025  6b(k)x4 49(I)x2 3c(<)x1             20( )x3 37(7)x2 00(.)x1 61(a)x1 +8u  DIFFER
   0x0026  39(9)x4 49(I)x2 62(b)x1             32(2)x2 00(.)x1 6b(k)x1 65(e)x1 +10u  PARTIAL
   0x0027  68(h)x4 3a(:)x2 20( )x1             65(e)x2 27(')x2 20( )x2 2e(.)x2 +7u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6461.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6461,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6461 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6461 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6461 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).