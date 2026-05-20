# HANDOFF — Liquid Glass → Bootstrap 5.3 port (CRM + Twinr)

**Updated:** 2026-05-20 · **Branch:** `feat/bootstrap-port` · **Worktree:** `~/Desktop/design-project/.worktrees/feat-bootstrap-port`
**Resume command:** `resume design` → continue subagent-driven execution from "NEXT" below.

## What this is
Two Bootstrap 5.3 dev-handoff projects rebuilding approved Liquid Glass prototypes pixel-faithfully.
- Spec: `docs/superpowers/specs/2026-05-19-bootstrap-conversion-design.md`
- Plans: `docs/superpowers/plans/2026-05-19-crm-bootstrap-port.md`, `…-twinr-bootstrap-port.md`
- Ground truth (visual): `./designs/crm-glass.html` (CRM, 29 screens) · `./designs/twinr-liquid-glass.html` (Twinr, 21 pages + AI + Customizer). **Prototype always wins over plan/spec on any discrepancy.**

## Status

| Phase | CRM | Twinr |
|---|---|---|
| 0 scaffold | ✅ | ✅ |
| 1 tokens SSOT (+dawn/customizer) | ✅ | ✅ |
| 2 glass layer + `--bs-*` re-surface | ✅ | ✅ |
| 3 shell + JS (+AI chip-nav) | ✅ | ✅ (shell/JS done; first page is Phase 4) |
| 4 Customizer (Twinr only) | — (n/a) | ⬜ **NEXT** |
| 5 screen porting | ✅ **all 29 screens** | ⬜ |
| 6 styleguide + standalone + acceptance | ✅ | ⬜ |

### CRM — COMPLETE ✅ (2026-05-20)
All 29 screens ported + verified, kitchen-sink styleguide, single-file standalone build, `README`/`CONTRIBUTING`/`docs/ACCEPTANCE.md`, full acceptance pass. Every group passed 2-stage review (fidelity → code-quality). **Delivered to Эльбик** as `crm-bootstrap-handoff-2026-05-20.zip` (Telegram Saved Messages, audited CRM-isolated). Final commit `306166d`. Not merged to master (Twinr still pending — merge train is Эльбик-gated, after Twinr).

### Twinr — Phase 0-3 done, Phase 4 is NEXT
Scaffold, tokens (sunset+dawn+customizer), glass layer, app shell, AI chip-nav — all done. `src/pages/twinr/index.html` is still a plain-HTML stub. `modules/customizer.js` is an empty Phase-4 stub.

## NEXT (resume here) — Twinr only

Per Эльбик 2026-05-20: CRM was handed off solo; Twinr is the next session's work. Execute the Twinr plan `docs/superpowers/plans/2026-05-19-twinr-bootstrap-port.md`:
- **Phase 4** (Tasks 18-20): Liquid Glass Customizer SCSS (`widgets/_customizer.scss`) + Customizer JS (`modules/customizer.js`, exact intensity math 1:1) + first rendered pages (`page-stats` default + `page-guide` hosting the customizer; replace the plain-HTML `index.html` stub with the real `{% extends 'layouts/twinr-shell.njk' %}` page + 19 hidden `data-page` stubs).
- **Phase 5** (Tasks 40-41): lock `twinr-bootstrap/docs/PORT-MAPPING.md`, then port the 19 remaining pages — one screen = one commit = one fidelity gate.
- **Phase 6** (Tasks 42-44): styleguide, standalone build + docs, full acceptance pass.

TaskList for the next session: recreate Twinr T18-T44 tasks (CRM tasks 1-8 are done).

## 🚩 CRITICAL carry-forward — Twinr (read before dispatching implementers)
1. **`main.scss` is correct — never rewrite from the plan skeleton.** Dart Sass `@layer{}` scopes vars → all `$var`/mixin imports hoist to root scope; CSS `@layer reset,bootstrap,tokens,glass,widgets,utilities` order preserved. Only ADD partial `@import`s into existing slots. (A page partial that calls `@include glass()` must `@import '../abstracts/mixins'` at its top; one that does NOT call it must not — dead imports get flagged.)
2. **AI module = 9 tools, NOT 11.** Spec §2 / acceptance #5 / plan say "11" — **inaccurate**. Prototype `twinr-liquid-glass.html` `AI_TOOLS` has 9 (Контент: Источники, Промпты · Генерация: Работа с источником, Рерайтинг, Чат · Медиа: Транскрибация, Генерация видео · Анализ: Документы, Ключевые слова). `ai-subnav.js` `TOOLS` already uses the correct 9. Use 9 everywhere.
3. **Twinr Customizer (Phase 4):** use `twinr-bootstrap/src/scss/tokens/_customizer.scss` (prototype-wins values), NOT plan Task 4 Step 3 numbers. dim key is **`strong`** (not `hard`). Material recipes differ from plan (ultrathin .12/blur14, thin .22/blur22, thick .48/blur44 sat190, chrome .56/blur40 sat150, `clear` added); intensity ladder `(0,.07,.14,.22,.32)`. `modules/customizer.js` is currently an empty stub.
4. **Nunjucks↔Vite wiring** (`vite.config.js`): `createRequire(import.meta.url)` loads the plugin's bundled nunjucks + a custom Environment/FileSystemLoader at `src/templates`; ESM `__dirname` shim present (Twinr fixed `3bd5e70`). CRM proved this end-to-end. **Twinr Phase 4 Task 20 must replace the plain-HTML stub `src/pages/twinr/index.html` with the real `{% extends 'layouts/twinr-shell.njk' %}` page** (page-stats default + page-guide + 19 hidden `data-page` stub sections).
5. **`glass()` mixin emits `position:relative`** on every glass element. Fixed-position glass (sidebar) relies on Bootstrap `.position-fixed`'s *unlayered* `!important` to override it — keep `.position-fixed` on such elements; don't "fix" it.
6. **By-design — reviewers must NOT re-flag:** Onest font replaces Inter (hard-gate D2).

## 🧱 Patterns established during the CRM port — replicate for Twinr
The two projects are architecturally identical; Twinr should follow the same conventions and build its own equivalents of the CRM infrastructure:
- **Buttons:** `.btn-primary` (primary CTA) / `.btn-glass` (medium frosted) / `.btn-ghost` (low-emphasis transparent) / `.btn-danger`. Match the prototype's emphasis per button.
- **Glass surfaces** (any non-`.card` panel): ALWAYS `@include glass($bg,$blur,$rim)` — never a manual `background`+`backdrop-filter`+`border` triple (the mixin also adds `position:relative`+`isolation:isolate`).
- **Colors/sizes in SCSS:** `$ds-*` vars / `--ds-*` tokens / `map-get($ds-type,…)` — never hardcoded brand hex. Plain white tints (`rgba(255,255,255,.06)`) are OK.
- **No inline `style=` and no inline `on*=` handlers.** Variant styling → CSS modifier classes (use BEM `--` for new modifiers, e.g. `.ds-section-hero--compact`); spacing → Bootstrap utilities (`mt-2` etc.); behavior → small delegated `src/js/modules/` files imported in `main.js`.
- **JS module patterns CRM built (Twinr needs its own copies):** `toast.js` (delegated `[data-bs-toast-target]` click handler **+ a `submit` listener that `preventDefault()`s every form** — static SPA, no form may ever navigate); `counter.js` (`[data-counter]` live char-count); `bulk.js` (row-checkbox → bulk bar); dynamic breadcrumb (per-section `data-crumb` attr read by `router.js`). Sticky uppercase glass table headers belong in `_bs-resurface.scss`. alertdialog confirm modals use inline HTML (`role="alertdialog"`) — the `modal()` macro lacks it.
- **Responsive (spec criterion 9):** topbar must collapse the search field on narrow widths so controls stay reachable at 375px; `.ds-tabs` needs `overflow-x:auto`; sidebar→offcanvas at <992px. WCAG: keep hidden form-control radios focusable (`.visually-hidden`, not `display:none`); add `:focus-visible` rings to custom interactive elements.

## Execution protocol
- subagent-driven-development: fresh implementer per chunk (~4-5 screens) + 2-stage review (Stage-1 = `compound-engineering:design:design-implementation-reviewer` screenshot-diff vs prototype, no HIGH; Stage-2 = code-quality of the diff). Fix findings with fresh fix subagents (SendMessage-style continuation not relied on); fix systemic issues in shared files so later screens inherit them. The 2-stage review is load-bearing — during CRM it caught real HIGH defects (unwired bulk-bar, scroll-reveal hiding all content, form-submit page-reload).
- **One implementer at a time** (do NOT run parallel implementers — shared git index races + the skill's red-flag). CRM was done fully before Twinr.
- Per-screen: read `#page-X` from prototype → rebuild via shell+macros+Bootstrap per `PORT-MAPPING.md`, content VERBATIM → build green + css-lint 0 → fidelity gate (no HIGH) → one commit per screen.
- Worktree-local commits only; do NOT push (Эльбик-gated). Final: merge `feat/bootstrap-port` → `master` after Twinr + acceptance (Эльбик-gated).
- Models: scaffold/mechanical→haiku/sonnet; glass/JS/integration/screens→sonnet; review→sonnet.

## Commit ledger
- **CRM** P0 `bad434c..1adf4bc` · P1 `e64dcd9..ab40cba`(+`9126a22`) · P2 `f336f59..9829362` · P3 `…c308e12`+`38c2f08` · **P5-6 `ad4dd9a..306166d`** (all 29 screens + styleguide + standalone + acceptance; per-group fix commits inline). CRM final = `306166d`.
- **Twinr** P0 `d1bbee0..cb747f4` · P1 `a87ee22..`(+`5d3f4bf`) · P2 `c7ca56f..6dbe586` · P3 `a911b55,1c8aab4,4561ad8,f9d2d05`+`3bd5e70`. Twinr Phase 4+ not started.
