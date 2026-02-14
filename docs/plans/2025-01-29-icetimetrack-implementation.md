# Ice Time Track Landing Page Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Use frontend-design:frontend-design skill for each UI task.

**Goal:** Build a production-grade landing page for Ice Time Track at `masawata.net/IceTimeTrack/` with dark theme, gold accents, and full SEO.

**Architecture:** Single-page static site (HTML + CSS + JS) following the same patterns as the existing FitnessStory landing page but with an entirely dark theme (`#0D0D0D`) and athletic gold (`#FFB81C`) accents. No build script needed (English only). CSS variables for theming, BEM naming, semantic HTML5.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, flexbox), vanilla JavaScript (no frameworks).

**Reference:** Design doc at `docs/plans/2025-01-29-icetimetrack-landing-page-design.md`. Existing FitnessStory site at `FitnessStory/` for structural patterns.

---

### Task 1: Create directory structure and CSS foundation

**Files:**
- Create: `IceTimeTrack/css/style.css`
- Create: `IceTimeTrack/js/main.js` (empty placeholder)
- Create: `IceTimeTrack/images/` (empty directory)
- Create: `IceTimeTrack/assets/` (empty directory)

**Step 1: Create directories**

```bash
mkdir -p MasaWata.net/IceTimeTrack/{css,js,images,assets}
```

**Step 2: Create CSS with variables and reset**

Create `IceTimeTrack/css/style.css` with:
- CSS custom properties matching design color palette (#0D0D0D, #1A1A1A, #242424, #FFB81C, etc.)
- Typography variables (system font stack, sizes, letter-spacing for athletic feel)
- Spacing, border-radius, transition, layout variables
- CSS reset and base styles (dark background, white text)
- Container utility class (max-width 1200px)
- Reuse pattern from `FitnessStory/css/style.css` but invert to dark theme

**Step 3: Create empty JS placeholder**

Create `IceTimeTrack/js/main.js` with IIFE wrapper only.

**Step 4: Copy App Store badge asset**

```bash
cp -r MasaWata.net/FitnessStory/assets/app-store-badges MasaWata.net/IceTimeTrack/assets/
```

**Step 5: Verify structure**

```bash
find MasaWata.net/IceTimeTrack -type f
```

Expected: `css/style.css`, `js/main.js`, `assets/app-store-badges/...`

---

### Task 2: Build HTML structure with SEO head and Hero section

**Files:**
- Create: `IceTimeTrack/index.html`
- Reference: `FitnessStory/index.html` for SEO pattern

**Step 1: Create index.html with full `<head>`**

Include:
- `<!DOCTYPE html>`, `<html lang="en">`
- `<meta charset="UTF-8">`, viewport meta
- `<title>`: "Ice Time Track - Automatic Hockey Shift Detection for Apple Watch"
- `<meta name="description">`: ~155 char summary
- Canonical URL: `https://masawata.net/IceTimeTrack/`
- Open Graph tags (og:type, og:url, og:title, og:description, og:image, og:site_name)
- Twitter Card tags (summary_large_image)
- Apple Smart Banner meta tag (placeholder app-id)
- Favicon link (placeholder)
- Stylesheet link to `css/style.css`
- JSON-LD structured data (SoftwareApplication, name: "Ice Time Track", operatingSystem: "iOS, watchOS", applicationCategory: "SportsApplication")

**Step 2: Build Header with nav**

- Sticky header with backdrop-filter blur (dark variant)
- Logo area: app icon placeholder + "Ice Time Track" text
- Nav links: Features, How It Works, Screenshots, FAQ, Download
- Mobile hamburger toggle
- No language selector needed

**Step 3: Build Hero section**

- Full-width section with dark background + subtle gold radial gradient glow at top
- App icon placeholder with gold box-shadow glow
- `<h1>`: "Automatic Shift Detection for Hockey Players"
- Paragraph: "Know exactly how much ice time you get..."
- App Store download button (placeholder link)
- 4 subfeature callouts with SVG icons (shift detection, goals, penalties, analytics)
- "Available on Apple Watch + iPhone" text
- Device mockup placeholder area

**Step 4: Open in browser to verify**

```bash
open MasaWata.net/IceTimeTrack/index.html
```

Expected: Dark page with gold accents, hero section displays correctly, responsive on mobile.

---

### Task 3: Build Features section CSS and HTML

**Files:**
- Modify: `IceTimeTrack/index.html`
- Modify: `IceTimeTrack/css/style.css`

**Step 1: Add Features section HTML**

After hero section, add:
- `<section class="features" id="features">`
- Section header: `<h2>` "Features" with gold underline accent
- 6 feature cards in grid, each with:
  - SVG icon in gold-tinted container
  - `<h3>` title
  - `<p>` description
  - `data-aos="fade-up"` for scroll animation

**6 cards:**
1. Automatic Shift Detection (waveform icon)
2. Game Event Tracking (target/goal icon)
3. Live Health Metrics (heart icon)
4. Session Analytics (bar-chart icon)
5. Apple Health Integration (activity icon)
6. Works Offline (watch-checkmark icon)

**Step 2: Add Features CSS**

- Section padding, dark background
- Section header with gold underline (border-bottom or pseudo-element)
- 3-column grid → 2-column at 1024px → 1-column at 768px
- Feature cards: `#1A1A1A` background, rounded corners, hover: gold border + translateY(-4px)
- Icon containers with gold-tinted backgrounds
- All text white/muted

**Step 3: Verify in browser**

Open and check responsive behavior at desktop/tablet/mobile widths.

---

### Task 4: Build How It Works section with video placeholder

**Files:**
- Modify: `IceTimeTrack/index.html`
- Modify: `IceTimeTrack/css/style.css`

**Step 1: Add How It Works HTML**

- `<section class="how-it-works" id="how-it-works">`
- Section header: `<h2>` "How It Works"
- Video placeholder: 16:9 aspect ratio container with play button SVG overlay, dark background with gold border
- 3-step timeline:
  - Step 1: "Before the Game" - number in gold, title, description, device mockup placeholder
  - Step 2: "During the Game"
  - Step 3: "After the Game"
- Gold connecting line between steps

**Step 2: Add How It Works CSS**

- Horizontal timeline layout with flexbox (vertical stack on mobile)
- Large gold step numbers (font-size: 3rem, gold color)
- Gold connecting line (pseudo-element or border)
- Step cards with `#1A1A1A` background
- Video placeholder: aspect-ratio 16/9, `#1A1A1A` background, centered play button with gold circle
- Device mockup placeholder areas (rounded rectangles with subtle border)
- Responsive: stack vertically on mobile, vertical line instead of horizontal

**Step 3: Verify in browser**

Check timeline displays correctly at all breakpoints.

---

### Task 5: Build Screenshots gallery section

**Files:**
- Modify: `IceTimeTrack/index.html`
- Modify: `IceTimeTrack/css/style.css`

**Step 1: Add Screenshots HTML**

- `<section class="screenshots" id="screenshots">`
- Section header: `<h2>` "See It In Action"
- Horizontal scrollable track with 8 screenshot placeholder items
- Each item: placeholder image area (dark gray with "Screenshot" text)
- Items 1-4: Apple Watch size (smaller width)
- Items 5-8: iPhone size (larger width)
- Prev/Next arrow buttons

**Step 2: Add Screenshots CSS**

- Horizontal scroll container with `scroll-snap-type: x mandatory`
- Hidden scrollbar
- Placeholder items: `#1A1A1A` background, rounded corners, appropriate aspect ratios
- Watch screenshots: ~160px width
- iPhone screenshots: ~220px width
- Hover: subtle scale effect
- Arrow buttons: gold on hover
- Responsive: smaller items on mobile

**Step 3: Verify scrolling behavior**

Test horizontal scrolling, snap behavior, and arrow buttons.

---

### Task 6: Build Testimonials section

**Files:**
- Modify: `IceTimeTrack/index.html`
- Modify: `IceTimeTrack/css/style.css`

**Step 1: Add Testimonials HTML**

- `<section class="testimonials" id="testimonials">`
- Section header: `<h2>` "What Players Say"
- 3 testimonial cards, each with:
  - 5 gold star SVGs
  - Quote text (with large gold `"` accent mark)
  - Author name
  - `data-aos="fade-up"` with staggered delays

**Step 2: Add Testimonials CSS**

- 3-column grid → 1-column on mobile
- Cards: `#1A1A1A` background, rounded corners, padding
- Gold quote mark (large `"` character, positioned top-left, gold color, low opacity)
- Stars: gold fill
- Quote text: white, italic
- Author: muted gray
- Hover: translateY(-4px) + shadow

**Step 3: Verify in browser**

---

### Task 7: Build FAQ section with accordion (rescan FAQData.swift)

**Files:**
- Modify: `IceTimeTrack/index.html`
- Modify: `IceTimeTrack/css/style.css`
- Reference: `/Users/willhsiao/Desktop/Watch App/IceTimeTrack/Ice Time Track/Ice Time Track Phone/Models/FAQData.swift`

**Step 1: Rescan FAQData.swift for latest content**

Read the file and select ~10 most relevant questions for a landing page from categories:
- Getting Started (how to start, Watch independence)
- Shift Detection (how it works, colors, delay)
- Health & Fitness (what data is tracked, HealthKit)
- Privacy (data sharing, permissions)

**Step 2: Add FAQ HTML**

- `<section class="faq" id="faq">`
- Section header: `<h2>` "Frequently Asked Questions"
- Accordion list with selected Q&A items
- Each item: `<button>` question with chevron SVG, `<div>` answer
- `aria-expanded` attributes for accessibility

**Step 3: Add FAQ CSS**

- Adapted from FitnessStory FAQ styles but with dark theme
- Items: `#1A1A1A` background, gold left border on active/hover
- Question text: white, gold accent number counter
- Chevron: rotates 180deg on expand
- Answer: max-height transition for smooth expand/collapse
- Gold accents replace blue from FitnessStory

**Step 4: Verify accordion behavior**

(Will need JS from Task 9 to function - verify styling only at this step.)

---

### Task 8: Build Download CTA and Footer sections

**Files:**
- Modify: `IceTimeTrack/index.html`
- Modify: `IceTimeTrack/css/style.css`

**Step 1: Add Download CTA HTML**

- `<section class="download" id="download">`
- App icon placeholder with gold glow
- `<h2>`: "Ready to Track Your Ice Time?"
- Description paragraph
- Large App Store button (placeholder link)
- "Requires Apple Watch Series 4 or later" note

**Step 2: Add Download CTA CSS**

- `#1A1A1A` background (elevated from main)
- Centered text layout
- App icon with gold box-shadow glow effect
- Larger App Store badge (height: 60px)
- Gold gradient subtle glow behind content

**Step 3: Add Footer HTML**

- `<footer class="footer">`
- App name
- Links: Privacy Policy, Terms of Service, Support
- Copyright: "2025 MasaWata. All rights reserved."
- Close `</main>`, `</body>`, `</html>`

**Step 4: Add Footer CSS**

- Darkest background (#080808 or similar)
- Muted text (#A0A0A0)
- Links: gold on hover
- Centered, simple layout
- Responsive: stack links vertically on mobile

**Step 5: Verify complete page structure**

Scroll through entire page to confirm all sections render correctly.

---

### Task 9: Add JavaScript interactions

**Files:**
- Modify: `IceTimeTrack/js/main.js`

**Step 1: Implement header scroll effect**

- Add/remove `scrolled` class on scroll > 50px
- Use passive event listener

**Step 2: Implement mobile menu toggle**

- Toggle `active` class on nav menu and hamburger button
- Lock body scroll when menu is open
- Close menu when nav link is clicked

**Step 3: Implement FAQ accordion**

- Click handler on `.faq__question` buttons
- Toggle `active` class on parent `.faq__item`
- Close other items when opening one (one-at-a-time behavior)
- Toggle `aria-expanded` attribute

**Step 4: Implement screenshots gallery navigation**

- Prev/Next button click handlers
- Scroll track by fixed amount with `scrollBy` smooth behavior

**Step 5: Implement smooth scroll for anchor links**

- Intercept `a[href^="#"]` clicks
- Calculate target position minus header height
- Smooth scroll to position

**Step 6: Implement scroll animations (AOS-like)**

- IntersectionObserver watching `[data-aos]` elements
- Add `aos-animate` class when element enters viewport
- Unobserve after animation triggers

**Step 7: Verify all interactions**

Open page and test:
- Header effect on scroll
- Mobile menu open/close
- FAQ expand/collapse
- Screenshot gallery navigation
- Smooth scroll navigation
- Scroll reveal animations

---

### Task 10: Final polish and verification

**Files:**
- Modify: `IceTimeTrack/css/style.css` (responsive tweaks)
- Modify: `IceTimeTrack/index.html` (any fixes)

**Step 1: Test responsive breakpoints**

Verify at:
- Desktop (1200px+)
- Tablet (768px-1024px)
- Mobile (480px-768px)
- Small mobile (<480px)

Fix any layout issues found.

**Step 2: SEO checklist verification**

Verify in page source:
- [ ] Single `<h1>`
- [ ] Logical heading hierarchy
- [ ] Meta title and description
- [ ] Open Graph tags
- [ ] Twitter Card tags
- [ ] JSON-LD structured data
- [ ] Canonical URL
- [ ] Alt text on all images/placeholders
- [ ] Semantic HTML5 sections

**Step 3: Accessibility check**

- [ ] All interactive elements are keyboard accessible
- [ ] ARIA labels on buttons
- [ ] Sufficient color contrast (gold on dark)
- [ ] Focus styles visible

**Step 4: Verify complete page**

Open in browser, scroll through all sections, test all interactions at desktop and mobile widths.

```bash
open MasaWata.net/IceTimeTrack/index.html
```
