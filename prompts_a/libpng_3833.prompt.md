==== BLOCKER ====
Target: libpng
Branch ID: 3833
Location: /src/libpng/png.c:1288:26
Enclosing function: png.c:png_XYZ_from_xy
Source line:    if (xy->greenx < 0 || xy->greenx > PNG_FP_1) return 1;
Globally blocked side: T  (true branch)

==== TRIAL VECTOR (per fuzzer, n=10 trials) ====
fuzzer                    resolved  blocked  unreached  role
naive                            7        3          0  REFERENCE
cmplog                           2        8          0  loser (value_profile vs value_profile_cmplog)
value_profile                    8        2          0  REFERENCE
value_profile_cmplog             9        1          0  winner (value_profile vs cmplog)
naive_ctx                       10        0          0  REFERENCE
naive_ngram4                     9        1          0  REFERENCE
mopt                             8        2          0  REFERENCE
minimizer                        4        6          0  REFERENCE
fast                             9        1          0  REFERENCE
grimoire                         4        6          0  REFERENCE

INVOLVED fuzzers (synthetic-verification scope): ['cmplog', 'value_profile_cmplog']
REFERENCE fuzzers (auxiliary context only):     ['naive', 'value_profile', 'naive_ctx', 'naive_ngram4', 'mopt', 'minimizer', 'fast', 'grimoire']

==== DECISIVE PAIRS (1) ====
--- Pair 1: value_profile_cmplog > cmplog  [delta: value_profile] ---
  subject 23  (value_profile_cmplog vs cmplog, admissible)
  winner: resolved=9/10  blocked=1  unreached=0
  loser:  resolved=2/10  blocked=8  unreached=0
  avg duration blocked: winner=6.30h  loser=21.10h
  avg hitcount on branch: winner=56  loser=3
  prob_div=0.70  dur_div=14.80h  hit_div=53
  subject-level: delta_AUC=7265340.0  p_AUC=0.0003  delta_Final=83.1  p_final=0.0002

==== SOURCE CONTEXT (per-role coverage overlay) ====
Legend: [W] winner-resolving only  [L] loser-blocking only  [B] both  [ ] not hit
Source: db/per_role_coverage/libpng/3833/{W,L}/branch_coverage_show.txt

--- Enclosing function: png.c:png_XYZ_from_xy (/src/libpng/png.c:1277-1539) ---
[ ]  1275  static int
[ ]  1276  png_XYZ_from_xy(png_XYZ *XYZ, const png_xy *xy)
[B]  1277  {
[B]  1278     png_fixed_point red_inverse, green_inverse, blue_scale;
[B]  1279     png_fixed_point left, right, denominator;
[ ]  1280  
[ ]  1281     /* Check xy and, implicitly, z.  Note that wide gamut color spaces typically
[ ]  1282      * have end points with 0 tristimulus values (these are impossible end
[ ]  1283      * points, but they are used to cover the possible colors).  We check
[ ]  1284      * xy->whitey against 5, not 0, to avoid a possible integer overflow.
[ ]  1285      */
[B]  1286     if (xy->redx   < 0 || xy->redx > PNG_FP_1) return 1;
[B]  1287     if (xy->redy   < 0 || xy->redy > PNG_FP_1-xy->redx) return 1;
[B]  1288     if (xy->greenx < 0 || xy->greenx > PNG_FP_1) return 1; <-- BLOCKER
[L]  1289     if (xy->greeny < 0 || xy->greeny > PNG_FP_1-xy->greenx) return 1;
[L]  1290     if (xy->bluex  < 0 || xy->bluex > PNG_FP_1) return 1;
[L]  1291     if (xy->bluey  < 0 || xy->bluey > PNG_FP_1-xy->bluex) return 1;
[L]  1292     if (xy->whitex < 0 || xy->whitex > PNG_FP_1) return 1;
[L]  1293     if (xy->whitey < 5 || xy->whitey > PNG_FP_1-xy->whitex) return 1;
[ ]  1294  
[ ]  1295     /* The reverse calculation is more difficult because the original tristimulus
[ ]  1296      * value had 9 independent values (red,green,blue)x(X,Y,Z) however only 8
[ ]  1297      * derived values were recorded in the cHRM chunk;
[ ]  1298      * (red,green,blue,white)x(x,y).  This loses one degree of freedom and
[ ]  1299      * therefore an arbitrary ninth value has to be introduced to undo the
[ ]  1300      * original transformations.
[ ]  1301      *
[ ]  1302      * Think of the original end-points as points in (X,Y,Z) space.  The
[ ]  1303      * chromaticity values (c) have the property:
[ ]  1304      *
[ ]  1305      *           C
[ ]  1306      *   c = ---------
[ ]  1307      *       X + Y + Z
[ ]  1308      *
[ ]  1309      * For each c (x,y,z) from the corresponding original C (X,Y,Z).  Thus the
[ ]  1310      * three chromaticity values (x,y,z) for each end-point obey the
[ ]  1311      * relationship:
[ ]  1312      *
[ ]  1313      *   x + y + z = 1
[ ]  1314      *
[ ]  1315      * This describes the plane in (X,Y,Z) space that intersects each axis at the
[ ]  1316      * value 1.0; call this the chromaticity plane.  Thus the chromaticity
[ ]  1317      * calculation has scaled each end-point so that it is on the x+y+z=1 plane
[ ]  1318      * and chromaticity is the intersection of the vector from the origin to the
[ ]  1319      * (X,Y,Z) value with the chromaticity plane.
[ ]  1320      *
[ ]  1321      * To fully invert the chromaticity calculation we would need the three
[ ]  1322      * end-point scale factors, (red-scale, green-scale, blue-scale), but these
[ ]  1323      * were not recorded.  Instead we calculated the reference white (X,Y,Z) and
[ ]  1324      * recorded the chromaticity of this.  The reference white (X,Y,Z) would have
[ ]  1325      * given all three of the scale factors since:
[ ]  1326      *
[ ]  1327      *    color-C = color-c * color-scale
[ ]  1328      *    white-C = red-C + green-C + blue-C
[ ]  1329      *            = red-c*red-scale + green-c*green-scale + blue-c*blue-scale
[ ]  1330      *
[ ]  1331      * But cHRM records only white-x and white-y, so we have lost the white scale
[ ]  1332      * factor:
[ ]  1333      *
[ ]  1334      *    white-C = white-c*white-scale
[ ]  1335      *
[ ]  1336      * To handle this the inverse transformation makes an arbitrary assumption
[ ]  1337      * about white-scale:
[ ]  1338      *
[ ]  1339      *    Assume: white-Y = 1.0
[ ]  1340      *    Hence:  white-scale = 1/white-y
[ ]  1341      *    Or:     red-Y + green-Y + blue-Y = 1.0
[ ]  1342      *
[ ]  1343      * Notice the last statement of the assumption gives an equation in three of
[ ]  1344      * the nine values we want to calculate.  8 more equations come from the
[ ]  1345      * above routine as summarised at the top above (the chromaticity
[ ]  1346      * calculation):
[ ]  1347      *
[ ]  1348      *    Given: color-x = color-X / (color-X + color-Y + color-Z)
[ ]  1349      *    Hence: (color-x - 1)*color-X + color.x*color-Y + color.x*color-Z = 0
[ ]  1350      *
[ ]  1351      * This is 9 simultaneous equations in the 9 variables "color-C" and can be
[ ]  1352      * solved by Cramer's rule.  Cramer's rule requires calculating 10 9x9 matrix
[ ]  1353      * determinants, however this is not as bad as it seems because only 28 of
[ ]  1354      * the total of 90 terms in the various matrices are non-zero.  Nevertheless
[ ]  1355      * Cramer's rule is notoriously numerically unstable because the determinant
[ ]  1356      * calculation involves the difference of large, but similar, numbers.  It is
[ ]  1357      * difficult to be sure that the calculation is stable for real world values
[ ]  1358      * and it is certain that it becomes unstable where the end points are close
[ ]  1359      * together.
[ ]  1360      *
[ ]  1361      * So this code uses the perhaps slightly less optimal but more
[ ]  1362      * understandable and totally obvious approach of calculating color-scale.
[ ]  1363      *
[ ]  1364      * This algorithm depends on the precision in white-scale and that is
[ ]  1365      * (1/white-y), so we can immediately see that as white-y approaches 0 the
[ ]  1366      * accuracy inherent in the cHRM chunk drops off substantially.
[ ]  1367      *
[ ]  1368      * libpng arithmetic: a simple inversion of the above equations
[ ]  1369      * ------------------------------------------------------------
[ ]  1370      *
[ ]  1371      *    white_scale = 1/white-y
[ ]  1372      *    white-X = white-x * white-scale
[ ]  1373      *    white-Y = 1.0
[ ]  1374      *    white-Z = (1 - white-x - white-y) * white_scale
[ ]  1375      *
[ ]  1376      *    white-C = red-C + green-C + blue-C
[ ]  1377      *            = red-c*red-scale + green-c*green-scale + blue-c*blue-scale
[ ]  1378      *
[ ]  1379      * This gives us three equations in (red-scale,green-scale,blue-scale) where
[ ]  1380      * all the coefficients are now known:
[ ]  1381      *
[ ]  1382      *    red-x*red-scale + green-x*green-scale + blue-x*blue-scale
[ ]  1383      *       = white-x/white-y
[ ]  1384      *    red-y*red-scale + green-y*green-scale + blue-y*blue-scale = 1
[ ]  1385      *    red-z*red-scale + green-z*green-scale + blue-z*blue-scale
[ ]  1386      *       = (1 - white-x - white-y)/white-y
[ ]  1387      *
[ ]  1388      * In the last equation color-z is (1 - color-x - color-y) so we can add all
[ ]  1389      * three equations together to get an alternative third:
[ ]  1390      *
[ ]  1391      *    red-scale + green-scale + blue-scale = 1/white-y = white-scale
[ ]  1392      *
[ ]  1393      * So now we have a Cramer's rule solution where the determinants are just
[ ]  1394      * 3x3 - far more tractible.  Unfortunately 3x3 determinants still involve
[ ]  1395      * multiplication of three coefficients so we can't guarantee to avoid
[ ]  1396      * overflow in the libpng fixed point representation.  Using Cramer's rule in
[ ]  1397      * floating point is probably a good choice here, but it's not an option for
[ ]  1398      * fixed point.  Instead proceed to simplify the first two equations by
[ ]  1399      * eliminating what is likely to be the largest value, blue-scale:
[ ]  1400      *
[ ]  1401      *    blue-scale = white-scale - red-scale - green-scale
[ ]  1402      *
[ ]  1403      * Hence:
[ ]  1404      *
[ ]  1405      *    (red-x - blue-x)*red-scale + (green-x - blue-x)*green-scale =
[ ]  1406      *                (white-x - blue-x)*white-scale
[ ]  1407      *
[ ]  1408      *    (red-y - blue-y)*red-scale + (green-y - blue-y)*green-scale =
[ ]  1409      *                1 - blue-y*white-scale
[ ]  1410      *
[ ]  1411      * And now we can trivially solve for (red-scale,green-scale):
[ ]  1412      *
[ ]  1413      *    green-scale =
[ ]  1414      *                (white-x - blue-x)*white-scale - (red-x - blue-x)*red-scale
[ ]  1415      *                -----------------------------------------------------------
[ ]  1416      *                                  green-x - blue-x
[ ]  1417      *
[ ]  1418      *    red-scale =
[ ]  1419      *                1 - blue-y*white-scale - (green-y - blue-y) * green-scale
[ ]  1420      *                ---------------------------------------------------------
[ ]  1421      *                                  red-y - blue-y
[ ]  1422      *
[ ]  1423      * Hence:
[ ]  1424      *
[ ]  1425      *    red-scale =
[ ]  1426      *          ( (green-x - blue-x) * (white-y - blue-y) -
[ ]  1427      *            (green-y - blue-y) * (white-x - blue-x) ) / white-y
[ ]  1428      * -------------------------------------------------------------------------
[ ]  1429      *  (green-x - blue-x)*(red-y - blue-y)-(green-y - blue-y)*(red-x - blue-x)
[ ]  1430      *
[ ]  1431      *    green-scale =
[ ]  1432      *          ( (red-y - blue-y) * (white-x - blue-x) -
[ ]  1433      *            (red-x - blue-x) * (white-y - blue-y) ) / white-y
[ ]  1434      * -------------------------------------------------------------------------
[ ]  1435      *  (green-x - blue-x)*(red-y - blue-y)-(green-y - blue-y)*(red-x - blue-x)
[ ]  1436      *
[ ]  1437      * Accuracy:
[ ]  1438      * The input values have 5 decimal digits of accuracy.  The values are all in
[ ]  1439      * the range 0 < value < 1, so simple products are in the same range but may
[ ]  1440      * need up to 10 decimal digits to preserve the original precision and avoid
[ ]  1441      * underflow.  Because we are using a 32-bit signed representation we cannot
[ ]  1442      * match this; the best is a little over 9 decimal digits, less than 10.
[ ]  1443      *
[ ]  1444      * The approach used here is to preserve the maximum precision within the
[ ]  1445      * signed representation.  Because the red-scale calculation above uses the
[ ]  1446      * difference between two products of values that must be in the range -1..+1
[ ]  1447      * it is sufficient to divide the product by 7; ceil(100,000/32767*2).  The
[ ]  1448      * factor is irrelevant in the calculation because it is applied to both
[ ]  1449      * numerator and denominator.
[ ]  1450      *
[ ]  1451      * Note that the values of the differences of the products of the
[ ]  1452      * chromaticities in the above equations tend to be small, for example for
[ ]  1453      * the sRGB chromaticities they are:
[ ]  1454      *
[ ]  1455      * red numerator:    -0.04751
[ ]  1456      * green numerator:  -0.08788
[ ]  1457      * denominator:      -0.2241 (without white-y multiplication)
[ ]  1458      *
[ ]  1459      *  The resultant Y coefficients from the chromaticities of some widely used
[ ]  1460      *  color space definitions are (to 15 decimal places):
[ ]  1461      *
[ ]  1462      *  sRGB
[ ]  1463      *    0.212639005871510 0.715168678767756 0.072192315360734
[ ]  1464      *  Kodak ProPhoto
[ ]  1465      *    0.288071128229293 0.711843217810102 0.000085653960605
[ ]  1466      *  Adobe RGB
[ ]  1467      *    0.297344975250536 0.627363566255466 0.075291458493998
[ ]  1468      *  Adobe Wide Gamut RGB
[ ]  1469      *    0.258728243040113 0.724682314948566 0.016589442011321
[ ]  1470      */
[ ]  1471     /* By the argument, above overflow should be impossible here. The return
[ ]  1472      * value of 2 indicates an internal error to the caller.
[ ]  1473      */
[L]  1474     if (png_muldiv(&left, xy->greenx-xy->bluex, xy->redy - xy->bluey, 7) == 0)
[ ]  1475        return 2;
[L]  1476     if (png_muldiv(&right, xy->greeny-xy->bluey, xy->redx - xy->bluex, 7) == 0)
[ ]  1477        return 2;
[L]  1478     denominator = left - right;
[ ]  1479  
[ ]  1480     /* Now find the red numerator. */
[L]  1481     if (png_muldiv(&left, xy->greenx-xy->bluex, xy->whitey-xy->bluey, 7) == 0)
[ ]  1482        return 2;
[L]  1483     if (png_muldiv(&right, xy->greeny-xy->bluey, xy->whitex-xy->bluex, 7) == 0)
[ ]  1484        return 2;
[ ]  1485  
[ ]  1486     /* Overflow is possible here and it indicates an extreme set of PNG cHRM
[ ]  1487      * chunk values.  This calculation actually returns the reciprocal of the
[ ]  1488      * scale value because this allows us to delay the multiplication of white-y
[ ]  1489      * into the denominator, which tends to produce a small number.
[ ]  1490      */
[L]  1491     if (png_muldiv(&red_inverse, xy->whitey, denominator, left-right) == 0 ||
[L]  1492         red_inverse <= xy->whitey /* r+g+b scales = white scale */)
[L]  1493        return 1;
[ ]  1494  
[ ]  1495     /* Similarly for green_inverse: */
[L]  1496     if (png_muldiv(&left, xy->redy-xy->bluey, xy->whitex-xy->bluex, 7) == 0)
[ ]  1497        return 2;
[L]  1498     if (png_muldiv(&right, xy->redx-xy->bluex, xy->whitey-xy->bluey, 7) == 0)
[ ]  1499        return 2;
[L]  1500     if (png_muldiv(&green_inverse, xy->whitey, denominator, left-right) == 0 ||
[L]  1501         green_inverse <= xy->whitey)
[L]  1502        return 1;
[ ]  1503  
[ ]  1504     /* And the blue scale, the checks above guarantee this can't overflow but it
[ ]  1505      * can still produce 0 for extreme cHRM values.
[ ]  1506      */
[L]  1507     blue_scale = png_reciprocal(xy->whitey) - png_reciprocal(red_inverse) -
[L]  1508         png_reciprocal(green_inverse);
[L]  1509     if (blue_scale <= 0)
[ ]  1510        return 1;
[ ]  1511  
[ ]  1512  
[ ]  1513     /* And fill in the png_XYZ: */
[L]  1514     if (png_muldiv(&XYZ->red_X, xy->redx, PNG_FP_1, red_inverse) == 0)
[ ]  1515        return 1;
[L]  1516     if (png_muldiv(&XYZ->red_Y, xy->redy, PNG_FP_1, red_inverse) == 0)
[ ]  1517        return 1;
[L]  1518     if (png_muldiv(&XYZ->red_Z, PNG_FP_1 - xy->redx - xy->redy, PNG_FP_1,
[L]  1519         red_inverse) == 0)
[ ]  1520        return 1;
[ ]  1521  
[L]  1522     if (png_muldiv(&XYZ->green_X, xy->greenx, PNG_FP_1, green_inverse) == 0)
[ ]  1523        return 1;
[L]  1524     if (png_muldiv(&XYZ->green_Y, xy->greeny, PNG_FP_1, green_inverse) == 0)
[ ]  1525        return 1;
[L]  1526     if (png_muldiv(&XYZ->green_Z, PNG_FP_1 - xy->greenx - xy->greeny, PNG_FP_1,
[L]  1527         green_inverse) == 0)
[ ]  1528        return 1;
[ ]  1529  
[L]  1530     if (png_muldiv(&XYZ->blue_X, xy->bluex, blue_scale, PNG_FP_1) == 0)
[ ]  1531        return 1;
[L]  1532     if (png_muldiv(&XYZ->blue_Y, xy->bluey, blue_scale, PNG_FP_1) == 0)
[ ]  1533        return 1;
[L]  1534     if (png_muldiv(&XYZ->blue_Z, PNG_FP_1 - xy->bluex - xy->bluey, blue_scale,
[L]  1535         PNG_FP_1) == 0)
[ ]  1536        return 1;
[ ]  1537  
[L]  1538     return 0; /*success*/
[L]  1539  }

--- Caller (1 hop): png.c:png_colorspace_check_xy (/src/libpng/png.c:1619-1638, calls png.c:png_XYZ_from_xy at line 1624) (full body — short) ---
[B]  1619  {
[B]  1620     int result;
[B]  1621     png_xy xy_test;
[ ]  1622  
[ ]  1623     /* As a side-effect this routine also returns the XYZ endpoints. */
[B]  1624     result = png_XYZ_from_xy(XYZ, xy); <-- CALL
[B]  1625     if (result != 0)
[B]  1626        return result;
[ ]  1627  
[L]  1628     result = png_xy_from_XYZ(&xy_test, XYZ);
[L]  1629     if (result != 0)
[ ]  1630        return result;
[ ]  1631  
[L]  1632     if (png_colorspace_endpoints_match(xy, &xy_test,
[L]  1633         5/*actually, the math is pretty accurate*/) != 0)
[L]  1634        return 0;
[ ]  1635  
[ ]  1636     /* Too much slip */
[L]  1637     return 1;
[L]  1638  }

--- Call chain (depth 2..8, signatures only; depth 1 detailed above) ---
hop 2  png.c:png_colorspace_check_xy  (/src/libpng/png.c:1619-1638, calls png.c:png_XYZ_from_xy at line 1624)
hop 3  OSS_FUZZ_png_colorspace_set_chromaticities  (/src/libpng/png.c:1722-1754, calls png.c:png_colorspace_check_xy at line 1731)
hop 3  png.c:png_colorspace_check_XYZ  (/src/libpng/png.c:1645-1659, calls png.c:png_colorspace_check_xy at line 1658)
hop 4  OSS_FUZZ_png_colorspace_set_endpoints  (/src/libpng/png.c:1759-1781, calls png.c:png_colorspace_check_XYZ at line 1763)

==== HIT-COUNT DIVERGENCE (per function in cov dump) ====
Functions where W and L invocation counts differ by >=3.0x or one is zero. 'Entry-line count' = first executable line in the function body — a proxy for invocation count.

  W hits    L hits  function  (file:start-end)
      44      2150  OSS_FUZZ_png_get_io_ptr  (/src/libpng/png.c:687-692)
      30      1540  OSS_FUZZ_png_calculate_crc  (/src/libpng/png.c:140-187)
       0       851  OSS_FUZZ_png_muldiv  (/src/libpng/png.c:3351-3461)
      15       629  OSS_FUZZ_png_reset_crc  (/src/libpng/png.c:128-131)
      14       587  OSS_FUZZ_png_handle_as_unknown  (/src/libpng/png.c:927-956)
      14       587  OSS_FUZZ_png_chunk_unknown_handling  (/src/libpng/png.c:962-967)
       5       136  OSS_FUZZ_png_check_fp_number  (/src/libpng/png.c:2714-2834)
       1       120  OSS_FUZZ_png_reciprocal  (/src/libpng/png.c:3489-3503)
       2       114  OSS_FUZZ_png_colorspace_sync_info  (/src/libpng/png.c:1170-1211)
       2       114  OSS_FUZZ_png_colorspace_sync  (/src/libpng/png.c:1216-1222)
       4        97  OSS_FUZZ_png_free_data  (/src/libpng/png.c:473-678)
       0        84  png.c:png_colorspace_endpoints_match  (/src/libpng/png.c:1593-1605)
       3        85  OSS_FUZZ_png_check_fp_string  (/src/libpng/png.c:2840-2849)
       2        80  OSS_FUZZ_png_create_info_struct  (/src/libpng/png.c:355-375)
       2        80  OSS_FUZZ_png_destroy_info_struct  (/src/libpng/png.c:387-412)
... (20 more divergent functions)

==== DIVERGENT BRANCHES (on call chain, rough order) ====
Branches with W/L divergence in functions on the call chain (enclosing + 1-hop + chain). Rough execution order: outermost caller → blocker. Caveats: this assumes no recursion; loops/gotos break source-line order locally; off-chain divergent branches (L explored code W didn't, or vice versa) are summarized below the chain section — see HIT-COUNT DIVERGENCE for the function-level view.

depth     src  W(T/F)  L(T/F)  source
--- d=3  OSS_FUZZ_png_colorspace_set_chromaticities  (/src/libpng/png.c:1722-1754) ---
  d=3   L1733  T=0 F=1  T=30 F=10  case 0: /* success */
  d=3   L1737  T=1 F=0  T=10 F=30  case 1:
  d=3   L1745  T=0 F=1  T=0 F=40  default:
--- d=2  png.c:png_colorspace_check_xy  (/src/libpng/png.c:1619-1638) ---
  d=2   L1625  T=1 F=0  T=9 F=31  if (result != 0)
  d=2   L1629  T=0 F=0  T=0 F=31  if (result != 0)
  d=2   L1632  T=0 F=0  T=30 F=1  if (png_colorspace_endpoints_match(xy, &xy_test,
--- d=1  png.c:png_XYZ_from_xy  (/src/libpng/png.c:1277-1539) ---
  d=1   L1286  T=0 F=1  T=0 F=40  if (xy->redx   < 0 || xy->redx > PNG_FP_1) return 1;
  d=1   L1286  T=0 F=1  T=0 F=40  if (xy->redx   < 0 || xy->redx > PNG_FP_1) return 1;
  d=1   L1287  T=0 F=1  T=0 F=40  if (xy->redy   < 0 || xy->redy > PNG_FP_1-xy->redx) retur...
  d=1   L1287  T=0 F=1  T=0 F=40  if (xy->redy   < 0 || xy->redy > PNG_FP_1-xy->redx) retur...
  d=1   L1288  T=0 F=1  T=0 F=40  if (xy->greenx < 0 || xy->greenx > PNG_FP_1) return 1;  <-- BLOCKER
  d=1   L1288  T=1 F=0  T=0 F=40  if (xy->greenx < 0 || xy->greenx > PNG_FP_1) return 1;  <-- BLOCKER
  d=1   L1289  T=0 F=0  T=0 F=40  if (xy->greeny < 0 || xy->greeny > PNG_FP_1-xy->greenx) r...
  d=1   L1289  T=0 F=0  T=0 F=40  if (xy->greeny < 0 || xy->greeny > PNG_FP_1-xy->greenx) r...
  d=1   L1290  T=0 F=0  T=0 F=40  if (xy->bluex  < 0 || xy->bluex > PNG_FP_1) return 1;
  d=1   L1290  T=0 F=0  T=0 F=40  if (xy->bluex  < 0 || xy->bluex > PNG_FP_1) return 1;
  d=1   L1291  T=0 F=0  T=0 F=40  if (xy->bluey  < 0 || xy->bluey > PNG_FP_1-xy->bluex) ret...
  d=1   L1291  T=0 F=0  T=0 F=40  if (xy->bluey  < 0 || xy->bluey > PNG_FP_1-xy->bluex) ret...
  d=1   L1292  T=0 F=0  T=0 F=40  if (xy->whitex < 0 || xy->whitex > PNG_FP_1) return 1;
  d=1   L1292  T=0 F=0  T=1 F=39  if (xy->whitex < 0 || xy->whitex > PNG_FP_1) return 1;
  d=1   L1293  T=0 F=0  T=0 F=39  if (xy->whitey < 5 || xy->whitey > PNG_FP_1-xy->whitex) r...
  d=1   L1293  T=0 F=0  T=2 F=37  if (xy->whitey < 5 || xy->whitey > PNG_FP_1-xy->whitex) r...
  d=1   L1474  T=0 F=0  T=0 F=37  if (png_muldiv(&left, xy->greenx-xy->bluex, xy->redy - xy...
  d=1   L1476  T=0 F=0  T=0 F=37  if (png_muldiv(&right, xy->greeny-xy->bluey, xy->redx - x...
  d=1   L1481  T=0 F=0  T=0 F=37  if (png_muldiv(&left, xy->greenx-xy->bluex, xy->whitey-xy...
  d=1   L1483  T=0 F=0  T=0 F=37  if (png_muldiv(&right, xy->greeny-xy->bluey, xy->whitex-x...
  d=1   L1491  T=0 F=0  T=0 F=37  if (png_muldiv(&red_inverse, xy->whitey, denominator, lef...
  d=1   L1492  T=0 F=0  T=2 F=35  red_inverse <= xy->whitey /* r+g+b scales = white scale */)
  d=1   L1496  T=0 F=0  T=0 F=35  if (png_muldiv(&left, xy->redy-xy->bluey, xy->whitex-xy->...
  d=1   L1498  T=0 F=0  T=0 F=35  if (png_muldiv(&right, xy->redx-xy->bluex, xy->whitey-xy-...
  d=1   L1500  T=0 F=0  T=0 F=35  if (png_muldiv(&green_inverse, xy->whitey, denominator, l...
  d=1   L1501  T=0 F=0  T=4 F=31  green_inverse <= xy->whitey)
  d=1   L1509  T=0 F=0  T=0 F=31  if (blue_scale <= 0)
  d=1   L1514  T=0 F=0  T=0 F=31  if (png_muldiv(&XYZ->red_X, xy->redx, PNG_FP_1, red_inver...
  d=1   L1516  T=0 F=0  T=0 F=31  if (png_muldiv(&XYZ->red_Y, xy->redy, PNG_FP_1, red_inver...
  d=1   L1518  T=0 F=0  T=0 F=31  if (png_muldiv(&XYZ->red_Z, PNG_FP_1 - xy->redx - xy->red...
  d=1   L1522  T=0 F=0  T=0 F=31  if (png_muldiv(&XYZ->green_X, xy->greenx, PNG_FP_1, green...
  d=1   L1524  T=0 F=0  T=0 F=31  if (png_muldiv(&XYZ->green_Y, xy->greeny, PNG_FP_1, green...
  d=1   L1526  T=0 F=0  T=0 F=31  if (png_muldiv(&XYZ->green_Z, PNG_FP_1 - xy->greenx - xy-...
  d=1   L1530  T=0 F=0  T=0 F=31  if (png_muldiv(&XYZ->blue_X, xy->bluex, blue_scale, PNG_F...
  d=1   L1532  T=0 F=0  T=0 F=31  if (png_muldiv(&XYZ->blue_Y, xy->bluey, blue_scale, PNG_F...
  d=1   L1534  T=0 F=0  T=0 F=31  if (png_muldiv(&XYZ->blue_Z, PNG_FP_1 - xy->bluex - xy->b...

[off-chain: 181 additional divergent branches across 27 functions (see HIT-COUNT DIVERGENCE for which functions)]

==== BRANCH SEEDS (shared across decisive pairs) ====
Note: seed_bisect picks one (fuzzer, trial) per direction by lex-min, so the storing fuzzer may differ from a pair's decisive winner/loser. Each seed below carries its actual (fuzzer, trial); the bytes exercise the named branch side regardless of provenance.

==== Winner-resolving seeds (take true branch) ====
Seed 1 (id=60463be432c910b8, size=8765 bytes, fuzzer=value_profile_cmplog, trial=1, discovered_at=2914s, mutation_op=TokenReplace,WordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 19 00 00 00 45 10 02 00 00 00 52 ed aa   .......E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 68 49 53 54 01 d9 c9 2c 7f 00 00   .....hIST...,...

==== Loser-blocking seeds (take false branch) ====
Seed 1 (id=00148067fb51cd97, size=8759 bytes, fuzzer=cmplog, trial=3, discovered_at=0s):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 2 (id=02947d885c368b4b, size=8759 bytes, fuzzer=cmplog, trial=3, discovered_at=0s, mutation_op=BytesExpandMutator,BytesExpandMutator,ByteDecMutator,BytesDeleteMutator,ByteRandMutator,BytesInsertCopyMutator,TokenInsert):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 3 (id=035d27bda46a0fdc, size=8759 bytes, fuzzer=cmplog, trial=4, discovered_at=0s):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 4 (id=043dd78f0a522c88, size=4957 bytes, fuzzer=cmplog, trial=5, discovered_at=0s, mutation_op=ByteFlipMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...
Seed 5 (id=053e20fe503a3ed5, size=8759 bytes, fuzzer=cmplog, trial=5, discovered_at=1s, mutation_op=DwordAddMutator):
  0000: 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52   .PNG........IHDR
  0010: 00 00 00 5b 00 00 00 45 08 06 00 00 01 52 ed aa   ...[...E.....R..
  0020: e4 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61   .....gAMA......a
  0030: 05 00 00 00 01 73 52 47 42 01 d9 c9 2c 7f 00 00   .....sRGB...,...


==== BYTE DIFF (W vs L at common offsets) ====
Per-offset byte sets. Format: hex(ascii)xCOUNT. Shows offsets where W and L bytes differ AND at least one side is concentrated (≤4 distinct values) — likely-informative dataflow signal.

 Offset  W bytes                             L bytes                             tag
   0x0012  00(.)x1                             00(.)x39 01(.)x1                    PARTIAL
   0x0013  19(.)x1                             5b([)x23 03(.)x4 05(.)x3 02(.)x2 +6u  DIFFER
   0x0015  00(.)x1                             00(.)x38 0f(.)x1 03(.)x1            PARTIAL
   0x0016  00(.)x1                             00(.)x36 42(B)x1 e8(.)x1 01(.)x1 +1u  PARTIAL
   0x0017  45(E)x1                             45(E)x22 01(.)x2 2b(+)x2 e5(.)x2 +9u  PARTIAL
   0x0018  10(.)x1                             08(.)x31 10(.)x3 04(.)x3 01(.)x2 +1u  PARTIAL
   0x0019  02(.)x1                             06(.)x22 00(.)x11 04(.)x5 03(.)x2   DIFFER
   0x001c  00(.)x1                             01(.)x30 00(.)x10                   PARTIAL
   0x0025  67(g)x1                             67(g)x37 68(h)x2 74(t)x1            PARTIAL
   0x0026  41(A)x1                             41(A)x37 49(I)x2 52(R)x1            PARTIAL
   0x0027  4d(M)x1                             4d(M)x37 53(S)x2 4e(N)x1            PARTIAL
   0x0028  41(A)x1                             41(A)x37 54(T)x2 53(S)x1            PARTIAL
   0x0030  05(.)x1                             05(.)x38 02(.)x1 00(.)x1            PARTIAL
   0x0035  68(h)x1                             73(s)x38 69(i)x1 74(t)x1            DIFFER
   0x0036  49(I)x1                             52(R)x38 54(T)x1 45(E)x1            DIFFER
   0x0037  53(S)x1                             47(G)x37 58(X)x2 48(H)x1            DIFFER
   0x0038  54(T)x1                             42(B)x38 74(t)x2                    DIFFER
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
  /home/miao/BlockerAnalyzer/prompts/libpng_3833.analysis.json

Do NOT produce template.c or params.json — those are the deferred verification phase.

SCHEMA (every field is mandatory; missing or empty fields = analysis failure). The example below uses `//` comments for guidance — REMOVE all `//` lines and inline `//` comments from your emitted JSON (standard JSON does not allow comments).

{
  "branch_id": 3833,
  "target": "libpng",
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
    "verification_method": "ran `python3 tools/db_query.py lineage --branch 3833 --role W --fuzzer cmplog --trial 1 --seed <ID>` and observed an I2S-floor row (mutation_op = -) at depth 19 of the chain"
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
  python3 tools/db_query.py lineage --branch 3833 --role W|L --fuzzer <F> --trial <T> --seed <id>
    MANDATORY when claimed_mechanism="I2SRandReplace" (see RULES). Optional otherwise. Returns the ancestor chain (mutation ops walked back from the leaf up to 50 levels). The trailing 'I2S-floor signal' line summarizes dash rows (mutation_op = -); see fuzzer_mechanism_library.md cmplog section for the floor interpretation under the current build.
  python3 tools/db_query.py more-seeds --branch 3833 --role W|L [--fuzzer <F>] [--limit 20] [--show-bytes 64]
    Optional. Additional seeds beyond the 5 shown above (capped by seed_bisect's max_seeds; default 10 per branch x direction).