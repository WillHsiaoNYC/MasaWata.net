# WhereWasI Landing Page Design

**Date:** 2025-01-23
**Status:** Approved

## Overview

Create a multi-language landing page for WhereWasI, an iOS location journal app that automatically tracks and organizes places users visit.

## App Details

- **App Name:** WhereWasI
- **App Store ID:** 6758056060
- **Platforms:** iPhone, iPad
- **Pricing:** Free (pricing TBD for future)
- **Data Source:** iPhone location services + manual editing
- **Privacy:** All data on-device/iCloud only

## Key Features

1. **Timeline/History View** - Beautiful visualization of location history
2. **Statistics/Insights** - Most visited places, time spent, patterns
3. **Map Visualization** - Interactive map of all visits
4. **Privacy-Focused** - No external servers, all data local

## Landing Page Structure

### 1. Hero Section

**Tagline:** "Remember Every Place You've Been"

**Description:**
> WhereWasI automatically tracks and organizes everywhere you go. Revisit your favorite spots, discover patterns in your daily life, and keep a private journal of your journey—all without lifting a finger.

**Elements:**
- App icon (centered, prominent)
- Tagline + description
- App Store download badge
- Device frame showing the app
- No rating stars initially

### 2. Features Section

**Feature 1: Timeline View**
- Icon: Clock/timeline
- Title: "Your Life in Timeline"
- Description: "Scroll through a beautifully organized history of everywhere you've been. See your visits by day, week, or month—your life story unfolds automatically."

**Feature 2: Smart Statistics**
- Icon: Bar chart
- Title: "Discover Your Patterns"
- Description: "Uncover insights about your daily life. See your most visited places, time spent at each location, and how your routines evolve over time."

**Feature 3: Interactive Map**
- Icon: Map pin
- Title: "Your World at a Glance"
- Description: "View all your visits plotted on an interactive map. Zoom out to see everywhere life has taken you, or zoom in to explore a single neighborhood."

**Feature 4: Privacy First**
- Icon: Shield/lock
- Title: "Your Data, Your Device"
- Description: "All location data stays securely on your iPhone and your personal iCloud. Nothing is ever sent to external servers. Your journey remains yours alone."

### 3. Screenshots Gallery

Horizontal scrollable gallery with prev/next buttons showing:
1. Timeline view (main screen)
2. Visit detail page
3. Map view with pins
4. Statistics/insights dashboard
5. Place detail with visit history
6. Additional UI screens

### 4. Download CTA Section

**Title:** "Start Remembering Today"

**Description:**
> Free to download. Your location journal begins the moment you install. No account required—just you, your iPhone, and the places you go.

**Elements:**
- App icon
- App Store download badge
- Platform badge: "Available on iPhone and iPad"

### 5. FAQ Section

**Q1: How does WhereWasI track my location?**
> WhereWasI uses iOS location services to detect when you arrive and leave places. It runs efficiently in the background without draining your battery.

**Q2: Is my location data private?**
> Absolutely. All data is stored locally on your device and synced only to your personal iCloud account. We never see or store your location data on any external servers.

**Q3: Can I edit or delete visits?**
> Yes! You have full control. Edit visit times, merge duplicate places, add notes, or delete any visits you don't want to keep.

**Q4: Does it drain my battery?**
> No. WhereWasI uses Apple's power-efficient significant location change APIs, designed to minimize battery impact while still capturing your visits accurately.

### 6. Privacy Statement Section

Compact section with shield icon:
> "WhereWasI keeps all your location data on your device and your personal iCloud account. Your travels are never shared with us or any third parties."

Link to: masawata.net/privacy-policy.html

### 7. Footer

- App icon + "WhereWasI" name
- Links: App Store, Privacy Policy, Terms of Service
- Copyright: "© 2025 WhereWasI. All rights reserved."

## Technical Approach

### Reuse from FitnessStory

- Build system (build.py adapted for WhereWasI)
- CSS structure (style.css with WhereWasI theming)
- JavaScript (main.js for gallery, dropdowns, animations)
- Multi-language support (14 languages)
- SEO optimizations (meta tags, structured data, hreflang)

### Directory Structure

```
WhereWasI/
├── assets/
│   └── app-store-badges/
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
│   ├── WhereWasI.png (app icon)
│   ├── en/
│   │   ├── raw/
│   │   └── (optimized images)
│   └── [other language folders as needed]
├── locales/
│   ├── en.json
│   ├── zh-Hans.json
│   └── ... (14 language files)
├── [language directories]/
│   └── index.html (generated)
├── index.html (generated, English)
├── build.py
├── sitemap.xml (generated)
├── robots.txt
└── CLAUDE.md
```

### Differences from FitnessStory

- No promo banner (pricing TBD)
- 4 features instead of 11
- No testimonials section (initially)
- Simpler platform support (iPhone + iPad only)
- Different color scheme/theming (TBD based on app icon)

## Images Required

| Image | Purpose | Suggested Size |
|-------|---------|----------------|
| App icon | Hero, footer, favicon | 512x512 PNG |
| Hero screenshot | Device frame | 1290x2796 (iPhone 15 Pro) |
| 4 feature images | Feature cards | iPhone screenshot |
| 5-8 gallery images | Screenshots section | iPhone screenshot |

## Next Steps

1. Create WhereWasI directory structure
2. Adapt build.py from FitnessStory
3. Create English locale file (en.json)
4. Create CSS with WhereWasI theming
5. Copy and adapt JS from FitnessStory
6. Create index.html template
7. Run build and verify
8. Add remaining locale files (13 languages)
9. Add images when available
10. Test and refine
