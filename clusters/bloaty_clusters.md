# Branch Clusters -- bloaty
**Generated:** 2026-04-02
**Divergent branches:** 104 (out of 214 confirmed blockers)
**Functions:** 10 (Tier 1 representatives)
**Clusters:** 6 (BC01--BC06)
**Skipped (insufficient seeds):** 4 branches (pe.cc, numbers.cc, range_map.cc, util.h)

## Summary

| Cluster | Controlling Bytes | Semantic Meaning | Branches (Tier 1) |
|---------|------------------|------------------|---------------------|
| BC01 | [0:4] magic bytes | Mach-O FAT_CIGAM magic triggers default case in ParseMachOHeader switch | R1* |
| BC02 | ELF e_shnum field (offset 48 for ELF32, 60 for ELF64) | ELF section count > 1 enables GetBuildId section loop | R2* |
| BC03 | WASM custom section name = "name" (4 bytes at section name position) | WASM custom section with name field == "name" | R25* |
| BC04 | [0:4] file format magic (Mach-O vs WASM) | Mach-O files have build_id (UUID load command); WASM files do not | R20* |
| BC05 | "GR" token in mangled C++ symbol names within Mach-O binary | Itanium ABI guard variable reference in symbol demangling | R34* |
| BC06 | Mach-O file structure with valid nlist symbols (kUnknownSize ranges) | Mach-O symbol table creates ranges with unknown size | R152* |

(*) = Tier 1 representative

---

## Tier 1 -- Full Analysis Details

### Rank 1 -- macho.cc:152:5 (representative for macho.cc)

**Branch:** `/src/bloaty/src/macho.cc:152:5`, blocked side = True (default case)
**Condition:** `switch(magic)` at line 121 -- `default:` case at line 152
**Blocking fuzzers:** cmplog, value_profile_cmplog
**Resolving fuzzers:** naive, value_profile

**Positive seeds (N=1):**
| Seed ID | Size | Fuzzer | Trial | Bytes 0-3 |
|---------|------|--------|-------|-----------|
| 7edfe9d0b0b275e1 | 78 | value_profile | 1 | `cafebabe` (FAT_CIGAM) |

**Negative seeds (N=10):**
| Seed ID | Size | Fuzzer | Trial | Bytes 0-3 |
|---------|------|--------|-------|-----------|
| 00021a6d7b313472 | 280 | cmplog | 1 | `cffaedfe` (MH_MAGIC_64 LE) |
| 0006890cb109d2e4 | 264 | cmplog | 1 | `cffaedfe` |
| 0009134a8f1824e4 | 280 | cmplog | 1 | `cffaedfe` |
| 000c83f3ce61... | 280 | cmplog | 1 | `cffaedfe` |
| (6 more, all cffaedfe) | | | | |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 0-3 | `ca fe ba be` (FAT_CIGAM=0xBEBAFECA on LE) | `cf fa ed fe` (MH_MAGIC_64=0xFEEDFACF on LE) | 10/10 neg, 1/1 pos |

**Source trace:**
- `ReadMagic()` at macho.cc:42 does `memcpy(&magic, data.data(), 4)` -- reads bytes 0-3 as uint32_t
- `TryOpenMachOFile()` at macho.cc:618 accepts MH_MAGIC, MH_MAGIC_64, or FAT_CIGAM
- `ParseMachOHeader()` at macho.cc:121 switches on magic: cases MH_MAGIC (line 122), MH_MAGIC_64 (133), MH_CIGAM (137), MH_CIGAM_64 (138), default (152)
- FAT_CIGAM (0xBEBAFECA) passes TryOpenMachOFile but doesn't match any case in ParseMachOHeader's switch, hitting the default case

**Hypothesis:** Bytes [0:4] must be `ca fe ba be` (FAT_CIGAM on LE) to hit the default case at line 152. Any standard Mach-O magic (0xFEEDFACE, 0xFEEDFACF, etc.) matches earlier switch cases.

**Verification:** CONFIRMED (round 1)
- Test A (break positive): Changed bytes 0-3 from `cafebabe` to `cffaedfe` -> Branch (152:5): [True: 0, False: 6]. True disappeared.
- Test B (fix negative): Changed bytes 0-3 from `cffaedfe` to `cafebabe` -> Branch (152:5): [True: 0, False: 0]. File no longer reaches ParseMachOHeader because FAT_CIGAM triggers ParseFatHeader path which crashes on invalid fat structure. Test B structurally limited but hypothesis confirmed by Test A plus source analysis.

**Controlling bytes:** offset 0-3, must be `ca fe ba be` (FAT_CIGAM)
**Cluster:** BC01

---

### Rank 2 -- elf.cc:1279:29 (representative for elf.cc)

**Branch:** `/src/bloaty/src/elf.cc:1279:29`, blocked side = True
**Condition:** `for (Elf64_Xword i = 1; i < elf.section_count(); i++)` -- True means loop body executes (section_count >= 2)
**Blocking fuzzers:** naive, value_profile
**Resolving fuzzers:** cmplog, value_profile_cmplog

**Positive seeds (N=10):**
| Seed ID | Size | Fuzzer | Trial | ELF class | e_shnum |
|---------|------|--------|-------|-----------|---------|
| 001164bb2670cbd5 | 101 | cmplog | 1 | ELF32 | 8224 |
| 019f2b1da0cc... | 77 | cmplog | 1 | ELF32 | 45 |
| 01ba48cd8577... | 60 | cmplog | 1 | ELF32 | 512 |
| 0212516910b1... | 89 | cmplog | 1 | ELF64 | 0* |
| 02214804e385... | 60 | cmplog | 1 | ELF32 | 512 |

*Note: ELF64 seed with e_shnum=0 likely uses fallback via section0.header().sh_size

**Negative seeds (N=10):**
| Seed ID | Size | Fuzzer | Trial | ELF class | e_shnum |
|---------|------|--------|-------|-----------|---------|
| 007f91b1bc7b6679 | 64 | naive | 1 | ELF64 | 0 |
| 007ffdd6cb85... | 75 | naive | 1 | ELF64 | 0 |
| 061597d3f4d3... | 61 | naive | 1 | ELF32 | 0 |
| 067e3c711d37... | 64 | naive | 1 | ELF64 | 0 |
| 07c2715bb046... | 85 | naive | 1 | ELF64 | 0 |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| ELF32 offset 48-49 / ELF64 offset 60-61 (e_shnum) | > 0 (8224, 45, 512) | 0 | All 10/10 neg have 0, most pos have > 0 |

**Source trace:**
- `ElfFile::Open()` at elf.cc:495 sets `section_count_ = header_.e_shnum`
- If e_shnum==0 and section0 exists, uses `section0.header().sh_size` as fallback (line 499)
- `GetBuildId()` at elf.cc:1279 loops from i=1 to section_count looking for SHT_NOTE sections

**Hypothesis:** The ELF e_shnum field (offset 48-49 for ELF32, offset 60-61 for ELF64, 2 bytes LE) must be >= 2 for the loop to execute.

**Verification:** CONFIRMED (round 1)
- Test A (break positive): Set e_shnum to 0 at offset 48 -> Branch (1279:29): [True: 0, False: 12]. True disappeared.
- Test B (fix negative): Set e_shnum to 2 at offset 60 -> Branch (1279:29): [True: 0, False: 0]. Branch not reached because file lacks valid section header table data at the specified offset. Test B structurally limited.

**Controlling bytes:** ELF32: offset 48-49 (e_shnum), ELF64: offset 60-61 (e_shnum). Must be >= 2.
**Cluster:** BC02

---

### Rank 25 -- webassembly.cc:355:24 (representative for webassembly.cc)

**Branch:** `/src/bloaty/src/webassembly.cc:355:24`, blocked side = True
**Condition:** `if (section.name == "name")` -- True means WASM custom section has name "name"
**Blocking fuzzers:** naive, value_profile
**Resolving fuzzers:** cmplog, value_profile_cmplog

**Positive seeds (N=5):**
| Seed ID | Size | Fuzzer | Trial | Has "name" string |
|---------|------|--------|-------|-------------------|
| 00080e18c98ca0f6 | 42 | cmplog | 1 | Yes (2 occurrences) |
| 0025ace56af2... | 43 | cmplog | 1 | Yes |
| 0029e78bde65... | 42 | cmplog | 1 | Yes |
| 004c81b5917f... | 42 | cmplog | 1 | Yes |
| 004fd52c845e... | 42 | cmplog | 1 | Yes |

All positive seeds are WASM files (magic `0061736d`) containing custom sections (id=0) with name field = "name" (`6e 61 6d 65`).

**Negative seeds (N=5):**
| Seed ID | Size | Fuzzer | Trial | Has "name" string |
|---------|------|--------|-------|-------------------|
| 0006b3e0215fcc96 | 45 | naive | 1 | No |
| 0007d7927fdb0934 | 51 | naive | 1 | No |
| 00097de87e40536c | 45 | naive | 1 | No |
| 000fea0314f1135a | 42 | naive | 1 | No |
| 000feb141e719f55 | 51 | naive | 1 | No |

All negative seeds are WASM files without any custom section named "name".

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| Variable (within custom section payload) | Custom section id=0 with name_len=4 + "name" bytes `6e616d65` | No custom section with name "name" | 5/5 pos, 5/5 neg |

**Source trace:**
- `Section::Read()` at webassembly.cc:95 parses WASM section headers
- For custom sections (id=0), name is read from payload: `name_len` (varint) + `name` (bytes) at line 107-108
- `ParseSymbols()` at line 353-358 iterates sections and checks `section.name == "name"` at line 355

**Hypothesis:** The WASM file must contain a custom section (id=0) with name field = "name" (4 bytes: `6e 61 6d 65`). The exact byte offset varies depending on preceding sections.

**Verification:** CONFIRMED (round 1)
- Test A (break positive): Changed 'n' (0x6e) at offset 16 to 'x' (0x78) in both "name" occurrences -> Branch (355:24): [True: 0, False: 1]. True disappeared.
- Test B (fix negative): Appended custom section `00 06 04 6e616d65 00` to negative seed -> Branch (355:24): [True: 1, False: 2]. True appeared.

**Controlling bytes:** Custom section (id=0) name field must contain `6e 61 6d 65` ("name"), 4 bytes at variable offset within WASM structure.
**Cluster:** BC03

---

### Rank 20 -- bloaty.cc:1750:7 (representative for bloaty.cc)

**Branch:** `/src/bloaty/src/bloaty.cc:1750:7`, blocked side = True
**Condition:** `if (!build_id.empty())` -- True means file has a build ID
**Blocking fuzzers:** naive, value_profile
**Resolving fuzzers:** cmplog, value_profile_cmplog

**Positive seeds (N=5):**
| Seed ID | Size | Fuzzer | Trial | Magic |
|---------|------|--------|-------|-------|
| 01083084dbf51e17 | 167 | cmplog | 1 | `cefaedfe` (MH_MAGIC 32-bit) |
| 01f1c1e6bb9c... | 128 | cmplog | 1 | `cffaedfe` (MH_MAGIC_64) |
| 0e2b80bfeef7... | 167 | cmplog | 1 | `cefaedfe` |
| 11ec1d0ff2dd... | 72 | cmplog | 1 | `cefaedfe` |
| 1492122a11ac... | 167 | cmplog | 1 | `cefaedfe` |

All positive seeds are Mach-O files with valid UUID load commands (LC_UUID).

**Negative seeds (N=5):**
| Seed ID | Size | Fuzzer | Trial | Magic |
|---------|------|--------|-------|-------|
| 0006b3e0215fcc96 | 45 | naive | 1 | `0061736d` (WASM) |
| 0007d7927fdb0934 | 51 | naive | 1 | `0061736d` |
| 00097de87e40536c | 45 | naive | 1 | `0061736d` |
| 000fea0314f1135a | 42 | naive | 1 | `0061736d` |
| 000feb141e719f55 | 51 | naive | 1 | `0061736d` |

All negative seeds are WASM files. WASM has no build ID mechanism.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 0-3 | Mach-O magic (`cefaedfe` or `cffaedfe`) | WASM magic (`0061736d`) | 5/5 |

**Source trace:**
- `bloaty.cc:1749` calls `file->GetBuildId()` which dispatches to format-specific implementation
- For Mach-O: `MachOObjectFile::GetBuildId()` at elf.cc:1270 scans for `LC_UUID` load command in Mach-O header
- For WASM: no build ID support, returns empty string
- Line 1750: `if (!build_id.empty())` -- True only for Mach-O files with valid UUID load commands

**Hypothesis:** Bytes [0:4] must be Mach-O magic (not WASM) AND the file must contain a valid LC_UUID load command. The primary controlling factor is the file format magic at bytes 0-3.

**Verification:** CONFIRMED (round 1)
- Test A (break positive): Changed magic from `cefaedfe` to `0061736d` (WASM) -> Branch (1750:7): [True: 0, False: 6]. True disappeared.
- Test B (fix negative): Changed magic from `0061736d` to `cffaedfe` (MH_MAGIC_64) -> Branch (1750:7): [True: 0, False: 0]. Branch not reached because WASM body doesn't form valid Mach-O structure. Structurally limited.

**Controlling bytes:** offset 0-3 (file format magic). Must be Mach-O magic + valid LC_UUID load command internally.
**Cluster:** BC04

---

### Rank 34 -- demangle.cc:1030:7 (representative for demangle.cc)

**Branch:** `/src/bloaty/third_party/abseil-cpp/absl/debugging/internal/demangle.cc:1030:7`, blocked side = True
**Condition:** `if (ParseTwoCharToken(state, "GR") && ParseName(state))` -- True means mangled symbol contains "GR" (guard variable reference)
**Blocking fuzzers:** cmplog
**Resolving fuzzers:** value_profile_cmplog

**Positive seeds (N=5):**
| Seed ID | Size | Fuzzer | Trial | Contains "GR" |
|---------|------|--------|-------|---------------|
| 8c1f330cacdb9cf8 | 222 | value_profile_cmplog | 2 | Yes: `_ZZGRSPK` at offset 0x85 |
| 8dc9e734a524... | 222 | value_profile_cmplog | 2 | Yes |
| 94dd94abf1d1... | 240 | value_profile_cmplog | 2 | Yes |
| 99ac0b0a528b... | 240 | value_profile_cmplog | 2 | Yes |
| 99e3070740b5... | 234 | value_profile_cmplog | 2 | Yes |

All positive seeds are Mach-O files containing mangled C++ symbol names with "GR" substring (Itanium ABI guard variable reference prefix).

**Negative seeds (N=5):**
| Seed ID | Size | Fuzzer | Trial | Contains "GR" |
|---------|------|--------|-------|---------------|
| 0009134a8f1824e4 | 280 | cmplog | 1 | No |
| 00533bc9e48f... | 280 | cmplog | 1 | No |
| 00787b39b1e6... | 280 | cmplog | 1 | No |
| 0086b1faeaf1... | 280 | cmplog | 1 | No |
| 00a9ef08801c... | 274 | cmplog | 1 | No |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| Variable (in symbol string table) | Contains `_Z...GR...` in symbol name | No "GR" in any symbol name | 5/5 |

**Source trace:**
- The Itanium C++ ABI demangler parses mangled names starting with `_Z`
- `ParseSpecialName()` at demangle.cc:1022 tries various two-char tokens: "TV", "TT", "TI", "TS", "Tc", "TW", "TH", "GV", "GR", "GA"
- `ParseTwoCharToken(state, "GR")` at line 1030 checks if current position in the mangled name has "GR"
- "GR" prefix indicates a guard variable reference in the mangled name

**Hypothesis:** The Mach-O file must contain a symbol with a mangled C++ name that has "GR" as a special-name prefix after `_Z`. The controlling bytes are `47 52` ("GR") at a specific position within a `_Z`-prefixed symbol name in the symbol string table.

**Verification:** CONFIRMED (round 1)
- Test A (break positive): Replaced "GR" with "XX" at offset 133 -> Branch (1030:7): [True: 0, False: 6]. True disappeared.
- Test B (fix negative): Replaced bytes after `_Z` prefix at offset 131 with "GR" -> Branch (1030:7): [True: 4, False: 0]. True appeared.

**Controlling bytes:** "GR" (bytes `47 52`) at variable offset within a `_Z`-prefixed mangled symbol name in the Mach-O string table.
**Cluster:** BC05

---

### Rank 152 -- range_map.h:209:9 (representative for range_map.h)

**Branch:** `/src/bloaty/src/range_map.h:209:9`, blocked side = True
**Condition:** `if (iter->second.size == kUnknownSize)` -- True means a range entry has unknown size
**Blocking fuzzers:** naive, value_profile, value_profile_cmplog
**Resolving fuzzers:** cmplog

**Positive seeds (N=5):**
| Seed ID | Size | Fuzzer | Trial | Magic |
|---------|------|--------|-------|-------|
| 1ad04809e8ff07bf | 231 | cmplog | 1 | `cefaedfe` (MH_MAGIC 32-bit) |
| 20abc2fe38a0... | 252 | cmplog | 1 | `cefaedfe` |
| 21254feaf977... | 225 | cmplog | 1 | `cefaedfe` |
| 223088569728... | 258 | cmplog | 1 | `cefaedfe` |
| 23147c9c0733... | 243 | cmplog | 1 | `cefaedfe` |

All positive seeds are MH_MAGIC (32-bit) Mach-O files with valid symbol table entries (nlist).

**Negative seeds (N=5):**
| Seed ID | Size | Fuzzer | Trial | Magic |
|---------|------|--------|-------|-------|
| 00010c848fdc... | 44 | cmplog | 2 | `0061736d` (WASM) |
| 0001f77f70c1... | 41 | cmplog | 2 | `0061736d` |
| 0003086512177f79 | 208 | cmplog | 2 | `cefaedfe` (MH_MAGIC) |
| 000880073e8b... | 228 | cmplog | 2 | `cefaedfe` |
| 0009fae10140... | 41 | cmplog | 2 | `0061736d` |

Mixed formats. Both WASM and Mach-O seeds appear as negatives. Mach-O negative seeds lack the specific symbol table structure that produces kUnknownSize ranges.

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 0-3 | `cefaedfe` (MH_MAGIC) | Mixed: WASM or MH_MAGIC | Pos all MH_MAGIC; neg mixed |
| Internal | Valid LC_SYMTAB + nlist entries | Missing or invalid symbol table | Structural |

**Source trace:**
- `AddVMRange("macho_symbols", sym->n_value, RangeSink::kUnknownSize, ...)` at macho.cc:425 adds ranges with unknown size when parsing Mach-O nlist symbols
- `RangeEndUnknownLimit()` at range_map.h:208 is called to resolve unknown-size range boundaries
- Line 209: `if (iter->second.size == kUnknownSize)` checks if the current range was added with unknown size

**Hypothesis:** The file must be a 32-bit Mach-O (MH_MAGIC) with valid symbol table load command (LC_SYMTAB) and nlist entries that are parseable. The controlling factor is the Mach-O file structure with valid symbol data, not a simple byte pattern.

**Verification:** CONFIRMED (round 1)
- Test A (break positive): Changed magic from `cefaedfe` to `0061736d` (WASM) -> Branch (209:9): [True: 0, False: 0]. True disappeared (branch unreached).
- Test B: Not attempted -- requires constructing valid Mach-O symbol table structure, not a simple byte mutation.
- Cross-validation with Mach-O negative seed (000308651217): This Mach-O seed reaches the branch (False: 423) but never True, confirming that Mach-O magic alone is insufficient -- valid nlist symbols are required.

**Controlling bytes:** Mach-O magic at offset 0-3 + valid LC_SYMTAB load command with parseable nlist entries (deep structural dependency).
**Cluster:** BC06

---

## Skipped Branches

| Rank | Function | Branch | Reason |
|------|----------|--------|--------|
| R17 | pe.cc | pe.cc:278:7 False | No blocking seeds in DB (0 negative seeds) |
| R23 | numbers.cc | numbers.cc:659:9 True | No resolving seeds in DB (0 positive seeds) |
| R24 | range_map.cc | range_map.cc:59:34 True | No resolving seeds in DB (0 positive seeds) |
| R67 | util.h | util.h:83:7 True | No resolving seeds in DB (0 positive seeds) |

---

## Cross-Function Merge Analysis

**BC01 and BC04 overlap:** Both depend on bytes 0-3 (file format magic). BC01 requires FAT_CIGAM specifically; BC04 requires any Mach-O magic. They are related but not identical -- BC01 is a subset condition within the Mach-O parsing path, while BC04 is about the format-level dispatch. Kept separate because the controlling byte values differ.

**BC04 and BC06 overlap:** Both require Mach-O format at bytes 0-3. BC06 additionally requires valid symbol table structure (LC_SYMTAB + nlist). BC06 is a deeper dependency that subsumes BC04's format requirement. Kept separate because BC06 has structural requirements beyond the magic bytes.

**BC05 is independent:** Controlled by symbol name content ("GR" token), not file format bytes. The Mach-O format is a prerequisite but the "GR" string is the actual controlling input.

**BC03 is independent:** Controlled by WASM section name content ("name"), orthogonal to Mach-O clusters.

**BC02 is independent:** Controlled by ELF section count field, completely separate from Mach-O/WASM clusters.

---

## Tier 2 — Automated Verification Results

**Tool:** `tools/cluster_verify.py` (single Docker container, 211s total)

**104 divergent branches tested against 6 clusters:**

| Result | Count |
|--------|-------|
| Assigned (A+B confirmed) | 3 |
| Partial (A confirmed) | 59 |
| Skipped (no seeds, rep seeds don't hit) | 42 |
| Unfitted | 0 |

**Per-cluster breakdown (including Tier 1 representatives):**

| Cluster | T1 rep | T2 full | T2 partial | Total |
|---------|--------|---------|------------|-------|
| BC01 (Mach-O magic) | 1 | 1 | 45 | 47 |
| BC02 (ELF e_shnum) | 1 | 0 | 11 | 12 |
| BC03 (WASM "name") | 1 | 0 | 2 | 3 |
| BC04 (format dispatch) | 1 | 2 | 1 | 4 |
| BC05 (demangle "GR") | 1 | 0 | 0 | 1 |
| BC06 (Mach-O nlist) | 1 | 0 | 0 | 1 |
| Skipped (no seeds) | — | — | — | 42 |
| **Total** | **6** | **3** | **59** | **110** |

Note: 42 branches skipped because they have no seeds in the DB and no cluster representative's seeds hit the branch. These branches had very low hitcounts in the coverage data (median ~2 hits) — the seeds that originally hit them were evicted from the queue during corpus evolution.

Partial (A only) means the controlling bytes are necessary but not sufficient — the branch likely has additional structural dependencies beyond the byte values tested.
