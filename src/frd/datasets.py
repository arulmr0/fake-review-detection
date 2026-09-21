"""Dataset loading for the fake review detection project.

Two real corpora are used in Semester 1:

* ``ott``       -- Ott et al. (2011) deceptive opinion spam corpus.
                   Human-written deceptive hotel reviews, crowdsourced.
* ``salminen``  -- Salminen et al. (2022) fake reviews dataset.
                   Machine-generated fake product reviews.

Neither is committed to the repository (see ``data/README.md``); run
``python -m frd.download`` to fetch them, or ``python -m frd.make_synthetic``
to generate a small stand-in so the pipeline can be exercised offline.

Every loader returns the same shape: a DataFrame with columns
``text`` (str) and ``label`` (int, 1 = fake, 0 = genuine), plus a
``source`` column naming the corpus.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .config import DATA_DIR

COLUMNS = ["text", "label", "source"]


@dataclass(frozen=True)
class DatasetSpec:
    """Where a corpus lives and which of its columns we need."""

    key: str
    filename: str
    text_column: str
    label_column: str
    #: value of ``label_column`` that means "this review is fake"
    fake_value: object
    description: str


SPECS: dict[str, DatasetSpec] = {
    "ott": DatasetSpec(
        key="ott",
        filename="deceptive-opinion.csv",
        text_column="text",
        label_column="deceptive",
        fake_value="deceptive",
        description="Ott et al. (2011) crowdsourced deceptive hotel reviews",
    ),
    "salminen": DatasetSpec(
        key="salminen",
        filename="fake_reviews_dataset.csv",
        text_column="text_",
        label_column="label",
        fake_value="CG",  # computer generated
        description="Salminen et al. (2022) machine-generated product reviews",
    ),
    "synthetic_human": DatasetSpec(
        key="synthetic_human",
        filename="synthetic_human.csv",
        text_column="text",
        label_column="label",
        fake_value=1,
        description="Generated stand-in for a human-written deception corpus",
    ),
    "synthetic_machine": DatasetSpec(
        key="synthetic_machine",
        filename="synthetic_machine.csv",
        text_column="text",
        label_column="label",
        fake_value=1,
        description="Generated stand-in for a machine-generated corpus",
    ),
}


class DatasetNotFoundError(FileNotFoundError):
    """Raised when a corpus has not been downloaded or generated yet."""


def available() -> list[str]:
    """Return the keys of every corpus currently present on disk."""
    return [key for key, spec in SPECS.items() if (DATA_DIR / spec.filename).exists()]


def load(key: str, data_dir: Path | None = None) -> pd.DataFrame:
    """Load one corpus into the canonical ``text`` / ``label`` / ``source`` frame.

    Parameters
    ----------
    key:
        One of the keys in :data:`SPECS`.
    data_dir:
        Directory to read from. Defaults to the project ``data/`` directory;
        tests pass their own fixture directory here.
    """
    if key not in SPECS:
        raise KeyError(f"unknown dataset {key!r}; expected one of {sorted(SPECS)}")

    spec = SPECS[key]
    root = Path(data_dir) if data_dir is not None else DATA_DIR
    path = root / spec.filename

    if not path.exists():
        raise DatasetNotFoundError(
            f"{spec.description} not found at {path}. "
            "Run 'make data' to download the real corpora, or "
            "'python -m frd.make_synthetic' for the offline stand-in."
        )

    raw = pd.read_csv(path)
    missing = {spec.text_column, spec.label_column} - set(raw.columns)
    if missing:
        raise ValueError(f"{path} is missing expected column(s): {sorted(missing)}")

    frame = pd.DataFrame(
        {
            "text": raw[spec.text_column].astype(str),
            "label": (raw[spec.label_column] == spec.fake_value).astype(int),
            "source": spec.key,
        }
    )
    frame = frame[frame["text"].str.strip().astype(bool)].reset_index(drop=True)
    return frame[COLUMNS]


def load_pair(human_key: str, machine_key: str, data_dir: Path | None = None):
    """Load the human-written and machine-generated corpora together."""
    return load(human_key, data_dir), load(machine_key, data_dir)


def describe(frame: pd.DataFrame) -> dict[str, float]:
    """Descriptive statistics used in the D1 feasibility section."""
    words = frame["text"].str.split().str.len()
    return {
        "n_reviews": int(len(frame)),
        "n_fake": int(frame["label"].sum()),
        "n_genuine": int((frame["label"] == 0).sum()),
        "fake_proportion": round(float(frame["label"].mean()), 4),
        "mean_words": round(float(words.mean()), 2),
        "median_words": float(words.median()),
        "vocabulary_size": int(
            len({token.lower() for text in frame["text"] for token in text.split()})
        ),
    }
