#!/usr/bin/env python3
"""GRC Control Mapper.

Maps a single self-assessment onto ISO/IEC 27001:2022 (Annex A), PCI DSS v4.0
and NIST CSF 2.0, then reports coverage per framework and lists gaps.

Usage:
    python mapper.py sample_assessment.csv
    python mapper.py my_assessment.csv --out report.md
"""
import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

FRAMEWORKS = {
    "iso27001_2022": "ISO/IEC 27001:2022",
    "pci_dss_v4": "PCI DSS v4.0",
    "nist_csf_2": "NIST CSF 2.0",
}
SCORE = {"implemented": 1.0, "partial": 0.5, "not_implemented": 0.0}
VALID = set(SCORE) | {"not_applicable"}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load(map_path, assessment_path):
    controls = {r["id"]: r for r in read_csv(map_path)}
    answers = {}
    for row in read_csv(assessment_path):
        status = row["status"].strip().lower()
        if row["id"] not in controls:
            sys.exit(f"Unknown control id in assessment: {row['id']}")
        if status not in VALID:
            sys.exit(f"Invalid status '{status}' for {row['id']} (use {sorted(VALID)})")
        answers[row["id"]] = (status, row.get("notes", ""))
    missing = sorted(set(controls) - set(answers))
    if missing:
        print(f"Warning: no answer for {', '.join(missing)}; treated as not_implemented",
              file=sys.stderr)
        for cid in missing:
            answers[cid] = ("not_implemented", "No answer provided")
    return controls, answers


def coverage(controls, answers):
    """Return per-framework score (percent) and the list of gaps."""
    result = {}
    for key, label in FRAMEWORKS.items():
        total = got = 0.0
        gaps = []
        for cid, ctl in controls.items():
            status, notes = answers[cid]
            if status == "not_applicable" or not ctl[key].strip():
                continue
            total += 1
            got += SCORE[status]
            if status != "implemented":
                gaps.append((cid, ctl["control"], ctl[key], status, notes))
        result[key] = (round(100 * got / total, 1) if total else 0.0, gaps)
    return result


def render(controls, answers, result):
    out = ["# GRC Coverage Report", ""]
    out += ["| Framework | Coverage |", "|---|---|"]
    for key, label in FRAMEWORKS.items():
        out.append(f"| {label} | {result[key][0]}% |")
    out += ["", "Scoring: implemented = 1, partial = 0.5, not implemented = 0. "
            "Not-applicable controls are excluded.", ""]
    by_status = defaultdict(int)
    for status, _ in answers.values():
        by_status[status] += 1
    out.append("**Status summary:** " + ", ".join(f"{k}: {v}" for k, v in sorted(by_status.items())))
    for key, label in FRAMEWORKS.items():
        out += ["", f"## Gaps against {label}", ""]
        gaps = result[key][1]
        if not gaps:
            out.append("No gaps identified.")
            continue
        out += ["| ID | Control | Reference | Status | Notes |", "|---|---|---|---|---|"]
        for cid, name, ref, status, notes in gaps:
            out.append(f"| {cid} | {name} | {ref} | {status} | {notes} |")
    out += ["", "> Indicative mapping for self-assessment and prioritisation only. "
            "Validate against the current published standards before relying on it "
            "for certification or audit."]
    return "\n".join(out) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("assessment", help="CSV with columns: id,status,notes")
    p.add_argument("--map", default=str(Path(__file__).with_name("controls_map.csv")))
    p.add_argument("--out", help="write the Markdown report to this file")
    args = p.parse_args()
    controls, answers = load(args.map, args.assessment)
    report = render(controls, answers, coverage(controls, answers))
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print(f"Report written to {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
