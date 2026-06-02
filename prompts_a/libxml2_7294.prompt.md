==== BLOCKER ====
Target: libxml2
Branch ID: 7294
Location: /src/libxml2/xmlreader.c:2952:10
Enclosing function: xmlTextReaderNodeType
Source line: 	    if ((reader->state == XML_TEXTREADER_END) ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           0       10          0  loser (grimoire_structural vs grimoire)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             2        8          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=1.80h  loser=24.00h
  avg hitcount on branch: winner=16  loser=0
  prob_div=1.00  dur_div=22.20h  hit_div=16
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7294/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlTextReaderNodeType (/src/libxml2/xmlreader.c:2939-2997) ---
[ ]  2937   */
[ ]  2938  int
[B]  2939  xmlTextReaderNodeType(xmlTextReaderPtr reader) {
[B]  2940      xmlNodePtr node;
[ ]  2941  
[B]  2942      if (reader == NULL)
[ ]  2943  	return(-1);
[B]  2944      if (reader->node == NULL)
[ ]  2945  	return(XML_READER_TYPE_NONE);
[B]  2946      if (reader->curnode != NULL)
[ ]  2947  	node = reader->curnode;
[B]  2948      else
[B]  2949  	node = reader->node;
[B]  2950      switch (node->type) {
[B]  2951          case XML_ELEMENT_NODE:
[B]  2952  	    if ((reader->state == XML_TEXTREADER_END) || <-- BLOCKER
[B]  2953  		(reader->state == XML_TEXTREADER_BACKTRACK))
[B]  2954  		return(XML_READER_TYPE_END_ELEMENT);
[B]  2955  	    return(XML_READER_TYPE_ELEMENT);
[ ]  2956          case XML_NAMESPACE_DECL:
[ ]  2957          case XML_ATTRIBUTE_NODE:
[ ]  2958  	    return(XML_READER_TYPE_ATTRIBUTE);
[B]  2959          case XML_TEXT_NODE:
[B]  2960  	    if (xmlIsBlankNode(reader->node)) {
[L]  2961  		if (xmlNodeGetSpacePreserve(reader->node))
[L]  2962  		    return(XML_READER_TYPE_SIGNIFICANT_WHITESPACE);
[ ]  2963  		else
[ ]  2964  		    return(XML_READER_TYPE_WHITESPACE);
[B]  2965  	    } else {
[B]  2966  		return(XML_READER_TYPE_TEXT);
[B]  2967  	    }
[ ]  2968          case XML_CDATA_SECTION_NODE:
[ ]  2969  	    return(XML_READER_TYPE_CDATA);
[ ]  2970          case XML_ENTITY_REF_NODE:
[ ]  2971  	    return(XML_READER_TYPE_ENTITY_REFERENCE);
[ ]  2972          case XML_ENTITY_NODE:
[ ]  2973  	    return(XML_READER_TYPE_ENTITY);
[B]  2974          case XML_PI_NODE:
[B]  2975  	    return(XML_READER_TYPE_PROCESSING_INSTRUCTION);
[ ]  2976          case XML_COMMENT_NODE:
[ ]  2977  	    return(XML_READER_TYPE_COMMENT);
[ ]  2978          case XML_DOCUMENT_NODE:
[ ]  2979          case XML_HTML_DOCUMENT_NODE:
[ ]  2980  	    return(XML_READER_TYPE_DOCUMENT);
[ ]  2981          case XML_DOCUMENT_FRAG_NODE:
[ ]  2982  	    return(XML_READER_TYPE_DOCUMENT_FRAGMENT);
[ ]  2983          case XML_NOTATION_NODE:
[ ]  2984  	    return(XML_READER_TYPE_NOTATION);
[ ]  2985          case XML_DOCUMENT_TYPE_NODE:
[B]  2986          case XML_DTD_NODE:
[B]  2987  	    return(XML_READER_TYPE_DOCUMENT_TYPE);
[ ]  2988  
[ ]  2989          case XML_ELEMENT_DECL:
[ ]  2990          case XML_ATTRIBUTE_DECL:
[ ]  2991          case XML_ENTITY_DECL:
[ ]  2992          case XML_XINCLUDE_START:
[ ]  2993          case XML_XINCLUDE_END:
[ ]  2994  	    return(XML_READER_TYPE_NONE);
[B]  2995      }
[ ]  2996      return(-1);
[B]  2997  }

--- Caller (1 hop): LLVMFuzzerTestOneInput (/src/libxml2/fuzz/xml.c:28-94, calls xmlTextReaderNodeType at line 80) (±10 around call site) ---
[B]    70      xmlParseChunk(ctxt, NULL, 0, 1);
[B]    71      xmlFreeDoc(ctxt->myDoc);
[B]    72      xmlFreeParserCtxt(ctxt);
[ ]    73  
[ ]    74      /* Reader */
[ ]    75  
[B]    76      reader = xmlReaderForMemory(docBuffer, docSize, NULL, NULL, opts);
[B]    77      if (reader == NULL)
[ ]    78          goto exit;
[B]    79      while (xmlTextReaderRead(reader) == 1) {
[B]    80          if (xmlTextReaderNodeType(reader) == XML_ELEMENT_NODE) { <-- CALL
[B]    81              int i, n = xmlTextReaderAttributeCount(reader);
[B]    82              for (i=0; i<n; i++) {
[B]    83                  xmlTextReaderMoveToAttributeNo(reader, i);
[B]    84                  while (xmlTextReaderReadAttributeValue(reader) == 1);
[B]    85              }
[B]    86          }
[B]    87      }
[B]    88      xmlFreeTextReader(reader);
[ ]    89  
[B]    90  exit:

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlTextReaderNodeType at line 80)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       2        22  xmlreader.c:xmlTextReaderCharacters  (/src/libxml2/xmlreader.c:721-731)
       0        15  xmlreader.c:xmlTextReaderStartElementNs  (/src/libxml2/xmlreader.c:664-682)
       6        21  xmlreader.c:xmlTextReaderPushData  (/src/libxml2/xmlreader.c:765-872)
       5        16  xmlreader.c:xmlTextReaderFreeNodeList  (/src/libxml2/xmlreader.c:291-375)
       3        10  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94)
       3        10  xmlreader.c:xmlTextReaderFreeDoc  (/src/libxml2/xmlreader.c:461-501)
       3        10  xmlNewTextReader  (/src/libxml2/xmlreader.c:2000-2103)
       3        10  xmlFreeTextReader  (/src/libxml2/xmlreader.c:2144-2202)
       3        10  xmlTextReaderClose  (/src/libxml2/xmlreader.c:2219-2254)
       3        10  xmlTextReaderSetup  (/src/libxml2/xmlreader.c:5048-5236)
       3        10  xmlReaderForMemory  (/src/libxml2/xmlreader.c:5361-5377)
       0         5  xmlreader.c:xmlTextReaderGetSuccessor  (/src/libxml2/xmlreader.c:1114-1123)
       0         5  xmlreader.c:xmlTextReaderDoExpand  (/src/libxml2/xmlreader.c:1137-1158)
       0         5  xmlTextReaderExpand  (/src/libxml2/xmlreader.c:1566-1576)
       5         1  xmlreader.c:xmlTextReaderValidatePop  (/src/libxml2/xmlreader.c:972-1012)
... (2 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94) ---
  d=2   L  45  T=0 F=3  T=0 F=10  if (docBuffer == NULL)
  d=2   L  59  T=0 F=3  T=0 F=10  if (ctxt == NULL)
  d=2   L  63  T=3 F=3  T=19 F=10  for (consumed = 0; consumed < docSize; consumed += chunkS...
  d=2   L  65  T=0 F=3  T=9 F=10  if (chunkSize > maxChunkSize)
  d=2   L  77  T=0 F=3  T=0 F=10  if (reader == NULL)
  d=2   L  79  T=20 F=3  T=47 F=10  while (xmlTextReaderRead(reader) == 1) {
  d=2   L  80  T=8 F=12  T=19 F=28  if (xmlTextReaderNodeType(reader) == XML_ELEMENT_NODE) {
--- d=1  xmlTextReaderNodeType  (/src/libxml2/xmlreader.c:2939-2997) ---
  d=1   L2942  T=0 F=20  T=0 F=47  if (reader == NULL)
  d=1   L2944  T=0 F=20  T=0 F=47  if (reader->node == NULL)
  d=1   L2946  T=0 F=20  T=0 F=47  if (reader->curnode != NULL)
  d=1   L2950  T=0 F=20  T=0 F=47  switch (node->type) {
  d=1   L2951  T=13 F=7  T=23 F=24  case XML_ELEMENT_NODE:
  d=1   L2952  T=3 F=10  T=0 F=23  if ((reader->state == XML_TEXTREADER_END) ||  <-- BLOCKER
  d=1   L2953  T=2 F=8  T=4 F=19  (reader->state == XML_TEXTREADER_BACKTRACK))
  d=1   L2956  T=0 F=20  T=0 F=47  case XML_NAMESPACE_DECL:
  d=1   L2957  T=0 F=20  T=0 F=47  case XML_ATTRIBUTE_NODE:
  d=1   L2959  T=1 F=19  T=13 F=34  case XML_TEXT_NODE:
  d=1   L2960  T=0 F=1  T=6 F=7  if (xmlIsBlankNode(reader->node)) {
  d=1   L2961  T=0 F=0  T=6 F=0  if (xmlNodeGetSpacePreserve(reader->node))
  d=1   L2968  T=0 F=20  T=0 F=47  case XML_CDATA_SECTION_NODE:
  d=1   L2970  T=0 F=20  T=0 F=47  case XML_ENTITY_REF_NODE:
  d=1   L2972  T=0 F=20  T=0 F=47  case XML_ENTITY_NODE:
  d=1   L2974  T=3 F=17  T=1 F=46  case XML_PI_NODE:
  d=1   L2976  T=0 F=20  T=0 F=47  case XML_COMMENT_NODE:
  d=1   L2978  T=0 F=20  T=0 F=47  case XML_DOCUMENT_NODE:
  d=1   L2979  T=0 F=20  T=0 F=47  case XML_HTML_DOCUMENT_NODE:
  d=1   L2981  T=0 F=20  T=0 F=47  case XML_DOCUMENT_FRAG_NODE:
  d=1   L2983  T=0 F=20  T=0 F=47  case XML_NOTATION_NODE:
  d=1   L2985  T=0 F=20  T=0 F=47  case XML_DOCUMENT_TYPE_NODE:
  d=1   L2986  T=3 F=17  T=10 F=37  case XML_DTD_NODE:
  d=1   L2989  T=0 F=20  T=0 F=47  case XML_ELEMENT_DECL:
  d=1   L2990  T=0 F=20  T=0 F=47  case XML_ATTRIBUTE_DECL:
  d=1   L2991  T=0 F=20  T=0 F=47  case XML_ENTITY_DECL:
  d=1   L2992  T=0 F=20  T=0 F=47  case XML_XINCLUDE_START:
  d=1   L2993  T=0 F=20  T=0 F=47  case XML_XINCLUDE_END:

[off-chain: 288 additional divergent branches across 23 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=4c1ded53000f2888, size=328 bytes, fuzzer=grimoire, trial=1, discovered_at=11655s, mutation_op=GrimoireRecursiveReplacementMutator,GrimoireRandomDeleteMutator,GrimoireRandomDeleteMutator):
  0000: 9c ff ff ff 06 78 6d 6c 5c 0a 3c 3f 6c 20 3f 3e   .....xml\.<?l ?>
  0010: 3c 21 44 4f 43 54 59 50 45 61 20 53 59 53 54 45   <!DOCTYPEa SYSTE
  0020: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
  0030: 74 64 22 3e 3c 61 3e 3c 62 20 66 3d 22 22 3e 3c   td"><a><b f=""><
Seed 2 (id=b662d817d5ab9bb6, size=220 bytes, fuzzer=grimoire, trial=1, discovered_at=13735s, mutation_op=BytesDeleteMutator,ByteDecMutator):
  0000: 77 77 6b 27 20 78 6c 69 6e 6b 20 28 65 29 20 27   wwk' xlink (e) '
  0010: 27 20 6e 6b 3a 68 72 65 66 20 43 44 41 54 41 20   ' nk:href CDATA 
  0020: 23 49 4d 50 4c 49 45 44 3e 9f 86 06 37 6d 6c 5c   #IMPLIED>...7ml\
  0030: 0a 3c 3f 6c 3f 3e 3c 21 44 4f 43 54 59 50 45 61   .<?l?><!DOCTYPEa
Seed 3 (id=7f4e04734d7c7f74, size=219 bytes, fuzzer=grimoire, trial=1, discovered_at=17396s, mutation_op=BytesSetMutator):
  0000: ff ab ab ab ab ab 15 a9 05 49 53 4f 12 38 38 35   .........ISO.885
  0010: 39 2d 34 78 6d 6c 00 49 53 4f 2d 38 38 35 39 2d   9-4xml.ISO-8859-
  0020: 32 78 6d 6c 00 00 d4 01 00 7f 69 67 ff ff ff ff   2xml......ig....
  0030: ff fd ff ff ff ff 49 53 4f 2d 38 38 35 39 2d 35   ......ISO-8859-5

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=05a2233124360cc9, size=299 bytes, fuzzer=cmplog, trial=1, discovered_at=22s, mutation_op=BytesExpandMutator,TokenReplace,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2c 78 6d 6c 5c 0a   ....127772,xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 6b 6b   a SYSTEM "dtdskk
Seed 2 (id=0243680d59374a7c, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=54s, mutation_op=WordInterestingMutator,TokenReplace):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=09facfa22bc46ce6, size=379 bytes, fuzzer=cmplog, trial=1, discovered_at=58s, mutation_op=BytesSetMutator,CrossoverReplaceMutator):
  0000: 77 77 77 77 77 77 77 77 77 77 77 77 6d 6c 5c 0a   wwwwwwwwwwwwml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=0a9c869d5e3c189b, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=95s, mutation_op=TokenInsert,BytesSetMutator,ByteIncMutator,BytesDeleteMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=047fe13ea3b05010, size=386 bytes, fuzzer=cmplog, trial=1, discovered_at=4456s, mutation_op=WordAddMutator,BytesDeleteMutator,CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 3b 31   a SYSTEM "dtds;1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  9c(.)x1 77(w)x1 ff(.)x1             06(.)x8 77(w)x1 31(1)x1             PARTIAL
   0x0001  ff(.)x1 77(w)x1 ab(.)x1             00(.)x7 77(w)x1 25(%)x1 32(2)x1     PARTIAL
   0x0002  ff(.)x1 6b(k)x1 ab(.)x1             00(.)x8 77(w)x1 37(7)x1             DIFFER
   0x0003  ff(.)x1 27(')x1 ab(.)x1             00(.)x8 77(w)x1 37(7)x1             DIFFER
   0x0004  06(.)x1 20( )x1 ab(.)x1             31(1)x6 77(w)x1 2f(/)x1 37(7)x1 +1u  DIFFER
   0x0005  78(x)x2 ab(.)x1                     32(2)x7 77(w)x1 2d(-)x1 74(t)x1     DIFFER
   0x0006  6d(m)x1 6c(l)x1 15(.)x1             37(7)x6 77(w)x1 02(.)x1 2e(.)x1 +1u  DIFFER
   0x0007  6c(l)x1 69(i)x1 a9(.)x1             37(7)x6 77(w)x1 02(.)x1 64(d)x1 +1u  DIFFER
   0x0008  5c(\)x1 6e(n)x1 05(.)x1             37(7)x7 77(w)x1 73(s)x1 2d(-)x1     DIFFER
   0x0009  0a(.)x1 6b(k)x1 49(I)x1             32(2)x7 77(w)x1 64(d)x1 3a(:)x1     DIFFER
   0x000a  3c(<)x1 20( )x1 53(S)x1             2e(.)x5 2c(,)x2 77(w)x1 06(.)x1 +1u  DIFFER
   0x000b  3f(?)x1 28(()x1 4f(O)x1             78(x)x6 77(w)x1 2f(/)x1 00(.)x1 +1u  DIFFER
   0x000c  6c(l)x1 65(e)x1 12(.)x1             6d(m)x8 00(.)x1 37(7)x1             DIFFER
   0x000d  20( )x1 29())x1 38(8)x1             6c(l)x8 00(.)x1 37(7)x1             DIFFER
   0x000e  3f(?)x1 20( )x1 38(8)x1             5c(\)x9 31(1)x1                     DIFFER
   0x000f  3e(>)x1 27(')x1 35(5)x1             0a(.)x9 32(2)x1                     DIFFER
   0x0010  3c(<)x1 27(')x1 39(9)x1             3c(<)x9 37(7)x1                     PARTIAL
   0x0011  21(!)x1 20( )x1 2d(-)x1             3f(?)x9 37(7)x1                     DIFFER
   0x0012  44(D)x1 6e(n)x1 34(4)x1             78(x)x9 37(7)x1                     DIFFER
   0x0013  4f(O)x1 6b(k)x1 78(x)x1             6d(m)x8 32(2)x1 54(T)x1             DIFFER
   0x0014  43(C)x1 3a(:)x1 6d(m)x1             6c(l)x9 2e(.)x1                     DIFFER
   0x0015  54(T)x1 68(h)x1 6c(l)x1             20( )x9 78(x)x1                     DIFFER
   0x0016  59(Y)x1 72(r)x1 00(.)x1             76(v)x9 6d(m)x1                     DIFFER
   0x0017  50(P)x1 65(e)x1 49(I)x1             65(e)x9 6c(l)x1                     PARTIAL
   0x0018  45(E)x1 66(f)x1 53(S)x1             72(r)x9 5c(\)x1                     DIFFER
   0x0019  61(a)x1 20( )x1 4f(O)x1             73(s)x9 0a(.)x1                     DIFFER
   0x001a  20( )x1 43(C)x1 2d(-)x1             69(i)x9 3c(<)x1                     DIFFER
   0x001b  53(S)x1 44(D)x1 38(8)x1             6f(o)x9 3f(?)x1                     DIFFER
   0x001c  59(Y)x1 41(A)x1 38(8)x1             6e(n)x9 78(x)x1                     DIFFER
   0x001d  53(S)x1 54(T)x1 35(5)x1             3d(=)x8 6d(m)x1 3a(:)x1             DIFFER
   0x001e  54(T)x1 41(A)x1 39(9)x1             22(")x9 6c(l)x1                     DIFFER
   0x001f  45(E)x1 20( )x1 2d(-)x1             31(1)x9 20( )x1                     PARTIAL
   0x0020  4d(M)x1 23(#)x1 32(2)x1             2e(.)x9 76(v)x1                     DIFFER
   0x0021  20( )x1 49(I)x1 78(x)x1             30(0)x9 65(e)x1                     DIFFER
   0x0022  22(")x1 4d(M)x1 6d(m)x1             22(")x9 72(r)x1                     PARTIAL
   0x0023  64(d)x1 50(P)x1 6c(l)x1             3f(?)x9 73(s)x1                     DIFFER
   0x0024  74(t)x1 4c(L)x1 00(.)x1             3e(>)x9 69(i)x1                     DIFFER
   0x0025  64(d)x1 49(I)x1 00(.)x1             0a(.)x9 6f(o)x1                     DIFFER
   0x0026  73(s)x1 45(E)x1 d4(.)x1             3c(<)x9 6e(n)x1                     DIFFER
   0x0027  2f(/)x1 44(D)x1 01(.)x1             21(!)x9 3d(=)x1                     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7294.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7294,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7294 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7294 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7294 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).