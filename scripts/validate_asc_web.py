#!/usr/bin/env python3
"""Validate generated product sites against checked-in live ASC snapshots."""

from __future__ import annotations

import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = (
    "FitnessStory",
    "IceTimeTrack",
    "SoccerTimeTrack",
    "TallyCounter123",
    "TimerOnMe",
    "WhereWasI",
)
FULL_DESCRIPTION_SITES = set(SITES) - {"TallyCounter123"}
FITNESS_STORY_ZH_HANT_PROMO_MARKERS = (
    "揮汗有禮！截圖有據！",
    "健身故事終身版限時 NT$10",
    "原價 <del>NT$980</del>",
    "優惠只到 9/30",
    "本網頁專屬優惠碼",
    "https://500.gov.tw/registrant/",
    "https://apps.apple.com/redeem?ctx=offercodes&amp;id=6748090363&amp;code=SWEATGIFT",
    "../css/zh-Hant-sweatgift.css",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def page_for(site: Path, locale: str) -> Path:
    return site / "index.html" if locale == "en-US" else site / locale / "index.html"


def validate_site(name: str) -> list[str]:
    errors: list[str] = []
    site = ROOT / name
    metadata = json.loads((site / "asc-metadata.json").read_text(encoding="utf-8"))
    locales = metadata["locales"]
    assets = json.loads((site / "asc-assets.json").read_text(encoding="utf-8"))
    if set(locales) != set(assets):
        fail(errors, f"{name}: metadata and ASC screenshot locale sets differ")

    sitemap = ET.parse(site / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = {
        node.text
        for node in sitemap.findall("sm:url/sm:loc", namespace)
        if node.text
    }
    expected_urls = {
        f"https://masawata.net/{name}/"
        if locale == "en-US"
        else f"https://masawata.net/{name}/{locale}/"
        for locale in locales
    }
    if urls != expected_urls:
        fail(errors, f"{name}: sitemap URLs do not exactly match ASC locales")

    for locale, content in locales.items():
        page = page_for(site, locale)
        if not page.is_file():
            fail(errors, f"{name} {locale}: generated page missing")
            continue
        raw = page.read_text(encoding="utf-8")
        readable = html.unescape(raw)
        for field in ("name", "subtitle", "promotionalText"):
            value = content.get(field)
            if value and value not in readable:
                fail(errors, f"{name} {locale}: ASC {field} missing from page")
        if name in FULL_DESCRIPTION_SITES:
            for line in content.get("description", "").splitlines():
                value = line.strip().lstrip("•·- ").strip()
                if value and value not in readable:
                    fail(errors, f"{name} {locale}: ASC description text missing: {value[:40]}")
        hreflangs = set(re.findall(r'hreflang="([^"]+)"', raw))
        expected_hreflangs = set(locales) | {"x-default"}
        if hreflangs != expected_hreflangs:
            fail(errors, f"{name} {locale}: hreflang set does not exactly match ASC locales")
        if locale in {"ar-SA", "he"} and 'dir="rtl"' not in raw:
            fail(errors, f"{name} {locale}: RTL direction missing")

        if name == "FitnessStory":
            if locale == "zh-Hant":
                for marker in FITNESS_STORY_ZH_HANT_PROMO_MARKERS:
                    if marker not in raw:
                        fail(errors, f"{name} {locale}: campaign marker missing: {marker}")
                if raw.find('class="campaign"') > raw.find('class="asc-hero"'):
                    fail(errors, f"{name} {locale}: campaign must appear before the app hero")
            elif any(
                marker in raw
                for marker in ("SWEATGIFT", "zh-Hant-sweatgift.css", 'class="campaign"')
            ):
                fail(errors, f"{name} {locale}: zh-Hant campaign leaked into this locale")

        screenshot_dir = site / "images" / "asc" / locale
        actual = sorted(screenshot_dir.glob("*.webp"))
        if len(actual) != len(assets[locale]):
            fail(
                errors,
                f"{name} {locale}: expected {len(assets[locale])} screenshots, found {len(actual)}",
            )
        for image in actual:
            expected_ref = (
                f"images/asc/{locale}/{image.name}"
                if locale == "en-US"
                else f"../images/asc/{locale}/{image.name}"
            )
            absolute_ref = f"/images/asc/{locale}/{image.name}"
            if expected_ref not in raw and absolute_ref not in raw:
                fail(errors, f"{name} {locale}: {image.name} is not referenced")
    return errors


def main() -> int:
    errors: list[str] = []
    for site in SITES:
        site_errors = validate_site(site)
        errors.extend(site_errors)
        if not site_errors:
            metadata = json.loads(
                (ROOT / site / "asc-metadata.json").read_text(encoding="utf-8")
            )
            print(f"✓ {site}: {len(metadata['locales'])} ASC locales")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("\nAll product sites match their checked-in live ASC locale and screenshot manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
