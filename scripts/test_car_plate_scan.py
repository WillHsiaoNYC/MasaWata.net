"""Behavioral checks for website localization and read-only ASC selection."""

import contextlib
from dataclasses import replace
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from scripts.asc_web import PageOptions, build_site
from scripts.sync_asc_web import APPS, AppConfig, live_context, remote_screenshot_manifest, sync_metadata


def localization(locale):
    return {"id": locale, "attributes": {"locale": locale, "description": "English app description"}}


class AscFixture:
    def __init__(self):
        self.versions = [{"id": "draft", "attributes": {"versionString": "1.0", "appStoreState": "PREPARE_FOR_SUBMISSION"}}]
        self.calls = []

    def find_app_id_by_bundle_id(self, bundle_id):
        return "app"

    def get_live_app_info_id(self, app_id):
        return "live-info"

    def list_app_info_localizations(self, app_info_id):
        return [{"id": locale, "attributes": {"locale": locale, "name": locale + " name"}} for locale in ("en-US", "fr-FR")]

    def _paged_get(self, path, params=None):
        self.calls.append(path)
        if path == "/apps/app/appStoreVersions":
            return self.versions
        if path == "/apps/app/appInfos":
            return [{"id": "draft-info"}]
        if path.endswith("/appStoreVersionLocalizations"):
            return [localization("en-US"), localization("fr-FR")]
        if path == "/appStoreVersionLocalizations/en-US/appScreenshotSets":
            return [{"id": "english-set", "attributes": {"screenshotDisplayType": "APP_IPHONE_61"}}]
        if path == "/appScreenshotSets/english-set/appScreenshots":
            return [{"id": "shot", "attributes": {"fileName": "01-poster.png", "sourceFileChecksum": "abc", "imageAsset": {"width": 2, "height": 4}}}]
        raise AssertionError("Unexpected ASC read: " + path)


class AscSelectionTests(unittest.TestCase):
    def setUp(self):
        self.client = AscFixture()
        self.config = replace(APPS["CarPlateScan"], unreleased_version_id="draft", unreleased_app_info_id="draft-info")

    def test_only_opted_in_product_can_read_a_pinned_draft(self):
        context = live_context(self.client, self.config)
        self.assertEqual(context[1]["id"], "draft")
        self.assertEqual(context[3], "draft-info")
        ordinary = AppConfig("ExistingApp", "bundle", "1", None)
        with self.assertRaisesRegex(RuntimeError, "No live iOS version"):
            live_context(self.client, ordinary)

    def test_live_version_takes_precedence_over_draft(self):
        self.client.versions.append({"id": "released", "attributes": {"appVersionState": "READY_FOR_DISTRIBUTION"}})
        context = live_context(self.client, self.config)
        self.assertEqual(context[1]["id"], "released")
        self.assertEqual(context[3], "live-info")

    def test_missing_pinned_record_fails_instead_of_selecting_another_draft(self):
        self.client.versions[0]["id"] = "some-other-draft"
        with self.assertRaisesRegex(RuntimeError, "pre-release version missing"):
            live_context(self.client, self.config)

    def test_non_english_data_never_enters_either_snapshot(self):
        # Pass an unfiltered context to verify filtering at both output boundaries.
        context = ("app", self.client.versions[0], [localization("en-US"), localization("fr-FR")], "draft-info")
        with tempfile.TemporaryDirectory() as directory, patch("scripts.sync_asc_web.REPO_ROOT", Path(directory)):
            with contextlib.redirect_stdout(io.StringIO()):
                metadata = sync_metadata(self.client, self.config, context)
            manifest = remote_screenshot_manifest(self.client, self.config, context)
            self.assertEqual(set(metadata["locales"]), {"en-US"})
            self.assertEqual(set(manifest), {"en-US"})
            self.assertEqual(metadata["source"]["versionState"], "PREPARE_FOR_SUBMISSION")
            self.assertTrue(all("fr-FR/appScreenshotSets" not in call for call in self.client.calls))

    def test_missing_english_data_fails_clearly(self):
        context = ("app", self.client.versions[0], [localization("fr-FR")], "draft-info")
        with self.assertRaisesRegex(RuntimeError, "exactly one ASC localization for en-US"):
            remote_screenshot_manifest(self.client, self.config, context)


class LocalizedLandingPageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.notice = "Core plate reading runs on your device. Optional cloud review requires internet."
        english = {
            "name": "Car Plate Scan: License Reader", "subtitle": "Photo OCR, History & Locations",
            "promotionalText": "Scan & review <carefully>.",
            "description": "Save a personal capture history.",
        }
        metadata = {"appName": "CarPlateScan", "locales": {"en-US": english}}
        (self.site / "asc-metadata.json").write_text(json.dumps(metadata))
        self.localized_metadata = {"locales": {"en-US": english, "fr-CA": {
            "name": "Car Plate Scan", "subtitle": "Numérisez les plaques",
            "promotionalText": "Lisez les plaques à partir de vos photos.",
            "description": "Retrouvez les plaques enregistrées.",
        }}}
        shots = self.site / "images/asc/en-US"
        shots.mkdir(parents=True)
        Image.new("RGB", (2, 4)).save(shots / "01-phone.webp")
        self.options = PageOptions(
            brand_name="Car Plate Scan", store_label="View on the App Store", skip_label="Skip to content",
            privacy_label="Privacy & processing", processing_notice=self.notice, screenshot_locale="en-US",
            screenshot_alts=('Review a plate reading & its "photo"',),
        )

    def render(self, options=None, metadata=None):
        with contextlib.redirect_stdout(io.StringIO()):
            build_site(site_dir=self.site, base_url="https://example.com/CarPlateScan", app_store_id="6825007024",
                       icon_path="images/icon.png", privacy_url="#privacy-processing", support_url="mailto:support@example.com",
                       accent="#a7dfd2", accent_dark="#83c7b7", locale_page_options=options, metadata=metadata)
        return (self.site / "index.html").read_text()

    def test_landing_page_has_listing_actions_platform_and_processing_details(self):
        page = self.render({"en-US": self.options})
        self.assertEqual(page.count('href="https://apps.apple.com/app/id6825007024" rel="noopener">View on the App Store'), 2)
        self.assertNotIn("Planned release", page)
        self.assertNotIn("Download on the App Store", page)
        self.assertIn("apple-itunes-app", page)
        self.assertIn('class="asc-languages"', page)
        self.assertNotIn('"downloadUrl"', page)
        self.assertIn('"sameAs": "https://apps.apple.com/app/id6825007024"', page)
        self.assertNotIn('"offers"', page)
        self.assertIn('"operatingSystem": "iOS"', page)
        self.assertIn('id="privacy-processing"', page)
        self.assertIn('href="#privacy-processing">Privacy &amp; processing</a>', page)
        self.assertEqual(page.count(self.notice), 1)
        self.assertIn('width="2" height="4"', page)
        self.assertIn('alt="Review a plate reading &amp; its &quot;photo&quot;"', page)
        self.assertIn("Scan &amp; review &lt;carefully&gt;.", page)
        self.assertFalse((self.site / "en-US").exists())

    def test_existing_page_defaults_stay_downloadable(self):
        page = self.render()
        self.assertIn("Download on the App Store", page)
        self.assertIn("apple-itunes-app", page)
        self.assertIn('"downloadUrl"', page)
        self.assertIn('class="asc-languages"', page)
        self.assertNotIn("Planned release", page)

    def test_localized_page_shares_english_images_and_provides_localized_alt(self):
        french = replace(
            self.options, store_label="Voir sur l’App Store", skip_label="Aller au contenu",
            privacy_label="Confidentialité et traitement", processing_notice="La lecture se fait sur ton appareil.",
            screenshot_alts=("Vérifier la plaque sur la photo",),
            screenshot_note="Les captures d’écran montrent l’app en anglais.",
        )
        self.render({"en-US": self.options, "fr-CA": french}, self.localized_metadata)
        page = (self.site / "fr-CA" / "index.html").read_text()
        self.assertIn('<html lang="fr-CA" dir="ltr">', page)
        self.assertIn('class="asc-brand" href="./"', page)
        self.assertIn('href="../" lang="en-US"', page)
        self.assertIn('href="../fr-CA/" lang="fr-CA" dir="auto" aria-current="page"', page)
        self.assertIn('src="../images/asc/en-US/01-phone.webp" alt="Vérifier la plaque sur la photo"', page)
        self.assertIn(french.screenshot_note, page)
        self.assertIn(french.processing_notice, page)
        self.assertIn(french.store_label, page)
        self.assertIn(french.skip_label, page)
        self.assertNotIn(self.notice, page)

    def test_each_screenshot_requires_localized_alt(self):
        with self.assertRaisesRegex(RuntimeError, "descriptive alt text"):
            self.render({"en-US": replace(self.options, screenshot_alts=())})


if __name__ == "__main__":
    unittest.main()
