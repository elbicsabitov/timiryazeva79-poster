# GOROD-047a — Трек (#/track) — высший explainability-экран — Build Spec

> Auto-captured 2026-06-02 from research-workflow (Karpathy-tier: blueprint §3 «Трек ГЛАВНЫЙ» + AUDIT §4 + grounded live-read + 3 real products). BUILD-READY. Перестраивает legacy-slop `#/track` (SVG-дуги hero + 3-stop gradient covers + collaborative «Также любят слушать») в наш честный ответ Pandora «Why did you play this song?». Реализовать строго по этому спеку.
>
> **Target file:** `designs/gorod-fm.html` (verified — все line-anchors ниже пересверены против реального ~14.1k-строчного файла в этой сессии: track-section 8646–9182, track-CSS 5363–5887, NowPlayingTint @13403, TwinrWhy @13330, REASONS @13334, VALID_ROUTES @10931, последний trailing-IIFE GorodContext заканчивается @14139, `</body>` @14142).
>
> **Module:** новый decoupled trailing-script IIFE `window.GorodTrack` (зеркалит GorodContext/GorodTaste/GorodRecap паттерн) + REPLACE-in-place блока View-region `track-stage-cover` и footer-band. Single-file, аддитивно где возможно, **rework-in-place** для legacy-узлов (этот экран — legacy→rework, не legacy→merge).

---

## 0. Inputs reconciliation (resolved conflicts — read first)

Where the blueprint, AUDIT, the real file, and the 3 reference products diverge, the resolution is **binding**. Где блюпринт дал конкретные значения (BPM/энергия/вокал) — они авторитетны и воспроизведены ниже; не выдумывать значения вне этого набора.

| # | Conflict / ambiguity | Resolution (binding) | Why |
|---|---|---|---|
| **C1** | Брифовый якорь «NowPlayingTint @13393» vs grounded. | **`window.NowPlayingTint` = @13403–13432, `setProperty('--np-accent')` @13426, export @13430.** `TwinrWhy` export @13393 (это конец TwinrWhy, не Tint). Брифовые «~13235/~13393» сдвинуты — все якоря ниже пересверены. | Файл эволюционировал; биндимся к реальным строкам. |
| **C2** | `#/track` — full REPLACE секции (8646–9182) vs точечный rework? | **Точечный rework-in-place, НЕ полная замена.** Сохраняем рабочий каркас: hero-band scaffold (8649–8673), action-tabs (8675–8763), scrubber+transport (8766–8825), view-region контейнер (8827–8828, 9065), lyrics-view (8881–8912), history-view (8914–9063), `</section>` (9182). **Заменяем 4 узла:** (a) `.track-cover` SVG-арки (8656–8664) → art-tint+монограмма; (b) eyebrow (8653) — оставить, но source станет динамическим; (c) `track-stage-cover` up-next (8830–8879) → **«Почему играет» L2 + вектор трека + контекст-старт**; (d) footer-band «Также любят слушать» (9068–9177) → **«Соседи по атрибутам» с почему-сосед**. | Hero/scrubber/lyrics/history — не slop, они работают. Slop = (a) SVG-дуги, (b) gradient-covers, (c) generic up-next, (d) **collaborative «также любят»** (AUDIT §4 «жутко»). Реворкаем ровно их. |
| **C3** | «Почему играет» — куда положить? Брифовый «центр». | **Заменить view-region default-view `track-stage-cover` (8830–8879) на новый `track-stage-why`** — это центр экрана, открыт по умолчанию (`data-track-view="cover"` @8646 переименовать дефолт-вид в `why`). Up-next-карусель удаляется (дублирует `#/home` between-track 048 + не explainability). | Центр экрана = первое, что видит юзер после hero. Up-next = радио-функция, живёт на `#/home`; на deep-dive Трека место под explainability-payload (блюпринт §3: «центр “Почему играет” полное L2»). |
| **C4** | Вектор трека — SVG-дуги (как было) vs волна-мотив (бриф/блюпринт)? | **Волна-мотив: 4 горизонтальных bar-meter (BPM/Энергия/Вокал/Акустичность), НЕ SVG-дуги, НЕ радар.** Переиспользуем `.taste-bar`/`.taste-bar-fill` визуальный язык (@13168, проверенный единый компонент вектора). | Holy-Grail hard-gate: ❌ SVG-силуэты/дуги. Волна = вся идентичность (§5). bar-meter = тот же «вектор как заполненная полоса», что уже на `#/taste` → консистентность, zero нового визуального языка. |
| **C5** | Соседи: collaborative «вам также понравится» vs attribute-based. | **ТОЛЬКО attribute-based «почему-сосед».** Каждый сосед несёт ОДНУ конкретную причину-атрибут («тот же темп ~112 BPM», «тот же женский вокал», «та же эпоха 2012»). НЕ «фанаты также слушают», НЕ «вам понравится». | AUDIT §4 + grounded research: collaborative-«также любят» = «жутко» (creepy); Pandora MGP цитирует musicological genes; академ-консенсус — scrutable attribute-объяснение > latent CF для доверия. Это материализует north-star «показанное = реальная причина». |
| **C6** | Demo-данные без маркировки = смерть доверия (бриф hard-req + блюпринт §8). | **ОБЯЗАТЕЛЬНЫЙ микро-лейбл «демо-вектор» на блоке вектора И на блоке соседей.** Прототип-вектор/соседи захардкожены (нет реального CLAP per-track) → честно помечены. | Блюпринт §8 «Демо-вектор Трека/соседей»: «Красивый НЕнастоящий вектор без маркировки = perceived transparency = смерть доверия». Это и есть основной объём 047a. |
| **C7** | «Исправить причину» — новый механизм vs переиспользовать TwinrWhy? | **Переиспользовать существующий `gorodfm_rejected` контракт + REASON-id namespace.** Кнопка «исправить» у каждого L2-буллета пишет тот же `gorodfm_rejected` массив, что TwinrWhy (@13339) → reject отражается на `#/taste` (W1) и `#/profile`/`#/recap` (уже читают). НОВЫЙ модуль НЕ заводит свой LS-ключ для reject. | Единый reason_tag контур (блюпринт §4 moat + §9-B петля explain→reject→edit). Заводить второй reject-store = расфиделить петлю. Track-reject = тот же сигнал, просто из другой поверхности. |
| **C8** | Hero eyebrow «ГОРОД РОК · 103.5 FM» (@8653) + meta «Believer/IMAGINE DRAGONS» — на каком треке демонстрируем? | **Демо-трек = тот же now-playing, что в плеере: «Егор Крид» (REASONS @13335 = «Егор Крид», рынок=Москва).** Заменить hero meta `Believer/IMAGINE DRAGONS/Night Visions 2012` → согласовать с REASONS-нарративом (поп-вокал, ~95 BPM, вечер). | Fidelity: страница Трека должна цитировать ТОТ ЖЕ трек и ТЕ ЖЕ причины, что player-«почему» (REASONS @13334–13338). Imagine Dragons/Believer — англо-рок, расходится с REASONS «тёплый поп-вокал». Единый демо-трек = «Город» / Егор Крид (рынок Москва). |

No other conflicts.

---

## 1. Final placement + additive-safety proof (не ломает built, не триггерит 045)

### 1.1 Where it goes
- **CSS (REPLACE-in-place + ADD):** track-CSS блок 5363–5887. Заменяем `.track-cover` (5396–5425, SVG+gradient → art-tint), eyebrow цвет (5391, cyan → token). Заменяем `.track-up-next-*` блок (5517–5630) и `.track-also-*` блок (5785–5887) на новые `.track-why-*` / `.track-vector-*` / `.track-neighbor-*` правила (§6). Новый art-tint/монограмма CSS добавляется здесь же.
- **DOM (REPLACE-in-place):** внутри `<section data-page="track">` (8646–9182) заменяем 4 узла из C2. Hero scaffold / action-tabs / scrubber / lyrics / history — не трогаем.
- **Module (ADD):** `window.GorodTrack` IIFE — **последний trailing `<script>` перед `</body>`**, после строки 14140 (закрывающий `</script>` GorodContext), перед 14142 (`</body>`). Зеркалит GorodContext/GorodTaste паттерн.
- **JS controller (минимальная правка):** `setTrackView` viewStates (@11152) `['cover','lyrics','история']` → дефолт-вид рендерится модулем; контроллер не трогаем кроме одного: up-next-carousel-wiring (@11214–11227 `.track-up-next-card`) больше не имеет узлов → guard `if (trackSection)` уже null-safe (querySelectorAll вернёт пусто). **Изменений в контроллере не требуется** — удаление узлов безопасно (forEach по пустому списку = no-op).

### 1.2 Почему это безопасно — built не ломается, 045 не активируется
1. **Zero bytes в `#/home`.** Секция `data-page="home"` (@7443+), `.home-tile-row` (8 absolute-плиток Figma 2174:422), `.home-featured` — не тронуты. Никакой узел не входит в `.home-stage` flow → pixel-perfect сохранён byte-for-byte → gated-045 **не триггерится**.
2. **`#/taste` / вектор / контекст-старты 051 не тронуты.** GorodTaste (@13134 seed/render), GorodContext (@14065), `#taste-wave`, `gorodfm_taste` — нетронуты. W1 fidelity-петля цела.
3. **`gorodfm_rejected` контракт расширяется, НЕ переписывается** (C7). GorodTrack пишет тот же массив тем же форматом id-строк, что TwinrWhy (@13339–13343). REJ_LABELS (@13154) и applyRejections (@13150) на `#/taste` продолжают матчить. Новые track-reason-id, если их нет в REJ_LABELS, просто не матчат facet (graceful — пушатся в rejList как `matched:false`, ровно как сейчас неизвестные id).
4. **TwinrWhy (@13330) не тронут** — REASONS @13334, player-«почему?» @12836, why-pop — работают. GorodTrack — отдельный модуль на `#/track`, не перехватывает player.
5. **NowPlayingTint переиспользуется read-only.** GorodTrack читает `--np-accent` (`getComputedStyle(documentElement)`) для art-tint hero; НЕ переопределяет его, НЕ дёргает `NowPlayingTint.refresh()`. Если `--np-accent` не установлен (cover ещё не сэмплирован) → fallback `--brand-blue-light`. Zero coupling.
6. **Нет нового route.** `VALID_ROUTES` (@10931) уже содержит `#/track` — не модифицируется.
7. **Нет нового LS-ключа для reject** (C7). Демо-state модуля (раскрытый L2, выбранный сосед) — эфемерный in-memory, без localStorage (страница-демо, не персист-настройка). Единственное чтение LS = `gorodfm_rejected` (общий контракт). `gorodfm_taste`/`gorodfm_context`/`gorodfm_ad_less` не тронуты.
8. **Нет backend, флагов, гейтов.** Чистый клиент-UI. Демо-вектор/соседи захардкожены + помечены «демо-вектор» (C6).
9. **Up-next-carousel удаление безопасно:** контроллер-wiring @11214 (`.track-up-next-card`) → `forEach` по пустому NodeList = no-op, без ошибок. `setTrackView('cover')` default (@11204) → переименовываем дефолт-вид в `why` (правка C3), контроллер `viewStates` массив обновляется на `['why','lyrics','история']`.

---

## 2. Демо-контент — реальные параметры (захардкожены + помечены «демо-вектор»)

**Демо-трек (C8, согласован с REASONS @13334):** «Когда ты со мной» — Егор Крид · альбом «Дитя» · 2023. Поп. Hero eyebrow: `Сейчас играет · ГОРОД ПОП · 105.2 FM`.

**«Почему играет» — L2-причины** (каждая = действие/аудио-атрибут, каждая reject-абельна; параметрические, НИКОГДА маркетинг). id согласованы с TwinrWhy REASONS namespace где возможно:

| id | L1 (короткая) | L2-полная причина (что показываем) | reject-эффект |
|---|---|---|---|
| `artist` | Артист | Егор Крид — ты <b>дослушал до конца 3 раза</b> за неделю | пишет `'artist'` в `gorodfm_rejected` |
| `vocal` | Вокал | <b>Тёплый поп-вокал</b> (мужской) — паттерн, который ты часто дослушиваешь | пишет `'vocal'` |
| `tempo` | Темп | <b>105 BPM</b> — попадает в твой вечерний диапазон 90–110 | пишет `'tempo'` |
| `mood` | Настроение | Настроение «спокойно-тёплое» → <b>ты сам выбрал «Спокойно»</b> в контексте | пишет `'mood'` |

(`artist`/`vocal`/`tempo` совпадают с TwinrWhy REASONS-id @13335–13337 → reject с Трека отразится в той же `why-pop` и на `#/taste`. `mood` — новый id, graceful если нет в REJ_LABELS.)

**Вектор трека — 4 атрибута (bar-meter, «демо-вектор»):**

| Атрибут | Значение (label) | Заполнение бара % | Подпись-почему |
|---|---|---|---|
| Темп | 105 BPM | 58 | средний — твой вечерний диапазон |
| Энергия | средняя | 52 | ровная, без скачков |
| Вокал | мужской, тёплый | 78 | твой частый паттерн дослушивания |
| Акустичность | низкая | 30 | электронная аранжировка |

**Соседи по атрибутам (3, attribute-based «почему-сосед», «демо-вектор»):** монограмма + art-tint, ОДНА конкретная причина-связь. НЕ collaborative.

| Трек | Артист | Монограмма | Причина-сосед (одна) |
|---|---|---|---|
| Часики |ミёт (Miyagi & Эндшпиль) | ЧA | тот же темп ~105 BPM |
| Гипнозы | Markul | ГИ | тот же тёплый мужской вокал |
| Не свидимся | Скриптонит | НE | та же эпоха — релизы 2022–23 |

---

## 3. DOM structure — verbatim REPLACE blocks (semantics + a11y)

### 3.1 Hero cover — REPLACE 8656–8664 (SVG-арки → art-tint+монограмма)
Заменить узел `<div class="track-cover">…</div>` (8656–8664) на:
```html
            <!-- Art-tint cover: монограмма на однотонной плашке от цвета (НЕ fake-обложка, НЕ градиент) -->
            <div class="track-cover" id="track-cover" aria-hidden="true">
              <span class="track-cover-mono" id="track-cover-mono">ЕК</span>
            </div>
```
И обновить hero meta (8667–8671) под C8:
```html
            <h2 class="track-title" id="track-page-title">Когда ты со мной</h2>
            <p class="track-artist" id="track-page-artist">ЕГОР КРИД</p>
            <p class="track-album-line" id="track-page-album">альбом · Дитя · 2023</p>
```
И eyebrow (8653):
```html
            <p class="track-eyebrow" aria-hidden="true">Сейчас играет · ГОРОД ПОП · 105.2 FM</p>
```

### 3.2 «Почему играет» центр — REPLACE 8830–8879 (`track-stage-cover` up-next → why-block)
Заменить весь `<div class="track-stage-cover">…</div>` (8830–8879) на:
```html
            <!-- VIEW: why — ГЛАВНЫЙ explainability-блок (наш ответ Pandora MGP, честнее) -->
            <div class="track-stage-why">

              <!-- C. Почему играет — полное L2, каждый буллет = действие/аудио-атрибут + «исправить причину» -->
              <section class="track-why" aria-labelledby="track-why-h">
                <h2 class="track-why-title" id="track-why-h">Почему играет</h2>
                <ul class="track-why-list" id="track-why-list" role="list">
                  <!-- инжектится GorodTrack из WHY[] -->
                </ul>
                <p class="track-why-status" id="track-why-status" role="status" aria-live="polite"></p>
              </section>

              <!-- Вектор трека — 4 атрибута через bar-meter (волна-мотив, НЕ SVG-дуги) -->
              <section class="track-vector" aria-labelledby="track-vector-h">
                <div class="track-vector-head">
                  <h2 class="track-vector-title" id="track-vector-h">Вектор трека</h2>
                  <span class="demo-tag" aria-label="демонстрационные данные">демо-вектор</span>
                </div>
                <div class="track-vector-list" id="track-vector-list">
                  <!-- инжектится GorodTrack из VECTOR[] -->
                </div>
              </section>

            </div>
            <!-- /why view -->
```

### 3.3 Соседи по атрибутам — REPLACE 9068–9177 (collaborative «Также любят» → attribute-neighbors)
Заменить весь `<div class="track-also-band">…</div>` (9068–9177) на:
```html
          <!-- ---- E. Соседи по атрибутам — НЕ «вам также понравится» (attribute-honest, AUDIT §4) -->
          <div class="track-neighbors-band">
            <div class="track-neighbors-head">
              <h2 class="track-neighbors-heading">Рядом по звучанию</h2>
              <span class="demo-tag" aria-label="демонстрационные данные">демо-вектор</span>
            </div>
            <div class="track-neighbors-row" id="track-neighbors-row" role="list" aria-label="Треки с общим атрибутом">
              <!-- инжектится GorodTrack из NEIGHBORS[] -->
            </div>
          </div>
          <!-- /neighbors-band -->
```

a11y-гарантии:
- `<section aria-labelledby>` под существующим `<h1 id="page-track-heading">` (@8647) → корректная вложенность landmark/heading (h2 под h1).
- Каждый «исправить причину» = `<button type="button">`, ≥44px, focus-visible 3px.
- `#track-why-status` `role="status" aria-live="polite"` → reject анонсируется с реальной причиной («убрал “тёплый вокал” — пересчитываю»).
- bar-meter вектора имеет текстовую AT-репрезентацию: `aria-label` на каждой строке («Темп: 105 BPM, средний — твой вечерний диапазон») — вектор «видишь свою логику» работает для незрячих (блюпринт §10).
- Сосед = `<button role="listitem">` с `aria-label` содержащим причину-сосед.
- `.demo-tag` — текстовый лейбл (не color-only), `aria-label="демонстрационные данные"`.
- Zero emoji-as-icon. Монограмма = текст (буквы), не SVG-силуэт.

---

## 4. `window.GorodTrack` module (новый trailing IIFE)

Append после строки 14140 (закрывающий `</script>` GorodContext), последний блок перед `</body>` (14142). Детерминированный, null-guarded, `esc`-санитизированный, hashchange-wired. Читает общий `gorodfm_rejected` (C7), не заводит свой reject-store.

```html
  <script>
  /* ---- GOROD-047a — Трек: высший explainability-экран ----------------------
     Наш честный ответ Pandora «Why did you play this song?».
     «Почему играет» (L2, reject-абельно → общий gorodfm_rejected, как TwinrWhy) +
     вектор трека (bar-meter, демо-вектор) + соседи по АТРИБУТАМ (НЕ collaborative).
     Аддитивно: читает --np-accent read-only, не трогает home/taste/051. */
  (function () {
    'use strict';
    var REJ_KEY = 'gorodfm_rejected';   // ОБЩИЙ контракт с TwinrWhy (@13339) — не заводим свой
    // L2-причины: id совпадают с TwinrWhy REASONS где можно (artist/vocal/tempo) → reject отражается на #/taste и в why-pop
    var WHY = [
      { id: 'artist', short: 'Артист',     t: 'Егор Крид — ты <b>дослушал до конца 3 раза</b> за неделю' },
      { id: 'vocal',  short: 'Вокал',      t: '<b>Тёплый поп-вокал</b> (мужской) — паттерн, который ты часто дослушиваешь' },
      { id: 'tempo',  short: 'Темп',       t: '<b>105 BPM</b> — попадает в твой вечерний диапазон 90–110' },
      { id: 'mood',   short: 'Настроение', t: 'Настроение «спокойно-тёплое» → <b>ты сам выбрал «Спокойно»</b> в контексте' }
    ];
    var VECTOR = [   // демо-вектор: bar-meter, волна-мотив, НЕ SVG-дуги
      { k: 'Темп',         v: '105 BPM',        pct: 58, why: 'средний — твой вечерний диапазон' },
      { k: 'Энергия',      v: 'средняя',        pct: 52, why: 'ровная, без скачков' },
      { k: 'Вокал',        v: 'мужской, тёплый', pct: 78, why: 'твой частый паттерн дослушивания' },
      { k: 'Акустичность', v: 'низкая',         pct: 30, why: 'электронная аранжировка' }
    ];
    var NEIGHBORS = [  // attribute-based «почему-сосед» — ОДНА конкретная связь, НЕ «фанаты также»
      { mono: 'ЧA', title: 'Часики',      artist: 'Miyagi & Эндшпиль', why: 'тот же темп ~105 BPM' },
      { mono: 'ГИ', title: 'Гипнозы',     artist: 'Markul',            why: 'тот же тёплый мужской вокал' },
      { mono: 'НE', title: 'Не свидимся', artist: 'Скриптонит',        why: 'та же эпоха — релизы 2022–23' }
    ];

    function $(id) { return document.getElementById(id); }
    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function stripTags(s) { return String(s == null ? '' : s).replace(/<[^>]*>/g, ''); }   // для aria-label из <b>-разметки
    function getRej() { try { return JSON.parse(localStorage.getItem(REJ_KEY) || '[]'); } catch (e) { return []; } }
    function setRej(a) { try { localStorage.setItem(REJ_KEY, JSON.stringify(a)); } catch (e) {} }

    function renderWhy() {
      var list = $('track-why-list'); if (!list) return;
      var rej = getRej();
      list.innerHTML = '';
      WHY.forEach(function (r) {
        var isRej = rej.indexOf(r.id) !== -1;
        var li = document.createElement('li');
        li.className = 'track-why-row' + (isRej ? ' is-rejected' : '');
        li.setAttribute('role', 'listitem');
        li.innerHTML =
          '<span class="track-why-dot" aria-hidden="true"></span>' +
          '<span class="track-why-text">' + r.t + '</span>' +   // r.t = trusted literal с <b> (module const, не user input)
          '<button class="track-why-fix" type="button" aria-label="' +
            (isRej ? 'Вернуть причину: ' : 'Исправить причину: ') + esc(stripTags(r.t)) + '">' +
            (isRej ? 'вернуть' : 'исправить причину') + '</button>';
        li.querySelector('.track-why-fix').addEventListener('click', function () { toggle(r); });
        list.appendChild(li);
      });
    }
    function toggle(r) {
      var rej = getRej(), i = rej.indexOf(r.id), nowRej;
      if (i === -1) { rej.push(r.id); nowRej = true; } else { rej.splice(i, 1); nowRej = false; }
      setRej(rej); renderWhy();
      var st = $('track-why-status');
      if (st) { st.innerHTML = nowRej
        ? ('✓ Убрал причину «' + esc(r.short) + '» — пересчитываю волну. Виден и в «Мой вкус».')
        : ('Вернул «' + esc(r.short) + '» в причины.'); }
      if (window.TwinrWave) window.TwinrWave.bump();   // тот же видимый эффект, что TwinrWhy (@13373)
      if (nowRej && window.TwinrRibbon) window.TwinrRibbon.show('Убрал из волны: <b>' + esc(r.short) + '</b>. <span class="ai-why">меньше такого дальше</span>.');
    }

    function renderVector() {
      var box = $('track-vector-list'); if (!box) return;
      box.innerHTML = '';
      VECTOR.forEach(function (a) {
        var row = document.createElement('div');
        row.className = 'track-vector-row';
        row.setAttribute('aria-label', a.k + ': ' + a.v + ' — ' + a.why);   // AT-репрезентация (блюпринт §10)
        row.innerHTML =
          '<span class="track-vector-k">' + esc(a.k) + '</span>' +
          '<span class="track-vector-v">' + esc(a.v) + '</span>' +
          '<div class="track-vector-bar" aria-hidden="true"><div class="track-vector-fill" style="width:' + (a.pct | 0) + '%"></div></div>' +
          '<span class="track-vector-why">' + esc(a.why) + '</span>';
        box.appendChild(row);
      });
    }

    function renderNeighbors() {
      var row = $('track-neighbors-row'); if (!row) return;
      row.innerHTML = '';
      NEIGHBORS.forEach(function (n) {
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'track-neighbor'; b.setAttribute('role', 'listitem');
        b.setAttribute('aria-label', 'Трек ' + n.title + ' — ' + n.artist + '. Причина: ' + n.why);
        b.innerHTML =
          '<span class="track-neighbor-cover" aria-hidden="true"><span class="track-neighbor-mono">' + esc(n.mono) + '</span></span>' +
          '<span class="track-neighbor-meta">' +
            '<span class="track-neighbor-title">' + esc(n.title) + '</span>' +
            '<span class="track-neighbor-artist">' + esc(n.artist) + '</span>' +
            '<span class="track-neighbor-why">' + esc(n.why) + '</span>' +
          '</span>';
        row.appendChild(b);
      });
    }

    function tintCover() {
      var cover = $('track-cover'); if (!cover) return;
      // read-only: переиспользуем --np-accent (NowPlayingTint @13426), fallback на brand
      var c = getComputedStyle(document.documentElement).getPropertyValue('--np-accent').trim() || '#5168FC';
      cover.style.setProperty('--track-tint', c);
    }

    function render() { renderWhy(); renderVector(); renderNeighbors(); tintCover(); }

    function onRoute() { if ((location.hash || '') === '#/track') render(); }
    window.addEventListener('hashchange', onRoute);
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', onRoute); else onRoute();
    window.GorodTrack = { render: render };
  })();
  </script>
```

**Data model:** in-memory module-const (WHY/VECTOR/NEIGHBORS) — демо-данные (C6 маркированы в DOM). Единственный durable read/write = `gorodfm_rejected` (общий контракт, C7).
**Correctness / zero-console-errors:** try/catch на LS; null-guard на каждый `$()`; `esc()` на всех динамических строках; WHY-тексты = module-const trusted-литералы (`<b>` only) → `innerHTML` безопасен; `getComputedStyle` fallback `#5168FC`; zero `Math.random` (детерминизм — fidelity, как GorodTaste @13140); `bump`/`TwinrRibbon` guarded.

---

## 5. Player-«почему?» → ведёт на Трек (опционально, минимальная правка — рекомендация)

Сейчас «почему?» в плеере открывает why-pop (@12836). Чтобы Трек реально использовался как ГЛАВНЫЙ explainability-экран (бриф «используется на 10%»), why-pop кнопка «подробнее» (`#why-pop-more` @13388) уже ведёт в чат. **Рекомендация (не блокер):** оставить why-pop как быстрый L2, а в hero Трека дать связность. **В v1 правку плеера НЕ делаем** — Трек достижим из любой track-card (`data-track-title` wiring @11216/11229 на `#/track` навигацию уже существует). Один источник правды по reject (`gorodfm_rejected`) гарантирует: reject в why-pop и reject на Треке — один массив, отражаются друг в друге при ре-рендере (`hashchange` → `onRoute` → `renderWhy`).

---

## 6. CSS — tokens only (every var enumerated)

REPLACE/ADD в track-CSS блоке (5363–5887). **Никаких новых хардкод-цветов** сверх уже-существующих в файле white-шкал и RGB `81,104,252` (= `--brand-blue-light` #5168FC, паттерн файла @585).

### 6.1 Eyebrow — REPLACE 5391 (cyan → token, ретайр одного из 74 cyan-вхождений)
```css
        color: var(--accent-on-dark);   /* было var(--brand-cyan) — ретайр в синюю семью (§5) */
```

### 6.2 Cover — REPLACE 5396–5425 (gradient+SVG → art-tint+монограмма)
```css
      .track-cover {
        --track-tint: var(--brand-blue-light);
        width: 480px; max-width: 72vw; aspect-ratio: 1 / 1; height: auto;
        border-radius: 24px; flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
        /* art-tint: однотонная плашка от цвета обложки (--np-accent), НЕ multi-stop gradient */
        background: color-mix(in oklab, var(--track-tint) 22%, #111318);
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.55), 0 0 64px -16px var(--track-tint);
        position: relative; overflow: hidden;
      }
      .track-cover-mono {
        font-family: 'Onest', sans-serif; font-weight: 800;
        font-size: clamp(72px, 16vw, 132px); line-height: 1;
        color: #fff; letter-spacing: -0.02em;
        text-shadow: 0 2px 24px rgba(0,0,0,0.35);
      }
```
(Удаляются `.track-cover svg` @5410–5416 и `.track-cover::after` @5419–5425 — SVG-арки и cyan-shimmer больше не нужны.)

### 6.3 NEW — «Почему играет» + вектор + соседи + demo-tag (ADD после 5630, на месте удаляемых `.track-up-next-*`; и после 5887 на месте удаляемых `.track-also-*`)
```css
      /* ---- «Почему играет» (L2 explainability) ------------------------------ */
      .track-stage-why { width: 100%; max-width: 620px; margin: 0 auto; padding: 8px 24px 0; box-sizing: border-box; }
      .track-why { margin: 0 0 28px; }
      .track-why-title { font-family: 'Onest', sans-serif; font-weight: 800; font-size: 20px; color: #fff; margin: 0 0 14px; letter-spacing: -0.01em; }
      .track-why-list { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 10px; }
      .track-why-row {
        display: flex; align-items: center; gap: 11px; padding: 12px 13px;
        border-radius: 11px; background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07); transition: opacity var(--t-fast);
      }
      .track-why-row.is-rejected { opacity: 0.5; }
      .track-why-row.is-rejected .track-why-text { text-decoration: line-through; }
      .track-why-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--brand-blue-light); flex: none; }
      .track-why-text { flex: 1 1 auto; font-family: 'Onest', sans-serif; font-size: 14px; line-height: 1.45; color: rgba(255,255,255,0.86); }
      .track-why-text b { color: #fff; font-weight: 700; }
      .track-why-fix {
        flex: none; background: none; border: 1px solid rgba(255,255,255,0.16); color: var(--text-sec);
        font-family: 'Onest', sans-serif; font-size: 12px; font-weight: 600;
        padding: 7px 13px; min-height: 44px; border-radius: var(--r-pill); cursor: pointer;
        transition: color var(--t-fast), border-color var(--t-fast); white-space: nowrap;
      }
      .track-why-fix:hover { color: #fff; border-color: var(--brand-blue-light); }
      .track-why-fix:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }
      .track-why-status { margin: 12px 0 0; font-family: 'Onest', sans-serif; font-size: 13px; line-height: 1.5; color: var(--accent-on-dark); min-height: 18px; }

      /* ---- Вектор трека (bar-meter, волна-мотив) ---------------------------- */
      .track-vector { margin: 0 0 8px; }
      .track-vector-head { display: flex; align-items: baseline; gap: 10px; margin: 0 0 14px; }
      .track-vector-title { font-family: 'Onest', sans-serif; font-weight: 800; font-size: 20px; color: #fff; margin: 0; letter-spacing: -0.01em; }
      .track-vector-list { display: flex; flex-direction: column; gap: 12px; }
      .track-vector-row { display: grid; grid-template-columns: 92px auto 1fr; grid-template-rows: auto auto; column-gap: 12px; row-gap: 4px; align-items: center; }
      .track-vector-k { grid-column: 1; font-family: 'Onest', sans-serif; font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.92); }
      .track-vector-v { grid-column: 2; font-family: 'Onest', sans-serif; font-size: 13px; font-weight: 600; color: var(--accent-on-dark); white-space: nowrap; }
      .track-vector-bar { grid-column: 3; height: 6px; border-radius: var(--r-pill); background: rgba(255,255,255,0.08); overflow: hidden; }
      .track-vector-fill { height: 100%; border-radius: var(--r-pill); background: var(--brand-blue-light); }
      .track-vector-why { grid-column: 1 / -1; grid-row: 2; font-family: 'Onest', sans-serif; font-size: 12px; color: rgba(235,235,245,0.60); line-height: 1.4; }

      /* ---- demo-tag (микро-лейбл «демо-вектор») ----------------------------- */
      .demo-tag {
        display: inline-flex; align-items: center; font-family: 'Onest', sans-serif;
        font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
        color: var(--accent-on-dark); background: rgba(81,104,252,0.12);
        border: 1px solid rgba(81,104,252,0.28); border-radius: var(--r-pill);
        padding: 3px 9px; white-space: nowrap;
      }

      /* ---- Соседи по атрибутам (attribute-honest, НЕ collaborative) --------- */
      .track-neighbors-band { width: 100%; max-width: 620px; margin: 8px auto 0; padding: 0 24px; box-sizing: border-box; }
      .track-neighbors-head { display: flex; align-items: baseline; gap: 10px; margin: 0 0 14px; }
      .track-neighbors-heading { font-family: 'Onest', sans-serif; font-weight: 800; font-size: 18px; color: #fff; margin: 0; letter-spacing: -0.01em; }
      .track-neighbors-row { display: flex; flex-direction: column; gap: 10px; }
      .track-neighbor {
        display: flex; align-items: center; gap: 13px; width: 100%; text-align: left;
        padding: 10px 12px; min-height: 64px; cursor: pointer;
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
        border-radius: var(--r-base); transition: background var(--t-fast), border-color var(--t-fast);
      }
      .track-neighbor:hover { background: rgba(255,255,255,0.07); border-color: rgba(81,104,252,0.40); }
      .track-neighbor:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }
      .track-neighbor-cover {
        width: 48px; height: 48px; flex: none; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        background: color-mix(in oklab, var(--brand-blue-light) 20%, #191C24);
      }
      .track-neighbor-mono { font-family: 'Onest', sans-serif; font-weight: 800; font-size: 16px; color: #fff; }
      .track-neighbor-meta { display: flex; flex-direction: column; gap: 1px; min-width: 0; }
      .track-neighbor-title { font-family: 'Onest', sans-serif; font-size: 14px; font-weight: 700; color: #fff; }
      .track-neighbor-artist { font-family: 'Onest', sans-serif; font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.62); }
      .track-neighbor-why { font-family: 'Onest', sans-serif; font-size: 12px; font-weight: 600; color: var(--accent-on-dark); margin-top: 2px; }

      @media (prefers-reduced-motion: reduce) {
        .track-why-row, .track-why-fix, .track-neighbor { transition: none; }
      }
```

**Token inventory (каждый var):**
- `--brand-blue-light` (#5168FC, единственный акцент) — dot, bar-fill, focus-visible, cover tint fallback, glow shadow + RGB `81,104,252` для tint/border.
- `--accent-on-dark` (#8094ff, AA 6.8:1) — eyebrow (заменил cyan), why-status, vector-value, demo-tag, neighbor-why.
- `--np-accent` (content-derived от обложки, @127) — читается read-only через `--track-tint` для art-tint hero.
- `--r-base` (10px) — neighbor/cover радиусы. `--r-pill` (999px) — fix-кнопка, bar, demo-tag.
- `--t-fast` (180ms) — все transitions.
- `--text-sec` — fix-кнопка label (существующий токен).
- Onest only на каждом текст-узле.
- White-шкалы rgba — все pre-existing в файле.
- `#111318`/`#191C24` в `color-mix` — существующие surface-токены-значения (`--surface-1`/`--surface-2`, §5 AUDIT).
- **Не использованы:** `--brand-cyan` (намеренно ретайрится), `--success`, `--t-mid`, `--ease-*`. Никаких новых хардкод-hue.

---

## 7. Entry / route wiring

- **Нет нового route.** `VALID_ROUTES` (@10931) уже включает `#/track` — не тронут.
- **Module self-wires:** `hashchange` + `DOMContentLoaded`/immediate (`document.readyState` guard), независимо от главного роутера/`activatePage`. Действует только при `location.hash === '#/track'`.
- **Контроллер `setTrackView` (@11151):** обновить `viewStates` (@11152) `['cover','lyrics','история']` → `['why','lyrics','история']`; обновить дефолт в `swapTrackMeta` (@11204) `setTrackView('cover')` → `setTrackView('why')`; и `data-track-view="cover"` (@8646) → `data-track-view="why"`; action-tab `data-tab="..."` для cover-view (если есть) не существует в табах (табы = share/lyrics/история/favorite/watch @8687–8761) → no-op, дефолт-вид показывается через CSS-селектор по `data-track-view`. **CSS view-селекторы:** найти существующие `[data-track-view="cover"] .track-stage-cover { display: … }` правила и переименовать `cover`→`why` + класс `.track-stage-cover`→`.track-stage-why` (Grep `data-track-view` в CSS перед правкой — anchor-точка для Integrate-фазы).
- **Up-next-carousel-wiring (@11214–11227):** узлы `.track-up-next-card` удалены → `forEach` по пустому = no-op. Без изменений в контроллере.
- **Соседи-навигация:** GorodTrack-кнопки `.track-neighbor` в v1 — демо (no-op клик, как share @8698). Реальная навигация на под-трек = Ф1 (требует роутинг с track-id). aria-label несёт причину для AT.

---

## 8. Holy-Grail / anti-slop checklist

| Gate | Status | Evidence |
|---|---|---|
| **Onest only** | ✅ | Каждый текст-узел `font-family:'Onest',sans-serif`. No Inter/Roboto/system-ui. |
| **near-black bg + 1 accent** | ✅ | bg не тронут; единственный акцент `--brand-blue-light`; малый accent-текст `--accent-on-dark`. Cover art-tint = `--np-accent` (content-derived, разрешено §5). |
| **❌ SVG-дуги/силуэты** | ✅ | `.track-cover svg` (3 концентрич. круга @8658–8662) **удалён** → монограмма-текст. Вектор = bar-meter, НЕ SVG-дуги/радар. |
| **❌ multi-stop gradient bg / fake-обложка** | ✅ | 3-stop gradient cover (@5404, 8858) и все gradient up-next/history/also covers заменены на однотонный `color-mix(--track-tint 22%)` art-tint + монограмма. Никаких `linear-gradient` covers. |
| **❌ collaborative «вам также понравится»** | ✅ | «Также любят слушать» (@9070, AUDIT §4 «жутко») **удалён** → «Рядом по звучанию» с ОДНОЙ attribute-причиной на соседа («тот же темп 105 BPM»). |
| **❌ эмодзи-как-иконки / orb / gradient-placeholder** | ✅ | Монограмма = буквы (текст), не SVG/эмодзи; demo-tag = текст; `✓` в статусе — глиф в тексте (как TwinrWhy @13369), не иконка. |
| **demo-маркировка** | ✅ | `.demo-tag` «демо-вектор» на блоке вектора И соседей (C6, блюпринт §8) — текст + `aria-label`, не color-only. |
| **parametric copy, не маркетинг** | ✅ | Каждая L2-причина = действие/аудио-атрибут (105 BPM, дослушал 3×, мужской вокал, выбрал «Спокойно»). «тебе понравится» отсутствует. |
| **fidelity-петля (reason_tag)** | ✅ | «исправить причину» пишет ОБЩИЙ `gorodfm_rejected` (C7) → отражается на `#/taste` (W1) + `#/profile`/`#/recap`. Один контур, не второй store. |
| **targets ≥44px** | ✅ | `.track-why-fix` min-height 44px; `.track-neighbor` min-height 64px; cover-mono декоративен (`aria-hidden`). |
| **focus-visible 3px** | ✅ | `.track-why-fix`/`.track-neighbor` `outline:3px solid var(--brand-blue-light)`. |
| **prefers-reduced-motion** | ✅ | CSS отключает transitions на why-row/fix/neighbor. Вектор-fill — статичная ширина (без анимации). |
| **a11y AT-репрезентация** | ✅ | Вектор-строки `aria-label` (k+v+why); why `role=status aria-live`; соседи `aria-label` с причиной; cover `aria-hidden`. «Видишь свою логику» работает для незрячих (§10). |
| **WCAG AA** | ✅ | `#fff`/`rgba(255,255,255,.86)` текст на `.04` bg; малый accent = `--accent-on-dark` (6.8:1). |
| **zero console errors** | ✅ | try/catch LS; null-guard `$()`; `esc()`+`stripTags()` динамики; trusted-литерал `<b>` only; `getComputedStyle` fallback; zero `Math.random`; guarded `bump`/`Ribbon`. |
| **детерминизм (fidelity)** | ✅ | Нет `Math.random` — тот же `gorodfm_rejected` → byte-identical рендер при reload (как GorodTaste @13140, Recap, Profile). |

---

## 9. Implementer's edit manifest (ordered, line-anchored)

1. **CSS eyebrow** — REPLACE строку 5391 (`color: var(--brand-cyan)` → `var(--accent-on-dark)`).
2. **CSS cover** — REPLACE 5396–5425 (`.track-cover` gradient+`svg`+`::after` → art-tint+`.track-cover-mono`) per §6.2.
3. **CSS up-next → why/vector** — REPLACE блок `.track-up-next-*` (5517–5630) на §6.3 «Почему играет» + вектор + demo-tag правила. (Grep `.track-up-next` подтвердить полный диапазон удаления.)
4. **CSS also → neighbors** — REPLACE блок `.track-also-*` (5785–5887) на §6.3 neighbors-правила.
5. **CSS view-selectors** — Grep `data-track-view="cover"` и `.track-stage-cover` в CSS-зоне, переименовать `cover`→`why` + класс. (Anchor для Integrate.)
6. **DOM hero cover** — REPLACE 8656–8664 (SVG → монограмма) per §3.1; обновить eyebrow (8653) + meta (8667–8671) под C8.
7. **DOM why-block** — REPLACE 8830–8879 (`track-stage-cover` up-next → `track-stage-why`) per §3.2.
8. **DOM neighbors** — REPLACE 9068–9177 (`track-also-band` → `track-neighbors-band`) per §3.3.
9. **JS controller** — `viewStates` @11152 `['cover',…]`→`['why',…]`; `swapTrackMeta` @11204 `setTrackView('cover')`→`'why'`; `data-track-view="cover"` @8646 → `"why"`.
10. **Module** — append §4 `window.GorodTrack` `<script>` после строки 14140 (закрывающий `</script>` GorodContext), последний блок перед `</body>` (14142).

Все anchor-диапазоны (track-section 8646–9182, track-CSS 5363–5887, NowPlayingTint 13403–13432, TwinrWhy 13330–13395 / REASONS 13334, VALID_ROUTES 10931, GorodContext-конец 14139, `</body>` 14142) пересверены против текущего файла в этой сессии.

---

## 10. Shared seams (для Integrate-фазы)

- **Ретайр cyan:** §6.1 убирает 1 из 74 `--brand-cyan`/`#56afd7`-вхождений (eyebrow + cover shimmer/shadow `rgba(86,175,215)`). Полный ретайр cyan → отдельная Integrate-задача (блюпринт §5).
- **Общий `gorodfm_rejected`:** GorodTrack добавляет НОВЫЙ источник записи в существующий контракт (TwinrWhy писал, GorodTaste/Profile/Recap читали). Новый track-reason-id `mood` стоит добавить в REJ_LABELS (@13154) на `#/taste` чтобы reject `mood` тоже матчил facet (иначе graceful `matched:false`). — Integrate-решение.
- **`--np-accent` read coupling:** GorodTrack читает `--np-accent` read-only. Если будущий 045/per-track-tint поменяет источник — track-cover автоматически подхватит (через `--track-tint` fallback).
- **View-state переименование `cover`→`why`:** затрагивает CSS-селекторы `[data-track-view]` + `LS_KEYS.trackView` persisted-значение (старое `'cover'` в LS у вернувшегося юзера → guard: `setTrackView` отвергнет невалидный, дефолт отрендерится через CSS). — проверить Integrate.
- **Нет правок:** VALID_ROUTES, nav-плиток, `#/home`, `#/taste`, 051. routeChanges/navChanges = пусто.
