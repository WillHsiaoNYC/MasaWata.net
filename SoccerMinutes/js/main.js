(function () {
    "use strict";

    document.documentElement.classList.add("js");

    const header = document.getElementById("site-header");
    const nav = document.getElementById("nav");
    const toggle = document.getElementById("nav-toggle");
    const links = document.querySelectorAll("#nav-links a");

    function updateHeader() {
        if (header) {
            header.classList.toggle("is-scrolled", window.scrollY > 20);
        }
    }

    function closeNavigation() {
        if (!nav || !toggle) return;
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open navigation");
    }

    if (toggle && nav) {
        toggle.addEventListener("click", function () {
            const willOpen = !nav.classList.contains("is-open");
            nav.classList.toggle("is-open", willOpen);
            toggle.setAttribute("aria-expanded", String(willOpen));
            toggle.setAttribute("aria-label", willOpen ? "Close navigation" : "Open navigation");
        });

        links.forEach(function (link) {
            link.addEventListener("click", closeNavigation);
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeNavigation();
                toggle.focus();
            }
        });
    }

    document.querySelectorAll(".faq__item").forEach(function (item) {
        const question = item.querySelector(".faq__question");
        if (!question) return;

        question.addEventListener("click", function () {
            const isOpen = item.classList.contains("is-open");

            document.querySelectorAll(".faq__item.is-open").forEach(function (openItem) {
                openItem.classList.remove("is-open");
                const openButton = openItem.querySelector(".faq__question");
                if (openButton) openButton.setAttribute("aria-expanded", "false");
            });

            if (!isOpen) {
                item.classList.add("is-open");
                question.setAttribute("aria-expanded", "true");
            }
        });
    });

    const gallery = document.getElementById("gallery");
    const previous = document.getElementById("gallery-prev");
    const next = document.getElementById("gallery-next");

    function moveGallery(direction) {
        if (!gallery) return;
        const card = gallery.querySelector("figure");
        const distance = card ? card.getBoundingClientRect().width + 18 : 348;
        gallery.scrollBy({ left: direction * distance, behavior: "smooth" });
    }

    if (previous) previous.addEventListener("click", function () { moveGallery(-1); });
    if (next) next.addEventListener("click", function () { moveGallery(1); });

    if (gallery) {
        gallery.addEventListener("keydown", function (event) {
            if (event.key === "ArrowLeft") {
                event.preventDefault();
                moveGallery(-1);
            } else if (event.key === "ArrowRight") {
                event.preventDefault();
                moveGallery(1);
            }
        });
    }

    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });
}());
