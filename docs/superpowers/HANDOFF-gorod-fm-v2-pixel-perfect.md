# HANDOFF v2 — Город ФМ pixel-perfect rebuild from Figma

**Created:** 2026-05-27 night (handoff to next session)
**Predecessor:** `HANDOFF-gorod-fm.md` (v1 shipped, 16 commits, HEAD `77ee5c1`)
**Status:** ❌ NOT STARTED — context pulled for 1 of 5 nodes, NO code changes yet
**Branch:** `master` (direct push convention, atomic commits)

---

## Why this exists

User feedback 2026-05-27 night (verbatim):

> «доведи все до pixel perfect в нужных экранах, пока что все еще далеко от фигмы и в хедере дублируется лого и не того размера»
>
> [после v1 pixel-perfect фикс-волны]
>
> «главная хуже чем в фигме · подборки тоже хуже, не накладываются картинки и не взяты из фигмы картинки · избранное в фигме лучше · медиатека тоже хуже · и избранное у нас хуже · и это страница артиста оказывается, в общем **сделай все pixel perfect с фигмы**»

**Ключевые откровения:**
1. В Figma есть БОЛЬШЕ design'ed экранов чем мы думали — НЕ только Подборки `2384:6054`
2. На каждом экране в Figma есть РЕАЛЬНЫЕ ассеты (фото артистов, обложки, иконки), которые мы не использовали (мы делали градиенты-плейсхолдеры)
3. Наш `#/favorites` (раздел) — НЕ страница артиста, это два разных экрана; нужна и страница артиста, и раздел избранное

---

## Five Figma source nodes (the new ground truth)

File key: `ODcQ2ERWYi3w504Z86TOy3` (город фм 2 (Copy))

| Node | Что | Маршрут в нашем SPA | Текущий статус |
|------|-----|---------------------|----------------|
| `2174:422` | **Главная** (real one) — DARK BLACK theme, blurred radial bg, 9 horizontal tiles + featured central card "Потрачу/Егор Крид" с play-CTA | `#/home` | ❌ наш сильно отличается |
| `2384:6054` | **Подборки** — 9 tiles с РЕАЛЬНЫМИ artist-photos + tile-shade overlay (124.4°) + rotated -90deg labels Actay Wide 44px | `#/podborki` | ⚠️ структура OK, но НЕТ реальных картинок (gradient placeholders) |
| `2385:2924` | **Медиатека** — Search bar + ABC alphabet filter row + Artists grid (3 cols × N rows, 205×205 photo cards с именами) | `#/library` | ❌ наш сильно отличается (у нас 2-row + ad slot) |
| `2535:11151` | **Раздел Избранное** — секции "DJ" (8×298px cards), "Группы" (6×287px tall), "Исполнители" (7×286px cards с image) — genre rows | `#/favorites` | ❌ наш сильно отличается (у нас mixed-type list) |
| `2537:14090` | **Страница артиста** — карточка артиста "Зацепила / Артур Пирожков" + lyrics + station list (3 columns × 5 tracks each) | `#/artist` | ❌ наш сильно отличается (у нас bio + top tracks + albums) |

---

## What was done this session

1. **Pulled `2174:422` Главная full design context** via Figma MCP (got React+Tailwind source code + all 22 asset URLs). Saved key facts here.
2. **Pulled `2174:422` screenshot** at 1920px max-dimension (image_url short-lived).
3. **Confirmed sidebar nav per Figma:** Лайвы (microphone icon, ACTIVE highlighted blue gradient on текст «Подборки» — wait actually highlighted entry is «Подборки» which gets the blue tint) / Подборки / Медиатека / Избранное. **NO Главная item** — Город.fm logo top-left IS the home link.
4. **Confirmed Главная structural details:**
   - Black bg `#0C0B0B` + huge blurred radial particle bg (image asset, blur 150px)
   - Logo top-left at (45, 45) — Actay Wide Bold 44px UPPERCASE white
   - Search-icon-pill (52×64) top-right + «Личный кабинет» pill — both `bg-[var(--black,black)]` (NOT glass-20 like before)
   - Chip row centered y=145 with 5 chips, gap 63px — **active chip "ХИП-ХОП"** with bg `rgba(81,104,252,0.2)` (BLUE not white-glass)
   - 9 horizontal tiles row at y=240-273, varying widths 184 / 249 / 339 / 309 / 383 / 368 / 373 / 373 / 373 — heights 600 (most) / 628 (first DFM CHILL only) — each with `border-top-right-radius: 60px`, real artist photo + tile-shade gradient + rotated -90deg label
   - Tiles overlaid by `rgba(3,3,3,0.35)` h=607 darken layer at left=8.33%+35 top=273 w=1815 — gives the whole tile row a dim look
   - Center featured card 617×673 at left=33.33%+88 top=240 — `rounded-[20px]` with image_6 backdrop + linear-gradient overlay (180deg) — large featured artist
   - Featured CTA bar at bottom y=837 — `bg-[#2d2d5d]` purple, rounded-bl-br 20, contains "Потрачу" Actay Wide Bold 20 + "Егор Крид" Actay Regular 17 + 60×60 round play-button with arrow icon (`bg-[rgba(255,255,255,0.2)]`)
   - Player bar y=953, full 1920 width, `bg-[rgba(81,104,252,0.2)]` BLUE-tinted (NOT glass white), w/ prev 50 + play 60 + next 50 group LEFT + image 60 + title 24 + artist 16 + share badge + volume + slider RIGHT
   - Left-side sidebar gradient overlay `from-rgba(255,255,255,0.1) to-rgba(3,3,3,0.81)` blurred 16.35px, h=1129, w=317 — darkens left edge
5. **Created `.scratch/gorod-fm-research/`** directory + `designs/assets/gorod-fm/` directory for assets
6. **NO code changes** to `designs/gorod-fm.html` yet — this is purely intel gathering

---

## Strategy for next session

### Phase 1 — Asset acquisition (DO FIRST)

The Figma asset URLs from MCP expire in 7 days. **Re-pull all 5 design contexts** at the start of next session via parallel `mcp__figma__get_design_context` calls — that gives fresh URLs. Then download all unique images.

```
Parallel fetch:
- mcp__figma__get_design_context(2174:422)
- mcp__figma__get_design_context(2384:6054)
- mcp__figma__get_design_context(2385:2924)
- mcp__figma__get_design_context(2535:11151)
- mcp__figma__get_design_context(2537:14090)
```

For each context: extract all `https://www.figma.com/api/mcp/asset/<uuid>` URLs, dedupe (many tiles share assets across screens), then `curl -o designs/assets/gorod-fm/<descriptive-name>.png <url>` to local disk. Estimate 40-80 unique assets total.

**Naming convention:** `assets/gorod-fm/tile-pop-gold-2010s.png`, `assets/gorod-fm/artist-vadim-adamov.png`, `assets/gorod-fm/featured-egor-krid.png`, etc. Use Cyrillic-safe ASCII slugs.

### Phase 2 — Per-screen rewrite

Each of the 5 screens is a substantial rewrite (current implementations don't match Figma). Dispatch ONE implementer subagent per screen sequentially:

1. **`#/home` Главная** — full rewrite to match `2174:422`. Black bg + blurred radial particles + 9-tile horizontal row + center featured card + purple CTA bar + blue-tinted player bar. Most divergent screen — current has stations grid which Figma doesn't show.
2. **`#/podborki` Подборки** — keep current tile structure (geometry is right: 245/299/310/309/373 widths × 628 height + tile-tr-60 + rotated -90deg labels). ONLY add real images (replace gradient placeholders with downloaded photos from `2384:6054` assets). Big visual improvement for small effort.
3. **`#/library` Медиатека** — full rewrite to `2385:2924` Figma. Search bar + ABC alphabet filter row + 3-col artist grid (~205×205 photos). Drop current 2-row+ad-slot variant.
4. **`#/favorites` Раздел Избранное** — full rewrite to `2535:11151`. Multiple horizontal scrolling sections: DJ (8 cards 298×?) / Группы (6 cards 287 tall) / Исполнители (7 cards 286 with images).
5. **`#/artist` Страница артиста** — full rewrite to `2537:14090`. Artist photo card + track meta "Зацепила / Артур Пирожков" + lyrics block + station list (3 cols × 5 tracks).

Each rewrite = atomic commit. Don't push.

### Phase 3 — Verification

- Visually compare each rewritten screen vs Figma screenshot via Chrome MCP
- Forbidden-font check (`Inter|Roboto|Arial|Helvetica|Fraunces|system-ui`)
- File still parses; JS IIFE intact
- All 7 routes still navigable
- Player overlay still functional
- Tweaks panel still works

### Phase 4 — Standalone rebuild

Re-run `tools/build_gorod_fm_standalone.py` — now that local assets exist in `designs/assets/gorod-fm/`, the script will inline them as base64 data URIs. Standalone will become properly self-contained (~10-15 MB depending on photo sizes).

---

## What stays from v1

Don't touch these unless they conflict with the v2 rewrites:

- Skeleton structure (`@layer reset, tokens, base, layout, components, surfaces, utilities`)
- Player overlay (mini bar + full Monte Carlo from Task #2)
- Карта флоу `#/map` (internal review hub from Task #3)
- Страница трека `#/track` (Monte Carlo adapted from Task #8) — different node, not in user's complaint list
- Adaptable surface architecture (`data-surface="web|mobile|tv|carplay"` from Task #10)
- Tweaks panel
- Hash router
- Mobile responsive logic
- Bottom mini-player (will need restyling to match Figma blue-tinted variant on `#/home` though)

---

## Brand tokens — updated facts from Figma `2174:422`

| Token | v1 value | v2 fact (from Figma) |
|---|---|---|
| `--brand-black` | `#0C0B0B` | ✓ confirmed `#111111` aka `var(--black, black)` (Figma) |
| Active-chip background | `rgba(255,255,255,0.32)` (white) | **`rgba(81,104,252,0.2)`** (blue `#5168FC` 20%) — NEW |
| Featured CTA card bg | n/a | **`#2d2d5d`** purple — NEW |
| Player bar bg | `var(--surf-glass-20)` (white) | **`rgba(81,104,252,0.2)`** blue-tinted — NEW |
| `--brand-blue-light` | n/a | **`#5168FC`** (Figma "blue light") — NEW |
| Sidebar darkening | 240px solid black with 60% blur | Gradient `from-rgba(255,255,255,0.1) to-rgba(3,3,3,0.81)` blurred 16.35px, h=1129 w=317 left edge |

**Decision:** add `--brand-blue-light: #5168FC` to tokens. Active states (chips, player bar on `#/home`) use `rgba(81,104,252,0.2)` not glass-white.

---

## Sidebar nav items — confirmed from Figma `2174:422`

| Position | Label | Icon | Route | Active? |
|---|---|---|---|---|
| 1 | Лайвы | microphone (Player/Music Artist) | `#/lives` (NEW route — placeholder) | — |
| 2 | Подборки | podcast/microphone-lines-solid | `#/podborki` | ✓ blue gradient text in Figma when on this screen |
| 3 | Медиатека | (Icon Frame 2 — music-library shape) | `#/library` | — |
| 4 | Избранное | star (Vector) | `#/favorites` (or `#/artist`?) | — |

**Open question for next session:** in v1 we made sidebar's «Избранное» route to `#/artist` (artist profile) per Эльбик direction. Now we have BOTH artist profile (`2537:14090`) AND list (`2535:11151`) as distinct Figma screens. Decision: **«Избранное» sidebar → `#/favorites` (the list). Add secondary entry to artist profile from clicking an artist card in the favorites list.** This matches Figma structure (sidebar Избранное icon = star = collection).

**Лайвы:** new route stub for "live broadcasts" — currently no Figma design. Stub it with placeholder for prototype OR keep current Главная route there. Decision: **route #/lives → opens player overlay with live-radio meta (since this IS live radio platform). Quick stub for prototype.**

---

## Critical hygiene rules (carry over from v1)

- ❌ No Inter / Roboto / Arial / Helvetica / Fraunces / system-ui
- ✓ Onest fonts only (Actay Wide substituted via `scaleX(1.05) + letter-spacing 0.04em` on Onest 900)
- ✓ Hit targets ≥44px (≥56 on TV, ≥80 on CarPlay)
- ✓ `text-wrap: balance` on headings, `pretty` on paragraphs
- ✓ Focus-visible rings
- ✓ `prefers-reduced-motion` respected
- ✓ Atomic commits per screen, do NOT push
- ✓ Master direct (no feature branch)

---

## File pointers

- HTML: `designs/gorod-fm.html` (currently 10,274 lines at HEAD `77ee5c1`)
- Standalone: `designs/gorod-fm-standalone.html`
- New assets target: `designs/assets/gorod-fm/` (directory exists, empty)
- Scratch screenshots: `.scratch/gorod-fm-research/` (3 Figma PNGs from v1 — `gorod-home-2384-6054.png` / `mc-desktop-player-3314-13423.png` / `mc-mobile-player-3407-2224.png`)
- Build script: `tools/build_gorod_fm_standalone.py` (already supports local-asset inlining via base64)
- Predecessor handoff: `docs/superpowers/HANDOFF-gorod-fm.md` (v1 shipped)
- v1 review: `docs/superpowers/REVIEW-gorod-fm-2026-05-27.md`
- v1 session log: `.claude-memory/session_2026_05_27_gorod_fm_v1.md`

---

## TaskList state

Resume next session by reading this file. Recreate the TaskList for these tasks:

1. ⬜ Re-fetch 5 Figma design contexts in parallel (fresh URLs)
2. ⬜ Download & dedupe all unique image assets to `designs/assets/gorod-fm/`
3. ⬜ Rewrite `#/podborki` — keep structure, swap gradient placeholders → real photos (smallest delta, do first as warm-up)
4. ⬜ Rewrite `#/home` (`2174:422`) — full structural rewrite
5. ⬜ Rewrite `#/library` (`2385:2924`) — full structural rewrite
6. ⬜ Rewrite `#/favorites` (`2535:11151`) — full structural rewrite
7. ⬜ Rewrite `#/artist` (`2537:14090`) — full structural rewrite
8. ⬜ Add `--brand-blue-light: #5168FC` token + blue-tinted active chip/player variant on `#/home`
9. ⬜ Add `#/lives` placeholder route (sidebar item exists in Figma)
10. ⬜ Visual verify each screen via Chrome MCP
11. ⬜ Standalone rebuild (assets now inlined as base64)
12. ⬜ Update DEBT.md GOROD-021 → done, update session log + memory
