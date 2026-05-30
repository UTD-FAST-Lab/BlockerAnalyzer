==== BLOCKER ====
Target: libxml2
Branch ID: 6414
Location: /src/libxml2/hash.c:787:3
Enclosing function: xmlHashLookup3
Source line: 		(entry->name3 == name3))
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (calibrated_energy vs minimizer)
cmplog                           2        8          0  loser (grimoire_structural vs grimoire); loser (value_profile vs value_profile_cmplog)
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog); winner (I2S vs value_profile)
naive_ctx                        5        5          0  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        9        1          0  winner (calibrated_energy vs naive); winner (aflfast_rarity vs fast)
fast                             2        8          0  loser (aflfast_rarity vs minimizer)
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'fast', 'grimoire', 'minimizer', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt']

==== DECISIVE PAIRS (5) ====
--- Pair 1: minimizer > naive  [delta: calibrated_energy] ---
  subject 38  (minimizer vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.10h  loser=22.60h
  avg hitcount on branch: winner=36  loser=0
  prob_div=0.90  dur_div=12.50h  hit_div=36
  subject-level: delta_AUC=20906460.0  p_AUC=0.1041  delta_Final=371.4  p_final=0.0046
--- Pair 2: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=5.50h  loser=20.20h
  avg hitcount on branch: winner=1004  loser=2
  prob_div=0.80  dur_div=14.70h  hit_div=1002
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002
--- Pair 3: minimizer > fast  [delta: aflfast_rarity] ---
  subject 39  (fast vs minimizer, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=10.10h  loser=19.70h
  avg hitcount on branch: winner=36  loser=11
  prob_div=0.70  dur_div=9.60h  hit_div=24
  subject-level: delta_AUC=-20200320.0  p_AUC=0.0376  delta_Final=-295.1  p_final=0.0452
--- Pair 4: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.80h  loser=20.20h
  avg hitcount on branch: winner=10  loser=2
  prob_div=0.60  dur_div=8.40h  hit_div=8
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 5: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.80h  loser=19.00h
  avg hitcount on branch: winner=10  loser=2
  prob_div=0.60  dur_div=7.20h  hit_div=8
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6414/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlHashLookup3 (/src/libxml2/hash.c:772-798) ---
[ ]   770  void *
[ ]   771  xmlHashLookup3(xmlHashTablePtr table, const xmlChar *name,
[B]   772  	       const xmlChar *name2, const xmlChar *name3) {
[B]   773      unsigned long key;
[B]   774      xmlHashEntryPtr entry;
[ ]   775  
[B]   776      if (table == NULL)
[B]   777  	return(NULL);
[B]   778      if (name == NULL)
[ ]   779  	return(NULL);
[B]   780      key = xmlHashComputeKey(table, name, name2, name3);
[B]   781      if (table->table[key].valid == 0)
[B]   782  	return(NULL);
[B]   783      if (table->dict) {
[B]   784  	for (entry = &(table->table[key]); entry != NULL; entry = entry->next) {
[B]   785  	    if ((entry->name == name) &&
[B]   786  		(entry->name2 == name2) &&
[B]   787  		(entry->name3 == name3)) <-- BLOCKER
[B]   788  		return(entry->payload);
[B]   789  	}
[B]   790      }
[B]   791      for (entry = &(table->table[key]); entry != NULL; entry = entry->next) {
[B]   792  	if ((xmlStrEqual(entry->name, name)) &&
[B]   793  	    (xmlStrEqual(entry->name2, name2)) &&
[B]   794  	    (xmlStrEqual(entry->name3, name3)))
[B]   795  	    return(entry->payload);
[B]   796      }
[B]   797      return(NULL);
[B]   798  }

--- Caller (1 hop): xmlHashLookup2 (/src/libxml2/hash.c:479-481, calls xmlHashLookup3 at line 480) (full body — short) ---
[B]   479  	      const xmlChar *name2) {
[B]   480      return(xmlHashLookup3(table, name, name2, NULL)); <-- CALL
[B]   481  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlHashLookup  (/src/libxml2/hash.c:463-465, calls xmlHashLookup3 at line 464)
hop 2  xmlHashLookup2  (/src/libxml2/hash.c:479-481, calls xmlHashLookup3 at line 480)
hop 3  entities.c:xmlGetEntityFromTable  (/src/libxml2/entities.c:471-473, calls xmlHashLookup at line 472)
hop 3  xmlFuzzReadEntities  (/src/libxml2/fuzz/fuzz.c:199-230, calls xmlHashLookup at line 213)
hop 3  parser.c:xmlAddDefAttrs  (/src/libxml2/parser.c:1194-1292, calls xmlHashLookup2 at line 1204)
hop 4  xmlGetParameterEntity  (/src/libxml2/entities.c:486-503, calls entities.c:xmlGetEntityFromTable at line 494)
hop 4  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlFuzzReadEntities at line 42)
hop 4  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169, calls parser.c:xmlAddDefAttrs at line 6151)
hop 5  xmlSAX2GetParameterEntity  (/src/libxml2/SAX2.c:601-613, calls xmlGetParameterEntity at line 611)
hop 5  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseAttributeListDecl at line 6964)
hop 6  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 6  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 7  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 7  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 7  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 8  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 8  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 8  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     179      1440  hash.c:xmlHashComputeKey  (/src/libxml2/hash.c:84-110)
     149      1010  xmlHashLookup3  (/src/libxml2/hash.c:772-798)  <-- enclosing
      76       786  xmlHashLookup2  (/src/libxml2/hash.c:479-481)
      36       436  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      36       434  xmlHashAddEntry3  (/src/libxml2/hash.c:535-631)
      12       269  xmlHashAddEntry2  (/src/libxml2/hash.c:409-411)
      21       263  xmlHashCreate  (/src/libxml2/hash.c:178-200)
      21       263  xmlHashFree  (/src/libxml2/hash.c:324-365)
      18       239  xmlHashCreateDict  (/src/libxml2/hash.c:212-221)
      12       142  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
       6       136  xmlAddElementDecl  (/src/libxml2/valid.c:1414-1620)
      18       145  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)
      12       139  valid.c:xmlFreeElement  (/src/libxml2/valid.c:1382-1395)
      12       139  valid.c:xmlFreeElementTableEntry  (/src/libxml2/valid.c:1623-1625)
      15       122  xmlHashLookup  (/src/libxml2/hash.c:463-465)
... (48 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlHashLookup3  (/src/libxml2/hash.c:772-798) ---
  d=1   L 776  T=6 F=143  T=136 F=880  if (table == NULL)
  d=1   L 778  T=0 F=143  T=0 F=880  if (name == NULL)
  d=1   L 781  T=44 F=99  T=463 F=417  if (table->table[key].valid == 0)
  d=1   L 783  T=89 F=10  T=323 F=94  if (table->dict) {
  d=1   L 784  T=89 F=77  T=333 F=141  for (entry = &(table->table[key]); entry != NULL; entry =...
  d=1   L 785  T=38 F=51  T=203 F=130  if ((entry->name == name) &&
  d=1   L 786  T=38 F=0  T=193 F=10  (entry->name2 == name2) &&
  d=1   L 787  T=12 F=26  T=182 F=11  (entry->name3 == name3))  <-- BLOCKER
  d=1   L 791  T=90 F=1  T=248 F=19  for (entry = &(table->table[key]); entry != NULL; entry =...
  d=1   L 792  T=86 F=4  T=226 F=22  if ((xmlStrEqual(entry->name, name)) &&
  d=1   L 793  T=86 F=0  T=216 F=10  (xmlStrEqual(entry->name2, name2)) &&
  d=1   L 794  T=86 F=0  T=216 F=0  (xmlStrEqual(entry->name3, name3)))

[off-chain: 532 additional divergent branches across 51 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=b3f5d62fb26f5823, size=214 bytes, fuzzer=grimoire, trial=1, discovered_at=8398s, mutation_op=I2SRandReplace):
  0000: 2f 2f 2f 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   ///l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 3c 61 3e 3c 62 20 78 6c 69 6e 6b 3d 22 22 3e 3c   <a><b xlink=""><
Seed 2 (id=105610b4c7cd98fb, size=468 bytes, fuzzer=grimoire, trial=1, discovered_at=15035s, mutation_op=WordInterestingMutator):
  0000: a9 aa aa aa aa aa aa 0a 5a ae ff ff ff 15 a9 05   ........Z.......
  0010: 00 01 01 00 30 88 02 02 3e 42 0f 00 06 00 00 00   ....0...>B......
  0020: 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   127772.xml\.<?xm
  0030: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
Seed 3 (id=2f5c033439b53a6d, size=207 bytes, fuzzer=grimoire, trial=1, discovered_at=80059s, mutation_op=WordAddMutator):
  0000: e9 eb fe ff ff ff ff ff 06 31 6d 6c 5c 0a 3c 3f   .........1ml\.<?
  0010: 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20 53   l ?><!DOCTYPEa S
  0020: 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37   YSTEM "dtds/1277
  0030: 37 32 2e 64 74 64 22 3e 3c 61 3e 3c 62 3c 62 3c   72.dtd"><a><b<b<

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=43903e30ba267c1e, size=521 bytes, fuzzer=fast, trial=1):
  0000: 2f 6e 65 65 65 6d 60 22 3e 62 20 74 06 ff 00 00   /neeem`">b t....
  0010: 31 32 37 5c 0a 3c 3f 6d 6c 20 76 65 72 73 69 6f   127\.<?ml versio
  0020: 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54   n="1.0"?>.<!DOCT
  0030: 59 50 45 20 61 20 53 59 53 54 45 4d 20 22 64 74   YPE a SYSTEM "dt
Seed 2 (id=8e0c19a9dc274a9a, size=369 bytes, fuzzer=fast, trial=1):
  0000: 38 aa aa aa aa aa aa aa aa 32 2e 78 6d 6c 5c 0a   8........2.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=b65221764c18d15e, size=652 bytes, fuzzer=fast, trial=1):
  0000: ff 64 ff 65 65 65 65 3a 2f 6e 65 65 65 6d 60 22   .d.eeee:/neeem`"
  0010: 3e 62 20 74 06 ff 00 00 31 32 37 5c 0a 3c 3f 6d   >b t....127\.<?m
  0020: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0030: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
Seed 4 (id=e7821580957cb5e4, size=781 bytes, fuzzer=fast, trial=1):
  0000: 2d 2d a7 a7 a7 a7 a7 a7 aa aa aa aa aa aa aa 8c   --..............
  0010: aa 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   .2.xml\.<?xml ve
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
Seed 5 (id=0be939129cb3ca8a, size=377 bytes, fuzzer=cmplog, trial=1, discovered_at=3s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  2f(/)x1 a9(.)x1 e9(.)x1             06(.)x14 2f(/)x1 38(8)x1 ff(.)x1 +7u  PARTIAL
   0x0001  2f(/)x1 aa(.)x1 eb(.)x1             00(.)x17 6e(n)x1 aa(.)x1 64(d)x1 +4u  PARTIAL
   0x0002  2f(/)x1 aa(.)x1 fe(.)x1             00(.)x17 65(e)x1 aa(.)x1 ff(.)x1 +4u  PARTIAL
   0x0003  6c(l)x1 aa(.)x1 ff(.)x1             00(.)x17 65(e)x2 aa(.)x1 a7(.)x1 +3u  PARTIAL
   0x0004  5c(\)x1 aa(.)x1 ff(.)x1             31(1)x17 65(e)x2 aa(.)x1 a7(.)x1 +3u  PARTIAL
   0x0005  0a(.)x1 aa(.)x1 ff(.)x1             32(2)x18 6d(m)x1 aa(.)x1 65(e)x1 +3u  PARTIAL
   0x0006  3c(<)x1 aa(.)x1 ff(.)x1             37(7)x18 60(`)x1 aa(.)x1 65(e)x1 +3u  PARTIAL
   0x0007  3f(?)x1 0a(.)x1 ff(.)x1             37(7)x19 22(")x1 aa(.)x1 3a(:)x1 +2u  DIFFER
   0x0008  6c(l)x1 5a(Z)x1 06(.)x1             37(7)x18 aa(.)x2 3e(>)x1 2f(/)x1 +2u  DIFFER
   0x0009  20( )x1 ae(.)x1 31(1)x1             32(2)x18 62(b)x1 6e(n)x1 aa(.)x1 +3u  DIFFER
   0x000a  3f(?)x1 ff(.)x1 6d(m)x1             2e(.)x19 20( )x1 65(e)x1 aa(.)x1 +2u  DIFFER
   0x000b  3e(>)x1 ff(.)x1 6c(l)x1             78(x)x18 74(t)x1 65(e)x1 aa(.)x1 +3u  DIFFER
   0x000c  3c(<)x1 ff(.)x1 5c(\)x1             6d(m)x18 06(.)x1 65(e)x1 aa(.)x1 +3u  DIFFER
   0x000d  21(!)x1 15(.)x1 0a(.)x1             6c(l)x19 ff(.)x1 6d(m)x1 aa(.)x1 +2u  DIFFER
   0x000e  44(D)x1 a9(.)x1 3c(<)x1             5c(\)x20 00(.)x1 60(`)x1 aa(.)x1 +1u  DIFFER
   0x000f  4f(O)x1 05(.)x1 3f(?)x1             0a(.)x20 00(.)x1 22(")x1 8c(.)x1 +1u  DIFFER
   0x0010  43(C)x1 00(.)x1 6c(l)x1             3c(<)x20 31(1)x1 3e(>)x1 aa(.)x1 +1u  DIFFER
   0x0011  54(T)x1 01(.)x1 20( )x1             3f(?)x20 32(2)x2 62(b)x1 20( )x1    PARTIAL
   0x0012  59(Y)x1 01(.)x1 3f(?)x1             78(x)x20 20( )x2 37(7)x1 2e(.)x1    DIFFER
   0x0013  50(P)x1 00(.)x1 3e(>)x1             6d(m)x20 5c(\)x1 74(t)x1 78(x)x1 +1u  DIFFER
   0x0014  45(E)x1 30(0)x1 3c(<)x1             6c(l)x19 0a(.)x1 06(.)x1 6d(m)x1 +2u  DIFFER
   0x0015  61(a)x1 88(.)x1 21(!)x1             20( )x20 3c(<)x1 ff(.)x1 6c(l)x1 +1u  DIFFER
   0x0016  20( )x1 02(.)x1 44(D)x1             76(v)x20 3f(?)x1 00(.)x1 5c(\)x1 +1u  DIFFER
   0x0017  53(S)x1 02(.)x1 4f(O)x1             65(e)x20 6d(m)x1 00(.)x1 0a(.)x1 +1u  DIFFER
   0x0018  59(Y)x1 3e(>)x1 43(C)x1             72(r)x20 6c(l)x1 31(1)x1 3c(<)x1 +1u  DIFFER
   0x0019  53(S)x1 42(B)x1 54(T)x1             73(s)x20 20( )x1 32(2)x1 3f(?)x1 +1u  DIFFER
   0x001a  54(T)x1 0f(.)x1 59(Y)x1             69(i)x20 76(v)x1 37(7)x1 78(x)x1 +1u  DIFFER
   0x001b  45(E)x1 00(.)x1 50(P)x1             6f(o)x19 65(e)x1 5c(\)x1 6d(m)x1 +2u  DIFFER
   0x001c  4d(M)x1 06(.)x1 45(E)x1             6e(n)x19 0a(.)x2 72(r)x1 6c(l)x1 +1u  DIFFER
   0x001d  20( )x1 00(.)x1 61(a)x1             3d(=)x19 20( )x2 73(s)x1 3c(<)x1 +1u  PARTIAL
   0x001e  22(")x1 00(.)x1 20( )x1             22(")x19 69(i)x1 3f(?)x1 76(v)x1 +2u  PARTIAL
   0x001f  64(d)x1 00(.)x1 53(S)x1             31(1)x19 6f(o)x1 6d(m)x1 65(e)x1 +2u  DIFFER
   0x0020  74(t)x1 31(1)x1 59(Y)x1             2e(.)x19 6e(n)x1 6c(l)x1 72(r)x1 +2u  DIFFER
   0x0021  64(d)x1 32(2)x1 53(S)x1             30(0)x19 20( )x2 3d(=)x1 73(s)x1 +1u  DIFFER
   0x0022  73(s)x1 37(7)x1 54(T)x1             22(")x20 76(v)x1 69(i)x1 20( )x1 +1u  DIFFER
   0x0023  2f(/)x1 37(7)x1 45(E)x1             3f(?)x19 6f(o)x2 31(1)x1 65(e)x1 +1u  DIFFER
   0x0024  31(1)x1 37(7)x1 4d(M)x1             3e(>)x19 2e(.)x1 72(r)x1 6e(n)x1 +2u  DIFFER
   0x0025  32(2)x2 20( )x1                     0a(.)x19 3d(=)x2 30(0)x1 73(s)x1 +1u  DIFFER
   0x0026  37(7)x1 2e(.)x1 22(")x1             3c(<)x19 22(")x3 69(i)x1 4c(L)x1    PARTIAL
   0x0027  37(7)x1 78(x)x1 64(d)x1             21(!)x19 31(1)x2 3f(?)x1 6f(o)x1 +1u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6414.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6414,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [minimizer>naive (calibrated_energy), grimoire>cmplog (grimoire_structural), minimizer>fast (aflfast_rarity), value_profile_cmplog>cmplog (value_profile), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6414 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6414 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6414 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).