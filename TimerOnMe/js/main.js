/**
 * Timer on Me - Main JavaScript
 * Handles interactions, animations, and UI components
 */

(function () {
    'use strict';

    // ===== Locale Detection & Persistence =====
    const SUPPORTED_LOCALES = ['en', 'cs', 'da', 'de', 'es', 'fi', 'fr', 'hi', 'hu', 'id', 'it', 'ja', 'ko', 'nb', 'pt-BR', 'ru', 'sk', 'sv', 'vi', 'zh-Hans', 'zh-Hant'];
    const LOCALE_STORAGE_KEY = 'preferred-locale';
    const BASE_PATH = '/TimerOnMe';

    function getCurrentLocale() {
        const path = window.location.pathname;
        for (const locale of SUPPORTED_LOCALES) {
            if (path.includes('/' + locale + '/') || path.endsWith('/' + locale)) {
                return locale;
            }
        }
        return 'en';
    }

    function detectUserLocale() {
        const userLang = navigator.language || navigator.userLanguage;
        // Check full locale first
        if (SUPPORTED_LOCALES.includes(userLang)) {
            return userLang;
        }
        // Check base language
        const baseLang = userLang.split('-')[0];
        if (SUPPORTED_LOCALES.includes(baseLang)) {
            return baseLang;
        }
        // Special handling for Chinese variants
        if (userLang.startsWith('zh')) {
            return userLang.includes('TW') || userLang.includes('HK') ? 'zh-Hant' : 'zh-Hans';
        }
        // Special handling for Portuguese
        if (userLang.startsWith('pt')) {
            return 'pt-BR';
        }
        // Special handling for Norwegian
        if (userLang.startsWith('nb') || userLang.startsWith('no')) {
            return 'nb';
        }
        return 'en';
    }

    function redirectToLocale(locale) {
        if (locale === 'en') {
            window.location.href = BASE_PATH + '/';
        } else {
            window.location.href = BASE_PATH + '/' + locale + '/';
        }
    }

    function initLocaleRedirect() {
        const currentLocale = getCurrentLocale();
        const savedLocale = localStorage.getItem(LOCALE_STORAGE_KEY);
        const path = window.location.pathname;

        // Enforce trailing slash for locale pages
        if (currentLocale !== 'en' && !path.endsWith('/')) {
            window.location.replace(path + '/');
            return;
        }

        // Prevent redirect if we are already on a specific language page
        if (currentLocale !== 'en') {
            if (savedLocale !== currentLocale) {
                localStorage.setItem(LOCALE_STORAGE_KEY, currentLocale);
            }
            return;
        }

        if (savedLocale) {
            if (savedLocale !== currentLocale) {
                redirectToLocale(savedLocale);
                return;
            }
        } else {
            const detectedLocale = detectUserLocale();
            if (detectedLocale !== currentLocale) {
                localStorage.setItem(LOCALE_STORAGE_KEY, detectedLocale);
                redirectToLocale(detectedLocale);
                return;
            }
            localStorage.setItem(LOCALE_STORAGE_KEY, currentLocale);
        }
    }

    // Run locale detection immediately
    initLocaleRedirect();

    // ===== DOM Elements =====
    const header = document.getElementById('header');
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const screenshotsTrack = document.getElementById('screenshots-track');
    const prevBtn = document.getElementById('screenshots-prev');
    const nextBtn = document.getElementById('screenshots-next');

    // ===== Header Scroll Effect =====
    function handleScroll() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleScroll, { passive: true });

    // ===== Mobile Menu Toggle =====
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
        });

        navMenu.querySelectorAll('.nav__link').forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // ===== Language Selectors =====
    const languageSelectors = document.querySelectorAll('.language-selector');

    languageSelectors.forEach(selector => {
        const btn = selector.querySelector('.language-btn');
        if (!btn) return;

        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            languageSelectors.forEach(s => {
                if (s !== selector) s.classList.remove('active');
            });
            selector.classList.toggle('active');
        });

        selector.querySelectorAll('.language-dropdown a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const href = link.getAttribute('href');
                let locale = 'en';
                for (const loc of SUPPORTED_LOCALES) {
                    if (href.includes('/' + loc + '/') || href === loc + '/') {
                        locale = loc;
                        break;
                    }
                }

                if (href === '../' || href === './') {
                    locale = 'en';
                }

                localStorage.setItem(LOCALE_STORAGE_KEY, locale);
                redirectToLocale(locale);
            });
        });
    });

    document.addEventListener('click', (e) => {
        languageSelectors.forEach(selector => {
            if (!selector.contains(e.target)) {
                selector.classList.remove('active');
            }
        });
    });

    // ===== Screenshots Gallery Navigation =====
    if (screenshotsTrack && prevBtn && nextBtn) {
        const scrollAmount = 250;

        prevBtn.addEventListener('click', () => {
            screenshotsTrack.scrollBy({
                left: -scrollAmount,
                behavior: 'smooth'
            });
        });

        nextBtn.addEventListener('click', () => {
            screenshotsTrack.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
        });
    }

    // ===== Smooth Scroll for Anchor Links =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const headerHeight = header.offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ===== Scroll Animations (AOS-like) =====
    function initScrollAnimations() {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('aos-animate');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('[data-aos]').forEach(el => {
            observer.observe(el);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScrollAnimations);
    } else {
        initScrollAnimations();
    }

    // ===== Lazy Loading for Images =====
    if ('loading' in HTMLImageElement.prototype) {
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            img.src = img.src;
        });
    } else {
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');

        const lazyLoad = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.src;
                    lazyLoad.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => lazyLoad.observe(img));
    }

    // ===== Prevent Flash of Unstyled Content =====
    document.documentElement.classList.add('js-loaded');

})();
