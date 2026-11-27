#!/usr/bin/env python3
"""Validate generated product sites against their checked-in copy and assets."""

from __future__ import annotations

import html
from html.parser import HTMLParser
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from CarPlateScan.build import APP_STORE_ID, SCREENSHOT_LOCALE, WEBSITE_LOCALES, load_website_copy


CARPLATE_STORE_URL = f"https://apps.apple.com/app/id{APP_STORE_ID}"
CARPLATE_URL = "https://masawata.net/CarPlateScan/"
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
FULL_DESCRIPTION_SITES = set(SITES)
FITNESS_STORY_ZH_HANT_PROMO_MARKERS = (
    "揮汗有禮！截圖有據！",
    "2026.09.01–11.30",
    "https://500.gov.tw/registrant/",
    "../css/zh-Hant-sweatgift.css",
)
EXPIRED_FITNESS_STORY_PROMO_MARKERS = (
    "優惠只到 9/30",
    "SWEATGIFT",
    "2026 年 9 月 30 日",
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
        self.tags = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("src", "href", "poster"):
            if key in attrs:
                self.references.append(attrs[key])


def validate_car_plate_scan(page: Path, locale: str, raw: str, options, alternates: dict) -> list[str]:
    errors: list[str] = []
    label = f"CarPlateScan {locale}"
    prefix = "" if locale == SCREENSHOT_LOCALE else "../"
    expected_shots = [f"{prefix}images/asc/{SCREENSHOT_LOCALE}/{index:02d}-phone.webp" for index in range(1, 8)]
    if re.findall(r'<figure><img src="([^"]+)"', raw) != expected_shots:
        fail(errors, f"{label}: gallery must preserve all seven screenshots in ASC order")
    if 'class="release-status"' in raw or "November 28, 2026" in raw:
        fail(errors, f"{label}: obsolete release date on product page")
    if raw.count(f'href="{CARPLATE_STORE_URL}" rel="noopener">{html.escape(options.store_label)}</a>') != 2:
        fail(errors, f"{label}: missing localized App Store links")
    if f'name="apple-itunes-app" content="app-id={APP_STORE_ID}"' not in raw:
        fail(errors, f"{label}: missing App Store banner")
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)
    try:
        schema = json.loads(schemas[0]) if len(schemas) == 1 else {}
        if schema.get("operatingSystem") != "iOS" or schema.get("sameAs") != CARPLATE_STORE_URL or "downloadUrl" in schema:
            fail(errors, f"{label}: incorrect App Store structured data")
    except (ValueError, IndexError):
        fail(errors, f"{label}: invalid structured data")
    readable = html.unescape(raw)
    if (
        f'href="#privacy-processing">{options.privacy_label}</a>' not in readable
        or any(paragraph not in readable for paragraph in options.processing_notice.split("\n\n"))
    ):
        fail(errors, f"{label}: missing localized processing notice or footer link")
    if options.screenshot_note and f'id="screenshot-note">{options.screenshot_note}</p>' not in readable:
        fail(errors, f"{label}: missing English screenshot disclosure")
    parser = PageReferences()
    parser.feed(raw)
    if ('html', {'lang': locale, 'dir': 'rtl' if locale in {'ar-SA', 'he'} else 'ltr'}) not in parser.tags:
        fail(errors, f"{label}: incorrect page language or direction")
    language_links = [attrs for tag, attrs in parser.tags if tag == "a" and "lang" in attrs]
    targets = {attrs["lang"]: urljoin(alternates[locale], attrs["href"]) for attrs in language_links}
    if len(language_links) != len(WEBSITE_LOCALES) or targets != {code: alternates[code] for code in WEBSITE_LOCALES}:
        fail(errors, f"{label}: language selector must link to every supported locale")
    if [attrs["lang"] for attrs in language_links[:2]] != ["en-US", "zh-Hant"]:
        fail(errors, f"{label}: Traditional Chinese must appear directly after English")
    if [attrs["lang"] for attrs in language_links if attrs.get("aria-current") == "page"] != [locale]:
        fail(errors, f"{label}: language selector must mark the active language")
    image_alts = {attrs["src"]: attrs["alt"] for tag, attrs in parser.tags if tag == "img" and "alt" in attrs}
    if tuple(image_alts.get(path) for path in expected_shots) != options.screenshot_alts:
        fail(errors, f"{label}: gallery must provide localized descriptions")
    videos = [attrs for tag, attrs in parser.tags if tag == "video"]
    if locale == "zh-Hant":
        if (
            'id="taiwan-live-demo"' not in raw
            or raw.index('id="taiwan-live-demo"') > raw.find('class="asc-hero"')
            or len(videos) != 1
            or not {"controls", "playsinline", "poster"} <= videos[0].keys()
            or videos[0].get("preload") != "metadata"
            or "autoplay" in videos[0]
            or not any(
                tag == "source" and attrs.get("src", "").endswith("/taiwan-live-plate-checks.mp4")
                for tag, attrs in parser.tags
            )
        ):
            fail(errors, f"{label}: expected the featured Taiwan demo with click-to-play video")
    elif videos or 'id="taiwan-live-demo"' in raw:
        fail(errors, f"{label}: Taiwan demo must appear only in Traditional Chinese")
    for reference in parser.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        target = ROOT / unquote(url.path).lstrip("/") if url.path.startswith("/") else page.parent / unquote(url.path)
        if not url.path:
            if url.fragment and url.fragment not in parser.ids:
                fail(errors, f"{label}: missing anchor {reference}")
        elif not (target.is_file() or (target.is_dir() and (target / "index.html").is_file())):
            fail(errors, f"{label}: missing local URL {reference}")
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
    carplate = [entry["item"] for entry in entries if entry["item"]["url"] == CARPLATE_URL]
    if len(carplate) != 1 or carplate[0].get("sameAs") != CARPLATE_STORE_URL:
        fail(errors, "Studio: expected one Car Plate Scan entry with its App Store listing")
    if 'href="/CarPlateScan/"' not in raw or f'href="{CARPLATE_STORE_URL}"' not in raw or "Planned release" in raw:
        fail(errors, "Studio: incorrect Car Plate Scan navigation or release copy")
    index = ET.parse(ROOT / "sitemap.xml")
    if not any(node.text == "https://masawata.net/CarPlateScan/sitemap.xml" for node in index.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")):
        fail(errors, "Studio: sitemap index omits CarPlateScan")
    pages = ET.parse(ROOT / "pages.xml")
    page_urls = {
        node.text
        for node in pages.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if node.text
    }
    expected_page_urls = {
        "https://masawata.net/",
        "https://masawata.net/privacy-policy.html",
        "https://masawata.net/SoccerTimeTrack/privacy-policy.html",
        "https://masawata.net/SoccerTimeTrack/support.html",
    }
    if page_urls != expected_page_urls:
        fail(errors, "Studio: pages.xml URLs do not match canonical static pages")
    return errors


def validate_site(name: str) -> list[str]:
    errors: list[str] = []
    site = ROOT / name
    assets = json.loads((site / "asc-assets.json").read_text(encoding="utf-8"))
    carplate_options = {}
    if name == "CarPlateScan":
        metadata, carplate_options = load_website_copy(site)
        english_shots = assets.get(SCREENSHOT_LOCALE, [])
        if set(assets) != {SCREENSHOT_LOCALE} or len(english_shots) != 7 or any(
            item["displayType"] != "APP_IPHONE_61" for item in english_shots
        ):
            fail(errors, "CarPlateScan: expected the shared set of seven APP_IPHONE_61 screenshots")
        if len(list((site / "images" / "asc" / SCREENSHOT_LOCALE).glob("*.webp"))) != len(english_shots):
            fail(errors, "CarPlateScan: screenshot files must match the shared ASC manifest")
    else:
        metadata = json.loads((site / "asc-metadata.json").read_text(encoding="utf-8"))
        if set(metadata["locales"]) != set(assets):
            fail(errors, f"{name}: metadata and ASC screenshot locale sets differ")
    locales = metadata["locales"]

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
        fail(errors, f"{name}: sitemap URLs do not exactly match canonical locales")

    canonical_map = CANONICAL_LOCALES.get(name, {})
    expected_alternates = {
        locale: (
            f"https://masawata.net/{name}/"
            if canonical_map.get(locale, locale) == "en-US"
            else f"https://masawata.net/{name}/{canonical_map.get(locale, locale)}/"
        )
        for locale in locales
    }
    expected_alternates["x-default"] = f"https://masawata.net/{name}/"
    for entry in sitemap.findall("sm:url", namespace):
        alternates = {
            node.get("hreflang"): node.get("href")
            for node in entry.findall("xhtml:link", namespace)
        }
        if alternates != expected_alternates:
            fail(errors, f"{name}: sitemap alternates do not exactly match site locales")

    for locale, content in locales.items():
        page = page_for(site, locale)
        if not page.is_file():
            fail(errors, f"{name} {locale}: generated page missing")
            continue
        raw = page.read_text(encoding="utf-8")
        if carplate_options:
            errors.extend(validate_car_plate_scan(page, locale, raw, carplate_options[locale], expected_alternates))
        readable = html.unescape(raw)
        canonical_locale = canonical_map.get(locale, locale)
        canonical = expected_alternates[canonical_locale]
        if re.findall(r'<link rel="canonical" href="([^"]+)"', raw) != [canonical]:
            fail(errors, f"{name} {locale}: expected canonical {canonical}")
        if "G-ZL852HY2Z4" not in raw:
            fail(errors, f"{name} {locale}: Google Analytics tag missing")
        for meta_marker in ('property="og:title"', 'property="og:image"', 'name="twitter:card"'):
            if meta_marker not in raw:
                fail(errors, f"{name} {locale}: social metadata missing ({meta_marker})")
        if re.search(r'<meta\s+name="robots"[^>]*content="[^"]*noindex', raw, re.I):
            fail(errors, f"{name} {locale}: product page must be indexable")
        for field in ("name", "subtitle", "promotionalText"):
            value = content.get(field)
            if value and value not in readable:
                fail(errors, f"{name} {locale}: {field} missing from page")
        if name in FULL_DESCRIPTION_SITES:
            for line in content.get("description", "").splitlines():
                value = line.strip().lstrip("•·- ").strip()
                if value and value not in readable:
                    fail(errors, f"{name} {locale}: description text missing: {value[:40]}")
        html_alternates = dict(
            re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', raw)
        )
        if html_alternates != expected_alternates:
            fail(errors, f"{name} {locale}: HTML hreflang alternates do not match canonical site locales")
        if locale in {"ar-SA", "he"} and 'dir="rtl"' not in raw:
            fail(errors, f"{name} {locale}: RTL direction missing")

        if name == "FitnessStory":
            if locale == "zh-Hant":
                for marker in FITNESS_STORY_ZH_HANT_PROMO_MARKERS:
                    if marker not in raw:
                        fail(errors, f"{name} {locale}: campaign marker missing: {marker}")
                for marker in EXPIRED_FITNESS_STORY_PROMO_MARKERS:
                    if marker in raw:
                        fail(errors, f"{name} {locale}: expired promo marker present: {marker}")
                if raw.find('class="campaign"') > raw.find('class="asc-hero"'):
                    fail(errors, f"{name} {locale}: campaign must appear before the app hero")
            elif any(
                marker in raw
                for marker in ("SWEATGIFT", "zh-Hant-sweatgift.css", 'class="campaign"')
            ):
                fail(errors, f"{name} {locale}: zh-Hant campaign leaked into this locale")

        if carplate_options:
            continue
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
        if not site_errors and site == "CarPlateScan":
            print(f"✓ {site}: {len(WEBSITE_LOCALES)} website locales")
        elif not site_errors:
            metadata = json.loads(
                (ROOT / site / "asc-metadata.json").read_text(encoding="utf-8")
            )
            print(f"✓ {site}: {len(metadata['locales'])} ASC locales")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("\nAll product sites match their checked-in copy and screenshot manifests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
