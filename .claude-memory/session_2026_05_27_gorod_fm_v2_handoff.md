# Session 2026-05-27 night — Город ФМ v2 handoff (pixel-perfect rebuild from Figma)

**Started from:** v1 shipped state (HEAD `77ee5c1`, 16 commits, file `designs/gorod-fm.html` 10,274 lines)
**Ended at:** handoff written, NO code changes (HEAD still `77ee5c1`)
**Reason for v2:** user feedback after v1 «доведи все до pixel perfect с фигмы»

## What user said (verbatim)

User sent links to 5 Figma nodes with verdicts:

1. `node-id=2174-422` — «главная **хуже** чем в фигме»
2. `node-id=2384-6054` — «подборки тоже **хуже**, **не накладываются картинки** и **не взяты из фигмы картинки**»
3. `node-id=2537-14090` — «избранное в фигме **лучше**» (later clarified: «и это страница артиста оказывается»)
4. `node-id=2385-2924` — «медиатека тоже **хуже**»
5. `node-id=2535-11151` — «и избранное у нас **хуже**»

Closing directive: **«в общем сделай все pixel perfect с фигмы»**

## What we discovered this session

1. **Figma has FULL designs for 5 screens**, not just Подборки (`2384:6054`). We built our 7-screen prototype based on only that one Figma reference + user brief; the rest we designed from scratch. Wrong assumption — Figma has the canonical versions.

2. **Real artist photos exist in Figma** for all tiles/cards on every screen. v1 used gradient placeholders + abstract SVG illustration art per кэрри-форвард «Asset placeholder V1 — Figma URLs expire 7d». That was an over-cautious workaround — we should download the assets to local disk and inline them via the standalone build script.

3. **Naming was wrong:**
   - Our `#/artist` (artist profile, hand-designed bio + top tracks + albums) ≠ Figma `2537:14090` (different layout: photo card + lyrics + station list)
   - Our `#/favorites` (mixed-type list with filter chips) ≠ Figma `2535:11151` (DJ/Группы/Исполнители horizontal rows)
   - Sidebar nav в Figma = Лайвы / Подборки / Медиатека / Избранное (no «Главная» — logo doubles as home)

4. **Brand tokens updated** based on Figma `2174:422`:
   - Active chip bg: `rgba(81,104,252,0.2)` blue (NOT glass white)
   - Player bar bg на `#/home`: `rgba(81,104,252,0.2)` blue-tinted
   - Featured CTA card bg: `#2d2d5d` purple
   - New brand token needed: `--brand-blue-light: #5168FC`

5. **Главная structural surprise:** Figma `2174:422` is NOT a stations grid (which is what we built). It's:
   - Black bg + huge blurred radial particle bg
   - 9 horizontal tiles across the page (like Подборки but at smaller height)
   - Center featured card 617×673 with image_6 backdrop + "Потрачу / Егор Крид" CTA bar with play-button
   - Left-edge sidebar darkening gradient

## What was done

- Pulled `2174:422` Главная full design context via Figma MCP — extracted React+Tailwind source, all 22 asset URLs, layout coordinates, exact pixel values
- Pulled `2174:422` screenshot at 1920px (image_url short-lived; will need refetch)
- Created `.scratch/gorod-fm-research/` and `designs/assets/gorod-fm/` directories
- Identified all 5 nodes that need rebuilds
- Captured complete v2 strategy in `docs/superpowers/HANDOFF-gorod-fm-v2-pixel-perfect.md`
- Updated `docs/RESUME_PROMPT.md` to route ACTIVE WORK at v2 handoff
- Updated `DEBT.md`: added GOROD-021 (pixel-perfect rebuild), GOROD-022 (brand-blue-light token), GOROD-023 (`#/lives` route); marked GOROD-016 partially superseded; added v2 status note at top of Город ФМ section

## What was NOT done (deferred to next session)

- Pulled design contexts for the other 4 nodes (`2384:6054`, `2385:2924`, `2535:11151`, `2537:14090`)
- Downloaded any image assets
- Modified `designs/gorod-fm.html`
- Touched the build script

## Why deferred

User asked for «передача в след сессию» (handoff) before the rebuild started. v2 is a substantial rewrite (5 screens × full HTML+CSS rewrite + ~40-80 unique asset downloads + standalone rebuild) — better to do it in a fresh session with full context budget.

## Next session entry point

1. Read `docs/superpowers/HANDOFF-gorod-fm-v2-pixel-perfect.md` (this session's main artifact)
2. Re-fetch 5 Figma design contexts in parallel (fresh URLs)
3. Download & dedupe assets to `designs/assets/gorod-fm/`
4. Rewrite screens sequentially: Подборки (smallest delta — warm-up) → Главная → Медиатека → Раздел Избранное → Страница артиста
5. Visual verify via Chrome MCP
6. Standalone rebuild (assets auto-inlined)
7. Close GOROD-021/022/023 in DEBT.md; update memory

## Holy Grail compliance reminder

Must carry over from v1 (don't break):
- Onest fonts only (no Inter/Roboto/etc)
- Hit targets ≥44px on web/mobile, ≥56 TV, ≥80 CarPlay
- `text-wrap: balance` headings, `pretty` paragraphs
- Concentric corners (tile-tr 60, base 10, pill 999)
- Focus-visible rings 3px (4px TV)
- `prefers-reduced-motion` respected
- Zero console errors
- Master direct (atomic commits, no feature branch)
