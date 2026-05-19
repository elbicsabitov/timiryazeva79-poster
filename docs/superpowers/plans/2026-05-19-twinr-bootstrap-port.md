# Twinr Liquid Glass → Bootstrap 5.3 Port — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `designs/twinr-liquid-glass.html` (Twinr «Большой Цифровой», 21 pages + 11-tool AI module + Liquid Glass Customizer, sunset/dawn themes) as a clean Bootstrap 5.3 dev-handoff project `twinr-bootstrap/`, pixel-faithful to the original.

**Architecture:** Bootstrap 5.3 = structural substrate; Liquid Glass system layered above via CSS cascade layers (`@layer reset, bootstrap, tokens, glass, widgets, utilities`) + `--bs-*` overrides — zero `!important`. Vite 6 + SCSS 7-1 + token SSOT + Nunjucks. Runtime stays hash-SPA (single-file standalone buildable). Adds two Twinr-only subsystems absent from CRM: **dawn/sunset color modes** and the **Liquid Glass Customizer** + AI chip-nav.

**Tech Stack:** Bootstrap 5.3.8 (SCSS source, exact pin), Vite ^6, sass ~1.99, Nunjucks, stylelint-config-twbs-bootstrap, Prettier, self-hosted Onest.

**Spec:** `docs/superpowers/specs/2026-05-19-bootstrap-conversion-design.md`
**Source of truth (visual):** `C:\Users\elbics\Desktop\design-project\designs\twinr-liquid-glass.html` — never edit; fidelity reference.

> This plan is **self-contained and executable independently** of the CRM plan (parallel worktree agents). Phases 0–3 mirror the CRM scaffold (proven-identical architecture) with full code reproduced here; Phases 4–5 add the Twinr-only deltas in full.

---

## Conventions

Same as the CRM plan: per-task gate = `npm run build` green + `npm run css-lint` green + zero console errors + `compound-engineering:design:design-implementation-reviewer` screenshot-diff vs the matching `#page-*` in `twinr-liquid-glass.html` (no HIGH findings). Work in an isolated worktree. Token values transcribed **verbatim** from the prototype `:root` (lines 17–131 + customizer control tokens lines 2231–2265). Screen-porting tasks are procedure-driven by explicit design with an objective gate (see Task 40).

## File Structure (locked)

```
twinr-bootstrap/
├── package.json package-lock.json vite.config.js postcss.config.js
├── .nvmrc .browserslistrc .editorconfig .gitignore .stylelintrc.json .prettierrc.json
├── README.md CONTRIBUTING.md
├── src/
│   ├── pages/twinr/index.njk           # all 21 + AI + guide as data-page sections
│   ├── templates/{layouts,partials,macros}/
│   ├── scss/
│   │   ├── main.scss
│   │   ├── tokens/{_colors,_typography,_glass,_space-radii,_maps}.scss
│   │   ├── abstracts/_mixins.scss
│   │   ├── base/{_index,_backdrop,_fonts}.scss
│   │   ├── layout/{_index,_shell}.scss
│   │   ├── components/{_index,_bs-resurface,_modal-glass}.scss
│   │   ├── themes/_index.scss          # sunset + dawn (DELTA vs CRM)
│   │   └── widgets/_customizer.scss     # Liquid Glass Customizer (DELTA)
│   ├── js/
│   │   ├── main.js bootstrap.js theme.js
│   │   └── modules/{router,table,scroll-reveal,ai-subnav,customizer}.js
│   └── assets/{img,icons,fonts}/
└── styleguide/index.njk
```

---

## Phase 0 — Scaffold (mirror CRM; twinr-named)

### Task 1: package.json + base configs

**Files:** Create `twinr-bootstrap/package.json`, `.nvmrc`, `.browserslistrc`, `.editorconfig`, `.gitignore`

- [ ] **Step 1: `package.json`** (identical to CRM except name/description/standalone filename)

```json
{
  "name": "twinr-bootstrap",
  "version": "1.0.0",
  "private": true,
  "description": "Twinr «Большой Цифровой» — Liquid Glass on Bootstrap 5.3 (design handoff)",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview --port 8081",
    "css-lint": "stylelint \"src/scss/**/*.scss\"",
    "format": "prettier --write \"src/**/*.{scss,js,njk}\"",
    "format-check": "prettier --check \"src/**/*.{scss,js,njk}\"",
    "build:standalone": "vite build && node tools/inline-standalone.mjs",
    "test": "npm-run-all css-lint format-check build"
  },
  "dependencies": { "@popperjs/core": "^2.11.8", "bootstrap": "5.3.8" },
  "devDependencies": {
    "autoprefixer": "^10.5.0", "glob": "^11", "npm-run-all": "^4.1.5",
    "postcss": "^8.5.13", "prettier": "^3", "sass": "~1.99.0",
    "stylelint": "^16.26.1", "stylelint-config-prettier-scss": "^1",
    "stylelint-config-twbs-bootstrap": "^16.1.0", "vite": "^6",
    "vite-plugin-nunjucks": "^0.1", "vite-plugin-singlefile": "^2"
  }
}
```

- [ ] **Step 2:** `.nvmrc` = `20`. `.browserslistrc`, `.editorconfig`, `.gitignore` — byte-identical to CRM plan Task 1 (steps 3–5).
- [ ] **Step 3:** `cd twinr-bootstrap && npm install`; commit `chore(twinr): scaffold package.json + base config`.

### Task 2: vite.config.js + postcss.config.js

- [ ] **Step 1:** `vite.config.js` identical to CRM plan Task 2 Step 1 (the glob/silenceDeprecations config is project-relative — no change). `postcss.config.js` = `export default { plugins: { autoprefixer: {} } }`.
- [ ] **Step 2:** Commit `chore(twinr): vite 6 MPA + autoprefixer + sass deprecation silence`.

### Task 3: lint/format config

- [ ] **Step 1:** `.stylelintrc.json` + `.prettierrc.json` byte-identical to CRM plan Task 3.
- [ ] **Step 2:** Commit `chore(twinr): stylelint + prettier config`.

---

## Phase 1 — Tokens SSOT (with dawn/sunset — DELTA)

### Task 4: Extract `:root` tokens verbatim (incl. dawn + customizer control tokens)

**Files:** Read `twinr-liquid-glass.html` lines 17–131 (`:root` + `[data-theme="dawn"]`) and 2231–2265 (customizer control tokens). Create `tokens/_colors.scss`, `_typography.scss`, `_glass.scss`, `_space-radii.scss`.

- [ ] **Step 1:** `tokens/_colors.scss`, `_typography.scss`, `_glass.scss`, `_space-radii.scss` — same structure as CRM plan Task 4 (glass ladder, blur ladder, spec-rim, ink, accents, radii, shadow, ease, dur, sidebar widths) transcribed from THIS prototype. Add Twinr-only: `$ds-glass-highlight: rgba(255,255,255,.32); $ds-glass-highlight-strong: rgba(255,255,255,.48);` and `$ds-dur` adds `slow: 600ms`.
- [ ] **Step 2:** Create `tokens/_dawn.scss` capturing the `[data-theme="dawn"]` overrides verbatim (frosted-white glass, darker coral `#E05A3A`, light shadow):

```scss
$ds-dawn: (
  glass-bg: rgba(255, 255, 255, 0.52),
  glass-border: rgba(255, 255, 255, 0.68),
  coral: #E05A3A,
  shadow-card: 0 24px 64px -16px rgba(180, 80, 60, 0.18),
  ink-1: #1c1a17,
);
```

- [ ] **Step 3:** Create `tokens/_customizer.scss` capturing the control-token contract (materials/tints/intensity/dim verbatim from lines 2231–2265):

```scss
// Customizer state → CSS var recipe (1:1 with original math)
$dr-materials: (
  ultrathin: (bg: rgba(51,51,51,.18), blur: blur(16px) saturate(140%)),
  thin:      (bg: rgba(51,51,51,.28), blur: blur(24px) saturate(160%)),
  regular:   (bg: rgba(51,51,51,.34), blur: blur(32px) saturate(180%)),
  thick:     (bg: rgba(51,51,51,.50), blur: blur(48px) saturate(200%)),
  chrome:    (bg: rgba(51,51,51,.42), blur: blur(36px) saturate(180%)),
  clear:     (bg: rgba(51,51,51,.08), blur: blur(8px)  saturate(120%)),
);
$dr-tints: (none, coral, blue, indigo, teal, mint, green, yellow, orange, pink, purple, graphite);
$dr-intensity: (0, 0.07, 0.14, 0.22, 0.32); // verbatim math; index = level 0..4
$dr-dim: (none: 0, soft: .14, medium: .26, hard: .40);
```

- [ ] **Step 4:** Commit `feat(twinr): tokens extracted verbatim (incl dawn + customizer control tokens)`.

### Task 5: main.scss @layer skeleton

**Files:** Create `main.scss` + empty partials.

- [ ] **Step 1:** Same `@layer reset, bootstrap, tokens, glass, widgets, utilities;` skeleton + Bootstrap Option-B import order as CRM plan Task 5 Step 2, with these selective-component additions Twinr needs beyond CRM: also `@import 'bootstrap/scss/progress'; @import 'bootstrap/scss/list-group'; @import 'bootstrap/scss/accordion';`. Add `@layer widgets { @import 'widgets/index'; }` and `@layer tokens { @import 'tokens/dawn'; @import 'tokens/customizer'; }` lines.
- [ ] **Step 2:** Create empty partials incl. `widgets/_index.scss`, `widgets/_customizer.scss`. Verify `npx vite build` compiles. Commit `feat(twinr): main.scss @layer skeleton`.

### Task 6: tokens/_maps.scss (Bootstrap bridge)

- [ ] **Step 1:** Same as CRM plan Task 7 (custom colors coral/amber/rose, `$spacers` g14/g24/g28, backdrop-blur utility). Verify build. Commit `feat(twinr): bridge tokens into Bootstrap maps`.

### Task 7: themes/_index.scss — sunset (active) + dawn color modes (DELTA)

**Files:** Modify `themes/_index.scss`.

- [ ] **Step 1:** Emit `--ds-*` like CRM plan Task 8, but split by color mode and wire the toggle:

```scss
:root, [data-bs-theme='dark'] { // sunset (active default)
  /* …all --ds-glass-* / --ds-blur-* / --ds-spec-rim / --ds-ink-* / radii /
     sidebar / ease / dur (incl --ds-dur-slow) — verbatim, same as CRM Task 8 list… */
  --ds-glass-highlight: #{$ds-glass-highlight};
  --ds-glass-highlight-strong: #{$ds-glass-highlight-strong};
}
[data-bs-theme='light'] { // dawn
  --ds-glass-regular: #{map-get($ds-dawn, glass-bg)};
  --ds-glass-thick:   #{map-get($ds-dawn, glass-bg)};
  --ds-glass-border:  #{map-get($ds-dawn, glass-border)};
  --bs-coral:         #{map-get($ds-dawn, coral)};
  --ds-ink-1:         #{map-get($ds-dawn, ink-1)};
}
:root { color-scheme: dark; }
[data-bs-theme='light'] { color-scheme: light; }
```

- [ ] **Step 2:** Verify build; commit `feat(twinr): sunset + dawn color modes via data-bs-theme`.

---

## Phase 2 — Glass layer + component re-surfacing

### Task 8: glass() mixin

- [ ] **Step 1:** `abstracts/_mixins.scss` identical to CRM plan Task 9 (`glass()` + `specular-highlight()`). Commit `feat(twinr): glass() + specular-highlight() mixins`.

### Task 9: Re-surface Bootstrap components

- [ ] **Step 1:** `components/_bs-resurface.scss` identical to CRM plan Task 10 Step 1, **plus** Twinr-only components: `.accordion { --bs-accordion-bg: transparent; --bs-accordion-active-bg: rgba(255,255,255,.04); --bs-accordion-border-color: var(--ds-glass-border); --bs-accordion-btn-color: var(--ds-ink-1); }` and `.list-group { --bs-list-group-bg: transparent; --bs-list-group-color: var(--ds-ink-2); --bs-list-group-border-color: var(--ds-glass-border); }` and `.progress { --bs-progress-bg: rgba(255,255,255,.08); --bs-progress-bar-bg: var(--bs-coral); }`. Verify build. Commit `feat(twinr): re-surface Bootstrap components to glass`.

### Task 10: Backdrop + modal-glass + pitfall guards

- [ ] **Step 1:** `base/_backdrop.scss` (CRM plan Task 11) + `components/_modal-glass.scss` (CRM plan Task 12) reproduced verbatim. The `.app-shell { transform: none !important; }` documented backdrop-root guard applies (spec §5 R1). Verify build. Commit `feat(twinr): backdrop + frosted modal + pitfall guards (R1/R2)`.

### Task 11: Externalize backdrop + self-host Onest + preserve SVG noise textures

**Files:** `src/assets/img/sunset-backdrop.jpg`, `src/assets/fonts/onest-*.woff2`, `base/_fonts.scss`, `base/_noise.scss`.

- [ ] **Step 1:** `cp "C:/Users/elbics/Desktop/design-project/designs/assets/sunset-backdrop.jpg" twinr-bootstrap/src/assets/img/`. Onest woff2 300–800 self-hosted; `base/_fonts.scss` identical to CRM plan Task 13 Step 3.
- [ ] **Step 2:** Extract the two `feTurbulence` noise SVGs (ripple `baseFrequency=0.85`, subtle `baseFrequency=2.4`) from `twinr-liquid-glass.html` lines ~2278–2282 verbatim into `base/_noise.scss` as `--ds-noise-ripple`/`--ds-noise-subtle` data-URL custom properties (used by customizer texture option).
- [ ] **Step 3:** Verify build (assets emit); commit `feat(twinr): externalize backdrop + Onest + preserve noise textures`.

---

## Phase 3 — Shell + JS (with AI subnav — DELTA)

### Task 12: Selective Bootstrap JS + entrypoint

- [ ] **Step 1:** `js/bootstrap.js` = CRM plan Task 14 Step 1 **plus** `import Collapse from 'bootstrap/js/dist/collapse'` (accordion) and export it. `js/main.js`:

```js
import '../scss/main.scss'
import './bootstrap.js'
import './theme.js'
import './modules/router.js'
import './modules/table.js'
import './modules/scroll-reveal.js'
import './modules/ai-subnav.js'
import './modules/customizer.js'
```

- [ ] **Step 2:** Commit `feat(twinr): selective Bootstrap JS + entrypoint`.

### Task 13: theme.js — sunset/dawn toggle (DELTA vs CRM dark-lock)

**Files:** `js/theme.js`.

- [ ] **Step 1:**

```js
const root = document.documentElement
const KEY = 'twinr-theme' // original key; values: 'sunset'|'dawn'
const map = { sunset: 'dark', dawn: 'light' }
function apply(name) {
  root.setAttribute('data-bs-theme', map[name] || 'dark')
  try { localStorage.setItem(KEY, name) } catch {}
}
let saved = 'sunset'
try { saved = localStorage.getItem(KEY) || 'sunset' } catch {}
apply(saved)
document.addEventListener('click', (e) => {
  if (!e.target.closest('[data-theme-toggle]')) return
  const cur = (localStorage.getItem(KEY) || 'sunset')
  apply(cur === 'sunset' ? 'dawn' : 'sunset')
})
```

- [ ] **Step 2:** Commit `feat(twinr): sunset/dawn theme toggle (twinr-theme key parity)`.

### Task 14: router.js (Twinr keys) + table.js + scroll-reveal.js

- [ ] **Step 1:** `js/modules/router.js` = CRM plan Task 16 but `STORE = 'twinr-last-route'`, default `'page-stats'`, **plus** AI-tool memory: when navigating to a `data-page` whose `dataset.aiGroup` is set, also `localStorage.setItem('twinr-last-ai-tool', id)`; clicking sidebar "ИИ" reads `twinr-last-ai-tool` and routes there if present else `page-ai`.
- [ ] **Step 2:** `js/modules/table.js` + `js/modules/scroll-reveal.js` identical to CRM plan Tasks 17–18.
- [ ] **Step 3:** Commit `feat(twinr): hash router (twinr keys + AI-tool memory) + table + reveal`.

### Task 15: AI chip-nav module (DELTA)

**Files:** `js/modules/ai-subnav.js`, `templates/partials/ai-chiprow.njk`.

- [ ] **Step 1:** Recreate the dynamic chip-row: on `hashchange`, if the active `data-page` has `data-ai-group`, render the chip-row (`templates/partials/ai-chiprow.njk` macro listing the 11 tools grouped Контент/Генерация/Медиа/Анализ) below the topbar and mark the active chip; remove it on non-AI pages. Preserve slide-morph indicator (translateX+width on the active chip, `--ds-ease-glass`/`--ds-dur-glass`).

```js
const TOOLS = [ /* {id,label,group} ×11 verbatim from twinr-liquid-glass.html AI hub */ ]
function syncSubnav() {
  const active = document.querySelector('[data-page]:not([hidden])')
  const host = document.getElementById('aiSubnav')
  const isAI = active && active.dataset.aiGroup
  host.hidden = !isAI
  if (!isAI) return
  host.querySelectorAll('.ds-chip').forEach((c) =>
    c.classList.toggle('active', c.dataset.tool === active.id))
  // slide-morph: position indicator under .ds-chip.active
  const a = host.querySelector('.ds-chip.active')
  if (a) host.style.setProperty('--ind-x', a.offsetLeft + 'px'),
         host.style.setProperty('--ind-w', a.offsetWidth + 'px')
}
window.addEventListener('hashchange', syncSubnav)
window.addEventListener('DOMContentLoaded', syncSubnav)
```

- [ ] **Step 2:** Commit `feat(twinr): AI chip-nav (dynamic, slide-morph indicator)`.

### Task 16: App shell (sidebar+offcanvas+sticky topbar+theme toggle+AI subnav slot)

- [ ] **Step 1:** `templates/layouts/base.njk` (CRM plan Task 20 Step 1 but `data-bs-theme` set by `theme.js`, lang ru, title Twinr), `partials/sidebar.njk` with Twinr's items (Рекламный кабинет / Статистика / Wordstat / ИИ / Руководство + auth) 1:1, `partials/topbar.njk` incl. `[data-theme-toggle]` sun/moon, `layouts/twinr-shell.njk` adding `<div id="aiSubnav" hidden>{% include 'partials/ai-chiprow.njk' %}</div>` between topbar and `<main>`. `layout/_shell.scss` identical dims to CRM plan Task 20 Step 5 (sidebar 72→248, sticky topbar, `.offcanvas{z-index:1100}`).
- [ ] **Step 2:** Verify build + css-lint green; commit `feat(twinr): app shell + theme toggle + AI subnav slot`.

### Task 17: Shared UI macros

- [ ] **Step 1:** `templates/macros/ui.njk` — CRM plan Task 21 set **plus** `accordion()`, `tabs3()` (advertiser 3-tab: Реквизиты/Кампании/Ролики), `aiToolCard()`, `chip()`. Commit `feat(twinr): shared UI macros (+accordion/tabs3/aiToolCard)`.

---

## Phase 4 — Liquid Glass Customizer (the crown jewel — DELTA)

### Task 18: Customizer SCSS (widgets/_customizer.scss)

**Files:** `src/scss/widgets/_customizer.scss`.

- [ ] **Step 1:** Recreate the fixed bottom-right panel (300px desktop; full-width <768px), scroll area, collapse state — visual 1:1 with `twinr-liquid-glass.html` lines 2427–2657. Drive the live preview element via `--dr-*` custom props that resolve from the control tokens in `tokens/_customizer.scss`. Segmented controls (material/dim), swatch grid (12 tints), range (intensity 0–4), preset chips — styled as `.ds-*` (not stock Bootstrap) to match original.
- [ ] **Step 2:** Verify build; commit `feat(twinr): Liquid Glass Customizer styles`.

### Task 19: Customizer JS (modules/customizer.js) — exact math 1:1

**Files:** `src/js/modules/customizer.js`.

- [ ] **Step 1:** Port the original logic verbatim. State `{material,tint,intensity,dim,shape,texture,collapsed}`; `apply()` sets `data-*` on `.guide-layout` and recomputes CSS vars with the **exact** original intensity math; 5 presets (DEFAULTS, Material Thin, Teal Tint, Dim Soft, Chrome) as full state snapshots; Copy-CSS reads computed `.droplet` style → clipboard with feedback; Reset; Collapse; persist to `localStorage['twinr-lg-state']`.

```js
const KEY = 'twinr-lg-state'
const INTENSITY = [0, 0.07, 0.14, 0.22, 0.32] // verbatim
const PRESETS = {
  DEFAULTS:       { material:'regular', tint:'none', intensity:0, dim:'none', shape:'rounded', texture:'none' },
  'Material Thin':{ material:'thin',    tint:'none', intensity:0, dim:'none', shape:'rounded', texture:'none' },
  'Teal Tint':    { material:'thin',    tint:'teal', intensity:3, dim:'soft', shape:'rounded', texture:'none' },
  'Dim Soft':     { material:'regular', tint:'none', intensity:0, dim:'soft', shape:'rounded', texture:'none' },
  Chrome:         { material:'chrome',  tint:'none', intensity:0, dim:'none', shape:'pill',    texture:'none' },
}
let state = { ...PRESETS.DEFAULTS }
try { Object.assign(state, JSON.parse(localStorage.getItem(KEY) || '{}')) } catch {}
const layout = () => document.querySelector('.guide-layout')
function apply() {
  const el = layout(); if (!el) return
  for (const k of ['material','tint','dim','shape','texture']) el.dataset[k] = state[k]
  el.dataset.tintIntensity = state.intensity
  el.style.setProperty('--dr-tint-a', INTENSITY[state.intensity])
  try { localStorage.setItem(KEY, JSON.stringify(state)) } catch {}
}
document.addEventListener('click', (e) => {
  const m = e.target.closest('[data-cz-material]'); if (m) { state.material = m.dataset.czMaterial; return apply() }
  const t = e.target.closest('[data-cz-tint]');     if (t) { state.tint = t.dataset.czTint; return apply() }
  const d = e.target.closest('[data-cz-dim]');       if (d) { state.dim = d.dataset.czDim; return apply() }
  const p = e.target.closest('[data-cz-preset]');    if (p) { state = { ...PRESETS[p.dataset.czPreset] }; return apply() }
  if (e.target.closest('[data-cz-reset]'))   { state = { ...PRESETS.DEFAULTS }; return apply() }
  if (e.target.closest('[data-cz-collapse]')){ document.querySelector('.lg-customizer')?.classList.toggle('is-collapsed'); }
  if (e.target.closest('[data-cz-copy]'))    { copyCss() }
})
document.addEventListener('input', (e) => {
  const r = e.target.closest('[data-cz-intensity]')
  if (r) { state.intensity = Number(r.value); apply() }
})
function copyCss() {
  const el = layout(); if (!el) return
  const cs = getComputedStyle(el)
  const css = `.droplet{background:${cs.getPropertyValue('--dr-bg')||cs.background};` +
    `backdrop-filter:${cs.backdropFilter};border:1px solid var(--ds-glass-border);` +
    `box-shadow:var(--ds-spec-rim);}`
  navigator.clipboard?.writeText(css)
  document.querySelector('[data-cz-copy]')?.classList.add('copied')
  setTimeout(() => document.querySelector('[data-cz-copy]')?.classList.remove('copied'), 1200)
}
window.addEventListener('DOMContentLoaded', apply)
```

- [ ] **Step 2: Verify (Customizer fidelity gate)** — build + preview; dispatch `design-implementation-reviewer` on `#page-guide` cycling all 5 presets + each material/tint/dim, screenshot-diff vs original. No HIGH.
- [ ] **Step 3:** Commit `feat(twinr): Liquid Glass Customizer logic (exact math 1:1, presets, copy-css)`.

### Task 20: page-guide + first proof screen (page-stats)

- [ ] **Step 1:** Create `src/pages/twinr/index.njk` extending `twinr-shell.njk`. Build `page-stats` (default route) from `twinr-liquid-glass.html#page-stats` via macros/Bootstrap, and `page-guide` (hosts `.guide-layout` + Customizer). All other 19 pages as empty `data-page hidden` stubs.
- [ ] **Step 2: Verify (first + customizer pipeline gate)** — `design-implementation-reviewer` on `#page-stats` and `#page-guide` vs original at 1440/375/768/1024; WCAG AA; console. No HIGH; fix+re-run once.
- [ ] **Step 3:** Commit `feat(twinr): page-stats + page-guide ported (pipeline + customizer PASS)`.

---

## Phase 5 — Screen porting (procedure-driven; per-screen gate)

### Task 40: Lock the mapping table

- [ ] **Step 1:** Create `twinr-bootstrap/docs/PORT-MAPPING.md` = CRM plan Task 30 table **plus** rows: `tabs (Реквизиты/Кампании/Ролики)→Bootstrap Tabs`, `accordion (5 program modules)→Bootstrap Accordion`, `AI hub cards→aiToolCard macro + data-ai-group`, `live preview inputs (#campName→#pvName)→input event binding`, `<tr onclick=hash>→role=button + module`. Same per-screen procedure + gate. Commit `docs(twinr): locked port mapping table`.

### Task 41: Port the remaining 19 pages (grouped; one verify+commit per screen)

Apply Task 40 procedure; one commit per screen; gate = screenshot-diff vs `twinr-liquid-glass.html#page-*` (no HIGH).

- [ ] **Group A — Auth (3):** `page-promo`, `page-login`, `page-register`
- [ ] **Group B — Stats (2):** `page-stats-clips`, `page-stats-detail`
- [ ] **Group C — Admin advertisers (5):** `page-advertisers`, `page-add-advertiser`, `page-advertiser-details` (3-tab), `page-create-campaign` (live preview), `page-bind-clip`
- [ ] **Group D — AI tools (8):** `page-ai` (hub), `page-sources`, `page-prompts`, `page-source-work`, `page-rewrite`, `page-transcribe`, `page-chat`, `page-video-gen` — plus `page-docs`, `page-keywords`, `page-wordstat` (place: 11 AI/analysis sections total; verify each has `data-ai-group` where original groups it)

(21 total = page-stats + page-guide [Task 20] + 19 here.)

---

## Phase 6 — Standalone, docs, final verification

### Task 42: Kitchen-sink styleguide

- [ ] **Step 1:** `styleguide/index.njk` — swatches/type/`.ds-*` states/glass-on-backdrop/forms **plus** Customizer panel demo + dawn↔sunset live toggle. Commit `docs(twinr): kitchen-sink styleguide`.

### Task 43: Standalone build + dev-handoff docs

- [ ] **Step 1:** `tools/inline-standalone.mjs` → one `twinr-bootstrap-standalone.html` (all 21+guide via hash), separate from `npm run build`.
- [ ] **Step 2:** `README.md` (what/why, prereqs, scripts, dir map, "where things live" incl. **Customizer** = `widgets/_customizer.scss`+`modules/customizer.js`, dawn/sunset = `themes/_index.scss`; Sass-deprecation note; pin policy) + `CONTRIBUTING.md` (CRM plan Task 33 content, twinr-named).
- [ ] **Step 3: Verify** `npm run build:standalone` → double-click works, Customizer + theme toggle + AI subnav functional offline.
- [ ] **Step 4:** Commit `docs(twinr): standalone build + README + CONTRIBUTING`.

### Task 44: Full-project fidelity + acceptance pass

- [ ] **Step 1:** `design-implementation-reviewer` over all 21 pages + AI tools + guide + customizer states + styleguide + **both dawn & sunset**; screenshot-diff vs original; WCAG AA; 375/768/1024; console. Fix HIGH/MEDIUM; re-run once.
- [ ] **Step 2:** Verify spec §8 acceptance 1–10 for Twinr (esp. #5: AI module 11 tools + chip-nav + Customizer + sunset/dawn + 4 localStorage keys 1:1). Record in `twinr-bootstrap/docs/ACCEPTANCE.md`.
- [ ] **Step 3:** Commit `test(twinr): full fidelity + acceptance pass`.

---

## Self-Review (results)

**1. Spec coverage:** D1 separate project ✓. D2 Onest ✓ T11. D3/D4/D6 ✓ T1/T2/T5. D5 hash-SPA ✓ T14/T20. §4.1 @layer ✓ T5. §4.2 tokens SSOT incl dawn+customizer ✓ T4/T6/T7. §4.3 markup/JS parity ✓ T12–T17/T40. §4.3 Customizer rewire to setProperty ✓ T19. §4.4 assets/noise/standalone ✓ T11/T43. §4.5 docs ✓ T42/T43. §5 risks R1 ✓ T10, R2 ✓ T10, R3 ✓ T16, Customizer-heaviest ✓ T18/T19 (own gate), AI-subnav ✓ T15, perf/Safari ✓ T8. §6 verification ✓ T20/T44. §8 acceptance ✓ T44.
**2. Placeholder scan:** Screen porting (T41) procedure-driven by explicit design + objective gate (T40), not TODO. TOOLS/icon/macro contracts specify exact source + output. No "TBD/handle edge cases".
**3. Type consistency:** keys `twinr-last-route`/`twinr-last-ai-tool`/`twinr-theme`/`twinr-lg-state` consistent T13/T14/T19. `data-page`/`data-nav`/`data-ai-group`/`data-cz-*` consistent T14/T15/T16/T19/T40. `glass()` sig consistent T8→T9/T16. `--ds-*`/`--dr-*` names consistent T4/T7→T9/T18/T19. PRESETS/INTENSITY math single-defined T19.

---

## Execution Handoff (covers BOTH plans)

Plan complete and saved to `docs/superpowers/plans/2026-05-19-twinr-bootstrap-port.md` (twin: `…-crm-bootstrap-port.md`). Two execution options:

**1. Subagent-Driven (recommended)** — fresh subagent per task, two-stage review between tasks, fast iteration. Maps cleanly to the spec's parallel model: two worktrees (`crm-bootstrap`, `twinr-bootstrap`) advancing concurrently, build/css-lint green gate between merges, sequential merge train to `master`.

**2. Inline Execution** — execute tasks in this session via executing-plans, batch with checkpoints.

**Which approach?**
