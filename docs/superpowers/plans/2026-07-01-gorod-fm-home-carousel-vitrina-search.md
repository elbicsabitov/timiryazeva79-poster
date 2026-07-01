# Город ФМ Home — Station Carousel + Music Витрина + Search — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `designs/gorod-fm.html` `#/home` into a lean-forward radio storefront — a flat (no-tilt) carousel of the 6 РМГ live stations, a persistent live-aware player, a persistent search, and a non-AI music витрина (browse/editorial/social shelves) below.

**Architecture:** Evolve the existing single-file SPA in place. Replace the home hero (`#home-radio`) with the station carousel (reusing the existing `.home-station` card CSS), keep the global player (`.player-mini`) but make it live-aware, add a persistent search field + overlay, and add a shelf-based витрина feed. All AI/personalization (wave, steer, «для вас») is OUT of scope — it relocates to a future «Моя волна» AI tab.

**Tech Stack:** Vanilla HTML/CSS/JS in one file. CSS `scroll-snap` + scroll-driven `animation-timeline: view()` for the carousel; `IntersectionObserver` for the active-index + fallback; `MediaSession` API for the player; `localStorage` for state. Verification: `node .scratch/check_scripts.cjs` + local `python -m http.server` + Chrome visual + `compound-engineering:design:design-implementation-reviewer`.

**Spec:** `docs/superpowers/specs/2026-07-01-gorod-fm-home-station-carousel-feed-search-design.md`
**Research:** `docs/superpowers/RESEARCH-gorod-fm-home-carousel-feed-search.md` (wave-1), `…-home-feed-frontier-wave2.md` (wave-2, for the future «Моя волна» tab).

## Global Constraints
- **Surface:** `#/home` only. Do NOT change any other route, the sidebar/tab IA, or the design system. Other routes must stay byte-unaffected.
- **Skin (reuse tokens, add none):** page bg `#0B0C0F`; surfaces `--surface-0/1/2/3` = `#111318`/`#15171D`/`#1B1E26`/`#23262F`; text `--text-pri` `#FFFFFF` / `--text-sec` `rgba(255,255,255,.62)`; accent (large/icon) `--brand-blue-light` `#5168FC`; accent (small text/focus) `--accent-on-dark` `#8094ff`; hairline `--hairline` `rgba(255,255,255,.08)`; player height `--player-mini-h` `72px`; font Onest.
- **Anti-slop (hard gate):** no gradient-fill backgrounds, no rotated text, no emoji, **no fabricated stats/counts**, single accent only, flat > skeuo, hit targets ≥44px, WCAG AA (small accent text uses `--accent-on-dark`).
- **Roster (real, do not invent):** Город ФМ (default center) · Русское Радио · ХИТ FM · DFM · MAXIMUM · Radio Monte Carlo. Logos are pending owner assets → use honestly-labeled placeholders (station monogram on `--surface-2`) until provided; never fabricate FM numbers.
- **Honesty:** representative/demo content is allowed in a prototype but must never be presented as real user stats; `Друзья слушают` uses clearly-representative activity; no listener/play counts unless a real value exists.
- **Branch:** `feat/gorod-home-rmg-storefront` (already created; repo shared with Twinr — keep isolated, do not touch Twinr files).
- **Per-task verify loop:** (1) `node .scratch/check_scripts.cjs` (or `node --check` per `<script>` if that helper is absent) → 0 errors; (2) serve `cd designs && python -m http.server 8791`, open `http://127.0.0.1:8791/gorod-fm.html?v=N#/home` in Chrome, screenshot desktop (1440) + mobile (390), confirm 0 console errors; (3) atomic commit. **Anchors drift — always re-grep the live file before editing; never trust line numbers from this plan.**

---

### Task 1: Station data model + roster

**Files:**
- Modify: `designs/gorod-fm.html` — add a `GorodStations` IIFE near the other trailing `<script>` modules (re-grep for the last `</script>` before `</body>`; insert before it).

**Interfaces:**
- Produces: `window.GorodStations = { list: Station[], active: id, get(id), setActive(id) }` where `Station = {id, name, freq|null, logo|null, streamUrl|null, kind:'live'}` and `NowPlaying = {title, artist, source:'icy'|'demo', ts}` (now-playing is looked up per station; `source:'demo'` for representative data).

- [ ] **Step 1: Add the roster module.** Insert:

```html
<script>
(function(){
  // Real РМГ roster (brand-book set). Logos pending → null renders a monogram placeholder.
  const S = [
    {id:'gorod',   name:'Город ФМ',        freq:null, logo:null, streamUrl:null, kind:'live'},
    {id:'russkoe', name:'Русское Радио',   freq:null, logo:null, streamUrl:null, kind:'live'},
    {id:'hit',     name:'ХИТ FM',          freq:null, logo:null, streamUrl:null, kind:'live'},
    {id:'dfm',     name:'DFM',             freq:null, logo:null, streamUrl:null, kind:'live'},
    {id:'maximum', name:'MAXIMUM',         freq:null, logo:null, streamUrl:null, kind:'live'},
    {id:'mc',      name:'Radio Monte Carlo',freq:null,logo:null, streamUrl:null, kind:'live'},
  ];
  // Representative now-playing (source:'demo' — replaced by real ICY metadata when streamUrl exists).
  const NP = {
    gorod:{title:'Любимка', artist:'Niletto', source:'demo', ts:0},
    russkoe:{title:'Я русский', artist:'SHAMAN', source:'demo', ts:0},
    hit:{title:'Плачу на техно', artist:'Cream Soda', source:'demo', ts:0},
    dfm:{title:"Baby Don't Hurt Me", artist:'David Guetta', source:'demo', ts:0},
    maximum:{title:'Sonne', artist:'Rammstein', source:'demo', ts:0},
    mc:{title:'Smooth Operator', artist:'Sade', source:'demo', ts:0},
  };
  let active = 'gorod';
  window.GorodStations = {
    list: S,
    get active(){ return active; },
    get(id){ return S.find(s=>s.id===id); },
    nowPlaying(id){ return NP[id] || {title:'', artist:'', source:'demo', ts:0}; },
    setActive(id){ if(S.some(s=>s.id===id)) active = id; return active; },
  };
})();
</script>
```

- [ ] **Step 2: Verify syntax.** Run `node .scratch/check_scripts.cjs` → 0 errors (or `node --check` on the extracted block).
- [ ] **Step 3: Verify in Chrome.** Reload `?v=1#/home`; in console confirm `GorodStations.list.length === 6` and `GorodStations.nowPlaying('gorod').artist === 'Niletto'`; 0 console errors.
- [ ] **Step 4: Commit.** `git add designs/gorod-fm.html && git commit -m "feat(gorod-home): РМГ station roster + now-playing data model"`

---

### Task 2: Carousel markup + flat no-tilt CSS

**Files:**
- Modify: `designs/gorod-fm.html` — the home hero markup (re-grep `id="home-radio"`, currently ~L8682) and the home CSS block (re-grep `.home-station {`, currently ~L4231, and `Home page — stations grid`, ~L4231).

**Interfaces:**
- Consumes: `GorodStations` (Task 1).
- Produces: `<section class="rmg-rail" id="rmg-rail">` containing `<ul class="rmg-track">` of `<li class="rmg-card">` (native `<button>` inside); CSS classes `.rmg-rail/.rmg-track/.rmg-card/.rmg-card-art/.rmg-card-name/.rmg-card-freq/.rmg-card-live/.rmg-card-np`.

- [ ] **Step 1: Replace the home hero content with the carousel container.** Re-grep `id="home-radio"`; inside `#/home`'s panel, replace the `#home-radio` hero block (the `home-radio-top`/`home-radio-stage`/`home-radio-bottom` wave hero — Task 1 keeps that code available for the future «Моя волна» tab, so cut it to a commented `<!-- MOVED TO «Моя волна» tab -->` marker rather than deleting logic you may relocate) with:

```html
<section class="rmg-rail" id="rmg-rail" role="group" aria-roledescription="карусель" aria-label="Радиостанции">
  <ul class="rmg-track" id="rmg-track" role="list"><!-- cards injected by Task 3 --></ul>
</section>
```

- [ ] **Step 2: Add the flat centered-snap CSS.** In the home CSS block, add (accent only on the active card; transform+opacity only; no rotation):

```css
.rmg-rail{ position:relative; }
.rmg-track{ list-style:none; margin:0; padding:0; display:flex; gap:20px;
  overflow-x:auto; overscroll-behavior-x:contain; scroll-snap-type:x mandatory;
  scroll-behavior:smooth; padding-inline:calc(50% - var(--rmg-card,320px)/2);
  scrollbar-width:none; }
.rmg-track::-webkit-scrollbar{ display:none; }
.rmg-card{ flex:0 0 var(--rmg-card,320px); scroll-snap-align:center; }
.rmg-card > button{ all:unset; box-sizing:border-box; display:block; width:100%; cursor:pointer;
  border-radius:20px; background:var(--surface-1); padding:14px; }
.rmg-card-art{ aspect-ratio:1; border-radius:14px; background:var(--surface-2);
  display:grid; place-items:center; font:600 40px Onest,sans-serif; color:var(--text-sec); overflow:hidden; }
.rmg-card-name{ font:700 20px Onest,sans-serif; color:var(--text-pri); margin-top:12px; }
.rmg-card-freq{ font:500 14px Onest,sans-serif; color:var(--text-sec); }
.rmg-card-np{ font:500 14px Onest,sans-serif; color:var(--text-sec);
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:6px; }
.rmg-card-live{ display:none; }
.rmg-card[aria-current="true"] .rmg-card-live{ display:inline-flex; align-items:center; gap:6px;
  font:600 12px Onest,sans-serif; color:var(--accent-on-dark); }
.rmg-card[aria-current="true"] .rmg-card-live::before{ content:''; width:8px; height:8px; border-radius:50%;
  background:var(--brand-blue-light); animation:rmg-pulse 1.6s ease-in-out infinite; }
@keyframes rmg-focus{ 0%,100%{opacity:.45; transform:scale(.82)} 50%{opacity:1; transform:scale(1)} }
@keyframes rmg-pulse{ 0%,100%{opacity:1} 50%{opacity:.4} }
@supports (animation-timeline: view()){
  .rmg-card{ animation:rmg-focus linear both; animation-timeline:view(inline); will-change:transform,opacity; }
}
@supports not (animation-timeline: view()){
  .rmg-card{ opacity:.45; transform:scale(.82); transition:opacity .25s, transform .25s; }
  .rmg-card.is-centered{ opacity:1; transform:scale(1); }
}
@media (prefers-reduced-motion: reduce){
  .rmg-track{ scroll-behavior:auto; }
  .rmg-card{ animation:none !important; opacity:1 !important; transform:none !important; }
  .rmg-card-live::before{ animation:none; }
}
```

- [ ] **Step 3: Verify syntax + visual.** `node .scratch/check_scripts.cjs`; serve + open `?v=2#/home` — the empty rail renders (cards come in Task 3), no layout break, 0 console errors, other routes still load.
- [ ] **Step 4: Commit.** `git commit -am "feat(gorod-home): flat no-tilt station carousel markup + CSS (reduced-motion + Firefox fallback)"`

---

### Task 3: Carousel rendering + interaction JS

**Files:**
- Modify: `designs/gorod-fm.html` — add a `GorodRail` IIFE (insert near Task 1's module).

**Interfaces:**
- Consumes: `GorodStations`, `#rmg-track`.
- Produces: `window.GorodRail = { render(), setActive(id), center(id) }`; emits a `gorod:tune` CustomEvent on `document` with `{detail:{id}}` when a station is centered+activated (Task 5/6 listen).

- [ ] **Step 1: Render cards + wire interaction.** Insert:

```html
<script>
(function(){
  const track = () => document.getElementById('rmg-track');
  const supportsSDA = CSS.supports('animation-timeline','view(inline)');
  function monogram(name){ return (name||'?').trim()[0] || '?'; }
  function cardHTML(s, np){
    return `<li class="rmg-card" data-id="${s.id}">
      <button type="button" aria-label="Слушать ${s.name}">
        <span class="rmg-card-art">${s.logo?`<img src="${s.logo}" alt="" style="width:100%;height:100%;object-fit:cover">`:monogram(s.name)}</span>
        <span class="rmg-card-live">В ЭФИРЕ</span>
        <span class="rmg-card-name">${s.name}${s.freq?` <span class="rmg-card-freq">${s.freq}</span>`:''}</span>
        <span class="rmg-card-np">${np.artist} — ${np.title}</span>
      </button></li>`;
  }
  function render(){
    const t = track(); if(!t) return;
    t.innerHTML = GorodStations.list.map(s=>cardHTML(s, GorodStations.nowPlaying(s.id))).join('');
    const cards = [...t.querySelectorAll('.rmg-card')];
    cards.forEach((c,i)=> c.querySelector('button').tabIndex = (i===0?0:-1));
    // active-index via IntersectionObserver (also the SDA-less fallback painter)
    const io = new IntersectionObserver(es=>{
      es.forEach(e=>{ if(e.isIntersecting && e.intersectionRatio>0.6) setActive(e.target.dataset.id, false); });
    }, {root:t, threshold:[0.6]});
    cards.forEach(c=> io.observe(c));
    // click side card → center it
    cards.forEach(c=> c.querySelector('button').addEventListener('click', ()=>{
      if(GorodStations.active===c.dataset.id) tune(c.dataset.id); else center(c.dataset.id);
    }));
    // keyboard: roving tabindex
    t.addEventListener('keydown', e=>{
      const cur = cards.findIndex(c=>c.dataset.id===GorodStations.active);
      let n = cur;
      if(e.key==='ArrowRight') n=Math.min(cur+1,cards.length-1);
      else if(e.key==='ArrowLeft') n=Math.max(cur-1,0);
      else if(e.key==='Home') n=0; else if(e.key==='End') n=cards.length-1;
      else if(e.key==='Enter'||e.key===' ') { tune(GorodStations.active); e.preventDefault(); return; }
      else return;
      e.preventDefault(); center(cards[n].dataset.id); cards[n].querySelector('button').focus();
    });
    setActive('gorod', false); center('gorod', true);
  }
  function setActive(id, doCenter){
    GorodStations.setActive(id);
    const cards = [...track().querySelectorAll('.rmg-card')];
    cards.forEach(c=>{
      const on = c.dataset.id===id;
      c.toggleAttribute('aria-current', on);
      if(!supportsSDA) c.classList.toggle('is-centered', on);
      c.querySelector('button').tabIndex = on?0:-1;
    });
    document.dispatchEvent(new CustomEvent('gorod:activecard',{detail:{id}}));
    if(doCenter) center(id, true);
  }
  function center(id, instant){
    const el = track().querySelector(`.rmg-card[data-id="${id}"]`);
    if(el) el.scrollIntoView({inline:'center', block:'nearest', behavior: instant?'auto':'smooth'});
    setActive(id, false);
  }
  function tune(id){ document.dispatchEvent(new CustomEvent('gorod:tune',{detail:{id}})); }
  window.GorodRail = { render, setActive, center };
  document.addEventListener('DOMContentLoaded', render);
  // also render on hash → #/home (re-grep the router; call GorodRail.render() when entering #/home)
})();
</script>
```

- [ ] **Step 2: Hook render on route enter.** Re-grep `routeFromHash`/the route switch (~L11839–11923); ensure `GorodRail.render()` runs when `#/home` becomes active (idempotent — guard against double-render by checking `track().children.length`).
- [ ] **Step 3: Verify.** `node .scratch/check_scripts.cjs`; Chrome `?v=3#/home`: 6 cards render, Город ФМ centered + `aria-current` + live dot; scrolling recenters focus; ←/→ moves active; clicking a side card centers it; 0 console errors. Screenshot desktop confirms flat scaling, **no rotation**.
- [ ] **Step 4: Commit.** `git commit -am "feat(gorod-home): carousel render + click-to-center + roving-tabindex + IO active-index"`

---

### Task 4: Live-aware player (reuse `.player-mini`)

**Files:**
- Modify: `designs/gorod-fm.html` — the `.player-mini` markup (re-grep `class="player-mini"`, ~L11192) + its controller JS (re-grep `playerState`, `renderPlay`, `syncFullPlayerFromMini`).

**Interfaces:**
- Consumes: `gorod:tune`, `gorod:activecard`, `GorodStations`.
- Produces: `window.GorodPlayer = { tune(id), isLive }`; player reflects the tuned station; MediaSession registers play/pause only.

- [ ] **Step 1: Add a LIVE badge + isLive state to the mini-player.** In `.player-mini`, add a `<span class="player-live-badge" hidden>LIVE</span>` and ensure NO scrubber shows while `isLive` (re-grep the player markup; if a progress element exists, hide it under `[data-live="true"]`). CSS:

```css
.player-live-badge{ font:600 12px Onest,sans-serif; color:var(--accent-on-dark);
  display:inline-flex; align-items:center; gap:6px; }
.player-live-badge::before{ content:''; width:8px;height:8px;border-radius:50%;
  background:var(--brand-blue-light); animation:rmg-pulse 1.6s ease-in-out infinite; }
[data-live="true"] .player-progress, [data-live="true"] .player-scrubber{ display:none !important; }
@media (prefers-reduced-motion: reduce){ .player-live-badge::before{ animation:none; } }
```

- [ ] **Step 2: Wire tune → player.** Add:

```html
<script>
(function(){
  let isLive = true;
  function paint(id){
    const s = GorodStations.get(id), np = GorodStations.nowPlaying(id);
    const bar = document.querySelector('.player-mini'); if(!bar) return;
    bar.setAttribute('data-live','true');
    const badge = bar.querySelector('.player-live-badge'); if(badge) badge.hidden = false;
    // re-grep existing mini-player title/artist/cover nodes and set them:
    const t = bar.querySelector('[data-player-title]') || document.getElementById('player-mini-title');
    const a = bar.querySelector('[data-player-artist]') || document.getElementById('player-mini-artist');
    if(t) t.textContent = np.title; if(a) a.textContent = `${s.name} · ${np.artist}`;
    if('mediaSession' in navigator){
      navigator.mediaSession.metadata = new MediaMetadata({title:np.title, artist:`${s.name} · ${np.artist}`});
      navigator.mediaSession.setActionHandler('play', ()=>{}); // rejoin live edge
      navigator.mediaSession.setActionHandler('pause', ()=>{});
      // do NOT register seekto/seekforward/seekbackward on live
    }
  }
  function tune(id){ GorodStations.setActive(id); GorodRail && GorodRail.setActive(id,false); paint(id); }
  document.addEventListener('gorod:tune', e=> tune(e.detail.id));
  document.addEventListener('gorod:activecard', e=> paint(e.detail.id)); // preview text on center, no audio
  window.GorodPlayer = { tune, get isLive(){ return isLive; } };
  document.addEventListener('DOMContentLoaded', ()=> paint('gorod'));
})();
</script>
```

- [ ] **Step 3: Verify.** `node .scratch/check_scripts.cjs`; Chrome: centering a station updates the mini-player text; LIVE badge shows; no scrubber visible; clicking the centered card fires `tune` and paints; 0 console errors. (Real audio playback is deferred to when `streamUrl` exists — do not add fake audio.)
- [ ] **Step 4: Commit.** `git commit -am "feat(gorod-home): live-aware mini-player (LIVE badge, no live scrubber, MediaSession play/pause)"`

---

### Task 5: Persistent search field + overlay shell

**Files:**
- Modify: `designs/gorod-fm.html` — the home top bar / topbar markup (re-grep the topbar / `Личный кабинет`) + add a search overlay container + CSS + a `GorodSearch` IIFE.

**Interfaces:**
- Produces: `window.GorodSearch = { open(), close() }`; `#gorod-search-field` (persistent), `#gorod-search-overlay` (panel).

- [ ] **Step 1: Add the persistent field to the topbar** (desktop centered ~440px; mobile full-width pill above hero) and an overlay container after it:

```html
<div class="gorod-search"><input id="gorod-search-field" type="search" class="gorod-search-input"
  placeholder="Поиск станций, шоу, треков…" aria-label="Поиск" autocomplete="off"></div>
<div id="gorod-search-overlay" class="gorod-search-overlay" hidden role="dialog" aria-label="Поиск"></div>
```
CSS: input `background:var(--surface-1); height:48px; border-radius:12px; color:var(--text-pri); border:1px solid var(--hairline);` focus ring `1px var(--accent-on-dark)`; overlay `position:fixed; inset:56px 0 var(--player-mini-h) 0; background:rgba(11,12,15,.98); backdrop-filter:blur(20px);` (leaves the docked player visible).

- [ ] **Step 2: Wire open/close + Ctrl-K + `/`.**

```html
<script>
(function(){
  const field = () => document.getElementById('gorod-search-field');
  const ov = () => document.getElementById('gorod-search-overlay');
  function open(){ ov().hidden=false; field().focus(); }
  function close(){ ov().hidden=true; }
  document.addEventListener('DOMContentLoaded', ()=>{
    field() && field().addEventListener('focus', open);
    document.addEventListener('keydown', e=>{
      if((e.key==='k'&&(e.metaKey||e.ctrlKey))||(e.key==='/'&&document.activeElement.tagName!=='INPUT')){ e.preventDefault(); open(); }
      if(e.key==='Escape') close();
    });
  });
  window.GorodSearch = { open, close };
})();
</script>
```

- [ ] **Step 3: Verify.** `node .scratch/check_scripts.cjs`; Chrome: field visible in topbar; focusing / `Ctrl-K` / `/` opens the overlay above the docked player; `Esc` closes; opening search does not stop the (future) audio; 0 console errors.
- [ ] **Step 4: Commit.** `git commit -am "feat(gorod-home): persistent search field + overlay shell (Ctrl-K / '/' focus)"`

---

### Task 6: Search content — typeahead groups + scopes + browse grid

**Files:**
- Modify: `designs/gorod-fm.html` — extend `GorodSearch`; add a small representative search index.

**Interfaces:**
- Consumes: `GorodStations` + a `GorodCatalog` sample (define inline: a few stations/shows/genres/collections/tracks for the prototype).

- [ ] **Step 1: Render the overlay states.** Empty state = «Недавние запросы» (localStorage `gorod_recent`, ×-removable) + «Часто ищут» chips + the **browse-all grid** (mono-accent: real-art tiles where available, else `--surface-1` + 1px `--accent-on-dark`@12% + ghost letterform — **no rainbow tiles**). Typing (≥1 char, ~160ms debounce) = a «Лучший результат» card + grouped capped sections «Станции · Шоу и DJ · Жанры · Подборки · Треки и артисты» with «Показать все →». No-results = «Ничего не нашлось по «…»» + 4–6 fallback stations. Scope chips «Всё · Станции · Треки · Артисты · Подборки · Подкасты» (sticky; «Всё» floats stations/live first). Keyboard ↑/↓ traverse, Enter opens/plays.
- [ ] **Step 2: Verify.** `node .scratch/check_scripts.cjs`; Chrome: typing «рус» surfaces Русское Радио in Станции with a live dot; scopes filter; browse grid renders with **zero rainbow color** (only accent on hover/active); no-results state works; recent-searches persist; 0 console errors. Screenshot to confirm anti-slop grid.
- [ ] **Step 3: Commit.** `git commit -am "feat(gorod-home): search typeahead + scopes + mono-accent browse grid"`

---

### Task 7: Витрина feed — shelf component

**Files:**
- Modify: `designs/gorod-fm.html` — add a `<section class="vitrina" id="vitrina">` below the carousel (inside `#/home`) + shelf CSS + a `GorodVitrina` IIFE.

**Interfaces:**
- Produces: `renderShelf({id,title,seeAllHref,geometry,items})` → a `.shelf` with header (title + `Все ›`) and a horizontal `.shelf-track` of cards; lazy-mounted via IntersectionObserver. `geometry ∈ {circle, square, wide, portrait, row}` sets card shape.

- [ ] **Step 1: Shelf CSS + renderer.** Horizontal scroll shelves, peeking half-card (desktop ~5–6, mobile ~2.2), varied geometry per shelf, header with right-aligned `Все ›`, whitespace separation (**no divider lines, no boxed section backgrounds**), skeletons on mount. Cards: `background:var(--surface-1); border-radius:14px;` art per geometry (circle for stations/artists, square for categories, 16:9 for shows, 1:1 for collections, thumb+text row for tracks).
- [ ] **Step 2: Verify.** `node .scratch/check_scripts.cjs`; Chrome: render one demo shelf → header + `Все ›` + horizontal scroll + peeking card + skeleton→content; geometry switch works; no divider slop; 0 console errors.
- [ ] **Step 3: Commit.** `git commit -am "feat(gorod-home): витрина shelf component (varied geometry, lazy-load, no-slop headers)"`

---

### Task 8: Витрина feed — the non-AI shelves

**Files:**
- Modify: `designs/gorod-fm.html` — populate `GorodVitrina` with the §8.1 shelves + representative content.

**Interfaces:**
- Consumes: `renderShelf` (Task 7).

- [ ] **Step 1: Build the ordered non-AI shelves** (representative content, honestly framed; **no AI/personalization shelves**):
  1. `Друзья слушают` (geometry `row` — avatar + name + station/track + «Слушать то же»; representative activity, clearly example — real needs a social graph)
  2. `Категории и жанры` (geometry `square` — жанры · настроения · активности · эпохи · языки)
  3. `Подборки` (geometry `portrait`/`square` — editorial + curated collections)
  4. `Выбор редакции ГОРОДА` (geometry `square` — human picks)
  5. `Новинки` (geometry `square`)
  6. `Популярное · Чарты` (geometry `row` — real counts or none)
  7. `Коллекции` (geometry `square` — по десятилетиям / языку / городу)
  8. `Исполнители` (geometry `circle`)
  9. `Программы и ведущие` (geometry `wide` — daypart badge «сейчас»/«в 18:00»; opening → player on-demand mode later)
- [ ] **Step 2: Ordering + empty-hide.** Fixed editorial order (same for everyone — no personalization); a shelf with 0 real items is hidden (never padded). Optional calendar-only freshness (e.g. «Новинки» emphasis Fri) using real date, never per-user.
- [ ] **Step 3: Verify.** `node .scratch/check_scripts.cjs`; Chrome desktop + mobile: all shelves render in order, varied geometry, `Друзья слушают` shows representative (not fabricated-as-real) activity, **no fabricated counts**, **no AI shelves present**; scroll performance smooth; 0 console errors. Screenshot both breakpoints.
- [ ] **Step 4: Commit.** `git commit -am "feat(gorod-home): non-AI music витрина shelves (friends/categories/collections/editorial/charts/artists/programs)"`

---

### Task 9: Mobile responsive pass

**Files:**
- Modify: `designs/gorod-fm.html` — home CSS `@media`/`[data-surface="mobile"]` blocks (re-grep existing mobile home rules ~L7156–7332).

- [ ] **Step 1:** Carousel: `--rmg-card` ~78vw, center + peeking neighbors; search = full-width pill above the hero; shelves single-column swipe (~2.2 cards); player docked, feed `padding-bottom:var(--player-mini-h)`; hit targets ≥44px; respect `env(safe-area-inset-bottom)`.
- [ ] **Step 2: Verify.** Chrome at 390 + 768: carousel peeks correctly, search pill above hero, shelves swipe, nothing hidden behind the player; 0 console errors. Screenshots at both widths.
- [ ] **Step 3: Commit.** `git commit -am "feat(gorod-home): mobile responsive (carousel peek, search pill, single-col shelves)"`

---

### Task 10: Anti-slop + a11y review pass

**Files:**
- Modify: `designs/gorod-fm.html` — fixes from the reviewer.

- [ ] **Step 1: Run the reviewer.** Dispatch `compound-engineering:design:design-implementation-reviewer` on `#/home` (desktop 1440 + mobile 390): check single-accent compliance, no gradient/rotated-text/emoji/fabricated-counts, Onest everywhere, WCAG AA contrast (esp. small accent text = `--accent-on-dark`), 44px hit targets, focus-visible rings, `prefers-reduced-motion`.
- [ ] **Step 2:** Apply every finding. Re-run until clean.
- [ ] **Step 3: Verify.** Reviewer report clean; `node .scratch/check_scripts.cjs` 0 errors; other routes byte-unaffected (`git diff --stat` touches only home code).
- [ ] **Step 4: Commit.** `git commit -am "fix(gorod-home): anti-slop + a11y review findings"`

---

### Task 11: Standalone regen + final verification

**Files:**
- Modify: `designs/gorod-fm-standalone.html` (regenerated); build script under `.scratch/`.

- [ ] **Step 1: Regenerate the standalone.** Run the standalone rebuild (re-grep for `rebuild_standalone_full.py` / `tools/build_*_standalone.py`); it inlines assets from the dev file. Confirm the carousel + витрина + search are mirrored.
- [ ] **Step 2: Verify.** Open the standalone offline; carousel, витрина, search all work; 0 console errors; file opens without a server.
- [ ] **Step 3: Full acceptance sweep** against spec §14 (each checkbox); confirm `#/home` only changed.
- [ ] **Step 4: Commit.** `git commit -am "build(gorod-home): regenerate standalone with carousel + витрина + search"`

---

## Self-Review (plan vs spec)

**Spec coverage:** §3 IA → T2/T7; §4 top bar+search → T5/T6; §5 carousel → T1–T3; §6 player → T4; §7 search overlay → T5/T6; §8 витрина → T7/T8; §9 data model → T1; §10 states/mobile → T4 (first-load/reduced-motion in T2/T3), T9 (mobile); §11 scope → Global Constraints + T10 diff-check; §14 acceptance → T11. **AI relocation to «Моя волна» tab is explicitly OUT of scope** (a follow-up plan): the home cuts the `#home-radio` wave to a marked comment (T2) rather than deleting it, so the relocation task can reuse that code.

**Placeholder scan:** representative data (roster, now-playing, search index, shelf content) is intentional prototype content per the spec's honesty rules — clearly labeled, never fabricated stats. No "TODO/implement later" steps.

**Type consistency:** `GorodStations` (Task 1) → consumed by `GorodRail`/`GorodPlayer`/`GorodVitrina` with matching shapes; events `gorod:tune`/`gorod:activecard` produced in T3, consumed in T4; `renderShelf` signature in T7 matches its calls in T8.

**Known follow-ups (not in this plan):** the «Моя волна» AI tab (relocate `#home-radio` wave/steer + wire the frontier recsys from wave-2 research); real ICY stream metadata; real social graph for `Друзья слушают`; real catalog + logos from the client.
