/**
 * Fitness Story - Main JavaScript
 * Handles interactions, animations, and UI components
 */

(function () {
    'use strict';

    // ===== DOM Elements =====
    const header = document.getElementById('header');
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const languageBtn = document.getElementById('language-btn');
    const languageSelector = languageBtn?.parentElement;
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

        // Close menu when clicking a link
        navMenu.querySelectorAll('.nav__link').forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // ===== Language Selector =====
    if (languageBtn && languageSelector) {
        languageBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            languageSelector.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!languageSelector.contains(e.target)) {
                languageSelector.classList.remove('active');
            }
        });
    }

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

    // Initialize animations after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScrollAnimations);
    } else {
        initScrollAnimations();
    }

    // ===== Lazy Loading for Images =====
    if ('loading' in HTMLImageElement.prototype) {
        // Browser supports native lazy loading
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            img.src = img.src;
        });
    } else {
        // Fallback for browsers that don't support native lazy loading
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

    // ===== Promo Countdown Timer =====
    function initCountdown() {
        const countdownEl = document.getElementById('promo-countdown');
        if (!countdownEl) return;

        const endDate = new Date('2026-01-02T23:59:59').getTime();

        function updateCountdown() {
            const now = new Date().getTime();
            const distance = endDate - now;

            if (distance < 0) {
                // Promo expired
                const banner = document.querySelector('.promo-banner');
                if (banner) banner.style.display = 'none';
                document.body.classList.remove('has-promo-banner');
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            const daysEl = document.getElementById('countdown-days');
            const hoursEl = document.getElementById('countdown-hours');
            const minutesEl = document.getElementById('countdown-minutes');
            const secondsEl = document.getElementById('countdown-seconds');

            if (daysEl) daysEl.textContent = String(days).padStart(2, '0');
            if (hoursEl) hoursEl.textContent = String(hours).padStart(2, '0');
            if (minutesEl) minutesEl.textContent = String(minutes).padStart(2, '0');
            if (secondsEl) secondsEl.textContent = String(seconds).padStart(2, '0');
        }

        // Update immediately and then every second
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }

    // Initialize countdown
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCountdown);
    } else {
        initCountdown();
    }

    // ===== Promo Banner and Header Height Calculation =====
    function updateLayoutMetrics() {
        const banner = document.querySelector('.promo-banner');
        const header = document.querySelector('.header');

        if (banner) {
            const height = banner.offsetHeight;
            document.body.style.setProperty('--promo-banner-height', `${height}px`);
        }

        if (header) {
            const headerRect = header.getBoundingClientRect();
            // This captures the actual bottom position of the header in the viewport
            document.body.style.setProperty('--header-bottom-position', `${headerRect.bottom}px`);
        }
    }

    // Initialize metrics
    updateLayoutMetrics();

    // Update on resize and scroll (since header might move or banner might change)
    window.addEventListener('resize', updateLayoutMetrics, { passive: true });
    window.addEventListener('scroll', updateLayoutMetrics, { passive: true });

    // Update again after delay to ensure fonts/layout settled
    setTimeout(updateLayoutMetrics, 100);
    setTimeout(updateLayoutMetrics, 500);

})();
