# Город ФМ — End-to-End System Architecture & MLOps

**Topic:** Real-time AI music-streaming / smart-radio backend. Differentiators: explainable autoplay, steerable taste, near-real-time "Twinr" profile, conversational companion, taste-based ads.
**Audience:** Founder + eng lead choosing the build. **Bias:** startup budget, ship-an-MVP-first.

---

## 0. The brutal constraint first: LICENSING (read this before any code)

**You cannot legally stream a major-label catalog by scraping/hosting MP3s. Full stop.** Streaming any commercial recording triggers **two separate rights**, owed to two separate groups:

1. **Master/sound-recording rights** → record labels (Universal, Sony, Warner + indies). Paid per-stream.
2. **Composition rights** (the song itself) → publishers + songwriters, collected as **mechanical** and **performance** royalties. In the US the **MLC** administers a blanket mechanical license; the reporting burden is "stringent" and a "common mistake for new DSPs is underestimating the administrative burden of mechanical royalties." ([themlc.com](https://www.themlc.com/), [developers.dev](https://www.developers.dev/tech-talk/impact-of-music-licensing-in-streaming-app.html))

Direct deals with all three majors require minimum guarantees (often **six–seven figures advances + per-stream minima**) and are not available to a pre-revenue startup. Time-to-market for a globally compliant MVP slips **3–5 months** if licensing+data architecture isn't settled before the build. ([developers.dev](https://www.developers.dev/tech-talk/impact-of-music-licensing-in-streaming-app.html))

### The three realistic paths for Город ФМ

| Path | What it is | Pro | Con | Verdict for Город ФМ |
|---|---|---|---|---|
| **A. Music-as-a-Service aggregator (7digital / MassiveMusic)** | A B2B provider holds the label deals; you get a **licensed catalog API + audio delivery + royalty reporting**, pay per-stream/wholesale. 7digital = **150M tracks, 300+ labels, ingests 800k releases/week**, "compliant delivery at any scale." | Real catalog, real streams, **rights handled for you**, royalty reporting built-in. Fastest legal route to a true streaming product. | Wholesale cost per stream; still need your own min-commit; integration work. | **Primary recommendation for the real product.** This is how non-major-funded "radio" services launch legally. ([7digital](https://www.7digital.com/music-as-a-service-platform/), [massivemusic.com](https://massivemusic.com/services/platform-music-delivery-services/api-music-delivery)) |
| **B. Playback-SDK wrapper (Spotify Web Playback SDK / YouTube)** | You build the *experience* (explainable autoplay, Twinr, chat); **audio + rights stay with Spotify/YouTube**; user logs in with their own Premium account. | Zero licensing/royalty liability — it's their stream. Cheapest legal MVP. | **Spotify forbids commercial use without written approval; >95% of extended-API apps are rejected; access tightened May 2025.** You're a guest on their platform and can be cut off. Can't do taste-based audio ads. | **Good for a demo / wedge, dangerous as the business.** Use to validate UX, not to scale. ([developer.spotify.com SDK](https://developer.spotify.com/documentation/web-playback-sdk), [Spotify API access criteria](https://developer.spotify.com/blog/2025-04-15-updating-the-criteria-for-web-api-extended-access)) |
| **C. Indie / Creative-Commons / direct-distributor catalog** | License via distributors (TuneCore, ONErpm, Zvonko, MusicDiffusion) or CC/royalty-free pools; do **direct deals with local KZ/CIS artists**. | You own the relationship + the rights terms; differentiated local catalog; cheap. | No Taylor Swift. Smaller catalog → must win on curation + local identity. | **Use to seed an owned KZ/CIS catalog** alongside Path A. Strong fit for a Kazakhstan-first identity. ([tunecore.com](https://www.tunecore.com/), [zvonkodigital.com](https://zvonkodigital.com/en)) |

### Kazakhstan / CIS specifics (a real risk, not a footnote)

- **KZ collective-rights management is weak and under international scrutiny.** Nov 2025: CISAC, IFPI, IFRRO, IAF, IMPF sent an open letter to President Tokayev about "weaknesses in the country's system of collective rights management." Translation: **you cannot rely on a clean local CMO blanket license** the way you could in the EU. Get a Kazakhstani IP lawyer; budget for direct/aggregator deals. ([creativeindustriesnews.com](https://creativeindustriesnews.com/2025/11/music-sector-urges-kazakhstan-to-address-the-weaknesses-in-the-countrys-system-of-collective-rights-management/))
- **Yandex Music is the proof of the model in-region:** ~3.5M licensed recordings, operating legally across KZ + CIS via local + international rightsholder deals. ([Yandex Music — Wikipedia](https://en.wikipedia.org/wiki/Yandex_Music))

**De-risking the licensing constraint:**
1. **MVP = Path B (Spotify SDK) for the UX demo + Path C owned-KZ catalog you can legally stream end-to-end.** Prove explainable autoplay + Twinr + chat on *real audio you control* without label exposure.
2. **In parallel, open a 7digital / MassiveMusic (Path A) conversation early** — their integration + your min-commit is the long pole. Treat it as a fundraising milestone ("we have the license path").
3. **Engage KZ IP counsel before public launch.** Never assume a local CMO covers you.

---

## 1. Reference architecture (the real service)

```
                    ┌─────────────── CLIENT (web / mobile) ───────────────┐
                    │  player · bubble onboarding · chat · "why this?"     │
                    └───────┬───────────────────────────────┬─────────────┘
        plays/skips/dwell   │                               │ chat / NL steer
                            ▼                               ▼
                 ┌──────────────────┐            ┌──────────────────────────┐
                 │  EVENT GATEWAY   │            │   LLM ORCHESTRATOR        │
                 │  (HTTP→Redpanda) │            │  (gateway: route/cache/   │
                 └────────┬─────────┘            │   guardrails)             │
                          ▼                      └───────────┬───────────────┘
              ┌───────────────────────┐                     │ reads profile + track meta
              │  STREAM PROC (Flink)  │                     ▼
              │  sessionize · dwell · │       ┌──────────────────────────────┐
              │  near-real-time Twinr │       │  RECO SERVING (gRPC, <100ms) │
              └─────┬───────────┬─────┘       │  ① candidate-gen (ANN)       │
                    │           │             │  ② ranker (GBDT/light NN)    │
        offline ▼              ▼ online       │  ③ business rules / explain  │
   ┌──────────────────┐  ┌──────────────────┐ └───────┬──────────────┬───────┘
   │  FEATURE STORE   │  │  ONLINE STORE    │◄────────┘              │
   │  (Feast offline) │  │  (Redis: profile,│                       ▼
   │  warehouse/S3    │  │   features)      │            ┌──────────────────────┐
   └──────────────────┘  └──────────────────┘            │ VECTOR STORE         │
            ▲                                             │ (track + user embeds)│
            │ nightly batch train (two-tower, ranker)     │ Qdrant / pgvector    │
            └─────────────────────────────────────────────┴──────────────────────┘
   AUDIO: 7digital/Spotify-SDK/owned-CDN  |  OBSERVABILITY: OTel→Grafana  |  EXPERIMENTS: GrowthBook
```

### 1a. Event streaming & near-real-time Twinr profile
- **Bus: Redpanda** (Kafka-API-compatible, single binary, no JVM/ZooKeeper) for a small team. Move to managed **Kafka 4.0 (KRaft)** or **Confluent/MSK** only when ops demand it. **Kinesis** is fine if you're all-in on AWS and want zero ops. ([Conduktor: streaming reco](https://www.conduktor.io/glossary/building-recommendation-systems-with-streaming-data), [Kai Waehner](https://www.kai-waehner.de/blog/2025/02/23/online-model-training-and-model-drift-in-machine-learning-with-apache-kafka-and-flink/))
- **Processor: Apache Flink** for sessionization, dwell-time aggregation, and updating the Twinr embedding in the online store. Flink does point-in-time enrichment to avoid **train/inference skew**. ([Conduktor: streaming reco](https://www.conduktor.io/glossary/building-recommendation-systems-with-streaming-data))
- **Freshness target:** a skip/like should shift the next-track candidate set within **seconds**, not a nightly batch. That's the whole "Twinr updates in near-real-time" promise — implement it as an **online embedding nudge** (EWMA of last-N track vectors + bandit exploration), not a model retrain.

### 1b. Feature store + vector/embedding store
- **Feature store: Feast** (open-source, free) — offline (S3/warehouse) for training, **online = Redis** for <10ms reads. Tecton/Hopsworks are excellent but overkill/overpriced at MVP. ([Conduktor: feature stores](https://conduktor.io/glossary/feature-stores-for-machine-learning), [devgenius](https://blog.devgenius.io/feature-store-architecture-1324eff5a573))
- **Vector store — startup-scale tradeoff (named, opinionated):**
  - **Start: `pgvector`** if you already run Postgres and have **<10M track vectors** — "add pgvector before adding a new database." One less system to operate.
  - **Grow: Qdrant** — Rust, easiest dedicated vector DB to self-host, great small/mid latency + strong metadata filtering (genre/lang/region). Note it **degrades at very large scale** (~41 QPS @50M vs pgvectorscale ~471 QPS), but a KZ-first catalog won't hit that soon.
  - **Milvus** only at distributed scale (50–100M+ vectors). **FAISS/Voyager** as an *embedded library* inside the candidate-gen service for raw speed, not as your system-of-record (no native CRUD/HA). ([vector DB comparison](https://medium.com/@elisheba.t.anderson/choosing-the-right-vector-database-opensearch-vs-pinecone-vs-qdrant-vs-weaviate-vs-milvus-vs-037343926d7e), [Tiger Data pgvector vs Qdrant](https://www.tigerdata.com/blog/pgvector-vs-qdrant))
  - **Migrate trigger:** ~50–100M vectors **or** $500+/mo managed spend.

### 1c. Serving: candidate-gen → ranking, <~100ms
Copy the proven Spotify shape: **two-tower model** maps users + tracks into one vector space; **ANN search** retrieves candidates without running heavy ML at request time. Spotify built **Annoy** (2013) → now **Voyager (HNSW, ~10× faster)** for exactly this. ([Spotify Voyager](https://engineering.atspotify.com/2023/10/introducing-voyager-spotifys-new-nearest-neighbor-search-library), [Two-Tower deep-dive](https://www.shaped.ai/blog/the-two-tower-model-for-recommendation-systems-a-deep-dive))
- **① Candidate-gen:** ANN top-500 from Qdrant/HNSW on the Twinr vector (~5–15ms).
- **② Ranker:** lightweight **GBDT (LightGBM/XGBoost)** or small NN over Feast online features — fast, cheap, debuggable. Keep the heavy model offline; serve the cheap one. ([Databricks online reco](https://www.databricks.com/blog/guide-to-building-online-recommendation-system))
- **③ Rules + explainability:** dedup/recency/diversity, then **derive the "why this?" string from ranker feature attributions** (top SHAP-like signals → "because you've been playing dream-pop and skipped high-tempo tracks"). The explanation is a by-product of ranking, not a second LLM call.
- **Latency budget:** precompute next-track during the *current* track (you have ~3 min); cache the upcoming queue in Redis so the actual "next" is a sub-ms lookup. **<100ms is trivial when you decide ahead of playback.** ([appitsoftware real-time reco](https://www.appitsoftware.com/blog/building-real-time-recommendation-engines-retail-ai-architecture))

### 1d. LLM orchestration (chat / explanations / steering)
- **Put a gateway in front** (LiteLLM / Bifrost-style) for **routing + semantic caching + budget caps + guardrails** from one place. ([Maxim cost/latency](https://www.getmaxim.ai/articles/reduce-llm-cost-and-latency-a-comprehensive-guide-for-2026/), [Redis LLMOps](https://redis.io/blog/large-language-model-operations-guide/))
- **Small-vs-large routing:** small/fast model (Haiku-class / Llama-8B) for "explain this track," intent parsing of NL steering, and simple chat; large model only for genuinely open-ended companion conversation. Routing "can match or exceed single-model quality while cutting average cost." ([Maxim 5 ways](https://www.getmaxim.ai/articles/5-ways-to-optimize-costs-and-latency-in-llm-powered-applications/))
- **Caching is the budget:** prefix/prompt caching = **~90% cost / ~85% latency** reduction on long prompts; **31% of queries are semantically similar** → semantic cache for repeated "why this song?" explanations. ([Introl prompt caching](https://introl.com/blog/prompt-caching-infrastructure-llm-cost-latency-reduction-guide-2025), [Maxim semantic caching](https://www.getmaxim.ai/articles/how-to-optimize-llm-cost-and-latency-with-semantic-caching/))
- **Steering = structured output, not vibes:** the LLM parses "more upbeat, less sad" into **structured deltas** (tempo↑, valence↑, genre filter) applied to the Twinr vector / ranker — the LLM never picks tracks directly. Keeps it cheap, fast, debuggable, and on-catalog (a guardrail against hallucinated songs you don't have rights to).
- **Guardrails:** schema-validate every LLM output; constrain recommendations to in-catalog IDs; rate-limit + budget-cap per user at the gateway.

### 1e. Online vs batch learning (profile freshness)
**Hybrid — the 2025 industry default.** Batch (nightly) retrains two-tower + ranker for a stable baseline; a **nearline/online layer** (contextual bandit, e.g. "Online Matching"-style closed loop) handles immediate adaptation + exploration of new tracks/tastes. Pure-online at scale is still hard, so don't over-invest early. ([Online Matching bandit](https://arxiv.org/abs/2307.15893), [batch vs online](https://medium.com/@aakriti_saxena/batch-machine-learning-offline-vs-online-learning-2c663516f208), [Kai Waehner online training](https://www.kai-waehner.de/blog/2025/02/23/online-model-training-and-model-drift-in-machine-learning-with-apache-kafka-and-flink/))

### 1f. Privacy / GDPR, observability, A/B
- **Taste data is profiling under GDPR.** Run **content personalization on legitimate interest** (with an LIA + opt-out), but **taste-based *advertising* needs explicit consent**. Anonymize where possible; keep EU data handling clean; honor deletion (feeds back to "delete my Twinr"). Note CJEU C-621/22 + EDPB Guidelines 1/2024 tightened legitimate-interest interpretation. ([IAPP legal basis](https://iapp.org/news/a/data-analytics-on-online-services-under-gdpr-legal-basis-for-processing), [Osborne Clarke profiling](https://www.osborneclarke.com/insights/profiling-and-automated-decision-making-under-gdpr), [Usercentrics LI](https://usercentrics.com/knowledge-hub/gdpr-legitimate-interest/))
- **A/B: GrowthBook** (open-source, **server-side** evaluation = cleanest GDPR posture, avoids consent-gated cookies). Every reco/explanation change ships behind a flag. ([DRIP GDPR A/B](https://dripagency.de/blog/ab-testing-tools-gdpr-compliant))
- **Observability: OpenTelemetry → Grafana/Prometheus** for service + model latency; log ranker feature snapshots for explainability audits and offline replay.

---

## 2. Pragmatic MVP → scale path

**Phase 0 — Demo (weeks, ~1–2 devs):** Spotify Web Playback SDK (Path B) **+ owned KZ/CC tracks (Path C)** you can stream end-to-end. Postgres + **pgvector**, precomputed track embeddings, a GBDT ranker, Redis queue cache, one small LLM behind a gateway for "why this?" + NL steering. Bubble onboarding seeds the first Twinr vector. **Goal: prove explainable autoplay + steering + Twinr feel magic.** No Kafka yet — write events straight to Postgres/Redis.

**Phase 1 — Real-time loop:** Add **Redpanda + Flink** for live skip/dwell → near-real-time Twinr nudges + bandit exploration. **Feast** formalizes features. **GrowthBook** for A/B. **OTel** observability. Begin **7digital/MassiveMusic (Path A)** integration + KZ legal counsel — the licensing long pole.

**Phase 2 — Licensed scale:** Go live on the aggregator catalog (real per-stream royalties + reporting). Migrate vectors **pgvector → Qdrant**. Nightly two-tower retrain + nearline bandit. Taste-based ads **only after explicit-consent flow** is in place.

**Hardest constraints, ranked:** (1) **licensing** — solve via aggregator + owned-KZ catalog, never assume the KZ CMO covers you; (2) **profile freshness** — solve with online embedding nudge, not retrains; (3) **LLM cost** — solve with routing + caching + structured steering; (4) **GDPR on ads** — gate behind explicit consent.

---

### Sources
- 7digital MaaS / catalog & delivery — https://www.7digital.com/music-as-a-service-platform/ , https://www.7digital.com/partner-integration/
- MassiveMusic delivery API — https://massivemusic.com/services/platform-music-delivery-services/api-music-delivery
- Licensing burden / MVP timeline — https://www.developers.dev/tech-talk/impact-of-music-licensing-in-streaming-app.html
- Mechanical Licensing Collective — https://www.themlc.com/ , https://www.themlc.com/digital-music-royalties-landscape
- Spotify Web Playback SDK terms — https://developer.spotify.com/documentation/web-playback-sdk
- Spotify API access tightening (May 2025) — https://developer.spotify.com/blog/2025-04-15-updating-the-criteria-for-web-api-extended-access
- KZ collective-rights weakness (CISAC/IFPI letter, Nov 2025) — https://creativeindustriesnews.com/2025/11/music-sector-urges-kazakhstan-to-address-the-weaknesses-in-the-countrys-system-of-collective-rights-management/
- Yandex Music (in-region model) — https://en.wikipedia.org/wiki/Yandex_Music
- Indie distributors — https://www.tunecore.com/ , https://zvonkodigital.com/en
- Real-time reco architecture — https://www.conduktor.io/glossary/building-recommendation-systems-with-streaming-data , https://www.appitsoftware.com/blog/building-real-time-recommendation-engines-retail-ai-architecture
- Feature stores — https://conduktor.io/glossary/feature-stores-for-machine-learning , https://blog.devgenius.io/feature-store-architecture-1324eff5a573
- Vector DB tradeoffs — https://medium.com/@elisheba.t.anderson/choosing-the-right-vector-database-opensearch-vs-pinecone-vs-qdrant-vs-weaviate-vs-milvus-vs-037343926d7e , https://www.tigerdata.com/blog/pgvector-vs-qdrant
- Spotify Voyager / ANN — https://engineering.atspotify.com/2023/10/introducing-voyager-spotifys-new-nearest-neighbor-search-library ; Two-tower — https://www.shaped.ai/blog/the-two-tower-model-for-recommendation-systems-a-deep-dive ; Databricks online reco — https://www.databricks.com/blog/guide-to-building-online-recommendation-system
- LLM cost/latency/routing/caching — https://www.getmaxim.ai/articles/reduce-llm-cost-and-latency-a-comprehensive-guide-for-2026/ , https://introl.com/blog/prompt-caching-infrastructure-llm-cost-latency-reduction-guide-2025 , https://redis.io/blog/large-language-model-operations-guide/
- Online vs batch / bandits — https://arxiv.org/abs/2307.15893 , https://www.kai-waehner.de/blog/2025/02/23/online-model-training-and-model-drift-in-machine-learning-with-apache-kafka-and-flink/
- GDPR profiling / legal basis / A/B — https://iapp.org/news/a/data-analytics-on-online-services-under-gdpr-legal-basis-for-processing , https://www.osborneclarke.com/insights/profiling-and-automated-decision-making-under-gdpr , https://dripagency.de/blog/ab-testing-tools-gdpr-compliant
