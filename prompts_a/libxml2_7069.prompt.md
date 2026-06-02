==== BLOCKER ====
Target: libxml2
Branch ID: 7069
Location: /src/libxml2/valid.c:1125:13
Enclosing function: xmlFreeDocElementContent
Source line:         if (cur == parent->c1)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        3          5  REFERENCE
cmplog                           0        9          1  loser (value_profile vs value_profile_cmplog); loser (grimoire_structural vs grimoire)
value_profile                    8        2          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        2        5          3  REFERENCE
naive_ngram4                     0        2          8  REFERENCE
mopt                             0        1          9  REFERENCE
minimizer                        2        1          7  REFERENCE
fast                             2        0          8  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=9  unreached=1
  avg duration blocked: winner=8.20h  loser=17.11h
  avg hitcount on branch: winner=6  loser=0
  prob_div=0.80  dur_div=8.91h  hit_div=6
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 2: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=9  unreached=1
  avg duration blocked: winner=10.70h  loser=17.11h
  avg hitcount on branch: winner=63  loser=0
  prob_div=0.80  dur_div=6.41h  hit_div=63
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7069/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlFreeDocElementContent (/src/libxml2/valid.c:1082-1138) ---
[ ]  1080   */
[ ]  1081  void
[B]  1082  xmlFreeDocElementContent(xmlDocPtr doc, xmlElementContentPtr cur) {
[B]  1083      xmlDictPtr dict = NULL;
[B]  1084      size_t depth = 0;
[ ]  1085  
[B]  1086      if (cur == NULL)
[ ]  1087          return;
[B]  1088      if (doc != NULL)
[B]  1089          dict = doc->dict;
[ ]  1090  
[B]  1091      while (1) {
[B]  1092          xmlElementContentPtr parent;
[ ]  1093  
[B]  1094          while ((cur->c1 != NULL) || (cur->c2 != NULL)) {
[B]  1095              cur = (cur->c1 != NULL) ? cur->c1 : cur->c2;
[B]  1096              depth += 1;
[B]  1097          }
[ ]  1098  
[B]  1099  	switch (cur->type) {
[L]  1100  	    case XML_ELEMENT_CONTENT_PCDATA:
[B]  1101  	    case XML_ELEMENT_CONTENT_ELEMENT:
[B]  1102  	    case XML_ELEMENT_CONTENT_SEQ:
[B]  1103  	    case XML_ELEMENT_CONTENT_OR:
[B]  1104  		break;
[ ]  1105  	    default:
[ ]  1106  		xmlErrValid(NULL, XML_ERR_INTERNAL_ERROR,
[ ]  1107  			"Internal: ELEMENT content corrupted invalid type\n",
[ ]  1108  			NULL);
[ ]  1109  		return;
[B]  1110  	}
[B]  1111  	if (dict) {
[L]  1112  	    if ((cur->name != NULL) && (!xmlDictOwns(dict, cur->name)))
[ ]  1113  	        xmlFree((xmlChar *) cur->name);
[L]  1114  	    if ((cur->prefix != NULL) && (!xmlDictOwns(dict, cur->prefix)))
[ ]  1115  	        xmlFree((xmlChar *) cur->prefix);
[B]  1116  	} else {
[B]  1117  	    if (cur->name != NULL) xmlFree((xmlChar *) cur->name);
[B]  1118  	    if (cur->prefix != NULL) xmlFree((xmlChar *) cur->prefix);
[B]  1119  	}
[B]  1120          parent = cur->parent;
[B]  1121          if ((depth == 0) || (parent == NULL)) {
[B]  1122              xmlFree(cur);
[B]  1123              break;
[B]  1124          }
[B]  1125          if (cur == parent->c1) <-- BLOCKER
[B]  1126              parent->c1 = NULL;
[W]  1127          else
[W]  1128              parent->c2 = NULL;
[B]  1129  	xmlFree(cur);
[ ]  1130  
[B]  1131          if (parent->c2 != NULL) {
[W]  1132  	    cur = parent->c2;
[B]  1133          } else {
[B]  1134              depth -= 1;
[B]  1135              cur = parent;
[B]  1136          }
[B]  1137      }
[B]  1138  }

--- Caller (1 hop): valid.c:xmlFreeElement (/src/libxml2/valid.c:1382-1395, calls xmlFreeDocElementContent at line 1385) (full body — short) ---
[W]  1382  xmlFreeElement(xmlElementPtr elem) {
[W]  1383      if (elem == NULL) return;
[W]  1384      xmlUnlinkNode((xmlNodePtr) elem);
[W]  1385      xmlFreeDocElementContent(elem->doc, elem->content); <-- CALL
[W]  1386      if (elem->name != NULL)
[W]  1387  	xmlFree((xmlChar *) elem->name);
[W]  1388      if (elem->prefix != NULL)
[ ]  1389  	xmlFree((xmlChar *) elem->prefix);
[W]  1390  #ifdef LIBXML_REGEXP_ENABLED
[W]  1391      if (elem->contModel != NULL)
[W]  1392  	xmlRegFreeRegexp(elem->contModel);
[W]  1393  #endif
[W]  1394      xmlFree(elem);
[W]  1395  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseElementMixedContentDecl  (/src/libxml2/parser.c:6193-6284, calls xmlFreeDocElementContent at line 6227)
hop 3  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675, calls xmlParseElementMixedContentDecl at line 6666)
hop 4  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788, calls xmlParseElementContentDecl at line 6736)
hop 5  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseElementDecl at line 6957)
hop 6  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 6  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 7  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 7  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 7  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 8  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 8  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 8  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     159      1030  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      96       756  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     106       552  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      18       144  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       0        66  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
       9        54  inputPop  (/src/libxml2/parser.c:1723-1738)
      12        54  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
       6        45  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
       0        33  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       6        36  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
       6        36  inputPush  (/src/libxml2/parser.c:1693-1712)
      28         0  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
       6        33  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
       6        33  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
       6        33  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)  <-- enclosing
... (89 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=8   L8396  T=0 F=3  T=0 F=18  if (name == NULL) {
  d=8   L8409  T=3 F=0  T=18 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=8   L8420  T=3 F=0  T=18 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=8   L8420  T=3 F=0  T=18 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=8   L8421  T=3 F=0  T=18 F=0  (!ctxt->disableSAX))
  d=8   L8423  T=0 F=3  T=0 F=18  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L8430  T=0 F=3  T=0 F=18  if (RAW == '[')
  d=8   L8436  T=0 F=3  T=0 F=18  if (RAW != '>') {
--- d=8  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=8   L10816  T=0 F=1  T=0 F=6  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=8   L10816  T=0 F=1  T=0 F=6  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=8   L10829  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L10829  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L10831  T=0 F=1  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L10834  T=1 F=0  T=6 F=0  if ((ctxt->encoding == NULL) &&
  d=8   L10835  T=1 F=0  T=6 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=8   L10846  T=1 F=0  T=6 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=8   L10852  T=0 F=1  T=0 F=6  if (CUR == 0) {
  d=8   L10863  T=0 F=1  T=0 F=6  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=8   L10872  T=0 F=1  T=0 F=6  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=8   L10873  T=0 F=1  T=0 F=6  (ctxt->instate == XML_PARSER_EOF)) {
  d=8   L10884  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=8   L10884  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=8   L10884  T=1 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=8   L10886  T=0 F=1  T=0 F=6  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L10888  T=1 F=0  T=6 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=8   L10888  T=1 F=0  T=6 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=8   L10889  T=1 F=0  T=6 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=8   L10889  T=0 F=1  T=0 F=6  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=8   L10907  T=0 F=1  T=0 F=6  if (RAW == '[') {
  d=8   L10918  T=1 F=0  T=6 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=8   L10918  T=1 F=0  T=6 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=8   L10919  T=1 F=0  T=6 F=0  (!ctxt->disableSAX))
  d=8   L10922  T=0 F=1  T=6 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L10936  T=0 F=1  T=0 F=0  if (RAW != '<') {
  d=8   L10950  T=0 F=1  T=0 F=0  if (RAW != 0) {
  d=8   L10959  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L10959  T=1 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L10965  T=1 F=0  T=0 F=0  if ((ctxt->myDoc != NULL) &&
  d=8   L10966  T=0 F=1  T=0 F=0  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=8   L10971  T=1 F=0  T=0 F=0  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=8   L10971  T=1 F=0  T=0 F=0  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=8   L10973  T=0 F=1  T=0 F=0  if (ctxt->valid)
  d=8   L10975  T=0 F=1  T=0 F=0  if (ctxt->nsWellFormed)
  d=8   L10977  T=0 F=1  T=0 F=0  if (ctxt->options & XML_PARSE_OLD10)
  d=8   L10980  T=0 F=1  T=0 F=0  if (! ctxt->wellFormed) {
--- d=6  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=6   L7099  T=3 F=0  T=18 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L7100  T=3 F=0  T=18 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=6   L7109  T=0 F=3  T=0 F=18  if (enc != XML_CHAR_ENCODING_NONE)
  d=6   L7123  T=0 F=3  T=0 F=18  if (ctxt->myDoc == NULL) {
  d=6   L7131  T=0 F=3  T=0 F=18  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=6   L7131  T=3 F=0  T=18 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=6   L7137  T=9 F=0  T=63 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=6   L7137  T=6 F=3  T=63 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=6   L7139  T=6 F=0  T=45 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=6   L7139  T=6 F=0  T=45 F=18  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=6   L7139  T=0 F=6  T=0 F=45  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=6   L7141  T=6 F=0  T=45 F=18  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=6   L7141  T=6 F=0  T=45 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=6   L7151  T=0 F=3  T=0 F=0  if (RAW != 0) {
--- d=5  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=5   L6952  T=6 F=0  T=45 F=0  if (CUR == '<') {
  d=5   L6953  T=6 F=0  T=45 F=0  if (NXT(1) == '!') {
  d=5   L6955  T=6 F=0  T=33 F=12  case 'E':
  d=5   L6956  T=6 F=0  T=33 F=0  if (NXT(3) == 'L')
  d=5   L6963  T=0 F=6  T=12 F=33  case 'A':
  d=5   L6966  T=0 F=6  T=0 F=45  case 'N':
  d=5   L6969  T=0 F=6  T=0 F=45  case '-':
  d=5   L6972  T=0 F=6  T=0 F=45  default:
  d=5   L6986  T=0 F=6  T=0 F=45  if (ctxt->instate == XML_PARSER_EOF)
--- d=4  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788) ---
  d=4   L6698  T=0 F=6  T=0 F=33  if ((CUR != '<') || (NXT(1) != '!'))
  d=4   L6698  T=0 F=6  T=0 F=33  if ((CUR != '<') || (NXT(1) != '!'))
  d=4   L6707  T=0 F=6  T=0 F=33  if (SKIP_BLANKS == 0) {
  d=4   L6713  T=0 F=6  T=0 F=33  if (name == NULL) {
  d=4   L6718  T=0 F=6  T=0 F=33  if (SKIP_BLANKS == 0) {
  d=4   L6728  T=0 F=6  T=0 F=33  } else if ((RAW == 'A') && (NXT(1) == 'N') &&
  d=4   L6735  T=6 F=0  T=33 F=0  } else if (RAW == '(') {
  d=4   L6754  T=0 F=6  T=6 F=27  if (RAW != '>') {
  d=4   L6756  T=0 F=0  T=0 F=6  if (content != NULL) {
  d=4   L6760  T=0 F=6  T=0 F=27  if (inputid != ctxt->input->id) {
  d=4   L6767  T=6 F=0  T=27 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=4   L6767  T=6 F=0  T=3 F=24  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=4   L6768  T=6 F=0  T=3 F=0  (ctxt->sax->elementDecl != NULL)) {
  d=4   L6769  T=6 F=0  T=0 F=3  if (content != NULL)
  d=4   L6773  T=6 F=0  T=0 F=3  if ((content != NULL) && (content->parent == NULL)) {
  d=4   L6773  T=0 F=6  T=0 F=0  if ((content != NULL) && (content->parent == NULL)) {
  d=4   L6782  T=0 F=0  T=3 F=21  } else if (content != NULL) {
--- d=3  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675) ---
  d=3   L6655  T=0 F=6  T=0 F=33  if (RAW != '(') {
  d=3   L6662  T=0 F=6  T=0 F=33  if (ctxt->instate == XML_PARSER_EOF)
--- d=2  xmlParseElementMixedContentDecl  (/src/libxml2/parser.c:6193-6284) ---
  d=2   L6202  T=0 F=0  T=3 F=6  if (RAW == ')') {
  d=2   L6203  T=0 F=0  T=0 F=3  if (ctxt->input->id != inputchk) {
  d=2   L6210  T=0 F=0  T=0 F=3  if (ret == NULL)
  d=2   L6212  T=0 F=0  T=0 F=3  if (RAW == '*') {
  d=2   L6218  T=0 F=0  T=0 F=6  if ((RAW == '(') || (RAW == '|')) {
  d=2   L6218  T=0 F=0  T=6 F=0  if ((RAW == '(') || (RAW == '|')) {
  d=2   L6220  T=0 F=0  T=0 F=6  if (ret == NULL) return(NULL);
  d=2   L6222  T=0 F=0  T=6 F=0  while ((RAW == '|') && (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L6222  T=0 F=0  T=6 F=0  while ((RAW == '|') && (ctxt->instate != XML_PARSER_EOF)) {
  d=2   L6224  T=0 F=0  T=6 F=0  if (elem == NULL) {
  d=2   L6226  T=0 F=0  T=0 F=6  if (ret == NULL) {
  d=2   L6231  T=0 F=0  T=6 F=0  if (cur != NULL)
  d=2   L6250  T=0 F=0  T=6 F=0  if (elem == NULL) {
--- d=1  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138) ---
  d=1   L1086  T=0 F=6  T=0 F=33  if (cur == NULL)
  d=1   L1088  T=6 F=0  T=33 F=0  if (doc != NULL)
  d=1   L1094  T=0 F=12  T=0 F=54  while ((cur->c1 != NULL) || (cur->c2 != NULL)) {
  d=1   L1094  T=3 F=12  T=21 F=54  while ((cur->c1 != NULL) || (cur->c2 != NULL)) {
  d=1   L1095  T=3 F=0  T=21 F=0  cur = (cur->c1 != NULL) ? cur->c1 : cur->c2;
  d=1   L1100  T=0 F=12  T=9 F=45  case XML_ELEMENT_CONTENT_PCDATA:
  d=1   L1101  T=9 F=3  T=24 F=30  case XML_ELEMENT_CONTENT_ELEMENT:
  d=1   L1102  T=0 F=12  T=6 F=48  case XML_ELEMENT_CONTENT_SEQ:
  d=1   L1103  T=3 F=9  T=15 F=39  case XML_ELEMENT_CONTENT_OR:
  d=1   L1105  T=0 F=12  T=0 F=54  default:
  d=1   L1111  T=0 F=12  T=48 F=6  if (dict) {
  d=1   L1112  T=0 F=0  T=0 F=21  if ((cur->name != NULL) && (!xmlDictOwns(dict, cur->name)))
  d=1   L1112  T=0 F=0  T=21 F=27  if ((cur->name != NULL) && (!xmlDictOwns(dict, cur->name)))
  d=1   L1114  T=0 F=0  T=0 F=48  if ((cur->prefix != NULL) && (!xmlDictOwns(dict, cur->pre...
  d=1   L1117  T=9 F=3  T=3 F=3  if (cur->name != NULL) xmlFree((xmlChar *) cur->name);
  d=1   L1118  T=0 F=12  T=0 F=6  if (cur->prefix != NULL) xmlFree((xmlChar *) cur->prefix);
  d=1   L1121  T=6 F=6  T=33 F=21  if ((depth == 0) || (parent == NULL)) {
  d=1   L1121  T=0 F=6  T=0 F=21  if ((depth == 0) || (parent == NULL)) {
  d=1   L1125  T=3 F=3  T=21 F=0  if (cur == parent->c1)  <-- BLOCKER
  d=1   L1131  T=3 F=3  T=0 F=21  if (parent->c2 != NULL) {

[off-chain: 1051 additional divergent branches across 97 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=ae2d760d094b65d2, size=348 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=48779s, mutation_op=BytesInsertCopyMutator,DwordInterestingMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 74 74 70 3a 40 2f 55 77 77 2b 77 33 2e 6f 72 67   ttp:@/Uww+w3.org
  0010: 2f 31 0a 39 39 2f 78 6c 69 6e 6b 27 0a 21 20 20   /1.99/xlink'.!  
  0020: 9f 20 28 20 20 20 20 20 20 78 9f 24 8c 8c 8c 8c   . (      x.$....
  0030: 8c 8c 8c 8c 8c 8c 8c 78 6d 6c 6e 73 3a 78 6c 69   .......xmlns:xli

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=a3057bec1d93edff, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=271s, mutation_op=ByteIncMutator,CrossoverInsertMutator,TokenReplace,WordInterestingMutator,ByteDecMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=dc7cd90ae5b5f946, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=271s, mutation_op=ByteIncMutator,CrossoverInsertMutator,TokenReplace,WordInterestingMutator,ByteDecMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=92ef089df3591385, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=4017s, mutation_op=ByteIncMutator,BytesSetMutator,BytesSwapMutator,BytesSwapMutator,BytesDeleteMutator,BytesSwapMutator,ByteNegMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=db880535c7727f82, size=385 bytes, fuzzer=cmplog, trial=1, discovered_at=4074s, mutation_op=BytesInsertCopyMutator,BytesRandInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=03c5006cca4defe0, size=339 bytes, fuzzer=cmplog, trial=1, discovered_at=5448s, mutation_op=ByteFlipMutator,WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 31 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .1"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  74(t)x1                             06(.)x5 37(7)x1                     DIFFER
   0x0001  74(t)x1                             00(.)x5 37(7)x1                     DIFFER
   0x0002  70(p)x1                             00(.)x5 32(2)x1                     DIFFER
   0x0003  3a(:)x1                             00(.)x5 2e(.)x1                     DIFFER
   0x0004  40(@)x1                             31(1)x5 78(x)x1                     DIFFER
   0x0005  2f(/)x1                             32(2)x5 6d(m)x1                     DIFFER
   0x0006  55(U)x1                             37(7)x5 ff(.)x1                     DIFFER
   0x0007  77(w)x1                             37(7)x5 ff(.)x1                     DIFFER
   0x0008  77(w)x1                             37(7)x5 ff(.)x1                     DIFFER
   0x0009  2b(+)x1                             32(2)x5 3f(?)x1                     DIFFER
   0x000a  77(w)x1                             2e(.)x5 3f(?)x1                     DIFFER
   0x000b  33(3)x1                             78(x)x6                             DIFFER
   0x000c  2e(.)x1                             6d(m)x6                             DIFFER
   0x000d  6f(o)x1                             6c(l)x6                             DIFFER
   0x000e  72(r)x1                             5c(\)x5 20( )x1                     DIFFER
   0x000f  67(g)x1                             0a(.)x5 76(v)x1                     DIFFER
   0x0010  2f(/)x1                             3c(<)x5 65(e)x1                     DIFFER
   0x0011  31(1)x1                             3f(?)x5 72(r)x1                     DIFFER
   0x0012  0a(.)x1                             78(x)x5 73(s)x1                     DIFFER
   0x0013  39(9)x1                             6d(m)x5 69(i)x1                     DIFFER
   0x0014  39(9)x1                             6c(l)x5 6f(o)x1                     DIFFER
   0x0015  2f(/)x1                             20( )x5 6e(n)x1                     DIFFER
   0x0016  78(x)x1                             76(v)x5 3d(=)x1                     DIFFER
   0x0017  6c(l)x1                             65(e)x5 22(")x1                     DIFFER
   0x0018  69(i)x1                             72(r)x5 31(1)x1                     DIFFER
   0x0019  6e(n)x1                             73(s)x5 2e(.)x1                     DIFFER
   0x001a  6b(k)x1                             69(i)x5 30(0)x1                     DIFFER
   0x001b  27(')x1                             6f(o)x5 22(")x1                     DIFFER
   0x001c  0a(.)x1                             6e(n)x5 3f(?)x1                     DIFFER
   0x001d  21(!)x1                             3d(=)x5 3e(>)x1                     DIFFER
   0x001e  20( )x1                             22(")x5 0a(.)x1                     DIFFER
   0x001f  20( )x1                             31(1)x5 3c(<)x1                     DIFFER
   0x0020  9f(.)x1                             2e(.)x5 21(!)x1                     DIFFER
   0x0021  20( )x1                             30(0)x4 31(1)x1 fb(.)x1             DIFFER
   0x0022  28(()x1                             22(")x5 fb(.)x1                     DIFFER
   0x0023  20( )x1                             3f(?)x5 fb(.)x1                     DIFFER
   0x0024  20( )x1                             3e(>)x5 fb(.)x1                     DIFFER
   0x0025  20( )x1                             0a(.)x5 fb(.)x1                     DIFFER
   0x0026  20( )x1                             3c(<)x5 fb(.)x1                     DIFFER
   0x0027  20( )x1                             21(!)x5 fb(.)x1                     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7069.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7069,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7069 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7069 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7069 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).