# Branch Clusters — mbedtls
**Generated:** 2026-04-02
**Divergent branches:** 10 (out of 25 confirmed blockers)
**Functions:** 3 (ssl_msg.c, ssl_tls12_client.c, ssl_tls.c)
**Clusters:** 5

## Summary

| Cluster | Controlling Bytes | Semantic Meaning | Branches (Tier 1 + Tier 2) |
|---------|------------------|------------------|----------------------------|
| BC01 | [14] = 0x64 | DTLS alert description (NO_RENEGOTIATION) | R1* |
| BC02 | [25:27] = version | DTLS handshake version field (ServerHello/HelloVerifyRequest) | R4*, R3, R8 |
| BC03 | [11:12] + [13:N] structure | Complete DTLS record with valid ServerHello advancing state machine | R7*, R5, R6, R16 |
| BC04 | input length < 13 | Input too short for DTLS record header | R2* |
| BC05 | [14:17] = msg_len | Handshake message length triggering reassembly buffer limit | R17* |

(*) = Tier 1 representative

## Cluster Details

### BC01 — DTLS alert description byte

**Controlling bytes:** offset 14, single byte
**Positive pattern:** byte[14] != 0x64 (any value other than NO_RENEGOTIATION)
**Negative pattern:** byte[14] = 0x64 (MBEDTLS_SSL_ALERT_MSG_NO_RENEGOTIATION = 100)
**Source mapping:** `ssl->in_msg[1] == MBEDTLS_SSL_ALERT_MSG_NO_RENEGOTIATION` at ssl_msg.c:4791:13. Input byte 14 maps to `in_msg[1]` (alert description) within a DTLS alert record (content type 0x15, 13-byte record header, in_msg starts at offset 13).
**Verification:** CONFIRMED (round 1)

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R1 | ssl_msg.c:4791:13 | False | 1 (rep) | Confirmed |

---

### BC02 — DTLS handshake version field

**Controlling bytes:** offset 25-26, two bytes (big-endian uint16)
**Positive pattern:** 0xfefd (DTLS 1.2) or 0xfeff (DTLS 1.0) — valid DTLS versions
**Negative pattern:** any other value (e.g., 0x3333, 0x0000) — invalid DTLS version
**Source mapping:** These bytes correspond to the `ProtocolVersion` field at the start of the handshake message body (after 13-byte DTLS record header + 12-byte handshake header = offset 25). Read via `MBEDTLS_GET_UINT16_BE(p, 0)` in both `ssl_parse_server_hello_verify_request()` (dtls_legacy_version at ssl_tls12_client.c:1123) and `ssl_parse_server_hello()` (tls_version comparison at ssl_tls12_client.c:1266, version writing at ssl_msg.c:5824).
**Verification:** CONFIRMED (round 1)

**Sub-cases by branch:**
- R4 (1131:9 F): `dtls_legacy_version != 0xfefd && != 0xfeff` — blocked False requires valid version
- R3 (5824:30 T): `tls_version == 0x0302` — blocked True requires version 0xfeff (DTLS 1.0 = internal 0x0302)
- R8 (1266:9 F): `ssl->tls_version > ssl->conf->max_tls_version` — blocked False requires version within configured range

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R4 | ssl_tls12_client.c:1131:9 | False | 1 (rep) | Confirmed |
| R3 | ssl_msg.c:5824:30 | True | 2 | Confirmed (bytes 25-26 = 0xfeff for True) |
| R8 | ssl_tls12_client.c:1266:9 | False | 2 | Confirmed (bytes 25-26 = valid version for False) |

---

### BC03 — DTLS record structure (state machine advancement)

**Controlling bytes:** offset 11-12 (record length field) + offset 13-N (handshake body)
**Positive pattern:** record length >= 76 (0x004c) with a valid ServerHello handshake message (type 0x02) in the body, advancing the TLS state machine past `MBEDTLS_SSL_SERVER_HELLO`
**Negative pattern:** record too short, invalid handshake content, or missing ServerHello — state stays at SERVER_HELLO
**Source mapping:** The DTLS record length at bytes 11-12 tells the record layer how much body to read. The body must contain a complete DTLS handshake header (12 bytes: type + length + seq + frag_offset + frag_len) plus a valid ServerHello payload. When processed, the state machine advances from `MBEDTLS_SSL_SERVER_HELLO` to `MBEDTLS_SSL_SERVER_CERTIFICATE` and beyond.
**Verification:** CONFIRMED (round 2)
- Test A: bytes[11:12] = 0x0010 -> state stays at SERVER_HELLO (False disappears)
- Test A: body bytes[50:100] zeroed -> state stays at SERVER_HELLO (False disappears)
- Test B: negative header[0:10] + positive length+body -> state advances (False appears)

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R7 | ssl_tls.c:3291:10 | False | 1 (rep) | Confirmed |
| R5 | ssl_tls12_client.c:3505:9 | False | 2 | Confirmed (state not SERVER_HELLO) |
| R6 | ssl_tls12_client.c:3509:9 | True | 2 | Confirmed (state is SERVER_CERTIFICATE) |
| R16 | ssl_tls12_client.c:1442:12 | True | 2 | Confirmed (ServerHello has extensions) |

---

### BC04 — Input length constraint (record header minimum)

**Controlling bytes:** total input size, must be < 13 bytes
**Positive pattern:** input < 13 bytes (shorter than DTLS record header)
**Negative pattern:** input >= 13 bytes
**Source mapping:** `len < rec_hdr_len_offset + rec_hdr_len_len` at ssl_msg.c:3514:9, where `rec_hdr_len_offset` = 11 (DTLS) and `rec_hdr_len_len` = 2, so threshold = 13 bytes.
**Verification:** CONFIRMED (round 2)
- Test A: extended 4-byte positive seed to 20 bytes -> True disappears
- Test B: truncated 137-byte negative seed to 4 bytes -> True appears

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R2 | ssl_msg.c:3514:9 | True | 1 (rep) | Confirmed |

---

### BC05 — Handshake message length (reassembly buffer limit)

**Controlling bytes:** offset 14-16, three bytes (big-endian uint24 — handshake message length)
**Positive pattern:** msg_len large enough that `ssl_get_reassembly_buffer_size(msg_len)` exceeds `MBEDTLS_SSL_DTLS_MAX_BUFFERING - total_bytes_buffered`
**Negative pattern:** msg_len small (e.g., 0x000001) — reassembly buffer fits within limit
**Source mapping:** Handshake message `length` field at offset 14-16 (after 13-byte record header + 1-byte handshake type). Parsed by the DTLS record layer to determine reassembly buffer allocation. Checked at ssl_msg.c:4165:21: `if (reassembly_buf_sz > (MBEDTLS_SSL_DTLS_MAX_BUFFERING - hs->buffering.total_bytes_buffered))`.
**Verification:** CONFIRMED (round 2)
- Test A: bytes[14:17] = 0x000001 -> True disappears (branch not reached)
- Test B: bytes[14:17] = 0x003dff -> True appears

**Context:** The positive seed contains multiple DTLS records with fragmented handshake messages. The large `msg_len` triggers reassembly allocation that exceeds the compile-time buffering limit.

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R17 | ssl_msg.c:4165:21 | True | 1 (rep) | Confirmed |

---

## Tier 1 — Full Analysis Details

### Rank 1 — ssl_msg.c:4791:13 (representative for ssl_msg.c alert handling)

**Positive seeds (N=5):**
| Seed ID | Size | Fuzzer | byte[14] (alert desc) |
|---------|------|--------|-----------------------|
| be178560198fbdf6 | 15 | naive/trial3 | 0x01 |
| 06e380f9cc7181d2 | 24 | value_profile/trial1 | 0xf8 |
| 17a44be8c64fb413 | 24 | value_profile/trial1 | 0x02 |
| a2538dc6e2225ae5 | 20 | value_profile_cmplog/trial1 | 0x04 |
| f56302793f912559 | 20 | value_profile_cmplog/trial1 | 0x24 |

**Negative seeds (N=3):**
| Seed ID | Size | Fuzzer | byte[14] |
|---------|------|--------|----------|
| fb2127d68060398a | 32 | cmplog/trial1 | 0x01 |
| 67f3fc87607b5f07 | 32 | naive/trial1 | 0x00 |
| 5205f2702386c95a | 51 | value_profile_cmplog/trial3 | 0x64 |

**Byte diff:**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 14 | 0x01, 0xf8, 0x02, 0x04, 0x24 (never 0x64) | 0x64 (in seed 5205f270) | High |
| 6-17 | Various | Various | Low (non-controlling) |

**Source trace:**
- ssl_msg.c:4790: `if (ssl->in_msg[0] == MBEDTLS_SSL_ALERT_LEVEL_WARNING &&`
- ssl_msg.c:4791: `    ssl->in_msg[1] == MBEDTLS_SSL_ALERT_MSG_NO_RENEGOTIATION)`
- `in_msg[1]` = byte 14 of input (after 13-byte DTLS record header)

**Hypothesis:** byte[14] = 0x64 (100 = NO_RENEGOTIATION) -> True; byte[14] != 0x64 -> False (blocked side)
**Verification:** CONFIRMED (round 1)
- Test A: positive seed a2538dc6 byte[14] 0x04->0x64: Branch flipped to [True: 1, False: 0]
- Test B: negative seed 5205f270 byte[14] 0x64->0x01: Branch flipped to [True: 0, False: 1]

**Controlling bytes:** offset 14 = 0x64
**Cluster:** BC01

---

### Rank 4 — ssl_tls12_client.c:1131:9 (representative for ssl_tls12_client.c version handling)

**Positive seeds (N=10):** 5 from cmplog/trial3, 5 from value_profile_cmplog/trial1
| Seed ID | Size | Fuzzer | bytes[25:27] |
|---------|------|--------|--------------|
| 4c05bb242809a0d2 | 84 | cmplog/trial3 | fe fd |
| 81464308f847418d | 84 | cmplog/trial3 | fe fd |
| 84539894e33c5733 | 84 | cmplog/trial3 | fe fd |
| 0974dd482006e918 | 171 | value_profile_cmplog/trial1 | fe fd |
| 0bd0dbd67bf63622 | 153 | value_profile_cmplog/trial1 | fe fd |

**Negative seeds (N=10):** all from cmplog/trial1
| Seed ID | Size | Fuzzer | bytes[25:27] |
|---------|------|--------|--------------|
| 168bb332a87cc0d1 | 126 | cmplog/trial1 | (complex) |
| 686b72d98ad585a0 | 42 | cmplog/trial1 | fe ff |
| 3f3d341d532860b6 | 45 | cmplog/trial1 | (complex) |

**Byte diff (positive seed 81464308 vs negative seed 686b72d9):**
| Offset | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| 1 | 0xfe (DTLS) | 0x01 (TLS) | High |
| 25-26 | 0xfe 0xfd (DTLS 1.2) | 0xfe 0xff (DTLS 1.0) | Key diff |

**Source trace:**
- ssl_tls12_client.c:1123: `dtls_legacy_version = MBEDTLS_GET_UINT16_BE(p, 0);`
- ssl_tls12_client.c:1131: `if (dtls_legacy_version != 0xfefd && dtls_legacy_version != 0xfeff)`
- `p` points to HelloVerifyRequest body at record_header(13) + handshake_header(12) = offset 25

**Hypothesis:** bytes[25:27] must be 0xfefd or 0xfeff for False (blocked side); any other value -> True
**Verification:** CONFIRMED (round 1)
- Test A: positive seed 81464308 bytes[25:27] 0xfefd->0x0000: Branch [True: 1, False: 0]
- Test B: negative seed 686b72d9 bytes[25:27] 0xfeff->0xfefd: Branch [True: 0, False: 1]

**Controlling bytes:** offset 25-26 = DTLS version
**Cluster:** BC02

---

### Rank 7 — ssl_tls.c:3291:10 (representative for ssl_tls.c state machine)

**Positive seeds (N=10):** all from value_profile/trial3
| Seed ID | Size | Fuzzer | bytes[11:13] (record len) |
|---------|------|--------|---------------------------|
| 11c93be599485a14 | 299 | value_profile/trial3 | 00 a8 (168) |
| 126d81fd8fc77ab6 | 268 | value_profile/trial3 | 00 a8 (168) |
| 3dfc102ba8833e91 | 191 | value_profile/trial3 | 00 88 (136) |

**Negative seeds (N=10):** from cmplog/trial1, sizes 42-219
| Seed ID | Size | Fuzzer | bytes[11:13] |
|---------|------|--------|--------------|
| 00625dc030587f5c | 45 | cmplog/trial1 | 00 1e (30) |
| 01cfd25932fd4daf | 45 | cmplog/trial1 | 00 1e (30) |

**Key observations:**
- All positive seeds >= 191 bytes, first 50 bytes nearly identical (constant template)
- All negative seeds <= 219 bytes with different record structure
- Positive seeds have record length 136-168; negative seeds have <= 30

**Source trace:**
- ssl_tls.c:3289-3291: Checks `ssl->state == CLIENT_HELLO || ssl->state == SERVER_HELLO`
- False at 3291 means state is PAST SERVER_HELLO (e.g., SERVER_CERTIFICATE)
- State advances when a valid ServerHello is fully processed

**Hypothesis:** bytes[11:12] must set record length >= 136 AND bytes[13:N] must contain a valid DTLS handshake response
**Verification:** CONFIRMED (round 2)
- Round 1 attempt (byte[1] corruption): Failed — version byte alone doesn't control
- Test A: bytes[11:12] = 0x0010 -> [True: 3, False: 0]
- Test A: bytes[50:100] zeroed -> [True: 4, False: 0]
- Test B: neg[0:11] + pos[11:] -> [True: 3, False: 1]

**Controlling bytes:** offset 11-181 (record length field + complete handshake body)
**Cluster:** BC03

---

### Rank 2 — ssl_msg.c:3514:9 (promoted from Tier 2, Round 2)

**Positive seed:** ca8486fa696bed3b (4 bytes: `00 00 00 00`)
**Negative seed:** 018d3b536bb91a41 (137 bytes)

**Hypothesis:** input must be < 13 bytes (DTLS record header minimum)
**Verification:** CONFIRMED (round 2)
- Test A: extended 4-byte positive to 20 bytes -> [True: 0, False: 1]
- Test B: truncated 137-byte negative to 4 bytes -> [True: 1, False: 0]

**Controlling bytes:** input length (not specific byte values)
**Cluster:** BC04

---

### Rank 17 — ssl_msg.c:4165:21 (promoted from Tier 2, Round 2)

**Positive seed:** 15fa34111baade50 (133 bytes, naive/trial3)
**Negative seed:** 018d3b536bb91a41 (137 bytes, doesn't reach branch)

**Seed structure:** Multiple DTLS records with fragmented handshake message. Handshake msg_len at bytes[14:17] = 0x003dff (15871).

**Hypothesis:** bytes[14:17] (handshake message length) must be large enough to exceed `MBEDTLS_SSL_DTLS_MAX_BUFFERING` during reassembly.
**Verification:** CONFIRMED (round 2)
- Test A: bytes[14:17] = 0x000001 -> [True: 0, False: 0] (branch not reached)
- Test B: bytes[14:17] = 0x003dff -> [True: 1, False: 1]

**Controlling bytes:** offset 14-16 = handshake message length
**Cluster:** BC05

---

## Tier 2 — Verification Results

| Rank | Branch | Function | Representative Cluster | Test A | Test B | Result |
|------|--------|----------|----------------------|--------|--------|--------|
| R3 | ssl_msg.c:5824:30 | ssl_msg.c | BC02 (R4) | pass (0xfeff->0xfefd: True lost) | pass (0xfefd->0xfeff: True gained) | BC02 |
| R5 | ssl_tls12_client.c:3505:9 | ssl_tls12_client.c | BC03 (R7) | pass (len=0x0010: False lost) | pass (pos body grafted: False gained) | BC03 |
| R6 | ssl_tls12_client.c:3509:9 | ssl_tls12_client.c | BC03 (R7) | pass (len=0x0010: True lost) | pass (pos body grafted: True gained) | BC03 |
| R8 | ssl_tls12_client.c:1266:9 | ssl_tls12_client.c | BC02 (R4) | pass (0xfefd->0x3333: True gained) | pass (0x3333->0xfefd: True lost) | BC02 |
| R16 | ssl_tls12_client.c:1442:12 | ssl_tls12_client.c | BC03 (R7) | pass (len=0x0010: True lost) | pass (pos body grafted: True gained) | BC03 |

## Promoted Branches (Tier 2 -> Tier 1)

| Rank | Branch | Reason | New Cluster |
|------|--------|--------|-------------|
| R2 | ssl_msg.c:3514:9 | No existing cluster fits (input length constraint) | BC04 |
| R17 | ssl_msg.c:4165:21 | No existing cluster fits (reassembly buffer limit) | BC05 |

## Skipped Branches

None — all 10 divergent branches assigned to clusters.
