"""Cleaning and splitting.

The pipeline is deliberately thin. Aggressive normalisation was tried in
Week 6 and hurt the transformer (see ``docs/02-research/literature.md``),
so the default cleaner only removes markup, URLs and repeated whitespace,
and leaves casing and punctuation alone. Classical models lowercase
inside the vectoriser instead, where it can be switched off per run.
"""

from __future__ import annotations

import html
import re

import pandas as pd
from sklearn.model_selection import train_test_split

from .config import RANDOM_SEED, SPLIT

_URL = re.compile(r"https?://\S+|www\.\S+")
_TAG = re.compile(r"<[^>]+>")
_WHITESPACE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Normalise one review without destroying stylistic signal."""
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = _TAG.sub(" ", text)
    text = _URL.sub(" <url> ", text)
    text = _WHITESPACE.sub(" ", text)
    return text.strip()


def clean_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply :func:`clean_text` and drop reviews left empty or duplicated.

    Duplicate removal matters more than it looks: several fake-review
    corpora contain near-identical rows, and leaving them in leaks
    between the train and test splits.
    """
    out = frame.copy()
    out["text"] = out["text"].map(clean_text)
    out = out[out["text"].str.len() > 0]
    out = out.drop_duplicates(subset=["text"]).reset_index(drop=True)
    return out


def split_frame(frame: pd.DataFrame, seed: int = RANDOM_SEED):
    """Stratified 70 / 15 / 15 split.

    Returns
    -------
    (train, validation, test) : tuple of DataFrame
    """
    if frame["label"].nunique() < 2:
        raise ValueError("cannot stratify a split on a single class")

    holdout_size = SPLIT["validation"] + SPLIT["test"]
    train, holdout = train_test_split(
        frame,
        test_size=holdout_size,
        random_state=seed,
        stratify=frame["label"],
    )
    # Split the holdout in half so validation and test are the same size.
    validation, test = train_test_split(
        holdout,
        test_size=SPLIT["test"] / holdout_size,
        random_state=seed,
        stratify=holdout["label"],
    )
    return (
        train.reset_index(drop=True),
        validation.reset_index(drop=True),
        test.reset_index(drop=True),
    )


def prepare(frame: pd.DataFrame, seed: int = RANDOM_SEED):
    """Clean then split, which is the order every experiment uses."""
    return split_frame(clean_frame(frame), seed=seed)
