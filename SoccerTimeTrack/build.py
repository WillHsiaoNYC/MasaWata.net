#!/usr/bin/env python3
"""Build the Soccer Time Track site from the checked-in live ASC snapshot."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

from scripts.asc_web import build_site


def build() -> int:
    return build_site(
        site_dir=ROOT,
        base_url="https://masawata.net/SoccerTimeTrack",
        app_store_id="6791397600",
        icon_path="images/app-icon.png",
        privacy_url="https://masawata.net/SoccerTimeTrack/privacy-policy.html",
        support_url="https://masawata.net/SoccerTimeTrack/support.html",
        accent="#00C96B",
        accent_dark="#008D49",
        background="#020907",
        surface="#071B12",
        ink="#F5FFF9",
        muted="#9CB4A7",
        line="#153C2A",
        color_scheme="dark",
    )


if __name__ == "__main__":
    raise SystemExit(0 if build() else 1)
