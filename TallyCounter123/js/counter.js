// One-time count-up animation for the "123" in the hero title.
(function () {
  const el = document.getElementById('counter');
  if (!el) return;

  const target = parseInt(el.dataset.target || el.textContent, 10);
  if (!Number.isFinite(target) || target <= 0) return;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) {
    el.textContent = String(target);
    return;
  }

  const duration = 1400;
  el.textContent = '0';

  const easeOutQuart = (t) => 1 - Math.pow(1 - t, 4);
  let start = null;

  function tick(now) {
    if (start === null) start = now;
    const t = Math.min(1, (now - start) / duration);
    el.textContent = String(Math.floor(easeOutQuart(t) * target));
    if (t < 1) {
      requestAnimationFrame(tick);
    } else {
      el.textContent = String(target);
    }
  }

  // Defer to after first paint so the rest of the hero renders first.
  requestAnimationFrame(() => requestAnimationFrame(tick));
})();
