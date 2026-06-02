==== BLOCKER ====
Target: curl
Branch ID: 167
Location: /src/curl/lib/http.c:2858:37
Enclosing function: Curl_http_range
Source line:     if(((httpreq == HTTPREQ_GET) || (httpreq == HTTPREQ_HEAD)) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    5        4          1  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     1        8          1  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                            10        0          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=5.70h  loser=12.20h
  avg hitcount on branch: winner=2  loser=0
  prob_div=1.00  dur_div=6.50h  hit_div=2
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/167/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_http_range (/src/curl/lib/http.c:2851-2903) ---
[ ]  2849  CURLcode Curl_http_range(struct Curl_easy *data,
[ ]  2850                           Curl_HttpReq httpreq)
[B]  2851  {
[B]  2852    if(data->state.use_range) {
[ ]  2853      /*
[ ]  2854       * A range is selected. We use different headers whether we're downloading
[ ]  2855       * or uploading and we always let customized headers override our internal
[ ]  2856       * ones if any such are specified.
[ ]  2857       */
[B]  2858      if(((httpreq == HTTPREQ_GET) || (httpreq == HTTPREQ_HEAD)) && <-- BLOCKER
[B]  2859         !Curl_checkheaders(data, STRCONST("Range"))) {
[ ]  2860        /* if a line like this was already allocated, free the previous one */
[W]  2861        free(data->state.aptr.rangeline);
[W]  2862        data->state.aptr.rangeline = aprintf("Range: bytes=%s\r\n",
[W]  2863                                             data->state.range);
[W]  2864      }
[L]  2865      else if((httpreq == HTTPREQ_POST || httpreq == HTTPREQ_PUT) &&
[L]  2866              !Curl_checkheaders(data, STRCONST("Content-Range"))) {
[ ]  2867  
[ ]  2868        /* if a line like this was already allocated, free the previous one */
[ ]  2869        free(data->state.aptr.rangeline);
[ ]  2870  
[ ]  2871        if(data->set.set_resume_from < 0) {
[ ]  2872          /* Upload resume was asked for, but we don't know the size of the
[ ]  2873             remote part so we tell the server (and act accordingly) that we
[ ]  2874             upload the whole file (again) */
[ ]  2875          data->state.aptr.rangeline =
[ ]  2876            aprintf("Content-Range: bytes 0-%" CURL_FORMAT_CURL_OFF_T
[ ]  2877                    "/%" CURL_FORMAT_CURL_OFF_T "\r\n",
[ ]  2878                    data->state.infilesize - 1, data->state.infilesize);
[ ]  2879  
[ ]  2880        }
[ ]  2881        else if(data->state.resume_from) {
[ ]  2882          /* This is because "resume" was selected */
[ ]  2883          curl_off_t total_expected_size =
[ ]  2884            data->state.resume_from + data->state.infilesize;
[ ]  2885          data->state.aptr.rangeline =
[ ]  2886            aprintf("Content-Range: bytes %s%" CURL_FORMAT_CURL_OFF_T
[ ]  2887                    "/%" CURL_FORMAT_CURL_OFF_T "\r\n",
[ ]  2888                    data->state.range, total_expected_size-1,
[ ]  2889                    total_expected_size);
[ ]  2890        }
[ ]  2891        else {
[ ]  2892          /* Range was selected and then we just pass the incoming range and
[ ]  2893             append total size */
[ ]  2894          data->state.aptr.rangeline =
[ ]  2895            aprintf("Content-Range: bytes %s/%" CURL_FORMAT_CURL_OFF_T "\r\n",
[ ]  2896                    data->state.range, data->state.infilesize);
[ ]  2897        }
[ ]  2898        if(!data->state.aptr.rangeline)
[ ]  2899          return CURLE_OUT_OF_MEMORY;
[ ]  2900      }
[B]  2901    }
[B]  2902    return CURLE_OK;
[B]  2903  }

--- Caller (1 hop): Curl_http (/src/curl/lib/http.c:3088-3372, calls Curl_http_range at line 3213) (±10 around call site) ---
[B]  3203    if(result)
[ ]  3204      return result;
[ ]  3205  
[B]  3206    p_accept = Curl_checkheaders(data,
[B]  3207                                 STRCONST("Accept"))?NULL:"Accept: */*\r\n";
[ ]  3208  
[B]  3209    result = Curl_http_resume(data, conn, httpreq);
[B]  3210    if(result)
[ ]  3211      return result;
[ ]  3212  
[B]  3213    result = Curl_http_range(data, httpreq); <-- CALL
[B]  3214    if(result)
[ ]  3215      return result;
[ ]  3216  
[B]  3217    httpstring = get_http_string(data, conn);
[ ]  3218  
[ ]  3219    /* initialize a dynamic send-buffer */
[B]  3220    Curl_dyn_init(&req, DYN_HTTP_REQUEST);
[ ]  3221  
[ ]  3222    /* make sure the header buffer is reset - if there are leftovers from a
[ ]  3223       previous transfer */

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_http  (/src/curl/lib/http.c:3088-3372, calls Curl_http_range at line 3213)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       3         1  http.c:http_setup_conn  (/src/curl/lib/http.c:234-264)
       3         1  Curl_http_output_auth  (/src/curl/lib/http.c:870-943)
       3         1  Curl_buffer_send  (/src/curl/lib/http.c:1295-1471)
       3         1  Curl_http_connect  (/src/curl/lib/http.c:1541-1584)
       3         1  Curl_http_done  (/src/curl/lib/http.c:1675-1721)
       3         1  Curl_use_http_1_1plus  (/src/curl/lib/http.c:1734-1742)
       3         1  http.c:get_http_string  (/src/curl/lib/http.c:1747-1763)
       3         1  Curl_add_custom_headers  (/src/curl/lib/http.c:1853-1996)
       3         1  Curl_add_timecondition  (/src/curl/lib/http.c:2006-2074)
       3         1  Curl_http_method  (/src/curl/lib/http.c:2088-2124)
       3         1  Curl_http_useragent  (/src/curl/lib/http.c:2127-2137)
       3         1  Curl_http_host  (/src/curl/lib/http.c:2141-2230)
       3         1  Curl_http_target  (/src/curl/lib/http.c:2238-2344)
       3         1  Curl_http_body  (/src/curl/lib/http.c:2348-2433)
       3         1  Curl_http_bodysend  (/src/curl/lib/http.c:2437-2772)
... (9 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  Curl_http  (/src/curl/lib/http.c:3088-3372) ---
  d=2   L3105  T=3 F=0  T=1 F=0  if(conn->transport != TRNSPRT_QUIC) {
  d=2   L3106  T=3 F=0  T=1 F=0  if(conn->httpversion < 20) { /* unless the connection is ...
  d=2   L3109  T=0 F=3  T=0 F=1  case CURL_HTTP_VERSION_2:
  d=2   L3116  T=0 F=3  T=0 F=1  case CURL_HTTP_VERSION_1_1:
  d=2   L3119  T=3 F=0  T=1 F=0  default:
  d=2   L3122  T=0 F=3  T=0 F=1  if(data->state.httpwant == CURL_HTTP_VERSION_2_PRIOR_KNOW...
  d=2   L3153  T=0 F=3  T=0 F=1  if(result)
  d=2   L3157  T=0 F=3  T=0 F=1  if(result)
  d=2   L3165  T=0 F=3  T=0 F=1  if(data->state.up.query) {
  d=2   L3171  T=0 F=3  T=0 F=1  (pq ? pq : data->state.up.path), FALSE);
  d=2   L3173  T=0 F=3  T=0 F=1  if(result)
  d=2   L3178  T=0 F=3  T=0 F=1  if(data->state.referer && !Curl_checkheaders(data, STRCON...
  d=2   L3184  T=3 F=0  T=1 F=0  if(!Curl_checkheaders(data, STRCONST("Accept-Encoding")) &&
  d=2   L3185  T=0 F=3  T=0 F=1  data->set.str[STRING_ENCODING]) {
  d=2   L3198  T=0 F=3  T=0 F=1  if(result)
  d=2   L3203  T=0 F=3  T=0 F=1  if(result)
  d=2   L3206  T=0 F=3  T=0 F=1  p_accept = Curl_checkheaders(data,
  d=2   L3210  T=0 F=3  T=0 F=1  if(result)
  d=2   L3214  T=0 F=3  T=0 F=1  if(result)
  d=2   L3229  T=3 F=0  T=1 F=0  if(!result)
  d=2   L3231  T=0 F=3  T=0 F=1  if(result) {
  d=2   L3237  T=0 F=3  T=0 F=1  if(conn->bits.altused && !Curl_checkheaders(data, STRCONS...
  d=2   L3263  T=3 F=0  T=1 F=0  (data->state.aptr.host?data->state.aptr.host:""),
  d=2   L3264  T=0 F=3  T=0 F=1  data->state.aptr.proxyuserpwd?
  d=2   L3266  T=0 F=3  T=0 F=1  data->state.aptr.userpwd?data->state.aptr.userpwd:"",
  d=2   L3267  T=3 F=0  T=1 F=0  (data->state.use_range && data->state.aptr.rangeline)?
  d=2   L3267  T=3 F=0  T=0 F=1  (data->state.use_range && data->state.aptr.rangeline)?
  d=2   L3269  T=0 F=3  T=0 F=1  (data->set.str[STRING_USERAGENT] &&
  d=2   L3273  T=3 F=0  T=1 F=0  p_accept?p_accept:"",
  d=2   L3274  T=0 F=3  T=0 F=1  data->state.aptr.te?data->state.aptr.te:"",
  d=2   L3275  T=0 F=3  T=0 F=1  (data->set.str[STRING_ENCODING] &&
  d=2   L3279  T=0 F=3  T=0 F=1  (data->state.referer && data->state.aptr.ref)?
  d=2   L3282  T=0 F=3  T=0 F=1  (conn->bits.httpproxy &&
  d=2   L3293  T=0 F=3  T=0 F=1  altused ? altused : ""
  d=2   L3302  T=0 F=3  T=0 F=1  if(result) {
  d=2   L3307  T=3 F=0  T=1 F=0  if(!(conn->handler->flags&PROTOPT_SSL) &&
  d=2   L3308  T=3 F=0  T=1 F=0  conn->httpversion != 20 &&
  d=2   L3309  T=0 F=3  T=0 F=1  (data->state.httpwant == CURL_HTTP_VERSION_2)) {
  d=2   L3320  T=0 F=3  T=0 F=1  if(!result && conn->handler->protocol&(CURLPROTO_WS|CURLP...
  d=2   L3320  T=3 F=0  T=1 F=0  if(!result && conn->handler->protocol&(CURLPROTO_WS|CURLP...
  d=2   L3322  T=3 F=0  T=1 F=0  if(!result)
  d=2   L3324  T=3 F=0  T=1 F=0  if(!result)
  d=2   L3327  T=3 F=0  T=1 F=0  if(!result) {
  d=2   L3329  T=0 F=3  T=0 F=1  if((httpreq == HTTPREQ_GET) ||
  d=2   L3330  T=3 F=0  T=0 F=1  (httpreq == HTTPREQ_HEAD))
  d=2   L3336  T=0 F=3  T=0 F=1  if(result) {
  d=2   L3341  T=3 F=0  T=1 F=0  if((http->postsize > -1) &&
  d=2   L3342  T=3 F=0  T=0 F=1  (http->postsize <= data->req.writebytecount) &&
  d=2   L3343  T=3 F=0  T=0 F=0  (http->sending != HTTPSEND_REQUEST))
  d=2   L3346  T=0 F=3  T=0 F=1  if(data->req.writebytecount) {
  d=2   L3366  T=0 F=3  T=0 F=1  if((conn->httpversion == 20) && data->req.upload_chunky)
--- d=1  Curl_http_range  (/src/curl/lib/http.c:2851-2903) ---
  d=1   L2852  T=3 F=0  T=1 F=0  if(data->state.use_range) {
  d=1   L2858  T=3 F=0  T=0 F=1  if(((httpreq == HTTPREQ_GET) || (httpreq == HTTPREQ_HEAD)...  <-- BLOCKER
  d=1   L2858  T=0 F=3  T=0 F=1  if(((httpreq == HTTPREQ_GET) || (httpreq == HTTPREQ_HEAD)...  <-- BLOCKER
  d=1   L2859  T=3 F=0  T=0 F=0  !Curl_checkheaders(data, STRCONST("Range"))) {
  d=1   L2865  T=0 F=0  T=0 F=1  else if((httpreq == HTTPREQ_POST || httpreq == HTTPREQ_PU...
  d=1   L2865  T=0 F=0  T=0 F=1  else if((httpreq == HTTPREQ_POST || httpreq == HTTPREQ_PU...

[off-chain: 141 additional divergent branches across 21 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=e7b4feb262a3f0aa, size=164 bytes, fuzzer=cmplog, trial=1, discovered_at=787s, mutation_op=WordInterestingMutator):
  0000: 00 01 00 00 00 19 70 6f 00 33 3a 2f 2f 31 32 37   ......po.3://127
  0010: 2e 30 2e 30 75 75 00 0c 00 00 75 75 38 35 30 00   .0.0uu....uu850.
  0020: 1f 00 00 00 47 70 72 6f 6d 3a 20 80 65 40 30 6f   ....Gprom: .e@0o
  0030: 6d 65 77 68 65 72 65 00 54 54 6f 3a 20 66 61 6b   mewhere.TTo: fak
Seed 2 (id=6a8c9f22928441f9, size=164 bytes, fuzzer=cmplog, trial=1, discovered_at=819s, mutation_op=BytesDeleteMutator,BytesRandInsertMutator):
  0000: 00 01 00 00 00 19 70 6f 00 33 3a 2f 2f 31 32 37   ......po.3://127
  0010: 2e 30 2e 30 75 75 00 0c 00 00 75 75 38 35 30 00   .0.0uu....uu850.
  0020: 1f 00 00 00 47 70 72 6f 6d 3a 20 80 65 40 30 6f   ....Gprom: .e@0o
  0030: 6d 65 77 68 65 72 65 00 54 54 6f 3a 20 66 61 6b   mewhere.TTo: fak
Seed 3 (id=5e1a4d2d7d8c63e6, size=147 bytes, fuzzer=cmplog, trial=1, discovered_at=85189s, mutation_op=ByteFlipMutator,CrossoverInsertMutator,CrossoverReplaceMutator,CrossoverReplaceMutator,WordInterestingMutator):
  0000: 00 01 00 00 00 19 70 6f 00 33 3a 2f 2f 3b cd e5   ......po.3://;..
  0010: 2e 30 2e ff 7f 00 00 02 00 00 00 ff 38 35 30 00   .0..........850.
  0020: 23 00 00 00 47 00 72 6f 6d 00 25 80 00 40 30 6e   #...G.rom.%..@0n
  0030: 6d 65 77 00 65 72 65 00 01 04 00 00 11 48 06 54   mew.ere......H.T

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=cc86b564ea45f225, size=55 bytes, fuzzer=naive, trial=1, discovered_at=56260s, mutation_op=BitFlipMutator,WordInterestingMutator):
  0000: 00 06 00 00 00 00 00 09 00 00 00 00 00 06 00 00   ................
  0010: 00 00 00 0d 00 00 00 00 00 01 00 00 00 19 70 e4   ..............p.
  0020: 00 00 00 00 00 00 00 00 00 ff 00 33 19 40 00 00   ...........3.@..
  0030: 00 00 64 00 00 00 19                              ..d....


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  01(.)x3                             06(.)x1                             DIFFER
   0x0005  19(.)x3                             00(.)x1                             DIFFER
   0x0006  70(p)x3                             00(.)x1                             DIFFER
   0x0007  6f(o)x3                             09(.)x1                             DIFFER
   0x0009  33(3)x3                             00(.)x1                             DIFFER
   0x000a  3a(:)x3                             00(.)x1                             DIFFER
   0x000b  2f(/)x3                             00(.)x1                             DIFFER
   0x000c  2f(/)x3                             00(.)x1                             DIFFER
   0x000d  31(1)x2 3b(;)x1                     06(.)x1                             DIFFER
   0x000e  32(2)x2 cd(.)x1                     00(.)x1                             DIFFER
   0x000f  37(7)x2 e5(.)x1                     00(.)x1                             DIFFER
   0x0010  2e(.)x3                             00(.)x1                             DIFFER
   0x0011  30(0)x3                             00(.)x1                             DIFFER
   0x0012  2e(.)x3                             00(.)x1                             DIFFER
   0x0013  30(0)x2 ff(.)x1                     0d(.)x1                             DIFFER
   0x0014  75(u)x2 7f(.)x1                     00(.)x1                             DIFFER
   0x0015  75(u)x2 00(.)x1                     00(.)x1                             PARTIAL
   0x0017  0c(.)x2 02(.)x1                     00(.)x1                             DIFFER
   0x0019  00(.)x3                             01(.)x1                             DIFFER
   0x001a  75(u)x2 00(.)x1                     00(.)x1                             PARTIAL
   0x001b  75(u)x2 ff(.)x1                     00(.)x1                             DIFFER
   0x001c  38(8)x3                             00(.)x1                             DIFFER
   0x001d  35(5)x3                             19(.)x1                             DIFFER
   0x001e  30(0)x3                             70(p)x1                             DIFFER
   0x001f  00(.)x3                             e4(.)x1                             DIFFER
   0x0020  1f(.)x2 23(#)x1                     00(.)x1                             DIFFER
   0x0024  47(G)x3                             00(.)x1                             DIFFER
   0x0025  70(p)x2 00(.)x1                     00(.)x1                             PARTIAL
   0x0026  72(r)x3                             00(.)x1                             DIFFER
   0x0027  6f(o)x3                             00(.)x1                             DIFFER
   0x0028  6d(m)x3                             00(.)x1                             DIFFER
   0x0029  3a(:)x2 00(.)x1                     ff(.)x1                             DIFFER
   0x002a  20( )x2 25(%)x1                     00(.)x1                             DIFFER
   0x002b  80(.)x3                             33(3)x1                             DIFFER
   0x002c  65(e)x2 00(.)x1                     19(.)x1                             DIFFER
   0x002e  30(0)x3                             00(.)x1                             DIFFER
   0x002f  6f(o)x2 6e(n)x1                     00(.)x1                             DIFFER
   0x0030  6d(m)x3                             00(.)x1                             DIFFER
   0x0031  65(e)x3                             00(.)x1                             DIFFER
   0x0032  77(w)x3                             64(d)x1                             DIFFER
   ... (4 more divergent offsets)
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
  prompts_b/curl_167.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 167,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 167 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 167 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 167 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).