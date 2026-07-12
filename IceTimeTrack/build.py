#!/usr/bin/env python3
"""
Build script to generate localized HTML files for IceTimeTrack SEO.
Run with: python3 build.py
"""

import json
import os
from datetime import date

LANGUAGES = [
    {'code': 'en', 'name': 'English', 'dir': ''},
    {'code': 'cs', 'name': 'Czech', 'dir': 'cs'},
    {'code': 'da', 'name': 'Danish', 'dir': 'da'},
    {'code': 'de', 'name': 'German', 'dir': 'de'},
    {'code': 'es', 'name': 'Spanish', 'dir': 'es'},
    {'code': 'fi', 'name': 'Finnish', 'dir': 'fi'},
    {'code': 'fr', 'name': 'French', 'dir': 'fr'},
    {'code': 'hu', 'name': 'Hungarian', 'dir': 'hu'},
    {'code': 'it', 'name': 'Italian', 'dir': 'it'},
    {'code': 'ja', 'name': 'Japanese', 'dir': 'ja'},
    {'code': 'ko', 'name': 'Korean', 'dir': 'ko'},
    {'code': 'nb', 'name': 'Norwegian Bokmål', 'dir': 'nb'},
    {'code': 'ru', 'name': 'Russian', 'dir': 'ru'},
    {'code': 'sk', 'name': 'Slovak', 'dir': 'sk'},
    {'code': 'sv', 'name': 'Swedish', 'dir': 'sv'},
    {'code': 'zh-Hans', 'name': 'Chinese Simplified', 'dir': 'zh-Hans'},
    {'code': 'zh-Hant', 'name': 'Chinese Traditional', 'dir': 'zh-Hant'},
]

BASE_URL = 'https://masawata.net/IceTimeTrack'

OG_LOCALES = {
    'en': 'en_US', 'cs': 'cs_CZ', 'da': 'da_DK', 'de': 'de_DE',
    'es': 'es_ES', 'fi': 'fi_FI', 'fr': 'fr_FR', 'hu': 'hu_HU',
    'it': 'it_IT', 'ja': 'ja_JP', 'ko': 'ko_KR', 'nb': 'nb_NO',
    'ru': 'ru_RU', 'sk': 'sk_SK', 'sv': 'sv_SV',
    'zh-Hans': 'zh_CN', 'zh-Hant': 'zh_TW',
}

LANG_NAMES = {
    'en': 'English', 'cs': 'Čeština', 'da': 'Dansk', 'de': 'Deutsch',
    'es': 'Español', 'fi': 'Suomi', 'fr': 'Français', 'hu': 'Magyar',
    'it': 'Italiano', 'ja': '日本語', 'ko': '한국어', 'nb': 'Norsk',
    'ru': 'Русский', 'sk': 'Slovenčina', 'sv': 'Svenska',
    'zh-Hans': '简体中文', 'zh-Hant': '繁體中文',
}

GOOGLE_ANALYTICS = '''<!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZL852HY2Z4"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-ZL852HY2Z4');
    </script>'''

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_translation(lang_code):
    filepath = os.path.join(SCRIPT_DIR, 'locales', f'{lang_code}.json')
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


def generate_html(lang, translations):
    asset_path = get_asset_path(lang['dir'])
    canonical_url = f"{BASE_URL}/{lang['dir']}/" if lang['dir'] else f"{BASE_URL}/"
    hreflang_tags = generate_hreflang_tags()
    og_locale = OG_LOCALES.get(lang['code'], 'en_US')
    t = translations

    # Star SVG for testimonials
    star_svg = '<svg aria-hidden="true" viewBox="0 0 20 20" fill="currentColor"><path d="M10 1l2.39 4.84 5.34.78-3.87 3.77.91 5.32L10 13.27l-4.77 2.5.91-5.31L2.27 6.68l5.34-.78L10 1z"/></svg>'
    five_stars = (star_svg + '\n                            ') * 5

    # Language selector links
    lang_links = ''
    for l in LANGUAGES:
        active = ' active' if l['code'] == lang['code'] else ''
        href = f"{asset_path}{l['dir']}/" if l['dir'] else f"{asset_path}" if asset_path else "./"
        lang_links += f'                    <a href="{href}" class="language-option{active}">{LANG_NAMES[l["code"]]}</a>\n'

    # FAQ items HTML
    faq_html = ''
    for i, item in enumerate(t['faq']['items']):
        delay = (i % 5) * 100
        # Escape HTML special chars in answers
        answer = item['answer'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Convert newlines to <br> for multi-paragraph answers
        answer = answer.replace('\n\n', '</p><p>').replace('\n', '<br>')
        question = item['question'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Restore &amp; for already-escaped entities
        question = question.replace('&amp;amp;', '&amp;')
        answer = answer.replace('&amp;amp;', '&amp;')

        faq_html += f'''
                    <div class="faq__item" data-aos="fade-up" data-aos-delay="{delay}">
                        <button class="faq__question" aria-expanded="false">
                            <span>{question}</span>
                            <svg class="faq__icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="6 9 12 15 18 9"/>
                            </svg>
                        </button>
                        <div class="faq__answer">
                            <p>{answer}</p>
                        </div>
                    </div>
'''

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
    <meta name="keywords" content="hockey, ice time, shift tracking, Apple Watch, hockey app, ice hockey, shift detection, hockey stats, game tracker">
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
    <meta property="og:image" content="{BASE_URL}/images/og-image.png">
    <meta property="og:site_name" content="{t['appName']}">
    <meta property="og:locale" content="{og_locale}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{t['meta']['title']}">
    <meta name="twitter:description" content="{t['meta']['description']}">
    <meta name="twitter:image" content="{BASE_URL}/images/og-image.png">

    <!-- Apple Smart Banner (placeholder app-id) -->
    <meta name="apple-itunes-app" content="app-id=PLACEHOLDER">

    <!-- Favicon -->
    <link rel="icon" type="image/png" href="{asset_path}images/app-icon.png">
    <link rel="apple-touch-icon" href="{asset_path}images/app-icon.png">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

    <!-- Stylesheet -->
    <link rel="stylesheet" href="{asset_path}css/style.css">

    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "{t['appName']}",
        "operatingSystem": "iOS, watchOS",
        "applicationCategory": "SportsApplication",
        "sameAs": "https://apps.apple.com/app/id6758258172",
        "downloadUrl": "https://apps.apple.com/app/id6758258172",
        "publisher": {{
            "@type": "Organization",
            "name": "MasaWata Tech",
            "url": "https://masawata.net/"
        }},
        "offers": {{
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        }},
        "description": "{t['meta']['description']}",
        "author": {{
            "@type": "Person",
            "name": "Weiren Hsiao"
        }},
        "inLanguage": "{lang['code']}"
    }}
    </script>
</head>
<body>
    <header class="header" id="header">
        <nav class="nav container">
            <a href="{asset_path or './'}" class="nav__logo">
                <img src="{asset_path}images/app-icon.png" alt="{t['appName']}" class="nav__logo-icon">
                <span class="nav__logo-text">{t['appName']}</span>
            </a>

            <ul class="nav__menu" id="nav-menu">
                <li class="nav__item"><a href="#features" class="nav__link">{t['nav']['features']}</a></li>
                <li class="nav__item"><a href="#how-it-works" class="nav__link">{t['nav']['howItWorks']}</a></li>
                <li class="nav__item"><a href="#screenshots" class="nav__link">{t['nav']['screenshots']}</a></li>
                <li class="nav__item"><a href="#faq" class="nav__link">{t['nav']['faq']}</a></li>
                <li class="nav__item"><a href="#download" class="nav__link nav__link--cta" id="nav-cta">{t['nav']['cta']}</a></li>
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

            <button class="nav__toggle" id="nav-toggle" aria-label="Toggle Menu">
                <span></span><span></span><span></span>
            </button>
        </nav>
    </header>

    <main>
        <!-- Countdown Section -->
        <section class="countdown" id="countdown">
            <div class="container">
                <div class="countdown__content">
                    <h2 class="countdown__title" id="cd-title">{t['countdown']['title']}</h2>
                    <p class="countdown__promo countdown--hidden" id="cd-promo">{t['countdown']['promo']}</p>
                    <p class="countdown__promo-sub countdown--hidden" id="cd-promo-sub">{t['countdown']['promoSub']}</p>
                    <div class="countdown__timer">
                        <div class="countdown__unit">
                            <span class="countdown__number" id="cd-days">00</span>
                            <span class="countdown__label">{t['countdown']['days']}</span>
                        </div>
                        <span class="countdown__separator">:</span>
                        <div class="countdown__unit">
                            <span class="countdown__number" id="cd-hours">00</span>
                            <span class="countdown__label">{t['countdown']['hours']}</span>
                        </div>
                        <span class="countdown__separator">:</span>
                        <div class="countdown__unit">
                            <span class="countdown__number" id="cd-minutes">00</span>
                            <span class="countdown__label">{t['countdown']['minutes']}</span>
                        </div>
                        <span class="countdown__separator">:</span>
                        <div class="countdown__unit">
                            <span class="countdown__number" id="cd-seconds">00</span>
                            <span class="countdown__label">{t['countdown']['seconds']}</span>
                        </div>
                    </div>
                    <p class="countdown__date" id="cd-date">{t['countdown']['date']}</p>
                    <a href="https://apps.apple.com/redeem?ctx=offercodes&id=6758258172&code=LAUNCH" class="countdown__claim-btn countdown--hidden" id="cd-claim" target="_blank" rel="noopener">{t['countdown']['claimOffer']}</a>
                </div>
            </div>
        </section>

        <section class="hero" id="hero">
            <div class="hero__bg"></div>
            <div class="hero__container container">
                <div class="hero__content">
                    <div class="hero__icon-wrapper">
                        <img src="{asset_path}images/app-icon.png" alt="{t['appName']} app icon" class="hero__icon">
                    </div>

                    <h1 class="hero__title">{t['hero']['title']}</h1>
                    <p class="hero__description">{t['hero']['description']}</p>

                    <a href="https://apps.apple.com/us/app/ice-time-track/id6758258172?ct=WEB" class="launch-btn" id="hero-download" target="_blank" rel="noopener">{t['hero']['preOrder']}</a>

                    <img src="{asset_path}assets/app-store-badges/app-store-badge-{lang['code']}.svg" alt="App Store" class="app-store-badge app-store-badge--static" onerror="this.src='{asset_path}assets/app-store-badges/app-store-badge-en.svg'">

                    <p class="hero__platforms">{t['hero']['platforms']}</p>

                    <div class="hero__callouts">
                        <div class="hero__callout">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                            <span>{t['hero']['shiftDetection']}</span>
                        </div>
                        <div class="hero__callout">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v8M8 12h8"/></svg>
                            <span>{t['hero']['goalTracking']}</span>
                        </div>
                        <div class="hero__callout">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 3v18"/></svg>
                            <span>{t['hero']['penaltyLogging']}</span>
                        </div>
                        <div class="hero__callout">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                            <span>{t['hero']['gameAnalytics']}</span>
                        </div>
                    </div>
                </div>

                <div class="hero__device">
                    <img src="{asset_path}images/hero-watch.png" alt="{t['appName']} on Apple Watch" class="hero__image">
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features" id="features">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['features']['title']}</h2>
                    <p class="section-subtitle">{t['features']['subtitle']}</p>
                </div>

                <div class="features__grid">
                    <div class="feature-card" data-aos="fade-up">
                        <div class="feature-card__icon">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['shiftDetection']['title']}</h3>
                        <p class="feature-card__description">{t['features']['shiftDetection']['description']}</p>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="100">
                        <div class="feature-card__icon">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/></svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['eventTracking']['title']}</h3>
                        <p class="feature-card__description">{t['features']['eventTracking']['description']}</p>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="200">
                        <div class="feature-card__icon">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['healthMetrics']['title']}</h3>
                        <p class="feature-card__description">{t['features']['healthMetrics']['description']}</p>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="300">
                        <div class="feature-card__icon">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['analytics']['title']}</h3>
                        <p class="feature-card__description">{t['features']['analytics']['description']}</p>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="400">
                        <div class="feature-card__icon">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/><path d="M16 16l2 2"/><path d="M8 16l-2 2"/></svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['healthIntegration']['title']}</h3>
                        <p class="feature-card__description">{t['features']['healthIntegration']['description']}</p>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="500">
                        <div class="feature-card__icon">
                            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="1" y1="1" x2="23" y2="23"/><path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"/><path d="M5 12.55a10.94 10.94 0 0 1 5.17-2.39"/><path d="M10.71 5.05A16 16 0 0 1 22.56 9"/><path d="M1.42 9a15.91 15.91 0 0 1 4.7-2.88"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['offline']['title']}</h3>
                        <p class="feature-card__description">{t['features']['offline']['description']}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- How It Works Section -->
        <section class="how-it-works" id="how-it-works">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['howItWorks']['title']}</h2>
                    <p class="section-subtitle">{t['howItWorks']['subtitle']}</p>
                </div>

                <div class="how-it-works__steps">
                    <div class="step" data-aos="fade-up" data-aos-delay="100">
                        <div class="step__number">1</div>
                        <h3 class="step__title">{t['howItWorks']['step1']['title']}</h3>
                        <p class="step__description">{t['howItWorks']['step1']['description']}</p>
                        <div class="step__device step__device--watch">
                            <img src="{asset_path}images/step-before.png" alt="{t['howItWorks']['step1']['title']}" class="step__device-img">
                        </div>
                    </div>

                    <div class="step" data-aos="fade-up" data-aos-delay="200">
                        <div class="step__number">2</div>
                        <h3 class="step__title">{t['howItWorks']['step2']['title']}</h3>
                        <p class="step__description">{t['howItWorks']['step2']['description']}</p>
                        <div class="step__device step__device--watch">
                            <img src="{asset_path}images/step-during.png" alt="{t['howItWorks']['step2']['title']}" class="step__device-img">
                        </div>
                    </div>

                    <div class="step" data-aos="fade-up" data-aos-delay="300">
                        <div class="step__number">3</div>
                        <h3 class="step__title">{t['howItWorks']['step3']['title']}</h3>
                        <p class="step__description">{t['howItWorks']['step3']['description']}</p>
                        <div class="step__device step__device--phone">
                            <img src="{asset_path}images/step-after.png" alt="{t['howItWorks']['step3']['title']}" class="step__device-img">
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Screenshots Gallery Section -->
        <section class="screenshots" id="screenshots">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['screenshots']['title']}</h2>
                    <p class="section-subtitle">{t['screenshots']['subtitle']}</p>
                </div>

                <div class="screenshots__gallery">
                    <button class="screenshots__arrow screenshots__arrow--prev" aria-label="Previous screenshot">
                        <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
                    </button>

                    <div class="screenshots__track">
                        <div class="screenshot-item screenshot-item--watch"><img src="{asset_path}images/watch-on-ice.png" alt="Apple Watch on-ice session" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--phone"><img src="{asset_path}images/phone-sessions.png" alt="iPhone sessions" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--watch"><img src="{asset_path}images/watch-events.png" alt="Apple Watch events" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--phone"><img src="{asset_path}images/phone-analytics.png" alt="iPhone analytics" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--phone"><img src="{asset_path}images/phone-game-detail.png" alt="iPhone game detail" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--phone"><img src="{asset_path}images/phone-settings.png" alt="iPhone settings" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--phone"><img src="{asset_path}images/phone-live-session.png" alt="iPhone live session" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--phone"><img src="{asset_path}images/phone-session-header.png" alt="iPhone session header" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--phone"><img src="{asset_path}images/phone-live-meter.png" alt="iPhone live meter" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--phone"><img src="{asset_path}images/phone-motion-stats.png" alt="iPhone motion stats" class="screenshot-img"></div>
                        <div class="screenshot-item screenshot-item--phone"><img src="{asset_path}images/phone-shift-list.png" alt="iPhone shift list" class="screenshot-img"></div>
                    </div>

                    <button class="screenshots__arrow screenshots__arrow--next" aria-label="Next screenshot">
                        <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
                    </button>
                </div>
            </div>
        </section>

        <!-- Testimonials Section (hidden until launch) -->
        <section class="testimonials testimonials--hidden" id="testimonials">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['testimonials']['title']}</h2>
                    <p class="section-subtitle">{t['testimonials']['subtitle']}</p>
                </div>

                <div class="testimonials__grid">
                    <div class="testimonial-card" data-aos="fade-up">
                        <div class="testimonial-card__stars">
                            {five_stars}
                        </div>
                        <p class="testimonial-card__quote">{t['testimonials']['review1']['quote']}</p>
                        <span class="testimonial-card__author">{t['testimonials']['review1']['author']}</span>
                    </div>

                    <div class="testimonial-card" data-aos="fade-up" data-aos-delay="100">
                        <div class="testimonial-card__stars">
                            {five_stars}
                        </div>
                        <p class="testimonial-card__quote">{t['testimonials']['review2']['quote']}</p>
                        <span class="testimonial-card__author">{t['testimonials']['review2']['author']}</span>
                    </div>

                    <div class="testimonial-card" data-aos="fade-up" data-aos-delay="200">
                        <div class="testimonial-card__stars">
                            {five_stars}
                        </div>
                        <p class="testimonial-card__quote">{t['testimonials']['review3']['quote']}</p>
                        <span class="testimonial-card__author">{t['testimonials']['review3']['author']}</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- FAQ Section -->
        <section class="faq" id="faq">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['faq']['title']}</h2>
                    <p class="section-subtitle">{t['faq']['subtitle']}</p>
                </div>

                <div class="faq__list">
{faq_html}
                </div>
            </div>
        </section>

        <!-- Download CTA Section -->
        <section class="download" id="download">
            <div class="container">
                <div class="download__content" data-aos="fade-up">
                    <div class="download__icon">
                        <img src="{asset_path}images/app-icon.png" alt="{t['appName']} app icon" class="download__icon-img">
                    </div>
                    <h2 class="download__title">{t['download']['title']}</h2>
                    <p class="download__description">{t['download']['description']}</p>
                    <a href="https://apps.apple.com/us/app/ice-time-track/id6758258172?ct=WEB" class="launch-btn launch-btn--lg" id="download-cta" target="_blank" rel="noopener">{t['download']['preOrder']}</a>
                    <img src="{asset_path}assets/app-store-badges/app-store-badge-{lang['code']}.svg" alt="App Store" class="app-store-badge app-store-badge--static" onerror="this.src='{asset_path}assets/app-store-badges/app-store-badge-en.svg'">
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer__content">
                <span class="footer__name">{t['appName']}</span>
                <div class="footer__links">
                    <a href="/privacy-policy.html" class="footer__link">{t['footer']['privacy']}</a>
                    <a href="#" class="footer__link">{t['footer']['terms']}</a>
                    <a href="mailto:support@masawata.net" class="footer__link">{t['footer']['support']}</a>
                </div>
                <p class="footer__copyright">{t['footer']['copyright']}</p>
            </div>
        </div>
    </footer>

    <script src="{asset_path}js/main.js"></script>
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
    print('Building localized HTML files for IceTimeTrack...\n')

    for lang in LANGUAGES:
        translations = load_translation(lang['code'])
        html = generate_html(lang, translations)

        if lang['dir']:
            output_dir = os.path.join(SCRIPT_DIR, lang['dir'])
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = SCRIPT_DIR

        filepath = os.path.join(output_dir, 'index.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        dir_display = f"{lang['dir']}/" if lang['dir'] else ''
        print(f"  Created: {dir_display}index.html ({lang['name']})")

    sitemap = generate_sitemap()
    sitemap_path = os.path.join(SCRIPT_DIR, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print('\n  Updated: sitemap.xml')

    print(f'\nBuild complete! Generated {len(LANGUAGES)} localized pages.')


if __name__ == '__main__':
    build()
