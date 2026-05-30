==== BLOCKER ====
Target: libxml2
Branch ID: 6887
Location: /src/libxml2/parserInternals.c:622:11
Enclosing function: xmlCurrentChar
Source line: 		    if (val < 0x800)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ctx_coverage vs naive_ctx); loser (ngram_coverage vs naive_ngram4)
cmplog                           4        6          0  REFERENCE
value_profile                    5        5          0  REFERENCE
value_profile_cmplog             4        6          0  REFERENCE
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     8        2          0  winner (ngram_coverage vs naive)
mopt                             4        6          0  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx', 'naive_ngram4']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=10.20h  loser=18.30h
  avg hitcount on branch: winner=10  loser=1
  prob_div=0.60  dur_div=8.10h  hit_div=9
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001
--- Pair 2: naive_ngram4 > naive  [delta: ngram_coverage] ---
  subject 36  (naive_ngram4 vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.10h  loser=18.30h
  avg hitcount on branch: winner=8  loser=1
  prob_div=0.60  dur_div=7.20h  hit_div=6
  subject-level: delta_AUC=-26852220.0  p_AUC=0.0173  delta_Final=-260.4  p_final=0.0312

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6887/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlCurrentChar (/src/libxml2/parserInternals.c:558-701) ---
[ ]   556  
[ ]   557  int
[B]   558  xmlCurrentChar(xmlParserCtxtPtr ctxt, int *len) {
[B]   559      if ((ctxt == NULL) || (len == NULL) || (ctxt->input == NULL)) return(0);
[B]   560      if (ctxt->instate == XML_PARSER_EOF)
[ ]   561  	return(0);
[ ]   562  
[B]   563      if ((*ctxt->input->cur >= 0x20) && (*ctxt->input->cur <= 0x7F)) {
[B]   564  	    *len = 1;
[B]   565  	    return(*ctxt->input->cur);
[B]   566      }
[B]   567      if (ctxt->charset == XML_CHAR_ENCODING_UTF8) {
[ ]   568  	/*
[ ]   569  	 * We are supposed to handle UTF8, check it's valid
[ ]   570  	 * From rfc2044: encoding of the Unicode values on UTF-8:
[ ]   571  	 *
[ ]   572  	 * UCS-4 range (hex.)           UTF-8 octet sequence (binary)
[ ]   573  	 * 0000 0000-0000 007F   0xxxxxxx
[ ]   574  	 * 0000 0080-0000 07FF   110xxxxx 10xxxxxx
[ ]   575  	 * 0000 0800-0000 FFFF   1110xxxx 10xxxxxx 10xxxxxx
[ ]   576  	 *
[ ]   577  	 * Check for the 0x110000 limit too
[ ]   578  	 */
[B]   579  	const unsigned char *cur = ctxt->input->cur;
[B]   580  	unsigned char c;
[B]   581  	unsigned int val;
[ ]   582  
[B]   583  	c = *cur;
[B]   584  	if (c & 0x80) {
[B]   585  	    if (((c & 0x40) == 0) || (c == 0xC0))
[L]   586  		goto encoding_error;
[B]   587  	    if (cur[1] == 0) {
[ ]   588  		xmlParserInputGrow(ctxt->input, INPUT_CHUNK);
[ ]   589                  cur = ctxt->input->cur;
[ ]   590              }
[B]   591  	    if ((cur[1] & 0xc0) != 0x80)
[L]   592  		goto encoding_error;
[B]   593  	    if ((c & 0xe0) == 0xe0) {
[B]   594  		if (cur[2] == 0) {
[L]   595  		    xmlParserInputGrow(ctxt->input, INPUT_CHUNK);
[L]   596                      cur = ctxt->input->cur;
[L]   597                  }
[B]   598  		if ((cur[2] & 0xc0) != 0x80)
[L]   599  		    goto encoding_error;
[B]   600  		if ((c & 0xf0) == 0xf0) {
[L]   601  		    if (cur[3] == 0) {
[ ]   602  			xmlParserInputGrow(ctxt->input, INPUT_CHUNK);
[ ]   603                          cur = ctxt->input->cur;
[ ]   604                      }
[L]   605  		    if (((c & 0xf8) != 0xf0) ||
[L]   606  			((cur[3] & 0xc0) != 0x80))
[ ]   607  			goto encoding_error;
[ ]   608  		    /* 4-byte code */
[L]   609  		    *len = 4;
[L]   610  		    val = (cur[0] & 0x7) << 18;
[L]   611  		    val |= (cur[1] & 0x3f) << 12;
[L]   612  		    val |= (cur[2] & 0x3f) << 6;
[L]   613  		    val |= cur[3] & 0x3f;
[L]   614  		    if (val < 0x10000)
[ ]   615  			goto encoding_error;
[B]   616  		} else {
[ ]   617  		  /* 3-byte code */
[B]   618  		    *len = 3;
[B]   619  		    val = (cur[0] & 0xf) << 12;
[B]   620  		    val |= (cur[1] & 0x3f) << 6;
[B]   621  		    val |= cur[2] & 0x3f;
[B]   622  		    if (val < 0x800) <-- BLOCKER
[W]   623  			goto encoding_error;
[B]   624  		}
[B]   625  	    } else {
[ ]   626  	      /* 2-byte code */
[L]   627  		*len = 2;
[L]   628  		val = (cur[0] & 0x1f) << 6;
[L]   629  		val |= cur[1] & 0x3f;
[L]   630  		if (val < 0x80)
[ ]   631  		    goto encoding_error;
[L]   632  	    }
[L]   633  	    if (!IS_CHAR(val)) {
[L]   634  	        xmlErrEncodingInt(ctxt, XML_ERR_INVALID_CHAR,
[L]   635  				  "Char 0x%X out of allowed range\n", val);
[L]   636  	    }
[L]   637  	    return(val);
[B]   638  	} else {
[ ]   639  	    /* 1-byte code */
[L]   640  	    *len = 1;
[L]   641  	    if (*ctxt->input->cur == 0)
[L]   642  		xmlParserInputGrow(ctxt->input, INPUT_CHUNK);
[L]   643  	    if ((*ctxt->input->cur == 0) &&
[L]   644  	        (ctxt->input->end > ctxt->input->cur)) {
[L]   645  	        xmlErrEncodingInt(ctxt, XML_ERR_INVALID_CHAR,
[L]   646  				  "Char 0x0 out of allowed range\n", 0);
[L]   647  	    }
[L]   648  	    if (*ctxt->input->cur == 0xD) {
[L]   649  		if (ctxt->input->cur[1] == 0xA) {
[ ]   650  		    ctxt->input->cur++;
[ ]   651  		}
[L]   652  		return(0xA);
[L]   653  	    }
[L]   654  	    return(*ctxt->input->cur);
[L]   655  	}
[B]   656      }
[ ]   657      /*
[ ]   658       * Assume it's a fixed length encoding (1) with
[ ]   659       * a compatible encoding for the ASCII set, since
[ ]   660       * XML constructs only use < 128 chars
[ ]   661       */
[B]   662      *len = 1;
[B]   663      if (*ctxt->input->cur == 0xD) {
[B]   664  	if (ctxt->input->cur[1] == 0xA) {
[ ]   665  	    ctxt->input->cur++;
[ ]   666  	}
[B]   667  	return(0xA);
[B]   668      }
[B]   669      return(*ctxt->input->cur);
[B]   670  encoding_error:
[ ]   671      /*
[ ]   672       * An encoding problem may arise from a truncated input buffer
[ ]   673       * splitting a character in the middle. In that case do not raise
[ ]   674       * an error but return 0 to indicate an end of stream problem
[ ]   675       */
[B]   676      if (ctxt->input->end - ctxt->input->cur < 4) {
[L]   677  	*len = 0;
[L]   678  	return(0);
[L]   679      }
[ ]   680  
[ ]   681      /*
[ ]   682       * If we detect an UTF8 error that probably mean that the
[ ]   683       * input encoding didn't get properly advertised in the
[ ]   684       * declaration header. Report the error and switch the encoding
[ ]   685       * to ISO-Latin-1 (if you don't like this policy, just declare the
[ ]   686       * encoding !)
[ ]   687       */
[B]   688      {
[B]   689          char buffer[150];
[ ]   690  
[B]   691  	snprintf(&buffer[0], 149, "Bytes: 0x%02X 0x%02X 0x%02X 0x%02X\n",
[B]   692  			ctxt->input->cur[0], ctxt->input->cur[1],
[B]   693  			ctxt->input->cur[2], ctxt->input->cur[3]);
[B]   694  	__xmlErrEncoding(ctxt, XML_ERR_INVALID_CHAR,
[B]   695  		     "Input is not proper UTF-8, indicate encoding !\n%s",
[B]   696  		     BAD_CAST buffer, NULL);
[B]   697      }
[B]   698      ctxt->charset = XML_CHAR_ENCODING_8859_1;
[B]   699      *len = 1;
[B]   700      return(*ctxt->input->cur);
[B]   701  }

--- Caller (1 hop): parser.c:xmlParseCharDataComplex (/src/libxml2/parser.c:4628-4706, calls xmlCurrentChar at line 4639) (±10 around call site) ---
[B]  4629      xmlChar buf[XML_PARSER_BIG_BUFFER_SIZE + 5];
[B]  4630      int nbchar = 0;
[B]  4631      int cur, l;
[B]  4632      int count = 0;
[ ]  4633  
[B]  4634      SHRINK;
[B]  4635      GROW;
[B]  4636      cur = CUR_CHAR(l);
[B]  4637      while ((cur != '<') && /* checked */
[B]  4638             (cur != '&') &&
[B]  4639  	   (IS_CHAR(cur))) /* test also done in xmlCurrentChar() */ { <-- CALL
[B]  4640  	if ((cur == ']') && (NXT(1) == ']') && (NXT(2) == '>')) {
[L]  4641  	    xmlFatalErr(ctxt, XML_ERR_MISPLACED_CDATA_END, NULL);
[L]  4642  	}
[B]  4643  	COPY_BUF(l,buf,nbchar,cur);
[ ]  4644  	/* move current position before possible calling of ctxt->sax->characters */
[B]  4645  	NEXTL(l);
[B]  4646  	cur = CUR_CHAR(l);
[B]  4647  	if (nbchar >= XML_PARSER_BIG_BUFFER_SIZE) {
[ ]  4648  	    buf[nbchar] = 0;
[ ]  4649  

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706, calls xmlCurrentChar at line 4639)
hop 3  xmlParseCharData  (/src/libxml2/parser.c:4480-4614, calls parser.c:xmlParseCharDataComplex at line 4613)
hop 4  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseCharData at line 10027)
hop 4  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseCharData at line 11788)
hop 5  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 5  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 5  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 6  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 6  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 6  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 6  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 7  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 7  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 7  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 7  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 8  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 8  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0      1190  xmlCopyCharMultiByte  (/src/libxml2/parserInternals.c:825-854)
       0       509  parserInternals.c:xmlErrEncodingInt  (/src/libxml2/parserInternals.c:190-204)
      16       135  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      43       159  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
      52       166  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       0        30  parserInternals.c:xmlSwitchInputEncodingInt  (/src/libxml2/parserInternals.c:1032-1153)
       9        33  parser.c:xmlIsNameStartChar  (/src/libxml2/parser.c:3152-3180)
      10         2  parser.c:xmlParseNameAndCompare  (/src/libxml2/parser.c:3549-3576)
       0         7  parser.c:xmlParseLookupString  (/src/libxml2/parser.c:11137-11161)
       0         6  parser.c:xmlNsErr  (/src/libxml2/parser.c:688-700)
       0         6  xmlParsePITarget  (/src/libxml2/parser.c:5123-5155)
       0         6  xmlParsePI  (/src/libxml2/parser.c:5233-5371)
       8         2  parser.c:xmlParseEndTag1  (/src/libxml2/parser.c:8770-8816)
       7         1  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033)
       0         4  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
... (4 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=7   L7181  T=0 F=0  T=0 F=4  if (RAW != '&')
  d=7   L7187  T=0 F=0  T=0 F=4  if (NXT(1) == '#') {
  d=7   L7233  T=0 F=0  T=4 F=0  if (ent == NULL) return;
--- d=6  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=6   L10816  T=0 F=15  T=0 F=31  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=6   L10816  T=0 F=15  T=0 F=31  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=6   L10829  T=15 F=0  T=31 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L10829  T=15 F=0  T=31 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L10831  T=0 F=15  T=0 F=31  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10834  T=15 F=0  T=31 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L10835  T=15 F=0  T=31 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=6   L10846  T=0 F=15  T=11 F=20  if (enc != XML_CHAR_ENCODING_NONE) {
  d=6   L10852  T=0 F=15  T=0 F=31  if (CUR == 0) {
  d=6   L10863  T=1 F=14  T=6 F=25  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=6   L10884  T=15 F=0  T=31 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=6   L10884  T=15 F=0  T=31 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=6   L10884  T=15 F=0  T=31 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=6   L10886  T=0 F=15  T=0 F=31  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10888  T=15 F=0  T=31 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=6   L10888  T=15 F=0  T=31 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=6   L10889  T=15 F=0  T=31 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=6   L10889  T=0 F=15  T=0 F=31  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=6   L10936  T=0 F=15  T=2 F=29  if (RAW != '<') {
  d=6   L10959  T=15 F=0  T=31 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L10959  T=15 F=0  T=31 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L10965  T=15 F=0  T=31 F=0  if ((ctxt->myDoc != NULL) &&
  d=6   L10966  T=0 F=15  T=0 F=31  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=6   L10971  T=0 F=15  T=0 F=31  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=6   L10980  T=15 F=0  T=31 F=0  if (! ctxt->wellFormed) {
--- d=5  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=5   L10081  T=0 F=7  T=0 F=1  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10084  T=6 F=1  T=1 F=0  if (CUR == 0) {
--- d=5  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=5   L12139  T=0 F=75  T=0 F=160  if (ctxt == NULL)
  d=5   L12141  T=4 F=7  T=0 F=10  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L12141  T=11 F=64  T=10 F=150  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L12143  T=0 F=71  T=0 F=160  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L12145  T=0 F=71  T=0 F=160  if (ctxt->input == NULL)
  d=5   L12149  T=30 F=41  T=69 F=91  if (ctxt->instate == XML_PARSER_START)
  d=5   L12151  T=42 F=29  T=75 F=85  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=5   L12152  T=0 F=42  T=2 F=73  (chunk[size - 1] == '\r')) {
  d=5   L12159  T=42 F=29  T=81 F=85  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=5   L12170  T=30 F=0  T=63 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=5   L12171  T=30 F=0  T=63 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=5   L12171  T=0 F=30  T=10 F=53  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=5   L12174  T=0 F=0  T=10 F=0  if ((xmlStrcasestr(BAD_CAST ctxt->input->buf->encoder->name,
  d=5   L12185  T=0 F=0  T=10 F=0  if (ctxt->input->buf->rawconsumed < len)
  d=5   L12193  T=0 F=0  T=6 F=4  if ((unsigned int) size > len) {
  d=5   L12211  T=29 F=0  T=85 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=5   L12212  T=29 F=0  T=85 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=5   L12212  T=29 F=0  T=85 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=5   L12214  T=0 F=29  T=30 F=55  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=5   L12214  T=0 F=0  T=30 F=0  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=5   L12215  T=0 F=0  T=30 F=0  (in->raw != NULL)) {
  d=5   L12222  T=0 F=0  T=0 F=30  if (nbchars < 0) {
  d=5   L12233  T=0 F=71  T=6 F=160  if (remain != 0) {
  d=5   L12238  T=5 F=66  T=4 F=162  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L12241  T=66 F=0  T=162 F=0  if ((ctxt->input != NULL) &&
  d=5   L12242  T=0 F=66  T=0 F=162  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=5   L12243  T=0 F=66  T=0 F=162  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=5   L12248  T=6 F=26  T=4 F=64  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L12248  T=32 F=34  T=68 F=94  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L12251  T=0 F=60  T=6 F=152  if (remain != 0) {
  d=5   L12257  T=0 F=0  T=2 F=0  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=5   L12257  T=0 F=60  T=2 F=150  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=5   L12258  T=0 F=0  T=2 F=0  (ctxt->input->buf != NULL)) {
  d=5   L12268  T=14 F=46  T=50 F=102  if (terminate) {
  d=5   L12274  T=14 F=0  T=50 F=0  if (ctxt->input != NULL) {
  d=5   L12275  T=0 F=14  T=0 F=50  if (ctxt->input->buf == NULL)
  d=5   L12283  T=14 F=0  T=50 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=5   L12284  T=14 F=0  T=50 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=5   L12287  T=0 F=14  T=0 F=50  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=5   L12290  T=14 F=0  T=50 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=5   L12291  T=14 F=0  T=50 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L12291  T=14 F=0  T=50 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L12296  T=26 F=34  T=61 F=91  if (ctxt->wellFormed == 0)
--- d=4  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=4   L9973  T=38 F=6  T=2 F=1  while ((RAW != 0) &&
  d=4   L9974  T=38 F=0  T=2 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=4   L9980  T=8 F=30  T=0 F=2  if ((*cur == '<') && (cur[1] == '?')) {
  d=4   L9980  T=0 F=8  T=0 F=0  if ((*cur == '<') && (cur[1] == '?')) {
  d=4   L9995  T=8 F=30  T=0 F=2  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=4   L9995  T=0 F=8  T=0 F=0  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=4   L10004  T=8 F=30  T=0 F=2  else if (*cur == '<') {
  d=4   L10005  T=1 F=7  T=0 F=0  if (NXT(1) == '/') {
  d=4   L10006  T=1 F=0  T=0 F=0  if (ctxt->nameNr <= nameNr)
  d=4   L10019  T=0 F=30  T=0 F=2  else if (*cur == '&') {
--- d=4  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=4   L11409  T=0 F=71  T=0 F=166  if (ctxt->input == NULL)
  d=4   L11465  T=71 F=0  T=166 F=0  if ((ctxt->input != NULL) &&
  d=4   L11466  T=0 F=71  T=0 F=166  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=4   L11470  T=508 F=0  T=1030 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=4   L11471  T=6 F=340  T=4 F=699  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L11471  T=346 F=162  T=703 F=327  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L11474  T=0 F=502  T=0 F=1020  if (ctxt->input == NULL) break;
  d=4   L11475  T=0 F=502  T=0 F=1020  if (ctxt->input->buf == NULL)
  d=4   L11486  T=442 F=60  T=906 F=120  if ((ctxt->instate != XML_PARSER_START) &&
  d=4   L11487  T=0 F=442  T=402 F=504  (ctxt->input->buf->raw != NULL) &&
  d=4   L11488  T=0 F=0  T=103 F=299  (xmlBufIsEmpty(ctxt->input->buf->raw) == 0)) {
  d=4   L11500  T=14 F=488  T=48 F=978  if (avail < 1)
  d=4   L11502  T=0 F=488  T=0 F=978  switch (ctxt->instate) {
  d=4   L11503  T=0 F=488  T=0 F=978  case XML_PARSER_EOF:
  d=4   L11508  T=60 F=428  T=120 F=858  case XML_PARSER_START:
  d=4   L11509  T=30 F=30  T=51 F=69  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=4   L11535  T=0 F=30  T=0 F=69  if (avail < 2)
  d=4   L11539  T=0 F=30  T=0 F=69  if (cur == 0) {
  d=4   L11553  T=0 F=20  T=11 F=56  if ((cur == '<') && (next == '?')) {
  d=4   L11553  T=20 F=10  T=67 F=2  if ((cur == '<') && (next == '?')) {
  d=4   L11555  T=0 F=0  T=0 F=11  if (avail < 5) goto done;
  d=4   L11556  T=0 F=0  T=7 F=4  if ((!terminate) &&
  d=4   L11557  T=0 F=0  T=7 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=4   L11559  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L11559  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L11562  T=0 F=0  T=4 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=4   L11563  T=0 F=0  T=2 F=2  (ctxt->input->cur[3] == 'm') &&
  d=4   L11564  T=0 F=0  T=0 F=2  (ctxt->input->cur[4] == 'l') &&
  d=4   L11594  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=4   L11594  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=4   L11595  T=0 F=0  T=4 F=0  (!ctxt->disableSAX))
  d=4   L11622  T=95 F=393  T=171 F=807  case XML_PARSER_START_TAG: {
  d=4   L11678  T=0 F=12  T=0 F=0  if ((RAW == '/') && (NXT(1) == '>')) {
  d=4   L11678  T=12 F=43  T=0 F=76  if ((RAW == '/') && (NXT(1) == '>')) {
  d=4   L11721  T=291 F=197  T=623 F=355  case XML_PARSER_CONTENT: {
  d=4   L11722  T=1 F=290  T=2 F=621  if ((avail < 2) && (ctxt->inputNr == 1))
  d=4   L11722  T=1 F=0  T=2 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=4   L11727  T=44 F=246  T=40 F=581  if ((cur == '<') && (next == '/')) {
  d=4   L11730  T=34 F=246  T=38 F=581  } else if ((cur == '<') && (next == '?')) {
  d=4   L11736  T=34 F=246  T=38 F=581  } else if ((cur == '<') && (next != '!')) {
  d=4   L11739  T=4 F=246  T=14 F=581  } else if ((cur == '<') && (next == '!') &&
  d=4   L11739  T=4 F=0  T=14 F=0  } else if ((cur == '<') && (next == '!') &&
  d=4   L11740  T=0 F=4  T=0 F=14  (ctxt->input->cur[2] == '-') &&
  d=4   L11747  T=4 F=0  T=14 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=4   L11747  T=4 F=246  T=14 F=581  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=4   L11748  T=0 F=4  T=2 F=12  (ctxt->input->cur[2] == '[') &&
  d=4   L11749  T=0 F=0  T=2 F=0  (ctxt->input->cur[3] == 'C') &&
  d=4   L11750  T=0 F=0  T=2 F=0  (ctxt->input->cur[4] == 'D') &&
  d=4   L11751  T=0 F=0  T=2 F=0  (ctxt->input->cur[5] == 'A') &&
  d=4   L11752  T=0 F=0  T=2 F=0  (ctxt->input->cur[6] == 'T') &&
  d=4   L11753  T=0 F=0  T=2 F=0  (ctxt->input->cur[7] == 'A') &&
  d=4   L11754  T=0 F=0  T=0 F=2  (ctxt->input->cur[8] == '[')) {
  d=4   L11758  T=4 F=246  T=14 F=581  } else if ((cur == '<') && (next == '!') &&
  d=4   L11758  T=4 F=0  T=14 F=0  } else if ((cur == '<') && (next == '!') &&
  d=4   L11759  T=0 F=4  T=0 F=14  (avail < 9)) {
  d=4   L11761  T=4 F=246  T=14 F=581  } else if (cur == '<') {
  d=4   L11765  T=0 F=246  T=4 F=577  } else if (cur == '&') {
  d=4   L11766  T=0 F=0  T=2 F=2  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=4   L11766  T=0 F=0  T=0 F=2  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=4   L11782  T=246 F=0  T=577 F=0  if ((ctxt->inputNr == 1) &&
  d=4   L11783  T=238 F=8  T=507 F=70  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=4   L11784  T=77 F=161  T=116 F=391  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=4   L11792  T=11 F=477  T=2 F=976  case XML_PARSER_END_TAG:
  d=4   L11793  T=0 F=11  T=0 F=2  if (avail < 2)
  d=4   L11795  T=2 F=2  T=0 F=2  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=4   L11795  T=4 F=7  T=2 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=4   L11797  T=1 F=8  T=0 F=2  if (ctxt->sax2) {
  d=4   L11805  T=0 F=9  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF) {
  d=4   L11807  T=1 F=8  T=0 F=2  } else if (ctxt->nameNr == 0) {
  d=4   L11813  T=0 F=488  T=0 F=978  case XML_PARSER_CDATA_SECTION: {
  d=4   L11904  T=30 F=458  T=62 F=916  case XML_PARSER_MISC:
  d=4   L11905  T=0 F=488  T=0 F=978  case XML_PARSER_PROLOG:
  d=4   L11906  T=1 F=487  T=0 F=978  case XML_PARSER_EPILOG:
  d=4   L11908  T=0 F=31  T=0 F=62  if (ctxt->input->buf == NULL)
  d=4   L11914  T=0 F=31  T=0 F=62  if (avail < 2)
  d=4   L11918  T=30 F=1  T=62 F=0  if ((cur == '<') && (next == '?')) {
  d=4   L11918  T=0 F=30  T=4 F=58  if ((cur == '<') && (next == '?')) {
  d=4   L11919  T=0 F=0  T=0 F=4  if ((!terminate) &&
  d=4   L11927  T=0 F=0  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L11929  T=30 F=1  T=58 F=0  } else if ((cur == '<') && (next == '!') &&
  d=4   L11942  T=30 F=1  T=58 F=0  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=4   L11985  T=30 F=1  T=58 F=0  } else if ((cur == '<') && (next == '!') &&
  d=4   L11989  T=1 F=30  T=0 F=58  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=4   L11996  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L11996  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12007  T=0 F=488  T=0 F=978  case XML_PARSER_DTD: {
  d=4   L12029  T=0 F=488  T=0 F=978  case XML_PARSER_COMMENT:
  d=4   L12038  T=0 F=488  T=0 F=978  case XML_PARSER_IGNORE:
  d=4   L12047  T=0 F=488  T=0 F=978  case XML_PARSER_PI:
  d=4   L12056  T=0 F=488  T=0 F=978  case XML_PARSER_ENTITY_DECL:
  d=4   L12065  T=0 F=488  T=0 F=978  case XML_PARSER_ENTITY_VALUE:
  d=4   L12074  T=0 F=488  T=0 F=978  case XML_PARSER_ATTRIBUTE_VALUE:
  d=4   L12083  T=0 F=488  T=0 F=978  case XML_PARSER_SYSTEM_LITERAL:
  d=4   L12092  T=0 F=488  T=0 F=978  case XML_PARSER_PUBLIC_LITERAL:
--- d=3  xmlParseCharData  (/src/libxml2/parser.c:4480-4614) ---
  d=3   L4497  T=3 F=269  T=3 F=569  if (*in == 0xA) {
  d=3   L4501  T=0 F=3  T=1 F=3  } while (*in == 0xA);
  d=3   L4504  T=0 F=269  T=0 F=569  if (*in == '<') {
  d=3   L4540  T=29 F=291  T=18 F=773  if (*in == 0xA) {
  d=3   L4544  T=24 F=29  T=2 F=18  } while (*in == 0xA);
  d=3   L4547  T=22 F=269  T=252 F=521  if (*in == ']') {
  d=3   L4548  T=0 F=11  T=48 F=128  if ((in[1] == ']') && (in[2] == '>')) {
  d=3   L4548  T=11 F=11  T=176 F=76  if ((in[1] == ']') && (in[2] == '>')) {
  d=3   L4566  T=0 F=4  T=0 F=14  if (areBlanks(ctxt, tmp, nbchar, 0)) {
  d=3   L4571  T=4 F=0  T=14 F=0  if (ctxt->sax->characters != NULL)
  d=3   L4574  T=0 F=4  T=3 F=11  if (*ctxt->space == -1)
  d=3   L4588  T=0 F=269  T=5 F=516  if (*in == 0xD) {
  d=3   L4590  T=0 F=0  T=0 F=5  if (*in == 0xA) {
  d=3   L4601  T=0 F=240  T=0 F=505  if (*in == '&') {
  d=3   L4606  T=0 F=240  T=0 F=505  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L4609  T=121 F=119  T=338 F=167  } while (((*in >= 0x20) && (*in <= 0x7F)) ||
  d=3   L4609  T=0 F=121  T=0 F=338  } while (((*in >= 0x20) && (*in <= 0x7F)) ||
  d=3   L4610  T=0 F=240  T=0 F=505  (*in == 0x09) || (*in == 0x0a));
  d=3   L4610  T=0 F=240  T=0 F=505  (*in == 0x09) || (*in == 0x0a));
--- d=2  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706) ---
  d=2   L4638  T=1870 F=0  T=2710 F=2  (cur != '&') &&
  d=2   L4640  T=0 F=16  T=6 F=8  if ((cur == ']') && (NXT(1) == ']') && (NXT(2) == '>')) {
  d=2   L4681  T=121 F=119  T=211 F=294  if (nbchar != 0) {
  d=2   L4686  T=112 F=9  T=211 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) {
  d=2   L4699  T=227 F=13  T=463 F=42  if ((ctxt->input->cur < ctxt->input->end) && (!IS_CHAR(cu...
  d=2   L4699  T=202 F=25  T=449 F=14  if ((ctxt->input->cur < ctxt->input->end) && (!IS_CHAR(cu...
  d=2   L4703  T=89 F=113  T=267 F=182  cur ? cur : CUR);
--- d=1  xmlCurrentChar  (/src/libxml2/parserInternals.c:558-701) ---
  d=1   L 567  T=42 F=921  T=2020 F=696  if (ctxt->charset == XML_CHAR_ENCODING_UTF8) {
  d=1   L 584  T=42 F=0  T=1870 F=148  if (c & 0x80) {
  d=1   L 585  T=0 F=42  T=25 F=1840  if (((c & 0x40) == 0) || (c == 0xC0))
  d=1   L 585  T=0 F=42  T=0 F=1840  if (((c & 0x40) == 0) || (c == 0xC0))
  d=1   L 587  T=0 F=42  T=0 F=1840  if (cur[1] == 0) {
  d=1   L 591  T=0 F=42  T=3 F=1840  if ((cur[1] & 0xc0) != 0x80)
  d=1   L 593  T=42 F=0  T=1780 F=60  if ((c & 0xe0) == 0xe0) {
  d=1   L 594  T=0 F=42  T=11 F=1770  if (cur[2] == 0) {
  d=1   L 598  T=0 F=42  T=19 F=1760  if ((cur[2] & 0xc0) != 0x80)
  d=1   L 600  T=0 F=42  T=31 F=1730  if ((c & 0xf0) == 0xf0) {
  d=1   L 601  T=0 F=0  T=0 F=31  if (cur[3] == 0) {
  d=1   L 605  T=0 F=0  T=0 F=31  if (((c & 0xf8) != 0xf0) ||
  d=1   L 606  T=0 F=0  T=0 F=31  ((cur[3] & 0xc0) != 0x80))
  d=1   L 614  T=0 F=0  T=0 F=31  if (val < 0x10000)
  d=1   L 622  T=42 F=0  T=0 F=1730  if (val < 0x800)  <-- BLOCKER
  d=1   L 630  T=0 F=0  T=0 F=60  if (val < 0x80)
  d=1   L 633  T=0 F=0  T=225 F=1600  if (!IS_CHAR(val)) {
  d=1   L 641  T=0 F=0  T=125 F=23  if (*ctxt->input->cur == 0)
  d=1   L 643  T=0 F=0  T=125 F=23  if ((*ctxt->input->cur == 0) &&
  d=1   L 644  T=0 F=0  T=100 F=25  (ctxt->input->end > ctxt->input->cur)) {
  d=1   L 648  T=0 F=0  T=3 F=145  if (*ctxt->input->cur == 0xD) {
  d=1   L 649  T=0 F=0  T=0 F=3  if (ctxt->input->cur[1] == 0xA) {
  d=1   L 664  T=0 F=2  T=0 F=18  if (ctxt->input->cur[1] == 0xA) {
  d=1   L 676  T=0 F=42  T=11 F=36  if (ctxt->input->end - ctxt->input->cur < 4) {

[off-chain: 613 additional divergent branches across 54 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0020c73cfac74f46, size=268 bytes, fuzzer=naive_ngram4, trial=2):
  0000: 62 20 78 6d 6c 6e 63 3a 78 30 2f 3f 3f 3f 3f 3f   b xmlnc:x0/?????
  0010: 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 3f 2f 2f 2f 23   OOOOOOOOOOO?///#
  0020: 2f 2f 11 10 00 96 98 00 2f 2d 6e 10 74 01 00 0a   //....../-n.t...
  0030: 2f 2f 2f 74 22 49 0a 2f 2f 2f 2f 53 53 53 53 53   ///t"I.////SSSSS
Seed 2 (id=009a93593c0b86a3, size=275 bytes, fuzzer=naive_ngram4, trial=2):
  0000: 2c f2 fa 80 5c 0a 3c 50 3e e0 99 99 5b 0a 3c 3a   ,...\.<P>...[.<:
  0010: 00 08 01 00 30 30 30 30 30 30 30 30 30 30 30 e0   ....00000000000.
  0020: 99 99 99 99 93 96 96 15 15 15 15 15 15 15 15 15   ................
  0030: 15 15 15 15 15 15 5d 5d 5f 4f 69 69 69 69 99 37   ......]]_Oiiii.7
Seed 3 (id=0e52124c225d589d, size=135 bytes, fuzzer=naive_ngram4, trial=2):
  0000: 99 37 58 2c f2 fa 80 5c 0a 3c 50 3e e0 99 99 5b   .7X,...\.<P>...[
  0010: 0a 3c 50 3e 00 80 50 45 20 61 20 53 6c 10 e0 99   .<P>..PE a Sl...
  0020: 99 99 99 93 96 96 96 96 96 96 96 96 96 96 96 99   ................
  0030: 99 95 99 99 c4 5d 5d 5f 4f 99 99 99 99 99 99 95   .....]]_O.......
Seed 4 (id=0f3652878c4ac616, size=236 bytes, fuzzer=naive_ngram4, trial=2):
  0000: 43 50 3e e0 9b 99 5c 0a 3c 50 3e e0 99 99 1e 99   CP>...\.<P>.....
  0010: 99 99 95 99 99 c4 5d 5d 5e 4f 99 99 99 99 99 99   ......]]^O......
  0020: 95 99 99 c4 7f 62 20 5d 2f 62 ff 7f 3c 2f 9f 80   .....b ]/b..</..
  0030: 00 00 00 c0 c8 ff 7f 00 00 00 00 80 81 64 64 64   .............ddd
Seed 5 (id=1e00b69c9579321f, size=77 bytes, fuzzer=naive_ngram4, trial=2):
  0000: 01 01 00 e7 01 08 08 08 08 08 9c 9d 9c 9c 9c 9c   ................
  0010: 9c 64 9c 9c 9c 9c 00 ff f4 a2 ff ff ff 00 10 00   .d..............
  0020: 00 00 40 39 01 01 ff 01 01 01 01 01 01 01 01 01   ..@9............
  0030: 01 70 3a 2f 7f 2e 2f 2f 01 39 2d 80 5c 0a 3c 69   .p:/..//.9-.\.<i

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0ae9d40906f8d16e, size=263 bytes, fuzzer=naive, trial=1, discovered_at=3168s, mutation_op=ByteInterestingMutator,CrossoverReplaceMutator,TokenReplace,ByteNegMutator,WordAddMutator,BitFlipMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 49 53 4f 2d   ....127772.xISO-
  0010: 31 30 36 34 ca 2d 55 43 53 2d 32 6d 6c 5c 0a 3c   1064.-UCS-2ml\.<
  0020: 3f 78 6d 73 73 73 68 74 74 3c 62 20 78 6c 69 6e   ?xmssshtt<b xlin
  0030: 6b 3a 68 72 65 66 3d 22 68 74 74 70 3a 2f 2f 65   k:href="http://e
Seed 2 (id=0c0cc5fa6e59cf7b, size=138 bytes, fuzzer=naive, trial=1, discovered_at=4329s, mutation_op=BytesInsertCopyMutator):
  0000: 4d 20 43 db db ff 80 78 6d 43 db db ff 80 78 6d   M C....xmC....xm
  0010: 6c 5c 0a 3c 56 56 56 56 56 56 56 56 56 69 6f 37   l\.<VVVVVVVVVio7
  0020: e8 8a ad 56 56 56 56 56 56 56 56 56 69 6f 37 e8   ...VVVVVVVVVio7.
  0030: 8a ad 9c f0 4c ff 6e 3d 22 31 2e 30 de 9c ff ff   ....L.n="1.0....
Seed 3 (id=cfac0fd5f1668af0, size=260 bytes, fuzzer=naive, trial=5, discovered_at=4864s, mutation_op=ByteRandMutator,BytesExpandMutator,BytesExpandMutator):
  0000: 06 b4 b4 b4 b4 b4 b4 b4 00 00 00 31 cf cf cf 37   ...........1...7
  0010: 1a 2e 78 6d 6c 5c 0a 3c 3f 78 49 53 4f 2d 38 38   ..xml\.<?xISO-88
  0020: ec ac ac 78 49 53 4f 2d 38 38 49 53 4f 2d 38 38   ...xISO-88ISO-88
  0030: ec ac ac 78 49 53 4f 2d 38 38 ec ac ac ac ac ac   ...xISO-88......
Seed 4 (id=57b81f636fd6e03a, size=177 bytes, fuzzer=naive, trial=4, discovered_at=5452s, mutation_op=BytesExpandMutator,TokenInsert):
  0000: 1f 0a 3c 2f 61 3e 0a 06 00 00 00 31 32 37 37 37   ..</a>.....12777
  0010: 32 2e 78 6d 6c 5c 0a 3c e8 8b 8b 3d 0a 5c 5c 0a   2.xml\.<...=.\\.
  0020: 3c e8 8b 8b 3d 0a 5c 0a 64 20 20 20 20 2e 6e 65   <...=.\.d    .ne
  0030: 74 b7 b7 b7 b7 b7 49 53 4f 2d 31 30 36 34 36 2d   t.....ISO-10646-
Seed 5 (id=65c67326bbba8ad6, size=138 bytes, fuzzer=naive, trial=1, discovered_at=6367s, mutation_op=ByteIncMutator,WordInterestingMutator,DwordAddMutator,BytesSetMutator):
  0000: 4d 20 43 db db ff 80 78 6d 43 db db ff 80 78 6d   M C....xmC....xm
  0010: 6c 5c 0a 3c 56 56 56 00 10 56 56 56 56 69 6f 37   l\.<VVV..VVVVio7
  0020: e8 8a ad 56 56 56 56 56 56 56 56 56 69 6f 37 e8   ...VVVVVVVVVio7.
  0030: 8a e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8 e8   ................


==== BYTE DIFF (W vs L at common offsets) ====
[no informative byte-level divergence — seeds look structurally similar across W and L at every offset, OR diverge only at high-entropy positions (noise)]

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

--- naive_ngram4 ---
**Instrumentation**: naive's edge counters, but the executor installs
an `NgramHook` (`HookableInProcessExecutor`) that folds a rolling
history of the last 4 edge IDs into the map index. A map slot
therefore encodes a length-4 edge path (an n-gram of N=4) rather than
a single edge.

**Feedback**: `MaxMapFeedback` over the n-gram-indexed map — a "new
bucket" is a previously-unseen 4-edge path tuple.

**Mutators**: naive's havoc + token stack. No I2S, no CMP_MAP. Stages
are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no dash rows.

**Per-execution cost**: edge increment plus a rolling 4-edge-history
update per executed edge.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6887.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6887,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage), naive_ngram4>naive (ngram_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6887 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6887 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6887 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).