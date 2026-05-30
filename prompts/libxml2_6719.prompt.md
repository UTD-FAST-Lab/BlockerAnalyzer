==== BLOCKER ====
Target: libxml2
Branch ID: 6719
Location: /src/libxml2/parser.c:8986:9
Enclosing function: parser.c:xmlParseQNameAndCompare
Source line:     if ((*cmp == 0) && (*in == ':')) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            4        6          0  REFERENCE
cmplog                           1        8          1  loser (value_profile vs value_profile_cmplog)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        4        6          0  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         3        6          1  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=8  unreached=1
  avg duration blocked: winner=10.20h  loser=18.78h
  avg hitcount on branch: winner=4  loser=2
  prob_div=0.69  dur_div=8.58h  hit_div=2
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6719/{W,L}/branch_coverage_show.txt

--- Enclosing function: parser.c:xmlParseQNameAndCompare (/src/libxml2/parser.c:8970-9007) ---
[ ]  8968  static const xmlChar *
[ ]  8969  xmlParseQNameAndCompare(xmlParserCtxtPtr ctxt, xmlChar const *name,
[B]  8970                          xmlChar const *prefix) {
[B]  8971      const xmlChar *cmp;
[B]  8972      const xmlChar *in;
[B]  8973      const xmlChar *ret;
[B]  8974      const xmlChar *prefix2;
[ ]  8975  
[B]  8976      if (prefix == NULL) return(xmlParseNameAndCompare(ctxt, name));
[ ]  8977  
[B]  8978      GROW;
[B]  8979      in = ctxt->input->cur;
[ ]  8980  
[B]  8981      cmp = prefix;
[B]  8982      while (*in != 0 && *in == *cmp) {
[B]  8983  	++in;
[B]  8984  	++cmp;
[B]  8985      }
[B]  8986      if ((*cmp == 0) && (*in == ':')) { <-- BLOCKER
[W]  8987          in++;
[W]  8988  	cmp = name;
[W]  8989  	while (*in != 0 && *in == *cmp) {
[ ]  8990  	    ++in;
[ ]  8991  	    ++cmp;
[ ]  8992  	}
[W]  8993  	if (*cmp == 0 && (*in == '>' || IS_BLANK_CH (*in))) {
[ ]  8994  	    /* success */
[ ]  8995              ctxt->input->col += in - ctxt->input->cur;
[ ]  8996  	    ctxt->input->cur = in;
[ ]  8997  	    return((const xmlChar*) 1);
[ ]  8998  	}
[W]  8999      }
[ ]  9000      /*
[ ]  9001       * all strings coms from the dictionary, equality can be done directly
[ ]  9002       */
[B]  9003      ret = xmlParseQName (ctxt, &prefix2);
[B]  9004      if ((ret == name) && (prefix == prefix2))
[ ]  9005  	return((const xmlChar*) 1);
[B]  9006      return ret;
[B]  9007  }

--- Caller (1 hop): parser.c:xmlParseEndTag2 (/src/libxml2/parser.c:9792-9843, calls parser.c:xmlParseQNameAndCompare at line 9805) (±10 around call site) ---
[B]  9795      GROW;
[B]  9796      if ((RAW != '<') || (NXT(1) != '/')) {
[ ]  9797  	xmlFatalErr(ctxt, XML_ERR_LTSLASH_REQUIRED, NULL);
[ ]  9798  	return;
[ ]  9799      }
[B]  9800      SKIP(2);
[ ]  9801  
[B]  9802      if (tag->prefix == NULL)
[B]  9803          name = xmlParseNameAndCompare(ctxt, ctxt->name);
[B]  9804      else
[B]  9805          name = xmlParseQNameAndCompare(ctxt, ctxt->name, tag->prefix); <-- CALL
[ ]  9806  
[ ]  9807      /*
[ ]  9808       * We should definitely be at the ending "S? '>'" part
[ ]  9809       */
[B]  9810      GROW;
[B]  9811      if (ctxt->instate == XML_PARSER_EOF)
[ ]  9812          return;
[B]  9813      SKIP_BLANKS;
[B]  9814      if ((!IS_BYTE_CHAR(RAW)) || (RAW != '>')) {
[B]  9815  	xmlFatalErr(ctxt, XML_ERR_GT_REQUIRED, NULL);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlParseEndTag2  (/src/libxml2/parser.c:9792-9843, calls parser.c:xmlParseQNameAndCompare at line 9805)
hop 3  parser.c:xmlParseElementEnd  (/src/libxml2/parser.c:10235-10267, calls parser.c:xmlParseEndTag2 at line 10249)
hop 3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls parser.c:xmlParseEndTag2 at line 11798)
hop 4  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls parser.c:xmlParseElementEnd at line 10008)
hop 4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 4  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseElementEnd at line 10093)
hop 5  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 5  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 6  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls xmlParseContent at line 12969)
hop 6  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 6  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 6  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 7  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 7  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 7  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 8  xmlParseEntity  (/src/libxml2/parser.c:13761-13763, calls xmlSAXParseEntity at line 13762)
hop 8  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 8  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       4        85  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      31       103  nodePop  (/src/libxml2/parser.c:1788-1802)
       9        53  parser.c:xmlParseAttribute2  (/src/libxml2/parser.c:9225-9323)
      14        53  parser.c:xmlFatalErrMsgStr  (/src/libxml2/parser.c:632-647)
       3        20  parser.c:xmlParseNameAndCompare  (/src/libxml2/parser.c:3549-3576)
      12         3  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
      12         3  xmlParseEncodingDecl  (/src/libxml2/parser.c:10460-10558)
      12         3  xmlParseSDDecl  (/src/libxml2/parser.c:10594-10644)
       6         0  parser.c:xmlWarningMsg  (/src/libxml2/parser.c:494-518)
       6         0  xmlParsePITarget  (/src/libxml2/parser.c:5123-5155)
       6         0  xmlParsePI  (/src/libxml2/parser.c:5233-5371)
       0         6  parser.c:xmlParseAttValueInternal  (/src/libxml2/parser.c:9058-9203)
       0         3  parser.c:xmlCtxtGrowAttrs  (/src/libxml2/parser.c:1653-1680)
       0         3  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
       0         3  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  xmlParseReference  (/src/libxml2/parser.c:7173-7586) ---
  d=7   L7181  T=0 F=0  T=0 F=3  if (RAW != '&')
  d=7   L7187  T=0 F=0  T=0 F=3  if (NXT(1) == '#') {
  d=7   L7233  T=0 F=0  T=3 F=0  if (ent == NULL) return;
--- d=5  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=5   L10846  T=10 F=0  T=9 F=3  if (enc != XML_CHAR_ENCODING_NONE) {
--- d=4  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=4   L9973  T=142 F=9  T=47 F=2  while ((RAW != 0) &&
  d=4   L9974  T=142 F=0  T=47 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=4   L9980  T=56 F=86  T=22 F=25  if ((*cur == '<') && (cur[1] == '?')) {
  d=4   L9980  T=0 F=56  T=0 F=22  if ((*cur == '<') && (cur[1] == '?')) {
  d=4   L9995  T=56 F=86  T=22 F=25  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=4   L9995  T=5 F=51  T=0 F=22  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=4   L9996  T=0 F=5  T=0 F=0  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=4   L10004  T=56 F=86  T=22 F=25  else if (*cur == '<') {
  d=4   L10005  T=12 F=44  T=7 F=15  if (NXT(1) == '/') {
  d=4   L10019  T=0 F=86  T=0 F=25  else if (*cur == '&') {
--- d=4  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=4   L10077  T=0 F=10  T=4 F=8  if (xmlParseElementStart(ctxt) != 0)
--- d=4  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=4   L12248  T=0 F=8  T=2 F=31  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=4   L12268  T=0 F=26  T=12 F=28  if (terminate) {
  d=4   L12274  T=0 F=0  T=12 F=0  if (ctxt->input != NULL) {
  d=4   L12275  T=0 F=0  T=0 F=12  if (ctxt->input->buf == NULL)
  d=4   L12283  T=0 F=0  T=12 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=4   L12284  T=0 F=0  T=7 F=5  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=4   L12287  T=0 F=0  T=0 F=5  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=4   L12287  T=0 F=0  T=5 F=7  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=4   L12290  T=0 F=0  T=12 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=4   L12291  T=0 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=4   L12291  T=0 F=0  T=12 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
--- d=3  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=3   L11471  T=0 F=277  T=2 F=319  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=3   L11500  T=0 F=377  T=10 F=437  if (avail < 1)
  d=3   L11553  T=38 F=0  T=21 F=6  if ((cur == '<') && (next == '?')) {
  d=3   L11594  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11594  T=4 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11595  T=4 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=3   L11604  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11604  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=3   L11608  T=0 F=0  T=0 F=6  if (ctxt->version == NULL) {
  d=3   L11612  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11612  T=0 F=0  T=6 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=3   L11613  T=0 F=0  T=6 F=0  (!ctxt->disableSAX))
  d=3   L11657  T=19 F=68  T=0 F=71  if (name == NULL) {
  d=3   L11660  T=19 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11660  T=19 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11678  T=0 F=0  T=0 F=1  if ((RAW == '/') && (NXT(1) == '>')) {
  d=3   L11678  T=0 F=68  T=1 F=70  if ((RAW == '/') && (NXT(1) == '>')) {
  d=3   L11736  T=68 F=0  T=48 F=6  } else if ((cur == '<') && (next != '!')) {
  d=3   L11739  T=0 F=103  T=6 F=139  } else if ((cur == '<') && (next == '!') &&
  d=3   L11739  T=0 F=0  T=6 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11740  T=0 F=0  T=0 F=6  (ctxt->input->cur[2] == '-') &&
  d=3   L11747  T=0 F=0  T=6 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11747  T=0 F=103  T=6 F=139  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=3   L11748  T=0 F=0  T=0 F=6  (ctxt->input->cur[2] == '[') &&
  d=3   L11758  T=0 F=103  T=6 F=139  } else if ((cur == '<') && (next == '!') &&
  d=3   L11758  T=0 F=0  T=6 F=0  } else if ((cur == '<') && (next == '!') &&
  d=3   L11759  T=0 F=0  T=0 F=6  (avail < 9)) {
  d=3   L11761  T=0 F=103  T=6 F=139  } else if (cur == '<') {
  d=3   L11765  T=0 F=103  T=5 F=134  } else if (cur == '&') {
  d=3   L11766  T=0 F=0  T=2 F=3  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11766  T=0 F=0  T=2 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, ';')))
  d=3   L11793  T=0 F=16  T=0 F=36  if (avail < 2)
  d=3   L11795  T=0 F=14  T=2 F=20  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11795  T=14 F=2  T=22 F=14  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=3   L11797  T=16 F=0  T=34 F=0  if (ctxt->sax2) {
  d=3   L11805  T=0 F=16  T=0 F=34  if (ctxt->instate == XML_PARSER_EOF) {
  d=3   L11807  T=0 F=16  T=10 F=24  } else if (ctxt->nameNr == 0) {
  d=3   L11906  T=0 F=377  T=10 F=427  case XML_PARSER_EPILOG:
  d=3   L11914  T=0 F=36  T=8 F=42  if (avail < 2)
  d=3   L11918  T=36 F=0  T=40 F=2  if ((cur == '<') && (next == '?')) {
  d=3   L11918  T=4 F=32  T=0 F=40  if ((cur == '<') && (next == '?')) {
  d=3   L11919  T=4 F=0  T=0 F=0  if ((!terminate) &&
  d=3   L11920  T=0 F=4  T=0 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=3   L11927  T=0 F=4  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=3   L11929  T=32 F=0  T=40 F=2  } else if ((cur == '<') && (next == '!') &&
  d=3   L11985  T=20 F=0  T=24 F=2  } else if ((cur == '<') && (next == '!') &&
  d=3   L11989  T=0 F=20  T=2 F=24  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=3   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=3   L11996  T=0 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
--- d=2  parser.c:xmlParseEndTag2  (/src/libxml2/parser.c:9792-9843) ---
  d=2   L9825  T=28 F=0  T=34 F=7  if (name != (xmlChar*)1) {
  d=2   L9826  T=0 F=28  T=2 F=32  if (name == NULL) name = BAD_CAST "unparsable";
  d=2   L9836  T=28 F=0  T=39 F=2  (!ctxt->disableSAX))
--- d=1  parser.c:xmlParseQNameAndCompare  (/src/libxml2/parser.c:8970-9007) ---
  d=1   L8982  T=47 F=0  T=26 F=2  while (*in != 0 && *in == *cmp) {
  d=1   L8986  T=22 F=3  T=0 F=21  if ((*cmp == 0) && (*in == ':')) {  <-- BLOCKER
  d=1   L8986  T=4 F=18  T=0 F=0  if ((*cmp == 0) && (*in == ':')) {  <-- BLOCKER
  d=1   L8989  T=0 F=3  T=0 F=0  while (*in != 0 && *in == *cmp) {
  d=1   L8989  T=3 F=1  T=0 F=0  while (*in != 0 && *in == *cmp) {
  d=1   L8993  T=0 F=4  T=0 F=0  if (*cmp == 0 && (*in == '>' || IS_BLANK_CH (*in))) {

[off-chain: 464 additional divergent branches across 41 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=2ab6c1d86ed2cc66, size=368 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=5613s, mutation_op=CrossoverReplaceMutator,BytesRandSetMutator,BytesDeleteMutator,ByteDecMutator,QwordAddMutator,BytesCopyMutator):
  0000: 45 4d 45 4e 54 20 06 00 00 00 31 32 37 37 37 32   EMENT ....127772
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
Seed 2 (id=91c72f116c93f792, size=368 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=10516s, mutation_op=TokenInsert,ByteNegMutator,ByteFlipMutator,WordAddMutator):
  0000: 45 4d 45 4e 54 20 06 00 00 00 31 32 37 37 37 32   EMENT ....127772
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
  0020: 69 6f 6e 3d 22 0a 2e 30 22 3f 22 0a 3c 21 44 4f   ion="..0"?".<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
Seed 3 (id=ba004e783d8875ef, size=316 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=10532s, mutation_op=BytesDeleteMutator,BytesCopyMutator,BytesRandInsertMutator,DwordAddMutator):
  0000: 45 4d 45 4e 54 20 06 00 00 00 31 32 37 37 37 32   EMENT ....127772
  0010: 2e 78 6d 6c 8c 8c 8c 8c 5c 0a 3c 3f 78 6d 6c 20   .xml....\.<?xml 
  0020: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0030: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
Seed 4 (id=143c004d3d4213fb, size=316 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=16333s, mutation_op=CrossoverReplaceMutator,DwordAddMutator,BitFlipMutator,BytesInsertCopyMutator,WordAddMutator):
  0000: 45 4d 45 4e 54 20 06 00 00 00 31 32 37 37 37 32   EMENT ....127772
  0010: 2e 78 6d 6c 8c 8c 8c 8c 5c 0a 3c 3f 78 6d 6c 3a   .xml....\.<?xml:
  0020: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0030: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
Seed 5 (id=1683a41876b4a583, size=316 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=16333s, mutation_op=ByteRandMutator,BytesDeleteMutator,TokenReplace,ByteInterestingMutator,ByteNegMutator,BytesInsertCopyMutator):
  0000: 45 4d 45 4e 54 20 06 00 00 00 31 32 37 37 37 32   EMENT ....127772
  0010: 2e 78 6d 6c 8c 8c 8c 8c 5c 0a 3c 3f 78 6d 6c 20   .xml....\.<?xml 
  0020: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0030: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=46d1f13b506003f2, size=378 bytes, fuzzer=cmplog, trial=1, discovered_at=274s, mutation_op=ByteFlipMutator,DwordAddMutator,BytesRandInsertMutator):
  0000: f9 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=00ebab469d057524, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=573s, mutation_op=ByteFlipMutator,ByteNegMutator,BitFlipMutator,CrossoverReplaceMutator):
  0000: 37 58 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7X72.xml\.<?xml 
  0010: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 73 2a 31 32 37 37 37 32 2e   EM "dtds*127772.
Seed 3 (id=56c1349fab4c6f53, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=1257s, mutation_op=BitFlipMutator,WordAddMutator,ByteRandMutator):
  0000: 23 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   #...127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=182575608813b2de, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=1526s, mutation_op=QwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 0d 76 65 72 73 69 6f 6e 3d 22 31   <?xml.version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 7e 31   a SYSTEM "dtds~1
Seed 5 (id=3990ce23b3b3546a, size=372 bytes, fuzzer=cmplog, trial=1, discovered_at=3539s, mutation_op=CrossoverInsertMutator,BytesDeleteMutator,BytesDeleteMutator,BytesDeleteMutator,ByteNegMutator):
  0000: 31 3c 39 39 2f 3a 6c 69 6e 22 27 0a 20 20 20 20   1<99/:lin"'.    
  0010: 20 20 20 20 20 20 20 20 78 6c 69 25 6b 3a 74 79           xli%k:ty
  0020: 70 ff 0a 20 20 28 73 27 6d 70 25 65 29 2d 20 23   p..  (s'mp%e)- #
  0030: 46 49 58 45 44 20 27 73 0a 28 3f 78 6d 6c 2e 76   FIXED 's.(?xml.v


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  45(E)x10                            07(.)x3 f9(.)x1 37(7)x1 23(#)x1 +6u  DIFFER
   0x0001  4d(M)x10                            00(.)x6 58(X)x1 3c(<)x1 69(i)x1 +3u  DIFFER
   0x0002  45(E)x10                            00(.)x6 37(7)x1 39(9)x1 69(i)x1 +3u  DIFFER
   0x0003  4e(N)x10                            00(.)x7 32(2)x1 39(9)x1 09(.)x1 +2u  DIFFER
   0x0004  54(T)x10                            31(1)x7 2e(.)x1 2f(/)x1 09(.)x1 +2u  DIFFER
   0x0005  20( )x10                            32(2)x7 78(x)x1 3a(:)x1 09(.)x1 +2u  DIFFER
   0x0006  06(.)x10                            37(7)x7 6d(m)x1 6c(l)x1 09(.)x1 +2u  DIFFER
   0x0007  00(.)x10                            37(7)x7 6c(l)x1 69(i)x1 09(.)x1 +2u  DIFFER
   0x0008  00(.)x10                            37(7)x7 5c(\)x1 6e(n)x1 09(.)x1 +2u  DIFFER
   0x0009  00(.)x10                            32(2)x7 0a(.)x1 22(")x1 31(1)x1 +2u  DIFFER
   0x000a  31(1)x10                            2e(.)x7 3c(<)x1 27(')x1 32(2)x1 +2u  DIFFER
   0x000b  32(2)x10                            78(x)x5 3f(?)x1 0a(.)x1 20( )x1 +4u  DIFFER
   0x000c  37(7)x10                            6d(m)x6 78(x)x1 20( )x1 8e(.)x1 +3u  PARTIAL
   0x000d  37(7)x10                            6c(l)x6 6d(m)x1 20( )x1 36(6)x1 +3u  PARTIAL
   0x000e  37(7)x10                            5c(\)x6 6c(l)x1 20( )x1 ef(.)x1 +3u  DIFFER
   0x000f  32(2)x10                            0a(.)x6 20( )x3 53(S)x1 40(@)x1 +1u  DIFFER
   0x0010  2e(.)x10                            3c(<)x6 76(v)x1 20( )x1 5c(\)x1 +3u  DIFFER
   0x0011  78(x)x10                            3f(?)x5 6d(m)x2 65(e)x1 20( )x1 +3u  PARTIAL
   0x0012  6d(m)x10                            78(x)x5 6c(l)x2 72(r)x1 20( )x1 +3u  PARTIAL
   0x0013  6c(l)x10                            6d(m)x6 73(s)x1 20( )x1 6c(l)x1 +3u  PARTIAL
   0x0014  5c(\)x5 8c(.)x5                     6c(l)x6 69(i)x1 20( )x1 6e(n)x1 +3u  DIFFER
   0x0015  0a(.)x5 8c(.)x5                     20( )x5 0d(.)x2 6f(o)x1 73(s)x1 +3u  DIFFER
   0x0016  3c(<)x5 8c(.)x5                     76(v)x6 6e(n)x1 20( )x1 3a(:)x1 +3u  DIFFER
   0x0017  3f(?)x5 8c(.)x5                     65(e)x6 20( )x2 78(x)x2 3d(=)x1 +1u  DIFFER
   0x0018  78(x)x5 5c(\)x5                     72(r)x6 22(")x1 78(x)x1 6c(l)x1 +3u  PARTIAL
   0x0019  6d(m)x5 0a(.)x5                     73(s)x6 6c(l)x2 31(1)x1 69(i)x1 +2u  DIFFER
   0x001a  6c(l)x5 3c(<)x5                     69(i)x7 2e(.)x1 6e(n)x1 20( )x1 +2u  DIFFER
   0x001b  20( )x5 3f(?)x5                     6f(o)x6 30(0)x1 25(%)x1 6b(k)x1 +3u  DIFFER
   0x001c  76(v)x5 78(x)x5                     6e(n)x6 22(")x1 6b(k)x1 c6(.)x1 +3u  DIFFER
   0x001d  65(e)x5 6d(m)x5                     3d(=)x6 3f(?)x1 3a(:)x1 c6(.)x1 +3u  DIFFER
   0x001e  72(r)x5 6c(l)x5                     22(")x6 3e(>)x1 74(t)x1 c6(.)x1 +3u  DIFFER
   0x001f  73(s)x5 20( )x3 3a(:)x2             31(1)x6 0a(.)x1 79(y)x1 20( )x1 +3u  PARTIAL
   0x0020  69(i)x5 76(v)x5                     2e(.)x6 3c(<)x1 70(p)x1 20( )x1 +3u  DIFFER
   0x0021  65(e)x5 61(a)x3 6f(o)x2             30(0)x6 6e(n)x2 21(!)x1 ff(.)x1 +2u  DIFFER
   0x0022  6e(n)x5 72(r)x5                     22(")x6 44(D)x2 0a(.)x1 3d(=)x1 +2u  PARTIAL
   0x0023  3d(=)x5 73(s)x5                     3f(?)x6 20( )x2 4f(O)x1 41(A)x1 +2u  DIFFER
   0x0024  22(")x5 69(i)x5                     3e(>)x6 20( )x2 43(C)x1 54(T)x1 +2u  DIFFER
   0x0025  6f(o)x5 0a(.)x4 31(1)x1             0a(.)x6 54(T)x1 28(()x1 41(A)x1 +3u  PARTIAL
   0x0026  2e(.)x5 6e(n)x5                     3c(<)x6 59(Y)x1 73(s)x1 20( )x1 +3u  PARTIAL
   0x0027  30(0)x5 3d(=)x5                     21(!)x6 50(P)x1 27(')x1 20( )x1 +3u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6719.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6719,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6719 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6719 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6719 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).