# CRM Glass → Bootstrap 5.3 Port — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `designs/crm-glass.html` (Turbo Performance CRM, 29 screens, dark-only Liquid Glass) as a clean Bootstrap 5.3 dev-handoff project `crm-bootstrap/`, pixel-faithful to the original.

**Architecture:** Bootstrap 5.3 is the structural substrate (grid, utilities, JS plugins); the Liquid Glass design system sits above it via CSS cascade layers (`@layer reset, bootstrap, tokens, glass, widgets, utilities`) and `--bs-*` custom-property overrides — zero `!important`. Vite 6 + SCSS 7-1 + design-token SSOT + Nunjucks templating; runtime stays hash-SPA so a single-file standalone preview is still buildable.

**Tech Stack:** Bootstrap 5.3.8 (SCSS source, exact pin), Vite ^6, sass ~1.99, Nunjucks (vite-plugin-nunjucks), stylelint-config-twbs-bootstrap, Prettier, self-hosted Onest font.

**Spec:** `docs/superpowers/specs/2026-05-19-bootstrap-conversion-design.md`
**Source of truth (visual):** `C:\Users\elbics\Desktop\design-project\designs\crm-glass.html` — never edit; it is the fidelity reference.

---

## Conventions for this plan

- **The "test" for a faithful port** is objective and gated, not unit-test-shaped. Per task the acceptance gate is: (1) `npm run build` green, (2) `npm run css-lint` green, (3) zero console errors, (4) **screenshot-diff vs the matching `#page-*` in the original `crm-glass.html`** via the `compound-engineering:design:design-implementation-reviewer` agent — no HIGH findings. Where a step says "Verify", run that gate.
- Work happens in an isolated git worktree (created via `superpowers:using-git-worktrees` at execution time). All paths below are relative to that worktree root unless absolute.
- The original prototype's `:root` token values are reproduced **verbatim**. Token tables in the spec §4.2 list names; exact values are read out of `crm-glass.html` lines 17–82 during Task 4 and transcribed 1:1.
- Screen-porting tasks (Phase 5+) are **procedure-driven by design**: each screen's DOM is read from the original and rebuilt through the fixed mapping table (Task 30). This is not a placeholder — it is the only honest representation of mechanical 1:1 port work, and every screen has a hard, objective verification gate.

## File Structure (locked decomposition)

```
crm-bootstrap/
├── package.json                       # deps + scripts (Task 1)
├── package-lock.json                  # committed; npm ci (Task 1)
├── vite.config.js                     # MPA glob input + silenceDeprecations (Task 2)
├── postcss.config.js                  # autoprefixer (Task 2)
├── .nvmrc .browserslistrc .editorconfig .gitignore        # (Task 1)
├── .stylelintrc.json .prettierrc.json                      # (Task 3)
├── README.md  CONTRIBUTING.md         # dev-handoff docs (Task 33)
├── src/
│   ├── pages/crm/<screen>.njk         # 29 screens (Phase 5)
│   ├── templates/
│   │   ├── layouts/base.njk           # html/head, asset links (Task 6)
│   │   ├── layouts/crm-shell.njk      # sidebar+topbar shell (Task 20)
│   │   ├── partials/{sidebar,topbar,icons}.njk   (Task 19-20)
│   │   └── macros/ui.njk              # card/table/modal macros (Task 21)
│   ├── scss/
│   │   ├── main.scss                  # @layer skeleton + Option-B import order (Task 5)
│   │   ├── tokens/{_colors,_typography,_glass,_space-radii,_maps}.scss   (Task 4,7)
│   │   ├── abstracts/_mixins.scss     # glass() mixin (Task 9)
│   │   ├── base/_index.scss
│   │   ├── layout/_index.scss         # shell, sidebar, topbar (Task 20)
│   │   ├── components/_index.scss     # .ds-* glass components (Task 10-12)
│   │   ├── pages/_index.scss
│   │   └── themes/_index.scss         # [data-bs-theme=dark] --ds-* (Task 8)
│   ├── js/
│   │   ├── main.js                    # imports scss + bootstrap.js + modules (Task 14)
│   │   ├── bootstrap.js               # selective plugin imports (Task 14)
│   │   ├── theme.js                   # data-bs-theme + localStorage (Task 15)
│   │   └── modules/{router,table,modal-glass,scroll-reveal}.js   (Task 16-18)
│   └── assets/{img,icons,fonts}/      # externalized backdrop + Onest (Task 13)
└── styleguide/index.njk               # kitchen-sink gallery (Task 32)
```

---

## Phase 0 — Project scaffold

### Task 1: Initialize project + base config files

**Files:**
- Create: `crm-bootstrap/package.json`
- Create: `crm-bootstrap/.nvmrc`, `.browserslistrc`, `.editorconfig`, `.gitignore`

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "crm-bootstrap",
  "version": "1.0.0",
  "private": true,
  "description": "Turbo Performance CRM — Liquid Glass on Bootstrap 5.3 (design handoff)",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview --port 8080",
    "css-lint": "stylelint \"src/scss/**/*.scss\"",
    "format": "prettier --write \"src/**/*.{scss,js,njk}\"",
    "format-check": "prettier --check \"src/**/*.{scss,js,njk}\"",
    "build:standalone": "vite build && node tools/inline-standalone.mjs",
    "test": "npm-run-all css-lint format-check build"
  },
  "dependencies": {
    "@popperjs/core": "^2.11.8",
    "bootstrap": "5.3.8"
  },
  "devDependencies": {
    "autoprefixer": "^10.5.0",
    "glob": "^11",
    "npm-run-all": "^4.1.5",
    "postcss": "^8.5.13",
    "prettier": "^3",
    "sass": "~1.99.0",
    "stylelint": "^16.26.1",
    "stylelint-config-prettier-scss": "^1",
    "stylelint-config-twbs-bootstrap": "^16.1.0",
    "vite": "^6",
    "vite-plugin-nunjucks": "^0.1",
    "vite-plugin-singlefile": "^2"
  }
}
```

- [ ] **Step 2: Create `.nvmrc`**

```
20
```

- [ ] **Step 3: Create `.browserslistrc`**

```
>= 0.5%
last 2 major versions
not dead
Safari >= 15
iOS >= 15
```

- [ ] **Step 4: Create `.editorconfig`**

```ini
root = true
[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2
```

- [ ] **Step 5: Create `.gitignore`**

```
node_modules/
dist/
*.local
.DS_Store
```

- [ ] **Step 6: Install + commit**

Run: `cd crm-bootstrap && npm install`
Expected: lockfile created, no peer-dep errors that abort install.

```bash
git add crm-bootstrap/package.json crm-bootstrap/package-lock.json crm-bootstrap/.nvmrc crm-bootstrap/.browserslistrc crm-bootstrap/.editorconfig crm-bootstrap/.gitignore
git commit -m "chore(crm): scaffold package.json + base config"
```

### Task 2: Vite + PostCSS config (MPA + Sass deprecation silence)

**Files:**
- Create: `crm-bootstrap/vite.config.js`
- Create: `crm-bootstrap/postcss.config.js`

- [ ] **Step 1: Create `vite.config.js`**

```js
import { resolve } from 'node:path'
import { globSync } from 'glob'
import { defineConfig } from 'vite'
import nunjucks from 'vite-plugin-nunjucks'

// MPA: every src/pages/**/*.html becomes a Rollup input.
// Nunjucks compiles .njk → .html before this resolves (see plugin order).
const pages = Object.fromEntries(
  globSync('src/pages/**/*.html').map((f) => [
    f.replace(/^src\//, '').replace(/\.html$/, ''),
    resolve(__dirname, f),
  ]),
)

export default defineConfig({
  root: 'src',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: { input: pages },
  },
  server: { port: 8080 },
  plugins: [nunjucks()],
  css: {
    devSourcemap: true,
    preprocessorOptions: {
      scss: {
        // Bootstrap 5.3 still uses @import + global Sass fns → expected upstream
        // deprecations (twbs/bootstrap#41558). Silence; pinned sass ~1.99.
        silenceDeprecations: ['import', 'mixed-decls', 'color-functions', 'global-builtin'],
      },
    },
  },
})
```

- [ ] **Step 2: Create `postcss.config.js`**

```js
export default { plugins: { autoprefixer: {} } }
```

- [ ] **Step 3: Commit**

```bash
git add crm-bootstrap/vite.config.js crm-bootstrap/postcss.config.js
git commit -m "chore(crm): vite 6 MPA config + autoprefixer + sass deprecation silence"
```

### Task 3: Lint + format config

**Files:**
- Create: `crm-bootstrap/.stylelintrc.json`
- Create: `crm-bootstrap/.prettierrc.json`

- [ ] **Step 1: Create `.stylelintrc.json`**

```json
{
  "extends": ["stylelint-config-twbs-bootstrap/scss", "stylelint-config-prettier-scss"],
  "rules": {
    "scss/at-import-partial-extension": null,
    "scss/at-import-no-partial-leading-underscore": null
  }
}
```

- [ ] **Step 2: Create `.prettierrc.json`**

```json
{ "semi": false, "singleQuote": true, "printWidth": 100, "trailingComma": "all" }
```

- [ ] **Step 3: Commit**

```bash
git add crm-bootstrap/.stylelintrc.json crm-bootstrap/.prettierrc.json
git commit -m "chore(crm): stylelint (twbs-bootstrap) + prettier config"
```

---

## Phase 1 — Design tokens (single source of truth)

### Task 4: Extract `:root` tokens from the original prototype verbatim

**Files:**
- Read (reference, do not edit): `C:\Users\elbics\Desktop\design-project\designs\crm-glass.html` lines 17–82
- Create: `crm-bootstrap/src/scss/tokens/_colors.scss`
- Create: `crm-bootstrap/src/scss/tokens/_typography.scss`
- Create: `crm-bootstrap/src/scss/tokens/_glass.scss`
- Create: `crm-bootstrap/src/scss/tokens/_space-radii.scss`

- [ ] **Step 1: Read original token block**

Read `crm-glass.html` lines 17–82. Transcribe every `--*` custom property name **and its exact value** into the four token partials below as SCSS variables (one `$`-var per CSS var, value verbatim). Spec §4.2 lists the token families; the file is authoritative for exact numbers.

- [ ] **Step 2: Create `tokens/_colors.scss`** (Bootstrap-bridged brand + glass-ink + status)

```scss
// Brand accents (verbatim from crm-glass.html :root)
$ds-coral:   #FF8A6E;
$ds-amber:   #FFC171;
$ds-rose:    #FF7D9D;
$ds-gold:    #FFD98A;
$ds-peach:   #FFB088;
$ds-success: #7DD3A8;
$ds-warning: #FFC171;
$ds-danger:  #FF8A8A;

// Ink (light text on dark glass)
$ds-ink-1: rgba(255, 255, 255, 1);
$ds-ink-2: rgba(235, 235, 245, 0.85);
$ds-ink-3: rgba(235, 235, 245, 0.66);
$ds-ink-4: rgba(235, 235, 245, 0.46);

// Bootstrap brand bridge — Bootstrap auto-folds these into $theme-colors
$primary:   $ds-coral;
$success:   $ds-success;
$warning:   $ds-warning;
$danger:    $ds-danger;
$body-color: $ds-ink-1;
```

- [ ] **Step 3: Create `tokens/_typography.scss`**

```scss
// Onest replaces Inter (Holy Grail hard-gate; self-hosted, see Task 13)
$font-family-sans-serif: 'Onest', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
$font-family-base: $font-family-sans-serif;

// iOS type scale (verbatim) → exposed as --ds-t-* in Task 8
$ds-type: (
  large-title: 34px, title-1: 28px, title-2: 22px, title-3: 20px,
  headline: 17px, body: 17px, callout: 16px, subhead: 15px,
  footnote: 13px, caption-1: 12px, caption-2: 11px,
);
```

- [ ] **Step 4: Create `tokens/_glass.scss`**

```scss
// Glass material — opacity ladder (verbatim crm-glass.html)
$ds-glass: (
  ultrathin: rgba(51, 51, 51, 0.18),
  thin:      rgba(51, 51, 51, 0.28),
  regular:   rgba(51, 51, 51, 0.38),
  thick:     rgba(51, 51, 51, 0.50),
  chrome:    rgba(51, 51, 51, 0.42),
);
$ds-blur: (
  ultrathin: blur(16px) saturate(140%),
  thin:      blur(24px) saturate(160%),
  regular:   blur(36px) saturate(180%),
  thick:     blur(48px) saturate(200%),
);
$ds-glass-border:        rgba(255, 255, 255, 0.18);
$ds-glass-border-strong: rgba(255, 255, 255, 0.30);
$ds-spec-rim:        inset 0 1px 0 rgba(255,255,255,.4), inset 0 -1px 0 rgba(255,255,255,.06), inset 0 0 0 .5px rgba(255,255,255,.08);
$ds-spec-rim-strong: inset 0 1.5px 0 rgba(255,255,255,.55), inset 0 -1px 0 rgba(255,255,255,.08), inset 0 0 0 .5px rgba(255,255,255,.14);
```

- [ ] **Step 5: Create `tokens/_space-radii.scss`**

```scss
$ds-radius: (xl: 28px, lg: 22px, md: 16px, sm: 12px, xs: 8px, pill: 999px);
$ds-shadow: (
  s1:    0 1px 2px rgba(0,0,0,.10),
  soft:  0 2px 8px -2px rgba(0,0,0,.15),
  card:  0 4px 16px -6px rgba(0,0,0,.20),
  hover: 0 8px 24px -8px rgba(0,0,0,.28),
  button: 0 4px 12px -3px rgba(255,138,110,.35),
);
$ds-ease: (
  glass: cubic-bezier(.32,.72,0,1),
  spring: cubic-bezier(.5,1.4,.4,1),
  out-quart: cubic-bezier(.25,1,.5,1),
);
$ds-dur: (fast: 180ms, glass: 380ms);
$ds-sidebar-w: 72px;
$ds-sidebar-expanded: 248px;

// Bootstrap radius bridge
$border-radius:    map-get($ds-radius, md);
$border-radius-sm: map-get($ds-radius, sm);
$border-radius-lg: map-get($ds-radius, lg);
$border-radius-xl: map-get($ds-radius, xl);
$border-radius-pill: map-get($ds-radius, pill);
```

- [ ] **Step 6: Commit**

```bash
git add crm-bootstrap/src/scss/tokens/
git commit -m "feat(crm): design tokens extracted verbatim from crm-glass.html"
```

### Task 5: `main.scss` — @layer skeleton + Bootstrap Option-B import order

**Files:**
- Create: `crm-bootstrap/src/scss/main.scss`
- Create: empty `crm-bootstrap/src/scss/tokens/_maps.scss`, `abstracts/_mixins.scss`, `base/_index.scss`, `layout/_index.scss`, `components/_index.scss`, `pages/_index.scss`, `themes/_index.scss` (one-line `// placeholder` each, filled in later tasks — these are real files this task creates so imports resolve)

- [ ] **Step 1: Create the empty partials** (each contains exactly `// filled by a later task`)

- [ ] **Step 2: Create `main.scss`**

```scss
// Cascade layer order — ONE declaration, first. Later layers win w/o !important.
@layer reset, bootstrap, tokens, glass, widgets, utilities;

@layer bootstrap {
  @import 'bootstrap/scss/functions';

  // Variable + map overrides MUST sit after functions, before variables.
  @import 'tokens/colors';
  @import 'tokens/typography';
  @import 'tokens/glass';
  @import 'tokens/space-radii';

  @import 'bootstrap/scss/variables';
  @import 'bootstrap/scss/variables-dark';

  @import 'tokens/maps'; // map-merge into $theme-colors / $utilities

  @import 'bootstrap/scss/maps';
  @import 'bootstrap/scss/mixins';
  @import 'bootstrap/scss/root';

  // Selective components — only what the 29 CRM screens use
  @import 'bootstrap/scss/reboot';
  @import 'bootstrap/scss/type';
  @import 'bootstrap/scss/containers';
  @import 'bootstrap/scss/grid';
  @import 'bootstrap/scss/tables';
  @import 'bootstrap/scss/forms';
  @import 'bootstrap/scss/buttons';
  @import 'bootstrap/scss/dropdown';
  @import 'bootstrap/scss/nav';
  @import 'bootstrap/scss/card';
  @import 'bootstrap/scss/badge';
  @import 'bootstrap/scss/modal';
  @import 'bootstrap/scss/offcanvas';
  @import 'bootstrap/scss/toasts';
  @import 'bootstrap/scss/tooltip';
  @import 'bootstrap/scss/spinners';
  @import 'bootstrap/scss/helpers';
}

@layer utilities {
  @import 'bootstrap/scss/utilities';
  @import 'bootstrap/scss/utilities/api';
}

@layer tokens  { @import 'themes/index'; }
@layer glass   { @import 'abstracts/mixins'; @import 'components/index'; }
@layer glass   { @import 'base/index'; @import 'layout/index'; }
@layer widgets { @import 'pages/index'; }
```

- [ ] **Step 3: Verify it compiles**

Run: `cd crm-bootstrap && npx sass --version && npx vite build 2>&1 | tail -20`
Expected: build completes; only silenced Sass deprecation notes; no `SassError`. (No HTML pages yet → Rollup may warn "no input"; acceptable until Task 22.)

- [ ] **Step 4: Commit**

```bash
git add crm-bootstrap/src/scss/
git commit -m "feat(crm): main.scss @layer skeleton + Bootstrap Option-B import order"
```

### Task 7: `tokens/_maps.scss` — bridge tokens into Bootstrap maps

**Files:**
- Modify: `crm-bootstrap/src/scss/tokens/_maps.scss`

- [ ] **Step 1: Write map merges**

```scss
// Custom theme color + a backdrop-blur utility generated by Bootstrap's API.
$custom-colors: (
  'coral': $ds-coral, 'amber': $ds-amber, 'rose': $ds-rose,
);
$theme-colors: map-merge($theme-colors, $custom-colors);

// Extend spacer scale with the prototype's exact gap steps (14px, 24px, 28px)
$spacers: map-merge($spacers, (
  'g14': 0.875rem, 'g24': 1.5rem, 'g28': 1.75rem,
));

$utilities: map-merge($utilities, (
  'backdrop-blur': (
    property: backdrop-filter,
    class: blur,
    values: (sm: blur(16px), md: blur(24px), lg: blur(36px), xl: blur(48px)),
  ),
));
```

- [ ] **Step 2: Verify**

Run: `cd crm-bootstrap && npx vite build 2>&1 | tail -5`
Expected: compiles; no map errors.

- [ ] **Step 3: Commit**

```bash
git add crm-bootstrap/src/scss/tokens/_maps.scss
git commit -m "feat(crm): bridge design tokens into Bootstrap \$theme-colors/\$utilities/\$spacers"
```

### Task 8: `themes/_index.scss` — emit `--ds-*` runtime vars under `[data-bs-theme=dark]`

**Files:**
- Modify: `crm-bootstrap/src/scss/themes/_index.scss`

- [ ] **Step 1: Emit CSS custom properties (CRM is dark-only; lock to dark)**

```scss
:root, [data-bs-theme='dark'] {
  --ds-glass-ultrathin: #{map-get($ds-glass, ultrathin)};
  --ds-glass-thin:      #{map-get($ds-glass, thin)};
  --ds-glass-regular:   #{map-get($ds-glass, regular)};
  --ds-glass-thick:     #{map-get($ds-glass, thick)};
  --ds-glass-chrome:    #{map-get($ds-glass, chrome)};
  --ds-blur-regular:    #{map-get($ds-blur, regular)};
  --ds-blur-thin:       #{map-get($ds-blur, thin)};
  --ds-glass-border:        #{$ds-glass-border};
  --ds-glass-border-strong: #{$ds-glass-border-strong};
  --ds-spec-rim:        #{$ds-spec-rim};
  --ds-spec-rim-strong: #{$ds-spec-rim-strong};
  --ds-ink-1: #{$ds-ink-1}; --ds-ink-2: #{$ds-ink-2};
  --ds-ink-3: #{$ds-ink-3}; --ds-ink-4: #{$ds-ink-4};
  --ds-r-xl: #{map-get($ds-radius, xl)};  --ds-r-lg: #{map-get($ds-radius, lg)};
  --ds-r-md: #{map-get($ds-radius, md)};  --ds-r-pill: #{map-get($ds-radius, pill)};
  --ds-sidebar-w: #{$ds-sidebar-w};  --ds-sidebar-expanded: #{$ds-sidebar-expanded};
  --ds-ease-glass: #{map-get($ds-ease, glass)};
  --ds-dur-glass: #{map-get($ds-dur, glass)};
}
// Force dark color-mode app-wide (original prototype is dark-only).
:root { color-scheme: dark; }
```

- [ ] **Step 2: Verify + commit**

Run: `cd crm-bootstrap && npx vite build 2>&1 | tail -5` → compiles.

```bash
git add crm-bootstrap/src/scss/themes/_index.scss
git commit -m "feat(crm): emit --ds-* runtime tokens (dark-only color mode)"
```

---

## Phase 2 — Glass layer + Bootstrap component re-surfacing (linchpin)

### Task 9: `abstracts/_mixins.scss` — the `glass()` mixin

**Files:**
- Modify: `crm-bootstrap/src/scss/abstracts/_mixins.scss`

- [ ] **Step 1: Write the mixin** (single source of the material recipe; `-webkit-` mandatory)

```scss
@mixin glass($bg: var(--ds-glass-regular), $blur: var(--ds-blur-regular), $rim: var(--ds-spec-rim)) {
  background: $bg;
  -webkit-backdrop-filter: $blur;
  backdrop-filter: $blur;
  border: 1px solid var(--ds-glass-border);
  box-shadow: $rim;
  position: relative;
  isolation: isolate; // contain blend/stacking to the panel
}
@mixin specular-highlight($radius: inherit) {
  &::before {
    content: ''; position: absolute; inset: 0;
    border-radius: $radius; pointer-events: none;
    background: linear-gradient(135deg, var(--ds-glass-border-strong), transparent 42%);
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add crm-bootstrap/src/scss/abstracts/_mixins.scss
git commit -m "feat(crm): glass() + specular-highlight() mixins"
```

### Task 10: Re-surface Bootstrap components via `--bs-*` overrides

**Files:**
- Create: `crm-bootstrap/src/scss/components/_bs-resurface.scss`
- Modify: `crm-bootstrap/src/scss/components/_index.scss` (add `@import 'bs-resurface';`)

- [ ] **Step 1: Write `_bs-resurface.scss`** (zero added specificity — feeds Bootstrap its own vars)

```scss
.card {
  --bs-card-bg: var(--ds-glass-regular);
  --bs-card-border-color: var(--ds-glass-border);
  --bs-card-border-radius: var(--ds-r-xl);
  --bs-card-color: var(--ds-ink-1);
  --bs-card-cap-bg: transparent;
  @include glass(var(--ds-glass-regular), var(--ds-blur-regular), var(--ds-spec-rim));
  @include specular-highlight(var(--ds-r-xl));
}
.modal { --bs-modal-bg: var(--ds-glass-thick); --bs-modal-border-color: var(--ds-glass-border-strong); --bs-modal-border-radius: var(--ds-r-xl); --bs-modal-color: var(--ds-ink-1); }
.modal-content { @include glass(var(--ds-glass-thick), var(--ds-blur-thick), var(--ds-spec-rim-strong)); }
.offcanvas { --bs-offcanvas-bg: var(--ds-glass-thick); --bs-offcanvas-color: var(--ds-ink-1); --bs-offcanvas-border-color: var(--ds-glass-border); @include glass(var(--ds-glass-thick), var(--ds-blur-thick)); }
.dropdown-menu { --bs-dropdown-bg: var(--ds-glass-thick); --bs-dropdown-border-color: var(--ds-glass-border); --bs-dropdown-color: var(--ds-ink-2); --bs-dropdown-link-color: var(--ds-ink-2); --bs-dropdown-link-hover-bg: rgba(255,255,255,.06); --bs-dropdown-border-radius: var(--ds-r-md); @include glass(var(--ds-glass-thick), var(--ds-blur-thin)); }
.btn { --bs-btn-color: var(--ds-ink-1); --bs-btn-border-color: var(--ds-glass-border); --bs-btn-border-radius: var(--ds-r-pill); }
.btn-primary { --bs-btn-bg: var(--bs-coral); --bs-btn-border-color: transparent; --bs-btn-hover-bg: #{$ds-coral}; box-shadow: #{map-get($ds-shadow, button)}; }
.table { --bs-table-bg: transparent; --bs-table-color: var(--ds-ink-2); --bs-table-border-color: var(--ds-glass-border); }
.form-control, .form-select { --bs-body-bg: transparent; background: rgba(255,255,255,.05); border-color: var(--ds-glass-border); color: var(--ds-ink-1); border-radius: var(--ds-r-sm); }
.form-control::placeholder { color: var(--ds-ink-4); }
.nav-link { --bs-nav-link-color: var(--ds-ink-3); --bs-nav-link-hover-color: var(--ds-ink-1); }
```

- [ ] **Step 2: Verify + commit**

Run: `cd crm-bootstrap && npx vite build 2>&1 | tail -5` → compiles.

```bash
git add crm-bootstrap/src/scss/components/
git commit -m "feat(crm): re-surface Bootstrap components to glass via --bs-* overrides"
```

### Task 11: Backdrop photo layer + pitfall guards

**Files:**
- Create: `crm-bootstrap/src/scss/base/_backdrop.scss`
- Modify: `crm-bootstrap/src/scss/base/_index.scss` (add `@import 'backdrop';`)
- Asset dependency: `src/assets/img/sunset-backdrop.jpg` (Task 13)

- [ ] **Step 1: Write `_backdrop.scss`** (photo lives outside any backdrop-root ancestor — mitigation R1)

```scss
body { min-height: 100vh; background: #0a0612; color: var(--ds-ink-1); }
body::before {
  content: ''; position: fixed; inset: 0; z-index: -1;
  background: url('/assets/img/sunset-backdrop.jpg') center 30% / cover no-repeat;
}
body::after { // dark wash for legibility (gradient overlay from original)
  content: ''; position: fixed; inset: 0; z-index: -1;
  background: linear-gradient(180deg, rgba(10,6,18,.35), rgba(10,6,18,.65));
}
// Guard: never put filter/opacity/transform on the shell wrapper (breaks blur).
.app-shell { transform: none !important; } // documented exception: prevents backdrop-root
```

> Note: the single `!important` here is a documented pitfall guard (prevents an accidental backdrop-root), **not** a Bootstrap override — allowed per spec §5 R1.

- [ ] **Step 2: Commit**

```bash
git add crm-bootstrap/src/scss/base/
git commit -m "feat(crm): fixed photo backdrop + backdrop-root pitfall guard"
```

### Task 12: Glass modal-backdrop blur (pitfall R2)

**Files:**
- Create: `crm-bootstrap/src/scss/components/_modal-glass.scss`
- Modify: `crm-bootstrap/src/scss/components/_index.scss` (add import)

- [ ] **Step 1: Write it**

```scss
.modal-backdrop.show {
  --bs-backdrop-opacity: 0.25;
  --bs-backdrop-bg: #0a0612;
  -webkit-backdrop-filter: blur(20px);
  backdrop-filter: blur(20px);
}
.modal { --bs-modal-box-shadow: #{map-get($ds-shadow, hover)}, var(--ds-spec-rim-strong); }
```

- [ ] **Step 2: Verify + commit**

Run: `cd crm-bootstrap && npx vite build 2>&1 | tail -5` → compiles.

```bash
git add crm-bootstrap/src/scss/components/
git commit -m "feat(crm): frosted modal backdrop (pitfall R2 mitigation)"
```

### Task 13: Externalize backdrop asset + self-host Onest

**Files:**
- Create: `crm-bootstrap/src/assets/img/sunset-backdrop.jpg`
- Create: `crm-bootstrap/src/assets/fonts/onest-*.woff2`
- Create: `crm-bootstrap/src/scss/base/_fonts.scss`
- Modify: `crm-bootstrap/src/scss/base/_index.scss`

- [ ] **Step 1: Copy the backdrop**

Run: `cp "C:/Users/elbics/Desktop/design-project/designs/assets/sunset-backdrop.jpg" crm-bootstrap/src/assets/img/sunset-backdrop.jpg`
Expected: file exists, ~525 KB.

- [ ] **Step 2: Fetch Onest woff2** (weights 300–800; self-hosted, not Google Fonts — Holy Grail)

Run: `node -e "console.log('download Onest 300,400,500,600,700,800 woff2 from https://github.com/sevmeyer/onest or fontsource into src/assets/fonts/')"`
Then place `onest-{300,400,500,600,700,800}.woff2` in `src/assets/fonts/`. If `@fontsource/onest` is preferred, `npm i @fontsource/onest` and import in `main.js` instead — pick one; this plan uses self-hosted woff2.

- [ ] **Step 3: Create `base/_fonts.scss`**

```scss
@each $w in (300, 400, 500, 600, 700, 800) {
  @font-face {
    font-family: 'Onest';
    font-style: normal;
    font-weight: #{$w};
    font-display: swap;
    src: url('/assets/fonts/onest-#{$w}.woff2') format('woff2');
  }
}
```

- [ ] **Step 4: Verify + commit**

Run: `cd crm-bootstrap && npx vite build 2>&1 | tail -5` → compiles; assets emitted to `dist/assets`.

```bash
git add crm-bootstrap/src/assets/ crm-bootstrap/src/scss/base/
git commit -m "feat(crm): externalize backdrop + self-host Onest font (replaces Inter)"
```

---

## Phase 3 — App shell + JS

### Task 14: Selective Bootstrap JS bundle

**Files:**
- Create: `crm-bootstrap/src/js/bootstrap.js`
- Create: `crm-bootstrap/src/js/main.js`

- [ ] **Step 1: `bootstrap.js`** (only plugins the 29 screens use)

```js
import Modal from 'bootstrap/js/dist/modal'
import Dropdown from 'bootstrap/js/dist/dropdown'
import Offcanvas from 'bootstrap/js/dist/offcanvas'
import Tab from 'bootstrap/js/dist/tab'
import Toast from 'bootstrap/js/dist/toast'
import Tooltip from 'bootstrap/js/dist/tooltip'
export { Modal, Dropdown, Offcanvas, Tab, Toast, Tooltip }
```

- [ ] **Step 2: `main.js`**

```js
import '../scss/main.scss'
import './bootstrap.js'
import './theme.js'
import './modules/router.js'
import './modules/table.js'
import './modules/scroll-reveal.js'
```

- [ ] **Step 3: Commit**

```bash
git add crm-bootstrap/src/js/bootstrap.js crm-bootstrap/src/js/main.js
git commit -m "feat(crm): selective Bootstrap JS bundle + entrypoint"
```

### Task 15: Theme module (dark lock + localStorage parity)

**Files:**
- Create: `crm-bootstrap/src/js/theme.js`

- [ ] **Step 1: Write it** (CRM dark-only; keep API shape for parity, force dark)

```js
const root = document.documentElement
root.setAttribute('data-bs-theme', 'dark')
try { localStorage.setItem('crm-glass.theme', 'dark') } catch {}
```

- [ ] **Step 2: Commit**

```bash
git add crm-bootstrap/src/js/theme.js
git commit -m "feat(crm): theme module (dark-only lock, localStorage parity)"
```

### Task 16: Hash router (preserve original SPA behavior + key)

**Files:**
- Create: `crm-bootstrap/src/js/modules/router.js`

- [ ] **Step 1: Write it** (parity with original `crm-glass.last-route`)

```js
const STORE = 'crm-glass.last-route'
function route() {
  const id = location.hash.replace('#', '') || 'page-home'
  document.querySelectorAll('[data-page]').forEach((el) => {
    el.hidden = el.dataset.page !== id
  })
  document.querySelectorAll('[data-nav]').forEach((el) => {
    el.classList.toggle('active', el.dataset.nav === id)
  })
  try { localStorage.setItem(STORE, id) } catch {}
  window.scrollTo(0, 0)
}
window.addEventListener('hashchange', route)
window.addEventListener('DOMContentLoaded', () => {
  if (!location.hash) {
    let last = null
    try { last = localStorage.getItem(STORE) } catch {}
    if (last) location.hash = last
  }
  route()
})
```

- [ ] **Step 2: Commit**

```bash
git add crm-bootstrap/src/js/modules/router.js
git commit -m "feat(crm): hash router with crm-glass.last-route parity"
```

### Task 17: Sortable + column-toggle table module

**Files:**
- Create: `crm-bootstrap/src/js/modules/table.js`

- [ ] **Step 1: Write it** (replicates original table sort + column toggle behavior)

```js
// Sort: click <th data-sort> toggles asc/desc; numeric auto-detected.
document.addEventListener('click', (e) => {
  const th = e.target.closest('th[data-sort]')
  if (!th) return
  const table = th.closest('table')
  const idx = [...th.parentNode.children].indexOf(th)
  const dir = th.dataset.dir === 'asc' ? 'desc' : 'asc'
  th.dataset.dir = dir
  const rows = [...table.tBodies[0].rows]
  rows.sort((a, b) => {
    const x = a.cells[idx].textContent.trim()
    const y = b.cells[idx].textContent.trim()
    const nx = parseFloat(x.replace(/[^\d.-]/g, ''))
    const ny = parseFloat(y.replace(/[^\d.-]/g, ''))
    const cmp = !isNaN(nx) && !isNaN(ny) ? nx - ny : x.localeCompare(y, 'ru')
    return dir === 'asc' ? cmp : -cmp
  })
  rows.forEach((r) => table.tBodies[0].appendChild(r))
})
// Column toggle: [data-col-toggle="N"] checkbox hides nth col.
document.addEventListener('change', (e) => {
  const cb = e.target.closest('[data-col-toggle]')
  if (!cb) return
  const n = Number(cb.dataset.colToggle)
  const table = document.querySelector(cb.dataset.colTable)
  table.querySelectorAll('tr').forEach((tr) => {
    const cell = tr.children[n]
    if (cell) cell.hidden = !cb.checked
  })
})
```

- [ ] **Step 2: Commit**

```bash
git add crm-bootstrap/src/js/modules/table.js
git commit -m "feat(crm): sortable + column-toggle table module"
```

### Task 18: Scroll-reveal module

**Files:**
- Create: `crm-bootstrap/src/js/modules/scroll-reveal.js`

- [ ] **Step 1: Write it**

```js
const io = new IntersectionObserver((entries) => {
  entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('is-revealed'); io.unobserve(en.target) } })
}, { threshold: 0.12 })
window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el))
})
```

- [ ] **Step 2: Commit**

```bash
git add crm-bootstrap/src/js/modules/scroll-reveal.js
git commit -m "feat(crm): scroll-reveal module"
```

### Task 19: Icons partial

**Files:**
- Create: `crm-bootstrap/src/templates/partials/icons.njk`

- [ ] **Step 1:** Extract the inline SVG icon set used by `crm-glass.html` (sidebar/nav/kebab/chevron icons) into a Nunjucks macro file `{% macro icon(name) %}…{% endmacro %}` reproducing each `<svg>` verbatim. One macro call per icon used in screens.

- [ ] **Step 2: Commit**

```bash
git add crm-bootstrap/src/templates/partials/icons.njk
git commit -m "feat(crm): icons macro (verbatim SVGs from original)"
```

### Task 20: App shell — sidebar (72→248 hover + offcanvas <lg) + sticky topbar

**Files:**
- Create: `crm-bootstrap/src/templates/partials/sidebar.njk`
- Create: `crm-bootstrap/src/templates/partials/topbar.njk`
- Create: `crm-bootstrap/src/templates/layouts/crm-shell.njk`
- Create: `crm-bootstrap/src/templates/layouts/base.njk`
- Create: `crm-bootstrap/src/scss/layout/_shell.scss` (+ import in `layout/_index.scss`)

- [ ] **Step 1: `base.njk`**

```njk
<!doctype html>
<html lang="ru" data-bs-theme="dark">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% block title %}Turbo Performance CRM{% endblock %}</title>
</head>
<body>
<div class="app-shell">{% block shell %}{% endblock %}</div>
<script type="module" src="/js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: `sidebar.njk`** — fixed rail ≥lg, offcanvas <lg, same markup (mitigation R3: z-index)

```njk
<aside class="ds-sidebar position-fixed top-0 bottom-0 start-0 d-none d-lg-flex flex-column">
  {# nav items: Главная · Проекты · Организации · Документы · Библиотека · Выйти #}
  {% include 'partials/_nav-items.njk' %}
</aside>
<div class="offcanvas offcanvas-start d-lg-none" tabindex="-1" id="navOff">
  <div class="offcanvas-body">{% include 'partials/_nav-items.njk' %}</div>
</div>
```

(Create `partials/_nav-items.njk` with the five nav links + footer "Выйти", each `<a data-nav="page-…" href="#page-…">{{ icon('…') }}<span>…</span></a>`, copied 1:1 from `crm-glass.html` sidebar.)

- [ ] **Step 3: `topbar.njk`** — `sticky-top`, search + notifications dropdown + user dropdown + burger (offcanvas trigger), markup 1:1.

- [ ] **Step 4: `crm-shell.njk`**

```njk
{% extends 'layouts/base.njk' %}
{% block shell %}
{% include 'partials/sidebar.njk' %}
<div class="ds-main">
  {% include 'partials/topbar.njk' %}
  <main class="ds-stage">{% block content %}{% endblock %}</main>
</div>
{% endblock %}
```

- [ ] **Step 5: `layout/_shell.scss`** (exact dims from original; sidebar hover-expand)

```scss
.ds-sidebar {
  width: var(--ds-sidebar-w); z-index: 100; padding: 20px 0;
  margin: 20px; border-radius: var(--ds-r-xl);
  @include glass(var(--ds-glass-thick), var(--ds-blur-thick));
  transition: width var(--ds-dur-glass) var(--ds-ease-glass);
  overflow: hidden;
  &:hover { width: var(--ds-sidebar-expanded); }
  span { opacity: 0; transition: opacity 120ms; }
  &:hover span { opacity: 1; }
}
.ds-main { padding-inline-start: calc(var(--ds-sidebar-w) + 48px); }
@media (max-width: 991.98px) { .ds-main { padding-inline-start: 0; } }
.ds-stage { padding: 24px 28px 48px; min-height: 100vh; }
.ds-main > .ds-topbar { position: sticky; top: 0; z-index: 90; }
.offcanvas { z-index: 1100; } // > sticky topbar (mitigation R3 / twbs#40575)
```

- [ ] **Step 6: Verify (visual gate begins next phase)** — `npm run build` green; `npm run css-lint` green.

- [ ] **Step 7: Commit**

```bash
git add crm-bootstrap/src/templates/ crm-bootstrap/src/scss/layout/
git commit -m "feat(crm): app shell — sidebar(hover-expand+offcanvas) + sticky topbar"
```

### Task 21: Shared UI macros

**Files:**
- Create: `crm-bootstrap/src/templates/macros/ui.njk`

- [ ] **Step 1:** Define Nunjucks macros for the recurring patterns observed in `crm-glass.html`: `kpiCard()`, `glassCard()`, `dataTable()`, `pageHeader()`, `pillFilter()`, `modal()`. Each renders Bootstrap markup (`.card`, `.table`, `.modal`, `.btn`, `.nav`) per the Task 30 mapping. Reproduce class/structure so a screen = compose macros.

- [ ] **Step 2: Commit**

```bash
git add crm-bootstrap/src/templates/macros/ui.njk
git commit -m "feat(crm): shared UI macros (kpi/card/table/header/filter/modal)"
```

### Task 22: First screen end-to-end — `page-home` (proves the pipeline + pattern)

**Files:**
- Create: `crm-bootstrap/src/pages/crm/index.njk` (renders all screens; `page-home` first)

- [ ] **Step 1:** Create `src/pages/crm/index.njk` extending `crm-shell.njk`. Add `page-home` as a `<section data-page="page-home">` rebuilt from `crm-glass.html#page-home` (KPI×4 + activity feed + presence + quick actions + pinned) using Task 21 macros + Bootstrap grid/cards. All other 28 screens added as empty `<section data-page="…" hidden>` stubs so the router + nav work.

- [ ] **Step 2: Verify (FIRST fidelity gate)**

Run: `cd crm-bootstrap && npm run build && npm run preview` (serve dist).
Then dispatch `compound-engineering:design:design-implementation-reviewer`: compare rendered `#page-home` against `crm-glass.html#page-home` at 1440px + 375/768/1024; WCAG AA; console.
Expected: no HIGH findings. Fix any, re-run once.

- [ ] **Step 3: Commit**

```bash
git add crm-bootstrap/src/pages/
git commit -m "feat(crm): page-home ported + pipeline proven (fidelity gate PASS)"
```

---

## Phase 5 — Screen porting (procedure-driven; per-screen verification gate)

### Task 30: Lock the mapping table (reference for every screen task)

**Files:**
- Create: `crm-bootstrap/docs/PORT-MAPPING.md`

- [ ] **Step 1: Write the fixed original→Bootstrap mapping** (the procedure every screen follows)

```md
| Original construct (crm-glass.html)        | Bootstrap rebuild                                  |
|--------------------------------------------|----------------------------------------------------|
| .modal-overlay/.modal-panel + openModal()  | Bootstrap Modal (data-bs-toggle / new Modal())     |
| custom .dd dropdown + data-dd-toggle       | Bootstrap Dropdown                                 |
| .tab-panel radio group                     | Bootstrap Tabs (nav-tabs + tab-pane)               |
| .pill-group filter                         | btn-group + .btn-check                              |
| CSS grid .form-grid/.kpi-grid/.two-col     | .row + .col-* (+ $spacers g14/g24/g28)             |
| .col-toggle checkboxes                     | data-col-toggle module (Task 17)                   |
| sortable header                            | th[data-sort] module (Task 17)                     |
| .toast-stack/showToast()                   | Bootstrap Toast                                    |
| .ask-confirm/askConfirm()                  | Bootstrap Modal (role=alertdialog) + confirm btn   |
| is-loading button                          | .btn + spinner-border span, disabled while pending |
| section #page-X                            | <section data-page="page-X"> in index.njk          |
| inline SVG icon                            | {{ icon('name') }} macro (Task 19)                 |
Per-screen procedure: (a) read #page-X markup from crm-glass.html; (b) rebuild
with shell+macros+mapping above, content/text/numbers VERBATIM; (c) build;
(d) design-implementation-reviewer screenshot-diff vs original #page-X (no HIGH);
(e) commit "feat(crm): port page-X (fidelity PASS)".
```

- [ ] **Step 2: Commit**

```bash
git add crm-bootstrap/docs/PORT-MAPPING.md
git commit -m "docs(crm): locked original→Bootstrap port mapping table"
```

### Task 31: Port the remaining 28 screens (grouped; each screen = its own verify+commit)

Apply the Task 30 procedure to each screen below. **One commit per screen; do not batch.** The verification gate (design-implementation-reviewer screenshot-diff vs the matching `crm-glass.html#page-*`, no HIGH findings) is the pass condition for each.

- [ ] **Group A — Projects (8):** `page-projects`, `page-project`, `page-project-edit`, `page-project-options`, `page-option-resources`, `page-project-documents`, `page-project-permissions`, `page-option-files`
- [ ] **Group B — Org/Admin (10):** `page-organisations`, `page-organisation`, `page-organisation-profiles`, `page-organisation-documents`, `page-org-new`, `page-org-edit`, `page-option-new`, `page-option-edit`, `page-profile-new`, `page-permission-new`
- [ ] **Group C — Resources (6):** `page-resource-new`, `page-resource-edit`, `page-resource-files`, `page-resource-broadcasts`, `page-resource-content`, `page-option-broadcasts`
- [ ] **Group D — Core (4):** `page-documents`, `page-library`, `page-library-item`, `page-library-item-edit`

(29 total = page-home [Task 22] + 28 here. Each `- [ ]` group expands to one verify+commit per screen.)

---

## Phase 6 — Standalone, docs, final verification

### Task 32: Kitchen-sink styleguide page

**Files:**
- Create: `crm-bootstrap/styleguide/index.njk`

- [ ] **Step 1:** Build a single page rendering: `$theme-colors` swatches, type scale, every `.ds-*`/glass component in default/hover/disabled, glass card over the busy backdrop, all form controls. Add it to `vite.config.js` glob (already covered by `src/**` — place under `src/styleguide/`).
- [ ] **Step 2: Commit** `git commit -m "docs(crm): kitchen-sink styleguide page"`

### Task 33: Standalone build script + dev-handoff docs

**Files:**
- Create: `crm-bootstrap/tools/inline-standalone.mjs`
- Create: `crm-bootstrap/README.md`, `crm-bootstrap/CONTRIBUTING.md`

- [ ] **Step 1: `tools/inline-standalone.mjs`** — use `vite-plugin-singlefile` OR a post-`dist` inliner that base64-embeds CSS/JS/img/fonts into one `crm-bootstrap-standalone.html` (all screens via hash). Keep separate from `npm run build`.
- [ ] **Step 2: `README.md`** — what/why, prereqs (`.nvmrc`, `npm ci`), scripts table, directory map, "where things live" (tokens→`scss/tokens/`; glass→`abstracts/_mixins.scss`+`components/_bs-resurface.scss`+`base/_backdrop.scss`; add screen = add `<section data-page>` in `index.njk`), Sass-deprecation note (upstream twbs#41558), Bootstrap pin policy.
- [ ] **Step 3: `CONTRIBUTING.md`** — `.ds-*` BEM-lite naming, never edit `node_modules/bootstrap`, never redefine `.card` directly (use modifier), `npm test` gate, browser target.
- [ ] **Step 4: Verify** `cd crm-bootstrap && npm run build:standalone` → one self-contained HTML opens by double-click, all 29 screens reachable via hash.
- [ ] **Step 5: Commit** `git commit -m "docs(crm): standalone build + README + CONTRIBUTING"`

### Task 34: Full-project fidelity + acceptance pass

- [ ] **Step 1:** Dispatch `compound-engineering:design:design-implementation-reviewer` over **all 29 screens + styleguide**: screenshot-diff vs original, WCAG AA, breakpoints 375/768/1024, console. Fix all HIGH/MEDIUM; re-run once.
- [ ] **Step 2:** Verify spec §8 acceptance criteria 1–10 for CRM. Record results in `crm-bootstrap/docs/ACCEPTANCE.md`.
- [ ] **Step 3: Commit** `git commit -m "test(crm): full fidelity + acceptance pass"`

---

## Self-Review (run after writing; results)

**1. Spec coverage:** D1 (separate project) ✓ this whole plan. D2 Onest ✓ T13. D3 Bootstrap5.3.8 source ✓ T1/T5. D4 Vite6 ✓ T2. D5 hash-SPA ✓ T16/T22. D6 sass pin+silence ✓ T1/T2. §4.1 @layer ✓ T5. §4.2 tokens SSOT ✓ T4/T7/T8. §4.3 markup/JS parity ✓ T14–T18/T30. §4.4 assets+standalone ✓ T13/T33. §4.5 docs ✓ T32/T33. §5 risks R1 ✓ T11, R2 ✓ T12, R3 ✓ T20, perf/Safari ✓ T9. §6 verification ✓ T22/T34. §8 acceptance ✓ T34. CRM has no Customizer/AI/dawn — correctly absent.
**2. Placeholder scan:** Screen-porting (T31) is procedure-driven by explicit design (documented in Conventions + T30), with an objective per-screen gate — not a "TODO". Macro/icon tasks (T19/T21) specify exact source + output contract. No "TBD/handle edge cases/write tests for the above".
**3. Type consistency:** localStorage key `crm-glass.last-route` consistent T16; `data-page`/`data-nav` attributes consistent T16/T20/T22/T30; `glass()` mixin signature consistent T9→T10/T20; `--ds-*` names consistent T8→T9/T10/T20.

---

**Next:** execution handoff (see twin plan `2026-05-19-twinr-bootstrap-port.md`).
