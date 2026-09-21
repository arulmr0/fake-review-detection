"""Figure generation for D1 and the D2 video.

Every figure is produced by this script rather than by hand, so when a
result changes the figures change with it. Run ``make figures`` after
``make experiments``.
"""

from __future__ import annotations

import argparse

import matplotlib

matplotlib.use("Agg")  # no display in CI or on a headless machine
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from .config import FIGURES_DIR, ensure_directories  # noqa: E402
from .experiments import RESULTS_FILE  # noqa: E402

# Colour-blind safe, and distinguishable in greyscale when printed.
CONDITION_COLOURS = {
    "within": "#3B6EA5",
    "combined": "#C57B2C",
    "cross": "#8C3A3A",
}
CONDITION_LABELS = {
    "within": "Within dataset",
    "combined": "Combined training",
    "cross": "Cross dataset",
}


def _latest(frame: pd.DataFrame) -> pd.DataFrame:
    """Keep only the most recent run, so figures never mix commits."""
    return frame[frame["run_at"] == frame["run_at"].max()]


def condition_comparison(frame: pd.DataFrame, out_path=None):
    """Grouped bars: macro-F1 per model, one bar per training condition.

    This is the figure the whole report turns on -- the cross-dataset bar
    sitting well below the within-dataset bar for every model.
    """
    frame = _latest(frame)
    pivot = frame.pivot_table(
        index="model", columns="condition", values="macro_f1", aggfunc="mean"
    )
    order = [c for c in ("within", "combined", "cross") if c in pivot.columns]
    pivot = pivot[order]

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    width = 0.8 / len(order)
    positions = range(len(pivot.index))

    for offset, condition in enumerate(order):
        ax.bar(
            [p + offset * width for p in positions],
            pivot[condition].values,
            width=width,
            label=CONDITION_LABELS[condition],
            color=CONDITION_COLOURS[condition],
        )

    ax.set_xticks([p + width * (len(order) - 1) / 2 for p in positions])
    ax.set_xticklabels([name.replace("_", " ") for name in pivot.index])
    ax.set_ylabel("Macro-F1")
    ax.set_ylim(0, 1)
    ax.axhline(0.5, color="#999999", linewidth=0.8, linestyle="--")
    ax.text(len(pivot.index) - 0.45, 0.515, "chance", fontsize=8, color="#666666")
    ax.set_title("Detection performance falls when the fake-review source changes")
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    out_path = out_path or FIGURES_DIR / "condition_comparison.png"
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return out_path


def vectoriser_comparison(frame: pd.DataFrame, out_path=None):
    """Word versus character n-grams, split by training condition."""
    frame = _latest(frame)
    if frame["vectoriser"].nunique() < 2:
        return None

    pivot = frame.pivot_table(
        index="condition", columns="vectoriser", values="macro_f1", aggfunc="mean"
    ).reindex([c for c in ("within", "combined", "cross") if c in frame["condition"].unique()])

    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    pivot.plot(kind="bar", ax=ax, color=["#3B6EA5", "#6BA368"], width=0.7, rot=0)
    ax.set_ylabel("Macro-F1")
    ax.set_xlabel("")
    ax.set_ylim(0, 1)
    ax.set_xticklabels([CONDITION_LABELS.get(c, c) for c in pivot.index])
    ax.set_title("Character n-grams hold up better under distribution shift")
    ax.legend(title="", frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    out_path = out_path or FIGURES_DIR / "vectoriser_comparison.png"
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return out_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate every figure.")
    parser.add_argument("--results", default=RESULTS_FILE, help="results CSV")
    args = parser.parse_args(argv)

    ensure_directories()
    frame = pd.read_csv(args.results)

    for path in (condition_comparison(frame), vectoriser_comparison(frame)):
        if path is not None:
            print(f"wrote {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
