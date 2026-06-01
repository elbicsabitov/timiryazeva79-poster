# Город ФМ — Making Twinr AI Feel NATIVE, Not a Bolted-On Chatbot

**Topic 07 of the Город ФМ architecture research.** Audience: founder + designer/eng lead. **Date:** 2026-06-02.
**The trigger:** the prototype's AI is a corner chat dock — it reads as a *widget glued onto a player*. This brief says exactly where and how to **weave Twinr into the player, radio flow, now-playing, and home** so the AI is the product's *substance*, not an accessory. Companion to [02-steerable-conversational](./02-steerable-conversational.md) (the steering backend) and [04-explainability-narration](./04-explainability-narration.md) (the "why" layer).

**Bottom line:** *AI is a layer, not a window.* The chat dock stays — but it becomes the **deep/precise path**, while 80% of AI value moves **inline into the surfaces the user already looks at**: the now-playing card, the next-up queue, the home shelves. The model for this is **Spotify AI DJ living inside the player**, not Spotify's separate "AI Playlist" screen.

---

## 1. "AI as a layer, not a window" — the core stance

The dominant failure mode of 2024–25 AI products is the **corner-chatbot reflex**: bolt a chat panel on the side and call it AI-native. The industry has explicitly named this an anti-pattern — "most AI apps follow a familiar chat pattern… easy to implement, [but] they create unnecessary interaction overhead" ([LangChain, Ambient Agents](https://www.langchain.com/blog/introducing-ambient-agents)). The opposite stance is **ambient/woven AI**: the intelligence shows up *in the object the user is already manipulating*, anticipating and acting in-context rather than waiting behind a "send" button ([Raw.Studio, Ambient AI in UX](https://raw.studio/blog/ambient-ai-in-ux-interfaces-that-work-without-buttons/); [Shout Digital, Invisible AI](https://www.shoutdigital.com/insights/invisible-ai-ambient-intelligence-for-seamless-ux/)).

The cleanest articulation comes from **Dia** (the AI browser from the Arc team): it deliberately rejects the sidebar-add-on and puts the model **into the omnibox and into the page itself**, so the assistant "feel[s] like part of the browsing workflow, not an add-on that sits next to it" ([TechCrunch on Dia](https://techcrunch.com/2025/11/03/dias-ai-browser-starts-adding-arcs-greatest-hits-to-its-feature-set/); [SupaSidebar comparison](https://supasidebar.com/blog/arc-browser-vs-dia-browser)). That is the exact reframing Город ФМ needs: **Twinr should be felt in the music, not visited in a panel.**

**When chat IS right vs when inline beats it:**
- **Inline wins** for the high-frequency, in-flow micro-acts: "why this track," "make it darker," "more like this," skip-with-reason, "shake it up." These happen *every minute* and must never cost a context-switch to a chat window.
- **Chat wins** for the rare, expressive, multi-turn acts: "build me a 40-min rainy-drive set, nothing sad," the **music-history tour** ("how we got to Imagine Dragons"), résumé→taste, "explain my whole Twinr profile." These are conversational by nature — the dock is their home.

---

## 2. Deep dive: how Spotify AI DJ lives INSIDE the player (the model to copy)

Spotify AI DJ is the canonical "AI woven into a player" — study its exact mechanics:

- **It is not a screen, it's a control.** You start it from search → "DJ" → play, and from then on **you manage everything from the playback screen without leaving it** ([Spotify newsroom, 2025-05-13](https://newsroom.spotify.com/2025-05-13/dj-voice-requests/)). There is no "AI tab" you navigate to.
- **One button, two gestures = the entire steer.** The **DJ button sits in the right-hand corner of the player.** **Quick tap = "change the vibe" / skip to a new section** (no words needed — the lazy path). **Press-and-hold = voice request** ("you'll hear a beep when DJ is ready"), e.g. *"Give me some electronic beats for a midday run."* ([Spotify newsroom](https://newsroom.spotify.com/2025-05-13/dj-voice-requests/); [TechCrunch](https://techcrunch.com/2025/05/13/spotifys-ai-dj-now-lets-you-use-voice-commands-to-personalize-your-tunes/)).
- **Text requests too**, added Oct 2025 — so steering isn't voice-only ([TechCrunch, text DJ](https://techcrunch.com/2025/10/15/you-can-now-text-spotifys-ai-dj/)).
- **Spoken commentary between tracks** introduces songs/artists with facts and **says *why a track was chosen for you*** — the explainability is *narrated in the flow*, not buried in a menu ([Spotify newsroom 2023 launch](https://newsroom.spotify.com/2023-02-22/spotify-debuts-a-new-ai-dj-right-in-your-pocket/)). Voice tech is Sonantic; **facts are human-editor-verified, not free-hallucinated** (see [04](./04-explainability-narration.md)).

**The lesson for Город ФМ:** the AI's primary body is a **button on the now-playing card** plus **narration between tracks** — not a panel. The chat dock is the *secondary*, expressive surface.

**Yandex «Моя волна» — the dial primitive** (the lazy, no-typing path): contextual **mood + activity + language dials sit at the bottom of the now-playing screen** (energetic/cheerful/calm/sad; workout/work/drive), and **«Встряхнуть волну» (Shake)** is a one-gesture re-roll off the usual path ([Yandex support, Моя волна](https://yandex.ru/support/music/ru/new-library/my-wave); [t-j.ru explainer](https://t-j.ru/lt-my-vibe-yandex-music/)). Город ФМ should ship **dials + Shake (lazy) alongside chat + voice (precise)** — three steering surfaces, one shared session-intent vector (per [02 §7](./02-steerable-conversational.md)).

**Apple Music** is the counter-reference: strong taste-aware **Autoplay (infinity loop)** and bubble onboarding, but the intelligence is **silent — no "why," no steer-in-flow.** That silence is precisely the gap Город ФМ attacks; don't copy Apple's opacity, copy its onboarding only ([Apple Music algorithm guide 2026](https://beatstorapon.com/blog/the-apple-music-algorithm-in-2026-a-comprehensive-guide-for-artists-labels-and-data-scientists/)).

---

## 3. In-context AI affordances from outside music (what "woven in" looks like)

- **Superhuman** — AI is keyboard-/inline-native, never a chatbot: **Cmd+J writes a draft in place**; **Instant Reply shows 3 draft replies at the bottom of the message, Tab-cycle to preview**; **Cmd+K → Ask AI** is the command-bar deep path ([Superhuman: Write with AI](https://help.superhuman.com/hc/en-us/articles/38456855116307-Write-with-AI); [Instant Reply](https://help.superhuman.com/hc/en-us/articles/38458397554963-Instant-Reply); [Ask AI](https://help.superhuman.com/hc/en-us/articles/38458628979091-Ask-AI)). **Pattern to steal: Tab-cycle suggested alternatives** → Город's "next-up" can show 2–3 candidate next tracks you tab through, each with its one-line reason.
- **Notion AI** — inline writer invoked at the cursor / via highlight, transforming the block you're in rather than a side panel ([eesel, Notion AI Inline guide](https://www.eesel.ai/blog/notion-ai-inline)). **Pattern: act on the object under focus** (the current track), not a detached input.
- **Raycast / command-bar** — AI as a keystroke-summoned action layer over whatever you're doing; the dock is invoked, used, dismissed — never persistently in your face.
- **Granola** — the **"invisible/ambient" extreme**: it captures meetings with **no bot joining the call**, staying in the background and "out of the way," explicitly "the meeting note-taker that stays invisible" ([The Weekly Momentum](https://theweeklymomentum1.substack.com/p/ai-unlocked-3-granola-the-meeting); [aiixx review](https://aiixx.ai/blog/granola-ai-review-the-meeting-notepad-that-killed-the-awkward-bot)). Founding rule: *"AI should help you think better. It should not be thinking for you."* **Pattern for Город: the AI assists the listen, it doesn't seize the wheel** — the user still owns play/skip/save; AI annotates and offers, never hijacks.

**Synthesis of the woven pattern (4 reusable moves):**
1. **Act on the focused object** (current track), not a detached prompt box (Notion).
2. **Offer in-place alternatives you can cycle** (Superhuman Tab; Yandex Shake).
3. **One control, layered gestures** (Spotify DJ tap vs hold).
4. **Stay ambient until invoked or genuinely useful** (Granola; Raycast).

---

## 4. CONCRETE recommendations — exactly where Twinr lives in Город ФМ

Map every AI capability to a **specific UI placement + interaction**. (Reuse brand tokens `--brand-blue-light #5168FC`, Onest, hit-targets ≥44px, `prefers-reduced-motion`.)

### A. Now-playing card — the AI's primary body
- **"Twinr" steer button, bottom-right of the now-playing card** (the DJ-button slot). **Tap = "Shake / change the vibe"** (re-roll the next pick, lazy path). **Press-and-hold = voice/text steer** ("сделай темнее", "больше как это") → routes to the §2 session-intent vector. One control, two gestures — copied from Spotify DJ. Visually distinct from the Tweaks gear and from the corner chat launcher.
- **Always-on "почему?" affordance under the track title** — a 3–6-word reason chip ("арена-рок 2010-х · вы сохранили Molchat Doma"), tap to expand the KG-path sentence (per [04 §5](./04-explainability-narration.md), progressive disclosure). This is the single most important native move: **the explanation is *on the track*, not in a chat reply.** (Spotify proved explained recs get up to 4× clicks — [04](./04-explainability-narration.md).)
- **Inline steer-chips on the card** (not only in chat): `Темнее` · `Поэнергичнее` · `Меньше рекламы` · `Сделай по-другому`. Tapping mutates the session vector and **the next track changes within 1–2 songs with a transition ramp** ([02 §4](./02-steerable-conversational.md)). Each tap throws a tiny confirmation ("убрал арена-рок, добавил тёмный бит — профиль обновлён").
- **Mood/activity/language dials** (Yandex pattern) collapsed into a "Настроить волну" pill on the card → expands to dials. The lazy, no-typing steer for users who won't talk to an AI.

### B. Radio flow / between tracks — narration as the ambient AI presence
- **Optional spoken/▶-to-hear DJ intro between tracks** (Spotify-style), generated **async while the current track plays** (never blocks playback — [02 §5](./02-steerable-conversational.md)). Default to a **text "now→next" ribbon** ("Сейчас *Believer* → дальше *Centuries*, потому что…"); voice narration is an opt-in toggle, not forced.
- **Narration is the proof the radio is *thinking*** — it's where "explainable autoplay" becomes *felt*. Cap frequency (see §5): narrate on **vibe-shifts and user steers**, not every single track.

### C. Next-up queue — make the queue itself explainable & steerable
- **Each upcoming track shows a one-line "why it's next" + a thumb/✕**, and (Superhuman Tab pattern) the immediate next slot can offer **2–3 candidates you swipe/tab between**, each with its reason. Removing one re-plans the chain live. The queue stops being a dumb list and becomes a *visible reasoning trace*.

### D. Home — Twinr profile as a living, first-class object (not a hidden vector)
- **"Twinr" taste widget pinned on home** (per VISION #5 and Spotify's Mar-2026 *Taste Profile* which is **visible + editable**, lets users flag inaccuracies and ask for "more/less of a vibe" — [Spotify Taste Profile beta](https://newsroom.spotify.com/2026-03-13/taste-profile-beta-announcement/), cited in [02 §3](./02-steerable-conversational.md)). Show genres/mood/era as **editable tiles** + a live "% match / how it evolved this week" line. Editing a tile **is** steering — it writes to the durable profile via the confirmation gate ([02 §4](./02-steerable-conversational.md)).
- **Shelves carry inline "why" + a "сделай иначе" on each row**, so steering exists on home too, not only in-player.
- **Profile changes animate** when the user steers anywhere — the widget pulses/updates so the cause→effect of "I corrected the radio → my profile moved" is *seen*. This visible feedback loop is the differentiator the VISION is built on.

### E. The chat dock — demote to the deep/expressive path (keep, don't delete)
- The corner dock **stays as the home for multi-turn, expressive intents**: music-history **tours**, "build a set for X," résumé→taste, "explain my whole profile." It should **open *from* an inline affordance** (tap "почему?" → "ask Twinr more" expands the dock with that track already in context — the Dia "@-mention the page into chat" move), so chat feels *continuous with* the UI, not a separate room ([Dia/Arc](https://techcrunch.com/2025/11/03/dias-ai-browser-starts-adding-arcs-greatest-hits-to-its-feature-set/)).
- **Command-bar (Cmd/Ctrl-K) "Спросить Twinr"** as a power-user deep path over the whole app (Superhuman Ask AI / Raycast pattern).

**One-line rule for the team:** *if an AI action happens more than once a session, it must have an inline home on the surface where it's needed; only rare, multi-turn, expressive actions go to the dock.*

---

## 5. Proactive vs reactive — narration & cues without being annoying

The radio's AI is inherently **proactive** (it narrates, it suggests). Proactivity is also where products self-destruct. Govern it with an explicit **interruption budget**:

- **Hard ceiling: 3–5 proactive interventions per session**, treated as withdrawals from a finite trust account. A proactive cue the user ignores is **worse than none** — it spent budget and produced *negative* trust; only a cue that triggers action is net-positive ([TianPan, Notification/Attention Budget](https://tianpan.co/blog/2026-05-13-background-agents-notification-budget-attention-economy); [Glean, proactive notifications](https://www.glean.com/perspectives/how-to-use-ai-for-proactive-customer-support-notifications)).
- **Gate every proactive cue on relevance + importance + user-state** — don't narrate when the user is clearly in flow / just hit play / is mid-skip-spree ([vanishlabs, Proactive AI](https://vanishlabs.ai/news/proactive-ai); [Forge, Interruption Design](https://guide.forge.athena.io/guidelines/interruption-design)).
- **Suggestive, not imposing language**, low linguistic complexity — research on proactive voice assistants shows users prefer "хотите темнее?" over "Переключаю на тёмный режим" ([How May I Interrupt?, IJHCI 2024](https://www.tandfonline.com/doi/full/10.1080/10447318.2023.2266251)).
- **Narrate on events, not on a timer:** vibe-shift, a user steer, a new-artist discovery, the top of a tour — **not** every track. Make between-track voice **opt-in** with a one-tap mute-for-session.
- **Always-available opt-out + oversight**, per the ambient-agent UX patterns (status, controls, "what did it just do / why," undo) — the user must always be able to see what Twinr changed and turn the talking off ([bprigent, 7 UX Patterns for Ambient AI](https://www.bprigent.com/article/7-ux-patterns-for-human-oversight-in-ambient-ai-agents)).
- **Trust = honesty:** the narrated "why" must reflect the *real* signal that drove the pick (no post-hoc fairy tales — [04 §5](./04-explainability-narration.md)), and facts must be grounded/verified (no hallucinated tour dates — [04 §2](./04-explainability-narration.md)).

---

## Pitfalls (read before building)

1. **Re-bolting the chatbot.** If "AI" = only the corner dock, you've shipped the anti-pattern. The dock must be the *minority* of AI surface; the majority is inline on the now-playing card, queue, and home.
2. **AI seizing the wheel.** Granola's rule: assist, don't override. Never auto-change taste, auto-skip, or talk over the user without an obvious, instant opt-out. The listener owns play/skip/save.
3. **Narration fatigue.** Talking between every track is the fastest way to get muted forever. Event-gated + budgeted + opt-in voice.
4. **Explanation in the wrong place.** Putting "why" only inside chat re-creates the window problem — the reason must live *on the track*.
5. **Two steering brains.** Chat-steer and inline-steer (dials/chips/voice) must write to the **same session-intent vector** ([02 §4](./02-steerable-conversational.md)), or the radio will contradict itself.
6. **Dishonest or hallucinated "why."** Post-hoc rationalizations and invented facts kill the entire "explainable" pitch on first catch ([04](./04-explainability-narration.md)).
7. **Cyrillic/RU steering as an afterthought.** Inline chips, voice parse, and dials must all be first-class in Russian from day one ([02 pitfalls](./02-steerable-conversational.md)).
8. **Reduced-motion / a11y.** The living-profile animation and floating cues need `prefers-reduced-motion` fallbacks and ≥44px targets (Holy Grail gates).

---

## TL;DR build order for the prototype
1. **Now-playing "почему?" reason chip** (always-on, tap-to-expand) — the highest-leverage native move.
2. **Twinr steer button on the card** (tap=Shake, hold=voice/text) + **inline steer-chips** + **mood dials**.
3. **Living Twinr profile widget on home** that visibly moves when you steer anywhere.
4. **Between-track "now→next" ribbon** (text default, voice opt-in), event-gated to the interruption budget.
5. **Demote chat dock to the tour/build/explain deep path**, openable *from* inline affordances.

*Sources linked inline. Primary: Spotify AI DJ ([newsroom 2025](https://newsroom.spotify.com/2025-05-13/dj-voice-requests/), [2023](https://newsroom.spotify.com/2023-02-22/spotify-debuts-a-new-ai-dj-right-in-your-pocket/)), Spotify Taste Profile ([2026-03](https://newsroom.spotify.com/2026-03-13/taste-profile-beta-announcement/)), Yandex Моя волна ([support](https://yandex.ru/support/music/ru/new-library/my-wave)), Dia/Arc ([TechCrunch](https://techcrunch.com/2025/11/03/dias-ai-browser-starts-adding-arcs-greatest-hits-to-its-feature-set/)), Superhuman ([Write with AI](https://help.superhuman.com/hc/en-us/articles/38456855116307-Write-with-AI), [Instant Reply](https://help.superhuman.com/hc/en-us/articles/38458397554963-Instant-Reply)), Notion AI Inline ([eesel](https://www.eesel.ai/blog/notion-ai-inline)), Granola ([Weekly Momentum](https://theweeklymomentum1.substack.com/p/ai-unlocked-3-granola-the-meeting)), ambient agents ([LangChain](https://www.langchain.com/blog/introducing-ambient-agents), [bprigent 7 patterns](https://www.bprigent.com/article/7-ux-patterns-for-human-oversight-in-ambient-ai-agents)), interruption budget ([TianPan](https://tianpan.co/blog/2026-05-13-background-agents-notification-budget-attention-economy)). Internal: [02-steerable-conversational](./02-steerable-conversational.md), [04-explainability-narration](./04-explainability-narration.md), [VISION](../../superpowers/VISION-gorod-fm-ai-driven.md).*
