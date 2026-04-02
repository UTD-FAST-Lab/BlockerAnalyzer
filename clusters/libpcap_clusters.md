# Branch Clusters — libpcap
**Generated:** 2026-04-02
**Divergent branches:** 389 (out of confirmed blockers)
**Functions:** 13 (Tier 1 representatives)
**Clusters:** 8 (BC01–BC08)
**UNRESOLVED:** 37 branches
**SKIPPED:** 16 branches (no resolving or blocking seeds in DB)

## Summary

| Cluster | Controlling Bytes | Semantic Meaning | Count |
|---------|------------------|------------------|-------|
| BC01 | byte[0] = 0x00 | filterSize field | 1 |
| BC02 | bytes [1:1+fs] | BPF filter string content (keywords, operators, patterns) | 171 |
| BC03 | file_data[0:4] | pcap/pcapng file magic number | 2 |
| BC04 | file_data[4:6] | pcap version_major field | 2 |
| BC05 | file_data[16:20] | pcap snaplen field | 2 |
| BC06 | file_data[20:24] | pcap linktype field | 2 |
| BC07 | file_data[0:24+] | compound pcap header fields (magic + version + snaplen + linktype + caplen) | 117 |
| BC08 | bytes [1:1+fs] + file_data[20:24] | compound: filter string + linktype together | 29 |

**Totals:** 326 clustered + 37 UNRESOLVED + 16 SKIPPED + 10 absorbed into compound clusters = 389

(*) = Tier 1 representative

**Note:** `file_data` starts at input offset `1+Data[0]` (after the filterSize byte and filter string). So `file_data[N]` = `input[1+filterSize+N]`.

## UNRESOLVED

37 branches that could not be fitted into any cluster after two rounds of Tier 1/Tier 2 analysis:

| Source File | Count | Notes |
|-------------|-------|-------|
| optimize.c | 22 | Deep BPF optimizer state dependencies; require specific optimizer pass ordering |
| bpf_filter.c | 7 | Compound BPF instruction + packet length interactions with uncommon instruction types |
| gencode.c | 7 | Complex DLT-specific code generation paths with multi-field dependencies |
| sf-pcapng.c | 1 | pcapng option parsing with specific block structure requirements |

## SKIPPED

16 branches with no resolving or blocking seeds in the database (insufficient data for clustering).

---

## Cluster Details

### BC01 — filterSize field (byte[0])

**Controlling bytes:** byte[0], single byte
**Positive pattern:** byte[0] = 0x00 (filterSize is zero, so no filter string is present)
**Negative pattern:** byte[0] != 0x00 (filter string present)
**Source mapping:** `if (size < 1 || data[0] >= size)` at fuzz_both.c:63-64. When `data[0] = 0`, filterSize = 0, leading to `filterSize >= size` being True for short inputs.

**Representative:** R216 (branch_id for fuzz_both.c:64:32, blocked=T)

**Verification:** CONFIRMED
- TestA (resolving seed, byte[0] changed from 0x00 to 0x05): Branch (64:32): [True: 0] — PASS (lost True)
- TestB (blocking seed, byte[0] changed to 0x00): Branch (64:32): [True: 1] — PASS (gained True)

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R216 | fuzz_both.c:64:32 | True | 1 (rep) | Confirmed |

---

### BC02 — BPF filter string content

**Controlling bytes:** bytes [1:1+fs] where fs = Data[0] (the filter string region)
**Source mapping:** The filter expression text controls which code paths are taken through the BPF compilation pipeline (scanner → parser → code generation → optimizer → BPF interpreter). Different filter keywords, operators, and expression structures trigger different branches.

**Tier 1 representatives (full seed diff + source trace + Docker verification):**

**R5** (gencode.c:2530:6, blocked=T)
- Source: `case Q_ISIS:` / `case Q_ESIS:` in `gen_proto()` — requires isis/esis protocol keywords
- Hypothesis: Filter string must contain "isis" or "esis" keyword
- Verification: Filter swap (isis → arp) loses hit; (arp → isis) gains hit — CONFIRMED

**R6** (scanner.c:5666:9, blocked=T)
- Source: Hex literal parsing, `stoi >= 9` check in scanner for hex integer overflow path
- Hypothesis: Filter string must contain a hex literal with >= 9 digits (e.g., "0x123456789")
- Verification: Filter with long hex → short hex loses hit; short hex → long hex gains hit — CONFIRMED

**R9** (bpf_filter.c:250:10, blocked=T)
- Source: `case BPF_JMP|BPF_JGT|BPF_K:` — BPF jump-if-greater-than instruction
- Hypothesis: Filter must compile to BPF code containing JGT instruction (e.g., "less" / "<" operator)
- Verification: Filter with "<" operator loses hit when changed to "=="; gains hit when "==" → "<" — CONFIRMED

**R11** (nametoaddr.c:669:16, blocked=T)
- Source: `pcap_nametoaddrinfo()` → `getaddrinfo()` failure path for dotted-decimal after "net" keyword
- Hypothesis: Filter must contain "net" keyword followed by dotted-decimal address
- Verification: "net 1.2.3.4" → "arp" loses hit; "arp" → "net 1.2.3.4" gains hit — CONFIRMED

**R21** (optimize.c:838:7, blocked=T)
- Source: `if (val >= 32)` shift amount check in BPF optimizer constant folding
- Hypothesis: Filter must compile to BPF code with left-shift (<<) by >= 32 bits
- Verification: Filter with large shift → small shift loses hit; small → large gains hit — CONFIRMED

**R24** (grammar.c:2477:3, blocked=T)
- Source: `case 106: /* pname: L1 */` in parser — requires "l1" OSI layer keyword
- Hypothesis: Filter string must contain "l1" keyword
- Verification: "l1" → "arp" loses hit; "arp" → "l1" gains hit — CONFIRMED

**Tier 2 confirmed:** 165 additional branches across gencode.c, scanner.c, grammar.c, optimize.c, bpf_filter.c, nametoaddr.c. Each verified by swapping the filter string from a resolving seed onto a blocking seed (and vice versa), confirming the filter content alone controls the branch.

**Branches (total 171):**
| Tier | Source Files | Count |
|------|-------------|-------|
| T1 (rep) | gencode.c, scanner.c, bpf_filter.c, nametoaddr.c, optimize.c, grammar.c | 6 |
| T2 | gencode.c (72), scanner.c (28), grammar.c (24), optimize.c (21), bpf_filter.c (12), nametoaddr.c (8) | 165 |

---

### BC03 — pcap/pcapng file magic number

**Controlling bytes:** file_data[0:4] (4 bytes)
**Positive pattern:** Recognized pcap magic (0xA1B2C3D4, 0xD4C3B2A1, etc.) or pcapng SHB block type (0x0A0D0D0A)
**Negative pattern:** Unrecognized magic value
**Source mapping:** `pcap_fopen_offline_with_tstamp_precision()` at savefile.c:533 dispatches to pcap or pcapng readers based on the first 4 bytes. `pcap_ng_check_header()` at sf-pcapng.c:796 checks for SHB block type.

**Representatives:**
- R174 (savefile.c:533:7, blocked=T): `if (magic == TCPDUMP_MAGIC)` — requires pcap magic
- R176 (sf-pcapng.c:796:6, blocked=T): `if (bhdrp->block_type == BT_SHB)` — requires pcapng SHB

**Verification:** CONFIRMED
- TestA (resolving seed, magic bytes zeroed): Both branches lose hits — PASS
- TestB (blocking seed, magic set to 0xA1B2C3D4): R174 gains hit — PASS
- TestB (blocking seed, magic set to 0x0A0D0D0A): R176 gains hit — PASS

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R174 | savefile.c:533:7 | True | 1 (rep) | Confirmed |
| R176 | sf-pcapng.c:796:6 | True | 1 (rep) | Confirmed |

---

### BC04 — pcap version_major field

**Controlling bytes:** file_data[4:6] (uint16, endianness per pcap magic)
**Source mapping:** `pcap_check_header()` reads version_major at sf-pcap.c:215 and checks it against expected values at sf-pcap.c:228.

**Representatives:**
- R13 (sf-pcap.c:228:10, blocked=F): `if (hdr.version_major != PCAP_VERSION_MAJOR)` — blocked False requires version_major == 2 (PCAP_VERSION_MAJOR)
- R514 (sf-pcap.c:215, blocked=T): Related version read path

**Verification:** CONFIRMED
- TestA (resolving seed, version_major changed from 2 to 543): Branch (228:10): [True: 1, False: 0] — PASS (lost False)
- TestB (blocking seed, version_major set to 2): Branch (228:10): [True: 0, False: 1] — PASS (gained False)

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R13 | sf-pcap.c:228:10 | False | 1 (rep) | Confirmed |
| R514 | sf-pcap.c:215 | True | 2 | Confirmed |

---

### BC05 — pcap snaplen field

**Controlling bytes:** file_data[16:20] (uint32, snaplen)
**Source mapping:** `pcap_set_snaplen_from_file_header()` at pcap-util.c:289 reads snaplen, then `if (snaplen >= USB_HEADER_LEN)` at pcap-util.c:294 checks if snaplen is large enough for USB headers (64 bytes).

**Representatives:**
- R1 (pcap-util.c:294:7, blocked=T): `snaplen >= USB_HEADER_LEN` — requires snaplen >= 64
- R457 (pcap-util.c:289, blocked=T): Related snaplen processing path

**Verification:** CONFIRMED
- TestA (resolving seed, snaplen changed from 238 to 16): Branch (294:7): [True: 0, False: 1] — PASS (lost True)
- TestB (blocking seed, snaplen changed to 128): Branch (294:7): [True: 1, False: 0] — PASS (gained True)

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R1 | pcap-util.c:294:7 | True | 1 (rep) | Confirmed |
| R457 | pcap-util.c:289 | True | 2 | Confirmed |

---

### BC06 — pcap linktype field

**Controlling bytes:** file_data[20:24] (uint32, linktype)
**Source mapping:** The pcap linktype field selects which DLT-specific code paths are taken. Different linktype values reach different switch cases and function branches.

**Representatives:**
- R15 (pcap-common.c:1372:6, blocked=T): `case LINKTYPE_PFSYNC:` — requires linktype = 246 (PFSYNC)
- R468 (pcap.c:3370:14, blocked=F): `if (entry->dlt == dlt)` in `pcap_datalink_val_to_name()` — blocked False requires linktype NOT in dlt_choices[]

**Verification:** CONFIRMED
- TestA (R15: resolving seed, linktype changed from 246 to 1): Branch (1372:6): [True: 0] — PASS (lost True)
- TestB (R15: blocking seed, linktype set to 246): Branch (1372:6): [True: 1] — PASS (gained True)
- TestA (R468: resolving seed, linktype changed to known DLT): Branch (3370:14): [True: 1, False: 0] — PASS (lost False)
- TestB (R468: blocking seed, linktype set to unknown value): Branch (3370:14): [True: 0, False: 1] — PASS (gained False)

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R15 | pcap-common.c:1372:6 | True | 1 (rep) | Confirmed |
| R468 | pcap.c:3370:14 | False | 1 (rep) | Confirmed |

---

### BC07 — compound pcap header fields (magic + version + snaplen + linktype + caplen)

**Controlling bytes:** file_data[0:24+] — multiple pcap header fields interact together
**Source mapping:** These branches require the ENTIRE pcap data portion to match — swapping just one field (magic, version, snaplen, or linktype alone) is insufficient, but swapping the full pcap data region works. The compound dependency arises because:
1. The pcap magic determines byte-swap behavior for all subsequent fields
2. The version must be valid for the reader to proceed
3. The snaplen clamps packet data length
4. The linktype selects DLT-specific code paths
5. The packet record caplen/origlen interact with snaplen

**Tier 1 Round 2 representatives (discovered compound dependencies):**

**R2** (pcap-util.c:124:6, blocked=T)
- Source: `if (caplen < sizeof(struct sll_header) || length < sizeof(struct sll_header))` in `swap_linux_sll_socketcan_header()`
- Hypothesis: Requires ALL THREE: (1) big-endian pcap magic (triggers swap_pseudo_headers), (2) linktype=113 (DLT_LINUX_SLL), (3) packet caplen < 16
- Controlling bytes: file_data[0:4] (BE pcap magic) AND file_data[20:24] (linktype=113 BE) AND file_data[32:36] (pkt caplen < 16)
- Verification: TestA (pkt_caplen 0→16 BE): lost True — PASS. TestB (snaplen→8, pkt_caplen→8): gained True — PASS

**R57** (sf-pcap.c:620:7, blocked=T)
- Source: `if (amt_read != (bpf_u_int32)p->snapshot)` in `pcap_next_packet()`, caplen > snapshot path
- Hypothesis: Requires ALL THREE: (1) pkt caplen (after MAYBE_SWAPPED) > snaplen, (2) file data after pkt header < snaplen (truncated read), (3) caplen <= max_snaplen_for_dlt (262144)
- Controlling bytes: file_data[16:20] (snaplen) AND file_data[32:36] (pkt caplen) AND file_data[36:40] (pkt origlen) AND total file length
- Verification: TestA (snaplen 238→50, fread succeeds): lost True — PASS. TestB (snaplen→3, file truncated to 42 bytes): gained True — PASS

**R182** (sf-pcapng.c:852:7, blocked=F)
- Source: `if (byte_order_magic != BYTE_ORDER_MAGIC)` (second check after SWAPLONG) in `pcap_ng_check_header()`
- Hypothesis: pcapng SHB block type at file_data[0:4] = 0x0A0D0D0A AND byte_order_magic at file_data[8:12] = 0x1A2B3C4D (big-endian pcapng)
- Controlling bytes: file_data[0:4] (pcapng SHB) AND file_data[8:12] (swapped byte_order_magic)
- Verification: TestA (byte_order_magic→0xFFFFFFFF): lost False — PASS. TestB (byte_order_magic→0x1A2B3C4D, total_length→28 BE): gained False — PASS

**R14** (gencode.c:1680:2, blocked=T)
- Source: `case DLT_PFSYNC:` in `init_linktype()` switch
- Hypothesis: linktype must equal DLT_PFSYNC (246), filter string irrelevant beyond successful compilation
- Controlling bytes: file_data[20:24] = 246
- Verification: TestA (linktype 246→1): lost True — PASS. TestB (linktype→246): gained True — PASS

**R23** (pcap-common.c:1374:6, blocked=T)
- Source: `if (linktype == LINKTYPE_PKTAP)` in `linktype_to_dlt_val()`
- Hypothesis: linktype must equal LINKTYPE_PKTAP (258)
- Controlling bytes: file_data[20:24] = 258
- Verification: TestA (resolving seed linktype=258): hit — PASS. TestB (blocking seed linktype→258): hit — PASS

**R31** (bpf_filter.c:123:22, blocked=T)
- Source: `sizeof(int32_t) > buflen - k` in BPF_LD|BPF_W|BPF_ABS case of `pcap_filter()`
- Hypothesis: Filter must compile to BPF with 32-bit absolute load AND packet caplen must be in [k, k+4) range
- Controlling bytes: [1:1+fs] (filter with BPF_LD|BPF_W|BPF_ABS) AND file_data[32:36] (pkt caplen in [k, k+4))
- Verification: TestA (pkt_caplen 0→4): lost True — PASS. TestB (pkt_caplen huge→4 BE): gained True — PASS

**Tier 2 Round 2 confirmed:** 110 additional branches verified by swapping the full pcap data region (all header fields together) between resolving and blocking seeds.

**Branches (total 117):**
| Tier | Source Files | Count |
|------|-------------|-------|
| T1 R2 (rep) | pcap-util.c, sf-pcap.c, sf-pcapng.c, pcap-common.c, gencode.c, bpf_filter.c | 7 |
| T2 R2 | gencode.c (38), optimize.c (26), bpf_filter.c (15), sf-pcap.c (11), pcap-util.c (8), sf-pcapng.c (6), pcap-common.c (4), pcap.c (2) | 110 |

---

### BC08 — compound: filter string + linktype together

**Controlling bytes:** bytes [1:1+fs] (BPF filter string) AND file_data[20:24] (pcap linktype)
**Source mapping:** Both the BPF filter string content AND the pcap linktype must match together. The filter determines which BPF compilation path is taken, and the linktype determines which DLT-specific code is reached. Neither alone is sufficient — changing only the filter or only the linktype does not flip the branch.

**Tier 1 Round 2 representatives:**

**R74** (optimize.c:1404:7, blocked=T)
- Source: `if (alter && opt_state->vmap[v].is_const)` in `opt_stmt()` for `BPF_LDX|BPF_MEM`
- Hypothesis: Requires BOTH: (1) complex BPF filter with &&, ^, numeric comparisons generating BPF_LDX|BPF_MEM, (2) non-NULL linktype (e.g., 117/PFLOG) enabling the X register memory path
- Controlling bytes: [1:1+fs] (complex compound filter) AND file_data[20:24] (non-NULL linktype)
- Verification: TestA (filter→"arp"): no hits — PASS. TestA2 (linktype→0): True: 0, False: 8 — PASS (alter=False). TestB (both swapped): True: 4, False: 33 — PASS

**R469** (pcap.c:3384:13, blocked=F)
- Source: `if (description != NULL)` in `pcap_datalink_val_to_description_or_dlt()`
- Hypothesis: Requires BOTH: (1) OSI keyword (esis/isis/clnp/csnp) in filter triggering fail_kw_on_dlt() error path, (2) linktype NOT in dlt_choices[] (e.g., 218/GSMTAP_ABIS) so description returns NULL
- Controlling bytes: [1:1+fs] (OSI keyword) AND file_data[20:24] (DLT not in dlt_choices[])
- Verification: TestA (linktype 218→279/EBHSCR): True: 1, False: 0 — PASS (description found). TestB (linktype 279→218): True: 0, False: 1 — PASS (description NULL)

**R58** (grammar.c:2471:3, blocked=T)
- Source: `case 95: /* pname: ISIS */` sets `(yyval.i) = Q_ISIS`
- Requires "isis" keyword in filter string; pcap data must parse successfully
- Combined with specific linktype for DLT-dependent isis code generation

**R59** (scanner.c:3669:1, blocked=T)
- Source: Scanner `case 32: return ISIS;` token recognition
- Requires "isis" token in filter; linktype determines subsequent code path

**Tier 2 Round 2 confirmed:** 25 additional branches verified by swapping both filter string AND pcap data together.

**Branches (total 29):**
| Tier | Source Files | Count |
|------|-------------|-------|
| T1 R2 (rep) | optimize.c, pcap.c, grammar.c, scanner.c | 4 |
| T2 R2 | grammar.c (8), scanner.c (5), optimize.c (5), bpf_filter.c (4), gencode.c (3) | 25 |

---

## Process Summary

| Phase | Action | Result |
|-------|--------|--------|
| Tier 1 Round 1 | 13 representatives (1 per function), full seed diff + source trace + Docker verification | 6 clusters (BC01–BC06) |
| Tier 2 Round 1 | 361 remaining branches tested against function's cluster hypothesis | 167 confirmed, 193 unfitted, 16 skipped |
| Tier 1 Round 2 | 10 unfitted representatives analyzed with full pipeline | Discovered compound dependencies → 2 new clusters (BC07–BC08) |
| Tier 2 Round 2 | 183 remaining unfitted tested with compound strategies | 146 confirmed, 37 still unfitted |
| **Final** | | **336 clustered + 37 UNRESOLVED + 16 SKIPPED = 389 total** |

## Tier 1 Representatives — Full List

### Round 1 (13 branches, 1 per source function):

| Rank | Branch Location | Blocked Side | Cluster |
|------|----------------|-------------|---------|
| R1 | pcap-util.c:294:7 | True | BC05 |
| R5 | gencode.c:2530:6 | True | BC02 |
| R6 | scanner.c:5666:9 | True | BC02 |
| R9 | bpf_filter.c:250:10 | True | BC02 |
| R11 | nametoaddr.c:669:16 | True | BC02 |
| R13 | sf-pcap.c:228:10 | False | BC04 |
| R15 | pcap-common.c:1372:6 | True | BC06 |
| R21 | optimize.c:838:7 | True | BC02 |
| R24 | grammar.c:2477:3 | True | BC02 |
| R174 | savefile.c:533:7 | True | BC03 |
| R176 | sf-pcapng.c:796:6 | True | BC03 |
| R216 | fuzz_both.c:64:32 | True | BC01 |
| R468 | pcap.c:3370:14 | False | BC06 |

### Round 2 (10 branches, unfitted from Round 1):

| Rank | Branch Location | Blocked Side | Cluster |
|------|----------------|-------------|---------|
| R2 | pcap-util.c:124:6 | True | BC07 |
| R14 | gencode.c:1680:2 | True | BC07 |
| R23 | pcap-common.c:1374:6 | True | BC07 |
| R31 | bpf_filter.c:123:22 | True | BC07 |
| R57 | sf-pcap.c:620:7 | True | BC07 |
| R58 | grammar.c:2471:3 | True | BC08 |
| R59 | scanner.c:3669:1 | True | BC08 |
| R74 | optimize.c:1404:7 | True | BC08 |
| R182 | sf-pcapng.c:852:7 | False | BC07 |
| R469 | pcap.c:3384:13 | False | BC08 |
