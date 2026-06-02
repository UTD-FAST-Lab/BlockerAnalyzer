==== BLOCKER ====
Target: curl
Branch ID: 405
Location: /src/curl/lib/strerror.c:529:3
Enclosing function: curl_url_strerror
Source line:   case CURLUE_BAD_FILE_URL:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     3        7          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             5        5          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=2.90h  loser=21.60h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=18.70h  hit_div=3
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/405/{W,L}/branch_coverage_show.txt

--- Enclosing function: curl_url_strerror (/src/curl/lib/strerror.c:460-564) ---
[ ]   458  const char *
[ ]   459  curl_url_strerror(CURLUcode error)
[B]   460  {
[B]   461  #ifndef CURL_DISABLE_VERBOSE_STRINGS
[B]   462    switch(error) {
[ ]   463    case CURLUE_OK:
[ ]   464      return "No error";
[ ]   465  
[ ]   466    case CURLUE_BAD_HANDLE:
[ ]   467      return "An invalid CURLU pointer was passed as argument";
[ ]   468  
[ ]   469    case CURLUE_BAD_PARTPOINTER:
[ ]   470      return "An invalid 'part' argument was passed as argument";
[ ]   471  
[ ]   472    case CURLUE_MALFORMED_INPUT:
[ ]   473      return "Malformed input to a URL function";
[ ]   474  
[L]   475    case CURLUE_BAD_PORT_NUMBER:
[L]   476      return "Port number was not a decimal number between 0 and 65535";
[ ]   477  
[ ]   478    case CURLUE_UNSUPPORTED_SCHEME:
[ ]   479      return "Unsupported URL scheme";
[ ]   480  
[ ]   481    case CURLUE_URLDECODE:
[ ]   482      return "URL decode error, most likely because of rubbish in the input";
[ ]   483  
[ ]   484    case CURLUE_OUT_OF_MEMORY:
[ ]   485      return "A memory function failed";
[ ]   486  
[ ]   487    case CURLUE_USER_NOT_ALLOWED:
[ ]   488      return "Credentials was passed in the URL when prohibited";
[ ]   489  
[ ]   490    case CURLUE_UNKNOWN_PART:
[ ]   491      return "An unknown part ID was passed to a URL API function";
[ ]   492  
[ ]   493    case CURLUE_NO_SCHEME:
[ ]   494      return "No scheme part in the URL";
[ ]   495  
[ ]   496    case CURLUE_NO_USER:
[ ]   497      return "No user part in the URL";
[ ]   498  
[ ]   499    case CURLUE_NO_PASSWORD:
[ ]   500      return "No password part in the URL";
[ ]   501  
[ ]   502    case CURLUE_NO_OPTIONS:
[ ]   503      return "No options part in the URL";
[ ]   504  
[ ]   505    case CURLUE_NO_HOST:
[ ]   506      return "No host part in the URL";
[ ]   507  
[ ]   508    case CURLUE_NO_PORT:
[ ]   509      return "No port part in the URL";
[ ]   510  
[ ]   511    case CURLUE_NO_QUERY:
[ ]   512      return "No query part in the URL";
[ ]   513  
[ ]   514    case CURLUE_NO_FRAGMENT:
[ ]   515      return "No fragment part in the URL";
[ ]   516  
[ ]   517    case CURLUE_NO_ZONEID:
[ ]   518      return "No zoneid part in the URL";
[ ]   519  
[ ]   520    case CURLUE_BAD_LOGIN:
[ ]   521      return "Bad login part";
[ ]   522  
[ ]   523    case CURLUE_BAD_IPV6:
[ ]   524      return "Bad IPv6 address";
[ ]   525  
[L]   526    case CURLUE_BAD_HOSTNAME:
[L]   527      return "Bad hostname";
[ ]   528  
[W]   529    case CURLUE_BAD_FILE_URL: <-- BLOCKER
[W]   530      return "Bad file:// URL";
[ ]   531  
[ ]   532    case CURLUE_BAD_SLASHES:
[ ]   533      return "Unsupported number of slashes following scheme";
[ ]   534  
[ ]   535    case CURLUE_BAD_SCHEME:
[ ]   536      return "Bad scheme";
[ ]   537  
[L]   538    case CURLUE_BAD_PATH:
[L]   539      return "Bad path";
[ ]   540  
[ ]   541    case CURLUE_BAD_FRAGMENT:
[ ]   542      return "Bad fragment";
[ ]   543  
[ ]   544    case CURLUE_BAD_QUERY:
[ ]   545      return "Bad query";
[ ]   546  
[ ]   547    case CURLUE_BAD_PASSWORD:
[ ]   548      return "Bad password";
[ ]   549  
[ ]   550    case CURLUE_BAD_USER:
[ ]   551      return "Bad user";
[ ]   552  
[ ]   553    case CURLUE_LAST:
[ ]   554      break;
[B]   555    }
[ ]   556  
[ ]   557    return "CURLUcode unknown";
[ ]   558  #else
[ ]   559    if(error == CURLUE_OK)
[ ]   560      return "No error";
[ ]   561    else
[ ]   562      return "Error";
[ ]   563  #endif
[B]   564  }

--- Caller (1 hop): url.c:parseurlandfillconn (/src/curl/lib/url.c:1969-2174, calls curl_url_strerror at line 2011) (±10 around call site) ---
[B]  2001    if(!use_set_uh) {
[B]  2002      char *newurl;
[B]  2003      uc = curl_url_set(uh, CURLUPART_URL, data->state.url,
[B]  2004                      CURLU_GUESS_SCHEME |
[B]  2005                      CURLU_NON_SUPPORT_SCHEME |
[B]  2006                      (data->set.disallow_username_in_url ?
[B]  2007                       CURLU_DISALLOW_USER : 0) |
[B]  2008                      (data->set.path_as_is ? CURLU_PATH_AS_IS : 0));
[B]  2009      if(uc) {
[B]  2010        DEBUGF(infof(data, "curl_url_set rejected %s: %s", data->state.url,
[B]  2011                     curl_url_strerror(uc))); <-- CALL
[B]  2012        return Curl_uc_to_curlcode(uc);
[B]  2013      }
[ ]  2014  
[ ]  2015      /* after it was parsed, get the generated normalized version */
[ ]  2016      uc = curl_url_get(uh, CURLUPART_URL, &newurl, 0);
[ ]  2017      if(uc)
[ ]  2018        return Curl_uc_to_curlcode(uc);
[ ]  2019      if(data->state.url_alloc)
[ ]  2020        free(data->state.url);
[ ]  2021      data->state.url = newurl;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_follow  (/src/curl/lib/transfer.c:1568-1849, calls curl_url_strerror at line 1654)
hop 2  url.c:parseurlandfillconn  (/src/curl/lib/url.c:1969-2174, calls curl_url_strerror at line 2011)
hop 3  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_follow at line 2222)
hop 3  url.c:create_conn  (/src/curl/lib/url.c:3683-4145, calls url.c:parseurlandfillconn at line 3721)
hop 4  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 4  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)
hop 4  url.c:findprotocol  (/src/curl/lib/url.c:1864-1893, calls url.c:create_conn at line 1888)
hop 4  url.c:resolve_server  (/src/curl/lib/url.c:3572-3586, calls url.c:create_conn at line 3579)
hop 5  curl_multi_socket  (/src/curl/lib/multi.c:3288-3296, calls multi.c:multi_socket at line 3292)
hop 5  curl_multi_socket_action  (/src/curl/lib/multi.c:3300-3308, calls multi.c:multi_socket at line 3304)
hop 5  curl_multi_strerror  (/src/curl/lib/strerror.c:364-420, calls curl_multi_perform at line 368)
hop 6  easy.c:wait_or_timeout  (/src/curl/lib/easy.c:541-628, calls curl_multi_socket_action at line 582)
hop 6  curl_multi_add_handle  (/src/curl/lib/multi.c:464-590, calls curl_multi_socket at line 509)
hop 7  easy.c:easy_events  (/src/curl/lib/easy.c:636-645, calls easy.c:wait_or_timeout at line 644)
hop 7  easy.c:easy_perform  (/src/curl/lib/easy.c:706-763, calls curl_multi_add_handle at line 741)
hop 7  Curl_multi_add_perform  (/src/curl/lib/multi.c:1574-1594, calls curl_multi_add_handle at line 1580)
hop 8  curl_easy_perform  (/src/curl/lib/easy.c:771-773, calls easy.c:easy_perform at line 772)
hop 8  curl_easy_perform_ev  (/src/curl/lib/easy.c:781-783, calls easy.c:easy_perform at line 782)
hop 8  http2.c:push_promise  (/src/curl/lib/http2.c:565-663, calls Curl_multi_add_perform at line 633)

==== HIT-COUNT DIVERGENCE (per function) ====
[no significant per-function W/L divergence in the cov dump]


==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  curl_url_strerror  (/src/curl/lib/strerror.c:460-564) ---
  d=1   L 475  T=0 F=10  T=1 F=9  case CURLUE_BAD_PORT_NUMBER:
  d=1   L 526  T=0 F=10  T=7 F=3  case CURLUE_BAD_HOSTNAME:
  d=1   L 529  T=10 F=0  T=0 F=10  case CURLUE_BAD_FILE_URL:  <-- BLOCKER
  d=1   L 538  T=0 F=10  T=2 F=8  case CURLUE_BAD_PATH:

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=279a44f7e64c80a9, size=130 bytes, fuzzer=cmplog, trial=1, discovered_at=1s, mutation_op=BytesCopyMutator,WordInterestingMutator,CrossoverInsertMutator):
  0000: 00 01 00 00 00 19 66 69 6c 65 3a 2f 2f 31 32 00   ......file://12.
  0010: 2e 30 23 30 2e 31 3a 39 00 30 31 2f 38 35 30 00   .0#0.1:9.01/850.
  0020: 02 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 23 6f   ....GFrom: me@#o
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak
Seed 2 (id=63ad41294b23b407, size=130 bytes, fuzzer=cmplog, trial=1, discovered_at=2s, mutation_op=ByteNegMutator,BytesSetMutator):
  0000: 00 01 00 00 00 19 46 49 4c 45 3a 2f 2f 31 32 37   ......FILE://127
  0010: 2e 30 00 00 00 00 00 00 00 00 00 00 38 00 30 00   .0..........8.0.
  0020: 02 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 73 6f   ....GFrom: me@so
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak
Seed 3 (id=532510d6d4d72b60, size=108 bytes, fuzzer=cmplog, trial=1, discovered_at=15s, mutation_op=BytesSwapMutator,BytesDeleteMutator,BytesInsertCopyMutator,ByteRandMutator):
  0000: 00 01 00 00 00 19 46 49 4c 45 3a 2f 2f 31 32 3f   ......FILE://12?
  0010: 2e 00 2e 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   ...0.1:9001/850.
  0020: 16 00 00 00 47 50 72 6f 00 01 00 00 00 19 70 6f   ....GPro......po
  0030: 70 33 3a 2f 2f 31 32 37 2e 30 2e 30 2e 31 3a 39   p3://127.0.0.1:9
Seed 4 (id=722fb44f525b4172, size=43 bytes, fuzzer=cmplog, trial=1, discovered_at=44s, mutation_op=BytesSwapMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 46 49 4c 45 3a 2f 2f 31 32 37   ......FILE://127
  0010: 40 95 23 30 2e 31 3a 39 30 30 31 2f 3a 65 72 00   @.#0.1:9001/:er.
  0020: 20 00 00 00 06 00 65 63 72 65 49                   .....ecreI
Seed 5 (id=3375f472faf6fd2e, size=32 bytes, fuzzer=cmplog, trial=1, discovered_at=827s, mutation_op=ByteAddMutator,DwordAddMutator,BitFlipMutator,BytesSwapMutator,CrossoverInsertMutator):
  0000: 00 01 00 00 00 19 66 69 6c 65 3a 2f 2f 4c 3a 5c   ......file://L:\
  0010: 0a 25 65 41 25 41 44 70 70 18 50 40 7e 35 00 02   .%eA%ADpp.P@~5..

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00182ecc311b5f0b, size=32 bytes, fuzzer=naive, trial=1, discovered_at=3s, mutation_op=BitFlipMutator,BytesRandSetMutator,ByteDecMutator,ByteDecMutator,QwordAddMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 70 6b 2b 2b 2b 2b 2b 2a 2b 2b   ......pk+++++*++
  0010: 2b 2b 4b 2b 1f 1f 1e 1f 1f 40 2f 2f 2f 14 00 00   ++K+.....@///...
Seed 2 (id=00d52fa893f2c30f, size=35 bytes, fuzzer=naive, trial=1, discovered_at=55s, mutation_op=DwordAddMutator,TokenReplace,WordAddMutator,ByteIncMutator):
  0000: 00 01 00 00 00 19 24 25 41 25 30 da 25 46 00 ff   ......$%A%0.%F..
  0010: ff ff ff ff e7 ff 80 ff ff ff da 6f 25 cd 25 38   ...........o%.%8
  0020: 25 00 6f                                          %.o
Seed 3 (id=00f9d8e1a166a48a, size=36 bytes, fuzzer=naive, trial=1, discovered_at=72s, mutation_op=ByteInterestingMutator,CrossoverReplaceMutator,ByteAddMutator,ByteInterestingMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 25 e2 25 25 64 25 65 25 ff 80   ......%.%%d%e%..
  0010: 27 25 43 38 25 50 80 2d 2e 2b 2b 51 59 00 00 6c   '%C8%P.-.++QY..l
  0020: 02 43 63 43                                       .CcC
Seed 4 (id=00078b9eb464eef9, size=33 bytes, fuzzer=naive, trial=1, discovered_at=190s, mutation_op=ByteDecMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 19 2e 2e 2b 2d 2e 2b 2b d4 2b 2c   ........+-.++.+,
  0010: 2f 2f 02 2f 2f 2f d1 00 00 56 28 6d 7e ad 80 72   //.///...V(m~..r
  0020: 56                                                V
Seed 5 (id=00180f1c833e1ad6, size=36 bytes, fuzzer=naive, trial=1, discovered_at=641s, mutation_op=BytesRandSetMutator,DwordAddMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 19 25 61 45 25 61 45 25 25 25 25   ......%aE%aE%%%%
  0010: 65 25 31 42 42 42 42 25 41 45 25 62 eb 00 00 00   e%1BBBB%AE%b....
  0020: 7e 00 00 00                                       ~...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x10                            19(.)x8 28(()x1 23(#)x1             PARTIAL
   0x0006  66(f)x6 46(F)x4                     25(%)x3 70(p)x1 24($)x1 2e(.)x1 +4u  DIFFER
   0x0007  69(i)x6 49(I)x4                     25(%)x2 6b(k)x1 e2(.)x1 2e(.)x1 +5u  DIFFER
   0x0008  6c(l)x6 4c(L)x4                     2b(+)x2 25(%)x2 41(A)x1 45(E)x1 +4u  DIFFER
   0x0009  65(e)x6 45(E)x4                     25(%)x5 2b(+)x1 2d(-)x1 33(3)x1 +2u  DIFFER
   0x000a  3a(:)x10                            2b(+)x2 30(0)x1 64(d)x1 2e(.)x1 +5u  PARTIAL
   0x000b  2f(/)x10                            2b(+)x2 25(%)x2 da(.)x1 45(E)x1 +4u  PARTIAL
   0x000c  2f(/)x9 72(r)x1                     25(%)x4 2b(+)x2 65(e)x1 d0(.)x1 +2u  DIFFER
   0x0017  39(9)x4 70(p)x4 00(.)x1 65(e)x1     25(%)x2 1f(.)x1 ff(.)x1 2d(-)x1 +5u  PARTIAL
   0x0019  30(0)x4 18(.)x3 2f(/)x2 00(.)x1     40(@)x2 ff(.)x1 2b(+)x1 56(V)x1 +5u  DIFFER
   0x001f  00(.)x6 02(.)x3 54(T)x1             00(.)x3 38(8)x1 6c(l)x1 72(r)x1 +4u  PARTIAL
   0x0020  02(.)x3 16(.)x1 20( )x1 72(r)x1     25(%)x2 02(.)x1 56(V)x1 7e(~)x1 +3u  PARTIAL
   0x0021  00(.)x5 65(e)x1                     00(.)x3 43(C)x1 27(')x1 25(%)x1 +1u  PARTIAL
   0x0022  00(.)x5 74(t)x1                     41(A)x2 6f(o)x1 63(c)x1 00(.)x1 +2u  PARTIAL
   0x0023  00(.)x5                             43(C)x1 00(.)x1 56(V)x1 31(1)x1 +1u  PARTIAL
   0x0024  47(G)x4 06(.)x1                     25(%)x1 2f(/)x1                     DIFFER
   0x0025  46(F)x3 50(P)x1 00(.)x1             25(%)x1 d0(.)x1                     DIFFER
   0x0026  72(r)x4 65(e)x1                     25(%)x1 2f(/)x1                     DIFFER
   0x0027  6f(o)x4 63(c)x1                     25(%)x1 00(.)x1                     DIFFER
   0x0028  6d(m)x3 00(.)x1 72(r)x1             32(2)x1 2f(/)x1                     DIFFER
   0x0029  3a(:)x3 01(.)x1 65(e)x1             46(F)x1 2f(/)x1                     DIFFER
   0x002a  20( )x3 00(.)x1 49(I)x1             25(%)x1                             DIFFER
   0x002b  6d(m)x3 00(.)x1                     41(A)x1                             DIFFER
   0x002c  65(e)x3 00(.)x1                     31(1)x1                             DIFFER
   0x002d  40(@)x3 19(.)x1                     25(%)x1                             DIFFER
   0x002e  73(s)x2 23(#)x1 70(p)x1             25(%)x1                             DIFFER
   0x002f  6f(o)x4                             25(%)x1                             DIFFER
   0x0030  6d(m)x3 70(p)x1                     25(%)x1                             DIFFER
   0x0031  65(e)x3 33(3)x1                     27(')x1                             DIFFER
   0x0032  77(w)x3 3a(:)x1                     3e(>)x1                             DIFFER
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
  prompts_b/curl_405.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 405,
  "target": "curl",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 405 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 405 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 405 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).