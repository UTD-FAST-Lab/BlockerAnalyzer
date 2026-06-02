==== BLOCKER ====
Target: libxml2
Branch ID: 9361
Location: /src/libxml2/parser.c:10185:6
Enclosing function: parser.c:xmlParseElementStart
Source line: 	if (nsNr != ctxt->nsNr)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            ?        ?          ?  REFERENCE
cmplog                           0        9          1  loser (value_profile vs value_profile_cmplog)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog); winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=9  unreached=1
  avg duration blocked: winner=9.50h  loser=15.33h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.80  dur_div=5.83h  hit_div=1
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=9.50h  loser=19.00h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.80  dur_div=9.50h  hit_div=1
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/9361/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlParseElementStart (/src/libxml2/parser.c:10106-10226) ---
[ ] 10104   */
[ ] 10105  static int
[B] 10106  xmlParseElementStart(xmlParserCtxtPtr ctxt) {
[B] 10107      const xmlChar *name;
[B] 10108      const xmlChar *prefix = NULL;
[B] 10109      const xmlChar *URI = NULL;
[B] 10110      xmlParserNodeInfo node_info;
[B] 10111      int line, tlen = 0;
[B] 10112      xmlNodePtr ret;
[B] 10113      int nsNr = ctxt->nsNr;
[ ] 10114  
[B] 10115      if (((unsigned int) ctxt->nameNr > xmlParserMaxDepth) &&
[B] 10116          ((ctxt->options & XML_PARSE_HUGE) == 0)) {
[ ] 10117  	xmlFatalErrMsgInt(ctxt, XML_ERR_INTERNAL_ERROR,
[ ] 10118  		 "Excessive depth in document: %d use XML_PARSE_HUGE option\n",
[ ] 10119  			  xmlParserMaxDepth);
[ ] 10120  	xmlHaltParser(ctxt);
[ ] 10121  	return(-1);
[ ] 10122      }
[ ] 10123  
[ ] 10124      /* Capture start position */
[B] 10125      if (ctxt->record_info) {
[ ] 10126          node_info.begin_pos = ctxt->input->consumed +
[ ] 10127                            (CUR_PTR - ctxt->input->base);
[ ] 10128  	node_info.begin_line = ctxt->input->line;
[ ] 10129      }
[ ] 10130  
[B] 10131      if (ctxt->spaceNr == 0)
[ ] 10132  	spacePush(ctxt, -1);
[B] 10133      else if (*ctxt->space == -2)
[L] 10134  	spacePush(ctxt, -1);
[B] 10135      else
[B] 10136  	spacePush(ctxt, *ctxt->space);
[ ] 10137  
[B] 10138      line = ctxt->input->line;
[B] 10139  #ifdef LIBXML_SAX1_ENABLED
[B] 10140      if (ctxt->sax2)
[B] 10141  #endif /* LIBXML_SAX1_ENABLED */
[B] 10142          name = xmlParseStartTag2(ctxt, &prefix, &URI, &tlen);
[L] 10143  #ifdef LIBXML_SAX1_ENABLED
[L] 10144      else
[L] 10145  	name = xmlParseStartTag(ctxt);
[B] 10146  #endif /* LIBXML_SAX1_ENABLED */
[B] 10147      if (ctxt->instate == XML_PARSER_EOF)
[ ] 10148  	return(-1);
[B] 10149      if (name == NULL) {
[L] 10150  	spacePop(ctxt);
[L] 10151          return(-1);
[L] 10152      }
[B] 10153      nameNsPush(ctxt, name, prefix, URI, line, ctxt->nsNr - nsNr);
[B] 10154      ret = ctxt->node;
[ ] 10155  
[B] 10156  #ifdef LIBXML_VALID_ENABLED
[ ] 10157      /*
[ ] 10158       * [ VC: Root Element Type ]
[ ] 10159       * The Name in the document type declaration must match the element
[ ] 10160       * type of the root element.
[ ] 10161       */
[B] 10162      if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
[B] 10163          ctxt->node && (ctxt->node == ctxt->myDoc->children))
[ ] 10164          ctxt->valid &= xmlValidateRoot(&ctxt->vctxt, ctxt->myDoc);
[B] 10165  #endif /* LIBXML_VALID_ENABLED */
[ ] 10166  
[ ] 10167      /*
[ ] 10168       * Check for an Empty Element.
[ ] 10169       */
[B] 10170      if ((RAW == '/') && (NXT(1) == '>')) {
[B] 10171          SKIP(2);
[B] 10172  	if (ctxt->sax2) {
[B] 10173  	    if ((ctxt->sax != NULL) && (ctxt->sax->endElementNs != NULL) &&
[B] 10174  		(!ctxt->disableSAX))
[B] 10175  		ctxt->sax->endElementNs(ctxt->userData, name, prefix, URI);
[B] 10176  #ifdef LIBXML_SAX1_ENABLED
[B] 10177  	} else {
[L] 10178  	    if ((ctxt->sax != NULL) && (ctxt->sax->endElement != NULL) &&
[L] 10179  		(!ctxt->disableSAX))
[L] 10180  		ctxt->sax->endElement(ctxt->userData, name);
[L] 10181  #endif /* LIBXML_SAX1_ENABLED */
[L] 10182  	}
[B] 10183  	namePop(ctxt);
[B] 10184  	spacePop(ctxt);
[B] 10185  	if (nsNr != ctxt->nsNr) <-- BLOCKER
[W] 10186  	    nsPop(ctxt, ctxt->nsNr - nsNr);
[B] 10187  	if ( ret != NULL && ctxt->record_info ) {
[ ] 10188  	   node_info.end_pos = ctxt->input->consumed +
[ ] 10189  			      (CUR_PTR - ctxt->input->base);
[ ] 10190  	   node_info.end_line = ctxt->input->line;
[ ] 10191  	   node_info.node = ret;
[ ] 10192  	   xmlParserAddNodeInfo(ctxt, &node_info);
[ ] 10193  	}
[B] 10194  	return(1);
[B] 10195      }
[B] 10196      if (RAW == '>') {
[B] 10197          NEXT1;
[B] 10198      } else {
[B] 10199          xmlFatalErrMsgStrIntStr(ctxt, XML_ERR_GT_REQUIRED,
[B] 10200  		     "Couldn't find end of Start Tag %s line %d\n",
[B] 10201  		                name, line, NULL);
[ ] 10202  
[ ] 10203  	/*
[ ] 10204  	 * end of parsing of this node.
[ ] 10205  	 */
[B] 10206  	nodePop(ctxt);
[B] 10207  	namePop(ctxt);
[B] 10208  	spacePop(ctxt);
[B] 10209  	if (nsNr != ctxt->nsNr)
[ ] 10210  	    nsPop(ctxt, ctxt->nsNr - nsNr);
[ ] 10211  
[ ] 10212  	/*
[ ] 10213  	 * Capture end position and add node
[ ] 10214  	 */
[B] 10215  	if ( ret != NULL && ctxt->record_info ) {
[ ] 10216  	   node_info.end_pos = ctxt->input->consumed +
[ ] 10217  			      (CUR_PTR - ctxt->input->base);
[ ] 10218  	   node_info.end_line = ctxt->input->line;
[ ] 10219  	   node_info.node = ret;
[ ] 10220  	   xmlParserAddNodeInfo(ctxt, &node_info);
[ ] 10221  	}
[B] 10222  	return(-1);
[B] 10223      }
[ ] 10224  
[B] 10225      return(0);
[B] 10226  }

--- Caller (1 hop): parser.c:xmlParseContentInternal (/src/libxml2/parser.c:9969-10033, calls parser.c:xmlParseElementStart at line 10010) (±10 around call site) ---
[ ] 10000  
[ ] 10001  	/*
[ ] 10002  	 * Fourth case :  a sub-element.
[ ] 10003  	 */
[B] 10004  	else if (*cur == '<') {
[B] 10005              if (NXT(1) == '/') {
[L] 10006                  if (ctxt->nameNr <= nameNr)
[L] 10007                      break;
[L] 10008  	        xmlParseElementEnd(ctxt);
[B] 10009              } else {
[B] 10010  	        xmlParseElementStart(ctxt); <-- CALL
[B] 10011              }
[B] 10012  	}
[ ] 10013  
[ ] 10014  	/*
[ ] 10015  	 * Fifth case : a reference. If if has not been resolved,
[ ] 10016  	 *    parsing returns it's Name, create the node
[ ] 10017  	 */
[ ] 10018  
[B] 10019  	else if (*cur == '&') {
[B] 10020  	    xmlParseReference(ctxt);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls parser.c:xmlParseElementStart at line 10010)
hop 2  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseElementStart at line 10077)
hop 3  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 3  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 4  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 4  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 4  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 4  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 5  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 5  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 5  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 6  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseReference at line 11768)
hop 6  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 6  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 6  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)
hop 7  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 8  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     415     14600  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      40      2580  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      58      1980  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      30       820  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
      15       725  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
       9       676  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       9       549  inputPop  (/src/libxml2/parser.c:1723-1738)
      15       542  nodePush  (/src/libxml2/parser.c:1750-1776)
       6       513  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
      13       503  parser.c:nameNsPush  (/src/libxml2/parser.c:1820-1860)
      39       525  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
      27       488  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
       6       394  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
       6       391  nodePop  (/src/libxml2/parser.c:1788-1802)
       5       373  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226)  <-- enclosing
... (63 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=7   L12139  T=0 F=5  T=0 F=276  if (ctxt == NULL)
  d=7   L12141  T=0 F=3  T=56 F=25  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12141  T=3 F=2  T=81 F=195  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12143  T=0 F=5  T=0 F=220  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L12145  T=0 F=5  T=0 F=220  if (ctxt->input == NULL)
  d=7   L12149  T=2 F=3  T=188 F=32  if (ctxt->instate == XML_PARSER_START)
  d=7   L12151  T=4 F=0  T=161 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=7   L12151  T=4 F=1  T=161 F=59  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=7   L12151  T=4 F=0  T=161 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=7   L12152  T=0 F=4  T=0 F=161  (chunk[size - 1] == '\r')) {
  d=7   L12159  T=4 F=0  T=161 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=7   L12159  T=4 F=0  T=161 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=7   L12159  T=4 F=1  T=161 F=59  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=7   L12160  T=4 F=0  T=161 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=7   L12160  T=4 F=0  T=161 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=7   L12170  T=2 F=2  T=146 F=15  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=7   L12170  T=2 F=0  T=146 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=7   L12171  T=2 F=0  T=146 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=7   L12171  T=0 F=2  T=0 F=146  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=7   L12202  T=0 F=4  T=0 F=161  if (res < 0) {
  d=7   L12211  T=1 F=0  T=59 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=7   L12212  T=1 F=0  T=59 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=7   L12212  T=1 F=0  T=59 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=7   L12214  T=0 F=1  T=0 F=59  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=7   L12233  T=0 F=5  T=0 F=220  if (remain != 0) {
  d=7   L12238  T=0 F=5  T=44 F=176  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L12241  T=5 F=0  T=176 F=0  if ((ctxt->input != NULL) &&
  d=7   L12242  T=0 F=5  T=0 F=176  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=7   L12243  T=0 F=5  T=0 F=176  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=7   L12248  T=0 F=5  T=40 F=59  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12248  T=5 F=0  T=99 F=77  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L12251  T=0 F=5  T=0 F=136  if (remain != 0) {
  d=7   L12257  T=0 F=5  T=0 F=136  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=7   L12268  T=1 F=4  T=30 F=106  if (terminate) {
  d=7   L12274  T=1 F=0  T=30 F=0  if (ctxt->input != NULL) {
  d=7   L12275  T=0 F=1  T=0 F=30  if (ctxt->input->buf == NULL)
  d=7   L12283  T=1 F=0  T=30 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=7   L12284  T=1 F=0  T=27 F=3  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=7   L12287  T=0 F=0  T=0 F=3  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=7   L12287  T=0 F=1  T=3 F=27  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=7   L12290  T=1 F=0  T=30 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=7   L12291  T=1 F=0  T=30 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L12291  T=1 F=0  T=30 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L12296  T=5 F=0  T=58 F=78  if (ctxt->wellFormed == 0)
--- d=6  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=6   L11409  T=0 F=5  T=0 F=220  if (ctxt->input == NULL)
  d=6   L11465  T=5 F=0  T=220 F=0  if ((ctxt->input != NULL) &&
  d=6   L11466  T=0 F=5  T=0 F=220  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=6   L11470  T=58 F=0  T=1620 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=6   L11471  T=0 F=52  T=40 F=1030  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L11471  T=52 F=6  T=1070 F=546  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L11474  T=0 F=58  T=0 F=1580  if (ctxt->input == NULL) break;
  d=6   L11475  T=0 F=58  T=0 F=1580  if (ctxt->input->buf == NULL)
  d=6   L11486  T=54 F=4  T=1300 F=281  if ((ctxt->instate != XML_PARSER_START) &&
  d=6   L11487  T=0 F=54  T=0 F=1300  (ctxt->input->buf->raw != NULL) &&
  d=6   L11500  T=1 F=57  T=27 F=1550  if (avail < 1)
  d=6   L11502  T=0 F=57  T=0 F=1550  switch (ctxt->instate) {
  d=6   L11503  T=0 F=57  T=0 F=1550  case XML_PARSER_EOF:
  d=6   L11508  T=4 F=53  T=281 F=1270  case XML_PARSER_START:
  d=6   L11509  T=2 F=2  T=93 F=188  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=6   L11516  T=0 F=2  T=0 F=93  if (avail < 4)
  d=6   L11535  T=0 F=2  T=0 F=188  if (avail < 2)
  d=6   L11539  T=0 F=2  T=0 F=188  if (cur == 0) {
  d=6   L11553  T=2 F=0  T=132 F=52  if ((cur == '<') && (next == '?')) {
  d=6   L11553  T=2 F=0  T=184 F=4  if ((cur == '<') && (next == '?')) {
  d=6   L11555  T=0 F=2  T=0 F=132  if (avail < 5) goto done;
  d=6   L11556  T=2 F=0  T=104 F=28  if ((!terminate) &&
  d=6   L11557  T=0 F=2  T=66 F=38  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=6   L11559  T=2 F=0  T=66 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11559  T=2 F=0  T=66 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11562  T=0 F=2  T=66 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=6   L11563  T=0 F=0  T=58 F=8  (ctxt->input->cur[3] == 'm') &&
  d=6   L11564  T=0 F=0  T=58 F=0  (ctxt->input->cur[4] == 'l') &&
  d=6   L11572  T=0 F=0  T=0 F=58  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=6   L11581  T=0 F=0  T=58 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L11582  T=0 F=0  T=0 F=58  (ctxt->input->encoding != NULL))
  d=6   L11584  T=0 F=0  T=58 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11584  T=0 F=0  T=58 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11585  T=0 F=0  T=44 F=14  (!ctxt->disableSAX))
  d=6   L11594  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11594  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11595  T=2 F=0  T=8 F=0  (!ctxt->disableSAX))
  d=6   L11604  T=0 F=0  T=56 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11604  T=0 F=0  T=56 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L11608  T=0 F=0  T=0 F=56  if (ctxt->version == NULL) {
  d=6   L11612  T=0 F=0  T=56 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11612  T=0 F=0  T=56 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=6   L11613  T=0 F=0  T=56 F=0  (!ctxt->disableSAX))
  d=6   L11622  T=11 F=46  T=360 F=1190  case XML_PARSER_START_TAG: {
  d=6   L11629  T=0 F=11  T=0 F=360  if ((avail < 2) && (ctxt->inputNr == 1))
  d=6   L11632  T=0 F=11  T=0 F=360  if (cur != '<') {
  d=6   L11639  T=1 F=10  T=8 F=202  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11639  T=11 F=0  T=210 F=150  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11641  T=0 F=10  T=0 F=352  if (ctxt->spaceNr == 0)
  d=6   L11643  T=0 F=10  T=68 F=284  else if (*ctxt->space == -2)
  d=6   L11648  T=10 F=0  T=160 F=192  if (ctxt->sax2)
  d=6   L11655  T=0 F=10  T=0 F=352  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11657  T=0 F=10  T=4 F=348  if (name == NULL) {
  d=6   L11660  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11660  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11670  T=0 F=10  T=0 F=348  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=6   L11678  T=2 F=2  T=152 F=26  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L11678  T=4 F=6  T=178 F=170  if ((RAW == '/') && (NXT(1) == '>')) {
  d=6   L11681  T=2 F=0  T=74 F=78  if (ctxt->sax2) {
  d=6   L11682  T=2 F=0  T=74 F=0  if ((ctxt->sax != NULL) &&
  d=6   L11683  T=2 F=0  T=74 F=0  (ctxt->sax->endElementNs != NULL) &&
  d=6   L11684  T=2 F=0  T=64 F=10  (!ctxt->disableSAX))
  d=6   L11687  T=2 F=0  T=0 F=74  if (ctxt->nsNr - nsNr > 0)
  d=6   L11691  T=0 F=0  T=78 F=0  if ((ctxt->sax != NULL) &&
  d=6   L11692  T=0 F=0  T=78 F=0  (ctxt->sax->endElement != NULL) &&
  d=6   L11693  T=0 F=0  T=70 F=8  (!ctxt->disableSAX))
  d=6   L11697  T=0 F=2  T=0 F=152  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11700  T=0 F=2  T=48 F=104  if (ctxt->nameNr == 0) {
  d=6   L11707  T=6 F=2  T=124 F=72  if (RAW == '>') {
  d=6   L11721  T=36 F=21  T=704 F=851  case XML_PARSER_CONTENT: {
  d=6   L11722  T=0 F=36  T=7 F=697  if ((avail < 2) && (ctxt->inputNr == 1))
  d=6   L11722  T=0 F=0  T=7 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=6   L11727  T=0 F=8  T=26 F=250  if ((cur == '<') && (next == '/')) {
  d=6   L11727  T=8 F=28  T=276 F=421  if ((cur == '<') && (next == '/')) {
  d=6   L11730  T=0 F=8  T=0 F=250  } else if ((cur == '<') && (next == '?')) {
  d=6   L11730  T=8 F=28  T=250 F=421  } else if ((cur == '<') && (next == '?')) {
  d=6   L11736  T=8 F=0  T=248 F=2  } else if ((cur == '<') && (next != '!')) {
  d=6   L11736  T=8 F=28  T=250 F=421  } else if ((cur == '<') && (next != '!')) {
  d=6   L11739  T=0 F=28  T=2 F=421  } else if ((cur == '<') && (next == '!') &&
  d=6   L11739  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (next == '!') &&
  d=6   L11740  T=0 F=0  T=0 F=2  (ctxt->input->cur[2] == '-') &&
  d=6   L11747  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=6   L11747  T=0 F=28  T=2 F=421  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=6   L11748  T=0 F=0  T=0 F=2  (ctxt->input->cur[2] == '[') &&
  d=6   L11758  T=0 F=28  T=2 F=421  } else if ((cur == '<') && (next == '!') &&
  d=6   L11758  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (next == '!') &&
  d=6   L11759  T=0 F=0  T=0 F=2  (avail < 9)) {
  d=6   L11761  T=0 F=28  T=2 F=421  } else if (cur == '<') {
  d=6   L11765  T=4 F=24  T=3 F=418  } else if (cur == '&') {
  d=6   L11782  T=24 F=0  T=418 F=0  if ((ctxt->inputNr == 1) &&
  d=6   L11783  T=24 F=0  T=395 F=23  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=6   L11784  T=1 F=12  T=22 F=151  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=6   L11784  T=13 F=11  T=173 F=222  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=6   L11792  T=0 F=57  T=26 F=1520  case XML_PARSER_END_TAG:
  d=6   L11793  T=0 F=0  T=0 F=26  if (avail < 2)
  d=6   L11795  T=0 F=0  T=0 F=20  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=6   L11795  T=0 F=0  T=20 F=6  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=6   L11797  T=0 F=0  T=14 F=12  if (ctxt->sax2) {
  d=6   L11805  T=0 F=0  T=0 F=26  if (ctxt->instate == XML_PARSER_EOF) {
  d=6   L11807  T=0 F=0  T=14 F=12  } else if (ctxt->nameNr == 0) {
  d=6   L11813  T=0 F=57  T=0 F=1550  case XML_PARSER_CDATA_SECTION: {
  d=6   L11904  T=4 F=53  T=116 F=1430  case XML_PARSER_MISC:
  d=6   L11905  T=2 F=55  T=24 F=1530  case XML_PARSER_PROLOG:
  d=6   L11906  T=0 F=57  T=44 F=1510  case XML_PARSER_EPILOG:
  d=6   L11908  T=0 F=6  T=0 F=184  if (ctxt->input->buf == NULL)
  d=6   L11914  T=0 F=6  T=4 F=180  if (avail < 2)
  d=6   L11918  T=6 F=0  T=142 F=38  if ((cur == '<') && (next == '?')) {
  d=6   L11918  T=2 F=4  T=10 F=132  if ((cur == '<') && (next == '?')) {
  d=6   L11919  T=2 F=0  T=10 F=0  if ((!terminate) &&
  d=6   L11920  T=0 F=2  T=0 F=10  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=6   L11927  T=0 F=2  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11929  T=2 F=2  T=26 F=106  } else if ((cur == '<') && (next == '!') &&
  d=6   L11929  T=4 F=0  T=132 F=38  } else if ((cur == '<') && (next == '!') &&
  d=6   L11930  T=0 F=2  T=0 F=26  (ctxt->input->cur[2] == '-') &&
  d=6   L11942  T=2 F=2  T=106 F=64  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=6   L11943  T=2 F=0  T=26 F=80  (cur == '<') && (next == '!') &&
  d=6   L11943  T=2 F=0  T=106 F=0  (cur == '<') && (next == '!') &&
  d=6   L11944  T=2 F=0  T=26 F=0  (ctxt->input->cur[2] == 'D') &&
  d=6   L11945  T=2 F=0  T=26 F=0  (ctxt->input->cur[3] == 'O') &&
  d=6   L11946  T=2 F=0  T=26 F=0  (ctxt->input->cur[4] == 'C') &&
  d=6   L11947  T=2 F=0  T=26 F=0  (ctxt->input->cur[5] == 'T') &&
  d=6   L11948  T=2 F=0  T=26 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=6   L11949  T=2 F=0  T=26 F=0  (ctxt->input->cur[7] == 'P') &&
  d=6   L11950  T=2 F=0  T=26 F=0  (ctxt->input->cur[8] == 'E')) {
  d=6   L11951  T=2 F=0  T=26 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11951  T=0 F=2  T=0 F=26  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=6   L11959  T=0 F=2  T=0 F=26  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L11961  T=0 F=2  T=0 F=26  if (RAW == '[') {
  d=6   L11972  T=2 F=0  T=26 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=6   L11972  T=2 F=0  T=24 F=2  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=6   L11973  T=2 F=0  T=24 F=0  (ctxt->sax->externalSubset != NULL))
  d=6   L11985  T=0 F=2  T=0 F=106  } else if ((cur == '<') && (next == '!') &&
  d=6   L11985  T=2 F=0  T=106 F=38  } else if ((cur == '<') && (next == '!') &&
  d=6   L11989  T=0 F=2  T=40 F=104  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=6   L11996  T=0 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L11996  T=0 F=0  T=40 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12007  T=0 F=57  T=0 F=1550  case XML_PARSER_DTD: {
  d=6   L12029  T=0 F=57  T=0 F=1550  case XML_PARSER_COMMENT:
  d=6   L12038  T=0 F=57  T=0 F=1550  case XML_PARSER_IGNORE:
  d=6   L12047  T=0 F=57  T=0 F=1550  case XML_PARSER_PI:
  d=6   L12056  T=0 F=57  T=0 F=1550  case XML_PARSER_ENTITY_DECL:
  d=6   L12065  T=0 F=57  T=0 F=1550  case XML_PARSER_ENTITY_VALUE:
  d=6   L12074  T=0 F=57  T=0 F=1550  case XML_PARSER_ATTRIBUTE_VALUE:
  d=6   L12083  T=0 F=57  T=0 F=1550  case XML_PARSER_SYSTEM_LITERAL:
  d=6   L12092  T=0 F=57  T=0 F=1550  case XML_PARSER_PUBLIC_LITERAL:
--- d=3  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=3   L10816  T=0 F=1  T=0 F=61  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=3   L10816  T=0 F=1  T=0 F=61  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=3   L10829  T=1 F=0  T=61 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L10829  T=1 F=0  T=61 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L10831  T=0 F=1  T=0 F=61  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L10834  T=1 F=0  T=61 F=0  if ((ctxt->encoding == NULL) &&
  d=3   L10835  T=1 F=0  T=61 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=3   L10846  T=0 F=1  T=29 F=32  if (enc != XML_CHAR_ENCODING_NONE) {
  d=3   L10852  T=0 F=1  T=0 F=61  if (CUR == 0) {
  d=3   L10863  T=0 F=1  T=9 F=52  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=3   L10872  T=0 F=0  T=0 F=29  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=3   L10873  T=0 F=0  T=0 F=29  (ctxt->instate == XML_PARSER_EOF)) {
  d=3   L10884  T=1 F=0  T=61 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=3   L10884  T=1 F=0  T=54 F=7  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=3   L10884  T=1 F=0  T=61 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=3   L10886  T=0 F=1  T=0 F=61  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L10888  T=1 F=0  T=54 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=3   L10888  T=1 F=0  T=54 F=7  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=3   L10889  T=1 F=0  T=54 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=3   L10889  T=0 F=1  T=0 F=54  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=3   L10907  T=0 F=1  T=0 F=18  if (RAW == '[') {
  d=3   L10918  T=1 F=0  T=18 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=3   L10918  T=1 F=0  T=18 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=3   L10919  T=1 F=0  T=12 F=6  (!ctxt->disableSAX))
  d=3   L10922  T=0 F=1  T=0 F=18  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L10936  T=0 F=1  T=0 F=61  if (RAW != '<') {
  d=3   L10950  T=0 F=1  T=31 F=30  if (RAW != 0) {
  d=3   L10959  T=1 F=0  T=61 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L10959  T=1 F=0  T=61 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L10965  T=1 F=0  T=54 F=7  if ((ctxt->myDoc != NULL) &&
  d=3   L10966  T=0 F=1  T=0 F=54  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=3   L10971  T=0 F=1  T=2 F=59  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=3   L10971  T=0 F=0  T=2 F=0  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=3   L10973  T=0 F=0  T=2 F=0  if (ctxt->valid)
  d=3   L10975  T=0 F=0  T=2 F=0  if (ctxt->nsWellFormed)
  d=3   L10977  T=0 F=0  T=1 F=1  if (ctxt->options & XML_PARSE_OLD10)
  d=3   L10980  T=1 F=0  T=59 F=2  if (! ctxt->wellFormed) {
--- d=2  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=2   L9973  T=12 F=1  T=761 F=26  while ((RAW != 0) &&
  d=2   L9974  T=12 F=0  T=761 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L9980  T=4 F=8  T=334 F=427  if ((*cur == '<') && (cur[1] == '?')) {
  d=2   L9980  T=0 F=4  T=2 F=332  if ((*cur == '<') && (cur[1] == '?')) {
  d=2   L9995  T=4 F=8  T=332 F=427  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=2   L9995  T=0 F=4  T=8 F=324  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=2   L9996  T=0 F=0  T=0 F=8  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=2   L10004  T=4 F=8  T=332 F=427  else if (*cur == '<') {
  d=2   L10005  T=0 F=4  T=20 F=312  if (NXT(1) == '/') {
  d=2   L10006  T=0 F=0  T=11 F=9  if (ctxt->nameNr <= nameNr)
  d=2   L10019  T=1 F=7  T=3 F=424  else if (*cur == '&') {
--- d=2  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=2   L10077  T=0 F=1  T=24 F=37  if (xmlParseElementStart(ctxt) != 0)
  d=2   L10081  T=0 F=1  T=0 F=37  if (ctxt->instate == XML_PARSER_EOF)
  d=2   L10084  T=1 F=0  T=26 F=11  if (CUR == 0) {
--- d=1  parser.c:xmlParseElementStart  (/src/libxml2/parser.c:10106-10226) ---
  d=1   L10115  T=0 F=5  T=0 F=373  if (((unsigned int) ctxt->nameNr > xmlParserMaxDepth) &&
  d=1   L10125  T=0 F=5  T=0 F=373  if (ctxt->record_info) {
  d=1   L10131  T=0 F=5  T=0 F=373  if (ctxt->spaceNr == 0)
  d=1   L10133  T=0 F=5  T=62 F=311  else if (*ctxt->space == -2)
  d=1   L10140  T=5 F=0  T=201 F=172  if (ctxt->sax2)
  d=1   L10147  T=0 F=5  T=0 F=373  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L10149  T=0 F=5  T=66 F=307  if (name == NULL) {
  d=1   L10162  T=0 F=0  T=0 F=12  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=1   L10162  T=0 F=5  T=12 F=295  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=1   L10170  T=1 F=1  T=94 F=21  if ((RAW == '/') && (NXT(1) == '>')) {
  d=1   L10170  T=2 F=3  T=115 F=192  if ((RAW == '/') && (NXT(1) == '>')) {
  d=1   L10172  T=1 F=0  T=50 F=44  if (ctxt->sax2) {
  d=1   L10173  T=1 F=0  T=50 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->endElementNs != NU...
  d=1   L10173  T=1 F=0  T=50 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->endElementNs != NU...
  d=1   L10174  T=1 F=0  T=33 F=17  (!ctxt->disableSAX))
  d=1   L10178  T=0 F=0  T=44 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->endElement != NULL...
  d=1   L10178  T=0 F=0  T=44 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->endElement != NULL...
  d=1   L10179  T=0 F=0  T=35 F=9  (!ctxt->disableSAX))
  d=1   L10185  T=1 F=0  T=0 F=94  if (nsNr != ctxt->nsNr)  <-- BLOCKER
  d=1   L10187  T=1 F=0  T=69 F=25  if ( ret != NULL && ctxt->record_info ) {
  d=1   L10187  T=0 F=1  T=0 F=69  if ( ret != NULL && ctxt->record_info ) {
  d=1   L10196  T=3 F=1  T=134 F=79  if (RAW == '>') {
  d=1   L10209  T=0 F=1  T=0 F=79  if (nsNr != ctxt->nsNr)
  d=1   L10215  T=1 F=0  T=53 F=26  if ( ret != NULL && ctxt->record_info ) {
  d=1   L10215  T=0 F=1  T=0 F=53  if ( ret != NULL && ctxt->record_info ) {

[off-chain: 817 additional divergent branches across 72 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=f97f950fbd784430, size=398 bytes, fuzzer=value_profile_cmplog, trial=4, discovered_at=42018s, mutation_op=BytesSetMutator,ByteIncMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 73 69 6f 6e 00 22 31 2e 30 22 3f 3e 0a 3c 21 06   sion."1.0"?>.<!.
  0010: f7 ff ff ff 00 00 00 31 32 37 37 37 32 2e 78 6d   .......127772.xm
  0020: 6c 5c 0a 3c 3f 61 6d 6c ff 76 65 72 73 69 6f 6e   l\.<?aml.version
  0030: 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59   ="1.0"?>.<!DOCTY

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=44136f62ea3c33f6, size=272 bytes, fuzzer=cmplog, trial=3, discovered_at=19s, mutation_op=BytesExpandMutator,CrossoverReplaceMutator,BytesSetMutator,BytesRandInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 0a 76 65 72 73 69 6f 6e 3d 22 39   <?xml.version="9
  0020: 2e 30 22 3f 0a 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?..<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=8aa99f549dc656d0, size=319 bytes, fuzzer=cmplog, trial=2, discovered_at=224s, mutation_op=ByteFlipMutator,ByteNegMutator,BytesInsertCopyMutator,WordAddMutator,BitFlipMutator,TokenInsert):
  0000: 06 00 00 00 31 32 37 61 61 61 61 61 61 61 61 61   ....127aaaaaaaaa
  0010: 61 61 61 61 61 61 61 37 37 32 2e 78 3a 6c 5c 0a   aaaaaaa772.x:l\.
  0020: 3c 4b 78 6d 6c 20 76 65 72 2e 64 74 64 2f 3e 0a   <Kxml ver.dtd/>.
  0030: 0a 3c 61 3e 3c 5c 20 3c 62 20 78 6c 69 6e 6b 3a   .<a><\ <b xlink:
Seed 3 (id=30f0023ef4146b96, size=272 bytes, fuzzer=cmplog, trial=3, discovered_at=982s, mutation_op=ByteInterestingMutator,ByteDecMutator,ByteAddMutator,BytesDeleteMutator,CrossoverInsertMutator):
  0000: 20 20 20 23 46 49 58 45 44 20 27 68 74 74 70 3a      #FIXED 'http:
  0010: 2f 2f 77 77 77 2e 77 33 2e 6f 72 67 2f 31 39 fe   //www.w3.org/19.
  0020: ff ff ff 39 39 2f 78 6c 69 6e 6b 27 0a 2d 20 20   ...99/xlink'.-  
  0030: 20 20 20 54 59 50 45 6c 69 6e 6b 27 0a 2d 20 20      TYPElink'.-  
Seed 4 (id=0924f1eaa832c979, size=257 bytes, fuzzer=cmplog, trial=3, discovered_at=1511s, mutation_op=BytesInsertMutator,BitFlipMutator,BytesSetMutator,WordAddMutator):
  0000: c1 3d 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53   .=.<!DOCTYPE a S
  0010: 59 53 54 45 4d 20 26 64 74 64 73 2f 31 32 37 37   YSTEM &dtds/1277
  0020: 37 32 2e 64 74 64 22 3e 0a 0a 3c 61 3e 0a 20 20   72.dtd">..<a>.  
  0030: 3c 62 3a 78 6c 69 6e 6b 3a 68 72 65 66 3d 22 68   <b:xlink:href="h
Seed 5 (id=03b409bc40ca9428, size=377 bytes, fuzzer=cmplog, trial=3, discovered_at=1529s, mutation_op=BytesInsertCopyMutator,WordInterestingMutator,ByteFlipMutator,WordInterestingMutator,CrossoverReplaceMutator):
  0000: 06 ff 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 20 31   <?xml version= 1
  0020: 2e 0d 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .."?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  73(s)x1                             20( )x7 06(.)x5 37(7)x4 2e(.)x3 +31u  DIFFER
   0x0001  69(i)x1                             20( )x5 2f(/)x5 44(D)x4 00(.)x3 +30u  PARTIAL
   0x0002  6f(o)x1                             20( )x10 00(.)x5 69(i)x3 68(h)x3 +29u  DIFFER
   0x0003  6e(n)x1                             00(.)x6 20( )x6 2f(/)x5 74(t)x4 +29u  PARTIAL
   0x0004  00(.)x1                             74(t)x6 2f(/)x6 31(1)x5 6e(n)x3 +28u  PARTIAL
   0x0005  22(")x1                             32(2)x6 6c(l)x4 74(t)x4 70(p)x4 +28u  DIFFER
   0x0006  31(1)x1                             37(7)x5 3a(:)x5 77(w)x4 2f(/)x4 +32u  PARTIAL
   0x0007  2e(.)x1                             2f(/)x8 37(7)x4 45(E)x3 70(p)x3 +33u  DIFFER
   0x0008  30(0)x1                             37(7)x7 0a(.)x4 3a(:)x4 2f(/)x4 +32u  DIFFER
   0x0009  22(")x1                             2f(/)x7 32(2)x5 61(a)x4 20( )x3 +28u  PARTIAL
   0x000a  3f(?)x1                             2f(/)x6 2e(.)x5 78(x)x4 20( )x3 +32u  PARTIAL
   0x000b  3e(>)x1                             78(x)x9 77(w)x3 2e(.)x3 2f(/)x3 +33u  PARTIAL
   0x000c  0a(.)x1                             6d(m)x8 20( )x5 6c(l)x5 77(w)x5 +27u  PARTIAL
   0x000d  3c(<)x1                             6c(l)x9 20( )x4 5c(\)x4 77(w)x3 +28u  PARTIAL
   0x000e  21(!)x1                             5c(\)x6 20( )x6 2f(/)x4 2e(.)x4 +28u  DIFFER
   0x000f  06(.)x1                             0a(.)x6 2f(/)x4 65(e)x3 3c(<)x3 +31u  DIFFER
   0x0010  f7(.)x1                             3c(<)x6 72(r)x5 20( )x5 68(h)x4 +29u  DIFFER
   0x0011  ff(.)x1                             3f(?)x5 2f(/)x5 0a(.)x5 20( )x5 +22u  PARTIAL
   0x0012  ff(.)x1                             78(x)x6 69(i)x6 20( )x6 2f(/)x6 +26u  PARTIAL
   0x0013  ff(.)x1                             20( )x8 6d(m)x6 69(i)x4 3e(>)x4 +27u  PARTIAL
   0x0014  00(.)x1                             20( )x10 6c(l)x6 0a(.)x3 3c(<)x3 +28u  DIFFER
   0x0015  00(.)x1                             20( )x10 0a(.)x4 61(a)x3 3c(<)x3 +29u  DIFFER
   0x0016  00(.)x1                             20( )x6 76(v)x5 2f(/)x4 69(i)x3 +29u  DIFFER
   0x0017  31(1)x1                             65(e)x8 20( )x7 2f(/)x5 69(i)x4 +22u  PARTIAL
   0x0018  32(2)x1                             72(r)x6 2e(.)x4 0a(.)x4 20( )x4 +27u  PARTIAL
   0x0019  37(7)x1                             20( )x8 73(s)x6 2f(/)x5 69(i)x4 +28u  PARTIAL
   0x001a  37(7)x1                             69(i)x8 20( )x5 3c(<)x5 3e(>)x4 +24u  PARTIAL
   0x001b  37(7)x1                             20( )x7 6f(o)x6 2f(/)x6 22(")x4 +29u  PARTIAL
   0x001c  32(2)x1                             20( )x7 6e(n)x6 2f(/)x5 69(i)x4 +27u  DIFFER
   0x001d  2e(.)x1                             3d(=)x6 0a(.)x6 3e(>)x5 3c(<)x4 +25u  DIFFER
   0x001e  78(x)x1                             20( )x6 22(")x5 74(t)x4 2f(/)x4 +28u  DIFFER
   0x001f  6d(m)x1                             2f(/)x5 31(1)x4 3c(<)x4 74(t)x4 +32u  DIFFER
   0x0020  6c(l)x1                             2e(.)x5 20( )x4 2f(/)x4 ff(.)x3 +32u  DIFFER
   0x0021  5c(\)x1                             20( )x6 30(0)x4 3e(>)x4 64(d)x3 +33u  PARTIAL
   0x0022  0a(.)x1                             22(")x6 2f(/)x6 78(x)x3 20( )x3 +28u  PARTIAL
   0x0023  3c(<)x1                             20( )x6 2f(/)x5 3f(?)x4 27(')x3 +30u  DIFFER
   0x0024  3f(?)x1                             3e(>)x5 27(')x5 0a(.)x3 74(t)x3 +32u  DIFFER
   0x0025  61(a)x1                             0a(.)x10 2f(/)x4 20( )x3 59(Y)x3 +28u  PARTIAL
   0x0026  6d(m)x1                             3c(<)x8 22(")x4 2f(/)x4 0a(.)x3 +27u  PARTIAL
   0x0027  6c(l)x1                             21(!)x7 2e(.)x4 74(t)x4 31(1)x3 +29u  PARTIAL
   ... (24 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_9361.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9361,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9361 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9361 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9361 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).