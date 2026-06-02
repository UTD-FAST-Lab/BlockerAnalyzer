==== BLOCKER ====
Target: libxml2
Branch ID: 6696
Location: /src/libxml2/parser.c:8015:9
Enclosing function: xmlParsePEReference
Source line:     if (RAW != ';') {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        9          1  REFERENCE
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog)
value_profile                    4        6          0  REFERENCE
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog)
naive_ctx                        3        7          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         2        8          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.70h  loser=18.00h
  avg hitcount on branch: winner=5  loser=1
  prob_div=0.80  dur_div=10.30h  hit_div=4
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6696/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParsePEReference (/src/libxml2/parser.c:7999-8146) ---
[ ]  7997  void
[ ]  7998  xmlParsePEReference(xmlParserCtxtPtr ctxt)
[B]  7999  {
[B]  8000      const xmlChar *name;
[B]  8001      xmlEntityPtr entity = NULL;
[B]  8002      xmlParserInputPtr input;
[ ]  8003  
[B]  8004      if (RAW != '%')
[ ]  8005          return;
[B]  8006      NEXT;
[B]  8007      name = xmlParseName(ctxt);
[B]  8008      if (name == NULL) {
[L]  8009  	xmlFatalErrMsg(ctxt, XML_ERR_PEREF_NO_NAME, "PEReference: no name\n");
[L]  8010  	return;
[L]  8011      }
[B]  8012      if (xmlParserDebugEntities)
[ ]  8013  	xmlGenericError(xmlGenericErrorContext,
[ ]  8014  		"PEReference: %s\n", name);
[B]  8015      if (RAW != ';') { <-- BLOCKER
[B]  8016  	xmlFatalErr(ctxt, XML_ERR_PEREF_SEMICOL_MISSING, NULL);
[B]  8017          return;
[B]  8018      }
[ ]  8019  
[B]  8020      NEXT;
[ ]  8021  
[ ]  8022      /*
[ ]  8023       * Request the entity from SAX
[ ]  8024       */
[B]  8025      if ((ctxt->sax != NULL) &&
[B]  8026  	(ctxt->sax->getParameterEntity != NULL))
[B]  8027  	entity = ctxt->sax->getParameterEntity(ctxt->userData, name);
[B]  8028      if (ctxt->instate == XML_PARSER_EOF)
[ ]  8029  	return;
[B]  8030      if (entity == NULL) {
[ ]  8031  	/*
[ ]  8032  	 * [ WFC: Entity Declared ]
[ ]  8033  	 * In a document without any DTD, a document with only an
[ ]  8034  	 * internal DTD subset which contains no parameter entity
[ ]  8035  	 * references, or a document with "standalone='yes'", ...
[ ]  8036  	 * ... The declaration of a parameter entity must precede
[ ]  8037  	 * any reference to it...
[ ]  8038  	 */
[B]  8039  	if ((ctxt->standalone == 1) ||
[B]  8040  	    ((ctxt->hasExternalSubset == 0) &&
[B]  8041  	     (ctxt->hasPErefs == 0))) {
[W]  8042  	    xmlFatalErrMsgStr(ctxt, XML_ERR_UNDECLARED_ENTITY,
[W]  8043  			      "PEReference: %%%s; not found\n",
[W]  8044  			      name);
[B]  8045  	} else {
[ ]  8046  	    /*
[ ]  8047  	     * [ VC: Entity Declared ]
[ ]  8048  	     * In a document with an external subset or external
[ ]  8049  	     * parameter entities with "standalone='no'", ...
[ ]  8050  	     * ... The declaration of a parameter entity must
[ ]  8051  	     * precede any reference to it...
[ ]  8052  	     */
[B]  8053              if ((ctxt->validate) && (ctxt->vctxt.error != NULL)) {
[W]  8054                  xmlValidityError(ctxt, XML_WAR_UNDECLARED_ENTITY,
[W]  8055                                   "PEReference: %%%s; not found\n",
[W]  8056                                   name, NULL);
[W]  8057              } else
[B]  8058                  xmlWarningMsg(ctxt, XML_WAR_UNDECLARED_ENTITY,
[B]  8059                                "PEReference: %%%s; not found\n",
[B]  8060                                name, NULL);
[B]  8061              ctxt->valid = 0;
[B]  8062  	}
[B]  8063      } else {
[ ]  8064  	/*
[ ]  8065  	 * Internal checking in case the entity quest barfed
[ ]  8066  	 */
[ ]  8067  	if ((entity->etype != XML_INTERNAL_PARAMETER_ENTITY) &&
[ ]  8068  	    (entity->etype != XML_EXTERNAL_PARAMETER_ENTITY)) {
[ ]  8069  	    xmlWarningMsg(ctxt, XML_WAR_UNDECLARED_ENTITY,
[ ]  8070  		  "Internal: %%%s; is not a parameter entity\n",
[ ]  8071  			  name, NULL);
[ ]  8072  	} else {
[ ]  8073              xmlChar start[4];
[ ]  8074              xmlCharEncoding enc;
[ ]  8075              unsigned long parentConsumed;
[ ]  8076              xmlEntityPtr oldEnt;
[ ]  8077  
[ ]  8078  	    if ((entity->etype == XML_EXTERNAL_PARAMETER_ENTITY) &&
[ ]  8079  	        ((ctxt->options & XML_PARSE_NOENT) == 0) &&
[ ]  8080  		((ctxt->options & XML_PARSE_DTDVALID) == 0) &&
[ ]  8081  		((ctxt->options & XML_PARSE_DTDLOAD) == 0) &&
[ ]  8082  		((ctxt->options & XML_PARSE_DTDATTR) == 0) &&
[ ]  8083  		(ctxt->replaceEntities == 0) &&
[ ]  8084  		(ctxt->validate == 0))
[ ]  8085  		return;
[ ]  8086  
[ ]  8087              if (entity->flags & XML_ENT_EXPANDING) {
[ ]  8088                  xmlFatalErr(ctxt, XML_ERR_ENTITY_LOOP, NULL);
[ ]  8089                  xmlHaltParser(ctxt);
[ ]  8090                  return;
[ ]  8091              }
[ ]  8092  
[ ]  8093              /* Must be computed from old input before pushing new input. */
[ ]  8094              parentConsumed = ctxt->input->parentConsumed;
[ ]  8095              oldEnt = ctxt->input->entity;
[ ]  8096              if ((oldEnt == NULL) ||
[ ]  8097                  ((oldEnt->etype == XML_EXTERNAL_PARAMETER_ENTITY) &&
[ ]  8098                   ((oldEnt->flags & XML_ENT_PARSED) == 0))) {
[ ]  8099                  xmlSaturatedAdd(&parentConsumed, ctxt->input->consumed);
[ ]  8100                  xmlSaturatedAddSizeT(&parentConsumed,
[ ]  8101                                       ctxt->input->cur - ctxt->input->base);
[ ]  8102              }
[ ]  8103  
[ ]  8104  	    input = xmlNewEntityInputStream(ctxt, entity);
[ ]  8105  	    if (xmlPushInput(ctxt, input) < 0) {
[ ]  8106                  xmlFreeInputStream(input);
[ ]  8107  		return;
[ ]  8108              }
[ ]  8109  
[ ]  8110              entity->flags |= XML_ENT_EXPANDING;
[ ]  8111  
[ ]  8112              input->parentConsumed = parentConsumed;
[ ]  8113  
[ ]  8114  	    if (entity->etype == XML_EXTERNAL_PARAMETER_ENTITY) {
[ ]  8115                  /*
[ ]  8116                   * Get the 4 first bytes and decode the charset
[ ]  8117                   * if enc != XML_CHAR_ENCODING_NONE
[ ]  8118                   * plug some encoding conversion routines.
[ ]  8119                   * Note that, since we may have some non-UTF8
[ ]  8120                   * encoding (like UTF16, bug 135229), the 'length'
[ ]  8121                   * is not known, but we can calculate based upon
[ ]  8122                   * the amount of data in the buffer.
[ ]  8123                   */
[ ]  8124                  GROW
[ ]  8125                  if (ctxt->instate == XML_PARSER_EOF)
[ ]  8126                      return;
[ ]  8127                  if ((ctxt->input->end - ctxt->input->cur)>=4) {
[ ]  8128                      start[0] = RAW;
[ ]  8129                      start[1] = NXT(1);
[ ]  8130                      start[2] = NXT(2);
[ ]  8131                      start[3] = NXT(3);
[ ]  8132                      enc = xmlDetectCharEncoding(start, 4);
[ ]  8133                      if (enc != XML_CHAR_ENCODING_NONE) {
[ ]  8134                          xmlSwitchEncoding(ctxt, enc);
[ ]  8135                      }
[ ]  8136                  }
[ ]  8137  
[ ]  8138                  if ((CMP5(CUR_PTR, '<', '?', 'x', 'm', 'l')) &&
[ ]  8139                      (IS_BLANK_CH(NXT(5)))) {
[ ]  8140                      xmlParseTextDecl(ctxt);
[ ]  8141                  }
[ ]  8142              }
[ ]  8143  	}
[ ]  8144      }
[B]  8145      ctxt->hasPErefs = 1;
[B]  8146  }

--- Caller (1 hop): xmlSkipBlankChars (/src/libxml2/parser.c:2132-2217, calls xmlParsePEReference at line 2174) (±10 around call site) ---
[ ]  2164  
[B]  2165  	while (ctxt->instate != XML_PARSER_EOF) {
[B]  2166              if (IS_BLANK_CH(CUR)) { /* CHECKED tstblanks.xml */
[B]  2167  		NEXT;
[B]  2168  	    } else if (CUR == '%') {
[ ]  2169                  /*
[ ]  2170                   * Need to handle support of entities branching here
[ ]  2171                   */
[B]  2172  	        if ((expandPE == 0) || (IS_BLANK_CH(NXT(1))) || (NXT(1) == 0))
[B]  2173                      break;
[B]  2174  	        xmlParsePEReference(ctxt); <-- CALL
[B]  2175              } else if (CUR == 0) {
[L]  2176                  unsigned long consumed;
[L]  2177                  xmlEntityPtr ent;
[ ]  2178  
[L]  2179                  if (ctxt->inputNr <= 1)
[L]  2180                      break;
[ ]  2181  
[ ]  2182                  consumed = ctxt->input->consumed;
[ ]  2183                  xmlSaturatedAddSizeT(&consumed,
[ ]  2184                                       ctxt->input->cur - ctxt->input->base);

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlParserHandlePEReference  (/src/libxml2/parser.c:2529-2585, calls xmlParsePEReference at line 2584)
hop 2  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217, calls xmlParsePEReference at line 2174)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     444      5530  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     193      3100  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     218      2510  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      57       709  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       0       270  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      27       252  inputPop  (/src/libxml2/parser.c:1723-1738)
      18       204  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
      18       195  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
      12       188  xmlParsePEReference  (/src/libxml2/parser.c:7999-8146)  <-- enclosing
       6       165  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
      15       162  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
      15       162  inputPush  (/src/libxml2/parser.c:1693-1712)
       3       144  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       9       132  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)
      12       127  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
... (78 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217) ---
  d=2   L2139  T=218 F=0  T=2510 F=0  if (((ctxt->inputNr == 1) && (ctxt->instate != XML_PARSER...
  d=2   L2139  T=71 F=147  T=859 F=1650  if (((ctxt->inputNr == 1) && (ctxt->instate != XML_PARSER...
  d=2   L2140  T=0 F=147  T=0 F=1650  (ctxt->instate == XML_PARSER_START)) {
  d=2   L2147  T=12 F=36  T=163 F=389  if (*cur == '\n') {
  d=2   L2153  T=48 F=0  T=552 F=0  if (res < INT_MAX)
  d=2   L2155  T=0 F=48  T=14 F=538  if (*cur == 0) {
  d=2   L2163  T=141 F=6  T=1650 F=4  int expandPE = ((ctxt->external != 0) || (ctxt->inputNr !...
  d=2   L2165  T=306 F=0  T=4400 F=0  while (ctxt->instate != XML_PARSER_EOF) {
  d=2   L2168  T=12 F=144  T=188 F=1650  } else if (CUR == '%') {
  d=2   L2172  T=0 F=9  T=0 F=186  if ((expandPE == 0) || (IS_BLANK_CH(NXT(1))) || (NXT(1) =...
  d=2   L2172  T=3 F=9  T=2 F=186  if ((expandPE == 0) || (IS_BLANK_CH(NXT(1))) || (NXT(1) =...
  d=2   L2175  T=0 F=144  T=45 F=1610  } else if (CUR == 0) {
  d=2   L2179  T=0 F=0  T=45 F=0  if (ctxt->inputNr <= 1)
  d=2   L2212  T=159 F=0  T=2740 F=0  if (res < INT_MAX)
--- d=1  xmlParsePEReference  (/src/libxml2/parser.c:7999-8146) ---
  d=1   L8004  T=0 F=12  T=0 F=188  if (RAW != '%')
  d=1   L8008  T=0 F=12  T=90 F=98  if (name == NULL) {
  d=1   L8015  T=3 F=9  T=95 F=3  if (RAW != ';') {  <-- BLOCKER
  d=1   L8025  T=9 F=0  T=3 F=0  if ((ctxt->sax != NULL) &&
  d=1   L8026  T=9 F=0  T=3 F=0  (ctxt->sax->getParameterEntity != NULL))
  d=1   L8028  T=0 F=9  T=0 F=3  if (ctxt->instate == XML_PARSER_EOF)
  d=1   L8030  T=9 F=0  T=3 F=0  if (entity == NULL) {
  d=1   L8039  T=0 F=9  T=0 F=3  if ((ctxt->standalone == 1) ||
  d=1   L8040  T=3 F=6  T=0 F=3  ((ctxt->hasExternalSubset == 0) &&
  d=1   L8041  T=3 F=0  T=0 F=0  (ctxt->hasPErefs == 0))) {
  d=1   L8053  T=3 F=0  T=0 F=3  if ((ctxt->validate) && (ctxt->vctxt.error != NULL)) {
  d=1   L8053  T=3 F=3  T=3 F=0  if ((ctxt->validate) && (ctxt->vctxt.error != NULL)) {

[off-chain: 1117 additional divergent branches across 94 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=1ea1c606e0f4e543, size=368 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2936s, mutation_op=BytesInsertCopyMutator,BytesRandSetMutator,BytesRandInsertMutator,ByteIncMutator,BytesDeleteMutator,ByteAddMutator,BytesSetMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=91d353df749235a7, size=157 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=38256s, mutation_op=BytesRandInsertMutator,ByteAddMutator,ByteAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 0d 20 53 59 53 54 45 4d 0a 5b 25 ff 64 3b 3a 3f   . SYSTEM.[%.d;:?
Seed 3 (id=6a47050097729f16, size=566 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=58007s, mutation_op=ByteInterestingMutator,DwordInterestingMutator,BytesSwapMutator,BytesCopyMutator,BytesInsertCopyMutator,CrossoverInsertMutator,BytesInsertCopyMutator):
  0000: 54 20 62 20 78 6d 4a 6e 73 3a 78 6c 69 6e 06 00   T b xmJns:xlin..
  0010: 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f   ..127772.xml\.<?
  0020: 68 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30   hml version="1.0
  0030: 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20   "?>.<!DOCTYPE a 

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=745db6217bf97fe2, size=387 bytes, fuzzer=cmplog, trial=2, discovered_at=10s, mutation_op=DwordAddMutator,BytesInsertCopyMutator,BytesInsertMutator,QwordAddMutator,ByteIncMutator,ByteIncMutator):
  0000: 06 00 00 00 31 32 37 37 55 54 46 2d 31 36 37 32   ....1277UTF-1672
  0010: 2f 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   /xml\.<?xml vers
  0020: 69 6f 6e 3d 20 20 20 20 20 20 20 20 20 22 31 2e   ion=         "1.
  0030: 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61   0"?>.<!DOCTYPE a
Seed 2 (id=179a193292324501, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=24s, mutation_op=ByteAddMutator,TokenInsert,CrossoverReplaceMutator,ByteFlipMutator,BitFlipMutator,BytesSwapMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=0cbec52e461d3aa1, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=90s, mutation_op=BytesInsertCopyMutator,WordInterestingMutator,TokenInsert,ByteIncMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=5b14c6f3dd4723ac, size=368 bytes, fuzzer=cmplog, trial=3, discovered_at=1884s, mutation_op=BitFlipMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=134af14fb3d5e76e, size=379 bytes, fuzzer=cmplog, trial=1, discovered_at=3398s, mutation_op=BytesDeleteMutator,ByteIncMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x2 54(T)x1                     06(.)x12 37(7)x4 27(')x2 31(1)x1 +9u  PARTIAL
   0x0001  00(.)x2 20( )x1                     00(.)x14 37(7)x6 32(2)x1 9d(.)x1 +6u  PARTIAL
   0x0002  00(.)x2 62(b)x1                     00(.)x14 37(7)x5 74(t)x2 9d(.)x1 +6u  PARTIAL
   0x0003  00(.)x2 20( )x1                     00(.)x15 32(2)x3 37(7)x2 74(t)x2 +6u  PARTIAL
   0x0004  31(1)x2 78(x)x1                     31(1)x14 2e(.)x3 00(.)x2 70(p)x2 +7u  PARTIAL
   0x0005  32(2)x2 6d(m)x1                     32(2)x15 78(x)x3 00(.)x2 2e(.)x1 +7u  PARTIAL
   0x0006  37(7)x2 4a(J)x1                     37(7)x15 6d(m)x3 00(.)x2 2e(.)x1 +7u  PARTIAL
   0x0007  37(7)x2 6e(n)x1                     37(7)x15 6c(l)x3 00(.)x2 78(x)x1 +7u  PARTIAL
   0x0008  37(7)x2 73(s)x1                     37(7)x16 5c(\)x3 55(U)x1 6d(m)x1 +7u  PARTIAL
   0x0009  32(2)x2 3a(:)x1                     32(2)x16 0a(.)x3 77(w)x2 54(T)x1 +6u  PARTIAL
   0x000a  2e(.)x2 78(x)x1                     2e(.)x15 3c(<)x3 77(w)x2 37(7)x2 +6u  PARTIAL
   0x000b  78(x)x2 6c(l)x1                     78(x)x15 3f(?)x3 0a(.)x2 2e(.)x2 +5u  PARTIAL
   0x000c  6d(m)x2 69(i)x1                     6d(m)x16 78(x)x3 37(7)x2 31(1)x1 +6u  PARTIAL
   0x000d  6c(l)x2 6e(n)x1                     6c(l)x16 6d(m)x3 36(6)x1 3f(?)x1 +7u  PARTIAL
   0x000e  5c(\)x2 06(.)x1                     5c(\)x15 6c(l)x3 2e(.)x2 37(7)x1 +7u  PARTIAL
   0x000f  0a(.)x2 00(.)x1                     0a(.)x15 20( )x3 32(2)x1 6d(m)x1 +8u  PARTIAL
   0x0010  3c(<)x2 00(.)x1                     3c(<)x15 76(v)x3 2f(/)x2 6c(l)x1 +7u  PARTIAL
   0x0011  3f(?)x2 00(.)x1                     3f(?)x15 65(e)x3 20( )x2 72(r)x2 +6u  PARTIAL
   0x0012  78(x)x2 31(1)x1                     78(x)x15 72(r)x3 2f(/)x2 6d(m)x1 +7u  PARTIAL
   0x0013  6d(m)x2 32(2)x1                     6d(m)x15 73(s)x3 6c(l)x1 65(e)x1 +8u  PARTIAL
   0x0014  6c(l)x2 37(7)x1                     6c(l)x15 69(i)x3 5c(\)x1 72(r)x1 +8u  PARTIAL
   0x0015  20( )x2 37(7)x1                     20( )x15 6f(o)x3 0a(.)x2 39(9)x2 +6u  PARTIAL
   0x0016  76(v)x2 37(7)x1                     76(v)x15 6e(n)x3 39(9)x2 3c(<)x1 +7u  PARTIAL
   0x0017  65(e)x2 32(2)x1                     65(e)x15 3d(=)x3 2f(/)x2 3f(?)x1 +7u  PARTIAL
   0x0018  72(r)x2 2e(.)x1                     72(r)x15 22(")x3 78(x)x2 6e(n)x1 +7u  PARTIAL
   0x0019  73(s)x2 78(x)x1                     73(s)x15 31(1)x3 2e(.)x2 6c(l)x2 +6u  PARTIAL
   0x001a  69(i)x2 6d(m)x1                     69(i)x16 2e(.)x3 6c(l)x2 22(")x1 +6u  PARTIAL
   0x001b  6f(o)x2 6c(l)x1                     6f(o)x15 30(0)x3 20( )x1 31(1)x1 +8u  PARTIAL
   0x001c  6e(n)x2 5c(\)x1                     6e(n)x16 22(")x3 76(v)x1 2e(.)x1 +7u  PARTIAL
   0x001d  3d(=)x2 0a(.)x1                     3d(=)x15 3f(?)x3 65(e)x1 30(0)x1 +8u  PARTIAL
   0x001e  22(")x2 3c(<)x1                     22(")x16 3e(>)x4 0a(.)x2 72(r)x1 +5u  PARTIAL
   0x001f  31(1)x2 3f(?)x1                     31(1)x15 0a(.)x4 73(s)x1 3f(?)x1 +7u  PARTIAL
   0x0020  2e(.)x2 68(h)x1                     2e(.)x15 3c(<)x4 69(i)x1 3e(>)x1 +7u  PARTIAL
   0x0021  30(0)x2 6d(m)x1                     30(0)x15 21(!)x3 0a(.)x2 20( )x2 +6u  PARTIAL
   0x0022  22(")x2 6c(l)x1                     22(")x15 44(D)x3 3c(<)x2 20( )x2 +6u  PARTIAL
   0x0023  3f(?)x2 20( )x1                     3f(?)x16 4f(O)x3 20( )x2 3d(=)x1 +6u  PARTIAL
   0x0024  3e(>)x2 76(v)x1                     3e(>)x15 20( )x3 43(C)x3 44(D)x1 +6u  PARTIAL
   0x0025  0a(.)x2 65(e)x1                     0a(.)x15 20( )x3 54(T)x3 4f(O)x1 +6u  PARTIAL
   0x0026  3c(<)x2 72(r)x1                     3c(<)x15 20( )x3 59(Y)x3 43(C)x1 +6u  PARTIAL
   0x0027  21(!)x2 73(s)x1                     21(!)x15 20( )x3 50(P)x3 5f(_)x2 +5u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6696.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6696,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6696 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6696 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6696 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).