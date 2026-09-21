# Detecting Human-Written and Machine-Generated Fake Reviews

A comparative machine learning study. BSc Honours project, Heriot-Watt
University, 2026/27.

**This repository is the single source of truth for the project.** Code,
documents, planning and task tracking all live here. If you are my
supervisor, everything you need is linked from this page.

---

## Start here

| What | Where |
|---|---|
| Task tracker | [Issues](../../issues) — one issue per task, each with an acceptance criterion |
| Progress against deadlines | [Milestones](../../milestones) — named after the fixed dates, not topics |
| Board | [Projects](../../projects) — Backlog → Next → In Progress → Blocked → In Review → Done |
| Planning documents | [`docs/01-planning/`](docs/01-planning) — scope, MoSCoW, roadmap, risk register |
| Research and D1 | [`docs/02-research/`](docs/02-research) — literature table, D1 outline |
| Ethics | [`docs/04-ethics/`](docs/04-ethics) |
| Supervision record | [`docs/06-meetings/`](docs/06-meetings) — meeting log and the D2 video script |
| Results | [`results/results.csv`](results) — one row per run, tagged with the commit hash |

## The question

Most published fake-review detectors are trained and tested on a single
corpus and report a single headline score. Two quite different things get
called a fake review: text a paid human wrote to deceive, and text a
language model generated. This project asks whether a detector trained on
one transfers to the other.

The Semester 1 answer, from the feasibility study in D1, is that it does
not. Within a corpus the models do well; tested across corpora every one
of them falls sharply, and the transformer's advantage largely
disappears. That gap is the subject of the dissertation.

## Semester 1 scope

Semester 1 delivers the proposal, the research report and evidence that
the Semester 2 plan is achievable — not a finished system.

- **D1** Project Proposal and Research Report — due 26 November 2026
- **D2** Preparation and Feasibility Video — due 26 November 2026
- **D4** Project meetings and management — this repository, plus the
  journals submitted on Canvas
- Ethics — submitted 28 October 2026, ahead of the 30 October deadline

## Quick start

```bash
git clone https://github.com/<username>/fake-review-detection.git
cd fake-review-detection
python -m venv .venv && source .venv/bin/activate
make setup
make demo
```

`make demo` generates a small stand-in corpus, runs every model in every
condition, writes the figures and trains the CLI model. It takes about a
minute and needs no downloads, which is what makes the repository
runnable in CI and on a fresh machine.

Then classify something:

```bash
python -m frd.cli predict "Absolutely the best hotel ever, five stars is not enough!!"
#    fake  (0.777)  Absolutely the best hotel ever, five stars is not enough!!
```

> **The stand-in data is not research data.** It is generated from
> templates so the pipeline can be exercised offline, and it is
> separable almost perfectly, which the real corpora are not. Any number
> produced from `synthetic_*` is a smoke test. Run `make data` before
> reporting anything.

## Working with the real corpora

```bash
make data            # fetch what can be fetched, report what cannot
make experiments     # every model, every condition -> results/results.csv
make figures         # regenerate the figures from the results
```

| Corpus | Fake reviews are | Source |
|---|---|---|
| Ott et al. (2011) | human-written, crowdsourced | Kaggle (manual download — needs an account) |
| Salminen et al. (2022) | machine-generated | [OSF](https://osf.io/tyue9/) |

Neither is committed: one file exceeds GitHub's 100 MB limit, both are
publicly available, and Git LFS was evaluated and rejected. See
[`data/README.md`](data/README.md) for sources, licences and checksums.

## Repository layout

```
src/frd/            the package
  config.py         paths, seed, split proportions — change nothing here casually
  datasets.py       loaders; every corpus becomes text / label / source
  preprocess.py     cleaning, deduplication, stratified split
  models.py         the three classical pipelines
  transformer.py    distilroberta fine-tune (optional dependencies)
  evaluate.py       macro-F1, per-class metrics, confusion matrices
  experiments.py    within / cross / combined runner -> results.csv
  figures.py        every figure, regenerated from the results
  cli.py            the artefact: train, predict, info
  download.py       fetch and verify the real corpora
  make_synthetic.py the offline stand-in generator
tests/              28 tests, run in CI on every push
notebooks/          exploration and baselines
docs/               planning, research, design, ethics, testing, meetings
results/            results.csv and the generated figures
```

## How the work is tracked

Every task is an issue with an acceptance criterion in the body. Labels
carry the MoSCoW priority (`priority:must` / `should` / `could`) as well
as the kind of work. Branches are named after the issue
(`14-tfidf-baseline`), merged into `dev` by pull request, and commit
messages close their issue — so the code history and the task history are
the same record.

Every experiment row in `results/results.csv` carries the commit hash and
the seed that produced it, which means any number in D1 can be traced
back to the exact code.

## Reproducibility

Seed 42 throughout, a stratified 70/15/15 split, pinned dependencies, and
vectorisation inside the cross-validation fold rather than fitted on the
whole corpus first. That last one is not a detail: fitting it first leaks
test information into training and inflates every score.

## Licence

MIT — see [LICENSE](LICENSE). The datasets carry their own licences and
are not redistributed here.
