# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important: Public Repository

This repository is public on GitHub. Before committing any file, ensure it does not contain:
- API keys, secrets, or credentials
- Personal information (emails, phone numbers, addresses)
- Internal URLs or private server addresses
- Any sensitive or proprietary information

When in doubt, ask before committing.

## Repository Structure

- **Root**: GitHub Pages site for masawata.net
- **FitnessStory/**: Multi-language landing page for the Fitness Story iOS app

## FitnessStory Build Command

```bash
cd FitnessStory && python3 build.py
```

This generates 14 localized HTML pages (one per language) and updates `sitemap.xml`. Run after any changes to translation files or the build script.

See `FitnessStory/CLAUDE.md` for detailed architecture and build documentation.
