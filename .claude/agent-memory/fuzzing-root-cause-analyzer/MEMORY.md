# Agent Memory Index

## Reference

- [Fuzzer Knowledge Base](fuzzer_knowledge_base.md) — LibAFL FuzzBench fuzzer variant designs (naive, cmplog, value_profile, value_profile_cmplog): component matrix, mutation strategies, 3 known barrier types with per-fuzzer performance, diagnostic framework for root cause analysis.

## Project Memories

- [htslib project context](project_htslib.md) — Entry point, format detection gate, CRAM/SAM barriers, blocking branch findings and mitigations from 2026-03-17 campaign.
- [harfbuzz project context](project_harfbuzz.md) — GSUB ligature IS_LIG_BASE blocking branch, cmplog vs n4 seed divergence, font structure constraint findings from 2026-03-19 campaign.
- [lcms project context](project_lcms.md) — BC01 ICC 'Lab ' magic value (branch_ids 358+143), I2S resolves, naive/value_profile blocked 11.8h/12h; fix = Lab  seed or dictionary token. 2026-04-03 campaign.
