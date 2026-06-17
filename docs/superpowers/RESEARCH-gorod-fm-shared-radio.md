# RESEARCH — Город ФМ · Совместное радио (Collaborative Shared Radio)

> Build-ready synthesis. One spec. Grounded in `designs/gorod-fm.html` (17 354-line scripted SPA).
> **Hard constraint: everything group = SCRIPTED / SEEDED demo. No backend, no real-time sync.** Honestly marked `демо`.
> Skin: dark cinema + glass · Onest · brand `#5168FC` · text `--accent-on-dark` · a11y · the rail stays always-visible.

---

## 1. Executive summary — why shared radio *reinforces* the wedge (instead of diluting it)

Город ФМ's moat is the **explainable, editable, taste-driven station**: a living Twinr taste-cloud (`#/taste`), an adaptive personal Волна (`#/home`) you steer by voice/text ("сделай по-другому"), and a "почему этот трек" answer for everything. The owner's request — *share your radio, chat together, friends suggest via Twinr, you accept, listen together* — could be built as a Spotify-Jam clone (a democratic free-for-all queue). **That would be a strictly worse Spotify.** Spotify Jam already has the shared room; Spotify Blend already has AI taste-blend + a compatibility score. We cannot out-breadth them.

What no competitor ships is the **one mechanic that turns a social feature into a taste-building, retention loop**: a friend doesn't drop a track into a queue — they **ask Twinr**, Twinr proposes a track **with a "почему" tied to the owner's taste-cloud**, and the **owner accepts or rejects** it into their station. Accepting can **visibly grow the editable taste-cloud** (a new, attributed, removable bubble: "+ darkwave — от Ани"). So the social act *compounds* the wedge: every accepted suggestion is an explained, owner-curated, reversible edit to a coherent station — not noise in a queue.

Design stance (load-bearing, do not cut):
- **Suggest, don't control.** Guests suggest + react; only the owner curates the live Волна. This is *our* design stance — **not** "Spotify Jam's host toggle" (Jam actually defaults to collaborative queue-editing by everyone; host-only is opt-in). [`must_fix` Rec3 across dossiers]
- **Every suggestion is AI-mediated + explained + owner-gated.** That trio (explain + accept-gate) is the differentiator — **not** attribution alone (Jam *does* attribute who added each track). [`must_fix`]
- **Accept can teach the profile, never silently.** Taste mutation is an explicit *secondary* action, previewed before confirm, attributed, and removable.
- **Sell sync, don't fake sync.** Reuse the single `isPlaying`/now-playing transport as the room's "shared" transport; add a "в синхроне" pill; mark `демо`. No real cross-device sync exists or is promised.
- **The rail is the home, not a new surface.** The shared session is a *special rail room*; suggestions are a *new message type* in the existing AI lane. Zero new full-screen surfaces; the rail stays always-visible.

---

## 2. Distilled synthesis of the 4 dimensions (steal / avoid + sources)

### D1 — Group / social listening (listen together)
**Steal:** host owns the session; low-friction join (link + QR/code + seeded "invite friends"); a **graduated control model** defaulted to *only-suggest*; visible intimate presence ("4 слушают · в синхроне") with avatar pulse on reaction; sell the *feeling* of sync via a single shared transport + a "в синхроне" pill.
**Avoid:** SharePlay-style "everyone needs a paid sub / it's a call"; a democratic free-for-all queue; faked backend-scale numbers *in the private room* (big seeded counts stay fine in public station rooms — they already exist in the proto: "1 240 слушают", "4 832 слушают"); a modal that hides the rail.
**Cautionary tale, NOT a model:** Amazon Amp (shut down Oct 2023 — live-audio social died on cooled demand + no revenue).
Sources: Spotify Jam support; Spotify 2026 Request-to-Jam/Listening Activity; Apple Music SharePlay; Discord Listen Along; Turntable.fm → Hangout; Amazon Amp shutdown (MBW/GeekWire).

### D2 — Collaborative curation (queue / suggestions / accept-reject)
**Steal:** the **owner approval gate** (pending tray → Принять / Отклонить / "Принять и добавить во вкус"); **split permissions** (may-suggest ≠ may-control-playback); **inline attribution** on every pending card and accepted track ("от Ани"); **soft/silent decline** ("на потом", never a red "отклонено"); **spam control at the source** — Twinr refuses dupes/off-vibe at generation time, per-friend pending cap, mute/remove a contributor without erasing their already-accepted credit; **undo everywhere**.
**Avoid:** a single "collaborative ON/OFF" switch; auto-mutating taste on every accept; public reject badges; a separate full-screen moderation page.
Sources: Spotify Jam support; Spotify community "DJ that approves songs" (top-voted idea); Spotify collaborative-playlist invite/remove; Apple Music collaborative + SharePlay; Stationhead; YouTube collaborative-playlist voting (May 2025); open-Spotify-API rate-limit thread. *(Dropped per `must_fix`: "Fotify"/"VibeQueue"/"Lime DJ"/"Canny"/"Discord Sharing-mode" — unverifiable/category-mismatch; the patterns stand on the verifiable analogs above.)*

### D3 — AI-assisted group recommendation & taste blending
**Steal:** a **compatibility score** ("совместимость вкусов 73%") as a *scripted/seeded* Blend-style analog (NOT computed live — friends are seeded, no backend); **per-track attribution chips** ("для вас двоих" / "тянет к вкусу Ани" / "твоё ядро"); **two-sided explainable "почему"** naming both people (friend's ask + owner's vector) + optional counterfactual hover; **owner-anchored aggregation** = `owner_fit (hard floor) × friend_ask_fit` (a multiplicative, owner-floored rule) so an accepted track never drops below the owner's threshold; one tangible owner **dial** "Моя станция ↔ Поровну" that, in the demo, *swaps which pre-authored suggestion Twinr surfaces*.
**Avoid:** plain Average-to-mush; Most-Pleasure framing; a synthetic DJ voice; verbose paragraph explanations; **mis-citing research** — in Masthoff's studies plain Average performs *well* and Most-Pleasure is *not* the single "worst"; the owner-floor is a design choice to protect the owner, not "Average-without-Misery." [`must_fix`]
Sources: Spotify Blend (taste-match % + who-it's-for avatars); Spotify Jam; Spotify community "AI DJ in Jam" (the white-space request); Spotify AI DJ voice requests (May 2025); group-recommender literature (Masthoff aggregation strategies; "With Friends Like These…" 2025; LLM-enhanced group rec 2025).

### D4 — Sharing your taste / station (the entry point)
**Steal:** a **3-object mental model** kept as a *2-branch fork* — (A) a static, screenshot-able **taste/Волна card** (Wrapped-style purpose-built 9:16, not a raw screenshot) and (B) a **live "Слушать вместе" session** that routes into the rail; **multi-rail invite** (copy-link + brand-glass QR/"Город-код" + seeded "позвать друзей"); a **read-only recipient preview** before join (host taste snapshot + now-playing **with its "почему"** + who's already in) — *this rich preview is our original, not a Jam copy*; **privacy defaults** (card = "видно только по ссылке", session = private/invite-only, host can remove/end).
**Avoid:** one ambiguous "Share" button; a card that secretly implies live presence; fabricated precedents — there is **no documented "~5-min Jam invite timeout"**, Jam is **not** "anonymous", and the rich pre-join preview is **not** a Jam feature. ["Город-код" is **net-new** — 0 matches in the proto.] [`must_fix`]
Sources: Spotify Wrapped; stats.fm; Spotify Jam + Spotify Codes (Aug 2025) + Request-to-Jam (Jan 2026); Spotify Blend; Apple Music profile privacy tiers; Last.fm Friends/Neighbours.

---

## 3. SHARE FLOW — the entry point

### 3.1 Entry — a 2-branch fork off `#/taste` and `#/home`
Add a **"Поделиться"** affordance to the header of both `#/taste` (the editable taste-cloud) and `#/home` (the live Волна). Tapping opens a small dark-glass fork sheet (reuse the segmented-composer visual language) with two explicit jobs:

- **(A) «Карточка вкуса» / «Карточка волны»** → renders a static, shareable image (DOM/canvas-to-image) of the taste-cloud or current Волна in dark-cinema glass + Onest + `#5168FC`, with a one-line "почему"-tagline baked in. Async, one-to-many, no commitment. *Card never implies live presence.*
- **(B) «Слушать вместе»** → spins up the **live shared-session room in the rail** + an invite card (link / QR-«Город-код» / "позвать сид-друзей"). Synchronous, routes into the always-visible rail.

### 3.2 What is shared
| Branch | Object | Surface reused | Honesty |
|---|---|---|---|
| A | Snapshot **taste/Волна card** (image) | `#/taste` cloud render + `#/home` now-playing + Twinr tagline | static; no presence |
| B | **Live session room** + invite (link, «Город-код» QR, seeded friends) | rail room + auto-follow + seeded presence | `демо: друзья смоделированы`; «Город-код» = net-new artifact |

Privacy default: card = «видно только по ссылке»; session = private/invite-only; host can «завершить сессию» and remove a participant. No real data leaves; opt-in only for any "currently listening".

### 3.3 Recipient first-run (deep-link target — a single new scripted route)
Open **read-only preview before join** (reuses `#/taste` cloud read-only + `#/home` now-playing + Twinr "почему" + seeded presence list):
1. Host name/avatar (art-tint monogram).
2. Host taste-cloud snapshot.
3. **Now-playing with its "почему этот трек"** ← our differentiator, visible *before* joining (Jam shows songs; we show *explained* songs).
4. Who's already in the room (seeded avatars).
5. One CTA: **«Присоединиться и слушать вместе»** → drops into the rail session room.
Preview is open (no signup); join may be gated. Anything that can't truly pair a second device is marked `демо — откроет сессию у вас`.

### 3.4 ASCII — share card (taste/Волна snapshot, branch A)
```
╭───────────────────────────────────────────────╮
│  ●  Город.fm                          демо ▸    │   ← dark glass, Onest, #5168FC
│                                                 │
│   ВОЛНА ЭЛЬБИКА · «меланхоличное электро»       │
│                                                 │
│        ·  darkwave  ·                           │
│   · пост-панк ·      ◯ dream-pop                │   ← editable taste-cloud render
│        · synthwave ·     · IDM ·                │      (bubble sizes = weights)
│              · ambient ·                        │
│                                                 │
│   ▸ Сейчас: «Звёзды» — Buerak                   │
│   «почему: рядом с твоим darkwave-ядром»        │   ← the tagline = the wedge
│                                                 │
│   ──────────────────────────────────────────   │
│   Слушать вместе →   [ gorod.fm/w/elbik ]  ▣QR  │   ← link + «Город-код» (net-new)
╰───────────────────────────────────────────────╯
   видно только по ссылке · друзья смоделированы (демо)
```

---

## 4. SESSION MODEL — host, guests, presence, the rail room

### 4.1 The shared session = a SPECIAL RAIL ROOM (not a new page)
The rail already has rooms (pinned «Общий эфир» + per-station), per-room state `{html, scrollTop, draft, mode, seeded}`, seeded presence, and non-destructive **auto-follow** of the playing station. The shared session is **one more room type** pinned at the top while active:

```
RAIL (always visible)
├─ «Слушаем вместе · станция Эльбика»   ◉ session room (host-owned, while active)
├─ «Общий эфир»                          (pinned global)
├─ «<играющая станция>»                  (auto-follow, non-destructive)
└─ …
```
Auto-follow is **suspended-but-not-destroyed** while a session is active: the session room takes focus, the auto-follow room is preserved and restored on «завершить сессию» (reuse the existing non-destructive room state).

### 4.2 Host vs guests — lifecycle & control rules
- **Host = the Волна/taste owner.** Owner owns lifecycle: start («Слушать вместе») and end («завершить сессию» from the room header → ends for everyone, Jam-style host-leaves-ends-it). Owner can remove a participant.
- **Guests (seeded):** present + chat + react + **suggest via Twinr**. By default they **cannot** skip/pause/reorder/steer the live Волна.
- **Permission ladder (default-safe, plain-RU labels, not raw switches):**
  1. **Предлагать** → owner gate (default ON for all guests).
  2. **Рулить волной** → a trusted friend's "сделай по-другому" acts directly (still *ephemeral*, never edits the saved profile) — *explicitly granted per-friend* («дать Ане право рулить»).
  3. **Менять вкус** → **owner-only, always, never delegable** (the crown jewel).
- Optional per-station toggle **«Авто-приём от друзей»** (gated → open) and per-friend **«доверять предложениям Ани»**, both shown OFF-by-default to telegraph the curate-first stance. Scripted/inert in the demo. (This is *our* stance — not attributed to a Spotify "host toggle".)

### 4.3 Presence + sync indicator
- Room-header chip: **`◉ 4 слушают · в синхроне`** with 3–4 seeded art-tint monogram avatars.
- **Intimate counts in the private session room** ("4 слушают") — an *intentional contrast* with the existing big seeded public-room counts ("1 240 слушают"); do not delete the big counts, just scope small ones to the private room.
- **Avatar pulse on reaction** — *inspired by* Turntable's embodied approval (Turntable's actual signature is continuous beat-synced head-bob; ours is a per-reaction pulse). Reuse the existing pulse/animation pattern (verify exact helper before claiming literal reuse).
- **"в синхроне" breath** — reuse the `--dur-breathe` (1600ms) timing token as a persistent in-sync breath on the chip. NOTE: `--dur-breathe` is currently wired to fire only while Twinr speaks (`twinr-breathe`); this is a **new animation context** reusing the *token*, not the live trigger. Mark `демо`.

### 4.4 Playback control rules
- Single source of truth = the existing `isPlaying`/now-playing transport, re-read as the room's **«общая»** transport with a **«слушаем вместе · в синхроне»** pill near the player.
- Owner-only skip/pause by default. No per-guest scrubber (would imply independent control, contradicting suggest-only).
- On track change / accept, fire a seeded rail line: **`▶ Сейчас у всех: «<track>» — добавил по просьбе Ани`**.
- Honestly labeled: no real cross-device sync; `демо: друзья смоделированы`.

---

## 5. SUGGESTION → ACCEPT FLOW (the hero interaction)

### 5.1 How a friend's Twinr suggestion enters
The AI lane already has the segmented composer **[👥 Всем | ✦ Twinr]** and private Twinr replies ("видно только вам"). The group flow reuses it as a **new message type — a pending suggestion card** interleaved in the session room:
1. Seeded friend "asks Twinr" in the room: `✦ Аня → Twinr: больше пост-панка под вечер`.
2. **Twinr mediates** (owner-anchored): scores `owner_fit (floor) × friend_ask_fit`. If below the owner's floor or a duplicate, Twinr **refuses at generation time** — visible guardrail: `Twinr: это уже в твоей волне` / `Twinr: уводит станцию от твоего вкуса — предложить ближе?` (demo this once with a seeded dupe). Spam never becomes a card.
3. Otherwise Twinr posts a **pending suggestion card** to the owner.

### 5.2 Attribution, gate, reactions
- **Attribution inline + always visible:** `Аня предложила через Twinr` + avatar. (Inline, not buried — stated as our design goal, *not* a factual jab at Spotify.)
- **Two-sided "почему":** one clause for the ask, one for the owner's vector — `Аня просила под вечер; ложится в твоё «меланхоличное электро» — поэтому вам обоим`. Optional counterfactual on hover: `без вкуса Ани Twinr предложил бы X`. A private "видно только вам" Twinr line can give the owner the rationale before a public accept.
- **Owner-only gate:** `[ Принять ]` `[ Принять и добавить во вкус ]` `[ Не сейчас ]`.
- **Seeded pre-vote reactions** (🔥 / 👍 / 😴, seeded counts "3 тоже хотят") inform but never override the gate.

### 5.3 What happens on accept
- **«Принять»** → track animates into the Волna; persists a `от Ани` chip on the track (tapping it shows Twinr's "почему" — attribution and explanation are the same surface).
- **«Принять и добавить во вкус»** (secondary, explicit) → ALSO mutates the Twinr profile via the **same path "сделай по-другому" already uses** — a new, attributed, removable bubble fades into `#/taste`: `+ darkwave — от Ани`. **Preview the taste change before confirming.** Guarded by the existing "тренировочная волна не переписывает вкус навсегда" rule (proto ~line 10360) — taste mutates **only on explicit accept**, never silently.
- **«Не сейчас»** → **soft/silent to the room**; the suggester sees a quiet "на потом", never a red "отклонено".

### 5.4 Spam control & undo
- Twinr is the spam filter (refuses dupes/off-vibe at generation — §5.1).
- Per-friend cap on pending suggestions (no flooding).
- Owner can mute/remove a contributor **without erasing credit on tracks they already had accepted**.
- **Every accept is undoable**: remove from Волna + remove the taste bubble.

### 5.5 ASCII — pending suggestion card (in the rail AI lane)
```
┌─────────────────────────────────────────────┐
│ ✦ Twinr · предложение           видно вам ▸  │
│                                              │
│  [▤]  «Звёзды» — Buerak                      │   ← art-tint cover + монограмма
│       🔥 3 тоже хотят                         │   ← seeded pre-vote reactions
│                                              │
│  Аня предложила через Twinr                  │   ← attribution, inline
│  ┝ почему: Аня просила под вечер; ложится    │
│    в твоё «меланхоличное электро»            │   ← two-sided «почему»
│    (без вкуса Ани → Twinr предложил бы X)    │   ← counterfactual, on hover
│                                              │
│  [ Принять ]  [ + во вкус ]  [ Не сейчас ]   │   ← owner-only gate
└─────────────────────────────────────────────┘
   принятие добавит «+ darkwave — от Ани» во #/taste · можно отменить
```

---

## 6. AI GROUP CURATION — how Twinr proposes for the group

- **Owner-anchored aggregation (not consensus mush).** Twinr never averages to beige. Rule: `score = owner_fit (hard floor) × friend_ask_fit`. Every accepted track clears the owner's taste floor (no dilution) while honoring the friend's ask. This is a **multiplicative, owner-floored** strategy — *not* "Average-without-Misery", and it deliberately avoids Most-Pleasure (one friend hijacking). Below-floor asks get an honest reframe offer rather than a forced pick.
- **One tangible owner dial:** «насколько подстраиваться под гостей» (**Моя станция ↔ Поровну**). In the scripted demo the dial position **swaps which pre-authored suggestion Twinr surfaces** (Моя станция → tighter to owner; Поровну → a touch more adventurous). Reuses the taste-edit UX; no recomputation.
- **Compatibility at join.** When a (seeded) friend joins, show a **scripted** «совместимость вкусов · 73%» — a Blend-style analog, **not** computed live (friends are seeded; no backend). Seed the session's first track with the highest owner↔friend overlap, chipped `для вас двоих`.
- **Room-level "почему".** The shared now-playing carries the same "почему этот трек" visible to everyone — the explainability Jam/Stationhead lack. Group suggestions add the friend's name as a second input to the existing explain template. Keep explanations to one concise line (literature favors single-tradeoff explanations); counterfactual on demand only.

---

## 7. WHERE IT LIVES — per surface

| Surface | Treatment |
|---|---|
| **Rail — shared-session room** | New pinned room type while active; header chip `◉ N слушают · в синхроне` + seeded avatars + «частная · по ссылке» pill + «завершить сессию» + per-participant remove. Auto-follow suspended-not-destroyed, restored on end. |
| **Rail — AI lane** | New message type = pending suggestion card (cover + 🔥 seeded reactions + attribution + two-sided «почему» + owner-only `Принять / + во вкус / Не сейчас`). Reuses [👥 Всем \| ✦ Twinr] composer + private "видно только вам". |
| **`#/taste`** | Header «Поделиться» → fork (card A / session B). On «+ во вкус» accept, a new attributed, removable bubble («+ darkwave — от Ани») fades in via the existing "сделай по-другому" mutation. |
| **`#/home` (Волна)** | Header «Поделиться» → same fork. Accepted track animates into the Волна with a persistent `от Ани` chip; «слушаем вместе · в синхроне» pill near the player; seeded `▶ Сейчас у всех:` rail line on change. |
| **Recipient deep-link route** | New scripted read-only preview (host taste snapshot + now-playing «почему» + present members) → CTA «Присоединиться и слушать вместе». |
| **Share card (image)** | DOM/canvas-to-image render, dark glass + Onest + `#5168FC`, baked "почему" tagline, «видно только по ссылке», `демо` mark, «Город-код» QR (net-new). |

---

## 8. STAGED BUILD PLAN (scripted/seeded, reusing rail + Twinr)

1. **Stage 0 — Seed data + demo scaffold.** Add 2–3 seeded friends (fixed taste vectors, art-tint monograms) + a global `демо: друзья смоделированы` marker convention. No UI changes to live flows. Reuses existing seeded-presence model.
2. **Stage 1 — Share fork + taste/Волна card (branch A).** Add «Поделиться» to `#/taste` + `#/home` headers → fork sheet; build the DOM/canvas-to-image card render (static, "видно по ссылке"). Fully self-contained, no rail dependency.
3. **Stage 2 — Live session room (branch B) + presence.** New pinned rail room type tied to the active Волна; header chip `◉ N слушают · в синхроне`, seeded avatars, «частная» pill, «завершить сессию», auto-follow suspend/restore. Seeded friend join/leave lines on a timer.
4. **Stage 3 — Invite rails + recipient preview.** Copy-link + brand-glass «Город-код» QR (net-new) + seeded «позвать друзей»; new scripted read-only preview route (host taste snapshot + now-playing «почему» + present members) → join CTA. Demo-mark anything that can't truly pair a device.
5. **Stage 4 — Suggestion → accept hero loop.** New AI-lane message type (pending suggestion card): seeded friend asks Twinr → Twinr posts card with two-sided «почему» + seeded 🔥 reactions + owner-only gate. «Принять» → Волна + `от Ани` chip; «+ во вкус» → previewed, attributed, removable taste bubble via the "сделай по-другому" mutation path; «Не сейчас» → silent soft state. Undo wired.
6. **Stage 5 — AI group curation polish.** Owner-anchored aggregation (scripted suggestion-swap by dial «Моя станция ↔ Поровну»); scripted «совместимость · 73%» at join; seeded dupe/off-vibe Twinr refusal to demo the guardrail; room-level "почему" on shared now-playing.
7. **Stage 6 — Sync feel + honesty pass.** «в синхроне» breath (reuse `--dur-breathe` token in a new context), «слушаем вместе» pill, seeded `▶ Сейчас у всех:` lines; a11y sweep (focusable controls, labels, rail focus order); final `демо` labeling audit so nothing reads as live.

---

## 9. OPEN DECISIONS for the owner

1. **Card object scope:** ship both «Карточка вкуса» and «Карточка волны» as separate cards, or one combined card? (Affects Stage 1 surface count.)
2. **«Город-код» visual:** real scannable QR encoding a deep-link vs a branded-glass decorative code that only opens the session locally (demo)? Net-new artifact either way.
3. **Permission-ladder exposure:** surface the «Рулить волной» / «Авто-приём» toggles in the demo (scripted/inert) to telegraph the design stance, or hide them entirely until a real build?
4. **Taste-nudge default:** should «Принять» offer the «+ во вкус» path inline every time, or keep taste-mutation behind a separate confirm step only (to protect the profile from drift)?
5. **Compatibility score:** show the scripted «совместимость · N%» at join, or omit it to avoid implying real cross-user computation even with a `демо` tag?
6. **Recipient preview depth:** full taste-cloud snapshot in the preview, or a lighter identity-only preview (name + now-playing «почему») to keep the deep-link route cheap?
7. **Reactions surface:** seeded 🔥/👍/😴 pre-votes on pending cards (more alive, more rail clutter) vs attribution-only cards (cleaner)?

---

## SOURCES (consolidated)

**Group / social listening**
- https://support.spotify.com/us/article/jam/
- https://newsroom.spotify.com/2026-01-07/listening-activity-request-to-jam-messages-updates/
- https://newsroom.spotify.com/2023-09-26/spotify-jam-personalized-collaborative-listening-session-free-premium-users/
- https://support.apple.com/guide/iphone/play-music-together-using-shareplay-iph212965adb/ios
- https://support.apple.com/guide/facetime/use-shareplay-to-watch-and-listen-together-fctm725416ba/mac
- https://support.discord.com/hc/en-us/articles/115003966072-Listening-Along-with-Spotify
- https://screenrant.com/turntable-fm-org-dj-music-virtual-club-rooms-explained/
- https://www.hypebot.com/hypebot/2024/08/turntable-returns-as-hangout.html
- https://www.musicbusinessworldwide.com/amazon-shutters-live-radio-app-amp-less-than-20-months-after-it-launched/ (cautionary tale only)
- https://www.geekwire.com/2023/amazon-pulls-the-plug-on-amp-the-live-audio-app-it-launched-last-year-to-reimagine-radio/

**Collaborative curation / accept-reject**
- https://community.spotify.com/t5/Live-Ideas/Social-Party-Mode-with-DJ-that-approves-songs/idi-p/4900147
- https://community.spotify.com/t5/Spotify-for-Developers/API-rate-limit/td-p/5064564
- https://routenote.com/blog/spotify-invite-to-collaborative-playlists/
- https://www.simplymac.com/apps/new-apple-music-feature
- https://www.stationhead.com/
- https://support.google.com/youtube/answer/6109639
- https://support-apps.discord.com/hc/en-us/articles/26502500234519-Watch-Together-FAQ

**AI group recommendation & taste blending**
- https://newsroom.spotify.com/2025-05-13/dj-voice-requests/
- https://community.spotify.com/t5/Live-Ideas/Allow-Spotify-AI-DJ-to-Fully-Work-in-Jam-Sessions/idi-p/7460806
- https://screenrant.com/spotify-blend-valentines-day-explained-music-compatibility/
- https://towardsdatascience.com/an-introduction-to-group-recommender-systems-8f942a06db56/
- https://ceur-ws.org/Vol-2955/paper11.pdf
- https://link.springer.com/chapter/10.1007/978-1-4899-7637-6_22
- https://arxiv.org/html/2505.04273
- https://arxiv.org/pdf/2507.19283

**Sharing taste / station (entry point)**
- https://newsroom.spotify.com/2024-12-04/10-years-spotify-wrapped/
- https://apps.apple.com/us/app/stats-fm-for-spotify-music-app/id1526912392
- https://newsroom.spotify.com/2025-08-11/how-to-use-create-and-share-spotify-codes/
- https://freeyourmusic.com/blog/how-to-make-a-blend-on-spotify
- https://support.apple.com/en-us/HT210664

**Grounding (this codebase):** `designs/gorod-fm.html` — verified: rail rooms + «Общий эфир» + auto-follow; [👥 Всем \| ✦ Twinr] composer (~l.3082/3461); private "видно только вам"; `#/taste` editable bubble-cloud + `#/home` Волна + `#/lives`; "сделай по-другому"/"почему этот трек"/"Больше такого"; `--dur-breathe` (1600ms, `twinr-breathe`); art-tint monogram avatars; seeded public counts ("1 240 слушают", "4 832 слушают"); taste-mutation guard (~l.10360). **«Город-код» = net-new (0 matches).**
