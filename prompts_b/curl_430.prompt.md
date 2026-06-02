==== BLOCKER ====
Target: curl
Branch ID: 430
Location: /src/curl/lib/transfer.c:666:8
Enclosing function: transfer.c:readwrite_data
Source line:     if(!k->header && (nread > 0 || is_empty_data)) {
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
fast                             2        8          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive', 'value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (2) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.60h  loser=24.00h
  avg hitcount on branch: winner=341  loser=0
  prob_div=1.00  dur_div=23.40h  hit_div=341
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002
--- Pair 2: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 4  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=0.10h  loser=24.00h
  avg hitcount on branch: winner=587  loser=0
  prob_div=1.00  dur_div=23.90h  hit_div=587
  subject-level: delta_AUC=118940940.0  p_AUC=0.0002  delta_Final=1804.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/430/{W,L}/branch_coverage_show.txt

--- Enclosing function: transfer.c:readwrite_data (/src/curl/lib/transfer.c:520-878) ---
[ ]   518                                 int *didwhat, bool *done,
[ ]   519                                 bool *comeback)
[B]   520  {
[B]   521    CURLcode result = CURLE_OK;
[B]   522    ssize_t nread; /* number of bytes read */
[B]   523    size_t excess = 0; /* excess bytes read */
[B]   524    bool readmore = FALSE; /* used by RTP to signal for more data */
[B]   525    int maxloops = 100;
[B]   526    char *buf = data->state.buffer;
[B]   527    DEBUGASSERT(buf);
[ ]   528  
[B]   529    *done = FALSE;
[B]   530    *comeback = FALSE;
[ ]   531  
[ ]   532    /* This is where we loop until we have read everything there is to
[ ]   533       read or we get a CURLE_AGAIN */
[B]   534    do {
[B]   535      bool is_empty_data = FALSE;
[B]   536      size_t buffersize = data->set.buffer_size;
[B]   537      size_t bytestoread = buffersize;
[B]   538  #ifdef USE_NGHTTP2
[B]   539      bool is_http2 = ((conn->handler->protocol & PROTO_FAMILY_HTTP) &&
[B]   540                       (conn->httpversion == 20));
[B]   541  #endif
[B]   542      bool is_http3 =
[ ]   543  #ifdef ENABLE_QUIC
[ ]   544        ((conn->handler->protocol & PROTO_FAMILY_HTTP) &&
[ ]   545         (conn->httpversion == 30));
[ ]   546  #else
[B]   547        FALSE;
[B]   548  #endif
[ ]   549  
[B]   550      if(
[B]   551  #ifdef USE_NGHTTP2
[ ]   552        /* For HTTP/2, read data without caring about the content length. This
[ ]   553           is safe because body in HTTP/2 is always segmented thanks to its
[ ]   554           framing layer. Meanwhile, we have to call Curl_read to ensure that
[ ]   555           http2_handle_stream_close is called when we read all incoming bytes
[ ]   556           for a particular stream. */
[B]   557        !is_http2 &&
[B]   558  #endif
[B]   559        !is_http3 && /* Same reason mentioned above. */
[B]   560        k->size != -1 && !k->header) {
[ ]   561        /* make sure we don't read too much */
[ ]   562        curl_off_t totalleft = k->size - k->bytecount;
[ ]   563        if(totalleft < (curl_off_t)bytestoread)
[ ]   564          bytestoread = (size_t)totalleft;
[ ]   565      }
[ ]   566  
[B]   567      if(bytestoread) {
[ ]   568        /* receive data from the network! */
[B]   569        result = Curl_read(data, conn->sockfd, buf, bytestoread, &nread);
[ ]   570  
[ ]   571        /* read would've blocked */
[B]   572        if(CURLE_AGAIN == result)
[ ]   573          break; /* get out of loop */
[ ]   574  
[B]   575        if(result>0)
[ ]   576          return result;
[B]   577      }
[ ]   578      else {
[ ]   579        /* read nothing but since we wanted nothing we consider this an OK
[ ]   580           situation to proceed from */
[ ]   581        DEBUGF(infof(data, "readwrite_data: we're done"));
[ ]   582        nread = 0;
[ ]   583      }
[ ]   584  
[B]   585      if(!k->bytecount) {
[B]   586        Curl_pgrsTime(data, TIMER_STARTTRANSFER);
[B]   587        if(k->exp100 > EXP100_SEND_DATA)
[ ]   588          /* set time stamp to compare with when waiting for the 100 */
[ ]   589          k->start100 = Curl_now();
[B]   590      }
[ ]   591  
[B]   592      *didwhat |= KEEP_RECV;
[ ]   593      /* indicates data of zero size, i.e. empty file */
[B]   594      is_empty_data = ((nread == 0) && (k->bodywrites == 0)) ? TRUE : FALSE;
[ ]   595  
[B]   596      if(0 < nread || is_empty_data) {
[B]   597        buf[nread] = 0;
[B]   598      }
[W]   599      else {
[ ]   600        /* if we receive 0 or less here, either the http2 stream is closed or the
[ ]   601           server closed the connection and we bail out from this! */
[W]   602  #ifdef USE_NGHTTP2
[W]   603        if(is_http2 && !nread)
[ ]   604          DEBUGF(infof(data, "nread == 0, stream closed, bailing"));
[W]   605        else
[W]   606  #endif
[W]   607        if(is_http3 && !nread)
[ ]   608          DEBUGF(infof(data, "nread == 0, stream closed, bailing"));
[W]   609        else
[W]   610          DEBUGF(infof(data, "nread <= 0, server closed connection, bailing"));
[W]   611        k->keepon &= ~KEEP_RECV;
[W]   612        break;
[W]   613      }
[ ]   614  
[ ]   615      /* Default buffer to use when we write the buffer, it may be changed
[ ]   616         in the flow below before the actual storing is done. */
[B]   617      k->str = buf;
[ ]   618  
[B]   619      if(conn->handler->readwrite) {
[ ]   620        result = conn->handler->readwrite(data, conn, &nread, &readmore);
[ ]   621        if(result)
[ ]   622          return result;
[ ]   623        if(readmore)
[ ]   624          break;
[ ]   625      }
[ ]   626  
[B]   627  #ifndef CURL_DISABLE_HTTP
[ ]   628      /* Since this is a two-state thing, we check if we are parsing
[ ]   629         headers at the moment or not. */
[B]   630      if(k->header) {
[ ]   631        /* we are in parse-the-header-mode */
[B]   632        bool stop_reading = FALSE;
[B]   633        result = Curl_http_readwrite_headers(data, conn, &nread, &stop_reading);
[B]   634        if(result)
[ ]   635          return result;
[ ]   636  
[B]   637        if(conn->handler->readwrite &&
[B]   638           (k->maxdownload <= 0 && nread > 0)) {
[ ]   639          result = conn->handler->readwrite(data, conn, &nread, &readmore);
[ ]   640          if(result)
[ ]   641            return result;
[ ]   642          if(readmore)
[ ]   643            break;
[ ]   644        }
[ ]   645  
[B]   646        if(stop_reading) {
[ ]   647          /* We've stopped dealing with input, get out of the do-while loop */
[ ]   648  
[ ]   649          if(nread > 0) {
[ ]   650            infof(data,
[ ]   651                  "Excess found:"
[ ]   652                  " excess = %zd"
[ ]   653                  " url = %s (zero-length body)",
[ ]   654                  nread, data->state.up.path);
[ ]   655          }
[ ]   656  
[ ]   657          break;
[ ]   658        }
[B]   659      }
[B]   660  #endif /* CURL_DISABLE_HTTP */
[ ]   661  
[ ]   662  
[ ]   663      /* This is not an 'else if' since it may be a rest from the header
[ ]   664         parsing, where the beginning of the buffer is headers and the end
[ ]   665         is non-headers. */
[B]   666      if(!k->header && (nread > 0 || is_empty_data)) { <-- BLOCKER
[ ]   667  
[W]   668        if(data->set.opt_no_body) {
[ ]   669          /* data arrives although we want none, bail out */
[ ]   670          streamclose(conn, "ignoring body");
[ ]   671          *done = TRUE;
[ ]   672          return CURLE_WEIRD_SERVER_REPLY;
[ ]   673        }
[ ]   674  
[W]   675  #ifndef CURL_DISABLE_HTTP
[W]   676        if(0 == k->bodywrites && !is_empty_data) {
[ ]   677          /* These checks are only made the first time we are about to
[ ]   678             write a piece of the body */
[W]   679          if(conn->handler->protocol&(PROTO_FAMILY_HTTP|CURLPROTO_RTSP)) {
[ ]   680            /* HTTP-only checks */
[W]   681            result = Curl_http_firstwrite(data, conn, done);
[W]   682            if(result || *done)
[ ]   683              return result;
[W]   684          }
[W]   685        } /* this is the first time we write a body part */
[W]   686  #endif /* CURL_DISABLE_HTTP */
[ ]   687  
[W]   688        k->bodywrites++;
[ ]   689  
[ ]   690        /* pass data to the debug function before it gets "dechunked" */
[W]   691        if(data->set.verbose) {
[ ]   692          if(k->badheader) {
[ ]   693            Curl_debug(data, CURLINFO_DATA_IN,
[ ]   694                       Curl_dyn_ptr(&data->state.headerb),
[ ]   695                       Curl_dyn_len(&data->state.headerb));
[ ]   696            if(k->badheader == HEADER_PARTHEADER)
[ ]   697              Curl_debug(data, CURLINFO_DATA_IN,
[ ]   698                         k->str, (size_t)nread);
[ ]   699          }
[ ]   700          else
[ ]   701            Curl_debug(data, CURLINFO_DATA_IN,
[ ]   702                       k->str, (size_t)nread);
[ ]   703        }
[ ]   704  
[W]   705  #ifndef CURL_DISABLE_HTTP
[W]   706        if(k->chunk) {
[ ]   707          /*
[ ]   708           * Here comes a chunked transfer flying and we need to decode this
[ ]   709           * properly.  While the name says read, this function both reads
[ ]   710           * and writes away the data. The returned 'nread' holds the number
[ ]   711           * of actual data it wrote to the client.
[ ]   712           */
[ ]   713          CURLcode extra;
[ ]   714          CHUNKcode res =
[ ]   715            Curl_httpchunk_read(data, k->str, nread, &nread, &extra);
[ ]   716  
[ ]   717          if(CHUNKE_OK < res) {
[ ]   718            if(CHUNKE_PASSTHRU_ERROR == res) {
[ ]   719              failf(data, "Failed reading the chunked-encoded stream");
[ ]   720              return extra;
[ ]   721            }
[ ]   722            failf(data, "%s in chunked-encoding", Curl_chunked_strerror(res));
[ ]   723            return CURLE_RECV_ERROR;
[ ]   724          }
[ ]   725          if(CHUNKE_STOP == res) {
[ ]   726            /* we're done reading chunks! */
[ ]   727            k->keepon &= ~KEEP_RECV; /* read no more */
[ ]   728  
[ ]   729            /* N number of bytes at the end of the str buffer that weren't
[ ]   730               written to the client. */
[ ]   731            if(conn->chunk.datasize) {
[ ]   732              infof(data, "Leftovers after chunking: % "
[ ]   733                    CURL_FORMAT_CURL_OFF_T "u bytes",
[ ]   734                    conn->chunk.datasize);
[ ]   735            }
[ ]   736          }
[ ]   737          /* If it returned OK, we just keep going */
[ ]   738        }
[W]   739  #endif   /* CURL_DISABLE_HTTP */
[ ]   740  
[ ]   741        /* Account for body content stored in the header buffer */
[W]   742        if((k->badheader == HEADER_PARTHEADER) && !k->ignorebody) {
[ ]   743          size_t headlen = Curl_dyn_len(&data->state.headerb);
[ ]   744          DEBUGF(infof(data, "Increasing bytecount by %zu", headlen));
[ ]   745          k->bytecount += headlen;
[ ]   746        }
[ ]   747  
[W]   748        if((-1 != k->maxdownload) &&
[W]   749           (k->bytecount + nread >= k->maxdownload)) {
[ ]   750  
[ ]   751          excess = (size_t)(k->bytecount + nread - k->maxdownload);
[ ]   752          if(excess > 0 && !k->ignorebody) {
[ ]   753            infof(data,
[ ]   754                  "Excess found in a read:"
[ ]   755                  " excess = %zu"
[ ]   756                  ", size = %" CURL_FORMAT_CURL_OFF_T
[ ]   757                  ", maxdownload = %" CURL_FORMAT_CURL_OFF_T
[ ]   758                  ", bytecount = %" CURL_FORMAT_CURL_OFF_T,
[ ]   759                  excess, k->size, k->maxdownload, k->bytecount);
[ ]   760            connclose(conn, "excess found in a read");
[ ]   761          }
[ ]   762  
[ ]   763          nread = (ssize_t) (k->maxdownload - k->bytecount);
[ ]   764          if(nread < 0) /* this should be unusual */
[ ]   765            nread = 0;
[ ]   766  
[ ]   767          /* HTTP/3 over QUIC should keep reading until QUIC connection
[ ]   768             is closed.  In contrast to HTTP/2 which can stop reading
[ ]   769             from TCP connection, HTTP/3 over QUIC needs ACK from server
[ ]   770             to ensure stream closure.  It should keep reading. */
[ ]   771          if(!is_http3) {
[ ]   772            k->keepon &= ~KEEP_RECV; /* we're done reading */
[ ]   773          }
[ ]   774        }
[ ]   775  
[W]   776        k->bytecount += nread;
[ ]   777  
[W]   778        Curl_pgrsSetDownloadCounter(data, k->bytecount);
[ ]   779  
[W]   780        if(!k->chunk && (nread || k->badheader || is_empty_data)) {
[ ]   781          /* If this is chunky transfer, it was already written */
[ ]   782  
[W]   783          if(k->badheader && !k->ignorebody) {
[ ]   784            /* we parsed a piece of data wrongly assuming it was a header
[ ]   785               and now we output it as body instead */
[ ]   786            size_t headlen = Curl_dyn_len(&data->state.headerb);
[ ]   787  
[ ]   788            /* Don't let excess data pollute body writes */
[ ]   789            if(k->maxdownload == -1 || (curl_off_t)headlen <= k->maxdownload)
[ ]   790              result = Curl_client_write(data, CLIENTWRITE_BODY,
[ ]   791                                         Curl_dyn_ptr(&data->state.headerb),
[ ]   792                                         headlen);
[ ]   793            else
[ ]   794              result = Curl_client_write(data, CLIENTWRITE_BODY,
[ ]   795                                         Curl_dyn_ptr(&data->state.headerb),
[ ]   796                                         (size_t)k->maxdownload);
[ ]   797  
[ ]   798            if(result)
[ ]   799              return result;
[ ]   800          }
[W]   801          if(k->badheader < HEADER_ALLBAD) {
[ ]   802            /* This switch handles various content encodings. If there's an
[ ]   803               error here, be sure to check over the almost identical code
[ ]   804               in http_chunks.c.
[ ]   805               Make sure that ALL_CONTENT_ENCODINGS contains all the
[ ]   806               encodings handled here. */
[W]   807            if(data->set.http_ce_skip || !k->writer_stack) {
[W]   808              if(!k->ignorebody && nread) {
[W]   809  #ifndef CURL_DISABLE_POP3
[W]   810                if(conn->handler->protocol & PROTO_FAMILY_POP3)
[ ]   811                  result = Curl_pop3_write(data, k->str, nread);
[W]   812                else
[W]   813  #endif /* CURL_DISABLE_POP3 */
[W]   814                  result = Curl_client_write(data, CLIENTWRITE_BODY, k->str,
[W]   815                                             nread);
[W]   816              }
[W]   817            }
[W]   818            else if(!k->ignorebody && nread)
[W]   819              result = Curl_unencode_write(data, k->writer_stack, k->str, nread);
[W]   820          }
[W]   821          k->badheader = HEADER_NORMAL; /* taken care of now */
[ ]   822  
[W]   823          if(result)
[W]   824            return result;
[W]   825        }
[ ]   826  
[W]   827      } /* if(!header and data to read) */
[ ]   828  
[B]   829      if(conn->handler->readwrite && excess) {
[ ]   830        /* Parse the excess data */
[ ]   831        k->str += nread;
[ ]   832  
[ ]   833        if(&k->str[excess] > &buf[data->set.buffer_size]) {
[ ]   834          /* the excess amount was too excessive(!), make sure
[ ]   835             it doesn't read out of buffer */
[ ]   836          excess = &buf[data->set.buffer_size] - k->str;
[ ]   837        }
[ ]   838        nread = (ssize_t)excess;
[ ]   839  
[ ]   840        result = conn->handler->readwrite(data, conn, &nread, &readmore);
[ ]   841        if(result)
[ ]   842          return result;
[ ]   843  
[ ]   844        if(readmore)
[ ]   845          k->keepon |= KEEP_RECV; /* we're not done reading */
[ ]   846        break;
[ ]   847      }
[ ]   848  
[B]   849      if(is_empty_data) {
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
[B]   860    } while(data_pending(data) && maxloops--);
[ ]   861  
[B]   862    if(maxloops <= 0) {
[ ]   863      /* we mark it as read-again-please */
[ ]   864      conn->cselect_bits = CURL_CSELECT_IN;
[ ]   865      *comeback = TRUE;
[ ]   866    }
[ ]   867  
[B]   868    if(((k->keepon & (KEEP_RECV|KEEP_SEND)) == KEEP_SEND) &&
[B]   869       conn->bits.close) {
[ ]   870      /* When we've read the entire thing and the close bit is set, the server
[ ]   871         may now close the connection. If there's now any kind of sending going
[ ]   872         on from our side, we need to stop that immediately. */
[ ]   873      infof(data, "we are done reading and this is set to close, stop send");
[ ]   874      k->keepon &= ~KEEP_SEND; /* no writing anymore either */
[ ]   875    }
[ ]   876  
[B]   877    return CURLE_OK;
[B]   878  }

--- Caller (1 hop): Curl_readwrite (/src/curl/lib/transfer.c:1167-1340, calls transfer.c:readwrite_data at line 1219) (±10 around call site) ---
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
[B]  1219      result = readwrite_data(data, conn, k, &didwhat, done, comeback); <-- CALL
[B]  1220      if(result || *done)
[W]  1221        return result;
[B]  1222    }
[ ]  1223  
[ ]  1224    /* If we still have writing to do, we check if we have a writable socket. */
[B]  1225    if((k->keepon & KEEP_SEND) && (select_res & CURL_CSELECT_OUT)) {
[ ]  1226      /* write */
[ ]  1227  
[W]  1228      result = readwrite_upload(data, conn, &didwhat);
[W]  1229      if(result)

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  Curl_readwrite  (/src/curl/lib/transfer.c:1167-1340, calls transfer.c:readwrite_data at line 1219)
hop 3  multi.c:multi_runsingle  (/src/curl/lib/multi.c:1811-2661, calls Curl_readwrite at line 2405)
hop 4  curl_multi_perform  (/src/curl/lib/multi.c:2665-2716, calls multi.c:multi_runsingle at line 2683)
hop 4  multi.c:multi_socket  (/src/curl/lib/multi.c:3101-3208, calls multi.c:multi_runsingle at line 3158)
hop 5  curl_multi_socket  (/src/curl/lib/multi.c:3288-3296, calls multi.c:multi_socket at line 3292)
hop 5  curl_multi_socket_action  (/src/curl/lib/multi.c:3300-3308, calls multi.c:multi_socket at line 3304)
hop 5  curl_multi_strerror  (/src/curl/lib/strerror.c:364-420, calls curl_multi_perform at line 368)
hop 6  easy.c:wait_or_timeout  (/src/curl/lib/easy.c:541-628, calls curl_multi_socket_action at line 582)
hop 6  curl_multi_add_handle  (/src/curl/lib/multi.c:464-590, calls curl_multi_socket at line 509)
hop 7  easy.c:easy_events  (/src/curl/lib/easy.c:636-645, calls easy.c:wait_or_timeout at line 644)
hop 7  easy.c:easy_perform  (/src/curl/lib/easy.c:706-763, calls curl_multi_add_handle at line 741)
hop 7  Curl_multi_add_perform  (/src/curl/lib/multi.c:1574-1594, calls curl_multi_add_handle at line 1580)
hop 8  curl_easy_perform  (/src/curl/lib/easy.c:771-773, calls easy.c:easy_perform at line 772)
hop 8  curl_easy_perform_ev  (/src/curl/lib/easy.c:781-783, calls easy.c:easy_perform at line 782)
hop 8  http2.c:push_promise  (/src/curl/lib/http2.c:565-663, calls Curl_multi_add_perform at line 633)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      20         0  Curl_single_getsock  (/src/curl/lib/transfer.c:1352-1387)
       2         0  Curl_get_upload_buffer  (/src/curl/lib/transfer.c:118-125)
       1         0  Curl_fillreadbuffer  (/src/curl/lib/transfer.c:163-363)
       1         0  Curl_done_sending  (/src/curl/lib/transfer.c:882-896)
       1         0  transfer.c:readwrite_upload  (/src/curl/lib/transfer.c:928-1154)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  Curl_readwrite  (/src/curl/lib/transfer.c:1167-1340) ---
  d=2   L1181  T=40 F=0  T=20 F=0  if((k->keepon & KEEP_RECVBITS) == KEEP_RECV)
  d=2   L1186  T=1 F=39  T=0 F=20  if((k->keepon & KEEP_SENDBITS) == KEEP_SEND)
  d=2   L1192  T=0 F=40  T=0 F=20  if(data->state.drain) {
  d=2   L1198  T=40 F=0  T=20 F=0  if(!select_res) /* Call for select()/poll() only, if read...
  d=2   L1202  T=0 F=40  T=0 F=20  if(select_res == CURL_CSELECT_ERR) {
  d=2   L1218  T=40 F=0  T=20 F=0  if((k->keepon & KEEP_RECV) && (select_res & CURL_CSELECT_...
  d=2   L1218  T=40 F=0  T=20 F=0  if((k->keepon & KEEP_RECV) && (select_res & CURL_CSELECT_...
  d=2   L1220  T=2 F=38  T=0 F=20  if(result || *done)
  d=2   L1225  T=1 F=0  T=0 F=0  if((k->keepon & KEEP_SEND) && (select_res & CURL_CSELECT_...
  d=2   L1225  T=1 F=37  T=0 F=20  if((k->keepon & KEEP_SEND) && (select_res & CURL_CSELECT_...
  d=2   L1229  T=0 F=1  T=0 F=0  if(result)
  d=2   L1279  T=20 F=18  T=0 F=20  if(k->keepon) {
  d=2   L1280  T=0 F=20  T=0 F=0  if(0 > Curl_timeleft(data, &k->now, FALSE)) {
  d=2   L1336  T=18 F=20  T=20 F=0  *done = (0 == (k->keepon&(KEEP_RECV|KEEP_SEND|
--- d=1  transfer.c:readwrite_data  (/src/curl/lib/transfer.c:520-878) ---
  d=1   L 539  T=40 F=0  T=20 F=0  bool is_http2 = ((conn->handler->protocol & PROTO_FAMILY_...
  d=1   L 540  T=0 F=40  T=0 F=20  (conn->httpversion == 20));
  d=1   L 557  T=40 F=0  T=20 F=0  !is_http2 &&
  d=1   L 559  T=40 F=0  T=20 F=0  !is_http3 && /* Same reason mentioned above. */
  d=1   L 560  T=0 F=40  T=0 F=20  k->size != -1 && !k->header) {
  d=1   L 567  T=40 F=0  T=20 F=0  if(bytestoread) {
  d=1   L 572  T=0 F=40  T=0 F=20  if(CURLE_AGAIN == result)
  d=1   L 575  T=0 F=40  T=0 F=20  if(result>0)
  d=1   L 585  T=21 F=19  T=20 F=0  if(!k->bytecount) {
  d=1   L 594  T=18 F=22  T=20 F=0  is_empty_data = ((nread == 0) && (k->bodywrites == 0)) ? ...
  d=1   L 594  T=1 F=17  T=20 F=0  is_empty_data = ((nread == 0) && (k->bodywrites == 0)) ? ...
  d=1   L 596  T=1 F=17  T=20 F=0  if(0 < nread || is_empty_data) {
  d=1   L 596  T=22 F=18  T=0 F=20  if(0 < nread || is_empty_data) {
  d=1   L 603  T=0 F=17  T=0 F=0  if(is_http2 && !nread)
  d=1   L 607  T=0 F=17  T=0 F=0  if(is_http3 && !nread)
  d=1   L 630  T=20 F=3  T=20 F=0  if(k->header) {
  d=1   L 666  T=21 F=2  T=0 F=0  if(!k->header && (nread > 0 || is_empty_data)) {  <-- BLOCKER
  d=1   L 666  T=1 F=1  T=0 F=0  if(!k->header && (nread > 0 || is_empty_data)) {  <-- BLOCKER
  d=1   L 666  T=23 F=0  T=0 F=20  if(!k->header && (nread > 0 || is_empty_data)) {  <-- BLOCKER
  d=1   L 668  T=0 F=22  T=0 F=0  if(data->set.opt_no_body) {
  d=1   L 676  T=19 F=1  T=0 F=0  if(0 == k->bodywrites && !is_empty_data) {
  d=1   L 676  T=20 F=2  T=0 F=0  if(0 == k->bodywrites && !is_empty_data) {
  d=1   L 679  T=19 F=0  T=0 F=0  if(conn->handler->protocol&(PROTO_FAMILY_HTTP|CURLPROTO_R...
  d=1   L 682  T=0 F=19  T=0 F=0  if(result || *done)
  d=1   L 682  T=0 F=19  T=0 F=0  if(result || *done)
  d=1   L 691  T=0 F=22  T=0 F=0  if(data->set.verbose) {
  d=1   L 706  T=0 F=22  T=0 F=0  if(k->chunk) {
  d=1   L 742  T=0 F=22  T=0 F=0  if((k->badheader == HEADER_PARTHEADER) && !k->ignorebody) {
  d=1   L 748  T=0 F=22  T=0 F=0  if((-1 != k->maxdownload) &&
  d=1   L 780  T=1 F=0  T=0 F=0  if(!k->chunk && (nread || k->badheader || is_empty_data)) {
  d=1   L 780  T=21 F=1  T=0 F=0  if(!k->chunk && (nread || k->badheader || is_empty_data)) {
  d=1   L 780  T=0 F=1  T=0 F=0  if(!k->chunk && (nread || k->badheader || is_empty_data)) {
  d=1   L 780  T=22 F=0  T=0 F=0  if(!k->chunk && (nread || k->badheader || is_empty_data)) {
  d=1   L 783  T=0 F=22  T=0 F=0  if(k->badheader && !k->ignorebody) {
  d=1   L 801  T=22 F=0  T=0 F=0  if(k->badheader < HEADER_ALLBAD) {
  d=1   L 807  T=19 F=3  T=0 F=0  if(data->set.http_ce_skip || !k->writer_stack) {
  d=1   L 807  T=0 F=22  T=0 F=0  if(data->set.http_ce_skip || !k->writer_stack) {
  d=1   L 808  T=19 F=0  T=0 F=0  if(!k->ignorebody && nread) {
  d=1   L 808  T=19 F=0  T=0 F=0  if(!k->ignorebody && nread) {
  d=1   L 810  T=0 F=19  T=0 F=0  if(conn->handler->protocol & PROTO_FAMILY_POP3)
  d=1   L 818  T=2 F=1  T=0 F=0  else if(!k->ignorebody && nread)
  d=1   L 818  T=3 F=0  T=0 F=0  else if(!k->ignorebody && nread)
  d=1   L 823  T=2 F=20  T=0 F=0  if(result)
  d=1   L 849  T=1 F=20  T=20 F=0  if(is_empty_data) {

[off-chain: 51 additional divergent branches across 8 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=21cecf684c1b463d, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=254s, mutation_op=ByteNegMutator,BytesExpandMutator,BytesCopyMutator,ByteRandMutator,BytesDeleteMutator,ByteRandMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 4b 2f 2f 3f 32 37   ......pop3K//?27
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 ad 38 35 30 00   .0.0.1:9001.850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 6c 6f   ....GHTTP/ me@lo
  0030: 6d 65 77 68 65 72 65 0a 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak
Seed 2 (id=2b2d16587a91ec51, size=143 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1425s, mutation_op=BytesCopyMutator,BytesDeleteMutator,BytesSwapMutator,BytesInsertCopyMutator,TokenReplace,BytesInsertCopyMutator,BytesSwapMutator):
  0000: 00 01 00 00 00 19 48 54 54 50 3a 2f 30 23 32 25   ......HTTP:/0#2%
  0010: 2e 00 2e 30 2e ad 3a 39 30 30 00 00 38 35 30 00   ...0..:900..850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 40 31 6f   ....GHTTP/ me@1o
  0030: 6d 65 77 68 65 72 65 0d 0a 0d 6f 3a 20 66 60 6b   mewhere...o: f`k
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
Seed 5 (id=29c45d22bae2f634, size=130 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=8082s, mutation_op=BytesDeleteMutator,ByteFlipMutator,DwordInterestingMutator,BytesDeleteMutator,BytesExpandMutator):
  0000: 00 01 00 00 00 19 70 6f 70 fa 00 00 fa 3a 3a 3a   ......pop....:::
  0010: 3a 3a 3a 3a 3a 3a 3a 39 30 30 00 ad 38 35 30 00   :::::::900..850.
  0020: 02 00 00 00 47 48 54 54 50 2f 09 6d 65 40 68 6f   ....GHTTP/.me@ho
  0030: 6d 65 77 68 65 5d 65 0d 0a 54 72 61 6e 73 66 65   mewhe]e..Transfe

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
   0x0005  19(.)x20                            19(.)x10 43(C)x3 2e(.)x2 44(D)x1 +4u  PARTIAL
   0x0006  70(p)x14 9a(.)x5 48(H)x1            25(%)x4 64(d)x3 2e(.)x3 43(C)x2 +7u  PARTIAL
   0x0007  6f(o)x14 9a(.)x5 54(T)x1            55(U)x2 41(A)x2 25(%)x2 2e(.)x2 +12u  DIFFER
   0x0008  70(p)x19 54(T)x1                    43(C)x5 2e(.)x3 25(%)x3 41(A)x2 +7u  DIFFER
   0x000b  2f(/)x14 00(.)x4 7f(.)x1 77(w)x1    25(%)x5 2e(.)x3 63(c)x2 66(f)x1 +9u  DIFFER
   0x0017  39(9)x17 f6(.)x1 bf(.)x1 6f(o)x1    41(A)x3 2e(.)x3 25(%)x3 00(.)x1 +10u  DIFFER
   0x001a  31(1)x12 00(.)x4 ad(.)x3 6f(o)x1    25(%)x5 41(A)x3 f9(.)x1 2b(+)x1 +10u  PARTIAL
   0x001e  30(0)x18 15(.)x1 00(.)x1            25(%)x4 44(D)x2 49(I)x1 65(e)x1 +12u  DIFFER
   0x001f  00(.)x20                            25(%)x3 2e(.)x3 41(A)x2 62(b)x1 +11u  DIFFER
   0x0020  02(.)x20                            65(e)x2 42(B)x2 2e(.)x2 7e(~)x1 +13u  DIFFER
   0x0021  00(.)x20                            25(%)x3 2d(-)x3 05(.)x1 69(i)x1 +11u  PARTIAL
   0x0022  00(.)x20                            44(D)x3 2e(.)x2 61(a)x1 74(t)x1 +10u  PARTIAL
   0x0023  00(.)x20                            2e(.)x2 25(%)x2 d6(.)x1 bb(.)x1 +6u  DIFFER
   0x0024  47(G)x20                            50(P)x2 42(B)x1 9e(.)x1 2e(.)x1 +5u  DIFFER
   0x0025  48(H)x20                            25(%)x3 2e(.)x3 41(A)x2 64(d)x1 +1u  DIFFER
   0x0026  54(T)x20                            2e(.)x2 45(E)x1 41(A)x1 25(%)x1 +5u  DIFFER
   0x0027  54(T)x20                            72(r)x1 27(')x1 40(@)x1 2e(.)x1 +6u  DIFFER
   0x0028  50(P)x20                            25(%)x4 2e(.)x2 33(3)x1 db(.)x1 +2u  PARTIAL
   0x0029  2f(/)x20                            25(%)x2 31(1)x1 2e(.)x1 42(B)x1 +5u  DIFFER
   0x002a  20( )x15 09(.)x3 25(%)x2            25(%)x3 65(e)x1 2e(.)x1 42(B)x1 +4u  PARTIAL
   0x002b  6d(m)x19 92(.)x1                    25(%)x4 2e(.)x2 4b(K)x1 66(f)x1 +2u  DIFFER
   0x002c  65(e)x14 98(.)x3 99(.)x2 9a(.)x1    25(%)x2 2e(.)x2 65(e)x2 d2(.)x1 +3u  PARTIAL
   0x002d  40(@)x7 61(a)x6 a1(.)x5 68(h)x2     25(%)x2 2e(.)x2 43(C)x1 ff(.)x1 +4u  PARTIAL
   0x002f  24($)x9 6f(o)x5 25(%)x5 32(2)x1     25(%)x2 2e(.)x2 55(U)x1 44(D)x1 +3u  PARTIAL
   0x0030  6d(m)x9 65(e)x9 76(v)x1 3a(:)x1     25(%)x2 43(C)x1 2e(.)x1 41(A)x1 +4u  DIFFER
   0x0031  63(c)x9 65(e)x7 3a(:)x3 3f(?)x1     25(%)x1 db(.)x1 2e(.)x1 42(B)x1 +4u  DIFFER
   0x0033  68(h)x9 65(e)x9 2d(-)x1 3a(:)x1     25(%)x3 2e(.)x2 41(A)x2 bd(.)x1     DIFFER
   0x0035  72(r)x17 5d(])x1 43(C)x1 39(9)x1    25(%)x3 44(D)x2 66(f)x1 4f(O)x1 +1u  DIFFER
   0x0036  65(e)x18 6f(o)x1 30(0)x1            25(%)x4 4e(N)x1 45(E)x1 44(D)x1     DIFFER
   0x0038  0a(.)x17 13(.)x2 6e(n)x1            25(%)x3 42(B)x2 80(.)x1 64(d)x1     DIFFER
   0x0039  54(T)x6 43(C)x6 53(S)x3 0d(.)x1 +4u  25(%)x3 62(b)x2                     DIFFER
   0x003a  6f(o)x7 72(r)x4 65(e)x4 8d(.)x2 +3u  25(%)x2 9e(.)x1 42(B)x1 65(e)x1     PARTIAL
   0x003b  6e(n)x6 61(a)x6 74(t)x6 3a(:)x2     25(%)x2 66(f)x1 42(B)x1 65(e)x1     DIFFER
   0x003c  6e(n)x12 2d(-)x4 20( )x2 72(r)x1 +1u  64(d)x2 26(&)x1 52(R)x1 25(%)x1     DIFFER
   0x003e  63(c)x6 66(f)x6 6f(o)x3 61(a)x1 +4u  40(@)x2 25(%)x2 79(y)x1             DIFFER
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
  prompts_b/curl_430.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 430,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 430 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 430 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 430 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).