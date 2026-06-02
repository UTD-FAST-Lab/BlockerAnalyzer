==== BLOCKER ====
Target: libxml2
Branch ID: 9841
Location: /src/libxml2/valid.c:4660:9
Enclosing function: xmlValidateOneNamespace
Source line:     if (attrDecl == NULL) {
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0        4          6  REFERENCE
cmplog                           0        8          2  loser (value_profile vs value_profile_cmplog)
value_profile                    0        6          4  REFERENCE
value_profile_cmplog             8        2          0  winner (value_profile vs cmplog)
naive_ctx                        1        6          3  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         7        3          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 33  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=8/10  blocked=2  unreached=0
  loser:  resolved=0/10  blocked=8  unreached=2
  avg duration blocked: winner=7.20h  loser=19.50h
  avg hitcount on branch: winner=3  loser=0
  prob_div=0.80  dur_div=12.30h  hit_div=3
  subject-level: delta_AUC=48643200.0  p_AUC=0.0002  delta_Final=809.5  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libxml2/9841/{W,L}/branch_coverage_show.txt

--- Enclosing function: xmlValidateOneNamespace (/src/libxml2/valid.c:4607-4810) ---
[ ]  4605  int
[ ]  4606  xmlValidateOneNamespace(xmlValidCtxtPtr ctxt, xmlDocPtr doc,
[B]  4607  xmlNodePtr elem, const xmlChar *prefix, xmlNsPtr ns, const xmlChar *value) {
[ ]  4608      /* xmlElementPtr elemDecl; */
[B]  4609      xmlAttributePtr attrDecl =  NULL;
[B]  4610      int val;
[B]  4611      int ret = 1;
[ ]  4612  
[B]  4613      CHECK_DTD;
[B]  4614      if ((elem == NULL) || (elem->name == NULL)) return(0);
[B]  4615      if ((ns == NULL) || (ns->href == NULL)) return(0);
[ ]  4616  
[B]  4617      if (prefix != NULL) {
[ ]  4618  	xmlChar fn[50];
[ ]  4619  	xmlChar *fullname;
[ ]  4620  
[ ]  4621  	fullname = xmlBuildQName(elem->name, prefix, fn, 50);
[ ]  4622  	if (fullname == NULL) {
[ ]  4623  	    xmlVErrMemory(ctxt, "Validating namespace");
[ ]  4624  	    return(0);
[ ]  4625  	}
[ ]  4626  	if (ns->prefix != NULL) {
[ ]  4627  	    attrDecl = xmlGetDtdQAttrDesc(doc->intSubset, fullname,
[ ]  4628  		                          ns->prefix, BAD_CAST "xmlns");
[ ]  4629  	    if ((attrDecl == NULL) && (doc->extSubset != NULL))
[ ]  4630  		attrDecl = xmlGetDtdQAttrDesc(doc->extSubset, fullname,
[ ]  4631  					  ns->prefix, BAD_CAST "xmlns");
[ ]  4632  	} else {
[ ]  4633  	    attrDecl = xmlGetDtdAttrDesc(doc->intSubset, fullname,
[ ]  4634  		                         BAD_CAST "xmlns");
[ ]  4635  	    if ((attrDecl == NULL) && (doc->extSubset != NULL))
[ ]  4636  		attrDecl = xmlGetDtdAttrDesc(doc->extSubset, fullname,
[ ]  4637  			                 BAD_CAST "xmlns");
[ ]  4638  	}
[ ]  4639  	if ((fullname != fn) && (fullname != elem->name))
[ ]  4640  	    xmlFree(fullname);
[ ]  4641      }
[B]  4642      if (attrDecl == NULL) {
[B]  4643  	if (ns->prefix != NULL) {
[B]  4644  	    attrDecl = xmlGetDtdQAttrDesc(doc->intSubset, elem->name,
[B]  4645  		                          ns->prefix, BAD_CAST "xmlns");
[B]  4646  	    if ((attrDecl == NULL) && (doc->extSubset != NULL))
[B]  4647  		attrDecl = xmlGetDtdQAttrDesc(doc->extSubset, elem->name,
[B]  4648  					      ns->prefix, BAD_CAST "xmlns");
[B]  4649  	} else {
[ ]  4650  	    attrDecl = xmlGetDtdAttrDesc(doc->intSubset,
[ ]  4651  		                         elem->name, BAD_CAST "xmlns");
[ ]  4652  	    if ((attrDecl == NULL) && (doc->extSubset != NULL))
[ ]  4653  		attrDecl = xmlGetDtdAttrDesc(doc->extSubset,
[ ]  4654  					     elem->name, BAD_CAST "xmlns");
[ ]  4655  	}
[B]  4656      }
[ ]  4657  
[ ]  4658  
[ ]  4659      /* Validity Constraint: Attribute Value Type */
[B]  4660      if (attrDecl == NULL) { <-- BLOCKER
[W]  4661  	if (ns->prefix != NULL) {
[W]  4662  	    xmlErrValidNode(ctxt, elem, XML_DTD_UNKNOWN_ATTRIBUTE,
[W]  4663  		   "No declaration for attribute xmlns:%s of element %s\n",
[W]  4664  		   ns->prefix, elem->name, NULL);
[W]  4665  	} else {
[ ]  4666  	    xmlErrValidNode(ctxt, elem, XML_DTD_UNKNOWN_ATTRIBUTE,
[ ]  4667  		   "No declaration for attribute xmlns of element %s\n",
[ ]  4668  		   elem->name, NULL, NULL);
[ ]  4669  	}
[W]  4670  	return(0);
[W]  4671      }
[ ]  4672  
[B]  4673      val = xmlValidateAttributeValueInternal(doc, attrDecl->atype, value);
[B]  4674      if (val == 0) {
[ ]  4675  	if (ns->prefix != NULL) {
[ ]  4676  	    xmlErrValidNode(ctxt, elem, XML_DTD_INVALID_DEFAULT,
[ ]  4677  	       "Syntax of value for attribute xmlns:%s of %s is not valid\n",
[ ]  4678  		   ns->prefix, elem->name, NULL);
[ ]  4679  	} else {
[ ]  4680  	    xmlErrValidNode(ctxt, elem, XML_DTD_INVALID_DEFAULT,
[ ]  4681  	       "Syntax of value for attribute xmlns of %s is not valid\n",
[ ]  4682  		   elem->name, NULL, NULL);
[ ]  4683  	}
[ ]  4684          ret = 0;
[ ]  4685      }
[ ]  4686  
[ ]  4687      /* Validity constraint: Fixed Attribute Default */
[B]  4688      if (attrDecl->def == XML_ATTRIBUTE_FIXED) {
[B]  4689  	if (!xmlStrEqual(value, attrDecl->defaultValue)) {
[ ]  4690  	    if (ns->prefix != NULL) {
[ ]  4691  		xmlErrValidNode(ctxt, elem, XML_DTD_ATTRIBUTE_DEFAULT,
[ ]  4692         "Value for attribute xmlns:%s of %s is different from default \"%s\"\n",
[ ]  4693  		       ns->prefix, elem->name, attrDecl->defaultValue);
[ ]  4694  	    } else {
[ ]  4695  		xmlErrValidNode(ctxt, elem, XML_DTD_ATTRIBUTE_DEFAULT,
[ ]  4696         "Value for attribute xmlns of %s is different from default \"%s\"\n",
[ ]  4697  		       elem->name, attrDecl->defaultValue, NULL);
[ ]  4698  	    }
[ ]  4699  	    ret = 0;
[ ]  4700  	}
[B]  4701      }
[ ]  4702  
[ ]  4703      /*
[ ]  4704       * Casting ns to xmlAttrPtr is wrong. We'd need separate functions
[ ]  4705       * xmlAddID and xmlAddRef for namespace declarations, but it makes
[ ]  4706       * no practical sense to use ID types anyway.
[ ]  4707       */
[ ]  4708  #if 0
[ ]  4709      /* Validity Constraint: ID uniqueness */
[ ]  4710      if (attrDecl->atype == XML_ATTRIBUTE_ID) {
[ ]  4711          if (xmlAddID(ctxt, doc, value, (xmlAttrPtr) ns) == NULL)
[ ]  4712  	    ret = 0;
[ ]  4713      }
[ ]  4714  
[ ]  4715      if ((attrDecl->atype == XML_ATTRIBUTE_IDREF) ||
[ ]  4716  	(attrDecl->atype == XML_ATTRIBUTE_IDREFS)) {
[ ]  4717          if (xmlAddRef(ctxt, doc, value, (xmlAttrPtr) ns) == NULL)
[ ]  4718  	    ret = 0;
[ ]  4719      }
[ ]  4720  #endif
[ ]  4721  
[ ]  4722      /* Validity Constraint: Notation Attributes */
[B]  4723      if (attrDecl->atype == XML_ATTRIBUTE_NOTATION) {
[ ]  4724          xmlEnumerationPtr tree = attrDecl->tree;
[ ]  4725          xmlNotationPtr nota;
[ ]  4726  
[ ]  4727          /* First check that the given NOTATION was declared */
[ ]  4728  	nota = xmlGetDtdNotationDesc(doc->intSubset, value);
[ ]  4729  	if (nota == NULL)
[ ]  4730  	    nota = xmlGetDtdNotationDesc(doc->extSubset, value);
[ ]  4731  
[ ]  4732  	if (nota == NULL) {
[ ]  4733  	    if (ns->prefix != NULL) {
[ ]  4734  		xmlErrValidNode(ctxt, elem, XML_DTD_UNKNOWN_NOTATION,
[ ]  4735         "Value \"%s\" for attribute xmlns:%s of %s is not a declared Notation\n",
[ ]  4736  		       value, ns->prefix, elem->name);
[ ]  4737  	    } else {
[ ]  4738  		xmlErrValidNode(ctxt, elem, XML_DTD_UNKNOWN_NOTATION,
[ ]  4739         "Value \"%s\" for attribute xmlns of %s is not a declared Notation\n",
[ ]  4740  		       value, elem->name, NULL);
[ ]  4741  	    }
[ ]  4742  	    ret = 0;
[ ]  4743          }
[ ]  4744  
[ ]  4745  	/* Second, verify that it's among the list */
[ ]  4746  	while (tree != NULL) {
[ ]  4747  	    if (xmlStrEqual(tree->name, value)) break;
[ ]  4748  	    tree = tree->next;
[ ]  4749  	}
[ ]  4750  	if (tree == NULL) {
[ ]  4751  	    if (ns->prefix != NULL) {
[ ]  4752  		xmlErrValidNode(ctxt, elem, XML_DTD_NOTATION_VALUE,
[ ]  4753  "Value \"%s\" for attribute xmlns:%s of %s is not among the enumerated notations\n",
[ ]  4754  		       value, ns->prefix, elem->name);
[ ]  4755  	    } else {
[ ]  4756  		xmlErrValidNode(ctxt, elem, XML_DTD_NOTATION_VALUE,
[ ]  4757  "Value \"%s\" for attribute xmlns of %s is not among the enumerated notations\n",
[ ]  4758  		       value, elem->name, NULL);
[ ]  4759  	    }
[ ]  4760  	    ret = 0;
[ ]  4761  	}
[ ]  4762      }
[ ]  4763  
[ ]  4764      /* Validity Constraint: Enumeration */
[B]  4765      if (attrDecl->atype == XML_ATTRIBUTE_ENUMERATION) {
[ ]  4766          xmlEnumerationPtr tree = attrDecl->tree;
[ ]  4767  	while (tree != NULL) {
[ ]  4768  	    if (xmlStrEqual(tree->name, value)) break;
[ ]  4769  	    tree = tree->next;
[ ]  4770  	}
[ ]  4771  	if (tree == NULL) {
[ ]  4772  	    if (ns->prefix != NULL) {
[ ]  4773  		xmlErrValidNode(ctxt, elem, XML_DTD_ATTRIBUTE_VALUE,
[ ]  4774  "Value \"%s\" for attribute xmlns:%s of %s is not among the enumerated set\n",
[ ]  4775  		       value, ns->prefix, elem->name);
[ ]  4776  	    } else {
[ ]  4777  		xmlErrValidNode(ctxt, elem, XML_DTD_ATTRIBUTE_VALUE,
[ ]  4778  "Value \"%s\" for attribute xmlns of %s is not among the enumerated set\n",
[ ]  4779  		       value, elem->name, NULL);
[ ]  4780  	    }
[ ]  4781  	    ret = 0;
[ ]  4782  	}
[ ]  4783      }
[ ]  4784  
[ ]  4785      /* Fixed Attribute Default */
[B]  4786      if ((attrDecl->def == XML_ATTRIBUTE_FIXED) &&
[B]  4787          (!xmlStrEqual(attrDecl->defaultValue, value))) {
[ ]  4788  	if (ns->prefix != NULL) {
[ ]  4789  	    xmlErrValidNode(ctxt, elem, XML_DTD_ELEM_NAMESPACE,
[ ]  4790  		   "Value for attribute xmlns:%s of %s must be \"%s\"\n",
[ ]  4791  		   ns->prefix, elem->name, attrDecl->defaultValue);
[ ]  4792  	} else {
[ ]  4793  	    xmlErrValidNode(ctxt, elem, XML_DTD_ELEM_NAMESPACE,
[ ]  4794  		   "Value for attribute xmlns of %s must be \"%s\"\n",
[ ]  4795  		   elem->name, attrDecl->defaultValue, NULL);
[ ]  4796  	}
[ ]  4797          ret = 0;
[ ]  4798      }
[ ]  4799  
[ ]  4800      /* Extra check for the attribute value */
[B]  4801      if (ns->prefix != NULL) {
[B]  4802  	ret &= xmlValidateAttributeValue2(ctxt, doc, ns->prefix,
[B]  4803  					  attrDecl->atype, value);
[B]  4804      } else {
[ ]  4805  	ret &= xmlValidateAttributeValue2(ctxt, doc, BAD_CAST "xmlns",
[ ]  4806  					  attrDecl->atype, value);
[ ]  4807      }
[ ]  4808  
[B]  4809      return(ret);
[B]  4810  }

--- Caller (1 hop): SAX2.c:xmlSAX2AttributeInternal (/src/libxml2/SAX2.c:1097-1438, calls xmlValidateOneNamespace at line 1291) (±10 around call site) ---
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
[B]  1291  	    ctxt->valid &= xmlValidateOneNamespace(&ctxt->vctxt, ctxt->myDoc, <-- CALL
[B]  1292  					   ctxt->node, prefix, nsret, value);
[B]  1293  #endif /* LIBXML_VALID_ENABLED */
[B]  1294  	if (name != NULL)
[B]  1295  	    xmlFree(name);
[B]  1296  	if (nval != NULL)
[ ]  1297  	    xmlFree(nval);
[B]  1298  	if (val != value)
[B]  1299  	    xmlFree(val);
[B]  1300  	return;
[B]  1301      }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438, calls xmlValidateOneNamespace at line 1223)
hop 3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591, calls SAX2.c:xmlSAX2AttributeInternal at line 1574)
hop 3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806, calls SAX2.c:xmlSAX2AttributeInternal at line 1726)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      63       855  valid.c:xmlIsDocNameChar  (/src/libxml2/valid.c:3546-3581)
      36       156  valid.c:xmlValidateAttributeValueInternal  (/src/libxml2/valid.c:3864-3883)
       9        75  valid.c:xmlValidateNmtokensValueInternal  (/src/libxml2/valid.c:3765-3810)
      27        84  SAX2.c:xmlSAX2TextNode  (/src/libxml2/SAX2.c:1868-1943)
      27        81  xmlSAX2AttributeDecl  (/src/libxml2/SAX2.c:701-758)
      27        81  valid.c:xmlFreeAttribute  (/src/libxml2/valid.c:1907-1939)
      27        81  xmlAddAttributeDecl  (/src/libxml2/valid.c:1964-2172)
      27        81  valid.c:xmlFreeAttributeTableEntry  (/src/libxml2/valid.c:2175-2177)
      27        81  valid.c:xmlGetDtdElementDesc2  (/src/libxml2/valid.c:3280-3334)
      27        81  xmlValidateAttributeDecl  (/src/libxml2/valid.c:4197-4288)
      27        81  valid.c:xmlValidateAttributeCallback  (/src/libxml2/valid.c:6762-6830)
       0        42  xmlSAX2StartElementNs  (/src/libxml2/SAX2.c:2228-2459)
       9        48  valid.c:xmlValidateAttributeValue2  (/src/libxml2/valid.c:3945-4033)
       0        39  xmlValidateOneAttribute  (/src/libxml2/valid.c:4431-4577)
      18        54  xmlSAX2ElementDecl  (/src/libxml2/SAX2.c:772-807)
... (29 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  SAX2.c:xmlCheckDefaultedAttributes  (/src/libxml2/SAX2.c:1447-1591) ---
  d=3   L1539  T=9 F=0  T=6 F=6  (xmlStrEqual(attr->prefix, BAD_CAST "xmlns"))) ||
  d=3   L1540  T=0 F=0  T=0 F=6  ((attr->prefix == NULL) &&
  d=3   L1542  T=0 F=0  T=0 F=6  (ctxt->loadsubset & XML_COMPLETE_ATTRS)) {
--- d=3  xmlSAX2StartElement  (/src/libxml2/SAX2.c:1603-1806) ---
  d=3   L1724  T=9 F=0  T=0 F=0  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1724  T=9 F=0  T=0 F=6  if ((att[0] == 'x') && (att[1] == 'm') && (att[2] == 'l') &&
  d=3   L1725  T=9 F=0  T=0 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=3   L1725  T=9 F=0  T=0 F=0  (att[3] == 'n') && (att[4] == 's'))
  d=3   L1771  T=0 F=9  T=0 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1771  T=0 F=9  T=6 F=0  if ((att[0] != 'x') || (att[1] != 'm') || (att[2] != 'l') ||
  d=3   L1772  T=0 F=9  T=0 F=0  (att[3] != 'n') || (att[4] != 's'))
  d=3   L1772  T=0 F=9  T=0 F=0  (att[3] != 'n') || (att[4] != 's'))
--- d=2  SAX2.c:xmlSAX2AttributeInternal  (/src/libxml2/SAX2.c:1097-1438) ---
  d=2   L1235  T=18 F=0  T=6 F=6  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1235  T=18 F=0  T=6 F=0  (ns != NULL) && (ns[0] == 'x') && (ns[1] == 'm') && (ns[2...
  d=2   L1236  T=18 F=0  T=6 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=2   L1236  T=18 F=0  T=6 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=2   L1236  T=18 F=0  T=6 F=0  (ns[3] == 'n') && (ns[4] == 's') && (ns[5] == 0)) {
  d=2   L1243  T=18 F=0  T=3 F=3  if (!ctxt->replaceEntities) {
  d=2   L1248  T=0 F=18  T=0 F=3  if (val == NULL) {
  d=2   L1261  T=0 F=18  T=0 F=6  if (val[0] == 0) {
  d=2   L1265  T=18 F=0  T=3 F=0  if ((ctxt->pedantic != 0) && (val[0] != 0)) {
  d=2   L1265  T=18 F=0  T=3 F=3  if ((ctxt->pedantic != 0) && (val[0] != 0)) {
  d=2   L1269  T=9 F=9  T=3 F=0  if (uri == NULL) {
  d=2   L1273  T=0 F=9  T=0 F=0  if (uri->scheme == NULL) {
  d=2   L1289  T=18 F=0  T=6 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1289  T=18 F=0  T=6 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1289  T=18 F=0  T=6 F=0  if (nsret != NULL && ctxt->validate && ctxt->wellFormed &&
  d=2   L1290  T=18 F=0  T=6 F=0  ctxt->myDoc && ctxt->myDoc->intSubset)
  d=2   L1290  T=18 F=0  T=6 F=0  ctxt->myDoc && ctxt->myDoc->intSubset)
  d=2   L1294  T=18 F=0  T=6 F=0  if (name != NULL)
  d=2   L1296  T=0 F=18  T=0 F=6  if (nval != NULL)
  d=2   L1298  T=18 F=0  T=3 F=3  if (val != value)
  d=2   L1303  T=0 F=0  T=6 F=0  if (ns != NULL) {
  d=2   L1306  T=0 F=0  T=3 F=3  if (namespace == NULL) {
  d=2   L1314  T=0 F=0  T=0 F=3  while (prop != NULL) {
  d=2   L1338  T=0 F=0  T=0 F=6  if (ret == NULL)
  d=2   L1341  T=0 F=0  T=3 F=0  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1341  T=0 F=0  T=3 F=3  if ((ctxt->replaceEntities == 0) && (!ctxt->html)) {
  d=2   L1346  T=0 F=0  T=3 F=3  while (tmp != NULL) {
  d=2   L1348  T=0 F=0  T=3 F=0  if (tmp->next == NULL)
  d=2   L1352  T=0 F=0  T=3 F=0  } else if (value != NULL) {
  d=2   L1355  T=0 F=0  T=3 F=0  if (ret->children != NULL)
  d=2   L1360  T=0 F=0  T=6 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1360  T=0 F=0  T=6 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1360  T=0 F=0  T=6 F=0  if ((!ctxt->html) && ctxt->validate && ctxt->wellFormed &&
  d=2   L1361  T=0 F=0  T=6 F=0  ctxt->myDoc && ctxt->myDoc->intSubset) {
  d=2   L1361  T=0 F=0  T=6 F=0  ctxt->myDoc && ctxt->myDoc->intSubset) {
  d=2   L1367  T=0 F=0  T=3 F=3  if (!ctxt->replaceEntities) {
  d=2   L1375  T=0 F=0  T=0 F=3  if (val == NULL)
  d=2   L1388  T=0 F=0  T=0 F=3  if (nvalnorm != NULL) {
  d=2   L1434  T=0 F=0  T=0 F=6  if (nval != NULL)
  d=2   L1436  T=0 F=0  T=6 F=0  if (ns != NULL)
--- d=1  xmlValidateOneNamespace  (/src/libxml2/valid.c:4607-4810) ---
  d=1   L4660  T=9 F=9  T=0 F=27  if (attrDecl == NULL) {  <-- BLOCKER
  d=1   L4661  T=9 F=0  T=0 F=0  if (ns->prefix != NULL) {
  d=1   L4674  T=0 F=9  T=0 F=27  if (val == 0) {
  d=1   L4688  T=9 F=0  T=27 F=0  if (attrDecl->def == XML_ATTRIBUTE_FIXED) {
  d=1   L4689  T=0 F=9  T=0 F=27  if (!xmlStrEqual(value, attrDecl->defaultValue)) {
  d=1   L4723  T=0 F=9  T=0 F=27  if (attrDecl->atype == XML_ATTRIBUTE_NOTATION) {
  d=1   L4765  T=0 F=9  T=0 F=27  if (attrDecl->atype == XML_ATTRIBUTE_ENUMERATION) {
  d=1   L4786  T=9 F=0  T=27 F=0  if ((attrDecl->def == XML_ATTRIBUTE_FIXED) &&
  d=1   L4787  T=0 F=9  T=0 F=27  (!xmlStrEqual(attrDecl->defaultValue, value))) {
  d=1   L4801  T=9 F=0  T=27 F=0  if (ns->prefix != NULL) {

[off-chain: 557 additional divergent branches across 48 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=a425477316d1bc9c, size=381 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=1682s, mutation_op=CrossoverInsertMutator,BytesExpandMutator,ByteAddMutator,TokenInsert):
  0000: f5 ff ff ff ff ff ff ff 06 00 00 00 31 32 37 37   ............1277
  0010: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 0a 61 20 53 59 53 54 45 4d   DOCTYPE.a SYSTEM
Seed 2 (id=8022c433e1cf131c, size=381 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=21097s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,DwordAddMutator):
  0000: f5 ff ff ff ff ff ff ff 06 00 00 00 31 32 37 37   ............1277
  0010: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 0a 61 20 53 59 53 54 45 4d   DOCTYPE.a SYSTEM
Seed 3 (id=fe67214245b40d4f, size=381 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=21097s, mutation_op=BytesRandSetMutator,BytesDeleteMutator,DwordAddMutator):
  0000: f5 ff ff ff ff ff ff ff 06 00 00 00 31 32 37 37   ............1277
  0010: 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c 20 76 65   72.xml\.<?xml ve
  0020: 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e 0a 3c 21   rsion="1.0"?>.<!
  0030: 44 4f 43 54 59 50 45 0a 61 20 53 59 53 54 45 4d   DOCTYPE.a SYSTEM

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=4381a942c85ca897, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=94s, mutation_op=ByteNegMutator):
  0000: fa 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 2 (id=3f82a3daf8d36108, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3471s, mutation_op=BytesDeleteMutator,BytesSetMutator):
  0000: fa 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 3 (id=c8a923dfc409199c, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3471s, mutation_op=BytesDeleteMutator,BytesSetMutator):
  0000: fa 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 4 (id=4fa23f37cdba538c, size=368 bytes, fuzzer=cmplog, trial=1, discovered_at=3590s, mutation_op=CrossoverReplaceMutator,QwordAddMutator,ByteDecMutator):
  0000: f9 00 00 00 31 32 37 37 37 32 2e 78 6d 6c 5c 0a   ....127772.xml\.
  0010: 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31   <?xml version="1
  0020: 2e 30 22 3f 3e 0a 3c 21 44 4f 43 54 59 50 45 20   .0"?>.<!DOCTYPE 
  0030: 61 20 53 59 53 54 45 4d 20 22 64 74 64 73 2f 31   a SYSTEM "dtds/1
Seed 5 (id=d6c3c9bf33c78dac, size=363 bytes, fuzzer=cmplog, trial=1, discovered_at=4496s, mutation_op=BytesDeleteMutator,WordInterestingMutator,CrossoverReplaceMutator,ByteNegMutator):
  0000: 32 37 37 37 32 2e 78 6d 6c 5c 0a 3c 3f 78 6d 6c   27772.xml\.<?xml
  0010: 20 76 65 72 73 69 6f 6e 3d 22 31 2e 30 22 3f 3e    version="1.0"?>
  0020: 0a 3c 21 44 4f 43 54 59 50 45 20 61 20 53 59 53   .<!DOCTYPE a SYS
  0030: 54 45 4d 20 22 64 74 64 73 2f 31 32 37 37 37 32   TEM "dtds/127772


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  f5(.)x3                             fa(.)x6 f9(.)x1 32(2)x1 f1(.)x1     DIFFER
   0x0001  ff(.)x3                             00(.)x7 37(7)x1 ff(.)x1             PARTIAL
   0x0002  ff(.)x3                             00(.)x7 37(7)x1 ff(.)x1             PARTIAL
   0x0003  ff(.)x3                             00(.)x7 37(7)x1 ff(.)x1             PARTIAL
   0x0004  ff(.)x3                             31(1)x7 32(2)x1 30(0)x1             DIFFER
   0x0005  ff(.)x3                             32(2)x8 2e(.)x1                     DIFFER
   0x0006  ff(.)x3                             37(7)x7 78(x)x1 4a(J)x1             DIFFER
   0x0007  ff(.)x3                             37(7)x8 6d(m)x1                     DIFFER
   0x0008  06(.)x3                             37(7)x8 6c(l)x1                     DIFFER
   0x0009  00(.)x3                             32(2)x8 5c(\)x1                     DIFFER
   0x000a  00(.)x3                             2e(.)x8 0a(.)x1                     DIFFER
   0x000b  00(.)x3                             78(x)x8 3c(<)x1                     DIFFER
   0x000c  31(1)x3                             6d(m)x8 3f(?)x1                     DIFFER
   0x000d  32(2)x3                             6c(l)x8 78(x)x1                     DIFFER
   0x000e  37(7)x3                             5c(\)x8 6d(m)x1                     DIFFER
   0x000f  37(7)x3                             0a(.)x8 6c(l)x1                     DIFFER
   0x0010  37(7)x3                             3c(<)x8 20( )x1                     DIFFER
   0x0011  32(2)x3                             3f(?)x8 76(v)x1                     DIFFER
   0x0012  2e(.)x3                             78(x)x8 65(e)x1                     DIFFER
   0x0013  78(x)x3                             6d(m)x8 72(r)x1                     DIFFER
   0x0014  6d(m)x3                             6c(l)x8 73(s)x1                     DIFFER
   0x0015  6c(l)x3                             20( )x8 69(i)x1                     DIFFER
   0x0016  5c(\)x3                             76(v)x8 6f(o)x1                     DIFFER
   0x0017  0a(.)x3                             65(e)x8 6e(n)x1                     DIFFER
   0x0018  3c(<)x3                             72(r)x8 3d(=)x1                     DIFFER
   0x0019  3f(?)x3                             73(s)x8 22(")x1                     DIFFER
   0x001a  78(x)x3                             69(i)x8 31(1)x1                     DIFFER
   0x001b  6d(m)x3                             6f(o)x8 2e(.)x1                     DIFFER
   0x001c  6c(l)x3                             6e(n)x8 30(0)x1                     DIFFER
   0x001d  20( )x3                             3d(=)x8 22(")x1                     DIFFER
   0x001e  76(v)x3                             22(")x8 3f(?)x1                     DIFFER
   0x001f  65(e)x3                             31(1)x8 3e(>)x1                     DIFFER
   0x0020  72(r)x3                             2e(.)x8 0a(.)x1                     DIFFER
   0x0021  73(s)x3                             30(0)x8 3c(<)x1                     DIFFER
   0x0022  69(i)x3                             22(")x8 21(!)x1                     DIFFER
   0x0023  6f(o)x3                             3f(?)x8 44(D)x1                     DIFFER
   0x0024  6e(n)x3                             3e(>)x8 4f(O)x1                     DIFFER
   0x0025  3d(=)x3                             0a(.)x8 43(C)x1                     DIFFER
   0x0026  22(")x3                             3c(<)x8 54(T)x1                     DIFFER
   0x0027  31(1)x3                             21(!)x8 59(Y)x1                     DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libxml2_9841.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 9841,
  "target": "libxml2",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [value_profile_cmplog>cmplog (value_profile)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 9841 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 9841 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 9841 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).