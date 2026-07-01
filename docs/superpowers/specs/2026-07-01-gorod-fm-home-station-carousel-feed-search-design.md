# Design spec — Город ФМ home: РМГ station carousel + frontier discovery feed + search

**Date:** 2026-07-01 · **Surface:** `designs/gorod-fm.html` `#/home` only · **Branch:** `feat/gorod-home-rmg-storefront`
**Status:** awaiting owner review → then implementation plan (writing-plans)
**Research:** `docs/superpowers/RESEARCH-gorod-fm-home-carousel-feed-search.md` (wave-1) · `…-home-feed-frontier-wave2.md` (wave-2, feed frontier)

## 0. Intent
Turn the home from a lean-back single-stream "Волна" into a **lean-forward radio storefront**: a hero carousel that IS the live эфир (tune across the РМГ family), a persistent live-aware player, and — on scroll — a **frontier, explainable music витрина** (friends' recommendations, categories/genres, collections, personal picks — a storefront of all music). The AI-radio wedge is preserved (Город ФМ's own card = the AI wave; «Моя волна» is a feed shelf). Skin unchanged; only the home's structure changes.

## 1. Locked decisions (owner, 2026-07-01)
1. **D1 — keep the shipped dark skin** (`#0B0C0F` / accent `#5168FC` / Onest / anti-slop). Structure changes, not skin.
2. **D2 — carousel = РМГ sibling stations** (a portal across the holding), not internal themed streams.
3. **Model — the carousel IS the эфир:** center card = station playing now; side cards switch by scroll/click. No separate "now-playing" block. Feed is the continuation on scroll-down.
4. **Scope — `#/home` only.** Every other route, the sidebar/tab IA, and the design system stay untouched.
5. **Feed — must be best-in-class / frontier** (owner directive) — see §8.

## 2. Design system (reuse existing tokens — do NOT introduce new ones)
| Purpose | Token | Value |
|---|---|---|
| Page bg | near-black | `#0B0C0F` (confirm exact body-bg token at build) |
| Surfaces | `--surface-0/1/2/3` | `#111318` / `#15171D` / `#1B1E26` / `#23262F` |
| Text | `--text-pri` / `--text-sec` | `#FFFFFF` / `rgba(255,255,255,.62)` |
| Accent (large/icon) | `--brand-blue-light` | `#5168FC` |
| Accent (small text / focus, AA 6.8:1) | `--accent-on-dark` | `#8094ff` |
| Hairline / divider | `--hairline` / `--divider` | `rgba(255,255,255,.08)` / `.06` |
| Player bar height | `--player-mini-h` | `72px` |
| Font | Onest (weights already loaded) | — |

Anti-slop hard rules (DESIGN_PROTOCOL §2): no gradient-fill backgrounds, no rotated text, no emoji, **no fabricated stats/counts**, single accent only, flat > skeuomorphic, `text-wrap: balance`/`pretty`, concentric radii, hit targets ≥44px, WCAG AA. Small accent text uses `--accent-on-dark`, not raw `#5168FC` (which is 4.25:1).

## 3. Information architecture (top → bottom)
```
[ sticky top bar ]  ГОРОД.FM · 🔍 persistent search · Личный кабинет
[ HERO carousel-эфир ]  ‹ Русское .82 ›  ▐ ГОРОД.FM (center = playing now) ▌  ‹ ХИТ FM .82 ›   (flat, no tilt)
[ persistent player ]   docked bottom, live-aware (rides with feed scroll)
[ discovery feed ]      ↓ frontier shelves (§8), adaptive order, provenance + honest "why" + control
```
First screen (above fold) = top bar + carousel + player. Scroll reveals the feed.

## 4. Top bar + persistent search
- Left: ГОРОД.FM wordmark. Right: Личный кабинет (existing account sheet).
- **Search = persistent field** (not an icon): desktop centered ~440px, h48, radius 12, `--surface-1` on page bg, glyph left, placeholder «Поиск станций, шоу, треков…» at 62% white; mobile = full-width pill pinned above the hero. `/` or `Ctrl/Cmd+K` focuses from anywhere. Focus → expands into the search overlay (§7). Focus ring 1px `--accent-on-dark`.

## 5. Hero carousel-эфир (THE hero)
**Roster (6, real — from `smartwatch-rmg.html` brand-book set):** Город ФМ *(default center)* · Русское Радио · ХИТ FM · DFM · MAXIMUM · Radio Monte Carlo. Real station **logos are an owner asset dependency** (§13); no fabricated FM numbers.

**Flat, NO edge tilt** (the ask; Apple retired 3D cover-flow): center card `scale(1)`/opacity 1; neighbors `scale(.82)`/`opacity(.45)`; horizontal offset only, **no rotation**.
- **Technique:** CSS `scroll-snap-type:x mandatory` + `scroll-snap-align:center`; `padding-inline:calc(50% - card/2)` so first/last reach center; scale/fade via scroll-driven `animation-timeline: view(inline)` (keyframe opaque at 50% = centered). Animate `transform`+`opacity` only (GPU). Thin JS owns click-to-center, arrow keys, active-index, and the now-playing bind; an IntersectionObserver `.is-centered` toggle is the fallback where scroll-driven animations are unsupported (Firefox stable). Reuse the existing `.home-station` card CSS (icon/name/freq/active + tv/carplay/mobile variants) as the card base.

**Center card = now-playing, two states:**
- **Город ФМ active (default):** the current AI experience, kept verbatim — refactor `#home-radio` (home-wave canvas + «почему играет» + like / steer / skip) into this center-card state. This is the wedge, first-class.
- **Sibling active:** live now-playing — `Track — Artist` from real ICY/Icecast `StreamTitle` (poll ~10s; fallback to station name, never invent) + `В ЭФИРЕ` pulsing dot + ♥ like + «в избранное». **No steer** (it's their stream).

**Interaction:** tap a side card → `scrollIntoView({inline:'center',behavior:'smooth'})` → tune + cross-fade audio ~400ms (`Подключение…` state) → player + card reflect it (single source of truth; one active card). **No autoplay on scroll**; **no hover audio preview**. **First load:** center = Город ФМ, NOT auto-playing (browser policy) — prominent play affordance; first gesture starts the live stream. Keyboard: roving tabindex, ←/→ move active ±1, Home/End; Enter/Space plays. `prefers-reduced-motion` → kill scale/fade + `scroll-behavior:auto` (instant center) + freeze equalizer. `role="group" aria-roledescription="карусель" aria-label="Радиостанции"`, cards in `<ul role="list">` as native buttons, centered card `aria-current="true"`.

## 6. Persistent live-aware player (reuse `.player-mini`, `--player-mini-h`)
Docked bottom, mounted across route changes (keep the `<audio>` element alive so playback never drops).
- **Live:** NO scrubber/seek → `LIVE` badge (+ optional non-timeline equalizer). MediaSession registers **only** play/pause (no seek handlers). Pause→resume **rejoins the live edge** (offer «Вернуться в эфир»; a Stop-square, not Pause, signals this). Controls: Play/Stop · Volume · **♥ Like (feeds the AI engine)** · Share (track or station) · Recently-played · Favorite station. LIVE badge ⟂ progress bar (they never co-exist).
- **On-demand mode** (a show replay from the feed): same component swaps to scrubber + 15/30s skip + resume-position + speed, keyed off an `isLive` flag.

## 7. Search overlay
On focus, a full-width panel over the hero. **Empty:** `Недавние запросы` (last ~8, ×-removable, «Очистить историю») + `Часто ищут` chips. **Typing (debounce ~160ms):** a «Лучший результат» card (96px art, name, type badge, inline Play) then grouped, capped sections with «Показать все →»: **Станции · Шоу и DJ · Жанры · Подборки · Треки и артисты** (order radio-biased; live stations get an accent dot). **Browse-all grid** = **real cover art on dark tiles** + `#0B0C0F` bottom scrim + Onest label; genre tiles without art = `--surface-1` + 1px `--accent-on-dark`@12% + ghost letterform. **Never Spotify's rainbow tiles** — accent spent only on meaning. **Scopes** (sticky chips): `Всё · Станции · Треки · Артисты · Подборки · Подкасты` (Всё floats stations/live above tracks). No-results = suggestion + fallback popular stations (never a dead end). Mobile overlay sits above the docked player (`padding-bottom` = player h + safe-area); **opening search never stops playback**.

## 8. Discovery feed — FRONTIER (the owner's focus)
The feed is a **music-discovery витрина** — a storefront of ALL music: friends' recommendations, categories/genres, collections, and personal picks, so the user browses «всё что есть» and picks what they like. Radio/эфир lives in the carousel above; radio shows are one minor accent shelf, not the focus. On top of that витрина we layer the frontier make-it-best-in-class mechanics — **explainable, steerable, context-aware, honest** (the 2025-26 frontier: Spotify "steer the algorithm", Apple algo-torial, Yandex Моя волна, DSA Art. 27) — which is 1:1 with Город ФМ's wedge.

### 8.1 Canonical shelf catalog — a витрина of ALL music (each shelf = provenance chip + one honest "why" + one control)
The feed is a **music-discovery storefront**: friends' recommendations, categories/genres, collections, and personal picks — the user browses «всё что есть» and picks what they like. Radio shows are one minor accent shelf; radio/эфир itself is the carousel above. Provenance chips: **`Друзья` · `Подбор ИИ` · `Куратор` · `Микс`**.
**Друзья и рекомендации (lead — the owner's core ask):** `Друзья слушают` (what friends play + their подборки; **first-class shelf** — prototype shows clearly-representative example activity, the real version needs accounts + social graph + privacy defaults per 152-ФЗ; never present demo as real user stats) · `Для вас` / `Потому что вы слушали…` (personalized picks) · `Моя волна` (AI adaptive stream + dials настроение/язык/активность; reuses `TwinrWave`/`GorodContext`) · `Дежавю` (from your own history).
**Категории и жанры («всякие категории»):** `Категории и жанры` (the browse-all system — жанры · настроения · активности · эпохи · языки; pick anything, витрина of the whole catalog) · `Не ваш обычный выбор` (labeled exploration/serendipity ~20-30%).
**Подборки и редакция («подборки»):** `Подборки` (ready-made collections/playlists — editorial + algorithmic) · `Выбор редакции ГОРОДА` (human picks; leads cold-start) · `Новинки` · `Популярное · Чарты` (real counts or none) · `Коллекции` (deep rubrics — по десятилетиям / языку / городу).
**Артисты:** `Исполнители` (browse by artist).
**Радио-контент (minor accent — эфир is the carousel):** `Программы и ведущие` (radio shows/DJs, daypart badge «сейчас»/«в 18:00») · optional `Из эфира — песни` (save the tracks the stations just played — the live-radio ↔ music bridge).

### 8.2 Adaptive shelf selection & ordering (the frontier move)
Meta-rank the SHELVES, not just cards (Spotify BaRT: the shelf title is the explanation AND the constraint). MVP is fully client-side and ships in the single-file SPA:
1. Per-shelf candidate generators (continue / station-affinity / co-occurrence / fresh / editorial).
2. Linear item scorer `w·affinity + w·freshness − w·repetition − w·recent_skip + w·tod_match`; per-shelf top-K then greedy **MMR diversity**.
3. **Shelf meta-ranker** `shelf_score = mean(topItemScores) × type_prior × context_boost × novelty`; **ε-greedy (ε≈0.15)** promotes one uncertain/fresh shelf; suppress a shelf shown top last session.
4. **Order visibly adapts by time-of-day** with a real timestamp: «Обновлено 07:14 · утренний эфир». Cold-start / thin signal → editorial-only, relabeled honestly.
5. Thin shelves are **hidden, never padded** (honesty = anti-slop). Scale path (GBDT → two-tower → LinUCB) swaps scorers behind the same UI.

### 8.3 Honesty & transparency (headline feature, DSA-aligned)
- Every shelf title / per-card «Почему?» derives from a **real logged signal only** — «Потому что вы часто слушаете Монте-Карло по вечерам», «Та же станция, что в эфире, но спокойнее». Thin signal → degrade to «Выбор редакции» / «Популярное»; never fake personalization.
- **Every explanation ships with a control** («Меньше такого» / dials / genre toggles) — explanation without a lever is theater.
- Surface exploration as trust: «Пробуем для вас — может, зайдёт» (not hidden).
- A plain «Как работает подбор» page + a **«Только редакция» non-profiling mode**.
- **No fabricated counts anywhere** (no «2,3 млн слушают», no «тренд #1»); a live listeners number appears only if it's a real value, else omit.

### 8.4 Density, geometry, headers
Horizontal shelves default (vertical grids only for `Все ›` landings). 10–20 items/shelf; **peeking half-card** (mobile ≈2.2, desktop ≈5–6). **Vary card geometry per shelf** to break the identical-wall: stations=circle, moods=square, shows=16:9, collections=1:1, tracks=thumb+text rows; occasional full-bleed spotlight. Header = Title (Onest ~18–20 semibold) + provenance chip + muted "why" (~13) + right-aligned `Все ›`. Separate shelves with whitespace + a consistent left gutter — **no divider lines, boxed cards, or colored section backgrounds**. Lazy-load shelves (IntersectionObserver + skeletons).

### 8.5 Signal schema (log day one — can't backfill)
Append-only event envelope in localStorage (beacon to backend later):
`{ts, session_id, user|anon, type: play_start|play_30s|play_complete|skip|like|station_switch|hide|shelf_impression|card_click|search, entity:{kind,id}, context:{surface, shelf_id, slot_index, tod_bucket, dow, device}, value:{listen_ms,pct,skip_at}, propensity: ε_at_serve, was_explore}`. Reward = `play_30s`; fast-skip (<30s) = negative. Derive an EMA-decayed affinity vector + `last_seen` recency map.

## 9. Data model
- **Station** `{id, name, freq?, logo, streamUrl?, isFlagship(Город ФМ), kind:'live'}`.
- **NowPlaying** `{title, artist, source:'icy'|'demo', ts}` — `source:'demo'` renders honestly (representative, never a fabricated stat).
- **Shelf** `{id, title, provenance:'Эфир'|'Подбор ИИ'|'Куратор'|'Микс', why:{template, evidence:[eventIds]}, control, items[], minSignal}`.
- **Card** `{kind:'station'|'track'|'show'|'collection', art, title, subtitle, badge?, why?}`.
- Honesty invariant: any `why`/count must trace to a real event or defensible computed similarity, else it does not render.

## 10. States & edge cases
Cold-start (no history) → carousel + 100% editorial feed, no faked personalization. No ICY metadata → station name, no invented track. First load → paused, gesture-to-play. `prefers-reduced-motion` → static carousel + frozen equalizers. Mobile → carousel center + peeking, search pill above hero, single-column swipe shelves, docked player. Standalone build → inline assets; demo now-playing honestly framed; `localStorage` for last-station/route/tweaks.

## 11. Scope & non-goals
IN: `#/home` structure (carousel, player upgrade, feed, search). OUT: all other routes, the sidebar/tab IA and its labels (home tab stays «Волна» unless owner renames — optional micro-decision), real backend ML/ICY/social (wired when available), the cont-17 chat-layer (independent). Repo shared with Twinr → stay on `feat/gorod-home-rmg-storefront`, keep isolated.

## 12. Deviations from research (documented)
- **Feed = music-discovery витрина, NOT a radio-schedule feed** (owner clarification 2026-07-01): friends' recommendations + categories/genres + collections + personal picks lead; wave-2's radio-first "time-state" shelves (schedule strip, catch-up, «Сейчас в эфире») are demoted to one minor «Программы и ведущие» accent. Radio/эфир is the carousel above; the feed is «витрина всего что есть по музыке».
- **РМГ siblings in the carousel** (owner D2) overrides wave-1's "de-emphasize siblings" recommendation. Consequence: dropped the generic "station directory" shelf (the carousel already is the directory).
- **Now-playing merged into the carousel center** (owner model) — no separate now-playing block.
- Themed streams (POP GOLD / K-POP / CHILL / ДИСКАЧ 90-Х) are NOT the carousel; they live in the feed («Коллекции» / genre) if used.

## 13. Assets & open dependencies (owner/client)
1. **Real logos** for the 6 stations (have Monte Carlo; need Русское Радио / ХИТ FM / DFM / MAXIMUM — brand books B018; Город ФМ mark exists).
2. **Город ФМ frequency** (if it has one) — else name-only card.
3. **Live stream URLs + ICY metadata** availability — else now-playing is representative/honestly-labeled in the prototype.
4. Confirm whether social/friends and real personalization are in-scope for the prototype (default: honest empty/representative until backend exists).

## 14. Acceptance criteria (falsifiable)
- [ ] Carousel: 6 stations, center focused, neighbors scaled+faded, **zero rotation**; snap-to-center; keyboard + touch + click-to-center; no autoplay; reduced-motion safe; works in Firefox (fallback).
- [ ] Center card = playing station; Город ФМ shows AI wave + steer, siblings show live now-playing; switching cross-fades and updates the player (one active).
- [ ] Player: LIVE badge, no scrubber on live, MediaSession play/pause only, survives route changes.
- [ ] Search: persistent, `/`/Ctrl-K, typeahead + scopes, mono-accent browse grid (no rainbow), never stops playback.
- [ ] Feed: the §8.1 shelves render with provenance chips + honest "why" + a control; order adapts by time-of-day with a real timestamp; thin shelves hidden; **no fabricated counts**; «Друзья слушают», категории, подборки и рекомендации present and populated (representative in prototype; real friends need a social graph).
- [ ] Anti-slop gate (DESIGN_PROTOCOL §2/§9) passes; single accent; Onest; WCAG AA; verified via `design-implementation-reviewer`.
- [ ] `#/home` only; other routes byte-unaffected; standalone rebuilt.

## 15. Build phasing (detail → writing-plans)
P1 carousel-эфир (roster + flat no-tilt + reuse `.home-station`, refactor `#home-radio` into center state) → P2 live-aware player (`.player-mini` + MediaSession + isLive) → P3 search (persistent + overlay + mono browse grid) → P4 feed frame (shelf component + provenance/why/control + geometry) → P5 feed intelligence (signal log + client-side scorer + ε-greedy shelf order + adaptive daypart + honest states) → P6 anti-slop + reviewer pass + standalone regen. Each: `node --check`/`check_scripts.cjs` + Chrome verify + atomic commit.
