# SPEC — Город ФМ Taste-Cloud: «ПОПУЛЯРНО СЕЙЧАС» + calm-over-time (не забивался на смерть)

- Product: Город ФМ — Moscow AI-radio web app
- File: `C:/Users/elbics/Desktop/design-project/designs/gorod-fm.html` (single-file SPA)
- Surface: `GorodTasteCloud` IIFE (lines 14861–15076) + `GorodTasteSeed` (lines 14781–14860) + CSS (lines 4364–4386) + HTML (lines 7929–7933)
- Status: build-ready, anchors re-grepped against the live file (2026-06-03)
- Design law: single blue accent `#5168FC` = `var(--brand-blue-light)` ONLY; Onest only; flat surfaces; behavioral honesty (scripted/demo data must be honestly labeled); green only as positive-delta semantic, never a brand accent.

---

## 0. Decisions (locked)

| Question | Decision |
|---|---|
| Which items are «популярно сейчас» | **6 items**, curated from the EXISTING seed (3 genres + 3 real-artist photos): `ЭЛЕКТРО`, `ХИП-ХОП`, `ПОП` (genres) + `Егор Крид`, `Макс Корж`, `Linkin Park` (artist photos). All already in `DATA` + have `REL`/`POOL` entries → bloom works, zero new assets. |
| How many | 6. Enough to feel like a real chart row; small enough that the marker stays special and the field stays calm. |
| Honest label | NOT a fake live metric. Editorial/demo framing: eyebrow reads **«ПОПУЛЯРНО СЕЙЧАС · в эфире Город ФМ»**. No listener counts, no «+340%». |
| Where they seed | **First** in `DATA` order so `scatter()` (index-angle based) clusters them centrally, AND we add `pop:true` to those 6 entries. No separate mini-section (keeps one calm float field + onboarding metaphor). |
| Visual distinction | **Option D (UI lens): eyebrow legend + monochrome top-left trend chip.** Hue-free (white-on-dark). Blue stays 100% reserved for selection. Optional one-time entrance pulse, reduced-motion gated. |
| Anti-clog model | **Hybrid A + C (UX lens): graduate-selected-out + capped float + «Обновить подборку» reshuffle**, with the counter line as the honest «где это» divider. `gorodfm_taste` is NEVER touched on graduation (view-only DOM removal). |
| MAX_BUBBLES | Drop **24 → 16** for calm density (graduation guarantees the cap is never reached by accumulated picks). |

---

## 1. POPULAR BUBBLES

### 1.1 Popular set (curated, honest)
Tag exactly these 6 with `pop: true` and **move them to the front** of `DATA` (front = central cluster after `scatter()`):

1. `ЭЛЕКТРО` (genre, hue 190)
2. `ХИП-ХОП` (genre, hue 258)
3. `ПОП` (genre, hue 330)
4. `Егор Крид` (artist photo, g: ПОП)
5. `Макс Корж` (artist photo, g: ХИП-ХОП)
6. `Linkin Park` (artist photo, g: РОК)

All 6 already exist in `DATA`, `REL`, `POOL`, `GENRE_HUE` → blooming and pre-selection are unaffected. This is editorial/demo data, labeled as such.

### 1.2 Visual distinction (every visual → a token)

| Element | Spec | Token / value | Why |
|---|---|---|---|
| Per-bubble trend chip | 18px circle, **top-left** (mirror of the existing bottom-right `.tcloud-bubble-check` at `left:7px/top:7px`) | bg `rgba(255,255,255,.10)`, border `1px rgba(255,255,255,.18)` | hue-free → does not collide with the blue selection accent |
| Chip glyph | monochrome up-trend SVG polyline (3-point ▲ line), same line-drawing vocabulary as the check polyline | `stroke #fff` @ ~88% opacity, NEVER blue, NEVER a flame/🔥/orange/red | meaning is hue-free; teaches off the eyebrow legend |
| Eyebrow legend | one static row under the field: 12px trend glyph + `ПОПУЛЯРНО СЕЙЧАС · в эфире Город ФМ` | `font: 600 11.5px 'Onest'; color: var(--text-ter)` | legend teaches the chip + honestly labels the source (design law) |
| Chip gating | depth-0 full-size bubbles ONLY | — | bloomed children (~30–38px) already have photo+gradient+label+check; a 5th overlay crowds them |
| Entrance pulse (optional) | reuse `pulse()` once on mount, `REDUCEmq.matches` gated, static no-op fallback | existing `el.animate` | additive sugar; conveys nothing to SR/reduced-motion so it is never the marker |
| a11y | accessible name carries the meaning, not color/icon | `aria-label = (pop ? 'Популярно сейчас. ' : '') + (sel ? 'В вкусе: ' : 'Добавить в вкус: ') + name` | WCAG icon-button: meaning lives in the programmatic name; glyph stays `aria-hidden` |

**Forbidden (pitfalls):** blue popular marker (overloads the one accent → indistinguishable from selected); flame/red/orange «hot» badge (violates single-accent law); size-only signal (size already encodes weight + depth); dashed-ring-only (reads as placeholder/disabled); a separate leading popular mini-section (fractures the calm float field).

---

## 2. ANTI-CLOG UX (не забивался на смерть)

Model in one sentence: **tapping a bubble blooms its related ones, you collect what you like, and each collected bubble "graduates" off the canvas into your taste — so exploring frees space rather than filling it.**

### 2.1 Graduate-selected-out (A)
- On select, the bubble keeps the blue ring + check as the receipt for **~700ms**.
- For **genres**, bloom the ≤4 related children FIRST (existing `spawnChildren`), so discovery is not cut.
- THEN animate the bubble small+fade and **splice it from `bubbles[]`** (DOM removal only).
- **CRITICAL: `writeTaste()` already persisted the pick to `gorodfm_taste` (called via `scheduleWrite()` inside `toggle()`). Graduation must run AFTER the write is committed and must NOT touch storage.** Sequence: `toggle()` → `scheduleWrite()` (120ms debounce) → bloom (genres) → ~700ms → splice DOM bubble.
- Counter becomes a persistent, tappable directional receipt: **`N в твоём вкусе →`** routing to `#/taste`. That single line IS the minimized «твой вкус vs поисследуй» divider — it answers "where did my pick go" without a second inline editor competing with `#/taste`.
- Reduced-motion: skip the float-away; brief static check then immediate removal.

### 2.2 Capped float + reshuffle (C)
- `MAX_BUBBLES` 24 → **16** (calm density). Keep `ensureRoom()` recycling oldest-untouched (`!sel && !expanded`).
- Add a quiet ghost control under the field: **«Обновить подборку ↻»** that swaps `!sel && !expanded` bubbles for a fresh batch (rotate in new POOL items + refresh the popular set). Must NOT reshuffle expanded parents or just-bloomed children (same predicate as `ensureRoom`).
- Because selected bubbles graduate OUT, the field never saturates with picks → the `idx === -1 → break` dead-end (where blooms/popular silently no-op) disappears. A 50th-session user sees the same calm ~16-bubble field as day one.

### 2.3 Honesty backbone (where added taste goes — preserve existing)
- The canvas is a VIEW; the store is `gorodfm_taste` (localStorage, JSON array, uncapped + verbatim).
- `writeTaste()` merges preserving non-cloud entries (grid «+ в вкус», onboarding-only names). A graduated bubble stays in `gorodfm_taste`.
- `preselectFromStorage()` / `refresh()` re-hydrate on return; the durable editable view is `#/taste`. Un-picking a graduated item happens on `#/taste` (canonical editor) — closes the loop.
- `gorodfm-taste-changed` stays debounced + `selfDispatch` guarded; reshuffle/graduation/popular-refresh must NOT spuriously fire it.

### 2.4 rAF + reduced-motion lifecycle (must stay intact)
- Graduation, popular pulse, and reshuffle all degrade in `.is-static` flex-wrap mode (`REDUCEmq`) and respect the `IntersectionObserver` `isVisible` pause — never animate/RAF while the wrapper is offscreen.
- Clear any per-bubble timers on graduation to avoid acting on a removed node.

---

## 3. EXACT BUILD STEPS (re-grepped anchors)

> All line numbers verified against the live file 2026-06-03. Re-grep each anchor before editing (file shifts as you add lines).

### STEP 1 — Seed: add `pop:true` + reorder popular-first (lines 14790–14811)
Re-grep anchor: `var DATA = [` (line 14790). Reorder so the 6 popular entries are first, and add `pop: true` to each:
```js
var DATA = [
  // ── ПОПУЛЯРНО СЕЙЧАС (editorial / "в эфире Город ФМ", seeded first → central) ──
  { t: 'ЭЛЕКТРО', hue: 190, w: 1.05, pop: true },
  { t: 'ХИП-ХОП', hue: 258, w: 1.2,  pop: true },
  { t: 'ПОП',     hue: 330, w: 1.15, pop: true },
  { t: 'Егор Крид',  img: 'home-featured-egor-krid.png',      w: 1.15, g: 'ПОП',     pop: true },
  { t: 'Макс Корж',  img: 'favs-artist-maks-korzh-base.png',  w: 1.1,  g: 'ХИП-ХОП', pop: true },
  { t: 'Linkin Park',img: 'favs-group-linkin-park-overlay.png', w: 1.1, g: 'РОК',    pop: true },
  // ── rest (unchanged) ──
  { t: 'РОК', hue: 2, w: 1.1 },
  { t: 'ДИСКО', hue: 292, w: 1.0 },
  { t: 'Дима Билан', img: 'favs-artist-dima-bilan-overlay.png', w: 1.0, g: 'ПОП' },
  { t: 'Martin Garrix', img: 'favs-dj-martin-garrix.png', w: 1.05, g: 'ЭЛЕКТРО' },
  { t: 'ЛОФАЙ', hue: 222, w: 0.95 },
  { t: 'ИНДИ', hue: 152, w: 0.95 },
  { t: 'Вадим Адамов', img: 'home-tile-vadim-adamov-base.png', w: 1.0, g: 'ЭЛЕКТРО' },
  { t: 'ДЖАЗ', hue: 36, w: 0.9 },
  { t: 'РЭП', hue: 278, w: 1.0 },
  { t: 'Мия Бойка', img: 'favs-artist-mia-boyka.png', w: 0.95, g: 'ПОП' },
  { t: 'R&B', hue: 320, w: 0.9 },
  { t: 'Рамиль', img: 'favs-artist-ramil.png', w: 0.95, g: 'ПОП' },
  { t: 'МЕТАЛЛ', hue: 210, w: 0.9 },
  { t: 'КЛАССИКА', hue: 45, w: 0.85 }
];
```
Note: onboarding copies the seed VERBATIM; reordering + a new optional `pop` key is safe (onboarding ignores unknown keys and is order-agnostic for its own bubble loop). Verify onboarding still mounts (STEP 8 checklist).

### STEP 2 — CSS: trend chip + eyebrow (after line 4379 `.tcloud-bubble-check svg`)
Re-grep anchor: `.tcloud-bubble-check svg { width: 12px; height: 12px; }` (line 4379). Insert after it:
```css
/* ПОПУЛЯРНО СЕЙЧАС — monochrome trend chip (top-left), hue-free; blue stays selection-only */
.tcloud-bubble-trend { position: absolute; z-index: 3; left: 7px; top: 7px; width: 18px; height: 18px; border-radius: 50%; background: rgba(255,255,255,.10); border: 1px solid rgba(255,255,255,.18); display: flex; align-items: center; justify-content: center; }
.tcloud-bubble-trend svg { width: 11px; height: 11px; }
.tcloud-pop-legend { display: flex; align-items: center; gap: 6px; margin: 10px 0 0; font: 600 11.5px/1.3 'Onest', sans-serif; color: var(--text-ter); }
.tcloud-pop-legend svg { width: 12px; height: 12px; flex: none; }
/* graduate-out (reduced-motion fallback removes instantly via JS) */
.tcloud-bubble.is-graduating { opacity: 0; transform: scale(.4) !important; transition: opacity .5s ease, transform .5s ease; pointer-events: none; }
/* reshuffle ghost control */
.tcloud-reshuffle { margin: 10px 0 0; background: transparent; border: 1px solid var(--hairline); border-radius: 999px; padding: 6px 14px; font: 600 12.5px 'Onest', sans-serif; color: var(--text-sec); cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: border-color var(--t-fast), color var(--t-fast); }
.tcloud-reshuffle:hover { border-color: var(--brand-blue-light); color: #fff; }
.tcloud-reshuffle:focus-visible { outline: 3px solid var(--accent-on-dark); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { .tcloud-bubble.is-graduating { transition: none; } }
```

### STEP 3 — HTML: eyebrow legend + reshuffle button (after line 7932)
Re-grep anchor: `<p class="tcloud-editorial-note" id="tcloud-ed-note" hidden>` (line 7932). Insert after it (still inside `#mediateka-tcloud`):
```html
<p class="tcloud-pop-legend" id="tcloud-pop-legend"><svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="4 16 10 10 14 14 20 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15 7 20 7 20 12" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>ПОПУЛЯРНО СЕЙЧАС · в эфире Город ФМ</p>
<button type="button" class="tcloud-reshuffle" id="tcloud-reshuffle"><svg viewBox="0 0 24 24" aria-hidden="true" width="14" height="14"><path d="M3 12a9 9 0 0 1 15-6.7L21 8M21 12a9 9 0 0 1-15 6.7L3 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Обновить подборку</button>
```

### STEP 4 — JS: read new DOM refs + lower MAX_BUBBLES (lines 14875, 14882–14883)
Re-grep anchor: `var BASE = 58, MAX_BUBBLES = 24;` (line 14875) → change to `MAX_BUBBLES = 16`.
Re-grep anchor: `var edNote  = document.getElementById('tcloud-ed-note');` (line 14882). Add after it:
```js
var reshuffleBtn = document.getElementById('tcloud-reshuffle');
var GRADUATE_MS = 700, GRADUATE_ANIM_MS = 500;
```

### STEP 5 — JS: render trend chip + a11y in makeBubble (lines 14961–14994)
Re-grep anchor: `el.setAttribute('aria-label', 'Добавить в вкус: ' + d.t);` (line 14973). Replace that line with the popular-aware label:
```js
el.setAttribute('aria-label', (d.pop ? 'Популярно сейчас. ' : '') + 'Добавить в вкус: ' + d.t);
```
Re-grep anchor: the `el.innerHTML = ...` block (lines 14974–14975). Append the trend chip ONLY for depth-0 popular bubbles. After the existing `innerHTML` assignment add:
```js
if (d.pop && depth === 0) {
  el.classList.add('tcloud-bubble--popular');
  el.insertAdjacentHTML('beforeend',
    '<span class="tcloud-bubble-trend" aria-hidden="true"><svg viewBox="0 0 24 24"><polyline points="4 16 10 10 14 14 20 7" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity="0.88"/><polyline points="15 7 20 7 20 12" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity="0.88"/></svg></span>');
  if (!REDUCEmq.matches) pulse(b); // one-time entrance sugar, gated
}
```
(Place this AFTER `var b = {...}` so `pulse(b)` has the object; `b` is created at line 14976.)
Re-grep anchor: `b.el.setAttribute('aria-label', (b.sel ? 'В вкусе: ' : 'Добавить в вкус: ') + b.d.t);` appears in `toggle()` (line 14928) and `setSelected()` (line 14053→14053? actual 15053). Update BOTH to prefix popular:
```js
b.el.setAttribute('aria-label', (b.d.pop ? 'Популярно сейчас. ' : '') + (b.sel ? 'В вкусе: ' : 'Добавить в вкус: ') + b.d.t);
```
(In `setSelected` the var is `b`; in `toggle` it is `b` too.)

### STEP 6 — JS: graduate-out after select/bloom (onTap, line 14932)
Re-grep anchor: `function onTap(b){ toggle(b); if (b.sel && !b.expanded) { b.expanded = true; spawnChildren(b); } }` (line 14932). Replace with:
```js
function onTap(b){
  var wasSel = b.sel;
  toggle(b);                                   // writes gorodfm_taste via scheduleWrite()
  if (b.sel && !b.expanded) { b.expanded = true; spawnChildren(b); } // bloom FIRST
  if (b.sel && !wasSel) { graduate(b); }        // only on newly-selected
}
function graduate(b){
  if (b._grad) return; b._grad = true;
  setTimeout(function () {                       // keep ring+check receipt ~700ms
    if (!b.el) return;
    var done = function () {
      var idx = bubbles.indexOf(b); if (idx !== -1) bubbles.splice(idx, 1);
      delete byName[b.d.t];
      if (b.el && b.el.parentNode) b.el.parentNode.removeChild(b.el);
      refreshCount();                            // updates "N в твоём вкусе →"
    };
    if (REDUCEmq.matches || !b.el.animate) { done(); return; }
    b.el.classList.add('is-graduating');
    setTimeout(done, GRADUATE_ANIM_MS);
  }, GRADUATE_MS);
}
```
**Note:** graduation removes the bubble from `bubbles[]` only — `gorodfm_taste` already holds it (written by `toggle→scheduleWrite`). `writeTaste()` filters by current `bubbles` cloudNames, so a graduated (removed) bubble is no longer a "cloud name" and is preserved as a non-cloud entry on subsequent writes. This is correct: it stays in storage verbatim.

### STEP 7 — JS: counter = directional receipt + reshuffle wiring (lines 14911–14922, 15070–15074)
Re-grep anchor: `function refreshCount(receipt){` (line 14911). Make the resting line directional + tappable. Replace the `n === 0 / n < 5 / else` block so the resting (non-receipt) state reads `N в твоём вкусе →`:
```js
function refreshCount(receipt){
  if (!countEl) return;
  if (settleTimer) { clearTimeout(settleTimer); settleTimer = 0; }
  var n = totalTaste(), disp = Math.min(n, 99), met = n >= 5, line;
  if (n === 0) line = 'Собери вкус — тапни жанр или артиста';
  else line = '<b class="n">' + disp + '</b> в твоём вкусе' + (met ? ' · <span class="met">стартовый вектор собран</span>' : ' · ещё ' + (5 - n) + ' до старта') + ' <span class="tc-go">→</span>';
  if (receipt) { line = receipt + ' · ' + line; }
  countEl.innerHTML = line;
  countEl.classList.toggle('is-met', met);
  if (receipt) { settleTimer = setTimeout(function () { settleTimer = 0; refreshCount(); }, 2400); }
}
function totalTaste(){ return readTaste().length; }  // graduated picks live in storage, not bubbles[]
```
Make `#tcloud-count` route to `#/taste` (it is the honest "where it went" divider). Re-grep anchor: the `window.GorodTasteCloud = {...}` export (line 15074). Before it add:
```js
if (countEl) { countEl.style.cursor = 'pointer'; countEl.setAttribute('role','link'); countEl.setAttribute('tabindex','0');
  var goTaste = function () { location.hash = '#/taste'; };
  countEl.addEventListener('click', goTaste);
  countEl.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); goTaste(); } });
}
function reshuffle(){
  var fresh = [], i;
  // cull !sel && !expanded (same predicate as ensureRoom), then re-seed from POOL/popular
  for (i = bubbles.length - 1; i >= 0; i--) {
    var b = bubbles[i];
    if (!b.sel && !b.expanded && !b.d.pop) {   // keep popular sticky-visible
      bubbles.splice(i, 1); delete byName[b.d.t];
      if (b.el && b.el.parentNode) b.el.parentNode.removeChild(b.el);
    }
  }
  // refill from a rotating pool of unused names (genre POOLs)
  var genres = Object.keys(POOL), tries = 0;
  while (bubbles.length < MAX_BUBBLES - 1 && tries < 60) {
    tries++;
    var g = genres[Math.floor(Math.random() * genres.length)];
    var pool = POOL[g] || [];
    var nm = pool[Math.floor(Math.random() * pool.length)];
    if (nm && !byName[nm]) { var nb = makeBubble({ t: nm, g: g }, 1, null); if (nb) fresh.push(nb); }
  }
  placed = false; if (isVisible) scatter(); requestRun();
}
if (reshuffleBtn) reshuffleBtn.addEventListener('click', reshuffle);
```
**Important:** `reshuffle()` and `graduate()` mutate `bubbles[]` but DO NOT call `scheduleWrite()` (no storage change → no `gorodfm-taste-changed` → grid does not needlessly re-render). They only re-scatter the view.

### STEP 8 — initial refreshCount uses storage count
Re-grep anchor: `refreshCount();` at init (line 15067). No change needed — `refreshCount` now reads `totalTaste()` from storage, so on return visits it correctly shows accumulated `N в твоём вкусе →` even though selected bubbles graduated out last session.

---

## 4. CHROME VERIFICATION CHECKLIST

Run `#/podborki` → scroll to Медиатека. Use chrome-devtools MCP (navigate, take_snapshot, list_console_messages, evaluate_script).

1. **Popular distinct + labeled** — 6 popular bubbles (`ЭЛЕКТРО`, `ХИП-ХОП`, `ПОП`, `Егор Крид`, `Макс Корж`, `Linkin Park`) each show a top-left monochrome ▲ chip; eyebrow row reads `ПОПУЛЯРНО СЕЙЧАС · в эфире Город ФМ`. They cluster centrally. `evaluate_script`: `document.querySelectorAll('.tcloud-bubble--popular .tcloud-bubble-trend').length === 6`.
2. **Single blue accent** — trend chip + eyebrow are white/neutral; the ONLY `#5168FC`/`--brand-blue-light` on the field is the selection ring + check. `evaluate_script`: confirm no blue in `.tcloud-bubble-trend` computed `borderColor`/`background` and no flame/red/orange anywhere.
3. **a11y** — `evaluate_script`: a popular unselected bubble `aria-label` starts with `Популярно сейчас. Добавить в вкус:`; after tap (before graduation) → `Популярно сейчас. В вкусе:`. Glyph spans are `aria-hidden`.
4. **Adding many taps stays calm** — tap 10–12 bubbles in sequence; each blooms (genres) then graduates out after ~700ms+500ms; the field never exceeds ~16 live bubbles. `evaluate_script` after the burst: `document.querySelectorAll('#tcloud-field .tcloud-bubble').length <= 16`. No overlap pile-up; physics stays smooth.
5. **Taste persists when a bubble leaves** — tap `ЭЛЕКТРО`; after it graduates, `evaluate_script`: `JSON.parse(localStorage.getItem('gorodfm_taste')).includes('ЭЛЕКТРО') === true`. Reload `#/podborki`; counter shows `N в твоём вкусе →` with the right N. Navigate `#/taste` — the picked items appear in the weight-cloud.
6. **Counter is a working link** — click `#tcloud-count` → routes to `#/taste`; keyboard Enter on it also routes.
7. **Reshuffle** — click «Обновить подборку»; unselected non-popular bubbles swap for fresh POOL names; popular bubbles + any expanded parents stay; `gorodfm_taste` unchanged (`evaluate_script` compare before/after). No `gorodfm-taste-changed` fired (grid not re-rendered).
8. **0 console errors** — `list_console_messages` clean across all the above.
9. **Reduced-motion** — emulate `prefers-reduced-motion: reduce`; field becomes static flex-wrap; popular chip + eyebrow still visible; graduation = instant removal (no float animation); no rAF running while wrapper offscreen (`IntersectionObserver` pause intact).
10. **Onboarding not broken** — navigate `#/onboarding`; bubble cloud still mounts and floats (seed reorder + new `pop` key did not regress it). 0 console errors.

---

## 5. RISKS / OPEN QUESTIONS

- **R1 ensureRoom dead-end** — fixed by construction: selected bubbles graduate OUT, so `bubbles[]` never saturates with `sel/expanded` items; the old `idx===-1 break` silent no-op path is no longer reachable in normal use. Reshuffle keeps fresh supply.
- **R2 popular stickiness vs room** — `reshuffle()` and `ensureRoom()` skip popular (`!b.d.pop`) so they stay visible; combined with graduation there is always an evictable slot (no permanent saturation). Verify item 4.
- **R3 timing race** — graduate runs AFTER `toggle→scheduleWrite` (120ms) and AFTER `spawnChildren`; `GRADUATE_MS=700` > 120ms write debounce, so storage is committed before DOM removal. `_grad` guard prevents double-graduation.
- **R4 onboarding seed sync** — onboarding copies `DATA` verbatim; reorder + extra `pop` key is order-agnostic and ignored there. Checklist item 10 gates it.
- **OQ1** — Should popular set rotate per session (pick 6 at random from a larger editorial list) or stay fixed? Spec uses a FIXED curated 6 for honesty + predictability. Rotation can be layered later via a `POPULAR_LIST` + random-6 at init.
- **OQ2** — Should graduated genres auto-bloom their children into the freed periphery (endless discovery) or leave the field calmer? Spec leaves children in place (they came from the bloom) and relies on reshuffle for fresh supply. Tunable.
- **OQ3** — `#/taste` is being redesigned separately as an editable weight-cloud; this spec routes the counter there but does not modify `#/taste`. Confirm the route + that un-pick lives there.

---

## COMPACT SUMMARY

- **Popular set (6, editorial/«в эфире Город ФМ», NOT a live metric):** `ЭЛЕКТРО`, `ХИП-ХОП`, `ПОП`, `Егор Крид`, `Макс Корж`, `Linkin Park` — all already in seed; tagged `pop:true`, moved first → central cluster.
- **Visual distinction (Option D, hue-free):** monochrome white top-left ▲ trend chip (`rgba(255,255,255,.10)` bg, `.18` border, `#fff`~88% glyph) on depth-0 popular bubbles + static eyebrow legend «ПОПУЛЯРНО СЕЙЧАС · в эфире Город ФМ» (`--text-ter`) + one-time reduced-motion-gated entrance pulse. Blue (`--brand-blue-light`) stays selection-only; a11y meaning in `aria-label` prefix «Популярно сейчас.».
- **Anti-clog model (Hybrid A+C):** graduate-selected-out (bloom→~700ms receipt→fade+splice DOM, storage untouched) + `MAX_BUBBLES` 24→16 + «Обновить подборку» reshuffle of `!sel && !expanded && !pop` bubbles. Counter becomes tappable `N в твоём вкусе →` routing to `#/taste` = honest "where it went" divider. `gorodfm_taste` stays uncapped/verbatim; graduated picks persist in storage and on `#/taste`.
- **Sections:** 0 Decisions · 1 Popular bubbles (set + visual + a11y) · 2 Anti-clog UX (graduate / cap+reshuffle / honesty backbone / rAF lifecycle) · 3 Exact build steps (8 re-grepped anchors) · 4 Chrome checklist (10) · 5 Risks/Open questions.
- **Open questions:** OQ1 fixed-vs-rotating popular set; OQ2 freed-slot auto-bloom vs calm; OQ3 confirm `#/taste` route + un-pick lives there (it is being redesigned separately).
- **File written:** `C:/Users/elbics/Desktop/design-project/docs/superpowers/SPEC-gorod-fm-cloud-popular-and-scale.md`
