# HANDOFF — Город ФМ HTML SPA (kickoff)

**Updated:** 2026-05-27 17:36
**Resume command:** `resume design` → RESUME_PROMPT.md routes here → continue from `## NEXT`
**Branch:** `master` (direct push convention — НЕ feature branch; bootstrap-port worktree остаётся как было, не трогать)

## What this is

Single-file hi-fi clickable HTML SPA для нового клиента **Город ФМ** (онлайн-радио платформа). Эстетика — Город ФМ existing brand-blue cinematic + **Monte Carlo-style player overlay** (заказчик любит Monte Carlo, не любит текущий мобильный плеер Город ФМ). По образцу design-project's `twinr-liquid-glass.html` / `showcase-aggregator.html` (single-file + hash router + центр-hub). **НЕ paws-data** — только методологический pattern из mkt prototypes.

**Future surfaces:** web sites, mobile apps, TVs, CarPlay. Structure должна быть **адаптируемая** с day-1 через `data-surface="..."`.

## Sources of truth

### Figma — Город ФМ
- File: `ODcQ2ERWYi3w504Z86TOy3` (город фм 2 (Copy))
- Page: `2001:297` (название «превью»)
- Hero reference screen: `2384:6054` — «Подборки» desktop 1920×1074 (это **единственный** dev'd экран в Figma; остальные проектируем мы по brief)
- URL: https://www.figma.com/design/ODcQ2ERWYi3w504Z86TOy3/...?node-id=2384-6054

### Figma — Monte Carlo (player reference)
- File: `l38kZVrZXzdNlBIIOLFX4g`
- Section: `3314:29960` «Плеер»
- Desktop player: `3314:13423` (1440×900)
- Lyrics view: `3314:14890`
- История view: `3314:15114`
- Mobile player: `3407:2224` (375×828)
- Mobile lyrics: `3332:16813`
- Mobile история: `3407:1969`
- Mobile player loading: `3407:1755`

### Photo reference (mobile bottom)
- `C:\Users\elbics\Desktop\photo_2026-05-27_17-27-05.jpg` — Monte Carlo mobile bottom: sticky teal-tinted track card (AMA / Eros Ramazzotti / play / heart) + 5-icon tabbar (crown/antenna/news/gallery/burger) над warm sunset gradient. **Это reference для mobile player + bottom-nav стиля.**

### Downloaded screenshots (preserved)
- `.scratch/gorod-fm-research/gorod-home-2384-6054.png` (1920×1074)
- `.scratch/gorod-fm-research/mc-desktop-player-3314-13423.png`
- `.scratch/gorod-fm-research/mc-mobile-player-3407-2224.png`

## Brand tokens (extracted)

### Город ФМ — dark cinema (primary palette)

| Token | Value |
|---|---|
| `--brand-cyan` | `rgb(86, 175, 215)` |
| `--brand-blue` | `rgb(26, 107, 222)` |
| `--brand-deep` | `rgb(21, 82, 172)` |
| `--brand-ink` (overlay tint) | `rgb(30, 27, 46)` |
| `--brand-black` | `#0C0B0B` |
| `--surf-glass-20` | `rgba(255,255,255,0.20)` (chips, pills, player bar) |
| `--surf-glass-12` | `rgba(255,255,255,0.12)` |
| `--text-pri` | `#FFFFFF` |
| `--text-sec` | `rgba(255,255,255,0.70)` |
| `--text-quat` (Apple sec-dark) | `rgba(235,235,245,0.60)` |
| `--r-base` | `10px` |
| `--r-tile-tr` | `60px` (top-right corner ONLY) |
| `--r-pill` | `999px` |

```css
--bg-base: linear-gradient(-90deg, var(--brand-cyan) 0%, var(--brand-blue) 49.519%, var(--brand-deep) 100%);
--bg-overlay: linear-gradient(-88.75deg, rgba(30,27,46,0) 72.913%, rgba(30,27,46,0.3) 86.553%, rgba(30,27,46,0.5) 99.397%);
--tile-shade: linear-gradient(124.4deg, rgba(0,0,0,0) 39.815%, rgba(0,0,0,0.4) 65.624%, rgba(0,0,0,0.4) 80.293%);
```

### Monte Carlo — warm sunset (player overlay variant)

| Element | Token / Value |
|---|---|
| Backdrop | photo + `backdrop-filter: blur(30px); background: rgba(255,255,255,0.01)` |
| Center album | 261×261 |
| Track title | Gilroy Medium 24px `#EAF0FF` |
| Artist | Gilroy Regular 16px `rgba(255,255,255,0.7)` uppercase |
| Side track previews (carousel) | Gilroy Medium 24px |
| Action label | SF Pro Regular 15px `rgba(235,235,245,0.6)` tracking -0.4 |
| Action icon | SF Pro Symbols 20px |
| Time | Gilroy Regular 12px white |
| Prev / Pause / Next | 44×44 / gap 60px |
| Back + «Назад» top-left | SF Pro 19px `rgba(255,255,255,0.96)` |

## Fonts — Holy Grail compliant

❌ **Запрещены:** Inter / Roboto / Arial / Helvetica / Fraunces / system-ui (см. `DESIGN_PROTOCOL.md` Часть 2.1).
Figma uses: Actay Wide Bold (display, Город ФМ logo + vertical tile labels) + SF Pro Display + Gilroy (Monte Carlo).

**Decision (web-safe substitutes):**
- **Display** (logo + tile labels rotated -90°): **`Onest` weight 900** + `letter-spacing: 0.04em` + `transform: scaleX(1.05)` — fake wide-bold close to Actay Wide proportions. Alt вариант: `Bebas Neue` (Google Fonts, condensed heavy).
- **Body** (nav / chips / track-meta / actions): **`Onest`** 400/500/600/700 (Google Fonts). Подменяет SF Pro Display и Gilroy.
- **Numbers** (time, scrubber): `Onest` tabular-nums.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;900&display=swap" rel="stylesheet">
```

## Screen list (build order)

| # | Route | Screen | Source |
|---|---|---|---|
| 1 | `#/map` | **Flow Map / Index** — карточки всех экранов с thumbnail-style backgrounds, click → hash route. Internal review only, hide in prod build. | По образцу design-project's index/hub pattern (showcase-aggregator). |
| 2 | `#/home` | **Главная** — radio stations grid + filter chips (РОК/ДИСКО/ПОП/ХИП-ХОП/ЕЩЁ) top + центр-cover текущего трека + round expand-button в углу → bottom drawer с queue/file по меню слева | brief; UX «ещё не додумали как сделать» — propose 2 варианта Tweak |
| 3 | `#/podborki` | **Подборки** — gallery tiles row (245/299/310/309/373×5 widths, 628 height, `border-top-right-radius:60px`, label rotated -90° «POP GOLD 2010s / K-POP / CHILL / ДИСКАЧ 90-Х / Z. CITY SHOW / VADIM ADAMOV / DJ PITKIN / DFM CHILL …»). Mobile = 2-row carousel. | Figma `2384:6054` ground truth |
| 4 | `#/library` | **Медиатека** — **2-row grid + ad slot** (заказчик: «не понятно надо ли в 3 ряда — попробовать в 2 ряда и оставить блок под рекламу»). Mobile single column. | brief |
| 5 | `#/artist` | **Избранное (артист профайл)** — hero фото + bio + tracks + станции артиста | brief: «профиль артиста — названо избранным» |
| 6 | `#/track` | **Страница трека** — Monte Carlo desktop card (album cover 261 + title 24 + actions row + scrubber + prev/play/next + close X) + mobile carousel previews + lyrics + история | Figma Monte Carlo `3314:13423` + `3407:2224`; adapt warm → cinema tokens |
| 7 | `#/favorites` | **Раздел Избранное** — list избранных tracks / artists / playlists / станций + фильтры по типу | brief: «раздел избранное» отдельно от профиля артиста |

## Persistent components

- **Topbar** (web only): `<Город.fm>` logo + Search icon-pill + «Личный кабинет» pill (`--surf-glass-20`, h-52, r-10)
- **Sidebar** (web only): Главная / Подборки / Медиатека / Избранное (icons + labels 17px) + footer entry «Карта флоу» (internal)
- **Player mini bar** (bottom): skip-back / play / skip-forward + image 60×60 r-10 + title 24px Medium + subtitle 16px Regular + share + volume slider. Click anywhere on mini → expands to full overlay.
- **Player full overlay**: mobile = full-screen Monte Carlo style; desktop = centered modal Monte Carlo style. Both with warm sunset backdrop + center cover 261 + carousel previews + поделиться/текст-песни/история actions + scrubber + prev/play/next + close X.
- **Mobile bottom tabbar**: 5 icons (Главная / Подборки / Медиа / Избранное / Плеер). Hide on web ≥1024px.
- **Tweaks panel** (internal review, bottom-right floating): theme variants (cinema / warm / light) + surface variants (web / mobile / tv / carplay). localStorage persist `gorod-fm.theme`, `.surface`, `.last-route`.

## Adaptable surface architecture

Через `data-surface="web|mobile|tv|carplay"` на `<html>`:

| Surface | Layout |
|---|---|
| `web` | desktop sidebar + topbar + main + mini-player bottom |
| `mobile` | hidden sidebar/topbar; bottom tabbar; full-screen player overlay; collapsed mini |
| `tv` | 10-foot viewing: 1920+ canvas, ≥56px hits, focus-visible 3px ring на каждом interactive, big text (24px+), arrow-key nav |
| `carplay` | high-contrast, audio-first, ≥80px tap, minimal motion, voice-friendly stub |

CSS Custom Properties + container queries для responsive primitives. CSS layers: `@layer reset, tokens, base, layout, components, surfaces, utilities`.

## NEXT (resume here)

1. `cd ~/Desktop/design-project` · `git fetch && git pull` · `git log --oneline -5` (kickoff commit `gorod-fm: kickoff…` должен быть на топе).
2. **Read this file** + `.claude-memory/session_2026_05_27_gorod_fm_kickoff.md` + `.scratch/gorod-fm-research/*.png`.
3. Invoke `superpowers:subagent-driven-development`. **One implementer at a time** (shared git index — не параллелить).
4. **Build `designs/gorod-fm.html`** — single-file SPA. Skeleton:
   - `<head>`: meta + Onest Google Fonts link + inline CSS (`@layer reset/tokens/base/layout/components/surfaces/utilities`)
   - `<body>`:
     - 2× `.bg-layer` (cinema + warm — animated swap by `[data-theme]`)
     - `<header class="topbar">` (`[data-surface=web]:block; mobile:hidden`)
     - `<aside class="sidebar">` (web only)
     - `<main>` containing 7 `<section data-page="X">`, only `[data-page-current]` visible
     - `.player-mini` + `.player-full` (data-expanded toggle)
     - `<nav class="mobile-tabbar">` (mobile only)
     - `.tweaks` (internal review panel)
   - `<script>`: hash router + player toggle + tweak handler + localStorage persist
5. Build screens 1→7 per build order. Atomic commits per screen.
6. Mobile responsive 375/414/768/1024 — fix gallery (user complaint), mobile player = Monte Carlo overlay.
7. Standalone build `tools/build_gorod_fm_standalone.py` (base64 inline backdrop + any local PNGs).
8. Anti-slop pass via `compound-engineering:design:design-implementation-reviewer` (Holy Grail Часть 9 чек-лист).
9. Update `DEBT.md` GOROD-004..018 as you progress.
10. Session log в `.claude-memory/session_2026_05_27_gorod_fm_v1.md`.

## TaskList state (at kickoff handoff)

- ✅ #1 Acquire Figma context (gorod-fm + Monte Carlo metadata/screenshots/design_context)
- ✅ #2 Probe other Город ФМ screens (none exist beyond 2384:6054 — design rest ourselves)
- ✅ #3 Brief Questions Gate (брифа достаточно — Figma + photo + screen list + future surfaces)
- ⬜ #4 Design tokens — **entry point next session**: переписать tokens из этого doc в CSS блок файла
- ⬜ #5 Build Flow Map / Index page
- ⬜ #6 Build Главная
- ⬜ #7 Build Подборки
- ⬜ #8 Build Медиатека
- ⬜ #9 Build Избранное (артист + раздел)
- ⬜ #10 Build Страница трека
- ⬜ #11 Build Player overlay (mini bar + full Monte Carlo)
- ⬜ #12 Mobile responsive pass
- ⬜ #13 Adaptable surface architecture
- ⬜ #14 Anti-slop + WCAG via reviewer agent
- ⬜ #15 Standalone build + commit + DEBT update

## Carry-forward decisions

1. **NO paws data** — конструктивно зеркалить только pattern «single-file SPA + hash router + index hub» из mkt/showcase prior prototypes. НЕ контент / НЕ цвета paws / НЕ Sofia / НЕ GAP memos.
2. **Onest substitute for SF Pro / Gilroy** — Holy Grail compliant. Fake-wide для display.
3. **Asset strategy V1**: gradient + heavy display typography для tiles (Figma URLs expire 7 days). Real assets когда заказчик пришлёт.
4. **Themes**: dual primary (cinema для app + warm для player overlay), light theme optional Phase 2.
5. **Variations as Tweaks** (Holy Grail Часть 3.2): один файл с переключателем, НЕ N тематических файлов.
6. **Master branch direct** (как kinolog/rutv/showcase/crm-glass — solo dev). НЕ feature branch.
7. **Bootstrap-port worktree остаётся paused** — Twinr Phase 4 не блокирует Город ФМ; заказчик ждёт Город ФМ. Bootstrap-port HANDOFF (`HANDOFF-bootstrap-port.md`) preserved.
8. **Round expand-button в углу → bottom drawer** на Главной — заказчик: «ещё не додумали как сделать и может по другому надо будет». Predложить 2 варианта Tweak (corner FAB → bottom-sheet vs sidebar slide-out drawer).
9. **Mobile gallery бaд в текущем Figma** — заказчик: «стремно выглядит». Fix через горизонтальный snap-scroll carousel + 2-row на mobile (не 3-row 3-column кучу).
