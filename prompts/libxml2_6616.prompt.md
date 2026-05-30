==== BLOCKER ====
Target: libxml2
Branch ID: 6616
Location: /src/libxml2/parser.c:5892:6
Enclosing function: xmlParseEnumerationType
Source line: 	if (name == NULL) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ctx_coverage vs naive_ctx)
cmplog                           7        3          0  REFERENCE
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     2        8          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        6        4          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=9.40h  loser=18.50h
  avg hitcount on branch: winner=9  loser=2
  prob_div=0.60  dur_div=9.10h  hit_div=7
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6616/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseEnumerationType (/src/libxml2/parser.c:5879-5930) ---
[ ]  5877  
[ ]  5878  xmlEnumerationPtr
[B]  5879  xmlParseEnumerationType(xmlParserCtxtPtr ctxt) {
[B]  5880      xmlChar *name;
[B]  5881      xmlEnumerationPtr ret = NULL, last = NULL, cur, tmp;
[ ]  5882  
[B]  5883      if (RAW != '(') {
[L]  5884  	xmlFatalErr(ctxt, XML_ERR_ATTLIST_NOT_STARTED, NULL);
[L]  5885  	return(NULL);
[L]  5886      }
[B]  5887      SHRINK;
[B]  5888      do {
[B]  5889          NEXT;
[B]  5890  	SKIP_BLANKS;
[B]  5891          name = xmlParseNmtoken(ctxt);
[B]  5892  	if (name == NULL) { <-- BLOCKER
[W]  5893  	    xmlFatalErr(ctxt, XML_ERR_NMTOKEN_REQUIRED, NULL);
[W]  5894  	    return(ret);
[W]  5895  	}
[B]  5896  	tmp = ret;
[B]  5897  	while (tmp != NULL) {
[ ]  5898  	    if (xmlStrEqual(name, tmp->name)) {
[ ]  5899  		xmlValidityError(ctxt, XML_DTD_DUP_TOKEN,
[ ]  5900  	  "standalone: attribute enumeration value token %s duplicated\n",
[ ]  5901  				 name, NULL);
[ ]  5902  		if (!xmlDictOwns(ctxt->dict, name))
[ ]  5903  		    xmlFree(name);
[ ]  5904  		break;
[ ]  5905  	    }
[ ]  5906  	    tmp = tmp->next;
[ ]  5907  	}
[B]  5908  	if (tmp == NULL) {
[B]  5909  	    cur = xmlCreateEnumeration(name);
[B]  5910  	    if (!xmlDictOwns(ctxt->dict, name))
[B]  5911  		xmlFree(name);
[B]  5912  	    if (cur == NULL) {
[ ]  5913                  xmlFreeEnumeration(ret);
[ ]  5914                  return(NULL);
[ ]  5915              }
[B]  5916  	    if (last == NULL) ret = last = cur;
[ ]  5917  	    else {
[ ]  5918  		last->next = cur;
[ ]  5919  		last = cur;
[ ]  5920  	    }
[B]  5921  	}
[B]  5922  	SKIP_BLANKS;
[B]  5923      } while (RAW == '|');
[B]  5924      if (RAW != ')') {
[L]  5925  	xmlFatalErr(ctxt, XML_ERR_ATTLIST_NOT_FINISHED, NULL);
[L]  5926  	return(ret);
[L]  5927      }
[B]  5928      NEXT;
[B]  5929      return(ret);
[B]  5930  }

--- Caller (1 hop): xmlParseEnumeratedType (/src/libxml2/parser.c:5950-5965, calls xmlParseEnumerationType at line 5962) (full body — short) ---
[B]  5950  xmlParseEnumeratedType(xmlParserCtxtPtr ctxt, xmlEnumerationPtr *tree) {
[B]  5951      if (CMP8(CUR_PTR, 'N', 'O', 'T', 'A', 'T', 'I', 'O', 'N')) {
[ ]  5952  	SKIP(8);
[ ]  5953  	if (SKIP_BLANKS == 0) {
[ ]  5954  	    xmlFatalErrMsg(ctxt, XML_ERR_SPACE_REQUIRED,
[ ]  5955  			   "Space required after 'NOTATION'\n");
[ ]  5956  	    return(0);
[ ]  5957  	}
[ ]  5958  	*tree = xmlParseNotationType(ctxt);
[ ]  5959  	if (*tree == NULL) return(0);
[ ]  5960  	return(XML_ATTRIBUTE_NOTATION);
[ ]  5961      }
[B]  5962      *tree = xmlParseEnumerationType(ctxt); <-- CALL
[B]  5963      if (*tree == NULL) return(0);
[B]  5964      return(XML_ATTRIBUTE_ENUMERATION);
[B]  5965  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseEnumeratedType  (/src/libxml2/parser.c:5950-5965, calls xmlParseEnumerationType at line 5962)
hop 3  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043, calls xmlParseEnumeratedType at line 6042)
hop 4  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169, calls xmlParseAttributeType at line 6104)
hop 5  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseAttributeListDecl at line 6964)
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
     168       543  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      45       243  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
       0       156  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
      45       170  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
      48       167  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
      48       161  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203)
      48       155  xmlParseAttValue  (/src/libxml2/parser.c:4229-4232)
      30       133  parser.c:xmlAddSpecialAttr  (/src/libxml2/parser.c:1308-1325)
      30       118  parser.c:xmlAddDefAttrs  (/src/libxml2/parser.c:1194-1292)
      20       108  parser.c:xmlCleanSpecialAttrCallback  (/src/libxml2/parser.c:1335-1341)
       0        73  parser.c:xmlGetNamespace  (/src/libxml2/parser.c:8856-8867)
       0        62  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
       0        52  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
      48         0  xmlParsePEReference  (/src/libxml2/parser.c:7999-8146)
      24        72  parser.c:xmlParseLookupGt  (/src/libxml2/parser.c:11194-11221)
... (31 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440) ---
  d=8   L8396  T=0 F=30  T=0 F=72  if (name == NULL) {
  d=8   L8409  T=30 F=0  T=72 F=0  if ((URI != NULL) || (ExternalID != NULL)) {
  d=8   L8420  T=30 F=0  T=72 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=8   L8420  T=30 F=0  T=72 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->internalSubset != ...
  d=8   L8421  T=30 F=0  T=72 F=0  (!ctxt->disableSAX))
  d=8   L8423  T=0 F=30  T=0 F=72  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L8430  T=0 F=30  T=0 F=72  if (RAW == '[')
  d=8   L8436  T=0 F=30  T=0 F=72  if (RAW != '>') {
--- d=8  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=8   L10816  T=0 F=10  T=0 F=24  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=8   L10816  T=0 F=10  T=0 F=24  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=8   L10829  T=10 F=0  T=24 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L10829  T=10 F=0  T=24 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=8   L10831  T=0 F=10  T=0 F=24  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L10834  T=10 F=0  T=24 F=0  if ((ctxt->encoding == NULL) &&
  d=8   L10835  T=10 F=0  T=24 F=0  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=8   L10846  T=10 F=0  T=24 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=8   L10852  T=0 F=10  T=0 F=24  if (CUR == 0) {
  d=8   L10863  T=0 F=10  T=0 F=24  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=8   L10872  T=0 F=10  T=0 F=23  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=8   L10873  T=0 F=10  T=0 F=23  (ctxt->instate == XML_PARSER_EOF)) {
  d=8   L10884  T=10 F=0  T=24 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=8   L10884  T=10 F=0  T=24 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=8   L10884  T=10 F=0  T=24 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=8   L10886  T=0 F=10  T=0 F=24  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L10888  T=10 F=0  T=24 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=8   L10888  T=10 F=0  T=24 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=8   L10889  T=10 F=0  T=24 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=8   L10889  T=0 F=10  T=0 F=24  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=8   L10907  T=0 F=10  T=0 F=24  if (RAW == '[') {
  d=8   L10918  T=10 F=0  T=24 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=8   L10918  T=10 F=0  T=24 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=8   L10919  T=10 F=0  T=24 F=0  (!ctxt->disableSAX))
  d=8   L10922  T=9 F=1  T=15 F=9  if (ctxt->instate == XML_PARSER_EOF)
  d=8   L10936  T=0 F=1  T=0 F=9  if (RAW != '<') {
  d=8   L10950  T=0 F=1  T=4 F=5  if (RAW != 0) {
  d=8   L10959  T=1 F=0  T=9 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L10959  T=1 F=0  T=9 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=8   L10965  T=1 F=0  T=9 F=0  if ((ctxt->myDoc != NULL) &&
  d=8   L10966  T=0 F=1  T=0 F=9  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=8   L10971  T=0 F=1  T=0 F=9  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=8   L10980  T=1 F=0  T=9 F=0  if (! ctxt->wellFormed) {
--- d=6  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=6   L7099  T=30 F=0  T=69 F=0  if ((ctxt->encoding == NULL) &&
  d=6   L7100  T=30 F=0  T=69 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=6   L7109  T=0 F=30  T=0 F=69  if (enc != XML_CHAR_ENCODING_NONE)
  d=6   L7123  T=0 F=30  T=0 F=69  if (ctxt->myDoc == NULL) {
  d=6   L7131  T=0 F=30  T=0 F=69  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=6   L7131  T=30 F=0  T=69 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=6   L7137  T=126 F=0  T=277 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=6   L7137  T=123 F=3  T=253 F=24  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=6   L7139  T=96 F=0  T=208 F=3  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=6   L7139  T=96 F=27  T=211 F=42  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=6   L7139  T=0 F=96  T=0 F=208  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=6   L7141  T=0 F=0  T=0 F=3  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=6   L7141  T=96 F=27  T=211 F=42  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=6   L7141  T=96 F=0  T=208 F=3  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=6   L7151  T=0 F=3  T=0 F=24  if (RAW != 0) {
--- d=5  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990) ---
  d=5   L6952  T=96 F=0  T=208 F=0  if (CUR == '<') {
  d=5   L6953  T=96 F=0  T=208 F=0  if (NXT(1) == '!') {
  d=5   L6955  T=66 F=30  T=138 F=70  case 'E':
  d=5   L6956  T=66 F=0  T=138 F=0  if (NXT(3) == 'L')
  d=5   L6963  T=30 F=66  T=70 F=138  case 'A':
  d=5   L6966  T=0 F=96  T=0 F=208  case 'N':
  d=5   L6969  T=0 F=96  T=0 F=208  case '-':
  d=5   L6972  T=0 F=96  T=0 F=208  default:
  d=5   L6986  T=0 F=96  T=0 F=208  if (ctxt->instate == XML_PARSER_EOF)
--- d=4  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169) ---
  d=4   L6064  T=0 F=30  T=0 F=70  if ((CUR != '<') || (NXT(1) != '!'))
  d=4   L6064  T=0 F=30  T=0 F=70  if ((CUR != '<') || (NXT(1) != '!'))
  d=4   L6072  T=0 F=30  T=1 F=69  if (SKIP_BLANKS == 0) {
  d=4   L6077  T=0 F=30  T=1 F=69  if (elemName == NULL) {
  d=4   L6084  T=75 F=0  T=191 F=0  while ((RAW != '>') && (ctxt->instate != XML_PARSER_EOF)) {
  d=4   L6084  T=75 F=0  T=191 F=15  while ((RAW != '>') && (ctxt->instate != XML_PARSER_EOF)) {
  d=4   L6092  T=0 F=75  T=11 F=180  if (attrName == NULL) {
  d=4   L6098  T=0 F=75  T=3 F=177  if (SKIP_BLANKS == 0) {
  d=4   L6105  T=30 F=45  T=6 F=171  if (type <= 0) {
  d=4   L6110  T=0 F=45  T=1 F=170  if (SKIP_BLANKS == 0) {
  d=4   L6113  T=0 F=0  T=1 F=0  if (tree != NULL)
  d=4   L6119  T=0 F=45  T=0 F=170  if (def <= 0) {
  d=4   L6126  T=15 F=0  T=62 F=6  if ((type != XML_ATTRIBUTE_CDATA) && (defaultValue != NULL))
  d=4   L6126  T=15 F=30  T=68 F=102  if ((type != XML_ATTRIBUTE_CDATA) && (defaultValue != NULL))
  d=4   L6130  T=45 F=0  T=155 F=15  if (RAW != '>') {
  d=4   L6131  T=0 F=45  T=33 F=122  if (SKIP_BLANKS == 0) {
  d=4   L6134  T=0 F=0  T=9 F=24  if (defaultValue != NULL)
  d=4   L6136  T=0 F=0  T=15 F=18  if (tree != NULL)
  d=4   L6141  T=45 F=0  T=137 F=0  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=4   L6141  T=30 F=15  T=85 F=52  if ((ctxt->sax != NULL) && (!ctxt->disableSAX) &&
  d=4   L6142  T=30 F=0  T=85 F=0  (ctxt->sax->attributeDecl != NULL))
  d=4   L6145  T=6 F=9  T=21 F=31  else if (tree != NULL)
  d=4   L6148  T=30 F=0  T=118 F=15  if ((ctxt->sax2) && (defaultValue != NULL) &&
  d=4   L6148  T=30 F=15  T=133 F=4  if ((ctxt->sax2) && (defaultValue != NULL) &&
  d=4   L6149  T=30 F=0  T=118 F=0  (def != XML_ATTRIBUTE_IMPLIED) &&
  d=4   L6150  T=30 F=0  T=118 F=0  (def != XML_ATTRIBUTE_REQUIRED)) {
  d=4   L6153  T=30 F=15  T=133 F=4  if (ctxt->sax2) {
  d=4   L6156  T=45 F=0  T=122 F=15  if (defaultValue != NULL)
  d=4   L6160  T=0 F=30  T=15 F=54  if (RAW == '>') {
  d=4   L6161  T=0 F=0  T=0 F=15  if (inputid != ctxt->input->id) {
--- d=1  xmlParseEnumerationType  (/src/libxml2/parser.c:5879-5930) ---
  d=1   L5883  T=0 F=45  T=6 F=69  if (RAW != '(') {
  d=1   L5892  T=30 F=15  T=0 F=69  if (name == NULL) {  <-- BLOCKER
  d=1   L5897  T=0 F=15  T=0 F=69  while (tmp != NULL) {
  d=1   L5908  T=15 F=0  T=69 F=0  if (tmp == NULL) {
  d=1   L5910  T=15 F=0  T=69 F=0  if (!xmlDictOwns(ctxt->dict, name))
  d=1   L5912  T=0 F=15  T=0 F=69  if (cur == NULL) {
  d=1   L5916  T=15 F=0  T=69 F=0  if (last == NULL) ret = last = cur;
  d=1   L5923  T=0 F=15  T=0 F=69  } while (RAW == '|');
  d=1   L5924  T=0 F=15  T=1 F=68  if (RAW != ')') {

[off-chain: 910 additional divergent branches across 81 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=00ea7e66e00573c5, size=519 bytes, fuzzer=naive_ctx, trial=1, discovered_at=0s, mutation_op=BytesExpandMutator,CrossoverInsertMutator,ByteNegMutator,BytesSetMutator,BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=adf73de9c553f571, size=756 bytes, fuzzer=naive_ctx, trial=1, discovered_at=712s, mutation_op=BytesCopyMutator,TokenReplace,ByteInterestingMutator,TokenInsert):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 06 00 00 00 31   ....127772.....1
  0010: 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c   27772.xml\.<?xml
  0020: 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e    version="1.0"?>
  0030: 0a 3c 21 44 4f 43 54 59 50 45 42 61 20 53 59 53   .<!DOCTYPEBa SYS
Seed 3 (id=7e5b8381a25e9da7, size=293 bytes, fuzzer=naive_ctx, trial=1, discovered_at=1219s, mutation_op=BytesDeleteMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
Seed 4 (id=5490d017a729e344, size=782 bytes, fuzzer=naive_ctx, trial=1, discovered_at=2627s, mutation_op=CrossoverInsertMutator,TokenReplace,BytesInsertCopyMutator,BytesRandSetMutator):
  0000: 06 00 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 5c 0a   ..............\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 42   .0"?>.<!DOCTYPEB
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=a04d19468f4fe66a, size=348 bytes, fuzzer=naive_ctx, trial=1, discovered_at=3528s, mutation_op=TokenReplace,ByteInterestingMutator,BytesSetMutator,DwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=178d47227f124563, size=317 bytes, fuzzer=naive, trial=1, discovered_at=3s, mutation_op=WordInterestingMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=08c59e3361d9781a, size=559 bytes, fuzzer=naive, trial=1, discovered_at=5s, mutation_op=BytesInsertCopyMutator,TokenReplace,BytesSetMutator,BytesInsertMutator):
  0000: 6e 65 8b 22 3e 62 20 74 65 78 6d 6c 5c 0a 3c 3f   ne.">b texml\.<?
  0010: 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30   xml version="1.0
  0020: 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20   "?>.<!DOCTYPE a 
  0030: 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37   SYSTEM "dtds/127
Seed 3 (id=5fc4f2e61808d2a4, size=395 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=BytesInsertCopyMutator,ByteFlipMutator,BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=5b6ae456dcd36093, size=519 bytes, fuzzer=naive, trial=2, discovered_at=34s, mutation_op=QwordAddMutator,TokenReplace,BytesInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 6c 20   <?xm..........l 
  0020: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0030: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
Seed 5 (id=491e10d6ee916429, size=368 bytes, fuzzer=naive, trial=2, discovered_at=38s, mutation_op=BytesSetMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  32(2)x7 6c(l)x1 a3(.)x1 78(x)x1     32(2)x14 62(b)x4 f9(.)x1 2c(,)x1 +4u  PARTIAL
   0x001a  69(i)x6 22(")x2 0a(.)x1 2e(.)x1     69(i)x13 6e(n)x4 2e(.)x1 72(r)x1 +5u  PARTIAL
   0x001e  22(")x7 6d(m)x1 3c(<)x1 3e(>)x1     22(")x13 2e(.)x4 6c(l)x1 6e(n)x1 +5u  PARTIAL
   0x0029  4f(O)x6 20( )x2 22(")x1 50(P)x1     4f(O)x13 54(T)x4 31(1)x1 21(!)x1 +5u  PARTIAL
   0x002b  54(T)x6 20( )x2 2e(.)x1 59(Y)x1     54(T)x13 50(P)x4 30(0)x1 4f(O)x1 +5u  PARTIAL
   0x002c  59(Y)x6 53(S)x2 30(0)x1 61(a)x1     59(Y)x13 45(E)x4 2f(/)x2 22(")x1 +4u  PARTIAL
   0x002e  45(E)x7 53(S)x2 3f(?)x1             45(E)x13 61(a)x4 3e(>)x1 59(Y)x1 +5u  PARTIAL
   0x0034  53(S)x6 64(d)x2 4f(O)x1 20( )x1     53(S)x14 45(E)x4 43(C)x1 2f(/)x1 +4u  PARTIAL
   0x0036  45(E)x6 64(d)x2 54(T)x1 2f(/)x1     45(E)x13 20( )x4 59(Y)x1 53(S)x1 +5u  PARTIAL
   0x003b  74(t)x6 37(7)x2 61(a)x1 31(1)x1     74(t)x13 73(s)x4 20( )x2 22(")x1 +4u  PARTIAL
   0x003c  64(d)x6 32(2)x2 20( )x1 37(7)x1     64(d)x14 2f(/)x4 53(S)x1 3a(:)x1 +4u  PARTIAL
   0x003d  73(s)x6 37(7)x2 53(S)x1 2e(.)x1     73(s)x13 31(1)x4 59(Y)x1 74(t)x1 +5u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6616.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6616,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6616 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6616 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6616 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).