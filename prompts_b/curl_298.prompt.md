==== BLOCKER ====
Target: curl
Branch ID: 298
Location: /src/curl/lib/multi.c:711:11
Enclosing function: multi.c:multi_done
Source line:      ) || conn->bits.close
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             8        2          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.30h  loser=22.90h
  avg hitcount on branch: winner=332  loser=13
  prob_div=0.80  dur_div=16.60h  hit_div=319
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=8.90h  loser=23.30h
  avg hitcount on branch: winner=45  loser=1
  prob_div=0.70  dur_div=14.40h  hit_div=44
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/298/{W,L}/branch_coverage_show.txt

--- Enclosing function: multi.c:multi_done (/src/curl/lib/multi.c:612-746) ---
[ ]   610                                                  after an error was detected */
[ ]   611                             bool premature)
[B]   612  {
[B]   613    CURLcode result;
[B]   614    struct connectdata *conn = data->conn;
[B]   615    unsigned int i;
[ ]   616  
[B]   617    DEBUGF(infof(data, "multi_done: status: %d prem: %d done: %d",
[B]   618                 (int)status, (int)premature, data->state.done));
[ ]   619  
[B]   620    if(data->state.done)
[ ]   621      /* Stop if multi_done() has already been called */
[ ]   622      return CURLE_OK;
[ ]   623  
[ ]   624    /* Stop the resolver and free its own resources (but not dns_entry yet). */
[B]   625    Curl_resolver_kill(data);
[ ]   626  
[ ]   627    /* Cleanup possible redirect junk */
[B]   628    Curl_safefree(data->req.newurl);
[B]   629    Curl_safefree(data->req.location);
[ ]   630  
[B]   631    switch(status) {
[ ]   632    case CURLE_ABORTED_BY_CALLBACK:
[ ]   633    case CURLE_READ_ERROR:
[ ]   634    case CURLE_WRITE_ERROR:
[ ]   635      /* When we're aborted due to a callback return code it basically have to
[ ]   636         be counted as premature as there is trouble ahead if we don't. We have
[ ]   637         many callbacks and protocols work differently, we could potentially do
[ ]   638         this more fine-grained in the future. */
[ ]   639      premature = TRUE;
[B]   640    default:
[B]   641      break;
[B]   642    }
[ ]   643  
[ ]   644    /* this calls the protocol-specific function pointer previously set */
[B]   645    if(conn->handler->done)
[B]   646      result = conn->handler->done(data, status, premature);
[ ]   647    else
[ ]   648      result = status;
[ ]   649  
[B]   650    if(CURLE_ABORTED_BY_CALLBACK != result) {
[ ]   651      /* avoid this if we already aborted by callback to avoid this calling
[ ]   652         another callback */
[B]   653      int rc = Curl_pgrsDone(data);
[B]   654      if(!result && rc)
[ ]   655        result = CURLE_ABORTED_BY_CALLBACK;
[B]   656    }
[ ]   657  
[B]   658    process_pending_handles(data->multi); /* connection / multiplex */
[ ]   659  
[B]   660    CONNCACHE_LOCK(data);
[B]   661    Curl_detach_connection(data);
[B]   662    if(CONN_INUSE(conn)) {
[ ]   663      /* Stop if still used. */
[ ]   664      CONNCACHE_UNLOCK(data);
[ ]   665      DEBUGF(infof(data, "Connection still in use %zu, "
[ ]   666                   "no more multi_done now!",
[ ]   667                   conn->easyq.size));
[ ]   668      return CURLE_OK;
[ ]   669    }
[ ]   670  
[B]   671    data->state.done = TRUE; /* called just now! */
[ ]   672  
[B]   673    if(conn->dns_entry) {
[B]   674      Curl_resolv_unlock(data, conn->dns_entry); /* done with this */
[B]   675      conn->dns_entry = NULL;
[B]   676    }
[B]   677    Curl_hostcache_prune(data);
[B]   678    Curl_safefree(data->state.ulbuf);
[ ]   679  
[ ]   680    /* if the transfer was completed in a paused state there can be buffered
[ ]   681       data left to free */
[B]   682    for(i = 0; i < data->state.tempcount; i++) {
[ ]   683      Curl_dyn_free(&data->state.tempwrite[i].b);
[ ]   684    }
[B]   685    data->state.tempcount = 0;
[ ]   686  
[ ]   687    /* if data->set.reuse_forbid is TRUE, it means the libcurl client has
[ ]   688       forced us to close this connection. This is ignored for requests taking
[ ]   689       place in a NTLM/NEGOTIATE authentication handshake
[ ]   690  
[ ]   691       if conn->bits.close is TRUE, it means that the connection should be
[ ]   692       closed in spite of all our efforts to be nice, due to protocol
[ ]   693       restrictions in our or the server's end
[ ]   694  
[ ]   695       if premature is TRUE, it means this connection was said to be DONE before
[ ]   696       the entire request operation is complete and thus we can't know in what
[ ]   697       state it is for re-using, so we're forced to close it. In a perfect world
[ ]   698       we can add code that keep track of if we really must close it here or not,
[ ]   699       but currently we have no such detail knowledge.
[ ]   700    */
[ ]   701  
[B]   702    if((data->set.reuse_forbid
[B]   703  #if defined(USE_NTLM)
[B]   704        && !(conn->http_ntlm_state == NTLMSTATE_TYPE2 ||
[ ]   705             conn->proxy_ntlm_state == NTLMSTATE_TYPE2)
[B]   706  #endif
[ ]   707  #if defined(USE_SPNEGO)
[ ]   708        && !(conn->http_negotiate_state == GSS_AUTHRECV ||
[ ]   709             conn->proxy_negotiate_state == GSS_AUTHRECV)
[ ]   710  #endif
[B]   711       ) || conn->bits.close <-- BLOCKER
[B]   712         || (premature && !(conn->handler->flags & PROTOPT_STREAM))) {
[L]   713      connclose(conn, "disconnecting");
[L]   714      Curl_conncache_remove_conn(data, conn, FALSE);
[L]   715      CONNCACHE_UNLOCK(data);
[L]   716      Curl_disconnect(data, conn, premature);
[L]   717    }
[W]   718    else {
[W]   719      char buffer[256];
[W]   720      const char *host =
[W]   721  #ifndef CURL_DISABLE_PROXY
[W]   722        conn->bits.socksproxy ?
[ ]   723        conn->socks_proxy.host.dispname :
[W]   724        conn->bits.httpproxy ? conn->http_proxy.host.dispname :
[W]   725  #endif
[W]   726        conn->bits.conn_to_host ? conn->conn_to_host.dispname :
[W]   727        conn->host.dispname;
[ ]   728      /* create string before returning the connection */
[W]   729      long connection_id = conn->connection_id;
[W]   730      msnprintf(buffer, sizeof(buffer),
[W]   731                "Connection #%ld to host %s left intact",
[W]   732                connection_id, host);
[ ]   733      /* the connection is no longer in use by this transfer */
[W]   734      CONNCACHE_UNLOCK(data);
[W]   735      if(Curl_conncache_return_conn(data, conn)) {
[ ]   736        /* remember the most recently used connection */
[W]   737        data->state.lastconnect_id = connection_id;
[W]   738        infof(data, "%s", buffer);
[W]   739      }
[ ]   740      else
[ ]   741        data->state.lastconnect_id = -1;
[W]   742    }
[ ]   743  
[B]   744    Curl_safefree(data->state.buffer);
[B]   745    return result;
[B]   746  }

--- Caller (1 hop): multi.c:multi_runsingle (/src/curl/lib/multi.c:1811-2661, calls multi.c:multi_done at line 2248) (±10 around call site) ---
[ ]  2238            else {
[ ]  2239              /* Have error handler disconnect conn if we can't retry */
[ ]  2240              stream_error = TRUE;
[ ]  2241            }
[ ]  2242            free(newurl);
[ ]  2243          }
[W]  2244          else {
[ ]  2245            /* failure detected */
[W]  2246            Curl_posttransfer(data);
[W]  2247            if(data->conn)
[W]  2248              multi_done(data, result, FALSE); <-- CALL
[W]  2249            stream_error = TRUE;
[W]  2250          }
[B]  2251        }
[B]  2252        break;
[ ]  2253  
[B]  2254      case MSTATE_DOING:
[ ]  2255        /* we continue DOING until the DO phase is complete */
[ ]  2256        DEBUGASSERT(data->conn);
[ ]  2257        result = protocol_doing(data, &dophase_done);
[ ]  2258        if(!result) {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  curl_multi_remove_handle  (/src/curl/lib/multi.c:765-934, calls multi.c:multi_done at line 809)
hop 3  Curl_close  (/src/curl/lib/url.c:380-497, calls curl_multi_remove_handle at line 399)
hop 4  Curl_free_request_state  (/src/curl/lib/url.c:2250-2260, calls Curl_close at line 2256)
hop 5  Curl_connect  (/src/curl/lib/url.c:4208-4246, calls Curl_free_request_state at line 4215)
hop 6  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_connect at line 1905)
hop 7  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 7  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)
hop 8  curl_multi_socket  (/src/curl/lib/multi.c:3288-3296, calls multi.c:multi_socket at line 3292)
hop 8  curl_multi_socket_action  (/src/curl/lib/multi.c:3300-3308, calls multi.c:multi_socket at line 3304)
hop 8  curl_multi_strerror  (/src/curl/lib/strerror.c:364-420, calls curl_multi_perform at line 368)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0        20  multi.c:sh_getentry  (/src/curl/lib/multi.c:238-244)
      17         0  multi.c:close_connect_only  (/src/curl/lib/multi.c:750-761)
      10         0  Curl_multi_max_concurrent_streams  (/src/curl/lib/multi.c:3730-3733)
       2         0  curl_multi_fdset  (/src/curl/lib/multi.c:1099-1154)
       2         0  multi.c:add_next_timeout  (/src/curl/lib/multi.c:3055-3094)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716) ---
  d=7   L2704  T=2 F=19  T=0 F=20  if(t)
  d=7   L2708  T=2 F=19  T=0 F=20  } while(t);
--- d=6  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661) ---
  d=6   L1842  T=10 F=117  T=0 F=160  if(multi_ischanged(multi, TRUE)) {
  d=6   L1848  T=92 F=1  T=120 F=0  data->mstate < MSTATE_COMPLETED) {
  d=6   L2159  T=16 F=1  T=20 F=0  if(!result) {
  d=6   L2196  T=0 F=1  T=0 F=0  else if((CURLE_SEND_ERROR == result) &&
  d=6   L2247  T=1 F=0  T=0 F=0  if(data->conn)
  d=6   L2303  T=9 F=7  T=0 F=20  if(data->conn->bits.multiplex)
  d=6   L2407  T=7 F=11  T=20 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=6   L2407  T=0 F=11  T=0 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=6   L2413  T=7 F=0  T=20 F=0  if(!ret)
  d=6   L2414  T=0 F=7  T=0 F=20  retry = (newurl)?TRUE:FALSE;
  d=6   L2418  T=0 F=7  T=0 F=20  if(retry) {
  d=6   L2425  T=9 F=2  T=0 F=0  else if((CURLE_HTTP2_STREAM == result) &&
  d=6   L2426  T=0 F=9  T=0 F=0  Curl_h2_http_1_1_error(data)) {
  d=6   L2448  T=9 F=9  T=0 F=20  if(result) {
  d=6   L2457  T=9 F=0  T=0 F=0  if(!(data->conn->handler->flags & PROTOPT_DUAL) &&
  d=6   L2458  T=0 F=9  T=0 F=0  result != CURLE_HTTP2_STREAM)
  d=6   L2464  T=7 F=2  T=20 F=0  else if(done) {
  d=6   L2471  T=0 F=7  T=0 F=20  if(data->req.newurl || retry) {
  d=6   L2471  T=0 F=7  T=0 F=20  if(data->req.newurl || retry) {
  d=6   L2497  T=0 F=7  T=0 F=20  if(data->req.location) {
  d=6   L2509  T=7 F=0  T=20 F=0  if(!result) {
  d=6   L2515  T=0 F=2  T=0 F=0  else if(comeback) {
  d=6   L2529  T=7 F=0  T=20 F=0  if(data->conn) {
  d=6   L2532  T=0 F=7  T=0 F=20  if(data->conn->bits.multiplex)
  d=6   L2540  T=7 F=0  T=20 F=0  if(!result)
  d=6   L2545  T=0 F=7  T=0 F=20  if(data->state.wildcardmatch) {
  d=6   L2562  T=1 F=126  T=0 F=160  case MSTATE_MSGSENT:
  d=6   L2587  T=10 F=109  T=0 F=140  if(result) {
  d=6   L2599  T=0 F=10  T=0 F=0  if(data->conn) {
  d=6   L2617  T=0 F=10  T=0 F=0  else if(data->mstate == MSTATE_CONNECT) {
  d=6   L2657  T=1 F=18  T=0 F=20  } while((rc == CURLM_CALL_MULTI_PERFORM) || multi_ischang...
--- d=2  curl_multi_remove_handle  (/src/curl/lib/multi.c:765-934) ---
  d=2   L 870  T=17 F=0  T=0 F=20  if(data->state.lastconnect_id != -1) {
--- d=1  multi.c:multi_done  (/src/curl/lib/multi.c:612-746) ---
  d=1   L 654  T=7 F=10  T=0 F=20  if(!result && rc)
  d=1   L 654  T=0 F=7  T=0 F=0  if(!result && rc)
  d=1   L 711  T=0 F=17  T=20 F=0  ) || conn->bits.close  <-- BLOCKER
  d=1   L 712  T=9 F=8  T=0 F=0  || (premature && !(conn->handler->flags & PROTOPT_STREAM)...
  d=1   L 712  T=0 F=9  T=0 F=0  || (premature && !(conn->handler->flags & PROTOPT_STREAM)...
  d=1   L 722  T=0 F=17  T=0 F=0  conn->bits.socksproxy ?
  d=1   L 724  T=0 F=17  T=0 F=0  conn->bits.httpproxy ? conn->http_proxy.host.dispname :
  d=1   L 726  T=17 F=0  T=0 F=0  conn->bits.conn_to_host ? conn->conn_to_host.dispname :
  d=1   L 735  T=17 F=0  T=0 F=0  if(Curl_conncache_return_conn(data, conn)) {

[off-chain: 32 additional divergent branches across 9 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
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
Seed 5 (id=4cfa911e483390cc, size=112 bytes, fuzzer=cmplog, trial=1, discovered_at=13209s, mutation_op=ByteDecMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2f 5b 32 00   ......pop.://[2.
  0010: 00 30 28 28 00 1e 3a 39 9c 30 31 72 38 35 30 00   .0((..:9.01r850.
  0020: 02 00 00 00 48 48 54 54 50 2f 25 6d 65 61 06 24   ....HHTTP/%mea.$
  0030: 65 63 8e 65 25 72 87 0d 0a 43 6f 6e 6e 65 63 74   ec.e%r...Connect

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
   0x0005  19(.)x17                            19(.)x10 43(C)x3 2e(.)x2 44(D)x1 +4u  PARTIAL
   0x0006  70(p)x16 fd(.)x1                    25(%)x4 64(d)x3 2e(.)x3 43(C)x2 +7u  PARTIAL
   0x0007  6f(o)x9 bb(.)x5 50(P)x2 2e(.)x1     55(U)x2 41(A)x2 25(%)x2 2e(.)x2 +12u  PARTIAL
   0x0009  33(3)x8 00(.)x5 ad(.)x2 2e(.)x2     25(%)x4 2b(+)x2 46(F)x2 2e(.)x1 +11u  PARTIAL
   0x000c  2f(/)x14 39(9)x2 4a(J)x1            2e(.)x5 25(%)x4 41(A)x2 45(E)x2 +7u  DIFFER
   0x0017  39(9)x15 40(@)x2                    41(A)x3 2e(.)x3 25(%)x3 00(.)x1 +10u  DIFFER
   0x0019  30(0)x14 4b(K)x2 ff(.)x1            25(%)x3 2b(+)x3 00(.)x2 40(@)x2 +10u  PARTIAL
   0x001a  31(1)x14 d0(.)x2 ff(.)x1            25(%)x5 41(A)x3 f9(.)x1 2b(+)x1 +10u  DIFFER
   0x001c  38(8)x15 3f(?)x2                    2e(.)x3 45(E)x3 2b(+)x2 ff(.)x1 +11u  DIFFER
   0x001d  35(5)x15 32(2)x2                    2e(.)x2 64(d)x2 2d(-)x2 ff(.)x1 +13u  DIFFER
   0x001e  30(0)x15 37(7)x2                    25(%)x4 44(D)x2 49(I)x1 65(e)x1 +12u  DIFFER
   0x001f  00(.)x17                            25(%)x3 2e(.)x3 41(A)x2 62(b)x1 +11u  DIFFER
   0x0021  00(.)x17                            25(%)x3 2d(-)x3 05(.)x1 69(i)x1 +11u  PARTIAL
   0x0022  00(.)x17                            44(D)x3 2e(.)x2 61(a)x1 74(t)x1 +10u  PARTIAL
   0x0023  00(.)x17                            2e(.)x2 25(%)x2 d6(.)x1 bb(.)x1 +6u  DIFFER
   0x0024  47(G)x16 48(H)x1                    50(P)x2 42(B)x1 9e(.)x1 2e(.)x1 +5u  DIFFER
   0x0025  48(H)x13 6b(k)x2 68(h)x1 69(i)x1    25(%)x3 2e(.)x3 41(A)x2 64(d)x1 +1u  DIFFER
   0x0033  2f(/)x6 72(r)x4 04(.)x3 65(e)x1 +3u  25(%)x3 2e(.)x2 41(A)x2 bd(.)x1     DIFFER
   0x0036  2e(.)x6 65(e)x3 0a(.)x3 87(.)x1 +4u  25(%)x4 4e(N)x1 45(E)x1 44(D)x1     PARTIAL
   0x0038  2f(/)x6 72(r)x4 3d(=)x3 0a(.)x2 +2u  25(%)x3 42(B)x2 80(.)x1 64(d)x1     DIFFER
   0x0039  2f(/)x6 54(T)x4 61(a)x3 72(r)x2 +2u  25(%)x3 62(b)x2                     DIFFER
   0x003a  2f(/)x6 6f(o)x3 6e(n)x3 72(r)x2 +3u  25(%)x2 9e(.)x1 42(B)x1 65(e)x1     PARTIAL
   0x003b  25(%)x6 3a(:)x4 37(7)x2 6e(n)x1 +4u  25(%)x2 66(f)x1 42(B)x1 65(e)x1     PARTIAL
   0x003c  74(t)x6 20( )x4 66(f)x3 6e(n)x1 +3u  64(d)x2 26(&)x1 52(R)x1 25(%)x1     DIFFER
   0x003d  65(e)x10 66(f)x4 f3(.)x2 1e(.)x1    25(%)x1 66(f)x1 bd(.)x1 64(d)x1 +1u  PARTIAL
   0x003e  6e(n)x6 72(r)x3 61(a)x2 f3(.)x2 +4u  40(@)x2 25(%)x2 79(y)x1             PARTIAL
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
  prompts_b/curl_298.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 298,
  "target": "curl",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S), cmplog>naive (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 298 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 298 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 298 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).