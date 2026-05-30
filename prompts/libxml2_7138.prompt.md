==== BLOCKER ====
Target: libxml2
Branch ID: 7138
Location: /src/libxml2/valid.c:3573:31
Enclosing function: valid.c:xmlIsDocNameChar
Source line:         if ((IS_LETTER(c)) || (IS_DIGIT(c)) ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            4        4          2  REFERENCE
cmplog                           1        9          0  loser (grimoire_structural vs grimoire); loser (value_profile vs value_profile_cmplog)
value_profile                    8        2          0  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        5        4          1  REFERENCE
naive_ngram4                     1        6          3  REFERENCE
mopt                             1        5          4  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             2        6          2  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (2) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=4.50h  loser=20.10h
  avg hitcount on branch: winner=170  loser=8
  prob_div=0.90  dur_div=15.60h  hit_div=162
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002
--- Pair 2: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=7.30h  loser=20.10h
  avg hitcount on branch: winner=99  loser=8
  prob_div=0.70  dur_div=12.80h  hit_div=91
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7138/{W,L}/branch_coverage_show.txt

--- Enclosing function: valid.c:xmlIsDocNameChar (/src/libxml2/valid.c:3546-3581) ---
[ ]  3544  
[ ]  3545  static int
[B]  3546  xmlIsDocNameChar(xmlDocPtr doc, int c) {
[B]  3547      if ((doc == NULL) || (doc->properties & XML_DOC_OLD10) == 0) {
[ ]  3548          /*
[ ]  3549  	 * Use the new checks of production [4] [4a] amd [5] of the
[ ]  3550  	 * Update 5 of XML-1.0
[ ]  3551  	 */
[ ]  3552  	if (((c >= 'a') && (c <= 'z')) ||
[ ]  3553  	    ((c >= 'A') && (c <= 'Z')) ||
[ ]  3554  	    ((c >= '0') && (c <= '9')) || /* !start */
[ ]  3555  	    (c == '_') || (c == ':') ||
[ ]  3556  	    (c == '-') || (c == '.') || (c == 0xB7) || /* !start */
[ ]  3557  	    ((c >= 0xC0) && (c <= 0xD6)) ||
[ ]  3558  	    ((c >= 0xD8) && (c <= 0xF6)) ||
[ ]  3559  	    ((c >= 0xF8) && (c <= 0x2FF)) ||
[ ]  3560  	    ((c >= 0x300) && (c <= 0x36F)) || /* !start */
[ ]  3561  	    ((c >= 0x370) && (c <= 0x37D)) ||
[ ]  3562  	    ((c >= 0x37F) && (c <= 0x1FFF)) ||
[ ]  3563  	    ((c >= 0x200C) && (c <= 0x200D)) ||
[ ]  3564  	    ((c >= 0x203F) && (c <= 0x2040)) || /* !start */
[ ]  3565  	    ((c >= 0x2070) && (c <= 0x218F)) ||
[ ]  3566  	    ((c >= 0x2C00) && (c <= 0x2FEF)) ||
[ ]  3567  	    ((c >= 0x3001) && (c <= 0xD7FF)) ||
[ ]  3568  	    ((c >= 0xF900) && (c <= 0xFDCF)) ||
[ ]  3569  	    ((c >= 0xFDF0) && (c <= 0xFFFD)) ||
[ ]  3570  	    ((c >= 0x10000) && (c <= 0xEFFFF)))
[ ]  3571  	     return(1);
[B]  3572      } else {
[B]  3573          if ((IS_LETTER(c)) || (IS_DIGIT(c)) || <-- BLOCKER
[B]  3574              (c == '.') || (c == '-') ||
[B]  3575  	    (c == '_') || (c == ':') ||
[B]  3576  	    (IS_COMBINING(c)) ||
[B]  3577  	    (IS_EXTENDER(c)))
[B]  3578  	    return(1);
[B]  3579      }
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
       0       394  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
      72       360  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
      84       285  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883)
      57       252  valid.c:xmlFreeAttributeTableEntry  (/src/libxml2/valid.c:2175-2177)
      57       252  valid.c:xmlGetDtdElementDesc2  (/src/libxml2/valid.c:3280-3334)
      69       252  valid.c:xmlFreeAttribute  (/src/libxml2/valid.c:1907-1939)
      69       252  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172)
       0       160  xmlGetDtdQElementDesc  (/src/libxml2/valid.c:3349-3357)
       0       141  valid.c:xmlValidateAttributeCallback  (/src/libxml2/valid.c:6762-6830)
      54       192  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)
      54       192  valid.c:xmlFreeElement  (/src/libxml2/valid.c:1382-1395)
      54       192  valid.c:xmlFreeElementTableEntry  (/src/libxml2/valid.c:1623-1625)
      54       174  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
      54       174  xmlAddElementDecl  (/src/libxml2/valid.c:1414-1620)
       0        98  xmlGetDtdQAttrDesc  (/src/libxml2/valid.c:3410-3418)
... (32 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172) ---
  d=4   L1970  T=0 F=69  T=0 F=252  if (dtd == NULL) {
  d=4   L1974  T=0 F=69  T=0 F=252  if (name == NULL) {
  d=4   L1978  T=0 F=69  T=0 F=252  if (elem == NULL) {
  d=4   L1982  T=69 F=0  T=252 F=0  if (dtd->doc != NULL)
  d=4   L1990  T=42 F=27  T=162 F=90  case XML_ATTRIBUTE_CDATA:
  d=4   L1992  T=0 F=69  T=0 F=252  case XML_ATTRIBUTE_ID:
  d=4   L1994  T=0 F=69  T=0 F=252  case XML_ATTRIBUTE_IDREF:
  d=4   L1996  T=0 F=69  T=0 F=252  case XML_ATTRIBUTE_IDREFS:
  d=4   L1998  T=0 F=69  T=0 F=252  case XML_ATTRIBUTE_ENTITY:
  d=4   L2000  T=0 F=69  T=0 F=252  case XML_ATTRIBUTE_ENTITIES:
  d=4   L2002  T=0 F=69  T=0 F=252  case XML_ATTRIBUTE_NMTOKEN:
  d=4   L2004  T=0 F=69  T=0 F=252  case XML_ATTRIBUTE_NMTOKENS:
  d=4   L2006  T=27 F=42  T=90 F=162  case XML_ATTRIBUTE_ENUMERATION:
  d=4   L2008  T=0 F=69  T=0 F=252  case XML_ATTRIBUTE_NOTATION:
  d=4   L2010  T=0 F=69  T=0 F=252  default:
  d=4   L2017  T=51 F=18  T=177 F=75  if ((defaultValue != NULL) &&
  d=4   L2018  T=0 F=51  T=0 F=177  (!xmlValidateAttributeValueInternal(dtd->doc, type, defau...
  d=4   L2032  T=69 F=0  T=252 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=4   L2032  T=69 F=0  T=252 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=4   L2033  T=69 F=0  T=252 F=0  (dtd->doc->intSubset != NULL) &&
  d=4   L2034  T=0 F=69  T=0 F=252  (dtd->doc->intSubset->attributes != NULL)) {
  d=4   L2046  T=27 F=42  T=87 F=165  if (table == NULL) {
  d=4   L2050  T=0 F=69  T=0 F=252  if (table == NULL) {
  d=4   L2059  T=0 F=69  T=0 F=252  if (ret == NULL) {
  d=4   L2077  T=27 F=42  T=96 F=156  if (dict) {
  d=4   L2088  T=51 F=18  T=177 F=75  if (defaultValue != NULL) {
  d=4   L2089  T=21 F=30  T=69 F=108  if (dict)
  d=4   L2099  T=12 F=57  T=0 F=252  if (xmlHashAddEntry3(table, ret->name, ret->prefix, ret->...
  d=4   L2117  T=57 F=0  T=252 F=0  if (elemDef != NULL) {
  d=4   L2120  T=0 F=57  T=0 F=252  if ((type == XML_ATTRIBUTE_ID) &&
  d=4   L2134  T=0 F=57  T=6 F=246  if ((xmlStrEqual(ret->name, BAD_CAST "xmlns")) ||
  d=4   L2135  T=24 F=33  T=213 F=33  ((ret->prefix != NULL &&
  d=4   L2136  T=6 F=18  T=54 F=159  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns"))))) {
  d=4   L2142  T=30 F=21  T=168 F=30  while ((tmp != NULL) &&
  d=4   L2143  T=0 F=30  T=12 F=156  ((xmlStrEqual(tmp->name, BAD_CAST "xmlns")) ||
  d=4   L2144  T=18 F=12  T=132 F=24  ((ret->prefix != NULL &&
  d=4   L2145  T=0 F=18  T=0 F=132  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns")))))) {
  d=4   L2146  T=0 F=0  T=6 F=6  if (tmp->nexth == NULL)
  d=4   L2150  T=30 F=21  T=162 F=30  if (tmp != NULL) {
  d=4   L2164  T=0 F=57  T=0 F=252  if (dtd->last == NULL) {
--- d=3  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883) ---
  d=3   L3865  T=0 F=84  T=0 F=285  switch (type) {
  d=3   L3866  T=0 F=84  T=0 F=285  case XML_ATTRIBUTE_ENTITIES:
  d=3   L3867  T=0 F=84  T=0 F=285  case XML_ATTRIBUTE_IDREFS:
  d=3   L3869  T=0 F=84  T=0 F=285  case XML_ATTRIBUTE_ENTITY:
  d=3   L3870  T=0 F=84  T=0 F=285  case XML_ATTRIBUTE_IDREF:
  d=3   L3871  T=0 F=84  T=0 F=285  case XML_ATTRIBUTE_ID:
  d=3   L3872  T=0 F=84  T=0 F=285  case XML_ATTRIBUTE_NOTATION:
  d=3   L3874  T=0 F=84  T=0 F=285  case XML_ATTRIBUTE_NMTOKENS:
  d=3   L3875  T=45 F=39  T=135 F=150  case XML_ATTRIBUTE_ENUMERATION:
  d=3   L3877  T=0 F=84  T=0 F=285  case XML_ATTRIBUTE_NMTOKEN:
  d=3   L3879  T=39 F=45  T=150 F=135  case XML_ATTRIBUTE_CDATA:
--- d=1  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581) ---
  d=1   L3573  T=123 F=387  T=30 F=192  if ((IS_LETTER(c)) || (IS_DIGIT(c)) ||  <-- BLOCKER
  d=1   L3574  T=0 F=387  T=0 F=192  (c == '.') || (c == '-') ||
  d=1   L3574  T=21 F=366  T=12 F=180  (c == '.') || (c == '-') ||
  d=1   L3575  T=60 F=306  T=0 F=180  (c == '_') || (c == ':') ||

[off-chain: 435 additional divergent branches across 42 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d7c31b52479b9451, size=195 bytes, fuzzer=grimoire, trial=1, discovered_at=818s, mutation_op=GrimoireRecursiveReplacementMutator,GrimoireExtensionMutator):
  0000: 06 00 32 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   ..2l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 3c 61 3e 3c 62 20 78 6c 69 6e 6b 3a 66 3d 22 22   <a><b xlink:f=""
Seed 2 (id=f03624776c8784f9, size=198 bytes, fuzzer=grimoire, trial=1, discovered_at=5223s, mutation_op=CrossoverInsertMutator):
  0000: 06 00 32 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   ..2l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 3c 61 3e 3c 62 20 78 6c 69 6e 6b 3a 66 3d 22 22   <a><b xlink:f=""
Seed 3 (id=ca1522c2be5cd3dc, size=421 bytes, fuzzer=grimoire, trial=1, discovered_at=12880s, mutation_op=GrimoireRandomDeleteMutator,GrimoireRecursiveReplacementMutator):
  0000: 3c 21 5b 43 44 41 54 41 5b 00 07 c0 ff ff 06 00   <![CDATA[.......
  0010: 32 6c 5c 0a 3c 3f 6c 3f 3e 3c 21 44 4f 43 54 59   2l\.<?l?><!DOCTY
  0020: 50 45 61 20 53 59 53 54 45 4d 20 22 64 74 64 73   PEa SYSTEM "dtds
  0030: 2f 31 32 37 37 37 32 2e 64 74 64 22 3e 5c 0a 64   /127772.dtd">\.d
Seed 4 (id=2334ba5aca083669, size=160 bytes, fuzzer=grimoire, trial=1, discovered_at=20007s, mutation_op=BytesInsertMutator):
  0000: 06 00 e7 6c 5c 0a 3c 3f 6c 3f 3e 3c 21 44 4f 43   ...l\.<?l?><!DOC
  0010: 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64 74   TYPEa SYSTEM "dt
  0020: 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e 5c   ds/127772.dtd">\
  0030: 0a 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64   .dtds/127772.dtd
Seed 5 (id=43ab1e30bd2d4ce6, size=239 bytes, fuzzer=grimoire, trial=1, discovered_at=28291s, mutation_op=ByteDecMutator):
  0000: fe ff 0f 00 06 00 32 6c 5c 0a 3c 3f 6c 3f 3e 3c   ......2l\.<?l?><
  0010: 21 44 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d   !DOCTYPEa SYSTEM
  0020: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
  0030: 64 22 3e 5c 0a 64 74 64 73 2f 31 32 37 37 37 32   d">\.dtds/127772

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=a0f1e597ae5a2ec0, size=370 bytes, fuzzer=cmplog, trial=3, discovered_at=18s, mutation_op=BytesExpandMutator):
  0000: 06 00 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c   ......127772.xml
  0010: 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d   \.<?xml version=
  0020: 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50   "1.0"?>.<!DOCTYP
  0030: 45 20 61 20 53 59 53 54 45 4d 20 22 64 74 64 73   E a SYSTEM "dtds
Seed 2 (id=742fc2ee4437355e, size=364 bytes, fuzzer=cmplog, trial=2, discovered_at=1514s, mutation_op=CrossoverReplaceMutator,BytesInsertCopyMutator,CrossoverInsertMutator,BytesCopyMutator,QwordAddMutator):
  0000: 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   127772.xml\.<?xm
  0010: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0020: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
  0030: 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37   STEM "dtds/12777
Seed 3 (id=dbbd3fac0607b3bf, size=371 bytes, fuzzer=cmplog, trial=4, discovered_at=2201s, mutation_op=BytesDeleteMutator):
  0000: 37 37 32 2e 78 6d 00 5c 0a 3c 3f 78 6d 6c 20 76   772.xm.\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c   ersion="1.0"?>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE
  0030: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
Seed 4 (id=07327721331bad69, size=368 bytes, fuzzer=cmplog, trial=3, discovered_at=3011s, mutation_op=ByteDecMutator):
  0000: 06 00 ff 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 0a 76 65 72 73 69 6f 6e 3d 22 31   <?xml.version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=43214b30e31c6f69, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3468s, mutation_op=BytesCopyMutator):
  0000: 06 00 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c   ......127772.xml
  0010: 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d   \.<?xml version=
  0020: 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50   "1.0"?>.<!DOCTYP
  0030: 45 20 61 20 53 59 53 54 45 4d 20 22 64 74 64 73   E a SYSTEM "dtds


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  fe(.)x4 06(.)x3 3c(<)x1 f2(.)x1     06(.)x8 37(7)x6 31(1)x3 ff(.)x3 +9u  PARTIAL
   0x0001  ff(.)x4 00(.)x3 21(!)x1 f2(.)x1     00(.)x10 32(2)x5 37(7)x5 7f(.)x2 +6u  PARTIAL
   0x0003  6c(l)x4 00(.)x4 43(C)x1             00(.)x8 ff(.)x7 37(7)x6 2e(.)x2 +5u  PARTIAL
   0x0004  5c(\)x4 06(.)x4 44(D)x1             31(1)x6 37(7)x5 00(.)x4 30(0)x4 +7u  DIFFER
   0x0005  0a(.)x4 00(.)x4 41(A)x1             32(2)x14 00(.)x3 6d(m)x2 6c(l)x2 +7u  PARTIAL
   0x0006  3c(<)x4 32(2)x4 54(T)x1             37(7)x7 31(1)x4 2e(.)x4 c8(.)x2 +10u  PARTIAL
   0x0007  3f(?)x4 6c(l)x4 41(A)x1             37(7)x10 32(2)x4 78(x)x4 0a(.)x3 +6u  PARTIAL
   0x0008  6c(l)x4 5c(\)x4 5b([)x1             37(7)x14 6d(m)x4 0a(.)x3 3c(<)x2 +5u  PARTIAL
   0x0009  0a(.)x4 20( )x2 3f(?)x2 00(.)x1     32(2)x11 37(7)x4 6c(l)x4 0a(.)x3 +5u  PARTIAL
   0x000a  3c(<)x4 3f(?)x2 3e(>)x2 07(.)x1     2e(.)x11 37(7)x4 5c(\)x4 3f(?)x2 +5u  PARTIAL
   0x000b  3f(?)x4 3e(>)x2 3c(<)x2 c0(.)x1     78(x)x14 32(2)x4 0a(.)x4 6d(m)x2 +4u  PARTIAL
   0x000c  6c(l)x4 3c(<)x2 21(!)x2 ff(.)x1     6d(m)x14 3c(<)x4 2e(.)x3 6c(l)x2 +5u  PARTIAL
   0x000d  3f(?)x4 21(!)x2 44(D)x2 ff(.)x1     6c(l)x13 78(x)x5 3f(?)x4 20( )x2 +4u  PARTIAL
   0x000e  3e(>)x4 44(D)x2 4f(O)x2 06(.)x1     5c(\)x12 6d(m)x5 78(x)x4 20( )x2 +4u  DIFFER
   0x000f  3c(<)x4 4f(O)x2 43(C)x2 00(.)x1     0a(.)x12 6c(l)x5 6d(m)x4 76(v)x2 +4u  PARTIAL
   0x0010  21(!)x4 43(C)x2 54(T)x2 32(2)x1     3c(<)x12 5c(\)x4 6c(l)x4 65(e)x2 +5u  DIFFER
   0x0011  44(D)x4 54(T)x2 59(Y)x2 6c(l)x1     3f(?)x12 0a(.)x4 20( )x4 72(r)x2 +5u  PARTIAL
   0x0012  4f(O)x4 59(Y)x2 50(P)x2 5c(\)x1     78(x)x12 3c(<)x4 76(v)x4 73(s)x2 +5u  DIFFER
   0x0013  43(C)x4 50(P)x2 45(E)x2 0a(.)x1     6d(m)x12 3f(?)x4 65(e)x4 69(i)x2 +5u  DIFFER
   0x0014  54(T)x4 45(E)x2 61(a)x2 3c(<)x1     6c(l)x12 78(x)x4 72(r)x4 6f(o)x2 +5u  DIFFER
   0x0015  59(Y)x4 61(a)x2 20( )x2 3f(?)x1     20( )x11 6d(m)x4 73(s)x4 6e(n)x2 +6u  PARTIAL
   0x0016  50(P)x4 20( )x2 53(S)x2 6c(l)x1     76(v)x12 6c(l)x4 69(i)x4 3d(=)x2 +5u  PARTIAL
   0x0017  45(E)x4 53(S)x2 59(Y)x2 3f(?)x1     65(e)x12 20( )x4 6f(o)x4 22(")x2 +5u  DIFFER
   0x0018  61(a)x4 59(Y)x2 53(S)x2 3e(>)x1     72(r)x12 76(v)x4 6e(n)x4 31(1)x2 +5u  DIFFER
   0x0019  20( )x4 53(S)x2 54(T)x2 3c(<)x1     73(s)x12 65(e)x4 3d(=)x4 2e(.)x2 +5u  DIFFER
   0x001a  53(S)x4 54(T)x2 45(E)x2 21(!)x1     69(i)x12 22(")x6 72(r)x4 30(0)x2 +4u  DIFFER
   0x001b  59(Y)x4 45(E)x2 4d(M)x2 44(D)x1     6f(o)x12 73(s)x4 31(1)x4 22(")x3 +4u  DIFFER
   0x001c  53(S)x4 4d(M)x2 20( )x2 4f(O)x1     6e(n)x12 69(i)x4 2e(.)x4 3f(?)x2 +5u  DIFFER
   0x001d  54(T)x4 20( )x2 22(")x2 43(C)x1     3d(=)x12 6f(o)x4 30(0)x4 3e(>)x2 +5u  PARTIAL
   0x001e  45(E)x4 22(")x2 64(d)x2 54(T)x1     22(")x16 6e(n)x4 0a(.)x2 3c(<)x2 +3u  PARTIAL
   0x001f  4d(M)x4 64(d)x2 74(t)x2 59(Y)x1     31(1)x12 3d(=)x4 3f(?)x4 3c(<)x2 +5u  DIFFER
   0x0020  20( )x4 74(t)x2 64(d)x2 50(P)x1     2e(.)x12 22(")x4 3e(>)x4 21(!)x2 +5u  DIFFER
   0x0021  22(")x4 64(d)x2 73(s)x2 45(E)x1     30(0)x12 31(1)x4 0a(.)x4 44(D)x2 +5u  DIFFER
   0x0022  64(d)x4 73(s)x2 2f(/)x2 61(a)x1     22(")x12 2e(.)x4 3c(<)x4 4f(O)x2 +5u  DIFFER
   0x0023  74(t)x4 2f(/)x2 31(1)x2 20( )x1     3f(?)x12 30(0)x4 21(!)x4 43(C)x2 +5u  DIFFER
   0x0024  64(d)x4 31(1)x2 32(2)x2 53(S)x1     3e(>)x12 22(")x4 44(D)x4 54(T)x2 +5u  DIFFER
   0x0025  73(s)x4 32(2)x2 37(7)x2 59(Y)x1     0a(.)x12 3f(?)x4 4f(O)x4 59(Y)x2 +5u  PARTIAL
   0x0026  37(7)x4 2f(/)x4 53(S)x1             3c(<)x12 3e(>)x4 43(C)x4 50(P)x2 +5u  DIFFER
   0x0027  37(7)x4 31(1)x4 54(T)x1             21(!)x12 0a(.)x4 54(T)x4 45(E)x2 +5u  PARTIAL
   0x0028  32(2)x6 37(7)x2 45(E)x1             44(D)x12 3c(<)x4 59(Y)x4 20( )x2 +5u  PARTIAL
   ... (23 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7138.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7138,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [grimoire>cmplog (grimoire_structural), value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7138 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7138 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7138 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).