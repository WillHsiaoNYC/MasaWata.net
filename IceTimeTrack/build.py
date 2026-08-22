#!/usr/bin/env python3
"""Build the Ice Time Track site from the checked-in live ASC snapshot."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

from scripts.asc_web import build_site


def build() -> int:
    return build_site(
        site_dir=ROOT,
        base_url="https://masawata.net/IceTimeTrack",
        app_store_id="6758258172",
        icon_path="images/app-icon.png",
        privacy_url="https://masawata.net/privacy-policy.html",
        support_url="https://masawata.net/",
        accent="#FFB81C",
        accent_dark="#C98400",
        background="#0D0D0D",
        surface="#1A1A1A",
        ink="#FFFFFF",
        muted="#A0A0A0",
        line="#2A2A2A",
        color_scheme="dark",
        aliases={"de": "de-DE", "es": "es-MX", "fr": "fr-FR", "nb": "no"},
    )


if __name__ == "__main__":
    raise SystemExit(0 if build() else 1)
