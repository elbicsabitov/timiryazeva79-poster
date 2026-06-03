# HANDOFF — Город ФМ · cont-15 (2026-06-03) — «доделай все долги»: weight-cloud + light theme + ЛК + standalone

> READ-FIRST. Self-contained. All commits LOCAL on `master`, **PUSH HELD until explicit `sync`**.
> File: `designs/gorod-fm.html` (~15.8k lines, single-file SPA). Mirror: `designs/gorod-fm-standalone.html`. Server :8770 serves `designs/`.
> Disc: re-grep anchors (they drift ~+150/feature); `?v=N` cache-bust; light theme needs `?dev=1`; clean `gorodfm_*`/`gorod-fm.theme` LS after probe.

## Commits this session (on top of cont-13/14 `0aae4c1`):
1. `09704df` — **#/taste «Облако вкуса»** weight-editable bubble cloud (cont-14). Size=weight (√w area-honest), tap→docked −/pips/+ stepper, weights PERSIST (`gorodfm_weights`), honest provenance you/pick/demo/rejected. 5-lens reviewed. See `HANDOFF-gorod-fm-cont-13.md` + `SPEC-gorod-fm-taste-weight-cloud.md`.
2. `36a688e` — **Light theme v1** (Apple-grade, ADDITIVE, dev-gated). Dark `cinema` BYTE-IDENTICAL (verified). `html[data-theme="light"]` token block + unlayered per-surface overrides + 2 JS-canvas branches (wave ink #3A4ED0 alpha≥0.82) + toggle cinema↔light. Theme name = **`light`**. Prod forces cinema at boot (~L7479) → can't reach the client. All 7 §8 critic fixes folded in (focus-ring, alpha floor, --text-quat→.60, blue fill #3346C4 for AA labels, success #0A7A53). Player chrome stays immersive-dark in light (re-assert dark tokens). Onboarding intentionally immersive-dark.
3. `ca20b28` — **ЛК account sheet** (thin, demo). Topbar «Личный кабинет» pill → modal: Twinr-ID pointer, theme pills (route through real applyTheme), demo-labeled История/Export/Delete/Logout. Esc/backdrop close, single-accent.
4. `b2bb18f` — **review fixes** (workflow `w5iwcj491`): light main-flow gaps closed (taste-saved/streak, discover ask-results, weight-cloud focus-strip — all were white-on-paper); ЛК «Светлая»/«Система» pills hidden in prod (`data-dev="false"`) so light stays truly dev-gated; setTheme CarPlay fallback + TwinrWave.bump() repaint.
5. `8199bed` — **standalone regenerated** 3.07 MB via `tools/build_gorod_fm_standalone.py` (Pillow, downscale+WebP). Carries cont-13/14 + light + ЛК. 0 console errors.

**Verified Chrome (:8770, 0 errors):** dark home byte-identical; light home/taste/discover clean; ЛК opens + theme pills switch + re-theme sheet + Esc; weight-cloud persist; #/artist + #/taste saved render. node --check clean (24 blocks). Adversarial reviews: weight-cloud (5-lens) + light/ЛК (4-lens+verify) — dark-regression CLEAN, honesty CLEAN.

## 🔴 NEXT SESSION
### A. PUSH at `sync` — 6 commits local (`0aae4c1`..`8199bed`), `master`.
### B. Light theme — DEFERRED secondary-route sweep (the §6 token-retire pass; ~1 session). These routes still have hardcoded dark surfaces / white text uncovered by the light override block (UNLAYERED, before first `</style>` ~L7330, grep `LIGHT theme — per-surface overrides`):
   - `#/track` (history covers inline `#15171D`, lyrics, hero), `#/profile` (redacted strip + `#111318` boxes), `#/recap` (PNG export stays dark by O3 — intentional), `#/artist`, `#/podborki` gallery tiles, `#/lives`.
   - Pattern: light override `html[data-theme="light"] .X { color/background → token }` for white-on-paper; leave white text that sits on dark covers/photos. The `--cover-mix-base` seam (dark `#111318`/light `#FFFFFF`, defined L179/209) is PREPARED but UNWIRED — wire the art-tint `color-mix` call-sites (L~5790 #111318, L~5826 #191C24, L~8918 track-history #15171D) to `var(--cover-mix-base, #111318)` to re-tint covers on white.
   - FOUC pre-paint script + PNG light branch = only if O7 goes public.
### C. Standalone — cloud photos (genre-*.jpg + artist .png) build URLs at runtime (`GorodTasteSeed ASSET + d.img`) → static inliner misses ~38 refs → offline they fall back to flat bubbles. For true-offline investor build, add a GorodTasteSeed-aware inline pass (extract DATA img filenames → inline). Re-run `python tools/build_gorod_fm_standalone.py` after any dev change.
### D. Backlog (not started): #/artist real content (Ф1+ needs-assets — don't fabricate; demo is honestly labeled).

## 🟡 Эльбик decisions (build NOT blocked on these — defaults shipped, reversible)
- **Light theme**: warm `#FAFAF7` base, blue fills `#3346C4` (deeper, AA), name `light`, dev-gated. Flip if wanted: cool `#F2F2F7` base / role-split #5168FC / public toggle (O7).
- **ЛК**: identity = thin Twinr-ID pointer (vs bespoke auth). Светлая dev-only in prod.
- **Standalone**: full inline (genres+artists) vs current (main images only, cloud photos degrade offline).
- GOROD-029 positioning · GOROD-030 licences (long-standing gates).

## Artefacts
- Specs: `SPEC-gorod-fm-taste-weight-cloud.md`, `SPEC-gorod-fm-light-theme.md`, `BLUEPRINT-gorod-fm-sections-integration.md`.
- Builder: `tools/build_gorod_fm_standalone.py` (Pillow OK). Script-check: `.scratch/check_scripts.cjs` (node, all <script> blocks).
- Review workflows: `ws0z0y9d0` (weight grounding), `wuobrjxae` (weight review), `wfejos5ns` (debt inventory), `w5iwcj491` (light/ЛК review).
