# SPEC — «Облако вкуса»: weight-editable bubble cloud for #/taste

**Surface:** `section[data-page="taste"]` → `#taste-body` (Город ФМ AI-radio, `designs/gorod-fm.html`).
**Wedge:** transparency + EDITABLE taste + behavioral explainability. The taste vector is the moat — you SEE it and CHANGE it, and every change is honestly explained.
**Status:** build-ready. Implement directly in the single-file SPA. Re-grep every anchor before editing — anchors drift.

---

## 0. One-paragraph decision

Replace the `#taste-body` row stack with a **packed-bubble cloud where each interest's SIZE = its weight in your taste vector**, reusing the existing `.onb-bubble` / `.tcloud-bubble` visual language and force-layout engine. The chosen re-weight interaction is **tap-a-bubble → it focuses and shows an inline `−  ◦◦●◦◦  +` stepper; − / + steps the weight one notch** (5 discrete levels), the bubble's radius animates, and the existing collision solver re-flows the neighbours so you literally watch your taste re-balance. This is the "interesting" payoff the operator asked for ("настраивать размеры интересов"), kept honest and accessible. **Free-drag-to-resize is rejected** (fights the rAF collision solver, fails WCAG single-pointer precision, inaccessible). Each bubble is a `role="slider"` so the SAME notch is reachable by keyboard arrows and announced by screen readers; the `−`/`+` buttons are the explicit accessible control on every modality. **Critical wedge fix shipped with it:** weights now persist to a new `gorodfm_weights` store (today they are re-derived from pick-order every load and edits die on reload — that is "control theater" and it bleeds the wedge). Size encodes weight by **AREA (`diameter ∝ √weight`)** so a 2× weight looks 2× bigger, never 4×; the exact value rides as an always-visible label so perception never has to read area precisely. Unmeasured pick-order/DEFAULT weights stop wearing a precise "%" costume — they carry a `демо`/`по прослушиванию` provenance chip instead, and only a weight YOU set shows an exact number.

---

## 1. INTERACTION MODEL

### 1.1 Primary gesture — "steppy resize" (tap → focus → notch)

| Step | Behaviour |
|---|---|
| Tap / click / Enter on a bubble | Bubble **focuses**: lifts (`scale(1.06)`), siblings dim to `filter:brightness(.82)`, an inline control strip appears anchored under the bubble: `[ − ]  ◦◦●◦◦  [ + ]  [📌 закрепить]`. The pips are the readout — NOT a free-form %. |
| `−` / `+` | Step weight by **one notch** (see §3.2 levels). `b.r` recomputes from `√weight`; `paint()` + `step()` re-flow neighbours. On step: `src='you'`, blue ring, **persist** (§3), `TwinrWave.bump()` once, `renderSponsor()`, `updateVectorSr()`, `GorodSaved.refreshStreak()`. |
| Tap the bubble again / tap empty field / `Esc` | Defocus: strip hides, siblings restore. |
| 📌 pin | Toggles `r.pinned` (existing logic) → solid-blue **hairline ring** distinct from selected glow; pinned bubbles are excluded from the field's `ensureRoom` eviction. |

There is **no continuous drag-resize.** The "size changes under your hand" feeling comes from the notch animating the radius + the physics re-settling — honest motion (physics, not decoration), one `bump()` per committed step (never per-pixel jitter = theatrical).

### 1.2 Modality matrix (all paths drive ONE setter `setWeight(group, name, level)`)

| Modality | Mechanic |
|---|---|
| **Desktop pointer** | Tap bubble → focus → click `−`/`+`. |
| **Touch** | Same. Bubble core ≥ 44px hittable; `−`/`+` buttons 44×44 with `::before{inset:-9px}` expanded hit area (reuse `.taste-ctrl` pattern). |
| **Keyboard** | Tab to bubble (`tabindex=0`, `role=slider`). `→`/`↑` = +1 notch, `←`/`↓` = −1, `Home` = level 0, `End` = max, `PageUp`/`PageDown` = ±2 notches, `Enter`/`Space` = open the pin/remove menu (the focus strip). Focus ring = existing `:focus-visible{outline:3px solid var(--accent-on-dark)}`. |
| **Wheel (desktop only)** | Wheel-resize ONLY when the bubble is focused or hovered; listener scoped to the bubble with `{passive:false}` + `preventDefault()` so an idle wheel over the cloud still scrolls the page. Low priority — ship `−`/`+` + arrows first; wheel is additive. |

### 1.3 Static / reduced-motion fallback (REQUIRED)

`@media (prefers-reduced-motion: reduce)` AND a persistent **«Списком»** toggle in the cloud header:
- Field gets `.tcloud-field.is-static` (existing): `display:flex; flex-wrap:wrap; transform:none !important` — bubbles laid out deterministically (descending weight), **no float, no spring**. Size still encodes weight (it is information, not decoration).
- In static mode the focus strip still works; OR fall back to the current `.taste-row` editor (kept in the file, behind the «Списком» toggle) which already has `−`/`+` + bar + `%`. **Never make the cloud the only editor.**
- Kill the bouncy spring: in reduced-motion, bubble radius transitions = `transition: none` (snap) or ≤120ms ease, never the overshoot cubic-bezier.

---

## 2. LAYOUT

### 2.1 Packed cloud, one GROUP at a time (segmented control)

- **Do NOT mix ~17 bubbles from 4 groups in one field** (area comparison only honest WITHIN a category; >30 bubbles overlap). Add a segmented control above the field: **`Жанры · Артисты · Настроения · Эпохи`** (4 chips, single blue selected state, Onest). One group's bubbles render at a time, max 6 (existing per-group cap at L13039). `MAX_BUBBLES` stays 16 — never exceeded with a 6-cap.
- Reuse the discover physics verbatim (`makeBubble`/`scatter`/`step`/`paint`, L15055–15134): force-to-center + pairwise push + bounce. Field box `min-height:280px` (existing `.tcloud-field`).

### 2.2 Genre vs artist distinction (reuse existing classes — zero new visual language)

- Genre bubble = `.tcloud-bubble--genre` (flat radial dark gradient `#1b1d24→#121318`, hairline border). Names UPPERCASE per the `gorodfm_taste` genre convention.
- Artist bubble = `.tcloud-bubble--artist` (photo-fill via `background-image` from `GorodTasteSeed.ASSET` when available, `::before` dark wash for label legibility). Falls back to genre-style dark fill if no photo asset matches the name.
- Selected/your-set ring, check, focus = identical to discover (`.is-selected`, `.tcloud-bubble-check`, `:focus-visible`). Provenance chip (§4.1) reuses the trend-chip slot pattern (`.tcloud-bubble-trend`, top-left, monochrome) so blue stays selection-only.

### 2.3 Size → weight mapping (HONEST PERCEPTION — hard gate)

- **Encode by AREA, not radius:** `wgt = Math.sqrt(level / MAXLEVEL)`, `size = Math.round(BASE_T * wgt)`, `BASE_T ≈ 132` (so max bubble ≈ 132px, min readable ≈ 0.45×132 ≈ 60px ≥ 44px touch floor). `b.r = size/2` for the collision solver. A level-4 interest has 2× the AREA of a level-1, never 2× the diameter.
- **Always print the value.** The label inside the bubble = the interest name; a small `%` or `n/5` chip is shown for `src='you'` bubbles (you set it → the number is true). For `демо`/`heard` bubbles, NO number — the provenance chip carries meaning (§4.1). Never let a fabricated value wear a precise costume.
- Smallest bubble (rejected/level-0-ish) clamps to a readable min (60px) so it stays tappable; `+` on a rejected bubble is locked (§4.3).

### 2.4 Placement relative to existing blocks (KEEP ALL)

Order inside `.taste-stage` is unchanged except `#taste-body` content:
`taste-hero` → `ctx-strip` → **`#taste-body` (now: segmented control + cloud + «Списком» toggle + reject-card)** → `taste-sponsor` → `taste-streak` → `taste-saved` → `taste-foot`.
The sponsor card, streak, and Сохранённое accordion are untouched and keep re-rendering on edit.

---

## 3. PERSISTENCE (THE WEDGE — do this FIRST)

### 3.1 New store `gorodfm_weights`

```
gorodfm_weights = { "<name>": { w: <0..100>, src: "you" } }
```
- Keyed by the SAME name string used in `gorodfm_taste` (genres UPPERCASE, artists mixed-case).
- ONLY `src:'you'` entries are written here — i.e. weights the user actually set. We never persist a fabricated pick-order weight as if measured.
- `gorodfm_taste` (the name array) stays the **membership source of truth**. `gorodfm_weights` is additive and per-name. Removing a name from `gorodfm_taste` (via onboarding ✕) leaves a dangling weight entry — harmless; `seed()` only applies a weight to a facet that still exists.

### 3.2 Weight levels (categorical, not 100-point false precision)

5 notches mapped to stored `w`: **L0=8, L1=28, L2=48, L3=72, L4=92** (`MAXLEVEL=4`). Helper `wToLevel(w)` = nearest notch; `levelToW(l)` = the table. `−`/`+` move ±1 level. Stored `w` keeps the existing 0–100 contract so `matchSponsor()` and `updateVectorSr()` need ZERO changes.

### 3.3 `seed()` merge (the critical refactor — at L13028)

After the existing DEFAULT clone + pick-order baseline + `applyRejections()`, add a final pass:
```
// merge persisted user weights OVER pick-order/DEFAULT, and tag provenance
var saved = JSON.parse(localStorage.getItem('gorodfm_weights') || '{}');
Object.keys(data).forEach(function (g) {
  data[g].forEach(function (r) {
    if (r.rej) { r.src = 'rejected'; return; }              // rejection wins
    var key = (g === 'Жанры') ? r.n.toUpperCase() : r.n;
    if (saved[key]) { r.w = saved[key].w; r.src = 'you'; }   // user-set survives reload
    else if (window.TwinrModel.hasRealSignal && window.TwinrModel.hasRealSignal(r.n)) r.src = 'heard';
    else r.src = 'demo';                                     // DEFAULT / unmeasured pick-order
  });
});
```
Order is load-bearing: clone DEFAULT → pick-order baseline → `applyRejections()` → weight-merge. Never reorder.

### 3.4 `persistWeight(group, name, w)` — called by `setWeight`

```
var key = (group === 'Жанры') ? name.toUpperCase() : name;
var m = JSON.parse(localStorage.getItem('gorodfm_weights') || '{}');
m[key] = { w: w, src: 'you' };
localStorage.setItem('gorodfm_weights', JSON.stringify(m));
window.dispatchEvent(new Event('gorodfm-taste-changed'));   // sync with discover cloud
```
A rejected facet's `+` does NOT call this (locked, §4.3).

### 3.5 Compatibility with onboarding / discover writers (DO NOT BREAK)

- Onboarding `.onb-vec-row` `syncTaste()` (L12495) keeps writing the **name array** to `gorodfm_taste`. It does not write weights. After onboarding, those names appear in #/taste as `src:'demo'`/`heard` until the user resizes one → then `src:'you'`. (Optional polish, not required: have onboarding `syncTaste` also seed `gorodfm_weights[name]={w:r.weight,src:'you'}` so the onboarding edit carries through — but only if it does not break the array format. Default: leave onboarding writing names only.)
- Discover `GorodTasteCloud.writeTaste()` (L14968) keeps writing names uncapped/verbatim and dispatching `gorodfm-taste-changed`. #/taste must **listen** for that event and re-`seed()`+re-render if built, so building in discover live-updates the cloud. New names arrive as `demo`/`heard`, never fabricated `you`.
- `GorodProfile` / `GorodRecap` read `gorodfm_taste` + `gorodfm_rejected` only — unaffected. (Optional: Profile can later read `gorodfm_weights` for the same provenance chips; not required for this build.)

---

## 4. HONESTY

### 4.1 Provenance — three honest states (the cloud's killer feature)

| `src` | Meaning | Bubble treatment | Number? |
|---|---|---|---|
| `you` | you sized it | solid **blue hairline ring** (the only ringed state besides selected) | YES — exact `%`/`n/5` (you set it, it's true) |
| `heard` | from real listening signal | flat dark, normal hairline, tiny chip «по прослушиванию» | NO number |
| `demo` | DEFAULT / unmeasured pick-order, no real signal | flat dark + small **«демо»** pill (reuse trend-chip slot) | NO number |
| `rejected` | argued-down in player | locked, struck, min-size (§4.3) | NO |

Empty / zero-real-signal state: cloud header reads **«Пока это пример — собери вкус, и облако станет твоим»** (mirrors discover's «Собери вкус» empty state). First resize retires the `демо` pill for that facet.

### 4.2 The one truthful line per resize (behavioral, never marketing)

Shown in `#taste-delta` (`aria-live="polite"`) on every committed step. Pattern = *facet ↑/↓ → concrete consequence in what gets played + the trade-off named*:
- Up: **«Арена-рок — больше в волне. Чаще буду ставить рок-гимны; реже — спокойное.»**
- Down: **«Электро-поп — меньше. Реже в эфире; вместо него поднимается то, что выше.»**
Never «тебе понравится». Always what the SYSTEM does. (Upgrades the onboarding bare-number receipt `«87 → 93 % — пересчитал»` to a consequence.)

### 4.3 Rejected facets — locked, struck, min-size, can't inflate

- Render IN the cloud at min size (the `w≤12` clamp at L13052 maps to L0), desaturated wash + a small **lock glyph** where the check sits, label struck (reuse `.taste-row.is-rejected` semantics in bubble form).
- `+` / `↑` / wheel on a rejected bubble does NOT inflate. It surfaces: **«Эту грань ты оспорил на плеере. Вернуть можно там же — «почему?» → «вернуть».»** No silent backdoor that contradicts the player's provenance.
- Keep the dedicated **«Отклонено в плеере»** card below the cloud verbatim (L13105–13113) — cloud shows rejections in context (small+locked), card shows the full provenance list. Two views, one truth.

### 4.4 Wave + sponsor stay believable

- **Wave:** one proportional `TwinrWave.bump()` per committed step (existing). Optional: route a sustained re-weight through `TwinrWave.setContext()` ONLY when the dominant facet of the group changes — ambient character shifts only when your actual top interest shifts. Theatrical = react to every pixel; honest = react once to the commit.
- **Sponsor:** `matchSponsor()` (L13131) re-scores live on the same `r.w` values — leave it untouched. Down-weighting a matched facet visibly demotes/changes the ad = proof the control is real (the anti-theater test). Keep «реклама будет реже и точнее» (L13167).

### 4.5 DEFAULT / sponsor demo labeling

`DEFAULT` (L13017) and `SPONSORS` (L13123) are scripted → MUST be honestly labeled. DEFAULT facets carry the `демо` pill (§4.1). The sponsor card already shows «Спонсор · по вкусу» badge + behavioral «Почему вам». In a sized cloud a fabricated big bubble would scream — so the cloud is the BEST place to be honest; the `демо` pill makes it unavoidable.

### 4.6 One story across the three taste surfaces

| Surface | Verb | Size means | Writes |
|---|---|---|---|
| Onboarding build (`.onb-bubble`) | **собери** | n/a (selection) | `gorodfm_taste` names |
| Discover build (`.tcloud-bubble`, #/podborki) | **собери** | popularity / relatedness (system-shown: «ПОПУЛЯРНО СЕЙЧАС») | `gorodfm_taste` names |
| #/taste cloud (NEW) | **настрой** | YOUR weight / conviction | `gorodfm_taste` + `gorodfm_weights` |

Contract: same store, same `gorodfm-taste-changed` event, same 4 provenance chips. Each surface states what size means via a one-line legend so discover-popularity never masquerades as taste-weight.

---

## 5. A11Y (exact)

- Field wrapper: `role="group" aria-label="Размеры интересов — настрой вес каждого"`. NOT listbox (single-select semantics would mislead).
- Each bubble: `role="slider"`, `tabindex="0"`, `aria-valuemin="0" aria-valuemax="4" aria-valuenow="<level>"`, `aria-valuetext="<name>: вес <level> из 4"`, `aria-labelledby` → its `.tcloud-bubble-label` id (visible-text label; satisfies WCAG 2.5.3). **Omit `aria-orientation`** (resize is radial, neither horizontal nor vertical — asserting either is a lie).
- DOM order is **weight-stable** (e.g. descending weight or alphabetical) and NEVER reorders on resize — only `transform` reflows visually. Tab/SR reading order follows DOM, not float position (critical correctness rule).
- Keyboard map = §1.2. Slider role auto-announces `aria-valuetext` on arrow change (do NOT also push to a live region → double-announce).
- `−`/`+` buttons (focus is on the button, not the slider): update a single `role="status" aria-live="polite"` node ONLY on button-path edits (`«Арена-рок: вес 3 из 4»`), never on arrow/wheel edits.
- Rejected bubble: `aria-disabled="true"` (keep focusable so SR hears WHY), arrows/wheel no-op, `aria-valuetext="<name>: отклонено в плеере — заморожено. Вернуть можно в плеере."`.
- Keep `#taste-vector-sr` (role=img) refreshed by `updateVectorSr()` as the digest vector; keep `#taste-wave` canvas `aria-hidden`.
- `prefers-reduced-motion` = §1.3.

---

## 6. ANTI-SLOP (every choice → token)

| Element | Token |
|---|---|
| Selected / your-set ring | `--brand-blue-light` (#5168FC) |
| Focus ring | `--accent-on-dark` (#8094ff), `3px` outline, `offset 3px` |
| Genre bubble fill | flat radial `#1b1d24→#121318` (existing `.tcloud-bubble--genre`) |
| Artist wash | existing `::before` dark gradient |
| Surfaces | `rgba(255,255,255,.03/.04)` + `1px var(--hairline)` |
| Pip filled / empty | `--brand-blue-light` / `rgba(255,255,255,.16)` |
| Provenance chip | monochrome `rgba(255,255,255,.10)` + `.18` border (NO color) |
| Positive delta (recap only) | `--success` #34d399 — NOT used here as accent |
| Font | Onest only |
| Radii / motion | `--r-lg`, `--t-fast`, `--t-mid` |

Hard gates: single blue accent, zero cyan/violet/red, flat surfaces, NO multi-stop gradient backgrounds, NO rotated/scaleX-900 labels (GDS-19), behavioral honesty over vanity numbers. Bubbles use flat dark fill + blue RING (sidesteps the `.taste-bar-fill` blue→accent gradient question entirely).

---

## 7. EXACT BUILD STEPS (re-grep anchors first; current values shown)

1. **HTML — `#taste-body` (L9476).** Inject from JS: a `.tcloud-segctrl` (4 group chips), `.tcloud-field` wrapper `role="group"`, the «Списком» toggle, and (in static/list mode) the legacy `.taste-row` container. Keep the `<div id="taste-body">` shell; render() fills it.
2. **CSS (after `.tcloud-bubble` block, L4413).** Add `.taste-cloud-*` helpers ONLY where reuse is impossible: `.tcloud-segctrl` (pill chips), `.tcloud-focus-strip` (`−`/pips/`+`/pin, absolute under focused bubble), `.tcloud-bubble--rejected` (grayscale + lock), `.tcloud-bubble--you` (blue hairline ring distinct from selected glow), `.tcloud-prov-pill` (reuse trend-chip styling). Reduced-motion: snap radius transition. Reuse `.tcloud-bubble`, `--genre/--artist`, `.is-selected`, `-check`, `:focus-visible`, `.is-static` as-is.
3. **JS `GorodTaste` (L13016–13186) refactor:**
   - `seed()` (L13028): add the §3.3 weight-merge + provenance tagging pass.
   - Add `levelToW`/`wToLevel`/`setWeight(group,name,level)` + `persistWeight` (§3.2–3.4). `setWeight` updates `r.w`, `r.src='you'`, persists, re-paints the bubble radius, re-runs physics, calls `TwinrWave.bump()`, `renderSponsor()`, `updateVectorSr()`, `GorodSaved.refreshStreak()`, updates `#taste-delta` (§4.2).
   - Replace `rowHtml`/`render()` body (L13058–13102) with cloud builder forked from `makeBubble`/`scatter`/`step`/`paint` (L15055–15134): per-group bubbles, `size` from `√(level/4)*BASE_T`, `role=slider` + ARIA (§5), tap→focus strip, keyboard handler. Keep the click→`setWeight` delegation. **Preserve** `applyRejections` (L13044, unchanged), `updateVectorSr` (L13070, unchanged), the reject-card (L13105–13113, unchanged), `matchSponsor`/`renderSponsor`/`wireSponsor` (L13131–13174, unchanged), `onRoute` (L13176).
   - Add `window.addEventListener('gorodfm-taste-changed', ...)` → if `built`, re-`seed()`+re-render (sync with discover/onboarding).
   - Keep the legacy `.taste-row` render available behind the «Списком» toggle and as the reduced-motion editor.
4. **Do NOT touch:** onboarding `Model` `syncTaste` (L12495), `.onb-vec-row` handler (L12477), `GorodTasteCloud` (L14942+), `GorodProfile`, `GorodRecap`, `GorodSaved`, `TwinrModel.REJ_LABELS`/`hasRealSignal`.

### 7.1 Chrome verification checklist (`:8770`, `?v=N` cache-bust)

- [ ] Bubbles render sized by weight; level-4 ≈ 2× AREA of level-1 (not 4×).
- [ ] Tap bubble → focus strip; `−`/`+` steps size; neighbours re-flow.
- [ ] Resize → reload → size PERSISTS (gorodfm_weights written; `seed()` restores).
- [ ] `src='you'` bubble shows exact value + blue hairline ring; `demo` shows «демо» pill, no number.
- [ ] Rejected facet = small, struck, locked; `+` shows «верни на плеере», does NOT inflate; reject-card still lists it.
- [ ] Wave bumps once per step (not per pixel); sponsor re-matches when a matched facet is down-weighted.
- [ ] SR: bubble announces `role=slider` + `aria-valuetext`; button-path edit announces once via `role=status`; `#taste-vector-sr` digest correct.
- [ ] Keyboard: Tab→bubble, arrows/Home/End step; focus ring = accent-on-dark.
- [ ] `prefers-reduced-motion` (DevTools rendering emulate) → static flex-wrap, no float/spring; «Списком» toggle gives row editor.
- [ ] Segmented control switches groups; max 6 per group; ≤16 bubbles.
- [ ] Сохранённое accordion + streak still render and update on edit.
- [ ] Onboarding `.onb-vec-row` ±/✕ and discover cloud still write `gorodfm_taste` and live-sync into #/taste; building in discover updates the cloud.
- [ ] 0 console errors; `:8770` alive.

---

## 8. UNRESOLVED (flag to operator, do not block build)

1. **Onboarding weight carry-through:** should onboarding `.onb-vec-row` edits also seed `gorodfm_weights` (so a weight set during onboarding survives into #/taste as `src:'you'`)? Default in this spec = NO (onboarding writes names only; weights become `you` only when set on #/taste). Cheap to add later.
2. **Group switch vs all-at-once:** spec picks segmented control (one group at a time) for honest within-category area comparison. If the operator prefers ONE mixed cloud for spectacle, color-code is forbidden (single accent) — distinguish only by genre/artist fill, and accept that cross-group area comparison is less rigorous.
3. **`hasRealSignal` coverage:** the `heard` provenance depends on `TwinrModel.hasRealSignal(name)` actually returning real-signal truth for facet names; if it is itself scripted, `heard` collapses into `demo` honestly (acceptable — never invent a `heard` we can't back).
