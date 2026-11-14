# MasaWata Tech brand assets

The three supplied business-logo files were moved from Downloads on November 14,
2026. Filenames were normalized for web URLs; file contents were preserved and
verified with SHA-256 before and after the move.

## Asset inventory

| File | Supplied filename | Format and dimensions | Suggested role |
| --- | --- | --- | --- |
| [masawata-tech-mark.svg](masawata-tech-mark.svg) | `MasaWata_Tech_Logo_Mark.svg` | Transparent vector; 1024 × 1024 declared size; 1,650 bytes | Primary website monogram: navigation, studio signatures, and source for browser icons |
| [masawata-tech-mark.png](masawata-tech-mark.png) | `MasaWata_Tech_Logo_Mark.png` | Transparent PNG; 1024 × 1024; 44,487 bytes | Raster fallback, organization-logo metadata, and source for exported touch icons |
| [masawata-tech-logo.png](masawata-tech-logo.png) | `MasaWata Tech Interlocking Logo.png` | Opaque PNG; 2172 × 724; 1,110,106 bytes | Full horizontal monogram and wordmark on a cream background; larger studio presentations or source artwork for a social card |

The SVG uses navy `#0B3158` and teal `#08A097`. The horizontal PNG has its own
baked-in background and subtle texture; it is not a transparent wordmark. The
SVG is the preferred compact UI asset.

## Website placement assessment

This is an assessment, not an applied redesign. This import changes no existing
page markup, styling, favicon, touch icon, social metadata, or generated page.
The recommendations below have not been approved as implementation scope.

| Surface | Current observation | Recommendation |
| --- | --- | --- |
| Studio homepage header (`/`) | An older blue square symbol accompanies “MasaWata.” | Highest priority: use the SVG monogram at approximately 28–32 CSS px beside live text “MasaWata Tech,” linked to `/`. Keep the name readable on mobile. |
| Studio homepage hero | A compact studio eyebrow introduces the main app-focused headline. | Keep the headline as text. The full horizontal PNG could become a single larger brand presentation on a matching light surface, but it is optional; the header already establishes identity. Avoid repeating a large lockup in both header and hero. |
| Studio homepage footer | Text identifies MasaWata Tech without a logo. | Add a modest SVG and live studio name alongside the existing studio description and links. |
| Shared studio privacy page (`/privacy-policy.html`) | Its home link repeats the older blue symbol. | Use the same compact monogram/name treatment as the homepage. Preserve the policy text and effective date. |
| Studio browser and touch icons | Root `favicon.svg` and `apple-touch-icon.png` represent the older identity. | Derive icons from the monogram. Give the navy portion a light backing so it remains visible in dark browser chrome. Test the diagonal negative space at small sizes before replacing the favicon. |
| Studio social previews | The homepage currently reuses its touch icon for Open Graph and Twitter images; the shared privacy page has no social image. | Create a deliberate studio share image using the monogram or horizontal logo with adequate margins. The supplied 3:1 PNG needs composition for the chosen card shape, rather than an automatic crop. |
| Organization structured data | The homepage's `Organization.logo` points to the older favicon. | Point the organization logo to a stable business-logo asset, with the 1024 px PNG as a practical raster choice. Keep application icons and screenshots associated with their respective products. |
| All seven product sites and their locale routes | Each product header uses its app icon. Six product sites have no studio homepage link; Car Plate Scan already has text links in its navigation and footer. | Add one small monogram plus “By MasaWata Tech” studio signature linking to `/` in the shared footer. Keep each product's app identity prominent in its header, browser icon, screenshots, and product social images. Upgrade Car Plate Scan's existing footer studio link instead of duplicating it. |
| Car Plate Scan navigation | A text-only “MasaWata” link already returns to the studio. | Optionally pair that existing secondary link with a small monogram if mobile spacing allows. The footer signature is sufficient if the navigation becomes crowded. |
| Soccer Time Track support and product privacy pages | Their footers already say “By MasaWata Tech” and include a studio link. | Enhance the existing publisher link with a small monogram. Keep the Soccer Time Track app icon and product name. |
| App event and deep-link fallback pages | These pages use several independent templates and prioritize the app, event artwork, and open/download actions. | A small studio signature near the bottom is appropriate where space allows. Keep it secondary to the event and app-opening actions; do not overlay it on event illustrations or replace app artwork. Reuse an existing studio link where present. |
| Legacy redirects, 404 routing, verification files, AASA, crawl files, and app-ads.txt | These serve routing, machine-readable, or verification roles. | No additional visible logo placement is needed. |

The strongest first use is the studio header and root icons, followed by a
consistent publisher signature across the product footers. The full horizontal
PNG is useful brand artwork, but does not need to be loaded on every page merely
because it is available.

## Appearance and accessibility considerations

- Preserve the supplied monogram proportions and diagonal negative space. Keep
  these originals intact if optimized or derived exports are introduced later.
- The navy portion can disappear into dark backgrounds. This affects the studio
  site's automatic dark appearance and the dark Ice Time Track, Soccer Time Track,
  and Car Plate Scan sites. A small light backing is the most direct way to use
  the supplied colors consistently; do not silently recolor the originals.
- The horizontal logo's cream rectangle and texture will be visible against pure
  white or dark page backgrounds. Use it as deliberate artwork on a matching
  surface. For navigation, SVG plus live text scales more naturally.
- Keep “MasaWata Tech” as the business identity across the site; preserve app names
  and their individual color systems. The studio's blue accent could later be
  reconsidered alongside the navy/teal palette, but that is a separate design choice.
- Where visible text already names the business, use an empty image alternative
  and let the link text name the destination. A logo-only link needs an accessible
  name such as “MasaWata Tech home.” Keep visible keyboard focus and a comfortably
  sized link target even when the mark is small.
- Specify image dimensions to reserve layout space. At narrow widths, allow footer
  content to wrap and retain the complete business name. For localized pages, keep
  the business name intact and translate any added “By” wording as appropriate.

## Assessment coverage and source locations

Repository inventory at assessment time: 180 generated product documents across
seven sites, 22 event documents, two independent product support/legal documents,
three root HTML documents, 21 redirects, and two HTML includes. The counts describe
source inventory, not a claim of individual visual review of every locale.

Live browser review covered the homepage, all seven English product pages, shared
privacy, Soccer Time Track support and privacy, Car Plate Scan's Analysis event,
and Fitness Story's Health event. Representative screenshots included light and
dark product footers. Mobile layouts and proposed logo placements have not been
rendered or validated; existing page source and styles informed those recommendations.

- [`../../index.html`](../../index.html): studio header/footer, social metadata, organization schema.
- [`../../privacy-policy.html`](../../privacy-policy.html): shared studio legal-page branding.
- [`../../favicon.svg`](../../favicon.svg) and [`../../apple-touch-icon.png`](../../apple-touch-icon.png): existing root icons.
- [`../../scripts/asc_web.py`](../../scripts/asc_web.py): shared renderer for all seven product sites and their locales.
- [`../../includes/asc-localized.css`](../../includes/asc-localized.css): shared product header/footer styles.
- Each app's `build.py`: invokes the shared renderer; generated locale HTML is output, not the primary place for shared branding changes.
- `SoccerTimeTrack/support.html`, `SoccerTimeTrack/privacy-policy.html`, and the apps' `event/` directories: independent pages outside that shared renderer.

No new raster exports, theme variants, or social cards were created as part of the
asset move and assessment.
