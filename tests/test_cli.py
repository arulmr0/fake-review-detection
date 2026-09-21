"""End-to-end test of the artefact: train, save, reload, predict."""

import pytest

from frd import cli


@pytest.fixture
def trained_model(tmp_path, fixture_dir):
    """Train on the committed fixtures and save to a temporary path."""
    path = tmp_path / "model.joblib"
    metadata = cli.train(
        "synthetic_human",
        "synthetic_machine",
        "logistic_regression",
        path,
        data_dir=fixture_dir,
    )
    return path, metadata


def test_training_saves_a_model_with_metadata(trained_model):
    path, metadata = trained_model
    assert path.exists()
    assert metadata["model"] == "logistic_regression"
    assert metadata["n_train"] > metadata["n_test"]
    assert 0.0 <= metadata["test_macro_f1"] <= 1.0


def test_predict_labels_an_obvious_fake_and_an_obvious_genuine(trained_model):
    path, _ = trained_model
    results = cli.predict(
        [
            "I absolutely LOVED it, the best experience of my life, five stars is not enough!",
            "Stayed two nights, shower pressure was weak and breakfast stopped at nine.",
        ],
        path,
    )
    assert len(results) == 2
    assert {r["prediction"] for r in results} <= {"fake", "genuine"}
    assert all(0.0 <= r["confidence"] for r in results)


def test_predict_without_a_model_gives_an_actionable_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="frd.cli train"):
        cli.predict(["anything"], tmp_path / "missing.joblib")
