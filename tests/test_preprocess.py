"""Tests for cleaning and splitting."""

import pandas as pd
import pytest

from frd.config import SPLIT
from frd.preprocess import clean_frame, clean_text, split_frame


def test_clean_text_strips_markup_and_whitespace():
    assert clean_text("<b>Great</b>   stay\n\nhere") == "Great stay here"


def test_clean_text_replaces_urls_with_a_placeholder():
    assert "<url>" in clean_text("see https://example.com/deal for more")
    assert "example.com" not in clean_text("see https://example.com/deal for more")


def test_clean_text_handles_non_strings():
    assert clean_text(None) == ""
    assert clean_text(float("nan")) == ""


def test_clean_frame_removes_duplicates_that_would_leak_between_splits(sample_frame):
    duplicated = pd.concat([sample_frame, sample_frame.head(5)], ignore_index=True)
    cleaned = clean_frame(duplicated)
    assert len(cleaned) == cleaned["text"].nunique()


def test_split_proportions_are_correct(sample_frame):
    train, validation, test = split_frame(sample_frame)
    total = len(train) + len(validation) + len(test)
    assert total == len(sample_frame)
    assert abs(len(train) / total - SPLIT["train"]) < 0.05
    assert abs(len(test) / total - SPLIT["test"]) < 0.05


def test_split_is_stratified(sample_frame):
    train, validation, test = split_frame(sample_frame)
    overall = sample_frame["label"].mean()
    for part in (train, validation, test):
        assert abs(part["label"].mean() - overall) < 0.1


def test_split_is_deterministic_for_a_fixed_seed(sample_frame):
    first, _, _ = split_frame(sample_frame, seed=7)
    second, _, _ = split_frame(sample_frame, seed=7)
    pd.testing.assert_frame_equal(first, second)


def test_split_refuses_a_single_class_frame(sample_frame):
    one_class = sample_frame[sample_frame["label"] == 0]
    with pytest.raises(ValueError, match="single class"):
        split_frame(one_class)
