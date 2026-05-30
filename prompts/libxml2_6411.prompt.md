==== BLOCKER ====
Target: libxml2
Branch ID: 6411
Location: /src/libxml2/hash.c:684:9
Enclosing function: xmlHashUpdateEntry3
Source line:     if (table->table[key].valid == 0) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (grimoire_structural vs grimoire)
value_profile                    0       10          0  REFERENCE
value_profile_cmplog             2        8          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                         9        1          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=8.30h  loser=21.60h
  avg hitcount on branch: winner=76  loser=0
  prob_div=0.80  dur_div=13.30h  hit_div=76
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6411/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlHashUpdateEntry3 (/src/libxml2/hash.c:651-757) ---
[ ]   649  xmlHashUpdateEntry3(xmlHashTablePtr table, const xmlChar *name,
[ ]   650  	           const xmlChar *name2, const xmlChar *name3,
[B]   651  		   void *userdata, xmlHashDeallocator f) {
[B]   652      unsigned long key;
[B]   653      xmlHashEntryPtr entry;
[B]   654      xmlHashEntryPtr insert;
[ ]   655  
[B]   656      if ((table == NULL) || name == NULL)
[ ]   657  	return(-1);
[ ]   658  
[ ]   659      /*
[ ]   660       * If using a dict internalize if needed
[ ]   661       */
[B]   662      if (table->dict) {
[B]   663          if (!xmlDictOwns(table->dict, name)) {
[ ]   664  	    name = xmlDictLookup(table->dict, name, -1);
[ ]   665  	    if (name == NULL)
[ ]   666  	        return(-1);
[ ]   667  	}
[B]   668          if ((name2 != NULL) && (!xmlDictOwns(table->dict, name2))) {
[ ]   669  	    name2 = xmlDictLookup(table->dict, name2, -1);
[ ]   670  	    if (name2 == NULL)
[ ]   671  	        return(-1);
[ ]   672  	}
[B]   673          if ((name3 != NULL) && (!xmlDictOwns(table->dict, name3))) {
[ ]   674  	    name3 = xmlDictLookup(table->dict, name3, -1);
[ ]   675  	    if (name3 == NULL)
[ ]   676  	        return(-1);
[ ]   677  	}
[B]   678      }
[ ]   679  
[ ]   680      /*
[ ]   681       * Check for duplicate and insertion location.
[ ]   682       */
[B]   683      key = xmlHashComputeKey(table, name, name2, name3);
[B]   684      if (table->table[key].valid == 0) { <-- BLOCKER
[B]   685  	insert = NULL;
[B]   686      } else {
[W]   687          if (table ->dict) {
[W]   688  	    for (insert = &(table->table[key]); insert->next != NULL;
[W]   689  		 insert = insert->next) {
[ ]   690  		if ((insert->name == name) &&
[ ]   691  		    (insert->name2 == name2) &&
[ ]   692  		    (insert->name3 == name3)) {
[ ]   693  		    if (f)
[ ]   694  			f(insert->payload, insert->name);
[ ]   695  		    insert->payload = userdata;
[ ]   696  		    return(0);
[ ]   697  		}
[ ]   698  	    }
[W]   699  	    if ((insert->name == name) &&
[W]   700  		(insert->name2 == name2) &&
[W]   701  		(insert->name3 == name3)) {
[W]   702  		if (f)
[ ]   703  		    f(insert->payload, insert->name);
[W]   704  		insert->payload = userdata;
[W]   705  		return(0);
[W]   706  	    }
[W]   707  	} else {
[ ]   708  	    for (insert = &(table->table[key]); insert->next != NULL;
[ ]   709  		 insert = insert->next) {
[ ]   710  		if ((xmlStrEqual(insert->name, name)) &&
[ ]   711  		    (xmlStrEqual(insert->name2, name2)) &&
[ ]   712  		    (xmlStrEqual(insert->name3, name3))) {
[ ]   713  		    if (f)
[ ]   714  			f(insert->payload, insert->name);
[ ]   715  		    insert->payload = userdata;
[ ]   716  		    return(0);
[ ]   717  		}
[ ]   718  	    }
[ ]   719  	    if ((xmlStrEqual(insert->name, name)) &&
[ ]   720  		(xmlStrEqual(insert->name2, name2)) &&
[ ]   721  		(xmlStrEqual(insert->name3, name3))) {
[ ]   722  		if (f)
[ ]   723  		    f(insert->payload, insert->name);
[ ]   724  		insert->payload = userdata;
[ ]   725  		return(0);
[ ]   726  	    }
[ ]   727  	}
[W]   728      }
[ ]   729  
[B]   730      if (insert == NULL) {
[B]   731  	entry =  &(table->table[key]);
[B]   732      } else {
[ ]   733  	entry = xmlMalloc(sizeof(xmlHashEntry));
[ ]   734  	if (entry == NULL)
[ ]   735  	     return(-1);
[ ]   736      }
[ ]   737  
[B]   738      if (table->dict != NULL) {
[B]   739          entry->name = (xmlChar *) name;
[B]   740          entry->name2 = (xmlChar *) name2;
[B]   741          entry->name3 = (xmlChar *) name3;
[B]   742      } else {
[ ]   743  	entry->name = xmlStrdup(name);
[ ]   744  	entry->name2 = xmlStrdup(name2);
[ ]   745  	entry->name3 = xmlStrdup(name3);
[ ]   746      }
[B]   747      entry->payload = userdata;
[B]   748      entry->next = NULL;
[B]   749      entry->valid = 1;
[B]   750      table->nbElems++;
[ ]   751  
[ ]   752  
[B]   753      if (insert != NULL) {
[ ]   754  	insert->next = entry;
[ ]   755      }
[B]   756      return(0);
[B]   757  }

--- Caller (1 hop): xmlHashUpdateEntry2 (/src/libxml2/hash.c:449-451, calls xmlHashUpdateEntry3 at line 450) (full body — short) ---
[B]   449  		   xmlHashDeallocator f) {
[B]   450      return(xmlHashUpdateEntry3(table, name, name2, NULL, userdata, f)); <-- CALL
[B]   451  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlHashUpdateEntry  (/src/libxml2/hash.c:428-430, calls xmlHashUpdateEntry3 at line 429)
hop 2  xmlHashUpdateEntry2  (/src/libxml2/hash.c:449-451, calls xmlHashUpdateEntry3 at line 450)
hop 3  parser.c:xmlAddDefAttrs  (/src/libxml2/parser.c:1194-1292, calls xmlHashUpdateEntry2 at line 1238)
hop 3  xmlRemoveRef  (/src/libxml2/valid.c:3157-3201, calls xmlHashUpdateEntry at line 3198)
hop 3  xmlXPathRegisterNs  (/src/libxml2/xpath.c:5132-5149, calls xmlHashUpdateEntry at line 5147)
hop 4  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169, calls parser.c:xmlAddDefAttrs at line 6151)
hop 4  xpointer.c:xmlXPtrEvalXPtrPart  (/src/libxml2/xpointer.c:953-1086, calls xmlXPathRegisterNs at line 1075)
hop 5  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseAttributeListDecl at line 6964)
hop 5  xpointer.c:xmlXPtrEvalFullXPtr  (/src/libxml2/xpointer.c:1116-1174, calls xpointer.c:xmlXPtrEvalXPtrPart at line 1123)
hop 6  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 6  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 6  xpointer.c:xmlXPtrEvalXPointer  (/src/libxml2/xpointer.c:1239-1275, calls xpointer.c:xmlXPtrEvalFullXPtr at line 1264)
hop 7  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 7  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 7  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 7  xmlXPtrEval  (/src/libxml2/xpointer.c:1356-1415, calls xpointer.c:xmlXPtrEvalXPointer at line 1370)
hop 8  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 8  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 8  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)
hop 8  xinclude.c:xmlXIncludeLoadDoc  (/src/libxml2/xinclude.c:1252-1611, calls xmlXPtrEval at line 1429)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0         9  hash.c:stubHashScannerFull  (/src/libxml2/hash.c:847-850)
       0         6  hash.c:xmlHashComputeQKey  (/src/libxml2/hash.c:119-167)
       0         6  xmlHashQLookup2  (/src/libxml2/hash.c:514-516)
       0         6  xmlHashQLookup3  (/src/libxml2/hash.c:818-837)
       0         3  xmlHashScan  (/src/libxml2/hash.c:861-866)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlHashUpdateEntry3  (/src/libxml2/hash.c:651-757) ---
  d=1   L 656  T=0 F=60  T=0 F=30  if ((table == NULL) || name == NULL)
  d=1   L 656  T=0 F=60  T=0 F=30  if ((table == NULL) || name == NULL)
  d=1   L 662  T=60 F=0  T=30 F=0  if (table->dict) {
  d=1   L 663  T=0 F=60  T=0 F=30  if (!xmlDictOwns(table->dict, name)) {
  d=1   L 668  T=0 F=36  T=0 F=0  if ((name2 != NULL) && (!xmlDictOwns(table->dict, name2))) {
  d=1   L 668  T=36 F=24  T=0 F=30  if ((name2 != NULL) && (!xmlDictOwns(table->dict, name2))) {
  d=1   L 673  T=0 F=60  T=0 F=30  if ((name3 != NULL) && (!xmlDictOwns(table->dict, name3))) {
  d=1   L 684  T=30 F=30  T=30 F=0  if (table->table[key].valid == 0) {  <-- BLOCKER
  d=1   L 687  T=30 F=0  T=0 F=0  if (table ->dict) {
  d=1   L 688  T=0 F=30  T=0 F=0  for (insert = &(table->table[key]); insert->next != NULL;
  d=1   L 699  T=30 F=0  T=0 F=0  if ((insert->name == name) &&
  d=1   L 700  T=30 F=0  T=0 F=0  (insert->name2 == name2) &&
  d=1   L 701  T=30 F=0  T=0 F=0  (insert->name3 == name3)) {
  d=1   L 702  T=0 F=30  T=0 F=0  if (f)

[off-chain: 65 additional divergent branches across 7 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=2bc0de3a6d70d34a, size=219 bytes, fuzzer=grimoire, trial=2, discovered_at=15759s, mutation_op=I2SRandReplace):
  0000: 06 00 32 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   ..2l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 5c 0a 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74   \.dtds/127772.dt
Seed 2 (id=1f9b14226825622d, size=235 bytes, fuzzer=grimoire, trial=2, discovered_at=24646s, mutation_op=ByteAddMutator,BytesRandInsertMutator):
  0000: 2d 31 32 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   -12l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 5c 0a 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74   \.dtds/127772.dt
Seed 3 (id=519469c76dc54a97, size=219 bytes, fuzzer=grimoire, trial=2, discovered_at=29220s, mutation_op=ByteRandMutator):
  0000: 06 00 5b 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   ..[l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 5c 0a 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74   \.dtds/127772.dt
Seed 4 (id=1192004ea85383c7, size=231 bytes, fuzzer=grimoire, trial=2, discovered_at=35427s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 32 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   ..2l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 5c 0a 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74   \.dtds/127772.dt
Seed 5 (id=1effa5392a0d2a2b, size=220 bytes, fuzzer=grimoire, trial=2, discovered_at=48138s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 32 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   ..2l\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 5c 0a 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74   \.dtds/127772.dt

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0be939129cb3ca8a, size=377 bytes, fuzzer=cmplog, trial=1, discovered_at=3s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=1ae4076072a04432, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=91s, mutation_op=WordAddMutator,BytesSwapMutator,BytesCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=0d5f26ea8b67d379, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=93s, mutation_op=DwordInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=01986dbadd87a561, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=128s, mutation_op=ByteDecMutator,CrossoverReplaceMutator,BytesRandInsertMutator,ByteAddMutator,ByteAddMutator,CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=273e1a1b133aabea, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=229s, mutation_op=BytesSwapMutator,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 09 20 76 65 72 73 69 27 0a 20 20 20   <?xm. versi'.   
  0020: 20 20 20 6f 22 3d 22 31 2e 30 22 3f 3e 0a 3c 21      o"="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  2d(-)x5 06(.)x4 14(.)x1             06(.)x8 3d(=)x1 2b(+)x1             PARTIAL
   0x0001  00(.)x5 2d(-)x4 31(1)x1             00(.)x9 3d(=)x1                     PARTIAL
   0x0002  32(2)x6 5b([)x1 3b(;)x1 ce(.)x1 +1u  00(.)x9 3d(=)x1                     DIFFER
   0x0003  6c(l)x10                            00(.)x9 3d(=)x1                     DIFFER
   0x0004  5c(\)x10                            31(1)x9 3d(=)x1                     DIFFER
   0x0005  0a(.)x10                            32(2)x10                            DIFFER
   0x0006  3c(<)x10                            37(7)x10                            DIFFER
   0x0007  3f(?)x10                            37(7)x10                            DIFFER
   0x0008  6c(l)x10                            37(7)x10                            DIFFER
   0x0009  20( )x10                            32(2)x10                            DIFFER
   0x000a  3f(?)x10                            2e(.)x10                            DIFFER
   0x000b  3e(>)x10                            78(x)x9 20( )x1                     DIFFER
   0x000c  3c(<)x10                            6d(m)x9 20( )x1                     DIFFER
   0x000d  21(!)x10                            6c(l)x9 20( )x1                     DIFFER
   0x000e  44(D)x10                            5c(\)x10                            DIFFER
   0x000f  4f(O)x10                            0a(.)x10                            DIFFER
   0x0010  43(C)x10                            3c(<)x10                            DIFFER
   0x0011  54(T)x10                            3f(?)x10                            DIFFER
   0x0012  59(Y)x10                            78(x)x10                            DIFFER
   0x0013  50(P)x10                            6d(m)x10                            DIFFER
   0x0014  45(E)x10                            6c(l)x9 09(.)x1                     DIFFER
   0x0015  61(a)x9 7a(z)x1                     20( )x10                            DIFFER
   0x0016  20( )x10                            76(v)x10                            DIFFER
   0x0017  53(S)x10                            65(e)x10                            DIFFER
   0x0018  59(Y)x10                            72(r)x10                            DIFFER
   0x0019  53(S)x10                            73(s)x10                            DIFFER
   0x001a  54(T)x10                            69(i)x10                            DIFFER
   0x001b  45(E)x10                            6f(o)x9 27(')x1                     DIFFER
   0x001c  4d(M)x10                            6e(n)x9 0a(.)x1                     DIFFER
   0x001d  20( )x10                            3d(=)x9 20( )x1                     PARTIAL
   0x001e  22(")x10                            22(")x9 20( )x1                     PARTIAL
   0x001f  64(d)x10                            31(1)x9 20( )x1                     DIFFER
   0x0020  74(t)x10                            2e(.)x9 20( )x1                     DIFFER
   0x0021  64(d)x10                            30(0)x9 20( )x1                     DIFFER
   0x0022  73(s)x10                            22(")x9 20( )x1                     DIFFER
   0x0023  2f(/)x10                            3f(?)x9 6f(o)x1                     DIFFER
   0x0024  31(1)x10                            3e(>)x9 22(")x1                     DIFFER
   0x0025  32(2)x10                            0a(.)x9 3d(=)x1                     DIFFER
   0x0026  37(7)x10                            3c(<)x9 22(")x1                     DIFFER
   0x0027  37(7)x10                            21(!)x9 31(1)x1                     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6411.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6411,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6411 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6411 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6411 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).