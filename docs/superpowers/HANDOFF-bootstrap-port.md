# HANDOFF — Liquid Glass → Bootstrap 5.3 port (CRM + Twinr)

**Updated:** 2026-05-20 · **Branch:** `feat/bootstrap-port` · **Worktree:** `~/Desktop/design-project/.worktrees/feat-bootstrap-port`
**Resume command:** `resume design` → continue subagent-driven execution from "NEXT" below.

## What this is
Two Bootstrap 5.3 dev-handoff projects rebuilding approved Liquid Glass prototypes pixel-faithfully.
- Spec: `docs/superpowers/specs/2026-05-19-bootstrap-conversion-design.md`
- Plans: `docs/superpowers/plans/2026-05-19-crm-bootstrap-port.md`, `…-twinr-bootstrap-port.md`
- Ground truth (visual): `./designs/crm-glass.html` (CRM, 29 screens) · `./designs/twinr-liquid-glass.html` (Twinr, 21 pages + AI + Customizer). **Prototype always wins over plan/spec on any discrepancy.**

## Status — DONE
| Phase | CRM | Twinr |
|---|---|---|
| 0 scaffold | ✅ | ✅ |
| 1 tokens SSOT (+dawn/customizer) | ✅ | ✅ |
| 2 glass layer + `--bs-*` re-surface | ✅ | ✅ |
| 3 shell + JS (+AI chip-nav) + first proof | ✅ (page-home fidelity gate **PASS**) | ✅ (shell/JS; first page is Phase 4) |

Every phase passed 2-stage review (spec/fidelity then quality). Reviews caught & fixed real bugs each phase. CRM `page-home` is the **verified fidelity reference** for all Phase-5 screen porting.

## NEXT (resume here)
Run two parallel subagent-driven streams (independent dirs, conflict-free):
- **CRM → Phase 5** (plan Tasks 30–31): lock `docs/PORT-MAPPING.md`, then port the 28 remaining screens — **one screen = one commit = one per-screen `design-implementation-reviewer` screenshot-diff gate vs `crm-glass.html#page-*` (no HIGH)**. Then Phase 6 (Tasks 32–34: styleguide, standalone+README+CONTRIBUTING, full fidelity+acceptance).
- **Twinr → Phase 4** (plan Tasks 18–20): Liquid Glass Customizer SCSS + JS (exact math 1:1) + first rendered pages (page-stats default, page-guide). Then Phase 5 (Tasks 40–41: 19 pages, per-screen gate) → Phase 6.
TaskList: CRM #13,#14 · Twinr #19,#20,#21.

## 🚩 CRITICAL carry-forward (read before dispatching implementers)
1. **`main.scss` is correct in BOTH — never rewrite from plan skeleton.** Dart Sass `@layer{}` scopes vars → all `$var`/mixin imports hoisted to root scope; CSS `@layer reset,bootstrap,tokens,glass,widgets,utilities` order preserved. Only ADD partial `@import`s into existing slots, matching the established pattern.
2. **AI module = 9 tools, NOT 11.** Spec §2 / acceptance #5 / plans say "11" — **inaccurate**. Prototype `twinr-liquid-glass.html` `AI_TOOLS` has 9 (Контент: Источники, Промпты · Генерация: Работа с источником, Рерайтинг, Чат · Медиа: Транскрибация, Генерация видео · Анализ: Документы, Ключевые слова). `ai-subnav.js` `TOOLS` already uses the correct 9 verbatim. Use 9 everywhere downstream.
3. **Twinr Customizer (Phase 4):** use `twinr-bootstrap/src/scss/tokens/_customizer.scss` (prototype-wins values), NOT plan Task 4 Step 3 numbers. dim key is **`strong`** (not `hard`). Material recipes differ from plan (ultrathin .12/blur14, thin .22/blur22, thick .48/blur44 sat190, chrome .56/blur40 sat150, `clear` added); intensity ladder `(0,.07,.14,.22,.32)`. `modules/customizer.js` is currently an empty Phase-4 stub.
4. **Nunjucks↔Vite wiring** (both `vite.config.js`): `createRequire(import.meta.url)` loads the plugin's bundled nunjucks + a custom Environment/FileSystemLoader at `src/templates`; ESM `__dirname` shim present in BOTH (Twinr fixed `3bd5e70`). CRM proven end-to-end (compiled SPA renders from `.njk`). **Twinr Phase 4 Task 20 must replace the plain-HTML stub `src/pages/twinr/index.html` with the real `{% extends 'layouts/twinr-shell.njk' %}` page** (page-stats default + page-guide + 19 hidden `data-page` stub sections) — same pattern CRM used in Task 22.
5. **page-home = the fidelity bar for Phase 5.** Reuse its established macros/classes: glass buttons via `.btn-glass` (NOT `btn-outline-secondary`); `.btn svg{width:15px;height:15px}`; panels use exact prototype glass tokens/padding/sizes; sidebar 20px viewport inset; topbar `backdrop-filter: var(--ds-blur-thick)`; presence count = success-green. Phase-5 screens should compose the Task-21/17 macros, not re-invent.
6. **`glass()` mixin emits `position:relative`** on every glass element. Fixed-position glass (sidebar) relies on Bootstrap `.position-fixed`'s *unlayered* `!important` to override it — works (unlayered beats layered per CSS cascade). Don't "fix" it; keep `.position-fixed` on such elements.
7. **By-design — reviewers must NOT re-flag as defects:** Onest font (replaces Inter per hard-gate D2); per-screen gate compares vs prototype but Onest≠Inter is correct.
8. **Tracked deferred items (handle in Phase 6 polish / Эльбик decision, not per-screen blockers):** topbar `position:sticky` (prototype topbar scrolls — spec mapped it to `.sticky-top`; confirm with Эльбик if strict "max fidelity" wants non-sticky), specular `::before` additive highlight, scroll-reveal FOUC risk, collapsed-sidebar hover tooltip (L4 — prototype has it, not yet implemented), `⌘K` label on Windows app.
9. **Per-screen Phase-5 protocol:** read `#page-X` from prototype → rebuild via shell+macros+Bootstrap per `PORT-MAPPING.md`, content/text/numbers VERBATIM → build green + css-lint 0 → `compound-engineering:design:design-implementation-reviewer` screenshot-diff vs prototype `#page-X` (no HIGH) → one commit per screen.

## Execution protocol
- subagent-driven-development: fresh implementer per task/phase + 2-stage review (spec/fidelity → code-quality). **SendMessage is NOT available in this harness** — use fresh fix subagents with precise self-contained instructions (don't try to continue an agent).
- 2 parallel streams OK (CRM/Twinr = independent dirs, zero conflict). Never two implementers in the SAME project dir simultaneously.
- Worktree-local commits only; do NOT push (Эльбик-gated). Final: merge train `feat/bootstrap-port` → `master` after all phases + acceptance (Эльбik-gated).
- Models: scaffold/mechanical→haiku/sonnet; glass/JS/integration→sonnet; review→sonnet.

## Commit ledger (phase ends)
- P0 CRM `bad434c..1adf4bc` · Twinr `d1bbee0..cb747f4`
- P1 CRM `e64dcd9..ab40cba` (+fix `9126a22`) · Twinr `a87ee22..` (+fix `5d3f4bf`)
- P2 CRM `f336f59..9829362` · Twinr `c7ca56f..6dbe586`
- P3 CRM `…29f4d20,5d944f7,c308e12` +fix `38c2f08` · Twinr `a911b55,1c8aab4,4561ad8,f9d2d05` +fix `3bd5e70`
