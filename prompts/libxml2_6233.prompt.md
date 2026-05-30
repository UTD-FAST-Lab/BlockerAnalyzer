==== BLOCKER ====
Target: libxml2
Branch ID: 6233
Location: /src/libxml2/SAX2.c:1415:6
Enclosing function: SAX2.c:xmlSAX2AttributeInternal
Source line: 	if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  REFERENCE
cmplog                           4        6          0  REFERENCE
value_profile                    0       10          0  loser (I2S vs value_profile_cmplog)
value_profile_cmplog            10        0          0  winner (I2S vs value_profile)
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         3        7          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['value_profile', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > value_profile  [delta: I2S] ---
  subject 34  (value_profile_cmplog vs value_profile, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=11.10h  loser=23.90h
  avg hitcount on branch: winner=38  loser=0
  prob_div=1.00  dur_div=12.80h  hit_div=38
  subject-level: delta_AUC=30627000.0  p_AUC=0.0376  delta_Final=430.2  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/6233/{W,L}/branch_coverage_show.txt

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
[L]  1307  	    xmlNsErrMsg(ctxt, XML_NS_ERR_UNDEFINED_NAMESPACE,
[L]  1308  		    "Namespace prefix %s of attribute %s is not defined\n",
[L]  1309  		             ns, name);
[B]  1310  	} else {
[W]  1311              xmlAttrPtr prop;
[ ]  1312  
[W]  1313              prop = ctxt->node->properties;
[W]  1314              while (prop != NULL) {
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
[W]  1331          }
[B]  1332      } else {
[L]  1333  	namespace = NULL;
[L]  1334      }
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
[B]  1415  	if (xmlStrEqual(fullname, BAD_CAST "xml:id")) { <-- BLOCKER
[ ]  1416  	    /*
[ ]  1417  	     * Add the xml:id value
[ ]  1418  	     *
[ ]  1419  	     * Open issue: normalization of the value.
[ ]  1420  	     */
[W]  1421  	    if (xmlValidateNCName(content, 1) != 0) {
[W]  1422  	        xmlErrValid(ctxt, XML_DTD_XMLID_VALUE,
[W]  1423  		      "xml:id : attribute value %s is not an NCName\n",
[W]  1424  			    (const char *) content, NULL);
[W]  1425  	    }
[W]  1426  	    xmlAddID(&ctxt->vctxt, ctxt->myDoc, content, ret);
[B]  1427  	} else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
[ ]  1428  	    xmlAddID(&ctxt->vctxt, ctxt->myDoc, content, ret);
[L]  1429  	else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
[ ]  1430  	    xmlAddRef(&ctxt->vctxt, ctxt->myDoc, content, ret);
[B]  1431      }
[ ]  1432  
[B]  1433  error:
[B]  1434      if (nval != NULL)
[ ]  1435  	xmlFree(nval);
[B]  1436      if (ns != NULL)
[B]  1437  	xmlFree(ns);
[B]  1438  }

--- Caller (1 hop): xmlSAX2StartElement (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1773) (±10 around call site) ---
[B]  1763  	if (ctxt->html) {
[ ]  1764  	    while (att != NULL) {
[ ]  1765  		xmlSAX2AttributeInternal(ctxt, att, value, NULL);
[ ]  1766  		att = atts[i++];
[ ]  1767  		value = atts[i++];
[ ]  1768  	    }
[B]  1769  	} else {
[B]  1770  	    while ((att != NULL) && (value != NULL)) {
[B]  1771  		if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
[B]  1772  		    (att[3] != 'n') || (att[4] != 's'))
[B]  1773  		    xmlSAX2AttributeInternal(ctxt, att, value, NULL); <-- CALL
[ ]  1774  
[ ]  1775  		/*
[ ]  1776  		 * Next ones
[ ]  1777  		 */
[B]  1778  		att = atts[i++];
[B]  1779  		value = atts[i++];
[B]  1780  	    }
[B]  1781  	}
[B]  1782      }
[ ]  1783  

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 2  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      69       222  SAX2.c:xmlSAX2Text  (/src/libxml2/SAX2.c:2547-2671)
      69       222  xmlSAX2Characters  (/src/libxml2/SAX2.c:2683-2685)
      27       118  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806)
      24        86  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
       0        40  xmlSAX2EndElement  (/src/libxml2/SAX2.c:1817-1854)
       0        18  SAX2.c:xmlNsErrMsg  (/src/libxml2/SAX2.c:1070-1080)
       0        17  xmlSAX2IgnorableWhitespace  (/src/libxml2/SAX2.c:2698-2704)
      15         0  xmlSAX2ProcessingInstruction  (/src/libxml2/SAX2.c:2717-2769)
       0        12  SAX2.c:xmlNsWarnMsg  (/src/libxml2/SAX2.c:194-204)
      15         3  xmlSAX2InternalSubset  (/src/libxml2/SAX2.c:330-354)
      15         3  xmlSAX2ExternalSubset  (/src/libxml2/SAX2.c:368-496)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806) ---
  d=2   L1614  T=0 F=27  T=0 F=118  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=2   L1614  T=0 F=27  T=0 F=118  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=2   L1614  T=0 F=27  T=0 F=118  if ((ctx == NULL) || (fullname == NULL) || (ctxt->myDoc =...
  d=2   L1624  T=15 F=12  T=21 F=97  if (ctxt->validate && (ctxt->myDoc->extSubset == NULL) &&
  d=2   L1625  T=0 F=15  T=18 F=3  ((ctxt->myDoc->intSubset == NULL) ||
  d=2   L1626  T=15 F=0  T=3 F=0  ((ctxt->myDoc->intSubset->notations == NULL) &&
  d=2   L1627  T=15 F=0  T=3 F=0  (ctxt->myDoc->intSubset->elements == NULL) &&
  d=2   L1628  T=15 F=0  T=3 F=0  (ctxt->myDoc->intSubset->attributes == NULL) &&
  d=2   L1629  T=15 F=0  T=3 F=0  (ctxt->myDoc->intSubset->entities == NULL)))) {
  d=2   L1648  T=0 F=27  T=0 F=118  if (ret == NULL) {
  d=2   L1654  T=0 F=27  T=27 F=91  if (ctxt->myDoc->children == NULL) {
  d=2   L1659  T=15 F=12  T=21 F=70  } else if (parent == NULL) {
  d=2   L1663  T=27 F=0  T=118 F=0  if (ctxt->linenumbers) {
  d=2   L1664  T=27 F=0  T=118 F=0  if (ctxt->input != NULL) {
  d=2   L1665  T=27 F=0  T=118 F=0  if ((unsigned) ctxt->input->line < (unsigned) USHRT_MAX)
  d=2   L1678  T=0 F=27  T=0 F=118  if (nodePush(ctxt, ret) < 0) {
  d=2   L1689  T=27 F=0  T=91 F=27  if (parent != NULL) {
  d=2   L1690  T=12 F=15  T=88 F=3  if (parent->type == XML_ELEMENT_NODE) {
  d=2   L1706  T=27 F=0  T=118 F=0  if (!ctxt->html) {
  d=2   L1711  T=27 F=0  T=26 F=92  if ((ctxt->myDoc->intSubset != NULL) ||
  d=2   L1712  T=0 F=0  T=0 F=92  (ctxt->myDoc->extSubset != NULL)) {
  d=2   L1719  T=12 F=15  T=30 F=88  if (atts != NULL) {
  d=2   L1723  T=12 F=0  T=32 F=0  while ((att != NULL) && (value != NULL)) {
  d=2   L1723  T=12 F=12  T=32 F=30  while ((att != NULL) && (value != NULL)) {
  d=2   L1724  T=12 F=0  T=0 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1724  T=12 F=0  T=0 F=27  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1724  T=12 F=0  T=27 F=5  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=2   L1725  T=0 F=12  T=0 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=2   L1738  T=27 F=0  T=91 F=27  if ((ns == NULL) && (parent != NULL))
  d=2   L1738  T=27 F=0  T=118 F=0  if ((ns == NULL) && (parent != NULL))
  d=2   L1740  T=0 F=27  T=12 F=106  if ((prefix != NULL) && (ns == NULL)) {
  d=2   L1740  T=0 F=0  T=12 F=0  if ((prefix != NULL) && (ns == NULL)) {
  d=2   L1751  T=0 F=27  T=12 F=106  if ((ns != NULL) && (ns->href != NULL) &&
  d=2   L1751  T=0 F=0  T=0 F=12  if ((ns != NULL) && (ns->href != NULL) &&
  d=2   L1759  T=12 F=15  T=30 F=88  if (atts != NULL) {
  d=2   L1763  T=0 F=12  T=0 F=30  if (ctxt->html) {
  d=2   L1770  T=12 F=12  T=32 F=30  while ((att != NULL) && (value != NULL)) {
  d=2   L1770  T=12 F=0  T=32 F=0  while ((att != NULL) && (value != NULL)) {
  d=2   L1771  T=0 F=12  T=0 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1771  T=0 F=12  T=27 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1771  T=0 F=12  T=5 F=27  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=2   L1772  T=12 F=0  T=0 F=0  (att[3] != 'n') || (att[4] != 's'))
  d=2   L1789  T=0 F=27  T=0 F=118  if ((ctxt->validate) &&
  d=2   L1803  T=0 F=27  T=12 F=106  if (prefix != NULL)
--- d=1  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=1   L1105  T=0 F=12  T=0 F=32  if (ctxt->html) {
  d=1   L1114  T=12 F=0  T=32 F=0  if ((name != NULL) && (name[0] == 0)) {
  d=1   L1114  T=0 F=12  T=0 F=32  if ((name != NULL) && (name[0] == 0)) {
  d=1   L1131  T=0 F=12  T=0 F=32  if (name == NULL) {
  d=1   L1139  T=0 F=12  T=0 F=32  if ((ctxt->html) &&
  d=1   L1156  T=0 F=12  T=0 F=32  if (ctxt->vctxt.valid != 1) {
  d=1   L1159  T=0 F=12  T=0 F=32  if (nval != NULL)
  d=1   L1169  T=0 F=12  T=14 F=18  if ((!ctxt->html) && (ns == NULL) &&
  d=1   L1169  T=12 F=0  T=32 F=0  if ((!ctxt->html) && (ns == NULL) &&
  d=1   L1170  T=0 F=0  T=9 F=5  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=1   L1170  T=0 F=0  T=0 F=9  (name[0] == 'x') && (name[1] == 'm') && (name[2] == 'l') &&
  d=1   L1234  T=12 F=0  T=32 F=0  if ((!ctxt->html) &&
  d=1   L1235  T=12 F=0  T=0 F=18  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=1   L1235  T=12 F=0  T=0 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=1   L1235  T=12 F=0  T=18 F=14  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=1   L1236  T=0 F=12  T=0 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=1   L1303  T=12 F=0  T=18 F=14  if (ns != NULL) {
  d=1   L1306  T=0 F=12  T=18 F=0  if (namespace == NULL) {
  d=1   L1314  T=0 F=12  T=0 F=0  while (prop != NULL) {
  d=1   L1338  T=0 F=12  T=0 F=32  if (ret == NULL)
  d=1   L1341  T=0 F=0  T=5 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=1   L1341  T=0 F=12  T=5 F=27  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=1   L1346  T=0 F=0  T=5 F=5  while (tmp != NULL) {
  d=1   L1348  T=0 F=0  T=5 F=0  if (tmp->next == NULL)
  d=1   L1352  T=12 F=0  T=27 F=0  } else if (value != NULL) {
  d=1   L1355  T=12 F=0  T=27 F=0  if (ret->children != NULL)
  d=1   L1360  T=0 F=12  T=0 F=32  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1360  T=12 F=0  T=32 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=1   L1403  T=12 F=0  T=32 F=0  if (((ctxt->loadsubset & XML_SKIP_IDS) == 0) &&
  d=1   L1404  T=0 F=12  T=5 F=27  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=1   L1404  T=0 F=0  T=5 F=0  (((ctxt->replaceEntities == 0) && (ctxt->external != 2)) ||
  d=1   L1405  T=12 F=0  T=27 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L1405  T=12 F=0  T=27 F=0  ((ctxt->replaceEntities != 0) && (ctxt->inSubset == 0))) &&
  d=1   L1407  T=12 F=0  T=32 F=0  (ret->children != NULL) &&
  d=1   L1408  T=12 F=0  T=32 F=0  (ret->children->type == XML_TEXT_NODE) &&
  d=1   L1409  T=12 F=0  T=32 F=0  (ret->children->next == NULL)) {
  d=1   L1415  T=12 F=0  T=0 F=32  if (xmlStrEqual(fullname, BAD_CAST "xml:id")) {  <-- BLOCKER
  d=1   L1421  T=12 F=0  T=0 F=0  if (xmlValidateNCName(content, 1) != 0) {
  d=1   L1427  T=0 F=0  T=0 F=32  } else if (xmlIsID(ctxt->myDoc, ctxt->node, ret))
  d=1   L1429  T=0 F=0  T=0 F=32  else if (xmlIsRef(ctxt->myDoc, ctxt->node, ret))
  d=1   L1434  T=0 F=12  T=0 F=32  if (nval != NULL)
  d=1   L1436  T=12 F=0  T=18 F=14  if (ns != NULL)

[off-chain: 67 additional divergent branches across 10 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=c20581314eb72916, size=307 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=36030s, mutation_op=ByteRandMutator,QwordAddMutator,BytesSwapMutator,WordInterestingMutator,BytesRandInsertMutator,ByteNegMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   72.xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 26 37 37 32 2e 64 3a    ".:d./12&772.d:
Seed 2 (id=168e9a373a411e74, size=333 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=53552s, mutation_op=ByteRandMutator,BytesCopyMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   72.xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 5d 37 37 32 2e 64 3a    ".:d./12]772.d:
Seed 3 (id=c0f4fb619d9e55cd, size=345 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=53552s, mutation_op=WordAddMutator,ByteFlipMutator,WordInterestingMutator,WordInterestingMutator,ByteFlipMutator,BytesRandInsertMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 0a 6c 3a 76 65   72.xml\.<?x.l:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 3c 3f 3e 0a 3c 21   rsion="1.0<?>.<!
  0020: 44 4f 43 54 59 50 45 3a 61 00 3c 59 53 54 45 3e   DOCTYPE:a.<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 5d 37 37 32 2e 64 3a    ".:d./12]772.d:
Seed 4 (id=46534405fa42067d, size=115 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=61859s, mutation_op=BytesSetMutator,BytesRandInsertMutator,ByteRandMutator,BitFlipMutator,BytesCopyMutator,WordAddMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 3a 76 65   72.xml\.<?xml:ve
  0010: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 3a 70 26 3c 59 53 54 45 3e   DOCTYPE:p&<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 26 37 37 32 2e 64 3a    ".:d./12&772.d:
Seed 5 (id=0093d6d1c62c278e, size=122 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=79334s, mutation_op=BytesRandSetMutator,BytesRandInsertMutator,ByteAddMutator):
  0000: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 3a 76 65   72.xml\.<?xml:ve
  0010: 72 73 56 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsVon="1.0"?>.<!
  0020: 44 4f 43 54 59 50 45 3a 70 26 3c 59 53 54 45 3e   DOCTYPE:p&<YSTE>
  0030: 20 22 00 3a 64 0a 2f 31 32 26 37 37 32 2e 64 3a    ".:d./12&772.d:

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=075f3886887037b7, size=369 bytes, fuzzer=value_profile, trial=1, discovered_at=1088s, mutation_op=DwordAddMutator,TokenInsert,ByteAddMutator,BitFlipMutator):
  0000: 77 77 2e 77 fe ff ff ff 33 2e 6f 72 67 2f 31 2f   ww.w....3.org/1/
  0010: 2f 2f 2f 2f 2f 2f 2f 2f 2f 2f 20 20 20 20 20 20   //////////      
  0020: 20 20 20 20 20 20 78 6c 69 6e 6b 3a 74 79 70 65         xlink:type
  0030: 20 20 20 28 73 69 6d 70 6c 65 29 20 20 23 46 49      (simple)  #FI
Seed 2 (id=0dbb09534c8db0ab, size=438 bytes, fuzzer=value_profile, trial=1, discovered_at=1116s, mutation_op=ByteDecMutator,ByteFlipMutator,ByteFlipMutator,CrossoverInsertMutator):
  0000: 31 32 37 37 37 32 2e 64 aa aa aa aa aa aa aa aa   127772.d........
  0010: 2f 31 32 37 37 37 32 2e 64 74 64 22 3e 0a 0a 3b   /127772.dtd">..;
  0020: 61 3e 0a 20 64 73 2f cf 32 64 00 00 00 2e 64 74   a>. ds/.2d....dt
  0030: 64 5c 0a 3c 6e 6b 3a 74 79 70 65 76 65 72 73 69   d\.<nk:typeversi
Seed 3 (id=0418896bc4e3a59f, size=508 bytes, fuzzer=value_profile, trial=1, discovered_at=1755s, mutation_op=BytesExpandMutator,BytesInsertMutator,ByteDecMutator):
  0000: 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21 44 4f 43   on="1.0"?>.<!DOC
  0010: 54 59 50 45 e0 6d 6d 20 20 77 20 43 44 41 54 41   TYPE.mm  w CDATA
  0020: 20 20 20 20 20 23 49 4d 50 4c 49 45 44 3e 0a 0a        #IMPLIED>..
  0030: 5c 0a 3c 61 3e 0a 20 20 3c 62 20 78 6c 69 6e 6b   \.<a>.  <b xlink
Seed 4 (id=2162db13540e853c, size=235 bytes, fuzzer=value_profile, trial=1, discovered_at=1835s, mutation_op=BytesInsertMutator,BytesRandSetMutator):
  0000: 73 2f cf 32 37 37 37 32 2e 64 74 64 5c 0a 3c 6e   s/.27772.dtd\.<n
  0010: 6b 3a 74 79 70 65 21 45 4c 45 4d 29 3e 0a 0a 3c   k:type!ELEM)>..<
  0020: 21 54 54 54 54 54 54 54 54 45 4c 9c 45 41 20 20   !TTTTTTTTEL.EA  
  0030: 20 20 20 20 20 20 20 78 6c 69 6e 6b 3a 68 72 65          xlink:hre
Seed 5 (id=08aa863e68a012de, size=116 bytes, fuzzer=value_profile, trial=1, discovered_at=2742s, mutation_op=QwordAddMutator,BytesCopyMutator):
  0000: 37 37 32 2e 78 6d 6c 5c 0a 3c c3 78 6d 6c 20 76   772.xml\.<.xml v
  0010: 65 72 73 69 6f fa fa fa fa fa fa fa fa fa fa fa   ersio...........
  0020: fa fa fa 6e 6c 20 76 65 72 73 69 6f fa fa fa fa   ...nl versio....
  0030: fa fa fa fa fa fa fa fa fa fa 6e 3d 22 41 3e 0a   ..........n="A>.


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  37(7)x5                             77(w)x2 6f(o)x2 73(s)x2 37(7)x2 +2u  PARTIAL
   0x0001  32(2)x5                             6e(n)x3 77(w)x2 2f(/)x2 37(7)x2 +1u  PARTIAL
   0x0002  2e(.)x5                             2e(.)x2 37(7)x2 3d(=)x2 cf(.)x2 +2u  PARTIAL
   0x0003  78(x)x5                             77(w)x2 22(")x2 32(2)x2 37(7)x1 +3u  DIFFER
   0x0004  6d(m)x5                             fe(.)x2 37(7)x2 31(1)x2 78(x)x1 +3u  DIFFER
   0x0005  6c(l)x5                             ff(.)x2 32(2)x2 2e(.)x2 37(7)x1 +3u  DIFFER
   0x0006  5c(\)x5                             ff(.)x2 30(0)x2 37(7)x2 2e(.)x1 +3u  DIFFER
   0x0007  0a(.)x5                             ff(.)x2 22(")x2 64(d)x1 32(2)x1 +4u  DIFFER
   0x0008  3c(<)x5                             33(3)x2 3f(?)x2 aa(.)x1 2e(.)x1 +4u  DIFFER
   0x0009  3f(?)x5                             2e(.)x2 3e(>)x2 aa(.)x1 64(d)x1 +4u  DIFFER
   0x000a  78(x)x5                             6f(o)x2 0a(.)x2 aa(.)x1 74(t)x1 +4u  DIFFER
   0x000b  0a(.)x3 6d(m)x2                     72(r)x2 3c(<)x2 64(d)x2 aa(.)x1 +3u  DIFFER
   0x000c  6c(l)x5                             67(g)x2 21(!)x2 aa(.)x1 5c(\)x1 +4u  DIFFER
   0x000d  3a(:)x5                             2f(/)x3 44(D)x2 aa(.)x1 0a(.)x1 +3u  DIFFER
   0x000e  76(v)x5                             31(1)x2 4f(O)x2 aa(.)x1 3c(<)x1 +4u  DIFFER
   0x000f  65(e)x5                             2f(/)x3 43(C)x2 aa(.)x1 6e(n)x1 +3u  DIFFER
   0x0010  72(r)x5                             2f(/)x3 54(T)x2 6b(k)x1 65(e)x1 +3u  DIFFER
   0x0011  73(s)x5                             2f(/)x2 59(Y)x2 31(1)x1 3a(:)x1 +4u  DIFFER
   0x0012  69(i)x4 56(V)x1                     2f(/)x2 50(P)x2 32(2)x1 74(t)x1 +4u  DIFFER
   0x0013  6f(o)x5                             2f(/)x2 45(E)x2 37(7)x1 79(y)x1 +4u  DIFFER
   0x0014  6e(n)x5                             2f(/)x2 e0(.)x2 37(7)x1 70(p)x1 +4u  DIFFER
   0x0015  3d(=)x5                             2f(/)x2 6d(m)x2 37(7)x1 65(e)x1 +4u  DIFFER
   0x0016  22(")x5                             2f(/)x2 6d(m)x2 32(2)x1 21(!)x1 +4u  DIFFER
   0x0017  31(1)x5                             2f(/)x2 20( )x2 2e(.)x1 45(E)x1 +4u  DIFFER
   0x0018  2e(.)x5                             2f(/)x2 20( )x2 64(d)x1 4c(L)x1 +4u  DIFFER
   0x0019  30(0)x5                             2f(/)x2 77(w)x2 45(E)x2 74(t)x1 +3u  DIFFER
   0x001a  3c(<)x3 22(")x2                     20( )x4 64(d)x1 4d(M)x1 fa(.)x1 +3u  DIFFER
   0x001b  3f(?)x5                             20( )x2 43(C)x2 22(")x1 29())x1 +4u  DIFFER
   0x001c  3e(>)x5                             20( )x3 3e(>)x2 44(D)x2 fa(.)x1 +2u  PARTIAL
   0x001d  0a(.)x5                             20( )x3 0a(.)x2 41(A)x2 fa(.)x1 +2u  PARTIAL
   0x001e  3c(<)x5                             20( )x2 0a(.)x2 54(T)x2 3e(>)x2 +2u  PARTIAL
   0x001f  21(!)x5                             20( )x2 41(A)x2 0a(.)x2 3b(;)x1 +3u  DIFFER
   0x0020  44(D)x5                             20( )x5 61(a)x1 21(!)x1 fa(.)x1 +2u  DIFFER
   0x0021  4f(O)x5                             20( )x4 3e(>)x1 54(T)x1 fa(.)x1 +3u  DIFFER
   0x0022  43(C)x5                             20( )x4 0a(.)x1 54(T)x1 fa(.)x1 +3u  DIFFER
   0x0023  54(T)x5                             20( )x4 54(T)x2 6e(n)x1 e4(.)x1 +2u  PARTIAL
   0x0024  59(Y)x5                             20( )x4 54(T)x2 64(d)x1 6c(l)x1 +2u  DIFFER
   0x0025  50(P)x5                             20( )x3 54(T)x3 23(#)x2 73(s)x1 +1u  DIFFER
   0x0026  45(E)x5                             78(x)x2 49(I)x2 59(Y)x2 2f(/)x1 +3u  DIFFER
   0x0027  3a(:)x5                             6c(l)x2 4d(M)x2 54(T)x2 cf(.)x1 +3u  DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_6233.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 6233,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 6233 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 6233 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 6233 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).