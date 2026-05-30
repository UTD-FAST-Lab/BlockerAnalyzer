==== BLOCKER ====
Target: libxml2
Branch ID: 6948
Location: /src/libxml2/tree.c:6182:7
Enclosing function: xmlSearchNs
Source line: 		if ((cur->prefix == NULL) && (nameSpace == NULL) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (value_profile vs value_profile); loser (ctx_coverage vs naive_ctx)
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog); loser (grimoire_structural vs grimoire)
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog            10        0          0  winner (value_profile vs cmplog)
naive_ctx                        8        2          0  winner (ctx_coverage vs naive)
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             3        7          0  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire', 'naive', 'naive_ctx', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (4) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.90h  loser=19.50h
  avg hitcount on branch: winner=15  loser=2
  prob_div=0.80  dur_div=11.60h  hit_div=13
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002
--- Pair 2: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.70h  loser=19.50h
  avg hitcount on branch: winner=2199  loser=2
  prob_div=0.80  dur_div=12.80h  hit_div=2197
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002
--- Pair 3: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=13.20h  loser=20.70h
  avg hitcount on branch: winner=289  loser=8
  prob_div=0.60  dur_div=7.50h  hit_div=281
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002
--- Pair 4: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 35  (naive_ctx vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=12.40h  loser=20.70h
  avg hitcount on branch: winner=144  loser=8
  prob_div=0.60  dur_div=8.30h  hit_div=136
  subject-level: delta_AUC=21345840.0  p_AUC=0.0452  delta_Final=464.2  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6948/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlSearchNs (/src/libxml2/tree.c:6134-6207) ---
[ ]  6132   */
[ ]  6133  xmlNsPtr
[B]  6134  xmlSearchNs(xmlDocPtr doc, xmlNodePtr node, const xmlChar *nameSpace) {
[ ]  6135  
[B]  6136      xmlNsPtr cur;
[B]  6137      const xmlNode *orig = node;
[ ]  6138  
[B]  6139      if ((node == NULL) || (node->type == XML_NAMESPACE_DECL)) return(NULL);
[B]  6140      if ((nameSpace != NULL) &&
[B]  6141  	(xmlStrEqual(nameSpace, (const xmlChar *)"xml"))) {
[ ]  6142  	if ((doc == NULL) && (node->type == XML_ELEMENT_NODE)) {
[ ]  6143  	    /*
[ ]  6144  	     * The XML-1.0 namespace is normally held on the root
[ ]  6145  	     * element. In this case exceptionally create it on the
[ ]  6146  	     * node element.
[ ]  6147  	     */
[ ]  6148  	    cur = (xmlNsPtr) xmlMalloc(sizeof(xmlNs));
[ ]  6149  	    if (cur == NULL) {
[ ]  6150  		xmlTreeErrMemory("searching namespace");
[ ]  6151  		return(NULL);
[ ]  6152  	    }
[ ]  6153  	    memset(cur, 0, sizeof(xmlNs));
[ ]  6154  	    cur->type = XML_LOCAL_NAMESPACE;
[ ]  6155  	    cur->href = xmlStrdup(XML_XML_NAMESPACE);
[ ]  6156  	    cur->prefix = xmlStrdup((const xmlChar *)"xml");
[ ]  6157  	    cur->next = node->nsDef;
[ ]  6158  	    node->nsDef = cur;
[ ]  6159  	    return(cur);
[ ]  6160  	}
[ ]  6161  	if (doc == NULL) {
[ ]  6162  	    doc = node->doc;
[ ]  6163  	    if (doc == NULL)
[ ]  6164  		return(NULL);
[ ]  6165  	}
[ ]  6166  	/*
[ ]  6167  	* Return the XML namespace declaration held by the doc.
[ ]  6168  	*/
[ ]  6169  	if (doc->oldNs == NULL)
[ ]  6170  	    return(xmlTreeEnsureXMLDecl(doc));
[ ]  6171  	else
[ ]  6172  	    return(doc->oldNs);
[ ]  6173      }
[B]  6174      while (node != NULL) {
[B]  6175  	if ((node->type == XML_ENTITY_REF_NODE) ||
[B]  6176  	    (node->type == XML_ENTITY_NODE) ||
[B]  6177  	    (node->type == XML_ENTITY_DECL))
[ ]  6178  	    return(NULL);
[B]  6179  	if (node->type == XML_ELEMENT_NODE) {
[B]  6180  	    cur = node->nsDef;
[B]  6181  	    while (cur != NULL) {
[B]  6182  		if ((cur->prefix == NULL) && (nameSpace == NULL) && <-- BLOCKER
[B]  6183  		    (cur->href != NULL))
[W]  6184  		    return(cur);
[B]  6185  		if ((cur->prefix != NULL) && (nameSpace != NULL) &&
[B]  6186  		    (cur->href != NULL) &&
[B]  6187  		    (xmlStrEqual(cur->prefix, nameSpace)))
[L]  6188  		    return(cur);
[B]  6189  		cur = cur->next;
[B]  6190  	    }
[B]  6191  	    if (orig != node) {
[B]  6192  	        cur = node->ns;
[B]  6193  	        if (cur != NULL) {
[W]  6194  		    if ((cur->prefix == NULL) && (nameSpace == NULL) &&
[W]  6195  		        (cur->href != NULL))
[W]  6196  		        return(cur);
[W]  6197  		    if ((cur->prefix != NULL) && (nameSpace != NULL) &&
[W]  6198  		        (cur->href != NULL) &&
[W]  6199  		        (xmlStrEqual(cur->prefix, nameSpace)))
[ ]  6200  		        return(cur);
[W]  6201  	        }
[B]  6202  	    }
[B]  6203  	}
[B]  6204  	node = node->parent;
[B]  6205      }
[B]  6206      return(NULL);
[B]  6207  }

--- Caller (1 hop): xmlSAX2StartElement (/src/libxml2/SAX2.c:1603-1806, calls xmlSearchNs at line 1737) (±10 around call site) ---
[ ]  1727  
[B]  1728  		att = atts[i++];
[B]  1729  		value = atts[i++];
[B]  1730  	    }
[B]  1731          }
[ ]  1732  
[ ]  1733          /*
[ ]  1734           * Search the namespace, note that since the attributes have been
[ ]  1735           * processed, the local namespaces are available.
[ ]  1736           */
[B]  1737          ns = xmlSearchNs(ctxt->myDoc, ret, prefix); <-- CALL
[B]  1738          if ((ns == NULL) && (parent != NULL))
[B]  1739              ns = xmlSearchNs(ctxt->myDoc, parent, prefix);
[B]  1740          if ((prefix != NULL) && (ns == NULL)) {
[L]  1741              ns = xmlNewNs(ret, NULL, prefix);
[L]  1742              xmlNsWarnMsg(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[L]  1743                           "Namespace prefix %s is not defined\n",
[L]  1744                           prefix, NULL);
[L]  1745          }
[ ]  1746  
[ ]  1747          /*

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  relaxng.c:xmlRelaxNGCleanupTree  (/src/libxml2/relaxng.c:7043-7472, calls xmlSearchNs at line 7299)
hop 2  xmlTextReaderGetAttribute  (/src/libxml2/xmlreader.c:2317-2374, calls xmlSearchNs at line 2365)
hop 3  relaxng.c:xmlRelaxNGCleanupDoc  (/src/libxml2/relaxng.c:7486-7500, calls relaxng.c:xmlRelaxNGCleanupTree at line 7498)
hop 4  relaxng.c:xmlRelaxNGLoadExternalRef  (/src/libxml2/relaxng.c:1953-2027, calls relaxng.c:xmlRelaxNGCleanupDoc at line 2018)
hop 4  relaxng.c:xmlRelaxNGLoadInclude  (/src/libxml2/relaxng.c:1605-1765, calls relaxng.c:xmlRelaxNGCleanupDoc at line 1681)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     200         0  xmlSetNs  (/src/libxml2/tree.c:806-817)
     193        35  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)
     140         5  xmlNewNode  (/src/libxml2/tree.c:2259-2287)
     140         5  xmlNewDocNode  (/src/libxml2/tree.c:2352-2369)
     112        11  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591)
      99         8  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438)
      85        12  xmlreader.c:xmlTextReaderStartElementNs  (/src/libxml2/xmlreader.c:664-682)
      76        19  xmlBuildQName  (/src/libxml2/tree.c:223-247)
      50         3  xmlGetLastChild  (/src/libxml2/tree.c:3542-3551)
      50        12  xmlSAX2IgnorableWhitespace  (/src/libxml2/SAX2.c:2698-2704)
       2        20  SAX2.c:xmlSAX2AttributeNs  (/src/libxml2/SAX2.c:1996-2199)
       4        22  xmlSAX2EndElementNs  (/src/libxml2/SAX2.c:2476-2502)
      21         6  xmlAddSibling  (/src/libxml2/tree.c:3248-3311)
      12         0  xmlSAX2ProcessingInstruction  (/src/libxml2/SAX2.c:2717-2769)
      12         0  xmlNewDocPI  (/src/libxml2/tree.c:2194-2228)
... (13 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  xmlSearchNs  (/src/libxml2/tree.c:6134-6207) ---
  d=1   L6139  T=42 F=455  T=0 F=309  if ((node == NULL) || (node->type == XML_NAMESPACE_DECL))...
  d=1   L6141  T=0 F=7  T=0 F=147  (xmlStrEqual(nameSpace, (const xmlChar *)"xml"))) {
  d=1   L6182  T=735 F=0  T=0 F=180  if ((cur->prefix == NULL) && (nameSpace == NULL) &&  <-- BLOCKER
  d=1   L6182  T=723 F=12  T=0 F=0  if ((cur->prefix == NULL) && (nameSpace == NULL) &&  <-- BLOCKER
  d=1   L6183  T=161 F=562  T=0 F=0  (cur->href != NULL))
  d=1   L6185  T=0 F=574  T=180 F=0  if ((cur->prefix != NULL) && (nameSpace != NULL) &&
  d=1   L6185  T=0 F=0  T=107 F=73  if ((cur->prefix != NULL) && (nameSpace != NULL) &&
  d=1   L6186  T=0 F=0  T=23 F=84  (cur->href != NULL) &&
  d=1   L6187  T=0 F=0  T=20 F=3  (xmlStrEqual(cur->prefix, nameSpace)))
  d=1   L6193  T=110 F=541  T=0 F=438  if (cur != NULL) {
  d=1   L6194  T=110 F=0  T=0 F=0  if ((cur->prefix == NULL) && (nameSpace == NULL) &&
  d=1   L6194  T=102 F=8  T=0 F=0  if ((cur->prefix == NULL) && (nameSpace == NULL) &&
  d=1   L6195  T=102 F=0  T=0 F=0  (cur->href != NULL))
  d=1   L6197  T=0 F=8  T=0 F=0  if ((cur->prefix != NULL) && (nameSpace != NULL) &&

[off-chain: 575 additional divergent branches across 56 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=67f9a08bf1c7e0c1, size=362 bytes, fuzzer=grimoire, trial=1, discovered_at=9482s, mutation_op=I2SRandReplace,I2SRandReplace,I2SRandReplace):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
Seed 2 (id=378eaab990ad2f1b, size=139 bytes, fuzzer=grimoire, trial=1, discovered_at=13781s, mutation_op=GrimoireRandomDeleteMutator,GrimoireExtensionMutator):
  0000: 09 96 98 00 06 00 6d 6c 5c 0a 3c 3f 6c 20 3f 3e   ......ml\.<?l ?>
  0010: 3c 21 44 4f 43 54 59 50 45 61 20 53 59 53 54 45   <!DOCTYPEa SYSTE
  0020: 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64   M "dtds/127772.d
  0030: 74 64 22 3e 3c 61 3e 3c 62 3c 62 20 6b 3a 66 3d   td"><a><b<b k:f=
Seed 3 (id=c23096ec9dae2ed4, size=389 bytes, fuzzer=grimoire, trial=1, discovered_at=18912s, mutation_op=ByteNegMutator,BytesExpandMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 20 61 20 53 59 53 54 45 4d   DOCTYPE a SYSTEM
  0030: 20 22 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74    "dtds/127772.dt
Seed 4 (id=ea8c1594a6141f7c, size=924 bytes, fuzzer=naive_ctx, trial=1, discovered_at=18944s, mutation_op=CrossoverInsertMutator,ByteFlipMutator,WordAddMutator,BytesInsertCopyMutator):
  0000: 3d 22 68 3d 22 68 74 74 70 3a 2f 2f 66 61 6b 2f   ="h="http://fak/
  0010: 31 39 39 39 2f 65 75 72 6c 2e 6e 65 74 22 3e 62   1999/eurl.net">b
  0020: 3f 74 65 78 74 3c 2f 62 3e 0a 3c 2f 61 3e 67 2f   ?text</b>.</a>g/
  0030: 31 39 39 39 2f 78 6c 69 6e 73 27 0a 20 20 20 20   1999/xlins'.    
Seed 5 (id=1b39186f122ab058, size=258 bytes, fuzzer=value_profile, trial=2, discovered_at=22387s, mutation_op=BitFlipMutator,BytesDeleteMutator,TokenReplace,DwordInterestingMutator,ByteAddMutator):
  0000: ef ef 2e 78 6d 6c 5c 0a 3c 6c df 76 62 20 78 6d   ...xml\.<l.vb xm
  0010: 6c 6e 73 3d 22 31 2e 30 f1 ef ef ef ef 9b ff ff   lns="1.0........
  0020: ff ff ff 0a ff 22 3e 0a 0a 3c 61 3e 0a 20 20 3c   .....">..<a>.  <
  0030: 62 0a 3c 61 74 74 74 74 74 50 45 20 61 20 53 59   b.<atttttPE a SY

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=8c7bd7ba6dfb824c, size=368 bytes, fuzzer=naive, trial=1):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=671269cb256ddf38, size=289 bytes, fuzzer=naive, trial=1, discovered_at=58s, mutation_op=BytesDeleteMutator,ByteAddMutator):
  0000: 0d 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=761f2909b204e1a3, size=397 bytes, fuzzer=naive, trial=1, discovered_at=110s, mutation_op=BytesInsertCopyMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=60696a628f69cc2b, size=358 bytes, fuzzer=naive, trial=1, discovered_at=301s, mutation_op=ByteInterestingMutator,TokenInsert,ByteDecMutator,DwordInterestingMutator):
  0000: f9 f9 f9 f9 f9 f9 f9 f9 37 32 2e 78 6d 6c 5c 0a   ........72.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=9b6b2bebaa2cdd22, size=372 bytes, fuzzer=naive, trial=1, discovered_at=3395s, mutation_op=WordInterestingMutator,BytesRandSetMutator):
  0000: ab ab ab 00 31 32 37 37 38 32 2e 78 6d 6c 5c 0a   ....127782.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
[no informative byte-level divergence — seeds look structurally similar across W and L at every offset, OR diverge only at high-entropy positions (noise)]

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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6948.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6948,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile), grimoire>cmplog (grimoire_structural), value_profile>naive (value_profile), naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6948 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6948 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6948 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).