"""Fetch the real corpora and verify them against recorded checksums.

The datasets are not committed (see ``data/README.md``): one exceeds
GitHub's 100 MB file limit, both are publicly available, and Git LFS was
evaluated and rejected. Instead the repository records where each file
came from and what its SHA-256 should be, and this script reproduces the
``data/`` directory on any machine.

The Ott corpus is distributed through Kaggle, which requires an account,
so it cannot be fetched unattended. The script says so plainly rather
than failing with a network error.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from .config import DATA_DIR, ensure_directories

#: filename -> (url or None, expected sha256 or None, note)
SOURCES: dict[str, dict] = {
    "deceptive-opinion.csv": {
        "url": None,
        "sha256": None,
        "note": (
            "Ott et al. (2011) deceptive opinion spam corpus.\n"
            "  Manual download: https://www.kaggle.com/datasets/rtatman/"
            "deceptive-opinion-spam-corpus\n"
            "  Kaggle requires a signed-in account, so this cannot be automated.\n"
            "  Save the CSV into data/ under this exact filename."
        ),
    },
    "fake_reviews_dataset.csv": {
        "url": "https://osf.io/download/tyue9/",
        "sha256": None,  # fill in after the first verified download
        "note": (
            "Salminen et al. (2022) fake reviews dataset, hosted on OSF.\n"
            "  Project page: https://osf.io/tyue9/"
        ),
    },
}


def sha256(path: Path, chunk_size: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(filename: str, force: bool = False) -> bool:
    """Download one dataset. Returns True if the file is present afterwards."""
    ensure_directories()
    spec = SOURCES[filename]
    target = DATA_DIR / filename

    if target.exists() and not force:
        print(f"[ok]   {filename} already present ({target.stat().st_size / 1e6:.1f} MB)")
        return True

    if spec["url"] is None:
        print(f"[skip] {filename} cannot be downloaded automatically.\n       {spec['note']}")
        return False

    print(f"[get]  {filename} from {spec['url']}")
    try:
        with urlopen(spec["url"], timeout=120) as response:
            target.write_bytes(response.read())
    except (URLError, TimeoutError, OSError) as error:
        print(f"[fail] {filename}: {error}\n       {spec['note']}")
        return False

    digest = sha256(target)
    if spec["sha256"] and digest != spec["sha256"]:
        print(
            f"[fail] {filename} checksum mismatch\n"
            f"       expected {spec['sha256']}\n"
            f"       got      {digest}"
        )
        return False

    print(f"[ok]   {filename} ({target.stat().st_size / 1e6:.1f} MB) sha256={digest[:16]}...")
    return True


def verify() -> None:
    """Print the checksum of every dataset currently on disk."""
    for filename in SOURCES:
        path = DATA_DIR / filename
        if path.exists():
            print(f"{filename}  {sha256(path)}")
        else:
            print(f"{filename}  (absent)")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="re-download even if present")
    parser.add_argument("--verify", action="store_true", help="print checksums and exit")
    args = parser.parse_args(argv)

    if args.verify:
        verify()
        return 0

    results = {name: fetch(name, force=args.force) for name in SOURCES}
    missing = [name for name, ok in results.items() if not ok]
    if missing:
        print(
            "\nSome datasets are not in place: "
            + ", ".join(missing)
            + "\nThe pipeline still runs on the generated stand-in: "
            "python -m frd.make_synthetic"
        )
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
