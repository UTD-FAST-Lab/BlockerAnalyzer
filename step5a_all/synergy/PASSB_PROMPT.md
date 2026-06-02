# Canonical synergy Pass-B dispatch prompt

Synergy is a **composite** family, so its Pass-B classification carries one extra
constraint the single-technique families don't have (co-cluster a branch's two
technique-halves). This file is the reusable prompt for that step so a future /
automated run reproduces it instead of re-inventing it.

**How to run (after `build_signature_cards.py --family synergy` + Pass-A distill):**
dispatch the `signature-feature-classifier` agent with the prompt below, then
validate with `python3 tools/check_synergy_clusters.py`.

The agent definition (`.claude/agents/signature-feature-classifier.md`) stays
generic — the synergy-specific knowledge lives ONLY here (prompt) and in the
deterministic validator. Do not bake it into the agent.

---

## PROMPT (feed verbatim to signature-feature-classifier)

Cluster the **synergy** mechanism family and overwrite `step5a_all/synergy/clusters.json`.

### Inputs (read these)
- `step5a_all/synergy/signatures.json` — the distilled signatures (the aggregated server-A + server-B union).
- `step5a_all/synergy.cards.json` — the cards (full mechanism text + `analysis_path` back-pointers).
- Open member `.analysis.json` files via `analysis_path` when a case is ambiguous.

### CRITICAL synergy-specific structure — read before clustering
This family is NOT like the single-technique families. Each synergy **branch**
contributes **two** signatures:
- `<branch>_h0` = the **I2S** angle (CmpLog/I2SRandReplace splices exact literals).
- `<branch>_h1` = the **VP** angle (CMP_MAP gradient preserves near-miss corpus).

They are a synergy family because at each branch **neither technique resolves
alone** — only `value_profile_cmplog` wins (VP builds the near-valid corpus
scaffold; I2S then completes the exact gate). So `_h0` and `_h1` are two views of
ONE joint mechanism, not two features.

**Hard constraints:**
1. **Cluster at the BRANCH level by the joint mechanism.** A branch's `_h0` and
   `_h1` MUST land in the SAME cluster — never split a branch's two halves. Treat
   (`<branch>_h0`, `<branch>_h1`) as an inseparable unit.
2. **Do NOT lump one-cluster-per-target.** Re-discover the real mechanism clusters
   from `mechanism_summary`; let the data decide the count (it is typically MORE
   than the number of targets — e.g. a single target's branches can split between
   a *field-read/dispatch* mechanism and a *structure-assembly* mechanism).
3. Coin an **emergent, descriptive** `mechanism_label` + `feature_id` per cluster
   naming the actual program feature (the joint gate's structural surface), NOT the
   generic "i2s_vp_joint_necessity". `feature_id` is snake_case and becomes a
   step-5b template dir name, so make it concrete.

### Output schema — match the other families EXACTLY
JSON array of cluster objects, each:
```json
{
  "feature_id": "<snake_case_descriptive>",
  "mechanism_family": "synergy",
  "mechanism_label": "<snake_case_descriptive>",
  "definition": "<1-2 sentences: the program feature + why both I2S and VP are jointly necessary>",
  "n_members": <int = number of member ids>,
  "members": [ {"id": "<branch>_h0", "target": "...", "branch_id": <int>, "analysis_path": "prompts_<a|b>/<branch>.analysis.json"}, ... ]
}
```
- `members` lists BOTH `_h0` and `_h1` for every branch in the cluster (so
  `n_members` is even = 2 × #branches).
- Carry each member's `analysis_path` **verbatim from its card** — it is already
  server-namespaced (`prompts_a/…` for server-A branches, `prompts_b/…` for
  server-B). Do NOT rewrite or invent it.
- Every signature id appears in exactly one cluster. No drops, no duplicates.

Return a short report: clusters discovered, each feature_id with its branch list,
and one line per target on whether/why it split.

---

## Validate (deterministic, after the agent writes clusters.json)
```bash
python3 tools/check_synergy_clusters.py     # coverage + co-cluster + schema invariants
```
A FAIL here (e.g. a branch split across clusters) means the agent violated a hard
constraint — re-dispatch with the violation quoted.
