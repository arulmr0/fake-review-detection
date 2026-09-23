# D1 — Project Proposal and Research Report

**Submitted 24 November 2026** (deadline 26 November). Approx. 6,000
words. This file is the working outline and section-by-section status;
the submitted document itself is `D1-report.docx` in this folder.

| # | Section | Words | Evidence it rests on | Status |
|---|---|---|---|---|
| 1 | Introduction and motivation |  | — | final |
| 2 | Aims and objectives |  | `docs/01-planning/scope-statement.md` | final |
| 3 | Literature review |  | `literature.md`, 14-study synthesis table | final |
| 4 | Requirements |  | `docs/01-planning/moscow-requirements.md` | final |
| 5 | Proposed methodology |  | `src/frd/`, Dietterich (1998) for the Semester 2 analysis | final |
| 6 | Feasibility evidence |  | `feasibility-study.md`, `results/results.csv`, `results/figures/` | final |
| 7 | Project plan |  | `docs/01-planning/roadmap.md`, milestones | final |
| 8 | Risks |  | `docs/01-planning/risk-register.md` | final |
| 9 | Professional, legal and ethical issues |  | `docs/04-ethics/` | final |
| 10 | References | — | Zotero, generated not typed | final |
| A | Appendix A — full results tables | — | moved here after 19 Nov feedback | final |
| B | Appendix B — issue export and milestone burndown (D4 evidence) | — | `docs/06-meetings/` | final |

## The argument, in one paragraph

Fake review detection is usually reported as a single score on a single
corpus. Two different populations hide inside that framing: human-written
deceptive reviews and machine-generated ones. This project measures
transfer between them. The feasibility study shows the transfer is poor
— every model drops sharply, and the transformer's advantage largely
disappears — so the dissertation is about the gap, not about squeezing
out another within-dataset point.

## What the feasibility section claims, and what it does not

**Claims.** The pipeline runs end to end and is reproducible from a
clean clone. Three classical models and one transformer can be compared
on equal terms. Within each corpus, performance is in line with the
literature. Across corpora, it falls to near chance for the classical
models and well below the within-dataset figure for the transformer.
Pooled training narrows the gap but does not close it.

**Does not claim.** That this generalises beyond two corpora. Each one
represents a single way of producing fake text, so a cross-corpus
comparison is partly a comparison of two production methods. Five folds
support a confidence interval, not a significance test — McNemar comes
in Semester 2. Nothing here says which model is best in general.

That paragraph is the limitations section the supervisor asked for on
19 November, and it is what makes the negative result defensible rather
than disappointing.

## Revisions after supervisor feedback (19 Nov)

- Introduction cut by ~400 words; it was setting out the field rather
  than the question.
- Explicit limitations subsection added at 5.4 (above).
- Two full results tables moved to Appendix A; the body keeps the one
  figure that carries the argument.
- Semester 2 plan given dates and named deliverables rather than phases.
