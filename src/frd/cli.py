"""Command-line predictor -- the Semester 1 artefact.

    python -m frd.cli train --human synthetic_human --machine synthetic_machine
    python -m frd.cli predict "This hotel was absolutely the best ever!!!"
    python -m frd.cli predict --file reviews.txt

The demonstrator planned for Semester 2 wraps this same saved model, so
the interface is deliberately small: train, predict, info.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd

from . import datasets, models
from .config import MODELS_DIR, RANDOM_SEED, ensure_directories
from .evaluate import score
from .preprocess import clean_text, prepare

DEFAULT_MODEL_PATH = MODELS_DIR / "baseline.joblib"


def train(
    human_key: str,
    machine_key: str,
    model_name: str,
    path: Path,
    data_dir: Path | None = None,
) -> dict:
    """Train on both corpora pooled and save the fitted pipeline.

    ``data_dir`` exists so the tests can train from ``tests/fixtures``
    without touching the project's ``data/`` directory.
    """
    ensure_directories()
    frames = [datasets.load(human_key, data_dir), datasets.load(machine_key, data_dir)]

    train_parts, test_parts = [], []
    for frame in frames:
        train_part, _, test_part = prepare(frame)
        train_parts.append(train_part)
        test_parts.append(test_part)

    train_frame = pd.concat(train_parts, ignore_index=True)
    test_frame = pd.concat(test_parts, ignore_index=True)

    model = models.build(model_name)
    model.fit(train_frame["text"], train_frame["label"])
    scores = score(test_frame["label"], model.predict(test_frame["text"]))

    metadata = {
        "model": model_name,
        "trained_on": [human_key, machine_key],
        "seed": RANDOM_SEED,
        "n_train": len(train_frame),
        "n_test": len(test_frame),
        "test_macro_f1": scores.macro_f1,
    }
    joblib.dump({"model": model, "metadata": metadata}, path)
    return metadata


def load_model(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"no model at {path}. Run 'python -m frd.cli train' first."
        )
    return joblib.load(path)


def predict(texts: list[str], path: Path) -> list[dict]:
    """Score one or more reviews. Returns label plus confidence where available."""
    bundle = load_model(path)
    model = bundle["model"]
    cleaned = [clean_text(text) for text in texts]
    predictions = model.predict(cleaned)

    confidences: list[float | None]
    if hasattr(model, "predict_proba"):
        confidences = [float(max(row)) for row in model.predict_proba(cleaned)]
    else:
        # LinearSVC has no probabilities; report the margin instead so the
        # output is still informative rather than silently missing.
        confidences = [abs(float(value)) for value in model.decision_function(cleaned)]

    return [
        {
            "text": text[:120] + ("..." if len(text) > 120 else ""),
            "prediction": "fake" if int(label) == 1 else "genuine",
            "confidence": round(confidence, 4),
        }
        for text, label, confidence in zip(
            texts, predictions, confidences, strict=True
        )
    ]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="frd", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    train_parser = sub.add_parser("train", help="train and save the baseline model")
    train_parser.add_argument("--human", default="ott")
    train_parser.add_argument("--machine", default="salminen")
    train_parser.add_argument("--model", default="logistic_regression")
    train_parser.add_argument("--out", type=Path, default=DEFAULT_MODEL_PATH)

    predict_parser = sub.add_parser("predict", help="classify one or more reviews")
    predict_parser.add_argument("text", nargs="*", help="review text")
    predict_parser.add_argument("--file", type=Path, help="file with one review per line")
    predict_parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)

    info_parser = sub.add_parser("info", help="show the saved model's metadata")
    info_parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)

    args = parser.parse_args(argv)

    if args.command == "train":
        metadata = train(args.human, args.machine, args.model, args.out)
        print(json.dumps(metadata, indent=2))
        print(f"\nsaved to {args.out}")
        return 0

    if args.command == "info":
        print(json.dumps(load_model(args.model_path)["metadata"], indent=2))
        return 0

    texts = list(args.text)
    if args.file:
        texts.extend(
            line.strip() for line in args.file.read_text().splitlines() if line.strip()
        )
    if not texts:
        print("nothing to classify: pass review text or --file", file=sys.stderr)
        return 2

    for result in predict(texts, args.model_path):
        print(f"{result['prediction']:>7}  ({result['confidence']:.3f})  {result['text']}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
