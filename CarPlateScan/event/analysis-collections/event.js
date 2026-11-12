/* Only approved event translations; no cookies, storage, tracking or auto-open. */
(() => {
  const aliases = {en: 'en-US', ar: 'ar-SA', de: 'de-DE', nl: 'nl-NL', bn: 'bn-BD',
    gu: 'gu-IN', kn: 'kn-IN', ml: 'ml-IN', mr: 'mr-IN', or: 'or-IN', pa: 'pa-IN',
    sl: 'sl-SI', ta: 'ta-IN', te: 'te-IN', ur: 'ur-PK', nb: 'no', iw: 'he'};

  function resolveLocale(tag, supported) {
    if (typeof tag !== 'string') return null;
    const normalized = tag.replace(/_/g, '-').toLowerCase();
    const exact = supported.find(code => code.toLowerCase() === normalized);
    if (exact) return exact;
    if (/^zh-(hant|tw|hk|mo)(-|$)/.test(normalized)) return 'zh-Hant';
    if (normalized.startsWith('zh')) return null;
    const base = normalized.split('-')[0];
    if (['ja', 'ko', 'th'].includes(base)) return null;
    const language = supported.find(code => code.toLowerCase() === base);
    if (language) return language;
    // One approved variant for these languages; no inferred French, Spanish
    // or Portuguese region when the browser supplies an ambiguous generic tag.
    return aliases[base] && supported.includes(aliases[base]) ? aliases[base] : null;
  }

  function chooseLocale(requested, preferred, supported) {
    if (requested !== null) return resolveLocale(requested, supported) || 'en-US';
    for (const language of preferred) {
      const match = resolveLocale(language, supported);
      if (match) return match;
    }
    return 'en-US';
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {resolveLocale, chooseLocale};
  }
  if (typeof document === 'undefined') return;

  async function start() {
    const response = await fetch('localizations.json');
    if (!response.ok) return;
    const data = await response.json();
    const supported = Object.keys(data.locales);
    const select = document.getElementById('language');
    select.replaceChildren(...supported.map(code => {
      const option = document.createElement('option');
      option.value = code;
      try { option.textContent = new Intl.DisplayNames([code], {type: 'language'}).of(code); }
      catch { option.textContent = data.locales[code].label; }
      return option;
    }));
    function show(code) {
      const copy = data.locales[code];
      document.documentElement.lang = code;
      document.documentElement.dir = ['ar-SA', 'he', 'ur-PK'].includes(code) ? 'rtl' : 'ltr';
      document.title = copy.name + ' — Car Plate Scan';
      for (const [id, field] of Object.entries({title:'name',short:'short_description',long:'long_description',
        'language-label':'language','app-store':'appStore',requires:'requires',interface:'interface'})) {
        document.getElementById(id).textContent = copy[field];
      }
      document.querySelector('meta[name="description"]').content = copy.short_description;
      const format = new Intl.DateTimeFormat(code, {year:'numeric',month:'long',day:'numeric',
        hour:'numeric',minute:'2-digit',timeZone:'America/New_York',timeZoneName:'short'});
      for (const key of ['start', 'end']) document.getElementById(key).textContent = format.format(new Date(data[key]));
      select.value = code;
    }
    show(chooseLocale(new URL(location.href).searchParams.get('lang'),
      navigator.languages || [navigator.language], supported));
    select.disabled = false;
    select.addEventListener('change', () => {
      show(select.value);
      const url = new URL(location.href);
      url.searchParams.set('lang', select.value);
      history.replaceState(null, '', url);
    });
  }
  // The static English fallback stays usable if translation loading fails.
  start().catch(() => {});
})();
