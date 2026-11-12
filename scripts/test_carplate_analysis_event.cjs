const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.join(__dirname, '../CarPlateScan/event/analysis-collections');
const data = JSON.parse(fs.readFileSync(path.join(root, 'localizations.json'), 'utf8'));
const {resolveLocale, chooseLocale} = require(path.join(root, 'event.js'));
const supported = Object.keys(data.locales);

test('all46 approved selectable variants resolve exactly', () => {
  assert.equal(supported.length, 46);
  for (const code of supported) assert.equal(resolveLocale(code, supported), code);
});
test('Traditional script inference never selects Simplified or ambiguous Chinese', () => {
  for (const tag of ['zh-TW', 'zh-HK', 'zh-MO', 'zh-Hant-TW']) assert.equal(resolveLocale(tag, supported), 'zh-Hant');
  for (const tag of ['zh', 'zh-CN', 'zh-SG', 'zh-Hans', 'zh-Hans-HK']) assert.equal(resolveLocale(tag, supported), null);
});
test('excluded, unknown and ambiguous overrides fall back to English', () => {
  for (const tag of ['ja', 'ko-KR', 'th', 'zh-Hans', 'unknown', 'fr', 'es', 'pt', '']) {
    assert.equal(chooseLocale(tag, ['de-DE'], supported), 'en-US');
  }
});
test('explicit preference and supported browser preference take precedence', () => {
  assert.equal(chooseLocale('zh-Hant', ['de-DE'], supported), 'zh-Hant');
  assert.equal(chooseLocale('en-US', ['zh-TW'], supported), 'en-US');
  assert.equal(chooseLocale(null, ['ja-JP', 'de-DE', 'en-US'], supported), 'de-DE');
  assert.equal(chooseLocale(null, ['zh-Hans'], supported), 'en-US');
  assert.equal(chooseLocale(null, ['fr-CA', 'fr-FR'], supported), 'fr-CA');
  assert.equal(chooseLocale(null, ['es-MX'], supported), 'es-MX');
});
test('single-variant aliases retain approved copy without inventing a region', () => {
  for (const [tag, code] of Object.entries({en:'en-US',de:'de-DE',ar:'ar-SA',bn:'bn-BD',ur:'ur-PK',nb:'no',iw:'he',hi_IN:'hi'})) {
    assert.equal(resolveLocale(tag, supported), code);
  }
});
test('confirmed New York event dates span exactly14 days in every locale', () => {
  assert.equal(data.start, '2026-12-01T09:00:00-05:00');
  assert.equal(data.end, '2026-12-15T09:00:00-05:00');
  assert.equal(new Date(data.end) - new Date(data.start), 14*24*60*60*1000);
  for (const code of supported) {
    const formatter = new Intl.DateTimeFormat(code, {timeZone:'America/New_York',hour:'numeric'});
    assert.equal(formatter.resolvedOptions().timeZone, 'America/New_York');
    assert.ok(formatter.format(new Date(data.start)).length);
  }
});
