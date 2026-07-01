# RESEARCH wave-2 — Город ФМ discovery feed at FRONTIER standard

> Owner directive (2026-07-01): "убедись что структура ленты собрана по топовым мировым стандартам
> на передовом уровне + карпати ресёрч." Four deep parallel agents on the FEED specifically.
> Builds on wave-1 (`RESEARCH-gorod-fm-home-carousel-feed-search.md`). Constraints unchanged:
> dark `#0B0C0F` / accent `#5168FC` / Onest / anti-slop / **honesty wedge (no fabricated data)**.

## Thesis
The 2025-26 frontier already moved toward **explainable · steerable · context-aware** discovery
(Spotify "You're in Control / steer the algorithm" Dec 2025; Apple's *algo-torial* human-led curation;
Yandex «Моя волна» prompts + AI-sets; DSA Art. 27 forcing plain-language recommender disclosure +
controls + a non-profiling option). The black-box magic feed is last-gen. **Город ФМ's honesty
positioning is not fighting the trend — it IS the trend, done without cheating.** Our unfair edge:
we sit on **live эфир** = real РМГ DJs curating in real time — an editorial backbone pure-streaming
apps have to fake.

## §A — Recsys architecture (the engine)
- **3-stage funnel:** candidate generation → ranking → re-rank for diversity. Model *engagement*
  (play) and *satisfaction* (like/skip) as SEPARATE heads — never one score (YouTube MMoE).
- **The frontier move most clones miss — meta-rank the SHELVES, not just the cards.** Spotify BaRT
  ("Explore, Exploit, Explain," RecSys 2018) jointly ranks rows + cards; **the shelf title IS the
  explanation and the constraint** ("Потому что вы слушали X" both explains the row and defines what
  may fill it). This maps 1:1 onto our wedge.
- **Explore/exploit:** ε-greedy contextual bandit (ε≈0.15); reward = a stream **>30 s = 1** (blunt,
  honest). Surface exploration as a TRUST feature ("Пробуем для вас — может, зайдёт") instead of
  hiding it — the differentiator.
- **Cold-start → editorial + popularity → content-based** (genre/station metadata as cheap content
  proxy; Yandex Моя волна uses raw-audio content model for zero-play placement).
- **Calibrated recommendation** (Steck, Netflix RecSys 2018): keep feed genre-mix *proportional* to
  the user's real taste so minority interests aren't crowded out. Anderson et al. (Spotify, WWW 2020):
  pure algo → LOWER diversity, but diversity → higher retention + free→paid. Diversity is revenue.
- **Signal schema — log day one (can't backfill):** append-only event envelope
  `{ts, session_id, user|anon, type: play_start|play_30s|play_complete|skip|like|station_switch|hide|
  shelf_impression|card_click|search, entity:{kind,id}, context:{surface, shelf_id, slot_index,
  tod_bucket, dow, device}, value:{listen_ms,pct,skip_at}, propensity: ε_at_serve, was_explore}`.
  The two fields everyone forgets: **`slot_index` + `propensity`** (needed for unbiased offline training).
  Reward label = `play_30s`; fast-skip (<30 s) = negative.
- **MVP→scale, same UI:** MVP = client-side per-shelf candidate generators + linear scorer
  (`w·affinity + w·freshness − w·repetition − w·recent_skip + w·tod_match`) + greedy MMR diversity +
  ε-greedy shelf meta-ranker + provenance object built from the scoring features. Scale = swap in
  GBDT → two-tower embeddings → LinUCB/Thompson, interfaces unchanged.

## §B — Frontier mechanics (ADOPT / ADAPT / SKIP)
**ADOPT:** (1) per-card honest "why" provenance (the wedge, visible; Spotify Prompted Playlists +
DJ X rationale). (2) time-of-day adaptive home (daylist model) under *sober* labels — no "unhinged"
microgenre naming, no emoji. (3) text-prompt station tuning as a **transparent rules-mapped dial**
("спокойнее" → visible real filters echoed back "по запросу: X"), NOT a hallucinating LLM. (4)
preview-on-tap (native to live radio: center card = playing now). (5) dynamic shelf selection/reorder
— thin shelves HIDDEN, never padded (honesty = anti-slop).
**ADAPT:** (6) AI-DJ "why" as a TEXT interstitial in the queue ("Далее: … потому что …") — skip
synthesized voice for now. (7) Smart-Shuffle/blended queue but label "эфир" vs "рекомендация". (8)
one "Свежее сегодня" block that *verifiably* changes daily with a real timestamp.
**SKIP:** (9) full TikTok vertical-video feed (collides with the carousel; needs Canvas video our
РМГ catalog lacks → slop). (10) Canvas/Clips. (11) **all fabricated social proof** — play counts,
"trending #1", "2.3M слушают", friend counts (direct honesty violation; where incumbents cheat and we
win). (12) emoji-prompt flair / persona naming.

## §C — Radio-first (segregate by TIME-STATE, not media type)
- Best audio apps (SiriusXM Next-Gen, BBC Sounds, TuneIn, iHeart, Apple Music Radio, NPR One) split
  **live / linear-scheduled / on-demand**, not by content type. Shelves on-demand music apps DON'T have:
  **Сейчас в эфире**, **далее/up-next**, **программа передач (schedule)**, **записи эфира/catch-up**,
  live event modules, **local/geographic**.
- **Honest resume (critical):** a LIVE tile NEVER shows a progress bar (it's a lie). Live = pulsing
  LIVE badge + "К эфиру" (jump to edge); with a rewind buffer → "Слушать сначала / Отмотать" (BBC
  Sounds). Only **replays** get a real progress bar + "осталось N мин". LIVE badge ⟂ progress bar.
- **Carousel = the tuner** (6 РМГ, always present). **Do NOT repeat the 6 stations as the top feed
  shelf** (redundant filler). Feed = everything the carousel can't hold. "Похоже на [станцию]" must
  NOT return only РМГ (that's an ad) — mix adjacent taste.
- **Pair the wave with the tuner; never replace it.** NPR One sunset its app by dropping the station
  anchor and confusing loyal listeners. Carousel gives control; «Моя волна» gives surrender.
- Shows/DJs = **daypart-aware** (timeslot badges «сейчас» / «в 18:00»).

## §D — Curation · serendipity · transparency · habit
- **Curation = "algo-torial" hybrid:** interleave 1–2 human shelves (live эфир, «Выбор редакции»)
  → ML shelves → serendipity. Editorial LEADS on cold-start + brand voice; algo takes over as signal
  accrues. **Provenance chip on every shelf:** «Куратор» / «Подбор ИИ» / «Микс» / «Эфир».
- **Serendipity engineered:** genre/artist caps + intra-shelf artist cap + inter-shelf dedupe; a
  LABELED exploration shelf «Не ваш обычный выбор» (~20-30%, framed as a stretch, said out loud).
- **Transparency = the headline feature** (DSA Art. 27 tailwind): per-shelf one honest "why";
  per-item «Почему этот трек?» surfacing REAL signals (co-listening / same station / mood-tempo /
  editor pick); **every explanation ships with a CONTROL** («Меньше такого» / dials / genre toggles)
  — "explanation without a lever is theater." Add a plain «Как работает подбор» page + a
  **«Только редакция» non-profiling mode** (DSA-compliant + ultimate anti-slop flex).
- **Habit without dark patterns:** daypart reorder with a REAL timestamp «Обновлено 07:14 · утренний
  эфир»; daily «Волна дня» + Friday «Премьера»; **«Дежавю» from the user's OWN history** (huge pull,
  zero fabrication); honest rolling recap «Ваша неделя» from real data; streaks count real days and
  lapse gracefully — no loss-aversion nagging, no fake scarcity.

## §E — Definitive frontier feed (synthesis) — canonical shelf catalog
Below carousel + player. Adaptive **shelf selection + order** per session/time (hide thin ones).
Every shelf carries: **provenance chip · one honest "why" · one control** (where relevant). Grouped:

**Live / эфир (radio-unique, time-state):**
- `Сейчас в эфире` [Эфир] — live now-playing across the 6 РМГ stations; tap → live edge. Bridge from carousel.
- `Программы и ведущие` [Эфир · daypart] — shows/DJs w/ timeslot badges.
- `Записи эфира · Пропущенное` [—] — catch-up replays, the ONLY shelf with a real progress bar.
- `Сегодня в эфире` [Эфир] — compact daypart schedule strip (optional).

**Personal AI (Подбор ИИ):**
- `Моя волна` [Подбор ИИ] — the one "just play" adaptive stream + dials (настроение/язык/активность). Surrender core; reuses TwinrWave/GorodContext.
- `Похоже на [станцию]` [Подбор ИИ] — station-seeded cross-discovery; not РМГ-walled.
- `Дежавю` [Подбор ИИ] — from the user's own history; real signal only.
- `Не ваш обычный выбор` [Подбор ИИ] — labeled exploration/serendipity (~20-30%).

**Editorial / curated (Куратор / Микс):**
- `Выбор редакции ГОРОДА` [Куратор] — human picks; leads cold-start; brand voice.
- `Волна дня` [Микс · daypart] — daily-refresh mix, real timestamp.
- `Премьера` [Микс · Fri] — weekly new-releases anchor.

**Cross / social:**
- `Из эфира — песни` [Микс] — save/identify tracks the stations just played (live-radio ↔ AI-music bridge).
- `Друзья слушают` [social] — HONEST empty/onboarding state (no social graph yet — never fake friends).
- `Коллекции` [Куратор] — deep rubrics (по десятилетиям / языку / городу).

**Cross-cutting rules:** cold-start = 100% editorial + carousel (no faked personalization); thin
shelves hidden not padded; live never resumes; no fabricated counts anywhere; exploration surfaced;
calibrated genre mix; adaptive order visible with real timestamp.

## Sources
Spotify Explore-Exploit-Explain (RecSys'18) · McInerney write-up · YouTube DNN (Covington'16) + MMoE
(Zhao'19) · Steck Calibrated Recommendations (RecSys'18) · Anderson et al. WWW'20 (diversity) · Yandex
Моя волна / Yambda (2025) · Spotify Newsroom 2025-12-10 (steer) / 2025-09 (controls) / 2023-09 (daylist)
· Apple Music algo-torial (The Drum, 2025) · SiriusXM Next-Gen · BBC Sounds (+ live rewind/critique) ·
iHeartRadio 5.0 · TuneIn · Apple Music Radio · NPR One flow + sunset · DSA Art. 27 (DSA Observatory,
Pinsent Masons) · Spotify AI DJ (Dynamoi, Newsroom). Full per-agent citations in task transcripts.
