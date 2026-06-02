==== BLOCKER ====
Target: curl
Branch ID: 459
Location: /src/curl/lib/transfer.c:1303:36
Enclosing function: Curl_readwrite
Source line:     if(!(data->set.opt_no_body) && (k->size != -1) &&
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
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=6.80h  loser=24.00h
  avg hitcount on branch: winner=3  loser=0
  prob_div=1.00  dur_div=17.20h  hit_div=3
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=6.00h  loser=24.00h
  avg hitcount on branch: winner=4  loser=0
  prob_div=1.00  dur_div=18.00h  hit_div=4
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/459/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_readwrite (/src/curl/lib/transfer.c:1167-1340) ---
[ ]  1165                          bool *done,
[ ]  1166                          bool *comeback)
[B]  1167  {
[B]  1168    struct SingleRequest *k = &data->req;
[B]  1169    CURLcode result;
[B]  1170    int didwhat = 0;
[ ]  1171  
[B]  1172    curl_socket_t fd_read;
[B]  1173    curl_socket_t fd_write;
[B]  1174    int select_res = conn->cselect_bits;
[ ]  1175  
[B]  1176    conn->cselect_bits = 0;
[ ]  1177  
[ ]  1178    /* only use the proper socket if the *_HOLD bit is not set simultaneously as
[ ]  1179       then we are in rate limiting state in that transfer direction */
[ ]  1180  
[B]  1181    if((k->keepon & KEEP_RECVBITS) == KEEP_RECV)
[B]  1182      fd_read = conn->sockfd;
[ ]  1183    else
[ ]  1184      fd_read = CURL_SOCKET_BAD;
[ ]  1185  
[B]  1186    if((k->keepon & KEEP_SENDBITS) == KEEP_SEND)
[W]  1187      fd_write = conn->writesockfd;
[B]  1188    else
[B]  1189      fd_write = CURL_SOCKET_BAD;
[ ]  1190  
[B]  1191  #if defined(USE_HTTP2) || defined(USE_HTTP3)
[B]  1192    if(data->state.drain) {
[ ]  1193      select_res |= CURL_CSELECT_IN;
[ ]  1194      DEBUGF(infof(data, "Curl_readwrite: forcibly told to drain data"));
[ ]  1195    }
[B]  1196  #endif
[ ]  1197  
[B]  1198    if(!select_res) /* Call for select()/poll() only, if read/write/error
[ ]  1199                       status is not known. */
[B]  1200      select_res = Curl_socket_check(fd_read, CURL_SOCKET_BAD, fd_write, 0);
[ ]  1201  
[B]  1202    if(select_res == CURL_CSELECT_ERR) {
[ ]  1203      failf(data, "select/poll returned error");
[ ]  1204      return CURLE_SEND_ERROR;
[ ]  1205    }
[ ]  1206  
[ ]  1207  #ifdef USE_HYPER
[ ]  1208    if(conn->datastream) {
[ ]  1209      result = conn->datastream(data, conn, &didwhat, done, select_res);
[ ]  1210      if(result || *done)
[ ]  1211        return result;
[ ]  1212    }
[ ]  1213    else {
[ ]  1214  #endif
[ ]  1215    /* We go ahead and do a read if we have a readable socket or if
[ ]  1216       the stream was rewound (in which case we have data in a
[ ]  1217       buffer) */
[B]  1218    if((k->keepon & KEEP_RECV) && (select_res & CURL_CSELECT_IN)) {
[B]  1219      result = readwrite_data(data, conn, k, &didwhat, done, comeback);
[B]  1220      if(result || *done)
[ ]  1221        return result;
[B]  1222    }
[ ]  1223  
[ ]  1224    /* If we still have writing to do, we check if we have a writable socket. */
[B]  1225    if((k->keepon & KEEP_SEND) && (select_res & CURL_CSELECT_OUT)) {
[ ]  1226      /* write */
[ ]  1227  
[W]  1228      result = readwrite_upload(data, conn, &didwhat);
[W]  1229      if(result)
[ ]  1230        return result;
[W]  1231    }
[ ]  1232  #ifdef USE_HYPER
[ ]  1233    }
[ ]  1234  #endif
[ ]  1235  
[B]  1236    k->now = Curl_now();
[B]  1237    if(!didwhat) {
[ ]  1238      /* no read no write, this is a timeout? */
[ ]  1239      if(k->exp100 == EXP100_AWAITING_CONTINUE) {
[ ]  1240        /* This should allow some time for the header to arrive, but only a
[ ]  1241           very short time as otherwise it'll be too much wasted time too
[ ]  1242           often. */
[ ]  1243  
[ ]  1244        /* Quoting RFC2616, section "8.2.3 Use of the 100 (Continue) Status":
[ ]  1245  
[ ]  1246           Therefore, when a client sends this header field to an origin server
[ ]  1247           (possibly via a proxy) from which it has never seen a 100 (Continue)
[ ]  1248           status, the client SHOULD NOT wait for an indefinite period before
[ ]  1249           sending the request body.
[ ]  1250  
[ ]  1251        */
[ ]  1252  
[ ]  1253        timediff_t ms = Curl_timediff(k->now, k->start100);
[ ]  1254        if(ms >= data->set.expect_100_timeout) {
[ ]  1255          /* we've waited long enough, continue anyway */
[ ]  1256          k->exp100 = EXP100_SEND_DATA;
[ ]  1257          k->keepon |= KEEP_SEND;
[ ]  1258          Curl_expire_done(data, EXPIRE_100_TIMEOUT);
[ ]  1259          infof(data, "Done waiting for 100-continue");
[ ]  1260        }
[ ]  1261      }
[ ]  1262  
[ ]  1263  #ifdef ENABLE_QUIC
[ ]  1264      if(conn->transport == TRNSPRT_QUIC) {
[ ]  1265        result = Curl_quic_idle(data);
[ ]  1266        if(result)
[ ]  1267          return result;
[ ]  1268      }
[ ]  1269  #endif
[ ]  1270    }
[ ]  1271  
[B]  1272    if(Curl_pgrsUpdate(data))
[ ]  1273      result = CURLE_ABORTED_BY_CALLBACK;
[B]  1274    else
[B]  1275      result = Curl_speedcheck(data, k->now);
[B]  1276    if(result)
[ ]  1277      return result;
[ ]  1278  
[B]  1279    if(k->keepon) {
[W]  1280      if(0 > Curl_timeleft(data, &k->now, FALSE)) {
[ ]  1281        if(k->size != -1) {
[ ]  1282          failf(data, "Operation timed out after %" CURL_FORMAT_TIMEDIFF_T
[ ]  1283                " milliseconds with %" CURL_FORMAT_CURL_OFF_T " out of %"
[ ]  1284                CURL_FORMAT_CURL_OFF_T " bytes received",
[ ]  1285                Curl_timediff(k->now, data->progress.t_startsingle),
[ ]  1286                k->bytecount, k->size);
[ ]  1287        }
[ ]  1288        else {
[ ]  1289          failf(data, "Operation timed out after %" CURL_FORMAT_TIMEDIFF_T
[ ]  1290                " milliseconds with %" CURL_FORMAT_CURL_OFF_T " bytes received",
[ ]  1291                Curl_timediff(k->now, data->progress.t_startsingle),
[ ]  1292                k->bytecount);
[ ]  1293        }
[ ]  1294        return CURLE_OPERATION_TIMEDOUT;
[ ]  1295      }
[W]  1296    }
[B]  1297    else {
[ ]  1298      /*
[ ]  1299       * The transfer has been performed. Just make some general checks before
[ ]  1300       * returning.
[ ]  1301       */
[ ]  1302  
[B]  1303      if(!(data->set.opt_no_body) && (k->size != -1) && <-- BLOCKER
[B]  1304         (k->bytecount != k->size) &&
[B]  1305  #ifdef CURL_DO_LINEEND_CONV
[ ]  1306         /* Most FTP servers don't adjust their file SIZE response for CRLFs,
[ ]  1307            so we'll check to see if the discrepancy can be explained
[ ]  1308            by the number of CRLFs we've changed to LFs.
[ ]  1309         */
[B]  1310         (k->bytecount != (k->size + data->state.crlf_conversions)) &&
[B]  1311  #endif /* CURL_DO_LINEEND_CONV */
[B]  1312         !k->newurl) {
[W]  1313        failf(data, "transfer closed with %" CURL_FORMAT_CURL_OFF_T
[W]  1314              " bytes remaining to read", k->size - k->bytecount);
[W]  1315        return CURLE_PARTIAL_FILE;
[W]  1316      }
[B]  1317      if(!(data->set.opt_no_body) && k->chunk &&
[B]  1318         (conn->chunk.state != CHUNK_STOP)) {
[ ]  1319        /*
[ ]  1320         * In chunked mode, return an error if the connection is closed prior to
[ ]  1321         * the empty (terminating) chunk is read.
[ ]  1322         *
[ ]  1323         * The condition above used to check for
[ ]  1324         * conn->proto.http->chunk.datasize != 0 which is true after reading
[ ]  1325         * *any* chunk, not just the empty chunk.
[ ]  1326         *
[ ]  1327         */
[ ]  1328        failf(data, "transfer closed with outstanding read data remaining");
[ ]  1329        return CURLE_PARTIAL_FILE;
[ ]  1330      }
[B]  1331      if(Curl_pgrsUpdate(data))
[ ]  1332        return CURLE_ABORTED_BY_CALLBACK;
[B]  1333    }
[ ]  1334  
[ ]  1335    /* Now update the "done" boolean we return */
[B]  1336    *done = (0 == (k->keepon&(KEEP_RECV|KEEP_SEND|
[B]  1337                              KEEP_RECV_PAUSE|KEEP_SEND_PAUSE))) ? TRUE : FALSE;
[ ]  1338  
[B]  1339    return CURLE_OK;
[B]  1340  }

--- Caller (1 hop): multi.c:multi_runsingle (/src/curl/lib/multi.c:1811-2661, calls Curl_readwrite at line 2405) (±10 around call site) ---
[ ]  2395          Curl_ratelimit(data, *nowp);
[ ]  2396          multistate(data, MSTATE_RATELIMITING);
[ ]  2397          if(send_timeout_ms >= recv_timeout_ms)
[ ]  2398            Curl_expire(data, send_timeout_ms, EXPIRE_TOOFAST);
[ ]  2399          else
[ ]  2400            Curl_expire(data, recv_timeout_ms, EXPIRE_TOOFAST);
[ ]  2401          break;
[ ]  2402        }
[ ]  2403  
[ ]  2404        /* read/write data if it is ready to do so */
[B]  2405        result = Curl_readwrite(data->conn, data, &done, &comeback); <-- CALL
[ ]  2406  
[B]  2407        if(done || (result == CURLE_RECV_ERROR)) {
[ ]  2408          /* If CURLE_RECV_ERROR happens early enough, we assume it was a race
[ ]  2409           * condition and the server closed the re-used connection exactly when
[ ]  2410           * we wanted to use it, so figure out if that is indeed the case.
[ ]  2411           */
[B]  2412          CURLcode ret = Curl_retry_request(data, &newurl);
[B]  2413          if(!ret)
[B]  2414            retry = (newurl)?TRUE:FALSE;
[ ]  2415          else if(!result)

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_readwrite at line 2405)
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
      58       200  multi.c:mstate  (/src/curl/lib/multi.c:153-209)
      60       180  multi.c:multi_ischanged  (/src/curl/lib/multi.c:1564-1569)
      41       131  Curl_checkheaders  (/src/curl/lib/transfer.c:102-114)
      36       120  Curl_detach_connection  (/src/curl/lib/multi.c:949-957)
      38       120  multi.c:multi_handle_timeout  (/src/curl/lib/multi.c:1641-1683)
      24        80  Curl_expire_clear  (/src/curl/lib/multi.c:3579-3610)
      19        60  multi.c:multi_deltimeout  (/src/curl/lib/multi.c:3436-3447)
      19        60  multi.c:multi_addtimeout  (/src/curl/lib/multi.c:3460-3490)
      19        60  Curl_expire  (/src/curl/lib/multi.c:3504-3559)
      12        40  Curl_attach_connection  (/src/curl/lib/multi.c:966-975)
      12        40  Curl_preconnect  (/src/curl/lib/multi.c:1794-1801)
       4        20  Curl_retry_request  (/src/curl/lib/transfer.c:1855-1925)
       6        20  multi.c:before_perform  (/src/curl/lib/multi.c:132-135)
       6        20  multi.c:init_completed  (/src/curl/lib/multi.c:138-145)
       6        20  multi.c:sh_getentry  (/src/curl/lib/multi.c:238-244)
... (27 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=5  curl_multi_add_handle  (/src/curl/lib/multi.c:464-590) ---
  d=5   L 476  T=0 F=6  T=0 F=20  if(data->multi)
  d=5   L 479  T=0 F=6  T=0 F=20  if(multi->in_callback)
  d=5   L 482  T=0 F=6  T=0 F=20  if(multi->dead) {
  d=5   L 500  T=0 F=6  T=0 F=20  if(data->set.errorbuffer)
  d=5   L 528  T=0 F=6  T=0 F=20  if(rc)
  d=5   L 536  T=6 F=0  T=20 F=0  if(!data->dns.hostcache ||
  d=5   L 543  T=0 F=6  T=0 F=20  if(data->share && (data->share->specifier & (1<< CURL_LOC...
  d=5   L 559  T=0 F=6  T=0 F=20  if(multi->easyp) {
--- d=3  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716) ---
  d=3   L2674  T=0 F=10  T=0 F=20  if(multi->in_callback)
  d=3   L2678  T=10 F=10  T=20 F=20  while(data) {
  d=3   L2686  T=0 F=10  T=0 F=20  if(result)
  d=3   L2704  T=4 F=10  T=0 F=20  if(t)
  d=3   L2708  T=4 F=10  T=0 F=20  } while(t);
  d=3   L2712  T=10 F=0  T=20 F=0  if(CURLM_OK >= returncode)
--- d=2  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661) ---
  d=2   L1827  T=0 F=10  T=0 F=20  if(multi->dead) {
  d=2   L1842  T=0 F=50  T=0 F=160  if(multi_ischanged(multi, TRUE)) {
  d=2   L1847  T=38 F=12  T=120 F=40  if(data->mstate > MSTATE_CONNECT &&
  d=2   L1848  T=38 F=0  T=120 F=0  data->mstate < MSTATE_COMPLETED) {
  d=2   L1851  T=0 F=38  T=0 F=120  if(!data->conn)
  d=2   L1855  T=38 F=12  T=120 F=40  if(data->conn &&
  d=2   L1856  T=38 F=0  T=120 F=0  (data->mstate >= MSTATE_CONNECT) &&
  d=2   L1857  T=38 F=0  T=120 F=0  (data->mstate < MSTATE_COMPLETED)) {
  d=2   L1867  T=0 F=38  T=0 F=120  if(multi_handle_timeout(data, nowp, &stream_error, &resul...
  d=2   L1874  T=6 F=44  T=20 F=140  case MSTATE_INIT:
  d=2   L1878  T=6 F=0  T=20 F=0  if(!result) {
  d=2   L1886  T=0 F=50  T=0 F=160  case MSTATE_PENDING:
  d=2   L1891  T=6 F=44  T=20 F=140  case MSTATE_CONNECT:
  d=2   L1895  T=0 F=6  T=0 F=20  if(result)
  d=2   L1899  T=6 F=0  T=20 F=0  if(data->set.timeout)
  d=2   L1902  T=0 F=6  T=0 F=20  if(data->set.connecttimeout)
  d=2   L1906  T=0 F=6  T=0 F=20  if(CURLE_NO_CONNECTION_AVAILABLE == result) {
  d=2   L1917  T=0 F=6  T=0 F=20  else if(data->state.previouslypending) {
  d=2   L1923  T=6 F=0  T=20 F=0  if(!result) {
  d=2   L1924  T=0 F=6  T=0 F=20  if(async)
  d=2   L1933  T=0 F=6  T=0 F=20  if(protocol_connected)
  d=2   L1937  T=0 F=6  T=0 F=20  if(Curl_connect_ongoing(data->conn))
  d=2   L1947  T=0 F=50  T=0 F=160  case MSTATE_RESOLVING:
  d=2   L2024  T=0 F=50  T=0 F=160  case MSTATE_TUNNELING:
  d=2   L2055  T=6 F=44  T=20 F=140  case MSTATE_CONNECTING:
  d=2   L2059  T=6 F=0  T=20 F=0  if(connected && !result) {
  d=2   L2059  T=6 F=0  T=20 F=0  if(connected && !result) {
  d=2   L2063  T=0 F=6  T=0 F=20  (data->conn->http_proxy.proxytype == CURLPROXY_HTTPS &&
  d=2   L2066  T=0 F=6  T=0 F=20  Curl_connect_ongoing(data->conn)) {
  d=2   L2089  T=6 F=44  T=20 F=140  case MSTATE_PROTOCONNECT:
  d=2   L2091  T=0 F=6  T=0 F=20  if(!result && !protocol_connected)
  d=2   L2091  T=6 F=0  T=20 F=0  if(!result && !protocol_connected)
  d=2   L2094  T=6 F=0  T=20 F=0  else if(!result) {
  d=2   L2107  T=0 F=50  T=0 F=160  case MSTATE_PROTOCONNECTING:
  d=2   L2123  T=6 F=44  T=20 F=140  case MSTATE_DO:
  d=2   L2124  T=0 F=6  T=0 F=20  if(data->set.fprereq) {
  d=2   L2146  T=0 F=6  T=0 F=20  if(data->set.connect_only == 1) {
  d=2   L2159  T=6 F=0  T=20 F=0  if(!result) {
  d=2   L2160  T=0 F=6  T=0 F=20  if(!dophase_done) {
  d=2   L2184  T=0 F=6  T=0 F=20  else if(data->conn->bits.do_more) {
  d=2   L2254  T=0 F=50  T=0 F=160  case MSTATE_DOING:
  d=2   L2274  T=0 F=50  T=0 F=160  case MSTATE_DOING_MORE:
  d=2   L2301  T=6 F=44  T=20 F=140  case MSTATE_DID:
  d=2   L2303  T=0 F=6  T=0 F=20  if(data->conn->bits.multiplex)
  d=2   L2309  T=6 F=0  T=20 F=0  if((data->conn->sockfd != CURL_SOCKET_BAD) ||
  d=2   L2324  T=0 F=50  T=0 F=160  case MSTATE_RATELIMITING: /* limit-rate exceeded in eithe...
  d=2   L2370  T=10 F=40  T=20 F=140  case MSTATE_PERFORMING:
  d=2   L2378  T=0 F=10  T=0 F=20  if(data->set.max_send_speed)
  d=2   L2387  T=0 F=10  T=0 F=20  if(data->set.max_recv_speed)
  d=2   L2394  T=0 F=10  T=0 F=20  if(send_timeout_ms || recv_timeout_ms) {
  d=2   L2394  T=0 F=10  T=0 F=20  if(send_timeout_ms || recv_timeout_ms) {
  d=2   L2407  T=4 F=6  T=20 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=2   L2407  T=0 F=6  T=0 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=2   L2413  T=4 F=0  T=20 F=0  if(!ret)
  d=2   L2414  T=0 F=4  T=0 F=20  retry = (newurl)?TRUE:FALSE;
  d=2   L2418  T=0 F=4  T=0 F=20  if(retry) {
  d=2   L2425  T=0 F=6  T=0 F=0  else if((CURLE_HTTP2_STREAM == result) &&
  d=2   L2448  T=2 F=8  T=0 F=20  if(result) {
  d=2   L2457  T=2 F=0  T=0 F=0  if(!(data->conn->handler->flags & PROTOPT_DUAL) &&
  d=2   L2458  T=2 F=0  T=0 F=0  result != CURLE_HTTP2_STREAM)
  d=2   L2464  T=4 F=4  T=20 F=0  else if(done) {
  d=2   L2471  T=0 F=4  T=0 F=20  if(data->req.newurl || retry) {
  d=2   L2471  T=0 F=4  T=0 F=20  if(data->req.newurl || retry) {
  d=2   L2497  T=0 F=4  T=0 F=20  if(data->req.location) {
  d=2   L2509  T=4 F=0  T=20 F=0  if(!result) {
  d=2   L2515  T=0 F=4  T=0 F=0  else if(comeback) {
  d=2   L2525  T=4 F=46  T=20 F=140  case MSTATE_DONE:
  d=2   L2529  T=4 F=0  T=20 F=0  if(data->conn) {
  d=2   L2532  T=0 F=4  T=0 F=20  if(data->conn->bits.multiplex)
  d=2   L2540  T=4 F=0  T=20 F=0  if(!result)
  d=2   L2545  T=0 F=4  T=0 F=20  if(data->state.wildcardmatch) {
  d=2   L2559  T=0 F=50  T=0 F=160  case MSTATE_COMPLETED:
  d=2   L2562  T=0 F=50  T=0 F=160  case MSTATE_MSGSENT:
  d=2   L2566  T=0 F=50  T=0 F=160  default:
  d=2   L2570  T=38 F=12  T=120 F=40  if(data->conn &&
  d=2   L2571  T=38 F=0  T=120 F=0  data->mstate >= MSTATE_CONNECT &&
  d=2   L2572  T=12 F=26  T=40 F=80  data->mstate < MSTATE_DO &&
  d=2   L2573  T=0 F=12  T=0 F=40  rc != CURLM_CALL_MULTI_PERFORM &&
  d=2   L2586  T=46 F=4  T=140 F=20  if(data->mstate < MSTATE_COMPLETED) {
  d=2   L2587  T=2 F=44  T=0 F=140  if(result) {
  d=2   L2599  T=0 F=2  T=0 F=0  if(data->conn) {
  d=2   L2617  T=0 F=2  T=0 F=0  else if(data->mstate == MSTATE_CONNECT) {
  d=2   L2626  T=0 F=38  T=0 F=120  else if(data->conn && Curl_pgrsUpdate(data)) {
  d=2   L2626  T=38 F=6  T=120 F=20  else if(data->conn && Curl_pgrsUpdate(data)) {
  d=2   L2639  T=6 F=44  T=20 F=140  if(MSTATE_COMPLETED == data->mstate) {
  d=2   L2640  T=0 F=6  T=0 F=20  if(data->set.fmultidone) {
  d=2   L2657  T=0 F=10  T=0 F=20  } while((rc == CURLM_CALL_MULTI_PERFORM) || multi_ischang...
  d=2   L2657  T=40 F=10  T=140 F=20  } while((rc == CURLM_CALL_MULTI_PERFORM) || multi_ischang...
--- d=1  Curl_readwrite  (/src/curl/lib/transfer.c:1167-1340) ---
  d=1   L1181  T=10 F=0  T=20 F=0  if((k->keepon & KEEP_RECVBITS) == KEEP_RECV)
  d=1   L1186  T=1 F=9  T=0 F=20  if((k->keepon & KEEP_SENDBITS) == KEEP_SEND)
  d=1   L1192  T=0 F=10  T=0 F=20  if(data->state.drain) {
  d=1   L1198  T=10 F=0  T=20 F=0  if(!select_res) /* Call for select()/poll() only, if read...
  d=1   L1202  T=0 F=10  T=0 F=20  if(select_res == CURL_CSELECT_ERR) {
  d=1   L1218  T=10 F=0  T=20 F=0  if((k->keepon & KEEP_RECV) && (select_res & CURL_CSELECT_...
  d=1   L1218  T=10 F=0  T=20 F=0  if((k->keepon & KEEP_RECV) && (select_res & CURL_CSELECT_...
  d=1   L1220  T=0 F=10  T=0 F=20  if(result || *done)
  d=1   L1220  T=0 F=10  T=0 F=20  if(result || *done)
  d=1   L1225  T=1 F=0  T=0 F=0  if((k->keepon & KEEP_SEND) && (select_res & CURL_CSELECT_...
  d=1   L1225  T=1 F=9  T=0 F=20  if((k->keepon & KEEP_SEND) && (select_res & CURL_CSELECT_...
  d=1   L1229  T=0 F=1  T=0 F=0  if(result)
  d=1   L1237  T=0 F=10  T=0 F=20  if(!didwhat) {
  d=1   L1272  T=0 F=10  T=0 F=20  if(Curl_pgrsUpdate(data))
  d=1   L1276  T=0 F=10  T=0 F=20  if(result)
  d=1   L1279  T=4 F=6  T=0 F=20  if(k->keepon) {
  d=1   L1280  T=0 F=4  T=0 F=0  if(0 > Curl_timeleft(data, &k->now, FALSE)) {
  d=1   L1303  T=6 F=0  T=20 F=0  if(!(data->set.opt_no_body) && (k->size != -1) &&  <-- BLOCKER
  d=1   L1303  T=6 F=0  T=0 F=20  if(!(data->set.opt_no_body) && (k->size != -1) &&  <-- BLOCKER
  d=1   L1304  T=2 F=4  T=0 F=0  (k->bytecount != k->size) &&
  d=1   L1310  T=2 F=0  T=0 F=0  (k->bytecount != (k->size + data->state.crlf_conversions)...
  d=1   L1312  T=2 F=0  T=0 F=0  !k->newurl) {
  d=1   L1317  T=0 F=4  T=0 F=20  if(!(data->set.opt_no_body) && k->chunk &&
  d=1   L1317  T=4 F=0  T=20 F=0  if(!(data->set.opt_no_body) && k->chunk &&
  d=1   L1331  T=0 F=4  T=0 F=20  if(Curl_pgrsUpdate(data))
  d=1   L1336  T=4 F=4  T=20 F=0  *done = (0 == (k->keepon&(KEEP_RECV|KEEP_SEND|

[off-chain: 251 additional divergent branches across 40 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=529e44cdba094a04, size=112 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=4631s, mutation_op=QwordAddMutator,ByteAddMutator,TokenReplace,BytesCopyMutator,BytesRandSetMutator,TokenReplace):
  0000: 00 01 00 00 00 19 49 4d 00 50 3a 2f 2f 3f 32 37   ......IM.P://?27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   .0.0.1:9001/850.
  0020: 02 00 00 00 47 48 54 54 50 2f 48 6d 65 40 38 6f   ....GHTTP/Hme@8o
  0030: 6d 65 77 68 65 72 65 0d 25 54 6f 3a 11 66 61 6b   mewhere.%To:.fak
Seed 2 (id=a608095a4d425f1c, size=113 bytes, fuzzer=cmplog, trial=1, discovered_at=12253s, mutation_op=ByteDecMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2f 31 32 00   ......pop.://12.
  0010: 00 30 28 28 2e 31 3a 39 9c 30 31 72 38 35 30 00   .0((.1:9.01r850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 61 06 24   ....GHTTP/ mea.$
  0030: 65 63 8e 65 74 72 65 0d 0a 43 6f 6e 6e 65 63 74   ec.etre..Connect
Seed 3 (id=f899171559e30e59, size=112 bytes, fuzzer=cmplog, trial=1, discovered_at=17456s, mutation_op=BytesSetMutator,QwordAddMutator,ByteDecMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2f 31 32 01   ......pop.://12.
  0010: 30 30 28 28 2e 31 3a 39 9c 05 ff ff 05 35 30 00   00((.1:9.....50.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 61 06 24   ....GHTTP/ mea.$
  0030: 65 63 8e 65 74 72 65 0d 0a 43 6f 6e 74 65 6e 74   ec.etre..Content
Seed 4 (id=b5881836c0b5a0bd, size=112 bytes, fuzzer=cmplog, trial=1, discovered_at=31546s, mutation_op=BitFlipMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 3f 2f 31 32 01   ......pop.:?/12.
  0010: 30 30 28 28 2e 31 3a 39 9c 05 ff ff 05 35 25 00   00((.1:9.....5%.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 61 06 24   ....GHTTP/ mea.$
  0030: 65 63 8e 65 74 72 65 0d 0a 43 6f 6e 74 65 6e 74   ec.etre..Content
Seed 5 (id=707ea75b936eb551, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=38318s, mutation_op=BytesCopyMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 3a 3a 3a 3a   ......pop3K/::::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 31 ad 38 35 30 00   :::::::9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 72 65 0d 0a 54 72 e0 6e 63 66 65   mewhere..Tr.ncfe

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
   0x0005  19(.)x6                             19(.)x10 43(C)x3 2e(.)x2 44(D)x1 +4u  PARTIAL
   0x0006  70(p)x4 49(I)x1 9a(.)x1             25(%)x4 64(d)x3 2e(.)x3 43(C)x2 +7u  PARTIAL
   0x0007  6f(o)x4 4d(M)x1 9a(.)x1             55(U)x2 41(A)x2 25(%)x2 2e(.)x2 +12u  DIFFER
   0x0008  70(p)x5 00(.)x1                     43(C)x5 2e(.)x3 25(%)x3 41(A)x2 +7u  DIFFER
   0x0009  00(.)x3 50(P)x1 33(3)x1 cd(.)x1     25(%)x4 2b(+)x2 46(F)x2 2e(.)x1 +11u  DIFFER
   0x000a  3a(:)x4 4b(K)x1 cb(.)x1             25(%)x7 2e(.)x3 51(Q)x1 3e(>)x1 +8u  DIFFER
   0x000b  2f(/)x5 3f(?)x1                     25(%)x5 2e(.)x3 63(c)x2 66(f)x1 +9u  DIFFER
   0x000c  2f(/)x4 3a(:)x2                     2e(.)x5 25(%)x4 41(A)x2 45(E)x2 +7u  DIFFER
   0x000d  31(1)x3 3a(:)x2 3f(?)x1             2e(.)x3 25(%)x2 48(H)x1 9f(.)x1 +13u  PARTIAL
   0x000e  32(2)x4 3a(:)x1 00(.)x1             25(%)x7 2e(.)x5 63(c)x1 64(d)x1 +6u  DIFFER
   0x0010  30(0)x2 3a(:)x2 2e(.)x1 00(.)x1     2e(.)x4 25(%)x4 42(B)x2 80(.)x1 +9u  PARTIAL
   0x0011  30(0)x4 3a(:)x1 32(2)x1             25(%)x6 2b(+)x2 62(b)x2 2d(-)x2 +8u  DIFFER
   0x0012  28(()x3 3a(:)x2 2e(.)x1             25(%)x3 66(f)x2 41(A)x2 21(!)x1 +12u  PARTIAL
   0x0013  28(()x3 3a(:)x2 30(0)x1             25(%)x3 2d(-)x3 41(A)x2 62(b)x2 +10u  DIFFER
   0x0014  2e(.)x4 3a(:)x1 54(T)x1             25(%)x4 2e(.)x3 47(G)x1 bf(.)x1 +11u  PARTIAL
   0x0015  31(1)x4 3a(:)x2                     25(%)x5 41(A)x3 46(F)x2 4d(M)x2 +8u  DIFFER
   0x0016  3a(:)x5 ff(.)x1                     41(A)x3 2e(.)x2 64(d)x2 25(%)x2 +11u  DIFFER
   0x0017  39(9)x6                             41(A)x3 2e(.)x3 25(%)x3 00(.)x1 +10u  DIFFER
   0x0018  30(0)x3 9c(.)x3                     43(C)x3 2e(.)x3 00(.)x2 41(A)x2 +8u  DIFFER
   0x0019  30(0)x4 05(.)x2                     25(%)x3 2b(+)x3 00(.)x2 40(@)x2 +10u  DIFFER
   0x001a  31(1)x3 ff(.)x2 00(.)x1             25(%)x5 41(A)x3 f9(.)x1 2b(+)x1 +10u  PARTIAL
   0x001b  ff(.)x2 ad(.)x2 2f(/)x1 72(r)x1     25(%)x3 2e(.)x2 2d(-)x2 00(.)x2 +11u  PARTIAL
   0x001c  38(8)x3 05(.)x2 e8(.)x1             2e(.)x3 45(E)x3 2b(+)x2 ff(.)x1 +11u  DIFFER
   0x001d  35(5)x5 03(.)x1                     2e(.)x2 64(d)x2 2d(-)x2 ff(.)x1 +13u  PARTIAL
   0x001e  30(0)x5 25(%)x1                     25(%)x4 44(D)x2 49(I)x1 65(e)x1 +12u  PARTIAL
   0x001f  00(.)x6                             25(%)x3 2e(.)x3 41(A)x2 62(b)x1 +11u  DIFFER
   0x0020  02(.)x6                             65(e)x2 42(B)x2 2e(.)x2 7e(~)x1 +13u  DIFFER
   0x0021  00(.)x6                             25(%)x3 2d(-)x3 05(.)x1 69(i)x1 +11u  PARTIAL
   0x0022  00(.)x6                             44(D)x3 2e(.)x2 61(a)x1 74(t)x1 +10u  PARTIAL
   0x0023  00(.)x6                             2e(.)x2 25(%)x2 d6(.)x1 bb(.)x1 +6u  DIFFER
   0x0024  47(G)x6                             50(P)x2 42(B)x1 9e(.)x1 2e(.)x1 +5u  DIFFER
   0x0025  48(H)x6                             25(%)x3 2e(.)x3 41(A)x2 64(d)x1 +1u  DIFFER
   0x0026  54(T)x6                             2e(.)x2 45(E)x1 41(A)x1 25(%)x1 +5u  DIFFER
   0x0027  54(T)x6                             72(r)x1 27(')x1 40(@)x1 2e(.)x1 +6u  DIFFER
   0x0028  50(P)x6                             25(%)x4 2e(.)x2 33(3)x1 db(.)x1 +2u  PARTIAL
   0x0029  2f(/)x6                             25(%)x2 31(1)x1 2e(.)x1 42(B)x1 +5u  DIFFER
   0x002a  20( )x5 48(H)x1                     25(%)x3 65(e)x1 2e(.)x1 42(B)x1 +4u  DIFFER
   0x002b  6d(m)x5 7d(})x1                     25(%)x4 2e(.)x2 4b(K)x1 66(f)x1 +2u  DIFFER
   0x002c  65(e)x5 98(.)x1                     25(%)x2 2e(.)x2 65(e)x2 d2(.)x1 +3u  PARTIAL
   0x002d  61(a)x3 40(@)x2 a1(.)x1             25(%)x2 2e(.)x2 43(C)x1 ff(.)x1 +4u  PARTIAL
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
  prompts_b/curl_459.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 459,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 459 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 459 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 459 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).