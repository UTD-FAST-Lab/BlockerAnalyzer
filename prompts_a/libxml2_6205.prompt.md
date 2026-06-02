==== BLOCKER ====
Target: libxml2
Branch ID: 6205
Location: /src/libxml2/SAX2.c:1236:9
Enclosing function: SAX2.c:xmlSAX2AttributeInternal
Source line:         (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (I2S vs cmplog)
cmplog                           8        2          0  winner (I2S vs naive)
value_profile                    3        7          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        5        5          0  REFERENCE
naive_ngram4                     0        9          1  REFERENCE
mopt                             1        8          1  REFERENCE
minimizer                        5        5          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                        10        0          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 31  (cmplog vs naive, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=10.20h  loser=18.10h
  avg hitcount on branch: winner=11  loser=2
  prob_div=0.60  dur_div=7.90h  hit_div=9
  subject-level: delta_AUC=23254200.0  p_AUC=0.0452  delta_Final=447.3  p_final=0.001

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6205/{W,L}/branch_coverage_show.txt

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
[B]  1171          (name[3] == 'n') && (name[4] == 's') && (name[5] == 0)) {
[ ]  1172  	xmlNsPtr nsret;
[ ]  1173  	xmlChar *val;
[ ]  1174  
[ ]  1175          /* Avoid unused variable warning if features are disabled. */
[ ]  1176          (void) nsret;
[ ]  1177  
[ ]  1178          if (!ctxt->replaceEntities) {
[ ]  1179  	    ctxt->depth++;
[ ]  1180  	    val = xmlStringDecodeEntities(ctxt, value, XML_SUBSTITUTE_REF,
[ ]  1181  		                          0,0,0);
[ ]  1182  	    ctxt->depth--;
[ ]  1183  	    if (val == NULL) {
[ ]  1184  	        xmlSAX2ErrMemory(ctxt, "xmlSAX2StartElement");
[ ]  1185  		if (name != NULL)
[ ]  1186  		    xmlFree(name);
[ ]  1187                  if (nval != NULL)
[ ]  1188                      xmlFree(nval);
[ ]  1189  		return;
[ ]  1190  	    }
[ ]  1191  	} else {
[ ]  1192  	    val = (xmlChar *) value;
[ ]  1193  	}
[ ]  1194  
[ ]  1195  	if (val[0] != 0) {
[ ]  1196  	    xmlURIPtr uri;
[ ]  1197  
[ ]  1198  	    uri = xmlParseURI((const char *)val);
[ ]  1199  	    if (uri == NULL) {
[ ]  1200  		if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
[ ]  1201  		    ctxt->sax->warning(ctxt->userData,
[ ]  1202  			 "xmlns: %s not a valid URI\n", val);
[ ]  1203  	    } else {
[ ]  1204  		if (uri->scheme == NULL) {
[ ]  1205  		    if ((ctxt->sax != NULL) && (ctxt->sax->warning != NULL))
[ ]  1206  			ctxt->sax->warning(ctxt->userData,
[ ]  1207  			     "xmlns: URI %s is not absolute\n", val);
[ ]  1208  		}
[ ]  1209  		xmlFreeURI(uri);
[ ]  1210  	    }
[ ]  1211  	}
[ ]  1212  
[ ]  1213  	/* a default namespace definition */
[ ]  1214  	nsret = xmlNewNs(ctxt->node, val, NULL);
[ ]  1215  
[ ]  1216  #ifdef LIBXML_VALID_ENABLED
[ ]  1217  	/*
[ ]  1218  	 * Validate also for namespace decls, they are attributes from
[ ]  1219  	 * an XML-1.0 perspective
[ ]  1220  	 */
[ ]  1221          if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
[ ]  1222  	    ctxt->myDoc && ctxt->myDoc->intSubset)
[ ]  1223  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc,
[ ]  1224  					   ctxt->node, prefix, nsret, val);
[ ]  1225  #endif /* LIBXML_VALID_ENABLED */
[ ]  1226  	if (name != NULL)
[ ]  1227  	    xmlFree(name);
[ ]  1228  	if (nval != NULL)
[ ]  1229  	    xmlFree(nval);
[ ]  1230  	if (val != value)
[ ]  1231  	    xmlFree(val);
[ ]  1232  	return;
[ ]  1233      }
[B]  1234      if ((!ctxt->html) &&
[B]  1235  	(ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2] == 'l') &&
[B]  1236          (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) { <-- BLOCKER
[L]  1237  	xmlNsPtr nsret;
[L]  1238  	xmlChar *val;
[ ]  1239  
[ ]  1240          /* Avoid unused variable warning if features are disabled. */
[L]  1241          (void) nsret;
[ ]  1242  
[L]  1243          if (!ctxt->replaceEntities) {
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
[L]  1257  	} else {
[L]  1258  	    val = (xmlChar *) value;
[L]  1259  	}
[ ]  1260  
[L]  1261  	if (val[0] == 0) {
[ ]  1262  	    xmlNsErrMsg(ctxt, XML_NS_ERR_EMPTY,
[ ]  1263  		        "Empty namespace name for prefix %s\n", name, NULL);
[ ]  1264  	}
[L]  1265  	if ((ctxt->pedantic != 0) && (val[0] != 0)) {
[L]  1266  	    xmlURIPtr uri;
[ ]  1267  
[L]  1268  	    uri = xmlParseURI((const char *)val);
[L]  1269  	    if (uri == NULL) {
[L]  1270  	        xmlNsWarnMsg(ctxt, XML_WAR_NS_URI,
[L]  1271  			 "xmlns:%s: %s not a valid URI\n", name, value);
[L]  1272  	    } else {
[L]  1273  		if (uri->scheme == NULL) {
[ ]  1274  		    xmlNsWarnMsg(ctxt, XML_WAR_NS_URI_RELATIVE,
[ ]  1275  			   "xmlns:%s: URI %s is not absolute\n", name, value);
[ ]  1276  		}
[L]  1277  		xmlFreeURI(uri);
[L]  1278  	    }
[L]  1279  	}
[ ]  1280  
[ ]  1281  	/* a standard namespace definition */
[L]  1282  	nsret = xmlNewNs(ctxt->node, val, name);
[L]  1283  	xmlFree(ns);
[L]  1284  #ifdef LIBXML_VALID_ENABLED
[ ]  1285  	/*
[ ]  1286  	 * Validate also for namespace decls, they are attributes from
[ ]  1287  	 * an XML-1.0 perspective
[ ]  1288  	 */
[L]  1289          if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
[L]  1290  	    ctxt->myDoc && ctxt->myDoc->intSubset)
[ ]  1291  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc,
[ ]  1292  					   ctxt->node, prefix, nsret, value);
[L]  1293  #endif /* LIBXML_VALID_ENABLED */
[L]  1294  	if (name != NULL)
[L]  1295  	    xmlFree(name);
[L]  1296  	if (nval != NULL)
[ ]  1297  	    xmlFree(nval);
[L]  1298  	if (val != value)
[ ]  1299  	    xmlFree(val);
[L]  1300  	return;
[L]  1301      }
[ ]  1302  
[B]  1303      if (ns != NULL) {
[B]  1304  	namespace = xmlSearchNs(ctxt->myDoc, ctxt->node, ns);
[ ]  1305  
[B]  1306  	if (namespace == NULL) {
[W]  1307  	    xmlNsErrMsg(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[W]  1308  		    "Namespace prefix %s of attribute %s is not defined\n",
[W]  1309  		             ns, name);
[B]  1310  	} else {
[B]  1311              xmlAttrPtr prop;
[ ]  1312  
[B]  1313              prop = ctxt->node->properties;
[B]  1314              while (prop != NULL) {
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
[B]  1331          }
[B]  1332      } else {
[ ]  1333  	namespace = NULL;
[ ]  1334      }
[ ]  1335  
[ ]  1336      /* !!!!!! <a toto:arg="" xmlns:toto="http://toto.com"> */
[B]  1337      ret = xmlNewNsPropEatName(ctxt->node, namespace, name, NULL);
[B]  1338      if (ret == NULL)
[ ]  1339          goto error;
[ ]  1340  
[B]  1341      if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
[ ]  1342          xmlNodePtr tmp;
[ ]  1343  
[ ]  1344          ret->children = xmlStringGetNodeList(ctxt->myDoc, value);
[ ]  1345          tmp = ret->children;
[ ]  1346          while (tmp != NULL) {
[ ]  1347              tmp->parent = (xmlNodePtr) ret;
[ ]  1348              if (tmp->next == NULL)
[ ]  1349                  ret->last = tmp;
[ ]  1350              tmp = tmp->next;
[ ]  1351          }
[B]  1352      } else if (value != NULL) {
[B]  1353          ret->children = xmlNewDocText(ctxt->myDoc, value);
[B]  1354          ret->last = ret->children;
[B]  1355          if (ret->children != NULL)
[B]  1356              ret->children->parent = (xmlNodePtr) ret;
[B]  1357      }
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
[L]  1564  			    i = 0;
[L]  1565  			    att = atts[i];
[L]  1566  			    while (att != NULL) {
[L]  1567  				if (xmlStrEqual(att, fulln))
[ ]  1568  				    break;
[L]  1569  				i += 2;
[L]  1570  				att = atts[i];
[L]  1571  			    }
[L]  1572  			}
[B]  1573  			if (att == NULL) {
[B]  1574  			    xmlSAX2AttributeInternal(ctxt, fulln, <-- CALL
[B]  1575  						 attr->defaultValue, prefix);
[B]  1576  			}
[B]  1577  			if ((fulln != fn) && (fulln != attr->name))
[ ]  1578  			    xmlFree(fulln);
[B]  1579  		    }
[B]  1580  		}
[B]  1581  	    }
[B]  1582  	    attr = attr->nexth;
[B]  1583  	}
[B]  1584  	if (internal == 1) {

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 2  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       6         0  SAX2.c:xmlNsErrMsg  (/src/libxml2/SAX2.c:1070-1080)
       3         0  SAX2.c:xmlErrValid  (/src/libxml2/SAX2.c:99-124)
       0         2  SAX2.c:xmlNsWarnMsg  (/src/libxml2/SAX2.c:194-204)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591) ---
  d=2   L1461  T=6 F=15  T=11 F=0  if (elemDecl != NULL) {
  d=2   L1539  T=0 F=6  T=5 F=0  (xmlStrEqual(attr->prefix, BAD_CAST "xmlns"))) ||
  d=2   L1540  T=0 F=6  T=0 F=0  ((attr->prefix == NULL) &&
  d=2   L1542  T=6 F=0  T=0 F=0  (ctxt->loadsubset & XML_COMPLETE_ATTRS)) {
  d=2   L1563  T=0 F=6  T=3 F=2  if (atts != NULL) {
  d=2   L1566  T=0 F=0  T=3 F=3  while (att != NULL) {
  d=2   L1567  T=0 F=0  T=0 F=3  if (xmlStrEqual(att, fulln))
--- d=2  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806) ---
  d=2   L1624  T=9 F=12  T=0 F=11  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=2   L1624  T=3 F=6  T=0 F=0  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=2   L1625  T=0 F=3  T=0 F=0  ((ctxt->myDoc->intSubset == NULL) ||
  d=2   L1626  T=3 F=0  T=0 F=0  ((ctxt->myDoc->intSubset->notations == NULL) &&
  d=2   L1627  T=3 F=0  T=0 F=0  (ctxt->myDoc->intSubset->elements == NULL) &&
  d=2   L1628  T=3 F=0  T=0 F=0  (ctxt->myDoc->intSubset->attributes == NULL) &&
  d=2   L1629  T=3 F=0  T=0 F=0  (ctxt->myDoc->intSubset->entities == NULL)))) {
  d=2   L1723  T=6 F=0  T=3 F=0  while ((att != NULL) && (value != NULL)) {
  d=2   L1723  T=6 F=6  T=3 F=3  while ((att != NULL) && (value != NULL)) {
  d=2   L1724  T=3 F=0  T=0 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1724  T=3 F=3  T=0 F=3  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1724  T=6 F=0  T=3 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1725  T=0 F=3  T=0 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=2   L1763  T=0 F=6  T=0 F=3  if (ctxt->html) {
  d=2   L1770  T=6 F=6  T=3 F=3  while ((att != NULL) && (value != NULL)) {
  d=2   L1770  T=6 F=0  T=3 F=0  while ((att != NULL) && (value != NULL)) {
  d=2   L1771  T=0 F=3  T=0 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1771  T=3 F=3  T=3 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1771  T=0 F=6  T=0 F=3  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1772  T=3 F=0  T=0 F=0  (att[3] != 'n') || (att[4] != 's'))
  d=2   L1789  T=6 F=15  T=0 F=11  if ((ctxt->validate) &&
  d=2   L1790  T=3 F=3  T=0 F=0  ((ctxt->vctxt.flags & XML_VCTXT_DTD_VALIDATED) == 0)) {
  d=2   L1794  T=0 F=3  T=0 F=0  if (chk <= 0)
  d=2   L1796  T=0 F=3  T=0 F=0  if (chk < 0)
--- d=1  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=1   L1159  T=3 F=9  T=0 F=8  if (nval != NULL)
  d=1   L1236  T=0 F=6  T=5 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {  <-- BLOCKER
  d=1   L1236  T=0 F=0  T=5 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {  <-- BLOCKER
  d=1   L1236  T=0 F=0  T=5 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {  <-- BLOCKER
  d=1   L1243  T=0 F=0  T=0 F=5  if (!ctxt->replaceEntities) {
  d=1   L1261  T=0 F=0  T=0 F=5  if (val[0] == 0) {
  d=1   L1265  T=0 F=0  T=5 F=0  if ((ctxt->pedantic != 0) && (val[0] != 0)) {
  d=1   L1265  T=0 F=0  T=5 F=0  if ((ctxt->pedantic != 0) && (val[0] != 0)) {
  d=1   L1269  T=0 F=0  T=2 F=3  if (uri == NULL) {
  d=1   L1273  T=0 F=0  T=0 F=3  if (uri->scheme == NULL) {
  d=1   L1289  T=0 F=0  T=0 F=5  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=1   L1289  T=0 F=0  T=5 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=1   L1294  T=0 F=0  T=5 F=0  if (name != NULL)
  d=1   L1296  T=0 F=0  T=0 F=5  if (nval != NULL)
  d=1   L1298  T=0 F=0  T=0 F=5  if (val != value)
  d=1   L1303  T=12 F=0  T=3 F=0  if (ns != NULL) {
  d=1   L1306  T=6 F=6  T=0 F=3  if (namespace == NULL) {
  d=1   L1314  T=0 F=6  T=0 F=3  while (prop != NULL) {
  d=1   L1338  T=0 F=12  T=0 F=3  if (ret == NULL)
  d=1   L1341  T=0 F=12  T=0 F=3  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=1   L1352  T=12 F=0  T=3 F=0  } else if (value != NULL) {
  d=1   L1355  T=12 F=0  T=3 F=0  if (ret->children != NULL)
  d=1   L1360  T=6 F=6  T=0 F=3  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1360  T=0 F=6  T=0 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1360  T=12 F=0  T=3 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1403  T=12 F=0  T=3 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=1   L1404  T=0 F=12  T=0 F=3  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=1   L1405  T=12 F=0  T=3 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L1405  T=12 F=0  T=3 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L1407  T=12 F=0  T=3 F=0  (ret->children != NULL) &&
  d=1   L1408  T=12 F=0  T=3 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=1   L1409  T=12 F=0  T=3 F=0  (ret->children->next == NULL)) {
  d=1   L1415  T=0 F=12  T=0 F=3  if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
  d=1   L1427  T=0 F=12  T=0 F=3  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
  d=1   L1429  T=0 F=12  T=0 F=3  else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
  d=1   L1434  T=3 F=9  T=0 F=3  if (nval != NULL)
  d=1   L1436  T=12 F=0  T=3 F=0  if (ns != NULL)

[off-chain: 81 additional divergent branches across 12 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=51fd9b36079604e3, size=371 bytes, fuzzer=cmplog, trial=1, discovered_at=3541s, mutation_op=ByteAddMutator,DwordInterestingMutator):
  0000: ff 7f ff ff 31 32 c8 37 37 32 2e 78 6d 6c 5c 0a   ....12.772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=f32dee7a138d773b, size=378 bytes, fuzzer=cmplog, trial=1, discovered_at=24520s, mutation_op=WordInterestingMutator):
  0000: 33 2e 6f 72 67 00 02 39 39 39 2f 78 3a 69 6e 6b   3.org..999/x:ink
  0010: 27 0a 20 20 20 20 20 20 20 20 78 6d 6c 6e 73 28   '.        xmlns(
  0020: 78 6c 69 6e 6b 20 20 43 44 41 54 41 20 20 20 20   xlink  CDATA    
  0030: 20 23 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65    #.xml\.<?xml ve

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=e38b37912b0d39bb, size=407 bytes, fuzzer=naive, trial=1, discovered_at=342s, mutation_op=BytesDeleteMutator,WordInterestingMutator,BitFlipMutator,BytesDeleteMutator,BytesExpandMutator,TokenInsert):
  0000: 8b 22 3e 62 20 74 65 78 6d 6c 5c 0a 3c 3f 78 6d   .">b texml\.<?xm
  0010: 6c 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f   l version="1.0"?
  0020: 3e 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59   >.<!DOCTYPE a SY
  0030: 53 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37   STEM "dtds/12777
Seed 2 (id=9b6b2bebaa2cdd22, size=372 bytes, fuzzer=naive, trial=1, discovered_at=3395s, mutation_op=WordInterestingMutator,BytesRandSetMutator):
  0000: ab ab ab 00 31 32 37 37 38 32 2e 78 6d 6c 5c 0a   ....127782.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  ff(.)x1 33(3)x1                     8b(.)x1 ab(.)x1                     DIFFER
   0x0001  7f(.)x1 2e(.)x1                     22(")x1 ab(.)x1                     DIFFER
   0x0002  ff(.)x1 6f(o)x1                     3e(>)x1 ab(.)x1                     DIFFER
   0x0003  ff(.)x1 72(r)x1                     62(b)x1 00(.)x1                     DIFFER
   0x0004  31(1)x1 67(g)x1                     20( )x1 31(1)x1                     PARTIAL
   0x0005  32(2)x1 00(.)x1                     74(t)x1 32(2)x1                     PARTIAL
   0x0006  c8(.)x1 02(.)x1                     65(e)x1 37(7)x1                     DIFFER
   0x0007  37(7)x1 39(9)x1                     78(x)x1 37(7)x1                     PARTIAL
   0x0008  37(7)x1 39(9)x1                     6d(m)x1 38(8)x1                     DIFFER
   0x0009  32(2)x1 39(9)x1                     6c(l)x1 32(2)x1                     PARTIAL
   0x000a  2e(.)x1 2f(/)x1                     5c(\)x1 2e(.)x1                     PARTIAL
   0x000b  78(x)x2                             0a(.)x1 78(x)x1                     PARTIAL
   0x000c  6d(m)x1 3a(:)x1                     3c(<)x1 6d(m)x1                     PARTIAL
   0x000d  6c(l)x1 69(i)x1                     3f(?)x1 6c(l)x1                     PARTIAL
   0x000e  5c(\)x1 6e(n)x1                     78(x)x1 5c(\)x1                     PARTIAL
   0x000f  0a(.)x1 6b(k)x1                     6d(m)x1 0a(.)x1                     PARTIAL
   0x0010  3c(<)x1 27(')x1                     6c(l)x1 3c(<)x1                     PARTIAL
   0x0011  3f(?)x1 0a(.)x1                     20( )x1 3f(?)x1                     PARTIAL
   0x0012  78(x)x1 20( )x1                     76(v)x1 78(x)x1                     PARTIAL
   0x0013  6d(m)x1 20( )x1                     65(e)x1 6d(m)x1                     PARTIAL
   0x0014  6c(l)x1 20( )x1                     72(r)x1 6c(l)x1                     PARTIAL
   0x0015  20( )x2                             73(s)x1 20( )x1                     PARTIAL
   0x0016  76(v)x1 20( )x1                     69(i)x1 76(v)x1                     PARTIAL
   0x0017  65(e)x1 20( )x1                     6f(o)x1 65(e)x1                     PARTIAL
   0x0018  72(r)x1 20( )x1                     6e(n)x1 72(r)x1                     PARTIAL
   0x0019  73(s)x1 20( )x1                     3d(=)x1 73(s)x1                     PARTIAL
   0x001a  69(i)x1 78(x)x1                     22(")x1 69(i)x1                     PARTIAL
   0x001b  6f(o)x1 6d(m)x1                     31(1)x1 6f(o)x1                     PARTIAL
   0x001c  6e(n)x1 6c(l)x1                     2e(.)x1 6e(n)x1                     PARTIAL
   0x001d  3d(=)x1 6e(n)x1                     30(0)x1 3d(=)x1                     PARTIAL
   0x001e  22(")x1 73(s)x1                     22(")x2                             PARTIAL
   0x001f  31(1)x1 28(()x1                     3f(?)x1 31(1)x1                     PARTIAL
   0x0020  2e(.)x1 78(x)x1                     3e(>)x1 2e(.)x1                     PARTIAL
   0x0021  30(0)x1 6c(l)x1                     0a(.)x1 30(0)x1                     PARTIAL
   0x0022  22(")x1 69(i)x1                     3c(<)x1 22(")x1                     PARTIAL
   0x0023  3f(?)x1 6e(n)x1                     21(!)x1 3f(?)x1                     PARTIAL
   0x0024  3e(>)x1 6b(k)x1                     44(D)x1 3e(>)x1                     PARTIAL
   0x0025  0a(.)x1 20( )x1                     4f(O)x1 0a(.)x1                     PARTIAL
   0x0026  3c(<)x1 20( )x1                     43(C)x1 3c(<)x1                     PARTIAL
   0x0027  21(!)x1 43(C)x1                     54(T)x1 21(!)x1                     PARTIAL
   ... (23 more divergent offsets)
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6205.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6205,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6205 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6205 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6205 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).