==== BLOCKER ====
Target: libxml2
Branch ID: 6687
Location: /src/libxml2/parser.c:7137:12
Enclosing function: xmlParseExternalSubset
Source line:     while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile)
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog)
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.60h  loser=19.00h
  avg hitcount on branch: winner=5  loser=1
  prob_div=0.60  dur_div=7.40h  hit_div=4
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.20h  loser=20.00h
  avg hitcount on branch: winner=4  loser=1
  prob_div=0.60  dur_div=8.80h  hit_div=4
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6687/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlParseExternalSubset (/src/libxml2/parser.c:7095-7155) ---
[ ]  7093  void
[ ]  7094  xmlParseExternalSubset(xmlParserCtxtPtr ctxt, const xmlChar *ExternalID,
[B]  7095                         const xmlChar *SystemID) {
[B]  7096      xmlDetectSAX2(ctxt);
[B]  7097      GROW;
[ ]  7098  
[B]  7099      if ((ctxt->encoding == NULL) &&
[B]  7100          (ctxt->input->end - ctxt->input->cur >= 4)) {
[B]  7101          xmlChar start[4];
[B]  7102  	xmlCharEncoding enc;
[ ]  7103  
[B]  7104  	start[0] = RAW;
[B]  7105  	start[1] = NXT(1);
[B]  7106  	start[2] = NXT(2);
[B]  7107  	start[3] = NXT(3);
[B]  7108  	enc = xmlDetectCharEncoding(start, 4);
[B]  7109  	if (enc != XML_CHAR_ENCODING_NONE)
[L]  7110  	    xmlSwitchEncoding(ctxt, enc);
[B]  7111      }
[ ]  7112  
[B]  7113      if (CMP5(CUR_PTR, '<', '?', 'x', 'm', 'l')) {
[L]  7114  	xmlParseTextDecl(ctxt);
[L]  7115  	if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
[ ]  7116  	    /*
[ ]  7117  	     * The XML REC instructs us to stop parsing right here
[ ]  7118  	     */
[ ]  7119  	    xmlHaltParser(ctxt);
[ ]  7120  	    return;
[ ]  7121  	}
[L]  7122      }
[B]  7123      if (ctxt->myDoc == NULL) {
[ ]  7124          ctxt->myDoc = xmlNewDoc(BAD_CAST "1.0");
[ ]  7125  	if (ctxt->myDoc == NULL) {
[ ]  7126  	    xmlErrMemory(ctxt, "New Doc failed");
[ ]  7127  	    return;
[ ]  7128  	}
[ ]  7129  	ctxt->myDoc->properties = XML_DOC_INTERNAL;
[ ]  7130      }
[B]  7131      if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == NULL))
[ ]  7132          xmlCreateIntSubset(ctxt->myDoc, NULL, ExternalID, SystemID);
[ ]  7133  
[B]  7134      ctxt->instate = XML_PARSER_DTD;
[B]  7135      ctxt->external = 1;
[B]  7136      SKIP_BLANKS;
[B]  7137      while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) { <-- BLOCKER
[B]  7138  	GROW;
[B]  7139          if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
[W]  7140              xmlParseConditionalSections(ctxt);
[B]  7141          } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) == '?'))) {
[B]  7142              xmlParseMarkupDecl(ctxt);
[B]  7143          } else {
[L]  7144              xmlFatalErr(ctxt, XML_ERR_EXT_SUBSET_NOT_FINISHED, NULL);
[L]  7145              xmlHaltParser(ctxt);
[L]  7146              return;
[L]  7147          }
[B]  7148          SKIP_BLANKS;
[B]  7149      }
[ ]  7150  
[B]  7151      if (RAW != 0) {
[ ]  7152  	xmlFatalErr(ctxt, XML_ERR_EXT_SUBSET_NOT_FINISHED, NULL);
[ ]  7153      }
[ ]  7154  
[B]  7155  }

--- Caller (1 hop): xmlSAX2ExternalSubset (/src/libxml2/SAX2.c:368-496, calls xmlParseExternalSubset at line 457) (±10 around call site) ---
[B]   447  	    input->filename = (char *) xmlCanonicPath(SystemID);
[B]   448  	input->line = 1;
[B]   449  	input->col = 1;
[B]   450  	input->base = ctxt->input->cur;
[B]   451  	input->cur = ctxt->input->cur;
[B]   452  	input->free = NULL;
[ ]   453  
[ ]   454  	/*
[ ]   455  	 * let's parse that entity knowing it's an external subset.
[ ]   456  	 */
[B]   457  	xmlParseExternalSubset(ctxt, ExternalID, SystemID); <-- CALL
[ ]   458  
[ ]   459          /*
[ ]   460  	 * Free up the external entities
[ ]   461  	 */
[ ]   462  
[B]   463  	while (ctxt->inputNr > 1)
[ ]   464  	    xmlPopInput(ctxt);
[ ]   465  
[B]   466          consumed = ctxt->input->consumed;
[B]   467          buffered = ctxt->input->cur - ctxt->input->base;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 2  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 3  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 4  xmlValidateDocument  (/src/libxml2/valid.c:6896-6954, calls xmlParseDTD at line 6921)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     457     11900  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
     301      7930  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
     268      7670  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      42      1550  xmlParseName  (/src/libxml2/parser.c:3368-3412)
       0       831  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
      36       711  inputPop  (/src/libxml2/parser.c:1723-1738)
      18       600  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
      24       465  parser.c:xmlDetectSAX2  (/src/libxml2/parser.c:1043-1068)
      24       465  inputPush  (/src/libxml2/parser.c:1693-1712)
      12       410  xmlParseElementDecl  (/src/libxml2/parser.c:6693-6788)
      12       394  xmlParseElementContentDecl  (/src/libxml2/parser.c:6647-6675)
       6       329  xmlParseAttributeType  (/src/libxml2/parser.c:6015-6043)
      18       324  parser.c:xmlFatalErr  (/src/libxml2/parser.c:249-453)
      16       316  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
       6       301  xmlParseDefaultDecl  (/src/libxml2/parser.c:5755-5785)
... (106 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155) ---
  d=1   L7099  T=12 F=0  T=228 F=0  if ((ctxt->encoding == NULL) &&
  d=1   L7100  T=12 F=0  T=228 F=0  (ctxt->input->end - ctxt->input->cur >= 4)) {
  d=1   L7109  T=0 F=12  T=6 F=222  if (enc != XML_CHAR_ENCODING_NONE)
  d=1   L7115  T=0 F=0  T=0 F=3  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=1   L7123  T=0 F=12  T=0 F=228  if (ctxt->myDoc == NULL) {
  d=1   L7131  T=0 F=12  T=0 F=228  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=1   L7131  T=12 F=0  T=228 F=0  if ((ctxt->myDoc != NULL) && (ctxt->myDoc->intSubset == N...
  d=1   L7137  T=30 F=12  T=828 F=0  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {  <-- BLOCKER
  d=1   L7137  T=30 F=0  T=730 F=98  while ((ctxt->instate != XML_PARSER_EOF) && (RAW != 0)) {  <-- BLOCKER
  d=1   L7139  T=30 F=0  T=595 F=8  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=1   L7139  T=30 F=0  T=603 F=127  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=1   L7139  T=12 F=18  T=0 F=595  if ((RAW == '<') && (NXT(1) == '!') && (NXT(2) == '[')) {
  d=1   L7141  T=0 F=0  T=5 F=3  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=1   L7141  T=18 F=0  T=603 F=127  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=1   L7141  T=18 F=0  T=595 F=8  } else if ((RAW == '<') && ((NXT(1) == '!') || (NXT(1) ==...
  d=1   L7151  T=0 F=12  T=0 F=98  if (RAW != 0) {

[off-chain: 1511 additional divergent branches across 115 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=c2ef14a3db44578b, size=368 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=134s, mutation_op=TokenReplace):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=52d6203fbc0f535a, size=368 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=1580s, mutation_op=ByteAddMutator,BytesRandSetMutator,BytesSwapMutator,ByteIncMutator,QwordAddMutator,QwordAddMutator,BytesSetMutator):
  0000: ff 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=e0238400d3b4fff4, size=368 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=2643s, mutation_op=ByteIncMutator,ByteRandMutator,DwordInterestingMutator,BytesSetMutator,ByteAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=fc1b1c8fd7dfad31, size=526 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=2880s, mutation_op=DwordInterestingMutator,BytesInsertCopyMutator,CrossoverInsertMutator,BytesExpandMutator,QwordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=00f7af173db700b0, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=0s, mutation_op=BytesExpandMutator,DwordAddMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=1b8864de1388e378, size=331 bytes, fuzzer=naive, trial=5, discovered_at=0s, mutation_op=BitFlipMutator,BytesRandSetMutator,CrossoverReplaceMutator,BytesDeleteMutator,BytesInsertCopyMutator):
  0000: c8 c8 c8 c8 31 32 37 ec ff ff ff 78 6d 6c 5c 0a   ....127....xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=979f009205bcfa18, size=381 bytes, fuzzer=naive, trial=5, discovered_at=0s, mutation_op=ByteIncMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=00fd268513ef89d3, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=1s, mutation_op=BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=062e97a74ea2d1b7, size=368 bytes, fuzzer=cmplog, trial=5, discovered_at=1s, mutation_op=ByteNegMutator,DwordInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x3 ff(.)x1                     06(.)x44 32(2)x3 31(1)x3 05(.)x3 +22u  PARTIAL
   0x0001  00(.)x4                             00(.)x48 32(2)x4 2e(.)x2 44(D)x2 +23u  PARTIAL
   0x0002  00(.)x4                             00(.)x50 78(x)x3 2e(.)x2 74(t)x2 +20u  PARTIAL
   0x0003  00(.)x4                             00(.)x52 6d(m)x4 74(t)x4 78(x)x3 +13u  PARTIAL
   0x0004  31(1)x4                             31(1)x49 6d(m)x4 6c(l)x3 74(t)x3 +16u  PARTIAL
   0x0005  32(2)x4                             32(2)x48 74(t)x4 6c(l)x3 5c(\)x3 +14u  PARTIAL
   0x0006  37(7)x4                             37(7)x48 3a(:)x4 0a(.)x3 74(t)x3 +15u  PARTIAL
   0x0007  37(7)x4                             37(7)x47 0a(.)x4 3a(:)x3 3c(<)x3 +16u  PARTIAL
   0x0008  37(7)x4                             37(7)x47 3a(:)x5 3c(<)x4 2f(/)x4 +15u  PARTIAL
   0x0009  32(2)x4                             32(2)x46 2f(/)x5 78(x)x3 0a(.)x2 +18u  PARTIAL
   0x000a  2e(.)x4                             2e(.)x45 6d(m)x5 2f(/)x4 20( )x3 +18u  PARTIAL
   0x000b  78(x)x4                             78(x)x46 6c(l)x4 3a(:)x3 20( )x2 +18u  PARTIAL
   0x000c  6d(m)x4                             6d(m)x46 3c(<)x3 31(1)x3 20( )x3 +15u  PARTIAL
   0x000d  6c(l)x4                             6c(l)x45 00(.)x3 76(v)x3 37(7)x2 +20u  PARTIAL
   0x000e  5c(\)x4                             5c(\)x47 65(e)x4 37(7)x3 32(2)x2 +18u  PARTIAL
   0x000f  0a(.)x4                             0a(.)x46 32(2)x3 72(r)x3 2e(.)x2 +19u  PARTIAL
   0x0010  3c(<)x4                             3c(<)x46 78(x)x3 72(r)x3 73(s)x3 +17u  PARTIAL
   0x0011  3f(?)x4                             3f(?)x46 6d(m)x3 69(i)x3 20( )x3 +18u  PARTIAL
   0x0012  78(x)x4                             78(x)x45 6f(o)x5 00(.)x3 6c(l)x3 +18u  PARTIAL
   0x0013  6d(m)x4                             6d(m)x46 31(1)x3 5c(\)x3 6e(n)x3 +16u  PARTIAL
   0x0014  6c(l)x4                             6c(l)x45 32(2)x3 3d(=)x3 0a(.)x2 +21u  PARTIAL
   0x0015  20( )x4                             20( )x45 37(7)x5 22(")x3 3c(<)x2 +19u  PARTIAL
   0x0016  76(v)x4                             76(v)x44 31(1)x4 37(7)x3 3f(?)x2 +21u  PARTIAL
   0x0017  65(e)x4                             65(e)x44 2e(.)x6 37(7)x3 31(1)x3 +19u  PARTIAL
   0x0018  72(r)x4                             72(r)x44 32(2)x3 78(x)x3 2e(.)x3 +20u  PARTIAL
   0x0019  73(s)x4                             73(s)x45 6c(l)x3 2e(.)x3 65(e)x3 +16u  PARTIAL
   0x001a  69(i)x4                             69(i)x46 78(x)x5 22(")x3 3f(?)x3 +17u  PARTIAL
   0x001b  6f(o)x4                             6f(o)x44 6d(m)x6 3f(?)x4 3e(>)x3 +17u  PARTIAL
   0x001c  6e(n)x4                             6e(n)x45 6c(l)x6 3e(>)x4 0a(.)x4 +14u  PARTIAL
   0x001d  3d(=)x4                             3d(=)x44 3c(<)x4 5c(\)x3 0a(.)x3 +17u  PARTIAL
   0x001e  22(")x4                             22(")x45 0a(.)x5 6c(l)x3 6e(n)x3 +15u  PARTIAL
   0x001f  31(1)x4                             31(1)x44 20( )x5 3c(<)x3 21(!)x3 +19u  PARTIAL
   0x0020  2e(.)x4                             2e(.)x44 76(v)x4 3f(?)x3 22(")x3 +17u  PARTIAL
   0x0021  30(0)x4                             30(0)x43 65(e)x5 78(x)x3 31(1)x3 +20u  PARTIAL
   0x0022  22(")x4                             22(")x45 72(r)x4 6d(m)x3 54(T)x3 +19u  PARTIAL
   0x0023  3f(?)x4                             3f(?)x44 73(s)x4 6c(l)x3 22(")x3 +19u  PARTIAL
   0x0024  3e(>)x4                             3e(>)x45 20( )x4 69(i)x4 22(")x3 +18u  PARTIAL
   0x0025  0a(.)x4                             0a(.)x44 6f(o)x4 76(v)x3 45(E)x3 +19u  PARTIAL
   0x0026  3c(<)x4                             3c(<)x45 6e(n)x4 20( )x4 65(e)x3 +16u  PARTIAL
   0x0027  21(!)x4                             21(!)x44 3d(=)x4 20( )x4 72(r)x3 +19u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6687.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6687,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile>naive (value_profile), value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6687 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6687 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6687 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).