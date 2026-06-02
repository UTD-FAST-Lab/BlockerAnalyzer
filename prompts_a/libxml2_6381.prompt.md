==== BLOCKER ====
Target: libxml2
Branch ID: 6381
Location: /src/libxml2/entities.c:299:9
Enclosing function: xmlGetPredefinedEntity
Source line:         case 'l':
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        2        7          1  REFERENCE
naive_ngram4                     3        7          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             3        7          0  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=8.80h  loser=16.50h
  avg hitcount on branch: winner=129  loser=329
  prob_div=0.80  dur_div=7.70h  hit_div=200
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=10.40h  loser=17.60h
  avg hitcount on branch: winner=358  loser=1
  prob_div=0.70  dur_div=7.20h  hit_div=357
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6381/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlGetPredefinedEntity (/src/libxml2/entities.c:296-321) ---
[ ]   294   */
[ ]   295  xmlEntityPtr
[B]   296  xmlGetPredefinedEntity(const xmlChar *name) {
[B]   297      if (name == NULL) return(NULL);
[B]   298      switch (name[0]) {
[W]   299          case 'l': <-- BLOCKER
[W]   300  	    if (xmlStrEqual(name, BAD_CAST "lt"))
[ ]   301  	        return(&xmlEntityLt);
[W]   302  	    break;
[W]   303          case 'g':
[ ]   304  	    if (xmlStrEqual(name, BAD_CAST "gt"))
[ ]   305  	        return(&xmlEntityGt);
[ ]   306  	    break;
[ ]   307          case 'a':
[ ]   308  	    if (xmlStrEqual(name, BAD_CAST "amp"))
[ ]   309  	        return(&xmlEntityAmp);
[ ]   310  	    if (xmlStrEqual(name, BAD_CAST "apos"))
[ ]   311  	        return(&xmlEntityApos);
[ ]   312  	    break;
[ ]   313          case 'q':
[ ]   314  	    if (xmlStrEqual(name, BAD_CAST "quot"))
[ ]   315  	        return(&xmlEntityQuot);
[ ]   316  	    break;
[L]   317  	default:
[L]   318  	    break;
[B]   319      }
[B]   320      return(NULL);
[B]   321  }

--- Caller (1 hop): xmlGetDocEntity (/src/libxml2/entities.c:541-563, calls xmlGetPredefinedEntity at line 562) (full body — short) ---
[B]   541  xmlGetDocEntity(const xmlDoc *doc, const xmlChar *name) {
[B]   542      xmlEntityPtr cur;
[B]   543      xmlEntitiesTablePtr table;
[ ]   544  
[B]   545      if (doc != NULL) {
[B]   546  	if ((doc->intSubset != NULL) && (doc->intSubset->entities != NULL)) {
[ ]   547  	    table = (xmlEntitiesTablePtr) doc->intSubset->entities;
[ ]   548  	    cur = xmlGetEntityFromTable(table, name);
[ ]   549  	    if (cur != NULL)
[ ]   550  		return(cur);
[ ]   551  	}
[B]   552  	if (doc->standalone != 1) {
[B]   553  	    if ((doc->extSubset != NULL) &&
[B]   554  		(doc->extSubset->entities != NULL)) {
[ ]   555  		table = (xmlEntitiesTablePtr) doc->extSubset->entities;
[ ]   556  		cur = xmlGetEntityFromTable(table, name);
[ ]   557  		if (cur != NULL)
[ ]   558  		    return(cur);
[ ]   559  	    }
[B]   560  	}
[B]   561      }
[B]   562      return(xmlGetPredefinedEntity(name)); <-- CALL
[B]   563  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  entities.c:xmlAddEntity  (/src/libxml2/entities.c:203-285, calls xmlGetPredefinedEntity at line 219)
hop 2  xmlGetDocEntity  (/src/libxml2/entities.c:541-563, calls xmlGetPredefinedEntity at line 562)
hop 3  xmlAddDocEntity  (/src/libxml2/entities.c:388-419, calls entities.c:xmlAddEntity at line 403)
hop 3  xmlAddDtdEntity  (/src/libxml2/entities.c:339-370, calls entities.c:xmlAddEntity at line 354)
hop 3  xmlschemastypes.c:xmlSchemaValAtomicType  (/src/libxml2/xmlschemastypes.c:2251-3465, calls xmlGetDocEntity at line 2939)
hop 4  xmlSAX2EntityDecl  (/src/libxml2/SAX2.c:630-683, calls xmlAddDtdEntity at line 660)
hop 4  xmlSAX2UnparsedEntityDecl  (/src/libxml2/SAX2.c:876-930, calls xmlAddDtdEntity at line 906)
hop 4  xmlNewEntity  (/src/libxml2/entities.c:441-457, calls xmlAddDocEntity at line 446)
hop 4  xmlSchemaValPredefTypeNode  (/src/libxml2/xmlschemastypes.c:3482-3485, calls xmlschemastypes.c:xmlSchemaValAtomicType at line 3483)
hop 4  xmlSchemaValPredefTypeNodeNoNorm  (/src/libxml2/xmlschemastypes.c:3503-3506, calls xmlschemastypes.c:xmlSchemaValAtomicType at line 3504)
hop 5  xmlParseEntityDecl  (/src/libxml2/parser.c:5476-5721, calls xmlSAX2EntityDecl at line 5598)
hop 5  relaxng.c:xmlRelaxNGSchemaTypeCheck  (/src/libxml2/relaxng.c:2464-2484, calls xmlSchemaValPredefTypeNode at line 2475)
hop 5  relaxng.c:xmlRelaxNGSchemaTypeCompare  (/src/libxml2/relaxng.c:2596-2632, calls xmlSchemaValPredefTypeNode at line 2609)
hop 5  xmlschemas.c:xmlSchemaVCheckCVCSimpleType  (/src/libxml2/xmlschemas.c:24723-25054, calls xmlSchemaValPredefTypeNodeNoNorm at line 24813)
hop 6  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseEntityDecl at line 6959)
hop 6  xmlschemas.c:xmlSchemaParseCheckCOSValidDefault  (/src/libxml2/xmlschemas.c:15954-16011, calls xmlschemas.c:xmlSchemaVCheckCVCSimpleType at line 15997)
hop 7  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 7  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 7  xmlschemas.c:xmlSchemaCheckElemPropsCorrect  (/src/libxml2/xmlschemas.c:19732-19890, calls xmlschemas.c:xmlSchemaParseCheckCOSValidDefault at line 19876)
hop 8  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 8  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 8  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 8  xmlschemas.c:xmlSchemaCheckElementDeclComponent  (/src/libxml2/xmlschemas.c:20140-20152, calls xmlschemas.c:xmlSchemaCheckElemPropsCorrect at line 20146)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     435      4090  xmlInitParser  (/src/libxml2/parser.c:14520-14553)
      26       592  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      60       390  xmlGetPredefinedEntity  (/src/libxml2/entities.c:296-321)  <-- enclosing
      18       316  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      32       289  xmlSkipBlankChars  (/src/libxml2/parser.c:2132-2217)
      15       261  xmlParseReference  (/src/libxml2/parser.c:7173-7586)
      15       261  xmlParseEntityRef  (/src/libxml2/parser.c:7619-7769)
      29       265  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      29       265  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
      41       258  xmlParseCharData  (/src/libxml2/parser.c:4480-4614)
      30       204  xmlGetDocEntity  (/src/libxml2/entities.c:541-563)
       1       166  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
       6       144  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
      10       115  parser.c:xmlParseLookupChar  (/src/libxml2/parser.c:11108-11124)
      18       115  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
... (77 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlGetDocEntity  (/src/libxml2/entities.c:541-563) ---
  d=2   L 545  T=30 F=0  T=204 F=0  if (doc != NULL) {
  d=2   L 546  T=0 F=30  T=0 F=190  if ((doc->intSubset != NULL) && (doc->intSubset->entities...
  d=2   L 546  T=30 F=0  T=190 F=14  if ((doc->intSubset != NULL) && (doc->intSubset->entities...
  d=2   L 552  T=30 F=0  T=204 F=0  if (doc->standalone != 1) {
  d=2   L 553  T=0 F=30  T=0 F=204  if ((doc->extSubset != NULL) &&
--- d=1  xmlGetPredefinedEntity  (/src/libxml2/entities.c:296-321) ---
  d=1   L 297  T=0 F=60  T=0 F=390  if (name == NULL) return(NULL);
  d=1   L 299  T=60 F=0  T=0 F=390  case 'l':  <-- BLOCKER
  d=1   L 300  T=0 F=60  T=0 F=0  if (xmlStrEqual(name, BAD_CAST "lt"))
  d=1   L 303  T=0 F=60  T=0 F=390  case 'g':
  d=1   L 307  T=0 F=60  T=0 F=390  case 'a':
  d=1   L 313  T=0 F=60  T=0 F=390  case 'q':
  d=1   L 317  T=0 F=60  T=390 F=0  default:

[off-chain: 1107 additional divergent branches across 85 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=e987102bebde5d16, size=402 bytes, fuzzer=cmplog, trial=5, discovered_at=17431s, mutation_op=CrossoverInsertMutator,CrossoverInsertMutator,CrossoverReplaceMutator,ByteAddMutator):
  0000: 01 00 00 00 31 32 37 37 00 32 2e 78 6d 6c 5c 0a   ....1277.2.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 09   .0"?>.<!DOCTYPE.
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 21 31   a SYSTEM "dtds!1

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=38501a99c7a866aa, size=386 bytes, fuzzer=naive, trial=1, discovered_at=5008s, mutation_op=BytesInsertCopyMutator,QwordAddMutator,BytesInsertMutator,DwordAddMutator):
  0000: 3d 06 00 00 00 31 32 37 37 33 32 2e 78 6d 6c 5c   =....127732.xml\
  0010: 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22   .<?xml version="
  0020: 47 2e 22 64 74 64 73 2f 31 32 37 6b 65 75 72 6c   G."dtds/127keurl
  0030: 2e 6e 22 3e 0a 0a 3c 61 3e 0a 20 20 3c 64 64 64   .n">..<a>.  <ddd
Seed 2 (id=fa1197ec4c86a140, size=405 bytes, fuzzer=naive, trial=1, discovered_at=12585s, mutation_op=BytesRandSetMutator,TokenReplace,CrossoverReplaceMutator,BytesRandInsertMutator):
  0000: 45 4d 45 3d 06 00 00 00 31 32 37 37 33 32 2e 78   EME=....127732.x
  0010: 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f   ml\.<?xml versio
  0020: 6e 3d 22 47 2e 22 64 74 64 73 2f 31 32 37 6b 65   n="G."dtds/127ke
  0030: 75 72 6c 2e 6e 22 3e 0a 0a 3c 61 3e 0a 20 20 3c   url.n">..<a>.  <
Seed 3 (id=a172dd2c7d78ee98, size=174 bytes, fuzzer=naive, trial=4, discovered_at=29422s, mutation_op=BytesCopyMutator,ByteRandMutator):
  0000: 3d 22 74 80 70 3a 2f 2f 2d 2d 2d 2e 2d 2d 2d 2d   ="t.p://---.----
  0010: 2d 2e 2d 2d 2d 2e 2e 2d 2d 36 2d 2d 2d 2e 2e 2d   -.---..--6---..-
  0020: 2d 2d 2d 2d 2d 2d 2d 2e 2d 2d 2d 2e 2e 2d 2d 2d   -------.---..---
  0030: 2d 2d 2e 2d 2d 2d 2e 2d 2d 2d 2e 2e 2d 2d 2d 2d   --.---.---..----
Seed 4 (id=c4db5506cfb84099, size=258 bytes, fuzzer=naive, trial=1, discovered_at=62229s, mutation_op=BytesExpandMutator,CrossoverInsertMutator,BytesCopyMutator):
  0000: 5f 5f 5f 5f 77 75 06 00 00 00 31 32 37 37 37 32   ____wu....127772
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "
Seed 5 (id=793608322986bf11, size=270 bytes, fuzzer=naive, trial=1, discovered_at=70094s, mutation_op=ByteInterestingMutator,ByteInterestingMutator,BytesCopyMutator):
  0000: 5f 10 00 5f 77 75 06 00 00 00 31 32 37 37 37 32   _.._wu....127772
  0010: 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73   .xml\.<?xml vers
  0020: 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f   ion="1.0"?>.<!DO
  0030: 43 54 59 50 45 20 61 20 53 59 53 54 45 4d 20 22   CTYPE a SYSTEM "


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  01(.)x1                             5f(_)x4 3d(=)x2 45(E)x1 61(a)x1     DIFFER
   0x0001  00(.)x1                             10(.)x3 06(.)x1 4d(M)x1 22(")x1 +2u  DIFFER
   0x0002  00(.)x1                             00(.)x4 45(E)x1 74(t)x1 5f(_)x1 +1u  PARTIAL
   0x0003  00(.)x1                             5f(_)x4 00(.)x1 3d(=)x1 80(.)x1 +1u  PARTIAL
   0x0004  31(1)x1                             77(w)x4 00(.)x1 06(.)x1 70(p)x1 +1u  DIFFER
   0x0005  32(2)x1                             75(u)x4 31(1)x1 00(.)x1 3a(:)x1 +1u  DIFFER
   0x0006  37(7)x1                             06(.)x3 32(2)x1 00(.)x1 2f(/)x1 +2u  DIFFER
   0x0007  37(7)x1                             00(.)x4 37(7)x1 2f(/)x1 ff(.)x1 +1u  PARTIAL
   0x0008  00(.)x1                             00(.)x3 37(7)x1 31(1)x1 2d(-)x1 +2u  PARTIAL
   0x0009  32(2)x1                             00(.)x4 33(3)x1 32(2)x1 2d(-)x1 +1u  PARTIAL
   0x000a  2e(.)x1                             31(1)x4 32(2)x1 37(7)x1 2d(-)x1 +1u  DIFFER
   0x000b  78(x)x1                             32(2)x4 2e(.)x2 37(7)x1 00(.)x1     DIFFER
   0x000c  6d(m)x1                             37(7)x4 78(x)x1 33(3)x1 2d(-)x1 +1u  DIFFER
   0x000d  6c(l)x1                             37(7)x4 6d(m)x1 32(2)x1 2d(-)x1 +1u  DIFFER
   0x000e  5c(\)x1                             37(7)x4 6c(l)x1 2e(.)x1 2d(-)x1 +1u  DIFFER
   0x000f  0a(.)x1                             32(2)x4 5c(\)x1 78(x)x1 2d(-)x1 +1u  DIFFER
   0x0010  3c(<)x1                             2e(.)x2 00(.)x2 0a(.)x1 6d(m)x1 +2u  DIFFER
   0x0011  3f(?)x1                             78(x)x2 40(@)x2 3c(<)x1 6c(l)x1 +2u  DIFFER
   0x0012  78(x)x1                             6d(m)x4 3f(?)x1 5c(\)x1 2d(-)x1 +1u  DIFFER
   0x0013  6d(m)x1                             6c(l)x4 78(x)x1 0a(.)x1 2d(-)x1 +1u  DIFFER
   0x0014  6c(l)x1                             5c(\)x4 6d(m)x1 3c(<)x1 2d(-)x1 +1u  DIFFER
   0x0015  20( )x1                             0a(.)x4 6c(l)x1 3f(?)x1 2e(.)x1 +1u  DIFFER
   0x0016  76(v)x1                             3c(<)x4 20( )x1 78(x)x1 2e(.)x1 +1u  DIFFER
   0x0017  65(e)x1                             3f(?)x4 76(v)x1 6d(m)x1 2d(-)x1 +1u  DIFFER
   0x0018  72(r)x1                             78(x)x4 65(e)x1 6c(l)x1 2d(-)x1 +1u  DIFFER
   0x0019  73(s)x1                             6d(m)x4 72(r)x1 20( )x1 36(6)x1 +1u  DIFFER
   0x001a  69(i)x1                             6c(l)x4 73(s)x1 76(v)x1 2d(-)x1 +1u  DIFFER
   0x001b  6f(o)x1                             20( )x4 69(i)x1 65(e)x1 2d(-)x1 +1u  DIFFER
   0x001c  6e(n)x1                             76(v)x4 6f(o)x1 72(r)x1 2d(-)x1 +1u  DIFFER
   0x001d  3d(=)x1                             65(e)x4 6e(n)x1 73(s)x1 2e(.)x1 +1u  DIFFER
   0x001e  22(")x1                             72(r)x4 3d(=)x1 69(i)x1 2e(.)x1 +1u  DIFFER
   0x001f  31(1)x1                             73(s)x4 22(")x1 6f(o)x1 2d(-)x1 +1u  DIFFER
   0x0020  2e(.)x1                             69(i)x4 47(G)x1 6e(n)x1 2d(-)x1 +1u  DIFFER
   0x0021  30(0)x1                             6f(o)x4 2e(.)x1 3d(=)x1 2d(-)x1 +1u  DIFFER
   0x0022  22(")x1                             6e(n)x4 22(")x2 2d(-)x1 78(x)x1     PARTIAL
   0x0023  3f(?)x1                             3d(=)x4 64(d)x1 47(G)x1 2d(-)x1 +1u  DIFFER
   0x0024  3e(>)x1                             22(")x4 74(t)x1 2e(.)x1 2d(-)x1 +1u  DIFFER
   0x0025  0a(.)x1                             31(1)x4 64(d)x1 22(")x1 2d(-)x1 +1u  DIFFER
   0x0026  3c(<)x1                             2e(.)x4 73(s)x1 64(d)x1 2d(-)x1 +1u  DIFFER
   0x0027  21(!)x1                             30(0)x4 2f(/)x1 74(t)x1 2e(.)x1 +1u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6381.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6381,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6381 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6381 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6381 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).