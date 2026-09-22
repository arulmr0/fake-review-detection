# D1 — Section 6: Feasibility evidence

_Drafting copy for the report. ~700 words, matching the allocation in
`D1-outline.md`. The evidence behind every claim here is in
`feasibility-study.md`; this is the prose version for the marker._

---

## 6. Feasibility evidence

This section establishes that the project can be completed to its stated
aim within the time, compute and data access available, and does so from
measurement rather than assertion. Four kinds of evidence are offered:
a working prototype, pilot results across all three experimental
conditions, benchmarked compute, and a budget calculation that closes.

### 6.1 The pipeline runs end to end

The central feasibility claim is not that a detector can be built —
that much is settled in the literature — but that the *comparison* this
project rests on can be made rigorously by one student in two semesters.
The prototype demonstrates it. A single command, `make demo`, generates
a stand-in corpus, runs three classical models under two vectorisers
across every experimental condition, appends results to an append-only
log tagged with the commit hash and random seed, regenerates the
figures, and trains the command-line predictor — with no network access
and in under two minutes. The same command is what allows continuous
integration to run at all, since the real corpora are excluded from
version control on licence grounds.

Reproducibility was tested rather than claimed. In Week 9 the repository
was cloned onto a second machine and the README followed line by line:
the twenty-eight tests passed, the linter was clean, and the experiments
reproduced. That exercise, not the results themselves, is what supports
the claim that a third party could verify this work.

### 6.2 All three conditions are expressible

A feasibility study for this project has to show that the research
question can be *asked*, not that it has a flattering answer. The
experimental design produces rows for each corpus evaluated within
itself under five-fold cross-validation, for both cross-corpus
directions, and for pooled training — all under one protocol, one seed
and one metric, so that differences between conditions are attributable
to the conditions rather than to the setup.

Two design decisions make those numbers trustworthy. The vectoriser is
fitted inside each cross-validation fold rather than over the whole
corpus; an early version did the latter, which leaked test vocabulary
into training and inflated every score before Week 5. That bug is now
guarded by a regression test. And macro-F1 with per-class precision,
recall and a confusion matrix replaced plain accuracy after supervision
on 29 October, because the splits are not exactly balanced and accuracy
conceals per-class collapse — the precise failure mode expected when a
detector is moved to a population it was not trained on.

### 6.3 Compute is benchmarked, not estimated

The binding constraint was identified in Week 4, when `roberta-base`
failed to load in laptop memory. Rather than assume a workaround, the
alternative was measured: `distilroberta-base`, at 82 million
parameters, fine-tunes on a free-tier T4 in roughly twelve minutes of
wall-clock time including the model download. The model choice therefore
follows from a measurement, which is what distinguishes a feasible plan
from an aspirational one.

Extrapolating from the measured throughput, a full fine-tune pass over
the larger corpus requires approximately 6,450 optimiser steps, or
around thirty-six minutes; both corpora plus the cross-direction
evaluations come to roughly an hour and a half. Semester 2, which adds a
second generator corpus, a third corpus and feature ablations, is
budgeted at about ten hours of GPU time across twelve weeks — well
inside what free-tier access provides, with checkpointing enabled so
that an interrupted session resumes rather than restarts.

The other resource worth calculating is memory, and the constraint there
is the character n-gram matrix rather than the model: roughly 340 MB as
a sparse matrix for the larger corpus, which is comfortable on the
available hardware and is the reason vectorisation happens inside the
pipeline rather than once over the whole corpus.

### 6.4 What this evidence supports, and what it does not

**It supports:** that the pipeline runs end to end and is reproducible
from a clean clone; that three classical models and one transformer can
be compared on equal terms; that within-corpus performance is in line
with published figures on the same data; and that the compute and time
required for Semester 2 are within reach of the resources actually
available, with a contingency buffer sized against a quantified residual
risk exposure of approximately twenty-seven hours.

**It does not support:** any claim that these findings generalise beyond
two corpora. Each represents a single method of producing fake text, so
a cross-corpus comparison is partly a comparison of two production
methods rather than of two populations of deception. Five folds support
a confidence interval, not a significance test; McNemar's test is
scheduled for Semester 2. And nothing here establishes which model is
best in general.

Stating the second list is what makes the first one worth reading.
