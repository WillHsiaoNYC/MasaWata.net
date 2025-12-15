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

## Image Workflow

### Folder Structure

```
images/
├── en/
│   ├── raw/                    # Original screenshots (source of truth for ALL languages)
│   │   ├── Title.png           # Hero image raw
│   │   ├── Storyline.png       # Feature images raw
│   │   ├── Dashboard.png
│   │   ├── Action_*.png        # Screenshot gallery raw (prefix: Action_)
│   │   └── ...
│   ├── title.jpg               # Optimized hero image
│   ├── storyline.jpg           # Optimized feature images (kebab-case)
│   ├── dashboard.jpg
│   ├── action-*.jpg            # Optimized screenshot gallery (prefix: action-)
│   └── ...
├── ja/                         # Optimized Japanese images (when localized)
├── ko/                         # Optimized Korean images
├── zh-Hans/                    # Optimized Chinese (Simplified) images
├── zh-Hant/                    # Optimized Chinese (Traditional) images
├── fr/                         # Optimized French images
├── de/                         # Optimized German images
├── es/                         # Optimized Spanish images
├── pt/                         # Optimized Portuguese images
├── it/                         # Optimized Italian images
├── ru/                         # Optimized Russian images
├── hi/                         # Optimized Hindi images
├── id/                         # Optimized Indonesian images
└── vi/                         # Optimized Vietnamese images
```

### Image Categories

| Category | Raw Naming | Optimized Naming | Used In |
|----------|------------|------------------|---------|
| Hero | `Title.png` | `title.jpg` | Page top device frame |
| Features | `[Name].png` | `kebab-case.jpg` | Features section cards |
| Screenshots | `Action_[Name].png` | `action-kebab-case.jpg` | "See It In Action" gallery |

### Workflow

1. **Save raw screenshots** to `images/en/raw/`
   - Use descriptive names with spaces (e.g., `Personal Records.png`)
   - Prefix screenshot gallery images with `Action_` (e.g., `Action_Dashboard Calendar.png`)

2. **Optimize images** for web use (Python with Pillow):
   ```python
   from PIL import Image

   img = Image.open('raw/Example.png')
   if img.mode == 'RGBA':
       background = Image.new('RGB', img.size, (255, 255, 255))
       background.paste(img, mask=img.split()[3])
       img = background

   # Resize to 660px width
   new_width = 660
   new_height = int(img.size[1] * (new_width / img.size[0]))
   img_resized = img.resize((new_width, new_height), Image.LANCZOS)

   # Save as JPEG with quality 85
   img_resized.save('example.jpg', 'JPEG', quality=85, optimize=True)
   ```

3. **Save optimized images** to the appropriate language folder:
   - English: `images/en/`
   - Other languages: `images/[lang-code]/` (e.g., `images/ja/`, `images/ko/`)

### Image Optimization Guidelines

- **Format**: JPEG (quality 85) for all images
- **Dimensions**: 660px width (maintains aspect ratio)
- **Target size**: Under 200KB per image (typically achieves 90-97% reduction)
- **Naming**:
  - Use kebab-case for output files (e.g., `personal-records.jpg`)
  - Prefix gallery images with `action-` (e.g., `action-dashboard-calendar.jpg`)

### Adding Localized Screenshots

When adding screenshots for a new language:

1. Take screenshots in that language from the app
2. Save raw versions to `images/en/raw/` (or create `images/[lang]/raw/` if preferred)
3. Optimize and save to `images/[lang]/` using the same filenames as English
4. Update `build.py` if image paths need language-specific handling

## Common Issues

- **JSON parse errors**: Check for unescaped quotes or curly quote characters (`""`) in translation files. Use straight quotes or escape them.
- **Images not loading in subdirectories**: Asset paths should be relative; the build script handles this automatically.
