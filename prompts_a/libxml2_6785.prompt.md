==== BLOCKER ====
Target: libxml2
Branch ID: 6785
Location: /src/libxml2/parser.c:10852:9
Enclosing function: xmlParseDocument
Source line:     if (CUR == 0) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (value_profile vs value_profile); loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     5        5          0  REFERENCE
mopt                             4        6          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.30h  loser=24.00h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.90  dur_div=19.70h  hit_div=2
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=5.10h  loser=24.00h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.80  dur_div=18.90h  hit_div=1
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6785/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseDocument (/src/libxml2/parser.c:10810-10985) ---
[ ] 10808  
[ ] 10809  int
[B] 10810  xmlParseDocument(xmlParserCtxtPtr ctxt) {
[B] 10811      xmlChar start[4];
[B] 10812      xmlCharEncoding enc;
[ ] 10813  
[B] 10814      xmlInitParser();
[ ] 10815  
[B] 10816      if ((ctxt == NULL) || (ctxt->input == NULL))
[ ] 10817          return(-1);
[ ] 10818  
[B] 10819      GROW;
[ ] 10820  
[ ] 10821      /*
[ ] 10822       * SAX: detecting the level.
[ ] 10823       */
[B] 10824      xmlDetectSAX2(ctxt);
[ ] 10825  
[ ] 10826      /*
[ ] 10827       * SAX: beginning of the document processing.
[ ] 10828       */
[B] 10829      if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
[B] 10830          ctxt->sax->setDocumentLocator(ctxt->userData, &xmlDefaultSAXLocator);
[B] 10831      if (ctxt->instate == XML_PARSER_EOF)
[ ] 10832  	return(-1);
[ ] 10833  
[B] 10834      if ((ctxt->encoding == NULL) &&
[B] 10835          ((ctxt->input->end - ctxt->input->cur) >= 4)) {
[ ] 10836  	/*
[ ] 10837  	 * Get the 4 first bytes and decode the charset
[ ] 10838  	 * if enc != XML_CHAR_ENCODING_NONE
[ ] 10839  	 * plug some encoding conversion routines.
[ ] 10840  	 */
[B] 10841  	start[0] = RAW;
[B] 10842  	start[1] = NXT(1);
[B] 10843  	start[2] = NXT(2);
[B] 10844  	start[3] = NXT(3);
[B] 10845  	enc = xmlDetectCharEncoding(&start[0], 4);
[B] 10846  	if (enc != XML_CHAR_ENCODING_NONE) {
[L] 10847  	    xmlSwitchEncoding(ctxt, enc);
[L] 10848  	}
[B] 10849      }
[ ] 10850  
[ ] 10851  
[B] 10852      if (CUR == 0) { <-- BLOCKER
[W] 10853  	xmlFatalErr(ctxt, XML_ERR_DOCUMENT_EMPTY, NULL);
[W] 10854  	return(-1);
[W] 10855      }
[ ] 10856  
[ ] 10857      /*
[ ] 10858       * Check for the XMLDecl in the Prolog.
[ ] 10859       * do not GROW here to avoid the detected encoder to decode more
[ ] 10860       * than just the first line, unless the amount of data is really
[ ] 10861       * too small to hold "<?xml version="1.0" encoding="foo"
[ ] 10862       */
[L] 10863      if ((ctxt->input->end - ctxt->input->cur) < 35) {
[L] 10864         GROW;
[L] 10865      }
[L] 10866      if ((CMP5(CUR_PTR, '<', '?', 'x', 'm', 'l')) && (IS_BLANK_CH(NXT(5)))) {
[ ] 10867  
[ ] 10868  	/*
[ ] 10869  	 * Note that we will switch encoding on the fly.
[ ] 10870  	 */
[L] 10871  	xmlParseXMLDecl(ctxt);
[L] 10872  	if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
[L] 10873  	    (ctxt->instate == XML_PARSER_EOF)) {
[ ] 10874  	    /*
[ ] 10875  	     * The XML REC instructs us to stop parsing right here
[ ] 10876  	     */
[ ] 10877  	    return(-1);
[ ] 10878  	}
[L] 10879  	ctxt->standalone = ctxt->input->standalone;
[L] 10880  	SKIP_BLANKS;
[L] 10881      } else {
[L] 10882  	ctxt->version = xmlCharStrdup(XML_DEFAULT_VERSION);
[L] 10883      }
[L] 10884      if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->disableSAX))
[L] 10885          ctxt->sax->startDocument(ctxt->userData);
[L] 10886      if (ctxt->instate == XML_PARSER_EOF)
[ ] 10887  	return(-1);
[L] 10888      if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
[L] 10889          (ctxt->input->buf != NULL) && (ctxt->input->buf->compressed >= 0)) {
[ ] 10890  	ctxt->myDoc->compression = ctxt->input->buf->compressed;
[ ] 10891      }
[ ] 10892  
[ ] 10893      /*
[ ] 10894       * The Misc part of the Prolog
[ ] 10895       */
[L] 10896      xmlParseMisc(ctxt);
[ ] 10897  
[ ] 10898      /*
[ ] 10899       * Then possibly doc type declaration(s) and more Misc
[ ] 10900       * (doctypedecl Misc*)?
[ ] 10901       */
[L] 10902      GROW;
[L] 10903      if (CMP9(CUR_PTR, '<', '!', 'D', 'O', 'C', 'T', 'Y', 'P', 'E')) {
[ ] 10904  
[L] 10905  	ctxt->inSubset = 1;
[L] 10906  	xmlParseDocTypeDecl(ctxt);
[L] 10907  	if (RAW == '[') {
[ ] 10908  	    ctxt->instate = XML_PARSER_DTD;
[ ] 10909  	    xmlParseInternalSubset(ctxt);
[ ] 10910  	    if (ctxt->instate == XML_PARSER_EOF)
[ ] 10911  		return(-1);
[ ] 10912  	}
[ ] 10913  
[ ] 10914  	/*
[ ] 10915  	 * Create and update the external subset.
[ ] 10916  	 */
[L] 10917  	ctxt->inSubset = 2;
[L] 10918  	if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != NULL) &&
[L] 10919  	    (!ctxt->disableSAX))
[L] 10920  	    ctxt->sax->externalSubset(ctxt->userData, ctxt->intSubName,
[L] 10921  	                              ctxt->extSubSystem, ctxt->extSubURI);
[L] 10922  	if (ctxt->instate == XML_PARSER_EOF)
[ ] 10923  	    return(-1);
[L] 10924  	ctxt->inSubset = 0;
[ ] 10925  
[L] 10926          xmlCleanSpecialAttr(ctxt);
[ ] 10927  
[L] 10928  	ctxt->instate = XML_PARSER_PROLOG;
[L] 10929  	xmlParseMisc(ctxt);
[L] 10930      }
[ ] 10931  
[ ] 10932      /*
[ ] 10933       * Time to start parsing the tree itself
[ ] 10934       */
[L] 10935      GROW;
[L] 10936      if (RAW != '<') {
[L] 10937  	xmlFatalErrMsg(ctxt, XML_ERR_DOCUMENT_EMPTY,
[L] 10938  		       "Start tag expected, '<' not found\n");
[L] 10939      } else {
[L] 10940  	ctxt->instate = XML_PARSER_CONTENT;
[L] 10941  	xmlParseElement(ctxt);
[L] 10942  	ctxt->instate = XML_PARSER_EPILOG;
[ ] 10943  
[ ] 10944  
[ ] 10945  	/*
[ ] 10946  	 * The Misc part at the end
[ ] 10947  	 */
[L] 10948  	xmlParseMisc(ctxt);
[ ] 10949  
[L] 10950  	if (RAW != 0) {
[L] 10951  	    xmlFatalErr(ctxt, XML_ERR_DOCUMENT_END, NULL);
[L] 10952  	}
[L] 10953  	ctxt->instate = XML_PARSER_EOF;
[L] 10954      }
[ ] 10955  
[ ] 10956      /*
[ ] 10957       * SAX: end of the document processing.
[ ] 10958       */
[L] 10959      if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
[L] 10960          ctxt->sax->endDocument(ctxt->userData);
[ ] 10961  
[ ] 10962      /*
[ ] 10963       * Remove locally kept entity definitions if the tree was not built
[ ] 10964       */
[L] 10965      if ((ctxt->myDoc != NULL) &&
[L] 10966  	(xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
[ ] 10967  	xmlFreeDoc(ctxt->myDoc);
[ ] 10968  	ctxt->myDoc = NULL;
[ ] 10969      }
[ ] 10970  
[L] 10971      if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
[ ] 10972          ctxt->myDoc->properties |= XML_DOC_WELLFORMED;
[ ] 10973  	if (ctxt->valid)
[ ] 10974  	    ctxt->myDoc->properties |= XML_DOC_DTDVALID;
[ ] 10975  	if (ctxt->nsWellFormed)
[ ] 10976  	    ctxt->myDoc->properties |= XML_DOC_NSVALID;
[ ] 10977  	if (ctxt->options & XML_PARSE_OLD10)
[ ] 10978  	    ctxt->myDoc->properties |= XML_DOC_OLD10;
[ ] 10979      }
[L] 10980      if (! ctxt->wellFormed) {
[L] 10981  	ctxt->valid = 0;
[L] 10982  	return(-1);
[L] 10983      }
[ ] 10984      return(0);
[L] 10985  }

--- Caller (1 hop): parser.c:xmlDoRead (/src/libxml2/parser.c:15002-15031, calls xmlParseDocument at line 15016) (full body — short) ---
[B] 15002  {
[B] 15003      xmlDocPtr ret;
[ ] 15004  
[B] 15005      xmlCtxtUseOptionsInternal(ctxt, options, encoding);
[B] 15006      if (encoding != NULL) {
[ ] 15007          xmlCharEncodingHandlerPtr hdlr;
[ ] 15008  
[ ] 15009  	hdlr = xmlFindCharEncodingHandler(encoding);
[ ] 15010  	if (hdlr != NULL)
[ ] 15011  	    xmlSwitchToEncoding(ctxt, hdlr);
[ ] 15012      }
[B] 15013      if ((URL != NULL) && (ctxt->input != NULL) &&
[B] 15014          (ctxt->input->filename == NULL))
[B] 15015          ctxt->input->filename = (char *) xmlStrdup((const xmlChar *) URL);
[B] 15016      xmlParseDocument(ctxt); <-- CALL
[B] 15017      if ((ctxt->wellFormed) || ctxt->recovery)
[B] 15018          ret = ctxt->myDoc;
[B] 15019      else {
[B] 15020          ret = NULL;
[B] 15021  	if (ctxt->myDoc != NULL) {
[L] 15022  	    xmlFreeDoc(ctxt->myDoc);
[L] 15023  	}
[B] 15024      }
[B] 15025      ctxt->myDoc = NULL;
[B] 15026      if (!reuse) {
[B] 15027  	xmlFreeParserCtxt(ctxt);
[B] 15028      }
[ ] 15029  
[B] 15030      return (ret);
[B] 15031  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 2  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)
hop 3  xmlSAXParseFile  (/src/libxml2/parser.c:14012-14014, calls xmlSAXParseFileWithData at line 14013)
hop 4  xmlParseFile  (/src/libxml2/parser.c:14048-14050, calls xmlSAXParseFile at line 14049)
hop 4  xmlRecoverFile  (/src/libxml2/parser.c:14067-14069, calls xmlSAXParseFile at line 14068)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     204       850  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
       3       120  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
       0        88  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
       0        71  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      27        90  inputPop  (/src/libxml2/parser.c:1723-1738)
       0        63  xmlParsePITarget  (/src/libxml2/parser.c:5123-5155)
       0        63  xmlParsePI  (/src/libxml2/parser.c:5233-5371)
       0        49  parser.c:xmlParseLookupString  (/src/libxml2/parser.c:11137-11161)
       9        45  xmlParseChunk  (/src/libxml2/parser.c:12135-12300)
       0        34  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
       6        36  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120)
       0        25  parser.c:areBlanks  (/src/libxml2/parser.c:2889-2942)
       9        33  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
       0        22  parser.c:xmlParseLookupCharData  (/src/libxml2/parser.c:11170-11184)
       9        30  inputPush  (/src/libxml2/parser.c:1693-1712)
... (37 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=1   L10816  T=0 F=3  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=1   L10816  T=0 F=3  T=0 F=10  if ((ctxt == NULL) || (ctxt->input == NULL))
  d=1   L10829  T=3 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L10829  T=3 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))
  d=1   L10831  T=0 F=3  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L10834  T=3 F=0  T=10 F=0  if ((ctxt->encoding == NULL) &&
  d=1   L10835  T=3 F=0  T=9 F=1  ((ctxt->input->end - ctxt->input->cur) >= 4)) {
  d=1   L10846  T=0 F=3  T=2 F=7  if (enc != XML_CHAR_ENCODING_NONE) {
  d=1   L10852  T=3 F=0  T=0 F=10  if (CUR == 0) {  <-- BLOCKER
  d=1   L10863  T=0 F=0  T=4 F=6  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=1   L10872  T=0 F=0  T=0 F=2  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=1   L10873  T=0 F=0  T=0 F=2  (ctxt->instate == XML_PARSER_EOF)) {
  d=1   L10884  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=1   L10884  T=0 F=0  T=9 F=1  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=1   L10884  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) && (!ctxt->...
  d=1   L10886  T=0 F=0  T=0 F=10  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L10888  T=0 F=0  T=9 F=0  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=1   L10888  T=0 F=0  T=9 F=1  if ((ctxt->myDoc != NULL) && (ctxt->input != NULL) &&
  d=1   L10889  T=0 F=0  T=9 F=0  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=1   L10889  T=0 F=0  T=0 F=9  (ctxt->input->buf != NULL) && (ctxt->input->buf->compress...
  d=1   L10907  T=0 F=0  T=0 F=2  if (RAW == '[') {
  d=1   L10918  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=1   L10918  T=0 F=0  T=2 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->externalSubset != ...
  d=1   L10919  T=0 F=0  T=1 F=1  (!ctxt->disableSAX))
  d=1   L10922  T=0 F=0  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L10936  T=0 F=0  T=6 F=4  if (RAW != '<') {
  d=1   L10950  T=0 F=0  T=3 F=1  if (RAW != 0) {
  d=1   L10959  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L10959  T=0 F=0  T=10 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=1   L10965  T=0 F=0  T=9 F=1  if ((ctxt->myDoc != NULL) &&
  d=1   L10966  T=0 F=0  T=0 F=9  (xmlStrEqual(ctxt->myDoc->version, SAX_COMPAT_MODE))) {
  d=1   L10971  T=0 F=0  T=0 F=10  if ((ctxt->wellFormed) && (ctxt->myDoc != NULL)) {
  d=1   L10980  T=0 F=0  T=10 F=0  if (! ctxt->wellFormed) {

[off-chain: 573 additional divergent branches across 50 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d17e8c479b6b27ab, size=380 bytes, fuzzer=value_profile, trial=1, discovered_at=1s, mutation_op=DwordAddMutator,BytesSetMutator,CrossoverInsertMutator,DwordAddMutator):
  0000: 06 54 41 20 20 20 20 20 23 49 4d 50 4c 49 45 44   .TA     #IMPLIED
  0010: 3e 0a 0a 5c 0a 00 00 00 31 32 37 37 37 32 2e 78   >..\....127772.x
  0020: 6d 55 43 53 34 3f 78 6d 6c 20 76 65 72 73 69 6f   mUCS4?xml versio
  0030: 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54   n="1.0"?>.<!DOCT
Seed 2 (id=0924e8911eb5e636, size=332 bytes, fuzzer=value_profile, trial=1, discovered_at=4s, mutation_op=BytesDeleteMutator,ByteInterestingMutator,ByteNegMutator,ByteAddMutator):
  0000: 45 44 3e 0a 0a 5c 0a 00 80 59 50 45 20 61 20 ad   ED>..\...YPE a .
  0010: 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37   YSTEM "dtds/1277
  0020: 37 32 2e 64 74 64 22 3e 0a 0a 3c 61 3e 0a 20 20   72.dtd">..<a>.  
  0030: 3c 62 20 78 6c 69 6e 6b 3a 6b 72 65 66 3d 20 20   <b xlink:kref=  
Seed 3 (id=bac443e768a2dda5, size=129 bytes, fuzzer=value_profile, trial=1, discovered_at=1871s, mutation_op=ByteNegMutator,CrossoverReplaceMutator,BytesInsertMutator,TokenInsert,QwordAddMutator,CrossoverReplaceMutator):
  0000: 54 1f 62 20 28 23 50 44 41 54 45 29 27 27 27 27   T.b (#PDATE)''''
  0010: 27 27 27 27 27 27 5d 5d 5d 5d 5d 5d 5d 5d 5d 5d   '''''']]]]]]]]]]
  0020: 5d 20 62 20 78 6d 94 6e 73 3a 78 6c 49 58 45 fd   ] b xm.ns:xlIXE.
  0030: ff ff ff bf ff ff ff 65 27 0a 20 20 20 20 20 78   .......e'.     x

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=002c299ed57b4600, size=429 bytes, fuzzer=naive, trial=1, discovered_at=41s, mutation_op=BytesInsertCopyMutator,ByteInterestingMutator,ByteDecMutator,BytesExpandMutator,BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 64 72 73 69 6f 6e 3d 22 31   <?xml vdrsion="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=0028492ac168fa2b, size=312 bytes, fuzzer=naive, trial=1, discovered_at=78s, mutation_op=ByteAddMutator,TokenReplace):
  0000: 44 20 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 33   D 'http://www.w3
  0010: 7e 96 98 00 2f 31 39 39 39 2f 78 6c 69 6e 6b 27   ~.../1999/xlink'
  0020: 0a 20 20 20 20 20 20 20 20 20 20 20 20 78 6c 69   .            xli
  0030: 6e 6b 3a 74 79 70 50 20 20 20 28 73 69 6d 70 6c   nk:typP   (simpl
Seed 3 (id=000181ef2e7b3e6f, size=143 bytes, fuzzer=naive, trial=1, discovered_at=228s, mutation_op=DwordAddMutator,BytesRandInsertMutator,ByteDecMutator,ByteFlipMutator,ByteAddMutator):
  0000: 20 27 68 74 74 70 3a 2f 3a 2e 2f 77 77 ba ba ba    'http:/:./ww...
  0010: ba ba ba ba ba ba ba ba ba ba ba 78 6c 69 6e 6b   ...........xlink
  0020: 27 0a 59 ae ff ff 20 20 20 20 20 20 20 20 20 20   '.Y...          
  0030: 20 21 78 6c 69 6e 6b 3a 74 79 70 65 20 20 20 28    !xlink:type   (
Seed 4 (id=001a3d727c70e720, size=183 bytes, fuzzer=naive, trial=1, discovered_at=3389s, mutation_op=DwordAddMutator,ByteAddMutator,ByteFlipMutator,BytesRandInsertMutator,TokenInsert,BytesInsertMutator):
  0000: 20 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 33 2e    'http://www.w3.
  0010: 6f 72 67 2f f7 f7 f7 f7 f7 29 29 29 29 29 29 29   org/.....)))))))
  0020: 29 29 29 29 f7 f7 f7 f7 f7 f7 31 39 39 39 2f 78   ))))......1999/x
  0030: 65 69 6e 84 27 64 73 2f 4b 32 37 37 ce ce ce 73   ein.'ds/K277...s
Seed 5 (id=002678f710d61c62, size=186 bytes, fuzzer=naive, trial=1, discovered_at=8243s, mutation_op=BytesRandInsertMutator,ByteIncMutator,ByteIncMutator,WordAddMutator,WordAddMutator,BytesInsertCopyMutator):
  0000: 98 98 98 98 74 70 3a 2f 2f 66 28 28 28 28 3d 28   ....tp://f((((=(
  0010: 5f 28 28 28 3d 28 5f 5f 5f 5f 5f 5f 5f 5f 31 28   _(((=(________1(
  0020: 5f 5f 5f 5f 5f 5f 5f 5f 31 28 5f 5f 5f 6b 3b 64   ________1(___k;d
  0030: 64 55 43 53 2d 32 64 63 64 64 64 64 83 64 64 64   dUCS-2dcdddd.ddd


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x1 45(E)x1 54(T)x1             44(D)x2 20( )x2 06(.)x1 98(.)x1 +4u  PARTIAL
   0x0001  54(T)x1 44(D)x1 1f(.)x1             20( )x2 27(')x2 00(.)x1 98(.)x1 +4u  DIFFER
   0x0002  41(A)x1 3e(>)x1 62(b)x1             27(')x2 68(h)x2 00(.)x1 98(.)x1 +4u  DIFFER
   0x0003  20( )x2 0a(.)x1                     68(h)x2 74(t)x2 00(.)x1 98(.)x1 +4u  PARTIAL
   0x0004  20( )x1 0a(.)x1 28(()x1             74(t)x6 31(1)x1 68(h)x1 2f(/)x1 +1u  DIFFER
   0x0005  20( )x1 5c(\)x1 23(#)x1             70(p)x4 74(t)x2 32(2)x1 77(w)x1 +2u  DIFFER
   0x0006  20( )x1 0a(.)x1 50(P)x1             3a(:)x4 37(7)x1 70(p)x1 74(t)x1 +3u  DIFFER
   0x0007  20( )x1 00(.)x1 44(D)x1             2f(/)x4 37(7)x1 3a(:)x1 73(s)x1 +3u  DIFFER
   0x0008  23(#)x1 80(.)x1 41(A)x1             2f(/)x4 74(t)x2 37(7)x1 3a(:)x1 +2u  DIFFER
   0x0009  49(I)x1 59(Y)x1 54(T)x1             2f(/)x2 70(p)x2 32(2)x1 2e(.)x1 +4u  DIFFER
   0x000a  4d(M)x1 50(P)x1 45(E)x1             77(w)x2 3a(:)x2 2e(.)x1 2f(/)x1 +4u  DIFFER
   0x000b  50(P)x1 45(E)x1 29())x1             77(w)x3 2f(/)x2 78(x)x1 28(()x1 +3u  DIFFER
   0x000c  4c(L)x1 20( )x1 27(')x1             77(w)x2 2f(/)x2 6d(m)x1 2e(.)x1 +4u  DIFFER
   0x000d  49(I)x1 61(a)x1 27(')x1             77(w)x2 6c(l)x1 2e(.)x1 ba(.)x1 +5u  DIFFER
   0x000e  45(E)x1 20( )x1 27(')x1             5c(\)x1 77(w)x1 ba(.)x1 33(3)x1 +6u  DIFFER
   0x000f  44(D)x1 ad(.)x1 27(')x1             0a(.)x2 33(3)x1 ba(.)x1 2e(.)x1 +5u  DIFFER
   0x0010  3e(>)x1 59(Y)x1 27(')x1             3c(<)x2 7e(~)x1 ba(.)x1 6f(o)x1 +5u  DIFFER
   0x0011  0a(.)x1 53(S)x1 27(')x1             3f(?)x1 96(.)x1 ba(.)x1 72(r)x1 +6u  DIFFER
   0x0012  0a(.)x1 54(T)x1 27(')x1             78(x)x1 98(.)x1 ba(.)x1 67(g)x1 +6u  DIFFER
   0x0013  5c(\)x1 45(E)x1 27(')x1             6d(m)x1 00(.)x1 ba(.)x1 2f(/)x1 +6u  DIFFER
   0x0014  0a(.)x1 4d(M)x1 27(')x1             2f(/)x2 6c(l)x1 ba(.)x1 f7(.)x1 +5u  PARTIAL
   0x0015  00(.)x1 20( )x1 27(')x1             20( )x1 31(1)x1 ba(.)x1 f7(.)x1 +6u  PARTIAL
   0x0016  00(.)x1 22(")x1 5d(])x1             76(v)x1 39(9)x1 ba(.)x1 f7(.)x1 +6u  DIFFER
   0x0017  00(.)x1 64(d)x1 5d(])x1             64(d)x1 39(9)x1 ba(.)x1 f7(.)x1 +6u  PARTIAL
   0x0018  31(1)x1 74(t)x1 5d(])x1             77(w)x2 72(r)x1 39(9)x1 ba(.)x1 +5u  DIFFER
   0x0019  32(2)x1 64(d)x1 5d(])x1             73(s)x1 2f(/)x1 ba(.)x1 29())x1 +6u  DIFFER
   0x001a  37(7)x1 73(s)x1 5d(])x1             69(i)x1 78(x)x1 ba(.)x1 29())x1 +6u  DIFFER
   0x001b  37(7)x1 2f(/)x1 5d(])x1             6f(o)x1 6c(l)x1 78(x)x1 29())x1 +6u  PARTIAL
   0x001c  37(7)x1 31(1)x1 5d(])x1             6e(n)x1 69(i)x1 6c(l)x1 29())x1 +6u  PARTIAL
   0x001d  32(2)x2 5d(])x1                     3d(=)x1 6e(n)x1 69(i)x1 29())x1 +6u  PARTIAL
   0x001e  2e(.)x1 37(7)x1 5d(])x1             22(")x1 6b(k)x1 6e(n)x1 29())x1 +6u  PARTIAL
   0x001f  78(x)x1 37(7)x1 5d(])x1             31(1)x1 27(')x1 6b(k)x1 29())x1 +6u  DIFFER
   0x0020  6d(m)x1 37(7)x1 5d(])x1             2e(.)x2 0a(.)x1 27(')x1 29())x1 +5u  DIFFER
   0x0021  55(U)x1 32(2)x1 20( )x1             30(0)x1 20( )x1 0a(.)x1 29())x1 +6u  PARTIAL
   0x0022  43(C)x1 2e(.)x1 62(b)x1             22(")x1 20( )x1 59(Y)x1 29())x1 +6u  DIFFER
   0x0023  53(S)x1 64(d)x1 20( )x1             29())x2 3f(?)x1 20( )x1 ae(.)x1 +5u  PARTIAL
   0x0024  34(4)x1 74(t)x1 78(x)x1             3e(>)x1 20( )x1 ff(.)x1 f7(.)x1 +6u  PARTIAL
   0x0025  3f(?)x1 64(d)x1 6d(m)x1             0a(.)x1 20( )x1 ff(.)x1 f7(.)x1 +6u  PARTIAL
   0x0026  78(x)x1 22(")x1 94(.)x1             20( )x2 3c(<)x1 f7(.)x1 5f(_)x1 +5u  DIFFER
   0x0027  6d(m)x1 3e(>)x1 6e(n)x1             20( )x2 21(!)x1 f7(.)x1 5f(_)x1 +5u  PARTIAL
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6785.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6785,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6785 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6785 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6785 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).