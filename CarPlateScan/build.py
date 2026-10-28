#!/usr/bin/env python3
"""Build the English Car Plate Scan page from its checked-in ASC snapshot."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

from scripts.asc_web import PageOptions, build_site, load_metadata


# This is a planned date, not a time-based switch to a download claim.
PLANNED_RELEASE = "November 28, 2026"
SCREENSHOT_ALTS = (
    "Car Plate Scan overview — scan it, keep the details",
    "Camera or photos, capture history, maps and favorites",
    "Scan license plates from the camera or photos",
    "Review and edit a plate reading before saving",
    "Search saved plate capture history",
    "Browse captures by map and date",
    "Find favorite plates",
)


def build() -> int:
    description = load_metadata(ROOT)["locales"]["en-US"]["description"]
    marker = "Car Plate Scan records what you capture."
    if marker not in description:
        raise RuntimeError("Review the updated ASC description's privacy and processing paragraphs")
    notice = description[description.index(marker):]
    return build_site(
        site_dir=ROOT,
        base_url="https://masawata.net/CarPlateScan",
        app_store_id="6825007024",
        icon_path="images/app-icon.png",
        privacy_url="#privacy-processing",
        support_url="mailto:fitnessstoryapp@gmail.com",
        accent="#a7dfd2",
        accent_dark="#83c7b7",
        background="#0b171c",
        surface="#13232c",
        ink="#f4f8f7",
        muted="#b5c8ca",
        line="#30464d",
        color_scheme="dark",
        locale_stylesheets={"en-US": ("css/style.css",)},
        page_options=PageOptions(
            brand_name="Car Plate Scan",
            planned_release=PLANNED_RELEASE,
            processing_notice=notice,
            screenshot_alts=SCREENSHOT_ALTS,
        ),
    )


if __name__ == "__main__":
    raise SystemExit(0 if build() else 1)
