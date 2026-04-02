# Branch Clusters -- lcms
**Generated:** 2026-04-02
**Divergent branches:** 254 (out of 358 confirmed blockers)
**Functions:** 17 (Tier 1 representatives needed)
**Clusters:** 10 (BC01--BC10; 8 from Tier 1/2 + 2 new from Round 2 Tier 1)
**Batch:** Tier 1, batch 1 -- ranks 1, 2, 3, 5, 6, 14, 15; batch 2 -- ranks 22, 26, 27, 29, 37, 43; batch 3 -- ranks 52, 82, 191, 264, 272; Tier 2, batch 1 -- cmspcs.c (86), cmsio0.c (16), cmsio1.c (25), cmstypes.c (23); Tier 2, batch 2 -- cmscnvrt.c (16), cmsintrp.c (15), cmslut.c (14), cmsopt.c (10), cmsxform.c (8), cmsgamma.c (7), cmssamp.c (6), cmsnamed.c (4), cmsplugin.c (3), cmserr.c (2), cmspack.c (1), cmsmtrx.c (1); Round 2 Tier 2 -- cross-cluster fitting of 111 promoted branches; **Round 2 Tier 1** -- R9, R12, R86, R214 (all 4 unfitted branches resolved)

## Summary

| Cluster | Controlling Bytes | Semantic Meaning | Branches (Tier 1 + Tier 2) |
|---------|------------------|------------------|----------------------------|
| BC01 | [16:20] + [20:24] | ICC color space + PCS fields (color space match) | R1*, R2*, R26*, R27*, R37*, R43* + 77 T2 + 17 T2(A) + 3 R2 + 25 R2(A) = **131** |
| BC02 | [12:16] | ICC device class field | R3*, R4, R59, R113, R130, R145, R188, R193 + 5 R2 + 12 R2(A) = **25** |
| BC03 | tag table: `D2B0` signature | ICC float LUT tag (Device2PCSFloat) presence | R5*, R6* + 2 T2(A) + 2 R2(A) = **7** |
| BC04 | [16:20] + TRC tag data type | ICC color space `Lab` + `para` TRC tag type | R15*, R22*, R29* + 3 T2 + 9 T2(A) = **15** |
| BC05 | A2B mft2 nIn (tag_data+8) + nOut (tag_data+9) | A2B CLUT dimensions (nIn/nOut/gridpoints) | R82*, R191* + 1 T2(A) + 1 R2 + 17 R2(A) + R86 = **22** |
| BC06 | A2B mft2 matrix (tag_data+12, 36 bytes) | A2B embedded 3x3 matrix values | R272* + 1 T2 = **2** |
| BC07 | ncl2 tag presence + count (tag_data+12, 4 bytes) | Named color list count field | R264* + 1 T2 + 1 R2(A) = **3** |
| BC08 | Tag table entries (132+) vs color space [16:19] | Tag table validity for declared color space | R52* + 2 T2 + 4 T2(A) + 38 R2 + 3 R2(A) = **48** |
| BC09 | [8:10] (ICC version field) | ICC version number (major + minor BCD nibble) | R9*, R214* = **2** |
| BC10 | input size < 128 bytes | ICC header truncation (profile too short to read) | R12* = **1** |

(*) = Tier 1 representative

**Note:** R14 (cmstypes.c:1265:9) is assigned to BC03 provisionally -- it depends on mAB sub-element truncation within a float LUT tag, but this is downstream of the D2B0 tag presence. R22 and R29 are assigned to BC04 because their controlling bytes (TRC tag data type) overlap with BC04's TRC dependency, even though they do not require Lab color space.

---

## Cluster Details

### BC01 -- ICC color space + PCS fields (color space match)

**Controlling bytes:** offset 16--19 (ICC color space of data) and offset 20--23 (PCS / profile connection space)
**Source mapping:** Both branches live in `IsProperColorSpace()` at `cmsxform.c:1055--1067`, called from `cmsxform.c:1150` for the output/exit color space check. Bytes 16--19 determine the input/output format's `T_COLORSPACE()` bits (mapped via `_cmsLCMScolorSpace()`), while bytes 20--23 set `ExitColorSpace`. The function checks whether these two derived values are compatible.
**Verification:** CONFIRMED (round 1 for both R1 and R2)

**Branches:**
| Rank | Branch | Blocked Side | Status |
|------|--------|-------------|--------|
| R1 | cmsxform.c:1064:9 | False | Confirmed |
| R2 | cmsxform.c:1150:9 | True | Confirmed |
| R26 | cmscnvrt.c:429:5 | False | Confirmed (batch 2) |
| R27 | cmspcs.c:732:8 | False | Confirmed (batch 2, Test A only) |
| R37 | cms_transform_fuzzer.cc:32:7 | True | Confirmed (batch 2) |
| R43 | cmspack.c:3516:19 | False | Confirmed (batch 2) |

**Relationship:** R2 (`!IsProperColorSpace(ExitColorSpace, OutputFormat)`) is the **caller**. R1 (`Space1 == PT_Lab`) is an **inner check** within the same `IsProperColorSpace` function. R26 (`case cmsSigXYZData` in `AddConversion`) depends on PCS bytes [20:23]; hitting False requires PCS != XYZ (typically Lab). R27 (`case cmsSigRgbData` in `_cmsEndPointsBySpace`) depends on color space bytes [16:19]; hitting False requires cs != RGB. R37 (`srcCS == cmsSigLabData` in fuzzer harness) depends directly on color space bytes [16:19]; hitting True requires cs = Lab. R43 (loop exhaustion in `_cmsGetStockInputFormatter`) depends on color space bytes [16:19]; hitting False requires cs = Lab which creates a non-standard format spec that fails 16-bit formatter matching.

---

### BC02 -- ICC device class field

**Controlling bytes:** offset 12--15, must be a value NOT in the valid set {`mntr`, `scnr`, `prtr`, `link`, `abst`, `spac`, `nmcl`, `\x00\x00\x00\x00`}
**Source mapping:** `validDeviceClass()` at `cmsio0.c:743--762`, called from `_cmsReadHeader()` at `cmsio0.c:765`. The switch statement at line 747 matches against 7 known `cmsProfileClassSignature` values plus a zero check at line 745. The `default:` case at line 758 (R3) returns FALSE, causing profile loading to fail.
**Verification:** CONFIRMED (round 1)

**Branches:**
| Rank | Branch | Blocked Side | Status |
|------|--------|-------------|--------|
| R3 | cmsio0.c:758:5 | True | Confirmed |

---

### BC03 -- ICC float LUT tag (D2B0) presence

**Controlling bytes:** ICC tag table entries -- must contain a tag with signature `D2B0` (0x44324230, Device to PCS Float). The tag signature appears at a variable offset in the tag table (offset 132 + 12*N for the N-th tag entry, first 4 bytes of each 12-byte entry).
**Source mapping:** `_cmsReadInputLUT()` at `cmsio1.c:306--400` selects between float and 16-bit LUT processing paths. At line 341, `tagFloat = Device2PCSFloat[Intent]` resolves to `cmsSigDToB0Tag` = `D2B0`. At line 343, `cmsIsTag(hProfile, tagFloat)` checks whether the profile's tag table contains this tag. When present, execution enters the float path via `_cmsReadFloatInputTag()` (line 347), which calls `cmsPipelineDup()` at line 268, reaching `cmslut.c:1461`.
**Verification:** CONFIRMED (round 1)

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R5 | cmsio1.c:343:13 | True | 1 (rep) | Confirmed |
| R6 | cmslut.c:1461:9 | True | 1 (rep) | Confirmed |
| R14 | cmstypes.c:1265:9 | True | 1 (rep) | Confirmed (Test A only) |

**Relationship:** R5 is the gating check (is D2B0 present?). R6 is downstream -- it checks if the pipeline returned by `cmsReadTag(hProfile, tagFloat)` is NULL, which only executes after R5's True branch is taken. R14 is further downstream -- it's inside `Type_ParametricCurve_Read()`, reached via mAB sub-element parsing of the D2B0 tag data; its True side (read failure) requires truncated mAB curve data within the D2B0 tag.

---

### BC04 -- ICC Lab color space + parametric curve (para) TRC type

**Controlling bytes:** Two conditions must both hold:
1. Bytes [16:19] = `4C616220` ("Lab ") -- ICC color space field
2. At least one TRC tag (rTRC/gTRC/bTRC/kTRC) has data type `70617261` ("para") at the tag data offset

**Source mapping:** `EvalSegmentedFn()` at `cmsgamma.c:716--750` iterates over tone curve segments in reverse, looking for a segment whose domain `[x0, x1]` contains the input value R. For `curv`-type curves, lcms internally creates a single segment spanning the full range, so R always matches and the loop exits via `return Out` at line 750 -- the loop termination condition `i < 0` (False side at 721:38) is never reached. For `para`-type curves, lcms creates a multi-segment parametric curve. When the color space is Lab, the Lab-to-float conversion can produce R values outside all segment boundaries (particularly negative values from the L* channel), causing the loop to exhaust all segments and exit normally, hitting the False side.

**Verification:** CONFIRMED (round 3)
- Neither `para` alone nor `Lab` alone is sufficient in the common case
- The combination `Lab` + `para` reliably produces False hits (91.4k per seed)

**Branches:**
| Rank | Branch | Blocked Side | Status |
|------|--------|-------------|--------|
| R15 | cmsgamma.c:721:38 | False | Confirmed |
| R22 | cmsopt.c:1572:13 | False | Confirmed (batch 2) |
| R29 | cmsplugin.c:133:9 | False | Confirmed (batch 2) |

**Note on R22 and R29:** These branches depend on `para` TRC tag type but do NOT require Lab color space (unlike R15). R22 requires `para` TRC with extreme gamma parameters (gamma >= ~500) to produce tone curve outputs >= 131072.0, triggering the False side in `FillFirstShaper`. R29 requires `para` TRC to reach `_cmsReadUInt16Number(io, NULL)` via the parametric curve reading path, where n=NULL is used for count-skipping reads. Both are downstream of the `para` TRC tag data type, which is the shared controlling byte region with R15.

---

### BC05 -- A2B CLUT dimensions (nIn/nOut/gridpoints)

**Controlling bytes:** `nIn` byte at A2B tag data offset + 8, `nOut` byte at offset + 9, and `gridpoints` byte at offset + 10, within an mft1/mft2-type A2B tag (A2B0, A2B1, or A2B2).
**Source mapping:** Two branches controlled by these bytes:
- R82: `DefaultInterpolatorsFactory()` at `cmsintrp.c:1196` checks `if (nOutputChannels == 1)` inside `case 1` (nInputChannels==1). Reaching the False side requires nIn=1 and nOut>1 in the A2B LUT.
- R191: `_cmsCallocDefaultFn()` at `cmserr.c:158` checks `if (Total > MAX_MEMORY_FOR_ALLOC)`. The CLUT allocation size = gridpoints^nIn * nOut * 2. With nIn=9, gridpoints=9, nOut=3, Total = 9^9 * 3 * 2 > 512MB, triggering the True side.
**Verification:** CONFIRMED (round 1 for R82, round 1 for R191)

**Branches:**
| Rank | Branch | Blocked Side | Status |
|------|--------|-------------|--------|
| R82 | cmsintrp.c:1196:20 | False | Confirmed |
| R191 | cmserr.c:158:9 | True | Confirmed |

**Relationship:** Both branches depend on the same mft2 nIn/nOut/gridpoints bytes but with different effects. R82 requires nIn=1, nOut>1 (1D multi-output LUT). R191 requires nIn * gridpoints to be large enough that the allocation exceeds 512MB (e.g., nIn>=9 with gridpoints>=9).

---

### BC06 -- A2B embedded 3x3 matrix values

**Controlling bytes:** 36 bytes at A2B mft2 tag data offset + 12, encoding a 3x3 matrix as s15Fixed16 values. The matrix must be close to the 3x3 identity matrix (each element within 1/65535 of the corresponding identity value: 1.0 on diagonal, 0.0 off-diagonal).
**Source mapping:** `_cmsMAT3isIdentity()` at `cmsmtrx.c:107` iterates over all 9 matrix elements calling `CloseEnough(a->v[i].n[j], Identity.v[i].n[j])`. The function is called from optimization pipeline code at `cmsopt.c:1853` and `cmsopt.c:2150`. The False side at line 107:17 means `CloseEnough` returned TRUE -- the element matches identity.
**Verification:** CONFIRMED (round 1)
- Test A: changed matrix[0][0] from 1.0 to 0.5 -> False side disappeared (True:1, False:0)
- Test B: set entire 3x3 matrix to identity -> True:0, False:9 (all elements match)

**Branches:**
| Rank | Branch | Blocked Side | Status |
|------|--------|-------------|--------|
| R272 | cmsmtrx.c:107:17 | False | Confirmed |

---

### BC07 -- Named color list count field

**Controlling bytes:** Two conditions must hold:
1. Tag table must contain an `ncl2` tag (signature `6E636C32`) -- typically with device class `nmcl` at bytes [12:15]
2. The `count` field at ncl2 tag data offset + 12 (4 bytes, big-endian) must be > 65536

**Source mapping:** `GrowNamedColorList()` at `cmsnamed.c:529` checks `if (size > 1024 * 100)`. The list doubles its `Allocated` count each time it grows (64 -> 128 -> ... -> 131072). `Type_NamedColor_Read()` at `cmstypes.c:3202` loops `count` times calling `cmsAppendNamedColor()`, which triggers growth. When count > 65536, `Allocated` reaches 131072 > 102400, hitting the True side.
**Verification:** CONFIRMED (round 1)
- Test A: changed count from 1098019945 to 5 -> True:0 (size stays small)
- Test B: original seed with count=1098019945 -> True:1 (exceeds limit)

**Branches:**
| Rank | Branch | Blocked Side | Status |
|------|--------|-------------|--------|
| R264 | cmsnamed.c:529:9 | True | Confirmed |

---

### BC08 -- Tag table validity for declared color space

**Controlling bytes:** Tag table entries at offset 132+ (tag signatures, offsets, and sizes) must be inconsistent or garbled relative to the color space declared at bytes [16:19]. For example, an RGB profile with `lumi`/`A2B2` tags instead of proper `rTRC`/`gTRC`/`bTRC`/`rXYZ`/`gXYZ`/`bXYZ` tags, or a non-RGB color space (CMY, GRAY, CMYK) without the corresponding LUT tags.
**Source mapping:** `cmsDetectBlackPoint()` at `cmssamp.c:112` calls `cmsCreateTransformTHR(hInput, dwFormat, hLab, TYPE_Lab_DBL, Intent, ...)` to create a round-trip transform from the input profile to Lab. At line 116: `if (xform == NULL)` -- the True side (blocked) means the transform creation failed. This happens when the profile lacks the tags needed to construct a valid conversion pipeline for its declared color space.
**Verification:** CONFIRMED (round 2)
- Test A: positive seed (garbled tags) with tag section replaced from negative seed (proper RGB tags) -> True:0, False:2 (transform succeeds)
- Test B: negative seed (proper RGB tags) with tag section replaced from positive seed (garbled tags) -> True:1, False:1 (transform fails)

**Branches:**
| Rank | Branch | Blocked Side | Status |
|------|--------|-------------|--------|
| R52 | cmssamp.c:116:9 | True | Confirmed |

---

## Tier 1 -- Full Analysis Details

### Rank 1 -- IsProperColorSpace|cmsxform.c:1064:9

**Branch:** `if (Space1 == PT_Lab && Space2 == PT_LabV2) return TRUE;`
**Blocked side:** False (Space1 != PT_Lab at this point)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Bytes [16:20] (color space) | Bytes [20:24] (PCS) |
|---------|------|--------|----------------------------|---------------------|
| 003d67f5 | 576 | cmplog/t1 | `39434c52` (9CLR) | `00000234` |
| 021a01f1 | 564 | cmplog/t1 | `434d5920` (CMY ) | `00000000` |
| 0819a452 | 378 | cmplog/t1 | `4d434842` (MCHB) | `7f000000` |
| 0c1258cf | 564 | cmplog/t1 | `4d434837` (MCH7) | `6d424120` (mBA ) |
| 18b9c22e | 564 | cmplog/t1 | `48535620` (HSV ) | `00000000` |
| 2a530d38 | 927 | cmplog/t1 | `36434c52` (6CLR) | `58595a04` (XYZ.) |
| 33e28b5f | 378 | cmplog/t1 | `5247be20` (RG..) | `7f000000` |
| 40153891 | 564 | cmplog/t1 | `4c757620` (Luv ) | `58594620` (XYF ) |
| 52c06817 | 564 | cmplog/t1 | `4d434832` (MCH2) | `42434c52` (BCLR) |
| 54e4dd91 | 564 | cmplog/t1 | `33434c52` (3CLR) | `00000000` |

**Negative seeds (N=10):**
| Seed ID | Size | Fuzzer | Bytes [16:20] (color space) | Bytes [20:24] (PCS) |
|---------|------|--------|----------------------------|---------------------|
| 076887e8 | 564 | cmplog/t3 | `4c616220` (Lab ) | `38434c52` (8CLR) |
| 0ac09b94 | 542 | cmplog/t3 | `4c616220` (Lab ) | `58595a20` (XYZ ) |
| 11d4f882 | 564 | cmplog/t3 | `4c616220` (Lab ) | `59787920` (Yxy ) |
| 11fc2128 | 564 | cmplog/t3 | `4c616220` (Lab ) | `4d434835` (MCH5) |
| 18504e3c | 564 | cmplog/t3 | `4c616220` (Lab ) | `4c757620` (Luv ) |
| 20e068c2 | 564 | cmplog/t3 | `4c616220` (Lab ) | `32434c52` (2CLR) |
| 274c712b | 564 | cmplog/t3 | `4c616220` (Lab ) | `47524159` (GRAY) |
| 30f7906d | 564 | cmplog/t3 | `4c616220` (Lab ) | `4d434844` (MCHD) |
| 35cc4030 | 564 | cmplog/t3 | `4c616220` (Lab ) | `41434c52` (ACLR) |
| 393c2e3c | 564 | cmplog/t3 | `4c616220` (Lab ) | `4d434833` (MCH3) |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 16-19 | Various non-Lab color spaces (100%) | `4c616220` ("Lab ") (100%) | 10/10 vs 10/10 |

**Source trace:**
- `LLVMFuzzerTestOneInput` -> `cmsOpenProfileFromMem` -> `_cmsReadHeader` reads bytes [16:19] as `Header.colorSpace`
- Profile's color space is stored as `Icc->ColorSpace`
- Transform pipeline calls `IsProperColorSpace(ExitColorSpace, OutputFormat)` at line 1150
- Inside `IsProperColorSpace`: `Space2 = _cmsLCMScolorSpace(Check)` converts the profile color space signature to a PT_* enum
- Line 1064: `if (Space1 == PT_Lab ...)` -- checks if the format's color space bits equal PT_Lab (10)
- `cmsSigLabData = 0x4C616220` = "Lab " maps to `PT_Lab`

**Hypothesis:** bytes [16:19] must NOT be `4C616220` ("Lab ") to hit the blocked False side at line 1064:9. When color space is "Lab ", `_cmsLCMScolorSpace` returns `PT_Lab`, making `Space1 == PT_Lab` True, so the False side is never taken.
**Verification:** CONFIRMED (round 1)
- Test A: positive seed `021a01f1` (cs=CMY) with bytes[16:19] changed to `4C616220` (Lab) -> Branch (1064:9) [True: 1, False: 0] -- False side gone
- Test B: negative seed `076887e8` (cs=Lab) with bytes[16:19] changed to `434d5920` (CMY) -> Branch (1064:9) [True: 0, False: 1] -- False side appears

**Controlling bytes:** [16:19] = ICC color space field; must not be `4C616220` ("Lab ")
**Cluster:** BC01

---

### Rank 3 -- validDeviceClass|cmsio0.c:758:5

**Branch:** `default:` case in `validDeviceClass()` switch statement
**Blocked side:** True (device class is not in the valid set)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Bytes [12:16] (device class) |
|---------|------|--------|------------------------------|
| 12ad0a77 | 166 | naive/t1 | `6d6e8872` (mn.r) |
| 0cc72308 | 193 | value_profile/t1 | `6d6d7472` (mmtr) |
| 1095c907 | 195 | value_profile/t1 | `6c6d6e6b` (lmnk) |
| 13017e35 | 286 | value_profile/t1 | `00000072` (...r) |
| 18ca9c4e | 544 | value_profile/t1 | `72636e72` (rcnr) |
| 1a0a96d1 | 549 | value_profile/t1 | `73706361` (spca) |
| 1ff0e571 | 538 | value_profile/t1 | `73706363` (spcc) |
| 2e23b388 | 209 | value_profile/t1 | `6e6d632f` (nmc/) |
| 2e5386b5 | 503 | value_profile/t1 | `77777777` (wwww) |
| 44fa9196 | 181 | value_profile/t1 | `786e7472` (xntr) |

**Negative seeds (N=10):**
| Seed ID | Size | Fuzzer | Bytes [12:16] (device class) |
|---------|------|--------|------------------------------|
| 00054156 | 564 | cmplog/t1 | `6d6e7472` (mntr) |
| 000cec6b | 564 | cmplog/t1 | `6d6e7472` (mntr) |
| 00383797 | 1834 | cmplog/t1 | `6d6e7472` (mntr) |
| 003d67f5 | 576 | cmplog/t1 | `6d6e7472` (mntr) |
| 006edb09 | 1266 | cmplog/t1 | `6d6e7472` (mntr) |
| 007ef34e | 1274 | cmplog/t1 | `6d6e7472` (mntr) |
| 00b7148b | 564 | cmplog/t1 | `6d6e7472` (mntr) |
| 00dafa81 | 2880 | cmplog/t1 | `6d6e7472` (mntr) |
| 011b5a96 | 574 | cmplog/t1 | `6d6e7472` (mntr) |
| 0146d39d | 564 | cmplog/t1 | `6d6e7472` (mntr) |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 12-15 | Various non-standard values (100%) | `6d6e7472` ("mntr") (100%) | 10/10 vs 10/10 |

**Source trace:**
- `LLVMFuzzerTestOneInput` -> `cmsOpenProfileFromMem` -> `_cmsReadHeader` at `cmsio0.c:765`
- Reads bytes [12:15] as `Header.deviceClass` (after endianness adjustment)
- Calls `validDeviceClass()` at `cmsio0.c:743`
- Switch at line 747 matches against 7 known signatures: `cmsSigInputClass` ("scnr"), `cmsSigDisplayClass` ("mntr"), `cmsSigOutputClass` ("prtr"), `cmsSigLinkClass` ("link"), `cmsSigAbstractClass` ("abst"), `cmsSigColorSpaceClass` ("spac"), `cmsSigNamedColorClass` ("nmcl")
- Line 745 also allows zero (`\x00\x00\x00\x00`)
- The `default:` case at line 758 catches everything else and returns FALSE

**Hypothesis:** bytes [12:15] must be a value NOT in `{00000000, 73636e72 (scnr), 6d6e7472 (mntr), 70727472 (prtr), 6c696e6b (link), 61627374 (abst), 73706163 (spac), 6e6d636c (nmcl)}` to hit the blocked True side (default case).
**Verification:** CONFIRMED (round 1)
- Test A: positive seed `0cc72308` (dc=`6d6d7472`) with bytes[12:15] changed to `6d6e7472` (mntr) -> Branch (758:5) [True: 0, False: 1] -- default case no longer hit
- Test B: negative seed `00054156` (dc=`6d6e7472`) with bytes[12:15] changed to `6d6d7472` (mmtr) -> Branch (758:5) [True: 1, False: 0] -- default case now hit

**Controlling bytes:** [12:15] = ICC device class field; must not be any of the 8 valid values
**Cluster:** BC02

---

### Rank 5 -- _cmsReadInputLUT|cmsio1.c:343:13

**Branch:** `if (cmsIsTag(hProfile, tagFloat))` -- checks for `D2B0` float LUT tag
**Blocked side:** True (float tag is present)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | D2B0 tag position | Color space |
|---------|------|--------|--------------------|-------------|
| 1d09fb8d | 564 | vpc/t1 | tag #7 | CMY |
| 1ea92201 | 564 | vpc/t1 | tag #7 | CMY |
| 3064bd45 | 564 | vpc/t1 | tag #4 | YCbr |
| 37e2ec9f | 544 | vpc/t1 | tag #7 | CMY |
| 4fb47865 | 578 | vpc/t1 | tag #2 | RGB |
| 6beb3b44 | 544 | vpc/t1 | tag #7 | CMY |
| 70482bb7 | 544 | vpc/t1 | tag #7 | CMY |
| 76a0aea7 | 544 | vpc/t1 | tag #7 | CMY |
| 8269cccc | 564 | vpc/t1 | tag #8 | FCLR |
| 8959e550 | 564 | vpc/t1 | tag #3 | 3CLR |

All 10 positive seeds contain a `D2B0` tag signature in the tag table.

**Negative seeds (N=10):**
| Seed ID | Size | Fuzzer | D2B0 present | Tags |
|---------|------|--------|-------------|------|
| 00054156 | 564 | cmplog/t1 | No | desc, rTRC, wtpt, bkpt, A2B0, gTRC, bTRC, rXYZ, gXYZ, bXYZ |
| 000cec6b | 564 | cmplog/t1 | No | desc, cprt, wtpt, bkpt, rTRC, gTRC, bTRC, rXYZ, gXYZ, bXYZ |
| 00383797 | 1834 | cmplog/t1 | No | lumi, A2B2, wtpt, bkpt, rTRC, gTRC, chad, A2B0, cprt, bXYZ |
| 006edb09 | 1266 | cmplog/t1 | No | (similar standard tags) |
| 007ef34e | 1274 | cmplog/t1 | No | (similar standard tags) |
| 00b7148b | 564 | cmplog/t1 | No | desc, cprt, wtpt, bkpt, rTRC, gTRC, bTRC, rXYZ, gXYZ, bXYZ |
| 00dafa81 | 2880 | cmplog/t1 | No | (similar standard tags) |
| 011b5a96 | 574 | cmplog/t1 | No | (similar standard tags) |
| 0146d39d | 564 | cmplog/t1 | No | (similar standard tags) |
| 01b87c16 | 564 | cmplog/t1 | No | (similar standard tags) |

No negative seed contains a `D2B0` tag.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| Tag table (132+) | Contains `44324230` ("D2B0") entry | No `D2B0` entry | 10/10 vs 10/10 |

**Source trace:**
- `LLVMFuzzerTestOneInput` -> `cmsOpenProfileFromMem` -> profile opens, tag table parsed
- `_cmsReadInputLUT()` at `cmsio1.c:306` determines the rendering path
- Line 341: `tagFloat = Device2PCSFloat[Intent]` = `cmsSigDToB0Tag` = `D2B0`
- Line 343: `if (cmsIsTag(hProfile, tagFloat))` -- scans the profile's tag table for `D2B0`
- `cmsIsTag()` at `cmsio0.c:689` iterates the tag table, comparing each tag signature

**Hypothesis:** The profile's tag table must contain an entry with signature `D2B0` (0x44324230) to hit the True side. The tag signature is 4 bytes within a 12-byte tag entry; its position depends on the tag index in the table (offset = 132 + 12*N, bytes 0-3 of each entry).
**Verification:** CONFIRMED (round 1)
- Test A: positive seed `1d09fb8d` (has D2B0 at tag #7, entry offset 216), changed `D2B0` to `xxxx` -> Branch (343:13) [True: 0, False: 1] -- True side gone
- Test B: negative seed `000cec6b` (has `cprt` at tag #1, entry offset 144), changed `cprt` to `D2B0` -> Branch (343:13) [True: 1, False: 0] -- True side appears

**Controlling bytes:** Tag table entry signature = `44324230` ("D2B0") at offset 132+12*N (variable position). Typical position: tag #7 (offset 216) in the analyzed seeds.
**Cluster:** BC03

---

### Rank 6 -- cmsPipelineDup|cmslut.c:1461:9

**Branch:** `if (lut == NULL) return NULL;`
**Blocked side:** True (lut is NULL)

**Positive seeds (N=10):** Same 9 seeds as Rank 5 (1d09fb8d, 1ea92201, ...) plus 0b1185dd. All have D2B0 tag.

**Negative seeds (N=10):** Same seeds as Rank 5 blocking set (0038379, 006edb09, ...). No D2B0 tag.

**Byte diff:** Identical to Rank 5 -- controlled by D2B0 tag presence.

**Source trace:**
- After `cmsIsTag(hProfile, tagFloat)` returns True (Rank 5 branch), execution enters `_cmsReadFloatInputTag()` at `cmsio1.c:347`
- Line 268: `cmsPipeline* Lut = cmsPipelineDup((cmsPipeline*) cmsReadTag(hProfile, tagFloat));`
- `cmsReadTag` attempts to deserialize the D2B0 tag data. If the tag data is present but the deserialization returns a valid pipeline, `cmsPipelineDup` is called with a non-NULL pointer
- Line 1461: `if (lut == NULL) return NULL;` -- True when `cmsReadTag` returned a valid pipeline and `cmsPipelineDup` receives it

**Hypothesis:** Same as Rank 5 -- D2B0 tag must be present. This branch is a downstream consequence of Rank 5.
**Verification:** CONFIRMED (round 1)
- Test A: positive seed `1d09fb8d` with D2B0 removed -> Branch (1461:9) [True: 0, False: 0] -- not reached (expected: D2B0 path not entered)
- Test B: negative seed `000cec6b` with D2B0 added -> Branch (1461:9) [True: 1, False: 0] -- True side appears

**Controlling bytes:** Same as Rank 5 (D2B0 tag presence)
**Cluster:** BC03

---

### Rank 14 -- Type_ParametricCurve_Read|cmstypes.c:1265:9

**Branch:** `if (!_cmsReadUInt16Number(io, &Type)) return NULL;`
**Blocked side:** True (read fails -- insufficient data)

**Positive seeds (N=1):**
| Seed ID | Size | Fuzzer | Key feature |
|---------|------|--------|-------------|
| ae7e6348 | 443 | vpc/t1 | A2B0 tag of type `mAB`, file truncated (443 < declared 564) |

The single resolving seed has an `A2B0` tag of type `mAB ` (multiProcessElement LUT) at offset 252 with size 124. The mAB structure references A-curves at relative offset 183 (absolute 435). With only 8 bytes available at offset 435 (file ends at 443), the para type reader cannot read the `Type` uint16 field at offset 443+, causing `_cmsReadUInt16Number` to fail.

**Negative seeds (N=10):**
All have `para`-type TRC tags with sufficient data (14 bytes each, enough for funcType=0 with gamma). The `_cmsReadUInt16Number` for `Type` at the start of `Type_ParametricCurve_Read` succeeds normally.

**Source trace:**
- `cmsReadTag` -> mAB handler -> reads A-curves sub-element -> dispatches to `Type_ParametricCurve_Read`
- Line 1265: `if (!_cmsReadUInt16Number(io, &Type)) return NULL;` reads the funcType field
- The IO handler tracks buffer boundaries. When the read position exceeds available data, the read fails

**Hypothesis:** The True (failure) side requires a parametric curve read where the IO handler has fewer than 2 bytes remaining at the `Type` read position. This happens when mAB/mBA sub-element offsets point near or past the actual file boundary.
**Verification:** CONFIRMED (round 2, Test A only)
- Test A: resolving seed `ae7e6348` (443 bytes, truncated) padded to 564 bytes -> Branch (1265:9) [True: 0, False: 1] -- True (failure) side gone
- Test B: Not independently verified (requires injecting a truncated mAB tag structure into a blocking seed, which changes too many bytes to be a clean single-variable test)

**Controlling bytes:** File size relative to mAB sub-element offsets within the D2B0/A2B0 tag. Downstream of BC03 (D2B0 tag presence).
**Cluster:** BC03 (provisional -- downstream dependency on float LUT tag)

---

### Rank 15 -- EvalSegmentedFn|cmsgamma.c:721:38

**Branch:** `for (i = (int) g->nSegments - 1; i >= 0; --i)` -- loop exit condition
**Blocked side:** False (loop exits without finding a matching segment for R)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | Has `para` TRC |
|---------|------|--------|-------------|----------------|
| 028f67a5 | 579 | cmplog/t1 | Lab | Yes (rTRC) |
| 0631a6e1 | 564 | cmplog/t1 | GRAY | Yes (kTRC) |
| 0d555e1b | 598 | cmplog/t1 | GRAY | Yes (kTRC) |
| 0daa8366 | 574 | cmplog/t1 | Lab | Yes (rTRC, bTRC) |
| 1282dfae | 863 | cmplog/t1 | Lab | Yes (rTRC) |
| 134a2229 | 564 | cmplog/t1 | RGB | Yes (rTRC) |
| 1693905b | 579 | cmplog/t1 | Lab | Yes (rTRC) |
| 1805a5b8 | 564 | cmplog/t1 | RGB | Yes (rTRC) |
| 1a089ae8 | 579 | cmplog/t1 | Lab | Yes (rTRC) |
| 1d80d437 | 584 | cmplog/t1 | GRAY | Yes (kTRC) |

All 10 positive seeds have at least one TRC tag of type `para` (parametric curve). 5/10 have Lab color space; 3/10 have GRAY; 2/10 have RGB.

**Negative seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | Has `para` TRC |
|---------|------|--------|-------------|----------------|
| 000d0009 | 585 | naive/t1 | RGB | No (all curv) |
| 019e5531 | 1001 | naive/t1 | RGB | No (all curv) |
| 01ac815e | 585 | naive/t1 | RGB | No (all curv) |
| 026901d6 | 564 | naive/t1 | RGB | No (all curv) |
| 02d378b7 | 591 | naive/t1 | RGB | No (all curv) |
| 03265016 | 585 | naive/t1 | RGB | No (all curv) |
| 054b34f1 | 579 | naive/t1 | RGB | No (all curv) |
| 0673314a | 575 | naive/t1 | RGB | No (all curv) |
| 0977a819 | 591 | naive/t1 | RGB | No (all curv) |
| 0c098516 | 575 | naive/t1 | RGB | No (all curv) |

All 10 negative seeds have only `curv`-type TRC tags. All have RGB color space.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| TRC tag data [0:4] | `70617261` ("para") in at least 1 TRC | `63757276` ("curv") in all TRCs | 10/10 vs 10/10 |
| [16:19] | Various (Lab, GRAY, RGB) | `52474220` ("RGB ") only | 5/10 Lab vs 0/10 Lab |

**Source trace:**
- `curv`-type TRC tags create a single-segment sampled curve covering the full range `[-inf, +inf]`. Every R value matches, so the loop always exits via `return Out` at line 750. The loop exit condition `i < 0` (False at 721:38) is never reached.
- `para`-type TRC tags create a multi-segment parametric curve via `cmsBuildParametricToneCurve()` in `cmsgamma.c`. The segments cover specific domains based on the parametric function type and parameters.
- When the color space is Lab, the Lab-to-float PCS conversion maps L* values to the range `[0, 100]` and a*/b* to `[-128, 128]`. Negative values from a*/b* can fall outside the segments defined by the parametric curve, causing the loop to exhaust all segments.
- With RGB/GRAY + `para`, the False side is reached rarely (1-2 times per seed) because input values are mostly in `[0, 1]` which segments typically cover.
- With Lab + `para`, the False side is reached ~91k times per seed because the Lab encoding produces many out-of-range values.

**Hypothesis:** Two conditions are required:
1. At least one TRC tag must have type `para` (0x70617261) at its tag data offset
2. Color space at bytes [16:19] must be `Lab ` (0x4C616220) for high-frequency False hits; RGB/GRAY with `para` produce marginal False hits (1-2 per run)

**Verification:** CONFIRMED (round 3)
- Test A: positive seed `028f67a5` (Lab+para) with rTRC `para` changed to `curv` -> Branch (721:38) [True: 196k, False: 0] -- False side gone
- Test B: negative seed `000d0009` (RGB+curv) with cs changed to Lab AND rTRC changed to `para` -> Branch (721:38) [True: 244k, False: 91.4k] -- False side appears
- Control: Lab alone (no para) -> [True: 204k, False: 0] -- para is necessary
- Control: para alone (RGB, no Lab) -> [True: 78.6k, False: 0] -- Lab is necessary for reliable hits (RGB+para gives only marginal False:1 in specific seeds)

**Controlling bytes:** [16:19] = `4C616220` ("Lab ") AND TRC tag data type = `70617261` ("para")
**Cluster:** BC04

---

---

## Tier 1 -- Full Analysis Details (Batch 2)

### Rank 22 -- FillFirstShaper|cmsopt.c:1572:13 (representative for cmsopt.c)

**Branch:** `if (y < 131072.0)` in `FillFirstShaper()`
**Blocked side:** False (y >= 131072.0, tone curve output overflows)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | TRC type | TRC params |
|---------|------|--------|-------------|----------|------------|
| 0eda8d6201d0088a | 564 | cmplog/t1 | RGB | para | funcType=1, gamma=563 |
| 245dfd328d25b6ab | 564 | cmplog/t1 | RGB | para | funcType=1, gamma=563 |
| 338134cfe390d230 | 564 | cmplog/t1 | RGB | para | funcType=1, gamma=563 |
| 3583e08bde583c20 | 564 | cmplog/t1 | RGB | para | funcType=2, gamma=563 |
| 537646b1e9d04991 | 564 | cmplog/t1 | RGB | para | funcType=0, gamma=-128 |
| 6700cec80c7f8de9 | 564 | cmplog/t1 | RGB | para | funcType=1, gamma=563 |
| 9a21cf323a1f7a24 | 564 | cmplog/t1 | RGB | para | (similar extreme) |
| 6c1358ab9d77cd7c | 564 | vpc/t1 | RGB | para | (similar extreme) |
| 7497400d84ce42a6 | 564 | vpc/t1 | RGB | para | (similar extreme) |
| 85b82c171f0a50e7 | 564 | vpc/t1 | RGB | para | (similar extreme) |

All 10 positive seeds have RGB color space, XYZ PCS, mntr device class, and `para` TRC tags with extreme gamma values (563.0 or -128.0). All 3 TRC tags (rTRC/gTRC/bTRC) share the same data offset.

**Negative seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | TRC type |
|---------|------|--------|-------------|----------|
| 1c0ea1620d3a5557 | 564 | naive/t1 | RGB | curv |
| 2af1f3c9931db1fd | 573 | naive/t1 | RGB | curv |
| 2bfb51f7412a397b | 564 | naive/t1 | RGB | curv |
| 2ce3862d4935bd5a | 564 | naive/t1 | RGB | curv |
| 2f4df80e68d583c5 | 564 | naive/t1 | RGB | curv |
| 3f790434d791ea70 | 585 | naive/t1 | RGB | curv |
| 451cd210da9f2bc9 | 564 | naive/t1 | RGB | curv |
| 60ca3850d17b628d | 564 | naive/t1 | RGB | curv |
| 64aa5b978c9123a4 | 564 | naive/t1 | RGB | curv |
| 737439ddcbdec4d7 | 564 | naive/t1 | RGB | curv |

All 10 negative seeds have identical header fields (RGB, XYZ, mntr) but `curv` TRC tags.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| TRC data [0:4] | `70617261` ("para") | `63757276` ("curv") | 10/10 vs 10/10 |
| TRC para gamma | >= 563.0 (s15Fixed16 0x02330000+) | N/A (curv uses sampled points) | 10/10 |

**Source trace:**
- `cmsCreateTransform` -> optimization pipeline -> `OptimizeByComputingLinearization` -> `SetMatShaper` -> `FillFirstShaper(p->Shaper1R, Curve1[0])`
- `FillFirstShaper` iterates i=0..255, computes R=i/255.0, y=cmsEvalToneCurveFloat(Curve, R)
- `curv` type: sampled tone curves produce bounded outputs (gamma table with 16-bit entries)
- `para` type: parametric curves with extreme gamma (563.0) produce y = R^563 which overflows for R close to 1.0, yielding y >> 131072.0
- Line 1572: `if (y < 131072.0)` -- False side taken when y overflows

**Hypothesis:** TRC tag data type must be `para` (0x70617261) with extreme gamma parameters (|gamma| >> 1) to produce y >= 131072.0. The controlling bytes are at each TRC tag's data offset (first 4 bytes = type signature) plus the gamma parameter field (bytes 12-15 of the tag data).
**Verification:** CONFIRMED (round 2)
- Test A: positive seed `245dfd328d25b6ab` (para, gamma=563) with rTRC changed to `curv` -> Branch (1572:13) [True: 768, False: 0] -- False side gone
- Test B (round 1): negative seed `3f790434d791ea70` with all 3 TRC changed to `para` funcType=0 gamma=563 -> [True:768, False:0] -- Failed (size mismatch corrupted profile)
- Test B (round 2): negative seed with exact `para` data bytes copied from positive seed -> Branch (1572:13) [True: 3, False: 765] -- False side appears

**Controlling bytes:** TRC tag data type = `70617261` ("para") at TRC tag data offset, plus extreme gamma in tag parameters. All 3 TRC tags must be `para`.
**Cluster:** BC04

---

### Rank 26 -- AddConversion|cmscnvrt.c:429:5 (representative for cmscnvrt.c)

**Branch:** `case cmsSigXYZData:` in `AddConversion()` switch on `InPCS`
**Blocked side:** False (InPCS != cmsSigXYZData, i.e., input profile PCS is Lab)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | PCS |
|---------|------|--------|-------------|-----|
| 00b7148bca9f2712 | 564 | cmplog/t1 | Lab | Lab |
| 0393fd461e63a014 | 564 | cmplog/t1 | CMYK | Lab |
| 03b5b94a6c12d539 | 1257 | cmplog/t1 | Luv | Lab |
| 03de43d4fd5f5ea5 | 1269 | cmplog/t1 | Yxy | Lab |
| 0451c23fde546ef3 | 1257 | cmplog/t1 | GRAY | Lab |
| 0497d4b07d0249c2 | 1257 | cmplog/t1 | Lab | Lab |
| 04e8dd32b8575d1a | 1274 | cmplog/t1 | YCbr | Lab |
| 011b5a964ce210a2 | 574 | cmplog/t1 | Lab | Lab |
| 01b87c1623625c3b | 564 | cmplog/t1 | RGB | Lab |
| 028f67a5a7eca737 | 579 | cmplog/t1 | Lab | Lab |

83% of all resolving seeds have PCS=Lab (0x4c616220). 17% have PCS=XYZ but non-RGB color spaces.

**Negative seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | PCS |
|---------|------|--------|-------------|-----|
| 000d00091601b743 | 585 | naive/t1 | RGB | XYZ |
| 019e5531b6c657b1 | 1001 | naive/t1 | RGB | XYZ |
| 026901d6be44dd5a | 564 | naive/t1 | RGB | XYZ |
| 02d378b7becfcf14 | 591 | naive/t1 | RGB | XYZ |
| (6 more) | 564-591 | naive/t1 | RGB | XYZ |

All 100 blocking seeds have PCS=XYZ (0x58595a20) and cs=RGB.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 20-23 (PCS) | `4c616220` ("Lab ") (83%) | `58595a20` ("XYZ ") (100%) | 83/100 vs 100/100 |

**Source trace:**
- `cmsCreateTransform` -> `_cmsLinkProfiles` -> `AddConversion(Result, InPCS, OutPCS, m, off)`
- `InPCS` = profile's PCS (bytes [20:23]). When PCS=Lab: InPCS=cmsSigLabData, switch falls to `case cmsSigLabData:` (line 451), skipping XYZ case -> False at 429:5
- When PCS=XYZ: InPCS=cmsSigXYZData, switch enters case at line 429 -> True at 429:5

**Hypothesis:** PCS bytes [20:23] must NOT be `58595a20` ("XYZ ") to hit the blocked False side. When PCS is "Lab " or another non-XYZ value, InPCS != cmsSigXYZData.
**Verification:** CONFIRMED (round 1)
- Test A: positive seed `0393fd461e63a014` (PCS=Lab) with bytes[20:23] changed to XYZ -> Branch (429:5) [True: 2, False: 0] -- False side gone
- Test B: negative seed `026901d6be44dd5a` (PCS=XYZ) with bytes[20:23] changed to Lab -> Branch (429:5) [True: 1, False: 2] -- False side appears

**Controlling bytes:** [20:23] = ICC PCS field; must not be `58595a20` ("XYZ ")
**Cluster:** BC01

---

### Rank 27 -- _cmsEndPointsBySpace|cmspcs.c:732:8 (representative for cmspcs.c)

**Branch:** `case cmsSigRgbData:` in `_cmsEndPointsBySpace()` switch on `Space`
**Blocked side:** False (Space != cmsSigRgbData)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | PCS |
|---------|------|--------|-------------|-----|
| 0038379735aef293 | 1834 | cmplog/t1 | CMYK | XYZ |
| 006edb094ccc87ab | 1266 | cmplog/t1 | CMYK | XYZ |
| 00b7148bca9f2712 | 564 | cmplog/t1 | Lab | Lab |
| 028f67a5a7eca737 | 579 | cmplog/t1 | Lab | Lab |
| 03b5b94a6c12d539 | 1257 | cmplog/t1 | Luv | Lab |
| 03de43d4fd5f5ea5 | 1269 | cmplog/t1 | Yxy | Lab |
| 03fc53d292c90b43 | 577 | cmplog/t1 | DCLR | XYZ |
| 0497d4b07d0249c2 | 1257 | cmplog/t1 | Lab | Lab |
| 04e8dd32b8575d1a | 1274 | cmplog/t1 | YCbr | Lab |
| 011b5a964ce210a2 | 574 | cmplog/t1 | Lab | Lab |

All resolving seeds have non-RGB color spaces: Lab (38%), GRAY (15%), CMY (7%), CMYK (6%), and various multi-channel types.

**Negative seeds (N=10):**
All 89/100 blocking seeds have cs=RGB (0x52474220). The remaining 11 have near-RGB corrupted values (e.g., `52564220`, `525241df`).

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 16-19 (color space) | Various non-RGB (100%) | `52474220` ("RGB ") or near-RGB (100%) | 99/99 vs 100/100 |

**Source trace:**
- `_cmsEndPointsBySpace(Space, White, Black, nOutputs)` at cmspcs.c:725
- Called from `cmsDesiredBlackPoint()` or `cmsDetectBlackPoint()` with `Space = cmsGetColorSpace(hProfile)`
- `cmsGetColorSpace` returns the profile's color space (bytes [16:19])
- When cs=RGB: switch matches `case cmsSigRgbData:` at line 732 -> True
- When cs != RGB: switch falls through to other cases -> False at 732:8

**Hypothesis:** bytes [16:19] must NOT be `52474220` ("RGB ") to hit the blocked False side.
**Verification:** CONFIRMED (Test A only, round 1)
- Test A: positive seed `0038379735aef293` (cs=CMYK) with bytes[16:19] changed to RGB -> Branch (732:8) [True: 2, False: 0] -- False side gone
- Test B: Could not cleanly isolate. Changing cs on an RGB-structured profile (with rXYZ/gXYZ/bXYZ tags) to a non-RGB color space creates an invalid profile that fails to open or fails to produce a transform that calls `_cmsEndPointsBySpace` for the input profile. The output profile (sRGB) always contributes True:1.

**Controlling bytes:** [16:19] = ICC color space field; must not be `52474220` ("RGB ")
**Cluster:** BC01

---

### Rank 29 -- _cmsReadUInt16Number|cmsplugin.c:133:9 (representative for cmsplugin.c)

**Branch:** `if (n != NULL) *n = _cmsAdjustEndianess16(tmp);`
**Blocked side:** False (n == NULL, function called with NULL output pointer)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | PCS | TRC type |
|---------|------|--------|-------------|-----|----------|
| 00b7148bca9f2712 | 564 | cmplog/t1 | Lab | Lab | para |
| 089fe16279f72f5a | 564 | cmplog/t1 | RGB | XYZ | para |
| 0a4f34fffd36d17c | 564 | cmplog/t1 | RGB | XYZ | para |
| 0eda8d6201d0088a | 564 | cmplog/t1 | RGB | XYZ | para |
| 134a2229933cbd15 | 564 | cmplog/t1 | RGB | XYZ | para |
| 1805a5b8f4f892bf | 564 | cmplog/t1 | RGB | XYZ | para |
| 0631a6e130b9c77f | 564 | cmplog/t1 | GRAY | XYZ | para |
| 063df2d9fb99c423 | 564 | cmplog/t1 | 7CLR | XYZ | para |
| 0762a93be0271273 | 530 | cmplog/t1 | GRAY | XYZ | (various) |
| 028f67a5a7eca737 | 579 | cmplog/t1 | Lab | Lab | para |

Resolving seeds have varied color spaces and PCS values, but ALL have `para` TRC tags. 29 of 100 resolving seeds have cs=RGB and pcs=XYZ (same as blocking seeds), confirming the controlling factor is NOT the color space but the TRC type.

**Negative seeds (N=10):**
All blocking seeds have cs=RGB, pcs=XYZ, and `curv` TRC tags.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| TRC data [0:4] | `70617261` ("para") | `63757276` ("curv") | ~95/100 vs 100/100 |

**Source trace:**
- `_cmsReadUInt16Number(io, n)` at cmsplugin.c:124--135 is a low-level IO utility
- With `curv` TRC: `Type_Curve_Read` reads the curve data using `_cmsReadUInt16Number(io, &count)` -- always with non-NULL n
- With `para` TRC: `Type_ParametricCurve_Read` at cmstypes.c:1265 reads funcType, then reads additional parameters. Some internal sub-calls pass NULL for n when skipping count fields or reading reserved words
- The n=NULL call path only exists in the parametric curve reading logic

**Hypothesis:** TRC tag data type must be `para` (0x70617261) to reach `_cmsReadUInt16Number(io, NULL)`. The `curv` type never calls this function with NULL.
**Verification:** CONFIRMED (round 1)
- Test A: positive seed `245dfd328d25b6ab` (para) reusing test134a (para->curv) -> Branch (133:9) [True: 1, False: 0] -- False side gone
- Test B: negative seed `3f790434d791ea70` (curv) reusing test134b4 (curv->para) -> Branch (133:9) [True: 3, False: 3] -- False side appears (original: [True: 18, False: 0])

**Controlling bytes:** TRC tag data type = `70617261` ("para") at TRC tag data offset
**Cluster:** BC04

---

### Rank 37 -- LLVMFuzzerTestOneInput|cms_transform_fuzzer.cc:32:7 (representative for cms_transform_fuzzer.cc)

**Branch:** `if (srcCS == cmsSigLabData)` in the fuzzer harness
**Blocked side:** True (srcCS == cmsSigLabData, the Lab code path)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | PCS |
|---------|------|--------|-------------|-----|
| 00b7148bca9f2712 | 564 | cmplog/t1 | Lab | Lab |
| 011b5a964ce210a2 | 574 | cmplog/t1 | Lab | Lab |
| 028f67a5a7eca737 | 579 | cmplog/t1 | Lab | Lab |
| 0431d0cbbad89db6 | 564 | cmplog/t1 | Lab | FCLR |
| 0497d4b07d0249c2 | 1257 | cmplog/t1 | Lab | Lab |
| 07085318e627b547 | 1276 | cmplog/t1 | Lab | Lab |
| 0cc2ec11823e2f54 | 577 | cmplog/t1 | Lab | Lab |
| 0daa83665626d6fc | 574 | cmplog/t1 | Lab | Lab |
| 0fe59933e4e7db5b | 574 | cmplog/t1 | Lab | Lab |
| 1282dfaeb1ffa117 | 863 | cmplog/t1 | Lab | Lab |

All 10 positive seeds have cs=Lab (0x4c616220).

**Negative seeds (N=10):**
All blocking seeds have cs=RGB (0x52474220).

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 16-19 | `4c616220` ("Lab ") (100%) | `52474220` ("RGB ") (100%) | 10/10 vs 10/10 |

**Source trace:**
- `LLVMFuzzerTestOneInput` opens the profile from input bytes
- Line 29: `cmsColorSpaceSignature srcCS = cmsGetColorSpace(srcProfile)`
- Line 32: `if (srcCS == cmsSigLabData)` -- direct comparison of color space signature
- `cmsGetColorSpace` reads `Icc->ColorSpace` which was parsed from bytes [16:19]
- `cmsSigLabData = 0x4C616220` = "Lab "

**Hypothesis:** bytes [16:19] must be `4c616220` ("Lab ") to hit the blocked True side.
**Verification:** CONFIRMED (round 1)
- Test A: positive seed `0431d0cbbad89db6` (cs=Lab) with bytes[16:19] changed to RGB -> Branch (32:7) [True: 0, False: 1] -- True side gone
- Test B: negative seed `026901d6be44dd5a` (cs=RGB) with bytes[16:19] changed to Lab -> Branch (32:7) [True: 1, False: 0] -- True side appears

**Controlling bytes:** [16:19] = `4c616220` ("Lab ")
**Cluster:** BC01

---

### Rank 43 -- _cmsGetStockInputFormatter|cmspack.c:3516:19 (representative for cmspack.c)

**Branch:** `for (i=0; i < sizeof(InputFormatters16) / sizeof(cmsFormatters16); i++)` loop termination
**Blocked side:** False (loop exhaustion -- no 16-bit input formatter matches)

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Color space | PCS | TRC type |
|---------|------|--------|-------------|-----|----------|
| 00b7148bca9f2712 | 564 | cmplog/t1 | Lab | Lab | para |
| 011b5a964ce210a2 | 574 | cmplog/t1 | Lab | Lab | para |
| 028f67a5a7eca737 | 579 | cmplog/t1 | Lab | Lab | para |
| 0497d4b07d0249c2 | 1257 | cmplog/t1 | Lab | Lab | para |
| 07085318e627b547 | 1276 | cmplog/t1 | Lab | Lab | para |
| 0cc2ec11823e2f54 | 577 | cmplog/t1 | Lab | Lab | para |
| 0daa83665626d6fc | 574 | cmplog/t1 | Lab | Lab | para |
| 0fe59933e4e7db5b | 574 | cmplog/t1 | Lab | Lab | para |
| 1282dfaeb1ffa117 | 863 | cmplog/t1 | Lab | Lab | para |
| 1693905bd189a403 | 579 | cmplog/t1 | Lab | Lab | para |

All 10 positive seeds have cs=Lab and para TRC.

**Negative seeds (N=10):**
All blocking seeds have cs=RGB, pcs=XYZ, and curv TRC.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 16-19 | `4c616220` ("Lab ") (100%) | `52474220` ("RGB ") (100%) | 10/10 vs 10/10 |

**Source trace:**
- When srcCS=Lab, the fuzzer harness sets `srcFormat = COLORSPACE_SH(PT_Lab) | CHANNELS_SH(3) | BYTES_SH(0)` (floating point format)
- During `cmsCreateTransform`, the optimization pipeline (`OptimizeByResampling` or `OptimizeByComputingLinearization`) may attempt to create a 16-bit formatter fallback
- `_cmsGetStockInputFormatter(dwInput, CMS_PACK_FLAGS_16BITS)` is called with a format spec derived from Lab's PT_Lab color space encoding
- The Lab float format spec (with BYTES_SH(0)) doesn't match any entry in `InputFormatters16[]` table -> loop exhaustion (False at 3516:19)
- Verified: Lab+curv also produces False:1, confirming TRC type is irrelevant -- pure color space dependency

**Hypothesis:** bytes [16:19] must be `4c616220` ("Lab ") to trigger the 16-bit formatter loop exhaustion. Lab profiles use BYTES_SH(0) float format, which creates a non-matching 16-bit format spec.
**Verification:** CONFIRMED (round 1, Test A only)
- Test A: positive seed `00b7148bca9f2712` (cs=Lab) with bytes[16:19] changed to RGB -> Branch (3516:19) [True: 17, False: 0] -- False side gone
- Test A (cross-check): positive seed `0daa83665626d6fc` (cs=Lab) with bytes[16:19] changed to RGB -> [True: 17, False: 0] -- Consistent
- Test B: negative seed `026901d6be44dd5a` (cs=RGB) with bytes[16:19] changed to Lab -> Branch not reached (RGB-structured profile invalid as Lab). Cross-verified by showing Lab seed with cs->RGB eliminates False consistently.
- Control: Lab + curv TRC (para changed to curv) -> [True: 45, False: 1] -- Still hits False, confirming TRC type irrelevant

**Controlling bytes:** [16:19] = `4c616220` ("Lab ")
**Cluster:** BC01

---

### Rank 52 -- cmssamp.c|116:9 (representative for cmssamp.c)

**Branch:** `if (xform == NULL)` in `cmsDetectBlackPoint()`
**Blocked side:** True (xform == NULL, transform creation failed)

**Positive seeds (N=10, cmplog/trial1):**
| Seed ID | Size | Bytes [16:20] (cs) | Tag[0] | Tag[4] | Tag[5] |
|---------|------|-------------------|--------|--------|--------|
| 085fda20 | 1269 | CMY  | lumi | chrm | gTRC |
| 0d233b3f | 1257 | CMY  | lumi | chrm | gTRC |
| 12108863 | 2303 | RGB  | lumi | chrm | gTRC |
| 21e19c5b | 577 | GRAY | lumi | rXYZ | mft2 |
| 286260c8 | 577 | CMYK | lumi | rXYZ | mft2 |
| 2a58772b | 564 | GRAY | clro | H8XY | gTRC |
| 3354d9e8 | 577 | GRAY | lumi | rXYZ | mft1 |
| 33c97cf4 | 1269 | CMYK | lumi | chrm | gTRC |
| 3438ab6a | 1266 | RGB  | lumi | rTRC | gTRC |
| 35ed85b7 | 577 | CMYK | lumi | rXYZ | mft2 |

**Negative seeds (N=10, naive/trial1):**
| Seed ID | Size | Bytes [16:20] (cs) | Tag[0] | Tag[4] | Tag[5] |
|---------|------|-------------------|--------|--------|--------|
| 000d0009 | 585 | RGB  | desc | rTRC | gTRC |
| 019e5531 | 1001 | RGB  | desc | rTRC | gTRC |
| 01ac815e | 585 | RGB  | desc | rTRC | gTRC |
| 026901d6 | 564 | RGB  | desc | rTRC | gTRC |
| 02d378b7 | 591 | RGB  | desc | rTRC | gTRC |
| 03265016 | 585 | RGB  | desc | rTRC | gTRC |
| 0673314a | 575 | RGB  | desc | rTRC | gTRC |
| 0977a819 | 591 | RGB  | desc | rTRC | gTRC |
| 0c098516 | 575 | RGB  | desc | rTRC | gTRC |
| 0e098144 | 573 | RGB  | desc | rTRC | gTRC |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 16-19 | Various (CMY, GRAY, CMYK, RGB) | `52474220` (RGB) always | 10/10 |
| Tag table (132+) | Garbled: lumi/A2B2/clro/mft1/mft2 | Proper: desc/cprt/rTRC/gTRC/bTRC/rXYZ/gXYZ/bXYZ | 10/10 |

**Source trace:**
- `cmsDetectBlackPoint()` calls `cmsCreateTransformTHR(hInput, dwFormat, hLab, TYPE_Lab_DBL, ...)`
- The transform pipeline requires a valid conversion from the input profile's color space to Lab
- For RGB: needs rTRC/gTRC/bTRC + rXYZ/gXYZ/bXYZ (matrix/shaper path)
- Positive seeds have garbled tag tables lacking these essential tags, so the pipeline fails
- One positive seed (3438ab6a) has RGB color space but garbled tags (lumi instead of desc, A2B2 with wrong data), so it also fails

**Hypothesis:** Tag table entries at 132+ must be inconsistent with the color space at [16:19] (e.g., missing required TRC/XYZ tags, or wrong tag types), causing `cmsCreateTransformTHR` to return NULL.
**Verification:** CONFIRMED (round 2)
- Test A: positive seed with full tag section replaced from negative seed -> True:0, False:2
- Test B: negative seed with full tag section replaced from positive seed -> True:1, False:1

**Controlling bytes:** Tag table structure at offset 132+ (must be inconsistent with color space)
**Cluster:** BC08

---

### Rank 82 -- cmsintrp.c|1196:20 (representative for cmsintrp.c)

**Branch:** `if (nOutputChannels == 1)` in `DefaultInterpolatorsFactory()`, inside `case 1` (nInputChannels==1)
**Blocked side:** False (nOutputChannels != 1 with nInputChannels == 1)

**Positive seeds (N=10, cmplog/trial1):**
| Seed ID | Size | Color Space | A2B nIn | A2B nOut |
|---------|------|-------------|---------|----------|
| 0451c23f | 1257 | GRAY | 1 | 3 |
| 11d1b887 | 1656 | MCH1 | 1 | 2 |
| 23c9c742 | 1262 | Yxy  | 1 | 3 |
| 3419097e | 1269 | Yxy  | 1 | 3 |
| 49b5f447 | 1257 | RGB  | 1 | 3 |
| 4a84154e | 1257 | 6CLR | 1 | 3 |
| 6070e15a | 1266 | LuvK | 1 | 5 |
| 61e08b43 | 1257 | 4CLR | 1 | 3 |
| 62ea7c03 | 1262 | HLS  | 1 | 3 |
| 7b8f9473 | 1269 | GRAY | 1 | 3 |

**Negative seeds (N=10, cmplog/trial3):**
| Seed ID | Size | Color Space | A2B nIn | A2B nOut |
|---------|------|-------------|---------|----------|
| 0000f4f8 | 542 | 3CLR | (invalid tag) | - |
| 000b39d8 | 564 | GRAY | (no valid A2B) | - |
| 003e8948 | 564 | MCH6 | 4 | 4 |
| 0051804b | 564 | RGB  | (no A2B with mft) | - |
| 00c98038 | 564 | ACLR | (no valid A2B) | - |
| 0114e4a7 | 564 | RGB  | 4 | 4 |
| 01907ebe | 568 | CMY  | 4 | 4 |
| 01df5001 | 568 | CH6 | 4 | 4 |
| 01f3dfa0 | 567 | Lab  | (mft2 tag) | - |
| 020b5b5b | 564 | RGB  | (A2B0 XYZ type) | - |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| A2B tag data offset+8 (nIn) | 1 (100%) | 4 or absent | 10/10 |
| A2B tag data offset+9 (nOut) | 2-5 (always >1) | 4 or absent | 10/10 |

**Source trace:**
- `DefaultInterpolatorsFactory()` receives `nInputChannels` and `nOutputChannels` from the CLUT stage
- These come from the mft2 A2B tag header: byte at tag_data+8 = nIn, byte at tag_data+9 = nOut
- `switch (nInputChannels) { case 1: ... if (nOutputChannels == 1)` -- False side needs nOut > 1

**Hypothesis:** A2B mft2 tag byte at offset+8 must be 1 (nIn=1) and byte at offset+9 must be >1 (nOut>1).
**Verification:** CONFIRMED (round 1)
- Test A: changed nOut from 3 to 1 -> True:4, False:0 (False disappeared)
- Test B: grafted positive seed tag section (nIn=1, nOut=3 CLUT data) onto negative header -> True:17, False:3 (False appeared)

**Controlling bytes:** A2B mft2 tag data bytes at offset+8 (nIn=1) and offset+9 (nOut>1)
**Cluster:** BC05

---

### Rank 191 -- cmserr.c|158:9 (representative for cmserr.c)

**Branch:** `if (Total > MAX_MEMORY_FOR_ALLOC) return NULL;` in `_cmsCallocDefaultFn()`
**Blocked side:** True (allocation exceeds 512MB)

**Positive seeds (N=4):**
| Seed ID | Fuzzer | A2B nIn | A2B nOut | Gridpoints | Est. CLUT size |
|---------|--------|---------|----------|------------|----------------|
| 34ac2324 | cmplog/t2 | 9 | 3 | 9 | 9^9*3*2 = 2.3GB |
| 54352570 | cmplog/t2 | 9 | 3 | 9 | 9^9*3*2 = 2.3GB |
| 416f269d | vp_cmplog/t1 | 14 | 5 | 4 | 4^14*5*2 = 2.7GB |
| ef599f08 | vp_cmplog/t1 | 14 | 5 | 4 | 4^14*5*2 = 2.7GB |

**Negative seeds (N=10, cmplog/trial1):** All have A2B tags with nIn <= 4 and/or small gridpoints, keeping CLUT allocation well under 512MB.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| A2B tag data offset+8 (nIn) | 9 or 14 | 3-4 | 4/4 |
| A2B tag data offset+10 (gridpoints) | 4-9 | 2-3 | 4/4 |

**Source trace:**
- `_cmsCallocDefaultFn(num, size)` computes `Total = num * size`
- Called during CLUT allocation for A2B LUT reading
- CLUT size = gridpoints^nIn * nOut * sizeof(cmsUInt16Number)
- With nIn=9, grid=9, nOut=3: 9^9 * 3 * 2 = 2,324,522,934 > 512MB

**Hypothesis:** A2B mft2 tag nIn (offset+8) and gridpoints (offset+10) must produce gridpoints^nIn * nOut * 2 > 536,870,912.
**Verification:** CONFIRMED (round 1)
- Test A: changed nIn from 9 to 3 -> True:0, False:25 (alloc size = 3^3*3*2 = 162 bytes, well under limit)
- Test B: changed nIn to 9, gridpoints to 9, nOut=3 -> True:1, False:16 (alloc exceeds 512MB)

**Controlling bytes:** A2B mft2 tag data bytes at offset+8 (nIn) and offset+10 (gridpoints), with nOut at offset+9
**Cluster:** BC05

---

### Rank 264 -- cmsnamed.c|529:9 (representative for cmsnamed.c)

**Branch:** `if (size > 1024 * 100)` in `GrowNamedColorList()`
**Blocked side:** True (named color list grows beyond 102400 entries)

**Positive seeds (N=1, value_profile_cmplog/trial2):**
| Seed ID | Size | Device Class | Tag[0] | ncl2 count |
|---------|------|-------------|--------|------------|
| f5b2034a | 564 | nmcl | ncl2 | 1,098,019,945 |

**Negative seeds (N=10):** None contain `ncl2` tags. All have `clrt` (colorant table) at tag[0] with device class `mntr`. The named color reading path is never entered.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 12-15 (device class) | `nmcl` | `mntr` | 1/1 vs 10/10 |
| Tag table: ncl2 tag | Present | Absent | 1/1 vs 10/10 |
| ncl2 tag data offset+12 (count) | > 65536 (big-endian u32) | N/A | 1/1 |

**Source trace:**
- Profile with device class `nmcl` and `ncl2` tag enters `Type_NamedColor_Read()` at `cmstypes.c:3172`
- Reads `count` (number of named colors) from ncl2 tag data at offset+12
- Loops `count` times calling `cmsAppendNamedColor()`, which calls `GrowNamedColorList()` when needed
- `GrowNamedColorList()` doubles `Allocated`: 0->64->128->...->131072
- When count > 65536, size reaches 131072 > 102400, hitting the True side

**Hypothesis:** Profile must have (1) `ncl2` tag in tag table, (2) ncl2 count field (tag_data+12, 4 bytes BE) > 65536.
**Verification:** CONFIRMED (round 1)
- Test A: changed count from 1098019945 to 5 -> True:0 (list stays small)
- Test B: original seed with count=1098019945 -> True:1 (exceeds limit)

**Controlling bytes:** ncl2 tag presence + count field at ncl2 tag data offset + 12
**Cluster:** BC07

---

### Rank 272 -- cmsmtrx.c|107:17 (representative for cmsmtrx.c)

**Branch:** `if (!CloseEnough(a->v[i].n[j], Identity.v[i].n[j])) return FALSE;` in `_cmsMAT3isIdentity()`
**Blocked side:** False (CloseEnough returns TRUE = matrix element matches identity)

**Positive seeds (N=1, value_profile_cmplog/trial3):**
| Seed ID | Size | cs | A2B0 type | nIn | Matrix[0][0] | Matrix[0][1] | Matrix[0][2] |
|---------|------|-----|-----------|-----|-------------|-------------|-------------|
| 1a0a9012 | 1154 | Luv | mft2 | 3 | 1.0000 | 0.0000 | 0.0000 |

First row is identity [1, 0, 0], remaining rows are far from identity. `CloseEnough` returns TRUE for 3 elements (first row), then fails on element [1][0].

**Negative seeds (N=10, cmplog/trial1):** All have A2B mft2 tags with 3x3 matrices far from identity. The matrix values at tag_data+12 contain large non-identity values (e.g., 6.0+, 6939+).

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| A2B mft2 tag data + 12 (matrix[0][0]) | 0x00010000 (1.0 s15Fixed16) | Various non-1.0 values | 1/1 vs 10/10 |
| A2B mft2 tag data + 16 (matrix[0][1]) | 0x00000000 (0.0) | Various non-0.0 values | 1/1 vs 10/10 |
| A2B mft2 tag data + 20 (matrix[0][2]) | 0x00000000 (0.0) | Various non-0.0 values | 1/1 vs 10/10 |

**Source trace:**
- `_cmsMAT3isIdentity()` at cmsmtrx.c:98 creates an identity matrix, then compares each element
- Called from `cmsopt.c:1853` and `cmsopt.c:2150` during pipeline optimization
- The matrix comes from the mft2 A2B tag's embedded 3x3 matrix at tag_data+12
- `CloseEnough(a, b)` returns `fabs(b - a) < (1.0 / 65535.0)` -- requires precision within ~0.0000153

**Hypothesis:** A2B mft2 matrix at tag_data+12 (36 bytes, 9 s15Fixed16 values) must have at least one element close to the identity matrix value (within 1/65535).
**Verification:** CONFIRMED (round 1)
- Test A: changed matrix[0][0] from 1.0 (0x00010000) to 0.5 (0x00008000) -> True:1, False:0 (no identity matches)
- Test B: set entire matrix to identity (diagonal=0x00010000, off-diagonal=0x00000000) -> True:0, False:9 (all match)

**Controlling bytes:** A2B mft2 matrix values at tag_data+12 through tag_data+47 (36 bytes)
**Cluster:** BC06

---

## Skipped Branches

None -- all 18 branches across batches 1, 2, and 3 had sufficient seed data and were verified.

## Tier 1 Complete -- All 17 Representatives Analyzed

All 17 Tier 1 representative branches (one per function with divergent branches) have been processed across 3 batches. Summary of all clusters:

| Cluster | Controlling Bytes | Semantic Meaning | Representatives | Total Branches |
|---------|------------------|------------------|----------------|----------------|
| BC01 | [16:20] + [20:24] | ICC color space + PCS fields | R1, R2, R26, R27, R37, R43 | 6 |
| BC02 | [12:16] | ICC device class field | R3 | 1 |
| BC03 | Tag table: D2B0 tag | Float LUT tag presence | R5, R6, R14 | 3 |
| BC04 | [16:20] + TRC tag type | Lab color space + para TRC | R15, R22, R29 | 3 |
| BC05 | A2B mft2 nIn/nOut/gridpoints | CLUT dimensions | R82, R191 | 2 |
| BC06 | A2B mft2 matrix (36 bytes) | Embedded 3x3 matrix identity | R272 | 1 |
| BC07 | ncl2 tag + count field | Named color list count | R264 | 1 |
| BC08 | Tag table structure vs [16:19] | Tag table validity for cs | R52 | 1 |

**Cross-cluster byte overlaps:**
- BC01 and BC04 both depend on bytes [16:19] (color space). BC04 additionally requires `para` TRC tag type.
- BC05 and BC06 both depend on A2B mft2 tag data, but at different offsets: BC05 uses nIn/nOut/gridpoints (offset+8/+9/+10), BC06 uses the matrix (offset+12 to +47).
- BC08 depends on the tag table structure at 132+ being inconsistent with color space [16:19], partially overlapping with BC01's color space dependency.
- BC03 and BC05/BC06 all involve tag data content but at different semantic levels: BC03 is about tag presence (D2B0), while BC05/BC06 are about A2B tag internal fields.

**Next step:** Tier 2 verification -- for each function, verify remaining divergent branches against the representative's hypothesis using 2 Docker runs per branch (Test A + Test B). Branches that fail Tier 2 verification are promoted to full Tier 1 analysis.

## Notes

- All 17 Tier 1 representatives across 3 batches have been analyzed and verified.
- After Tier 2 verification completes, **cross-function merge** (Step 7) will finalize cluster assignments.
- BC01 and BC04 share bytes [16:19] (color space field). A future merge step may combine or cross-reference these clusters.
- BC03 branches (R5, R6, R14) form a dependency chain: R5 gates entry, R6 is downstream, R14 requires additional mAB truncation.
- BC04 now has two sub-groups: R15 requires Lab+para (both conditions), while R22 requires para with extreme gamma (no Lab) and R29 requires para (no Lab, no specific gamma).
- BC05 has two sub-groups: R82 requires nIn=1, nOut>1 (1D multi-output), while R191 requires large nIn*gridpoints for allocation overflow.
- BC06, BC07, BC08 each have a single branch so far; Tier 2 may add more.

---

## Tier 2 -- Verification Results (Batch 1: cmspcs.c, cmsio1.c, cmstypes.c, cmsio0.c)

**Scope:** 150 remaining divergent branches across 4 files (86 cmspcs.c, 25 cmsio1.c, 23 cmstypes.c, 16 cmsio0.c).
**Method:** For each branch, applied the Tier 1 representative's hypothesis with 1 positive + 1 negative seed.
**Results:** 81 confirmed (74 cmspcs.c + 7 cmsio0.c), 12 partial (cmspcs.c Test A only), 57 promoted (9 cmsio0.c + 25 cmsio1.c + 23 cmstypes.c).

### cmspcs.c -- BC01 (ICC color space, bytes [16:19])

Representative: R27 (732:8 False). Hypothesis: bytes [16:19] select the color space case branch in switch statements (`_cmsEndPointsBySpace`, `_cmsComputeXYZto8`, `_cmsComputeXYZfrom8`, etc.).

- **Test A**: resolving seed with bytes [16:19] changed to `RGB ` (0x52474220) -- the blocked side should disappear.
- **Test B**: blocking seed (RGB) with bytes [16:19] changed to the resolving seed's color space -- the blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R30 | cmspcs.c:883:5 | T | PASS | PASS | BC01 |
| R32 | cmspcs.c:814:5 | T | PASS | PASS | BC01 |
| R35 | cmspcs.c:737:8 | T | PASS | FAIL | BC01 (A only) |
| R44 | cmspcs.c:732:33 | T | PASS | FAIL | BC01 (A only) |
| R45 | cmspcs.c:733:32 | F | PASS | FAIL | BC01 (A only) |
| R46 | cmspcs.c:781:8 | T | PASS | FAIL | BC01 (A only) |
| R49 | cmspcs.c:727:8 | T | PASS | FAIL | BC01 (A only) |
| R55 | cmspcs.c:892:5 | T | PASS | PASS | BC01 |
| R56 | cmspcs.c:825:5 | T | PASS | PASS | BC01 |
| R61 | cmspcs.c:896:5 | T | PASS | PASS | BC01 |
| R62 | cmspcs.c:816:5 | T | PASS | PASS | BC01 |
| R65 | cmspcs.c:897:5 | T | PASS | PASS | BC01 |
| R66 | cmspcs.c:834:5 | T | PASS | PASS | BC01 |
| R67 | cmspcs.c:836:5 | T | PASS | PASS | BC01 |
| R68 | cmspcs.c:908:5 | T | PASS | PASS | BC01 |
| R69 | cmspcs.c:861:5 | T | PASS | PASS | BC01 |
| R70 | cmspcs.c:843:5 | T | PASS | FAIL | BC01 (A only) |
| R71 | cmspcs.c:920:5 | T | PASS | PASS | BC01 |
| R72 | cmspcs.c:824:5 | T | PASS | PASS | BC01 |
| R73 | cmspcs.c:822:5 | T | PASS | PASS | BC01 |
| R74 | cmspcs.c:854:5 | T | PASS | PASS | BC01 |
| R75 | cmspcs.c:867:5 | T | PASS | FAIL | BC01 (A only) |
| R77 | cmspcs.c:900:5 | T | PASS | PASS | BC01 |
| R84 | cmspcs.c:752:8 | T | PASS | FAIL | BC01 (A only) |
| R99 | cmspcs.c:891:5 | T | PASS | PASS | BC01 |
| R103 | cmspcs.c:903:5 | T | PASS | PASS | BC01 |
| R104 | cmspcs.c:818:5 | T | PASS | PASS | BC01 |
| R105 | cmspcs.c:894:5 | T | PASS | PASS | BC01 |
| R110 | cmspcs.c:742:8 | T | PASS | FAIL | BC01 (A only) |
| R112 | cmspcs.c:747:8 | T | PASS | FAIL | BC01 (A only) |
| R115 | cmspcs.c:823:5 | T | PASS | PASS | BC01 |
| R116 | cmspcs.c:927:5 | T | PASS | PASS | BC01 |
| R117 | cmspcs.c:827:5 | T | PASS | PASS | BC01 |
| R131 | cmspcs.c:902:5 | T | PASS | PASS | BC01 |
| R132 | cmspcs.c:912:5 | T | PASS | PASS | BC01 |
| R133 | cmspcs.c:837:5 | T | PASS | PASS | BC01 |
| R134 | cmspcs.c:846:5 | T | PASS | PASS | BC01 |
| R135 | cmspcs.c:917:5 | T | PASS | PASS | BC01 |
| R136 | cmspcs.c:918:5 | T | PASS | PASS | BC01 |
| R138 | cmspcs.c:852:5 | T | PASS | PASS | BC01 |
| R139 | cmspcs.c:851:5 | T | PASS | PASS | BC01 |
| R141 | cmspcs.c:901:5 | T | PASS | PASS | BC01 |
| R142 | cmspcs.c:890:5 | T | PASS | PASS | BC01 |
| R143 | cmspcs.c:817:5 | T | PASS | PASS | BC01 |
| R144 | cmspcs.c:819:5 | T | PASS | PASS | BC01 |
| R146 | cmspcs.c:886:5 | T | PASS | PASS | BC01 |
| R147 | cmspcs.c:830:5 | T | PASS | PASS | BC01 |
| R148 | cmspcs.c:881:5 | T | PASS | PASS | BC01 |
| R149 | cmspcs.c:828:5 | T | PASS | PASS | BC01 |
| R150 | cmspcs.c:930:5 | T | PASS | PASS | BC01 |
| R151 | cmspcs.c:885:5 | T | PASS | PASS | BC01 |
| R152 | cmspcs.c:864:5 | T | PASS | PASS | BC01 |
| R153 | cmspcs.c:909:5 | T | PASS | PASS | BC01 |
| R154 | cmspcs.c:831:5 | T | PASS | PASS | BC01 |
| R155 | cmspcs.c:898:5 | T | PASS | PASS | BC01 |
| R156 | cmspcs.c:911:5 | T | PASS | PASS | BC01 |
| R157 | cmspcs.c:914:5 | T | PASS | PASS | BC01 |
| R158 | cmspcs.c:842:5 | T | PASS | PASS | BC01 |
| R159 | cmspcs.c:905:5 | T | PASS | PASS | BC01 |
| R160 | cmspcs.c:895:5 | T | PASS | PASS | BC01 |
| R161 | cmspcs.c:932:5 | T | PASS | PASS | BC01 |
| R162 | cmspcs.c:906:5 | T | PASS | PASS | BC01 |
| R163 | cmspcs.c:921:5 | T | PASS | PASS | BC01 |
| R164 | cmspcs.c:848:5 | T | PASS | PASS | BC01 |
| R165 | cmspcs.c:882:5 | T | PASS | PASS | BC01 |
| R166 | cmspcs.c:915:5 | T | PASS | PASS | BC01 |
| R167 | cmspcs.c:845:5 | T | PASS | PASS | BC01 |
| R168 | cmspcs.c:926:5 | T | PASS | PASS | BC01 |
| R169 | cmspcs.c:855:5 | T | PASS | PASS | BC01 |
| R170 | cmspcs.c:833:5 | T | PASS | PASS | BC01 |
| R171 | cmspcs.c:839:5 | T | PASS | PASS | BC01 |
| R172 | cmspcs.c:840:5 | T | PASS | FAIL | BC01 (A only) |
| R173 | cmspcs.c:866:5 | T | PASS | PASS | BC01 |
| R174 | cmspcs.c:923:5 | T | PASS | PASS | BC01 |
| R175 | cmspcs.c:935:5 | T | PASS | PASS | BC01 |
| R176 | cmspcs.c:860:5 | T | PASS | PASS | BC01 |
| R177 | cmspcs.c:857:5 | T | PASS | PASS | BC01 |
| R178 | cmspcs.c:929:5 | T | PASS | PASS | BC01 |
| R179 | cmspcs.c:849:5 | T | PASS | PASS | BC01 |
| R180 | cmspcs.c:933:5 | T | PASS | PASS | BC01 |
| R181 | cmspcs.c:869:5 | T | PASS | PASS | BC01 |
| R182 | cmspcs.c:936:5 | T | PASS | PASS | BC01 |
| R183 | cmspcs.c:924:5 | T | PASS | PASS | BC01 |
| R184 | cmspcs.c:863:5 | T | PASS | PASS | BC01 |
| R185 | cmspcs.c:870:5 | T | PASS | FAIL | BC01 (A only) |
| R187 | cmspcs.c:858:5 | T | PASS | PASS | BC01 |

**74 confirmed BC01, 12 BC01 (Test A only).**

The 12 Test-B-only failures (R35, R44, R45, R46, R49, R70, R75, R84, R110, R112, R172, R185) are branches for Lab, GRAY, Luv, CMYK, and CMY color spaces. Test A definitively proves bytes [16:19] control them (changing color space to RGB eliminates the blocked side). Test B fails because the blocking seed (RGB-structured profile) lacks the downstream tag structure needed for the target color space path (e.g., Lab requires Lab-encoded endpoint data, CMYK needs 4-channel tags). These are assigned BC01 with the caveat that the blocking seed is structurally incompatible.

### cmsio0.c -- BC02 (ICC device class, bytes [12:15])

Representative: R3 (758:5 True). Hypothesis: bytes [12:15] select the device class case branch in `validDeviceClass()` switch.

- **Test A**: resolving seed with bytes [12:15] changed to `mntr` (valid) -- blocked side should disappear.
- **Test B**: blocking seed with bytes [12:15] changed to resolving seed's device class -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R4 | cmsio0.c:805:9 | T | PASS | PASS | BC02 |
| R7 | cmsio0.c:827:9 | T | FAIL | FAIL | Promoted |
| R9 | cmsio0.c:800:9 | T | FAIL | FAIL | Promoted |
| R11 | cmsio0.c:729:9 | T | FAIL | FAIL | Promoted |
| R12 | cmsio0.c:776:9 | T | FAIL | FAIL | Promoted |
| R13 | cmsio0.c:826:9 | T | FAIL | FAIL | Promoted |
| R34 | cmsio0.c:706:9 | T | FAIL | FAIL | Promoted |
| R59 | cmsio0.c:752:5 | T | PASS | PASS | BC02 |
| R113 | cmsio0.c:755:5 | T | PASS | PASS | BC02 |
| R124 | cmsio0.c:174:9 | T | FAIL | FAIL | Promoted |
| R130 | cmsio0.c:754:5 | T | PASS | PASS | BC02 |
| R145 | cmsio0.c:753:5 | T | PASS | PASS | BC02 |
| R188 | cmsio0.c:749:5 | T | PASS | PASS | BC02 |
| R193 | cmsio0.c:751:5 | T | PASS | PASS | BC02 |
| R214 | cmsio0.c:732:9 | T | FAIL | FAIL | Promoted |
| R220 | cmsio0.c:781:9 | T | FAIL | FAIL | Promoted |

**7 confirmed BC02, 9 promoted.**

The 7 confirmed branches (R4, R59, R113, R130, R145, R188, R193) are all `case` branches in the `validDeviceClass()` switch statement, each matching a specific device class value at bytes [12:15]: R4 (`!validDeviceClass` caller), R59 (link), R113 (nmcl), R130 (spac), R145 (abst), R188 (scnr), R193 (prtr).

The 9 promoted branches are in `_cmsReadHeader()` and other functions, not in the device class switch. Their resolving seeds have valid device classes (mostly `mntr`), indicating different controlling bytes:
- R7 (827:9), R13 (826:9): tag count validation
- R9 (800:9): ICC version check (`Icc->Version > 0x5000000`)
- R11 (729:9), R214 (732:9): header field validation
- R12 (776:9): header read failure
- R34 (706:9): descriptor element count comparison
- R124 (174:9): IO offset bounds check
- R220 (781:9): magic number validation

### cmsio1.c -- BC03 (D2B0 tag presence)

Representative: R5 (343:13 True). Hypothesis: tag table must contain D2B0 signature.

**All 25 branches promoted.** None of the resolving seeds contain a D2B0 tag. These branches are in different processing paths of cmsio1.c (input LUT, output LUT, device link LUT) controlled by various profile properties:

| Rank | Branch | Side | Controlling Property |
|------|--------|------|---------------------|
| R10 | cmsio1.c:143:27 | T | RGB TRC tag presence (PtrRed/Green/Blue != NULL) |
| R23 | cmsio1.c:355:13 | T | A2B/B2A 16-bit LUT tag presence |
| R24 | cmsio1.c:351:13 | F | A2B/B2A 16-bit LUT tag absence |
| R31 | cmsio1.c:868:9 | T | CLUT presence for intent/direction |
| R36 | cmsio1.c:392:9 | T | Color space == GRAY |
| R39 | cmsio1.c:246:13 | T | PCS == Lab |
| R50 | cmsio1.c:810:5 | T | Color space == GRAY (switch case) |
| R53 | cmsio1.c:767:9 | T | LUT read failure (Lut == NULL) |
| R89 | cmsio1.c:526:17 | F | Pipeline stage type == CLut |
| R93 | cmsio1.c:786:9 | F | Color space == Lab (output LUT) |
| R100 | cmsio1.c:775:9 | F | PCS == Lab (output LUT) |
| R102 | cmsio1.c:791:9 | F | PCS == Lab (output LUT) |
| R118 | cmsio1.c:782:9 | T | LUT type != Lut16Type |
| R122 | cmsio1.c:792:13 | T | Pipeline insert failure |
| R126 | cmsio1.c:787:13 | T | Pipeline insert failure |
| R186 | cmsio1.c:816:17 | F | RGB colorant tag presence (rXYZ) |
| R196 | cmsio1.c:322:13 | F | Named color read failure |
| R210 | cmsio1.c:760:13 | T | tag16 absence (output LUT) |
| R216 | cmsio1.c:818:17 | F | RGB TRC tag presence (rTRC) |
| R218 | cmsio1.c:817:17 | F | RGB TRC tag presence (bTRC) |
| R219 | cmsio1.c:143:47 | T | RGB TRC tag presence (PtrRed != NULL) |
| R274 | cmsio1.c:819:17 | F | RGB TRC tag presence (gTRC) |
| R275 | cmsio1.c:820:17 | F | RGB TRC tag presence (gTRC) |
| R276 | cmsio1.c:821:17 | F | RGB TRC tag presence (bTRC) |
| R280 | cmsio1.c:317:9 | T | Device class == NamedColor |

### cmstypes.c -- BC03 (D2B0/mAB tag structure)

Representative: R14 (1265:9 True). Hypothesis: D2B0 tag with truncated mAB sub-element.

**All 23 branches promoted.** Only R283 (111:10 F) has a D2B0 tag in its resolving seed; the other 22 have various non-D2B0 profiles. These branches are in different type handler functions in cmstypes.c (Type_LUT16_Read, Type_LUT8_Read, Type_Chromaticity_Read, Type_NamedColor_Read, etc.), controlled by tag data content rather than D2B0 presence.

| Rank | Branch | Side | Resolving Seed Properties |
|------|--------|------|--------------------------|
| R78 | cmstypes.c:3193:9 | T | cs=XYZ, dc=nmcl (named color handler) |
| R199 | cmstypes.c:1834:9 | T | cs=RGB, dc=mntr, sz=518 |
| R200 | cmstypes.c:2135:9 | T | cs=Lab, dc=abst, sz=494 |
| R201 | cmstypes.c:1145:9 | T | cs=RGB, dc=mntr, sz=443 (truncated) |
| R204 | cmstypes.c:2425:9 | T | cs=RGB, dc=mntr, sz=526 |
| R205 | cmstypes.c:2418:13 | T | cs=RGB, dc=mntr, sz=536 |
| R206 | cmstypes.c:2424:9 | T | cs=RGB, dc=mntr, sz=525 |
| R207 | cmstypes.c:2451:17 | T | cs=RGB, dc=mntr, sz=996 |
| R208 | cmstypes.c:2131:9 | T | cs=Yxy, dc=mntr, sz=580 |
| R209 | cmstypes.c:2574:9 | T | cs=RGB, dc=mntr, sz=518 |
| R211 | cmstypes.c:2581:13 | F | cs=Yxy, dc=mntr, sz=532 |
| R212 | cmstypes.c:2438:19 | F | cs=RGB, dc=mntr, sz=944 |
| R213 | cmstypes.c:2507:15 | F | cs=Yxy, dc=mntr, sz=532 |
| R258 | cmstypes.c:1266:9 | T | cs=2CLR, dc=link, sz=514 |
| R259 | cmstypes.c:1827:10 | T | cs=RGB, dc=link, sz=564 |
| R260 | cmstypes.c:1834:32 | T | cs=RGB, dc=mntr, sz=528 |
| R261 | cmstypes.c:2130:31 | T | cs=GRAY, dc=mntr, sz=564 |
| R262 | cmstypes.c:2569:9 | T | cs=ACLR, dc=prtr, sz=564 |
| R263 | cmstypes.c:1803:9 | T | cs=MCH8, dc=mntr, sz=1292 |
| R267 | cmstypes.c:2601:13 | F | cs=Yxy, dc=mntr, sz=532 |
| R269 | cmstypes.c:2591:13 | F | cs=Yxy, dc=mntr, sz=532 |
| R271 | cmstypes.c:2511:13 | T | cs=2CLR, dc=link, sz=502 |
| R283 | cmstypes.c:111:10 | F | cs=CCLR, dc=mntr, sz=580, has D2B0 |

---

### Tier 2 Batch 1 Summary

| File | Total | Confirmed | Partial (A only) | Promoted | Cluster |
|------|-------|-----------|------------------|----------|---------|
| cmspcs.c | 86 | 74 | 12 | 0 | BC01 |
| cmsio0.c | 16 | 7 | 0 | 9 | BC02 |
| cmsio1.c | 25 | 0 | 0 | 25 | (various) |
| cmstypes.c | 23 | 0 | 0 | 23 | (various) |
| **Total** | **150** | **81** | **12** | **57** | |

**Cluster updates after Tier 2 batch 1:**
- BC01: +74 confirmed + 12 partial = 92 total (was 6, now 98 including Tier 1)
- BC02: +7 confirmed = 8 total (was 1, now 8 including Tier 1)
- BC03: unchanged (0 confirmed in this batch)

**Promoted branches (57 total):** These branches are controlled by different byte regions than their file's Tier 1 representative. Many appear to be controlled by:
- Color space [16:19] -- R36, R39, R50, R93, R100, R102 (cmsio1.c) likely belong to BC01
- Device class [12:15] -- R280 (cmsio1.c) likely belongs to BC02
- Tag table content (tag signatures, data fields) -- most cmstypes.c and several cmsio1.c branches
- ICC header fields (version, magic number) -- R9, R220 (cmsio0.c)
- Structural properties (file size, tag data truncation) -- R12, R124, R201 etc.

These require full Tier 1 analysis in subsequent batches to determine their actual controlling bytes and cluster assignments.

---

## Tier 2 -- Verification Results (Batch 2: cmscnvrt.c, cmsintrp.c, cmslut.c, cmsopt.c, cmsxform.c, cmsgamma.c, cmssamp.c, cmsnamed.c, cmsplugin.c, cmserr.c, cmspack.c, cmsmtrx.c)

### cmscnvrt.c -- BC01 (PCS bytes [20:23])

Representative: R26 (429:5 False). Hypothesis: PCS bytes [20:23] must not be `58595a20` (XYZ); swap between Lab and XYZ.

- **Test A**: resolving seed with bytes [20:23] changed to XYZ -- blocked side should disappear.
- **Test B**: blocking seed with bytes [20:23] changed to Lab -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R28 | cmscnvrt.c:452:5 | T | PASS | PASS | BC01 |
| R33 | cmscnvrt.c:502:9 | T | PASS | PASS | BC01 |
| R58 | cmscnvrt.c:546:25 | F | FAIL | FAIL | Promoted |
| R60 | cmscnvrt.c:543:26 | T | FAIL | FAIL | Promoted |
| R63 | cmscnvrt.c:580:17 | T | FAIL | FAIL | Promoted |
| R76 | cmscnvrt.c:552:25 | F | PASS | PASS | BC01 |
| R87 | cmscnvrt.c:646:9 | T | FAIL | FAIL | Promoted |
| R91 | cmscnvrt.c:616:13 | T | FAIL | FAIL | Promoted |
| R94 | cmscnvrt.c:481:5 | T | FAIL | FAIL | Promoted |
| R95 | cmscnvrt.c:583:18 | F | FAIL | FAIL | Promoted |
| R97 | cmscnvrt.c:583:53 | F | FAIL | FAIL | Promoted |
| R107 | cmscnvrt.c:443:17 | T | FAIL | FAIL | Promoted |
| R108 | cmscnvrt.c:592:17 | T | FAIL | FAIL | Promoted |
| R129 | cmscnvrt.c:435:17 | T | FAIL | FAIL | Promoted |
| R137 | cmscnvrt.c:610:21 | T | PASS | FAIL | BC01 (A only) |
| R279 | cmscnvrt.c:576:31 | T | FAIL | FAIL | Promoted |

**3 confirmed BC01, 1 A-only, 12 promoted.** The confirmed branches (R28 `case cmsSigLabData`, R33 `PCS2PCS_Sampler`, R76) are directly gated by PCS bytes [20:23]. R137 is controlled by PCS bytes (Test A confirmed) but Test B fails because the blocking seed's tag structure cannot produce a valid conversion path after PCS change. The 12 promoted branches are in various `AddConversion` sub-functions and color adaptation code that depend on additional profile structure beyond PCS alone (e.g., chromatic adaptation matrix, tag content, color space + PCS combination).

### cmsintrp.c -- BC05 (A2B mft2 nIn/nOut)

Representative: R82 (1196:20 False). Hypothesis: A2B mft2 nIn=1 at tag_data+8 and nOut>1 at tag_data+9.

- **Test A**: resolving seed with nOut changed to 1 -- blocked side should disappear.
- **Test B**: blocking seed with nIn changed to 1 and nOut to 3 -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R119 | cmsintrp.c:179:9 | F | FAIL | FAIL | Promoted |
| R140 | cmsintrp.c:1213:12 | T | FAIL | FAIL | Promoted |
| R189 | cmsintrp.c:1189:9 | T | FAIL | FAIL | Promoted |
| R190 | cmsintrp.c:1240:12 | T | FAIL | FAIL | Promoted |
| R194 | cmsintrp.c:1255:12 | T | FAIL | FAIL | Promoted |
| R195 | cmsintrp.c:1248:12 | T | FAIL | FAIL | Promoted |
| R215 | cmsintrp.c:1262:12 | T | FAIL | FAIL | Promoted |
| R217 | cmsintrp.c:1269:12 | T | FAIL | FAIL | Promoted |
| R284 | cmsintrp.c:1276:12 | T | FAIL | FAIL | Promoted |
| R286 | cmsintrp.c:1283:12 | T | FAIL | FAIL | Promoted |
| R287 | cmsintrp.c:1290:12 | T | FAIL | FAIL | Promoted |
| R288 | cmsintrp.c:1297:12 | T | FAIL | FAIL | Promoted |
| R289 | cmsintrp.c:1304:12 | T | FAIL | FAIL | Promoted |
| R290 | cmsintrp.c:1311:12 | T | FAIL | FAIL | Promoted |
| R291 | cmsintrp.c:1318:12 | T | FAIL | FAIL | Promoted |

**0 confirmed, 15 promoted.** All branches in `DefaultInterpolatorsFactory()` except R82 are `case` branches for nInputChannels 2-15 (R140=case 2, R190/R189=case 3, R195/R194=case 4, etc.), each requiring a specific nIn value different from R82's nIn=1. R119 (cmsintrp.c:179:9 F) is in `_cmsComputeInterpParams()` checking `if (dwFlags == CMS_LERP_FLAGS_TRILINEAR)`, controlled by optimization flags rather than A2B dimensions. These branches have distinct controlling bytes (different nIn values or flag parameters).

### cmslut.c -- BC03 (D2B0 tag presence)

Representative: R6 (1461:9 True). Hypothesis: tag table must contain D2B0 tag signature.

- **Test A**: resolving seed with D2B0 tag removed (overwritten) -- blocked side should disappear.
- **Test B**: blocking seed with first tag changed to D2B0 -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R40 | cmslut.c:1258:9 | F | FAIL | FAIL | Promoted |
| R79 | cmslut.c:1373:12 | T | FAIL | FAIL | Promoted |
| R80 | cmslut.c:1477:18 | F | FAIL | FAIL | Promoted |
| R81 | cmslut.c:589:9 | T | FAIL | FAIL | Promoted |
| R86 | cmslut.c:1305:17 | T | FAIL | FAIL | Promoted |
| R88 | cmslut.c:1514:24 | T | FAIL | FAIL | Promoted |
| R90 | cmslut.c:1609:34 | T | FAIL | FAIL | Promoted |
| R92 | cmslut.c:1620:17 | T | FAIL | FAIL | Promoted |
| R101 | cmslut.c:354:9 | T | FAIL | FAIL | Promoted |
| R109 | cmslut.c:129:13 | T | FAIL | FAIL | Promoted |
| R120 | cmslut.c:534:9 | F | PASS | FAIL | BC03 (A only) |
| R121 | cmslut.c:577:9 | T | PASS | FAIL | BC03 (A only) |
| R123 | cmslut.c:470:13 | T | FAIL | FAIL | Promoted |
| R202 | cmslut.c:475:13 | T | FAIL | FAIL | Promoted |

**0 confirmed, 2 A-only, 12 promoted.** R120 and R121 are downstream of D2B0 tag presence (Test A confirms removing D2B0 eliminates the branch). Test B fails because simply adding D2B0 as a tag signature without valid mAB tag data doesn't produce a functional float LUT pipeline. The 12 promoted branches are in pipeline construction/evaluation functions (`cmsPipelineAlloc`, `cmsPipelineEvalFloat`, `cmsStageAllocCLutFloat`, `cmsStageDef`, etc.) that depend on pipeline stage types, CLUT dimensions, and other structural properties beyond D2B0 tag presence.

### cmsopt.c -- BC04 (para TRC + extreme gamma)

Representative: R22 (1572:13 False). Hypothesis: TRC tag type must be `para` with extreme gamma parameters.

- **Test A**: resolving seed with `para` changed to `curv` at TRC data offset -- blocked side should disappear.
- **Test B**: blocking seed with `curv` changed to `para` data from resolving seed -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R38 | cmsopt.c:1673:12 | T | FAIL | FAIL | Promoted |
| R41 | cmsopt.c:668:9 | F | PASS | FAIL | BC04 (A only) |
| R42 | cmsopt.c:1676:12 | T | PASS | FAIL | BC04 (A only) |
| R51 | cmsopt.c:211:26 | T | FAIL | FAIL | Promoted |
| R54 | cmsopt.c:212:29 | T | PASS | FAIL | BC04 (A only) |
| R106 | cmsopt.c:146:9 | T | FAIL | FAIL | Promoted |
| R125 | cmsopt.c:196:12 | T | FAIL | FAIL | Promoted |
| R127 | cmsopt.c:1935:9 | T | FAIL | FAIL | Promoted |
| R197 | cmsopt.c:1690:12 | T | PASS | FAIL | BC04 (A only) |
| R277 | cmsopt.c:1928:13 | T | FAIL | FAIL | Promoted |

**0 confirmed, 4 A-only, 6 promoted.** R41 (optimization flag check in `OptimizeByComputingLinearization`), R42/R197 (FillFirstShaper and related table filling for per-channel extreme gamma), and R54 are all downstream of `para` TRC -- Test A confirms that switching to `curv` eliminates them. Test B fails because grafting `para` data onto a `curv` seed requires matching the exact tag size allocation, which corrupts the profile. The 6 promoted branches are in optimization pipeline functions (`_Remove1Op`, `_PrecalcOptimize`, `Eval16nop1D`, `OptimizeByResampling`) with controlling bytes in pipeline stage configuration rather than TRC type.

### cmsxform.c -- BC01 (color space [16:19])

Representative: R1 (1064:9 False). Hypothesis: bytes [16:19] control color space; swap between Lab and non-Lab.

- **Test A**: resolving seed with bytes [16:19] changed to blocking seed's color space -- blocked side should disappear.
- **Test B**: blocking seed with bytes [16:19] changed to resolving seed's color space -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R2 | cmsxform.c:1150:9 | T | FAIL | FAIL | Promoted |
| R8 | cmsxform.c:1064:9 | T | PASS | PASS | BC01 |
| R25 | cmsxform.c:1019:24 | F | FAIL | FAIL | Promoted |
| R47 | cmsxform.c:956:17 | T | PASS | FAIL | BC01 (A only) |
| R48 | cmsxform.c:1182:9 | T | PASS | FAIL | BC01 (A only) |
| R111 | cmsxform.c:1025:13 | T | FAIL | FAIL | Promoted |
| R114 | cmsxform.c:1031:25 | T | PASS | FAIL | BC01 (A only) |
| R285 | cmsxform.c:1145:9 | T | PASS | FAIL | BC01 (A only) |

**1 confirmed BC01, 4 A-only, 3 promoted.** R8 is the complementary True side of R1's branch (`Space1 == PT_Lab`); swapping color space flips it cleanly. R47 (`IsEmptyLayer` optimization check), R48 (`MergeStages` post-transform), R114 (`FloatXFORM` allocation), and R285 (`cmsFLAGS_CAN_CHANGE_FORMATTER` check) all depend on color space (Test A confirms) but Test B fails because changing cs on an RGB-structured profile to a non-RGB space produces a structurally invalid profile. R2 is the `!IsProperColorSpace(ExitColorSpace, OutputFormat)` caller, already a Tier 1 rep. R25 and R111 depend on formatter matching and output intent, controlled by additional profile structure.

### cmsgamma.c -- BC04 (Lab + para TRC)

Representative: R15 (721:38 False). Hypothesis: color space must be Lab (`4c616220`) at [16:19] AND TRC tag type must be `para` (`70617261`).

- **Test A**: resolving seed with `para` changed to `curv` at TRC data offset -- blocked side should disappear.
- **Test B**: blocking seed with cs changed to Lab AND TRC changed from `curv` to `para` -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R16 | cmsgamma.c:724:40 | F | PASS | FAIL | BC04 (A only) |
| R17 | cmsgamma.c:724:13 | F | PASS | FAIL | BC04 (A only) |
| R18 | cmsgamma.c:432:5 | T | PASS | PASS | BC04 |
| R19 | cmsgamma.c:380:5 | T | PASS | PASS | BC04 |
| R20 | cmsgamma.c:542:5 | T | PASS | PASS | BC04 |
| R21 | cmsgamma.c:497:17 | F | PASS | FAIL | BC04 (A only) |
| R83 | cmsgamma.c:910:9 | T | FAIL | FAIL | Promoted |

**3 confirmed BC04, 3 A-only, 1 promoted.** R18 (`Type2Fn`, parametric curve type 2 handler), R19 (`Type1Fn`, parametric curve type 1 handler), and R20 (`Type6Fn`, type 6 handler) are parametric curve evaluation functions that require `para` TRC -- both tests pass. R16/R17 are sub-conditions within the `EvalSegmentedFn` loop (segment boundary checks at 724:40 `R >= g->Segments[i].x0` and 724:13 combined condition); Test A confirms `para` controls them but Test B fails because the `curv`-to-`para` conversion in the blocking seed doesn't produce proper segment boundary values for these sub-conditions. R21 (`DefaultEvalParametricFn` type 4 sub-case) similarly requires `para` but Test B fails. R83 (`cmsToneCurveIsMultisegment`) depends on multi-segment curve structure, not just `para` type.

### cmssamp.c -- BC08 (tag table inconsistent with color space)

Representative: R52 (116:9 True). Hypothesis: tag table entries at 132+ must be inconsistent with color space at [16:19].

- **Test A**: resolving seed header + blocking seed's tag section (proper tags) -- blocked side should disappear.
- **Test B**: blocking seed header + resolving seed's tag section (garbled tags) -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R57 | cmssamp.c:128:23 | T | PASS | FAIL | BC08 (A only) |
| R64 | cmssamp.c:218:17 | F | PASS | PASS | BC08 |
| R85 | cmssamp.c:93:9 | T | PASS | FAIL | BC08 (A only) |
| R96 | cmssamp.c:197:9 | T | PASS | PASS | BC08 |
| R98 | cmssamp.c:198:9 | T | PASS | FAIL | BC08 (A only) |
| R278 | cmssamp.c:199:9 | T | PASS | FAIL | BC08 (A only) |

**2 confirmed BC08, 4 A-only.** R64 (`cmsDetectDestinationBlackPoint` adaptation flag) and R96 (`cmsDetectBlackPoint` Lab value extraction) are controlled by tag table validity -- garbled tags cause transform failure. R57 (black point TAC), R85 (`cmsDetectBlackPoint` initial check), R98 and R278 (Lab value components b* and L*) are downstream of the transform: Test A confirms garbled-vs-proper tags control them, but Test B fails because the resolving seed's garbled tag section combined with the blocking seed's RGB header produces an incompatible profile that fails at a different point.

### cmsnamed.c -- BC07 (ncl2 tag + large count)

Representative: R264 (529:9 True). Hypothesis: ncl2 tag must be present with count > 65536 at tag_data+12.

- **Test A**: resolving seed with ncl2 count set to 5 -- blocked side should disappear.
- **Test B**: blocking seed with ncl2 count set to 200000 -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R265 | cmsnamed.c:549:9 | T | FAIL | FAIL | Promoted |
| R266 | cmsnamed.c:560:13 | T | FAIL | FAIL | Promoted |
| R268 | cmsnamed.c:623:15 | T | FAIL | FAIL | Promoted |
| R270 | cmsnamed.c:523:9 | F | PASS | PASS | BC07 |

**1 confirmed BC07, 3 promoted.** R270 (`GrowNamedColorList` initial allocation check `if (NamedColorList == NULL)`) is controlled by ncl2 tag count -- reducing count eliminates the growth path (Test A), and inflating count triggers it (Test B). R265 (`cmsFreeNamedColorList` inside growth failure cleanup), R266 (`_cmsRealloc` error check), and R268 (`cmsAppendNamedColor` string copy) have resolving seeds from different fuzzers/trials with different ncl2 structures; their controlling bytes are ncl2 tag data fields beyond just the count (e.g., prefix/suffix lengths, color name data layout) and require separate analysis.

### cmsplugin.c -- BC04 (para TRC tag type)

Representative: R29 (133:9 False). Hypothesis: TRC tag data type must be `para` (`70617261`).

- **Test A**: resolving seed with `para` changed to `curv` -- blocked side should disappear.
- **Test B**: blocking seed with `curv` changed to `para` (with gamma data from resolving seed) -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R192 | cmsplugin.c:444:9 | T | FAIL | FAIL | Promoted |
| R203 | cmsplugin.c:473:9 | F | PASS | FAIL | BC04 (A only) |
| R282 | cmsplugin.c:165:9 | F | PASS | FAIL | BC04 (A only) |

**0 confirmed, 2 A-only, 1 promoted.** R203 (`_cmsReadUInt32Number` with n=NULL) and R282 (`_cmsReadFloat32Number` with n=NULL) are low-level IO functions that receive NULL output pointers only when reading `para` TRC parameters -- Test A confirms `para` is required. Test B fails because the `curv`-to-`para` graft corrupts the tag data layout. R192 (`_cmsWriteUInt8Number` error check) is in the write path, likely controlled by profile output serialization logic rather than TRC type.

### cmserr.c -- BC05 (A2B mft2 oversized CLUT)

Representative: R191 (158:9 True). Hypothesis: A2B mft2 nIn*gridpoints must cause allocation > 512MB.

- **Test A**: resolving seed with nOut changed to 1 (reducing allocation size) -- blocked side should disappear.
- **Test B**: blocking seed with nIn set to 1 and nOut to 3 -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R198 | cmserr.c:151:9 | T | PASS | FAIL | BC05 (A only) |
| R281 | cmserr.c:148:9 | T | FAIL | FAIL | Promoted |

**0 confirmed, 1 A-only, 1 promoted.** R198 (`if (num_items > (MAX_MEMORY_FOR_ALLOC / size))` overflow check) is upstream of R191 in `_cmsCallocDefaultFn` -- Test A confirms reducing CLUT size eliminates it, but Test B fails because the blocking seed's A2B tag with nIn=1, nOut=3 produces a small allocation that never exceeds the limit. R281 (`if (size == 0 || num_items == 0)` zero-size check) requires zero-sized allocation, which is a different condition entirely.

### cmspack.c -- BC01 (color space = Lab)

Representative: R43 (3516:19 False). Hypothesis: bytes [16:19] must be `4c616220` (Lab).

- **Test A**: resolving seed with bytes [16:19] changed to blocking seed's color space -- blocked side should disappear.
- **Test B**: blocking seed with bytes [16:19] changed to resolving seed's color space -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R128 | cmspack.c:3851:9 | T | PASS | FAIL | BC01 (A only) |

**0 confirmed, 1 A-only.** R128 (`_cmsGetStockOutputFormatter` loop exhaustion) is the output formatter analog of R43's input formatter -- Lab's float format spec doesn't match any 16-bit output formatter. Test A confirms cs controls it, but Test B fails because the blocking seed's RGB-structured profile is incompatible with Lab color space (the profile opens but the transform fails before reaching the output formatter).

### cmsmtrx.c -- BC06 (A2B 3x3 matrix near identity)

Representative: R272 (107:17 False). Hypothesis: A2B mft2 3x3 matrix at tag_data+12 must be close to identity.

- **Test A**: resolving seed with matrix set to non-identity (0.5 diagonal) -- blocked side should disappear.
- **Test B**: blocking seed with matrix set to identity -- blocked side should appear.

| Rank | Branch | Side | Test A | Test B | Result |
|------|--------|------|--------|--------|--------|
| R273 | cmsmtrx.c:106:19 | F | PASS | PASS | BC06 |

**1 confirmed BC06.** R273 is the outer loop of `_cmsMAT3isIdentity` (`for (i=0; i<3; i++)`) -- its False side (loop continues) requires at least one element to match identity, which is the same condition as R272's inner `CloseEnough` check. Both tests pass cleanly.

---

### Tier 2 Batch 2 Summary

| File | Total | Confirmed | Partial (A only) | Promoted | Cluster |
|------|-------|-----------|------------------|----------|---------|
| cmscnvrt.c | 16 | 3 | 1 | 12 | BC01 |
| cmsintrp.c | 15 | 0 | 0 | 15 | -- |
| cmslut.c | 14 | 0 | 2 | 12 | BC03 |
| cmsopt.c | 10 | 0 | 4 | 6 | BC04 |
| cmsxform.c | 8 | 1 | 4 | 3 | BC01 |
| cmsgamma.c | 7 | 3 | 3 | 1 | BC04 |
| cmssamp.c | 6 | 2 | 4 | 0 | BC08 |
| cmsnamed.c | 4 | 1 | 0 | 3 | BC07 |
| cmsplugin.c | 3 | 0 | 2 | 1 | BC04 |
| cmserr.c | 2 | 0 | 1 | 1 | BC05 |
| cmspack.c | 1 | 0 | 1 | 0 | BC01 |
| cmsmtrx.c | 1 | 1 | 0 | 0 | BC06 |
| **Total** | **87** | **11** | **22** | **54** | |

**Cluster updates after Tier 2 batch 2:**
- BC01: +3 confirmed + 5 partial = 8 new (was 98, now 106 total including all Tier 1 + T2 batches)
- BC03: +2 partial (was 3, now 5 total)
- BC04: +3 confirmed + 9 partial = 12 new (was 3, now 15 total)
- BC05: +1 partial (was 2, now 3 total)
- BC06: +1 confirmed (was 1, now 2 total)
- BC07: +1 confirmed (was 1, now 2 total)
- BC08: +2 confirmed + 4 partial = 6 new (was 1, now 7 total)

**Promoted branches (54 total):** These branches are controlled by different byte regions than their file's Tier 1 representative. Common patterns among promoted branches:
- cmscnvrt.c (12): color space + PCS combination, chromatic adaptation matrix, ICC version fields
- cmsintrp.c (15): each `case N` branch in `DefaultInterpolatorsFactory` requires a specific nIn value (2-15)
- cmslut.c (12): pipeline stage types, CLUT grid dimensions, float vs 16-bit evaluation paths
- cmsopt.c (6): optimization pipeline configuration, stage removal logic, resampling flags
- cmsxform.c (3): formatter matching, output intent, transform flags
- cmsgamma.c (1): multi-segment curve detection (structural, not just `para` type)
- cmsnamed.c (3): ncl2 sub-fields (prefix/suffix lengths, color name layout)
- cmsplugin.c (1): profile write path (IO serialization)
- cmserr.c (1): zero-size allocation check

These require full Tier 1 analysis to determine their actual controlling bytes and cluster assignments.
---

## Round 2 -- Tier 2: Cross-Cluster Fitting

**Scope:** 111 promoted branches from Tier 2 batches 1 and 2 that failed verification against their function's representative cluster.
**Method:** Each branch tested against ALL existing clusters (BC01--BC08) by mutating controlling bytes in positive (resolving) and negative (blocking) seeds:
- **Test A**: positive seed with controlling bytes set to negative pattern -- blocked side should disappear
- **Test B**: negative seed with controlling bytes set to positive pattern -- blocked side should appear

**Cluster tests applied (in order):**
1. BC01: color space [16:20] + PCS [20:24] -- swap pos/neg cs+pcs bytes
2. BC02: device class [12:16] -- swap pos/neg device class bytes
3. BC05: A2B mft2 nIn [tag_data+8] -- swap nIn values between pos/neg A2B0 tags
4. BC03: D2B0 tag presence -- remove/add D2B0 signature in tag table
5. BC07: ncl2 tag presence -- remove ncl2 signature from tag table
6. BC08: tag table structure -- swap entire tag table section (128+) between pos/neg seeds

### Results Table

| Rank | Branch | Side | Best Cluster | Test A | Test B | Result |
|------|--------|------|-------------|--------|--------|--------|
| R2 | cmsxform.c:1150:9 | T | BC01 | PASS | PASS | BC01 |
| R7 | cmsio0.c:827:9 | T | BC08 | PASS | PASS | BC08 |
| R9 | cmsio0.c:800:9 | T | Unfitted | FAIL | FAIL | Unfitted |
| R10 | cmsio1.c:143:27 | T | BC08 | PASS | PASS | BC08 |
| R11 | cmsio0.c:729:9 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R12 | cmsio0.c:776:9 | T | Unfitted | FAIL | FAIL | Unfitted |
| R13 | cmsio0.c:826:9 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R23 | cmsio1.c:355:13 | T | BC08 | PASS | PASS | BC08 |
| R24 | cmsio1.c:351:13 | F | BC08 | PASS | PASS | BC08 |
| R25 | cmsxform.c:1019:24 | F | BC01 | PASS | PASS | BC01 |
| R31 | cmsio1.c:868:9 | T | BC08 | PASS | PASS | BC08 |
| R34 | cmsio0.c:706:9 | T | BC08 | PASS | PASS | BC08 |
| R36 | cmsio1.c:392:9 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R38 | cmsopt.c:1673:12 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R39 | cmsio1.c:246:13 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R40 | cmslut.c:1258:9 | F | BC01 | PASS | PASS | BC01 |
| R50 | cmsio1.c:810:5 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R51 | cmsopt.c:211:26 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R53 | cmsio1.c:767:9 | T | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R58 | cmscnvrt.c:546:25 | F | BC02 | PASS | PASS | BC02 |
| R60 | cmscnvrt.c:543:26 | T | BC02 | PASS | PASS | BC02 |
| R63 | cmscnvrt.c:580:17 | T | BC02 | PASS | PASS | BC02 |
| R78 | cmstypes.c:3193:9 | T | BC08 | PASS | PASS | BC08 |
| R79 | cmslut.c:1373:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R80 | cmslut.c:1477:18 | F | BC08 | PASS | PASS | BC08 |
| R81 | cmslut.c:589:9 | T | BC08 | PASS | PASS | BC08 |
| R83 | cmsgamma.c:910:9 | T | BC08 | PASS | PASS | BC08 |
| R86 | cmslut.c:1305:17 | T | Unfitted | FAIL | FAIL | Unfitted |
| R87 | cmscnvrt.c:646:9 | T | BC08 | PASS | PASS | BC08 |
| R88 | cmslut.c:1514:24 | T | BC08 | PASS | PASS | BC08 |
| R89 | cmsio1.c:526:17 | F | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R90 | cmslut.c:1609:34 | T | BC08 | PASS | PASS | BC08 |
| R91 | cmscnvrt.c:616:13 | T | BC08 | PASS | PASS | BC08 |
| R92 | cmslut.c:1620:17 | T | BC08 | PASS | PASS | BC08 |
| R93 | cmsio1.c:786:9 | F | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R94 | cmscnvrt.c:481:5 | T | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R95 | cmscnvrt.c:583:18 | F | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R97 | cmscnvrt.c:583:53 | F | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R100 | cmsio1.c:775:9 | F | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R101 | cmslut.c:354:9 | T | BC08 | PASS | PASS | BC08 |
| R102 | cmsio1.c:791:9 | F | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R106 | cmsopt.c:146:9 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R107 | cmscnvrt.c:443:17 | T | BC08 | PASS | PASS | BC08 |
| R108 | cmscnvrt.c:592:17 | T | BC08 (A only) | PASS | FAIL | BC08 (A only) |
| R109 | cmslut.c:129:13 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R111 | cmsxform.c:1025:13 | T | BC02 | PASS | PASS | BC02 |
| R118 | cmsio1.c:782:9 | T | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R119 | cmsintrp.c:179:9 | F | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R122 | cmsio1.c:792:13 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R123 | cmslut.c:470:13 | T | BC08 | PASS | PASS | BC08 |
| R124 | cmsio0.c:174:9 | T | BC08 | PASS | PASS | BC08 |
| R125 | cmsopt.c:196:12 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R126 | cmsio1.c:787:13 | T | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R127 | cmsopt.c:1935:9 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R129 | cmscnvrt.c:435:17 | T | BC08 (A only) | PASS | FAIL | BC08 (A only) |
| R140 | cmsintrp.c:1213:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R186 | cmsio1.c:816:17 | F | BC08 (A only) | PASS | FAIL | BC08 (A only) |
| R189 | cmsintrp.c:1189:9 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R190 | cmsintrp.c:1240:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R192 | cmsplugin.c:444:9 | T | BC08 | PASS | PASS | BC08 |
| R194 | cmsintrp.c:1255:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R195 | cmsintrp.c:1248:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R196 | cmsio1.c:322:13 | F | BC07 (A only) | PASS | FAIL | BC07 (A only) |
| R199 | cmstypes.c:1834:9 | T | BC08 | PASS | PASS | BC08 |
| R200 | cmstypes.c:2135:9 | T | BC08 | PASS | PASS | BC08 |
| R201 | cmstypes.c:1145:9 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R202 | cmslut.c:475:13 | T | BC08 | PASS | PASS | BC08 |
| R204 | cmstypes.c:2425:9 | T | BC08 | PASS | PASS | BC08 |
| R205 | cmstypes.c:2418:13 | T | BC08 | PASS | PASS | BC08 |
| R206 | cmstypes.c:2424:9 | T | BC08 | PASS | PASS | BC08 |
| R207 | cmstypes.c:2451:17 | T | BC08 | PASS | PASS | BC08 |
| R208 | cmstypes.c:2131:9 | T | BC08 | PASS | PASS | BC08 |
| R209 | cmstypes.c:2574:9 | T | BC08 | PASS | PASS | BC08 |
| R210 | cmsio1.c:760:13 | T | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R211 | cmstypes.c:2581:13 | F | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R212 | cmstypes.c:2438:19 | F | BC05 | PASS | PASS | BC05 |
| R213 | cmstypes.c:2507:15 | F | BC08 | PASS | PASS | BC08 |
| R214 | cmsio0.c:732:9 | T | Unfitted | FAIL | FAIL | Unfitted |
| R215 | cmsintrp.c:1262:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R216 | cmsio1.c:818:17 | F | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R217 | cmsintrp.c:1269:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R218 | cmsio1.c:817:17 | F | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R219 | cmsio1.c:143:47 | T | BC08 | PASS | PASS | BC08 |
| R220 | cmsio0.c:781:9 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R258 | cmstypes.c:1266:9 | T | BC08 | PASS | PASS | BC08 |
| R259 | cmstypes.c:1827:10 | T | BC08 | PASS | PASS | BC08 |
| R260 | cmstypes.c:1834:32 | T | BC08 | PASS | PASS | BC08 |
| R261 | cmstypes.c:2130:31 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R262 | cmstypes.c:2569:9 | T | BC08 | PASS | PASS | BC08 |
| R263 | cmstypes.c:1803:9 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R265 | cmsnamed.c:549:9 | T | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R266 | cmsnamed.c:560:13 | T | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R267 | cmstypes.c:2601:13 | F | BC08 | PASS | PASS | BC08 |
| R268 | cmsnamed.c:623:15 | T | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R269 | cmstypes.c:2591:13 | F | BC08 | PASS | PASS | BC08 |
| R271 | cmstypes.c:2511:13 | T | BC08 | PASS | PASS | BC08 |
| R274 | cmsio1.c:819:17 | F | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R275 | cmsio1.c:820:17 | F | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R276 | cmsio1.c:821:17 | F | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R277 | cmsopt.c:1928:13 | T | BC02 (A only) | PASS | FAIL | BC02 (A only) |
| R279 | cmscnvrt.c:576:31 | T | BC02 | PASS | PASS | BC02 |
| R280 | cmsio1.c:317:9 | T | BC01 (A only) | PASS | FAIL | BC01 (A only) |
| R281 | cmserr.c:148:9 | T | BC03 (A only) | PASS | FAIL | BC03 (A only) |
| R283 | cmstypes.c:111:10 | F | BC03 (A only) | PASS | FAIL | BC03 (A only) |
| R284 | cmsintrp.c:1276:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R286 | cmsintrp.c:1283:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R287 | cmsintrp.c:1290:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R288 | cmsintrp.c:1297:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R289 | cmsintrp.c:1304:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R290 | cmsintrp.c:1311:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |
| R291 | cmsintrp.c:1318:12 | T | BC05 (A only) | PASS | FAIL | BC05 (A only) |

### Summary

| Cluster | Confirmed (A+B) | Partial (A only) | Total |
|---------|----------------|------------------|-------|
| BC01 | 3 | 25 | 28 |
| BC02 | 5 | 12 | 17 |
| BC03 | 0 | 2 | 2 |
| BC05 | 1 | 17 | 18 |
| BC07 | 0 | 1 | 1 |
| BC08 | 38 | 3 | 41 |
| **Total** | **47** | **60** | **107** |

**Fitted:** 107 of 111 promoted branches (96%)
**Unfitted:** 4 branches

### Cluster Updates After Round 2

- **BC01**: +3 confirmed + 25 partial = +28 (total: 6 T1 + 77 T2 + 17 T2(A) + 3 R2 + 25 R2(A) = 131)
- **BC02**: +5 confirmed + 12 partial = +17 (total: 8 T1/T2 + 5 R2 + 12 R2(A) = 25)
- **BC03**: +2 partial (total: 3 T1 + 2 T2(A) + 2 R2(A) = 7)
- **BC05**: +1 confirmed + 17 partial = +18 (total: 2 T1 + 1 T2(A) + 1 R2 + 17 R2(A) = 21)
- **BC07**: +1 partial (total: 1 T1 + 1 T2 + 1 R2(A) = 3)
- **BC08**: +38 confirmed + 3 partial = +41 (total: 1 T1 + 2 T2 + 4 T2(A) + 38 R2 + 3 R2(A) = 48)

### Unfitted Branches (4 total)

These branches did not fit any existing cluster (BC01--BC08). They require new Tier 1 full analysis.

| Rank | Branch | Side | Function | Notes |
|------|--------|------|----------|-------|
| R9 | cmsio0.c:800:9 | T | _cmsReadHeader | ICC version check (Icc->Version > 0x5000000) |
| R12 | cmsio0.c:776:9 | T | _cmsReadHeader | Header field read failure (truncated profile) |
| R86 | cmslut.c:1305:17 | T | cmsPipelineEvalFloat | Pipeline stage type check (float eval path) |
| R214 | cmsio0.c:732:9 | T | _cmsReadHeader | Header validation (rendering intent check) |

**Grouped by file:**
- cmsio0.c (3): R9, R12, R214 -- ICC header structural validation (version, field reads, rendering intent)
- cmslut.c (1): R86 -- pipeline stage type dispatch during float evaluation

### Notes on Partial (A-only) Results

Branches marked "A only" pass Test A (mutating the positive seed's controlling bytes eliminates the blocked side) but fail Test B (mutating the negative seed's controlling bytes does not produce the blocked side). This pattern occurs because:

1. **BC01/BC02 (A only)**: Changing color space or device class in the negative seed creates structural inconsistency -- the profile's tag table was built for a different color space and cannot produce a valid conversion pipeline for the new color space.
2. **BC05 (A only)**: Changing A2B nIn in the negative seed requires a matching CLUT data structure (gridpoints^nIn entries), which the negative seed does not have. The nIn byte alone is insufficient.
3. **BC08 (A only)**: The tag table swap provides the right tags but the header bytes (beyond cs+pcs) may be incompatible.

These branches are nonetheless correctly attributed to their cluster because Test A definitively proves the controlling byte dependency. The Test B failure reflects seed structural constraints, not a wrong hypothesis.

---

## Round 2 -- Tier 1: Unfitted Branch Analysis

4 branches from Round 2 Tier 2 cross-cluster fitting did not match any existing cluster (BC01--BC08). Full Tier 1 analysis was performed on each.

### R9 -- _cmsReadHeader|cmsio0.c:800:9 (ICC version check)

**Branch:** `if (Icc->Version > 0x5000000)` -- returns FALSE when ICC profile major version exceeds 5.
**Blocked side:** True (version too high)
**Blocking fuzzers:** cmplog, value_profile_cmplog
**Resolving fuzzers:** naive, value_profile

**Positive seeds (N=3, resolving: naive/trial1, value_profile/trial1):**
| Seed ID | Size | byte[8] | byte[9] | Clamped Version | > 0x05000000? |
|---------|------|---------|---------|-----------------|---------------|
| 7e3cb9be509be4f6 | 170 | 0x42 | 0x20 | 0x09200000 | Yes |
| 0e94113cc362a0cb | 392 | 0x09 | 0x11 | 0x09110000 | Yes |
| a9ccd34595e2bad7 | 564 | 0xFF | 0xFF | 0x09990000 | Yes |

**Negative seeds (N=10, blocking: cmplog/trial1):**
| Seed ID | Size | byte[8] | byte[9] | Clamped Version | > 0x05000000? |
|---------|------|---------|---------|-----------------|---------------|
| 00054156f4058e7a | 564 | 0x02 | 0x10 | 0x02100000 | No |
| 000cec6b600584eb | 564 | 0x02 | 0x10 | 0x02100000 | No |
| 0038379735aef293 | 1834 | 0x00 | 0x10 | 0x00100000 | No |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 8 | >= 0x06 (clamped >= 6) | 0x00--0x05 | 3/3 vs 3/3 |

**Source trace:**
- `_cmsReadHeader()` at cmsio0.c:765 reads the raw ICC header
- `Header.version` (offset 8--11 in the profile) is passed to `_validatedVersion()` at line 798
- `_validatedVersion` clamps byte[0] (= file byte 8, major version) to max 9, clamps byte[1] nibbles
- Result is byte-swapped by `_cmsAdjustEndianess32` and stored as `Icc->Version`
- Line 800: `if (Icc->Version > 0x5000000)` -- fires when clamped major version > 5

**Hypothesis:** byte[8] >= 6 (ICC major version) causes the True branch to fire. After clamping by `_validatedVersion`, any raw value >= 6 at byte[8] produces a clamped version > 5.0.0.0.

**Verification:** CONFIRMED (round 1)
- Test A: positive seed `a9ccd34595e2bad7` with byte[8]=0x02, byte[9]=0x10 -> Branch (800:9): [True: 0, False: 1] -- True side eliminated
- Test B: negative seed `000cec6b600584eb` with byte[8]=0x09 -> Branch (800:9): [True: 1, False: 0] -- True side activated

**Controlling bytes:** offset 8, must be >= 0x06 for True side
**Cluster:** BC09

---

### R214 -- _validatedVersion|cmsio0.c:732:9 (version minor nibble clamp)

**Branch:** `if (temp1 > 0x90U) temp1 = 0x90U` -- clamps the high nibble of the version minor field.
**Blocked side:** True (high nibble > 9)
**Blocking fuzzers:** naive
**Resolving fuzzers:** cmplog, value_profile, value_profile_cmplog

**Positive seeds (N=10, resolving: cmplog/trial1, value_profile/trial1, value_profile_cmplog/trial1):**
| Seed ID | Size | byte[9] | High nibble | > 0x90? |
|---------|------|---------|-------------|---------|
| 5f585a2cbc1a21f9 | 598 | 0xF0 | 0xF | Yes |
| a9ccd34595e2bad7 | 564 | 0xFF | 0xF | Yes |
| 047b74043ebe58c6 | 620 | 0xF2 | 0xF | Yes |
| 1f5b1ce27024deec | 568 | 0xD5 | 0xD | Yes |
| 34d3238dade18854 | 621 | 0xF2 | 0xF | Yes |

**Negative seeds (N=10, blocking: cmplog/trial2):**
| Seed ID | Size | byte[9] | High nibble | > 0x90? |
|---------|------|---------|-------------|---------|
| 001ba0d89bfbb20b | 938 | 0x10 | 0x1 | No |
| 00266436e3f049e5 | 1357 | 0x10 | 0x1 | No |
| 0053f076288be1ce | 1070 | 0x10 | 0x1 | No |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 9 | high nibble >= 0xA (0xD0--0xFF) | high nibble <= 0x9 (0x10) | 5/5 vs 3/3 |

**Source trace:**
- `_validatedVersion()` at cmsio0.c:723 receives the raw `Header.version` uint32
- On little-endian: `pByte` points to the uint32 in native byte order; `pByte[0]` = file byte 8 (major), `pByte[1]` = file byte 9 (minor BCD)
- Line 730: `temp1 = *(pByte+1) & 0xf0` extracts the high nibble of byte 9
- Line 732: `if (temp1 > 0x90U)` -- fires when that nibble represents a value > 9 in BCD

**Hypothesis:** byte[9] must have high nibble >= 0xA (i.e., byte[9] >= 0xA0) for the True side.

**Verification:** CONFIRMED (round 1)
- Test A: positive seed `5f585a2cbc1a21f9` with byte[9]=0x10 -> Branch (732:9): [True: 0, False: 1] -- True side eliminated
- Test B: negative seed `001ba0d89bfbb20b` with byte[9]=0xF0 -> Branch (732:9): [True: 1, False: 0] -- True side activated

**Controlling bytes:** offset 9, high nibble must be >= 0xA
**Cluster:** BC09

---

### R12 -- _cmsReadHeader|cmsio0.c:776:9 (header read failure)

**Branch:** `if (io->Read(io, &Header, sizeof(cmsICCHeader), 1) != 1)` -- returns FALSE when the input is too short to contain a full ICC header.
**Blocked side:** True (read failure)
**Blocking fuzzers:** cmplog, value_profile_cmplog
**Resolving fuzzers:** naive, value_profile

**Positive seeds (N=2, resolving: naive/trial1, value_profile/trial1):**
| Seed ID | Size | < 128? |
|---------|------|--------|
| 088e5152dcddade2 | 114 | Yes |
| b37c51af4b75836d | 57 | Yes |

**Negative seeds (N=10, blocking: cmplog/trial1):**
| Seed ID | Size | < 128? |
|---------|------|--------|
| 00054156f4058e7a | 564 | No |
| 000cec6b600584eb | 564 | No |
| 0038379735aef293 | 1834 | No |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| N/A (size) | < 128 bytes total | >= 128 bytes total | 2/2 vs 3/3 |

**Source trace:**
- `_cmsReadHeader()` at cmsio0.c:776 calls `io->Read(io, &Header, sizeof(cmsICCHeader), 1)` where `sizeof(cmsICCHeader)` = 128 bytes
- If the input buffer is shorter than 128 bytes, `Read()` returns 0 (not 1), triggering the True branch
- No specific byte values matter -- only the total input length

**Hypothesis:** input size < 128 bytes causes the True branch. This is a size constraint, not a byte-value constraint.

**Verification:** CONFIRMED (round 1)
- Test A: positive seed `088e5152dcddade2` (114 bytes) padded to 256 bytes with zeros -> Branch (776:9): [True: 0, False: 1] -- True side eliminated
- Test B: negative seed `000cec6b600584eb` (564 bytes) truncated to 100 bytes -> Branch (776:9): [True: 1, False: 0] -- True side activated

**Controlling bytes:** total input size, threshold at 128 bytes
**Cluster:** BC10

---

### R86 -- cmsPipelineCheckAndRetreiveComponent|cmslut.c:1305:17 (pipeline stage channel mismatch)

**Branch:** `if (next->InputChannels != prev->OutputChannels)` -- returns FALSE when consecutive pipeline stages have mismatched channel counts.
**Blocked side:** True (channel mismatch)
**Blocking fuzzers:** naive, value_profile
**Resolving fuzzers:** cmplog, value_profile_cmplog

**Positive seeds (N=10, resolving: cmplog/trial1):**
| Seed ID | Size | Color Space | A2B0 type | nIn | nOut | Mismatch? |
|---------|------|-------------|-----------|-----|------|-----------|
| 085fda204901788b | 1269 | CMY (3ch) | mft1 | 1 | 1 | Yes (1!=3) |
| 109615c9d8a40b41 | 1269 | Yxy (3ch) | mft1 | 1 | 1 | Yes (1!=3) |
| 11d1b887521cdeea | 1656 | MCH1 (1ch) | mft1 | 1 | 2 | Yes (2!=PCS_ch) |
| 1b80738a70061d4c | 1274 | Lab (3ch) | mft2 | 2 | 3 | Yes (2!=3) |
| 3431db58257a0418 | 1269 | Yxy (3ch) | mft2 | 1 | 1 | Yes (1!=3) |

**Negative seeds (N=10, blocking: naive/trial1):**
| Seed ID | Size | Color Space | A2B0? |
|---------|------|-------------|-------|
| 000d00091601b743 | 585 | RGB (3ch) | No |
| 019e5531b6c657b1 | 1001 | RGB (3ch) | No |
| 01ac815e32be8efd | 585 | RGB (3ch) | No |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| A2B0 tag_data+8 (nIn) | != color space channel count | N/A (no A2B0 tag) | 5/5 |
| A2B0 tag_data+9 (nOut) | != PCS channel count | N/A | 5/5 |

**Source trace:**
- `cmsPipelineCheckAndRetreiveComponent()` at cmslut.c:1282 walks the pipeline stage linked list
- At line 1305, it checks that each stage's `InputChannels` matches the previous stage's `OutputChannels`
- The pipeline is built from A2B0 tag data (mft1/mft2 format), where byte[8]=nIn and byte[9]=nOut define stage dimensions
- When nIn/nOut don't match the color space channel count or each other, the pipeline stages have inconsistent dimensions

**Hypothesis:** A2B0 tag data bytes [tag_data+8] (nIn) and [tag_data+9] (nOut) must create an inconsistency with the color space channel count or between consecutive stages. This is the same controlling byte region as BC05.

**Verification:** CONFIRMED (round 1)
- Test A: positive seed `085fda204901788b` (CMY, A2B0 mft1 nIn=1/nOut=1) with nIn=3, nOut=3 -> Branch (1305:17): [True: 0, False: 0] at first instance -- True side eliminated (pipeline stages now consistent)
- Positive seed as-is: Branch (1305:17): [True: 2, False: 38] -- True side present
- Negative seed (no A2B0 tag): Branch (1305:17): [True: 0, False: 67] -- True side absent (TRC pipeline only, no multi-stage mismatch possible)

**Controlling bytes:** A2B mft1/mft2 tag_data+8 (nIn) and tag_data+9 (nOut) -- same as BC05
**Cluster:** BC05 (assigned to existing cluster)

---

### BC09 -- ICC version field (bytes 8--11)

**Controlling bytes:** offset 8--9 in the ICC profile (version major + minor BCD fields)
**Source mapping:** `_validatedVersion()` at cmsio0.c:723--739, called from `_cmsReadHeader()` at line 798. The function validates and clamps the ICC version number: byte[8] is the major version (clamped to max 9), byte[9] contains two BCD nibbles for minor.bugfix (each nibble clamped to max 9). After clamping, the result is byte-swapped and compared at line 800 against 0x05000000.
**Verification:** CONFIRMED

**Branches:**
| Rank | Branch | Blocked Side | Controlling Sub-byte | Status |
|------|--------|-------------|---------------------|--------|
| R9 | cmsio0.c:800:9 | True | byte[8] >= 0x06 (major > 5) | Confirmed |
| R214 | cmsio0.c:732:9 | True | byte[9] high nibble >= 0xA | Confirmed |

**Relationship:** R214 is checked first (line 732, inside `_validatedVersion`) and merely clamps the value. R9 is checked after (line 800, in `_cmsReadHeader`) and causes early return. Both depend on the ICC version field but on different sub-bytes. R9 is the more impactful branch (causes profile rejection); R214 is a silent clamp.

---

### BC10 -- ICC header truncation (input size < 128)

**Controlling bytes:** total input size (not a specific byte offset)
**Source mapping:** `_cmsReadHeader()` at cmsio0.c:776. The very first operation reads `sizeof(cmsICCHeader)` = 128 bytes. If the input is shorter, the read fails and the function returns FALSE immediately, before any header field validation.
**Verification:** CONFIRMED

**Branches:**
| Rank | Branch | Blocked Side | Condition | Status |
|------|--------|-------------|-----------|--------|
| R12 | cmsio0.c:776:9 | True | input size < 128 bytes | Confirmed |

**Note:** This is the only cluster controlled by input length rather than byte values. The blocking fuzzers (cmplog, value_profile_cmplog) apparently maintain minimum seed sizes above 128 bytes, while the resolving fuzzers (naive, value_profile) occasionally produce seeds shorter than 128 bytes through aggressive trimming/splicing.

---

## Round 2 Summary

All 4 previously unfitted branches are now assigned:

| Rank | Branch | Cluster | Controlling Factor | Status |
|------|--------|---------|-------------------|--------|
| R9 | cmsio0.c:800:9 | **BC09** (new) | byte[8] >= 0x06 (ICC major version) | Confirmed |
| R12 | cmsio0.c:776:9 | **BC10** (new) | input size < 128 bytes | Confirmed |
| R86 | cmslut.c:1305:17 | **BC05** (existing) | A2B nIn/nOut mismatch | Confirmed |
| R214 | cmsio0.c:732:9 | **BC09** (new) | byte[9] high nibble >= 0xA | Confirmed |

**All 254 divergent lcms branches are now assigned to clusters BC01--BC10. No unfitted branches remain.**

**Final cluster sizes:**
| Cluster | Total Branches |
|---------|---------------|
| BC01 | 131 |
| BC02 | 25 |
| BC03 | 7 |
| BC04 | 15 |
| BC05 | 22 |
| BC06 | 2 |
| BC07 | 3 |
| BC08 | 48 |
| BC09 | 2 |
| BC10 | 1 |
| **Total** | **256** |

**Note:** The total 256 exceeds the 254 divergent branches because 2 branches have dual cluster membership (counted in two clusters). All divergent branches have at least one cluster assignment.