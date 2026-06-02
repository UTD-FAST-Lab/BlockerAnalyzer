==== BLOCKER ====
Target: curl
Branch ID: 303
Location: /src/curl/lib/multi.c:800:6
Enclosing function: curl_multi_remove_handle
Source line:   if(data->conn &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    2        8          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        2        8          0  REFERENCE
naive_ngram4                     1        9          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         9        1          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=5.20h  loser=22.90h
  avg hitcount on branch: winner=5  loser=1
  prob_div=0.80  dur_div=17.70h  hit_div=5
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002
--- Pair 2: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=9.30h  loser=23.00h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.60  dur_div=13.70h  hit_div=2
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/303/{W,L}/branch_coverage_show.txt

--- Enclosing function: curl_multi_remove_handle (/src/curl/lib/multi.c:765-934) ---
[ ]   763  CURLMcode curl_multi_remove_handle(struct Curl_multi *multi,
[ ]   764                                     struct Curl_easy *data)
[B]   765  {
[B]   766    struct Curl_easy *easy = data;
[B]   767    bool premature;
[B]   768    struct Curl_llist_element *e;
[B]   769    CURLMcode rc;
[ ]   770  
[ ]   771    /* First, make some basic checks that the CURLM handle is a good handle */
[B]   772    if(!GOOD_MULTI_HANDLE(multi))
[ ]   773      return CURLM_BAD_HANDLE;
[ ]   774  
[ ]   775    /* Verify that we got a somewhat good easy handle too */
[B]   776    if(!GOOD_EASY_HANDLE(data))
[ ]   777      return CURLM_BAD_EASY_HANDLE;
[ ]   778  
[ ]   779    /* Prevent users from trying to remove same easy handle more than once */
[B]   780    if(!data->multi)
[ ]   781      return CURLM_OK; /* it is already removed so let's say it is fine! */
[ ]   782  
[ ]   783    /* Prevent users from trying to remove an easy handle from the wrong multi */
[B]   784    if(data->multi != multi)
[ ]   785      return CURLM_BAD_EASY_HANDLE;
[ ]   786  
[B]   787    if(multi->in_callback)
[ ]   788      return CURLM_RECURSIVE_API_CALL;
[ ]   789  
[B]   790    premature = (data->mstate < MSTATE_COMPLETED) ? TRUE : FALSE;
[ ]   791  
[ ]   792    /* If the 'state' is not INIT or COMPLETED, we might need to do something
[ ]   793       nice to put the easy_handle in a good known state when this returns. */
[B]   794    if(premature) {
[ ]   795      /* this handle is "alive" so we need to count down the total number of
[ ]   796         alive connections when this is removed */
[W]   797      multi->num_alive--;
[W]   798    }
[ ]   799  
[B]   800    if(data->conn && <-- BLOCKER
[B]   801       data->mstate > MSTATE_DO &&
[B]   802       data->mstate < MSTATE_COMPLETED) {
[ ]   803      /* Set connection owner so that the DONE function closes it.  We can
[ ]   804         safely do this here since connection is killed. */
[W]   805      streamclose(data->conn, "Removed with partial response");
[W]   806    }
[ ]   807  
[B]   808    if(data->conn) {
[ ]   809      /* multi_done() clears the association between the easy handle and the
[ ]   810         connection.
[ ]   811  
[ ]   812         Note that this ignores the return code simply because there's
[ ]   813         nothing really useful to do with it anyway! */
[W]   814      (void)multi_done(data, data->result, premature);
[W]   815    }
[ ]   816  
[ ]   817    /* The timer must be shut down before data->multi is set to NULL, else the
[ ]   818       timenode will remain in the splay tree after curl_easy_cleanup is
[ ]   819       called. Do it after multi_done() in case that sets another time! */
[B]   820    Curl_expire_clear(data);
[ ]   821  
[B]   822    if(data->connect_queue.ptr)
[ ]   823      /* the handle was in the pending list waiting for an available connection,
[ ]   824         so go ahead and remove it */
[ ]   825      Curl_llist_remove(&multi->pending, &data->connect_queue, NULL);
[ ]   826  
[B]   827    if(data->dns.hostcachetype == HCACHE_MULTI) {
[ ]   828      /* stop using the multi handle's DNS cache, *after* the possible
[ ]   829         multi_done() call above */
[B]   830      data->dns.hostcache = NULL;
[B]   831      data->dns.hostcachetype = HCACHE_NONE;
[B]   832    }
[ ]   833  
[B]   834    Curl_wildcard_dtor(&data->wildcard);
[ ]   835  
[ ]   836    /* destroy the timeout list that is held in the easy handle, do this *after*
[ ]   837       multi_done() as that may actually call Curl_expire that uses this */
[B]   838    Curl_llist_destroy(&data->state.timeoutlist, NULL);
[ ]   839  
[ ]   840    /* change state without using multistate(), only to make singlesocket() do
[ ]   841       what we want */
[B]   842    data->mstate = MSTATE_COMPLETED;
[ ]   843  
[ ]   844    /* This ignores the return code even in case of problems because there's
[ ]   845       nothing more to do about that, here */
[B]   846    (void)singlesocket(multi, easy); /* to let the application know what sockets
[ ]   847                                        that vanish with this handle */
[ ]   848  
[ ]   849    /* Remove the association between the connection and the handle */
[B]   850    Curl_detach_connection(data);
[ ]   851  
[B]   852    if(data->set.connect_only && !data->multi_easy) {
[ ]   853      /* This removes a handle that was part the multi interface that used
[ ]   854         CONNECT_ONLY, that connection is now left alive but since this handle
[ ]   855         has bits.close set nothing can use that transfer anymore and it is
[ ]   856         forbidden from reuse. And this easy handle cannot find the connection
[ ]   857         anymore once removed from the multi handle
[ ]   858  
[ ]   859         Better close the connection here, at once.
[ ]   860      */
[ ]   861      struct connectdata *c;
[ ]   862      curl_socket_t s;
[ ]   863      s = Curl_getconnectinfo(data, &c);
[ ]   864      if((s != CURL_SOCKET_BAD) && c) {
[ ]   865        Curl_conncache_remove_conn(data, c, TRUE);
[ ]   866        Curl_disconnect(data, c, TRUE);
[ ]   867      }
[ ]   868    }
[ ]   869  
[B]   870    if(data->state.lastconnect_id != -1) {
[ ]   871      /* Mark any connect-only connection for closure */
[ ]   872      Curl_conncache_foreach(data, data->state.conn_cache,
[ ]   873                             NULL, close_connect_only);
[ ]   874    }
[ ]   875  
[ ]   876  #ifdef USE_LIBPSL
[ ]   877    /* Remove the PSL association. */
[ ]   878    if(data->psl == &multi->psl)
[ ]   879      data->psl = NULL;
[ ]   880  #endif
[ ]   881  
[ ]   882    /* as this was using a shared connection cache we clear the pointer to that
[ ]   883       since we're not part of that multi handle anymore */
[B]   884    data->state.conn_cache = NULL;
[ ]   885  
[B]   886    data->multi = NULL; /* clear the association to this multi handle */
[ ]   887  
[ ]   888    /* make sure there's no pending message in the queue sent from this easy
[ ]   889       handle */
[ ]   890  
[B]   891    for(e = multi->msglist.head; e; e = e->next) {
[L]   892      struct Curl_message *msg = e->ptr;
[ ]   893  
[L]   894      if(msg->extmsg.easy_handle == easy) {
[L]   895        Curl_llist_remove(&multi->msglist, e, NULL);
[ ]   896        /* there can only be one from this specific handle */
[L]   897        break;
[L]   898      }
[L]   899    }
[ ]   900  
[ ]   901    /* Remove from the pending list if it is there. Otherwise this will
[ ]   902       remain on the pending list forever due to the state change. */
[B]   903    for(e = multi->pending.head; e; e = e->next) {
[ ]   904      struct Curl_easy *curr_data = e->ptr;
[ ]   905  
[ ]   906      if(curr_data == data) {
[ ]   907        Curl_llist_remove(&multi->pending, e, NULL);
[ ]   908        break;
[ ]   909      }
[ ]   910    }
[ ]   911  
[ ]   912    /* make the previous node point to our next */
[B]   913    if(data->prev)
[ ]   914      data->prev->next = data->next;
[B]   915    else
[B]   916      multi->easyp = data->next; /* point to first node */
[ ]   917  
[ ]   918    /* make our next point to our previous node */
[B]   919    if(data->next)
[ ]   920      data->next->prev = data->prev;
[B]   921    else
[B]   922      multi->easylp = data->prev; /* point to last node */
[ ]   923  
[ ]   924    /* NOTE NOTE NOTE
[ ]   925       We do not touch the easy handle here! */
[B]   926    multi->num_easy--; /* one less to care about now */
[ ]   927  
[B]   928    process_pending_handles(multi);
[ ]   929  
[B]   930    rc = Curl_update_timer(multi);
[B]   931    if(rc)
[ ]   932      return rc;
[B]   933    return CURLM_OK;
[B]   934  }

--- No 1-hop callers of curl_multi_remove_handle fired in W (callers index present but none matched) ---

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_close  (/src/curl/lib/url.c:380-497, calls curl_multi_remove_handle at line 399)
hop 3  Curl_free_request_state  (/src/curl/lib/url.c:2250-2260, calls Curl_close at line 2256)
hop 4  Curl_connect  (/src/curl/lib/url.c:4208-4246, calls Curl_free_request_state at line 4215)
hop 5  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_connect at line 1905)
hop 6  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 6  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)
hop 7  curl_multi_socket  (/src/curl/lib/multi.c:3288-3296, calls multi.c:multi_socket at line 3292)
hop 7  curl_multi_socket_action  (/src/curl/lib/multi.c:3300-3308, calls multi.c:multi_socket at line 3304)
hop 7  curl_multi_strerror  (/src/curl/lib/strerror.c:364-420, calls curl_multi_perform at line 368)
hop 8  easy.c:wait_or_timeout  (/src/curl/lib/easy.c:541-628, calls curl_multi_socket_action at line 582)
hop 8  curl_multi_add_handle  (/src/curl/lib/multi.c:464-590, calls curl_multi_socket at line 509)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      28       158  multi.c:mstate  (/src/curl/lib/multi.c:153-209)
      20       120  Curl_detach_connection  (/src/curl/lib/multi.c:949-957)
      12        80  Curl_expire_clear  (/src/curl/lib/multi.c:3579-3610)
      16        80  Curl_free_idnconverted_hostname  (/src/curl/lib/url.c:1665-1679)
      12        60  url.c:up_free  (/src/curl/lib/url.c:358-370)
      12        60  Curl_free_request_state  (/src/curl/lib/url.c:2250-2260)
      16        59  Curl_builtin_scheme  (/src/curl/lib/url.c:1846-1858)
      12        53  multi.c:multi_deltimeout  (/src/curl/lib/multi.c:3436-3447)
      12        53  multi.c:multi_addtimeout  (/src/curl/lib/multi.c:3460-3490)
      12        53  Curl_expire  (/src/curl/lib/multi.c:3504-3559)
      20        60  Curl_update_timer  (/src/curl/lib/multi.c:3383-3427)
       8        40  curl_easy_init  (/src/curl/lib/easy.c:341-367)
       8        40  multi.c:process_pending_handles  (/src/curl/lib/multi.c:3659-3677)
       8        40  Curl_freeset  (/src/curl/lib/url.c:329-354)
       8        40  Curl_close  (/src/curl/lib/url.c:380-497)
... (58 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=8  curl_multi_add_handle  (/src/curl/lib/multi.c:464-590) ---
  d=8   L 476  T=0 F=4  T=0 F=20  if(data->multi)
  d=8   L 479  T=0 F=4  T=0 F=20  if(multi->in_callback)
  d=8   L 482  T=0 F=4  T=0 F=20  if(multi->dead) {
  d=8   L 500  T=0 F=4  T=0 F=20  if(data->set.errorbuffer)
  d=8   L 528  T=0 F=4  T=0 F=20  if(rc)
  d=8   L 536  T=4 F=0  T=20 F=0  if(!data->dns.hostcache ||
  d=8   L 543  T=0 F=4  T=0 F=20  if(data->share && (data->share->specifier & (1<< CURL_LOC...
  d=8   L 559  T=0 F=4  T=0 F=20  if(multi->easyp) {
--- d=6  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716) ---
  d=6   L2704  T=4 F=12  T=0 F=20  if(t)
  d=6   L2708  T=4 F=12  T=0 F=20  } while(t);
--- d=5  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661) ---
  d=5   L1842  T=0 F=36  T=0 F=118  if(multi_ischanged(multi, TRUE)) {
  d=5   L1847  T=28 F=8  T=78 F=40  if(data->mstate > MSTATE_CONNECT &&
  d=5   L1848  T=28 F=0  T=78 F=0  data->mstate < MSTATE_COMPLETED) {
  d=5   L1851  T=0 F=28  T=0 F=78  if(!data->conn)
  d=5   L1855  T=28 F=8  T=78 F=40  if(data->conn &&
  d=5   L1856  T=28 F=0  T=78 F=0  (data->mstate >= MSTATE_CONNECT) &&
  d=5   L1857  T=28 F=0  T=78 F=0  (data->mstate < MSTATE_COMPLETED)) {
  d=5   L1867  T=0 F=28  T=0 F=78  if(multi_handle_timeout(data, nowp, &stream_error, &resul...
  d=5   L1874  T=4 F=32  T=20 F=98  case MSTATE_INIT:
  d=5   L1878  T=4 F=0  T=20 F=0  if(!result) {
  d=5   L1886  T=0 F=36  T=0 F=118  case MSTATE_PENDING:
  d=5   L1891  T=4 F=32  T=20 F=98  case MSTATE_CONNECT:
  d=5   L1895  T=0 F=4  T=0 F=20  if(result)
  d=5   L1899  T=4 F=0  T=20 F=0  if(data->set.timeout)
  d=5   L1902  T=0 F=4  T=0 F=20  if(data->set.connecttimeout)
  d=5   L1906  T=0 F=4  T=0 F=20  if(CURLE_NO_CONNECTION_AVAILABLE == result) {
  d=5   L1917  T=0 F=4  T=0 F=20  else if(data->state.previouslypending) {
  d=5   L1923  T=4 F=0  T=13 F=7  if(!result) {
  d=5   L1924  T=0 F=4  T=0 F=13  if(async)
  d=5   L1933  T=0 F=4  T=0 F=13  if(protocol_connected)
  d=5   L1937  T=0 F=4  T=0 F=13  if(Curl_connect_ongoing(data->conn))
  d=5   L1947  T=0 F=36  T=0 F=118  case MSTATE_RESOLVING:
  d=5   L2024  T=0 F=36  T=0 F=118  case MSTATE_TUNNELING:
  d=5   L2055  T=4 F=32  T=13 F=105  case MSTATE_CONNECTING:
  d=5   L2059  T=4 F=0  T=13 F=0  if(connected && !result) {
  d=5   L2059  T=4 F=0  T=13 F=0  if(connected && !result) {
  d=5   L2063  T=0 F=4  T=0 F=13  (data->conn->http_proxy.proxytype == CURLPROXY_HTTPS &&
  d=5   L2066  T=0 F=4  T=0 F=13  Curl_connect_ongoing(data->conn)) {
  d=5   L2089  T=4 F=32  T=13 F=105  case MSTATE_PROTOCONNECT:
  d=5   L2091  T=0 F=4  T=0 F=13  if(!result && !protocol_connected)
  d=5   L2091  T=4 F=0  T=13 F=0  if(!result && !protocol_connected)
  d=5   L2094  T=4 F=0  T=13 F=0  else if(!result) {
  d=5   L2107  T=0 F=36  T=0 F=118  case MSTATE_PROTOCONNECTING:
  d=5   L2123  T=4 F=32  T=13 F=105  case MSTATE_DO:
  d=5   L2124  T=0 F=4  T=0 F=13  if(data->set.fprereq) {
  d=5   L2146  T=0 F=4  T=0 F=13  if(data->set.connect_only == 1) {
  d=5   L2159  T=4 F=0  T=13 F=0  if(!result) {
  d=5   L2160  T=0 F=4  T=0 F=13  if(!dophase_done) {
  d=5   L2184  T=0 F=4  T=0 F=13  else if(data->conn->bits.do_more) {
  d=5   L2254  T=0 F=36  T=0 F=118  case MSTATE_DOING:
  d=5   L2274  T=0 F=36  T=0 F=118  case MSTATE_DOING_MORE:
  d=5   L2301  T=4 F=32  T=13 F=105  case MSTATE_DID:
  d=5   L2303  T=0 F=4  T=0 F=13  if(data->conn->bits.multiplex)
  d=5   L2309  T=4 F=0  T=13 F=0  if((data->conn->sockfd != CURL_SOCKET_BAD) ||
  d=5   L2324  T=0 F=36  T=0 F=118  case MSTATE_RATELIMITING: /* limit-rate exceeded in eithe...
  d=5   L2370  T=12 F=24  T=13 F=105  case MSTATE_PERFORMING:
  d=5   L2407  T=0 F=12  T=13 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=5   L2407  T=0 F=12  T=0 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=5   L2413  T=0 F=0  T=13 F=0  if(!ret)
  d=5   L2414  T=0 F=0  T=0 F=13  retry = (newurl)?TRUE:FALSE;
  d=5   L2418  T=0 F=0  T=0 F=13  if(retry) {
  d=5   L2425  T=0 F=12  T=0 F=0  else if((CURLE_HTTP2_STREAM == result) &&
  d=5   L2464  T=0 F=12  T=13 F=0  else if(done) {
  d=5   L2471  T=0 F=0  T=0 F=13  if(data->req.newurl || retry) {
  d=5   L2471  T=0 F=0  T=0 F=13  if(data->req.newurl || retry) {
  d=5   L2497  T=0 F=0  T=0 F=13  if(data->req.location) {
  d=5   L2509  T=0 F=0  T=13 F=0  if(!result) {
  d=5   L2515  T=0 F=12  T=0 F=0  else if(comeback) {
  d=5   L2525  T=0 F=36  T=13 F=105  case MSTATE_DONE:
  d=5   L2529  T=0 F=0  T=13 F=0  if(data->conn) {
  d=5   L2532  T=0 F=0  T=0 F=13  if(data->conn->bits.multiplex)
  d=5   L2540  T=0 F=0  T=13 F=0  if(!result)
  d=5   L2545  T=0 F=0  T=0 F=13  if(data->state.wildcardmatch) {
  d=5   L2559  T=0 F=36  T=0 F=118  case MSTATE_COMPLETED:
  d=5   L2562  T=0 F=36  T=0 F=118  case MSTATE_MSGSENT:
  d=5   L2566  T=0 F=36  T=0 F=118  default:
  d=5   L2570  T=32 F=4  T=78 F=40  if(data->conn &&
  d=5   L2571  T=32 F=0  T=78 F=0  data->mstate >= MSTATE_CONNECT &&
  d=5   L2572  T=8 F=24  T=26 F=52  data->mstate < MSTATE_DO &&
  d=5   L2573  T=0 F=8  T=0 F=26  rc != CURLM_CALL_MULTI_PERFORM &&
  d=5   L2586  T=36 F=0  T=105 F=13  if(data->mstate < MSTATE_COMPLETED) {
  d=5   L2587  T=0 F=36  T=7 F=98  if(result) {
  d=5   L2599  T=0 F=0  T=0 F=7  if(data->conn) {
  d=5   L2617  T=0 F=0  T=7 F=0  else if(data->mstate == MSTATE_CONNECT) {
  d=5   L2626  T=0 F=32  T=0 F=78  else if(data->conn && Curl_pgrsUpdate(data)) {
  d=5   L2626  T=32 F=4  T=78 F=20  else if(data->conn && Curl_pgrsUpdate(data)) {
  d=5   L2639  T=0 F=36  T=20 F=98  if(MSTATE_COMPLETED == data->mstate) {
  d=5   L2640  T=0 F=0  T=0 F=20  if(data->set.fmultidone) {
  d=5   L2657  T=24 F=12  T=98 F=20  } while((rc == CURLM_CALL_MULTI_PERFORM) || multi_ischang...
--- d=4  Curl_connect  (/src/curl/lib/url.c:4208-4246) ---
  d=4   L4222  T=4 F=0  T=13 F=7  if(!result) {
  d=4   L4223  T=0 F=4  T=0 F=13  if(CONN_INUSE(conn) > 1)
  d=4   L4226  T=4 F=0  T=13 F=0  else if(!*asyncp) {
  d=4   L4234  T=0 F=4  T=0 F=20  if(result == CURLE_NO_CONNECTION_AVAILABLE) {
  d=4   L4237  T=0 F=4  T=7 F=13  else if(result && conn) {
  d=4   L4237  T=0 F=0  T=7 F=0  else if(result && conn) {
--- d=3  Curl_free_request_state  (/src/curl/lib/url.c:2250-2260) ---
  d=3   L2255  T=0 F=12  T=0 F=60  if(data->req.doh) {
--- d=2  Curl_close  (/src/curl/lib/url.c:380-497) ---
  d=2   L 384  T=0 F=8  T=0 F=40  if(!datap || !*datap)
  d=2   L 384  T=0 F=8  T=0 F=40  if(!datap || !*datap)
  d=2   L 396  T=0 F=8  T=0 F=40  if(m)
  d=2   L 401  T=0 F=8  T=0 F=40  if(data->multi_easy) {
  d=2   L 417  T=0 F=8  T=0 F=40  if(data->state.rangestringalloc)
  d=2   L 433  T=0 F=8  T=0 F=40  if(data->state.referer_alloc) {
  d=2   L 461  T=0 F=8  T=0 F=40  if(data->share) {
  d=2   L 483  T=0 F=8  T=0 F=40  if(data->req.doh) {
--- d=1  curl_multi_remove_handle  (/src/curl/lib/multi.c:765-934) ---
  d=1   L 780  T=0 F=4  T=0 F=20  if(!data->multi)
  d=1   L 784  T=0 F=4  T=0 F=20  if(data->multi != multi)
  d=1   L 787  T=0 F=4  T=0 F=20  if(multi->in_callback)
  d=1   L 790  T=4 F=0  T=0 F=20  premature = (data->mstate < MSTATE_COMPLETED) ? TRUE : FA...
  d=1   L 794  T=4 F=0  T=0 F=20  if(premature) {
  d=1   L 800  T=4 F=0  T=0 F=20  if(data->conn &&  <-- BLOCKER
  d=1   L 801  T=4 F=0  T=0 F=0  data->mstate > MSTATE_DO &&
  d=1   L 802  T=4 F=0  T=0 F=0  data->mstate < MSTATE_COMPLETED) {
  d=1   L 808  T=4 F=0  T=0 F=20  if(data->conn) {
  d=1   L 822  T=0 F=4  T=0 F=20  if(data->connect_queue.ptr)
  d=1   L 827  T=4 F=0  T=20 F=0  if(data->dns.hostcachetype == HCACHE_MULTI) {
  d=1   L 852  T=0 F=4  T=0 F=20  if(data->set.connect_only && !data->multi_easy) {
  d=1   L 870  T=0 F=4  T=0 F=20  if(data->state.lastconnect_id != -1) {
  d=1   L 891  T=0 F=4  T=20 F=0  for(e = multi->msglist.head; e; e = e->next) {
  d=1   L 894  T=0 F=0  T=20 F=0  if(msg->extmsg.easy_handle == easy) {
  d=1   L 903  T=0 F=4  T=0 F=20  for(e = multi->pending.head; e; e = e->next) {
  d=1   L 913  T=0 F=4  T=0 F=20  if(data->prev)
  d=1   L 919  T=0 F=4  T=0 F=20  if(data->next)
  d=1   L 931  T=0 F=4  T=0 F=20  if(rc)

[off-chain: 327 additional divergent branches across 64 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=5d9ce7f391be0a62, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=7349s, mutation_op=BytesDeleteMutator,BitFlipMutator,TokenReplace,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 25 3a 3a 3a   ......pop3K/%:::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 00 ad 38 35 30 00   :::::::900..850.
  0020: 11 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 72 65 0d 0a 54 72 61 6e 32 66 65   mewhere..Tran2fe
Seed 2 (id=faf6b58d07527f1a, size=140 bytes, fuzzer=cmplog, trial=2, discovered_at=32307s, mutation_op=WordInterestingMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 26 2f 2f 70 4d 37   ......pop3&//pM7
  0010: 2e ff 2e 30 2e 31 3a 39 30 30 31 3f 38 35 30 00   ...0.1:9001?850.
  0020: 12 00 00 00 47 00 72 00 6d 3a 20 6d 65 40 37 6f   ....G.r.m: me@7o
  0030: 6d 65 77 68 38 3d 65 00 00 54 00 3a 20 66 61 6b   mewh8=e..T.: fak
Seed 3 (id=7ed01751fe602efb, size=140 bytes, fuzzer=cmplog, trial=2, discovered_at=38842s, mutation_op=ByteIncMutator,QwordAddMutator,TokenReplace):
  0000: 00 01 00 00 00 19 70 6f 70 33 26 2f 2f 70 4d 37   ......pop3&//pM7
  0010: 2e ff 2e 30 2e 31 3a 39 30 30 31 3f 38 35 30 00   ...0.1:9001?850.
  0020: 12 00 00 00 47 00 72 00 6d 3a 20 6d 65 40 37 6f   ....G.r.m: me@7o
  0030: 6d 65 77 68 38 3d 65 00 00 54 00 3a 20 66 61 6b   mewh8=e..T.: fak
Seed 4 (id=be54c16922eb9ce7, size=140 bytes, fuzzer=cmplog, trial=2, discovered_at=60490s, mutation_op=BytesSetMutator,BytesCopyMutator,WordInterestingMutator,DwordInterestingMutator):
  0000: 00 01 00 00 00 19 70 6f 64 00 00 00 2f 70 4d 37   ......pod.../pM7
  0010: 2e ff 2e 30 2e 31 3a 39 30 30 31 3f 38 35 30 00   ...0.1:9001?850.
  0020: 12 00 00 00 47 00 72 00 6d 3a 20 6d 65 40 37 6f   ....G.r.m: me@7o
  0030: 6d 65 77 68 38 3d 65 00 00 54 00 3a 20 66 61 6b   mewh8=e..T.: fak

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00182ecc311b5f0b, size=32 bytes, fuzzer=naive, trial=1, discovered_at=3s, mutation_op=BitFlipMutator,BytesRandSetMutator,ByteDecMutator,ByteDecMutator,QwordAddMutator,ByteAddMutator):
  0000: 00 01 00 00 00 19 70 6b 2b 2b 2b 2b 2b 2a 2b 2b   ......pk+++++*++
  0010: 2b 2b 4b 2b 1f 1f 1e 1f 1f 40 2f 2f 2f 14 00 00   ++K+.....@///...
Seed 2 (id=0024e5972fc0b2e0, size=35 bytes, fuzzer=naive, trial=1, discovered_at=88s, mutation_op=WordAddMutator):
  0000: 00 01 00 00 00 19 25 60 25 61 3e 66 9f 9f 63 25   ......%`%a>f..c%
  0010: 2b 5d 25 41 bf 41 41 41 41 40 41 41 5a 70 65 72   +]%A.AAAA@AAZper
  0020: 6d 69 74                                          mit
Seed 3 (id=00225bc4819174d2, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=152s, mutation_op=BytesInsertMutator,ByteAddMutator,ByteIncMutator,BytesDeleteMutator,ByteDecMutator):
  0000: 00 01 00 00 00 43 64 55 43 25 25 25 25 21 25 65   .....CdUC%%%%!%e
  0010: 26 25 65 24 25 64 45 72 46 25 41 27 25 31 25 25   &%e$%dErF%A'%1%%
  0020: 65 25 44 d6 42 64 45 72 33 25 65 4b 25 43 25 25   e%D.BdEr3%eK%C%%
  0030: 25 25 25 25 25 25 25 25 25 25 25 25 26 25 40 e8   %%%%%%%%%%%%&%@.
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
   0x0005  19(.)x4                             19(.)x8 43(C)x4 44(D)x1 23(#)x1 +6u  PARTIAL
   0x0006  70(p)x4                             25(%)x6 64(d)x3 2e(.)x3 70(p)x1 +7u  PARTIAL
   0x0007  6f(o)x4                             55(U)x2 2e(.)x2 25(%)x2 62(b)x2 +12u  DIFFER
   0x0008  70(p)x3 64(d)x1                     43(C)x5 2b(+)x3 25(%)x2 2e(.)x2 +8u  PARTIAL
   0x0009  33(3)x3 00(.)x1                     25(%)x4 2b(+)x2 41(A)x2 46(F)x2 +10u  DIFFER
   0x000a  26(&)x2 4b(K)x1 00(.)x1             25(%)x6 2e(.)x3 2b(+)x2 3e(>)x1 +8u  DIFFER
   0x000b  2f(/)x3 00(.)x1                     25(%)x4 2b(+)x3 2d(-)x2 63(c)x2 +9u  DIFFER
   0x000c  2f(/)x3 25(%)x1                     25(%)x5 2b(+)x3 2e(.)x3 45(E)x2 +7u  PARTIAL
   0x000d  70(p)x3 3a(:)x1                     2e(.)x3 25(%)x2 64(d)x2 2a(*)x1 +12u  DIFFER
   0x000e  4d(M)x3 3a(:)x1                     25(%)x7 2b(+)x2 2d(-)x2 63(c)x1 +8u  DIFFER
   0x000f  37(7)x3 3a(:)x1                     25(%)x4 45(E)x2 42(B)x2 2b(+)x1 +11u  DIFFER
   0x0010  2e(.)x3 3a(:)x1                     2e(.)x3 2b(+)x2 42(B)x2 25(%)x2 +11u  PARTIAL
   0x0011  ff(.)x3 3a(:)x1                     25(%)x7 2b(+)x2 2d(-)x2 5d(])x1 +8u  DIFFER
   0x0012  2e(.)x3 3a(:)x1                     25(%)x3 41(A)x2 4b(K)x1 65(e)x1 +13u  PARTIAL
   0x0013  30(0)x3 3a(:)x1                     2e(.)x3 41(A)x2 42(B)x2 62(b)x2 +9u  DIFFER
   0x0014  2e(.)x3 3a(:)x1                     25(%)x2 2f(/)x2 42(B)x2 41(A)x2 +11u  PARTIAL
   0x0015  31(1)x3 3a(:)x1                     25(%)x5 41(A)x2 1f(.)x1 64(d)x1 +11u  DIFFER
   0x0016  3a(:)x4                             41(A)x3 64(d)x3 42(B)x2 25(%)x2 +10u  DIFFER
   0x0017  39(9)x4                             41(A)x3 25(%)x2 2e(.)x2 1f(.)x1 +12u  DIFFER
   0x0018  30(0)x4                             41(A)x3 43(C)x3 00(.)x2 25(%)x2 +10u  DIFFER
   0x0019  30(0)x4                             25(%)x3 40(@)x2 45(E)x2 2e(.)x2 +10u  DIFFER
   0x001a  31(1)x3 00(.)x1                     25(%)x5 41(A)x3 2f(/)x2 66(f)x2 +8u  DIFFER
   0x001b  3f(?)x3 ad(.)x1                     2e(.)x3 25(%)x3 2d(-)x2 2f(/)x1 +11u  DIFFER
   0x001c  38(8)x4                             2f(/)x2 2e(.)x2 45(E)x2 5a(Z)x1 +13u  DIFFER
   0x001d  35(5)x4                             2e(.)x2 2d(-)x2 25(%)x2 62(b)x2 +12u  DIFFER
   0x001e  30(0)x4                             25(%)x4 00(.)x2 65(e)x2 44(D)x2 +10u  DIFFER
   0x001f  00(.)x4                             2e(.)x4 25(%)x3 00(.)x2 72(r)x2 +8u  PARTIAL
   0x0020  12(.)x3 11(.)x1                     65(e)x2 2e(.)x2 42(B)x2 6d(m)x1 +12u  DIFFER
   0x0021  00(.)x4                             2d(-)x3 25(%)x2 00(.)x2 62(b)x2 +8u  PARTIAL
   0x0022  00(.)x4                             44(D)x2 00(.)x2 2e(.)x2 74(t)x1 +10u  PARTIAL
   0x0023  00(.)x4                             2e(.)x3 62(b)x2 25(%)x2 d6(.)x1 +7u  PARTIAL
   0x0024  47(G)x4                             50(P)x2 42(B)x1 9e(.)x1 2f(/)x1 +7u  DIFFER
   0x0025  00(.)x3 48(H)x1                     25(%)x3 2e(.)x2 41(A)x2 64(d)x1 +4u  DIFFER
   0x0026  72(r)x3 54(T)x1                     45(E)x2 41(A)x1 2f(/)x1 25(%)x1 +7u  DIFFER
   0x0027  00(.)x3 54(T)x1                     72(r)x1 27(')x1 00(.)x1 40(@)x1 +8u  PARTIAL
   0x0028  6d(m)x3 50(P)x1                     25(%)x5 33(3)x1 db(.)x1 2f(/)x1 +4u  PARTIAL
   0x0029  3a(:)x3 2f(/)x1                     25(%)x2 41(A)x2 31(1)x1 2f(/)x1 +6u  PARTIAL
   0x002a  20( )x4                             25(%)x4 65(e)x1 2e(.)x1 42(B)x1 +4u  DIFFER
   0x002b  6d(m)x4                             25(%)x5 2e(.)x2 4b(K)x1 66(f)x1 +2u  DIFFER
   0x002c  65(e)x4                             25(%)x3 65(e)x2 d2(.)x1 2e(.)x1 +4u  PARTIAL
   ... (19 more divergent offsets)
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
  prompts_b/curl_303.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 303,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 303 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 303 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 303 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).