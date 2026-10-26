#!/usr/bin/env python3
"""Validate generated product sites against checked-in ASC snapshots."""

from __future__ import annotations

import html
from html.parser import HTMLParser
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITES = (
    "CarPlateScan",
    "FitnessStory",
    "IceTimeTrack",
    "SoccerTimeTrack",
    "TallyCounter123",
    "TimerOnMe",
    "WhereWasI",
)
CANONICAL_LOCALES = {"TimerOnMe": {"es-ES": "es-MX"}}
FULL_DESCRIPTION_SITES = set(SITES) - {"TallyCounter123"}
FITNESS_STORY_ZH_HANT_PROMO_MARKERS = (
    "揮汗有禮！截圖有據！",
    '健身故事終身版限時 <span class="campaign-sale-price">NT$10</span>',
    "原價 <del>NT$980</del>",
    "優惠只到 9/30",
    "本網頁專屬優惠碼",
    "請用已安裝健身故事的設備點下右側兌換按鈕",
    "https://500.gov.tw/registrant/",
    "https://apps.apple.com/redeem?ctx=offercodes&amp;id=6748090363&amp;code=SWEATGIFT",
    "../css/zh-Hant-sweatgift.css",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def page_for(site: Path, locale: str) -> Path:
    return site / "index.html" if locale == "en-US" else site / locale / "index.html"


class PageReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = set()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("src", "href"):
            if key in attrs:
                self.references.append(attrs[key])


def validate_car_plate_scan(site: Path, raw: str, metadata: dict, assets: dict) -> list[str]:
    errors: list[str] = []
    if set(metadata["locales"]) != {"en-US"} or set(assets) != {"en-US"}:
        fail(errors, "CarPlateScan: website must remain English only")
    if len(assets.get("en-US", [])) != 7 or any(
        item["displayType"] != "APP_IPHONE_61" for item in assets.get("en-US", [])
    ):
        fail(errors, "CarPlateScan: expected seven APP_IPHONE_61 ASC screenshots")
    expected_shots = [f"images/asc/en-US/{index:02d}-phone.webp" for index in range(1, 8)]
    if re.findall(r'<figure><img src="([^"]+)"', raw) != expected_shots:
        fail(errors, "CarPlateScan: gallery must preserve all seven screenshots in ASC order")
    if raw.count("Planned release: November 30, 2026") != 2:
        fail(errors, "CarPlateScan: planned release must appear in hero and final action panel")
    if any(marker in raw for marker in ("apple-itunes-app", 'class="asc-languages"', "Download on the App Store")):
        fail(errors, "CarPlateScan: pre-release page contains a download claim or language selector")
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)
    try:
        schema = json.loads(schemas[0]) if len(schemas) == 1 else {}
        if schema.get("operatingSystem") != "iOS" or any(key in schema for key in ("downloadUrl", "offers", "aggregateRating", "datePublished")):
            fail(errors, "CarPlateScan: incorrect pre-release structured data")
    except (ValueError, IndexError):
        fail(errors, "CarPlateScan: invalid structured data")
    if 'href="#privacy-processing">Privacy &amp; processing</a>' not in raw:
        fail(errors, "CarPlateScan: footer must link to its accurate processing information")
    parser = PageReferences()
    parser.feed(raw)
    for reference in parser.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        target = ROOT / unquote(url.path).lstrip("/") if url.path.startswith("/") else site / unquote(url.path)
        if not url.path:
            if url.fragment and url.fragment not in parser.ids:
                fail(errors, f"CarPlateScan: missing anchor {reference}")
        elif not (target.is_file() or (target.is_dir() and (target / "index.html").is_file())):
            fail(errors, f"CarPlateScan: missing local URL {reference}")
    return errors


def validate_catalog() -> list[str]:
    errors: list[str] = []
    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)[1])
    catalog = next(item["mainEntity"] for item in schema["@graph"] if item["@type"] == "CollectionPage")
    entries = catalog["itemListElement"]
    if catalog["numberOfItems"] != len(entries) or [entry["position"] for entry in entries] != list(range(1, len(entries) + 1)):
        fail(errors, "Studio: catalog count/positions do not match entries")
    if f'Index · {len(entries):02d}' not in raw or raw.count('<li class="app">') != len(entries):
        fail(errors, "Studio: visible catalog count does not match structured data")
    upcoming = [entry["item"] for entry in entries if entry["item"]["url"] == "https://masawata.net/CarPlateScan/"]
    if len(upcoming) != 1 or any(key in upcoming[0] for key in ("downloadUrl", "offers")):
        fail(errors, "Studio: expected one Car Plate Scan entry without unverified download/price claims")
    if 'href="/CarPlateScan/"' not in raw or "Planned release: November 30, 2026" not in raw:
        fail(errors, "Studio: missing Car Plate Scan navigation or planned release")
    index = ET.parse(ROOT / "sitemap.xml")
    if not any(node.text == "https://masawata.net/CarPlateScan/sitemap.xml" for node in index.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")):
        fail(errors, "Studio: sitemap index omits CarPlateScan")
    return errors


def validate_site(name: str) -> list[str]:
    errors: list[str] = []
    site = ROOT / name
    metadata = json.loads((site / "asc-metadata.json").read_text(encoding="utf-8"))
    locales = metadata["locales"]
    assets = json.loads((site / "asc-assets.json").read_text(encoding="utf-8"))
    if set(locales) != set(assets):
        fail(errors, f"{name}: metadata and ASC screenshot locale sets differ")

    sitemap = ET.parse(site / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9", "xhtml": "http://www.w3.org/1999/xhtml"}
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
        if CANONICAL_LOCALES.get(name, {}).get(locale, locale) == locale
    }
    if urls != expected_urls:
        fail(errors, f"{name}: sitemap URLs do not exactly match canonical ASC locales")

    expected_alternates = {
        locale: f"https://masawata.net/{name}/" if locale == "en-US"
        else f"https://masawata.net/{name}/{locale}/"
        for locale in locales
    }
    expected_alternates["x-default"] = f"https://masawata.net/{name}/"
    for entry in sitemap.findall("sm:url", namespace):
        alternates = {
            node.get("hreflang"): node.get("href")
            for node in entry.findall("xhtml:link", namespace)
        }
        # Tally uses HTML hreflang only; the shared generator also emits XML alternates.
        if name != "TallyCounter123" and alternates != expected_alternates:
            fail(errors, f"{name}: sitemap alternates do not exactly match ASC locales")

    for locale, content in locales.items():
        page = page_for(site, locale)
        if not page.is_file():
            fail(errors, f"{name} {locale}: generated page missing")
            continue
        raw = page.read_text(encoding="utf-8")
        if name == "CarPlateScan":
            errors.extend(validate_car_plate_scan(site, raw, metadata, assets))
        readable = html.unescape(raw)
        canonical_locale = CANONICAL_LOCALES.get(name, {}).get(locale, locale)
        canonical = expected_alternates[canonical_locale]
        if re.findall(r'<link rel="canonical" href="([^"]+)"', raw) != [canonical]:
            fail(errors, f"{name} {locale}: expected canonical {canonical}")
        if re.search(r'<meta\s+name="robots"[^>]*content="[^"]*noindex', raw, re.I):
            fail(errors, f"{name} {locale}: product page must be indexable")
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
    errors: list[str] = validate_catalog()
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
    print("\nAll product sites match their checked-in ASC locale and screenshot manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
