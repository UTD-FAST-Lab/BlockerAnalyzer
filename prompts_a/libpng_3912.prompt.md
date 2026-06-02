==== BLOCKER ====
Target: libpng
Branch ID: 3912
Location: /src/libpng/pngrtran.c:1493:8
Enclosing function: OSS_FUZZ_png_init_read_transformations
Source line:    if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            0       10          0  loser (I2S vs cmplog)
cmplog                           9        1          0  winner (I2S vs naive)
value_profile                    6        4          0  REFERENCE
value_profile_cmplog            10        0          0  REFERENCE
naive_ctx                        ?        ?          ?  REFERENCE
naive_ngram4                     ?        ?          ?  REFERENCE
mopt                             1        9          0  REFERENCE
minimizer                        0       10          0  REFERENCE
fast                             1        9          0  REFERENCE
grimoire                         8        2          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'naive']
REFERENCE fuzzers (auxiliary context only):     ['value_profile', 'value_profile_cmplog', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: cmplog > naive  [delta: I2S] ---
  subject 21  (cmplog vs naive, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=0/10  blocked=10  unreached=0
  avg duration blocked: winner=3.30h  loser=24.00h
  avg hitcount on branch: winner=57  loser=0
  prob_div=0.90  dur_div=20.70h  hit_div=57
  subject-level: delta_AUC=22677480.0  p_AUC=0.0002  delta_Final=307.4  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3912/{W,L}/branch_coverage_show.txt

--- Enclosing function: OSS_FUZZ_png_init_read_transformations (/src/libpng/pngrtran.c:1292-1933) ---
[ ]  1290  void /* PRIVATE */
[ ]  1291  png_init_read_transformations(png_structrp png_ptr)
[B]  1292  {
[B]  1293     png_debug(1, "in png_init_read_transformations");
[ ]  1294  
[ ]  1295     /* This internal function is called from png_read_start_row in pngrutil.c
[ ]  1296      * and it is called before the 'rowbytes' calculation is done, so the code
[ ]  1297      * in here can change or update the transformations flags.
[ ]  1298      *
[ ]  1299      * First do updates that do not depend on the details of the PNG image data
[ ]  1300      * being processed.
[ ]  1301      */
[ ]  1302  
[B]  1303  #ifdef PNG_READ_GAMMA_SUPPORTED
[ ]  1304     /* Prior to 1.5.4 these tests were performed from png_set_gamma, 1.5.4 adds
[ ]  1305      * png_set_alpha_mode and this is another source for a default file gamma so
[ ]  1306      * the test needs to be performed later - here.  In addition prior to 1.5.4
[ ]  1307      * the tests were repeated for the PALETTE color type here - this is no
[ ]  1308      * longer necessary (and doesn't seem to have been necessary before.)
[ ]  1309      */
[B]  1310     {
[ ]  1311        /* The following temporary indicates if overall gamma correction is
[ ]  1312         * required.
[ ]  1313         */
[B]  1314        int gamma_correction = 0;
[ ]  1315  
[B]  1316        if (png_ptr->colorspace.gamma != 0) /* has been set */
[B]  1317        {
[B]  1318           if (png_ptr->screen_gamma != 0) /* screen set too */
[ ]  1319              gamma_correction = png_gamma_threshold(png_ptr->colorspace.gamma,
[ ]  1320                  png_ptr->screen_gamma);
[ ]  1321  
[B]  1322           else
[ ]  1323              /* Assume the output matches the input; a long time default behavior
[ ]  1324               * of libpng, although the standard has nothing to say about this.
[ ]  1325               */
[B]  1326              png_ptr->screen_gamma = png_reciprocal(png_ptr->colorspace.gamma);
[B]  1327        }
[ ]  1328  
[ ]  1329        else if (png_ptr->screen_gamma != 0)
[ ]  1330           /* The converse - assume the file matches the screen, note that this
[ ]  1331            * perhaps undesirable default can (from 1.5.4) be changed by calling
[ ]  1332            * png_set_alpha_mode (even if the alpha handling mode isn't required
[ ]  1333            * or isn't changed from the default.)
[ ]  1334            */
[ ]  1335           png_ptr->colorspace.gamma = png_reciprocal(png_ptr->screen_gamma);
[ ]  1336  
[ ]  1337        else /* neither are set */
[ ]  1338           /* Just in case the following prevents any processing - file and screen
[ ]  1339            * are both assumed to be linear and there is no way to introduce a
[ ]  1340            * third gamma value other than png_set_background with 'UNIQUE', and,
[ ]  1341            * prior to 1.5.4
[ ]  1342            */
[ ]  1343           png_ptr->screen_gamma = png_ptr->colorspace.gamma = PNG_FP_1;
[ ]  1344  
[ ]  1345        /* We have a gamma value now. */
[B]  1346        png_ptr->colorspace.flags |= PNG_COLORSPACE_HAVE_GAMMA;
[ ]  1347  
[ ]  1348        /* Now turn the gamma transformation on or off as appropriate.  Notice
[ ]  1349         * that PNG_GAMMA just refers to the file->screen correction.  Alpha
[ ]  1350         * composition may independently cause gamma correction because it needs
[ ]  1351         * linear data (e.g. if the file has a gAMA chunk but the screen gamma
[ ]  1352         * hasn't been specified.)  In any case this flag may get turned off in
[ ]  1353         * the code immediately below if the transform can be handled outside the
[ ]  1354         * row loop.
[ ]  1355         */
[B]  1356        if (gamma_correction != 0)
[ ]  1357           png_ptr->transformations |= PNG_GAMMA;
[ ]  1358  
[B]  1359        else
[B]  1360           png_ptr->transformations &= ~PNG_GAMMA;
[B]  1361     }
[B]  1362  #endif
[ ]  1363  
[ ]  1364     /* Certain transformations have the effect of preventing other
[ ]  1365      * transformations that happen afterward in png_do_read_transformations;
[ ]  1366      * resolve the interdependencies here.  From the code of
[ ]  1367      * png_do_read_transformations the order is:
[ ]  1368      *
[ ]  1369      *  1) PNG_EXPAND (including PNG_EXPAND_tRNS)
[ ]  1370      *  2) PNG_STRIP_ALPHA (if no compose)
[ ]  1371      *  3) PNG_RGB_TO_GRAY
[ ]  1372      *  4) PNG_GRAY_TO_RGB iff !PNG_BACKGROUND_IS_GRAY
[ ]  1373      *  5) PNG_COMPOSE
[ ]  1374      *  6) PNG_GAMMA
[ ]  1375      *  7) PNG_STRIP_ALPHA (if compose)
[ ]  1376      *  8) PNG_ENCODE_ALPHA
[ ]  1377      *  9) PNG_SCALE_16_TO_8
[ ]  1378      * 10) PNG_16_TO_8
[ ]  1379      * 11) PNG_QUANTIZE (converts to palette)
[ ]  1380      * 12) PNG_EXPAND_16
[ ]  1381      * 13) PNG_GRAY_TO_RGB iff PNG_BACKGROUND_IS_GRAY
[ ]  1382      * 14) PNG_INVERT_MONO
[ ]  1383      * 15) PNG_INVERT_ALPHA
[ ]  1384      * 16) PNG_SHIFT
[ ]  1385      * 17) PNG_PACK
[ ]  1386      * 18) PNG_BGR
[ ]  1387      * 19) PNG_PACKSWAP
[ ]  1388      * 20) PNG_FILLER (includes PNG_ADD_ALPHA)
[ ]  1389      * 21) PNG_SWAP_ALPHA
[ ]  1390      * 22) PNG_SWAP_BYTES
[ ]  1391      * 23) PNG_USER_TRANSFORM [must be last]
[ ]  1392      */
[B]  1393  #ifdef PNG_READ_STRIP_ALPHA_SUPPORTED
[B]  1394     if ((png_ptr->transformations & PNG_STRIP_ALPHA) != 0 &&
[B]  1395         (png_ptr->transformations & PNG_COMPOSE) == 0)
[ ]  1396     {
[ ]  1397        /* Stripping the alpha channel happens immediately after the 'expand'
[ ]  1398         * transformations, before all other transformation, so it cancels out
[ ]  1399         * the alpha handling.  It has the side effect negating the effect of
[ ]  1400         * PNG_EXPAND_tRNS too:
[ ]  1401         */
[ ]  1402        png_ptr->transformations &= ~(PNG_BACKGROUND_EXPAND | PNG_ENCODE_ALPHA |
[ ]  1403           PNG_EXPAND_tRNS);
[ ]  1404        png_ptr->flags &= ~PNG_FLAG_OPTIMIZE_ALPHA;
[ ]  1405  
[ ]  1406        /* Kill the tRNS chunk itself too.  Prior to 1.5.4 this did not happen
[ ]  1407         * so transparency information would remain just so long as it wasn't
[ ]  1408         * expanded.  This produces unexpected API changes if the set of things
[ ]  1409         * that do PNG_EXPAND_tRNS changes (perfectly possible given the
[ ]  1410         * documentation - which says ask for what you want, accept what you
[ ]  1411         * get.)  This makes the behavior consistent from 1.5.4:
[ ]  1412         */
[ ]  1413        png_ptr->num_trans = 0;
[ ]  1414     }
[B]  1415  #endif /* STRIP_ALPHA supported, no COMPOSE */
[ ]  1416  
[B]  1417  #ifdef PNG_READ_ALPHA_MODE_SUPPORTED
[ ]  1418     /* If the screen gamma is about 1.0 then the OPTIMIZE_ALPHA and ENCODE_ALPHA
[ ]  1419      * settings will have no effect.
[ ]  1420      */
[B]  1421     if (png_gamma_significant(png_ptr->screen_gamma) == 0)
[ ]  1422     {
[ ]  1423        png_ptr->transformations &= ~PNG_ENCODE_ALPHA;
[ ]  1424        png_ptr->flags &= ~PNG_FLAG_OPTIMIZE_ALPHA;
[ ]  1425     }
[B]  1426  #endif
[ ]  1427  
[B]  1428  #ifdef PNG_READ_RGB_TO_GRAY_SUPPORTED
[ ]  1429     /* Make sure the coefficients for the rgb to gray conversion are set
[ ]  1430      * appropriately.
[ ]  1431      */
[B]  1432     if ((png_ptr->transformations & PNG_RGB_TO_GRAY) != 0)
[ ]  1433        png_colorspace_set_rgb_coefficients(png_ptr);
[B]  1434  #endif
[ ]  1435  
[B]  1436  #ifdef PNG_READ_GRAY_TO_RGB_SUPPORTED
[B]  1437  #if defined(PNG_READ_EXPAND_SUPPORTED) && defined(PNG_READ_BACKGROUND_SUPPORTED)
[ ]  1438     /* Detect gray background and attempt to enable optimization for
[ ]  1439      * gray --> RGB case.
[ ]  1440      *
[ ]  1441      * Note:  if PNG_BACKGROUND_EXPAND is set and color_type is either RGB or
[ ]  1442      * RGB_ALPHA (in which case need_expand is superfluous anyway), the
[ ]  1443      * background color might actually be gray yet not be flagged as such.
[ ]  1444      * This is not a problem for the current code, which uses
[ ]  1445      * PNG_BACKGROUND_IS_GRAY only to decide when to do the
[ ]  1446      * png_do_gray_to_rgb() transformation.
[ ]  1447      *
[ ]  1448      * TODO: this code needs to be revised to avoid the complexity and
[ ]  1449      * interdependencies.  The color type of the background should be recorded in
[ ]  1450      * png_set_background, along with the bit depth, then the code has a record
[ ]  1451      * of exactly what color space the background is currently in.
[ ]  1452      */
[B]  1453     if ((png_ptr->transformations & PNG_BACKGROUND_EXPAND) != 0)
[ ]  1454     {
[ ]  1455        /* PNG_BACKGROUND_EXPAND: the background is in the file color space, so if
[ ]  1456         * the file was grayscale the background value is gray.
[ ]  1457         */
[ ]  1458        if ((png_ptr->color_type & PNG_COLOR_MASK_COLOR) == 0)
[ ]  1459           png_ptr->mode |= PNG_BACKGROUND_IS_GRAY;
[ ]  1460     }
[ ]  1461  
[B]  1462     else if ((png_ptr->transformations & PNG_COMPOSE) != 0)
[ ]  1463     {
[ ]  1464        /* PNG_COMPOSE: png_set_background was called with need_expand false,
[ ]  1465         * so the color is in the color space of the output or png_set_alpha_mode
[ ]  1466         * was called and the color is black.  Ignore RGB_TO_GRAY because that
[ ]  1467         * happens before GRAY_TO_RGB.
[ ]  1468         */
[ ]  1469        if ((png_ptr->transformations & PNG_GRAY_TO_RGB) != 0)
[ ]  1470        {
[ ]  1471           if (png_ptr->background.red == png_ptr->background.green &&
[ ]  1472               png_ptr->background.red == png_ptr->background.blue)
[ ]  1473           {
[ ]  1474              png_ptr->mode |= PNG_BACKGROUND_IS_GRAY;
[ ]  1475              png_ptr->background.gray = png_ptr->background.red;
[ ]  1476           }
[ ]  1477        }
[ ]  1478     }
[B]  1479  #endif /* READ_EXPAND && READ_BACKGROUND */
[B]  1480  #endif /* READ_GRAY_TO_RGB */
[ ]  1481  
[ ]  1482     /* For indexed PNG data (PNG_COLOR_TYPE_PALETTE) many of the transformations
[ ]  1483      * can be performed directly on the palette, and some (such as rgb to gray)
[ ]  1484      * can be optimized inside the palette.  This is particularly true of the
[ ]  1485      * composite (background and alpha) stuff, which can be pretty much all done
[ ]  1486      * in the palette even if the result is expanded to RGB or gray afterward.
[ ]  1487      *
[ ]  1488      * NOTE: this is Not Yet Implemented, the code behaves as in 1.5.1 and
[ ]  1489      * earlier and the palette stuff is actually handled on the first row.  This
[ ]  1490      * leads to the reported bug that the palette returned by png_get_PLTE is not
[ ]  1491      * updated.
[ ]  1492      */
[B]  1493     if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE) <-- BLOCKER
[W]  1494        png_init_palette_transformations(png_ptr);
[ ]  1495  
[L]  1496     else
[L]  1497        png_init_rgb_transformations(png_ptr);
[ ]  1498  
[B]  1499  #if defined(PNG_READ_BACKGROUND_SUPPORTED) && \
[B]  1500     defined(PNG_READ_EXPAND_16_SUPPORTED)
[B]  1501     if ((png_ptr->transformations & PNG_EXPAND_16) != 0 &&
[B]  1502         (png_ptr->transformations & PNG_COMPOSE) != 0 &&
[B]  1503         (png_ptr->transformations & PNG_BACKGROUND_EXPAND) == 0 &&
[B]  1504         png_ptr->bit_depth != 16)
[ ]  1505     {
[ ]  1506        /* TODO: fix this.  Because the expand_16 operation is after the compose
[ ]  1507         * handling the background color must be 8, not 16, bits deep, but the
[ ]  1508         * application will supply a 16-bit value so reduce it here.
[ ]  1509         *
[ ]  1510         * The PNG_BACKGROUND_EXPAND code above does not expand to 16 bits at
[ ]  1511         * present, so that case is ok (until do_expand_16 is moved.)
[ ]  1512         *
[ ]  1513         * NOTE: this discards the low 16 bits of the user supplied background
[ ]  1514         * color, but until expand_16 works properly there is no choice!
[ ]  1515         */
[ ]  1516  #     define CHOP(x) (x)=((png_uint_16)PNG_DIV257(x))
[ ]  1517        CHOP(png_ptr->background.red);
[ ]  1518        CHOP(png_ptr->background.green);
[ ]  1519        CHOP(png_ptr->background.blue);
[ ]  1520        CHOP(png_ptr->background.gray);
[ ]  1521  #     undef CHOP
[ ]  1522     }
[B]  1523  #endif /* READ_BACKGROUND && READ_EXPAND_16 */
[ ]  1524  
[B]  1525  #if defined(PNG_READ_BACKGROUND_SUPPORTED) && \
[B]  1526     (defined(PNG_READ_SCALE_16_TO_8_SUPPORTED) || \
[B]  1527     defined(PNG_READ_STRIP_16_TO_8_SUPPORTED))
[B]  1528     if ((png_ptr->transformations & (PNG_16_TO_8|PNG_SCALE_16_TO_8)) != 0 &&
[B]  1529         (png_ptr->transformations & PNG_COMPOSE) != 0 &&
[B]  1530         (png_ptr->transformations & PNG_BACKGROUND_EXPAND) == 0 &&
[B]  1531         png_ptr->bit_depth == 16)
[ ]  1532     {
[ ]  1533        /* On the other hand, if a 16-bit file is to be reduced to 8-bits per
[ ]  1534         * component this will also happen after PNG_COMPOSE and so the background
[ ]  1535         * color must be pre-expanded here.
[ ]  1536         *
[ ]  1537         * TODO: fix this too.
[ ]  1538         */
[ ]  1539        png_ptr->background.red = (png_uint_16)(png_ptr->background.red * 257);
[ ]  1540        png_ptr->background.green =
[ ]  1541           (png_uint_16)(png_ptr->background.green * 257);
[ ]  1542        png_ptr->background.blue = (png_uint_16)(png_ptr->background.blue * 257);
[ ]  1543        png_ptr->background.gray = (png_uint_16)(png_ptr->background.gray * 257);
[ ]  1544     }
[B]  1545  #endif
[ ]  1546  
[ ]  1547     /* NOTE: below 'PNG_READ_ALPHA_MODE_SUPPORTED' is presumed to also enable the
[ ]  1548      * background support (see the comments in scripts/pnglibconf.dfa), this
[ ]  1549      * allows pre-multiplication of the alpha channel to be implemented as
[ ]  1550      * compositing on black.  This is probably sub-optimal and has been done in
[ ]  1551      * 1.5.4 betas simply to enable external critique and testing (i.e. to
[ ]  1552      * implement the new API quickly, without lots of internal changes.)
[ ]  1553      */
[ ]  1554  
[B]  1555  #ifdef PNG_READ_GAMMA_SUPPORTED
[B]  1556  #  ifdef PNG_READ_BACKGROUND_SUPPORTED
[ ]  1557        /* Includes ALPHA_MODE */
[B]  1558        png_ptr->background_1 = png_ptr->background;
[B]  1559  #  endif
[ ]  1560  
[ ]  1561     /* This needs to change - in the palette image case a whole set of tables are
[ ]  1562      * built when it would be quicker to just calculate the correct value for
[ ]  1563      * each palette entry directly.  Also, the test is too tricky - why check
[ ]  1564      * PNG_RGB_TO_GRAY if PNG_GAMMA is not set?  The answer seems to be that
[ ]  1565      * PNG_GAMMA is cancelled even if the gamma is known?  The test excludes the
[ ]  1566      * PNG_COMPOSE case, so apparently if there is no *overall* gamma correction
[ ]  1567      * the gamma tables will not be built even if composition is required on a
[ ]  1568      * gamma encoded value.
[ ]  1569      *
[ ]  1570      * In 1.5.4 this is addressed below by an additional check on the individual
[ ]  1571      * file gamma - if it is not 1.0 both RGB_TO_GRAY and COMPOSE need the
[ ]  1572      * tables.
[ ]  1573      */
[B]  1574     if ((png_ptr->transformations & PNG_GAMMA) != 0 ||
[B]  1575         ((png_ptr->transformations & PNG_RGB_TO_GRAY) != 0 &&
[B]  1576          (png_gamma_significant(png_ptr->colorspace.gamma) != 0 ||
[ ]  1577           png_gamma_significant(png_ptr->screen_gamma) != 0)) ||
[B]  1578          ((png_ptr->transformations & PNG_COMPOSE) != 0 &&
[B]  1579           (png_gamma_significant(png_ptr->colorspace.gamma) != 0 ||
[ ]  1580            png_gamma_significant(png_ptr->screen_gamma) != 0
[ ]  1581  #  ifdef PNG_READ_BACKGROUND_SUPPORTED
[ ]  1582           || (png_ptr->background_gamma_type == PNG_BACKGROUND_GAMMA_UNIQUE &&
[ ]  1583             png_gamma_significant(png_ptr->background_gamma) != 0)
[ ]  1584  #  endif
[B]  1585          )) || ((png_ptr->transformations & PNG_ENCODE_ALPHA) != 0 &&
[B]  1586         png_gamma_significant(png_ptr->screen_gamma) != 0))
[ ]  1587     {
[ ]  1588        png_build_gamma_table(png_ptr, png_ptr->bit_depth);
[ ]  1589  
[ ]  1590  #ifdef PNG_READ_BACKGROUND_SUPPORTED
[ ]  1591        if ((png_ptr->transformations & PNG_COMPOSE) != 0)
[ ]  1592        {
[ ]  1593           /* Issue a warning about this combination: because RGB_TO_GRAY is
[ ]  1594            * optimized to do the gamma transform if present yet do_background has
[ ]  1595            * to do the same thing if both options are set a
[ ]  1596            * double-gamma-correction happens.  This is true in all versions of
[ ]  1597            * libpng to date.
[ ]  1598            */
[ ]  1599           if ((png_ptr->transformations & PNG_RGB_TO_GRAY) != 0)
[ ]  1600              png_warning(png_ptr,
[ ]  1601                  "libpng does not support gamma+background+rgb_to_gray");
[ ]  1602  
[ ]  1603           if ((png_ptr->color_type == PNG_COLOR_TYPE_PALETTE) != 0)
[ ]  1604           {
[ ]  1605              /* We don't get to here unless there is a tRNS chunk with non-opaque
[ ]  1606               * entries - see the checking code at the start of this function.
[ ]  1607               */
[ ]  1608              png_color back, back_1;
[ ]  1609              png_colorp palette = png_ptr->palette;
[ ]  1610              int num_palette = png_ptr->num_palette;
[ ]  1611              int i;
[ ]  1612              if (png_ptr->background_gamma_type == PNG_BACKGROUND_GAMMA_FILE)
[ ]  1613              {
[ ]  1614  
[ ]  1615                 back.red = png_ptr->gamma_table[png_ptr->background.red];
[ ]  1616                 back.green = png_ptr->gamma_table[png_ptr->background.green];
[ ]  1617                 back.blue = png_ptr->gamma_table[png_ptr->background.blue];
[ ]  1618  
[ ]  1619                 back_1.red = png_ptr->gamma_to_1[png_ptr->background.red];
[ ]  1620                 back_1.green = png_ptr->gamma_to_1[png_ptr->background.green];
[ ]  1621                 back_1.blue = png_ptr->gamma_to_1[png_ptr->background.blue];
[ ]  1622              }
[ ]  1623              else
[ ]  1624              {
[ ]  1625                 png_fixed_point g, gs;
[ ]  1626  
[ ]  1627                 switch (png_ptr->background_gamma_type)
[ ]  1628                 {
[ ]  1629                    case PNG_BACKGROUND_GAMMA_SCREEN:
[ ]  1630                       g = (png_ptr->screen_gamma);
[ ]  1631                       gs = PNG_FP_1;
[ ]  1632                       break;
[ ]  1633  
[ ]  1634                    case PNG_BACKGROUND_GAMMA_FILE:
[ ]  1635                       g = png_reciprocal(png_ptr->colorspace.gamma);
[ ]  1636                       gs = png_reciprocal2(png_ptr->colorspace.gamma,
[ ]  1637                           png_ptr->screen_gamma);
[ ]  1638                       break;
[ ]  1639  
[ ]  1640                    case PNG_BACKGROUND_GAMMA_UNIQUE:
[ ]  1641                       g = png_reciprocal(png_ptr->background_gamma);
[ ]  1642                       gs = png_reciprocal2(png_ptr->background_gamma,
[ ]  1643                           png_ptr->screen_gamma);
[ ]  1644                       break;
[ ]  1645                    default:
[ ]  1646                       g = PNG_FP_1;    /* back_1 */
[ ]  1647                       gs = PNG_FP_1;   /* back */
[ ]  1648                       break;
[ ]  1649                 }
[ ]  1650  
[ ]  1651                 if (png_gamma_significant(gs) != 0)
[ ]  1652                 {
[ ]  1653                    back.red = png_gamma_8bit_correct(png_ptr->background.red,
[ ]  1654                        gs);
[ ]  1655                    back.green = png_gamma_8bit_correct(png_ptr->background.green,
[ ]  1656                        gs);
[ ]  1657                    back.blue = png_gamma_8bit_correct(png_ptr->background.blue,
[ ]  1658                        gs);
[ ]  1659                 }
[ ]  1660  
[ ]  1661                 else
[ ]  1662                 {
[ ]  1663                    back.red   = (png_byte)png_ptr->background.red;
[ ]  1664                    back.green = (png_byte)png_ptr->background.green;
[ ]  1665                    back.blue  = (png_byte)png_ptr->background.blue;
[ ]  1666                 }
[ ]  1667  
[ ]  1668                 if (png_gamma_significant(g) != 0)
[ ]  1669                 {
[ ]  1670                    back_1.red = png_gamma_8bit_correct(png_ptr->background.red,
[ ]  1671                        g);
[ ]  1672                    back_1.green = png_gamma_8bit_correct(
[ ]  1673                        png_ptr->background.green, g);
[ ]  1674                    back_1.blue = png_gamma_8bit_correct(png_ptr->background.blue,
[ ]  1675                        g);
[ ]  1676                 }
[ ]  1677  
[ ]  1678                 else
[ ]  1679                 {
[ ]  1680                    back_1.red   = (png_byte)png_ptr->background.red;
[ ]  1681                    back_1.green = (png_byte)png_ptr->background.green;
[ ]  1682                    back_1.blue  = (png_byte)png_ptr->background.blue;
[ ]  1683                 }
[ ]  1684              }
[ ]  1685  
[ ]  1686              for (i = 0; i < num_palette; i++)
[ ]  1687              {
[ ]  1688                 if (i < (int)png_ptr->num_trans &&
[ ]  1689                     png_ptr->trans_alpha[i] != 0xff)
[ ]  1690                 {
[ ]  1691                    if (png_ptr->trans_alpha[i] == 0)
[ ]  1692                    {
[ ]  1693                       palette[i] = back;
[ ]  1694                    }
[ ]  1695                    else /* if (png_ptr->trans_alpha[i] != 0xff) */
[ ]  1696                    {
[ ]  1697                       png_byte v, w;
[ ]  1698  
[ ]  1699                       v = png_ptr->gamma_to_1[palette[i].red];
[ ]  1700                       png_composite(w, v, png_ptr->trans_alpha[i], back_1.red);
[ ]  1701                       palette[i].red = png_ptr->gamma_from_1[w];
[ ]  1702  
[ ]  1703                       v = png_ptr->gamma_to_1[palette[i].green];
[ ]  1704                       png_composite(w, v, png_ptr->trans_alpha[i], back_1.green);
[ ]  1705                       palette[i].green = png_ptr->gamma_from_1[w];
[ ]  1706  
[ ]  1707                       v = png_ptr->gamma_to_1[palette[i].blue];
[ ]  1708                       png_composite(w, v, png_ptr->trans_alpha[i], back_1.blue);
[ ]  1709                       palette[i].blue = png_ptr->gamma_from_1[w];
[ ]  1710                    }
[ ]  1711                 }
[ ]  1712                 else
[ ]  1713                 {
[ ]  1714                    palette[i].red = png_ptr->gamma_table[palette[i].red];
[ ]  1715                    palette[i].green = png_ptr->gamma_table[palette[i].green];
[ ]  1716                    palette[i].blue = png_ptr->gamma_table[palette[i].blue];
[ ]  1717                 }
[ ]  1718              }
[ ]  1719  
[ ]  1720              /* Prevent the transformations being done again.
[ ]  1721               *
[ ]  1722               * NOTE: this is highly dubious; it removes the transformations in
[ ]  1723               * place.  This seems inconsistent with the general treatment of the
[ ]  1724               * transformations elsewhere.
[ ]  1725               */
[ ]  1726              png_ptr->transformations &= ~(PNG_COMPOSE | PNG_GAMMA);
[ ]  1727           } /* color_type == PNG_COLOR_TYPE_PALETTE */
[ ]  1728  
[ ]  1729           /* if (png_ptr->background_gamma_type!=PNG_BACKGROUND_GAMMA_UNKNOWN) */
[ ]  1730           else /* color_type != PNG_COLOR_TYPE_PALETTE */
[ ]  1731           {
[ ]  1732              int gs_sig, g_sig;
[ ]  1733              png_fixed_point g = PNG_FP_1;  /* Correction to linear */
[ ]  1734              png_fixed_point gs = PNG_FP_1; /* Correction to screen */
[ ]  1735  
[ ]  1736              switch (png_ptr->background_gamma_type)
[ ]  1737              {
[ ]  1738                 case PNG_BACKGROUND_GAMMA_SCREEN:
[ ]  1739                    g = png_ptr->screen_gamma;
[ ]  1740                    /* gs = PNG_FP_1; */
[ ]  1741                    break;
[ ]  1742  
[ ]  1743                 case PNG_BACKGROUND_GAMMA_FILE:
[ ]  1744                    g = png_reciprocal(png_ptr->colorspace.gamma);
[ ]  1745                    gs = png_reciprocal2(png_ptr->colorspace.gamma,
[ ]  1746                        png_ptr->screen_gamma);
[ ]  1747                    break;
[ ]  1748  
[ ]  1749                 case PNG_BACKGROUND_GAMMA_UNIQUE:
[ ]  1750                    g = png_reciprocal(png_ptr->background_gamma);
[ ]  1751                    gs = png_reciprocal2(png_ptr->background_gamma,
[ ]  1752                        png_ptr->screen_gamma);
[ ]  1753                    break;
[ ]  1754  
[ ]  1755                 default:
[ ]  1756                    png_error(png_ptr, "invalid background gamma type");
[ ]  1757              }
[ ]  1758  
[ ]  1759              g_sig = png_gamma_significant(g);
[ ]  1760              gs_sig = png_gamma_significant(gs);
[ ]  1761  
[ ]  1762              if (g_sig != 0)
[ ]  1763                 png_ptr->background_1.gray = png_gamma_correct(png_ptr,
[ ]  1764                     png_ptr->background.gray, g);
[ ]  1765  
[ ]  1766              if (gs_sig != 0)
[ ]  1767                 png_ptr->background.gray = png_gamma_correct(png_ptr,
[ ]  1768                     png_ptr->background.gray, gs);
[ ]  1769  
[ ]  1770              if ((png_ptr->background.red != png_ptr->background.green) ||
[ ]  1771                  (png_ptr->background.red != png_ptr->background.blue) ||
[ ]  1772                  (png_ptr->background.red != png_ptr->background.gray))
[ ]  1773              {
[ ]  1774                 /* RGB or RGBA with color background */
[ ]  1775                 if (g_sig != 0)
[ ]  1776                 {
[ ]  1777                    png_ptr->background_1.red = png_gamma_correct(png_ptr,
[ ]  1778                        png_ptr->background.red, g);
[ ]  1779  
[ ]  1780                    png_ptr->background_1.green = png_gamma_correct(png_ptr,
[ ]  1781                        png_ptr->background.green, g);
[ ]  1782  
[ ]  1783                    png_ptr->background_1.blue = png_gamma_correct(png_ptr,
[ ]  1784                        png_ptr->background.blue, g);
[ ]  1785                 }
[ ]  1786  
[ ]  1787                 if (gs_sig != 0)
[ ]  1788                 {
[ ]  1789                    png_ptr->background.red = png_gamma_correct(png_ptr,
[ ]  1790                        png_ptr->background.red, gs);
[ ]  1791  
[ ]  1792                    png_ptr->background.green = png_gamma_correct(png_ptr,
[ ]  1793                        png_ptr->background.green, gs);
[ ]  1794  
[ ]  1795                    png_ptr->background.blue = png_gamma_correct(png_ptr,
[ ]  1796                        png_ptr->background.blue, gs);
[ ]  1797                 }
[ ]  1798              }
[ ]  1799  
[ ]  1800              else
[ ]  1801              {
[ ]  1802                 /* GRAY, GRAY ALPHA, RGB, or RGBA with gray background */
[ ]  1803                 png_ptr->background_1.red = png_ptr->background_1.green
[ ]  1804                     = png_ptr->background_1.blue = png_ptr->background_1.gray;
[ ]  1805  
[ ]  1806                 png_ptr->background.red = png_ptr->background.green
[ ]  1807                     = png_ptr->background.blue = png_ptr->background.gray;
[ ]  1808              }
[ ]  1809  
[ ]  1810              /* The background is now in screen gamma: */
[ ]  1811              png_ptr->background_gamma_type = PNG_BACKGROUND_GAMMA_SCREEN;
[ ]  1812           } /* color_type != PNG_COLOR_TYPE_PALETTE */
[ ]  1813        }/* png_ptr->transformations & PNG_BACKGROUND */
[ ]  1814  
[ ]  1815        else
[ ]  1816        /* Transformation does not include PNG_BACKGROUND */
[ ]  1817  #endif /* READ_BACKGROUND */
[ ]  1818        if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE
[ ]  1819  #ifdef PNG_READ_RGB_TO_GRAY_SUPPORTED
[ ]  1820           /* RGB_TO_GRAY needs to have non-gamma-corrected values! */
[ ]  1821           && ((png_ptr->transformations & PNG_EXPAND) == 0 ||
[ ]  1822           (png_ptr->transformations & PNG_RGB_TO_GRAY) == 0)
[ ]  1823  #endif
[ ]  1824           )
[ ]  1825        {
[ ]  1826           png_colorp palette = png_ptr->palette;
[ ]  1827           int num_palette = png_ptr->num_palette;
[ ]  1828           int i;
[ ]  1829  
[ ]  1830           /* NOTE: there are other transformations that should probably be in
[ ]  1831            * here too.
[ ]  1832            */
[ ]  1833           for (i = 0; i < num_palette; i++)
[ ]  1834           {
[ ]  1835              palette[i].red = png_ptr->gamma_table[palette[i].red];
[ ]  1836              palette[i].green = png_ptr->gamma_table[palette[i].green];
[ ]  1837              palette[i].blue = png_ptr->gamma_table[palette[i].blue];
[ ]  1838           }
[ ]  1839  
[ ]  1840           /* Done the gamma correction. */
[ ]  1841           png_ptr->transformations &= ~PNG_GAMMA;
[ ]  1842        } /* color_type == PALETTE && !PNG_BACKGROUND transformation */
[ ]  1843     }
[B]  1844  #ifdef PNG_READ_BACKGROUND_SUPPORTED
[B]  1845     else
[B]  1846  #endif
[B]  1847  #endif /* READ_GAMMA */
[ ]  1848  
[B]  1849  #ifdef PNG_READ_BACKGROUND_SUPPORTED
[ ]  1850     /* No GAMMA transformation (see the hanging else 4 lines above) */
[B]  1851     if ((png_ptr->transformations & PNG_COMPOSE) != 0 &&
[B]  1852         (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE))
[ ]  1853     {
[ ]  1854        int i;
[ ]  1855        int istop = (int)png_ptr->num_trans;
[ ]  1856        png_color back;
[ ]  1857        png_colorp palette = png_ptr->palette;
[ ]  1858  
[ ]  1859        back.red   = (png_byte)png_ptr->background.red;
[ ]  1860        back.green = (png_byte)png_ptr->background.green;
[ ]  1861        back.blue  = (png_byte)png_ptr->background.blue;
[ ]  1862  
[ ]  1863        for (i = 0; i < istop; i++)
[ ]  1864        {
[ ]  1865           if (png_ptr->trans_alpha[i] == 0)
[ ]  1866           {
[ ]  1867              palette[i] = back;
[ ]  1868           }
[ ]  1869  
[ ]  1870           else if (png_ptr->trans_alpha[i] != 0xff)
[ ]  1871           {
[ ]  1872              /* The png_composite() macro is defined in png.h */
[ ]  1873              png_composite(palette[i].red, palette[i].red,
[ ]  1874                  png_ptr->trans_alpha[i], back.red);
[ ]  1875  
[ ]  1876              png_composite(palette[i].green, palette[i].green,
[ ]  1877                  png_ptr->trans_alpha[i], back.green);
[ ]  1878  
[ ]  1879              png_composite(palette[i].blue, palette[i].blue,
[ ]  1880                  png_ptr->trans_alpha[i], back.blue);
[ ]  1881           }
[ ]  1882        }
[ ]  1883  
[ ]  1884        png_ptr->transformations &= ~PNG_COMPOSE;
[ ]  1885     }
[B]  1886  #endif /* READ_BACKGROUND */
[ ]  1887  
[B]  1888  #ifdef PNG_READ_SHIFT_SUPPORTED
[B]  1889     if ((png_ptr->transformations & PNG_SHIFT) != 0 &&
[B]  1890         (png_ptr->transformations & PNG_EXPAND) == 0 &&
[B]  1891         (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE))
[ ]  1892     {
[ ]  1893        int i;
[ ]  1894        int istop = png_ptr->num_palette;
[ ]  1895        int shift = 8 - png_ptr->sig_bit.red;
[ ]  1896  
[ ]  1897        png_ptr->transformations &= ~PNG_SHIFT;
[ ]  1898  
[ ]  1899        /* significant bits can be in the range 1 to 7 for a meaningful result, if
[ ]  1900         * the number of significant bits is 0 then no shift is done (this is an
[ ]  1901         * error condition which is silently ignored.)
[ ]  1902         */
[ ]  1903        if (shift > 0 && shift < 8)
[ ]  1904           for (i=0; i<istop; ++i)
[ ]  1905           {
[ ]  1906              int component = png_ptr->palette[i].red;
[ ]  1907  
[ ]  1908              component >>= shift;
[ ]  1909              png_ptr->palette[i].red = (png_byte)component;
[ ]  1910           }
[ ]  1911  
[ ]  1912        shift = 8 - png_ptr->sig_bit.green;
[ ]  1913        if (shift > 0 && shift < 8)
[ ]  1914           for (i=0; i<istop; ++i)
[ ]  1915           {
[ ]  1916              int component = png_ptr->palette[i].green;
[ ]  1917  
[ ]  1918              component >>= shift;
[ ]  1919              png_ptr->palette[i].green = (png_byte)component;
[ ]  1920           }
[ ]  1921  
[ ]  1922        shift = 8 - png_ptr->sig_bit.blue;
[ ]  1923        if (shift > 0 && shift < 8)
[ ]  1924           for (i=0; i<istop; ++i)
[ ]  1925           {
[ ]  1926              int component = png_ptr->palette[i].blue;
[ ]  1927  
[ ]  1928              component >>= shift;
[ ]  1929              png_ptr->palette[i].blue = (png_byte)component;
[ ]  1930           }
[ ]  1931     }
[B]  1932  #endif /* READ_SHIFT */
[B]  1933  }

--- No 1-hop callers of OSS_FUZZ_png_init_read_transformations fired in W (callers index present but none matched) ---

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
       0       702  pngrtran.c:png_do_expand  (/src/libpng/pngrtran.c:4385-4605)
     248         0  pngrtran.c:png_do_expand_palette  (/src/libpng/pngrtran.c:4212-4377)
      10         0  pngrtran.c:png_init_palette_transformations  (/src/libpng/pngrtran.c:1118-1203)
       0        10  pngrtran.c:png_init_rgb_transformations  (/src/libpng/pngrtran.c:1207-1288)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=1  OSS_FUZZ_png_init_read_transformations  (/src/libpng/pngrtran.c:1292-1933) ---
  d=1   L1493  T=10 F=0  T=0 F=10  if (png_ptr->color_type == PNG_COLOR_TYPE_PALETTE)  <-- BLOCKER

[off-chain: 88 additional divergent branches across 8 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=282c4c4b85d3af6c, size=8764 bytes, fuzzer=cmplog, trial=1, discovered_at=7s, mutation_op=BitFlipMutator,ByteIncMutator,DwordAddMutator,BytesSetMutator,BytesDeleteMutator,WordInterestingMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=414b4a1157e93507, size=8568 bytes, fuzzer=cmplog, trial=1, discovered_at=27126s, mutation_op=BytesRandInsertMutator,BytesDeleteMutator,ByteDecMutator,WordInterestingMutator,BytesCopyMutator,ByteIncMutator,BytesRandSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 0f 42 40 08 03 00 00 00 52 ed aa   ......B@.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=04430d1404dcf240, size=8765 bytes, fuzzer=cmplog, trial=1, discovered_at=29940s, mutation_op=ByteInterestingMutator,WordInterestingMutator,ByteFlipMutator,WordInterestingMutator,CrossoverInsertMutator,TokenInsert,DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 02 03 00 00 00 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=49a1380366efbf3e, size=8568 bytes, fuzzer=cmplog, trial=1, discovered_at=35373s, mutation_op=WordInterestingMutator,ByteAddMutator,BytesDeleteMutator,BytesSetMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 08 00 0f 42 40 08 03 00 00 00 52 ed aa   ......B@.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=1b177c559d885638, size=1016 bytes, fuzzer=cmplog, trial=1, discovered_at=48986s, mutation_op=ByteNegMutator,ByteNegMutator,QwordAddMutator,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 03 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 69 54 58 74 00 00 b1 8f 0b fc 61   .....iTXt......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=0165867d1e996ed7, size=1672 bytes, fuzzer=naive, trial=1, discovered_at=205s, mutation_op=ByteIncMutator,ByteAddMutator,BitFlipMutator,BytesRandSetMutator,ByteRandMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 21 00 00 80 00 04 00 00 00 01 00 ff aa   ...!............
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=021042b836a3f5aa, size=927 bytes, fuzzer=naive, trial=1, discovered_at=257s, mutation_op=ByteDecMutator,BytesSetMutator,ByteNegMutator,ByteFlipMutator,WordInterestingMutator,BytesInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 00 00 02 04 00 00 00 01 00 00 aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=00c12f3d55212fd8, size=932 bytes, fuzzer=naive, trial=1, discovered_at=408s, mutation_op=QwordAddMutator,ByteInterestingMutator,BytesSetMutator,ByteIncMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 55 00 00 a0 86 10 00 00 00 01 7f ed aa   ...U............
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=00a0761917250025, size=768 bytes, fuzzer=naive, trial=1, discovered_at=1159s, mutation_op=DwordAddMutator,TokenReplace,BytesInsertCopyMutator,BytesRandInsertMutator,BytesRandInsertMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 05 0a 00 00 80 00 02 00 00 00 01 00 ff aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=004b9750af3eaa48, size=5109 bytes, fuzzer=naive, trial=1, discovered_at=1232s, mutation_op=ByteNegMutator,BytesDeleteMutator,CrossoverReplaceMutator,WordInterestingMutator,ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 05 00 00 00 03 04 00 00 00 01 00 00 aa   ................
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b 04 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x10                            00(.)x9 05(.)x1                     PARTIAL
   0x0013  5b([)x6 05(.)x3 08(.)x1             05(.)x2 21(!)x1 55(U)x1 0a(.)x1 +5u  PARTIAL
   0x0015  00(.)x6 0f(.)x4                     00(.)x10                            PARTIAL
   0x0016  00(.)x6 42(B)x4                     00(.)x4 a0(.)x3 80(.)x2 02(.)x1     PARTIAL
   0x0017  45(E)x6 40(@)x4                     00(.)x3 86(.)x2 02(.)x1 03(.)x1 +3u  PARTIAL
   0x0018  08(.)x7 02(.)x3                     10(.)x4 04(.)x3 02(.)x1 08(.)x1 +1u  PARTIAL
   0x0019  03(.)x10                            00(.)x8 04(.)x2                     DIFFER
   0x001d  52(R)x10                            7f(.)x5 00(.)x4 ff(.)x1             DIFFER
   0x001e  ed(.)x10                            ed(.)x6 ff(.)x2 00(.)x2             PARTIAL
   0x0025  67(g)x8 69(i)x2                     67(g)x10                            PARTIAL
   0x0026  41(A)x8 54(T)x2                     41(A)x10                            PARTIAL
   0x0027  4d(M)x8 58(X)x2                     4d(M)x10                            PARTIAL
   0x0028  41(A)x8 74(t)x2                     41(A)x10                            PARTIAL
   0x002d  0b(.)x10                            0b(.)x8 aa(.)x1 1b(.)x1             PARTIAL
   0x002e  fc(.)x10                            fc(.)x5 04(.)x4 56(V)x1             PARTIAL
   0x002f  61(a)x10                            61(a)x9 aa(.)x1                     PARTIAL
   0x0030  05(.)x10                            05(.)x9 aa(.)x1                     PARTIAL
   0x0034  01(.)x10                            01(.)x9 09(.)x1                     PARTIAL
   0x0035  73(s)x10                            73(s)x9 74(t)x1                     PARTIAL
   0x0036  52(R)x10                            52(R)x9 45(E)x1                     PARTIAL
   0x0037  47(G)x10                            47(G)x9 58(X)x1                     PARTIAL
   0x0038  42(B)x10                            42(B)x9 74(t)x1                     PARTIAL
   0x0039  01(.)x10                            01(.)x9 54(T)x1                     PARTIAL
   0x003a  d9(.)x10                            d9(.)x9 69(i)x1                     PARTIAL
   0x003b  c9(.)x10                            c9(.)x9 74(t)x1                     PARTIAL
   0x003c  2c(,)x10                            2c(,)x9 6c(l)x1                     PARTIAL
   0x003d  7f(.)x10                            7f(.)x9 65(e)x1                     PARTIAL
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3912.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3912,
  "target": "libpng",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3912 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3912 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3912 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).