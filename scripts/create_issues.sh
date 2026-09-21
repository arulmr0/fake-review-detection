#!/usr/bin/env bash
# Create the Semester 1 issue backlog, labels and milestones on GitHub.
#
# Requires the gh CLI, authenticated:  gh auth login
# Run once, from the repository root:  bash scripts/create_issues.sh
#
# Issue numbers in scripts/issues.csv are the ones the documents and
# journals refer to. GitHub assigns numbers in creation order, so run
# this on an empty repository and the numbering lines up. Gaps in the
# CSV (10, 11, 13, ...) are deliberate: they were the numbers of issues
# closed as duplicates, and the file records the backlog as it ended up
# rather than pretending it was planned perfectly.

set -euo pipefail

command -v gh >/dev/null || { echo "gh CLI not found: https://cli.github.com"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "not authenticated: run 'gh auth login'"; exit 1; }

echo "== labels =="
create_label() { gh label create "$1" --color "$2" --description "$3" --force; }
create_label "type:experiment" "1D76DB" "A run that produces a number for the report"
create_label "type:writing"    "5319E7" "A section of a report or document"
create_label "type:setup"      "0E8A16" "Tooling, pipeline or infrastructure"
create_label "type:admin"      "FBCA04" "Submissions, approvals, access requests"
create_label "type:bug"        "D73A4A" "Something is wrong"
create_label "priority:must"   "B60205" "MoSCoW: must have"
create_label "priority:should" "D93F0B" "MoSCoW: should have"
create_label "priority:could"  "FEF2C0" "MoSCoW: could have"
create_label "status:blocked"  "000000" "Waiting on something outside my control"

echo "== milestones =="
# Milestones are named after the fixed dates, not topics, so that
# progress is always measured against a real deadline.
create_milestone() {
  gh api "repos/{owner}/{repo}/milestones" -f title="$1" -f due_on="$2" -f description="$3" >/dev/null 2>&1 \
    || echo "   (milestone '$1' already exists)"
}
create_milestone "M1 Ethics"               "2026-10-30T23:59:59Z" "Ethics submission deadline, Week 7"
create_milestone "M2 Feasibility baseline" "2026-11-06T23:59:59Z" "Pipeline runs end to end with results"
create_milestone "M3 D1"                   "2026-11-26T23:59:59Z" "Project Proposal and Research Report"
create_milestone "M4 D2 video"             "2026-11-26T23:59:59Z" "Preparation and Feasibility Video"
create_milestone "M5 Semester 2"           "2027-04-30T23:59:59Z" "Demonstrator, robustness, dissertation"

echo "== issues =="
python3 - <<'PY'
import csv, subprocess, pathlib

rows = list(csv.DictReader(open(pathlib.Path("scripts/issues.csv"), encoding="utf-8")))
for row in rows:
    command = [
        "gh", "issue", "create",
        "--title", row["title"],
        "--body", row["body"],
        "--milestone", row["milestone"],
    ]
    for label in row["labels"].split(","):
        command += ["--label", label.strip()]
    print(f"  #{row['number']:>2}  {row['title']}")
    subprocess.run(command, check=True, capture_output=True)
print(f"\ncreated {len(rows)} issues")
PY

echo
echo "Done. Next: create a Projects board with columns"
echo "Backlog / Next / In Progress / Blocked / In Review / Done,"
echo "add the repository to it, and enable the built-in automation."
