==== BLOCKER ====
Target: libxml2
Branch ID: 6405
Location: /src/libxml2/hash.c:580:10
Enclosing function: xmlHashAddEntry3
Source line: 	    if ((insert->name == name) &&
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ctx_coverage vs naive_ctx); loser (value_profile vs value_profile); loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    9        1          0  winner (value_profile vs naive)
value_profile_cmplog             9        1          0  REFERENCE
naive_ctx                        9        0          1  winner (ctx_coverage vs naive)
naive_ngram4                     1        9          0  REFERENCE
mopt                             1        7          2  REFERENCE
minimizer                        6        4          0  REFERENCE
fast                             3        4          3  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'naive_ctx', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (3) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=9/10  blocked=0  unreached=1
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.11h  loser=16.90h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.80  dur_div=9.79h  hit_div=2
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001
--- Pair 2: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.60h  loser=16.90h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.70  dur_div=12.30h  hit_div=2
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002
--- Pair 3: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=5.40h  loser=16.90h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.60  dur_div=11.50h  hit_div=1
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6405/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlHashAddEntry3 (/src/libxml2/hash.c:535-631) ---
[ ]   533  xmlHashAddEntry3(xmlHashTablePtr table, const xmlChar *name,
[ ]   534  	         const xmlChar *name2, const xmlChar *name3,
[B]   535  		 void *userdata) {
[B]   536      unsigned long key, len = 0;
[B]   537      xmlHashEntryPtr entry;
[B]   538      xmlHashEntryPtr insert;
[ ]   539  
[B]   540      if ((table == NULL) || (name == NULL))
[ ]   541  	return(-1);
[ ]   542  
[ ]   543      /*
[ ]   544       * If using a dict internalize if needed
[ ]   545       */
[B]   546      if (table->dict) {
[B]   547          if (!xmlDictOwns(table->dict, name)) {
[ ]   548  	    name = xmlDictLookup(table->dict, name, -1);
[ ]   549  	    if (name == NULL)
[ ]   550  	        return(-1);
[ ]   551  	}
[B]   552          if ((name2 != NULL) && (!xmlDictOwns(table->dict, name2))) {
[ ]   553  	    name2 = xmlDictLookup(table->dict, name2, -1);
[ ]   554  	    if (name2 == NULL)
[ ]   555  	        return(-1);
[ ]   556  	}
[B]   557          if ((name3 != NULL) && (!xmlDictOwns(table->dict, name3))) {
[ ]   558  	    name3 = xmlDictLookup(table->dict, name3, -1);
[ ]   559  	    if (name3 == NULL)
[ ]   560  	        return(-1);
[ ]   561  	}
[B]   562      }
[ ]   563  
[ ]   564      /*
[ ]   565       * Check for duplicate and insertion location.
[ ]   566       */
[B]   567      key = xmlHashComputeKey(table, name, name2, name3);
[B]   568      if (table->table[key].valid == 0) {
[B]   569  	insert = NULL;
[B]   570      } else {
[B]   571          if (table->dict) {
[B]   572  	    for (insert = &(table->table[key]); insert->next != NULL;
[B]   573  		 insert = insert->next) {
[ ]   574  		if ((insert->name == name) &&
[ ]   575  		    (insert->name2 == name2) &&
[ ]   576  		    (insert->name3 == name3))
[ ]   577  		    return(-1);
[ ]   578  		len++;
[ ]   579  	    }
[B]   580  	    if ((insert->name == name) && <-- BLOCKER
[B]   581  		(insert->name2 == name2) &&
[B]   582  		(insert->name3 == name3))
[ ]   583  		return(-1);
[B]   584  	} else {
[L]   585  	    for (insert = &(table->table[key]); insert->next != NULL;
[L]   586  		 insert = insert->next) {
[ ]   587  		if ((xmlStrEqual(insert->name, name)) &&
[ ]   588  		    (xmlStrEqual(insert->name2, name2)) &&
[ ]   589  		    (xmlStrEqual(insert->name3, name3)))
[ ]   590  		    return(-1);
[ ]   591  		len++;
[ ]   592  	    }
[L]   593  	    if ((xmlStrEqual(insert->name, name)) &&
[L]   594  		(xmlStrEqual(insert->name2, name2)) &&
[L]   595  		(xmlStrEqual(insert->name3, name3)))
[ ]   596  		return(-1);
[L]   597  	}
[B]   598      }
[ ]   599  
[B]   600      if (insert == NULL) {
[B]   601  	entry = &(table->table[key]);
[B]   602      } else {
[B]   603  	entry = xmlMalloc(sizeof(xmlHashEntry));
[B]   604  	if (entry == NULL)
[ ]   605  	     return(-1);
[B]   606      }
[ ]   607  
[B]   608      if (table->dict != NULL) {
[B]   609          entry->name = (xmlChar *) name;
[B]   610          entry->name2 = (xmlChar *) name2;
[B]   611          entry->name3 = (xmlChar *) name3;
[B]   612      } else {
[B]   613  	entry->name = xmlStrdup(name);
[B]   614  	entry->name2 = xmlStrdup(name2);
[B]   615  	entry->name3 = xmlStrdup(name3);
[B]   616      }
[B]   617      entry->payload = userdata;
[B]   618      entry->next = NULL;
[B]   619      entry->valid = 1;
[ ]   620  
[ ]   621  
[B]   622      if (insert != NULL)
[B]   623  	insert->next = entry;
[ ]   624  
[B]   625      table->nbElems++;
[ ]   626  
[B]   627      if (len > MAX_HASH_LEN)
[ ]   628  	xmlHashGrow(table, MAX_HASH_LEN * table->size);
[ ]   629  
[B]   630      return(0);
[B]   631  }

--- Caller (1 hop): xmlHashAddEntry2 (/src/libxml2/hash.c:409-411, calls xmlHashAddEntry3 at line 410) (full body — short) ---
[B]   409  	        const xmlChar *name2, void *userdata) {
[B]   410      return(xmlHashAddEntry3(table, name, name2, NULL, userdata)); <-- CALL
[B]   411  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlHashAddEntry  (/src/libxml2/hash.c:391-393, calls xmlHashAddEntry3 at line 392)
hop 2  xmlHashAddEntry2  (/src/libxml2/hash.c:409-411, calls xmlHashAddEntry3 at line 410)
hop 3  entities.c:xmlAddEntity  (/src/libxml2/entities.c:203-285, calls xmlHashAddEntry at line 277)
hop 3  xmlFuzzReadEntities  (/src/libxml2/fuzz/fuzz.c:199-230, calls xmlHashAddEntry at line 220)
hop 3  parser.c:xmlAddSpecialAttr  (/src/libxml2/parser.c:1308-1325, calls xmlHashAddEntry2 at line 1318)
hop 3  relaxng.c:xmlRelaxNGCheckChoiceDeterminism  (/src/libxml2/relaxng.c:4113-4237, calls xmlHashAddEntry2 at line 4171)
hop 4  xmlAddDocEntity  (/src/libxml2/entities.c:388-419, calls entities.c:xmlAddEntity at line 403)
hop 4  xmlAddDtdEntity  (/src/libxml2/entities.c:339-370, calls entities.c:xmlAddEntity at line 354)
hop 4  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlFuzzReadEntities at line 42)
hop 4  xmlParseAttributeListDecl  (/src/libxml2/parser.c:6059-6169, calls parser.c:xmlAddSpecialAttr at line 6154)
hop 4  relaxng.c:xmlRelaxNGCheckRules  (/src/libxml2/relaxng.c:6284-6595, calls relaxng.c:xmlRelaxNGCheckChoiceDeterminism at line 6562)
hop 5  xmlSAX2EntityDecl  (/src/libxml2/SAX2.c:630-683, calls xmlAddDtdEntity at line 660)
hop 5  xmlSAX2UnparsedEntityDecl  (/src/libxml2/SAX2.c:876-930, calls xmlAddDtdEntity at line 906)
hop 5  xmlNewEntity  (/src/libxml2/entities.c:441-457, calls xmlAddDocEntity at line 446)
hop 5  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseAttributeListDecl at line 6964)
hop 5  relaxng.c:xmlRelaxNGParseDocument  (/src/libxml2/relaxng.c:6682-6751, calls relaxng.c:xmlRelaxNGCheckRules at line 6740)
hop 6  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 6  xmlParseEntityDecl  (/src/libxml2/parser.c:5476-5721, calls xmlSAX2EntityDecl at line 5598)
hop 6  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 6  relaxng.c:xmlRelaxNGProcessExternalRef  (/src/libxml2/relaxng.c:4760-4833, calls relaxng.c:xmlRelaxNGParseDocument at line 4812)
hop 6  xmlRelaxNGParse  (/src/libxml2/relaxng.c:7514-7638, calls relaxng.c:xmlRelaxNGParseDocument at line 7577)
hop 7  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 7  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 7  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 7  relaxng.c:xmlRelaxNGParsePattern  (/src/libxml2/relaxng.c:4847-5133, calls relaxng.c:xmlRelaxNGProcessExternalRef at line 5007)
hop 7  xmlreader.c:xmlTextReaderRelaxNGValidateInternal  (/src/libxml2/xmlreader.c:4277-4359, calls xmlRelaxNGParse at line 4323)
hop 8  xmlParseDTD  (/src/libxml2/parser.c:12762-12764, calls xmlSAXParseDTD at line 12763)
hop 8  xmlParseDocTypeDecl  (/src/libxml2/parser.c:8380-8440, calls parser.c:xmlParseInternalSubset at line 8428)
hop 8  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls parser.c:xmlParseInternalSubset at line 10909)
hop 8  relaxng.c:xmlRelaxNGParseData  (/src/libxml2/relaxng.c:3635-3782, calls relaxng.c:xmlRelaxNGParsePattern at line 3759)
hop 8  relaxng.c:xmlRelaxNGParseInterleave  (/src/libxml2/relaxng.c:4510-4559, calls relaxng.c:xmlRelaxNGParsePattern at line 4544)
hop 8  xmlTextReaderRelaxNGValidate  (/src/libxml2/xmlreader.c:4555-4557, calls xmlreader.c:xmlTextReaderRelaxNGValidateInternal at line 4556)
hop 8  xmlTextReaderRelaxNGValidateCtxt  (/src/libxml2/xmlreader.c:4537-4539, calls xmlreader.c:xmlTextReaderRelaxNGValidateInternal at line 4538)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      79      1100  hash.c:xmlHashComputeKey  (/src/libxml2/hash.c:84-110)
      50       712  xmlHashLookup3  (/src/libxml2/hash.c:772-798)
      45       615  xmlHashLookup2  (/src/libxml2/hash.c:479-481)
      26       334  xmlHashAddEntry3  (/src/libxml2/hash.c:535-631)  <-- enclosing
      24       294  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      15       222  xmlHashAddEntry2  (/src/libxml2/hash.c:409-411)
      13       188  xmlHashCreate  (/src/libxml2/hash.c:178-200)
      13       188  xmlHashFree  (/src/libxml2/hash.c:324-365)
      12       171  xmlHashCreateDict  (/src/libxml2/hash.c:212-221)
       6        99  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
       6        99  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)
       5        85  xmlHashDefaultDeallocator  (/src/libxml2/hash.c:375-377)
       5        85  xmlHashLookup  (/src/libxml2/hash.c:463-465)
       6        86  xmlHashRemoveEntry2  (/src/libxml2/hash.c:1074-1076)
       6        86  xmlHashRemoveEntry3  (/src/libxml2/hash.c:1094-1140)
... (40 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlHashAddEntry3  (/src/libxml2/hash.c:535-631) ---
  d=1   L 540  T=0 F=26  T=0 F=334  if ((table == NULL) || (name == NULL))
  d=1   L 540  T=0 F=26  T=0 F=334  if ((table == NULL) || (name == NULL))
  d=1   L 546  T=24 F=2  T=273 F=61  if (table->dict) {
  d=1   L 547  T=0 F=24  T=0 F=273  if (!xmlDictOwns(table->dict, name)) {
  d=1   L 552  T=0 F=18  T=0 F=204  if ((name2 != NULL) && (!xmlDictOwns(table->dict, name2))) {
  d=1   L 552  T=18 F=6  T=204 F=69  if ((name2 != NULL) && (!xmlDictOwns(table->dict, name2))) {
  d=1   L 557  T=0 F=9  T=0 F=63  if ((name3 != NULL) && (!xmlDictOwns(table->dict, name3))) {
  d=1   L 557  T=9 F=15  T=63 F=210  if ((name3 != NULL) && (!xmlDictOwns(table->dict, name3))) {
  d=1   L 568  T=25 F=1  T=322 F=12  if (table->table[key].valid == 0) {
  d=1   L 571  T=1 F=0  T=9 F=3  if (table->dict) {
  d=1   L 572  T=0 F=1  T=0 F=9  for (insert = &(table->table[key]); insert->next != NULL;
  d=1   L 580  T=1 F=0  T=9 F=0  if ((insert->name == name) &&  <-- BLOCKER
  d=1   L 581  T=0 F=1  T=0 F=9  (insert->name2 == name2) &&
  d=1   L 585  T=0 F=0  T=0 F=3  for (insert = &(table->table[key]); insert->next != NULL;
  d=1   L 593  T=0 F=0  T=0 F=3  if ((xmlStrEqual(insert->name, name)) &&
  d=1   L 600  T=25 F=1  T=322 F=12  if (insert == NULL) {
  d=1   L 604  T=0 F=1  T=0 F=12  if (entry == NULL)
  d=1   L 608  T=24 F=2  T=273 F=61  if (table->dict != NULL) {
  d=1   L 622  T=1 F=25  T=12 F=322  if (insert != NULL)
  d=1   L 627  T=0 F=26  T=0 F=334  if (len > MAX_HASH_LEN)

[off-chain: 407 additional divergent branches across 40 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=baca9f1cf32b3884, size=324 bytes, fuzzer=cmplog, trial=3, discovered_at=93s, mutation_op=ByteFlipMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0973ec6dd6e8f9d9, size=368 bytes, fuzzer=naive, trial=2, discovered_at=0s, mutation_op=ByteAddMutator):
  0000: 06 00 00 00 31 4a 37 37 37 32 2e 78 6d 6c 5c 0a   ....1J7772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=151e7a5b22369cfc, size=368 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=DwordInterestingMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=f200874c1db79335, size=368 bytes, fuzzer=naive, trial=2, discovered_at=2s, mutation_op=WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 77 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?wml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=d8d50c5c972bbc97, size=376 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=ByteIncMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=491e10d6ee916429, size=368 bytes, fuzzer=naive, trial=2, discovered_at=38s, mutation_op=BytesSetMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x1                             06(.)x13 32(2)x2 fa(.)x1 6c(l)x1    PARTIAL
   0x0001  00(.)x1                             00(.)x14 d1(.)x2 6c(l)x1            PARTIAL
   0x0002  00(.)x1                             00(.)x13 78(x)x2 6c(l)x1 fe(.)x1    PARTIAL
   0x0003  00(.)x1                             00(.)x13 6d(m)x2 6c(l)x1 ff(.)x1    PARTIAL
   0x0004  31(1)x1                             31(1)x13 6c(l)x3 ff(.)x1            PARTIAL
   0x0005  32(2)x1                             32(2)x12 5c(\)x2 4a(J)x1 6c(l)x1 +1u  PARTIAL
   0x0006  37(7)x1                             37(7)x13 0a(.)x2 6c(l)x1 bf(.)x1    PARTIAL
   0x0007  37(7)x1                             37(7)x13 3c(<)x2 6c(l)x1 ff(.)x1    PARTIAL
   0x0008  37(7)x1                             37(7)x11 38(8)x2 3f(?)x2 6c(l)x1 +1u  PARTIAL
   0x0009  32(2)x1                             32(2)x13 78(x)x2 6c(l)x1 ff(.)x1    PARTIAL
   0x000a  2e(.)x1                             2e(.)x14 6d(m)x2 6c(l)x1            PARTIAL
   0x000b  78(x)x1                             78(x)x14 6c(l)x3                    PARTIAL
   0x000c  6d(m)x1                             6d(m)x15 20( )x2                    PARTIAL
   0x000d  6c(l)x1                             6c(l)x15 76(v)x2                    PARTIAL
   0x000e  5c(\)x1                             5c(\)x15 65(e)x2                    PARTIAL
   0x000f  0a(.)x1                             0a(.)x15 72(r)x2                    PARTIAL
   0x0010  3c(<)x1                             3c(<)x15 73(s)x2                    PARTIAL
   0x0011  3f(?)x1                             3f(?)x15 69(i)x2                    PARTIAL
   0x0012  78(x)x1                             78(x)x14 6f(o)x2 77(w)x1            PARTIAL
   0x0013  6d(m)x1                             6d(m)x15 6e(n)x2                    PARTIAL
   0x0014  6c(l)x1                             6c(l)x15 3d(=)x2                    PARTIAL
   0x0015  20( )x1                             20( )x15 22(")x2                    PARTIAL
   0x0016  76(v)x1                             76(v)x15 31(1)x2                    PARTIAL
   0x0017  65(e)x1                             65(e)x15 2e(.)x2                    PARTIAL
   0x0018  72(r)x1                             72(r)x15 30(0)x2                    PARTIAL
   0x0019  73(s)x1                             73(s)x15 22(")x2                    PARTIAL
   0x001a  69(i)x1                             69(i)x15 3f(?)x2                    PARTIAL
   0x001b  6f(o)x1                             6f(o)x15 3e(>)x2                    PARTIAL
   0x001c  6e(n)x1                             6e(n)x15 0a(.)x2                    PARTIAL
   0x001d  3d(=)x1                             3d(=)x15 3c(<)x2                    PARTIAL
   0x001e  22(")x1                             22(")x15 21(!)x2                    PARTIAL
   0x001f  31(1)x1                             31(1)x15 44(D)x2                    PARTIAL
   0x0020  2e(.)x1                             2e(.)x15 4f(O)x2                    PARTIAL
   0x0021  30(0)x1                             30(0)x15 43(C)x2                    PARTIAL
   0x0022  22(")x1                             22(")x15 54(T)x2                    PARTIAL
   0x0023  3f(?)x1                             3f(?)x15 59(Y)x2                    PARTIAL
   0x0024  3e(>)x1                             3e(>)x15 50(P)x2                    PARTIAL
   0x0025  0a(.)x1                             0a(.)x15 45(E)x2                    PARTIAL
   0x0026  3c(<)x1                             3c(<)x15 20( )x2                    PARTIAL
   0x0027  21(!)x1                             21(!)x15 61(a)x2                    PARTIAL
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

--- naive_ctx ---
**Instrumentation**: naive's SanitizerCoverage edge counters, but the
executor installs a `CtxHook` (`HookableInProcessExecutor`). The hook
keeps a running hash of the current call context (caller chain) and
folds it into the edge-map index, so the same basic-block edge is
recorded at different map slots depending on the call path that
reached it.

**Feedback**: the same `MaxMapFeedback` edge-bucket signal as naive,
computed over the context-indexed map — a "new bucket" is a new
(call-context, edge) pair rather than a bare edge.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`, no
CMP_MAP. Stages are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no ParentInfo-only / dash rows.

**Per-execution cost**: one edge-counter increment per executed edge
plus a context-hash update per call/return.

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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6405.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6405,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage), value_profile>naive (value_profile), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6405 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6405 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6405 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).