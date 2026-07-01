# HANDOFF — Город ФМ home: РМГ carousel + music витрина + search (storefront redesign)

**Session:** 2026-07-01 · **Branch:** `feat/gorod-home-rmg-storefront` (rebased onto `master` 1eab466 — clean base, NO chat-layer) · **Server:** `cd designs && python -m http.server 8791` → `http://127.0.0.1:8791/gorod-fm.html#/home` · **Visual verify:** chrome-devtools MCP works (claude-in-chrome extension was NOT connected).

**Spec:** `docs/superpowers/specs/2026-07-01-gorod-fm-home-station-carousel-feed-search-design.md`
**Research:** `RESEARCH-gorod-fm-home-carousel-feed-search.md` (wave-1) + `RESEARCH-gorod-fm-home-feed-frontier-wave2.md` (wave-2 — the frontier recsys/personalization findings are for the future «Моя волна» AI tab, NOT this non-AI home).
**Plan:** `docs/superpowers/plans/2026-07-01-gorod-fm-home-carousel-vitrina-search.md`
**Ledger:** `.superpowers/sdd/progress.md`

---

## ✅ SESSION 2 (cont, 2026-07-01) — ALL 10 owner-feedback + deferred items DONE + adversarial review + standalone

**HEAD = `8da6443`** on `feat/gorod-home-rmg-storefront` (5 commits, **NOT pushed** — push at `sync`). `check_scripts.cjs` 31/0; **0 console errors on every route**. Verified via chrome-devtools MCP at desktop 1440 + mobile 390. Server now `python -m http.server 8791`.

**Done (maps to the 🔴 REMAINING list further below):**
1. ✅ **Carousel center-card transport** — ♥/⏸/⏭ on the aria-current card, wired to `TwinrTransition`; play glyph stays synced with the mini-player via a MutationObserver on `#btn-play`.
2. ✅ **Carousel spacing/centering/focus** — `.rmg-rail` clears the topbar (`padding-top: topbar-h+32`); `center()` uses transform-immune `offsetLeft`; sharper `view()` focus (neighbours .72/.34). Re-centers on the ACTIVE station when #/home becomes visible (review M4).
3. ✅ **Друзья слушают → ▶/＋ icons** — `buildFriendRow` (avatar + «слушает X» + two 44px icon buttons). ⚠️ icons are demo **hooks** (`data-friend-action`) — **not yet wired to playback** (review L7).
4. ✅ **FULL витрина content** — 122-item RU-music dataset (`window.GOROD_VITRINA_CONTENT`, 9 shelves × 10–20), **eager render** (skeleton-until-scroll removed); honest «· демо» suffix on claim-shelves; monogram art (no fabricated imagery/hard stats).
5. ✅ **Retire AI chrome on #/home** — scoped via `html[data-active-route="#/home"]` (these render OUTSIDE `[data-page=home]`, after `</main>`): Twinr AI launcher, up-chevron FAB, «почему?» ribbon, «Ты дослушал» line, legacy Believer sheet + `.player-full`; mini-player click guarded on home.
6. ✅ **Search** — fixed the overlay rendering **0-height** (it was a child of `.topbar`, whose `backdrop-filter` made it the fixed containing block → moved to `<body>`). Mobile: search **pill** above the carousel + an **in-overlay input** (topbar field is hidden on mobile) driving the same typeahead (review H1). Verified «dfm» → DFM.
7. ✅ **Mobile** — narrow (`≤768px`) adopts the app's `data-surface="mobile"` shell via a `matchMedia` flip (sidebar→bottom tabbar; guarded for tv/carplay, review M2); home full-bleed margins neutralized; `--rmg-card:76vw`.
8. ✅ **Chat rail «Общий эфир» restored** (owner-flagged «чат справа пропал») — ported from `feat/gorod-chat-layer` (Option A: `.app-shell` → `sidebar | main | 360px rail`; main + витрина reflow beside it; mini-player full-width below, z below rail). Mobile: rail hidden + FAB opens it as a dialog (FAB hides when open). **Home leads with the «Всем · Общий эфир» community lane, NOT the Twinr AI composer/greeting** (review M3 — aligns with the non-AI home; Twinr is one tap away via the mode toggle). 🟡 **OWNER-CONFIRM this default.** Rail is **global** on all content routes (as on chat-layer) — if home-only wanted, gate `grid-column:3`/`.chat-rail` by route.
9. ✅ **Honest mini-cover** — `GorodPlayer.stationArt()` per-station SVG-monogram data-URI (was a stale «Слеза»/Егор-Крид PNG); static markup is a neutral «Г» monogram too (no first-paint flash).
10. ✅ **Review + standalone** — adversarial code/anti-slop/a11y review → 6 fixes (H1/M2/M3/M4/M5/L9). Standalone regenerated fresh from dev (`.scratch/gorod2/regen_standalone.py`, Pillow webp-inline: 30 assets 39.8 MB→2.8 MB, **5.18 MB**); renders identically.

**Still GATED / follow-up (NOT blockers):**
- **Owner real assets** — 6 РМГ station **logos** (have Monte Carlo only), Город ФМ **frequency**, live **stream URLs + ICY**, real catalog. Until then carousel/mini-cover use honest monograms.
- **L7** — wire friend ▶/＋ (and vitrina cards, search `selectItem`) to real playback/nav (currently `console.log`/hooks; was inert pre-session too).
- **«Моя волна» AI tab** — relocate the commented-out `#home-radio` wave/steer there + wave-2 recsys.
- **M6** (perf) — eager render builds 122 cards on load; fine for demo, revisit if low-end jank.
- **Standalone regen tool** = `.scratch/gorod2/regen_standalone.py` (run via `C:\Users\elbics\scoop\shims\python3.exe`). Splice scripts: `.scratch/gorod2/{integrate_vitrina2,splice}.cjs`; agent artifacts in `.scratch/gorod2/`.
- **Push** held until `sync`.

**START next session: this block.** Session-1 handoff + the 12-item remaining list preserved below for reference.

---

## Owner-locked model (do not re-litigate)
Home = non-AI **radio storefront**: (1) hero **carousel = the эфир** — 6 РМГ stations, flat NO tilt, center card = station playing now, sides switch by scroll/click; (2) persistent **live-aware player** (bottom); (3) **music витрина** below (browse/editorial/social shelves — friends, categories, collections, editorial, charts, artists, programs). Dark skin kept, `#/home` only. **ALL AI/personalization** (wave, steer, «для вас») → a separate **«Моя волна» AI tab** (the current `#/home` «Волна» experience, preserved commented-out as `#home-radio`).

## ✅ DONE this session (all committed on the branch, 0 console errors, `node .scratch/check_scripts.cjs` green = 29 blocks)
- **Research (9 Karpathy briefs, 2 waves) + spec + plan** — committed.
- **Base rebased to clean master** (chat-layer dropped from home base; it stays on `feat/gorod-chat-layer`).
- **T1 station data** (`window.GorodStations`, 6 real РМГ stations + demo now-playing) — commit `92c80d3`. Reviewed ✅.
- **T2 carousel markup + flat no-tilt CSS** (`.rmg-rail/.rmg-track/.rmg-card`, scroll-snap + `animation-timeline:view()`, IO fallback, reduced-motion) — `7ac08cc`. Reviewed ✅ (2 fixes applied: `--rmg-card` declared, reduced-motion pulse). `#home-radio` AI hero commented out (preserved for «Моя волна»).
- **T3 carousel render/interaction** (`window.GorodRail`, injects 6 cards, click-to-center, roving-tabindex, `gorod:tune`/`gorod:activecard` events) — `95e1bd3` + centering-race fix `09b3949`. Город ФМ centers + active («● В ЭФИРЕ»).
- **T4 live-aware player** (`window.GorodPlayer`) — `cfc6e3f`. Mini-player is station-aware («Любимка / Город ФМ · Niletto / ● LIVE»), MediaSession play/pause bridged to existing `TwinrTransition.setPlaying`, no scrubber on live. Real selectors (`#player-track-title/-artist`, `#mini-art-img`).
- **T7+8 non-AI витрина** (`window.GorodVitrina`) — `abe5f76`. 9 shelves render: Друзья слушают · Категории и жанры · Подборки · Выбор редакции ГОРОДА · Новинки · Популярное·Чарты · Коллекции · Исполнители · Программы и ведущие. CSS scoped under `.vitrina` (avoids collision with existing `.shelf-*`). Demo content, generic labels, no fabricated counts. Lazy-render via IntersectionObserver.
- **T5+6 search** (`window.GorodSearch`) — `2aceb42`. Persistent field replaced the inert `.topbar-search` placeholder; overlay + typeahead + scope chips + mono-accent browse grid + recent searches. `/` and `Ctrl/Cmd+K` open; doesn't stop playback.

**HEAD = `2aceb42`.** Reviews: T1, T2 reviewed clean. **T3–T8 were NOT individually reviewed** (parallel-authored per owner "many waves" request) → do a **holistic review** (see remaining).

## 🔴 REMAINING (next session) — owner feedback + deferred tasks, in priority order
1. **Carousel center card = play controls on the PLAYING station** (owner: «как раньше чтоб были кнопки плей … в центральной станции которая сейчас проигрывается»). The center (active) `.rmg-card` should show transport on the card itself — at minimum ▶/⏸ play-pause, plus like/skip — like the old AI hero had. Wire to `TwinrTransition.setPlaying` + `GorodPlayer`. Only the centered/`aria-current` card shows them.
2. **Carousel top spacing + initial centering** (owner: «отступы сверху и скролл чтоб изначально центру был надо поправить»). There's odd top gap and the initial scroll isn't cleanly centered on Город ФМ. Also the scale/opacity **focus effect is too subtle** — make the center card visibly dominant, neighbors clearly smaller/faded. Check `padding-inline` math + the `animation-timeline:view()` range; consider an explicit `scrollLeft` set on init instead of `scrollIntoView`.
3. **Друзья слушают cards: replace «Слушать то же» text → icon buttons on the right** (owner: «может лучше плей и кнопку добавить себе типа плюса … иконками справа»). Each friend row: avatar + name + «слушает X» (left), then **▶ play + ＋ add** icon buttons (right, ~44px hit). Edit the friend-card renderer inside the integrated `GorodVitrina` (grep `Слушать то же`).
4. **FULL content-fill of all витрina shelves** (owner: «фулл все контентом заполнить как мы делали для онбординга»). Currently lazy-render + thin demo; make every shelf richly populated (10–20 items), eager-render or fix IO so shelves don't sit as skeletons, real-ish Russian-music content. Model the thoroughness on how onboarding was built out.
5. **Retire residual AI/legacy chrome on `#/home`** (scope to `[data-page="home"]` — these are global, don't break other routes):
   - The **legacy full-player panel** showing «Believer / Imagine Dragons / СЛЕДУЮЩИЕ В ЭФИРЕ (Thunder/Enemy/Radioactive/Demons)» — a `home-bottom-sheet`/`.player-full` expanded view rendering on the home. Hide it on `#/home`.
   - The top **«почему?» between-track banner** (AI ribbon).
   - The **«Twinr AI» floating launcher** + up-chevron (bottom-right).
   - The mini-player **«Ты дослушал … 3 раза»** AI reason line (`.player-mini-reason`).
   - Mini-player **cover is stale** (shows Слеза) — needs per-station art (see assets).
6. **Search: verify overlay live** (typeahead/scopes/browse grid — only syntax-verified, not visually) + **add a mobile entry point** (topbar is `display:none` on mobile, so no search affordance there; add to `.mobile-tabbar` or a header).
7. **Mobile responsive pass (Task 9):** `--rmg-card`→~78vw peeking, search pill above hero, single-col shelves, feed `padding-bottom:var(--player-mini-h)`.
8. **Holistic anti-slop + a11y review (Task 10):** dispatch `compound-engineering:design:design-implementation-reviewer` on `#/home` (desktop 1440 + mobile 390); covers T3–T8 which skipped per-task review. Minor known nits: search active-chip white-on-`#5168FC` ~4.4:1 (matches precedent); font-shorthand style in some new CSS.
9. **Standalone regen (Task 11):** rebuild `designs/gorod-fm-standalone.html` (re-grep `rebuild_standalone_full.py`).
10. **Real assets (owner-supplied):** 6 station **logos** (have Monte Carlo; need Русское Радио/ХИТ FM/DFM/MAXIMUM from brand books B018), Город ФМ **frequency**, live **stream URLs + ICY metadata**, real catalog for the витрина.
11. **Separate follow-up (out of this scope):** the **«Моя волна» AI tab** — relocate the commented-out `#home-radio` wave/steer there + wire the wave-2 frontier recsys research.
12. **Chat rail «Общий эфир» — OWNER DECISION** (owner flagged its absence 2026-07-01). It was DROPPED when this branch rebased onto clean `master` (option A); the full chat-layer is intact on `feat/gorod-chat-layer`. Decide: **(a) restore it on the new home** — needs layout reconciliation (the витрина is currently full-width; either narrow the витрина to leave a right rail, or make the rail a toggle/overlay) — cherry-pick the chat-rail feature from `feat/gorod-chat-layer` into this branch; **(b) keep it parked** (separate experiment). Owner leans toward wanting it back — confirm layout approach first.

## Key anchors (RE-GREP — they drift)
- Carousel: CSS `.rmg-rail` (~L2220), markup `id="rmg-rail"` (in `data-page="home"`), JS `window.GorodRail` (trailing script). `#home-radio` = commented-out AI hero.
- Player: `window.GorodPlayer` (trailing script), badge `.player-live-badge`, mini-player `#player-mini`/`#player-track-title`.
- Витрина: `window.GorodVitrina`, `<section id="vitrina">` after `#rmg-rail`, CSS scoped `.vitrina …`.
- Search: `window.GorodSearch`, `#gorod-search-field` (topbar), `#gorod-search-overlay`.
- Contracts: events `gorod:tune`/`gorod:activecard` `{detail:{id}}`; `GorodStations.{list,get,nowPlaying,setActive}`.

## Discipline
Repo shared with Twinr (`master`=Twinr). Stay on `feat/gorod-home-rmg-storefront`, don't touch Twinr files. Re-grep anchors before every edit. Verify each change: `node .scratch/check_scripts.cjs` + chrome-devtools screenshot (desktop+mobile) + console. Anti-slop gate (DESIGN_PROTOCOL §2/§9) before "done". No fabricated stats/counts.
