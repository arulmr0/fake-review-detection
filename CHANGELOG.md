# Changelog

## v0.2.0-feasibility — 24 November 2026

The code behind D1 and the D2 video. Tagged after verifying the README's
reproduction steps from a clean clone on a second machine.

- Dataset loaders for both corpora with a canonical `text` / `label` /
  `source` schema, plus an offline stand-in generator
- Reproducible preprocessing: cleaning, deduplication, stratified
  70/15/15 split at seed 42
- Three TF–IDF baselines (Logistic Regression, Linear SVM, Random
  Forest) with word and character n-grams
- Optional `distilroberta-base` fine-tune
- Experiment runner covering within-dataset, cross-dataset and combined
  training, appending to `results/results.csv` with the commit hash
- Macro-F1 with per-class precision, recall and confusion matrices
- Command-line predictor (train / predict / info)
- Script-generated figures
- 28 tests and GitHub Actions CI on Python 3.11 and 3.12

### Rejected along the way
Git LFS for the datasets, MLflow for tracking, DVC for data versioning,
and SMOTE oversampling — the last on evidence (macro-F1 0.88 → 0.84),
the rest on effort disproportionate to a single-student project.
