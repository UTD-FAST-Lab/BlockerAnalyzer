==== BLOCKER ====
Target: curl
Branch ID: 415
Location: /src/curl/lib/transfer.c:470:53
Enclosing function: transfer.c:data_pending
Source line:     ((conn->handler->protocol&PROTO_FAMILY_HTTP) && conn->httpversion >= 20) ||
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             2        8          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.40h  loser=24.00h
  avg hitcount on branch: winner=294  loser=0
  prob_div=0.90  dur_div=13.60h  hit_div=294
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=8.80h  loser=24.00h
  avg hitcount on branch: winner=893  loser=0
  prob_div=0.90  dur_div=15.20h  hit_div=893
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/415/{W,L}/branch_coverage_show.txt

--- Enclosing function: transfer.c:data_pending (/src/curl/lib/transfer.c:448-473) ---
[ ]   446  
[ ]   447  static int data_pending(const struct Curl_easy *data)
[B]   448  {
[B]   449    struct connectdata *conn = data->conn;
[ ]   450  
[ ]   451  #ifdef ENABLE_QUIC
[ ]   452    if(conn->transport == TRNSPRT_QUIC)
[ ]   453      return Curl_quic_data_pending(data);
[ ]   454  #endif
[ ]   455  
[B]   456    if(conn->handler->protocol&PROTO_FAMILY_FTP)
[ ]   457      return Curl_ssl_data_pending(conn, SECONDARYSOCKET);
[ ]   458  
[ ]   459    /* in the case of libssh2, we can never be really sure that we have emptied
[ ]   460       its internal buffers so we MUST always try until we get EAGAIN back */
[B]   461    return conn->handler->protocol&(CURLPROTO_SCP|CURLPROTO_SFTP) ||
[B]   462  #ifdef USE_NGHTTP2
[ ]   463      /* For HTTP/2, we may read up everything including response body
[ ]   464         with header fields in Curl_http_readwrite_headers. If no
[ ]   465         content-length is provided, curl waits for the connection
[ ]   466         close, which we emulate it using conn->proto.httpc.closed =
[ ]   467         TRUE. The thing is if we read everything, then http2_recv won't
[ ]   468         be called and we cannot signal the HTTP/2 stream has closed. As
[ ]   469         a workaround, we return nonzero here to call http2_recv. */
[B]   470      ((conn->handler->protocol&PROTO_FAMILY_HTTP) && conn->httpversion >= 20) || <-- BLOCKER
[B]   471  #endif
[B]   472      Curl_ssl_data_pending(conn, FIRSTSOCKET);
[B]   473  }

--- Caller (1 hop): transfer.c:readwrite_data (/src/curl/lib/transfer.c:520-878, calls transfer.c:data_pending at line 860) (±10 around call site) ---
[ ]   850        /* if we received nothing, the server closed the connection and we
[ ]   851           are done */
[B]   852        k->keepon &= ~KEEP_RECV;
[B]   853      }
[ ]   854  
[B]   855      if(k->keepon & KEEP_RECV_PAUSE) {
[ ]   856        /* this is a paused transfer */
[ ]   857        break;
[ ]   858      }
[ ]   859  
[B]   860    } while(data_pending(data) && maxloops--); <-- CALL
[ ]   861  
[B]   862    if(maxloops <= 0) {
[ ]   863      /* we mark it as read-again-please */
[W]   864      conn->cselect_bits = CURL_CSELECT_IN;
[W]   865      *comeback = TRUE;
[W]   866    }
[ ]   867  
[B]   868    if(((k->keepon & (KEEP_RECV|KEEP_SEND)) == KEEP_SEND) &&
[B]   869       conn->bits.close) {
[ ]   870      /* When we've read the entire thing and the close bit is set, the server

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  transfer.c:readwrite_data  (/src/curl/lib/transfer.c:520-878, calls transfer.c:data_pending at line 860)
hop 2  Curl_ssl_data_pending  (/src/curl/lib/vtls/vtls.c:784-786, calls transfer.c:data_pending at line 785)
hop 3  Curl_readwrite  (/src/curl/lib/transfer.c:1167-1340, calls transfer.c:readwrite_data at line 1219)
hop 4  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_readwrite at line 2405)
hop 5  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 5  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)
hop 6  curl_multi_socket  (/src/curl/lib/multi.c:3288-3296, calls multi.c:multi_socket at line 3292)
hop 6  curl_multi_socket_action  (/src/curl/lib/multi.c:3300-3308, calls multi.c:multi_socket at line 3304)
hop 6  curl_multi_strerror  (/src/curl/lib/strerror.c:364-420, calls curl_multi_perform at line 368)
hop 7  easy.c:wait_or_timeout  (/src/curl/lib/easy.c:541-628, calls curl_multi_socket_action at line 582)
hop 7  curl_multi_add_handle  (/src/curl/lib/multi.c:464-590, calls curl_multi_socket at line 509)
hop 8  easy.c:easy_events  (/src/curl/lib/easy.c:636-645, calls easy.c:wait_or_timeout at line 644)
hop 8  easy.c:easy_perform  (/src/curl/lib/easy.c:706-763, calls curl_multi_add_handle at line 741)
hop 8  Curl_multi_add_perform  (/src/curl/lib/multi.c:1574-1594, calls curl_multi_add_handle at line 1580)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
    1010        20  transfer.c:data_pending  (/src/curl/lib/transfer.c:448-473)  <-- enclosing
       0        20  Curl_ssl_data_pending  (/src/curl/lib/vtls/vtls.c:784-786)
      14         0  Curl_ssl_random  (/src/curl/lib/vtls/vtls.c:882-884)
       9         0  Curl_get_upload_buffer  (/src/curl/lib/transfer.c:118-125)
       8         0  Curl_done_sending  (/src/curl/lib/transfer.c:882-896)
       5         0  transfer.c:readwrite_upload  (/src/curl/lib/transfer.c:928-1154)
       4         0  Curl_fillreadbuffer  (/src/curl/lib/transfer.c:163-363)
       3         0  Curl_single_getsock  (/src/curl/lib/transfer.c:1352-1387)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  Curl_readwrite  (/src/curl/lib/transfer.c:1167-1340) ---
  d=3   L1186  T=7 F=12  T=0 F=20  if((k->keepon & KEEP_SENDBITS) == KEEP_SEND)
  d=3   L1218  T=17 F=2  T=20 F=0  if((k->keepon & KEEP_RECV) && (select_res & CURL_CSELECT_...
  d=3   L1225  T=5 F=0  T=0 F=0  if((k->keepon & KEEP_SEND) && (select_res & CURL_CSELECT_...
  d=3   L1225  T=5 F=14  T=0 F=20  if((k->keepon & KEEP_SEND) && (select_res & CURL_CSELECT_...
  d=3   L1229  T=0 F=5  T=0 F=0  if(result)
  d=3   L1279  T=3 F=16  T=0 F=20  if(k->keepon) {
  d=3   L1280  T=0 F=3  T=0 F=0  if(0 > Curl_timeleft(data, &k->now, FALSE)) {
  d=3   L1303  T=15 F=1  T=20 F=0  if(!(data->set.opt_no_body) && (k->size != -1) &&
  d=3   L1317  T=15 F=1  T=20 F=0  if(!(data->set.opt_no_body) && k->chunk &&
  d=3   L1336  T=16 F=3  T=20 F=0  *done = (0 == (k->keepon&(KEEP_RECV|KEEP_SEND|
--- d=2  transfer.c:readwrite_data  (/src/curl/lib/transfer.c:520-878) ---
  d=2   L 539  T=1020 F=0  T=20 F=0  bool is_http2 = ((conn->handler->protocol & PROTO_FAMILY_...
  d=2   L 540  T=1010 F=12  T=0 F=20  (conn->httpversion == 20));
  d=2   L 557  T=12 F=1010  T=20 F=0  !is_http2 &&
  d=2   L 567  T=1020 F=0  T=20 F=0  if(bytestoread) {
  d=2   L 572  T=1 F=1020  T=0 F=20  if(CURLE_AGAIN == result)
  d=2   L 575  T=0 F=1020  T=0 F=20  if(result>0)
  d=2   L 585  T=1020 F=5  T=20 F=0  if(!k->bytecount) {
  d=2   L 587  T=4 F=1010  T=0 F=20  if(k->exp100 > EXP100_SEND_DATA)
  d=2   L 594  T=1010 F=13  T=20 F=0  is_empty_data = ((nread == 0) && (k->bodywrites == 0)) ? ...
  d=2   L 594  T=1000 F=6  T=20 F=0  is_empty_data = ((nread == 0) && (k->bodywrites == 0)) ? ...
  d=2   L 596  T=1000 F=6  T=20 F=0  if(0 < nread || is_empty_data) {
  d=2   L 596  T=13 F=1010  T=0 F=20  if(0 < nread || is_empty_data) {
  d=2   L 603  T=6 F=0  T=0 F=0  if(is_http2 && !nread)
  d=2   L 603  T=6 F=0  T=0 F=0  if(is_http2 && !nread)
  d=2   L 619  T=0 F=1010  T=0 F=20  if(conn->handler->readwrite) {
  d=2   L 630  T=1010 F=3  T=20 F=0  if(k->header) {
  d=2   L 634  T=0 F=1010  T=0 F=20  if(result)
  d=2   L 637  T=0 F=1010  T=0 F=20  if(conn->handler->readwrite &&
  d=2   L 646  T=0 F=1010  T=0 F=20  if(stop_reading) {
  d=2   L 666  T=5 F=4  T=0 F=0  if(!k->header && (nread > 0 || is_empty_data)) {
  d=2   L 666  T=2 F=2  T=0 F=0  if(!k->header && (nread > 0 || is_empty_data)) {
  d=2   L 666  T=9 F=1010  T=0 F=20  if(!k->header && (nread > 0 || is_empty_data)) {
  d=2   L 668  T=0 F=7  T=0 F=0  if(data->set.opt_no_body) {
  d=2   L 676  T=4 F=2  T=0 F=0  if(0 == k->bodywrites && !is_empty_data) {
  d=2   L 676  T=6 F=1  T=0 F=0  if(0 == k->bodywrites && !is_empty_data) {
  d=2   L 679  T=4 F=0  T=0 F=0  if(conn->handler->protocol&(PROTO_FAMILY_HTTP|CURLPROTO_R...
  d=2   L 682  T=0 F=4  T=0 F=0  if(result || *done)
  d=2   L 682  T=0 F=4  T=0 F=0  if(result || *done)
  d=2   L 691  T=0 F=7  T=0 F=0  if(data->set.verbose) {
  d=2   L 706  T=0 F=7  T=0 F=0  if(k->chunk) {
  d=2   L 742  T=0 F=7  T=0 F=0  if((k->badheader == HEADER_PARTHEADER) && !k->ignorebody) {
  d=2   L 748  T=0 F=7  T=0 F=0  if((-1 != k->maxdownload) &&
  d=2   L 780  T=2 F=0  T=0 F=0  if(!k->chunk && (nread || k->badheader || is_empty_data)) {
  d=2   L 780  T=5 F=2  T=0 F=0  if(!k->chunk && (nread || k->badheader || is_empty_data)) {
  d=2   L 780  T=0 F=2  T=0 F=0  if(!k->chunk && (nread || k->badheader || is_empty_data)) {
  d=2   L 780  T=7 F=0  T=0 F=0  if(!k->chunk && (nread || k->badheader || is_empty_data)) {
  d=2   L 783  T=0 F=7  T=0 F=0  if(k->badheader && !k->ignorebody) {
  d=2   L 801  T=7 F=0  T=0 F=0  if(k->badheader < HEADER_ALLBAD) {
  d=2   L 807  T=7 F=0  T=0 F=0  if(data->set.http_ce_skip || !k->writer_stack) {
  d=2   L 807  T=0 F=7  T=0 F=0  if(data->set.http_ce_skip || !k->writer_stack) {
  d=2   L 808  T=5 F=2  T=0 F=0  if(!k->ignorebody && nread) {
  d=2   L 808  T=7 F=0  T=0 F=0  if(!k->ignorebody && nread) {
  d=2   L 810  T=0 F=5  T=0 F=0  if(conn->handler->protocol & PROTO_FAMILY_POP3)
  d=2   L 823  T=0 F=7  T=0 F=0  if(result)
  d=2   L 829  T=0 F=1010  T=0 F=20  if(conn->handler->readwrite && excess) {
  d=2   L 849  T=1000 F=13  T=20 F=0  if(is_empty_data) {
  d=2   L 855  T=0 F=1010  T=0 F=20  if(k->keepon & KEEP_RECV_PAUSE) {
  d=2   L 860  T=1010 F=0  T=0 F=20  } while(data_pending(data) && maxloops--);
  d=2   L 860  T=1000 F=10  T=0 F=0  } while(data_pending(data) && maxloops--);
  d=2   L 862  T=10 F=7  T=0 F=20  if(maxloops <= 0) {
  d=2   L 868  T=4 F=13  T=0 F=20  if(((k->keepon & (KEEP_RECV|KEEP_SEND)) == KEEP_SEND) &&
  d=2   L 869  T=1 F=3  T=0 F=0  conn->bits.close) {
--- d=1  transfer.c:data_pending  (/src/curl/lib/transfer.c:448-473) ---
  d=1   L 456  T=0 F=1010  T=0 F=20  if(conn->handler->protocol&PROTO_FAMILY_FTP)
  d=1   L 461  T=0 F=1010  T=0 F=20  return conn->handler->protocol&(CURLPROTO_SCP|CURLPROTO_S...
  d=1   L 470  T=1010 F=0  T=20 F=0  ((conn->handler->protocol&PROTO_FAMILY_HTTP) && conn->htt...  <-- BLOCKER
  d=1   L 470  T=1010 F=0  T=0 F=20  ((conn->handler->protocol&PROTO_FAMILY_HTTP) && conn->htt...  <-- BLOCKER
  d=1   L 472  T=0 F=0  T=0 F=20  Curl_ssl_data_pending(conn, FIRSTSOCKET);

[off-chain: 60 additional divergent branches across 8 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=32d10b449c4075ee, size=131 bytes, fuzzer=cmplog, trial=1, discovered_at=7757s, mutation_op=BytesDeleteMutator,ByteNegMutator,BytesDeleteMutator,BytesRandSetMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 25 00 3a 2f 2f 31 32 25   ......po%.://12%
  0010: 2f 30 28 28 2e 31 3a 39 30 30 31 2f 38 35 30 00   /0((.1:9001/850.
  0020: 02 00 00 00 47 48 54 54 50 2f 32 37 2e 30 2e 2f   ....GHTTP/27.0./
  0030: 2f 2f 2f 2f 2f 2f 2e 2f 2f 2f 2f 25 74 65 6e 74   //////.////%tent
Seed 2 (id=d3cb6bfbb0737585, size=131 bytes, fuzzer=cmplog, trial=1, discovered_at=7775s, mutation_op=BytesSetMutator):
  0000: 00 01 00 00 00 19 70 6f 25 ad 25 2f 2f 31 32 25   ......po%.%//12%
  0010: 2f 30 28 28 2e 31 3a 39 30 30 31 2f 38 35 30 00   /0((.1:9001/850.
  0020: 02 00 00 00 47 48 54 54 50 2f 32 37 2e 30 2e 2f   ....GHTTP/27.0./
  0030: 2f 2f 2f 2f 2f 2f 2e 2f 2f 2f 2f 25 74 65 6e 74   //////.////%tent
Seed 3 (id=33867fc1c42dc542, size=131 bytes, fuzzer=cmplog, trial=1, discovered_at=12913s, mutation_op=TokenInsert,BytesDeleteMutator,ByteIncMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 19 70 6f 25 ad 25 2f 2f 31 32 25   ......po%.%//12%
  0010: 2f 30 28 28 2e 31 3a 39 30 30 31 2f 38 35 30 00   /0((.1:9001/850.
  0020: 02 00 00 00 47 48 54 54 50 2f 32 37 2e 30 2e 2f   ....GHTTP/27.0./
  0030: 2f 2f 2f 2f 2f 2f 2e 2f 2f 2f 2f 25 74 65 6e 74   //////.////%tent
Seed 4 (id=cf948dc66207fdd3, size=131 bytes, fuzzer=cmplog, trial=1, discovered_at=13161s, mutation_op=TokenReplace,WordInterestingMutator):
  0000: 00 01 00 00 00 19 70 6f 25 00 3a 2f 2f 31 0a 56   ......po%.://1.V
  0010: 95 ce 57 53 f2 dd 3a 39 30 30 31 2f 38 35 30 00   ..WS..:9001/850.
  0020: 02 00 00 00 47 48 54 54 50 2f 32 37 2e 30 2e 2f   ....GHTTP/27.0./
  0030: 2f 2f 2f 2f 2f 2f 2e 2f 2f 2f 2f 25 74 65 6e 74   //////.////%tent
Seed 5 (id=75b3329660f25ba4, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=15708s, mutation_op=WordInterestingMutator,DwordAddMutator,ByteRandMutator,BytesSetMutator,BytesRandSetMutator,BitFlipMutator):
  0000: 00 01 00 00 00 19 9a 9a 70 33 cb 2f 3a 3a 00 10   ........p3./::..
  0010: 09 09 09 09 09 09 08 09 30 30 31 ad 38 35 30 00   ........001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 32 32 32 32 32 25   ....GHTTP/22222%
  0030: 6d 3a 54 68 65 72 65 2c 0a 54 72 61 6e 53 7e 65   m:There,.TranS~e

==== Loser-blocking seeds (take false branch) ====
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
   0x0005  19(.)x16                            19(.)x10 43(C)x3 2e(.)x2 44(D)x1 +4u  PARTIAL
   0x0006  70(p)x12 9a(.)x4                    25(%)x4 64(d)x3 2e(.)x3 43(C)x2 +7u  PARTIAL
   0x0007  6f(o)x8 9a(.)x4 25(%)x2 bb(.)x2     55(U)x2 41(A)x2 25(%)x2 2e(.)x2 +12u  PARTIAL
   0x0008  70(p)x8 25(%)x6 00(.)x2             43(C)x5 2e(.)x3 25(%)x3 41(A)x2 +7u  PARTIAL
   0x0009  33(3)x10 00(.)x4 ad(.)x2            25(%)x4 2b(+)x2 46(F)x2 2e(.)x1 +11u  DIFFER
   0x000a  4b(K)x6 3a(:)x4 cb(.)x4 25(%)x2     25(%)x7 2e(.)x3 51(Q)x1 3e(>)x1 +8u  PARTIAL
   0x000b  2f(/)x13 00(.)x1 c8(.)x1 2d(-)x1    25(%)x5 2e(.)x3 63(c)x2 66(f)x1 +9u  PARTIAL
   0x000c  2f(/)x10 3a(:)x4 00(.)x1 72(r)x1    2e(.)x5 25(%)x4 41(A)x2 45(E)x2 +7u  DIFFER
   0x000d  31(1)x6 3a(:)x5 3f(?)x4 ad(.)x1     2e(.)x3 25(%)x2 48(H)x1 9f(.)x1 +13u  PARTIAL
   0x0016  3a(:)x11 08(.)x4 00(.)x1            41(A)x3 2e(.)x2 64(d)x2 25(%)x2 +11u  DIFFER
   0x0017  39(9)x11 09(.)x4 6e(n)x1            41(A)x3 2e(.)x3 25(%)x3 00(.)x1 +10u  DIFFER
   0x0018  30(0)x15 4c(L)x1                    43(C)x3 2e(.)x3 00(.)x2 41(A)x2 +8u  DIFFER
   0x0019  30(0)x16                            25(%)x3 2b(+)x3 00(.)x2 40(@)x2 +10u  DIFFER
   0x001a  31(1)x16                            25(%)x5 41(A)x3 f9(.)x1 2b(+)x1 +10u  DIFFER
   0x001c  38(8)x15 58(X)x1                    2e(.)x3 45(E)x3 2b(+)x2 ff(.)x1 +11u  DIFFER
   0x001d  35(5)x16                            2e(.)x2 64(d)x2 2d(-)x2 ff(.)x1 +13u  DIFFER
   0x001e  30(0)x16                            25(%)x4 44(D)x2 49(I)x1 65(e)x1 +12u  DIFFER
   0x001f  00(.)x16                            25(%)x3 2e(.)x3 41(A)x2 62(b)x1 +11u  DIFFER
   0x0020  02(.)x14 11(.)x2                    65(e)x2 42(B)x2 2e(.)x2 7e(~)x1 +13u  DIFFER
   0x0021  00(.)x16                            25(%)x3 2d(-)x3 05(.)x1 69(i)x1 +11u  PARTIAL
   0x0022  00(.)x16                            44(D)x3 2e(.)x2 61(a)x1 74(t)x1 +10u  PARTIAL
   0x0023  00(.)x16                            2e(.)x2 25(%)x2 d6(.)x1 bb(.)x1 +6u  DIFFER
   0x0024  47(G)x16                            50(P)x2 42(B)x1 9e(.)x1 2e(.)x1 +5u  DIFFER
   0x0025  48(H)x13 68(h)x2 00(.)x1            25(%)x3 2e(.)x3 41(A)x2 64(d)x1 +1u  DIFFER
   0x0026  54(T)x12 72(r)x2 6f(o)x1 00(.)x1    2e(.)x2 45(E)x1 41(A)x1 25(%)x1 +5u  DIFFER
   0x0027  54(T)x12 37(7)x3 6f(o)x1            72(r)x1 27(')x1 40(@)x1 2e(.)x1 +6u  DIFFER
   0x0028  50(P)x12 6d(m)x2 fc(.)x2            25(%)x4 2e(.)x2 33(3)x1 db(.)x1 +2u  PARTIAL
   0x0029  2f(/)x12 3a(:)x2 ff(.)x2            25(%)x2 31(1)x1 2e(.)x1 42(B)x1 +5u  DIFFER
   0x002a  32(2)x12 20( )x2 ff(.)x2            25(%)x3 65(e)x1 2e(.)x1 42(B)x1 +4u  DIFFER
   0x0033  2f(/)x6 68(h)x4 72(r)x2 65(e)x1 +3u  25(%)x3 2e(.)x2 41(A)x2 bd(.)x1     DIFFER
   0x0036  2e(.)x6 65(e)x5 0a(.)x2 0d(.)x1 +2u  25(%)x4 4e(N)x1 45(E)x1 44(D)x1     DIFFER
   0x0038  2f(/)x6 0a(.)x5 72(r)x2 00(.)x1 +2u  25(%)x3 42(B)x2 80(.)x1 64(d)x1     DIFFER
   0x0039  2f(/)x6 54(T)x3 0a(.)x2 61(a)x2 +3u  25(%)x3 62(b)x2                     DIFFER
   0x003a  2f(/)x6 72(r)x2 6c(l)x2 6e(n)x2 +4u  25(%)x2 9e(.)x1 42(B)x1 65(e)x1     PARTIAL
   0x003b  25(%)x6 00(.)x3 61(a)x2 37(7)x2 +3u  25(%)x2 66(f)x1 42(B)x1 65(e)x1     PARTIAL
   0x003c  74(t)x6 66(f)x3 6e(n)x2 2d(-)x2 +2u  64(d)x2 26(&)x1 52(R)x1 25(%)x1     DIFFER
   0x003e  6e(n)x6 72(r)x3 7e(~)x2 76(v)x2 +2u  40(@)x2 25(%)x2 79(y)x1             DIFFER
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
  prompts_b/curl_415.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 415,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 415 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 415 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 415 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).