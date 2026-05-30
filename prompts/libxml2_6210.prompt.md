==== BLOCKER ====
Target: libxml2
Branch ID: 6210
Location: /src/libxml2/SAX2.c:1261:6
Enclosing function: SAX2.c:xmlSAX2AttributeInternal
Source line: 	if (val[0] == 0) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           2        8          0  loser (grimoire_structural vs grimoire)
value_profile                    5        5          0  REFERENCE
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        0       10          0  REFERENCE
naive_ngram4                     0        9          1  REFERENCE
mopt                             0        8          2  REFERENCE
minimizer                        1        9          0  REFERENCE
fast                             2        6          2  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=4.70h  loser=17.90h
  avg hitcount on branch: winner=20  loser=1
  prob_div=0.80  dur_div=13.20h  hit_div=19
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6210/{W,L}/branch_coverage_show.txt

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
[ ]  1160              value = nval;
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
[B]  1236          (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
[B]  1237  	xmlNsPtr nsret;
[B]  1238  	xmlChar *val;
[ ]  1239  
[ ]  1240          /* Avoid unused variable warning if features are disabled. */
[B]  1241          (void) nsret;
[ ]  1242  
[B]  1243          if (!ctxt->replaceEntities) {
[W]  1244  	    ctxt->depth++;
[W]  1245  	    val = xmlStringDecodeEntities(ctxt, value, XML_SUBSTITUTE_REF,
[W]  1246  		                          0,0,0);
[W]  1247  	    ctxt->depth--;
[W]  1248  	    if (val == NULL) {
[ ]  1249  	        xmlSAX2ErrMemory(ctxt, "xmlSAX2StartElement");
[ ]  1250  	        xmlFree(ns);
[ ]  1251  		if (name != NULL)
[ ]  1252  		    xmlFree(name);
[ ]  1253                  if (nval != NULL)
[ ]  1254                      xmlFree(nval);
[ ]  1255  		return;
[ ]  1256  	    }
[B]  1257  	} else {
[B]  1258  	    val = (xmlChar *) value;
[B]  1259  	}
[ ]  1260  
[B]  1261  	if (val[0] == 0) { <-- BLOCKER
[W]  1262  	    xmlNsErrMsg(ctxt, XML_NS_ERR_EMPTY,
[W]  1263  		        "Empty namespace name for prefix %s\n", name, NULL);
[W]  1264  	}
[B]  1265  	if ((ctxt->pedantic != 0) && (val[0] != 0)) {
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
[B]  1282  	nsret = xmlNewNs(ctxt->node, val, name);
[B]  1283  	xmlFree(ns);
[B]  1284  #ifdef LIBXML_VALID_ENABLED
[ ]  1285  	/*
[ ]  1286  	 * Validate also for namespace decls, they are attributes from
[ ]  1287  	 * an XML-1.0 perspective
[ ]  1288  	 */
[B]  1289          if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
[B]  1290  	    ctxt->myDoc && ctxt->myDoc->intSubset)
[W]  1291  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc,
[W]  1292  					   ctxt->node, prefix, nsret, value);
[B]  1293  #endif /* LIBXML_VALID_ENABLED */
[B]  1294  	if (name != NULL)
[B]  1295  	    xmlFree(name);
[B]  1296  	if (nval != NULL)
[ ]  1297  	    xmlFree(nval);
[B]  1298  	if (val != value)
[W]  1299  	    xmlFree(val);
[B]  1300  	return;
[B]  1301      }
[ ]  1302  
[B]  1303      if (ns != NULL) {
[L]  1304  	namespace = xmlSearchNs(ctxt->myDoc, ctxt->node, ns);
[ ]  1305  
[L]  1306  	if (namespace == NULL) {
[L]  1307  	    xmlNsErrMsg(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[L]  1308  		    "Namespace prefix %s of attribute %s is not defined\n",
[L]  1309  		             ns, name);
[L]  1310  	} else {
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
[W]  1342          xmlNodePtr tmp;
[ ]  1343  
[W]  1344          ret->children = xmlStringGetNodeList(ctxt->myDoc, value);
[W]  1345          tmp = ret->children;
[W]  1346          while (tmp != NULL) {
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
[W]  1367          if (!ctxt->replaceEntities) {
[W]  1368  	    xmlChar *val;
[ ]  1369  
[W]  1370  	    ctxt->depth++;
[W]  1371  	    val = xmlStringDecodeEntities(ctxt, value, XML_SUBSTITUTE_REF,
[W]  1372  		                          0,0,0);
[W]  1373  	    ctxt->depth--;
[ ]  1374  
[W]  1375  	    if (val == NULL)
[ ]  1376  		ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt,
[ ]  1377  				ctxt->myDoc, ctxt->node, ret, value);
[W]  1378  	    else {
[W]  1379  		xmlChar *nvalnorm;
[ ]  1380  
[ ]  1381  		/*
[ ]  1382  		 * Do the last stage of the attribute normalization
[ ]  1383  		 * It need to be done twice ... it's an extra burden related
[ ]  1384  		 * to the ability to keep xmlSAX2References in attributes
[ ]  1385  		 */
[W]  1386  		nvalnorm = xmlValidNormalizeAttributeValue(ctxt->myDoc,
[W]  1387  					    ctxt->node, fullname, val);
[W]  1388  		if (nvalnorm != NULL) {
[ ]  1389  		    xmlFree(val);
[ ]  1390  		    val = nvalnorm;
[ ]  1391  		}
[ ]  1392  
[W]  1393  		ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt,
[W]  1394  			        ctxt->myDoc, ctxt->node, ret, val);
[W]  1395                  xmlFree(val);
[W]  1396  	    }
[W]  1397  	} else {
[W]  1398  	    ctxt->valid &= xmlValidateOneAttribute(&ctxt->vctxt, ctxt->myDoc,
[W]  1399  					       ctxt->node, ret, value);
[W]  1400  	}
[W]  1401      } else
[L]  1402  #endif /* LIBXML_VALID_ENABLED */
[L]  1403             if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
[L]  1404  	       (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
[L]  1405  	        ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
[ ]  1406                 /* Don't create IDs containing entity references */
[L]  1407                 (ret->children != NULL) &&
[L]  1408                 (ret->children->type == XML_TEXT_NODE) &&
[L]  1409                 (ret->children->next == NULL)) {
[L]  1410          xmlChar *content = ret->children->content;
[ ]  1411          /*
[ ]  1412  	 * when validating, the ID registration is done at the attribute
[ ]  1413  	 * validation level. Otherwise we have to do specific handling here.
[ ]  1414  	 */
[L]  1415  	if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
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
[L]  1427  	} else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
[ ]  1428  	    xmlAddID(&ctxt->vctxt, ctxt->myDoc, content, ret);
[L]  1429  	else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
[ ]  1430  	    xmlAddRef(&ctxt->vctxt, ctxt->myDoc, content, ret);
[L]  1431      }
[ ]  1432  
[B]  1433  error:
[B]  1434      if (nval != NULL)
[ ]  1435  	xmlFree(nval);
[B]  1436      if (ns != NULL)
[L]  1437  	xmlFree(ns);
[B]  1438  }

--- Caller (1 hop): SAX2.c:xmlCheckDefaultedAttributes (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574) (±10 around call site) ---
[B]  1564  			    i = 0;
[B]  1565  			    att = atts[i];
[B]  1566  			    while (att != NULL) {
[B]  1567  				if (xmlStrEqual(att, fulln))
[ ]  1568  				    break;
[B]  1569  				i += 2;
[B]  1570  				att = atts[i];
[B]  1571  			    }
[B]  1572  			}
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
      18         3  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758)
      12         4  xmlSAXVersion  (/src/libxml2/SAX2.c:2886-2930)
       9         2  xmlSAX2EndDocument  (/src/libxml2/SAX2.c:1023-1054)
       9         3  xmlSAX2SetDocumentLocator  (/src/libxml2/SAX2.c:942-948)
       9         3  xmlSAX2StartDocument  (/src/libxml2/SAX2.c:958-1013)
       9         3  SAX2.c:xmlNsErrMsg  (/src/libxml2/SAX2.c:1070-1080)
       0         6  xmlSAX2IgnorableWhitespace  (/src/libxml2/SAX2.c:2698-2704)
       6         0  xmlSAX2ProcessingInstruction  (/src/libxml2/SAX2.c:2717-2769)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591) ---
  d=2   L1454  T=12 F=0  T=6 F=0  if (elemDecl == NULL) {
  d=2   L1461  T=12 F=0  T=6 F=0  if (elemDecl != NULL) {
  d=2   L1467  T=0 F=12  T=0 F=6  if ((ctxt->myDoc->standalone == 1) &&
  d=2   L1523  T=18 F=12  T=3 F=6  while (attr != NULL) {
  d=2   L1529  T=9 F=9  T=3 F=0  if (attr->defaultValue != NULL) {
  d=2   L1538  T=6 F=3  T=3 F=0  if (((attr->prefix != NULL) &&
  d=2   L1539  T=6 F=0  T=3 F=0  (xmlStrEqual(attr->prefix, BAD_CAST "xmlns"))) ||
  d=2   L1540  T=3 F=0  T=0 F=0  ((attr->prefix == NULL) &&
  d=2   L1541  T=0 F=3  T=0 F=0  (xmlStrEqual(attr->name, BAD_CAST "xmlns"))) ||
  d=2   L1542  T=0 F=3  T=0 F=0  (ctxt->loadsubset & XML_COMPLETE_ATTRS)) {
  d=2   L1548  T=0 F=6  T=0 F=3  if ((tst == attr) || (tst == NULL)) {
  d=2   L1548  T=6 F=0  T=3 F=0  if ((tst == attr) || (tst == NULL)) {
  d=2   L1553  T=0 F=6  T=0 F=3  if (fulln == NULL) {
  d=2   L1563  T=6 F=0  T=3 F=0  if (atts != NULL) {
  d=2   L1566  T=6 F=6  T=3 F=3  while (att != NULL) {
  d=2   L1567  T=0 F=6  T=0 F=3  if (xmlStrEqual(att, fulln))
  d=2   L1573  T=6 F=0  T=3 F=0  if (att == NULL) {
  d=2   L1577  T=0 F=6  T=0 F=3  if ((fulln != fn) && (fulln != attr->name))
  d=2   L1584  T=0 F=12  T=0 F=6  if (internal == 1) {
--- d=2  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806) ---
  d=2   L1614  T=0 F=15  T=0 F=6  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=2   L1614  T=0 F=15  T=0 F=6  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=2   L1614  T=0 F=15  T=0 F=6  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=2   L1624  T=12 F=3  T=0 F=6  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=2   L1624  T=0 F=12  T=0 F=0  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=2   L1648  T=0 F=15  T=0 F=6  if (ret == NULL) {
  d=2   L1654  T=3 F=12  T=0 F=6  if (ctxt->myDoc->children == NULL) {
  d=2   L1659  T=6 F=6  T=3 F=3  } else if (parent == NULL) {
  d=2   L1663  T=15 F=0  T=6 F=0  if (ctxt->linenumbers) {
  d=2   L1664  T=15 F=0  T=6 F=0  if (ctxt->input != NULL) {
  d=2   L1665  T=15 F=0  T=6 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=2   L1678  T=0 F=15  T=0 F=6  if (nodePush(ctxt, ret) < 0) {
  d=2   L1689  T=12 F=3  T=6 F=0  if (parent != NULL) {
  d=2   L1690  T=6 F=6  T=3 F=3  if (parent->type == XML_ELEMENT_NODE) {
  d=2   L1706  T=15 F=0  T=6 F=0  if (!ctxt->html) {
  d=2   L1711  T=12 F=3  T=6 F=0  if ((ctxt->myDoc->intSubset != NULL) ||
  d=2   L1712  T=0 F=3  T=0 F=0  (ctxt->myDoc->extSubset != NULL)) {
  d=2   L1719  T=9 F=6  T=3 F=3  if (atts != NULL) {
  d=2   L1723  T=9 F=0  T=3 F=0  while ((att != NULL) && (value != NULL)) {
  d=2   L1723  T=9 F=9  T=3 F=3  while ((att != NULL) && (value != NULL)) {
  d=2   L1724  T=3 F=0  T=0 F=3  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1724  T=3 F=6  T=3 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1725  T=3 F=0  T=0 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=2   L1725  T=3 F=0  T=0 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=2   L1738  T=12 F=3  T=6 F=0  if ((ns == NULL) && (parent != NULL))
  d=2   L1738  T=15 F=0  T=6 F=0  if ((ns == NULL) && (parent != NULL))
  d=2   L1740  T=0 F=15  T=0 F=6  if ((prefix != NULL) && (ns == NULL)) {
  d=2   L1751  T=0 F=15  T=0 F=6  if ((ns != NULL) && (ns->href != NULL) &&
  d=2   L1759  T=9 F=6  T=3 F=3  if (atts != NULL) {
  d=2   L1763  T=0 F=9  T=0 F=3  if (ctxt->html) {
  d=2   L1770  T=9 F=9  T=3 F=3  while ((att != NULL) && (value != NULL)) {
  d=2   L1770  T=9 F=0  T=3 F=0  while ((att != NULL) && (value != NULL)) {
  d=2   L1771  T=0 F=3  T=3 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1771  T=6 F=3  T=0 F=3  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1772  T=0 F=3  T=0 F=0  (att[3] != 'n') || (att[4] != 's'))
  d=2   L1772  T=0 F=3  T=0 F=0  (att[3] != 'n') || (att[4] != 's'))
  d=2   L1789  T=12 F=3  T=0 F=6  if ((ctxt->validate) &&
  d=2   L1790  T=6 F=6  T=0 F=0  ((ctxt->vctxt.flags & XML_VCTXT_DTD_VALIDATED) == 0)) {
  d=2   L1794  T=0 F=6  T=0 F=0  if (chk <= 0)
  d=2   L1796  T=0 F=6  T=0 F=0  if (chk < 0)
  d=2   L1803  T=0 F=15  T=0 F=6  if (prefix != NULL)
--- d=1  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=1   L1105  T=0 F=15  T=0 F=6  if (ctxt->html) {
  d=1   L1114  T=15 F=0  T=6 F=0  if ((name != NULL) && (name[0] == 0)) {
  d=1   L1114  T=0 F=15  T=0 F=6  if ((name != NULL) && (name[0] == 0)) {
  d=1   L1131  T=0 F=15  T=0 F=6  if (name == NULL) {
  d=1   L1139  T=0 F=15  T=0 F=6  if ((ctxt->html) &&
  d=1   L1156  T=0 F=15  T=0 F=6  if (ctxt->vctxt.valid != 1) {
  d=1   L1159  T=0 F=15  T=0 F=6  if (nval != NULL)
  d=1   L1169  T=6 F=9  T=0 F=6  if ((!ctxt->html) && (ns == NULL) &&
  d=1   L1169  T=15 F=0  T=6 F=0  if ((!ctxt->html) && (ns == NULL) &&
  d=1   L1170  T=0 F=6  T=0 F=0  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=1   L1234  T=15 F=0  T=6 F=0  if ((!ctxt->html) &&
  d=1   L1235  T=9 F=0  T=3 F=3  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=1   L1235  T=9 F=6  T=6 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=1   L1236  T=9 F=0  T=3 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=1   L1236  T=9 F=0  T=3 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=1   L1236  T=9 F=0  T=3 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=1   L1243  T=6 F=3  T=0 F=3  if (!ctxt->replaceEntities) {
  d=1   L1248  T=0 F=6  T=0 F=0  if (val == NULL) {
  d=1   L1261  T=9 F=0  T=0 F=3  if (val[0] == 0) {  <-- BLOCKER
  d=1   L1265  T=0 F=3  T=0 F=0  if ((ctxt->pedantic != 0) && (val[0] != 0)) {
  d=1   L1265  T=3 F=6  T=0 F=3  if ((ctxt->pedantic != 0) && (val[0] != 0)) {
  d=1   L1289  T=6 F=3  T=0 F=3  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=1   L1289  T=6 F=0  T=0 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=1   L1289  T=9 F=0  T=3 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=1   L1290  T=6 F=0  T=0 F=0  ctxt->myDoc && ctxt->myDoc->intSubset)
  d=1   L1290  T=6 F=0  T=0 F=0  ctxt->myDoc && ctxt->myDoc->intSubset)
  d=1   L1294  T=9 F=0  T=3 F=0  if (name != NULL)
  d=1   L1296  T=0 F=9  T=0 F=3  if (nval != NULL)
  d=1   L1298  T=6 F=3  T=0 F=3  if (val != value)
  d=1   L1303  T=0 F=6  T=3 F=0  if (ns != NULL) {
  d=1   L1306  T=0 F=0  T=3 F=0  if (namespace == NULL) {
  d=1   L1338  T=0 F=6  T=0 F=3  if (ret == NULL)
  d=1   L1341  T=3 F=0  T=0 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=1   L1341  T=3 F=3  T=0 F=3  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=1   L1346  T=0 F=3  T=0 F=0  while (tmp != NULL) {
  d=1   L1360  T=6 F=0  T=0 F=3  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1360  T=6 F=0  T=0 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1360  T=6 F=0  T=3 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1361  T=6 F=0  T=0 F=0  ctxt->myDoc && ctxt->myDoc->intSubset) {
  d=1   L1361  T=6 F=0  T=0 F=0  ctxt->myDoc && ctxt->myDoc->intSubset) {
  d=1   L1367  T=3 F=3  T=0 F=0  if (!ctxt->replaceEntities) {
  d=1   L1375  T=0 F=3  T=0 F=0  if (val == NULL)
  d=1   L1388  T=0 F=3  T=0 F=0  if (nvalnorm != NULL) {
  d=1   L1403  T=0 F=0  T=3 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=1   L1404  T=0 F=0  T=0 F=3  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=1   L1405  T=0 F=0  T=3 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L1405  T=0 F=0  T=3 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L1407  T=0 F=0  T=3 F=0  (ret->children != NULL) &&
  d=1   L1408  T=0 F=0  T=3 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=1   L1409  T=0 F=0  T=3 F=0  (ret->children->next == NULL)) {
  d=1   L1415  T=0 F=0  T=0 F=3  if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
  d=1   L1427  T=0 F=0  T=0 F=3  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
  d=1   L1429  T=0 F=0  T=0 F=3  else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
  d=1   L1434  T=0 F=6  T=0 F=3  if (nval != NULL)
  d=1   L1436  T=0 F=6  T=3 F=0  if (ns != NULL)

[off-chain: 93 additional divergent branches across 12 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=3ab4d97b081ac59f, size=173 bytes, fuzzer=grimoire, trial=1, discovered_at=6390s, mutation_op=GrimoireRandomDeleteMutator,GrimoireRandomDeleteMutator,GrimoireRecursiveReplacementMutator):
  0000: d8 3e 42 0f 6c 5c 0a 3c 3f 6c 20 3f 3e 3c 21 44   .>B.l\.<?l ?><!D
  0010: 4f 43 54 59 50 45 61 20 53 59 53 54 45 4d 20 22   OCTYPEa SYSTEM "
  0020: 64 74 64 73 2f 31 32 37 37 37 32 2e 64 74 64 22   dtds/127772.dtd"
  0030: 3e 3c 61 3e 3c 62 20 51 3d 22 22 3e 5c 0a 64 74   ><a><b Q="">\.dt
Seed 2 (id=282b5462beef8741, size=1059 bytes, fuzzer=grimoire, trial=1, discovered_at=7462s, mutation_op=GrimoireRecursiveReplacementMutator):
  0000: 49 53 4f 2d 38 38 35 39 2d 34 00 00 6d 6c 5c 0a   ISO-8859-4..ml\.
  0010: 3c 3f 78 6d 6c 20 3e 3c 62 20 78 6d 6c 6e 73 3a   <?xml ><b xmlns:
  0020: 66 3d 22 22 3e 74 64 5c 0a 9b 70 3a 2f 2f 6e 22   f="">td\..p://n"
  0030: 3e 7f 96 98 00 ff 78 6d 6c 5c 0a 3c 3f 6c 3f 3e   >.....xml\.<?l?>
Seed 3 (id=b662d817d5ab9bb6, size=220 bytes, fuzzer=grimoire, trial=1, discovered_at=13735s, mutation_op=BytesDeleteMutator,ByteDecMutator):
  0000: 77 77 6b 27 20 78 6c 69 6e 6b 20 28 65 29 20 27   wwk' xlink (e) '
  0010: 27 20 6e 6b 3a 68 72 65 66 20 43 44 41 54 41 20   ' nk:href CDATA 
  0020: 23 49 4d 50 4c 49 45 44 3e 9f 86 06 37 6d 6c 5c   #IMPLIED>...7ml\
  0030: 0a 3c 3f 6c 3f 3e 3c 21 44 4f 43 54 59 50 45 61   .<?l?><!DOCTYPEa

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=6f437bf6be6c86ba, size=557 bytes, fuzzer=cmplog, trial=1, discovered_at=80851s, mutation_op=DwordInterestingMutator,CrossoverInsertMutator):
  0000: 2f 2f 2b 27 2f 2a 3a 27 2a 66 66 28 2f 2f 2b 27   //+'/*:'*ff(//+'
  0010: 2f 2a 2a 3a 27 2a 66 66 2b 2f 2f 2b 27 2f 2a 2f   /**:'*ff+//+'/*/
  0020: 2f 2f 2b 27 2f 2a 3a 27 2a 66 66 28 2f 2f 2b 27   //+'/*:'*ff(//+'
  0030: 2f 2a 2a 3a 27 2a 66 66 2b 2f 2f 2b 27 2f 2a 2f   /**:'*ff+//+'/*/


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  d8(.)x1 49(I)x1 77(w)x1             2f(/)x1                             DIFFER
   0x0001  3e(>)x1 53(S)x1 77(w)x1             2f(/)x1                             DIFFER
   0x0002  42(B)x1 4f(O)x1 6b(k)x1             2b(+)x1                             DIFFER
   0x0003  0f(.)x1 2d(-)x1 27(')x1             27(')x1                             PARTIAL
   0x0004  6c(l)x1 38(8)x1 20( )x1             2f(/)x1                             DIFFER
   0x0005  5c(\)x1 38(8)x1 78(x)x1             2a(*)x1                             DIFFER
   0x0006  0a(.)x1 35(5)x1 6c(l)x1             3a(:)x1                             DIFFER
   0x0007  3c(<)x1 39(9)x1 69(i)x1             27(')x1                             DIFFER
   0x0008  3f(?)x1 2d(-)x1 6e(n)x1             2a(*)x1                             DIFFER
   0x0009  6c(l)x1 34(4)x1 6b(k)x1             66(f)x1                             DIFFER
   0x000a  20( )x2 00(.)x1                     66(f)x1                             DIFFER
   0x000b  3f(?)x1 00(.)x1 28(()x1             28(()x1                             PARTIAL
   0x000c  3e(>)x1 6d(m)x1 65(e)x1             2f(/)x1                             DIFFER
   0x000d  3c(<)x1 6c(l)x1 29())x1             2f(/)x1                             DIFFER
   0x000e  21(!)x1 5c(\)x1 20( )x1             2b(+)x1                             DIFFER
   0x000f  44(D)x1 0a(.)x1 27(')x1             27(')x1                             PARTIAL
   0x0010  4f(O)x1 3c(<)x1 27(')x1             2f(/)x1                             DIFFER
   0x0011  43(C)x1 3f(?)x1 20( )x1             2a(*)x1                             DIFFER
   0x0012  54(T)x1 78(x)x1 6e(n)x1             2a(*)x1                             DIFFER
   0x0013  59(Y)x1 6d(m)x1 6b(k)x1             3a(:)x1                             DIFFER
   0x0014  50(P)x1 6c(l)x1 3a(:)x1             27(')x1                             DIFFER
   0x0015  45(E)x1 20( )x1 68(h)x1             2a(*)x1                             DIFFER
   0x0016  61(a)x1 3e(>)x1 72(r)x1             66(f)x1                             DIFFER
   0x0017  20( )x1 3c(<)x1 65(e)x1             66(f)x1                             DIFFER
   0x0018  53(S)x1 62(b)x1 66(f)x1             2b(+)x1                             DIFFER
   0x0019  20( )x2 59(Y)x1                     2f(/)x1                             DIFFER
   0x001a  53(S)x1 78(x)x1 43(C)x1             2f(/)x1                             DIFFER
   0x001b  54(T)x1 6d(m)x1 44(D)x1             2b(+)x1                             DIFFER
   0x001c  45(E)x1 6c(l)x1 41(A)x1             27(')x1                             DIFFER
   0x001d  4d(M)x1 6e(n)x1 54(T)x1             2f(/)x1                             DIFFER
   0x001e  20( )x1 73(s)x1 41(A)x1             2a(*)x1                             DIFFER
   0x001f  22(")x1 3a(:)x1 20( )x1             2f(/)x1                             DIFFER
   0x0020  64(d)x1 66(f)x1 23(#)x1             2f(/)x1                             DIFFER
   0x0021  74(t)x1 3d(=)x1 49(I)x1             2f(/)x1                             DIFFER
   0x0022  64(d)x1 22(")x1 4d(M)x1             2b(+)x1                             DIFFER
   0x0023  73(s)x1 22(")x1 50(P)x1             27(')x1                             DIFFER
   0x0024  2f(/)x1 3e(>)x1 4c(L)x1             2f(/)x1                             PARTIAL
   0x0025  31(1)x1 74(t)x1 49(I)x1             2a(*)x1                             DIFFER
   0x0026  32(2)x1 64(d)x1 45(E)x1             3a(:)x1                             DIFFER
   0x0027  37(7)x1 5c(\)x1 44(D)x1             27(')x1                             DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6210.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6210,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6210 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6210 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6210 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).