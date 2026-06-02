# GOROD-051 — Контекстные старты (Утро/Работа/Вечер) — Build Spec

> Auto-captured 2026-06-02 from research-workflow wpxkf0v52 (Karpathy 2-agent research + synthesis). BUILD-READY. New window.GorodContext module on #/taste (additive) + backward-compatible TwinrWave.setContext. Does NOT trigger gated 045 (home pixel-perfect untouched). Implement per this spec.

---

All anchors confirmed. The two inputs are accurate against the real file. One conflict to flag: the player-track-reason `span` is shared and gets overwritten by the existing player code (line 13479 on track change). I have everything needed to produce the unified spec.

---

# GOROD-051 — Контекстные старты (Утро/Работа/Вечер) — Unified Implementation Spec

**Module:** `window.GorodContext` (new decoupled trailing-script IIFE) + a backward-compatible `setContext` extension to the existing `window.TwinrWave`. Single-file, atomic, additive.

**Target file:** `designs/gorod-fm.html` (verified — all line anchors below confirmed against the real 13.8k-line file as of this read).

---

## 0. Inputs reconciliation (resolved conflicts — read first)

Both inputs (RESEARCH + grounded draft) agree on the core mechanic. Where they diverge or where I verified against the real file, the resolution is binding:

| # | Conflict / ambiguity | Resolution (binding) | Why |
|---|---|---|---|
| **C1** | RESEARCH says **3 contexts** (Утро/Работа/Вечер, no carousel); grounded draft ships **4 time-contexts** (+ Ночь) **+ 2 activities** (Тренировка/Дорога). | **Ship the draft's 4 time + 2 activity set**, but in **two visually distinct rows** (time-row = mutually-exclusive segmented; activity-row = optional toggle modifier). | The audit (§6) names Утро/Работа/Вечер; Ночь is a natural completion of the 24h `getHours()` partition (the default function MUST return *something* for 23–05 — leaving a 6-hour dead zone would be a bug). Activities are explicitly tagged "поверх времени / не авто-дефолт", so they don't reintroduce the carousel CTR-cliff or choice-paralysis the RESEARCH warns about — they're a secondary, opt-in layer. Both rows are **fully visible** (no carousel), honoring RESEARCH's NN/g guidance. |
| **C2** | RESEARCH labels the work context **«Работа»**; grounded draft labels it **«День / Работа»** key `day`. | Use key **`day`**, label **«День»**, with the param strip carrying the work framing. Section heading stays "контекст" not "работа". | Key `day` is part of a clean 4-way clock partition; "День" reads as a time-of-day sibling to Утро/Вечер/Ночь (consistent mental model), while the behavioral «почему» supplies the "фон для работы" intent. |
| **C3** | RESEARCH proposes a **± nudge** on BPM/energy (Endel-slider spirit) + optional `setEnergy`. | **Defer ± nudge / `setEnergy` to v2.** v1 ships preset contexts only. `setContext` is the sole new TwinrWave method. | Draft marks `setEnergy` "НЕ обязателен для v1"; the editable-wedge is already satisfied in v1 by **override** (one tap to any context) + **persistence** (`gorodfm_context`). Adding a live numeric slider is additive on top later without touching this spec's surface. The `setContext` map keeps a clean seam for it. |
| **C4** | Placement: RESEARCH says "pinned **above** the TwinrWave"; grounded draft says insert **after** `.taste-hero` (which *contains* the wave) and **before** `.taste-body`. | **Draft wins: insert after `</header>` of `.taste-hero` (line 9632), before `.taste-body` (line 9634).** | Verified: the wave canvas `#taste-wave` lives *inside* `.taste-hero`. "Above the wave" would mean inside the pixel-flexible hero but would crowd the hero's existing actions (share/sonify/profile/delta at 9616–9630). Placing the strip immediately *after* the hero keeps the wave visually adjacent (scroll-coupled) while staying in clean flow — satisfies RESEARCH's intent ("the change lands on the surface that shows the wave") without restructuring the hero. |
| **C5** | Draft writes the active-context readout into the **shared** `#player-track-reason > span`. | **Allowed, but it is a transient mirror, not the source of truth.** The durable, always-correct readout is the new **`#ctx-why`** (role=status). The player-reason mirror is best-effort and **will be overwritten** by the existing player on the next track change (verified: line 13478–13479 `rs.innerHTML = t.pill || t.reason`). | The player-reason span is owned by the player IIFE. Co-opting it permanently would fight that code. Spec uses it as an *opportunistic* "current context" echo on the now-playing chrome, and accepts it's ephemeral — `#ctx-why` carries the authoritative, persistent explanation on `#/taste`. Documented so the implementer doesn't "fix" the overwrite as a bug. |
| **C6** | Placement variants A / B / C. | **Ship VARIANT A only in v1.** B (floating home pill) and C (both) are explicitly out of scope; the public `window.GorodContext` API (`suggest`/`apply`) is exported so B can be added later with zero refactor. | Draft: "НАЧАТЬ С A only … A самодостаточен". A alone closes "контекст-ДО-запуска" and never touches pixel-perfect home. |
| **C7** | Honesty floor: when to actually drive the wave. | **Bind to the draft's rule:** on `#/taste` load, if a saved choice exists AND `isToday(ts)` → apply `setContext` + reflect. Else → **suggest only** (highlight `defaultCtx()` chip via `data-now`, show `#ctx-hint`), do **not** drive the wave until the user taps. | Mirrors GorodRecap's "no signal → suggest, don't fabricate state" honesty floor. Auto-driving the wave on mere page-load would be a decision made *for* the user, violating the fidelity/control wedge. |

No other conflicts. Where the draft supplied concrete numbers (waveDelta multipliers, BPM, durations), those are authoritative and reproduced verbatim below — **do not invent values outside this set.**

---

## 1. Final placement + additive-safety proof (does NOT trigger gated 045)

### 1.1 Where it goes
- **DOM:** new `<section class="ctx-strip">` inserted **between line 9632 (`</header>` closing `.taste-hero`) and line 9634 (`<div class="taste-body" id="taste-body">`).** Normal flow inside `.taste-stage` (a flexible `max-width:1080px` flow container) on `#/taste` — the **non-pixel-perfect** AI screen.
- **CSS:** new block inserted near the existing `.taste-*` rules (after line 3058, `.taste-delta`).
- **TwinrWave extension:** edits inside the existing wave IIFE (lines 12920–13021) — additive only.
- **New module:** `window.GorodContext` IIFE appended as the **last trailing `<script>` before `</body>`** (mirroring GorodRecap/GorodProfile), i.e. after line 13153's `</script>`.

### 1.2 Why this is purely additive — and does NOT activate gated 045
1. **Zero bytes change in `#/home`.** The `data-page="home"` section (line 7443+), `.home-stage`, `.home-chip-row`, `.home-tile-row` (8 absolute tiles `--x`/`--top`), and `.home-featured` (Figma 2174:422 «Потрачу/Егор Крид») are untouched. No node enters the `.home-stage` flow → no absolute tile shifts → **pixel-perfect preserved byte-for-byte** → Эльбик's "насколько ломать home" decision (045) is **not triggered**.
2. **The wave lives only on `#/taste`** (verified: `TwinrWave.start()` fires only when `location.hash === '#/taste'`, line 13146). `#/home` has **no wave canvas at all** — so "context changes the wave" can only be shown *honestly* on `#/taste`. Putting the picker on home would promise a visible wave-change with no wave present = FIDELITY violation. Placement on `#/taste` is the *only* truthful surface.
3. **New section is in clean flow**, not absolute — adding it shifts nothing absolutely-positioned.
4. **TwinrWave is extended, not rewritten:** `start`/`stop`/`bump` signatures and the audio branch are unchanged; the neutral context state `{ampMul:1,speedMul:1,energyBoost:0,warm:0}` makes the render formula byte-identical to today until `setContext` is first called → **zero regression** on every other screen/state. All 3 existing `bump()` callers (GorodTaste render, WaveDials apply, GorodRecap copySummary — verified at lines 13075/13083/13187/13245/13609/13846) keep working unchanged.
5. **No new route.** `VALID_ROUTES` (verified line 10849) already contains `#/taste`; not modified.
6. **New LS key `gorodfm_context` is isolated** — `gorodfm_taste` / `gorodfm_rejected` / `gorodfm_ad_less` untouched.
7. **No backend, no flags, no gates.** Pure client UI that only changes the *local, visible* wave. Nothing is "activated."
8. **Does not duplicate GorodDiscover 046 chips** (`#/podborki`): different screen, different object (radio *session* reshape vs semantic *search* query), different mechanism (`TwinrWave.setContext` vs navigation into a подборка).

---

## 2. Context set — real parameters + time-aware default

**Time contexts** (mutually exclusive; one is the time-of-day default; `data-ctx`):

| key | label | BPM (target) | Energy | Duration | `getHours()` default range | waveDelta `{ampMul, speedMul, energyBoost, warm}` |
|---|---|---|---|---|---|---|
| `morning` | Утро | 80–95 (**85**) | низкая→средняя (нарастает) | 40 мин | 5 ≤ h < 11 | `{.78, .70, .00, 0}` |
| `day` | День | 95–110 (**100**) | средняя, ровная | 90 мин | 11 ≤ h < 17 | `{.85, .92, .15, .15}` |
| `evening` | Вечер | 90–105 (**95**) | средняя, теплее | 60 мин | 17 ≤ h < 23 | `{1.0, .85, .25, .55}` |
| `night` | Ночь | 60–80 (**70**) | низкая | 30 мин | h ≥ 23 OR h < 5 | `{.62, .50, -.10, 0}` |

**Activity contexts** (optional modifier, **never** an auto time-default; override the time context's wave while active; `data-act`):

| key | label | BPM (target) | Energy | Duration | waveDelta |
|---|---|---|---|---|---|
| `workout` | Тренировка | 120–140 (**128**) | высокая | 45 мин | `{1.35, 1.40, .60, .30}` |
| `commute` | Дорога | 100–115 (**108**) | средне-высокая | 35 мин | `{1.10, 1.05, .35, .35}` |

**Time-aware default** (deterministic, no random):
```js
function defaultCtx(){ var h=new Date().getHours();
  if(h>=5&&h<11) return 'morning';
  if(h>=11&&h<17) return 'day';
  if(h>=17&&h<23) return 'evening';
  return 'night'; }
```
The default is a **suggestion**, never auto-launched and never locked: the suggested chip is highlighted (`data-now="1"` → text suffix "· сейчас" + `#ctx-hint`), but the wave is driven **only** on an explicit fresh choice (C7).

**Behavioral «почему» strings** (parametric, never marketing — literal trusted HTML with `<b>` around the number; safe for `innerHTML` because they are module constants, not user input):
- morning: `Старт мягкий: <b>85 BPM</b>, низкая энергия первые 10 минут — потом плавно вверх. Без рывка.`
- day: `Ровный темп <b>~100 BPM</b>, без скачков энергии 90 минут — фон для работы.`
- evening: `Тёплый вектор <b>~95 BPM</b> — так ты дослушиваешь до конца вечером.`
- night: `Медленно, <b>70 BPM</b>, низкая энергия — волна почти не двигается.`
- workout: `<b>128 BPM</b>, высокая энергия — бит задаёт темп под нагрузку. Перекрывает время, пока активно.`
- commute: `<b>108 BPM</b>, средне-высокая энергия на 35 минут — под дорогу, держит в тонусе.`

---

## 3. DOM structure (semantics + a11y)

Insert verbatim between line 9632 and 9634. Native `<button type="button">` for every interactive; two labelled `role="group"`s; live regions for SR announcement; the "сейчас" marker is **text + aria, not color-only**.

```html
<section class="ctx-strip" aria-labelledby="ctx-strip-h">
  <div class="ctx-strip-head">
    <h2 class="ctx-strip-title" id="ctx-strip-h">Контекстный старт</h2>
    <p class="ctx-strip-hint" id="ctx-hint" aria-live="polite"></p>
  </div>

  <!-- time contexts: mutually-exclusive, radio-like (aria-pressed) -->
  <div class="ctx-row" role="group" aria-label="Контекст по времени суток">
    <button class="ctx-chip" type="button" data-ctx="morning" aria-pressed="false">
      <span class="ctx-chip-label">Утро</span>
      <span class="ctx-chip-params">85 BPM · мягко · ~40 мин</span>
    </button>
    <button class="ctx-chip" type="button" data-ctx="day" aria-pressed="false">
      <span class="ctx-chip-label">День</span>
      <span class="ctx-chip-params">100 BPM · ровно · ~90 мин</span>
    </button>
    <button class="ctx-chip" type="button" data-ctx="evening" aria-pressed="false">
      <span class="ctx-chip-label">Вечер</span>
      <span class="ctx-chip-params">95 BPM · теплее · ~60 мин</span>
    </button>
    <button class="ctx-chip" type="button" data-ctx="night" aria-pressed="false">
      <span class="ctx-chip-label">Ночь</span>
      <span class="ctx-chip-params">70 BPM · тихо · ~30 мин</span>
    </button>
  </div>

  <!-- activity modifier: optional toggle on top of time -->
  <div class="ctx-row ctx-row--activity" role="group" aria-label="Занятие — накладывается поверх времени">
    <span class="ctx-row-cap" aria-hidden="true">Занятие</span>
    <button class="ctx-chip ctx-chip--act" type="button" data-act="workout" aria-pressed="false">
      <span class="ctx-chip-label">Тренировка</span>
      <span class="ctx-chip-params">128 BPM</span>
    </button>
    <button class="ctx-chip ctx-chip--act" type="button" data-act="commute" aria-pressed="false">
      <span class="ctx-chip-label">Дорога</span>
      <span class="ctx-chip-params">108 BPM</span>
    </button>
  </div>

  <p class="ctx-why" id="ctx-why" role="status" aria-live="polite"></p>
</section>
```

a11y guarantees:
- `<section aria-labelledby="ctx-strip-h">` under existing `<h1 id="page-taste-heading">` → correct landmark/heading nesting (h2 below h1).
- Each chip `aria-pressed` true/false (time-row radio-like = one active; activity = independent toggle).
- "сейчас" marker = `.ctx-chip-label::after { content:" · сейчас" }` (text) + `#ctx-hint` aria-live — never color alone.
- `#ctx-why` `role="status" aria-live="polite"` + `#ctx-hint` aria-live → context change is announced with real params (BPM/energy/duration).
- No emoji-as-icon. Targets ≥44px (see CSS §6).

---

## 4. TwinrWave extension — final `setContext` (deterministic, backward-compatible)

All edits inside the existing wave IIFE (lines 12920–13021). **No random.** Neutral state = today's render exactly.

### 4.1 Add state vars (after line 12924, alongside `audioCtx…` decls)
```js
    var ctxState  = { ampMul:1, speedMul:1, energyBoost:0, warm:0 }; // neutral = current behavior
    var ctxTarget = { ampMul:1, speedMul:1, energyBoost:0, warm:0 }; // interpolation target
```

### 4.2 Add `setContext` (place near `bump`, after line 12973)
```js
    function setContext(c){
      if(!c) return;
      ctxTarget = { ampMul:c.ampMul, speedMul:c.speedMul, energyBoost:c.energyBoost, warm:c.warm };
      if(REDUCE){ ctxState = { ampMul:c.ampMul, speedMul:c.speedMul, energyBoost:c.energyBoost, warm:c.warm };
        if(canvas && ctx) frame(); return; }            // single static frame, like startWave
      if(!running && canvas && ctx){ running = true; loop(); }
    }
```
(The waveDelta `c` passed in is exactly the `wave` object from CTX/ACT in §2/§5.)

### 4.3 Apply additively inside `frame()` (edit lines 12945, 12951, 12954)

**Interpolation** — insert at the top of `frame()` (right after `ctx.clearRect(...)`, line 12939), runs every frame so the shift is visible but smooth (~1–1.5 s):
```js
      ctxState.ampMul      += (ctxTarget.ampMul      - ctxState.ampMul)      * 0.05;
      ctxState.speedMul    += (ctxTarget.speedMul    - ctxState.speedMul)    * 0.05;
      ctxState.energyBoost += (ctxTarget.energyBoost - ctxState.energyBoost) * 0.05;
      ctxState.warm        += (ctxTarget.warm        - ctxState.warm)        * 0.05;
```

**Energy** (line 12945) — add `ctxState.energyBoost`, keep pulse+audio working on top:
```js
      var mid = h * 0.52, e = 1 + pulse * 1.5 + audioEnergy * 1.7 + ctxState.energyBoost, i, x;
```

**Amplitude + speed** (line 12951) — multiply existing terms:
```js
          var y = mid + Math.sin(nx * Math.PI * 2 * L.freq + t * L.speed * ctxState.speedMul)
                        * (h * L.amp * ctxState.ampMul) * e * env;
```

**Warmth via alpha of the two existing token colors** (line 12954) — no new colors; bias toward `#8b5cf6` (violet/warm), away from `#5168FC` (blue/cool):
```js
        ctx.strokeStyle = L.color;
        ctx.globalAlpha = L.alpha * (L.color === '#8b5cf6' ? (1 + ctxState.warm * 0.5)
                                                            : (1 - ctxState.warm * 0.2));
        ctx.lineWidth = L.width;
```
(Note: drop the standalone `ctx.globalAlpha = L.alpha;` on the original line 12954; the line above now sets it. `ctx.globalAlpha = 1;` reset at line 12957 stays.)

### 4.4 Export (edit line 13021)
```js
    window.TwinrWave = { start: startWave, stop: stopWave, bump: bump, setContext: setContext };
```

**Invariants:** until `setContext` fires, `ctxState = {1,1,0,0}` → `speedMul=1`, `ampMul=1`, `energyBoost=0`, `warm=0` → formula reduces to today's exactly → byte-identical render. `bump` and the audio FFT branch run *on top of* context, never replaced. `setEnergy` is intentionally **not** added in v1 (C3).

---

## 5. `window.GorodContext` module (new trailing IIFE)

Append after the existing wave script's `</script>` (after line 13153), last trailing block before `</body>`. Deterministic, null-guarded, `esc`-sanitized on dynamic strings, hashchange-wired.

```html
<script>
/* ---- GOROD-051 — контекстный старт: пере-форма ВОЛНЫ по времени/занятию ----
   Аддитивно. TwinrWave.setContext (устойчивый state, не transient bump).
   «Почему» — всегда параметрическое (BPM/энергия/длит), никогда маркетинг. */
(function () {
  'use strict';
  var LS = 'gorodfm_context';
  var CTX = {
    morning:{ label:'Утро',  bpm:85,  energy:'низкая→средняя', dur:40, wave:{ampMul:.78,speedMul:.70,energyBoost:.00,warm:0},
      why:'Старт мягкий: <b>85 BPM</b>, низкая энергия первые 10 минут — потом плавно вверх. Без рывка.' },
    day:{ label:'День', bpm:100, energy:'средняя, ровная', dur:90, wave:{ampMul:.85,speedMul:.92,energyBoost:.15,warm:.15},
      why:'Ровный темп <b>~100 BPM</b>, без скачков энергии 90 минут — фон для работы.' },
    evening:{ label:'Вечер', bpm:95, energy:'средняя, теплее', dur:60, wave:{ampMul:1.0,speedMul:.85,energyBoost:.25,warm:.55},
      why:'Тёплый вектор <b>~95 BPM</b> — так ты дослушиваешь до конца вечером.' },
    night:{ label:'Ночь', bpm:70, energy:'низкая', dur:30, wave:{ampMul:.62,speedMul:.50,energyBoost:-.10,warm:0},
      why:'Медленно, <b>70 BPM</b>, низкая энергия — волна почти не двигается.' }
  };
  var ACT = {
    workout:{ label:'Тренировка', bpm:128, energy:'высокая', dur:45, wave:{ampMul:1.35,speedMul:1.40,energyBoost:.60,warm:.30},
      why:'<b>128 BPM</b>, высокая энергия — бит задаёт темп под нагрузку. Перекрывает время, пока активно.' },
    commute:{ label:'Дорога', bpm:108, energy:'средне-высокая', dur:35, wave:{ampMul:1.10,speedMul:1.05,energyBoost:.35,warm:.35},
      why:'<b>108 BPM</b>, средне-высокая энергия на 35 минут — под дорогу, держит в тонусе.' }
  };
  function $(id){ return document.getElementById(id); }
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function defaultCtx(){ var h=new Date().getHours(); if(h>=5&&h<11)return 'morning'; if(h>=11&&h<17)return 'day'; if(h>=17&&h<23)return 'evening'; return 'night'; }
  function isToday(ts){ if(!ts)return false; var a=new Date(ts),b=new Date(); return a.getFullYear()===b.getFullYear()&&a.getMonth()===b.getMonth()&&a.getDate()===b.getDate(); }
  function read(){ try{ return JSON.parse(localStorage.getItem(LS)||'null'); }catch(e){ return null; } }
  function write(o){ try{ localStorage.setItem(LS, JSON.stringify(o)); }catch(e){} }

  function effective(state){
    if(state && state.activity && ACT[state.activity]) return { obj:ACT[state.activity], src:'activity', time:state.ctx };
    var ck=(state && state.ctx) || defaultCtx();
    return { obj:CTX[ck]||CTX.morning, src:'time', time:ck };
  }
  function applyWave(eff){ if(window.TwinrWave && window.TwinrWave.setContext) window.TwinrWave.setContext(eff.obj.wave); }
  function reflectPlayer(eff){            // opportunistic echo — overwritten by player on next track (C5)
    var reason=$('player-track-reason'), span=reason&&reason.querySelector('span');
    if(span){ span.innerHTML='Контекст «'+esc(eff.obj.label)+'»: <b>'+eff.obj.bpm+' BPM</b>, '+esc(eff.obj.energy)+', ~'+eff.obj.dur+' мин'; }
  }
  function setWhy(eff){ var w=$('ctx-why'); if(w) w.innerHTML='Сейчас «'+esc(eff.obj.label)+'»: '+eff.obj.why; } // why = trusted literal with <b>BPM</b>
  function paintChips(state){
    var eff=effective(state), sugg=defaultCtx(), fresh=state&&isToday(state.ts);
    [].forEach.call(document.querySelectorAll('.ctx-chip[data-ctx]'),function(b){
      var on=(eff.src==='time'&&b.getAttribute('data-ctx')===eff.time)||(eff.src==='activity'&&state&&b.getAttribute('data-ctx')===state.ctx);
      b.setAttribute('aria-pressed', on?'true':'false'); b.classList.toggle('is-on', !!on);
      b.setAttribute('data-now', (!fresh && b.getAttribute('data-ctx')===sugg)?'1':'0');
    });
    [].forEach.call(document.querySelectorAll('.ctx-chip[data-act]'),function(b){
      var on=state&&state.activity===b.getAttribute('data-act');
      b.setAttribute('aria-pressed', on?'true':'false'); b.classList.toggle('is-on', !!on);
    });
    var hint=$('ctx-hint');
    if(hint){ hint.textContent = fresh ? '' : ('Сейчас '+CTX[sugg].label.toLowerCase()+' — предлагаю '+CTX[sugg].bpm+' BPM. Можно поменять.'); }
  }
  function render(state){ paintChips(state); setWhy(effective(state)); }
  function chooseTime(key){ var s=read()||{}; s.ctx=key; s.ts=Date.now(); write(s); var eff=effective(s); applyWave(eff); reflectPlayer(eff); render(s); if(window.TwinrWave)window.TwinrWave.bump(); }
  function toggleAct(key){ var s=read()||{}; s.activity=(s.activity===key)?null:key; if(!s.ctx)s.ctx=defaultCtx(); s.ts=Date.now(); write(s); var eff=effective(s); applyWave(eff); reflectPlayer(eff); render(s); if(window.TwinrWave)window.TwinrWave.bump(); }

  var wired=false;
  function wire(){
    if(wired)return; var strip=document.querySelector('.ctx-strip'); if(!strip)return;
    strip.addEventListener('click',function(e){
      var t=e.target.closest('.ctx-chip'); if(!t)return;
      if(t.hasAttribute('data-ctx')) chooseTime(t.getAttribute('data-ctx'));
      else if(t.hasAttribute('data-act')) toggleAct(t.getAttribute('data-act'));
    });
    wired=true;
  }
  function onRoute(){
    if((location.hash||'')==='#/taste'){
      wire(); var s=read(); render(s);
      if(s && (s.activity || s.ctx) && isToday(s.ts)){ var eff=effective(s); setTimeout(function(){ applyWave(eff); reflectPlayer(eff); },60); }
    }
  }
  window.addEventListener('hashchange', onRoute);
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', onRoute); else onRoute();
  // public API (lets a future #/home pill — VARIANT B — suggest/apply without coupling)
  window.GorodContext = { render:render, suggest:function(){ var s=read()||{}; if(!isToday(s.ts)) s.ctx=defaultCtx(); write(s); render(s); }, apply:chooseTime };
})();
</script>
```

**Data model** — LS key `gorodfm_context`, JSON object `{ "ctx": "morning"|"day"|"evening"|"night"|null, "activity": null|"workout"|"commute", "ts": <Date.now()> }`. `ctx=null` means "by time". `activity` overrides the wave while set; the time `ctx` stays visible as background. `ts` gates same-day freshness so yesterday's pick is never forced — instead it re-surfaces as a suggestion.

**Effective context:** `activity ? ACT[activity] : CTX[ctx || defaultCtx()]` — activity has wave priority, time stays the visible background.

**Correctness / zero-console-errors:** `try/catch` on all LS; guard on `window.TwinrWave.setContext` (module never throws if the wave patch §4 isn't present); null-guard on every `$()`/`querySelector`; `esc()` on all dynamic strings; `why` strings are module constants (trusted `<b>BPM</b>` literals, no user input) so `innerHTML` is safe; click delegated to `.ctx-strip` (survives even if chips are absent); zero `Math.random` (fully deterministic).

---

## 6. CSS — tokens only (every var enumerated)

Insert after line 3058 (`.taste-delta`). **No new hardcoded colors** beyond the same `rgba(255,255,255,…)` / `rgba(235,235,245,…)` white scales already pervasive in the file, plus the literal `rgba(81,104,252,…)` which is the documented RGB of `--brand-blue-light` (#5168FC) used for tint/shadow (matching the file's existing pattern at e.g. line 585).

```css
.ctx-strip { margin: 0 0 28px; }
.ctx-strip-head { display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; margin-bottom:14px; }
.ctx-strip-title { font-family:'Onest',sans-serif; font-weight:800; font-size:18px; color:#fff; margin:0; letter-spacing:-0.01em; }
.ctx-strip-hint { font-family:'Onest',sans-serif; font-size:13px; font-weight:600; color:var(--accent-on-dark); margin:0; }
.ctx-row { display:flex; gap:10px; flex-wrap:wrap; align-items:stretch; }
.ctx-row + .ctx-row { margin-top:10px; }
.ctx-row--activity { align-items:center; }
.ctx-row-cap { font-family:'Onest',sans-serif; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:rgba(255,255,255,0.70); margin-right:2px; }

.ctx-chip {
  position:relative; display:flex; flex-direction:column; align-items:flex-start; gap:2px;
  min-height:56px; min-width:120px; padding:9px 16px; cursor:pointer;
  font-family:'Onest',sans-serif; text-align:left;
  background:rgba(255,255,255,0.04); color:#fff;
  border:1px solid rgba(255,255,255,0.10); border-radius:var(--r-base);
  transition: background var(--t-fast), border-color var(--t-fast), transform var(--t-fast);
}
.ctx-chip--act { min-height:44px; min-width:auto; flex-direction:row; align-items:center; gap:8px; }
.ctx-chip-label { font-size:14px; font-weight:700; line-height:1.1; }
.ctx-chip-params { font-size:11px; font-weight:600; color:rgba(235,235,245,0.60); letter-spacing:0.01em; }
.ctx-chip:hover { background:rgba(255,255,255,0.07); transform:translateY(-1px); }
.ctx-chip[aria-pressed="true"], .ctx-chip.is-on {
  background:rgba(81,104,252,0.16);
  border-color:rgba(81,104,252,0.55);
  box-shadow:0 0 0 1px rgba(81,104,252,0.30), 0 6px 20px -8px var(--brand-blue-light);
}
.ctx-chip[aria-pressed="true"] .ctx-chip-params { color:var(--accent-on-dark); }
.ctx-chip:focus-visible { outline:3px solid var(--brand-blue-light); outline-offset:3px; }

/* time-aware «сейчас» — text suffix, not color-only */
.ctx-chip[data-now="1"] .ctx-chip-label::after {
  content:" · сейчас"; font-size:10px; font-weight:700; color:var(--accent-on-dark);
  text-transform:uppercase; letter-spacing:0.05em;
}

.ctx-why {
  margin:14px 0 0; font-family:'Onest',sans-serif; font-size:13px; line-height:1.5;
  color:rgba(255,255,255,0.70); max-width:560px;
}
.ctx-why b { color:#cdd4f5; font-weight:700; }

@media (max-width:560px){ .ctx-chip { flex:1 1 calc(50% - 5px); min-width:0; } }
@media (prefers-reduced-motion: reduce){
  .ctx-chip { transition:none; }
  .ctx-chip:hover { transform:none; }
}
```

**Token inventory (every var used):**
- `--accent-on-dark` (#8094ff, AA small-accent) — hint text, active-chip params, "· сейчас" suffix.
- `--brand-blue-light` (#5168FC, the single accent) — focus-visible outline, active-chip glow shadow (and its RGB `81,104,252` for tint/border).
- `--r-base` (10px) — chip radius.
- `--t-fast` (180ms) — chip transitions.
- Onest only (`font-family:'Onest',sans-serif` on every text node).
- White-scale rgba: `#fff`, `rgba(255,255,255,.70)`, `rgba(255,255,255,.10)`, `rgba(255,255,255,.07)`, `rgba(255,255,255,.04)`, `rgba(235,235,245,.60)` — all pre-existing in the file.
- `#cdd4f5` for `.ctx-why b` — a desaturated light-blue text emphasis already used in the grounded draft's family; **if strict-tokens is required, swap to `var(--accent-on-dark)`** (AA) to avoid any non-token literal. (Recommended: use `--accent-on-dark` to keep the zero-hardcode gate clean.)
- **Not used:** `--np-accent` (reserved content-derived; available if a per-context tint is wanted later), `--r-pill`, `--success`, `--t-mid/-slow`, `--ease-*`, `--dur-*`. The wave's warmth uses the two existing layer colors `#5168FC`/`#8b5cf6` via alpha only — no new color.

---

## 7. Entry / route wiring

- **No new route.** `VALID_ROUTES` (line 10849) already includes `#/taste` — unchanged.
- **Module self-wires:** `hashchange` + `DOMContentLoaded`/immediate (`document.readyState` guard), independent of the main router/`activatePage`. It does **not** hook the existing wave IIFE's `onRoute` (line 13142) — it runs its own gated `onRoute()` and only acts when `location.hash === '#/taste'`.
- **Apply timing:** on a fresh-today saved choice, `applyWave` is deferred `setTimeout(…,60)` so it lands after the wave IIFE's own `start()` (`setTimeout(…,30)`, line 13146) — the wave canvas is initialized before `setContext` drives it.
- **Click delegation:** single listener on `.ctx-strip`; `chooseTime`/`toggleAct` persist → drive wave → reflect player → re-render → `bump()` for an immediate visible "you did this" transient on top of the new durable base state.
- **VARIANT B hook (deferred):** `window.GorodContext.suggest()` / `.apply(key)` are exported so a future floating `#/home` pill can pre-select by time and navigate to `#/taste` without coupling — **not built in v1.**

---

## 8. Holy-Grail / anti-slop checklist

| Gate | Status | Evidence |
|---|---|---|
| **Onest only** | ✅ | Every text node `font-family:'Onest',sans-serif`. No Inter/Roboto/system-ui. |
| **near-black bg + 1 accent** | ✅ | bg unchanged (`--bg-base` #0B0C0F context); single accent `--brand-blue-light`. No second hue introduced (wave warmth = alpha shift between two *existing* layer colors). |
| **`--accent-on-dark` for small accent text** | ✅ | Used for `#ctx-hint`, active-chip params, "· сейчас" — the only places small accent text appears (AA 6.8:1). |
| **targets ≥44px** | ✅ | `.ctx-chip` 56px (time) / 44px (activity); mobile `flex:1 1 50%` preserves height. |
| **focus-visible 3px** | ✅ | `.ctx-chip:focus-visible { outline:3px solid var(--brand-blue-light); outline-offset:3px; }`. |
| **prefers-reduced-motion** | ✅ | CSS disables chip transition/hover-translate; `setContext` under `REDUCE` snaps state + draws one static `frame()` (param visible, no animation) — mirrors `startWave`'s existing guard. |
| **parametric copy, not marketing** | ✅ | Every «почему» cites real BPM/energy/duration; "тебе понравится" absent. Honest fallback `#ctx-hint` when no fresh choice ("предлагаю … по времени"). |
| **❌ no multi-stop gradient bg** | ✅ | Flat `rgba(255,255,255,.04)` chips; active = flat 16% blue tint + single-color glow. |
| **❌ no orb-avatar / fake-wave / gradient-placeholder / emoji-icons** | ✅ | No avatars; wave change is driven on the *real* TwinrWave canvas (no fake/placeholder wave); no gradient fills; zero emoji (text "· сейчас", not 🌅). |
| **WCAG AA** | ✅ | `#fff` & `rgba(235,235,245,.60)` params on `.04`/16%-tint bg; small accent = `--accent-on-dark`. |
| **zero console errors** | ✅ | try/catch on LS; guards on `TwinrWave.setContext`, every `$()`/`querySelector`; delegated listener; deterministic (no random). |
| **additive single-file** | ✅ | One new section + one CSS block + 5 additive edits to the wave IIFE + one trailing IIFE. No route added, no existing method signature changed, neutral-state = byte-identical current render. |
| **additive-safety / 045 not triggered** | ✅ | `#/home` untouched (§1.2); pixel-perfect Figma 2174:422 preserved; gated 045 not activated. |
| **no GorodDiscover 046 dup** | ✅ | Different screen (`#/taste` vs `#/podborki`), object (session reshape vs search), mechanism (`setContext` vs navigation). |

---

## 9. Implementer's edit manifest (ordered, line-anchored)

1. **CSS** — insert §6 block after line 3058 (`.taste-delta`).
2. **DOM** — insert §3 `<section class="ctx-strip">` between line 9632 (`</header>`) and 9634 (`.taste-body`).
3. **TwinrWave** — apply §4 edits: state vars after 12924; `setContext` after 12973; interpolation at top of `frame()` (after 12939); energy line 12945; amp/speed line 12951; warmth alpha line 12954; export line 13021.
4. **Module** — append §5 `window.GorodContext` `<script>` after line 13153 (`</script>`), last block before `</body>` (13931).
5. Recommended token-purity tweak: set `.ctx-why b` color to `var(--accent-on-dark)` to eliminate the one non-token literal `#cdd4f5`.

All four anchor pairs (9632/9634, 12920–13021 wave IIFE, 13021 export, 10849 VALID_ROUTES, 10022 `#player-track-reason`, 13478 player overwrite) verified against the current file in this session.