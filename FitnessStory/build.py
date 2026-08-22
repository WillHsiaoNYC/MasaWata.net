#!/usr/bin/env python3
"""Build the Fitness Story site from the checked-in live ASC snapshot."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

from scripts.asc_web import build_site


def build() -> int:
    return build_site(
        site_dir=ROOT,
        base_url="https://masawata.net/FitnessStory",
        app_store_id="6748090363",
        icon_path="images/Fitness Story.png",
        privacy_url="https://masawata.net/privacy-policy.html",
        support_url="https://masawata.net/",
        accent="#007AFF",
        accent_dark="#0055CC",
        aliases={"de": "de-DE", "es": "es-ES", "fr": "fr-FR", "pt": "pt-BR"},
    )


if __name__ == "__main__":
    raise SystemExit(0 if build() else 1)
