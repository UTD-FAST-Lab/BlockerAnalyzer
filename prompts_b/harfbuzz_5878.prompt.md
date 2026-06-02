==== BLOCKER ====
Target: harfbuzz
Branch ID: 5878
Location: /src/harfbuzz/src/hb-ot-shaper-indic.cc:1099:27
Enclosing function: hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)
Source line:       if (start < base && info[base].indic_position() > POS_BASE_C)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            2        8          0  loser (ctx_coverage vs naive_ctx)
cmplog                           0       10          0  REFERENCE
value_profile                    2        8          0  REFERENCE
value_profile_cmplog             1        9          0  REFERENCE
naive_ctx                       10        0          0  winner (ctx_coverage vs naive)
naive_ngram4                     1        9          0  REFERENCE
mopt                             2        8          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             4        6          0  REFERENCE
grimoire                         ?        ?          ?  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['naive', 'naive_ctx']
REFERENCE fuzzers (auxiliary context only):     ['cmplog', 'value_profile', 'value_profile_cmplog', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive_ctx > naive  [delta: ctx_coverage] ---
  subject 15  (naive_ctx vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=8.60h  loser=22.20h
  avg hitcount on branch: winner=16  loser=0
  prob_div=0.80  dur_div=13.60h  hit_div=15
  subject-level: delta_AUC=15634800.0  p_AUC=0.0003  delta_Final=258.3  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5878/{W,L}/branch_coverage_show.txt

--- Enclosing function: hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474) ---
[ ]  1015  				 hb_buffer_t *buffer,
[ ]  1016  				 unsigned int start, unsigned int end)
[B]  1017  {
[B]  1018    const indic_shape_plan_t *indic_plan = (const indic_shape_plan_t *) plan->data;
[B]  1019    hb_glyph_info_t *info = buffer->info;
[ ]  1020  
[ ]  1021  
[ ]  1022    /* This function relies heavily on halant glyphs.  Lots of ligation
[ ]  1023     * and possibly multiple substitutions happened prior to this
[ ]  1024     * phase, and that might have messed up our properties.  Recover
[ ]  1025     * from a particular case of that where we're fairly sure that a
[ ]  1026     * class of I_Cat(H) is desired but has been lost. */
[ ]  1027    /* We don't call load_virama_glyph(), since we know it's already
[ ]  1028     * loaded. */
[B]  1029    hb_codepoint_t virama_glyph = indic_plan->virama_glyph;
[B]  1030    if (virama_glyph)
[ ]  1031    {
[ ]  1032      for (unsigned int i = start; i < end; i++)
[ ]  1033        if (info[i].codepoint == virama_glyph &&
[ ]  1034  	  _hb_glyph_info_ligated (&info[i]) &&
[ ]  1035  	  _hb_glyph_info_multiplied (&info[i]))
[ ]  1036        {
[ ]  1037  	/* This will make sure that this glyph passes is_halant() test. */
[ ]  1038  	info[i].indic_category() = I_Cat(H);
[ ]  1039  	_hb_glyph_info_clear_ligated_and_multiplied (&info[i]);
[ ]  1040        }
[ ]  1041    }
[ ]  1042  
[ ]  1043  
[ ]  1044    /* 4. Final reordering:
[ ]  1045     *
[ ]  1046     * After the localized forms and basic shaping forms GSUB features have been
[ ]  1047     * applied (see below), the shaping engine performs some final glyph
[ ]  1048     * reordering before applying all the remaining font features to the entire
[ ]  1049     * syllable.
[ ]  1050     */
[ ]  1051  
[B]  1052    bool try_pref = !!indic_plan->mask_array[INDIC_PREF];
[ ]  1053  
[ ]  1054    /* Find base again */
[B]  1055    unsigned int base;
[B]  1056    for (base = start; base < end; base++)
[B]  1057      if (info[base].indic_position() >= POS_BASE_C)
[B]  1058      {
[B]  1059        if (try_pref && base + 1 < end)
[ ]  1060        {
[ ]  1061  	for (unsigned int i = base + 1; i < end; i++)
[ ]  1062  	  if ((info[i].mask & indic_plan->mask_array[INDIC_PREF]) != 0)
[ ]  1063  	  {
[ ]  1064  	    if (!(_hb_glyph_info_substituted (&info[i]) &&
[ ]  1065  		  _hb_glyph_info_ligated_and_didnt_multiply (&info[i])))
[ ]  1066  	    {
[ ]  1067  	      /* Ok, this was a 'pref' candidate but didn't form any.
[ ]  1068  	       * Base is around here... */
[ ]  1069  	      base = i;
[ ]  1070  	      while (base < end && is_halant (info[base]))
[ ]  1071  		base++;
[ ]  1072  	      info[base].indic_position() = POS_BASE_C;
[ ]  1073  
[ ]  1074  	      try_pref = false;
[ ]  1075  	    }
[ ]  1076  	    break;
[ ]  1077  	  }
[ ]  1078        }
[ ]  1079        /* For Malayalam, skip over unformed below- (but NOT post-) forms. */
[B]  1080        if (buffer->props.script == HB_SCRIPT_MALAYALAM)
[ ]  1081        {
[ ]  1082  	for (unsigned int i = base + 1; i < end; i++)
[ ]  1083  	{
[ ]  1084  	  while (i < end && is_joiner (info[i]))
[ ]  1085  	    i++;
[ ]  1086  	  if (i == end || !is_halant (info[i]))
[ ]  1087  	    break;
[ ]  1088  	  i++; /* Skip halant. */
[ ]  1089  	  while (i < end && is_joiner (info[i]))
[ ]  1090  	    i++;
[ ]  1091  	  if (i < end && is_consonant (info[i]) && info[i].indic_position() == POS_BELOW_C)
[ ]  1092  	  {
[ ]  1093  	    base = i;
[ ]  1094  	    info[base].indic_position() = POS_BASE_C;
[ ]  1095  	  }
[ ]  1096  	}
[ ]  1097        }
[ ]  1098  
[B]  1099        if (start < base && info[base].indic_position() > POS_BASE_C) <-- BLOCKER
[W]  1100  	base--;
[B]  1101        break;
[B]  1102      }
[B]  1103    if (base == end && start < base &&
[B]  1104        is_one_of (info[base - 1], FLAG (I_Cat(ZWJ))))
[ ]  1105      base--;
[B]  1106    if (base < end)
[B]  1107      while (start < base &&
[B]  1108  	   is_one_of (info[base], (FLAG (I_Cat(N)) | FLAG (I_Cat(H)))))
[ ]  1109        base--;
[ ]  1110  
[ ]  1111  
[ ]  1112    /*   o Reorder matras:
[ ]  1113     *
[ ]  1114     *     If a pre-base matra character had been reordered before applying basic
[ ]  1115     *     features, the glyph can be moved closer to the main consonant based on
[ ]  1116     *     whether half-forms had been formed. Actual position for the matra is
[ ]  1117     *     defined as “after last standalone halant glyph, after initial matra
[ ]  1118     *     position and before the main consonant”. If ZWJ or ZWNJ follow this
[ ]  1119     *     halant, position is moved after it.
[ ]  1120     *
[ ]  1121     * IMPLEMENTATION NOTES:
[ ]  1122     *
[ ]  1123     * It looks like the last sentence is wrong.  Testing, with Windows 7 Uniscribe
[ ]  1124     * and Devanagari shows that the behavior is best described as:
[ ]  1125     *
[ ]  1126     * "If ZWJ follows this halant, matra is NOT repositioned after this halant.
[ ]  1127     *  If ZWNJ follows this halant, position is moved after it."
[ ]  1128     *
[ ]  1129     * Test case, with Adobe Devanagari or Nirmala UI:
[ ]  1130     *
[ ]  1131     *   U+091F,U+094D,U+200C,U+092F,U+093F
[ ]  1132     *   (Matra moves to the middle, after ZWNJ.)
[ ]  1133     *
[ ]  1134     *   U+091F,U+094D,U+200D,U+092F,U+093F
[ ]  1135     *   (Matra does NOT move, stays to the left.)
[ ]  1136     *
[ ]  1137     * https://github.com/harfbuzz/harfbuzz/issues/1070
[ ]  1138     */
[ ]  1139  
[B]  1140    if (start + 1 < end && start < base) /* Otherwise there can't be any pre-base matra characters. */
[L]  1141    {
[ ]  1142      /* If we lost track of base, alas, position before last thingy. */
[L]  1143      unsigned int new_pos = base == end ? base - 2 : base - 1;
[ ]  1144  
[ ]  1145      /* Malayalam / Tamil do not have "half" forms or explicit virama forms.
[ ]  1146       * The glyphs formed by 'half' are Chillus or ligated explicit viramas.
[ ]  1147       * We want to position matra after them.
[ ]  1148       */
[L]  1149      if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer->props.script != HB_SCRIPT_TAMIL)
[L]  1150      {
[L]  1151      search:
[L]  1152        while (new_pos > start &&
[L]  1153  	     !(is_one_of (info[new_pos], (FLAG (I_Cat(M)) | FLAG (I_Cat(MPst)) | FLAG (I_Cat(H))))))
[ ]  1154  	new_pos--;
[ ]  1155  
[ ]  1156        /* If we found no Halant we are done.
[ ]  1157         * Otherwise only proceed if the Halant does
[ ]  1158         * not belong to the Matra itself! */
[L]  1159        if (is_halant (info[new_pos]) &&
[L]  1160  	  info[new_pos].indic_position() != POS_PRE_M)
[L]  1161        {
[ ]  1162  #if 0 // See comment above
[ ]  1163  	/* -> If ZWJ or ZWNJ follow this halant, position is moved after it. */
[ ]  1164  	if (new_pos + 1 < end && is_joiner (info[new_pos + 1]))
[ ]  1165  	  new_pos++;
[ ]  1166  #endif
[L]  1167  	if (new_pos + 1 < end)
[L]  1168  	{
[ ]  1169  	  /* -> If ZWJ follows this halant, matra is NOT repositioned after this halant. */
[L]  1170  	  if (info[new_pos + 1].indic_category() == I_Cat(ZWJ))
[ ]  1171  	  {
[ ]  1172  	    /* Keep searching. */
[ ]  1173  	    if (new_pos > start)
[ ]  1174  	    {
[ ]  1175  	      new_pos--;
[ ]  1176  	      goto search;
[ ]  1177  	    }
[ ]  1178  	  }
[ ]  1179  	  /* -> If ZWNJ follows this halant, position is moved after it.
[ ]  1180  	   *
[ ]  1181  	   * IMPLEMENTATION NOTES:
[ ]  1182  	   *
[ ]  1183  	   * This is taken care of by the state-machine. A Halant,ZWNJ is a terminating
[ ]  1184  	   * sequence for a consonant syllable; any pre-base matras occurring after it
[ ]  1185  	   * will belong to the subsequent syllable.
[ ]  1186  	   */
[L]  1187  	}
[L]  1188        }
[L]  1189        else
[L]  1190  	new_pos = start; /* No move. */
[L]  1191      }
[ ]  1192  
[L]  1193      if (start < new_pos && info[new_pos].indic_position () != POS_PRE_M)
[ ]  1194      {
[ ]  1195        /* Now go see if there's actually any matras... */
[ ]  1196        for (unsigned int i = new_pos; i > start; i--)
[ ]  1197  	if (info[i - 1].indic_position () == POS_PRE_M)
[ ]  1198  	{
[ ]  1199  	  unsigned int old_pos = i - 1;
[ ]  1200  	  if (old_pos < base && base <= new_pos) /* Shouldn't actually happen. */
[ ]  1201  	    base--;
[ ]  1202  
[ ]  1203  	  hb_glyph_info_t tmp = info[old_pos];
[ ]  1204  	  memmove (&info[old_pos], &info[old_pos + 1], (new_pos - old_pos) * sizeof (info[0]));
[ ]  1205  	  info[new_pos] = tmp;
[ ]  1206  
[ ]  1207  	  /* Note: this merge_clusters() is intentionally *after* the reordering.
[ ]  1208  	   * Indic matra reordering is special and tricky... */
[ ]  1209  	  buffer->merge_clusters (new_pos, hb_min (end, base + 1));
[ ]  1210  
[ ]  1211  	  new_pos--;
[ ]  1212  	}
[L]  1213      } else {
[L]  1214        for (unsigned int i = start; i < base; i++)
[L]  1215  	if (info[i].indic_position () == POS_PRE_M) {
[L]  1216  	  buffer->merge_clusters (i, hb_min (end, base + 1));
[L]  1217  	  break;
[L]  1218  	}
[L]  1219      }
[L]  1220    }
[ ]  1221  
[ ]  1222  
[ ]  1223    /*   o Reorder reph:
[ ]  1224     *
[ ]  1225     *     Reph’s original position is always at the beginning of the syllable,
[ ]  1226     *     (i.e. it is not reordered at the character reordering stage). However,
[ ]  1227     *     it will be reordered according to the basic-forms shaping results.
[ ]  1228     *     Possible positions for reph, depending on the script, are; after main,
[ ]  1229     *     before post-base consonant forms, and after post-base consonant forms.
[ ]  1230     */
[ ]  1231  
[ ]  1232    /* Two cases:
[ ]  1233     *
[ ]  1234     * - If repha is encoded as a sequence of characters (Ra,H or Ra,H,ZWJ), then
[ ]  1235     *   we should only move it if the sequence ligated to the repha form.
[ ]  1236     *
[ ]  1237     * - If repha is encoded separately and in the logical position, we should only
[ ]  1238     *   move it if it did NOT ligate.  If it ligated, it's probably the font trying
[ ]  1239     *   to make it work without the reordering.
[ ]  1240     */
[B]  1241    if (start + 1 < end &&
[B]  1242        info[start].indic_position() == POS_RA_TO_BECOME_REPH &&
[B]  1243        ((info[start].indic_category() == I_Cat(Repha)) ^
[ ]  1244         _hb_glyph_info_ligated_and_didnt_multiply (&info[start])))
[ ]  1245    {
[ ]  1246      unsigned int new_reph_pos;
[ ]  1247      reph_position_t reph_pos = indic_plan->config->reph_pos;
[ ]  1248  
[ ]  1249      /*       1. If reph should be positioned after post-base consonant forms,
[ ]  1250       *          proceed to step 5.
[ ]  1251       */
[ ]  1252      if (reph_pos == REPH_POS_AFTER_POST)
[ ]  1253      {
[ ]  1254        goto reph_step_5;
[ ]  1255      }
[ ]  1256  
[ ]  1257      /*       2. If the reph repositioning class is not after post-base: target
[ ]  1258       *          position is after the first explicit halant glyph between the
[ ]  1259       *          first post-reph consonant and last main consonant. If ZWJ or ZWNJ
[ ]  1260       *          are following this halant, position is moved after it. If such
[ ]  1261       *          position is found, this is the target position. Otherwise,
[ ]  1262       *          proceed to the next step.
[ ]  1263       *
[ ]  1264       *          Note: in old-implementation fonts, where classifications were
[ ]  1265       *          fixed in shaping engine, there was no case where reph position
[ ]  1266       *          will be found on this step.
[ ]  1267       */
[ ]  1268      {
[ ]  1269        new_reph_pos = start + 1;
[ ]  1270        while (new_reph_pos < base && !is_halant (info[new_reph_pos]))
[ ]  1271  	new_reph_pos++;
[ ]  1272  
[ ]  1273        if (new_reph_pos < base && is_halant (info[new_reph_pos]))
[ ]  1274        {
[ ]  1275  	/* ->If ZWJ or ZWNJ are following this halant, position is moved after it. */
[ ]  1276  	if (new_reph_pos + 1 < base && is_joiner (info[new_reph_pos + 1]))
[ ]  1277  	  new_reph_pos++;
[ ]  1278  	goto reph_move;
[ ]  1279        }
[ ]  1280      }
[ ]  1281  
[ ]  1282      /*       3. If reph should be repositioned after the main consonant: find the
[ ]  1283       *          first consonant not ligated with main, or find the first
[ ]  1284       *          consonant that is not a potential pre-base-reordering Ra.
[ ]  1285       */
[ ]  1286      if (reph_pos == REPH_POS_AFTER_MAIN)
[ ]  1287      {
[ ]  1288        new_reph_pos = base;
[ ]  1289        while (new_reph_pos + 1 < end && info[new_reph_pos + 1].indic_position() <= POS_AFTER_MAIN)
[ ]  1290  	new_reph_pos++;
[ ]  1291        if (new_reph_pos < end)
[ ]  1292  	goto reph_move;
[ ]  1293      }
[ ]  1294  
[ ]  1295      /*       4. If reph should be positioned before post-base consonant, find
[ ]  1296       *          first post-base classified consonant not ligated with main. If no
[ ]  1297       *          consonant is found, the target position should be before the
[ ]  1298       *          first matra, syllable modifier sign or vedic sign.
[ ]  1299       */
[ ]  1300      /* This is our take on what step 4 is trying to say (and failing, BADLY). */
[ ]  1301      if (reph_pos == REPH_POS_AFTER_SUB)
[ ]  1302      {
[ ]  1303        new_reph_pos = base;
[ ]  1304        while (new_reph_pos + 1 < end &&
[ ]  1305  	     !( FLAG_UNSAFE (info[new_reph_pos + 1].indic_position()) & (FLAG (POS_POST_C) | FLAG (POS_AFTER_POST) | FLAG (POS_SMVD))))
[ ]  1306  	new_reph_pos++;
[ ]  1307        if (new_reph_pos < end)
[ ]  1308  	goto reph_move;
[ ]  1309      }
[ ]  1310  
[ ]  1311      /*       5. If no consonant is found in steps 3 or 4, move reph to a position
[ ]  1312       *          immediately before the first post-base matra, syllable modifier
[ ]  1313       *          sign or vedic sign that has a reordering class after the intended
[ ]  1314       *          reph position. For example, if the reordering position for reph
[ ]  1315       *          is post-main, it will skip above-base matras that also have a
[ ]  1316       *          post-main position.
[ ]  1317       */
[ ]  1318      reph_step_5:
[ ]  1319      {
[ ]  1320        /* Copied from step 2. */
[ ]  1321        new_reph_pos = start + 1;
[ ]  1322        while (new_reph_pos < base && !is_halant (info[new_reph_pos]))
[ ]  1323  	new_reph_pos++;
[ ]  1324  
[ ]  1325        if (new_reph_pos < base && is_halant (info[new_reph_pos]))
[ ]  1326        {
[ ]  1327  	/* ->If ZWJ or ZWNJ are following this halant, position is moved after it. */
[ ]  1328  	if (new_reph_pos + 1 < base && is_joiner (info[new_reph_pos + 1]))
[ ]  1329  	  new_reph_pos++;
[ ]  1330  	goto reph_move;
[ ]  1331        }
[ ]  1332      }
[ ]  1333      /* See https://github.com/harfbuzz/harfbuzz/issues/2298#issuecomment-615318654 */
[ ]  1334  
[ ]  1335      /*       6. Otherwise, reorder reph to the end of the syllable.
[ ]  1336       */
[ ]  1337      {
[ ]  1338        new_reph_pos = end - 1;
[ ]  1339        while (new_reph_pos > start && info[new_reph_pos].indic_position() == POS_SMVD)
[ ]  1340  	new_reph_pos--;
[ ]  1341  
[ ]  1342        /*
[ ]  1343         * If the Reph is to be ending up after a Matra,Halant sequence,
[ ]  1344         * position it before that Halant so it can interact with the Matra.
[ ]  1345         * However, if it's a plain Consonant,Halant we shouldn't do that.
[ ]  1346         * Uniscribe doesn't do this.
[ ]  1347         * TEST: U+0930,U+094D,U+0915,U+094B,U+094D
[ ]  1348         */
[ ]  1349        if (!indic_plan->uniscribe_bug_compatible &&
[ ]  1350  	  unlikely (is_halant (info[new_reph_pos])))
[ ]  1351        {
[ ]  1352  	for (unsigned int i = base + 1; i < new_reph_pos; i++)
[ ]  1353  	  if (FLAG_UNSAFE (info[i].indic_category()) & (FLAG (I_Cat(M)) | FLAG (I_Cat(MPst))))
[ ]  1354  	  {
[ ]  1355  	    /* Ok, got it. */
[ ]  1356  	    new_reph_pos--;
[ ]  1357  	  }
[ ]  1358        }
[ ]  1359  
[ ]  1360        goto reph_move;
[ ]  1361      }
[ ]  1362  
[ ]  1363      reph_move:
[ ]  1364      {
[ ]  1365        /* Move */
[ ]  1366        buffer->merge_clusters (start, new_reph_pos + 1);
[ ]  1367        hb_glyph_info_t reph = info[start];
[ ]  1368        memmove (&info[start], &info[start + 1], (new_reph_pos - start) * sizeof (info[0]));
[ ]  1369        info[new_reph_pos] = reph;
[ ]  1370  
[ ]  1371        if (start < base && base <= new_reph_pos)
[ ]  1372  	base--;
[ ]  1373      }
[ ]  1374    }
[ ]  1375  
[ ]  1376  
[ ]  1377    /*   o Reorder pre-base-reordering consonants:
[ ]  1378     *
[ ]  1379     *     If a pre-base-reordering consonant is found, reorder it according to
[ ]  1380     *     the following rules:
[ ]  1381     */
[ ]  1382  
[B]  1383    if (try_pref && base + 1 < end) /* Otherwise there can't be any pre-base-reordering Ra. */
[ ]  1384    {
[ ]  1385      for (unsigned int i = base + 1; i < end; i++)
[ ]  1386        if ((info[i].mask & indic_plan->mask_array[INDIC_PREF]) != 0)
[ ]  1387        {
[ ]  1388  	/*       1. Only reorder a glyph produced by substitution during application
[ ]  1389  	 *          of the <pref> feature. (Note that a font may shape a Ra consonant with
[ ]  1390  	 *          the feature generally but block it in certain contexts.)
[ ]  1391  	 */
[ ]  1392  	/* Note: We just check that something got substituted.  We don't check that
[ ]  1393  	 * the <pref> feature actually did it...
[ ]  1394  	 *
[ ]  1395  	 * Reorder pref only if it ligated. */
[ ]  1396  	if (_hb_glyph_info_ligated_and_didnt_multiply (&info[i]))
[ ]  1397  	{
[ ]  1398  	  /*
[ ]  1399  	   *       2. Try to find a target position the same way as for pre-base matra.
[ ]  1400  	   *          If it is found, reorder pre-base consonant glyph.
[ ]  1401  	   *
[ ]  1402  	   *       3. If position is not found, reorder immediately before main
[ ]  1403  	   *          consonant.
[ ]  1404  	   */
[ ]  1405  
[ ]  1406  	  unsigned int new_pos = base;
[ ]  1407  	  /* Malayalam / Tamil do not have "half" forms or explicit virama forms.
[ ]  1408  	   * The glyphs formed by 'half' are Chillus or ligated explicit viramas.
[ ]  1409  	   * We want to position matra after them.
[ ]  1410  	   */
[ ]  1411  	  if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer->props.script != HB_SCRIPT_TAMIL)
[ ]  1412  	  {
[ ]  1413  	    while (new_pos > start &&
[ ]  1414  		   !(is_one_of (info[new_pos - 1], FLAG (I_Cat(M)) | FLAG (I_Cat(MPst)) | FLAG (I_Cat(H)))))
[ ]  1415  	      new_pos--;
[ ]  1416  	  }
[ ]  1417  
[ ]  1418  	  if (new_pos > start && is_halant (info[new_pos - 1]))
[ ]  1419  	  {
[ ]  1420  	    /* -> If ZWJ or ZWNJ follow this halant, position is moved after it. */
[ ]  1421  	    if (new_pos < end && is_joiner (info[new_pos]))
[ ]  1422  	      new_pos++;
[ ]  1423  	  }
[ ]  1424  
[ ]  1425  	  {
[ ]  1426  	    unsigned int old_pos = i;
[ ]  1427  
[ ]  1428  	    buffer->merge_clusters (new_pos, old_pos + 1);
[ ]  1429  	    hb_glyph_info_t tmp = info[old_pos];
[ ]  1430  	    memmove (&info[new_pos + 1], &info[new_pos], (old_pos - new_pos) * sizeof (info[0]));
[ ]  1431  	    info[new_pos] = tmp;
[ ]  1432  
[ ]  1433  	    if (new_pos <= base && base < old_pos)
[ ]  1434  	      base++;
[ ]  1435  	  }
[ ]  1436  	}
[ ]  1437  
[ ]  1438  	break;
[ ]  1439        }
[ ]  1440    }
[ ]  1441  
[ ]  1442  
[ ]  1443    /* Apply 'init' to the Left Matra if it's a word start. */
[B]  1444    if (info[start].indic_position () == POS_PRE_M)
[L]  1445    {
[L]  1446      if (!start ||
[L]  1447  	!(FLAG_UNSAFE (_hb_glyph_info_get_general_category (&info[start - 1])) &
[L]  1448  	 FLAG_RANGE (HB_UNICODE_GENERAL_CATEGORY_FORMAT, HB_UNICODE_GENERAL_CATEGORY_NON_SPACING_MARK)))
[L]  1449        info[start].mask |= indic_plan->mask_array[INDIC_INIT];
[L]  1450      else
[L]  1451        buffer->unsafe_to_break (start - 1, start + 1);
[L]  1452    }
[ ]  1453  
[ ]  1454  
[ ]  1455    /*
[ ]  1456     * Finish off the clusters and go home!
[ ]  1457     */
[B]  1458    if (indic_plan->uniscribe_bug_compatible)
[ ]  1459    {
[ ]  1460      switch ((hb_tag_t) plan->props.script)
[ ]  1461      {
[ ]  1462        case HB_SCRIPT_TAMIL:
[ ]  1463  	break;
[ ]  1464  
[ ]  1465        default:
[ ]  1466  	/* Uniscribe merges the entire syllable into a single cluster... Except for Tamil.
[ ]  1467  	 * This means, half forms are submerged into the main consonant's cluster.
[ ]  1468  	 * This is unnecessary, and makes cursor positioning harder, but that's what
[ ]  1469  	 * Uniscribe does. */
[ ]  1470  	buffer->merge_clusters (start, end);
[ ]  1471  	break;
[ ]  1472      }
[ ]  1473    }
[B]  1474  }

--- Caller (1 hop): hb-ot-shaper-indic.cc:final_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*) (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1481-1495, calls hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int) at line 1487) (full body — short) ---
[B]  1481  {
[B]  1482    unsigned int count = buffer->len;
[B]  1483    if (unlikely (!count)) return false;
[ ]  1484  
[B]  1485    if (buffer->message (font, "start reordering indic final")) {
[B]  1486      foreach_syllable (buffer, start, end)
[B]  1487        final_reordering_syllable_indic (plan, buffer, start, end); <-- CALL
[B]  1488      (void) buffer->message (font, "end reordering indic final");
[B]  1489    }
[ ]  1490  
[B]  1491    HB_BUFFER_DEALLOCATE_VAR (buffer, indic_category);
[B]  1492    HB_BUFFER_DEALLOCATE_VAR (buffer, indic_position);
[ ]  1493  
[B]  1494    return false;
[B]  1495  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  hb-ot-shaper-indic.cc:final_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1481-1495, calls hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int) at line 1487)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      13       245  hb-ot-shaper-indic.cc:is_one_of(hb_glyph_info_t const&, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:55-59)
      32       160  hb-ot-shaper-indic.cc:set_indic_properties(hb_glyph_info_t&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:44-50)
      32       160  hb-ot-shaper-indic.cc:decompose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int*, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1513-1539)
       9       133  hb-ot-shaper-indic.cc:is_consonant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:72-74)
      29       101  hb-ot-shaper-indic.cc:initial_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:968-986)
      29       101  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474)  <-- enclosing
       3        68  hb-ot-shaper-indic.cc:compare_indic_order(hb_glyph_info_t const*, hb_glyph_info_t const*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:430-435)
       6        66  hb-ot-shaper-indic.cc:compose_indic(hb_ot_shape_normalize_context_t const*, unsigned int, unsigned int, unsigned int*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1546-1555)
       3        59  hb-ot-shaper-indic.cc:is_joiner(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:80-82)
      10        50  hb_indic_would_substitute_feature_t::init(hb_ot_map_t const*, unsigned int, bool)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:93-97)
       3        33  hb-ot-shaper-indic.cc:initial_reordering_consonant_syllable(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:470-939)
       0        22  hb-ot-shaper-indic.cc:is_halant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:86-88)
       3        17  hb-ot-shaper-indic.cc:initial_reordering_standalone_cluster(hb_ot_shape_plan_t const*, hb_face_t*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:946-961)
       2        10  hb-ot-shaper-indic.cc:collect_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:241-265)
       2        10  hb-ot-shaper-indic.cc:override_features_indic(hb_ot_shape_planner_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:269-272)
... (9 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=2  hb-ot-shaper-indic.cc:final_reordering_indic(hb_ot_shape_plan_t const*, hb_font_t*, hb_buffer_t*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1481-1495) ---
  d=2   L1485  T=2 F=0  T=10 F=0  if (buffer->message (font, "start reordering indic final"...
--- d=1  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474) ---
  d=1   L1030  T=0 F=29  T=0 F=101  if (virama_glyph)
  d=1   L1056  T=31 F=1  T=128 F=10  for (base = start; base < end; base++)
  d=1   L1057  T=28 F=3  T=91 F=37  if (info[base].indic_position() >= POS_BASE_C)
  d=1   L1059  T=0 F=28  T=0 F=91  if (try_pref && base + 1 < end)
  d=1   L1080  T=0 F=28  T=0 F=91  if (buffer->props.script == HB_SCRIPT_MALAYALAM)
  d=1   L1099  T=2 F=0  T=0 F=17  if (start < base && info[base].indic_position() > POS_BAS...  <-- BLOCKER
  d=1   L1099  T=2 F=26  T=17 F=74  if (start < base && info[base].indic_position() > POS_BAS...  <-- BLOCKER
  d=1   L1103  T=1 F=0  T=10 F=0  if (base == end && start < base &&
  d=1   L1103  T=1 F=28  T=10 F=91  if (base == end && start < base &&
  d=1   L1104  T=0 F=1  T=0 F=10  is_one_of (info[base - 1], FLAG (I_Cat(ZWJ))))
  d=1   L1106  T=28 F=1  T=91 F=10  if (base < end)
  d=1   L1107  T=0 F=28  T=17 F=74  while (start < base &&
  d=1   L1108  T=0 F=0  T=0 F=17  is_one_of (info[base], (FLAG (I_Cat(N)) | FLAG (I_Cat(H)))))
  d=1   L1140  T=2 F=27  T=26 F=75  if (start + 1 < end && start < base) /* Otherwise there c...
  d=1   L1140  T=0 F=2  T=22 F=4  if (start + 1 < end && start < base) /* Otherwise there c...
  d=1   L1143  T=0 F=0  T=5 F=17  unsigned int new_pos = base == end ? base - 2 : base - 1;
  d=1   L1149  T=0 F=0  T=22 F=0  if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer...
  d=1   L1149  T=0 F=0  T=22 F=0  if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer...
  d=1   L1152  T=0 F=0  T=4 F=18  while (new_pos > start &&
  d=1   L1153  T=0 F=0  T=0 F=4  !(is_one_of (info[new_pos], (FLAG (I_Cat(M)) | FLAG (I_Ca...
  d=1   L1159  T=0 F=0  T=5 F=17  if (is_halant (info[new_pos]) &&
  d=1   L1160  T=0 F=0  T=5 F=0  info[new_pos].indic_position() != POS_PRE_M)
  d=1   L1167  T=0 F=0  T=5 F=0  if (new_pos + 1 < end)
  d=1   L1170  T=0 F=0  T=0 F=5  if (info[new_pos + 1].indic_category() == I_Cat(ZWJ))
  d=1   L1193  T=0 F=0  T=0 F=22  if (start < new_pos && info[new_pos].indic_position () !=...
  d=1   L1214  T=0 F=0  T=23 F=6  for (unsigned int i = start; i < base; i++)
  d=1   L1215  T=0 F=0  T=16 F=7  if (info[i].indic_position () == POS_PRE_M) {
  d=1   L1241  T=2 F=27  T=26 F=75  if (start + 1 < end &&
  d=1   L1242  T=0 F=2  T=0 F=26  info[start].indic_position() == POS_RA_TO_BECOME_REPH &&
  d=1   L1383  T=0 F=29  T=0 F=101  if (try_pref && base + 1 < end) /* Otherwise there can't ...
  d=1   L1444  T=0 F=29  T=17 F=84  if (info[start].indic_position () == POS_PRE_M)
  d=1   L1446  T=0 F=0  T=1 F=16  if (!start ||
  d=1   L1447  T=0 F=0  T=5 F=11  !(FLAG_UNSAFE (_hb_glyph_info_get_general_category (&info...
  d=1   L1458  T=0 F=29  T=0 F=101  if (indic_plan->uniscribe_bug_compatible)

[off-chain: 83 additional divergent branches across 13 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=2bbb97abff5a2d66, size=22 bytes, fuzzer=naive_ctx, trial=1, discovered_at=16008s, mutation_op=BytesRandInsertMutator,QwordAddMutator,TokenReplace,BytesDeleteMutator,ByteDecMutator):
  0000: 75 75 75 75 80 75 75 75 75 0a 00 00 00 09 00 00   uuuu.uuuu.......
  0010: ff 00 00 00 0d 00                                 ......
Seed 2 (id=df72f775e7cfce96, size=70 bytes, fuzzer=naive_ctx, trial=1, discovered_at=60801s, mutation_op=BytesDeleteMutator,BytesInsertMutator,BytesInsertMutator,BitFlipMutator,WordInterestingMutator):
  0000: 00 00 81 0a 00 6e 6e 6e 40 75 75 0a 00 00 01 0a   .....nnn@uu.....
  0010: 00 00 40 0a 00 00 ff 97 97 97 0a 80 ff 97 97 97   ..@.............
  0020: 97 97 97 97 97 97 97 97 97 97 97 97 98 97 97 97   ................
  0030: 6e 6e 6e 6e 6e 6e 97 6e 02 00 6e 6e 40 75 75 2d   nnnnnn.n..nn@uu-

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=1d1c5f97f339da84, size=63 bytes, fuzzer=naive, trial=2, discovered_at=637s, mutation_op=ByteNegMutator,BytesExpandMutator,BytesDeleteMutator,BytesInsertCopyMutator):
  0000: 90 0c 00 00 c0 09 00 00 90 0c 00 00 bf 09 00 00   ................
  0010: 01 ea ff 0c 18 09 00 00 90 0c 00 00 bf 09 00 00   ................
  0020: 01 ea ff 0c 0c 0c 0c 21 0c 0c 0c 0c 0c f4 0c ff   .......!........
  0030: 18 18 18 18 18 18 18 28 20 20 01 09 00 00 00      .......(  .....
Seed 2 (id=1c43755ab7a6feba, size=60 bytes, fuzzer=naive, trial=2, discovered_at=20047s, mutation_op=BytesCopyMutator,CrossoverInsertMutator,BytesDeleteMutator):
  0000: 00 1a 1a 1a 4d 0c 00 00 1d 0d 00 00 00 09 00 00   ....M...........
  0010: 00 0d 00 00 60 66 63 ff 4d 0c 00 00 1e 0d 00 00   ....`fc.M.......
  0020: 00 09 00 00 00 0d 00 00 5f 66 63 00 00 1e 0d 00   ........_fc.....
  0030: 00 00 09 00 00 00 0d 00 00 0d 00 00               ............
Seed 3 (id=21ec1043661fc076, size=91 bytes, fuzzer=naive, trial=2, discovered_at=30492s, mutation_op=BitFlipMutator,ByteFlipMutator,BytesExpandMutator,BytesDeleteMutator):
  0000: 01 63 73 00 20 22 22 42 22 e9 01 09 00 00 ef ef   .cs. ""B".......
  0010: ef ee 01 f7 00 00 01 f7 dd e0 00 00 00 00 00 00   ................
  0020: 00 00 00 19 ff 00 20 20 00 00 20 21 00 00 00 00   ......  .. !....
  0030: 00 00 19 ff 09 00 00 e3 09 00 00 3f 09 00 00 9a   ...........?....
Seed 4 (id=06267a9c1a97d696, size=64 bytes, fuzzer=naive, trial=2, discovered_at=34594s, mutation_op=BytesExpandMutator,BytesDeleteMutator):
  0000: 01 09 00 00 01 09 00 00 90 09 00 00 bf 0c 00 00   ................
  0010: bf 09 00 00 01 09 00 00 bf 0c 00 00 bf 0c 00 00   ................
  0020: bf 09 00 00 01 09 00 00 00 09 00 00 b7 09 00 00   ................
  0030: 90 09 00 00 bf 0c 00 00 bf 09 00 00 01 09 00 00   ................
Seed 5 (id=0ce3894f21596ebe, size=60 bytes, fuzzer=naive, trial=2, discovered_at=49677s, mutation_op=BytesDeleteMutator,ByteNegMutator,BytesDeleteMutator):
  0000: 00 1a 1a 1a 4d 0c 00 00 1d 0d 00 00 00 09 00 00   ....M...........
  0010: 00 0d 00 00 a0 66 63 ff 4d 0c 00 00 1e 0d 00 00   .....fc.M.......
  0020: 00 09 00 00 00 0d 00 00 60 66 63 ff 4d 0c 00 00   ........`fc.M...
  0030: 1e 0d 00 00 00 09 00 00 00 0d 00 00               ............


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  75(u)x1 00(.)x1                     01(.)x5 90(.)x2 00(.)x2 10(.)x1     PARTIAL
   0x0001  75(u)x1 00(.)x1                     09(.)x3 0c(.)x2 1a(.)x2 9e(.)x2 +1u  DIFFER
   0x0002  75(u)x1 81(.)x1                     00(.)x4 1a(.)x2 9e(.)x2 73(s)x1 +1u  DIFFER
   0x0003  75(u)x1 0a(.)x1                     00(.)x6 1a(.)x2 9e(.)x2             DIFFER
   0x0004  80(.)x1 00(.)x1                     c0(.)x2 4d(M)x2 01(.)x2 9e(.)x2 +2u  DIFFER
   0x0005  75(u)x1 6e(n)x1                     0c(.)x3 09(.)x2 9e(.)x2 22(")x1 +2u  DIFFER
   0x0006  75(u)x1 6e(n)x1                     00(.)x6 9e(.)x2 22(")x1 09(.)x1     DIFFER
   0x0007  75(u)x1 6e(n)x1                     00(.)x7 9e(.)x2 42(B)x1             DIFFER
   0x0008  75(u)x1 40(@)x1                     90(.)x3 09(.)x3 1d(.)x2 22(")x1 +1u  DIFFER
   0x0009  0a(.)x1 75(u)x1                     09(.)x3 0d(.)x2 1c(.)x2 0c(.)x1 +2u  DIFFER
   0x000a  00(.)x1 75(u)x1                     00(.)x7 09(.)x2 01(.)x1             PARTIAL
   0x000b  00(.)x1 0a(.)x1                     00(.)x6 09(.)x2 9a(.)x1 af(.)x1     PARTIAL
   0x000c  00(.)x2                             00(.)x4 bf(.)x3 9a(.)x1 af(.)x1 +1u  PARTIAL
   0x000d  09(.)x1 00(.)x1                     09(.)x3 0c(.)x2 00(.)x1 fa(.)x1 +3u  PARTIAL
   0x000e  00(.)x1 01(.)x1                     00(.)x6 09(.)x2 ef(.)x1 af(.)x1     PARTIAL
   0x000f  00(.)x1 0a(.)x1                     00(.)x7 ef(.)x1 af(.)x1 09(.)x1     PARTIAL
   0x0010  ff(.)x1 00(.)x1                     00(.)x3 bf(.)x2 01(.)x1 ef(.)x1 +3u  PARTIAL
   0x0011  00(.)x2                             09(.)x3 0d(.)x2 ea(.)x1 ee(.)x1 +3u  DIFFER
   0x0012  00(.)x1 40(@)x1                     00(.)x4 ff(.)x2 01(.)x1 9a(.)x1 +2u  PARTIAL
   0x0013  00(.)x1 0a(.)x1                     00(.)x3 0c(.)x1 f7(.)x1 9a(.)x1 +4u  PARTIAL
   0x0014  0d(.)x1 00(.)x1                     00(.)x2 18(.)x1 60(`)x1 01(.)x1 +5u  PARTIAL
   0x0015  00(.)x2                             09(.)x4 66(f)x2 9a(.)x2 00(.)x1 +1u  PARTIAL
   0x0016  ff(.)x1                             00(.)x5 63(c)x2 01(.)x1 0c(.)x1 +1u  DIFFER
   0x0017  97(.)x1                             00(.)x5 ff(.)x3 f7(.)x1 bf(.)x1     DIFFER
   0x0018  97(.)x1                             4d(M)x2 bf(.)x2 09(.)x2 90(.)x1 +3u  DIFFER
   0x0019  97(.)x1                             0c(.)x5 00(.)x2 e0(.)x1 09(.)x1 +1u  DIFFER
   0x001a  0a(.)x1                             00(.)x9 09(.)x1                     DIFFER
   0x001b  80(.)x1                             00(.)x8 0b(.)x2                     DIFFER
   0x001c  ff(.)x1                             bf(.)x3 1e(.)x2 00(.)x2 09(.)x2 +1u  DIFFER
   0x001d  97(.)x1                             00(.)x3 0d(.)x2 09(.)x1 0c(.)x1 +3u  DIFFER
   0x001e  97(.)x1                             00(.)x7 ff(.)x1 ed(.)x1 09(.)x1     DIFFER
   0x001f  97(.)x1                             00(.)x7 bf(.)x2 ff(.)x1             DIFFER
   0x0020  97(.)x1                             00(.)x5 0c(.)x2 01(.)x1 bf(.)x1 +1u  DIFFER
   0x0021  97(.)x1                             09(.)x5 00(.)x3 ea(.)x1 b6(.)x1     DIFFER
   0x0022  97(.)x1                             00(.)x8 ff(.)x1 09(.)x1             DIFFER
   0x0023  97(.)x1                             00(.)x6 bf(.)x2 0c(.)x1 19(.)x1     DIFFER
   0x0024  97(.)x1                             00(.)x3 09(.)x2 0c(.)x1 ff(.)x1 +3u  DIFFER
   0x0025  97(.)x1                             00(.)x3 0d(.)x2 09(.)x2 0c(.)x1 +2u  DIFFER
   0x0026  97(.)x1                             00(.)x6 0c(.)x1 20( )x1 27(')x1 +1u  DIFFER
   0x0027  97(.)x1                             00(.)x5 01(.)x2 21(!)x1 20( )x1 +1u  DIFFER
   ... (24 more divergent offsets)
==== MECHANISM CONTEXT (involved fuzzers only) ====
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

--- naive_ctx ---
**Instrumentation**: naive's SanitizerCoverage edge counters, but the
executor installs a `CtxHook` (`HookableInProcessExecutor`). The hook
keeps a running hash of the current call context (caller chain) and
folds it into the edge-map index, so the same basic-block edge is
recorded at different map slots depending on the call path that
reached it.

**Feedback**: the same `MaxMapFeedback` edge-bucket signal as naive,
computed over the context-indexed map — a "new bucket" is a new
(call-context, edge) pair rather than a bare edge.

**Mutators**: naive's havoc + token stack. No `I2SRandReplace`, no
CMP_MAP. Stages are `[mutator]` (`LineageMutator`, names captured).

**Observed `mutation_op` in seed metadata**: havoc/token names only;
no ParentInfo-only / dash rows.

**Per-execution cost**: one edge-counter increment per executed edge
plus a context-hash update per call/return.

==== TASK ====
ANALYZE THIS BRANCH IN ISOLATION. Do NOT compare against templates/. Naming an existing template here anchors the later cross-branch classification pass.

WRITE EXACTLY ONE FILE:
  prompts_b/harfbuzz_5878.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5878,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive_ctx>naive (ctx_coverage)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5878 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5878 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5878 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).