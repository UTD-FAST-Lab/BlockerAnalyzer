==== BLOCKER ====
Target: curl
Branch ID: 152
Location: /src/curl/lib/http.c:2615:8
Enclosing function: Curl_http_bodysend
Source line:     if(!Curl_checkheaders(data, STRCONST("Content-Type"))) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    0       10          0  REFERENCE
value_profile_cmplog             7        3          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=13.00h  loser=21.40h
  avg hitcount on branch: winner=2  loser=0
  prob_div=0.80  dur_div=8.40h  hit_div=2
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/152/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_http_bodysend (/src/curl/lib/http.c:2437-2772) ---
[ ]  2435  CURLcode Curl_http_bodysend(struct Curl_easy *data, struct connectdata *conn,
[ ]  2436                              struct dynbuf *r, Curl_HttpReq httpreq)
[B]  2437  {
[B]  2438  #ifndef USE_HYPER
[ ]  2439    /* Hyper always handles the body separately */
[B]  2440    curl_off_t included_body = 0;
[ ]  2441  #else
[ ]  2442    /* from this point down, this function should not be used */
[ ]  2443  #define Curl_buffer_send(a,b,c,d,e) CURLE_OK
[ ]  2444  #endif
[B]  2445    CURLcode result = CURLE_OK;
[B]  2446    struct HTTP *http = data->req.p.http;
[B]  2447    const char *ptr;
[ ]  2448  
[ ]  2449    /* If 'authdone' is FALSE, we must not set the write socket index to the
[ ]  2450       Curl_transfer() call below, as we're not ready to actually upload any
[ ]  2451       data yet. */
[ ]  2452  
[B]  2453    switch(httpreq) {
[ ]  2454  
[ ]  2455    case HTTPREQ_PUT: /* Let's PUT the data to the server! */
[ ]  2456  
[ ]  2457      if(conn->bits.authneg)
[ ]  2458        http->postsize = 0;
[ ]  2459      else
[ ]  2460        http->postsize = data->state.infilesize;
[ ]  2461  
[ ]  2462      if((http->postsize != -1) && !data->req.upload_chunky &&
[ ]  2463         (conn->bits.authneg ||
[ ]  2464          !Curl_checkheaders(data, STRCONST("Content-Length")))) {
[ ]  2465        /* only add Content-Length if not uploading chunked */
[ ]  2466        result = Curl_dyn_addf(r, "Content-Length: %" CURL_FORMAT_CURL_OFF_T
[ ]  2467                               "\r\n", http->postsize);
[ ]  2468        if(result)
[ ]  2469          return result;
[ ]  2470      }
[ ]  2471  
[ ]  2472      if(http->postsize) {
[ ]  2473        result = expect100(data, conn, r);
[ ]  2474        if(result)
[ ]  2475          return result;
[ ]  2476      }
[ ]  2477  
[ ]  2478      /* end of headers */
[ ]  2479      result = Curl_dyn_addn(r, STRCONST("\r\n"));
[ ]  2480      if(result)
[ ]  2481        return result;
[ ]  2482  
[ ]  2483      /* set the upload size to the progress meter */
[ ]  2484      Curl_pgrsSetUploadSize(data, http->postsize);
[ ]  2485  
[ ]  2486      /* this sends the buffer and frees all the buffer resources */
[ ]  2487      result = Curl_buffer_send(r, data, &data->info.request_size, 0,
[ ]  2488                                FIRSTSOCKET);
[ ]  2489      if(result)
[ ]  2490        failf(data, "Failed sending PUT request");
[ ]  2491      else
[ ]  2492        /* prepare for transfer */
[ ]  2493        Curl_setup_transfer(data, FIRSTSOCKET, -1, TRUE,
[ ]  2494                            http->postsize?FIRSTSOCKET:-1);
[ ]  2495      if(result)
[ ]  2496        return result;
[ ]  2497      break;
[ ]  2498  
[ ]  2499    case HTTPREQ_POST_FORM:
[ ]  2500    case HTTPREQ_POST_MIME:
[ ]  2501      /* This is form posting using mime data. */
[ ]  2502      if(conn->bits.authneg) {
[ ]  2503        /* nothing to post! */
[ ]  2504        result = Curl_dyn_addn(r, STRCONST("Content-Length: 0\r\n\r\n"));
[ ]  2505        if(result)
[ ]  2506          return result;
[ ]  2507  
[ ]  2508        result = Curl_buffer_send(r, data, &data->info.request_size, 0,
[ ]  2509                                  FIRSTSOCKET);
[ ]  2510        if(result)
[ ]  2511          failf(data, "Failed sending POST request");
[ ]  2512        else
[ ]  2513          /* setup variables for the upcoming transfer */
[ ]  2514          Curl_setup_transfer(data, FIRSTSOCKET, -1, TRUE, -1);
[ ]  2515        break;
[ ]  2516      }
[ ]  2517  
[ ]  2518      data->state.infilesize = http->postsize;
[ ]  2519  
[ ]  2520      /* We only set Content-Length and allow a custom Content-Length if
[ ]  2521         we don't upload data chunked, as RFC2616 forbids us to set both
[ ]  2522         kinds of headers (Transfer-Encoding: chunked and Content-Length) */
[ ]  2523      if(http->postsize != -1 && !data->req.upload_chunky &&
[ ]  2524         (conn->bits.authneg ||
[ ]  2525          !Curl_checkheaders(data, STRCONST("Content-Length")))) {
[ ]  2526        /* we allow replacing this header if not during auth negotiation,
[ ]  2527           although it isn't very wise to actually set your own */
[ ]  2528        result = Curl_dyn_addf(r,
[ ]  2529                               "Content-Length: %" CURL_FORMAT_CURL_OFF_T
[ ]  2530                               "\r\n", http->postsize);
[ ]  2531        if(result)
[ ]  2532          return result;
[ ]  2533      }
[ ]  2534  
[ ]  2535  #ifndef CURL_DISABLE_MIME
[ ]  2536      /* Output mime-generated headers. */
[ ]  2537      {
[ ]  2538        struct curl_slist *hdr;
[ ]  2539  
[ ]  2540        for(hdr = http->sendit->curlheaders; hdr; hdr = hdr->next) {
[ ]  2541          result = Curl_dyn_addf(r, "%s\r\n", hdr->data);
[ ]  2542          if(result)
[ ]  2543            return result;
[ ]  2544        }
[ ]  2545      }
[ ]  2546  #endif
[ ]  2547  
[ ]  2548      /* For really small posts we don't use Expect: headers at all, and for
[ ]  2549         the somewhat bigger ones we allow the app to disable it. Just make
[ ]  2550         sure that the expect100header is always set to the preferred value
[ ]  2551         here. */
[ ]  2552      ptr = Curl_checkheaders(data, STRCONST("Expect"));
[ ]  2553      if(ptr) {
[ ]  2554        data->state.expect100header =
[ ]  2555          Curl_compareheader(ptr, STRCONST("Expect:"), STRCONST("100-continue"));
[ ]  2556      }
[ ]  2557      else if(http->postsize > EXPECT_100_THRESHOLD || http->postsize < 0) {
[ ]  2558        result = expect100(data, conn, r);
[ ]  2559        if(result)
[ ]  2560          return result;
[ ]  2561      }
[ ]  2562      else
[ ]  2563        data->state.expect100header = FALSE;
[ ]  2564  
[ ]  2565      /* make the request end in a true CRLF */
[ ]  2566      result = Curl_dyn_addn(r, STRCONST("\r\n"));
[ ]  2567      if(result)
[ ]  2568        return result;
[ ]  2569  
[ ]  2570      /* set the upload size to the progress meter */
[ ]  2571      Curl_pgrsSetUploadSize(data, http->postsize);
[ ]  2572  
[ ]  2573      /* Read from mime structure. */
[ ]  2574      data->state.fread_func = (curl_read_callback) Curl_mime_read;
[ ]  2575      data->state.in = (void *) http->sendit;
[ ]  2576      http->sending = HTTPSEND_BODY;
[ ]  2577  
[ ]  2578      /* this sends the buffer and frees all the buffer resources */
[ ]  2579      result = Curl_buffer_send(r, data, &data->info.request_size, 0,
[ ]  2580                                FIRSTSOCKET);
[ ]  2581      if(result)
[ ]  2582        failf(data, "Failed sending POST request");
[ ]  2583      else
[ ]  2584        /* prepare for transfer */
[ ]  2585        Curl_setup_transfer(data, FIRSTSOCKET, -1, TRUE,
[ ]  2586                            http->postsize?FIRSTSOCKET:-1);
[ ]  2587      if(result)
[ ]  2588        return result;
[ ]  2589  
[ ]  2590      break;
[ ]  2591  
[B]  2592    case HTTPREQ_POST:
[ ]  2593      /* this is the simple POST, using x-www-form-urlencoded style */
[ ]  2594  
[B]  2595      if(conn->bits.authneg)
[ ]  2596        http->postsize = 0;
[B]  2597      else
[ ]  2598        /* the size of the post body */
[B]  2599        http->postsize = data->state.infilesize;
[ ]  2600  
[ ]  2601      /* We only set Content-Length and allow a custom Content-Length if
[ ]  2602         we don't upload data chunked, as RFC2616 forbids us to set both
[ ]  2603         kinds of headers (Transfer-Encoding: chunked and Content-Length) */
[B]  2604      if((http->postsize != -1) && !data->req.upload_chunky &&
[B]  2605         (conn->bits.authneg ||
[B]  2606          !Curl_checkheaders(data, STRCONST("Content-Length")))) {
[ ]  2607        /* we allow replacing this header if not during auth negotiation,
[ ]  2608           although it isn't very wise to actually set your own */
[B]  2609        result = Curl_dyn_addf(r, "Content-Length: %" CURL_FORMAT_CURL_OFF_T
[B]  2610                               "\r\n", http->postsize);
[B]  2611        if(result)
[ ]  2612          return result;
[B]  2613      }
[ ]  2614  
[B]  2615      if(!Curl_checkheaders(data, STRCONST("Content-Type"))) { <-- BLOCKER
[L]  2616        result = Curl_dyn_addn(r, STRCONST("Content-Type: application/"
[L]  2617                                           "x-www-form-urlencoded\r\n"));
[L]  2618        if(result)
[ ]  2619          return result;
[L]  2620      }
[ ]  2621  
[ ]  2622      /* For really small posts we don't use Expect: headers at all, and for
[ ]  2623         the somewhat bigger ones we allow the app to disable it. Just make
[ ]  2624         sure that the expect100header is always set to the preferred value
[ ]  2625         here. */
[B]  2626      ptr = Curl_checkheaders(data, STRCONST("Expect"));
[B]  2627      if(ptr) {
[ ]  2628        data->state.expect100header =
[ ]  2629          Curl_compareheader(ptr, STRCONST("Expect:"), STRCONST("100-continue"));
[ ]  2630      }
[B]  2631      else if(http->postsize > EXPECT_100_THRESHOLD || http->postsize < 0) {
[ ]  2632        result = expect100(data, conn, r);
[ ]  2633        if(result)
[ ]  2634          return result;
[ ]  2635      }
[B]  2636      else
[B]  2637        data->state.expect100header = FALSE;
[ ]  2638  
[B]  2639  #ifndef USE_HYPER
[ ]  2640      /* With Hyper the body is always passed on separately */
[B]  2641      if(data->set.postfields) {
[ ]  2642  
[ ]  2643        /* In HTTP2, we send request body in DATA frame regardless of
[ ]  2644           its size. */
[B]  2645        if(conn->httpversion != 20 &&
[B]  2646           !data->state.expect100header &&
[B]  2647           (http->postsize < MAX_INITIAL_POST_SIZE)) {
[ ]  2648          /* if we don't use expect: 100  AND
[ ]  2649             postsize is less than MAX_INITIAL_POST_SIZE
[ ]  2650  
[ ]  2651             then append the post data to the HTTP request header. This limit
[ ]  2652             is no magic limit but only set to prevent really huge POSTs to
[ ]  2653             get the data duplicated with malloc() and family. */
[ ]  2654  
[ ]  2655          /* end of headers! */
[B]  2656          result = Curl_dyn_addn(r, STRCONST("\r\n"));
[B]  2657          if(result)
[ ]  2658            return result;
[ ]  2659  
[B]  2660          if(!data->req.upload_chunky) {
[ ]  2661            /* We're not sending it 'chunked', append it to the request
[ ]  2662               already now to reduce the number if send() calls */
[B]  2663            result = Curl_dyn_addn(r, data->set.postfields,
[B]  2664                                   (size_t)http->postsize);
[B]  2665            included_body = http->postsize;
[B]  2666          }
[ ]  2667          else {
[ ]  2668            if(http->postsize) {
[ ]  2669              char chunk[16];
[ ]  2670              /* Append the POST data chunky-style */
[ ]  2671              msnprintf(chunk, sizeof(chunk), "%x\r\n", (int)http->postsize);
[ ]  2672              result = Curl_dyn_add(r, chunk);
[ ]  2673              if(!result) {
[ ]  2674                included_body = http->postsize + strlen(chunk);
[ ]  2675                result = Curl_dyn_addn(r, data->set.postfields,
[ ]  2676                                       (size_t)http->postsize);
[ ]  2677                if(!result)
[ ]  2678                  result = Curl_dyn_addn(r, STRCONST("\r\n"));
[ ]  2679                included_body += 2;
[ ]  2680              }
[ ]  2681            }
[ ]  2682            if(!result) {
[ ]  2683              result = Curl_dyn_addn(r, STRCONST("\x30\x0d\x0a\x0d\x0a"));
[ ]  2684              /* 0  CR  LF  CR  LF */
[ ]  2685              included_body += 5;
[ ]  2686            }
[ ]  2687          }
[B]  2688          if(result)
[ ]  2689            return result;
[ ]  2690          /* Make sure the progress information is accurate */
[B]  2691          Curl_pgrsSetUploadSize(data, http->postsize);
[B]  2692        }
[ ]  2693        else {
[ ]  2694          /* A huge POST coming up, do data separate from the request */
[ ]  2695          http->postdata = data->set.postfields;
[ ]  2696  
[ ]  2697          http->sending = HTTPSEND_BODY;
[ ]  2698  
[ ]  2699          data->state.fread_func = (curl_read_callback)readmoredata;
[ ]  2700          data->state.in = (void *)data;
[ ]  2701  
[ ]  2702          /* set the upload size to the progress meter */
[ ]  2703          Curl_pgrsSetUploadSize(data, http->postsize);
[ ]  2704  
[ ]  2705          /* end of headers! */
[ ]  2706          result = Curl_dyn_addn(r, STRCONST("\r\n"));
[ ]  2707          if(result)
[ ]  2708            return result;
[ ]  2709        }
[B]  2710      }
[ ]  2711      else
[ ]  2712  #endif
[ ]  2713      {
[ ]  2714         /* end of headers! */
[ ]  2715        result = Curl_dyn_addn(r, STRCONST("\r\n"));
[ ]  2716        if(result)
[ ]  2717          return result;
[ ]  2718  
[ ]  2719        if(data->req.upload_chunky && conn->bits.authneg) {
[ ]  2720          /* Chunky upload is selected and we're negotiating auth still, send
[ ]  2721             end-of-data only */
[ ]  2722          result = Curl_dyn_addn(r, (char *)STRCONST("\x30\x0d\x0a\x0d\x0a"));
[ ]  2723          /* 0  CR  LF  CR  LF */
[ ]  2724          if(result)
[ ]  2725            return result;
[ ]  2726        }
[ ]  2727  
[ ]  2728        else if(data->state.infilesize) {
[ ]  2729          /* set the upload size to the progress meter */
[ ]  2730          Curl_pgrsSetUploadSize(data, http->postsize?http->postsize:-1);
[ ]  2731  
[ ]  2732          /* set the pointer to mark that we will send the post body using the
[ ]  2733             read callback, but only if we're not in authenticate negotiation */
[ ]  2734          if(!conn->bits.authneg)
[ ]  2735            http->postdata = (char *)&http->postdata;
[ ]  2736        }
[ ]  2737      }
[ ]  2738      /* issue the request */
[B]  2739      result = Curl_buffer_send(r, data, &data->info.request_size, included_body,
[B]  2740                                FIRSTSOCKET);
[ ]  2741  
[B]  2742      if(result)
[ ]  2743        failf(data, "Failed sending HTTP POST request");
[B]  2744      else
[B]  2745        Curl_setup_transfer(data, FIRSTSOCKET, -1, TRUE,
[B]  2746                            http->postdata?FIRSTSOCKET:-1);
[B]  2747      break;
[ ]  2748  
[ ]  2749    default:
[ ]  2750      result = Curl_dyn_addn(r, STRCONST("\r\n"));
[ ]  2751      if(result)
[ ]  2752        return result;
[ ]  2753  
[ ]  2754      /* issue the request */
[ ]  2755      result = Curl_buffer_send(r, data, &data->info.request_size, 0,
[ ]  2756                                FIRSTSOCKET);
[ ]  2757      if(result)
[ ]  2758        failf(data, "Failed sending HTTP request");
[ ]  2759  #ifdef USE_WEBSOCKETS
[ ]  2760      else if((conn->handler->protocol & (CURLPROTO_WS|CURLPROTO_WSS)) &&
[ ]  2761              !(data->set.connect_only))
[ ]  2762        /* Set up the transfer for two-way since without CONNECT_ONLY set, this
[ ]  2763           request probably wants to send data too post upgrade */
[ ]  2764        Curl_setup_transfer(data, FIRSTSOCKET, -1, TRUE, FIRSTSOCKET);
[ ]  2765  #endif
[ ]  2766      else
[ ]  2767        /* HTTP GET/HEAD download: */
[ ]  2768        Curl_setup_transfer(data, FIRSTSOCKET, -1, TRUE, -1);
[B]  2769    }
[ ]  2770  
[B]  2771    return result;
[B]  2772  }

--- Caller (1 hop): Curl_http (/src/curl/lib/http.c:3088-3372, calls Curl_http_bodysend at line 3334) (±10 around call site) ---
[B]  3324    if(!result)
[B]  3325      result = Curl_add_custom_headers(data, FALSE, &req);
[ ]  3326  
[B]  3327    if(!result) {
[B]  3328      http->postdata = NULL;  /* nothing to post at this point */
[B]  3329      if((httpreq == HTTPREQ_GET) ||
[B]  3330         (httpreq == HTTPREQ_HEAD))
[ ]  3331        Curl_pgrsSetUploadSize(data, 0); /* nothing */
[ ]  3332  
[ ]  3333      /* bodysend takes ownership of the 'req' memory on success */
[B]  3334      result = Curl_http_bodysend(data, conn, &req, httpreq); <-- CALL
[B]  3335    }
[B]  3336    if(result) {
[ ]  3337      Curl_dyn_free(&req);
[ ]  3338      return result;
[ ]  3339    }
[ ]  3340  
[B]  3341    if((http->postsize > -1) &&
[B]  3342       (http->postsize <= data->req.writebytecount) &&
[B]  3343       (http->sending != HTTPSEND_REQUEST))
[B]  3344      data->req.upload_done = TRUE;

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_http  (/src/curl/lib/http.c:3088-3372, calls Curl_http_bodysend at line 3334)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       1         9  http.c:http_setup_conn  (/src/curl/lib/http.c:234-264)
       1         9  Curl_http_output_auth  (/src/curl/lib/http.c:870-943)
       1         9  Curl_buffer_send  (/src/curl/lib/http.c:1295-1471)
       1         9  Curl_http_connect  (/src/curl/lib/http.c:1541-1584)
       1         9  Curl_http_done  (/src/curl/lib/http.c:1675-1721)
       1         9  Curl_use_http_1_1plus  (/src/curl/lib/http.c:1734-1742)
       1         9  http.c:get_http_string  (/src/curl/lib/http.c:1747-1763)
       1         9  Curl_add_custom_headers  (/src/curl/lib/http.c:1853-1996)
       1         9  Curl_add_timecondition  (/src/curl/lib/http.c:2006-2074)
       1         9  Curl_http_method  (/src/curl/lib/http.c:2088-2124)
       1         9  Curl_http_useragent  (/src/curl/lib/http.c:2127-2137)
       1         9  Curl_http_host  (/src/curl/lib/http.c:2141-2230)
       1         9  Curl_http_target  (/src/curl/lib/http.c:2238-2344)
       1         9  Curl_http_body  (/src/curl/lib/http.c:2348-2433)
       1         9  Curl_http_bodysend  (/src/curl/lib/http.c:2437-2772)  <-- enclosing
... (11 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  Curl_http  (/src/curl/lib/http.c:3088-3372) ---
  d=2   L3105  T=1 F=0  T=9 F=0  if(conn->transport != TRNSPRT_QUIC) {
  d=2   L3106  T=1 F=0  T=9 F=0  if(conn->httpversion < 20) { /* unless the connection is ...
  d=2   L3109  T=0 F=1  T=0 F=9  case CURL_HTTP_VERSION_2:
  d=2   L3116  T=0 F=1  T=0 F=9  case CURL_HTTP_VERSION_1_1:
  d=2   L3119  T=1 F=0  T=9 F=0  default:
  d=2   L3122  T=0 F=1  T=0 F=9  if(data->state.httpwant == CURL_HTTP_VERSION_2_PRIOR_KNOW...
  d=2   L3153  T=0 F=1  T=0 F=9  if(result)
  d=2   L3157  T=0 F=1  T=0 F=9  if(result)
  d=2   L3165  T=1 F=0  T=0 F=9  if(data->state.up.query) {
  d=2   L3167  T=0 F=1  T=0 F=0  if(!pq)
  d=2   L3171  T=1 F=0  T=0 F=9  (pq ? pq : data->state.up.path), FALSE);
  d=2   L3173  T=0 F=1  T=0 F=9  if(result)
  d=2   L3178  T=0 F=1  T=0 F=9  if(data->state.referer && !Curl_checkheaders(data, STRCON...
  d=2   L3184  T=1 F=0  T=9 F=0  if(!Curl_checkheaders(data, STRCONST("Accept-Encoding")) &&
  d=2   L3185  T=0 F=1  T=0 F=9  data->set.str[STRING_ENCODING]) {
  d=2   L3198  T=0 F=1  T=0 F=9  if(result)
  d=2   L3203  T=0 F=1  T=0 F=9  if(result)
  d=2   L3206  T=0 F=1  T=0 F=9  p_accept = Curl_checkheaders(data,
  d=2   L3210  T=0 F=1  T=0 F=9  if(result)
  d=2   L3214  T=0 F=1  T=0 F=9  if(result)
  d=2   L3229  T=1 F=0  T=9 F=0  if(!result)
  d=2   L3231  T=0 F=1  T=0 F=9  if(result) {
  d=2   L3237  T=0 F=1  T=0 F=9  if(conn->bits.altused && !Curl_checkheaders(data, STRCONS...
  d=2   L3263  T=1 F=0  T=9 F=0  (data->state.aptr.host?data->state.aptr.host:""),
  d=2   L3264  T=0 F=1  T=0 F=9  data->state.aptr.proxyuserpwd?
  d=2   L3266  T=0 F=1  T=2 F=7  data->state.aptr.userpwd?data->state.aptr.userpwd:"",
  d=2   L3267  T=0 F=1  T=0 F=9  (data->state.use_range && data->state.aptr.rangeline)?
  d=2   L3269  T=0 F=1  T=0 F=9  (data->set.str[STRING_USERAGENT] &&
  d=2   L3273  T=1 F=0  T=9 F=0  p_accept?p_accept:"",
  d=2   L3274  T=0 F=1  T=0 F=9  data->state.aptr.te?data->state.aptr.te:"",
  d=2   L3275  T=0 F=1  T=0 F=9  (data->set.str[STRING_ENCODING] &&
  d=2   L3279  T=0 F=1  T=0 F=9  (data->state.referer && data->state.aptr.ref)?
  d=2   L3282  T=0 F=1  T=0 F=9  (conn->bits.httpproxy &&
  d=2   L3293  T=0 F=1  T=0 F=9  altused ? altused : ""
  d=2   L3302  T=0 F=1  T=0 F=9  if(result) {
  d=2   L3307  T=1 F=0  T=9 F=0  if(!(conn->handler->flags&PROTOPT_SSL) &&
  d=2   L3308  T=1 F=0  T=9 F=0  conn->httpversion != 20 &&
  d=2   L3309  T=0 F=1  T=0 F=9  (data->state.httpwant == CURL_HTTP_VERSION_2)) {
  d=2   L3320  T=0 F=1  T=0 F=9  if(!result && conn->handler->protocol&(CURLPROTO_WS|CURLP...
  d=2   L3320  T=1 F=0  T=9 F=0  if(!result && conn->handler->protocol&(CURLPROTO_WS|CURLP...
  d=2   L3322  T=1 F=0  T=9 F=0  if(!result)
  d=2   L3324  T=1 F=0  T=9 F=0  if(!result)
  d=2   L3327  T=1 F=0  T=9 F=0  if(!result) {
  d=2   L3329  T=0 F=1  T=0 F=9  if((httpreq == HTTPREQ_GET) ||
  d=2   L3330  T=0 F=1  T=0 F=9  (httpreq == HTTPREQ_HEAD))
  d=2   L3336  T=0 F=1  T=0 F=9  if(result) {
  d=2   L3341  T=1 F=0  T=9 F=0  if((http->postsize > -1) &&
  d=2   L3342  T=1 F=0  T=9 F=0  (http->postsize <= data->req.writebytecount) &&
  d=2   L3343  T=1 F=0  T=9 F=0  (http->sending != HTTPSEND_REQUEST))
  d=2   L3346  T=0 F=1  T=3 F=6  if(data->req.writebytecount) {
  d=2   L3350  T=0 F=0  T=0 F=3  if(Curl_pgrsUpdate(data))
  d=2   L3353  T=0 F=0  T=0 F=3  if(!http->postsize) {
  d=2   L3366  T=0 F=1  T=0 F=9  if((conn->httpversion == 20) && data->req.upload_chunky)
--- d=1  Curl_http_bodysend  (/src/curl/lib/http.c:2437-2772) ---
  d=1   L2455  T=0 F=1  T=0 F=9  case HTTPREQ_PUT: /* Let's PUT the data to the server! */
  d=1   L2499  T=0 F=1  T=0 F=9  case HTTPREQ_POST_FORM:
  d=1   L2500  T=0 F=1  T=0 F=9  case HTTPREQ_POST_MIME:
  d=1   L2592  T=1 F=0  T=9 F=0  case HTTPREQ_POST:
  d=1   L2595  T=0 F=1  T=0 F=9  if(conn->bits.authneg)
  d=1   L2604  T=1 F=0  T=9 F=0  if((http->postsize != -1) && !data->req.upload_chunky &&
  d=1   L2604  T=1 F=0  T=9 F=0  if((http->postsize != -1) && !data->req.upload_chunky &&
  d=1   L2605  T=0 F=1  T=0 F=9  (conn->bits.authneg ||
  d=1   L2606  T=1 F=0  T=9 F=0  !Curl_checkheaders(data, STRCONST("Content-Length")))) {
  d=1   L2611  T=0 F=1  T=0 F=9  if(result)
  d=1   L2615  T=0 F=1  T=9 F=0  if(!Curl_checkheaders(data, STRCONST("Content-Type"))) {  <-- BLOCKER
  d=1   L2618  T=0 F=0  T=0 F=9  if(result)
  d=1   L2627  T=0 F=1  T=0 F=9  if(ptr) {
  d=1   L2631  T=0 F=1  T=0 F=9  else if(http->postsize > EXPECT_100_THRESHOLD || http->po...
  d=1   L2631  T=0 F=1  T=0 F=9  else if(http->postsize > EXPECT_100_THRESHOLD || http->po...
  d=1   L2641  T=1 F=0  T=9 F=0  if(data->set.postfields) {
  d=1   L2645  T=1 F=0  T=9 F=0  if(conn->httpversion != 20 &&
  d=1   L2646  T=1 F=0  T=9 F=0  !data->state.expect100header &&
  d=1   L2647  T=1 F=0  T=9 F=0  (http->postsize < MAX_INITIAL_POST_SIZE)) {
  d=1   L2657  T=0 F=1  T=0 F=9  if(result)
  d=1   L2660  T=1 F=0  T=9 F=0  if(!data->req.upload_chunky) {
  d=1   L2688  T=0 F=1  T=0 F=9  if(result)
  d=1   L2742  T=0 F=1  T=0 F=9  if(result)
  d=1   L2746  T=0 F=1  T=0 F=9  http->postdata?FIRSTSOCKET:-1);
  d=1   L2749  T=0 F=1  T=0 F=9  default:

[off-chain: 152 additional divergent branches across 23 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=6d68b5da252422ab, size=144 bytes, fuzzer=cmplog, trial=1, discovered_at=74909s, mutation_op=BytesInsertMutator,ByteIncMutator,TokenReplace,BytesExpandMutator):
  0000: 00 01 00 00 00 19 70 3f 00 33 3a 2f 00 ad cd c8   ......p?.3:/....
  0010: 80 00 2e ff 7f 00 00 22 ad 00 fe ff ff ff 30 00   ......."......0.
  0020: 06 00 00 00 47 43 6f 6e 74 65 6e 74 2d 54 79 70   ....GContent-Typ
  0030: 65 3a fe fe fe fe fe fe fe cd cd cd cd cd d9 cd   e:..............

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=53b0a593a7569378, size=37 bytes, fuzzer=naive, trial=1, discovered_at=364s, mutation_op=BytesSetMutator,TokenReplace,ByteFlipMutator,ByteDecMutator):
  0000: 00 05 00 00 00 00 00 01 00 00 00 19 70 4f 41 52   ............pOAR
  0010: 41 4d 45 54 45 52 ac 00 00 00 00 3a 20 6e 65 40   AMETER.....: ne@
  0020: 00 ff ff ff ff                                    .....
Seed 2 (id=7b466369118227c6, size=69 bytes, fuzzer=naive, trial=1, discovered_at=1198s, mutation_op=ByteAddMutator,ByteRandMutator):
  0000: 00 2c 00 00 00 00 00 05 00 00 00 19 00 01 00 71   .,.............q
  0010: 25 6f 70 2e 2e 2d 2d 2d 2d 2e 65 2e 2e 00 10 2e   %op..----.e.....
  0020: 2e 2f 2e 2d 2d 00 01 00 00 00 19 27 41 db 25 25   ./.--......'A.%%
  0030: 40 b3 25 2d 85 84 85 85 85 85 85 2d 2e 65 2e 2e   @.%-.......-.e..
Seed 3 (id=6fbc18fb4fc90a08, size=70 bytes, fuzzer=naive, trial=1, discovered_at=4878s, mutation_op=BytesExpandMutator,ByteRandMutator):
  0000: 00 2c 00 00 00 00 00 05 00 00 00 19 9f 01 00 71   .,.............q
  0010: 25 6f 70 2e 2e 2d 2d 2d 2d 2e 65 2e 2e 00 10 2e   %op..----.e.....
  0020: 2e 2f 2e 2d 2d 00 01 00 00 00 19 27 41 db 25 25   ./.--......'A.%%
  0030: 40 b3 25 2d 85 84 85 85 85 85 85 2d 2d 2e 65 2e   @.%-.......--.e.
Seed 4 (id=18d7978a64e26a05, size=37 bytes, fuzzer=naive, trial=1, discovered_at=5903s, mutation_op=ByteInterestingMutator,TokenReplace):
  0000: 00 05 00 00 00 00 00 01 00 00 00 19 70 4f 64 52   ............pOdR
  0010: 41 4d 45 00 00 00 03 00 00 00 00 3a 20 6e 65 40   AME........: ne@
  0020: 00 ff ff ff ff                                    .....
Seed 5 (id=bf91a265ce4ffcd6, size=113 bytes, fuzzer=naive, trial=1, discovered_at=9317s, mutation_op=ByteDecMutator,ByteIncMutator,BytesRandSetMutator):
  0000: 00 01 00 00 00 19 91 6f 70 33 fa 2f 2e 31 32 37   .......op3./.127
  0010: 2e 2f 2f 30 2e 31 a7 39 30 30 31 2f 38 96 30 00   .//0.1.9001/8.0.
  0020: 05 00 00 00 47 67 72 cc cc cc cc cc cc cc cc cc   ....Ggr.........
  0030: cc cc cc cc cc 52 52 52 52 52 6f 52 19 ff 25 41   .....RRRRRoR..%A


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  01(.)x1                             05(.)x2 2c(,)x2 01(.)x2 06(.)x2 +1u  PARTIAL
   0x0005  19(.)x1                             00(.)x7 19(.)x2                     PARTIAL
   0x0006  70(p)x1                             00(.)x7 91(.)x1 31(1)x1             DIFFER
   0x0007  3f(?)x1                             05(.)x4 01(.)x2 6f(o)x1 06(.)x1 +1u  DIFFER
   0x0008  00(.)x1                             00(.)x7 70(p)x1 37(7)x1             PARTIAL
   0x0009  33(3)x1                             00(.)x7 33(3)x1 2e(.)x1             PARTIAL
   0x000a  3a(:)x1                             00(.)x7 fa(.)x1 30(0)x1             DIFFER
   0x000b  2f(/)x1                             19(.)x4 00(.)x3 2f(/)x1 2e(.)x1     PARTIAL
   0x000c  00(.)x1                             00(.)x4 70(p)x2 9f(.)x1 2e(.)x1 +1u  PARTIAL
   0x000d  ad(.)x1                             01(.)x3 4f(O)x2 31(1)x1 06(.)x1 +2u  DIFFER
   0x000e  cd(.)x1                             00(.)x5 41(A)x1 64(d)x1 32(2)x1 +1u  DIFFER
   0x000f  c8(.)x1                             00(.)x4 52(R)x2 71(q)x2 37(7)x1     DIFFER
   0x0010  80(.)x1                             00(.)x3 41(A)x2 25(%)x2 2e(.)x2     DIFFER
   0x0011  00(.)x1                             4d(M)x2 6f(o)x2 00(.)x2 2f(/)x1 +2u  PARTIAL
   0x0012  2e(.)x1                             70(p)x3 45(E)x2 00(.)x2 2f(/)x1 +1u  PARTIAL
   0x0013  ff(.)x1                             2e(.)x2 54(T)x1 00(.)x1 30(0)x1 +4u  DIFFER
   0x0014  7f(.)x1                             2e(.)x4 00(.)x3 45(E)x1 44(D)x1     DIFFER
   0x0015  00(.)x1                             00(.)x3 2d(-)x2 31(1)x2 52(R)x1 +1u  PARTIAL
   0x0016  00(.)x1                             2d(-)x2 00(.)x2 ac(.)x1 03(.)x1 +3u  PARTIAL
   0x0017  22(")x1                             00(.)x3 2d(-)x2 39(9)x2 42(B)x1 +1u  DIFFER
   0x0018  ad(.)x1                             00(.)x3 2d(-)x2 30(0)x2 25(%)x1 +1u  DIFFER
   0x0019  00(.)x1                             00(.)x3 2e(.)x2 30(0)x2 01(.)x1 +1u  PARTIAL
   0x001a  fe(.)x1                             00(.)x3 65(e)x2 31(1)x2 23(#)x1 +1u  DIFFER
   0x001b  ff(.)x1                             3a(:)x2 2e(.)x2 2f(/)x2 00(.)x2 +1u  DIFFER
   0x001c  ff(.)x1                             20( )x2 2e(.)x2 38(8)x2 00(.)x2 +1u  DIFFER
   0x001d  ff(.)x1                             00(.)x3 6e(n)x2 96(.)x2 19(.)x1 +1u  DIFFER
   0x001e  30(0)x1                             65(e)x2 10(.)x2 30(0)x2 70(p)x1 +2u  PARTIAL
   0x001f  00(.)x1                             00(.)x4 40(@)x2 2e(.)x2 23(#)x1     PARTIAL
   0x0020  06(.)x1                             05(.)x3 00(.)x2 2e(.)x2 23(#)x1 +1u  DIFFER
   0x0021  00(.)x1                             00(.)x3 ff(.)x2 2f(/)x2 23(#)x1 +1u  PARTIAL
   0x0022  00(.)x1                             00(.)x3 ff(.)x2 2e(.)x2 23(#)x1 +1u  PARTIAL
   0x0023  00(.)x1                             00(.)x4 ff(.)x2 2d(-)x2 23(#)x1     PARTIAL
   0x0024  47(G)x1                             ff(.)x2 2d(-)x2 47(G)x2 00(.)x2 +1u  PARTIAL
   0x0025  43(C)x1                             00(.)x4 67(g)x1 23(#)x1 47(G)x1     DIFFER
   0x0026  6f(o)x1                             01(.)x3 72(r)x2 23(#)x1 00(.)x1     DIFFER
   0x0027  6e(n)x1                             00(.)x3 cc(.)x1 23(#)x1 01(.)x1 +1u  DIFFER
   0x0028  74(t)x1                             00(.)x4 cc(.)x1 df(.)x1 6d(m)x1     DIFFER
   0x0029  65(e)x1                             00(.)x2 cc(.)x1 ff(.)x1 d0(.)x1 +2u  DIFFER
   0x002a  6e(n)x1                             19(.)x2 cc(.)x1 18(.)x1 31(1)x1 +2u  DIFFER
   0x002b  74(t)x1                             27(')x2 cc(.)x1 70(p)x1 d0(.)x1 +2u  DIFFER
   ... (20 more divergent offsets)
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
  prompts_b/curl_152.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 152,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 152 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 152 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 152 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).