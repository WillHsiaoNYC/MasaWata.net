/**
 * Ice Time Track - Main JavaScript
 * Handles interactions, animations, and UI components
 */
(function () {
    'use strict';

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

    var cdSection = document.getElementById('countdown');
    var cdDays = document.getElementById('cd-days');
    var cdHours = document.getElementById('cd-hours');
    var cdMinutes = document.getElementById('cd-minutes');
    var cdSeconds = document.getElementById('cd-seconds');
    var heroBtn = document.getElementById('hero-download');
    var downloadBtn = document.getElementById('download-cta');
    var navCta = document.getElementById('nav-cta');

    // Show testimonials after Feb 14, 2026
    var TESTIMONIALS_DATE = new Date('2026-02-14T00:00:00-08:00');
    var testimonials = document.getElementById('testimonials');
    if (testimonials && new Date() >= TESTIMONIALS_DATE) {
        testimonials.classList.remove('testimonials--hidden');
    }

    function switchToDownload() {
        if (cdSection) cdSection.classList.add('countdown--hidden');
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

    function updateCountdown() {
        var now = new Date();
        var diff = LAUNCH_DATE - now;

        if (diff <= 0) {
            switchToDownload();
            return false;
        }

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
