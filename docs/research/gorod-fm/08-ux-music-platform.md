# Город ФМ — Best-in-Class UI/UX for a Next-Gen Music / Radio Platform

**Topic 08 of the Город ФМ architecture research.** Audience: founder + designer/eng lead.
Scope: the **product surface** — now-playing/player design language, the radio/"wave" metaphor vs library browsing, information architecture, core gestures, cross-surface behavior, and what makes a music app feel premium vs generic. Opinionated; cites named products inline.

> Companion docs: 02 (steering/conversational), 03 (onboarding), 04 (explainability). This doc decides **what the screens look like and what to cut.**

---

## 1. Player / now-playing design language — what's strong, what's tired

**The convergent 2025 grammar** (Spotify, Apple Music, Tidal, Yandex): a near-full-bleed, dark canvas; large album art as the emotional anchor; color extracted *from the cover* to tint the surface; minimal chrome (play/pause, prev/next, scrubber, like, queue, share); micro-animations on play/pause (pulsing wave, animated progress) for perceived liveliness ([rausr.com/blog/the-evolution-of-spotify-design](https://rausr.com/blog/the-evolution-of-spotify-design/)). Spotify's "dark theme that makes album covers pop" is the foundational move; its signature green was re-tuned repeatedly for OLED legibility — a reminder that **a single accent must survive on a dynamic, art-tinted background** (Город ФМ's #5168FC needs the same OLED audit).

**What's strong, steal it:**
- **Art-driven ambient color** (Spotify/Apple): tint the now-playing background from the cover, clamped toward the dark theme so it never blows out contrast.
- **Animated/Canvas covers** (Spotify Canvas): a short looping visual layer per track — "opened a new visual layer for artists" though "controversial… mini-TikToks" ([rausr](https://rausr.com/blog/the-evolution-of-spotify-design/)). For a *radio*, use a calmer generative/ambient motion, not vertical video.
- **Music Haptics** (Apple, iOS 18→): audio translated to taps/textures via the Taptic Engine; began as accessibility, now a premium multi-sensory layer ([thinkdebug.com](https://thinkdebug.com/multi-sensory-apps-designing-with-sound-vibration-and-haptics/), [design.google](https://design.google/library/ux-sound-haptic-material-design)). Cheap to add, disproportionately "premium."
- **Tidal's restraint**: "clean, sophisticated, slick" interface ([macobserver](https://www.macobserver.com/tips/round-ups/apple-music-vs-tidal/)) — proof that *fewer elements, more space* reads as high-end.

**What's tired / avoid:** Apple Music's now-playing "can look cluttered" ([freeyourmusic](https://freeyourmusic.com/blog/apple-music-vs-tidal-sound-quality-music-discovery-cost-compared-2024)); over-stuffed control rows; generic equalizer-bar clichés. Город ФМ's differentiator is **explainability + steering on the player itself** — surfaces nobody else foregrounds — so the player must reserve room for a "**why this is playing**" line and a "**сделай по-другому**" affordance without becoming a control panel.

---

## 2. Radio / "wave" / flow vs library — lean-back vs lean-forward

Город ФМ is a **radio-first** product; the metaphor is the moat. Prior art to mirror:
- **Yandex «Моя волна»**: an infinite, steerable stream with mood/activity/language **dials** and a one-gesture **«Встряхнуть волну»** re-roll ([yandex.com/company/news/28-05-2025](https://yandex.com/company/news/28-05-2025)); 2025 added context-aware AI-sets with smooth neural transitions ([vc.ru](https://vc.ru/services/1247751-obnovlenie-yandeks-muzyki-moya-volna-uchityvaet-kontekst-zanyatiy)). This is the closest reference to Город ФМ — copy the *dials-as-lazy-path + flow-not-list* model.
- **NTS Infinite Mixtapes**: themed, talk-free 100%-music streams with evocative titles ("POOLSIDE", "OTAKU", "SEDATIVE") and an explicit **"LEAN BACK"** category — "designed to counter algorithm culture" ([nts.live](https://www.nts.live/)). Lesson: *name the streams with human/cultural language*, not "Mix 1."
- **Sonos Radio**: "expertly curated stations for mellow mornings, dinner parties" — programming framed as *experiences/occasions* ([sonos.com/.../sonos-radio](https://www.sonos.com/en-us/sonos-radio)).
- **Endel**: real-time adaptive soundscapes from time/weather/location/biometrics — audio that "feels alive and responsive," for people who want background sound "without constant playlist management" ([autonomous.ai](https://www.autonomous.ai/ourblog/endel-app-review), [ixd.pratt](https://ixd.prattsi.org/2026/02/design-critique-endel-ios-app/)). This is the *purest lean-back* archetype — Город ФМ should match its "zero-management" promise.
- **Spotify** is now explicitly nudging toward **lean-back** (Radio, DJ X, Discover Weekly), positioning itself "as your DJ rather than your library"; DJ X takes **voice requests** via tap-and-hold ([newsroom 2025-05-07](https://newsroom.spotify.com/2025-05-07/experience-a-new-dimension-of-music-discovery-with-more-controls-and-enhanced-tools/), [9to5mac](https://9to5mac.com/2025/05/14/dj-spotify-ai-now-takes-requests/)).

**Recommendation — best way to visualize "radio that adapts to you":** make the **flow itself the home screen**, not a grid of playlists. Default state = full-bleed player + a thin, *living* "wave" visualization that visibly reacts when you steer (the wave re-forms on "сделай по-другому" / re-roll). Provide a **lazy path** (3–5 mood/activity/language dials, Yandex-style) and a **precise path** (chat steer, per doc 02) — both editing the *same* stream. The evolving **Twinr** profile is the only "library-like" object users browse; everything else flows.

---

## 3. Information architecture & navigation

**Cautionary tale — Sonos (2024):** the redesign shipped with **5 menu tabs, 3 of which were music-browse** with duplicated functionality; it dropped sleep timer & queue management and wiped ~$500M in value, costing the CEO his job ([rogerwong.me](https://rogerwong.me/2025/02/when-the-music-stopped-inside-the-sonos-app-disaster), [techcrunch](https://techcrunch.com/2024/10/01/sonos-outlines-turnaround-plan-following-app-disaster/), [leaddev](https://leaddev.com/technical-direction/what-went-wrong-at-sonos)). Two rules fall out: **(a) never ship without the boring core (queue, timer, basic controls)**; **(b) collapse duplicate browse surfaces.**

**Incumbent nav for reference:** Apple Music = 4 tabs (Listen Now / Browse / Radio / Library) ([freeyourmusic](https://freeyourmusic.com/blog/apple-music-vs-tidal-sound-quality-music-discovery-cost-compared-2024)). General IA practice: group into few high-level categories that expand progressively, per **Hick's Law** — decision time grows logarithmically with options, so a cluttered home "is off-putting" ([nngroup](https://www.nngroup.com/videos/hicks-law-long-menus/), [hubspot](https://blog.hubspot.com/website/information-overload)).

**Recommendation — 3-tab IA for Город ФМ:**
1. **Волна (Now/Radio)** — the default; the living flow + steer. This is 80% of sessions.
2. **Мой вкус (Twinr)** — the visible, editable taste profile (doc 04); doubles as "library/saved."
3. **Открыть (Discover)** — named/curated waves (NTS-style cultural titles + KZ/CIS locality), AI tours, occasions.

Cut: a separate "Search" tab (fold search into a persistent top affordance + the chat companion); a separate "Radio" *and* "Browse" split (one Discover surface); any "Browse" wall of editorial grids that competes with the flow.

---

## 4. Core gestures & interactions (lean-back, Hick-minimized)

A lean-back radio must make the **5 primary actions effortless and everything else secondary**:

| Action | Recommended interaction | Precedent |
|---|---|---|
| **Skip / next** | Large always-visible next; swipe-left on art | universal |
| **Like / dislike** | Twin tap targets on player; dislike = "less like this" steer (feeds Twinr, doc 02) | Yandex thumbs, Spotify Hide/Snooze ([support.spotify](https://support.spotify.com/us/article/autoplay/)) |
| **Save** | Single tap heart; bookmarks into Twinr | universal |
| **Steer** | "**Сделай по-другому**" pill + tap-and-hold mic for voice request | DJ X voice request ([9to5mac](https://9to5mac.com/2025/05/14/dj-spotify-ai-now-takes-requests/)); Yandex dials |
| **Seek** | Standard scrubber (lean-forward only; de-emphasize in radio mode) | universal |

**Re-roll the whole wave** = one gesture (Yandex «Встряхнуть»). **Apply Hick's Law:** never present more than ~3 mood dials at once; reveal sub-options progressively; keep the default screen to player + one steer affordance + one "why this" line. Endel's lesson: the moment the UI demands management, the lean-back promise breaks (its forced 5-min warmups frustrate users — [ixd.pratt](https://ixd.prattsi.org/2026/02/design-critique-endel-ios-app/)). **Don't gate the flow behind setup.**

---

## 5. Cross-surface (web / mobile / TV / car)

Radio is the *one* music format that shines in lean-back contexts (car, TV, speaker), so cross-surface is strategic, not optional.
- **Car (CarPlay / Android Auto):** oversized targets, simplified menus, **voice-first** — research shows voice yields "significantly lower distraction" than touch ([androidpolice](https://www.androidpolice.com/android-auto-better-than-carplay/), [developer.apple.com/carplay](https://developer.apple.com/carplay/)); drivers want "less tapping, more glanceable info" ([bgr](https://www.bgr.com/2021996/apple-carplay-features-android-auto-needs/)). Город ФМ's voice-steer ("сделай по-другому") is *natively* the right car interaction — lead with it. Reduce to: now-playing, skip, like, one voice-steer button.
- **TV / speaker:** glanceable now-playing + ambient cover motion; steer via voice or remote D-pad; never require text entry.
- **Web/mobile:** the full experience (Twinr editing, chat, discover).

Design the **flow + steer as a portable core** that degrades gracefully: every surface shows player + skip + like + voice-steer; only rich surfaces add Twinr/Discover/chat.

---

## 6. Premium / immersive vs generic — the craft checklist

What separates premium (Tidal, Apple) from generic players:
- **Space & restraint** over feature density (Tidal "clean/slick"; Apple "cluttered" when over-packed).
- **Art-tinted ambient backgrounds** + **animated covers** (calm, radio-appropriate motion, not TikTok).
- **Haptics**: Apple Music Haptics + higher-quality motors make apps "not just look good but feel right" ([darioo.com](https://darioo.com/haptic-feedback-sensory-design-the-next-big-thing-in-mobile-app-ux/)); add subtle haptics on like/skip/steer-confirm.
- **Motion that means something**: the wave visibly *responds* to steering — the single most ownable "premium + explainable" moment, since no incumbent shows the taste reacting in real time.
- **Onest + #5168FC + true-dark canvas** (per project tokens) audited on OLED so the accent and art-tints stay legible.

### Pitfalls to avoid
- Shipping without the **boring core** (queue/timer/controls) — the Sonos mistake.
- **Duplicate browse surfaces** / too many nav tabs (Sonos: 3 of 5 tabs browsing).
- **Choice overload** on the home screen (Hick's Law) — don't open with a grid wall.
- **Gating the flow** behind warmups/setup (Endel) — let the wave start instantly.
- **Talk over music** by default (NTS keeps Infinite Mixtapes 100% music) — make AI commentary opt-in/ambient, not constant.
- Treating the player as a control panel — reserve its prime real estate for **"why this" + steer**, Город ФМ's actual differentiators.

---

### Sources
Spotify design evolution ([rausr.com](https://rausr.com/blog/the-evolution-of-spotify-design/)) · Spotify controls/DJ ([newsroom 2025-05-07](https://newsroom.spotify.com/2025-05-07/experience-a-new-dimension-of-music-discovery-with-more-controls-and-enhanced-tools/), [2025-09-05](https://newsroom.spotify.com/2025-09-05/new-user-controls-personalize-listening/), [9to5mac](https://9to5mac.com/2025/05/14/dj-spotify-ai-now-takes-requests/), [support](https://support.spotify.com/us/article/autoplay/)) · Yandex «Моя волна» ([yandex 28-05-2025](https://yandex.com/company/news/28-05-2025), [vc.ru context](https://vc.ru/services/1247751-obnovlenie-yandeks-muzyki-moya-volna-uchityvaet-kontekst-zanyatiy)) · Apple Music vs Tidal ([freeyourmusic](https://freeyourmusic.com/blog/apple-music-vs-tidal-sound-quality-music-discovery-cost-compared-2024), [macobserver](https://www.macobserver.com/tips/round-ups/apple-music-vs-tidal/)) · NTS ([nts.live](https://www.nts.live/)) · Sonos Radio ([sonos.com](https://www.sonos.com/en-us/sonos-radio)) · Endel ([autonomous.ai](https://www.autonomous.ai/ourblog/endel-app-review), [ixd.pratt critique](https://ixd.prattsi.org/2026/02/design-critique-endel-ios-app/)) · Sonos app disaster ([rogerwong.me](https://rogerwong.me/2025/02/when-the-music-stopped-inside-the-sonos-app-disaster), [techcrunch](https://techcrunch.com/2024/10/01/sonos-outlines-turnaround-plan-following-app-disaster/), [leaddev](https://leaddev.com/technical-direction/what-went-wrong-at-sonos)) · Hick's Law / IA ([nngroup](https://www.nngroup.com/videos/hicks-law-long-menus/), [hubspot](https://blog.hubspot.com/website/information-overload), [ixdf](https://ixdf.org/literature/topics/hick-s-law)) · Haptics/multi-sensory ([thinkdebug](https://thinkdebug.com/multi-sensory-apps-designing-with-sound-vibration-and-haptics/), [design.google](https://design.google/library/ux-sound-haptic-material-design), [darioo](https://darioo.com/haptic-feedback-sensory-design-the-next-big-thing-in-mobile-app-ux/)) · Car/cross-surface ([developer.apple.com/carplay](https://developer.apple.com/carplay/), [androidpolice](https://www.androidpolice.com/android-auto-better-than-carplay/), [bgr](https://www.bgr.com/2021996/apple-carplay-features-android-auto-needs/))
