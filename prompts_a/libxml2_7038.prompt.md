==== BLOCKER ====
Target: libxml2
Branch ID: 7038
Location: /src/libxml2/uri.c:2064:32
Enclosing function: xmlBuildURI
Source line:     if ((ref->path != NULL) && (ref->path[0] == '/')) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  loser (I2S vs cmplog)
cmplog                          10        0          0  winner (I2S vs naive)
value_profile                    5        5          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        6        4          0  REFERENCE
naive_ngram4                     4        6          0  REFERENCE
mopt                             3        7          0  REFERENCE
minimizer                        7        3          0  REFERENCE
fast                             6        4          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=1.20h  loser=22.70h
  avg hitcount on branch: winner=14  loser=0
  prob_div=0.90  dur_div=21.50h  hit_div=14
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7038/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlBuildURI (/src/libxml2/uri.c:1903-2152) ---
[ ]  1901   */
[ ]  1902  xmlChar *
[B]  1903  xmlBuildURI(const xmlChar *URI, const xmlChar *base) {
[B]  1904      xmlChar *val = NULL;
[B]  1905      int ret, len, indx, cur, out;
[B]  1906      xmlURIPtr ref = NULL;
[B]  1907      xmlURIPtr bas = NULL;
[B]  1908      xmlURIPtr res = NULL;
[ ]  1909  
[ ]  1910      /*
[ ]  1911       * 1) The URI reference is parsed into the potential four components and
[ ]  1912       *    fragment identifier, as described in Section 4.3.
[ ]  1913       *
[ ]  1914       *    NOTE that a completely empty URI is treated by modern browsers
[ ]  1915       *    as a reference to "." rather than as a synonym for the current
[ ]  1916       *    URI.  Should we do that here?
[ ]  1917       */
[B]  1918      if (URI == NULL)
[ ]  1919  	ret = -1;
[B]  1920      else {
[B]  1921  	if (*URI) {
[B]  1922  	    ref = xmlCreateURI();
[B]  1923  	    if (ref == NULL)
[ ]  1924  		goto done;
[B]  1925  	    ret = xmlParseURIReference(ref, (const char *) URI);
[B]  1926  	}
[ ]  1927  	else
[ ]  1928  	    ret = 0;
[B]  1929      }
[B]  1930      if (ret != 0)
[ ]  1931  	goto done;
[B]  1932      if ((ref != NULL) && (ref->scheme != NULL)) {
[ ]  1933  	/*
[ ]  1934  	 * The URI is absolute don't modify.
[ ]  1935  	 */
[ ]  1936  	val = xmlStrdup(URI);
[ ]  1937  	goto done;
[ ]  1938      }
[B]  1939      if (base == NULL)
[B]  1940  	ret = -1;
[B]  1941      else {
[B]  1942  	bas = xmlCreateURI();
[B]  1943  	if (bas == NULL)
[ ]  1944  	    goto done;
[B]  1945  	ret = xmlParseURIReference(bas, (const char *) base);
[B]  1946      }
[B]  1947      if (ret != 0) {
[B]  1948  	if (ref)
[B]  1949  	    val = xmlSaveUri(ref);
[B]  1950  	goto done;
[B]  1951      }
[B]  1952      if (ref == NULL) {
[ ]  1953  	/*
[ ]  1954  	 * the base fragment must be ignored
[ ]  1955  	 */
[ ]  1956  	if (bas->fragment != NULL) {
[ ]  1957  	    xmlFree(bas->fragment);
[ ]  1958  	    bas->fragment = NULL;
[ ]  1959  	}
[ ]  1960  	val = xmlSaveUri(bas);
[ ]  1961  	goto done;
[ ]  1962      }
[ ]  1963  
[ ]  1964      /*
[ ]  1965       * 2) If the path component is empty and the scheme, authority, and
[ ]  1966       *    query components are undefined, then it is a reference to the
[ ]  1967       *    current document and we are done.  Otherwise, the reference URI's
[ ]  1968       *    query and fragment components are defined as found (or not found)
[ ]  1969       *    within the URI reference and not inherited from the base URI.
[ ]  1970       *
[ ]  1971       *    NOTE that in modern browsers, the parsing differs from the above
[ ]  1972       *    in the following aspect:  the query component is allowed to be
[ ]  1973       *    defined while still treating this as a reference to the current
[ ]  1974       *    document.
[ ]  1975       */
[B]  1976      res = xmlCreateURI();
[B]  1977      if (res == NULL)
[ ]  1978  	goto done;
[B]  1979      if ((ref->scheme == NULL) && (ref->path == NULL) &&
[B]  1980  	((ref->authority == NULL) && (ref->server == NULL) &&
[ ]  1981           (ref->port == PORT_EMPTY))) {
[ ]  1982  	if (bas->scheme != NULL)
[ ]  1983  	    res->scheme = xmlMemStrdup(bas->scheme);
[ ]  1984  	if (bas->authority != NULL)
[ ]  1985  	    res->authority = xmlMemStrdup(bas->authority);
[ ]  1986  	else {
[ ]  1987  	    if (bas->server != NULL)
[ ]  1988  		res->server = xmlMemStrdup(bas->server);
[ ]  1989  	    if (bas->user != NULL)
[ ]  1990  		res->user = xmlMemStrdup(bas->user);
[ ]  1991  	    res->port = bas->port;
[ ]  1992  	}
[ ]  1993  	if (bas->path != NULL)
[ ]  1994  	    res->path = xmlMemStrdup(bas->path);
[ ]  1995  	if (ref->query_raw != NULL)
[ ]  1996  	    res->query_raw = xmlMemStrdup (ref->query_raw);
[ ]  1997  	else if (ref->query != NULL)
[ ]  1998  	    res->query = xmlMemStrdup(ref->query);
[ ]  1999  	else if (bas->query_raw != NULL)
[ ]  2000  	    res->query_raw = xmlMemStrdup(bas->query_raw);
[ ]  2001  	else if (bas->query != NULL)
[ ]  2002  	    res->query = xmlMemStrdup(bas->query);
[ ]  2003  	if (ref->fragment != NULL)
[ ]  2004  	    res->fragment = xmlMemStrdup(ref->fragment);
[ ]  2005  	goto step_7;
[ ]  2006      }
[ ]  2007  
[ ]  2008      /*
[ ]  2009       * 3) If the scheme component is defined, indicating that the reference
[ ]  2010       *    starts with a scheme name, then the reference is interpreted as an
[ ]  2011       *    absolute URI and we are done.  Otherwise, the reference URI's
[ ]  2012       *    scheme is inherited from the base URI's scheme component.
[ ]  2013       */
[B]  2014      if (ref->scheme != NULL) {
[ ]  2015  	val = xmlSaveUri(ref);
[ ]  2016  	goto done;
[ ]  2017      }
[B]  2018      if (bas->scheme != NULL)
[B]  2019  	res->scheme = xmlMemStrdup(bas->scheme);
[ ]  2020  
[B]  2021      if (ref->query_raw != NULL)
[ ]  2022  	res->query_raw = xmlMemStrdup(ref->query_raw);
[B]  2023      else if (ref->query != NULL)
[ ]  2024  	res->query = xmlMemStrdup(ref->query);
[B]  2025      if (ref->fragment != NULL)
[B]  2026  	res->fragment = xmlMemStrdup(ref->fragment);
[ ]  2027  
[ ]  2028      /*
[ ]  2029       * 4) If the authority component is defined, then the reference is a
[ ]  2030       *    network-path and we skip to step 7.  Otherwise, the reference
[ ]  2031       *    URI's authority is inherited from the base URI's authority
[ ]  2032       *    component, which will also be undefined if the URI scheme does not
[ ]  2033       *    use an authority component.
[ ]  2034       */
[B]  2035      if ((ref->authority != NULL) || (ref->server != NULL) ||
[B]  2036           (ref->port != PORT_EMPTY)) {
[ ]  2037  	if (ref->authority != NULL)
[ ]  2038  	    res->authority = xmlMemStrdup(ref->authority);
[ ]  2039  	else {
[ ]  2040              if (ref->server != NULL)
[ ]  2041                  res->server = xmlMemStrdup(ref->server);
[ ]  2042  	    if (ref->user != NULL)
[ ]  2043  		res->user = xmlMemStrdup(ref->user);
[ ]  2044              res->port = ref->port;
[ ]  2045  	}
[ ]  2046  	if (ref->path != NULL)
[ ]  2047  	    res->path = xmlMemStrdup(ref->path);
[ ]  2048  	goto step_7;
[ ]  2049      }
[B]  2050      if (bas->authority != NULL)
[ ]  2051  	res->authority = xmlMemStrdup(bas->authority);
[B]  2052      else if ((bas->server != NULL) || (bas->port != PORT_EMPTY)) {
[B]  2053  	if (bas->server != NULL)
[B]  2054  	    res->server = xmlMemStrdup(bas->server);
[B]  2055  	if (bas->user != NULL)
[ ]  2056  	    res->user = xmlMemStrdup(bas->user);
[B]  2057  	res->port = bas->port;
[B]  2058      }
[ ]  2059  
[ ]  2060      /*
[ ]  2061       * 5) If the path component begins with a slash character ("/"), then
[ ]  2062       *    the reference is an absolute-path and we skip to step 7.
[ ]  2063       */
[B]  2064      if ((ref->path != NULL) && (ref->path[0] == '/')) { <-- BLOCKER
[W]  2065  	res->path = xmlMemStrdup(ref->path);
[W]  2066  	goto step_7;
[W]  2067      }
[ ]  2068  
[ ]  2069  
[ ]  2070      /*
[ ]  2071       * 6) If this step is reached, then we are resolving a relative-path
[ ]  2072       *    reference.  The relative path needs to be merged with the base
[ ]  2073       *    URI's path.  Although there are many ways to do this, we will
[ ]  2074       *    describe a simple method using a separate string buffer.
[ ]  2075       *
[ ]  2076       * Allocate a buffer large enough for the result string.
[ ]  2077       */
[L]  2078      len = 2; /* extra / and 0 */
[L]  2079      if (ref->path != NULL)
[L]  2080  	len += strlen(ref->path);
[L]  2081      if (bas->path != NULL)
[L]  2082  	len += strlen(bas->path);
[L]  2083      res->path = (char *) xmlMallocAtomic(len);
[L]  2084      if (res->path == NULL) {
[ ]  2085          xmlURIErrMemory("resolving URI against base\n");
[ ]  2086  	goto done;
[ ]  2087      }
[L]  2088      res->path[0] = 0;
[ ]  2089  
[ ]  2090      /*
[ ]  2091       * a) All but the last segment of the base URI's path component is
[ ]  2092       *    copied to the buffer.  In other words, any characters after the
[ ]  2093       *    last (right-most) slash character, if any, are excluded.
[ ]  2094       */
[L]  2095      cur = 0;
[L]  2096      out = 0;
[L]  2097      if (bas->path != NULL) {
[L]  2098  	while (bas->path[cur] != 0) {
[L]  2099  	    while ((bas->path[cur] != 0) && (bas->path[cur] != '/'))
[L]  2100  		cur++;
[L]  2101  	    if (bas->path[cur] == 0)
[L]  2102  		break;
[ ]  2103  
[L]  2104  	    cur++;
[L]  2105  	    while (out < cur) {
[L]  2106  		res->path[out] = bas->path[out];
[L]  2107  		out++;
[L]  2108  	    }
[L]  2109  	}
[L]  2110      }
[L]  2111      res->path[out] = 0;
[ ]  2112  
[ ]  2113      /*
[ ]  2114       * b) The reference's path component is appended to the buffer
[ ]  2115       *    string.
[ ]  2116       */
[L]  2117      if (ref->path != NULL && ref->path[0] != 0) {
[L]  2118  	indx = 0;
[ ]  2119  	/*
[ ]  2120  	 * Ensure the path includes a '/'
[ ]  2121  	 */
[L]  2122  	if ((out == 0) && ((bas->server != NULL) || bas->port != PORT_EMPTY))
[L]  2123  	    res->path[out++] = '/';
[L]  2124  	while (ref->path[indx] != 0) {
[L]  2125  	    res->path[out++] = ref->path[indx++];
[L]  2126  	}
[L]  2127      }
[L]  2128      res->path[out] = 0;
[ ]  2129  
[ ]  2130      /*
[ ]  2131       * Steps c) to h) are really path normalization steps
[ ]  2132       */
[L]  2133      xmlNormalizeURIPath(res->path);
[ ]  2134  
[B]  2135  step_7:
[ ]  2136  
[ ]  2137      /*
[ ]  2138       * 7) The resulting URI components, including any inherited from the
[ ]  2139       *    base URI, are recombined to give the absolute form of the URI
[ ]  2140       *    reference.
[ ]  2141       */
[B]  2142      val = xmlSaveUri(res);
[ ]  2143  
[B]  2144  done:
[B]  2145      if (ref != NULL)
[B]  2146  	xmlFreeURI(ref);
[B]  2147      if (bas != NULL)
[B]  2148  	xmlFreeURI(bas);
[B]  2149      if (res != NULL)
[B]  2150  	xmlFreeURI(res);
[B]  2151      return(val);
[B]  2152  }

--- Caller (1 hop): xmlSAX2ResolveEntity (/src/libxml2/SAX2.c:514-538, calls xmlBuildURI at line 526) (full body — short) ---
[B]   514  {
[B]   515      xmlParserCtxtPtr ctxt = (xmlParserCtxtPtr) ctx;
[B]   516      xmlParserInputPtr ret;
[B]   517      xmlChar *URI;
[B]   518      const char *base = NULL;
[ ]   519  
[B]   520      if (ctx == NULL) return(NULL);
[B]   521      if (ctxt->input != NULL)
[B]   522  	base = ctxt->input->filename;
[B]   523      if (base == NULL)
[B]   524  	base = ctxt->directory;
[ ]   525  
[B]   526      URI = xmlBuildURI(systemId, (const xmlChar *) base); <-- CALL
[ ]   527  
[ ]   528  #ifdef DEBUG_SAX
[ ]   529      xmlGenericError(xmlGenericErrorContext,
[ ]   530  	    "SAX.xmlSAX2ResolveEntity(%s, %s)\n", publicId, systemId);
[ ]   531  #endif
[ ]   532  
[B]   533      ret = xmlLoadExternalEntity((const char *) URI,
[B]   534  				(const char *) publicId, ctxt);
[B]   535      if (URI != NULL)
[B]   536  	xmlFree(URI);
[B]   537      return(ret);
[B]   538  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  parser.c:xmlCreateEntityParserCtxtInternal  (/src/libxml2/parser.c:13782-13835, calls xmlBuildURI at line 13803)
hop 2  relaxng.c:xmlRelaxNGCleanupTree  (/src/libxml2/relaxng.c:7043-7472, calls xmlBuildURI at line 7126)
hop 3  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls parser.c:xmlCreateEntityParserCtxtInternal at line 12854)
hop 3  xmlCreateEntityParserCtxt  (/src/libxml2/parser.c:13851-13854, calls parser.c:xmlCreateEntityParserCtxtInternal at line 13852)
hop 3  relaxng.c:xmlRelaxNGCleanupDoc  (/src/libxml2/relaxng.c:7486-7500, calls relaxng.c:xmlRelaxNGCleanupTree at line 7498)
hop 4  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 4  relaxng.c:xmlRelaxNGLoadExternalRef  (/src/libxml2/relaxng.c:1953-2027, calls relaxng.c:xmlRelaxNGCleanupDoc at line 2018)
hop 4  relaxng.c:xmlRelaxNGLoadInclude  (/src/libxml2/relaxng.c:1605-1765, calls relaxng.c:xmlRelaxNGCleanupDoc at line 1681)
hop 5  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseReference at line 10020)
hop 5  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseReference at line 11768)
hop 6  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 6  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 6  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 7  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 7  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)
hop 8  xmlSAXParseEntity  (/src/libxml2/parser.c:13716-13745, calls xmlParseExtParsedEnt at line 13731)
hop 8  xmlSAXParseFileWithData  (/src/libxml2/parser.c:13945-13991, calls xmlParseDocument at line 13970)
hop 8  xmlSAXUserParseFile  (/src/libxml2/parser.c:14124-14157, calls xmlParseDocument at line 14138)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
     772      2840  uri.c:is_hex  (/src/libxml2/uri.c:1607-1613)
     163       629  uri.c:xmlParse3986Segment  (/src/libxml2/uri.c:564-577)
      29       106  uri.c:xmlParse3986PathNoScheme  (/src/libxml2/uri.c:721-747)
      20        87  xmlParseName  (/src/libxml2/parser.c:3368-3412)
      19        77  uri.c:xmlParse3986HierPart  (/src/libxml2/uri.c:766-800)
      25        77  uri.c:xmlParse3986Userinfo  (/src/libxml2/uri.c:371-390)
      25        77  uri.c:xmlParse3986Host  (/src/libxml2/uri.c:446-506)
      25        77  uri.c:xmlParse3986Authority  (/src/libxml2/uri.c:522-544)
      25        77  uri.c:xmlParse3986PathAbEmpty  (/src/libxml2/uri.c:593-617)
      18        63  xmlUnlinkNode  (/src/libxml2/tree.c:3910-3971)
      53        16  parser.c:xmlParseNCName  (/src/libxml2/parser.c:3489-3535)
       0        33  xmlSearchNs  (/src/libxml2/tree.c:6134-6207)
      44        12  parser.c:xmlParseQName  (/src/libxml2/parser.c:8884-8953)
       9        41  uri.c:xmlSaveUriRealloc  (/src/libxml2/uri.c:1048-1064)
       0        30  xmlGetDtdQElementDesc  (/src/libxml2/valid.c:3349-3357)
... (59 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=7   L10922  T=0 F=6  T=4 F=6  if (ctxt->instate == XML_PARSER_EOF)
  d=7   L10936  T=0 F=6  T=1 F=5  if (RAW != '<') {
  d=7   L10950  T=3 F=3  T=0 F=5  if (RAW != 0) {
--- d=6  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=6   L10084  T=3 F=3  T=5 F=0  if (CUR == 0) {
--- d=6  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=6   L12139  T=0 F=22  T=0 F=44  if (ctxt == NULL)
  d=6   L12141  T=6 F=0  T=5 F=14  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12141  T=6 F=16  T=19 F=25  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12143  T=0 F=16  T=0 F=39  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L12145  T=0 F=16  T=0 F=39  if (ctxt->input == NULL)
  d=6   L12149  T=12 F=4  T=20 F=19  if (ctxt->instate == XML_PARSER_START)
  d=6   L12151  T=13 F=3  T=23 F=16  if ((size > 0) && (chunk != NULL) && (!terminate) &&
  d=6   L12159  T=13 F=3  T=23 F=16  if ((size > 0) && (chunk != NULL) && (ctxt->input != NULL...
  d=6   L12211  T=3 F=0  T=16 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=6   L12212  T=3 F=0  T=16 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=6   L12212  T=3 F=0  T=16 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=6   L12214  T=0 F=3  T=0 F=16  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=6   L12233  T=0 F=16  T=0 F=39  if (remain != 0) {
  d=6   L12238  T=6 F=10  T=3 F=36  if (ctxt->instate == XML_PARSER_EOF)
  d=6   L12241  T=10 F=0  T=36 F=0  if ((ctxt->input != NULL) &&
  d=6   L12242  T=0 F=10  T=0 F=36  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=6   L12243  T=0 F=10  T=0 F=36  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=6   L12248  T=4 F=2  T=10 F=19  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12248  T=6 F=4  T=29 F=7  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12251  T=0 F=6  T=0 F=26  if (remain != 0) {
  d=6   L12257  T=0 F=6  T=0 F=26  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=6   L12268  T=2 F=4  T=7 F=19  if (terminate) {
  d=6   L12274  T=2 F=0  T=7 F=0  if (ctxt->input != NULL) {
  d=6   L12275  T=0 F=2  T=0 F=7  if (ctxt->input->buf == NULL)
  d=6   L12283  T=2 F=0  T=7 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=6   L12284  T=2 F=0  T=6 F=1  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=6   L12287  T=0 F=0  T=0 F=1  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=6   L12287  T=0 F=2  T=1 F=6  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=6   L12290  T=2 F=0  T=7 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=6   L12291  T=2 F=0  T=7 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12291  T=2 F=0  T=7 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12296  T=2 F=4  T=8 F=18  if (ctxt->wellFormed == 0)
--- d=5  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=5   L9980  T=0 F=10  T=0 F=4  if ((*cur == '<') && (cur[1] == '?')) {
  d=5   L9995  T=0 F=10  T=0 F=4  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=5   L10005  T=4 F=6  T=1 F=3  if (NXT(1) == '/') {
  d=5   L10006  T=3 F=1  T=0 F=1  if (ctxt->nameNr <= nameNr)
--- d=5  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=5   L11409  T=0 F=16  T=0 F=39  if (ctxt->input == NULL)
  d=5   L11465  T=16 F=0  T=39 F=0  if ((ctxt->input != NULL) &&
  d=5   L11466  T=0 F=16  T=0 F=39  (ctxt->input->cur - ctxt->input->base > 4096)) {
  d=5   L11471  T=4 F=16  T=10 F=46  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=5   L11500  T=0 F=106  T=5 F=128  if (avail < 1)
  d=5   L11632  T=0 F=25  T=1 F=24  if (cur != '<') {
  d=5   L11635  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11635  T=0 F=0  T=1 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11648  T=22 F=0  T=6 F=12  if (ctxt->sax2)
  d=5   L11660  T=4 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11660  T=4 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11722  T=2 F=31  T=0 F=31  if ((avail < 2) && (ctxt->inputNr == 1))
  d=5   L11722  T=2 F=0  T=0 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=5   L11784  T=17 F=0  T=18 F=4  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=5   L11793  T=0 F=4  T=0 F=2  if (avail < 2)
  d=5   L11795  T=0 F=4  T=0 F=2  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=5   L11795  T=4 F=0  T=2 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=5   L11797  T=4 F=0  T=2 F=0  if (ctxt->sax2) {
  d=5   L11805  T=0 F=4  T=0 F=2  if (ctxt->instate == XML_PARSER_EOF) {
  d=5   L11807  T=2 F=2  T=1 F=1  } else if (ctxt->nameNr == 0) {
  d=5   L11914  T=0 F=26  T=6 F=34  if (avail < 2)
  d=5   L11951  T=0 F=12  T=2 F=20  if ((!terminate) && (!xmlParseLookupGt(ctxt)))
  d=5   L11989  T=2 F=12  T=0 F=12  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=5   L11996  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11996  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
--- d=1  xmlBuildURI  (/src/libxml2/uri.c:1903-2152) ---
  d=1   L1948  T=8 F=0  T=17 F=0  if (ref)
  d=1   L2052  T=0 F=8  T=2 F=4  else if ((bas->server != NULL) || (bas->port != PORT_EMPT...
  d=1   L2053  T=2 F=0  T=7 F=2  if (bas->server != NULL)
  d=1   L2055  T=0 F=2  T=0 F=9  if (bas->user != NULL)
  d=1   L2064  T=10 F=0  T=0 F=13  if ((ref->path != NULL) && (ref->path[0] == '/')) {  <-- BLOCKER
  d=1   L2079  T=0 F=0  T=13 F=0  if (ref->path != NULL)
  d=1   L2081  T=0 F=0  T=7 F=6  if (bas->path != NULL)
  d=1   L2084  T=0 F=0  T=0 F=13  if (res->path == NULL) {
  d=1   L2097  T=0 F=0  T=7 F=6  if (bas->path != NULL) {
  d=1   L2098  T=0 F=0  T=156 F=0  while (bas->path[cur] != 0) {
  d=1   L2099  T=0 F=0  T=137 F=149  while ((bas->path[cur] != 0) && (bas->path[cur] != '/'))
  d=1   L2099  T=0 F=0  T=286 F=7  while ((bas->path[cur] != 0) && (bas->path[cur] != '/'))
  d=1   L2101  T=0 F=0  T=7 F=149  if (bas->path[cur] == 0)
  d=1   L2105  T=0 F=0  T=237 F=149  while (out < cur) {
  d=1   L2117  T=0 F=0  T=13 F=0  if (ref->path != NULL && ref->path[0] != 0) {
  d=1   L2117  T=0 F=0  T=13 F=0  if (ref->path != NULL && ref->path[0] != 0) {
  d=1   L2122  T=0 F=0  T=0 F=4  if ((out == 0) && ((bas->server != NULL) || bas->port != ...
  d=1   L2122  T=0 F=0  T=6 F=4  if ((out == 0) && ((bas->server != NULL) || bas->port != ...
  d=1   L2122  T=0 F=0  T=10 F=3  if ((out == 0) && ((bas->server != NULL) || bas->port != ...
  d=1   L2124  T=0 F=0  T=201 F=13  while (ref->path[indx] != 0) {

[off-chain: 1142 additional divergent branches across 126 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=6c78d3f922fb9894, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=2s, mutation_op=WordAddMutator,BytesDeleteMutator,BytesDeleteMutator,DwordAddMutator,BytesDeleteMutator):
  0000: 06 00 00 00 31 32 00 37 37 32 2e 78 6d 6c 5c 0a   ....12.772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 2f 74 64 73 2f 31   a SYSTEM "/tds/1
Seed 2 (id=0a8ffe5adb5dead8, size=378 bytes, fuzzer=cmplog, trial=1, discovered_at=1957s, mutation_op=DwordInterestingMutator,WordAddMutator,WordAddMutator,BytesExpandMutator,DwordInterestingMutator,ByteFlipMutator,BytesInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 2f 2f 2f 2f 2f 3d   a SYSTEM "/////=
Seed 3 (id=8769fc77915bb09c, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3765s, mutation_op=ByteIncMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 2f 74 40 2e 27 27   a SYSTEM "/t@.''
Seed 4 (id=d94a42320100522b, size=236 bytes, fuzzer=cmplog, trial=1, discovered_at=8808s, mutation_op=BytesDeleteMutator,BytesRandInsertMutator):
  0000: 45 44 20 27 68 74 74 70 3a 2f 2f 77 77 77 26 77   ED 'http://www&w
  0010: 02 2e 6f 72 67 2f 45 44 20 27 68 74 74 70 3a 2f   ..org/ED 'http:/
  0020: 2f 77 77 77 26 77 02 2e 6f 72 67 2f 31 39 39 39   /www&w..org/1999
  0030: 2f 78 6c 69 6e 6b 27 0a 20 20 20 20 20 20 20 20   /xlink'.        
Seed 5 (id=db79f1d810d3fa26, size=238 bytes, fuzzer=cmplog, trial=1, discovered_at=33298s, mutation_op=ByteRandMutator,BytesInsertMutator,BytesRandInsertMutator,ByteIncMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 46 6d 6c 5c 0a   ....127772.Fml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 2f 74 64 73 2f 2f   a SYSTEM "/tds//

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=022872fb8319f510, size=611 bytes, fuzzer=naive, trial=1, discovered_at=11s, mutation_op=CrossoverInsertMutator,WordAddMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=013a786979d45920, size=375 bytes, fuzzer=naive, trial=1, discovered_at=59s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=00c0385729a5223c, size=537 bytes, fuzzer=naive, trial=1, discovered_at=5238s, mutation_op=BytesInsertCopyMutator,BytesInsertCopyMutator,BytesInsertMutator,BytesInsertCopyMutator,BytesRandInsertMutator,ByteFlipMutator):
  0000: 45 44 20 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77   ED 'http://www.w
  0010: c4 2e 6f 72 88 2f 31 39 39 39 2f 78 6c 69 6e 6b   ..or./1999/xlink
  0020: 6e 65 8b 22 3e 2f 2f 2f 62 20 74 65 78 6d 6c 5c   ne.">///b texml\
  0030: 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22   .<?xml version="
Seed 4 (id=01693899945ec61c, size=165 bytes, fuzzer=naive, trial=1, discovered_at=7599s, mutation_op=BitFlipMutator,ByteAddMutator,BytesDeleteMutator):
  0000: 39 2f 20 74 74 70 3a 2f 2f 77 77 77 2e 77 33 2e   9/ ttp://www.w3.
  0010: 6f 72 28 62 2a 29 3e 0a 0a 4c 45 4d 45 4e 54 20   or(b*)>..LEMENT 
  0020: 61 20 28 62 2a 2c 2c 2c 20 20 20 20 20 20 20 20   a (b*,,,        
  0030: 20 20 20 62 20 28 23 af 43 39 2f 2c 74 27 0a 20      b (#.C9/,t'. 
Seed 5 (id=017f68cf7a6263c8, size=280 bytes, fuzzer=naive, trial=1, discovered_at=15136s, mutation_op=WordAddMutator,BytesExpandMutator,BytesInsertMutator,QwordAddMutator):
  0000: 3d 22 3d 22 68 74 74 70 3a 2f 2f 75 c2 6b 65 75   ="="http://u.keu
  0010: a2 a2 6c 6c 6c 6c 6c a2 a2 68 68 68 a2 a2 a2 a2   ..lllll..hhh....
  0020: a2 a2 a3 a2 a2 a2 68 68 68 68 37 e8 76 ad 9c f0   ......hhhh7.v...
  0030: 4c ff 68 68 68 68 68 a2 a2 a2 9c f0 4c ff 68 68   L.hhhhh.....L.hh


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  06(.)x4 45(E)x2                     3d(=)x3 06(.)x2 45(E)x1 39(9)x1 +3u  PARTIAL
   0x0001  00(.)x4 44(D)x2                     00(.)x2 2f(/)x2 22(")x2 44(D)x1 +3u  PARTIAL
   0x0002  00(.)x4 20( )x1 7e(~)x1             00(.)x2 20( )x2 68(h)x2 3d(=)x1 +3u  PARTIAL
   0x0003  00(.)x4 27(')x2                     74(t)x3 00(.)x2 27(')x1 22(")x1 +3u  PARTIAL
   0x0004  31(1)x4 68(h)x2                     74(t)x5 31(1)x2 68(h)x2 70(p)x1     PARTIAL
   0x0005  32(2)x4 74(t)x2                     70(p)x4 74(t)x3 32(2)x2 3a(:)x1     PARTIAL
   0x0006  37(7)x3 74(t)x2 00(.)x1             3a(:)x4 37(7)x2 74(t)x2 2f(/)x1 +1u  PARTIAL
   0x0007  37(7)x4 70(p)x2                     2f(/)x5 37(7)x2 70(p)x2 3a(:)x1     PARTIAL
   0x0008  37(7)x4 3a(:)x2                     2f(/)x6 37(7)x2 3a(:)x2             PARTIAL
   0x0009  32(2)x4 2f(/)x2                     2f(/)x4 32(2)x2 66(f)x2 77(w)x1 +1u  PARTIAL
   0x000a  2e(.)x4 2f(/)x2                     2f(/)x3 2e(.)x2 77(w)x2 9f(.)x2 +1u  PARTIAL
   0x000b  78(x)x3 77(w)x2 46(F)x1             77(w)x3 78(x)x2 6b(k)x2 75(u)x1 +2u  PARTIAL
   0x000c  6d(m)x4 77(w)x2                     6d(m)x2 77(w)x2 2e(.)x1 c2(.)x1 +4u  PARTIAL
   0x000d  6c(l)x4 77(w)x2                     6c(l)x2 77(w)x2 6b(k)x1 21(!)x1 +4u  PARTIAL
   0x000e  5c(\)x4 26(&)x1 2c(,)x1             5c(\)x2 2e(.)x1 33(3)x1 65(e)x1 +5u  PARTIAL
   0x000f  0a(.)x4 77(w)x2                     0a(.)x2 77(w)x1 2e(.)x1 75(u)x1 +5u  PARTIAL
   0x0010  3c(<)x4 02(.)x1 33(3)x1             3c(<)x2 c4(.)x1 6f(o)x1 a2(.)x1 +5u  PARTIAL
   0x0011  3f(?)x4 2e(.)x1 23(#)x1             3f(?)x2 2e(.)x1 72(r)x1 a2(.)x1 +5u  PARTIAL
   0x0012  78(x)x4 6f(o)x2                     78(x)x2 6f(o)x1 28(()x1 6c(l)x1 +5u  PARTIAL
   0x0013  6d(m)x4 72(r)x2                     6d(m)x2 72(r)x1 62(b)x1 6c(l)x1 +5u  PARTIAL
   0x0014  6c(l)x4 67(g)x1 2f(/)x1             6c(l)x3 88(.)x1 2a(*)x1 2f(/)x1 +4u  PARTIAL
   0x0015  20( )x4 2f(/)x2                     20( )x3 2f(/)x2 ff(.)x2 29())x1 +2u  PARTIAL
   0x0016  76(v)x4 45(E)x1 2f(/)x1             76(v)x2 31(1)x1 3e(>)x1 6c(l)x1 +5u  PARTIAL
   0x0017  65(e)x4 44(D)x1 2f(/)x1             65(e)x2 39(9)x1 0a(.)x1 a2(.)x1 +5u  PARTIAL
   0x0018  72(r)x4 20( )x1 3a(:)x1             72(r)x2 39(9)x1 0a(.)x1 a2(.)x1 +5u  PARTIAL
   0x0019  73(s)x4 27(')x1 7e(~)x1             73(s)x2 39(9)x1 4c(L)x1 68(h)x1 +5u  PARTIAL
   0x001a  69(i)x4 68(h)x1 2f(/)x1             69(i)x2 2f(/)x2 45(E)x1 68(h)x1 +4u  PARTIAL
   0x001b  6f(o)x4 74(t)x1 7e(~)x1             6f(o)x2 78(x)x1 4d(M)x1 68(h)x1 +5u  PARTIAL
   0x001c  6e(n)x4 74(t)x1 2f(/)x1             6e(n)x3 6c(l)x1 45(E)x1 a2(.)x1 +4u  PARTIAL
   0x001d  3d(=)x4 70(p)x1 7e(~)x1             3d(=)x2 69(i)x1 4e(N)x1 a2(.)x1 +5u  PARTIAL
   0x001e  22(")x4 3a(:)x1 2f(/)x1             22(")x2 6e(n)x1 54(T)x1 a2(.)x1 +5u  PARTIAL
   0x001f  31(1)x4 2f(/)x2                     31(1)x2 6b(k)x1 20( )x1 a2(.)x1 +5u  PARTIAL
   0x0020  2e(.)x4 2f(/)x2                     2e(.)x2 6e(n)x1 61(a)x1 a2(.)x1 +5u  PARTIAL
   0x0021  30(0)x4 77(w)x1 3a(:)x1             30(0)x2 65(e)x1 20( )x1 a2(.)x1 +5u  PARTIAL
   0x0022  22(")x4 77(w)x1 7e(~)x1             22(")x2 8b(.)x1 28(()x1 a3(.)x1 +5u  PARTIAL
   0x0023  3f(?)x4 77(w)x1 2f(/)x1             3f(?)x2 22(")x1 62(b)x1 a2(.)x1 +5u  PARTIAL
   0x0024  3e(>)x4 26(&)x1 7f(.)x1             3e(>)x3 2f(/)x2 2a(*)x1 a2(.)x1 +3u  PARTIAL
   0x0025  0a(.)x4 77(w)x1 2f(/)x1             2f(/)x3 0a(.)x2 ff(.)x2 2c(,)x1 +2u  PARTIAL
   0x0026  3c(<)x4 02(.)x1 7e(~)x1             3c(<)x3 2f(/)x2 2c(,)x1 68(h)x1 +3u  PARTIAL
   0x0027  21(!)x5 2e(.)x1                     21(!)x2 2f(/)x2 2c(,)x1 68(h)x1 +4u  PARTIAL
   ... (21 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7038.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7038,
  "target": "libxml2",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7038 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7038 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7038 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).