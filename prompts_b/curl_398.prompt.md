==== BLOCKER ====
Target: curl
Branch ID: 398
Location: /src/curl/lib/setopt.c:3110:3
Enclosing function: Curl_vsetopt
Source line:   default:
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            8        2          0  winner (I2S vs cmplog)
cmplog                           0       10          0  loser (I2S vs naive)
value_profile                    7        3          0  REFERENCE
value_profile_cmplog             0       10          0  REFERENCE
naive_ctx                        4        6          0  REFERENCE
naive_ngram4                     8        2          0  REFERENCE
mopt                             6        4          0  REFERENCE
minimizer                        3        7          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 1  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=10.30h  loser=24.00h
  avg hitcount on branch: winner=1  loser=0
  prob_div=0.80  dur_div=13.70h  hit_div=1
  subject-level: delta_AUC=100639080.0  p_AUC=0.0002  delta_Final=1286.6  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/curl/398/{W,L}/branch_coverage_show.txt

--- Enclosing function: Curl_vsetopt (/src/curl/lib/setopt.c:190-3117) ---
[ ]   188   */
[ ]   189  CURLcode Curl_vsetopt(struct Curl_easy *data, CURLoption option, va_list param)
[B]   190  {
[B]   191    char *argptr;
[B]   192    CURLcode result = CURLE_OK;
[B]   193    long arg;
[B]   194    unsigned long uarg;
[B]   195    curl_off_t bigsize;
[ ]   196  
[B]   197    switch(option) {
[ ]   198    case CURLOPT_DNS_CACHE_TIMEOUT:
[ ]   199      arg = va_arg(param, long);
[ ]   200      if(arg < -1)
[ ]   201        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   202      else if(arg > INT_MAX)
[ ]   203        arg = INT_MAX;
[ ]   204  
[ ]   205      data->set.dns_cache_timeout = (int)arg;
[ ]   206      break;
[ ]   207    case CURLOPT_DNS_USE_GLOBAL_CACHE:
[ ]   208      /* deprecated */
[ ]   209      break;
[ ]   210    case CURLOPT_SSL_CIPHER_LIST:
[ ]   211      /* set a list of cipher we want to use in the SSL connection */
[ ]   212      result = Curl_setstropt(&data->set.str[STRING_SSL_CIPHER_LIST],
[ ]   213                              va_arg(param, char *));
[ ]   214      break;
[ ]   215  #ifndef CURL_DISABLE_PROXY
[ ]   216    case CURLOPT_PROXY_SSL_CIPHER_LIST:
[ ]   217      /* set a list of cipher we want to use in the SSL connection for proxy */
[ ]   218      result = Curl_setstropt(&data->set.str[STRING_SSL_CIPHER_LIST_PROXY],
[ ]   219                              va_arg(param, char *));
[ ]   220      break;
[ ]   221  #endif
[ ]   222    case CURLOPT_TLS13_CIPHERS:
[ ]   223      if(Curl_ssl_tls13_ciphersuites()) {
[ ]   224        /* set preferred list of TLS 1.3 cipher suites */
[ ]   225        result = Curl_setstropt(&data->set.str[STRING_SSL_CIPHER13_LIST],
[ ]   226                                va_arg(param, char *));
[ ]   227      }
[ ]   228      else
[ ]   229        return CURLE_NOT_BUILT_IN;
[ ]   230      break;
[ ]   231  #ifndef CURL_DISABLE_PROXY
[ ]   232    case CURLOPT_PROXY_TLS13_CIPHERS:
[ ]   233      if(Curl_ssl_tls13_ciphersuites()) {
[ ]   234        /* set preferred list of TLS 1.3 cipher suites for proxy */
[ ]   235        result = Curl_setstropt(&data->set.str[STRING_SSL_CIPHER13_LIST_PROXY],
[ ]   236                                va_arg(param, char *));
[ ]   237      }
[ ]   238      else
[ ]   239        return CURLE_NOT_BUILT_IN;
[ ]   240      break;
[ ]   241  #endif
[ ]   242    case CURLOPT_RANDOM_FILE:
[ ]   243      break;
[ ]   244    case CURLOPT_EGDSOCKET:
[ ]   245      break;
[ ]   246    case CURLOPT_MAXCONNECTS:
[ ]   247      /*
[ ]   248       * Set the absolute number of maximum simultaneous alive connection that
[ ]   249       * libcurl is allowed to have.
[ ]   250       */
[ ]   251      arg = va_arg(param, long);
[ ]   252      if(arg < 0)
[ ]   253        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   254      data->set.maxconnects = arg;
[ ]   255      break;
[ ]   256    case CURLOPT_FORBID_REUSE:
[ ]   257      /*
[ ]   258       * When this transfer is done, it must not be left to be reused by a
[ ]   259       * subsequent transfer but shall be closed immediately.
[ ]   260       */
[ ]   261      data->set.reuse_forbid = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   262      break;
[ ]   263    case CURLOPT_FRESH_CONNECT:
[ ]   264      /*
[ ]   265       * This transfer shall not use a previously cached connection but
[ ]   266       * should be made with a fresh new connect!
[ ]   267       */
[ ]   268      data->set.reuse_fresh = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   269      break;
[ ]   270    case CURLOPT_VERBOSE:
[ ]   271      /*
[ ]   272       * Verbose means infof() calls that give a lot of information about
[ ]   273       * the connection and transfer procedures as well as internal choices.
[ ]   274       */
[ ]   275      data->set.verbose = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   276      break;
[ ]   277    case CURLOPT_HEADER:
[ ]   278      /*
[ ]   279       * Set to include the header in the general data output stream.
[ ]   280       */
[ ]   281      data->set.include_header = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   282      break;
[ ]   283    case CURLOPT_NOPROGRESS:
[ ]   284      /*
[ ]   285       * Shut off the internal supported progress meter
[ ]   286       */
[ ]   287      data->set.hide_progress = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   288      if(data->set.hide_progress)
[ ]   289        data->progress.flags |= PGRS_HIDE;
[ ]   290      else
[ ]   291        data->progress.flags &= ~PGRS_HIDE;
[ ]   292      break;
[ ]   293    case CURLOPT_NOBODY:
[ ]   294      /*
[ ]   295       * Do not include the body part in the output data stream.
[ ]   296       */
[ ]   297      data->set.opt_no_body = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   298  #ifndef CURL_DISABLE_HTTP
[ ]   299      if(data->set.opt_no_body)
[ ]   300        /* in HTTP lingo, no body means using the HEAD request... */
[ ]   301        data->set.method = HTTPREQ_HEAD;
[ ]   302      else if(data->set.method == HTTPREQ_HEAD)
[ ]   303        data->set.method = HTTPREQ_GET;
[ ]   304  #endif
[ ]   305      break;
[ ]   306    case CURLOPT_FAILONERROR:
[ ]   307      /*
[ ]   308       * Don't output the >=400 error code HTML-page, but instead only
[ ]   309       * return error.
[ ]   310       */
[ ]   311      data->set.http_fail_on_error = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   312      break;
[ ]   313    case CURLOPT_KEEP_SENDING_ON_ERROR:
[ ]   314      data->set.http_keep_sending_on_error = (0 != va_arg(param, long)) ?
[ ]   315        TRUE : FALSE;
[ ]   316      break;
[ ]   317    case CURLOPT_UPLOAD:
[ ]   318    case CURLOPT_PUT:
[ ]   319      /*
[ ]   320       * We want to sent data to the remote host. If this is HTTP, that equals
[ ]   321       * using the PUT request.
[ ]   322       */
[ ]   323      data->set.upload = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   324      if(data->set.upload) {
[ ]   325        /* If this is HTTP, PUT is what's needed to "upload" */
[ ]   326        data->set.method = HTTPREQ_PUT;
[ ]   327        data->set.opt_no_body = FALSE; /* this is implied */
[ ]   328      }
[ ]   329      else
[ ]   330        /* In HTTP, the opposite of upload is GET (unless NOBODY is true as
[ ]   331           then this can be changed to HEAD later on) */
[ ]   332        data->set.method = HTTPREQ_GET;
[ ]   333      break;
[ ]   334    case CURLOPT_REQUEST_TARGET:
[ ]   335      result = Curl_setstropt(&data->set.str[STRING_TARGET],
[ ]   336                              va_arg(param, char *));
[ ]   337      break;
[ ]   338    case CURLOPT_FILETIME:
[ ]   339      /*
[ ]   340       * Try to get the file time of the remote document. The time will
[ ]   341       * later (possibly) become available using curl_easy_getinfo().
[ ]   342       */
[ ]   343      data->set.get_filetime = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   344      break;
[L]   345    case CURLOPT_SERVER_RESPONSE_TIMEOUT:
[ ]   346      /*
[ ]   347       * Option that specifies how quickly a server response must be obtained
[ ]   348       * before it is considered failure. For pingpong protocols.
[ ]   349       */
[L]   350      arg = va_arg(param, long);
[L]   351      if((arg >= 0) && (arg <= (INT_MAX/1000)))
[L]   352        data->set.server_response_timeout = (unsigned int)arg * 1000;
[ ]   353      else
[ ]   354        return CURLE_BAD_FUNCTION_ARGUMENT;
[L]   355      break;
[L]   356  #ifndef CURL_DISABLE_TFTP
[L]   357    case CURLOPT_TFTP_NO_OPTIONS:
[ ]   358      /*
[ ]   359       * Option that prevents libcurl from sending TFTP option requests to the
[ ]   360       * server.
[ ]   361       */
[ ]   362      data->set.tftp_no_options = va_arg(param, long) != 0;
[ ]   363      break;
[ ]   364    case CURLOPT_TFTP_BLKSIZE:
[ ]   365      /*
[ ]   366       * TFTP option that specifies the block size to use for data transmission.
[ ]   367       */
[ ]   368      arg = va_arg(param, long);
[ ]   369      if(arg < 0)
[ ]   370        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   371      data->set.tftp_blksize = arg;
[ ]   372      break;
[ ]   373  #endif
[ ]   374  #ifndef CURL_DISABLE_NETRC
[ ]   375    case CURLOPT_NETRC:
[ ]   376      /*
[ ]   377       * Parse the $HOME/.netrc file
[ ]   378       */
[ ]   379      arg = va_arg(param, long);
[ ]   380      if((arg < CURL_NETRC_IGNORED) || (arg >= CURL_NETRC_LAST))
[ ]   381        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   382      data->set.use_netrc = (unsigned char)arg;
[ ]   383      break;
[L]   384    case CURLOPT_NETRC_FILE:
[ ]   385      /*
[ ]   386       * Use this file instead of the $HOME/.netrc file
[ ]   387       */
[L]   388      result = Curl_setstropt(&data->set.str[STRING_NETRC_FILE],
[L]   389                              va_arg(param, char *));
[L]   390      break;
[ ]   391  #endif
[ ]   392    case CURLOPT_TRANSFERTEXT:
[ ]   393      /*
[ ]   394       * This option was previously named 'FTPASCII'. Renamed to work with
[ ]   395       * more protocols than merely FTP.
[ ]   396       *
[ ]   397       * Transfer using ASCII (instead of BINARY).
[ ]   398       */
[ ]   399      data->set.prefer_ascii = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   400      break;
[ ]   401    case CURLOPT_TIMECONDITION:
[ ]   402      /*
[ ]   403       * Set HTTP time condition. This must be one of the defines in the
[ ]   404       * curl/curl.h header file.
[ ]   405       */
[ ]   406      arg = va_arg(param, long);
[ ]   407      if((arg < CURL_TIMECOND_NONE) || (arg >= CURL_TIMECOND_LAST))
[ ]   408        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   409      data->set.timecondition = (curl_TimeCond)arg;
[ ]   410      break;
[ ]   411    case CURLOPT_TIMEVALUE:
[ ]   412      /*
[ ]   413       * This is the value to compare with the remote document with the
[ ]   414       * method set with CURLOPT_TIMECONDITION
[ ]   415       */
[ ]   416      data->set.timevalue = (time_t)va_arg(param, long);
[ ]   417      break;
[ ]   418  
[ ]   419    case CURLOPT_TIMEVALUE_LARGE:
[ ]   420      /*
[ ]   421       * This is the value to compare with the remote document with the
[ ]   422       * method set with CURLOPT_TIMECONDITION
[ ]   423       */
[ ]   424      data->set.timevalue = (time_t)va_arg(param, curl_off_t);
[ ]   425      break;
[ ]   426  
[ ]   427    case CURLOPT_SSLVERSION:
[ ]   428  #ifndef CURL_DISABLE_PROXY
[ ]   429    case CURLOPT_PROXY_SSLVERSION:
[ ]   430  #endif
[ ]   431      /*
[ ]   432       * Set explicit SSL version to try to connect with, as some SSL
[ ]   433       * implementations are lame.
[ ]   434       */
[ ]   435  #ifdef USE_SSL
[ ]   436      {
[ ]   437        long version, version_max;
[ ]   438        struct ssl_primary_config *primary = &data->set.ssl.primary;
[ ]   439  #ifndef CURL_DISABLE_PROXY
[ ]   440        if(option != CURLOPT_SSLVERSION)
[ ]   441          primary = &data->set.proxy_ssl.primary;
[ ]   442  #endif
[ ]   443  
[ ]   444        arg = va_arg(param, long);
[ ]   445  
[ ]   446        version = C_SSLVERSION_VALUE(arg);
[ ]   447        version_max = C_SSLVERSION_MAX_VALUE(arg);
[ ]   448  
[ ]   449        if(version < CURL_SSLVERSION_DEFAULT ||
[ ]   450           version == CURL_SSLVERSION_SSLv2 ||
[ ]   451           version == CURL_SSLVERSION_SSLv3 ||
[ ]   452           version >= CURL_SSLVERSION_LAST ||
[ ]   453           version_max < CURL_SSLVERSION_MAX_NONE ||
[ ]   454           version_max >= CURL_SSLVERSION_MAX_LAST)
[ ]   455          return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   456  
[ ]   457        primary->version = version;
[ ]   458        primary->version_max = version_max;
[ ]   459      }
[ ]   460  #else
[ ]   461      result = CURLE_NOT_BUILT_IN;
[ ]   462  #endif
[ ]   463      break;
[ ]   464  
[ ]   465      /* MQTT "borrows" some of the HTTP options */
[ ]   466  #if !defined(CURL_DISABLE_HTTP) || !defined(CURL_DISABLE_MQTT)
[ ]   467    case CURLOPT_COPYPOSTFIELDS:
[ ]   468      /*
[ ]   469       * A string with POST data. Makes curl HTTP POST. Even if it is NULL.
[ ]   470       * If needed, CURLOPT_POSTFIELDSIZE must have been set prior to
[ ]   471       *  CURLOPT_COPYPOSTFIELDS and not altered later.
[ ]   472       */
[ ]   473      argptr = va_arg(param, char *);
[ ]   474  
[ ]   475      if(!argptr || data->set.postfieldsize == -1)
[ ]   476        result = Curl_setstropt(&data->set.str[STRING_COPYPOSTFIELDS], argptr);
[ ]   477      else {
[ ]   478        /*
[ ]   479         *  Check that requested length does not overflow the size_t type.
[ ]   480         */
[ ]   481  
[ ]   482        if((data->set.postfieldsize < 0) ||
[ ]   483           ((sizeof(curl_off_t) != sizeof(size_t)) &&
[ ]   484            (data->set.postfieldsize > (curl_off_t)((size_t)-1))))
[ ]   485          result = CURLE_OUT_OF_MEMORY;
[ ]   486        else {
[ ]   487          char *p;
[ ]   488  
[ ]   489          (void) Curl_setstropt(&data->set.str[STRING_COPYPOSTFIELDS], NULL);
[ ]   490  
[ ]   491          /* Allocate even when size == 0. This satisfies the need of possible
[ ]   492             later address compare to detect the COPYPOSTFIELDS mode, and
[ ]   493             to mark that postfields is used rather than read function or
[ ]   494             form data.
[ ]   495          */
[ ]   496          p = malloc((size_t)(data->set.postfieldsize?
[ ]   497                              data->set.postfieldsize:1));
[ ]   498  
[ ]   499          if(!p)
[ ]   500            result = CURLE_OUT_OF_MEMORY;
[ ]   501          else {
[ ]   502            if(data->set.postfieldsize)
[ ]   503              memcpy(p, argptr, (size_t)data->set.postfieldsize);
[ ]   504  
[ ]   505            data->set.str[STRING_COPYPOSTFIELDS] = p;
[ ]   506          }
[ ]   507        }
[ ]   508      }
[ ]   509  
[ ]   510      data->set.postfields = data->set.str[STRING_COPYPOSTFIELDS];
[ ]   511      data->set.method = HTTPREQ_POST;
[ ]   512      break;
[ ]   513  
[B]   514    case CURLOPT_POSTFIELDS:
[ ]   515      /*
[ ]   516       * Like above, but use static data instead of copying it.
[ ]   517       */
[B]   518      data->set.postfields = va_arg(param, void *);
[ ]   519      /* Release old copied data. */
[B]   520      (void) Curl_setstropt(&data->set.str[STRING_COPYPOSTFIELDS], NULL);
[B]   521      data->set.method = HTTPREQ_POST;
[B]   522      break;
[ ]   523  
[ ]   524    case CURLOPT_POSTFIELDSIZE:
[ ]   525      /*
[ ]   526       * The size of the POSTFIELD data to prevent libcurl to do strlen() to
[ ]   527       * figure it out. Enables binary posts.
[ ]   528       */
[ ]   529      bigsize = va_arg(param, long);
[ ]   530      if(bigsize < -1)
[ ]   531        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   532  
[ ]   533      if(data->set.postfieldsize < bigsize &&
[ ]   534         data->set.postfields == data->set.str[STRING_COPYPOSTFIELDS]) {
[ ]   535        /* Previous CURLOPT_COPYPOSTFIELDS is no longer valid. */
[ ]   536        (void) Curl_setstropt(&data->set.str[STRING_COPYPOSTFIELDS], NULL);
[ ]   537        data->set.postfields = NULL;
[ ]   538      }
[ ]   539  
[ ]   540      data->set.postfieldsize = bigsize;
[ ]   541      break;
[ ]   542  
[ ]   543    case CURLOPT_POSTFIELDSIZE_LARGE:
[ ]   544      /*
[ ]   545       * The size of the POSTFIELD data to prevent libcurl to do strlen() to
[ ]   546       * figure it out. Enables binary posts.
[ ]   547       */
[ ]   548      bigsize = va_arg(param, curl_off_t);
[ ]   549      if(bigsize < -1)
[ ]   550        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   551  
[ ]   552      if(data->set.postfieldsize < bigsize &&
[ ]   553         data->set.postfields == data->set.str[STRING_COPYPOSTFIELDS]) {
[ ]   554        /* Previous CURLOPT_COPYPOSTFIELDS is no longer valid. */
[ ]   555        (void) Curl_setstropt(&data->set.str[STRING_COPYPOSTFIELDS], NULL);
[ ]   556        data->set.postfields = NULL;
[ ]   557      }
[ ]   558  
[ ]   559      data->set.postfieldsize = bigsize;
[ ]   560      break;
[ ]   561  #endif
[ ]   562  #ifndef CURL_DISABLE_HTTP
[ ]   563    case CURLOPT_AUTOREFERER:
[ ]   564      /*
[ ]   565       * Switch on automatic referer that gets set if curl follows locations.
[ ]   566       */
[ ]   567      data->set.http_auto_referer = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   568      break;
[ ]   569  
[ ]   570    case CURLOPT_ACCEPT_ENCODING:
[ ]   571      /*
[ ]   572       * String to use at the value of Accept-Encoding header.
[ ]   573       *
[ ]   574       * If the encoding is set to "" we use an Accept-Encoding header that
[ ]   575       * encompasses all the encodings we support.
[ ]   576       * If the encoding is set to NULL we don't send an Accept-Encoding header
[ ]   577       * and ignore an received Content-Encoding header.
[ ]   578       *
[ ]   579       */
[ ]   580      argptr = va_arg(param, char *);
[ ]   581      if(argptr && !*argptr) {
[ ]   582        argptr = Curl_all_content_encodings();
[ ]   583        if(!argptr)
[ ]   584          result = CURLE_OUT_OF_MEMORY;
[ ]   585        else {
[ ]   586          result = Curl_setstropt(&data->set.str[STRING_ENCODING], argptr);
[ ]   587          free(argptr);
[ ]   588        }
[ ]   589      }
[ ]   590      else
[ ]   591        result = Curl_setstropt(&data->set.str[STRING_ENCODING], argptr);
[ ]   592      break;
[ ]   593  
[ ]   594    case CURLOPT_TRANSFER_ENCODING:
[ ]   595      data->set.http_transfer_encoding = (0 != va_arg(param, long)) ?
[ ]   596        TRUE : FALSE;
[ ]   597      break;
[ ]   598  
[ ]   599    case CURLOPT_FOLLOWLOCATION:
[ ]   600      /*
[ ]   601       * Follow Location: header hints on a HTTP-server.
[ ]   602       */
[ ]   603      data->set.http_follow_location = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   604      break;
[ ]   605  
[ ]   606    case CURLOPT_UNRESTRICTED_AUTH:
[ ]   607      /*
[ ]   608       * Send authentication (user+password) when following locations, even when
[ ]   609       * hostname changed.
[ ]   610       */
[ ]   611      data->set.allow_auth_to_other_hosts =
[ ]   612        (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   613      break;
[ ]   614  
[ ]   615    case CURLOPT_MAXREDIRS:
[ ]   616      /*
[ ]   617       * The maximum amount of hops you allow curl to follow Location:
[ ]   618       * headers. This should mostly be used to detect never-ending loops.
[ ]   619       */
[ ]   620      arg = va_arg(param, long);
[ ]   621      if(arg < -1)
[ ]   622        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   623      data->set.maxredirs = arg;
[ ]   624      break;
[ ]   625  
[ ]   626    case CURLOPT_POSTREDIR:
[ ]   627      /*
[ ]   628       * Set the behavior of POST when redirecting
[ ]   629       * CURL_REDIR_GET_ALL - POST is changed to GET after 301 and 302
[ ]   630       * CURL_REDIR_POST_301 - POST is kept as POST after 301
[ ]   631       * CURL_REDIR_POST_302 - POST is kept as POST after 302
[ ]   632       * CURL_REDIR_POST_303 - POST is kept as POST after 303
[ ]   633       * CURL_REDIR_POST_ALL - POST is kept as POST after 301, 302 and 303
[ ]   634       * other - POST is kept as POST after 301 and 302
[ ]   635       */
[ ]   636      arg = va_arg(param, long);
[ ]   637      if(arg < CURL_REDIR_GET_ALL)
[ ]   638        /* no return error on too high numbers since the bitmask could be
[ ]   639           extended in a future */
[ ]   640        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   641      data->set.keep_post = arg & CURL_REDIR_POST_ALL;
[ ]   642      break;
[ ]   643  
[ ]   644    case CURLOPT_POST:
[ ]   645      /* Does this option serve a purpose anymore? Yes it does, when
[ ]   646         CURLOPT_POSTFIELDS isn't used and the POST data is read off the
[ ]   647         callback! */
[ ]   648      if(va_arg(param, long)) {
[ ]   649        data->set.method = HTTPREQ_POST;
[ ]   650        data->set.opt_no_body = FALSE; /* this is implied */
[ ]   651      }
[ ]   652      else
[ ]   653        data->set.method = HTTPREQ_GET;
[ ]   654      data->set.upload = FALSE;
[ ]   655      break;
[ ]   656  
[ ]   657  #ifndef CURL_DISABLE_MIME
[L]   658    case CURLOPT_HTTPPOST:
[ ]   659      /*
[ ]   660       * Set to make us do HTTP POST
[ ]   661       */
[L]   662      data->set.httppost = va_arg(param, struct curl_httppost *);
[L]   663      data->set.method = HTTPREQ_POST_FORM;
[L]   664      data->set.opt_no_body = FALSE; /* this is implied */
[L]   665      break;
[ ]   666  #endif
[ ]   667  
[ ]   668    case CURLOPT_AWS_SIGV4:
[ ]   669      /*
[ ]   670       * String that is merged to some authentication
[ ]   671       * parameters are used by the algorithm.
[ ]   672       */
[ ]   673      result = Curl_setstropt(&data->set.str[STRING_AWS_SIGV4],
[ ]   674                              va_arg(param, char *));
[ ]   675      /*
[ ]   676       * Basic been set by default it need to be unset here
[ ]   677       */
[ ]   678      if(data->set.str[STRING_AWS_SIGV4])
[ ]   679        data->set.httpauth = CURLAUTH_AWS_SIGV4;
[ ]   680      break;
[ ]   681  
[ ]   682    case CURLOPT_REFERER:
[ ]   683      /*
[ ]   684       * String to set in the HTTP Referer: field.
[ ]   685       */
[ ]   686      if(data->state.referer_alloc) {
[ ]   687        Curl_safefree(data->state.referer);
[ ]   688        data->state.referer_alloc = FALSE;
[ ]   689      }
[ ]   690      result = Curl_setstropt(&data->set.str[STRING_SET_REFERER],
[ ]   691                              va_arg(param, char *));
[ ]   692      data->state.referer = data->set.str[STRING_SET_REFERER];
[ ]   693      break;
[ ]   694  
[ ]   695    case CURLOPT_USERAGENT:
[ ]   696      /*
[ ]   697       * String to use in the HTTP User-Agent field
[ ]   698       */
[ ]   699      result = Curl_setstropt(&data->set.str[STRING_USERAGENT],
[ ]   700                              va_arg(param, char *));
[ ]   701      break;
[ ]   702  
[ ]   703  #ifndef CURL_DISABLE_PROXY
[ ]   704    case CURLOPT_PROXYHEADER:
[ ]   705      /*
[ ]   706       * Set a list with proxy headers to use (or replace internals with)
[ ]   707       *
[ ]   708       * Since CURLOPT_HTTPHEADER was the only way to set HTTP headers for a
[ ]   709       * long time we remain doing it this way until CURLOPT_PROXYHEADER is
[ ]   710       * used. As soon as this option has been used, if set to anything but
[ ]   711       * NULL, custom headers for proxies are only picked from this list.
[ ]   712       *
[ ]   713       * Set this option to NULL to restore the previous behavior.
[ ]   714       */
[ ]   715      data->set.proxyheaders = va_arg(param, struct curl_slist *);
[ ]   716      break;
[ ]   717  #endif
[ ]   718    case CURLOPT_HEADEROPT:
[ ]   719      /*
[ ]   720       * Set header option.
[ ]   721       */
[ ]   722      arg = va_arg(param, long);
[ ]   723      data->set.sep_headers = (bool)((arg & CURLHEADER_SEPARATE)? TRUE: FALSE);
[ ]   724      break;
[ ]   725  
[ ]   726    case CURLOPT_HTTP200ALIASES:
[ ]   727      /*
[ ]   728       * Set a list of aliases for HTTP 200 in response header
[ ]   729       */
[ ]   730      data->set.http200aliases = va_arg(param, struct curl_slist *);
[ ]   731      break;
[ ]   732  
[ ]   733  #if !defined(CURL_DISABLE_COOKIES)
[L]   734    case CURLOPT_COOKIE:
[ ]   735      /*
[ ]   736       * Cookie string to send to the remote server in the request.
[ ]   737       */
[L]   738      result = Curl_setstropt(&data->set.str[STRING_COOKIE],
[L]   739                              va_arg(param, char *));
[L]   740      break;
[ ]   741  
[L]   742    case CURLOPT_COOKIEFILE:
[ ]   743      /*
[ ]   744       * Set cookie file to read and parse. Can be used multiple times.
[ ]   745       */
[L]   746      argptr = (char *)va_arg(param, void *);
[L]   747      if(argptr) {
[L]   748        struct curl_slist *cl;
[ ]   749        /* general protection against mistakes and abuse */
[L]   750        if(strlen(argptr) > CURL_MAX_INPUT_LENGTH)
[ ]   751          return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   752        /* append the cookie file name to the list of file names, and deal with
[ ]   753           them later */
[L]   754        cl = curl_slist_append(data->state.cookielist, argptr);
[L]   755        if(!cl) {
[ ]   756          curl_slist_free_all(data->state.cookielist);
[ ]   757          data->state.cookielist = NULL;
[ ]   758          return CURLE_OUT_OF_MEMORY;
[ ]   759        }
[L]   760        data->state.cookielist = cl; /* store the list for later use */
[L]   761      }
[ ]   762      else {
[ ]   763        /* clear the list of cookie files */
[ ]   764        curl_slist_free_all(data->state.cookielist);
[ ]   765        data->state.cookielist = NULL;
[ ]   766  
[ ]   767        if(!data->share || !data->share->cookies) {
[ ]   768          /* throw away all existing cookies if this isn't a shared cookie
[ ]   769             container */
[ ]   770          Curl_cookie_clearall(data->cookies);
[ ]   771          Curl_cookie_cleanup(data->cookies);
[ ]   772        }
[ ]   773        /* disable the cookie engine */
[ ]   774        data->cookies = NULL;
[ ]   775      }
[L]   776      break;
[ ]   777  
[L]   778    case CURLOPT_COOKIEJAR:
[ ]   779      /*
[ ]   780       * Set cookie file name to dump all cookies to when we're done.
[ ]   781       */
[L]   782    {
[L]   783      struct CookieInfo *newcookies;
[L]   784      result = Curl_setstropt(&data->set.str[STRING_COOKIEJAR],
[L]   785                              va_arg(param, char *));
[ ]   786  
[ ]   787      /*
[ ]   788       * Activate the cookie parser. This may or may not already
[ ]   789       * have been made.
[ ]   790       */
[L]   791      newcookies = Curl_cookie_init(data, NULL, data->cookies,
[L]   792                                    data->set.cookiesession);
[L]   793      if(!newcookies)
[ ]   794        result = CURLE_OUT_OF_MEMORY;
[L]   795      data->cookies = newcookies;
[L]   796    }
[L]   797    break;
[ ]   798  
[ ]   799    case CURLOPT_COOKIESESSION:
[ ]   800      /*
[ ]   801       * Set this option to TRUE to start a new "cookie session". It will
[ ]   802       * prevent the forthcoming read-cookies-from-file actions to accept
[ ]   803       * cookies that are marked as being session cookies, as they belong to a
[ ]   804       * previous session.
[ ]   805       *
[ ]   806       * In the original Netscape cookie spec, "session cookies" are cookies
[ ]   807       * with no expire date set. RFC2109 describes the same action if no
[ ]   808       * 'Max-Age' is set and RFC2965 includes the RFC2109 description and adds
[ ]   809       * a 'Discard' action that can enforce the discard even for cookies that
[ ]   810       * have a Max-Age.
[ ]   811       *
[ ]   812       * We run mostly with the original cookie spec, as hardly anyone implements
[ ]   813       * anything else.
[ ]   814       */
[ ]   815      data->set.cookiesession = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]   816      break;
[ ]   817  
[ ]   818    case CURLOPT_COOKIELIST:
[ ]   819      argptr = va_arg(param, char *);
[ ]   820  
[ ]   821      if(!argptr)
[ ]   822        break;
[ ]   823  
[ ]   824      if(strcasecompare(argptr, "ALL")) {
[ ]   825        /* clear all cookies */
[ ]   826        Curl_share_lock(data, CURL_LOCK_DATA_COOKIE, CURL_LOCK_ACCESS_SINGLE);
[ ]   827        Curl_cookie_clearall(data->cookies);
[ ]   828        Curl_share_unlock(data, CURL_LOCK_DATA_COOKIE);
[ ]   829      }
[ ]   830      else if(strcasecompare(argptr, "SESS")) {
[ ]   831        /* clear session cookies */
[ ]   832        Curl_share_lock(data, CURL_LOCK_DATA_COOKIE, CURL_LOCK_ACCESS_SINGLE);
[ ]   833        Curl_cookie_clearsess(data->cookies);
[ ]   834        Curl_share_unlock(data, CURL_LOCK_DATA_COOKIE);
[ ]   835      }
[ ]   836      else if(strcasecompare(argptr, "FLUSH")) {
[ ]   837        /* flush cookies to file, takes care of the locking */
[ ]   838        Curl_flush_cookies(data, FALSE);
[ ]   839      }
[ ]   840      else if(strcasecompare(argptr, "RELOAD")) {
[ ]   841        /* reload cookies from file */
[ ]   842        Curl_cookie_loadfiles(data);
[ ]   843        break;
[ ]   844      }
[ ]   845      else {
[ ]   846        if(!data->cookies)
[ ]   847          /* if cookie engine was not running, activate it */
[ ]   848          data->cookies = Curl_cookie_init(data, NULL, NULL, TRUE);
[ ]   849  
[ ]   850        /* general protection against mistakes and abuse */
[ ]   851        if(strlen(argptr) > CURL_MAX_INPUT_LENGTH)
[ ]   852          return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   853        argptr = strdup(argptr);
[ ]   854        if(!argptr || !data->cookies) {
[ ]   855          result = CURLE_OUT_OF_MEMORY;
[ ]   856          free(argptr);
[ ]   857        }
[ ]   858        else {
[ ]   859          Curl_share_lock(data, CURL_LOCK_DATA_COOKIE, CURL_LOCK_ACCESS_SINGLE);
[ ]   860  
[ ]   861          if(checkprefix("Set-Cookie:", argptr))
[ ]   862            /* HTTP Header format line */
[ ]   863            Curl_cookie_add(data, data->cookies, TRUE, FALSE, argptr + 11, NULL,
[ ]   864                            NULL, TRUE);
[ ]   865  
[ ]   866          else
[ ]   867            /* Netscape format line */
[ ]   868            Curl_cookie_add(data, data->cookies, FALSE, FALSE, argptr, NULL,
[ ]   869                            NULL, TRUE);
[ ]   870  
[ ]   871          Curl_share_unlock(data, CURL_LOCK_DATA_COOKIE);
[ ]   872          free(argptr);
[ ]   873        }
[ ]   874      }
[ ]   875  
[ ]   876      break;
[ ]   877  #endif /* !CURL_DISABLE_COOKIES */
[ ]   878  
[ ]   879    case CURLOPT_HTTPGET:
[ ]   880      /*
[ ]   881       * Set to force us do HTTP GET
[ ]   882       */
[ ]   883      if(va_arg(param, long)) {
[ ]   884        data->set.method = HTTPREQ_GET;
[ ]   885        data->set.upload = FALSE; /* switch off upload */
[ ]   886        data->set.opt_no_body = FALSE; /* this is implied */
[ ]   887      }
[ ]   888      break;
[ ]   889  
[ ]   890    case CURLOPT_HTTP_VERSION:
[ ]   891      /*
[ ]   892       * This sets a requested HTTP version to be used. The value is one of
[ ]   893       * the listed enums in curl/curl.h.
[ ]   894       */
[ ]   895      arg = va_arg(param, long);
[ ]   896      if(arg < CURL_HTTP_VERSION_NONE)
[ ]   897        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   898  #ifdef ENABLE_QUIC
[ ]   899      if(arg == CURL_HTTP_VERSION_3)
[ ]   900        ;
[ ]   901      else
[ ]   902  #endif
[ ]   903  #ifndef USE_HTTP2
[ ]   904      if(arg >= CURL_HTTP_VERSION_2)
[ ]   905        return CURLE_UNSUPPORTED_PROTOCOL;
[ ]   906  #else
[ ]   907      if(arg >= CURL_HTTP_VERSION_LAST)
[ ]   908        return CURLE_UNSUPPORTED_PROTOCOL;
[ ]   909      if(arg == CURL_HTTP_VERSION_NONE)
[ ]   910        arg = CURL_HTTP_VERSION_2TLS;
[ ]   911  #endif
[ ]   912      data->set.httpwant = (unsigned char)arg;
[ ]   913      break;
[ ]   914  
[ ]   915    case CURLOPT_EXPECT_100_TIMEOUT_MS:
[ ]   916      /*
[ ]   917       * Time to wait for a response to a HTTP request containing an
[ ]   918       * Expect: 100-continue header before sending the data anyway.
[ ]   919       */
[ ]   920      arg = va_arg(param, long);
[ ]   921      if(arg < 0)
[ ]   922        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   923      data->set.expect_100_timeout = arg;
[ ]   924      break;
[ ]   925  
[ ]   926    case CURLOPT_HTTP09_ALLOWED:
[ ]   927      arg = va_arg(param, unsigned long);
[ ]   928      if(arg > 1L)
[ ]   929        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   930  #ifdef USE_HYPER
[ ]   931      /* Hyper does not support HTTP/0.9 */
[ ]   932      if(arg)
[ ]   933        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]   934  #else
[ ]   935      data->set.http09_allowed = arg ? TRUE : FALSE;
[ ]   936  #endif
[ ]   937      break;
[ ]   938  #endif   /* CURL_DISABLE_HTTP */
[ ]   939  
[ ]   940  #if !defined(CURL_DISABLE_HTTP) || !defined(CURL_DISABLE_SMTP) ||       \
[ ]   941      !defined(CURL_DISABLE_IMAP)
[ ]   942  # if !defined(CURL_DISABLE_HTTP) || !defined(CURL_DISABLE_MIME)
[L]   943    case CURLOPT_HTTPHEADER:
[ ]   944      /*
[ ]   945       * Set a list with HTTP headers to use (or replace internals with)
[ ]   946       */
[L]   947      data->set.headers = va_arg(param, struct curl_slist *);
[L]   948      break;
[ ]   949  # endif
[ ]   950  
[ ]   951  # ifndef CURL_DISABLE_MIME
[ ]   952    case CURLOPT_MIMEPOST:
[ ]   953      /*
[ ]   954       * Set to make us do MIME POST
[ ]   955       */
[ ]   956      result = Curl_mime_set_subparts(&data->set.mimepost,
[ ]   957                                      va_arg(param, curl_mime *), FALSE);
[ ]   958      if(!result) {
[ ]   959        data->set.method = HTTPREQ_POST_MIME;
[ ]   960        data->set.opt_no_body = FALSE; /* this is implied */
[ ]   961      }
[ ]   962      break;
[ ]   963  
[ ]   964    case CURLOPT_MIME_OPTIONS:
[ ]   965      data->set.mime_options = (unsigned int)va_arg(param, long);
[ ]   966      break;
[ ]   967  # endif
[ ]   968  #endif
[ ]   969  
[ ]   970    case CURLOPT_HTTPAUTH:
[ ]   971      /*
[ ]   972       * Set HTTP Authentication type BITMASK.
[ ]   973       */
[ ]   974    {
[ ]   975      int bitcheck;
[ ]   976      bool authbits;
[ ]   977      unsigned long auth = va_arg(param, unsigned long);
[ ]   978  
[ ]   979      if(auth == CURLAUTH_NONE) {
[ ]   980        data->set.httpauth = auth;
[ ]   981        break;
[ ]   982      }
[ ]   983  
[ ]   984      /* the DIGEST_IE bit is only used to set a special marker, for all the
[ ]   985         rest we need to handle it as normal DIGEST */
[ ]   986      data->state.authhost.iestyle =
[ ]   987        (bool)((auth & CURLAUTH_DIGEST_IE) ? TRUE : FALSE);
[ ]   988  
[ ]   989      if(auth & CURLAUTH_DIGEST_IE) {
[ ]   990        auth |= CURLAUTH_DIGEST; /* set standard digest bit */
[ ]   991        auth &= ~CURLAUTH_DIGEST_IE; /* unset ie digest bit */
[ ]   992      }
[ ]   993  
[ ]   994      /* switch off bits we can't support */
[ ]   995  #ifndef USE_NTLM
[ ]   996      auth &= ~CURLAUTH_NTLM;    /* no NTLM support */
[ ]   997      auth &= ~CURLAUTH_NTLM_WB; /* no NTLM_WB support */
[ ]   998  #elif !defined(NTLM_WB_ENABLED)
[ ]   999      auth &= ~CURLAUTH_NTLM_WB; /* no NTLM_WB support */
[ ]  1000  #endif
[ ]  1001  #ifndef USE_SPNEGO
[ ]  1002      auth &= ~CURLAUTH_NEGOTIATE; /* no Negotiate (SPNEGO) auth without
[ ]  1003                                      GSS-API or SSPI */
[ ]  1004  #endif
[ ]  1005  
[ ]  1006      /* check if any auth bit lower than CURLAUTH_ONLY is still set */
[ ]  1007      bitcheck = 0;
[ ]  1008      authbits = FALSE;
[ ]  1009      while(bitcheck < 31) {
[ ]  1010        if(auth & (1UL << bitcheck++)) {
[ ]  1011          authbits = TRUE;
[ ]  1012          break;
[ ]  1013        }
[ ]  1014      }
[ ]  1015      if(!authbits)
[ ]  1016        return CURLE_NOT_BUILT_IN; /* no supported types left! */
[ ]  1017  
[ ]  1018      data->set.httpauth = auth;
[ ]  1019    }
[ ]  1020    break;
[ ]  1021  
[L]  1022    case CURLOPT_CUSTOMREQUEST:
[ ]  1023      /*
[ ]  1024       * Set a custom string to use as request
[ ]  1025       */
[L]  1026      result = Curl_setstropt(&data->set.str[STRING_CUSTOMREQUEST],
[L]  1027                              va_arg(param, char *));
[ ]  1028  
[ ]  1029      /* we don't set
[ ]  1030         data->set.method = HTTPREQ_CUSTOM;
[ ]  1031         here, we continue as if we were using the already set type
[ ]  1032         and this just changes the actual request keyword */
[L]  1033      break;
[ ]  1034  
[ ]  1035  #ifndef CURL_DISABLE_PROXY
[ ]  1036    case CURLOPT_HTTPPROXYTUNNEL:
[ ]  1037      /*
[ ]  1038       * Tunnel operations through the proxy instead of normal proxy use
[ ]  1039       */
[ ]  1040      data->set.tunnel_thru_httpproxy = (0 != va_arg(param, long)) ?
[ ]  1041        TRUE : FALSE;
[ ]  1042      break;
[ ]  1043  
[ ]  1044    case CURLOPT_PROXYPORT:
[ ]  1045      /*
[ ]  1046       * Explicitly set HTTP proxy port number.
[ ]  1047       */
[ ]  1048      arg = va_arg(param, long);
[ ]  1049      if((arg < 0) || (arg > 65535))
[ ]  1050        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1051      data->set.proxyport = arg;
[ ]  1052      break;
[ ]  1053  
[ ]  1054    case CURLOPT_PROXYAUTH:
[ ]  1055      /*
[ ]  1056       * Set HTTP Authentication type BITMASK.
[ ]  1057       */
[ ]  1058    {
[ ]  1059      int bitcheck;
[ ]  1060      bool authbits;
[ ]  1061      unsigned long auth = va_arg(param, unsigned long);
[ ]  1062  
[ ]  1063      if(auth == CURLAUTH_NONE) {
[ ]  1064        data->set.proxyauth = auth;
[ ]  1065        break;
[ ]  1066      }
[ ]  1067  
[ ]  1068      /* the DIGEST_IE bit is only used to set a special marker, for all the
[ ]  1069         rest we need to handle it as normal DIGEST */
[ ]  1070      data->state.authproxy.iestyle =
[ ]  1071        (bool)((auth & CURLAUTH_DIGEST_IE) ? TRUE : FALSE);
[ ]  1072  
[ ]  1073      if(auth & CURLAUTH_DIGEST_IE) {
[ ]  1074        auth |= CURLAUTH_DIGEST; /* set standard digest bit */
[ ]  1075        auth &= ~CURLAUTH_DIGEST_IE; /* unset ie digest bit */
[ ]  1076      }
[ ]  1077      /* switch off bits we can't support */
[ ]  1078  #ifndef USE_NTLM
[ ]  1079      auth &= ~CURLAUTH_NTLM;    /* no NTLM support */
[ ]  1080      auth &= ~CURLAUTH_NTLM_WB; /* no NTLM_WB support */
[ ]  1081  #elif !defined(NTLM_WB_ENABLED)
[ ]  1082      auth &= ~CURLAUTH_NTLM_WB; /* no NTLM_WB support */
[ ]  1083  #endif
[ ]  1084  #ifndef USE_SPNEGO
[ ]  1085      auth &= ~CURLAUTH_NEGOTIATE; /* no Negotiate (SPNEGO) auth without
[ ]  1086                                      GSS-API or SSPI */
[ ]  1087  #endif
[ ]  1088  
[ ]  1089      /* check if any auth bit lower than CURLAUTH_ONLY is still set */
[ ]  1090      bitcheck = 0;
[ ]  1091      authbits = FALSE;
[ ]  1092      while(bitcheck < 31) {
[ ]  1093        if(auth & (1UL << bitcheck++)) {
[ ]  1094          authbits = TRUE;
[ ]  1095          break;
[ ]  1096        }
[ ]  1097      }
[ ]  1098      if(!authbits)
[ ]  1099        return CURLE_NOT_BUILT_IN; /* no supported types left! */
[ ]  1100  
[ ]  1101      data->set.proxyauth = auth;
[ ]  1102    }
[ ]  1103    break;
[ ]  1104  
[ ]  1105    case CURLOPT_PROXY:
[ ]  1106      /*
[ ]  1107       * Set proxy server:port to use as proxy.
[ ]  1108       *
[ ]  1109       * If the proxy is set to "" (and CURLOPT_SOCKS_PROXY is set to "" or NULL)
[ ]  1110       * we explicitly say that we don't want to use a proxy
[ ]  1111       * (even though there might be environment variables saying so).
[ ]  1112       *
[ ]  1113       * Setting it to NULL, means no proxy but allows the environment variables
[ ]  1114       * to decide for us (if CURLOPT_SOCKS_PROXY setting it to NULL).
[ ]  1115       */
[ ]  1116      result = Curl_setstropt(&data->set.str[STRING_PROXY],
[ ]  1117                              va_arg(param, char *));
[ ]  1118      break;
[ ]  1119  
[ ]  1120    case CURLOPT_PRE_PROXY:
[ ]  1121      /*
[ ]  1122       * Set proxy server:port to use as SOCKS proxy.
[ ]  1123       *
[ ]  1124       * If the proxy is set to "" or NULL we explicitly say that we don't want
[ ]  1125       * to use the socks proxy.
[ ]  1126       */
[ ]  1127      result = Curl_setstropt(&data->set.str[STRING_PRE_PROXY],
[ ]  1128                              va_arg(param, char *));
[ ]  1129      break;
[ ]  1130  
[ ]  1131    case CURLOPT_PROXYTYPE:
[ ]  1132      /*
[ ]  1133       * Set proxy type. HTTP/HTTP_1_0/SOCKS4/SOCKS4a/SOCKS5/SOCKS5_HOSTNAME
[ ]  1134       */
[ ]  1135      arg = va_arg(param, long);
[ ]  1136      if((arg < CURLPROXY_HTTP) || (arg > CURLPROXY_SOCKS5_HOSTNAME))
[ ]  1137        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1138      data->set.proxytype = (curl_proxytype)arg;
[ ]  1139      break;
[ ]  1140  
[ ]  1141    case CURLOPT_PROXY_TRANSFER_MODE:
[ ]  1142      /*
[ ]  1143       * set transfer mode (;type=<a|i>) when doing FTP via an HTTP proxy
[ ]  1144       */
[ ]  1145      switch(va_arg(param, long)) {
[ ]  1146      case 0:
[ ]  1147        data->set.proxy_transfer_mode = FALSE;
[ ]  1148        break;
[ ]  1149      case 1:
[ ]  1150        data->set.proxy_transfer_mode = TRUE;
[ ]  1151        break;
[ ]  1152      default:
[ ]  1153        /* reserve other values for future use */
[ ]  1154        result = CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1155        break;
[ ]  1156      }
[ ]  1157      break;
[ ]  1158  
[ ]  1159    case CURLOPT_SOCKS5_AUTH:
[ ]  1160      data->set.socks5auth = va_arg(param, unsigned long);
[ ]  1161      if(data->set.socks5auth & ~(CURLAUTH_BASIC | CURLAUTH_GSSAPI))
[ ]  1162        result = CURLE_NOT_BUILT_IN;
[ ]  1163      break;
[ ]  1164  #endif   /* CURL_DISABLE_PROXY */
[ ]  1165  
[ ]  1166  #if defined(HAVE_GSSAPI) || defined(USE_WINDOWS_SSPI)
[ ]  1167    case CURLOPT_SOCKS5_GSSAPI_NEC:
[ ]  1168      /*
[ ]  1169       * Set flag for NEC SOCK5 support
[ ]  1170       */
[ ]  1171      data->set.socks5_gssapi_nec = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  1172      break;
[ ]  1173  #endif
[ ]  1174  #ifndef CURL_DISABLE_PROXY
[ ]  1175    case CURLOPT_SOCKS5_GSSAPI_SERVICE:
[ ]  1176    case CURLOPT_PROXY_SERVICE_NAME:
[ ]  1177      /*
[ ]  1178       * Set proxy authentication service name for Kerberos 5 and SPNEGO
[ ]  1179       */
[ ]  1180      result = Curl_setstropt(&data->set.str[STRING_PROXY_SERVICE_NAME],
[ ]  1181                              va_arg(param, char *));
[ ]  1182      break;
[ ]  1183  #endif
[ ]  1184    case CURLOPT_SERVICE_NAME:
[ ]  1185      /*
[ ]  1186       * Set authentication service name for DIGEST-MD5, Kerberos 5 and SPNEGO
[ ]  1187       */
[ ]  1188      result = Curl_setstropt(&data->set.str[STRING_SERVICE_NAME],
[ ]  1189                              va_arg(param, char *));
[ ]  1190      break;
[ ]  1191  
[ ]  1192    case CURLOPT_HEADERDATA:
[ ]  1193      /*
[ ]  1194       * Custom pointer to pass the header write callback function
[ ]  1195       */
[ ]  1196      data->set.writeheader = (void *)va_arg(param, void *);
[ ]  1197      break;
[ ]  1198    case CURLOPT_ERRORBUFFER:
[ ]  1199      /*
[ ]  1200       * Error buffer provided by the caller to get the human readable
[ ]  1201       * error string in.
[ ]  1202       */
[ ]  1203      data->set.errorbuffer = va_arg(param, char *);
[ ]  1204      break;
[L]  1205    case CURLOPT_WRITEDATA:
[ ]  1206      /*
[ ]  1207       * FILE pointer to write to. Or possibly
[ ]  1208       * used as argument to the write callback.
[ ]  1209       */
[L]  1210      data->set.out = va_arg(param, void *);
[L]  1211      break;
[ ]  1212  
[ ]  1213    case CURLOPT_DIRLISTONLY:
[ ]  1214      /*
[ ]  1215       * An option that changes the command to one that asks for a list only, no
[ ]  1216       * file info details. Used for FTP, POP3 and SFTP.
[ ]  1217       */
[ ]  1218      data->set.list_only = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  1219      break;
[ ]  1220  
[ ]  1221    case CURLOPT_APPEND:
[ ]  1222      /*
[ ]  1223       * We want to upload and append to an existing file. Used for FTP and
[ ]  1224       * SFTP.
[ ]  1225       */
[ ]  1226      data->set.remote_append = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  1227      break;
[ ]  1228  
[ ]  1229  #ifndef CURL_DISABLE_FTP
[ ]  1230    case CURLOPT_FTP_FILEMETHOD:
[ ]  1231      /*
[ ]  1232       * How do access files over FTP.
[ ]  1233       */
[ ]  1234      arg = va_arg(param, long);
[ ]  1235      if((arg < CURLFTPMETHOD_DEFAULT) || (arg >= CURLFTPMETHOD_LAST))
[ ]  1236        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1237      data->set.ftp_filemethod = (curl_ftpfile)arg;
[ ]  1238      break;
[ ]  1239    case CURLOPT_FTPPORT:
[ ]  1240      /*
[ ]  1241       * Use FTP PORT, this also specifies which IP address to use
[ ]  1242       */
[ ]  1243      result = Curl_setstropt(&data->set.str[STRING_FTPPORT],
[ ]  1244                              va_arg(param, char *));
[ ]  1245      data->set.ftp_use_port = (data->set.str[STRING_FTPPORT]) ? TRUE : FALSE;
[ ]  1246      break;
[ ]  1247  
[ ]  1248    case CURLOPT_FTP_USE_EPRT:
[ ]  1249      data->set.ftp_use_eprt = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  1250      break;
[ ]  1251  
[ ]  1252    case CURLOPT_FTP_USE_EPSV:
[ ]  1253      data->set.ftp_use_epsv = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  1254      break;
[ ]  1255  
[ ]  1256    case CURLOPT_FTP_USE_PRET:
[ ]  1257      data->set.ftp_use_pret = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  1258      break;
[ ]  1259  
[ ]  1260    case CURLOPT_FTP_SSL_CCC:
[ ]  1261      arg = va_arg(param, long);
[ ]  1262      if((arg < CURLFTPSSL_CCC_NONE) || (arg >= CURLFTPSSL_CCC_LAST))
[ ]  1263        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1264      data->set.ftp_ccc = (curl_ftpccc)arg;
[ ]  1265      break;
[ ]  1266  
[ ]  1267    case CURLOPT_FTP_SKIP_PASV_IP:
[ ]  1268      /*
[ ]  1269       * Enable or disable FTP_SKIP_PASV_IP, which will disable/enable the
[ ]  1270       * bypass of the IP address in PASV responses.
[ ]  1271       */
[ ]  1272      data->set.ftp_skip_ip = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  1273      break;
[ ]  1274  
[ ]  1275    case CURLOPT_FTP_ACCOUNT:
[ ]  1276      result = Curl_setstropt(&data->set.str[STRING_FTP_ACCOUNT],
[ ]  1277                              va_arg(param, char *));
[ ]  1278      break;
[ ]  1279  
[ ]  1280    case CURLOPT_FTP_ALTERNATIVE_TO_USER:
[ ]  1281      result = Curl_setstropt(&data->set.str[STRING_FTP_ALTERNATIVE_TO_USER],
[ ]  1282                              va_arg(param, char *));
[ ]  1283      break;
[ ]  1284  
[ ]  1285    case CURLOPT_FTPSSLAUTH:
[ ]  1286      /*
[ ]  1287       * Set a specific auth for FTP-SSL transfers.
[ ]  1288       */
[ ]  1289      arg = va_arg(param, long);
[ ]  1290      if((arg < CURLFTPAUTH_DEFAULT) || (arg >= CURLFTPAUTH_LAST))
[ ]  1291        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1292      data->set.ftpsslauth = (curl_ftpauth)arg;
[ ]  1293      break;
[ ]  1294    case CURLOPT_KRBLEVEL:
[ ]  1295      /*
[ ]  1296       * A string that defines the kerberos security level.
[ ]  1297       */
[ ]  1298      result = Curl_setstropt(&data->set.str[STRING_KRB_LEVEL],
[ ]  1299                              va_arg(param, char *));
[ ]  1300      data->set.krb = (data->set.str[STRING_KRB_LEVEL]) ? TRUE : FALSE;
[ ]  1301      break;
[ ]  1302  #endif
[ ]  1303    case CURLOPT_FTP_CREATE_MISSING_DIRS:
[ ]  1304      /*
[ ]  1305       * An FTP/SFTP option that modifies an upload to create missing
[ ]  1306       * directories on the server.
[ ]  1307       */
[ ]  1308      arg = va_arg(param, long);
[ ]  1309      /* reserve other values for future use */
[ ]  1310      if((arg < CURLFTP_CREATE_DIR_NONE) ||
[ ]  1311         (arg > CURLFTP_CREATE_DIR_RETRY))
[ ]  1312        result = CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1313      else
[ ]  1314        data->set.ftp_create_missing_dirs = (unsigned char)arg;
[ ]  1315      break;
[L]  1316    case CURLOPT_READDATA:
[ ]  1317      /*
[ ]  1318       * FILE pointer to read the file to be uploaded from. Or possibly
[ ]  1319       * used as argument to the read callback.
[ ]  1320       */
[L]  1321      data->set.in_set = va_arg(param, void *);
[L]  1322      break;
[ ]  1323    case CURLOPT_INFILESIZE:
[ ]  1324      /*
[ ]  1325       * If known, this should inform curl about the file size of the
[ ]  1326       * to-be-uploaded file.
[ ]  1327       */
[ ]  1328      arg = va_arg(param, long);
[ ]  1329      if(arg < -1)
[ ]  1330        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1331      data->set.filesize = arg;
[ ]  1332      break;
[ ]  1333    case CURLOPT_INFILESIZE_LARGE:
[ ]  1334      /*
[ ]  1335       * If known, this should inform curl about the file size of the
[ ]  1336       * to-be-uploaded file.
[ ]  1337       */
[ ]  1338      bigsize = va_arg(param, curl_off_t);
[ ]  1339      if(bigsize < -1)
[ ]  1340        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1341      data->set.filesize = bigsize;
[ ]  1342      break;
[ ]  1343    case CURLOPT_LOW_SPEED_LIMIT:
[ ]  1344      /*
[ ]  1345       * The low speed limit that if transfers are below this for
[ ]  1346       * CURLOPT_LOW_SPEED_TIME, the transfer is aborted.
[ ]  1347       */
[ ]  1348      arg = va_arg(param, long);
[ ]  1349      if(arg < 0)
[ ]  1350        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1351      data->set.low_speed_limit = arg;
[ ]  1352      break;
[ ]  1353    case CURLOPT_MAX_SEND_SPEED_LARGE:
[ ]  1354      /*
[ ]  1355       * When transfer uploads are faster then CURLOPT_MAX_SEND_SPEED_LARGE
[ ]  1356       * bytes per second the transfer is throttled..
[ ]  1357       */
[ ]  1358      bigsize = va_arg(param, curl_off_t);
[ ]  1359      if(bigsize < 0)
[ ]  1360        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1361      data->set.max_send_speed = bigsize;
[ ]  1362      break;
[ ]  1363    case CURLOPT_MAX_RECV_SPEED_LARGE:
[ ]  1364      /*
[ ]  1365       * When receiving data faster than CURLOPT_MAX_RECV_SPEED_LARGE bytes per
[ ]  1366       * second the transfer is throttled..
[ ]  1367       */
[ ]  1368      bigsize = va_arg(param, curl_off_t);
[ ]  1369      if(bigsize < 0)
[ ]  1370        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1371      data->set.max_recv_speed = bigsize;
[ ]  1372      break;
[ ]  1373    case CURLOPT_LOW_SPEED_TIME:
[ ]  1374      /*
[ ]  1375       * The low speed time that if transfers are below the set
[ ]  1376       * CURLOPT_LOW_SPEED_LIMIT during this time, the transfer is aborted.
[ ]  1377       */
[ ]  1378      arg = va_arg(param, long);
[ ]  1379      if(arg < 0)
[ ]  1380        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1381      data->set.low_speed_time = arg;
[ ]  1382      break;
[ ]  1383    case CURLOPT_CURLU:
[ ]  1384      /*
[ ]  1385       * pass CURLU to set URL
[ ]  1386       */
[ ]  1387      data->set.uh = va_arg(param, CURLU *);
[ ]  1388      break;
[B]  1389    case CURLOPT_URL:
[ ]  1390      /*
[ ]  1391       * The URL to fetch.
[ ]  1392       */
[B]  1393      if(data->state.url_alloc) {
[ ]  1394        /* the already set URL is allocated, free it first! */
[ ]  1395        Curl_safefree(data->state.url);
[ ]  1396        data->state.url_alloc = FALSE;
[ ]  1397      }
[B]  1398      result = Curl_setstropt(&data->set.str[STRING_SET_URL],
[B]  1399                              va_arg(param, char *));
[B]  1400      data->state.url = data->set.str[STRING_SET_URL];
[B]  1401      break;
[ ]  1402    case CURLOPT_PORT:
[ ]  1403      /*
[ ]  1404       * The port number to use when getting the URL. 0 disables it.
[ ]  1405       */
[ ]  1406      arg = va_arg(param, long);
[ ]  1407      if((arg < 0) || (arg > 65535))
[ ]  1408        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1409      data->set.use_port = (unsigned short)arg;
[ ]  1410      break;
[ ]  1411    case CURLOPT_TIMEOUT:
[ ]  1412      /*
[ ]  1413       * The maximum time you allow curl to use for a single transfer
[ ]  1414       * operation.
[ ]  1415       */
[ ]  1416      arg = va_arg(param, long);
[ ]  1417      if((arg >= 0) && (arg <= (INT_MAX/1000)))
[ ]  1418        data->set.timeout = (unsigned int)arg * 1000;
[ ]  1419      else
[ ]  1420        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1421      break;
[ ]  1422  
[L]  1423    case CURLOPT_TIMEOUT_MS:
[L]  1424      uarg = va_arg(param, unsigned long);
[L]  1425      if(uarg >= UINT_MAX)
[ ]  1426        uarg = UINT_MAX;
[L]  1427      data->set.timeout = (unsigned int)uarg;
[L]  1428      break;
[ ]  1429  
[ ]  1430    case CURLOPT_CONNECTTIMEOUT:
[ ]  1431      /*
[ ]  1432       * The maximum time you allow curl to use to connect.
[ ]  1433       */
[ ]  1434      arg = va_arg(param, long);
[ ]  1435      if((arg >= 0) && (arg <= (INT_MAX/1000)))
[ ]  1436        data->set.connecttimeout = (unsigned int)arg * 1000;
[ ]  1437      else
[ ]  1438        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1439      break;
[ ]  1440  
[ ]  1441    case CURLOPT_CONNECTTIMEOUT_MS:
[ ]  1442      uarg = va_arg(param, unsigned long);
[ ]  1443      if(uarg >= UINT_MAX)
[ ]  1444        uarg = UINT_MAX;
[ ]  1445      data->set.connecttimeout = (unsigned int)uarg;
[ ]  1446      break;
[ ]  1447  
[ ]  1448  #ifndef CURL_DISABLE_FTP
[ ]  1449    case CURLOPT_ACCEPTTIMEOUT_MS:
[ ]  1450      /*
[ ]  1451       * The maximum time for curl to wait for FTP server connect
[ ]  1452       */
[ ]  1453      uarg = va_arg(param, unsigned long);
[ ]  1454      if(uarg >= UINT_MAX)
[ ]  1455        uarg = UINT_MAX;
[ ]  1456      data->set.accepttimeout = (unsigned int)uarg;
[ ]  1457      break;
[ ]  1458  #endif
[ ]  1459  
[ ]  1460    case CURLOPT_USERPWD:
[ ]  1461      /*
[ ]  1462       * user:password to use in the operation
[ ]  1463       */
[ ]  1464      result = setstropt_userpwd(va_arg(param, char *),
[ ]  1465                                 &data->set.str[STRING_USERNAME],
[ ]  1466                                 &data->set.str[STRING_PASSWORD]);
[ ]  1467      break;
[ ]  1468  
[L]  1469    case CURLOPT_USERNAME:
[ ]  1470      /*
[ ]  1471       * authentication user name to use in the operation
[ ]  1472       */
[L]  1473      result = Curl_setstropt(&data->set.str[STRING_USERNAME],
[L]  1474                              va_arg(param, char *));
[L]  1475      break;
[L]  1476    case CURLOPT_PASSWORD:
[ ]  1477      /*
[ ]  1478       * authentication password to use in the operation
[ ]  1479       */
[L]  1480      result = Curl_setstropt(&data->set.str[STRING_PASSWORD],
[L]  1481                              va_arg(param, char *));
[L]  1482      break;
[ ]  1483  
[ ]  1484    case CURLOPT_LOGIN_OPTIONS:
[ ]  1485      /*
[ ]  1486       * authentication options to use in the operation
[ ]  1487       */
[ ]  1488      result = Curl_setstropt(&data->set.str[STRING_OPTIONS],
[ ]  1489                              va_arg(param, char *));
[ ]  1490      break;
[ ]  1491  
[ ]  1492    case CURLOPT_XOAUTH2_BEARER:
[ ]  1493      /*
[ ]  1494       * OAuth 2.0 bearer token to use in the operation
[ ]  1495       */
[ ]  1496      result = Curl_setstropt(&data->set.str[STRING_BEARER],
[ ]  1497                              va_arg(param, char *));
[ ]  1498      break;
[ ]  1499  
[ ]  1500    case CURLOPT_POSTQUOTE:
[ ]  1501      /*
[ ]  1502       * List of RAW FTP commands to use after a transfer
[ ]  1503       */
[ ]  1504      data->set.postquote = va_arg(param, struct curl_slist *);
[ ]  1505      break;
[ ]  1506    case CURLOPT_PREQUOTE:
[ ]  1507      /*
[ ]  1508       * List of RAW FTP commands to use prior to RETR (Wesley Laxton)
[ ]  1509       */
[ ]  1510      data->set.prequote = va_arg(param, struct curl_slist *);
[ ]  1511      break;
[ ]  1512    case CURLOPT_QUOTE:
[ ]  1513      /*
[ ]  1514       * List of RAW FTP commands to use before a transfer
[ ]  1515       */
[ ]  1516      data->set.quote = va_arg(param, struct curl_slist *);
[ ]  1517      break;
[ ]  1518    case CURLOPT_RESOLVE:
[ ]  1519      /*
[ ]  1520       * List of HOST:PORT:[addresses] strings to populate the DNS cache with
[ ]  1521       * Entries added this way will remain in the cache until explicitly
[ ]  1522       * removed or the handle is cleaned up.
[ ]  1523       *
[ ]  1524       * Prefix the HOST with plus sign (+) to have the entry expire just like
[ ]  1525       * automatically added entries.
[ ]  1526       *
[ ]  1527       * Prefix the HOST with dash (-) to _remove_ the entry from the cache.
[ ]  1528       *
[ ]  1529       * This API can remove any entry from the DNS cache, but only entries
[ ]  1530       * that aren't actually in use right now will be pruned immediately.
[ ]  1531       */
[ ]  1532      data->set.resolve = va_arg(param, struct curl_slist *);
[ ]  1533      data->state.resolve = data->set.resolve;
[ ]  1534      break;
[ ]  1535    case CURLOPT_PROGRESSFUNCTION:
[ ]  1536      /*
[ ]  1537       * Progress callback function
[ ]  1538       */
[ ]  1539      data->set.fprogress = va_arg(param, curl_progress_callback);
[ ]  1540      if(data->set.fprogress)
[ ]  1541        data->progress.callback = TRUE; /* no longer internal */
[ ]  1542      else
[ ]  1543        data->progress.callback = FALSE; /* NULL enforces internal */
[ ]  1544      break;
[ ]  1545  
[ ]  1546    case CURLOPT_XFERINFOFUNCTION:
[ ]  1547      /*
[ ]  1548       * Transfer info callback function
[ ]  1549       */
[ ]  1550      data->set.fxferinfo = va_arg(param, curl_xferinfo_callback);
[ ]  1551      if(data->set.fxferinfo)
[ ]  1552        data->progress.callback = TRUE; /* no longer internal */
[ ]  1553      else
[ ]  1554        data->progress.callback = FALSE; /* NULL enforces internal */
[ ]  1555  
[ ]  1556      break;
[ ]  1557  
[ ]  1558    case CURLOPT_PROGRESSDATA:
[ ]  1559      /*
[ ]  1560       * Custom client data to pass to the progress callback
[ ]  1561       */
[ ]  1562      data->set.progress_client = va_arg(param, void *);
[ ]  1563      break;
[ ]  1564  
[ ]  1565  #ifndef CURL_DISABLE_PROXY
[ ]  1566    case CURLOPT_PROXYUSERPWD:
[ ]  1567      /*
[ ]  1568       * user:password needed to use the proxy
[ ]  1569       */
[ ]  1570      result = setstropt_userpwd(va_arg(param, char *),
[ ]  1571                                 &data->set.str[STRING_PROXYUSERNAME],
[ ]  1572                                 &data->set.str[STRING_PROXYPASSWORD]);
[ ]  1573      break;
[ ]  1574    case CURLOPT_PROXYUSERNAME:
[ ]  1575      /*
[ ]  1576       * authentication user name to use in the operation
[ ]  1577       */
[ ]  1578      result = Curl_setstropt(&data->set.str[STRING_PROXYUSERNAME],
[ ]  1579                              va_arg(param, char *));
[ ]  1580      break;
[ ]  1581    case CURLOPT_PROXYPASSWORD:
[ ]  1582      /*
[ ]  1583       * authentication password to use in the operation
[ ]  1584       */
[ ]  1585      result = Curl_setstropt(&data->set.str[STRING_PROXYPASSWORD],
[ ]  1586                              va_arg(param, char *));
[ ]  1587      break;
[ ]  1588    case CURLOPT_NOPROXY:
[ ]  1589      /*
[ ]  1590       * proxy exception list
[ ]  1591       */
[ ]  1592      result = Curl_setstropt(&data->set.str[STRING_NOPROXY],
[ ]  1593                              va_arg(param, char *));
[ ]  1594      break;
[ ]  1595  #endif
[ ]  1596  
[ ]  1597    case CURLOPT_RANGE:
[ ]  1598      /*
[ ]  1599       * What range of the file you want to transfer
[ ]  1600       */
[ ]  1601      result = Curl_setstropt(&data->set.str[STRING_SET_RANGE],
[ ]  1602                              va_arg(param, char *));
[ ]  1603      break;
[ ]  1604    case CURLOPT_RESUME_FROM:
[ ]  1605      /*
[ ]  1606       * Resume transfer at the given file position
[ ]  1607       */
[ ]  1608      arg = va_arg(param, long);
[ ]  1609      if(arg < -1)
[ ]  1610        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1611      data->set.set_resume_from = arg;
[ ]  1612      break;
[ ]  1613    case CURLOPT_RESUME_FROM_LARGE:
[ ]  1614      /*
[ ]  1615       * Resume transfer at the given file position
[ ]  1616       */
[ ]  1617      bigsize = va_arg(param, curl_off_t);
[ ]  1618      if(bigsize < -1)
[ ]  1619        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1620      data->set.set_resume_from = bigsize;
[ ]  1621      break;
[ ]  1622    case CURLOPT_DEBUGFUNCTION:
[ ]  1623      /*
[ ]  1624       * stderr write callback.
[ ]  1625       */
[ ]  1626      data->set.fdebug = va_arg(param, curl_debug_callback);
[ ]  1627      /*
[ ]  1628       * if the callback provided is NULL, it'll use the default callback
[ ]  1629       */
[ ]  1630      break;
[ ]  1631    case CURLOPT_DEBUGDATA:
[ ]  1632      /*
[ ]  1633       * Set to a void * that should receive all error writes. This
[ ]  1634       * defaults to CURLOPT_STDERR for normal operations.
[ ]  1635       */
[ ]  1636      data->set.debugdata = va_arg(param, void *);
[ ]  1637      break;
[ ]  1638    case CURLOPT_STDERR:
[ ]  1639      /*
[ ]  1640       * Set to a FILE * that should receive all error writes. This
[ ]  1641       * defaults to stderr for normal operations.
[ ]  1642       */
[ ]  1643      data->set.err = va_arg(param, FILE *);
[ ]  1644      if(!data->set.err)
[ ]  1645        data->set.err = stderr;
[ ]  1646      break;
[ ]  1647    case CURLOPT_HEADERFUNCTION:
[ ]  1648      /*
[ ]  1649       * Set header write callback
[ ]  1650       */
[ ]  1651      data->set.fwrite_header = va_arg(param, curl_write_callback);
[ ]  1652      break;
[L]  1653    case CURLOPT_WRITEFUNCTION:
[ ]  1654      /*
[ ]  1655       * Set data write callback
[ ]  1656       */
[L]  1657      data->set.fwrite_func = va_arg(param, curl_write_callback);
[L]  1658      if(!data->set.fwrite_func)
[ ]  1659        /* When set to NULL, reset to our internal default function */
[ ]  1660        data->set.fwrite_func = (curl_write_callback)fwrite;
[L]  1661      break;
[L]  1662    case CURLOPT_READFUNCTION:
[ ]  1663      /*
[ ]  1664       * Read data callback
[ ]  1665       */
[L]  1666      data->set.fread_func_set = va_arg(param, curl_read_callback);
[L]  1667      if(!data->set.fread_func_set) {
[ ]  1668        data->set.is_fread_set = 0;
[ ]  1669        /* When set to NULL, reset to our internal default function */
[ ]  1670        data->set.fread_func_set = (curl_read_callback)fread;
[ ]  1671      }
[L]  1672      else
[L]  1673        data->set.is_fread_set = 1;
[L]  1674      break;
[ ]  1675    case CURLOPT_SEEKFUNCTION:
[ ]  1676      /*
[ ]  1677       * Seek callback. Might be NULL.
[ ]  1678       */
[ ]  1679      data->set.seek_func = va_arg(param, curl_seek_callback);
[ ]  1680      break;
[ ]  1681    case CURLOPT_SEEKDATA:
[ ]  1682      /*
[ ]  1683       * Seek control callback. Might be NULL.
[ ]  1684       */
[ ]  1685      data->set.seek_client = va_arg(param, void *);
[ ]  1686      break;
[ ]  1687    case CURLOPT_IOCTLFUNCTION:
[ ]  1688      /*
[ ]  1689       * I/O control callback. Might be NULL.
[ ]  1690       */
[ ]  1691      data->set.ioctl_func = va_arg(param, curl_ioctl_callback);
[ ]  1692      break;
[ ]  1693    case CURLOPT_IOCTLDATA:
[ ]  1694      /*
[ ]  1695       * I/O control data pointer. Might be NULL.
[ ]  1696       */
[ ]  1697      data->set.ioctl_client = va_arg(param, void *);
[ ]  1698      break;
[ ]  1699    case CURLOPT_SSLCERT:
[ ]  1700      /*
[ ]  1701       * String that holds file name of the SSL certificate to use
[ ]  1702       */
[ ]  1703      result = Curl_setstropt(&data->set.str[STRING_CERT],
[ ]  1704                              va_arg(param, char *));
[ ]  1705      break;
[ ]  1706    case CURLOPT_SSLCERT_BLOB:
[ ]  1707      /*
[ ]  1708       * Blob that holds file content of the SSL certificate to use
[ ]  1709       */
[ ]  1710      result = Curl_setblobopt(&data->set.blobs[BLOB_CERT],
[ ]  1711                               va_arg(param, struct curl_blob *));
[ ]  1712      break;
[ ]  1713  #ifndef CURL_DISABLE_PROXY
[ ]  1714    case CURLOPT_PROXY_SSLCERT:
[ ]  1715      /*
[ ]  1716       * String that holds file name of the SSL certificate to use for proxy
[ ]  1717       */
[ ]  1718      result = Curl_setstropt(&data->set.str[STRING_CERT_PROXY],
[ ]  1719                              va_arg(param, char *));
[ ]  1720      break;
[ ]  1721    case CURLOPT_PROXY_SSLCERT_BLOB:
[ ]  1722      /*
[ ]  1723       * Blob that holds file content of the SSL certificate to use for proxy
[ ]  1724       */
[ ]  1725      result = Curl_setblobopt(&data->set.blobs[BLOB_CERT_PROXY],
[ ]  1726                               va_arg(param, struct curl_blob *));
[ ]  1727      break;
[ ]  1728  #endif
[ ]  1729    case CURLOPT_SSLCERTTYPE:
[ ]  1730      /*
[ ]  1731       * String that holds file type of the SSL certificate to use
[ ]  1732       */
[ ]  1733      result = Curl_setstropt(&data->set.str[STRING_CERT_TYPE],
[ ]  1734                              va_arg(param, char *));
[ ]  1735      break;
[ ]  1736  #ifndef CURL_DISABLE_PROXY
[ ]  1737    case CURLOPT_PROXY_SSLCERTTYPE:
[ ]  1738      /*
[ ]  1739       * String that holds file type of the SSL certificate to use for proxy
[ ]  1740       */
[ ]  1741      result = Curl_setstropt(&data->set.str[STRING_CERT_TYPE_PROXY],
[ ]  1742                              va_arg(param, char *));
[ ]  1743      break;
[ ]  1744  #endif
[ ]  1745    case CURLOPT_SSLKEY:
[ ]  1746      /*
[ ]  1747       * String that holds file name of the SSL key to use
[ ]  1748       */
[ ]  1749      result = Curl_setstropt(&data->set.str[STRING_KEY],
[ ]  1750                              va_arg(param, char *));
[ ]  1751      break;
[ ]  1752    case CURLOPT_SSLKEY_BLOB:
[ ]  1753      /*
[ ]  1754       * Blob that holds file content of the SSL key to use
[ ]  1755       */
[ ]  1756      result = Curl_setblobopt(&data->set.blobs[BLOB_KEY],
[ ]  1757                               va_arg(param, struct curl_blob *));
[ ]  1758      break;
[ ]  1759  #ifndef CURL_DISABLE_PROXY
[ ]  1760    case CURLOPT_PROXY_SSLKEY:
[ ]  1761      /*
[ ]  1762       * String that holds file name of the SSL key to use for proxy
[ ]  1763       */
[ ]  1764      result = Curl_setstropt(&data->set.str[STRING_KEY_PROXY],
[ ]  1765                              va_arg(param, char *));
[ ]  1766      break;
[ ]  1767    case CURLOPT_PROXY_SSLKEY_BLOB:
[ ]  1768      /*
[ ]  1769       * Blob that holds file content of the SSL key to use for proxy
[ ]  1770       */
[ ]  1771      result = Curl_setblobopt(&data->set.blobs[BLOB_KEY_PROXY],
[ ]  1772                               va_arg(param, struct curl_blob *));
[ ]  1773      break;
[ ]  1774  #endif
[ ]  1775    case CURLOPT_SSLKEYTYPE:
[ ]  1776      /*
[ ]  1777       * String that holds file type of the SSL key to use
[ ]  1778       */
[ ]  1779      result = Curl_setstropt(&data->set.str[STRING_KEY_TYPE],
[ ]  1780                              va_arg(param, char *));
[ ]  1781      break;
[ ]  1782  #ifndef CURL_DISABLE_PROXY
[ ]  1783    case CURLOPT_PROXY_SSLKEYTYPE:
[ ]  1784      /*
[ ]  1785       * String that holds file type of the SSL key to use for proxy
[ ]  1786       */
[ ]  1787      result = Curl_setstropt(&data->set.str[STRING_KEY_TYPE_PROXY],
[ ]  1788                              va_arg(param, char *));
[ ]  1789      break;
[ ]  1790  #endif
[ ]  1791    case CURLOPT_KEYPASSWD:
[ ]  1792      /*
[ ]  1793       * String that holds the SSL or SSH private key password.
[ ]  1794       */
[ ]  1795      result = Curl_setstropt(&data->set.str[STRING_KEY_PASSWD],
[ ]  1796                              va_arg(param, char *));
[ ]  1797      break;
[ ]  1798  #ifndef CURL_DISABLE_PROXY
[ ]  1799    case CURLOPT_PROXY_KEYPASSWD:
[ ]  1800      /*
[ ]  1801       * String that holds the SSL private key password for proxy.
[ ]  1802       */
[ ]  1803      result = Curl_setstropt(&data->set.str[STRING_KEY_PASSWD_PROXY],
[ ]  1804                              va_arg(param, char *));
[ ]  1805      break;
[ ]  1806  #endif
[ ]  1807    case CURLOPT_SSLENGINE:
[ ]  1808      /*
[ ]  1809       * String that holds the SSL crypto engine.
[ ]  1810       */
[ ]  1811      argptr = va_arg(param, char *);
[ ]  1812      if(argptr && argptr[0]) {
[ ]  1813        result = Curl_setstropt(&data->set.str[STRING_SSL_ENGINE], argptr);
[ ]  1814        if(!result) {
[ ]  1815          result = Curl_ssl_set_engine(data, argptr);
[ ]  1816        }
[ ]  1817      }
[ ]  1818      break;
[ ]  1819  
[ ]  1820    case CURLOPT_SSLENGINE_DEFAULT:
[ ]  1821      /*
[ ]  1822       * flag to set engine as default.
[ ]  1823       */
[ ]  1824      Curl_setstropt(&data->set.str[STRING_SSL_ENGINE], NULL);
[ ]  1825      result = Curl_ssl_set_engine_default(data);
[ ]  1826      break;
[ ]  1827    case CURLOPT_CRLF:
[ ]  1828      /*
[ ]  1829       * Kludgy option to enable CRLF conversions. Subject for removal.
[ ]  1830       */
[ ]  1831      data->set.crlf = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  1832      break;
[ ]  1833  #ifndef CURL_DISABLE_PROXY
[ ]  1834    case CURLOPT_HAPROXYPROTOCOL:
[ ]  1835      /*
[ ]  1836       * Set to send the HAProxy Proxy Protocol header
[ ]  1837       */
[ ]  1838      data->set.haproxyprotocol = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  1839      break;
[ ]  1840  #endif
[ ]  1841    case CURLOPT_INTERFACE:
[ ]  1842      /*
[ ]  1843       * Set what interface or address/hostname to bind the socket to when
[ ]  1844       * performing an operation and thus what from-IP your connection will use.
[ ]  1845       */
[ ]  1846      result = Curl_setstropt(&data->set.str[STRING_DEVICE],
[ ]  1847                              va_arg(param, char *));
[ ]  1848      break;
[ ]  1849    case CURLOPT_LOCALPORT:
[ ]  1850      /*
[ ]  1851       * Set what local port to bind the socket to when performing an operation.
[ ]  1852       */
[ ]  1853      arg = va_arg(param, long);
[ ]  1854      if((arg < 0) || (arg > 65535))
[ ]  1855        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1856      data->set.localport = curlx_sltous(arg);
[ ]  1857      break;
[ ]  1858    case CURLOPT_LOCALPORTRANGE:
[ ]  1859      /*
[ ]  1860       * Set number of local ports to try, starting with CURLOPT_LOCALPORT.
[ ]  1861       */
[ ]  1862      arg = va_arg(param, long);
[ ]  1863      if((arg < 0) || (arg > 65535))
[ ]  1864        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1865      data->set.localportrange = curlx_sltosi(arg);
[ ]  1866      break;
[ ]  1867    case CURLOPT_GSSAPI_DELEGATION:
[ ]  1868      /*
[ ]  1869       * GSS-API credential delegation bitmask
[ ]  1870       */
[ ]  1871      arg = va_arg(param, long);
[ ]  1872      if(arg < CURLGSSAPI_DELEGATION_NONE)
[ ]  1873        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  1874      data->set.gssapi_delegation = arg;
[ ]  1875      break;
[ ]  1876    case CURLOPT_SSL_VERIFYPEER:
[ ]  1877      /*
[ ]  1878       * Enable peer SSL verifying.
[ ]  1879       */
[ ]  1880      data->set.ssl.primary.verifypeer = (0 != va_arg(param, long)) ?
[ ]  1881        TRUE : FALSE;
[ ]  1882  
[ ]  1883      /* Update the current connection ssl_config. */
[ ]  1884      if(data->conn) {
[ ]  1885        data->conn->ssl_config.verifypeer =
[ ]  1886          data->set.ssl.primary.verifypeer;
[ ]  1887      }
[ ]  1888      break;
[ ]  1889  #ifndef CURL_DISABLE_DOH
[ ]  1890    case CURLOPT_DOH_SSL_VERIFYPEER:
[ ]  1891      /*
[ ]  1892       * Enable peer SSL verifying for DoH.
[ ]  1893       */
[ ]  1894      data->set.doh_verifypeer = (0 != va_arg(param, long)) ?
[ ]  1895        TRUE : FALSE;
[ ]  1896      break;
[ ]  1897  #endif
[ ]  1898  #ifndef CURL_DISABLE_PROXY
[ ]  1899    case CURLOPT_PROXY_SSL_VERIFYPEER:
[ ]  1900      /*
[ ]  1901       * Enable peer SSL verifying for proxy.
[ ]  1902       */
[ ]  1903      data->set.proxy_ssl.primary.verifypeer =
[ ]  1904        (0 != va_arg(param, long))?TRUE:FALSE;
[ ]  1905  
[ ]  1906      /* Update the current connection proxy_ssl_config. */
[ ]  1907      if(data->conn) {
[ ]  1908        data->conn->proxy_ssl_config.verifypeer =
[ ]  1909          data->set.proxy_ssl.primary.verifypeer;
[ ]  1910      }
[ ]  1911      break;
[ ]  1912  #endif
[ ]  1913    case CURLOPT_SSL_VERIFYHOST:
[ ]  1914      /*
[ ]  1915       * Enable verification of the host name in the peer certificate
[ ]  1916       */
[ ]  1917      arg = va_arg(param, long);
[ ]  1918  
[ ]  1919      /* Obviously people are not reading documentation and too many thought
[ ]  1920         this argument took a boolean when it wasn't and misused it.
[ ]  1921         Treat 1 and 2 the same */
[ ]  1922      data->set.ssl.primary.verifyhost = (bool)((arg & 3) ? TRUE : FALSE);
[ ]  1923  
[ ]  1924      /* Update the current connection ssl_config. */
[ ]  1925      if(data->conn) {
[ ]  1926        data->conn->ssl_config.verifyhost =
[ ]  1927          data->set.ssl.primary.verifyhost;
[ ]  1928      }
[ ]  1929      break;
[ ]  1930  #ifndef CURL_DISABLE_DOH
[ ]  1931    case CURLOPT_DOH_SSL_VERIFYHOST:
[ ]  1932      /*
[ ]  1933       * Enable verification of the host name in the peer certificate for DoH
[ ]  1934       */
[ ]  1935      arg = va_arg(param, long);
[ ]  1936  
[ ]  1937      /* Treat both 1 and 2 as TRUE */
[ ]  1938      data->set.doh_verifyhost = (bool)((arg & 3) ? TRUE : FALSE);
[ ]  1939      break;
[ ]  1940  #endif
[ ]  1941  #ifndef CURL_DISABLE_PROXY
[ ]  1942    case CURLOPT_PROXY_SSL_VERIFYHOST:
[ ]  1943      /*
[ ]  1944       * Enable verification of the host name in the peer certificate for proxy
[ ]  1945       */
[ ]  1946      arg = va_arg(param, long);
[ ]  1947  
[ ]  1948      /* Treat both 1 and 2 as TRUE */
[ ]  1949      data->set.proxy_ssl.primary.verifyhost = (bool)((arg & 3)?TRUE:FALSE);
[ ]  1950  
[ ]  1951      /* Update the current connection proxy_ssl_config. */
[ ]  1952      if(data->conn) {
[ ]  1953        data->conn->proxy_ssl_config.verifyhost =
[ ]  1954          data->set.proxy_ssl.primary.verifyhost;
[ ]  1955      }
[ ]  1956      break;
[ ]  1957  #endif
[ ]  1958    case CURLOPT_SSL_VERIFYSTATUS:
[ ]  1959      /*
[ ]  1960       * Enable certificate status verifying.
[ ]  1961       */
[ ]  1962      if(!Curl_ssl_cert_status_request()) {
[ ]  1963        result = CURLE_NOT_BUILT_IN;
[ ]  1964        break;
[ ]  1965      }
[ ]  1966  
[ ]  1967      data->set.ssl.primary.verifystatus = (0 != va_arg(param, long)) ?
[ ]  1968        TRUE : FALSE;
[ ]  1969  
[ ]  1970      /* Update the current connection ssl_config. */
[ ]  1971      if(data->conn) {
[ ]  1972        data->conn->ssl_config.verifystatus =
[ ]  1973          data->set.ssl.primary.verifystatus;
[ ]  1974      }
[ ]  1975      break;
[ ]  1976  #ifndef CURL_DISABLE_DOH
[ ]  1977    case CURLOPT_DOH_SSL_VERIFYSTATUS:
[ ]  1978      /*
[ ]  1979       * Enable certificate status verifying for DoH.
[ ]  1980       */
[ ]  1981      if(!Curl_ssl_cert_status_request()) {
[ ]  1982        result = CURLE_NOT_BUILT_IN;
[ ]  1983        break;
[ ]  1984      }
[ ]  1985  
[ ]  1986      data->set.doh_verifystatus = (0 != va_arg(param, long)) ?
[ ]  1987        TRUE : FALSE;
[ ]  1988      break;
[ ]  1989  #endif
[ ]  1990    case CURLOPT_SSL_CTX_FUNCTION:
[ ]  1991      /*
[ ]  1992       * Set a SSL_CTX callback
[ ]  1993       */
[ ]  1994  #ifdef USE_SSL
[ ]  1995      if(Curl_ssl->supports & SSLSUPP_SSL_CTX)
[ ]  1996        data->set.ssl.fsslctx = va_arg(param, curl_ssl_ctx_callback);
[ ]  1997      else
[ ]  1998  #endif
[ ]  1999        result = CURLE_NOT_BUILT_IN;
[ ]  2000      break;
[ ]  2001    case CURLOPT_SSL_CTX_DATA:
[ ]  2002      /*
[ ]  2003       * Set a SSL_CTX callback parameter pointer
[ ]  2004       */
[ ]  2005  #ifdef USE_SSL
[ ]  2006      if(Curl_ssl->supports & SSLSUPP_SSL_CTX)
[ ]  2007        data->set.ssl.fsslctxp = va_arg(param, void *);
[ ]  2008      else
[ ]  2009  #endif
[ ]  2010        result = CURLE_NOT_BUILT_IN;
[ ]  2011      break;
[ ]  2012    case CURLOPT_SSL_FALSESTART:
[ ]  2013      /*
[ ]  2014       * Enable TLS false start.
[ ]  2015       */
[ ]  2016      if(!Curl_ssl_false_start()) {
[ ]  2017        result = CURLE_NOT_BUILT_IN;
[ ]  2018        break;
[ ]  2019      }
[ ]  2020  
[ ]  2021      data->set.ssl.falsestart = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2022      break;
[ ]  2023    case CURLOPT_CERTINFO:
[ ]  2024  #ifdef USE_SSL
[ ]  2025      if(Curl_ssl->supports & SSLSUPP_CERTINFO)
[ ]  2026        data->set.ssl.certinfo = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2027      else
[ ]  2028  #endif
[ ]  2029        result = CURLE_NOT_BUILT_IN;
[ ]  2030          break;
[ ]  2031    case CURLOPT_PINNEDPUBLICKEY:
[ ]  2032      /*
[ ]  2033       * Set pinned public key for SSL connection.
[ ]  2034       * Specify file name of the public key in DER format.
[ ]  2035       */
[ ]  2036  #ifdef USE_SSL
[ ]  2037      if(Curl_ssl->supports & SSLSUPP_PINNEDPUBKEY)
[ ]  2038        result = Curl_setstropt(&data->set.str[STRING_SSL_PINNEDPUBLICKEY],
[ ]  2039                                va_arg(param, char *));
[ ]  2040      else
[ ]  2041  #endif
[ ]  2042        result = CURLE_NOT_BUILT_IN;
[ ]  2043      break;
[ ]  2044  #ifndef CURL_DISABLE_PROXY
[ ]  2045    case CURLOPT_PROXY_PINNEDPUBLICKEY:
[ ]  2046      /*
[ ]  2047       * Set pinned public key for SSL connection.
[ ]  2048       * Specify file name of the public key in DER format.
[ ]  2049       */
[ ]  2050  #ifdef USE_SSL
[ ]  2051      if(Curl_ssl->supports & SSLSUPP_PINNEDPUBKEY)
[ ]  2052        result = Curl_setstropt(&data->set.str[STRING_SSL_PINNEDPUBLICKEY_PROXY],
[ ]  2053                                va_arg(param, char *));
[ ]  2054      else
[ ]  2055  #endif
[ ]  2056        result = CURLE_NOT_BUILT_IN;
[ ]  2057      break;
[ ]  2058  #endif
[ ]  2059    case CURLOPT_CAINFO:
[ ]  2060      /*
[ ]  2061       * Set CA info for SSL connection. Specify file name of the CA certificate
[ ]  2062       */
[ ]  2063      result = Curl_setstropt(&data->set.str[STRING_SSL_CAFILE],
[ ]  2064                              va_arg(param, char *));
[ ]  2065      break;
[ ]  2066    case CURLOPT_CAINFO_BLOB:
[ ]  2067      /*
[ ]  2068       * Blob that holds CA info for SSL connection.
[ ]  2069       * Specify entire PEM of the CA certificate
[ ]  2070       */
[ ]  2071  #ifdef USE_SSL
[ ]  2072      if(Curl_ssl->supports & SSLSUPP_CAINFO_BLOB)
[ ]  2073        result = Curl_setblobopt(&data->set.blobs[BLOB_CAINFO],
[ ]  2074                                 va_arg(param, struct curl_blob *));
[ ]  2075      else
[ ]  2076  #endif
[ ]  2077        return CURLE_NOT_BUILT_IN;
[ ]  2078  
[ ]  2079      break;
[ ]  2080  #ifndef CURL_DISABLE_PROXY
[ ]  2081    case CURLOPT_PROXY_CAINFO:
[ ]  2082      /*
[ ]  2083       * Set CA info SSL connection for proxy. Specify file name of the
[ ]  2084       * CA certificate
[ ]  2085       */
[ ]  2086      result = Curl_setstropt(&data->set.str[STRING_SSL_CAFILE_PROXY],
[ ]  2087                              va_arg(param, char *));
[ ]  2088      break;
[ ]  2089    case CURLOPT_PROXY_CAINFO_BLOB:
[ ]  2090      /*
[ ]  2091       * Blob that holds CA info for SSL connection proxy.
[ ]  2092       * Specify entire PEM of the CA certificate
[ ]  2093       */
[ ]  2094  #ifdef USE_SSL
[ ]  2095      if(Curl_ssl->supports & SSLSUPP_CAINFO_BLOB)
[ ]  2096        result = Curl_setblobopt(&data->set.blobs[BLOB_CAINFO_PROXY],
[ ]  2097                                 va_arg(param, struct curl_blob *));
[ ]  2098      else
[ ]  2099  #endif
[ ]  2100        return CURLE_NOT_BUILT_IN;
[ ]  2101      break;
[ ]  2102  #endif
[ ]  2103    case CURLOPT_CAPATH:
[ ]  2104      /*
[ ]  2105       * Set CA path info for SSL connection. Specify directory name of the CA
[ ]  2106       * certificates which have been prepared using openssl c_rehash utility.
[ ]  2107       */
[ ]  2108  #ifdef USE_SSL
[ ]  2109      if(Curl_ssl->supports & SSLSUPP_CA_PATH)
[ ]  2110        /* This does not work on windows. */
[ ]  2111        result = Curl_setstropt(&data->set.str[STRING_SSL_CAPATH],
[ ]  2112                                va_arg(param, char *));
[ ]  2113      else
[ ]  2114  #endif
[ ]  2115        result = CURLE_NOT_BUILT_IN;
[ ]  2116      break;
[ ]  2117  #ifndef CURL_DISABLE_PROXY
[ ]  2118    case CURLOPT_PROXY_CAPATH:
[ ]  2119      /*
[ ]  2120       * Set CA path info for SSL connection proxy. Specify directory name of the
[ ]  2121       * CA certificates which have been prepared using openssl c_rehash utility.
[ ]  2122       */
[ ]  2123  #ifdef USE_SSL
[ ]  2124      if(Curl_ssl->supports & SSLSUPP_CA_PATH)
[ ]  2125        /* This does not work on windows. */
[ ]  2126        result = Curl_setstropt(&data->set.str[STRING_SSL_CAPATH_PROXY],
[ ]  2127                                va_arg(param, char *));
[ ]  2128      else
[ ]  2129  #endif
[ ]  2130        result = CURLE_NOT_BUILT_IN;
[ ]  2131      break;
[ ]  2132  #endif
[L]  2133    case CURLOPT_CRLFILE:
[ ]  2134      /*
[ ]  2135       * Set CRL file info for SSL connection. Specify file name of the CRL
[ ]  2136       * to check certificates revocation
[ ]  2137       */
[L]  2138      result = Curl_setstropt(&data->set.str[STRING_SSL_CRLFILE],
[L]  2139                              va_arg(param, char *));
[L]  2140      break;
[ ]  2141  #ifndef CURL_DISABLE_PROXY
[ ]  2142    case CURLOPT_PROXY_CRLFILE:
[ ]  2143      /*
[ ]  2144       * Set CRL file info for SSL connection for proxy. Specify file name of the
[ ]  2145       * CRL to check certificates revocation
[ ]  2146       */
[ ]  2147      result = Curl_setstropt(&data->set.str[STRING_SSL_CRLFILE_PROXY],
[ ]  2148                              va_arg(param, char *));
[ ]  2149      break;
[ ]  2150  #endif
[ ]  2151    case CURLOPT_ISSUERCERT:
[ ]  2152      /*
[ ]  2153       * Set Issuer certificate file
[ ]  2154       * to check certificates issuer
[ ]  2155       */
[ ]  2156      result = Curl_setstropt(&data->set.str[STRING_SSL_ISSUERCERT],
[ ]  2157                              va_arg(param, char *));
[ ]  2158      break;
[ ]  2159    case CURLOPT_ISSUERCERT_BLOB:
[ ]  2160      /*
[ ]  2161       * Blob that holds Issuer certificate to check certificates issuer
[ ]  2162       */
[ ]  2163      result = Curl_setblobopt(&data->set.blobs[BLOB_SSL_ISSUERCERT],
[ ]  2164                               va_arg(param, struct curl_blob *));
[ ]  2165      break;
[ ]  2166  #ifndef CURL_DISABLE_PROXY
[ ]  2167    case CURLOPT_PROXY_ISSUERCERT:
[ ]  2168      /*
[ ]  2169       * Set Issuer certificate file
[ ]  2170       * to check certificates issuer
[ ]  2171       */
[ ]  2172      result = Curl_setstropt(&data->set.str[STRING_SSL_ISSUERCERT_PROXY],
[ ]  2173                              va_arg(param, char *));
[ ]  2174      break;
[ ]  2175    case CURLOPT_PROXY_ISSUERCERT_BLOB:
[ ]  2176      /*
[ ]  2177       * Blob that holds Issuer certificate to check certificates issuer
[ ]  2178       */
[ ]  2179      result = Curl_setblobopt(&data->set.blobs[BLOB_SSL_ISSUERCERT_PROXY],
[ ]  2180                               va_arg(param, struct curl_blob *));
[ ]  2181      break;
[ ]  2182  #endif
[ ]  2183  #ifndef CURL_DISABLE_TELNET
[ ]  2184    case CURLOPT_TELNETOPTIONS:
[ ]  2185      /*
[ ]  2186       * Set a linked list of telnet options
[ ]  2187       */
[ ]  2188      data->set.telnet_options = va_arg(param, struct curl_slist *);
[ ]  2189      break;
[ ]  2190  #endif
[ ]  2191    case CURLOPT_BUFFERSIZE:
[ ]  2192      /*
[ ]  2193       * The application kindly asks for a differently sized receive buffer.
[ ]  2194       * If it seems reasonable, we'll use it.
[ ]  2195       */
[ ]  2196      if(data->state.buffer)
[ ]  2197        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2198  
[ ]  2199      arg = va_arg(param, long);
[ ]  2200  
[ ]  2201      if(arg > READBUFFER_MAX)
[ ]  2202        arg = READBUFFER_MAX;
[ ]  2203      else if(arg < 1)
[ ]  2204        arg = READBUFFER_SIZE;
[ ]  2205      else if(arg < READBUFFER_MIN)
[ ]  2206        arg = READBUFFER_MIN;
[ ]  2207  
[ ]  2208      data->set.buffer_size = (int)arg;
[ ]  2209      break;
[ ]  2210  
[ ]  2211    case CURLOPT_UPLOAD_BUFFERSIZE:
[ ]  2212      /*
[ ]  2213       * The application kindly asks for a differently sized upload buffer.
[ ]  2214       * Cap it to sensible.
[ ]  2215       */
[ ]  2216      arg = va_arg(param, long);
[ ]  2217  
[ ]  2218      if(arg > UPLOADBUFFER_MAX)
[ ]  2219        arg = UPLOADBUFFER_MAX;
[ ]  2220      else if(arg < UPLOADBUFFER_MIN)
[ ]  2221        arg = UPLOADBUFFER_MIN;
[ ]  2222  
[ ]  2223      data->set.upload_buffer_size = (unsigned int)arg;
[ ]  2224      Curl_safefree(data->state.ulbuf); /* force a realloc next opportunity */
[ ]  2225      break;
[ ]  2226  
[ ]  2227    case CURLOPT_NOSIGNAL:
[ ]  2228      /*
[ ]  2229       * The application asks not to set any signal() or alarm() handlers,
[ ]  2230       * even when using a timeout.
[ ]  2231       */
[ ]  2232      data->set.no_signal = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2233      break;
[ ]  2234  
[ ]  2235    case CURLOPT_SHARE:
[ ]  2236    {
[ ]  2237      struct Curl_share *set;
[ ]  2238      set = va_arg(param, struct Curl_share *);
[ ]  2239  
[ ]  2240      /* disconnect from old share, if any */
[ ]  2241      if(data->share) {
[ ]  2242        Curl_share_lock(data, CURL_LOCK_DATA_SHARE, CURL_LOCK_ACCESS_SINGLE);
[ ]  2243  
[ ]  2244        if(data->dns.hostcachetype == HCACHE_SHARED) {
[ ]  2245          data->dns.hostcache = NULL;
[ ]  2246          data->dns.hostcachetype = HCACHE_NONE;
[ ]  2247        }
[ ]  2248  
[ ]  2249  #if !defined(CURL_DISABLE_HTTP) && !defined(CURL_DISABLE_COOKIES)
[ ]  2250        if(data->share->cookies == data->cookies)
[ ]  2251          data->cookies = NULL;
[ ]  2252  #endif
[ ]  2253  
[ ]  2254        if(data->share->sslsession == data->state.session)
[ ]  2255          data->state.session = NULL;
[ ]  2256  
[ ]  2257  #ifdef USE_LIBPSL
[ ]  2258        if(data->psl == &data->share->psl)
[ ]  2259          data->psl = data->multi? &data->multi->psl: NULL;
[ ]  2260  #endif
[ ]  2261  
[ ]  2262        data->share->dirty--;
[ ]  2263  
[ ]  2264        Curl_share_unlock(data, CURL_LOCK_DATA_SHARE);
[ ]  2265        data->share = NULL;
[ ]  2266      }
[ ]  2267  
[ ]  2268      if(GOOD_SHARE_HANDLE(set))
[ ]  2269        /* use new share if it set */
[ ]  2270        data->share = set;
[ ]  2271      if(data->share) {
[ ]  2272  
[ ]  2273        Curl_share_lock(data, CURL_LOCK_DATA_SHARE, CURL_LOCK_ACCESS_SINGLE);
[ ]  2274  
[ ]  2275        data->share->dirty++;
[ ]  2276  
[ ]  2277        if(data->share->specifier & (1<< CURL_LOCK_DATA_DNS)) {
[ ]  2278          /* use shared host cache */
[ ]  2279          data->dns.hostcache = &data->share->hostcache;
[ ]  2280          data->dns.hostcachetype = HCACHE_SHARED;
[ ]  2281        }
[ ]  2282  #if !defined(CURL_DISABLE_HTTP) && !defined(CURL_DISABLE_COOKIES)
[ ]  2283        if(data->share->cookies) {
[ ]  2284          /* use shared cookie list, first free own one if any */
[ ]  2285          Curl_cookie_cleanup(data->cookies);
[ ]  2286          /* enable cookies since we now use a share that uses cookies! */
[ ]  2287          data->cookies = data->share->cookies;
[ ]  2288        }
[ ]  2289  #endif   /* CURL_DISABLE_HTTP */
[ ]  2290        if(data->share->sslsession) {
[ ]  2291          data->set.general_ssl.max_ssl_sessions = data->share->max_ssl_sessions;
[ ]  2292          data->state.session = data->share->sslsession;
[ ]  2293        }
[ ]  2294  #ifdef USE_LIBPSL
[ ]  2295        if(data->share->specifier & (1 << CURL_LOCK_DATA_PSL))
[ ]  2296          data->psl = &data->share->psl;
[ ]  2297  #endif
[ ]  2298  
[ ]  2299        Curl_share_unlock(data, CURL_LOCK_DATA_SHARE);
[ ]  2300      }
[ ]  2301      /* check for host cache not needed,
[ ]  2302       * it will be done by curl_easy_perform */
[ ]  2303    }
[ ]  2304    break;
[ ]  2305  
[ ]  2306    case CURLOPT_PRIVATE:
[ ]  2307      /*
[ ]  2308       * Set private data pointer.
[ ]  2309       */
[ ]  2310      data->set.private_data = va_arg(param, void *);
[ ]  2311      break;
[ ]  2312  
[ ]  2313    case CURLOPT_MAXFILESIZE:
[ ]  2314      /*
[ ]  2315       * Set the maximum size of a file to download.
[ ]  2316       */
[ ]  2317      arg = va_arg(param, long);
[ ]  2318      if(arg < 0)
[ ]  2319        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2320      data->set.max_filesize = arg;
[ ]  2321      break;
[ ]  2322  
[ ]  2323  #ifdef USE_SSL
[ ]  2324    case CURLOPT_USE_SSL:
[ ]  2325      /*
[ ]  2326       * Make transfers attempt to use SSL/TLS.
[ ]  2327       */
[ ]  2328      arg = va_arg(param, long);
[ ]  2329      if((arg < CURLUSESSL_NONE) || (arg >= CURLUSESSL_LAST))
[ ]  2330        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2331      data->set.use_ssl = (curl_usessl)arg;
[ ]  2332      break;
[ ]  2333  
[ ]  2334    case CURLOPT_SSL_OPTIONS:
[ ]  2335      arg = va_arg(param, long);
[ ]  2336      data->set.ssl.primary.ssl_options = (unsigned char)(arg & 0xff);
[ ]  2337      data->set.ssl.enable_beast = !!(arg & CURLSSLOPT_ALLOW_BEAST);
[ ]  2338      data->set.ssl.no_revoke = !!(arg & CURLSSLOPT_NO_REVOKE);
[ ]  2339      data->set.ssl.no_partialchain = !!(arg & CURLSSLOPT_NO_PARTIALCHAIN);
[ ]  2340      data->set.ssl.revoke_best_effort = !!(arg & CURLSSLOPT_REVOKE_BEST_EFFORT);
[ ]  2341      data->set.ssl.native_ca_store = !!(arg & CURLSSLOPT_NATIVE_CA);
[ ]  2342      data->set.ssl.auto_client_cert = !!(arg & CURLSSLOPT_AUTO_CLIENT_CERT);
[ ]  2343      /* If a setting is added here it should also be added in dohprobe()
[ ]  2344         which sets its own CURLOPT_SSL_OPTIONS based on these settings. */
[ ]  2345      break;
[ ]  2346  
[ ]  2347  #ifndef CURL_DISABLE_PROXY
[ ]  2348    case CURLOPT_PROXY_SSL_OPTIONS:
[ ]  2349      arg = va_arg(param, long);
[ ]  2350      data->set.proxy_ssl.primary.ssl_options = (unsigned char)(arg & 0xff);
[ ]  2351      data->set.proxy_ssl.enable_beast = !!(arg & CURLSSLOPT_ALLOW_BEAST);
[ ]  2352      data->set.proxy_ssl.no_revoke = !!(arg & CURLSSLOPT_NO_REVOKE);
[ ]  2353      data->set.proxy_ssl.no_partialchain = !!(arg & CURLSSLOPT_NO_PARTIALCHAIN);
[ ]  2354      data->set.proxy_ssl.revoke_best_effort =
[ ]  2355        !!(arg & CURLSSLOPT_REVOKE_BEST_EFFORT);
[ ]  2356      data->set.proxy_ssl.native_ca_store = !!(arg & CURLSSLOPT_NATIVE_CA);
[ ]  2357      data->set.proxy_ssl.auto_client_cert =
[ ]  2358        !!(arg & CURLSSLOPT_AUTO_CLIENT_CERT);
[ ]  2359      break;
[ ]  2360  #endif
[ ]  2361  
[ ]  2362    case CURLOPT_SSL_EC_CURVES:
[ ]  2363      /*
[ ]  2364       * Set accepted curves in SSL connection setup.
[ ]  2365       * Specify colon-delimited list of curve algorithm names.
[ ]  2366       */
[ ]  2367      result = Curl_setstropt(&data->set.str[STRING_SSL_EC_CURVES],
[ ]  2368                              va_arg(param, char *));
[ ]  2369      break;
[ ]  2370  #endif
[ ]  2371    case CURLOPT_IPRESOLVE:
[ ]  2372      arg = va_arg(param, long);
[ ]  2373      if((arg < CURL_IPRESOLVE_WHATEVER) || (arg > CURL_IPRESOLVE_V6))
[ ]  2374        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2375      data->set.ipver = (unsigned char) arg;
[ ]  2376      break;
[ ]  2377  
[ ]  2378    case CURLOPT_MAXFILESIZE_LARGE:
[ ]  2379      /*
[ ]  2380       * Set the maximum size of a file to download.
[ ]  2381       */
[ ]  2382      bigsize = va_arg(param, curl_off_t);
[ ]  2383      if(bigsize < 0)
[ ]  2384        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2385      data->set.max_filesize = bigsize;
[ ]  2386      break;
[ ]  2387  
[ ]  2388    case CURLOPT_TCP_NODELAY:
[ ]  2389      /*
[ ]  2390       * Enable or disable TCP_NODELAY, which will disable/enable the Nagle
[ ]  2391       * algorithm
[ ]  2392       */
[ ]  2393      data->set.tcp_nodelay = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2394      break;
[ ]  2395  
[ ]  2396    case CURLOPT_IGNORE_CONTENT_LENGTH:
[ ]  2397      data->set.ignorecl = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2398      break;
[ ]  2399  
[ ]  2400    case CURLOPT_CONNECT_ONLY:
[ ]  2401      /*
[ ]  2402       * No data transfer.
[ ]  2403       * (1) - only do connection
[ ]  2404       * (2) - do first get request but get no content
[ ]  2405       */
[ ]  2406      arg = va_arg(param, long);
[ ]  2407      if(arg > 2)
[ ]  2408        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2409      data->set.connect_only = (unsigned char)arg;
[ ]  2410      break;
[ ]  2411  
[L]  2412    case CURLOPT_SOCKOPTFUNCTION:
[ ]  2413      /*
[ ]  2414       * socket callback function: called after socket() but before connect()
[ ]  2415       */
[L]  2416      data->set.fsockopt = va_arg(param, curl_sockopt_callback);
[L]  2417      break;
[ ]  2418  
[ ]  2419    case CURLOPT_SOCKOPTDATA:
[ ]  2420      /*
[ ]  2421       * socket callback data pointer. Might be NULL.
[ ]  2422       */
[ ]  2423      data->set.sockopt_client = va_arg(param, void *);
[ ]  2424      break;
[ ]  2425  
[L]  2426    case CURLOPT_OPENSOCKETFUNCTION:
[ ]  2427      /*
[ ]  2428       * open/create socket callback function: called instead of socket(),
[ ]  2429       * before connect()
[ ]  2430       */
[L]  2431      data->set.fopensocket = va_arg(param, curl_opensocket_callback);
[L]  2432      break;
[ ]  2433  
[L]  2434    case CURLOPT_OPENSOCKETDATA:
[ ]  2435      /*
[ ]  2436       * socket callback data pointer. Might be NULL.
[ ]  2437       */
[L]  2438      data->set.opensocket_client = va_arg(param, void *);
[L]  2439      break;
[ ]  2440  
[ ]  2441    case CURLOPT_CLOSESOCKETFUNCTION:
[ ]  2442      /*
[ ]  2443       * close socket callback function: called instead of close()
[ ]  2444       * when shutting down a connection
[ ]  2445       */
[ ]  2446      data->set.fclosesocket = va_arg(param, curl_closesocket_callback);
[ ]  2447      break;
[ ]  2448  
[ ]  2449    case CURLOPT_RESOLVER_START_FUNCTION:
[ ]  2450      /*
[ ]  2451       * resolver start callback function: called before a new resolver request
[ ]  2452       * is started
[ ]  2453       */
[ ]  2454      data->set.resolver_start = va_arg(param, curl_resolver_start_callback);
[ ]  2455      break;
[ ]  2456  
[ ]  2457    case CURLOPT_RESOLVER_START_DATA:
[ ]  2458      /*
[ ]  2459       * resolver start callback data pointer. Might be NULL.
[ ]  2460       */
[ ]  2461      data->set.resolver_start_client = va_arg(param, void *);
[ ]  2462      break;
[ ]  2463  
[ ]  2464    case CURLOPT_CLOSESOCKETDATA:
[ ]  2465      /*
[ ]  2466       * socket callback data pointer. Might be NULL.
[ ]  2467       */
[ ]  2468      data->set.closesocket_client = va_arg(param, void *);
[ ]  2469      break;
[ ]  2470  
[ ]  2471    case CURLOPT_SSL_SESSIONID_CACHE:
[ ]  2472      data->set.ssl.primary.sessionid = (0 != va_arg(param, long)) ?
[ ]  2473        TRUE : FALSE;
[ ]  2474  #ifndef CURL_DISABLE_PROXY
[ ]  2475      data->set.proxy_ssl.primary.sessionid = data->set.ssl.primary.sessionid;
[ ]  2476  #endif
[ ]  2477      break;
[ ]  2478  
[ ]  2479  #ifdef USE_SSH
[ ]  2480      /* we only include SSH options if explicitly built to support SSH */
[ ]  2481    case CURLOPT_SSH_AUTH_TYPES:
[ ]  2482      data->set.ssh_auth_types = (unsigned int)va_arg(param, long);
[ ]  2483      break;
[ ]  2484  
[ ]  2485    case CURLOPT_SSH_PUBLIC_KEYFILE:
[ ]  2486      /*
[ ]  2487       * Use this file instead of the $HOME/.ssh/id_dsa.pub file
[ ]  2488       */
[ ]  2489      result = Curl_setstropt(&data->set.str[STRING_SSH_PUBLIC_KEY],
[ ]  2490                              va_arg(param, char *));
[ ]  2491      break;
[ ]  2492  
[ ]  2493    case CURLOPT_SSH_PRIVATE_KEYFILE:
[ ]  2494      /*
[ ]  2495       * Use this file instead of the $HOME/.ssh/id_dsa file
[ ]  2496       */
[ ]  2497      result = Curl_setstropt(&data->set.str[STRING_SSH_PRIVATE_KEY],
[ ]  2498                              va_arg(param, char *));
[ ]  2499      break;
[ ]  2500    case CURLOPT_SSH_HOST_PUBLIC_KEY_MD5:
[ ]  2501      /*
[ ]  2502       * Option to allow for the MD5 of the host public key to be checked
[ ]  2503       * for validation purposes.
[ ]  2504       */
[ ]  2505      result = Curl_setstropt(&data->set.str[STRING_SSH_HOST_PUBLIC_KEY_MD5],
[ ]  2506                              va_arg(param, char *));
[ ]  2507      break;
[ ]  2508  
[ ]  2509    case CURLOPT_SSH_HOST_PUBLIC_KEY_SHA256:
[ ]  2510      /*
[ ]  2511       * Option to allow for the SHA256 of the host public key to be checked
[ ]  2512       * for validation purposes.
[ ]  2513       */
[ ]  2514      result = Curl_setstropt(&data->set.str[STRING_SSH_HOST_PUBLIC_KEY_SHA256],
[ ]  2515                              va_arg(param, char *));
[ ]  2516      break;
[ ]  2517  
[ ]  2518    case CURLOPT_SSH_KNOWNHOSTS:
[ ]  2519      /*
[ ]  2520       * Store the file name to read known hosts from.
[ ]  2521       */
[ ]  2522      result = Curl_setstropt(&data->set.str[STRING_SSH_KNOWNHOSTS],
[ ]  2523                              va_arg(param, char *));
[ ]  2524      break;
[ ]  2525  #ifdef USE_LIBSSH2
[ ]  2526    case CURLOPT_SSH_HOSTKEYFUNCTION:
[ ]  2527      /* the callback to check the hostkey without the knownhost file */
[ ]  2528      data->set.ssh_hostkeyfunc = va_arg(param, curl_sshhostkeycallback);
[ ]  2529      break;
[ ]  2530  
[ ]  2531    case CURLOPT_SSH_HOSTKEYDATA:
[ ]  2532      /*
[ ]  2533       * Custom client data to pass to the SSH keyfunc callback
[ ]  2534       */
[ ]  2535      data->set.ssh_hostkeyfunc_userp = va_arg(param, void *);
[ ]  2536      break;
[ ]  2537  #endif
[ ]  2538    case CURLOPT_SSH_KEYFUNCTION:
[ ]  2539      /* setting to NULL is fine since the ssh.c functions themselves will
[ ]  2540         then revert to use the internal default */
[ ]  2541      data->set.ssh_keyfunc = va_arg(param, curl_sshkeycallback);
[ ]  2542      break;
[ ]  2543  
[ ]  2544    case CURLOPT_SSH_KEYDATA:
[ ]  2545      /*
[ ]  2546       * Custom client data to pass to the SSH keyfunc callback
[ ]  2547       */
[ ]  2548      data->set.ssh_keyfunc_userp = va_arg(param, void *);
[ ]  2549      break;
[ ]  2550  
[ ]  2551    case CURLOPT_SSH_COMPRESSION:
[ ]  2552      data->set.ssh_compression = (0 != va_arg(param, long))?TRUE:FALSE;
[ ]  2553      break;
[ ]  2554  #endif /* USE_SSH */
[ ]  2555  
[ ]  2556    case CURLOPT_HTTP_TRANSFER_DECODING:
[ ]  2557      /*
[ ]  2558       * disable libcurl transfer encoding is used
[ ]  2559       */
[ ]  2560  #ifndef USE_HYPER
[ ]  2561      data->set.http_te_skip = (0 == va_arg(param, long)) ? TRUE : FALSE;
[ ]  2562      break;
[ ]  2563  #else
[ ]  2564      return CURLE_NOT_BUILT_IN; /* hyper doesn't support */
[ ]  2565  #endif
[ ]  2566  
[ ]  2567    case CURLOPT_HTTP_CONTENT_DECODING:
[ ]  2568      /*
[ ]  2569       * raw data passed to the application when content encoding is used
[ ]  2570       */
[ ]  2571      data->set.http_ce_skip = (0 == va_arg(param, long)) ? TRUE : FALSE;
[ ]  2572      break;
[ ]  2573  
[ ]  2574  #if !defined(CURL_DISABLE_FTP) || defined(USE_SSH)
[ ]  2575    case CURLOPT_NEW_FILE_PERMS:
[ ]  2576      /*
[ ]  2577       * Uses these permissions instead of 0644
[ ]  2578       */
[ ]  2579      arg = va_arg(param, long);
[ ]  2580      if((arg < 0) || (arg > 0777))
[ ]  2581        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2582      data->set.new_file_perms = (unsigned int)arg;
[ ]  2583      break;
[ ]  2584  
[ ]  2585    case CURLOPT_NEW_DIRECTORY_PERMS:
[ ]  2586      /*
[ ]  2587       * Uses these permissions instead of 0755
[ ]  2588       */
[ ]  2589      arg = va_arg(param, long);
[ ]  2590      if((arg < 0) || (arg > 0777))
[ ]  2591        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2592      data->set.new_directory_perms = (unsigned int)arg;
[ ]  2593      break;
[ ]  2594  #endif
[ ]  2595  
[ ]  2596  #ifdef ENABLE_IPV6
[ ]  2597    case CURLOPT_ADDRESS_SCOPE:
[ ]  2598      /*
[ ]  2599       * Use this scope id when using IPv6
[ ]  2600       * We always get longs when passed plain numericals so we should check
[ ]  2601       * that the value fits into an unsigned 32 bit integer.
[ ]  2602       */
[ ]  2603      uarg = va_arg(param, unsigned long);
[ ]  2604  #if SIZEOF_LONG > 4
[ ]  2605      if(uarg > UINT_MAX)
[ ]  2606        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2607  #endif
[ ]  2608      data->set.scope_id = (unsigned int)uarg;
[ ]  2609      break;
[ ]  2610  #endif
[ ]  2611  
[ ]  2612    case CURLOPT_PROTOCOLS:
[ ]  2613      /* set the bitmask for the protocols that are allowed to be used for the
[ ]  2614         transfer, which thus helps the app which takes URLs from users or other
[ ]  2615         external inputs and want to restrict what protocol(s) to deal
[ ]  2616         with. Defaults to CURLPROTO_ALL. */
[ ]  2617      data->set.allowed_protocols = (curl_prot_t)va_arg(param, long);
[ ]  2618      break;
[ ]  2619  
[ ]  2620    case CURLOPT_REDIR_PROTOCOLS:
[ ]  2621      /* set the bitmask for the protocols that libcurl is allowed to follow to,
[ ]  2622         as a subset of the CURLOPT_PROTOCOLS ones. That means the protocol needs
[ ]  2623         to be set in both bitmasks to be allowed to get redirected to. */
[ ]  2624      data->set.redir_protocols = (curl_prot_t)va_arg(param, long);
[ ]  2625      break;
[ ]  2626  
[L]  2627    case CURLOPT_PROTOCOLS_STR: {
[L]  2628      curl_prot_t prot;
[L]  2629      argptr = va_arg(param, char *);
[L]  2630      result = protocol2num(argptr, &prot);
[L]  2631      if(result)
[ ]  2632        return result;
[L]  2633      data->set.allowed_protocols = prot;
[L]  2634      break;
[L]  2635    }
[ ]  2636  
[ ]  2637    case CURLOPT_REDIR_PROTOCOLS_STR: {
[ ]  2638      curl_prot_t prot;
[ ]  2639      argptr = va_arg(param, char *);
[ ]  2640      result = protocol2num(argptr, &prot);
[ ]  2641      if(result)
[ ]  2642        return result;
[ ]  2643      data->set.redir_protocols = prot;
[ ]  2644      break;
[ ]  2645    }
[ ]  2646  
[ ]  2647    case CURLOPT_DEFAULT_PROTOCOL:
[ ]  2648      /* Set the protocol to use when the URL doesn't include any protocol */
[ ]  2649      result = Curl_setstropt(&data->set.str[STRING_DEFAULT_PROTOCOL],
[ ]  2650                              va_arg(param, char *));
[ ]  2651      break;
[ ]  2652  #ifndef CURL_DISABLE_SMTP
[ ]  2653    case CURLOPT_MAIL_FROM:
[ ]  2654      /* Set the SMTP mail originator */
[ ]  2655      result = Curl_setstropt(&data->set.str[STRING_MAIL_FROM],
[ ]  2656                              va_arg(param, char *));
[ ]  2657      break;
[ ]  2658  
[ ]  2659    case CURLOPT_MAIL_AUTH:
[ ]  2660      /* Set the SMTP auth originator */
[ ]  2661      result = Curl_setstropt(&data->set.str[STRING_MAIL_AUTH],
[ ]  2662                              va_arg(param, char *));
[ ]  2663      break;
[ ]  2664  
[ ]  2665    case CURLOPT_MAIL_RCPT:
[ ]  2666      /* Set the list of mail recipients */
[ ]  2667      data->set.mail_rcpt = va_arg(param, struct curl_slist *);
[ ]  2668      break;
[ ]  2669    case CURLOPT_MAIL_RCPT_ALLLOWFAILS:
[ ]  2670      /* allow RCPT TO command to fail for some recipients */
[ ]  2671      data->set.mail_rcpt_allowfails = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2672      break;
[ ]  2673  #endif
[ ]  2674  
[ ]  2675    case CURLOPT_SASL_AUTHZID:
[ ]  2676      /* Authorization identity (identity to act as) */
[ ]  2677      result = Curl_setstropt(&data->set.str[STRING_SASL_AUTHZID],
[ ]  2678                              va_arg(param, char *));
[ ]  2679      break;
[ ]  2680  
[ ]  2681    case CURLOPT_SASL_IR:
[ ]  2682      /* Enable/disable SASL initial response */
[ ]  2683      data->set.sasl_ir = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2684      break;
[ ]  2685  #ifndef CURL_DISABLE_RTSP
[L]  2686    case CURLOPT_RTSP_REQUEST:
[L]  2687    {
[ ]  2688      /*
[ ]  2689       * Set the RTSP request method (OPTIONS, SETUP, PLAY, etc...)
[ ]  2690       * Would this be better if the RTSPREQ_* were just moved into here?
[ ]  2691       */
[L]  2692      long in_rtspreq = va_arg(param, long);
[L]  2693      Curl_RtspReq rtspreq = RTSPREQ_NONE;
[L]  2694      switch(in_rtspreq) {
[ ]  2695      case CURL_RTSPREQ_OPTIONS:
[ ]  2696        rtspreq = RTSPREQ_OPTIONS;
[ ]  2697        break;
[ ]  2698  
[ ]  2699      case CURL_RTSPREQ_DESCRIBE:
[ ]  2700        rtspreq = RTSPREQ_DESCRIBE;
[ ]  2701        break;
[ ]  2702  
[ ]  2703      case CURL_RTSPREQ_ANNOUNCE:
[ ]  2704        rtspreq = RTSPREQ_ANNOUNCE;
[ ]  2705        break;
[ ]  2706  
[ ]  2707      case CURL_RTSPREQ_SETUP:
[ ]  2708        rtspreq = RTSPREQ_SETUP;
[ ]  2709        break;
[ ]  2710  
[ ]  2711      case CURL_RTSPREQ_PLAY:
[ ]  2712        rtspreq = RTSPREQ_PLAY;
[ ]  2713        break;
[ ]  2714  
[ ]  2715      case CURL_RTSPREQ_PAUSE:
[ ]  2716        rtspreq = RTSPREQ_PAUSE;
[ ]  2717        break;
[ ]  2718  
[ ]  2719      case CURL_RTSPREQ_TEARDOWN:
[ ]  2720        rtspreq = RTSPREQ_TEARDOWN;
[ ]  2721        break;
[ ]  2722  
[ ]  2723      case CURL_RTSPREQ_GET_PARAMETER:
[ ]  2724        rtspreq = RTSPREQ_GET_PARAMETER;
[ ]  2725        break;
[ ]  2726  
[ ]  2727      case CURL_RTSPREQ_SET_PARAMETER:
[ ]  2728        rtspreq = RTSPREQ_SET_PARAMETER;
[ ]  2729        break;
[ ]  2730  
[ ]  2731      case CURL_RTSPREQ_RECORD:
[ ]  2732        rtspreq = RTSPREQ_RECORD;
[ ]  2733        break;
[ ]  2734  
[ ]  2735      case CURL_RTSPREQ_RECEIVE:
[ ]  2736        rtspreq = RTSPREQ_RECEIVE;
[ ]  2737        break;
[L]  2738      default:
[L]  2739        rtspreq = RTSPREQ_NONE;
[L]  2740      }
[ ]  2741  
[L]  2742      data->set.rtspreq = rtspreq;
[L]  2743      break;
[L]  2744    }
[ ]  2745  
[ ]  2746  
[ ]  2747    case CURLOPT_RTSP_SESSION_ID:
[ ]  2748      /*
[ ]  2749       * Set the RTSP Session ID manually. Useful if the application is
[ ]  2750       * resuming a previously established RTSP session
[ ]  2751       */
[ ]  2752      result = Curl_setstropt(&data->set.str[STRING_RTSP_SESSION_ID],
[ ]  2753                              va_arg(param, char *));
[ ]  2754      break;
[ ]  2755  
[ ]  2756    case CURLOPT_RTSP_STREAM_URI:
[ ]  2757      /*
[ ]  2758       * Set the Stream URI for the RTSP request. Unless the request is
[ ]  2759       * for generic server options, the application will need to set this.
[ ]  2760       */
[ ]  2761      result = Curl_setstropt(&data->set.str[STRING_RTSP_STREAM_URI],
[ ]  2762                              va_arg(param, char *));
[ ]  2763      break;
[ ]  2764  
[ ]  2765    case CURLOPT_RTSP_TRANSPORT:
[ ]  2766      /*
[ ]  2767       * The content of the Transport: header for the RTSP request
[ ]  2768       */
[ ]  2769      result = Curl_setstropt(&data->set.str[STRING_RTSP_TRANSPORT],
[ ]  2770                              va_arg(param, char *));
[ ]  2771      break;
[ ]  2772  
[ ]  2773    case CURLOPT_RTSP_CLIENT_CSEQ:
[ ]  2774      /*
[ ]  2775       * Set the CSEQ number to issue for the next RTSP request. Useful if the
[ ]  2776       * application is resuming a previously broken connection. The CSEQ
[ ]  2777       * will increment from this new number henceforth.
[ ]  2778       */
[ ]  2779      data->state.rtsp_next_client_CSeq = va_arg(param, long);
[ ]  2780      break;
[ ]  2781  
[ ]  2782    case CURLOPT_RTSP_SERVER_CSEQ:
[ ]  2783      /* Same as the above, but for server-initiated requests */
[ ]  2784      data->state.rtsp_next_server_CSeq = va_arg(param, long);
[ ]  2785      break;
[ ]  2786  
[ ]  2787    case CURLOPT_INTERLEAVEDATA:
[ ]  2788      data->set.rtp_out = va_arg(param, void *);
[ ]  2789      break;
[ ]  2790    case CURLOPT_INTERLEAVEFUNCTION:
[ ]  2791      /* Set the user defined RTP write function */
[ ]  2792      data->set.fwrite_rtp = va_arg(param, curl_write_callback);
[ ]  2793      break;
[ ]  2794  #endif
[ ]  2795  #ifndef CURL_DISABLE_FTP
[ ]  2796    case CURLOPT_WILDCARDMATCH:
[ ]  2797      data->set.wildcard_enabled = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2798      break;
[ ]  2799    case CURLOPT_CHUNK_BGN_FUNCTION:
[ ]  2800      data->set.chunk_bgn = va_arg(param, curl_chunk_bgn_callback);
[ ]  2801      break;
[ ]  2802    case CURLOPT_CHUNK_END_FUNCTION:
[ ]  2803      data->set.chunk_end = va_arg(param, curl_chunk_end_callback);
[ ]  2804      break;
[ ]  2805    case CURLOPT_FNMATCH_FUNCTION:
[ ]  2806      data->set.fnmatch = va_arg(param, curl_fnmatch_callback);
[ ]  2807      break;
[ ]  2808    case CURLOPT_CHUNK_DATA:
[ ]  2809      data->wildcard.customptr = va_arg(param, void *);
[ ]  2810      break;
[ ]  2811    case CURLOPT_FNMATCH_DATA:
[ ]  2812      data->set.fnmatch_data = va_arg(param, void *);
[ ]  2813      break;
[ ]  2814  #endif
[ ]  2815  #ifdef USE_TLS_SRP
[ ]  2816    case CURLOPT_TLSAUTH_USERNAME:
[ ]  2817      result = Curl_setstropt(&data->set.str[STRING_TLSAUTH_USERNAME],
[ ]  2818                              va_arg(param, char *));
[ ]  2819      if(data->set.str[STRING_TLSAUTH_USERNAME] &&
[ ]  2820         !data->set.ssl.primary.authtype)
[ ]  2821        data->set.ssl.primary.authtype = CURL_TLSAUTH_SRP; /* default to SRP */
[ ]  2822      break;
[ ]  2823  #ifndef CURL_DISABLE_PROXY
[ ]  2824    case CURLOPT_PROXY_TLSAUTH_USERNAME:
[ ]  2825      result = Curl_setstropt(&data->set.str[STRING_TLSAUTH_USERNAME_PROXY],
[ ]  2826                              va_arg(param, char *));
[ ]  2827      if(data->set.str[STRING_TLSAUTH_USERNAME_PROXY] &&
[ ]  2828         !data->set.proxy_ssl.primary.authtype)
[ ]  2829        data->set.proxy_ssl.primary.authtype = CURL_TLSAUTH_SRP; /* default to
[ ]  2830                                                                    SRP */
[ ]  2831      break;
[ ]  2832  #endif
[ ]  2833    case CURLOPT_TLSAUTH_PASSWORD:
[ ]  2834      result = Curl_setstropt(&data->set.str[STRING_TLSAUTH_PASSWORD],
[ ]  2835                              va_arg(param, char *));
[ ]  2836      if(data->set.str[STRING_TLSAUTH_USERNAME] &&
[ ]  2837         !data->set.ssl.primary.authtype)
[ ]  2838        data->set.ssl.primary.authtype = CURL_TLSAUTH_SRP; /* default */
[ ]  2839      break;
[ ]  2840  #ifndef CURL_DISABLE_PROXY
[ ]  2841    case CURLOPT_PROXY_TLSAUTH_PASSWORD:
[ ]  2842      result = Curl_setstropt(&data->set.str[STRING_TLSAUTH_PASSWORD_PROXY],
[ ]  2843                              va_arg(param, char *));
[ ]  2844      if(data->set.str[STRING_TLSAUTH_USERNAME_PROXY] &&
[ ]  2845         !data->set.proxy_ssl.primary.authtype)
[ ]  2846        data->set.proxy_ssl.primary.authtype = CURL_TLSAUTH_SRP; /* default */
[ ]  2847      break;
[ ]  2848  #endif
[ ]  2849    case CURLOPT_TLSAUTH_TYPE:
[ ]  2850      argptr = va_arg(param, char *);
[ ]  2851      if(!argptr ||
[ ]  2852         strncasecompare(argptr, "SRP", strlen("SRP")))
[ ]  2853        data->set.ssl.primary.authtype = CURL_TLSAUTH_SRP;
[ ]  2854      else
[ ]  2855        data->set.ssl.primary.authtype = CURL_TLSAUTH_NONE;
[ ]  2856      break;
[ ]  2857  #ifndef CURL_DISABLE_PROXY
[ ]  2858    case CURLOPT_PROXY_TLSAUTH_TYPE:
[ ]  2859      argptr = va_arg(param, char *);
[ ]  2860      if(!argptr ||
[ ]  2861         strncasecompare(argptr, "SRP", strlen("SRP")))
[ ]  2862        data->set.proxy_ssl.primary.authtype = CURL_TLSAUTH_SRP;
[ ]  2863      else
[ ]  2864        data->set.proxy_ssl.primary.authtype = CURL_TLSAUTH_NONE;
[ ]  2865      break;
[ ]  2866  #endif
[ ]  2867  #endif
[ ]  2868  #ifdef USE_ARES
[ ]  2869    case CURLOPT_DNS_SERVERS:
[ ]  2870      result = Curl_setstropt(&data->set.str[STRING_DNS_SERVERS],
[ ]  2871                              va_arg(param, char *));
[ ]  2872      if(result)
[ ]  2873        return result;
[ ]  2874      result = Curl_set_dns_servers(data, data->set.str[STRING_DNS_SERVERS]);
[ ]  2875      break;
[ ]  2876    case CURLOPT_DNS_INTERFACE:
[ ]  2877      result = Curl_setstropt(&data->set.str[STRING_DNS_INTERFACE],
[ ]  2878                              va_arg(param, char *));
[ ]  2879      if(result)
[ ]  2880        return result;
[ ]  2881      result = Curl_set_dns_interface(data, data->set.str[STRING_DNS_INTERFACE]);
[ ]  2882      break;
[ ]  2883    case CURLOPT_DNS_LOCAL_IP4:
[ ]  2884      result = Curl_setstropt(&data->set.str[STRING_DNS_LOCAL_IP4],
[ ]  2885                              va_arg(param, char *));
[ ]  2886      if(result)
[ ]  2887        return result;
[ ]  2888      result = Curl_set_dns_local_ip4(data, data->set.str[STRING_DNS_LOCAL_IP4]);
[ ]  2889      break;
[ ]  2890    case CURLOPT_DNS_LOCAL_IP6:
[ ]  2891      result = Curl_setstropt(&data->set.str[STRING_DNS_LOCAL_IP6],
[ ]  2892                              va_arg(param, char *));
[ ]  2893      if(result)
[ ]  2894        return result;
[ ]  2895      result = Curl_set_dns_local_ip6(data, data->set.str[STRING_DNS_LOCAL_IP6]);
[ ]  2896      break;
[ ]  2897  #endif
[ ]  2898    case CURLOPT_TCP_KEEPALIVE:
[ ]  2899      data->set.tcp_keepalive = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2900      break;
[ ]  2901    case CURLOPT_TCP_KEEPIDLE:
[ ]  2902      arg = va_arg(param, long);
[ ]  2903      if(arg < 0)
[ ]  2904        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2905      else if(arg > INT_MAX)
[ ]  2906        arg = INT_MAX;
[ ]  2907      data->set.tcp_keepidle = (int)arg;
[ ]  2908      break;
[ ]  2909    case CURLOPT_TCP_KEEPINTVL:
[ ]  2910      arg = va_arg(param, long);
[ ]  2911      if(arg < 0)
[ ]  2912        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  2913      else if(arg > INT_MAX)
[ ]  2914        arg = INT_MAX;
[ ]  2915      data->set.tcp_keepintvl = (int)arg;
[ ]  2916      break;
[ ]  2917    case CURLOPT_TCP_FASTOPEN:
[ ]  2918  #if defined(CONNECT_DATA_IDEMPOTENT) || defined(MSG_FASTOPEN) || \
[ ]  2919     defined(TCP_FASTOPEN_CONNECT)
[ ]  2920      data->set.tcp_fastopen = (0 != va_arg(param, long))?TRUE:FALSE;
[ ]  2921  #else
[ ]  2922      result = CURLE_NOT_BUILT_IN;
[ ]  2923  #endif
[ ]  2924      break;
[ ]  2925    case CURLOPT_SSL_ENABLE_NPN:
[ ]  2926      break;
[ ]  2927    case CURLOPT_SSL_ENABLE_ALPN:
[ ]  2928      data->set.ssl_enable_alpn = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2929      break;
[ ]  2930  #ifdef USE_UNIX_SOCKETS
[ ]  2931    case CURLOPT_UNIX_SOCKET_PATH:
[ ]  2932      data->set.abstract_unix_socket = FALSE;
[ ]  2933      result = Curl_setstropt(&data->set.str[STRING_UNIX_SOCKET_PATH],
[ ]  2934                              va_arg(param, char *));
[ ]  2935      break;
[ ]  2936    case CURLOPT_ABSTRACT_UNIX_SOCKET:
[ ]  2937      data->set.abstract_unix_socket = TRUE;
[ ]  2938      result = Curl_setstropt(&data->set.str[STRING_UNIX_SOCKET_PATH],
[ ]  2939                              va_arg(param, char *));
[ ]  2940      break;
[ ]  2941  #endif
[ ]  2942  
[ ]  2943    case CURLOPT_PATH_AS_IS:
[ ]  2944      data->set.path_as_is = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2945      break;
[ ]  2946    case CURLOPT_PIPEWAIT:
[ ]  2947      data->set.pipewait = (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2948      break;
[ ]  2949    case CURLOPT_STREAM_WEIGHT:
[ ]  2950  #ifndef USE_NGHTTP2
[ ]  2951      return CURLE_NOT_BUILT_IN;
[ ]  2952  #else
[ ]  2953      arg = va_arg(param, long);
[ ]  2954      if((arg >= 1) && (arg <= 256))
[ ]  2955        data->set.stream_weight = (int)arg;
[ ]  2956      break;
[ ]  2957  #endif
[ ]  2958    case CURLOPT_STREAM_DEPENDS:
[ ]  2959    case CURLOPT_STREAM_DEPENDS_E:
[ ]  2960    {
[ ]  2961  #ifndef USE_NGHTTP2
[ ]  2962      return CURLE_NOT_BUILT_IN;
[ ]  2963  #else
[ ]  2964      struct Curl_easy *dep = va_arg(param, struct Curl_easy *);
[ ]  2965      if(!dep || GOOD_EASY_HANDLE(dep)) {
[ ]  2966        if(data->set.stream_depends_on) {
[ ]  2967          Curl_http2_remove_child(data->set.stream_depends_on, data);
[ ]  2968        }
[ ]  2969        Curl_http2_add_child(dep, data, (option == CURLOPT_STREAM_DEPENDS_E));
[ ]  2970      }
[ ]  2971      break;
[ ]  2972  #endif
[ ]  2973    }
[L]  2974    case CURLOPT_CONNECT_TO:
[L]  2975      data->set.connect_to = va_arg(param, struct curl_slist *);
[L]  2976      break;
[ ]  2977    case CURLOPT_SUPPRESS_CONNECT_HEADERS:
[ ]  2978      data->set.suppress_connect_headers = (0 != va_arg(param, long))?TRUE:FALSE;
[ ]  2979      break;
[ ]  2980    case CURLOPT_HAPPY_EYEBALLS_TIMEOUT_MS:
[ ]  2981      uarg = va_arg(param, unsigned long);
[ ]  2982      if(uarg >= UINT_MAX)
[ ]  2983        uarg = UINT_MAX;
[ ]  2984      data->set.happy_eyeballs_timeout = (unsigned int)uarg;
[ ]  2985      break;
[ ]  2986  #ifndef CURL_DISABLE_SHUFFLE_DNS
[ ]  2987    case CURLOPT_DNS_SHUFFLE_ADDRESSES:
[ ]  2988      data->set.dns_shuffle_addresses = (0 != va_arg(param, long)) ? TRUE:FALSE;
[ ]  2989      break;
[ ]  2990  #endif
[ ]  2991    case CURLOPT_DISALLOW_USERNAME_IN_URL:
[ ]  2992      data->set.disallow_username_in_url =
[ ]  2993        (0 != va_arg(param, long)) ? TRUE : FALSE;
[ ]  2994      break;
[ ]  2995  #ifndef CURL_DISABLE_DOH
[ ]  2996    case CURLOPT_DOH_URL:
[ ]  2997      result = Curl_setstropt(&data->set.str[STRING_DOH],
[ ]  2998                              va_arg(param, char *));
[ ]  2999      data->set.doh = data->set.str[STRING_DOH]?TRUE:FALSE;
[ ]  3000      break;
[ ]  3001  #endif
[ ]  3002    case CURLOPT_UPKEEP_INTERVAL_MS:
[ ]  3003      arg = va_arg(param, long);
[ ]  3004      if(arg < 0)
[ ]  3005        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  3006      data->set.upkeep_interval_ms = arg;
[ ]  3007      break;
[ ]  3008    case CURLOPT_MAXAGE_CONN:
[ ]  3009      arg = va_arg(param, long);
[ ]  3010      if(arg < 0)
[ ]  3011        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  3012      data->set.maxage_conn = arg;
[ ]  3013      break;
[ ]  3014    case CURLOPT_MAXLIFETIME_CONN:
[ ]  3015      arg = va_arg(param, long);
[ ]  3016      if(arg < 0)
[ ]  3017        return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  3018      data->set.maxlifetime_conn = arg;
[ ]  3019      break;
[ ]  3020    case CURLOPT_TRAILERFUNCTION:
[ ]  3021  #ifndef CURL_DISABLE_HTTP
[ ]  3022      data->set.trailer_callback = va_arg(param, curl_trailer_callback);
[ ]  3023  #endif
[ ]  3024      break;
[ ]  3025    case CURLOPT_TRAILERDATA:
[ ]  3026  #ifndef CURL_DISABLE_HTTP
[ ]  3027      data->set.trailer_data = va_arg(param, void *);
[ ]  3028  #endif
[ ]  3029      break;
[ ]  3030  #ifndef CURL_DISABLE_HSTS
[ ]  3031    case CURLOPT_HSTSREADFUNCTION:
[ ]  3032      data->set.hsts_read = va_arg(param, curl_hstsread_callback);
[ ]  3033      break;
[ ]  3034    case CURLOPT_HSTSREADDATA:
[ ]  3035      data->set.hsts_read_userp = va_arg(param, void *);
[ ]  3036      break;
[ ]  3037    case CURLOPT_HSTSWRITEFUNCTION:
[ ]  3038      data->set.hsts_write = va_arg(param, curl_hstswrite_callback);
[ ]  3039      break;
[ ]  3040    case CURLOPT_HSTSWRITEDATA:
[ ]  3041      data->set.hsts_write_userp = va_arg(param, void *);
[ ]  3042      break;
[L]  3043    case CURLOPT_HSTS:
[L]  3044      if(!data->hsts) {
[L]  3045        data->hsts = Curl_hsts_init();
[L]  3046        if(!data->hsts)
[ ]  3047          return CURLE_OUT_OF_MEMORY;
[L]  3048      }
[L]  3049      argptr = va_arg(param, char *);
[L]  3050      result = Curl_setstropt(&data->set.str[STRING_HSTS], argptr);
[L]  3051      if(result)
[ ]  3052        return result;
[L]  3053      if(argptr)
[L]  3054        (void)Curl_hsts_loadfile(data, data->hsts, argptr);
[L]  3055      break;
[ ]  3056    case CURLOPT_HSTS_CTRL:
[ ]  3057      arg = va_arg(param, long);
[ ]  3058      if(arg & CURLHSTS_ENABLE) {
[ ]  3059        if(!data->hsts) {
[ ]  3060          data->hsts = Curl_hsts_init();
[ ]  3061          if(!data->hsts)
[ ]  3062            return CURLE_OUT_OF_MEMORY;
[ ]  3063        }
[ ]  3064      }
[ ]  3065      else
[ ]  3066        Curl_hsts_cleanup(&data->hsts);
[ ]  3067      break;
[ ]  3068  #endif
[ ]  3069  #ifndef CURL_DISABLE_ALTSVC
[L]  3070    case CURLOPT_ALTSVC:
[L]  3071      if(!data->asi) {
[L]  3072        data->asi = Curl_altsvc_init();
[L]  3073        if(!data->asi)
[ ]  3074          return CURLE_OUT_OF_MEMORY;
[L]  3075      }
[L]  3076      argptr = va_arg(param, char *);
[L]  3077      result = Curl_setstropt(&data->set.str[STRING_ALTSVC], argptr);
[L]  3078      if(result)
[ ]  3079        return result;
[L]  3080      if(argptr)
[L]  3081        (void)Curl_altsvc_load(data->asi, argptr);
[L]  3082      break;
[ ]  3083    case CURLOPT_ALTSVC_CTRL:
[ ]  3084      if(!data->asi) {
[ ]  3085        data->asi = Curl_altsvc_init();
[ ]  3086        if(!data->asi)
[ ]  3087          return CURLE_OUT_OF_MEMORY;
[ ]  3088      }
[ ]  3089      arg = va_arg(param, long);
[ ]  3090      result = Curl_altsvc_ctrl(data->asi, arg);
[ ]  3091      if(result)
[ ]  3092        return result;
[ ]  3093      break;
[ ]  3094  #endif
[ ]  3095    case CURLOPT_PREREQFUNCTION:
[ ]  3096      data->set.fprereq = va_arg(param, curl_prereq_callback);
[ ]  3097      break;
[ ]  3098    case CURLOPT_PREREQDATA:
[ ]  3099      data->set.prereq_userp = va_arg(param, void *);
[ ]  3100      break;
[ ]  3101  #ifdef USE_WEBSOCKETS
[ ]  3102    case CURLOPT_WS_OPTIONS: {
[ ]  3103      bool raw;
[ ]  3104      arg = va_arg(param, long);
[ ]  3105      raw = (arg & CURLWS_RAW_MODE);
[ ]  3106      data->set.ws_raw_mode = raw;
[ ]  3107      break;
[ ]  3108    }
[ ]  3109  #endif
[W]  3110    default: <-- BLOCKER
[ ]  3111      /* unknown tag and its companion, just ignore: */
[W]  3112      result = CURLE_UNKNOWN_OPTION;
[W]  3113      break;
[B]  3114    }
[ ]  3115  
[B]  3116    return result;
[B]  3117  }

--- Caller (1 hop): curl_easy_setopt (/src/curl/lib/setopt.c:3129-3142, calls Curl_vsetopt at line 3138) (full body — short) ---
[B]  3129  {
[B]  3130    va_list arg;
[B]  3131    CURLcode result;
[ ]  3132  
[B]  3133    if(!data)
[ ]  3134      return CURLE_BAD_FUNCTION_ARGUMENT;
[ ]  3135  
[B]  3136    va_start(arg, tag);
[ ]  3137  
[B]  3138    result = Curl_vsetopt(data, tag, arg); <-- CALL
[ ]  3139  
[B]  3140    va_end(arg);
[B]  3141    return result;
[B]  3142  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  curl_easy_setopt  (/src/curl/lib/setopt.c:3129-3142, calls Curl_vsetopt at line 3138)
hop 3  doh.c:dohprobe  (/src/curl/lib/doh.c:219-354, calls curl_easy_setopt at line 330)
hop 4  Curl_doh  (/src/curl/lib/doh.c:365-418, calls doh.c:dohprobe at line 392)
hop 5  Curl_resolv  (/src/curl/lib/hostip.c:648-814, calls Curl_doh at line 766)
hop 6  Curl_SOCKS4  (/src/curl/lib/socks.c:197-483, calls Curl_resolv at line 244)
hop 7  connect.c:connect_SOCKS  (/src/curl/lib/connect.c:783-834, calls Curl_SOCKS4 at line 813)
hop 8  Curl_is_connected  (/src/curl/lib/connect.c:863-1085, calls connect.c:connect_SOCKS at line 885)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       6       352  Curl_vsetopt  (/src/curl/lib/setopt.c:190-3117)  <-- enclosing
       6       352  curl_easy_setopt  (/src/curl/lib/setopt.c:3129-3142)
      10       277  Curl_setstropt  (/src/curl/lib/setopt.c:60-76)
       0        19  setopt.c:protocol2num  (/src/curl/lib/setopt.c:152-183)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  curl_easy_setopt  (/src/curl/lib/setopt.c:3129-3142) ---
  d=2   L3133  T=0 F=6  T=0 F=352  if(!data)
--- d=1  Curl_vsetopt  (/src/curl/lib/setopt.c:190-3117) ---
  d=1   L 198  T=0 F=6  T=0 F=352  case CURLOPT_DNS_CACHE_TIMEOUT:
  d=1   L 207  T=0 F=6  T=0 F=352  case CURLOPT_DNS_USE_GLOBAL_CACHE:
  d=1   L 210  T=0 F=6  T=0 F=352  case CURLOPT_SSL_CIPHER_LIST:
  d=1   L 216  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSL_CIPHER_LIST:
  d=1   L 222  T=0 F=6  T=0 F=352  case CURLOPT_TLS13_CIPHERS:
  d=1   L 232  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_TLS13_CIPHERS:
  d=1   L 242  T=0 F=6  T=0 F=352  case CURLOPT_RANDOM_FILE:
  d=1   L 244  T=0 F=6  T=0 F=352  case CURLOPT_EGDSOCKET:
  d=1   L 246  T=0 F=6  T=0 F=352  case CURLOPT_MAXCONNECTS:
  d=1   L 256  T=0 F=6  T=0 F=352  case CURLOPT_FORBID_REUSE:
  d=1   L 263  T=0 F=6  T=0 F=352  case CURLOPT_FRESH_CONNECT:
  d=1   L 270  T=0 F=6  T=0 F=352  case CURLOPT_VERBOSE:
  d=1   L 277  T=0 F=6  T=0 F=352  case CURLOPT_HEADER:
  d=1   L 283  T=0 F=6  T=0 F=352  case CURLOPT_NOPROGRESS:
  d=1   L 293  T=0 F=6  T=0 F=352  case CURLOPT_NOBODY:
  d=1   L 306  T=0 F=6  T=0 F=352  case CURLOPT_FAILONERROR:
  d=1   L 313  T=0 F=6  T=0 F=352  case CURLOPT_KEEP_SENDING_ON_ERROR:
  d=1   L 317  T=0 F=6  T=0 F=352  case CURLOPT_UPLOAD:
  d=1   L 318  T=0 F=6  T=0 F=352  case CURLOPT_PUT:
  d=1   L 334  T=0 F=6  T=0 F=352  case CURLOPT_REQUEST_TARGET:
  d=1   L 338  T=0 F=6  T=0 F=352  case CURLOPT_FILETIME:
  d=1   L 345  T=0 F=6  T=19 F=333  case CURLOPT_SERVER_RESPONSE_TIMEOUT:
  d=1   L 351  T=0 F=0  T=19 F=0  if((arg >= 0) && (arg <= (INT_MAX/1000)))
  d=1   L 351  T=0 F=0  T=19 F=0  if((arg >= 0) && (arg <= (INT_MAX/1000)))
  d=1   L 357  T=0 F=6  T=0 F=352  case CURLOPT_TFTP_NO_OPTIONS:
  d=1   L 364  T=0 F=6  T=0 F=352  case CURLOPT_TFTP_BLKSIZE:
  d=1   L 375  T=0 F=6  T=0 F=352  case CURLOPT_NETRC:
  d=1   L 384  T=0 F=6  T=19 F=333  case CURLOPT_NETRC_FILE:
  d=1   L 392  T=0 F=6  T=0 F=352  case CURLOPT_TRANSFERTEXT:
  d=1   L 401  T=0 F=6  T=0 F=352  case CURLOPT_TIMECONDITION:
  d=1   L 411  T=0 F=6  T=0 F=352  case CURLOPT_TIMEVALUE:
  d=1   L 419  T=0 F=6  T=0 F=352  case CURLOPT_TIMEVALUE_LARGE:
  d=1   L 427  T=0 F=6  T=0 F=352  case CURLOPT_SSLVERSION:
  d=1   L 429  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSLVERSION:
  d=1   L 467  T=0 F=6  T=0 F=352  case CURLOPT_COPYPOSTFIELDS:
  d=1   L 514  T=1 F=5  T=1 F=351  case CURLOPT_POSTFIELDS:
  d=1   L 524  T=0 F=6  T=0 F=352  case CURLOPT_POSTFIELDSIZE:
  d=1   L 543  T=0 F=6  T=0 F=352  case CURLOPT_POSTFIELDSIZE_LARGE:
  d=1   L 563  T=0 F=6  T=0 F=352  case CURLOPT_AUTOREFERER:
  d=1   L 570  T=0 F=6  T=0 F=352  case CURLOPT_ACCEPT_ENCODING:
  d=1   L 594  T=0 F=6  T=0 F=352  case CURLOPT_TRANSFER_ENCODING:
  d=1   L 599  T=0 F=6  T=0 F=352  case CURLOPT_FOLLOWLOCATION:
  d=1   L 606  T=0 F=6  T=0 F=352  case CURLOPT_UNRESTRICTED_AUTH:
  d=1   L 615  T=0 F=6  T=0 F=352  case CURLOPT_MAXREDIRS:
  d=1   L 626  T=0 F=6  T=0 F=352  case CURLOPT_POSTREDIR:
  d=1   L 644  T=0 F=6  T=0 F=352  case CURLOPT_POST:
  d=1   L 658  T=0 F=6  T=2 F=350  case CURLOPT_HTTPPOST:
  d=1   L 668  T=0 F=6  T=0 F=352  case CURLOPT_AWS_SIGV4:
  d=1   L 682  T=0 F=6  T=0 F=352  case CURLOPT_REFERER:
  d=1   L 695  T=0 F=6  T=0 F=352  case CURLOPT_USERAGENT:
  d=1   L 704  T=0 F=6  T=0 F=352  case CURLOPT_PROXYHEADER:
  d=1   L 718  T=0 F=6  T=0 F=352  case CURLOPT_HEADEROPT:
  d=1   L 726  T=0 F=6  T=0 F=352  case CURLOPT_HTTP200ALIASES:
  d=1   L 734  T=0 F=6  T=1 F=351  case CURLOPT_COOKIE:
  d=1   L 742  T=0 F=6  T=19 F=333  case CURLOPT_COOKIEFILE:
  d=1   L 747  T=0 F=0  T=19 F=0  if(argptr) {
  d=1   L 750  T=0 F=0  T=0 F=19  if(strlen(argptr) > CURL_MAX_INPUT_LENGTH)
  d=1   L 755  T=0 F=0  T=0 F=19  if(!cl) {
  d=1   L 778  T=0 F=6  T=19 F=333  case CURLOPT_COOKIEJAR:
  d=1   L 793  T=0 F=0  T=0 F=19  if(!newcookies)
  d=1   L 799  T=0 F=6  T=0 F=352  case CURLOPT_COOKIESESSION:
  d=1   L 818  T=0 F=6  T=0 F=352  case CURLOPT_COOKIELIST:
  d=1   L 879  T=0 F=6  T=0 F=352  case CURLOPT_HTTPGET:
  d=1   L 890  T=0 F=6  T=0 F=352  case CURLOPT_HTTP_VERSION:
  d=1   L 915  T=0 F=6  T=0 F=352  case CURLOPT_EXPECT_100_TIMEOUT_MS:
  d=1   L 926  T=0 F=6  T=0 F=352  case CURLOPT_HTTP09_ALLOWED:
  d=1   L 943  T=0 F=6  T=2 F=350  case CURLOPT_HTTPHEADER:
  d=1   L 952  T=0 F=6  T=0 F=352  case CURLOPT_MIMEPOST:
  d=1   L 964  T=0 F=6  T=0 F=352  case CURLOPT_MIME_OPTIONS:
  d=1   L 970  T=0 F=6  T=0 F=352  case CURLOPT_HTTPAUTH:
  d=1   L1022  T=0 F=6  T=1 F=351  case CURLOPT_CUSTOMREQUEST:
  d=1   L1036  T=0 F=6  T=0 F=352  case CURLOPT_HTTPPROXYTUNNEL:
  d=1   L1044  T=0 F=6  T=0 F=352  case CURLOPT_PROXYPORT:
  d=1   L1054  T=0 F=6  T=0 F=352  case CURLOPT_PROXYAUTH:
  d=1   L1105  T=0 F=6  T=0 F=352  case CURLOPT_PROXY:
  d=1   L1120  T=0 F=6  T=0 F=352  case CURLOPT_PRE_PROXY:
  d=1   L1131  T=0 F=6  T=0 F=352  case CURLOPT_PROXYTYPE:
  d=1   L1141  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_TRANSFER_MODE:
  d=1   L1159  T=0 F=6  T=0 F=352  case CURLOPT_SOCKS5_AUTH:
  d=1   L1175  T=0 F=6  T=0 F=352  case CURLOPT_SOCKS5_GSSAPI_SERVICE:
  d=1   L1176  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SERVICE_NAME:
  d=1   L1184  T=0 F=6  T=0 F=352  case CURLOPT_SERVICE_NAME:
  d=1   L1192  T=0 F=6  T=0 F=352  case CURLOPT_HEADERDATA:
  d=1   L1198  T=0 F=6  T=0 F=352  case CURLOPT_ERRORBUFFER:
  d=1   L1205  T=0 F=6  T=19 F=333  case CURLOPT_WRITEDATA:
  d=1   L1213  T=0 F=6  T=0 F=352  case CURLOPT_DIRLISTONLY:
  d=1   L1221  T=0 F=6  T=0 F=352  case CURLOPT_APPEND:
  d=1   L1230  T=0 F=6  T=0 F=352  case CURLOPT_FTP_FILEMETHOD:
  d=1   L1239  T=0 F=6  T=0 F=352  case CURLOPT_FTPPORT:
  d=1   L1248  T=0 F=6  T=0 F=352  case CURLOPT_FTP_USE_EPRT:
  d=1   L1252  T=0 F=6  T=0 F=352  case CURLOPT_FTP_USE_EPSV:
  d=1   L1256  T=0 F=6  T=0 F=352  case CURLOPT_FTP_USE_PRET:
  d=1   L1260  T=0 F=6  T=0 F=352  case CURLOPT_FTP_SSL_CCC:
  d=1   L1267  T=0 F=6  T=0 F=352  case CURLOPT_FTP_SKIP_PASV_IP:
  d=1   L1275  T=0 F=6  T=0 F=352  case CURLOPT_FTP_ACCOUNT:
  d=1   L1280  T=0 F=6  T=0 F=352  case CURLOPT_FTP_ALTERNATIVE_TO_USER:
  d=1   L1285  T=0 F=6  T=0 F=352  case CURLOPT_FTPSSLAUTH:
  d=1   L1294  T=0 F=6  T=0 F=352  case CURLOPT_KRBLEVEL:
  d=1   L1303  T=0 F=6  T=0 F=352  case CURLOPT_FTP_CREATE_MISSING_DIRS:
  d=1   L1316  T=0 F=6  T=19 F=333  case CURLOPT_READDATA:
  d=1   L1323  T=0 F=6  T=0 F=352  case CURLOPT_INFILESIZE:
  d=1   L1333  T=0 F=6  T=0 F=352  case CURLOPT_INFILESIZE_LARGE:
  d=1   L1343  T=0 F=6  T=0 F=352  case CURLOPT_LOW_SPEED_LIMIT:
  d=1   L1353  T=0 F=6  T=0 F=352  case CURLOPT_MAX_SEND_SPEED_LARGE:
  d=1   L1363  T=0 F=6  T=0 F=352  case CURLOPT_MAX_RECV_SPEED_LARGE:
  d=1   L1373  T=0 F=6  T=0 F=352  case CURLOPT_LOW_SPEED_TIME:
  d=1   L1383  T=0 F=6  T=0 F=352  case CURLOPT_CURLU:
  d=1   L1389  T=1 F=5  T=19 F=333  case CURLOPT_URL:
  d=1   L1393  T=0 F=1  T=0 F=19  if(data->state.url_alloc) {
  d=1   L1402  T=0 F=6  T=0 F=352  case CURLOPT_PORT:
  d=1   L1411  T=0 F=6  T=0 F=352  case CURLOPT_TIMEOUT:
  d=1   L1423  T=0 F=6  T=19 F=333  case CURLOPT_TIMEOUT_MS:
  d=1   L1425  T=0 F=0  T=0 F=19  if(uarg >= UINT_MAX)
  d=1   L1430  T=0 F=6  T=0 F=352  case CURLOPT_CONNECTTIMEOUT:
  d=1   L1441  T=0 F=6  T=0 F=352  case CURLOPT_CONNECTTIMEOUT_MS:
  d=1   L1449  T=0 F=6  T=0 F=352  case CURLOPT_ACCEPTTIMEOUT_MS:
  d=1   L1460  T=0 F=6  T=0 F=352  case CURLOPT_USERPWD:
  d=1   L1469  T=0 F=6  T=1 F=351  case CURLOPT_USERNAME:
  d=1   L1476  T=0 F=6  T=1 F=351  case CURLOPT_PASSWORD:
  d=1   L1484  T=0 F=6  T=0 F=352  case CURLOPT_LOGIN_OPTIONS:
  d=1   L1492  T=0 F=6  T=0 F=352  case CURLOPT_XOAUTH2_BEARER:
  d=1   L1500  T=0 F=6  T=0 F=352  case CURLOPT_POSTQUOTE:
  d=1   L1506  T=0 F=6  T=0 F=352  case CURLOPT_PREQUOTE:
  d=1   L1512  T=0 F=6  T=0 F=352  case CURLOPT_QUOTE:
  d=1   L1518  T=0 F=6  T=0 F=352  case CURLOPT_RESOLVE:
  d=1   L1535  T=0 F=6  T=0 F=352  case CURLOPT_PROGRESSFUNCTION:
  d=1   L1546  T=0 F=6  T=0 F=352  case CURLOPT_XFERINFOFUNCTION:
  d=1   L1558  T=0 F=6  T=0 F=352  case CURLOPT_PROGRESSDATA:
  d=1   L1566  T=0 F=6  T=0 F=352  case CURLOPT_PROXYUSERPWD:
  d=1   L1574  T=0 F=6  T=0 F=352  case CURLOPT_PROXYUSERNAME:
  d=1   L1581  T=0 F=6  T=0 F=352  case CURLOPT_PROXYPASSWORD:
  d=1   L1588  T=0 F=6  T=0 F=352  case CURLOPT_NOPROXY:
  d=1   L1597  T=0 F=6  T=0 F=352  case CURLOPT_RANGE:
  d=1   L1604  T=0 F=6  T=0 F=352  case CURLOPT_RESUME_FROM:
  d=1   L1613  T=0 F=6  T=0 F=352  case CURLOPT_RESUME_FROM_LARGE:
  d=1   L1622  T=0 F=6  T=0 F=352  case CURLOPT_DEBUGFUNCTION:
  d=1   L1631  T=0 F=6  T=0 F=352  case CURLOPT_DEBUGDATA:
  d=1   L1638  T=0 F=6  T=0 F=352  case CURLOPT_STDERR:
  d=1   L1647  T=0 F=6  T=0 F=352  case CURLOPT_HEADERFUNCTION:
  d=1   L1653  T=0 F=6  T=19 F=333  case CURLOPT_WRITEFUNCTION:
  d=1   L1658  T=0 F=0  T=0 F=19  if(!data->set.fwrite_func)
  d=1   L1662  T=0 F=6  T=19 F=333  case CURLOPT_READFUNCTION:
  d=1   L1667  T=0 F=0  T=0 F=19  if(!data->set.fread_func_set) {
  d=1   L1675  T=0 F=6  T=0 F=352  case CURLOPT_SEEKFUNCTION:
  d=1   L1681  T=0 F=6  T=0 F=352  case CURLOPT_SEEKDATA:
  d=1   L1687  T=0 F=6  T=0 F=352  case CURLOPT_IOCTLFUNCTION:
  d=1   L1693  T=0 F=6  T=0 F=352  case CURLOPT_IOCTLDATA:
  d=1   L1699  T=0 F=6  T=0 F=352  case CURLOPT_SSLCERT:
  d=1   L1706  T=0 F=6  T=0 F=352  case CURLOPT_SSLCERT_BLOB:
  d=1   L1714  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSLCERT:
  d=1   L1721  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSLCERT_BLOB:
  d=1   L1729  T=0 F=6  T=0 F=352  case CURLOPT_SSLCERTTYPE:
  d=1   L1737  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSLCERTTYPE:
  d=1   L1745  T=0 F=6  T=0 F=352  case CURLOPT_SSLKEY:
  d=1   L1752  T=0 F=6  T=0 F=352  case CURLOPT_SSLKEY_BLOB:
  d=1   L1760  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSLKEY:
  d=1   L1767  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSLKEY_BLOB:
  d=1   L1775  T=0 F=6  T=0 F=352  case CURLOPT_SSLKEYTYPE:
  d=1   L1783  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSLKEYTYPE:
  d=1   L1791  T=0 F=6  T=0 F=352  case CURLOPT_KEYPASSWD:
  d=1   L1799  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_KEYPASSWD:
  d=1   L1807  T=0 F=6  T=0 F=352  case CURLOPT_SSLENGINE:
  d=1   L1820  T=0 F=6  T=0 F=352  case CURLOPT_SSLENGINE_DEFAULT:
  d=1   L1827  T=0 F=6  T=0 F=352  case CURLOPT_CRLF:
  d=1   L1834  T=0 F=6  T=0 F=352  case CURLOPT_HAPROXYPROTOCOL:
  d=1   L1841  T=0 F=6  T=0 F=352  case CURLOPT_INTERFACE:
  d=1   L1849  T=0 F=6  T=0 F=352  case CURLOPT_LOCALPORT:
  d=1   L1858  T=0 F=6  T=0 F=352  case CURLOPT_LOCALPORTRANGE:
  d=1   L1867  T=0 F=6  T=0 F=352  case CURLOPT_GSSAPI_DELEGATION:
  d=1   L1876  T=0 F=6  T=0 F=352  case CURLOPT_SSL_VERIFYPEER:
  d=1   L1890  T=0 F=6  T=0 F=352  case CURLOPT_DOH_SSL_VERIFYPEER:
  d=1   L1899  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSL_VERIFYPEER:
  d=1   L1913  T=0 F=6  T=0 F=352  case CURLOPT_SSL_VERIFYHOST:
  d=1   L1931  T=0 F=6  T=0 F=352  case CURLOPT_DOH_SSL_VERIFYHOST:
  d=1   L1942  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSL_VERIFYHOST:
  d=1   L1958  T=0 F=6  T=0 F=352  case CURLOPT_SSL_VERIFYSTATUS:
  d=1   L1977  T=0 F=6  T=0 F=352  case CURLOPT_DOH_SSL_VERIFYSTATUS:
  d=1   L1990  T=0 F=6  T=0 F=352  case CURLOPT_SSL_CTX_FUNCTION:
  d=1   L2001  T=0 F=6  T=0 F=352  case CURLOPT_SSL_CTX_DATA:
  d=1   L2012  T=0 F=6  T=0 F=352  case CURLOPT_SSL_FALSESTART:
  d=1   L2023  T=0 F=6  T=0 F=352  case CURLOPT_CERTINFO:
  d=1   L2031  T=0 F=6  T=0 F=352  case CURLOPT_PINNEDPUBLICKEY:
  d=1   L2045  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_PINNEDPUBLICKEY:
  d=1   L2059  T=0 F=6  T=0 F=352  case CURLOPT_CAINFO:
  d=1   L2066  T=0 F=6  T=0 F=352  case CURLOPT_CAINFO_BLOB:
  d=1   L2081  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_CAINFO:
  d=1   L2089  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_CAINFO_BLOB:
  d=1   L2103  T=0 F=6  T=0 F=352  case CURLOPT_CAPATH:
  d=1   L2118  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_CAPATH:
  d=1   L2133  T=0 F=6  T=19 F=333  case CURLOPT_CRLFILE:
  d=1   L2142  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_CRLFILE:
  d=1   L2151  T=0 F=6  T=0 F=352  case CURLOPT_ISSUERCERT:
  d=1   L2159  T=0 F=6  T=0 F=352  case CURLOPT_ISSUERCERT_BLOB:
  d=1   L2167  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_ISSUERCERT:
  d=1   L2175  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_ISSUERCERT_BLOB:
  d=1   L2184  T=0 F=6  T=0 F=352  case CURLOPT_TELNETOPTIONS:
  d=1   L2191  T=0 F=6  T=0 F=352  case CURLOPT_BUFFERSIZE:
  d=1   L2211  T=0 F=6  T=0 F=352  case CURLOPT_UPLOAD_BUFFERSIZE:
  d=1   L2227  T=0 F=6  T=0 F=352  case CURLOPT_NOSIGNAL:
  d=1   L2235  T=0 F=6  T=0 F=352  case CURLOPT_SHARE:
  d=1   L2306  T=0 F=6  T=0 F=352  case CURLOPT_PRIVATE:
  d=1   L2313  T=0 F=6  T=0 F=352  case CURLOPT_MAXFILESIZE:
  d=1   L2324  T=0 F=6  T=0 F=352  case CURLOPT_USE_SSL:
  d=1   L2334  T=0 F=6  T=0 F=352  case CURLOPT_SSL_OPTIONS:
  d=1   L2348  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_SSL_OPTIONS:
  d=1   L2362  T=0 F=6  T=0 F=352  case CURLOPT_SSL_EC_CURVES:
  d=1   L2371  T=0 F=6  T=0 F=352  case CURLOPT_IPRESOLVE:
  d=1   L2378  T=0 F=6  T=0 F=352  case CURLOPT_MAXFILESIZE_LARGE:
  d=1   L2388  T=0 F=6  T=0 F=352  case CURLOPT_TCP_NODELAY:
  d=1   L2396  T=0 F=6  T=0 F=352  case CURLOPT_IGNORE_CONTENT_LENGTH:
  d=1   L2400  T=0 F=6  T=0 F=352  case CURLOPT_CONNECT_ONLY:
  d=1   L2412  T=0 F=6  T=19 F=333  case CURLOPT_SOCKOPTFUNCTION:
  d=1   L2419  T=0 F=6  T=0 F=352  case CURLOPT_SOCKOPTDATA:
  d=1   L2426  T=0 F=6  T=19 F=333  case CURLOPT_OPENSOCKETFUNCTION:
  d=1   L2434  T=0 F=6  T=19 F=333  case CURLOPT_OPENSOCKETDATA:
  d=1   L2441  T=0 F=6  T=0 F=352  case CURLOPT_CLOSESOCKETFUNCTION:
  d=1   L2449  T=0 F=6  T=0 F=352  case CURLOPT_RESOLVER_START_FUNCTION:
  d=1   L2457  T=0 F=6  T=0 F=352  case CURLOPT_RESOLVER_START_DATA:
  d=1   L2464  T=0 F=6  T=0 F=352  case CURLOPT_CLOSESOCKETDATA:
  d=1   L2471  T=0 F=6  T=0 F=352  case CURLOPT_SSL_SESSIONID_CACHE:
  d=1   L2556  T=0 F=6  T=0 F=352  case CURLOPT_HTTP_TRANSFER_DECODING:
  d=1   L2567  T=0 F=6  T=0 F=352  case CURLOPT_HTTP_CONTENT_DECODING:
  d=1   L2575  T=0 F=6  T=0 F=352  case CURLOPT_NEW_FILE_PERMS:
  d=1   L2585  T=0 F=6  T=0 F=352  case CURLOPT_NEW_DIRECTORY_PERMS:
  d=1   L2597  T=0 F=6  T=0 F=352  case CURLOPT_ADDRESS_SCOPE:
  d=1   L2612  T=0 F=6  T=0 F=352  case CURLOPT_PROTOCOLS:
  d=1   L2620  T=0 F=6  T=0 F=352  case CURLOPT_REDIR_PROTOCOLS:
  d=1   L2627  T=0 F=6  T=19 F=333  case CURLOPT_PROTOCOLS_STR: {
  d=1   L2631  T=0 F=0  T=0 F=19  if(result)
  d=1   L2637  T=0 F=6  T=0 F=352  case CURLOPT_REDIR_PROTOCOLS_STR: {
  d=1   L2647  T=0 F=6  T=0 F=352  case CURLOPT_DEFAULT_PROTOCOL:
  d=1   L2653  T=0 F=6  T=0 F=352  case CURLOPT_MAIL_FROM:
  d=1   L2659  T=0 F=6  T=0 F=352  case CURLOPT_MAIL_AUTH:
  d=1   L2665  T=0 F=6  T=0 F=352  case CURLOPT_MAIL_RCPT:
  d=1   L2669  T=0 F=6  T=0 F=352  case CURLOPT_MAIL_RCPT_ALLLOWFAILS:
  d=1   L2675  T=0 F=6  T=0 F=352  case CURLOPT_SASL_AUTHZID:
  d=1   L2681  T=0 F=6  T=0 F=352  case CURLOPT_SASL_IR:
  d=1   L2686  T=0 F=6  T=1 F=351  case CURLOPT_RTSP_REQUEST:
  d=1   L2695  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_OPTIONS:
  d=1   L2699  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_DESCRIBE:
  d=1   L2703  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_ANNOUNCE:
  d=1   L2707  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_SETUP:
  d=1   L2711  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_PLAY:
  d=1   L2715  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_PAUSE:
  d=1   L2719  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_TEARDOWN:
  d=1   L2723  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_GET_PARAMETER:
  d=1   L2727  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_SET_PARAMETER:
  d=1   L2731  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_RECORD:
  d=1   L2735  T=0 F=0  T=0 F=1  case CURL_RTSPREQ_RECEIVE:
  d=1   L2738  T=0 F=0  T=1 F=0  default:
  d=1   L2747  T=0 F=6  T=0 F=352  case CURLOPT_RTSP_SESSION_ID:
  d=1   L2756  T=0 F=6  T=0 F=352  case CURLOPT_RTSP_STREAM_URI:
  d=1   L2765  T=0 F=6  T=0 F=352  case CURLOPT_RTSP_TRANSPORT:
  d=1   L2773  T=0 F=6  T=0 F=352  case CURLOPT_RTSP_CLIENT_CSEQ:
  d=1   L2782  T=0 F=6  T=0 F=352  case CURLOPT_RTSP_SERVER_CSEQ:
  d=1   L2787  T=0 F=6  T=0 F=352  case CURLOPT_INTERLEAVEDATA:
  d=1   L2790  T=0 F=6  T=0 F=352  case CURLOPT_INTERLEAVEFUNCTION:
  d=1   L2796  T=0 F=6  T=0 F=352  case CURLOPT_WILDCARDMATCH:
  d=1   L2799  T=0 F=6  T=0 F=352  case CURLOPT_CHUNK_BGN_FUNCTION:
  d=1   L2802  T=0 F=6  T=0 F=352  case CURLOPT_CHUNK_END_FUNCTION:
  d=1   L2805  T=0 F=6  T=0 F=352  case CURLOPT_FNMATCH_FUNCTION:
  d=1   L2808  T=0 F=6  T=0 F=352  case CURLOPT_CHUNK_DATA:
  d=1   L2811  T=0 F=6  T=0 F=352  case CURLOPT_FNMATCH_DATA:
  d=1   L2816  T=0 F=6  T=0 F=352  case CURLOPT_TLSAUTH_USERNAME:
  d=1   L2824  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_TLSAUTH_USERNAME:
  d=1   L2833  T=0 F=6  T=0 F=352  case CURLOPT_TLSAUTH_PASSWORD:
  d=1   L2841  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_TLSAUTH_PASSWORD:
  d=1   L2849  T=0 F=6  T=0 F=352  case CURLOPT_TLSAUTH_TYPE:
  d=1   L2858  T=0 F=6  T=0 F=352  case CURLOPT_PROXY_TLSAUTH_TYPE:
  d=1   L2898  T=0 F=6  T=0 F=352  case CURLOPT_TCP_KEEPALIVE:
  d=1   L2901  T=0 F=6  T=0 F=352  case CURLOPT_TCP_KEEPIDLE:
  d=1   L2909  T=0 F=6  T=0 F=352  case CURLOPT_TCP_KEEPINTVL:
  d=1   L2917  T=0 F=6  T=0 F=352  case CURLOPT_TCP_FASTOPEN:
  d=1   L2925  T=0 F=6  T=0 F=352  case CURLOPT_SSL_ENABLE_NPN:
  d=1   L2927  T=0 F=6  T=0 F=352  case CURLOPT_SSL_ENABLE_ALPN:
  d=1   L2931  T=0 F=6  T=0 F=352  case CURLOPT_UNIX_SOCKET_PATH:
  d=1   L2936  T=0 F=6  T=0 F=352  case CURLOPT_ABSTRACT_UNIX_SOCKET:
  d=1   L2943  T=0 F=6  T=0 F=352  case CURLOPT_PATH_AS_IS:
  d=1   L2946  T=0 F=6  T=0 F=352  case CURLOPT_PIPEWAIT:
  d=1   L2949  T=0 F=6  T=0 F=352  case CURLOPT_STREAM_WEIGHT:
  d=1   L2958  T=0 F=6  T=0 F=352  case CURLOPT_STREAM_DEPENDS:
  d=1   L2959  T=0 F=6  T=0 F=352  case CURLOPT_STREAM_DEPENDS_E:
  d=1   L2974  T=0 F=6  T=19 F=333  case CURLOPT_CONNECT_TO:
  d=1   L2977  T=0 F=6  T=0 F=352  case CURLOPT_SUPPRESS_CONNECT_HEADERS:
  d=1   L2980  T=0 F=6  T=0 F=352  case CURLOPT_HAPPY_EYEBALLS_TIMEOUT_MS:
  d=1   L2987  T=0 F=6  T=0 F=352  case CURLOPT_DNS_SHUFFLE_ADDRESSES:
  d=1   L2991  T=0 F=6  T=0 F=352  case CURLOPT_DISALLOW_USERNAME_IN_URL:
  d=1   L2996  T=0 F=6  T=0 F=352  case CURLOPT_DOH_URL:
  d=1   L3002  T=0 F=6  T=0 F=352  case CURLOPT_UPKEEP_INTERVAL_MS:
  d=1   L3008  T=0 F=6  T=0 F=352  case CURLOPT_MAXAGE_CONN:
  d=1   L3014  T=0 F=6  T=0 F=352  case CURLOPT_MAXLIFETIME_CONN:
  d=1   L3020  T=0 F=6  T=0 F=352  case CURLOPT_TRAILERFUNCTION:
  d=1   L3025  T=0 F=6  T=0 F=352  case CURLOPT_TRAILERDATA:
  d=1   L3031  T=0 F=6  T=0 F=352  case CURLOPT_HSTSREADFUNCTION:
  d=1   L3034  T=0 F=6  T=0 F=352  case CURLOPT_HSTSREADDATA:
  d=1   L3037  T=0 F=6  T=0 F=352  case CURLOPT_HSTSWRITEFUNCTION:
  d=1   L3040  T=0 F=6  T=0 F=352  case CURLOPT_HSTSWRITEDATA:
  d=1   L3043  T=0 F=6  T=19 F=333  case CURLOPT_HSTS:
  d=1   L3044  T=0 F=0  T=19 F=0  if(!data->hsts) {
  d=1   L3046  T=0 F=0  T=0 F=19  if(!data->hsts)
  d=1   L3051  T=0 F=0  T=0 F=19  if(result)
  d=1   L3053  T=0 F=0  T=19 F=0  if(argptr)
  d=1   L3056  T=0 F=6  T=0 F=352  case CURLOPT_HSTS_CTRL:
  d=1   L3070  T=0 F=6  T=19 F=333  case CURLOPT_ALTSVC:
  d=1   L3071  T=0 F=0  T=19 F=0  if(!data->asi) {
  d=1   L3073  T=0 F=0  T=0 F=19  if(!data->asi)
  d=1   L3078  T=0 F=0  T=0 F=19  if(result)
  d=1   L3080  T=0 F=0  T=19 F=0  if(argptr)
  d=1   L3083  T=0 F=6  T=0 F=352  case CURLOPT_ALTSVC_CTRL:
  d=1   L3095  T=0 F=6  T=0 F=352  case CURLOPT_PREREQFUNCTION:
  d=1   L3098  T=0 F=6  T=0 F=352  case CURLOPT_PREREQDATA:
  d=1   L3102  T=0 F=6  T=0 F=352  case CURLOPT_WS_OPTIONS: {
  d=1   L3110  T=4 F=2  T=0 F=352  default:  <-- BLOCKER

[off-chain: 10 additional divergent branches across 2 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=d118b0c85c3a7f4f, size=33 bytes, fuzzer=naive, trial=1, discovered_at=1s, mutation_op=BitFlipMutator,BytesDeleteMutator,ByteAddMutator):
  0000: 00 2f 00 00 00 19 70 6f 70 33 35 c9 2f cf 32 80   ./....pop35./.2.
  0010: 3d 52 77 fe 00 19 70 6f 73 65 63 56 56 76 72 65   =Rw...posecVVvre
  0020: 8c                                                .
Seed 2 (id=0c7c09e5df793ae2, size=45 bytes, fuzzer=naive, trial=1, discovered_at=7s, mutation_op=BytesDeleteMutator,BytesDeleteMutator,CrossoverInsertMutator,BytesInsertMutator,BytesInsertMutator,BytesExpandMutator,BytesCopyMutator):
  0000: 00 01 00 00 00 19 70 73 65 65 70 70 53 70 6f 70   ......pseeppSpop
  0010: 2e 2e 2e 2d 2e 2f 00 00 00 00 00 00 2e 00 01 00   ...-./..........
  0020: 2f 00 00 00 00 00 00 2e 2e 00 01 00 27            /...........'
Seed 3 (id=a66185ae800ddc28, size=39 bytes, fuzzer=naive, trial=1, discovered_at=10554s, mutation_op=BytesExpandMutator,QwordAddMutator,WordAddMutator,BytesInsertCopyMutator,BytesDeleteMutator,ByteIncMutator,BytesSetMutator):
  0000: 00 06 00 00 00 00 00 2f 00 00 00 00 00 00 00 00   ......./........
  0010: 00 80 00 64 00 33 2d 2d 2e 3c 00 01 00 21 0f 19   ...d.3--.<...!..
  0020: 80 00 64 00 33 2d 2e                              ..d.3-.
Seed 4 (id=9137b99251b78332, size=53 bytes, fuzzer=naive, trial=1, discovered_at=12309s, mutation_op=WordAddMutator,BytesExpandMutator,BytesExpandMutator,ByteDecMutator):
  0000: 00 05 00 00 00 00 00 2f 00 00 00 00 00 00 00 00   ......./........
  0010: 2f 00 00 00 00 00 00 00 00 00 00 00 00 00 21 80   /.............!.
  0020: 00 64 00 33 2d 2d 2e 3c 00 01 00 21 0f 19 80 00   .d.3--.<...!....
  0030: 64 00 33 2d 2e                                    d.3-.

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00319f73612c7096, size=109 bytes, fuzzer=cmplog, trial=1, discovered_at=0s, mutation_op=ByteRandMutator,ByteDecMutator,BytesDeleteMutator):
  0000: 00 01 00 00 00 19 70 6f 70 33 3a 2f 2f 31 32 37   ......pop3://127
  0010: 2e 30 2e 30 2e 31 3a 39 30 30 31 2f 38 35 30 00   .0.0.1:9001/850.
  0020: 17 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 30 6f   ....GFrom: me@0o
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 13 6b   mewhere..To: f.k
Seed 2 (id=001f31cb6e5a26e0, size=130 bytes, fuzzer=cmplog, trial=1, discovered_at=32s, mutation_op=DwordInterestingMutator,ByteIncMutator,BytesInsertMutator,ByteDecMutator,ByteInterestingMutator,BytesInsertMutator):
  0000: 00 01 00 00 00 19 70 6f 00 33 3a 2f 2f 31 32 37   ......po.3://127
  0010: 2e 30 2e 30 2e 31 3a 39 31 30 31 2f 38 35 30 00   .0.0.1:9101/850.
  0020: 03 00 00 00 47 46 72 6f 6d 3a 20 6d 32 40 30 6f   ....GFrom: m2@0o
  0030: 6d 65 77 68 65 72 65 70 6e 54 6f 3a 20 66 61 6b   mewherepnTo: fak
Seed 3 (id=0021b94cb27c43fc, size=108 bytes, fuzzer=cmplog, trial=1, discovered_at=52s, mutation_op=BitFlipMutator,QwordAddMutator,BytesInsertCopyMutator,ByteDecMutator):
  0000: 00 01 00 00 00 19 31 32 37 2e 30 2e 30 2e 3a 3a   ......127.0.0.::
  0010: 39 30 30 31 2f 38 35 30 00 29 00 00 00 47 46 00   9001/850.)...GF.
  0020: 02 00 00 00 47 46 72 6f 6d 3a 20 6d 65 40 23 6f   ....GFrom: me@#o
  0030: 6d 65 77 68 65 72 65 0d 0a 54 6f 3a 20 66 61 6b   mewhere..To: fak
Seed 4 (id=0008a7f8f3585654, size=35 bytes, fuzzer=cmplog, trial=1, discovered_at=216s, mutation_op=WordInterestingMutator,WordInterestingMutator,BytesDeleteMutator,TokenReplace):
  0000: 00 01 00 00 00 19 70 25 65 25 62 32 46 74 62 46   ......p%e%b2FtbF
  0010: 75 00 65 40 47 6f 00 65 77 61 00 72 72 72 72 72   u.e@Go.ewa.rrrrr
  0020: 72 72 72                                          rrr
Seed 5 (id=000d55f9f129e0aa, size=112 bytes, fuzzer=cmplog, trial=1, discovered_at=238s, mutation_op=BytesInsertMutator,BytesInsertCopyMutator,ByteIncMutator,BytesInsertMutator,WordAddMutator,BytesCopyMutator,BytesSwapMutator):
  0000: 00 01 00 00 00 19 70 6f 70 00 3a 2f 2f 31 32 00   ......pop.://12.
  0010: 00 30 28 28 2e 31 3a 39 30 30 31 72 38 35 30 00   .0((.1:9001r850.
  0020: 02 00 00 00 47 48 54 54 50 2f 20 6d 65 61 06 24   ....GHTTP/ mea.$
  0030: 65 63 8e 65 74 72 65 0d 0a 43 6f 6e 6e 65 63 74   ec.etre..Connect


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0001  2f(/)x1 01(.)x1 06(.)x1 05(.)x1     01(.)x19                            PARTIAL
   0x0005  19(.)x2 00(.)x2                     19(.)x19                            PARTIAL
   0x0006  70(p)x2 00(.)x2                     70(p)x15 31(1)x1 45(E)x1 2b(+)x1 +1u  PARTIAL
   0x0007  2f(/)x2 6f(o)x1 73(s)x1             6f(o)x12 25(%)x2 32(2)x1 5f(_)x1 +3u  PARTIAL
   0x0008  00(.)x2 70(p)x1 65(e)x1             70(p)x11 00(.)x1 37(7)x1 65(e)x1 +5u  PARTIAL
   0x0009  00(.)x2 33(3)x1 65(e)x1             00(.)x9 33(3)x3 25(%)x3 2e(.)x1 +3u  PARTIAL
   0x000a  00(.)x2 35(5)x1 70(p)x1             3a(:)x11 30(0)x1 62(b)x1 44(D)x1 +5u  DIFFER
   0x000b  00(.)x2 c9(.)x1 70(p)x1             2f(/)x8 25(%)x2 77(w)x2 2e(.)x1 +6u  DIFFER
   0x000c  00(.)x2 2f(/)x1 53(S)x1             2f(/)x11 30(0)x1 46(F)x1 44(D)x1 +5u  PARTIAL
   0x000d  00(.)x2 cf(.)x1 70(p)x1             31(1)x9 2e(.)x2 74(t)x1 a9(.)x1 +6u  DIFFER
   0x000e  00(.)x2 32(2)x1 6f(o)x1             32(2)x10 25(%)x2 3a(:)x1 62(b)x1 +5u  PARTIAL
   0x000f  00(.)x2 80(.)x1 70(p)x1             00(.)x8 37(7)x3 3a(:)x1 46(F)x1 +6u  PARTIAL
   0x0010  3d(=)x1 2e(.)x1 00(.)x1 2f(/)x1     00(.)x8 2e(.)x3 25(%)x2 39(9)x1 +5u  PARTIAL
   0x0011  52(R)x1 2e(.)x1 80(.)x1 00(.)x1     30(0)x11 00(.)x1 51(Q)x1 25(%)x1 +5u  PARTIAL
   0x0012  00(.)x2 77(w)x1 2e(.)x1             28(()x7 2e(.)x4 30(0)x1 65(e)x1 +6u  PARTIAL
   0x0013  fe(.)x1 2d(-)x1 64(d)x1 00(.)x1     28(()x8 30(0)x3 31(1)x1 40(@)x1 +6u  DIFFER
   0x0014  00(.)x3 2e(.)x1                     2e(.)x11 2f(/)x1 47(G)x1 40(@)x1 +5u  PARTIAL
   0x0015  19(.)x1 2f(/)x1 33(3)x1 00(.)x1     31(1)x8 00(.)x4 38(8)x1 6f(o)x1 +5u  PARTIAL
   0x0016  00(.)x2 70(p)x1 2d(-)x1             3a(:)x10 00(.)x3 35(5)x2 90(.)x1 +3u  PARTIAL
   0x0017  00(.)x2 6f(o)x1 2d(-)x1             39(9)x10 30(0)x1 65(e)x1 00(.)x1 +6u  PARTIAL
   0x0018  00(.)x2 73(s)x1 2e(.)x1             30(0)x5 9c(.)x5 70(p)x2 31(1)x1 +6u  PARTIAL
   0x0019  00(.)x2 65(e)x1 3c(<)x1             30(0)x11 29())x1 61(a)x1 70(p)x1 +5u  PARTIAL
   0x001a  00(.)x3 63(c)x1                     31(1)x10 00(.)x3 2f(/)x1 43(C)x1 +4u  PARTIAL
   0x001b  00(.)x2 56(V)x1 01(.)x1             72(r)x10 00(.)x3 2f(/)x2 43(C)x1 +3u  PARTIAL
   0x001c  00(.)x2 56(V)x1 2e(.)x1             38(8)x14 72(r)x2 00(.)x1 43(C)x1 +1u  PARTIAL
   0x001d  00(.)x2 76(v)x1 21(!)x1             35(5)x13 47(G)x1 72(r)x1 38(8)x1 +3u  PARTIAL
   0x001e  72(r)x1 01(.)x1 0f(.)x1 21(!)x1     30(0)x14 46(F)x1 72(r)x1 35(5)x1 +2u  PARTIAL
   0x001f  65(e)x1 00(.)x1 19(.)x1 80(.)x1     00(.)x15 72(r)x1 a0(.)x1 13(.)x1 +1u  PARTIAL
   0x0020  8c(.)x1 2f(/)x1 80(.)x1 00(.)x1     02(.)x9 06(.)x2 17(.)x1 03(.)x1 +4u  PARTIAL
   0x0021  00(.)x2 64(d)x1                     00(.)x14 72(r)x1 2f(/)x1            PARTIAL
   0x0022  00(.)x2 64(d)x1                     00(.)x14 72(r)x1 d1(.)x1            PARTIAL
   0x0023  00(.)x2 33(3)x1                     00(.)x14                            PARTIAL
   0x0024  00(.)x1 33(3)x1 2d(-)x1             47(G)x11 48(H)x3                    DIFFER
   0x0025  2d(-)x2 00(.)x1                     48(H)x9 46(F)x3 43(C)x1 70(p)x1     DIFFER
   0x0026  2e(.)x2 00(.)x1                     54(T)x9 72(r)x4 63(c)x1             DIFFER
   0x0027  2e(.)x1 3c(<)x1                     54(T)x9 6f(o)x4 63(c)x1             DIFFER
   0x0028  2e(.)x1 00(.)x1                     50(P)x9 6d(m)x4 65(e)x1             DIFFER
   0x0029  00(.)x1 01(.)x1                     2f(/)x9 3a(:)x3 70(p)x1 00(.)x1     PARTIAL
   0x002a  01(.)x1 00(.)x1                     20( )x7 25(%)x2 23(#)x2 74(t)x1 +2u  DIFFER
   0x002b  00(.)x1 21(!)x1                     6d(m)x9 92(.)x2 69(i)x1 80(.)x1 +1u  DIFFER
   ... (9 more divergent offsets)
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
  prompts_b/curl_398.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 398,
  "target": "curl",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 398 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 398 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 398 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).