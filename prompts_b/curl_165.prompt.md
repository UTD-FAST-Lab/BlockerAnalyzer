==== BLOCKER ====
Target: curl
Branch ID: 165
Location: /src/curl/lib/http.c:2792:26
Enclosing function: Curl_http_cookies
Source line:       const char *host = data->state.aptr.cookiehost ?
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        2        8          0  loser (aflfast_rarity vs fast)
fast                             8        2          0  winner (aflfast_rarity vs minimizer)
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'fast', 'minimizer', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'grimoire']

==== DECISIVE PAIRS (3) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.40h  loser=24.00h
  avg hitcount on branch: winner=174  loser=0
  prob_div=1.00  dur_div=23.60h  hit_div=174
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.70h  loser=24.00h
  avg hitcount on branch: winner=92  loser=0
  prob_div=1.00  dur_div=23.30h  hit_div=92
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002
--- Pair 3: fast > minimizer  [delta: aflfast_rarity] ---
  subject 9  (fast vs minimizer, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=11.60h  loser=22.40h
  avg hitcount on branch: winner=214  loser=53
  prob_div=0.60  dur_div=10.80h  hit_div=161
  subject-level: delta_AUC=11508300.0  p_AUC=0.1041  delta_Final=477.3  p_final=0.0172

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/165/{W,L}/branch_coverage_show.txt

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
[B]  2792        const char *host = data->state.aptr.cookiehost ? <-- BLOCKER
[B]  2793          data->state.aptr.cookiehost : conn->host.name;
[B]  2794        const bool secure_context =
[B]  2795          conn->handler->protocol&(CURLPROTO_HTTPS|CURLPROTO_WSS) ||
[B]  2796          strcasecompare("localhost", host) ||
[B]  2797          !strcmp(host, "127.0.0.1") ||
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
      30         0  Curl_copy_header_value  (/src/curl/lib/http.c:315-359)
       2        16  http.c:http_output_basic  (/src/curl/lib/http.c:369-421)
       2        16  http.c:output_auth_headers  (/src/curl/lib/http.c:736-846)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  Curl_http  (/src/curl/lib/http.c:3088-3372) ---
  d=2   L3165  T=16 F=14  T=0 F=30  if(data->state.up.query) {
  d=2   L3167  T=0 F=16  T=0 F=0  if(!pq)
  d=2   L3171  T=16 F=14  T=0 F=30  (pq ? pq : data->state.up.path), FALSE);
  d=2   L3267  T=1 F=29  T=0 F=30  (data->state.use_range && data->state.aptr.rangeline)?
  d=2   L3267  T=1 F=0  T=0 F=0  (data->state.use_range && data->state.aptr.rangeline)?
  d=2   L3269  T=1 F=29  T=0 F=30  (data->set.str[STRING_USERAGENT] &&
  d=2   L3270  T=1 F=0  T=0 F=0  *data->set.str[STRING_USERAGENT] &&
  d=2   L3271  T=1 F=0  T=0 F=0  data->state.aptr.uagent)?
  d=2   L3330  T=0 F=1  T=0 F=2  (httpreq == HTTPREQ_HEAD))
--- d=1  Curl_http_cookies  (/src/curl/lib/http.c:2779-2846) ---
  d=1   L2783  T=1 F=29  T=0 F=30  if(data->set.str[STRING_COOKIE] &&
  d=1   L2784  T=1 F=0  T=0 F=0  !Curl_checkheaders(data, STRCONST("Cookie")))
  d=1   L2792  T=30 F=0  T=0 F=30  const char *host = data->state.aptr.cookiehost ?  <-- BLOCKER
  d=1   L2831  T=1 F=0  T=0 F=0  if(addcookies && !result && !linecap) {
  d=1   L2831  T=1 F=29  T=0 F=30  if(addcookies && !result && !linecap) {
  d=1   L2831  T=1 F=0  T=0 F=0  if(addcookies && !result && !linecap) {
  d=1   L2832  T=1 F=0  T=0 F=0  if(!count)
  d=1   L2834  T=1 F=0  T=0 F=0  if(!result) {
  d=1   L2835  T=0 F=1  T=0 F=0  result = Curl_dyn_addf(r, "%s%s", count?"; ":"", addcooki...
  d=1   L2839  T=1 F=29  T=0 F=30  if(count && !result)
  d=1   L2839  T=1 F=0  T=0 F=0  if(count && !result)

[off-chain: 103 additional divergent branches across 11 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=03a52d351064c850, size=109 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2562s, mutation_op=BytesDeleteMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 4b 2f 2f 3f 32 37   ......pop.K//?27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 25 38 35 30 00   .0.0.1:9001%850.
  0020: 06 00 00 00 47 48 6f 73 74 3a e8 6d 2d 40 36 6f   ....GHost:.m-@6o
  0030: 6d 65 77 68 65 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5 a5   mewhe...........
Seed 2 (id=040204616893a098, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4409s, mutation_op=TokenReplace,TokenInsert):
  0000: 00 01 00 00 00 19 70 6f 70 00 4b 2f 2f 3f 32 37   ......pop.K//?27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 25 38 35 30 00   .0.0.1:9001%850.
  0020: 06 00 00 00 47 48 6f 73 74 3a 09 6f 76 76 00 6f   ....GHost:.ovv.o
  0030: 6d 65 77 68 65 72 00 00 00 54 6f 3a 20 66 61 6b   mewher...To: fak
Seed 3 (id=00298212dcacab05, size=111 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4710s, mutation_op=BytesRandInsertMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b ad 2f 3f 32 37   ......pop3K./?27
  0010: 00 30 2e 30 2e 31 3a 6e 30 30 31 00 38 35 30 00   .0.0.1:n001.850.
  0020: 06 00 00 00 47 48 6f 73 74 3a 09 0a 09 0a 09 20   ....GHost:..... 
  0030: 0d 0d 0d 0d 96 0d 0d 4f 6f 6e 57 76 ff 63 34 6e   .......OonWv.c4n
Seed 4 (id=0a3f81ed7ca3e7e4, size=119 bytes, fuzzer=cmplog, trial=1, discovered_at=4812s, mutation_op=BytesSetMutator):
  0000: 00 01 00 00 00 19 57 53 00 54 3a 2f 2f 00 32 37   ......WS.T://.27
  0010: 2e b0 23 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   ..#0.1:9001/850.
  0020: 06 00 00 00 47 48 6f 73 74 3a 4c 6d 65 40 23 6f   ....GHost:Lme@#o
  0030: 6d 65 3a 2e 6d 65 40 23 6f 6d 65 0a 0a 0a 0a 0a   me:.me@#ome.....
Seed 5 (id=01d33da9d2a42feb, size=144 bytes, fuzzer=cmplog, trial=1, discovered_at=7490s, mutation_op=BitFlipMutator,BytesRandSetMutator,ByteRandMutator,BytesRandInsertMutator,BytesDeleteMutator,WordAddMutator,BytesCopyMutator):
  0000: 00 01 00 00 00 19 70 6f 00 33 3a 2f 2f 31 cd c8   ......po.3://1..
  0010: 00 00 2e ff 7f 00 00 06 ad 00 35 2a 38 35 30 00   ..........5*850.
  0020: 06 00 00 00 47 48 6f 73 74 3a 20 0a 1c 5a 32 3b   ....GHost: ..Z2;
  0030: df ff 0d cd cd cd cd cd cd cd cd cd cd cd d9 cd   ................

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=003e4994f2c65fcf, size=35 bytes, fuzzer=value_profile, trial=1, discovered_at=22s, mutation_op=QwordAddMutator,WordAddMutator):
  0000: 00 01 00 00 00 19 30 49 2e 2e 51 2e 47 48 2e 2b   ......0I..Q.GH.+
  0010: 80 00 21 47 47 46 0f 00 00 00 f9 ff ff ff 49 62   ..!GGF........Ib
  0020: 7e 05 61                                          ~.a
Seed 2 (id=002ca4cb3749be7f, size=36 bytes, fuzzer=minimizer, trial=1, discovered_at=34s, mutation_op=BytesInsertMutator,TokenInsert,QwordAddMutator,ByteFlipMutator):
  0000: 00 01 00 00 00 19 66 74 70 00 78 6e 2d 2d 00 2e   ......ftp.xn--..
  0010: 70 30 70 ff 6e 8b 6d 62 73 74 72 00 70 70 70 7a   p0p.n.mbstr.pppz
  0020: 70 71 8f 00                                       pq..
Seed 3 (id=0024e5972fc0b2e0, size=35 bytes, fuzzer=naive, trial=1, discovered_at=88s, mutation_op=WordAddMutator):
  0000: 00 01 00 00 00 19 25 60 25 61 3e 66 9f 9f 63 25   ......%`%a>f..c%
  0010: 2b 5d 25 41 bf 41 41 41 41 40 41 41 5a 70 65 72   +]%A.AAAA@AAZper
  0020: 6d 69 74                                          mit
Seed 4 (id=00225bc4819174d2, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=152s, mutation_op=BytesInsertMutator,ByteAddMutator,ByteIncMutator,BytesDeleteMutator,ByteDecMutator):
  0000: 00 01 00 00 00 43 64 55 43 25 25 25 25 21 25 65   .....CdUC%%%%!%e
  0010: 26 25 65 24 25 64 45 72 46 25 41 27 25 31 25 25   &%e$%dErF%A'%1%%
  0020: 65 25 44 d6 42 64 45 72 33 25 65 4b 25 43 25 25   e%D.BdEr3%eK%C%%
  0030: 25 25 25 25 25 25 25 25 25 25 25 25 26 25 40 e8   %%%%%%%%%%%%&%@.
Seed 5 (id=00430153b42aa78b, size=35 bytes, fuzzer=naive, trial=1, discovered_at=175s, mutation_op=BytesDeleteMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 70 6b 73 65 2e 2e 2e 45 2e 41   ......pkse...E.A
  0010: 2e 2b 6b 73 65 4d 2e 2e 45 2b 2b 2b 2b 2b 2b 2b   .+kseM..E+++++++
  0020: 2b 55 6b                                          +Uk


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x30                            19(.)x19 43(C)x3 2e(.)x2 44(D)x1 +5u  PARTIAL
   0x0006  70(p)x11 2b(+)x10 9f(.)x8 57(W)x1   70(p)x6 25(%)x5 64(d)x3 2e(.)x3 +11u  PARTIAL
   0x0008  70(p)x10 00(.)x10 ab(.)x9 83(.)x1   25(%)x5 43(C)x5 70(p)x4 2e(.)x3 +12u  PARTIAL
   0x000c  2f(/)x19 ab(.)x9 6d(m)x1 72(r)x1    25(%)x6 2e(.)x5 2f(/)x3 41(A)x2 +12u  PARTIAL
   0x001e  30(0)x19 00(.)x9 65(e)x1 ff(.)x1    25(%)x4 00(.)x4 65(e)x2 44(D)x2 +18u  PARTIAL
   0x001f  00(.)x30                            25(%)x4 00(.)x4 2e(.)x3 ff(.)x2 +16u  PARTIAL
   0x0020  06(.)x30                            06(.)x3 65(e)x2 00(.)x2 42(B)x2 +19u  PARTIAL
   0x0021  00(.)x30                            00(.)x6 25(%)x3 2d(-)x3 05(.)x1 +15u  PARTIAL
   0x0022  00(.)x30                            00(.)x5 44(D)x3 25(%)x3 2e(.)x2 +12u  PARTIAL
   0x0023  00(.)x30                            00(.)x5 25(%)x4 2e(.)x2 d6(.)x1 +7u  PARTIAL
   0x0024  47(G)x20 48(H)x10                   47(G)x4 50(P)x2 42(B)x1 9e(.)x1 +7u  PARTIAL
   0x0025  48(H)x30                            25(%)x4 34(4)x3 2e(.)x3 41(A)x2 +3u  DIFFER
   0x0026  6f(o)x20 4f(O)x10                   72(r)x2 2e(.)x2 45(E)x1 41(A)x1 +9u  DIFFER
   0x0027  73(s)x19 53(S)x11                   48(H)x3 62(b)x2 72(r)x1 27(')x1 +8u  DIFFER
   0x0028  74(t)x30                            25(%)x5 48(H)x2 2e(.)x2 33(3)x1 +5u  DIFFER
   0x0029  3a(:)x22 3b(;)x8                    25(%)x3 48(H)x2 31(1)x1 53(S)x1 +8u  DIFFER
   0x0039  09(.)x6 0a(.)x5 0d(.)x4 20( )x3 +10u  25(%)x3 0a(.)x3 62(b)x2 0c(.)x1     PARTIAL
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

--- fast ---
**Baseline relationship**: identical to `minimizer` (same
`[calibration, power]` stages, same `StdPowerMutationalStage`, same
FIFO corpus order) EXCEPT the corpus scheduler is
`PowerQueueScheduler::fast()`, which sets PowerSchedule `FAST` in
`SchedulerMetadata`. The single-technique delta is therefore `fast`
vs `minimizer`, not vs naive.

**Instrumentation**: naive's edge counters only.

**Feedback**: edge-bucket `MaxMapFeedback` + `CalibrationStage` (as
minimizer).

**Mutators / stages**: `[calibration, power]` with the havoc+token
`StdPowerMutationalStage` (as minimizer). The FAST schedule changes the
`perf_score` energy formula: the per-seed mutation budget is multiplied
by an AFLFast factor based on `n_fuzz` — log2 of how many times that
seed's coverage bucket has been exercised campaign-wide. Rarely-hit
paths get up to 4× energy; saturated paths are damped to 0.4×. Seed
*selection* order is still FIFO (`PowerQueueScheduler::next()` walks the
corpus in order); only the energy allocation differs from minimizer.

**Observed `mutation_op` in seed metadata**: havoc/token names
(captured); no dash rows.

**Per-execution cost**: one edge increment per edge; calibration burst
per new entry; `n_fuzz` bookkeeping per execution.

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
  prompts_b/curl_165.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 165,
  "target": "curl",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [cmplog>naive (I2S), value_profile_cmplog>value_profile (I2S), fast>minimizer (aflfast_rarity)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 165 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 165 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 165 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).