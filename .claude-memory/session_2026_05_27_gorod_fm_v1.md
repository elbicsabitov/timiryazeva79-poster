# Session 2026-05-27 — Город ФМ build (v1)

**Started from:** kickoff session same day (commit ff56114)
**Ended at:** 5d58e43

## What shipped

13 commits on master after kickoff. Single file `designs/gorod-fm.html` grew from 0 → 10258 lines. Standalone produced at `designs/gorod-fm-standalone.html`.

### Commits (in order)

1. `2d7365f` — skeleton (tokens + scaffold + hash router + tweaks)
2. `42ba17b` — player overlay (mini + Monte Carlo full + 3 view states + theme swap)
3. `6b63cb3` — Карта флоу (7-card index hub + hide-in-prod tweak)
4. `ebc6d77` — Главная (chips + hero + 12 stations + FAB→sheet/drawer A/B tweak)
5. `2bfe56b` — Подборки (9 tiles per Figma 2384:6054 + mobile 2-row carousel)
6. `b98cd2f` — Медиатека (2-row grid + ad slot variant)
7. `261bbdf` — Избранное (артист профиль + раздел список)
8. `98f1e16` — Страница трека (Monte Carlo adapted as page, 3 views + 2 carousels)
9. `83cd970` — mobile + surface architecture (web/mobile/tv/carplay contracts)
10. `f981d6e` — review (anti-slop + WCAG + responsiveness findings → REVIEW-gorod-fm-2026-05-27.md)
11. `f9445ef` — fix wave 1: surface switch + Главная cover size + FAB position
12. `5d58e43` — fix wave 2: contrast + text-shadow + hit-targets ≥44 + sidebar opacity
13. `<this commit>` — standalone build + DEBT + session log + RESUME

### Workflow used

`superpowers:subagent-driven-development` — one implementer subagent per task, sequential (shared git index, не параллелить). Used `sonnet` model for each implementer. Final reviewer = `compound-engineering:design:design-implementation-reviewer`. Final fix iterator = `compound-engineering:design:design-iterator`.

### What was carried over from kickoff

- Onest substitute for SF Pro/Gilroy/Actay Wide (Holy Grail compliant)
- Asset placeholder V1 (gradients only — Figma URLs expire 7 days)
- Tweaks single-file pattern (theme + surface + hide-flow-map + home-variant A/B)
- Master direct (НЕ feature branch)
- Bootstrap-port worktree остался paused

### What's pending Эльбик / клиент

- GOROD-016 — real photography для Подборки (когда клиент пришлёт)
- GOROD-017 — показ + фидбек on cinema vs warm vs A/B home variant
- GOROD-018 — Next.js + shadcn/ui dev-handoff после утверждения
- GOROD-019 — final WCAG contrast verification

### Key decisions / discoveries

- CSS `@layer` cascade quirk: `@layer surfaces` rules silently lost to `@layer components` even with correct layer declaration order. Fix: dedicated `<style>` block outside the `@layer` cascade for surface display overrides (`html[data-surface="..."] ... !important`).
- Главная hero cover sized 480px broke layout (pushed stations below fold) → resized to 320px.
- FAB on Главная originally hardcoded `right: 328px` to avoid Tweaks panel — moved to `right: 24px` since Tweaks is collapsible.
- Theme auto-swap: opening full player overlay automatically sets `data-theme="warm"` and restores prior theme on close (carry-forward decision implemented).

### Holy Grail gates passed

- ✅ Onest fonts only (zero Inter/Roboto/Arial/Helvetica/Fraunces/system-ui)
- ✅ Hit targets ≥ 44px after fix wave
- ✅ `text-wrap: pretty/balance` applied
- ✅ Concentric corners (tile-tr 60 / r-base 10 / r-pill 999)
- ✅ Focus-visible 3px cyan ring (4px on TV surface)
- ✅ `prefers-reduced-motion` respected
- ✅ Zero console errors across all 7 routes
- ✅ Standalone build available

## Resume

`resume design` → `RESUME_PROMPT.md` routes to `HANDOFF-gorod-fm.md` → next session reads review.md + decides re: showing customer (Эльбик direct).

Bootstrap-port pause не блокирован Город ФМ.
