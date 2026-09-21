"""Generate a small stand-in corpus so the pipeline runs without downloads.

This exists for three reasons: continuous integration has no network
access to the real corpora, a new machine should be able to run
``make demo`` immediately, and the D2 video needs the pipeline to run on
screen without a large download.

**These are not research data.** The generator builds reviews from
templates with two deliberately different "fake" styles -- an
over-enthusiastic human-written style and a flatter, hedged
machine-written style -- so that the cross-dataset drop the project
studies is visible in miniature. Numbers produced from this data belong
in no report. ``frd.datasets`` labels them ``synthetic_*`` so they can
never be confused with the real corpora in ``results.csv``.
"""

from __future__ import annotations

import argparse
import random

import pandas as pd

from .config import DATA_DIR, RANDOM_SEED, ensure_directories

HOTELS = ["the Grand Plaza", "the Riverside Inn", "the Metro Suites", "the Park Lodge"]
PRODUCTS = ["the wireless earbuds", "the coffee grinder", "the desk lamp", "the backpack"]
CITIES = ["Edinburgh", "Kuala Lumpur", "Aktobe", "Penang", "Glasgow"]

GENUINE_OPENERS = [
    "Stayed three nights in {city} and {subject} was fine overall.",
    "Bought {subject} in March and have used it most days since.",
    "We arrived late and the front desk at {subject} sorted us out quickly.",
    "Not perfect but {subject} did the job for the price.",
]
GENUINE_DETAILS = [
    "The shower pressure was weak on the fourth floor, which the manager admitted.",
    "Battery lasts about five hours for me, not the eight the box claims.",
    "Breakfast stopped at nine sharp so we missed it on the Sunday.",
    "One of the screws was already loose, took ten minutes to fix.",
    "Parking cost extra and nobody mentioned that when booking.",
    "It is heavier than I expected but that has not been a problem.",
]
GENUINE_CLOSERS = [
    "Would book again if the price stays where it is.",
    "Fine for the money, would not pay more.",
    "Happy enough, minor complaints aside.",
    "Does what it says, nothing more.",
]

HUMAN_FAKE_OPENERS = [
    "I absolutely LOVED {subject}, it was the best experience of my life!",
    "My family and I had an amazing, wonderful, perfect stay at {subject}.",
    "I cannot recommend {subject} highly enough to everyone reading this!",
    "{subject} exceeded every single one of my expectations in every way.",
]
HUMAN_FAKE_DETAILS = [
    "The staff were incredibly friendly and made us feel like royalty from the moment we arrived.",
    "Everything was absolutely spotless and beautiful and luxurious beyond belief.",
    "I have travelled all over the world and nothing compares to this experience.",
    "My husband said it was the finest place he had ever seen in his entire life.",
    "You will not regret choosing this, I promise you that with all my heart.",
]
HUMAN_FAKE_CLOSERS = [
    "Five stars is not enough, I would give ten if I could!",
    "Book it now, you will thank me later!",
    "Simply the best, I will be back again and again!",
]

MACHINE_FAKE_OPENERS = [
    "This product offers a range of features that may appeal to many users.",
    "Overall, {subject} provides a generally positive experience for most customers.",
    "In terms of value, {subject} can be considered a reasonable option.",
    "Based on my experience, {subject} performs adequately in most situations.",
]
MACHINE_FAKE_DETAILS = [
    "The build quality appears to be reasonably solid, although individual results may vary.",
    "It is worth noting that the item generally meets expectations for its price range.",
    "Some users may find certain aspects more useful than others, depending on their needs.",
    "The overall design seems to balance functionality and appearance quite effectively.",
    "There are several aspects that could potentially be improved in future versions.",
]
MACHINE_FAKE_CLOSERS = [
    "In conclusion, this is a solid choice for those seeking this type of product.",
    "Overall, I would generally recommend it to potential buyers.",
    "It represents a reasonable option within its category.",
]


def _compose(opener, details, closer, subject, city, rng, n_details=2) -> str:
    parts = [opener.format(subject=subject, city=city)]
    parts.extend(rng.sample(details, k=min(n_details, len(details))))
    parts.append(rng.choice(closer))
    return " ".join(parts)


def build(kind: str, n: int, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Build ``n`` reviews, half genuine and half fake, for one style."""
    rng = random.Random(seed if kind == "human" else seed + 1)
    subjects = HOTELS if kind == "human" else PRODUCTS
    fake_openers = HUMAN_FAKE_OPENERS if kind == "human" else MACHINE_FAKE_OPENERS
    fake_details = HUMAN_FAKE_DETAILS if kind == "human" else MACHINE_FAKE_DETAILS
    fake_closers = HUMAN_FAKE_CLOSERS if kind == "human" else MACHINE_FAKE_CLOSERS

    rows = []
    for index in range(n):
        subject = rng.choice(subjects)
        city = rng.choice(CITIES)
        is_fake = index % 2 == 1
        if is_fake:
            text = _compose(
                rng.choice(fake_openers), fake_details, fake_closers, subject, city, rng
            )
        else:
            text = _compose(
                rng.choice(GENUINE_OPENERS),
                GENUINE_DETAILS,
                GENUINE_CLOSERS,
                subject,
                city,
                rng,
            )
        rows.append({"text": text, "label": int(is_fake)})

    frame = pd.DataFrame(rows)
    return frame.sample(frac=1.0, random_state=seed).reset_index(drop=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--n", type=int, default=400, help="reviews per corpus")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    args = parser.parse_args(argv)

    ensure_directories()
    for kind, filename in (
        ("human", "synthetic_human.csv"),
        ("machine", "synthetic_machine.csv"),
    ):
        frame = build(kind, args.n, seed=args.seed)
        path = DATA_DIR / filename
        frame.to_csv(path, index=False)
        print(f"wrote {len(frame):>5} reviews to {path}")

    print("\nThese are generated placeholders, not research data.")
    print("Run 'make data' to fetch the real corpora before reporting anything.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
