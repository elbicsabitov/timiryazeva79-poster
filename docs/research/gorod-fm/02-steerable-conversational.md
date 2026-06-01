# Город ФМ — Steerable & Conversational Music Recommendation

**Topic 02 of the Город ФМ architecture research.** Audience: founder + eng lead.
Scope: how the user *steers* taste in natural language ("make it darker", "more upbeat", "less like this", "for working out") and how that **live-corrects the Twinr profile** — plus the tech to build it without whiplash or unaffordable latency.

---

## 1. The core architectural decision: where does the LLM live?

There are three viable shapes. **Do not put a large LLM on the critical path of every track selection** — it is too slow and too expensive for a radio that must react in <1s. The 2024–2026 literature converges on a hybrid: **LLM for *interpretation*, classic recsys for *retrieval/ranking*.**

| Pattern | What it is | Verdict for Город ФМ |
|---|---|---|
| **LLM-as-recommender** | LLM directly emits tracks | ❌ hallucinates non-catalog songs, no personalization, slow |
| **LLM-as-planner / tool-caller** | LLM parses the request, then *calls* retrieval tools (dense embedding, BM25, SQL filters, semantic-ID retrieval) and ranks candidates | ✅ for the **chat companion** & one-shot prompt-to-playlist |
| **NL → control-signal → recsys** | NL request compiled into score adjustments / filters fed to the *existing* recommender | ✅✅ for **live radio steering** (the "say it and the radio changes" loop) |

The killer insight is **CTRL-Rec** (Carroll et al., Berkeley, Oct 2025, [arxiv.org/abs/2510.12742](https://arxiv.org/abs/2510.12742)): use the LLM **at training time** to simulate "would this user approve of item X given their request?", then **distill those judgments into embedding models**. At serving time you need **only a single LLM-embedding computation per request** — the control signal is then folded into the recommender's normal score weighting. Their user study (Letterboxd users) found it "significantly enhanced users' sense of control and satisfaction." **This is the blueprint for Город ФМ's steering**: the spoken/typed correction becomes one embedding, applied as a re-ranking nudge — not a fresh LLM call per song.

---

## 2. Mapping free-text feedback → concrete recsys controls

Every utterance should be **routed to the cheapest mechanism that satisfies it**. Build an intent router (small classifier or fast LLM) that emits a typed `SteerOp`:

| User says | Control mechanism | Implementation |
|---|---|---|
| "no rap", "only Russian", "nothing explicit" | **Hard filter** | metadata `WHERE` clause, deterministic |
| "for working out", "darker", "more chill" | **Soft re-rank** toward an audio/mood region | shift target vector in tempo/energy/valence + genre embedding space |
| "more like this" / "less like this" | **Embedding nudge (critiquing)** | move the session's query vector toward/away from the current track's embedding |
| "more upbeat" | **Attribute critique** | bump the `energy`/`valence` axis on the target vector |
| "do it differently" / "surprise me" | **Diversity/exploration boost** | raise novelty weight, widen ANN radius, drop recent-artist penalty |
| "play more 90s but keep the vibe" | **Constraint satisfaction** | decade filter ∩ current mood region |

The academic grounding is **critiquing-based conversational recsys**: *Latent Linear Critiquing* (Luo & Sanner, WWW 2020, [dl.acm.org/doi/10.1145/3366423.3380003](https://dl.acm.org/doi/abs/10.1145/3366423.3380003)) and *Deep Language-based Critiquing* (Wu et al., RecSys 2019, [ssanner.github.io/papers/recsys19_deepcrit.pdf](https://ssanner.github.io/papers/recsys19_deepcrit.pdf)) co-embed a keyphrase critique with the user-preference vector and solve a small LP for how strongly to apply it. **Город ФМ should treat each steer as a weighted vector operation on a live "session intent" embedding**, not a profile rewrite — see §4.

**Retrieval backbone for prompt-to-playlist:** the strongest published result is **Text2Tracks** (Spotify Research, Apr 2025, [research.atspotify.com/2025/04/text2tracks...](https://research.atspotify.com/2025/04/text2tracks-improving-prompt-based-music-recommendations-with-generative-retrieval) / [arxiv.org/abs/2503.24193](https://arxiv.org/abs/2503.24193)): a fine-tuned LLM does **generative retrieval** — it emits **semantic track IDs** ("zip codes in collaborative-filtering vector space") directly from the prompt via diversified beam search, **+127% accuracy vs the closest baseline**, and semantic IDs crush title-based IDs. For the conversational companion, **TalkPlay-Tools** (Oct 2025, [arxiv.org/html/2510.01698v1](https://arxiv.org/html/2510.01698v1)) positions the LLM as a **planner orchestrating SQL + BM25 + dense + semantic-ID retrieval** across multi-turn dialogue — the right shape for "build me a playlist for a rainy drive, but no sad songs." TalkPlay itself uses a vocabulary-expanded **Llama-3.2-1B** ([arxiv.org/html/2502.13713v3](https://arxiv.org/html/2502.13713v3)) — proof that a *small* model suffices.

---

## 3. What the incumbents actually shipped (cite-able prior art)

- **Spotify AI DJ ("DJ X")** — recsys picks tracks; a **fine-tuned small Llama** generates **culturally-aware spoken commentary**; the **"tap-the-DJ" button** is the steer (refresh/switch the vibe), and since May 2025 it **takes voice requests** ([newsroom.spotify.com/2023-02-22](https://newsroom.spotify.com/2023-02-22/spotify-debuts-a-new-ai-dj-right-in-your-pocket/), [9to5mac.com/2025/05/14](https://9to5mac.com/2025/05/14/dj-spotify-ai-now-takes-requests/)). Commentary facts are **human-editor-verified, not hallucinated**.
- **Spotify narratives research** ([research.atspotify.com/2024/12/contextualized-recommendations...](https://research.atspotify.com/2024/12/contextualized-recommendations-through-personalized-narratives-using-llms)): fine-tuned Llama, **+14% on Spotify-specific tasks**, editors supply "golden examples"; users were **up to 4× more likely to click** a recommendation that came **with an explanation** — direct validation of Город ФМ's *explainable autoplay* thesis.
- **Spotify AI Playlist / Prompted Playlists** ([2024-04-07](https://newsroom.spotify.com/2024-04-07/spotify-premium-users-can-now-turn-any-idea-into-a-personalized-playlist-with-ai-playlist-in-beta/), [2025-12-10 "You're in Control"](https://newsroom.spotify.com/2025-12-10/spotify-prompted-playlists-algorithm-gustav-soderstrom/)): prompt → 30 tracks, each with a **one-line "why it's here"**; users **revise in natural language** ("more pop", "less upbeat"); Söderström frames it as *"Spotify that doesn't just passively learn from you but literally listens to you."*
- **Spotify Taste Profile** (Mar 2026, [newsroom.spotify.com/2026-03-13](https://newsroom.spotify.com/2026-03-13/taste-profile-beta-announcement/)): a **visible, editable** taste model — users **flag inaccuracies and ask for "more/less of a vibe"**, which changes what gets prioritized. *This is exactly the Twinr profile* — Город ФМ should ship it as a first-class screen, not a hidden vector.
- **Yandex «Моя волна»** ([yandex.com/company/news/28-05-2025](https://yandex.com/company/news/28-05-2025)): **mood/activity/language dials** ("спокойный джаз для работы", "рок для бега") on top of the **ARGUS** autoregressive generative user model; **«Встряхнуть волну»** = one-gesture re-roll. The dials are a UI primitive Город ФМ should copy *alongside* free text (dials for the lazy path, chat for the precise path).

---

## 4. Steerable AND coherent — avoiding whiplash + the Twinr update rule

The central tension: a steer must change the radio *now*, but not erase who the user is. **Separate two memories:**

1. **Session intent vector** (ephemeral, fast-moving) — every steer mutates this. Decays over the session. This is what makes "darker" take effect in 1–2 tracks.
2. **Twinr taste profile** (durable, slow-moving) — updated only from **persistent signal**: repeated steers in the same direction, sustained skips/saves, explicit profile edits. Apply an **EMA with a low learning rate + confirmation gate** ("Lately you're reaching for darker, moodier tracks — pin that to your taste?"). This prevents one workout session from permanently turning the profile into gym music.

**Anti-whiplash:** the recommender already trades **coherence vs diversity** — recommended tracks should be "coherent continuations" with bounded tempo/key jumps between neighbors ([EPJ Data Science 2025](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-025-00531-3); [ACM TORS longitudinal diversity study](https://dl.acm.org/doi/10.1145/3608487)). So apply steers as a **target-region shift with a transition ramp** (cross-fade the query vector over 2–3 tracks) rather than a hard cut, unless the user said "skip"/"do it differently" (then cut immediately). Always **cap per-step novelty** to avoid filter-bubble collapse *and* avoid jarring jumps.

**Explainability is free here:** because every next track was chosen by a known `SteerOp` + scoring contribution, Город ФМ can say *why* ("darker pick because you asked for moodier, and you saved Molchat Doma") — this is the differentiator, and it doubles as **debuggability** for the eng team.

---

## 5. Latency budget ("say it and the radio changes")

Target end-to-end **< 800 ms** for a steer to alter the *next* track; < 2 s acceptable for a full prompt-to-playlist build.

- ASR/intent parse: 150–300 ms (small/fast model or on-device).
- Control compute: **one embedding** per CTRL-Rec (≈10–50 ms) — *not* a generative LLM call.
- Re-rank ANN over candidate pool: <50 ms.
- Spoken commentary (DJ mode) is generated **async/ahead** while the current track plays — never block playback on it.
**Rule: the generative LLM is allowed on the chat-companion path and the commentary path; it is NOT allowed on the per-track steering path.**

---

## 6. Evaluation of steerability

- **Offline:** measure **Steering Error** (did the output move toward the requested region?), **Orthogonality/side-effects** (did it move attributes the user *didn't* ask for?), and **Miscalibration** — the SteerEval / steerability-probe framing ([steerability.org](https://steerability.org/), [NeurIPS SafeGenAI 2024](https://openreview.net/pdf?id=y2J5dAqcJW)). Recent work warns **bigger models are *not* automatically more steerable** and side-effects are the main failure mode — so test for *unwanted drift*.
- **Online:** **steer-acceptance rate** (did the user keep listening after the steer vs immediately skip again?), correction-to-satisfaction, and **steer→save lift**. CTRL-Rec's headline metric was **subjective sense of control + satisfaction** — instrument that with a lightweight thumbs/"this is it" tap.
- **Guardrail:** track **catalog coverage** under steering so the system stays diverse, not collapsed to a few safe tracks.

---

## 7. Concrete recommendation for Город ФМ

1. **Two-tier memory**: ephemeral *session intent vector* (every steer) + durable *Twinr profile* (EMA + confirmation gate). Never let a steer silently rewrite Twinr.
2. **Build the steer compiler à la CTRL-Rec**: NL → typed `SteerOp` (hard filter | soft re-rank | embedding nudge | diversity boost | constraint) → applied as **one embedding / weight change**, LLM only at training time. This is the cheapest path to real-time and the most testable.
3. **Retrieval = Text2Tracks-style generative retrieval with semantic IDs** for prompt-to-playlist; **TalkPlay-Tools LLM-as-planner** (small Llama-3.2-1B class) for the multi-turn companion.
4. **Ship a visible, editable Twinr profile** (Spotify Taste Profile) **+ mood/activity dials** (Yandex Моя волна) **+ free-text chat** — three steering surfaces, one shared session vector.
5. **Transition ramp** (cross-fade the query vector over 2–3 tracks) except on explicit "skip/different"; **cap per-step novelty** to kill whiplash.
6. **Explain every steered pick** ("darker because you asked + you saved X") — proven 4× engagement lift, and it's your moat.

## Pitfalls
- **LLM on the hot path** → cost + latency death. Keep it to training/commentary/chat.
- **Hallucinated facts in commentary** → use a **fact/metadata layer + human-curated templates** (Spotify uses editor "golden examples"); never let the model assert tour dates/album facts unverified.
- **Steers permanently corrupting Twinr** → confirmation gate + slow EMA.
- **Filter-bubble collapse** under repeated "more like this" → enforce a novelty floor.
- **Side-effect drift** (steerability literature) → evaluate orthogonality; "darker" must not silently also make it slower/sadder if unasked.
- **Generative retrieval staleness** — new catalog tracks need ID assignment + periodic re-fine-tune; keep a dense-retrieval fallback for cold items.
- **Cyrillic/RU-language steering** must be first-class in the intent parser — test Russian critiques explicitly, don't assume an English-tuned router generalizes.

---
*Sources are linked inline. Key papers: CTRL-Rec ([2510.12742](https://arxiv.org/abs/2510.12742)), Text2Tracks ([2503.24193](https://arxiv.org/abs/2503.24193)), TalkPlay ([2502.13713](https://arxiv.org/html/2502.13713v3)) / TalkPlay-Tools ([2510.01698](https://arxiv.org/html/2510.01698v1)), Latent Linear Critiquing (WWW 2020), Deep Language-based Critiquing (RecSys 2019), steerability eval ([steerability.org](https://steerability.org/)). Industry: Spotify AI DJ / narratives / Prompted Playlists / Taste Profile; Yandex Моя волна / ARGUS.*
