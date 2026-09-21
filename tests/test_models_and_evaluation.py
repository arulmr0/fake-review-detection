"""Tests for the model pipelines, the metrics, and the experiment runner."""

import numpy as np
import pytest

from frd import experiments, models
from frd.evaluate import mean_and_interval, score


def test_every_registered_model_builds():
    for name in models.REGISTRY:
        assert models.build(name) is not None


def test_vectorisation_happens_inside_the_pipeline():
    """Guards the Week 5 leak: the vectoriser must be a pipeline step,
    not something fitted on the whole corpus beforehand."""
    pipeline = models.build("logistic_regression")
    assert pipeline.steps[0][0] == "tfidf"


def test_unknown_model_is_rejected():
    with pytest.raises(KeyError):
        models.build("transformer_but_not_really")


def test_char_vectoriser_differs_from_word():
    word = models.build("linear_svm", vectoriser="word")
    char = models.build("linear_svm", vectoriser="char")
    assert word.named_steps["tfidf"].analyzer != char.named_steps["tfidf"].analyzer


def test_score_is_perfect_on_perfect_predictions():
    labels = [0, 1, 0, 1]
    result = score(labels, labels)
    assert result.macro_f1 == 1.0
    assert result.accuracy == 1.0


def test_score_penalises_a_majority_class_collapse():
    """A model predicting one class everywhere must not look good on
    macro-F1, which is why accuracy is not the headline metric."""
    y_true = [0] * 60 + [1] * 40
    y_pred = [0] * 100
    result = score(y_true, y_pred)
    assert result.accuracy == 0.6
    assert result.macro_f1 < 0.5


def test_confusion_matrix_is_two_by_two():
    result = score([0, 1, 1, 0], [0, 1, 0, 0])
    assert np.array(result.confusion).shape == (2, 2)


def test_mean_and_interval_returns_zero_width_for_one_value():
    mean, half_width = mean_and_interval([0.9])
    assert mean == 0.9
    assert half_width == 0.0


def test_within_condition_runs_and_scores_above_chance(sample_frame):
    row = experiments.run_within(sample_frame.assign(source="fixture"), "logistic_regression")
    assert row["condition"] == "within"
    assert row["macro_f1"] > 0.5


def test_cross_condition_records_both_sources(sample_pair):
    human, machine = sample_pair
    row = experiments.run_cross(human, machine, "linear_svm")
    assert row["train_source"] == "fixture_human"
    assert row["test_source"] == "fixture_machine"
    assert 0.0 <= row["macro_f1"] <= 1.0


def test_combined_condition_reports_one_row_per_corpus(sample_pair):
    rows = experiments.run_combined(list(sample_pair), "logistic_regression")
    assert len(rows) == 2
    assert {row["test_source"] for row in rows} == {"fixture_human", "fixture_machine"}
