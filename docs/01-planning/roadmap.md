# Semester 1 roadmap

Planned backwards from the three fixed dates, not forwards from the
start. Two of the original estimates turned out to be impossible once
the deadlines were treated as immovable, and were re-scoped rather than
hoped through.

| Fixed date | What |
|---|---|
| 25 Sep 2026 (W2) | Project allocation completed |
| 2 Oct 2026 (W3) | Project meetings and management start (D4) |
| 30 Oct 2026 (W7) | Ethics submission deadline |
| 26 Nov 2026 (W11) | D1 and D2 due |

Internal deadlines sit a week ahead of every external one. That is the
single practice most responsible for both deliverables going in two days
early.

## Phases

### Phase 1 — Setup and scoping (W2–W4, to 9 Oct)
Milestone: none · Journal 1

- Repository, issue backlog, board, branch model
- Scope statement and MoSCoW list
- Dataset shortlist with licences; both corpora downloaded
- Reading list started; D1 skeleton committed
- Ethics form drafted

### Phase 2 — Ethics and feasibility baseline (W5–W7, to 30 Oct)
Milestones: M1 Ethics, M2 Feasibility baseline · Journal 2

- **Ethics submitted 28 Oct** — two days before the deadline
- Literature review restructured around three themes; synthesis table
- Preprocessing pipeline, reproducible from one command
- TF–IDF baselines, five-fold cross-validated
- First cross-dataset test — the finding that reframes the project
- Title changed, agreed 29 Oct, in time for D1

### Phase 3 — Report and video (W8–W10, to 20 Nov)
Milestones: M3 D1, M4 D2 · Journal 3

- Remaining conditions: reverse cross-dataset, combined training
- **D1 full draft to supervisor 12 Nov** (internal deadline)
- CI, issue templates, test suite
- D2 storyboarded, scripted, recorded, edited by 20 Nov
- D1 revised after 19 Nov feedback

### Phase 4 — Submit and close out (W11–W12, to 4 Dec)
Journal 4

- **D1 and D2 submitted 24 Nov** (deadline 26 Nov)
- Release `v0.2.0-feasibility`; reproduction verified from a clean clone
- Milestones closed; issue list exported as D4 evidence
- Semester 2 backlog written under milestone M5

## Dependencies worth naming

- Everything experimental depends on the preprocessing pipeline (#12).
  It was scheduled first for that reason.
- The D2 video depends on the pipeline running end to end on screen, so
  the video could not be recorded before the baselines worked.
- D1's feasibility chapter depends on the cross-dataset result, which is
  why that experiment was pulled forward into Phase 2.
- Nothing in Semester 1 depends on ethics approval being *returned* —
  only on it being submitted — because no participants are involved.
  That is what made R3 a low-impact risk.

## What slipped

- A baseline classifier was planned for W4 and arrived in W5. The
  rejected large-file push and the failed local transformer load
  accounted for most of the difference.
- SMOTE oversampling (#19) cost two days and produced a negative result.
  Kept in the report as the evidence for not resampling.
- MLflow and DVC were each adopted and dropped. Rule adopted after the
  second one: at most half a day evaluating a new tool before deciding.
