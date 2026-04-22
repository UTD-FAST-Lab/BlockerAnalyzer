# RCA Ontology Summary — cross-target root cause classification

Generated from 306 RCA reports across 5 targets (mbedtls, bloaty, sqlite3, lcms, libpcap).

Raw class names are agent-invented; this summary normalizes them into canonical families. See `raw classes` column for the agent-emitted labels.

## Reports per target


| target    | reports | tokens (sum)   | hours (sum) |
| --------- | ------- | -------------- | ----------- |
| mbedtls   | 7       | 446,812        | 0.8         |
| bloaty    | 25      | 1,443,084      | 2.7         |
| sqlite3   | 50      | 2,862,606      | 4.3         |
| lcms      | 76      | 4,677,582      | 8.2         |
| libpcap   | 148     | 9,091,186      | 12.9        |
| **total** | **306** | **18,521,270** | **28.9**    |


## Root-cause families (normalized)


| family                                                     | total | mbedtls | bloaty | sqlite3 | lcms | libpcap | high | medium | avg tokens | avg dur (s) | top winning pattern                             | top blocking pattern                      |
| ---------------------------------------------------------- | ----- | ------- | ------ | ------- | ---- | ------- | ---- | ------ | ---------- | ----------- | ----------------------------------------------- | ----------------------------------------- |
| `I2S_constant_match`                                       | 87    | 0       | 11     | 13      | 54   | 9       | 68   | 19     | 59,984     | 363         | cmplog,value_profile_cmplog                     | naive,value_profile                       |
| `synergy_cmplog_plus_vp`                                   | 51    | 1       | 8      | 9       | 16   | 17      | 24   | 27     | 62,027     | 367         | value_profile_cmplog                            | cmplog,naive,value_profile                |
| `structural_invariant_destruction`                         | 45    | 0       | 5      | 7       | 2    | 31      | 16   | 29     | 56,780     | 280         | naive,value_profile,value_profile_cmplog        | cmplog                                    |
| `jump_table_opacity`                                       | 39    | 0       | 0      | 1       | 0    | 38      | 28   | 11     | 58,035     | 262         | naive,value_profile,value_profile_cmplog        | cmplog                                    |
| `value_profile_hamming_gradient`                           | 30    | 5       | 0      | 11      | 0    | 14      | 5    | 25     | 61,089     | 341         | value_profile,value_profile_cmplog              | cmplog,naive                              |
| `I2S_corpus_composition_bias`                              | 22    | 0       | 0      | 4       | 0    | 18      | 6    | 16     | 65,944     | 389         | cmplog,naive,value_profile,value_profile_cmplog | —                                         |
| `I2S_switch_case_lock`                                     | 11    | 0       | 1      | 0       | 1    | 9       | 3    | 8      | 62,943     | 291         | naive,value_profile,value_profile_cmplog        | cmplog                                    |
| `I2S_inequality_substitution`                              | 5     | 0       | 0      | 2       | 0    | 3       | 4    | 1      | 53,223     | 299         | naive,value_profile,value_profile_cmplog        | cmplog                                    |
| `other_I2S_harm`                                           | 3     | 0       | 0      | 1       | 2    | 0       | 2    | 1      | 74,315     | 650         | naive,value_profile                             | cmplog,value_profile_cmplog               |
| `I2S_keyword_or_token`                                     | 2     | 0       | 0      | 0       | 0    | 2       | 0    | 2      | 63,540     | 437         | cmplog,naive,value_profile,value_profile_cmplog | —                                         |
| `experimental_artifact`                                    | 2     | 0       | 0      | 0       | 0    | 2       | 1    | 1      | 81,691     | 684         | value_profile_cmplog                            | cmplog,naive,value_profile                |
| `corpus_shape_or_volume`                                   | 2     | 0       | 0      | 0       | 0    | 2       | 0    | 2      | 52,090     | 288         | cmplog,naive,value_profile,value_profile_cmplog | —                                         |
| `I2S_equality_lock`                                        | 1     | 1       | 0      | 0       | 0    | 0       | 1    | 0      | 52,533     | 377         | naive,value_profile,value_profile_cmplog        | cmplog                                    |
| `I2S_accelerated_reach`                                    | 1     | 0       | 0      | 1       | 0    | 0       | 0    | 1      | 50,276     | 270         | cmplog,value_profile_cmplog                     | value_profile                             |
| `cmplog_throughput_overhead_and_cmpmap_queue_displacement` | 1     | 0       | 0      | 1       | 0    | 0       | 1    | 0      | 75,027     | 569         | naive                                           | cmplog,value_profile,value_profile_cmplog |
| `I2S_multi_mechanism_harm`                                 | 1     | 0       | 0      | 0       | 1    | 0       | 1    | 0      | 53,962     | 256         | naive,value_profile                             | cmplog,value_profile_cmplog               |
| `I2S_switch_value_lock_in`                                 | 1     | 0       | 0      | 0       | 0    | 1       | 1    | 0      | 58,042     | 258         | naive,value_profile,value_profile_cmplog        | cmplog                                    |
| `I2S_structural_or_root_seed`                              | 1     | 0       | 0      | 0       | 0    | 1       | 0    | 1      | 72,263     | 304         | cmplog,naive,value_profile,value_profile_cmplog | —                                         |
| `unknown`                                                  | 1     | 0       | 0      | 0       | 0    | 1       | 0    | 1      | 0          | 0           | value_profile_cmplog                            | cmplog,naive,value_profile                |


## Family details

### `I2S_constant_match` — 87 reports

**Description:** Input-to-state (I2S) matching of a specific multi-byte magic/signature/opcode constant. cmplog logs the CMP at runtime and substitutes the exact constant into the input byte that feeds the comparison. Without I2S, the constant is too sparse for random bytes to hit. Winning: cmplog (and value_profile_cmplog). Losing: naive and value_profile. The classic I2S-helps case.
**Confidence:** high=68, medium=19
**Top resolving fuzzers:** `cmplog,value_profile_cmplog` (53); `cmplog,value_profile,value_profile_cmplog` (23); `cmplog` (3)
**Top blocking fuzzers:** `naive,value_profile` (48); `naive` (27); `value_profile` (5)
**Raw class variants emitted by agents:**

- `I2S_constant_match` × 87
**Representative hypothesis statements:**
- Resolving the true branches requires matching one of three 32-bit Mach-O magic constants (0xfeedface, 0xfeedfacf, or 0xbebafeca) at the first 4 bytes of the input; cmplog's I2S stage directly substitutes the logged comparison operand into those bytes in a single step, while naive and value_profile-a
- The switch at line 121 dispatches on a 4-byte little-endian magic field (0xfeedface for MH_MAGIC or 0xfeedfacf for MH_MAGIC_64) read directly from the input; only cmplog-enabled fuzzers can log this comparison and substitute the exact constant, while naive and value_profile must blindly guess a 32-b
- ForEachLoadCommand() dispatches on a 32-bit magic number read from bytes [0:3] of the input; the required constants (MH_MAGIC=0xfeedface, MH_MAGIC_64=0xfeedfacf, FAT_CIGAM=0xbebafeca) are too sparse for random mutation to produce, but cmplog's I2S stage logs the switch comparison and directly substi
**Cost:** 5,218,644 total tokens over 87 matched jobs (avg 59,984/job, 363s/job).

### `synergy_cmplog_plus_vp` — 51 reports

**Description:** Two-condition barrier where neither I2S alone nor CMP_MAP gradient alone suffices. Typically one condition is a discrete constant/keyword (I2S solves) and the other needs stepping-stone retention (CMP_MAP provides). Only value_profile_cmplog holds both capabilities simultaneously. Examples: filter-keyword + DLT conjunction in libpcap, deep parser-chain reach in bloaty demangler.
**Confidence:** medium=27, high=24
**Top resolving fuzzers:** `value_profile_cmplog` (26); `cmplog,value_profile,value_profile_cmplog` (10); `naive,value_profile_cmplog` (8)
**Top blocking fuzzers:** `cmplog,naive,value_profile` (14); `naive` (12); `cmplog,value_profile` (9)
**Raw class variants emitted by agents:**

- `synergy_cmplog_plus_vp` × 51
**Representative hypothesis statements:**
- Advancing the DTLS handshake past SERVER_HELLO requires crafting a structurally valid ServerHello record; CMP_MAP feedback (value_profile) provides the gradient to navigate the multi-field TLS comparisons needed for ssl_parse_server_hello() to succeed, while I2S (cmplog) alone offers no measurable b
- The ParseExpression recursive descent parser requires two-char tokens ('fp', 'dt', 'pt') to appear at the exact parser cursor position within a structurally valid C++ mangled name; cmplog's I2S substitutions satisfy the byte comparisons locally but disrupt the surrounding parse structure, while valu
- Reaching the 'sr' alternates in ParseUnresolvedName requires a structurally valid Itanium-mangled symbol that survives a deep chain of prior parsing steps; value_profile_cmplog's CMP_MAP gradient retains near-valid corpus seeds as stepping stones, while cmplog alone (without the gradient) has its I2
**Cost:** 3,163,396 total tokens over 51 matched jobs (avg 62,027/job, 367s/job).

### `structural_invariant_destruction` — 45 reports

**Description:** Type 2 harm. A branch guard depends on a multi-instruction / cross-field / CFG invariant. I2S substitutes one comparand value to satisfy its local CMP but destroys the surrounding structural invariant, so downstream predicates fail. Winning: any non-I2S fuzzer (naive, value_profile, sometimes VPC because CMP_MAP retains valid structure). Losing: cmplog. Includes structural_reach_gap variants.
**Confidence:** medium=29, high=16
**Top resolving fuzzers:** `naive,value_profile,value_profile_cmplog` (14); `value_profile_cmplog` (6); `naive` (5)
**Top blocking fuzzers:** `cmplog` (20); `cmplog,value_profile,value_profile_cmplog` (5); `cmplog,naive,value_profile_cmplog` (5)
**Raw class variants emitted by agents:**

- `structural_invariant_destruction` × 18
- `structural_reach_gap` × 13
- `structural_invariant_I2S_corruption` × 4
- `I2S_structural_invariant_destruction` × 4
- `I2S_lock_in_structural_invariant` × 1
- `structural_invariant_I2S_destruction` × 1
- `I2S_keyword_substitution_plus_structural_reach_gap` × 1
- `structural_invariant_I2S_corpus_starvation` × 1
**Representative hypothesis statements:**
- cmplog's I2S pass locks the corpus into the first successful ParseSpecialName path (the 'T[VTISH]' branch at line 992) by repeatedly substituting its single/two-char token bytes, starving exploration of the later 'GV', 'TC', and 'GR' alternatives; value_profile_cmplog's CMP_MAP gradient retains step
- cmplog's I2S (redqueen) pass substitutes individual single-character comparison operands throughout the deeply recursive C++ demangling grammar (the many ParseOneCharToken comparisons for 'Z', 'N', 'E', 's', etc.), locally satisfying each character check but disrupting the holistic structural sequen
- The I2S redqueen pass in cmplog satisfies early token comparisons ('U','t'/'U','l') but positionally corrupts the terminal character ('_' or 'E') that must follow at a precise mangled-name offset, while value_profile_cmplog's CMP_MAP gradient provides incremental feedback that guides the full sequen
**Cost:** 2,555,107 total tokens over 45 matched jobs (avg 56,780/job, 280s/job).

### `jump_table_opacity` — 39 reports

**Description:** Type 8 harm. A large switch compiles to an indirect jump table with no per-case CMP instruction (DLT dispatch, BPF opcode dispatch, flex DFA, bison state table). I2S is completely blind to the dispatch and instead substitutes values from inside already-reached case bodies, locking the corpus out of unvisited cases. Winning: naive (random) and value_profile (CMP_MAP gradient inside case bodies). Losing: cmplog.
**Confidence:** high=28, medium=11
**Top resolving fuzzers:** `naive,value_profile,value_profile_cmplog` (26); `naive,value_profile_cmplog` (4); `cmplog,naive,value_profile,value_profile_cmplog` (4)
**Top blocking fuzzers:** `cmplog` (26); `value_profile` (4); `—` (4)
**Raw class variants emitted by agents:**

- `jump_table_opacity_I2S_lock_in` × 14
- `jump_table_opacity_I2S_lockout` × 4
- `jump_table_opacity_cmpmap_gradient` × 2
- `jump_table_opacity_cmp_map_gradient` × 1
- `jump_table_opacity_cmplog_lock_in` × 1
- `jump_table_opacity_cmplog_harm` × 1
- `jump_table_opacity_two_condition_reach` × 1
- `jump_table_opacity_DLT_corpus_lockout` × 1
**Representative hypothesis statements:**
- OP_BitAnd and OP_BitOr are dispatched via an indirect jump table in sqlite3VdbeExec with no explicit CMP instruction for the opcode field, making them invisible to I2S/cmplog; value_profile's CMP_MAP Hamming gradient on arithmetic inside neighboring case bodies provides the only stepping-stone signa
- The gen_linktype() switch on cstate->linktype (the pcap DLT field) is compiled as a jump table with no per-case CMP instructions; cmplog's I2S pass never sees the DLT dispatch and instead locks in filter-keyword comparisons it does intercept, producing a narrowly diversified corpus that misses the r
- The DLT_JUNIPER_* cases in gen_linktype() are reached only when cstate->linktype matches one of ~20 Juniper DLT constants; the switch is compiled as a jump table with no CMP instructions per case, so cmplog's I2S stage never sees the DLT dispatch and its corpus becomes locked into non-Juniper DLT va
**Cost:** 2,263,390 total tokens over 39 matched jobs (avg 58,035/job, 262s/job).

### `value_profile_hamming_gradient` — 30 reports

**Description:** CMP_MAP Hamming-distance feedback produces a progressive gradient toward a target comparand, letting value_profile converge where edge coverage alone stalls. Often the winning mechanism for multi-field TLS records, arithmetic thresholds, or character-level DFA approximation. Winning: value_profile and/or VPC. Losing: naive and cmplog (I2S has no CMP to log or actively harms via lock-in).
**Confidence:** medium=25, high=5
**Top resolving fuzzers:** `value_profile,value_profile_cmplog` (14); `cmplog,naive,value_profile,value_profile_cmplog` (6); `value_profile` (6)
**Top blocking fuzzers:** `cmplog,naive` (9); `naive` (6); `—` (6)
**Raw class variants emitted by agents:**

- `value_profile_hamming_gradient` × 25
- `value_profile_hamming_gradient_misleading` × 1
- `value_profile_corpus_diversity` × 1
- `cmp_map_gradient_false_attractor` × 1
- `value_profile_gradient_repulsion` × 1
- `value_profile_corpus_gradient_vs_I2S_throughput_penalty` × 1
**Representative hypothesis statements:**
- Reaching the SERVER_HELLO and SERVER_CERTIFICATE case labels requires the fuzzer input to constitute a structurally valid TLS 1.2 ServerHello record (type=0x16, version=0x0303, handshake-type=0x02, plus valid length fields and a recognized ciphersuite); value_profile's CMP_MAP feedback rewards input
- The tls_version field is a protocol-layer derived value produced by TLS handshake state parsing, not a byte directly lifted from raw input; cmplog I2S logs the comparison tls_version == 0x0302 but cannot identify which input bytes control tls_version so its substitutions corrupt unrelated bytes with
- The dim3 hitcount gap arises because CMP_MAP gradient feedback (value_profile variants) rewards byte-level progress toward valid DTLS record structures, enabling the handshake state machine to advance past SERVER_HELLO into later phases, whereas naive and cmplog fail to consistently produce or prese
**Cost:** 1,832,690 total tokens over 30 matched jobs (avg 61,089/job, 341s/job).

### `I2S_corpus_composition_bias` — 22 reports

**Description:** I2S substitution does not block the target branch directly — it reshapes corpus composition globally, starving a different code path. Variants: filter-string corrupted into binary garbage; filterSize byte fixated at 2; endian-swapped magic lock-in; keyword-lock-out; BPF program simplification. Dim3 (hitcount divergence) reveals these most clearly. Winning: varies (naive/VP/VPC). Losing: cmplog.
**Confidence:** medium=16, high=6
**Top resolving fuzzers:** `cmplog,naive,value_profile,value_profile_cmplog` (8); `naive,value_profile_cmplog` (5); `value_profile_cmplog` (3)
**Top blocking fuzzers:** `—` (8); `cmplog,value_profile` (5); `cmplog,naive,value_profile` (3)
**Raw class variants emitted by agents:**

- `vpc_combined_overhead_corpus_inflation` × 1
- `I2S_corpus_inflation_structural_delay` × 1
- `value_profile_cmp_map_corpus_bias` × 1
- `value_profile_corpus_bias` × 1
- `I2S_corpus_lock_arithmetic_bias` × 1
- `I2S_corpus_path_lock_in` × 1
- `I2S_corpus_lockdown_stochastic_delay` × 1
- `I2S_corpus_inflation_filter_size_fixation` × 1
**Representative hypothesis statements:**
- In sqlite3GetToken CC_QUOTE2 case, value_profile_cmplog is slow to resolve the properly-closed '[...]' bracket condition because its CMP_MAP feedback inflates the corpus with near-miss unclosed-bracket seeds (trial 2 other_hitcount=255) while the cmplog tracing stage imposes ~10x per-seed overhead o
- The blocked side requires SQL referencing the TEMP schema (iDb==1); naive's random havoc finds this incidentally within seconds, while cmplog and value_profile_cmplog inflate the corpus with I2S-derived SQL variants that do not use the TEMP schema, delaying resolution by hours on average.
- CMP_MAP gradient feedback in value_profile and value_profile_cmplog rewards seeds producing pWalker->eCode==2 (JOIN constancy checks) more consistently, biasing at least one trial per fuzzer into a corpus composed almost exclusively of JOIN-heavy SQL where the early-return true branch always fires, 
**Cost:** 1,384,825 total tokens over 21 matched jobs (avg 65,944/job, 389s/job).

### `I2S_switch_case_lock` — 11 reports

**Description:** Type 5 harm. The switch IS visible to I2S (not a jump table), but all case constants get logged and substituted. The corpus becomes locked onto the set of recognized case values — the `default:` arm or unlisted values become permanently unreachable. Winning: naive (random bytes miss all cases) and VPC (gradient retains non-case stepping stones). Losing: cmplog.
**Confidence:** medium=8, high=3
**Top resolving fuzzers:** `naive,value_profile,value_profile_cmplog` (6); `naive,value_profile_cmplog` (2); `cmplog,naive,value_profile,value_profile_cmplog` (1)
**Top blocking fuzzers:** `cmplog` (6); `cmplog,value_profile` (2); `value_profile_cmplog` (2)
**Raw class variants emitted by agents:**

- `I2S_switch_case_lock` × 4
- `I2S_switch_case_valid_value_barrier` × 2
- `I2S_switch_case_systematic_exploration` × 1
- `I2S_switch_case_locking` × 1
- `I2S_switch_case_locks_with_CMP_MAP_rescue` × 1
- `I2S_switch_case_lock_delay` × 1
- `I2S_switch_case_lock_in_duration_gap` × 1
**Representative hypothesis statements:**
- cmplog's I2S stage logs PE_TYPE::PE32 (0x10B) and PE_TYPE::PE32_PLUS (0x20B) as comparison targets at line 132 and substitutes these known constants back into the Magic field, locking the corpus to valid PE types and blocking the unknown-magic true branch; value_profile_cmplog's additional CMP_MAP g
- cmsChannelsOfColorSpace is a large switch over 4-byte ICC color space signatures; cmplog's I2S stage logs each constant comparison and systematically replaces the colorspace field with every recognized case value, producing 10-30 corpus entries per unusual case label, while value_profile and naive l
- Cmplog's I2S redqueen stage systematically substitutes the pcap linktype field with DLT constants recognized elsewhere in the gen_linktype() dispatch (DLT_EN10MB, DLT_LINUX_SLL, etc.), locking the corpus away from DLT_IEEE802_11_RADIO=127 specifically, while naive and value_profile freely explore th
**Cost:** 692,379 total tokens over 11 matched jobs (avg 62,943/job, 291s/job).

### `I2S_inequality_substitution` — 5 reports

**Description:** Type 4 harm. The branch is a strict inequality like `k > buflen` or `X > 31`. I2S substitutes k = buflen (equality), which fails the strict inequality. Winning: any fuzzer that mutates past the equality boundary via havoc. Losing: cmplog.
**Confidence:** high=4, medium=1
**Top resolving fuzzers:** `naive,value_profile,value_profile_cmplog` (4); `naive` (1)
**Top blocking fuzzers:** `cmplog` (4); `cmplog,value_profile,value_profile_cmplog` (1)
**Raw class variants emitted by agents:**

- `I2S_inequality_substitution_barrier` × 3
- `I2S_inequality_substitution` × 2
**Representative hypothesis statements:**
- The condition pIn[1]+nInt > pIn[0] (VList buffer overflow) is a strict inequality over internal runtime state; cmplog's I2S stage substitutes the RHS value (nAlloc) for the LHS expression, producing pIn[1]+nInt == pIn[0] which still fails the strict > test, and the absent CMP_MAP gradient provides n
- The condition pIn[1]+nInt > pIn[0] is a strict inequality over VList runtime state; cmplog's I2S stage substitutes the RHS comparand producing equality rather than strictly-greater-than, and the accumulation nature of the barrier (requires many named SQL variables across multiple VListAdd calls) res
- cmplog's I2S pass logs the comparison `a1->s->s.k > 31` and substitutes k = 31 (the threshold), which satisfies neither the >31 predicate; simultaneously, I2S locks the shift opcode field to BPF_LSH/BPF_RSH constants (0x60/0x70), narrowing the effective corpus, while naive and value_profile fuzzers 
**Cost:** 266,116 total tokens over 5 matched jobs (avg 53,223/job, 299s/job).

### `other_I2S_harm` — 3 reports

**Description:** Miscellaneous I2S harm patterns that don't fit the main categories. Includes early_return_lock, format_invariant_preservation, feedback_corpus_drift.
**Confidence:** high=2, medium=1
**Top resolving fuzzers:** `naive,value_profile` (2); `naive` (1)
**Top blocking fuzzers:** `cmplog,value_profile_cmplog` (2); `cmplog,value_profile,value_profile_cmplog` (1)
**Raw class variants emitted by agents:**

- `feedback_corpus_drift` × 1
- `I2S_format_invariant_preservation` × 1
- `I2S_early_return_lock` × 1
**Representative hypothesis statements:**
- I2S and CMP_MAP feedback in cmplog/value_profile/value_profile_cmplog bias the corpus toward derivatives of the initial 'SELECT 1;' seed, creating a local-optimum pull around SELECT-based SQL that delays or prevents discovery of VACUUM-type inputs; naive, with no such feedback bias, freely produces 
- cmplog/vpc's I2S redqueen pass operates on ICC header field comparisons during the tracing stage, continuously substituting recognized valid values (valid size, version, magic, device class) that flood the corpus with structurally-sound ICC profiles, systematically preventing all four sequential val
- cmplog's I2S redqueen pass observes the `Space1 == Space2` comparison at line 1061 and immediately substitutes the colorspace field to make them equal, causing the function to return TRUE at line 1061 and permanently locking cmplog's corpus out of the false-branch path (Space1 != Space2) that leads 
**Cost:** 222,946 total tokens over 3 matched jobs (avg 74,315/job, 650s/job).

### `I2S_keyword_or_token` — 2 reports

**Description:** I2S extracts runtime tokens during DFA/lexer tracing and populates the fuzzer's token dictionary, enabling TokenInsert/TokenReplace mutations to inject rare keywords. Winning: VPC (needs token extraction + CMP_MAP retention). Losing: naive/value_profile (no I2S token extraction).
**Confidence:** medium=2
**Top resolving fuzzers:** `cmplog,naive,value_profile,value_profile_cmplog` (1); `value_profile_cmplog` (1)
**Top blocking fuzzers:** `—` (1); `cmplog,naive,value_profile` (1)
**Raw class variants emitted by agents:**

- `I2S_filter_string_keyword_boost` × 1
- `I2S_token_extraction_for_flex_dfa_keywords` × 1
**Representative hypothesis statements:**
- The fuzz_both harness requires a valid ASCII BPF filter expression in its first input bytes; cmplog and value_profile use I2S/CMP_MAP to quickly converge on valid filter keywords causing pcap_compile to succeed and emit BPF opcodes, while naive relies on random havoc to accidentally produce a valid 
- These three grammar.c switch cases correspond to specific protocol keyword tokens (arp, msu, sio) recognized by a flex-generated DFA scanner; value_profile_cmplog resolves them because its I2S (cmplog) stage extracts keyword character sequences from the DFA character-level comparisons and adds them 
**Cost:** 127,080 total tokens over 2 matched jobs (avg 63,540/job, 437s/job).

### `experimental_artifact` — 2 reports

**Description:** Not a real fuzzer mechanism. The divergence is caused by unequal trial durations, random trial variance, or a 30-min measurement floor artifact. Flagged by the RCA agent for exclusion from mechanism inference.
**Confidence:** medium=1, high=1
**Top resolving fuzzers:** `value_profile_cmplog` (1); `naive,value_profile,value_profile_cmplog` (1)
**Top blocking fuzzers:** `cmplog,naive,value_profile` (1); `cmplog` (1)
**Raw class variants emitted by agents:**

- `run_length_artifact_plus_lexer_dfa_opacity` × 1
- `trial_duration_confound` × 1
**Representative hypothesis statements:**
- The dim2 duration divergence is dominated by a campaign run-length artifact (cmplog and value_profile only produced 1 coverage checkpoint at 30min while naive and vpc ran up to 12h), but there is a genuine secondary signal: within equal time windows, value_profile_cmplog is the only fuzzer that expl
- The dim3 hitcount divergence between 'high_exploration' (naive, vpc) and 'low_exploration' (cmplog, value_profile) is almost entirely explained by a run-duration confound: the long-running trials (12 h) belong to naive and vpc, while all cmplog trials and most value_profile trials ended after 30 min
**Cost:** 163,382 total tokens over 2 matched jobs (avg 81,691/job, 684s/job).

### `corpus_shape_or_volume` — 2 reports

**Description:** Dim3 'hitcount' divergence driven purely by how many total seeds accumulate without any structural barrier — the code path is reachable, fuzzers just exercise it more or fewer times based on corpus size/complexity.
**Confidence:** medium=2
**Top resolving fuzzers:** `cmplog,naive,value_profile,value_profile_cmplog` (2)
**Top blocking fuzzers:** `—` (2)
**Raw class variants emitted by agents:**

- `corpus_volume_divergence_via_I2S_filter_simplification` × 1
- `corpus_shape_iteration_depth` × 1
**Representative hypothesis statements:**
- Cmplog and value_profile build corpora of shorter, structurally simpler pcap filter programs, resulting in 30-100x fewer BPF bytecode instructions processed by atomuse() compared to naive and value_profile_cmplog, which develop larger and more complex filter programs through broad corpus expansion.
- The hitcount divergence in compute_local_ud arises because naive and value_profile_cmplog generate structurally complex BPF filter expressions (many BPF blocks, many stmts per block), driving high loop iteration counts in the optimizer, while cmplog's I2S substitution locks corpus seeds to specific 
**Cost:** 104,181 total tokens over 2 matched jobs (avg 52,090/job, 288s/job).

### `I2S_equality_lock` — 1 reports

**Description:** I2S satisfies an equality branch but cannot produce the inequality side. Similar to inequality_substitution but for `==` instead of `>`. Winning: non-I2S fuzzers. Losing: cmplog.
**Confidence:** high=1
**Top resolving fuzzers:** `naive,value_profile,value_profile_cmplog` (1)
**Top blocking fuzzers:** `cmplog` (1)
**Raw class variants emitted by agents:**

- `I2S_equality_lock` × 1
**Representative hypothesis statements:**
- Cmplog's I2S pass logs the comparison `ssl->in_msg[1] == 0x64 (100)` and substitutes the constant 100, driving all descendants toward the True branch (renegotiation alert matched) and starving the corpus of values != 100 that would hit the False branch.
**Cost:** 52,533 total tokens over 1 matched jobs (avg 52,533/job, 377s/job).

### `I2S_accelerated_reach` — 1 reports

**Description:** I2S resolves an upstream magic/signature so downstream code becomes reachable. The downstream branches appear as 'cmplog wins' even though the actual barrier was upstream. Winning: cmplog, VPC. Losing: value_profile (cannot cross the upstream constant gate).
**Confidence:** medium=1
**Top resolving fuzzers:** `cmplog,value_profile_cmplog` (1)
**Top blocking fuzzers:** `value_profile` (1)
**Raw class variants emitted by agents:**

- `I2S_accelerated_reach` × 1
**Representative hypothesis statements:**
- Reaching the fp_math floating-point arithmetic path at lines 86850-86852 requires SQL operands that are not both MEM_Int typed (or that cause integer overflow); cmplog's I2S stage accelerates discovery of the right operand-type configuration by 3-4x compared to value_profile which relies solely on C
**Cost:** 50,276 total tokens over 1 matched jobs (avg 50,276/job, 270s/job).

### `cmplog_throughput_overhead_and_cmpmap_queue_displacement` — 1 reports

**Description:** Observed in sqlite3. cmplog's tracing stage imposes ~10× per-seed throughput tax, and simultaneously VPC's CMP_MAP queue gets displaced by I2S-derived seeds that dominate scheduler priority. Winning: naive (high throughput). Losing: cmplog, VP, VPC.
**Confidence:** high=1
**Top resolving fuzzers:** `naive` (1)
**Top blocking fuzzers:** `cmplog,value_profile,value_profile_cmplog` (1)
**Raw class variants emitted by agents:**

- `cmplog_throughput_overhead_and_cmpmap_queue_displacement` × 1
**Representative hypothesis statements:**
- Naive resolves both branches within the first checkpoint interval (t<1800s) by processing the initial 22036-seed corpus at full throughput, reaching the VACUUM seed at t=11s; cmplog is delayed ~60x by its 10x-overhead tracing stage, value_profile is delayed because CMP_MAP-feedback-driven scheduler 
**Cost:** 75,027 total tokens over 1 matched jobs (avg 75,027/job, 569s/job).

### `I2S_multi_mechanism_harm` — 1 reports

**Description:** A branch is harmed by cmplog through multiple distinct I2S mechanisms simultaneously (e.g., corpus bias + structural corruption + throughput tax). Classification is 'compound' rather than any single Type N.
**Confidence:** high=1
**Top resolving fuzzers:** `naive,value_profile` (1)
**Top blocking fuzzers:** `cmplog,value_profile_cmplog` (1)
**Raw class variants emitted by agents:**

- `I2S_multi_mechanism_harm` × 1
**Representative hypothesis statements:**
- All four error-exit branches in _cmsReadHeader are blocked by cmplog's I2S machinery through a combination of corpus size inflation (branches 68 and 72 require inputs shorter than 128 bytes), inequality substitution failure (branch 70 requires Version > 0x5000000), and switch-case value lock-in (bra
**Cost:** 53,962 total tokens over 1 matched jobs (avg 53,962/job, 256s/job).

### `I2S_switch_value_lock_in` — 1 reports

**Description:** Specific case of switch-case lock where I2S locks the dispatch value into one specific case and downstream branches of other cases become unreachable. Winning: non-I2S fuzzers. Losing: cmplog.
**Confidence:** high=1
**Top resolving fuzzers:** `naive,value_profile,value_profile_cmplog` (1)
**Top blocking fuzzers:** `cmplog` (1)
**Raw class variants emitted by agents:**

- `I2S_switch_value_lock_in` × 1
**Representative hypothesis statements:**
- cmplog's I2S redqueen pass logs DLT constants from comparison instructions inside switch case bodies in gen_linktype() and related dispatch functions, then substitutes those constants into the pcap header linktype field, locking the corpus into a narrow set of DLT values that exclude DLT_IEEE802_11_
**Cost:** 58,042 total tokens over 1 matched jobs (avg 58,042/job, 258s/job).

### `I2S_structural_or_root_seed` — 1 reports

**Description:** An I2S-produced root seed propagates across the corpus, sometimes helping other fuzzers via shared ancestry. Includes cases where I2S corrupts a parent seed's structure but the descendants are preserved by CMP_MAP.
**Confidence:** medium=1
**Top resolving fuzzers:** `cmplog,naive,value_profile,value_profile_cmplog` (1)
**Top blocking fuzzers:** `—` (1)
**Raw class variants emitted by agents:**

- `I2S_root_seed_advantage` × 1
**Representative hypothesis statements:**
- An I2S-produced seed (mutation_op=None, from cmplog's tracing stage) becomes the common ancestor for all DLT-specific branch resolutions across trials; cmplog produces this root seed early, while naive must discover rare DLT constants via random arithmetic alone, causing multi-hour blocking delays e
**Cost:** 72,263 total tokens over 1 matched jobs (avg 72,263/job, 304s/job).

### `unknown` — 1 reports

**Description:** RCA agent could not classify or returned 'no_clear_root_cause'.
**Confidence:** medium=1
**Top resolving fuzzers:** `value_profile_cmplog` (1)
**Top blocking fuzzers:** `cmplog,naive,value_profile` (1)
**Raw class variants emitted by agents:**

- `unknown` × 1
**Representative hypothesis statements:**
- The dim2 duration divergence in init_linktype's DLT switch captures stochastic trial-level variance in DLT value sampling, systematically worsened for cmplog by I2S corpus restriction: cmplog trial2 converged on a narrow DLT set early and I2S reinforcement prevented exploration of the full 60+ DLT c

