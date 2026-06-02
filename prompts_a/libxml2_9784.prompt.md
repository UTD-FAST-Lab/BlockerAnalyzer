==== BLOCKER ====
Target: libxml2
Branch ID: 9784
Location: /src/libxml2/valid.c:3497:2
Enclosing function: xmlIsMixedElement
Source line: 	case XML_ELEMENT_TYPE_UNDEFINED:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           0       10          0  loser (grimoire_structural vs grimoire)
value_profile                    0       10          0  REFERENCE
value_profile_cmplog             2        8          0  REFERENCE
naive_ctx                        4        6          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=11.90h  loser=20.20h
  avg hitcount on branch: winner=62  loser=0
  prob_div=0.80  dur_div=8.30h  hit_div=62
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/9784/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlIsMixedElement (/src/libxml2/valid.c:3487-3511) ---
[ ]  3485  
[ ]  3486  int
[B]  3487  xmlIsMixedElement(xmlDocPtr doc, const xmlChar *name) {
[B]  3488      xmlElementPtr elemDecl;
[ ]  3489  
[B]  3490      if ((doc == NULL) || (doc->intSubset == NULL)) return(-1);
[ ]  3491  
[B]  3492      elemDecl = xmlGetDtdElementDesc(doc->intSubset, name);
[B]  3493      if ((elemDecl == NULL) && (doc->extSubset != NULL))
[B]  3494  	elemDecl = xmlGetDtdElementDesc(doc->extSubset, name);
[B]  3495      if (elemDecl == NULL) return(-1);
[B]  3496      switch (elemDecl->etype) {
[W]  3497  	case XML_ELEMENT_TYPE_UNDEFINED: <-- BLOCKER
[W]  3498  	    return(-1);
[L]  3499  	case XML_ELEMENT_TYPE_ELEMENT:
[L]  3500  	    return(0);
[ ]  3501          case XML_ELEMENT_TYPE_EMPTY:
[ ]  3502  	    /*
[ ]  3503  	     * return 1 for EMPTY since we want VC error to pop up
[ ]  3504  	     * on <empty>     </empty> for example
[ ]  3505  	     */
[ ]  3506  	case XML_ELEMENT_TYPE_ANY:
[ ]  3507  	case XML_ELEMENT_TYPE_MIXED:
[ ]  3508  	    return(1);
[B]  3509      }
[ ]  3510      return(1);
[B]  3511  }

--- Caller (1 hop): parser.c:areBlanks (/src/libxml2/parser.c:2889-2942, calls xmlIsMixedElement at line 2920) (±10 around call site) ---
[B]  2910      if (blank_chars == 0) {
[B]  2911  	for (i = 0;i < len;i++)
[B]  2912  	    if (!(IS_BLANK_CH(str[i]))) return(0);
[B]  2913      }
[ ]  2914  
[ ]  2915      /*
[ ]  2916       * Look if the element is mixed content in the DTD if available
[ ]  2917       */
[B]  2918      if (ctxt->node == NULL) return(0);
[B]  2919      if (ctxt->myDoc != NULL) {
[B]  2920  	ret = xmlIsMixedElement(ctxt->myDoc, ctxt->node->name); <-- CALL
[B]  2921          if (ret == 0) return(1);
[W]  2922          if (ret == 1) return(0);
[W]  2923      }
[ ]  2924  
[ ]  2925      /*
[ ]  2926       * Otherwise, heuristic :-\
[ ]  2927       */
[W]  2928      if ((RAW != '<') && (RAW != 0xD)) return(0);
[W]  2929      if ((ctxt->node->children == NULL) &&
[W]  2930  	(RAW == '<') && (NXT(1) == '/')) return(0);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942, calls xmlIsMixedElement at line 2920)
hop 3  xmlParseCharData  (/src/libxml2/parser.c:4480-4614, calls parser.c:areBlanks at line 4513)
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
     260      1030  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
       0       186  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
       0       112  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      18        75  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
      18        72  inputPop  (/src/libxml2/parser.c:1723-1738)
       0        53  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
       6        55  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
       9        57  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      57        12  xmlGetDtdQAttrDesc  (/src/libxml2/valid.c:3410-3418)
       0        43  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
       6        48  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
       6        48  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)
       6        48  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883)
       6        46  nodePop  (/src/libxml2/parser.c:1788-1802)
      57        18  xmlValidCtxtNormalizeAttributeValue  (/src/libxml2/valid.c:4061-4111)
... (97 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=7   L7181  T=0 F=0  T=0 F=2  if (RAW != '&')
  d=7   L7187  T=0 F=0  T=0 F=2  if (NXT(1) == '#') {
  d=7   L7233  T=0 F=0  T=2 F=0  if (ent == NULL) return;
--- d=6  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=6   L10816  T=0 F=2  T=0 F=8  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=6   L10816  T=0 F=2  T=0 F=8  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=6   L10829  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L10829  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L10831  T=0 F=2  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10834  T=2 F=0  T=8 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L10835  T=2 F=0  T=8 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=6   L10846  T=0 F=2  T=8 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=6   L10852  T=0 F=2  T=0 F=8  if (CUR == 0) {
  d=6   L10863  T=0 F=2  T=0 F=8  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=6   L10872  T=0 F=0  T=0 F=8  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=6   L10873  T=0 F=0  T=0 F=8  (ctxt->instate == XML_PARSER_EOF)) {
  d=6   L10884  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=6   L10884  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=6   L10884  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=6   L10886  T=0 F=2  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10888  T=2 F=0  T=8 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=6   L10888  T=2 F=0  T=8 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=6   L10889  T=2 F=0  T=8 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=6   L10889  T=0 F=2  T=0 F=8  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=6   L10907  T=0 F=2  T=0 F=8  if (RAW == '[') {
  d=6   L10918  T=2 F=0  T=8 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=6   L10918  T=2 F=0  T=8 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=6   L10919  T=2 F=0  T=8 F=0  (!ctxt->disableSAX))
  d=6   L10922  T=0 F=2  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10936  T=0 F=2  T=0 F=8  if (RAW != '<') {
  d=6   L10950  T=0 F=2  T=4 F=4  if (RAW != 0) {
  d=6   L10959  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L10959  T=2 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L10965  T=2 F=0  T=8 F=0  if ((ctxt->myDoc != NULL) &&
  d=6   L10966  T=0 F=2  T=0 F=8  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=6   L10971  T=0 F=2  T=0 F=8  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=6   L10980  T=2 F=0  T=8 F=0  if (! ctxt->wellFormed) {
--- d=5  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=5   L10077  T=0 F=2  T=0 F=8  if (xmlParseElementStart(ctxt) != 0)
  d=5   L10081  T=0 F=2  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L10084  T=2 F=0  T=3 F=5  if (CUR == 0) {
--- d=5  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=5   L12139  T=0 F=8  T=0 F=27  if (ctxt == NULL)
  d=5   L12141  T=0 F=4  T=2 F=6  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L12141  T=4 F=4  T=8 F=19  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L12143  T=0 F=8  T=0 F=25  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L12145  T=0 F=8  T=0 F=25  if (ctxt->input == NULL)
  d=5   L12149  T=4 F=4  T=16 F=9  if (ctxt->instate == XML_PARSER_START)
  d=5   L12151  T=6 F=0  T=17 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=5   L12151  T=6 F=2  T=17 F=8  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=5   L12151  T=6 F=0  T=17 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=5   L12152  T=0 F=6  T=0 F=17  (chunk[size - 1] == '\r')) {
  d=5   L12159  T=6 F=0  T=17 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=5   L12159  T=6 F=0  T=17 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=5   L12159  T=6 F=2  T=17 F=8  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=5   L12160  T=6 F=0  T=17 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=5   L12160  T=6 F=0  T=17 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=5   L12170  T=4 F=2  T=16 F=1  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=5   L12170  T=4 F=0  T=16 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=5   L12171  T=4 F=0  T=16 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=5   L12171  T=0 F=4  T=0 F=16  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=5   L12202  T=0 F=6  T=0 F=17  if (res < 0) {
  d=5   L12211  T=2 F=0  T=8 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=5   L12212  T=2 F=0  T=8 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=5   L12212  T=2 F=0  T=8 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=5   L12214  T=0 F=2  T=0 F=8  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=5   L12233  T=0 F=8  T=0 F=25  if (remain != 0) {
  d=5   L12238  T=0 F=8  T=5 F=20  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L12241  T=8 F=0  T=20 F=0  if ((ctxt->input != NULL) &&
  d=5   L12242  T=0 F=8  T=0 F=20  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=5   L12243  T=0 F=8  T=0 F=20  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=5   L12248  T=0 F=8  T=2 F=15  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L12248  T=8 F=0  T=17 F=3  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L12251  T=0 F=8  T=0 F=18  if (remain != 0) {
  d=5   L12257  T=0 F=8  T=0 F=18  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=5   L12268  T=2 F=6  T=4 F=14  if (terminate) {
  d=5   L12274  T=2 F=0  T=4 F=0  if (ctxt->input != NULL) {
  d=5   L12275  T=0 F=2  T=0 F=4  if (ctxt->input->buf == NULL)
  d=5   L12283  T=2 F=0  T=4 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=5   L12284  T=2 F=0  T=0 F=4  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=5   L12287  T=0 F=0  T=0 F=4  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=5   L12287  T=0 F=2  T=4 F=0  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=5   L12290  T=2 F=0  T=4 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=5   L12291  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L12291  T=2 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L12296  T=8 F=0  T=15 F=3  if (ctxt->wellFormed == 0)
--- d=4  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=4   L9995  T=0 F=19  T=1 F=19  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=4   L9996  T=0 F=0  T=0 F=1  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=4   L10006  T=0 F=2  T=5 F=2  if (ctxt->nameNr <= nameNr)
  d=4   L10019  T=0 F=24  T=1 F=21  else if (*cur == '&') {
--- d=4  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=4   L11409  T=0 F=8  T=0 F=25  if (ctxt->input == NULL)
  d=4   L11465  T=8 F=0  T=25 F=0  if ((ctxt->input != NULL) &&
  d=4   L11466  T=0 F=8  T=0 F=25  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=4   L11471  T=0 F=138  T=2 F=145  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L11509  T=4 F=4  T=8 F=16  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=4   L11516  T=0 F=4  T=0 F=8  if (avail < 4)
  d=4   L11535  T=0 F=4  T=0 F=16  if (avail < 2)
  d=4   L11539  T=0 F=4  T=0 F=16  if (cur == 0) {
  d=4   L11553  T=4 F=0  T=16 F=0  if ((cur == '<') && (next == '?')) {
  d=4   L11553  T=4 F=0  T=16 F=0  if ((cur == '<') && (next == '?')) {
  d=4   L11555  T=0 F=4  T=0 F=16  if (avail < 5) goto done;
  d=4   L11556  T=4 F=0  T=16 F=0  if ((!terminate) &&
  d=4   L11557  T=0 F=4  T=0 F=16  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=4   L11559  T=4 F=0  T=16 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L11559  T=4 F=0  T=16 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L11562  T=0 F=4  T=16 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=4   L11563  T=0 F=0  T=16 F=0  (ctxt->input->cur[3] == 'm') &&
  d=4   L11564  T=0 F=0  T=16 F=0  (ctxt->input->cur[4] == 'l') &&
  d=4   L11572  T=0 F=0  T=0 F=16  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=4   L11581  T=0 F=0  T=16 F=0  if ((ctxt->encoding == NULL) &&
  d=4   L11582  T=0 F=0  T=0 F=16  (ctxt->input->encoding != NULL))
  d=4   L11584  T=0 F=0  T=16 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=4   L11584  T=0 F=0  T=16 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=4   L11585  T=0 F=0  T=16 F=0  (!ctxt->disableSAX))
  d=4   L11594  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=4   L11594  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=4   L11595  T=4 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=4   L11639  T=0 F=38  T=6 F=38  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=4   L11639  T=38 F=0  T=44 F=4  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=4   L11643  T=8 F=30  T=0 F=42  else if (*ctxt->space == -2)
  d=4   L11648  T=0 F=38  T=20 F=22  if (ctxt->sax2)
  d=4   L11657  T=0 F=38  T=5 F=37  if (name == NULL) {
  d=4   L11660  T=0 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L11660  T=0 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L11670  T=0 F=0  T=8 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=4   L11670  T=0 F=0  T=8 F=21  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=4   L11670  T=0 F=38  T=29 F=8  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=4   L11671  T=0 F=0  T=0 F=8  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=4   L11671  T=0 F=0  T=8 F=0  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=4   L11678  T=0 F=0  T=0 F=1  if ((RAW == '/') && (NXT(1) == '>')) {
  d=4   L11678  T=0 F=38  T=1 F=36  if ((RAW == '/') && (NXT(1) == '>')) {
  d=4   L11707  T=38 F=0  T=22 F=15  if (RAW == '>') {
  d=4   L11736  T=34 F=0  T=27 F=2  } else if ((cur == '<') && (next != '!')) {
  d=4   L11739  T=0 F=51  T=2 F=59  } else if ((cur == '<') && (next == '!') &&
  d=4   L11739  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (next == '!') &&
  d=4   L11740  T=0 F=0  T=0 F=2  (ctxt->input->cur[2] == '-') &&
  d=4   L11747  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=4   L11747  T=0 F=51  T=2 F=59  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=4   L11748  T=0 F=0  T=0 F=2  (ctxt->input->cur[2] == '[') &&
  d=4   L11758  T=0 F=51  T=2 F=59  } else if ((cur == '<') && (next == '!') &&
  d=4   L11758  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (next == '!') &&
  d=4   L11759  T=0 F=0  T=0 F=2  (avail < 9)) {
  d=4   L11761  T=0 F=51  T=2 F=59  } else if (cur == '<') {
  d=4   L11765  T=0 F=51  T=1 F=58  } else if (cur == '&') {
  d=4   L11766  T=0 F=0  T=0 F=1  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=4   L11784  T=5 F=44  T=0 F=56  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=4   L11793  T=0 F=4  T=0 F=18  if (avail < 2)
  d=4   L11795  T=0 F=4  T=0 F=18  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=4   L11795  T=4 F=0  T=18 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=4   L11797  T=0 F=4  T=4 F=14  if (ctxt->sax2) {
  d=4   L11805  T=0 F=4  T=0 F=18  if (ctxt->instate == XML_PARSER_EOF) {
  d=4   L11807  T=0 F=4  T=8 F=10  } else if (ctxt->nameNr == 0) {
  d=4   L11906  T=0 F=151  T=8 F=228  case XML_PARSER_EPILOG:
  d=4   L11908  T=0 F=12  T=0 F=40  if (ctxt->input->buf == NULL)
  d=4   L11914  T=0 F=12  T=8 F=32  if (avail < 2)
  d=4   L11918  T=12 F=0  T=32 F=0  if ((cur == '<') && (next == '?')) {
  d=4   L11918  T=4 F=8  T=0 F=32  if ((cur == '<') && (next == '?')) {
  d=4   L11919  T=4 F=0  T=0 F=0  if ((!terminate) &&
  d=4   L11920  T=0 F=4  T=0 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=4   L11927  T=0 F=4  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L11929  T=4 F=4  T=16 F=16  } else if ((cur == '<') && (next == '!') &&
  d=4   L11929  T=8 F=0  T=32 F=0  } else if ((cur == '<') && (next == '!') &&
  d=4   L11930  T=0 F=4  T=0 F=16  (ctxt->input->cur[2] == '-') &&
  d=4   L11942  T=4 F=4  T=16 F=16  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=4   L11943  T=4 F=0  T=16 F=0  (cur == '<') && (next == '!') &&
  d=4   L11943  T=4 F=0  T=16 F=0  (cur == '<') && (next == '!') &&
  d=4   L11944  T=4 F=0  T=16 F=0  (ctxt->input->cur[2] == 'D') &&
  d=4   L11945  T=4 F=0  T=16 F=0  (ctxt->input->cur[3] == 'O') &&
  d=4   L11946  T=4 F=0  T=16 F=0  (ctxt->input->cur[4] == 'C') &&
  d=4   L11947  T=4 F=0  T=16 F=0  (ctxt->input->cur[5] == 'T') &&
  d=4   L11948  T=4 F=0  T=16 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=4   L11949  T=4 F=0  T=16 F=0  (ctxt->input->cur[7] == 'P') &&
  d=4   L11950  T=4 F=0  T=16 F=0  (ctxt->input->cur[8] == 'E')) {
  d=4   L11951  T=4 F=0  T=16 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=4   L11951  T=0 F=4  T=0 F=16  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=4   L11959  T=0 F=4  T=0 F=16  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L11961  T=0 F=4  T=0 F=16  if (RAW == '[') {
  d=4   L11972  T=4 F=0  T=16 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=4   L11972  T=4 F=0  T=16 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=4   L11973  T=4 F=0  T=16 F=0  (ctxt->sax->externalSubset != NULL))
  d=4   L11985  T=0 F=4  T=0 F=16  } else if ((cur == '<') && (next == '!') &&
  d=4   L11985  T=4 F=0  T=16 F=0  } else if ((cur == '<') && (next == '!') &&
  d=4   L11989  T=0 F=4  T=0 F=16  } else if (ctxt->instate == XML_PARSER_EPILOG) {
--- d=3  xmlParseCharData  (/src/libxml2/parser.c:4480-4614) ---
  d=3   L4518  T=3 F=0  T=6 F=0  if (ctxt->sax->characters != NULL)
  d=3   L4521  T=3 F=0  T=6 F=0  if (*ctxt->space == -1)
  d=3   L4566  T=0 F=17  T=0 F=0  if (areBlanks(ctxt, tmp, nbchar, 0)) {
  d=3   L4571  T=17 F=0  T=0 F=0  if (ctxt->sax->characters != NULL)
  d=3   L4574  T=17 F=0  T=0 F=0  if (*ctxt->space == -1)
  d=3   L4601  T=0 F=13  T=1 F=15  if (*in == '&') {
  d=3   L4609  T=0 F=13  T=1 F=14  } while (((*in >= 0x20) && (*in <= 0x7F)) ||
  d=3   L4609  T=0 F=0  T=0 F=1  } while (((*in >= 0x20) && (*in <= 0x7F)) ||
--- d=2  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942) ---
  d=2   L2911  T=46 F=2  T=1 F=0  for (i = 0;i < len;i++)
  d=2   L2918  T=0 F=26  T=6 F=30  if (ctxt->node == NULL) return(0);
  d=2   L2921  T=0 F=26  T=30 F=0  if (ret == 0) return(1);
  d=2   L2922  T=0 F=26  T=0 F=0  if (ret == 1) return(0);
  d=2   L2928  T=2 F=24  T=0 F=0  if ((RAW != '<') && (RAW != 0xD)) return(0);
  d=2   L2928  T=2 F=0  T=0 F=0  if ((RAW != '<') && (RAW != 0xD)) return(0);
  d=2   L2929  T=21 F=3  T=0 F=0  if ((ctxt->node->children == NULL) &&
  d=2   L2930  T=0 F=21  T=0 F=0  (RAW == '<') && (NXT(1) == '/')) return(0);
  d=2   L2930  T=21 F=0  T=0 F=0  (RAW == '<') && (NXT(1) == '/')) return(0);
  d=2   L2933  T=21 F=3  T=0 F=0  if (lastChild == NULL) {
  d=2   L2934  T=0 F=21  T=0 F=0  if ((ctxt->node->type != XML_ELEMENT_NODE) &&
  d=2   L2936  T=0 F=3  T=0 F=0  } else if (xmlNodeIsText(lastChild))
  d=2   L2938  T=3 F=0  T=0 F=0  else if ((ctxt->node->children != NULL) &&
  d=2   L2939  T=3 F=0  T=0 F=0  (xmlNodeIsText(ctxt->node->children)))
--- d=1  xmlIsMixedElement  (/src/libxml2/valid.c:3487-3511) ---
  d=1   L3497  T=26 F=0  T=0 F=30  case XML_ELEMENT_TYPE_UNDEFINED:  <-- BLOCKER
  d=1   L3499  T=0 F=26  T=30 F=0  case XML_ELEMENT_TYPE_ELEMENT:

[off-chain: 1136 additional divergent branches across 122 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=3d8f461906a66986, size=302 bytes, fuzzer=grimoire, trial=2, discovered_at=70965s, mutation_op=I2SRandReplace):
  0000: 2f 27 22 3e 06 00 00 37 32 2e 78 6d 6c 5c 0a 3c   /'">...72.xml\.<
  0010: 3f 6d 2e 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20   ?m.?><!DOCTYPEa 
  0020: 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37   SYSTEM "dtds/127
  0030: 37 37 32 2e 64 74 64 22 3e 3c 62 3e 0a 74 64 22   772.dtd"><b>.td"
Seed 2 (id=094847c215eef122, size=327 bytes, fuzzer=grimoire, trial=2, discovered_at=71690s, mutation_op=I2SRandReplace):
  0000: 2f 27 22 3e 06 00 00 37 32 2e 3a 6d 6c 5c 0a 3c   /'">...72.:ml\.<
  0010: 3f 6d 2e 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20   ?m.?><!DOCTYPEa 
  0020: 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37   SYSTEM "dtds/127
  0030: 37 37 32 2e 64 74 64 22 3e 3c 62 3e 0a 74 64 22   772.dtd"><b>.td"

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=b817e7066df7fe62, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=89s, mutation_op=WordAddMutator,BytesRandSetMutator,BytesExpandMutator):
  0000: 06 25 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   .%..127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=1c65f70d71c9b113, size=370 bytes, fuzzer=cmplog, trial=1, discovered_at=241s, mutation_op=BytesSetMutator,BytesSetMutator,BytesExpandMutator):
  0000: 3d 3d 3d 3d 3d 32 37 37 37 32 2e 20 20 20 5c 0a   =====27772.   \.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=001c8c9d4510710d, size=248 bytes, fuzzer=cmplog, trial=1, discovered_at=411s, mutation_op=ByteNegMutator,BytesCopyMutator,BytesInsertMutator,ByteIncMutator,BytesSwapMutator,BytesDeleteMutator,TokenReplace):
  0000: 5f 5f 5f 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ___.127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=51fd9b36079604e3, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=3541s, mutation_op=ByteAddMutator,DwordInterestingMutator):
  0000: ff 7f ff ff 31 32 c8 37 37 32 2e 78 6d 6c 5c 0a   ....12.772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=3df972b457200ada, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=4456s, mutation_op=BytesSetMutator,CrossoverInsertMutator,BytesInsertCopyMutator,ByteFlipMutator,BytesDeleteMutator,TokenInsert,BytesInsertCopyMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c   ersion="1.0"?>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE
  0030: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  2f(/)x2                             ff(.)x2 37(7)x2 06(.)x1 3d(=)x1 +2u  PARTIAL
   0x0001  27(')x2                             7f(.)x2 25(%)x1 3d(=)x1 5f(_)x1 +3u  DIFFER
   0x0002  22(")x2                             ff(.)x2 00(.)x1 3d(=)x1 5f(_)x1 +3u  DIFFER
   0x0003  3e(>)x2                             00(.)x2 ff(.)x2 3d(=)x1 2e(.)x1 +2u  DIFFER
   0x0004  06(.)x2                             31(1)x4 3d(=)x1 78(x)x1 37(7)x1 +1u  DIFFER
   0x0005  00(.)x2                             32(2)x5 6d(m)x1 37(7)x1 2a(*)x1     DIFFER
   0x0006  00(.)x2                             37(7)x4 c8(.)x2 6c(l)x1 3a(:)x1     DIFFER
   0x0007  37(7)x2                             37(7)x6 5c(\)x1 27(')x1             PARTIAL
   0x0008  32(2)x2                             37(7)x6 0a(.)x1 2a(*)x1             DIFFER
   0x0009  2e(.)x2                             32(2)x5 3c(<)x1 37(7)x1 66(f)x1     DIFFER
   0x000a  78(x)x1 3a(:)x1                     2e(.)x5 3f(?)x1 37(7)x1 66(f)x1     DIFFER
   0x000b  6d(m)x2                             78(x)x5 20( )x1 37(7)x1 28(()x1     DIFFER
   0x000c  6c(l)x2                             6d(m)x5 20( )x1 37(7)x1 2f(/)x1     DIFFER
   0x000d  5c(\)x2                             6c(l)x6 20( )x1 2f(/)x1             DIFFER
   0x000e  0a(.)x2                             5c(\)x6 20( )x1 2b(+)x1             DIFFER
   0x000f  3c(<)x2                             0a(.)x6 76(v)x1 27(')x1             DIFFER
   0x0010  3f(?)x2                             3c(<)x6 65(e)x1 2f(/)x1             DIFFER
   0x0011  6d(m)x2                             3f(?)x6 72(r)x1 2a(*)x1             DIFFER
   0x0012  2e(.)x2                             78(x)x6 73(s)x1 2a(*)x1             DIFFER
   0x0013  3f(?)x2                             6d(m)x6 69(i)x1 3a(:)x1             DIFFER
   0x0014  3e(>)x2                             6c(l)x6 6f(o)x1 27(')x1             DIFFER
   0x0015  3c(<)x2                             20( )x6 6e(n)x1 2a(*)x1             DIFFER
   0x0016  21(!)x2                             76(v)x6 3d(=)x1 66(f)x1             DIFFER
   0x0017  44(D)x2                             65(e)x6 22(")x1 66(f)x1             DIFFER
   0x0018  4f(O)x2                             72(r)x6 31(1)x1 2b(+)x1             DIFFER
   0x0019  43(C)x2                             73(s)x6 2e(.)x1 2f(/)x1             DIFFER
   0x001a  54(T)x2                             69(i)x6 30(0)x1 2f(/)x1             DIFFER
   0x001b  59(Y)x2                             6f(o)x6 22(")x1 2b(+)x1             DIFFER
   0x001c  50(P)x2                             6e(n)x6 3f(?)x1 27(')x1             DIFFER
   0x001d  45(E)x2                             3d(=)x6 3e(>)x1 2f(/)x1             DIFFER
   0x001e  61(a)x2                             22(")x6 0a(.)x1 2a(*)x1             DIFFER
   0x001f  20( )x2                             31(1)x6 3c(<)x1 2f(/)x1             DIFFER
   0x0020  53(S)x2                             2e(.)x6 21(!)x1 2f(/)x1             DIFFER
   0x0021  59(Y)x2                             30(0)x6 44(D)x1 2f(/)x1             DIFFER
   0x0022  53(S)x2                             22(")x6 4f(O)x1 2b(+)x1             DIFFER
   0x0023  54(T)x2                             3f(?)x6 43(C)x1 27(')x1             DIFFER
   0x0024  45(E)x2                             3e(>)x6 54(T)x1 2f(/)x1             DIFFER
   0x0025  4d(M)x2                             0a(.)x6 59(Y)x1 2a(*)x1             DIFFER
   0x0026  20( )x2                             3c(<)x6 50(P)x1 3a(:)x1             DIFFER
   0x0027  22(")x2                             21(!)x6 45(E)x1 27(')x1             DIFFER
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

--- grimoire ---
**Baseline relationship**: grimoire builds on the full cmplog stack —
it includes the `CmpLogObserver`, the `TracingStage`, and the
`I2SRandReplace` (i2s) stage — and ADDS a `GeneralizationStage` plus
Grimoire structural mutators. The single-technique delta is therefore
`grimoire` vs `cmplog` (both have I2S; grimoire adds generalization +
Grimoire mutators), not vs naive.

**Instrumentation**: cmplog's edge counters + per-execution CMP buffer
(`CmpLogObserver`).

**Feedback**: edge-bucket `MaxMapFeedback`.

**Mutators / stages**: stages are
`[generalization, tracing, i2s, havoc, grimoire]`. `GeneralizationStage`
replaces concrete byte runs in a corpus entry with `<GAP>` placeholders
(a generalised input) by repeatedly re-executing and checking that
coverage is preserved. The Grimoire mutators —
`GrimoireExtensionMutator`, `GrimoireRecursiveReplacementMutator`,
`GrimoireStringReplacementMutator`, `GrimoireRandomDeleteMutator` —
splice and recurse on these generalised token/gap structures
(string-based, grammar-free structural mutation). `I2SRandReplace` (the
cmplog i2s stage) also runs.

**Observed `mutation_op` in seed metadata**: all grimoire stages (i2s,
havoc, grimoire) are wrapped in `LineageMutatorWrap` with **no
per-operator name list**, so grimoire seeds appear nameless in lineage
(`mutation_op = -`). As with mopt, nameless rows are NOT an
I2S-exclusive signal here — and grimoire genuinely runs I2S too, so the
two are not separable from lineage names.

**Per-execution cost**: cmplog's per-CMP cost, plus extra executions
during generalization (each candidate gap is validated by a re-run).

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_9784.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9784,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9784 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9784 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9784 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).