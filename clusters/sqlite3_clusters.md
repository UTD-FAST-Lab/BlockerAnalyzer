# Branch Clusters -- sqlite3
**Generated:** 2026-04-02
**Divergent branches:** 23 (out of 227 confirmed blockers with seeds)
**Functions:** 1 (all in sqlite3.c)
**Clusters:** 4
**Tier 1 branches analyzed:** 5

## Summary

| Cluster | Controlling Bytes | Semantic Meaning | Branches (Tier 1) |
|---------|------------------|------------------|----------------------------|
| BC01 | SQL operator char `-` or `/` in arithmetic expr | VDBE arithmetic opcode dispatch | R9*, R13* |
| BC02 | FLOAT/NULL/BLOB token in SQL | Parser rule 173: term ::= NULL\|FLOAT\|BLOB | R10* |
| BC03 | Unary `-` before integer literal | codeInteger negFlag path | R11* |
| BC04 | Float literal triggering internal printf `!` flag | sqlite3VXPrintf flag_altform2 | R15* |

(*) = Tier 1 representative

## Cluster Details

### BC01 -- SQL arithmetic operator (subtract/divide)

**Controlling bytes:** The input must be a syntactically valid SQL `SELECT` statement containing an arithmetic expression with the specific operator character: `-` for OP_Subtract (R9) or `/` for OP_Divide (R13).
**Source mapping:** The SQL parser produces VDBE bytecode with OP_Subtract (TK_MINUS) or OP_Divide (TK_SLASH). These are case labels in the VDBE execution loop at sqlite3.c:86801-86805. The branch at each `case` label tests whether `pOp->opcode` matches that specific opcode.
**Verification:** CONFIRMED (round 1)

**Why naive fails:** The naive fuzzer generates mostly binary/garbage inputs that never parse as valid SQL. Without I2S (cmplog) or value-profile feedback, the fuzzer cannot discover the `SELECT` keyword or the specific operator tokens needed to trigger these VDBE opcodes.

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R9 | sqlite3.c:86802:1 | True | 1 (rep) | Confirmed -- needs `-` operator |
| R13 | sqlite3.c:86804:1 | True | 1 (rep) | Confirmed -- needs `/` operator |

---

### BC02 -- FLOAT/NULL/BLOB literal token

**Controlling bytes:** The input must contain a SQL literal recognized as a FLOAT (e.g. `0.001`, `1e5`), NULL, or BLOB (e.g. `X'AB'`) token. An INTEGER token alone does not trigger this branch.
**Source mapping:** The Lemon-generated parser at sqlite3.c:157660 dispatches `case 173: /* term ::= NULL|FLOAT|BLOB */`. This is a `yyruleno` switch: the branch tests `yyruleno == 173`.
**Verification:** CONFIRMED (round 1)

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R10 | sqlite3.c:157660:7 | True | 1 (rep) | Confirmed |

---

### BC03 -- Unary minus before integer (negFlag)

**Controlling bytes:** The SQL must contain a unary minus operator immediately before an integer literal (e.g. `-1`, `+-1`). This sets `negFlag=1` in the `codeInteger()` function.
**Source mapping:** `codeInteger()` at sqlite3.c:102982 tests `if( negFlag ) i = -i;`. The `negFlag` parameter is set by the expression code generator when it encounters a `TK_UMINUS` node wrapping an integer expression with the `EP_IntValue` flag.
**Verification:** CONFIRMED (round 1)

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R11 | sqlite3.c:102982:9 | True | 1 (rep) | Confirmed |

---

### BC04 -- Internal printf `!` flag (flag_altform2)

**Controlling bytes:** The SQL must produce a result that triggers sqlite3's internal `%!.15g`-style float formatting. This happens when a float literal appears in a SELECT expression (e.g. `SELECT 0.000100000`). The `!` flag is a custom sqlite3 printf extension that controls float display precision.
**Source mapping:** `sqlite3VXPrintf()` at sqlite3.c:28404, case `'!'` in the format-flag switch. The `!` flag is embedded in internal format strings used by `sqlite3_mprintf()` when converting float results to text for output.
**Verification:** CONFIRMED (round 1)

**Note:** This branch is downstream of BC02 -- a float literal must first be parsed (BC02) before it can produce a float result that triggers the `!` format flag (BC04). However, BC02 can also be triggered by NULL or BLOB tokens which do NOT trigger BC04, so they are distinct clusters.

**Branches:**
| Rank | Branch | Blocked Side | Tier | Status |
|------|--------|-------------|------|--------|
| R15 | sqlite3.c:28404:9 | True | 1 (rep) | Confirmed |

---

## Tier 1 -- Full Analysis Details

### R9 -- sqlite3.c:86802:1 (OP_Subtract)

**Positive seeds (N=10, cmplog/trial1):**
| Seed ID | Size | Key content |
|---------|------|-------------|
| 15005b87b8310ed5 | 30 | `SELECT\t0-000000000000000000000` |
| 161dbb32aa53028e | 103 | `SELECT\t0*11,111+11111111*11,...,1-01111,...` |
| 175c42f025fe43a3 | 53 | `SELECT\t111-0/00001+100011*+0111+...` |
| 177267f6c5115100 | 87 | `SELECT\t10-0111-11+111-1.+111=1+...` |
| a20e58b8712255ab | 39 | `SELECT\t1111,1-11101,1111,2-11111,1+1111` |
| a3d5f196fb163f75 | 27 | `SELECT\t1111-11101 1+111111;` |
| a41a65c5e233a325 | 87 | `SELECT\t1111,1,...,1-111111111111111,...` |
| d05cd188787db9ac | 82 | `SELECT\t- 11,111-01,1,1-0101,...` |
| d063949221114201 | 76 | `SELECT\t+1\t+-+1+11%+-+11\t+-+1+11%+-+11...` |
| d080bec9f80fce03 | 80 | `SELECT\t+1\t+-+1+11%+-+11\t+-+111%+-+11...` |

**Negative seeds (N=10, naive/trial1):**
| Seed ID | Size | Key content |
|---------|------|-------------|
| 0000512cb37d4bfe | 58 | Binary: `6f0c f3e8 030c...` |
| 0000f558b5d87274 | 220 | Binary: `c58d 3b20 0c3b...` |
| 0001ab1ce073909e | 29 | Partial text: `E666E"""";;...` |
| 00028f38d81bd49b | 56 | Binary: `353b ba1e f8ff...` |
| 0002d1052224e9a7 | 10 | Partial: `;;;;:..Q.E` |
| 0002da9c061c9b67 | 84 | Binary with fragments: `NE`, `CT/;;` |
| 0002f00af7fa46c4 | 18 | `""/LLLLLLLLLLLLLLL` |
| 0004a044a6331af0 | 29 | `unix-...ix-exclIF` |
| 000767e454135a1b | 12 | `N..T NE ; 5;` |
| 00082c6a8422ce36 | 20 | `Crc#;E;...NECT` |

**Byte diff:**
| Region | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| Bytes 0-5 | `SELECT` (0x53454c454354) | Random binary | 10/10 vs 0/10 |
| Byte 6 | `\t` or ` ` (whitespace) | Random | 10/10 vs 0/10 |
| Body | Contains `-` operator in arithmetic context | No valid SQL | 10/10 vs 0/10 |

**Source trace:**
1. Input parsed by `sqlite3RunParser()` -> tokenizer recognizes `SELECT` keyword
2. Parser generates expression tree with `TK_MINUS` operator node
3. Code generator emits `OP_Subtract` VDBE instruction
4. VDBE interpreter hits `case OP_Subtract:` at line 86802

**Hypothesis:** Input must start with `SELECT` followed by whitespace and an arithmetic expression containing the `-` character as a binary subtraction operator between two numeric operands.
**Verification:** CONFIRMED (round 1)
- Test A: Positive seed `SELECT\t0-0...` with `-` replaced by `+` -> Branch 86802:1 True: 0. PASS.
- Test B: Synthetic `SELECT 1-1` -> Branch 86802:1 True: 1. PASS.

**Controlling bytes:** Bytes 0-6 must spell `SELECT` + whitespace; body must contain `-` operator in valid arithmetic expression context.
**Cluster:** BC01

---

### R13 -- sqlite3.c:86804:1 (OP_Divide)

**Positive seeds (N=10, value_profile_cmplog/trial1):**
| Seed ID | Size | Key content |
|---------|------|-------------|
| 3daf775b9d2740cb | ~200 | `SELECT 1333...+3/-4,444&44,...` (contains `/`) |
| 3e65b47c79de8e8b | ~150 | `SELECT 133...+3/-4,44,...` (contains `/`) |
| 3f0541d6472eb569 | ~15 | `SELECT 1e99/95 ...` (contains `/`) |
| 3f6d35b4c69d3235 | ~200 | `SELECT 1333...+3/-4,...` (contains `/`) |
| 6150c2095c5f1603 | ~50 | `SELeCT+- 11e11/11111/11/...` (contains `/`) |

**Negative seeds (N=10, naive/trial1):** Same set as R9 -- binary garbage, no valid SQL.

**Hypothesis:** Input must be valid SQL containing the `/` operator.
**Verification:** CONFIRMED (round 1)
- Test A: `SELECT 1+1` (no `/`) -> Branch 86804:1 True: 0. PASS.
- Test B: `SELECT 1/1` -> Branch 86804:1 True: 1. PASS.

**Controlling bytes:** Body of SQL expression must contain `/` as division operator.
**Cluster:** BC01

---

### R10 -- sqlite3.c:157660:7 (parser case 173: term ::= NULL|FLOAT|BLOB)

**Positive seeds (N=8, cmplog/trial1 + value_profile/trial1):**
| Seed ID | Size | Fuzzer | Key content |
|---------|------|--------|-------------|
| 161dbb32aa53028e | 103 | cmplog | Contains `1e111111111` (scientific notation = FLOAT) |
| 169fea6de73c403b | ~120 | cmplog | Contains `1E11111111` (FLOAT) |
| 177267f6c5115100 | 87 | cmplog | Contains `1.+111` (FLOAT-like) |
| 998d7e6ae39e287b | ~80 | cmplog | Contains `1.+111` |
| 99aa4d10ad997a81 | 30 | cmplog | `SELECT\t0.000100000` (FLOAT) |
| e6d413b107c09d3c | ~50 | cmplog | Contains `11111.1` (FLOAT) |
| 3dfd783a71b4d4c9 | ~150 | value_profile | (FLOAT in expression) |
| 3fcbeed716132a45 | ~150 | value_profile | (FLOAT in expression) |

**Negative seeds (N=10, naive/trial1):** Binary garbage -- no FLOAT/NULL/BLOB tokens.

**Hypothesis:** Input must contain a FLOAT literal (decimal point or `E`/`e` notation), NULL keyword, or BLOB literal (`X'...'`).
**Verification:** CONFIRMED (round 1)
- Test A: `SELECT 1` (INTEGER only) -> Branch 157660:7 True: 0. PASS.
- Test B: `SELECT 1.5` -> True: 1. `SELECT NULL` -> True: 1. `SELECT X'AB'` -> True: 1. PASS.

**Controlling bytes:** SQL body must contain a token recognized as TK_FLOAT (`.` or `e`/`E` in number), TK_NULL (`NULL`), or TK_BLOB (`X'...'`).
**Cluster:** BC02

---

### R11 -- sqlite3.c:102982:9 (codeInteger negFlag)

**Positive seeds (N=8, value_profile_cmplog/trial1):**
| Seed ID | Size | Key content |
|---------|------|-------------|
| 3daf775b9d2740cb | ~200 | `SELECT 1333...+3/-4,...` (unary `-` before `4`) |
| 3e65b47c79de8e8b | ~150 | `SELECT 133...E44,...` |
| 3f6d35b4c69d3235 | ~200 | `SELECT 1333...+3/-4,...` |
| 9d406c8cd9e958bb | ~200 | `SELECT 1333...+3/-0,...` |
| 9e1b8f15e0af61f9 | ~200 | Contains `*-44,...` (unary minus) |
| 9e3dd7ce95abd76a | ~20 | `SELeCT+- 11/11/11111/19` (unary `-` before `11`) |
| fd75b29a098453ce | ~150 | (unary minus in expression) |
| fd8684f19b500b5a | ~150 | (unary minus in expression) |

**Negative seeds (N=10, value_profile/trial2):**
| Seed ID | Size | Key content |
|---------|------|-------------|
| 6a171c596eb4d6db | 78 | `SELECT 121221111118811%2211...` (no unary minus) |
| 6a1f51c6e8d30678 | ~40 | `SELECT 7:SE...` (corrupted) |
| 6aa1c995f3f19c9e | ~120 | `SELECT 1*$$R+++++...` (no unary minus before int) |

**Byte diff:**
| Region | Positive pattern | Negative pattern | Consistency |
|--------|-----------------|------------------|-------------|
| Body | Contains `-` immediately before integer (unary context: after operator or at start) | No unary minus before integer literals | 8/8 vs 0/10 |

**Source trace:**
1. SQL parser recognizes unary minus before integer literal -> sets `TK_UMINUS` node
2. Expression code generator calls `codeInteger()` with `negFlag=1`
3. Inside `codeInteger()`, `if( negFlag ) i = -i;` at line 102982

**Hypothesis:** SQL expression must have unary minus directly before an integer literal (e.g. `-1`, `+-1`, `*-4`).
**Verification:** CONFIRMED (round 1)
- Test A: `SELECT 1` (no unary minus) -> Branch 102982:9 True: 0. PASS.
- Test B: `SELECT -1` -> Branch 102982:9 True: 1. PASS.
- Cross-check: Negative seed `SELECT 121221...%22111...` reaches `codeInteger` (Branch 102979:7 True: 3) but has True: 0 for 102982:9 (no negFlag).

**Controlling bytes:** Arithmetic expression must contain unary minus before integer literal.
**Cluster:** BC03

---

### R15 -- sqlite3.c:28404:9 (flag_altform2 `!` in printf)

**Positive seeds (N=7, cmplog/trial1 + value_profile_cmplog/trial1):**
| Seed ID | Size | Fuzzer | Key content |
|---------|------|--------|-------------|
| 99aa4d10ad997a81 | 30 | cmplog | `SELECT\t0.000100000...` (float) |
| e6d413b107c09d3c | ~50 | cmplog | `SELECT\t1++...111-11111.1+11+...` (float via `.`) |
| c4d464a1d0d55291 | ~100 | vp_cmplog | `SELECT 133...+3*244...` |
| f6bfbe992f178891 | ~100 | vp_cmplog | `SELECT 133...*++4444...` |
| f7047334c86d3fa1 | ~100 | vp_cmplog | `SELECT 133...444...` |
| f8479b82ca85e083 | ~100 | vp_cmplog | (arithmetic with floats) |
| f84ebf8485834f44 | ~100 | vp_cmplog | (arithmetic with floats) |

**Negative seeds (N=10, naive/trial1):** Binary garbage (same set as other branches).

**Source trace:**
1. SQL expression evaluates to a float result
2. Result is formatted for output using sqlite3's internal `sqlite3_mprintf()`
3. Internal format string contains `%!.15g` (custom `!` flag)
4. `sqlite3VXPrintf()` at line 28404: `case '!': flag_altform2 = 1; break;`

**Hypothesis:** SQL must produce a float-valued result. This requires either (a) a FLOAT literal, (b) arithmetic involving a float, or (c) integer division producing a non-integer result. The float result triggers the internal `%!.15g` formatter.
**Verification:** CONFIRMED (round 1)
- Test A: `SELECT 1` (integer result) -> Branch 28404:9 True: 0. PASS.
- Test B: `SELECT 0.000100000` -> Branch 28404:9 True: 2. PASS.

**Controlling bytes:** SQL expression body must produce a floating-point result (needs `.` or `e`/`E` in a number literal, or an arithmetic expression yielding float).
**Cluster:** BC04

---

## Cross-Cluster Relationships

BC02 (FLOAT/NULL/BLOB token) and BC04 (float printf `!` flag) are related but distinct:
- BC02 is triggered at **parse time** when the tokenizer recognizes a FLOAT, NULL, or BLOB literal.
- BC04 is triggered at **output time** when a float result is formatted for display.
- A NULL or BLOB token triggers BC02 but NOT BC04.
- A float token triggers BOTH BC02 and BC04.
- BC04 is downstream of BC02 for the float case, but not for NULL/BLOB.

BC01 (arithmetic operators `-`, `/`) can co-occur with BC03 (unary minus) when the expression contains both binary subtraction/division and unary negation (e.g. `SELECT 1-(-1)`). They are independent: `-` as binary operator triggers BC01, while `-` as unary prefix triggers BC03.

## Root Cause Summary

All 5 branches share a common meta-cause: **the naive fuzzer cannot synthesize valid SQL syntax**. The naive fuzzer relies purely on random mutation and lacks:
1. **Input-to-state (I2S/cmplog)** feedback that helps discover the `SELECT` keyword and operator tokens
2. **Value profile** feedback that rewards partial matches on multi-byte comparisons

Without these, the fuzzer generates binary noise that fails at the tokenizer stage, never reaching the parser (BC02), expression code generator (BC03), VDBE interpreter (BC01), or output formatter (BC04).

---

## Tier 2 — Automated Verification Results

**Tool:** `tools/cluster_verify.py` (single Docker container, 194s total)

**227 divergent branches tested against 4 clusters:**

| Result | Count |
|--------|-------|
| Assigned (A+B confirmed) | 60 |
| Skipped (no seeds on either side) | 50 |
| Unfitted (has seeds, no cluster fits) | 117 |

**Per-cluster breakdown (including Tier 1 representatives):**

| Cluster | T1 rep | T2 assigned | Total |
|---------|--------|-------------|-------|
| BC01 (SELECT arithmetic) | 2 | 51 | 53 |
| BC03 (unary minus) | 1 | 5 | 6 |
| BC04 (float printf) | 1 | 0 | 1 |
| Unfitted | — | — | 117 |
| Skipped (no seeds) | — | — | 50 |
| **Total** | **5** | **56** | **227** |

Note: 117 unfitted branches have seeds on at least one side but don't match any current cluster. These need additional T1 analysis rounds.
