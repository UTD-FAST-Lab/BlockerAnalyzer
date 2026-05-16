│ Step 1: subject_significance.py — statistical significant subject (target x, fuzzer A, fuzzer B)          │
  │                                                                             │
  │   20 study_subjects total (5 targets × 4 canonical pairs)                   │
  │   12 accepted                                                             │
  │     bloaty:  2/4    lcms:    4/4    libpcap: 0/4 (dropped)                  │
  │     mbedtls: 2/4    sqlite3: 4/4   

 ┌─────────────────────────────────────────────────────────────────────────────┐
  │ Step 2: extract_blockers_ts.py + study_units.py — DB population             │
  │                                                                             │
  │                                                                             │
  │   subject_branches:         8,933 (subject, branch) rows                    │
  │     covers all 2,518 unique branches across 12 accepted subjects          

  │ Step 3: build_candidates.py — per-branch ≥7/≥7 rule                        │
  │   "winner_resolved ≥ 7 AND loser_blocked ≥ 7" per canonical pair            │
  │                                                                             │
  │   275 candidates  (one row per branch with ≥1 decisive pair)                │
  │     bloaty 35 │ lcms 203 │ mbedtls 2 │ sqlite3 35  (libpcap dropped)        │
  │                                                                             │
  │   Reduction: 2,518 → 275  (≈ 11% pass through)     

  │ Step 4: select_representatives.py — shape × region dedup                   │
  │   group_key = (decisive_shape, file, function, line // 50)   
      resolve >= 7 IS R, blocked >= 7 IS B, otherwise -
      line gap = 50 is the region bucket
  │   keep one rep per group (dur_div, hit_div)
  │                                                                             │
  │   158 representatives                                                       │
  │     bloaty 29 │ lcms 96 │ mbedtls 2 │ sqlite3 31                            │
  │                                                                             │
  │   Reduction: 275 → 158  (43% reduction; 117 dedup'd)             