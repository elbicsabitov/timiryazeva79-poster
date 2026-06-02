---
title: "SPEC — #/taste «дом роста модели»: Сохранённое (архив) + строка стрика + AT-репрезентация вектора"
key: taste_saved
date: 2026-06-02
surface: "#/taste (Мой вкус)"
file: C:/Users/elbics/Desktop/design-project/designs/gorod-fm.html
status: build-ready
blueprint: docs/superpowers/BLUEPRINT-gorod-fm-full-service.md (§1.2 строки 65/72/73, §3 «Сохранённое» стр.115, §10.1 a11y стр.238, §7 ВОЛНА 1 GOROD-046 / ВОЛНА 2 GOROD-053)
template: docs/superpowers/SPEC-gorod-051-context-starts.md
supersedes: none (additive)
---

# SPEC — #/taste: Сохранённое + стрик + AT-вектор

> **Что это.** Расширение `#/taste` («Мой вкус») в единый **«дом роста модели»** (blueprint §3, стр.103). Три аддитивных блока, ставящиеся ПОД уже-построенным вектором (`#taste-body` @9716), не трогая ни вектор (GorodTaste W1 @13134), ни контекст-старты (051 @9679/14138), ни taste-sponsor (@9721):
> 1. **«Сохранённое»** — единый архив-аккордеон, впитывающий легаси-Медиатеку (`#/library` @7911) и легаси-Избранное (`#/favorites` @9241). Фильтры Треки/Артисты/Плейлисты/Станции. Каждый элемент → строка «что добавил в вкус». art-tint+монограмма ВМЕСТО gradient-обложек (которые сейчас в `--brand-cyan`/purple — нарушение «один акцент»).
> 2. **Строка стрика** «модель росла N дней» (053-lite, scripted, детерминированная — НЕ огонёк-эмодзи; рост = bloom-точки + волна-bump).
> 3. **AT-репрезентация вектора** (§10.1, прямое следствие north-star): `#taste-wave` @9655 `aria-hidden` → невидим для screen-reader. Добавляем `role="img"` + `aria-label` с текстовым составом вектора («вектор: Жанры — Арена-рок 80%…»), чтобы «видишь свою логику» работало и для незрячих.
>
> **Почему именно эти три вместе.** §3 (стр.103) определяет `#/taste` как «дом роста модели» = вектор + контекст-старты + recap + **стрик** + **Сохранённое**. Вектор/контекст/recap уже built. Стрик и Сохранённое — последние недостающие комнаты «дома». AT-вектор — не отдельная фича, а консистентность тезиса (§10.1: иначе north-star ломается для незрячих). Все три живут на одной поверхности → один спек, один аккордеон-каркас, одна route-уборка.
>
> **Все номера строк ниже — РЕАЛЬНЫЕ** (пересверены Read/Grep живого файла в этой сессии). Реализация СТРОГО аддитивна (новая DOM-секция-блок, новый CSS-блок, новый trailing-IIFE-модуль `GorodSaved`) — как 051/052.

---

## 0. Conflict-reconciliation table (разрешение конфликтов ПЕРЕД правкой)

| # | Конфликт / риск | Источник | Резолюция |
|---|---|---|---|
| C1 | **Куда впитать Медиатеку+Избранное?** Blueprint §1.2 (стр.72/73): MERGE обоих → «Сохранённое» в `#/taste`, route → redirect. §8 IA-реорг: «Сливать. Часть 046, средний риск». | BP §1.2, §8 | Сливаем в **новый блок `#taste-saved` внутри `#/taste`**, ПОД вектором/спонсором. Легаси-секции `#/library` @7911 и `#/favorites` @9241 **НЕ удаляются физически** (deep-link/закладки/carplay-boot-guard @11023/12183) — но скрываются из навигации + route→redirect на `#/taste#saved`. Полное удаление DOM = НЕ в этом спеке (отдельная Integrate-чистка). |
| C2 | **«Свалка» при слиянии двух архивов** (явный risk в задаче и §3 стр.115). | задача, BP §3 | СТРОГАЯ иерархия: один `<details>`-аккордеон (схлопнут по умолчанию, прогрессивное раскрытие — §1.2 стр.65 «прогрессивное раскрытие»), внутри — фильтр-чипы (Все/Треки/Артисты/Плейлисты/Станции) + плоский список `track-row`-паттерна. Никакой 2-row-grid (легаси `#/library`) и никакого отдельного list-экрана. Один компонент, один список. |
| C3 | **Asset-wall: gradient-обложки.** Легаси thumbs = `linear-gradient(135deg,#1a3a6e,#56afd7)` (@9291 и др.) → `#56afd7`/`#0ea8e8` = cyan-семья = нарушение Holy-Grail «один акцент». | Holy-Grail, BP §5 стр.115 | Новый блок использует **art-tint+монограмма** (детерминированный hue из имени, в СИНЕЙ семье → `--brand-blue-light`/`--accent-on-dark`), НЕ переносим legacy-градиенты. Это и есть «art-tint вместо gradient» (§3 стр.115). |
| C4 | **Демо-контент без маркировки = «perceived transparency» = смерть доверия** (Holy-Grail, §8 стр.211). | Holy-Grail | Архив-список = мок → **обязательный микро-лейбл «демо-архив»** в заголовке блока (как «демо-вектор» для Трека). Стрик scripted → подпись «демо · реальная логика = Ф1». |
| C5 | **Стрик не должен быть Duolingo-dark-pattern** (§8 стр.212: «переопределить — сигнал/правка, НЕ заход»). | BP §8 | Стрик = «модель росла N **дней правок**» (не «заходов»), визуал = bloom-точки (НЕ 🔥-эмодзи, иначе нарушение «❌ эмодзи-как-иконки»). N — детерминированный из `gorodfm_taste`-длины + базы, НЕ `Date.now()`-инкремент (фиделити: same localStorage → same N на reload, как GorodRecap/Profile). |
| C6 | **Дублирование счётчиков фильтров.** Легаси Избранное: Треки 47 / Артисты 12 / Плейлисты 38 / Станции 8 (@9263-9275). Легаси Медиатека: другой набор (треки/альбомы/плейлисты/подкасты @7931-7934). | @9263, @7931 | Берём **единый набор фильтров Избранного** (Треки/Артисты/Плейлисты/Станции — задача требует именно их), счётчики из мок-данных нового модуля. Альбомы/подкасты Медиатеки в MVP-архив НЕ тащим (они = generic-каталог, 0 wedge). |
| C7 | **AT-вектор: canvas `aria-hidden` обязан остаться декоративным** (§10.1 стр.238: «canvas остаётся декоративным `aria-hidden`, но рядом — semantic-summary»). | BP §10.1 | НЕ снимаем `aria-hidden` с canvas. Добавляем **отдельный визуально-скрытый (`.sr-only`) summary-узел** рядом с canvas, который GorodTaste наполняет текстом вектора в `render()`. SR читает summary, зрячий видит волну. |
| C8 | **GorodTaste владеет `data`-моделью вектора; GorodSaved не должен её дублировать/расходиться.** | grounded @13134 | Стрик и AT-summary **читают факты из того же localStorage (`gorodfm_taste`) детерминированно**; GorodSaved сам по себе НЕ хранит вектор. AT-summary генерит САМ GorodTaste в `render()` (у него уже есть `data`) — GorodSaved отвечает только за архив+стрик. Единая модель фактов (дедуп, BP §9-B W6). |
| C9 | **`#saved`-hash vs router.** Router резолвит только `#/`-роуты (`routeFromHash` @10954 проверяет `VALID_ROUTES`). `#/taste#saved` сломает резолв. | grounded @10954 | НЕ используем вложенный hash. Redirect легаси-routes ведёт на `#/taste` (чистый роут), а GorodSaved при заходе с `?scrollToSaved`-флага (set в redirect) делает `scrollIntoView` на блок. Альтернатива (проще, выбрана): redirect просто на `#/taste`, без авто-скролла — блок виден ниже вектора. Авто-скролл = опц. follow-up. |

---

## 1. Edit-manifest (line-anchored, в порядке применения)

Все якоря пересверены в живом файле. 4 правки: **3 аддитивных** (DOM-блок, CSS-блок, JS-модуль) + **1 микро-правка** к GorodTaste (`render()` пишет AT-summary). Плюс **раздел §5 «Shared seams»** — НЕ применять в этом спеке, передать в Integrate.

### EDIT-1 (DOM, additive) — вставить блок «Сохранённое» + стрик + AT-summary внутрь `.taste-stage`

**Якорь:** после taste-sponsor `</aside>` @9735 и ПЕРЕД `<p class="taste-foot">` @9737.
Уникальная строка-якорь для вставки ПОСЛЕ неё:
```
        </aside>
```
(это закрытие `#taste-sponsor`, строка 9735 — единственный `</aside>` внутри `.taste-stage`; для надёжности матчить блок 9734-9737 целиком, см. verbatim §2.1).

Вставляемое: (а) `<div class="taste-streak">` (стрик), (б) `<section class="taste-saved">` (Сохранённое-аккордеон). AT-summary — НЕ здесь; он вставляется рядом с canvas (EDIT-1b).

### EDIT-1b (DOM, additive) — AT-summary рядом с canvas

**Якорь:** строка 9655 (canvas), внутри `.taste-hero`:
```
            <canvas class="taste-wave" id="taste-wave" aria-hidden="true"></canvas>
```
Вставить СРАЗУ ПОСЛЕ неё узел `<p id="taste-vector-sr" class="sr-only" role="img" aria-label="…"></p>` (наполняется JS).

### EDIT-2 (CSS, additive) — новый блок стилей

**Якорь:** после последней `.taste-*`-строки CSS — `.taste-rej-cap{…}` @3144 и ПЕРЕД комментарием-разделителем @3145-3146:
```
      .taste-rej-cap { font-family: 'Onest', sans-serif; font-size: 12.5px; line-height: 1.5; color: var(--text-sec); margin: 0; }

      /* =====================================================================
```
Вставить блок `/* --- Saved archive + streak + AT-vector (SPEC-taste_saved) --- */` МЕЖДУ ними. Также добавить `.sr-only` ТОЛЬКО ЕСЛИ его нет (Grep: в файле есть `.visually-hidden` @7912 — переиспользуем `visually-hidden`, НЕ плодим `.sr-only`; см. §2.2 примечание).

### EDIT-3 (JS, additive) — новый trailing-IIFE `GorodSaved`

**Якорь:** перед закрывающим `</body>`/последним `<script>`-блоком — вставить ПОСЛЕ модуля GorodContext (закрытие @14138-14139 `window.GorodContext = …; })();`) тем же паттерном decoupled-IIFE, что 051. (Точный байт-якорь подтвердить Grep `window.GorodContext =` при реализации — модуль может эволюционировать; вставка идёт сразу за его `})();`.)

### EDIT-4 (JS, micro-edit к GorodTaste) — `render()` пишет AT-summary + дёргает стрик

**Якорь:** внутри `render()` GorodTaste, после построения групп и ПЕРЕД reject-картой — строка 13198 `body.appendChild(card); });` (конец `forEach` по группам) → ДОБАВИТЬ вызов `updateVectorSr(data)` и (опц.) `if(window.GorodSaved) window.GorodSaved.refreshStreak()`. Точный verbatim §2.3. Это ЕДИНСТВЕННАЯ правка существующего кода; чисто additive по поведению (новые строки, ничего не удаляется).

---

## 2. Verbatim DOM / CSS / JS

### 2.1 EDIT-1 + EDIT-1b — DOM verbatim

**EDIT-1b** — заменить строку 9655 на (canvas + sr-summary):
```html
            <canvas class="taste-wave" id="taste-wave" aria-hidden="true"></canvas>
            <p id="taste-vector-sr" class="visually-hidden" role="img" aria-label="Ваш вкусовой вектор">Ваш вкусовой вектор загружается…</p>
```

**EDIT-1** — вставить ПОСЛЕ блока taste-sponsor (после `</aside>` @9735), ПЕРЕД `<p class="taste-foot">` @9737:
```html

          <!-- Стрик «дни роста модели» (053-lite, scripted, детерминир.) — SPEC-taste_saved -->
          <div class="taste-streak" id="taste-streak" aria-live="polite">
            <div class="taste-streak-bloom" id="taste-streak-bloom" aria-hidden="true"></div>
            <div class="taste-streak-txt">
              <span class="taste-streak-n" id="taste-streak-n">—</span>
              <span class="taste-streak-cap">дней модель росла с твоих правок</span>
            </div>
            <span class="taste-streak-demo" aria-hidden="true">демо · логика роста = Ф1</span>
          </div>

          <!-- Сохранённое — единый архив (быв. Медиатека + Избранное), MERGE 046 — SPEC-taste_saved -->
          <details class="taste-saved" id="taste-saved">
            <summary class="taste-saved-sum">
              <span class="taste-saved-sum-l">
                <span class="taste-saved-title">Сохранённое</span>
                <span class="taste-saved-count" id="taste-saved-count">0</span>
                <span class="taste-saved-demo">демо-архив</span>
              </span>
              <svg class="taste-saved-chev" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
            </summary>
            <div class="taste-saved-body">
              <p class="taste-saved-lead">Что ты сохранил — и чем это кормит твою волну. Лайк здесь = сигнал в вектор, не просто закладка.</p>
              <div class="taste-saved-filters" role="group" aria-label="Фильтр сохранённого по типу" id="taste-saved-filters">
                <!-- chips injected by GorodSaved -->
              </div>
              <div class="taste-saved-list" id="taste-saved-list" role="list" aria-label="Сохранённое">
                <!-- rows injected by GorodSaved -->
              </div>
            </div>
          </details>
```

### 2.2 EDIT-2 — CSS verbatim

> **Примечание `.sr-only`:** файл уже имеет `.visually-hidden` (@7912). Переиспользуем его на AT-summary (EDIT-1b использует `class="visually-hidden"`). НЕ добавляем дубль-класс `.sr-only`. Если по Grep `.visually-hidden` окажется не глобально-определён — добавить стандартное правило в этот же блок; на момент спека он используется в `#/library` heading, т.е. определён.

Вставить между @3144 и @3145:
```css

      /* ===== Saved archive + streak + AT-vector (SPEC-taste_saved) ========= */
      /* Стрик «дни роста модели» — рост = bloom-точки, НЕ огонёк-эмодзи (Holy-Grail) */
      .taste-streak {
        display: flex; align-items: center; gap: 14px;
        margin: 4px 0 22px; padding: 14px 18px;
        background: var(--bg-card, rgba(255,255,255,0.03));
        border: 1px solid rgba(81, 104, 252, 0.22); border-radius: 14px;
      }
      .taste-streak-bloom {
        width: 40px; height: 40px; flex: none; border-radius: 50%;
        background: radial-gradient(circle at 50% 50%, var(--brand-blue-light) 0%, rgba(81,104,252,0.18) 55%, transparent 72%);
        box-shadow: 0 0 0 1px rgba(81,104,252,0.20);
        animation: taste-streak-pulse 2.8s ease-in-out infinite;
      }
      @keyframes taste-streak-pulse { 0%,100%{transform:scale(1);opacity:.92} 50%{transform:scale(1.12);opacity:1} }
      .taste-streak-txt { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; flex: 1; }
      .taste-streak-n { font-family: 'Onest', sans-serif; font-weight: 800; font-size: 26px; color: #fff; line-height: 1; font-variant-numeric: tabular-nums; }
      .taste-streak-cap { font-family: 'Onest', sans-serif; font-size: 13.5px; font-weight: 600; color: var(--text-sec); }
      .taste-streak-demo { font-family: 'Onest', sans-serif; font-size: 11px; font-weight: 600; color: var(--accent-on-dark); opacity: .85; letter-spacing: .02em; }

      /* Сохранённое — аккордеон (схлопнут по умолчанию = прогрессивное раскрытие) */
      .taste-saved { border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; background: var(--bg-card, rgba(255,255,255,0.03)); margin-bottom: 8px; overflow: hidden; }
      .taste-saved[open] { border-color: rgba(81,104,252,0.22); }
      .taste-saved-sum { list-style: none; cursor: pointer; display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 18px; -webkit-tap-highlight-color: transparent; min-height: 44px; }
      .taste-saved-sum::-webkit-details-marker { display: none; }
      .taste-saved-sum:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: -2px; border-radius: 14px; }
      .taste-saved-sum-l { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
      .taste-saved-title { font-family: 'Onest', sans-serif; font-weight: 800; font-size: 18px; color: #fff; letter-spacing: -0.01em; }
      .taste-saved-count { font-family: 'Onest', sans-serif; font-weight: 800; font-size: 13px; color: var(--brand-blue-light); }
      .taste-saved-demo { font-family: 'Onest', sans-serif; font-size: 11px; font-weight: 600; color: var(--accent-on-dark); opacity: .85; }
      .taste-saved-chev { width: 20px; height: 20px; color: var(--text-sec); transition: transform var(--t-fast); flex: none; }
      .taste-saved[open] .taste-saved-chev { transform: rotate(180deg); }
      .taste-saved-body { padding: 0 18px 18px; }
      .taste-saved-lead { font-family: 'Onest', sans-serif; font-size: 13px; line-height: 1.5; color: var(--text-sec); margin: 0 0 14px; }
      .taste-saved-filters { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
      .taste-saved-chip {
        font-family: 'Onest', sans-serif; font-size: 12.5px; font-weight: 700; letter-spacing: .03em;
        padding: 7px 13px; border-radius: var(--r-pill); cursor: pointer; min-height: 34px;
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.10); color: var(--text-sec);
        transition: background var(--t-fast), color var(--t-fast), border-color var(--t-fast);
      }
      .taste-saved-chip:hover { color: #fff; }
      .taste-saved-chip[aria-pressed="true"] { background: var(--tint-blue-light-20); border-color: rgba(81,104,252,0.45); color: #fff; }
      .taste-saved-chip:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }
      .taste-saved-chip-n { color: var(--accent-on-dark); margin-left: 5px; font-weight: 800; }
      .taste-saved-list { display: flex; flex-direction: column; gap: 8px; }
      .taste-saved-row { display: flex; align-items: center; gap: 12px; padding: 10px; border-radius: 12px; background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); }
      /* art-tint+монограмма ВМЕСТО gradient-обложек (Holy-Grail: цвет-от-контента, синяя семья) */
      .taste-saved-tint { width: 44px; height: 44px; flex: none; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-family: 'Onest', sans-serif; font-weight: 800; font-size: 16px; color: #fff; }
      .taste-saved-meta { display: flex; flex-direction: column; gap: 3px; min-width: 0; flex: 1; }
      .taste-saved-name { font-family: 'Onest', sans-serif; font-size: 14px; font-weight: 700; color: #eef0f6; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      .taste-saved-sub { font-family: 'Onest', sans-serif; font-size: 12px; color: var(--text-sec); }
      /* «что добавил в вкус» — мёртвый архив = доказательство роста (BP §3 стр.115) */
      .taste-saved-fed { font-family: 'Onest', sans-serif; font-size: 11.5px; font-weight: 600; color: var(--accent-on-dark); display: inline-flex; align-items: center; gap: 5px; }
      .taste-saved-fed::before { content: '↳'; opacity: .8; }
      .taste-saved-badge { font-family: 'Onest', sans-serif; font-size: 10px; font-weight: 800; letter-spacing: .06em; color: var(--text-sec); border: 1px solid rgba(255,255,255,0.12); border-radius: var(--r-pill); padding: 3px 8px; flex: none; }
      .taste-saved-empty { font-family: 'Onest', sans-serif; font-size: 13px; color: var(--text-sec); padding: 12px 0; text-align: center; }
      @media (max-width: 720px) { .taste-saved-fed { display: none; } }
      @media (prefers-reduced-motion: reduce) { .taste-streak-bloom { animation: none; } }
```

### 2.3 EDIT-3 — JS verbatim (новый trailing-IIFE, вставить после GorodContext `})();`)

```html
  <script>
  /* ---- GorodSaved — единый архив «Сохранённое» (MERGE Медиатека+Избранное, 046) +
     стрик «дни роста модели» (053-lite). Decoupled trailing-IIFE как 051/052.
     Архив = ДЕМО-данные (микро-лейбл «демо-архив»). art-tint+монограмма, НЕ gradient.
     Стрик = ДЕТЕРМИНИРОВАННЫЙ из gorodfm_taste (same storage → same N, фиделити). --- */
  (function () {
    'use strict';
    var TASTE_KEY = 'gorodfm_taste';
    // Демо-архив (мок). Каждый элемент: тип, имя, sub, «что добавил в вкус» (fed).
    var SAVED = [
      { type: 'track',    name: 'Believer',                    sub: 'Imagine Dragons · 03:38', fed: 'усилил Арена-рок' },
      { type: 'track',    name: 'Stressed Out',                sub: 'twenty one pilots · 03:22', fed: 'добавил Меланхолию' },
      { type: 'artist',   name: 'Молчат Дома',                 sub: 'артист · 12 треков',       fed: 'открыл пост-панк' },
      { type: 'artist',   name: 'OneRepublic',                 sub: 'артист · 31 трек',         fed: 'поднял Электро-поп' },
      { type: 'playlist', name: 'Город ФМ · Тёмный вечер',     sub: 'плейлист · 24 трека',      fed: 'сместил к darkwave' },
      { type: 'playlist', name: 'Дорога домой',                sub: 'плейлист · 18 треков',     fed: 'добавил 108 BPM' },
      { type: 'station',  name: 'ГОРОД РОК',                   sub: 'станция · 103.5 FM',       fed: 'закрепил Драйв' }
    ];
    var FILTERS = [
      { k: 'all',      label: 'ВСЕ' },
      { k: 'track',    label: 'ТРЕКИ' },
      { k: 'artist',   label: 'АРТИСТЫ' },
      { k: 'playlist', label: 'ПЛЕЙЛИСТЫ' },
      { k: 'station',  label: 'СТАНЦИИ' }
    ];
    var TYPE_BADGE = { track: 'ТРЕК', artist: 'АРТИСТ', playlist: 'ПЛЕЙЛИСТ', station: 'СТАНЦИЯ' };
    var cur = 'all', wired = false;

    function $(id) { return document.getElementById(id); }
    // детерминированный hue из имени → синяя семья (220-255°), НЕ радуга, НЕ cyan
    function tint(name) {
      var h = 0; for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) % 36;
      var hue = 218 + h;                         // 218..253° = синяя семья
      return 'linear-gradient(135deg, hsl(' + hue + ',62%,30%), hsl(' + hue + ',70%,48%))';
    }
    function mono(name) { var s = name.replace(/^Город ФМ · /, '').trim(); return (s[0] || '?').toUpperCase(); }
    function counts() {
      var c = { all: SAVED.length, track: 0, artist: 0, playlist: 0, station: 0 };
      SAVED.forEach(function (x) { c[x.type] = (c[x.type] || 0) + 1; });
      return c;
    }
    function renderFilters() {
      var wrap = $('taste-saved-filters'); if (!wrap) return;
      var c = counts();
      wrap.innerHTML = FILTERS.map(function (f) {
        var n = c[f.k] || 0;
        return '<button class="taste-saved-chip" type="button" data-f="' + f.k + '" aria-pressed="' + (f.k === cur) + '">' +
          f.label + (f.k === 'all' ? '' : ' <span class="taste-saved-chip-n">' + n + '</span>') + '</button>';
      }).join('');
    }
    function rowHtml(x) {
      return '<div class="taste-saved-row" role="listitem">' +
        '<span class="taste-saved-tint" style="background:' + tint(x.name) + '" aria-hidden="true">' + mono(x.name) + '</span>' +
        '<span class="taste-saved-meta">' +
          '<span class="taste-saved-name">' + x.name + '</span>' +
          '<span class="taste-saved-sub">' + x.sub + '</span>' +
          '<span class="taste-saved-fed">' + x.fed + '</span>' +
        '</span>' +
        '<span class="taste-saved-badge" aria-hidden="true">' + (TYPE_BADGE[x.type] || '') + '</span>' +
      '</div>';
    }
    function renderList() {
      var list = $('taste-saved-list'); if (!list) return;
      var items = SAVED.filter(function (x) { return cur === 'all' || x.type === cur; });
      list.innerHTML = items.length ? items.map(rowHtml).join('') : '<p class="taste-saved-empty">В этой категории пока пусто.</p>';
      var cnt = $('taste-saved-count'); if (cnt) cnt.textContent = SAVED.length;
    }
    function wire() {
      if (wired) return;
      var filters = $('taste-saved-filters'); if (!filters) return;
      filters.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-f]'); if (!btn) return;
        cur = btn.getAttribute('data-f');
        [].forEach.call(filters.querySelectorAll('[data-f]'), function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        renderList();
      });
      wired = true;
    }
    // Стрик: ДЕТЕРМИНИРОВАННЫЙ — база 6 + число пользовательских пиков (как растёт вектор). НЕ Date.now().
    function refreshStreak() {
      var n;
      try { n = 6 + (JSON.parse(localStorage.getItem(TASTE_KEY) || '[]') || []).length; } catch (e) { n = 6; }
      var el = $('taste-streak-n'); if (el) el.textContent = n;
    }
    function build() {
      renderFilters(); renderList(); wire(); refreshStreak();
    }
    function onRoute() {
      if (location.hash === '#/taste') {
        // ждём, пока GorodTaste отрисует #taste-body, затем строим архив ниже
        if ($('taste-saved-list')) build();
      }
    }
    window.GorodSaved = { build: build, refreshStreak: refreshStreak };
    window.addEventListener('hashchange', onRoute);
    if (document.readyState === 'complete' || document.readyState === 'interactive') onRoute();
    else window.addEventListener('DOMContentLoaded', onRoute);
  })();
  </script>
```

### 2.4 EDIT-4 — micro-edit к GorodTaste verbatim

В GorodTaste, ВНУТРИ `render()`, после `body.appendChild(card); });` (@13198, конец `Object.keys(data).forEach`) и ПЕРЕД `if (rejList.length) {` (@13199) — добавить:
```javascript
        // AT-репрезентация вектора (§10.1) — SR читает текст, canvas остаётся декоративным
        updateVectorSr();
        if (window.GorodSaved) window.GorodSaved.refreshStreak();
```
И добавить функцию `updateVectorSr` внутрь того же IIFE (рядом с `render`, перед `onRoute`):
```javascript
    // §10.1 — текстовый вектор для screen-reader (canvas #taste-wave = aria-hidden декор)
    function updateVectorSr() {
      var el = document.getElementById('taste-vector-sr'); if (!el) return;
      var parts = Object.keys(data).map(function (g) {
        var top = data[g].filter(function (r) { return !r.rej; }).slice(0, 3)
          .map(function (r) { return r.n + ' ' + r.w + '%'; }).join(', ');
        return g + ': ' + top;
      });
      el.setAttribute('aria-label', 'Ваш вкусовой вектор. ' + parts.join('. ') + '.');
      el.textContent = 'Вектор — ' + parts.join('; ') + '.';
    }
```

> **Почему EDIT-4 безопасен:** добавляются ТОЛЬКО новые строки. `updateVectorSr()` no-op если узел отсутствует (`if (!el) return`). `window.GorodSaved.refreshStreak()` guard'нут `if (window.GorodSaved)`. Существующая логика `render()` (группы, reject-карта, share, sonify) не тронута.

---

## 3. Holy-Grail чеклист (HARD GATE)

| Правило | Статус | Как соблюдено |
|---|---|---|
| Onest ONLY | ✅ | Все новые узлы — `font-family: 'Onest', sans-serif`. |
| near-black `#0B0C0F` + ОДИН акцент | ✅ | Фоны = `--bg-card`/rgba-white; акцент = `--brand-blue-light #5168FC`; мелкий текст = `--accent-on-dark #8094ff`. Ноль новых хардкод-цветов вне синей семьи. |
| art-tint hue в СИНЕЙ семье (не радуга, не cyan) | ✅ | `tint()` clamp 218–253° (`hsl`), монограмма — НЕ перенос legacy `#56afd7`-градиентов. C3. |
| ❌ multi-stop gradient bg | ✅ | Только 2-stop art-tint на 44px-плашках (контент-производный, не фон-страницы) + 1 radial bloom-точка (сигнал). |
| ❌ orb-аватар | ✅ | Стрик-bloom = 40px индикатор роста (motion=сигнал), НЕ аватар-орб. |
| ❌ fake-волна / ❌ gradient-плейсхолдеры вместо контента | ✅ | art-tint+монограмма = осознанный «цвет-от-контента» паттерн (нет per-track обложек), маркирован «демо-архив». |
| ❌ эмодзи-как-иконки | ✅ | Стрик = bloom-точка + chevron-SVG (C5). Ноль эмодзи в новой разметке/CSS (📌 в `is-pinned` — существующий, не трогаем). |
| ≥44px hit | ✅ | `.taste-saved-sum` min-height 44px; чипы min-height 34px (вторичные фильтры — допустимо, как существующие `.ctx-chip`/`.taste-rej-chip`; при ужесточении поднять до 44). |
| focus-visible 3px | ✅ | `.taste-saved-sum:focus-visible`, `.taste-saved-chip:focus-visible` = `3px solid var(--brand-blue-light)`. |
| prefers-reduced-motion | ✅ | `@media (prefers-reduced-motion: reduce){ .taste-streak-bloom{animation:none} }`. |
| motion = сигнал | ✅ | bloom-pulse = индикатор «модель живёт/растёт»; chevron-rotate = состояние аккордеона. Никакого decorative-motion. |
| Demo-маркировка | ✅ | «демо-архив» в summary + «демо · логика роста = Ф1» у стрика (C4). |
| a11y AT-вектор (§10.1) | ✅ | `#taste-vector-sr` `role="img"` + динамический `aria-label`; canvas остаётся `aria-hidden` декором (C7). aria-live на стрике/саммари наследуется (`aria-live="polite"` на `.taste-streak`). |
| Строгая иерархия (не свалка) | ✅ | Один `<details>`-аккордеон, схлопнут по умолчанию, один список, фильтр-чипы (C2). |

---

## 4. Additive-safety / не-ломает-built доказательство

- **Вектор W1 (GorodTaste @13134–13215)** — НЕ тронут по логике. Единственная правка (EDIT-4) добавляет 2 вызова + 1 функцию, все guard'нутые/no-op-safe. `data`-модель остаётся единственным источником (C8) — AT-summary читает её же, дедуп фактов (BP §9-B).
- **Контекст-старты 051 (`.ctx-strip` @9679, GorodContext @14138)** — новый блок вставлен ПОСЛЕ спонсора, контекст-стрип выше не сдвинут структурно. GorodContext не зависит от новых узлов.
- **taste-sponsor (@9721, renderSponsor @13242)** — не тронут; новый блок идёт строго после `</aside>`.
- **`#taste-wave` canvas / RAF (startWave @13052, stopWave)** — `aria-hidden` сохранён (C7); SR-узел отдельный. Перф не затронут (стрик-bloom = CSS-animation, паузится reduced-motion; нет нового RAF).
- **Роутер (@10954/11014/12175)** — этот спек НЕ меняет `VALID_ROUTES`, НЕ добавляет роутов, НЕ трогает redirect. Легаси `#/library`/`#/favorites` секции остаются физически (C1) → carplay-boot-guard @11023/12183 продолжает работать.
- **Изоляция модуля** — `GorodSaved` — отдельный IIFE с собственным `onRoute`, как 051. `build()` идемпотентен (`wired`-guard, `innerHTML`-перерисовка). Если GorodTaste ещё не отрисовал `#taste-body` — GorodSaved работает по своим узлам (`#taste-saved-list` статичен в DOM из EDIT-1), независимость сохранена.
- **Детерминизм (фиделити)** — стрик и archive — без `Math.random()`/`Date.now()`-инкремента; same `gorodfm_taste` → same N и same art-tint (hue из имени). Согласовано с W1-доктриной «фиделити-продукт детерминирован».

---

## 5. SHARED SEAMS — НЕ применять здесь, передать в фазу Integrate

Эти изменения касаются общих швов и сводятся отдельной Integrate-фазой (чтобы один спек не ломал nav/router глобально):

1. **Route-aliases / redirect (BP §1.2 стр.72/73, §8 IA-реорг).** `#/library` и `#/favorites` → redirect на `#/taste`. Точка правки: `routeFromHash`/`activatePage` (@10954/11014) или `initialRoute`-резолв (@12175). Сейчас НЕ трогаем (C1, C9).
2. **Nav-tile retire.** Удалить из tabbar плитку «Медиа» (`data-route="#/library"` @10691–10702). Плитка «Избранное» @10704 уже ведёт на `#/artist` (legacy-quirk) — Integrate решит: убрать или перенацелить на `#/taste`. Соответствующие promo/discover-карточки `href="#/library"` @7343 / `href="#/favorites"` @7417/8354 — перенацелить на `#/taste`.
3. **Cyan-retirement (Holy-Grail «один акцент»).** Этот спек НЕ вводит cyan и использует синюю семью. Но легаси-секции `#/library`/`#/favorites`, остающиеся в DOM, всё ещё содержат `#56afd7`/`#0ea8e8`-градиенты (@9291 и др.) и `--brand-cyan` (@88). Их ретайр — общий blueprint-долг §5, сводится Integrate (не в scope одного экрана).
4. **Опц. авто-скролл к `#saved`** после redirect (C9) — follow-up, если Integrate выберет deep-link на архив.

---

## 6. Реальные продукты (опора, с URL)

- **Spotify «Your Library» + Smart Filters (2025).** Один экран Библиотеки, фильтр-иконка top-left открывает Smart Filters (activity/mood/genre), grid↔list toggle. Подтверждает: **один архив + фильтр-чипы** (наш аккордеон-паттерн), но Spotify фильтрует по mood/genre — мы добавляем wedge-слой **«что добавил в вкус»**, которого у них нет (их библиотека = пассивный список, наша = доказательство роста модели). https://newsroom.spotify.com/2025-09-05/new-user-controls-personalize-listening/ , https://support.spotify.com/us/article/sort-and-filter/
- **Apple Music Library (iOS 26).** Tabs Songs/Artists/Albums + **pinned items** (закрепить артиста/альбом). Подтверждает паттерн фильтр-по-типу; мы берём Треки/Артисты/Плейлисты/Станции (тип-фильтр), но pin-логика у нас живёт на ВЕКТОРЕ (taste-pin @13166), не на архиве — архив = read-only «что сформировало вкус». https://support.apple.com/guide/music-web/sort-songs-apdmbb7c96e5/web
- **Вывод дифференциации.** Оба конкурента = архив как каталог-хранилище. Наш «Сохранённое» = архив как **причинная летопись роста вектора** (каждый элемент → «↳ усилил Арена-рок»). Это прямое продолжение north-star «видишь свою логику», перенесённое на архив — то, что §3 (стр.115) называет «мёртвый архив = доказательство роста».

---

## 7. Build order (для исполнителя)

1. EDIT-1b (canvas SR-узел) → EDIT-1 (DOM-блок) → EDIT-2 (CSS) → EDIT-3 (GorodSaved IIFE) → EDIT-4 (GorodTaste micro-edit).
2. Verify: `#/taste` рендерит вектор → ниже стрик «N дней» → ниже схлопнутый «Сохранённое (демо-архив)»; раскрытие → фильтры + список с art-tint+монограммой + «↳ …»; фильтр-чипы переключают; SR читает `#taste-vector-sr`.
3. Regression: контекст-старты, спонсор, reject-карта, share→recap, sonify — без изменений. carplay-boot не падает.
4. Shared seams §5 — НЕ в этом проходе.
