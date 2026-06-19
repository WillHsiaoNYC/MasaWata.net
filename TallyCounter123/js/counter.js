// Tally Counter 123 — hero "123" count-up + gentle scroll reveals.
(function () {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── Count-up for the "123" in the hero title ──
  const el = document.getElementById('counter');
  if (el) {
    const target = parseInt(el.dataset.target || el.textContent, 10);
    if (Number.isFinite(target) && target > 0) {
      if (reduced) {
        el.textContent = String(target);
      } else {
        const duration = 1200;
        const easeOutQuart = (t) => 1 - Math.pow(1 - t, 4);
        let start = null;
        el.textContent = '0';
        const tick = (now) => {
          if (start === null) start = now;
          const t = Math.min(1, (now - start) / duration);
          el.textContent = String(Math.floor(easeOutQuart(t) * target));
          if (t < 1) requestAnimationFrame(tick);
          else el.textContent = String(target);
        };
        requestAnimationFrame(() => requestAnimationFrame(tick));
      }
    }
  }

  // ── Scroll reveals ──
  const items = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  if (!items.length) return;
  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach((n) => n.classList.add('in'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.16, rootMargin: '0px 0px -8% 0px' });
  items.forEach((n) => io.observe(n));
})();
