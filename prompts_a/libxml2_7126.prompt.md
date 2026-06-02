==== BLOCKER ====
Target: libxml2
Branch ID: 7126
Location: /src/libxml2/valid.c:3556:20
Enclosing function: valid.c:xmlIsDocNameChar
Source line: 	    (c == '-') || (c == '.') || (c == 0xB7) || /* !start */
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (calibrated_energy vs minimizer)
cmplog                           7        3          0  REFERENCE
value_profile                    5        5          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                        4        5          1  REFERENCE
naive_ngram4                     2        6          2  REFERENCE
mopt                             0        9          1  REFERENCE
minimizer                        8        2          0  winner (calibrated_energy vs naive)
fast                             4        5          1  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['minimizer', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: minimizer > naive  [delta: calibrated_energy] ---
  subject 38  (minimizer vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=8.40h  loser=19.20h
  avg hitcount on branch: winner=84  loser=8
  prob_div=0.60  dur_div=10.80h  hit_div=75
  subject-level: delta_AUC=20906460.0  p_AUC=0.1041  delta_Final=371.4  p_final=0.0046

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7126/{W,L}/branch_coverage_show.txt

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
[B]  3555  	    (c == '_') || (c == ':') ||
[B]  3556  	    (c == '-') || (c == '.') || (c == 0xB7) || /* !start */ <-- BLOCKER
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
    2029       475  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)  <-- enclosing
       0        38  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
       0        24  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
       0        12  xmlValidateAttributeDecl  (/src/libxml2/valid.c:4197-4288)
       0        12  xmlValidateElementDecl  (/src/libxml2/valid.c:4308-4401)
       0        10  xmlIsID  (/src/libxml2/valid.c:2767-2816)
       0        10  xmlIsRef  (/src/libxml2/valid.c:3115-3143)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172) ---
  d=4   L1970  T=0 F=45  T=0 F=103  if (dtd == NULL) {
  d=4   L1974  T=0 F=45  T=0 F=103  if (name == NULL) {
  d=4   L1978  T=0 F=45  T=0 F=103  if (elem == NULL) {
  d=4   L1982  T=45 F=0  T=103 F=0  if (dtd->doc != NULL)
  d=4   L1990  T=27 F=18  T=59 F=44  case XML_ATTRIBUTE_CDATA:
  d=4   L1992  T=0 F=45  T=0 F=103  case XML_ATTRIBUTE_ID:
  d=4   L1994  T=0 F=45  T=0 F=103  case XML_ATTRIBUTE_IDREF:
  d=4   L1996  T=0 F=45  T=0 F=103  case XML_ATTRIBUTE_IDREFS:
  d=4   L1998  T=0 F=45  T=0 F=103  case XML_ATTRIBUTE_ENTITY:
  d=4   L2000  T=0 F=45  T=0 F=103  case XML_ATTRIBUTE_ENTITIES:
  d=4   L2002  T=0 F=45  T=0 F=103  case XML_ATTRIBUTE_NMTOKEN:
  d=4   L2004  T=0 F=45  T=0 F=103  case XML_ATTRIBUTE_NMTOKENS:
  d=4   L2006  T=18 F=27  T=44 F=59  case XML_ATTRIBUTE_ENUMERATION:
  d=4   L2008  T=0 F=45  T=0 F=103  case XML_ATTRIBUTE_NOTATION:
  d=4   L2010  T=0 F=45  T=0 F=103  default:
  d=4   L2017  T=36 F=9  T=88 F=15  if ((defaultValue != NULL) &&
  d=4   L2018  T=3 F=33  T=3 F=85  (!xmlValidateAttributeValueInternal(dtd->doc, type, defau...
  d=4   L2032  T=45 F=0  T=103 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=4   L2032  T=45 F=0  T=103 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=4   L2033  T=45 F=0  T=103 F=0  (dtd->doc->intSubset != NULL) &&
  d=4   L2034  T=0 F=45  T=0 F=103  (dtd->doc->intSubset->attributes != NULL)) {
  d=4   L2046  T=18 F=27  T=44 F=59  if (table == NULL) {
  d=4   L2050  T=0 F=45  T=0 F=103  if (table == NULL) {
  d=4   L2059  T=0 F=45  T=0 F=103  if (ret == NULL) {
  d=4   L2077  T=45 F=0  T=103 F=0  if (dict) {
  d=4   L2088  T=33 F=12  T=85 F=18  if (defaultValue != NULL) {
  d=4   L2089  T=33 F=0  T=85 F=0  if (dict)
  d=4   L2099  T=0 F=45  T=0 F=103  if (xmlHashAddEntry3(table, ret->name, ret->prefix, ret->...
  d=4   L2117  T=45 F=0  T=103 F=0  if (elemDef != NULL) {
  d=4   L2120  T=0 F=45  T=0 F=103  if ((type == XML_ATTRIBUTE_ID) &&
  d=4   L2134  T=0 F=45  T=0 F=103  if ((xmlStrEqual(ret->name, BAD_CAST "xmlns")) ||
  d=4   L2135  T=42 F=3  T=97 F=6  ((ret->prefix != NULL &&
  d=4   L2136  T=6 F=36  T=41 F=56  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns"))))) {
  d=4   L2143  T=0 F=27  T=0 F=59  ((xmlStrEqual(tmp->name, BAD_CAST "xmlns")) ||
  d=4   L2144  T=24 F=3  T=53 F=6  ((ret->prefix != NULL &&
  d=4   L2145  T=0 F=24  T=0 F=53  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns")))))) {
  d=4   L2164  T=0 F=45  T=0 F=103  if (dtd->last == NULL) {
--- d=3  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883) ---
  d=3   L3865  T=0 F=36  T=0 F=100  switch (type) {
  d=3   L3866  T=0 F=36  T=0 F=100  case XML_ATTRIBUTE_ENTITIES:
  d=3   L3867  T=0 F=36  T=0 F=100  case XML_ATTRIBUTE_IDREFS:
  d=3   L3869  T=0 F=36  T=0 F=100  case XML_ATTRIBUTE_ENTITY:
  d=3   L3870  T=0 F=36  T=0 F=100  case XML_ATTRIBUTE_IDREF:
  d=3   L3871  T=0 F=36  T=0 F=100  case XML_ATTRIBUTE_ID:
  d=3   L3872  T=0 F=36  T=0 F=100  case XML_ATTRIBUTE_NOTATION:
  d=3   L3874  T=0 F=36  T=0 F=100  case XML_ATTRIBUTE_NMTOKENS:
  d=3   L3875  T=18 F=18  T=50 F=50  case XML_ATTRIBUTE_ENUMERATION:
  d=3   L3877  T=0 F=36  T=0 F=100  case XML_ATTRIBUTE_NMTOKEN:
  d=3   L3879  T=18 F=18  T=50 F=50  case XML_ATTRIBUTE_CDATA:
--- d=1  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581) ---
  d=1   L3547  T=2029 F=0  T=475 F=0  if ((doc == NULL) || (doc->properties & XML_DOC_OLD10) ==...
  d=1   L3547  T=0 F=2029  T=0 F=475  if ((doc == NULL) || (doc->properties & XML_DOC_OLD10) ==...
  d=1   L3552  T=120 F=1910  T=389 F=86  if (((c >= 'a') && (c <= 'z')) ||
  d=1   L3552  T=120 F=0  T=389 F=0  if (((c >= 'a') && (c <= 'z')) ||
  d=1   L3553  T=711 F=1200  T=15 F=71  ((c >= 'A') && (c <= 'Z')) ||
  d=1   L3553  T=183 F=528  T=15 F=0  ((c >= 'A') && (c <= 'Z')) ||
  d=1   L3554  T=780 F=948  T=6 F=65  ((c >= '0') && (c <= '9')) || /* !start */
  d=1   L3554  T=252 F=528  T=0 F=6  ((c >= '0') && (c <= '9')) || /* !start */
  d=1   L3555  T=525 F=951  T=0 F=71  (c == '_') || (c == ':') ||
  d=1   L3555  T=0 F=951  T=6 F=65  (c == '_') || (c == ':') ||
  d=1   L3556  T=84 F=867  T=0 F=65  (c == '-') || (c == '.') || (c == 0xB7) || /* !start */  <-- BLOCKER
  d=1   L3556  T=837 F=30  T=0 F=65  (c == '-') || (c == '.') || (c == 0xB7) || /* !start */  <-- BLOCKER
  d=1   L3556  T=0 F=30  T=0 F=65  (c == '-') || (c == '.') || (c == 0xB7) || /* !start */  <-- BLOCKER
  d=1   L3557  T=0 F=30  T=0 F=65  ((c >= 0xC0) && (c <= 0xD6)) ||
  d=1   L3558  T=0 F=30  T=0 F=65  ((c >= 0xD8) && (c <= 0xF6)) ||
  d=1   L3559  T=0 F=30  T=0 F=65  ((c >= 0xF8) && (c <= 0x2FF)) ||
  d=1   L3560  T=0 F=30  T=0 F=65  ((c >= 0x300) && (c <= 0x36F)) || /* !start */
  d=1   L3561  T=0 F=30  T=0 F=65  ((c >= 0x370) && (c <= 0x37D)) ||
  d=1   L3562  T=0 F=30  T=0 F=65  ((c >= 0x37F) && (c <= 0x1FFF)) ||
  d=1   L3563  T=0 F=30  T=0 F=65  ((c >= 0x200C) && (c <= 0x200D)) ||
  d=1   L3564  T=0 F=30  T=0 F=65  ((c >= 0x203F) && (c <= 0x2040)) || /* !start */
  d=1   L3565  T=0 F=30  T=0 F=65  ((c >= 0x2070) && (c <= 0x218F)) ||
  d=1   L3566  T=0 F=30  T=0 F=65  ((c >= 0x2C00) && (c <= 0x2FEF)) ||
  d=1   L3567  T=0 F=30  T=0 F=65  ((c >= 0x3001) && (c <= 0xD7FF)) ||
  d=1   L3568  T=0 F=30  T=0 F=65  ((c >= 0xF900) && (c <= 0xFDCF)) ||
  d=1   L3569  T=0 F=30  T=0 F=65  ((c >= 0xFDF0) && (c <= 0xFFFD)) ||
  d=1   L3570  T=0 F=30  T=0 F=65  ((c >= 0x10000) && (c <= 0xEFFFF)))

[off-chain: 148 additional divergent branches across 16 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=60af511b92259f7e, size=384 bytes, fuzzer=minimizer, trial=1, discovered_at=606s, mutation_op=WordAddMutator,BytesRandInsertMutator,TokenReplace):
  0000: 06 00 00 00 31 32 cb cc cc cc cc cc cc 0c 5c 0a   ....12........\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=43fc180097d4c285, size=388 bytes, fuzzer=minimizer, trial=1, discovered_at=2055s, mutation_op=BitFlipMutator,BytesInsertMutator):
  0000: 06 00 00 00 31 32 cb cc cc cc cc cc cc 0c 5c 0a   ....12........\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=abc3c4a104c60a94, size=384 bytes, fuzzer=minimizer, trial=1, discovered_at=2055s, mutation_op=BytesRandSetMutator):
  0000: 06 00 00 00 31 32 cb cc cc cc cc cc cc 0c 5c 0a   ....12........\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=9073db3d5ded154f, size=588 bytes, fuzzer=minimizer, trial=1, discovered_at=63828s, mutation_op=BytesSetMutator):
  0000: 6c 6c 6c 6c 6c 6c 6c 6c 6c 32 32 32 32 0c 5c 0a   lllllllll2222.\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=cccd6ec6fb70f9b1, size=601 bytes, fuzzer=minimizer, trial=1, discovered_at=64019s, mutation_op=BytesSetMutator,CrossoverReplaceMutator,TokenReplace):
  0000: 06 00 04 32 32 32 32 32 32 32 32 32 32 0c 5c 0a   ...2222222222.\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=8c7bd7ba6dfb824c, size=368 bytes, fuzzer=naive, trial=1):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=03d78b3095fb6a26, size=388 bytes, fuzzer=naive, trial=4, discovered_at=0s, mutation_op=BitFlipMutator,BytesInsertMutator,CrossoverReplaceMutator,ByteRandMutator,ByteFlipMutator,BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=10742186bee0dd9b, size=368 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=BytesCopyMutator,BitFlipMutator,QwordAddMutator):
  0000: 06 00 00 00 31 06 00 00 00 31 32 37 37 37 32 2e   ....1....127772.
  0010: 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69   xml\.<?xml versi
  0020: 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43   on="1.0"?>.<!DOC
  0030: 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22 64   TYPE a SYSTEM "d
Seed 4 (id=151e7a5b22369cfc, size=368 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=DwordInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=4a0619124602addc, size=381 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=BytesInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x5 6c(l)x1                     06(.)x12 7f(.)x1 3e(>)x1 27(')x1    PARTIAL
   0x0001  00(.)x5 6c(l)x1                     00(.)x13 41(A)x1 68(h)x1            PARTIAL
   0x0002  00(.)x3 04(.)x2 6c(l)x1             00(.)x13 41(A)x1 74(t)x1            PARTIAL
   0x0003  00(.)x3 32(2)x2 6c(l)x1             00(.)x13 41(A)x1 74(t)x1            PARTIAL
   0x0004  31(1)x3 32(2)x2 6c(l)x1             31(1)x12 3e(>)x1 41(A)x1 70(p)x1    PARTIAL
   0x0005  32(2)x5 6c(l)x1                     32(2)x11 06(.)x1 62(b)x1 41(A)x1 +1u  PARTIAL
   0x0006  cb(.)x3 32(2)x2 6c(l)x1             37(7)x11 00(.)x1 20( )x1 41(A)x1 +1u  DIFFER
   0x0007  cc(.)x3 32(2)x2 6c(l)x1             37(7)x11 00(.)x1 74(t)x1 20( )x1 +1u  DIFFER
   0x0008  cc(.)x3 32(2)x2 6c(l)x1             37(7)x11 00(.)x1 65(e)x1 20( )x1 +1u  DIFFER
   0x0009  cc(.)x3 32(2)x3                     32(2)x11 31(1)x1 78(x)x1 20( )x1 +1u  PARTIAL
   0x000a  cc(.)x3 32(2)x3                     2e(.)x11 32(2)x1 6d(m)x1 40(@)x1 +1u  PARTIAL
   0x000b  cc(.)x3 32(2)x3                     78(x)x11 37(7)x1 6c(l)x1 20( )x1 +1u  DIFFER
   0x000c  cc(.)x3 32(2)x3                     6d(m)x11 37(7)x1 5c(\)x1 20( )x1 +1u  DIFFER
   0x000d  0c(.)x6                             6c(l)x11 37(7)x1 0a(.)x1 55(U)x1 +1u  DIFFER
   0x000e  5c(\)x6                             5c(\)x11 32(2)x1 3c(<)x1 54(T)x1 +1u  PARTIAL
   0x000f  0a(.)x6                             0a(.)x11 2e(.)x1 3f(?)x1 46(F)x1 +1u  PARTIAL
   0x0010  3c(<)x6                             3c(<)x11 78(x)x2 2d(-)x1 20( )x1    PARTIAL
   0x0011  3f(?)x6                             3f(?)x11 6d(m)x2 38(8)x1 20( )x1    PARTIAL
   0x0012  78(x)x6                             78(x)x11 6c(l)x2 00(.)x1 20( )x1    PARTIAL
   0x0013  6d(m)x6                             6d(m)x11 20( )x3 5c(\)x1            PARTIAL
   0x0014  6c(l)x6                             6c(l)x11 0a(.)x1 76(v)x1 20( )x1 +1u  PARTIAL
   0x0015  20( )x6                             20( )x12 3c(<)x1 65(e)x1 38(8)x1    PARTIAL
   0x0016  76(v)x6                             76(v)x11 3f(?)x1 72(r)x1 20( )x1 +1u  PARTIAL
   0x0017  65(e)x6                             65(e)x11 78(x)x1 73(s)x1 20( )x1 +1u  PARTIAL
   0x0018  72(r)x6                             72(r)x11 6d(m)x1 69(i)x1 3a(:)x1 +1u  PARTIAL
   0x0019  73(s)x6                             73(s)x11 6c(l)x1 6f(o)x1 2f(/)x1 +1u  PARTIAL
   0x001a  69(i)x6                             69(i)x11 20( )x1 6e(n)x1 2f(/)x1 +1u  PARTIAL
   0x001b  6f(o)x6                             6f(o)x11 76(v)x1 3d(=)x1 66(f)x1 +1u  PARTIAL
   0x001c  6e(n)x6                             6e(n)x11 65(e)x1 22(")x1 78(x)x1 +1u  PARTIAL
   0x001d  3d(=)x6                             3d(=)x11 72(r)x1 31(1)x1 3e(>)x1 +1u  PARTIAL
   0x001e  22(")x6                             22(")x11 73(s)x1 2e(.)x1 0a(.)x1 +1u  PARTIAL
   0x001f  31(1)x6                             31(1)x11 69(i)x1 30(0)x1 20( )x1 +1u  PARTIAL
   0x0020  2e(.)x6                             2e(.)x11 6f(o)x1 22(")x1 20( )x1 +1u  PARTIAL
   0x0021  30(0)x6                             30(0)x11 6e(n)x1 3f(?)x1 3c(<)x1 +1u  PARTIAL
   0x0022  22(")x6                             22(")x11 3d(=)x1 3e(>)x1 62(b)x1 +1u  PARTIAL
   0x0023  3f(?)x6                             3f(?)x11 22(")x1 0a(.)x1 20( )x1 +1u  PARTIAL
   0x0024  3e(>)x6                             3e(>)x11 31(1)x1 3c(<)x1 78(x)x1 +1u  PARTIAL
   0x0025  0a(.)x6                             0a(.)x11 2e(.)x1 21(!)x1 6c(l)x1 +1u  PARTIAL
   0x0026  3c(<)x6                             3c(<)x11 30(0)x1 44(D)x1 69(i)x1 +1u  PARTIAL
   0x0027  21(!)x6                             21(!)x11 22(")x1 4f(O)x1 6e(n)x1 +1u  PARTIAL
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- minimizer ---
**Instrumentation**: naive's edge counters only.

**Feedback**: naive's edge-bucket `MaxMapFeedback`, plus a
`CalibrationStage` that measures each new corpus entry's execution
time, edge-map fill, and stability into `SchedulerMetadata`/testcase
metadata.

**Mutators / stages**: havoc + token mutator (`LineageMutator`, names
captured) run inside a `StdPowerMutationalStage` rather than naive's
plain `StdMutationalStage`. Stages are `[calibration, power]`. The
power stage derives the number of havoc mutations per seed visit (the
"energy") from a calibration-based `perf_score` — faster, smaller,
more-stable seeds earn more mutations. PowerSchedule is `None`, so the
energy uses ONLY intrinsic calibration and is NOT weighted by how often
a region has been hit. Corpus selection is plain FIFO `QueueScheduler`
(same order as naive).

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge, plus a one-time
calibration burst per new corpus entry.

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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_7126.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7126,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [minimizer>naive (calibrated_energy)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7126 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7126 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7126 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).