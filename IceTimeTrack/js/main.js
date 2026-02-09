/**
 * Ice Time Track - Main JavaScript
 * Handles interactions, animations, and UI components
 */
(function () {
    'use strict';

    // ===== Locale Detection & Persistence =====
    const SUPPORTED_LOCALES = ['en', 'cs', 'da', 'de', 'es', 'fi', 'fr', 'hu', 'it', 'ja', 'ko', 'nb', 'ru', 'sk', 'sv', 'zh-Hans', 'zh-Hant'];
    const LOCALE_STORAGE_KEY = 'preferred-locale';
    const BASE_PATH = '/IceTimeTrack';

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
        if (SUPPORTED_LOCALES.includes(userLang)) {
            return userLang;
        }
        const baseLang = userLang.split('-')[0];
        if (SUPPORTED_LOCALES.includes(baseLang)) {
            return baseLang;
        }
        // Special handling for Chinese variants
        if (userLang.startsWith('zh')) {
            return userLang.includes('TW') || userLang.includes('HK') ? 'zh-Hant' : 'zh-Hans';
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

        // If already on a specific language page, save that preference
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

    /* ========================================
     * 7. JS loaded marker
     * ======================================== */
    document.documentElement.classList.add('js-loaded');

    /* ========================================
     * 1. Header scroll effect
     * ======================================== */
    const header = document.getElementById('header');

    function handleScroll() {
        if (!header) return;
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleScroll, { passive: true });

    /* ========================================
     * 2. Mobile menu toggle
     * ======================================== */
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            // Lock or unlock body scroll when menu is open
            document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
        });

        // Close menu when any nav link is clicked
        const navLinks = document.querySelectorAll('.nav__link');
        navLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    /* ========================================
     * 2b. Language Selector
     * ======================================== */
    const languageSelectors = document.querySelectorAll('.language-selector');

    languageSelectors.forEach(function (selector) {
        const btn = selector.querySelector('.language-btn');
        if (!btn) return;

        btn.addEventListener('click', function (e) {
            e.stopPropagation();
            languageSelectors.forEach(function (s) {
                if (s !== selector) s.classList.remove('active');
            });
            selector.classList.toggle('active');
        });

        selector.querySelectorAll('.language-dropdown a').forEach(function (link) {
            link.addEventListener('click', function (e) {
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

    document.addEventListener('click', function (e) {
        languageSelectors.forEach(function (selector) {
            if (!selector.contains(e.target)) {
                selector.classList.remove('active');
            }
        });
    });

    /* ========================================
     * 3. FAQ accordion (one-at-a-time)
     * ======================================== */
    const faqItems = document.querySelectorAll('.faq__item');

    faqItems.forEach(function (item) {
        const question = item.querySelector('.faq__question');
        if (!question) return;

        question.addEventListener('click', function () {
            const isActive = item.classList.contains('active');

            // Close all other FAQ items
            faqItems.forEach(function (otherItem) {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                    const otherBtn = otherItem.querySelector('.faq__question');
                    if (otherBtn) {
                        otherBtn.setAttribute('aria-expanded', 'false');
                    }
                }
            });

            // Toggle current item
            item.classList.toggle('active');
            question.setAttribute('aria-expanded', isActive ? 'false' : 'true');
        });
    });

    /* ========================================
     * 4. Screenshots gallery navigation
     * ======================================== */
    const screenshotsTrack = document.querySelector('.screenshots__track');
    const prevArrow = document.querySelector('.screenshots__arrow--prev');
    const nextArrow = document.querySelector('.screenshots__arrow--next');

    if (screenshotsTrack && prevArrow && nextArrow) {
        prevArrow.addEventListener('click', function () {
            screenshotsTrack.scrollBy({ left: -280, behavior: 'smooth' });
        });

        nextArrow.addEventListener('click', function () {
            screenshotsTrack.scrollBy({ left: 280, behavior: 'smooth' });
        });
    }

    /* ========================================
     * 5. Smooth scroll for anchor links
     * ======================================== */
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            const href = link.getAttribute('href');
            // Skip empty hashes or "#" only
            if (!href || href === '#') return;

            const target = document.querySelector(href);
            if (!target) return;

            e.preventDefault();

            // Calculate position with header offset
            const headerHeight = header ? header.offsetHeight : 0;
            const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        });
    });

    /* ========================================
     * 6. Launch countdown + pre-order/download toggle
     * ======================================== */
    var LAUNCH_DATE = new Date('2026-02-14T00:00:00-08:00'); // Pacific time
    var PROMO_END_DATE = new Date('2026-02-28T23:59:59-08:00'); // Promo ends

    var cdSection = document.getElementById('countdown');
    var cdDays = document.getElementById('cd-days');
    var cdHours = document.getElementById('cd-hours');
    var cdMinutes = document.getElementById('cd-minutes');
    var cdSeconds = document.getElementById('cd-seconds');
    var cdTitle = document.getElementById('cd-title');
    var cdDate = document.getElementById('cd-date');
    var cdPromo = document.getElementById('cd-promo');
    var cdPromoSub = document.getElementById('cd-promo-sub');
    var cdClaim = document.getElementById('cd-claim');
    var heroBtn = document.getElementById('hero-download');
    var downloadBtn = document.getElementById('download-cta');
    var navCta = document.getElementById('nav-cta');

    // Show testimonials after Feb 14, 2026
    var TESTIMONIALS_DATE = new Date('2026-02-14T00:00:00-08:00');
    var testimonials = document.getElementById('testimonials');
    if (testimonials && new Date() >= TESTIMONIALS_DATE) {
        testimonials.classList.remove('testimonials--hidden');
    }

    var promoMode = false;

    function enableDownloadButtons() {
        if (heroBtn) heroBtn.textContent = 'Download Now';
        if (downloadBtn) downloadBtn.textContent = 'Download Now';
        if (navCta) navCta.textContent = 'Download';

        // Make App Store badges clickable
        var badges = document.querySelectorAll('.app-store-badge--static');
        badges.forEach(function (badge) {
            badge.style.pointerEvents = 'auto';
            badge.style.opacity = '1';
            badge.style.cursor = 'pointer';
            badge.addEventListener('click', function () {
                window.open('https://apps.apple.com/us/app/ice-time-track/id6758258172?ct=WEB', '_blank');
            });
        });
    }

    function switchToPromo() {
        promoMode = true;
        enableDownloadButtons();
        if (cdTitle) cdTitle.textContent = 'Launch Special';
        if (cdDate) cdDate.textContent = 'Offer ends February 28, 2026';
        if (cdPromo) cdPromo.classList.remove('countdown--hidden');
        if (cdPromoSub) cdPromoSub.classList.remove('countdown--hidden');
        if (cdClaim) cdClaim.classList.remove('countdown--hidden');
    }

    function switchToDownload() {
        if (cdSection) cdSection.classList.add('countdown--hidden');
        enableDownloadButtons();
    }

    function updateTimer(targetDate) {
        var now = new Date();
        var diff = targetDate - now;

        if (diff <= 0) return false;

        var days = Math.floor(diff / (1000 * 60 * 60 * 24));
        var hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((diff % (1000 * 60)) / 1000);

        if (cdDays) cdDays.textContent = String(days).padStart(2, '0');
        if (cdHours) cdHours.textContent = String(hours).padStart(2, '0');
        if (cdMinutes) cdMinutes.textContent = String(minutes).padStart(2, '0');
        if (cdSeconds) cdSeconds.textContent = String(seconds).padStart(2, '0');

        return true;
    }

    function updateCountdown() {
        var now = new Date();

        if (now < LAUNCH_DATE) {
            // Before launch: count down to launch
            return updateTimer(LAUNCH_DATE);
        } else if (now < PROMO_END_DATE) {
            // After launch, before promo ends: show promo countdown
            if (!promoMode) switchToPromo();
            return updateTimer(PROMO_END_DATE);
        } else {
            // After promo ends: hide countdown
            switchToDownload();
            return false;
        }
    }

    if (updateCountdown()) {
        var countdownInterval = setInterval(function () {
            if (!updateCountdown()) {
                clearInterval(countdownInterval);
            }
        }, 1000);
    }

    /* ========================================
     * 7. Scroll animations (AOS-like)
     * ======================================== */
    function initAOS() {
        const aosElements = document.querySelectorAll('[data-aos]');
        if (aosElements.length === 0) return;

        // Check for IntersectionObserver support
        if (!('IntersectionObserver' in window)) {
            // Fallback: make all elements visible immediately
            aosElements.forEach(function (el) {
                el.classList.add('aos-animate');
            });
            return;
        }

        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    // Apply delay if specified via data-aos-delay
                    const delay = entry.target.getAttribute('data-aos-delay');
                    if (delay) {
                        setTimeout(function () {
                            entry.target.classList.add('aos-animate');
                        }, parseInt(delay, 10));
                    } else {
                        entry.target.classList.add('aos-animate');
                    }
                    // Stop observing once animated
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });

        aosElements.forEach(function (el) {
            observer.observe(el);
        });
    }

    // Initialize AOS after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAOS);
    } else {
        // DOM already loaded
        initAOS();
    }

})();
