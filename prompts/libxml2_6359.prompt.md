==== BLOCKER ====
Target: libxml2
Branch ID: 6359
Location: /src/libxml2/encoding.c:987:6
Enclosing function: xmlDetectCharEncoding
Source line: 	if ((in[0] == 0xEF) && (in[1] == 0xBB) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog); loser (ngram_coverage vs naive_ngram4)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    5        5          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        0       10          0  REFERENCE
naive_ngram4                     9        1          0  winner (ngram_coverage vs naive)
mopt                             6        4          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             7        3          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'naive_ngram4']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.40h  loser=21.40h
  avg hitcount on branch: winner=266  loser=2
  prob_div=0.80  dur_div=21.00h  hit_div=264
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001
--- Pair 2: naive_ngram4 > naive  [delta: ngram_coverage] ---
  subject 36  (naive_ngram4 vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=10.80h  loser=21.40h
  avg hitcount on branch: winner=24  loser=2
  prob_div=0.70  dur_div=10.60h  hit_div=21
  subject-level: delta_AUC=-26852220.0  p_AUC=0.0173  delta_Final=-260.4  p_final=0.0312

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6359/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlDetectCharEncoding (/src/libxml2/encoding.c:948-999) ---
[ ]   946  xmlCharEncoding
[ ]   947  xmlDetectCharEncoding(const unsigned char* in, int len)
[B]   948  {
[B]   949      if (in == NULL)
[ ]   950          return(XML_CHAR_ENCODING_NONE);
[B]   951      if (len >= 4) {
[B]   952  	if ((in[0] == 0x00) && (in[1] == 0x00) &&
[B]   953  	    (in[2] == 0x00) && (in[3] == 0x3C))
[ ]   954  	    return(XML_CHAR_ENCODING_UCS4BE);
[B]   955  	if ((in[0] == 0x3C) && (in[1] == 0x00) &&
[B]   956  	    (in[2] == 0x00) && (in[3] == 0x00))
[ ]   957  	    return(XML_CHAR_ENCODING_UCS4LE);
[B]   958  	if ((in[0] == 0x00) && (in[1] == 0x00) &&
[B]   959  	    (in[2] == 0x3C) && (in[3] == 0x00))
[ ]   960  	    return(XML_CHAR_ENCODING_UCS4_2143);
[B]   961  	if ((in[0] == 0x00) && (in[1] == 0x3C) &&
[B]   962  	    (in[2] == 0x00) && (in[3] == 0x00))
[ ]   963  	    return(XML_CHAR_ENCODING_UCS4_3412);
[B]   964  	if ((in[0] == 0x4C) && (in[1] == 0x6F) &&
[B]   965  	    (in[2] == 0xA7) && (in[3] == 0x94))
[ ]   966  	    return(XML_CHAR_ENCODING_EBCDIC);
[B]   967  	if ((in[0] == 0x3C) && (in[1] == 0x3F) &&
[B]   968  	    (in[2] == 0x78) && (in[3] == 0x6D))
[L]   969  	    return(XML_CHAR_ENCODING_UTF8);
[ ]   970  	/*
[ ]   971  	 * Although not part of the recommendation, we also
[ ]   972  	 * attempt an "auto-recognition" of UTF-16LE and
[ ]   973  	 * UTF-16BE encodings.
[ ]   974  	 */
[B]   975  	if ((in[0] == 0x3C) && (in[1] == 0x00) &&
[B]   976  	    (in[2] == 0x3F) && (in[3] == 0x00))
[ ]   977  	    return(XML_CHAR_ENCODING_UTF16LE);
[B]   978  	if ((in[0] == 0x00) && (in[1] == 0x3C) &&
[B]   979  	    (in[2] == 0x00) && (in[3] == 0x3F))
[ ]   980  	    return(XML_CHAR_ENCODING_UTF16BE);
[B]   981      }
[B]   982      if (len >= 3) {
[ ]   983  	/*
[ ]   984  	 * Errata on XML-1.0 June 20 2001
[ ]   985  	 * We now allow an UTF8 encoded BOM
[ ]   986  	 */
[B]   987  	if ((in[0] == 0xEF) && (in[1] == 0xBB) && <-- BLOCKER
[B]   988  	    (in[2] == 0xBF))
[ ]   989  	    return(XML_CHAR_ENCODING_UTF8);
[B]   990      }
[ ]   991      /* For UTF-16 we can recognize by the BOM */
[B]   992      if (len >= 2) {
[B]   993  	if ((in[0] == 0xFE) && (in[1] == 0xFF))
[ ]   994  	    return(XML_CHAR_ENCODING_UTF16BE);
[B]   995  	if ((in[0] == 0xFF) && (in[1] == 0xFE))
[ ]   996  	    return(XML_CHAR_ENCODING_UTF16LE);
[B]   997      }
[B]   998      return(XML_CHAR_ENCODING_NONE);
[B]   999  }

--- Caller (1 hop): parser.c:xmlParseTryOrFinish (/src/libxml2/parser.c:11404-12120, calls xmlDetectCharEncoding at line 11530) (±10 around call site) ---
[ ] 11520  		     * Get the 4 first bytes and decode the charset
[ ] 11521  		     * if enc != XML_CHAR_ENCODING_NONE
[ ] 11522  		     * plug some encoding conversion routines,
[ ] 11523  		     * else xmlSwitchEncoding will set to (default)
[ ] 11524  		     * UTF8.
[ ] 11525  		     */
[B] 11526  		    start[0] = RAW;
[B] 11527  		    start[1] = NXT(1);
[B] 11528  		    start[2] = NXT(2);
[B] 11529  		    start[3] = NXT(3);
[B] 11530  		    enc = xmlDetectCharEncoding(start, 4); <-- CALL
[B] 11531  		    xmlSwitchEncoding(ctxt, enc);
[B] 11532  		    break;
[B] 11533  		}
[ ] 11534  
[B] 11535  		if (avail < 2)
[ ] 11536  		    goto done;
[B] 11537  		cur = ctxt->input->cur[0];
[B] 11538  		next = ctxt->input->cur[1];
[B] 11539  		if (cur == 0) {
[ ] 11540  		    if ((ctxt->sax) && (ctxt->sax->setDocumentLocator))

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlDetectCharEncoding at line 7108)
hop 2  xmlParsePEReference  (/src/libxml2/parser.c:7999-8146, calls xmlDetectCharEncoding at line 8132)
hop 3  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 3  xmlParserHandlePEReference  (/src/libxml2/parser.c:2529-2585, calls xmlParsePEReference at line 2584)
hop 3  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 3  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217, calls xmlParsePEReference at line 2174)
hop 4  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 5  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        16  parser.c:xmlIsNameStartChar  (/src/libxml2/parser.c:3152-3180)
       0        16  parser.c:xmlParseNCNameComplex  (/src/libxml2/parser.c:3415-3471)
       0        16  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
       0        16  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
       0        14  parser.c:spacePush  (/src/libxml2/parser.c:1945-1962)
       0        14  parser.c:spacePop  (/src/libxml2/parser.c:1964-1975)
       0        14  parser.c:xmlParseLookupGt  (/src/libxml2/parser.c:11194-11221)
       0        11  parser.c:xmlParseStartTag2  (/src/libxml2/parser.c:9355-9774)
       0        10  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
       0         9  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       0         6  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       0         5  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)
       0         5  nodePush  (/src/libxml2/parser.c:1750-1776)
       0         5  nodePop  (/src/libxml2/parser.c:1788-1802)
       0         5  parser.c:nameNsPush  (/src/libxml2/parser.c:1820-1860)
... (29 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217) ---
  d=3   L2139  T=30 F=0  T=73 F=0  if (((ctxt->inputNr == 1) && (ctxt->instate != XML_PARSER...
  d=3   L2139  T=30 F=0  T=61 F=12  if (((ctxt->inputNr == 1) && (ctxt->instate != XML_PARSER...
  d=3   L2140  T=0 F=0  T=0 F=12  (ctxt->instate == XML_PARSER_START)) {
  d=3   L2147  T=0 F=0  T=3 F=12  if (*cur == '\n') {
  d=3   L2153  T=0 F=0  T=15 F=0  if (res < INT_MAX)
  d=3   L2155  T=0 F=0  T=0 F=15  if (*cur == 0) {
  d=3   L2163  T=0 F=0  T=12 F=0  int expandPE = ((ctxt->external != 0) || (ctxt->inputNr !...
  d=3   L2165  T=0 F=0  T=15 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=3   L2168  T=0 F=0  T=0 F=12  } else if (CUR == '%') {
  d=3   L2175  T=0 F=0  T=0 F=12  } else if (CUR == 0) {
  d=3   L2212  T=0 F=0  T=3 F=0  if (res < INT_MAX)
--- d=2  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=2   L7099  T=0 F=0  T=3 F=0  if ((ctxt->encoding == NULL) &&
  d=2   L7100  T=0 F=0  T=3 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=2   L7109  T=0 F=0  T=0 F=3  if (enc != XML_CHAR_ENCODING_NONE)
  d=2   L7123  T=0 F=0  T=0 F=3  if (ctxt->myDoc == NULL) {
  d=2   L7131  T=0 F=0  T=0 F=3  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=2   L7131  T=0 F=0  T=3 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=2   L7137  T=0 F=0  T=6 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=2   L7137  T=0 F=0  T=6 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
  d=2   L7139  T=0 F=0  T=3 F=0  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=2   L7139  T=0 F=0  T=3 F=3  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=2   L7139  T=0 F=0  T=0 F=3  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=2   L7141  T=0 F=0  T=3 F=3  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=2   L7141  T=0 F=0  T=3 F=0  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
--- d=1  xmlDetectCharEncoding  (/src/libxml2/encoding.c:948-999) ---
  d=1   L 955  T=0 F=0  T=0 F=22  if ((in[0] == 0x3C) && (in[1] == 0x00) &&
  d=1   L 955  T=0 F=40  T=22 F=20  if ((in[0] == 0x3C) && (in[1] == 0x00) &&
  d=1   L 967  T=0 F=0  T=3 F=19  if ((in[0] == 0x3C) && (in[1] == 0x3F) &&
  d=1   L 967  T=0 F=40  T=22 F=20  if ((in[0] == 0x3C) && (in[1] == 0x3F) &&
  d=1   L 968  T=0 F=0  T=3 F=0  (in[2] == 0x78) && (in[3] == 0x6D))
  d=1   L 968  T=0 F=0  T=3 F=0  (in[2] == 0x78) && (in[3] == 0x6D))
  d=1   L 975  T=0 F=0  T=0 F=19  if ((in[0] == 0x3C) && (in[1] == 0x00) &&
  d=1   L 975  T=0 F=40  T=19 F=20  if ((in[0] == 0x3C) && (in[1] == 0x00) &&
  d=1   L 987  T=0 F=40  T=0 F=0  if ((in[0] == 0xEF) && (in[1] == 0xBB) &&  <-- BLOCKER
  d=1   L 987  T=40 F=0  T=0 F=39  if ((in[0] == 0xEF) && (in[1] == 0xBB) &&  <-- BLOCKER

[off-chain: 487 additional divergent branches across 51 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0a40feb3df5b3fdc, size=246 bytes, fuzzer=cmplog, trial=1, discovered_at=5742s, mutation_op=WordInterestingMutator,BytesExpandMutator,DwordAddMutator,ByteIncMutator,CrossoverReplaceMutator):
  0000: 06 2a 28 2a 2a 2a 2a 2a 2a 2a 2b 2a 2a 7e 6e 65   .*(*******+**~ne
  0010: 74 27 9f 62 20 74 65 78 74 3c 2f 62 2e 0a 3c 2f   t'.b text</b..</
  0020: 61 21 0a 0a 5c 0a ef 74 64 73 2f 31 32 37 37 37   a!..\..tds/12777
  0030: 32 2e 64 74 64 5c 0a 3c 21 45 20 3c 62 20 78 6c   2.dtd\.<!E <b xl
Seed 2 (id=075587e535715c53, size=393 bytes, fuzzer=cmplog, trial=1, discovered_at=6681s, mutation_op=BytesCopyMutator,BytesDeleteMutator,ByteIncMutator,DwordAddMutator,TokenReplace,BytesSetMutator):
  0000: 0a 3c 21 45 4c 74 74 70 3a 2f 2f 77 77 77 21 77   .<!ELttp://www!w
  0010: 33 3d 6f 72 67 26 31 39 39 39 2f 78 3a 69 6e 6b   3=org&1999/x:ink
  0020: 27 0a 3b 28 28 20 20 20 20 20 20 20 20 20 78 6c   '.;((         xl
  0030: 69 6e 6b 2d 0a 79 25 65 20 20 20 28 73 69 6d 70   ink-.y%e   (simp
Seed 3 (id=003371b638ddfc81, size=407 bytes, fuzzer=cmplog, trial=1, discovered_at=11380s, mutation_op=DwordInterestingMutator,BytesInsertCopyMutator):
  0000: 0a 3c 21 45 4c 74 74 70 3a 2f 2f 77 77 77 2e 77   .<!ELttp://www.w
  0010: 33 2e 6f 72 67 2f 31 39 39 39 2f 78 3a 28 6e 6b   3.org/1999/x:(nk
  0020: 27 72 67 2f 31 39 39 39 2f 78 3a 5f 6e 6b 2c 0a   'rg/1999/x:_nk,.
  0030: 3d 20 20 20 29 20 20 20 20 20 20 20 78 6c 69 6e   =   )       xlin
Seed 4 (id=0e0bb3d879be4298, size=156 bytes, fuzzer=cmplog, trial=1, discovered_at=16811s, mutation_op=ByteRandMutator):
  0000: 2e 55 55 2e 2e 2e 2e 2e 2e 28 2d 2a 2e 2e 55 55   .UU......(-*..UU
  0010: 2e 2e 2e 2e 2e 2e 28 2d 2a 2e 2e 2e 2e 28 2d 2a   ......(-*....(-*
  0020: 2e 2e 2e 2e 3d 26 2e 2e 28 2d 2e 2e 2e 3d 2e 2e   ....=&..(-...=..
  0030: 2e 28 2f 20 20 20 20 20 20 20 2d 2a 2e 20 20 20   .(/       -*.   
Seed 5 (id=09a32cca54963e34, size=30 bytes, fuzzer=cmplog, trial=1, discovered_at=17353s, mutation_op=ByteInterestingMutator):
  0000: f0 9f 43 44 2f 25 41 42 2a 24 29 3b 3a 49 7e 50   ..CD/%AB*$);:I~P
  0010: 4c 02 2b 5c 2e 5c 63 5c 0a ef 26 5c 5c 0a         L.+\.\c\..&\\.

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003a9c177fd1ad1c, size=201 bytes, fuzzer=naive, trial=2, discovered_at=39s, mutation_op=ByteRandMutator,WordInterestingMutator,DwordInterestingMutator,BytesDeleteMutator):
  0000: 38 38 38 38 38 49 22 31 00 31 32 37 37 37 32 2e   88888I"1.127772.
  0010: 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69   xml\.<?xml versi
  0020: 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43   on="1.0"?>.<!DOC
  0030: 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22 64   TYPE a SYSTEM "d
Seed 2 (id=008ab3952eba90c9, size=384 bytes, fuzzer=naive, trial=2, discovered_at=306s, mutation_op=BytesExpandMutator,BytesRandSetMutator,CrossoverReplaceMutator,BytesExpandMutator,BytesInsertCopyMutator):
  0000: 3d 22 31 2e 2b 70 3a 2f 22 3f 3e 0a 3c 21 44 4f   ="1.+p:/"?>.<!DO
  0010: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
  0020: 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22   dtds/127772.dtd"
  0030: 3e 0a 0a 3c 61 3e 0a 20 20 3c 62 20 78 6c 69 6e   >..<a>.  <b xlin
Seed 3 (id=00187c32cbdbd121, size=492 bytes, fuzzer=naive, trial=2, discovered_at=5331s, mutation_op=ByteNegMutator,ByteNegMutator,TokenInsert,ByteIncMutator,WordAddMutator,TokenInsert,BytesInsertMutator):
  0000: 74 74 70 3a 75 2f 2f 2f 2f 2b 2f 2f 2f 2f 2f 2f   ttp:u////+//////
  0010: 2f 2f 74 74 70 3a 2f 2f 2f 2f 2e 2b 2f 30 2f 2f   //ttp:////.+/0//
  0020: 2f 2f 2f 2f 2f 2f 2f 66 77 6b 65 3e 0a 3c 2f 61   ///////fwke>.</a
  0030: 5e 0a 0a 55 54 46 38 5c 0a 78 6c 69 6e 6b 3a 74   ^..UTF8\.xlink:t
Seed 4 (id=0009d2d8a40e2949, size=209 bytes, fuzzer=naive, trial=2, discovered_at=6150s, mutation_op=TokenInsert,BytesInsertMutator):
  0000: 27 2f 2f 2f 2f 2f 2f 2f 2f 2f 2f 68 74 74 70 3a   '//////////http:
  0010: 2f 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 33 2e   /'http://www.w3.
  0020: 6f 72 67 2f 25 39 3a 39 2f 78 6c 69 6e 6b 27 0a   org/%9:9/xlink'.
  0030: 20 fe 20 20 20 20 20 06 14 00 00 31 20 20 06 11    .     ....1  ..
Seed 5 (id=001a17f4d76ed9c3, size=47 bytes, fuzzer=naive, trial=2, discovered_at=6362s, mutation_op=CrossoverReplaceMutator,BytesExpandMutator):
  0000: 64 74 64 73 64 74 64 73 2f 73 2f 2b 2c 2b 2b 45   dtdsdtds/s/+,++E
  0010: 2f 2b 2b 2b 2b 2b 2b 2a 2b 2b d5 43 53 2d 00 d0   /++++++*++.CS-..
  0020: 01 00 6c 5c 64 5c 0a 3c 30 45 4c 45 4d 00 00      ..l\d\.<0ELEM..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0039  20( )x4 21(!)x3 45(E)x1 37(7)x1     53(S)x1 3c(<)x1 78(x)x1 00(.)x1 +4u  DIFFER
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

--- naive_ngram4 ---
**Instrumentation**: naive's edge counters, but the executor installs
an `NgramHook` (`HookableInProcessExecutor`) that folds a rolling
history of the last 4 edge IDs into the map index. A map slot
therefore encodes a length-4 edge path (an n-gram of N=4) rather than
a single edge.

**Feedback**: `MaxMapFeedback` over the n-gram-indexed map — a "new
bucket" is a previously-unseen 4-edge path tuple.

**Mutators**: naive's havoc + token stack. No I2S, no CMP_MAP. Stages
are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no dash rows.

**Per-execution cost**: edge increment plus a rolling 4-edge-history
update per executed edge.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6359.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6359,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), naive_ngram4>naive (ngram_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6359 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6359 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6359 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).