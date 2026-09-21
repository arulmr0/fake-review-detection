# Test plan

28 tests, run locally as a pre-commit hook and in CI on every push and
pull request, against Python 3.11 and 3.12.

## What is tested and why

| Area | Tests | What it protects |
|---|---|---|
| `preprocess` | 8 | Split proportions, stratification, determinism under a fixed seed, duplicate removal, markup and URL handling |
| `datasets` | 6 | Canonical schema, binary integer labels, source tagging, actionable errors for a missing corpus |
| `models` / `evaluate` | 11 | Every registered model builds; vectorisation is inside the pipeline; macro-F1 penalises a majority-class collapse; each experiment condition runs |
| `cli` | 3 | Train, save, reload, predict — the artefact end to end |

## Two tests worth singling out

**`test_vectorisation_happens_inside_the_pipeline`** asserts the first
pipeline step is the vectoriser. It exists because the Week 5 leak was
invisible in the output: the code ran, and the scores simply looked
better than they should have.

**`test_score_penalises_a_majority_class_collapse`** builds a model that
predicts one class everywhere and asserts accuracy is 0.6 while macro-F1
is below 0.5. It encodes the supervisor's Week 7 point about metric
choice in a form that cannot be forgotten.

## CI

No network access to the real corpora, so tests read the 60-row
fixtures committed in `tests/fixtures/`. Two early CI runs failed
because tests assumed `data/` was populated (issue #31); the fixtures
are the fix. CI also smoke-tests the whole pipeline — generate, run
experiments, make figures, train, predict — so a break in the wiring
between modules fails the build even when every unit test passes.

## Not covered

- `transformer.py` — needs optional dependencies and a GPU; exercised by
  hand on Colab and recorded in `results/results.csv`.
- `download.py` network paths — mocking the download to test the
  download is close to testing nothing. The checksum helper is the part
  that matters and is straightforward.
