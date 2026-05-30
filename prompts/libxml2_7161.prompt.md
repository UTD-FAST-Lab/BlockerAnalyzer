==== BLOCKER ====
Target: libxml2
Branch ID: 7161
Location: /src/libxml2/valid.c:4314:9
Enclosing function: xmlValidateElementDecl
Source line:     if (elem == NULL) return(1);
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  REFERENCE
cmplog                           1        9          0  loser (grimoire_structural vs grimoire)
value_profile                    4        6          0  REFERENCE
value_profile_cmplog             0       10          0  REFERENCE
naive_ctx                        4        6          0  REFERENCE
naive_ngram4                     3        7          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        2        8          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         8        2          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=12.10h  loser=21.30h
  avg hitcount on branch: winner=9  loser=0
  prob_div=0.70  dur_div=9.20h  hit_div=9
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7161/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlValidateElementDecl (/src/libxml2/valid.c:4308-4401) ---
[ ]  4306  int
[ ]  4307  xmlValidateElementDecl(xmlValidCtxtPtr ctxt, xmlDocPtr doc,
[B]  4308                         xmlElementPtr elem) {
[B]  4309      int ret = 1;
[B]  4310      xmlElementPtr tst;
[ ]  4311  
[B]  4312      CHECK_DTD;
[ ]  4313  
[B]  4314      if (elem == NULL) return(1); <-- BLOCKER
[ ]  4315  
[ ]  4316  #if 0
[ ]  4317  #ifdef LIBXML_REGEXP_ENABLED
[ ]  4318      /* Build the regexp associated to the content model */
[ ]  4319      ret = xmlValidBuildContentModel(ctxt, elem);
[ ]  4320  #endif
[ ]  4321  #endif
[ ]  4322  
[ ]  4323      /* No Duplicate Types */
[B]  4324      if (elem->etype == XML_ELEMENT_TYPE_MIXED) {
[L]  4325  	xmlElementContentPtr cur, next;
[L]  4326          const xmlChar *name;
[ ]  4327  
[L]  4328  	cur = elem->content;
[L]  4329  	while (cur != NULL) {
[L]  4330  	    if (cur->type != XML_ELEMENT_CONTENT_OR) break;
[ ]  4331  	    if (cur->c1 == NULL) break;
[ ]  4332  	    if (cur->c1->type == XML_ELEMENT_CONTENT_ELEMENT) {
[ ]  4333  		name = cur->c1->name;
[ ]  4334  		next = cur->c2;
[ ]  4335  		while (next != NULL) {
[ ]  4336  		    if (next->type == XML_ELEMENT_CONTENT_ELEMENT) {
[ ]  4337  		        if ((xmlStrEqual(next->name, name)) &&
[ ]  4338  			    (xmlStrEqual(next->prefix, cur->c1->prefix))) {
[ ]  4339  			    if (cur->c1->prefix == NULL) {
[ ]  4340  				xmlErrValidNode(ctxt, (xmlNodePtr) elem, XML_DTD_CONTENT_ERROR,
[ ]  4341  		   "Definition of %s has duplicate references of %s\n",
[ ]  4342  				       elem->name, name, NULL);
[ ]  4343  			    } else {
[ ]  4344  				xmlErrValidNode(ctxt, (xmlNodePtr) elem, XML_DTD_CONTENT_ERROR,
[ ]  4345  		   "Definition of %s has duplicate references of %s:%s\n",
[ ]  4346  				       elem->name, cur->c1->prefix, name);
[ ]  4347  			    }
[ ]  4348  			    ret = 0;
[ ]  4349  			}
[ ]  4350  			break;
[ ]  4351  		    }
[ ]  4352  		    if (next->c1 == NULL) break;
[ ]  4353  		    if (next->c1->type != XML_ELEMENT_CONTENT_ELEMENT) break;
[ ]  4354  		    if ((xmlStrEqual(next->c1->name, name)) &&
[ ]  4355  		        (xmlStrEqual(next->c1->prefix, cur->c1->prefix))) {
[ ]  4356  			if (cur->c1->prefix == NULL) {
[ ]  4357  			    xmlErrValidNode(ctxt, (xmlNodePtr) elem, XML_DTD_CONTENT_ERROR,
[ ]  4358  	       "Definition of %s has duplicate references to %s\n",
[ ]  4359  				   elem->name, name, NULL);
[ ]  4360  			} else {
[ ]  4361  			    xmlErrValidNode(ctxt, (xmlNodePtr) elem, XML_DTD_CONTENT_ERROR,
[ ]  4362  	       "Definition of %s has duplicate references to %s:%s\n",
[ ]  4363  				   elem->name, cur->c1->prefix, name);
[ ]  4364  			}
[ ]  4365  			ret = 0;
[ ]  4366  		    }
[ ]  4367  		    next = next->c2;
[ ]  4368  		}
[ ]  4369  	    }
[ ]  4370  	    cur = cur->c2;
[ ]  4371  	}
[L]  4372      }
[ ]  4373  
[ ]  4374      /* VC: Unique Element Type Declaration */
[B]  4375      tst = xmlGetDtdElementDesc(doc->intSubset, elem->name);
[B]  4376      if ((tst != NULL ) && (tst != elem) &&
[B]  4377  	((tst->prefix == elem->prefix) ||
[ ]  4378  	 (xmlStrEqual(tst->prefix, elem->prefix))) &&
[B]  4379  	(tst->etype != XML_ELEMENT_TYPE_UNDEFINED)) {
[ ]  4380  	xmlErrValidNode(ctxt, (xmlNodePtr) elem, XML_DTD_ELEM_REDEFINED,
[ ]  4381  	                "Redefinition of element %s\n",
[ ]  4382  		       elem->name, NULL, NULL);
[ ]  4383  	ret = 0;
[ ]  4384      }
[B]  4385      tst = xmlGetDtdElementDesc(doc->extSubset, elem->name);
[B]  4386      if ((tst != NULL ) && (tst != elem) &&
[B]  4387  	((tst->prefix == elem->prefix) ||
[ ]  4388  	 (xmlStrEqual(tst->prefix, elem->prefix))) &&
[B]  4389  	(tst->etype != XML_ELEMENT_TYPE_UNDEFINED)) {
[ ]  4390  	xmlErrValidNode(ctxt, (xmlNodePtr) elem, XML_DTD_ELEM_REDEFINED,
[ ]  4391  	                "Redefinition of element %s\n",
[ ]  4392  		       elem->name, NULL, NULL);
[ ]  4393  	ret = 0;
[ ]  4394      }
[ ]  4395      /* One ID per Element Type
[ ]  4396       * already done when registering the attribute
[ ]  4397      if (xmlScanIDAttributeDecl(ctxt, elem) > 1) {
[ ]  4398  	ret = 0;
[ ]  4399      } */
[B]  4400      return(ret);
[B]  4401  }

--- Caller (1 hop): xmlSAX2ElementDecl (/src/libxml2/SAX2.c:772-807, calls xmlValidateElementDecl at line 805) (full body — short) ---
[B]   772  {
[B]   773      xmlParserCtxtPtr ctxt = (xmlParserCtxtPtr) ctx;
[B]   774      xmlElementPtr elem = NULL;
[ ]   775  
[ ]   776      /* Avoid unused variable warning if features are disabled. */
[B]   777      (void) elem;
[ ]   778  
[B]   779      if ((ctxt == NULL) || (ctxt->myDoc == NULL))
[ ]   780          return;
[ ]   781  
[ ]   782  #ifdef DEBUG_SAX
[ ]   783      xmlGenericError(xmlGenericErrorContext,
[ ]   784                      "SAX.xmlSAX2ElementDecl(%s, %d, ...)\n", name, type);
[ ]   785  #endif
[ ]   786  
[B]   787      if (ctxt->inSubset == 1)
[ ]   788          elem = xmlAddElementDecl(&ctxt->vctxt, ctxt->myDoc->intSubset,
[ ]   789                                   name, (xmlElementTypeVal) type, content);
[B]   790      else if (ctxt->inSubset == 2)
[B]   791          elem = xmlAddElementDecl(&ctxt->vctxt, ctxt->myDoc->extSubset,
[B]   792                                   name, (xmlElementTypeVal) type, content);
[ ]   793      else {
[ ]   794          xmlFatalErrMsg(ctxt, XML_ERR_INTERNAL_ERROR,
[ ]   795  	     "SAX.xmlSAX2ElementDecl(%s) called while not in subset\n",
[ ]   796  	               name, NULL);
[ ]   797          return;
[ ]   798      }
[B]   799  #ifdef LIBXML_VALID_ENABLED
[B]   800      if (elem == NULL)
[W]   801          ctxt->valid = 0;
[B]   802      if (ctxt->validate && ctxt->wellFormed &&
[B]   803          ctxt->myDoc && ctxt->myDoc->intSubset)
[B]   804          ctxt->valid &=
[B]   805              xmlValidateElementDecl(&ctxt->vctxt, ctxt->myDoc, elem); <-- CALL
[B]   806  #endif /* LIBXML_VALID_ENABLED */
[B]   807  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlSAX2ElementDecl  (/src/libxml2/SAX2.c:772-807, calls xmlValidateElementDecl at line 805)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      96       534  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      46       388  xmlGetDtdElementDesc  (/src/libxml2/valid.c:3250-3267)
      48       195  xmlGetDtdAttrDesc  (/src/libxml2/valid.c:3372-3393)
      24       162  xmlGetDtdQElementDesc  (/src/libxml2/valid.c:3349-3357)
      24       155  valid.c:xmlFreeElement  (/src/libxml2/valid.c:1382-1395)
      24       155  valid.c:xmlFreeElementTableEntry  (/src/libxml2/valid.c:1623-1625)
      19       136  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      19       136  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
      39       155  xmlNewDocElementContent  (/src/libxml2/valid.c:902-961)
      45       161  xmlFreeDocElementContent  (/src/libxml2/valid.c:1082-1138)
       9       121  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
      39       149  xmlSAX2ElementDecl  (/src/libxml2/SAX2.c:772-807)
      39       149  xmlAddElementDecl  (/src/libxml2/valid.c:1414-1620)
      16       120  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
      39       143  xmlValidateElementDecl  (/src/libxml2/valid.c:4308-4401)  <-- enclosing
... (46 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlSAX2ElementDecl  (/src/libxml2/SAX2.c:772-807) ---
  d=2   L 779  T=0 F=39  T=0 F=149  if ((ctxt == NULL) || (ctxt->myDoc == NULL))
  d=2   L 779  T=0 F=39  T=0 F=149  if ((ctxt == NULL) || (ctxt->myDoc == NULL))
  d=2   L 787  T=0 F=39  T=0 F=149  if (ctxt->inSubset == 1)
  d=2   L 790  T=39 F=0  T=149 F=0  else if (ctxt->inSubset == 2)
  d=2   L 800  T=21 F=18  T=0 F=149  if (elem == NULL)
  d=2   L 802  T=39 F=0  T=149 F=0  if (ctxt->validate && ctxt->wellFormed &&
  d=2   L 802  T=39 F=0  T=143 F=6  if (ctxt->validate && ctxt->wellFormed &&
  d=2   L 803  T=39 F=0  T=143 F=0  ctxt->myDoc && ctxt->myDoc->intSubset)
  d=2   L 803  T=39 F=0  T=143 F=0  ctxt->myDoc && ctxt->myDoc->intSubset)
--- d=1  xmlValidateElementDecl  (/src/libxml2/valid.c:4308-4401) ---
  d=1   L4314  T=21 F=18  T=0 F=143  if (elem == NULL) return(1);  <-- BLOCKER
  d=1   L4324  T=0 F=18  T=60 F=83  if (elem->etype == XML_ELEMENT_TYPE_MIXED) {
  d=1   L4329  T=0 F=0  T=60 F=0  while (cur != NULL) {
  d=1   L4330  T=0 F=0  T=60 F=0  if (cur->type != XML_ELEMENT_CONTENT_OR) break;
  d=1   L4376  T=0 F=18  T=0 F=143  if ((tst != NULL ) && (tst != elem) &&
  d=1   L4386  T=18 F=0  T=143 F=0  if ((tst != NULL ) && (tst != elem) &&
  d=1   L4386  T=0 F=18  T=0 F=143  if ((tst != NULL ) && (tst != elem) &&

[off-chain: 811 additional divergent branches across 60 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=96a40d5532ded328, size=400 bytes, fuzzer=grimoire, trial=1, discovered_at=5227s, mutation_op=BytesInsertMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c   ersion="1.0"?>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 74 74 74 74 74 74   !DOCTYPE atttttt
  0030: 74 74 74 74 20 53 59 53 54 45 4d 20 22 64 74 64   tttt SYSTEM "dtd
Seed 2 (id=5d5a87c006c99a11, size=400 bytes, fuzzer=grimoire, trial=1, discovered_at=10759s, mutation_op=I2SRandReplace,I2SRandReplace):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76   772.xml\.<?xml v
  0010: 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c   ersion="1.0"?>.<
  0020: 21 44 4f 43 54 59 50 45 20 61 74 74 74 74 74 74   !DOCTYPE atttttt
  0030: 74 74 74 74 20 53 59 53 54 45 4d 20 22 64 74 64   tttt SYSTEM "dtd
Seed 3 (id=6311f928da701e6e, size=197 bytes, fuzzer=grimoire, trial=1, discovered_at=36639s, mutation_op=BytesCopyMutator):
  0000: 56 00 6d 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   V.ml\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 5c 0a 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74   \.dtds/127772.dt
Seed 4 (id=9607baa0b21b5833, size=213 bytes, fuzzer=grimoire, trial=1, discovered_at=79923s, mutation_op=BytesExpandMutator):
  0000: 56 00 6d 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f   V.ml\.<?l ?><!DO
  0010: 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22 64   CTYPEa SYSTEM "d
  0020: 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22 3e   tds/127772.dtd">
  0030: 5c 0a 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74   \.dtds/127772.dt

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=08e581afd1b4edda, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=2s, mutation_op=QwordAddMutator,BytesDeleteMutator,BytesInsertMutator):
  0000: 37 58 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7X72.xml\.<?xml 
  0010: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e   EM "dtds/127772.
Seed 2 (id=4002ce2fbfac9b23, size=323 bytes, fuzzer=cmplog, trial=1, discovered_at=11s, mutation_op=BytesInsertCopyMutator,ByteDecMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7772.xml\.<?xml 
  0010: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e   EM "dtds/127772.
Seed 3 (id=1c65f70d71c9b113, size=370 bytes, fuzzer=cmplog, trial=1, discovered_at=241s, mutation_op=BytesSetMutator,BytesSetMutator,BytesExpandMutator):
  0000: 3d 3d 3d 3d 3d 32 37 37 37 32 2e 20 20 20 5c 0a   =====27772.   \.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=0923733cbce2bef5, size=381 bytes, fuzzer=cmplog, trial=1, discovered_at=269s, mutation_op=QwordAddMutator,BytesInsertCopyMutator,BitFlipMutator,WordInterestingMutator,BytesSwapMutator):
  0000: 74 70 3a 2f 2f 77 77 77 2e 77 33 2e 6f 72 67 2f   tp://www.w3.org/
  0010: 31 39 3d 39 2f 78 6c 69 37 37 37 32 2e 78 6d 6c   19=9/xli7772.xml
  0020: 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d   \.<?xml version=
  0030: 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50   "1.0"?>.<!DOCTYP
Seed 5 (id=001c8c9d4510710d, size=248 bytes, fuzzer=cmplog, trial=1, discovered_at=411s, mutation_op=ByteNegMutator,BytesCopyMutator,BytesInsertMutator,ByteIncMutator,BytesSwapMutator,BytesDeleteMutator,TokenReplace):
  0000: 5f 5f 5f 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ___.127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  37(7)x2 56(V)x2                     37(7)x11 32(2)x3 31(1)x3 f9(.)x3 +8u  PARTIAL
   0x0001  37(7)x2 00(.)x2                     37(7)x5 32(2)x5 2e(.)x3 22(")x2 +13u  PARTIAL
   0x0002  32(2)x2 6d(m)x2                     37(7)x6 32(2)x4 78(x)x3 3d(=)x2 +11u  PARTIAL
   0x0003  2e(.)x2 6c(l)x2                     37(7)x5 6d(m)x4 00(.)x3 78(x)x3 +9u  PARTIAL
   0x0004  78(x)x2 5c(\)x2                     31(1)x5 37(7)x5 6d(m)x4 6c(l)x3 +9u  PARTIAL
   0x0005  6d(m)x2 0a(.)x2                     32(2)x8 6d(m)x4 6c(l)x3 5c(\)x3 +6u  PARTIAL
   0x0006  6c(l)x2 3c(<)x2                     37(7)x6 6d(m)x4 0a(.)x3 6c(l)x3 +10u  PARTIAL
   0x0007  5c(\)x2 3f(?)x2                     37(7)x8 6c(l)x3 3c(<)x3 5c(\)x3 +9u  PARTIAL
   0x0008  0a(.)x2 6c(l)x2                     37(7)x7 5c(\)x3 3f(?)x3 2f(/)x3 +8u  PARTIAL
   0x0009  3c(<)x2 20( )x2                     32(2)x5 0a(.)x3 78(x)x3 2f(/)x3 +9u  PARTIAL
   0x000a  3f(?)x4                             2e(.)x5 6d(m)x4 3c(<)x3 3f(?)x3 +10u  PARTIAL
   0x000b  78(x)x2 3e(>)x2                     78(x)x7 3f(?)x3 6c(l)x3 6d(m)x2 +12u  PARTIAL
   0x000c  6d(m)x2 3c(<)x2                     6d(m)x7 20( )x5 78(x)x3 6c(l)x2 +11u  PARTIAL
   0x000d  6c(l)x2 21(!)x2                     6c(l)x9 6d(m)x3 20( )x3 76(v)x3 +11u  PARTIAL
   0x000e  20( )x2 44(D)x2                     5c(\)x7 65(e)x4 6c(l)x3 20( )x3 +11u  PARTIAL
   0x000f  76(v)x2 4f(O)x2                     0a(.)x7 20( )x3 72(r)x3 76(v)x3 +12u  PARTIAL
   0x0010  65(e)x2 43(C)x2                     3c(<)x7 76(v)x3 73(s)x3 65(e)x3 +12u  PARTIAL
   0x0011  72(r)x2 54(T)x2                     3f(?)x7 65(e)x3 73(s)x3 69(i)x3 +11u  PARTIAL
   0x0012  73(s)x2 59(Y)x2                     78(x)x8 6f(o)x4 72(r)x3 73(s)x3 +10u  PARTIAL
   0x0013  69(i)x2 50(P)x2                     6d(m)x8 73(s)x3 6e(n)x3 69(i)x3 +11u  PARTIAL
   0x0014  6f(o)x2 45(E)x2                     6c(l)x8 69(i)x3 3d(=)x3 6f(o)x3 +11u  PARTIAL
   0x0015  6e(n)x2 61(a)x2                     20( )x7 6f(o)x3 22(")x3 6e(n)x3 +10u  PARTIAL
   0x0016  3d(=)x2 20( )x2                     76(v)x7 6e(n)x3 31(1)x3 3d(=)x3 +11u  PARTIAL
   0x0017  22(")x2 53(S)x2                     65(e)x7 2e(.)x4 3d(=)x3 22(")x3 +10u  PARTIAL
   0x0018  31(1)x2 59(Y)x2                     72(r)x7 22(")x3 30(0)x3 31(1)x3 +12u  PARTIAL
   0x0019  2e(.)x2 53(S)x2                     73(s)x7 2e(.)x4 31(1)x3 22(")x3 +11u  PARTIAL
   0x001a  30(0)x2 54(T)x2                     69(i)x7 22(")x4 2e(.)x3 3f(?)x3 +11u  PARTIAL
   0x001b  22(")x2 45(E)x2                     6f(o)x7 22(")x4 30(0)x3 3f(?)x3 +9u  PARTIAL
   0x001c  3f(?)x2 4d(M)x2                     6e(n)x7 0a(.)x4 22(")x3 2e(.)x3 +10u  PARTIAL
   0x001d  3e(>)x2 20( )x2                     3d(=)x7 3c(<)x4 3f(?)x3 3e(>)x3 +10u  PARTIAL
   0x001e  0a(.)x2 22(")x2                     22(")x9 3e(>)x4 21(!)x3 0a(.)x3 +10u  PARTIAL
   0x001f  3c(<)x2 64(d)x2                     31(1)x7 0a(.)x4 21(!)x3 44(D)x3 +10u  PARTIAL
   0x0020  21(!)x2 74(t)x2                     2e(.)x7 3c(<)x3 4f(O)x3 21(!)x3 +10u  PARTIAL
   0x0021  44(D)x2 64(d)x2                     30(0)x7 21(!)x3 0a(.)x3 43(C)x3 +10u  PARTIAL
   0x0022  4f(O)x2 73(s)x2                     22(")x7 44(D)x3 3c(<)x3 54(T)x3 +11u  PARTIAL
   0x0023  43(C)x2 2f(/)x2                     3f(?)x8 4f(O)x3 59(Y)x3 43(C)x3 +11u  PARTIAL
   0x0024  54(T)x2 31(1)x2                     3e(>)x8 43(C)x3 50(P)x3 54(T)x3 +10u  PARTIAL
   0x0025  59(Y)x2 32(2)x2                     0a(.)x7 54(T)x3 45(E)x3 59(Y)x3 +11u  PARTIAL
   0x0026  50(P)x2 37(7)x2                     3c(<)x7 20( )x4 59(Y)x3 50(P)x3 +11u  PARTIAL
   0x0027  45(E)x2 37(7)x2                     21(!)x8 50(P)x3 20( )x3 61(a)x3 +9u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7161.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7161,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7161 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7161 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7161 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).