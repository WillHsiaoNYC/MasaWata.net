# masawata.net

Website hosted at https://masawata.net — the home of **MasaWata Tech**, an independent studio building focused apps for iPhone and Apple Watch.

## Structure

```
masawata.net/
├── index.html              → masawata.net/            (studio hub: index of all apps)
├── privacy-policy.html     → masawata.net/privacy-policy.html
├── favicon.svg             → site icon
├── llms.txt                → AI-agent-friendly site summary (llmstxt.org)
├── robots.txt              → crawl rules (search engines + AI crawlers welcomed)
├── sitemap.xml             → sitemap index (points at pages.xml + each app sitemap)
├── pages.xml               → sitemap for the root pages (home + privacy)
├── app-ads.txt             → masawata.net/app-ads.txt
├── CNAME                   → custom domain configuration
├── .well-known/            → apple-app-site-association (universal links)
├── FitnessStory/           → masawata.net/FitnessStory/    (build.py, [lang]/, sitemap.xml)
├── IceTimeTrack/           → masawata.net/IceTimeTrack/
├── SoccerTimeTrack/        → masawata.net/SoccerTimeTrack/  (Soccer Time Track)
├── SoccerMinutes/          → legacy redirects to SoccerTimeTrack/
├── TallyCounter123/        → masawata.net/TallyCounter123/
├── TimerOnMe/              → masawata.net/TimerOnMe/
└── WhereWasI/              → masawata.net/WhereWasI/
```

Each app directory is a self-contained marketing site. Product pages are generated from checked-in snapshots of their live App Store Connect localizations. Event, support, and privacy pages remain independent static pages.

## Sites

- **Home** (`/`): Studio hub — links to every app, with `Organization` / `WebSite` / `ItemList` structured data.
- **Privacy Policy** (`/privacy-policy.html`): Shared privacy information for apps without a dedicated product policy. Soccer Time Track uses its app-specific policy below `/SoccerTimeTrack/`.
- **Fitness Story** (`/FitnessStory/`): Apple Health & Watch workouts → visual journeys.
- **Ice Time Track** (`/IceTimeTrack/`): Automatic hockey shift detection for Apple Watch.
- **Soccer Time Track** (`/SoccerTimeTrack/`): Automatic soccer field time, match events, and player performance analysis for Apple Watch and iPhone.
- **Soccer Time Track legacy path** (`/SoccerMinutes/`): Redirects old marketing, support, and privacy-policy URLs to `/SoccerTimeTrack/`.
- **Tally Counter 123** (`/TallyCounter123/`): Watch-synced tally counter & scorekeeper.
- **Timer on Me** (`/TimerOnMe/`): Up to 50 timers & stopwatches at once.
- **Where was I?** (`/WhereWasI/`): Private, automatic location memory.

## AI-agent / crawler optimization

- `robots.txt` explicitly allows the major AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, CCBot, etc.).
- `llms.txt` gives agents a concise Markdown index of the studio and every app. Keep it in sync when apps are added or App Store links change.
- Every page ships static, server-rendered HTML (no JS required to read content) plus `SoftwareApplication` JSON-LD.
- When you add or remove an app: update `index.html` (the app list + `ItemList` JSON-LD), `llms.txt`, and `sitemap.xml`.

## Updating localized app sites

```bash
# Read-only: refresh live ASC metadata and localized screenshot manifests/assets.
python3 scripts/sync_asc_web.py

# Regenerate every product site.
python3 FitnessStory/build.py
python3 IceTimeTrack/build.py
python3 SoccerTimeTrack/build.py
python3 TallyCounter123/build.py
python3 TimerOnMe/build.py
python3 WhereWasI/build.py

# Prove generated routes and screenshots match the ASC snapshots.
python3 scripts/validate_asc_web.py
```

`scripts/sync_asc_web.py` only performs GET requests against App Store Connect. It prefers checksum-matching local fastlane screenshots and falls back to ASC's image CDN when a source is unavailable. Pass `--remote-assets` when local screenshot files are cloud placeholders. Ice Time Track currently inherits the English screenshot set for every locale because only `en-US` owns screenshot sets in live ASC.

The generated product routes use exact ASC locale identifiers. Older generic routes such as `/de/`, `/es/`, `/fr/`, `/pt/`, and `/nb/` are maintained as redirects where applicable.
