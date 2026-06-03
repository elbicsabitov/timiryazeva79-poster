# SPEC — Город ФМ · Médiateka «Собери вкус» taste-cloud (Открыть / #/podborki)

> Build-ready, opinionated. Implement directly in the single-file SPA
> `designs/gorod-fm.html` (~14.7k lines). Every visual choice maps to a token
> from the ground map; every behavior is grounded in re-grepped code anchors
> (verified 2026-06-03 against the live file).
>
> **One-line intent:** Replace the static genre **filter** at the bottom of the
> Médiateka section with an *embedded, in-page* select-to-build-taste **cloud**
> (genres **and** artists) whose taps write the real `gorodfm_taste` vector and
> drive a live, honest "модель за N сигналов" counter — staying a scrollable
> section so the Подборки carousel + AI-ask remain visible above.

---

## 0. Ground truth (re-grepped, do not trust from memory)

| Thing | Where (verified) |
|---|---|
| Médiateka `<section class="mediateka">` | **L7908–L7920** |
| `<div class="media-bubbles" id="mediateka-bubbles" role="group" aria-label="Жанры — тапни шарик, чтобы отфильтровать">` | **L7913** — **REPLACE** |
| Subtitle (already promises taste, currently a lie) | **L7911** `"…тапни жанр-шарик — добавляй в вкус, и волна учится."` |
| `<input id="mediateka-input">` search | **L7914–L7917** — **KEEP** |
| `<div id="mediateka-grid">` | **L7918** — **KEEP** |
| `<p id="mediateka-empty">` | **L7919** — **KEEP** |
| `.media-bubble*` CSS (static filter pill + float keyframe) | **L4363–L4370** — leave defined, becomes dead after HTML swap; optionally delete |
| `.mediateka-*` CSS (search/grid/cards) | **L4350–L4362** |
| `.onb-*` cloud CSS (bubble/check/static fallback) | **L2291–L2448** |
| Onboarding IIFE (`window.GorodOnboarding`) | starts ~L11816, `start/stop` **L12513–12533**, `sync()` route-gates on `#/onboarding` **L12536–12542** |
| Engine internals: `makeBubble` **L11969**, `measure` (couples `.onb-head`/`.onb-foot`) **L12034**, `scatter` **L12051**, `paint` **L12069**, `step` physics **L12074–12110**, `ensureRoom` recycle **L11945**, `relatedFor` bloom **L11932** |
| Shared seed constants | `ASSET` **L11817**, `DATA` **L11818–11839**, `REL` **L11842–11863**, `MAX_BUBBLES=80` **L11864**, `GENRE_HUE` **L11865**, `POOL` **L11872+** |
| Onboarding readiness gate | **L11904** `var met = n >= 5;` |
| Honest per-tap "why" literals | genre **L12343** `'выбрал <b>X</b> — поставил <lc> в центр вектора.'`; artist **L12348** `'тапнул <b>X</b> → подтянул <lc(g)> и похожих.'` |
| Canonical taste write format | **L12429–12430** `JSON.stringify(vec.map(r => r.kind==='genre' ? r.name.toUpperCase() : r.name).slice(0,8))` |
| Fidelity rule (count chosen, not derived) | **L12383** `pickedCount()` excludes `kind==='mood'` |
| Current GorodMediateka IIFE | **L14713–L14772** (`ART` L14715, `GENRES` L14723, `addTaste` L14733, `activeGenre` filter L14730/L14756–14761) |
| aria-live receipt precedent | `announce()` **L12407** |

**The honesty gap to close:** L7911/L14752 say taps *add to taste*, but the
bubble tap handler (L14756–14761) only sets `activeGenre` and **writes nothing**
to `gorodfm_taste`. The cloud must make the bubble tap a *real additive signal*.

---

## 1. DECISION SUMMARY (read this, then build)

| Question | Decision |
|---|---|
| **Interaction model** | **EMBEDDED, always-on, NOT collapsed, NOT a takeover.** A labeled in-page section that sits where `#mediateka-bubbles` was, *above* the search+grid. Live bubbles + honest one-line promise visible immediately (research: show value/preview before asking effort; never a mystery "tap to start" box). |
| **Reuse vs Fork** | **FORK** → new IIFE `GorodTasteCloud` mounting on `#tcloud-field`. Justified below (§3). Onboarding engine is route-gated and viewport-coupled; a copy with tuned constants is safer than parameterizing the live onboarding cloud. **Zero edits to the onboarding IIFE.** |
| **Seed data** | **Reuse the shared onboarding seed** (`DATA`/`REL`/`POOL`/`GENRE_HUE`/`ASSET`) by lifting them to file/module scope (§4). Same genres + same real artist assets + same coherent bloom. Single source of truth → "волна учится" is literally true cross-surface. |
| **Taste write** | Taps write the **real `gorodfm_taste`** in the **canonical format** (genres `toUpperCase()`, `slice(0,8)`) shared with onboarding + the grid's "+ в вкус". Pre-populate selected state from existing `gorodfm_taste` at init. |
| **Counter** | **`Твоя модель за N сигналов`**, threshold **`n >= 5`** identical to onboarding. Counts only *directly-tapped* genre/artist bubbles — never bloomed children, never derived moods. Claim ladder is seed-honest (§5). |
| **Filter vs Build** | **BUILD only.** The cloud commits to taste (durable). The grid below is filtered **only by search text** (existing `#mediateka-input`). The old `activeGenre` single-select filter is **removed** — one gesture, one meaning (research: never overload tap with filter+commit). |
| **Bloom label** | Bloomed/expanded artists carry a hairline **"Подборка от редакции"** microcaption — scripted relations are honestly labeled curated, never "Похожие исполнители" (no real neighbor model exists; `REL`/`POOL` are hardcoded). |
| **a11y** | Keep the onboarding `role="group"` + per-bubble `<button aria-pressed>` toggle-group pattern. NOT listbox. One `aria-live="polite" aria-atomic="true"` region = the visible counter line. Freeze focused bubble's physics. |
| **Motion/perf** | `prefers-reduced-motion` static flex-wrap fallback (live `matchMedia` listener). IntersectionObserver pauses rAF off-screen. `touch-action: manipulation` (never `none`). Transform-only paint. Lower `MAX_BUBBLES` (=22). All gated through one `requestRun()` predicate. |

---

## 2. Interaction model (embedded, always-on)

```
#/podborki (scrollable) ─────────────────────────────────────────
  [ AI-ask conversational top ]
  [ Подборки hero carousel — tall tiles, real covers ]   ← value shown FIRST
  [ taste-map ]
  [ shelves: Рядом / Исполнители / Группы / От редакции ]
  ┌─ <section class="mediateka"> ──────────────────────────────┐
  │  h3 Медиатека                                              │
  │  p  "Тапни жанр или артиста — добавится в твой вкус,       │  ← honest promise (replaces L7911)
  │      волна сразу подстроится."                             │
  │  ┌─ .tcloud-wrapper (always visible) ──────────────────┐   │  ← REPLACES #mediateka-bubbles
  │  │  .tcloud-field  (role=group, ~190px, rAF cloud)     │   │
  │  │  .tcloud-counter  "Твоя модель за N сигналов"        │   │  ← aria-live region
  │  └─────────────────────────────────────────────────────┘   │
  │  [ 🔍 search input #mediateka-input ]   ← KEEP (text filter only)
  │  [ artist grid #mediateka-grid ]        ← KEEP ("+ в вкус" stays)
  │  [ empty state #mediateka-empty ]       ← KEEP
  └────────────────────────────────────────────────────────────┘
```

- **Always-on**, not collapsed. Renders a live cloud + honest one-line promise
  on first paint. No "Собери вкус" expand-affordance gate (research pitfall:
  default-collapsed mystery box suppresses adoption; preview the value).
- **Height:** `.tcloud-field { min-height: 190px }` (a bounded box, lower than
  the full-screen `#onb-field`). The wrapper has `padding:16px`, so total
  section footprint ≈ 230px — comparable to the old `.media-bubbles` 104px +
  margins, so layout below is undisturbed. On narrow viewports clamp to 170px.
- **Sits ABOVE** search + grid (same DOM order as the old bubbles). Collections
  remain visible above the whole section; AI-ask never buried (operator's hard
  requirement "красивые подборки видно сразу", "AI не потерять").

---

## 3. REUSE vs FORK — decision = **FORK** (`GorodTasteCloud`)

**Why fork, not reuse the onboarding engine** (grounded in the ground map):

1. **Viewport coupling.** `measure()` (L12034–L12049) reads `.onb-head` /
   `.onb-foot` `getBoundingClientRect()` to compute `PAD_TOP`/`PAD_BOTTOM`. Those
   elements live only in the `#/onboarding` route. An embedded ~190px box has no
   such header/footer; it needs a scoped `measure()` using its own container rect
   (small fixed insets), not viewport-relative onboarding chrome.
2. **Physics calibration.** Constants are tuned for a ~600×800 full-screen band
   (attraction `k` 0.00020/0.00008, repulsion `push=0.16`, damping `0.965`, wall
   bounce `-0.55`, `BASE=104`, `MAX_BUBBLES=80`). In a ~360×190 box these cause
   wall-bounce thrash and oversized repulsion. The fork retunes (§7).
3. **Route gating conflict.** Onboarding's `sync()` (L12536) starts the loop only
   on `#/onboarding` and stops otherwise. The cloud must run on `#/podborki`.
   Sharing one IIFE would tangle two route predicates and two lifecycles.
4. **Scope mismatch.** Onboarding = "pick 5+ from scratch" with a mandatory CTA
   gate (`#onb-cta` disabled until met). Médiateka = "add to existing taste",
   no CTA — just a live counter. Different `refreshCount()` semantics (no CTA
   disable; pre-populate from storage).
5. **Lifecycle additions.** The cloud needs IntersectionObserver pause +
   focus-freeze + live `matchMedia` re-eval that onboarding does not have.

**Shared, not duplicated:** the *seed data* (`DATA`/`REL`/`POOL`/`GENRE_HUE`/
`ASSET`) is lifted to a tiny module-scope namespace so both IIFEs read one
source of truth (§4). The *engine functions* are copied (forked) with tuned
constants — duplicating ~120 lines of physics is acceptable and isolates risk
from the live onboarding cloud (the operator's "do not break #/onboarding" gate).

**Module API (trimmed):**

```js
// IIFE auto-mounts; exposes a tiny control surface for the lifecycle gate.
window.GorodTasteCloud = {
  start(),          // begin rAF (idempotent; no-op if reduced/off-screen/focus-paused)
  stop(),           // cancelAnimationFrame
  requestRun(),     // re-evaluate predicate (motion-allowed && visible && !focusPaused)
  refresh()         // re-read gorodfm_taste, re-sync selected state + counter
                    //   (call after the grid '+ в вкус' writes so cloud stays in sync)
};
```

`opts` is not needed — there is exactly one mount (`#tcloud-field`). The mount id
is hard-required: if `document.getElementById('tcloud-field')` is null, the IIFE
returns early (mirrors onboarding `build()` returning false on missing field).

---

## 4. Seed data — REUSE onboarding seed (single source of truth)

Lift the five constants out of the onboarding IIFE into a small shared namespace
declared **once, before both IIFEs** (so neither re-declares them). Place it
immediately before the onboarding IIFE opening (~L11816).

```js
/* Shared taste-elicitation seed — single source of truth for #/onboarding
   AND the Médiateka taste-cloud. Genres + real Figma artist assets + curated
   bloom relations. Do NOT fork this data; both clouds read it. */
window.GorodTasteSeed = (function () {
  var ASSET = 'assets/gorod-fm/';
  var DATA = [ /* …verbatim copy of L11818–11839 (20 genre+artist roots) … */ ];
  var REL  = { /* …verbatim copy of L11842–11863 … */ };
  var POOL = { /* …verbatim copy of L11872+ … */ };
  var GENRE_HUE = { /* …verbatim copy of L11865–11869 … */ };
  return { ASSET:ASSET, DATA:DATA, REL:REL, POOL:POOL, GENRE_HUE:GENRE_HUE };
})();
```

Then in the onboarding IIFE, replace its local `var ASSET/DATA/REL/POOL/GENRE_HUE`
with `var S = window.GorodTasteSeed, ASSET=S.ASSET, DATA=S.DATA, REL=S.REL,
POOL=S.POOL, GENRE_HUE=S.GENRE_HUE;`. **This is the only edit to the onboarding
IIFE — a pure no-op refactor (same values, same names).** Verify `#/onboarding`
still works after (§9).

> If the operator prefers ZERO touch to onboarding: skip the lift and let
> `GorodTasteCloud` declare its **own** copies of the same arrays. Acceptable but
> violates the "single source of truth" mitigation (data could drift). **Default
> = lift to `GorodTasteSeed`.**

**Seed for the cloud:** initialize the cloud field with the same `DATA` roots
(20 items: 12 genres + 8 real artists with `home-*`/`favs-*`/`library-artist-*`
covers). `MAX_BUBBLES_CLOUD = 22` (§7) caps total; `ensureRoom()` recycles the
oldest untouched (unselected & unexpanded) bubble before bloom.

**Bloom rules (coherent, bounded):**
- Genre tap → blooms ≤4 representative artists from `REL[genre]`, topped up from
  `POOL[genre]` (shuffled, dedup) — exactly `relatedFor()` (L11932).
- Artist tap → blooms ≤4 similar from `REL[artist]` (e.g. `'Linkin Park'`), then
  `POOL[artist.genre]`.
- Each bubble blooms **once** (`b.expanded` guard, L11925). Exhausted branch →
  `pulse()` instead of spawning (L11960).
- Bounded by `MAX_BUBBLES_CLOUD=22` + `ensureRoom()` recycle → the section never
  grows unbounded; oldest untouched bubbles are removed from DOM (L11945–11956).

**Asset paths:** all 8 root artist covers in `DATA` already point at files under
`assets/gorod-fm/`. **Verify they exist** (§9 checklist) — `home-featured-egor-krid.png`,
`favs-artist-maks-korzh-base.png`, `favs-artist-dima-bilan-overlay.png`,
`favs-dj-martin-garrix.png`, `favs-group-linkin-park-overlay.png`,
`home-tile-vadim-adamov-base.png`, `favs-artist-mia-boyka.png`, `favs-artist-ramil.png`.
Bloomed children are **genre-tinted gradient bubbles** (text labels), not photos
(they have no `img`), so no extra assets needed for the bloom.

---

## 5. Taste write + counter + honest feedback

### 5.1 Storage (canonical, shared)
- Key: `gorodfm_taste` (`TKEY`).
- **Write format identical to onboarding L12429–12430:** array of names where
  **genre names are `toUpperCase()`** and artist names are as-is, capped
  **`slice(0,8)`**. A discover tap on `Рок` serializes as `'РОК'` (so it equals
  the onboarding token and does not duplicate).
- On init: `readTaste()`; for each cloud bubble whose name (genre uppercased) is
  in the stored array, set `b.sel=true` + `aria-pressed` + `.is-selected`. So a
  user arriving from onboarding at N=7 sees those bubbles pre-lit and the counter
  continuing, never resetting to 0.
- Debounce the write 120ms (throttle) to avoid a race with the grid's `+ в вкус`
  writer (risk: localStorage race). Each toggle still does an atomic
  read-modify-write of the full array.

### 5.2 Counter copy + claim ladder (HONEST, behavioral)
The visible counter line `#tcloud-count` **is** the aria-live region. Copy keyed
to N (count of directly-tapped genre+artist signals, NOT bloomed, NOT mood):

| State | Counter text | Why honest |
|---|---|---|
| `N === 0` | **`Собери вкус — тапни жанр или артиста`** | invitation, no claim |
| `0 < N < 5` | **`Твоя модель за N сигналов · ещё {5−N} до старта`** | seed-in-progress, exact remainder |
| `N >= 5` | **`Твоя модель за N сигналов · стартовый вектор собран`** | "seeded" claim only — Spotify-style |

Cap displayed N at 8 (matches `slice(0,8)`); beyond 8, show `за 8 сигналов`
(extra taps refine, don't unlock a categorically better claim — decision-tree
elicitation diminishing-returns finding).

**NEVER** say "мы поняли твой вкус" / "профиль готов". Understanding is reserved
for *behavioral* signals (the "дослушал 3×" wedge), which taps are not. Use the
verb "собрал стартовый вектор" (seeded).

### 5.3 Per-tap receipt (aria-live, states only the increment)
On each *select* tap, set the counter line text (it is `aria-live=polite`) — but
the persistent visible label is the counter; for the transient receipt reuse the
onboarding literal style (L12343/L12348) appended briefly OR fold into the
counter line as a prefix that resets on next tap. **Recommended:** the counter
line shows the state row from §5.2; additionally fire a short receipt into the
SAME live region for the increment, then it settles back to the state line.
Receipts:

- Genre select: **`+ Рок · сигнал N`** (and SR also hears via aria-pressed "нажато").
- Artist select: **`+ Linkin Park · сигнал N`**.
- Deselect: **`− Рок · сигнал N`** (count decremented).
- Bloom appended (new tappable targets, focus does NOT move to them):
  **`+N похожих ниже`** — described as the *expansion action*, never a claim
  about the user. Because focus stays on the tapped bubble, this announcement is
  the only way a SR user learns new bubbles appeared (ground-map a11y finding).

Each tap states **exactly one increment**. Never phrase a single tap as
completing the profile.

### 5.4 Scripted-relation honesty label
Below the cloud field (inside `.tcloud-wrapper`, under the counter) render a
hairline microcaption, shown only once any bloom has happened:
**`Связи между артистами подобраны редакцией`** (`.tcloud-editorial-note`,
`color: var(--text-ter)`, 11.5px Onest). This labels the curated `REL`/`POOL`
relations honestly (no computed neighbor graph exists) — matching the
onboarding mood's honest-derivation flag (L12351). Do **not** title the bloom
"Похожие исполнители".

---

## 6. Cloud taps ↔ grid/search — **BUILD, not filter**

- **Remove** the `activeGenre` single-select filter entirely (delete L14730 var,
  L14756–14761 bubble handler, and the `(!activeGenre || a.g === activeGenre)`
  clause in `render()` at L14744 → becomes `return (!q || a.n.toLowerCase()…)`).
- The grid (`#mediateka-grid`) is now filtered **only by search text**
  (`#mediateka-input`). One gesture, one meaning.
- **Sync the two surfaces:** after the grid's `+ в вкус` writer (L14762–14769)
  writes `gorodfm_taste`, call `window.GorodTasteCloud && GorodTasteCloud.refresh()`
  so a bubble for that artist (if present) lights up. Conversely, the cloud's
  toggle is the same `gorodfm_taste` array the grid's `inTaste()` reads — so
  after a cloud tap, re-render the grid (`render(input.value)`) so any matching
  card's button flips to "✓ в вкусе". Wire this by having the cloud dispatch a
  `window.dispatchEvent(new Event('gorodfm-taste-changed'))` after each write,
  and have `GorodMediateka` listen and re-`render(input.value)`. (Onboarding can
  optionally dispatch the same event from `syncTaste`, but that's out of scope.)
- Net: tapping a bubble = a real, durable, attributable "добавил(а) X в вкус"
  signal (the behavioral "почему"), distinct from "послушал". No transient
  filter overload, no reset affordance needed (there is no filter to reset).

---

## 7. Forked engine — tuned constants + lifecycle

Copy `measure / scatter / paint / step / makeBubble / relatedFor / ensureRoom /
spawnChildren / pulse / toggle / onTap` from the onboarding IIFE into
`GorodTasteCloud`, with these changes:

**Tuned physics (bounded ~360×190 box):**

| Constant | Onboarding | Cloud | Reason |
|---|---|---|---|
| `BASE` | 104 | **72** | smaller bubbles fit the bounded box |
| `MAX_BUBBLES` | 80 | **22** | keeps O(n²) repulsion cheap on mobile; aggressive recycle |
| repulsion `push` | 0.16 | **0.08** | smaller field → softer push, no thrash |
| damping | 0.965 | **0.98** | settles faster, less oscillation |
| wall bounce | −0.55 | **−0.42** | gentler bounce in a tight box |
| attraction `k` sel/unsel | .00020/.00008 | **.00016/.00007** | weaker pull to a near center |
| velocity clamp | 2.6 | **2.0** | keep — prevents runaway |

**Scoped `measure()`** (no `.onb-head`/`.onb-foot` coupling):
```js
function measure(){
  if(!field) return;
  var r = field.getBoundingClientRect();
  W = r.width; H = r.height;
  PAD_TOP = 8; PAD_BOTTOM = 8;   // small fixed insets; counter lives OUTSIDE the field
}
```
The counter + editorial note sit **outside** `.tcloud-field` (in `.tcloud-wrapper`),
so the field's whole height is usable band — no header/footer to dodge.

**Lifecycle gate — one idempotent predicate** (so reduced-motion + IO + focus
cannot fight each other):
```js
var REDUCEmq = window.matchMedia('(prefers-reduced-motion: reduce)');
var isVisible = false, focusPaused = false;
function motionOK(){ return !REDUCEmq.matches; }   // read LIVE, never cache
function requestRun(){
  if (motionOK() && isVisible && !focusPaused) start();
  else stop();
}
REDUCEmq.addEventListener('change', function(){
  field.classList.toggle('is-static', REDUCEmq.matches);
  if (REDUCEmq.matches) staticLayout();   // reflow to flex-wrap grid
  requestRun();
});
new IntersectionObserver(function(e){
  isVisible = e[0].isIntersecting; requestRun();
}, { threshold: 0, rootMargin: '200px 0px' }).observe(wrapper);
field.addEventListener('focusin', function(){ focusPaused = true; requestRun(); });
field.addEventListener('focusout', function(){ focusPaused = false; requestRun(); });
```

**Focus-freeze inside `step()`** (stable focus on a moving target — WCAG 2.4.7/
2.4.11): when `field.matches(':focus-within')`, zero the focused bubble's
velocity and skip its center-attraction so the focus ring holds still. (With the
`focusin`→`focusPaused`→`stop()` gate above, the loop is already paused on
focus; keep the in-`step` guard as a belt-and-suspenders for the resume tick.)

**Reduced-motion static fallback** = exact onboarding pattern (`.onb-field.is-static`
L2438–2448 → mirror as `.tcloud-field.is-static`): flex-wrap grid of the SAME
`<button aria-pressed>` bubbles, `position:relative; transform:none!important`.
Selection, counter, AND bloom all still work with zero rAF (bloom appends into the
flex wrap and items reflow). `matchMedia('change')` listened to (mid-session OS
toggle honored), not read once.

**`touch-action: manipulation`** on `.tcloud-field` and each `.tcloud-bubble`
(carry from L2296). NEVER `touch-action:none`; no `touchmove preventDefault` —
vertical page scroll falls through. Bubbles are click-only tap targets.

**Transform-only paint** (compositor): `paint()` writes `translate()+scale()`
only; transitions limited to box-shadow/filter/opacity (mirror L2326). `will-change:
transform` on bubbles (sparingly; the 22-cap keeps it bounded — optional: drop
`will-change` after a bubble settles velocity≈0).

---

## 8. a11y — toggle-button-group (NOT listbox)

- Container: `<div class="tcloud-field" id="tcloud-field" role="group"
  aria-label="Собери вкус — жанры и исполнители; тапни, чтобы добавить в волну">`.
  (Replaces the misleading L7913 label "…чтобы отфильтровать".)
- Each bubble: `<button type="button" aria-pressed="false" aria-label="Добавить
  в вкус: NAME">…</button>`. On select: `aria-pressed="true"`, label →
  `"В вкусе: NAME"`. **Do NOT** use `role=listbox`/`option`/`aria-multiselectable`
  — randomized animated positions make roving-tabindex arrow nav a lie, and the
  whole app standardizes on `aria-pressed` groups (home/discover/library chips).
- **One** `aria-live="polite" aria-atomic="true"` region = the visible
  `#tcloud-count` line. No hidden duplicate (avoid spoken/visible desync). It
  announces state row (§5.2) + per-tap receipt (§5.3) + bloom "+N похожих ниже".
- Tab order = DOM insertion order; NEVER reorder DOM for physics (transform-only,
  already the rule). Bloomed bubbles append (so they tab after their parent).
- `.tcloud-bubble:focus-visible { outline: 3px solid var(--accent-on-dark);
  outline-offset: 3px; }` (single-accent law; mirrors L2353).
- Keyboard: Tab to a bubble, Space/Enter toggles (native button). Focus-freeze
  (§7) keeps the ring stable.

---

## 9. Anti-slop compliance (every choice → a token)

| Visual | Token / rule (from ground map) |
|---|---|
| Selected ring | `0 0 0 2px var(--surface-0 #111318)`, `0 0 0 4px var(--brand-blue-light #5168FC)`, `0 6px 16px rgba(0,0,0,.4)` — single blue accent only (mirror L2357–2362, swap `--home-bg-base`→`--surface-0`) |
| Genre bubble bg | `radial-gradient(120% 120% at 30% 25%, #1b1d24, #121318)` + `1px rgba(255,255,255,.10)` (mirror `.onb-bubble--genre` L2338–2341) — flat, no multi-stop brand gradient |
| Artist bubble | `background-size:cover` + `::before` dark wash (mirror L2343–2351) — real photo, no SVG imagery |
| Wrapper surface | `background: rgba(255,255,255,.03)` + `1px solid var(--hairline)` + `border-radius: var(--r-lg 14px)` — flat surface law |
| Check badge | `background: var(--brand-blue-light)`, 20px circle, 12px svg (mirror `.onb-bubble-check` L2363–2376) |
| Counter text | `var(--text-sec)`; N highlight `var(--accent-on-dark #8094ff)`; met state `var(--success #34d399)` ONLY on the "стартовый вектор собран" word (matches onboarding `.onb-count.is-met`); accent blue stays single |
| Editorial note | `var(--text-ter)`, 11.5px |
| Font | `'Onest', sans-serif` everywhere (no Inter/Roboto/system-ui) |
| Focus rings | `var(--accent-on-dark)` |
| Transitions | `var(--t-fast)` box-shadow/filter/opacity |
| Labels | upright text inside circle (mirror `.onb-bubble-label`); **NO** rotated/scaleX 900-weight labels (GDS-19) |
| Float keyframe | **none** — motion comes from rAF physics, not a CSS float keyframe; reduced-motion freezes it |

ZERO cyan/violet/red/green-as-accent. Green (`--success`) appears only as the
onboarding-consistent "met" text color, not as an accent surface.

---

## 10. EXACT build steps

### 10.A HTML — replace L7913, keep the rest
**Replace** (L7913):
```html
<div class="media-bubbles" id="mediateka-bubbles" role="group" aria-label="Жанры — тапни шарик, чтобы отфильтровать"></div>
```
**with:**
```html
<div class="tcloud-wrapper" id="mediateka-tcloud">
  <div class="tcloud-field" id="tcloud-field" role="group"
       aria-label="Собери вкус — жанры и исполнители; тапни, чтобы добавить в волну"></div>
  <p class="tcloud-count" id="tcloud-count" aria-live="polite" aria-atomic="true">Собери вкус — тапни жанр или артиста</p>
  <p class="tcloud-editorial-note" id="tcloud-ed-note" hidden>Связи между артистами подобраны редакцией</p>
</div>
```
**Update the subtitle** (L7911) to match commit semantics:
```html
<p class="mediateka-sub">Тапни жанр или артиста — добавится в твой вкус, волна сразу подстроится.</p>
```
KEEP L7914–7919 (`#mediateka-input`, `#mediateka-grid`, `#mediateka-empty`) unchanged.

### 10.B CSS — add after the `.media-bubble` block (after L4370)
(Place AFTER `.mediateka-*` rules so `.tcloud-*` wins any cascade collision.)
```css
.tcloud-wrapper { position: relative; z-index: 1; margin: 2px 0 22px; padding: 16px;
  background: rgba(255,255,255,.03); border: 1px solid var(--hairline); border-radius: var(--r-lg); }
.tcloud-field { position: relative; min-height: 190px; overflow: hidden; touch-action: manipulation; }
@media (max-width: 560px){ .tcloud-field { min-height: 170px; } }
.tcloud-bubble { position: absolute; top:0; left:0; width: var(--size,72px); height: var(--size,72px);
  border-radius:50%; border:none; padding:0; display:flex; align-items:center; justify-content:center;
  text-align:center; cursor:pointer; color:#fff; font:700 clamp(11px,calc(var(--size)*0.16),17px)/1.05 'Onest',sans-serif;
  overflow:hidden; will-change:transform; -webkit-tap-highlight-color:transparent; touch-action:manipulation;
  transition: box-shadow var(--t-fast), filter var(--t-fast), opacity .35s ease;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.14), 0 8px 22px rgba(0,0,0,.42); }
.tcloud-bubble-label { position:relative; z-index:2; padding:0 7px; text-shadow:0 1px 6px rgba(0,0,0,.5); pointer-events:none; }
.tcloud-bubble--genre { background: radial-gradient(120% 120% at 30% 25%, #1b1d24, #121318); border:1px solid rgba(255,255,255,.10); }
.tcloud-bubble--artist { background-size:cover; background-position:center; }
.tcloud-bubble--artist::before { content:''; position:absolute; inset:0; z-index:1;
  background: linear-gradient(180deg, rgba(0,0,0,.05) 30%, rgba(0,0,0,.72) 100%); }
.tcloud-bubble:hover { filter: brightness(1.12); }
.tcloud-bubble:focus-visible { outline:3px solid var(--accent-on-dark); outline-offset:3px; }
.tcloud-bubble.is-selected { box-shadow: 0 0 0 2px var(--surface-0), 0 0 0 4px var(--brand-blue-light), 0 6px 16px rgba(0,0,0,.4); }
.tcloud-bubble-check { position:absolute; z-index:3; right:7px; bottom:7px; width:20px; height:20px; border-radius:50%;
  background: var(--brand-blue-light); display:flex; align-items:center; justify-content:center;
  opacity:0; transform:scale(.5); transition: opacity var(--t-fast), transform var(--t-fast); }
.tcloud-bubble.is-selected .tcloud-bubble-check { opacity:1; transform:scale(1); }
.tcloud-bubble-check svg { width:12px; height:12px; }
.tcloud-count { margin: 12px 0 0; font:600 14px/1.3 'Onest',sans-serif; color: var(--text-sec); }
.tcloud-count b, .tcloud-count .n { color: var(--accent-on-dark); font-weight:700; }
.tcloud-count.is-met .met { color: var(--success, #34d399); }
.tcloud-editorial-note { margin: 6px 0 0; font:400 11.5px/1.3 'Onest',sans-serif; color: var(--text-ter); }
/* reduced-motion / fallback: static flex-wrap grid, no physics (mirror .onb-field.is-static) */
.tcloud-field.is-static { display:flex; flex-wrap:wrap; align-content:flex-start; gap:12px; overflow:visible; }
.tcloud-field.is-static .tcloud-bubble { position:relative; transform:none !important; }
@media (prefers-reduced-motion: reduce){ .tcloud-bubble { transition: box-shadow var(--t-fast), opacity .2s; } }
```

### 10.C JS — lift shared seed (before onboarding IIFE, ~L11816)
Add `window.GorodTasteSeed` (§4), and refactor the onboarding IIFE's local
seed vars to read from it (pure no-op rename). **Re-grep `var DATA = [` to find
the exact onboarding line before editing.**

### 10.D JS — add `GorodTasteCloud` IIFE (after GorodMediateka, before `</script>` ~L14772)
- Mount on `#tcloud-field` (required; early-return if missing).
- Pull seed from `window.GorodTasteSeed`.
- Copy tuned engine (§7): `measure/scatter/paint/step/makeBubble/relatedFor/
  ensureRoom/spawnChildren/pulse/toggle/onTap` with §7 constants and the scoped
  `measure()`.
- `toggle()` writes canonical `gorodfm_taste` (genres uppercased, slice(0,8)),
  debounced 120ms, then `dispatchEvent('gorodfm-taste-changed')`.
- `refreshCount()` → updates `#tcloud-count` text per §5.2 ladder, toggles
  `.is-met` at N≥5, counts only directly-tapped (sel && root-or-tapped) bubbles,
  NOT bloomed children. (Track a `b.userTapped` flag set in `onTap`, so bloomed
  selected children — if a user later taps them — still count, but auto-spawned
  ones never inflate N until tapped.)
- aria-live receipts per §5.3 into `#tcloud-count`.
- Reveal `#tcloud-ed-note` (un-hide) the first time any bloom spawns.
- Init: read `gorodfm_taste`, pre-select matching root bubbles; set initial
  counter text.
- Lifecycle gate (§7): `matchMedia('change')` + IntersectionObserver(wrapper,
  rootMargin 200px) + focusin/out, all → `requestRun()`.
- Expose `window.GorodTasteCloud = { start, stop, requestRun, refresh }`.

### 10.E JS — edit GorodMediateka (L14713–14772) to drop the filter
- Delete `var activeGenre` (L14730), the bubble handler (L14756–14761), and the
  `activeGenre` clause in `render()` (L14744). The `bubbles` ref (L14728) +
  `renderBubbles()` (L14735–14741) become dead — **delete them** and remove the
  `renderBubbles()` call at L14771.
- After the grid `+ в вкус` write (L14766–14768), dispatch
  `window.dispatchEvent(new Event('gorodfm-taste-changed'))`.
- Add `window.addEventListener('gorodfm-taste-changed', function(){ render(input.value); });`
  so grid card buttons re-sync when the cloud writes. Guard against the grid's
  own dispatch causing a benign re-render (idempotent, fine).

---

## 11. Chrome verification checklist (probe, don't assume)

Open `designs/gorod-fm.html`, navigate `#/podborki`, scroll to Médiateка.

1. **Renders embedded:** cloud bubbles visible as a section ABOVE search+grid;
   Подборки carousel + AI-ask still visible above (no takeover). 0 console errors.
2. **Genres + artists present:** ≥12 genre bubbles + the 8 root artist photo
   bubbles; artist covers load (no broken-image) — DevTools Network: 200 for the
   8 `assets/gorod-fm/*.png` in §4.
3. **Tap writes real taste:** tap `Рок` → DevTools Console
   `JSON.parse(localStorage.getItem('gorodfm_taste'))` includes `"РОК"` (uppercased).
   Tap an artist → name appended as-is. Array length ≤8.
4. **Counter increments honestly:** counter shows `Твоя модель за N сигналов`,
   increments only on direct taps; N≥5 → "стартовый вектор собран" + `.is-met`.
   Bloomed children do NOT inflate N. Cap at 8.
5. **Bloom works + labeled:** tapping a genre spawns ≤4 artists; `#tcloud-ed-note`
   ("Связи… подобраны редакцией") un-hides. Field never exceeds 22 bubbles
   (recycle): tap several genres → count of `.tcloud-bubble` ≤ 22.
6. **Grid sync:** after a cloud tap on an artist that's in the grid, that card's
   button flips to "✓ в вкусе". After a grid "+ в вкус", a matching cloud bubble
   lights up (`GorodTasteCloud.refresh()`).
7. **No filter behavior:** tapping a bubble does NOT filter the grid; only the
   search input filters. (Old `activeGenre` gone.)
8. **Reduced-motion fallback:** emulate `prefers-reduced-motion: reduce` (DevTools
   Rendering tab) → cloud becomes a static flex-wrap grid, no motion; tapping
   still selects, counter still updates, bloom still appends. Toggle it back →
   physics resumes (live `matchMedia` listener).
9. **Off-screen pause:** scroll cloud out of view; in Performance/console confirm
   rAF stops (e.g. log in `step` gated, or check no paint churn). Scroll back →
   resumes (IntersectionObserver rootMargin pre-warm).
10. **Mobile scroll not trapped:** emulate a phone, vertical-swipe over a bubble →
    page scrolls (touch-action manipulation; no scroll hijack).
11. **a11y:** Tab reaches bubbles; Space/Enter toggles; focused bubble freezes
    (ring stable); screen reader (or DevTools Accessibility tree) shows
    `role=group` + `aria-pressed` flips + live counter announces count & "+N похожих".
12. **Onboarding unbroken:** navigate `#/onboarding` → original cloud still
    builds, blooms, counter gates CTA at 5, writes `gorodfm_taste`. (Confirms the
    `GorodTasteSeed` lift was a no-op.)
13. **Anti-slop:** inspect — single blue `#5168FC` accent only; no cyan/violet/
    red/green-as-accent; Onest font; flat surfaces; no rotated/scaleX labels.

---

## 12. Open questions (could not fully resolve from inputs)

1. **`MAX_BUBBLES_CLOUD` exact value.** Chose **22** (research said ~14–18 visible
   for a 380–440px box; this field is ~360×190, tighter, so 22 total with ≤4-wide
   blooms is a starting estimate). **Must be tuned in Chrome** (step 5) — if
   bubbles jitter/overlap, drop to 18; physics constants in §7 are likewise
   first-pass and need a live tuning pass in the actual bounded box.
2. **Counter as live region vs transient receipt blending.** §5.3 folds the
   per-tap receipt into the same `#tcloud-count` aria-live line that also shows
   the persistent state row. If the operator wants the state row to persist
   visually while still announcing the increment, a second visually-hidden
   live region would be needed — but that risks spoken/visible desync (a11y
   pitfall). Default keeps ONE region; revisit only if SR testing shows the
   state row vanishing too fast.
3. **Whether to also dispatch `gorodfm-taste-changed` from onboarding's
   `syncTaste`** so the cloud reflects onboarding edits live in the same session.
   Left OUT (out of scope, onboarding is a different route); the cloud re-reads
   storage on mount/IO-intersect anyway. Flag if cross-route live sync is wanted.
4. **Genre count source.** `GorodTasteSeed.DATA` has 12 genres; the old
   `GorodMediateka.GENRES` had 8. The cloud uses the 12-genre `DATA` (single
   source of truth). The old 8-genre `GENRES`/`ART` arrays in GorodMediateka are
   only used by the grid `render()` now — left intact (the grid still lists its
   18 `ART` artists by search). Confirm the operator is OK with the cloud showing
   genres (e.g. ДЖАЗ, ЛОФАЙ, ИНДИ, КЛАССИКА) that the grid's 18-artist `ART` set
   may not all cover — acceptable since the cloud builds *taste*, the grid is a
   separate searchable artist directory.
```
