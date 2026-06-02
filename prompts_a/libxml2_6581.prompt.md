==== BLOCKER ====
Target: libxml2
Branch ID: 6581
Location: /src/libxml2/parser.c:4653:33
Enclosing function: parser.c:xmlParseCharDataComplex
Source line: 	    if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        8          1  loser (ctx_coverage vs naive_ctx)
cmplog                           2        7          1  REFERENCE
value_profile                    0       10          0  REFERENCE
value_profile_cmplog             2        5          3  REFERENCE
naive_ctx                        9        1          0  winner (ctx_coverage vs naive)
naive_ngram4                     1        6          3  REFERENCE
mopt                             3        6          1  REFERENCE
minimizer                        2        7          1  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         0        6          4  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=8  unreached=1
  avg duration blocked: winner=8.10h  loser=15.67h
  avg hitcount on branch: winner=3  loser=0
  prob_div=0.79  dur_div=7.57h  hit_div=3
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6581/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlParseCharDataComplex (/src/libxml2/parser.c:4628-4706) ---
[ ]  4626   */
[ ]  4627  static void
[B]  4628  xmlParseCharDataComplex(xmlParserCtxtPtr ctxt) {
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
[B]  4639  	   (IS_CHAR(cur))) /* test also done in xmlCurrentChar() */ {
[B]  4640  	if ((cur == ']') && (NXT(1) == ']') && (NXT(2) == '>')) {
[ ]  4641  	    xmlFatalErr(ctxt, XML_ERR_MISPLACED_CDATA_END, NULL);
[ ]  4642  	}
[B]  4643  	COPY_BUF(l,buf,nbchar,cur);
[ ]  4644  	/* move current position before possible calling of ctxt->sax->characters */
[B]  4645  	NEXTL(l);
[B]  4646  	cur = CUR_CHAR(l);
[B]  4647  	if (nbchar >= XML_PARSER_BIG_BUFFER_SIZE) {
[B]  4648  	    buf[nbchar] = 0;
[ ]  4649  
[ ]  4650  	    /*
[ ]  4651  	     * OK the segment is to be consumed as chars.
[ ]  4652  	     */
[B]  4653  	    if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) { <-- BLOCKER
[L]  4654  		if (areBlanks(ctxt, buf, nbchar, 0)) {
[ ]  4655  		    if (ctxt->sax->ignorableWhitespace != NULL)
[ ]  4656  			ctxt->sax->ignorableWhitespace(ctxt->userData,
[ ]  4657  			                               buf, nbchar);
[L]  4658  		} else {
[L]  4659  		    if (ctxt->sax->characters != NULL)
[L]  4660  			ctxt->sax->characters(ctxt->userData, buf, nbchar);
[L]  4661  		    if ((ctxt->sax->characters !=
[L]  4662  		         ctxt->sax->ignorableWhitespace) &&
[L]  4663  			(*ctxt->space == -1))
[ ]  4664  			*ctxt->space = -2;
[L]  4665  		}
[L]  4666  	    }
[B]  4667  	    nbchar = 0;
[ ]  4668              /* something really bad happened in the SAX callback */
[B]  4669              if (ctxt->instate != XML_PARSER_CONTENT)
[ ]  4670                  return;
[B]  4671  	}
[B]  4672  	count++;
[B]  4673  	if (count > 50) {
[B]  4674  	    SHRINK;
[B]  4675  	    GROW;
[B]  4676  	    count = 0;
[B]  4677              if (ctxt->instate == XML_PARSER_EOF)
[ ]  4678  		return;
[B]  4679  	}
[B]  4680      }
[B]  4681      if (nbchar != 0) {
[B]  4682          buf[nbchar] = 0;
[ ]  4683  	/*
[ ]  4684  	 * OK the segment is to be consumed as chars.
[ ]  4685  	 */
[B]  4686  	if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) {
[L]  4687  	    if (areBlanks(ctxt, buf, nbchar, 0)) {
[ ]  4688  		if (ctxt->sax->ignorableWhitespace != NULL)
[ ]  4689  		    ctxt->sax->ignorableWhitespace(ctxt->userData, buf, nbchar);
[L]  4690  	    } else {
[L]  4691  		if (ctxt->sax->characters != NULL)
[L]  4692  		    ctxt->sax->characters(ctxt->userData, buf, nbchar);
[L]  4693  		if ((ctxt->sax->characters != ctxt->sax->ignorableWhitespace) &&
[L]  4694  		    (*ctxt->space == -1))
[L]  4695  		    *ctxt->space = -2;
[L]  4696  	    }
[L]  4697  	}
[B]  4698      }
[B]  4699      if ((ctxt->input->cur < ctxt->input->end) && (!IS_CHAR(cur))) {
[ ]  4700  	/* Generate the error and skip the offending character */
[B]  4701          xmlFatalErrMsgInt(ctxt, XML_ERR_INVALID_CHAR,
[B]  4702                            "PCDATA invalid Char value %d\n",
[B]  4703  	                  cur ? cur : CUR);
[B]  4704  	NEXT;
[B]  4705      }
[B]  4706  }

--- Caller (1 hop): xmlParseCharData (/src/libxml2/parser.c:4480-4614, calls parser.c:xmlParseCharDataComplex at line 4613) (±10 around call site) ---
[L]  4603          }
[B]  4604          SHRINK;
[B]  4605          GROW;
[B]  4606          if (ctxt->instate == XML_PARSER_EOF)
[ ]  4607              return;
[B]  4608          in = ctxt->input->cur;
[B]  4609      } while (((*in >= 0x20) && (*in <= 0x7F)) ||
[B]  4610               (*in == 0x09) || (*in == 0x0a));
[B]  4611      ctxt->input->line = line;
[B]  4612      ctxt->input->col = col;
[B]  4613      xmlParseCharDataComplex(ctxt); <-- CALL
[B]  4614  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseCharData  (/src/libxml2/parser.c:4480-4614, calls parser.c:xmlParseCharDataComplex at line 4613)
hop 3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseCharData at line 10027)
hop 3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseCharData at line 11788)
hop 4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 4  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 4  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 5  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 5  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 5  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 6  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 6  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 6  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 6  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 7  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 7  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 8  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 8  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     625      5340  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      15       251  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706)  <-- enclosing
       6       229  parser.c:xmlFatalErrMsgInt  (/src/libxml2/parser.c:572-586)
      45       252  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
       0       140  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
       0       135  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942)
      89         9  parser.c:xmlSHRINK  (/src/libxml2/parser.c:2059-2066)
      59        17  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      13        52  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      53        17  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
      45        10  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774)
      15        50  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120)
      33         5  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226)
      31        10  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
       4        20  parser.c:xmlParseLookupCharData  (/src/libxml2/parser.c:11170-11184)
... (20 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=6  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=6   L7181  T=0 F=0  T=0 F=4  if (RAW != '&')
  d=6   L7187  T=0 F=0  T=0 F=4  if (NXT(1) == '#') {
  d=6   L7233  T=0 F=0  T=4 F=0  if (ent == NULL) return;
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10816  T=0 F=2  T=0 F=5  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10816  T=0 F=2  T=0 F=5  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=5   L10829  T=2 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10829  T=2 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L10831  T=0 F=2  T=0 F=5  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10834  T=2 F=0  T=5 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L10835  T=2 F=0  T=5 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=5   L10846  T=2 F=0  T=4 F=1  if (enc != XML_CHAR_ENCODING_NONE) {
  d=5   L10852  T=0 F=2  T=0 F=5  if (CUR == 0) {
  d=5   L10863  T=0 F=2  T=0 F=5  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=5   L10872  T=0 F=2  T=0 F=0  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=5   L10873  T=0 F=2  T=0 F=0  (ctxt->instate == XML_PARSER_EOF)) {
  d=5   L10884  T=2 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=2 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10884  T=2 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=5   L10886  T=0 F=2  T=0 F=5  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10888  T=2 F=0  T=5 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10888  T=2 F=0  T=5 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=5   L10889  T=2 F=0  T=5 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10889  T=0 F=2  T=0 F=5  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=5   L10907  T=0 F=2  T=0 F=0  if (RAW == '[') {
  d=5   L10918  T=2 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10918  T=2 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=5   L10919  T=2 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=5   L10922  T=0 F=2  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10936  T=0 F=2  T=0 F=5  if (RAW != '<') {
  d=5   L10950  T=0 F=2  T=2 F=3  if (RAW != 0) {
  d=5   L10959  T=2 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10959  T=2 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L10965  T=2 F=0  T=5 F=0  if ((ctxt->myDoc != NULL) &&
  d=5   L10966  T=0 F=2  T=0 F=5  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=5   L10971  T=0 F=2  T=0 F=5  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=5   L10980  T=2 F=0  T=5 F=0  if (! ctxt->wellFormed) {
--- d=4  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=4   L10077  T=0 F=2  T=2 F=3  if (xmlParseElementStart(ctxt) != 0)
--- d=4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=4   L12139  T=0 F=22  T=0 F=46  if (ctxt == NULL)
  d=4   L12141  T=7 F=0  T=0 F=18  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12141  T=7 F=15  T=18 F=28  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12143  T=0 F=15  T=0 F=46  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12145  T=0 F=15  T=0 F=46  if (ctxt->input == NULL)
  d=4   L12149  T=4 F=11  T=10 F=36  if (ctxt->instate == XML_PARSER_START)
  d=4   L12151  T=15 F=0  T=37 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12151  T=15 F=0  T=37 F=9  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12151  T=15 F=0  T=37 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=4   L12152  T=0 F=15  T=0 F=37  (chunk[size - 1] == '\r')) {
  d=4   L12159  T=15 F=0  T=41 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12159  T=15 F=0  T=41 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12159  T=15 F=0  T=41 F=9  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=4   L12160  T=15 F=0  T=41 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=4   L12160  T=15 F=0  T=41 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=4   L12170  T=4 F=11  T=10 F=31  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=4   L12170  T=4 F=0  T=10 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=4   L12171  T=4 F=0  T=10 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12171  T=0 F=4  T=4 F=6  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=4   L12174  T=0 F=0  T=4 F=0  if ((xmlStrcasestr(BAD_CAST ctxt->input->buf->encoder->name,
  d=4   L12185  T=0 F=0  T=4 F=0  if (ctxt->input->buf->rawconsumed < len)
  d=4   L12193  T=0 F=0  T=4 F=0  if ((unsigned int) size > len) {
  d=4   L12202  T=0 F=15  T=0 F=41  if (res < 0) {
  d=4   L12211  T=0 F=0  T=9 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12212  T=0 F=0  T=9 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12212  T=0 F=0  T=9 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=4   L12214  T=0 F=0  T=8 F=1  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=4   L12214  T=0 F=0  T=8 F=0  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=4   L12215  T=0 F=0  T=8 F=0  (in->raw != NULL)) {
  d=4   L12222  T=0 F=0  T=0 F=8  if (nbchars < 0) {
  d=4   L12233  T=0 F=15  T=4 F=46  if (remain != 0) {
  d=4   L12238  T=0 F=15  T=0 F=50  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L12241  T=15 F=0  T=50 F=0  if ((ctxt->input != NULL) &&
  d=4   L12242  T=0 F=15  T=0 F=50  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=4   L12243  T=0 F=15  T=0 F=50  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=4   L12248  T=4 F=0  T=0 F=28  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12248  T=4 F=11  T=28 F=22  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12251  T=0 F=11  T=4 F=46  if (remain != 0) {
  d=4   L12257  T=0 F=11  T=0 F=46  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=4   L12268  T=0 F=11  T=7 F=39  if (terminate) {
  d=4   L12274  T=0 F=0  T=7 F=0  if (ctxt->input != NULL) {
  d=4   L12275  T=0 F=0  T=0 F=7  if (ctxt->input->buf == NULL)
  d=4   L12283  T=0 F=0  T=7 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=4   L12284  T=0 F=0  T=7 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=4   L12287  T=0 F=0  T=0 F=7  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=4   L12290  T=0 F=0  T=7 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12291  T=0 F=0  T=7 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12291  T=0 F=0  T=7 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12296  T=0 F=11  T=26 F=20  if (ctxt->wellFormed == 0)
--- d=3  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=3   L9980  T=31 F=37  T=0 F=64  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9980  T=0 F=31  T=0 F=0  if ((*cur == '<') && (cur[1] == '?')) {
  d=3   L9995  T=31 F=37  T=0 F=64  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9995  T=23 F=8  T=0 F=0  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=3   L9996  T=0 F=23  T=0 F=0  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=3   L10004  T=31 F=37  T=0 F=64  else if (*cur == '<') {
  d=3   L10005  T=0 F=31  T=0 F=0  if (NXT(1) == '/') {
  d=3   L10019  T=0 F=37  T=2 F=62  else if (*cur == '&') {
--- d=3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=3   L11409  T=0 F=15  T=0 F=50  if (ctxt->input == NULL)
  d=3   L11465  T=15 F=0  T=50 F=0  if ((ctxt->input != NULL) &&
  d=3   L11466  T=0 F=15  T=0 F=50  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=3   L11470  T=57 F=0  T=286 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=3   L11471  T=4 F=0  T=0 F=224  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11471  T=4 F=53  T=224 F=62  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11474  T=0 F=53  T=0 F=286  if (ctxt->input == NULL) break;
  d=3   L11475  T=0 F=53  T=0 F=286  if (ctxt->input->buf == NULL)
  d=3   L11486  T=47 F=6  T=270 F=16  if ((ctxt->instate != XML_PARSER_START) &&
  d=3   L11487  T=0 F=47  T=252 F=18  (ctxt->input->buf->raw != NULL) &&
  d=3   L11488  T=0 F=0  T=66 F=186  (xmlBufIsEmpty(ctxt->input->buf->raw) == 0)) {
  d=3   L11500  T=0 F=53  T=13 F=273  if (avail < 1)
  d=3   L11502  T=0 F=53  T=0 F=273  switch (ctxt->instate) {
  d=3   L11503  T=0 F=53  T=0 F=273  case XML_PARSER_EOF:
  d=3   L11508  T=6 F=47  T=16 F=257  case XML_PARSER_START:
  d=3   L11509  T=2 F=4  T=6 F=10  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=3   L11516  T=0 F=2  T=0 F=6  if (avail < 4)
  d=3   L11535  T=0 F=4  T=0 F=10  if (avail < 2)
  d=3   L11539  T=0 F=4  T=0 F=10  if (cur == 0) {
  d=3   L11553  T=4 F=0  T=0 F=8  if ((cur == '<') && (next == '?')) {
  d=3   L11553  T=4 F=0  T=8 F=2  if ((cur == '<') && (next == '?')) {
  d=3   L11555  T=0 F=4  T=0 F=0  if (avail < 5) goto done;
  d=3   L11556  T=4 F=0  T=0 F=0  if ((!terminate) &&
  d=3   L11557  T=0 F=4  T=0 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11559  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11559  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11562  T=4 F=0  T=0 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=3   L11563  T=4 F=0  T=0 F=0  (ctxt->input->cur[3] == 'm') &&
  d=3   L11564  T=4 F=0  T=0 F=0  (ctxt->input->cur[4] == 'l') &&
  d=3   L11572  T=0 F=4  T=0 F=0  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=3   L11581  T=4 F=0  T=0 F=0  if ((ctxt->encoding == NULL) &&
  d=3   L11582  T=0 F=4  T=0 F=0  (ctxt->input->encoding != NULL))
  d=3   L11584  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11584  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11585  T=4 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=3   L11604  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11604  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11608  T=0 F=0  T=0 F=10  if (ctxt->version == NULL) {
  d=3   L11612  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11612  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11613  T=0 F=0  T=10 F=0  (!ctxt->disableSAX))
  d=3   L11622  T=23 F=30  T=30 F=243  case XML_PARSER_START_TAG: {
  d=3   L11639  T=23 F=0  T=22 F=8  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11648  T=12 F=0  T=8 F=6  if (ctxt->sax2)
  d=3   L11721  T=16 F=37  T=217 F=56  case XML_PARSER_CONTENT: {
  d=3   L11722  T=0 F=16  T=0 F=217  if ((avail < 2) && (ctxt->inputNr == 1))
  d=3   L11727  T=0 F=8  T=0 F=4  if ((cur == '<') && (next == '/')) {
  d=3   L11727  T=8 F=8  T=4 F=213  if ((cur == '<') && (next == '/')) {
  d=3   L11730  T=0 F=8  T=0 F=4  } else if ((cur == '<') && (next == '?')) {
  d=3   L11730  T=8 F=8  T=4 F=213  } else if ((cur == '<') && (next == '?')) {
  d=3   L11736  T=8 F=0  T=4 F=0  } else if ((cur == '<') && (next != '!')) {
  d=3   L11736  T=8 F=8  T=4 F=213  } else if ((cur == '<') && (next != '!')) {
  d=3   L11739  T=0 F=8  T=0 F=213  } else if ((cur == '<') && (next == '!') &&
  d=3   L11747  T=0 F=8  T=0 F=213  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11758  T=0 F=8  T=0 F=213  } else if ((cur == '<') && (next == '!') &&
  d=3   L11761  T=0 F=8  T=0 F=213  } else if (cur == '<') {
  d=3   L11765  T=0 F=8  T=5 F=208  } else if (cur == '&') {
  d=3   L11766  T=0 F=0  T=4 F=1  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11766  T=0 F=0  T=3 F=1  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11782  T=8 F=0  T=208 F=0  if ((ctxt->inputNr == 1) &&
  d=3   L11783  T=4 F=4  T=29 F=179  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=3   L11784  T=0 F=4  T=18 F=2  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=3   L11784  T=4 F=0  T=20 F=9  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=3   L11792  T=0 F=53  T=0 F=273  case XML_PARSER_END_TAG:
  d=3   L11813  T=0 F=53  T=0 F=273  case XML_PARSER_CDATA_SECTION: {
  d=3   L11904  T=4 F=49  T=10 F=263  case XML_PARSER_MISC:
  d=3   L11905  T=4 F=49  T=0 F=273  case XML_PARSER_PROLOG:
  d=3   L11906  T=0 F=53  T=0 F=273  case XML_PARSER_EPILOG:
  d=3   L11929  T=4 F=4  T=0 F=10  } else if ((cur == '<') && (next == '!') &&
  d=3   L11930  T=0 F=4  T=0 F=0  (ctxt->input->cur[2] == '-') &&
  d=3   L11942  T=4 F=4  T=10 F=0  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=3   L11943  T=4 F=0  T=0 F=10  (cur == '<') && (next == '!') &&
  d=3   L11943  T=4 F=0  T=10 F=0  (cur == '<') && (next == '!') &&
  d=3   L11944  T=4 F=0  T=0 F=0  (ctxt->input->cur[2] == 'D') &&
  d=3   L11945  T=4 F=0  T=0 F=0  (ctxt->input->cur[3] == 'O') &&
  d=3   L11946  T=4 F=0  T=0 F=0  (ctxt->input->cur[4] == 'C') &&
  d=3   L11947  T=4 F=0  T=0 F=0  (ctxt->input->cur[5] == 'T') &&
  d=3   L11948  T=4 F=0  T=0 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=3   L11949  T=4 F=0  T=0 F=0  (ctxt->input->cur[7] == 'P') &&
  d=3   L11950  T=4 F=0  T=0 F=0  (ctxt->input->cur[8] == 'E')) {
  d=3   L11951  T=4 F=0  T=0 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11951  T=0 F=4  T=0 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=3   L11959  T=0 F=4  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11961  T=0 F=4  T=0 F=0  if (RAW == '[') {
  d=3   L11972  T=4 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11972  T=4 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L11973  T=4 F=0  T=0 F=0  (ctxt->sax->externalSubset != NULL))
  d=3   L11985  T=0 F=4  T=0 F=10  } else if ((cur == '<') && (next == '!') &&
  d=3   L11985  T=4 F=0  T=10 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11989  T=0 F=4  T=0 F=10  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=3   L12007  T=0 F=53  T=0 F=273  case XML_PARSER_DTD: {
  d=3   L12029  T=0 F=53  T=0 F=273  case XML_PARSER_COMMENT:
  d=3   L12038  T=0 F=53  T=0 F=273  case XML_PARSER_IGNORE:
  d=3   L12047  T=0 F=53  T=0 F=273  case XML_PARSER_PI:
  d=3   L12056  T=0 F=53  T=0 F=273  case XML_PARSER_ENTITY_DECL:
  d=3   L12065  T=0 F=53  T=0 F=273  case XML_PARSER_ENTITY_VALUE:
  d=3   L12074  T=0 F=53  T=0 F=273  case XML_PARSER_ATTRIBUTE_VALUE:
  d=3   L12083  T=0 F=53  T=0 F=273  case XML_PARSER_SYSTEM_LITERAL:
  d=3   L12092  T=0 F=53  T=0 F=273  case XML_PARSER_PUBLIC_LITERAL:
--- d=2  xmlParseCharData  (/src/libxml2/parser.c:4480-4614) ---
  d=2   L4496  T=16 F=59  T=13 F=257  while (*in == 0x20) { in++; ctxt->input->col++; }
  d=2   L4497  T=14 F=45  T=5 F=252  if (*in == 0xA) {
  d=2   L4501  T=0 F=14  T=0 F=5  } while (*in == 0xA);
  d=2   L4504  T=8 F=37  T=0 F=252  if (*in == '<') {
  d=2   L4506  T=8 F=0  T=0 F=0  if (nbchar > 0) {
  d=2   L4510  T=8 F=0  T=0 F=0  if ((ctxt->sax != NULL) &&
  d=2   L4511  T=0 F=8  T=0 F=0  (ctxt->sax->ignorableWhitespace !=
  d=2   L4524  T=8 F=0  T=0 F=0  } else if ((ctxt->sax != NULL) &&
  d=2   L4525  T=8 F=0  T=0 F=0  (ctxt->sax->characters != NULL)) {
  d=2   L4540  T=24 F=37  T=10 F=252  if (*in == 0xA) {
  d=2   L4547  T=0 F=37  T=0 F=252  if (*in == ']') {
  d=2   L4558  T=33 F=4  T=10 F=242  if (nbchar > 0) {
  d=2   L4559  T=33 F=0  T=10 F=0  if ((ctxt->sax != NULL) &&
  d=2   L4560  T=0 F=33  T=8 F=2  (ctxt->sax->ignorableWhitespace !=
  d=2   L4566  T=0 F=0  T=0 F=5  if (areBlanks(ctxt, tmp, nbchar, 0)) {
  d=2   L4571  T=0 F=0  T=5 F=0  if (ctxt->sax->characters != NULL)
  d=2   L4574  T=0 F=0  T=3 F=2  if (*ctxt->space == -1)
  d=2   L4579  T=33 F=0  T=5 F=0  } else if (ctxt->sax != NULL) {
  d=2   L4580  T=33 F=0  T=5 F=0  if (ctxt->sax->characters != NULL)
  d=2   L4588  T=0 F=37  T=0 F=252  if (*in == 0xD) {
  d=2   L4598  T=22 F=15  T=0 F=252  if (*in == '<') {
  d=2   L4601  T=0 F=15  T=1 F=251  if (*in == '&') {
  d=2   L4606  T=0 F=15  T=0 F=251  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L4609  T=13 F=2  T=211 F=40  } while (((*in >= 0x20) && (*in <= 0x7F)) ||
  d=2   L4609  T=0 F=13  T=0 F=211  } while (((*in >= 0x20) && (*in <= 0x7F)) ||
  d=2   L4610  T=0 F=15  T=0 F=251  (*in == 0x09) || (*in == 0x0a));
  d=2   L4610  T=0 F=15  T=0 F=251  (*in == 0x09) || (*in == 0x0a));
--- d=1  parser.c:xmlParseCharDataComplex  (/src/libxml2/parser.c:4628-4706) ---
  d=1   L4637  T=1250 F=7  T=4680 F=2  while ((cur != '<') && /* checked */
  d=1   L4638  T=1250 F=0  T=4680 F=4  (cur != '&') &&
  d=1   L4639  T=1240 F=8  T=4430 F=245  (IS_CHAR(cur))) /* test also done in xmlCurrentChar() */ {
  d=1   L4640  T=0 F=1240  T=0 F=4430  if ((cur == ']') && (NXT(1) == ']') && (NXT(2) == '>')) {
  d=1   L4647  T=2 F=1240  T=16 F=4420  if (nbchar >= XML_PARSER_BIG_BUFFER_SIZE) {
  d=1   L4653  T=2 F=0  T=16 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) {  <-- BLOCKER
  d=1   L4653  T=0 F=2  T=16 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) {  <-- BLOCKER
  d=1   L4654  T=0 F=0  T=0 F=16  if (areBlanks(ctxt, buf, nbchar, 0)) {
  d=1   L4659  T=0 F=0  T=16 F=0  if (ctxt->sax->characters != NULL)
  d=1   L4661  T=0 F=0  T=9 F=7  if ((ctxt->sax->characters !=
  d=1   L4663  T=0 F=0  T=0 F=9  (*ctxt->space == -1))
  d=1   L4669  T=0 F=2  T=0 F=16  if (ctxt->instate != XML_PARSER_CONTENT)
  d=1   L4673  T=20 F=1220  T=58 F=4370  if (count > 50) {
  d=1   L4677  T=0 F=20  T=0 F=58  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L4681  T=13 F=2  T=114 F=137  if (nbchar != 0) {
  d=1   L4686  T=13 F=0  T=114 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) {
  d=1   L4686  T=0 F=13  T=114 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX)) {
  d=1   L4687  T=0 F=0  T=0 F=114  if (areBlanks(ctxt, buf, nbchar, 0)) {
  d=1   L4691  T=0 F=0  T=114 F=0  if (ctxt->sax->characters != NULL)
  d=1   L4693  T=0 F=0  T=61 F=53  if ((ctxt->sax->characters != ctxt->sax->ignorableWhitesp...
  d=1   L4694  T=0 F=0  T=3 F=58  (*ctxt->space == -1))
  d=1   L4699  T=13 F=2  T=235 F=16  if ((ctxt->input->cur < ctxt->input->end) && (!IS_CHAR(cu...
  d=1   L4699  T=6 F=7  T=229 F=6  if ((ctxt->input->cur < ctxt->input->end) && (!IS_CHAR(cu...
  d=1   L4703  T=4 F=2  T=178 F=51  cur ? cur : CUR);

[off-chain: 556 additional divergent branches across 55 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=b55a03ed1e7c070a, size=1056 bytes, fuzzer=naive_ctx, trial=1, discovered_at=4970s, mutation_op=TokenReplace,TokenInsert,WordAddMutator,ByteFlipMutator,BytesRandInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=3fcad568c7a0ba50, size=1067 bytes, fuzzer=naive_ctx, trial=1, discovered_at=5455s, mutation_op=BytesInsertMutator,BytesCopyMutator,DwordAddMutator,BytesSwapMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=73fe7ddec3b99f11, size=1160 bytes, fuzzer=naive, trial=1, discovered_at=28905s, mutation_op=BytesCopyMutator,CrossoverInsertMutator,TokenReplace):
  0000: 27 68 74 7e 70 3a 2f 2f 2d 2f 27 2e 2e 27 68 74   'ht~p://-/'..'ht
  0010: 5f 5f 5f 5f 5f 5f 5f 74 5f 5f 5f 74 70 3a 2f 27   _______t___tp:/'
  0020: 68 2e 2e 2e 2e 2e 2f 27 28 27 27 2e 2e 2f 2e 27   h...../'(''../.'
  0030: 68 74 7e 70 3a 2f 2f 2d 2a 2a 2a 2a 2a 2a 2a 2a   ht~p://-********
Seed 2 (id=072348b73866a766, size=623 bytes, fuzzer=naive, trial=1, discovered_at=51736s, mutation_op=BytesRandSetMutator,CrossoverInsertMutator,BytesInsertCopyMutator):
  0000: 13 13 13 61 3f 0a 09 5c 0a 0a 3c 61 3e 0a 20 22   ...a?..\..<a>. "
  0010: 22 22 22 22 20 4d 4d 4d 4d 4d 0a 20 20 22 22 22   """" MMMMM.  """
  0020: 22 22 22 22 22 22 22 22 22 22 6e 33 2e 6f 72 4d   """"""""""n3.orM
  0030: 4d 4d 4d 4d 67 2f 31 4c 0a 0a 0a ec 0a f2 c0 78   MMMMg/1L.......x
Seed 3 (id=3e42ab855898918a, size=558 bytes, fuzzer=naive, trial=1, discovered_at=55755s, mutation_op=CrossoverInsertMutator,CrossoverInsertMutator,CrossoverInsertMutator):
  0000: 9f 86 01 00 43 54 59 50 20 20 61 20 ad 2d 2d 29   ....CTYP  a .--)
  0010: 2d 2d 2d 0a 59 3f 3f 3f 5c 0a fe ff 00 3c 21 44   ---.Y???\....<!D
  0020: f5 ff ff ff ff ff ff ff 3f 3f 3f 3f 22 30 2e 10   ........????"0..
  0030: 00 00 00 00 00 00 2e 26 26 26 26 26 00 00 00 00   .......&&&&&....
Seed 4 (id=3005ab04f8172dbe, size=1413 bytes, fuzzer=naive, trial=1, discovered_at=79114s, mutation_op=CrossoverInsertMutator,ByteNegMutator,DwordAddMutator,BytesSetMutator,ByteDecMutator,BytesInsertMutator,BytesInsertCopyMutator):
  0000: 41 27 68 74 74 70 3a 2f 2f 41 20 20 20 20 78 64   A'http://A    xd
  0010: 69 6e 6b 3a 68 72 65 0b 1a 0b 0b 0b 69 6d 6b 3a   ink:hre.....imk:
  0020: 74 79 70 65 20 20 20 28 73 69 5c 0a fe ff 00 3c   type   (si\....<
  0030: 21 44 4f 4b 4b 4b 4b 4b 4b 4a 4b 4b b4 4b 6d 6c   !DOKKKKKKJKK.Kml
Seed 5 (id=758a98ab23f055b9, size=715 bytes, fuzzer=naive, trial=1, discovered_at=83992s, mutation_op=WordInterestingMutator,DwordAddMutator,ByteNegMutator,CrossoverInsertMutator,WordAddMutator):
  0000: 65 20 20 20 28 73 69 5c 0a fe ff 00 3c 21 44 4f   e   (si\....<!DO
  0010: 4b 4b 4b 4b 4b 4b 4a 4b 4b b4 4b 6d 6c 20 76 65   KKKKKKJKK.Kml ve
  0020: 72 73 06 06 06 06 06 06 72 73 69 06 06 06 06 06   rs......rsi.....
  0030: 06 06 06 06 06 06 06 06 06 06 22 3e 0a 0a 80 00   ..........">....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x2                             27(')x1 13(.)x1 9f(.)x1 41(A)x1 +1u  DIFFER
   0x0001  00(.)x2                             68(h)x1 13(.)x1 86(.)x1 27(')x1 +1u  DIFFER
   0x0002  00(.)x2                             74(t)x1 13(.)x1 01(.)x1 68(h)x1 +1u  DIFFER
   0x0003  00(.)x2                             7e(~)x1 61(a)x1 00(.)x1 74(t)x1 +1u  PARTIAL
   0x0004  31(1)x2                             70(p)x1 3f(?)x1 43(C)x1 74(t)x1 +1u  DIFFER
   0x0005  32(2)x2                             3a(:)x1 0a(.)x1 54(T)x1 70(p)x1 +1u  DIFFER
   0x0006  37(7)x2                             2f(/)x1 09(.)x1 59(Y)x1 3a(:)x1 +1u  DIFFER
   0x0007  37(7)x2                             2f(/)x2 5c(\)x2 50(P)x1             DIFFER
   0x0008  37(7)x2                             0a(.)x2 2d(-)x1 20( )x1 2f(/)x1     DIFFER
   0x0009  32(2)x2                             2f(/)x1 0a(.)x1 20( )x1 41(A)x1 +1u  DIFFER
   0x000a  2e(.)x2                             27(')x1 3c(<)x1 61(a)x1 20( )x1 +1u  DIFFER
   0x000b  78(x)x2                             20( )x2 2e(.)x1 61(a)x1 00(.)x1     DIFFER
   0x000c  6d(m)x2                             2e(.)x1 3e(>)x1 ad(.)x1 20( )x1 +1u  DIFFER
   0x000d  6c(l)x2                             27(')x1 0a(.)x1 2d(-)x1 20( )x1 +1u  DIFFER
   0x000e  5c(\)x2                             68(h)x1 20( )x1 2d(-)x1 78(x)x1 +1u  DIFFER
   0x000f  0a(.)x2                             74(t)x1 22(")x1 29())x1 64(d)x1 +1u  DIFFER
   0x0010  3c(<)x2                             5f(_)x1 22(")x1 2d(-)x1 69(i)x1 +1u  DIFFER
   0x0011  3f(?)x2                             5f(_)x1 22(")x1 2d(-)x1 6e(n)x1 +1u  DIFFER
   0x0012  78(x)x2                             5f(_)x1 22(")x1 2d(-)x1 6b(k)x1 +1u  DIFFER
   0x0013  6d(m)x2                             5f(_)x1 22(")x1 0a(.)x1 3a(:)x1 +1u  DIFFER
   0x0014  6c(l)x2                             5f(_)x1 20( )x1 59(Y)x1 68(h)x1 +1u  DIFFER
   0x0015  20( )x2                             5f(_)x1 4d(M)x1 3f(?)x1 72(r)x1 +1u  DIFFER
   0x0016  76(v)x2                             5f(_)x1 4d(M)x1 3f(?)x1 65(e)x1 +1u  DIFFER
   0x0017  65(e)x2                             74(t)x1 4d(M)x1 3f(?)x1 0b(.)x1 +1u  DIFFER
   0x0018  72(r)x2                             5f(_)x1 4d(M)x1 5c(\)x1 1a(.)x1 +1u  DIFFER
   0x0019  73(s)x2                             5f(_)x1 4d(M)x1 0a(.)x1 0b(.)x1 +1u  DIFFER
   0x001a  69(i)x2                             5f(_)x1 0a(.)x1 fe(.)x1 0b(.)x1 +1u  DIFFER
   0x001b  6f(o)x2                             74(t)x1 20( )x1 ff(.)x1 0b(.)x1 +1u  DIFFER
   0x001c  6e(n)x2                             70(p)x1 20( )x1 00(.)x1 69(i)x1 +1u  DIFFER
   0x001d  3d(=)x2                             3a(:)x1 22(")x1 3c(<)x1 6d(m)x1 +1u  DIFFER
   0x001e  22(")x2                             2f(/)x1 22(")x1 21(!)x1 6b(k)x1 +1u  PARTIAL
   0x001f  31(1)x2                             27(')x1 22(")x1 44(D)x1 3a(:)x1 +1u  DIFFER
   0x0020  2e(.)x2                             68(h)x1 22(")x1 f5(.)x1 74(t)x1 +1u  DIFFER
   0x0021  30(0)x2                             2e(.)x1 22(")x1 ff(.)x1 79(y)x1 +1u  DIFFER
   0x0022  22(")x2                             2e(.)x1 22(")x1 ff(.)x1 70(p)x1 +1u  PARTIAL
   0x0023  3f(?)x2                             2e(.)x1 22(")x1 ff(.)x1 65(e)x1 +1u  DIFFER
   0x0024  3e(>)x2                             2e(.)x1 22(")x1 ff(.)x1 20( )x1 +1u  DIFFER
   0x0025  0a(.)x2                             2e(.)x1 22(")x1 ff(.)x1 20( )x1 +1u  DIFFER
   0x0026  3c(<)x2                             2f(/)x1 22(")x1 ff(.)x1 20( )x1 +1u  DIFFER
   0x0027  21(!)x2                             27(')x1 22(")x1 ff(.)x1 28(()x1 +1u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6581.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6581,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6581 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6581 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6581 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).