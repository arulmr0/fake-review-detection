"""Tests for dataset loading and description."""

import pytest

from frd import datasets
from frd.datasets import DatasetNotFoundError


def test_load_returns_the_canonical_columns(fixture_dir):
    frame = datasets.load("synthetic_human", data_dir=fixture_dir)
    assert list(frame.columns) == datasets.COLUMNS


def test_labels_are_binary_integers(fixture_dir):
    frame = datasets.load("synthetic_machine", data_dir=fixture_dir)
    assert set(frame["label"].unique()) <= {0, 1}
    assert frame["label"].dtype.kind == "i"


def test_source_column_identifies_the_corpus(fixture_dir):
    frame = datasets.load("synthetic_human", data_dir=fixture_dir)
    assert frame["source"].unique().tolist() == ["synthetic_human"]


def test_missing_dataset_raises_an_actionable_error(tmp_path):
    with pytest.raises(DatasetNotFoundError, match="make data"):
        datasets.load("ott", data_dir=tmp_path)


def test_unknown_key_is_rejected(fixture_dir):
    with pytest.raises(KeyError):
        datasets.load("not_a_dataset", data_dir=fixture_dir)


def test_describe_reports_the_statistics_used_in_d1(fixture_dir):
    stats = datasets.describe(datasets.load("synthetic_human", data_dir=fixture_dir))
    assert stats["n_reviews"] == stats["n_fake"] + stats["n_genuine"]
    assert 0.0 < stats["fake_proportion"] < 1.0
    assert stats["mean_words"] > 0
    assert stats["vocabulary_size"] > 0
