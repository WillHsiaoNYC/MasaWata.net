# Car Plate Scan English product website

Status: **REVIEWED — ready for implementation handoff.** Independent planning review completed October 25, 2026. No implementation authorized to Astra or performed.

Executor: **GPT-6.1-Sol with reasoning effort `xhigh`**.

## Objective and authority

Create the English-only product website at **https://masawata.net/CarPlateScan/** in the existing MasaWata.net repository. Use the user's other product pages as the structural reference and Car Plate Scan's actual ASC English metadata and screenshots as the content source. The user plans release on **November 30**; interpret the year as **2026** from this session's date and describe it as planned, not guaranteed.

The user requested a website, not an Apple app change. Their standing instructions authorize implementation by Sol, proportionate verification, task-only commits, push, normal PR/merge integration, and task branch/worktree cleanup. Astra remains planning-only. No application source, dependencies, build configuration, tests, production resources, branches, or commits were changed in planning. A read-only fetch was performed.

Repository: `/Users/willhsiao/Desktop/Air Repo/MasaWata.net`
Remote: `https://github.com/WillHsiaoNYC/MasaWata.net.git`
Reviewed source: local main `46279c2f7ee2e17e29ec57e6a8d097871942949d`; fetched origin/main `106cc169f0ba5eb9b094e78a5953e404ca6ac21a` on October 25, 2026. Start implementation from freshly fetched current main.

GitHub Pages API confirms legacy Pages publishing from `main`, path `/`, custom URL `https://masawata.net/`. Use this existing hosting; do not create a Sites project, register another domain, or change hosting settings. Merging these static website files publishes through the repository's normal Pages flow, which fulfills the requested public URL. No separate app release, tag, package publication, or Apple submission is authorized.

## User decisions and justified design defaults

Explicit: new product page at `/CarPlateScan/`; English only; planned November 30 release; refer to existing app product pages; use ASC metadata and screenshots.

Defaults selected from evidence, not presented as user-approved mockups:

- Match the established product-page progression: branded header, large hero, ASC description/features, screenshot gallery, final action panel, footer. Add a visible return link to the MasaWata studio.
- Use slate/near-black surfaces, mint/teal details and restrained amber highlights from the supplied artwork and icon. Maintain the established system-font typography and readable spacing. Suggested tokens: background `#0b171c`, surface `#13232c`, text `#f4f8f7`, muted `#b5c8ca`, mint `#a7dfd2`, amber `#f5cc69`; verify contrast instead of assuming it.
- Show `Car Plate Scan` as the compact brand; preserve the complete ASC name `Car Plate Scan: License Reader`, subtitle `Photo OCR, History & Locations`, and promotional text visibly in the page. The ASC subtitle can remain the main heading to minimize renderer changes; do not invent a different product position.
- Use the first ASC poster as the hero image and all seven screenshots in their existing order in the gallery. Do not crop off captions, redraw app screens, generate replacement art, or add another device frame around already-framed screenshots.
- Initial launch status: `Planned release: November 30, 2026`. Primary action: `Explore screenshots`, linking to `#screenshots`. Repeat the same truthful status in the final action panel and root catalog entry. Do not use an active Download/Get/Pre-order action until publicly verified availability supports it.
- No countdown, email collection, accounts, live scanning demo, tracking additions, pricing, ratings, testimonials, or unsupported device/language promises.

No extra user decision blocks implementation under these defaults. The launch year is an explicit interpretation; correct it if the user supplies another year. No rendered design proposal was requested or created during planning.

## Verified product evidence

ASC was read through the existing read-only client and saved outside the repository:

- App Store ID: `6825007024`.
- Bundle ID: `net.MasaWata.CarPlateScan` (use ASC, not stale development identifiers in app README).
- Version: `1.0`, ID `6c5328b1-15ae-4b33-936c-018ba3c7ff87`, state `PREPARE_FOR_SUBMISSION`.
- App info ID: `fbb8f6bd-11ab-4211-8b45-b4e91f0b9dc8`.
- English version-localization ID: `6e43ff4c-625f-4540-b812-6cec80b921b2`.
- English info-localization ID: `9286e7e0-a72d-4844-9b43-71cea9b5c437`.
- Screenshot set: `dd27fdfb-b07a-440b-b946-5f2200325e81`, display type **`APP_IPHONE_61`**, seven COMPLETE images, original size **1206 × 2622**.
- Release attributes currently say `AFTER_APPROVAL` and `earliestReleaseDate: null`. November 30 is the user's plan; it is not configured or confirmed by ASC.
- The public US listing `https://apps.apple.com/us/app/id6825007024` displayed Apple's page-not-found state. `downloadable: true` in draft ASC attributes does not prove public availability.
- ASC privacy-policy, support, and marketing URL fields are currently null. Do not fill or alter ASC as part of this task.

Durable source bundle (same directory as this plan):

- `asc-en-US-source.json`: sanitized English copy, source identifiers/state, screenshot filenames/checksums/CDN templates. Suitable for deriving checked-in website snapshots.
- `asc-en-US-evidence.json`: raw private read response; retain externally and **do not commit raw API responses**, upload operations, credentials, or signed upload URLs.
- `asc-screenshots/01-01-poster-left.webp` through `07-07-favorites.webp`: downloaded, visually inspected 600-pixel-wide reference assets. For website output prefer fresh CDN downloads at the established 720-pixel width, preserving aspect ratio.
- `app-icon.png`: existing regular 1024-pixel icon copied for durable reference; SHA-256 `25178dbdc590e064fee242e6e56befdda76bf2b3b1b59f9c3ea81f790a9bfd50`.
- `reference-wherewasi-desktop.png`, `reference-studio-desktop.png`: observed existing page references, not proposals to integrate.

Icon original: `/Users/willhsiao/Desktop/Air Repo/CarPlate/CarPlateScan/CarPlateScan/Assets.xcassets/AppIcon.appiconset/AppIcon-Regular.png`. Reading/copying this existing asset is in scope; changing the CarPlate repository is not.

Screenshot source order and accessible descriptions:

1. `01-poster-left.png` — Car Plate Scan promotional overview; Scan it. Keep the details.
2. `02-poster-right.png` — Camera or photos, capture history, maps and favorites.
3. `03-scan.png` — Scan license plates from the camera or photos.
4. `04-review.png` — Review and edit a plate reading before saving.
5. `05-history.png` — Search saved plate capture history.
6. `06-map.png` — Browse captures by map and date.
7. `07-favorites.png` — Find favorite plates.

Keep the complete current ASC description present in semantic HTML, preserving its claims and meaningful paragraphs. It explains camera/photo capture, uncertain-reading review/correction, automatic-save/repeat settings, crop/full-frame images, capture times and available locations, repeated sightings, search/date/map browsing, and favorites. It explicitly says there are no owner identities, VIN/registration/vehicle-history reports; core reading is on device; optional cloud review uses Apple Private Cloud Compute on supported devices with internet and availability limits; recognition can be incorrect; do not operate while driving; respect privacy. Do not claim all processing is offline or all data always stays on device.

## Privacy and support treatment

The studio-wide `privacy-policy.html` currently claims that data never goes to any third-party server. That conflicts with the verified optional PCC flow. Do not link that document as if it accurately describes this app, and do not rewrite policy for unrelated apps.

Provide a clearly named `Privacy & processing` section/anchor containing the exact relevant ASC paragraphs; link the footer's `Privacy & processing` item to it. This is product information, not a newly drafted legal privacy policy. Do not label it `Privacy Policy`. Add Support using the studio's existing `mailto:fitnessstoryapp@gmail.com`, and the existing Apple standard terms link. Do not invent a support site or empty legal document. Record the absent dedicated legal policy as an ASC-launch follow-up outside this website task, not a reason to leave the website unfinished.

## Repository contracts and likely file scope

- `README.md`: static repository structure, commands and catalog-maintenance rules.
- `scripts/sync_asc_web.py`: app registry; `live_context()` only accepts released versions and a live app-info record; screenshot configuration defaults to `APP_IPHONE_67`. A naive registry entry will fail for this app. `remote_screenshot_manifest()` currently processes every returned locale.
- `scripts/asc_web.py`: shared renderer/builder and HTML escaping; existing parameters cover colors, stylesheets and pre-hero HTML. Current renderer unconditionally creates a language picker, download CTA, Smart App Banner, `downloadUrl`, generic screenshot alt text, and `operatingSystem: iOS, iPadOS, watchOS`.
- `includes/asc-localized.css`: shared responsive layout and reduced-motion support, used by existing products.
- `TimerOnMe/build.py`, `WhereWasI/build.py`, and their generated English pages: implementation conventions.
- The five shared-builder consumers are FitnessStory, IceTimeTrack, SoccerTimeTrack, TimerOnMe and WhereWasI. `TallyCounter123/build.py` is a separate renderer that reads external Markdown through `ASC_SOURCE`; do not run it just to verify a shared-renderer change.
- `scripts/validate_asc_web.py`: fixed site list, full-description preservation, snapshot/gallery parity, canonical and hreflang checks. Extend coverage to the new English-only site without requiring other ASC languages.
- `scripts/test_asc_web.py`: current shared-renderer sitemap tests.
- `index.html`: studio catalog, displayed count `Index · 06`, structured-data `numberOfItems: 6`, title/description/keyword catalog mentions, and app rows.
- `llms.txt`, root `sitemap.xml`: add new product; do not submit a draft-only or nonexistent language route.
- Existing `404.html` redirects unknown paths to FitnessStory. `/CarPlateScan/` currently reaches that fallback. Verification must check the actual HTTP result and final URL/content, not merely that a page appeared. Do not redesign the global 404 handler in this task.

Expected new files: `CarPlateScan/build.py`, `CarPlateScan/index.html`, `CarPlateScan/asc-metadata.json`, `CarPlateScan/asc-assets.json`, `CarPlateScan/images/app-icon.png`, seven `CarPlateScan/images/asc/en-US/NN-phone.webp` images, `CarPlateScan/sitemap.xml`, and an app-specific stylesheet only if necessary. Add no JS unless a required interaction cannot work natively. No non-English pages or locale files.

## Ordered execution

1. Read applicable AGENTS.md and skills. Refresh Git state, inspect worktrees/branches/checks and preserve unrelated work. Create a short-lived task branch from current `origin/main`, using an isolated temporary worktree if useful. **Copy this reviewed plan into `docs/plans/2026-10-25-car-plate-scan-website.md` on that branch and commit it with the implementation.** Keep its agreement/review outcome intact; append deviations and final verification instead of rewriting approval history. Keep the external handoff available until integration completes.
2. Re-read ASC English content and screenshot set through the existing credentials/client, GET only. Credentials live through `iOS_submission_tools`' existing loader; never print/store keys or tokens. Existing source directory is `/Users/willhsiao/Desktop/Air Repo/iOS_submission_tools`; its markdown apps tree has no Car Plate Scan entry today. Use current ASC and the sanitized planning snapshot, not another app's metadata.
3. Add narrowly scoped registry/sync support for **English-only CarPlateScan**, display type `APP_IPHONE_61`, and its unreleased version. Keep the existing six apps' live-only selection semantics. For this opt-in app prefer a live version if one actually exists; otherwise select the verified 1.0 draft explicitly and fail clearly on ambiguity/missing English data. Choose its corresponding editable info rather than calling live-info-only logic. Enforce `en-US` selection on both metadata and screenshots even if ASC later gains other locales. Preserve source version/state in the snapshot or equivalent documented provenance. Add no generic implicit fallback to any app's latest draft.
4. Import sanitized English snapshots and seven web-sized assets, maintaining ASC order and file checksums in the manifest. Copy the existing icon. Do not run a full-account website synchronization or touch other apps' snapshots/assets.
5. Implement the page using the shared builder/CSS with narrow opt-in options for this app's launch state, English-only header, correct platform metadata, accurate footer label/target and descriptive image alt text. Existing defaults must preserve other product output. If a small app-local renderer is materially simpler, document that choice and keep content escaping and regeneration explicit; do not duplicate the entire shared renderer or build a new framework. Avoid a generic configuration framework for a single page.
6. Render the design above with semantic static HTML. Header links to the studio and in-page About/Screenshots; no language dropdown. Put the planned date prominently next to the hero and final action, preserve the exact ASC text, and give the privacy paragraphs a clear anchor. Gallery supports native horizontal scrolling, keyboard access and visible focus; make it focusable/labeled where needed. Avoid hiding first/last screenshots. Images have intrinsic dimensions, useful alt text and lazy loading below the hero. Provide a skip link and prevent sticky-header anchor obstruction. Verify readable desktop/mobile contrast and reduced-motion behavior.
7. Use factual SEO: canonical `/CarPlateScan/`, English language, title, description, icon, Open Graph/Twitter information and absolute social image URL; use the existing poster/icon, no fabricated social image. Structured data is `SoftwareApplication` with name, true platform (iOS only unless current first-party evidence establishes more), description, URL and images. Omit unverified price/rating/offers, actual release date, download URL and Smart App Banner in coming-soon mode. Do not use the shared watchOS/iPadOS default accidentally. No nonexistent alternate languages; only self English/x-default if following the existing convention.
8. Add a Car Plate Scan row to the studio catalog with icon, factual short description, planned-release status and working product-page link. Update visible count and ItemList count/position, root metadata catalog mentions, README, llms.txt and sitemap index. Do not introduce a broken App Store link or download metadata in the catalog for this unreleased app.
9. Launch state must be an explicit website setting/default, not a clock switch: `coming-soon` now. If supporting later `preorder`/`available` states, only expose truthful labels after fresh public verification and never infer release from the November date or draft `downloadable` flag. A future launch-state update remains a follow-up unless release is actually verified during execution. The current page must remain useful if launch slips.
10. Run proportional verification below, inspect rendered results, simplify dead/duplicate code, and review task-only diff. Commit the plan and implementation, push, follow the repository's normal PR/check/merge flow, confirm the merged commit on default branch and the published new URL, then remove only this task's branch/worktree. Safely fast-forward the original main checkout while preserving its unrelated untracked screenshots. Keep evidence outside disposable resources.

## Verification and acceptance

Run existing checks before modifications once to establish relevant baseline failures. Expected commands from the task checkout:

```
python3 -m unittest scripts.test_asc_web
python3 scripts/validate_asc_web.py
python3 CarPlateScan/build.py
python3 scripts/sync_asc_web.py --app CarPlateScan --remote-assets --asc-tools '/Users/willhsiao/Desktop/Air Repo/iOS_submission_tools'
```

Planning baseline at local `46279c2` (shared scripts unchanged in the fetched two-commit delta): `python3 -m unittest scripts.test_asc_web` passed all three tests; `python3 scripts/validate_asc_web.py` passed all six existing products (179 locale pages total). All seven downloaded reference images decode. These are existing-site/source checks only, not verification of an implemented CarPlateScan page. Reuse this baseline if the source is unchanged; rerun after implementation and on any newly fetched relevant change.

The last command is a read-only ASC refresh that writes only this app's website snapshots/assets. Its explicit `--asc-tools` path is required from isolated worktrees: the current default is relative to the checkout's parent and will otherwise look for a nonexistent tools directory. Reuse the canonical tools/credential directory without copying credentials into the worktree. Run only after implementing the scoped prerelease/locale support. Build again after a refresh, validate, and prove an unchanged second build is idempotent. Do not call the unfiltered synchronizer. Check dependencies available before choosing interpreter; no new production dependency is authorized.

Add focused behavioral regression coverage for new shared logic, rather than assertions mirroring HTML internals: (a) draft selection works only for opted-in CarPlateScan; existing apps still reject unreleased-only data, (b) locale filtering excludes a supplied non-English locale from both snapshots/assets/routes, (c) coming-soon output has the planned date and working in-page CTA and lacks download/banner/offer claims, (d) correct product platform/footer semantics, (e) existing consumer defaults remain intact. Use fixtures/mocks for ASC selection tests, never writes to ASC. If implementing additional launch states, test those explicit transitions. Retain current sitemap/canonical tests. For the five actual shared-builder consumers, compare pre/post rendered baselines under unchanged snapshots; there should be no output changes from these opt-in extensions. Classify any pre-existing generation drift rather than fixing it here, and restore only task-created generated changes after inspection, not unrelated work. Validate TallyCounter123's checked-in output without rebuilding its independent external-Markdown pipeline unless a changed dependency demonstrably affects it.

Extend the validator to include CarPlateScan, full ASC description including caution paragraphs, seven ordered image references, correct manifest counts, indexability, one canonical English URL and applicable English alternates. Parse JSON/JSON-LD and XML. Check local internal URLs/assets exist and reject unexpanded placeholder links. Check hub count/list positions and the product entry's truthful launch status.

Serve the task checkout on localhost, capture mobile (~390px) and desktop (~1440px) views with **ego-browser** after reading its skill; inspect them directly. Cover hero/date, About, all seven images, native gallery scrolling, privacy anchor, footer, studio-to-product navigation and return, keyboard focus, narrow width/200% zoom, and reduced motion. No full-page horizontal overflow apart from the intentional gallery. Test one representative existing English product, one localized/RTL page, and current campaign/event hooks if shared renderer changes affect them; shared default output identity is useful supporting evidence. No Apple simulator, Xcode build, physical-device installation or Xcode source handoff is needed for a website-only repository change.

After merge/Pages publication verify actual HTTP 200 and correct canonical/final URL at `https://masawata.net/CarPlateScan/`, correct title/content instead of the existing 404 redirect, asset loads, and updated studio navigation. Record the deployed commit and evidence; diagnose bounded publication delay and report honestly if not yet verified. Do not hide a deployment failure behind a successful local preview.

## Delegation and responsibility

Orchestrator: **GPT-6.1-Sol, `xhigh`** owns scope, implementation, shared-contract impact analysis, diagnostics, evidence review, final acceptance, all edits and Git integration.

Preferred bounded verifier: **GPT-6-Luna, `medium`**, when available and useful. Give it a fresh minimal packet: exact checkout and commit/identified working-tree revision, commands, baseline warning/failure notes, local-preview URL and ownership, viewport/navigation assertions above, fixtures/prerequisites, and an absolute durable evidence directory. Assign one owner to the preview server/browser task space and generated files; verification must not race the orchestrator's build or snapshot refresh. Verifier may write evidence only, not product code, fixtures, snapshots or Git state.

Verifier reports every assigned case as passed/failed/blocked/not run with revision, observations and evidence paths. Preserve failures, distinguish baseline from new issues, and escalate after one bounded infrastructure investigation. It must not weaken assertions or silently skip failed cases. Orchestrator reviews evidence and closes coverage gaps, especially existing shared renderer consumers and navigation/return behavior. If Luna is unavailable, disclose the fallback and Sol runs the needed checks locally; do not silently pick a costlier model. Do not rerun passing checks without a changed input or unresolved concern.

## Integration, preservation and cleanup

At planning time the canonical checkout has 16 unrelated untracked `TallyCounter123/images/screenshots/.../* 2.jpg` files; preserve all exactly. It is two commits behind fetched main and has no tracked modifications. Other branches/worktrees exist for unrelated work. A stale/prunable date-alarms worktree record exists; do not treat this task as permission to prune/delete it or other tasks' branches.

Before landing fetch/prune remotes, inspect branches, worktrees, upstreams, PRs and required checks; perform only missing safe steps. Commit task files only. Preserve unrelated branches, PRs and worktrees. After merge confirm default HEAD contains the task, return canonical checkout to current main without stashing/discarding unrelated work, delete this task's local/remote branch and temporary worktree, and list **every remaining local and remote branch besides main with its retention reason**. Use `Retained branches: none` only if accurate.

Save screenshots/logs before stopping task-owned preview processes or removing disposable directories. Do not delete this external handoff as routine cleanup. The committed `docs/plans/...` copy becomes authoritative; append material implementation deviations and final tested revision/commands/results there. Keep references to product source/proposals understandable: commit sanitized source snapshots and final assets, not machine-only raw evidence or existing reference screenshots unless they materially aid review.

## Independent review outcome

Independent planning-only review completed October 25, 2026 by `/root/review_carplate_handoff`. Report: `independent-review.md` alongside this external plan. The reviewer inspected the plan, user decisions/instructions, saved source evidence and relevant repository code; live network findings and baseline test runs were attributed to the parent's evidence rather than claimed as independently repeated.

Both actionable findings were adopted and verified:

1. Pass the absolute canonical `--asc-tools` directory in the refresh command, because the current relative default fails in isolated worktrees; reuse credentials without copying them.
2. Restrict regeneration/output-identity checks to the five actual shared-builder consumers. TallyCounter123 reads external Markdown through its separate renderer; validate its existing output without an unrelated refresh, and classify any baseline generation drift separately.

The reviewer found no remaining blocking contradictions, missing product decisions or unsupported source assumptions and recommended delivery after recording these corrections. No findings were rejected; no substantial scope/design revision required another review. Preserve the privacy/legal-policy distinction and keep any optional future launch-state support minimal. Explicit user requirements and justified defaults remain distinguished above. No user approval of an unshown visual proposal or extra legal-policy scope is implied.

## Implementation and final implementation verification — October 25, 2026

The user subsequently directed execution with GPT-6.1-Sol and xhigh reasoning. Implemented on `feat/car-plate-scan-website` from `106cc16` in an isolated temporary worktree, preserving the canonical checkout and unrelated screenshot files.

Implemented the English-only product, all seven current ASC screenshots, static pre-release action/date, scoped `PageOptions` renderer presentation, explicitly pinned pre-release ASC selection with English-only filtering, catalog/count/schema integration, sitemap, README and llms.txt updates. A fresh read-only ASC import still reports version 1.0 in `PREPARE_FOR_SUBMISSION`. No ASC fields, Apple application files, hosting settings or dependencies were changed. The icon uses the existing approved artwork resized to 256 × 256 for web delivery. No additional future availability-state framework was needed.

Final source revision reviewed: `a4af5b20ef9b8bc4c8d3ec3ebabce8e9bc77dca0` (following `9b2cd2a`; the final source change corrected CSS specificity so the hero date uses the intended amber accent). This appended verification record itself is documentation only.

- `python3 -m unittest scripts.test_asc_web scripts.test_car_plate_scan`: **passed, 11 tests**, covering opt-in draft selection, live preference, missing-source failure, output locale filtering, processing-text preservation, escaped output, truthful pre-release metadata/actions, and existing defaults.
- `python3 scripts/validate_asc_web.py`: **passed**, seven products / 180 locale pages, including full ASC copy, ordered seven-image gallery, canonical/alternate links, local URLs/anchors, structured data and studio count/navigation.
- Pre/post renderer output comparison: **all 184 existing shared-consumer HTML/sitemap files byte-identical**. Tally's external-Markdown renderer was not run. CarPlateScan's repeated build is idempotent.
- `git diff --check origin/main...HEAD`: **passed**. Simplification review found no unused framework/dependency or unrelated generated changes; opt-in output preserves existing defaults.
- Bounded rendered UI verification by GPT-6-Luna, medium: **passed** desktop 1440px, mobile 390px, all seven image loads/order and gallery endpoints, no document overflow, studio/product return paths, screenshot/privacy anchors below sticky header, footer targets, keyboard skip-to-main/gallery focus/ArrowRight, reduced motion, and representative English/RTL/campaign pages. Parent inspected desktop/mobile screenshots and final hero directly before accepting results.
- Actual browser chrome 200% zoom: **not run**, because ego keyboard controls did not change it. Equivalent layout reflow at 720 CSS pixels passed; pinch-style page scaling was correctly excluded from the zoom claim. This is a verification limitation, not a claimed full zoom pass.

Raw logs, output hashes and UI evidence are retained outside disposable resources at `/Users/willhsiao/.codex/plans/2026-10-25-car-plate-scan-website/verification/`, notably `automated-checks.log`, `shared-consumer-result.json`, `ui-report.md`, and `browser-*.png`. Normal PR/merge integration and a fresh production URL/asset check follow this verified implementation. The dedicated legal policy and public App Store launch-state update remain separate follow-ups, as agreed above.
