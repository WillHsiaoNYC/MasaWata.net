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
    "06-SetValue":    "Set an exact value, or add, subtract, and transfer in bulk",
    "07-Settings":    "Personalize each counter with a name, color, icon, and step size",
    "08-Random":      "Random mode rolls a new value on every tap",
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
        (i for i, l in enumerate(lines)
         if l.lstrip().startswith(("Privacy Policy", "Terms")) or "http" in l),
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
    for _, asc, _hlang, _, d, _, _ in LOCALES:
        url = f"{SITE_BASE}/{d}/" if d else f"{SITE_BASE}/"
        out.append(f'  <link rel="alternate" hreflang="{asc}" href="{url}">')
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


SCREENSHOTS = {
    "01-PosterLeft": "01-phone.webp",
    "02-PosterRight": "02-phone.webp",
    "03-WatchSync": "03-phone.webp",
    "04-Counters": "04-phone.webp",
    "05-Charts": "05-phone.webp",
    "06-SetValue": "06-phone.webp",
    "07-Settings": "07-phone.webp",
    "08-Random": "08-phone.webp",
}

_TAG_SPLIT = re.compile(r"[,،、;؛/]| [-–—] ")

# Give every feature section a DISTINCT screenshot. Watch and Charts move around
# by locale, so match those two by meaning (keyword); fill the rest in order from
# the remaining distinct shots, never repeating within a page.
_WATCH_RE = re.compile(r"watch|⌚|watchos", re.I)
_CHART_RE = re.compile(
    r"chart|graph|total|percent|histor|stat|"
    r"グラフ|チャート|图表|圖表|차트|그래프|график|диаграм|"
    r"gr[áa]fic|graphiq|diagramm|grafico|grafiek|wykres",
    re.I,
)
_ALL_SHOTS = ["04-Counters", "06-SetValue", "08-Random", "03-WatchSync", "05-Charts", "07-Settings"]
_FILL_SHOTS = ["04-Counters", "06-SetValue", "08-Random", "07-Settings"]


def _preferred_shot(sec):
    # Watch terms (usually kept in English) are safe anywhere; chart terms match the
    # TITLE only, so a bullet like "...recorded in the history" doesn't steal a shot.
    if _WATCH_RE.search(sec["title"] + " " + " ".join(sec["bullets"])):
        return "03-WatchSync"
    if _CHART_RE.search(sec["title"]):
        return "05-Charts"
    return None


def assign_shots(sections):
    """One distinct screenshot per section: Watch/Charts matched by meaning, the
    rest filled from the remaining shots in order. Repeats only if a locale has
    more sections than the six available shots."""
    used, shots = set(), []
    for sec in sections:
        p = _preferred_shot(sec)
        if p and p not in used:
            shot = p
        else:
            shot = (next((s for s in _FILL_SHOTS if s not in used), None)
                    or next((s for s in _ALL_SHOTS if s not in used), None)
                    or _ALL_SHOTS[len(shots) % len(_ALL_SHOTS)])
        used.add(shot)
        shots.append(shot)
    return shots


def first_tag(bullet: str) -> str:
    """First clause of a comma-separated 'use' bullet -> a short tag."""
    return _TAG_SPLIT.split(bullet, 1)[0].strip()


def nice_title(s: str) -> str:
    """All-caps Latin titles -> Title Case; leaves other scripts / mixed case untouched."""
    if s and s == s.upper() and any("a" <= c.lower() <= "z" for c in s):
        return s.title()
    return s


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
    p_shots = (f"../images/asc/{asc}" if dir_name
               else f"images/asc/{asc}")

    title_meta = h(f"{name} — {subtitle}") if subtitle else h(name)
    desc_meta = h(promo)
    hero_title = hero_title_with_123(name)

    # ── Device showcase (clean, headline-cropped shots) ──
    SHOWCASE = ["03-WatchSync", "04-Counters", "05-Charts"]
    showcase_block = "\n".join(
        f'      <div class="showcase__shot"><img src="{p_shots}/{SCREENSHOTS[s]}" alt="{h(SCREENSHOT_ALTS[s])}" loading="{load}"></div>'
        for s, load in zip(SHOWCASE, ("lazy", "eager", "lazy"))
    )

    # ── Feature sections: eyebrow (title) + distilled headline/line + screenshot ──
    secs = parsed["sections"]
    feature_secs = secs[:-1] if len(secs) > 1 else secs
    uses_sec = secs[-1] if len(secs) > 1 else None

    shots = assign_shots(feature_secs)
    feats = []
    for i, sec in enumerate(feature_secs):
        bl = sec["bullets"]
        headline = h(bl[0]) if bl else h(sec["title"])
        body = f'\n          <p class="feature__body">{h(bl[1])}</p>' if len(bl) > 1 else ""
        shot = shots[i]
        cls = "feature is-reversed" if i % 2 else "feature"
        feats.append(f'''    <section class="{cls}">
      <div class="wrap feature__grid">
        <div class="feature__text reveal">
          <p class="feature__eyebrow">{h(sec["title"])}</p>
          <h2 class="feature__title">{headline}</h2>{body}
        </div>
        <div class="feature__media reveal"><div class="feature__phone"><img src="{p_shots}/{SCREENSHOTS[shot]}" alt="{h(sec["title"])}" loading="lazy"></div></div>
      </div>
    </section>''')
    features_block = "\n".join(feats)

    # ── Popular uses -> tag grid ──
    uses_block = ""
    if uses_sec and uses_sec["bullets"]:
        tags = "".join(f'<span class="tag">{h(first_tag(b))}</span>' for b in uses_sec["bullets"])
        uses_block = f'''
    <section class="uses reveal">
      <h2 class="uses__h">{h(nice_title(uses_sec["title"]))}</h2>
      <div class="uses__tags">{tags}</div>
    </section>'''

    # JSON-LD screenshot array — feeds Google's rich-result software card.
    screenshot_urls = [f"{SITE_BASE}/images/asc/{asc}/{filename}" for filename in SCREENSHOTS.values()]
    screenshot_json = ",\n      ".join(f'"{u}"' for u in screenshot_urls)

    keywords_meta = ""
    if keywords:
        keywords_meta = f'  <meta name="keywords" content="{h(keywords)}">\n'

    lang_switcher_html = render_lang_switcher(asc, dir_name)

    closing = h(parsed["closing"]) if parsed["closing"] else ""
    closing_block = ""
    if closing:
        closing_block = f'''
    <section class="end reveal">
      <h2 class="end__h">{closing}</h2>
      <div class="end__cta">
        <a class="cta" href="https://apps.apple.com/app/id{APP_STORE_ID}" rel="noopener">{APP_STORE_SVG} Download on the App Store</a>
      </div>
    </section>'''

    return f'''<!DOCTYPE html>
<html lang="{hlang}" dir="{'rtl' if rtl else 'ltr'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#ffffff">

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

  <link rel="stylesheet" href="{p_css}/style.css?v=7">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{h(name)}",
    "applicationCategory": "LifestyleApplication",
    "operatingSystem": "iOS, iPadOS, watchOS",
    "sameAs": "https://apps.apple.com/app/id6769252146",
    "downloadUrl": "https://apps.apple.com/app/id6769252146",
    "publisher": {{ "@type": "Organization", "name": "MasaWata Tech", "url": "https://masawata.net/" }},
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
  <div class="bar">
    <div class="bar__brand"><img src="{p_img}/icon-512.png" alt=""> {h(name)}</div>
    <div class="bar__right">
      {lang_switcher_html}
      <a class="bar__dl" href="https://apps.apple.com/app/id{APP_STORE_ID}" rel="noopener">Download</a>
    </div>
  </div>

  <main>
    <section class="hero">
      <img class="hero__icon" src="{p_img}/icon-512.png" alt="{h(name)} app icon" width="96" height="96">
      <h1 class="hero__title">{hero_title}</h1>
      <p class="hero__subtitle">{h(subtitle)}</p>
      <div class="hero__cta">
        <a class="cta" href="https://apps.apple.com/app/id{APP_STORE_ID}" rel="noopener">{APP_STORE_SVG} Download on the App Store</a>
      </div>
      <p class="hero__blurb">{desc_meta}</p>
    </section>

    <section class="showcase" aria-label="Screenshots">
{showcase_block}
    </section>

{features_block}
{uses_block}
{closing_block}
  </main>

  <footer>
    <div class="foot">
      <small>© 2026 Masawata</small>
      <nav>
        <a href="https://masawata.net/privacy-policy.html">Privacy</a>
        <a href="https://masawata.net/">Support</a>
      </nav>
    </div>
  </footer>

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
