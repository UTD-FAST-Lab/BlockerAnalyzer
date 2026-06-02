==== BLOCKER ====
Target: libxml2
Branch ID: 6967
Location: /src/libxml2/uri.c:454:9
Enclosing function: uri.c:xmlParse3986Host
Source line:     if (*cur == '[') {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog); loser (value_profile vs value_profile)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    8        2          0  winner (value_profile vs naive)
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        5        5          0  REFERENCE
naive_ngram4                     3        7          0  REFERENCE
mopt                             4        6          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile']
REFERENCE fuzzers (auxiliary context only):     ['value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.20h  loser=19.80h
  avg hitcount on branch: winner=14  loser=2
  prob_div=0.60  dur_div=12.60h  hit_div=13
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001
--- Pair 2: value_profile > naive  [delta: value_profile] ---
  subject 32  (value_profile vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=12.60h  loser=19.80h
  avg hitcount on branch: winner=10  loser=2
  prob_div=0.60  dur_div=7.20h  hit_div=8
  subject-level: delta_AUC=41270400.0  p_AUC=0.0046  delta_Final=826.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6967/{W,L}/branch_coverage_show.txt

--- Enclosing function: uri.c:xmlParse3986Host (/src/libxml2/uri.c:446-506) ---
[ ]   444  static int
[ ]   445  xmlParse3986Host(xmlURIPtr uri, const char **str)
[B]   446  {
[B]   447      const char *cur = *str;
[B]   448      const char *host;
[ ]   449  
[B]   450      host = cur;
[ ]   451      /*
[ ]   452       * IPv6 and future addressing scheme are enclosed between brackets
[ ]   453       */
[B]   454      if (*cur == '[') { <-- BLOCKER
[W]   455          cur++;
[W]   456  	while ((*cur != ']') && (*cur != 0))
[W]   457  	    cur++;
[W]   458  	if (*cur != ']')
[W]   459  	    return(1);
[W]   460  	cur++;
[W]   461  	goto found;
[W]   462      }
[ ]   463      /*
[ ]   464       * try to parse an IPv4
[ ]   465       */
[B]   466      if (ISA_DIGIT(cur)) {
[L]   467          if (xmlParse3986DecOctet(&cur) != 0)
[ ]   468  	    goto not_ipv4;
[L]   469  	if (*cur != '.')
[L]   470  	    goto not_ipv4;
[L]   471  	cur++;
[L]   472          if (xmlParse3986DecOctet(&cur) != 0)
[L]   473  	    goto not_ipv4;
[ ]   474  	if (*cur != '.')
[ ]   475  	    goto not_ipv4;
[ ]   476          if (xmlParse3986DecOctet(&cur) != 0)
[ ]   477  	    goto not_ipv4;
[ ]   478  	if (*cur != '.')
[ ]   479  	    goto not_ipv4;
[ ]   480          if (xmlParse3986DecOctet(&cur) != 0)
[ ]   481  	    goto not_ipv4;
[ ]   482  	goto found;
[L]   483  not_ipv4:
[L]   484          cur = *str;
[L]   485      }
[ ]   486      /*
[ ]   487       * then this should be a hostname which can be empty
[ ]   488       */
[B]   489      while (ISA_UNRESERVED(cur) || ISA_PCT_ENCODED(cur) || ISA_SUB_DELIM(cur))
[B]   490          NEXT(cur);
[B]   491  found:
[B]   492      if (uri != NULL) {
[B]   493  	if (uri->authority != NULL) xmlFree(uri->authority);
[B]   494  	uri->authority = NULL;
[B]   495  	if (uri->server != NULL) xmlFree(uri->server);
[B]   496  	if (cur != host) {
[B]   497  	    if (uri->cleanup & 2)
[ ]   498  		uri->server = STRNDUP(host, cur - host);
[B]   499  	    else
[B]   500  		uri->server = xmlURIUnescapeString(host, cur - host, NULL);
[B]   501  	} else
[L]   502  	    uri->server = NULL;
[B]   503      }
[B]   504      *str = cur;
[B]   505      return(0);
[B]   506  }

--- Caller (1 hop): uri.c:xmlParse3986Authority (/src/libxml2/uri.c:522-544, calls uri.c:xmlParse3986Host at line 535) (full body — short) ---
[B]   522  {
[B]   523      const char *cur;
[B]   524      int ret;
[ ]   525  
[B]   526      cur = *str;
[ ]   527      /*
[ ]   528       * try to parse an userinfo and check for the trailing @
[ ]   529       */
[B]   530      ret = xmlParse3986Userinfo(uri, &cur);
[B]   531      if ((ret != 0) || (*cur != '@'))
[B]   532          cur = *str;
[B]   533      else
[B]   534          cur++;
[B]   535      ret = xmlParse3986Host(uri, &cur); <-- CALL
[B]   536      if (ret != 0) return(ret);
[B]   537      if (*cur == ':') {
[B]   538          cur++;
[B]   539          ret = xmlParse3986Port(uri, &cur);
[B]   540  	if (ret != 0) return(ret);
[B]   541      }
[B]   542      *str = cur;
[B]   543      return(0);
[B]   544  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  uri.c:xmlParse3986Authority  (/src/libxml2/uri.c:522-544, calls uri.c:xmlParse3986Host at line 535)
hop 3  uri.c:xmlParse3986HierPart  (/src/libxml2/uri.c:766-800, calls uri.c:xmlParse3986Authority at line 774)
hop 3  uri.c:xmlParse3986RelativeRef  (/src/libxml2/uri.c:819-857, calls uri.c:xmlParse3986Authority at line 824)
hop 4  uri.c:xmlParse3986URI  (/src/libxml2/uri.c:873-899, calls uri.c:xmlParse3986HierPart at line 882)
hop 4  uri.c:xmlParse3986URIReference  (/src/libxml2/uri.c:914-935, calls uri.c:xmlParse3986RelativeRef at line 928)
hop 5  xmlParseURI  (/src/libxml2/uri.c:948-963, calls uri.c:xmlParse3986URIReference at line 956)
hop 5  xmlParseURIReference  (/src/libxml2/uri.c:978-980, calls uri.c:xmlParse3986URIReference at line 979)
hop 6  xmlParseEntityDecl  (/src/libxml2/parser.c:5476-5721, calls xmlParseURI at line 5545)
hop 6  xmlParseURIRaw  (/src/libxml2/uri.c:994-1012, calls xmlParseURIReference at line 1005)
hop 6  xmlURIEscape  (/src/libxml2/uri.c:1764-1879, calls xmlParseURIReference at line 1778)
hop 7  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseEntityDecl at line 6959)
hop 7  xinclude.c:xmlXIncludeAddNode  (/src/libxml2/xinclude.c:441-592, calls xmlURIEscape at line 503)
hop 8  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 8  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 8  xinclude.c:xmlXIncludeExpandNode  (/src/libxml2/xinclude.c:1854-1885, calls xinclude.c:xmlXIncludeAddNode at line 1875)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    2630     19900  uri.c:is_hex  (/src/libxml2/uri.c:1607-1613)
     121      1810  uri.c:xmlParse3986Segment  (/src/libxml2/uri.c:564-577)
     468      1570  uri.c:xmlCleanURI  (/src/libxml2/uri.c:1367-1388)
     213       908  xmlURIUnescapeString  (/src/libxml2/uri.c:1630-1677)
     132       445  xmlCreateURI  (/src/libxml2/uri.c:1028-1039)
     132       445  xmlFreeURI  (/src/libxml2/uri.c:1397-1410)
      46       354  uri.c:xmlParse3986PathAbEmpty  (/src/libxml2/uri.c:593-617)
     131       434  uri.c:xmlParse3986Scheme  (/src/libxml2/uri.c:214-232)
     131       434  uri.c:xmlParse3986URI  (/src/libxml2/uri.c:873-899)
     131       434  uri.c:xmlParse3986URIReference  (/src/libxml2/uri.c:914-935)
     126       379  xmlParseURI  (/src/libxml2/uri.c:948-963)
     108       338  uri.c:xmlParse3986RelativeRef  (/src/libxml2/uri.c:819-857)
      47       158  xmlCanonicPath  (/src/libxml2/uri.c:2396-2522)
       3        79  uri.c:xmlParse3986Fragment  (/src/libxml2/uri.c:251-273)
      30       106  xmlSaveUri  (/src/libxml2/uri.c:1075-1340)
... (6 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  xmlParseURI  (/src/libxml2/uri.c:948-963) ---
  d=5   L 952  T=0 F=126  T=0 F=379  if (str == NULL)
  d=5   L 955  T=126 F=0  T=379 F=0  if (uri != NULL) {
  d=5   L 957  T=102 F=24  T=267 F=112  if (ret) {
--- d=4  uri.c:xmlParse3986URI  (/src/libxml2/uri.c:873-899) ---
  d=4   L 877  T=0 F=131  T=18 F=416  if (ret != 0) return(ret);
  d=4   L 878  T=5 F=126  T=57 F=359  if (*str != ':') {
  d=4   L 883  T=80 F=46  T=21 F=338  if (ret != 0) return(ret);
  d=4   L 884  T=3 F=43  T=40 F=298  if (*str == '?') {
  d=4   L 887  T=0 F=3  T=0 F=40  if (ret != 0) return(ret);
  d=4   L 889  T=3 F=43  T=79 F=259  if (*str == '#') {
  d=4   L 892  T=0 F=3  T=0 F=79  if (ret != 0) return(ret);
  d=4   L 894  T=23 F=23  T=242 F=96  if (*str != 0) {
--- d=4  uri.c:xmlParse3986URIReference  (/src/libxml2/uri.c:914-935) ---
  d=4   L 917  T=0 F=131  T=0 F=434  if (str == NULL)
  d=4   L 926  T=108 F=23  T=338 F=96  if (ret != 0) {
  d=4   L 929  T=103 F=5  T=278 F=60  if (ret != 0) {
--- d=3  uri.c:xmlParse3986HierPart  (/src/libxml2/uri.c:766-800) ---
  d=3   L 772  T=126 F=0  T=359 F=0  if ((*cur == '/') && (*(cur + 1) == '/')) {
  d=3   L 772  T=126 F=0  T=359 F=0  if ((*cur == '/') && (*(cur + 1) == '/')) {
  d=3   L 775  T=80 F=46  T=21 F=338  if (ret != 0) return(ret);
  d=3   L 779  T=0 F=46  T=53 F=285  if ((uri->server == NULL) && (uri->port == PORT_EMPTY))
  d=3   L 779  T=0 F=0  T=53 F=0  if ((uri->server == NULL) && (uri->port == PORT_EMPTY))
  d=3   L 782  T=0 F=46  T=0 F=338  if (ret != 0) return(ret);
--- d=3  uri.c:xmlParse3986RelativeRef  (/src/libxml2/uri.c:819-857) ---
  d=3   L 822  T=0 F=108  T=18 F=320  if ((*str == '/') && (*(str + 1) == '/')) {
  d=3   L 822  T=0 F=0  T=16 F=2  if ((*str == '/') && (*(str + 1) == '/')) {
  d=3   L 825  T=0 F=0  T=0 F=16  if (ret != 0) return(ret);
  d=3   L 827  T=0 F=0  T=0 F=16  if (ret != 0) return(ret);
  d=3   L 828  T=0 F=108  T=2 F=320  } else if (*str == '/') {
  d=3   L 830  T=0 F=0  T=0 F=2  if (ret != 0) return(ret);
  d=3   L 833  T=0 F=108  T=0 F=320  if (ret != 0) return(ret);
  d=3   L 842  T=0 F=108  T=0 F=338  if (*str == '?') {
  d=3   L 847  T=0 F=108  T=0 F=338  if (*str == '#') {
  d=3   L 852  T=103 F=5  T=278 F=60  if (*str != 0) {
--- d=2  uri.c:xmlParse3986Authority  (/src/libxml2/uri.c:522-544) ---
  d=2   L 531  T=104 F=22  T=353 F=22  if ((ret != 0) || (*cur != '@'))
  d=2   L 536  T=56 F=70  T=0 F=375  if (ret != 0) return(ret);
  d=2   L 537  T=24 F=46  T=21 F=354  if (*cur == ':') {
--- d=1  uri.c:xmlParse3986Host  (/src/libxml2/uri.c:446-506) ---
  d=1   L 454  T=69 F=57  T=0 F=375  if (*cur == '[') {  <-- BLOCKER
  d=1   L 456  T=7110 F=13  T=0 F=0  while ((*cur != ']') && (*cur != 0))
  d=1   L 456  T=7050 F=56  T=0 F=0  while ((*cur != ']') && (*cur != 0))
  d=1   L 458  T=56 F=13  T=0 F=0  if (*cur != ']')
  d=1   L 467  T=0 F=0  T=0 F=24  if (xmlParse3986DecOctet(&cur) != 0)
  d=1   L 469  T=0 F=0  T=16 F=8  if (*cur != '.')
  d=1   L 472  T=0 F=0  T=8 F=0  if (xmlParse3986DecOctet(&cur) != 0)
  d=1   L 492  T=70 F=0  T=375 F=0  if (uri != NULL) {
  d=1   L 493  T=0 F=70  T=0 F=375  if (uri->authority != NULL) xmlFree(uri->authority);
  d=1   L 495  T=0 F=70  T=0 F=375  if (uri->server != NULL) xmlFree(uri->server);
  d=1   L 496  T=70 F=0  T=307 F=68  if (cur != host) {
  d=1   L 497  T=0 F=70  T=0 F=307  if (uri->cleanup & 2)

[off-chain: 245 additional divergent branches across 20 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=20b2621140bcb91b, size=119 bytes, fuzzer=cmplog, trial=3, discovered_at=4561s, mutation_op=BytesDeleteMutator,QwordAddMutator,BytesRandInsertMutator,BytesDeleteMutator,BytesDeleteMutator,BytesSetMutator):
  0000: 3d 22 6a 22 74 70 3a 2f 2f 5b 61 6b 65 75 72 2a   ="j"tp://[akeur*
  0010: 2e 01 01 01 01 01 01 01 01 01 01 01 3f 01 01 6d   ............?..m
  0020: 65 74 22 3e 62 20 74 65 2f 8b 3c 2f 62 3e 1a 3c   et">b te/.</b>.<
  0030: 2f 80 3e 2b db 43 dc 64 74 64 73 2a 00 32 37 37   /.>+.C.dtds*.277
Seed 2 (id=2ec8851de49ee930, size=113 bytes, fuzzer=value_profile, trial=1, discovered_at=6244s, mutation_op=BytesDeleteMutator,ByteAddMutator,TokenInsert):
  0000: 27 68 74 74 70 3a 2f 2f 5b 77 77 2e 77 33 2e 6f   'http://[ww.w3.o
  0010: 73 6e 6b 3a 74 79 70 65 20 20 20 28 73 69 6d 70   snk:type   (simp
  0020: 6c 65 29 20 20 23 46 49 58 45 44 20 27 73 69 6d   le)  #FIXED 'sim
  0030: 70 6c 65 27 0a 20 20 20 20 20 78 6c 69 6e 6b 77   ple'.     xlinkw
Seed 3 (id=fc534f8367e94fa3, size=119 bytes, fuzzer=value_profile, trial=1, discovered_at=6244s, mutation_op=BytesRandSetMutator,BytesCopyMutator,BytesCopyMutator,BytesExpandMutator,ByteNegMutator):
  0000: 44 20 27 68 74 74 70 3a 2f 2f 5b 77 77 2e 77 33   D 'http://[ww.w3
  0010: 2e 6f 73 6e 6b 3a 74 79 70 65 20 20 20 28 73 69   .osnk:type   (si
  0020: 6d 70 94 6d 6d 6d 6d 6d 6d 6d 6d 6d 44 20 6d 6d   mp.mmmmmmmmmD mm
  0030: 6d 6d 6d 6d 44 20 27 73 69 6d 20 20 28 73 69 23   mmmmD 'sim  (si#
Seed 4 (id=32cf94fabd205af8, size=168 bytes, fuzzer=value_profile, trial=1, discovered_at=9377s, mutation_op=ByteDecMutator,CrossoverInsertMutator,BytesExpandMutator,BytesRandInsertMutator,QwordAddMutator,BytesCopyMutator):
  0000: 44 20 27 68 74 74 70 3a 2f 2f 5b 77 77 2e 77 33   D 'http://[ww.w3
  0010: 2e 6f 73 6e 6b 3a 74 79 70 65 20 20 20 28 73 69   .osnk:type   (si
  0020: 6d 70 94 6d 6d 6d 6d 6d 6d 6d 6d 6d 44 20 6d 6d   mp.mmmmmmmmmD mm
  0030: 43 44 41 99 28 38 28 2d 28 28 2d 28 54 20 62 20   CDA.(8(-((-(T b 
Seed 5 (id=994b4b4cace1a63a, size=357 bytes, fuzzer=value_profile, trial=1, discovered_at=11520s, mutation_op=ByteNegMutator,BytesRandInsertMutator,ByteDecMutator,WordAddMutator,BytesCopyMutator,CrossoverInsertMutator,QwordAddMutator):
  0000: 44 20 27 68 74 74 70 3a 2f 2f 5b 77 77 2e 77 33   D 'http://[ww.w3
  0010: d2 6f 73 6e 6b 3a 74 79 70 65 20 20 20 28 73 69   .osnk:type   (si
  0020: 6d 70 94 6d 6d 6d 6d 6d 6d 79 6d 6d 44 20 6d 6d   mp.mmmmmmymmD mm
  0030: 43 44 41 99 28 38 28 2d 28 28 20 20 28 73 69 6d   CDA.(8(-((  (sim

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0023aedf54362876, size=518 bytes, fuzzer=naive, trial=4, discovered_at=26s, mutation_op=BytesSetMutator,ByteIncMutator,CrossoverInsertMutator):
  0000: 01 00 70 3a 2f 2f 66 32 2e 64 74 64 5c 0a 3c 21   ..p://f2.dtd\.<!
  0010: 45 4c 45 4d 45 4e 54 20 61 20 28 62 2a 29 3e 0a   ELEMENT a (b*)>.
  0020: 0a 3c 21 45 4c 45 4d 45 4d 54 20 62 20 28 23 50   .<!ELEMEMT b (#P
  0030: 43 44 41 54 41 29 3e 0a 3c 21 41 54 54 4c 49 53   CDATA)>.<!ATTLIS
Seed 2 (id=000ed87ac60d44fc, size=162 bytes, fuzzer=naive, trial=1, discovered_at=70s, mutation_op=WordInterestingMutator,WordInterestingMutator,BytesDeleteMutator):
  0000: 66 3d 22 68 74 74 70 3a 2f 2f 66 61 6b 65 75 20   f="http://fakeu 
  0010: 61 20 28 62 0c 29 3e 0a 0a 3c 21 45 4c 45 4d 45   a (b.)>..<!ELEME
  0020: 4e 54 20 62 20 28 23 50 43 44 41 54 41 29 3e 0a   NT b (#PCDATA)>.
  0030: 3c 21 41 00 64 4c 49 53 54 20 62 20 78 6d 6c 75   <!A.dLIST b xmlu
Seed 3 (id=0028492ac168fa2b, size=312 bytes, fuzzer=naive, trial=1, discovered_at=78s, mutation_op=ByteAddMutator,TokenReplace):
  0000: 44 20 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 33   D 'http://www.w3
  0010: 7e 96 98 00 2f 31 39 39 39 2f 78 6c 69 6e 6b 27   ~.../1999/xlink'
  0020: 0a 20 20 20 20 20 20 20 20 20 20 20 20 78 6c 69   .            xli
  0030: 6e 6b 3a 74 79 70 50 20 20 20 28 73 69 6d 70 6c   nk:typP   (simpl
Seed 4 (id=00bc240c762794a6, size=80 bytes, fuzzer=naive, trial=1, discovered_at=195s, mutation_op=BytesDeleteMutator,DwordAddMutator):
  0000: 00 00 80 74 70 3a 2f 2f 66 61 6c 20 76 65 72 73   ...tp://fal vers
  0010: 69 6f 6e 45 4c 6b 65 75 f9 ff ff ff 72 6c 2e 6e   ionELkeu....rl.n
  0020: 65 74 24 3e 62 20 74 6e 78 74 3c 2f 62 3e 0a 3c   et$>b tnxt</b>.<
  0030: 2f 61 3e 0a 0a d7 ff ff ff ff ff ff ff 0a 5c 0a   /a>...........\.
Seed 5 (id=00129acafe9ff042, size=161 bytes, fuzzer=naive, trial=1, discovered_at=217s, mutation_op=TokenReplace,BytesExpandMutator,ByteFlipMutator):
  0000: 45 44 20 27 73 69 68 74 74 70 3a 2f 2f 66 61 6b   ED 'sihttp://fak
  0010: 65 75 72 6c 2e 6e 65 74 fd ff ff ff 7a 7a 7a 7a   eurl.net....zzzz
  0020: 7a 7a 7a fd ff ff ff 7a 7a 7a 7a 7a 7a 7a 7a 20   zzz....zzzzzzzz 
  0030: 20 20 20 20 20 20 7a 7a 7a 7a 20 20 3e 0a 3c 2f         zzzz  >.</


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0004  74(t)x8 70(p)x7 64(d)x1 68(h)x1     74(t)x22 70(p)x8 68(h)x8 73(s)x5 +4u  PARTIAL
   0x0005  3a(:)x8 74(t)x5 70(p)x2 64(d)x2     74(t)x17 70(p)x16 3a(:)x7 2f(/)x4 +5u  PARTIAL
   0x0007  2f(/)x10 3a(:)x4 70(p)x3            2f(/)x22 3a(:)x10 70(p)x7 74(t)x2 +9u  PARTIAL
   0x0008  5b([)x8 2f(/)x6 3a(:)x3             2f(/)x24 3a(:)x7 74(t)x5 66(f)x3 +9u  PARTIAL
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

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_6967.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6967,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile>naive (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6967 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6967 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6967 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).