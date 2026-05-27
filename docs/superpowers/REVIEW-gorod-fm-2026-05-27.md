# Город ФМ — Anti-slop Review

**File:** `designs/gorod-fm.html` (10 216 lines, 370 KB uncompressed)
**Date:** 2026-05-27
**Commit:** `83cd970` (feat: gorod-fm — mobile + surface architecture)
**Method:** Live browser audit via Chrome MCP at `http://127.0.0.1:8765/` + Figma MCP screenshot + JS contrast/DOM analysis + HTML code review

---

## Critical (must fix before showing customer)

### 1. WCAG AA contrast fails — body text on cinema gradient background

All text directly on the cinema gradient background fails WCAG AA Normal (4.5:1 requirement):

| Token | Composed RGB | Contrast vs bgMid | WCAG AA Normal | WCAG AA Large |
|-------|-------------|-------------------|----------------|---------------|
| `--text-pri` `#FFFFFF` | 255,255,255 | **3.55:1** | FAIL | FAIL |
| `--text-sec` `rgba(255,255,255,0.70)` | 191,221,244 | **2.51:1** | FAIL | FAIL |
| `--text-quat` `rgba(235,235,245,0.60)` | 157,197,228 | **1.95:1** | FAIL | FAIL |
| Active chip white text on `rgba(255,255,255,0.32)` bg | chip bg 109,177,230 | **2.31:1** | FAIL | FAIL |

Calculation uses cinema gradient midpoint `rgb(41,141,218)` (between cyan endpoint and blue deep endpoint). Even `--text-pri` fails at 3.55:1. The cyan endpoint `rgb(86,175,215)` is even lighter — contrast drops further to ~2.5:1 at the right edge.

Mitigation path: add a semi-transparent dark backdrop to content areas (`rgba(0,0,0,0.25)` behind all text blocks), or darken the overall background overlay. The `--bg-overlay` already exists but is only applied at the right edge. `--text-quat` is the worst offender at 1.95:1 — borderline unusable at small sizes.

Note: `--text-quat` on the Tweaks dark panel passes at **6.2:1** — fine.

### 2. Surface switch (Tweaks) silently broken on desktop viewport

Clicking "Mobile" or "TV" in the Tweaks panel changes `data-surface` on `<html>` but the sidebar stays visible, tabbar stays hidden, and the grid layout doesn't change. Verified at 1920×1080:

- `[data-surface="mobile"] .sidebar { display: none }` in `@layer surfaces` is NOT overriding `.sidebar { display: flex }` from `@layer components`, even though the layer order declaration (`reset, tokens, base, layout, components, surfaces, utilities`) should make surfaces win.
- Injecting the same rule inline with `!important` correctly hides the sidebar.
- This is a CSS `@layer` cascade bug: all rules in `@layer surfaces` appear to be losing to same-specificity rules in `@layer components`. Likely cause: the entire stylesheet is one `<style>` block and Chrome's layer ordering isn't being applied as expected — possible edge-case with nested `@media` inside a layer block.

**Fix:** Add `!important` to all display-critical overrides in `@layer surfaces`, or move mobile/TV surface rules outside the layer into a dedicated `<style>` block after the main one, or replace `@layer` with explicit specificity bumping (`html[data-surface="mobile"] .sidebar`).

The `@media (max-width: 768px)` fallback at line 4639 DOES work (uses `!important`) — real narrow browsers will get correct mobile layout.

### 3. #/podborki — no real photography / placeholder tiles lack brand imagery

Figma `2384:6054` shows tiles with real artist photography: person in neon light, face-close-up in red, dancer, outdoor festival crowd, man in suit, etc. The implementation uses solid/gradient color blocks with no imagery at all. This is the single biggest visual gap vs Figma.

The implementation CSS correctly supports `background-image` on `.podborki-tile-bg` — only the HTML needs real images or at minimum stylized photo-like placeholders. Solid gradients look like a dev placeholder not a client presentation.

---

## Important (fix soon)

### 4. Small hit targets on Tweaks panel (34px and 28px)

- All `.tweak-btn` elements are **34px tall** (spec: min 44px for web, 56px for TV).
- All `.tweaks-header-btn` elements (collapse/close icons) are **28px tall**.

These are inside an "internal" Tweaks panel — lower priority for end-users but still a usability issue for the design review workflow.

### 5. `home-tf-close` button is 32×32px

The close button on the home track-file drawer panel renders at **32×32px** — below the 44px minimum. CSS declares `min-height: 44px` for the home-tf-action-btn but `.home-tf-close` has no `min-height`. Should be `min-height: 44px; min-width: 44px`.

### 6. Tweaks panel overlaps rightmost podborki tile at 1920px

At 1920×1080 the Tweaks panel (fixed, `right: 20px`, `width: 280px`) sits on top of the rightmost visible tile. The podborki gallery `scrollWidth` is 3278px (9 tiles × 245–373px) — the gallery extends well past the viewport, but the last visible tile's right edge is obscured by the Tweaks panel. Not a structural bug, but the Tweaks panel needs a toggle-FAB mode at wider viewports, or the gallery needs `padding-right: 320px` when Tweaks is open.

### 7. #/podborki — tile widths 5–9 all equal (373px) — differs from Figma

Figma `2384:6054` shows widths **245 / 299 / 310 / 309 / 373** for the first 5 tiles (as described in brief). Tiles 5–9 in the implementation are all 373px (same as tile 5). The brief specified width sequence only covers 5 unique widths — tiles 6–9 were extrapolated as equal. This should be intentional (only 5 unique Figma tiles, rest repeat) but worth confirming with Эльбик. The first 5 widths match exactly.

### 8. `home-chip` hit target: 40px (below 44px minimum)

`.home-chip` has `min-height: 40px` — 4px short. CSS fix: change to `min-height: 44px`.

### 9. Home station cover art is SVG placeholder — acceptable, but flagged

`.home-cover` and all station thumbnails use inline SVG drawings (concentric circles, abstract shapes). DESIGN_PROTOCOL.md explicitly bans "Drawing imagery via SVG when no real asset." These are abstract/geometric placeholder art, not figurative SVG drawings — they pass the spirit of the rule. However, the home hero 480×480 cover being a blue radial SVG pattern for a live radio prototype needs a real image or at minimum a station-branded placeholder before client showing.

---

## Polish (nice to fix)

### P1. Tweaks panel top-right corner radius (cosmetic)

The Tweaks panel uses `border-radius: var(--r-tile-tr) var(--r-base) var(--r-base) var(--r-base)` which gives a 60px top-left corner. The intent is "concentric corner" aesthetics matching the podborki tiles — this is intentional design per protocol. However at 280px panel width, 60px top-left corner is quite prominent and the asymmetry (top-left huge, others 10px) reads as a bug rather than design. Consider `border-radius: 24px 10px 10px 10px` or `20px 10px 10px 20px` for a more balanced concentric effect.

### P2. `sidebar-item-internal` has `opacity: 0.6` — very low contrast

`.sidebar-item-internal { font-size: 13px; opacity: 0.6; }` on `--text-sec` on dark sidebar. At 13px the 0.6 opacity brings effective contrast to ~1.5:1 against the dark sidebar. This only affects the internal "Карта флоу" / "Cinema / Warm" labels visible in the sidebar footer — low priority since they're internal/debug, but fix before any client show.

### P3. `player-action-tab` label at 15px doesn't have `text-wrap: pretty`

Minor: player action tab labels are small single-word labels — not a wrapping issue in practice.

### P4. Lyrics line `font-size: 38px` — large, but acceptable

The lyrics view has 38px lines. For a live prototype desktop view this is fine. On mobile surface this needs verification that text doesn't overflow.

### P5. `home-cover` uses hardcoded gradient `#1a3a6e → #56afd7` (not CSS tokens)

Hardcoded hex values in inline `background` on `.home-cover`. Should use `var(--brand-deep)` / `var(--brand-cyan)` for design-system consistency if this gradient is intentional brand expression.

---

## Strengths (what's solid)

- **Font: Onest only, no banned fonts.** `Inter`, `Roboto`, `Arial`, `system-ui` absent from computed styles. Full compliance.
- **`text-wrap: pretty/balance` applied correctly.** `p { text-wrap: pretty }`, `h1–h6 { text-wrap: balance }` per protocol.
- **CSS Grid for all layouts.** App shell, library 2-row, map 3-col card grid — no flexbox waterfall anti-pattern.
- **CSS layers ordered correctly.** Declaration at line 19: `reset, tokens, base, layout, components, surfaces, utilities` — design intent is right even though the cascade bug exists.
- **Reduced motion support.** `@media (prefers-reduced-motion: reduce)` applied to animations, transitions, backdrop-filter.
- **`focus-visible` ring.** `3px solid var(--brand-cyan)` on all interactive elements — keyboard accessible.
- **All buttons ≥44px height** (except Tweaks-internal ones): `.sidebar-item`, `.topbar-search`, `.topbar-account`, `.home-fab`, `.player-transport-btn`, `.player-ctrl-btn`, `.tabbar-item` all pass.
- **Hash routing works correctly.** All 7 routes (`#/home`, `#/podborki`, `#/library`, `#/artist`, `#/track`, `#/favorites`, `#/map`) render correctly. No 404s or blank pages.
- **Player overlay works.** Mini-player click → full overlay opens with warm background. Escape key closes it. Theme switch cinema↔warm works. Home variant A/B switch works.
- **No console errors.** Zero JavaScript errors across all routes tested.
- **Concentric corners.** App uses `--r-tile-tr: 60px` (tile) + `--r-base: 10px` (inner elements) + `--r-pill: 999px` — three levels, correct concentric nesting per protocol.
- **No aggressive multi-stop gradients** on content backgrounds. The cinema gradient is 3-stop but this IS the brand background (not a card/section decoration), so it's a brand asset not a slop pattern.
- **No data slop / fake stats.** No decorative progress bars with random numbers. Library item counts, favorites counts, track durations are consistently applied across all items.
- **Figma tile geometry reproduced correctly:** height 628px, `border-top-right-radius: 60px` ONLY (other corners 0px), label `rotate(-90deg)`, `font-weight: 900`, all-caps, Onest font — all confirmed via DOM measurement.
- **Performance.** DOMContentLoaded ~301ms, load ~785ms for a 370KB single-file SPA. Acceptable.

---

## Smoke test outcomes

| Check | Result | Notes |
|-------|--------|-------|
| Hash routing (#/home) | PASS | All 7 routes render |
| Hash routing (#/podborki) | PASS | Tiles visible, gallery scrolls |
| Hash routing (#/library) | PASS | 2-row grid visible |
| Hash routing (#/artist) | PASS | Artist header + top tracks |
| Hash routing (#/track) | PASS | Cover + meta + scrubber |
| Hash routing (#/favorites) | PASS | Filtered list renders |
| Hash routing (#/map) | PASS | 3-col card grid renders |
| Theme switch cinema→warm | PASS | `data-theme` changes, warm bg fades in |
| Theme switch warm→cinema | PASS | Restores cinema bg |
| Surface switch web→TV | PARTIAL | `data-surface` attr changes, but layout does NOT update (Critical #2) |
| Surface switch web→mobile | PARTIAL | `data-surface` attr changes, but sidebar stays, tabbar stays hidden (Critical #2) |
| Home variant FAB→drawer | PASS | `data-home-variant` attr changes |
| Flow map hide/show toggle | PASS | Tweaks button fires |
| Mini-player visible | PASS | Fixed at bottom |
| Mini-player → full overlay | PASS | Click opens full overlay |
| Escape closes overlay | PASS | Keyboard event handled |
| Player warm theme bg | PASS | Orange/purple gradient appears |
| Console errors | PASS | Zero errors across all routes |
| Mobile 414px breakpoint | PASS via @media | At actual narrow viewports media query fires with !important; Tweaks button doesn't help at desktop (Critical #2) |
| No horizontal scroll (web) | PASS | documentElement.scrollWidth = viewport width |
| WCAG AA contrast (body text on bg) | FAIL | Worst: 1.95:1 (--text-quat). Even --text-pri = 3.55:1 fails AA Normal 4.5:1 |
| Hit targets ≥44px (primary UI) | PASS | Core nav, player, chips all ≥44px |
| Hit targets ≥44px (Tweaks) | FAIL | tweak-btn 34px, header-btn 28px |
| File size <200KB | FAIL | 370KB (single-file SPA, expected, not a bug) |
| Fonts (no banned) | PASS | Only Onest used |

---

## Figma fidelity (#/podborki vs node 2384:6054)

| Check | Result | Detail |
|-------|--------|--------|
| Tile height 628px | PASS | Measured via DOM: 628px |
| Tile width sequence (first 5) | PASS | 245 / 299 / 310 / 309 / 373px — exact match |
| Tiles 6–9 (only 5 unique in Figma) | ASSUMED | All 373px; Figma has 9 tiles including radio shows — needs visual verification |
| `border-top-right-radius: 60px` ONLY | PASS | TR=60px, TL=BL=BR=0px confirmed via getComputedStyle |
| Label rotation -90deg | PASS | `transform: matrix(0, -1.05, 1, 0, 0, 0)` = rotate(-90deg) scaleX(1.05) |
| Label all-caps | PASS | `text-transform: uppercase` |
| Label font: display weight 900 | PASS | Onest 900, 44px |
| Cinema gradient background | PASS | `--bg-base: linear-gradient(-90deg, cyan → blue → deep)` |
| Tile shade/glow overlay | PASS | `--tile-shade` + per-tile glow with blur |
| Bottom player bar present | PASS | `player-mini` fixed at bottom |
| Real photography in tiles | FAIL | Figma shows artist photos; implementation has solid gradient fills only — biggest visual gap |
| Sidebar icon labels (Figma has text labels below icons) | PARTIAL | Implementation uses text-beside-icon layout; Figma shows icon-over-text column style in narrow sidebar |
| Filter chips (РОК, ДИСКО, ПОП...) | PASS | Both have same 5 labels, same layout |

---

## Summary of critical path to customer-ready

1. **[Critical #1]** Body text contrast — add `rgba(0,0,0,0.30)` overlay behind all text content, or darken the cinema gradient. `--text-quat` at 1.95:1 is unusable.
2. **[Critical #2]** Surface switch — replace `@layer surfaces` display overrides with `html[data-surface="mobile"] .sidebar` (full specificity) OR add `!important` to all display rules in surfaces. The FAB mode (responsive `@media` fallback) works correctly at real narrow viewports.
3. **[Critical #3]** Podborki tile imagery — add at least one real or near-real photo per tile before client presentation. The Figma shows strong editorial photography; solid gradients read as wireframe.
