==== BLOCKER ====
Target: libxml2
Branch ID: 7107
Location: /src/libxml2/valid.c:3286:9
Enclosing function: valid.c:xmlGetDtdElementDesc2
Source line:     if (dtd->elements == NULL) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    2        8          0  REFERENCE
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        3        7          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.10h  loser=19.50h
  avg hitcount on branch: winner=286  loser=1
  prob_div=0.80  dur_div=19.40h  hit_div=285
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7107/{W,L}/branch_coverage_show.txt

--- Enclosing function: valid.c:xmlGetDtdElementDesc2 (/src/libxml2/valid.c:3280-3334) ---
[ ]  3278  
[ ]  3279  static xmlElementPtr
[B]  3280  xmlGetDtdElementDesc2(xmlDtdPtr dtd, const xmlChar *name, int create) {
[B]  3281      xmlElementTablePtr table;
[B]  3282      xmlElementPtr cur;
[B]  3283      xmlChar *uqname = NULL, *prefix = NULL;
[ ]  3284  
[B]  3285      if (dtd == NULL) return(NULL);
[B]  3286      if (dtd->elements == NULL) { <-- BLOCKER
[W]  3287  	xmlDictPtr dict = NULL;
[ ]  3288  
[W]  3289  	if (dtd->doc != NULL)
[W]  3290  	    dict = dtd->doc->dict;
[ ]  3291  
[W]  3292  	if (!create)
[ ]  3293  	    return(NULL);
[ ]  3294  	/*
[ ]  3295  	 * Create the Element table if needed.
[ ]  3296  	 */
[W]  3297  	table = (xmlElementTablePtr) dtd->elements;
[W]  3298  	if (table == NULL) {
[W]  3299  	    table = xmlHashCreateDict(0, dict);
[W]  3300  	    dtd->elements = (void *) table;
[W]  3301  	}
[W]  3302  	if (table == NULL) {
[ ]  3303  	    xmlVErrMemory(NULL, "element table allocation failed");
[ ]  3304  	    return(NULL);
[ ]  3305  	}
[W]  3306      }
[B]  3307      table = (xmlElementTablePtr) dtd->elements;
[ ]  3308  
[B]  3309      uqname = xmlSplitQName2(name, &prefix);
[B]  3310      if (uqname != NULL)
[ ]  3311          name = uqname;
[B]  3312      cur = xmlHashLookup2(table, name, prefix);
[B]  3313      if ((cur == NULL) && (create)) {
[B]  3314  	cur = (xmlElementPtr) xmlMalloc(sizeof(xmlElement));
[B]  3315  	if (cur == NULL) {
[ ]  3316  	    xmlVErrMemory(NULL, "malloc failed");
[ ]  3317  	    return(NULL);
[ ]  3318  	}
[B]  3319  	memset(cur, 0, sizeof(xmlElement));
[B]  3320  	cur->type = XML_ELEMENT_DECL;
[ ]  3321  
[ ]  3322  	/*
[ ]  3323  	 * fill the structure.
[ ]  3324  	 */
[B]  3325  	cur->name = xmlStrdup(name);
[B]  3326  	cur->prefix = xmlStrdup(prefix);
[B]  3327  	cur->etype = XML_ELEMENT_TYPE_UNDEFINED;
[ ]  3328  
[B]  3329  	xmlHashAddEntry2(table, name, prefix, cur);
[B]  3330      }
[B]  3331      if (prefix != NULL) xmlFree(prefix);
[B]  3332      if (uqname != NULL) xmlFree(uqname);
[B]  3333      return(cur);
[B]  3334  }

--- Caller (1 hop): xmlAddAttributeDecl (/src/libxml2/valid.c:1964-2172, calls valid.c:xmlGetDtdElementDesc2 at line 2116) (±10 around call site) ---
[ ]  2106  		 name, elem, NULL);
[ ]  2107  #endif /* LIBXML_VALID_ENABLED */
[ ]  2108  	xmlFreeAttribute(ret);
[ ]  2109  	return(NULL);
[ ]  2110      }
[ ]  2111  
[ ]  2112      /*
[ ]  2113       * Validity Check:
[ ]  2114       * Multiple ID per element
[ ]  2115       */
[B]  2116      elemDef = xmlGetDtdElementDesc2(dtd, elem, 1); <-- CALL
[B]  2117      if (elemDef != NULL) {
[ ]  2118  
[B]  2119  #ifdef LIBXML_VALID_ENABLED
[B]  2120          if ((type == XML_ATTRIBUTE_ID) &&
[B]  2121  	    (xmlScanIDAttributeDecl(NULL, elemDef, 1) != 0)) {
[ ]  2122  	    xmlErrValidNode(ctxt, (xmlNodePtr) dtd, XML_DTD_MULTIPLE_ID,
[ ]  2123  	   "Element %s has too may ID attributes defined : %s\n",
[ ]  2124  		   elem, name, NULL);
[ ]  2125  	    if (ctxt != NULL)
[ ]  2126  		ctxt->valid = 0;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172, calls valid.c:xmlGetDtdElementDesc2 at line 2116)
hop 3  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758, calls xmlAddAttributeDecl at line 731)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      15       192  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      88         0  xmlGetDtdQElementDesc  (/src/libxml2/valid.c:3349-3357)
       0        57  xmlAddElementDecl  (/src/libxml2/valid.c:1414-1620)
      28         0  xmlValidCtxtNormalizeAttributeValue  (/src/libxml2/valid.c:4061-4111)
      26         0  xmlGetDtdQAttrDesc  (/src/libxml2/valid.c:3410-3418)
       0        18  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
       6        24  valid.c:xmlValidateNmtokensValueInternal  (/src/libxml2/valid.c:3765-3810)
       0         9  xmlValidateAttributeDecl  (/src/libxml2/valid.c:4197-4288)
       0         9  valid.c:xmlValidateAttributeCallback  (/src/libxml2/valid.c:6762-6830)
       0         6  xmlValidateElementDecl  (/src/libxml2/valid.c:4308-4401)
       3         0  valid.c:xmlErrValidNode  (/src/libxml2/valid.c:139-159)
       3         0  valid.c:xmlValidNormalizeString  (/src/libxml2/valid.c:2596-2616)
       0         3  xmlIsMixedElement  (/src/libxml2/valid.c:3487-3511)
       0         3  xmlValidateRoot  (/src/libxml2/valid.c:6397-6446)
       0         3  xmlValidateDtdFinal  (/src/libxml2/valid.c:6850-6879)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172) ---
  d=2   L2018  T=3 F=30  T=0 F=51  (!xmlValidateAttributeValueInternal(dtd->doc, type, defau...
  d=2   L2023  T=3 F=0  T=0 F=0  if (ctxt != NULL)
  d=2   L2135  T=3 F=24  T=57 F=6  ((ret->prefix != NULL &&
  d=2   L2136  T=0 F=3  T=21 F=36  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns"))))) {
  d=2   L2143  T=0 F=9  T=6 F=33  ((xmlStrEqual(tmp->name, BAD_CAST "xmlns")) ||
  d=2   L2144  T=3 F=6  T=33 F=0  ((ret->prefix != NULL &&
  d=2   L2145  T=0 F=3  T=0 F=33  (xmlStrEqual(ret->prefix, BAD_CAST "xmlns")))))) {
  d=2   L2146  T=0 F=0  T=3 F=3  if (tmp->nexth == NULL)
  d=2   L2164  T=27 F=9  T=0 F=66  if (dtd->last == NULL) {
--- d=1  valid.c:xmlGetDtdElementDesc2  (/src/libxml2/valid.c:3280-3334) ---
  d=1   L3286  T=27 F=9  T=0 F=66  if (dtd->elements == NULL) {  <-- BLOCKER
  d=1   L3289  T=27 F=0  T=0 F=0  if (dtd->doc != NULL)
  d=1   L3292  T=0 F=27  T=0 F=0  if (!create)
  d=1   L3298  T=27 F=0  T=0 F=0  if (table == NULL) {
  d=1   L3302  T=0 F=27  T=0 F=0  if (table == NULL) {
  d=1   L3313  T=27 F=0  T=3 F=0  if ((cur == NULL) && (create)) {
  d=1   L3315  T=0 F=27  T=0 F=3  if (cur == NULL) {

[off-chain: 200 additional divergent branches across 24 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=1047d2c3429fdf34, size=164 bytes, fuzzer=grimoire, trial=1, discovered_at=1697s, mutation_op=I2SRandReplace):
  0000: 7f f0 fa 02 7e 96 98 00 fc ff ff ff ff ff ff ff   ....~...........
  0010: 80 69 67 ff ff ff ff ff fd ff ff ff 00 00 00 40   .ig............@
  0020: 00 16 a9 05 06 00 31 6c 5c 0a 3c 3f 6c 20 3f 3e   ......1l\.<?l ?>
  0030: 3c 21 44 4f 43 54 59 50 45 61 20 53 59 53 54 45   <!DOCTYPEa SYSTE
Seed 2 (id=07198a887a941246, size=147 bytes, fuzzer=grimoire, trial=1, discovered_at=3762s, mutation_op=GrimoireExtensionMutator,GrimoireRecursiveReplacementMutator,GrimoireRandomDeleteMutator):
  0000: ff 06 49 53 4f 2d 38 38 35 39 2d 35 6c 5c 0a 3c   ..ISO-8859-5l\.<
  0010: 3f 6c 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20 53   ?l?><!DOCTYPEa S
  0020: 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37   YSTEM "dtds/1277
  0030: 37 32 2e 64 74 64 22 3e 5c 0a 64 74 64 73 2f 31   72.dtd">\.dtds/1
Seed 3 (id=a438d45b1757ca3f, size=555 bytes, fuzzer=grimoire, trial=1, discovered_at=5602s, mutation_op=GrimoireExtensionMutator,GrimoireRecursiveReplacementMutator):
  0000: 27 68 74 74 70 3a 2f 2f f5 ff ff ff ff ff ff ff   'http://........
  0010: 69 64 00 00 d1 01 00 23 06 00 31 6c 5c 0a 3c 3f   id.....#..1l\.<?
  0020: 6c 48 54 4d 4c 3f 3e 3c 21 44 4f 43 54 59 50 45   lHTML?><!DOCTYPE
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=b3f5d62fb26f5823, size=214 bytes, fuzzer=grimoire, trial=1, discovered_at=8398s, mutation_op=I2SRandReplace):
  0000: 2f 2f 2f 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   ///l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 3c 61 3e 3c 62 20 78 6c 69 6e 6b 3d 22 22 3e 3c   <a><b xlink=""><
Seed 5 (id=9d8c776ad564d013, size=181 bytes, fuzzer=grimoire, trial=1, discovered_at=11025s, mutation_op=BytesExpandMutator,BytesInsertMutator):
  0000: 27 68 74 74 70 3a 2f 2f 2f 20 28 20 68 74 74 70   'http:/// ( http
  0010: 3a 2f 2f 2f 20 28 20 20 06 00 31 6c 5c 0a 3c 3f   :/// (  ..1l\.<?
  0020: 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20 53   l ?><!DOCTYPEa S
  0030: 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37   YSTEM "dtds/1277

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0be939129cb3ca8a, size=377 bytes, fuzzer=cmplog, trial=1, discovered_at=3s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=0d5f26ea8b67d379, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=93s, mutation_op=DwordInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=01986dbadd87a561, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=128s, mutation_op=ByteDecMutator,CrossoverReplaceMutator,BytesRandInsertMutator,ByteAddMutator,ByteAddMutator,CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=273e1a1b133aabea, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=229s, mutation_op=BytesSwapMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 09 20 76 65 72 73 69 27 0a 20 20 20   <?xm. versi'.   
  0020: 20 20 20 6f 22 3d 22 31 2e 30 22 3f 3e 0a 3c 21      o"="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
Seed 5 (id=1c65f70d71c9b113, size=370 bytes, fuzzer=cmplog, trial=1, discovered_at=241s, mutation_op=BytesSetMutator,BytesSetMutator,BytesExpandMutator):
  0000: 3d 3d 3d 3d 3d 32 37 37 37 32 2e 20 20 20 5c 0a   =====27772.   \.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  27(')x3 e9(.)x2 7f(.)x1 ff(.)x1 +3u  06(.)x7 3d(=)x1 2b(+)x1 07(.)x1     PARTIAL
   0x0001  68(h)x3 f0(.)x1 06(.)x1 2f(/)x1 +4u  00(.)x9 3d(=)x1                     DIFFER
   0x0002  74(t)x3 ff(.)x2 fa(.)x1 49(I)x1 +3u  00(.)x9 3d(=)x1                     DIFFER
   0x0003  74(t)x3 ff(.)x3 02(.)x1 53(S)x1 +2u  00(.)x9 3d(=)x1                     PARTIAL
   0x0004  70(p)x3 ff(.)x2 7e(~)x1 4f(O)x1 +3u  31(1)x9 3d(=)x1                     DIFFER
   0x0005  3a(:)x3 00(.)x2 ff(.)x2 96(.)x1 +2u  32(2)x10                            DIFFER
   0x0006  2f(/)x3 ff(.)x2 98(.)x1 38(8)x1 +3u  37(7)x10                            DIFFER
   0x0007  2f(/)x3 6c(l)x2 ff(.)x2 00(.)x1 +2u  37(7)x10                            DIFFER
   0x0008  2f(/)x2 5c(\)x2 06(.)x2 fc(.)x1 +3u  37(7)x10                            DIFFER
   0x0009  ff(.)x2 20( )x2 0a(.)x2 31(1)x2 +2u  32(2)x10                            DIFFER
   0x000a  ff(.)x2 3c(<)x2 6d(m)x2 2d(-)x1 +3u  2e(.)x10                            DIFFER
   0x000b  ff(.)x2 3f(?)x2 6c(l)x2 35(5)x1 +3u  78(x)x9 20( )x1                     PARTIAL
   0x000c  6c(l)x3 ff(.)x2 5c(\)x2 3c(<)x1 +2u  6d(m)x9 20( )x1                     DIFFER
   0x000d  ff(.)x2 0a(.)x2 5c(\)x1 21(!)x1 +4u  6c(l)x9 20( )x1                     PARTIAL
   0x000e  ff(.)x2 3c(<)x2 0a(.)x1 44(D)x1 +4u  5c(\)x10                            DIFFER
   0x000f  ff(.)x2 3c(<)x2 3f(?)x2 4f(O)x1 +3u  0a(.)x10                            DIFFER
   0x0010  6c(l)x2 80(.)x1 3f(?)x1 69(i)x1 +5u  3c(<)x10                            PARTIAL
   0x0011  20( )x2 69(i)x1 6c(l)x1 64(d)x1 +5u  3f(?)x10                            DIFFER
   0x0012  3f(?)x3 67(g)x1 00(.)x1 59(Y)x1 +4u  78(x)x10                            DIFFER
   0x0013  3e(>)x3 ff(.)x1 00(.)x1 50(P)x1 +4u  6d(m)x10                            DIFFER
   0x0014  3c(<)x3 ff(.)x1 d1(.)x1 45(E)x1 +4u  6c(l)x9 09(.)x1                     DIFFER
   0x0015  21(!)x3 ff(.)x1 01(.)x1 61(a)x1 +4u  20( )x10                            DIFFER
   0x0016  44(D)x3 20( )x2 ff(.)x1 00(.)x1 +3u  76(v)x10                            DIFFER
   0x0017  4f(O)x3 ff(.)x1 23(#)x1 53(S)x1 +4u  65(e)x10                            DIFFER
   0x0018  43(C)x3 06(.)x2 fd(.)x1 59(Y)x1 +3u  72(r)x10                            DIFFER
   0x0019  54(T)x3 00(.)x2 ff(.)x1 53(S)x1 +3u  73(s)x10                            DIFFER
   0x001a  59(Y)x3 31(1)x2 ff(.)x1 54(T)x1 +3u  69(i)x10                            DIFFER
   0x001b  50(P)x3 6c(l)x2 ff(.)x1 45(E)x1 +3u  6f(o)x9 27(')x1                     DIFFER
   0x001c  45(E)x3 5c(\)x2 00(.)x1 4d(M)x1 +3u  6e(n)x9 0a(.)x1                     DIFFER
   0x001d  61(a)x3 0a(.)x2 00(.)x1 20( )x1 +3u  3d(=)x9 20( )x1                     PARTIAL
   0x001e  20( )x3 3c(<)x2 00(.)x1 22(")x1 +3u  22(")x9 20( )x1                     PARTIAL
   0x001f  53(S)x3 3f(?)x2 40(@)x1 64(d)x1 +3u  31(1)x9 20( )x1                     PARTIAL
   0x0020  59(Y)x3 6c(l)x2 00(.)x1 74(t)x1 +3u  2e(.)x9 20( )x1                     PARTIAL
   0x0021  53(S)x3 20( )x2 16(.)x1 48(H)x1 +3u  30(0)x9 20( )x1                     PARTIAL
   0x0022  54(T)x4 a9(.)x1 73(s)x1 3f(?)x1 +3u  22(")x9 20( )x1                     PARTIAL
   0x0023  45(E)x3 05(.)x1 4d(M)x1 2f(/)x1 +4u  3f(?)x9 6f(o)x1                     DIFFER
   0x0024  4d(M)x3 06(.)x1 4c(L)x1 31(1)x1 +4u  3e(>)x9 22(")x1                     DIFFER
   0x0025  20( )x3 00(.)x1 3f(?)x1 32(2)x1 +4u  0a(.)x9 3d(=)x1                     DIFFER
   0x0026  22(")x3 31(1)x1 3e(>)x1 37(7)x1 +4u  3c(<)x9 22(")x1                     PARTIAL
   0x0027  64(d)x3 6c(l)x1 3c(<)x1 37(7)x1 +4u  21(!)x9 31(1)x1                     PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7107.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7107,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7107 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7107 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7107 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).