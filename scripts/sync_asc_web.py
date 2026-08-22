#!/usr/bin/env python3
"""Read live App Store Connect metadata/screenshots into the website.

This script is intentionally read-only with respect to App Store Connect. It
uses GET endpoints only, prefers checksum-matching local fastlane screenshots,
and downloads the ASC asset when a matching local source is unavailable.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import requests
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ASC_TOOLS = REPO_ROOT.parent / "iOS_submission_tools"


@dataclass(frozen=True)
class AppConfig:
    site: str
    bundle_id: str
    app_store_id: str
    local_screenshots: Path | None
    display_types: tuple[tuple[str, int | None], ...] = (("APP_IPHONE_67", None),)
    screenshot_fallback_locale: str | None = None


APPS = {
    "FitnessStory": AppConfig(
        "FitnessStory",
        "MasaWata.Fitness-Report",
        "6748090363",
        REPO_ROOT.parent / "FitnessReport/fastlane/screenshots",
    ),
    "IceTimeTrack": AppConfig(
        "IceTimeTrack",
        "MasaWata.Ice-Time-Track-Phone",
        "6758258172",
        None,
        (("APP_IPHONE_67", None), ("APP_WATCH_ULTRA", 2)),
        screenshot_fallback_locale="en-US",
    ),
    "SoccerTimeTrack": AppConfig(
        "SoccerTimeTrack",
        "MasaWata.SoccerTrack",
        "6791397600",
        REPO_ROOT.parent / "SoccerTrack/fastlane/screenshots",
    ),
    "TallyCounter123": AppConfig(
        "TallyCounter123",
        "net.MasaWata.TallyCounter123",
        "6769252146",
        REPO_ROOT.parent / "CounterOnMe/fastlane/screenshots",
    ),
    "TimerOnMe": AppConfig(
        "TimerOnMe",
        "MasaWata.Timer-on-Me",
        "6746874284",
        REPO_ROOT.parent / "TimerOnMe/fastlane/screenshots",
    ),
    "WhereWasI": AppConfig(
        "WhereWasI",
        "MasaWata.Where-was-I",
        "6758056060",
        REPO_ROOT.parent / "Where-Was-I/fastlane/screenshots",
    ),
}


def load_client(asc_tools: Path):
    sys.path.insert(0, str(asc_tools))
    from dotenv import load_dotenv
    from asc_common.client import AscClient

    load_dotenv(asc_tools / ".env")
    required = ("ASC_KEY_ID", "ASC_ISSUER_ID", "ASC_KEY_PATH")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise SystemExit(f"Missing ASC credentials: {', '.join(missing)}")
    return AscClient(
        os.environ["ASC_KEY_ID"],
        os.environ["ASC_ISSUER_ID"],
        os.environ["ASC_KEY_PATH"],
    )


def live_context(client, config: AppConfig) -> tuple[str, dict, list[dict], str | None]:
    app_id = client.find_app_id_by_bundle_id(config.bundle_id)
    if not app_id:
        raise RuntimeError(f"ASC app not found for {config.site}")
    versions = client._paged_get(
        f"/apps/{app_id}/appStoreVersions", {"filter[platform]": "IOS"}
    )
    live_versions = [
        item
        for item in versions
        if item.get("attributes", {}).get("appStoreState") == "READY_FOR_SALE"
        or item.get("attributes", {}).get("appVersionState") == "READY_FOR_DISTRIBUTION"
    ]
    if not live_versions:
        raise RuntimeError(f"No live iOS version found for {config.site}")
    version = live_versions[0]
    localizations = client._paged_get(
        f"/appStoreVersions/{version['id']}/appStoreVersionLocalizations"
    )
    app_info_id = client.get_live_app_info_id(app_id)
    return app_id, version, localizations, app_info_id


def sync_metadata(client, config: AppConfig, context) -> dict:
    _, version, version_localizations, app_info_id = context
    info_by_locale: dict[str, dict] = {}
    if app_info_id:
        for item in client.list_app_info_localizations(app_info_id):
            attrs = item.get("attributes", {})
            if attrs.get("locale"):
                info_by_locale[attrs["locale"]] = attrs

    locales: dict[str, dict] = {}
    for item in version_localizations:
        attrs = item.get("attributes", {})
        locale = attrs.get("locale")
        if not locale:
            continue
        info = info_by_locale.get(locale, {})
        locales[locale] = {
            "name": info.get("name") or config.site,
            "subtitle": info.get("subtitle") or "",
            "promotionalText": attrs.get("promotionalText") or "",
            "description": attrs.get("description") or "",
            "keywords": attrs.get("keywords") or "",
        }

    ordered = {locale: locales[locale] for locale in sorted(locales)}
    snapshot = {
        "appName": config.site,
        "appStoreId": config.app_store_id,
        "bundleId": config.bundle_id,
        "version": version.get("attributes", {}).get("versionString"),
        "locales": ordered,
    }
    destination = REPO_ROOT / config.site / "asc-metadata.json"
    destination.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{config.site}: wrote {len(ordered)} live ASC locales")
    return snapshot


def md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_screenshot(attrs: dict, max_width: int) -> bytes:
    asset = attrs.get("imageAsset") or {}
    template = asset.get("templateUrl")
    if not template:
        raise RuntimeError(f"ASC screenshot has no imageAsset: {attrs.get('fileName')}")
    width = min(max_width, asset["width"])
    height = round(asset["height"] * width / asset["width"])
    url = (
        template.replace("{w}", str(width))
        .replace("{h}", str(height))
        .replace("{f}", "webp")
    )
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    return response.content


def write_webp(source: Path | bytes, destination: Path, max_width: int) -> None:
    if isinstance(source, bytes):
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source)
        return
    with Image.open(source) as image:
        image.load()
        if image.width > max_width:
            height = round(image.height * max_width / image.width)
            image = image.resize((max_width, height), Image.Resampling.LANCZOS)
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, "WEBP", quality=82, method=6)


def remote_screenshot_manifest(client, config: AppConfig, context) -> dict[str, list[dict]]:
    _, _, version_localizations, _ = context
    manifest: dict[str, list[dict]] = {}
    localizations = {
        item.get("attributes", {}).get("locale"): item for item in version_localizations
    }
    cache: dict[str, list[dict]] = {}

    def screenshots_for(source_locale: str) -> list[dict]:
        if source_locale in cache:
            return cache[source_locale]
        localization = localizations[source_locale]
        sets = client._paged_get(
            f"/appStoreVersionLocalizations/{localization['id']}/appScreenshotSets"
        )
        selected: list[dict] = []
        by_type = {item.get("attributes", {}).get("screenshotDisplayType"): item for item in sets}
        for display_type, limit in config.display_types:
            screenshot_set = by_type.get(display_type)
            if not screenshot_set:
                raise RuntimeError(
                    f"{config.site} {source_locale}: missing ASC set {display_type}"
                )
            screenshots = client._paged_get(
                f"/appScreenshotSets/{screenshot_set['id']}/appScreenshots"
            )
            if limit is not None:
                screenshots = screenshots[:limit]
            for screenshot in screenshots:
                attrs = screenshot.get("attributes", {})
                selected.append(
                    {
                        "displayType": display_type,
                        "fileName": attrs.get("fileName"),
                        "sourceFileChecksum": attrs.get("sourceFileChecksum"),
                        "imageAsset": attrs.get("imageAsset"),
                    }
                )
        cache[source_locale] = selected
        return selected

    for locale in sorted(localizations):
        try:
            manifest[locale] = screenshots_for(locale)
        except RuntimeError:
            if not config.screenshot_fallback_locale:
                raise
            manifest[locale] = screenshots_for(config.screenshot_fallback_locale)
    return manifest


def sync_assets(client, config: AppConfig, context, *, prefer_local: bool) -> None:
    manifest = remote_screenshot_manifest(client, config, context)
    manifest_path = REPO_ROOT / config.site / "asc-assets.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    output_root = REPO_ROOT / config.site / "images" / "asc"
    total = 0
    downloaded = 0
    remote_cache: dict[str, bytes] = {}
    for locale, screenshots in manifest.items():
        locale_root = output_root / locale
        expected_names = {
            f"{index:02d}-{'watch' if 'WATCH' in attrs['displayType'] else 'phone'}.webp"
            for index, attrs in enumerate(screenshots, 1)
        }

        def prepare(item: tuple[int, dict]) -> bool:
            index, attrs = item
            kind = "watch" if "WATCH" in attrs["displayType"] else "phone"
            name = f"{index:02d}-{kind}.webp"
            destination = locale_root / name
            source: Path | bytes
            local = (
                config.local_screenshots / locale / attrs["fileName"]
                if prefer_local and config.local_screenshots and attrs.get("fileName")
                else None
            )
            if local and local.is_file() and md5(local) == attrs.get("sourceFileChecksum"):
                source = local
                was_downloaded = False
            else:
                checksum = attrs.get("sourceFileChecksum") or f"{locale}:{name}"
                if checksum in remote_cache:
                    source = remote_cache[checksum]
                    was_downloaded = False
                else:
                    source = download_screenshot(attrs, 520 if kind == "watch" else 720)
                    remote_cache[checksum] = source
                    was_downloaded = True
            write_webp(source, destination, 520 if kind == "watch" else 720)
            return was_downloaded

        with ThreadPoolExecutor(max_workers=min(6, len(screenshots))) as pool:
            downloaded += sum(pool.map(prepare, enumerate(screenshots, 1)))
        total += len(screenshots)
        if locale_root.exists():
            for stale in locale_root.glob("*.webp"):
                if stale.name not in expected_names:
                    stale.unlink()
        print(f"{config.site}: prepared {locale} ({len(screenshots)} screenshots)", flush=True)
    print(f"{config.site}: prepared {total} web screenshots ({downloaded} downloaded from ASC)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", action="append", choices=sorted(APPS))
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--assets-only", action="store_true")
    parser.add_argument(
        "--remote-assets",
        action="store_true",
        help="Skip local fastlane sources and download web-sized copies from ASC's CDN",
    )
    parser.add_argument("--asc-tools", type=Path, default=DEFAULT_ASC_TOOLS)
    args = parser.parse_args()
    if args.metadata_only and args.assets_only:
        parser.error("--metadata-only and --assets-only are mutually exclusive")

    client = load_client(args.asc_tools)
    selected = args.app or list(APPS)
    for name in selected:
        config = APPS[name]
        context = live_context(client, config)
        if not args.assets_only:
            sync_metadata(client, config, context)
        if not args.metadata_only:
            sync_assets(client, config, context, prefer_local=not args.remote_assets)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
