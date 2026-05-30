==== BLOCKER ====
Target: libxml2
Branch ID: 6576
Location: /src/libxml2/parser.c:4610:31
Enclosing function: xmlParseCharData
Source line:              (*in == 0x09) || (*in == 0x0a));
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            8        2          0  winner (ctx_coverage vs naive_ctx)
cmplog                          10        0          0  REFERENCE
value_profile                    5        5          0  REFERENCE
value_profile_cmplog             9        1          0  REFERENCE
naive_ctx                        2        8          0  loser (ctx_coverage vs naive)
naive_ngram4                     4        6          0  REFERENCE
mopt                             6        4          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > naive_ctx  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.90h  loser=19.90h
  avg hitcount on branch: winner=62  loser=5
  prob_div=0.60  dur_div=8.00h  hit_div=57
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6576/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseCharData (/src/libxml2/parser.c:4480-4614) ---
[ ]  4478  
[ ]  4479  void
[B]  4480  xmlParseCharData(xmlParserCtxtPtr ctxt, ATTRIBUTE_UNUSED int cdata) {
[B]  4481      const xmlChar *in;
[B]  4482      int nbchar = 0;
[B]  4483      int line = ctxt->input->line;
[B]  4484      int col = ctxt->input->col;
[B]  4485      int ccol;
[ ]  4486  
[B]  4487      SHRINK;
[B]  4488      GROW;
[ ]  4489      /*
[ ]  4490       * Accelerated common case where input don't need to be
[ ]  4491       * modified before passing it to the handler.
[ ]  4492       */
[B]  4493      in = ctxt->input->cur;
[B]  4494      do {
[B]  4495  get_more_space:
[B]  4496          while (*in == 0x20) { in++; ctxt->input->col++; }
[B]  4497          if (*in == 0xA) {
[B]  4498              do {
[B]  4499                  ctxt->input->line++; ctxt->input->col = 1;
[B]  4500                  in++;
[B]  4501              } while (*in == 0xA);
[B]  4502              goto get_more_space;
[B]  4503          }
[B]  4504          if (*in == '<') {
[B]  4505              nbchar = in - ctxt->input->cur;
[B]  4506              if (nbchar > 0) {
[B]  4507                  const xmlChar *tmp = ctxt->input->cur;
[B]  4508                  ctxt->input->cur = in;
[ ]  4509  
[B]  4510                  if ((ctxt->sax != NULL) &&
[B]  4511                      (ctxt->sax->ignorableWhitespace !=
[B]  4512                       ctxt->sax->characters)) {
[L]  4513                      if (areBlanks(ctxt, tmp, nbchar, 1)) {
[L]  4514                          if (ctxt->sax->ignorableWhitespace != NULL)
[L]  4515                              ctxt->sax->ignorableWhitespace(ctxt->userData,
[L]  4516                                                     tmp, nbchar);
[L]  4517                      } else {
[L]  4518                          if (ctxt->sax->characters != NULL)
[L]  4519                              ctxt->sax->characters(ctxt->userData,
[L]  4520                                                    tmp, nbchar);
[L]  4521                          if (*ctxt->space == -1)
[L]  4522                              *ctxt->space = -2;
[L]  4523                      }
[B]  4524                  } else if ((ctxt->sax != NULL) &&
[B]  4525                             (ctxt->sax->characters != NULL)) {
[B]  4526                      ctxt->sax->characters(ctxt->userData,
[B]  4527                                            tmp, nbchar);
[B]  4528                  }
[B]  4529              }
[B]  4530              return;
[B]  4531          }
[ ]  4532  
[B]  4533  get_more:
[B]  4534          ccol = ctxt->input->col;
[B]  4535          while (test_char_data[*in]) {
[B]  4536              in++;
[B]  4537              ccol++;
[B]  4538          }
[B]  4539          ctxt->input->col = ccol;
[B]  4540          if (*in == 0xA) {
[B]  4541              do {
[B]  4542                  ctxt->input->line++; ctxt->input->col = 1;
[B]  4543                  in++;
[B]  4544              } while (*in == 0xA);
[B]  4545              goto get_more;
[B]  4546          }
[B]  4547          if (*in == ']') {
[L]  4548              if ((in[1] == ']') && (in[2] == '>')) {
[ ]  4549                  xmlFatalErr(ctxt, XML_ERR_MISPLACED_CDATA_END, NULL);
[ ]  4550                  ctxt->input->cur = in + 1;
[ ]  4551                  return;
[ ]  4552              }
[L]  4553              in++;
[L]  4554              ctxt->input->col++;
[L]  4555              goto get_more;
[L]  4556          }
[B]  4557          nbchar = in - ctxt->input->cur;
[B]  4558          if (nbchar > 0) {
[B]  4559              if ((ctxt->sax != NULL) &&
[B]  4560                  (ctxt->sax->ignorableWhitespace !=
[B]  4561                   ctxt->sax->characters) &&
[B]  4562                  (IS_BLANK_CH(*ctxt->input->cur))) {
[L]  4563                  const xmlChar *tmp = ctxt->input->cur;
[L]  4564                  ctxt->input->cur = in;
[ ]  4565  
[L]  4566                  if (areBlanks(ctxt, tmp, nbchar, 0)) {
[ ]  4567                      if (ctxt->sax->ignorableWhitespace != NULL)
[ ]  4568                          ctxt->sax->ignorableWhitespace(ctxt->userData,
[ ]  4569                                                         tmp, nbchar);
[L]  4570                  } else {
[L]  4571                      if (ctxt->sax->characters != NULL)
[L]  4572                          ctxt->sax->characters(ctxt->userData,
[L]  4573                                                tmp, nbchar);
[L]  4574                      if (*ctxt->space == -1)
[L]  4575                          *ctxt->space = -2;
[L]  4576                  }
[L]  4577                  line = ctxt->input->line;
[L]  4578                  col = ctxt->input->col;
[B]  4579              } else if (ctxt->sax != NULL) {
[B]  4580                  if (ctxt->sax->characters != NULL)
[B]  4581                      ctxt->sax->characters(ctxt->userData,
[B]  4582                                            ctxt->input->cur, nbchar);
[B]  4583                  line = ctxt->input->line;
[B]  4584                  col = ctxt->input->col;
[B]  4585              }
[B]  4586          }
[B]  4587          ctxt->input->cur = in;
[B]  4588          if (*in == 0xD) {
[W]  4589              in++;
[W]  4590              if (*in == 0xA) {
[W]  4591                  ctxt->input->cur = in;
[W]  4592                  in++;
[W]  4593                  ctxt->input->line++; ctxt->input->col = 1;
[W]  4594                  continue; /* while */
[W]  4595              }
[W]  4596              in--;
[W]  4597          }
[B]  4598          if (*in == '<') {
[B]  4599              return;
[B]  4600          }
[B]  4601          if (*in == '&') {
[B]  4602              return;
[B]  4603          }
[B]  4604          SHRINK;
[B]  4605          GROW;
[B]  4606          if (ctxt->instate == XML_PARSER_EOF)
[ ]  4607              return;
[B]  4608          in = ctxt->input->cur;
[B]  4609      } while (((*in >= 0x20) && (*in <= 0x7F)) ||
[B]  4610               (*in == 0x09) || (*in == 0x0a)); <-- BLOCKER
[B]  4611      ctxt->input->line = line;
[B]  4612      ctxt->input->col = col;
[B]  4613      xmlParseCharDataComplex(ctxt);
[B]  4614  }

--- Caller (1 hop): parser.c:xmlParseContentInternal (/src/libxml2/parser.c:9969-10033, calls xmlParseCharData at line 10027) (±10 around call site) ---
[ ] 10017  	 */
[ ] 10018  
[B] 10019  	else if (*cur == '&') {
[B] 10020  	    xmlParseReference(ctxt);
[B] 10021  	}
[ ] 10022  
[ ] 10023  	/*
[ ] 10024  	 * Last case, text. Note that References are handled directly.
[ ] 10025  	 */
[B] 10026  	else {
[B] 10027  	    xmlParseCharData(ctxt, 0); <-- CALL
[B] 10028  	}
[ ] 10029  
[B] 10030  	GROW;
[B] 10031  	SHRINK;
[B] 10032      }
[B] 10033  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseCharData at line 10027)
hop 2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseCharData at line 11788)
hop 3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 3  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 3  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 4  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 4  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 4  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 5  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 5  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 5  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 5  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 6  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 6  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 7  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 7  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1030      6580  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     384         0  parser.c:xmlSHRINK  (/src/libxml2/parser.c:2059-2066)
     254        40  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226)
      15       222  parser.c:xmlFatalErrMsgInt  (/src/libxml2/parser.c:572-586)
      72       266  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      34       192  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       4       148  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
       4       148  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
       0       113  nodePush  (/src/libxml2/parser.c:1750-1776)
       0        89  parser.c:xmlParseLookupCharData  (/src/libxml2/parser.c:11170-11184)
       0        86  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942)
      19       101  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
       6        85  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
      18        90  inputPop  (/src/libxml2/parser.c:1723-1738)
       0        68  parser.c:xmlParseLookupGt  (/src/libxml2/parser.c:11194-11221)
... (56 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=5   L7181  T=0 F=4  T=0 F=148  if (RAW != '&')
  d=5   L7187  T=0 F=4  T=0 F=148  if (NXT(1) == '#') {
  d=5   L7233  T=4 F=0  T=148 F=0  if (ent == NULL) return;
--- d=4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=4   L10816  T=0 F=2  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10816  T=0 F=2  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10829  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10829  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10831  T=0 F=2  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10834  T=2 F=0  T=10 F=0  if ((ctxt->encoding == NULL) &&
  d=4   L10835  T=2 F=0  T=10 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=4   L10846  T=2 F=0  T=7 F=3  if (enc != XML_CHAR_ENCODING_NONE) {
  d=4   L10852  T=0 F=2  T=0 F=10  if (CUR == 0) {
  d=4   L10863  T=0 F=2  T=0 F=10  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=4   L10872  T=0 F=2  T=0 F=7  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=4   L10873  T=0 F=2  T=0 F=7  (ctxt->instate == XML_PARSER_EOF)) {
  d=4   L10884  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=0 F=2  T=9 F=1  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10886  T=0 F=2  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10888  T=0 F=0  T=9 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10888  T=0 F=2  T=9 F=1  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10889  T=0 F=0  T=9 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10889  T=0 F=0  T=0 F=9  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10919  T=0 F=2  T=2 F=0  (!ctxt->disableSAX))
  d=4   L10936  T=0 F=2  T=0 F=10  if (RAW != '<') {
  d=4   L10950  T=0 F=2  T=3 F=7  if (RAW != 0) {
  d=4   L10959  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10959  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10965  T=0 F=2  T=9 F=1  if ((ctxt->myDoc != NULL) &&
  d=4   L10966  T=0 F=0  T=0 F=9  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=4   L10971  T=0 F=2  T=0 F=10  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10980  T=2 F=0  T=10 F=0  if (! ctxt->wellFormed) {
--- d=3  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=3   L10077  T=0 F=2  T=3 F=7  if (xmlParseElementStart(ctxt) != 0)
  d=3   L10081  T=0 F=2  T=0 F=7  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L10084  T=2 F=0  T=7 F=0  if (CUR == 0) {
--- d=3  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=3   L12141  T=29 F=0  T=6 F=10  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12143  T=0 F=4  T=0 F=54  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L12145  T=0 F=4  T=0 F=54  if (ctxt->input == NULL)
  d=3   L12149  T=4 F=0  T=40 F=14  if (ctxt->instate == XML_PARSER_START)
  d=3   L12151  T=4 F=0  T=35 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12151  T=4 F=0  T=35 F=19  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12151  T=4 F=0  T=35 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=3   L12152  T=2 F=2  T=0 F=35  (chunk[size - 1] == '\r')) {
  d=3   L12159  T=4 F=0  T=35 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12159  T=4 F=0  T=35 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12159  T=4 F=0  T=35 F=19  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=3   L12160  T=4 F=0  T=35 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=3   L12160  T=4 F=0  T=35 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=3   L12170  T=4 F=0  T=28 F=7  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12170  T=4 F=0  T=28 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=3   L12171  T=4 F=0  T=28 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12171  T=0 F=4  T=0 F=28  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=3   L12202  T=0 F=4  T=0 F=35  if (res < 0) {
  d=3   L12211  T=0 F=0  T=19 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=3   L12212  T=0 F=0  T=19 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=3   L12212  T=0 F=0  T=19 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=3   L12214  T=0 F=0  T=0 F=19  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=3   L12233  T=0 F=4  T=0 F=54  if (remain != 0) {
  d=3   L12238  T=0 F=4  T=2 F=52  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L12241  T=4 F=0  T=52 F=0  if ((ctxt->input != NULL) &&
  d=3   L12242  T=0 F=4  T=0 F=52  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=3   L12243  T=0 F=4  T=0 F=52  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=3   L12248  T=4 F=0  T=4 F=24  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12248  T=4 F=0  T=28 F=24  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L12251  T=0 F=0  T=0 F=48  if (remain != 0) {
  d=3   L12257  T=0 F=0  T=0 F=48  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=3   L12268  T=0 F=0  T=10 F=38  if (terminate) {
  d=3   L12274  T=0 F=0  T=10 F=0  if (ctxt->input != NULL) {
  d=3   L12275  T=0 F=0  T=0 F=10  if (ctxt->input->buf == NULL)
  d=3   L12283  T=0 F=0  T=10 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=3   L12284  T=0 F=0  T=10 F=0  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=3   L12287  T=0 F=0  T=0 F=10  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=3   L12290  T=0 F=0  T=10 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=3   L12291  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L12291  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L12296  T=0 F=0  T=23 F=25  if (ctxt->wellFormed == 0)
--- d=2  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=2   L9973  T=523 F=2  T=217 F=7  while ((RAW != 0) &&
  d=2   L9974  T=523 F=0  T=217 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L9980  T=252 F=271  T=35 F=182  if ((*cur == '<') && (cur[1] == '?')) {
  d=2   L9980  T=0 F=252  T=1 F=34  if ((*cur == '<') && (cur[1] == '?')) {
  d=2   L9995  T=252 F=271  T=34 F=182  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=2   L9995  T=12 F=240  T=5 F=29  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=2   L9996  T=0 F=12  T=0 F=5  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=2   L10004  T=252 F=271  T=34 F=182  else if (*cur == '<') {
  d=2   L10005  T=0 F=252  T=4 F=30  if (NXT(1) == '/') {
  d=2   L10006  T=0 F=0  T=0 F=4  if (ctxt->nameNr <= nameNr)
--- d=2  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=2   L11409  T=0 F=4  T=0 F=54  if (ctxt->input == NULL)
  d=2   L11465  T=4 F=0  T=54 F=0  if ((ctxt->input != NULL) &&
  d=2   L11466  T=0 F=4  T=0 F=54  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=2   L11470  T=10 F=0  T=643 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=2   L11471  T=4 F=0  T=4 F=556  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L11471  T=4 F=6  T=560 F=83  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=2   L11474  T=0 F=6  T=0 F=639  if (ctxt->input == NULL) break;
  d=2   L11475  T=0 F=6  T=0 F=639  if (ctxt->input->buf == NULL)
  d=2   L11486  T=0 F=6  T=586 F=53  if ((ctxt->instate != XML_PARSER_START) &&
  d=2   L11487  T=0 F=0  T=0 F=586  (ctxt->input->buf->raw != NULL) &&
  d=2   L11500  T=0 F=6  T=9 F=630  if (avail < 1)
  d=2   L11502  T=0 F=6  T=0 F=630  switch (ctxt->instate) {
  d=2   L11503  T=0 F=6  T=0 F=630  case XML_PARSER_EOF:
  d=2   L11508  T=6 F=0  T=53 F=577  case XML_PARSER_START:
  d=2   L11509  T=2 F=4  T=13 F=40  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=2   L11516  T=0 F=2  T=0 F=13  if (avail < 4)
  d=2   L11535  T=0 F=4  T=0 F=40  if (avail < 2)
  d=2   L11539  T=0 F=4  T=0 F=40  if (cur == 0) {
  d=2   L11553  T=4 F=0  T=34 F=6  if ((cur == '<') && (next == '?')) {
  d=2   L11553  T=4 F=0  T=40 F=0  if ((cur == '<') && (next == '?')) {
  d=2   L11555  T=0 F=4  T=0 F=34  if (avail < 5) goto done;
  d=2   L11556  T=4 F=0  T=26 F=8  if ((!terminate) &&
  d=2   L11557  T=0 F=4  T=20 F=6  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=2   L11559  T=4 F=0  T=14 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11559  T=4 F=0  T=14 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11562  T=4 F=0  T=14 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=2   L11563  T=4 F=0  T=14 F=0  (ctxt->input->cur[3] == 'm') &&
  d=2   L11564  T=4 F=0  T=14 F=0  (ctxt->input->cur[4] == 'l') &&
  d=2   L11572  T=0 F=4  T=0 F=14  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=2   L11581  T=4 F=0  T=14 F=0  if ((ctxt->encoding == NULL) &&
  d=2   L11582  T=0 F=4  T=0 F=14  (ctxt->input->encoding != NULL))
  d=2   L11584  T=4 F=0  T=14 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11584  T=4 F=0  T=14 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11585  T=0 F=4  T=12 F=2  (!ctxt->disableSAX))
  d=2   L11604  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11604  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=2   L11608  T=0 F=0  T=0 F=6  if (ctxt->version == NULL) {
  d=2   L11612  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11612  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=2   L11613  T=0 F=0  T=6 F=0  (!ctxt->disableSAX))
  d=2   L11622  T=0 F=6  T=100 F=530  case XML_PARSER_START_TAG: {
  d=2   L11629  T=0 F=0  T=0 F=100  if ((avail < 2) && (ctxt->inputNr == 1))
  d=2   L11632  T=0 F=0  T=0 F=100  if (cur != '<') {
  d=2   L11639  T=0 F=0  T=12 F=52  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11639  T=0 F=0  T=64 F=36  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11641  T=0 F=0  T=0 F=88  if (ctxt->spaceNr == 0)
  d=2   L11643  T=0 F=0  T=7 F=81  else if (*ctxt->space == -2)
  d=2   L11648  T=0 F=0  T=57 F=31  if (ctxt->sax2)
  d=2   L11655  T=0 F=0  T=0 F=88  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11657  T=0 F=0  T=0 F=88  if (name == NULL) {
  d=2   L11670  T=0 F=0  T=0 F=88  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=2   L11678  T=0 F=0  T=0 F=6  if ((RAW == '/') && (NXT(1) == '>')) {
  d=2   L11678  T=0 F=0  T=6 F=82  if ((RAW == '/') && (NXT(1) == '>')) {
  d=2   L11707  T=0 F=0  T=44 F=44  if (RAW == '>') {
  d=2   L11721  T=0 F=6  T=442 F=188  case XML_PARSER_CONTENT: {
  d=2   L11722  T=0 F=0  T=1 F=441  if ((avail < 2) && (ctxt->inputNr == 1))
  d=2   L11722  T=0 F=0  T=1 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=2   L11727  T=0 F=0  T=10 F=93  if ((cur == '<') && (next == '/')) {
  d=2   L11727  T=0 F=0  T=103 F=338  if ((cur == '<') && (next == '/')) {
  d=2   L11730  T=0 F=0  T=3 F=90  } else if ((cur == '<') && (next == '?')) {
  d=2   L11730  T=0 F=0  T=93 F=338  } else if ((cur == '<') && (next == '?')) {
  d=2   L11731  T=0 F=0  T=2 F=1  if ((!terminate) &&
  d=2   L11732  T=0 F=0  T=0 F=2  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=2   L11736  T=0 F=0  T=72 F=18  } else if ((cur == '<') && (next != '!')) {
  d=2   L11736  T=0 F=0  T=90 F=338  } else if ((cur == '<') && (next != '!')) {
  d=2   L11739  T=0 F=0  T=18 F=338  } else if ((cur == '<') && (next == '!') &&
  d=2   L11739  T=0 F=0  T=18 F=0  } else if ((cur == '<') && (next == '!') &&
  d=2   L11740  T=0 F=0  T=0 F=18  (ctxt->input->cur[2] == '-') &&
  d=2   L11747  T=0 F=0  T=18 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=2   L11747  T=0 F=0  T=18 F=338  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=2   L11748  T=0 F=0  T=0 F=18  (ctxt->input->cur[2] == '[') &&
  d=2   L11758  T=0 F=0  T=18 F=338  } else if ((cur == '<') && (next == '!') &&
  d=2   L11758  T=0 F=0  T=18 F=0  } else if ((cur == '<') && (next == '!') &&
  d=2   L11759  T=0 F=0  T=0 F=18  (avail < 9)) {
  d=2   L11761  T=0 F=0  T=18 F=338  } else if (cur == '<') {
  d=2   L11765  T=0 F=0  T=93 F=245  } else if (cur == '&') {
  d=2   L11766  T=0 F=0  T=0 F=93  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=2   L11782  T=0 F=0  T=245 F=0  if ((ctxt->inputNr == 1) &&
  d=2   L11783  T=0 F=0  T=201 F=44  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=2   L11784  T=0 F=0  T=5 F=84  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=2   L11784  T=0 F=0  T=89 F=112  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=2   L11792  T=0 F=6  T=11 F=619  case XML_PARSER_END_TAG:
  d=2   L11793  T=0 F=0  T=0 F=11  if (avail < 2)
  d=2   L11795  T=0 F=0  T=1 F=4  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=2   L11795  T=0 F=0  T=5 F=6  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=2   L11797  T=0 F=0  T=4 F=6  if (ctxt->sax2) {
  d=2   L11805  T=0 F=0  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF) {
  d=2   L11807  T=0 F=0  T=2 F=8  } else if (ctxt->nameNr == 0) {
  d=2   L11813  T=0 F=6  T=0 F=630  case XML_PARSER_CDATA_SECTION: {
  d=2   L11904  T=0 F=6  T=18 F=612  case XML_PARSER_MISC:
  d=2   L11905  T=0 F=6  T=4 F=626  case XML_PARSER_PROLOG:
  d=2   L11906  T=0 F=6  T=2 F=628  case XML_PARSER_EPILOG:
  d=2   L11908  T=0 F=0  T=0 F=24  if (ctxt->input->buf == NULL)
  d=2   L11914  T=0 F=0  T=0 F=24  if (avail < 2)
  d=2   L11918  T=0 F=0  T=22 F=2  if ((cur == '<') && (next == '?')) {
  d=2   L11918  T=0 F=0  T=0 F=22  if ((cur == '<') && (next == '?')) {
  d=2   L11929  T=0 F=0  T=4 F=18  } else if ((cur == '<') && (next == '!') &&
  d=2   L11929  T=0 F=0  T=22 F=2  } else if ((cur == '<') && (next == '!') &&
  d=2   L11930  T=0 F=0  T=0 F=4  (ctxt->input->cur[2] == '-') &&
  d=2   L11942  T=0 F=0  T=18 F=6  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=2   L11943  T=0 F=0  T=4 F=14  (cur == '<') && (next == '!') &&
  d=2   L11943  T=0 F=0  T=18 F=0  (cur == '<') && (next == '!') &&
  d=2   L11944  T=0 F=0  T=4 F=0  (ctxt->input->cur[2] == 'D') &&
  d=2   L11945  T=0 F=0  T=4 F=0  (ctxt->input->cur[3] == 'O') &&
  d=2   L11946  T=0 F=0  T=4 F=0  (ctxt->input->cur[4] == 'C') &&
  d=2   L11947  T=0 F=0  T=4 F=0  (ctxt->input->cur[5] == 'T') &&
  d=2   L11948  T=0 F=0  T=4 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=2   L11949  T=0 F=0  T=4 F=0  (ctxt->input->cur[7] == 'P') &&
  d=2   L11950  T=0 F=0  T=4 F=0  (ctxt->input->cur[8] == 'E')) {
  d=2   L11951  T=0 F=0  T=4 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11951  T=0 F=0  T=0 F=4  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=2   L11959  T=0 F=0  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L11961  T=0 F=0  T=0 F=4  if (RAW == '[') {
  d=2   L11972  T=0 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L11972  T=0 F=0  T=4 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L11973  T=0 F=0  T=4 F=0  (ctxt->sax->externalSubset != NULL))
  d=2   L11985  T=0 F=0  T=0 F=18  } else if ((cur == '<') && (next == '!') &&
  d=2   L11985  T=0 F=0  T=18 F=2  } else if ((cur == '<') && (next == '!') &&
  d=2   L11989  T=0 F=0  T=2 F=18  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=2   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=2   L12007  T=0 F=6  T=0 F=630  case XML_PARSER_DTD: {
  d=2   L12029  T=0 F=6  T=0 F=630  case XML_PARSER_COMMENT:
  d=2   L12038  T=0 F=6  T=0 F=630  case XML_PARSER_IGNORE:
  d=2   L12047  T=0 F=6  T=0 F=630  case XML_PARSER_PI:
  d=2   L12056  T=0 F=6  T=0 F=630  case XML_PARSER_ENTITY_DECL:
  d=2   L12065  T=0 F=6  T=0 F=630  case XML_PARSER_ENTITY_VALUE:
  d=2   L12074  T=0 F=6  T=0 F=630  case XML_PARSER_ATTRIBUTE_VALUE:
  d=2   L12083  T=0 F=6  T=0 F=630  case XML_PARSER_SYSTEM_LITERAL:
  d=2   L12092  T=0 F=6  T=0 F=630  case XML_PARSER_PUBLIC_LITERAL:
--- d=1  xmlParseCharData  (/src/libxml2/parser.c:4480-4614) ---
  d=1   L4501  T=25 F=209  T=1 F=58  } while (*in == 0xA);
  d=1   L4511  T=0 F=38  T=14 F=36  (ctxt->sax->ignorableWhitespace !=
  d=1   L4513  T=0 F=0  T=9 F=5  if (areBlanks(ctxt, tmp, nbchar, 1)) {
  d=1   L4514  T=0 F=0  T=9 F=0  if (ctxt->sax->ignorableWhitespace != NULL)
  d=1   L4518  T=0 F=0  T=5 F=0  if (ctxt->sax->characters != NULL)
  d=1   L4521  T=0 F=0  T=2 F=3  if (*ctxt->space == -1)
  d=1   L4544  T=5 F=50  T=60 F=69  } while (*in == 0xA);
  d=1   L4547  T=0 F=233  T=1 F=317  if (*in == ']') {
  d=1   L4548  T=0 F=0  T=0 F=1  if ((in[1] == ']') && (in[2] == '>')) {
  d=1   L4560  T=0 F=215  T=62 F=68  (ctxt->sax->ignorableWhitespace !=
  d=1   L4566  T=0 F=0  T=0 F=19  if (areBlanks(ctxt, tmp, nbchar, 0)) {
  d=1   L4571  T=0 F=0  T=19 F=0  if (ctxt->sax->characters != NULL)
  d=1   L4574  T=0 F=0  T=2 F=17  if (*ctxt->space == -1)
  d=1   L4588  T=138 F=95  T=0 F=317  if (*in == 0xD) {
  d=1   L4590  T=4 F=134  T=0 F=0  if (*in == 0xA) {
  d=1   L4610  T=4 F=208  T=0 F=253  (*in == 0x09) || (*in == 0x0a));  <-- BLOCKER

[off-chain: 796 additional divergent branches across 80 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=5832a0ea2cd8dfa1, size=1862 bytes, fuzzer=naive, trial=2, discovered_at=64414s, mutation_op=CrossoverInsertMutator,ByteFlipMutator,BytesCopyMutator,TokenInsert,WordInterestingMutator):
  0000: 9c 64 ff 64 73 2f 31 32 37 37 37 32 2e 64 74 64   .d.ds/127772.dtd
  0010: 22 3e 0a 0a 3c 61 3e 0a 20 20 3c 62 20 7f 6c 53   ">..<a>.  <b .lS
  0020: 6e 6b 3a 68 72 65 66 20 20 20 20 10 00 22 68 74   nk:href    .."ht
  0030: 74 70 3a 2f 2f 66 61 6b 65 75 72 6c 2e 6e 65 74   tp://fakeurl.net
Seed 2 (id=2c3a9685b4c37937, size=1898 bytes, fuzzer=naive, trial=2, discovered_at=78827s, mutation_op=BytesInsertCopyMutator,ByteDecMutator,ByteIncMutator,ByteAddMutator):
  0000: 66 0a 74 64 73 2b 31 0d 0d 0a 3c 0a 20 20 20 20   f.tds+1...<.    
  0010: 10 00 22 68 74 74 70 3a 2f 2f 66 61 6b 65 75 72   .."http://fakeur
  0020: 6c 2e 6e 65 74 22 3e 0a 3c 21 4d 54 54 4c 49 53   l.net">.<!MTTLIS
  0030: 54 20 62 20 78 6d 6c 6c 5c 0a 3c 3f 78 6d 6c 20   T b xmll\.<?xml 

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=05c546a2afe6b91e, size=295 bytes, fuzzer=naive_ctx, trial=1, discovered_at=1812s, mutation_op=QwordAddMutator,BytesInsertCopyMutator,BytesRandSetMutator,WordInterestingMutator,BytesCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 7e 96 16 16 16 16 16 16 16 16 16 16 16 16 16 16   ~...............
  0030: 16 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   . SYSTEM "dtds/1
Seed 2 (id=093a953251ab4478, size=479 bytes, fuzzer=naive_ctx, trial=1, discovered_at=3040s, mutation_op=CrossoverInsertMutator,ByteIncMutator,WordAddMutator,ByteNegMutator,QwordAddMutator,TokenReplace):
  0000: 05 ff ff ec 31 32 37 16 37 32 2e 78 6d 6c 5c 0a   ....127.72.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 54 59 50 45 20 61 20 53 59 53 54 45   .0"?TYPE a SYSTE
  0030: 4d 20 22 20 20 78 6c 69 6e 6b 3a 45 45 45 45 45   M "  xlink:EEEEE
Seed 3 (id=059ba862b22a654d, size=527 bytes, fuzzer=naive_ctx, trial=1, discovered_at=3983s, mutation_op=BytesRandInsertMutator,BytesDeleteMutator,TokenInsert,CrossoverInsertMutator,ByteIncMutator,ByteNegMutator,BytesInsertCopyMutator):
  0000: 37 37 37 32 2e 78 6d 6c 5c 0a 3c c1 79 6d 6c 20   7772.xml\.<.yml 
  0010: 76 65 72 73 54 54 45 4d 20 22 64 74 64 73 2f 20   versTTEM "dtds/ 
  0020: 62 20 78 ff ff 00 00 3a 78 6c 69 6f 6e 3d 22 0a   b x....:xlion=".
  0030: 0a 3c 61 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54   .<a1.0"?>.<!DOCT
Seed 4 (id=059f87b5900200ad, size=775 bytes, fuzzer=naive_ctx, trial=1, discovered_at=5830s, mutation_op=BytesDeleteMutator,BytesRandSetMutator,ByteIncMutator,BytesRandInsertMutator,ByteAddMutator):
  0000: 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72   2.xml\.<?xml ver
  0010: 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 49 45   sion="1.0"?>.<IE
  0020: 44 3e 22 22 22 22 22 1b 1b 1b 1b 1b 1b 1b 1b 1b   D>""""".........
  0030: 22 22 22 22 22 22 22 22 20 22 64 74 64 73 2f 31   """""""" "dtds/1
Seed 5 (id=05b465475ce49fed, size=247 bytes, fuzzer=naive_ctx, trial=1, discovered_at=6132s, mutation_op=TokenInsert,BytesExpandMutator,CrossoverReplaceMutator,ByteAddMutator,ByteInterestingMutator):
  0000: 0f 00 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c   ..772.xml\.<?xml
  0010: 20 76 55 43 54 59 50 45 20 2f 2f 2f 61 20 55 43    vUCTYPE ///a UC
  0020: 20 20 20 20 20 20 20 20 20 20 64 8b 64 71 30 31             d.dq01
  0030: 32 37 37 37 32 2e 64 74 64 22 3e 0a 0a 3c 61 3e   27772.dtd">..<a>


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  9c(.)x1 66(f)x1                     06(.)x1 05(.)x1 37(7)x1 32(2)x1 +6u  DIFFER
   0x0001  64(d)x1 0a(.)x1                     00(.)x2 ff(.)x1 37(7)x1 2e(.)x1 +5u  DIFFER
   0x0002  ff(.)x1 74(t)x1                     37(7)x2 20( )x2 00(.)x1 ff(.)x1 +4u  PARTIAL
   0x0003  64(d)x2                             20( )x2 00(.)x1 ec(.)x1 32(2)x1 +5u  DIFFER
   0x0004  73(s)x2                             31(1)x2 2e(.)x1 6c(l)x1 32(2)x1 +5u  DIFFER
   0x0005  2f(/)x1 2b(+)x1                     32(2)x2 78(x)x1 5c(\)x1 2e(.)x1 +5u  PARTIAL
   0x0006  31(1)x2                             37(7)x2 6d(m)x1 0a(.)x1 78(x)x1 +5u  DIFFER
   0x0007  32(2)x1 0d(.)x1                     00(.)x2 37(7)x1 16(.)x1 6c(l)x1 +5u  DIFFER
   0x0008  37(7)x1 0d(.)x1                     37(7)x2 5c(\)x1 3f(?)x1 6c(l)x1 +5u  PARTIAL
   0x0009  37(7)x1 0a(.)x1                     32(2)x2 2e(.)x2 0a(.)x1 78(x)x1 +4u  PARTIAL
   0x000a  37(7)x1 3c(<)x1                     2e(.)x3 00(.)x2 3c(<)x1 6d(m)x1 +3u  PARTIAL
   0x000b  32(2)x1 0a(.)x1                     78(x)x2 c1(.)x1 6c(l)x1 3c(<)x1 +5u  DIFFER
   0x000c  2e(.)x1 20( )x1                     6d(m)x2 20( )x2 2e(.)x2 79(y)x1 +3u  PARTIAL
   0x000d  64(d)x1 20( )x1                     6c(l)x2 6d(m)x1 76(v)x1 78(x)x1 +5u  PARTIAL
   0x000e  74(t)x1 20( )x1                     5c(\)x2 72(r)x2 6c(l)x1 65(e)x1 +4u  PARTIAL
   0x000f  64(d)x1 20( )x1                     0a(.)x2 20( )x2 6c(l)x2 72(r)x1 +3u  PARTIAL
   0x0010  22(")x1 10(.)x1                     3c(<)x2 20( )x2 76(v)x1 73(s)x1 +4u  DIFFER
   0x0011  3e(>)x1 00(.)x1                     3f(?)x2 31(1)x2 65(e)x1 69(i)x1 +4u  DIFFER
   0x0012  0a(.)x1 22(")x1                     78(x)x2 ff(.)x2 72(r)x1 6f(o)x1 +4u  DIFFER
   0x0013  0a(.)x1 68(h)x1                     6d(m)x2 73(s)x1 6e(n)x1 43(C)x1 +5u  PARTIAL
   0x0014  3c(<)x1 74(t)x1                     6c(l)x2 54(T)x2 7f(.)x2 3d(=)x1 +3u  DIFFER
   0x0015  61(a)x1 74(t)x1                     20( )x2 54(T)x1 22(")x1 59(Y)x1 +5u  DIFFER
   0x0016  3e(>)x1 70(p)x1                     76(v)x2 45(E)x1 31(1)x1 50(P)x1 +5u  DIFFER
   0x0017  0a(.)x1 3a(:)x1                     65(e)x2 4d(M)x1 2e(.)x1 45(E)x1 +5u  DIFFER
   0x0018  20( )x1 2f(/)x1                     72(r)x2 20( )x2 30(0)x1 0f(.)x1 +4u  PARTIAL
   0x0019  20( )x1 2f(/)x1                     73(s)x2 22(")x2 2f(/)x1 00(.)x1 +4u  PARTIAL
   0x001a  3c(<)x1 66(f)x1                     69(i)x2 64(d)x1 3f(?)x1 2f(/)x1 +5u  DIFFER
   0x001b  62(b)x1 61(a)x1                     6f(o)x2 74(t)x1 3e(>)x1 2f(/)x1 +5u  PARTIAL
   0x001c  20( )x1 6b(k)x1                     6e(n)x2 64(d)x1 0a(.)x1 61(a)x1 +5u  DIFFER
   0x001d  7f(.)x1 65(e)x1                     3d(=)x2 73(s)x1 3c(<)x1 20( )x1 +5u  DIFFER
   0x001e  6c(l)x1 75(u)x1                     22(")x2 2f(/)x1 49(I)x1 55(U)x1 +5u  PARTIAL
   0x001f  53(S)x1 72(r)x1                     20( )x3 31(1)x2 45(E)x1 43(C)x1 +3u  DIFFER
   0x0020  6e(n)x1 6c(l)x1                     20( )x3 7e(~)x1 2e(.)x1 62(b)x1 +4u  PARTIAL
   0x0021  6b(k)x1 2e(.)x1                     20( )x3 3e(>)x2 96(.)x1 30(0)x1 +3u  DIFFER
   0x0022  3a(:)x1 6e(n)x1                     22(")x2 20( )x2 16(.)x1 78(x)x1 +4u  DIFFER
   0x0023  68(h)x1 65(e)x1                     20( )x2 16(.)x1 3f(?)x1 ff(.)x1 +5u  DIFFER
   0x0024  72(r)x1 74(t)x1                     20( )x2 16(.)x1 54(T)x1 ff(.)x1 +5u  DIFFER
   0x0025  65(e)x1 22(")x1                     20( )x2 16(.)x1 59(Y)x1 00(.)x1 +5u  PARTIAL
   0x0026  66(f)x1 3e(>)x1                     20( )x2 16(.)x1 50(P)x1 00(.)x1 +5u  PARTIAL
   0x0027  20( )x1 0a(.)x1                     20( )x2 16(.)x1 45(E)x1 3a(:)x1 +5u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6576.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6576,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6576 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6576 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6576 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).