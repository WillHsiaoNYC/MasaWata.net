#!/usr/bin/env python3
"""
Build script to generate localized HTML files for WhereWasI SEO
Run with: python3 build.py
"""

import json
import os
from datetime import date

# Supported languages
LANGUAGES = [
    {'code': 'en', 'name': 'English', 'dir': ''},
    {'code': 'zh-Hans', 'name': 'Chinese Simplified', 'dir': 'zh-Hans'},
    {'code': 'zh-Hant', 'name': 'Chinese Traditional', 'dir': 'zh-Hant'},
    {'code': 'ja', 'name': 'Japanese', 'dir': 'ja'},
    {'code': 'ko', 'name': 'Korean', 'dir': 'ko'},
    {'code': 'fr', 'name': 'French', 'dir': 'fr'},
    {'code': 'de', 'name': 'German', 'dir': 'de'},
    {'code': 'es', 'name': 'Spanish', 'dir': 'es'},
    {'code': 'pt', 'name': 'Portuguese', 'dir': 'pt'},
    {'code': 'it', 'name': 'Italian', 'dir': 'it'},
    {'code': 'ru', 'name': 'Russian', 'dir': 'ru'},
    {'code': 'hi', 'name': 'Hindi', 'dir': 'hi'},
    {'code': 'id', 'name': 'Indonesian', 'dir': 'id'},
    {'code': 'vi', 'name': 'Vietnamese', 'dir': 'vi'},
]

APP_STORE_ID = '6758056060'
BASE_URL = 'https://masawata.net/WhereWasI'

OG_LOCALES = {
    'en': 'en_US',
    'zh-Hans': 'zh_CN',
    'zh-Hant': 'zh_TW',
    'ja': 'ja_JP',
    'ko': 'ko_KR',
    'fr': 'fr_FR',
    'de': 'de_DE',
    'es': 'es_ES',
    'pt': 'pt_BR',
    'it': 'it_IT',
    'ru': 'ru_RU',
    'hi': 'hi_IN',
    'id': 'id_ID',
    'vi': 'vi_VN',
}

# Google Analytics tracking code
GOOGLE_ANALYTICS = '''<!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZL852HY2Z4"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      // Only track on production
      if (location.hostname !== 'localhost' && location.hostname !== '127.0.0.1') {
        gtag('config', 'G-ZL852HY2Z4');
      }
    </script>'''

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Feature icons mapping
FEATURE_ICONS = {
    'clock': '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
            </svg>''',
    'chart': '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="20" x2="18" y2="10"></line>
                <line x1="12" y1="20" x2="12" y2="4"></line>
                <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>''',
    'map': '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
                <line x1="8" y1="2" x2="8" y2="18"></line>
                <line x1="16" y1="6" x2="16" y2="22"></line>
            </svg>''',
    'shield': '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>''',
}

# Feature colors
FEATURE_COLORS = {
    'timeline': 'blue',
    'statistics': 'green',
    'map': 'purple',
    'privacy': 'yellow',
}


def load_translation(lang_code):
    filepath = os.path.join(SCRIPT_DIR, 'locales', f'{lang_code}.json')
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_hreflang_tags():
    tags = ''
    for lang in LANGUAGES:
        url = f"{BASE_URL}/{lang['dir']}/" if lang['dir'] else f"{BASE_URL}/"
        tags += f'    <link rel="alternate" hreflang="{lang["code"]}" href="{url}">\n'
    tags += f'    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/">'
    return tags


def get_asset_path(lang_dir):
    return '../' if lang_dir else ''


def generate_features_html(features_list, asset_path):
    """Generate HTML for 4 feature cards."""
    features_html = ''
    for i, feature in enumerate(features_list):
        feature_id = feature.get('id', f'feature-{i}')
        icon_type = feature.get('icon', 'clock')
        icon_svg = FEATURE_ICONS.get(icon_type, FEATURE_ICONS['clock'])
        color = FEATURE_COLORS.get(feature_id, 'blue')
        delay = i * 100

        features_html += f'''
                    <div class="feature-card" data-aos="fade-up" data-aos-delay="{delay}">
                        <div class="feature-card__icon feature-card__icon--{color}">
                            {icon_svg}
                        </div>
                        <h3 class="feature-card__title">{feature['title']}</h3>
                        <p class="feature-card__description">{feature['description']}</p>
                    </div>
'''
    return features_html


def generate_faq_html(faq_items):
    """Generate HTML for FAQ accordion items."""
    faq_html = ''
    for i, item in enumerate(faq_items):
        delay = i * 100
        faq_html += f'''
                    <div class="faq__item" data-aos="fade-up" data-aos-delay="{delay}">
                        <button class="faq__question" aria-expanded="false">
                            <span>{item['question']}</span>
                            <svg class="faq__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="6 9 12 15 18 9"></polyline>
                            </svg>
                        </button>
                        <div class="faq__answer">
                            <p>{item['answer']}</p>
                        </div>
                    </div>
'''
    return faq_html


def generate_html(lang, translations):
    asset_path = get_asset_path(lang['dir'])
    canonical_url = f"{BASE_URL}/{lang['dir']}/" if lang['dir'] else f"{BASE_URL}/"
    hreflang_tags = generate_hreflang_tags()
    og_locale = OG_LOCALES.get(lang['code'], 'en_US')
    t = translations

    # Generate language selector links
    lang_links = ''
    for l in LANGUAGES:
        active = ' active' if l['code'] == lang['code'] else ''
        href = f"{asset_path}{l['dir']}/" if l['dir'] else f"{asset_path}"
        lang_names = {
            'en': 'English', 'zh-Hans': '简体中文', 'zh-Hant': '繁體中文',
            'ja': '日本語', 'ko': '한국어', 'fr': 'Français',
            'de': 'Deutsch', 'es': 'Español', 'pt': 'Português',
            'it': 'Italiano', 'ru': 'Русский', 'hi': 'हिन्दी',
            'id': 'Indonesia', 'vi': 'Tiếng Việt'
        }
        lang_links += f'                    <a href="{href}" class="language-option{active}">{lang_names[l["code"]]}</a>\n'

    # Generate features HTML
    features_html = generate_features_html(t['features']['list'], asset_path)

    # Generate FAQ HTML
    faq_html = generate_faq_html(t['faq']['list'])

    html = f'''<!DOCTYPE html>
<html lang="{lang['code']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

{GOOGLE_ANALYTICS}

    <!-- Primary Meta Tags -->
    <title>{t['meta']['title']}</title>
    <meta name="title" content="{t['meta']['title']}">
    <meta name="description" content="{t['meta']['description']}">
    <meta name="keywords" content="{t['meta'].get('keywords', 'location journal, places visited, location tracking, travel log, iOS app, privacy')}">
    <meta name="author" content="Weiren Hsiao">
    <meta name="robots" content="index, follow">

    <!-- Canonical URL -->
    <link rel="canonical" href="{canonical_url}">

    <!-- Hreflang Tags for Multi-language SEO -->
{hreflang_tags}

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{t['meta']['title']}">
    <meta property="og:description" content="{t['meta']['description']}">
    <meta property="og:image" content="{BASE_URL}/images/WhereWasI.png">
    <meta property="og:site_name" content="{t['appName']}">
    <meta property="og:locale" content="{og_locale}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{t['meta']['title']}">
    <meta name="twitter:description" content="{t['meta']['description']}">
    <meta name="twitter:image" content="{BASE_URL}/images/WhereWasI.png">

    <!-- App Store Smart Banner -->
    <meta name="apple-itunes-app" content="app-id={APP_STORE_ID}">

    <!-- Favicon -->
    <link rel="icon" type="image/png" href="{asset_path}images/WhereWasI.png">
    <link rel="apple-touch-icon" href="{asset_path}images/WhereWasI.png">

    <!-- Stylesheets -->
    <link rel="stylesheet" href="{asset_path}css/style.css?v=1.1">

    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "{t['appName']}",
        "operatingSystem": "iOS",
        "applicationCategory": "LifestyleApplication",
        "offers": {{
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        }},
        "description": "{t['meta']['description']}",
        "screenshot": "{BASE_URL}/images/en/screenshot.png",
        "softwareVersion": "1.0",
        "author": {{
            "@type": "Person",
            "name": "Weiren Hsiao"
        }},
        "inLanguage": "{lang['code']}"
    }}
    </script>
</head>
<body>
    <!-- Header -->
    <header class="header" id="header">
        <nav class="nav container">
            <a href="{asset_path}" class="nav__logo">
                <img src="{asset_path}images/WhereWasI.png" alt="WhereWasI" class="nav__logo-img">
                <span class="nav__logo-text">{t['appName']}</span>
            </a>

            <ul class="nav__menu" id="nav-menu">
                <li class="nav__item">
                    <a href="#features" class="nav__link">{t['nav']['features']}</a>
                </li>
                <li class="nav__item">
                    <a href="#screenshots" class="nav__link">{t['nav']['screenshots']}</a>
                </li>
                <li class="nav__item">
                    <a href="#download" class="nav__link">{t['nav']['download']}</a>
                </li>
                <li class="nav__item">
                    <a href="#faq" class="nav__link">{t['nav']['faq']}</a>
                </li>
            </ul>

            <!-- Language Selector -->
            <div class="language-selector" id="header-language-selector">
                <button class="language-btn" aria-label="Select Language">
                    <svg class="language-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="2" y1="12" x2="22" y2="12"></line>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                    </svg>
                    <span class="current-lang">{lang['code'].upper()[:2]}</span>
                    <svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                </button>
                <div class="language-dropdown">
{lang_links}                </div>
            </div>

            <!-- Mobile Menu Toggle -->
            <button class="nav__toggle" id="nav-toggle" aria-label="Toggle Menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </nav>
    </header>

    <main>
        <!-- Hero Section -->
        <section class="hero" id="hero">
            <div class="hero__container container">
                <div class="hero__content">
                    <img src="{asset_path}images/WhereWasI.png" alt="WhereWasI App Icon" class="hero__icon">
                    <h1 class="hero__title">{t['hero']['title']}</h1>
                    <p class="hero__description">{t['hero']['description']}</p>
                    <a href="https://apps.apple.com/app/apple-store/id{APP_STORE_ID}?pt=127843312&ct=WEB&mt=8" class="hero__download" target="_blank" rel="noopener">
                        <img src="{asset_path}assets/app-store-badges/app-store-badge-{lang['code']}.svg" alt="{t['hero'].get('downloadAlt', 'Download on the App Store')}" class="app-store-badge" onerror="this.src='{asset_path}assets/app-store-badges/app-store-badge-en.svg'">
                    </a>
                </div>
                <div class="hero__device">
                    <div class="device-frame">
                        <img src="{asset_path}images/en/title.jpg" alt="WhereWasI Screenshot" class="device-screen">
                    </div>
                </div>
            </div>
            <div class="hero__gradient"></div>
        </section>

        <!-- Features Section -->
        <section class="features" id="features">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['features']['sectionTitle']}</h2>
                    <p class="section-subtitle">{t['features']['sectionSubtitle']}</p>
                </div>

                <div class="features__grid features__grid--4">
{features_html}
                </div>
            </div>
        </section>

        <!-- Screenshots Section -->
        <section class="screenshots" id="screenshots">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['screenshots']['sectionTitle']}</h2>
                    <p class="section-subtitle">{t['screenshots']['sectionSubtitle']}</p>
                </div>

                <div class="screenshots__gallery">
                    <div class="screenshots__track" id="screenshots-track">
                        <div class="screenshot-item"><img src="{asset_path}images/en/screenshot-1.jpg" alt="Screenshot 1" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/en/screenshot-2.jpg" alt="Screenshot 2" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/en/screenshot-3.jpg" alt="Screenshot 3" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/en/screenshot-4.jpg" alt="Screenshot 4" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/en/screenshot-5.jpg" alt="Screenshot 5" loading="lazy"></div>
                    </div>
                </div>

                <div class="screenshots__nav">
                    <button class="screenshots__btn screenshots__btn--prev" id="screenshots-prev" aria-label="Previous">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
                    </button>
                    <button class="screenshots__btn screenshots__btn--next" id="screenshots-next" aria-label="Next">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
                    </button>
                </div>
            </div>
        </section>

        <!-- Download Section -->
        <section class="download" id="download">
            <div class="container">
                <div class="download__content">
                    <img src="{asset_path}images/WhereWasI.png" alt="WhereWasI" class="download__icon">
                    <h2 class="download__title">{t['download']['title']}</h2>
                    <p class="download__description">{t['download']['description']}</p>
                    <a href="https://apps.apple.com/app/apple-store/id{APP_STORE_ID}?pt=127843312&ct=WEB&mt=8" class="download__button" target="_blank" rel="noopener">
                        <img src="{asset_path}assets/app-store-badges/app-store-badge-{lang['code']}.svg" alt="Download on the App Store" class="app-store-badge" onerror="this.src='{asset_path}assets/app-store-badges/app-store-badge-en.svg'">
                    </a>
                    <div class="download__platforms">
                        <span class="platform-badge">{t['download']['platforms']}</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- FAQ Section -->
        <section class="faq" id="faq">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['faq']['sectionTitle']}</h2>
                    <p class="section-subtitle">{t['faq']['sectionSubtitle']}</p>
                </div>

                <div class="faq__list">
{faq_html}
                </div>
            </div>
        </section>

        <!-- Privacy Section -->
        <section class="privacy" id="privacy">
            <div class="container">
                <div class="privacy__content">
                    <div class="privacy__icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        </svg>
                    </div>
                    <h2 class="privacy__title">{t['privacy']['title']}</h2>
                    <p class="privacy__description">{t['privacy']['description']}</p>
                    <a href="https://masawata.net/privacy-policy.html" class="privacy__link">{t['privacy']['link']}</a>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer__content">
                <div class="footer__brand">
                    <img src="{asset_path}images/WhereWasI.png" alt="WhereWasI" class="footer__logo">
                    <span class="footer__name">{t['appName']}</span>
                </div>
                <div class="footer__links">
                    <a href="https://apps.apple.com/app/apple-store/id{APP_STORE_ID}?pt=127843312&ct=WEB&mt=8" target="_blank" rel="noopener">{t['footer']['appStore']}</a>
                    <a href="https://masawata.net/privacy-policy.html">{t['footer']['privacyPolicy']}</a>
                    <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/" target="_blank" rel="noopener">{t['footer']['termsOfService']}</a>
                </div>
                <p class="footer__copyright">{t['footer']['copyright']}</p>
            </div>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="{asset_path}js/main.js?v=1.1"></script>
</body>
</html>'''
    return html


def generate_sitemap():
    today = date.today().isoformat()
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
'''
    for lang in LANGUAGES:
        url = f"{BASE_URL}/{lang['dir']}/" if lang['dir'] else f"{BASE_URL}/"
        priority = '1.0' if lang['code'] == 'en' else '0.9'

        sitemap += f'''
    <url>
        <loc>{url}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>{priority}</priority>
'''
        for alt_lang in LANGUAGES:
            alt_url = f"{BASE_URL}/{alt_lang['dir']}/" if alt_lang['dir'] else f"{BASE_URL}/"
            sitemap += f'        <xhtml:link rel="alternate" hreflang="{alt_lang["code"]}" href="{alt_url}"/>\n'
        sitemap += f'        <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}/"/>\n'
        sitemap += '    </url>\n'

    sitemap += '</urlset>'
    return sitemap


def build():
    print('Building localized HTML files for WhereWasI...\n')

    generated_count = 0

    for lang in LANGUAGES:
        translations = load_translation(lang['code'])

        if translations is None:
            dir_display = f"{lang['dir']}/" if lang['dir'] else ''
            print(f"  Skipped: {dir_display}index.html ({lang['name']}) - locale file not found")
            continue

        html = generate_html(lang, translations)

        # Determine output directory
        if lang['dir']:
            output_dir = os.path.join(SCRIPT_DIR, lang['dir'])
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = SCRIPT_DIR

        # Write HTML file
        filepath = os.path.join(output_dir, 'index.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        dir_display = f"{lang['dir']}/" if lang['dir'] else ''
        print(f"  Created: {dir_display}index.html ({lang['name']})")
        generated_count += 1

    # Generate sitemap
    sitemap = generate_sitemap()
    sitemap_path = os.path.join(SCRIPT_DIR, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print('\n  Updated: sitemap.xml')

    print(f'\nBuild complete! Generated {generated_count} localized pages.')


if __name__ == '__main__':
    build()
