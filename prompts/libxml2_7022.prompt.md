==== BLOCKER ====
Target: libxml2
Branch ID: 7022
Location: /src/libxml2/uri.c:1952:9
Enclosing function: xmlBuildURI
Source line:     if (ref == NULL) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            5        5          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                        6        4          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             0       10          0  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=0.00h  loser=20.80h
  avg hitcount on branch: winner=251  loser=0
  prob_div=0.80  dur_div=20.80h  hit_div=251
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7022/{W,L}/branch_coverage_show.txt

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
[L]  1922  	    ref = xmlCreateURI();
[L]  1923  	    if (ref == NULL)
[ ]  1924  		goto done;
[L]  1925  	    ret = xmlParseURIReference(ref, (const char *) URI);
[L]  1926  	}
[W]  1927  	else
[W]  1928  	    ret = 0;
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
[L]  1949  	    val = xmlSaveUri(ref);
[B]  1950  	goto done;
[B]  1951      }
[B]  1952      if (ref == NULL) { <-- BLOCKER
[ ]  1953  	/*
[ ]  1954  	 * the base fragment must be ignored
[ ]  1955  	 */
[W]  1956  	if (bas->fragment != NULL) {
[W]  1957  	    xmlFree(bas->fragment);
[W]  1958  	    bas->fragment = NULL;
[W]  1959  	}
[W]  1960  	val = xmlSaveUri(bas);
[W]  1961  	goto done;
[W]  1962      }
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
[L]  1976      res = xmlCreateURI();
[L]  1977      if (res == NULL)
[ ]  1978  	goto done;
[L]  1979      if ((ref->scheme == NULL) && (ref->path == NULL) &&
[L]  1980  	((ref->authority == NULL) && (ref->server == NULL) &&
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
[L]  2014      if (ref->scheme != NULL) {
[ ]  2015  	val = xmlSaveUri(ref);
[ ]  2016  	goto done;
[ ]  2017      }
[L]  2018      if (bas->scheme != NULL)
[ ]  2019  	res->scheme = xmlMemStrdup(bas->scheme);
[ ]  2020  
[L]  2021      if (ref->query_raw != NULL)
[ ]  2022  	res->query_raw = xmlMemStrdup(ref->query_raw);
[L]  2023      else if (ref->query != NULL)
[ ]  2024  	res->query = xmlMemStrdup(ref->query);
[L]  2025      if (ref->fragment != NULL)
[ ]  2026  	res->fragment = xmlMemStrdup(ref->fragment);
[ ]  2027  
[ ]  2028      /*
[ ]  2029       * 4) If the authority component is defined, then the reference is a
[ ]  2030       *    network-path and we skip to step 7.  Otherwise, the reference
[ ]  2031       *    URI's authority is inherited from the base URI's authority
[ ]  2032       *    component, which will also be undefined if the URI scheme does not
[ ]  2033       *    use an authority component.
[ ]  2034       */
[L]  2035      if ((ref->authority != NULL) || (ref->server != NULL) ||
[L]  2036           (ref->port != PORT_EMPTY)) {
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
[L]  2050      if (bas->authority != NULL)
[ ]  2051  	res->authority = xmlMemStrdup(bas->authority);
[L]  2052      else if ((bas->server != NULL) || (bas->port != PORT_EMPTY)) {
[ ]  2053  	if (bas->server != NULL)
[ ]  2054  	    res->server = xmlMemStrdup(bas->server);
[ ]  2055  	if (bas->user != NULL)
[ ]  2056  	    res->user = xmlMemStrdup(bas->user);
[ ]  2057  	res->port = bas->port;
[ ]  2058      }
[ ]  2059  
[ ]  2060      /*
[ ]  2061       * 5) If the path component begins with a slash character ("/"), then
[ ]  2062       *    the reference is an absolute-path and we skip to step 7.
[ ]  2063       */
[L]  2064      if ((ref->path != NULL) && (ref->path[0] == '/')) {
[ ]  2065  	res->path = xmlMemStrdup(ref->path);
[ ]  2066  	goto step_7;
[ ]  2067      }
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
[ ]  2104  	    cur++;
[ ]  2105  	    while (out < cur) {
[ ]  2106  		res->path[out] = bas->path[out];
[ ]  2107  		out++;
[ ]  2108  	    }
[ ]  2109  	}
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
[ ]  2123  	    res->path[out++] = '/';
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
[L]  2135  step_7:
[ ]  2136  
[ ]  2137      /*
[ ]  2138       * 7) The resulting URI components, including any inherited from the
[ ]  2139       *    base URI, are recombined to give the absolute form of the URI
[ ]  2140       *    reference.
[ ]  2141       */
[L]  2142      val = xmlSaveUri(res);
[ ]  2143  
[B]  2144  done:
[B]  2145      if (ref != NULL)
[L]  2146  	xmlFreeURI(ref);
[B]  2147      if (bas != NULL)
[B]  2148  	xmlFreeURI(bas);
[B]  2149      if (res != NULL)
[L]  2150  	xmlFreeURI(res);
[B]  2151      return(val);
[L]  2152  }

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
    2860        12  uri.c:is_hex  (/src/libxml2/uri.c:1607-1613)
     203       803  parser.c:xmlGROW  (/src/libxml2/parser.c:2072-2094)
      85         0  uri.c:xmlParse3986Userinfo  (/src/libxml2/uri.c:371-390)
      85         0  uri.c:xmlParse3986Host  (/src/libxml2/uri.c:446-506)
      85         0  uri.c:xmlParse3986Authority  (/src/libxml2/uri.c:522-544)
      85         0  uri.c:xmlParse3986PathAbEmpty  (/src/libxml2/uri.c:593-617)
      85         0  uri.c:xmlParse3986HierPart  (/src/libxml2/uri.c:766-800)
       0        63  xmlSplitQName2  (/src/libxml2/tree.c:267-312)
      10        68  parser.c:xmlFatalErrMsg  (/src/libxml2/parser.c:466-479)
       0        57  parser.c:xmlIsNameChar  (/src/libxml2/parser.c:3183-3219)
       0        51  xmlSplitQName3  (/src/libxml2/tree.c:327-350)
       0        48  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
       4        48  xmlParseMarkupDecl  (/src/libxml2/parser.c:6950-6990)
       6        48  parser.c:xmlParseNameComplex  (/src/libxml2/parser.c:3225-3347)
       4        45  xmlSplitQName  (/src/libxml2/parser.c:2970-3118)
... (84 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=7  xmlParseDocument  (/src/libxml2/parser.c:10810-10985) ---
  d=7   L10846  T=0 F=10  T=10 F=0  if (enc != XML_CHAR_ENCODING_NONE) {
  d=7   L10863  T=3 F=7  T=0 F=10  if ((ctxt->input->end - ctxt->input->cur) < 35) {
  d=7   L10872  T=0 F=0  T=0 F=10  if ((ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) ||
  d=7   L10873  T=0 F=0  T=0 F=10  (ctxt->instate == XML_PARSER_EOF)) {
  d=7   L10936  T=0 F=9  T=1 F=7  if (RAW != '<') {
--- d=6  xmlParseElement  (/src/libxml2/parser.c:10076-10094) ---
  d=6   L10077  T=1 F=8  T=0 F=7  if (xmlParseElementStart(ctxt) != 0)
--- d=6  xmlParseChunk  (/src/libxml2/parser.c:12135-12300) ---
  d=6   L12141  T=2 F=2  T=8 F=3  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12170  T=20 F=0  T=20 F=1  if ((ctxt->instate == XML_PARSER_START) && (ctxt->input !...
  d=6   L12211  T=20 F=0  T=5 F=0  } else if (ctxt->instate != XML_PARSER_EOF) {
  d=6   L12212  T=20 F=0  T=5 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=6   L12212  T=20 F=0  T=5 F=0  if ((ctxt->input != NULL) && ctxt->input->buf != NULL) {
  d=6   L12214  T=0 F=20  T=0 F=5  if ((in->encoder != NULL) && (in->buffer != NULL) &&
  d=6   L12241  T=38 F=0  T=18 F=0  if ((ctxt->input != NULL) &&
  d=6   L12242  T=0 F=38  T=0 F=18  (((ctxt->input->end - ctxt->input->cur) > XML_MAX_LOOKUP_...
  d=6   L12243  T=0 F=38  T=0 F=18  ((ctxt->input->cur - ctxt->input->base) > XML_MAX_LOOKUP_...
  d=6   L12248  T=16 F=22  T=15 F=3  if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
  d=6   L12251  T=0 F=37  T=0 F=10  if (remain != 0) {
  d=6   L12257  T=0 F=37  T=0 F=10  if ((end_in_lf == 1) && (ctxt->input != NULL) &&
  d=6   L12268  T=14 F=23  T=2 F=8  if (terminate) {
  d=6   L12274  T=14 F=0  T=2 F=0  if (ctxt->input != NULL) {
  d=6   L12275  T=0 F=14  T=0 F=2  if (ctxt->input->buf == NULL)
  d=6   L12283  T=14 F=0  T=2 F=0  if ((ctxt->instate != XML_PARSER_EOF) &&
  d=6   L12284  T=12 F=2  T=0 F=2  (ctxt->instate != XML_PARSER_EPILOG)) {
  d=6   L12287  T=2 F=12  T=2 F=0  if ((ctxt->instate == XML_PARSER_EPILOG) && (cur_avail > ...
  d=6   L12290  T=14 F=0  T=2 F=0  if (ctxt->instate != XML_PARSER_EOF) {
  d=6   L12291  T=14 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12291  T=14 F=0  T=2 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=6   L12296  T=19 F=18  T=7 F=3  if (ctxt->wellFormed == 0)
--- d=5  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033) ---
  d=5   L9973  T=16 F=6  T=60 F=1  while ((RAW != 0) &&
  d=5   L9974  T=16 F=0  T=60 F=0  (ctxt->instate != XML_PARSER_EOF)) {
  d=5   L9980  T=9 F=7  T=32 F=28  if ((*cur == '<') && (cur[1] == '?')) {
  d=5   L9980  T=1 F=8  T=0 F=32  if ((*cur == '<') && (cur[1] == '?')) {
  d=5   L9995  T=8 F=7  T=32 F=28  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=5   L9995  T=1 F=7  T=0 F=32  else if ((*cur == '<') && (NXT(1) == '!') &&
  d=5   L9996  T=0 F=1  T=0 F=0  (NXT(2) == '-') && (NXT(3) == '-')) {
  d=5   L10004  T=8 F=7  T=32 F=28  else if (*cur == '<') {
  d=5   L10005  T=2 F=6  T=8 F=24  if (NXT(1) == '/') {
  d=5   L10006  T=2 F=0  T=6 F=2  if (ctxt->nameNr <= nameNr)
  d=5   L10019  T=0 F=7  T=0 F=28  else if (*cur == '&') {
--- d=5  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120) ---
  d=5   L11516  T=0 F=20  T=0 F=10  if (avail < 4)
  d=5   L11562  T=0 F=20  T=20 F=0  if ((ctxt->input->cur[2] == 'x') &&
  d=5   L11563  T=0 F=0  T=20 F=0  (ctxt->input->cur[3] == 'm') &&
  d=5   L11564  T=0 F=0  T=20 F=0  (ctxt->input->cur[4] == 'l') &&
  d=5   L11572  T=0 F=0  T=0 F=20  if (ctxt->errNo == XML_ERR_UNSUPPORTED_ENCODING) {
  d=5   L11581  T=0 F=0  T=20 F=0  if ((ctxt->encoding == NULL) &&
  d=5   L11582  T=0 F=0  T=0 F=20  (ctxt->input->encoding != NULL))
  d=5   L11584  T=0 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11584  T=0 F=0  T=20 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11585  T=0 F=0  T=20 F=0  (!ctxt->disableSAX))
  d=5   L11594  T=20 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11594  T=20 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->startDocument) &&
  d=5   L11595  T=20 F=0  T=0 F=0  (!ctxt->disableSAX))
  d=5   L11643  T=0 F=29  T=2 F=28  else if (*ctxt->space == -2)
  d=5   L11657  T=0 F=29  T=8 F=22  if (name == NULL) {
  d=5   L11660  T=0 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11660  T=0 F=0  T=8 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11670  T=0 F=0  T=0 F=2  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=5   L11670  T=0 F=29  T=2 F=20  if (ctxt->validate && ctxt->wellFormed && ctxt->myDoc &&
  d=5   L11722  T=7 F=53  T=0 F=48  if ((avail < 2) && (ctxt->inputNr == 1))
  d=5   L11722  T=7 F=0  T=0 F=0  if ((avail < 2) && (ctxt->inputNr == 1))
  d=5   L11730  T=5 F=13  T=0 F=16  } else if ((cur == '<') && (next == '?')) {
  d=5   L11731  T=3 F=2  T=0 F=0  if ((!terminate) &&
  d=5   L11732  T=3 F=0  T=0 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=5   L11736  T=11 F=2  T=16 F=0  } else if ((cur == '<') && (next != '!')) {
  d=5   L11739  T=2 F=31  T=0 F=24  } else if ((cur == '<') && (next == '!') &&
  d=5   L11739  T=2 F=0  T=0 F=0  } else if ((cur == '<') && (next == '!') &&
  d=5   L11740  T=0 F=2  T=0 F=0  (ctxt->input->cur[2] == '-') &&
  d=5   L11747  T=2 F=0  T=0 F=0  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=5   L11747  T=2 F=31  T=0 F=24  } else if ((cur == '<') && (ctxt->input->cur[1] == '!') &&
  d=5   L11748  T=0 F=2  T=0 F=0  (ctxt->input->cur[2] == '[') &&
  d=5   L11758  T=2 F=31  T=0 F=24  } else if ((cur == '<') && (next == '!') &&
  d=5   L11758  T=2 F=0  T=0 F=0  } else if ((cur == '<') && (next == '!') &&
  d=5   L11759  T=0 F=2  T=0 F=0  (avail < 9)) {
  d=5   L11761  T=2 F=31  T=0 F=24  } else if (cur == '<') {
  d=5   L11784  T=7 F=8  T=0 F=24  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=5   L11784  T=15 F=16  T=24 F=0  if ((!terminate) && (!xmlParseLookupCharData(ctxt)))
  d=5   L11793  T=0 F=4  T=0 F=8  if (avail < 2)
  d=5   L11795  T=0 F=2  T=0 F=8  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=5   L11795  T=2 F=2  T=8 F=0  if ((!terminate) && (!xmlParseLookupChar(ctxt, '>')))
  d=5   L11797  T=2 F=2  T=8 F=0  if (ctxt->sax2) {
  d=5   L11805  T=0 F=4  T=0 F=8  if (ctxt->instate == XML_PARSER_EOF) {
  d=5   L11807  T=4 F=0  T=4 F=4  } else if (ctxt->nameNr == 0) {
  d=5   L11914  T=0 F=61  T=4 F=34  if (avail < 2)
  d=5   L11918  T=20 F=41  T=0 F=34  if ((cur == '<') && (next == '?')) {
  d=5   L11919  T=20 F=0  T=0 F=0  if ((!terminate) &&
  d=5   L11920  T=0 F=20  T=0 F=0  (!xmlParseLookupString(ctxt, 2, "?>", 2)))
  d=5   L11927  T=0 F=20  T=0 F=0  if (ctxt->instate == XML_PARSER_EOF)
  d=5   L11989  T=2 F=19  T=0 F=14  } else if (ctxt->instate == XML_PARSER_EPILOG) {
  d=5   L11996  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
  d=5   L11996  T=2 F=0  T=0 F=0  if ((ctxt->sax) && (ctxt->sax->endDocument != NULL))
--- d=1  xmlBuildURI  (/src/libxml2/uri.c:1903-2152) ---
  d=1   L1921  T=0 F=30  T=30 F=0  if (*URI) {
  d=1   L1923  T=0 F=0  T=0 F=30  if (ref == NULL)
  d=1   L1932  T=0 F=30  T=30 F=0  if ((ref != NULL) && (ref->scheme != NULL)) {
  d=1   L1932  T=0 F=0  T=0 F=30  if ((ref != NULL) && (ref->scheme != NULL)) {
  d=1   L1948  T=0 F=19  T=10 F=0  if (ref)
  d=1   L1952  T=11 F=0  T=0 F=20  if (ref == NULL) {  <-- BLOCKER
  d=1   L1956  T=2 F=9  T=0 F=0  if (bas->fragment != NULL) {
  d=1   L1977  T=0 F=0  T=0 F=20  if (res == NULL)
  d=1   L1979  T=0 F=0  T=0 F=20  if ((ref->scheme == NULL) && (ref->path == NULL) &&
  d=1   L1979  T=0 F=0  T=20 F=0  if ((ref->scheme == NULL) && (ref->path == NULL) &&
  d=1   L2014  T=0 F=0  T=0 F=20  if (ref->scheme != NULL) {
  d=1   L2018  T=0 F=0  T=0 F=20  if (bas->scheme != NULL)
  d=1   L2021  T=0 F=0  T=0 F=20  if (ref->query_raw != NULL)
  d=1   L2023  T=0 F=0  T=0 F=20  else if (ref->query != NULL)
  d=1   L2025  T=0 F=0  T=0 F=20  if (ref->fragment != NULL)
  d=1   L2035  T=0 F=0  T=0 F=20  if ((ref->authority != NULL) || (ref->server != NULL) ||
  d=1   L2035  T=0 F=0  T=0 F=20  if ((ref->authority != NULL) || (ref->server != NULL) ||
  d=1   L2036  T=0 F=0  T=0 F=20  (ref->port != PORT_EMPTY)) {
  d=1   L2050  T=0 F=0  T=0 F=20  if (bas->authority != NULL)
  d=1   L2052  T=0 F=0  T=0 F=20  else if ((bas->server != NULL) || (bas->port != PORT_EMPT...
  d=1   L2052  T=0 F=0  T=0 F=20  else if ((bas->server != NULL) || (bas->port != PORT_EMPT...
  d=1   L2064  T=0 F=0  T=0 F=20  if ((ref->path != NULL) && (ref->path[0] == '/')) {
  d=1   L2064  T=0 F=0  T=20 F=0  if ((ref->path != NULL) && (ref->path[0] == '/')) {
  d=1   L2079  T=0 F=0  T=20 F=0  if (ref->path != NULL)
  d=1   L2081  T=0 F=0  T=20 F=0  if (bas->path != NULL)
  d=1   L2084  T=0 F=0  T=0 F=20  if (res->path == NULL) {
  d=1   L2097  T=0 F=0  T=20 F=0  if (bas->path != NULL) {
  d=1   L2098  T=0 F=0  T=20 F=0  while (bas->path[cur] != 0) {
  d=1   L2099  T=0 F=0  T=188 F=0  while ((bas->path[cur] != 0) && (bas->path[cur] != '/'))
  d=1   L2099  T=0 F=0  T=188 F=20  while ((bas->path[cur] != 0) && (bas->path[cur] != '/'))
  d=1   L2101  T=0 F=0  T=20 F=0  if (bas->path[cur] == 0)
  d=1   L2117  T=0 F=0  T=20 F=0  if (ref->path != NULL && ref->path[0] != 0) {
  d=1   L2117  T=0 F=0  T=20 F=0  if (ref->path != NULL && ref->path[0] != 0) {
  d=1   L2122  T=0 F=0  T=0 F=20  if ((out == 0) && ((bas->server != NULL) || bas->port != ...
  d=1   L2122  T=0 F=0  T=0 F=20  if ((out == 0) && ((bas->server != NULL) || bas->port != ...
  d=1   L2122  T=0 F=0  T=20 F=0  if ((out == 0) && ((bas->server != NULL) || bas->port != ...
  d=1   L2124  T=0 F=0  T=296 F=20  while (ref->path[indx] != 0) {
  d=1   L2145  T=0 F=30  T=30 F=0  if (ref != NULL)
  d=1   L2149  T=0 F=30  T=20 F=10  if (res != NULL)

[off-chain: 1269 additional divergent branches across 154 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=0d76e6f089b338f4, size=154 bytes, fuzzer=grimoire, trial=1, discovered_at=5964s, mutation_op=I2SRandReplace):
  0000: 49 53 4f 2d 38 38 35 39 2d 39 00 31 00 16 a9 05   ISO-8859-9.1....
  0010: 6d 6c 5c 0a 3c 3f 55 54 46 09 31 36 42 45 6c 20   ml\.<?UTF.16BEl 
  0020: 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20 53 59 53   ?><!DOCTYPEa SYS
  0030: 54 45 4d 20 22 22 3e 3c 61 3e 49 53 4f 2d 38 38   TEM ""><a>ISO-88
Seed 2 (id=0000c5065373f0e4, size=86 bytes, fuzzer=grimoire, trial=1, discovered_at=11061s, mutation_op=ByteIncMutator,BytesInsertMutator):
  0000: 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 a6 a6 a6   'http://www.w...
  0010: a6 a7 78 6c 27 27 27 27 27 27 27 69 6e 6b 27 bc   ..xl'''''''ink'.
  0020: 36 6d 6c 5c 0a 3c 3f 6c 3f 3e 3c 21 44 4f 43 54   6ml\.<?l?><!DOCT
  0030: 59 50 45 61 20 53 59 53 54 45 4d 20 22 22 3e 3c   YPEa SYSTEM ""><
Seed 3 (id=073545b81c36b34b, size=78 bytes, fuzzer=grimoire, trial=1, discovered_at=17939s, mutation_op=I2SRandReplace):
  0000: 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 33 45 6f   'http://www.w3Eo
  0010: 26 67 2f fe ff 21 03 01 78 6d 6c 00 5c 0a 3c 3f   &g/..!..xml.\.<?
  0020: 6c 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20 53 59   l?><!DOCTYPEa SY
  0030: 53 54 45 4d 20 22 22 3e 3c 61 3e 3c 62 20 69 3e   STEM ""><a><b i>
Seed 4 (id=078a8f5d4fc24f0c, size=230 bytes, fuzzer=grimoire, trial=1, discovered_at=18340s, mutation_op=BitFlipMutator,BytesInsertCopyMutator):
  0000: 27 68 74 74 70 3a 2f 2f 3f 25 25 4f 43 54 59 50   'http://?%%OCTYP
  0010: 45 61 20 53 59 53 54 25 25 25 25 25 25 25 35 25   Ea SYST%%%%%%%5%
  0020: 25 25 25 25 44 4f 43 54 59 50 45 61 20 53 59 53   %%%%DOCTYPEa SYS
  0030: 54 45 4d 20 22 22 3e 3c 61 3e 3c 62 20 0a 6c 20   TEM ""><a><b .l 
Seed 5 (id=018147f2010d4d07, size=66 bytes, fuzzer=grimoire, trial=1, discovered_at=19449s, mutation_op=I2SRandReplace):
  0000: 27 68 74 74 70 3a 2f 2f 23 2e 2f 2f 30 3d 2f 2f   'http://#.//0=//
  0010: 2f 2f 2f 2f 2f 2f 2f 2f 2f 2f 62 06 00 53 53 5c   //////////b..SS\
  0020: 0a 3c 3f 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45   .<?l ?><!DOCTYPE
  0030: 61 20 53 59 53 54 45 4d 20 22 22 3e 3c 61 3e 5c   a SYSTEM ""><a>\

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0243680d59374a7c, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=54s, mutation_op=WordInterestingMutator,TokenReplace):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=037ce516e253ed97, size=556 bytes, fuzzer=cmplog, trial=1, discovered_at=96s, mutation_op=QwordAddMutator,BitFlipMutator,CrossoverInsertMutator,BytesExpandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=01986dbadd87a561, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=128s, mutation_op=ByteDecMutator,CrossoverReplaceMutator,BytesRandInsertMutator,ByteAddMutator,ByteAddMutator,CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=001c8c9d4510710d, size=248 bytes, fuzzer=cmplog, trial=1, discovered_at=411s, mutation_op=ByteNegMutator,BytesCopyMutator,BytesInsertMutator,ByteIncMutator,BytesSwapMutator,BytesDeleteMutator,TokenReplace):
  0000: 5f 5f 5f 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ___.127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=00ebab469d057524, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=573s, mutation_op=ByteFlipMutator,ByteNegMutator,BitFlipMutator,CrossoverReplaceMutator):
  0000: 37 58 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20   7X72.xml\.<?xml 
  0010: 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a   version="1.0"?>.
  0020: 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53 54   <!DOCTYPE a SYST
  0030: 45 4d 20 22 64 74 64 73 2a 31 32 37 37 37 32 2e   EM "dtds*127772.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  27(')x9 49(I)x1                     06(.)x6 5f(_)x1 37(7)x1 2b(+)x1 +1u  DIFFER
   0x0001  68(h)x8 53(S)x1 67(g)x1             00(.)x7 5f(_)x1 58(X)x1 ff(.)x1     DIFFER
   0x0002  74(t)x8 4f(O)x1 27(')x1             00(.)x7 5f(_)x1 37(7)x1 ff(.)x1     DIFFER
   0x0003  74(t)x7 2d(-)x1 73(s)x1 68(h)x1     00(.)x8 32(2)x1 ec(.)x1             DIFFER
   0x0004  70(p)x8 38(8)x1 74(t)x1             31(1)x9 2e(.)x1                     DIFFER
   0x0005  3a(:)x8 38(8)x1 74(t)x1             32(2)x9 78(x)x1                     DIFFER
   0x0006  2f(/)x8 35(5)x1 70(p)x1             37(7)x9 6d(m)x1                     DIFFER
   0x0007  2f(/)x8 39(9)x1 3a(:)x1             37(7)x9 6c(l)x1                     DIFFER
   0x0008  77(w)x2 23(#)x2 2d(-)x1 3f(?)x1 +4u  37(7)x9 5c(\)x1                     DIFFER
   0x0009  77(w)x2 39(9)x1 25(%)x1 2e(.)x1 +5u  32(2)x9 0a(.)x1                     PARTIAL
   0x000a  77(w)x2 2f(/)x2 00(.)x1 25(%)x1 +4u  2e(.)x9 3c(<)x1                     DIFFER
   0x000b  2e(.)x2 7e(~)x2 31(1)x1 4f(O)x1 +4u  78(x)x9 3f(?)x1                     DIFFER
   0x000c  77(w)x2 a9(.)x2 00(.)x1 43(C)x1 +4u  6d(m)x9 78(x)x1                     DIFFER
   0x000d  16(.)x1 a6(.)x1 33(3)x1 54(T)x1 +6u  6c(l)x9 6d(m)x1                     DIFFER
   0x000e  a9(.)x1 a6(.)x1 45(E)x1 59(Y)x1 +6u  5c(\)x9 6c(l)x1                     DIFFER
   0x000f  05(.)x1 a6(.)x1 6f(o)x1 50(P)x1 +6u  0a(.)x9 20( )x1                     DIFFER
   0x0010  6d(m)x1 a6(.)x1 26(&)x1 45(E)x1 +6u  3c(<)x9 76(v)x1                     DIFFER
   0x0011  2f(/)x2 6c(l)x1 a7(.)x1 67(g)x1 +5u  3f(?)x9 65(e)x1                     DIFFER
   0x0012  2f(/)x3 5c(\)x1 78(x)x1 20( )x1 +4u  78(x)x9 72(r)x1                     PARTIAL
   0x0013  53(S)x2 2f(/)x2 0a(.)x1 6c(l)x1 +4u  6d(m)x9 73(s)x1                     DIFFER
   0x0014  3c(<)x1 27(')x1 ff(.)x1 59(Y)x1 +6u  6c(l)x9 69(i)x1                     DIFFER
   0x0015  3f(?)x1 27(')x1 21(!)x1 53(S)x1 +6u  20( )x9 6f(o)x1                     DIFFER
   0x0016  55(U)x1 27(')x1 03(.)x1 54(T)x1 +6u  76(v)x9 6e(n)x1                     DIFFER
   0x0017  54(T)x1 27(')x1 01(.)x1 25(%)x1 +6u  65(e)x9 3d(=)x1                     DIFFER
   0x0018  46(F)x1 27(')x1 78(x)x1 25(%)x1 +6u  72(r)x9 22(")x1                     PARTIAL
   0x0019  09(.)x1 27(')x1 6d(m)x1 25(%)x1 +6u  73(s)x9 31(1)x1                     DIFFER
   0x001a  31(1)x1 27(')x1 6c(l)x1 25(%)x1 +6u  69(i)x9 2e(.)x1                     DIFFER
   0x001b  36(6)x1 69(i)x1 00(.)x1 25(%)x1 +6u  6f(o)x9 30(0)x1                     DIFFER
   0x001c  42(B)x1 6e(n)x1 5c(\)x1 25(%)x1 +6u  6e(n)x9 22(")x1                     PARTIAL
   0x001d  0a(.)x2 45(E)x1 6b(k)x1 25(%)x1 +5u  3d(=)x9 3f(?)x1                     DIFFER
   0x001e  6c(l)x1 27(')x1 3c(<)x1 35(5)x1 +6u  22(")x9 3e(>)x1                     PARTIAL
   0x001f  20( )x1 bc(.)x1 3f(?)x1 25(%)x1 +6u  31(1)x9 0a(.)x1                     DIFFER
   0x0020  3f(?)x1 36(6)x1 6c(l)x1 25(%)x1 +6u  2e(.)x9 3c(<)x1                     DIFFER
   0x0021  3e(>)x1 6d(m)x1 3f(?)x1 25(%)x1 +6u  30(0)x9 21(!)x1                     DIFFER
   0x0022  3c(<)x1 6c(l)x1 3e(>)x1 25(%)x1 +6u  22(")x9 44(D)x1                     PARTIAL
   0x0023  21(!)x1 5c(\)x1 3c(<)x1 25(%)x1 +6u  3f(?)x9 4f(O)x1                     DIFFER
   0x0024  44(D)x2 0a(.)x1 21(!)x1 20( )x1 +5u  3e(>)x9 43(C)x1                     DIFFER
   0x0025  4f(O)x2 3c(<)x1 44(D)x1 3f(?)x1 +5u  0a(.)x9 54(T)x1                     DIFFER
   0x0026  43(C)x2 3f(?)x1 4f(O)x1 3e(>)x1 +5u  3c(<)x9 59(Y)x1                     DIFFER
   0x0027  54(T)x3 6c(l)x1 43(C)x1 3c(<)x1 +4u  21(!)x9 50(P)x1                     DIFFER
   ... (24 more divergent offsets)
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

--- grimoire ---
**Baseline relationship**: grimoire builds on the full cmplog stack —
it includes the `CmpLogObserver`, the `TracingStage`, and the
`I2SRandReplace` (i2s) stage — and ADDS a `GeneralizationStage` plus
Grimoire structural mutators. The single-technique delta is therefore
`grimoire` vs `cmplog` (both have I2S; grimoire adds generalization +
Grimoire mutators), not vs naive.

**Instrumentation**: cmplog's edge counters + per-execution CMP buffer
(`CmpLogObserver`).

**Feedback**: edge-bucket `MaxMapFeedback`.

**Mutators / stages**: stages are
`[generalization, tracing, i2s, havoc, grimoire]`. `GeneralizationStage`
replaces concrete byte runs in a corpus entry with `<GAP>` placeholders
(a generalised input) by repeatedly re-executing and checking that
coverage is preserved. The Grimoire mutators —
`GrimoireExtensionMutator`, `GrimoireRecursiveReplacementMutator`,
`GrimoireStringReplacementMutator`, `GrimoireRandomDeleteMutator` —
splice and recurse on these generalised token/gap structures
(string-based, grammar-free structural mutation). `I2SRandReplace` (the
cmplog i2s stage) also runs.

**Observed `mutation_op` in seed metadata**: all grimoire stages (i2s,
havoc, grimoire) are wrapped in `LineageMutatorWrap` with **no
per-operator name list**, so grimoire seeds appear nameless in lineage
(`mutation_op = -`). As with mopt, nameless rows are NOT an
I2S-exclusive signal here — and grimoire genuinely runs I2S too, so the
two are not separable from lineage names.

**Per-execution cost**: cmplog's per-CMP cost, plus extra executions
during generalization (each candidate gap is validated by a re-run).

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  /home/miao/BlockerAnalyzer/prompts/libxml2_7022.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7022,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [grimoire>cmplog (grimoire_structural)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7022 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7022 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7022 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).