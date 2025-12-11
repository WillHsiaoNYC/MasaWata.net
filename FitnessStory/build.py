#!/usr/bin/env python3
"""
Build script to generate localized HTML files for SEO
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

BASE_URL = 'https://masawata.net/FitnessStory'

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
    <meta name="keywords" content="fitness, workout, Apple Health, tracking, personal records, exercise, health, running, cycling, data visualization, iOS app">
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
    <meta property="og:image" content="{BASE_URL}/images/Fitness%20Story.png">
    <meta property="og:site_name" content="{t['appName']}">
    <meta property="og:locale" content="{og_locale}">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{t['meta']['title']}">
    <meta name="twitter:description" content="{t['meta']['description']}">
    <meta name="twitter:image" content="{BASE_URL}/images/Fitness%20Story.png">

    <!-- App Store Smart Banner -->
    <meta name="apple-itunes-app" content="app-id=6748090363">

    <!-- Favicon -->
    <link rel="icon" type="image/png" href="{asset_path}images/Fitness%20Story.png">
    <link rel="apple-touch-icon" href="{asset_path}images/Fitness%20Story.png">

    <!-- Stylesheets -->
    <link rel="stylesheet" href="{asset_path}css/style.css">

    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "{t['appName']}",
        "operatingSystem": "iOS",
        "applicationCategory": "HealthApplication",
        "offers": {{
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        }},
        "aggregateRating": {{
            "@type": "AggregateRating",
            "ratingValue": "5.0",
            "ratingCount": "23"
        }},
        "description": "{t['meta']['description']}",
        "screenshot": "{BASE_URL}/images/iphone/dashboard.png",
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
                <img src="{asset_path}images/Fitness%20Story.png" alt="Fitness Story" class="nav__logo-img">
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
                    <a href="#testimonials" class="nav__link">{t['nav']['testimonials']}</a>
                </li>
                <li class="nav__item">
                    <a href="#download" class="nav__link">{t['nav']['download']}</a>
                </li>
            </ul>

            <!-- Language Selector -->
            <div class="language-selector">
                <button class="language-btn" id="language-btn" aria-label="Select Language">
                    <svg class="language-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="2" y1="12" x2="22" y2="12"></line>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                    </svg>
                    <span id="current-lang">{lang['code'].upper()[:2]}</span>
                    <svg class="chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                </button>
                <div class="language-dropdown" id="language-dropdown">
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
                    <img src="{asset_path}images/Fitness%20Story.png" alt="Fitness Story App Icon" class="hero__icon">
                    <h1 class="hero__title">{t['hero']['title']}</h1>
                    <p class="hero__description">{t['hero']['description']}</p>
                    <a href="https://apps.apple.com/us/app/fitness-story/id6748090363" class="hero__download" target="_blank" rel="noopener">
                        <img src="{asset_path}assets/app-store-badges/app-store-badge-{lang['code']}.svg" alt="Download on the App Store" class="app-store-badge" onerror="this.src='{asset_path}assets/app-store-badges/app-store-badge-en.svg'">
                    </a>
                    <div class="hero__rating">
                        <div class="stars">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        </div>
                        <span class="rating-text">{t['hero']['rating']}</span>
                    </div>
                </div>
                <div class="hero__device">
                    <div class="device-frame">
                        <img src="{asset_path}images/iphone/dashboard.png" alt="Fitness Story Dashboard" class="device-screen">
                    </div>
                </div>
            </div>
            <div class="hero__gradient"></div>
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
                        <div class="feature-card__icon feature-card__icon--blue">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                            </svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['storyline']['title']}</h3>
                        <p class="feature-card__description">{t['features']['storyline']['description']}</p>
                        <div class="feature-card__image">
                            <img src="{asset_path}images/iphone/fitness%20storyline.png" alt="{t['features']['storyline']['title']}" loading="lazy">
                        </div>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="100">
                        <div class="feature-card__icon feature-card__icon--green">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['dashboard']['title']}</h3>
                        <p class="feature-card__description">{t['features']['dashboard']['description']}</p>
                        <div class="feature-card__image">
                            <img src="{asset_path}images/iphone/dashboard.png" alt="{t['features']['dashboard']['title']}" loading="lazy">
                        </div>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="200">
                        <div class="feature-card__icon feature-card__icon--yellow">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="20" x2="18" y2="10"></line>
                                <line x1="12" y1="20" x2="12" y2="4"></line>
                                <line x1="6" y1="20" x2="6" y2="14"></line>
                            </svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['analytics']['title']}</h3>
                        <p class="feature-card__description">{t['features']['analytics']['description']}</p>
                        <div class="feature-card__image">
                            <img src="{asset_path}images/iphone/workout%20analysis.png" alt="{t['features']['analytics']['title']}" loading="lazy">
                        </div>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="300">
                        <div class="feature-card__icon feature-card__icon--red">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M6 9H4.5a2.5 2.5 0 010-5C7 4 7 8 7 8M18 9h1.5a2.5 2.5 0 000-5C17 4 17 8 17 8"/>
                                <path d="M4 22h16"/>
                                <path d="M10 22V8h4v14"/>
                                <path d="M8 6V4h8v2"/>
                            </svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['records']['title']}</h3>
                        <p class="feature-card__description">{t['features']['records']['description']}</p>
                        <div class="feature-card__image">
                            <img src="{asset_path}images/iphone/Personal%20records.png" alt="{t['features']['records']['title']}" loading="lazy">
                        </div>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="400">
                        <div class="feature-card__icon feature-card__icon--blue">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/>
                                <circle cx="12" cy="10" r="3"/>
                            </svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['locations']['title']}</h3>
                        <p class="feature-card__description">{t['features']['locations']['description']}</p>
                        <div class="feature-card__image">
                            <img src="{asset_path}images/iphone/My%20fitness%20map.png" alt="{t['features']['locations']['title']}" loading="lazy">
                        </div>
                    </div>

                    <div class="feature-card" data-aos="fade-up" data-aos-delay="500">
                        <div class="feature-card__icon feature-card__icon--red">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
                            </svg>
                        </div>
                        <h3 class="feature-card__title">{t['features']['favorites']['title']}</h3>
                        <p class="feature-card__description">{t['features']['favorites']['description']}</p>
                        <div class="feature-card__image">
                            <img src="{asset_path}images/iphone/my%20favorites.png" alt="{t['features']['favorites']['title']}" loading="lazy">
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Screenshots Section -->
        <section class="screenshots" id="screenshots">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['screenshots']['title']}</h2>
                    <p class="section-subtitle">{t['screenshots']['subtitle']}</p>
                </div>

                <div class="screenshots__gallery">
                    <div class="screenshots__track" id="screenshots-track">
                        <div class="screenshot-item"><img src="{asset_path}images/iphone/dashboard.png" alt="Dashboard" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/iphone/fitness%20storyline.png" alt="Fitness Storyline" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/iphone/workout%20analysis.png" alt="Workout Analysis" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/iphone/Personal%20records.png" alt="Personal Records" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/iphone/My%20fitness%20map.png" alt="My Fitness Map" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/iphone/my%20favorites.png" alt="My Favorites" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/iphone/combined%20metrics%20analysis.png" alt="Combined Metrics" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/iphone/daily%20summary%20and%20benchmark.png" alt="Daily Summary" loading="lazy"></div>
                        <div class="screenshot-item"><img src="{asset_path}images/iphone/overall%20steps%20analysis%20and%20personal%20record.png" alt="Steps Analysis" loading="lazy"></div>
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

        <!-- Testimonials Section -->
        <section class="testimonials" id="testimonials">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">{t['testimonials']['title']}</h2>
                    <p class="section-subtitle">{t['testimonials']['subtitle']}</p>
                </div>

                <div class="testimonials__grid">
                    <div class="testimonial-card" data-aos="fade-up">
                        <div class="testimonial-card__stars">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        </div>
                        <p class="testimonial-card__quote">{t['testimonials']['review1']['quote']}</p>
                        <p class="testimonial-card__author">— Antcido</p>
                    </div>

                    <div class="testimonial-card" data-aos="fade-up" data-aos-delay="100">
                        <div class="testimonial-card__stars">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        </div>
                        <p class="testimonial-card__quote">{t['testimonials']['review2']['quote']}</p>
                        <p class="testimonial-card__author">— Sigmasigmarizz</p>
                    </div>

                    <div class="testimonial-card" data-aos="fade-up" data-aos-delay="200">
                        <div class="testimonial-card__stars">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                        </div>
                        <p class="testimonial-card__quote">{t['testimonials']['review3']['quote']}</p>
                        <p class="testimonial-card__author">— Cleverc77</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Download Section -->
        <section class="download" id="download">
            <div class="container">
                <div class="download__content">
                    <img src="{asset_path}images/Fitness%20Story.png" alt="Fitness Story" class="download__icon">
                    <h2 class="download__title">{t['download']['title']}</h2>
                    <p class="download__description">{t['download']['description']}</p>
                    <a href="https://apps.apple.com/us/app/fitness-story/id6748090363" class="download__button" target="_blank" rel="noopener">
                        <img src="{asset_path}assets/app-store-badges/app-store-badge-{lang['code']}.svg" alt="Download on the App Store" class="app-store-badge" onerror="this.src='{asset_path}assets/app-store-badges/app-store-badge-en.svg'">
                    </a>
                    <div class="download__platforms">
                        <span class="platform-badge">{t['download']['platforms']}</span>
                    </div>
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
                    <img src="{asset_path}images/Fitness%20Story.png" alt="Fitness Story" class="footer__logo">
                    <span class="footer__name">{t['appName']}</span>
                </div>
                <div class="footer__links">
                    <a href="https://apps.apple.com/us/app/fitness-story/id6748090363" target="_blank" rel="noopener">{t['footer']['appStore']}</a>
                    <a href="https://masawata.net/privacy-policy.html">{t['footer']['privacy']}</a>
                    <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/" target="_blank" rel="noopener">{t['footer']['terms']}</a>
                </div>
                <p class="footer__copyright">{t['footer']['copyright']}</p>
            </div>
        </div>
    </footer>

    <!-- Scripts -->
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
    print('Building localized HTML files for SEO...\n')

    for lang in LANGUAGES:
        translations = load_translation(lang['code'])
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

    # Generate sitemap
    sitemap = generate_sitemap()
    sitemap_path = os.path.join(SCRIPT_DIR, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print('\n  Updated: sitemap.xml')

    print(f'\nBuild complete! Generated {len(LANGUAGES)} localized pages.')


if __name__ == '__main__':
    build()
