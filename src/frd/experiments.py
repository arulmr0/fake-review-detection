"""The Semester 1 experiment runner.

Three training conditions are run for every classical model:

``within``
    Train and test on the same corpus, five-fold cross-validated. This is
    the number most published work reports.
``cross``
    Train on one corpus, test on the whole of the other. This is the
    condition that motivates the project: performance falls sharply,
    which is the central finding of the D1 feasibility study.
``combined``
    Train on both corpora pooled, test on each held-out split. Included to
    show whether simply mixing the data closes the gap. It does not close
    it, but it narrows it.

Every run appends a row to ``results/results.csv`` carrying the git commit
hash, so a number in the report can always be traced back to the code
that produced it.
"""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone

import pandas as pd
from sklearn.model_selection import StratifiedKFold

from . import datasets, models
from .config import N_FOLDS, RANDOM_SEED, RESULTS_DIR, ensure_directories
from .evaluate import mean_and_interval, score
from .preprocess import clean_frame, prepare

RESULTS_FILE = RESULTS_DIR / "results.csv"


def git_commit() -> str:
    """Short hash of the current commit, or 'unknown' outside a checkout."""
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def run_within(frame: pd.DataFrame, model_name: str, vectoriser: str = "word") -> dict:
    """Five-fold cross-validation on a single corpus."""
    frame = clean_frame(frame)
    folds = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_SEED)
    fold_scores = []

    for train_index, test_index in folds.split(frame["text"], frame["label"]):
        model = models.build(model_name, vectoriser=vectoriser)
        model.fit(frame["text"].iloc[train_index], frame["label"].iloc[train_index])
        predictions = model.predict(frame["text"].iloc[test_index])
        fold_scores.append(score(frame["label"].iloc[test_index], predictions))

    mean_f1, interval = mean_and_interval([s.macro_f1 for s in fold_scores])
    mean_accuracy, _ = mean_and_interval([s.accuracy for s in fold_scores])

    return {
        "condition": "within",
        "model": model_name,
        "vectoriser": vectoriser,
        "train_source": frame["source"].iloc[0],
        "test_source": frame["source"].iloc[0],
        "macro_f1": mean_f1,
        "macro_f1_ci95": interval,
        "accuracy": mean_accuracy,
        "n_train": int(len(frame) * (N_FOLDS - 1) / N_FOLDS),
        "n_test": int(len(frame) / N_FOLDS),
    }


def run_cross(
    train_frame: pd.DataFrame,
    test_frame: pd.DataFrame,
    model_name: str,
    vectoriser: str = "word",
) -> dict:
    """Train on one corpus, test on the whole of another."""
    train_frame = clean_frame(train_frame)
    test_frame = clean_frame(test_frame)

    model = models.build(model_name, vectoriser=vectoriser)
    model.fit(train_frame["text"], train_frame["label"])
    predictions = model.predict(test_frame["text"])
    scores = score(test_frame["label"], predictions)

    return {
        "condition": "cross",
        "model": model_name,
        "vectoriser": vectoriser,
        "train_source": train_frame["source"].iloc[0],
        "test_source": test_frame["source"].iloc[0],
        "macro_f1": scores.macro_f1,
        "macro_f1_ci95": 0.0,
        "accuracy": scores.accuracy,
        "n_train": len(train_frame),
        "n_test": len(test_frame),
    }


def run_combined(
    frames: list[pd.DataFrame], model_name: str, vectoriser: str = "word"
) -> list[dict]:
    """Train on both corpora pooled; report on each corpus's own test split."""
    splits = {}
    for frame in frames:
        train, _, test = prepare(frame)
        splits[frame["source"].iloc[0]] = (train, test)

    pooled_train = pd.concat([train for train, _ in splits.values()], ignore_index=True)
    model = models.build(model_name, vectoriser=vectoriser)
    model.fit(pooled_train["text"], pooled_train["label"])

    rows = []
    for source, (_, test) in splits.items():
        scores = score(test["label"], model.predict(test["text"]))
        rows.append(
            {
                "condition": "combined",
                "model": model_name,
                "vectoriser": vectoriser,
                "train_source": "+".join(sorted(splits)),
                "test_source": source,
                "macro_f1": scores.macro_f1,
                "macro_f1_ci95": 0.0,
                "accuracy": scores.accuracy,
                "n_train": len(pooled_train),
                "n_test": len(test),
            }
        )
    return rows


def run_all(human_key: str, machine_key: str, vectorisers=("word", "char")) -> pd.DataFrame:
    """Every model in every condition. This is what ``make experiments`` calls."""
    human, machine = datasets.load_pair(human_key, machine_key)
    rows: list[dict] = []

    for vectoriser in vectorisers:
        for model_name in models.REGISTRY:
            rows.append(run_within(human, model_name, vectoriser))
            rows.append(run_within(machine, model_name, vectoriser))
            rows.append(run_cross(human, machine, model_name, vectoriser))
            rows.append(run_cross(machine, human, model_name, vectoriser))
            rows.extend(run_combined([human, machine], model_name, vectoriser))

    frame = pd.DataFrame(rows)
    frame.insert(0, "run_at", datetime.now(timezone.utc).isoformat(timespec="seconds"))
    frame.insert(1, "commit", git_commit())
    frame.insert(2, "seed", RANDOM_SEED)
    return frame


def append_results(frame: pd.DataFrame, path=RESULTS_FILE) -> None:
    """Append to the results log, creating it with a header if absent."""
    ensure_directories()
    frame.to_csv(path, mode="a", header=not path.exists(), index=False)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run the Semester 1 experiments.")
    parser.add_argument("--human", default="ott", help="human-written corpus key")
    parser.add_argument("--machine", default="salminen", help="machine-generated corpus key")
    parser.add_argument(
        "--vectorisers",
        default="word,char",
        help="comma-separated list of vectorisers to run",
    )
    args = parser.parse_args(argv)

    frame = run_all(
        args.human,
        args.machine,
        vectorisers=tuple(v.strip() for v in args.vectorisers.split(",") if v.strip()),
    )
    append_results(frame)

    summary = frame.pivot_table(
        index=["model", "vectoriser"],
        columns="condition",
        values="macro_f1",
        aggfunc="mean",
    ).round(3)
    print(summary.to_string())
    print(f"\n{len(frame)} rows appended to {RESULTS_FILE}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
