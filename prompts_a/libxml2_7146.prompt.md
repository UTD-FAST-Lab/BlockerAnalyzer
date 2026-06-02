==== BLOCKER ====
Target: libxml2
Branch ID: 7146
Location: /src/libxml2/valid.c:3807:9
Enclosing function: valid.c:xmlValidateNmtokensValueInternal
Source line:     if (val != 0) return(0);
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            8        2          0  REFERENCE
cmplog                           7        3          0  REFERENCE
value_profile                    9        0          1  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        8        1          1  REFERENCE
naive_ngram4                     2        7          1  REFERENCE
mopt                             4        5          1  REFERENCE
minimizer                        9        1          0  winner (aflfast_rarity vs fast)
fast                             1        8          1  loser (aflfast_rarity vs minimizer)
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['fast', 'minimizer']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: minimizer > fast  [delta: aflfast_rarity] ---
  subject 39  (fast vs minimizer, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=8  unreached=1
  avg duration blocked: winner=6.30h  loser=19.00h
  avg hitcount on branch: winner=12  loser=0
  prob_div=0.79  dur_div=12.70h  hit_div=12
  subject-level: delta_AUC=-20200320.0  p_AUC=0.0376  delta_Final=-295.1  p_final=0.0452

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7146/{W,L}/branch_coverage_show.txt

--- Enclosing function: valid.c:xmlValidateNmtokensValueInternal (/src/libxml2/valid.c:3765-3810) ---
[ ]  3763  
[ ]  3764  static int
[B]  3765  xmlValidateNmtokensValueInternal(xmlDocPtr doc, const xmlChar *value) {
[B]  3766      const xmlChar *cur;
[B]  3767      int val, len;
[ ]  3768  
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
[B]  3779      if (!xmlIsDocNameChar(doc, val))
[ ]  3780  	return(0);
[ ]  3781  
[B]  3782      while (xmlIsDocNameChar(doc, val)) {
[B]  3783  	val = xmlStringCurrentChar(NULL, cur, &len);
[B]  3784  	cur += len;
[B]  3785      }
[ ]  3786  
[ ]  3787      /* Should not test IS_BLANK(val) here -- see erratum E20*/
[B]  3788      while (val == 0x20) {
[ ]  3789  	while (val == 0x20) {
[ ]  3790  	    val = xmlStringCurrentChar(NULL, cur, &len);
[ ]  3791  	    cur += len;
[ ]  3792  	}
[ ]  3793  	if (val == 0) return(1);
[ ]  3794  
[ ]  3795  	if (!xmlIsDocNameChar(doc, val))
[ ]  3796  	    return(0);
[ ]  3797  
[ ]  3798  	val = xmlStringCurrentChar(NULL, cur, &len);
[ ]  3799  	cur += len;
[ ]  3800  
[ ]  3801  	while (xmlIsDocNameChar(doc, val)) {
[ ]  3802  	    val = xmlStringCurrentChar(NULL, cur, &len);
[ ]  3803  	    cur += len;
[ ]  3804  	}
[ ]  3805      }
[ ]  3806  
[B]  3807      if (val != 0) return(0); <-- BLOCKER
[ ]  3808  
[L]  3809      return(1);
[B]  3810  }

--- Caller (1 hop): valid.c:xmlValidateAttributeValueInternal (/src/libxml2/valid.c:3864-3883, calls valid.c:xmlValidateNmtokensValueInternal at line 3876) (full body — short) ---
[B]  3864                                    const xmlChar *value) {
[B]  3865      switch (type) {
[ ]  3866  	case XML_ATTRIBUTE_ENTITIES:
[ ]  3867  	case XML_ATTRIBUTE_IDREFS:
[ ]  3868  	    return(xmlValidateNamesValueInternal(doc, value));
[ ]  3869  	case XML_ATTRIBUTE_ENTITY:
[ ]  3870  	case XML_ATTRIBUTE_IDREF:
[ ]  3871  	case XML_ATTRIBUTE_ID:
[ ]  3872  	case XML_ATTRIBUTE_NOTATION:
[ ]  3873  	    return(xmlValidateNameValueInternal(doc, value));
[ ]  3874  	case XML_ATTRIBUTE_NMTOKENS:
[B]  3875  	case XML_ATTRIBUTE_ENUMERATION:
[B]  3876  	    return(xmlValidateNmtokensValueInternal(doc, value)); <-- CALL
[ ]  3877  	case XML_ATTRIBUTE_NMTOKEN:
[ ]  3878  	    return(xmlValidateNmtokenValueInternal(doc, value));
[B]  3879          case XML_ATTRIBUTE_CDATA:
[B]  3880  	    break;
[B]  3881      }
[B]  3882      return(1);
[B]  3883  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883, calls valid.c:xmlValidateNmtokensValueInternal at line 3876)
hop 2  xmlValidateNmtokensValue  (/src/libxml2/valid.c:3824-3826, calls valid.c:xmlValidateNmtokensValueInternal at line 3825)
hop 3  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172, calls valid.c:xmlValidateAttributeValueInternal at line 2018)
hop 3  xmlValidateAttributeValue  (/src/libxml2/valid.c:3910-3912, calls valid.c:xmlValidateAttributeValueInternal at line 3911)
hop 4  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758, calls xmlAddAttributeDecl at line 731)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      60       414  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
       6       168  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
      24       162  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883)
       0       124  xmlGetDtdQElementDesc  (/src/libxml2/valid.c:3349-3357)
       0        97  xmlGetDtdQAttrDesc  (/src/libxml2/valid.c:3410-3418)
      30       126  valid.c:xmlFreeAttribute  (/src/libxml2/valid.c:1907-1939)
      30       126  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172)
      30       117  valid.c:xmlFreeAttributeTableEntry  (/src/libxml2/valid.c:2175-2177)
      30       117  valid.c:xmlGetDtdElementDesc2  (/src/libxml2/valid.c:3280-3334)
      12        90  valid.c:xmlValidateNmtokensValueInternal  (/src/libxml2/valid.c:3765-3810)  <-- enclosing
      27        90  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)
      27        90  valid.c:xmlFreeElement  (/src/libxml2/valid.c:1382-1395)
      27        90  valid.c:xmlFreeElementTableEntry  (/src/libxml2/valid.c:1623-1625)
       0        61  xmlValidCtxtNormalizeAttributeValue  (/src/libxml2/valid.c:4061-4111)
      24        84  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
... (32 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172) ---
  d=3   L1970  T=0 F=30  T=0 F=126  if (dtd == NULL) {
  d=3   L1974  T=0 F=30  T=0 F=126  if (name == NULL) {
  d=3   L1978  T=0 F=30  T=0 F=126  if (elem == NULL) {
  d=3   L1982  T=30 F=0  T=126 F=0  if (dtd->doc != NULL)
  d=3   L1990  T=18 F=12  T=63 F=63  case XML_ATTRIBUTE_CDATA:
  d=3   L1992  T=0 F=30  T=0 F=126  case XML_ATTRIBUTE_ID:
  d=3   L1994  T=0 F=30  T=0 F=126  case XML_ATTRIBUTE_IDREF:
  d=3   L1996  T=0 F=30  T=0 F=126  case XML_ATTRIBUTE_IDREFS:
  d=3   L1998  T=0 F=30  T=0 F=126  case XML_ATTRIBUTE_ENTITY:
  d=3   L2000  T=0 F=30  T=0 F=126  case XML_ATTRIBUTE_ENTITIES:
  d=3   L2002  T=0 F=30  T=0 F=126  case XML_ATTRIBUTE_NMTOKEN:
  d=3   L2004  T=0 F=30  T=0 F=126  case XML_ATTRIBUTE_NMTOKENS:
  d=3   L2006  T=12 F=18  T=63 F=63  case XML_ATTRIBUTE_ENUMERATION:
  d=3   L2008  T=0 F=30  T=0 F=126  case XML_ATTRIBUTE_NOTATION:
  d=3   L2010  T=0 F=30  T=0 F=126  default:
  d=3   L2017  T=24 F=6  T=108 F=18  if ((defaultValue != NULL) &&
  d=3   L2018  T=12 F=12  T=0 F=108  (!xmlValidateAttributeValueInternal(dtd->doc, type, defau...
  d=3   L2023  T=12 F=0  T=0 F=0  if (ctxt != NULL)
  d=3   L2032  T=30 F=0  T=126 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=3   L2032  T=30 F=0  T=126 F=0  if ((dtd->doc != NULL) && (dtd->doc->extSubset == dtd) &&
  d=3   L2033  T=30 F=0  T=126 F=0  (dtd->doc->intSubset != NULL) &&
  d=3   L2034  T=0 F=30  T=0 F=126  (dtd->doc->intSubset->attributes != NULL)) {
  d=3   L2046  T=12 F=18  T=42 F=84  if (table == NULL) {
  d=3   L2050  T=0 F=30  T=0 F=126  if (table == NULL) {
  d=3   L2059  T=0 F=30  T=0 F=126  if (ret == NULL) {
  d=3   L2077  T=21 F=9  T=87 F=39  if (dict) {
  d=3   L2088  T=12 F=18  T=108 F=18  if (defaultValue != NULL) {
  d=3   L2089  T=9 F=3  T=81 F=27  if (dict)
  d=3   L2099  T=0 F=30  T=9 F=117  if (xmlHashAddEntry3(table, ret->name, ret->prefix, ret->...
  d=3   L2117  T=30 F=0  T=117 F=0  if (elemDef != NULL) {
  d=3   L2120  T=0 F=30  T=0 F=117  if ((type == XML_ATTRIBUTE_ID) &&
  d=3   L2134  T=0 F=30  T=0 F=117  if ((xmlStrEqual(ret->name, BAD_CAST "xmlns")) ||
  d=3   L2135  T=30 F=0  T=102 F=15  ((ret->prefix != NULL &&
  d=3   L2136  T=6 F=24  T=18 F=84  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns"))))) {
  d=3   L2142  T=18 F=6  T=75 F=24  while ((tmp != NULL) &&
  d=3   L2143  T=0 F=18  T=0 F=75  ((xmlStrEqual(tmp->name, BAD_CAST "xmlns")) ||
  d=3   L2144  T=18 F=0  T=66 F=9  ((ret->prefix != NULL &&
  d=3   L2145  T=0 F=18  T=0 F=66  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns")))))) {
  d=3   L2150  T=18 F=6  T=75 F=24  if (tmp != NULL) {
  d=3   L2164  T=0 F=30  T=0 F=117  if (dtd->last == NULL) {
--- d=2  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883) ---
  d=2   L3865  T=0 F=24  T=0 F=162  switch (type) {
  d=2   L3866  T=0 F=24  T=0 F=162  case XML_ATTRIBUTE_ENTITIES:
  d=2   L3867  T=0 F=24  T=0 F=162  case XML_ATTRIBUTE_IDREFS:
  d=2   L3869  T=0 F=24  T=0 F=162  case XML_ATTRIBUTE_ENTITY:
  d=2   L3870  T=0 F=24  T=0 F=162  case XML_ATTRIBUTE_IDREF:
  d=2   L3871  T=0 F=24  T=0 F=162  case XML_ATTRIBUTE_ID:
  d=2   L3872  T=0 F=24  T=0 F=162  case XML_ATTRIBUTE_NOTATION:
  d=2   L3874  T=0 F=24  T=0 F=162  case XML_ATTRIBUTE_NMTOKENS:
  d=2   L3875  T=12 F=12  T=90 F=72  case XML_ATTRIBUTE_ENUMERATION:
  d=2   L3877  T=0 F=24  T=0 F=162  case XML_ATTRIBUTE_NMTOKEN:
  d=2   L3879  T=12 F=12  T=72 F=90  case XML_ATTRIBUTE_CDATA:
--- d=1  valid.c:xmlValidateNmtokensValueInternal  (/src/libxml2/valid.c:3765-3810) ---
  d=1   L3769  T=0 F=12  T=0 F=90  if (value == NULL) return(0);
  d=1   L3779  T=0 F=12  T=0 F=90  if (!xmlIsDocNameChar(doc, val))
  d=1   L3788  T=0 F=12  T=0 F=90  while (val == 0x20) {
  d=1   L3807  T=12 F=0  T=0 F=90  if (val != 0) return(0);  <-- BLOCKER

[off-chain: 435 additional divergent branches across 41 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=e5641bf030cc5383, size=384 bytes, fuzzer=minimizer, trial=1, discovered_at=389s, mutation_op=TokenReplace,BitFlipMutator,BytesInsertCopyMutator,WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=61ac017e4411cdee, size=400 bytes, fuzzer=minimizer, trial=1, discovered_at=3064s, mutation_op=BytesRandInsertMutator,ByteIncMutator):
  0000: 06 1a 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=deb9939fdc0f8f1b, size=736 bytes, fuzzer=minimizer, trial=1, discovered_at=3599s, mutation_op=BytesRandSetMutator,BytesRandInsertMutator):
  0000: a9 05 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   ..7772.xml\.<?xm
  0010: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0020: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
  0030: 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37   STEM "dtds/12777
Seed 4 (id=15a660576a8a241a, size=608 bytes, fuzzer=minimizer, trial=1, discovered_at=75272s, mutation_op=ByteIncMutator):
  0000: 06 00 04 32 32 32 32 32 32 32 32 32 32 0c 5c 0a   ...2222222222.\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=05bf61c6459b9374, size=702 bytes, fuzzer=fast, trial=1):
  0000: a7 a7 a7 a7 a7 a7 aa aa aa aa aa aa aa 8c aa 32   ...............2
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
Seed 2 (id=06c00740dadbf046, size=710 bytes, fuzzer=fast, trial=1):
  0000: a7 a7 a7 a7 a7 a7 aa aa aa aa aa aa aa 8c aa 32   ...............2
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
Seed 3 (id=094fee4ea64e7473, size=785 bytes, fuzzer=fast, trial=1):
  0000: 9b 00 00 f0 ff 9b 9b 00 31 32 37 37 37 32 2e 78   ........127772.x
  0010: 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f   ml\.<?xml versio
  0020: 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54   n="1.0"?>.<!DOCT
  0030: 59 50 45 20 61 20 53 59 53 54 45 4d 20 22 64 74   YPE a SYSTEM "dt
Seed 4 (id=0d5b13e14851332f, size=570 bytes, fuzzer=fast, trial=1):
  0000: 27 40 27 27 24 61 28 9d 27 27 27 ff ff ff 65 65   '@''$a(.'''...ee
  0010: 65 65 3a 2f 6e 65 65 65 6d 60 22 3e 62 20 74 06   ee:/neeem`">b t.
  0020: ff 00 00 31 32 37 5c 0a 3c 3f 6d 6c 20 76 65 72   ...127\.<?ml ver
  0030: 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44   sion="1.0"?>.<!D
Seed 5 (id=101db96d1b56bcd2, size=581 bytes, fuzzer=fast, trial=1):
  0000: ff ff ff 65 65 65 65 3a 2f 6e 65 65 65 6d 60 22   ...eeee:/neeem`"
  0010: 3e 62 20 74 06 ff 00 00 31 32 37 5c 0a 3c 3f 6d   >b t....127\.<?m
  0020: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0030: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x3 a9(.)x1                     ff(.)x5 a7(.)x2 9b(.)x1 27(')x1 +5u  DIFFER
   0x0001  00(.)x2 1a(.)x1 05(.)x1             ff(.)x4 a7(.)x2 00(.)x1 40(@)x1 +6u  PARTIAL
   0x0002  00(.)x2 37(7)x1 04(.)x1             ff(.)x5 a7(.)x3 00(.)x1 27(')x1 +4u  PARTIAL
   0x0003  00(.)x2 37(7)x1 32(2)x1             65(e)x6 a7(.)x3 f0(.)x1 27(')x1 +3u  DIFFER
   0x0004  31(1)x2 37(7)x1 32(2)x1             65(e)x6 a7(.)x3 ff(.)x1 24($)x1 +3u  DIFFER
   0x0005  32(2)x4                             65(e)x5 a7(.)x3 9b(.)x1 61(a)x1 +4u  DIFFER
   0x0006  37(7)x2 2e(.)x1 32(2)x1             65(e)x5 aa(.)x3 9b(.)x1 28(()x1 +4u  DIFFER
   0x0007  37(7)x2 78(x)x1 32(2)x1             3a(:)x5 aa(.)x3 00(.)x1 9d(.)x1 +4u  DIFFER
   0x0008  37(7)x2 6d(m)x1 32(2)x1             2f(/)x5 aa(.)x4 31(1)x1 27(')x1 +3u  DIFFER
   0x0009  32(2)x3 6c(l)x1                     6e(n)x5 aa(.)x3 32(2)x3 27(')x1 +2u  PARTIAL
   0x000a  2e(.)x2 5c(\)x1 32(2)x1             65(e)x5 aa(.)x3 2e(.)x2 37(7)x1 +3u  PARTIAL
   0x000b  78(x)x2 0a(.)x1 32(2)x1             65(e)x5 aa(.)x3 78(x)x2 37(7)x1 +3u  PARTIAL
   0x000c  6d(m)x2 3c(<)x1 32(2)x1             65(e)x5 aa(.)x3 6d(m)x2 37(7)x1 +3u  PARTIAL
   0x000d  6c(l)x2 3f(?)x1 0c(.)x1             6d(m)x5 8c(.)x2 ff(.)x2 6c(l)x2 +3u  PARTIAL
   0x000e  5c(\)x3 78(x)x1                     60(`)x4 aa(.)x3 5c(\)x3 2e(.)x1 +3u  PARTIAL
   0x000f  0a(.)x3 6d(m)x1                     22(")x5 0a(.)x3 32(2)x2 78(x)x1 +3u  PARTIAL
   0x0010  3c(<)x3 6c(l)x1                     3e(>)x5 3c(<)x3 2e(.)x2 6d(m)x1 +3u  PARTIAL
   0x0011  3f(?)x3 20( )x1                     62(b)x5 3f(?)x3 78(x)x2 32(2)x2 +2u  PARTIAL
   0x0012  78(x)x3 76(v)x1                     20( )x5 6d(m)x3 78(x)x2 5c(\)x1 +3u  PARTIAL
   0x0013  6d(m)x3 65(e)x1                     74(t)x5 6c(l)x3 6d(m)x2 0a(.)x1 +3u  PARTIAL
   0x0014  6c(l)x3 72(r)x1                     06(.)x5 5c(\)x2 6c(l)x2 3c(<)x1 +4u  PARTIAL
   0x0015  20( )x3 73(s)x1                     ff(.)x5 0a(.)x2 20( )x2 3f(?)x1 +4u  PARTIAL
   0x0016  76(v)x3 69(i)x1                     00(.)x5 3c(<)x2 65(e)x2 76(v)x2 +3u  PARTIAL
   0x0017  65(e)x3 6f(o)x1                     00(.)x5 65(e)x3 3f(?)x2 6d(m)x2 +2u  PARTIAL
   0x0018  72(r)x3 6e(n)x1                     31(1)x5 78(x)x2 6c(l)x2 72(r)x2 +3u  PARTIAL
   0x0019  73(s)x3 3d(=)x1                     32(2)x5 6d(m)x2 20( )x2 73(s)x2 +3u  PARTIAL
   0x001a  69(i)x3 22(")x1                     37(7)x5 6c(l)x2 76(v)x2 69(i)x2 +3u  PARTIAL
   0x001b  6f(o)x3 31(1)x1                     5c(\)x5 20( )x2 65(e)x2 6f(o)x2 +3u  PARTIAL
   0x001c  6e(n)x3 2e(.)x1                     0a(.)x5 76(v)x2 72(r)x2 6e(n)x2 +3u  PARTIAL
   0x001d  3d(=)x3 30(0)x1                     3c(<)x5 65(e)x2 73(s)x2 20( )x2 +2u  PARTIAL
   0x001e  22(")x4                             3f(?)x5 72(r)x2 69(i)x2 22(")x2 +3u  PARTIAL
   0x001f  31(1)x3 3f(?)x1                     6d(m)x5 73(s)x2 6f(o)x2 31(1)x2 +3u  PARTIAL
   0x0020  2e(.)x3 3e(>)x1                     6c(l)x5 69(i)x2 6e(n)x2 2e(.)x2 +3u  PARTIAL
   0x0021  30(0)x3 0a(.)x1                     20( )x5 6f(o)x2 3d(=)x2 30(0)x2 +3u  PARTIAL
   0x0022  22(")x3 3c(<)x1                     76(v)x5 22(")x4 6e(n)x2 00(.)x1 +2u  PARTIAL
   0x0023  3f(?)x3 21(!)x1                     65(e)x5 31(1)x3 3d(=)x2 3f(?)x2 +2u  PARTIAL
   0x0024  3e(>)x3 44(D)x1                     72(r)x5 22(")x2 2e(.)x2 3e(>)x2 +3u  PARTIAL
   0x0025  0a(.)x3 4f(O)x1                     73(s)x5 31(1)x2 30(0)x2 0a(.)x2 +3u  PARTIAL
   0x0026  3c(<)x3 43(C)x1                     69(i)x5 22(")x3 2e(.)x2 3c(<)x2 +2u  PARTIAL
   0x0027  21(!)x3 54(T)x1                     6f(o)x4 30(0)x2 3f(?)x2 21(!)x2 +4u  PARTIAL
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- fast ---
**Baseline relationship**: identical to `minimizer` (same
`[calibration, power]` stages, same `StdPowerMutationalStage`, same
FIFO corpus order) EXCEPT the corpus scheduler is
`PowerQueueScheduler::fast()`, which sets PowerSchedule `FAST` in
`SchedulerMetadata`. The single-technique delta is therefore `fast`
vs `minimizer`, not vs naive.

**Instrumentation**: naive's edge counters only.

**Feedback**: edge-bucket `MaxMapFeedback` + `CalibrationStage` (as
minimizer).

**Mutators / stages**: `[calibration, power]` with the havoc+token
`StdPowerMutationalStage` (as minimizer). The FAST schedule changes the
`perf_score` energy formula: the per-seed mutation budget is multiplied
by an AFLFast factor based on `n_fuzz` — log2 of how many times that
seed's coverage bucket has been exercised campaign-wide. Rarely-hit
paths get up to 4× energy; saturated paths are damped to 0.4×. Seed
*selection* order is still FIFO (`PowerQueueScheduler::next()` walks the
corpus in order); only the energy allocation differs from minimizer.

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge; calibration burst
per new entry; `n_fuzz` bookkeeping per execution.

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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_7146.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7146,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [minimizer>fast (aflfast_rarity)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7146 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7146 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7146 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).