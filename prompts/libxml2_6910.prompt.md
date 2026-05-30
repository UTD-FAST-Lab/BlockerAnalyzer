==== BLOCKER ====
Target: libxml2
Branch ID: 6910
Location: /src/libxml2/tree.c:334:9
Enclosing function: xmlSplitQName3
Source line:     if (name[0] == ':')
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            4        6          0  REFERENCE
cmplog                           9        1          0  REFERENCE
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        8        2          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.10h  loser=20.00h
  avg hitcount on branch: winner=26  loser=1
  prob_div=0.80  dur_div=15.90h  hit_div=25
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6910/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlSplitQName3 (/src/libxml2/tree.c:327-350) ---
[ ]   325  
[ ]   326  const xmlChar *
[B]   327  xmlSplitQName3(const xmlChar *name, int *len) {
[B]   328      int l = 0;
[ ]   329  
[B]   330      if (name == NULL) return(NULL);
[B]   331      if (len == NULL) return(NULL);
[ ]   332  
[ ]   333      /* nasty but valid */
[B]   334      if (name[0] == ':') <-- BLOCKER
[W]   335  	return(NULL);
[ ]   336  
[ ]   337      /*
[ ]   338       * we are not trying to validate but just to cut, and yes it will
[ ]   339       * work even if this is as set of UTF-8 encoded chars
[ ]   340       */
[B]   341      while ((name[l] != 0) && (name[l] != ':'))
[B]   342  	l++;
[ ]   343  
[B]   344      if (name[l] == 0)
[B]   345  	return(NULL);
[ ]   346  
[ ]   347      *len = l;
[ ]   348  
[ ]   349      return(&name[l+1]);
[B]   350  }

--- Caller (1 hop): xmlNewDocElementContent (/src/libxml2/valid.c:902-961, calls xmlSplitQName3 at line 944) (±10 around call site) ---
[ ]   934  	xmlVErrMemory(NULL, "malloc failed");
[ ]   935  	return(NULL);
[ ]   936      }
[B]   937      memset(ret, 0, sizeof(xmlElementContent));
[B]   938      ret->type = type;
[B]   939      ret->ocur = XML_ELEMENT_CONTENT_ONCE;
[B]   940      if (name != NULL) {
[B]   941          int l;
[B]   942  	const xmlChar *tmp;
[ ]   943  
[B]   944  	tmp = xmlSplitQName3(name, &l); <-- CALL
[B]   945  	if (tmp == NULL) {
[B]   946  	    if (dict == NULL)
[L]   947  		ret->name = xmlStrdup(name);
[B]   948  	    else
[B]   949  	        ret->name = xmlDictLookup(dict, name, -1);
[B]   950  	} else {
[ ]   951  	    if (dict == NULL) {
[ ]   952  		ret->prefix = xmlStrndup(name, l);
[ ]   953  		ret->name = xmlStrdup(tmp);
[ ]   954  	    } else {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlAddDefAttrs  (/src/libxml2/parser.c:1194-1292, calls xmlSplitQName3 at line 1218)
hop 3  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169, calls parser.c:xmlAddDefAttrs at line 6151)
hop 4  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseAttributeListDecl at line 6964)
hop 5  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 5  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 6  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 6  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 6  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 7  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 7  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)
hop 8  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseDocTypeDecl at line 11958)
hop 8  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 8  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 8  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     307      1350  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     210       688  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      39       128  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      18        90  inputPop  (/src/libxml2/parser.c:1723-1738)
       9        61  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
      12        64  xmlGetIntSubset  (/src/libxml2/tree.c:924-936)
      15        60  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
      12        56  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
      12        56  inputPush  (/src/libxml2/parser.c:1693-1712)
      12        56  xmlFreeDtd  (/src/libxml2/tree.c:1103-1150)
      39         0  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      12        50  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
      12        47  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
       5        37  parser.c:xmlHaltParser  (/src/libxml2/parser.c:12416-12441)
      12        42  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
... (77 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=8   L11409  T=0 F=4  T=0 F=24  if (ctxt->input == NULL)
  d=8   L11465  T=4 F=0  T=24 F=0  if ((ctxt->input != NULL) &&
  d=8   L11466  T=0 F=4  T=0 F=24  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=8   L11470  T=24 F=0  T=93 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=8   L11471  T=4 F=0  T=17 F=8  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L11471  T=4 F=20  T=25 F=68  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=8   L11474  T=0 F=20  T=0 F=76  if (ctxt->input == NULL) break;
  d=8   L11475  T=0 F=20  T=0 F=76  if (ctxt->input->buf == NULL)
  d=8   L11486  T=14 F=6  T=46 F=30  if ((ctxt->instate != XML_PARSER_START) &&
  d=8   L11487  T=0 F=14  T=0 F=46  (ctxt->input->buf->raw != NULL) &&
  d=8   L11500  T=0 F=20  T=2 F=74  if (avail < 1)
  d=8   L11502  T=0 F=20  T=0 F=74  switch (ctxt->instate) {
  d=8   L11503  T=0 F=20  T=0 F=74  case XML_PARSER_EOF:
  d=8   L11508  T=6 F=14  T=30 F=44  case XML_PARSER_START:
  d=8   L11509  T=2 F=4  T=10 F=20  if (ctxt->charset == XML_CHAR_ENCODING_NONE) {
  d=8   L11516  T=0 F=2  T=0 F=10  if (avail < 4)
  d=8   L11535  T=0 F=4  T=0 F=20  if (avail < 2)
  d=8   L11539  T=0 F=4  T=0 F=20  if (cur == 0) {
  d=8   L11553  T=4 F=0  T=20 F=0  if ((cur == '<') && (next == '?')) {
  d=8   L11553  T=4 F=0  T=20 F=0  if ((cur == '<') && (next == '?')) {
  d=8   L11555  T=0 F=4  T=0 F=20  if (avail < 5) goto done;
  d=8   L11556  T=4 F=0  T=20 F=0  if ((!terminate) &&
  d=8   L11557  T=0 F=4  T=0 F=20  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=8   L11559  T=4 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L11559  T=4 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L11562  T=4 F=0  T=20 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=8   L11563  T=4 F=0  T=20 F=0  (ctxt->input->cur[3] == 'm') &&
  d=8   L11564  T=4 F=0  T=20 F=0  (ctxt->input->cur[4] == 'l') &&
  d=8   L11572  T=0 F=4  T=0 F=20  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=8   L11581  T=4 F=0  T=20 F=0  if ((ctxt->encoding == NULL) &&
  d=8   L11582  T=0 F=4  T=0 F=20  (ctxt->input->encoding != NULL))
  d=8   L11584  T=4 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=8   L11584  T=4 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=8   L11585  T=4 F=0  T=20 F=0  (!ctxt->disableSAX))
  d=8   L11622  T=4 F=16  T=10 F=64  case XML_PARSER_START_TAG: {
  d=8   L11629  T=0 F=4  T=0 F=10  if ((avail < 2) && (ctxt->inputNr == 1))
  d=8   L11632  T=0 F=4  T=1 F=9  if (cur != '<') {
  d=8   L11635  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L11635  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L11639  T=0 F=4  T=4 F=3  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11639  T=4 F=0  T=7 F=2  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11648  T=4 F=0  T=4 F=1  if (ctxt->sax2)
  d=8   L11670  T=0 F=0  T=0 F=1  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=8   L11670  T=0 F=4  T=1 F=4  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=8   L11721  T=4 F=16  T=10 F=64  case XML_PARSER_CONTENT: {
  d=8   L11722  T=0 F=4  T=0 F=10  if ((avail < 2) && (ctxt->inputNr == 1))
  d=8   L11727  T=0 F=2  T=0 F=4  if ((cur == '<') && (next == '/')) {
  d=8   L11727  T=2 F=2  T=4 F=6  if ((cur == '<') && (next == '/')) {
  d=8   L11730  T=0 F=2  T=0 F=4  } else if ((cur == '<') && (next == '?')) {
  d=8   L11730  T=2 F=2  T=4 F=6  } else if ((cur == '<') && (next == '?')) {
  d=8   L11736  T=2 F=0  T=2 F=2  } else if ((cur == '<') && (next != '!')) {
  d=8   L11736  T=2 F=2  T=4 F=6  } else if ((cur == '<') && (next != '!')) {
  d=8   L11739  T=0 F=2  T=2 F=6  } else if ((cur == '<') && (next == '!') &&
  d=8   L11739  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (next == '!') &&
  d=8   L11740  T=0 F=0  T=0 F=2  (ctxt->input->cur[2] == '-') &&
  d=8   L11747  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=8   L11747  T=0 F=2  T=2 F=6  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=8   L11748  T=0 F=0  T=0 F=2  (ctxt->input->cur[2] == '[') &&
  d=8   L11758  T=0 F=2  T=2 F=6  } else if ((cur == '<') && (next == '!') &&
  d=8   L11758  T=0 F=0  T=2 F=0  } else if ((cur == '<') && (next == '!') &&
  d=8   L11759  T=0 F=0  T=0 F=2  (avail < 9)) {
  d=8   L11761  T=0 F=2  T=2 F=6  } else if (cur == '<') {
  d=8   L11765  T=0 F=2  T=0 F=6  } else if (cur == '&') {
  d=8   L11782  T=2 F=0  T=6 F=0  if ((ctxt->inputNr == 1) &&
  d=8   L11783  T=2 F=0  T=6 F=0  (avail < XML_PARSER_BIG_BUFFER_SIZE)) {
  d=8   L11784  T=2 F=0  T=2 F=4  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=8   L11792  T=0 F=20  T=0 F=74  case XML_PARSER_END_TAG:
  d=8   L11813  T=0 F=20  T=0 F=74  case XML_PARSER_CDATA_SECTION: {
  d=8   L11904  T=4 F=16  T=20 F=54  case XML_PARSER_MISC:
  d=8   L11905  T=2 F=18  T=4 F=70  case XML_PARSER_PROLOG:
  d=8   L11906  T=0 F=20  T=0 F=74  case XML_PARSER_EPILOG:
  d=8   L11908  T=0 F=6  T=0 F=24  if (ctxt->input->buf == NULL)
  d=8   L11914  T=0 F=6  T=0 F=24  if (avail < 2)
  d=8   L11918  T=6 F=0  T=23 F=1  if ((cur == '<') && (next == '?')) {
  d=8   L11918  T=0 F=6  T=0 F=23  if ((cur == '<') && (next == '?')) {
  d=8   L11929  T=4 F=2  T=20 F=3  } else if ((cur == '<') && (next == '!') &&
  d=8   L11929  T=6 F=0  T=23 F=1  } else if ((cur == '<') && (next == '!') &&
  d=8   L11930  T=0 F=4  T=0 F=20  (ctxt->input->cur[2] == '-') &&
  d=8   L11942  T=4 F=2  T=20 F=4  } else if ((ctxt->instate == XML_PARSER_MISC) &&
  d=8   L11943  T=4 F=0  T=20 F=0  (cur == '<') && (next == '!') &&
  d=8   L11943  T=4 F=0  T=20 F=0  (cur == '<') && (next == '!') &&
  d=8   L11944  T=4 F=0  T=20 F=0  (ctxt->input->cur[2] == 'D') &&
  d=8   L11945  T=4 F=0  T=20 F=0  (ctxt->input->cur[3] == 'O') &&
  d=8   L11946  T=4 F=0  T=20 F=0  (ctxt->input->cur[4] == 'C') &&
  d=8   L11947  T=4 F=0  T=20 F=0  (ctxt->input->cur[5] == 'T') &&
  d=8   L11948  T=4 F=0  T=20 F=0  (ctxt->input->cur[6] == 'Y') &&
  d=8   L11949  T=4 F=0  T=20 F=0  (ctxt->input->cur[7] == 'P') &&
  d=8   L11950  T=4 F=0  T=20 F=0  (ctxt->input->cur[8] == 'E')) {
  d=8   L11951  T=4 F=0  T=20 F=0  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11951  T=0 F=4  T=0 F=20  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=8   L11959  T=0 F=4  T=0 F=20  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L11961  T=0 F=4  T=0 F=20  if (RAW == '[') {
  d=8   L11972  T=4 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=8   L11972  T=4 F=0  T=20 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=8   L11973  T=4 F=0  T=20 F=0  (ctxt->sax->externalSubset != NULL))
  d=8   L11985  T=2 F=0  T=3 F=1  } else if ((cur == '<') && (next == '!') &&
  d=8   L11989  T=0 F=2  T=0 F=4  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=8   L12007  T=0 F=20  T=0 F=74  case XML_PARSER_DTD: {
  d=8   L12029  T=0 F=20  T=0 F=74  case XML_PARSER_COMMENT:
  d=8   L12038  T=0 F=20  T=0 F=74  case XML_PARSER_IGNORE:
  d=8   L12047  T=0 F=20  T=0 F=74  case XML_PARSER_PI:
  d=8   L12056  T=0 F=20  T=0 F=74  case XML_PARSER_ENTITY_DECL:
  d=8   L12065  T=0 F=20  T=0 F=74  case XML_PARSER_ENTITY_VALUE:
  d=8   L12074  T=0 F=20  T=0 F=74  case XML_PARSER_ATTRIBUTE_VALUE:
  d=8   L12083  T=0 F=20  T=0 F=74  case XML_PARSER_SYSTEM_LITERAL:
  d=8   L12092  T=0 F=20  T=0 F=74  case XML_PARSER_PUBLIC_LITERAL:
--- d=7  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=7   L8396  T=0 F=6  T=0 F=30  if (name == NULL) {
  d=7   L8409  T=6 F=0  T=30 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=7   L8420  T=6 F=0  T=30 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=7   L8420  T=6 F=0  T=30 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=7   L8421  T=6 F=0  T=30 F=0  (!ctxt->disableSAX))
  d=7   L8423  T=0 F=6  T=0 F=30  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L8430  T=0 F=6  T=0 F=30  if (RAW == '[')
  d=7   L8436  T=0 F=6  T=0 F=30  if (RAW != '>') {
--- d=7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=7   L10816  T=0 F=2  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=7   L10816  T=0 F=2  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=7   L10829  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L10829  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=7   L10831  T=0 F=2  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10834  T=2 F=0  T=10 F=0  if ((ctxt->encoding == NULL) &&
  d=7   L10835  T=2 F=0  T=10 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=7   L10846  T=2 F=0  T=10 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=7   L10852  T=0 F=2  T=0 F=10  if (CUR == 0) {
  d=7   L10863  T=0 F=2  T=0 F=10  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=7   L10872  T=0 F=2  T=0 F=10  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=7   L10873  T=0 F=2  T=0 F=10  (ctxt->instate == XML_PARSER_EOF)) {
  d=7   L10884  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=7   L10884  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=7   L10884  T=2 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=7   L10886  T=0 F=2  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10888  T=2 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=7   L10888  T=2 F=0  T=10 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=7   L10889  T=2 F=0  T=10 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=7   L10889  T=0 F=2  T=0 F=10  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=7   L10907  T=0 F=2  T=0 F=10  if (RAW == '[') {
  d=7   L10918  T=2 F=0  T=10 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=7   L10918  T=2 F=0  T=10 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=7   L10919  T=2 F=0  T=10 F=0  (!ctxt->disableSAX))
  d=7   L10922  T=1 F=1  T=10 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10936  T=0 F=1  T=0 F=0  if (RAW != '<') {
  d=7   L10950  T=0 F=1  T=0 F=0  if (RAW != 0) {
  d=7   L10959  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L10959  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=7   L10965  T=1 F=0  T=0 F=0  if ((ctxt->myDoc != NULL) &&
  d=7   L10966  T=0 F=1  T=0 F=0  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=7   L10971  T=0 F=1  T=0 F=0  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=7   L10980  T=1 F=0  T=0 F=0  if (! ctxt->wellFormed) {
--- d=5  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=5   L7099  T=6 F=0  T=26 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L7100  T=6 F=0  T=26 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=5   L7109  T=0 F=6  T=0 F=26  if (enc != XML_CHAR_ENCODING_NONE)
  d=5   L7123  T=0 F=6  T=0 F=26  if (ctxt->myDoc == NULL) {
  d=5   L7131  T=0 F=6  T=0 F=26  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=5   L7131  T=6 F=0  T=26 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=5   L7137  T=21 F=0  T=86 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=5   L7137  T=18 F=3  T=86 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=5   L7139  T=15 F=0  T=60 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=5   L7139  T=15 F=3  T=60 F=26  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=5   L7139  T=0 F=15  T=0 F=60  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=5   L7141  T=15 F=3  T=60 F=26  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=5   L7141  T=15 F=0  T=60 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=5   L7151  T=0 F=3  T=0 F=0  if (RAW != 0) {
--- d=4  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=4   L6952  T=15 F=0  T=60 F=0  if (CUR == '<') {
  d=4   L6953  T=15 F=0  T=60 F=0  if (NXT(1) == '!') {
  d=4   L6955  T=12 F=3  T=50 F=10  case 'E':
  d=4   L6956  T=12 F=0  T=50 F=0  if (NXT(3) == 'L')
  d=4   L6963  T=3 F=12  T=10 F=50  case 'A':
  d=4   L6966  T=0 F=15  T=0 F=60  case 'N':
  d=4   L6969  T=0 F=15  T=0 F=60  case '-':
  d=4   L6972  T=0 F=15  T=0 F=60  default:
  d=4   L6986  T=0 F=15  T=0 F=60  if (ctxt->instate == XML_PARSER_EOF)
--- d=3  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169) ---
  d=3   L6064  T=0 F=3  T=0 F=10  if ((CUR != '<') || (NXT(1) != '!'))
  d=3   L6064  T=0 F=3  T=0 F=10  if ((CUR != '<') || (NXT(1) != '!'))
  d=3   L6072  T=0 F=3  T=2 F=5  if (SKIP_BLANKS == 0) {
  d=3   L6077  T=0 F=3  T=2 F=5  if (elemName == NULL) {
  d=3   L6084  T=9 F=3  T=5 F=0  while ((RAW != '>') && (ctxt->instate != XML_PARSER_EOF)) {
  d=3   L6098  T=0 F=9  T=2 F=3  if (SKIP_BLANKS == 0) {
  d=3   L6105  T=0 F=9  T=0 F=3  if (type <= 0) {
  d=3   L6110  T=0 F=9  T=0 F=3  if (SKIP_BLANKS == 0) {
  d=3   L6119  T=0 F=9  T=0 F=3  if (def <= 0) {
  d=3   L6126  T=3 F=0  T=0 F=0  if ((type != XML_ATTRIBUTE_CDATA) && (defaultValue != NULL))
  d=3   L6126  T=3 F=6  T=0 F=3  if ((type != XML_ATTRIBUTE_CDATA) && (defaultValue != NULL))
  d=3   L6130  T=6 F=3  T=3 F=0  if (RAW != '>') {
  d=3   L6131  T=0 F=6  T=3 F=0  if (SKIP_BLANKS == 0) {
  d=3   L6134  T=0 F=0  T=0 F=3  if (defaultValue != NULL)
  d=3   L6136  T=0 F=0  T=0 F=3  if (tree != NULL)
  d=3   L6141  T=9 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L6141  T=9 F=0  T=0 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=3   L6142  T=9 F=0  T=0 F=0  (ctxt->sax->attributeDecl != NULL))
  d=3   L6148  T=6 F=3  T=0 F=0  if ((ctxt->sax2) && (defaultValue != NULL) &&
  d=3   L6148  T=9 F=0  T=0 F=0  if ((ctxt->sax2) && (defaultValue != NULL) &&
  d=3   L6149  T=6 F=0  T=0 F=0  (def != XML_ATTRIBUTE_IMPLIED) &&
  d=3   L6150  T=6 F=0  T=0 F=0  (def != XML_ATTRIBUTE_REQUIRED)) {
  d=3   L6153  T=9 F=0  T=0 F=0  if (ctxt->sax2) {
  d=3   L6156  T=6 F=3  T=0 F=0  if (defaultValue != NULL)
  d=3   L6160  T=3 F=0  T=2 F=3  if (RAW == '>') {
--- d=2  parser.c:xmlAddDefAttrs  (/src/libxml2/parser.c:1194-1292) ---
  d=2   L1203  T=3 F=3  T=0 F=0  if (ctxt->attsSpecial != NULL) {
  d=2   L1204  T=0 F=3  T=0 F=0  if (xmlHashLookup2(ctxt->attsSpecial, fullname, fullattr)...
  d=2   L1208  T=3 F=3  T=0 F=0  if (ctxt->attsDefault == NULL) {
  d=2   L1210  T=0 F=3  T=0 F=0  if (ctxt->attsDefault == NULL)
  d=2   L1219  T=6 F=0  T=0 F=0  if (name == NULL) {
  d=2   L1231  T=3 F=3  T=0 F=0  if (defaults == NULL) {
  d=2   L1234  T=0 F=3  T=0 F=0  if (defaults == NULL)
  d=2   L1238  T=0 F=3  T=0 F=0  if (xmlHashUpdateEntry2(ctxt->attsDefault, name, prefix,
  d=2   L1243  T=0 F=3  T=0 F=0  } else if (defaults->nbAttrs >= defaults->maxAttrs) {
  d=2   L1264  T=6 F=0  T=0 F=0  if (name == NULL) {
  d=2   L1277  T=0 F=6  T=0 F=0  if (value == NULL)
  d=2   L1281  T=6 F=0  T=0 F=0  if (ctxt->external)
--- d=1  xmlSplitQName3  (/src/libxml2/tree.c:327-350) ---
  d=1   L 334  T=6 F=15  T=0 F=32  if (name[0] == ':')  <-- BLOCKER
  d=1   L 344  T=15 F=0  T=32 F=0  if (name[l] == 0)

[off-chain: 986 additional divergent branches across 99 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=518db8383db21f1c, size=380 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2856s, mutation_op=BytesRandInsertMutator,CrossoverInsertMutator,BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=dbcbbbf82365a7dd, size=368 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=5017s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 0a   .0"?>.<!DOCTYPE.
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00ec62cd667738b2, size=186 bytes, fuzzer=value_profile, trial=1, discovered_at=0s, mutation_op=BytesDeleteMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=0358b5c796e7e3e2, size=309 bytes, fuzzer=value_profile, trial=1, discovered_at=2s, mutation_op=BytesDeleteMutator,BytesSetMutator):
  0000: 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7772.xml\.<?xml 
  0010: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e   EM "dtds/127772.
Seed 3 (id=0a6c20087c76565d, size=368 bytes, fuzzer=value_profile, trial=1, discovered_at=102s, mutation_op=DwordAddMutator):
  0000: 06 00 00 00 31 25 37 37 37 32 2e 78 6d 6c 5c 0a   ....1%7772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=08de27acff869474, size=443 bytes, fuzzer=value_profile, trial=1, discovered_at=4030s, mutation_op=WordInterestingMutator,BytesExpandMutator,BytesSwapMutator,WordAddMutator):
  0000: 06 00 fd 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=065805d908a7c637, size=452 bytes, fuzzer=value_profile, trial=1, discovered_at=5625s, mutation_op=WordInterestingMutator,BytesExpandMutator,QwordAddMutator,ByteInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x2                             06(.)x4 45(E)x2 37(7)x1 3c(<)x1 +2u  PARTIAL
   0x0001  00(.)x2                             00(.)x4 44(D)x2 37(7)x1 22(")x1 +2u  PARTIAL
   0x0002  00(.)x2                             00(.)x3 20( )x2 37(7)x1 fd(.)x1 +3u  PARTIAL
   0x0003  00(.)x2                             00(.)x4 27(')x2 74(t)x2 32(2)x1 +1u  PARTIAL
   0x0004  31(1)x2                             31(1)x4 68(h)x2 74(t)x2 2e(.)x1 +1u  PARTIAL
   0x0005  32(2)x2                             32(2)x3 74(t)x2 70(p)x2 78(x)x1 +2u  PARTIAL
   0x0006  37(7)x2                             37(7)x4 74(t)x2 3a(:)x2 6d(m)x1 +1u  PARTIAL
   0x0007  37(7)x2                             37(7)x4 70(p)x2 2f(/)x2 6c(l)x1 +1u  PARTIAL
   0x0008  37(7)x2                             37(7)x4 3a(:)x2 2f(/)x2 5c(\)x1 +1u  PARTIAL
   0x0009  32(2)x2                             32(2)x4 2f(/)x2 66(f)x2 0a(.)x1 +1u  PARTIAL
   0x000a  2e(.)x2                             2e(.)x4 2f(/)x2 3c(<)x1 5e(^)x1 +2u  PARTIAL
   0x000b  78(x)x2                             78(x)x4 77(w)x2 6b(k)x2 3f(?)x1 +1u  PARTIAL
   0x000c  6d(m)x2                             6d(m)x4 77(w)x2 65(e)x2 78(x)x1 +1u  PARTIAL
   0x000d  6c(l)x2                             6c(l)x4 77(w)x2 75(u)x2 6d(m)x1 +1u  PARTIAL
   0x000e  5c(\)x2                             5c(\)x4 2e(.)x2 72(r)x2 6c(l)x1 +1u  PARTIAL
   0x000f  0a(.)x2                             0a(.)x4 77(w)x2 20( )x1 6c(l)x1 +2u  PARTIAL
   0x0010  3c(<)x2                             3c(<)x4 3d(=)x2 76(v)x1 2e(.)x1 +2u  PARTIAL
   0x0011  3f(?)x2                             3f(?)x4 2e(.)x2 65(e)x1 6e(n)x1 +2u  PARTIAL
   0x0012  78(x)x2                             78(x)x4 6f(o)x2 72(r)x1 65(e)x1 +2u  PARTIAL
   0x0013  6d(m)x2                             6d(m)x4 72(r)x2 73(s)x1 74(t)x1 +2u  PARTIAL
   0x0014  6c(l)x2                             6c(l)x4 67(g)x2 69(i)x1 22(")x1 +2u  PARTIAL
   0x0015  20( )x2                             20( )x4 2f(/)x2 6f(o)x1 3e(>)x1 +2u  PARTIAL
   0x0016  76(v)x2                             76(v)x4 31(1)x2 6e(n)x1 62(b)x1 +2u  PARTIAL
   0x0017  65(e)x2                             65(e)x4 3d(=)x2 39(9)x2 05(.)x1 +1u  PARTIAL
   0x0018  72(r)x2                             72(r)x4 22(")x2 39(9)x2 fd(.)x1 +1u  PARTIAL
   0x0019  73(s)x2                             73(s)x4 39(9)x2 31(1)x1 ff(.)x1 +2u  PARTIAL
   0x001a  69(i)x2                             69(i)x4 2f(/)x2 2e(.)x1 ff(.)x1 +2u  PARTIAL
   0x001b  6f(o)x2                             6f(o)x4 78(x)x2 30(0)x1 ff(.)x1 +2u  PARTIAL
   0x001c  6e(n)x2                             6e(n)x4 6c(l)x3 22(")x2 2f(/)x1     PARTIAL
   0x001d  3d(=)x2                             3d(=)x4 69(i)x2 3f(?)x1 74(t)x1 +2u  PARTIAL
   0x001e  22(")x2                             22(")x4 6e(n)x2 3e(>)x1 65(e)x1 +2u  PARTIAL
   0x001f  31(1)x2                             31(1)x4 6b(k)x2 0a(.)x1 78(x)x1 +2u  PARTIAL
   0x0020  2e(.)x2                             2e(.)x4 72(r)x3 3c(<)x1 74(t)x1 +1u  PARTIAL
   0x0021  30(0)x2                             30(0)x4 67(g)x2 21(!)x1 3c(<)x1 +2u  PARTIAL
   0x0022  22(")x2                             22(")x4 2f(/)x3 44(D)x1 69(i)x1 +1u  PARTIAL
   0x0023  3f(?)x2                             3f(?)x4 31(1)x2 4f(O)x1 62(b)x1 +2u  PARTIAL
   0x0024  3e(>)x2                             3e(>)x4 39(9)x2 43(C)x1 06(.)x1 +2u  PARTIAL
   0x0025  0a(.)x2                             0a(.)x4 39(9)x2 54(T)x1 00(.)x1 +2u  PARTIAL
   0x0026  3c(<)x2                             3c(<)x4 39(9)x2 59(Y)x1 00(.)x1 +2u  PARTIAL
   0x0027  21(!)x2                             21(!)x4 2f(/)x2 50(P)x1 00(.)x1 +2u  PARTIAL
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6910.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6910,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6910 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6910 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6910 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).