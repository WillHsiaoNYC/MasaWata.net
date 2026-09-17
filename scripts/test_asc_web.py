"""Regression checks for canonical consolidation and sitemap eligibility."""

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from scripts.asc_web import build_site


class SitemapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.locales = ("en-US", "es-ES", "es-MX")
        (self.site / "asc-metadata.json").write_text(json.dumps({
            "appName": "Example", "locales": {
                locale: {"name": "Example", "description": "App description"}
                for locale in self.locales
            },
        }))
        event = self.site / "event" / "index.html"
        event.parent.mkdir()
        event.write_text('<meta name="robots" content="noindex">')

    def build(self, canonical_locales=None):
        with contextlib.redirect_stdout(io.StringIO()):
            build_site(
                site_dir=self.site, base_url="https://example.com/app",
                app_store_id="123", icon_path="icon.png", privacy_url="/privacy",
                support_url="/support", accent="#000", accent_dark="#000",
                aliases={"es": "es-MX"}, canonical_locales=canonical_locales,
            )

    def test_canonical_mapping_preserves_regional_pages_and_alternates(self):
        self.build({"es-ES": "es-MX"})
        page = (self.site / "es-ES/index.html").read_text()
        self.assertIn('<html lang="es-ES"', page)
        self.assertIn('<link rel="canonical" href="https://example.com/app/es-MX/">', page)
        self.assertIn('hreflang="es-ES" href="https://example.com/app/es-ES/"', page)
        root = ET.parse(self.site / "sitemap.xml")
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
        entries = root.findall("sm:url", ns)
        self.assertEqual([node.findtext("sm:loc", namespaces=ns) for node in entries],
                         ["https://example.com/app/", "https://example.com/app/es-MX/"])
        for entry in entries:
            self.assertEqual({node.get("hreflang") for node in entry.findall("x:link", ns)},
                             set(self.locales) | {"x-default"})
        self.assertEqual(root.findall(".//sm:lastmod", ns), [])
        self.assertIn('content="noindex"', (self.site / "es/index.html").read_text())
        # Neither the redirect nor the existing noindex event is submitted.
        self.assertNotIn("/event/", (self.site / "sitemap.xml").read_text())
        self.assertNotIn("/es/", (self.site / "sitemap.xml").read_text())

    def test_unmapped_locales_remain_self_canonical(self):
        self.build()
        for locale in ("es-ES", "es-MX"):
            self.assertIn(f'<link rel="canonical" href="https://example.com/app/{locale}/">',
                          (self.site / locale / "index.html").read_text())

    def test_invalid_mapping_fails_before_writing_pages(self):
        for mapping in ({"missing": "es-MX"}, {"es-ES": "missing"},
                        {"es-ES": "es-MX", "es-MX": "es-ES"}):
            with self.subTest(mapping=mapping), self.assertRaises(RuntimeError):
                self.build(mapping)
            self.assertFalse((self.site / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
