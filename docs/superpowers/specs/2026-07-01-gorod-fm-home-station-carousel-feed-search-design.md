# Design spec — Город ФМ home: РМГ station carousel + music витрина + search

**Date:** 2026-07-01 · **Surface:** `designs/gorod-fm.html` `#/home` only · **Branch:** `feat/gorod-home-rmg-storefront`
**Status:** owner-approved model (2026-07-01) → implementation plan next
**Research:** `docs/superpowers/RESEARCH-gorod-fm-home-carousel-feed-search.md` (wave-1) · `…-home-feed-frontier-wave2.md` (wave-2; the frontier recsys/personalization findings now apply to «Мой вкус», not the home — see §12)

## 0. Intent
Turn the home into a **lean-forward radio storefront + music витрина**: a hero carousel that IS the live эфир (tune across the РМГ family), a persistent live-aware player, and — on scroll — a **browse витрина of ALL music** (friends' recommendations, categories/genres, collections, editorial, charts, artists). **The home has NO AI/personalization** — the wave, steer, recommendations «для вас», taste, explainability all live in a dedicated **«Моя волна»** AI tab (the current `#/home` «Волна» experience relocated there; may consolidate with the existing «Мой вкус» `#/taste`). Skin unchanged; only the home's structure changes.

## 1. Locked decisions (owner, 2026-07-01)
1. **Dark skin kept** (`#0B0C0F` / accent `#5168FC` / Onest / anti-slop). Structure changes, not skin.
2. **Carousel = РМГ sibling stations** (a portal across the holding), flat, NO edge tilt.
3. **Carousel IS the эфир:** center card = the station playing now; side cards switch by scroll/click. No separate "now-playing" block.
4. **Home is NON-AI.** The wave, steer, «для вас» etc. move to a dedicated **«Моя волна»** AI tab (the current `#/home` «Волна» experience relocated; exact route/label + any consolidation with «Мой вкус» `#/taste` = IA follow-up, out of home scope). The carousel's Город ФМ card is a **plain live station like the others** (no wave/steer/«почему» on the home).
5. **Feed = a music-discovery витрина** (browse/editorial/social): categories, collections, friends, editorial, charts, artists — «выбираешь из всего что есть».
6. **Scope = `#/home` only.** Sidebar/tab IA, other routes, design system untouched.

## 2. Design system (reuse existing tokens — introduce none)
| Purpose | Token | Value |
|---|---|---|
| Page bg | near-black | `#0B0C0F` (confirm body-bg token at build) |
| Surfaces | `--surface-0/1/2/3` | `#111318` / `#15171D` / `#1B1E26` / `#23262F` |
| Text | `--text-pri` / `--text-sec` | `#FFFFFF` / `rgba(255,255,255,.62)` |
| Accent (large/icon) | `--brand-blue-light` | `#5168FC` |
| Accent (small text/focus, AA 6.8:1) | `--accent-on-dark` | `#8094ff` |
| Hairline / divider | `--hairline` / `--divider` | `rgba(255,255,255,.08)` / `.06` |
| Player bar height | `--player-mini-h` | `72px` |
| Font | Onest | — |

Anti-slop hard rules (DESIGN_PROTOCOL §2/§9): no gradient-fill backgrounds, no rotated text, no emoji, **no fabricated stats/counts**, single accent only, flat > skeuomorphic, `text-wrap` balance/pretty, concentric radii, hit targets ≥44px, WCAG AA (small accent text uses `--accent-on-dark`).

## 3. Information architecture (top → bottom)
```
[ sticky top bar ]   ГОРОД.FM · 🔍 persistent search · Личный кабинет
[ HERO carousel-эфир ]  ‹ Русское .82 ›  ▐ станция играет сейчас ▌  ‹ ХИТ FM .82 ›     flat, no tilt, 6 live stations
[ persistent player ]   docked bottom, live-aware (rides with feed scroll)
[ music витрина ]       ↓ browse shelves (§8): friends · categories · collections · editorial · charts · artists · (radio shows)
```
No AI on this surface. First screen = top bar + carousel + player; scroll reveals the витрина.

## 4. Top bar + persistent search
- Left: ГОРОД.FM wordmark. Right: Личный кабинет (existing account sheet).
- **Search = persistent field** (not an icon): desktop centered ~440px, h48, radius 12, `--surface-1` on page bg, glyph left, placeholder «Поиск станций, шоу, треков…» at 62% white; mobile = full-width pill above the hero. `/` or `Ctrl/Cmd+K` focuses. Focus → search overlay (§7). Focus ring 1px `--accent-on-dark`.

## 5. Hero carousel-эфир — live stations (NO AI)
**Roster (6, real — from `smartwatch-rmg.html` brand-book set):** Город ФМ *(default center)* · Русское Радио · ХИТ FM · DFM · MAXIMUM · Radio Monte Carlo. Real **logos = owner asset dependency** (§13); no fabricated FM numbers.

**Flat, NO edge tilt** (Apple retired 3D cover-flow): center card `scale(1)`/opacity 1; neighbors `scale(.82)`/`opacity(.45)`; horizontal offset only, **no rotation**.
- **Technique:** CSS `scroll-snap-type:x mandatory` + `scroll-snap-align:center`; `padding-inline:calc(50% - card/2)`; scale/fade via scroll-driven `animation-timeline: view(inline)` (opaque at 50% = centered); animate `transform`+`opacity` only (GPU). Thin JS = click-to-center, arrow keys, active-index, now-playing bind; IntersectionObserver `.is-centered` fallback (Firefox). Reuse the existing `.home-station` card CSS (icon/name/freq/active + tv/carplay/mobile variants) as the card base.

**Center card = the station playing now (SAME for all 6 — no special Город ФМ AI state):** station logo/name, freq (only where a real FM exists), `В ЭФИРЕ` pulsing dot, live now-playing `Track — Artist` from real ICY/Icecast `StreamTitle` (poll ~10s; fallback to station name, never invent), and basic controls: ♥ like / «в избранное» / share. **No steer / no «почему» / no wave here** — that AI experience relocates to the **«Моя волна»** AI tab. *(Implementation note: reuse the flat `.home-station` pattern; the former `#home-radio` AI wave is NOT wired into the carousel — it belongs to the «Моя волна» AI tab, not the home.)*

**Interaction:** tap a side card → `scrollIntoView({inline:'center',behavior:'smooth'})` → tune + cross-fade audio ~400ms («Подключение…») → player + card reflect it (single source of truth; one active card). **No autoplay on scroll; no hover audio preview.** **First load:** center = Город ФМ, NOT auto-playing (browser policy) — prominent play affordance; first gesture starts the stream. Keyboard: roving tabindex, ←/→ ±1, Home/End; Enter/Space plays. `prefers-reduced-motion` → kill scale/fade + `scroll-behavior:auto` + freeze equalizer. `role="group" aria-roledescription="карусель" aria-label="Радиостанции"`, cards in `<ul role="list">` as native buttons, centered card `aria-current="true"`.

## 6. Persistent live-aware player (reuse `.player-mini`, `--player-mini-h`)
Docked bottom, `<audio>` mounted across route changes (playback never drops).
- **Live:** NO scrubber/seek → `LIVE` badge (+ optional non-timeline equalizer). MediaSession registers **only** play/pause. Pause→resume **rejoins the live edge** (offer «Вернуться в эфир»; a Stop-square signals this). Controls: Play/Stop · Volume · ♥ Like (adds to favorites; the taste it feeds surfaces in the «Моя волна» AI tab, not here) · Share (track or station) · Recently-played · Favorite station. LIVE badge ⟂ progress bar.
- **On-demand mode** (a show replay opened from «Программы»): same component swaps to scrubber + 15/30s skip + resume-position + speed, keyed off an `isLive` flag.

## 7. Search overlay
On focus, a full-width panel over the hero. **Empty:** «Недавние запросы» (last ~8, ×-removable, «Очистить историю») + «Часто ищут» chips. **Typing (~160ms debounce):** «Лучший результат» card (96px art, name, type badge, inline Play) then grouped, capped sections with «Показать все →»: **Станции · Шоу и DJ · Жанры · Подборки · Треки и артисты** (radio-biased order; live stations get an accent dot). **Browse-all grid** = **real cover art on dark tiles** + `#0B0C0F` bottom scrim + Onest label; art-less genre tiles = `--surface-1` + 1px `--accent-on-dark`@12% + ghost letterform. **Never Spotify's rainbow tiles.** **Scopes** (sticky chips): «Всё · Станции · Треки · Артисты · Подборки · Подкасты». No-results = suggestion + fallback popular stations. Mobile overlay above the docked player; **opening search never stops playback**.

## 8. Music витрина (the feed — NON-AI browse storefront)
A storefront of ALL music: friends' recommendations, categories/genres, collections, editorial, charts, artists — the user browses «всё что есть» and picks manually. **No personalization/AI here** (that's «Мой вкус»). Frontier quality comes from world-class *browse* (rich categories, curated collections, editorial voice, social) — not from a recsys engine.

### 8.1 Shelf catalog (grouped; each shelf = a title + optional right-aligned «Все ›»)
**Друзья и социальное:** `Друзья слушают` — what friends play + their подборки (owner's core ask; **first-class shelf** — prototype shows clearly-representative example activity; the real version needs accounts + social graph + privacy defaults per 152-ФЗ; never present demo as real user stats).
**Категории («всякие категории»):** `Категории и жанры` — the browse-all system: жанры · настроения · активности · эпохи · языки (pick anything; the витрина of the whole catalog).
**Подборки и редакция («подборки»):** `Подборки` (ready-made collections/playlists — editorial + curated) · `Выбор редакции ГОРОДА` (human picks, brand voice) · `Коллекции` (deep rubrics — по десятилетиям / языку / городу).
**Каталог:** `Новинки` (new releases) · `Популярное · Чарты` (real counts or none) · `Исполнители` (browse by artist).
**Радио-контент (minor accent — эфир is the carousel):** `Программы и ведущие` (radio shows/DJs, daypart badge «сейчас»/«в 18:00»; opening a replay → player on-demand mode).

### 8.2 Ordering
Editorial / curated order — the **same for everyone** (no personalization). Order may lightly refresh by day-of-week / time-of-day for *editorial* freshness (e.g. «Новинки» on Fridays) using only real calendar signals — never per-user. Empty/thin shelves are **hidden, never padded** with filler (honesty = anti-slop). `Все ›` opens a full vertical grid landing.

### 8.3 Honesty (enforced in code)
- **No fabricated counts anywhere** (no «2,3 млн слушают», no «тренд #1»); a real listeners/plays number appears only if it's an actual value, else omit.
- `Друзья слушают`: representative/example content in the prototype, clearly framed; real friend activity requires a social graph + privacy consent; never dress demo as real.
- Categories, collections, charts, new = real catalog content (owner-supplied); placeholders where assets are pending (§13), asked for, not faked.

### 8.4 Density, geometry, headers
Horizontal shelves default (vertical grids only for `Все ›` landings). 10–20 items/shelf; **peeking half-card** (mobile ≈2.2, desktop ≈5–6). **Vary card geometry per shelf:** stations=circle, categories/moods=square, shows=16:9, collections=1:1, artists=circle, tracks=thumb+text rows; occasional full-bleed spotlight. Header = Title (Onest ~18–20 semibold) + optional muted subtitle (~13) + right-aligned `Все ›`. Separate shelves with whitespace + a consistent left gutter — **no divider lines, boxed cards, or colored section backgrounds**. Lazy-load via IntersectionObserver (skeletons on mount). Accent used sparingly (live dot, `Все ›` hover).

## 9. Data model
- **Station** `{id, name, freq?, logo, streamUrl?, kind:'live'}` (all 6 equal; no flagship-AI flag).
- **NowPlaying** `{title, artist, source:'icy'|'demo', ts}` — `source:'demo'` renders honestly (representative, never a fabricated stat).
- **Shelf** `{id, title, kind:'friends'|'category'|'collection'|'editorial'|'catalog'|'radio', items[], seeAllHref?}`.
- **Card** `{kind:'station'|'track'|'collection'|'category'|'artist'|'show', art, title, subtitle, badge?}`.
- Honesty invariant: any count/label traces to a real value or owner-supplied content, else it does not render.

## 10. States & edge cases
No history needed (витрина is the same for everyone). No ICY metadata → station name, never invented track. First load → paused, gesture-to-play. `prefers-reduced-motion` → static carousel + frozen equalizers. Mobile → carousel center + peeking, search pill above hero, single-column swipe shelves, docked player. Standalone build → inline assets; demo now-playing/friends honestly framed; `localStorage` for last-station/route/tweaks.

## 11. Scope & non-goals
IN: `#/home` structure — carousel, live-player upgrade, витрина feed, search. OUT: all other routes; the sidebar/tab IA + labels; the **«Моя волна»** AI tab (the relocated wave/steer + «для вас»/Дежавю/taste/explainability; may consolidate with the existing «Мой вкус» `#/taste`) — hosts ALL AI/personalization; building/redesigning that AI tab is out of the home scope; the home only *links* there; real backend ML/ICY/social (wired when available); the cont-17 chat-layer (independent). Repo shared with Twinr → stay on `feat/gorod-home-rmg-storefront`, keep isolated.

## 12. Deviations from research (documented)
- **Home is NON-AI; feed = a music-browse витрина** (owner, 2026-07-01). All AI/personalization → the **«Моя волна»** AI tab. Consequence: wave-2's frontier recsys/personalization findings (BaRT shelf meta-ranking, per-user adaptive order, explainable «почему»+control, signal schema, «Моя волна», «Дежавю», exploration) **do NOT apply to the home** — they are retained for the «Моя волна» AI tab and captured in `RESEARCH-…-frontier-wave2.md`. The home витрина keeps only the *browse/editorial/social* insights (categories, curated collections, editorial voice, honest handling).
- **Carousel Город ФМ = plain live station** (owner). No wave/steer/«почему» on the home; the AI radio experience lives in the «Моя волна» AI tab.
- **РМГ siblings in the carousel** (owner) overrides wave-1's "de-emphasize siblings"; the carousel is the station directory, so no separate "stations" shelf in the feed.

## 13. Assets & open dependencies (owner/client)
1. **Real logos** for the 6 stations (have Monte Carlo; need Русское Радио / ХИТ FM / DFM / MAXIMUM — brand books B018; Город ФМ mark exists).
2. **Город ФМ frequency** (if any) — else name-only card.
3. **Live stream URLs + ICY metadata** availability — else now-playing is representative/honestly-labeled.
4. **Catalog content** for the витрина (categories, collections, editorial picks, new/charts, artist list) — owner/client feed, or representative placeholders labeled as such.
5. Friends/social: representative in prototype until accounts + social graph exist.

## 14. Acceptance criteria (falsifiable)
- [ ] Carousel: 6 live stations, center focused, neighbors scaled+faded, **zero rotation**; snap-to-center; keyboard + touch + click-to-center; no autoplay; reduced-motion safe; Firefox fallback works. **All cards identical behavior — no special AI state on Город ФМ.**
- [ ] Center card = the playing station's live now-playing + like/favorite/share; switching cross-fades and updates the player (one active). No steer/«почему»/wave anywhere on the home.
- [ ] Player: LIVE badge, no scrubber on live, MediaSession play/pause only, survives route changes.
- [ ] Search: persistent, `/`/Ctrl-K, typeahead + scopes, mono-accent browse grid (no rainbow), never stops playback.
- [ ] Витрина: `Друзья слушают` + `Категории и жанры` + `Подборки` + `Выбор редакции` + `Новинки` + `Популярное` + `Коллекции` + `Исполнители` + `Программы` render; varied card geometry; `Все ›`; **no AI/personalization shelves on the home**; **no fabricated counts**; empty shelves hidden.
- [ ] Anti-slop gate (DESIGN_PROTOCOL §2/§9) passes; single accent; Onest; WCAG AA; verified via `design-implementation-reviewer`.
- [ ] `#/home` only; other routes byte-unaffected; standalone rebuilt.

## 15. Build phasing (detail → implementation plan)
P1 **Carousel-эфир** (roster + flat no-tilt; reuse `.home-station`; strip the AI center state; all 6 equal live cards) → P2 **live-aware player** (`.player-mini` + MediaSession + `isLive` + cross-fade) → P3 **search** (persistent + overlay + mono browse grid) → P4 **витрина feed** (shelf component + the §8.1 non-AI shelves + varied geometry + `Все ›` + honest states) → P5 **anti-slop + reviewer pass + standalone regen**. Each step: `node --check` / `check_scripts.cjs` + Chrome verify + atomic commit.
