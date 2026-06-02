==== BLOCKER ====
Target: libxml2
Branch ID: 8630
Location: /src/libxml2/xmlsave.c:686:36
Enclosing function: xmlsave.c:xmlDtdDumpOutput
Source line:     if ((dtd->entities == NULL) && (dtd->elements == NULL) &&
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (ctx_coverage vs naive_ctx)
cmplog                           0       10          0  REFERENCE
value_profile                    4        6          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=12.50h  loser=24.00h
  avg hitcount on branch: winner=46  loser=0
  prob_div=0.80  dur_div=11.50h  hit_div=46
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/8630/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlsave.c:xmlDtdDumpOutput (/src/libxml2/xmlsave.c:666-712) ---
[ ]   664   */
[ ]   665  static void
[B]   666  xmlDtdDumpOutput(xmlSaveCtxtPtr ctxt, xmlDtdPtr dtd) {
[B]   667      xmlOutputBufferPtr buf;
[B]   668      xmlNodePtr cur;
[B]   669      int format, level;
[ ]   670  
[B]   671      if (dtd == NULL) return;
[B]   672      if ((ctxt == NULL) || (ctxt->buf == NULL))
[ ]   673          return;
[B]   674      buf = ctxt->buf;
[B]   675      xmlOutputBufferWrite(buf, 10, "<!DOCTYPE ");
[B]   676      xmlOutputBufferWriteString(buf, (const char *)dtd->name);
[B]   677      if (dtd->ExternalID != NULL) {
[ ]   678  	xmlOutputBufferWrite(buf, 8, " PUBLIC ");
[ ]   679  	xmlBufWriteQuotedString(buf->buffer, dtd->ExternalID);
[ ]   680  	xmlOutputBufferWrite(buf, 1, " ");
[ ]   681  	xmlBufWriteQuotedString(buf->buffer, dtd->SystemID);
[B]   682      }  else if (dtd->SystemID != NULL) {
[L]   683  	xmlOutputBufferWrite(buf, 8, " SYSTEM ");
[L]   684  	xmlBufWriteQuotedString(buf->buffer, dtd->SystemID);
[L]   685      }
[B]   686      if ((dtd->entities == NULL) && (dtd->elements == NULL) && <-- BLOCKER
[B]   687          (dtd->attributes == NULL) && (dtd->notations == NULL) &&
[B]   688  	(dtd->pentities == NULL)) {
[L]   689  	xmlOutputBufferWrite(buf, 1, ">");
[L]   690  	return;
[L]   691      }
[W]   692      xmlOutputBufferWrite(buf, 3, " [\n");
[ ]   693      /*
[ ]   694       * Dump the notations first they are not in the DTD children list
[ ]   695       * Do this only on a standalone DTD or on the internal subset though.
[ ]   696       */
[W]   697      if ((dtd->notations != NULL) && ((dtd->doc == NULL) ||
[ ]   698          (dtd->doc->intSubset == dtd))) {
[ ]   699          xmlBufDumpNotationTable(buf->buffer,
[ ]   700                                  (xmlNotationTablePtr) dtd->notations);
[ ]   701      }
[W]   702      format = ctxt->format;
[W]   703      level = ctxt->level;
[W]   704      ctxt->format = 0;
[W]   705      ctxt->level = -1;
[W]   706      for (cur = dtd->children; cur != NULL; cur = cur->next) {
[W]   707          xmlNodeDumpOutputInternal(ctxt, cur);
[W]   708      }
[W]   709      ctxt->format = format;
[W]   710      ctxt->level = level;
[W]   711      xmlOutputBufferWrite(buf, 2, "]>");
[W]   712  }

--- Caller (1 hop): xmlsave.c:xmlNodeDumpOutputInternal (/src/libxml2/xmlsave.c:809-1068, calls xmlsave.c:xmlDtdDumpOutput at line 829) (±10 around call site) ---
[B]   819      root = cur;
[B]   820      parent = cur->parent;
[B]   821      while (1) {
[B]   822          switch (cur->type) {
[ ]   823          case XML_DOCUMENT_NODE:
[ ]   824          case XML_HTML_DOCUMENT_NODE:
[ ]   825  	    xmlDocContentDumpOutput(ctxt, (xmlDocPtr) cur);
[ ]   826  	    break;
[ ]   827  
[B]   828          case XML_DTD_NODE:
[B]   829              xmlDtdDumpOutput(ctxt, (xmlDtdPtr) cur); <-- CALL
[B]   830              break;
[ ]   831  
[ ]   832          case XML_DOCUMENT_FRAG_NODE:
[ ]   833              /* Always validate cur->parent when descending. */
[ ]   834              if ((cur->parent == parent) && (cur->children != NULL)) {
[ ]   835                  parent = cur;
[ ]   836                  cur = cur->children;
[ ]   837                  continue;
[ ]   838              }
[ ]   839  	    break;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlsave.c:xhtmlNodeDumpOutput  (/src/libxml2/xmlsave.c:1392-1700, calls xmlsave.c:xmlDtdDumpOutput at line 1413)
hop 2  xmlsave.c:xmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:809-1068, calls xmlsave.c:xmlDtdDumpOutput at line 829)
hop 3  xmlSaveTree  (/src/libxml2/xmlsave.c:1860-1879, calls xmlsave.c:xhtmlNodeDumpOutput at line 1866)
hop 3  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225, calls xmlsave.c:xmlNodeDumpOutputInternal at line 1206)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        20  xmlsave.c:xmlEscapeEntities  (/src/libxml2/xmlsave.c:166-274)
      10         0  xmlsave.c:xmlBufDumpElementDecl  (/src/libxml2/xmlsave.c:449-462)
       0         3  xmlsave.c:xmlSaveErr  (/src/libxml2/xmlsave.c:81-101)
       0         1  xmlsave.c:xmlSerializeHexCharRef  (/src/libxml2/xmlsave.c:109-147)
       0         1  xmlsave.c:xmlAttrSerializeContent  (/src/libxml2/xmlsave.c:393-415)
       1         0  xmlsave.c:xmlBufDumpAttributeDecl  (/src/libxml2/xmlsave.c:473-486)
       0         1  xmlsave.c:xmlAttrDumpOutput  (/src/libxml2/xmlsave.c:722-740)
       0         1  xmlBufAttrSerializeTxtContent  (/src/libxml2/xmlsave.c:1970-2080)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  xmlsave.c:xmlDocContentDumpOutput  (/src/libxml2/xmlsave.c:1077-1225) ---
  d=3   L1192  T=10 F=0  T=2 F=8  if (is_xhtml < 0) is_xhtml = 0;
--- d=2  xmlsave.c:xmlNodeDumpOutputInternal  (/src/libxml2/xmlsave.c:809-1068) ---
  d=2   L 823  T=0 F=23  T=0 F=57  case XML_DOCUMENT_NODE:
  d=2   L 824  T=0 F=23  T=0 F=57  case XML_HTML_DOCUMENT_NODE:
  d=2   L 828  T=10 F=13  T=10 F=47  case XML_DTD_NODE:
  d=2   L 832  T=0 F=23  T=0 F=57  case XML_DOCUMENT_FRAG_NODE:
  d=2   L 841  T=10 F=13  T=0 F=57  case XML_ELEMENT_DECL:
  d=2   L 845  T=1 F=22  T=0 F=57  case XML_ATTRIBUTE_DECL:
  d=2   L 849  T=0 F=23  T=0 F=57  case XML_ENTITY_DECL:
  d=2   L 853  T=0 F=23  T=26 F=31  case XML_ELEMENT_NODE:
  d=2   L 854  T=0 F=0  T=22 F=4  if ((cur != root) && (ctxt->format == 1) &&
  d=2   L 854  T=0 F=0  T=0 F=22  if ((cur != root) && (ctxt->format == 1) &&
  d=2   L 866  T=0 F=0  T=0 F=26  if ((cur->parent != parent) && (cur->children != NULL)) {
  d=2   L 872  T=0 F=0  T=0 F=26  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=2   L 877  T=0 F=0  T=0 F=26  if (cur->nsDef)
  d=2   L 879  T=0 F=0  T=1 F=26  for (attr = cur->properties; attr != NULL; attr = attr->n...
  d=2   L 882  T=0 F=0  T=18 F=8  if (cur->children == NULL) {
  d=2   L 883  T=0 F=0  T=18 F=0  if ((ctxt->options & XML_SAVE_NO_EMPTY) == 0) {
  d=2   L 884  T=0 F=0  T=0 F=18  if (ctxt->format == 2)
  d=2   L 902  T=0 F=0  T=0 F=8  if (ctxt->format == 1) {
  d=2   L 915  T=0 F=0  T=0 F=8  if (ctxt->format == 2)
  d=2   L 918  T=0 F=0  T=0 F=8  if (ctxt->format == 1) xmlOutputBufferWrite(buf, 1, "\n");
  d=2   L 919  T=0 F=0  T=8 F=0  if (ctxt->level >= 0) ctxt->level++;
  d=2   L 927  T=0 F=23  T=19 F=38  case XML_TEXT_NODE:
  d=2   L 928  T=0 F=0  T=0 F=19  if (cur->content == NULL)
  d=2   L 930  T=0 F=0  T=19 F=0  if (cur->name != xmlStringTextNoenc) {
  d=2   L 940  T=1 F=22  T=2 F=55  case XML_PI_NODE:
  d=2   L 941  T=0 F=1  T=0 F=2  if ((cur != root) && (ctxt->format == 1) && (xmlIndentTre...
  d=2   L 947  T=1 F=0  T=2 F=0  if (cur->content != NULL) {
  d=2   L 950  T=1 F=0  T=2 F=0  if (cur->content != NULL) {
  d=2   L 951  T=0 F=1  T=0 F=2  if (ctxt->format == 2)
  d=2   L 968  T=1 F=22  T=0 F=57  case XML_COMMENT_NODE:
  d=2   L 969  T=0 F=1  T=0 F=0  if ((cur != root) && (ctxt->format == 1) && (xmlIndentTre...
  d=2   L 975  T=1 F=0  T=0 F=0  if (cur->content != NULL) {
  d=2   L 982  T=0 F=23  T=0 F=57  case XML_ENTITY_REF_NODE:
  d=2   L 988  T=0 F=23  T=0 F=57  case XML_CDATA_SECTION_NODE:
  d=2   L1013  T=0 F=23  T=0 F=57  case XML_ATTRIBUTE_NODE:
  d=2   L1017  T=0 F=23  T=0 F=57  case XML_NAMESPACE_DECL:
  d=2   L1021  T=0 F=23  T=0 F=57  default:
  d=2   L1026  T=23 F=0  T=16 F=41  if (cur == root)
  d=2   L1028  T=0 F=0  T=0 F=41  if ((ctxt->format == 1) &&
  d=2   L1032  T=0 F=0  T=33 F=8  if (cur->next != NULL) {
  d=2   L1041  T=0 F=0  T=8 F=0  if (cur->type == XML_ELEMENT_NODE) {
  d=2   L1042  T=0 F=0  T=8 F=0  if (ctxt->level > 0) ctxt->level--;
  d=2   L1043  T=0 F=0  T=8 F=0  if ((xmlIndentTreeOutput) && (ctxt->format == 1))
  d=2   L1043  T=0 F=0  T=0 F=8  if ((xmlIndentTreeOutput) && (ctxt->format == 1))
  d=2   L1050  T=0 F=0  T=0 F=8  if ((cur->ns != NULL) && (cur->ns->prefix != NULL)) {
  d=2   L1057  T=0 F=0  T=0 F=8  if (ctxt->format == 2)
  d=2   L1061  T=0 F=0  T=0 F=8  if (cur == unformattedNode) {
--- d=1  xmlsave.c:xmlDtdDumpOutput  (/src/libxml2/xmlsave.c:666-712) ---
  d=1   L 682  T=0 F=10  T=8 F=2  }  else if (dtd->SystemID != NULL) {
  d=1   L 686  T=0 F=10  T=10 F=0  if ((dtd->entities == NULL) && (dtd->elements == NULL) &&  <-- BLOCKER
  d=1   L 687  T=0 F=0  T=10 F=0  (dtd->attributes == NULL) && (dtd->notations == NULL) &&
  d=1   L 687  T=0 F=0  T=10 F=0  (dtd->attributes == NULL) && (dtd->notations == NULL) &&
  d=1   L 688  T=0 F=0  T=10 F=0  (dtd->pentities == NULL)) {
  d=1   L 697  T=0 F=10  T=0 F=0  if ((dtd->notations != NULL) && ((dtd->doc == NULL) ||
  d=1   L 706  T=12 F=10  T=0 F=0  for (cur = dtd->children; cur != NULL; cur = cur->next) {

[off-chain: 67 additional divergent branches across 8 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=2acf7739d273f6a1, size=712 bytes, fuzzer=naive_ctx, trial=1, discovered_at=24567s, mutation_op=BytesDeleteMutator,CrossoverReplaceMutator):
  0000: 55 53 2d 39 39 39 51 78 6c 6d 6e 6b 0b 0a 20 20   US-999Qxlmnk..  
  0010: 65 75 72 6c 2e 6e 37 37 37 ff 72 72 20 20 20 20   eurl.n777.rr    
  0020: 21 20 20 20 20 20 78 54 69 6e 6b 3a 74 79 70 65   !     xTink:type
  0030: 20 20 3c 21 41 54 54 4c 4a 53 54 20 7f ff 41 54     <!ATTLJST ..AT
Seed 2 (id=34f2310e21fd75b1, size=227 bytes, fuzzer=naive_ctx, trial=1, discovered_at=35162s, mutation_op=BytesDeleteMutator,TokenReplace):
  0000: 41 20 20 20 41 54 41 20 20 20 21 20 00 d0 01 18   A   ATA   ! ....
  0010: 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e   l\.<?xml version
  0020: 3c 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59   <"1.0"?>.<!DOCTY
  0030: 50 45 20 61 20 53 5b 3c 21 45 4c 45 4d 45 4e 54   PE a S[<!ELEMENT
Seed 3 (id=30e7c6920ffe0afc, size=394 bytes, fuzzer=naive_ctx, trial=1, discovered_at=37826s, mutation_op=ByteIncMutator,ByteInterestingMutator):
  0000: 41 20 20 20 41 54 41 20 20 00 00 03 e8 d0 01 00   A   ATA  .......
  0010: 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e   l\.<?xml version
  0020: 3c 22 31 2e 30 22 40 3e 0a 3c 21 44 4f 43 54 59   <"1.0"@>.<!DOCTY
  0030: 50 45 20 61 20 53 5b 3c 21 45 4c 45 4d 45 4e 54   PE a S[<!ELEMENT
Seed 4 (id=3deee1be1b4e3ddf, size=855 bytes, fuzzer=naive_ctx, trial=1, discovered_at=43249s, mutation_op=BytesCopyMutator,WordAddMutator,BytesRandSetMutator):
  0000: 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 33 2e 6f   'http://www.w3.o
  0010: 72 67 2f 31 39 39 39 2f 78 6c 69 6e 6b 27 0a 20   rg/1999/xlink'. 
  0020: 20 77 77 2e 77 33 2e 6f 72 67 2f 31 39 39 39 2f    ww.w3.org/1999/
  0030: 78 6c 69 6e 6b 27 0a 20 20 20 20 20 20 20 20 20   xlink'.         
Seed 5 (id=4238cb326403568b, size=655 bytes, fuzzer=naive_ctx, trial=1, discovered_at=51810s, mutation_op=ByteRandMutator,ByteDecMutator,ByteInterestingMutator,ByteRandMutator,ByteNegMutator,BytesInsertMutator):
  0000: ff 31 32 37 37 a6 ff 5c 0a 3c 3f 78 6d 6c 20 76   .1277..\.<?xml v
  0010: 65 01 73 69 ff ff ff ff 31 1e 3a 3a 3a 3a 3a 3a   e.si....1.::::::
  0020: 1e 1e 1e 1e 1e 1e 1e 1e 1e 2e 30 64 3f 41 41 41   ..........0d?AAA
  0030: 50 41 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20   PA>.<!DOCTYPE a 

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0069aaf9cd0a41e4, size=247 bytes, fuzzer=naive, trial=1, discovered_at=0s, mutation_op=ByteRandMutator,BytesRandInsertMutator,BytesDeleteMutator,BytesSwapMutator,ByteAddMutator,BytesCopyMutator,QwordAddMutator):
  0000: 4d 20 ff ff 74 64 73 2f 31 32 37 37 06 00 00 00   M ..tds/1277....
  0010: 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d   127772.xml\.<?xm
  0020: 7c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   | version="1.0"?
  0030: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
Seed 2 (id=01a47cb938f3863b, size=396 bytes, fuzzer=naive, trial=1, discovered_at=5s, mutation_op=WordAddMutator,BytesDeleteMutator,ByteInterestingMutator,ByteInterestingMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 65 66 3d 22 68 74   72.xml\.<?ef="ht
  0010: 74 70 3a 2f 2f 3d 22 31 2e 30 22 3f 3e 0a 3c 21   tp://="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 fc ff   DOCTYPE a SYST..
  0030: ff ff ff ff ff ff 2f 31 32 37 37 37 32 2e 64 74   ....../127772.dt
Seed 3 (id=027401dcbcf50bef, size=362 bytes, fuzzer=naive, trial=1, discovered_at=3483s, mutation_op=ByteRandMutator,DwordAddMutator,WordAddMutator,BytesInsertCopyMutator,BytesRandInsertMutator,ByteIncMutator):
  0000: 3d 22 74 74 74 70 3a 2f 2f 66 62 3e b6 b6 b6 b6   ="tttp://fb>....
  0010: b6 b6 b6 b6 61 6b 65 75 28 73 69 6d 3e 3e 3e 3e   ....akeu(sim>>>>
  0020: 20 d6 23 46 49 58 45 44 30 27 73 69 6d 70 6c 65    .#FIXED0'simple
  0030: 27 0a 73 69 6d 70 6c 65 27 0a 20 20 20 20 20 20   '.simple'.      
Seed 4 (id=00c0385729a5223c, size=537 bytes, fuzzer=naive, trial=1, discovered_at=5238s, mutation_op=BytesInsertCopyMutator,BytesInsertCopyMutator,BytesInsertMutator,BytesInsertCopyMutator,BytesRandInsertMutator,ByteFlipMutator):
  0000: 45 44 20 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77   ED 'http://www.w
  0010: c4 2e 6f 72 88 2f 31 39 39 39 2f 78 6c 69 6e 6b   ..or./1999/xlink
  0020: 6e 65 8b 22 3e 2f 2f 2f 62 20 74 65 78 6d 6c 5c   ne.">///b texml\
  0030: 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22   .<?xml version="
Seed 5 (id=01693899945ec61c, size=165 bytes, fuzzer=naive, trial=1, discovered_at=7599s, mutation_op=BitFlipMutator,ByteAddMutator,BytesDeleteMutator):
  0000: 39 2f 20 74 74 70 3a 2f 2f 77 77 77 2e 77 33 2e   9/ ttp://www.w3.
  0010: 6f 72 28 62 2a 29 3e 0a 0a 4c 45 4d 45 4e 54 20   or(b*)>..LEMENT 
  0020: 61 20 28 62 2a 2c 2c 2c 20 20 20 20 20 20 20 20   a (b*,,,        
  0030: 20 20 20 62 20 28 23 af 43 39 2f 2c 74 27 0a 20      b (#.C9/,t'. 


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0004  41(A)x3 37(7)x2 00(.)x2 39(9)x1 +2u  74(t)x6 68(h)x2 6d(m)x1 6b(k)x1     DIFFER
   0x0007  20( )x3 5c(\)x2 00(.)x2 78(x)x1 +2u  2f(/)x6 70(p)x2 0a(.)x1 72(r)x1     PARTIAL
   0x003f  54(T)x4 20( )x4 3f(?)x1 39(9)x1     20( )x3 59(Y)x1 74(t)x1 22(")x1 +4u  PARTIAL
==== MECHANISM CONTEXT (involved fuzzers only) ====
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_8630.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 8630,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 8630 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 8630 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 8630 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).