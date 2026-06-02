---
title: "SPEC — RECAP (#/recap) + ПРОФИЛЬ (#/profile) upgrades"
spec_id: SPEC-recap_profile
date: 2026-06-02
surface: "#/recap (GorodRecap @13762) + #/profile (GorodProfile @13666)"
blueprint_refs: ["§1.2 (recap row + profile row)", "§3 Recap/Мой вкус", "§7 ВОЛНА 2 GOROD-050 scale", "§9-B W6 anti-fidelity dedup", "§10 a11y"]
status: build-ready
effort: low (самый лёгкий спек — оба экрана built, всё аддитивно)
research: ["Spotify Wrapped 2024 share-card-per-story", "html2canvas honest-render"]
---

# SPEC — RECAP + ПРОФИЛЬ (апгрейды built-экранов)

> Формат — по образцу `SPEC-gorod-051`: (1) conflict-reconciliation → (2) line-anchored edit-manifest → (3) DOM/CSS/JS verbatim → (4) Holy-Grail чеклист → (5) additive-safety / не-ломает-built. Все номера строк ПЕРЕСВЕРЕНЫ через Read/Grep живого `designs/gorod-fm.html` в этой сессии (файл ~14.1k строк; GorodRecap @13762, GorodProfile @13666, DOM recap @9794–9835, DOM profile @9769–9789, recap CSS @2926–2996, profile CSS @2901–2924).

---

## 0. Что строим (5 правок, все аддитивные)

| # | Экран | Правка | Тип | Effort |
|---|---|---|---|---|
| **R1** | recap | **Дельта-стрелка-ГЕРОЙ** карточки: `+darkwave −арена-рок` причинный сдвиг становится вторым по весу элементом share-card (сейчас `recap-card-delta` @9810 — мелкая 14px строка под bloom). Поднять в иерархии + двухчастный (`+gained · −rejected`), не одно слово. | restyle + reorder существующих узлов | low |
| **R2** | recap | **Реальный PNG-рендер 1080×1920** для Stories. Сейчас `copySummary()` @13962 кладёт ТЕКСТ в клипборд. Добавить вторую кнопку «Сохранить картинку» → honest html→canvas рендер `#recap-card` → download PNG. **Fallback если html2canvas нет** (CDN запрещён офлайн single-file): ручной Canvas-2D рендер тех же фактов (`buildIdentity`/`buildDeltas`/`buildDiscovery`) — НЕ скриншот пустоты. | новая кнопка + новый JS-блок (self-contained Canvas-2D) | low-med |
| **R3** | recap | **micro-CTA «Не согласен? Поправь причину»** под share-card. Сейчас ghost-кнопка @9819 «Поправить грань →» нейтральна. Сделать её причинно-адресной к минус-грани (цитирует то, что реально оспорено / приглашает оспорить). | текст + 1 узел | low |
| **P1** | profile | **Provenance-строка на КАЖДОЙ грани уже есть** (`profile-facet-prov` @9707/13710) — НО reject-грани в `gorodfm_rejected` показываются как голые чипы @13724 без провенанса «откуда оспорено». Добавить провенанс-строку reject-чипам («оспорено на плеере: почему? → не моё»). | дополнение к renderRejected | low |
| **W6** | оба + taste | **ДЕДУП модели фактов.** `REJ_LABELS`+`FALLBACK`+`facets()`+`readPicks()`+`readRej()` дублируются 3× (GorodTaste @13130, GorodProfile @13668/13673/13684, GorodRecap @13767/13768/13776). Любая правка в одном = расхождение views = fidelity-баг (W6 hard-gate §9-B). Ввести ОДИН источник `window.TwinrModel` (новый аддитивный IIFE ПЕРЕД тремя потребителями) + переключить три модуля на него. **Byte-identical вывод** — это рефактор-без-смены-поведения. | новый shared-IIFE + точечные замены | med (но 0 визуальных изменений) |

---

## 1. Conflict-reconciliation (разрешение конфликтов с blueprint и built-кодом)

| Конфликт / вопрос | Разрешение | Доказательство (grounded) |
|---|---|---|
| **R1 vs «❌ числа-как-Wrapped» (§3 Recap anti-slop)** | Дельта = ПРИЧИННЫЙ сдвиг («+darkwave −арена-рок»), НЕ vanity-число («147 артистов»). Герой остаётся СЛОВО-идентичность (`recap-card-word` @9808), дельта — второй по весу ПОД словом. Не нарушает «слово, а не цифры»: дельта качественная, не количественная. | blueprint §3: «дельта-стрелка-герой» прямо предписана; §7 ВОЛНА 2 GOROD-050 «дельта-герой». Build-код уже имеет `cardDeltaHTML()` @13860 → переиспользуем, только поднимаем визуально. |
| **R2: html2canvas vs single-file офлайн-ограничение** | НЕ грузить html2canvas с CDN (нарушит self-contained прототип + сеть). **Primary path = ручной Canvas-2D рендер** из той же чистой модели (`buildIdentity/buildDeltas/buildDiscovery/buildPetals`) — детерминированный, honest, 0 зависимостей. `html2canvas` — опциональный progressive-enhance: ЕСЛИ `window.html2canvas` существует (кто-то подключил) — используем его; иначе Canvas-2D. **Никогда не падать в «пустой/битый PNG».** | `copySummary()` @13962 уже строит lines из модели → те же факты рисуем на canvas. `--bg-base` @112 = **radial-gradient**, НЕ flat → html2canvas её не возьмёт корректно → Canvas-2D рисует solid `#0B0C0F` + radial-glow вручную = честнее. blueprint §3: «реальный PNG 1080×1920». |
| **R2: honest-floor для PNG** | PNG подчиняется тому же honesty-floor, что и render: `hasRealSignal()` @14015 false → НЕ генерировать карточку (показать receipt «Профиль пуст»), как делает `copySummary` @13964. PNG не должен врать о прослушиваниях, которых не было. | `copySummary` @13963–13964 уже гейтит на `hasRealSignal()`. Зеркалим. |
| **R3 vs «приглашение к управляемости, НЕ guilt» (§2-D)** | CTA = приглашение оспорить («Не согласен? Поправь — пересчитается»), не упрёк. Если есть реальный minus (`buildDeltas().minus`) — цитирует его («Убрал X? Можно вернуть»); иначе — общий «Что-то не так? Поправь грань». | blueprint §2-C «micro-CTA "не согласен? поправь"»; §2-D «приглашение к управляемости, НЕ guilt». |
| **W6: «дедуп» vs «не ломать byte-identical data-model» (задача)** | Рефактор ОБЯЗАН быть behavior-preserving: `TwinrModel.facets()` возвращает идентичный массив тому, что три локальные `facets()` возвращают сейчас (та же FALLBACK, тот же slice(0,5), тот же readPicks slice(0,6)). Тест-инвариант в §4. GorodTaste использует ДРУГУЮ структуру (DEFAULT-группы @13124, не FALLBACK) — он остаётся на своей `seed()`, но шарит `REJ_LABELS`+`readRej` (единственное, что у него общее с Profile/Recap). | Grep подтвердил: `REJ_LABELS` идентичен во всех 3 (@13131/13670/13767); `FALLBACK` идентичен Profile/Recap (@13673/13768); `facets()` идентичен Profile/Recap (@13684/13776). GorodTaste `facets`-эквивалента не имеет (группы), поэтому шарит только REJ-часть. |
| **Где победил blueprint над задачей** | Задача просила «дельта-стрелка-герой … (не одно слово)» — реализуем как `+gained · −rejected`. Но blueprint §3 держит СЛОВО-идентичность главным героем экрана. Резолюция: дельта = ВТОРОЙ герой (под словом), не заменяет слово. | §3 «word-identity» + «дельта-стрелка-герой» сосуществуют → иерархия: слово(1) → дельта(2) → bloom(3). |

---

## 2. Line-anchored edit-manifest

> Все правки аддитивны. Порядок применения: W6 (shared-model) ПЕРВЫМ (остальные опираются на него), затем R/P.

### Манифест (по якорям, пересверено Read/Grep)

| ID | Файл-якорь (verbatim/строка) | Действие | Шов для Integrate |
|---|---|---|---|
| **W6-a** | НОВЫЙ `<script>` IIFE вставить **перед** `<!-- ---- GOROD-052 — «Открытый профиль» -->` @13660 (т.е. перед первым потребителем) | ДОБАВИТЬ `window.TwinrModel` (REJ_LABELS, FALLBACK, readPicks, readRej, facets, hasRealSignal) | новый global `window.TwinrModel` |
| **W6-b** | GorodProfile @13668–13689 (локальные `TASTE_KEY/REJ_KEY/REJ_LABELS/FALLBACK/readPicks/readRej/facets`) | ЗАМЕНИТЬ тела на делегацию к `TwinrModel` (см. §3) | — |
| **W6-c** | GorodRecap @13766–13781 (локальные те же) | ЗАМЕНИТЬ тела на делегацию к `TwinrModel`; `hasRealSignal()` @14015 → `TwinrModel.hasRealSignal()` | — |
| **W6-d** | GorodTaste @13130–13131 (`REJ_KEY`, `REJ_LABELS`) + `readRej` inline @13152 | ЗАМЕНИТЬ только REJ-часть на `TwinrModel.REJ_LABELS` / `TwinrModel.readRej()` (группы DEFAULT не трогать) | — |
| **R1-css** | recap CSS, после `.recap-card-defense` @2953 (внутри блока @2943–2954) | ДОБАВИТЬ `.recap-card-delta` усиление + новый `.recap-card-delta--hero` | новые классы (без новых токенов) |
| **R1-dom** | DOM `recap-card-inner` @9806–9813: переставить `recap-card-delta` @9810 ВЫШЕ bloom @9809; добавить класс-модификатор | reorder + class | byte-shift в одной figure |
| **R1-js** | `render()` @14038–14041 (порядок setText/setHTML) — порядок DOM-узлов меняется в HTML, JS-ID те же | НИЧЕГО (JS адресует по id, reorder в DOM не ломает) | — |
| **R2-dom** | `.recap-actions` @9817–9820 | ДОБАВИТЬ вторую primary-кнопку `id="recap-png"` + скрытый `<a id="recap-png-dl">` | новый узел |
| **R2-js** | GorodRecap, после `legacyCopy()` @13985, перед `/* ---- DOM glue ---- */` @13987 | ДОБАВИТЬ `renderPNG()` (Canvas-2D primary + html2canvas opt) + wire в `init()` @14053 | — |
| **R2-css** | после `.recap-receipt` @2964 | ДОБАВИТЬ `.recap-btn--primary-alt` (вторичный primary-стиль) | новый класс |
| **R3-dom** | `.recap-actions` ghost-кнопка @9819 + новый `<p>` после @9820 | переписать текст ghost + добавить micro-CTA узел | новый узел |
| **R3-js** | `render()` @14036 (после `disc`), и empty-ветка @14026 | ДОБАВИТЬ `setText('recap-cta-line', …)` причинно | новый id `recap-cta-line` |
| **P1-js** | GorodProfile `renderRejected()` @13715–13727 | ДОБАВИТЬ провенанс-строку каждому rej-чипу | — |
| **P1-css** | profile CSS, после `.profile-empty` @2918 | ДОБАВИТЬ `.profile-rej-prov` | новый класс |

---

## 3. DOM / CSS / JS verbatim

### 3.1 — W6: shared model (новый IIFE перед @13660)

ВСТАВИТЬ перед строкой 13660 (`  <script>` GOROD-052):

```html
  <!-- ---- TwinrModel — ЕДИНЫЙ источник граней+reject (W6 anti-fidelity dedup, blueprint §9-B).
       До этого REJ_LABELS / FALLBACK / facets() / readPicks / readRej дублировались в
       GorodProfile (@13668+) и GorodRecap (@13766+) — любая правка одного = расхождение
       views = fidelity-баг. Теперь обе читают ОТСЮДА → views не могут разойтись.
       Вывод BYTE-IDENTICAL прежним локальным функциям (рефактор без смены поведения). ---- -->
  <script>
  (function () {
    'use strict';
    var TASTE_KEY = 'gorodfm_taste', REJ_KEY = 'gorodfm_rejected';
    // canon id→label (mirror of TwinrWhy REASONS, GOROD-041) — единственная копия
    var REJ_LABELS = { artist: 'Егор Крид', vocal: 'Тёплый поп-вокал', tempo: 'Темп ~95 BPM' };
    // honest behavioral defaults — `prov` = КАК грань вошла в профиль, никогда маркетинг
    var FALLBACK = [
      { n: 'Арена-рок',      w: 80, prov: 'усилено: дослушиваешь до конца' },
      { n: 'Хип-хоп 2010-х', w: 66, prov: 'из прослушивания за месяц' },
      { n: 'Электро-поп',    w: 54, prov: 'по времени суток — вечер' },
      { n: 'Инди',           w: 40, prov: 'смежное — рядом с твоим вектором' }
    ];
    function readPicks() { try { return (JSON.parse(localStorage.getItem(TASTE_KEY) || '[]')).slice(0, 6); } catch (e) { return []; } }
    function readRej() { try { return JSON.parse(localStorage.getItem(REJ_KEY) || '[]'); } catch (e) { return []; } }
    function facets() {
      var out = [];
      readPicks().forEach(function (p) { out.push({ n: p, w: 84, prov: 'из онбординга — ты выбрал сам' }); });
      FALLBACK.forEach(function (f) { if (out.length < 5 && !out.some(function (o) { return o.n === f.n; })) out.push(f); });
      return out.slice(0, 5);
    }
    // provenance строки для оспоренных граней (P1) — КАК/ГДЕ оспорено, не маркетинг
    var REJ_PROV = 'оспорено на плеере: «почему?» → «не моё»';
    // cold profile (нет picks И нет reject) = нет реального поведения (см. GorodRecap honesty-floor)
    function hasRealSignal() { return readPicks().length > 0 || readRej().length > 0; }
    window.TwinrModel = {
      TASTE_KEY: TASTE_KEY, REJ_KEY: REJ_KEY, REJ_LABELS: REJ_LABELS, REJ_PROV: REJ_PROV,
      FALLBACK: FALLBACK, readPicks: readPicks, readRej: readRej, facets: facets, hasRealSignal: hasRealSignal
    };
  })();
  </script>
```

**W6-b — GorodProfile.** ЗАМЕНИТЬ @13668–13689 на делегацию (поведение byte-identical):

```javascript
    var M = window.TwinrModel;
    var REJ_KEY = M.REJ_KEY;                       // оставлено для существующих ссылок
    var REJ_LABELS = M.REJ_LABELS;                 // единый canon
    var els = {}, built = false, receiptTimer = 0;
    function $(id) { return document.getElementById(id); }
    function readRej() { return M.readRej(); }
    function facets() { return M.facets(); }
```
(удаляются локальные `TASTE_KEY`, `FALLBACK`, `readPicks`, тела `readRej`/`facets` — теперь из `M`.)

**W6-c — GorodRecap.** ЗАМЕНИТЬ @13766–13781 на:

```javascript
    var M = window.TwinrModel;
    var TASTE_KEY = M.TASTE_KEY, REJ_KEY = M.REJ_KEY;
    var REJ_LABELS = M.REJ_LABELS;
    var FALLBACK = M.FALLBACK;                      // оставлено: identity-карты ниже могут ссылаться по имени
    function readPicks() { return M.readPicks(); }
    function readRej() { return M.readRej(); }
    function facets() { return M.facets(); }
```
И @14015 `function hasRealSignal() { return readPicks().length > 0 || readRej().length > 0; }` → `function hasRealSignal() { return M.hasRealSignal(); }`.

**W6-d — GorodTaste.** @13130–13131 ЗАМЕНИТЬ:
```javascript
    var REJ_KEY = window.TwinrModel.REJ_KEY;
    var REJ_LABELS = window.TwinrModel.REJ_LABELS;   // canon (единый источник W6)
```
@13152 `var rej; try { rej = JSON.parse(localStorage.getItem(REJ_KEY) || '[]'); } catch (e) { rej = []; }` → `var rej = window.TwinrModel.readRej();`. (Группы DEFAULT @13124 НЕ трогать — у GorodTaste своя структура вектора.)

> **Загрузочный инвариант:** новый IIFE стоит ПЕРЕД @13660, а все три потребителя — IIFE, которые вызывают `M.*` только из `render()`/`onRoute()` (runtime, после `DOMContentLoaded`), не на parse-time. `window.TwinrModel` гарантированно определён к моменту первого route. Проверено: ни один потребитель не читает модель на верхнем уровне своего IIFE (GorodProfile @13679 только объявляет `els`, GorodRecap @13766+ только объявляет карты).

### 3.2 — R1: дельта-герой

**R1-dom** — переставить `recap-card-delta` @9810 ВЫШЕ bloom @9809 и добавить hero-класс. ЗАМЕНИТЬ @9808–9811:
```html
              <p class="recap-card-word" id="recap-card-word">Размах с битом</p>
              <p class="recap-card-delta recap-card-delta--hero" id="recap-card-delta"></p>
              <div class="recap-card-bloom" id="recap-card-bloom" aria-hidden="true"></div>
              <p class="recap-card-discovery" id="recap-card-discovery"></p>
```
(`recap-card-delta` поднят на одну позицию: word → delta → bloom → discovery → defense. JS @14040 адресует по id — reorder не ломает.)

**R1-css** — после @2953 (`.recap-card-defense …`) ДОБАВИТЬ:
```css
      /* R1 — дельта = ПРИЧИННЫЙ герой (НЕ vanity-число): второй по весу под словом */
      .recap-card-delta--hero { font-size: clamp(15px, 4.4vw, 18px); font-weight: 700; color: var(--text-pri); margin: 0 0 6%; line-height: 1.25; }
      .recap-card-delta--hero .grow { color: var(--success, #34d399); }
      .recap-card-delta--hero .fade { color: rgba(255, 255, 255, 0.55); }
```
**R1-js** — усилить `cardDeltaHTML()` @13860 (двухчастный +/− с классами для honest-цвета). ЗАМЕНИТЬ @13860–13865:
```javascript
    function cardDeltaHTML(d) {
      if (!d.plus) return '';
      var s = '<span class="grow">▲ +' + esc(d.plus.n) + '</span>';
      if (d.minus) s += ' <span class="fade">· −' + esc(d.minus.label) + '</span>';
      return s + ' <span class="recap-card-delta-tail">за неделю</span>';
    }
```

### 3.3 — R2: honest PNG 1080×1920

**R2-dom** — ЗАМЕНИТЬ `.recap-actions` @9817–9820:
```html
          <div class="recap-actions">
            <button class="recap-btn recap-btn--primary" id="recap-png" type="button">Сохранить картинку</button>
            <button class="recap-btn recap-btn--primary-alt" id="recap-copy" type="button">Скопировать текст</button>
            <a class="recap-btn recap-btn--ghost" id="recap-cta-link" href="#/taste">Поправить грань →</a>
          </div>
          <a id="recap-png-dl" style="display:none" aria-hidden="true"></a>
```

**R2-css** — после @2964 ДОБАВИТЬ:
```css
      .recap-btn--primary-alt { background: transparent; color: var(--text-pri); border: 1px solid var(--brand-blue-light); }
      .recap-btn--primary-alt:hover { background: var(--tint-blue-light-20, rgba(81, 104, 252, 0.16)); }
```

**R2-js** — после `legacyCopy()` @13985, перед `/* ---- DOM glue ---- */` @13987 ДОБАВИТЬ:
```javascript
    /* ---- honest PNG 1080×1920. Primary: Canvas-2D рендер из ТОЙ ЖЕ модели
       (buildIdentity/buildDeltas/buildDiscovery/buildPetals) — детерминированный,
       0 зависимостей, honest. html2canvas НЕ грузим с CDN (self-contained офлайн);
       если кто-то подключил window.html2canvas — используем как progressive-enhance.
       Никогда не рендерим пустоту: тот же honesty-floor, что и copySummary. ---- */
    var PNG_W = 1080, PNG_H = 1920;
    function withFont(px, weight) { return (weight || 700) + ' ' + px + "px Onest, 'Segoe UI', sans-serif"; }
    function wrapLines(ctx, text, maxW) {
      var words = String(text).split(' '), lines = [], cur = '';
      for (var i = 0; i < words.length; i++) {
        var t = cur ? cur + ' ' + words[i] : words[i];
        if (ctx.measureText(t).width > maxW && cur) { lines.push(cur); cur = words[i]; } else cur = t;
      }
      if (cur) lines.push(cur);
      return lines;
    }
    function drawCanvasPNG() {
      var c = document.createElement('canvas'); c.width = PNG_W; c.height = PNG_H;
      var ctx = c.getContext('2d');
      // honest near-black + brand-glow вручную (--bg-base = radial-gradient, html2canvas её не возьмёт)
      ctx.fillStyle = '#0B0C0F'; ctx.fillRect(0, 0, PNG_W, PNG_H);
      var g = ctx.createRadialGradient(PNG_W / 2, -150, 0, PNG_W / 2, -150, PNG_W * 0.95);
      g.addColorStop(0, 'rgba(81,104,252,0.16)'); g.addColorStop(1, 'rgba(81,104,252,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, PNG_W, PNG_H);
      var id = buildIdentity(), d = buildDeltas(), disc = buildDiscovery(), fs = facets();
      var cx = PNG_W / 2, y = 150, pad = 96, maxW = PNG_W - pad * 2;
      ctx.textAlign = 'center';
      // kicker
      ctx.fillStyle = '#8094ff'; ctx.font = withFont(30, 700);
      ctx.fillText('ГОРОД ФМ · НЕДЕЛЯ ' + isoWeek(), cx, y); y += 120;
      // hero word (identity)
      ctx.fillStyle = '#ffffff'; ctx.font = withFont(76, 800);
      wrapLines(ctx, id.phrase, maxW).forEach(function (ln) { ctx.fillText(ln, cx, y); y += 92; });
      y += 18;
      // R1 дельта-герой (причинный сдвиг)
      ctx.font = withFont(42, 700);
      if (d.plus) {
        ctx.fillStyle = '#34d399'; ctx.fillText('▲ +' + d.plus.n, cx, y); y += 60;
        if (d.minus) { ctx.fillStyle = 'rgba(255,255,255,0.55)'; ctx.fillText('− ' + d.minus.label, cx, y); y += 60; }
      }
      y += 24;
      // bloom (тот же векторный buildPetals → рисуем path'ы на canvas)
      drawBloomCanvas(ctx, fs, cx, y + 230, 1.35); y += 540;
      // discovery
      if (disc) { ctx.fillStyle = 'rgba(235,235,245,0.60)'; ctx.font = withFont(30, 600);
        wrapLines(ctx, 'Открытие: ' + disc.line, maxW).forEach(function (ln) { ctx.fillText(ln, cx, y); y += 42; }); y += 20; }
      // defense (provenance — fidelity)
      ctx.fillStyle = '#8094ff'; ctx.font = withFont(27, 500);
      wrapLines(ctx, id.defense, maxW - 60).forEach(function (ln) { ctx.fillText(ln, cx, y); y += 38; });
      // mark
      ctx.fillStyle = 'rgba(235,235,245,0.55)'; ctx.font = withFont(30, 700);
      ctx.fillText('Город ФМ', cx, PNG_H - 90);
      return c;
    }
    // bloom на canvas: переиспользуем buildPetals (viewBox 320×320, центр 160,160) → масштаб
    function drawBloomCanvas(ctx, fs, ox, oy, scale) {
      var petals = buildPetals(fs);
      function X(x) { return ox + (x - 160) * scale; }
      function Y(yv) { return oy + (yv - 160) * scale; }
      petals.forEach(function (p) {
        ctx.beginPath();
        // path d = "M160 160 Qax ay nx ny Qbx by 160 160 Z" → парсим числа
        var n = p.d.match(/-?\d+(\.\d+)?/g).map(Number);
        ctx.moveTo(X(n[0]), Y(n[1]));
        ctx.quadraticCurveTo(X(n[2]), Y(n[3]), X(n[4]), Y(n[5]));
        ctx.quadraticCurveTo(X(n[6]), Y(n[7]), X(n[8]), Y(n[9]));
        ctx.closePath();
        ctx.fillStyle = 'rgba(128,148,255,' + p.bladeOp + ')'; ctx.fill();
        ctx.lineWidth = 1.2; ctx.strokeStyle = 'rgba(81,104,252,' + p.stemOp + ')'; ctx.stroke();
        ctx.beginPath(); ctx.arc(X(p.nx), Y(p.ny), parseFloat(p.nodeR) * scale, 0, 6.2832);
        ctx.fillStyle = p.dom ? '#ffffff' : '#8094ff'; ctx.fill();
      });
    }
    function downloadCanvas(c) {
      try {
        var url = c.toDataURL('image/png');
        var a = $('recap-png-dl') || document.body.appendChild(document.createElement('a'));
        a.href = url; a.download = 'gorod-fm-nedelya-' + isoWeek() + '.png'; a.click();
        showReceipt('✓ Картинка сохранена — выложи в сторис'); if (window.TwinrWave) window.TwinrWave.bump();
      } catch (e) { showReceipt('Не удалось сохранить картинку — скопируй текст.'); }
    }
    function renderPNG() {
      if (!hasRealSignal()) { showReceipt('Профиль пуст — собери вкус, и картинку будет из чего собрать.'); return; }
      // progressive-enhance: пиксель-точный html2canvas, ЕСЛИ подключён; иначе honest Canvas-2D
      if (window.html2canvas) {
        var card = $('recap-card');
        window.html2canvas(card, { backgroundColor: '#0B0C0F', width: card.offsetWidth, height: card.offsetHeight, scale: PNG_W / card.offsetWidth })
          .then(downloadCanvas).catch(function () { downloadCanvas(drawCanvasPNG()); });
      } else { downloadCanvas(drawCanvasPNG()); }
    }
```
И `init()` @14053 ЗАМЕНИТЬ:
```javascript
    function init() {
      var bc = $('recap-copy'); if (bc) bc.addEventListener('click', copySummary);
      var bp = $('recap-png'); if (bp) bp.addEventListener('click', renderPNG);
      built = true;
    }
```

### 3.4 — R3: причинная micro-CTA

**R3-dom** — после `</div>` `.recap-actions` (новая @9820+ из R2-dom) и `recap-png-dl`, ДОБАВИТЬ перед `<p class="recap-receipt"…>` @9821:
```html
          <p class="recap-cta-line" id="recap-cta-line"></p>
```
**R3-css** — после R2-css блока ДОБАВИТЬ:
```css
      .recap-cta-line { text-align: center; font-size: 13.5px; line-height: 1.45; color: var(--text-sec); margin: 12px 0 0; }
      .recap-cta-line a { color: var(--accent-on-dark); font-weight: 700; text-decoration: none; }
      .recap-cta-line a:hover { text-decoration: underline; }
```
**R3-js** — в `render()` после @14041 (`setText('recap-card-discovery', …)`) ДОБАВИТЬ:
```javascript
      var minus = d.minus;
      setHTML('recap-cta-line', minus
        ? 'Не согласен, что ушло «' + esc(minus.label) + '»? <a href="#/taste">Верни грань →</a> — пересчитается.'
        : 'Слово собрано из реального вектора. Что-то не так? <a href="#/taste">Поправь грань →</a>');
```
И в empty-ветке @14026, после @14033 ДОБАВИТЬ: `setHTML('recap-cta-line', '');`

### 3.5 — P1: провенанс оспоренных граней

**P1-js** — GorodProfile `renderRejected()` @13715–13727 ЗАМЕНИТЬ цикл @13722–13726:
```javascript
      els.rej.innerHTML = '';
      rej.forEach(function (id) {
        var wrap = document.createElement('div'); wrap.className = 'profile-rej-item';
        var chip = document.createElement('span'); chip.className = 'profile-rej-chip'; chip.textContent = REJ_LABELS[id];
        var prov = document.createElement('span'); prov.className = 'profile-rej-prov'; prov.textContent = M.REJ_PROV;
        wrap.appendChild(chip); wrap.appendChild(prov);
        els.rej.appendChild(wrap);
      });
```
(`M` доступен из W6-b.)

**P1-css** — после `.profile-empty` @2918 ДОБАВИТЬ:
```css
      .profile-rej-item { display: inline-flex; flex-direction: column; gap: 3px; margin: 0 8px 10px 0; vertical-align: top; }
      .profile-rej-prov { font-family: 'Onest', sans-serif; font-size: 11.5px; color: var(--text-quat); display: inline-flex; align-items: center; gap: 5px; }
      .profile-rej-prov::before { content: ''; width: 4px; height: 4px; border-radius: 50%; background: var(--accent-on-dark); flex: none; }
```

---

## 4. Holy-Grail чеклист (HARD GATE)

- **Onest ONLY** — ✅ все новые узлы наследуют `'Onest', sans-serif`; Canvas-2D PNG `withFont()` использует `Onest` с fallback `'Segoe UI'` (canvas-fallback при отсутствии web-font в headless — допустимо, не на DOM).
- **ОДИН акцент** — ✅ только `--brand-blue-light #5168FC` / `--np-accent` / `--accent-on-dark #8094ff` / `--success #34d399` (success = разрешённый growth-токен, уже в recap @2951/2975). PNG hex'ы (`#5168FC`/`#8094ff`/`#34d399`/`#0B0C0F`) = те же токены литералами (canvas не читает CSS-var). **0 cyan, 0 #8b5cf6.**
- **❌ multi-stop gradient bg** — ✅ PNG-фон = solid `#0B0C0F` + ОДИН radial-glow (тот же single-hue паттерн, что `--bg-base` @112) = НЕ multi-stop.
- **❌ orb / ❌ fake-волна / ❌ gradient-плейсхолдеры / ❌ эмодзи-иконки / ❌ SVG-силуэты** — ✅ ничего не добавлено; bloom = реальный векторный `buildPetals` (петля = реальные веса). `▲`/`−` = текстовые символы дельты, не эмодзи-иконки.
- **≥44px hit** — ✅ `.recap-btn` @2958 `min-height:44px` наследуется новыми кнопками; ghost/link тоже.
- **focus-visible 3px** — ✅ `.recap-btn:focus-visible` @2963 покрывает новые кнопки; `.recap-cta-line a` — текст-ссылка (наследует focus).
- **prefers-reduced-motion** — ✅ новые узлы статичны; PNG-рендер не анимирован; bloom-карточка уже static @2988.
- **AA контраст** — ✅ `--accent-on-dark` (6.8:1) для мелкого текста (cta-line ссылка, rej-prov); `--text-pri`/`--text-sec` для крупного. Дельта-герой `--text-pri` + `--success`.
- **Demo-маркировка** — N/A: данные recap/profile = РЕАЛЬНЫЙ localStorage-вектор (не мок). Honesty-floor (`hasRealSignal`) гейтит PNG и render, чтобы не утверждать несуществующее поведение.
- **a11y (§10)** — ✅ `recap-cta-line`/`profile-rej-prov` = текст для AT; share-card `role=group` @9805 не тронут; bloom остаётся `aria-hidden` с текстовой alt в `recap-screen-bloom` @9824 (не тронут); новые кнопки имеют видимый текст-лейбл (screen-reader friendly).

---

## 5. Additive-safety / доказательство «не ломает built»

**Инвариант byte-identical data-model (задача требует явно).**
- `TwinrModel.facets()` = дословная копия прежних локальных `facets()` (Profile @13684 / Recap @13776 идентичны по Grep): тот же `readPicks().slice(0,6)` → push `w:84,prov:'из онбординга…'`, тот же FALLBACK-backfill `out.length < 5`, тот же `slice(0,5)`. → **тот же массив на том же localStorage.** Profile/Recap уже были byte-identical друг другу (комментарий @13758–13760); теперь это ГАРАНТИРОВАНО общим источником, а не совпадением.
- `buildIdentity`/`buildDeltas`/`buildDiscovery`/`buildPetals` (@13825/13849/13886/13897) НЕ тронуты → детерминированная word-identity и bloom неизменны.
- GorodTaste меняет только REJ-источник (@13130–13131, @13152) → его `applyRejections()` @13150 получает идентичный `rej`-массив (тот же localStorage-ключ) → вектор `#/taste` рендерится байт-в-байт как до W1-фикса. Группы DEFAULT @13124 не тронуты.

**R1 (дельта-герой).** Reorder DOM-узлов внутри одной `figure` @9806; JS адресует строго по `id` (@14038–14041) → порядок в DOM не влияет на запись. `cardDeltaHTML` усилен (двухчастный) — `deltaText` @13866 (для копирования текста) НЕ тронут, текст-шер не меняется. **Pixel-perfect Figma 2174:422 (#/home) НЕ затронут** — все правки в `#/recap`.

**R2 (PNG).** Полностью аддитивен: новая кнопка + новый JS-блок + opt-in html2canvas. `copySummary()` @13962 не тронут (переименована только видимая надпись кнопки «Скопировать текст», id `recap-copy` тот же, обработчик тот же). Если canvas/`toDataURL` падает → try/catch → receipt-fallback, **никогда не битый файл**. Honesty-floor зеркалит copySummary.

**R3 (CTA).** Новый узел `recap-cta-line` + ghost-кнопка остаётся (href `#/taste` тот же). Empty-ветка @14026 чистит cta-line → нет stale-текста на холодном профиле.

**P1 (провенанс reject).** `renderRejected()` @13715 меняет только разметку чипов (оборачивает в `.profile-rej-item` + prov-строка); empty-ветка @13718–13720 не тронута; `profile-rej-chip` класс сохранён (стиль @ существующий). Reject-данные не меняются.

**W6 (дедуп) — почему не ломает порядок загрузки.** Новый IIFE @перед-13660 выполняется на parse-time и сразу ставит `window.TwinrModel`. Все три потребителя обращаются к `M.*` только из `render()`/`onRoute()`/`renderRejected()` (runtime, после первого `hashchange`/`DOMContentLoaded`) — ни один не читает модель на верхнем уровне своего IIFE. → `TwinrModel` всегда определён к первому обращению. Если по какой-то причине порядок нарушится, потребители всё равно ссылаются `window.TwinrModel` лениво (внутри функций), а не захватывают в замыкание на parse-time для критичных путей (кроме `var M = window.TwinrModel` @top — но это после IIFE-вставки гарантированно non-null).

**Что НЕ трогаем (built, §7 «не пере-предлагать»):** `#/home` pixel-perfect, P0 «почему»/«исправь причину»/цвет-от-обложки, 046/048/049/050-base/051/052, de-purple, GorodTaste W1-reject-loop (только REJ-источник переключаем на общий, поведение тождественно), bloom-геометрия, identity-карты, ISO-неделя.

**Новые швы для фазы Integrate:**
- Новый global `window.TwinrModel` (W6) — будущие модули (Трек 047, карта вкуса) должны читать грани отсюда, не дублировать.
- Новые CSS-классы: `.recap-card-delta--hero`, `.recap-btn--primary-alt`, `.recap-cta-line`, `.profile-rej-item`, `.profile-rej-prov`. **Новых :root-токенов НЕТ.**
- Новые DOM-id: `recap-png`, `recap-png-dl`, `recap-cta-line`, `recap-cta-link`. **VALID_ROUTES не меняется, nav не меняется.**
- Опциональная зависимость `window.html2canvas` (progressive-enhance, не требуется) — если Integrate решит подключить пиксель-точный рендер, путь готов; без неё работает Canvas-2D.
