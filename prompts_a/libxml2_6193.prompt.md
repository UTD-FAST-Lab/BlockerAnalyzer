==== BLOCKER ====
Target: libxml2
Branch ID: 6193
Location: /src/libxml2/SAX2.c:1171:49
Enclosing function: SAX2.c:xmlSAX2AttributeInternal
Source line:         (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        2          6  REFERENCE
cmplog                           6        0          4  REFERENCE
value_profile                    1        8          1  loser (I2S vs value_profile_cmplog)
value_profile_cmplog             8        2          0  winner (I2S vs value_profile)
naive_ctx                        4        4          2  REFERENCE
naive_ngram4                     2        0          8  REFERENCE
mopt                             1        0          9  REFERENCE
minimizer                        5        2          3  REFERENCE
fast                             2        2          6  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=1/10  blocked=8  unreached=1
  avg duration blocked: winner=7.00h  loser=10.11h
  avg hitcount on branch: winner=7  loser=1
  prob_div=0.69  dur_div=3.11h  hit_div=7
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6193/{W,L}/branch_coverage_show.txt

--- Enclosing function: SAX2.c:xmlSAX2AttributeInternal (/src/libxml2/SAX2.c:1097-1438) ---
[ ]  1095  xmlSAX2AttributeInternal(void *ctx, const xmlChar *fullname,
[ ]  1096               const xmlChar *value, const xmlChar *prefix ATTRIBUTE_UNUSED)
[B]  1097  {
[B]  1098      xmlParserCtxtPtr ctxt = (xmlParserCtxtPtr) ctx;
[B]  1099      xmlAttrPtr ret;
[B]  1100      xmlChar *name;
[B]  1101      xmlChar *ns;
[B]  1102      xmlChar *nval;
[B]  1103      xmlNsPtr namespace;
[ ]  1104  
[B]  1105      if (ctxt->html) {
[ ]  1106  	name = xmlStrdup(fullname);
[ ]  1107  	ns = NULL;
[ ]  1108  	namespace = NULL;
[B]  1109      } else {
[ ]  1110  	/*
[ ]  1111  	 * Split the full name into a namespace prefix and the tag name
[ ]  1112  	 */
[B]  1113  	name = xmlSplitQName(ctxt, fullname, &ns);
[B]  1114  	if ((name != NULL) && (name[0] == 0)) {
[ ]  1115  	    if (xmlStrEqual(ns, BAD_CAST "xmlns")) {
[ ]  1116  		xmlNsErrMsg(ctxt, XML_ERR_NS_DECL_ERROR,
[ ]  1117  			    "invalid namespace declaration '%s'\n",
[ ]  1118  			    fullname, NULL);
[ ]  1119  	    } else {
[ ]  1120  		xmlNsWarnMsg(ctxt, XML_WAR_NS_COLUMN,
[ ]  1121  			     "Avoid attribute ending with ':' like '%s'\n",
[ ]  1122  			     fullname, NULL);
[ ]  1123  	    }
[ ]  1124  	    if (ns != NULL)
[ ]  1125  		xmlFree(ns);
[ ]  1126  	    ns = NULL;
[ ]  1127  	    xmlFree(name);
[ ]  1128  	    name = xmlStrdup(fullname);
[ ]  1129  	}
[B]  1130      }
[B]  1131      if (name == NULL) {
[ ]  1132          xmlSAX2ErrMemory(ctxt, "xmlSAX2StartElement");
[ ]  1133  	if (ns != NULL)
[ ]  1134  	    xmlFree(ns);
[ ]  1135  	return;
[ ]  1136      }
[ ]  1137  
[B]  1138  #ifdef LIBXML_HTML_ENABLED
[B]  1139      if ((ctxt->html) &&
[B]  1140          (value == NULL) && (htmlIsBooleanAttr(fullname))) {
[ ]  1141              nval = xmlStrdup(fullname);
[ ]  1142              value = (const xmlChar *) nval;
[ ]  1143      } else
[B]  1144  #endif
[B]  1145      {
[B]  1146  #ifdef LIBXML_VALID_ENABLED
[ ]  1147          /*
[ ]  1148           * Do the last stage of the attribute normalization
[ ]  1149           * Needed for HTML too:
[ ]  1150           *   http://www.w3.org/TR/html4/types.html#h-6.2
[ ]  1151           */
[B]  1152          ctxt->vctxt.valid = 1;
[B]  1153          nval = xmlValidCtxtNormalizeAttributeValue(&ctxt->vctxt,
[B]  1154                                                 ctxt->myDoc, ctxt->node,
[B]  1155                                                 fullname, value);
[B]  1156          if (ctxt->vctxt.valid != 1) {
[ ]  1157              ctxt->valid = 0;
[ ]  1158          }
[B]  1159          if (nval != NULL)
[W]  1160              value = nval;
[ ]  1161  #else
[ ]  1162          nval = NULL;
[ ]  1163  #endif /* LIBXML_VALID_ENABLED */
[B]  1164      }
[ ]  1165  
[ ]  1166      /*
[ ]  1167       * Check whether it's a namespace definition
[ ]  1168       */
[B]  1169      if ((!ctxt->html) && (ns == NULL) &&
[B]  1170          (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
[B]  1171          (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) { <-- BLOCKER
[L]  1172  	xmlNsPtr nsret;
[L]  1173  	xmlChar *val;
[ ]  1174  
[ ]  1175          /* Avoid unused variable warning if features are disabled. */
[L]  1176          (void) nsret;
[ ]  1177  
[L]  1178          if (!ctxt->replaceEntities) {
[L]  1179  	    ctxt->depth++;
[L]  1180  	    val = xmlStringDecodeEntities(ctxt, value, XML_SUBSTITUTE_REF,
[L]  1181  		                          0,0,0);
[L]  1182  	    ctxt->depth--;
[L]  1183  	    if (val == NULL) {
[ ]  1184  	        xmlSAX2ErrMemory(ctxt, "xmlSAX2StartElement");
[ ]  1185  		if (name != NULL)
[ ]  1186  		    xmlFree(name);
[ ]  1187                  if (nval != NULL)
[ ]  1188                      xmlFree(nval);
[ ]  1189  		return;
[ ]  1190  	    }
[L]  1191  	} else {
[L]  1192  	    val = (xmlChar *) value;
[L]  1193  	}
[ ]  1194  
[L]  1195  	if (val[0] != 0) {
[L]  1196  	    xmlURIPtr uri;
[ ]  1197  
[L]  1198  	    uri = xmlParseURI((const char *)val);
[L]  1199  	    if (uri == NULL) {
[L]  1200  		if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
[L]  1201  		    ctxt->sax->warning(ctxt->userData,
[L]  1202  			 "xmlns: %s not a valid URI\n", val);
[L]  1203  	    } else {
[ ]  1204  		if (uri->scheme == NULL) {
[ ]  1205  		    if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
[ ]  1206  			ctxt->sax->warning(ctxt->userData,
[ ]  1207  			     "xmlns: URI %s is not absolute\n", val);
[ ]  1208  		}
[ ]  1209  		xmlFreeURI(uri);
[ ]  1210  	    }
[L]  1211  	}
[ ]  1212  
[ ]  1213  	/* a default namespace definition */
[L]  1214  	nsret = xmlNewNs(ctxt->node, val, NULL);
[ ]  1215  
[L]  1216  #ifdef LIBXML_VALID_ENABLED
[ ]  1217  	/*
[ ]  1218  	 * Validate also for namespace decls, they are attributes from
[ ]  1219  	 * an XML-1.0 perspective
[ ]  1220  	 */
[L]  1221          if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
[L]  1222  	    ctxt->myDoc && ctxt->myDoc->intSubset)
[ ]  1223  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc,
[ ]  1224  					   ctxt->node, prefix, nsret, val);
[L]  1225  #endif /* LIBXML_VALID_ENABLED */
[L]  1226  	if (name != NULL)
[L]  1227  	    xmlFree(name);
[L]  1228  	if (nval != NULL)
[ ]  1229  	    xmlFree(nval);
[L]  1230  	if (val != value)
[L]  1231  	    xmlFree(val);
[L]  1232  	return;
[L]  1233      }
[B]  1234      if ((!ctxt->html) &&
[B]  1235  	(ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2] == 'l') &&
[B]  1236          (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
[ ]  1237  	xmlNsPtr nsret;
[ ]  1238  	xmlChar *val;
[ ]  1239  
[ ]  1240          /* Avoid unused variable warning if features are disabled. */
[ ]  1241          (void) nsret;
[ ]  1242  
[ ]  1243          if (!ctxt->replaceEntities) {
[ ]  1244  	    ctxt->depth++;
[ ]  1245  	    val = xmlStringDecodeEntities(ctxt, value, XML_SUBSTITUTE_REF,
[ ]  1246  		                          0,0,0);
[ ]  1247  	    ctxt->depth--;
[ ]  1248  	    if (val == NULL) {
[ ]  1249  	        xmlSAX2ErrMemory(ctxt, "xmlSAX2StartElement");
[ ]  1250  	        xmlFree(ns);
[ ]  1251  		if (name != NULL)
[ ]  1252  		    xmlFree(name);
[ ]  1253                  if (nval != NULL)
[ ]  1254                      xmlFree(nval);
[ ]  1255  		return;
[ ]  1256  	    }
[ ]  1257  	} else {
[ ]  1258  	    val = (xmlChar *) value;
[ ]  1259  	}
[ ]  1260  
[ ]  1261  	if (val[0] == 0) {
[ ]  1262  	    xmlNsErrMsg(ctxt, XML_NS_ERR_EMPTY,
[ ]  1263  		        "Empty namespace name for prefix %s\n", name, NULL);
[ ]  1264  	}
[ ]  1265  	if ((ctxt->pedantic != 0) && (val[0] != 0)) {
[ ]  1266  	    xmlURIPtr uri;
[ ]  1267  
[ ]  1268  	    uri = xmlParseURI((const char *)val);
[ ]  1269  	    if (uri == NULL) {
[ ]  1270  	        xmlNsWarnMsg(ctxt, XML_WAR_NS_URI,
[ ]  1271  			 "xmlns:%s: %s not a valid URI\n", name, value);
[ ]  1272  	    } else {
[ ]  1273  		if (uri->scheme == NULL) {
[ ]  1274  		    xmlNsWarnMsg(ctxt, XML_WAR_NS_URI_RELATIVE,
[ ]  1275  			   "xmlns:%s: URI %s is not absolute\n", name, value);
[ ]  1276  		}
[ ]  1277  		xmlFreeURI(uri);
[ ]  1278  	    }
[ ]  1279  	}
[ ]  1280  
[ ]  1281  	/* a standard namespace definition */
[ ]  1282  	nsret = xmlNewNs(ctxt->node, val, name);
[ ]  1283  	xmlFree(ns);
[ ]  1284  #ifdef LIBXML_VALID_ENABLED
[ ]  1285  	/*
[ ]  1286  	 * Validate also for namespace decls, they are attributes from
[ ]  1287  	 * an XML-1.0 perspective
[ ]  1288  	 */
[ ]  1289          if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
[ ]  1290  	    ctxt->myDoc && ctxt->myDoc->intSubset)
[ ]  1291  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc,
[ ]  1292  					   ctxt->node, prefix, nsret, value);
[ ]  1293  #endif /* LIBXML_VALID_ENABLED */
[ ]  1294  	if (name != NULL)
[ ]  1295  	    xmlFree(name);
[ ]  1296  	if (nval != NULL)
[ ]  1297  	    xmlFree(nval);
[ ]  1298  	if (val != value)
[ ]  1299  	    xmlFree(val);
[ ]  1300  	return;
[ ]  1301      }
[ ]  1302  
[B]  1303      if (ns != NULL) {
[B]  1304  	namespace = xmlSearchNs(ctxt->myDoc, ctxt->node, ns);
[ ]  1305  
[B]  1306  	if (namespace == NULL) {
[B]  1307  	    xmlNsErrMsg(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[B]  1308  		    "Namespace prefix %s of attribute %s is not defined\n",
[B]  1309  		             ns, name);
[B]  1310  	} else {
[ ]  1311              xmlAttrPtr prop;
[ ]  1312  
[ ]  1313              prop = ctxt->node->properties;
[ ]  1314              while (prop != NULL) {
[ ]  1315                  if (prop->ns != NULL) {
[ ]  1316                      if ((xmlStrEqual(name, prop->name)) &&
[ ]  1317                          ((namespace == prop->ns) ||
[ ]  1318                           (xmlStrEqual(namespace->href, prop->ns->href)))) {
[ ]  1319                              xmlNsErrMsg(ctxt, XML_ERR_ATTRIBUTE_REDEFINED,
[ ]  1320                                      "Attribute %s in %s redefined\n",
[ ]  1321                                               name, namespace->href);
[ ]  1322                          ctxt->wellFormed = 0;
[ ]  1323                          if (ctxt->recovery == 0) ctxt->disableSAX = 1;
[ ]  1324                          if (name != NULL)
[ ]  1325                              xmlFree(name);
[ ]  1326                          goto error;
[ ]  1327                      }
[ ]  1328                  }
[ ]  1329                  prop = prop->next;
[ ]  1330              }
[ ]  1331          }
[B]  1332      } else {
[W]  1333  	namespace = NULL;
[W]  1334      }
[ ]  1335  
[ ]  1336      /* !!!!!! <a toto:arg="" xmlns:toto="http://toto.com"> */
[B]  1337      ret = xmlNewNsPropEatName(ctxt->node, namespace, name, NULL);
[B]  1338      if (ret == NULL)
[ ]  1339          goto error;
[ ]  1340  
[B]  1341      if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
[L]  1342          xmlNodePtr tmp;
[ ]  1343  
[L]  1344          ret->children = xmlStringGetNodeList(ctxt->myDoc, value);
[L]  1345          tmp = ret->children;
[L]  1346          while (tmp != NULL) {
[L]  1347              tmp->parent = (xmlNodePtr) ret;
[L]  1348              if (tmp->next == NULL)
[L]  1349                  ret->last = tmp;
[L]  1350              tmp = tmp->next;
[L]  1351          }
[B]  1352      } else if (value != NULL) {
[W]  1353          ret->children = xmlNewDocText(ctxt->myDoc, value);
[W]  1354          ret->last = ret->children;
[W]  1355          if (ret->children != NULL)
[W]  1356              ret->children->parent = (xmlNodePtr) ret;
[W]  1357      }
[ ]  1358  
[B]  1359  #ifdef LIBXML_VALID_ENABLED
[B]  1360      if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
[B]  1361          ctxt->myDoc && ctxt->myDoc->intSubset) {
[ ]  1362  
[ ]  1363  	/*
[ ]  1364  	 * If we don't substitute entities, the validation should be
[ ]  1365  	 * done on a value with replaced entities anyway.
[ ]  1366  	 */
[ ]  1367          if (!ctxt->replaceEntities) {
[ ]  1368  	    xmlChar *val;
[ ]  1369  
[ ]  1370  	    ctxt->depth++;
[ ]  1371  	    val = xmlStringDecodeEntities(ctxt, value, XML_SUBSTITUTE_REF,
[ ]  1372  		                          0,0,0);
[ ]  1373  	    ctxt->depth--;
[ ]  1374  
[ ]  1375  	    if (val == NULL)
[ ]  1376  		ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt,
[ ]  1377  				ctxt->myDoc, ctxt->node, ret, value);
[ ]  1378  	    else {
[ ]  1379  		xmlChar *nvalnorm;
[ ]  1380  
[ ]  1381  		/*
[ ]  1382  		 * Do the last stage of the attribute normalization
[ ]  1383  		 * It need to be done twice ... it's an extra burden related
[ ]  1384  		 * to the ability to keep xmlSAX2References in attributes
[ ]  1385  		 */
[ ]  1386  		nvalnorm = xmlValidNormalizeAttributeValue(ctxt->myDoc,
[ ]  1387  					    ctxt->node, fullname, val);
[ ]  1388  		if (nvalnorm != NULL) {
[ ]  1389  		    xmlFree(val);
[ ]  1390  		    val = nvalnorm;
[ ]  1391  		}
[ ]  1392  
[ ]  1393  		ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt,
[ ]  1394  			        ctxt->myDoc, ctxt->node, ret, val);
[ ]  1395                  xmlFree(val);
[ ]  1396  	    }
[ ]  1397  	} else {
[ ]  1398  	    ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt, ctxt->myDoc,
[ ]  1399  					       ctxt->node, ret, value);
[ ]  1400  	}
[ ]  1401      } else
[B]  1402  #endif /* LIBXML_VALID_ENABLED */
[B]  1403             if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
[B]  1404  	       (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
[B]  1405  	        ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
[ ]  1406                 /* Don't create IDs containing entity references */
[B]  1407                 (ret->children != NULL) &&
[B]  1408                 (ret->children->type == XML_TEXT_NODE) &&
[B]  1409                 (ret->children->next == NULL)) {
[B]  1410          xmlChar *content = ret->children->content;
[ ]  1411          /*
[ ]  1412  	 * when validating, the ID registration is done at the attribute
[ ]  1413  	 * validation level. Otherwise we have to do specific handling here.
[ ]  1414  	 */
[B]  1415  	if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
[ ]  1416  	    /*
[ ]  1417  	     * Add the xml:id value
[ ]  1418  	     *
[ ]  1419  	     * Open issue: normalization of the value.
[ ]  1420  	     */
[ ]  1421  	    if (xmlValidateNCName(content, 1) != 0) {
[ ]  1422  	        xmlErrValid(ctxt, XML_DTD_XMLID_VALUE,
[ ]  1423  		      "xml:id : attribute value %s is not an NCName\n",
[ ]  1424  			    (const char *) content, NULL);
[ ]  1425  	    }
[ ]  1426  	    xmlAddID(&ctxt->vctxt, ctxt->myDoc, content, ret);
[B]  1427  	} else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
[ ]  1428  	    xmlAddID(&ctxt->vctxt, ctxt->myDoc, content, ret);
[B]  1429  	else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
[ ]  1430  	    xmlAddRef(&ctxt->vctxt, ctxt->myDoc, content, ret);
[B]  1431      }
[ ]  1432  
[B]  1433  error:
[B]  1434      if (nval != NULL)
[W]  1435  	xmlFree(nval);
[B]  1436      if (ns != NULL)
[B]  1437  	xmlFree(ns);
[B]  1438  }

--- Caller (1 hop): SAX2.c:xmlCheckDefaultedAttributes (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574) (±10 around call site) ---
[ ]  1564  			    i = 0;
[ ]  1565  			    att = atts[i];
[ ]  1566  			    while (att != NULL) {
[ ]  1567  				if (xmlStrEqual(att, fulln))
[ ]  1568  				    break;
[ ]  1569  				i += 2;
[ ]  1570  				att = atts[i];
[ ]  1571  			    }
[ ]  1572  			}
[W]  1573  			if (att == NULL) {
[W]  1574  			    xmlSAX2AttributeInternal(ctxt, fulln, <-- CALL
[W]  1575  						 attr->defaultValue, prefix);
[W]  1576  			}
[W]  1577  			if ((fulln != fn) && (fulln != attr->name))
[ ]  1578  			    xmlFree(fulln);
[W]  1579  		    }
[W]  1580  		}
[W]  1581  	    }
[W]  1582  	    attr = attr->nexth;
[W]  1583  	}
[W]  1584  	if (internal == 1) {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 2  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      12       260  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806)
       6       192  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
       6       192  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
       4       103  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
       6        52  xmlSAX2IgnorableWhitespace  (/src/libxml2/SAX2.c:2698-2704)
       8        48  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
       6        36  xmlSAX2SetDocumentLocator  (/src/libxml2/SAX2.c:942-948)
       6        36  xmlSAX2StartDocument  (/src/libxml2/SAX2.c:958-1013)
      12        39  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438)  <-- enclosing
       4        29  xmlSAX2EndDocument  (/src/libxml2/SAX2.c:1023-1054)
      12         0  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758)
      12         0  xmlSAX2ElementDecl  (/src/libxml2/SAX2.c:772-807)
      12         0  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591)
       0         9  SAX2.c:xmlErrValid  (/src/libxml2/SAX2.c:99-124)
       6         0  xmlSAX2InternalSubset  (/src/libxml2/SAX2.c:330-354)
... (3 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591) ---
  d=2   L1454  T=12 F=0  T=0 F=0  if (elemDecl == NULL) {
  d=2   L1461  T=12 F=0  T=0 F=0  if (elemDecl != NULL) {
  d=2   L1467  T=0 F=12  T=0 F=0  if ((ctxt->myDoc->standalone == 1) &&
  d=2   L1523  T=12 F=12  T=0 F=0  while (attr != NULL) {
  d=2   L1529  T=12 F=0  T=0 F=0  if (attr->defaultValue != NULL) {
  d=2   L1538  T=6 F=6  T=0 F=0  if (((attr->prefix != NULL) &&
  d=2   L1539  T=0 F=6  T=0 F=0  (xmlStrEqual(attr->prefix, BAD_CAST "xmlns"))) ||
  d=2   L1540  T=6 F=6  T=0 F=0  ((attr->prefix == NULL) &&
  d=2   L1541  T=0 F=6  T=0 F=0  (xmlStrEqual(attr->name, BAD_CAST "xmlns"))) ||
  d=2   L1542  T=12 F=0  T=0 F=0  (ctxt->loadsubset & XML_COMPLETE_ATTRS)) {
  d=2   L1548  T=0 F=12  T=0 F=0  if ((tst == attr) || (tst == NULL)) {
  d=2   L1548  T=12 F=0  T=0 F=0  if ((tst == attr) || (tst == NULL)) {
  d=2   L1553  T=0 F=12  T=0 F=0  if (fulln == NULL) {
  d=2   L1563  T=0 F=12  T=0 F=0  if (atts != NULL) {
  d=2   L1573  T=12 F=0  T=0 F=0  if (att == NULL) {
  d=2   L1577  T=6 F=6  T=0 F=0  if ((fulln != fn) && (fulln != attr->name))
  d=2   L1577  T=0 F=6  T=0 F=0  if ((fulln != fn) && (fulln != attr->name))
  d=2   L1584  T=0 F=12  T=0 F=0  if (internal == 1) {
--- d=2  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806) ---
  d=2   L1614  T=0 F=12  T=0 F=260  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=2   L1614  T=0 F=12  T=0 F=260  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=2   L1614  T=0 F=12  T=0 F=260  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=2   L1624  T=0 F=12  T=9 F=251  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=2   L1624  T=0 F=0  T=9 F=0  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=2   L1625  T=0 F=0  T=9 F=0  ((ctxt->myDoc->intSubset == NULL) ||
  d=2   L1648  T=0 F=12  T=0 F=260  if (ret == NULL) {
  d=2   L1654  T=0 F=12  T=36 F=224  if (ctxt->myDoc->children == NULL) {
  d=2   L1659  T=6 F=6  T=41 F=183  } else if (parent == NULL) {
  d=2   L1663  T=12 F=0  T=260 F=0  if (ctxt->linenumbers) {
  d=2   L1664  T=12 F=0  T=260 F=0  if (ctxt->input != NULL) {
  d=2   L1665  T=12 F=0  T=260 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=2   L1678  T=0 F=12  T=0 F=260  if (nodePush(ctxt, ret) < 0) {
  d=2   L1689  T=12 F=0  T=224 F=36  if (parent != NULL) {
  d=2   L1690  T=6 F=6  T=224 F=0  if (parent->type == XML_ELEMENT_NODE) {
  d=2   L1706  T=12 F=0  T=260 F=0  if (!ctxt->html) {
  d=2   L1711  T=12 F=0  T=0 F=260  if ((ctxt->myDoc->intSubset != NULL) ||
  d=2   L1712  T=0 F=0  T=0 F=260  (ctxt->myDoc->extSubset != NULL)) {
  d=2   L1719  T=0 F=12  T=36 F=224  if (atts != NULL) {
  d=2   L1723  T=0 F=0  T=39 F=0  while ((att != NULL) && (value != NULL)) {
  d=2   L1723  T=0 F=0  T=39 F=36  while ((att != NULL) && (value != NULL)) {
  d=2   L1724  T=0 F=0  T=36 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1724  T=0 F=0  T=36 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1724  T=0 F=0  T=36 F=3  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1725  T=0 F=0  T=36 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=2   L1725  T=0 F=0  T=36 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=2   L1738  T=12 F=0  T=0 F=0  if ((ns == NULL) && (parent != NULL))
  d=2   L1738  T=12 F=0  T=0 F=260  if ((ns == NULL) && (parent != NULL))
  d=2   L1740  T=0 F=12  T=0 F=260  if ((prefix != NULL) && (ns == NULL)) {
  d=2   L1751  T=0 F=12  T=260 F=0  if ((ns != NULL) && (ns->href != NULL) &&
  d=2   L1751  T=0 F=0  T=260 F=0  if ((ns != NULL) && (ns->href != NULL) &&
  d=2   L1752  T=0 F=0  T=228 F=32  ((ns->href[0] != 0) || (ns->prefix != NULL)))
  d=2   L1752  T=0 F=0  T=0 F=32  ((ns->href[0] != 0) || (ns->prefix != NULL)))
  d=2   L1759  T=0 F=12  T=36 F=224  if (atts != NULL) {
  d=2   L1763  T=0 F=0  T=0 F=36  if (ctxt->html) {
  d=2   L1770  T=0 F=0  T=39 F=36  while ((att != NULL) && (value != NULL)) {
  d=2   L1770  T=0 F=0  T=39 F=0  while ((att != NULL) && (value != NULL)) {
  d=2   L1771  T=0 F=0  T=0 F=36  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1771  T=0 F=0  T=0 F=36  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1771  T=0 F=0  T=3 F=36  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1772  T=0 F=0  T=0 F=36  (att[3] != 'n') || (att[4] != 's'))
  d=2   L1772  T=0 F=0  T=0 F=36  (att[3] != 'n') || (att[4] != 's'))
  d=2   L1789  T=0 F=12  T=0 F=260  if ((ctxt->validate) &&
  d=2   L1803  T=0 F=12  T=0 F=260  if (prefix != NULL)
--- d=1  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=1   L1105  T=0 F=12  T=0 F=39  if (ctxt->html) {
  d=1   L1114  T=12 F=0  T=39 F=0  if ((name != NULL) && (name[0] == 0)) {
  d=1   L1114  T=0 F=12  T=0 F=39  if ((name != NULL) && (name[0] == 0)) {
  d=1   L1131  T=0 F=12  T=0 F=39  if (name == NULL) {
  d=1   L1139  T=0 F=12  T=0 F=39  if ((ctxt->html) &&
  d=1   L1156  T=0 F=12  T=0 F=39  if (ctxt->vctxt.valid != 1) {
  d=1   L1159  T=6 F=6  T=0 F=39  if (nval != NULL)
  d=1   L1169  T=6 F=6  T=36 F=3  if ((!ctxt->html) && (ns == NULL) &&
  d=1   L1169  T=12 F=0  T=39 F=0  if ((!ctxt->html) && (ns == NULL) &&
  d=1   L1170  T=6 F=0  T=36 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=1   L1170  T=6 F=0  T=36 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=1   L1170  T=6 F=0  T=36 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=1   L1171  T=6 F=0  T=36 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {  <-- BLOCKER
  d=1   L1171  T=6 F=0  T=36 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {  <-- BLOCKER
  d=1   L1171  T=0 F=6  T=36 F=0  (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {  <-- BLOCKER
  d=1   L1178  T=0 F=0  T=12 F=24  if (!ctxt->replaceEntities) {
  d=1   L1183  T=0 F=0  T=0 F=12  if (val == NULL) {
  d=1   L1195  T=0 F=0  T=33 F=3  if (val[0] != 0) {
  d=1   L1199  T=0 F=0  T=33 F=0  if (uri == NULL) {
  d=1   L1200  T=0 F=0  T=18 F=15  if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
  d=1   L1200  T=0 F=0  T=33 F=0  if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
  d=1   L1221  T=0 F=0  T=0 F=36  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=1   L1221  T=0 F=0  T=36 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=1   L1226  T=0 F=0  T=36 F=0  if (name != NULL)
  d=1   L1228  T=0 F=0  T=0 F=36  if (nval != NULL)
  d=1   L1230  T=0 F=0  T=12 F=24  if (val != value)
  d=1   L1234  T=12 F=0  T=3 F=0  if ((!ctxt->html) &&
  d=1   L1235  T=0 F=6  T=0 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=1   L1235  T=6 F=6  T=3 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=1   L1235  T=6 F=0  T=0 F=3  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=1   L1303  T=6 F=6  T=3 F=0  if (ns != NULL) {
  d=1   L1306  T=6 F=0  T=3 F=0  if (namespace == NULL) {
  d=1   L1338  T=0 F=12  T=0 F=3  if (ret == NULL)
  d=1   L1341  T=0 F=0  T=3 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=1   L1341  T=0 F=12  T=3 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=1   L1346  T=0 F=0  T=3 F=3  while (tmp != NULL) {
  d=1   L1348  T=0 F=0  T=3 F=0  if (tmp->next == NULL)
  d=1   L1352  T=12 F=0  T=0 F=0  } else if (value != NULL) {
  d=1   L1355  T=12 F=0  T=0 F=0  if (ret->children != NULL)
  d=1   L1360  T=0 F=12  T=0 F=3  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1360  T=12 F=0  T=3 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1403  T=12 F=0  T=3 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=1   L1404  T=0 F=12  T=3 F=0  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=1   L1404  T=0 F=0  T=3 F=0  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=1   L1405  T=12 F=0  T=0 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L1405  T=12 F=0  T=0 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L1407  T=12 F=0  T=3 F=0  (ret->children != NULL) &&
  d=1   L1408  T=12 F=0  T=3 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=1   L1409  T=12 F=0  T=3 F=0  (ret->children->next == NULL)) {
  d=1   L1415  T=0 F=12  T=0 F=3  if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
  d=1   L1427  T=0 F=12  T=0 F=3  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
  d=1   L1429  T=0 F=12  T=0 F=3  else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
  d=1   L1434  T=6 F=6  T=0 F=3  if (nval != NULL)
  d=1   L1436  T=6 F=6  T=3 F=0  if (ns != NULL)

[off-chain: 129 additional divergent branches across 14 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=f120aaa512a7ba5e, size=370 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=16996s, mutation_op=WordInterestingMutator,DwordAddMutator,DwordInterestingMutator):
  0000: 6b 6b 6b 6b 6b de 00 00 31 32 37 37 37 32 27 78   kkkkk...127772'x
  0010: 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f   ml\.<?xml versio
  0020: 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54   n="1.0"?>.<!DOCT
  0030: 59 50 45 0a 61 0a 53 59 53 54 45 4d 20 22 64 74   YPE.a.SYSTEM "dt
Seed 2 (id=b0c93658f77d3e4f, size=370 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=68227s, mutation_op=BytesCopyMutator,ByteDecMutator,ByteAddMutator,QwordAddMutator,BytesDeleteMutator,CrossoverInsertMutator):
  0000: 6b 6b 6b 6b 6b de 00 00 31 32 37 37 37 32 27 78   kkkkk...127772'x
  0010: 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65 72 73 69 6f   ml\.<?xml versio
  0020: 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54   n="1.0"?>.<!DOCT
  0030: 59 50 45 0a 61 0a 53 59 53 54 45 4d 20 22 64 74   YPE.a.SYSTEM "dt

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=a3a19ccf3245d2fa, size=130 bytes, fuzzer=value_profile, trial=2, discovered_at=22250s, mutation_op=BytesRandInsertMutator,BytesRandInsertMutator,ByteFlipMutator,BytesDeleteMutator,BytesRandSetMutator):
  0000: 3b 3b 3b 3b 3b 3b 3b 3b 3b 3b 3b 3b 3b 3b d6 3d   ;;;;;;;;;;;;;;.=
  0010: f6 3b 3b 3b 54 54 4c 49 53 54 20 20 27 69 74 74   .;;;TTLIST  'itt
  0020: 70 3a 2f 2f 77 88 77 d2 d1 2f 2f 2f 5f 5f 5f 5f   p://w.w..///____
  0030: 2f 2f ce 3f ef ef 62 22 4a 03 01 00 ef 62 22 4a   //.?..b"J....b"J
Seed 2 (id=1b39186f122ab058, size=258 bytes, fuzzer=value_profile, trial=2, discovered_at=22387s, mutation_op=BitFlipMutator,BytesDeleteMutator,TokenReplace,DwordInterestingMutator,ByteAddMutator):
  0000: ef ef 2e 78 6d 6c 5c 0a 3c 6c df 76 62 20 78 6d   ...xml\.<l.vb xm
  0010: 6c 6e 73 3d 22 31 2e 30 f1 ef ef ef ef 9b ff ff   lns="1.0........
  0020: ff ff ff 0a ff 22 3e 0a 0a 3c 61 3e 0a 20 20 3c   .....">..<a>.  <
  0030: 62 0a 3c 61 74 74 74 74 74 50 45 20 61 20 53 59   b.<atttttPE a SY
Seed 3 (id=4398e84e37abb198, size=282 bytes, fuzzer=value_profile, trial=2, discovered_at=22399s, mutation_op=ByteAddMutator,BytesSwapMutator,BytesSetMutator,BytesSetMutator,BitFlipMutator):
  0000: 45 03 01 00 ef 62 22 4a 03 01 00 22 00 01 00 ff   E....b"J..."....
  0010: 3c 30 ef 3e 0a 3c 01 37 37 32 ef ef ef ef ef ef   <0.>.<.772......
  0020: 2e 78 6d 6c 5c 0a 3c 6c df 76 62 20 78 6d 6c 6e   .xml\.<l.vb xmln
  0030: 73 3d 22 31 2e 30 f1 ef ef ef ef d0 73 73 73 73   s="1.0......ssss
Seed 4 (id=7e9446114c8524dc, size=278 bytes, fuzzer=value_profile, trial=2, discovered_at=22399s, mutation_op=BytesRandInsertMutator,BytesDeleteMutator,ByteIncMutator):
  0000: 23 62 22 23 21 21 62 22 23 21 21 49 45 8f 8f 8f   #b"#!!b"#!!IE...
  0010: 8f 8f 8f 8f 8f 8f 8f 8f 8f 8f 8f 8f 8f 03 01 00   ................
  0020: ef 62 22 4a 03 01 00 22 00 01 00 ff 3c 30 ef 3e   .b"J..."....<0.>
  0030: 0a 3c 01 f5 ff ff ff ff ff ff ff 37 37 32 ef ef   .<.........772..
Seed 5 (id=c7ab7d01d62efa61, size=278 bytes, fuzzer=value_profile, trial=2, discovered_at=22400s, mutation_op=BytesInsertMutator,QwordAddMutator,TokenInsert,BytesRandInsertMutator,WordInterestingMutator,BytesSetMutator,ByteDecMutator):
  0000: 7f ff 20 49 45 03 01 00 ef 62 22 23 21 21 62 22   .. IE....b"#!!b"
  0010: 23 62 22 23 21 21 62 22 23 21 21 49 45 03 01 00   #b"#!!b"#!!IE...
  0020: ef 62 22 4a 03 01 00 22 00 01 00 ff 3c 30 ef 3e   .b"J..."....<0.>
  0030: 0a 3c 01 37 37 32 ef ef ef ef ef ef 2e 78 6d 6c   .<.772.......xml


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  6b(k)x2                             01(.)x3 ef(.)x2 7f(.)x2 2f(/)x2 +3u  DIFFER
   0x0001  6b(k)x2                             37(7)x3 2f(/)x2 3b(;)x1 ef(.)x1 +5u  DIFFER
   0x0002  6b(k)x2                             37(7)x3 2f(/)x2 3b(;)x1 2e(.)x1 +5u  DIFFER
   0x0003  6b(k)x2                             32(2)x3 2f(/)x2 3b(;)x1 78(x)x1 +5u  DIFFER
   0x0004  6b(k)x2                             ef(.)x4 45(E)x2 73(s)x2 3b(;)x1 +3u  DIFFER
   0x0005  de(.)x2                             76(v)x3 03(.)x2 73(s)x2 3b(;)x1 +4u  DIFFER
   0x0006  00(.)x2                             76(v)x3 01(.)x2 74(t)x2 3b(;)x1 +4u  DIFFER
   0x0007  00(.)x2                             76(v)x3 00(.)x2 70(p)x2 3b(;)x1 +4u  PARTIAL
   0x0008  31(1)x2                             76(v)x3 ef(.)x2 3a(:)x2 3b(;)x1 +4u  DIFFER
   0x0009  32(2)x2                             76(v)x3 62(b)x2 2f(/)x2 3b(;)x1 +4u  DIFFER
   0x000a  37(7)x2                             ef(.)x3 22(")x2 2f(/)x2 3b(;)x1 +4u  DIFFER
   0x000b  37(7)x2                             ef(.)x3 23(#)x2 77(w)x2 3b(;)x1 +4u  DIFFER
   0x000c  37(7)x2                             ef(.)x3 21(!)x2 25(%)x2 3b(;)x1 +4u  DIFFER
   0x000d  32(2)x2                             ef(.)x3 21(!)x2 30(0)x2 3b(;)x1 +4u  DIFFER
   0x000e  27(')x2                             ef(.)x3 62(b)x2 36(6)x2 d6(.)x1 +4u  DIFFER
   0x000f  78(x)x2                             ff(.)x4 22(")x2 34(4)x2 3d(=)x1 +3u  DIFFER
   0x0010  6d(m)x2                             78(x)x3 23(#)x2 36(6)x2 f6(.)x1 +4u  DIFFER
   0x0011  6c(l)x2                             6d(m)x3 62(b)x2 2e(.)x2 3b(;)x1 +4u  DIFFER
   0x0012  5c(\)x2                             6c(l)x3 22(")x2 55(U)x2 3b(;)x1 +4u  DIFFER
   0x0013  0a(.)x2                             5c(\)x3 23(#)x2 76(v)x2 3b(;)x1 +4u  DIFFER
   0x0014  3c(<)x2                             0a(.)x4 21(!)x2 76(v)x2 54(T)x1 +3u  DIFFER
   0x0015  3f(?)x2                             3c(<)x4 21(!)x2 76(v)x2 54(T)x1 +3u  DIFFER
   0x0016  78(x)x2                             6c(l)x3 62(b)x2 76(v)x2 4c(L)x1 +4u  DIFFER
   0x0017  6d(m)x2                             df(.)x3 22(")x2 5c(\)x2 49(I)x1 +4u  DIFFER
   0x0018  6c(l)x2                             76(v)x5 23(#)x2 53(S)x1 f1(.)x1 +3u  DIFFER
   0x0019  20( )x2                             62(b)x3 ef(.)x2 21(!)x2 2f(/)x2 +3u  DIFFER
   0x001a  76(v)x2                             20( )x4 ef(.)x3 21(!)x2 2f(/)x2 +1u  DIFFER
   0x001b  65(e)x2                             ef(.)x3 78(x)x3 49(I)x2 2f(/)x2 +2u  DIFFER
   0x001c  72(r)x2                             6d(m)x3 ef(.)x2 2f(/)x2 27(')x1 +4u  DIFFER
   0x001d  73(s)x2                             2f(/)x3 6c(l)x3 03(.)x2 69(i)x1 +3u  DIFFER
   0x001e  69(i)x2                             6e(n)x3 74(t)x2 01(.)x2 2f(/)x2 +3u  DIFFER
   0x001f  6f(o)x2                             73(s)x3 74(t)x2 00(.)x2 2f(/)x2 +3u  DIFFER
   0x0020  6e(n)x2                             3d(=)x3 ef(.)x2 2f(/)x2 70(p)x1 +4u  DIFFER
   0x0021  3d(=)x2                             22(")x3 62(b)x2 7f(.)x2 3a(:)x1 +4u  DIFFER
   0x0022  22(")x2                             ff(.)x3 31(1)x3 22(")x2 2f(/)x1 +3u  PARTIAL
   0x0023  31(1)x2                             2e(.)x3 4a(J)x2 20( )x2 2f(/)x1 +4u  DIFFER
   0x0024  2e(.)x2                             30(0)x3 03(.)x2 49(I)x2 77(w)x1 +4u  DIFFER
   0x0025  30(0)x2                             f1(.)x3 01(.)x2 45(E)x2 88(.)x1 +4u  DIFFER
   0x0026  22(")x2                             ef(.)x3 00(.)x2 03(.)x2 77(w)x1 +4u  PARTIAL
   0x0027  3f(?)x2                             2f(/)x3 0a(.)x2 22(")x2 01(.)x2 +3u  DIFFER
   ... (24 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6193.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6193,
  "target": "libxml2",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6193 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6193 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6193 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).