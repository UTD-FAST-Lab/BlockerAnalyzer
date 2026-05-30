==== BLOCKER ====
Target: libxml2
Branch ID: 6621
Location: /src/libxml2/parser.c:6026:17
Enclosing function: xmlParseAttributeType
Source line:      } else if ((RAW == 'I') && (NXT(1) == 'D')) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (value_profile vs value_profile_cmplog)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog)
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.00h  loser=21.90h
  avg hitcount on branch: winner=6  loser=0
  prob_div=0.90  dur_div=14.90h  hit_div=6
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6621/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseAttributeType (/src/libxml2/parser.c:6015-6043) ---
[ ]  6013   */
[ ]  6014  int
[B]  6015  xmlParseAttributeType(xmlParserCtxtPtr ctxt, xmlEnumerationPtr *tree) {
[B]  6016      SHRINK;
[B]  6017      if (CMP5(CUR_PTR, 'C', 'D', 'A', 'T', 'A')) {
[B]  6018  	SKIP(5);
[B]  6019  	return(XML_ATTRIBUTE_CDATA);
[B]  6020       } else if (CMP6(CUR_PTR, 'I', 'D', 'R', 'E', 'F', 'S')) {
[ ]  6021  	SKIP(6);
[ ]  6022  	return(XML_ATTRIBUTE_IDREFS);
[B]  6023       } else if (CMP5(CUR_PTR, 'I', 'D', 'R', 'E', 'F')) {
[ ]  6024  	SKIP(5);
[ ]  6025  	return(XML_ATTRIBUTE_IDREF);
[B]  6026       } else if ((RAW == 'I') && (NXT(1) == 'D')) { <-- BLOCKER
[W]  6027          SKIP(2);
[W]  6028  	return(XML_ATTRIBUTE_ID);
[B]  6029       } else if (CMP6(CUR_PTR, 'E', 'N', 'T', 'I', 'T', 'Y')) {
[ ]  6030  	SKIP(6);
[ ]  6031  	return(XML_ATTRIBUTE_ENTITY);
[B]  6032       } else if (CMP8(CUR_PTR, 'E', 'N', 'T', 'I', 'T', 'I', 'E', 'S')) {
[ ]  6033  	SKIP(8);
[ ]  6034  	return(XML_ATTRIBUTE_ENTITIES);
[B]  6035       } else if (CMP8(CUR_PTR, 'N', 'M', 'T', 'O', 'K', 'E', 'N', 'S')) {
[ ]  6036  	SKIP(8);
[ ]  6037  	return(XML_ATTRIBUTE_NMTOKENS);
[B]  6038       } else if (CMP7(CUR_PTR, 'N', 'M', 'T', 'O', 'K', 'E', 'N')) {
[ ]  6039  	SKIP(7);
[ ]  6040  	return(XML_ATTRIBUTE_NMTOKEN);
[ ]  6041       }
[B]  6042       return(xmlParseEnumeratedType(ctxt, tree));
[B]  6043  }

--- Caller (1 hop): xmlParseAttributeListDecl (/src/libxml2/parser.c:6059-6169, calls xmlParseAttributeType at line 6104) (±10 around call site) ---
[L]  6094  			       "ATTLIST: no name for Attribute\n");
[L]  6095  		break;
[L]  6096  	    }
[B]  6097  	    GROW;
[B]  6098  	    if (SKIP_BLANKS == 0) {
[L]  6099  		xmlFatalErrMsg(ctxt, XML_ERR_SPACE_REQUIRED,
[L]  6100  		        "Space required after the attribute name\n");
[L]  6101  		break;
[L]  6102  	    }
[ ]  6103  
[B]  6104  	    type = xmlParseAttributeType(ctxt, &tree); <-- CALL
[B]  6105  	    if (type <= 0) {
[B]  6106  	        break;
[B]  6107  	    }
[ ]  6108  
[B]  6109  	    GROW;
[B]  6110  	    if (SKIP_BLANKS == 0) {
[B]  6111  		xmlFatalErrMsg(ctxt, XML_ERR_SPACE_REQUIRED,
[B]  6112  			       "Space required after the attribute type\n");
[B]  6113  	        if (tree != NULL)
[L]  6114  		    xmlFreeEnumeration(tree);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169, calls xmlParseAttributeType at line 6104)
hop 3  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseAttributeListDecl at line 6964)
hop 4  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 4  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 5  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 5  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 5  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 6  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 6  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 6  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)
hop 7  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseDocTypeDecl at line 11958)
hop 7  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 7  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 7  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)
hop 8  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 8  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     351      6920  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     486      6050  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     312      5670  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      69      1180  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      21       860  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      27       423  inputPop  (/src/libxml2/parser.c:1723-1738)
      27       423  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
      21       349  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)  <-- enclosing
      12       314  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
       9       288  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
      12       281  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203)
      18       281  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
      18       281  inputPush  (/src/libxml2/parser.c:1693-1712)
      18       280  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
      18       280  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
... (81 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=8   L12139  T=0 F=9  T=0 F=152  if (ctxt == NULL)
  d=8   L12141  T=3 F=0  T=41 F=17  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L12141  T=3 F=6  T=58 F=94  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L12143  T=0 F=6  T=0 F=111  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L12145  T=0 F=6  T=0 F=111  if (ctxt->input == NULL)
  d=8   L12149  T=6 F=0  T=94 F=17  if (ctxt->instate == XML_PARSER_START)
  d=8   L12151  T=6 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=8   L12151  T=6 F=0  T=96 F=15  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=8   L12151  T=6 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=8   L12152  T=0 F=6  T=0 F=96  (chunk[size - 1] == '\r')) {
  d=8   L12159  T=6 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=8   L12159  T=6 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=8   L12159  T=6 F=0  T=96 F=15  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=8   L12160  T=6 F=0  T=96 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=8   L12160  T=6 F=0  T=96 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=8   L12170  T=6 F=0  T=94 F=2  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=8   L12170  T=6 F=0  T=94 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=8   L12171  T=6 F=0  T=94 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=8   L12171  T=0 F=6  T=0 F=94  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=8   L12202  T=0 F=6  T=0 F=96  if (res < 0) {
  d=8   L12211  T=0 F=0  T=15 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=8   L12212  T=0 F=0  T=15 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=8   L12212  T=0 F=0  T=15 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=8   L12214  T=0 F=0  T=0 F=15  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=8   L12233  T=0 F=6  T=0 F=111  if (remain != 0) {
  d=8   L12238  T=0 F=6  T=8 F=103  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L12241  T=6 F=0  T=103 F=0  if ((ctxt->input != NULL) &&
  d=8   L12242  T=0 F=6  T=0 F=103  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=8   L12243  T=0 F=6  T=0 F=103  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=8   L12248  T=6 F=0  T=69 F=34  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L12248  T=6 F=0  T=103 F=0  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L12251  T=0 F=0  T=0 F=34  if (remain != 0) {
  d=8   L12257  T=0 F=0  T=0 F=34  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=8   L12268  T=0 F=0  T=11 F=23  if (terminate) {
  d=8   L12274  T=0 F=0  T=11 F=0  if (ctxt->input != NULL) {
  d=8   L12275  T=0 F=0  T=0 F=11  if (ctxt->input->buf == NULL)
  d=8   L12283  T=0 F=0  T=11 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=8   L12284  T=0 F=0  T=0 F=11  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=8   L12287  T=0 F=0  T=0 F=11  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=8   L12287  T=0 F=0  T=11 F=0  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=8   L12290  T=0 F=0  T=11 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=8   L12291  T=0 F=0  T=11 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L12291  T=0 F=0  T=11 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L12296  T=0 F=0  T=19 F=15  if (ctxt->wellFormed == 0)
--- d=7  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=7   L11409  T=0 F=6  T=0 F=111  if (ctxt->input == NULL)
  d=7   L11465  T=6 F=0  T=111 F=0  if ((ctxt->input != NULL) &&
  d=7   L11466  T=0 F=6  T=0 F=111  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=7   L11470  T=21 F=0  T=658 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=7   L11471  T=6 F=0  T=69 F=219  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L11471  T=6 F=15  T=288 F=370  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=7   L11474  T=0 F=15  T=0 F=589  if (ctxt->input == NULL) break;
  d=7   L11475  T=0 F=15  T=0 F=589  if (ctxt->input->buf == NULL)
  d=7   L11486  T=6 F=9  T=447 F=142  if ((ctxt->instate != XML_PARSER_START) &&
  d=7   L11487  T=0 F=6  T=0 F=447  (ctxt->input->buf->raw != NULL) &&
  d=7   L11500  T=0 F=15  T=14 F=575  if (avail < 1)
  d=7   L11502  T=0 F=15  T=0 F=575  switch (ctxt->instate) {
  d=7   L11503  T=0 F=15  T=0 F=575  case XML_PARSER_EOF:
  d=7   L11508  T=9 F=6  T=142 F=433  case XML_PARSER_START:
  d=7   L11509  T=3 F=6  T=48 F=94  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=7   L11516  T=0 F=3  T=0 F=48  if (avail < 4)
  d=7   L11535  T=0 F=6  T=0 F=94  if (avail < 2)
  d=7   L11539  T=0 F=6  T=0 F=94  if (cur == 0) {
  d=7   L11553  T=6 F=0  T=94 F=0  if ((cur == '<') && (next == '?')) {
  d=7   L11553  T=6 F=0  T=94 F=0  if ((cur == '<') && (next == '?')) {
  d=7   L11555  T=0 F=6  T=0 F=94  if (avail < 5) goto done;
  d=7   L11556  T=6 F=0  T=94 F=0  if ((!terminate) &&
  d=7   L11557  T=0 F=6  T=0 F=94  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=7   L11559  T=6 F=0  T=94 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L11559  T=6 F=0  T=94 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L11562  T=6 F=0  T=92 F=2  if ((ctxt->input->cur[2] == 'x') &&
  d=7   L11563  T=6 F=0  T=92 F=0  (ctxt->input->cur[3] == 'm') &&
  d=7   L11564  T=6 F=0  T=92 F=0  (ctxt->input->cur[4] == 'l') &&
  d=7   L11572  T=0 F=6  T=0 F=90  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=7   L11581  T=6 F=0  T=90 F=0  if ((ctxt->encoding == NULL) &&
  d=7   L11582  T=0 F=6  T=0 F=90  (ctxt->input->encoding != NULL))
  d=7   L11584  T=6 F=0  T=90 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=7   L11584  T=6 F=0  T=90 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=7   L11585  T=6 F=0  T=90 F=0  (!ctxt->disableSAX))
  d=7   L11594  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=7   L11594  T=0 F=0  T=4 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=7   L11595  T=0 F=0  T=4 F=0  (!ctxt->disableSAX))
  d=7   L11622  T=0 F=15  T=78 F=497  case XML_PARSER_START_TAG: {
  d=7   L11629  T=0 F=0  T=0 F=78  if ((avail < 2) && (ctxt->inputNr == 1))
  d=7   L11632  T=0 F=0  T=3 F=75  if (cur != '<') {
  d=7   L11635  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11635  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11639  T=0 F=0  T=3 F=70  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=7   L11639  T=0 F=0  T=73 F=2  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=7   L11641  T=0 F=0  T=0 F=72  if (ctxt->spaceNr == 0)
  d=7   L11643  T=0 F=0  T=0 F=72  else if (*ctxt->space == -2)
  d=7   L11648  T=0 F=0  T=66 F=6  if (ctxt->sax2)
  d=7   L11655  T=0 F=0  T=0 F=72  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L11657  T=0 F=0  T=3 F=69  if (name == NULL) {
  d=7   L11660  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11660  T=0 F=0  T=3 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11670  T=0 F=0  T=6 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=7   L11670  T=0 F=0  T=6 F=7  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=7   L11670  T=0 F=0  T=13 F=56  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=7   L11671  T=0 F=0  T=0 F=6  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=7   L11671  T=0 F=0  T=6 F=0  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=7   L11678  T=0 F=0  T=0 F=69  if ((RAW == '/') && (NXT(1) == '>')) {
  d=7   L11707  T=0 F=0  T=50 F=19  if (RAW == '>') {
  d=7   L11721  T=0 F=15  T=161 F=414  case XML_PARSER_CONTENT: {
  d=7   L11722  T=0 F=0  T=0 F=161  if ((avail < 2) && (ctxt->inputNr == 1))
  d=7   L11727  T=0 F=0  T=38 F=37  if ((cur == '<') && (next == '/')) {
  d=7   L11727  T=0 F=0  T=75 F=86  if ((cur == '<') && (next == '/')) {
  d=7   L11730  T=0 F=0  T=0 F=37  } else if ((cur == '<') && (next == '?')) {
  d=7   L11730  T=0 F=0  T=37 F=86  } else if ((cur == '<') && (next == '?')) {
  d=7   L11736  T=0 F=0  T=37 F=0  } else if ((cur == '<') && (next != '!')) {
  d=7   L11736  T=0 F=0  T=37 F=86  } else if ((cur == '<') && (next != '!')) {
  d=7   L11739  T=0 F=0  T=0 F=86  } else if ((cur == '<') && (next == '!') &&
  d=7   L11747  T=0 F=0  T=0 F=86  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=7   L11758  T=0 F=0  T=0 F=86  } else if ((cur == '<') && (next == '!') &&
  d=7   L11761  T=0 F=0  T=0 F=86  } else if (cur == '<') {
  d=7   L11765  T=0 F=0  T=1 F=85  } else if (cur == '&') {
  d=7   L11766  T=0 F=0  T=0 F=1  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=7   L11782  T=0 F=0  T=85 F=0  if ((ctxt->inputNr == 1) &&
  d=7   L11783  T=0 F=0  T=85 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=7   L11784  T=0 F=0  T=0 F=84  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=7   L11784  T=0 F=0  T=84 F=1  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=7   L11792  T=0 F=15  T=38 F=537  case XML_PARSER_END_TAG:
  d=7   L11793  T=0 F=0  T=0 F=38  if (avail < 2)
  d=7   L11795  T=0 F=0  T=0 F=38  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=7   L11795  T=0 F=0  T=38 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=7   L11797  T=0 F=0  T=36 F=2  if (ctxt->sax2) {
  d=7   L11805  T=0 F=0  T=0 F=38  if (ctxt->instate == XML_PARSER_EOF) {
  d=7   L11807  T=0 F=0  T=18 F=20  } else if (ctxt->nameNr == 0) {
  d=7   L11813  T=0 F=15  T=0 F=575  case XML_PARSER_CDATA_SECTION: {
  d=7   L11904  T=6 F=9  T=98 F=477  case XML_PARSER_MISC:
  d=7   L11905  T=0 F=15  T=39 F=536  case XML_PARSER_PROLOG:
  d=7   L11906  T=0 F=15  T=19 F=556  case XML_PARSER_EPILOG:
  d=7   L11908  T=0 F=6  T=0 F=156  if (ctxt->input->buf == NULL)
  d=7   L11914  T=0 F=6  T=17 F=139  if (avail < 2)
  d=7   L11918  T=6 F=0  T=136 F=3  if ((cur == '<') && (next == '?')) {
  d=7   L11918  T=0 F=6  T=4 F=132  if ((cur == '<') && (next == '?')) {
  d=7   L11919  T=0 F=0  T=4 F=0  if ((!terminate) &&
  d=7   L11920  T=0 F=0  T=0 F=4  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=7   L11927  T=0 F=0  T=0 F=4  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L11929  T=6 F=0  T=94 F=38  } else if ((cur == '<') && (next == '!') &&
  d=7   L11929  T=6 F=0  T=132 F=3  } else if ((cur == '<') && (next == '!') &&
  d=7   L11930  T=0 F=6  T=0 F=94  (ctxt->input->cur[2] == '-') &&
  d=7   L11942  T=6 F=0  T=94 F=41  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=7   L11943  T=6 F=0  T=94 F=0  (cur == '<') && (next == '!') &&
  d=7   L11943  T=6 F=0  T=94 F=0  (cur == '<') && (next == '!') &&
  d=7   L11944  T=6 F=0  T=94 F=0  (ctxt->input->cur[2] == 'D') &&
  d=7   L11945  T=6 F=0  T=94 F=0  (ctxt->input->cur[3] == 'O') &&
  d=7   L11946  T=6 F=0  T=94 F=0  (ctxt->input->cur[4] == 'C') &&
  d=7   L11947  T=6 F=0  T=94 F=0  (ctxt->input->cur[5] == 'T') &&
  d=7   L11948  T=6 F=0  T=94 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=7   L11949  T=6 F=0  T=94 F=0  (ctxt->input->cur[7] == 'P') &&
  d=7   L11950  T=6 F=0  T=94 F=0  (ctxt->input->cur[8] == 'E')) {
  d=7   L11951  T=6 F=0  T=94 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=7   L11951  T=0 F=6  T=0 F=94  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=7   L11959  T=0 F=6  T=0 F=94  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L11961  T=0 F=6  T=0 F=94  if (RAW == '[') {
  d=7   L11972  T=6 F=0  T=94 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=7   L11972  T=6 F=0  T=94 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=7   L11973  T=6 F=0  T=94 F=0  (ctxt->sax->externalSubset != NULL))
  d=7   L11985  T=0 F=0  T=0 F=38  } else if ((cur == '<') && (next == '!') &&
  d=7   L11985  T=0 F=0  T=38 F=3  } else if ((cur == '<') && (next == '!') &&
  d=7   L11989  T=0 F=0  T=2 F=39  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=7   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L12007  T=0 F=15  T=0 F=575  case XML_PARSER_DTD: {
  d=7   L12029  T=0 F=15  T=0 F=575  case XML_PARSER_COMMENT:
  d=7   L12038  T=0 F=15  T=0 F=575  case XML_PARSER_IGNORE:
  d=7   L12047  T=0 F=15  T=0 F=575  case XML_PARSER_PI:
  d=7   L12056  T=0 F=15  T=0 F=575  case XML_PARSER_ENTITY_DECL:
  d=7   L12065  T=0 F=15  T=0 F=575  case XML_PARSER_ENTITY_VALUE:
  d=7   L12074  T=0 F=15  T=0 F=575  case XML_PARSER_ATTRIBUTE_VALUE:
  d=7   L12083  T=0 F=15  T=0 F=575  case XML_PARSER_SYSTEM_LITERAL:
  d=7   L12092  T=0 F=15  T=0 F=575  case XML_PARSER_PUBLIC_LITERAL:
--- d=6  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=6   L8396  T=0 F=9  T=0 F=141  if (name == NULL) {
  d=6   L8409  T=9 F=0  T=141 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=6   L8420  T=9 F=0  T=141 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=6   L8420  T=9 F=0  T=141 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=6   L8421  T=9 F=0  T=141 F=0  (!ctxt->disableSAX))
  d=6   L8423  T=0 F=9  T=0 F=141  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L8430  T=0 F=9  T=0 F=141  if (RAW == '[')
  d=6   L8436  T=0 F=9  T=0 F=141  if (RAW != '>') {
--- d=6  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=6   L10816  T=0 F=3  T=0 F=47  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=6   L10816  T=0 F=3  T=0 F=47  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=6   L10829  T=3 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L10829  T=3 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=6   L10831  T=0 F=3  T=0 F=47  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10834  T=3 F=0  T=47 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L10835  T=3 F=0  T=47 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=6   L10846  T=3 F=0  T=46 F=1  if (enc != XML_CHAR_ENCODING_NONE) {
  d=6   L10852  T=0 F=3  T=0 F=47  if (CUR == 0) {
  d=6   L10863  T=0 F=3  T=0 F=47  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=6   L10872  T=0 F=3  T=0 F=45  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=6   L10873  T=0 F=3  T=0 F=45  (ctxt->instate == XML_PARSER_EOF)) {
  d=6   L10884  T=3 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=6   L10884  T=3 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=6   L10884  T=3 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=6   L10886  T=0 F=3  T=0 F=47  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10888  T=3 F=0  T=47 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=6   L10888  T=3 F=0  T=47 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=6   L10889  T=3 F=0  T=47 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=6   L10889  T=0 F=3  T=0 F=47  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=6   L10907  T=0 F=3  T=0 F=47  if (RAW == '[') {
  d=6   L10918  T=3 F=0  T=47 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=6   L10918  T=3 F=0  T=47 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=6   L10919  T=3 F=0  T=47 F=0  (!ctxt->disableSAX))
  d=6   L10922  T=3 F=0  T=19 F=28  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L10936  T=0 F=0  T=2 F=26  if (RAW != '<') {
  d=6   L10950  T=0 F=0  T=8 F=18  if (RAW != 0) {
  d=6   L10959  T=0 F=0  T=28 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L10959  T=0 F=0  T=28 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L10965  T=0 F=0  T=28 F=0  if ((ctxt->myDoc != NULL) &&
  d=6   L10966  T=0 F=0  T=0 F=28  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=6   L10971  T=0 F=0  T=3 F=25  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=6   L10971  T=0 F=0  T=3 F=0  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=6   L10973  T=0 F=0  T=3 F=0  if (ctxt->valid)
  d=6   L10975  T=0 F=0  T=0 F=3  if (ctxt->nsWellFormed)
  d=6   L10977  T=0 F=0  T=0 F=3  if (ctxt->options & XML_PARSE_OLD10)
  d=6   L10980  T=0 F=0  T=25 F=3  if (! ctxt->wellFormed) {
--- d=4  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=4   L7099  T=9 F=0  T=140 F=0  if ((ctxt->encoding == NULL) &&
  d=4   L7100  T=9 F=0  T=140 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=4   L7109  T=0 F=9  T=0 F=140  if (enc != XML_CHAR_ENCODING_NONE)
  d=4   L7123  T=0 F=9  T=0 F=140  if (ctxt->myDoc == NULL) {
  d=4   L7131  T=0 F=9  T=0 F=140  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=4   L7131  T=9 F=0  T=140 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=4   L7137  T=36 F=0  T=563 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=4   L7137  T=36 F=0  T=479 F=84  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=4   L7139  T=27 F=0  T=423 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=4   L7139  T=27 F=9  T=423 F=56  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=4   L7139  T=0 F=27  T=0 F=423  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=4   L7141  T=27 F=9  T=423 F=56  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=4   L7141  T=27 F=0  T=423 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=4   L7151  T=0 F=0  T=0 F=84  if (RAW != 0) {
--- d=3  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=3   L6952  T=27 F=0  T=423 F=0  if (CUR == '<') {
  d=3   L6953  T=27 F=0  T=423 F=0  if (NXT(1) == '!') {
  d=3   L6955  T=18 F=9  T=280 F=143  case 'E':
  d=3   L6956  T=18 F=0  T=280 F=0  if (NXT(3) == 'L')
  d=3   L6963  T=9 F=18  T=140 F=283  case 'A':
  d=3   L6966  T=0 F=27  T=0 F=423  case 'N':
  d=3   L6969  T=0 F=27  T=0 F=423  case '-':
  d=3   L6972  T=0 F=27  T=3 F=420  default:
  d=3   L6986  T=0 F=27  T=0 F=423  if (ctxt->instate == XML_PARSER_EOF)
--- d=2  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169) ---
  d=2   L6064  T=0 F=9  T=0 F=140  if ((CUR != '<') || (NXT(1) != '!'))
  d=2   L6064  T=0 F=9  T=0 F=140  if ((CUR != '<') || (NXT(1) != '!'))
  d=2   L6072  T=0 F=9  T=9 F=131  if (SKIP_BLANKS == 0) {
  d=2   L6077  T=0 F=9  T=0 F=140  if (elemName == NULL) {
  d=2   L6084  T=21 F=0  T=388 F=0  while ((RAW != '>') && (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L6084  T=21 F=0  T=388 F=60  while ((RAW != '>') && (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L6092  T=0 F=21  T=30 F=358  if (attrName == NULL) {
  d=2   L6098  T=0 F=21  T=9 F=349  if (SKIP_BLANKS == 0) {
  d=2   L6105  T=6 F=15  T=17 F=332  if (type <= 0) {
  d=2   L6110  T=3 F=12  T=18 F=314  if (SKIP_BLANKS == 0) {
  d=2   L6113  T=0 F=3  T=18 F=0  if (tree != NULL)
  d=2   L6119  T=0 F=12  T=0 F=314  if (def <= 0) {
  d=2   L6126  T=3 F=0  T=105 F=3  if ((type != XML_ATTRIBUTE_CDATA) && (defaultValue != NULL))
  d=2   L6126  T=3 F=9  T=108 F=206  if ((type != XML_ATTRIBUTE_CDATA) && (defaultValue != NULL))
  d=2   L6130  T=12 F=0  T=254 F=60  if (RAW != '>') {
  d=2   L6131  T=0 F=12  T=6 F=248  if (SKIP_BLANKS == 0) {
  d=2   L6134  T=0 F=0  T=0 F=6  if (defaultValue != NULL)
  d=2   L6136  T=0 F=0  T=3 F=3  if (tree != NULL)
  d=2   L6141  T=12 F=0  T=308 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L6141  T=9 F=3  T=272 F=36  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=2   L6142  T=9 F=0  T=272 F=0  (ctxt->sax->attributeDecl != NULL))
  d=2   L6145  T=0 F=3  T=12 F=24  else if (tree != NULL)
  d=2   L6148  T=12 F=0  T=215 F=57  if ((ctxt->sax2) && (defaultValue != NULL) &&
  d=2   L6148  T=12 F=0  T=272 F=36  if ((ctxt->sax2) && (defaultValue != NULL) &&
  d=2   L6149  T=12 F=0  T=215 F=0  (def != XML_ATTRIBUTE_IMPLIED) &&
  d=2   L6150  T=12 F=0  T=215 F=0  (def != XML_ATTRIBUTE_REQUIRED)) {
  d=2   L6153  T=12 F=0  T=272 F=36  if (ctxt->sax2) {
  d=2   L6156  T=12 F=0  T=242 F=66  if (defaultValue != NULL)
  d=2   L6160  T=0 F=9  T=63 F=77  if (RAW == '>') {
  d=2   L6161  T=0 F=0  T=0 F=63  if (inputid != ctxt->input->id) {
--- d=1  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043) ---
  d=1   L6026  T=3 F=6  T=0 F=0  } else if ((RAW == 'I') && (NXT(1) == 'D')) {  <-- BLOCKER
  d=1   L6026  T=9 F=3  T=0 F=143  } else if ((RAW == 'I') && (NXT(1) == 'D')) {  <-- BLOCKER

[off-chain: 897 additional divergent branches across 87 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=fc8699bbd779e3d9, size=368 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=92s, mutation_op=BytesCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=e3a3befc7b7e33ef, size=368 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=139s, mutation_op=BytesExpandMutator,BytesSwapMutator,BytesSetMutator,ByteAddMutator,DwordAddMutator,WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=39967b9a0f05aa26, size=368 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1810s, mutation_op=BytesInsertCopyMutator,DwordInterestingMutator,QwordAddMutator,BytesCopyMutator,BytesDeleteMutator):
  0000: 31 31 31 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   111.127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 0a   .0"?>.<!DOCTYPE.
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00f7af173db700b0, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=0s, mutation_op=BytesExpandMutator,DwordAddMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=00fd268513ef89d3, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=1s, mutation_op=BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=062e97a74ea2d1b7, size=368 bytes, fuzzer=cmplog, trial=5, discovered_at=1s, mutation_op=ByteNegMutator,DwordInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=076df8c667aefde7, size=373 bytes, fuzzer=cmplog, trial=2, discovered_at=3s, mutation_op=TokenInsert):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=0be939129cb3ca8a, size=377 bytes, fuzzer=cmplog, trial=1, discovered_at=3s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x2 31(1)x1                     06(.)x34 3d(=)x2 05(.)x2 31(1)x2 +7u  PARTIAL
   0x0001  00(.)x2 31(1)x1                     00(.)x36 3d(=)x2 32(2)x2 64(d)x1 +6u  PARTIAL
   0x0002  00(.)x2 31(1)x1                     00(.)x37 37(7)x2 64(d)x1 3d(=)x1 +6u  PARTIAL
   0x0003  00(.)x3                             00(.)x37 54(T)x2 37(7)x2 64(d)x1 +5u  PARTIAL
   0x0004  31(1)x3                             31(1)x36 41(A)x2 37(7)x2 64(d)x1 +6u  PARTIAL
   0x0005  32(2)x3                             32(2)x39 29())x2 64(d)x1 9d(.)x1 +4u  PARTIAL
   0x0006  37(7)x3                             37(7)x38 3e(>)x2 2e(.)x2 64(d)x1 +4u  PARTIAL
   0x0007  37(7)x3                             37(7)x38 0a(.)x2 78(x)x2 64(d)x1 +4u  PARTIAL
   0x0008  37(7)x3                             37(7)x39 3c(<)x2 6d(m)x2 55(U)x1 +3u  PARTIAL
   0x0009  32(2)x3                             32(2)x39 21(!)x2 6c(l)x2 54(T)x1 +3u  PARTIAL
   0x000a  2e(.)x3                             2e(.)x39 41(A)x2 5c(\)x2 46(F)x1 +3u  PARTIAL
   0x000b  78(x)x3                             78(x)x38 54(T)x2 0a(.)x2 2d(-)x1 +4u  PARTIAL
   0x000c  6d(m)x3                             6d(m)x38 20( )x2 54(T)x2 3c(<)x2 +3u  PARTIAL
   0x000d  6c(l)x3                             6c(l)x38 4c(L)x2 3f(?)x2 36(6)x1 +4u  PARTIAL
   0x000e  5c(\)x3                             5c(\)x39 49(I)x2 78(x)x2 37(7)x1 +3u  PARTIAL
   0x000f  0a(.)x3                             0a(.)x39 53(S)x2 6d(m)x2 32(2)x1 +3u  PARTIAL
   0x0010  3c(<)x3                             3c(<)x39 2e(.)x2 54(T)x2 6c(l)x2 +2u  PARTIAL
   0x0011  3f(?)x3                             3f(?)x39 20( )x4 78(x)x1 6e(n)x1 +2u  PARTIAL
   0x0012  78(x)x3                             78(x)x38 00(.)x2 76(v)x2 6d(m)x1 +4u  PARTIAL
   0x0013  6d(m)x3                             6d(m)x39 31(1)x2 65(e)x2 6c(l)x1 +3u  PARTIAL
   0x0014  6c(l)x3                             6c(l)x39 32(2)x2 72(r)x2 5c(\)x1 +3u  PARTIAL
   0x0015  20( )x3                             20( )x37 0a(.)x2 37(7)x2 73(s)x2 +4u  PARTIAL
   0x0016  76(v)x3                             76(v)x38 37(7)x2 69(i)x2 3c(<)x1 +4u  PARTIAL
   0x0017  65(e)x3                             65(e)x38 37(7)x2 6f(o)x2 20( )x2 +3u  PARTIAL
   0x0018  72(r)x3                             72(r)x38 32(2)x2 6e(n)x2 78(x)x1 +4u  PARTIAL
   0x0019  73(s)x3                             73(s)x38 2e(.)x2 3d(=)x2 65(e)x2 +3u  PARTIAL
   0x001a  69(i)x3                             69(i)x38 78(x)x2 22(")x2 6c(l)x1 +4u  PARTIAL
   0x001b  6f(o)x3                             6f(o)x38 6d(m)x2 31(1)x2 20( )x1 +4u  PARTIAL
   0x001c  6e(n)x3                             6e(n)x38 6c(l)x2 2e(.)x2 76(v)x1 +4u  PARTIAL
   0x001d  3d(=)x3                             3d(=)x38 5c(\)x2 30(0)x2 65(e)x1 +4u  PARTIAL
   0x001e  22(")x3                             22(")x40 0a(.)x2 72(r)x1 33(3)x1 +3u  PARTIAL
   0x001f  31(1)x3                             31(1)x38 3c(<)x2 3f(?)x2 73(s)x1 +4u  PARTIAL
   0x0020  2e(.)x3                             2e(.)x38 3f(?)x2 3e(>)x2 69(i)x1 +4u  PARTIAL
   0x0021  30(0)x3                             30(0)x37 78(x)x2 31(1)x2 0a(.)x2 +4u  PARTIAL
   0x0022  22(")x3                             22(")x38 6d(m)x2 3c(<)x2 6e(n)x1 +4u  PARTIAL
   0x0023  3f(?)x3                             3f(?)x38 6c(l)x2 21(!)x2 3d(=)x1 +4u  PARTIAL
   0x0024  3e(>)x3                             3e(>)x39 22(")x2 20( )x2 44(D)x2 +2u  PARTIAL
   0x0025  0a(.)x3                             0a(.)x38 76(v)x2 4f(O)x2 31(1)x1 +4u  PARTIAL
   0x0026  3c(<)x3                             3c(<)x38 65(e)x2 43(C)x2 2e(.)x1 +4u  PARTIAL
   0x0027  21(!)x3                             21(!)x38 72(r)x2 54(T)x2 30(0)x1 +4u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6621.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6621,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6621 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6621 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6621 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).