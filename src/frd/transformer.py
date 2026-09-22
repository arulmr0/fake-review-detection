"""Transformer fine-tuning (optional, GPU strongly recommended).

Kept out of ``frd.models`` because ``torch`` and ``transformers`` are not
in the core requirements: a fresh clone must be able to run the classical
baselines and the whole test suite without them. Install with::

    pip install -r requirements-transformer.txt

Loading ``roberta-base`` locally failed with an out-of-memory error in
Week 4, which is why the default here is ``distilroberta-base`` with a
short sequence length and small batch. Three epochs takes roughly twelve
minutes on a free-tier T4, and checkpointing is on because a lost session
cost a full run in Week 6 (issue #43).
"""

from __future__ import annotations

import argparse

import numpy as np

from . import datasets
from .config import MODELS_DIR, RANDOM_SEED, ensure_directories
from .evaluate import score
from .preprocess import prepare

DEFAULT_MODEL = "distilroberta-base"


def _require_dependencies():
    """Import the optional stack, with an actionable message if it is absent."""
    try:
        import torch  # noqa: F401
        from transformers import (  # noqa: F401
            AutoModelForSequenceClassification,
            AutoTokenizer,
            Trainer,
            TrainingArguments,
        )
    except ImportError as error:  # pragma: no cover - environment dependent
        raise SystemExit(
            "transformer dependencies are not installed.\n"
            "  pip install -r requirements-transformer.txt\n"
            f"  (import failed: {error})"
        ) from error
    return AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments


def fine_tune(
    human_key: str,
    machine_key: str,
    model_name: str = DEFAULT_MODEL,
    epochs: int = 3,
    batch_size: int = 16,
    max_length: int = 256,
):
    """Fine-tune on the pooled corpora and evaluate on each test split."""
    import torch
    from datasets import Dataset  # type: ignore

    (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        Trainer,
        TrainingArguments,
    ) = _require_dependencies()

    ensure_directories()
    torch.manual_seed(RANDOM_SEED)

    frames = {key: datasets.load(key) for key in (human_key, machine_key)}
    splits = {key: prepare(frame) for key, frame in frames.items()}

    import pandas as pd

    train_frame = pd.concat([train for train, _, _ in splits.values()], ignore_index=True)
    eval_frame = pd.concat([val for _, val, _ in splits.values()], ignore_index=True)

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize(batch):
        return tokenizer(
            batch["text"], truncation=True, padding="max_length", max_length=max_length
        )

    train_ds = Dataset.from_pandas(train_frame[["text", "label"]]).map(tokenize, batched=True)
    eval_ds = Dataset.from_pandas(eval_frame[["text", "label"]]).map(tokenize, batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    arguments = TrainingArguments(
        output_dir=str(MODELS_DIR / "transformer"),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=2e-5,
        warmup_ratio=0.1,
        eval_strategy="epoch",
        save_strategy="epoch",  # a lost Colab session cost a whole run once
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        seed=RANDOM_SEED,
        logging_steps=50,
        report_to=[],
    )

    trainer = Trainer(
        model=model, args=arguments, train_dataset=train_ds, eval_dataset=eval_ds
    )
    trainer.train()

    results = {}
    for key, (_, _, test_frame) in splits.items():
        test_ds = Dataset.from_pandas(test_frame[["text", "label"]]).map(tokenize, batched=True)
        predictions = np.argmax(trainer.predict(test_ds).predictions, axis=1)
        results[key] = score(test_frame["label"], predictions)
        print(f"{key}: macro-F1 {results[key].macro_f1}")

    trainer.save_model(str(MODELS_DIR / "transformer" / "best"))
    tokenizer.save_pretrained(str(MODELS_DIR / "transformer" / "best"))
    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--human", default="ott")
    parser.add_argument("--machine", default="salminen")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=256)
    args = parser.parse_args(argv)

    fine_tune(
        args.human,
        args.machine,
        model_name=args.model,
        epochs=args.epochs,
        batch_size=args.batch_size,
        max_length=args.max_length,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
