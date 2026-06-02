# GOROD-ONB — Онбординг augment: «Модель за 7 треков» + стриминг-import-seed — Build Spec

> Auto-captured 2026-06-02 from research-workflow (Karpathy-tier grounded read of live `designs/gorod-fm.html` + blueprint §3/§7 + 3 real products). BUILD-READY.
> **Поверхность:** `#/onboarding`. **AUGMENT, не rebuild.** Сохраняет built: пузыри (`window.GorodOnboarding` @12224) и резюме→музыка (VISION#7 @9586–9649 / @12532). Добавляет **только not-built** части блюпринта §3-Онбординг / §7-ВОЛНА-1: (A) экран «Вот как я понял тебя за N сигналов» = видимый редактируемый мини-вектор с поведенческой причиной под каждой строкой + «Поправь» (первая демонстрация управляемости — видимый wedge), (B) стриминг-import-seed (Last.fm/Spotify/Яндекс, opt-in fake-импорт + экран-подтверждение «убери лишнее»).
> Все номера строк ниже ПЕРЕСВЕРЕНЫ через Read/Grep живого файла в этой сессии (файл ~13.9k строк).

---

## 0. Inputs reconciliation (resolved conflicts — read first)

| # | Conflict / ambiguity | Resolution (binding) | Why |
|---|---|---|---|
| **C1** | Бриф: «модель за **7 треков**». Но пузыри — это сигналы выбора, не «прослушанные треки». | **Триггер = N≥7 выбранных пузырей** (`selectedNames().length >= 7`), а копи говорит **«7 сигналов»**, не «7 треков». Резюме-путь и import-путь тоже приводят к этому же экрану (там сигналов часто <7 — тогда копи «по твоему резюме» / «из импорта», без числа). | Прототип не проигрывает треки в онбординге — единственный честный счётчик = выбранные сигналы. Называть их «треками» = fidelity-нарушение (north-star «показанное = реальное»). Поведенческая причина под строкой («выбрал Linkin Park → рок↑») остаётся буквально-конкретной. |
| **C2** | Когда прерывать на экран модели? После 7-го тапа авто-прерывать ИЛИ показать по «Продолжить»? | **НЕ авто-прерывать в середине игры с пузырями.** Экран модели показывается, когда юзер сам нажал «Продолжить» (`onContinue`) ИЛИ «Собрать радио» (resume-build) ИЛИ «Импортировать» (новый seed-путь). Это **вставка между сбором и `#/home`**, не popup поверх живой физики. | Авто-прерывание на 7-м тапе убивает Apple-Music-bloom-механику (юзер ещё исследует ветки). Блюпринт §2-A говорит «после ~7 сигналов **прервать**» — но прерывание в точке намерения завершить (тап CTA), а не насильно. Сохраняет built-физику нетронутой. |
| **C3** | Куда ведёт «Поправь» на экране модели? | **«Поправь» = редактирование ПРЯМО на экране модели** (inline +/− по строкам мини-вектора), НЕ переход на `#/taste`. «Собрать радио» → `#/home`. Отдельная мелкая ссылка «Открыть полный профиль» ведёт на `#/taste` для тех, кто хочет глубже. | Первая демонстрация управляемости должна быть в потоке (один тап меняет вес на глазах), без выброса из онбординга. `#/taste` — дом роста модели для daily-driver, но в онбординге выброс туда = потеря momentum (TikTok-урок: держать в первой сессии до hook). |
| **C4** | Import: реально парсить файлы/OAuth или fake? | **Полностью fake/scripted, opt-in, on-device — как резюме-демо** (резюме уже честно маркирует «файл остаётся на устройстве»). Кнопка сервиса → 3-сек «нашли вкус» театр → экран-подтверждение с производным вектором + «убери лишнее». Никакого реального OAuth/сети. | Прототип = Ф0 (scripted AI, продаёт визию — блюпринт §4). Реальный Last.fm/Spotify export = Ф1+. Маркировка «демо-импорт» обязательна (как резюме «Демо: …») иначе perceived-transparency ломается. |
| **C5** | Last.fm/Spotify/Яндекс — какие сервисы? Spotify мёртв на РФ-2026 (блюпринт §6). | **Ship: Last.fm + Яндекс Музыка + ВК Музыка** как fake-источники (Spotify УБРАТЬ из списка — на РФ-рынке мёртв даже как UX-демо для импорта истории; держать только то, чем москвич реально пользуется). | Блюпринт §6: «Path B (Spotify SDK) на РФ-2026 как бизнес-путь мёртв». Список источников должен читаться правдоподобно для целевого рынка (Москва). Last.fm scrobble-история — реальный кросс-платформенный артефакт, которым пользуются меломаны (beachhead-сегмент §6). |
| **C6** | Дублирует ли это резюме-модал (тоже «производный объяснённый вкус»)? | **Нет — разные двери, один общий экран модели.** Резюме = парс текста о личности → вкус. Import = «история прослушиваний из сервиса» → вкус. Пузыри = ручной выбор. **Все три сходятся на ОДНОМ экране модели** (§3) — единый момент «вот как я тебя понял», источник честно подписан («из пузырей» / «по резюме» / «из Last.fm»). | DRY: один экран модели, не три. Источник = провенанс-строка (тот же fidelity-принцип, что REASONS). Это и есть «единая модель фактов», на которой настаивает блюпринт §9-B. |
| **C7** | Нужен ли durable-флаг «онбординг пройден» (для cold-start W0)? | **Да. Вводим LS-ключ `gorodfm_onboarded`** — пишется при выходе с экрана модели (`gorodfm_onboarded='1'`). Сегодня его НЕТ в файле (Grep: 0 вхождений). Блюпринт W0 cold-start-ветка ссылается на него — этот спек его и создаёт. | Cold-start (W0, отдельная задача DEFAULT_ROUTE) хочет «нет `gorodfm_taste` И нет `gorodfm_onboarded` → форсить `#/onboarding`». `gorodfm_taste` пишется при каждом тапе пузыря (даже без завершения), поэтому он плохой признак «прошёл онбординг». `gorodfm_onboarded` = чистый признак «видел экран модели, ушёл в приложение». |

Где бриф/блюпринт дали конкретику (поведенческие причины, не-«специально для тебя») — она авторитетна и воспроизведена ниже. **Не выдумывать причины-маркетинг.**

---

## 1. Финальное размещение + additive-safety доказательство

### 1.1 Где это живёт
- **DOM (2 новых блока):**
  1. **`<div class="onb-model" id="onb-model">`** — fixed-overlay экран модели (z-260, выше resume-modal z-250), вставляется **сразу после `</div>` закрытия `#resume-modal` (после строки 9648 `</div>` / 9649 `<!-- /resume-modal -->`), перед `<!-- Page: Мой вкус -->` (строка 9651).**
  2. **Расширение `.onb-foot`** (строки 9568–9581): добавить ОДНУ кнопку `#onb-import` после `#onb-alt` (строка 9580) — вход в import-seed. Import переиспользует тот же overlay-механизм, что и резюме (новый шаг внутри model-overlay — см. §3.3).
- **CSS:** новый блок вставляется **после строки 2453** (конец resume-modal media-query `@media (max-width: 760px)`), перед `/* TWINR AI CHAT */` (строка 2455).
- **JS:** все правки — ВНУТРИ существующего IIFE `GorodOnboarding` (12224–12752), аддитивно:
  - `onContinue` (12712) перехватывается → вместо прямого `#/home` показывает экран модели; «Собрать радио» в модели → реальный переход (новая функция `goHome()`).
  - resume-build (12696) и import → тоже через экран модели.
  - Новый под-модуль `Model` (state экрана модели) + `Import` (fake-источники) внутри того же IIFE.

### 1.2 Почему это чисто аддитивно
1. **Пузыри-физика не тронута.** `build/scatter/step/makeBubble/spawnChildren` (12419–12517) — 0 байт изменений. Экран модели рисуется ПОВЕРХ (fixed overlay), пузыри под ним замораживаются (`stop()` уже есть @12737, вызовем при показе модели).
2. **Резюме-flow не тронут.** `resume-modal` DOM (9586–9649), CSS (2310–2453), JS (12532–12710) — без изменений, КРОМЕ одной строки: `resume-build` (12696) сейчас `applyDerived(); closeResume(); onContinue();` — `onContinue` теперь ведёт на экран модели вместо `#/home`. Это и есть желаемое (резюме → видит модель → правит → радио). Поведение апгрейдится, не ломается.
3. **`onContinue` (12712) — единственная точка перехвата.** Сегодня: `saveTaste(); location.hash='#/home'; greetFromOnboarding`. Станет: `saveTaste(); Model.show(source)`. Реальный переход на `#/home` + `greetFromOnboarding` переезжает в новую `goHome()`, вызываемую кнопкой «Собрать радио». Один и тот же `selectedNames()` → `greetFromOnboarding` сохраняется байт-в-байт.
4. **Нет нового роута.** Экран модели и import — overlay'и на `#/onboarding` (как resume-modal). `VALID_ROUTES` @10931 не трогается.
5. **Новый LS-ключ `gorodfm_onboarded`** изолирован — `gorodfm_taste`/`gorodfm_rejected`/`gorodfm_context` не трогаются. Запись `'1'` при `goHome()`.
6. **`#/home` / Figma 2174:422 / `#/taste` — 0 байт.** Gated 045 НЕ триггерится (онбординг — отдельная full-bleed поверхность @2055, своя fixed-секция).
7. **Не ломает уже-built:** GorodTaste `seed()` @13134 читает `gorodfm_taste` — мы пишем туда тот же массив имён, что и пузыри (`saveTaste` формат — массив строк). Экран модели НЕ меняет формат `gorodfm_taste` (он визуализирует его + позволяет +/−, сохраняя обратно тем же массивом-строк). → GorodTaste/Profile/Recap читают как раньше.
8. **TwinrChat.greetFromOnboarding** (@12993) вызывается из `goHome()` тем же `selectedNames()` — контракт сохранён.

---

## 2. Данные: мини-вектор «модель за N сигналов» (детерминированно, поведенчески)

Экран модели строит мини-вектор ИЗ выбранных пузырей/производного источника — **каждая строка = реальный выбор + поведенческая причина**, никогда «специально для тебя».

**Маппинг сигнал → грань (детерминированный, без random).** Жанровый пузырь (UPPERCASE, как в `DATA` @12227) → грань-жанр. Артист-пузырь → грань-артист + его жанр-нота. Резюме/import дают `{name, why}` напрямую (резюме уже это делает @12582).

**Структура строки мини-вектора** (мирроринг GorodTaste `DEFAULT` @13123 — те же группы Жанры/Настроения/Артисты, тот же %-вес):
```js
{ name: 'Рок', weight: 78, why: 'выбрал Linkin Park и РОК → рок в центре вектора', kind: 'genre' }
```

**Веса — детерминированно по порядку выбора** (как GorodTaste @13141, `Math.max(72, 90 - i*3)` паттерн — переиспользуем ту же формулу):
```js
function weightFor(i){ return Math.max(58, 88 - i * 4); }   // 88,84,80,… пол 58
```

**Поведенческие причины — параметрические шаблоны** (никогда маркетинг; `<b>` вокруг сигнала, trusted literal — module constant, не user-input):
- genre-pick: `Выбрал <b>{LABEL}</b> — поставил {label_lc} в центр вектора.`
- artist-pick: `Тапнул <b>{ARTIST}</b> → подтянул {genre_lc} и похожих.`
- artist+bloom (если юзер раскрыл ветку артиста): `Раскрыл ветку <b>{ARTIST}</b>, выбрал {n} похожих → {genre_lc} усилен.`
- mood (выводится из набора жанров, не из пузыря-настроения — их в DATA нет): если среди выбранных есть РОК/МЕТАЛЛ → `Энергичное` (why: `рок и тяжёлое в выборе → энергичный профиль`); если ЛОФАЙ/ДЖАЗ/КЛАССИКА → `Спокойное`; если ХИП-ХОП/ЭЛЕКТРО/ДИСКО → `Драйв`. Берём максимум 1–2 настроения, чтобы вектор не раздувался.
- resume-source: причина приходит из `deriveTaste` (@12582 `it.why`) как есть.
- import-source: причина = `прослушал {N}× в {SERVICE}` (см. §2.1).

**Источник-провенанс (честная подпись сверху мини-вектора):**
- `bubbles` → `Собрал из {N} выбранных тобой сигналов.`
- `resume` → `Собрал из твоего резюме — каждый пункт объяснён.`
- `import` → `Вытащил из истории {SERVICE} — каждый пункт объяснён.`

### 2.1 Стриминг-import-seed — fake-источники (§3.3)

| key | label (кнопка) | seed-вкус `[{name, plays, why}]` (демо-данные, помечены) |
|---|---|---|
| `lastfm` | Last.fm | `Инди`(214× прослушал), `Рок`(180×), `Электро`(96×), `Arctic Monkeys`(artist), `Tame Impala`(artist) |
| `yandex` | Яндекс Музыка | `Поп`(значимо), `Хип-хоп`(значимо), `Электро`(средне), `Егор Крид`(artist), `Macan`(artist) |
| `vk` | ВК Музыка | `Хип-хоп`, `Рэп`, `Поп`, `Макс Корж`(artist), `Скриптонит`(artist) |

Причина для import: `Прослушал <b>{plays}×</b> в {SERVICE} — добавил в стартовый вкус.` (для artist-строк: `Часто слушал <b>{ARTIST}</b> в {SERVICE}.`).
Каждое имя, совпадающее с пузырём (`byName`), при «Собрать радио» подсвечивает соответствующий пузырь (как `applyDerived` @12669) — fidelity: вектор = реальный набор сигналов.

**Demo-маркер ОБЯЗАТЕЛЕН** (микро-лейбл, как резюме @9600): import-шаг показывает `Демо: реальная история не загружается — показываем пример вкуса из {SERVICE}.`

---

## 3. DOM structure (семантика + a11y)

### 3.1 Расширение `.onb-foot` (одна кнопка после строки 9580)
Вставить **после** `</button>` строки 9580 (`#onb-alt`), перед `</footer>` (9581):
```html
            <button class="onb-alt onb-alt--import" id="onb-import" type="button">
              или импортируй вкус из Last.fm · Яндекс · ВК
            </button>
```

### 3.2 Экран модели + import-overlay (вставить между строкой 9648 `</div>` и 9651)
Единый overlay с тремя возможными шагами (model — основной; import-pick и import-result — для import-двери). Native `<button>`, `role="dialog"`, live-region для квитанций, demo-маркер.

```html
      <!-- GOROD-ONB — «Модель за N сигналов» + стриминг-import (augment онбординга) -->
      <div class="onb-model" id="onb-model" role="dialog" aria-modal="true" aria-labelledby="onb-model-title" aria-hidden="true">
        <div class="onb-model-backdrop" id="onb-model-backdrop" aria-hidden="true"></div>
        <div class="onb-model-panel" role="document">

          <!-- STEP: import source picker (only via «импортируй») -->
          <div class="onb-model-step" id="onb-import-pick" hidden>
            <h2 class="onb-model-title">Откуда взять вкус?</h2>
            <p class="onb-model-sub">Демо: реальная история не загружается — соберём правдоподобный пример из выбранного сервиса. Ты увидишь и поправишь каждый пункт.</p>
            <div class="onb-src-row" role="group" aria-label="Сервис-источник">
              <button class="onb-src" type="button" data-src="lastfm"><span class="onb-src-name">Last.fm</span><span class="onb-src-hint">scrobble-история</span></button>
              <button class="onb-src" type="button" data-src="yandex"><span class="onb-src-name">Яндекс Музыка</span><span class="onb-src-hint">история прослушиваний</span></button>
              <button class="onb-src" type="button" data-src="vk"><span class="onb-src-name">ВК Музыка</span><span class="onb-src-hint">твои аудиозаписи</span></button>
            </div>
            <div class="onb-model-actions"><button class="onb-model-ghost" id="onb-import-back" type="button">Назад к пузырям</button></div>
          </div>

          <!-- STEP: import parsing theatre (~3s «нашли вкус») -->
          <div class="onb-model-step" id="onb-import-parse" hidden>
            <span class="onb-model-spark onb-model-spark--spin" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l1.9 5.8L20 9.7l-5.1 3.4L16 19l-4-3.3L8 19l1.1-5.9L4 9.7l6.1-1.9z"/></svg>
            </span>
            <h2 class="onb-model-title">Читаю историю <span id="onb-import-svc">Last.fm</span>…</h2>
            <ul class="onb-model-log" id="onb-import-log" aria-live="polite"></ul>
          </div>

          <!-- STEP: the model (shared destination of bubbles / resume / import) -->
          <div class="onb-model-step" id="onb-model-main" hidden>
            <span class="onb-model-kicker" id="onb-model-kicker">Вот как я тебя понял</span>
            <h2 class="onb-model-title" id="onb-model-title">Твоя модель за <b id="onb-model-n">7</b> сигналов</h2>
            <p class="onb-model-sub" id="onb-model-prov">Собрал из выбранных тобой сигналов — каждый пункт объяснён. Поправь прямо тут.</p>

            <ul class="onb-model-vec" id="onb-model-vec" aria-label="Стартовый вектор вкуса — можно поправить"></ul>

            <p class="onb-model-receipt" id="onb-model-receipt" role="status" aria-live="polite"></p>

            <div class="onb-model-actions">
              <button class="onb-model-ghost" id="onb-model-deeper" type="button">Открыть полный профиль</button>
              <button class="onb-model-go" id="onb-model-go" type="button">
                Собрать радио
                <svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="9 6 15 12 9 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </button>
            </div>
          </div>

        </div>
      </div>
      <!-- /onb-model -->
```

**Структура строки вектора** (рендерится JS в `#onb-model-vec`, мирроринг `.taste-row` визуально, но с inline +/− и причиной под именем):
```html
<li class="onb-vec-row" data-name="Рок">
  <div class="onb-vec-main">
    <span class="onb-vec-name">Рок</span>
    <div class="onb-vec-bar"><div class="onb-vec-fill" style="width:78%"></div></div>
    <span class="onb-vec-pct">78%</span>
    <div class="onb-vec-ctrl">
      <button class="onb-vec-btn" type="button" data-act="down" aria-label="Меньше: Рок">–</button>
      <button class="onb-vec-btn" type="button" data-act="up" aria-label="Больше: Рок">+</button>
      <button class="onb-vec-btn onb-vec-btn--x" type="button" data-act="remove" aria-label="Убрать: Рок">✕</button>
    </div>
  </div>
  <span class="onb-vec-why">выбрал Linkin Park и РОК → рок в центре вектора</span>
</li>
```
(✕ — текстовый символ U+2715 в кнопке с `aria-label`, НЕ эмодзи-иконка; см. Holy-Grail.)

**a11y-гарантии:**
- `role="dialog" aria-modal="true" aria-labelledby="onb-model-title"`; focus при показе → `#onb-model-go`; Esc → не закрывает в никуда (онбординг обязателен) — Esc на import-шаге возвращает к пузырям, на model-шаге игнорируется (нет «отмены онбординга»).
- Каждая +/−/✕ — отдельный `<button>` с конкретным `aria-label` (имя грани).
- `#onb-model-receipt role="status" aria-live="polite"` → правка озвучивается («Рок 78 → 82 % — пересчитал»).
- Причина (`.onb-vec-why`) — видимый текст под строкой = текстовая AT-репрезентация (§10 a11y north-star: «видишь логику» работает и для screen-reader).
- Демо-маркер import = видимый текст, не color-only.
- Цели ≥44px (CSS §5).

---

## 4. JS — правки внутри `GorodOnboarding` IIFE (аддитивно)

### 4.1 Перехват `onContinue` (заменить тело @12712–12720)
**Было** (12712–12720): `onContinue` сразу `location.hash='#/home'` + greet.
**Стало:**
```js
    function onContinue() {           // bubbles door → show model first (no longer jumps home)
      if (cta && cta.disabled) return;
      saveTaste();
      Model.show('bubbles');
    }
    function goHome() {               // model «Собрать радио» → the real handoff (was inside onContinue)
      saveTaste();
      try { localStorage.setItem('gorodfm_onboarded', '1'); } catch (e) {}   // C7 — durable cold-start flag (W0)
      window.location.hash = '#/home';
      if (window.TwinrChat && window.TwinrChat.greetFromOnboarding) {
        setTimeout(function () { window.TwinrChat.greetFromOnboarding(selectedNames()); }, 450);
      }
    }
```
resume-build (@12696) уже вызывает `onContinue()` → теперь корректно ведёт на экран модели (источник «resume» определит сам Model по факту наличия `rDerived`). Чтобы пометить источник явно: заменить `build.addEventListener('click', function () { applyDerived(); closeResume(); onContinue(); });` (12696) на `… applyDerived(); closeResume(); saveTaste(); Model.show('resume'); });`.

### 4.2 Подключить кнопку import (в `build()`, рядом с @12433)
После `if (alt) alt.addEventListener('click', onResumeDemo);` (12433) добавить:
```js
      var imp = document.getElementById('onb-import');
      if (imp) imp.addEventListener('click', function () { Import.open(); });
```

### 4.3 Новый под-модуль `Model` (вставить перед `function start()` @12722)
Детерминированный, null-guarded, `esc`-санитайз динамики, причины — module-constant literals.
```js
    /* ---- GOROD-ONB: экран «модель за N сигналов» (видимый редакт. вектор) ---- */
    var Model = (function () {
      var M = {}, wired = false, vec = [], source = 'bubbles';
      var GENRE_LC = { 'ПОП':'поп','РОК':'рок','ХИП-ХОП':'хип-хоп','ДИСКО':'диско','ЭЛЕКТРО':'электронику',
        'ЛОФАЙ':'лофай','ИНДИ':'инди','ДЖАЗ':'джаз','РЭП':'рэп','R&B':'r&b','МЕТАЛЛ':'тяжёлое','КЛАССИКА':'классику' };
      var MOOD = [
        { any:['РОК','МЕТАЛЛ','Linkin Park'], name:'Энергичное', why:'рок и тяжёлое в выборе → энергичный профиль' },
        { any:['ХИП-ХОП','ЭЛЕКТРО','ДИСКО','РЭП'], name:'Драйв', why:'хип-хоп и электро в выборе → ритм и драйв' },
        { any:['ЛОФАЙ','ДЖАЗ','КЛАССИКА','ИНДИ'], name:'Спокойное', why:'инди и лофай в выборе → спокойный профиль' }
      ];
      function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
      function weightFor(i){ return Math.max(58, 88 - i * 4); }
      function lc(g){ return GENRE_LC[g] || (g ? g.toLowerCase() : ''); }
      function isGenre(name){ return name === String(name).toUpperCase() && /[А-ЯA-Z]/.test(name); }

      // Build vec from current selected bubbles (deterministic, by selection order)
      function fromBubbles(){
        var picked = bubbles.filter(function(b){ return b.sel; });
        var rows = [], seen = {}, i = 0;
        picked.forEach(function(b){
          var nm = b.d.t;
          if (isGenre(nm)) {
            if (seen[nm]) return; seen[nm]=1;
            rows.push({ name: cap(nm), weight: weightFor(i++), kind:'genre',
              why: 'выбрал <b>'+esc(nm)+'</b> — поставил '+lc(nm)+' в центр вектора.' });
          } else {
            if (seen[nm]) return; seen[nm]=1;
            var g = b.genre || '';
            rows.push({ name: nm, weight: weightFor(i++), kind:'artist',
              why: 'тапнул <b>'+esc(nm)+'</b>'+(g?' → подтянул '+lc(g)+' и похожих.':'.') });
          }
        });
        // 1 mood derived from genre mix (moods are not bubbles — honest derivation)
        var names = picked.map(function(b){ return b.d.t; });
        for (var m=0;m<MOOD.length;m++){
          if (MOOD[m].any.some(function(x){ return names.indexOf(x)!==-1; })){
            rows.push({ name: MOOD[m].name, weight: 64, kind:'mood', why: MOOD[m].why }); break;
          }
        }
        return rows;
      }
      function cap(s){ s=String(s).toLowerCase(); return s.charAt(0).toUpperCase()+s.slice(1); }

      // Build vec from resume rDerived ({name, why}) — provenance already explained
      function fromDerived(items){
        return (items||[]).map(function(it,i){
          return { name: cap(it.name), weight: weightFor(i), kind:'genre',
            why: esc(it.why) }; });
      }
      // Build vec from import seed (set by Import module)
      function fromImport(items){
        return (items||[]).map(function(it,i){
          return { name: it.disp, weight: weightFor(i), kind: it.kind,
            why: it.why }; });   // why already a trusted literal from Import
      }

      function refs(){
        if (M.root) return;
        M.root=document.getElementById('onb-model'); M.back=document.getElementById('onb-model-backdrop');
        M.main=document.getElementById('onb-model-main'); M.vecEl=document.getElementById('onb-model-vec');
        M.n=document.getElementById('onb-model-n'); M.prov=document.getElementById('onb-model-prov');
        M.kicker=document.getElementById('onb-model-kicker'); M.receipt=document.getElementById('onb-model-receipt');
        M.go=document.getElementById('onb-model-go'); M.deeper=document.getElementById('onb-model-deeper');
      }
      function render(){
        if (!M.vecEl) return;
        if (M.n) M.n.textContent = vec.length;
        M.vecEl.innerHTML = vec.map(function(r){
          return '<li class="onb-vec-row" data-name="'+esc(r.name)+'">'+
            '<div class="onb-vec-main">'+
              '<span class="onb-vec-name">'+esc(r.name)+'</span>'+
              '<div class="onb-vec-bar"><div class="onb-vec-fill" style="width:'+r.weight+'%"></div></div>'+
              '<span class="onb-vec-pct">'+r.weight+'%</span>'+
              '<div class="onb-vec-ctrl">'+
                '<button class="onb-vec-btn" type="button" data-act="down" aria-label="Меньше: '+esc(r.name)+'">–</button>'+
                '<button class="onb-vec-btn" type="button" data-act="up" aria-label="Больше: '+esc(r.name)+'">+</button>'+
                '<button class="onb-vec-btn onb-vec-btn--x" type="button" data-act="remove" aria-label="Убрать: '+esc(r.name)+'">✕</button>'+
              '</div>'+
            '</div>'+
            '<span class="onb-vec-why">'+r.why+'</span>'+   // why = trusted literal (<b>signal</b>), module-built
          '</li>'; }).join('');
      }
      function provText(){
        if (source==='resume') return 'Собрал из твоего резюме — каждый пункт объяснён. Поправь прямо тут.';
        if (source==='import') return 'Вытащил из истории '+esc(Import.svcLabel())+' — каждый пункт объяснён. Поправь прямо тут.';
        return 'Собрал из '+vec.length+' выбранных тобой сигналов — каждый пункт объяснён. Поправь прямо тут.';
      }
      function announce(t){ if (M.receipt) M.receipt.textContent=t; }
      function wire(){
        if (wired) return; refs(); if (!M.root) return;
        M.vecEl.addEventListener('click', function(e){
          var btn=e.target.closest('.onb-vec-btn'); if(!btn) return;
          var li=btn.closest('.onb-vec-row'); var nm=li&&li.getAttribute('data-name');
          var i=vec.map(function(r){return r.name;}).indexOf(nm); if(i<0) return;
          var act=btn.getAttribute('data-act'), r=vec[i];
          if(act==='up'){ var ow=r.weight; r.weight=Math.min(100,r.weight+6); render(); announce(esc(r.name)+' '+ow+' → '+r.weight+' % — пересчитал.'); }
          else if(act==='down'){ var ow2=r.weight; r.weight=Math.max(4,r.weight-6); render(); announce(esc(r.name)+' '+ow2+' → '+r.weight+' % — пересчитал.'); }
          else if(act==='remove'){ vec.splice(i,1); render(); announce('Убрал '+esc(nm)+' — больше не в стартовом векторе.'); }
          syncTaste();
        });
        if (M.go) M.go.addEventListener('click', function(){ syncTaste(); hide(); goHome(); });
        if (M.deeper) M.deeper.addEventListener('click', function(){ syncTaste();
          try{ localStorage.setItem('gorodfm_onboarded','1'); }catch(e){}
          hide(); window.location.hash='#/taste'; });
        // Esc on the model step does NOT cancel onboarding (mandatory); only import steps escape (handled by Import)
        wired=true;
      }
      // write the edited vector back to gorodfm_taste as a name-array (same format GorodTaste reads)
      function syncTaste(){
        try { localStorage.setItem('gorodfm_taste',
          JSON.stringify(vec.map(function(r){ return r.kind==='genre' ? r.name.toUpperCase() : r.name; }).slice(0,8))); } catch(e){}
      }
      function show(src){
        refs(); wire(); if(!M.root) return;
        source = src || 'bubbles';
        vec = (src==='resume') ? fromDerived(rDerived && rDerived.items) :
              (src==='import') ? fromImport(Import.seed()) : fromBubbles();
        if (!vec.length) vec = fromDerived(RESUME_FALLBACK.map(function(f){return {name:f.name,why:f.why};}));
        if (window.GorodOnboarding) stop();      // freeze bubble physics behind overlay
        Import.hideSteps();
        if (M.main) M.main.hidden=false;
        if (M.kicker) M.kicker.textContent = (src==='resume'?'Вот что я прочитал':'Вот как я тебя понял');
        if (M.prov) M.prov.innerHTML = provText();
        render(); announce('');
        M.root.classList.add('is-open'); M.root.setAttribute('aria-hidden','false');
        setTimeout(function(){ if(M.go) M.go.focus(); }, 60);
      }
      function hide(){ if(!M.root) return; M.root.classList.remove('is-open'); M.root.setAttribute('aria-hidden','true'); }
      return { show: show, hide: hide, refs: refs };
    })();
```

### 4.4 Новый под-модуль `Import` (вставить после `Model`)
```js
    /* ---- GOROD-ONB: стриминг-import-seed (fake, opt-in, on-device) ---- */
    var Import = (function () {
      var I = {}, wired = false, current = 'lastfm';
      var SRC = {
        lastfm: { label:'Last.fm', seed:[
          { disp:'Инди',  kind:'genre',  why:'прослушал <b>214×</b> в Last.fm — добавил в стартовый вкус.' },
          { disp:'Рок',   kind:'genre',  why:'прослушал <b>180×</b> в Last.fm — добавил в стартовый вкус.' },
          { disp:'Электро',kind:'genre', why:'прослушал <b>96×</b> в Last.fm — добавил в стартовый вкус.' },
          { disp:'Arctic Monkeys', kind:'artist', why:'часто слушал <b>Arctic Monkeys</b> в Last.fm.' },
          { disp:'Tame Impala',    kind:'artist', why:'часто слушал <b>Tame Impala</b> в Last.fm.' } ] },
        yandex: { label:'Яндекс Музыка', seed:[
          { disp:'Поп',     kind:'genre',  why:'много в истории <b>Яндекс Музыки</b> — добавил в вкус.' },
          { disp:'Хип-хоп', kind:'genre',  why:'значимая доля в <b>Яндекс Музыке</b> — добавил.' },
          { disp:'Электро', kind:'genre',  why:'средне в истории <b>Яндекс Музыки</b>.' },
          { disp:'Егор Крид', kind:'artist', why:'часто слушал <b>Егора Крида</b> в Яндекс Музыке.' },
          { disp:'Macan',     kind:'artist', why:'часто слушал <b>Macan</b> в Яндекс Музыке.' } ] },
        vk: { label:'ВК Музыка', seed:[
          { disp:'Хип-хоп', kind:'genre', why:'основа аудиозаписей <b>ВК</b> — добавил в вкус.' },
          { disp:'Рэп',     kind:'genre', why:'много рэпа в <b>ВК Музыке</b> — добавил.' },
          { disp:'Поп',     kind:'genre', why:'заметная доля в <b>ВК</b>.' },
          { disp:'Макс Корж',  kind:'artist', why:'часто слушал <b>Макса Коржа</b> в ВК.' },
          { disp:'Скриптонит', kind:'artist', why:'часто слушал <b>Скриптонита</b> в ВК.' } ] }
      };
      function refs(){
        if (I.root) return;
        I.root=document.getElementById('onb-model');
        I.pick=document.getElementById('onb-import-pick'); I.parse=document.getElementById('onb-import-parse');
        I.log=document.getElementById('onb-import-log'); I.svc=document.getElementById('onb-import-svc');
        I.back=document.getElementById('onb-import-back'); I.backdrop=document.getElementById('onb-model-backdrop');
      }
      function hideSteps(){ [I.pick,I.parse].forEach(function(el){ if(el) el.hidden=true; }); var m=document.getElementById('onb-model-main'); if(m) m.hidden=true; }
      function open(){
        refs(); wire(); if(!I.root) return;
        if (window.GorodOnboarding) stop();
        hideSteps(); if(I.pick) I.pick.hidden=false;
        I.root.classList.add('is-open'); I.root.setAttribute('aria-hidden','false');
        setTimeout(function(){ var b=I.pick&&I.pick.querySelector('.onb-src'); if(b) b.focus(); }, 60);
      }
      function close(){ if(I.root){ I.root.classList.remove('is-open'); I.root.setAttribute('aria-hidden','true'); } }
      function run(src){
        current = SRC[src] ? src : 'lastfm';
        if (I.svc) I.svc.textContent = SRC[current].label;
        hideSteps(); if(I.parse) I.parse.hidden=false; if(I.log) I.log.innerHTML='';
        var lines=['Подключаюсь к '+SRC[current].label+'…','Читаю историю прослушиваний…','Нахожу повторы и фаворитов…','Собираю стартовый вкус…'];
        if (REDUCE){ Model.show('import'); return; }
        var i=0;(function n(){ if(i>=lines.length){ setTimeout(function(){ Model.show('import'); },300); return; }
          var li=document.createElement('li'); li.textContent=lines[i];
          if(I.log){ if(I.log.lastChild) I.log.lastChild.classList.add('is-done'); I.log.appendChild(li); }
          i++; setTimeout(n,520); })();
      }
      function wire(){
        if (wired) return; refs(); if(!I.root) return;
        if (I.pick) I.pick.addEventListener('click', function(e){ var b=e.target.closest('.onb-src'); if(b) run(b.getAttribute('data-src')); });
        if (I.back) I.back.addEventListener('click', function(){ close(); if (window.GorodOnboarding) start(); });
        document.addEventListener('keydown', function(e){
          if(e.key==='Escape' && I.root && I.root.classList.contains('is-open') && I.pick && !I.pick.hidden){ close(); if(window.GorodOnboarding) start(); }
        });
        wired=true;
      }
      return { open:open, hideSteps:hideSteps, seed:function(){ return SRC[current].seed; }, svcLabel:function(){ return SRC[current].label; } };
    })();
```
(`stop`/`start`/`bubbles`/`rDerived`/`RESUME_FALLBACK`/`byName`/`saveTaste`/`selectedNames` — все уже в scope IIFE; `Model`/`Import` cross-reference друг друга — оба определены до `start()`/первого использования.)

---

## 5. CSS — tokens only (вставить после строки 2453)

Никаких новых hardcode-цветов сверх уже-повсеместных `rgba(255,255,255,…)` / `rgba(81,104,252,…)` (RGB `--brand-blue-light`) — как в файле (напр. @2098, @2371).

```css
      /* =====================================================================
         GOROD-ONB — экран «модель за N сигналов» + стриминг-import overlay.
         Аддитивно поверх онбординга. Onest only, один акцент, art-tint логика.
         ===================================================================== */
      .onb-model {
        position: fixed; inset: 0; z-index: 260;   /* above resume-modal (z-250) */
        display: flex; align-items: center; justify-content: center; padding: 24px;
        opacity: 0; pointer-events: none; transition: opacity 0.22s ease;
      }
      .onb-model.is-open { opacity: 1; pointer-events: auto; }
      .onb-model-backdrop {
        position: absolute; inset: 0; background: rgba(6, 7, 10, 0.72);
        backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
      }
      .onb-model-panel {
        position: relative; width: 560px; max-width: 100%;
        max-height: calc(100vh - 48px); overflow-y: auto;
        background: rgba(18, 18, 24, 0.97);
        backdrop-filter: blur(26px) saturate(1.2); -webkit-backdrop-filter: blur(26px) saturate(1.2);
        border: 1px solid rgba(255, 255, 255, 0.10); border-radius: 22px;
        box-shadow: 0 28px 80px rgba(0, 0, 0, 0.62);
        padding: 28px 28px 22px;
        transform: translateY(14px) scale(0.98);
        transition: transform 0.24s cubic-bezier(.34, 1.4, .64, 1);
      }
      .onb-model.is-open .onb-model-panel { transform: none; }

      .onb-model-kicker {
        display: inline-block; font-family: 'Onest', sans-serif; font-size: 12px; font-weight: 700;
        letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent-on-dark); margin-bottom: 8px;
      }
      .onb-model-title { font-family: 'Onest', sans-serif; font-weight: 800; font-size: 24px; line-height: 1.18; color: #fff; margin: 0 0 8px; }
      .onb-model-title b { color: var(--brand-blue-light); font-weight: 800; }
      .onb-model-sub { font-family: 'Onest', sans-serif; font-size: 14px; line-height: 1.5; color: var(--text-sec); margin: 0 0 18px; }

      .onb-model-spark {
        display: inline-flex; align-items: center; justify-content: center;
        width: 42px; height: 42px; border-radius: 12px; margin-bottom: 14px;
        background: var(--tint-blue-light-20); color: var(--brand-blue-light);
      }
      .onb-model-spark svg { width: 22px; height: 22px; }
      .onb-model-spark--spin svg { animation: resume-spin 1.4s linear infinite; }   /* reuse existing keyframe */

      /* the editable mini-vector */
      .onb-model-vec { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 12px; }
      .onb-vec-row {
        padding: 12px 14px; border-radius: 13px;
        background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
      }
      .onb-vec-main { display: flex; align-items: center; gap: 12px; }
      .onb-vec-name { font-family: 'Onest', sans-serif; font-size: 15px; font-weight: 700; color: #fff; flex: none; min-width: 116px; }
      .onb-vec-bar { flex: 1; height: 8px; border-radius: 4px; background: rgba(255, 255, 255, 0.10); overflow: hidden; }
      .onb-vec-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, var(--brand-blue-light), var(--accent-on-dark)); transition: width 0.32s cubic-bezier(.34,1.4,.64,1); }
      .onb-vec-pct { font-family: 'Onest', sans-serif; font-size: 13px; font-weight: 700; color: var(--accent-on-dark); flex: none; min-width: 38px; text-align: right; }
      .onb-vec-ctrl { display: flex; gap: 6px; flex: none; }
      .onb-vec-btn {
        width: 44px; height: 44px; border-radius: 10px; cursor: pointer;
        background: rgba(255, 255, 255, 0.06); color: #fff; border: 1px solid rgba(255, 255, 255, 0.12);
        font-family: 'Onest', sans-serif; font-size: 18px; font-weight: 700; line-height: 1;
        display: flex; align-items: center; justify-content: center;
        transition: background var(--t-fast), border-color var(--t-fast);
      }
      .onb-vec-btn:hover { background: var(--tint-blue-light-20); border-color: var(--brand-blue-light); }
      .onb-vec-btn:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }
      .onb-vec-btn--x { color: var(--text-sec); font-size: 15px; }
      .onb-vec-btn--x:hover { color: #fff; }
      .onb-vec-why {
        display: block; margin-top: 8px;
        font-family: 'Onest', sans-serif; font-size: 13px; line-height: 1.45; color: var(--text-sec);
      }
      .onb-vec-why b { color: var(--accent-on-dark); font-weight: 700; }

      .onb-model-receipt {
        font-family: 'Onest', sans-serif; font-size: 13px; font-weight: 600; color: var(--accent-on-dark);
        min-height: 18px; margin: 14px 0 0;
      }

      .onb-model-actions { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 20px; }
      .onb-model-ghost {
        background: none; border: none; color: var(--text-sec);
        font-family: 'Onest', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; padding: 12px 8px; border-radius: 6px;
      }
      .onb-model-ghost:hover { color: #fff; }
      .onb-model-ghost:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }
      .onb-model-go {
        display: inline-flex; align-items: center; gap: 7px; height: 52px; padding: 0 26px;
        border: none; border-radius: var(--r-pill); background: var(--brand-blue-light); color: #fff;
        font-family: 'Onest', sans-serif; font-size: 16px; font-weight: 700; cursor: pointer;
        box-shadow: 0 10px 30px rgba(81, 104, 252, 0.4);
        transition: transform var(--t-fast), box-shadow var(--t-fast);
      }
      .onb-model-go:hover { transform: translateY(-2px); box-shadow: 0 14px 38px rgba(81, 104, 252, 0.5); }
      .onb-model-go:active { transform: translateY(0) scale(0.98); }
      .onb-model-go:focus-visible { outline: 3px solid #fff; outline-offset: 3px; }
      .onb-model-go svg { width: 18px; height: 18px; }

      /* import source picker */
      .onb-src-row { display: flex; flex-direction: column; gap: 10px; }
      .onb-src {
        display: flex; flex-direction: column; align-items: flex-start; gap: 2px;
        min-height: 56px; padding: 11px 16px; cursor: pointer; text-align: left;
        background: rgba(255, 255, 255, 0.04); color: #fff;
        border: 1px solid rgba(255, 255, 255, 0.10); border-radius: var(--r-base);
        font-family: 'Onest', sans-serif;
        transition: background var(--t-fast), border-color var(--t-fast), transform var(--t-fast);
      }
      .onb-src:hover { background: var(--tint-blue-light-20); border-color: var(--brand-blue-light); transform: translateY(-1px); }
      .onb-src:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 3px; }
      .onb-src-name { font-size: 15px; font-weight: 700; }
      .onb-src-hint { font-size: 12px; font-weight: 600; color: var(--text-quat); }

      /* import parsing log — reuse resume-log visual language */
      .onb-model-log { list-style: none; margin: 6px 0 0; padding: 0; display: flex; flex-direction: column; gap: 11px; }
      .onb-model-log li {
        font-family: 'Onest', sans-serif; font-size: 14px; color: var(--text-sec);
        display: flex; align-items: center; gap: 10px;
        opacity: 0; transform: translateY(6px); animation: resume-in 0.3s ease forwards;   /* reuse */
      }
      .onb-model-log li::before { content: ''; width: 7px; height: 7px; border-radius: 50%; background: var(--brand-blue-light); flex: none; }
      .onb-model-log li.is-done { color: #fff; }

      /* import entry link in footer — same family as .onb-alt */
      .onb-alt--import { color: var(--accent-on-dark); }
      .onb-alt--import:hover { color: #fff; }

      @media (max-width: 760px) {
        .onb-model-panel { padding: 22px 18px 18px; border-radius: 18px; width: 100%; }
        .onb-model-title { font-size: 20px; }
        .onb-vec-main { flex-wrap: wrap; }
        .onb-vec-name { min-width: 0; flex: 1 1 100%; }
        .onb-vec-ctrl { margin-left: auto; }
        .onb-model-actions { flex-direction: column-reverse; align-items: stretch; }
        .onb-model-go { justify-content: center; }
      }
      @media (prefers-reduced-motion: reduce) {
        .onb-model, .onb-model-panel { transition: none; }
        .onb-model-spark--spin svg { animation: none; }
        .onb-model-log li { animation: none; opacity: 1; transform: none; }
        .onb-vec-fill { transition: none; }
        .onb-src:hover, .onb-model-go:hover { transform: none; }
      }
```

**Token inventory (каждая используемая var):**
- `--accent-on-dark` (#8094ff, AA) — kicker, %-вес, why-`<b>`, receipt, import-link, mini-vector fill (gradient end).
- `--brand-blue-light` (#5168FC, единственный акцент) — title-`<b>`, focus-outline, кнопки, fill (gradient start), tint RGB `81,104,252` для теней.
- `--tint-blue-light-20` (rgba(81,104,252,.2)) — spark-bg, hover-состояния.
- `--text-sec` / `--text-quat` — вторичный/третичный текст (sub, why, hints).
- `--r-base` (10px), `--r-pill` (999px), `--t-fast` (180ms) — радиусы, переходы.
- `--success` — НЕ используется.
- Переиспользованы существующие keyframes `resume-spin` (@2358) и `resume-in` (@2420) — никаких новых анимаций.
- Onest на каждом текстовом узле. Белые-шкалы rgba — все уже в файле.

---

## 6. Holy-Grail / anti-slop чеклист

| Gate | Status | Evidence |
|---|---|---|
| **Onest only** | ✅ | Каждый текстовый узел `font-family:'Onest',sans-serif`. Нет Inter/Roboto/system-ui. |
| **near-black bg + 1 акцент** | ✅ | Панель `rgba(18,18,24,.97)` (та же, что resume-modal/ai-dock); единственный акцент `--brand-blue-light` + small-text `--accent-on-dark`. Второй hue не вводится. |
| **`--accent-on-dark` для small accent-текста** | ✅ | kicker / %-вес / why-`<b>` / receipt / import-link — все small accent. |
| **цели ≥44px** | ✅ | `.onb-vec-btn` 44×44; `.onb-model-go` 52px; `.onb-src` 56px; mobile сохраняет высоту. |
| **focus-visible 3px** | ✅ | Все интерактивы: `outline:3px solid var(--brand-blue-light)` (CTA — `#fff` на синем фоне). |
| **prefers-reduced-motion** | ✅ | Спин/лог/fill/hover-translate отключены; import-парс и model-show мгновенны под REDUCE (как resume @12636). |
| **поведенческая копи, не маркетинг** | ✅ | Каждая why = реальный сигнал («выбрал РОК», «прослушал 214× в Last.fm»). `«специально для тебя»` ОТСУТСТВУЕТ (C-уровень бриф-анти-паттерн). Число «сигналов», не «треков» (C1 — fidelity). |
| **demo-маркер для мок-данных** | ✅ | Import-pick: «Демо: реальная история не загружается…». Каждый import-vec — fake, помечен источником. (Резюме уже маркировано @9600.) |
| **❌ multi-stop gradient bg** | ✅ | Плоские `rgba(255,255,255,.04)` карточки; fill — 2-стоповый линейный В СИНЕЙ семье (brand→accent-on-dark), не радужный bg. |
| **❌ orb / fake-волна / gradient-placeholder / эмодзи-иконки** | ✅ | Нет аватаров/орбов; вектор = текст+бар (не fake-волна); ✕/–/+ = текстовые символы (`✕`/`–`/`+`) в `<button aria-label>`, НЕ эмодзи; артист-строки — текст (нет fake-обложек). |
| **WCAG AA** | ✅ | `#fff` + `--text-sec`(.70)/`--text-quat`(.60) на тёмной панели; small-accent = `--accent-on-dark` (6.8:1). |
| **AT-репрезентация (§10 north-star)** | ✅ | Причина под каждой строкой = видимый текст; receipt `aria-live="polite"`; +/−/✕ имеют конкретный `aria-label`; mini-vector — `<ul aria-label>`. «Видишь логику» работает для screen-reader. |
| **zero console errors** | ✅ | try/catch на всех LS; null-guard на каждом `getElementById`/`closest`; делегирование кликов; `esc()` на динамике; why — module-constant literals (innerHTML безопасен); zero `Math.random` (детерминированно). |
| **additive single-file** | ✅ | 1 кнопка в footer + 1 overlay-блок + 1 CSS-блок + правки внутри одного IIFE. Нет нового роута; формат `gorodfm_taste` сохранён; пузыри/резюме не тронуты. |
| **fidelity (показанное = реальное)** | ✅ | Vec строится ИЗ реально выбранных сигналов; правка пишется обратно в `gorodfm_taste` → GorodTaste/Profile/Recap видят то же. Источник честно подписан. |

---

## 7. Additive-safety / не-ломает-built доказательство

1. **Пузыри (built):** `DATA`/`REL`/`POOL`/`makeBubble`/`spawnChildren`/`scatter`/`step`/`measure` (12227–12530) — 0 правок. `onContinue` (12712) меняет только destination (модель вместо `#/home`); сам сбор не тронут. `stop()` (12737) переиспользуется для заморозки физики под overlay.
2. **Резюме→музыка (built, VISION#7):** DOM (9586–9649), CSS (2310–2453), `deriveTaste`/`runParse`/`showResult`/`applyDerived`/`wireResume` (12532–12710) — без изменений, кроме **1 строки** (resume-build @12696: `onContinue()` → `Model.show('resume')`), что апгрейд, не регрессия. `RESUME_FALLBACK`/`rDerived` переиспользуются Model как fallback-источник.
3. **GorodTaste (built, W1 fidelity):** `seed()` @13134 читает `gorodfm_taste` как массив строк (`picks`). Model.syncTaste пишет ровно тот же формат (массив имён, genre→UPPERCASE — совпадает с эвристикой @13139 `p===p.toUpperCase()→'Жанры'`). → нулевая регрессия в `#/taste`. `gorodfm_rejected` не трогается.
4. **TwinrChat (built):** `greetFromOnboarding` (@12993) вызывается из `goHome()` тем же `selectedNames()` (порядок и формат сохранены). Контракт цел.
5. **TwinrWave / GorodContext (built, 051):** не затрагиваются — экран модели не использует волну (честно: волны на онбординге нет; вектор показан баром, не fake-волной).
6. **Роутер / VALID_ROUTES (@10931):** не трогается. Overlay'и живут на `#/onboarding` (z-260/parse поверх z-200-секции, как resume z-250). `gorodfm_onboarded` — НОВЫЙ изолированный ключ (Grep подтвердил 0 текущих вхождений), его потребитель — будущий W0 cold-start (этот спек его и создаёт; до W0 он пишется-но-не-читается = безвреден).
7. **Гейт 045 / Figma 2174:422 / `#/home`:** 0 байт. Онбординг — отдельная full-bleed fixed-поверхность (@2055), home не участвует.
8. **Z-index sanity:** resume-modal z-250 и onb-model z-260 не открыты одновременно (resume-build закрывает resume → открывает model). Import переиспользует onb-model overlay (шаги взаимоисключающие через `hidden`).

---

## 8. Implementer's edit manifest (ordered, line-anchored)

1. **CSS** — вставить §5 блок **после строки 2453** (конец resume-modal `@media (max-width:760px)`), перед `/* TWINR AI CHAT */` (2455).
2. **DOM (footer)** — вставить `#onb-import` кнопку (§3.1) **после строки 9580** (`#onb-alt`), перед `</footer>` (9581).
3. **DOM (overlay)** — вставить §3.2 `<div class="onb-model">` **между строкой 9648** (`</div>` закрытия `#resume-modal`) **и 9651** (`<!-- Page: Мой вкус -->`).
4. **JS — onContinue/goHome** — заменить тело `onContinue` (12712–12720) на §4.1 (split на `onContinue` + новый `goHome`).
5. **JS — resume-build** — в `wireResume` заменить строку 12696 (`build.addEventListener… onContinue();`) на `… saveTaste(); Model.show('resume');`.
6. **JS — import button wire** — в `build()` после строки 12433 добавить §4.2 (привязка `#onb-import` → `Import.open()`).
7. **JS — Model module** — вставить §4.3 `var Model = (function(){…})();` **перед `function start()`** (12722).
8. **JS — Import module** — вставить §4.4 `var Import = (function(){…})();` **после `Model`** (перед `start()`).

Все anchor-пары (2453/2455, 9580/9581, 9648/9651, 12712–12720, 12696, 12433, 12722) пересверены против текущего файла в этой сессии. `gorodfm_onboarded` подтверждён как НЕ существующий (Grep) → вводится этим спеком.

---

## Real products grounding (3, с URL)
- **TikTok cold-start** — interest-selection при первом запуске + первая сессия комбинирует выбор с реальными взаимодействиями для быстрой тренировки feed; повторно поощряет скролл для hook. Урок для нас: **держать в первой сессии до момента "видимой управляемости"** (экран модели = наш aha), не выбрасывать на `#/taste`. https://goodux.appcues.com/blog/tiktok-user-onboarding · https://support.tiktok.com/en/using-tiktok/exploring-videos/how-tiktok-recommends-content
- **Spotify onboarding (cyclic artist-selection + Taste Profiles 2025 с "exclude songs")** — циклический выбор музыки/артистов + апгрейд Taste Profile опцией исключать треки, чтобы one-off не портил рекомендации. Урок: **наш "✕ убрать" на экране модели = тот же контроль, но ВИДИМЫЙ и СРАЗУ** (Spotify прячет; мы показываем = wedge). https://medium.com/@smarthvasdev/deep-dive-into-spotifys-user-onboarding-experience-f2eefb8619d6 · https://newsroom.spotify.com/2025-12-29/year-in-features/
- **Last.fm scrobble-история** — реальный кросс-платформенный артефакт прослушиваний, которым пользуется beachhead-сегмент (меломаны). Урок: import-seed правдоподобен именно через Last.fm/Яндекс/ВК (НЕ Spotify — мёртв на РФ-рынке, блюпринт §6).
