==== BLOCKER ====
Target: curl
Branch ID: 468
Location: /src/curl/lib/transfer.c:1499:8
Enclosing function: Curl_pretransfer
Source line:     if(data->state.wildcardmatch) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            4        6          0  REFERENCE
cmplog                          10        0          0  REFERENCE
value_profile                    1        9          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             9        1          0  winner (I2S vs value_profile)
naive_ctx                        9        1          0  REFERENCE
naive_ngram4                     5        5          0  REFERENCE
mopt                             6        4          0  REFERENCE
minimizer                        9        1          0  REFERENCE
fast                             8        2          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=6.40h  loser=22.90h
  avg hitcount on branch: winner=7  loser=0
  prob_div=0.80  dur_div=16.50h  hit_div=7
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/468/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_pretransfer (/src/curl/lib/transfer.c:1403-1541) ---
[ ]  1401   */
[ ]  1402  CURLcode Curl_pretransfer(struct Curl_easy *data)
[B]  1403  {
[B]  1404    CURLcode result;
[ ]  1405  
[B]  1406    if(!data->state.url && !data->set.uh) {
[ ]  1407      /* we can't do anything without URL */
[ ]  1408      failf(data, "No URL set");
[ ]  1409      return CURLE_URL_MALFORMAT;
[ ]  1410    }
[ ]  1411  
[ ]  1412    /* since the URL may have been redirected in a previous use of this handle */
[B]  1413    if(data->state.url_alloc) {
[ ]  1414      /* the already set URL is allocated, free it first! */
[ ]  1415      Curl_safefree(data->state.url);
[ ]  1416      data->state.url_alloc = FALSE;
[ ]  1417    }
[ ]  1418  
[B]  1419    if(!data->state.url && data->set.uh) {
[ ]  1420      CURLUcode uc;
[ ]  1421      free(data->set.str[STRING_SET_URL]);
[ ]  1422      uc = curl_url_get(data->set.uh,
[ ]  1423                        CURLUPART_URL, &data->set.str[STRING_SET_URL], 0);
[ ]  1424      if(uc) {
[ ]  1425        failf(data, "No URL set");
[ ]  1426        return CURLE_URL_MALFORMAT;
[ ]  1427      }
[ ]  1428    }
[ ]  1429  
[B]  1430    data->state.prefer_ascii = data->set.prefer_ascii;
[B]  1431    data->state.list_only = data->set.list_only;
[B]  1432    data->state.httpreq = data->set.method;
[B]  1433    data->state.url = data->set.str[STRING_SET_URL];
[ ]  1434  
[ ]  1435    /* Init the SSL session ID cache here. We do it here since we want to do it
[ ]  1436       after the *_setopt() calls (that could specify the size of the cache) but
[ ]  1437       before any transfer takes place. */
[B]  1438    result = Curl_ssl_initsessions(data, data->set.general_ssl.max_ssl_sessions);
[B]  1439    if(result)
[ ]  1440      return result;
[ ]  1441  
[B]  1442    data->state.requests = 0;
[B]  1443    data->state.followlocation = 0; /* reset the location-follow counter */
[B]  1444    data->state.this_is_a_follow = FALSE; /* reset this */
[B]  1445    data->state.errorbuf = FALSE; /* no error has occurred */
[B]  1446    data->state.httpwant = data->set.httpwant;
[B]  1447    data->state.httpversion = 0;
[B]  1448    data->state.authproblem = FALSE;
[B]  1449    data->state.authhost.want = data->set.httpauth;
[B]  1450    data->state.authproxy.want = data->set.proxyauth;
[B]  1451    Curl_safefree(data->info.wouldredirect);
[ ]  1452  
[B]  1453    if(data->state.httpreq == HTTPREQ_PUT)
[ ]  1454      data->state.infilesize = data->set.filesize;
[B]  1455    else if((data->state.httpreq != HTTPREQ_GET) &&
[B]  1456            (data->state.httpreq != HTTPREQ_HEAD)) {
[W]  1457      data->state.infilesize = data->set.postfieldsize;
[W]  1458      if(data->set.postfields && (data->state.infilesize == -1))
[ ]  1459        data->state.infilesize = (curl_off_t)strlen(data->set.postfields);
[W]  1460    }
[B]  1461    else
[B]  1462      data->state.infilesize = 0;
[ ]  1463  
[B]  1464  #ifndef CURL_DISABLE_COOKIES
[ ]  1465    /* If there is a list of cookie files to read, do it now! */
[B]  1466    if(data->state.cookielist)
[B]  1467      Curl_cookie_loadfiles(data);
[B]  1468  #endif
[ ]  1469    /* If there is a list of host pairs to deal with */
[B]  1470    if(data->state.resolve)
[ ]  1471      result = Curl_loadhostpairs(data);
[ ]  1472  
[B]  1473    if(!result) {
[ ]  1474      /* Allow data->set.use_port to set which port to use. This needs to be
[ ]  1475       * disabled for example when we follow Location: headers to URLs using
[ ]  1476       * different ports! */
[B]  1477      data->state.allow_port = TRUE;
[ ]  1478  
[ ]  1479  #if defined(HAVE_SIGNAL) && defined(SIGPIPE) && !defined(HAVE_MSG_NOSIGNAL)
[ ]  1480      /*************************************************************
[ ]  1481       * Tell signal handler to ignore SIGPIPE
[ ]  1482       *************************************************************/
[ ]  1483      if(!data->set.no_signal)
[ ]  1484        data->state.prev_signal = signal(SIGPIPE, SIG_IGN);
[ ]  1485  #endif
[ ]  1486  
[B]  1487      Curl_initinfo(data); /* reset session-specific information "variables" */
[B]  1488      Curl_pgrsResetTransferSizes(data);
[B]  1489      Curl_pgrsStartNow(data);
[ ]  1490  
[ ]  1491      /* In case the handle is re-used and an authentication method was picked
[ ]  1492         in the session we need to make sure we only use the one(s) we now
[ ]  1493         consider to be fine */
[B]  1494      data->state.authhost.picked &= data->state.authhost.want;
[B]  1495      data->state.authproxy.picked &= data->state.authproxy.want;
[ ]  1496  
[B]  1497  #ifndef CURL_DISABLE_FTP
[B]  1498      data->state.wildcardmatch = data->set.wildcard_enabled;
[B]  1499      if(data->state.wildcardmatch) { <-- BLOCKER
[W]  1500        struct WildcardData *wc = &data->wildcard;
[W]  1501        if(wc->state < CURLWC_INIT) {
[W]  1502          result = Curl_wildcard_init(wc); /* init wildcard structures */
[W]  1503          if(result)
[ ]  1504            return CURLE_OUT_OF_MEMORY;
[W]  1505        }
[W]  1506      }
[B]  1507  #endif
[B]  1508      Curl_http2_init_state(&data->state);
[B]  1509      result = Curl_hsts_loadcb(data, data->hsts);
[B]  1510    }
[ ]  1511  
[ ]  1512    /*
[ ]  1513     * Set user-agent. Used for HTTP, but since we can attempt to tunnel
[ ]  1514     * basically anything through a http proxy we can't limit this based on
[ ]  1515     * protocol.
[ ]  1516     */
[B]  1517    if(data->set.str[STRING_USERAGENT]) {
[ ]  1518      Curl_safefree(data->state.aptr.uagent);
[ ]  1519      data->state.aptr.uagent =
[ ]  1520        aprintf("User-Agent: %s\r\n", data->set.str[STRING_USERAGENT]);
[ ]  1521      if(!data->state.aptr.uagent)
[ ]  1522        return CURLE_OUT_OF_MEMORY;
[ ]  1523    }
[ ]  1524  
[B]  1525    if(!result)
[B]  1526      result = Curl_setstropt(&data->state.aptr.user,
[B]  1527                              data->set.str[STRING_USERNAME]);
[B]  1528    if(!result)
[B]  1529      result = Curl_setstropt(&data->state.aptr.passwd,
[B]  1530                              data->set.str[STRING_PASSWORD]);
[B]  1531    if(!result)
[B]  1532      result = Curl_setstropt(&data->state.aptr.proxyuser,
[B]  1533                              data->set.str[STRING_PROXYUSERNAME]);
[B]  1534    if(!result)
[B]  1535      result = Curl_setstropt(&data->state.aptr.proxypasswd,
[B]  1536                              data->set.str[STRING_PROXYPASSWORD]);
[ ]  1537  
[B]  1538    data->req.headerbytecount = 0;
[B]  1539    Curl_headers_cleanup(data);
[B]  1540    return result;
[B]  1541  }

--- Caller (1 hop): multi.c:multi_runsingle (/src/curl/lib/multi.c:1811-2661, calls Curl_pretransfer at line 1876) (±10 around call site) ---
[ ]  1866           stored, but we must not check already completed handles */
[B]  1867        if(multi_handle_timeout(data, nowp, &stream_error, &result, FALSE)) {
[ ]  1868          /* Skip the statemachine and go directly to error handling section. */
[ ]  1869          goto statemachine_end;
[ ]  1870        }
[B]  1871      }
[ ]  1872  
[B]  1873      switch(data->mstate) {
[B]  1874      case MSTATE_INIT:
[ ]  1875        /* init this transfer. */
[B]  1876        result = Curl_pretransfer(data); <-- CALL
[ ]  1877  
[B]  1878        if(!result) {
[ ]  1879          /* after init, go CONNECT */
[B]  1880          multistate(data, MSTATE_CONNECT);
[B]  1881          *nowp = Curl_pgrsTime(data, TIMER_STARTOP);
[B]  1882          rc = CURLM_CALL_MULTI_PERFORM;
[B]  1883        }
[B]  1884        break;
[ ]  1885  
[ ]  1886      case MSTATE_PENDING:

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_pretransfer at line 1876)
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
       5         0  curl_multi_fdset  (/src/curl/lib/multi.c:1099-1154)
       5         0  multi.c:add_next_timeout  (/src/curl/lib/multi.c:3055-3094)
       5         0  Curl_single_getsock  (/src/curl/lib/transfer.c:1352-1387)
       2         0  Curl_get_upload_buffer  (/src/curl/lib/transfer.c:118-125)
       1         0  Curl_fillreadbuffer  (/src/curl/lib/transfer.c:163-363)
       1         0  Curl_done_sending  (/src/curl/lib/transfer.c:882-896)
       1         0  transfer.c:readwrite_upload  (/src/curl/lib/transfer.c:928-1154)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716) ---
  d=3   L2704  T=5 F=14  T=0 F=10  if(t)
  d=3   L2708  T=5 F=14  T=0 F=10  } while(t);
--- d=2  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661) ---
  d=2   L2407  T=6 F=5  T=7 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=2   L2407  T=0 F=5  T=0 F=0  if(done || (result == CURLE_RECV_ERROR)) {
  d=2   L2425  T=0 F=5  T=0 F=0  else if((CURLE_HTTP2_STREAM == result) &&
  d=2   L2464  T=6 F=5  T=7 F=0  else if(done) {
  d=2   L2515  T=0 F=5  T=0 F=0  else if(comeback) {
--- d=1  Curl_pretransfer  (/src/curl/lib/transfer.c:1403-1541) ---
  d=1   L1455  T=1 F=8  T=0 F=10  else if((data->state.httpreq != HTTPREQ_GET) &&
  d=1   L1456  T=1 F=0  T=0 F=0  (data->state.httpreq != HTTPREQ_HEAD)) {
  d=1   L1458  T=0 F=1  T=0 F=0  if(data->set.postfields && (data->state.infilesize == -1))
  d=1   L1499  T=9 F=0  T=0 F=10  if(data->state.wildcardmatch) {  <-- BLOCKER
  d=1   L1501  T=9 F=0  T=0 F=0  if(wc->state < CURLWC_INIT) {
  d=1   L1503  T=0 F=9  T=0 F=0  if(result)

[off-chain: 81 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=5fec9094ba291fe6, size=119 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=6s, mutation_op=BytesCopyMutator,BytesDeleteMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 38 3a 2f 2f 31 32 37   ......pop8://127
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   .0.0.1:9001/850.
  0020: 02 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 73 6f   ....GFrom: me@so
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak
Seed 2 (id=66bbe8e2a6a91b6a, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1007s, mutation_op=BytesSwapMutator,BytesSwapMutator,BytesRandInsertMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 3a 2f 00 32 37   ......pop3K:/.27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   .0.0.1:9001/850.
  0020: 02 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 6c 6f   ....GFrom: me@lo
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak
Seed 3 (id=4cf5628c3a4c5dba, size=119 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2685s, mutation_op=BytesDeleteMutator):
  0000: 00 01 00 00 00 19 4d 51 54 54 3a 2f 2f 31 32 37   ......MQTT://127
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   .0.0.1:9001/850.
  0020: 02 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 73 6f   ....GFrom: me@so
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak
Seed 4 (id=7bcbae710a7130dd, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=7946s, mutation_op=BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 3f 3a 3a 3a   ......pop3K/?:::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 31 ad 38 35 30 00   :::::::9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 72 65 0d 0a 54 72 e0 6e 63 66 65   mewhere..Tr.ncfe
Seed 5 (id=6d700d2eb9984aee, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=11569s, mutation_op=BytesDeleteMutator,ByteNegMutator,BytesDeleteMutator,BytesRandSetMutator,ByteAddMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 19 4d 6f 70 33 40 2e 2f 3f 32 37   ......Mop3@./?27
  0010: 3e 30 2e 30 2e 31 3a 39 30 30 31 2f 56 35 30 00   >0.0.1:9001/V50.
  0020: 16 00 00 00 47 46 42 54 6d 3a 20 6d 65 40 24 6f   ....GFBTm: me@$o
  0030: 6d 65 77 68 65 48 65 0d 0a 54 6f 3a 20 66 61 6b   mewheHe..To: fak

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00225bc4819174d2, size=73 bytes, fuzzer=value_profile, trial=1, discovered_at=152s, mutation_op=BytesInsertMutator,ByteAddMutator,ByteIncMutator,BytesDeleteMutator,ByteDecMutator):
  0000: 00 01 00 00 00 43 64 55 43 25 25 25 25 21 25 65   .....CdUC%%%%!%e
  0010: 26 25 65 24 25 64 45 72 46 25 41 27 25 31 25 25   &%e$%dErF%A'%1%%
  0020: 65 25 44 d6 42 64 45 72 33 25 65 4b 25 43 25 25   e%D.BdEr3%eK%C%%
  0030: 25 25 25 25 25 25 25 25 25 25 25 25 26 25 40 e8   %%%%%%%%%%%%&%@.
Seed 2 (id=002bcaf632e31c2a, size=36 bytes, fuzzer=value_profile, trial=1, discovered_at=2534s, mutation_op=TokenReplace,BytesCopyMutator,ByteDecMutator,BytesSetMutator,BytesSetMutator):
  0000: 00 01 00 00 00 19 2d 70 2e 2e 2e 2d 2e 2e 2d 70   ......-p...-..-p
  0010: 2e 2e 2e 2e 3e 3e 42 0f 00 2e 2e 2e 2e 2e 2e 2e   ....>>B.........
  0020: 2e 2e 2e 2e                                       ....
Seed 3 (id=001607afc7f08ce7, size=74 bytes, fuzzer=value_profile, trial=1, discovered_at=3913s, mutation_op=BytesCopyMutator):
  0000: 00 01 00 00 00 44 64 55 43 db b5 25 45 66 25 66   .....DdUC..%Ef%f
  0010: 42 62 9e 62 9e 44 64 55 43 db b5 25 45 66 25 66   Bb.b.DdUC..%Ef%f
  0020: 42 62 9e 62 9e 43 41 27 db 31 25 25 25 25 26 55   Bb.b.CA'.1%%%%&U
  0030: 43 db b5 25 45 66 25 65 42 62 9e 66 52 66 25 65   C..%Ef%eBb.fRf%e
Seed 4 (id=00224975860e7d7e, size=36 bytes, fuzzer=value_profile, trial=1, discovered_at=4107s, mutation_op=DwordAddMutator,QwordAddMutator,CrossoverReplaceMutator):
  0000: 00 01 00 00 00 19 2e 2d 2b 47 2b 2b 2b 2e 4e 51   .......-+G+++.NQ
  0010: 37 2b 2b 2d 2b 2e 4e 41 59 2b 38 2d 2b 2e 46 25   7++-+.NAY+8-+.F%
  0020: 21 00 00 8d                                       !...
Seed 5 (id=001ce769b822a341, size=57 bytes, fuzzer=value_profile, trial=1, discovered_at=22931s, mutation_op=BytesCopyMutator):
  0000: 00 01 00 00 00 2e 2e 2e 2e 2b 2e 2d 2e 2e 2e 2e   .........+.-....
  0010: 2e 2d 6e 2e 2e 2d 6d 2e 2e 2d 6e 2e 2e 2d 6d 2e   .-n..-m..-n..-m.
  0020: 2e 2d 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e   .-..............
  0030: 2e 2e 2e 2e 2e 4f 4e 11 80                        .....ON..


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0005  19(.)x9                             43(C)x4 19(.)x2 44(D)x1 2e(.)x1 +2u  PARTIAL
   0x0006  70(p)x7 4d(M)x2                     64(d)x3 25(%)x3 2e(.)x2 2d(-)x1 +1u  DIFFER
   0x0007  6f(o)x8 51(Q)x1                     55(U)x2 62(b)x2 70(p)x1 2d(-)x1 +4u  DIFFER
   0x0008  70(p)x8 54(T)x1                     43(C)x3 2e(.)x2 2b(+)x1 25(%)x1 +3u  DIFFER
   0x0009  33(3)x7 38(8)x1 54(T)x1             25(%)x2 2e(.)x1 db(.)x1 47(G)x1 +5u  DIFFER
   0x000a  4b(K)x6 3a(:)x2 40(@)x1             25(%)x3 2e(.)x2 b5(.)x1 2b(+)x1 +3u  DIFFER
   0x000b  2e(.)x5 2f(/)x3 3a(:)x1             25(%)x3 2d(-)x2 2b(+)x1 bd(.)x1 +3u  DIFFER
   0x000c  2f(/)x8 3f(?)x1                     25(%)x3 2e(.)x2 45(E)x1 2b(+)x1 +3u  DIFFER
   0x000d  3f(?)x5 31(1)x2 00(.)x1 3a(:)x1     2e(.)x3 64(d)x2 21(!)x1 66(f)x1 +3u  PARTIAL
   0x000e  32(2)x8 3a(:)x1                     25(%)x6 2d(-)x1 4e(N)x1 2e(.)x1 +1u  DIFFER
   0x000f  37(7)x8 3a(:)x1                     65(e)x1 70(p)x1 66(f)x1 51(Q)x1 +6u  DIFFER
   0x0010  2e(.)x6 3a(:)x1 3e(>)x1 26(&)x1     2e(.)x2 42(B)x2 26(&)x1 37(7)x1 +4u  PARTIAL
   0x0011  30(0)x8 3a(:)x1                     25(%)x4 2e(.)x1 62(b)x1 2b(+)x1 +3u  DIFFER
   0x0012  2e(.)x8 3a(:)x1                     65(e)x1 2e(.)x1 9e(.)x1 2b(+)x1 +6u  PARTIAL
   0x0013  30(0)x8 3a(:)x1                     2e(.)x2 62(b)x2 24($)x1 2d(-)x1 +4u  DIFFER
   0x0014  2e(.)x8 3a(:)x1                     25(%)x2 61(a)x2 3e(>)x1 9e(.)x1 +4u  PARTIAL
   0x0015  31(1)x8 3a(:)x1                     25(%)x2 64(d)x1 3e(>)x1 44(D)x1 +5u  DIFFER
   0x0016  3a(:)x9                             64(d)x3 45(E)x1 42(B)x1 4e(N)x1 +4u  DIFFER
   0x0017  39(9)x9                             72(r)x1 0f(.)x1 55(U)x1 41(A)x1 +6u  DIFFER
   0x0018  30(0)x9                             46(F)x1 00(.)x1 43(C)x1 59(Y)x1 +6u  DIFFER
   0x0019  30(0)x9                             25(%)x2 2e(.)x1 db(.)x1 2b(+)x1 +5u  DIFFER
   0x001a  31(1)x9                             41(A)x2 66(f)x2 2e(.)x1 b5(.)x1 +4u  DIFFER
   0x001b  ad(.)x5 2f(/)x4                     25(%)x3 2e(.)x2 27(')x1 2d(-)x1 +3u  DIFFER
   0x001c  38(8)x8 56(V)x1                     2e(.)x2 25(%)x1 45(E)x1 2b(+)x1 +5u  DIFFER
   0x001d  35(5)x9                             2e(.)x2 25(%)x2 62(b)x2 31(1)x1 +3u  DIFFER
   0x001e  30(0)x9                             25(%)x3 2e(.)x1 46(F)x1 6d(m)x1 +4u  DIFFER
   0x001f  00(.)x9                             25(%)x3 2e(.)x2 66(f)x1 62(b)x1 +3u  DIFFER
   0x0020  02(.)x8 16(.)x1                     2e(.)x2 42(B)x2 65(e)x1 21(!)x1 +4u  DIFFER
   0x0021  00(.)x9                             62(b)x2 25(%)x1 2e(.)x1 00(.)x1 +5u  PARTIAL
   0x0022  00(.)x9                             2e(.)x2 44(D)x1 9e(.)x1 00(.)x1 +5u  PARTIAL
   0x0023  00(.)x9                             2e(.)x2 62(b)x2 d6(.)x1 8d(.)x1 +4u  DIFFER
   0x0024  47(G)x9                             42(B)x1 9e(.)x1 2e(.)x1 44(D)x1 +4u  DIFFER
   0x0025  48(H)x5 46(F)x4                     25(%)x2 64(d)x1 43(C)x1 2e(.)x1 +3u  DIFFER
   0x0026  54(T)x5 72(r)x3 42(B)x1             45(E)x2 41(A)x1 2e(.)x1 42(B)x1 +3u  PARTIAL
   0x0027  54(T)x6 6f(o)x3                     72(r)x1 27(')x1 2e(.)x1 42(B)x1 +4u  DIFFER
   0x0028  50(P)x5 6d(m)x4                     25(%)x4 33(3)x1 db(.)x1 2e(.)x1 +1u  DIFFER
   0x0029  2f(/)x5 3a(:)x4                     41(A)x2 25(%)x1 31(1)x1 2e(.)x1 +3u  DIFFER
   0x002a  20( )x9                             25(%)x2 65(e)x1 2e(.)x1 42(B)x1 +3u  DIFFER
   0x002b  6d(m)x9                             25(%)x3 4b(K)x1 2e(.)x1 66(f)x1 +2u  DIFFER
   0x002c  65(e)x9                             25(%)x3 2e(.)x1 6e(n)x1 62(b)x1 +2u  PARTIAL
   ... (18 more divergent offsets)
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
  prompts_b/curl_468.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 468,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 468 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 468 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 468 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).