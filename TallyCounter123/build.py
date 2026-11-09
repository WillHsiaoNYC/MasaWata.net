#!/usr/bin/env python3
"""Build the Tally Counter 123 site from the checked-in live ASC snapshot."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

from scripts.asc_web import build_site


def build() -> int:
    return build_site(
        site_dir=ROOT,
        base_url="https://masawata.net/TallyCounter123",
        app_store_id="6769252146",
        icon_path="images/icon-512.png",
        privacy_url="https://masawata.net/privacy-policy.html",
        support_url="https://masawata.net/",
        accent="#c2682f",
        accent_dark="#a8541f",
    )


if __name__ == "__main__":
    raise SystemExit(0 if build() else 1)
