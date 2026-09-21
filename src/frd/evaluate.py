"""Metrics and reporting.

Macro-F1 is the headline number throughout, with per-class precision and
recall and a confusion matrix reported alongside it. Accuracy is recorded
but never quoted on its own: the splits are close to balanced but not
exactly, and a model that collapses onto the majority class can still
look respectable on accuracy.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)


@dataclass
class Scores:
    """One evaluation of one model on one test set."""

    accuracy: float
    macro_f1: float
    precision_genuine: float
    recall_genuine: float
    precision_fake: float
    recall_fake: float
    support_genuine: int
    support_fake: int
    confusion: list[list[int]] = field(default_factory=list)

    def as_row(self) -> dict:
        """Flatten for the results CSV (the confusion matrix is stringified)."""
        row = asdict(self)
        row["confusion"] = ";".join(
            ",".join(str(value) for value in line) for line in self.confusion
        )
        return row


def score(y_true, y_pred) -> Scores:
    """Compute every metric reported in D1 for one set of predictions."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    precision, recall, _, support = precision_recall_fscore_support(
        y_true, y_pred, labels=[0, 1], zero_division=0
    )
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])

    return Scores(
        accuracy=round(float(accuracy_score(y_true, y_pred)), 4),
        macro_f1=round(float(f1_score(y_true, y_pred, average="macro", zero_division=0)), 4),
        precision_genuine=round(float(precision[0]), 4),
        recall_genuine=round(float(recall[0]), 4),
        precision_fake=round(float(precision[1]), 4),
        recall_fake=round(float(recall[1]), 4),
        support_genuine=int(support[0]),
        support_fake=int(support[1]),
        confusion=matrix.tolist(),
    )


def mean_and_interval(values) -> tuple[float, float]:
    """Mean and half-width of a 95% interval across folds.

    Uses the normal approximation, which is what the D1 tables report.
    With five folds this is indicative rather than rigorous, and the
    report says so: proper paired significance testing (McNemar) is
    Semester 2 work.
    """
    values = np.asarray(values, dtype=float)
    if values.size < 2:
        return round(float(values.mean()), 4), 0.0
    half_width = 1.96 * values.std(ddof=1) / np.sqrt(values.size)
    return round(float(values.mean()), 4), round(float(half_width), 4)
