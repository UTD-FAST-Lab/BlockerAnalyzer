==== BLOCKER ====
Target: libxml2
Branch ID: 6673
Location: /src/libxml2/parser.c:6966:10
Enclosing function: xmlParseMarkupDecl
Source line: 	        case 'N':
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           0       10          0  loser (value_profile vs value_profile_cmplog)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                        0       10          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.90h  loser=23.90h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.90  dur_div=13.00h  hit_div=4
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6673/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseMarkupDecl (/src/libxml2/parser.c:6950-6990) ---
[ ]  6948   */
[ ]  6949  void
[B]  6950  xmlParseMarkupDecl(xmlParserCtxtPtr ctxt) {
[B]  6951      GROW;
[B]  6952      if (CUR == '<') {
[B]  6953          if (NXT(1) == '!') {
[B]  6954  	    switch (NXT(2)) {
[L]  6955  	        case 'E':
[L]  6956  		    if (NXT(3) == 'L')
[L]  6957  			xmlParseElementDecl(ctxt);
[L]  6958  		    else if (NXT(3) == 'N')
[ ]  6959  			xmlParseEntityDecl(ctxt);
[L]  6960                      else
[L]  6961                          SKIP(2);
[L]  6962  		    break;
[L]  6963  	        case 'A':
[L]  6964  		    xmlParseAttributeListDecl(ctxt);
[L]  6965  		    break;
[W]  6966  	        case 'N': <-- BLOCKER
[W]  6967  		    xmlParseNotationDecl(ctxt);
[W]  6968  		    break;
[L]  6969  	        case '-':
[L]  6970  		    xmlParseComment(ctxt);
[L]  6971  		    break;
[ ]  6972  		default:
[ ]  6973  		    /* there is an error but it will be detected later */
[ ]  6974                      SKIP(2);
[ ]  6975  		    break;
[B]  6976  	    }
[B]  6977  	} else if (NXT(1) == '?') {
[ ]  6978  	    xmlParsePI(ctxt);
[ ]  6979  	}
[B]  6980      }
[ ]  6981  
[ ]  6982      /*
[ ]  6983       * detect requirement to exit there and act accordingly
[ ]  6984       * and avoid having instate overridden later on
[ ]  6985       */
[B]  6986      if (ctxt->instate == XML_PARSER_EOF)
[ ]  6987          return;
[ ]  6988  
[B]  6989      ctxt->instate = XML_PARSER_DTD;
[B]  6990  }

--- Caller (1 hop): xmlParseExternalSubset (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142) (±10 around call site) ---
[ ]  7132          xmlCreateIntSubset(ctxt->myDoc, NULL, ExternalID, SystemID);
[ ]  7133  
[B]  7134      ctxt->instate = XML_PARSER_DTD;
[B]  7135      ctxt->external = 1;
[B]  7136      SKIP_BLANKS;
[B]  7137      while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
[B]  7138  	GROW;
[B]  7139          if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
[ ]  7140              xmlParseConditionalSections(ctxt);
[B]  7141          } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) == '?'))) {
[B]  7142              xmlParseMarkupDecl(ctxt); <-- CALL
[B]  7143          } else {
[B]  7144              xmlFatalErr(ctxt, XML_ERR_EXT_SUBSET_NOT_FINISHED, NULL);
[B]  7145              xmlHaltParser(ctxt);
[B]  7146              return;
[B]  7147          }
[B]  7148          SKIP_BLANKS;
[B]  7149      }
[ ]  7150  
[L]  7151      if (RAW != 0) {
[ ]  7152  	xmlFatalErr(ctxt, XML_ERR_EXT_SUBSET_NOT_FINISHED, NULL);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 2  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 3  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 3  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 3  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 4  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 4  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)
hop 5  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseDocTypeDecl at line 11958)
hop 5  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 5  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 5  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)
hop 6  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 6  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 7  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 7  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 7  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     155      7030  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      38      5570  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      62      4950  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
       6      1050  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       0       572  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      18       423  inputPop  (/src/libxml2/parser.c:1723-1738)
       6       383  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)  <-- enclosing
       0       271  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
      12       280  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
      12       280  inputPush  (/src/libxml2/parser.c:1693-1712)
       0       265  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
       0       244  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)
       0       231  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
       0       227  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
       0       205  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203)
... (83 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=6  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=6   L12139  T=0 F=7  T=0 F=145  if (ctxt == NULL)
  d=6   L12141  T=3 F=0  T=42 F=9  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12141  T=3 F=4  T=51 F=94  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12143  T=0 F=4  T=0 F=103  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L12145  T=0 F=4  T=0 F=103  if (ctxt->input == NULL)
  d=6   L12149  T=4 F=0  T=94 F=9  if (ctxt->instate == XML_PARSER_START)
  d=6   L12151  T=4 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=6   L12151  T=4 F=0  T=96 F=7  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=6   L12151  T=4 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=6   L12152  T=0 F=4  T=0 F=96  (chunk[size - 1] == '\r')) {
  d=6   L12159  T=4 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=6   L12159  T=4 F=0  T=96 F=0  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=6   L12159  T=4 F=0  T=96 F=7  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=6   L12160  T=4 F=0  T=96 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=6   L12160  T=4 F=0  T=96 F=0  (ctxt->input->buf != NULL) && (ctxt->instate != XML_PARSE...
  d=6   L12170  T=4 F=0  T=94 F=2  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=6   L12170  T=4 F=0  T=94 F=0  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=6   L12171  T=4 F=0  T=94 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=6   L12171  T=0 F=4  T=0 F=94  (ctxt->input->buf != NULL) && (ctxt->input->buf->encoder ...
  d=6   L12202  T=0 F=4  T=0 F=96  if (res < 0) {
  d=6   L12211  T=0 F=0  T=7 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=6   L12212  T=0 F=0  T=7 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=6   L12212  T=0 F=0  T=7 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=6   L12214  T=0 F=0  T=0 F=7  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=6   L12233  T=0 F=4  T=0 F=103  if (remain != 0) {
  d=6   L12238  T=0 F=4  T=11 F=92  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L12241  T=4 F=0  T=92 F=0  if ((ctxt->input != NULL) &&
  d=6   L12242  T=0 F=4  T=0 F=92  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=6   L12243  T=0 F=4  T=0 F=92  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=6   L12248  T=4 F=0  T=74 F=18  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12248  T=4 F=0  T=92 F=0  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12251  T=0 F=0  T=0 F=18  if (remain != 0) {
  d=6   L12257  T=0 F=0  T=0 F=18  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=6   L12268  T=0 F=0  T=5 F=13  if (terminate) {
  d=6   L12274  T=0 F=0  T=5 F=0  if (ctxt->input != NULL) {
  d=6   L12275  T=0 F=0  T=0 F=5  if (ctxt->input->buf == NULL)
  d=6   L12283  T=0 F=0  T=5 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=6   L12284  T=0 F=0  T=1 F=4  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=6   L12287  T=0 F=0  T=0 F=4  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=6   L12287  T=0 F=0  T=4 F=1  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=6   L12290  T=0 F=0  T=5 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=6   L12291  T=0 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12291  T=0 F=0  T=5 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12296  T=0 F=0  T=13 F=5  if (ctxt->wellFormed == 0)
--- d=5  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=5   L11409  T=0 F=4  T=0 F=103  if (ctxt->input == NULL)
  d=5   L11465  T=4 F=0  T=103 F=0  if ((ctxt->input != NULL) &&
  d=5   L11466  T=0 F=4  T=0 F=103  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=5   L11470  T=14 F=0  T=573 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=5   L11471  T=4 F=0  T=74 F=150  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L11471  T=4 F=10  T=224 F=349  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L11474  T=0 F=10  T=0 F=499  if (ctxt->input == NULL) break;
  d=5   L11475  T=0 F=10  T=0 F=499  if (ctxt->input->buf == NULL)
  d=5   L11486  T=4 F=6  T=356 F=143  if ((ctxt->instate != XML_PARSER_START) &&
  d=5   L11487  T=0 F=4  T=0 F=356  (ctxt->input->buf->raw != NULL) &&
  d=5   L11500  T=0 F=10  T=6 F=493  if (avail < 1)
  d=5   L11502  T=0 F=10  T=0 F=493  switch (ctxt->instate) {
  d=5   L11503  T=0 F=10  T=0 F=493  case XML_PARSER_EOF:
  d=5   L11508  T=6 F=4  T=143 F=350  case XML_PARSER_START:
  d=5   L11509  T=2 F=4  T=49 F=94  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=5   L11516  T=0 F=2  T=0 F=49  if (avail < 4)
  d=5   L11535  T=0 F=4  T=0 F=94  if (avail < 2)
  d=5   L11539  T=0 F=4  T=0 F=94  if (cur == 0) {
  d=5   L11553  T=4 F=0  T=92 F=2  if ((cur == '<') && (next == '?')) {
  d=5   L11553  T=4 F=0  T=94 F=0  if ((cur == '<') && (next == '?')) {
  d=5   L11555  T=0 F=4  T=0 F=92  if (avail < 5) goto done;
  d=5   L11556  T=4 F=0  T=92 F=0  if ((!terminate) &&
  d=5   L11557  T=0 F=4  T=0 F=92  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=5   L11559  T=4 F=0  T=92 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L11559  T=4 F=0  T=92 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L11562  T=4 F=0  T=92 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=5   L11563  T=4 F=0  T=90 F=2  (ctxt->input->cur[3] == 'm') &&
  d=5   L11564  T=4 F=0  T=90 F=0  (ctxt->input->cur[4] == 'l') &&
  d=5   L11572  T=0 F=4  T=0 F=90  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=5   L11581  T=4 F=0  T=90 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L11582  T=0 F=4  T=0 F=90  (ctxt->input->encoding != NULL))
  d=5   L11584  T=4 F=0  T=90 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11584  T=4 F=0  T=90 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11585  T=4 F=0  T=90 F=0  (!ctxt->disableSAX))
  d=5   L11594  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11594  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11595  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=5   L11604  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L11604  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=5   L11608  T=0 F=0  T=0 F=2  if (ctxt->version == NULL) {
  d=5   L11612  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11612  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11613  T=0 F=0  T=2 F=0  (!ctxt->disableSAX))
  d=5   L11622  T=0 F=10  T=71 F=422  case XML_PARSER_START_TAG: {
  d=5   L11629  T=0 F=0  T=0 F=71  if ((avail < 2) && (ctxt->inputNr == 1))
  d=5   L11632  T=0 F=0  T=2 F=69  if (cur != '<') {
  d=5   L11635  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11635  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11639  T=0 F=0  T=3 F=64  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=5   L11639  T=0 F=0  T=67 F=2  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=5   L11641  T=0 F=0  T=0 F=66  if (ctxt->spaceNr == 0)
  d=5   L11643  T=0 F=0  T=4 F=62  else if (*ctxt->space == -2)
  d=5   L11648  T=0 F=0  T=48 F=18  if (ctxt->sax2)
  d=5   L11655  T=0 F=0  T=0 F=66  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L11657  T=0 F=0  T=7 F=59  if (name == NULL) {
  d=5   L11660  T=0 F=0  T=7 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11660  T=0 F=0  T=7 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11670  T=0 F=0  T=8 F=0  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=5   L11670  T=0 F=0  T=8 F=11  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=5   L11670  T=0 F=0  T=19 F=40  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=5   L11671  T=0 F=0  T=0 F=8  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=5   L11671  T=0 F=0  T=8 F=0  ctxt->node && (ctxt->node == ctxt->myDoc->children))
  d=5   L11678  T=0 F=0  T=0 F=59  if ((RAW == '/') && (NXT(1) == '>')) {
  d=5   L11707  T=0 F=0  T=48 F=11  if (RAW == '>') {
  d=5   L11721  T=0 F=10  T=120 F=373  case XML_PARSER_CONTENT: {
  d=5   L11722  T=0 F=0  T=0 F=120  if ((avail < 2) && (ctxt->inputNr == 1))
  d=5   L11727  T=0 F=0  T=20 F=35  if ((cur == '<') && (next == '/')) {
  d=5   L11727  T=0 F=0  T=55 F=65  if ((cur == '<') && (next == '/')) {
  d=5   L11730  T=0 F=0  T=0 F=35  } else if ((cur == '<') && (next == '?')) {
  d=5   L11730  T=0 F=0  T=35 F=65  } else if ((cur == '<') && (next == '?')) {
  d=5   L11736  T=0 F=0  T=35 F=0  } else if ((cur == '<') && (next != '!')) {
  d=5   L11736  T=0 F=0  T=35 F=65  } else if ((cur == '<') && (next != '!')) {
  d=5   L11739  T=0 F=0  T=0 F=65  } else if ((cur == '<') && (next == '!') &&
  d=5   L11747  T=0 F=0  T=0 F=65  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=5   L11758  T=0 F=0  T=0 F=65  } else if ((cur == '<') && (next == '!') &&
  d=5   L11761  T=0 F=0  T=0 F=65  } else if (cur == '<') {
  d=5   L11765  T=0 F=0  T=1 F=64  } else if (cur == '&') {
  d=5   L11766  T=0 F=0  T=0 F=1  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=5   L11782  T=0 F=0  T=64 F=0  if ((ctxt->inputNr == 1) &&
  d=5   L11783  T=0 F=0  T=64 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=5   L11784  T=0 F=0  T=2 F=60  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=5   L11784  T=0 F=0  T=62 F=2  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=5   L11792  T=0 F=10  T=20 F=473  case XML_PARSER_END_TAG:
  d=5   L11793  T=0 F=0  T=0 F=20  if (avail < 2)
  d=5   L11795  T=0 F=0  T=0 F=20  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=5   L11795  T=0 F=0  T=20 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=5   L11797  T=0 F=0  T=12 F=8  if (ctxt->sax2) {
  d=5   L11805  T=0 F=0  T=0 F=20  if (ctxt->instate == XML_PARSER_EOF) {
  d=5   L11807  T=0 F=0  T=8 F=12  } else if (ctxt->nameNr == 0) {
  d=5   L11813  T=0 F=10  T=0 F=493  case XML_PARSER_CDATA_SECTION: {
  d=5   L11904  T=4 F=6  T=96 F=397  case XML_PARSER_MISC:
  d=5   L11905  T=0 F=10  T=34 F=459  case XML_PARSER_PROLOG:
  d=5   L11906  T=0 F=10  T=9 F=484  case XML_PARSER_EPILOG:
  d=5   L11908  T=0 F=4  T=0 F=139  if (ctxt->input->buf == NULL)
  d=5   L11914  T=0 F=4  T=7 F=132  if (avail < 2)
  d=5   L11918  T=4 F=0  T=130 F=2  if ((cur == '<') && (next == '?')) {
  d=5   L11918  T=0 F=4  T=2 F=128  if ((cur == '<') && (next == '?')) {
  d=5   L11919  T=0 F=0  T=2 F=0  if ((!terminate) &&
  d=5   L11920  T=0 F=0  T=0 F=2  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=5   L11927  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L11929  T=4 F=0  T=94 F=34  } else if ((cur == '<') && (next == '!') &&
  d=5   L11929  T=4 F=0  T=128 F=2  } else if ((cur == '<') && (next == '!') &&
  d=5   L11930  T=0 F=4  T=0 F=94  (ctxt->input->cur[2] == '-') &&
  d=5   L11942  T=4 F=0  T=94 F=36  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=5   L11943  T=4 F=0  T=94 F=0  (cur == '<') && (next == '!') &&
  d=5   L11943  T=4 F=0  T=94 F=0  (cur == '<') && (next == '!') &&
  d=5   L11944  T=4 F=0  T=94 F=0  (ctxt->input->cur[2] == 'D') &&
  d=5   L11945  T=4 F=0  T=94 F=0  (ctxt->input->cur[3] == 'O') &&
  d=5   L11946  T=4 F=0  T=94 F=0  (ctxt->input->cur[4] == 'C') &&
  d=5   L11947  T=4 F=0  T=94 F=0  (ctxt->input->cur[5] == 'T') &&
  d=5   L11948  T=4 F=0  T=94 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=5   L11949  T=4 F=0  T=94 F=0  (ctxt->input->cur[7] == 'P') &&
  d=5   L11950  T=4 F=0  T=94 F=0  (ctxt->input->cur[8] == 'E')) {
  d=5   L11951  T=4 F=0  T=94 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=5   L11951  T=0 F=4  T=0 F=94  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=5   L11959  T=0 F=4  T=0 F=94  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L11961  T=0 F=4  T=0 F=94  if (RAW == '[') {
  d=5   L11972  T=4 F=0  T=94 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=5   L11972  T=4 F=0  T=94 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=5   L11973  T=4 F=0  T=94 F=0  (ctxt->sax->externalSubset != NULL))
  d=5   L11985  T=0 F=0  T=0 F=34  } else if ((cur == '<') && (next == '!') &&
  d=5   L11985  T=0 F=0  T=34 F=2  } else if ((cur == '<') && (next == '!') &&
  d=5   L11989  T=0 F=0  T=2 F=34  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=5   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L12007  T=0 F=10  T=0 F=493  case XML_PARSER_DTD: {
  d=5   L12029  T=0 F=10  T=0 F=493  case XML_PARSER_COMMENT:
  d=5   L12038  T=0 F=10  T=0 F=493  case XML_PARSER_IGNORE:
  d=5   L12047  T=0 F=10  T=0 F=493  case XML_PARSER_PI:
  d=5   L12056  T=0 F=10  T=0 F=493  case XML_PARSER_ENTITY_DECL:
  d=5   L12065  T=0 F=10  T=0 F=493  case XML_PARSER_ENTITY_VALUE:
  d=5   L12074  T=0 F=10  T=0 F=493  case XML_PARSER_ATTRIBUTE_VALUE:
  d=5   L12083  T=0 F=10  T=0 F=493  case XML_PARSER_SYSTEM_LITERAL:
  d=5   L12092  T=0 F=10  T=0 F=493  case XML_PARSER_PUBLIC_LITERAL:
--- d=4  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=4   L8396  T=0 F=6  T=0 F=141  if (name == NULL) {
  d=4   L8409  T=6 F=0  T=141 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=4   L8420  T=6 F=0  T=141 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=4   L8420  T=6 F=0  T=141 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=4   L8421  T=6 F=0  T=141 F=0  (!ctxt->disableSAX))
  d=4   L8423  T=0 F=6  T=0 F=141  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L8430  T=0 F=6  T=0 F=141  if (RAW == '[')
  d=4   L8436  T=0 F=6  T=0 F=141  if (RAW != '>') {
--- d=4  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=4   L10816  T=0 F=2  T=0 F=47  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10816  T=0 F=2  T=0 F=47  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=4   L10829  T=2 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10829  T=2 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=4   L10831  T=0 F=2  T=0 F=47  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10834  T=2 F=0  T=47 F=0  if ((ctxt->encoding == NULL) &&
  d=4   L10835  T=2 F=0  T=47 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=4   L10846  T=2 F=0  T=45 F=2  if (enc != XML_CHAR_ENCODING_NONE) {
  d=4   L10852  T=0 F=2  T=0 F=47  if (CUR == 0) {
  d=4   L10863  T=0 F=2  T=0 F=47  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=4   L10872  T=0 F=2  T=0 F=45  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=4   L10873  T=0 F=2  T=0 F=45  (ctxt->instate == XML_PARSER_EOF)) {
  d=4   L10884  T=2 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=2 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10884  T=2 F=0  T=47 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=4   L10886  T=0 F=2  T=0 F=47  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10888  T=2 F=0  T=47 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10888  T=2 F=0  T=47 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=4   L10889  T=2 F=0  T=47 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10889  T=0 F=2  T=0 F=47  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=4   L10907  T=0 F=2  T=0 F=47  if (RAW == '[') {
  d=4   L10918  T=2 F=0  T=47 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10918  T=2 F=0  T=47 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=4   L10919  T=2 F=0  T=47 F=0  (!ctxt->disableSAX))
  d=4   L10922  T=2 F=0  T=23 F=24  if (ctxt->instate == XML_PARSER_EOF)
  d=4   L10936  T=0 F=0  T=1 F=23  if (RAW != '<') {
  d=4   L10950  T=0 F=0  T=10 F=13  if (RAW != 0) {
  d=4   L10959  T=0 F=0  T=24 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10959  T=0 F=0  T=24 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L10965  T=0 F=0  T=24 F=0  if ((ctxt->myDoc != NULL) &&
  d=4   L10966  T=0 F=0  T=0 F=24  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=4   L10971  T=0 F=0  T=1 F=23  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10971  T=0 F=0  T=1 F=0  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=4   L10973  T=0 F=0  T=1 F=0  if (ctxt->valid)
  d=4   L10975  T=0 F=0  T=0 F=1  if (ctxt->nsWellFormed)
  d=4   L10977  T=0 F=0  T=0 F=1  if (ctxt->options & XML_PARSE_OLD10)
  d=4   L10980  T=0 F=0  T=23 F=1  if (! ctxt->wellFormed) {
--- d=2  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=2   L7099  T=6 F=0  T=139 F=0  if ((ctxt->encoding == NULL) &&
  d=2   L7100  T=6 F=0  T=139 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=2   L7109  T=0 F=6  T=0 F=139  if (enc != XML_CHAR_ENCODING_NONE)
  d=2   L7123  T=0 F=6  T=0 F=139  if (ctxt->myDoc == NULL) {
  d=2   L7131  T=0 F=6  T=0 F=139  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=2   L7131  T=6 F=0  T=139 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=2   L7137  T=12 F=0  T=522 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=2   L7137  T=12 F=0  T=450 F=72  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=2   L7139  T=6 F=0  T=383 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=2   L7139  T=6 F=6  T=383 F=67  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=2   L7139  T=0 F=6  T=0 F=383  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=2   L7141  T=6 F=6  T=383 F=67  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=2   L7141  T=6 F=0  T=383 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=2   L7151  T=0 F=0  T=0 F=72  if (RAW != 0) {
--- d=1  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=1   L6952  T=6 F=0  T=383 F=0  if (CUR == '<') {
  d=1   L6953  T=6 F=0  T=383 F=0  if (NXT(1) == '!') {
  d=1   L6955  T=0 F=6  T=273 F=110  case 'E':
  d=1   L6956  T=0 F=0  T=271 F=2  if (NXT(3) == 'L')
  d=1   L6958  T=0 F=0  T=0 F=2  else if (NXT(3) == 'N')
  d=1   L6963  T=0 F=6  T=107 F=276  case 'A':
  d=1   L6966  T=6 F=0  T=0 F=383  case 'N':  <-- BLOCKER
  d=1   L6969  T=0 F=6  T=3 F=380  case '-':
  d=1   L6972  T=0 F=6  T=0 F=383  default:
  d=1   L6986  T=0 F=6  T=0 F=383  if (ctxt->instate == XML_PARSER_EOF)

[off-chain: 950 additional divergent branches across 91 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=213b125c2564a0cb, size=365 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=92s, mutation_op=ByteIncMutator,ByteNegMutator):
  0000: 06 1a 00 00 31 32 37 37 37 32 2e 3a 6d 6c 5c 0a   ....127772.:ml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 0d 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a.SYSTEM "dtds/1
Seed 2 (id=27dc279821b94dd5, size=293 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=19832s, mutation_op=BitFlipMutator,ByteDecMutator,BytesDeleteMutator,BytesRandInsertMutator,ByteIncMutator,BytesCopyMutator):
  0000: 06 1a 00 00 31 32 37 37 37 32 2e 3a 6d 6c 5c 0a   ....127772.:ml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 0d 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a.SYSTEM "dtds/1

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
Seed 3 (id=239c7bb15678b33c, size=379 bytes, fuzzer=cmplog, trial=4, discovered_at=1s, mutation_op=TokenInsert,CrossoverReplaceMutator,WordInterestingMutator,TokenReplace,QwordAddMutator,ByteAddMutator,BytesSwapMutator):
  0000: 13 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30   .ml version="1.0
  0010: 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 41 53   "?>.<!DOCTYPE AS
  0020: 43 49 5e 2f 77 77 77 2e 77 33 2e 6f 72 67 2f 31   CI^/www.w3.org/1
  0030: 39 39 39 2f 78 6c 69 6e 6b 27 0a 20 20 20 20 20   999/xlink'.     
Seed 4 (id=0023d07679e4627f, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=2s, mutation_op=ByteInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=076df8c667aefde7, size=373 bytes, fuzzer=cmplog, trial=2, discovered_at=3s, mutation_op=TokenInsert):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x2                             06(.)x32 3c(<)x2 13(.)x1 64(d)x1 +11u  PARTIAL
   0x0001  1a(.)x2                             00(.)x30 25(%)x2 32(2)x2 6d(m)x1 +12u  DIFFER
   0x0002  00(.)x2                             00(.)x29 ff(.)x3 6c(l)x1 64(d)x1 +13u  PARTIAL
   0x0003  00(.)x2                             00(.)x35 74(t)x2 37(7)x2 20( )x1 +7u  PARTIAL
   0x0004  31(1)x2                             31(1)x35 37(7)x2 76(v)x1 64(d)x1 +8u  PARTIAL
   0x0005  32(2)x2                             32(2)x36 65(e)x1 64(d)x1 6c(l)x1 +8u  PARTIAL
   0x0006  37(7)x2                             37(7)x36 72(r)x1 64(d)x1 5c(\)x1 +8u  PARTIAL
   0x0007  37(7)x2                             37(7)x36 2f(/)x2 73(s)x1 64(d)x1 +7u  PARTIAL
   0x0008  37(7)x2                             37(7)x36 69(i)x1 55(U)x1 64(d)x1 +8u  PARTIAL
   0x0009  32(2)x2                             32(2)x36 6f(o)x1 54(T)x1 3f(?)x1 +8u  PARTIAL
   0x000a  2e(.)x2                             2e(.)x36 6e(n)x1 46(F)x1 78(x)x1 +8u  PARTIAL
   0x000b  3a(:)x2                             78(x)x36 3d(=)x1 2d(-)x1 6d(m)x1 +8u  DIFFER
   0x000c  6d(m)x2                             6d(m)x36 22(")x1 31(1)x1 6c(l)x1 +8u  PARTIAL
   0x000d  6c(l)x2                             6c(l)x35 00(.)x3 31(1)x1 36(6)x1 +7u  PARTIAL
   0x000e  5c(\)x2                             5c(\)x36 2e(.)x2 37(7)x1 76(v)x1 +7u  PARTIAL
   0x000f  0a(.)x2                             0a(.)x36 32(2)x2 30(0)x1 65(e)x1 +7u  PARTIAL
   0x0010  3c(<)x2                             3c(<)x36 2e(.)x2 72(r)x2 22(")x1 +6u  PARTIAL
   0x0011  3f(?)x2                             3f(?)x37 78(x)x1 73(s)x1 37(7)x1 +7u  PARTIAL
   0x0012  78(x)x2                             78(x)x36 3e(>)x1 6d(m)x1 69(i)x1 +8u  PARTIAL
   0x0013  6d(m)x2                             6d(m)x36 0a(.)x1 6c(l)x1 6f(o)x1 +8u  PARTIAL
   0x0014  6c(l)x2                             6c(l)x36 65(e)x2 3c(<)x1 5c(\)x1 +7u  PARTIAL
   0x0015  20( )x2                             20( )x35 0a(.)x2 21(!)x1 3d(=)x1 +8u  PARTIAL
   0x0016  76(v)x2                             76(v)x36 44(D)x1 3c(<)x1 22(")x1 +8u  PARTIAL
   0x0017  65(e)x2                             65(e)x36 20( )x2 4f(O)x1 3f(?)x1 +7u  PARTIAL
   0x0018  72(r)x2                             72(r)x36 78(x)x3 43(C)x1 2e(.)x1 +6u  PARTIAL
   0x0019  73(s)x2                             73(s)x36 6d(m)x2 65(e)x2 54(T)x1 +6u  PARTIAL
   0x001a  69(i)x2                             69(i)x37 6c(l)x2 22(")x2 59(Y)x1 +5u  PARTIAL
   0x001b  6f(o)x2                             6f(o)x36 3f(?)x2 50(P)x1 20( )x1 +7u  PARTIAL
   0x001c  6e(n)x2                             6e(n)x36 45(E)x1 76(v)x1 3e(>)x1 +8u  PARTIAL
   0x001d  3d(=)x2                             3d(=)x36 2f(/)x2 20( )x1 65(e)x1 +7u  PARTIAL
   0x001e  22(")x2                             22(")x37 41(A)x1 72(r)x1 3c(<)x1 +7u  PARTIAL
   0x001f  31(1)x2                             31(1)x36 20( )x2 53(S)x1 73(s)x1 +7u  PARTIAL
   0x0020  2e(.)x2                             2e(.)x36 43(C)x1 69(i)x1 44(D)x1 +8u  PARTIAL
   0x0021  30(0)x2                             30(0)x35 31(1)x2 49(I)x1 6f(o)x1 +8u  PARTIAL
   0x0022  22(")x2                             22(")x36 20( )x2 5e(^)x1 6e(n)x1 +7u  PARTIAL
   0x0023  3f(?)x2                             3f(?)x36 2f(/)x1 3d(=)x1 54(T)x1 +8u  PARTIAL
   0x0024  3e(>)x2                             3e(>)x37 22(")x2 77(w)x1 59(Y)x1 +6u  PARTIAL
   0x0025  0a(.)x2                             0a(.)x35 77(w)x1 31(1)x1 50(P)x1 +9u  PARTIAL
   0x0026  3c(<)x2                             3c(<)x36 2e(.)x2 77(w)x1 45(E)x1 +7u  PARTIAL
   0x0027  21(!)x2                             21(!)x36 20( )x2 2e(.)x1 30(0)x1 +7u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6673.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6673,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6673 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6673 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6673 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).