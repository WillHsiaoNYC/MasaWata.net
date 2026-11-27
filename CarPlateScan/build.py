#!/usr/bin/env python3
"""Build the Car Plate Scan landing page in every supported app language variant."""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))

from scripts.asc_web import PageOptions, build_site


APP_STORE_ID = "6825007024"
SCREENSHOT_LOCALE = "en-US"
# Website routes follow the studio's locale naming. Include all app UI variants.
WEBSITE_LOCALES = (
    "en-US", "ar-SA", "ca", "cs", "da", "de-DE", "el", "es-ES", "es-MX",
    "fi", "fr-CA", "fr-FR", "he", "hi", "hr", "hu", "id", "it", "ko",
    "nl-NL", "no", "pl", "pt-BR", "pt-PT", "ro", "ru", "sk", "sl-SI",
    "sv", "tr", "uk", "vi", "zh-Hans", "zh-Hant",
)


def load_website_copy(site_dir: Path = ROOT) -> tuple[dict, dict[str, PageOptions]]:
    locales = {}
    options = {}
    copy_dir = site_dir / "locales"
    if {path.stem for path in copy_dir.glob("*.json")} != set(WEBSITE_LOCALES):
        raise RuntimeError("Car Plate Scan website copy must cover all 34 app locale variants")
    for locale in WEBSITE_LOCALES:
        copy = json.loads((copy_dir / f"{locale}.json").read_text(encoding="utf-8"))
        brand = "車牌掃描" if locale == "zh-Hant" else "Car Plate Scan"
        locales[locale] = {
            "name": "Car Plate Scan: License Reader" if locale == "en-US" else brand,
            "subtitle": copy["subtitle"],
            "promotionalText": copy["promotionalText"],
            "description": "\n\n".join(copy["description"]),
        }
        options[locale] = PageOptions(
            brand_name=brand,
            store_label=copy["storeLabel"],
            skip_label=copy["skipLink"],
            privacy_label=copy["processingLabel"],
            processing_notice="\n\n".join(copy["processing"]),
            screenshot_locale=SCREENSHOT_LOCALE,
            screenshot_alts=tuple(copy["screenshotAlts"]),
            screenshot_note=copy["screenshotNote"] if locale != SCREENSHOT_LOCALE else "",
        )
    return {"locales": locales}, options


def build() -> int:
    metadata, options = load_website_copy()
    return build_site(
        site_dir=ROOT,
        base_url="https://masawata.net/CarPlateScan",
        app_store_id=APP_STORE_ID,
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
        locale_stylesheets={
            locale: ("css/style.css",) if locale == "en-US" else ("../css/style.css",)
            for locale in WEBSITE_LOCALES
        },
        metadata=metadata,
        locale_page_options=options,
    )


if __name__ == "__main__":
    raise SystemExit(0 if build() else 1)
