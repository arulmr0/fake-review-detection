"""Project-wide paths and constants.

Every experiment reads its randomness from :data:`RANDOM_SEED` and its
split proportions from :data:`SPLIT`, so a result can be reproduced from
the commit hash alone. Nothing here should be changed casually: the
numbers reported in D1 are tied to these values.
"""

from __future__ import annotations

from pathlib import Path

#: Repository root, resolved from this file's location.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
MODELS_DIR = PROJECT_ROOT / "models"

#: Fixed so that every reported number is reproducible.
RANDOM_SEED = 42

#: Stratified train / validation / test proportions.
SPLIT = {"train": 0.70, "validation": 0.15, "test": 0.15}

#: Number of folds for cross-validated baselines.
N_FOLDS = 5

#: Headline metric. Accuracy is deliberately not the headline: the splits
#: are close to balanced but not exactly, and per-class behaviour matters.
PRIMARY_METRIC = "macro_f1"

LABEL_NAMES = {0: "genuine", 1: "fake"}


def ensure_directories() -> None:
    """Create the output directories if they do not already exist."""
    for directory in (DATA_DIR, RESULTS_DIR, FIGURES_DIR, MODELS_DIR):
        directory.mkdir(parents=True, exist_ok=True)
