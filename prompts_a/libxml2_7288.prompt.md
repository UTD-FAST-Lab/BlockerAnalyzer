==== BLOCKER ====
Target: libxml2
Branch ID: 7288
Location: /src/libxml2/xmlreader.c:2826:6
Enclosing function: xmlTextReaderReadAttributeValue
Source line: 	if (reader->curnode->children == NULL)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           1        9          0  loser (grimoire_structural vs grimoire)
value_profile                    ?        ?          ?  REFERENCE
value_profile_cmplog             0       10          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=0.40h  loser=23.30h
  avg hitcount on branch: winner=25  loser=0
  prob_div=0.90  dur_div=22.90h  hit_div=25
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7288/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlTextReaderReadAttributeValue (/src/libxml2/xmlreader.c:2818-2849) ---
[ ]  2816   */
[ ]  2817  int
[B]  2818  xmlTextReaderReadAttributeValue(xmlTextReaderPtr reader) {
[B]  2819      if (reader == NULL)
[ ]  2820  	return(-1);
[B]  2821      if (reader->node == NULL)
[ ]  2822  	return(-1);
[B]  2823      if (reader->curnode == NULL)
[ ]  2824  	return(0);
[B]  2825      if (reader->curnode->type == XML_ATTRIBUTE_NODE) {
[B]  2826  	if (reader->curnode->children == NULL) <-- BLOCKER
[W]  2827  	    return(0);
[B]  2828  	reader->curnode = reader->curnode->children;
[B]  2829      } else if (reader->curnode->type == XML_NAMESPACE_DECL) {
[W]  2830  	xmlNsPtr ns = (xmlNsPtr) reader->curnode;
[ ]  2831  
[W]  2832  	if (reader->faketext == NULL) {
[W]  2833  	    reader->faketext = xmlNewDocText(reader->node->doc,
[W]  2834  		                             ns->href);
[W]  2835  	} else {
[ ]  2836              if ((reader->faketext->content != NULL) &&
[ ]  2837  	        (reader->faketext->content !=
[ ]  2838  		 (xmlChar *) &(reader->faketext->properties)))
[ ]  2839  		xmlFree(reader->faketext->content);
[ ]  2840  	    reader->faketext->content = xmlStrdup(ns->href);
[ ]  2841  	}
[W]  2842  	reader->curnode = reader->faketext;
[B]  2843      } else {
[B]  2844  	if (reader->curnode->next == NULL)
[B]  2845  	    return(0);
[ ]  2846  	reader->curnode = reader->curnode->next;
[ ]  2847      }
[B]  2848      return(1);
[B]  2849  }

--- Caller (1 hop): LLVMFuzzerTestOneInput (/src/libxml2/fuzz/xml.c:28-94, calls xmlTextReaderReadAttributeValue at line 84) (±10 around call site) ---
[ ]    74      /* Reader */
[ ]    75  
[B]    76      reader = xmlReaderForMemory(docBuffer, docSize, NULL, NULL, opts);
[B]    77      if (reader == NULL)
[ ]    78          goto exit;
[B]    79      while (xmlTextReaderRead(reader) == 1) {
[B]    80          if (xmlTextReaderNodeType(reader) == XML_ELEMENT_NODE) {
[B]    81              int i, n = xmlTextReaderAttributeCount(reader);
[B]    82              for (i=0; i<n; i++) {
[B]    83                  xmlTextReaderMoveToAttributeNo(reader, i);
[B]    84                  while (xmlTextReaderReadAttributeValue(reader) == 1); <-- CALL
[B]    85              }
[B]    86          }
[B]    87      }
[B]    88      xmlFreeTextReader(reader);
[ ]    89  
[B]    90  exit:
[B]    91      xmlFuzzDataCleanup();
[B]    92      xmlResetLastError();
[B]    93      return(0);
[B]    94  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlTextReaderReadAttributeValue at line 84)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       8        30  xmlreader.c:xmlTextReaderFreeNode  (/src/libxml2/xmlreader.c:386-451)
       9        28  xmlreader.c:xmlTextReaderCharacters  (/src/libxml2/xmlreader.c:721-731)
       0        17  xmlreader.c:xmlTextReaderStartElementNs  (/src/libxml2/xmlreader.c:664-682)
       1         9  xmlreader.c:xmlTextReaderDoExpand  (/src/libxml2/xmlreader.c:1137-1158)
       1         9  xmlTextReaderExpand  (/src/libxml2/xmlreader.c:1566-1576)
       1         7  xmlreader.c:xmlTextReaderValidateCData  (/src/libxml2/xmlreader.c:944-963)
       0         6  xmlreader.c:xmlTextReaderGetSuccessor  (/src/libxml2/xmlreader.c:1114-1123)
       0         5  xmlreader.c:xmlTextReaderEndElementNs  (/src/libxml2/xmlreader.c:698-708)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94) ---
  d=2   L  65  T=0 F=9  T=6 F=10  if (chunkSize > maxChunkSize)
  d=2   L  79  T=26 F=9  T=66 F=10  while (xmlTextReaderRead(reader) == 1) {
  d=2   L  80  T=14 F=12  T=25 F=41  if (xmlTextReaderNodeType(reader) == XML_ELEMENT_NODE) {
--- d=1  xmlTextReaderReadAttributeValue  (/src/libxml2/xmlreader.c:2818-2849) ---
  d=1   L2826  T=9 F=1  T=0 F=11  if (reader->curnode->children == NULL)  <-- BLOCKER
  d=1   L2829  T=2 F=3  T=0 F=11  } else if (reader->curnode->type == XML_NAMESPACE_DECL) {
  d=1   L2832  T=2 F=0  T=0 F=0  if (reader->faketext == NULL) {
  d=1   L2844  T=3 F=0  T=11 F=0  if (reader->curnode->next == NULL)

[off-chain: 201 additional divergent branches across 18 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0037c50e9826accb, size=38 bytes, fuzzer=grimoire, trial=1, discovered_at=97s, mutation_op=GrimoireRecursiveReplacementMutator):
  0000: ec ff ff ff 00 31 37 37 37 32 2e 78 6d 6c 5c 0a   .....17772.xml\.
  0010: 3c 6c 20 6e 3d 22 22 3e 3c 62 20 72 49 53 4f 2d   <l n=""><b rISO-
  0020: 38 38 35 39 2d 33                                 8859-3
Seed 2 (id=89b81b76a140847e, size=69 bytes, fuzzer=grimoire, trial=1, discovered_at=1948s, mutation_op=GrimoireExtensionMutator,GrimoireRecursiveReplacementMutator):
  0000: 49 53 4f 2d 38 38 35 39 2d 33 fb ff ff ff ff ff   ISO-8859-3......
  0010: ff ff 02 e0 ff ff 00 00 31 6c 5c 0a 3c 6c 20 6e   ........1l\.<l n
  0020: 3d 22 22 3e 20 20 3c 62 20 74 65 78 74 3c 00 fe   ="">  <b text<..
  0030: ff ff ff 49 53 4f 2d 38 38 35 39 2d 32 7f 69 67   ...ISO-8859-2.ig
Seed 3 (id=0d2e97323ba4a9ae, size=229 bytes, fuzzer=grimoire, trial=1, discovered_at=2209s, mutation_op=GrimoireRecursiveReplacementMutator):
  0000: 49 53 4f 2d 38 38 35 39 2d 39 00 78 6d 6c 5c 0a   ISO-8859-9.xml\.
  0010: 3c 6c 20 6e 3d 22 22 3e 0a 1f 0a 49 53 4f 6c 5c   <l n="">...ISOl\
  0020: 0a 3c 3f 6c 3f 3e 3c 21 44 4f 43 54 59 50 45 61   .<?l?><!DOCTYPEa
  0030: 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32    SYSTEM "dtds/12
Seed 4 (id=4dfb54980cf39827, size=155 bytes, fuzzer=grimoire, trial=1, discovered_at=4750s, mutation_op=GrimoireRecursiveReplacementMutator):
  0000: f8 ff ff ff ff 06 6d 6c 5c 0a 3c 3f 6c 20 3f 3e   ......ml\.<?l ?>
  0010: 3c 21 44 4f 43 54 59 50 45 61 20 53 59 53 54 45   <!DOCTYPEa SYSTE
  0020: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
  0030: 74 64 22 3e 3c 61 3e 3c 62 20 3a 51 3d 22 22 3e   td"><a><b :Q="">
Seed 5 (id=110e34e3a9cff266, size=416 bytes, fuzzer=grimoire, trial=1, discovered_at=4878s, mutation_op=GrimoireRecursiveReplacementMutator,GrimoireRecursiveReplacementMutator):
  0000: 55 36 e8 76 ad 9c f0 4c ff 37 37 32 6c 5c 0a 3c   U6.v...L.772l\.<
  0010: 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e   ?xml version="1.
  0020: 30 22 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20 53   0"?><!DOCTYPEa S
  0030: 59 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37   YSTEM "dtds/1277

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=2792bedfa11bd0f7, size=379 bytes, fuzzer=cmplog, trial=1, discovered_at=0s, mutation_op=BytesExpandMutator,TokenReplace,ByteDecMutator,BytesRandSetMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=0e43b227bd057ebf, size=410 bytes, fuzzer=cmplog, trial=1, discovered_at=20s, mutation_op=ByteRandMutator,BytesInsertCopyMutator,WordAddMutator,BytesSetMutator,BytesSetMutator,BytesInsertCopyMutator,BytesRandInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 25 31   a SYSTEM "dtds%1
Seed 3 (id=05a2233124360cc9, size=299 bytes, fuzzer=cmplog, trial=1, discovered_at=22s, mutation_op=BytesExpandMutator,TokenReplace,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2c 78 6d 6c 5c 0a   ....127772,xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 6b 6b   a SYSTEM "dtdskk
Seed 4 (id=0a9c869d5e3c189b, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=95s, mutation_op=TokenInsert,BytesSetMutator,ByteIncMutator,BytesDeleteMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=0daca46eaa46b0ce, size=365 bytes, fuzzer=cmplog, trial=1, discovered_at=271s, mutation_op=TokenInsert,BitFlipMutator,BytesDeleteMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c   ersion="1.0"?>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45   !DOCTYPE a SYSTE
  0030: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  49(I)x3 ec(.)x1 f8(.)x1 55(U)x1 +3u  06(.)x7 31(1)x2 37(7)x1             DIFFER
   0x0001  ff(.)x3 53(S)x3 36(6)x1 3e(>)x1 +1u  00(.)x7 32(2)x2 37(7)x1             DIFFER
   0x0002  ff(.)x3 4f(O)x3 e8(.)x1 42(B)x1 +1u  00(.)x7 37(7)x2 32(2)x1             DIFFER
   0x0003  ff(.)x3 2d(-)x3 76(v)x1 0f(.)x1 +1u  00(.)x7 37(7)x2 2e(.)x1             DIFFER
   0x0004  38(8)x2 00(.)x1 ff(.)x1 ad(.)x1 +4u  31(1)x6 37(7)x2 78(x)x1 2f(/)x1     DIFFER
   0x0005  38(8)x2 31(1)x1 06(.)x1 9c(.)x1 +4u  32(2)x8 6d(m)x1 2d(-)x1             DIFFER
   0x0006  35(5)x2 6d(m)x2 37(7)x1 f0(.)x1 +3u  37(7)x6 2e(.)x2 6c(l)x1 02(.)x1     PARTIAL
   0x0007  39(9)x2 6c(l)x2 37(7)x1 4c(L)x1 +3u  37(7)x6 64(d)x2 5c(\)x1 02(.)x1     PARTIAL
   0x0008  2d(-)x3 5c(\)x2 37(7)x1 ff(.)x1 +2u  37(7)x7 73(s)x2 0a(.)x1             PARTIAL
   0x0009  0a(.)x2 32(2)x1 33(3)x1 39(9)x1 +4u  32(2)x7 64(d)x2 3c(<)x1             PARTIAL
   0x000a  3c(<)x2 2e(.)x1 fb(.)x1 00(.)x1 +4u  2e(.)x5 2c(,)x2 06(.)x2 3f(?)x1     PARTIAL
   0x000b  3f(?)x3 78(x)x2 ff(.)x1 32(2)x1 +2u  78(x)x8 00(.)x2                     PARTIAL
   0x000c  6c(l)x3 6d(m)x2 ff(.)x1 3e(>)x1 +2u  6d(m)x8 00(.)x2                     PARTIAL
   0x000d  6c(l)x2 20( )x2 ff(.)x1 5c(\)x1 +3u  6c(l)x8 00(.)x2                     PARTIAL
   0x000e  5c(\)x2 3f(?)x2 ff(.)x1 0a(.)x1 +3u  5c(\)x7 31(1)x2 20( )x1             PARTIAL
   0x000f  0a(.)x2 3e(>)x2 ff(.)x1 3c(<)x1 +3u  0a(.)x7 32(2)x2 76(v)x1             PARTIAL
   0x0010  3c(<)x4 ff(.)x1 3f(?)x1 4f(O)x1 +2u  3c(<)x7 37(7)x2 65(e)x1             PARTIAL
   0x0011  6c(l)x2 21(!)x2 ff(.)x1 78(x)x1 +3u  3f(?)x7 37(7)x2 72(r)x1             DIFFER
   0x0012  20( )x2 44(D)x2 02(.)x1 6d(m)x1 +3u  78(x)x7 37(7)x2 73(s)x1             DIFFER
   0x0013  6e(n)x2 4f(O)x2 e0(.)x1 6c(l)x1 +3u  6d(m)x7 32(2)x2 69(i)x1             DIFFER
   0x0014  3d(=)x2 43(C)x2 ff(.)x1 20( )x1 +3u  6c(l)x7 2e(.)x2 6f(o)x1             DIFFER
   0x0015  22(")x2 54(T)x2 ff(.)x1 76(v)x1 +3u  20( )x7 78(x)x2 6e(n)x1             DIFFER
   0x0016  22(")x3 59(Y)x2 00(.)x1 65(e)x1 +2u  76(v)x7 6d(m)x2 3d(=)x1             DIFFER
   0x0017  3e(>)x2 50(P)x2 00(.)x1 72(r)x1 +3u  65(e)x7 6c(l)x2 22(")x1             PARTIAL
   0x0018  45(E)x2 3e(>)x2 3c(<)x1 31(1)x1 +3u  72(r)x7 5c(\)x2 31(1)x1             PARTIAL
   0x0019  61(a)x2 62(b)x1 6c(l)x1 1f(.)x1 +4u  73(s)x7 0a(.)x2 2e(.)x1             PARTIAL
   0x001a  20( )x4 5c(\)x1 0a(.)x1 6f(o)x1 +2u  69(i)x7 3c(<)x2 30(0)x1             PARTIAL
   0x001b  53(S)x2 72(r)x1 0a(.)x1 49(I)x1 +4u  6f(o)x7 3f(?)x2 22(")x1             DIFFER
   0x001c  59(Y)x2 49(I)x1 3c(<)x1 53(S)x1 +4u  6e(n)x7 78(x)x2 3f(?)x1             DIFFER
   0x001d  53(S)x3 6c(l)x1 4f(O)x1 22(")x1 +3u  3d(=)x7 6d(m)x2 3e(>)x1             DIFFER
   0x001e  20( )x2 54(T)x2 4f(O)x1 6c(l)x1 +3u  22(")x7 6c(l)x2 0a(.)x1             PARTIAL
   0x001f  45(E)x2 2d(-)x1 6e(n)x1 5c(\)x1 +3u  31(1)x7 20( )x2 3c(<)x1             DIFFER
   0x0020  4d(M)x2 38(8)x1 3d(=)x1 0a(.)x1 +3u  2e(.)x7 76(v)x2 21(!)x1             DIFFER
   0x0021  22(")x2 20( )x2 38(8)x1 3c(<)x1 +2u  30(0)x7 65(e)x2 44(D)x1             DIFFER
   0x0022  22(")x3 3f(?)x2 35(5)x1 64(d)x1 +1u  22(")x7 72(r)x2 4f(O)x1             PARTIAL
   0x0023  3e(>)x2 64(d)x2 39(9)x1 6c(l)x1 +2u  3f(?)x7 73(s)x2 43(C)x1             PARTIAL
   0x0024  74(t)x2 2d(-)x1 20( )x1 3f(?)x1 +3u  3e(>)x7 69(i)x2 54(T)x1             DIFFER
   0x0025  64(d)x2 33(3)x1 20( )x1 3e(>)x1 +3u  0a(.)x7 6f(o)x2 59(Y)x1             DIFFER
   0x0026  3c(<)x2 73(s)x2 44(D)x1 32(2)x1 +1u  3c(<)x7 6e(n)x2 50(P)x1             PARTIAL
   0x0027  2f(/)x2 62(b)x1 21(!)x1 4f(O)x1 +2u  21(!)x7 3d(=)x2 45(E)x1             PARTIAL
   ... (22 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7288.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7288,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7288 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7288 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7288 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).