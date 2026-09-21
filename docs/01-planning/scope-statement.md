# Scope statement

_Version 1.1 — revised 29 October 2026 after the title change. Original
agreed with supervisor 8 October 2026._

## Problem

Online reviews shape purchasing decisions, and fake reviews corrupt
that signal. The research literature treats "fake review" as one
category, but it covers two quite different things: text a paid human
wrote to deceive, and text a language model generated. Most published
detectors are trained and evaluated on one corpus and report one
headline score, so it is unclear whether a detector built for one
population works on the other.

## Aim

To build and evaluate a machine learning system that classifies reviews
as genuine or fake, and to measure how far detection performance
transfers between human-written and machine-generated fake reviews.

## Objectives

1. Assemble two labelled corpora, one of each fake-review population,
   with reproducible preprocessing.
2. Implement classical text-classification baselines and a transformer
   baseline within one pipeline so they are comparable.
3. Measure performance within each corpus, across corpora, and with
   pooled training.
4. Explain where the models' decisions come from, and whether they
   reflect deception or artefacts of how each corpus was produced.
   _(Semester 2)_
5. Deliver a demonstrator that scores a pasted review, and evaluate it
   with a small number of users. _(Semester 2)_

## In scope

- English-language review text.
- Public, already-published datasets.
- Text and simple surface features (length, punctuation, character
  n-grams).
- Offline evaluation, plus a single-page demonstrator in Semester 2.

## Out of scope

- Live scraping of any review platform. Rejected on ethics and terms-of-
  service grounds at the first supervision meeting.
- Reviewer-level behavioural and network features (burstiness, review
  graphs). Interesting — Rayana and Akoglu (2015) show they help — but
  they need platform metadata the chosen corpora do not carry.
- Non-English reviews.
- Deployment, scaling, or anything resembling a production service.

## Deliverables

| Deliverable | Due | Status |
|---|---|---|
| Ethics submission | 30 Oct 2026 | submitted 28 Oct |
| D1 Project Proposal and Research Report | 26 Nov 2026 | submitted 24 Nov |
| D2 Preparation and Feasibility Video | 26 Nov 2026 | submitted 24 Nov |
| D4 Project meetings and management | continuous | this repository + journals |
| D3 Dissertation | Semester 2 | not started |

## Constraints

- One student, roughly 400 hours across two semesters.
- No GPU beyond a free-tier cloud service; `roberta-base` would not fit
  in laptop memory, so `distilroberta-base` is the working model.
- No budget for data or compute.
- Semester 1 ends in Week 12; Weeks 8–10 collide with other coursework.

## Success criteria

Semester 1 succeeds if D1 and D2 are submitted on time, the ethics
approval is in place, and the repository contains a pipeline that a
third party can clone and run to reproduce the reported numbers. It does
**not** require a high detection score: the feasibility question is
whether the comparison can be made rigorously, and a low cross-dataset
number is a finding, not a failure.
