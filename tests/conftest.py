"""Shared fixtures.

Tests never touch ``data/``: they read the committed fixture in
``tests/fixtures`` instead. That fixture is tiny and generated, which is
what lets continuous integration run with no network access -- the two
CI failures in Week 8 were caused by tests that assumed the real corpora
were present (issue #31).
"""

from pathlib import Path

import pandas as pd
import pytest

FIXTURE_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def fixture_dir() -> Path:
    return FIXTURE_DIR


@pytest.fixture
def sample_frame() -> pd.DataFrame:
    """A small canonical frame: text / label / source, both classes present."""
    return pd.read_csv(FIXTURE_DIR / "synthetic_human.csv").assign(source="fixture")


@pytest.fixture
def sample_pair(fixture_dir):
    """Two corpora with different fake-review styles, as the project uses."""
    human = pd.read_csv(fixture_dir / "synthetic_human.csv").assign(source="fixture_human")
    machine = pd.read_csv(fixture_dir / "synthetic_machine.csv").assign(
        source="fixture_machine"
    )
    return human, machine
