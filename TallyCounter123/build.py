#!/usr/bin/env python3
"""Build the localized Tally Counter 123 site from ASC metadata.

Reads:  ~/Desktop/Air Repo/iOS_submission_tools/apps/Tally Counter 123/{Language}.md
Writes: TallyCounter123/index.html              (en-US, root)
        TallyCounter123/<asc-locale>/index.html (34 other locales)
        TallyCounter123/sitemap.xml

Run:    python3 build.py
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASC_SOURCE = Path(
    "/Users/willhsiao/Desktop/Air Repo/iOS_submission_tools/apps/Tally Counter 123"
)

APP_STORE_ID = "6769252146"
SITE_BASE = "https://masawata.net/TallyCounter123"

# (lang_file_stem, asc_locale, html_lang, og_locale, dir_name, rtl, native_name)
LOCALES = [
    ("English",                "en-US",   "en",      "en_US", "",        False, "English"),
    ("Japanese",               "ja",      "ja",      "ja_JP", "ja",      False, "日本語"),
    ("Korean",                 "ko",      "ko",      "ko_KR", "ko",      False, "한국어"),
    ("Chinese (Simplified)",   "zh-Hans", "zh-Hans", "zh_CN", "zh-Hans", False, "简体中文"),
    ("Chinese (Traditional)",  "zh-Hant", "zh-Hant", "zh_TW", "zh-Hant", False, "繁體中文"),
    ("Czech",                  "cs",      "cs",      "cs_CZ", "cs",      False, "Čeština"),
    ("Danish",                 "da",      "da",      "da_DK", "da",      False, "Dansk"),
    ("German",                 "de-DE",   "de",      "de_DE", "de-DE",   False, "Deutsch"),
    ("Spanish (Spain)",        "es-ES",   "es",      "es_ES", "es-ES",   False, "Español"),
    ("Spanish (Mexico)",       "es-MX",   "es-MX",   "es_MX", "es-MX",   False, "Español (México)"),
    ("Finnish",                "fi",      "fi",      "fi_FI", "fi",      False, "Suomi"),
    ("French",                 "fr-FR",   "fr",      "fr_FR", "fr-FR",   False, "Français"),
    ("Hindi",                  "hi",      "hi",      "hi_IN", "hi",      False, "हिन्दी"),
    ("Hungarian",              "hu",      "hu",      "hu_HU", "hu",      False, "Magyar"),
    ("Indonesian",             "id",      "id",      "id_ID", "id",      False, "Bahasa Indonesia"),
    ("Italian",                "it",      "it",      "it_IT", "it",      False, "Italiano"),
    ("Norwegian",              "no",      "no",      "nb_NO", "no",      False, "Norsk"),
    ("Portuguese (Brazil)",    "pt-BR",   "pt-BR",   "pt_BR", "pt-BR",   False, "Português (Brasil)"),
    ("Russian",                "ru",      "ru",      "ru_RU", "ru",      False, "Русский"),
    ("Slovak",                 "sk",      "sk",      "sk_SK", "sk",      False, "Slovenčina"),
    ("Swedish",                "sv",      "sv",      "sv_SE", "sv",      False, "Svenska"),
    ("Vietnamese",             "vi",      "vi",      "vi_VN", "vi",      False, "Tiếng Việt"),
    ("Arabic",                 "ar-SA",   "ar",      "ar_SA", "ar-SA",   True,  "العربية"),
    ("Turkish",                "tr",      "tr",      "tr_TR", "tr",      False, "Türkçe"),
    ("Polish",                 "pl",      "pl",      "pl_PL", "pl",      False, "Polski"),
    ("Dutch",                  "nl-NL",   "nl",      "nl_NL", "nl-NL",   False, "Nederlands"),
    ("Thai",                   "th",      "th",      "th_TH", "th",      False, "ไทย"),
    ("Portuguese (Portugal)",  "pt-PT",   "pt-PT",   "pt_PT", "pt-PT",   False, "Português (Portugal)"),
    ("Ukrainian",              "uk",      "uk",      "uk_UA", "uk",      False, "Українська"),
    ("Romanian",               "ro",      "ro",      "ro_RO", "ro",      False, "Română"),
    ("Greek",                  "el",      "el",      "el_GR", "el",      False, "Ελληνικά"),
    ("Croatian",               "hr",      "hr",      "hr_HR", "hr",      False, "Hrvatski"),
    ("Slovenian",              "sl-SI",   "sl",      "sl_SI", "sl-SI",   False, "Slovenščina"),
    ("Catalan",                "ca",      "ca",      "ca_ES", "ca",      False, "Català"),
    ("Hebrew",                 "he",      "he",      "he_IL", "he",      True,  "עברית"),
]

# Alt text per screenshot (descriptive, English — search engines use these for image rank).
SCREENSHOT_ALTS = {
    "01-PosterLeft":  "Tally Counter 123 marketing poster — count anything with custom counters",
    "02-PosterRight": "Tally Counter 123 marketing poster — fast input, charts, and history",
    "03-WatchSync":   "Live Apple Watch sync — counters mirror between iPhone and watch",
    "04-Counters":    "List of multiple personalized counters with names, colors, and smart transfers",
    "05-Charts":      "Sessions, history, and visual insights — interactive bar chart with totals",
}

H2_RE = re.compile(r"^## (.+?)$", re.MULTILINE)
BULLET_RE = re.compile(r"^[•·\-]\s+", re.MULTILINE)


def parse_md_sections(text: str) -> dict[str, str]:
    """Split `## Header` blocks into {header: body}."""
    parts = H2_RE.split(text)
    out = {}
    for i in range(1, len(parts), 2):
        out[parts[i].strip()] = parts[i + 1].strip() if i + 1 < len(parts) else ""
    return out


def parse_description(desc: str) -> dict:
    """Parse App Description into intro, feature sections, and closing paragraph."""
    lines = desc.splitlines()
    cutoff = next(
        (i for i, l in enumerate(lines) if l.lstrip().startswith(("Privacy Policy", "Terms"))),
        len(lines),
    )
    body = "\n".join(lines[:cutoff]).strip()

    blocks = re.split(r"\n\s*\n+", body)
    intro = ""
    closing = ""
    sections: list[dict] = []

    for block in blocks:
        block_lines = [l for l in block.strip().split("\n") if l.strip()]
        if not block_lines:
            continue
        bullet_lines = [l for l in block_lines if l.lstrip().startswith(("•", "·", "-"))]
        first_is_title = not block_lines[0].lstrip().startswith(("•", "·", "-"))
        if len(bullet_lines) >= 2 and first_is_title:
            title = block_lines[0].strip().rstrip(":")
            bullets = [BULLET_RE.sub("", l).strip() for l in bullet_lines]
            sections.append({"title": title, "bullets": bullets})
        else:
            paragraph = " ".join(block_lines).strip()
            if not intro:
                intro = paragraph
            else:
                closing = paragraph

    return {"intro": intro, "sections": sections, "closing": closing}


def h(s: str) -> str:
    return html.escape(s or "", quote=True)


def hreflang_block() -> str:
    out = []
    for _, _, hlang, _, d, _, _ in LOCALES:
        url = f"{SITE_BASE}/{d}/" if d else f"{SITE_BASE}/"
        out.append(f'  <link rel="alternate" hreflang="{hlang}" href="{url}">')
    out.append(f'  <link rel="alternate" hreflang="x-default" href="{SITE_BASE}/">')
    return "\n".join(out)


_HREFLANG_CACHE = hreflang_block()

APP_STORE_SVG = (
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    '<path d="M17.05 12.04c-.03-2.96 2.42-4.38 2.53-4.45-1.38-2.02-3.53-2.3-4.3-2.33'
    "-1.83-.18-3.57 1.08-4.5 1.08-.94 0-2.37-1.05-3.9-1.02-2 .03-3.86 1.17-4.9 2.96"
    "-2.1 3.63-.53 9 1.5 11.93 1 1.44 2.17 3.04 3.7 2.98 1.5-.06 2.06-.95 3.86-.95"
    " 1.8 0 2.32.95 3.9.92 1.62-.03 2.63-1.45 3.6-2.9 1.14-1.66 1.6-3.27 1.63-3.35"
    "-.04-.02-3.1-1.19-3.12-4.72zM14.3 3.1c.82-.99 1.37-2.37 1.22-3.74-1.18.05-2.62"
    '.8-3.46 1.78-.75.87-1.41 2.28-1.24 3.62 1.32.1 2.66-.67 3.48-1.66z"/></svg>'
)


def hero_title_with_123(name: str) -> str:
    """If the localized name contains '123', highlight it with .hero__counter."""
    if "123" not in name:
        return h(name)
    before, _, after = name.partition("123")
    before_html = h(before).rstrip()
    after_html = h(after).lstrip()
    parts = [before_html] if before_html else []
    parts.append('<span class="hero__counter" id="counter" data-target="123">123</span>')
    if after_html:
        parts.append(after_html)
    return " ".join(parts).strip()


SCREENSHOTS = ["01-PosterLeft", "02-PosterRight", "03-WatchSync", "04-Counters", "05-Charts"]


def render_lang_switcher(current_asc: str, dir_name: str) -> str:
    """Footer <select> that navigates to the chosen locale on change."""
    rel_root = "../" if dir_name else "./"
    options = []
    for _, asc, _hlang, _og, d, _rtl, native in LOCALES:
        sel = " selected" if asc == current_asc else ""
        target = f"{rel_root}{d}/" if d else rel_root
        options.append(f'        <option value="{h(target)}"{sel}>{h(native)}</option>')
    opts = "\n".join(options)
    return f'''<label class="lang-switch" aria-label="Choose language">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>
        <select onchange="if(this.value)location.href=this.value">
{opts}
        </select>
      </label>'''


def render_page(*, asc, hlang, og, rtl, name, subtitle, promo, keywords, parsed, dir_name):
    canonical = f"{SITE_BASE}/{dir_name}/" if dir_name else f"{SITE_BASE}/"
    p_img = "../images" if dir_name else "images"
    p_css = "../css" if dir_name else "css"
    p_js = "../js" if dir_name else "js"
    p_shots = (f"../images/screenshots/{asc}" if dir_name
               else f"images/screenshots/{asc}")

    title_meta = h(f"{name} — {subtitle}") if subtitle else h(name)
    desc_meta = h(promo)
    hero_title = hero_title_with_123(name)

    features_html = []
    for i, sec in enumerate(parsed["sections"], start=1):
        bullets = "\n".join(f"            <li>{h(b)}</li>" for b in sec["bullets"])
        features_html.append(f'''      <article class="feature">
        <div class="feature__num" aria-hidden="true">{i:02d}</div>
        <div class="feature__content">
          <h2>{h(sec["title"])}</h2>
          <ul>
{bullets}
          </ul>
        </div>
      </article>''')
    features_block = "\n".join(features_html)

    showcase_block = "\n".join(
        f'        <div class="showcase__shot"><img src="{p_shots}/{s}.png" alt="{h(SCREENSHOT_ALTS[s])}" loading="lazy" width="880" height="1912"></div>'
        for s in SCREENSHOTS
    )

    # JSON-LD screenshot array — feeds Google's rich-result software card.
    screenshot_urls = [f"{SITE_BASE}/images/screenshots/{asc}/{s}.png" for s in SCREENSHOTS]
    screenshot_json = ",\n      ".join(f'"{u}"' for u in screenshot_urls)

    keywords_meta = ""
    if keywords:
        keywords_meta = f'  <meta name="keywords" content="{h(keywords)}">\n'

    lang_switcher_html = render_lang_switcher(asc, dir_name)

    closing_html = h(parsed["closing"]) if parsed["closing"] else ""
    pitch_block = ""
    if closing_html:
        pitch_block = f'''
    <section class="pitch">
      <p>{closing_html}</p>
      <a class="hero__cta" href="https://apps.apple.com/app/id{APP_STORE_ID}" rel="noopener">
        {APP_STORE_SVG}
        Download on the App Store
      </a>
    </section>'''

    return f'''<!DOCTYPE html>
<html lang="{hlang}" dir="{'rtl' if rtl else 'ltr'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#FFF1E1">

  <title>{title_meta}</title>
  <meta name="description" content="{desc_meta}">
{keywords_meta}  <meta name="author" content="Masawata">
  <meta name="robots" content="index, follow">

  <meta name="apple-itunes-app" content="app-id={APP_STORE_ID}">

  <link rel="canonical" href="{canonical}">
{_HREFLANG_CACHE}

  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{title_meta}">
  <meta property="og:description" content="{desc_meta}">
  <meta property="og:image" content="{SITE_BASE}/images/icon-1024.png">
  <meta property="og:site_name" content="{h(name)}">
  <meta property="og:locale" content="{og}">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title_meta}">
  <meta name="twitter:description" content="{desc_meta}">
  <meta name="twitter:image" content="{SITE_BASE}/images/icon-1024.png">

  <link rel="icon" type="image/png" sizes="512x512" href="{p_img}/icon-512.png">
  <link rel="apple-touch-icon" href="{p_img}/icon-180.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Geist:wght@400;500;600&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="{p_css}/style.css?v=6">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{h(name)}",
    "applicationCategory": "LifestyleApplication",
    "operatingSystem": "iOS, iPadOS, watchOS",
    "description": "{desc_meta}",
    "url": "{canonical}",
    "image": "{SITE_BASE}/images/icon-1024.png",
    "screenshot": [
      {screenshot_json}
    ],
    "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
    "author": {{ "@type": "Organization", "name": "Masawata", "url": "https://masawata.net/" }}
  }}
  </script>

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZL852HY2Z4"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    if (location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {{
      gtag('config', 'G-ZL852HY2Z4');
    }}
  </script>
</head>

<body>
  <main>
    <div class="bg-mark" aria-hidden="true">123</div>

    <header class="page-header">
      {lang_switcher_html}
    </header>

    <section class="hero">
      <img class="hero__icon" src="{p_img}/icon-512.png" alt="{h(name)} app icon" width="104" height="104">
      <h1 class="hero__title">{hero_title}</h1>
      <p class="hero__subtitle">{h(subtitle)}</p>
      <a class="hero__cta" href="https://apps.apple.com/app/id{APP_STORE_ID}" rel="noopener">
        {APP_STORE_SVG}
        Download on the App Store
      </a>
      <p class="hero__blurb">{desc_meta}</p>
    </section>

    <section class="showcase" aria-label="Screenshots">
{showcase_block}
    </section>

    <section class="features" aria-label="Features">
{features_block}
    </section>
{pitch_block}

    <footer>
      <small>© 2026 Masawata</small>
      <nav>
        <a href="https://masawata.net/privacy-policy.html">Privacy</a>
        <a href="https://masawata.net/">Support</a>
      </nav>
    </footer>
  </main>

  <script src="{p_js}/counter.js" defer></script>
</body>
</html>
'''


def write_sitemap():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for _, _, _, _, d, _, _ in LOCALES:
        url = f"{SITE_BASE}/{d}/" if d else f"{SITE_BASE}/"
        lines.append(f'  <url><loc>{url}</loc></url>')
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    written, missing = [], []
    for lang, asc, hlang, og, dir_name, rtl, _native in LOCALES:
        md_path = ASC_SOURCE / f"{lang}.md"
        if not md_path.exists():
            missing.append(lang)
            continue
        sections = parse_md_sections(md_path.read_text(encoding="utf-8"))
        name = (sections.get("Localized App Name") or "Tally Counter 123").strip()
        subtitle = (sections.get("Subtitle") or "").strip()
        promo = (sections.get("Promotional Text") or "").strip()
        keywords = (sections.get("Key Words") or "").strip()
        desc = (sections.get("App Description") or "").strip()
        parsed = parse_description(desc)

        page = render_page(
            asc=asc, hlang=hlang, og=og, rtl=rtl,
            name=name, subtitle=subtitle, promo=promo, keywords=keywords,
            parsed=parsed, dir_name=dir_name,
        )

        if dir_name:
            (ROOT / dir_name).mkdir(parents=True, exist_ok=True)
            target = ROOT / dir_name / "index.html"
        else:
            target = ROOT / "index.html"
        target.write_text(page, encoding="utf-8")
        written.append(f"  {asc:8s}  {len(parsed['sections'])} sections  →  {target.relative_to(ROOT)}")

    write_sitemap()

    print("\n".join(written))
    if missing:
        print(f"\nMissing .md files: {', '.join(missing)}")
    print(f"\nWrote {len(written)} pages + sitemap.xml")


if __name__ == "__main__":
    sys.exit(main())
