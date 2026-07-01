# RESEARCH — Город ФМ home: station carousel + discovery feed + search

> Karpathy-tier research (5 parallel best-practices agents, 2026-07-01) for the client's
> ask: home page gets (1) a cover-flow-style carousel of radio stations (Apple-like but
> WITHOUT edge-card tilt), (2) a discovery feed below carousel + player (categories,
> rubrics, collections, recommendations, "friends listening"), (3) Spotify/Yandex-grade search.
> **Scope: homepage only.** Design system unchanged: near-black `#0B0C0F`, ONE accent
> `#5168FC`, Onest, anti-slop (no gradient bg, no rotated text, no emoji, no fabricated stats).
>
> Reference the client linked (Figma `l38kZVrZXzdNlBIIOLFX4g` node `3404-1971`) is actually a
> **Monte Carlo** desktop mock — we take its *carousel style* (focused center card, edge cards
> receding), NOT its warm skin. The older Город ФМ home Figma (`2384-6054`) shows a blue-gradient
> filmstrip of themed cards (POP GOLD / K-POP / CHILL / ДИСКАЧ 90-Х / Z.CITY SHOW / VADIM ADAMOV /
> DJ PITKIN / DFM CHILL) + genre chips + bottom player. Current *built* home = the AI-radio "Волна"
> single-stream focus (`#home-radio`), NOT a browse surface.

---

## §1 — Hero station carousel (flat, NO edge tilt)

**Why the client is right:** Apple *retired* 3D Cover Flow (iTunes 11 / iOS 7, the skeuomorphism flattening). Reasons were substantive: perspective rotation turns non-center covers into unreadable trapezoids (you effectively see one item); heavy translate+rotate motion triggers vestibular discomfort; near-impossible to make keyboard/SR accessible. Modern Apple Music / Apple TV / Podcasts all use **flat, upright, centered-snap** hero cards with scale/opacity emphasis and **zero tilt** — exactly the ask. Do NOT build 3D cover-flow.

**Technique (recommended: CSS-first hybrid).** CSS `scroll-snap` owns layout + snapping + the scale/fade via **scroll-driven animations** (`animation-timeline: view(inline)`); a thin JS layer owns interaction (click-to-center, arrow keys, active index) and is also the fallback. Scroll-driven animation runs on the compositor → tracks the finger 1:1, no jank; a scroll-listener JS approach can't match without rAF throttling + `getBoundingClientRect` layout thrash.

Each card gets a `view(inline)` timeline: 0%→100% as it crosses the scrollport, so **50% = centered**. Keyframe opaque/full-scale at 50%, shrunk/faded at 0/100%.

```css
.rail{ display:flex; gap:20px; overflow-x:auto; overscroll-behavior-x:contain;
  scroll-snap-type:x mandatory; scroll-behavior:smooth;
  padding-inline:calc(50% - var(--card,320px)/2);   /* first/last can reach center */
  scrollbar-width:none; }
.rail::-webkit-scrollbar{display:none}
.card{ flex:0 0 var(--card,320px); scroll-snap-align:center; }
@keyframes focus{ 0%,100%{opacity:.45;transform:scale(.82)} 50%{opacity:1;transform:scale(1)} }
@supports (animation-timeline: view()){
  .card{ animation:focus linear both; animation-timeline:view(inline); will-change:transform,opacity; } }
```
Only `transform`+`opacity` animate (GPU, no rotation, no layout). Optional small `translateX` pulls neighbors toward center.

**Support (2025/26):** Chrome/Edge 115+, Safari 26 full; **Firefox stable = NO** (flag only) → Firefox is the fallback trigger. Fallback: `@supports` guard; where absent, an IntersectionObserver callback (which we need anyway for the active index) toggles `.is-centered` to paint scale/opacity. Cards stay upright + snapping works regardless — graceful, never broken.

**Card content model** (accent reserved for the ACTIVE card only): square station art/logo; name + freq (`105.7 FM` muted; no fake FM for online-only); one-line tagline; **live now-playing** `Artist — Track` prefixed by a small `В ЭФИРЕ` label or a 3-bar CSS equalizer (freeze under reduced-motion; no emoji); the centered card *is* the play control (native `<button>`/`<a>`). No fake listener counts.

**Interaction:** click side card → `scrollIntoView({inline:'center',behavior:'smooth'})`; Enter/Space plays. Keyboard: roving tabindex, ←/→ move active ±1, Home/End to ends. Touch/drag native. **NO autoplay/auto-advance** (discovery picker, not slideshow; also WCAG 2.2.2). Move focus only on explicit key/click, never on passive scroll.

**A11y/perf:** container `role="group" aria-roledescription="карусель" aria-label="Радиостанции"`; cards in `<ul role="list">`, each a native button; centered card `aria-current="true"`. Exactly one card `tabindex=0`. `prefers-reduced-motion`: kill animation + `scroll-behavior:auto` (instant centering) + freeze equalizer. Animate transform/opacity only; `content-visibility:auto` + `contain:layout paint` off-screen; no rAF `getBoundingClientRect`.

**DON'T:** 3D perspective/rotateY tilt; autoplay timers; animate width/left/margin; scroll-jack the page; emoji "LIVE"; invented counts; scroll-driven w/o Firefox fallback; focus on passive scroll; gradient card bg; a 2nd accent.

---

## §2 — Search (Spotify/Yandex-grade)

**Entry point = persistent, always-visible field** (NOT an icon-that-expands — the brief is a discoverability request; a collapsed icon fails it).
- **Desktop:** input in the sticky top bar, centered ~440px, h48, radius 12, surface `#15161A` on `#0B0C0F`, glyph left, placeholder "Поиск станций, шоу, треков…" at 60% white. On focus expands downward into a full-width search panel overlaying the hero.
- **Mobile:** full-width search **pill** pinned above the hero carousel; tap → full-screen overlay, autofocus. Focus ring 1px `#5168FC`; clear "×".

**Panel states.** *Empty (on focus):* `Недавние запросы` (last ~8, each ×-removable + "Очистить историю") then `Часто ищут` (6–8 trending chips). *Typing (debounce ~160ms):* a **Лучший результат** card (96px art, name, type badge Станция/Шоу/Жанр, inline Play) then grouped sections capped 3–4 with "Показать все →": **Станции · Шоу и DJ · Жанры · Подборки · Треки и артисты**. Live stations get an accent dot + "В эфире". Group order fixed + radio-biased.

**"Browse all" grid** (search-landing) — keep it, but REJECT Spotify's rainbow tiles (brand-forbidden slop). Mono-accent alternative: every tile is a uniform dark card on `#0B0C0F`; richness from **real imagery** (station logos, show art, editorial photo) + a bottom-up `#0B0C0F` 0→90% scrim + Onest label (16/600, lower-left). Genres without art → mono-accent tile (`#15161A`, 1px `#5168FC`@12% border, oversized ghosted Onest letterform + tiny equalizer glyph). Accent `#5168FC` spent ONLY on meaning (hover/active border, live dot, selected scope) — never as tile fill. Grid: desktop 4–5 col, mobile 2 col, 1:1 or 4:3, 12 gap, 12 radius.

**Scopes** (sticky chips once results show): `Всё · Станции · Треки · Артисты · Подборки · Подкасты`. "Всё" default; radio-first → floats Станции/live above tracks. **Keyboard:** `/` or `Ctrl/Cmd+K` focus from anywhere; ↑/↓ traverse flat list incl. top-result; Enter opens/plays; Esc clears then closes. **No-results:** "Ничего не нашлось по «…»" + spelling suggestion + 4–6 fallback popular stations + "Открыть все категории". Never a dead end. **Mobile:** overlay sits ABOVE the docked mini-player (padding-bottom = player h + safe-area); opening search does NOT stop playback (core radio behavior).

---

## §3 — Discovery feed IA

**Majors converge:** personalization owns the fold → made-for-you → because-you-listened → new releases → editorial rubrics → charts → long tail. Yandex "Главная" is the most radio-like: **Моя волна** hero (with mood/activity/decade/tempo chips) → smart-playlist row (Плейлист дня, Дежавю, Премьера, Тайник) → Собрано для вас → Чарт → Новинки → Настроения и жанры → В стиле [артист].

**Ideal ordered shelf stack for our radio-first catalog** (below hero carousel + player):
1. **«Продолжить слушать»** — resume: recent stations/shows/tracks.
2. **«Ваша волна»** — the flagship AI stream(s) + mood/genre chip row to retune. Big cards. *(the product wedge stays first-class)*
3. **«Радиостанции»** — full station directory, circle logos, live "в эфире" dot. The storefront spine (`Все ›`).
4. **«Настроение и жанр»** — flat mono tiles (энергия, фокус, вечер, ретро).
5. **«Передачи и шоу»** — DJ programs, 16:9 landscape cards. *(shows live here, NOT in the carousel)*
6. **«Потому что вы слушали …»** — because-you-listened, honest subtitle naming the seed.
7. **«Новые выпуски»** — fresh episodes/releases from follows.
8. **«Выбор редакции»** — editorial подборки, larger hero cards.
9. **«Популярное сейчас»** — charts/trending — real counts only, or no numbers.
10. **«Коллекции»** — deep rubrics (по десятилетиям, по языку, по городу).
11. **«Друзья слушают»** — social shelf (see §4).

**Above the fold:** hero + player + shelves 1–2 (personalized) → first screen feels "made for me," not billboard.

**Density:** horizontal shelves default; vertical grids only for `Все ›` landings. 10–20 items/shelf; **peeking half-card** (mobile ≈2.2, desktop ≈5–6). **Vary card geometry per shelf** to break the identical-wall: stations=circle, moods=square tiles, shows=16:9, collections/playlists=1:1, tracks=thumb+text rows; alternate rhythm + an occasional full-bleed spotlight single-card shelf.

**Header:** Title (Onest ~18–20 semibold) + optional muted "why" subtitle (~13) + optional right-aligned `Все ›`. Separate shelves with whitespace + a consistent left gutter — **never divider lines, boxed cards, or colored section backgrounds** (slop). Accent used sparingly (live dot, `Все ›` hover, one spotlight).

**Honesty:** every personalized shelf explainable in its subtitle («Потому что вы слушали Radio Jazz», «На основе вашей истории»). No invented figures. Cold-start / thin signal → degrade to editorial and RELABEL «Выбор редакции» — never dress editorial as personal. Drive from real signals only (recent plays, follows, likes, dwell).

---

## §4 — "Друзья слушают" (social)

**Surface = a horizontal shelf on home** (title «Друзья слушают», ≤8 cards), NOT a Spotify always-on rail (heavier, more surveillance-flavored, off-brief). Item (~180–220px): 36px avatar (initials fallback on `#5168FC`@12%), display name (Onest Medium 14), object (station OR `Track — Artist` OR collection, 1 line), verb/state (*live*: "в эфире" + pulsing `#5168FC` dot; *past*: "слушал(а)"), relative timestamp («сейчас»/«5 мин»/«2 ч»), whole card taps to **"Слушать то же"** (the load-bearing element — turns voyeur feed into a discovery action). "в эфире" only while presence heartbeat ≤60s fresh; else degrade — never stale-live.

**Privacy (CRITICAL, RU 152-ФЗ):** adopt Apple-strict, NOT Spotify default-on. (1) **Default OFF**, explicit opt-in consent sheet. (2) Approve-a-follower / mutual graph. (3) Private Session one-tap. (4) Single master visibility flag gating every surface + per-friend block. (5) No contact-scraping default. (6) Coarsen — "слушает [станцию]", no exact scrubbing/location.

**Discovery-useful, not vanity:** rank by novelty-to-viewer (prefer things they haven't played); aggregate social proof ("5 друзей слушают [станцию]" = one strong card); optional taste-match weighting; one-tap join (live radio's superpower — friends are on the same stream NOW).

**HARD honesty constraint (no social graph yet):** do NOT render fake avatars/names as real. Default = **onboarding empty state** (heading + "Подключите друзей, чтобы видеть, что они слушают вживую" + CTA "Найти друзей"/"Пригласить"). If a pitch demo is needed → clearly-labeled ("Пример"/"Демо" chip, ghost styling, obviously-placeholder names). **Real impl requires:** accounts+auth, social graph, presence service (heartbeat+TTL), privacy/consent layer (152-ФЗ record). Gate the shelf behind all four; until then ship only the honest empty state.

---

## §5 — Station model + carousel↔player

**Governing rule:** a "station" = something continuously **playable right now**. That test sorts the taxonomy:

| Option | Playable now? | Verdict |
|---|---|---|
| Sibling РМГ stations (Русское Радио, DFM, Хит FM, Monte Carlo) | yes, but off-brand | **De-emphasize** — at most a small "Сеть РМГ" shelf far below; never hero. |
| Themed 24/7 streams (POP GOLD, K-POP, CHILL, ДИСКАЧ 90-Х) | yes | **PRIMARY** — carousel backbone (Record/DI.FM/iHeart artist-radio model). |
| Shows / DJ programs (Z.CITY SHOW, VADIM ADAMOV, DJ PITKIN) | no — time-bound | **Segment out** → "Передачи и ведущие" rail w/ schedule + replay; surface as a badge on the flagship card only when live now. |
| AI mood "stations" (Yandex Моя волна) | yes | **Feature type** — one/few tunable personal streams; the discovery hook. |

**Carousel = ONE hero, THREE card types** sharing identical tuning behavior: ① flagship LIVE FM (105.x, hosted), ② themed 24/7 streams, ③ AI "Ваша волна"/mood. A tiny type pill disambiguates `В ЭФИРЕ` / `24/7` / `AI`. Do NOT mix shows/DJs into it (different interaction). Sibling stations omitted/buried.

**Card content:** consistent frame + distinct art; flagship = big `105.7 FM` + tagline; themed = bold typographic genre art (no stock gradients). Live now-playing from real ICY/Icecast `StreamTitle` polled ~10s, fallback to station name (never invent). Listeners only if real (Icecast exposes true counts) else omit → LIVE dot is the honest substitute. Precise state labels (`В ЭФИРЕ` hosted-live only / `24/7` continuous / `AI`) prevent the "everything says LIVE" lie. Flagship only: `Далее: Z.CITY SHOW · 20:00`.

**Carousel ↔ player:** centering ≠ tuning (never autoplay on scroll; browsers block it + it's hostile). Tap = tune + play (TuneIn/iHeart); the player bar is the single source of truth, matching card shows playing-state (accent border + equalizer). No hover audio preview. Switch = cross-fade ~300–500ms between two `<audio>`/gain nodes + brief `Подключение…`; never hard-cut.

**Persistent player, LIVE specifics:** NO scrubber/seek on live → `LIVE` badge (+ optional non-timeline equalizer). MediaSession: register only play/pause, NOT seek. Pause→resume rejoins live edge (offer `Вернуться в эфир`; consider Stop-square not Pause). Controls: Play/Stop · Volume · **Like ❤ (feeds the AI engine — discovery payoff)** · Share (track or station) · Recently-played · Favorite station. On-demand mode-switch (show replay/podcast): same component swaps to scrubber + 15/30s skip + resume-position + speed, keyed off an `isLive` flag. SPA: keep the `<audio>` element mounted across route changes so playback never drops. LIVE dot + accent badge must pass WCAG AA on `#0B0C0F`.

---

## §6 — Proposed home anatomy (synthesis) + open decisions

**Top → bottom:**
1. Sticky top bar: ГОРОД.FM wordmark · **persistent search field** · Личный кабинет.
2. **Hero: flat centered-snap station carousel** (no tilt) — ① flagship live + ② themed streams + ③ Ваша волна card.
3. Persistent **now-playing player** (live-aware) — reflects the tuned station.
4. **Discovery feed** — shelves §3 (1–11), varying card geometry, honest labels.
5. (Search overlay + browse grid §2 layered above.)

**Reconciliation (product wedge):** the AI "Волна" is NOT dropped — it becomes the flagship AI card in the carousel AND shelf #2 «Ваша волна» with mood chips (Yandex model). Home shifts lean-back→lean-forward but keeps explainable-AI-radio first-class.

**Decisions for the owner (can't derive):**
- **D1 Visual direction:** keep shipped dark `#0B0C0F`/`#5168FC`/Onest and evolve home *structure* (recommended — "only the home changes" = structure not skin; honors anti-slop) vs re-skin toward blue Figma `2384-6054` vs warm Monte-Carlo.
- **D2 Carousel content:** themed 24/7 streams + flagship live + AI Волна, shows in a separate rail (recommended) vs РМГ siblings vs mostly-AI vs everything-mixed.
- **D3 Deliverable path:** design spec → plan → build in `gorod-fm.html` on an isolated branch (repo shared w/ Twinr).

**Sources:** per-agent citations retained in task transcripts (MDN scroll-driven animations, caniuse, W3C APG carousel/roving-tabindex, Spotify/Apple/Yandex/YouTube Music docs, TuneIn/iHeart/SiriusXM/Apple Music Radio, MDN MediaSession).
