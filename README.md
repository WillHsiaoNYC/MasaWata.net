# masawata.net

Website hosted at https://masawata.net

## Structure

```
masawata.net/
├── index.html              → masawata.net/
├── privacy-policy.html     → masawata.net/privacy-policy.html
├── app-ads.txt             → masawata.net/app-ads.txt
├── CNAME                   → Custom domain configuration
└── FitnessStory/           → masawata.net/FitnessStory/
    ├── index.html          → English landing page
    ├── [lang]/index.html   → 13 localized versions
    ├── build.py            → Generates localized HTML pages
    └── ...                 → See FitnessStory/README.md
```

## Sites

- **Root** (`/`): Main landing page
- **Privacy Policy** (`/privacy-policy.html`): Privacy policy for apps
- **Fitness Story** (`/FitnessStory/`): Marketing site for the Fitness Story iOS app (14 languages)

## Updating Fitness Story

```bash
cd FitnessStory
python3 build.py
```

See [FitnessStory/README.md](FitnessStory/README.md) for detailed documentation.
