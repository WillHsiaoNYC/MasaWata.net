# Quick Reference Guide

## Common Tasks

### Rebuild All Pages
```bash
cd FitnessStory
python3 build.py
```

### Update a Translation

1. Edit `locales/[lang-code].json`
2. Run `python3 build.py`
3. Verify changes in `[lang-code]/index.html`

### Add a New Language

1. Create `locales/[new-code].json` (copy from `en.json`)
2. Edit `build.py`:
   ```python
   LANGUAGES = [
       # Add new entry:
       {'code': 'new-code', 'name': 'Language Name', 'dir': 'new-code'},
   ]

   OG_LOCALES = {
       # Add new entry:
       'new-code': 'new_COUNTRY',
   }
   ```
3. Run `python3 build.py`

---

## File Locations

| What | Where |
|------|-------|
| English content | `locales/en.json` |
| Japanese content | `locales/ja.json` |
| Styles | `css/style.css` |
| JavaScript | `js/main.js` |
| Build script | `build.py` |
| Screenshots | `images/iphone/` |
| App Store badges | `assets/app-store-badges/` |

---

## Translation Keys Reference

```
appName              → Header logo, footer, OG site name, JSON-LD
meta.title           → <title>, og:title, twitter:title
meta.description     → meta description, og:description, twitter:description
nav.features         → Navigation link
nav.screenshots      → Navigation link
nav.testimonials     → Navigation link
nav.download         → Navigation link
hero.title           → Main headline
hero.description     → Subheadline
hero.rating          → "5.0 on the App Store"
features.title       → Section heading
features.subtitle    → Section subheading
features.storyline.title/description
features.dashboard.title/description
features.analytics.title/description
features.records.title/description
features.locations.title/description
features.favorites.title/description
screenshots.title    → Section heading
screenshots.subtitle → Section subheading
testimonials.title   → Section heading
testimonials.subtitle
testimonials.review1.quote
testimonials.review2.quote
testimonials.review3.quote
download.title       → CTA heading
download.description → CTA text
download.platforms   → Platform list
privacy.title        → Section heading
privacy.description  → Privacy text
privacy.link         → Link text
footer.appStore      → Link text
footer.privacy       → Link text
footer.terms         → Link text
footer.copyright     → Copyright notice
```

---

## Language Codes

| Language | Code | Directory | OG Locale |
|----------|------|-----------|-----------|
| English | en | / | en_US |
| Chinese Simplified | zh-Hans | /zh-Hans/ | zh_CN |
| Chinese Traditional | zh-Hant | /zh-Hant/ | zh_TW |
| Japanese | ja | /ja/ | ja_JP |
| Korean | ko | /ko/ | ko_KR |
| French | fr | /fr/ | fr_FR |
| German | de | /de/ | de_DE |
| Spanish | es | /es/ | es_ES |
| Portuguese | pt | /pt/ | pt_BR |
| Italian | it | /it/ | it_IT |
| Russian | ru | /ru/ | ru_RU |
| Hindi | hi | /hi/ | hi_IN |
| Indonesian | id | /id/ | id_ID |
| Vietnamese | vi | /vi/ | vi_VN |

---

## URLs

| Language | URL |
|----------|-----|
| English | https://masawata.net/FitnessStory/ |
| Japanese | https://masawata.net/FitnessStory/ja/ |
| Korean | https://masawata.net/FitnessStory/ko/ |
| Chinese (Simplified) | https://masawata.net/FitnessStory/zh-Hans/ |
| Chinese (Traditional) | https://masawata.net/FitnessStory/zh-Hant/ |
| ... | https://masawata.net/FitnessStory/[code]/ |

---

## Troubleshooting

### JSON Parse Error
```
json.decoder.JSONDecodeError: Expecting ',' delimiter
```
**Fix:** Check for missing commas or special quote characters in the JSON file

### Images Not Loading
**Fix:** Check that asset paths use `../` prefix in subdirectory pages (handled by build script)

### Build Creates 0 Files
**Fix:** Ensure you're running from the correct directory:
```bash
cd /path/to/FitnessStory
python3 build.py
```

---

## SEO Checklist

After making changes:

- [ ] Run `python3 build.py`
- [ ] Verify `<title>` is localized (view page source)
- [ ] Verify `<meta description>` is localized
- [ ] Verify `og:locale` is correct (e.g., `ja_JP` for Japanese)
- [ ] Check sitemap.xml has updated `<lastmod>` date
- [ ] Test social sharing preview (Facebook Debugger)

---

## Contact

For questions about this codebase, refer to:
- `README.md` - Overview and setup
- `docs/TECHNICAL.md` - Deep technical details
