# Branch Cluster Agent Memory

- [lcms run 2026-04-03](lcms_20260403.md) — T1 all 3 batches complete for lcms; 11 clusters BC01-BC11 confirmed; 43/254 branches assigned; T2 batch 1 done
- [mbedtls DTLS version pattern](mbedtls_dtls_version_pattern.md) — branches 371+373: bytes[25:27] controls DTLS version checks; 371 (ssl_msg.c:5824 True) needs b[13]=0x02+feff; 373 (ssl_tls12_client.c:1131 False) needs b[13]=0x03+fefd/feff
- [mbedtls DTLS Alert renegotiation pattern](mbedtls_alert_renegotiation_pattern.md) — branch 370: byte[14]=0x64 controls DTLS Alert no-renegotiation check at ssl_msg.c:4791
