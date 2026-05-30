==== BLOCKER ====
Target: libxml2
Branch ID: 6756
Location: /src/libxml2/parser.c:9890:9
Enclosing function: xmlParseCDSect
Source line:     if (!IS_CHAR(s)) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (value_profile vs value_profile)
cmplog                           0        9          1  REFERENCE
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        0        9          1  REFERENCE
naive_ngram4                     0        6          4  REFERENCE
mopt                             0        9          1  REFERENCE
minimizer                        0        9          1  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         3        6          1  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=6.20h  loser=13.60h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.80  dur_div=7.40h  hit_div=1
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6756/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseCDSect (/src/libxml2/parser.c:9862-9958) ---
[ ]  9860   */
[ ]  9861  void
[B]  9862  xmlParseCDSect(xmlParserCtxtPtr ctxt) {
[B]  9863      xmlChar *buf = NULL;
[B]  9864      int len = 0;
[B]  9865      int size = XML_PARSER_BUFFER_SIZE;
[B]  9866      int r, rl;
[B]  9867      int	s, sl;
[B]  9868      int cur, l;
[B]  9869      int count = 0;
[B]  9870      int maxLength = (ctxt->options & XML_PARSE_HUGE) ?
[B]  9871                      XML_MAX_HUGE_LENGTH :
[B]  9872                      XML_MAX_TEXT_LENGTH;
[ ]  9873  
[B]  9874      if ((CUR != '<') || (NXT(1) != '!') || (NXT(2) != '['))
[ ]  9875          return;
[B]  9876      SKIP(3);
[ ]  9877  
[B]  9878      if (!CMP6(CUR_PTR, 'C', 'D', 'A', 'T', 'A', '['))
[ ]  9879          return;
[B]  9880      SKIP(6);
[ ]  9881  
[B]  9882      ctxt->instate = XML_PARSER_CDATA_SECTION;
[B]  9883      r = CUR_CHAR(rl);
[B]  9884      if (!IS_CHAR(r)) {
[ ]  9885  	xmlFatalErr(ctxt, XML_ERR_CDATA_NOT_FINISHED, NULL);
[ ]  9886          goto out;
[ ]  9887      }
[B]  9888      NEXTL(rl);
[B]  9889      s = CUR_CHAR(sl);
[B]  9890      if (!IS_CHAR(s)) { <-- BLOCKER
[W]  9891  	xmlFatalErr(ctxt, XML_ERR_CDATA_NOT_FINISHED, NULL);
[W]  9892          goto out;
[W]  9893      }
[L]  9894      NEXTL(sl);
[L]  9895      cur = CUR_CHAR(l);
[L]  9896      buf = (xmlChar *) xmlMallocAtomic(size);
[L]  9897      if (buf == NULL) {
[ ]  9898  	xmlErrMemory(ctxt, NULL);
[ ]  9899          goto out;
[ ]  9900      }
[L]  9901      while (IS_CHAR(cur) &&
[L]  9902             ((r != ']') || (s != ']') || (cur != '>'))) {
[L]  9903  	if (len + 5 >= size) {
[L]  9904  	    xmlChar *tmp;
[ ]  9905  
[L]  9906  	    tmp = (xmlChar *) xmlRealloc(buf, size * 2);
[L]  9907  	    if (tmp == NULL) {
[ ]  9908  		xmlErrMemory(ctxt, NULL);
[ ]  9909                  goto out;
[ ]  9910  	    }
[L]  9911  	    buf = tmp;
[L]  9912  	    size *= 2;
[L]  9913  	}
[L]  9914  	COPY_BUF(rl,buf,len,r);
[L]  9915  	r = s;
[L]  9916  	rl = sl;
[L]  9917  	s = cur;
[L]  9918  	sl = l;
[L]  9919  	count++;
[L]  9920  	if (count > 50) {
[L]  9921  	    SHRINK;
[L]  9922  	    GROW;
[L]  9923              if (ctxt->instate == XML_PARSER_EOF) {
[ ]  9924                  goto out;
[ ]  9925              }
[L]  9926  	    count = 0;
[L]  9927  	}
[L]  9928  	NEXTL(l);
[L]  9929  	cur = CUR_CHAR(l);
[L]  9930          if (len > maxLength) {
[ ]  9931              xmlFatalErrMsg(ctxt, XML_ERR_CDATA_NOT_FINISHED,
[ ]  9932                             "CData section too big found\n");
[ ]  9933              goto out;
[ ]  9934          }
[L]  9935      }
[L]  9936      buf[len] = 0;
[L]  9937      if (cur != '>') {
[L]  9938  	xmlFatalErrMsgStr(ctxt, XML_ERR_CDATA_NOT_FINISHED,
[L]  9939  	                     "CData section not finished\n%.50s\n", buf);
[L]  9940          goto out;
[L]  9941      }
[ ]  9942      NEXTL(l);
[ ]  9943  
[ ]  9944      /*
[ ]  9945       * OK the buffer is to be consumed as cdata.
[ ]  9946       */
[ ]  9947      if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) {
[ ]  9948  	if (ctxt->sax->cdataBlock != NULL)
[ ]  9949  	    ctxt->sax->cdataBlock(ctxt->userData, buf, len);
[ ]  9950  	else if (ctxt->sax->characters != NULL)
[ ]  9951  	    ctxt->sax->characters(ctxt->userData, buf, len);
[ ]  9952      }
[ ]  9953  
[B]  9954  out:
[B]  9955      if (ctxt->instate != XML_PARSER_EOF)
[B]  9956          ctxt->instate = XML_PARSER_CONTENT;
[B]  9957      xmlFree(buf);
[B]  9958  }

--- Caller (1 hop): parser.c:xmlParseContentInternal (/src/libxml2/parser.c:9969-10033, calls xmlParseCDSect at line 9989) (±10 around call site) ---
[ ]  9979  	 */
[B]  9980  	if ((*cur == '<') && (cur[1] == '?')) {
[ ]  9981  	    xmlParsePI(ctxt);
[ ]  9982  	}
[ ]  9983  
[ ]  9984  	/*
[ ]  9985  	 * Second case : a CDSection
[ ]  9986  	 */
[ ]  9987  	/* 2.6.0 test was *cur not RAW */
[B]  9988  	else if (CMP9(CUR_PTR, '<', '!', '[', 'C', 'D', 'A', 'T', 'A', '[')) {
[B]  9989  	    xmlParseCDSect(ctxt); <-- CALL
[B]  9990  	}
[ ]  9991  
[ ]  9992  	/*
[ ]  9993  	 * Third case :  a comment
[ ]  9994  	 */
[B]  9995  	else if ((*cur == '<') && (NXT(1) == '!') &&
[B]  9996  		 (NXT(2) == '-') && (NXT(3) == '-')) {
[ ]  9997  	    xmlParseComment(ctxt);
[ ]  9998  	    ctxt->instate = XML_PARSER_CONTENT;
[ ]  9999  	}

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseCDSect at line 9989)
hop 3  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 3  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 4  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 4  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 5  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 5  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 5  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 5  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 6  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseReference at line 11768)
hop 6  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 6  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 7  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 7  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 7  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)
hop 8  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     893      2700  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
       0       263  parser.c:xmlSHRINK  (/src/libxml2/parser.c:2059-2066)
      14       199  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      58       211  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      26       172  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
      55       193  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
      37       174  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      37       171  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
      15       145  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
      26       154  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774)
      11       134  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226)
      11       118  parser.c:xmlParseNCNameComplex  (/src/libxml2/parser.c:3415-3471)
      11       116  parser.c:xmlIsNameStartChar  (/src/libxml2/parser.c:3152-3180)
       1        82  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      14        82  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120)
... (23 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=7   L12139  T=0 F=14  T=0 F=82  if (ctxt == NULL)
  d=7   L12141  T=0 F=6  T=0 F=34  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12141  T=6 F=8  T=34 F=48  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12143  T=0 F=14  T=0 F=82  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L12145  T=0 F=14  T=0 F=82  if (ctxt->input == NULL)
  d=7   L12149  T=8 F=6  T=21 F=61  if (ctxt->instate == XML_PARSER_START)
  d=7   L12151  T=10 F=0  T=62 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=7   L12151  T=10 F=4  T=62 F=20  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=7   L12151  T=10 F=0  T=62 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=7   L12152  T=0 F=10  T=0 F=62  (chunk[size - 1] == '\r')) {
  d=7   L12159  T=10 F=0  T=62 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=7   L12159  T=10 F=0  T=62 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=7   L12159  T=10 F=4  T=62 F=20  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=7   L12160  T=10 F=0  T=62 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=7   L12160  T=10 F=0  T=62 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=7   L12170  T=8 F=2  T=18 F=44  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=7   L12170  T=8 F=0  T=18 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=7   L12171  T=8 F=0  T=18 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=7   L12171  T=0 F=8  T=0 F=18  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=7   L12202  T=0 F=10  T=0 F=62  if (res < 0) {
  d=7   L12211  T=4 F=0  T=20 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=7   L12212  T=4 F=0  T=20 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=7   L12212  T=4 F=0  T=20 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=7   L12214  T=0 F=4  T=0 F=20  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=7   L12233  T=0 F=14  T=0 F=82  if (remain != 0) {
  d=7   L12238  T=0 F=14  T=0 F=82  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L12241  T=14 F=0  T=82 F=0  if ((ctxt->input != NULL) &&
  d=7   L12242  T=0 F=14  T=0 F=82  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=7   L12243  T=0 F=14  T=0 F=82  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=7   L12248  T=0 F=14  T=8 F=42  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12248  T=14 F=0  T=50 F=32  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12251  T=0 F=14  T=0 F=74  if (remain != 0) {
  d=7   L12257  T=0 F=14  T=0 F=74  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=7   L12268  T=4 F=10  T=6 F=68  if (terminate) {
  d=7   L12296  T=14 F=0  T=42 F=32  if (ctxt->wellFormed == 0)
--- d=6  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=6   L11409  T=0 F=14  T=0 F=82  if (ctxt->input == NULL)
  d=6   L11465  T=14 F=0  T=82 F=0  if ((ctxt->input != NULL) &&
  d=6   L11466  T=0 F=14  T=0 F=82  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=6   L11470  T=109 F=0  T=257 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=6   L11471  T=0 F=65  T=8 F=122  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L11471  T=65 F=44  T=130 F=127  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L11474  T=0 F=109  T=0 F=249  if (ctxt->input == NULL) break;
  d=6   L11475  T=0 F=109  T=0 F=249  if (ctxt->input->buf == NULL)
  d=6   L11486  T=93 F=16  T=215 F=34  if ((ctxt->instate != XML_PARSER_START) &&
  d=6   L11487  T=0 F=93  T=0 F=215  (ctxt->input->buf->raw != NULL) &&
  d=6   L11500  T=2 F=107  T=2 F=247  if (avail < 1)
  d=6   L11502  T=0 F=107  T=0 F=247  switch (ctxt->instate) {
  d=6   L11503  T=0 F=107  T=0 F=247  case XML_PARSER_EOF:
  d=6   L11508  T=16 F=91  T=34 F=213  case XML_PARSER_START:
  d=6   L11509  T=8 F=8  T=13 F=21  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=6   L11535  T=0 F=8  T=0 F=21  if (avail < 2)
  d=6   L11539  T=0 F=8  T=0 F=21  if (cur == 0) {
  d=6   L11553  T=0 F=6  T=11 F=0  if ((cur == '<') && (next == '?')) {
  d=6   L11553  T=6 F=2  T=11 F=10  if ((cur == '<') && (next == '?')) {
  d=6   L11555  T=0 F=0  T=0 F=11  if (avail < 5) goto done;
  d=6   L11556  T=0 F=0  T=9 F=2  if ((!terminate) &&
  d=6   L11557  T=0 F=0  T=5 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=6   L11559  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11559  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11562  T=0 F=0  T=6 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=6   L11563  T=0 F=0  T=6 F=0  (ctxt->input->cur[3] == 'm') &&
  d=6   L11564  T=0 F=0  T=6 F=0  (ctxt->input->cur[4] == 'l') &&
  d=6   L11572  T=0 F=0  T=0 F=6  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=6   L11581  T=0 F=0  T=6 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L11582  T=0 F=0  T=0 F=6  (ctxt->input->encoding != NULL))
  d=6   L11584  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11584  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11585  T=0 F=0  T=6 F=0  (!ctxt->disableSAX))
  d=6   L11622  T=17 F=90  T=65 F=182  case XML_PARSER_START_TAG: {
  d=6   L11629  T=0 F=17  T=0 F=65  if ((avail < 2) && (ctxt->inputNr == 1))
  d=6   L11632  T=0 F=17  T=0 F=65  if (cur != '<') {
  d=6   L11639  T=2 F=14  T=27 F=18  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11639  T=16 F=1  T=45 F=20  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11641  T=0 F=15  T=0 F=38  if (ctxt->spaceNr == 0)
  d=6   L11643  T=5 F=10  T=4 F=34  else if (*ctxt->space == -2)
  d=6   L11648  T=15 F=0  T=26 F=12  if (ctxt->sax2)
  d=6   L11655  T=0 F=15  T=0 F=38  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11657  T=0 F=15  T=0 F=38  if (name == NULL) {
  d=6   L11670  T=0 F=15  T=0 F=38  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L11678  T=0 F=15  T=0 F=38  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L11707  T=8 F=7  T=18 F=20  if (RAW == '>') {
  d=6   L11721  T=55 F=52  T=88 F=159  case XML_PARSER_CONTENT: {
  d=6   L11727  T=0 F=20  T=0 F=40  if ((cur == '<') && (next == '/')) {
  d=6   L11730  T=0 F=20  T=0 F=40  } else if ((cur == '<') && (next == '?')) {
  d=6   L11736  T=8 F=12  T=22 F=18  } else if ((cur == '<') && (next != '!')) {
  d=6   L11758  T=5 F=0  T=10 F=0  } else if ((cur == '<') && (next == '!') &&
  d=6   L11759  T=0 F=5  T=0 F=10  (avail < 9)) {
  d=6   L11783  T=35 F=0  T=38 F=10  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=6   L11792  T=0 F=107  T=0 F=247  case XML_PARSER_END_TAG:
  d=6   L11813  T=11 F=96  T=40 F=207  case XML_PARSER_CDATA_SECTION: {
  d=6   L11820  T=4 F=7  T=6 F=34  if (terminate) {
  d=6   L11831  T=11 F=0  T=40 F=0  if (term == NULL) {
  d=6   L11834  T=4 F=7  T=6 F=34  if (terminate) {
  d=6   L11838  T=7 F=0  T=4 F=30  if (avail < XML_PARSER_BIG_BUFFER_SIZE + 2)
  d=6   L11845  T=2 F=2  T=34 F=2  if (tmp <= 0) {
  d=6   L11904  T=8 F=99  T=16 F=231  case XML_PARSER_MISC:
  d=6   L11905  T=0 F=107  T=4 F=243  case XML_PARSER_PROLOG:
  d=6   L11906  T=0 F=107  T=0 F=247  case XML_PARSER_EPILOG:
  d=6   L11908  T=0 F=8  T=0 F=20  if (ctxt->input->buf == NULL)
  d=6   L11914  T=0 F=8  T=0 F=20  if (avail < 2)
  d=6   L11918  T=8 F=0  T=20 F=0  if ((cur == '<') && (next == '?')) {
  d=6   L11918  T=0 F=8  T=0 F=20  if ((cur == '<') && (next == '?')) {
  d=6   L11929  T=0 F=8  T=4 F=16  } else if ((cur == '<') && (next == '!') &&
  d=6   L11929  T=8 F=0  T=20 F=0  } else if ((cur == '<') && (next == '!') &&
  d=6   L11930  T=0 F=0  T=0 F=4  (ctxt->input->cur[2] == '-') &&
  d=6   L11942  T=8 F=0  T=16 F=4  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=6   L11943  T=0 F=8  T=4 F=12  (cur == '<') && (next == '!') &&
  d=6   L11943  T=8 F=0  T=16 F=0  (cur == '<') && (next == '!') &&
  d=6   L11944  T=0 F=0  T=4 F=0  (ctxt->input->cur[2] == 'D') &&
  d=6   L11945  T=0 F=0  T=4 F=0  (ctxt->input->cur[3] == 'O') &&
  d=6   L11946  T=0 F=0  T=4 F=0  (ctxt->input->cur[4] == 'C') &&
  d=6   L11947  T=0 F=0  T=4 F=0  (ctxt->input->cur[5] == 'T') &&
  d=6   L11948  T=0 F=0  T=4 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=6   L11949  T=0 F=0  T=4 F=0  (ctxt->input->cur[7] == 'P') &&
  d=6   L11950  T=0 F=0  T=4 F=0  (ctxt->input->cur[8] == 'E')) {
  d=6   L11951  T=0 F=0  T=4 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11951  T=0 F=0  T=0 F=4  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11959  T=0 F=0  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11961  T=0 F=0  T=0 F=4  if (RAW == '[') {
  d=6   L11972  T=0 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=6   L11972  T=0 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=6   L11973  T=0 F=0  T=4 F=0  (ctxt->sax->externalSubset != NULL))
  d=6   L11985  T=0 F=8  T=0 F=16  } else if ((cur == '<') && (next == '!') &&
  d=6   L11985  T=8 F=0  T=16 F=0  } else if ((cur == '<') && (next == '!') &&
  d=6   L11989  T=0 F=8  T=0 F=16  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=6   L12007  T=0 F=107  T=0 F=247  case XML_PARSER_DTD: {
  d=6   L12029  T=0 F=107  T=0 F=247  case XML_PARSER_COMMENT:
  d=6   L12038  T=0 F=107  T=0 F=247  case XML_PARSER_IGNORE:
  d=6   L12047  T=0 F=107  T=0 F=247  case XML_PARSER_PI:
  d=6   L12056  T=0 F=107  T=0 F=247  case XML_PARSER_ENTITY_DECL:
  d=6   L12065  T=0 F=107  T=0 F=247  case XML_PARSER_ENTITY_VALUE:
  d=6   L12074  T=0 F=107  T=0 F=247  case XML_PARSER_ATTRIBUTE_VALUE:
  d=6   L12083  T=0 F=107  T=0 F=247  case XML_PARSER_SYSTEM_LITERAL:
  d=6   L12092  T=0 F=107  T=0 F=247  case XML_PARSER_PUBLIC_LITERAL:
--- d=5  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=5   L7181  T=0 F=0  T=0 F=40  if (RAW != '&')
  d=5   L7187  T=0 F=0  T=0 F=40  if (NXT(1) == '#') {
  d=5   L7233  T=0 F=0  T=40 F=0  if (ent == NULL) return;
--- d=4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=4   L10816  T=0 F=4  T=0 F=8  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10816  T=0 F=4  T=0 F=8  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10829  T=4 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10829  T=4 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10831  T=0 F=4  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10834  T=4 F=0  T=8 F=0  if ((ctxt->encoding == NULL) &&
  d=4   L10835  T=4 F=0  T=8 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=4   L10846  T=0 F=4  T=3 F=5  if (enc != XML_CHAR_ENCODING_NONE) {
  d=4   L10852  T=0 F=4  T=0 F=8  if (CUR == 0) {
  d=4   L10863  T=0 F=4  T=0 F=8  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=4   L10872  T=0 F=0  T=0 F=3  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=4   L10873  T=0 F=0  T=0 F=3  (ctxt->instate == XML_PARSER_EOF)) {
  d=4   L10884  T=4 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=4 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=4 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10886  T=0 F=4  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10888  T=4 F=0  T=8 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10888  T=4 F=0  T=8 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10889  T=4 F=0  T=8 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10889  T=0 F=4  T=0 F=8  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10907  T=0 F=0  T=0 F=2  if (RAW == '[') {
  d=4   L10918  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10918  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10919  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=4   L10922  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10936  T=0 F=4  T=0 F=8  if (RAW != '<') {
  d=4   L10950  T=1 F=3  T=0 F=8  if (RAW != 0) {
  d=4   L10959  T=4 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10959  T=4 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10965  T=4 F=0  T=8 F=0  if ((ctxt->myDoc != NULL) &&
  d=4   L10966  T=0 F=4  T=0 F=8  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=4   L10971  T=0 F=4  T=0 F=8  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10980  T=4 F=0  T=8 F=0  if (! ctxt->wellFormed) {
--- d=3  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=3   L10077  T=0 F=4  T=0 F=8  if (xmlParseElementStart(ctxt) != 0)
  d=3   L10081  T=0 F=4  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L10084  T=3 F=1  T=8 F=0  if (CUR == 0) {
--- d=2  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=2   L9973  T=33 F=3  T=321 F=8  while ((RAW != 0) &&
  d=2   L9974  T=33 F=0  T=321 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L9980  T=12 F=21  T=134 F=187  if ((*cur == '<') && (cur[1] == '?')) {
  d=2   L9980  T=0 F=12  T=0 F=134  if ((*cur == '<') && (cur[1] == '?')) {
  d=2   L9995  T=8 F=21  T=126 F=187  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=2   L9995  T=3 F=5  T=83 F=43  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=2   L9996  T=0 F=3  T=0 F=83  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=2   L10004  T=8 F=21  T=126 F=187  else if (*cur == '<') {
  d=2   L10005  T=1 F=7  T=0 F=126  if (NXT(1) == '/') {
  d=2   L10006  T=1 F=0  T=0 F=0  if (ctxt->nameNr <= nameNr)
  d=2   L10019  T=0 F=21  T=40 F=147  else if (*cur == '&') {
--- d=1  xmlParseCDSect  (/src/libxml2/parser.c:9862-9958) ---
  d=1   L9870  T=1 F=3  T=1 F=7  int maxLength = (ctxt->options & XML_PARSE_HUGE) ?
  d=1   L9874  T=0 F=4  T=0 F=8  if ((CUR != '<') || (NXT(1) != '!') || (NXT(2) != '['))
  d=1   L9874  T=0 F=4  T=0 F=8  if ((CUR != '<') || (NXT(1) != '!') || (NXT(2) != '['))
  d=1   L9874  T=0 F=4  T=0 F=8  if ((CUR != '<') || (NXT(1) != '!') || (NXT(2) != '['))
  d=1   L9884  T=0 F=4  T=0 F=8  if (!IS_CHAR(r)) {
  d=1   L9890  T=4 F=0  T=0 F=8  if (!IS_CHAR(s)) {  <-- BLOCKER
  d=1   L9897  T=0 F=0  T=0 F=8  if (buf == NULL) {
  d=1   L9902  T=0 F=0  T=3220 F=0  ((r != ']') || (s != ']') || (cur != '>'))) {
  d=1   L9903  T=0 F=0  T=17 F=3210  if (len + 5 >= size) {
  d=1   L9907  T=0 F=0  T=0 F=17  if (tmp == NULL) {
  d=1   L9920  T=0 F=0  T=59 F=3160  if (count > 50) {
  d=1   L9923  T=0 F=0  T=0 F=59  if (ctxt->instate == XML_PARSER_EOF) {
  d=1   L9930  T=0 F=0  T=0 F=3220  if (len > maxLength) {
  d=1   L9937  T=0 F=0  T=8 F=0  if (cur != '>') {
  d=1   L9955  T=4 F=0  T=8 F=0  if (ctxt->instate != XML_PARSER_EOF)

[off-chain: 402 additional divergent branches across 54 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=6a1c49361344f20d, size=157 bytes, fuzzer=value_profile, trial=1, discovered_at=14664s, mutation_op=BytesInsertCopyMutator,BytesDeleteMutator):
  0000: 21 21 21 78 6c 72 6e 6b 20 20 0a 5c 0a 3c 61 3e   !!!xlrnk  .\.<a>
  0010: f7 20 20 3c 62 20 78 6c 96 6e 6b 6b 6b 6b 6b 6b   .  <b xl.nkkkkkk
  0020: 6b 6b 45 4e 54 20 61 20 28 62 2a 29 3e 0a 0a 3c   kkENT a (b*)>..<
  0030: 21 45 4c 45 4d 45 4e 54 44 80 00 83 74 74 70 3a   !ELEMENTD...ttp:
Seed 2 (id=a07724220965ae60, size=208 bytes, fuzzer=value_profile, trial=1, discovered_at=31481s, mutation_op=CrossoverReplaceMutator,BitFlipMutator,QwordAddMutator,BytesRandInsertMutator):
  0000: 23 49 4d 50 4d 49 45 44 3e 0a 0a 5c 0a 0a 0a 3c   #IMPMIED>..\...<
  0010: 61 3e 0a 20 20 3c 62 20 78 6c 69 6a 6a 6a 6a 6a   a>.  <b xlijjjjj
  0020: 6e 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20   n               
  0030: 6b 3a 3c 21 5b 43 44 41 54 41 5b ea 1f f8 ff ff   k:<![CDATA[.....
Seed 3 (id=2325e8045600a745, size=216 bytes, fuzzer=value_profile, trial=1, discovered_at=33125s, mutation_op=ByteAddMutator,BytesSwapMutator,ByteNegMutator):
  0000: 21 21 21 21 21 73 2f 31 32 37 37 37 32 41 54 41   !!!!!s/127772ATA
  0010: 29 3e 0a 3c 21 41 54 54 4c 49 53 54 21 62 20 78   )>.<!ATTLIST!b x
  0020: 6d 6c 6e 73 3a 78 6c 72 6e 6b 20 20 0a 5c 0a 3c   mlns:xlrnk  .\.<
  0030: 61 3e f7 20 20 3c 62 20 78 6c 96 6e 6b 6b 6b 6b   a>.  <b xl.nkkkk
Seed 4 (id=0ca3e7e2be9b7ea9, size=138 bytes, fuzzer=value_profile, trial=1, discovered_at=35915s, mutation_op=BytesDeleteMutator,ByteFlipMutator,WordAddMutator):
  0000: 21 21 21 21 21 73 2f 31 32 c8 37 37 32 41 54 3b   !!!!!s/12.772AT;
  0010: 29 3e 0a 3c 21 41 54 54 4c 49 53 54 21 62 20 78   )>.<!ATTLIST!b x
  0020: 6d 6c 6e 73 3a 78 6c 72 6e 6b 20 20 0a 5c 0a 3c   mlns:xlrnk  .\.<
  0030: 61 3e f7 20 20 3c 62 20 0a 3c 21 45 4c 45 4d 45   a>.  <b .<!ELEME

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=d0af71993ffffc89, size=316 bytes, fuzzer=naive, trial=1, discovered_at=5053s, mutation_op=BytesRandInsertMutator,BytesSetMutator,BytesInsertCopyMutator):
  0000: 65 20 20 20 36 36 36 28 73 69 93 20 70 6c 65 29   e   666(si. ple)
  0010: 20 20 23 46 20 68 74 74 70 3a 2f 78 6d 6c 5c 0a     #F http:/xml\.
  0020: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0030: 2e 30 d6 f2 f2 f2 3c 21 44 4f 43 54 59 50 45 20   .0....<!DOCTYPE 
Seed 2 (id=24053611769d46a7, size=610 bytes, fuzzer=naive, trial=1, discovered_at=8422s, mutation_op=BytesSetMutator,BytesDeleteMutator,ByteRandMutator,BytesSwapMutator,BytesRandInsertMutator,CrossoverInsertMutator):
  0000: 68 72 20 56 2f 78 6c 69 6e 6b 27 0a 59 20 20 20   hr V/xlink'.Y   
  0010: 20 20 20 20 20 78 6c 69 6e 6b 3a 74 20 20 20 20        xlink:t    
  0020: 20 20 78 6c 69 6e 6b 3a 74 79 70 65 20 20 43 28     xlink:type  C(
  0030: 73 69 6e 6e 6e 36 34 36 2d 55 43 53 ac ac ac ac   sinnn646-UCS....
Seed 3 (id=9e94fea113998f2f, size=557 bytes, fuzzer=naive, trial=1, discovered_at=8860s, mutation_op=DwordInterestingMutator,BytesCopyMutator,ByteInterestingMutator,BytesCopyMutator,BytesDeleteMutator,BytesCopyMutator,BitFlipMutator):
  0000: 68 72 20 56 2f 78 6c 69 6e 6b 27 0a 59 20 20 20   hr V/xlink'.Y   
  0010: 20 20 20 20 20 78 6c 69 6e 6b 3a 74 20 20 20 20        xlink:t    
  0020: 20 20 78 6c 69 6e 6b 3a 74 79 70 65 20 20 43 28     xlink:type  C(
  0030: 73 69 6e 6e 6e 36 34 36 2d 55 43 53 ac ac ac ac   sinnn646-UCS....
Seed 4 (id=70344916a600ed09, size=293 bytes, fuzzer=naive, trial=1, discovered_at=16287s, mutation_op=ByteRandMutator,BytesDeleteMutator,BytesExpandMutator,BytesDeleteMutator):
  0000: 20 20 20 20 20 78 6c 69 6e 6b 3a 74 20 20 20 20        xlink:t    
  0010: 20 20 78 6c 69 6e 6b 3a 74 79 70 65 20 20 20 28     xlink:type   (
  0020: 73 69 6e 6e 6e 36 34 36 2d 55 43 53 2d ac ac ac   sinnn646-UCS-...
  0030: ac ac ac ac 4c 45 4d 45 4e 54 20 61 20 68 2f 61   ....LEMENT a h/a
Seed 5 (id=61246b28182590cd, size=301 bytes, fuzzer=naive, trial=1, discovered_at=16638s, mutation_op=DwordAddMutator,BitFlipMutator,BytesExpandMutator):
  0000: 20 20 20 20 20 78 6c 69 6e 6b 3a 74 20 20 20 20        xlink:t    
  0010: 20 20 78 6c 69 6e 6b 3a 74 79 70 65 20 20 20 28     xlink:type   (
  0020: 73 69 6e 6e 6e 36 34 36 2d 55 43 53 2d ac ac ac   sinnn646-UCS-...
  0030: ac ac ac ac 4c 45 4d 45 4e 54 20 61 20 68 2f 61   ....LEMENT a h/a


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  21(!)x3 23(#)x1                     68(h)x2 20( )x2 25(%)x2 65(e)x1 +1u  DIFFER
   0x0001  21(!)x3 49(I)x1                     20( )x3 72(r)x2 25(%)x2 3f(?)x1     DIFFER
   0x0002  21(!)x3 4d(M)x1                     20( )x5 25(%)x2 0a(.)x1             DIFFER
   0x0003  21(!)x2 78(x)x1 50(P)x1             20( )x3 56(V)x2 25(%)x2 0a(.)x1     DIFFER
   0x0004  21(!)x2 6c(l)x1 4d(M)x1             2f(/)x2 20( )x2 25(%)x2 36(6)x1 +1u  DIFFER
   0x0005  73(s)x2 72(r)x1 49(I)x1             78(x)x4 25(%)x2 36(6)x1 0a(.)x1     DIFFER
   0x0006  2f(/)x2 6e(n)x1 45(E)x1             6c(l)x4 25(%)x2 36(6)x1 0a(.)x1     DIFFER
   0x0007  31(1)x2 6b(k)x1 44(D)x1             69(i)x4 25(%)x2 28(()x1 3c(<)x1     DIFFER
   0x0008  32(2)x2 20( )x1 3e(>)x1             6e(n)x4 25(%)x2 73(s)x1 61(a)x1     DIFFER
   0x0009  20( )x1 0a(.)x1 37(7)x1 c8(.)x1     6b(k)x4 25(%)x2 69(i)x1 3e(>)x1     DIFFER
   0x000a  0a(.)x2 37(7)x2                     27(')x2 3a(:)x2 6c(l)x2 93(.)x1 +1u  PARTIAL
   0x000b  5c(\)x2 37(7)x2                     20( )x2 0a(.)x2 74(t)x2 5c(\)x2     PARTIAL
   0x000c  0a(.)x2 32(2)x2                     20( )x3 59(Y)x2 0a(.)x2 70(p)x1     PARTIAL
   0x000d  41(A)x2 3c(<)x1 0a(.)x1             20( )x4 3c(<)x3 6c(l)x1             PARTIAL
   0x000e  54(T)x2 61(a)x1 0a(.)x1             20( )x4 3f(?)x2 65(e)x1 62(b)x1     DIFFER
   0x000f  3e(>)x1 3c(<)x1 41(A)x1 3b(;)x1     20( )x5 78(x)x2 29())x1             DIFFER
   0x0010  29())x2 f7(.)x1 61(a)x1             20( )x5 6d(m)x2 78(x)x1             DIFFER
   0x0011  3e(>)x3 20( )x1                     20( )x5 6c(l)x3                     PARTIAL
   0x0012  0a(.)x3 20( )x1                     20( )x4 78(x)x2 23(#)x1 69(i)x1     PARTIAL
   0x0013  3c(<)x3 20( )x1                     20( )x2 6c(l)x2 76(v)x2 46(F)x1 +1u  PARTIAL
   0x0014  21(!)x2 62(b)x1 20( )x1             20( )x3 69(i)x2 65(e)x2 3c(<)x1     PARTIAL
   0x0015  41(A)x2 20( )x1 3c(<)x1             78(x)x2 6e(n)x2 72(r)x2 68(h)x1 +1u  DIFFER
   0x0016  54(T)x2 78(x)x1 62(b)x1             6c(l)x2 6b(k)x2 73(s)x2 74(t)x1 +1u  DIFFER
   0x0017  54(T)x2 6c(l)x1 20( )x1             69(i)x4 3a(:)x2 74(t)x1 43(C)x1     DIFFER
   0x0018  4c(L)x2 96(.)x1 78(x)x1             6e(n)x2 74(t)x2 6f(o)x2 70(p)x1 +1u  DIFFER
   0x0019  49(I)x2 6e(n)x1 6c(l)x1             6b(k)x2 79(y)x2 6e(n)x2 3a(:)x1 +1u  PARTIAL
   0x001a  53(S)x2 6b(k)x1 69(i)x1             3a(:)x2 70(p)x2 3d(=)x2 2f(/)x1 +1u  DIFFER
   0x001b  54(T)x2 6b(k)x1 6a(j)x1             74(t)x2 65(e)x2 22(")x2 78(x)x1 +1u  DIFFER
   0x001c  21(!)x2 6b(k)x1 6a(j)x1             20( )x4 31(1)x2 6d(m)x1 5b([)x1     DIFFER
   0x001d  62(b)x2 6b(k)x1 6a(j)x1             20( )x4 2e(.)x2 6c(l)x1 ff(.)x1     DIFFER
   0x001e  20( )x2 6b(k)x1 6a(j)x1             20( )x4 30(0)x2 5c(\)x1 6b(k)x1     PARTIAL
   0x001f  78(x)x2 6b(k)x1 6a(j)x1             20( )x2 28(()x2 22(")x2 0a(.)x1 +1u  DIFFER
   0x0020  6d(m)x2 6b(k)x1 6e(n)x1             20( )x2 73(s)x2 3f(?)x2 3c(<)x1 +1u  DIFFER
   0x0021  6c(l)x2 6b(k)x1 20( )x1             20( )x2 69(i)x2 3e(>)x2 3f(?)x1 +1u  PARTIAL
   0x0022  6e(n)x2 45(E)x1 20( )x1             78(x)x3 6e(n)x2 0a(.)x2 2f(/)x1     PARTIAL
   0x0023  73(s)x2 4e(N)x1 20( )x1             6c(l)x2 6e(n)x2 3c(<)x2 6d(m)x1 +1u  DIFFER
   0x0024  3a(:)x2 54(T)x1 20( )x1             69(i)x2 6e(n)x2 21(!)x2 6c(l)x1 +1u  DIFFER
   0x0025  20( )x2 78(x)x2                     6e(n)x2 36(6)x2 44(D)x2 20( )x1 +1u  PARTIAL
   0x0026  6c(l)x2 61(a)x1 20( )x1             6b(k)x2 34(4)x2 4f(O)x2 76(v)x1 +1u  DIFFER
   0x0027  20( )x2 72(r)x2                     3a(:)x2 36(6)x2 43(C)x2 65(e)x1 +1u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6756.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6756,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6756 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6756 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6756 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).