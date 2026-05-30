==== BLOCKER ====
Target: libxml2
Branch ID: 6985
Location: /src/libxml2/uri.c:1178:17
Enclosing function: xmlSaveUri
Source line:             if (uri->port > 0) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            7        3          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    8        2          0  REFERENCE
value_profile_cmplog             4        6          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     5        5          0  REFERENCE
mopt                             4        6          0  REFERENCE
minimizer                        9        1          0  REFERENCE
fast                             9        1          0  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=7.70h  loser=21.30h
  avg hitcount on branch: winner=5  loser=0
  prob_div=0.80  dur_div=13.60h  hit_div=5
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6985/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlSaveUri (/src/libxml2/uri.c:1075-1340) ---
[ ]  1073   */
[ ]  1074  xmlChar *
[B]  1075  xmlSaveUri(xmlURIPtr uri) {
[B]  1076      xmlChar *ret = NULL;
[B]  1077      xmlChar *temp;
[B]  1078      const char *p;
[B]  1079      int len;
[B]  1080      int max;
[ ]  1081  
[B]  1082      if (uri == NULL) return(NULL);
[ ]  1083  
[ ]  1084  
[B]  1085      max = 80;
[B]  1086      ret = (xmlChar *) xmlMallocAtomic(max + 1);
[B]  1087      if (ret == NULL) {
[ ]  1088          xmlURIErrMemory("saving URI\n");
[ ]  1089  	return(NULL);
[ ]  1090      }
[B]  1091      len = 0;
[ ]  1092  
[B]  1093      if (uri->scheme != NULL) {
[B]  1094  	p = uri->scheme;
[B]  1095  	while (*p != 0) {
[B]  1096  	    if (len >= max) {
[ ]  1097                  temp = xmlSaveUriRealloc(ret, &max);
[ ]  1098                  if (temp == NULL) goto mem_error;
[ ]  1099  		ret = temp;
[ ]  1100  	    }
[B]  1101  	    ret[len++] = *p++;
[B]  1102  	}
[B]  1103  	if (len >= max) {
[ ]  1104              temp = xmlSaveUriRealloc(ret, &max);
[ ]  1105              if (temp == NULL) goto mem_error;
[ ]  1106              ret = temp;
[ ]  1107  	}
[B]  1108  	ret[len++] = ':';
[B]  1109      }
[B]  1110      if (uri->opaque != NULL) {
[ ]  1111  	p = uri->opaque;
[ ]  1112  	while (*p != 0) {
[ ]  1113  	    if (len + 3 >= max) {
[ ]  1114                  temp = xmlSaveUriRealloc(ret, &max);
[ ]  1115                  if (temp == NULL) goto mem_error;
[ ]  1116                  ret = temp;
[ ]  1117  	    }
[ ]  1118  	    if (IS_RESERVED(*(p)) || IS_UNRESERVED(*(p)))
[ ]  1119  		ret[len++] = *p++;
[ ]  1120  	    else {
[ ]  1121  		int val = *(unsigned char *)p++;
[ ]  1122  		int hi = val / 0x10, lo = val % 0x10;
[ ]  1123  		ret[len++] = '%';
[ ]  1124  		ret[len++] = hi + (hi > 9? 'A'-10 : '0');
[ ]  1125  		ret[len++] = lo + (lo > 9? 'A'-10 : '0');
[ ]  1126  	    }
[ ]  1127  	}
[B]  1128      } else {
[B]  1129  	if ((uri->server != NULL) || (uri->port != PORT_EMPTY)) {
[B]  1130  	    if (len + 3 >= max) {
[ ]  1131                  temp = xmlSaveUriRealloc(ret, &max);
[ ]  1132                  if (temp == NULL) goto mem_error;
[ ]  1133                  ret = temp;
[ ]  1134  	    }
[B]  1135  	    ret[len++] = '/';
[B]  1136  	    ret[len++] = '/';
[B]  1137  	    if (uri->user != NULL) {
[L]  1138  		p = uri->user;
[L]  1139  		while (*p != 0) {
[L]  1140  		    if (len + 3 >= max) {
[L]  1141                          temp = xmlSaveUriRealloc(ret, &max);
[L]  1142                          if (temp == NULL) goto mem_error;
[L]  1143                          ret = temp;
[L]  1144  		    }
[L]  1145  		    if ((IS_UNRESERVED(*(p))) ||
[L]  1146  			((*(p) == ';')) || ((*(p) == ':')) ||
[L]  1147  			((*(p) == '&')) || ((*(p) == '=')) ||
[L]  1148  			((*(p) == '+')) || ((*(p) == '$')) ||
[L]  1149  			((*(p) == ',')))
[L]  1150  			ret[len++] = *p++;
[L]  1151  		    else {
[L]  1152  			int val = *(unsigned char *)p++;
[L]  1153  			int hi = val / 0x10, lo = val % 0x10;
[L]  1154  			ret[len++] = '%';
[L]  1155  			ret[len++] = hi + (hi > 9? 'A'-10 : '0');
[L]  1156  			ret[len++] = lo + (lo > 9? 'A'-10 : '0');
[L]  1157  		    }
[L]  1158  		}
[L]  1159  		if (len + 3 >= max) {
[ ]  1160                      temp = xmlSaveUriRealloc(ret, &max);
[ ]  1161                      if (temp == NULL) goto mem_error;
[ ]  1162                      ret = temp;
[ ]  1163  		}
[L]  1164  		ret[len++] = '@';
[L]  1165  	    }
[B]  1166  	    if (uri->server != NULL) {
[B]  1167  		p = uri->server;
[B]  1168  		while (*p != 0) {
[B]  1169  		    if (len >= max) {
[L]  1170  			temp = xmlSaveUriRealloc(ret, &max);
[L]  1171  			if (temp == NULL) goto mem_error;
[L]  1172  			ret = temp;
[L]  1173  		    }
[ ]  1174                      /* TODO: escaping? */
[B]  1175  		    ret[len++] = (xmlChar) *p++;
[B]  1176  		}
[B]  1177  	    }
[B]  1178              if (uri->port > 0) { <-- BLOCKER
[W]  1179                  if (len + 10 >= max) {
[ ]  1180                      temp = xmlSaveUriRealloc(ret, &max);
[ ]  1181                      if (temp == NULL) goto mem_error;
[ ]  1182                      ret = temp;
[ ]  1183                  }
[W]  1184                  len += snprintf((char *) &ret[len], max - len, ":%d", uri->port);
[W]  1185              }
[B]  1186  	} else if (uri->authority != NULL) {
[ ]  1187  	    if (len + 3 >= max) {
[ ]  1188                  temp = xmlSaveUriRealloc(ret, &max);
[ ]  1189                  if (temp == NULL) goto mem_error;
[ ]  1190                  ret = temp;
[ ]  1191  	    }
[ ]  1192  	    ret[len++] = '/';
[ ]  1193  	    ret[len++] = '/';
[ ]  1194  	    p = uri->authority;
[ ]  1195  	    while (*p != 0) {
[ ]  1196  		if (len + 3 >= max) {
[ ]  1197                      temp = xmlSaveUriRealloc(ret, &max);
[ ]  1198                      if (temp == NULL) goto mem_error;
[ ]  1199                      ret = temp;
[ ]  1200  		}
[ ]  1201  		if ((IS_UNRESERVED(*(p))) ||
[ ]  1202                      ((*(p) == '$')) || ((*(p) == ',')) || ((*(p) == ';')) ||
[ ]  1203                      ((*(p) == ':')) || ((*(p) == '@')) || ((*(p) == '&')) ||
[ ]  1204                      ((*(p) == '=')) || ((*(p) == '+')))
[ ]  1205  		    ret[len++] = *p++;
[ ]  1206  		else {
[ ]  1207  		    int val = *(unsigned char *)p++;
[ ]  1208  		    int hi = val / 0x10, lo = val % 0x10;
[ ]  1209  		    ret[len++] = '%';
[ ]  1210  		    ret[len++] = hi + (hi > 9? 'A'-10 : '0');
[ ]  1211  		    ret[len++] = lo + (lo > 9? 'A'-10 : '0');
[ ]  1212  		}
[ ]  1213  	    }
[B]  1214  	} else if (uri->scheme != NULL) {
[ ]  1215  	    if (len + 3 >= max) {
[ ]  1216                  temp = xmlSaveUriRealloc(ret, &max);
[ ]  1217                  if (temp == NULL) goto mem_error;
[ ]  1218                  ret = temp;
[ ]  1219  	    }
[ ]  1220  	}
[B]  1221  	if (uri->path != NULL) {
[B]  1222  	    p = uri->path;
[ ]  1223  	    /*
[ ]  1224  	     * the colon in file:///d: should not be escaped or
[ ]  1225  	     * Windows accesses fail later.
[ ]  1226  	     */
[B]  1227  	    if ((uri->scheme != NULL) &&
[B]  1228  		(p[0] == '/') &&
[B]  1229  		(((p[1] >= 'a') && (p[1] <= 'z')) ||
[B]  1230  		 ((p[1] >= 'A') && (p[1] <= 'Z'))) &&
[B]  1231  		(p[2] == ':') &&
[B]  1232  	        (xmlStrEqual(BAD_CAST uri->scheme, BAD_CAST "file"))) {
[ ]  1233  		if (len + 3 >= max) {
[ ]  1234                      temp = xmlSaveUriRealloc(ret, &max);
[ ]  1235                      if (temp == NULL) goto mem_error;
[ ]  1236                      ret = temp;
[ ]  1237  		}
[ ]  1238  		ret[len++] = *p++;
[ ]  1239  		ret[len++] = *p++;
[ ]  1240  		ret[len++] = *p++;
[ ]  1241  	    }
[B]  1242  	    while (*p != 0) {
[B]  1243  		if (len + 3 >= max) {
[L]  1244                      temp = xmlSaveUriRealloc(ret, &max);
[L]  1245                      if (temp == NULL) goto mem_error;
[L]  1246                      ret = temp;
[L]  1247  		}
[B]  1248  		if ((IS_UNRESERVED(*(p))) || ((*(p) == '/')) ||
[B]  1249                      ((*(p) == ';')) || ((*(p) == '@')) || ((*(p) == '&')) ||
[B]  1250  	            ((*(p) == '=')) || ((*(p) == '+')) || ((*(p) == '$')) ||
[B]  1251  	            ((*(p) == ',')))
[B]  1252  		    ret[len++] = *p++;
[B]  1253  		else {
[B]  1254  		    int val = *(unsigned char *)p++;
[B]  1255  		    int hi = val / 0x10, lo = val % 0x10;
[B]  1256  		    ret[len++] = '%';
[B]  1257  		    ret[len++] = hi + (hi > 9? 'A'-10 : '0');
[B]  1258  		    ret[len++] = lo + (lo > 9? 'A'-10 : '0');
[B]  1259  		}
[B]  1260  	    }
[B]  1261  	}
[B]  1262  	if (uri->query_raw != NULL) {
[L]  1263  	    if (len + 1 >= max) {
[ ]  1264                  temp = xmlSaveUriRealloc(ret, &max);
[ ]  1265                  if (temp == NULL) goto mem_error;
[ ]  1266                  ret = temp;
[ ]  1267  	    }
[L]  1268  	    ret[len++] = '?';
[L]  1269  	    p = uri->query_raw;
[L]  1270  	    while (*p != 0) {
[L]  1271  		if (len + 1 >= max) {
[ ]  1272                      temp = xmlSaveUriRealloc(ret, &max);
[ ]  1273                      if (temp == NULL) goto mem_error;
[ ]  1274                      ret = temp;
[ ]  1275  		}
[L]  1276  		ret[len++] = *p++;
[L]  1277  	    }
[B]  1278  	} else if (uri->query != NULL) {
[ ]  1279  	    if (len + 3 >= max) {
[ ]  1280                  temp = xmlSaveUriRealloc(ret, &max);
[ ]  1281                  if (temp == NULL) goto mem_error;
[ ]  1282                  ret = temp;
[ ]  1283  	    }
[ ]  1284  	    ret[len++] = '?';
[ ]  1285  	    p = uri->query;
[ ]  1286  	    while (*p != 0) {
[ ]  1287  		if (len + 3 >= max) {
[ ]  1288                      temp = xmlSaveUriRealloc(ret, &max);
[ ]  1289                      if (temp == NULL) goto mem_error;
[ ]  1290                      ret = temp;
[ ]  1291  		}
[ ]  1292  		if ((IS_UNRESERVED(*(p))) || (IS_RESERVED(*(p))))
[ ]  1293  		    ret[len++] = *p++;
[ ]  1294  		else {
[ ]  1295  		    int val = *(unsigned char *)p++;
[ ]  1296  		    int hi = val / 0x10, lo = val % 0x10;
[ ]  1297  		    ret[len++] = '%';
[ ]  1298  		    ret[len++] = hi + (hi > 9? 'A'-10 : '0');
[ ]  1299  		    ret[len++] = lo + (lo > 9? 'A'-10 : '0');
[ ]  1300  		}
[ ]  1301  	    }
[ ]  1302  	}
[B]  1303      }
[B]  1304      if (uri->fragment != NULL) {
[ ]  1305  	if (len + 3 >= max) {
[ ]  1306              temp = xmlSaveUriRealloc(ret, &max);
[ ]  1307              if (temp == NULL) goto mem_error;
[ ]  1308              ret = temp;
[ ]  1309  	}
[ ]  1310  	ret[len++] = '#';
[ ]  1311  	p = uri->fragment;
[ ]  1312  	while (*p != 0) {
[ ]  1313  	    if (len + 3 >= max) {
[ ]  1314                  temp = xmlSaveUriRealloc(ret, &max);
[ ]  1315                  if (temp == NULL) goto mem_error;
[ ]  1316                  ret = temp;
[ ]  1317  	    }
[ ]  1318  	    if ((IS_UNRESERVED(*(p))) || (IS_RESERVED(*(p))))
[ ]  1319  		ret[len++] = *p++;
[ ]  1320  	    else {
[ ]  1321  		int val = *(unsigned char *)p++;
[ ]  1322  		int hi = val / 0x10, lo = val % 0x10;
[ ]  1323  		ret[len++] = '%';
[ ]  1324  		ret[len++] = hi + (hi > 9? 'A'-10 : '0');
[ ]  1325  		ret[len++] = lo + (lo > 9? 'A'-10 : '0');
[ ]  1326  	    }
[ ]  1327  	}
[ ]  1328      }
[B]  1329      if (len >= max) {
[ ]  1330          temp = xmlSaveUriRealloc(ret, &max);
[ ]  1331          if (temp == NULL) goto mem_error;
[ ]  1332          ret = temp;
[ ]  1333      }
[B]  1334      ret[len] = 0;
[B]  1335      return(ret);
[ ]  1336  
[ ]  1337  mem_error:
[ ]  1338      xmlFree(ret);
[ ]  1339      return(NULL);
[B]  1340  }

--- Caller (1 hop): xmlBuildURI (/src/libxml2/uri.c:1903-2152, calls xmlSaveUri at line 1949) (±10 around call site) ---
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
[B]  1949  	    val = xmlSaveUri(ref); <-- CALL
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

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  xmlBuildURI  (/src/libxml2/uri.c:1903-2152, calls xmlSaveUri at line 1949)
hop 2  xmlPrintURI  (/src/libxml2/uri.c:1350-1358, calls xmlSaveUri at line 1353)
hop 3  parser.c:xmlCreateEntityParserCtxtInternal  (/src/libxml2/parser.c:13782-13835, calls xmlBuildURI at line 13803)
hop 3  relaxng.c:xmlRelaxNGCleanupTree  (/src/libxml2/relaxng.c:7043-7472, calls xmlBuildURI at line 7126)
hop 4  parser.c:xmlParseExternalEntityPrivate  (/src/libxml2/parser.c:12831-13042, calls parser.c:xmlCreateEntityParserCtxtInternal at line 12854)
hop 4  xmlCreateEntityParserCtxt  (/src/libxml2/parser.c:13851-13854, calls parser.c:xmlCreateEntityParserCtxtInternal at line 13852)
hop 4  relaxng.c:xmlRelaxNGCleanupDoc  (/src/libxml2/relaxng.c:7486-7500, calls relaxng.c:xmlRelaxNGCleanupTree at line 7498)
hop 5  xmlParseReference  (/src/libxml2/parser.c:7173-7586, calls parser.c:xmlParseExternalEntityPrivate at line 7303)
hop 5  relaxng.c:xmlRelaxNGLoadExternalRef  (/src/libxml2/relaxng.c:1953-2027, calls relaxng.c:xmlRelaxNGCleanupDoc at line 2018)
hop 5  relaxng.c:xmlRelaxNGLoadInclude  (/src/libxml2/relaxng.c:1605-1765, calls relaxng.c:xmlRelaxNGCleanupDoc at line 1681)
hop 6  parser.c:xmlParseContentInternal  (/src/libxml2/parser.c:9969-10033, calls xmlParseReference at line 10020)
hop 6  parser.c:xmlParseTryOrFinish  (/src/libxml2/parser.c:11404-12120, calls xmlParseReference at line 11768)
hop 7  xmlParseChunk  (/src/libxml2/parser.c:12135-12300, calls parser.c:xmlParseTryOrFinish at line 12234)
hop 7  xmlParseContent  (/src/libxml2/parser.c:10045-10057, calls parser.c:xmlParseContentInternal at line 10048)
hop 7  xmlParseElement  (/src/libxml2/parser.c:10076-10094, calls parser.c:xmlParseContentInternal at line 10080)
hop 8  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlParseChunk at line 67)
hop 8  xmlParseDocument  (/src/libxml2/parser.c:10810-10985, calls xmlParseElement at line 10941)
hop 8  xmlParseExtParsedEnt  (/src/libxml2/parser.c:11002-11091, calls xmlParseContent at line 11073)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      28      7810  uri.c:is_hex  (/src/libxml2/uri.c:1607-1613)
      39       964  uri.c:xmlCleanURI  (/src/libxml2/uri.c:1367-1388)
      54       759  uri.c:xmlParse3986Segment  (/src/libxml2/uri.c:564-577)
      29       623  xmlURIUnescapeString  (/src/libxml2/uri.c:1630-1677)
      17       392  xmlCreateURI  (/src/libxml2/uri.c:1028-1039)
      17       392  xmlFreeURI  (/src/libxml2/uri.c:1397-1410)
      16       368  uri.c:xmlParse3986Scheme  (/src/libxml2/uri.c:214-232)
      16       368  uri.c:xmlParse3986URI  (/src/libxml2/uri.c:873-899)
      16       368  uri.c:xmlParse3986URIReference  (/src/libxml2/uri.c:914-935)
      11       248  uri.c:xmlParse3986RelativeRef  (/src/libxml2/uri.c:819-857)
      11       248  xmlParseURI  (/src/libxml2/uri.c:948-963)
      11       243  uri.c:xmlParse3986PathNoScheme  (/src/libxml2/uri.c:721-747)
       9       236  uri.c:xmlParse3986Userinfo  (/src/libxml2/uri.c:371-390)
       9       236  uri.c:xmlParse3986Host  (/src/libxml2/uri.c:446-506)
       9       236  uri.c:xmlParse3986Authority  (/src/libxml2/uri.c:522-544)
... (15 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlBuildURI  (/src/libxml2/uri.c:1903-2152) ---
  d=2   L1918  T=0 F=3  T=0 F=72  if (URI == NULL)
  d=2   L1921  T=3 F=0  T=72 F=0  if (*URI) {
  d=2   L1923  T=0 F=3  T=0 F=72  if (ref == NULL)
  d=2   L1930  T=0 F=3  T=0 F=72  if (ret != 0)
  d=2   L1932  T=3 F=0  T=72 F=0  if ((ref != NULL) && (ref->scheme != NULL)) {
  d=2   L1932  T=0 F=3  T=0 F=72  if ((ref != NULL) && (ref->scheme != NULL)) {
  d=2   L1939  T=1 F=2  T=24 F=48  if (base == NULL)
  d=2   L1943  T=0 F=2  T=0 F=48  if (bas == NULL)
  d=2   L1947  T=2 F=1  T=48 F=24  if (ret != 0) {
  d=2   L1948  T=2 F=0  T=48 F=0  if (ref)
  d=2   L1952  T=0 F=1  T=0 F=24  if (ref == NULL) {
  d=2   L1977  T=0 F=1  T=0 F=24  if (res == NULL)
  d=2   L1979  T=0 F=1  T=0 F=24  if ((ref->scheme == NULL) && (ref->path == NULL) &&
  d=2   L1979  T=1 F=0  T=24 F=0  if ((ref->scheme == NULL) && (ref->path == NULL) &&
  d=2   L2014  T=0 F=1  T=0 F=24  if (ref->scheme != NULL) {
  d=2   L2018  T=1 F=0  T=24 F=0  if (bas->scheme != NULL)
  d=2   L2021  T=0 F=1  T=1 F=23  if (ref->query_raw != NULL)
  d=2   L2023  T=0 F=1  T=0 F=23  else if (ref->query != NULL)
  d=2   L2025  T=0 F=1  T=0 F=24  if (ref->fragment != NULL)
  d=2   L2035  T=0 F=1  T=0 F=24  if ((ref->authority != NULL) || (ref->server != NULL) ||
  d=2   L2035  T=0 F=1  T=0 F=24  if ((ref->authority != NULL) || (ref->server != NULL) ||
  d=2   L2036  T=0 F=1  T=0 F=24  (ref->port != PORT_EMPTY)) {
  d=2   L2050  T=0 F=1  T=0 F=24  if (bas->authority != NULL)
  d=2   L2052  T=1 F=0  T=24 F=0  else if ((bas->server != NULL) || (bas->port != PORT_EMPT...
  d=2   L2053  T=1 F=0  T=24 F=0  if (bas->server != NULL)
  d=2   L2055  T=0 F=1  T=2 F=22  if (bas->user != NULL)
  d=2   L2064  T=0 F=1  T=1 F=23  if ((ref->path != NULL) && (ref->path[0] == '/')) {
  d=2   L2064  T=1 F=0  T=24 F=0  if ((ref->path != NULL) && (ref->path[0] == '/')) {
  d=2   L2079  T=1 F=0  T=23 F=0  if (ref->path != NULL)
  d=2   L2081  T=1 F=0  T=13 F=10  if (bas->path != NULL)
  d=2   L2084  T=0 F=1  T=0 F=23  if (res->path == NULL) {
  d=2   L2097  T=1 F=0  T=13 F=10  if (bas->path != NULL) {
  d=2   L2098  T=5 F=0  T=78 F=1  while (bas->path[cur] != 0) {
  d=2   L2099  T=23 F=4  T=813 F=66  while ((bas->path[cur] != 0) && (bas->path[cur] != '/'))
  d=2   L2099  T=27 F=1  T=879 F=12  while ((bas->path[cur] != 0) && (bas->path[cur] != '/'))
  d=2   L2101  T=1 F=4  T=12 F=66  if (bas->path[cur] == 0)
  d=2   L2105  T=21 F=4  T=361 F=66  while (out < cur) {
  d=2   L2117  T=1 F=0  T=23 F=0  if (ref->path != NULL && ref->path[0] != 0) {
  d=2   L2117  T=1 F=0  T=23 F=0  if (ref->path != NULL && ref->path[0] != 0) {
  d=2   L2122  T=0 F=0  T=10 F=0  if ((out == 0) && ((bas->server != NULL) || bas->port != ...
  d=2   L2122  T=0 F=1  T=10 F=13  if ((out == 0) && ((bas->server != NULL) || bas->port != ...
  d=2   L2124  T=15 F=1  T=330 F=23  while (ref->path[indx] != 0) {
  d=2   L2145  T=3 F=0  T=72 F=0  if (ref != NULL)
  d=2   L2147  T=2 F=1  T=48 F=24  if (bas != NULL)
  d=2   L2149  T=1 F=2  T=24 F=48  if (res != NULL)
--- d=1  xmlSaveUri  (/src/libxml2/uri.c:1075-1340) ---
  d=1   L1082  T=0 F=4  T=0 F=96  if (uri == NULL) return(NULL);
  d=1   L1087  T=0 F=4  T=0 F=96  if (ret == NULL) {
  d=1   L1093  T=1 F=3  T=24 F=72  if (uri->scheme != NULL) {
  d=1   L1095  T=1 F=1  T=63 F=24  while (*p != 0) {
  d=1   L1096  T=0 F=1  T=0 F=63  if (len >= max) {
  d=1   L1103  T=0 F=1  T=0 F=24  if (len >= max) {
  d=1   L1110  T=0 F=4  T=0 F=96  if (uri->opaque != NULL) {
  d=1   L1129  T=0 F=3  T=0 F=72  if ((uri->server != NULL) || (uri->port != PORT_EMPTY)) {
  d=1   L1129  T=1 F=3  T=24 F=72  if ((uri->server != NULL) || (uri->port != PORT_EMPTY)) {
  d=1   L1130  T=0 F=1  T=0 F=24  if (len + 3 >= max) {
  d=1   L1137  T=0 F=1  T=2 F=22  if (uri->user != NULL) {
  d=1   L1139  T=0 F=0  T=46 F=2  while (*p != 0) {
  d=1   L1140  T=0 F=0  T=1 F=45  if (len + 3 >= max) {
  d=1   L1142  T=0 F=0  T=0 F=1  if (temp == NULL) goto mem_error;
  d=1   L1146  T=0 F=0  T=1 F=29  ((*(p) == ';')) || ((*(p) == ':')) ||
  d=1   L1146  T=0 F=0  T=0 F=30  ((*(p) == ';')) || ((*(p) == ':')) ||
  d=1   L1147  T=0 F=0  T=0 F=28  ((*(p) == '&')) || ((*(p) == '=')) ||
  d=1   L1147  T=0 F=0  T=1 F=28  ((*(p) == '&')) || ((*(p) == '=')) ||
  d=1   L1148  T=0 F=0  T=0 F=28  ((*(p) == '+')) || ((*(p) == '$')) ||
  d=1   L1148  T=0 F=0  T=0 F=28  ((*(p) == '+')) || ((*(p) == '$')) ||
  d=1   L1149  T=0 F=0  T=0 F=28  ((*(p) == ',')))
  d=1   L1155  T=0 F=0  T=16 F=12  ret[len++] = hi + (hi > 9? 'A'-10 : '0');
  d=1   L1156  T=0 F=0  T=1 F=27  ret[len++] = lo + (lo > 9? 'A'-10 : '0');
  d=1   L1159  T=0 F=0  T=0 F=2  if (len + 3 >= max) {
  d=1   L1166  T=1 F=0  T=24 F=0  if (uri->server != NULL) {
  d=1   L1168  T=5 F=1  T=777 F=24  while (*p != 0) {
  d=1   L1169  T=0 F=5  T=4 F=773  if (len >= max) {
  d=1   L1171  T=0 F=0  T=0 F=4  if (temp == NULL) goto mem_error;
  d=1   L1178  T=1 F=0  T=0 F=24  if (uri->port > 0) {  <-- BLOCKER
  d=1   L1179  T=0 F=1  T=0 F=0  if (len + 10 >= max) {
  d=1   L1186  T=0 F=3  T=0 F=72  } else if (uri->authority != NULL) {
  d=1   L1214  T=0 F=3  T=0 F=72  } else if (uri->scheme != NULL) {
  d=1   L1221  T=4 F=0  T=96 F=0  if (uri->path != NULL) {
  d=1   L1227  T=1 F=3  T=24 F=72  if ((uri->scheme != NULL) &&
  d=1   L1228  T=1 F=0  T=24 F=0  (p[0] == '/') &&
  d=1   L1229  T=1 F=0  T=16 F=8  (((p[1] >= 'a') && (p[1] <= 'z')) ||
  d=1   L1229  T=1 F=0  T=16 F=0  (((p[1] >= 'a') && (p[1] <= 'z')) ||
  d=1   L1230  T=0 F=0  T=1 F=7  ((p[1] >= 'A') && (p[1] <= 'Z'))) &&
  d=1   L1230  T=0 F=0  T=0 F=1  ((p[1] >= 'A') && (p[1] <= 'Z'))) &&
  d=1   L1231  T=0 F=1  T=0 F=16  (p[2] == ':') &&
  d=1   L1242  T=112 F=4  T=5480 F=96  while (*p != 0) {
  d=1   L1243  T=0 F=112  T=50 F=5430  if (len + 3 >= max) {
  d=1   L1245  T=0 F=0  T=0 F=50  if (temp == NULL) goto mem_error;
  d=1   L1248  T=12 F=9  T=285 F=1100  if ((IS_UNRESERVED(*(p))) || ((*(p) == '/')) ||
  d=1   L1249  T=0 F=9  T=10 F=1070  ((*(p) == ';')) || ((*(p) == '@')) || ((*(p) == '&')) ||
  d=1   L1249  T=0 F=9  T=13 F=1080  ((*(p) == ';')) || ((*(p) == '@')) || ((*(p) == '&')) ||
  d=1   L1249  T=0 F=9  T=5 F=1090  ((*(p) == ';')) || ((*(p) == '@')) || ((*(p) == '&')) ||
  d=1   L1250  T=0 F=9  T=6 F=1050  ((*(p) == '=')) || ((*(p) == '+')) || ((*(p) == '$')) ||
  d=1   L1250  T=0 F=9  T=5 F=1060  ((*(p) == '=')) || ((*(p) == '+')) || ((*(p) == '$')) ||
  d=1   L1250  T=0 F=9  T=6 F=1060  ((*(p) == '=')) || ((*(p) == '+')) || ((*(p) == '$')) ||
  d=1   L1251  T=0 F=9  T=9 F=1040  ((*(p) == ',')))
  d=1   L1257  T=0 F=9  T=85 F=963  ret[len++] = hi + (hi > 9? 'A'-10 : '0');
  d=1   L1258  T=6 F=3  T=144 F=904  ret[len++] = lo + (lo > 9? 'A'-10 : '0');
  d=1   L1262  T=0 F=4  T=3 F=93  if (uri->query_raw != NULL) {
  d=1   L1263  T=0 F=0  T=0 F=3  if (len + 1 >= max) {
  d=1   L1270  T=0 F=0  T=30 F=3  while (*p != 0) {
  d=1   L1271  T=0 F=0  T=0 F=30  if (len + 1 >= max) {
  d=1   L1278  T=0 F=4  T=0 F=93  } else if (uri->query != NULL) {
  d=1   L1304  T=0 F=4  T=0 F=96  if (uri->fragment != NULL) {
  d=1   L1329  T=0 F=4  T=0 F=96  if (len >= max) {

[off-chain: 193 additional divergent branches across 26 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=2f02ccc3aa4fe4a5, size=394 bytes, fuzzer=grimoire, trial=3, discovered_at=16226s, mutation_op=BytesCopyMutator,ByteRandMutator):
  0000: 27 68 74 74 70 3a 2f 2f 33 2e 6f 72 67 3a 31 39   'http://3.org:19
  0010: 39 39 2f 6e 27 68 74 74 70 3a 2f 2f 33 2e 6f 72   99/n'http://3.or
  0020: 67 3a 31 39 39 39 2f 6e 6b 0d 0d 0d 6c 5c 0a 3c   g:1999/nk...l\.<
  0030: 3f 6c 20 3f 3e 3c 21 44 4f 43 54 59 50 45 61 20   ?l ?><!DOCTYPEa 

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=25e2315f41fc56db, size=361 bytes, fuzzer=cmplog, trial=1, discovered_at=6740s, mutation_op=ByteFlipMutator,BytesSetMutator):
  0000: 27 68 74 74 70 3a 2f 2f 77 77 77 d1 6b 20 20 43   'http://www.k  C
  0010: 44 41 54 41 20 20 20 20 20 06 00 00 00 31 32 37   DATA     ....127
  0020: 37 37 32 2e 88 6d 00 5c 0a 3c 3f 78 6b 20 20 43   772..m.\.<?xk  C
  0030: 44 41 54 41 20 20 20 20 20 2e 30 22 3f 3e 0a 3c   DATA     .0"?>.<
Seed 2 (id=08ccf3bb0da3cc28, size=485 bytes, fuzzer=cmplog, trial=2, discovered_at=6742s, mutation_op=BytesDeleteMutator,BytesSwapMutator,BytesInsertMutator,BytesExpandMutator,BytesRandSetMutator,BytesDeleteMutator,ByteInterestingMutator):
  0000: 27 68 74 74 70 3a 2f 2f 77 77 77 2e 77 33 2e 6f   'http://www.w3.o
  0010: 72 67 2f 5c 39 39 39 2f 78 6c 69 6e 6b 27 0a 20   rg/\999/xlink'. 
  0020: 20 20 20 20 20 20 20 20 20 20 20 78 6c 69 6e 6b              xlink
  0030: 3a 74 79 70 65 21 ff ff ff 73 69 6d 70 6c 65 29   :type!...simple)
Seed 3 (id=0c8a6a6705e242e6, size=248 bytes, fuzzer=cmplog, trial=1, discovered_at=6795s, mutation_op=CrossoverReplaceMutator,ByteDecMutator):
  0000: 27 0a 74 74 70 3a 2f 2f 77 77 77 0a 77 33 27 01   '.ttp://www.w3'.
  0010: 72 67 2f 31 39 39 39 2f 78 23 69 6e 6b 27 2e 20   rg/1999/x#ink'. 
  0020: 3b 20 20 20 20 20 20 20 7f 29 20 78 6c 69 6e 06   ;       .) xlin.
  0030: 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c   ...127772.xml\.<
Seed 4 (id=22aec5210a967574, size=380 bytes, fuzzer=cmplog, trial=1, discovered_at=6801s, mutation_op=BytesDeleteMutator,TokenReplace,ByteDecMutator):
  0000: 45 44 20 27 68 74 74 70 3a 2f 2f 77 77 77 0a 77   ED 'http://www.w
  0010: 33 2e 6f 72 67 2f 31 39 39 39 2f 78 3a 69 6e 6b   3.org/1999/x:ink
  0020: 27 0a 20 20 20 20 20 20 20 20 20 06 3c 21 44 4f   '.         .<!DO
  0030: 43 54 59 50 45 20 61 20 00 00 00 31 32 37 37 37   CTYPE a ...12777
Seed 5 (id=0442ffb6a2e3350c, size=758 bytes, fuzzer=cmplog, trial=2, discovered_at=7540s, mutation_op=BytesDeleteMutator,ByteInterestingMutator,TokenReplace,BytesCopyMutator,CrossoverInsertMutator,ByteInterestingMutator,TokenReplace):
  0000: 3d 22 68 74 74 70 3a 2f 2f 66 61 6b 65 75 72 6c   ="http://fakeurl
  0010: 21 6e 65 74 29 3e 62 20 74 65 78 5c 0a 3c 3f 78   !net)>b tex\.<?x
  0020: 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22   ml version="1.0"
  0030: 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53   ?>.<!DOCTYPE a S


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  27(')x1                             27(')x7 45(E)x4 3d(=)x4 66(f)x4 +3u  PARTIAL
   0x0001  68(h)x1                             68(h)x6 44(D)x4 22(")x4 66(f)x4 +3u  PARTIAL
   0x0002  74(t)x1                             74(t)x7 68(h)x4 3d(=)x4 22(")x4 +3u  PARTIAL
   0x0003  74(t)x1                             74(t)x11 22(")x5 27(')x4 68(h)x4    PARTIAL
   0x0004  70(p)x1                             68(h)x8 74(t)x8 70(p)x7 67(g)x1     PARTIAL
   0x0005  3a(:)x1                             74(t)x13 3a(:)x7 70(p)x4            PARTIAL
   0x0006  2f(/)x1                             74(t)x9 2f(/)x7 3a(:)x4 70(p)x4     PARTIAL
   0x0007  2f(/)x1                             2f(/)x11 70(p)x9 3a(:)x4            PARTIAL
   0x0008  33(3)x1                             3a(:)x9 2f(/)x8 77(w)x5 8a(.)x1 +1u  DIFFER
   0x0009  2e(.)x1                             2f(/)x13 77(w)x6 66(f)x4 2d(-)x1    DIFFER
   0x000a  6f(o)x1                             2f(/)x9 77(w)x6 61(a)x4 66(f)x3 +2u  DIFFER
   0x000b  72(r)x1                             66(f)x5 6b(k)x4 61(a)x4 77(w)x3 +7u  DIFFER
   0x000c  67(g)x1                             77(w)x7 61(a)x5 6b(k)x4 65(e)x4 +4u  DIFFER
   0x000d  3a(:)x1                             33(3)x4 6b(k)x4 77(w)x3 75(u)x3 +7u  DIFFER
   0x000e  31(1)x1                             65(e)x6 2e(.)x3 72(r)x3 75(u)x3 +8u  DIFFER
   0x000f  39(9)x1                             75(u)x5 6f(o)x3 77(w)x3 6c(l)x3 +8u  DIFFER
   0x0010  39(9)x1                             72(r)x7 33(3)x3 2e(.)x2 44(D)x1 +11u  DIFFER
   0x0011  39(9)x1                             67(g)x4 2e(.)x3 6e(n)x3 6c(l)x3 +11u  DIFFER
   0x0012  2f(/)x1                             2f(/)x4 6f(o)x4 65(e)x3 2e(.)x3 +9u  PARTIAL
   0x0013  6e(n)x1                             6e(n)x4 72(r)x3 20( )x3 31(1)x2 +10u  PARTIAL
   0x0014  27(')x1                             20( )x4 39(9)x3 65(e)x3 67(g)x2 +11u  PARTIAL
   0x0015  68(h)x1                             20( )x4 39(9)x3 2f(/)x3 74(t)x3 +10u  DIFFER
   0x0016  74(t)x1                             20( )x4 39(9)x3 31(1)x3 62(b)x3 +8u  DIFFER
   0x0017  74(t)x1                             2f(/)x4 3e(>)x4 20( )x3 39(9)x2 +11u  DIFFER
   0x0018  70(p)x1                             62(b)x4 78(x)x3 39(9)x2 74(t)x2 +12u  DIFFER
   0x0019  3a(:)x1                             20( )x3 6c(l)x2 65(e)x2 06(.)x1 +16u  DIFFER
   0x001a  2f(/)x1                             69(i)x3 2f(/)x3 74(t)x3 00(.)x1 +14u  PARTIAL
   0x001b  2f(/)x1                             65(e)x5 6e(n)x4 78(x)x2 00(.)x1 +12u  PARTIAL
   0x001c  33(3)x1                             6b(k)x4 0a(.)x2 20( )x2 74(t)x2 +13u  DIFFER
   0x001d  2e(.)x1                             27(')x4 31(1)x2 3c(<)x2 74(t)x2 +13u  DIFFER
   0x001e  6f(o)x1                             2f(/)x4 0a(.)x3 21(!)x2 ff(.)x2 +13u  DIFFER
   0x001f  72(r)x1                             20( )x3 78(x)x2 0a(.)x2 7e(~)x2 +15u  DIFFER
   0x0020  67(g)x1                             27(')x3 20( )x2 37(7)x1 3b(;)x1 +17u  DIFFER
   0x0021  3a(:)x1                             2f(/)x4 20( )x3 0a(.)x2 37(7)x1 +14u  PARTIAL
   0x0022  31(1)x1                             20( )x7 7e(~)x2 32(2)x1 ab(.)x1 +13u  DIFFER
   0x0023  39(9)x1                             20( )x5 2f(/)x2 2e(.)x1 76(v)x1 +15u  DIFFER
   0x0024  39(9)x1                             20( )x5 65(e)x2 3e(>)x2 88(.)x1 +14u  PARTIAL
   0x0025  39(9)x1                             20( )x6 0a(.)x2 28(()x2 2f(/)x2 +11u  PARTIAL
   0x0026  2f(/)x1                             20( )x6 3c(<)x2 7e(~)x2 00(.)x1 +13u  DIFFER
   0x0027  6e(n)x1                             20( )x6 21(!)x2 5c(\)x1 69(i)x1 +14u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6985.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6985,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6985 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6985 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6985 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).