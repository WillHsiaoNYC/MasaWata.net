# Fitness Story Website

A multi-language, SEO-optimized landing page for the Fitness Story iOS app, hosted on GitHub Pages.

**Live URL**: https://masawata.net/FitnessStory/

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Supported Languages](#supported-languages)
- [Build System](#build-system)
- [SEO Implementation](#seo-implementation)
- [How to Update Content](#how-to-update-content)
- [Deployment](#deployment)

---

## Overview

This website serves as the marketing landing page for Fitness Story, an iOS app that transforms Apple Health workout data into beautiful visual journeys. The site is built with:

- **Pure HTML5, CSS3, JavaScript** (no frameworks or build tools required for runtime)
- **Python build script** for generating localized pages
- **14 language versions** with full SEO optimization
- **Static hosting** compatible with GitHub Pages

---

## Features

- **Multi-language Support**: 14 fully translated language versions
- **SEO Optimized**: Each language has its own HTML file with localized meta tags
- **Responsive Design**: Mobile-first design that works on all devices
- **App Store Integration**: Localized App Store badges and smart banner
- **Fast Loading**: No JavaScript frameworks, minimal dependencies
- **Accessibility**: Semantic HTML, ARIA labels, keyboard navigation

---

## Project Structure

```
FitnessStory/
├── index.html                 # English (default) landing page
├── css/
│   └── style.css              # All styles (responsive, animations)
├── js/
│   ├── main.js                # Interactions (gallery, navigation, animations)
│   └── i18n.js                # Legacy client-side language switching
├── locales/                   # Translation files (JSON)
│   ├── en.json                # English
│   ├── zh-Hans.json           # Chinese Simplified
│   ├── zh-Hant.json           # Chinese Traditional
│   ├── ja.json                # Japanese
│   ├── ko.json                # Korean
│   ├── fr.json                # French
│   ├── de.json                # German
│   ├── es.json                # Spanish
│   ├── pt.json                # Portuguese
│   ├── it.json                # Italian
│   ├── ru.json                # Russian
│   ├── hi.json                # Hindi
│   ├── id.json                # Indonesian
│   └── vi.json                # Vietnamese
├── images/
│   ├── Fitness Story.png      # App icon
│   ├── Fitness Story Dark Mode.png
│   ├── iphone/                # iPhone screenshots
│   └── ipad/                  # iPad screenshots
├── assets/
│   └── app-store-badges/      # Localized App Store download badges
├── [language-code]/           # Generated language directories
│   └── index.html             # Localized HTML page
├── build.py                   # Python script to generate all HTML pages
├── build.js                   # Node.js alternative (if Node is available)
├── sitemap.xml                # SEO sitemap with all language URLs
├── robots.txt                 # Search engine crawling rules
└── README.md                  # This file
```

---

## Supported Languages

| Language | Code | Directory | Localized App Name |
|----------|------|-----------|-------------------|
| English | en | / (root) | Fitness Story |
| Chinese (Simplified) | zh-Hans | /zh-Hans/ | 健身故事 |
| Chinese (Traditional) | zh-Hant | /zh-Hant/ | 健身故事 |
| Japanese | ja | /ja/ | フィットネスストーリー |
| Korean | ko | /ko/ | 피트니스 스토리 |
| French | fr | /fr/ | Fitness Story |
| German | de | /de/ | Fitness Story |
| Spanish | es | /es/ | Fitness Story |
| Portuguese | pt | /pt/ | Fitness Story |
| Italian | it | /it/ | Fitness Story |
| Russian | ru | /ru/ | Fitness Story |
| Hindi | hi | /hi/ | फिटनेस स्टोरी |
| Indonesian | id | /id/ | Fitness Story |
| Vietnamese | vi | /vi/ | Fitness Story |

---

## Build System

### Why a Build System?

For optimal SEO, each language needs its own HTML file with:
- Localized `<title>` and `<meta>` tags baked into the HTML
- Language-specific `<html lang="">` attribute
- Proper canonical URLs and hreflang tags

JavaScript-based language switching doesn't work for SEO because search engine crawlers don't always execute JavaScript.

### Running the Build

```bash
# Navigate to the project directory
cd FitnessStory

# Run the Python build script
python3 build.py
```

**Output:**
```
Building localized HTML files for SEO...

  Created: index.html (English)
  Created: zh-Hans/index.html (Chinese Simplified)
  Created: zh-Hant/index.html (Chinese Traditional)
  ...
  Updated: sitemap.xml

Build complete! Generated 14 localized pages.
```

### Build Script Explained (build.py)

The `build.py` script performs the following:

#### 1. Configuration (Lines 1-50)

```python
LANGUAGES = [
    {'code': 'en', 'name': 'English', 'dir': ''},      # Root directory
    {'code': 'zh-Hans', 'name': 'Chinese Simplified', 'dir': 'zh-Hans'},
    # ... more languages
]

BASE_URL = 'https://masawata.net/FitnessStory'

OG_LOCALES = {
    'en': 'en_US',
    'ja': 'ja_JP',
    # Maps language codes to Open Graph locale format
}
```

- `LANGUAGES`: List of all supported languages with their codes and directory names
- `BASE_URL`: The production URL (used for canonical URLs and sitemap)
- `OG_LOCALES`: Maps language codes to Facebook Open Graph locale format

#### 2. Load Translations (Lines 51-55)

```python
def load_translation(lang_code):
    filepath = os.path.join(SCRIPT_DIR, 'locales', f'{lang_code}.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
```

Reads the JSON translation file for a given language code.

#### 3. Generate Hreflang Tags (Lines 57-63)

```python
def generate_hreflang_tags():
    tags = ''
    for lang in LANGUAGES:
        url = f"{BASE_URL}/{lang['dir']}/" if lang['dir'] else f"{BASE_URL}/"
        tags += f'    <link rel="alternate" hreflang="{lang["code"]}" href="{url}">\n'
    tags += f'    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/">'
    return tags
```

Creates `<link rel="alternate" hreflang="...">` tags for all 14 languages. These tell Google which page to show for each language.

#### 4. Asset Path Helper (Lines 65-66)

```python
def get_asset_path(lang_dir):
    return '../' if lang_dir else ''
```

Returns the relative path prefix for assets. Language subdirectories need `../` to reach root assets.

#### 5. Generate HTML (Lines 68-480)

```python
def generate_html(lang, translations):
    asset_path = get_asset_path(lang['dir'])
    canonical_url = f"{BASE_URL}/{lang['dir']}/" if lang['dir'] else f"{BASE_URL}/"
    # ... builds complete HTML page
```

This is the main function that generates a complete HTML page for a language. It:

1. **Sets up variables**: asset paths, canonical URL, locale
2. **Generates language selector links**: Creates navigation links to all language versions
3. **Builds the HTML template**: A large f-string with all page sections:
   - `<head>` with localized meta tags, Open Graph, Twitter Cards, JSON-LD
   - Header with navigation and language selector
   - Hero section with app icon and download button
   - Features section (6 feature cards)
   - Screenshots gallery
   - Testimonials (3 reviews)
   - Download CTA section
   - Privacy section
   - Footer

**Key template variables:**
- `{t['meta']['title]}` - Localized page title
- `{t['appName']}` - Localized app name (e.g., "フィットネスストーリー")
- `{asset_path}` - Relative path prefix (`../` for subdirectories)
- `{canonical_url}` - Full URL for this language version
- `{og_locale}` - Open Graph locale (e.g., "ja_JP")

#### 6. Generate Sitemap (Lines 482-510)

```python
def generate_sitemap():
    today = date.today().isoformat()
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
'''
    for lang in LANGUAGES:
        # Add URL entry with hreflang cross-references
```

Creates an XML sitemap with:
- All 14 language URLs
- `<lastmod>` date (today's date)
- `<changefreq>weekly</changefreq>`
- `<priority>` (1.0 for English, 0.9 for others)
- `<xhtml:link>` hreflang references between all pages

#### 7. Main Build Function (Lines 512-545)

```python
def build():
    print('Building localized HTML files for SEO...\n')

    for lang in LANGUAGES:
        translations = load_translation(lang['code'])
        html = generate_html(lang, translations)

        # Create directory if needed
        if lang['dir']:
            output_dir = os.path.join(SCRIPT_DIR, lang['dir'])
            os.makedirs(output_dir, exist_ok=True)

        # Write HTML file
        filepath = os.path.join(output_dir, 'index.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

    # Generate sitemap
    sitemap = generate_sitemap()
    # ... write sitemap.xml
```

Orchestrates the build process:
1. Loops through all languages
2. Loads translations for each
3. Generates HTML content
4. Creates subdirectory if needed
5. Writes the HTML file
6. Finally generates the sitemap

---

## SEO Implementation

### Per-Language SEO Features

Each generated HTML file includes:

#### 1. Localized Meta Tags
```html
<title>Fitness Story - Apple ヘルスケアのワークアウトを美しいビジュアルジャーニーに</title>
<meta name="description" content="Apple ヘルスケアのワークアウトを...">
```

#### 2. Canonical URL
```html
<link rel="canonical" href="https://masawata.net/FitnessStory/ja/">
```

#### 3. Hreflang Tags (all 14 languages)
```html
<link rel="alternate" hreflang="en" href="https://masawata.net/FitnessStory/">
<link rel="alternate" hreflang="ja" href="https://masawata.net/FitnessStory/ja/">
<link rel="alternate" hreflang="ko" href="https://masawata.net/FitnessStory/ko/">
<!-- ... all 14 languages -->
<link rel="alternate" hreflang="x-default" href="https://masawata.net/FitnessStory/">
```

#### 4. Open Graph Tags (Facebook/Social)
```html
<meta property="og:title" content="Fitness Story - ...">
<meta property="og:description" content="...">
<meta property="og:locale" content="ja_JP">
<meta property="og:site_name" content="フィットネスストーリー">
```

#### 5. Twitter Card Tags
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">
```

#### 6. Structured Data (JSON-LD)
```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "フィットネスストーリー",
    "inLanguage": "ja",
    ...
}
</script>
```

### Sitemap Structure

The `sitemap.xml` follows the multilingual sitemap format with xhtml:link annotations:

```xml
<url>
    <loc>https://masawata.net/FitnessStory/ja/</loc>
    <lastmod>2025-12-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://masawata.net/FitnessStory/"/>
    <xhtml:link rel="alternate" hreflang="ja" href="https://masawata.net/FitnessStory/ja/"/>
    <!-- ... all languages cross-referenced -->
</url>
```

---

## How to Update Content

### Updating Translations

1. Edit the appropriate JSON file in `/locales/`:

```json
{
    "appName": "フィットネスストーリー",
    "meta": {
        "title": "Fitness Story - ...",
        "description": "..."
    },
    "hero": {
        "title": "...",
        "description": "..."
    }
    // ... more sections
}
```

2. Run the build script:
```bash
python3 build.py
```

### Translation File Structure

Each locale JSON file has this structure:

```json
{
    "appName": "Localized app name",
    "meta": {
        "title": "SEO title for browser tab and search results",
        "description": "SEO meta description"
    },
    "nav": {
        "features": "Features",
        "screenshots": "Screenshots",
        "testimonials": "Testimonials",
        "download": "Download"
    },
    "hero": {
        "title": "Main headline",
        "description": "Subheadline text",
        "rating": "5.0 on the App Store"
    },
    "features": {
        "title": "Section title",
        "subtitle": "Section subtitle",
        "storyline": { "title": "...", "description": "..." },
        "dashboard": { "title": "...", "description": "..." },
        "analytics": { "title": "...", "description": "..." },
        "records": { "title": "...", "description": "..." },
        "locations": { "title": "...", "description": "..." },
        "favorites": { "title": "...", "description": "..." }
    },
    "screenshots": {
        "title": "...",
        "subtitle": "..."
    },
    "testimonials": {
        "title": "...",
        "subtitle": "...",
        "review1": { "quote": "..." },
        "review2": { "quote": "..." },
        "review3": { "quote": "..." }
    },
    "download": {
        "title": "...",
        "description": "...",
        "platforms": "Available on iPhone, iPad, Mac, and Apple Vision"
    },
    "privacy": {
        "title": "...",
        "description": "...",
        "link": "Read our Privacy Policy"
    },
    "footer": {
        "appStore": "App Store",
        "privacy": "Privacy Policy",
        "terms": "Terms of Service",
        "copyright": "© 2025 Fitness Story. All rights reserved."
    }
}
```

### Adding a New Language

1. Create a new JSON file in `/locales/` (e.g., `th.json` for Thai)

2. Add the language to `build.py`:
```python
LANGUAGES = [
    # ... existing languages
    {'code': 'th', 'name': 'Thai', 'dir': 'th'},
]

OG_LOCALES = {
    # ... existing locales
    'th': 'th_TH',
}
```

3. Run the build:
```bash
python3 build.py
```

### Updating Styles

Edit `/css/style.css`. Changes apply to all language versions automatically since they share the same stylesheet.

### Updating JavaScript

Edit `/js/main.js`. This handles:
- Screenshot gallery slider
- Mobile navigation toggle
- Language dropdown
- Smooth scrolling
- Scroll animations

---

## Deployment

### GitHub Pages

1. Push all files to your GitHub repository
2. Enable GitHub Pages in repository settings
3. Set the source to the branch containing these files
4. If using a custom domain, add a CNAME file

### Manual Deployment

1. Run the build script to generate all HTML files:
```bash
python3 build.py
```

2. Upload all files to your web server

### Verifying the Build

After building, verify:
- [ ] All 14 `index.html` files exist (root + 13 language directories)
- [ ] `sitemap.xml` is updated with today's date
- [ ] Language switcher links work correctly
- [ ] Meta tags are properly localized (check page source)

---

## File Dependencies

```
build.py
├── reads: locales/*.json (14 files)
├── creates: index.html (English)
├── creates: [lang]/index.html (13 files)
└── creates: sitemap.xml

index.html (each language version)
├── loads: css/style.css
├── loads: js/main.js
├── references: images/*
└── references: assets/app-store-badges/*
```

---

## Technical Notes

### Why Not a JavaScript SPA?

Single-page applications with client-side routing have SEO challenges:
- Search engine crawlers may not execute JavaScript
- Social media crawlers (Facebook, Twitter) don't execute JavaScript
- Meta tags must be in the initial HTML response

By generating separate HTML files per language, we ensure:
- Perfect SEO for all 14 languages
- Correct social media previews when sharing links
- Fast initial page load (no JavaScript required for content)

### Character Encoding

All files use UTF-8 encoding to properly handle:
- Chinese characters (简体/繁體)
- Japanese characters (日本語)
- Korean characters (한국어)
- Hindi characters (हिन्दी)
- Russian Cyrillic (Русский)

### URL Structure

```
https://masawata.net/FitnessStory/           # English (default)
https://masawata.net/FitnessStory/ja/        # Japanese
https://masawata.net/FitnessStory/ko/        # Korean
https://masawata.net/FitnessStory/zh-Hans/   # Chinese Simplified
...
```

This structure:
- Uses clean URLs (no query parameters)
- Is easily crawlable by search engines
- Supports browser language detection via hreflang

---

## Troubleshooting

### Build fails with JSON error

Check the locale JSON file for:
- Missing commas between properties
- Unescaped quotes inside strings (use `\"` or different quote styles)
- Invalid Unicode characters

### Images not loading in subdirectories

Ensure asset paths use the correct relative prefix. The build script handles this automatically via `get_asset_path()`.

### Changes not appearing after build

1. Clear your browser cache
2. Verify the build ran successfully
3. Check file timestamps to ensure files were updated

---

## License

Copyright 2025 Weiren Hsiao. All rights reserved.
