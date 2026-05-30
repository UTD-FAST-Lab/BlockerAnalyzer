==== BLOCKER ====
Target: libxml2
Branch ID: 7143
Location: /src/libxml2/valid.c:3779:9
Enclosing function: valid.c:xmlValidateNmtokensValueInternal
Source line:     if (!xmlIsDocNameChar(doc, val))
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile)
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog); loser (grimoire_structural vs grimoire)
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog)
naive_ctx                        1        8          1  REFERENCE
naive_ngram4                     2        7          1  REFERENCE
mopt                             1        8          1  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             4        5          1  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (3) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=3.60h  loser=19.10h
  avg hitcount on branch: winner=8  loser=2
  prob_div=0.80  dur_div=15.50h  hit_div=6
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 2: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.10h  loser=19.10h
  avg hitcount on branch: winner=333  loser=2
  prob_div=0.80  dur_div=19.00h  hit_div=331
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002
--- Pair 3: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=8.90h  loser=17.40h
  avg hitcount on branch: winner=6  loser=1
  prob_div=0.60  dur_div=8.50h  hit_div=6
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7143/{W,L}/branch_coverage_show.txt

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
[B]  3779      if (!xmlIsDocNameChar(doc, val)) <-- BLOCKER
[W]  3780  	return(0);
[ ]  3781  
[L]  3782      while (xmlIsDocNameChar(doc, val)) {
[L]  3783  	val = xmlStringCurrentChar(NULL, cur, &len);
[L]  3784  	cur += len;
[L]  3785      }
[ ]  3786  
[ ]  3787      /* Should not test IS_BLANK(val) here -- see erratum E20*/
[L]  3788      while (val == 0x20) {
[L]  3789  	while (val == 0x20) {
[L]  3790  	    val = xmlStringCurrentChar(NULL, cur, &len);
[L]  3791  	    cur += len;
[L]  3792  	}
[L]  3793  	if (val == 0) return(1);
[ ]  3794  
[L]  3795  	if (!xmlIsDocNameChar(doc, val))
[L]  3796  	    return(0);
[ ]  3797  
[L]  3798  	val = xmlStringCurrentChar(NULL, cur, &len);
[L]  3799  	cur += len;
[ ]  3800  
[L]  3801  	while (xmlIsDocNameChar(doc, val)) {
[L]  3802  	    val = xmlStringCurrentChar(NULL, cur, &len);
[L]  3803  	    cur += len;
[L]  3804  	}
[L]  3805      }
[ ]  3806  
[L]  3807      if (val != 0) return(0);
[ ]  3808  
[L]  3809      return(1);
[L]  3810  }

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
      29       470  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      26        78  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
       1        16  xmlIsID  (/src/libxml2/valid.c:2767-2816)
       1        16  xmlIsRef  (/src/libxml2/valid.c:3115-3143)
       9         2  xmlGetDtdQAttrDesc  (/src/libxml2/valid.c:3410-3418)
       3         9  xmlIsMixedElement  (/src/libxml2/valid.c:3487-3511)
       3         0  valid.c:xmlErrValidWarning  (/src/libxml2/valid.c:217-237)
       0         3  valid.c:nodeVPop  (/src/libxml2/valid.c:452-465)
       3         0  valid.c:xmlValidateAttributeValue2  (/src/libxml2/valid.c:3945-4033)
       3         0  xmlValidNormalizeAttributeValue  (/src/libxml2/valid.c:4134-4167)
       3         0  xmlValidateOneNamespace  (/src/libxml2/valid.c:4607-4810)
       0         3  valid.c:xmlValidateOneCdataElement  (/src/libxml2/valid.c:5607-5660)
       0         3  xmlValidateOneElement  (/src/libxml2/valid.c:6034-6380)
       0         1  xmlValidatePushCData  (/src/libxml2/valid.c:5899-5958)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172) ---
  d=3   L2023  T=29 F=0  T=6 F=0  if (ctxt != NULL)
  d=3   L2089  T=14 F=12  T=86 F=12  if (dict)
  d=3   L2099  T=3 F=66  T=0 F=137  if (xmlHashAddEntry3(table, ret->name, ret->prefix, ret->...
  d=3   L2117  T=66 F=0  T=137 F=0  if (elemDef != NULL) {
  d=3   L2120  T=0 F=66  T=0 F=137  if ((type == XML_ATTRIBUTE_ID) &&
  d=3   L2134  T=6 F=60  T=3 F=134  if ((xmlStrEqual(ret->name, BAD_CAST "xmlns")) ||
  d=3   L2135  T=18 F=42  T=125 F=9  ((ret->prefix != NULL &&
  d=3   L2136  T=6 F=12  T=43 F=82  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns"))))) {
  d=3   L2143  T=6 F=34  T=6 F=82  ((xmlStrEqual(tmp->name, BAD_CAST "xmlns")) ||
  d=3   L2144  T=12 F=22  T=76 F=6  ((ret->prefix != NULL &&
  d=3   L2145  T=0 F=12  T=0 F=76  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns")))))) {
  d=3   L2146  T=6 F=0  T=3 F=3  if (tmp->nexth == NULL)
  d=3   L2164  T=3 F=63  T=0 F=137  if (dtd->last == NULL) {
--- d=1  valid.c:xmlValidateNmtokensValueInternal  (/src/libxml2/valid.c:3765-3810) ---
  d=1   L3769  T=0 F=29  T=0 F=58  if (value == NULL) return(0);
  d=1   L3779  T=29 F=0  T=0 F=58  if (!xmlIsDocNameChar(doc, val))  <-- BLOCKER
  d=1   L3782  T=0 F=0  T=285 F=58  while (xmlIsDocNameChar(doc, val)) {
  d=1   L3788  T=0 F=0  T=18 F=55  while (val == 0x20) {
  d=1   L3789  T=0 F=0  T=18 F=18  while (val == 0x20) {
  d=1   L3793  T=0 F=0  T=0 F=18  if (val == 0) return(1);
  d=1   L3795  T=0 F=0  T=3 F=15  if (!xmlIsDocNameChar(doc, val))
  d=1   L3801  T=0 F=0  T=36 F=15  while (xmlIsDocNameChar(doc, val)) {
  d=1   L3807  T=0 F=0  T=3 F=52  if (val != 0) return(0);

[off-chain: 301 additional divergent branches across 29 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=03ed72aae69e1480, size=195 bytes, fuzzer=grimoire, trial=1, discovered_at=27s, mutation_op=GrimoireExtensionMutator):
  0000: 06 00 00 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   ...l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 3c 61 3e 3c 62 20 6b 3a 68 72 65 67 3d 22 74 22   <a><b k:hreg="t"
Seed 2 (id=8f8537181bfef3b5, size=234 bytes, fuzzer=grimoire, trial=1, discovered_at=1816s, mutation_op=I2SRandReplace,I2SRandReplace):
  0000: 55 54 46 38 06 00 37 37 32 2e 78 6d 6c 5c 0a 3c   UTF8..772.xml\.<
  0010: 3f 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20   ?l ?><!DOCTYPEa 
  0020: 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37   SYSTEM "dtds/127
  0030: 37 37 32 2e 64 74 64 22 3e 3c 61 3e 0a 20 20 3c   772.dtd"><a>.  <
Seed 3 (id=9ac54fe3dd9be284, size=216 bytes, fuzzer=grimoire, trial=1, discovered_at=1816s, mutation_op=GrimoireRecursiveReplacementMutator):
  0000: 45 55 43 2d 4a 50 55 54 46 38 06 00 5c 0a 3c 3f   EUC-JPUTF8..\.<?
  0010: 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20 53   l ?><!DOCTYPEa S
  0020: 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37   YSTEM "dtds/1277
  0030: 37 32 2e 64 74 64 22 3e 3c 61 3e 20 3c 62 20 6b   72.dtd"><a> <b k
Seed 4 (id=75a0e7d3edec39d2, size=177 bytes, fuzzer=grimoire, trial=1, discovered_at=6311s, mutation_op=BytesExpandMutator):
  0000: 06 31 32 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   .12l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 3c 61 3e 3c 62 20 66 3d 22 5c 0a 64 74 64 73 2f   <a><b f="\.dtds/
Seed 5 (id=3ab4d97b081ac59f, size=173 bytes, fuzzer=grimoire, trial=1, discovered_at=6390s, mutation_op=GrimoireRandomDeleteMutator,GrimoireRandomDeleteMutator,GrimoireRecursiveReplacementMutator):
  0000: d8 3e 42 0f 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44   .>B.l\.<?l ?><!D
  0010: 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22   OCTYPEa SYSTEM "
  0020: 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22   dtds/127772.dtd"
  0030: 3e 3c 61 3e 3c 62 20 51 3d 22 22 3e 5c 0a 64 74   ><a><b Q="">\.dt

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=8c7bd7ba6dfb824c, size=368 bytes, fuzzer=naive, trial=1):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=2fc1276953baf917, size=370 bytes, fuzzer=cmplog, trial=1, discovered_at=2s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=0be939129cb3ca8a, size=377 bytes, fuzzer=cmplog, trial=1, discovered_at=3s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=5fc4f2e61808d2a4, size=395 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=BytesInsertCopyMutator,ByteFlipMutator,BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=28d3c1a014f52844, size=547 bytes, fuzzer=naive, trial=1, discovered_at=72s, mutation_op=BytesSetMutator,DwordInterestingMutator):
  0000: 6e 65 8b 22 3e 62 20 74 65 78 6d 6c 5c 0a 3c 3f   ne.">b texml\.<?
  0010: 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30   xml version="1.0
  0020: 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20   "?>.<!DOCTYPE a 
  0030: 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37   SYSTEM "dtds/127


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x000d  21(!)x2 5c(\)x1 0a(.)x1 3c(<)x1 +5u  6c(l)x14 4f(O)x2 0a(.)x1 20( )x1    PARTIAL
   0x000e  44(D)x2 0a(.)x1 3c(<)x1 21(!)x1 +5u  5c(\)x14 20( )x2 3c(<)x1 65(e)x1    PARTIAL
   0x0013  50(P)x2 3f(?)x1 3e(>)x1 59(Y)x1 +5u  6d(m)x14 20( )x2 69(i)x1 6e(n)x1    DIFFER
   0x0017  53(S)x2 44(D)x1 4f(O)x1 20( )x1 +5u  65(e)x14 2e(.)x2 73(s)x1 22(")x1    DIFFER
   0x0028  37(7)x3 64(d)x1 74(t)x1 73(s)x1 +4u  44(D)x14 20( )x2 43(C)x1 4c(L)x1    DIFFER
   0x002a  2e(.)x2 64(d)x1 73(s)x1 32(2)x1 +5u  43(C)x14 59(Y)x2 20( )x1 39(9)x1    DIFFER
   0x002b  64(d)x2 20( )x2 73(s)x1 2f(/)x1 +4u  54(T)x14 53(S)x2 50(P)x1 39(9)x1    PARTIAL
   0x002c  74(t)x2 2f(/)x1 31(1)x1 64(d)x1 +5u  59(Y)x15 45(E)x1 54(T)x1 2f(/)x1    PARTIAL
   0x002d  64(d)x2 31(1)x1 32(2)x1 74(t)x1 +5u  50(P)x14 20( )x2 53(S)x1 45(E)x1    PARTIAL
   0x002f  3e(>)x2 37(7)x2 74(t)x2 22(")x1 +3u  20( )x17 45(E)x1                    PARTIAL
   0x0031  61(a)x2 22(")x2 37(7)x1 32(2)x1 +4u  20( )x16 59(Y)x1 64(d)x1            PARTIAL
   0x0032  3e(>)x3 20( )x2 32(2)x1 2e(.)x1 +3u  53(S)x15 22(")x1 74(t)x1 20( )x1    PARTIAL
   0x0033  3c(<)x3 3e(>)x2 2e(.)x1 64(d)x1 +3u  59(Y)x14 64(d)x2 54(T)x1 44(D)x1    PARTIAL
   0x003a  65(e)x1 61(a)x1 3e(>)x1 0a(.)x1 +6u  64(d)x15 37(7)x2 20( )x1            PARTIAL
   0x003f  22(")x1 3c(<)x1 6b(k)x1 2f(/)x1 +6u  31(1)x14 64(d)x2 37(7)x1 20( )x1    PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7143.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7143,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), grimoire>cmplog (grimoire_structural), value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7143 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7143 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7143 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).