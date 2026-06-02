==== BLOCKER ====
Target: curl
Branch ID: 470
Location: /src/curl/lib/transfer.c:1866:6
Enclosing function: Curl_retry_request
Source line:   if((data->req.bytecount + data->req.headerbytecount == 0) &&
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.30h  loser=24.00h
  avg hitcount on branch: winner=1690  loser=0
  prob_div=1.00  dur_div=23.70h  hit_div=1690
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.10h  loser=24.00h
  avg hitcount on branch: winner=1672  loser=0
  prob_div=1.00  dur_div=23.90h  hit_div=1672
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/470/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_retry_request (/src/curl/lib/transfer.c:1855-1925) ---
[ ]  1853     NOTE: that the *url is malloc()ed. */
[ ]  1854  CURLcode Curl_retry_request(struct Curl_easy *data, char **url)
[B]  1855  {
[B]  1856    struct connectdata *conn = data->conn;
[B]  1857    bool retry = FALSE;
[B]  1858    *url = NULL;
[ ]  1859  
[ ]  1860    /* if we're talking upload, we can't do the checks below, unless the protocol
[ ]  1861       is HTTP as when uploading over HTTP we will still get a response */
[B]  1862    if(data->set.upload &&
[B]  1863       !(conn->handler->protocol&(PROTO_FAMILY_HTTP|CURLPROTO_RTSP)))
[ ]  1864      return CURLE_OK;
[ ]  1865  
[B]  1866    if((data->req.bytecount + data->req.headerbytecount == 0) && <-- BLOCKER
[B]  1867       conn->bits.reuse &&
[B]  1868       (!data->set.opt_no_body || (conn->handler->protocol & PROTO_FAMILY_HTTP))
[B]  1869  #ifndef CURL_DISABLE_RTSP
[B]  1870       && (data->set.rtspreq != RTSPREQ_RECEIVE)
[B]  1871  #endif
[B]  1872      )
[ ]  1873      /* We got no data, we attempted to re-use a connection. For HTTP this
[ ]  1874         can be a retry so we try again regardless if we expected a body.
[ ]  1875         For other protocols we only try again only if we expected a body.
[ ]  1876  
[ ]  1877         This might happen if the connection was left alive when we were
[ ]  1878         done using it before, but that was closed when we wanted to read from
[ ]  1879         it again. Bad luck. Retry the same request on a fresh connect! */
[ ]  1880      retry = TRUE;
[B]  1881    else if(data->state.refused_stream &&
[B]  1882            (data->req.bytecount + data->req.headerbytecount == 0) ) {
[ ]  1883      /* This was sent on a refused stream, safe to rerun. A refused stream
[ ]  1884         error can typically only happen on HTTP/2 level if the stream is safe
[ ]  1885         to issue again, but the nghttp2 API can deliver the message to other
[ ]  1886         streams as well, which is why this adds the check the data counters
[ ]  1887         too. */
[ ]  1888      infof(data, "REFUSED_STREAM, retrying a fresh connect");
[ ]  1889      data->state.refused_stream = FALSE; /* clear again */
[ ]  1890      retry = TRUE;
[ ]  1891    }
[B]  1892    if(retry) {
[ ]  1893  #define CONN_MAX_RETRIES 5
[ ]  1894      if(data->state.retrycount++ >= CONN_MAX_RETRIES) {
[ ]  1895        failf(data, "Connection died, tried %d times before giving up",
[ ]  1896              CONN_MAX_RETRIES);
[ ]  1897        data->state.retrycount = 0;
[ ]  1898        return CURLE_SEND_ERROR;
[ ]  1899      }
[ ]  1900      infof(data, "Connection died, retrying a fresh connect (retry count: %d)",
[ ]  1901            data->state.retrycount);
[ ]  1902      *url = strdup(data->state.url);
[ ]  1903      if(!*url)
[ ]  1904        return CURLE_OUT_OF_MEMORY;
[ ]  1905  
[ ]  1906      connclose(conn, "retry"); /* close this connection */
[ ]  1907      conn->bits.retry = TRUE; /* mark this as a connection we're about
[ ]  1908                                  to retry. Marking it this way should
[ ]  1909                                  prevent i.e HTTP transfers to return
[ ]  1910                                  error just because nothing has been
[ ]  1911                                  transferred! */
[ ]  1912  
[ ]  1913  
[ ]  1914      if(conn->handler->protocol&PROTO_FAMILY_HTTP) {
[ ]  1915        if(data->req.writebytecount) {
[ ]  1916          CURLcode result = Curl_readrewind(data);
[ ]  1917          if(result) {
[ ]  1918            Curl_safefree(*url);
[ ]  1919            return result;
[ ]  1920          }
[ ]  1921        }
[ ]  1922      }
[ ]  1923    }
[B]  1924    return CURLE_OK;
[B]  1925  }

--- Caller (1 hop): multi.c:multi_runsingle (/src/curl/lib/multi.c:1811-2661, calls Curl_retry_request at line 2412) (±10 around call site) ---
[ ]  2402        }
[ ]  2403  
[ ]  2404        /* read/write data if it is ready to do so */
[B]  2405        result = Curl_readwrite(data->conn, data, &done, &comeback);
[ ]  2406  
[B]  2407        if(done || (result == CURLE_RECV_ERROR)) {
[ ]  2408          /* If CURLE_RECV_ERROR happens early enough, we assume it was a race
[ ]  2409           * condition and the server closed the re-used connection exactly when
[ ]  2410           * we wanted to use it, so figure out if that is indeed the case.
[ ]  2411           */
[B]  2412          CURLcode ret = Curl_retry_request(data, &newurl); <-- CALL
[B]  2413          if(!ret)
[B]  2414            retry = (newurl)?TRUE:FALSE;
[ ]  2415          else if(!result)
[ ]  2416            result = ret;
[ ]  2417  
[B]  2418          if(retry) {
[ ]  2419            /* if we are to retry, set the result to OK and consider the
[ ]  2420               request as done */
[ ]  2421            result = CURLE_OK;
[ ]  2422            done = TRUE;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  http2.c:http2_handle_stream_close  (/src/curl/lib/http2.c:1531-1602, calls Curl_retry_request at line 1555)
hop 2  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_retry_request at line 2207)
hop 3  http2.c:http2_recv  (/src/curl/lib/http2.c:1657-1858, calls http2.c:http2_handle_stream_close at line 1793)
hop 3  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 3  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)
hop 4  curl_multi_socket  (/src/curl/lib/multi.c:3288-3296, calls multi.c:multi_socket at line 3292)
hop 4  curl_multi_socket_action  (/src/curl/lib/multi.c:3300-3308, calls multi.c:multi_socket at line 3304)
hop 4  curl_multi_strerror  (/src/curl/lib/strerror.c:364-420, calls curl_multi_perform at line 368)
hop 5  easy.c:wait_or_timeout  (/src/curl/lib/easy.c:541-628, calls curl_multi_socket_action at line 582)
hop 5  curl_multi_add_handle  (/src/curl/lib/multi.c:464-590, calls curl_multi_socket at line 509)
hop 6  easy.c:easy_events  (/src/curl/lib/easy.c:636-645, calls easy.c:wait_or_timeout at line 644)
hop 6  easy.c:easy_perform  (/src/curl/lib/easy.c:706-763, calls curl_multi_add_handle at line 741)
hop 6  Curl_multi_add_perform  (/src/curl/lib/multi.c:1574-1594, calls curl_multi_add_handle at line 1580)
hop 7  curl_easy_perform  (/src/curl/lib/easy.c:771-773, calls easy.c:easy_perform at line 772)
hop 7  curl_easy_perform_ev  (/src/curl/lib/easy.c:781-783, calls easy.c:easy_perform at line 782)
hop 7  http2.c:push_promise  (/src/curl/lib/http2.c:565-663, calls Curl_multi_add_perform at line 633)
hop 8  Curl_getconnectinfo  (/src/curl/lib/connect.c:1485-1519, calls curl_easy_perform at line 1489)
hop 8  http2.c:on_frame_recv  (/src/curl/lib/http2.c:679-812, calls http2.c:push_promise at line 791)
hop 8  Curl_close  (/src/curl/lib/url.c:380-497, calls curl_easy_perform at line 402)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      22         0  curl_multi_fdset  (/src/curl/lib/multi.c:1099-1154)
      22         0  Curl_single_getsock  (/src/curl/lib/transfer.c:1352-1387)
      20         0  multi.c:add_next_timeout  (/src/curl/lib/multi.c:3055-3094)
       4         0  Curl_get_upload_buffer  (/src/curl/lib/transfer.c:118-125)
       2         0  Curl_http2_done_sending  (/src/curl/lib/http2.c:1486-1526)
       2         0  Curl_fillreadbuffer  (/src/curl/lib/transfer.c:163-363)
       2         0  Curl_done_sending  (/src/curl/lib/transfer.c:882-896)
       2         0  transfer.c:readwrite_upload  (/src/curl/lib/transfer.c:928-1154)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716) ---
  d=3   L2674  T=0 F=42  T=0 F=20  if(multi->in_callback)
  d=3   L2678  T=42 F=42  T=20 F=20  while(data) {
  d=3   L2686  T=0 F=42  T=0 F=20  if(result)
  d=3   L2704  T=20 F=42  T=0 F=20  if(t)
  d=3   L2708  T=20 F=42  T=0 F=20  } while(t);
  d=3   L2712  T=42 F=0  T=20 F=0  if(CURLM_OK >= returncode)
--- d=2  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661) ---
  d=2   L1827  T=0 F=42  T=0 F=20  if(multi->dead) {
  d=2   L2378  T=0 F=42  T=0 F=20  if(data->set.max_send_speed)
  d=2   L2387  T=0 F=42  T=0 F=20  if(data->set.max_recv_speed)
  d=2   L2394  T=0 F=42  T=0 F=20  if(send_timeout_ms || recv_timeout_ms) {
  d=2   L2394  T=0 F=42  T=0 F=20  if(send_timeout_ms || recv_timeout_ms) {
  d=2   L2407  T=20 F=22  T=20 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=2   L2407  T=0 F=22  T=0 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=2   L2425  T=0 F=22  T=0 F=0  else if((CURLE_HTTP2_STREAM == result) &&
  d=2   L2448  T=0 F=42  T=0 F=20  if(result) {
  d=2   L2464  T=20 F=22  T=20 F=0  else if(done) {
  d=2   L2515  T=0 F=22  T=0 F=0  else if(comeback) {
  d=2   L2657  T=0 F=42  T=0 F=20  } while((rc == CURLM_CALL_MULTI_PERFORM) || multi_ischang...
--- d=1  Curl_retry_request  (/src/curl/lib/transfer.c:1855-1925) ---
  d=1   L1862  T=1 F=19  T=0 F=20  if(data->set.upload &&
  d=1   L1863  T=0 F=1  T=0 F=0  !(conn->handler->protocol&(PROTO_FAMILY_HTTP|CURLPROTO_RT...
  d=1   L1866  T=0 F=20  T=20 F=0  if((data->req.bytecount + data->req.headerbytecount == 0) &&  <-- BLOCKER
  d=1   L1867  T=0 F=0  T=0 F=20  conn->bits.reuse &&

[off-chain: 138 additional divergent branches across 15 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=0057778b67d14b3b, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=888s, mutation_op=BytesDeleteMutator,ByteDecMutator,BytesInsertCopyMutator):
  0000: 00 01 00 00 00 19 70 6f 70 71 4b 2f 3a 3a 3a 3a   ......popqK/::::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 31 ad 38 35 30 00   :::::::9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 23 65 0d 0a 53 65 74 2d 43 6f 6f   mewhe#e..Set-Coo
Seed 2 (id=01bc69e4b71e5bec, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4539s, mutation_op=BytesRandInsertMutator,ByteDecMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 3a 3a 3a 3a   ......pop3K/::::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 31 48 38 35 30 00   :::::::9001H850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 25 6f   ....GHTTP/ me@%o
  0030: 6d 65 77 68 65 72 65 0d 0a 54 72 61 6e 45 66 65   mewhere..TranEfe
Seed 3 (id=00f515acb6373e33, size=112 bytes, fuzzer=cmplog, trial=1, discovered_at=7776s, mutation_op=BytesInsertCopyMutator,BytesDeleteMutator,ByteAddMutator,BytesInsertMutator,WordAddMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2f 31 32 00   ......pop.://12.
  0010: 00 30 28 28 2e 31 3a 39 9c 30 31 72 38 35 30 00   .0((.1:9.01r850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 61 06 24   ....GHTTP/ mea.$
  0030: 65 63 8e 65 74 72 65 0d 0a 43 6f 6e 6e 65 63 74   ec.etre..Connect
Seed 4 (id=00a044736f809ce4, size=112 bytes, fuzzer=cmplog, trial=1, discovered_at=7995s, mutation_op=BytesDeleteMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2f 31 32 00   ......pop.://12.
  0010: 00 30 28 28 2e f6 f6 f6 f6 30 31 72 38 35 30 00   .0((.....01r850.
  0020: 02 00 00 00 47 48 54 54 50 2f 25 6d 65 61 06 24   ....GHTTP/%mea.$
  0030: 65 63 8e 65 74 72 65 0d 0a 43 25 6e 6e 65 63 74   ec.etre..C%nnect
Seed 5 (id=007ebe990120e121, size=112 bytes, fuzzer=cmplog, trial=1, discovered_at=8141s, mutation_op=ByteAddMutator):
  0000: 00 01 00 00 00 19 70 6f 65 00 00 00 00 00 32 0b   ......poe.....2.
  0010: 0b 0b 0b 0b 0b 0b f4 39 9c 30 31 72 38 35 30 00   .......9.01r850.
  0020: 02 00 00 00 47 68 74 74 70 2f 09 6d 65 61 06 24   ....Ghttp/.mea.$
  0030: 65 63 8e 65 74 72 65 0d 0a 43 6f 6e 6e 65 63 74   ec.etre..Connect

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=003e4994f2c65fcf, size=35 bytes, fuzzer=value_profile, trial=1, discovered_at=22s, mutation_op=QwordAddMutator,WordAddMutator):
  0000: 00 01 00 00 00 19 30 49 2e 2e 51 2e 47 48 2e 2b   ......0I..Q.GH.+
  0010: 80 00 21 47 47 46 0f 00 00 00 f9 ff ff ff 49 62   ..!GGF........Ib
  0020: 7e 05 61                                          ~.a
Seed 2 (id=0024e5972fc0b2e0, size=35 bytes, fuzzer=naive, trial=1, discovered_at=88s, mutation_op=WordAddMutator):
  0000: 00 01 00 00 00 19 25 60 25 61 3e 66 9f 9f 63 25   ......%`%a>f..c%
  0010: 2b 5d 25 41 bf 41 41 41 41 40 41 41 5a 70 65 72   +]%A.AAAA@AAZper
  0020: 6d 69 74                                          mit
Seed 3 (id=00225bc4819174d2, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=152s, mutation_op=BytesInsertMutator,ByteAddMutator,ByteIncMutator,BytesDeleteMutator,ByteDecMutator):
  0000: 00 01 00 00 00 43 64 55 43 25 25 25 25 21 25 65   .....CdUC%%%%!%e
  0010: 26 25 65 24 25 64 45 72 46 25 41 27 25 31 25 25   &%e$%dErF%A'%1%%
  0020: 65 25 44 d6 42 64 45 72 33 25 65 4b 25 43 25 25   e%D.BdEr3%eK%C%%
  0030: 25 25 25 25 25 25 25 25 25 25 25 25 26 25 40 e8   %%%%%%%%%%%%&%@.
Seed 4 (id=00430153b42aa78b, size=35 bytes, fuzzer=naive, trial=1, discovered_at=175s, mutation_op=BytesDeleteMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 70 6b 73 65 2e 2e 2e 45 2e 41   ......pkse...E.A
  0010: 2e 2b 6b 73 65 4d 2e 2e 45 2b 2b 2b 2b 2b 2b 2b   .+kseM..E+++++++
  0020: 2b 55 6b                                          +Uk
Seed 5 (id=0036ed920052a1c1, size=35 bytes, fuzzer=naive, trial=1, discovered_at=626s, mutation_op=ByteIncMutator,ByteInterestingMutator):
  0000: 00 01 00 00 00 19 43 41 25 64 61 25 41 25 64 61   ......CA%da%A%da
  0010: 25 43 66 25 25 43 40 25 00 19 70 6b 2e 44 43 43   %Cf%%C@%..pk.DCC
  0020: 01 43 44                                          .CD


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x20                            19(.)x10 43(C)x3 2e(.)x2 44(D)x1 +4u  PARTIAL
   0x0006  70(p)x13 9a(.)x6 49(I)x1            25(%)x4 64(d)x3 2e(.)x3 43(C)x2 +7u  PARTIAL
   0x0007  6f(o)x12 9a(.)x6 00(.)x1 4d(M)x1    55(U)x2 41(A)x2 25(%)x2 2e(.)x2 +12u  DIFFER
   0x0008  70(p)x16 00(.)x2 65(e)x1 43(C)x1    43(C)x5 2e(.)x3 25(%)x3 41(A)x2 +7u  PARTIAL
   0x000c  3a(:)x8 2f(/)x8 00(.)x3 73(s)x1     2e(.)x5 25(%)x4 41(A)x2 45(E)x2 +7u  DIFFER
   0x0013  3a(:)x9 28(()x9 0b(.)x1 30(0)x1     25(%)x3 2d(-)x3 41(A)x2 62(b)x2 +10u  DIFFER
   0x0017  39(9)x19 f6(.)x1                    41(A)x3 2e(.)x3 25(%)x3 00(.)x1 +10u  DIFFER
   0x0019  30(0)x18 14(.)x1 cf(.)x1            25(%)x3 2b(+)x3 00(.)x2 40(@)x2 +10u  DIFFER
   0x001a  31(1)x16 00(.)x4                    25(%)x5 41(A)x3 f9(.)x1 2b(+)x1 +10u  PARTIAL
   0x001c  38(8)x12 e8(.)x6 3d(=)x1 21(!)x1    2e(.)x3 45(E)x3 2b(+)x2 ff(.)x1 +11u  DIFFER
   0x001d  35(5)x14 03(.)x6                    2e(.)x2 64(d)x2 2d(-)x2 ff(.)x1 +13u  PARTIAL
   0x001e  30(0)x20                            25(%)x4 44(D)x2 49(I)x1 65(e)x1 +12u  DIFFER
   0x001f  00(.)x20                            25(%)x3 2e(.)x3 41(A)x2 62(b)x1 +11u  DIFFER
   0x0020  02(.)x18 11(.)x2                    65(e)x2 42(B)x2 2e(.)x2 7e(~)x1 +13u  DIFFER
   0x0021  00(.)x20                            25(%)x3 2d(-)x3 05(.)x1 69(i)x1 +11u  PARTIAL
   0x0022  00(.)x20                            44(D)x3 2e(.)x2 61(a)x1 74(t)x1 +10u  PARTIAL
   0x0023  00(.)x20                            2e(.)x2 25(%)x2 d6(.)x1 bb(.)x1 +6u  DIFFER
   0x0024  47(G)x18 48(H)x2                    50(P)x2 42(B)x1 9e(.)x1 2e(.)x1 +5u  DIFFER
   0x0025  48(H)x19 68(h)x1                    25(%)x3 2e(.)x3 41(A)x2 64(d)x1 +1u  DIFFER
   0x0026  54(T)x19 74(t)x1                    2e(.)x2 45(E)x1 41(A)x1 25(%)x1 +5u  DIFFER
   0x0027  54(T)x19 74(t)x1                    72(r)x1 27(')x1 40(@)x1 2e(.)x1 +6u  DIFFER
   0x0028  50(P)x19 70(p)x1                    25(%)x4 2e(.)x2 33(3)x1 db(.)x1 +2u  PARTIAL
   0x0029  2f(/)x20                            25(%)x2 31(1)x1 2e(.)x1 42(B)x1 +5u  DIFFER
   0x002b  6d(m)x18 65(e)x1 29())x1            25(%)x4 2e(.)x2 4b(K)x1 66(f)x1 +2u  DIFFER
   0x0030  6d(m)x12 65(e)x6 63(c)x1 29())x1    25(%)x2 43(C)x1 2e(.)x1 41(A)x1 +4u  DIFFER
   0x0033  68(h)x12 65(e)x6 74(t)x1 29())x1    25(%)x3 2e(.)x2 41(A)x2 bd(.)x1     DIFFER
   0x0034  65(e)x12 74(t)x6 72(r)x1 29())x1    25(%)x3 45(E)x1 2e(.)x1 e2(.)x1 +2u  PARTIAL
   0x0036  65(e)x15 87(.)x2 0d(.)x1 4e(N)x1 +1u  25(%)x4 4e(N)x1 45(E)x1 44(D)x1     PARTIAL
   0x0038  0a(.)x14 13(.)x4 43(C)x1 25(%)x1    25(%)x3 42(B)x2 80(.)x1 64(d)x1     PARTIAL
   0x0039  54(T)x10 43(C)x5 52(R)x2 53(S)x1 +2u  25(%)x3 62(b)x2                     DIFFER
   0x003a  72(r)x7 6f(o)x4 65(e)x3 8d(.)x3 +3u  25(%)x2 9e(.)x1 42(B)x1 65(e)x1     PARTIAL
   0x003b  61(a)x10 6e(n)x6 74(t)x3 3a(:)x1    25(%)x2 66(f)x1 42(B)x1 65(e)x1     DIFFER
   0x003c  6e(n)x15 72(r)x2 2d(-)x1 65(e)x1 +1u  64(d)x2 26(&)x1 52(R)x1 25(%)x1     DIFFER
   0x003e  66(f)x10 63(c)x5 2d(-)x2 6f(o)x1 +2u  40(@)x2 25(%)x2 79(y)x1             DIFFER
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
  prompts_b/curl_470.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 470,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 470 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 470 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 470 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).