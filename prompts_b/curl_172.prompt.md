==== BLOCKER ====
Target: curl
Branch ID: 172
Location: /src/curl/lib/http.c:3051:6
Enclosing function: Curl_transferencode
Source line:   if(!Curl_checkheaders(data, STRCONST("TE")) &&
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (calibrated_energy vs minimizer)
cmplog                           6        4          0  REFERENCE
value_profile                    1        9          0  REFERENCE
value_profile_cmplog             5        5          0  REFERENCE
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        8        2          0  winner (calibrated_energy vs naive)
fast                             6        4          0  REFERENCE
grimoire                         5        5          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['minimizer', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: minimizer > naive  [delta: calibrated_energy] ---
  subject 8  (minimizer vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=14.00h  loser=24.00h
  avg hitcount on branch: winner=4  loser=0
  prob_div=0.80  dur_div=10.00h  hit_div=4
  subject-level: delta_AUC=13285080.0  p_AUC=0.0028  delta_Final=134.4  p_final=0.0311

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/172/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_transferencode (/src/curl/lib/http.c:3050-3078) ---
[ ]  3048  #ifdef HAVE_LIBZ
[ ]  3049  CURLcode Curl_transferencode(struct Curl_easy *data)
[B]  3050  {
[B]  3051    if(!Curl_checkheaders(data, STRCONST("TE")) && <-- BLOCKER
[B]  3052       data->set.http_transfer_encoding) {
[ ]  3053      /* When we are to insert a TE: header in the request, we must also insert
[ ]  3054         TE in a Connection: header, so we need to merge the custom provided
[ ]  3055         Connection: header and prevent the original to get sent. Note that if
[ ]  3056         the user has inserted his/her own TE: header we don't do this magic
[ ]  3057         but then assume that the user will handle it all! */
[ ]  3058      char *cptr = Curl_checkheaders(data, STRCONST("Connection"));
[ ]  3059  #define TE_HEADER "TE: gzip\r\n"
[ ]  3060  
[ ]  3061      Curl_safefree(data->state.aptr.te);
[ ]  3062  
[ ]  3063      if(cptr) {
[ ]  3064        cptr = Curl_copy_header_value(cptr);
[ ]  3065        if(!cptr)
[ ]  3066          return CURLE_OUT_OF_MEMORY;
[ ]  3067      }
[ ]  3068  
[ ]  3069      /* Create the (updated) Connection: header */
[ ]  3070      data->state.aptr.te = aprintf("Connection: %s%sTE\r\n" TE_HEADER,
[ ]  3071                                  cptr ? cptr : "", (cptr && *cptr) ? ", ":"");
[ ]  3072  
[ ]  3073      free(cptr);
[ ]  3074      if(!data->state.aptr.te)
[ ]  3075        return CURLE_OUT_OF_MEMORY;
[ ]  3076    }
[B]  3077    return CURLE_OK;
[B]  3078  }

--- Caller (1 hop): Curl_http (/src/curl/lib/http.c:3088-3372, calls Curl_transferencode at line 3197) (±10 around call site) ---
[ ]  3187      data->state.aptr.accept_encoding =
[ ]  3188        aprintf("Accept-Encoding: %s\r\n", data->set.str[STRING_ENCODING]);
[ ]  3189      if(!data->state.aptr.accept_encoding)
[ ]  3190        return CURLE_OUT_OF_MEMORY;
[ ]  3191    }
[B]  3192    else
[B]  3193      Curl_safefree(data->state.aptr.accept_encoding);
[ ]  3194  
[B]  3195  #ifdef HAVE_LIBZ
[ ]  3196    /* we only consider transfer-encoding magic if libz support is built-in */
[B]  3197    result = Curl_transferencode(data); <-- CALL
[B]  3198    if(result)
[ ]  3199      return result;
[B]  3200  #endif
[ ]  3201  
[B]  3202    result = Curl_http_body(data, conn, httpreq, &te);
[B]  3203    if(result)
[ ]  3204      return result;
[ ]  3205  
[B]  3206    p_accept = Curl_checkheaders(data,
[B]  3207                                 STRCONST("Accept"))?NULL:"Accept: */*\r\n";

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_http  (/src/curl/lib/http.c:3088-3372, calls Curl_transferencode at line 3197)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       3        15  http.c:http_setup_conn  (/src/curl/lib/http.c:234-264)
       3        15  Curl_http_output_auth  (/src/curl/lib/http.c:870-943)
       3        15  Curl_buffer_send  (/src/curl/lib/http.c:1295-1471)
       3        15  Curl_http_connect  (/src/curl/lib/http.c:1541-1584)
       3        15  Curl_http_done  (/src/curl/lib/http.c:1675-1721)
       3        15  Curl_use_http_1_1plus  (/src/curl/lib/http.c:1734-1742)
       3        15  http.c:get_http_string  (/src/curl/lib/http.c:1747-1763)
       3        15  Curl_add_custom_headers  (/src/curl/lib/http.c:1853-1996)
       3        15  Curl_add_timecondition  (/src/curl/lib/http.c:2006-2074)
       3        15  Curl_http_method  (/src/curl/lib/http.c:2088-2124)
       3        15  Curl_http_useragent  (/src/curl/lib/http.c:2127-2137)
       3        15  Curl_http_host  (/src/curl/lib/http.c:2141-2230)
       3        15  Curl_http_target  (/src/curl/lib/http.c:2238-2344)
       3        15  Curl_http_body  (/src/curl/lib/http.c:2348-2433)
       3        15  Curl_http_bodysend  (/src/curl/lib/http.c:2437-2772)
... (11 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  Curl_http  (/src/curl/lib/http.c:3088-3372) ---
  d=2   L3105  T=3 F=0  T=15 F=0  if(conn->transport != TRNSPRT_QUIC) {
  d=2   L3106  T=3 F=0  T=15 F=0  if(conn->httpversion < 20) { /* unless the connection is ...
  d=2   L3109  T=0 F=3  T=0 F=15  case CURL_HTTP_VERSION_2:
  d=2   L3116  T=0 F=3  T=0 F=15  case CURL_HTTP_VERSION_1_1:
  d=2   L3119  T=3 F=0  T=15 F=0  default:
  d=2   L3122  T=0 F=3  T=0 F=15  if(data->state.httpwant == CURL_HTTP_VERSION_2_PRIOR_KNOW...
  d=2   L3153  T=0 F=3  T=0 F=15  if(result)
  d=2   L3157  T=0 F=3  T=0 F=15  if(result)
  d=2   L3165  T=0 F=3  T=1 F=14  if(data->state.up.query) {
  d=2   L3167  T=0 F=0  T=0 F=1  if(!pq)
  d=2   L3171  T=0 F=3  T=1 F=14  (pq ? pq : data->state.up.path), FALSE);
  d=2   L3173  T=0 F=3  T=0 F=15  if(result)
  d=2   L3178  T=0 F=3  T=0 F=15  if(data->state.referer && !Curl_checkheaders(data, STRCON...
  d=2   L3184  T=3 F=0  T=15 F=0  if(!Curl_checkheaders(data, STRCONST("Accept-Encoding")) &&
  d=2   L3185  T=0 F=3  T=0 F=15  data->set.str[STRING_ENCODING]) {
  d=2   L3198  T=0 F=3  T=0 F=15  if(result)
  d=2   L3203  T=0 F=3  T=0 F=15  if(result)
  d=2   L3206  T=0 F=3  T=0 F=15  p_accept = Curl_checkheaders(data,
  d=2   L3210  T=0 F=3  T=0 F=15  if(result)
  d=2   L3214  T=0 F=3  T=0 F=15  if(result)
  d=2   L3229  T=3 F=0  T=15 F=0  if(!result)
  d=2   L3231  T=0 F=3  T=0 F=15  if(result) {
  d=2   L3237  T=0 F=3  T=0 F=15  if(conn->bits.altused && !Curl_checkheaders(data, STRCONS...
  d=2   L3263  T=3 F=0  T=15 F=0  (data->state.aptr.host?data->state.aptr.host:""),
  d=2   L3264  T=0 F=3  T=0 F=15  data->state.aptr.proxyuserpwd?
  d=2   L3266  T=3 F=0  T=11 F=4  data->state.aptr.userpwd?data->state.aptr.userpwd:"",
  d=2   L3267  T=0 F=3  T=0 F=15  (data->state.use_range && data->state.aptr.rangeline)?
  d=2   L3269  T=0 F=3  T=0 F=15  (data->set.str[STRING_USERAGENT] &&
  d=2   L3273  T=3 F=0  T=15 F=0  p_accept?p_accept:"",
  d=2   L3274  T=0 F=3  T=0 F=15  data->state.aptr.te?data->state.aptr.te:"",
  d=2   L3275  T=0 F=3  T=0 F=15  (data->set.str[STRING_ENCODING] &&
  d=2   L3279  T=0 F=3  T=0 F=15  (data->state.referer && data->state.aptr.ref)?
  d=2   L3282  T=0 F=3  T=0 F=15  (conn->bits.httpproxy &&
  d=2   L3293  T=0 F=3  T=0 F=15  altused ? altused : ""
  d=2   L3302  T=0 F=3  T=0 F=15  if(result) {
  d=2   L3307  T=3 F=0  T=15 F=0  if(!(conn->handler->flags&PROTOPT_SSL) &&
  d=2   L3308  T=3 F=0  T=15 F=0  conn->httpversion != 20 &&
  d=2   L3309  T=0 F=3  T=0 F=15  (data->state.httpwant == CURL_HTTP_VERSION_2)) {
  d=2   L3320  T=0 F=3  T=0 F=15  if(!result && conn->handler->protocol&(CURLPROTO_WS|CURLP...
  d=2   L3320  T=3 F=0  T=15 F=0  if(!result && conn->handler->protocol&(CURLPROTO_WS|CURLP...
  d=2   L3322  T=3 F=0  T=15 F=0  if(!result)
  d=2   L3324  T=3 F=0  T=15 F=0  if(!result)
  d=2   L3327  T=3 F=0  T=15 F=0  if(!result) {
  d=2   L3329  T=2 F=1  T=15 F=0  if((httpreq == HTTPREQ_GET) ||
  d=2   L3330  T=0 F=1  T=0 F=0  (httpreq == HTTPREQ_HEAD))
  d=2   L3336  T=0 F=3  T=0 F=15  if(result) {
  d=2   L3341  T=3 F=0  T=15 F=0  if((http->postsize > -1) &&
  d=2   L3342  T=2 F=1  T=15 F=0  (http->postsize <= data->req.writebytecount) &&
  d=2   L3343  T=2 F=0  T=15 F=0  (http->sending != HTTPSEND_REQUEST))
  d=2   L3346  T=0 F=3  T=0 F=15  if(data->req.writebytecount) {
  d=2   L3366  T=0 F=3  T=0 F=15  if((conn->httpversion == 20) && data->req.upload_chunky)
--- d=1  Curl_transferencode  (/src/curl/lib/http.c:3050-3078) ---
  d=1   L3051  T=0 F=3  T=15 F=0  if(!Curl_checkheaders(data, STRCONST("TE")) &&  <-- BLOCKER
  d=1   L3052  T=0 F=0  T=0 F=15  data->set.http_transfer_encoding) {

[off-chain: 172 additional divergent branches across 23 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=8d8aab9e31c05a70, size=122 bytes, fuzzer=minimizer, trial=2, discovered_at=39546s, mutation_op=BytesCopyMutator,ByteRandMutator,BytesSetMutator,CrossoverReplaceMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 70 40 33 26 38 4d 6e 6e 91   ......pp@3&8Mnn.
  0010: 6e 6e 66 6e fb 80 00 00 00 46 06 00 00 00 00 00   nnfn.....F......
  0020: 06 00 00 00 00 00 34 00 00 00 00 00 06 00 00 00   ......4.........
  0030: 47 74 65 3b 3b 3b 3b 3b 3b 3b 3b 20 20 80 ff ff   Gte;;;;;;;;  ...
Seed 2 (id=b2f66762ecc53833, size=110 bytes, fuzzer=minimizer, trial=2, discovered_at=40972s, mutation_op=ByteFlipMutator,ByteInterestingMutator,BytesDeleteMutator,TokenReplace):
  0000: 00 01 00 00 00 19 70 70 40 33 26 38 4d 6e 6e 91   ......pp@3&8Mnn.
  0010: 6e 6e 66 6e fb 80 00 00 00 46 06 00 00 00 00 00   nnfn.....F......
  0020: 06 00 00 00 47 74 65 3b 3b 3b 3b 3b 3b 3b 3b 20   ....Gte;;;;;;;; 
  0030: 20 80 ff ff ff 3b 20 20 09 86 20 0a 64 73 61 5f    ....;  .. .dsa_
Seed 3 (id=4b4bc313934f77d1, size=122 bytes, fuzzer=minimizer, trial=2, discovered_at=67270s, mutation_op=ByteInterestingMutator,QwordAddMutator,DwordAddMutator):
  0000: 00 01 00 00 00 19 70 70 40 33 26 38 4d 6e 6e 91   ......pp@3&8Mnn.
  0010: 6e 6e 66 6e fb 80 00 00 00 46 06 00 00 00 00 00   nnfn.....F......
  0020: 06 00 00 00 00 00 19 00 00 00 00 00 06 00 00 00   ................
  0030: 47 74 65 3b 3b 3b 3b 3b 3b 3b 3b 20 20 80 ff ff   Gte;;;;;;;;  ...

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=0024e5972fc0b2e0, size=35 bytes, fuzzer=naive, trial=1, discovered_at=88s, mutation_op=WordAddMutator):
  0000: 00 01 00 00 00 19 25 60 25 61 3e 66 9f 9f 63 25   ......%`%a>f..c%
  0010: 2b 5d 25 41 bf 41 41 41 41 40 41 41 5a 70 65 72   +]%A.AAAA@AAZper
  0020: 6d 69 74                                          mit
Seed 2 (id=00430153b42aa78b, size=35 bytes, fuzzer=naive, trial=1, discovered_at=175s, mutation_op=BytesDeleteMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 70 6b 73 65 2e 2e 2e 45 2e 41   ......pkse...E.A
  0010: 2e 2b 6b 73 65 4d 2e 2e 45 2b 2b 2b 2b 2b 2b 2b   .+kseM..E+++++++
  0020: 2b 55 6b                                          +Uk
Seed 3 (id=0036ed920052a1c1, size=35 bytes, fuzzer=naive, trial=1, discovered_at=626s, mutation_op=ByteIncMutator,ByteInterestingMutator):
  0000: 00 01 00 00 00 19 43 41 25 64 61 25 41 25 64 61   ......CA%da%A%da
  0010: 25 43 66 25 25 43 40 25 00 19 70 6b 2e 44 43 43   %Cf%%C@%..pk.DCC
  0020: 01 43 44                                          .CD
Seed 4 (id=004f868e7ea91716, size=36 bytes, fuzzer=naive, trial=1, discovered_at=3286s, mutation_op=ByteDecMutator,CrossoverInsertMutator,DwordInterestingMutator,BytesCopyMutator,BytesDeleteMutator,ByteNegMutator):
  0000: 00 01 00 00 00 19 26 41 41 25 25 29 25 62 25 29   ......&AA%%)%b%)
  0010: 25 62 2d 2d 2e 41 4b db 44 40 25 44 45 45 45 bb   %b--.AK.D@%DEEE.
  0020: 25 25 2a bb                                       %%*.
Seed 5 (id=000200d3c60deab7, size=35 bytes, fuzzer=naive, trial=1, discovered_at=4950s, mutation_op=ByteAddMutator):
  0000: 00 01 00 00 00 19 70 72 2d 2e 2d 65 2e 2e 2d 2d   ......pr-.-e..--
  0010: 2d 2d 2d 2d 65 2e 2d 2d 2d 2d 2d 2d 48 2e 2d 31   ----e.------H.-1
  0020: 2d 2d 2d                                          ---


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x3                             19(.)x10 25(%)x1 1e(.)x1 27(')x1 +2u  PARTIAL
   0x0006  70(p)x3                             25(%)x5 70(p)x3 43(C)x2 26(&)x1 +4u  PARTIAL
   0x0007  70(p)x3                             25(%)x3 41(A)x2 60(`)x1 6b(k)x1 +8u  DIFFER
   0x0008  40(@)x3                             25(%)x3 43(C)x3 41(A)x2 2d(-)x2 +5u  DIFFER
   0x0009  33(3)x3                             65(e)x2 25(%)x2 41(A)x2 61(a)x1 +8u  DIFFER
   0x000a  26(&)x3                             25(%)x7 2d(-)x2 3e(>)x1 2e(.)x1 +4u  DIFFER
   0x000b  38(8)x3                             25(%)x3 63(c)x2 66(f)x1 2e(.)x1 +8u  DIFFER
   0x000c  4d(M)x3                             2e(.)x3 41(A)x2 25(%)x2 9f(.)x1 +7u  DIFFER
   0x000d  6e(n)x3                             25(%)x4 45(E)x2 41(A)x2 9f(.)x1 +6u  DIFFER
   0x000e  6e(n)x3                             25(%)x4 2d(-)x2 63(c)x1 2e(.)x1 +7u  DIFFER
   0x000f  91(.)x3                             25(%)x4 41(A)x3 61(a)x2 29())x1 +5u  DIFFER
   0x0010  6e(n)x3                             25(%)x4 2d(-)x2 44(D)x2 2b(+)x1 +6u  DIFFER
   0x0011  6e(n)x3                             25(%)x5 2d(-)x2 5d(])x1 2b(+)x1 +6u  DIFFER
   0x0012  66(f)x3                             25(%)x5 66(f)x2 2d(-)x2 41(A)x2 +4u  PARTIAL
   0x0013  6e(n)x3                             25(%)x4 2d(-)x3 41(A)x2 46(F)x2 +4u  DIFFER
   0x0014  fb(.)x3                             25(%)x4 65(e)x2 bf(.)x1 2e(.)x1 +7u  DIFFER
   0x0015  80(.)x3                             41(A)x4 25(%)x4 4d(M)x1 43(C)x1 +5u  DIFFER
   0x0016  00(.)x3                             41(A)x3 2d(-)x2 25(%)x2 2e(.)x1 +7u  DIFFER
   0x0017  00(.)x3                             25(%)x6 41(A)x2 2d(-)x2 43(C)x2 +3u  DIFFER
   0x0018  00(.)x3                             45(E)x3 25(%)x3 43(C)x2 41(A)x1 +6u  PARTIAL
   0x0019  46(F)x3                             40(@)x2 25(%)x2 44(D)x2 2b(+)x1 +8u  PARTIAL
   0x001a  06(.)x3                             25(%)x5 41(A)x1 2b(+)x1 70(p)x1 +7u  DIFFER
   0x001b  00(.)x3                             25(%)x3 44(D)x2 2d(-)x2 00(.)x2 +6u  PARTIAL
   0x001c  00(.)x3                             45(E)x2 40(@)x2 25(%)x2 5a(Z)x1 +8u  PARTIAL
   0x001d  00(.)x3                             70(p)x1 2b(+)x1 44(D)x1 45(E)x1 +11u  DIFFER
   0x001e  00(.)x3                             ff(.)x2 25(%)x2 65(e)x1 2b(+)x1 +9u  DIFFER
   0x001f  00(.)x3                             41(A)x2 40(@)x2 72(r)x1 2b(+)x1 +9u  PARTIAL
   0x0020  06(.)x3                             25(%)x3 6d(m)x1 2b(+)x1 01(.)x1 +9u  PARTIAL
   0x0021  00(.)x3                             2d(-)x3 25(%)x2 00(.)x2 69(i)x1 +6u  PARTIAL
   0x0022  00(.)x3                             44(D)x2 74(t)x1 6b(k)x1 2a(*)x1 +8u  PARTIAL
   0x0023  00(.)x3                             25(%)x2 bb(.)x1 4c(L)x1 2d(-)x1 +2u  PARTIAL
   0x0024  00(.)x2 47(G)x1                     50(P)x2 25(%)x2 cd(.)x1 47(G)x1     PARTIAL
   0x0025  00(.)x2 74(t)x1                     25(%)x3 41(A)x2 2e(.)x1             DIFFER
   0x0026  34(4)x1 65(e)x1 19(.)x1             25(%)x2 66(f)x1 67(g)x1 46(F)x1 +1u  DIFFER
   0x0027  00(.)x2 3b(;)x1                     40(@)x1 25(%)x1 2d(-)x1 46(F)x1 +1u  DIFFER
   0x0028  00(.)x2 3b(;)x1                     25(%)x2 44(D)x1 50(P)x1 ff(.)x1     DIFFER
   0x0029  00(.)x2 3b(;)x1                     25(%)x1 66(f)x1 2d(-)x1 32(2)x1 +1u  DIFFER
   0x002a  00(.)x2 3b(;)x1                     25(%)x3 44(D)x1 ff(.)x1             DIFFER
   0x002b  00(.)x2 3b(;)x1                     25(%)x3 2e(.)x1 7f(.)x1             DIFFER
   0x002c  06(.)x2 3b(;)x1                     d2(.)x1 43(C)x1 65(e)x1 46(F)x1 +1u  DIFFER
   ... (19 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
--- minimizer ---
**Instrumentation**: naive's edge counters only.

**Feedback**: naive's edge-bucket `MaxMapFeedback`, plus a
`CalibrationStage` that measures each new corpus entry's execution
time, edge-map fill, and stability into `SchedulerMetadata`/testcase
metadata.

**Mutators / stages**: havoc + token mutator (`LineageMutator`, names
captured) run inside a `StdPowerMutationalStage` rather than naive's
plain `StdMutationalStage`. Stages are `[calibration, power]`. The
power stage derives the number of havoc mutations per seed visit (the
"energy") from a calibration-based `perf_score` — faster, smaller,
more-stable seeds earn more mutations. PowerSchedule is `None`, so the
energy uses ONLY intrinsic calibration and is NOT weighted by how often
a region has been hit. Corpus selection is plain FIFO `QueueScheduler`
(same order as naive).

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge, plus a one-time
calibration burst per new corpus entry.

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
  prompts_b/curl_172.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 172,
  "target": "curl",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [minimizer>naive (calibrated_energy)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 172 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 172 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 172 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).