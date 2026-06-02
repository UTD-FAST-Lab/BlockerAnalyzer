==== BLOCKER ====
Target: curl
Branch ID: 166
Location: /src/curl/lib/http.c:2797:9
Enclosing function: Curl_http_cookies
Source line:         !strcmp(host, "127.0.0.1") ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        3        7          0  REFERENCE
naive_ngram4                     3        7          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.60h  loser=21.70h
  avg hitcount on branch: winner=9  loser=0
  prob_div=0.80  dur_div=15.10h  hit_div=8
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.20h  loser=21.40h
  avg hitcount on branch: winner=10  loser=0
  prob_div=0.70  dur_div=15.20h  hit_div=10
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/166/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_http_cookies (/src/curl/lib/http.c:2779-2846) ---
[ ]  2777                             struct connectdata *conn,
[ ]  2778                             struct dynbuf *r)
[B]  2779  {
[B]  2780    CURLcode result = CURLE_OK;
[B]  2781    char *addcookies = NULL;
[B]  2782    bool linecap = FALSE;
[B]  2783    if(data->set.str[STRING_COOKIE] &&
[B]  2784       !Curl_checkheaders(data, STRCONST("Cookie")))
[W]  2785      addcookies = data->set.str[STRING_COOKIE];
[ ]  2786  
[B]  2787    if(data->cookies || addcookies) {
[B]  2788      struct Cookie *co = NULL; /* no cookies from start */
[B]  2789      int count = 0;
[ ]  2790  
[B]  2791      if(data->cookies && data->state.cookie_engine) {
[B]  2792        const char *host = data->state.aptr.cookiehost ?
[B]  2793          data->state.aptr.cookiehost : conn->host.name;
[B]  2794        const bool secure_context =
[B]  2795          conn->handler->protocol&(CURLPROTO_HTTPS|CURLPROTO_WSS) ||
[B]  2796          strcasecompare("localhost", host) ||
[B]  2797          !strcmp(host, "127.0.0.1") || <-- BLOCKER
[B]  2798          !strcmp(host, "[::1]") ? TRUE : FALSE;
[B]  2799        Curl_share_lock(data, CURL_LOCK_DATA_COOKIE, CURL_LOCK_ACCESS_SINGLE);
[B]  2800        co = Curl_cookie_getlist(data, data->cookies, host, data->state.up.path,
[B]  2801                                 secure_context);
[B]  2802        Curl_share_unlock(data, CURL_LOCK_DATA_COOKIE);
[B]  2803      }
[B]  2804      if(co) {
[ ]  2805        struct Cookie *store = co;
[ ]  2806        /* now loop through all cookies that matched */
[ ]  2807        while(co) {
[ ]  2808          if(co->value) {
[ ]  2809            if(0 == count) {
[ ]  2810              result = Curl_dyn_addn(r, STRCONST("Cookie: "));
[ ]  2811              if(result)
[ ]  2812                break;
[ ]  2813            }
[ ]  2814            if((Curl_dyn_len(r) + strlen(co->name) + strlen(co->value) + 1) >=
[ ]  2815               MAX_COOKIE_HEADER_LEN) {
[ ]  2816              infof(data, "Restricted outgoing cookies due to header size, "
[ ]  2817                    "'%s' not sent", co->name);
[ ]  2818              linecap = TRUE;
[ ]  2819              break;
[ ]  2820            }
[ ]  2821            result = Curl_dyn_addf(r, "%s%s=%s", count?"; ":"",
[ ]  2822                                   co->name, co->value);
[ ]  2823            if(result)
[ ]  2824              break;
[ ]  2825            count++;
[ ]  2826          }
[ ]  2827          co = co->next; /* next cookie please */
[ ]  2828        }
[ ]  2829        Curl_cookie_freelist(store);
[ ]  2830      }
[B]  2831      if(addcookies && !result && !linecap) {
[W]  2832        if(!count)
[W]  2833          result = Curl_dyn_addn(r, STRCONST("Cookie: "));
[W]  2834        if(!result) {
[W]  2835          result = Curl_dyn_addf(r, "%s%s", count?"; ":"", addcookies);
[W]  2836          count++;
[W]  2837        }
[W]  2838      }
[B]  2839      if(count && !result)
[W]  2840        result = Curl_dyn_addn(r, STRCONST("\r\n"));
[ ]  2841  
[B]  2842      if(result)
[ ]  2843        return result;
[B]  2844    }
[B]  2845    return result;
[B]  2846  }

--- Caller (1 hop): Curl_http (/src/curl/lib/http.c:3088-3372, calls Curl_http_cookies at line 3319) (±10 around call site) ---
[B]  3309       (data->state.httpwant == CURL_HTTP_VERSION_2)) {
[ ]  3310      /* append HTTP2 upgrade magic stuff to the HTTP request if it isn't done
[ ]  3311         over SSL */
[ ]  3312      result = Curl_http2_request_upgrade(&req, data);
[ ]  3313      if(result) {
[ ]  3314        Curl_dyn_free(&req);
[ ]  3315        return result;
[ ]  3316      }
[ ]  3317    }
[ ]  3318  
[B]  3319    result = Curl_http_cookies(data, conn, &req); <-- CALL
[B]  3320    if(!result && conn->handler->protocol&(CURLPROTO_WS|CURLPROTO_WSS))
[ ]  3321      result = Curl_ws_request(data, &req);
[B]  3322    if(!result)
[B]  3323      result = Curl_add_timecondition(data, &req);
[B]  3324    if(!result)
[B]  3325      result = Curl_add_custom_headers(data, FALSE, &req);
[ ]  3326  
[B]  3327    if(!result) {
[B]  3328      http->postdata = NULL;  /* nothing to post at this point */
[B]  3329      if((httpreq == HTTPREQ_GET) ||

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_http  (/src/curl/lib/http.c:3088-3372, calls Curl_http_cookies at line 3319)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       1         0  http.c:expect100  (/src/curl/lib/http.c:1770-1792)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  Curl_http  (/src/curl/lib/http.c:3088-3372) ---
  d=2   L3165  T=10 F=3  T=0 F=20  if(data->state.up.query) {
  d=2   L3167  T=0 F=10  T=0 F=0  if(!pq)
  d=2   L3171  T=10 F=3  T=0 F=20  (pq ? pq : data->state.up.path), FALSE);
  d=2   L3185  T=1 F=12  T=0 F=20  data->set.str[STRING_ENCODING]) {
  d=2   L3189  T=0 F=1  T=0 F=0  if(!data->state.aptr.accept_encoding)
  d=2   L3275  T=1 F=12  T=0 F=20  (data->set.str[STRING_ENCODING] &&
  d=2   L3276  T=1 F=0  T=0 F=0  *data->set.str[STRING_ENCODING] &&
  d=2   L3277  T=1 F=0  T=0 F=0  data->state.aptr.accept_encoding)?
  d=2   L3330  T=0 F=4  T=0 F=1  (httpreq == HTTPREQ_HEAD))
  d=2   L3343  T=9 F=0  T=19 F=0  (http->sending != HTTPSEND_REQUEST))
--- d=1  Curl_http_cookies  (/src/curl/lib/http.c:2779-2846) ---
  d=1   L2783  T=1 F=12  T=0 F=20  if(data->set.str[STRING_COOKIE] &&
  d=1   L2784  T=1 F=0  T=0 F=0  !Curl_checkheaders(data, STRCONST("Cookie")))
  d=1   L2797  T=13 F=0  T=0 F=20  !strcmp(host, "127.0.0.1") ||  <-- BLOCKER
  d=1   L2798  T=0 F=0  T=0 F=20  !strcmp(host, "[::1]") ? TRUE : FALSE;
  d=1   L2831  T=1 F=0  T=0 F=0  if(addcookies && !result && !linecap) {
  d=1   L2831  T=1 F=12  T=0 F=20  if(addcookies && !result && !linecap) {
  d=1   L2831  T=1 F=0  T=0 F=0  if(addcookies && !result && !linecap) {
  d=1   L2832  T=1 F=0  T=0 F=0  if(!count)
  d=1   L2834  T=1 F=0  T=0 F=0  if(!result) {
  d=1   L2835  T=0 F=1  T=0 F=0  result = Curl_dyn_addf(r, "%s%s", count?"; ":"", addcooki...
  d=1   L2839  T=1 F=12  T=0 F=20  if(count && !result)
  d=1   L2839  T=1 F=0  T=0 F=0  if(count && !result)

[off-chain: 77 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=3d12195f812303ed, size=130 bytes, fuzzer=cmplog, trial=1, discovered_at=4s, mutation_op=BytesInsertCopyMutator,QwordAddMutator,ByteInterestingMutator,TokenInsert,ByteAddMutator,ByteDecMutator):
  0000: 00 01 00 00 00 19 48 54 54 50 3a 2f 2f 31 32 37   ......HTTP://127
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 3f 2f 38 35 30 00   .0.0.1:900?/850.
  0020: 02 00 00 00 47 46 50 6f 6d 3a 20 6d 44 40 38 6f   ....GFPom: mD@8o
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak
Seed 2 (id=0cb8456462e8bda9, size=111 bytes, fuzzer=value_profile_cmplog, trial=2, discovered_at=5s, mutation_op=BytesDeleteMutator,DwordInterestingMutator,WordInterestingMutator,BytesSetMutator,CrossoverInsertMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 19 48 54 54 50 3a 2f 2f 31 32 37   ......HTTP://127
  0010: 2e 30 2e 30 2e 31 3a 39 2f 30 31 2f 38 35 30 00   .0.0.1:9/01/850.
  0020: 19 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 68 6f   ....GFrom: me@ho
  0030: 6d 65 77 61 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewaere..To: fak
Seed 3 (id=07cf12750965cfe9, size=130 bytes, fuzzer=cmplog, trial=1, discovered_at=19s, mutation_op=BytesDeleteMutator,BytesInsertMutator,BytesSetMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 48 54 54 50 3a 2f 2f 31 32 37   ......HTTP://127
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 3f 2f 38 35 30 00   .0.0.1:900?/850.
  0020: 02 00 00 00 47 46 72 6f 6d 3a 20 6d 2f 40 38 6f   ....GFrom: m/@8o
  0030: 6d 65 77 68 65 37 65 0d 0a 54 6f 3a 20 66 61 6b   mewhe7e..To: fak
Seed 4 (id=137673e7a361301c, size=130 bytes, fuzzer=cmplog, trial=1, discovered_at=19s, mutation_op=ByteInterestingMutator,WordInterestingMutator,QwordAddMutator,BytesInsertMutator):
  0000: 00 01 00 00 00 19 48 54 54 50 3a 2f 2f 31 32 37   ......HTTP://127
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 2f 2f 38 35 30 00   .0.0.1:900//850.
  0020: 34 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 38 6f   4...GFrom: me@8o
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak
Seed 5 (id=24b71e755ab532ba, size=130 bytes, fuzzer=cmplog, trial=1, discovered_at=19s, mutation_op=BytesDeleteMutator,BytesInsertMutator,BytesSetMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 48 54 54 50 3a 2f 2f 31 32 37   ......HTTP://127
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 3f 2f 38 35 30 00   .0.0.1:900?/850.
  0020: 02 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 38 6f   ....GFrom: me@8o
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003e4994f2c65fcf, size=35 bytes, fuzzer=value_profile, trial=1, discovered_at=22s, mutation_op=QwordAddMutator,WordAddMutator):
  0000: 00 01 00 00 00 19 30 49 2e 2e 51 2e 47 48 2e 2b   ......0I..Q.GH.+
  0010: 80 00 21 47 47 46 0f 00 00 00 f9 ff ff ff 49 62   ..!GGF........Ib
  0020: 7e 05 61                                          ~.a
Seed 2 (id=00225bc4819174d2, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=152s, mutation_op=BytesInsertMutator,ByteAddMutator,ByteIncMutator,BytesDeleteMutator,ByteDecMutator):
  0000: 00 01 00 00 00 43 64 55 43 25 25 25 25 21 25 65   .....CdUC%%%%!%e
  0010: 26 25 65 24 25 64 45 72 46 25 41 27 25 31 25 25   &%e$%dErF%A'%1%%
  0020: 65 25 44 d6 42 64 45 72 33 25 65 4b 25 43 25 25   e%D.BdEr3%eK%C%%
  0030: 25 25 25 25 25 25 25 25 25 25 25 25 26 25 40 e8   %%%%%%%%%%%%&%@.
Seed 3 (id=00349fd4a3c6fb4f, size=36 bytes, fuzzer=naive, trial=3, discovered_at=486s, mutation_op=BytesSetMutator,BytesSwapMutator):
  0000: 00 01 00 00 00 19 2b 2b 2b 2b 2b 2b 70 72 2b 2b   ......++++++pr++
  0010: 2b 2b 2b 2e 2e 2b 2b 2b 2b 2b 2b 2b 2b 2e 2e 2e   +++..++++++++...
  0020: 2e 2b 2b 2b                                       .+++
Seed 4 (id=00406322c903f711, size=56 bytes, fuzzer=naive, trial=3, discovered_at=3784s, mutation_op=BytesSetMutator):
  0000: 00 01 00 00 00 2f 25 36 36 36 ca 36 36 36 36 36   ...../%666.66666
  0010: 37 25 25 36 36 36 36 36 36 25 25 36 36 36 36 36   7%%666666%%66666
  0020: 36 36 36 36 37 25 25 25 36 25 88 88 88 88 88 88   66667%%%6%......
  0030: 88 25 40 52 41 4e 44 00                           .%@RAND.
Seed 5 (id=001607afc7f08ce7, size=74 bytes, fuzzer=value_profile, trial=1, discovered_at=3913s, mutation_op=BytesCopyMutator):
  0000: 00 01 00 00 00 44 64 55 43 db b5 25 45 66 25 66   .....DdUC..%Ef%f
  0010: 42 62 9e 62 9e 44 64 55 43 db b5 25 45 66 25 66   Bb.b.DdUC..%Ef%f
  0020: 42 62 9e 62 9e 43 41 27 db 31 25 25 25 25 26 55   Bb.b.CA'.1%%%%&U
  0030: 43 db b5 25 45 66 25 65 42 62 9e 66 52 66 25 65   C..%Ef%eBb.fRf%e


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x13                            19(.)x6 2e(.)x6 43(C)x3 2f(/)x1 +4u  PARTIAL
   0x0006  48(H)x13                            25(%)x5 64(d)x4 2e(.)x4 47(G)x2 +5u  DIFFER
   0x0007  54(T)x13                            2e(.)x3 55(U)x2 49(I)x1 2b(+)x1 +13u  DIFFER
   0x0008  54(T)x13                            2e(.)x4 43(C)x3 2b(+)x2 62(b)x2 +9u  DIFFER
   0x0009  50(P)x13                            25(%)x5 2b(+)x3 2e(.)x1 36(6)x1 +10u  DIFFER
   0x000a  3a(:)x13                            25(%)x3 2e(.)x3 2b(+)x2 51(Q)x1 +11u  DIFFER
   0x000b  2f(/)x13                            25(%)x4 2e(.)x2 2b(+)x2 42(B)x2 +10u  PARTIAL
   0x000c  2f(/)x12 40(@)x1                    2e(.)x3 25(%)x2 70(p)x2 47(G)x1 +12u  PARTIAL
   0x000d  31(1)x13                            2e(.)x5 25(%)x3 00(.)x2 48(H)x1 +9u  PARTIAL
   0x000e  32(2)x13                            2e(.)x5 25(%)x5 00(.)x3 37(7)x2 +5u  DIFFER
   0x000f  37(7)x13                            2e(.)x3 2b(+)x2 2f(/)x2 25(%)x2 +11u  DIFFER
   0x0010  2e(.)x13                            2e(.)x6 37(7)x2 42(B)x2 25(%)x2 +8u  PARTIAL
   0x0011  30(0)x13                            25(%)x7 00(.)x2 2b(+)x2 2e(.)x2 +7u  PARTIAL
   0x0012  2e(.)x13                            25(%)x3 21(!)x2 2b(+)x2 2f(/)x2 +10u  PARTIAL
   0x0013  30(0)x13                            2e(.)x3 62(b)x2 64(d)x2 47(G)x1 +12u  PARTIAL
   0x0014  2e(.)x13                            25(%)x5 2e(.)x5 47(G)x1 36(6)x1 +8u  PARTIAL
   0x0015  31(1)x13                            46(F)x3 25(%)x3 64(d)x2 2f(/)x2 +9u  PARTIAL
   0x0016  3a(:)x12 2f(/)x1                    64(d)x2 2f(/)x2 25(%)x2 2e(.)x2 +11u  PARTIAL
   0x0017  39(9)x12 3f(?)x1                    2e(.)x4 46(F)x2 00(.)x1 72(r)x1 +11u  PARTIAL
   0x0018  30(0)x11 2f(/)x2                    2e(.)x4 25(%)x2 00(.)x1 46(F)x1 +11u  PARTIAL
   0x0019  30(0)x13                            25(%)x4 2b(+)x3 42(B)x2 00(.)x1 +9u  PARTIAL
   0x001a  3f(?)x9 31(1)x2 2f(/)x1 23(#)x1     25(%)x3 41(A)x2 2e(.)x2 f9(.)x1 +11u  PARTIAL
   0x001b  2f(/)x12 25(%)x1                    25(%)x4 2e(.)x3 27(')x2 ff(.)x1 +9u  PARTIAL
   0x001c  38(8)x13                            25(%)x3 2b(+)x2 2f(/)x2 2e(.)x2 +10u  PARTIAL
   0x001d  35(5)x13                            2e(.)x4 25(%)x2 ff(.)x1 31(1)x1 +11u  PARTIAL
   0x001e  30(0)x13                            25(%)x5 2e(.)x2 49(I)x1 36(6)x1 +10u  PARTIAL
   0x001f  00(.)x13                            25(%)x5 2e(.)x3 37(7)x2 62(b)x1 +8u  PARTIAL
   0x0021  00(.)x13                            25(%)x3 00(.)x2 42(B)x2 64(d)x2 +9u  PARTIAL
   0x0022  00(.)x13                            00(.)x2 2e(.)x2 61(a)x1 44(D)x1 +11u  PARTIAL
   0x0023  00(.)x13                            2e(.)x4 25(%)x2 d6(.)x1 2b(+)x1 +8u  PARTIAL
   0x0024  47(G)x13                            2e(.)x3 46(F)x2 42(B)x1 37(7)x1 +7u  PARTIAL
   0x0025  46(F)x12 50(P)x1                    25(%)x4 2e(.)x3 43(C)x2 64(d)x1 +4u  PARTIAL
   0x0026  72(r)x12 50(P)x1                    25(%)x2 2e(.)x2 45(E)x1 41(A)x1 +8u  PARTIAL
   0x0027  6f(o)x13                            25(%)x3 72(r)x1 27(')x1 32(2)x1 +8u  PARTIAL
   0x0028  6d(m)x13                            25(%)x4 2e(.)x2 33(3)x1 36(6)x1 +6u  DIFFER
   0x0029  3a(:)x13                            25(%)x2 31(1)x1 8b(.)x1 e3(.)x1 +9u  DIFFER
   0x002a  20( )x13                            25(%)x2 65(e)x1 88(.)x1 8b(.)x1 +9u  DIFFER
   0x002b  6d(m)x13                            25(%)x2 4b(K)x1 88(.)x1 32(2)x1 +9u  DIFFER
   0x002c  65(e)x11 44(D)x1 2f(/)x1            25(%)x2 45(E)x2 2e(.)x2 88(.)x1 +7u  PARTIAL
   0x002d  40(@)x13                            25(%)x2 2e(.)x2 43(C)x1 88(.)x1 +8u  PARTIAL
   ... (18 more divergent offsets)
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
  prompts_b/curl_166.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 166,
  "target": "curl",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 166 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 166 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 166 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).