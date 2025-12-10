# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Command

```bash
python3 build.py
```

This generates 14 localized HTML pages (one per language) and updates `sitemap.xml`. Run after any changes to translation files or the build script.

## Architecture

This is a static multi-language landing page for an iOS app. The build system generates separate HTML files per language for SEO (search engine crawlers don't execute JavaScript).

### Build Flow

```
locales/*.json (14 translation files)
        ↓
    build.py (Python script)
        ↓
index.html + [lang]/index.html (14 HTML files) + sitemap.xml
```

### Key Components

- **`build.py`**: Reads JSON translations, generates HTML using f-string templates, creates sitemap. Key config: `LANGUAGES` array (language codes/directories), `BASE_URL`, `OG_LOCALES` (Open Graph locale mapping).

- **`locales/*.json`**: Translation files with keys: `appName`, `meta.title`, `meta.description`, `nav.*`, `hero.*`, `features.*`, `testimonials.*`, `download.*`, `privacy.*`, `footer.*`.

- **`css/style.css`**: Shared styles for all language versions.

- **`js/main.js`**: Screenshot gallery, language dropdown, smooth scrolling, scroll animations.

### URL Structure

- English: `/` (root `index.html`)
- Other languages: `/[lang-code]/index.html` (e.g., `/ja/`, `/ko/`, `/zh-Hans/`)

Asset paths use `../` prefix in subdirectory pages (handled by `get_asset_path()` in build script).

## Adding a New Language

1. Create `locales/[code].json` (copy from `en.json`)
2. Add entry to `LANGUAGES` array in `build.py`
3. Add entry to `OG_LOCALES` dict in `build.py`
4. Run `python3 build.py`

## Common Issues

- **JSON parse errors**: Check for unescaped quotes or curly quote characters (`""`) in translation files. Use straight quotes or escape them.
- **Images not loading in subdirectories**: Asset paths should be relative; the build script handles this automatically.
