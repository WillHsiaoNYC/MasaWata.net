/* Event language selection is local to this page; no cookies or storage. */
(() => {
  const english = {};
  document.querySelectorAll('[data-copy]').forEach(node => {
    english[node.dataset.copy] = node.textContent;
  });
  english.language = 'Language';
  english.artAlt = document.querySelector('[data-copy-alt="artAlt"]').alt;
  const traditionalChinese = {
    skip: '跳至主要內容', language: '語言', badge: '上市首週挑戰',
    title: '日常車牌收藏', intro: '三面路過車牌，收藏日常片刻。',
    description: '站在安全的人行道上，掃描三輛路過車輛的車牌，確認辨識結果後儲存，建立你的日常收藏。',
    dates: '2026 年 11 月 28 日至 12 月 5 日 · 上午 9 點（美東標準時間，UTC−5）',
    appStore: '前往 App Store', about: '認識 Car Plate Scan',
    artAlt: '插畫：一位站在人行道上的使用者拍攝路過的藍綠色車輛。',
    caption: '以插畫記錄日常片刻。你的收藏，留給自己回味。',
    stepsTitle: '幾筆值得收藏的日常',
    stepOneTitle: '找個安全的位置',
    stepOne: '站在安全的公共人行道上，避開車流與出入口，將手機朝向路過的車輛。',
    stepTwoTitle: '儲存三面清晰車牌',
    stepTwo: '使用即時掃描，逐筆確認辨識結果，必要時修正文字，再儲存紀錄。',
    stepThreeTitle: '回顧你的收藏',
    stepThree: '開啟「車牌」回顧儲存的照片，並選一筆加入最愛。',
    note: '在活動週內完成三筆車牌紀錄，建立個人收藏。車牌格式、距離、車速和影像狀況都會影響辨識結果。本活動沒有獎品或排名。',
    safety: '請留在人行道上，尊重私人土地及他人隱私，切勿在駕駛時操作本 App。',
    privacy: '隱私與資料處理', terms: '使用條款'
  };
  const url = new URL(window.location.href);
  const requested = url.searchParams.get('lang');
  const languages = navigator.languages || [navigator.language || 'en'];
  const preferredLanguage = languages.find(language => /^(en(-|$)|zh-(hant|tw|hk|mo)(-|$))/i.test(language)) || 'en';
  const prefersTraditional = /^zh-/i.test(preferredLanguage);
  const language = requested === 'zh-Hant' ? 'zh-Hant' :
    (requested === 'en' || requested === 'en-US') ? 'en' : prefersTraditional ? 'zh-Hant' : 'en';
  const copy = language === 'zh-Hant' ? traditionalChinese : english;
  document.documentElement.lang = language === 'zh-Hant' ? 'zh-Hant' : 'en-US';
  document.title = copy.title + ' — Car Plate Scan';
  document.querySelectorAll('[data-copy]').forEach(node => {
    node.textContent = copy[node.dataset.copy];
  });
  document.querySelectorAll('[data-copy-alt]').forEach(node => {
    node.alt = copy[node.dataset.copyAlt];
  });
  document.querySelectorAll('[data-copy-aria]').forEach(node => {
    node.setAttribute('aria-label', copy[node.dataset.copyAria]);
  });
  document.querySelectorAll('[data-language]').forEach(node => {
    if (node.dataset.language === language) node.setAttribute('aria-current', 'true');
    else node.removeAttribute('aria-current');
  });
  document.querySelector('meta[name="description"]').content = copy.description;
})();
