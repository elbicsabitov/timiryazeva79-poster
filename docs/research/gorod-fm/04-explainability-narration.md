# Город ФМ — Explainable Recommendations & Factual Music Narration

**Topic:** How to generate trustworthy "why this song" explanations and factual, LLM-narrated music-history tours.
**Audience:** Founder + eng lead. **Date:** 2026-06-02.
**Bottom line:** Treat the explanation/narration layer as **retrieval-first, LLM-last**. The recommender and a music **knowledge base** decide *what is true*; the LLM only *phrases* it. Never let the LLM choose facts (influences, dates, lineage) on its own — that is where the product dies on trust.

---

## 1. Techniques to explain "why this track"

There is no single best explanation; pick the style per context. Five families, all production-proven:

1. **Feature/attribute-based** — surface the audio/metadata attributes the recsys actually used: tempo, key, energy/valence, genre, era, mood. Cheapest, always available, and the backbone of "why" chips. Source the attributes from AcousticBrainz/Essentia low-level + rhythm + tonal descriptors (https://mtg.github.io/acousticbrainz-genre-dataset/data/).
2. **Collaborative ("because you liked X")** — "Recommended because you played *Shape of You*." Classic, intuitive, and the single most validated style: showing the user the items in their own history that drove the rec increases satisfaction (https://arxiv.org/pdf/2203.01310). Requires logging the nearest-neighbour / co-listen evidence at serve time.
3. **Knowledge-graph PATH explanations** — the differentiator for an "AI-driven" radio. A KG lets you extract a literal reasoning path: `user → liked → "I See Fire" → sung_by → Ed Sheeran → sang → "Shape of You"`. Models: **KPRN** (weighted path pooling, demonstrated on music, https://arxiv.org/abs/1811.04540) and **PGPR / Policy-Guided Path Reasoning** (RL agent that *finds* the path and recommends along it; SIGIR'19; code at https://github.com/orcax/PGPR; paper https://arxiv.org/abs/1906.05237). Also **KGAT** (KDD'19, attention over the KG). Path quality should be optimized for **recency, popularity, diversity** — explaining via the *last* track the user played makes the session feel "understood" (https://www.sciencedirect.com/science/article/abs/pii/S0950705122011947).
4. **Counterfactual ("you'd see something else if…")** — "We picked this *because* you've been on a synth-pop streak; skip three and it changes." Frameworks: **ACCENT** and the WWW'24 counterfactual framework (https://dl.acm.org/doi/10.1145/3589334.3645560; eval CEERS https://dl.acm.org/doi/10.1145/3640457.3688015). High trust value, higher engineering cost — make it a v2 "why did the mood shift?" feature, not v1.
5. **LLM-generated rationales GROUNDED in the above** — the LLM does **not** decide *why*; it receives the structured evidence (the chosen KG path + attribute deltas + co-listen items) and renders it as natural language. This is exactly the direction Spotify productionized in 2025 ("Semantic IDs" + LLM explanations grounded in the listener's own history; https://research.atspotify.com/2025/11/teaching-large-language-models-to-speak-spotify-how-semantic-ids-enable and https://research.atspotify.com/2025/9/beyond-the-next-track-spotify-research-at-recsys-2025).

**Recommendation:** Ship **chips = attribute + collaborative** at launch (always true, cheap). Add **KG path** rationales as the signature "explainable autoplay." Render all of it through a constrained LLM. Counterfactual is v2.

---

## 2. Hallucination risk — keeping explanations and history TRUE

This is the existential risk: an LLM will confidently invent influences, wrong release years, fake "X mentored Y" relationships. Mitigations, in order of importance:

- **RAG grounded on a music knowledge base.** Every fact in an explanation or tour must trace to a retrieved record (KG triple or catalog row). LLM-only sentences are frequently ungrounded even when they happen to be correct (https://arxiv.org/pdf/2404.07060) — so *forbid* free-form factual claims. Pattern = Knowledge-Graph-RAG for recommendation (https://arxiv.org/pdf/2501.02226).
- **Closed-world prompting.** System prompt: "Use ONLY the facts in CONTEXT. If a fact (date, influence, label) is not present, do not state it. Never infer relationships." Pass IDs, not prose, as context.
- **Automated faithfulness gate before display.** Decompose the generated text into atomic claims → run NLI entailment (DeBERTa / RoBERTa-MNLI, or LLM-as-judge) against the retrieved context → drop or regenerate any non-entailed sentence. This yields a 0–1 faithfulness score usable as a hard pre-publish gate plus a continuous regression signal (https://arxiv.org/pdf/2305.18029; tooling pattern https://123ofai.com/qnalab/system-design/blocks/faithfulness; RAGAS-style metrics https://deepchecks.com/rag-evaluation-metrics-answer-relevancy-faithfulness-accuracy/).
- **Cite-or-suppress.** Each tour sentence carries the source entity ID behind the scenes; if a sentence has no source, it does not ship.
- **Template the spine, LLM only the connective tissue.** For dates/years/genre labels, render from the DB directly (string interpolation), not from the model. Let the LLM only write transitions and color.

---

## 3. Music knowledge graphs & datasets for lineage / influence / era

| Source | Has | Quality / caveat |
|---|---|---|
| **MusicBrainz** | artists, releases, recordings, works, labels + rich typed relationships; stable MBIDs | The backbone identity layer. Members/bands, "performs", "founder", collaboration edges are good; explicit *artistic influence* edges are weak. Docs: https://musicbrainz.org/doc/MusicBrainz_Database |
| **Wikidata** | `P737 influenced by`, `P136 genre`, dates, places, `P279` subclass for genre hierarchies; links to MBIDs | **CRITICAL PITFALL: P737 is sparse and subjective.** Only ~31.5k statements *across all domains* (philosophy, science, art, code), citation-needed constraint, and explicitly flagged "sparse or subjective" for musicians; the inverse "influences" property was deleted (https://www.wikidata.org/wiki/Property_talk:P737). **Do not build a core lineage feature assuming dense, reliable P737 coverage for pop/rock artists.** |
| **DBpedia** | `dbo:influencedBy`, `dbo:genre`; SPARQL endpoint | Different ontology than Wikidata; complementary influence text mined from Wikipedia infoboxes. Useful to *cross-fill* P737 gaps but equally subjective. |
| **AllMusic / Discogs** | editorial genre/subgenre taxonomies, "influenced by / followers of / similar artists", styles, eras | Expert-curated → the best *editorial* influence/era signal, but licensing/ToS constrain bulk use. AllMusic + Discogs taxonomies are already aligned in the **AcousticBrainz Genre Dataset** (4 sources, 2M+ recordings; https://archives.ismir.net/ismir2019/paper/000042.pdf). |
| **AcousticBrainz** | audio features (Essentia: low-level, rhythm, tonal) keyed by MBID | The *sonic* "why" (tempo/key/energy/timbre). Note: AcousticBrainz stopped collecting new submissions, but the dump is rich and stable. |
| **Ishkur's Guide v4 (IGTEM26)** | 251 electronic genres, 502 typed influence/evolution connections, 11,493 representative tracks, phylogenetic-tree layout | A ready-made, human-curated *genre lineage graph* — excellent reference structure and a seed for genre-evolution tours (https://github.com/eskoNBG/IGTEM26). Genealogy of musical genres on Wikipedia is a lighter alt. |

**Recommendation — build "Город KG":** MBID as the primary key; ingest MusicBrainz relationships (identity, membership, collaboration) + Wikidata/DBpedia (genre hierarchy via `P136`/`P279`, dates, *available* influence edges) + AcousticBrainz features. **Treat artist-level "influence" edges as a curated, sparse, reviewed layer** — seed from Wikidata/DBpedia/AllMusic, then *human-verify the top ~1–2k artists you actually serve*. Genre-level lineage (denser, more objective) carries more of the narration than artist-level influence.

---

## 4. Building narrated "music history tours"

Goal: e.g. "the lineage leading to Imagine Dragons" — narrate *and* play the tracks. Architecture:

1. **Plan from the KG, not the LLM.** Given target artist → walk the KG backward along genre-lineage + influence edges to assemble an ordered chain of nodes (eras/genres/anchor artists). This guarantees the *skeleton* is factual. Ishkur-style genre evolution edges and Wikidata genre subclass paths are ideal for ordering.
2. **Bind a track to each node** from the owned/licensed catalog (representative track per genre/era). The KG gives the *story*; the catalog gives the *playlist*.
3. **Retrieve facts per node** (year, origin, why it mattered, link to next node) as structured records.
4. **LLM narrates per segment** with the closed-world prompt — it writes ~2–4 sentences of transition using ONLY the retrieved record, then hands to playback. This is the "host" voice between tracks.
5. **Faithfulness gate each segment** (§2) before it is spoken/shown.
6. **Mix mode:** KG = spine and facts; LLM = voice, pacing, and the "why you'll like the next one" personalization hook tied back to the user's Twinr profile.

Conversational companion = same pipeline behind a chat turn: intent → KG subgraph retrieval → grounded generation → faithfulness check.

---

## 5. UX of explanations — trust & transparency

- **Two altitudes.** (a) Always-on **"why" chip** under autoplay — 3–6 words, one reason, from attribute+collaborative signal ("Because you played *Radioactive* · same energy, darker key"). (b) **Expandable narrative** on tap — the KG path rendered as a sentence, plus an optional full tour. Do not lead with the long form; progressive disclosure preserves flow.
- **Map explanation to a goal, and pick the metric to match.** Tintarev & Masthoff's seven aims — *transparency, scrutability, trust, effectiveness, persuasiveness, efficiency, satisfaction* — are partly **incompatible** (e.g. persuasiveness can hurt effectiveness), so each surface should optimize one declared aim (https://link.springer.com/article/10.1007/s11257-011-9117-5). Город's "why" chip = **transparency + satisfaction**; the taste editor = **scrutability** (let users *correct* the stated reason → steers the Twinr profile).
- **Steerability is the trust loop.** Showing the reason *and* letting the user reject it ("not because of this") is the highest-trust pattern and feeds taste-steering — aligns with Spotify's 2025 "transparent and steerable" direction (https://research.atspotify.com/2025/9/beyond-the-next-track-spotify-research-at-recsys-2025).
- **Honesty constraint:** the explanation must reflect the *actual* signal that drove the rec (post-hoc fabricated rationales erode trust once users catch a mismatch). This is why the LLM must render the real KG path/co-listen evidence, not a plausible story.

---

## Pitfalls (read before building)

1. **P737 sparsity (biggest trap).** Do **not** assume dense, reliable artist-influence edges from Wikidata — ~31.5k statements total across all human knowledge, flagged subjective for musicians. Curate a reviewed influence layer for your served artists; lean on *genre* lineage (denser, more objective) for the rest.
2. **LLM picking facts = hallucinated history.** Wrong years/influences are unforgivable in a product whose pitch is "explainable & factual." Enforce closed-world prompting + NLI faithfulness gate + cite-or-suppress.
3. **Post-hoc rationalization mismatch.** If the chip says one thing but the recsys did another, power users will notice. Generate from the real serving-time evidence.
4. **Licensing.** AllMusic/Discogs influence data and track audio have ToS/licensing limits — design the KG ingest around what you can legally store/serve; MusicBrainz/Wikidata are open (CC0-ish), AcousticBrainz dump is available but frozen.
5. **Subjectivity of "influence."** Even curated, influence is contestable. Hedge phrasing ("often cited as an influence") and keep an editorial review queue.
6. **Latency.** Path reasoning + retrieval + NLI per track can be slow. Precompute explanations/paths offline for top catalog, cache, and gate asynchronously; only do live generation for the conversational tour.

## Suggested architecture (one line)
`Recommender (+KG path reasoner: PGPR/KPRN) → Evidence bundle (path + attribute deltas + co-listen + retrieved facts by MBID) → Constrained LLM renderer (closed-world) → NLI faithfulness gate (cite-or-suppress) → chip / narrative / spoken tour`, all over a **MBID-keyed "Город KG"** (MusicBrainz + Wikidata/DBpedia + AcousticBrainz + curated influence layer).
