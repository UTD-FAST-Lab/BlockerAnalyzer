==== BLOCKER ====
Target: libxml2
Branch ID: 6976
Location: /src/libxml2/uri.c:536:9
Enclosing function: uri.c:xmlParse3986Authority
Source line:     if (ret != 0) return(ret);
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        4        6          0  REFERENCE
naive_ngram4                     3        7          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         6        4          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.80h  loser=19.80h
  avg hitcount on branch: winner=13  loser=2
  prob_div=0.60  dur_div=12.00h  hit_div=12
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6976/{W,L}/branch_coverage_show.txt

--- Enclosing function: uri.c:xmlParse3986Authority (/src/libxml2/uri.c:522-544) ---
[ ]   520  static int
[ ]   521  xmlParse3986Authority(xmlURIPtr uri, const char **str)
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
[B]   535      ret = xmlParse3986Host(uri, &cur);
[B]   536      if (ret != 0) return(ret); <-- BLOCKER
[B]   537      if (*cur == ':') {
[B]   538          cur++;
[B]   539          ret = xmlParse3986Port(uri, &cur);
[B]   540  	if (ret != 0) return(ret);
[B]   541      }
[B]   542      *str = cur;
[B]   543      return(0);
[B]   544  }

--- Caller (1 hop): uri.c:xmlParse3986HierPart (/src/libxml2/uri.c:766-800, calls uri.c:xmlParse3986Authority at line 774) (full body — short) ---
[B]   766  {
[B]   767      const char *cur;
[B]   768      int ret;
[ ]   769  
[B]   770      cur = *str;
[ ]   771  
[B]   772      if ((*cur == '/') && (*(cur + 1) == '/')) {
[B]   773          cur += 2;
[B]   774  	ret = xmlParse3986Authority(uri, &cur); <-- CALL
[B]   775  	if (ret != 0) return(ret);
[ ]   776          /*
[ ]   777           * An empty server is marked with a special URI value.
[ ]   778           */
[B]   779  	if ((uri->server == NULL) && (uri->port == PORT_EMPTY))
[L]   780  	    uri->port = PORT_EMPTY_SERVER;
[B]   781  	ret = xmlParse3986PathAbEmpty(uri, &cur);
[B]   782  	if (ret != 0) return(ret);
[B]   783  	*str = cur;
[B]   784  	return(0);
[B]   785      } else if (*cur == '/') {
[ ]   786          ret = xmlParse3986PathAbsolute(uri, &cur);
[ ]   787  	if (ret != 0) return(ret);
[ ]   788      } else if (ISA_PCHAR(cur)) {
[ ]   789          ret = xmlParse3986PathRootless(uri, &cur);
[ ]   790  	if (ret != 0) return(ret);
[ ]   791      } else {
[ ]   792  	/* path-empty is effectively empty */
[ ]   793  	if (uri != NULL) {
[ ]   794  	    if (uri->path != NULL) xmlFree(uri->path);
[ ]   795  	    uri->path = NULL;
[ ]   796  	}
[ ]   797      }
[ ]   798      *str = cur;
[ ]   799      return (0);
[B]   800  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  uri.c:xmlParse3986HierPart  (/src/libxml2/uri.c:766-800, calls uri.c:xmlParse3986Authority at line 774)
hop 2  uri.c:xmlParse3986RelativeRef  (/src/libxml2/uri.c:819-857, calls uri.c:xmlParse3986Authority at line 824)
hop 3  uri.c:xmlParse3986URI  (/src/libxml2/uri.c:873-899, calls uri.c:xmlParse3986HierPart at line 882)
hop 3  uri.c:xmlParse3986URIReference  (/src/libxml2/uri.c:914-935, calls uri.c:xmlParse3986RelativeRef at line 928)
hop 4  xmlParseURI  (/src/libxml2/uri.c:948-963, calls uri.c:xmlParse3986URIReference at line 956)
hop 4  xmlParseURIReference  (/src/libxml2/uri.c:978-980, calls uri.c:xmlParse3986URIReference at line 979)
hop 5  xmlParseEntityDecl  (/src/libxml2/parser.c:5476-5721, calls xmlParseURI at line 5545)
hop 5  xmlParseURIRaw  (/src/libxml2/uri.c:994-1012, calls xmlParseURIReference at line 1005)
hop 5  xmlURIEscape  (/src/libxml2/uri.c:1764-1879, calls xmlParseURIReference at line 1778)
hop 6  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990, calls xmlParseEntityDecl at line 6959)
hop 6  xinclude.c:xmlXIncludeAddNode  (/src/libxml2/xinclude.c:441-592, calls xmlURIEscape at line 503)
hop 7  parser.c:xmlParseConditionalSections  (/src/libxml2/parser.c:6804-6923, calls xmlParseMarkupDecl at line 6907)
hop 7  xmlParseExternalSubset  (/src/libxml2/parser.c:7095-7155, calls xmlParseMarkupDecl at line 7142)
hop 7  xinclude.c:xmlXIncludeExpandNode  (/src/libxml2/xinclude.c:1854-1885, calls xinclude.c:xmlXIncludeAddNode at line 1875)
hop 8  parser.c:xmlParseInternalSubset  (/src/libxml2/parser.c:8452-8503, calls parser.c:xmlParseConditionalSections at line 8475)
hop 8  xmlIOParseDTD  (/src/libxml2/parser.c:12525-12629, calls xmlParseExternalSubset at line 12604)
hop 8  xmlSAXParseDTD  (/src/libxml2/parser.c:12646-12748, calls xmlParseExternalSubset at line 12723)
hop 8  xinclude.c:xmlXIncludeCopyNode  (/src/libxml2/xinclude.c:654-742, calls xinclude.c:xmlXIncludeExpandNode at line 680)
hop 8  xinclude.c:xmlXIncludeDoProcess  (/src/libxml2/xinclude.c:2227-2314, calls xinclude.c:xmlXIncludeExpandNode at line 2255)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1770     19900  uri.c:is_hex  (/src/libxml2/uri.c:1607-1613)
     147      1810  uri.c:xmlParse3986Segment  (/src/libxml2/uri.c:564-577)
     262      1570  uri.c:xmlCleanURI  (/src/libxml2/uri.c:1367-1388)
     118       908  xmlURIUnescapeString  (/src/libxml2/uri.c:1630-1677)
      82       445  xmlCreateURI  (/src/libxml2/uri.c:1028-1039)
      82       445  xmlFreeURI  (/src/libxml2/uri.c:1397-1410)
      81       434  uri.c:xmlParse3986Scheme  (/src/libxml2/uri.c:214-232)
      81       434  uri.c:xmlParse3986URI  (/src/libxml2/uri.c:873-899)
      81       434  uri.c:xmlParse3986URIReference  (/src/libxml2/uri.c:914-935)
      20       354  uri.c:xmlParse3986PathAbEmpty  (/src/libxml2/uri.c:593-617)
      76       379  xmlParseURI  (/src/libxml2/uri.c:948-963)
      74       375  uri.c:xmlParse3986Userinfo  (/src/libxml2/uri.c:371-390)
      74       375  uri.c:xmlParse3986Host  (/src/libxml2/uri.c:446-506)
      74       375  uri.c:xmlParse3986Authority  (/src/libxml2/uri.c:522-544)  <-- enclosing
      74       359  uri.c:xmlParse3986HierPart  (/src/libxml2/uri.c:766-800)
... (14 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=4  xmlParseURI  (/src/libxml2/uri.c:948-963) ---
  d=4   L 952  T=0 F=76  T=0 F=379  if (str == NULL)
  d=4   L 955  T=76 F=0  T=379 F=0  if (uri != NULL) {
  d=4   L 957  T=56 F=20  T=267 F=112  if (ret) {
--- d=3  uri.c:xmlParse3986URI  (/src/libxml2/uri.c:873-899) ---
  d=3   L 877  T=0 F=81  T=18 F=416  if (ret != 0) return(ret);
  d=3   L 878  T=7 F=74  T=57 F=359  if (*str != ':') {
  d=3   L 883  T=54 F=20  T=21 F=338  if (ret != 0) return(ret);
  d=3   L 884  T=3 F=17  T=40 F=298  if (*str == '?') {
  d=3   L 887  T=0 F=3  T=0 F=40  if (ret != 0) return(ret);
  d=3   L 889  T=3 F=17  T=79 F=259  if (*str == '#') {
  d=3   L 892  T=0 F=3  T=0 F=79  if (ret != 0) return(ret);
  d=3   L 894  T=3 F=17  T=242 F=96  if (*str != 0) {
--- d=3  uri.c:xmlParse3986URIReference  (/src/libxml2/uri.c:914-935) ---
  d=3   L 917  T=0 F=81  T=0 F=434  if (str == NULL)
  d=3   L 926  T=64 F=17  T=338 F=96  if (ret != 0) {
  d=3   L 929  T=57 F=7  T=278 F=60  if (ret != 0) {
--- d=2  uri.c:xmlParse3986HierPart  (/src/libxml2/uri.c:766-800) ---
  d=2   L 772  T=74 F=0  T=359 F=0  if ((*cur == '/') && (*(cur + 1) == '/')) {
  d=2   L 772  T=74 F=0  T=359 F=0  if ((*cur == '/') && (*(cur + 1) == '/')) {
  d=2   L 775  T=54 F=20  T=21 F=338  if (ret != 0) return(ret);
  d=2   L 779  T=0 F=20  T=53 F=285  if ((uri->server == NULL) && (uri->port == PORT_EMPTY))
  d=2   L 779  T=0 F=0  T=53 F=0  if ((uri->server == NULL) && (uri->port == PORT_EMPTY))
  d=2   L 782  T=0 F=20  T=0 F=338  if (ret != 0) return(ret);
--- d=2  uri.c:xmlParse3986RelativeRef  (/src/libxml2/uri.c:819-857) ---
  d=2   L 822  T=0 F=64  T=18 F=320  if ((*str == '/') && (*(str + 1) == '/')) {
  d=2   L 822  T=0 F=0  T=16 F=2  if ((*str == '/') && (*(str + 1) == '/')) {
  d=2   L 825  T=0 F=0  T=0 F=16  if (ret != 0) return(ret);
  d=2   L 827  T=0 F=0  T=0 F=16  if (ret != 0) return(ret);
  d=2   L 828  T=0 F=64  T=2 F=320  } else if (*str == '/') {
  d=2   L 830  T=0 F=0  T=0 F=2  if (ret != 0) return(ret);
  d=2   L 833  T=0 F=64  T=0 F=320  if (ret != 0) return(ret);
  d=2   L 842  T=0 F=64  T=0 F=338  if (*str == '?') {
  d=2   L 847  T=0 F=64  T=0 F=338  if (*str == '#') {
  d=2   L 852  T=57 F=7  T=278 F=60  if (*str != 0) {
--- d=1  uri.c:xmlParse3986Authority  (/src/libxml2/uri.c:522-544) ---
  d=1   L 531  T=0 F=11  T=0 F=22  if ((ret != 0) || (*cur != '@'))
  d=1   L 531  T=63 F=11  T=353 F=22  if ((ret != 0) || (*cur != '@'))
  d=1   L 536  T=42 F=32  T=0 F=375  if (ret != 0) return(ret);  <-- BLOCKER
  d=1   L 537  T=12 F=20  T=21 F=354  if (*cur == ':') {

[off-chain: 261 additional divergent branches across 21 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=29009d00708bb022, size=70 bytes, fuzzer=cmplog, trial=3, discovered_at=2472s, mutation_op=ByteIncMutator,ByteRandMutator,BytesExpandMutator,CrossoverReplaceMutator):
  0000: 3d 22 68 74 74 70 3a 2f 2f 5b 61 6b 65 75 72 6c   ="http://[akeurl
  0010: 2e 6e 65 74 2d 3e 2e 2d 74 65 78 74 3c 40 62 2c   .net->.-text<@b,
  0020: 0a 2a 20 20 20 0a 0a 5c 0a 64 74 64 73 26 31 32   .*   ..\.dtds&12
  0030: 37 37 4c 65 4d 0a 4e 54 5c 5c 28 28 0a 2a 29 9f   77LeM.NT\\((.*).
Seed 2 (id=28f085d41d33a581, size=560 bytes, fuzzer=cmplog, trial=3, discovered_at=3606s, mutation_op=BytesExpandMutator,BytesRandSetMutator,ByteAddMutator,BytesSwapMutator):
  0000: 65 66 3d 22 68 74 74 70 3a 2f 2f 5b 61 6b 65 75   ef="http://[akeu
  0010: 72 6c 2e 6e 65 2c 22 3a 7e 20 74 65 78 74 3c 2f   rl.ne,":~ text</
  0020: 62 3e 0a 3c 2f 61 3e 0a 0a 5c 0a 64 74 64 73 2f   b>.</a>..\.dtds/
  0030: 31 32 37 37 37 32 5f 64 74 64 5c 0a 3c 3f 45 74   127772_dtd\.<?Et
Seed 3 (id=20b2621140bcb91b, size=119 bytes, fuzzer=cmplog, trial=3, discovered_at=4561s, mutation_op=BytesDeleteMutator,QwordAddMutator,BytesRandInsertMutator,BytesDeleteMutator,BytesDeleteMutator,BytesSetMutator):
  0000: 3d 22 6a 22 74 70 3a 2f 2f 5b 61 6b 65 75 72 2a   ="j"tp://[akeur*
  0010: 2e 01 01 01 01 01 01 01 01 01 01 01 3f 01 01 6d   ............?..m
  0020: 65 74 22 3e 62 20 74 65 2f 8b 3c 2f 62 3e 1a 3c   et">b te/.</b>.<
  0030: 2f 80 3e 2b db 43 dc 64 74 64 73 2a 00 32 37 37   /.>+.C.dtds*.277
Seed 4 (id=0f6504dbdd3ce382, size=290 bytes, fuzzer=cmplog, trial=3, discovered_at=12628s, mutation_op=BytesExpandMutator,DwordAddMutator,BytesExpandMutator,ByteInterestingMutator):
  0000: 22 68 22 74 64 3a 2f 2f 5b 61 6b 3a 00 2b 29 25   "h"td://[ak:.+)%
  0010: 24 3d 3d 29 3d 3d 3d 3d 3d 3f 74 3e 25 62 29 0a   $==)=====?t>%b).
  0020: 2f 2f 61 3e 0a 0a 5c 0a 64 74 64 73 24 31 32 37   //a>..\.dtds$127
  0030: 37 37 32 2e 4c 74 02 5c 0a 3c 21 45 4c 45 4d 45   772.Lt.\.<!ELEME
Seed 5 (id=0a912a4f189676dc, size=200 bytes, fuzzer=cmplog, trial=3, discovered_at=13781s, mutation_op=BytesSwapMutator,ByteDecMutator,BitFlipMutator,ByteNegMutator,WordInterestingMutator,ByteFlipMutator):
  0000: 66 3d 22 68 74 74 70 3a 2f 2f 5b 61 6b 65 75 6e   f="http://[akeun
  0010: 6b 20 20 43 44 41 80 ff ff ff 20 fc ff ff ff 20   k  CDA.... .... 
  0020: 20 ff ff ff 20 fc ff ff ff 20 20 23 65 49 58 45    ... ....  #eIXE
  0030: 0a 20 28 68 7e 74 70 3a 2f 2f 77 77 77 28 77 33   . (h~tp://www(w3

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
   0x0003  74(t)x6 22(")x2 68(h)x1 4c(L)x1     74(t)x18 68(h)x9 22(")x4 27(')x3 +11u  PARTIAL
   0x0004  74(t)x5 70(p)x3 68(h)x1 64(d)x1     74(t)x22 70(p)x8 68(h)x8 73(s)x5 +4u  PARTIAL
   0x0005  3a(:)x4 70(p)x3 74(t)x2 64(d)x1     74(t)x17 70(p)x16 3a(:)x7 2f(/)x4 +5u  PARTIAL
   0x0007  2f(/)x7 70(p)x2 3a(:)x1             2f(/)x22 3a(:)x10 70(p)x7 74(t)x2 +9u  PARTIAL
   0x0008  2f(/)x4 5b([)x4 3a(:)x2             2f(/)x24 3a(:)x7 74(t)x5 66(f)x3 +9u  PARTIAL
   0x0009  5b([)x3 2f(/)x3 61(a)x2 2b(+)x2     2f(/)x16 77(w)x6 66(f)x5 70(p)x3 +15u  PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6976.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6976,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6976 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6976 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6976 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).