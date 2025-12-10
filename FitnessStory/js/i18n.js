/**
 * Fitness Story - Internationalization (i18n)
 * Handles multi-language support with JSON translation files
 */

(function() {
    'use strict';

    // ===== Configuration =====
    const DEFAULT_LANG = 'en';
    const STORAGE_KEY = 'fitness-story-lang';
    const SUPPORTED_LANGUAGES = {
        'en': 'English',
        'zh-Hans': '简体中文',
        'zh-Hant': '繁體中文',
        'ja': '日本語',
        'ko': '한국어',
        'fr': 'Français',
        'de': 'Deutsch',
        'es': 'Español',
        'pt': 'Português',
        'it': 'Italiano',
        'ru': 'Русский',
        'hi': 'हिन्दी',
        'id': 'Indonesia',
        'vi': 'Tiếng Việt'
    };

    // Language code display names (short form)
    const LANG_CODES = {
        'en': 'EN',
        'zh-Hans': '简',
        'zh-Hant': '繁',
        'ja': 'JA',
        'ko': 'KO',
        'fr': 'FR',
        'de': 'DE',
        'es': 'ES',
        'pt': 'PT',
        'it': 'IT',
        'ru': 'RU',
        'hi': 'HI',
        'id': 'ID',
        'vi': 'VI'
    };

    // Cache for loaded translations
    let translationsCache = {};
    let currentLang = DEFAULT_LANG;

    // ===== Utility Functions =====

    /**
     * Get nested property from object using dot notation
     */
    function getNestedValue(obj, path) {
        return path.split('.').reduce((current, key) => {
            return current && current[key] !== undefined ? current[key] : null;
        }, obj);
    }

    /**
     * Detect user's preferred language from browser or URL
     */
    function detectLanguage() {
        // Check URL parameter first
        const urlParams = new URLSearchParams(window.location.search);
        const urlLang = urlParams.get('lang');
        if (urlLang && SUPPORTED_LANGUAGES[urlLang]) {
            return urlLang;
        }

        // Check localStorage
        const storedLang = localStorage.getItem(STORAGE_KEY);
        if (storedLang && SUPPORTED_LANGUAGES[storedLang]) {
            return storedLang;
        }

        // Check browser language
        const browserLang = navigator.language || navigator.userLanguage;

        // Handle Chinese variants
        if (browserLang.startsWith('zh')) {
            if (browserLang.includes('TW') || browserLang.includes('HK') || browserLang.includes('Hant')) {
                return 'zh-Hant';
            }
            return 'zh-Hans';
        }

        // Check for exact match
        if (SUPPORTED_LANGUAGES[browserLang]) {
            return browserLang;
        }

        // Check for language code without region (e.g., 'en-US' -> 'en')
        const langCode = browserLang.split('-')[0];
        if (SUPPORTED_LANGUAGES[langCode]) {
            return langCode;
        }

        return DEFAULT_LANG;
    }

    /**
     * Load translations from JSON file
     */
    async function loadTranslations(lang) {
        if (translationsCache[lang]) {
            return translationsCache[lang];
        }

        try {
            const response = await fetch(`locales/${lang}.json`);
            if (!response.ok) {
                throw new Error(`Failed to load ${lang}.json`);
            }
            const translations = await response.json();
            translationsCache[lang] = translations;
            return translations;
        } catch (error) {
            console.warn(`Could not load translations for ${lang}, falling back to ${DEFAULT_LANG}`);
            if (lang !== DEFAULT_LANG) {
                return loadTranslations(DEFAULT_LANG);
            }
            return {};
        }
    }

    /**
     * Apply translations to the page
     */
    function applyTranslations(translations) {
        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = getNestedValue(translations, key);

            if (translation) {
                // Handle different element types
                if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
                    element.placeholder = translation;
                } else if (element.tagName === 'IMG') {
                    element.alt = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });

        // Update meta tags
        if (translations.meta) {
            if (translations.meta.title) {
                document.title = translations.meta.title;
                document.querySelector('meta[property="og:title"]')?.setAttribute('content', translations.meta.title);
                document.querySelector('meta[name="twitter:title"]')?.setAttribute('content', translations.meta.title);
            }
            if (translations.meta.description) {
                document.querySelector('meta[name="description"]')?.setAttribute('content', translations.meta.description);
                document.querySelector('meta[property="og:description"]')?.setAttribute('content', translations.meta.description);
                document.querySelector('meta[name="twitter:description"]')?.setAttribute('content', translations.meta.description);
            }
        }

        // Update HTML lang attribute
        document.documentElement.lang = currentLang;
    }

    /**
     * Update App Store badge based on language
     */
    function updateAppStoreBadge(lang) {
        const badges = document.querySelectorAll('.app-store-badge');
        badges.forEach(badge => {
            // Map language codes to App Store badge file names
            const badgeFile = `assets/app-store-badges/app-store-badge-${lang}.svg`;
            badge.src = badgeFile;

            // Fallback to English if locale badge doesn't exist
            badge.onerror = function() {
                this.src = 'assets/app-store-badges/app-store-badge-en.svg';
            };
        });
    }

    /**
     * Update language selector UI
     */
    function updateLanguageSelector(lang) {
        const currentLangSpan = document.getElementById('current-lang');
        if (currentLangSpan) {
            currentLangSpan.textContent = LANG_CODES[lang] || lang.toUpperCase();
        }

        // Update active state in dropdown
        document.querySelectorAll('.language-option').forEach(option => {
            if (option.getAttribute('data-lang') === lang) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    }

    /**
     * Change language
     */
    async function setLanguage(lang) {
        if (!SUPPORTED_LANGUAGES[lang]) {
            console.warn(`Unsupported language: ${lang}`);
            return;
        }

        currentLang = lang;
        localStorage.setItem(STORAGE_KEY, lang);

        // Update URL without reloading
        const url = new URL(window.location);
        url.searchParams.set('lang', lang);
        window.history.replaceState({}, '', url);

        const translations = await loadTranslations(lang);
        applyTranslations(translations);
        updateAppStoreBadge(lang);
        updateLanguageSelector(lang);

        // Close language dropdown
        document.querySelector('.language-selector')?.classList.remove('active');
    }

    /**
     * Initialize i18n
     */
    async function init() {
        // Detect and set initial language
        const detectedLang = detectLanguage();
        currentLang = detectedLang;

        // Load and apply translations
        const translations = await loadTranslations(currentLang);
        applyTranslations(translations);
        updateAppStoreBadge(currentLang);
        updateLanguageSelector(currentLang);

        // Set up language selector click handlers
        document.querySelectorAll('.language-option').forEach(option => {
            option.addEventListener('click', (e) => {
                const lang = e.target.getAttribute('data-lang');
                if (lang) {
                    setLanguage(lang);
                }
            });
        });
    }

    // ===== Public API =====
    window.i18n = {
        setLanguage,
        getCurrentLanguage: () => currentLang,
        getSupportedLanguages: () => ({ ...SUPPORTED_LANGUAGES })
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
