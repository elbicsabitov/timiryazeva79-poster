# HANDOFF — Город ФМ v2 pixel-perfect rebuild from Figma

**Created:** 2026-05-27 evening (continuation of v1 same day)
**Status:** ⏸️ В работе — NOT YET STARTED on actual rebuild. Figma context partially pulled (2174:422 + 2385:2924 screenshots only); 3 nodes still need re-fetching.
**Resume command:** `resume design` → RESUME_PROMPT.md routes here

---

## Why v2 exists — user feedback verbatim

> «главная хуже чем в фигме · подборки тоже хуже, не накладываются картинки и не взяты из фигмы картинки · избранное в фигме лучше · медиатека тоже хуже · и избранное у нас хуже · и это страница артиста оказывается, в общем сделай все pixel perfect с фигмы»

**Translation of what to do:**
1. Главная — нашего хуже, чем в Figma → переделать с Figma как ground truth
2. Подборки — не накладываются реальные картинки → скачать ассеты из Figma, заинлайнить
3. Избранное (что у нас) — это на самом деле **страница артиста** в Figma; rewrite as such
4. Медиатека — наш гораздо хуже Figma → перестроить
5. ОТДЕЛЬНОЕ «Раздел Избранное» — тоже хуже → перестроить

**Bottom line:** v1 (commits до `77ee5c1`) был построен «from brief» с гипотезами что в Figma есть только 1 готовый экран (2384:6054). На самом деле в Figma полностью задизайнено **5 экранов**. Надо переделать ВСЕ 5 1:1.

---

## The 5 Figma nodes (this is the new ground truth)

File: `ODcQ2ERWYi3w504Z86TOy3` ("город фм 2 (Copy)")

| # | nodeId | Что это | Чем отличается от нашей текущей реализации |
|---|---|---|---|
| 1 | `2174:422` | **Главная** (real one) | Black bg + radial blur particle background. 9 tile gallery (НЕ stations grid с центр-cover как у нас). Featured central card 617×673 «Потрачу / Егор Крид» с image6 + play badge + bottom solid card `#2d2d5d`. Sidebar: vertical icon-over-text Лайвы/Подборки/Медиатека/Избранное at left:40 top:273, NO «Главная» item. Логотип «Город.fm» 44px UPPERCASE Actay Wide bold at left:80 top:45. Player bar bg = `rgba(81,104,252,0.2)` (blue-tinted, НЕ glass-20 white). |
| 2 | `2384:6054` | **Подборки** | Same 9 tile structure but **REAL photos embedded** (DFM CHILL / VADIM ADAMOV / Z.CITY SHOW / ДИСКАЧ 90-Х / CHILL / K-POP / POP GOLD 2010s + 2 more). У нас сейчас гради енты — надо скачать ассеты и заинлайнить. |
| 3 | `2537:14090` | **Страница артиста** (NOT «Избранное» как я подумал в v1) | Artist photo card + lyrics + station list (3 columns × 5 tracks). У нас сейчас по этому маршруту рендерится artist-как-favorites профайл. Надо переделать как реальную страницу артиста с lyrics. |
| 4 | `2385:2924` | **Медиатека** | Search bar + ABC alphabet filter + Artists grid (205×205 photo cards с именами, 3 columns × N rows). У нас сейчас 2-row grid с ad slot + 4 типа content. Надо переделать как Apple Music-style "Artists" view с ABC nav. |
| 5 | `2535:11151` | **Раздел Избранное** | Sections: «DJ» (8 × 298px cards), «Группы» (6 × 287px tall cards), «Исполнители» (7 × 286px cards with images). Genre rows like Spotify category browsing. У нас сейчас 16-row mixed-type list с фильтрами — надо переделать как row-based browse. |

URLs to view in Figma:
- https://www.figma.com/design/ODcQ2ERWYi3w504Z86TOy3/?node-id=2174-422
- https://www.figma.com/design/ODcQ2ERWYi3w504Z86TOy3/?node-id=2384-6054
- https://www.figma.com/design/ODcQ2ERWYi3w504Z86TOy3/?node-id=2537-14090
- https://www.figma.com/design/ODcQ2ERWYi3w504Z86TOy3/?node-id=2385-2924
- https://www.figma.com/design/ODcQ2ERWYi3w504Z86TOy3/?node-id=2535-11151

---

## Work captured in v2 kickoff session (2026-05-27 evening, 2nd half)

### Already done

1. ✅ Pulled `mcp__figma__get_design_context` for `2174:422` (Главная) — full React/Tailwind dump with 22 image URLs. Saved in `.scratch/gorod-fm-research/figma-v2-asset-urls.json`.
2. ✅ Pulled `mcp__figma__get_screenshot` for `2174:422` and `2385:2924` (Медиатека) — URLs in same json (likely expired by next session — re-fetch).
3. ✅ Created `designs/assets/gorod-fm/` directory (empty, ready to receive downloads).
4. ✅ Saved this handoff document.

### NOT yet done (this is the work for next session)

1. ⏸️ Re-fetch design context for all 5 nodes (URLs from this session expire 7 days from 2026-05-27)
2. ⏸️ Download all unique image assets to `designs/assets/gorod-fm/` via curl/python — give them stable filenames (e.g. `tile-pop-gold.png`, `featured-egor-krid.png`, etc)
3. ⏸️ Rewrite each of 5 page sections in `designs/gorod-fm.html` to match Figma 1:1:
   - Главная section
   - Подборки section (replace gradient placeholders with real images)
   - Артист section (replace current favorites-style with lyrics-style)
   - Медиатека section (replace 2-row grid with ABC + artist grid)
   - Раздел Избранное section (replace mixed-type list with genre rows)
4. ⏸️ Update sidebar to match Figma: remove «Главная» item; keep Лайвы/Подборки/Медиатека/Избранное (4 items); icons at 34×34 vertical layout (DONE in v1 fix wave already — verify still good)
5. ⏸️ Update player-mini bar: bg `rgba(81,104,252,0.2)` blue-tinted (not white glass-20). Track meta = «MARTIN GARRIX/JULIAN JORDAN / Glitch» 24px/16px white. Transport sizes: prev 50 / play 60 / next 50.
6. ⏸️ Verify topbar logo «Город.fm» at left:80 top:45 — 44px UPPERCASE (v1 fix wave already moved logo to sidebar at 32px; may need to re-position OR keep sidebar logo and add a 2nd one — design intent in Figma is logo at the very top-left of viewport, OUTSIDE sidebar).
7. ⏸️ Update `tools/build_gorod_fm_standalone.py` to inline new local PNGs as base64 → produce updated `designs/gorod-fm-standalone.html`.
8. ⏸️ Visual verify all 5 routes via Chrome MCP at 1440×900 viewport; screenshot each, side-by-side compare against Figma screenshots.

---

## Strategy recommendation for next session

This rebuild is HEAVY (downloads + 5 section rewrites + standalone rebuild + visual verify). Dispatch via:

1. **Single Bash script** that loops over all 5 nodeIds, fetches design context via Figma MCP, parses image URLs, downloads to `designs/assets/gorod-fm/` with stable filenames (a Python script reading from a manifest is cleanest).
2. **Subagent-driven-development workflow** per HANDOFF v1 — one implementer per section (5 dispatches), opus model recommended for layout fidelity.
3. **Visual verify subagent** at the end via Chrome MCP (`compound-engineering:design:design-implementation-reviewer` agent).

DO NOT:
- ❌ Try to do all 5 sections inline yourself — context window exhaustion guaranteed
- ❌ Use the gradient placeholders «for now» — user explicitly asked for Figma images
- ❌ Touch topbar/player-mini/tweaks panel structure beyond Figma-matching tweaks
- ❌ Change DEBT.md status legend (it's locked from v1 handoff)

---

## v1 status (preserved — don't undo)

v1 commits `2d7365f`...`77ee5c1` (16 commits) shipped functional 7-screen SPA. **v2 is pure overlay** on top — replacing section CONTENT to match Figma. Keep:
- ✅ App shell structure (topbar / sidebar / main / player-mini / mobile-tabbar / tweaks panel)
- ✅ Hash router + localStorage persist
- ✅ Tweaks panel logic (theme / surface / A-B home / hide-flow-map)
- ✅ Player-full Monte Carlo overlay (this is for `openPlayer()` click — separate from page-route `/track`)
- ✅ Onest fonts only, hit targets ≥ 44, focus-visible, prefers-reduced-motion
- ✅ Adaptable surface architecture (web/mobile/tv/carplay)

Change ONLY:
- Section content within each `<section data-page="...">`
- Image assets (gradient → real Figma photos)
- Player-mini bar bg color (white-glass → blue-tinted per Figma)
- Sidebar item set (remove Главная if matching Figma) — careful with hash-router default route

---

## Files that need updating (concrete list for next session)

| File | Change |
|---|---|
| `designs/assets/gorod-fm/*.png` | Download ~25-40 unique Figma images here (curl from re-fetched URLs) |
| `designs/gorod-fm.html` lines ~5800-9500 (page section content) | Rewrite all 5 page sections per Figma |
| `designs/gorod-fm.html` lines ~5460-5500 (topbar/sidebar HTML) | Possibly move «Город.fm» logo to top-LEFT outside sidebar; remove «Главная» nav item |
| `designs/gorod-fm.html` lines ~492-680 (player-mini CSS) | Change `background` to `rgba(81,104,252,0.2)` |
| `tools/build_gorod_fm_standalone.py` | No code change — already finds local assets via pattern; just re-run after PNGs are in place |
| `designs/gorod-fm-standalone.html` | Regenerate via build script |
| `DEBT.md` | Mark GOROD-021 done at the end |
| `.claude-memory/session_2026_05_28_gorod_fm_v2.md` | NEW session log for v2 work |

---

## TaskList state at handoff

| # | Subject | Status |
|---|---|---|
| 16 | Pixel-perfect rebuild from 5 new Figma nodes | in_progress → pending (handoff) |

GOROD-021 in DEBT.md tracks the same work.

---

## How next session should start

```bash
cd ~/Desktop/design-project
git fetch && git pull
git log --oneline -5  # last commit should be the handoff docs commit

# Verify v1 state intact
ls designs/gorod-fm.html designs/gorod-fm-standalone.html
ls designs/assets/gorod-fm/  # likely empty — that's the gap

# Re-fetch Figma context for all 5 nodes (in parallel via mcp__figma__get_design_context)
# Then download images via Python script
# Then dispatch implementer subagents per section
```

Read THIS file first, then `HANDOFF-gorod-fm.md` (v1) for token reference + screen layouts, then proceed.
