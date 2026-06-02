# HANDOFF — Город ФМ · cont-11 (2026-06-03) — Mini-player redesign + FULL AUDIT-backlog cleared

> **READ-FIRST for next session.** Self-contained. Detailed inventory: `REMAINING-cont11-debt-plan.md`. Session outcomes: `docs/RESUME_PROMPT.md` cont-11 block.
> File: `designs/gorod-fm.html` (~14.7k lines, single-file SPA). Standalone: `designs/gorod-fm-standalone.html` (2.43 MB, 34 webp inline).
> Branch `master`, **PUSHED to origin** at end of cont-11.

## What this session delivered
1. **PRIORITY #1 — now-playing mini-bar (`.player-mini`) redesigned** (Эльбик flagged ×2). Research-first: Karpathy workflow `wa8ncwxs9` (4 lenses → synthesis → adversarial critic) → AskUserQuestion → **Variant A «минимум»**.
   - 84→**72px**; material `rgba(11,12,15,.72)+blur28`+hairline; art 48px; type 14/600 + 13/400.
   - Double «почему» → **ONE tappable caption** (→ `#why-pop` reject loop). Transparency wedge preserved (3 surfaces→1).
   - Transport = **play (filled blue 32px) + next (ghost)**; prev/steer/share/volume moved off-bar (not orphaned).
   - 🐛 **play/pause fidelity bug FIXED**: one `playerState.isPlaying` drives `#btn-play`+`#player-full-play`+`#track-page-play` via `aria-pressed`+dual-glyph swap.
   - 🎨 **Player locked to calm single blue** (Wave M, owner Variant A, `42d1902`): «color-from-art» (`--np-accent`/GOROD-042) sampled red on the red Krid cover → red progress + red glow halo on #/track. Locked `--np-accent`=#5168FC (stop sampling), removed colored glow halos (track cover + np-transition, §0.5), progress=fixed blue. Zero red, one accent. NOTE: GOROD-042 color-from-art glows are now retired.
2. **FULL AUDIT-apple-polish backlog cleared** (directive «доделай все долги»). Inventory workflow `w9js8v96c` (14 agents, 108 items) → 12 waves, 13 atomic commits:
   - **G2** `--brand-cyan` 42→**0** (alias deleted).
   - **G7** all focus rings → `--accent-on-dark` (47 blue-light→0, 62 unified) + reduced-motion `:active{scale(.98)}` + 44px hit (`::before`) on sub-44 controls.
   - **G6** anti-slop: live flat (taste tint, ai-dock violet, artist orb, 9 track-history covers) + dead neutralized (16 favorites + 6 library thumbs, `#1ecfe0` leak gone) + mini-art placeholders deleted. linear-gradient 86→50.
   - **DEFAULT_ROUTE** cold-start → `#/onboarding` (returning→home, deep-links intact; 3 paths verified).
   - **8 per-surface waves**: home · taste · discover · track · artist · onboarding · recap/profile · chrome (see RESUME cont-11 for per-item detail).
3. **Standalone rebuilt** with all waves (`rebuild_standalone_full.py` re-applies wave scripts to standalone, retargeting path — images stay inline).

## How to run / verify
```bash
cd designs && python -m http.server 8770       # if not alive
python .scratch/check_scripts_v2.py            # node --check all inline JS → "0 failures"
```
- Prod view: `http://127.0.0.1:8770/gorod-fm.html` · Dev (TWEAKS): `…?dev=1`. Cache-bust `?v=N` (server caches). Standalone: `…/gorod-fm-standalone.html`.
- Verified: 0 console errors across all 8 routes; `grep var(--brand-cyan)` == 0.

## Key artifacts
- `docs/RESUME_PROMPT.md` cont-11 — full done-list + informed deferrals.
- `docs/superpowers/REMAINING-cont11-debt-plan.md` — grounded 108-item inventory (12 waves), the source work-list.
- `.scratch/wave_*.py` + `apply_minibar.py` + `rebuild_standalone_full.py` — gitignored apply scripts (assert count==1 splices; the proven anchor-drift-safe pattern).

## Informed deferrals (low-value / risk, NOT prod-visible — pick up only if Эльбик asks)
- `scaleX` ×12 = intentional `ГОРОД.FM` brand-wordmark stretch (Actay-Wide approximation — do NOT touch) + dead hidden-tile / dev-route labels.
- chrome sidebar-row geometry redesign + tabbar split-indicator + topbar contextual-title (med-risk, low value).
- recap glyph→SVG (✓ ▲ − →); render-identical P2 tokenizations (raw hex == token value); dead library/favorites CSS-rule block deletion (gradients already neutralized).
- taste saved-rows interactivity (honesty: either wire them or drop the «Лайк здесь = сигнал» claim).

## Discipline / learnings
- **Anchors drift** — re-grep the live file before every edit; the python-splice `assert count==1` aborts cleanly on drift (no partial write). The Edit tool needs a fresh Read after any script write.
- **Standalone = code-identical to dev + webp images inline IN PLACE** — so code-only waves re-apply via path-retargeted wave scripts; no PNG→webp re-encoding needed.
- **`grep -c` returns exit 1 on zero matches** — use `grep -oF … | wc -l` in `&&` chains.
- Windows stdout is cp1251 → set `PYTHONIOENCODING=utf-8` before python prints with `→`/Cyrillic.

## START next session
1. `cd ~/Desktop/design-project`, dev-server :8770.
2. Read this + RESUME cont-11. AUDIT-apple-polish backlog is DONE — next work is Эльбик-driven.
3. 🔒 Эльбик-gate (NOT Claude): GOROD-029 positioning · GOROD-030 licensing.
