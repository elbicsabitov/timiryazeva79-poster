# Город ФМ — Cold-Start Onboarding & Preference Elicitation

**Topic:** Turning a handful of bubble taps (and novel inputs like a resume) into a strong initial "Twinr" taste profile, fast, with minimal drop-off.
**Audience:** founder + eng lead. Opinionated. Cite-as-you-read.

---

## 1. What the incumbents do (and why it works)

**Apple Music bubble onboarding** is the gold standard and the one Город ФМ should clone-then-beat. Mechanics: a screen of floating **genre bubbles**; **single-tap = like, double-tap = love, press-and-hold = dislike**. Selecting a genre **blooms a second screen of artist bubbles** weighted toward your chosen genres, plus an "Add an Artist" escape hatch. The signal feeds the "Listen Now" engine immediately, and Apple explicitly tells users *the more you tap, the better day-one personalization* — i.e. they convert effort into a felt **IKEA-effect** ([MacRumors setup guide](https://www.macrumors.com/how-to/set-up-apple-music/), [iMore](https://www.imore.com/how-tell-apple-music-what-you), [Apple Music algorithm guide 2026](https://beatstorapon.com/blog/the-apple-music-algorithm-in-2026-a-comprehensive-guide-for-artists-labels-and-data-scientists/)). Why it works: (a) **three-level affordance** (like/love/dislike) triples information per tap vs binary; (b) **genre→artist recursion** is itself active learning — your genre picks prune the artist candidate set; (c) it produces a visible **"aha"** payoff (instant sample playlists).

**Spotify** is the architectural reference for *what to do with the taps*. Onboarding signals (selected **artists, genres, languages**) are encoded **through the same embedding pipeline as established users** (an **autoencoder** that compresses multi-signal + demographic features into a compact user embedding), then **gradually decayed toward behavioral signals** as listening accrues. Their ablation is the killer stat: **removing onboarding signals drops nDCG@50 by 13.8% on onboarding-aligned clusters**, and accuracy improves **+5% within the first 4 hours** ([Spotify Research: Generalized User Representations, 2025](https://research.atspotify.com/2025/9/generalized-user-representations-for-large-scale-recommendations)). Spotify also seeds **regional-trend default playlists** for the truly cold — relevant for a KZ/RU-market launch.

**Takeaway:** the bubble UI (Apple) and the embed-then-decay backend (Spotify) are *separable* best-practices. Город ФМ should adopt both.

---

## 2. Active learning: which bubbles to surface

Goal: **few taps → maximum information gain** about the taste vector. The literature splits into **non-personalized** (popularity / variance / entropy heuristics — good for screen 1 when you know nothing) and **personalized** (adapt the next screen to prior taps) strategies ([Nature Sci Reports 2025, AL for user cold-start](https://www.nature.com/articles/s41598-025-09708-2); [Greedy SLIM, arXiv 2406.06061](https://arxiv.org/pdf/2406.06061)).

Concrete selection rules for Город ФМ:
- **Screen 1 (genres):** pick **high-entropy / high-variance** items — genres that *split* the population (electronic, hip-hop, rock, Kazakh/CIS pop, classical), not just the globally most popular. Popularity-only seeding causes **popularity bias** and low diversity ([Inherited Popularity Bias, arXiv 2510.11402](https://arxiv.org/pdf/2510.11402)).
- **Screen 2+ (artists):** go **personalized** — surface artists that maximally *disambiguate* within the chosen genres (uncertainty sampling). The strongest 2025 result is a **ternary decision tree** (like / dislike / **unknown** at each node) combined with **pairwise comparison** ("which of these two?") because *humans judge comparatively better than absolutely*, and **mixing attribute queries (genre) with item queries (artist)** beats item-only. Pairwise trees beat single-item trees, and the hybrid beats popularity/entropy baselines by ~iteration 13 ([Pairwise & Attribute-Aware Decision-Tree Elicitation, arXiv 2510.27342](https://arxiv.org/html/2510.27342)).
- **Always reserve ~10-20% of bubbles for exploration** (a "wildcard" ring) so the profile isn't trapped in the first genre clicked.

**How many is enough?** No universal threshold, but the practical consensus: **3 genres + ~5-10 artists** yields a usable vector; marginal info-gain flattens fast after ~10-15 selections. Gate the "Done" button at **≥3 picks**, celebrate at ~8, allow stop anytime.

---

## 3. Bubble taps → initial Twinr vector (the algorithm)

Recommended pipeline (build this exactly):

1. **Pre-train item embeddings.** Learn artist/genre vectors with **item2vec** over listening-session co-occurrence (artists that co-occur in playlists/sessions land near each other) ([item2vec, arXiv 1603.04259](https://arxiv.org/pdf/1603.04259)). Genres get their own vectors or are the centroid of their artists. Cold launch with no logs? Bootstrap from public co-listening data / editorial playlists, swap to your own logs within weeks.
2. **Pool taps into a user vector.** `twinr_0 = Σ wᵢ · embed(itemᵢ)`, where `w = +2 (love), +1 (like), −1.5 (dislike)`. Dislikes **subtract** — this is why the press-and-hold gesture is worth keeping.
3. **De-bias for popularity BEFORE averaging.** Embedding **magnitude correlates with popularity**; cosine (not dot product) for relevance, and apply **test-time/L2 normalization** or directional correction so a tap on a mega-star doesn't dominate ([Test-Time Embedding Normalization, arXiv 2308.11288](https://arxiv.org/pdf/2308.11288); [Rethinking Popularity Bias, arXiv 2512.10688](https://arxiv.org/pdf/2512.10688)). Down-weight each seed by `log(popularity)` so niche taps carry *more* signal — niche picks are more identifying.
4. **Decay onboarding weight over time.** Per Spotify, blend `twinr = α·twinr_0 + (1−α)·twinr_behavioral`, with α annealing from 1→~0 over the first days/sessions.
5. **Make it explainable** (your differentiator): store the *named seeds* alongside the vector so the UI can say "Because you loved X and Y." Explainable active learning is a known, tractable design ([Explainable AL for Preference Elicitation, arXiv 2309.00356](https://arxiv.org/pdf/2309.00356)).

---

## 4. Conversational onboarding (an alternative / complement)

A chat onboarding ("tell me 3 artists you've had on repeat / describe your last good night out") fits Город ФМ's "AI companion" pillar. Modern CRS frameworks combine **preference elicitation + example critiquing** in natural language, and **active-learning question selection inside the dialogue** measurably improves elicitation ([ICER synthetic dialogue, arXiv 2510.02331](https://arxiv.org/html/2510.02331); [AL in conversational RS, ResearchGate](https://www.researchgate.net/publication/351150845)). **Recommendation:** offer chat as a **secondary path** (a "skip the bubbles, just tell me" link), not the default — free-text is higher-friction and higher-drop-off than tapping. Use the LLM to **parse free text → genre/artist seeds → same vector pipeline** as §3. Keep bubbles primary for speed.

---

## 5. "Upload your resume → taste" — realistic design

This is feasible as a **fun, opt-in cold-start booster — not a precision instrument.** Pipeline:

1. User pastes/​uploads résumé or a social bio (LinkedIn/Instagram text).
2. **LLM extracts a structured persona**: age band, city, profession, subcultures, hobbies, era cues, languages. LLMs do zero-shot interest inference well and turn text rationale into structured tags ("studied in Berlin 2015-18", "into climbing") → latent signals ([Language-Based User Profiles, arXiv 2402.15623](https://arxiv.org/pdf/2402.15623); [Zero/Few-Shot LLM RecSys survey](https://blog.reachsumit.com/posts/2023/04/llm-for-recsys/)).
3. **Map persona → genre/artist priors** via an LLM prompt *grounded in your catalog* ("given this person, output 8 catalog genres + 12 artists with confidence 0-1"). Output is **soft priors with low weight** that **pre-light the bubble screen** (personalized first screen) — the user then confirms/corrects with taps. Never let it silently set the final profile.

**Accuracy expectations:** treat as **weak supervision** — it's a warm bias, not ground truth. A 30-year-old Almaty designer who studied abroad is a far better-than-random prior; it will still miss idiosyncratic taste. Always require **one confirmation screen of bubbles** so the user (not the LLM) owns the profile.

**Privacy/consent (non-negotiable):** résumés are sensitive PII (employer, education, sometimes age/location). Make it **explicit opt-in**, **process in memory and discard the raw doc** (store only derived tags), show the user **exactly what was inferred** ("we guessed: indie, electronic, Russian rap — fix this"), and never use it for the **taste-based ads** path without separate consent. This avoids a "creepy" backlash that would poison the headline feature.

---

## 6. Engagement, gamification & drop-off

The stakes: **60-80% of users churn in week 1**, **~90% abandon in 3 days** without an immediate "aha"; **progressive disclosure + gamification lift completion ~50%**, and gamified onboarding makes users **~3× more likely to adopt** ([SaaSFactor: why users drop off](https://www.saasfactor.co/blogs/why-users-drop-off-during-onboarding-and-how-to-fix-it); [StriveCloud gamification](https://www.strivecloud.io/blog/gamification-examples-onboarding); [Amplitude IKEA-effect](https://medium.com/@amplitudeHQ/onboarding-with-the-ikea-effect-how-to-use-ux-friction-to-build-retention-c33a155c8756)).

Design rules for Город ФМ:
- **Progressive disclosure:** one decision per screen (genres → artists → optional vibe), never a wall of options.
- **Make the bubbles the reward:** the recursive bloom (tap a genre, related bubbles spring out) is intrinsically playful — lean into animation/haptics.
- **Show the Twinr forming live** — a growing profile visualization as users tap is both gamification (progress) *and* your "visible evolving profile" differentiator.
- **Instant aha:** the moment they hit Done, **drop them into a playing, explained autoplay** ("starting from your love of X"). Don't show a spinner; show music.
- **Let them stop early** (≥3 picks) and **enrich later** via in-feed thumbs — don't gate the whole product on a long quiz.

---

## 7. Pitfalls

- **Popularity bias** — popularity-only seeds → everyone gets the same bland start; de-bias (§3.3).
- **One-genre trap** — without an exploration ring, the first tap dominates.
- **Over-long quiz** — info-gain flattens after ~10-15 picks; more screens just raise drop-off.
- **No dislike channel** — drop press-and-hold and you halve per-tap information.
- **Treating résumé output as truth** — it's a prior; always confirm. And the **privacy/consent** trap is existential for the ads feature.
- **Cold catalog** — if item2vec has no logs at launch, bootstrap embeddings from editorial/public co-listening, then retrain on your own data.

---

### Sources
- Apple Music onboarding: [MacRumors](https://www.macrumors.com/how-to/set-up-apple-music/) · [iMore](https://www.imore.com/how-tell-apple-music-what-you) · [Apple Music Algorithm 2026](https://beatstorapon.com/blog/the-apple-music-algorithm-in-2026-a-comprehensive-guide-for-artists-labels-and-data-scientists/)
- Spotify: [Generalized User Representations, 2025](https://research.atspotify.com/2025/9/generalized-user-representations-for-large-scale-recommendations)
- Active learning / elicitation: [Pairwise & Attribute Decision-Tree, arXiv 2510.27342](https://arxiv.org/html/2510.27342) · [Nature Sci Reports 2025](https://www.nature.com/articles/s41598-025-09708-2) · [Greedy SLIM, arXiv 2406.06061](https://arxiv.org/pdf/2406.06061) · [Explainable AL, arXiv 2309.00356](https://arxiv.org/pdf/2309.00356)
- Embeddings & popularity de-bias: [item2vec, arXiv 1603.04259](https://arxiv.org/pdf/1603.04259) · [Test-Time Embedding Normalization, arXiv 2308.11288](https://arxiv.org/pdf/2308.11288) · [Rethinking Popularity Bias, arXiv 2512.10688](https://arxiv.org/pdf/2512.10688) · [Inherited Popularity Bias, arXiv 2510.11402](https://arxiv.org/pdf/2510.11402)
- Conversational: [ICER, arXiv 2510.02331](https://arxiv.org/html/2510.02331) · [AL in CRS, ResearchGate 351150845](https://www.researchgate.net/publication/351150845)
- LLM text→taste: [Language-Based User Profiles, arXiv 2402.15623](https://arxiv.org/pdf/2402.15623) · [Zero/Few-Shot LLM RecSys](https://blog.reachsumit.com/posts/2023/04/llm-for-recsys/)
- Onboarding/gamification: [SaaSFactor drop-off](https://www.saasfactor.co/blogs/why-users-drop-off-during-onboarding-and-how-to-fix-it) · [StriveCloud](https://www.strivecloud.io/blog/gamification-examples-onboarding) · [Amplitude IKEA-effect](https://medium.com/@amplitudeHQ/onboarding-with-the-ikea-effect-how-to-use-ux-friction-to-build-retention-c33a155c8756)
