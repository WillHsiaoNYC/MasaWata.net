# Car Plate Scan — The Everyday Collection website

The user approved the rendered event proposal and authorized app/build and website changes. This is the website implementation record, not an implementation handoff. The parent task owns CarPlate code, build identity, Universal Link runtime checks, ASC upload, and overall acceptance.

## Agreed behavior

- Canonical event URL: `https://masawata.net/CarPlateScan/event/everyday-collection/` (the app also accepts the no-trailing-slash form).
- Challenge: save three readable passing-car plates from a safe stationary public-sidewalk position, review the readings, and revisit the collection.
- Starts November 28, 2026, 9 AM EST (UTC−5); ends December 5, 2026, 9 AM EST. No prizes, rankings, automatic progress tracking, or guaranteed recognition.
- English and Traditional Chinese only. English static HTML; browser preferences select Traditional Chinese only for supported traditional variants, with an explicit language override. No cookies/storage/analytics.
- Exact app name is retained. Chinese instructions name the shipped 車牌 control. A `noscript` block provides Chinese instructions when scripting is disabled.
- Smart App Banner app ID is `6825007024`, with the canonical HTTPS URL as `app-argument`. The App Store listing link makes no pre-order/live availability claim.
- AASA adds only `YJBS4SMU7Z.net.MasaWata.CarPlateScan` for `/CarPlateScan/event/*`. Every prior app block remains identical. No development-app association is added.
- The public CarPlate landing, builder, studio catalog and llms.txt correct the planned date from November 30 to November 28. Historical October 25 planning text remains a historical record.

## Sources and assets

Approved proposal/package: `/Users/willhsiao/.codex/artifacts/CarPlate/in-app-events/2026-11-28-everyday-collection/`. The landscape editorial illustration is reused as a WebP asset. It is a fictional AI-generated street scene with blank plates, no generated app UI or recognition-performance claim. No personal data was used.

## Verification

- `node --check CarPlateScan/event/everyday-collection/event.js`
- `python3 -m unittest scripts.test_car_plate_scan scripts.test_asc_web` (11 passed)
- `python3 scripts/validate_asc_web.py` (all seven product sites passed; existing locale/screenshot inventories preserved)
- Parsed AASA comparison against baseline: all six existing association blocks unchanged; one CarPlate Store block appended.
- Local HTTP route/asset checks, explicit language round trips, browser-language preference/override cases, and no-JavaScript bilingual fallback.
- Direct rendered inspection at 1440 px desktop and 390 px mobile; English and Traditional Chinese, light and dark appearances. No horizontal overflow, missing images, or untranslated/undefined copy. Keyboard targets have visible focus and at least 44 px height.
- Raw logs, screenshots, route/behavior checks, and deployment evidence are retained outside the worktree in the package's `website-evidence/` folder.

## Integration

The site uses GitHub Pages legacy deployment from `main` at repository root. Coordinate merge with the parent, verify live fallback and AASA after deployment, then remove only the task website worktree and branch and fast-forward the original clean checkout. HTTP/browser availability and Apple CDN association do not establish installed-app dispatch; the parent verifies cold/warm app behavior separately. No app binary or ASC event is uploaded by this website task.
