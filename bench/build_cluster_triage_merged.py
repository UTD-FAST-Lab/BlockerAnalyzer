#!/usr/bin/env python3
"""bench/build_cluster_triage_merged.py — regenerate docs/cluster_triage_merged.tex
from the current bench/dataset.jsonl.

The descriptive columns (cluster description / tool / metric(s) / metric meaning /
verify rule) are STABLE per (raw_cluster, decisive_shape) and are carried forward
verbatim from the existing .tex (they describe the shape's hypothesis, not the
canonical umbrella it landed in). Counts, umbrella grouping, family membership and
the Part-2 example rows are recomputed from the dataset, so a relabel/re-arbitrate
is reflected by re-running this script.

Run:  python3 bench/build_cluster_triage_merged.py
"""
import json, re, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "docs" / "cluster_triage_merged.tex"
DS = ROOT / "bench" / "dataset.jsonl"

FAM_ORDER = ["I2S-pro", "I2S-anti", "VP-pro", "JOINT (I2SxVP)",
             "ctx-coverage", "ngram-coverage", "grimoire"]


def fam_bracket(canon):
    if canon.startswith("i2s_anti"): return "I2S-anti"
    if canon.startswith("i2s_"): return "I2S-pro"
    if canon.startswith("vp_"): return "VP-pro"
    if canon.startswith("joint_"): return "JOINT (I2SxVP)"
    if canon.startswith("vpc_anti"): return "VPC-anti"   # merged away; should not appear
    if canon.startswith("ctx_"): return "ctx-coverage"
    if canon.startswith("ngram_"): return "ngram-coverage"
    if canon.startswith("grimoire_"): return "grimoire"
    return "??" + canon


def mangle(s):
    """clean identifier -> \\_\\allowbreak  style used in the table."""
    return s.replace("_", r"\_\allowbreak ")


def demangle(s):
    return (s.replace(r"\allowbreak", "").replace("{}", "")
             .replace(r"\_", "_").replace(" ", "").strip())


def shapecode(dataset_shape):
    """dataset shape -> the code used as the row key (i2s_vp_ prefix stripped)."""
    return dataset_shape[len("i2s_vp_"):] if dataset_shape.startswith("i2s_vp_") else dataset_shape


# ---------- parse the existing tex ----------
raw_text = TEX.read_text()
lines = raw_text.split("\n")

# Part-1 descriptive lookup keyed by (raw_label, shapecode)
P1 = {}          # (raw, code) -> dict(shape_field, desc, tool, metrics, meaning, rule, raw_field)
shape_field_by_code = {}
for ln in lines:
    s = ln.strip()
    if not (s.endswith(r"\\") and " & " in s):
        continue
    if s.startswith(r"\rowcolor") or "multicolumn" in s:
        continue
    parts = s[:-2].split(" & ")
    if len(parts) != 8:
        continue
    raw = demangle(parts[0])
    code = demangle(parts[1].split("(")[0])
    P1[(raw, code)] = dict(raw_field=parts[0], shape_field=parts[1], desc=parts[3],
                           tool=parts[4], metrics=parts[5], meaning=parts[6], rule=parts[7])
    shape_field_by_code.setdefault(code, parts[1])

# Part-2 mechanism lookup keyed by canonical label
P2 = {}          # canon -> dict(shapelist, example, metrics, rule, desc)
for ln in lines:
    s = ln.strip()
    if r"\newline" not in s or " & " not in s or r"\textbf{" not in s:
        continue
    head = s
    tail = ""
    for term in (r"\\\midrule", r"\\\bottomrule"):
        if term in head:
            head, tail = head.split(term, 1)
            break
    parts = head.split(" & ")
    if len(parts) != 5:
        continue
    m = re.search(r"\\textbf\{(.*?)\}", parts[0])
    canon = demangle(m.group(1)) if m else None
    shapelist = parts[0].split(r"\newline", 1)[1].strip() if r"\newline" in parts[0] else ""
    P2[canon] = dict(shapelist=shapelist, example=parts[1], metrics=parts[2],
                     rule=parts[3], desc=parts[4])


# ---------- recompute grouping from dataset ----------
rows = [json.loads(l) for l in open(DS)]
val = [r for r in rows if r["evidence"]["status"] == "validated"]
n_records = len(rows)
n_val = len(val)
n_inc = n_records - n_val
n_distinct = len({(r["target"], r["branch_id"]) for r in rows})

grp = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))  # fam -> canon -> (raw,code)->cnt
umb_n = collections.Counter()                                                          # (fam,canon)->n
for r in val:
    m = r["mechanism"] or {}
    canon, raw = m.get("canonical_label"), m.get("label")
    code = shapecode(r["shape"])
    fam = fam_bracket(canon)
    grp[fam][canon][(raw, code)] += 1
    umb_n[(fam, canon)] += 1

fam_n = collections.Counter()
fam_canons = collections.defaultdict(set)
for (fam, canon), n in umb_n.items():
    fam_n[fam] += n
    fam_canons[fam].add(canon)

n_features = len({c for f in grp for c in grp[f]})
n_raw = len({raw for f in grp for c in grp[f] for (raw, code) in grp[f][c]})


# ---------- emit Part 1 ----------
def umb_sorted(fam):
    return sorted(grp[fam], key=lambda c: (-umb_n[(fam, c)], c))


P1_BODY = []
fams_present = [f for f in FAM_ORDER if f in grp]
for fi, fam in enumerate(fams_present):
    for canon in umb_sorted(fam):
        P1_BODY.append(
            r"\rowcolor{black!10}\multicolumn{8}{@{}l}{\textbf{[%s]\ \ %s}\quad(final feature, n=%d)}\\"
            % (fam, mangle(canon), umb_n[(fam, canon)]))
        for (raw, code), cnt in sorted(grp[fam][canon].items(), key=lambda x: (-x[1], x[0][0])):
            e = P1[(raw, code)]
            P1_BODY.append(" & ".join([e["raw_field"], e["shape_field"], str(cnt),
                                       e["desc"], e["tool"], e["metrics"],
                                       e["meaning"], e["rule"]]) + r"\\")
        P1_BODY.append(r"\midrule")


# ---------- emit Part 2 ----------
def fmt_metrics(rec):
    rule = rec["evidence"]["rule"] or ""
    names = re.findall(r"[a-z][a-z_]+", rule.lower())
    m = rec["evidence"]["metrics"]
    out = []
    for k in names:
        if k in m and m[k] is not None and k not in (out):
            v = m[k]
            v = (str(v) if not isinstance(v, float) else (f"{v:.3f}".rstrip("0").rstrip(".")))
            out.append(f"{mangle(k)}={v}")
    out.append("target=" + str(m.get("target", rec["target"])))
    return "; ".join(out)


def part2_example(fam, canon):
    """build a fresh Part-2 cell-set for a mechanism with no carried-forward row."""
    recs = [r for r in val if (r["mechanism"] or {}).get("canonical_label") == canon]
    # representative = record whose metrics cover the most rule-named keys
    def score(r):
        names = set(re.findall(r"[a-z_]+", (r["evidence"]["rule"] or "").lower()))
        m = r["evidence"]["metrics"]
        return sum(1 for k in m if k in names and m[k] is not None)
    rep = max(recs, key=score)
    codes = sorted({shapecode(r["shape"]) for r in recs})
    shapelist = "; ".join(shape_field_by_code.get(c, mangle(c)) for c in codes)
    # description = largest raw cluster's desc
    (raw, code), _ = max(grp[fam][canon].items(), key=lambda x: x[1])
    desc = P1[(raw, code)]["desc"]
    example = "%s/%s -- derived gate" % (rep["target"], rep["branch_id"])
    rule_tex = (rep["evidence"]["rule"] or "").replace("_", r"\_\allowbreak ") \
                                              .replace(">=", r"\textgreater{}=") \
                                              .replace("<", r"\textless{}").replace(">", r"\textgreater{}")
    return dict(shapelist=shapelist, example=example, metrics=fmt_metrics(rep),
                rule=rule_tex, desc=desc)


COLSPEC = r"{@{}p{3.3cm}p{3.6cm}p{4.4cm}p{4.2cm}p{6.6cm}@{}}"
HDR = (r"\toprule \textbf{Mechanism (n; shapes)}&\textbf{Example branch \& gate}&"
       r"\textbf{Real-corpus metrics}&\textbf{Verify rule (arbiter)}&"
       r"\textbf{Description / reading}\\\midrule\endhead")

P2_BODY = []
for fam in fams_present:
    P2_BODY.append(r"\subsection*{%s\quad(%d roadblocks, %d mechanisms)}"
                   % (fam, fam_n[fam], len(fam_canons[fam])))
    P2_BODY.append(r"{\scriptsize\begin{longtable}" + COLSPEC)
    P2_BODY.append(HDR)
    mechs = umb_sorted(fam)
    for canon in mechs:
        cells = P2.get(canon) or part2_example(fam, canon)
        field0 = (r"\textbf{%s} (n=%d)\newline %s"
                  % (mangle(canon), umb_n[(fam, canon)], cells["shapelist"]))
        P2_BODY.append(" & ".join([field0, cells["example"], cells["metrics"],
                                   cells["rule"], cells["desc"]]) + r"\\\midrule")
    P2_BODY.append(r"\bottomrule\end{longtable}}\par\medskip")


# ---------- assemble ----------
PREAMBLE = r"""\documentclass[7pt]{extarticle}
\usepackage[landscape,margin=1cm]{geometry}
\usepackage{longtable,booktabs,array}
\usepackage[table]{xcolor}
\renewcommand{\arraystretch}{1.15}
\setlength{\tabcolsep}{3pt}
\begin{document}
\section*{Roadblock cluster triage --- raw clusters under final mechanism umbrellas (detailed)}
\noindent\small Source: \texttt{bench/dataset.jsonl} (%d rows over %d distinct branches; %d validated / %d inconclusive). %d raw clusters merged into %d final features. Each shaded block is a final feature (umbrella); rows beneath are the raw clusters (per decisive shape) merged into it.\\[3pt]
{\scriptsize\begin{longtable}{@{}p{2.4cm}p{1.9cm}rp{4.3cm}p{1.5cm}p{1.7cm}p{4.6cm}p{3.0cm}@{}}
\toprule \textbf{Raw cluster}&\textbf{Shape (res/blk)}&\textbf{\#br}&\textbf{Cluster description}&\textbf{Tool}&\textbf{Metric(s)}&\textbf{Metric meaning / prediction}&\textbf{Verify rule}\\\midrule
\endhead
""" % (n_records, n_distinct, n_val, n_inc, n_raw, n_features)

MID = (r"\bottomrule\end{longtable}}" + "\n"
       r"\clearpage\section*{Mechanism families --- detailed evidence}" + "\n"
       r"\noindent\small One table per technique-direction family. Each row is a final "
       r"mechanism with a representative validated branch, its real-corpus measured metrics, "
       r"the deterministic verify rule that fired, and the mechanism reading.\\[4pt]" + "\n")

out = (PREAMBLE + "\n".join(P1_BODY) + "\n" + MID + "\n".join(P2_BODY) + "\n" + r"\end{document}" + "\n")
TEX.write_text(out)
print(f"wrote {TEX}")
print(f"  {n_records} rows / {n_distinct} distinct / {n_val} validated / {n_inc} inconclusive")
print(f"  {n_raw} raw clusters -> {n_features} final features")
for fam in fams_present:
    print(f"  {fam:18s} {fam_n[fam]:4d} roadblocks, {len(fam_canons[fam])} mechanisms")
