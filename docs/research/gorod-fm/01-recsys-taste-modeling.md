# Music Recommendation & Taste-Modeling Architecture — Brief for Город ФМ

Scope: the engine behind the **evolving Twinr profile** and **explainable, steerable next-track** selection. Opinionated, with named tech and concrete recs.

---

## 1. The core stack: hybrid two-stage, not "an algorithm"

No serious service uses one model. The industry-standard shape is a **two-stage funnel**: cheap **candidate generation / retrieval** (catalog → a few hundred tracks) then expensive **ranking / re-ranking** ([Google Cloud two-tower guide](https://docs.cloud.google.com/architecture/implement-two-tower-retrieval-large-scale-candidate-generation); [Shaped two-tower deep-dive](https://www.shaped.ai/blog/the-two-tower-model-for-recommendation-systems-a-deep-dive)). Build this shape from day one — it is what lets you mix signals and stay cheap at scale.

**Collaborative filtering (CF) vs content-based vs hybrid.** CF (who-listens-to-what) is the strongest signal once you have usage, but it cannot rank a track nobody has played (cold-start) and can't *explain* in musical terms. Content-based (audio/metadata) fixes both but is taste-blind. **Hybrid wins** — this is now uncontested. Pandora's Music Genome (450 human-tagged attributes) was the content-purist; even Pandora now blends "raw audio analysis + collaborative filtering + editorial" ([TechCrunch](https://techcrunch.com/2018/03/28/pandora-takes-on-spotify-with-dozens-of-personalized-playlists-built-using-its-music-genome/); [AMW](https://amworldgroup.com/blog/music-radio-pandora)).

**Matrix factorization vs neural.** Spotify's classic CF is **vector models / matrix factorization** — project users, artists, tracks into a shared low-dim space, recommend by nearest-neighbour ([Erik Bernhardsson](https://erikbern.com/2015/09/24/nearest-neighbor-methods-vector-models-part-1.html)). They even learned **track vectors with Word2Vec over listening sequences** (a track in a queue ≈ a word in a sentence) — directly relevant to "flow." Recommendation: start with **MF/ALS or Word2Vec-on-sessions** for the CF tower (fast, robust, interpretable neighbours), graduate to neural two-tower later. Don't begin with deep models — you won't have the data.

---

## 2. Audio + metadata embeddings (the content tower)

You need a content embedding so cold tracks and "why" both work. Options, current SOTA:
- **CLAP** (Contrastive Language-Audio Pretraining) — maps **audio AND text into one space**, enables zero-shot and *text-queryable* audio ([CLAP paper](https://www.researchgate.net/publication/361253229_CLAP_Learning_Audio_Concepts_From_Natural_Language_Supervision)). This is the single highest-leverage model for Город ФМ because it makes **steering by natural language** ("make it more melancholic") a vector operation.
- **MERT** — self-supervised acoustic understanding ([MERT](https://arxiv.org/pdf/2306.00107)); **musicnn** — CNN tagger, the cheap reliable baseline.
- Benchmarks: musicnn gives a statistically significant lift over BERT4Rec; MERT ≈ CF-init ([Comparative Analysis, RecSys'24](https://arxiv.org/html/2409.08987v1); [contrastive neural audio for recsys](https://arxiv.org/abs/2409.09026v1)).
- **Metadata:** MusicBrainz/AcousticBrainz (BPM, key, mood) and editorial genre as cheap structured features.

**How to combine with CF:** the proven trick is **align content embeddings to the CF space via contrastive learning (e.g. CLCRec)** so a cold track lands near where CF *would* put it ([cold-start contrastive](https://www.emergentmind.com/topics/cold-start-item-recommendations)). Concatenate `[CF vec ⊕ CLAP vec ⊕ metadata]` as the item tower input.

> **Rec for Город ФМ:** dual item representation per track — a **CLAP/musicnn content vector** (always available, drives "why" + cold-start + steering) + a **CF vector** (fills in as plays accrue). This is exactly Yandex "My Wave"'s public design: "blending collaborative and content-based elements," analyzing spectrogram/timbre/rhythm in real time ([Yandex My Wave](https://ashgabattimes.com/index.php/en/2025/07/yandex-music-adapted-my-wave-under-the-pace-of-user-running/)).

---

## 3. Sequence/session models — radio ≠ playlist

Next-track is a **sequential** problem. Key models:
- **GRU4Rec** — RNN, session-based, the original ([overview](https://aman.ai/recsys/multi-armed-bandit/)).
- **SASRec** — self-attention; adaptively weights past items, long-range on dense data / recent on sparse; +6.9% HitRate, +9.6% NDCG over baselines ([SASRec](https://arxiv.org/abs/1808.09781)).
- **BERT4Rec** — bidirectional masked-item; strong but offline-flavoured.

**Radio/flow vs playlisting is a real architectural fork.** A *playlist* is a fixed bag judged as a set; *radio/flow* is an **unbounded online sequence** where each pick conditions on live feedback (skip/complete) and must balance coherence vs surprise. Город ФМ's product **is radio**: use a **session/sequence model (SASRec-style) as the re-ranker**, fed the live in-session history, and re-score after *every* skip/complete. Negative feedback matters — [contrastive learning on skips](https://arxiv.org/pdf/2409.07367) improves sequential music rec specifically.

---

## 4. The evolving Twinr profile (short vs long term, context)

Represent the user as **multiple vectors, not one**:
1. **Long-term taste** — slow EMA over completed/replayed tracks' embeddings (the visible, "evolving" Twinr).
2. **Short-term/session intent** — the sequence model's current hidden state; decays fast.
3. **Context** — time-of-day, mood, activity as side features (Yandex uses "running pace"; Spotify's session bandit shifts the content mix by context — commuter wants podcasts AM, music while working out ([Spotify neural contextual bandit](https://medium.com/@advaitss11/how-reinforcement-learning-quietly-runs-your-recommender-systems-b46601eab4cd))).

User-specific weighting of long vs short beats fixed weights ([parallel-attention LSTM](https://arxiv.org/pdf/2006.15346); [behavior-enhanced long/short](https://www.sciencedirect.com/science/article/abs/pii/S0020025524010417)).

**Implicit feedback → graded reward, not binary.** Skip-early = strong negative; complete = positive; replay = very positive; dwell/seek = signal. Model positive/negative/neutral distinctly ([implicit feedback modeling](https://arxiv.org/pdf/2205.06058)). Map to a scalar reward that nudges the EMA + retrains the ranker.

**Explicit corrections ("make it different") are the differentiator.** Implement as a **direct vector operation on the live profile**: parse the instruction with an LLM → a CLAP text embedding → shift the short-term intent vector (e.g. `intent -= α·"current cluster" + β·CLAP("more upbeat")`) and persist if repeated. Because it's the same embedding space, the change is *immediate and explainable*.

---

## 5. Explainability + exploration = Spotify BaRT (the blueprint to copy)

Город ФМ's "tells you WHY" maps **exactly** onto Spotify **BaRT** ("Bandits for Recommendations as Treatments") and its paper **"Explore, Exploit, Explain"** — the first system to jointly learn **(item, explanation, context) → satisfaction** and pick via a **contextual bandit**, treating the *explanation itself* as part of the arm to optimize ([Spotify Research](https://research.atspotify.com/publications/explore-exploit-explain-personalizing-explainable-recommendations-with-bandits); [BaRT overview](https://dynamoi.com/learn/faqs/what-is-spotify-bart-algorithm)). Exploit = highest predicted engagement; Explore = high-uncertainty items to learn + escape filter bubble.

**Exploration mechanism:** contextual bandits — **Thompson sampling or LinUCB** over candidates; cheaper start = **ε-greedy**. RL/slate methods (budget-aware MDP) lift play-rate over plain bandits but are heavier ([time-constrained slate RL](https://www.emergentmind.com/topics/time-constrained-slate-recommendation)); defer.

> **Rec:** Город ФМ's "why this track" string should be a **first-class arm**, generated from the *reason it was retrieved* (shared CF neighbour, matching CLAP attribute, your steer) and logged with the bandit reward — so you learn which *explanations* drive listening, not just which tracks.

---

## 6. Cold-start

- **New user:** bubble onboarding (Apple-Music style — you have this) seeds the long-term vector directly in **CLAP space** by mapping picked artists/moods to embeddings. "Upload résumé → infer taste": LLM → text → CLAP vector. **Active elicitation** (PERE) localizes the user to a region, +3–10% NDCG ([PERE](https://www.emergentmind.com/topics/cold-start-item-recommendations)).
- **New track:** content vector (CLAP/musicnn) only, aligned to CF space via contrastive init ([content-based init for cold items, RecSys'25](https://arxiv.org/pdf/2507.19473)); **LLM/metadata prior** as Bayesian prior ([LM-prior cold start](https://arxiv.org/html/2411.09065v1)). Give cold tracks an exploration bonus so the bandit surfaces them.

---

## 7. How the majors actually do it (public)

- **Spotify (BaRT):** MF/Word2Vec CF + audio (CNN) + NLP, retrieved via ANN (**Annoy → now Voyager/hnswlib** ([Voyager](https://engineering.atspotify.com/2023/10/introducing-voyager-spotifys-new-nearest-neighbor-search-library)), contextual-bandit Home ([Bernhardsson](https://erikbern.com/2015/09/24/nearest-neighbor-methods-vector-models-part-1.html)).
- **YouTube Music:** two-stage two-tower retrieval → heavy ranker ([guide](https://www.music-tomorrow.com/blog/a-complete-guide-to-youtube-recommendation-algorithms-for-music-and-artists)).
- **Pandora:** Music Genome (450 attrs) + CF + editorial hybrid.
- **Yandex "My Wave":** real-time neural audio (spectrogram/timbre/rhythm) + CF + context (>1000 factors); released **Yambda, 5B-event open dataset** ([Yandex](https://yandex.com/company/news/28-05-2025)) — directly usable to bootstrap CIS-market models.
- **Apple Music:** more editorial/curation-led, less public ML detail.

---

## 8. Pitfalls

- **Don't start neural.** ALS/Word2Vec-CF + musicnn + ε-greedy ships and is debuggable; SASRec/two-tower/Thompson come after data exists.
- **Popularity bias / filter bubble** — without an explore quota the flow collapses to hits; bake an exploration floor into candidate gen.
- **Skip ≠ dislike** (could be context); use graded, decaying rewards, not hard bans.
- **Explanation honesty** — the "why" must derive from the *actual* retrieval reason, or users lose trust fast. Log it as a bandit arm; never post-hoc fabricate.
- **Steer must be reversible & visible** in the Twinr UI, else it feels like a black box — undermining the whole pitch.
- **Latency:** re-rank per-skip must be <~100ms — keep the per-event model light (sequence re-ranker), heavy work offline.
- **CLAP licensing/compute** — validate the chosen checkpoint's license and GPU cost before committing it as the spine.

---

### Concrete target architecture for Город ФМ
1. **Item store:** every track = `[CF vec ⊕ CLAP vec ⊕ metadata]`, indexed in ANN (hnswlib/Voyager).
2. **Twinr profile:** long-term EMA vector (visible) + short-term session state + context features, all in shared embedding space.
3. **Retrieval:** ANN over blend of long-term + short-term intent + an **explore quota**.
4. **Ranker:** SASRec-style session model re-scoring after every skip/complete on graded reward.
5. **Selection/explain:** contextual bandit (ε-greedy→Thompson) choosing **(track, why-string)**; reason taken from the real retrieval cause.
6. **Steer:** NL → LLM → CLAP text vector → live shift of intent vector; persist if repeated; surface the change in the Twinr UI.
