==== BLOCKER ====
Target: curl
Branch ID: 297
Location: /src/curl/lib/multi.c:654:8
Enclosing function: multi.c:multi_done
Source line:     if(!result && rc)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            3        7          0  REFERENCE
cmplog                          10        0          0  REFERENCE
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        3        7          0  REFERENCE
naive_ngram4                     2        8          0  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             8        2          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.10h  loser=22.30h
  avg hitcount on branch: winner=1674  loser=1
  prob_div=0.80  dur_div=22.20h  hit_div=1673
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/297/{W,L}/branch_coverage_show.txt

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
[B]   654      if(!result && rc) <-- BLOCKER
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
[B]   711       ) || conn->bits.close
[B]   712         || (premature && !(conn->handler->flags & PROTOPT_STREAM))) {
[B]   713      connclose(conn, "disconnecting");
[B]   714      Curl_conncache_remove_conn(data, conn, FALSE);
[B]   715      CONNCACHE_UNLOCK(data);
[B]   716      Curl_disconnect(data, conn, premature);
[B]   717    }
[ ]   718    else {
[ ]   719      char buffer[256];
[ ]   720      const char *host =
[ ]   721  #ifndef CURL_DISABLE_PROXY
[ ]   722        conn->bits.socksproxy ?
[ ]   723        conn->socks_proxy.host.dispname :
[ ]   724        conn->bits.httpproxy ? conn->http_proxy.host.dispname :
[ ]   725  #endif
[ ]   726        conn->bits.conn_to_host ? conn->conn_to_host.dispname :
[ ]   727        conn->host.dispname;
[ ]   728      /* create string before returning the connection */
[ ]   729      long connection_id = conn->connection_id;
[ ]   730      msnprintf(buffer, sizeof(buffer),
[ ]   731                "Connection #%ld to host %s left intact",
[ ]   732                connection_id, host);
[ ]   733      /* the connection is no longer in use by this transfer */
[ ]   734      CONNCACHE_UNLOCK(data);
[ ]   735      if(Curl_conncache_return_conn(data, conn)) {
[ ]   736        /* remember the most recently used connection */
[ ]   737        data->state.lastconnect_id = connection_id;
[ ]   738        infof(data, "%s", buffer);
[ ]   739      }
[ ]   740      else
[ ]   741        data->state.lastconnect_id = -1;
[ ]   742    }
[ ]   743  
[B]   744    Curl_safefree(data->state.buffer);
[B]   745    return result;
[B]   746  }

--- Caller (1 hop): multi.c:multi_runsingle (/src/curl/lib/multi.c:1811-2661, calls multi.c:multi_done at line 2537) (±10 around call site) ---
[B]  2527        rc = CURLM_CALL_MULTI_PERFORM;
[ ]  2528  
[B]  2529        if(data->conn) {
[B]  2530          CURLcode res;
[ ]  2531  
[B]  2532          if(data->conn->bits.multiplex)
[ ]  2533            /* Check if we can move pending requests to connection */
[ ]  2534            process_pending_handles(multi); /* multiplexing */
[ ]  2535  
[ ]  2536          /* post-transfer command */
[B]  2537          res = multi_done(data, result, FALSE); <-- CALL
[ ]  2538  
[ ]  2539          /* allow a previously set error code take precedence */
[B]  2540          if(!result)
[B]  2541            result = res;
[B]  2542        }
[ ]  2543  
[B]  2544  #ifndef CURL_DISABLE_FTP
[B]  2545        if(data->state.wildcardmatch) {
[ ]  2546          if(data->wildcard.state != CURLWC_DONE) {
[ ]  2547            /* if a wildcard is set and we are not ending -> lets start again

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
      10         0  curl_multi_fdset  (/src/curl/lib/multi.c:1099-1154)
      10         0  multi.c:add_next_timeout  (/src/curl/lib/multi.c:3055-3094)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716) ---
  d=7   L2674  T=0 F=20  T=0 F=10  if(multi->in_callback)
  d=7   L2678  T=20 F=20  T=10 F=10  while(data) {
  d=7   L2686  T=0 F=20  T=0 F=10  if(result)
  d=7   L2704  T=10 F=20  T=0 F=10  if(t)
  d=7   L2708  T=10 F=20  T=0 F=10  } while(t);
  d=7   L2712  T=20 F=0  T=10 F=0  if(CURLM_OK >= returncode)
--- d=6  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661) ---
  d=6   L1827  T=0 F=20  T=0 F=10  if(multi->dead) {
  d=6   L2378  T=0 F=20  T=0 F=10  if(data->set.max_send_speed)
  d=6   L2387  T=0 F=20  T=0 F=10  if(data->set.max_recv_speed)
  d=6   L2394  T=0 F=20  T=0 F=10  if(send_timeout_ms || recv_timeout_ms) {
  d=6   L2394  T=0 F=20  T=0 F=10  if(send_timeout_ms || recv_timeout_ms) {
  d=6   L2407  T=10 F=10  T=10 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=6   L2407  T=0 F=10  T=0 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=6   L2425  T=0 F=10  T=0 F=0  else if((CURLE_HTTP2_STREAM == result) &&
  d=6   L2448  T=0 F=20  T=0 F=10  if(result) {
  d=6   L2464  T=10 F=10  T=10 F=0  else if(done) {
  d=6   L2515  T=0 F=10  T=0 F=0  else if(comeback) {
  d=6   L2657  T=0 F=20  T=0 F=10  } while((rc == CURLM_CALL_MULTI_PERFORM) || multi_ischang...
--- d=1  multi.c:multi_done  (/src/curl/lib/multi.c:612-746) ---
  d=1   L 654  T=10 F=0  T=0 F=10  if(!result && rc)  <-- BLOCKER
  d=1   L 654  T=0 F=10  T=0 F=0  if(!result && rc)  <-- BLOCKER

[off-chain: 24 additional divergent branches across 4 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
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
Seed 3 (id=01ae7bb3c2243a5f, size=110 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=35100s, mutation_op=ByteNegMutator,CrossoverReplaceMutator):
  0000: 00 01 00 00 00 19 9a 9a 70 33 cb 2f 3a 3a 00 10   ........p3./::..
  0010: 3a 00 3a 3a 4d 3a ff 39 2f 30 31 00 e8 03 30 00   :.::M:.9/01...0.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 98 a1 38 25   ....GHTTP/ m..8%
  0030: 6d 20 54 68 65 51 64 20 0a 54 72 61 6e 53 66 65   m TheQd .TranSfe
Seed 4 (id=00b60eeef7768f83, size=112 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=35116s, mutation_op=QwordAddMutator,BytesDeleteMutator,ByteNegMutator,BytesDeleteMutator,BytesInsertCopyMutator,TokenReplace):
  0000: 00 01 00 00 00 19 49 4d 00 50 3a 2f 2f 3f 32 37   ......IM.P://?27
  0010: 00 30 2e 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   .0.0.1:9001/850.
  0020: 02 00 00 00 47 48 54 54 50 2f 48 6d 65 40 6c 6f   ....GHTTP/Hme@lo
  0030: 6d 65 77 68 65 72 65 0d 25 54 6f 3a 11 66 61 6b   mewhere.%To:.fak
Seed 5 (id=00d9cc92bca9adac, size=131 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=47480s, mutation_op=BytesSwapMutator,CrossoverInsertMutator,WordAddMutator):
  0000: 00 01 00 00 00 19 9a 9a 70 cd cb 2f 3a 3a 00 10   ........p../::..
  0010: 3a 32 3a 3a 4e 3a ff 39 30 30 00 ad e8 03 30 00   :2::N:.900....0.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 98 a1 33 25   ....GHTTP/ m..3%
  0030: 6d 3f 54 68 65 72 65 02 13 54 72 61 6e 53 66 65   m?There..TranSfe

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
Seed 3 (id=001607afc7f08ce7, size=74 bytes, fuzzer=value_profile, trial=1, discovered_at=3913s, mutation_op=BytesCopyMutator):
  0000: 00 01 00 00 00 44 64 55 43 db b5 25 45 66 25 66   .....DdUC..%Ef%f
  0010: 42 62 9e 62 9e 44 64 55 43 db b5 25 45 66 25 66   Bb.b.DdUC..%Ef%f
  0020: 42 62 9e 62 9e 43 41 27 db 31 25 25 25 25 26 55   Bb.b.CA'.1%%%%&U
  0030: 43 db b5 25 45 66 25 65 42 62 9e 66 52 66 25 65   C..%Ef%eBb.fRf%e
Seed 4 (id=00412fff2cf16b82, size=34 bytes, fuzzer=value_profile, trial=1, discovered_at=3918s, mutation_op=BitFlipMutator):
  0000: 00 01 00 00 00 19 71 6e 2f 2f 2f 2e 2e 2f 2e 2f   ......qn///.././
  0010: 2e 2f 2f 2f 2f 2f 2f 2f 2e 2f 21 2e 2f 75 75 75   .///////./!./uuu
  0020: ff 35                                             .5
Seed 5 (id=00224975860e7d7e, size=36 bytes, fuzzer=value_profile, trial=1, discovered_at=4107s, mutation_op=DwordAddMutator,QwordAddMutator,CrossoverReplaceMutator):
  0000: 00 01 00 00 00 19 2e 2d 2b 47 2b 2b 2b 2e 4e 51   .......-+G+++.NQ
  0010: 37 2b 2b 2d 2b 2e 4e 41 59 2b 38 2d 2b 2e 46 25   7++-+.NAY+8-+.F%
  0020: 21 00 00 8d                                       !...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x10                            19(.)x3 43(C)x3 2e(.)x2 44(D)x1 +1u  PARTIAL
   0x0006  9a(.)x6 70(p)x3 49(I)x1             64(d)x3 2e(.)x3 30(0)x1 71(q)x1 +2u  DIFFER
   0x0007  9a(.)x6 6f(o)x3 4d(M)x1             55(U)x2 2e(.)x2 49(I)x1 6e(n)x1 +4u  DIFFER
   0x0008  70(p)x9 00(.)x1                     2e(.)x3 43(C)x2 2f(/)x1 2b(+)x1 +3u  DIFFER
   0x0009  33(3)x4 cd(.)x4 71(q)x1 50(P)x1     25(%)x2 2b(+)x2 2e(.)x1 db(.)x1 +4u  DIFFER
   0x000a  cb(.)x6 4b(K)x3 3a(:)x1             25(%)x2 2e(.)x2 51(Q)x1 b5(.)x1 +4u  DIFFER
   0x000b  2f(/)x10                            25(%)x3 2e(.)x2 2b(+)x1 2d(-)x1 +3u  DIFFER
   0x000c  3a(:)x8 2f(/)x1 00(.)x1             2e(.)x3 25(%)x2 47(G)x1 45(E)x1 +3u  DIFFER
   0x000d  3a(:)x9 3f(?)x1                     2e(.)x3 48(H)x1 21(!)x1 66(f)x1 +4u  DIFFER
   0x000e  00(.)x7 3a(:)x2 32(2)x1             25(%)x5 2e(.)x4 4e(N)x1             DIFFER
   0x000f  10(.)x7 3a(:)x2 37(7)x1             2e(.)x2 2b(+)x1 65(e)x1 66(f)x1 +5u  DIFFER
   0x0010  3a(:)x9 00(.)x1                     2e(.)x3 42(B)x2 80(.)x1 26(&)x1 +3u  DIFFER
   0x0012  3a(:)x8 2e(.)x1 c6(.)x1             21(!)x1 65(e)x1 9e(.)x1 2f(/)x1 +6u  PARTIAL
   0x0013  3a(:)x9 30(0)x1                     62(b)x2 47(G)x1 24($)x1 2f(/)x1 +5u  DIFFER
   0x0014  4e(N)x5 3a(:)x3 4d(M)x1 2e(.)x1     25(%)x2 2e(.)x2 47(G)x1 9e(.)x1 +4u  PARTIAL
   0x0015  3a(:)x9 31(1)x1                     46(F)x2 25(%)x2 64(d)x1 44(D)x1 +4u  DIFFER
   0x0016  ff(.)x6 3a(:)x3 3b(;)x1             64(d)x2 0f(.)x1 45(E)x1 2f(/)x1 +5u  DIFFER
   0x0017  39(9)x10                            2e(.)x2 00(.)x1 72(r)x1 55(U)x1 +5u  DIFFER
   0x0018  30(0)x8 2f(/)x1 34(4)x1             2e(.)x3 00(.)x1 46(F)x1 43(C)x1 +4u  DIFFER
   0x0019  30(0)x8 14(.)x1 cf(.)x1             25(%)x2 2b(+)x2 00(.)x1 db(.)x1 +4u  DIFFER
   0x001a  31(1)x6 00(.)x4                     41(A)x2 f9(.)x1 b5(.)x1 21(!)x1 +5u  DIFFER
   0x001c  e8(.)x6 38(8)x3 21(!)x1             2e(.)x2 ff(.)x1 25(%)x1 45(E)x1 +5u  DIFFER
   0x001d  03(.)x6 35(5)x4                     2e(.)x2 ff(.)x1 31(1)x1 66(f)x1 +5u  DIFFER
   0x001e  30(0)x10                            25(%)x3 49(I)x1 75(u)x1 46(F)x1 +4u  DIFFER
   0x001f  00(.)x10                            25(%)x3 2e(.)x2 62(b)x1 66(f)x1 +3u  DIFFER
   0x0020  02(.)x10                            42(B)x2 2e(.)x2 7e(~)x1 65(e)x1 +4u  DIFFER
   0x0021  00(.)x10                            05(.)x1 25(%)x1 62(b)x1 35(5)x1 +6u  PARTIAL
   0x0022  00(.)x10                            2e(.)x2 61(a)x1 44(D)x1 9e(.)x1 +4u  PARTIAL
   0x0023  00(.)x10                            2e(.)x2 d6(.)x1 62(b)x1 8d(.)x1 +3u  DIFFER
   0x0024  47(G)x10                            42(B)x1 9e(.)x1 2e(.)x1 44(D)x1 +3u  DIFFER
   0x0025  48(H)x10                            2e(.)x2 25(%)x2 64(d)x1 43(C)x1 +1u  DIFFER
   0x0026  54(T)x10                            2e(.)x2 45(E)x1 41(A)x1 42(B)x1 +2u  DIFFER
   0x0027  54(T)x10                            72(r)x1 27(')x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x0028  50(P)x10                            25(%)x3 2e(.)x2 33(3)x1 db(.)x1     DIFFER
   0x0029  2f(/)x10                            25(%)x1 31(1)x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x002a  20( )x7 48(H)x2 98(.)x1             65(e)x1 25(%)x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x002b  6d(m)x10                            25(%)x2 4b(K)x1 2e(.)x1 66(f)x1 +2u  DIFFER
   0x002c  98(.)x5 65(e)x4 0a(.)x1             25(%)x2 2e(.)x2 6e(n)x1 45(E)x1 +1u  PARTIAL
   0x002d  a1(.)x6 40(@)x4                     25(%)x2 2e(.)x2 43(C)x1 bd(.)x1 +1u  DIFFER
   0x002e  33(3)x4 6c(l)x3 38(8)x2 25(%)x1     25(%)x3 2e(.)x2 26(&)x1 64(d)x1     PARTIAL
   ... (16 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
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
  prompts_b/curl_297.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 297,
  "target": "curl",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>value_profile (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 297 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 297 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 297 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).