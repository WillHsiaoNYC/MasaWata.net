# Soccer Time Track website

Static, English-first product site published at:

- `https://masawata.net/SoccerTimeTrack/`
- `https://masawata.net/SoccerTimeTrack/support.html`
- `https://masawata.net/SoccerTimeTrack/privacy-policy.html`

There is no build step. Serve the repository root with any static HTTP server for local review. The legacy `/SoccerMinutes/` endpoints redirect to these canonical pages so existing App Store links remain valid during migration.

Run the no-dependency source checks with:

```bash
ruby SoccerTimeTrack/validate.rb
```

## Source assets

The optimized website images come from the approved English App Store screenshot set in the SoccerTrack repository. When screenshots change, regenerate the JPEGs at a web-appropriate size and keep meaningful alternative text in `index.html`.

## Release checklist

1. Validate the three HTML pages, JSON-LD blocks, internal links, and `sitemap.xml`.
2. Confirm the App Store launch status and CTA before replacing “Coming soon.”
3. Keep the privacy policy aligned with the release build’s Health, motion, location, iCloud, export, analytics, retention, and deletion behavior.
4. Update the root `index.html`, `llms.txt`, and `sitemap.xml` whenever the product name, availability, or App Store URL changes.
