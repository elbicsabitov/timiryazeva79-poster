# Город ФМ — Apple-Polish Build Plan

**File:** `C:/Users/elbics/Desktop/design-project/designs/gorod-fm.html` (~14.7k lines, single-file SPA)
**North-star:** FIDELITY (shown == real). **Bar:** Apple HIG — Clarity · Deference · Depth. Restraint, premium materials, precise type/spacing, calm.
**One accent:** blue `#5168FC` (large/UI) / `#8094ff` (small text, AA). Green `#34d399` = growth only. Font: Onest only.

Tokens live at `:root` L85–159. This plan supersedes scattered ad-hoc values with ONE coherent system, then applies it surface-by-surface.

---

## 0. THE BAR — Apple design-standard, distilled into a concrete system

Three pillars → web: **Clarity** = type/contrast hierarchy by weight not color; **Deference** = content first, chrome recedes; **Depth** = layered translucent materials + soft *ambient* shadows, never decoration. Add this token system to `:root` and migrate everything onto it.

### 0.1 Type scale (Onest; weights 400/500/600/700 only — retire 800/900 except logo)
```css
--lh-tight:1.08; --lh-snug:1.14; --lh-body:1.45; --track-tight:-0.02em;
/* role            size / line-height   weight  tracking          */
--fs-display: 40px;  /* clamp(32px,5vw,44px) /1.08  700  -0.022em  one hero/screen   */
--fs-h1:      28px;  /* /1.12                700  -0.02em   page title              */
--fs-h2:      21px;  /* /1.18                600  -0.014em  section/card title       */
--fs-h3:      17px;  /* /1.25                600  -0.01em   row/modal title          */
--fs-body:    15px;  /* /1.45                400  0         default                  */
--fs-caption: 13px;  /* /1.4                 400/500  0     meta, 2nd row            */
--fs-micro:   11px;  /* /1.2                 600  +0.04em UPPERCASE  eyebrows/chips   */
```
Rules: **weight does hierarchy, color does not** (never bold + accent same element). Three text tiers, drop secondary to .62 so primary pops:
```css
--text-pri: #fff;
--text-sec: rgba(255,255,255,.62);  /* was .70 */
--text-ter: rgba(255,255,255,.40);  /* keep --text-quat alias */
```
Accent text ≤14px MUST use `--accent-on-dark` (#8094ff), never #5168FC (4.25:1 fails AA). `font-variant-numeric:tabular-nums` on ALL times/stats/counts/durations. Body measure ≤68ch. **No `scaleX()` ever; no all-caps content labels** (uppercase only on `--fs-micro` eyebrows).

### 0.2 Spacing — 8pt grid (4pt half-steps)
```css
--s1:4; --s2:8; --s3:12; --s4:16; --s5:24; --s6:32; --s7:40; --s8:48; --s9:64; --s10:80px;
```
card padding 16 (mobile)/24 (desktop); list-row inner 12 16; section→section 32; major sections 40 (mobile)/64 (desktop); hero/page-bottom 80. `safe-bottom = var(--player-mini-h) + var(--s5)`. Content max-width 736px (reading/forms); wide grid 1064px; page gutter 20px mobile / 32px desktop; grid gutter 24, min tile 168, tile gap 16/24.

### 0.3 Nested radius scale (replace single `--r-base`)
```css
--r-xl:20px;  /* containers/sheets/modals  */
--r-lg:14px;  /* cards, covers             */
--r-md:10px;  /* controls/buttons          */
--r-sm:8px;   /* chips/inputs              */
--r-pill:999px;
```
Child radius ≈ parent − padding. Drop the bespoke 14/9/7px and the `--r-tile-tr:60px` corner on chrome.

### 0.4 Color · Elevation · Material (replace flat white-alpha stacking)
```css
--bg-base: #0B0C0F;            /* FLAT — retire the radial blue-glow default bg */
--surface-0:#111318;  --surface-1:#15171D;  --surface-2:#1B1E26;  --surface-3:#23262F;
--hairline: rgba(255,255,255,.08);  --divider: rgba(255,255,255,.06);  --border-strong: rgba(255,255,255,.14);
--inset-top: inset 0 1px 0 rgba(255,255,255,.05);
--surf-hover: rgba(255,255,255,.10);  --surf-active: rgba(255,255,255,.16);
```
Materials: topbar `blur(20px) saturate(1.2)`; sheets/popover `blur(28px) saturate(1.2)`; full overlays `blur(36px)`. Static panels use `--surface-*` (crisper/cheaper). Keep `@supports not (backdrop-filter)` + add `@media (prefers-reduced-transparency:reduce)` → opaque `rgba(15,16,20,.96)`.

### 0.5 Shadow scale (fix the "halloween" 0 32px 80px /.55 shadows)
```css
--sh-1: 0 1px 2px rgba(0,0,0,.30);
--sh-2: 0 4px 12px rgba(0,0,0,.35);             /* card hover  */
--sh-3: 0 12px 32px -8px rgba(0,0,0,.45);       /* popover/sheet */
--sh-4: 0 24px 56px -16px rgba(0,0,0,.50);      /* modal MAX   */
```
**No colored glow as a container/halo treatment, ever.** Accent lives only in progress bar + play button + active nav cue.

### 0.6 State language
- **Hover (surface):** step one surface tier OR +6% white; `border→--border-strong`; `--sh-2`. translateY only on hero/tiles (`-2px`), never on list rows >120px.
- **Active/press:** `scale(0.98)`, drop to `--sh-1`, 120ms.
- **Selected/accent:** `bg rgba(81,104,252,.14)`, `border rgba(81,104,252,.45)`, text `--accent-on-dark`.
- **Focus-visible (global, ONE color):** `outline:3px solid var(--accent-on-dark); outline-offset:2px`.
- **Icon-ghost hover:** `rgba(255,255,255,.06)`.

### 0.7 Motion (keep easings, tighten durations)
```css
--ease-standard: cubic-bezier(.2,.8,.2,1);
--ease-emphasized: cubic-bezier(.32,.72,0,1);  /* swap overshoot → Apple decel for sheets */
--ease-exit: cubic-bezier(.4,0,1,1);
--d-micro:120ms; --d-std:220ms; --d-emph:340ms;
```
ANIMATE: opacity, transform, background-color, box-shadow, backdrop-filter, height/clip reveals. NEVER: blur radius, list layout width, color of large text bodies. `prefers-reduced-motion` → opacity crossfades 150ms, kill transforms (global guard stays).

### 0.8 Icons
Single-stroke 1.5–2px, `currentColor`, 20–24px box. **No emoji, no ASCII glyphs as icons** (`▶ ✓ ▲ − ✕ → ↑↓ 📌`). Reuse the existing close/play SVG paths.

---

## 1. GLOBAL P0 — app-wide (do FIRST; unblocks every surface)

**G1 — Adopt the §0 token system.** Add all tokens to `:root`. Repoint `--text-sec:.70→.62`. Set `--bg-base` FLAT `#0B0C0F` (keep a localized brand radial ONLY behind the now-playing cover, ≤8%). Add `--brand-blue-hover:#6477ff` (or `color-mix(in oklab,#5168FC,#fff 10%)`).

**G2 — Retire `--brand-cyan` to zero.** It's aliased to #5168FC (renders blue) but is latent debt. Replace every `var(--brand-cyan)` ref → `--brand-blue-light` (rings/borders/progress) or `--accent-on-dark` (small text). Anchors: L33, L195, L326, L429, L1226, L1327, L1466/1468, L1544, L1638/1648/1659. Grep must return 0 on `player-*`/`track-*`/`map-*`/`sidebar-*`.

**G3 — Retire the warm theme entirely.** Remove `--warm-bg` (L117), `.bg-warm` (L265–274), `[data-theme="warm"]{--player-accent:#d19c4f}` (L157–159), and the `applyTheme('warm')` + `_previousTheme` save/restore in `openPlayer()` (L10798–10825). The overlay keeps the cinema palette. This is the single biggest "scary" driver.

**G4 — Remove the dev TWEAKS panel from production DOM (complaint #2).** Don't `display:none` a rendered panel (fidelity lie + a11y tree). Gate boot:
- Add `dev:'gorod-fm.dev'` to `LS_KEYS` (~L10677). Add `hidden` to `<aside id="tweaks-panel">` (~L10489) and `<button id="tweaks-fab">` (~L10658). CSS: `.tweaks[hidden],.tweaks-fab[hidden]{display:none!important}`.
- Boot gate before wiring (~L11030): precedence `?dev=1`/`?dev=0` → `localStorage['gorod-fm.dev']` → **off**. `Ctrl/Cmd+Shift+D` re-toggle. Wrap ALL `.tweak-btn` + collapse/close/FAB wiring (~L11125, incl. `tweaksFab.style.display` L11202/11210) in `if(window.__GFM_DEV){…}`.
- **Critical:** `applyTheme/Surface/HomeVariant/HideFlowMap` persist via `lsSet` and re-init from localStorage (~L11810) — keep that path ALWAYS-ON so prod renders the chosen config with the panel gone. Remove `[data-home-variant]` forks (~L3705); pick ONE canonical home variant.
- Same dev-gate the `#/map` route and the `.sidebar-item-internal` "Карта флоу" footer link.

**G5 — Player redesign (kills "scary"; see §1A).** Apply globally to mini + full.

**G6 — Global slop sweep.** Replace EVERY gradient-placeholder cover/thumbnail (home saved rows L14411, history L8717+/8801, track-history covers, player covers L907/10114/10162+, mini placeholders L606–608, artist track covers, onboarding genre bubbles, map thumbs) with the canonical flat placeholder: `background:var(--surface-1)` + centered Onest monogram (700/15px/#fff) OR a 1.5px-stroke note glyph in `--text-ter`. If real art exists, `<img object-fit:cover>`. **One blue-biased tint only** if identity needed: `hue=210+(hash%40)`, sat ≤40%. No multi-hue, no white orbs, no blurred PNG particle fields, no `scaleX`.

**G7 — Standardize focus-visible** on `--accent-on-dark` everywhere; add explicit `:active{transform:scale(.98)}` to all buttons/cards/rows (gated by reduced-motion). Hit-targets ≥44px (expand small controls via `::before{inset:-9px}` rather than visual growth where needed).

### §1A — PLAYER REDESIGN (mini + full)

**Mini bar (`.player-mini`):**
- height `72px` (`--player-mini-h:72px`; drop the always-on reason ROW, keep ONE `почему?` pill OR a 12px caption — not both; remove the redundant duplicate L639/9920).
- material `rgba(11,12,15,.72) + blur(28px) saturate(1.2)`; top border `1px var(--hairline)`.
- artwork 48px, `--r-sm`, `0 1px 3px rgba(0,0,0,.4), inset 0 0 0 .5px rgba(255,255,255,.08)` — **kill the colored `0 4px 20px var(--np-accent)` glow** (L585).
- title 14/600 `--text-pri`; artist 13/400 `--text-sec`; gap 2px.
- transport prev/play/next only. **Play = filled `--brand-blue-light` 32px circle**, prev/next 32px ghost (no border, `--text-sec`, hover `--surf-hover`), gap 4px. Give play distinct primacy (L718).
- progress 2px, fill **solid** `--np-accent` (no gradient, L572).
- steer: flat single-color disc (no gradient fill, L2942); group share+volume as identical ghost icons.

**Full now-playing (`.player-full`):**
- backdrop `rgba(11,12,15,.6) blur(36px)`; **inset window** (not full-bleed): `max-height:min(880px,92dvh); margin:auto; bg rgba(20,22,28,.7); border 1px var(--hairline)` (NOT 0.4 white, L764–768); `--r-xl`; `--sh-4`. Localized cover-radial only: `radial-gradient(120% 80% at 50% 0%, color-mix(in srgb,var(--np-accent) 12%, transparent), transparent 55%), #0B0C0F`.
- artwork **360px cap** (not 580; fluid `min(360px,72vmin)`), `--r-lg`, `0 24px 60px -20px rgba(0,0,0,.55)`. Real cover or flat placeholder; **delete `::after` radial shimmer**.
- title 26/600 #fff; artist 15/400 `--text-sec`, **no uppercase/tracking** (L999). Lyrics 24/600 inactive `rgba(255,255,255,.32)`, active 700 #fff (drop 38px/#545454, L1032).
- scrubber 4px `rgba(255,255,255,.14)`, fill **solid** `--np-accent` (drop blue→cyan gradient L1226), thumb 12px on hover/focus; times 12px tabular `--text-sec`.
- transport gap **28px** (not 60, L1236); cluster `max-width:280px;margin:auto`. Secondary borderless 44px `--text-sec`→`--text-pri` hover. **Play = 64px solid `--brand-blue-light`**, icon #fff 26px, `0 6px 20px -6px rgba(81,104,252,.5)` (re-skin L1272 glass disc). action-tabs gap 32px, label 13px.
- **Stateful play/pause:** drive mini (L9899 triangle) + full (L10401 bars) + aria-label from ONE `isPlaying` state — they MUST agree (fidelity bug today). Wire into transport handlers L13681.

---

## 2. PER-SURFACE FIXES (P0→P2; dedup of §1 globals noted)

### 2.1 Home / radio surface (`data-page="home"`)
- **P0** Hero colored cover-sampled glow: drop the `--home-np` shadow layer (L2040/2072); neutral depth `0 12px 32px -12px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06)`. *(covered by G3/G5 ethos)*
- **P0** Delete `.home-featured-halo` white orb (rgba .28 blur 22.4px, L1904–1915); depth from card elevation, or dark radial vignette — never white bloom.
- **P0** Off-brand purple: `--featured-cta-bg:#2d2d5d` (L130) → `rgba(11,12,15,.72)+blur(20px)` over image; drop the `!important` route-specific `player-mini` blue tint (L2022) so the player is consistent across routes.
- **P0** TWEAKS / `[data-home-variant]` fork → *G4.*
- **P1** Delete `.home-bg-particles` blurred PNG (L1748–1756); rest on flat `#0B0C0F` or one ≤6% brand radial.
- **P1** Remove all `scaleX(1.05)` + rotated 900-weight tile labels (L1889/1976); horizontal labels in a bottom scrim, weight 700, sentence case.
- **P1** Tokenize raw hero values (`#111318`, radii 20, rgba ladder, fs 22/15/13/11) → §0 tokens. Hero `--r-xl`.
- **P1** Control hierarchy: Skip resting `rgba(255,255,255,.55)`→.85 hover; hover = surface shift (Like .06→.12) not just translateY; keep Steer as the one filled primary.
- **P1** Saved/archive gradient tint swatches (L14411) → *G6.*
- **P2** Genre chips/labels uppercase+tracking → sentence case 15/600 (keep 11px eyebrow uppercase only).
- **P2** Hero markup fidelity: ship ONE real track's art+title+artist+aria-label that match; `paintWhy()` sets art + aria-label together so they never desync (L7505/14310).
- **P2** Hero height guard: `width:min(360px,78vw,42dvh)`; `.home-radio{overflow-y:auto}` so short/landscape doesn't clip controls (L2042/2070).

### 2.2 «Мой вкус» + Сохранённое + streak (`data-page="taste"`)
- **P0** Delete `.taste-row.is-pinned .taste-row-name::after{content:' 📌'}` emoji; SVG pin is the canonical indicator (add `color:#fff` + `inset 2px 0 0 --brand-blue-light` if a name cue is wanted).
- **P0** Remove three production «демо»/«демо-архив» labels from DOM; if needed gate behind `body[data-demo]` as a discreet pill, never inline literal strings.
- **P1** Two identical blue CTAs: keep «Поделиться» filled blue (soften shadow to `0 6px 18px rgba(81,104,252,.28)`); demote «Открытый профиль» to secondary (transparent + `1px var(--border-strong)`, `--text-pri`).
- **P1** Collapse 8 radii → §0 scale (hero `--r-xl`, groups/saved/sponsor 16, chips/rows 12, controls 8).
- **P1** Hover = bg/border/shadow change not lift-only (`.taste-share-btn:hover{background:var(--brand-blue-hover)}`).
- **P1** Saved rows: make real (`role=button`, cursor, hover bg .05, focus ring, click→like/feed) OR drop the affordance + the «Лайк здесь =» claim (honesty).
- **P1** Tokenize one-off hex/rgba (`#14161c/#0c0d12/#eef0f6/#d6dbe8`, rgba ladder) → §0.
- **P1** Name column `flex:0 1 140px;min-width:96px` (~150 desktop) instead of fixed 116px ellipsis.
- **P2** Streak pulsing orb → static growth glyph/ring (run once on enter, settle).
- **P2** Snap scattered margins to 8px; `.taste-stage>*+*{margin-top:24px}`.
- **P2** ctx-chip active = fill + crisp `inset ring` only; drop outer colored drop-glow.
- **P2** taste-pin/taste-ctrl 26px → 44px hit area via `::before{inset:-9px}`; saved-chip min-height 40.
- **P2** Green-meaning: only the «+» growth token green; render «−facet» + «✓ учту» in `--text-sec`/`--accent-on-dark`.
- **P2** Saved tint HSL gradient → flat `rgba(81,104,252,.18)` + monogram, or clamp hue 222–236.

### 2.3 «Открыть» discovery / карта вкуса (`data-page="podborki"`)
- **P0** «Рядом» cards blue→white gradient → flat `rgba(255,255,255,.04)+1px var(--hairline)`; convey closeness via the blue distance pill, hover→`.06` only.
- **P0** track-play 36px → 44px (or 36 visual + 44 tap area).
- **P1** «▶ Запустить как волну» ASCII glyph → inline play SVG, `inline-flex;gap:8px`.
- **P1** Map axis 10.5px `--text-quat` + arrow glyphs → 11px, split each axis into two anchored ends (top/bottom labels), color `--text-sec`; +8px stage inset so labels don't collide rings.
- **P1** Section-title scale: define `.surface-section-title` = 19/700 `-0.01em`; subtitles 13 `--text-sec`. Reserve 800 for the page H2 only.
- **P1** Normalize spacing to 8pt (section-gap 32, title→content 16); wrap page children flex column `gap:32px`.
- **P1** Map nodes 700/13 → 600/12; pill `rgba(11,12,15,.85)+blur(8px)`; at dist=3 show dots only, labels on hover/focus; connector lines `globalAlpha .10`.
- **P1** Primary CTA: hover `background:var(--brand-blue-hover)`+shadow; add `:active{scale(.98)}` to CTA/chips/cards (one `--lift:-2px` token).
- **P1** Radius vocab → §0 (track 12, cards/stage 16/`--r-lg`, pills 999).
- **P1** Tokenize one-off color/alpha; in JS read canvas colors via `getComputedStyle().getPropertyValue('--brand-blue-light')` not hardcoded `#5168FC`.
- **P1** ask-field: add `:hover{border rgba(255,255,255,.18)}` + 3px focus ring `0 0 0 3px rgba(81,104,252,.25)`; shorten placeholder to one example.
- **P2** Fold orientation sentence into axis labels → one persistent explainer (keep «демо-карта»).
- **P2** Empty-taste «Рядом»: one dashed-border onboarding prompt OR «примерно» chip (guessed vs personalized).
- **P2** Curator line `--accent-on-dark` → `--text-sec` grey (reserve blue for action).
- **P2** Compute map geometry once (`layout()→{cx,cy,R}`) shared by canvas + DOM (fidelity).

### 2.4 «Трек deep-dive» (`data-page="track"`)
- **P0** History 12 gradient-placeholder covers → flat tint + monogram (*G6*); delete inline styles (L8717+).
- **P0** Retired cyan leaks (eyebrow L5430, rings L5649/5679/5849, scrubber blue→cyan) → *G2*; scrubber solid `--brand-blue-light`.
- **P0** Player block no focus-visible + cold glass play disc → add `:focus-visible` 3px `--brand-blue-light`; re-skin play to brand fill (*§1A*).
- **P1** Hero cover 480/600 + double shadow + `::after` shimmer → cap 360/280/440, single `0 24px 60px -24px rgba(0,0,0,.6)`, delete shimmer, `--r-lg`.
- **P1** Section headings 20/18/22 mixed → one `.track-why-title` style 19/600 `-0.01em`, 14px bottom margin.
- **P1** Eyebrow: remove `aria-hidden` (carries real info); recolor cyan→`--accent-on-dark`, 600/`+0.08em`.
- **P1** Lyrics inactive `#545454` (3.3:1) → `rgba(235,235,245,.32)` 600; active #fff 700.
- **P1** action-row gap 24/44/60 → 20/32/44; labels 15→12/500; tab gap 6.
- **P2** Delete superseded `.track-cover` gradient block (L5435–5464) + unused `.track-also-*`/`.track-up-next-*`; drop warm gold override.
- **P2** History fake identical `06:45` → plausible durations; add «демо-история» tag.

### 2.5 Артист deep-dive (`data-page="artist"`)
- **P0** Avatar circle + 3px blue ring + radial `::after` sheen → rounded square `--r-xl` 200px, hairline + `0 24px 48px -16px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.06)`; flat top-light (no radial), tint sat 62→40.
- **P0** `.artist-name` 56/900/+0.03em ALL-CAPS → mixed case «Imagine Dragons», 48/700/`-0.02em`/1.05. Drop weight 900 everywhere (monograms ≤800, headings 700). Overline `+0.06em`/600.
- **P1** No material: wrap each section in card `rgba(255,255,255,.03)+1px var(--hairline)+--r-xl+pad 24 28` OR top-hairline divider between sections (pick one).
- **P1** Align hero + sections to one column (`--content-max:920px`,`--gutter:40px` on both).
- **P1** Track-row covers: single neutral `rgba(255,255,255,.06)`, remove per-row `tintFor()` + radial `::after`; radius 10.
- **P1** Tokenize raw rgba/brand-alpha (`--hairline`,`--brand-ghost-bg/border`).
- **P1** Snap rhythm to 8pt (gap 14→16, foot 18→24).
- **P1** Primary CTA `:active{scale(.97)}` + resting `0 8px 24px -8px rgba(81,104,252,.5)`; rows `:active` bg.
- **P1** Dense metadata `--text-quat`→`--text-sec`; bump on row hover (provenance must stay AA).
- **P2** Stations: CSS grid `repeat(auto-fill,minmax(240px,1fr))`, drop fixed 260px.
- **P2** «демо-вектор» badge → quiet 11px caption under H2, neutral, no `cursor:default`.
- **P2** Unify two reject controls into one component, min-height 44.
- **P2** Track rank 24/900 → 15/600 `--text-quat`, width 24 centered.

### 2.6 Онбординг (bubbles + model overlay + import)
- **P0** Genre bubbles full-hue radial gradients → single flat material `radial-gradient(120% 120% at 30% 25%, #1b1d24, #121318)+1px rgba(255,255,255,.10)`; differentiate ONLY by selected blue ring; remove `--hue`/`hashHue`/`GENRE_HUE`.
- **P0** Selected-bubble 4-layer neon shadow → `0 0 0 2px var(--bg-base), 0 0 0 4px var(--brand-blue-light), 0 8px 24px rgba(0,0,0,.45)`; drop one bg decoration layer (keep radial OR particles@.35/blur60, not both).
- **P1** Same header scaffold on all 3 steps (static spark badge + optional kicker + h2); add spark to `#onb-import-pick`.
- **P1** `– + ✕` text glyphs → consistent 16px stroked SVGs (reuse `#resume-close` X path).
- **P1** `.onb-src` radius 10 → match rows 13 (`--r-card:13px`); `.onb-title` 900→800 (presence via size/tracking).
- **P1** Count number + vec bar to `--accent-on-dark`; `.onb-vec-fill` gradient → solid `--brand-blue-light`.
- **P2** One register end-to-end (recommend formal «вы»); rewrite model sub + provText + why-literals.
- **P2** Two stacked «или…» underlined links → ONE quiet «Другой способ собрать вкус» sheet; drop underline + accent so CTA wins.
- **P2** `.onb-vec-name` fixed 116px → `flex:1 1 auto;ellipsis;min-width:88px`, or controls on 2nd line.
- **P2** Optional: swap AI-sparkle for a calmer brand mark; align badge radius to `--r-card`.

### 2.7 recap + profile (`#/recap`, `#/profile`)
- **P0** Tokenize surfaces/radii/borders (raw `#111318` vs `rgba(255,255,255,.03)`, 5 radii, 6 alphas) → `--surface-1`, §0 radius scale, `--hairline`/`--border-strong`.
- **P0** `.profile-box--open` `box-shadow:0 0 40px -10px var(--brand-blue-light)` neon glow → `border rgba(81,104,252,.35)` + `inset 0 1px 0 rgba(255,255,255,.04), 0 8px 24px -16px rgba(0,0,0,.6)`.
- **P0** Glyph icons (`✓` receipts L14010/14101, `▲ − → ←` deltas/CTAs) → strip or replace with 14–16px stroked SVGs.
- **P1** `.profile-facet` row affordance: `--r-md` + `:hover/:focus-within{bg rgba(255,255,255,.04)}`, strengthen lower button on hover, min 28px.
- **P1** Unify ONE button component (`--primary/--secondary/--ghost`) + single `--brand-blue-hover` (drop `#6d80ff`); recap row = ONE primary (Сохранить), demote Скопировать to secondary neutral.
- **P1** Lock 6-step type ramp (28/22/17/15/13/11); section headings 800→650-700; `-0.01em` on large.
- **P1** Reconcile column widths (profile 1000→~860px) + 8pt section spacing on both; bottom padding ~96–120 to clear player.
- **P1** Reserve intrinsic space for JS-injected blocks (`.recap-screen-bloom{min-height:clamp(220px,60vw,300px)}`, card-word 2-line min) + render empty-state strings in markup (no layout jump).
- **P2** Faux competitor: 3 varied-width bars + diagonal lock texture (reads "redacted" not "loading").
- **P2** Share-card: demote green delta to neutral name + small green «+» (card = blue+neutrals only).
- **P2** Remove profile kicker-dot glow; one shared `.gf-kicker-dot` no shadow.
- **P2** Focus-visible → `--accent-on-dark` everywhere (*G7*).
- **P2** recap-card add `inset 0 1px 0 rgba(255,255,255,.06)` top-light + hairline `.10`.

### 2.8 Sidebar + tabbar + topbar
- **P0** TWEAKS panel + cog FAB → *G4* (dev-gate, absent in prod).
- **P0** Active nav = white wash, no accent → 3px blue left-rail `inset 3px 0 0 var(--brand-blue-light)` + `rgba(81,104,252,.12)` fill + label #fff/600; hover stays neutral `--surf-hover`.
- **P1** Drop `filter:brightness()` hovers (search/account/FAB) → explicit `--surf-hover`/`--surf-active` bg transitions.
- **P1** Sidebar rows: 34px icons + 28px gap + 80px rows → horizontal `flex-direction:row;gap:12px;min-height:44px;padding:10px 12px`; icons 22px/1.75 stroke; `.sidebar-nav{gap:4px}` (`--nav-w:232px`).
- **P1** Unify IA labels across surfaces: canon Волна / Мой вкус / Открыть (+ Плеер mobile); same word + same icon per route; resolve taste/«Избранное» duplication.
- **P1** Remove `--brand-cyan` logo hovers (*G2*); wordmark doesn't recolor (use `opacity .85` if any).
- **P1** TWEAKS row (if kept for internal): segmented grid `repeat(auto-fit,minmax(0,1fr))`, short labels.
- **P2** Tabbar split hover (`--text-sec`) vs active (`--brand-blue-light`/600 + 3px top indicator); give player tab a route so exactly one is active.
- **P2** Topbar: add left-anchored contextual page title for balance OR shrink to a floating top-right cluster; scrim = scroll-tied single fade.
- **P2** Tokenize tweaks-header-btn radius (→8) + icon 16; tabbar label 10→11; drop the `--r-tile-tr:60px` corner on the settings card.
- **P2** Dev-gate «Карта флоу» footer link; rename theme toggle to user copy «Тема: Кино» (not raw «Cinema / Warm»).

### 2.9 Legacy `#/map` + `#/lives`
- **P0** `#/map` fake-UI SVG-silhouette + gradient thumbs (incl. 3-stop purple→amber L7394/7453) → **dev-gate the whole route** (it's self-labeled internal). If kept: real screenshots `object-fit:cover` or text-only cards.
- **P0** `#/lives` dead cards (no handler) → wire delegated click→`openPlayer()/setActiveStation()` driven by `STATION_TRACKS` (shown==real), OR convert `<button>`→`<article>` non-interactive + «скоро» state.
- **P0** `#/lives` LIVE pill hardcoded `#ff3b30` red → neutral glass pill + `--accent-on-dark` text + small pulsing blue dot (or keep a tiny 6px dot only).
- **P1** Tokenize map/lives raw values (radii→`--r-lg`, `--hairline`, `--sh-2`); SVG fills via `currentColor`/var.
- **P1** map focus/hover cyan → blue (*G2*).
- **P1** `▶ Открыть` glyph badge → inline SVG; re-tone to glass + hairline.
- **P1** Headings `scaleX(1.05)` + 900 + uppercase → drop scaleX, 700/`-0.02em`/sentence case; card-name 600.
- **P1** `#/lives` magic `margin-top:32px` → LIVE pill in a flex header row; clean fixed stack.
- **P1** Remove `#/map` internal badges/quick-chips/«скрыть в проде» subhead (scaffolding language).
- **P2** map weight spread 400/500/900 → 600/400/700; harmonize the two grids/paddings onto one token.

---

## 3. SEQUENCED EXECUTION (single-file build order)

Atomic commit per step; `?v=N` cache-bust; verify in Chrome between steps; re-grep anchors before each edit (file shifts).

1. **Tokens (§0 → :root).** Add type/space/radius/surface/shadow/state/motion tokens + `--brand-blue-hover`; flatten `--bg-base`; `--text-sec→.62`. *Foundation; nothing else lands cleanly first.*
2. **G2 cyan-retire** across all selectors → grep == 0.
3. **G3 warm-theme removal** (tokens + `.bg-warm` + openPlayer switch).
4. **G4 TWEAKS dev-gate** + remove `[data-home-variant]` fork + dev-gate `#/map` route & «Карта флоу» link.
5. **§1A Player redesign** (mini 72px + full inset window + solid progress + stateful play/pause). *Directly answers "scary".*
6. **G6 global slop sweep** — one canonical flat placeholder helper; replace every gradient/orb/particle/scaleX across home, taste, discover, track, artist, onboarding, map, player.
7. **G7 focus/active/hit-target** global pass.
8. **Per-surface P0s** in nav order: 2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6 → 2.7 → 2.8 → 2.9 (most are now thin after globals).
9. **Per-surface P1s** same order (type scale, tokenize, hover/active, spacing, radius).
10. **Per-surface P2s** (copy register, micro-polish, empty states, fidelity tweaks).
11. **Final verify:** grep `--brand-cyan`/`scaleX`/`linear-gradient(...placeholder)`/emoji-glyph == 0 on product surfaces; Chrome pass each route at desktop + 740px-tall landscape + mobile; confirm play/pause agreement, AA on small accent text, 44px targets, focus rings, prod render with TWEAKS gone.
