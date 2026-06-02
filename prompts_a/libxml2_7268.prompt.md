==== BLOCKER ====
Target: libxml2
Branch ID: 7268
Location: /src/libxml2/xmlreader.c:1328:13
Enclosing function: xmlTextReaderRead
Source line:             (reader->node->type == XML_ELEMENT_NODE) &&
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            1        9          0  REFERENCE
cmplog                           0       10          0  loser (grimoire_structural vs grimoire)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog             3        7          0  REFERENCE
naive_ctx                        1        9          0  REFERENCE
naive_ngram4                     0       10          0  REFERENCE
mopt                             0       10          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                        10        0          0  winner (grimoire_structural vs cmplog)

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'grimoire']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast']

==== DECISIVE PAIRS (1) ====
--- Pair 1: grimoire > cmplog  [delta: grimoire_structural] ---
  subject 40  (grimoire vs cmplog, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=5.60h  loser=24.00h
  avg hitcount on branch: winner=15  loser=0
  prob_div=1.00  dur_div=18.40h  hit_div=15
  subject-level: delta_AUC=46408860.0  p_AUC=0.0003  delta_Final=376.7  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/7268/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlTextReaderRead (/src/libxml2/xmlreader.c:1219-1538) ---
[ ]  1217   */
[ ]  1218  int
[B]  1219  xmlTextReaderRead(xmlTextReaderPtr reader) {
[B]  1220      int val, olddepth = 0;
[B]  1221      xmlTextReaderState oldstate = XML_TEXTREADER_START;
[B]  1222      xmlNodePtr oldnode = NULL;
[ ]  1223  
[ ]  1224  
[B]  1225      if (reader == NULL)
[ ]  1226  	return(-1);
[B]  1227      reader->curnode = NULL;
[B]  1228      if (reader->doc != NULL)
[ ]  1229          return(xmlTextReaderReadTree(reader));
[B]  1230      if (reader->ctxt == NULL)
[ ]  1231  	return(-1);
[ ]  1232  
[ ]  1233  #ifdef DEBUG_READER
[ ]  1234      fprintf(stderr, "\nREAD ");
[ ]  1235      DUMP_READER
[ ]  1236  #endif
[B]  1237      if (reader->mode == XML_TEXTREADER_MODE_INITIAL) {
[B]  1238  	reader->mode = XML_TEXTREADER_MODE_INTERACTIVE;
[ ]  1239  	/*
[ ]  1240  	 * Initial state
[ ]  1241  	 */
[B]  1242  	do {
[B]  1243  	    val = xmlTextReaderPushData(reader);
[B]  1244  		if (val < 0){
[ ]  1245  			reader->mode = XML_TEXTREADER_MODE_ERROR;
[ ]  1246  			reader->state = XML_TEXTREADER_ERROR;
[ ]  1247  		return(-1);
[ ]  1248  		}
[B]  1249  	} while ((reader->ctxt->node == NULL) &&
[B]  1250  		 ((reader->mode != XML_TEXTREADER_MODE_EOF) &&
[ ]  1251  		  (reader->state != XML_TEXTREADER_DONE)));
[B]  1252  	if (reader->ctxt->node == NULL) {
[ ]  1253  	    if (reader->ctxt->myDoc != NULL) {
[ ]  1254  		reader->node = reader->ctxt->myDoc->children;
[ ]  1255  	    }
[ ]  1256  	    if (reader->node == NULL){
[ ]  1257  			reader->mode = XML_TEXTREADER_MODE_ERROR;
[ ]  1258  			reader->state = XML_TEXTREADER_ERROR;
[ ]  1259  		return(-1);
[ ]  1260  		}
[ ]  1261  	    reader->state = XML_TEXTREADER_ELEMENT;
[B]  1262  	} else {
[B]  1263  	    if (reader->ctxt->myDoc != NULL) {
[B]  1264  		reader->node = reader->ctxt->myDoc->children;
[B]  1265  	    }
[B]  1266  	    if (reader->node == NULL)
[ ]  1267  		reader->node = reader->ctxt->nodeTab[0];
[B]  1268  	    reader->state = XML_TEXTREADER_ELEMENT;
[B]  1269  	}
[B]  1270  	reader->depth = 0;
[B]  1271  	reader->ctxt->parseMode = XML_PARSE_READER;
[B]  1272  	goto node_found;
[B]  1273      }
[B]  1274      oldstate = reader->state;
[B]  1275      olddepth = reader->ctxt->nodeNr;
[B]  1276      oldnode = reader->node;
[ ]  1277  
[B]  1278  get_next_node:
[B]  1279      if (reader->node == NULL) {
[ ]  1280  	if (reader->mode == XML_TEXTREADER_MODE_EOF)
[ ]  1281  	    return(0);
[ ]  1282  	else
[ ]  1283  	    return(-1);
[ ]  1284      }
[ ]  1285  
[ ]  1286      /*
[ ]  1287       * If we are not backtracking on ancestors or examined nodes,
[ ]  1288       * that the parser didn't finished or that we aren't at the end
[ ]  1289       * of stream, continue processing.
[ ]  1290       */
[B]  1291      while ((reader->node != NULL) && (reader->node->next == NULL) &&
[B]  1292  	   (reader->ctxt->nodeNr == olddepth) &&
[B]  1293             ((oldstate == XML_TEXTREADER_BACKTRACK) ||
[B]  1294              (reader->node->children == NULL) ||
[B]  1295  	    (reader->node->type == XML_ENTITY_REF_NODE) ||
[B]  1296  	    ((reader->node->children != NULL) &&
[B]  1297  	     (reader->node->children->type == XML_TEXT_NODE) &&
[B]  1298  	     (reader->node->children->next == NULL)) ||
[B]  1299  	    (reader->node->type == XML_DTD_NODE) ||
[B]  1300  	    (reader->node->type == XML_DOCUMENT_NODE) ||
[B]  1301  	    (reader->node->type == XML_HTML_DOCUMENT_NODE)) &&
[B]  1302  	   ((reader->ctxt->node == NULL) ||
[B]  1303  	    (reader->ctxt->node == reader->node) ||
[B]  1304  	    (reader->ctxt->node == reader->node->parent)) &&
[B]  1305  	   (reader->ctxt->instate != XML_PARSER_EOF)) {
[B]  1306  	val = xmlTextReaderPushData(reader);
[B]  1307  	if (val < 0){
[B]  1308  		reader->mode = XML_TEXTREADER_MODE_ERROR;
[B]  1309  		reader->state = XML_TEXTREADER_ERROR;
[B]  1310  	    return(-1);
[B]  1311  	}
[L]  1312  	if (reader->node == NULL)
[ ]  1313  	    goto node_end;
[L]  1314      }
[B]  1315      if (oldstate != XML_TEXTREADER_BACKTRACK) {
[B]  1316  	if ((reader->node->children != NULL) &&
[B]  1317  	    (reader->node->type != XML_ENTITY_REF_NODE) &&
[B]  1318  	    (reader->node->type != XML_XINCLUDE_START) &&
[B]  1319  	    (reader->node->type != XML_DTD_NODE)) {
[B]  1320  	    reader->node = reader->node->children;
[B]  1321  	    reader->depth++;
[B]  1322  	    reader->state = XML_TEXTREADER_ELEMENT;
[B]  1323  	    goto node_found;
[B]  1324  	}
[B]  1325      }
[B]  1326      if (reader->node->next != NULL) {
[B]  1327  	if ((oldstate == XML_TEXTREADER_ELEMENT) &&
[B]  1328              (reader->node->type == XML_ELEMENT_NODE) && <-- BLOCKER
[B]  1329  	    (reader->node->children == NULL) &&
[B]  1330  	    ((reader->node->extra & NODE_IS_EMPTY) == 0)
[B]  1331  #ifdef LIBXML_XINCLUDE_ENABLED
[B]  1332  	    && (reader->in_xinclude <= 0)
[B]  1333  #endif
[B]  1334  	    ) {
[W]  1335  	    reader->state = XML_TEXTREADER_END;
[W]  1336  	    goto node_found;
[W]  1337  	}
[B]  1338  #ifdef LIBXML_REGEXP_ENABLED
[B]  1339  	if ((reader->validate) &&
[B]  1340  	    (reader->node->type == XML_ELEMENT_NODE))
[B]  1341  	    xmlTextReaderValidatePop(reader);
[B]  1342  #endif /* LIBXML_REGEXP_ENABLED */
[B]  1343          if ((reader->preserves > 0) &&
[B]  1344  	    (reader->node->extra & NODE_IS_SPRESERVED))
[ ]  1345  	    reader->preserves--;
[B]  1346  	reader->node = reader->node->next;
[B]  1347  	reader->state = XML_TEXTREADER_ELEMENT;
[ ]  1348  
[ ]  1349  	/*
[ ]  1350  	 * Cleanup of the old node
[ ]  1351  	 */
[B]  1352  	if ((reader->preserves == 0) &&
[B]  1353  #ifdef LIBXML_XINCLUDE_ENABLED
[B]  1354  	    (reader->in_xinclude == 0) &&
[B]  1355  #endif
[B]  1356  	    (reader->entNr == 0) &&
[B]  1357  	    (reader->node->prev != NULL) &&
[B]  1358              (reader->node->prev->type != XML_DTD_NODE)) {
[B]  1359  	    xmlNodePtr tmp = reader->node->prev;
[B]  1360  	    if ((tmp->extra & NODE_IS_PRESERVED) == 0) {
[B]  1361                  if (oldnode == tmp)
[B]  1362                      oldnode = NULL;
[B]  1363  		xmlUnlinkNode(tmp);
[B]  1364  		xmlTextReaderFreeNode(reader, tmp);
[B]  1365  	    }
[B]  1366  	}
[ ]  1367  
[B]  1368  	goto node_found;
[B]  1369      }
[L]  1370      if ((oldstate == XML_TEXTREADER_ELEMENT) &&
[L]  1371  	(reader->node->type == XML_ELEMENT_NODE) &&
[L]  1372  	(reader->node->children == NULL) &&
[L]  1373  	((reader->node->extra & NODE_IS_EMPTY) == 0)) {;
[ ]  1374  	reader->state = XML_TEXTREADER_END;
[ ]  1375  	goto node_found;
[ ]  1376      }
[L]  1377  #ifdef LIBXML_REGEXP_ENABLED
[L]  1378      if ((reader->validate != XML_TEXTREADER_NOT_VALIDATE) && (reader->node->type == XML_ELEMENT_NODE))
[ ]  1379  	xmlTextReaderValidatePop(reader);
[L]  1380  #endif /* LIBXML_REGEXP_ENABLED */
[L]  1381      if ((reader->preserves > 0) &&
[L]  1382  	(reader->node->extra & NODE_IS_SPRESERVED))
[ ]  1383  	reader->preserves--;
[L]  1384      reader->node = reader->node->parent;
[L]  1385      if ((reader->node == NULL) ||
[L]  1386  	(reader->node->type == XML_DOCUMENT_NODE) ||
[L]  1387  	(reader->node->type == XML_HTML_DOCUMENT_NODE)) {
[ ]  1388  	if (reader->mode != XML_TEXTREADER_MODE_EOF) {
[ ]  1389  	    val = xmlParseChunk(reader->ctxt, "", 0, 1);
[ ]  1390  	    reader->state = XML_TEXTREADER_DONE;
[ ]  1391  	    if (val != 0)
[ ]  1392  	        return(-1);
[ ]  1393  	}
[ ]  1394  	reader->node = NULL;
[ ]  1395  	reader->depth = -1;
[ ]  1396  
[ ]  1397  	/*
[ ]  1398  	 * Cleanup of the old node
[ ]  1399  	 */
[ ]  1400  	if ((oldnode != NULL) && (reader->preserves == 0) &&
[ ]  1401  #ifdef LIBXML_XINCLUDE_ENABLED
[ ]  1402  	    (reader->in_xinclude == 0) &&
[ ]  1403  #endif
[ ]  1404  	    (reader->entNr == 0) &&
[ ]  1405  	    (oldnode->type != XML_DTD_NODE) &&
[ ]  1406  	    ((oldnode->extra & NODE_IS_PRESERVED) == 0)) {
[ ]  1407  	    xmlUnlinkNode(oldnode);
[ ]  1408  	    xmlTextReaderFreeNode(reader, oldnode);
[ ]  1409  	}
[ ]  1410  
[ ]  1411  	goto node_end;
[ ]  1412      }
[L]  1413      if ((reader->preserves == 0) &&
[L]  1414  #ifdef LIBXML_XINCLUDE_ENABLED
[L]  1415          (reader->in_xinclude == 0) &&
[L]  1416  #endif
[L]  1417  	(reader->entNr == 0) &&
[L]  1418          (reader->node->last != NULL) &&
[L]  1419          ((reader->node->last->extra & NODE_IS_PRESERVED) == 0)) {
[L]  1420  	xmlNodePtr tmp = reader->node->last;
[L]  1421  	xmlUnlinkNode(tmp);
[L]  1422  	xmlTextReaderFreeNode(reader, tmp);
[L]  1423      }
[L]  1424      reader->depth--;
[L]  1425      reader->state = XML_TEXTREADER_BACKTRACK;
[ ]  1426  
[B]  1427  node_found:
[B]  1428      DUMP_READER
[ ]  1429  
[ ]  1430      /*
[ ]  1431       * If we are in the middle of a piece of CDATA make sure it's finished
[ ]  1432       */
[B]  1433      if ((reader->node != NULL) &&
[B]  1434          (reader->node->next == NULL) &&
[B]  1435          ((reader->node->type == XML_TEXT_NODE) ||
[B]  1436  	 (reader->node->type == XML_CDATA_SECTION_NODE))) {
[L]  1437              if (xmlTextReaderExpand(reader) == NULL)
[L]  1438  	        return -1;
[L]  1439      }
[ ]  1440  
[B]  1441  #ifdef LIBXML_XINCLUDE_ENABLED
[ ]  1442      /*
[ ]  1443       * Handle XInclude if asked for
[ ]  1444       */
[B]  1445      if ((reader->xinclude) && (reader->in_xinclude == 0) &&
[B]  1446          (reader->node != NULL) &&
[B]  1447  	(reader->node->type == XML_ELEMENT_NODE) &&
[B]  1448  	(reader->node->ns != NULL) &&
[B]  1449  	((xmlStrEqual(reader->node->ns->href, XINCLUDE_NS)) ||
[ ]  1450  	 (xmlStrEqual(reader->node->ns->href, XINCLUDE_OLD_NS)))) {
[ ]  1451  	if (reader->xincctxt == NULL) {
[ ]  1452  	    reader->xincctxt = xmlXIncludeNewContext(reader->ctxt->myDoc);
[ ]  1453  	    xmlXIncludeSetFlags(reader->xincctxt,
[ ]  1454  	                        reader->parserFlags & (~XML_PARSE_NOXINCNODE));
[ ]  1455              xmlXIncludeSetStreamingMode(reader->xincctxt, 1);
[ ]  1456  	}
[ ]  1457  	/*
[ ]  1458  	 * expand that node and process it
[ ]  1459  	 */
[ ]  1460  	if (xmlTextReaderExpand(reader) == NULL)
[ ]  1461  	    return -1;
[ ]  1462  	xmlXIncludeProcessNode(reader->xincctxt, reader->node);
[ ]  1463      }
[B]  1464      if ((reader->node != NULL) && (reader->node->type == XML_XINCLUDE_START)) {
[ ]  1465          reader->in_xinclude++;
[ ]  1466  	goto get_next_node;
[ ]  1467      }
[B]  1468      if ((reader->node != NULL) && (reader->node->type == XML_XINCLUDE_END)) {
[ ]  1469          reader->in_xinclude--;
[ ]  1470  	goto get_next_node;
[ ]  1471      }
[B]  1472  #endif
[ ]  1473      /*
[ ]  1474       * Handle entities enter and exit when in entity replacement mode
[ ]  1475       */
[B]  1476      if ((reader->node != NULL) &&
[B]  1477  	(reader->node->type == XML_ENTITY_REF_NODE) &&
[B]  1478  	(reader->ctxt != NULL) && (reader->ctxt->replaceEntities == 1)) {
[ ]  1479  	if ((reader->node->children != NULL) &&
[ ]  1480  	    (reader->node->children->type == XML_ENTITY_DECL) &&
[ ]  1481  	    (reader->node->children->children != NULL)) {
[ ]  1482  	    if (xmlTextReaderEntPush(reader, reader->node) < 0)
[ ]  1483                  goto get_next_node;
[ ]  1484  	    reader->node = reader->node->children->children;
[ ]  1485  	}
[ ]  1486  #ifdef LIBXML_REGEXP_ENABLED
[B]  1487      } else if ((reader->node != NULL) &&
[B]  1488  	       (reader->node->type == XML_ENTITY_REF_NODE) &&
[B]  1489  	       (reader->ctxt != NULL) && (reader->validate)) {
[ ]  1490  	xmlTextReaderValidateEntity(reader);
[ ]  1491  #endif /* LIBXML_REGEXP_ENABLED */
[ ]  1492      }
[B]  1493      if ((reader->node != NULL) &&
[B]  1494  	(reader->node->type == XML_ENTITY_DECL) &&
[B]  1495  	(reader->ent != NULL) && (reader->ent->children == reader->node)) {
[ ]  1496  	reader->node = xmlTextReaderEntPop(reader);
[ ]  1497  	reader->depth++;
[ ]  1498          goto get_next_node;
[ ]  1499      }
[B]  1500  #ifdef LIBXML_REGEXP_ENABLED
[B]  1501      if ((reader->validate != XML_TEXTREADER_NOT_VALIDATE) && (reader->node != NULL)) {
[B]  1502  	xmlNodePtr node = reader->node;
[ ]  1503  
[B]  1504  	if ((node->type == XML_ELEMENT_NODE) &&
[B]  1505              ((reader->state != XML_TEXTREADER_END) &&
[B]  1506  	     (reader->state != XML_TEXTREADER_BACKTRACK))) {
[B]  1507  	    xmlTextReaderValidatePush(reader);
[B]  1508  	} else if ((node->type == XML_TEXT_NODE) ||
[B]  1509  		   (node->type == XML_CDATA_SECTION_NODE)) {
[B]  1510              xmlTextReaderValidateCData(reader, node->content,
[B]  1511  	                               xmlStrlen(node->content));
[B]  1512  	}
[B]  1513      }
[B]  1514  #endif /* LIBXML_REGEXP_ENABLED */
[B]  1515  #ifdef LIBXML_PATTERN_ENABLED
[B]  1516      if ((reader->patternNr > 0) && (reader->state != XML_TEXTREADER_END) &&
[B]  1517          (reader->state != XML_TEXTREADER_BACKTRACK)) {
[ ]  1518          int i;
[ ]  1519  	for (i = 0;i < reader->patternNr;i++) {
[ ]  1520  	     if (xmlPatternMatch(reader->patternTab[i], reader->node) == 1) {
[ ]  1521  	         xmlTextReaderPreserve(reader);
[ ]  1522  		 break;
[ ]  1523               }
[ ]  1524  	}
[ ]  1525      }
[B]  1526  #endif /* LIBXML_PATTERN_ENABLED */
[B]  1527  #ifdef LIBXML_SCHEMAS_ENABLED
[B]  1528      if ((reader->validate == XML_TEXTREADER_VALIDATE_XSD) &&
[B]  1529          (reader->xsdValidErrors == 0) &&
[B]  1530  	(reader->xsdValidCtxt != NULL)) {
[ ]  1531  	reader->xsdValidErrors = !xmlSchemaIsValid(reader->xsdValidCtxt);
[ ]  1532      }
[B]  1533  #endif /* LIBXML_PATTERN_ENABLED */
[B]  1534      return(1);
[ ]  1535  node_end:
[ ]  1536      reader->state = XML_TEXTREADER_DONE;
[ ]  1537      return(0);
[B]  1538  }

--- Caller (1 hop): LLVMFuzzerTestOneInput (/src/libxml2/fuzz/xml.c:28-94, calls xmlTextReaderRead at line 79) (±10 around call site) ---
[ ]    69  
[B]    70      xmlParseChunk(ctxt, NULL, 0, 1);
[B]    71      xmlFreeDoc(ctxt->myDoc);
[B]    72      xmlFreeParserCtxt(ctxt);
[ ]    73  
[ ]    74      /* Reader */
[ ]    75  
[B]    76      reader = xmlReaderForMemory(docBuffer, docSize, NULL, NULL, opts);
[B]    77      if (reader == NULL)
[ ]    78          goto exit;
[B]    79      while (xmlTextReaderRead(reader) == 1) { <-- CALL
[B]    80          if (xmlTextReaderNodeType(reader) == XML_ELEMENT_NODE) {
[B]    81              int i, n = xmlTextReaderAttributeCount(reader);
[B]    82              for (i=0; i<n; i++) {
[B]    83                  xmlTextReaderMoveToAttributeNo(reader, i);
[B]    84                  while (xmlTextReaderReadAttributeValue(reader) == 1);
[B]    85              }
[B]    86          }
[B]    87      }
[B]    88      xmlFreeTextReader(reader);
[ ]    89  

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94, calls xmlTextReaderRead at line 79)
hop 2  xmlTextReaderNext  (/src/libxml2/xmlreader.c:1589-1610, calls xmlTextReaderRead at line 1599)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       9        57  xmlTextReaderRead  (/src/libxml2/xmlreader.c:1219-1538)  <-- enclosing
       8        47  xmlTextReaderNodeType  (/src/libxml2/xmlreader.c:2939-2997)
       2        22  xmlreader.c:xmlTextReaderCharacters  (/src/libxml2/xmlreader.c:721-731)
       2        21  xmlreader.c:xmlTextReaderPushData  (/src/libxml2/xmlreader.c:765-872)
       0        15  xmlreader.c:xmlTextReaderStartElementNs  (/src/libxml2/xmlreader.c:664-682)
       4        19  xmlTextReaderAttributeCount  (/src/libxml2/xmlreader.c:2893-2926)
       3        17  xmlreader.c:xmlTextReaderFreeNode  (/src/libxml2/xmlreader.c:386-451)
       3        16  xmlreader.c:xmlTextReaderFreeNodeList  (/src/libxml2/xmlreader.c:291-375)
       1        10  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94)
       1        10  xmlreader.c:xmlTextReaderFreeDoc  (/src/libxml2/xmlreader.c:461-501)
       1        10  xmlNewTextReader  (/src/libxml2/xmlreader.c:2000-2103)
       1        10  xmlFreeTextReader  (/src/libxml2/xmlreader.c:2144-2202)
       1        10  xmlTextReaderClose  (/src/libxml2/xmlreader.c:2219-2254)
       1        10  xmlTextReaderSetup  (/src/libxml2/xmlreader.c:5048-5236)
       1        10  xmlReaderForMemory  (/src/libxml2/xmlreader.c:5361-5377)
... (9 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  LLVMFuzzerTestOneInput  (/src/libxml2/fuzz/xml.c:28-94) ---
  d=2   L  45  T=0 F=1  T=0 F=10  if (docBuffer == NULL)
  d=2   L  59  T=0 F=1  T=0 F=10  if (ctxt == NULL)
  d=2   L  63  T=1 F=1  T=19 F=10  for (consumed = 0; consumed < docSize; consumed += chunkS...
  d=2   L  65  T=0 F=1  T=9 F=10  if (chunkSize > maxChunkSize)
  d=2   L  77  T=0 F=1  T=0 F=10  if (reader == NULL)
  d=2   L  79  T=8 F=1  T=47 F=10  while (xmlTextReaderRead(reader) == 1) {
  d=2   L  80  T=4 F=4  T=19 F=28  if (xmlTextReaderNodeType(reader) == XML_ELEMENT_NODE) {
  d=2   L  82  T=2 F=4  T=6 F=19  for (i=0; i<n; i++) {
  d=2   L  84  T=2 F=2  T=6 F=6  while (xmlTextReaderReadAttributeValue(reader) == 1);
--- d=1  xmlTextReaderRead  (/src/libxml2/xmlreader.c:1219-1538) ---
  d=1   L1225  T=0 F=9  T=0 F=57  if (reader == NULL)
  d=1   L1228  T=0 F=9  T=0 F=57  if (reader->doc != NULL)
  d=1   L1230  T=0 F=9  T=0 F=57  if (reader->ctxt == NULL)
  d=1   L1237  T=1 F=8  T=10 F=47  if (reader->mode == XML_TEXTREADER_MODE_INITIAL) {
  d=1   L1244  T=0 F=1  T=0 F=10  if (val < 0){
  d=1   L1249  T=0 F=1  T=0 F=10  } while ((reader->ctxt->node == NULL) &&
  d=1   L1252  T=0 F=1  T=0 F=10  if (reader->ctxt->node == NULL) {
  d=1   L1263  T=1 F=0  T=10 F=0  if (reader->ctxt->myDoc != NULL) {
  d=1   L1266  T=0 F=1  T=0 F=10  if (reader->node == NULL)
  d=1   L1279  T=0 F=8  T=0 F=47  if (reader->node == NULL) {
  d=1   L1291  T=3 F=5  T=22 F=26  while ((reader->node != NULL) && (reader->node->next == N...
  d=1   L1291  T=8 F=0  T=48 F=0  while ((reader->node != NULL) && (reader->node->next == N...
  d=1   L1292  T=3 F=0  T=22 F=0  (reader->ctxt->nodeNr == olddepth) &&
  d=1   L1293  T=0 F=3  T=1 F=21  ((oldstate == XML_TEXTREADER_BACKTRACK) ||
  d=1   L1294  T=1 F=2  T=6 F=15  (reader->node->children == NULL) ||
  d=1   L1295  T=0 F=2  T=0 F=15  (reader->node->type == XML_ENTITY_REF_NODE) ||
  d=1   L1296  T=2 F=0  T=15 F=0  ((reader->node->children != NULL) &&
  d=1   L1297  T=0 F=2  T=15 F=0  (reader->node->children->type == XML_TEXT_NODE) &&
  d=1   L1298  T=0 F=0  T=7 F=8  (reader->node->children->next == NULL)) ||
  d=1   L1299  T=0 F=2  T=0 F=8  (reader->node->type == XML_DTD_NODE) ||
  d=1   L1300  T=0 F=2  T=0 F=8  (reader->node->type == XML_DOCUMENT_NODE) ||
  d=1   L1301  T=0 F=2  T=0 F=8  (reader->node->type == XML_HTML_DOCUMENT_NODE)) &&
  d=1   L1302  T=0 F=1  T=0 F=14  ((reader->ctxt->node == NULL) ||
  d=1   L1303  T=0 F=1  T=9 F=5  (reader->ctxt->node == reader->node) ||
  d=1   L1304  T=1 F=0  T=1 F=4  (reader->ctxt->node == reader->node->parent)) &&
  d=1   L1305  T=1 F=0  T=10 F=0  (reader->ctxt->instate != XML_PARSER_EOF)) {
  d=1   L1307  T=1 F=0  T=9 F=1  if (val < 0){
  d=1   L1312  T=0 F=0  T=0 F=1  if (reader->node == NULL)
  d=1   L1315  T=7 F=0  T=35 F=3  if (oldstate != XML_TEXTREADER_BACKTRACK) {
  d=1   L1316  T=2 F=5  T=11 F=24  if ((reader->node->children != NULL) &&
  d=1   L1317  T=2 F=0  T=11 F=0  (reader->node->type != XML_ENTITY_REF_NODE) &&
  d=1   L1318  T=2 F=0  T=11 F=0  (reader->node->type != XML_XINCLUDE_START) &&
  d=1   L1319  T=2 F=0  T=11 F=0  (reader->node->type != XML_DTD_NODE)) {
  d=1   L1326  T=5 F=0  T=23 F=4  if (reader->node->next != NULL) {
  d=1   L1327  T=4 F=1  T=20 F=3  if ((oldstate == XML_TEXTREADER_ELEMENT) &&
  d=1   L1328  T=1 F=3  T=0 F=20  (reader->node->type == XML_ELEMENT_NODE) &&  <-- BLOCKER
  d=1   L1329  T=1 F=0  T=0 F=0  (reader->node->children == NULL) &&
  d=1   L1330  T=1 F=0  T=0 F=0  ((reader->node->extra & NODE_IS_EMPTY) == 0)
  d=1   L1332  T=1 F=0  T=0 F=0  && (reader->in_xinclude <= 0)
  d=1   L1339  T=4 F=0  T=5 F=18  if ((reader->validate) &&
  d=1   L1343  T=0 F=4  T=0 F=23  if ((reader->preserves > 0) &&
  d=1   L1352  T=4 F=0  T=23 F=0  if ((reader->preserves == 0) &&
  d=1   L1354  T=4 F=0  T=23 F=0  (reader->in_xinclude == 0) &&
  d=1   L1356  T=4 F=0  T=23 F=0  (reader->entNr == 0) &&
  d=1   L1357  T=4 F=0  T=23 F=0  (reader->node->prev != NULL) &&
  d=1   L1358  T=3 F=1  T=13 F=10  (reader->node->prev->type != XML_DTD_NODE)) {
  d=1   L1360  T=3 F=0  T=13 F=0  if ((tmp->extra & NODE_IS_PRESERVED) == 0) {
  d=1   L1361  T=3 F=0  T=13 F=0  if (oldnode == tmp)
  d=1   L1370  T=0 F=0  T=4 F=0  if ((oldstate == XML_TEXTREADER_ELEMENT) &&
  d=1   L1371  T=0 F=0  T=0 F=4  (reader->node->type == XML_ELEMENT_NODE) &&
  d=1   L1378  T=0 F=0  T=1 F=3  if ((reader->validate != XML_TEXTREADER_NOT_VALIDATE) && ...
  d=1   L1378  T=0 F=0  T=0 F=1  if ((reader->validate != XML_TEXTREADER_NOT_VALIDATE) && ...
  d=1   L1381  T=0 F=0  T=0 F=4  if ((reader->preserves > 0) &&
  d=1   L1385  T=0 F=0  T=0 F=4  if ((reader->node == NULL) ||
  d=1   L1386  T=0 F=0  T=0 F=4  (reader->node->type == XML_DOCUMENT_NODE) ||
  d=1   L1387  T=0 F=0  T=0 F=4  (reader->node->type == XML_HTML_DOCUMENT_NODE)) {
  d=1   L1413  T=0 F=0  T=4 F=0  if ((reader->preserves == 0) &&
  d=1   L1415  T=0 F=0  T=4 F=0  (reader->in_xinclude == 0) &&
  d=1   L1417  T=0 F=0  T=4 F=0  (reader->entNr == 0) &&
  d=1   L1418  T=0 F=0  T=4 F=0  (reader->node->last != NULL) &&
  d=1   L1419  T=0 F=0  T=4 F=0  ((reader->node->last->extra & NODE_IS_PRESERVED) == 0)) {
  d=1   L1433  T=8 F=0  T=48 F=0  if ((reader->node != NULL) &&
  d=1   L1434  T=3 F=5  T=22 F=26  (reader->node->next == NULL) &&
  d=1   L1435  T=0 F=3  T=5 F=17  ((reader->node->type == XML_TEXT_NODE) ||
  d=1   L1436  T=0 F=3  T=0 F=17  (reader->node->type == XML_CDATA_SECTION_NODE))) {
  d=1   L1437  T=0 F=0  T=1 F=4  if (xmlTextReaderExpand(reader) == NULL)
  d=1   L1445  T=0 F=8  T=0 F=47  if ((reader->xinclude) && (reader->in_xinclude == 0) &&
  d=1   L1464  T=0 F=8  T=0 F=47  if ((reader->node != NULL) && (reader->node->type == XML_...
  d=1   L1464  T=8 F=0  T=47 F=0  if ((reader->node != NULL) && (reader->node->type == XML_...
  d=1   L1468  T=8 F=0  T=47 F=0  if ((reader->node != NULL) && (reader->node->type == XML_...
  d=1   L1468  T=0 F=8  T=0 F=47  if ((reader->node != NULL) && (reader->node->type == XML_...
  d=1   L1476  T=8 F=0  T=47 F=0  if ((reader->node != NULL) &&
  d=1   L1477  T=0 F=8  T=0 F=47  (reader->node->type == XML_ENTITY_REF_NODE) &&
  d=1   L1487  T=8 F=0  T=47 F=0  } else if ((reader->node != NULL) &&
  d=1   L1488  T=0 F=8  T=0 F=47  (reader->node->type == XML_ENTITY_REF_NODE) &&
  d=1   L1493  T=8 F=0  T=47 F=0  if ((reader->node != NULL) &&
  d=1   L1494  T=0 F=8  T=0 F=47  (reader->node->type == XML_ENTITY_DECL) &&
  d=1   L1501  T=8 F=0  T=10 F=37  if ((reader->validate != XML_TEXTREADER_NOT_VALIDATE) && ...
  d=1   L1505  T=4 F=1  T=5 F=0  ((reader->state != XML_TEXTREADER_END) &&
  d=1   L1506  T=4 F=0  T=4 F=1  (reader->state != XML_TEXTREADER_BACKTRACK))) {
  d=1   L1516  T=0 F=8  T=0 F=47  if ((reader->patternNr > 0) && (reader->state != XML_TEXT...
  d=1   L1528  T=0 F=8  T=0 F=47  if ((reader->validate == XML_TEXTREADER_VALIDATE_XSD) &&

[off-chain: 246 additional divergent branches across 24 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=7f4e04734d7c7f74, size=219 bytes, fuzzer=grimoire, trial=1, discovered_at=17396s, mutation_op=BytesSetMutator):
  0000: ff ab ab ab ab ab 15 a9 05 49 53 4f 12 38 38 35   .........ISO.885
  0010: 39 2d 34 78 6d 6c 00 49 53 4f 2d 38 38 35 39 2d   9-4xml.ISO-8859-
  0020: 32 78 6d 6c 00 00 d4 01 00 7f 69 67 ff ff ff ff   2xml......ig....
  0030: ff fd ff ff ff ff 49 53 4f 2d 38 38 35 39 2d 35   ......ISO-8859-5

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=05a2233124360cc9, size=299 bytes, fuzzer=cmplog, trial=1, discovered_at=22s, mutation_op=BytesExpandMutator,TokenReplace,ByteRandMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2c 78 6d 6c 5c 0a   ....127772,xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 6b 6b   a SYSTEM "dtdskk
Seed 2 (id=0243680d59374a7c, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=54s, mutation_op=WordInterestingMutator,TokenReplace):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=09facfa22bc46ce6, size=379 bytes, fuzzer=cmplog, trial=1, discovered_at=58s, mutation_op=BytesSetMutator,CrossoverReplaceMutator):
  0000: 77 77 77 77 77 77 77 77 77 77 77 77 6d 6c 5c 0a   wwwwwwwwwwwwml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=0a9c869d5e3c189b, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=95s, mutation_op=TokenInsert,BytesSetMutator,ByteIncMutator,BytesDeleteMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=047fe13ea3b05010, size=386 bytes, fuzzer=cmplog, trial=1, discovered_at=4456s, mutation_op=WordAddMutator,BytesDeleteMutator,CrossoverReplaceMutator):
  0000: 06 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 3b 31   a SYSTEM "dtds;1


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  ff(.)x1                             06(.)x8 77(w)x1 31(1)x1             DIFFER
   0x0001  ab(.)x1                             00(.)x7 77(w)x1 25(%)x1 32(2)x1     DIFFER
   0x0002  ab(.)x1                             00(.)x8 77(w)x1 37(7)x1             DIFFER
   0x0003  ab(.)x1                             00(.)x8 77(w)x1 37(7)x1             DIFFER
   0x0004  ab(.)x1                             31(1)x6 77(w)x1 2f(/)x1 37(7)x1 +1u  DIFFER
   0x0005  ab(.)x1                             32(2)x7 77(w)x1 2d(-)x1 74(t)x1     DIFFER
   0x0006  15(.)x1                             37(7)x6 77(w)x1 02(.)x1 2e(.)x1 +1u  DIFFER
   0x0007  a9(.)x1                             37(7)x6 77(w)x1 02(.)x1 64(d)x1 +1u  DIFFER
   0x0008  05(.)x1                             37(7)x7 77(w)x1 73(s)x1 2d(-)x1     DIFFER
   0x0009  49(I)x1                             32(2)x7 77(w)x1 64(d)x1 3a(:)x1     DIFFER
   0x000a  53(S)x1                             2e(.)x5 2c(,)x2 77(w)x1 06(.)x1 +1u  DIFFER
   0x000b  4f(O)x1                             78(x)x6 77(w)x1 2f(/)x1 00(.)x1 +1u  DIFFER
   0x000c  12(.)x1                             6d(m)x8 00(.)x1 37(7)x1             DIFFER
   0x000d  38(8)x1                             6c(l)x8 00(.)x1 37(7)x1             DIFFER
   0x000e  38(8)x1                             5c(\)x9 31(1)x1                     DIFFER
   0x000f  35(5)x1                             0a(.)x9 32(2)x1                     DIFFER
   0x0010  39(9)x1                             3c(<)x9 37(7)x1                     DIFFER
   0x0011  2d(-)x1                             3f(?)x9 37(7)x1                     DIFFER
   0x0012  34(4)x1                             78(x)x9 37(7)x1                     DIFFER
   0x0013  78(x)x1                             6d(m)x8 32(2)x1 54(T)x1             DIFFER
   0x0014  6d(m)x1                             6c(l)x9 2e(.)x1                     DIFFER
   0x0015  6c(l)x1                             20( )x9 78(x)x1                     DIFFER
   0x0016  00(.)x1                             76(v)x9 6d(m)x1                     DIFFER
   0x0017  49(I)x1                             65(e)x9 6c(l)x1                     DIFFER
   0x0018  53(S)x1                             72(r)x9 5c(\)x1                     DIFFER
   0x0019  4f(O)x1                             73(s)x9 0a(.)x1                     DIFFER
   0x001a  2d(-)x1                             69(i)x9 3c(<)x1                     DIFFER
   0x001b  38(8)x1                             6f(o)x9 3f(?)x1                     DIFFER
   0x001c  38(8)x1                             6e(n)x9 78(x)x1                     DIFFER
   0x001d  35(5)x1                             3d(=)x8 6d(m)x1 3a(:)x1             DIFFER
   0x001e  39(9)x1                             22(")x9 6c(l)x1                     DIFFER
   0x001f  2d(-)x1                             31(1)x9 20( )x1                     DIFFER
   0x0020  32(2)x1                             2e(.)x9 76(v)x1                     DIFFER
   0x0021  78(x)x1                             30(0)x9 65(e)x1                     DIFFER
   0x0022  6d(m)x1                             22(")x9 72(r)x1                     DIFFER
   0x0023  6c(l)x1                             3f(?)x9 73(s)x1                     DIFFER
   0x0024  00(.)x1                             3e(>)x9 69(i)x1                     DIFFER
   0x0025  00(.)x1                             0a(.)x9 6f(o)x1                     DIFFER
   0x0026  d4(.)x1                             3c(<)x9 6e(n)x1                     DIFFER
   0x0027  01(.)x1                             21(!)x9 3d(=)x1                     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_7268.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 7268,
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 7268 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 7268 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 7268 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).