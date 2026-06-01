# Город ФМ — Visual, Motion & Sonic Identity for an Immersive AI Audio Platform

**Topic:** A premium, distinctive, immersive visual/motion language where the AI ("Twinr") feels like a living presence — not generic-AI-slop.
**Audience:** Founder + designer/eng lead. **Date:** 2026-06-02.
**Constraints kept:** dark-first, Onest, blue `#5168FC`, glassmorphism.
**Bottom line:** Build the identity around **one living signal** — a single audio-reactive "radio wave" that *is* Twinr — rendered with restraint (one accent, deep neutral darks, real motion tied to the real audio). The premium signal is **coherence + responsiveness**, not effects. Kill the two slop tells up front: aggressive multi-stop gradients and decorative glow that doesn't react to anything.

---

## 1. What reads "premium" vs "generic-AI-slop" in dark audio UIs

The slop look is now a documented default: models regress to "the average of their training data — indigo gradients and rounded corners," amplified by generic prompts like "clean modern minimalist" (https://axe-web.com/insights/ai-website-design-sameness/, https://www.vandelaydesign.com/why-ai-generated-designs-look-the-same/). Premium dark audio brands move the opposite way — **reductive, not additive**. Sonos reduces "elements to their purest form," uses near-monochrome + one vivid accent, and lets *artwork* be the color ("putting the music first," https://medium.com/@m.dujardin/sonos-app-redesign-ux-ui-case-study-e174f748c804, https://docs.sonos.com/docs/seg-principles). NTS Radio is austere editorial: fixed grid, mono type, near-zero chrome — the *content* is the texture (https://catowens.com/NTS-Radio, https://www.nts.live/).

**Anti-slop rules for Город ФМ:**
- **One accent only.** `#5168FC` is the single hero hue. No teal→magenta→orange ramps. Gradients allowed *only* as a tight 2-stop tonal shift within the blue family (e.g. `#5168FC → #3A48C9`) for the Twinr surface, never as a page background.
- **Neutral, not blue-black, darks.** Use a desaturated near-black (`#0B0C0F`/`#121419`) so the blue actually pops; flooding the canvas with saturated blue-purple is the slop tell.
- **Let cover art be the color.** Like Sonos/Apple Music, the album/track artwork supplies hue; the UI stays neutral so it never competes (Apple Music album-motion guidance keeps focus locked on the cover, https://help.apple.com/itc/albummotionguide/en.lproj/static.html).
- **Glow must be earned.** Bloom/aura only where it represents *live audio or live AI*. Static decorative glow = slop.

---

## 2. Twinr as an AI PRESENCE — a living thing, not an avatar

The market has converged on **ambient, faceless presence** — and crucially, away from the bounded floating orb. Apple replaced Siri's orb with an **edge-of-screen glow that follows your voice** while you keep using the device — the assistant becomes *part of the OS*, not a popup (https://applemagazine.com/siri-glow-001/, https://www.pocket-lint.com/how-to-get-new-siri-look-glowing-border/). OpenAI likewise dissolved the full-screen blue orb *into* the chat stream — "ambient computing companion" rather than overlay (https://modernengineeringmarvels.com/2025/11/27/chatgpt-voice-mode-now-blends-seamlessly-with-text-chat/, https://www.webpronews.com/the-death-of-the-overlay-how-openais-integrated-voice-mode-signals-the-end-of-static-computing/). Reference vocabulary: Siri edge-glow, Alexa light-ring, the ChatGPT breathing blob (https://smoothui.dev/docs/components/siri-orb).

**Direction:** Twinr is **the wave itself** — a continuous audio-reactive line/field that lives at a fixed home (now-playing) and can **migrate to a screen-edge aura** when Twinr "speaks" (explains a pick, narrates a tour). Four expressive states from one primitive:
- **Idle** — slow ambient breathing (≈0.1 Hz), low amplitude, ~40% opacity. Alive but calm.
- **Listening/Playing** — the wave deforms to the *actual* track audio (§4).
- **Thinking** — amplitude collapses to a tight pulsing core; motion turns inward (the "considering" beat).
- **Speaking** — wave detaches into an **edge aura** + caption, mirroring Siri. Never a face, never an avatar — Twinr is felt, not anthropomorphized.

---

## 3. Audio-reactive / generative visuals — when they elevate vs distract

These elevate when **tied to the real signal and used sparingly**; they distract when they're ambient decoration fighting the content. The proof points: Spotify Canvas (3–8s loops in now-playing) drives **+145% shares, +20% playlist adds, +9% profile visits** — *because* the motion has "no clear start or end" (slow zooms, liquid, particles) and is engaging-but-not-distracting (https://artists.spotify.com/canvas, https://support.spotify.com/us/artists/article/canvas-guidelines/, https://imusician.pro/en/resources/guides/spotify-canvas). Endel pairs every soundscape with a **signature generative visual** that reacts to context (time, motion, heart rate) to induce a state — visuals *serve* the audio, never showboat (https://endel.io/technology, https://endel.io/soundscapes).

**Rules:** (1) Reactivity must map to *this* track, not a canned loop — fakeness is the distraction. (2) Confine the reactive surface to the now-playing hero + the Twinr aura; lists/settings stay still. (3) Honor reduced-motion (§6). (4) One technique, executed well — don't stack waveform + particles + mesh + blob.

**Performance (web):** Use `AnalyserNode` between source and destination; `getByteTimeDomainData()` for the waveform/oscilloscope line, `getByteFrequencyData()` for spectrum bars (https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Visualizations_with_Web_Audio_API). `fftSize` **2048** for the smooth wave, **256** for chunky bars; `frequencyBinCount` = fftSize/2; raise `smoothingTimeConstant` (~0.8) so the line glides instead of jitters. Drive everything from **one `requestAnimationFrame` loop** (never `setInterval`), single canvas/WebGL layer; on mobile/low battery, drop to a CSS-only breathing fallback.

---

## 4. The "wave/radio" as a LIVING motif + motion design

Make the **wave the brand mark** — it doubles as logo, loader, now-playing hero, and Twinr's body, so the identity is one idea expressed everywhere (the Siri-glow lesson: one motif, many surfaces).

- **Now-playing transition:** artwork blooms up while the wave "ignites" from a flat idle line into full audio-reactive deformation — a clear "the station is live" moment.
- **The wave as host:** between tracks, the wave *speaks* explanations — amplitude ducks under a caption, color shifts a half-step within the blue family, mirroring a human DJ handing off (ties to the explainability layer in `04-explainability-narration.md`).
- **Micro-interactions:** like/skip send a ripple *through* the wave (the wave reacts to the user, like Siri's edge-glow tracks the voice) — feedback lives in the living thing, not in a toast.
- **Canvas-style backdrops:** when artists provide motion art (Apple Music format, https://artists.apple.com/support/5544-create-motion-artwork) or a Canvas-like loop, let it play *behind* a darkened scrim so the neutral UI and the wave still read on top.

---

## 5. Color & type for a premium audio brand + locality without kitsch

- **Type:** Keep **Onest** — geometric, neutral, modern; pair with a *single* expressive display cut (Onest's heaviest weight, very tight tracking) for hero/station moments so it doesn't read as default sans. NTS proves disciplined mono/grid type can carry a whole music identity (https://catowens.com/NTS-Radio).
- **Color:** `#5168FC` as the lone accent over neutral darks; semantic states (success/warn/danger) stay muted so blue owns "Twinr/live." Borrow Okabe-Ito-grade restraint already established elsewhere in this project.

**Locality (Kazakhstan/Central Asia) — distinctiveness, not décor.** The strongest, least-kitsch move is to express **koshkar-muiz (ram's-horn) spiral logic as the *geometry of the wave itself*** — the interlocking spiral means "continuity/infinity," which is precisely what a never-ending personalized radio *is* (https://en.wikipedia.org/wiki/Kazakh_ornaments, https://kalpak-travel.com/blog/introduction-ornaments-central-asia/, https://astanatimes.com/2026/04/what-kazakh-ornaments-reveal-about-nomadic-life-and-nature/). Encode the curl into the wave's resting curve and loader, not as a slapped-on border pattern.
**Guardrail (mandatory):** the CABAR investigation documents global brands stripping these motifs of meaning for commercial gain without attribution or compensation — the appropriation failure mode (https://longreads.cabar.asia/ornaments_en). So: abstract the *structure* (spiral continuity), never lift a literal sacred ornament as wallpaper; if a recognizable pattern is ever used, attribute and contextualize it. Kitsch = literal ornament as skin; premium = the cultural *idea* shaping the motion.

---

## 6. Accessibility — motion, contrast, dark legibility

- **`prefers-reduced-motion`:** ship a real branch — freeze the wave to a static crest, kill auto-loops, disable parallax. Vestibular triggers (nausea/migraine) are severe; this is non-negotiable (https://www.w3.org/WAI/WCAG22/Techniques/css/C39, https://web.dev/learn/accessibility/motion). Also satisfy WCAG **Pause/Stop/Hide** for anything auto-animating >5s, and add an in-app motion toggle, not just the OS query (https://blog.pope.tech/2025/12/08/design-accessible-animation-and-movement/).
- **No flashing >3×/sec** — the audio-reactive wave must clamp peak flicker (https://www.a11y-collective.com/blog/wcag-animation/).
- **Dark legibility:** body text not pure-white-on-pure-black (halation) — use `#E8E9EC` on `#0B0C0F`; meet WCAG AA 4.5:1 for text, 3:1 for UI/icons. The glowing wave is **decorative** — never the sole carrier of state; always pair with text/icon.
- **Combine queries:** respect `prefers-reduced-motion` + `prefers-contrast` + `prefers-color-scheme` together (https://css-tricks.com/almanac/rules/m/media/prefers-reduced-motion/).

---

## 7. Signature moments (build these 3–4)

1. **"Station ignites"** — launch/first-play: idle line snaps into a full audio-reactive wave as artwork blooms. The product's hello.
2. **"Twinr speaks"** — wave ducks → edge-aura + caption explains the pick / narrates a tour, then re-merges into the wave. Siri-glow handoff = the soul.
3. **"You shaped it"** — like/steer sends a visible ripple through the wave + a micro-shift in the visible Twinr taste profile. Steerability made tangible.
4. **"Koshkar wave"** — the resting waveform and loader carry the ram's-horn spiral curl: locality you feel, can't name, never kitsch.

---

## 8. Pitfalls / anti-slop checklist

- ❌ Multi-stop rainbow gradients · purple-blue saturated backgrounds · décor glow that reacts to nothing.
- ❌ A floating bounded orb avatar for Twinr (the market *left* this — go edge-aura/wave).
- ❌ Fake/canned reactivity not bound to the real audio.
- ❌ Literal sacred ornament as wallpaper without attribution (appropriation).
- ❌ Stacking waveform + particles + mesh + blob simultaneously.
- ❌ Pure white on pure black; motion as the only state signal; auto-motion with no reduced-motion branch.
- ✅ One accent · neutral darks · art supplies color · one living wave = Twinr · motion bound to real signal · reduced-motion + AA contrast shipped.

---

### Sources
- AI-slop sameness: https://axe-web.com/insights/ai-website-design-sameness/ · https://www.vandelaydesign.com/why-ai-generated-designs-look-the-same/
- Sonos: https://medium.com/@m.dujardin/sonos-app-redesign-ux-ui-case-study-e174f748c804 · https://docs.sonos.com/docs/seg-principles
- NTS Radio: https://catowens.com/NTS-Radio · https://www.nts.live/
- Siri glow / AI presence: https://applemagazine.com/siri-glow-001/ · https://www.pocket-lint.com/how-to-get-new-siri-look-glowing-border/ · https://smoothui.dev/docs/components/siri-orb
- ChatGPT voice presence: https://modernengineeringmarvels.com/2025/11/27/chatgpt-voice-mode-now-blends-seamlessly-with-text-chat/ · https://www.webpronews.com/the-death-of-the-overlay-how-openais-integrated-voice-mode-signals-the-end-of-static-computing/
- Spotify Canvas: https://artists.spotify.com/canvas · https://support.spotify.com/us/artists/article/canvas-guidelines/ · https://imusician.pro/en/resources/guides/spotify-canvas
- Apple Music motion artwork: https://help.apple.com/itc/albummotionguide/en.lproj/static.html · https://artists.apple.com/support/5544-create-motion-artwork
- Endel generative visuals: https://endel.io/technology · https://endel.io/soundscapes
- Web Audio visualization (API/perf): https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Visualizations_with_Web_Audio_API
- Kazakh ornament / koshkar-muiz: https://en.wikipedia.org/wiki/Kazakh_ornaments · https://kalpak-travel.com/blog/introduction-ornaments-central-asia/ · https://astanatimes.com/2026/04/what-kazakh-ornaments-reveal-about-nomadic-life-and-nature/
- Appropriation guardrail: https://longreads.cabar.asia/ornaments_en
- Accessibility/motion: https://www.w3.org/WAI/WCAG22/Techniques/css/C39 · https://web.dev/learn/accessibility/motion · https://blog.pope.tech/2025/12/08/design-accessible-animation-and-movement/ · https://www.a11y-collective.com/blog/wcag-animation/ · https://css-tricks.com/almanac/rules/m/media/prefers-reduced-motion/
