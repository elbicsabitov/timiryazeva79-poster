# HANDOFF — Город ФМ · cont-17 (built 2026-06-17, closed-out + verified 2026-06-24)

> **STATUS: chat-layer track BUILT + VERIFIED + 2 bug-fixes applied. Working tree clean. PUSH of this session's commits HELD until explicit `sync`.**
>
> Branch: **`feat/gorod-chat-layer`** — the branch **IS on origin** (the 2026-06-17 session pushed it; `origin/feat/gorod-chat-layer` tip = `755ab63`), but it is **UNMERGED to master** (14 commits ahead of `origin/master`). **This session's 2 commits — `18d375d` (fix) + the docs commit — are LOCAL-ONLY (2 ahead of `origin/feat/gorod-chat-layer`), not yet pushed.** Local HEAD on `feat/gorod-chat-layer`.
> File: `designs/gorod-fm.html` (~1.01 MB single-file SPA). Mirror: `designs/gorod-fm-standalone.html` (3.86 MB, regenerated). Server `:8770` serves `designs/`.
> Disc: dev features need `?dev=1`; `?v=N` cache-bust; the screenshot capture downscales the full viewport to 1568px-wide (the rail is NOT clipped — verified `horizOverflow=0`); clean `gorodfm_*`/`gorod-fm.*` LS after probe.

## Why this handoff exists
The **2026-06-17 session built a whole new track (chat-layer + glass skin + shared radio) in 12 commits but never wrote a handoff and never updated DEBT.md / RESUME_PROMPT.md** (both stopped at cont-16, 2026-06-03). The 2026-06-24 `resume gorod fm` session reconstructed the state from git + the 4 research docs + the `gorod-cont17-*` screenshots, verified the build live in Chrome, fixed 2 real bugs the prior session left behind, and wrote this. Everything is still **dark / unpushed** — nothing reached production.

---

## What the cont-17 track is — "Город ФМ как живой эфир"
A ubiquitous-chat + collaborative-listening layer over the AI-radio. The radio becomes a **shared room**: a persistent Twitch-style "Общий эфир" chat rail where listeners talk, Twinr hosts the wave, and friends can listen together in sync.

Research backing (all `docs/superpowers/`, 2026-06-17):
- `RESEARCH-gorod-fm-ubiquitous-chat.md` — chat as the primary surface (not a corner widget)
- `RESEARCH-gorod-fm-chat-rail.md` + `RESEARCH-gorod-fm-chat-rail-uiux.md` — the docked rail UX
- `RESEARCH-gorod-fm-shared-radio.md` — group-listen / suggest / accept / listen-together spec

## What's built (13 commits, `f1a5663` → `18d375d`)
1. **Ubiquitous «Чат»** `f1a5663` — composer toggle **ЛЮДЯМ ↔ Twinr** unifies people-chat + the old corner Twinr AI into one surface.
2. **Glass skin «Стекло»** `992a9b1` + merge `f0a2d95` — additive `html[data-skin="glass"]` layer + topbar **Обычный ↔ Стекло** switcher. **Verified: switcher flips `data-skin`, dusk-lake ambient background renders, 5 glass surfaces.**
3. **Persistent docked chat rail «Общий эфир»** `a80d405` — Twitch-style, replaces the floating dock. Holds: live guest chat, Twinr AI host messages + a now-playing track card (Любимка/Niletto), live **TWINR-профиль · живой** strip (1 240 слушают · 18 пишут · Медленный режим), and the composer.
4. **Glass ambient background** `2800253` (glass-only) + removed the old Tweaks settings shutter.
5. **Chat-rail UI/UX refactor** `d9b37bf` — 1-row chips + ✦ menu, composer capsule + Twinr private hint, rail density, **mini-player expand**, glass cover image.
6. **Glass mode-popover legibility + overflow guard** `a6866df`.
7. **Collaborative shared radio** `c7b43d9` (+ spec `ddd4a18`) — share → session → suggest → accept → listen-together. Mini-bar gets a **«слушаем вместе · в синхроне»** sync pill (shown only in an active session). Entry points present: "◉ Слушать вместе", "Присоединиться и слушать вместе" (tg-style invite preview), "Поделиться карточкой".
8. **Session-UX** `244a92a` — chat stays dominant, icon-only send, live-chat drip.
9. **Standalone regen** `e86e0f9` + **offline images + sync-pill overflow fix** `755ab63`.

## ✅ This-session verification (2026-06-24, Chrome `:8770`, glass + normal skins)
- Switcher Обычный↔Стекло works; dusk-lake ambient renders; **0 console errors** across loads.
- Docked rail renders fully (chat, Twinr host + track card, live profile strip, composer ✦ «Только вы · Twinr» mode chip, "Спросить Twinr").
- Shared-radio affordances all present in DOM (start/join CTAs + sync pill).
- Now-playing **consistent** on primary surfaces (mini-bar / home hero / chat = Слеза / Егор Крид).
- Rail is 360px flush-right, `horizOverflow=0` (the "clipping" in screenshots = capture-width quirk, not a layout bug).

## 🐛 Bugs found + FIXED this session — commit `18d375d`
- **B1 — typo "IMAGINE DRAGON" (missing S)** in 3 spots: `#home-bs-artist`, `#home-sd-artist`, and the `rock` home-trackfile context string → all now "IMAGINE DRAGONS". Verified: 0 no-S occurrences remain in both files.
- **B2 — track-file expand sheet showed a STALE now-playing** (the mini-player chevron opens `#home-bottom-sheet` / `#home-side-drawer`, which hardcoded "Believer / Imagine Dragons" + a static all-Imagine-Dragons queue, shown while Слеза/Егор Крид was actually playing — visible in `gorod-cont17-glass-miniplayer-panel.jpeg`). Added `syncTrackFileFromNowPlaying()` called from `openHomePanel()` (mirrors the existing `syncFullPlayerFromMini()` for `#player-full`): title/artist/cover-label now sync from `#player-track-title`/`-artist` on open. **Verified live: sheet header = "Слеза / ЕГОР КРИД" after open.**
- Gate: `node .scratch/check_scripts.cjs` → 26 `<script>` blocks, 0 parse errors. Standalone regenerated (3.86 MB) + confirmed both fixes propagated.

## 🟡 Open / known items (NOT bugs to fix blindly — owner judgment)
1. **Track-file "Следующие в эфире" queue** is a labeled STATIC demo (Thunder/Enemy/Radioactive/Demons) — stays the same regardless of the playing track. Header desync (B2) is fixed; the demo queue was **intentionally left** (making it track-aware needs real per-track next-up data — won't fabricate per the project honesty-floor). Decide later: keep as demo, or wire a real taste-aware queue (Ф1+).
2. **Rail profile-tags strip (`.chat-rail .ai-profile-tags`)** is an intentional hidden-scrollbar **horizontal-scroll** strip (`flex-wrap:nowrap; overflow-x:auto; scrollbar-width:none`). At rest the last tag ("Хип-хоп 2010-х") shows partly cut — that's the normal scroll-strip rest-state, **not a clip-and-lose bug** (tags ARE reachable by swipe/scroll). ⚠️ Discoverability tradeoff on desktop (no visible scroll affordance). **This session tried wrapping → it produced an ugly 114px vertical stack → reverted.** Owner design-judgment: (a) keep hidden-scroll, (b) add a right-edge fade affordance, (c) stack the parent `.ai-profile` to a 2-line label-over-tags layout, or (d) cap to top-N + "+N".
3. Standing Эльбик-gates (unchanged): **GOROD-029** positioning · **GOROD-030** licences (the #1 bottleneck).

## ✅ Next-session START HERE
1. **Push this session's 2 commits + decide merge intent.** The branch is already on origin (`origin/feat/gorod-chat-layer` @ `755ab63`); this session's `18d375d` (fix) + docs commit are local-only and **held until Эльбик says `sync`**. The branch is **unmerged to master** — merge-to-master vs keep-as-branch is an owner call. ⚠️ This branch shares the `design-project` repo with **Twinr** (master = `1eab466` Twinr work) — keep the gorod branch isolated; do the master/twinr stash-dance if touching both.
2. Optional polish before showing: resolve the 2 owner-judgment items above (queue, profile-scroll affordance).
3. On `sync`: `git push` the 2 local commits to `origin/feat/gorod-chat-layer`, then decide merge-to-master vs keep-as-branch.

## Commit ledger (unmerged to master = dark / not in prod)
**On `origin/feat/gorod-chat-layer`** (pushed 2026-06-17): `f1a5663` `992a9b1` `f0a2d95` `a80d405` `2800253` `d9b37bf` `a6866df` `ddd4a18` `c7b43d9` `244a92a` `e86e0f9` `755ab63`.
**Local-only, NOT yet pushed (2 ahead of the origin branch):** **`18d375d`** (Jun-24 fixes) + the cont-17 docs commit.
Whole branch is 14 ahead of `origin/master` (never merged to master).

## Artefacts
- Screenshots: `designs/screenshots/gorod-cont17-{glass-home,glass-composer-popover,glass-lives,glass-miniplayer-panel,normal-home}.jpeg`.
- Builder: `tools/build_gorod_fm_standalone.py` (Pillow). Script-check: `.scratch/check_scripts.cjs`.
- Prior handoff: `docs/superpowers/HANDOFF-gorod-fm-cont-16.md` (the paused light-theme sweep — still pending, separate track on `master`).
