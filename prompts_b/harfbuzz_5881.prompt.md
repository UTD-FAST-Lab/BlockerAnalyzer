==== BLOCKER ====
Target: harfbuzz
Branch ID: 5881
Location: /src/harfbuzz/src/hb-ot-shaper-indic.cc:1149:56
Enclosing function: hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)
Source line:     if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer->props.script != HB_SCRIPT_TAMIL)
Globally blocked side: F  (false branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                           10        0          0  winner (I2S vs cmplog)
cmplog                           1        9          0  loser (I2S vs naive)
value_profile                    9        1          0  REFERENCE
value_profile_cmplog             6        4          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             ?        ?          ?  REFERENCE
minimizer                        ?        ?          ?  REFERENCE
fast                             ?        ?          ?  REFERENCE
grimoire                         1        9          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: naive > cmplog  [delta: I2S] ---
  subject 11  (cmplog vs naive, admissible)
  winner: resolved=10/10  blocked=0  unreached=0
  loser:  resolved=1/10  blocked=9  unreached=0
  avg duration blocked: winner=3.40h  loser=20.90h
  avg hitcount on branch: winner=74  loser=0
  prob_div=0.90  dur_div=17.50h  hit_div=74
  subject-level: delta_AUC=54905220.0  p_AUC=0.0002  delta_Final=812.8  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/harfbuzz/5881/{W,L}/branch_coverage_show.txt

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
[B]  1099        if (start < base && info[base].indic_position() > POS_BASE_C)
[ ]  1100  	base--;
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
[B]  1141    {
[ ]  1142      /* If we lost track of base, alas, position before last thingy. */
[B]  1143      unsigned int new_pos = base == end ? base - 2 : base - 1;
[ ]  1144  
[ ]  1145      /* Malayalam / Tamil do not have "half" forms or explicit virama forms.
[ ]  1146       * The glyphs formed by 'half' are Chillus or ligated explicit viramas.
[ ]  1147       * We want to position matra after them.
[ ]  1148       */
[B]  1149      if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer->props.script != HB_SCRIPT_TAMIL) <-- BLOCKER
[L]  1150      {
[L]  1151      search:
[L]  1152        while (new_pos > start &&
[L]  1153  	     !(is_one_of (info[new_pos], (FLAG (I_Cat(M)) | FLAG (I_Cat(MPst)) | FLAG (I_Cat(H))))))
[L]  1154  	new_pos--;
[ ]  1155  
[ ]  1156        /* If we found no Halant we are done.
[ ]  1157         * Otherwise only proceed if the Halant does
[ ]  1158         * not belong to the Matra itself! */
[L]  1159        if (is_halant (info[new_pos]) &&
[L]  1160  	  info[new_pos].indic_position() != POS_PRE_M)
[ ]  1161        {
[ ]  1162  #if 0 // See comment above
[ ]  1163  	/* -> If ZWJ or ZWNJ follow this halant, position is moved after it. */
[ ]  1164  	if (new_pos + 1 < end && is_joiner (info[new_pos + 1]))
[ ]  1165  	  new_pos++;
[ ]  1166  #endif
[ ]  1167  	if (new_pos + 1 < end)
[ ]  1168  	{
[ ]  1169  	  /* -> If ZWJ follows this halant, matra is NOT repositioned after this halant. */
[ ]  1170  	  if (info[new_pos + 1].indic_category() == I_Cat(ZWJ))
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
[ ]  1187  	}
[ ]  1188        }
[L]  1189        else
[L]  1190  	new_pos = start; /* No move. */
[L]  1191      }
[ ]  1192  
[B]  1193      if (start < new_pos && info[new_pos].indic_position () != POS_PRE_M)
[W]  1194      {
[ ]  1195        /* Now go see if there's actually any matras... */
[W]  1196        for (unsigned int i = new_pos; i > start; i--)
[W]  1197  	if (info[i - 1].indic_position () == POS_PRE_M)
[W]  1198  	{
[W]  1199  	  unsigned int old_pos = i - 1;
[W]  1200  	  if (old_pos < base && base <= new_pos) /* Shouldn't actually happen. */
[ ]  1201  	    base--;
[ ]  1202  
[W]  1203  	  hb_glyph_info_t tmp = info[old_pos];
[W]  1204  	  memmove (&info[old_pos], &info[old_pos + 1], (new_pos - old_pos) * sizeof (info[0]));
[W]  1205  	  info[new_pos] = tmp;
[ ]  1206  
[ ]  1207  	  /* Note: this merge_clusters() is intentionally *after* the reordering.
[ ]  1208  	   * Indic matra reordering is special and tricky... */
[W]  1209  	  buffer->merge_clusters (new_pos, hb_min (end, base + 1));
[ ]  1210  
[W]  1211  	  new_pos--;
[W]  1212  	}
[B]  1213      } else {
[B]  1214        for (unsigned int i = start; i < base; i++)
[B]  1215  	if (info[i].indic_position () == POS_PRE_M) {
[B]  1216  	  buffer->merge_clusters (i, hb_min (end, base + 1));
[B]  1217  	  break;
[B]  1218  	}
[B]  1219      }
[B]  1220    }
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
[B]  1445    {
[B]  1446      if (!start ||
[B]  1447  	!(FLAG_UNSAFE (_hb_glyph_info_get_general_category (&info[start - 1])) &
[B]  1448  	 FLAG_RANGE (HB_UNICODE_GENERAL_CATEGORY_FORMAT, HB_UNICODE_GENERAL_CATEGORY_NON_SPACING_MARK)))
[B]  1449        info[start].mask |= indic_plan->mask_array[INDIC_INIT];
[B]  1450      else
[B]  1451        buffer->unsafe_to_break (start - 1, start + 1);
[B]  1452    }
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
     142        42  hb-ot-shaper-indic.cc:is_consonant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:72-74)
      74        18  hb-ot-shaper-indic.cc:compare_indic_order(hb_glyph_info_t const*, hb_glyph_info_t const*)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:430-435)
      61        18  hb-ot-shaper-indic.cc:is_joiner(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:80-82)
       0        14  hb-ot-shaper-indic.cc:is_halant(hb_glyph_info_t const&)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:86-88)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  hb-ot-shaper-indic.cc:final_reordering_syllable_indic(hb_ot_shape_plan_t const*, hb_buffer_t*, unsigned int, unsigned int)  (/src/harfbuzz/src/hb-ot-shaper-indic.cc:1017-1474) ---
  d=1   L1099  T=0 F=12  T=0 F=0  if (start < base && info[base].indic_position() > POS_BAS...
  d=1   L1099  T=12 F=59  T=0 F=126  if (start < base && info[base].indic_position() > POS_BAS...
  d=1   L1107  T=12 F=59  T=0 F=126  while (start < base &&
  d=1   L1108  T=0 F=12  T=0 F=0  is_one_of (info[base], (FLAG (I_Cat(N)) | FLAG (I_Cat(H)))))
  d=1   L1140  T=29 F=3  T=14 F=0  if (start + 1 < end && start < base) /* Otherwise there c...
  d=1   L1143  T=17 F=12  T=14 F=0  unsigned int new_pos = base == end ? base - 2 : base - 1;
  d=1   L1149  T=0 F=29  T=14 F=0  if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer...  <-- BLOCKER
  d=1   L1149  T=29 F=0  T=14 F=0  if (buffer->props.script != HB_SCRIPT_MALAYALAM && buffer...  <-- BLOCKER
  d=1   L1152  T=0 F=0  T=3 F=12  while (new_pos > start &&
  d=1   L1153  T=0 F=0  T=1 F=2  !(is_one_of (info[new_pos], (FLAG (I_Cat(M)) | FLAG (I_Ca...
  d=1   L1159  T=0 F=0  T=0 F=14  if (is_halant (info[new_pos]) &&
  d=1   L1193  T=12 F=2  T=0 F=0  if (start < new_pos && info[new_pos].indic_position () !=...
  d=1   L1193  T=14 F=15  T=0 F=14  if (start < new_pos && info[new_pos].indic_position () !=...
  d=1   L1196  T=21 F=12  T=0 F=0  for (unsigned int i = new_pos; i > start; i--)
  d=1   L1197  T=15 F=6  T=0 F=0  if (info[i - 1].indic_position () == POS_PRE_M)
  d=1   L1200  T=15 F=0  T=0 F=0  if (old_pos < base && base <= new_pos) /* Shouldn't actua...
  d=1   L1200  T=0 F=15  T=0 F=0  if (old_pos < base && base <= new_pos) /* Shouldn't actua...
  d=1   L1242  T=0 F=32  T=0 F=14  info[start].indic_position() == POS_RA_TO_BECOME_REPH &&
  d=1   L1446  T=0 F=20  T=2 F=4  if (!start ||
  d=1   L1447  T=4 F=16  T=2 F=2  !(FLAG_UNSAFE (_hb_glyph_info_get_general_category (&info...

[off-chain: 39 additional divergent branches across 5 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take false branch) ====
Seed 1 (id=05c4b415b5d0250e, size=101 bytes, fuzzer=naive, trial=1, discovered_at=25163s, mutation_op=BytesSetMutator,BytesInsertCopyMutator,QwordAddMutator,DwordInterestingMutator):
  0000: 00 00 00 00 00 00 00 00 00 00 00 0c 0c 0c 0c 0c   ................
  0010: 0c 0c 0c 00 00 00 00 00 cb 84 f4 00 00 00 00 00   ................
  0020: 00 00 00 00 00 00 64 0c 00 c8 0b 00 00 0c 20 00   ......d....... .
  0030: 00 c8 0b 00 00 b1 0c 00 00 10 fc 00 43 97 9a 81   ............C...
Seed 2 (id=13ec4b96e74e5533, size=120 bytes, fuzzer=naive, trial=1, discovered_at=25359s, mutation_op=WordInterestingMutator,CrossoverInsertMutator,ByteFlipMutator,DwordInterestingMutator):
  0000: 5e 5e ff 0a 1a 00 00 03 e8 00 00 00 00 00 20 00   ^^............ .
  0010: 20 00 00 00 00 00 61 66 63 ff 00 01 00 00 20 00    .....afc..... .
  0020: 7f 10 00 ff dd 20 00 10 00 00 00 cb 00 00 0c 00   ..... ..........
  0030: ff e3 00 cb 83 0c 00 00 c8 0b 00 00 cb 0c 00 00   ................
Seed 3 (id=01fa62accae6f0d3, size=126 bytes, fuzzer=naive, trial=1, discovered_at=28756s, mutation_op=ByteDecMutator,BytesCopyMutator):
  0000: 0c 0c 0c bd bd bf bd bc cb cb cb bd cb cb cb cb   ................
  0010: cb 00 0c 72 61 66 63 ff 00 01 00 00 20 00 7f 10   ...rafc..... ...
  0020: 00 ff dd 20 00 10 00 00 00 cb 00 00 0c 00 ff e3   ... ............
  0030: 00 cb 84 0c 00 00 c8 0b 00 00 cb 0c 00 00 0c 20   ............... 
Seed 4 (id=23226f58b250bfb5, size=119 bytes, fuzzer=naive, trial=1, discovered_at=28855s, mutation_op=ByteRandMutator,TokenReplace,DwordInterestingMutator,WordAddMutator,BytesRandInsertMutator,DwordAddMutator,ByteAddMutator):
  0000: bd bf bd bd cb cb cb bd cb cb cb cb cb 00 0c 72   ...............r
  0010: 61 64 75 70 65 01 00 00 20 00 7f 10 00 ff 01 87   adupe... .......
  0020: 87 87 00 00 cb cb cb cb cb cb 10 40 00 00 00 00   ...........@....
  0030: 00 0c 00 ff e3 00 cb 84 0c 1b 00 c8 0b 00 ff cb   ................
Seed 5 (id=031d76132b7a7ce5, size=106 bytes, fuzzer=naive, trial=1, discovered_at=41507s, mutation_op=BytesExpandMutator,WordInterestingMutator):
  0000: 0c 00 00 cb 61 6e 2d 00 0b 00 00 1e 00 00 00 00   ....an-.........
  0010: 00 00 00 00 01 0c 00 00 cb 06 06 06 06 06 06 06   ................
  0020: 06 06 06 e0 0c 0b 00 00 cb 0b 00 00 cb 0b cb 0b   ................
  0030: 00 00 cb 0b 00 00 cb 0c 00 00 cb 0b 00 00 cb 0c   ................

==== Loser-blocking seeds (take true branch) ====
Seed 1 (id=190acdbcfb1cdc61, size=29 bytes, fuzzer=cmplog, trial=1, discovered_at=452s, mutation_op=ByteDecMutator,DwordInterestingMutator,BytesDeleteMutator):
  0000: 00 00 00 00 01 09 00 00 03 0d 00 00 00 ff 00 00   ................
  0010: ff 00 00 00 00 09 00 00 03 0d 00 00 00            .............
Seed 2 (id=076e7903a85d5b86, size=49 bytes, fuzzer=cmplog, trial=1, discovered_at=493s, mutation_op=TokenReplace):
  0000: 00 0c 00 00 01 0d 00 00 36 00 00 00 14 7f 00 00   ........6.......
  0010: 00 00 00 00 36 00 00 00 00 00 0e 00 fe 0d 00 00   ....6...........
  0020: 36 00 00 00 0e 00 03 00 4d 1b ff 00 00 09 75 65   6.......M.....ue
  0030: 2d                                                -
Seed 3 (id=2b46789b4ee10dbf, size=68 bytes, fuzzer=cmplog, trial=1, discovered_at=714s, mutation_op=BytesCopyMutator,DwordAddMutator,BytesRandSetMutator,BytesCopyMutator,BytesExpandMutator,BitFlipMutator,WordAddMutator):
  0000: 20 0a 00 00 00 fc ff ff 3f 0a 00 00 00 0d 00 00    .......?.......
  0010: 00 2d 00 00 40 0a 00 00 00 0d 00 00 8a 8a 8a 8a   .-..@...........
  0020: 8a 8a 8a 8a 8a 8a 3d 00 02 00 00 00 3d 3d 3e 00   ......=.....==>.
  0030: 02 00 00 00 0d 00 fe 1c 00 71 2e 00 00 0d 71 2e   .........q....q.
Seed 4 (id=3f277efc18d3587c, size=62 bytes, fuzzer=cmplog, trial=1, discovered_at=811s, mutation_op=ByteRandMutator,WordAddMutator):
  0000: 01 0a 00 00 00 0d 00 00 40 0b 00 ff ff ff 3f 00   ........@.....?.
  0010: 00 0d 00 10 ff fe 00 00 40 72 0a 00 00 00 0d 00   ........@r......
  0020: f0 f0 f0 f0 f0 f0 f0 f0 f0 f0 f0 64 ee ff 0d 00   ...........d....
  0030: fe 1b 11 fe 1b 11 71 6e 71 6e 01 00 7f 0d         ......qnqn....
Seed 5 (id=0e787421a9984e86, size=68 bytes, fuzzer=cmplog, trial=1, discovered_at=812s, mutation_op=BytesRandInsertMutator,TokenInsert,ByteAddMutator,BytesInsertCopyMutator,BytesExpandMutator):
  0000: 00 0a e2 00 2c 0d 01 00 bf 0a 00 00 00 0d 00 00   ....,...........
  0010: 00 0d 00 00 06 70 63 2d 68 61 6e 74 63 2d 68 61   .....pc-hantc-ha
  0020: 6e 74 2d 68 6b 00 00 00 0d 00 00 00 0d 00 00 06   nt-hk...........
  0030: 70 63 a1 a1 a1 a1 a1 a1 a1 fe 00 00 10 00 71 6e   pc............qn


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0000  00(.)x3 0c(.)x2 0b(.)x2 5e(^)x1 +2u  00(.)x7 20( )x1 01(.)x1 0c(.)x1     PARTIAL
   0x0001  00(.)x3 0b(.)x2 5e(^)x1 0c(.)x1 +3u  0a(.)x4 00(.)x3 0c(.)x2 01(.)x1     PARTIAL
   0x0002  00(.)x4 0c(.)x2 0b(.)x2 ff(.)x1 +1u  00(.)x8 e2(.)x2                     PARTIAL
   0x0003  00(.)x4 bd(.)x2 0b(.)x2 0a(.)x1 +1u  00(.)x8 fe(.)x1 30(0)x1             PARTIAL
   0x0006  00(.)x4 64(d)x2 bd(.)x1 cb(.)x1 +2u  00(.)x5 01(.)x3 ff(.)x1 20( )x1     PARTIAL
   0x000a  00(.)x5 cb(.)x2 2d(-)x2 0b(.)x1     00(.)x7 04(.)x1 ff(.)x1 df(.)x1     PARTIAL
   0x000b  00(.)x4 68(h)x2 0c(.)x1 bd(.)x1 +2u  00(.)x7 ff(.)x1 03(.)x1 20( )x1     PARTIAL
   0x000f  00(.)x5 0c(.)x1 cb(.)x1 72(r)x1 +2u  00(.)x7 03(.)x1 36(6)x1 53(S)x1     PARTIAL
   0x0010  00(.)x3 c2(.)x2 0c(.)x1 20( )x1 +3u  00(.)x6 ff(.)x2 bf(.)x1 0e(.)x1     PARTIAL
   0x0012  0c(.)x2 00(.)x2 0b(.)x2 75(u)x1 +3u  00(.)x10                            PARTIAL
   0x0013  00(.)x5 72(r)x1 70(p)x1 ff(.)x1 +2u  00(.)x7 10(.)x1 3f(?)x1 27(')x1     PARTIAL
   0x0017  00(.)x6 66(f)x1 ff(.)x1 2d(-)x1 +1u  00(.)x7 2d(-)x1 24($)x1 10(.)x1     PARTIAL
   0x001b  00(.)x6 01(.)x1 10(.)x1 06(.)x1 +1u  00(.)x8 74(t)x1 24($)x1             PARTIAL
   0x001c  00(.)x7 20( )x1 06(.)x1 0c(.)x1     00(.)x3 fe(.)x2 8a(.)x1 63(c)x1 +3u  PARTIAL
   0x0027  00(.)x5 0c(.)x1 10(.)x1 cb(.)x1 +2u  00(.)x5 f0(.)x1 05(.)x1 10(.)x1     PARTIAL
   0x0028  00(.)x6 cb(.)x2 b6(.)x1 0b(.)x1     4d(M)x2 02(.)x1 f0(.)x1 0d(.)x1 +3u  PARTIAL
   0x002a  00(.)x5 0b(.)x3 10(.)x1 14(.)x1     ff(.)x3 00(.)x3 f0(.)x1 20( )x1     PARTIAL
   0x002b  00(.)x7 cb(.)x1 40(@)x1 01(.)x1     00(.)x4 64(d)x1 ff(.)x1 20( )x1 +1u  PARTIAL
   0x002c  00(.)x7 0c(.)x2 cb(.)x1             00(.)x3 3d(=)x1 ee(.)x1 0d(.)x1 +2u  PARTIAL
   0x002f  00(.)x6 0b(.)x2 e3(.)x1 0c(.)x1     00(.)x4 65(e)x1 06(.)x1 ff(.)x1 +1u  PARTIAL
   0x0033  00(.)x5 cb(.)x1 0c(.)x1 ff(.)x1 +2u  00(.)x3 fe(.)x1 a1(.)x1 02(.)x1     PARTIAL
   0x0035  00(.)x4 0c(.)x2 b1(.)x1 7a(z)x1 +2u  00(.)x3 11(.)x1 a1(.)x1 05(.)x1     PARTIAL
   0x003a  00(.)x3 cb(.)x2 0b(.)x2 fc(.)x1 +2u  01(.)x2 00(.)x2 2e(.)x1 f0(.)x1     PARTIAL
   0x003b  00(.)x6 0c(.)x1 c8(.)x1 0b(.)x1 +1u  00(.)x4 ff(.)x1 02(.)x1             PARTIAL
   0x003c  00(.)x5 43(C)x1 cb(.)x1 0b(.)x1 +2u  00(.)x4 7f(.)x1 10(.)x1             PARTIAL
   0x003e  00(.)x3 0c(.)x3 9a(.)x1 ff(.)x1 +2u  71(q)x2 00(.)x2 ff(.)x1             PARTIAL
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
  prompts_b/harfbuzz_5881.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 5881,
  "target": "harfbuzz",
  "summary_one_line": "string, <=25 words, the input feature required to take the winning side",
  "pair_decision": "single_feature",
    // pick EXACTLY ONE of: "single_feature" | "multi_feature"
    // decisive pairs at this branch: [naive>cmplog (I2S)]
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 5881 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 5881 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 5881 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).