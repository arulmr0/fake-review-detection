# Design
<img width="1240" height="1060" alt="image" src="https://github.com/user-attachments/assets/ec1830c8-1e88-49ea-b6c4-521c9932f75e" />


## Components

```
                 +---------------------+
  data/  ---->   |  datasets.py        |  text / label / source
                 |  loaders + specs    |
                 +----------+----------+
                            |
                 +----------v----------+
                 |  preprocess.py      |  clean, dedupe, stratified split
                 +----------+----------+
                            |
            +---------------+---------------+
            |                               |
 +----------v----------+        +-----------v-----------+
 |  models.py          |        |  transformer.py       |
 |  TF-IDF pipelines   |        |  distilroberta        |
 |  LR / SVM / RF      |        |  (optional deps, GPU) |
 +----------+----------+        +-----------+-----------+
            |                               |
            +---------------+---------------+
                            |
                 +----------v----------+
                 |  evaluate.py        |  macro-F1, per-class, confusion
                 +----------+----------+
                            |
        +-------------------+-------------------+
        |                                       |
+-------v--------+                    +---------v---------+
| experiments.py |  results.csv  ---> |   figures.py      |
| within / cross |  (+ commit hash)   |   PNG figures     |
| / combined     |                    +-------------------+
+-------+--------+
        |
 +------v-------+
 |   cli.py     |  the artefact: train / predict / info
 +--------------+
```

The UML component diagram and its `.drawio` source live beside this file
and are the version used in D1.

## Decisions worth recording

**Vectorisation lives inside the pipeline.** Every classical model is a
scikit-learn `Pipeline` whose first step is the vectoriser. Fitting a
vectoriser on the whole corpus before splitting leaks test vocabulary
into training and inflates every score. This cost a day in Week 5
(issue #7) and is now guarded by a test.

**One canonical schema.** Every loader returns `text` / `label` /
`source`, so adding a third corpus in Semester 2 needs a `DatasetSpec`
entry and nothing else. `source` travels with the rows, which is what
makes the cross-dataset condition expressible at all.

**The results log is append-only.** Each row carries the commit hash,
the seed and the condition, so a number in D1 can be traced to the code
that produced it. Nothing is overwritten; figures filter to the latest
run so a stale row can never quietly change a chart.

**The transformer is isolated.** `torch` and `transformers` stay out of
the core requirements so a fresh clone runs the baselines and the whole
test suite without a multi-gigabyte download — which is also what lets
CI run at all.

**Light cleaning.** Aggressive normalisation was tried and dropped: it
strips exactly the stylistic signal (punctuation, capitalisation,
hedging) that distinguishes the two fake-review populations. Casing is
handled inside the vectoriser, where it can be switched per run.

## Semester 2

The demonstrator loads the same saved model the CLI produces, so no
model code changes. The spike is on `spike/streamlit` (issue #36).
