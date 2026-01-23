# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Command

```bash
python3 build.py
```

Generates 14 localized HTML pages (one per language) and updates `sitemap.xml`. Run after any changes to translation files or the build script.

## Architecture

Same as FitnessStory - static multi-language landing page with Python build system.

### Build Flow

```
locales/*.json (14 translation files)
        ↓
    build.py (Python script)
        ↓
index.html + [lang]/index.html (14 HTML files) + sitemap.xml
```

## Key Files

- `build.py` - Generates HTML from locale JSON files
- `locales/*.json` - Translation files (14 languages)
- `css/style.css` - Shared styles
- `js/main.js` - Gallery, dropdowns, animations

## URL Structure

- English: `/WhereWasI/` (root `index.html`)
- Other languages: `/WhereWasI/[lang-code]/index.html` (e.g., `/WhereWasI/ja/`, `/WhereWasI/ko/`)

## Adding Images

1. Save app icon to `images/WhereWasI.png` (512x512 PNG)
2. Save screenshots to `images/en/` with names:
   - `title.jpg` (hero image)
   - `timeline.jpg`, `statistics.jpg`, `map.jpg`, `privacy.jpg` (feature cards)
   - `action-*.jpg` (gallery screenshots)
3. Optimize images: 660px width, JPEG quality 85
4. Run `python3 build.py` to regenerate

## Adding a New Language

1. Create `locales/[code].json` (copy from `en.json`)
2. Add entry to `LANGUAGES` array in `build.py`
3. Add entry to `OG_LOCALES` dict in `build.py`
4. Run `python3 build.py`

## Differences from FitnessStory

- No promo banner
- No testimonials section
- 4 features (timeline, statistics, map, privacy) instead of 11
- App Store ID: 6758056060
