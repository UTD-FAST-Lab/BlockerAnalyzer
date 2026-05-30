==== BLOCKER ====
Target: libxml2
Branch ID: 6909
Location: /src/libxml2/tree.c:283:9
Enclosing function: xmlSplitQName2
Source line:     if (name[0] == ':')
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        5        5          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=4.10h  loser=23.50h
  avg hitcount on branch: winner=35  loser=0
  prob_div=1.00  dur_div=19.40h  hit_div=35
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6909/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlSplitQName2 (/src/libxml2/tree.c:267-312) ---
[ ]   265   */
[ ]   266  xmlChar *
[B]   267  xmlSplitQName2(const xmlChar *name, xmlChar **prefix) {
[B]   268      int len = 0;
[B]   269      xmlChar *ret = NULL;
[ ]   270  
[B]   271      if (prefix == NULL) return(NULL);
[B]   272      *prefix = NULL;
[B]   273      if (name == NULL) return(NULL);
[ ]   274  
[ ]   275  #ifndef XML_XML_NAMESPACE
[ ]   276      /* xml: prefix is not really a namespace */
[ ]   277      if ((name[0] == 'x') && (name[1] == 'm') &&
[ ]   278          (name[2] == 'l') && (name[3] == ':'))
[ ]   279  	return(NULL);
[ ]   280  #endif
[ ]   281  
[ ]   282      /* nasty but valid */
[B]   283      if (name[0] == ':') <-- BLOCKER
[W]   284  	return(NULL);
[ ]   285  
[ ]   286      /*
[ ]   287       * we are not trying to validate but just to cut, and yes it will
[ ]   288       * work even if this is as set of UTF-8 encoded chars
[ ]   289       */
[B]   290      while ((name[len] != 0) && (name[len] != ':'))
[B]   291  	len++;
[ ]   292  
[B]   293      if (name[len] == 0)
[B]   294  	return(NULL);
[ ]   295  
[L]   296      *prefix = xmlStrndup(name, len);
[L]   297      if (*prefix == NULL) {
[ ]   298  	xmlTreeErrMemory("QName split");
[ ]   299  	return(NULL);
[ ]   300      }
[L]   301      ret = xmlStrdup(&name[len + 1]);
[L]   302      if (ret == NULL) {
[ ]   303  	xmlTreeErrMemory("QName split");
[ ]   304  	if (*prefix != NULL) {
[ ]   305  	    xmlFree(*prefix);
[ ]   306  	    *prefix = NULL;
[ ]   307  	}
[ ]   308  	return(NULL);
[ ]   309      }
[ ]   310  
[L]   311      return(ret);
[L]   312  }

--- Caller (1 hop): xmlGetDtdElementDesc (/src/libxml2/valid.c:3250-3267, calls xmlSplitQName2 at line 3260) (full body — short) ---
[B]  3250  xmlGetDtdElementDesc(xmlDtdPtr dtd, const xmlChar *name) {
[B]  3251      xmlElementTablePtr table;
[B]  3252      xmlElementPtr cur;
[B]  3253      xmlChar *uqname = NULL, *prefix = NULL;
[ ]  3254  
[B]  3255      if ((dtd == NULL) || (name == NULL)) return(NULL);
[B]  3256      if (dtd->elements == NULL)
[B]  3257  	return(NULL);
[B]  3258      table = (xmlElementTablePtr) dtd->elements;
[ ]  3259  
[B]  3260      uqname = xmlSplitQName2(name, &prefix); <-- CALL
[B]  3261      if (uqname != NULL)
[ ]  3262          name = uqname;
[B]  3263      cur = xmlHashLookup2(table, name, prefix);
[B]  3264      if (prefix != NULL) xmlFree(prefix);
[B]  3265      if (uqname != NULL) xmlFree(uqname);
[B]  3266      return(cur);
[B]  3267  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  relaxng.c:xmlRelaxNGCleanupTree  (/src/libxml2/relaxng.c:7043-7472, calls xmlSplitQName2 at line 7295)
hop 2  xmlTextReaderGetAttribute  (/src/libxml2/xmlreader.c:2317-2374, calls xmlSplitQName2 at line 2334)
hop 3  relaxng.c:xmlRelaxNGCleanupDoc  (/src/libxml2/relaxng.c:7486-7500, calls relaxng.c:xmlRelaxNGCleanupTree at line 7498)
hop 4  relaxng.c:xmlRelaxNGLoadExternalRef  (/src/libxml2/relaxng.c:1953-2027, calls relaxng.c:xmlRelaxNGCleanupDoc at line 2018)
hop 4  relaxng.c:xmlRelaxNGLoadInclude  (/src/libxml2/relaxng.c:1605-1765, calls relaxng.c:xmlRelaxNGCleanupDoc at line 1681)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      80        12  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
      27         0  xmlSearchNs  (/src/libxml2/tree.c:6134-6207)
      24         0  xmlGetDtdQElementDesc  (/src/libxml2/valid.c:3349-3357)
      36        12  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
      24         0  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      30         8  xmlAddChild  (/src/libxml2/tree.c:3418-3532)
      21         6  xmlValidateElementDecl  (/src/libxml2/valid.c:4308-4401)
      14         0  valid.c:xmlErrValidNode  (/src/libxml2/valid.c:139-159)
      13         0  xmlNewNode  (/src/libxml2/tree.c:2259-2287)
      13         0  xmlNewDocNode  (/src/libxml2/tree.c:2352-2369)
      11         0  xmlIsMixedElement  (/src/libxml2/valid.c:3487-3511)
       9         0  xmlDocGetRootElement  (/src/libxml2/tree.c:5057-5068)
       9         0  xmlValidateRoot  (/src/libxml2/valid.c:6397-6446)
       9         0  xmlValidateDtdFinal  (/src/libxml2/valid.c:6850-6879)
       8         0  xmlGetLastChild  (/src/libxml2/tree.c:3542-3551)
... (38 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlSplitQName2  (/src/libxml2/tree.c:267-312) ---
  d=1   L 283  T=33 F=64  T=0 F=67  if (name[0] == ':')  <-- BLOCKER
  d=1   L 290  T=64 F=0  T=169 F=6  while ((name[len] != 0) && (name[len] != ':'))
  d=1   L 293  T=64 F=0  T=61 F=6  if (name[len] == 0)
  d=1   L 297  T=0 F=0  T=0 F=6  if (*prefix == NULL) {
  d=1   L 302  T=0 F=0  T=0 F=6  if (ret == NULL) {

[off-chain: 593 additional divergent branches across 77 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=a51d8f73d729c337, size=361 bytes, fuzzer=cmplog, trial=1, discovered_at=3395s, mutation_op=BytesCopyMutator,QwordAddMutator,BitFlipMutator,BytesRandSetMutator,WordAddMutator,BytesDeleteMutator,BytesSetMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
Seed 2 (id=b95689e94eabb200, size=464 bytes, fuzzer=cmplog, trial=1, discovered_at=4283s, mutation_op=ByteInterestingMutator,WordAddMutator,CrossoverInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=46f8f4fb7afd3e70, size=378 bytes, fuzzer=cmplog, trial=1, discovered_at=8257s, mutation_op=CrossoverInsertMutator,QwordAddMutator):
  0000: 06 00 eb ff 30 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....027772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=b96369824ac69302, size=261 bytes, fuzzer=cmplog, trial=1, discovered_at=15404s, mutation_op=ByteFlipMutator):
  0000: 3d 3d 3d 3d 3d 32 37 37 37 32 2d 20 20 20 5c 0a   =====27772-   \.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 3a   .0"?>.<!DOCTYPE:
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=b817581b4b71ba79, size=557 bytes, fuzzer=cmplog, trial=1, discovered_at=29843s, mutation_op=ByteIncMutator):
  0000: 31 32 37 37 37 32 2e 64 73 64 06 00 00 00 31 32   127772.dsd....12
  0010: 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7772.xml\.<?xml 
  0020: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0030: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=028449a3e7659dfa, size=389 bytes, fuzzer=naive, trial=1, discovered_at=4s, mutation_op=BytesDeleteMutator,BitFlipMutator,BytesSwapMutator,TokenInsert,ByteNegMutator,CrossoverInsertMutator):
  0000: 74 64 22 3e 0a 0a 3c 61 3e 0a 20 20 3c 62 20 06   td">..<a>.  <b .
  0010: 00 00 00 31 32 37 37 37 32 4a 78 6d 6c 5c 0a 3c   ...127772Jxml\.<
  0020: 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e   ?xml version="1.
  0030: 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61   0"?>.<!DOCTYPE a
Seed 2 (id=022872fb8319f510, size=611 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=CrossoverInsertMutator,WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=013a786979d45920, size=375 bytes, fuzzer=naive, trial=1, discovered_at=59s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=142a49267be69461, size=368 bytes, fuzzer=naive, trial=1, discovered_at=59s, mutation_op=ByteNegMutator,ByteAddMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 57 37 37 25 2e 78 6d 6c 5c 0a   ....12W77%.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=02f665196242465b, size=328 bytes, fuzzer=naive, trial=1, discovered_at=108s, mutation_op=BytesDeleteMutator,ByteNegMutator,BytesDeleteMutator):
  0000: c9 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   .2.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  32(2)x2 00(.)x2 3d(=)x1 7f(.)x1     00(.)x6 64(d)x1 32(2)x1 22(")x1 +1u  PARTIAL
   0x0005  32(2)x5 6c(l)x1                     32(2)x6 0a(.)x1 6c(l)x1 70(p)x1 +1u  PARTIAL
   0x0006  37(7)x3 5c(\)x1 2e(.)x1 c8(.)x1     37(7)x5 3c(<)x1 57(W)x1 5c(\)x1 +2u  PARTIAL
   0x0007  37(7)x4 0a(.)x1 64(d)x1             37(7)x6 61(a)x1 0a(.)x1 2f(/)x1 +1u  PARTIAL
   0x0008  37(7)x4 3c(<)x1 73(s)x1             37(7)x6 3e(>)x1 3c(<)x1 2f(/)x1 +1u  PARTIAL
   0x0009  32(2)x4 3f(?)x1 64(d)x1             32(2)x5 0a(.)x1 25(%)x1 3f(?)x1 +2u  PARTIAL
   0x000a  2e(.)x3 78(x)x1 2d(-)x1 06(.)x1     2e(.)x6 20( )x1 78(x)x1 62(b)x1 +1u  PARTIAL
   0x000b  78(x)x3 6d(m)x1 20( )x1 00(.)x1     78(x)x6 20( )x1 6d(m)x1 3e(>)x1 +1u  PARTIAL
   0x000c  6d(m)x3 6c(l)x1 20( )x1 00(.)x1     6d(m)x6 3c(<)x1 6c(l)x1 b6(.)x1 +1u  PARTIAL
   0x000d  6c(l)x3 20( )x2 00(.)x1             6c(l)x6 62(b)x1 20( )x1 b6(.)x1 +1u  PARTIAL
   0x000e  5c(\)x4 76(v)x1 31(1)x1             5c(\)x6 20( )x1 76(v)x1 b6(.)x1 +1u  PARTIAL
   0x000f  0a(.)x4 65(e)x1 32(2)x1             0a(.)x6 06(.)x1 65(e)x1 b6(.)x1 +1u  PARTIAL
   0x0010  3c(<)x4 72(r)x1 37(7)x1             3c(<)x6 00(.)x1 72(r)x1 b6(.)x1 +1u  PARTIAL
   0x0011  3f(?)x4 73(s)x1 37(7)x1             3f(?)x6 00(.)x1 73(s)x1 b6(.)x1 +1u  PARTIAL
   0x0012  78(x)x4 69(i)x1 37(7)x1             78(x)x6 00(.)x1 69(i)x1 b6(.)x1 +1u  PARTIAL
   0x0013  6d(m)x4 6f(o)x1 32(2)x1             6d(m)x6 31(1)x1 6f(o)x1 b6(.)x1 +1u  PARTIAL
   0x0014  6c(l)x4 6e(n)x1 2e(.)x1             6c(l)x6 32(2)x1 6e(n)x1 61(a)x1 +1u  PARTIAL
   0x0015  20( )x4 3d(=)x1 78(x)x1             20( )x6 37(7)x1 3d(=)x1 6b(k)x1 +1u  PARTIAL
   0x0016  76(v)x4 22(")x1 6d(m)x1             76(v)x6 37(7)x1 22(")x1 65(e)x1 +1u  PARTIAL
   0x0017  65(e)x4 31(1)x1 6c(l)x1             65(e)x6 37(7)x1 31(1)x1 75(u)x1 +1u  PARTIAL
   0x0018  72(r)x4 2e(.)x1 5c(\)x1             72(r)x6 32(2)x1 2e(.)x1 28(()x1 +1u  PARTIAL
   0x0019  73(s)x4 30(0)x1 0a(.)x1             73(s)x7 4a(J)x1 30(0)x1 39(9)x1     PARTIAL
   0x001a  69(i)x4 22(")x1 3c(<)x1             69(i)x7 78(x)x1 22(")x1 2f(/)x1     PARTIAL
   0x001b  6f(o)x4 3f(?)x2                     6f(o)x6 6d(m)x2 3f(?)x1 78(x)x1     PARTIAL
   0x001c  6e(n)x4 3e(>)x1 78(x)x1             6e(n)x6 6c(l)x2 3e(>)x2             PARTIAL
   0x001d  3d(=)x4 0a(.)x1 6d(m)x1             3d(=)x6 5c(\)x1 0a(.)x1 3e(>)x1 +1u  PARTIAL
   0x001e  22(")x4 3c(<)x1 6c(l)x1             22(")x6 0a(.)x1 3c(<)x1 3e(>)x1 +1u  PARTIAL
   0x001f  31(1)x4 21(!)x1 20( )x1             31(1)x6 3c(<)x1 21(!)x1 3e(>)x1 +1u  PARTIAL
   0x0020  2e(.)x4 44(D)x1 76(v)x1             2e(.)x6 3f(?)x1 44(D)x1 20( )x1 +1u  PARTIAL
   0x0021  30(0)x4 4f(O)x1 65(e)x1             30(0)x6 78(x)x1 4f(O)x1 d6(.)x1 +1u  PARTIAL
   0x0022  22(")x4 43(C)x1 72(r)x1             22(")x6 6d(m)x1 43(C)x1 23(#)x1 +1u  PARTIAL
   0x0023  3f(?)x4 54(T)x1 73(s)x1             3f(?)x6 6c(l)x1 54(T)x1 46(F)x1 +1u  PARTIAL
   0x0024  3e(>)x4 59(Y)x1 69(i)x1             3e(>)x7 20( )x1 59(Y)x1 49(I)x1     PARTIAL
   0x0025  0a(.)x4 50(P)x1 6f(o)x1             0a(.)x6 76(v)x1 50(P)x1 58(X)x1 +1u  PARTIAL
   0x0026  3c(<)x4 45(E)x1 6e(n)x1             3c(<)x6 45(E)x2 65(e)x1 2f(/)x1     PARTIAL
   0x0027  21(!)x4 20( )x1 3d(=)x1             21(!)x6 72(r)x1 20( )x1 44(D)x1 +1u  PARTIAL
   0x0028  44(D)x4 61(a)x1 22(")x1             44(D)x6 73(s)x1 61(a)x1 30(0)x1 +1u  PARTIAL
   0x0029  4f(O)x4 20( )x1 31(1)x1             4f(O)x6 20( )x2 69(i)x1 27(')x1     PARTIAL
   0x002a  43(C)x4 53(S)x1 2e(.)x1             43(C)x6 6f(o)x1 53(S)x1 73(s)x1 +1u  PARTIAL
   0x002b  54(T)x4 59(Y)x1 30(0)x1             54(T)x6 6e(n)x1 59(Y)x1 69(i)x1 +1u  PARTIAL
   ... (20 more divergent offsets)
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6909.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6909,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6909 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6909 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6909 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).