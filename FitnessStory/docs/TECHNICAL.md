# Technical Documentation

This document provides detailed technical information about the Fitness Story website implementation.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Build Time                                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ locales/*.json│ → │  build.py   │ → │ index.html (x14)    │  │
│  │ (14 files)   │    │             │    │ sitemap.xml         │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Runtime                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ User Request│ → │ Static HTML │ → │ Browser Renders      │  │
│  │ /ja/        │    │ ja/index.html│   │ + CSS + JS          │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Build System Deep Dive

### build.py Complete Code Walkthrough

#### Imports and Constants

```python
import json
import os
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
```

- `json`: Parse translation files
- `os`: File system operations (path joining, directory creation)
- `datetime.date`: Generate today's date for sitemap
- `SCRIPT_DIR`: Absolute path to the script's directory (ensures correct paths regardless of where script is run from)

#### Language Configuration

```python
LANGUAGES = [
    {'code': 'en', 'name': 'English', 'dir': ''},
    {'code': 'zh-Hans', 'name': 'Chinese Simplified', 'dir': 'zh-Hans'},
    # ...
]
```

Each language entry contains:
- `code`: ISO language code (used in hreflang, JSON filename)
- `name`: Human-readable name (used in console output)
- `dir`: Subdirectory name (empty string for English = root)

#### Open Graph Locale Mapping

```python
OG_LOCALES = {
    'en': 'en_US',
    'zh-Hans': 'zh_CN',
    'zh-Hant': 'zh_TW',
    'ja': 'ja_JP',
    # ...
}
```

Facebook Open Graph requires locale format `ll_CC` (language_COUNTRY). This maps our language codes to the correct format.

### HTML Generation Process

#### Template String Approach

The script uses Python f-strings to generate HTML:

```python
html = f'''<!DOCTYPE html>
<html lang="{lang['code']}">
<head>
    <title>{t['meta']['title']}</title>
    ...
</head>
'''
```

**Advantages:**
- No external templating dependencies
- Easy to understand and modify
- Full control over output
- Fast execution

**Escaping JSON in HTML:**

For the JSON-LD structured data block, we need double braces to escape in f-strings:

```python
html = f'''
<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{t['appName']}",
}}
</script>
'''
```

`{{` becomes `{` in the output, allowing us to write literal JSON.

### Asset Path Resolution

```python
def get_asset_path(lang_dir):
    return '../' if lang_dir else ''
```

**Problem:** Language subdirectories need relative paths to reach assets in root.

**Solution:**
- Root (`/index.html`): Assets at `images/foo.png`
- Subdirectory (`/ja/index.html`): Assets at `../images/foo.png`

**Usage in template:**
```python
<img src="{asset_path}images/Fitness%20Story.png" alt="...">
```

### Hreflang Implementation

```python
def generate_hreflang_tags():
    tags = ''
    for lang in LANGUAGES:
        url = f"{BASE_URL}/{lang['dir']}/" if lang['dir'] else f"{BASE_URL}/"
        tags += f'    <link rel="alternate" hreflang="{lang["code"]}" href="{url}">\n'
    tags += f'    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/">'
    return tags
```

**Output:**
```html
<link rel="alternate" hreflang="en" href="https://masawata.net/FitnessStory/">
<link rel="alternate" hreflang="zh-Hans" href="https://masawata.net/FitnessStory/zh-Hans/">
...
<link rel="alternate" hreflang="x-default" href="https://masawata.net/FitnessStory/">
```

**What `x-default` means:**
- Fallback for users whose language isn't in the list
- Google shows this version when no language match

### Sitemap Generation

```python
def generate_sitemap():
    today = date.today().isoformat()  # "2025-12-10"

    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
'''
```

**XML Namespaces:**
- `sitemaps.org/schemas/sitemap/0.9`: Standard sitemap schema
- `w3.org/1999/xhtml`: Required for `xhtml:link` elements

**Per-URL Structure:**
```xml
<url>
    <loc>https://masawata.net/FitnessStory/ja/</loc>
    <lastmod>2025-12-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="en" href="..."/>
    <xhtml:link rel="alternate" hreflang="ja" href="..."/>
    <!-- All 14 languages cross-referenced -->
</url>
```

**Priority Values:**
- `1.0` for English (default/primary)
- `0.9` for other languages

---

## CSS Architecture

### File: `/css/style.css`

#### CSS Custom Properties (Variables)

```css
:root {
    --color-primary: #007AFF;
    --color-red: #FF3B30;
    --color-yellow: #FFCC00;
    --color-green: #34C759;
    --color-text: #1D1D1F;
    --color-text-secondary: #86868B;
    --color-bg: #FFFFFF;
    --color-bg-secondary: #F5F5F7;
}
```

Colors derived from the Fitness Story app icon for brand consistency.

#### Responsive Breakpoints

```css
/* Mobile first approach */
.container {
    padding: 0 1rem;
}

/* Tablet */
@media (min-width: 768px) {
    .container {
        padding: 0 2rem;
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
}
```

#### BEM Naming Convention

```css
/* Block */
.feature-card { }

/* Element */
.feature-card__title { }
.feature-card__description { }
.feature-card__icon { }

/* Modifier */
.feature-card__icon--blue { }
.feature-card__icon--green { }
```

---

## JavaScript Architecture

### File: `/js/main.js`

#### Screenshot Gallery

```javascript
// State
let currentSlide = 0;
const track = document.getElementById('screenshots-track');
const slides = track.querySelectorAll('.screenshot-item');

// Navigation
function goToSlide(index) {
    currentSlide = Math.max(0, Math.min(index, slides.length - 1));
    const offset = currentSlide * slideWidth;
    track.style.transform = `translateX(-${offset}px)`;
}

// Event listeners
document.getElementById('screenshots-prev').addEventListener('click', () => {
    goToSlide(currentSlide - 1);
});
```

#### Language Dropdown Toggle

```javascript
const langBtn = document.getElementById('language-btn');
const langDropdown = document.getElementById('language-dropdown');

langBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    langDropdown.classList.toggle('active');
});

// Close on outside click
document.addEventListener('click', () => {
    langDropdown.classList.remove('active');
});
```

#### Smooth Scrolling

```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({ behavior: 'smooth' });
    });
});
```

#### Scroll Animations (Intersection Observer)

```javascript
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('[data-aos]').forEach(el => {
    observer.observe(el);
});
```

---

## SEO Technical Details

### Meta Tag Priority

Search engines prioritize meta information in this order:

1. **`<title>`** - Most important for rankings
2. **`<meta name="description">`** - Shown in search results
3. **`<h1>`** - Primary heading (should match title theme)
4. **Structured Data (JSON-LD)** - Rich snippets in search results

### Structured Data Schema

```json
{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Fitness Story",
    "operatingSystem": "iOS",
    "applicationCategory": "HealthApplication",
    "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
    },
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "ratingCount": "23"
    }
}
```

**Benefits:**
- App rating stars in Google search results
- Rich snippet with app information
- Better click-through rates

### Canonical URL Strategy

Each page declares itself as canonical:

```html
<!-- On /ja/index.html -->
<link rel="canonical" href="https://masawata.net/FitnessStory/ja/">
```

This prevents duplicate content issues if pages are accessed via different URLs.

### Open Graph Best Practices

```html
<meta property="og:type" content="website">
<meta property="og:image" content="https://masawata.net/FitnessStory/images/Fitness%20Story.png">
```

**Image requirements for social sharing:**
- Minimum 1200x630 pixels recommended
- Use absolute URLs (not relative)
- URL-encode special characters in filenames

---

## Localization Details

### JSON File Encoding

All JSON files must be UTF-8 encoded to support:
- CJK characters (Chinese, Japanese, Korean)
- Devanagari (Hindi)
- Cyrillic (Russian)

### Special Characters in JSON

Avoid these characters in JSON string values:
- Literal `"` - Use `\"` or different quotes
- Curly quotes `""` - Can cause parsing issues
- Line breaks - Use `\n` if needed

**Example fix:**
```json
// Problem
"description": "Tags like "Intervals" or "Recovery""

// Solution
"description": "Tags like 'Intervals' or 'Recovery'"
```

### Right-to-Left (RTL) Languages

Currently not supported, but if adding Arabic/Hebrew:

1. Add `dir="rtl"` to `<html>` tag
2. Add RTL CSS:
```css
[dir="rtl"] .nav__menu {
    flex-direction: row-reverse;
}
```

---

## Performance Considerations

### Image Optimization

Screenshots should be:
- Compressed (use tools like ImageOptim)
- Appropriate resolution (not 4K for thumbnails)
- WebP format with JPEG fallback (optional)

### Lazy Loading

```html
<img src="..." loading="lazy" alt="...">
```

All non-critical images use `loading="lazy"` to defer loading until needed.

### Minimal JavaScript

- No frameworks (React, Vue, etc.)
- No build step required for JS
- ~5KB total JavaScript

### CSS Efficiency

- Single CSS file (reduces HTTP requests)
- No CSS framework overhead
- Efficient selectors (avoid deep nesting)

---

## Security Considerations

### External Links

All external links use:
```html
<a href="..." target="_blank" rel="noopener">
```

`rel="noopener"` prevents:
- Reverse tabnapping attacks
- Performance issues with `window.opener`

### Content Security

- No inline JavaScript (all in external files)
- No user-generated content (static site)
- HTTPS enforced via hosting

---

## Testing Checklist

### SEO Validation

- [ ] Google Rich Results Test (structured data)
- [ ] Facebook Sharing Debugger (Open Graph)
- [ ] Twitter Card Validator
- [ ] Google Search Console (after deployment)

### Cross-Browser Testing

- [ ] Chrome (Windows, Mac)
- [ ] Safari (Mac, iOS)
- [ ] Firefox
- [ ] Edge
- [ ] Mobile Safari
- [ ] Chrome Mobile

### Accessibility Testing

- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Color contrast ratios
- [ ] Alt text on images

### Performance Testing

- [ ] Google PageSpeed Insights
- [ ] Lighthouse audit
- [ ] Mobile loading time

---

## Common Issues and Solutions

### Issue: Build script fails with encoding error

**Cause:** Non-UTF-8 characters in JSON files

**Solution:**
```bash
# Check file encoding
file locales/ja.json

# Convert to UTF-8 if needed
iconv -f ISO-8859-1 -t UTF-8 locales/ja.json > locales/ja_utf8.json
```

### Issue: Images not found in production

**Cause:** Case-sensitive file systems

**Solution:** Ensure filenames match exactly (including spaces, capitalization)

### Issue: Language selector not working

**Cause:** JavaScript error

**Solution:** Check browser console for errors, ensure `main.js` is loaded

### Issue: Social sharing shows wrong language

**Cause:** Social crawlers cache aggressively

**Solution:** Use Facebook/Twitter debugger tools to clear cache and re-scrape

---

## Maintenance Schedule

### Weekly
- Check for broken links
- Monitor Google Search Console for errors

### Monthly
- Update `<lastmod>` in sitemap (automatic via build script)
- Review analytics for language traffic

### Quarterly
- Update App Store rating count in structured data
- Review and update testimonials if needed
- Check for outdated dependencies

### Annually
- Update copyright year in footer
- Review and refresh translations
- Update screenshots if app UI changed
