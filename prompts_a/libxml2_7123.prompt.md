==== BLOCKER ====
Target: libxml2
Branch ID: 7123
Location: /src/libxml2/valid.c:3555:6
Enclosing function: valid.c:xmlIsDocNameChar
Source line: 	    (c == '_') || (c == ':') ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (grimoire_structural vs grimoire)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog             4        6          0  REFERENCE
naive_ctx                        3        6          1  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             0        9          1  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=15.10h  loser=20.30h
  avg hitcount on branch: winner=70  loser=1
  prob_div=0.70  dur_div=5.20h  hit_div=69
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7123/{W,L}/branch_coverage_show.txt

--- Enclosing function: valid.c:xmlIsDocNameChar (/src/libxml2/valid.c:3546-3581) ---
[ ]  3544  
[ ]  3545  static int
[B]  3546  xmlIsDocNameChar(xmlDocPtr doc, int c) {
[B]  3547      if ((doc == NULL) || (doc->properties & XML_DOC_OLD10) == 0) {
[ ]  3548          /*
[ ]  3549  	 * Use the new checks of production [4] [4a] amd [5] of the
[ ]  3550  	 * Update 5 of XML-1.0
[ ]  3551  	 */
[B]  3552  	if (((c >= 'a') && (c <= 'z')) ||
[B]  3553  	    ((c >= 'A') && (c <= 'Z')) ||
[B]  3554  	    ((c >= '0') && (c <= '9')) || /* !start */
[B]  3555  	    (c == '_') || (c == ':') || <-- BLOCKER
[B]  3556  	    (c == '-') || (c == '.') || (c == 0xB7) || /* !start */
[B]  3557  	    ((c >= 0xC0) && (c <= 0xD6)) ||
[B]  3558  	    ((c >= 0xD8) && (c <= 0xF6)) ||
[B]  3559  	    ((c >= 0xF8) && (c <= 0x2FF)) ||
[B]  3560  	    ((c >= 0x300) && (c <= 0x36F)) || /* !start */
[B]  3561  	    ((c >= 0x370) && (c <= 0x37D)) ||
[B]  3562  	    ((c >= 0x37F) && (c <= 0x1FFF)) ||
[B]  3563  	    ((c >= 0x200C) && (c <= 0x200D)) ||
[B]  3564  	    ((c >= 0x203F) && (c <= 0x2040)) || /* !start */
[B]  3565  	    ((c >= 0x2070) && (c <= 0x218F)) ||
[B]  3566  	    ((c >= 0x2C00) && (c <= 0x2FEF)) ||
[B]  3567  	    ((c >= 0x3001) && (c <= 0xD7FF)) ||
[B]  3568  	    ((c >= 0xF900) && (c <= 0xFDCF)) ||
[B]  3569  	    ((c >= 0xFDF0) && (c <= 0xFFFD)) ||
[B]  3570  	    ((c >= 0x10000) && (c <= 0xEFFFF)))
[B]  3571  	     return(1);
[B]  3572      } else {
[ ]  3573          if ((IS_LETTER(c)) || (IS_DIGIT(c)) ||
[ ]  3574              (c == '.') || (c == '-') ||
[ ]  3575  	    (c == '_') || (c == ':') ||
[ ]  3576  	    (IS_COMBINING(c)) ||
[ ]  3577  	    (IS_EXTENDER(c)))
[ ]  3578  	    return(1);
[ ]  3579      }
[B]  3580      return(0);
[B]  3581  }

--- Caller (1 hop): valid.c:xmlValidateNmtokensValueInternal (/src/libxml2/valid.c:3765-3810, calls valid.c:xmlIsDocNameChar at line 3779) (±10 around call site) ---
[B]  3769      if (value == NULL) return(0);
[B]  3770      cur = value;
[B]  3771      val = xmlStringCurrentChar(NULL, cur, &len);
[B]  3772      cur += len;
[ ]  3773  
[B]  3774      while (IS_BLANK(val)) {
[ ]  3775  	val = xmlStringCurrentChar(NULL, cur, &len);
[ ]  3776  	cur += len;
[ ]  3777      }
[ ]  3778  
[B]  3779      if (!xmlIsDocNameChar(doc, val)) <-- CALL
[ ]  3780  	return(0);
[ ]  3781  
[B]  3782      while (xmlIsDocNameChar(doc, val)) {
[B]  3783  	val = xmlStringCurrentChar(NULL, cur, &len);
[B]  3784  	cur += len;
[B]  3785      }
[ ]  3786  
[ ]  3787      /* Should not test IS_BLANK(val) here -- see erratum E20*/
[B]  3788      while (val == 0x20) {
[B]  3789  	while (val == 0x20) {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  valid.c:xmlValidateNameValueInternal  (/src/libxml2/valid.c:3594-3615, calls valid.c:xmlIsDocNameChar at line 3607)
hop 2  valid.c:xmlValidateNamesValueInternal  (/src/libxml2/valid.c:3642-3683, calls valid.c:xmlIsDocNameChar at line 3656)
hop 3  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883, calls valid.c:xmlValidateNameValueInternal at line 3873)
hop 3  xmlValidateNameValue  (/src/libxml2/valid.c:3627-3629, calls valid.c:xmlValidateNameValueInternal at line 3628)
hop 3  xmlValidateNamesValue  (/src/libxml2/valid.c:3695-3697, calls valid.c:xmlValidateNamesValueInternal at line 3696)
hop 4  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172, calls valid.c:xmlValidateAttributeValueInternal at line 2018)
hop 4  xmlValidateAttributeValue  (/src/libxml2/valid.c:3910-3912, calls valid.c:xmlValidateAttributeValueInternal at line 3911)
hop 5  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758, calls xmlAddAttributeDecl at line 731)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     222      1250  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)  <-- enclosing
       6       370  valid.c:xmlFreeAttributeTableEntry  (/src/libxml2/valid.c:2175-2177)
       6       370  valid.c:xmlGetDtdElementDesc2  (/src/libxml2/valid.c:3280-3334)
       9       370  valid.c:xmlFreeAttribute  (/src/libxml2/valid.c:1907-1939)
       9       370  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172)
      12       313  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883)
       6       289  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)
       6       280  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
       6       280  valid.c:xmlFreeElement  (/src/libxml2/valid.c:1382-1395)
       6       280  valid.c:xmlFreeElementTableEntry  (/src/libxml2/valid.c:1623-1625)
       6       274  xmlAddElementDecl  (/src/libxml2/valid.c:1414-1620)
       0       260  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
       6       155  valid.c:xmlValidateNmtokensValueInternal  (/src/libxml2/valid.c:3765-3810)
       3       140  xmlFreeElementTable  (/src/libxml2/valid.c:1634-1636)
       3       140  xmlCreateEnumeration  (/src/libxml2/valid.c:1788-1801)
... (24 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172) ---
  d=4   L1970  T=0 F=9  T=0 F=370  if (dtd == NULL) {
  d=4   L1974  T=0 F=9  T=0 F=370  if (name == NULL) {
  d=4   L1978  T=0 F=9  T=0 F=370  if (elem == NULL) {
  d=4   L1982  T=9 F=0  T=370 F=0  if (dtd->doc != NULL)
  d=4   L1990  T=6 F=3  T=230 F=140  case XML_ATTRIBUTE_CDATA:
  d=4   L1992  T=0 F=9  T=0 F=370  case XML_ATTRIBUTE_ID:
  d=4   L1994  T=0 F=9  T=0 F=370  case XML_ATTRIBUTE_IDREF:
  d=4   L1996  T=0 F=9  T=0 F=370  case XML_ATTRIBUTE_IDREFS:
  d=4   L1998  T=0 F=9  T=0 F=370  case XML_ATTRIBUTE_ENTITY:
  d=4   L2000  T=0 F=9  T=0 F=370  case XML_ATTRIBUTE_ENTITIES:
  d=4   L2002  T=0 F=9  T=0 F=370  case XML_ATTRIBUTE_NMTOKEN:
  d=4   L2004  T=0 F=9  T=0 F=370  case XML_ATTRIBUTE_NMTOKENS:
  d=4   L2006  T=3 F=6  T=140 F=230  case XML_ATTRIBUTE_ENUMERATION:
  d=4   L2008  T=0 F=9  T=0 F=370  case XML_ATTRIBUTE_NOTATION:
  d=4   L2010  T=0 F=9  T=0 F=370  default:
  d=4   L2017  T=6 F=3  T=280 F=90  if ((defaultValue != NULL) &&
  d=4   L2018  T=0 F=6  T=0 F=280  (!xmlValidateAttributeValueInternal(dtd->doc, type, defau...
  d=4   L2032  T=9 F=0  T=370 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=4   L2032  T=9 F=0  T=370 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=4   L2033  T=9 F=0  T=370 F=0  (dtd->doc->intSubset != NULL) &&
  d=4   L2034  T=0 F=9  T=0 F=370  (dtd->doc->intSubset->attributes != NULL)) {
  d=4   L2046  T=3 F=6  T=140 F=230  if (table == NULL) {
  d=4   L2050  T=0 F=9  T=0 F=370  if (table == NULL) {
  d=4   L2059  T=0 F=9  T=0 F=370  if (ret == NULL) {
  d=4   L2077  T=0 F=9  T=307 F=63  if (dict) {
  d=4   L2088  T=6 F=3  T=280 F=90  if (defaultValue != NULL) {
  d=4   L2089  T=0 F=6  T=232 F=48  if (dict)
  d=4   L2099  T=3 F=6  T=0 F=370  if (xmlHashAddEntry3(table, ret->name, ret->prefix, ret->...
  d=4   L2117  T=6 F=0  T=370 F=0  if (elemDef != NULL) {
  d=4   L2120  T=0 F=6  T=0 F=370  if ((type == XML_ATTRIBUTE_ID) &&
  d=4   L2134  T=0 F=6  T=6 F=364  if ((xmlStrEqual(ret->name, BAD_CAST "xmlns")) ||
  d=4   L2135  T=3 F=3  T=331 F=33  ((ret->prefix != NULL &&
  d=4   L2136  T=0 F=3  T=98 F=233  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns"))))) {
  d=4   L2142  T=3 F=3  T=233 F=39  while ((tmp != NULL) &&
  d=4   L2143  T=0 F=3  T=12 F=221  ((xmlStrEqual(tmp->name, BAD_CAST "xmlns")) ||
  d=4   L2144  T=3 F=0  T=206 F=15  ((ret->prefix != NULL &&
  d=4   L2145  T=0 F=3  T=0 F=206  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns")))))) {
  d=4   L2146  T=0 F=0  T=6 F=6  if (tmp->nexth == NULL)
  d=4   L2150  T=3 F=3  T=227 F=39  if (tmp != NULL) {
  d=4   L2164  T=0 F=6  T=0 F=370  if (dtd->last == NULL) {
--- d=3  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883) ---
  d=3   L3865  T=0 F=12  T=0 F=313  switch (type) {
  d=3   L3866  T=0 F=12  T=0 F=313  case XML_ATTRIBUTE_ENTITIES:
  d=3   L3867  T=0 F=12  T=0 F=313  case XML_ATTRIBUTE_IDREFS:
  d=3   L3869  T=0 F=12  T=0 F=313  case XML_ATTRIBUTE_ENTITY:
  d=3   L3870  T=0 F=12  T=0 F=313  case XML_ATTRIBUTE_IDREF:
  d=3   L3871  T=0 F=12  T=0 F=313  case XML_ATTRIBUTE_ID:
  d=3   L3872  T=0 F=12  T=0 F=313  case XML_ATTRIBUTE_NOTATION:
  d=3   L3874  T=0 F=12  T=0 F=313  case XML_ATTRIBUTE_NMTOKENS:
  d=3   L3875  T=6 F=6  T=155 F=158  case XML_ATTRIBUTE_ENUMERATION:
  d=3   L3877  T=0 F=12  T=0 F=313  case XML_ATTRIBUTE_NMTOKEN:
  d=3   L3879  T=6 F=6  T=158 F=155  case XML_ATTRIBUTE_CDATA:
--- d=1  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581) ---
  d=1   L3547  T=222 F=0  T=1250 F=0  if ((doc == NULL) || (doc->properties & XML_DOC_OLD10) ==...
  d=1   L3547  T=0 F=222  T=0 F=1250  if ((doc == NULL) || (doc->properties & XML_DOC_OLD10) ==...
  d=1   L3552  T=54 F=168  T=1070 F=176  if (((c >= 'a') && (c <= 'z')) ||
  d=1   L3552  T=54 F=0  T=1070 F=0  if (((c >= 'a') && (c <= 'z')) ||
  d=1   L3553  T=54 F=60  T=12 F=0  ((c >= 'A') && (c <= 'Z')) ||
  d=1   L3554  T=6 F=60  T=3 F=0  ((c >= '0') && (c <= '9')) || /* !start */
  d=1   L3555  T=60 F=48  T=0 F=161  (c == '_') || (c == ':') ||  <-- BLOCKER
  d=1   L3555  T=0 F=48  T=0 F=161  (c == '_') || (c == ':') ||  <-- BLOCKER
  d=1   L3556  T=0 F=48  T=3 F=158  (c == '-') || (c == '.') || (c == 0xB7) || /* !start */
  d=1   L3556  T=0 F=48  T=0 F=158  (c == '-') || (c == '.') || (c == 0xB7) || /* !start */
  d=1   L3556  T=0 F=48  T=0 F=158  (c == '-') || (c == '.') || (c == 0xB7) || /* !start */
  d=1   L3557  T=0 F=48  T=0 F=158  ((c >= 0xC0) && (c <= 0xD6)) ||
  d=1   L3558  T=0 F=48  T=0 F=158  ((c >= 0xD8) && (c <= 0xF6)) ||
  d=1   L3559  T=0 F=48  T=0 F=158  ((c >= 0xF8) && (c <= 0x2FF)) ||
  d=1   L3560  T=0 F=48  T=0 F=158  ((c >= 0x300) && (c <= 0x36F)) || /* !start */
  d=1   L3561  T=0 F=48  T=0 F=158  ((c >= 0x370) && (c <= 0x37D)) ||
  d=1   L3562  T=0 F=48  T=0 F=158  ((c >= 0x37F) && (c <= 0x1FFF)) ||
  d=1   L3563  T=0 F=48  T=0 F=158  ((c >= 0x200C) && (c <= 0x200D)) ||
  d=1   L3564  T=0 F=48  T=0 F=158  ((c >= 0x203F) && (c <= 0x2040)) || /* !start */
  d=1   L3565  T=0 F=48  T=0 F=158  ((c >= 0x2070) && (c <= 0x218F)) ||
  d=1   L3566  T=0 F=48  T=0 F=158  ((c >= 0x2C00) && (c <= 0x2FEF)) ||
  d=1   L3567  T=0 F=48  T=0 F=158  ((c >= 0x3001) && (c <= 0xD7FF)) ||
  d=1   L3568  T=0 F=48  T=0 F=158  ((c >= 0xF900) && (c <= 0xFDCF)) ||
  d=1   L3569  T=0 F=48  T=0 F=158  ((c >= 0xFDF0) && (c <= 0xFFFD)) ||
  d=1   L3570  T=0 F=48  T=0 F=158  ((c >= 0x10000) && (c <= 0xEFFFF)))

[off-chain: 326 additional divergent branches across 32 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=7ad8f014dc0faf86, size=233 bytes, fuzzer=grimoire, trial=1, discovered_at=55902s, mutation_op=BytesRandInsertMutator):
  0000: fe ff 10 00 06 00 32 6c 5c 0a 3c 3f 6c 3f 3e 3c   ......2l\.<?l?><
  0010: 21 44 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d   !DOCTYPEa SYSTEM
  0020: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
  0030: 64 22 3e 5c 0a 64 74 64 73 2f 31 32 37 37 37 32   d">\.dtds/127772

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00f7af173db700b0, size=368 bytes, fuzzer=cmplog, trial=2, discovered_at=0s, mutation_op=BytesExpandMutator,DwordAddMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=3e1acbd4982eb4a1, size=363 bytes, fuzzer=cmplog, trial=1, discovered_at=0s, mutation_op=BytesRandSetMutator,BytesInsertMutator,BitFlipMutator,ByteDecMutator,BytesDeleteMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2d 78 6d 6c 5c 0a   ....127772-xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=743a758b7f4e28eb, size=368 bytes, fuzzer=cmplog, trial=3, discovered_at=0s):
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
   0x0000  fe(.)x1                             06(.)x30 3d(=)x2 05(.)x2 2d(-)x1 +12u  DIFFER
   0x0001  ff(.)x1                             00(.)x36 3d(=)x2 78(x)x1 64(d)x1 +7u  PARTIAL
   0x0002  10(.)x1                             00(.)x37 64(d)x2 3d(=)x2 6d(m)x1 +5u  DIFFER
   0x0003  00(.)x1                             00(.)x35 3d(=)x2 54(T)x2 6c(l)x1 +7u  PARTIAL
   0x0004  06(.)x1                             31(1)x35 3d(=)x2 41(A)x2 5c(\)x1 +7u  PARTIAL
   0x0005  00(.)x1                             32(2)x37 29())x2 0a(.)x1 55(U)x1 +6u  PARTIAL
   0x0006  32(2)x1                             37(7)x38 3e(>)x2 00(.)x2 3c(<)x1 +4u  PARTIAL
   0x0007  6c(l)x1                             37(7)x38 0a(.)x2 00(.)x2 3f(?)x1 +4u  DIFFER
   0x0008  5c(\)x1                             37(7)x38 55(U)x2 3c(<)x2 78(x)x1 +4u  DIFFER
   0x0009  0a(.)x1                             32(2)x39 21(!)x2 6d(m)x1 54(T)x1 +4u  DIFFER
   0x000a  3c(<)x1                             2e(.)x36 41(A)x2 32(2)x2 2d(-)x1 +6u  DIFFER
   0x000b  3f(?)x1                             78(x)x35 20( )x3 54(T)x2 37(7)x2 +5u  DIFFER
   0x000c  6c(l)x1                             6d(m)x36 20( )x2 54(T)x2 37(7)x2 +5u  DIFFER
   0x000d  3f(?)x1                             6c(l)x36 20( )x2 4c(L)x2 65(e)x1 +6u  DIFFER
   0x000e  3e(>)x1                             5c(\)x38 49(I)x2 72(r)x1 37(7)x1 +5u  DIFFER
   0x000f  3c(<)x1                             0a(.)x38 53(S)x2 73(s)x1 32(2)x1 +5u  DIFFER
   0x0010  21(!)x1                             3c(<)x38 54(T)x2 69(i)x1 2e(.)x1 +5u  DIFFER
   0x0011  44(D)x1                             3f(?)x38 20( )x2 6f(o)x1 78(x)x1 +5u  DIFFER
   0x0012  4f(O)x1                             78(x)x37 00(.)x2 6e(n)x1 6d(m)x1 +6u  DIFFER
   0x0013  43(C)x1                             6d(m)x38 31(1)x2 3d(=)x1 6c(l)x1 +5u  DIFFER
   0x0014  54(T)x1                             6c(l)x38 32(2)x2 22(")x1 5c(\)x1 +5u  DIFFER
   0x0015  59(Y)x1                             20( )x36 37(7)x3 0a(.)x2 31(1)x1 +5u  DIFFER
   0x0016  50(P)x1                             76(v)x37 37(7)x2 2e(.)x1 3c(<)x1 +6u  DIFFER
   0x0017  45(E)x1                             65(e)x37 2e(.)x2 37(7)x2 30(0)x1 +5u  DIFFER
   0x0018  61(a)x1                             72(r)x37 78(x)x2 32(2)x2 22(")x1 +5u  DIFFER
   0x0019  20( )x1                             73(s)x37 6d(m)x2 2e(.)x2 3f(?)x1 +5u  PARTIAL
   0x001a  53(S)x1                             69(i)x37 6c(l)x2 78(x)x2 3e(>)x1 +5u  DIFFER
   0x001b  59(Y)x1                             6f(o)x37 20( )x2 6d(m)x2 0a(.)x1 +5u  DIFFER
   0x001c  53(S)x1                             6e(n)x37 0a(.)x2 6c(l)x2 3c(<)x1 +5u  DIFFER
   0x001d  54(T)x1                             3d(=)x37 3c(<)x2 5c(\)x2 21(!)x1 +5u  DIFFER
   0x001e  45(E)x1                             22(")x37 0a(.)x2 44(D)x1 72(r)x1 +6u  DIFFER
   0x001f  4d(M)x1                             31(1)x37 3c(<)x2 4f(O)x1 73(s)x1 +6u  DIFFER
   0x0020  20( )x1                             2e(.)x37 3f(?)x2 43(C)x1 69(i)x1 +6u  DIFFER
   0x0021  22(")x1                             30(0)x37 78(x)x2 54(T)x1 6f(o)x1 +6u  DIFFER
   0x0022  64(d)x1                             22(")x37 6d(m)x2 59(Y)x1 6e(n)x1 +6u  DIFFER
   0x0023  74(t)x1                             3f(?)x38 6c(l)x2 50(P)x1 3d(=)x1 +5u  DIFFER
   0x0024  64(d)x1                             3e(>)x37 65(e)x2 20( )x2 45(E)x1 +5u  DIFFER
   0x0025  73(s)x1                             0a(.)x37 76(v)x2 20( )x1 31(1)x1 +6u  DIFFER
   0x0026  2f(/)x1                             3c(<)x37 65(e)x2 61(a)x1 2e(.)x1 +6u  DIFFER
   0x0027  31(1)x1                             21(!)x37 20( )x2 72(r)x2 22(")x2 +4u  DIFFER
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_7123.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7123,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7123 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7123 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7123 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).