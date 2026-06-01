# Город ФМ — In-Context UX for Explainability, Steering & a Living Twinr Profile

**Topic 09 of the Город ФМ research.** Audience: founder + designer/eng lead. **Date:** 2026-06-02.
**Scope:** the *screens and gestures* (not the recsys/LLM internals — see [02-steerable-conversational.md] and [04-explainability-narration.md]). This is where Город ФМ's whole pitch — "music that's actually yours: see & edit your taste, know why every track plays" — either becomes tangible or stays a slogan.
**Bottom line:** Build **three coupled surfaces, all reachable from the player, none requiring chat**: (1) an always-on **why-chip** with progressive disclosure, (2) **quick dials + a free-text steer box** that share one session vector, and (3) a **first-class, editable Twinr profile screen**. Make the AI **legibly seamful** — show the reason, let the user reject/correct it, and feed that correction straight into the profile. The correction loop *is* the moat.

---

## 1. "Why this track" — inline, low-clutter, progressively disclosed

The model proven at scale is **Pandora's "Why This Song"**: it surfaces the actual genome attributes that drove the pick — *"…modern R&B stylings, subtle vocal harmony, mild rhythmic syncopation, mixed minor & major tonality, mixed acoustic and electric instrumentation"* (https://en.wikipedia.org/wiki/Music_Genome_Project, https://community.pandora.com/t5/Community-Blog/What-is-the-Music-Genome-Project/ba-p/116426). Pandora's failure mode is **clutter + jargon** — a wall of musicological terms behind a menu. Город ФМ wins by being shorter, plainer, and collaborative-first. Spotify's complementary move (every Prompted-Playlist track ships with a one-line "why it's here") drove **users up to 4× more likely to click** an explained recommendation (https://research.atspotify.com/2024/12/contextualized-recommendations-through-personalized-narratives-using-llms) — so the "why" is not decoration, it's conversion.

**Recommendation — three altitudes via progressive disclosure** (the canonical NN/g pattern: show common info by default, more on demand; secondary UI gets *subtle* affordances, full payload on hover/tap — https://ixdf.org/literature/topics/progressive-disclosure, https://www.uxpin.com/studio/blog/what-is-progressive-disclosure/):

- **L1 — always-on why-chip** under the now-playing title. 3–6 words, **one** reason, collaborative-first because it's the most validated style: *"Потому что вы слушали Молчат Дома"* / *"Темнее — как вы просили"*. A small ⓘ glyph is the only affordance. Never a paragraph.
- **L2 — hovercard / tap-sheet.** Expands the chip into the real evidence (the KG path or attribute deltas from file 04 rendered as a sentence + 2–3 "because you played X" tags). This is a *contextual* disclosure (revealed on demand), not a permanent panel — keeps the player clean.
- **L3 — full narrative / tour** only on explicit "tell me more." Never lead here; it breaks flow.

**Honesty constraint (load-bearing):** the chip must state the *real* signal that drove the pick. A post-hoc plausible story that mismatches the recsys is the fastest way to lose power users — the "scrutability" aim below depends on the reason being true and correctable.

---

## 2. Steering controls — dials + free text, both in the player

The market has **converged on dials-plus-free-text**, and Город ФМ should ship *both* because they serve different users:

- **Spotify AI DJ** — the steer is a single **"tap-the-DJ" button** bottom-right: a quick **tap = re-roll the vibe**; **press-and-hold = beep → speak or type a request** (genre/mood/artist/activity combos, e.g. "electronic beats for a midday run") (https://newsroom.spotify.com/2025-05-13/dj-voice-requests/, https://techcrunch.com/2025/10/15/you-can-now-text-spotifys-ai-dj/, https://www.tomsguide.com/entertainment/music-streaming/spotifys-ai-dj-now-takes-requests-heres-how-it-works). Lesson: **one button, two pressures** — re-roll vs. precise request.
- **Yandex «Моя волна»** — the dial set to copy. A settings sheet with **mood / activity / language** selectors rendered as **swipeable colored "wave" cards in a carousel** (sad·happy·calm·energetic; work·workout·road; Russian / foreign / instrumental), plus **«Встряхнуть»** = one-tap (or literal phone-shake) **re-roll** when "I like it but want something different now" (https://yandex.ru/support/music/ru/new-library/my-wave, https://yandex.ru/company/news/19-05-2026-01, https://music.yandex.ru/recommendations/). The carousel makes an abstract control *playful and glanceable* — directly applicable to a dark, Onest-set radio.

**Recommendation for Город ФМ's player bar:**
1. **Steer button (primary):** tap = «Встряхнуть» re-roll; long-press = free-text/voice steer box. Mirrors AI DJ muscle-memory.
2. **Quick dials (the lazy path):** a swipeable strip of **mood / energy / activity / language / decade** chips — pre-baked `SteerOp`s so the user never has to phrase anything. (Yandex's carousel, but as compact chips to fit a dark utility UI.)
3. **Free-text box (the precise path):** *"скажи, что поменять…"* — for anything the dials can't express ("больше синти, но не грустно"). Per file 02, this compiles to the **same session-intent vector** the dials write, so the two surfaces never fight.
4. **Per-track gestures:** **thumbs-up / «не нравится» / «меньше такого»** on every track — the cheapest steer and a profile signal. Spotify's homepage uses exactly this language ("more/less of a certain vibe"); make «меньше такого» visibly *do something* (a quick toast: "учту — реже такое").

**Coexistence rule:** dials and chips emit *typed* ops; free text emits a *parsed* op; both land on one ephemeral session vector with a transition ramp (file 02). The UI promise is "say it OR tap it — same radio reacts."

---

## 3. The Twinr profile as a first-class, editable object

This is the differentiator no incumbent fully shipped until 2026 — and Город ФМ should make it the **home of the product, not a settings page.**

- **Spotify Taste Profile (beta, Mar 2026)** is the closest precedent and a near-exact spec: a **visible model of your taste** showing artists, genres, **exploratory trends** ("starting to explore '90s alternative rock"), **vibes** ("hip-hop with distinctive influences"), and **habit signals** (workout/commute). Users **flag when it "misses the mark," ask for "more/less of a certain vibe,"** and those edits **steer the home feed** — *"what gets prioritized, what gets dialed back, what you discover next"* (https://newsroom.spotify.com/2026-03-13/taste-profile-beta-announcement/, https://techcrunch.com/2026/03/13/spotify-will-let-you-edit-your-taste-profile-to-control-your-recommendations/). Crucial design choice: **editing is optional** — "shape it as much as you'd like, or leave it."
- **Last.fm** shows what makes a profile feel *alive*: **real-time, ever-growing**, a "personal music museum" of how taste changed over years — **temporal continuity, not an annual snapshot** (https://www.techradar.com/audio/audio-streaming/forget-spotify-wrapped-and-apple-music-replay-this-unsung-app-beats-them-both, https://www.last.fm/about/trackmymusic).
- **Spotify Wrapped / "Music Evolution" + Apple Replay** show what makes it *shareable*: assigning named **"musical eras/phases"** with descriptors, bold typographic cards, one-tap share to TikTok/messaging (https://newsroom.spotify.com/2024-12-04/everything-you-need-to-know-about-your-music-evolution/, https://www.fastcompany.com/91239913/spotify-wrapped-2024-music-evolution). Город ФМ's edge: do this **live and year-round**, not once in December.

**Recommendation — render the evolving taste vector as an editable screen + a player widget:**
- **Human-readable mapping.** Never show raw embedding numbers. Group into **Genres / Moods / Artists / Eras**, each as a row with a **visible weight** (bar, ring, or sized chip). "How much of you is X."
- **Direct nudges.** Each row has **+ / − / pin / mute** (or a draggable slider). Dragging "synth-pop ↑" or pinning "Молчат Дома" writes to the **durable profile** with a **confirmation gate** (file 02's EMA + "pin this to your taste?") so one gym session can't corrupt identity. Muting a genre is a *hard* preference, not a soft nudge.
- **Alive, not static.** A timeline / "your eras" view ("раньше — synthwave; сейчас — пост-панк") + a **"что нового в вашем вкусе на этой неделе"** delta strip. This is Last.fm's continuity + Wrapped's narrative, merged.
- **Shareable card.** A generated "ваш Twinr этой недели" card (named era + top genres/artists) for Telegram/Instagram — CIS-native sharing is cheap viral surface.
- **Player widget (the always-visible hook):** a small **evolving Twinr badge** in the now-playing view that subtly animates when a steer/correction moves the vector — *visible proof the profile is real and you just changed it.* Tap → full screen.

---

## 4. Trust & scrutability — the research spine

- **Tintarev & Masthoff's seven explanation aims** — *transparency, scrutability, trust, effectiveness, persuasiveness, efficiency, satisfaction* — are **partly incompatible** (persuasiveness can hurt effectiveness), so **declare one aim per surface** and measure to match (https://link.springer.com/article/10.1007/s11257-011-9117-5). Map: **why-chip → transparency + satisfaction**; **dials/steer box → efficiency + (sense of) control**; **Twinr editor → scrutability** (the user can *inspect and correct* the model). Scrutability is the high-value, under-served aim — and it's precisely the "see & edit your taste" pitch.
- **Seamful design / Seamful XAI** (Inman & Ribes "Beautiful Seams," CHI'19, https://dl.acm.org/doi/fullHtml/10.1145/3290605.3300508; Seamful XAI, https://arxiv.org/abs/2211.06753): don't hide the AI's seams — **strategically reveal** the mismatch/uncertainty so users keep agency and can re-configure. For Город ФМ: surfacing *"я выбрал темнее, потому что вы просили — не то?"* and letting them reject it is a **beautiful seam** that converts a black box into a steerable instrument. Reveal the seam **at the moment of consequence** (the track), not buried in settings.
- **Scrutability closes the loop:** rejecting a stated reason on the chip should **edit the Twinr profile** (per file 04 §5). Explanation → correction → visible profile change → next track reflects it. That single loop is the product.

---

## Pitfalls (read before building)

1. **Pandora clutter / jargon.** A reason wall kills flow. One reason at L1; everything else behind progressive disclosure; plain Russian, not music theory.
2. **Two steering surfaces that disagree.** Dials and free text **must** write the same session vector, or the user feels the radio fighting itself.
3. **Profile as raw vector.** Never expose embeddings/percentages-as-noise. Map to genres/moods/artists/eras with human weights — otherwise "editable" is unusable.
4. **Edits silently corrupting identity.** Slow EMA + confirmation gate (file 02); separate *hard* mutes/pins from *soft* nudges. One workout ≠ new you.
5. **Fabricated/post-hoc reasons.** The chip must reflect the real serving-time signal; a caught mismatch destroys the whole "transparent" pitch.
6. **Dead-feeling profile.** A static settings page won't read as "alive." Needs the live delta strip, eras timeline, and a badge that *moves* when you steer.
7. **Russian-first steering & copy.** Dials, free-text parser, and «меньше такого» gestures must be first-class in RU/Cyrillic — don't assume an EN-tuned flow transfers.
8. **Forcing the chat window.** Chat is the *precise* path, not the *only* path. Dials + per-track gestures must let a user steer and inspect taste **without ever typing**.

---

## One-line blueprint
`Why-chip (L1 one reason → L2 hovercard → L3 tour) + Player steer button (tap=re-roll, hold=voice/text) + quick mood/energy/activity/lang/decade dials + per-track 👍/«меньше такого» → one session vector; with a first-class Twinr screen (genres/moods/artists/eras as editable weighted rows, +/−/pin/mute, eras timeline + weekly delta + shareable card) and a player Twinr badge that animates on every steer. Map why-chip→transparency, dials→control/efficiency, editor→scrutability (Tintarev & Masthoff); reveal beautiful seams (reject-the-reason) and route every correction back into the profile.`
