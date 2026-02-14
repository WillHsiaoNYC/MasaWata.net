# Ice Time Track Landing Page Design

**Date**: 2025-01-29
**URL**: `masawata.net/IceTimeTrack/`
**Status**: Approved for implementation

---

## Overview

A comprehensive landing page for Ice Time Track, a hockey performance tracking app for Apple Watch + iPhone. The page serves dual purposes: educating hockey players about the app and driving App Store downloads.

**Key differentiator**: Automatic shift detection without manual tapping.

---

## Technical Specifications

### File Structure

```
IceTimeTrack/
├── index.html          # Single page (English only)
├── css/style.css       # Dark theme styles
├── js/main.js          # Interactions (FAQ accordion, gallery, nav)
├── images/             # Screenshots, app icon (added later)
└── assets/             # App Store badge
```

### Color Palette

| Purpose | Color | Hex |
|---------|-------|-----|
| Background | Deep black | `#0D0D0D` |
| Card/sections | Dark gray | `#1A1A1A` |
| Elevated | Lighter gray | `#242424` |
| Primary accent | Athletic gold | `#FFB81C` |
| On Ice indicator | Green | `#34C759` |
| On Bench indicator | Orange | `#FF9500` |
| Text primary | White | `#FFFFFF` |
| Text muted | Gray | `#A0A0A0` |

### Typography

- Headlines: Bold, uppercase with letter spacing (athletic/jersey feel)
- Body: Clean system font stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI', ...`)
- Numbers/stats: Monospace for scoreboard aesthetic

### Requirements

- Mobile-first responsive design
- Full SEO optimization:
  - Semantic HTML5 structure
  - Meta tags (title, description, Open Graph, Twitter Card)
  - JSON-LD structured data (SoftwareApplication)
  - Canonical URL
  - Proper heading hierarchy
- Fast loading (minimal JS, optimized images)
- Touch-friendly interactions

---

## Page Sections

### 1. Hero

**Layout**: Full-width dark background with subtle gold gradient glow at top, centered content.

**Content**:
```
[App Icon with gold glow]

ICE TIME TRACK

Automatic Shift Detection for Hockey Players

Know exactly how much ice time you get - without tapping your watch.
Track goals, penalties, and periods. Just start a session and play.

[Download on App Store button]

Available on Apple Watch + iPhone
```

**Subfeature callouts** (icons below button):
- Automatic shift detection
- Goal & assist tracking
- Penalty logging
- Game stats & analytics

**Visual elements**:
- App icon with subtle gold glow/shadow
- Watch mockup showing ON ICE / ON BENCH states (placeholder)
- Pulsing gold accent or ice texture overlay

---

### 2. Features

**Layout**: Section title "FEATURES" with gold underline, 6 cards in 2x3 grid (stacks on mobile).

**Cards** (each with icon, title, description):

1. **Automatic Shift Detection**
   - Icon: waveform/motion sensor
   - "Step on the ice and your Watch knows. No buttons to press during play - sensors detect skating vs. bench time automatically."

2. **Game Event Tracking**
   - Icon: hockey goal/net
   - "Log goals, assists, and penalties right from your wrist. Track periods and keep a complete record of every game."

3. **Live Health Metrics**
   - Icon: heart
   - "Monitor heart rate, calories burned, and movement intensity in real-time. See how hard you're working each shift."

4. **Session Analytics**
   - Icon: chart/graph
   - "Review total ice time, shift count, average shift length, and personal records. Track your progress over the season."

5. **Apple Health Integration**
   - Icon: Apple Health logo
   - "Sessions sync to Apple Health as hockey workouts. Contribute to your Activity rings and fitness history."

6. **Works Offline**
   - Icon: watch with checkmark
   - "Your Watch records everything independently. No iPhone needed on the bench - data syncs automatically after the game."

**Visual treatment**: Cards have `#1A1A1A` background with subtle gold border on hover.

---

### 3. How It Works (Game Day Story)

**Layout**: Section title "HOW IT WORKS" with gold underline, 3 steps in horizontal timeline (vertical on mobile), gold connecting line.

**Video placeholder**: Prominent video player area with play button overlay for future video content showing the game day flow.

**Steps**:

| Step | Title | Description | Mockup |
|------|-------|-------------|--------|
| 1 | BEFORE THE GAME | Open Ice Time Track on your Apple Watch. Tap Game, Practice, or Scrimmage to start. | Watch: session type select |
| 2 | DURING THE GAME | Step on the ice and your Watch detects it automatically. Log goals and penalties with a tap. Focus on playing. | Watch: ON ICE status |
| 3 | AFTER THE GAME | Your session syncs to your iPhone. Review ice time, shifts, heart rate, and game events. Export or share your stats. | iPhone: session summary |

**Visual treatment**: Step numbers in large gold typography, timeline connector with gold gradient, device mockups (placeholders).

---

### 4. Screenshots Gallery

**Layout**: Section title "SEE IT IN ACTION" with gold underline, horizontal scrollable gallery with device frames.

**Screenshot slots** (8 total, placeholders for now):

**Apple Watch**:
1. Home screen - session type selection
2. Active session - ON ICE state with timer and heart rate
3. Active session - ON BENCH state showing shift count
4. Game event logging - goal/penalty buttons

**iPhone**:
5. Sessions list - history of games and practices
6. Session detail - ice time summary, shifts, health stats
7. Analytics/trends view - charts and personal records
8. Live session monitoring - watching active Watch session

**Interaction**: Auto-advances, pauses on hover/touch, arrow buttons, snap-to-card scrolling.

---

### 5. Testimonials

**Layout**: Section title "WHAT PLAYERS SAY" with gold underline, 3 cards in row (stacks on mobile).

**Placeholder testimonials** (replace with real App Store reviews):

```
Card 1:
★★★★★
"Finally an app that tracks my ice time without me having to tap anything.
Game changer for tracking my shifts."
— Hockey Dad

Card 2:
★★★★★
"Love seeing my heart rate and shift stats after each game. Helps me
understand my conditioning."
— Beer League Player

Card 3:
★★★★★
"The automatic detection is surprisingly accurate. My kids use it every game now."
— Youth Hockey Parent
```

**Visual treatment**: Cards with `#1A1A1A` background, gold accent quote marks.

---

### 6. FAQ

**Layout**: Section title "FREQUENTLY ASKED QUESTIONS" with gold underline, accordion-style expandable questions.

**Content**: Curated from app's FAQData.swift (~8-10 most relevant questions). Rescan codebase during implementation for latest content.

**Categories to pull from**:
- Getting Started
- Shift Detection
- Health & Fitness
- Privacy

**Interaction**: One question open at a time, smooth expand/collapse animation, chevron icon indicates state.

---

### 7. Download CTA

**Layout**: Full-width section with `#1A1A1A` background, centered content.

**Content**:
```
[App Icon with gold glow]

READY TO TRACK YOUR ICE TIME?

Download Ice Time Track and see exactly
how much you play - automatically.

[Download on App Store button]

Requires Apple Watch Series 4 or later
```

**Visual treatment**: Larger App Store button than hero, subtle device requirements note.

---

### 8. Footer

**Layout**: Full-width dark background, minimal centered content.

**Content**:
```
Ice Time Track

Privacy Policy  •  Terms of Service  •  Support

© 2025 MasaWata. All rights reserved.
```

**Links**:
- Privacy Policy → `/privacy-policy.html`
- Terms of Service → TBD
- Support → email or support page

**Visual treatment**: Muted text (`#A0A0A0`), gold hover on links.

---

## Implementation Notes

1. **No multi-language support** - English only, no build script needed
2. **No pricing/tier mentions** - Present all features as part of the app
3. **Screenshots are placeholders** - Structure page first, add images later
4. **Video placeholder** - Include player area in "How It Works" for future video
5. **FAQ content** - Rescan `/Users/willhsiao/Desktop/Watch App/IceTimeTrack/Ice Time Track/Ice Time Track Phone/Models/FAQData.swift` during implementation for latest questions
6. **App Store link** - Use placeholder, update when app is live

---

## SEO Checklist

- [ ] Single `<h1>` with app name and value proposition
- [ ] Logical `<h2>`/`<h3>` hierarchy for sections
- [ ] Meta title: "Ice Time Track - Automatic Hockey Shift Detection for Apple Watch"
- [ ] Meta description: ~155 characters summarizing the app
- [ ] Open Graph tags for social sharing
- [ ] Twitter Card tags
- [ ] JSON-LD SoftwareApplication structured data
- [ ] Canonical URL
- [ ] Alt text for all images
- [ ] Semantic HTML5 sections
