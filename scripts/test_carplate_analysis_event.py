import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "CarPlateScan/event/analysis-collections"

class Tags(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class AnalysisEventTests(unittest.TestCase):
    def test_approved46_locale_copy_is_unchanged_and_web_chrome_is_complete(self):
        data = json.loads((PAGE / "localizations.json").read_text())
        locales = data["locales"]
        self.assertEqual(len(locales), 46)
        self.assertTrue({"ja", "ko", "th", "zh-Hans"}.isdisjoint(locales))
        approved = {c:{k:v[k] for k in ["name", "short_description", "long_description"]} for c,v in locales.items()}
        digest = hashlib.sha256(json.dumps(approved,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        self.assertEqual(digest, "1527fd835a79a350d464c2ffa93d40bf7033ad70fbbb0a45a8913c6c862f5e60")
        for locale, fields in locales.items():
            for key in ["language", "appStore", "requires", "interface", "label"]:
                self.assertTrue(fields[key].strip(), (locale, key))
            self.assertIn("1.2", fields["requires"])
    def test_fallback_metadata_and_assets_are_exact_and_static_english_is_readable(self):
        html = (PAGE / "index.html").read_text()
        tags = Tags(html).tags
        meta = {v.get("name"):v.get("content") for t,v in tags if t == "meta"}
        self.assertEqual(meta["apple-itunes-app"], "app-id=6825007024, app-argument=https://masawata.net/CarPlateScan/event/analysis-collections/")
        self.assertEqual(meta["robots"], "noindex, nofollow")
        self.assertIn("Plate Collections Debut", html)
        self.assertIn("Browse saved plates by starting or ending letters and digits", html)
        self.assertIn("Requires v1.2. Update when", html)
        self.assertIn("App interface: English and Traditional Chinese.", html)
        for tag, attrs in tags:
            for key in ["src", "href", "srcset"]:
                value = attrs.get(key, "")
                if value and not value.startswith(("/", "http", "#")):
                    self.assertTrue((PAGE / value).is_file(), value)
        self.assertEqual(next(v["href"] for t,v in tags if t=="link" and v.get("rel")=="canonical"), "https://masawata.net/CarPlateScan/event/analysis-collections/")
