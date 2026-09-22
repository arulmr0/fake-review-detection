"""Model definitions for the feasibility baselines.

Four configurations are compared in Semester 1. The three classical ones
are built here as scikit-learn pipelines so that vectorisation happens
*inside* the cross-validation fold -- fitting the vectoriser on the whole
corpus first is the leak that cost a day in Week 5 (issue #7).

The transformer lives in ``frd.transformer`` because it needs optional
dependencies and a GPU to be practical.
"""

from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from .config import RANDOM_SEED

#: Word-level vectoriser settings shared by the classical models.
WORD_TFIDF = dict(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True,
    strip_accents="unicode",
)

#: Character n-grams. The Week 9 ablation found these carry most of the
#: performance on machine-generated text, so they are on by default.
CHAR_TFIDF = dict(
    analyzer="char_wb",
    ngram_range=(3, 5),
    min_df=2,
    sublinear_tf=True,
)


def _vectoriser(kind: str) -> TfidfVectorizer:
    if kind == "word":
        return TfidfVectorizer(**WORD_TFIDF)
    if kind == "char":
        return TfidfVectorizer(**CHAR_TFIDF)
    raise ValueError(f"unknown vectoriser {kind!r}; expected 'word' or 'char'")


def logistic_regression(vectoriser: str = "word") -> Pipeline:
    return Pipeline(
        [
            ("tfidf", _vectoriser(vectoriser)),
            (
                "clf",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )


def linear_svm(vectoriser: str = "word") -> Pipeline:
    return Pipeline(
        [
            ("tfidf", _vectoriser(vectoriser)),
            (
                "clf",
                LinearSVC(class_weight="balanced", random_state=RANDOM_SEED),
            ),
        ]
    )


def random_forest(vectoriser: str = "word") -> Pipeline:
    return Pipeline(
        [
            ("tfidf", _vectoriser(vectoriser)),
            (
                "clf",
                RandomForestClassifier(
                    n_estimators=300,
                    class_weight="balanced",
                    n_jobs=-1,
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )


#: Name -> factory. The experiment runner iterates over this mapping, so
#: adding a model here is enough to include it in every results table.
REGISTRY = {
    "logistic_regression": logistic_regression,
    "linear_svm": linear_svm,
    "random_forest": random_forest,
}


def build(name: str, vectoriser: str = "word") -> Pipeline:
    """Construct a model by name."""
    if name not in REGISTRY:
        raise KeyError(f"unknown model {name!r}; expected one of {sorted(REGISTRY)}")
    return REGISTRY[name](vectoriser=vectoriser)
