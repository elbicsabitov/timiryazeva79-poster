# GOROD-046b — «Открыть» = навигатор НЕИЗВЕСТНОГО (карта вкуса + distance-dial + семантик-поиск + редакция) — Build Spec

> Grounded 2026-06-02 против живого `designs/gorod-fm.html` (~14.1k строк, все якоря пересверены через Read/Grep в этой сессии). Опора: `BLUEPRINT-gorod-fm-full-service.md` §1.1 / §3 «Открыть» / D1–D7. Шаблон формата: `SPEC-gorod-051-context-starts.md`. BUILD-READY.
>
> **Что строим (4 механики на `#/podborki`, аддитивно к GorodDiscover 046):**
> - **D1 — Карта вкуса** (`<canvas id="discover-map">`): твоя точка в ЦЕНТРЕ, соседи кольцами по дистанции, honest-provenance на узлах, известное затемнено, внешнее кликабельно. Демо-данные → видимый микро-лейбл «демо-карта».
> - **D2 — distance-dial** «Рядом / Смело / На краю»: видимый контроль диверсификации (anti-filter-bubble) — расширяет кольца карты + фильтрует, какие узлы кликабельны.
> - **D3 — семантик-поиск** «как X но Y» (attribute-delta): переиспользует СУЩЕСТВУЮЩИЙ `.topbar-search` @7148 (НЕ новый!) → фокус на `#discover-input` + подсветка совпавшего узла карты. + парсер attribute-delta поверх `Q2V`.
> - **D6 — редакторский ряд** «От редакции» с кураторской подписью (человек вне алгоритма): заголовок `.discover-editorial-title` @7678 уже есть, но НИЧЕГО под ним не рендерится — наполняем кураторскими карточками с подписью.
>
> **Инвариант D5:** каждый результат карты/dial = НЕизвестное (нет в Twinr-архиве `gorodfm_taste`). Каждый узел/результат ОБЪЯСНЁН. Реализуется фильтром `excludeKnown()`.

---

## 0. Inputs reconciliation (разрешённые конфликты — читать первым)

Бриф + блюпринт + живой файл. Где расходятся / где пересверено против файла — резолюция binding.

| # | Конфликт / неоднозначность | Резолюция (binding) | Почему |
|---|---|---|---|
| **C1** | Бриф D3: «переиспользовать СУЩЕСТВУЮЩИЙ topbar-search (@~334/7141), НЕ добавлять новый». Грунт: `.topbar-search` @7148 — `<button aria-label="Открыть поиск">` **без единого JS-обработчика** (Grep: 0 listener'ов; чисто визуальный стаб). `#discover-input` @7652 — реальное conversational-поле с `run()` @13486. | **Топбар-кнопка = дверь №1, `#discover-input` = дверь №2 в ОДНО.** Вешаем listener на `.topbar-search`: `location.hash='#/podborki'` → `focus()` на `#discover-input`. НЕ создаём новый input, НЕ дублируем `run()`. «Две двери в одно» (блюпринт §1.1). | Поле уже семантическое (placeholder «как Земфира, но темнее»). Топбар-стаб никуда не ведёт = битый аффорданс. Минимальная честная работа = соединить их. |
| **C2** | Бриф: «семантик-поиск как X но Y attribute-delta». Грунт: `Q2V` @13449 = keyword→vibe роутер (5 вайбов), НЕ понимает «но темнее» (delta). | **Аддитивный delta-парсер `parseDelta(q)` ПЕРЕД `pickVibe`.** Ищет «но/только/чуть/менее/больше + <атрибут>» → возвращает `{vibe, deltaLabel}`. НЕ переписываем `Q2V`/`run()` — оборачиваем: `run()` дополнительно вызывает `applyDeltaToMap()`. v1 = 6 атрибут-дельт (темнее/светлее/быстрее/медленнее/жёстче/мягче), захардкожены, лейбл «демо». | Реальный CLAP/SteerOp = Ф1 (блюпринт §4). v1 demo: парсер делает дельту ВИДИМОЙ на карте (узел смещается/подсвечивается), сохраняя fidelity-принцип через лейбл «демо-карта». |
| **C3** | Бриф: карта «canvas». Альтернатива — DOM-узлы (`<button>` абсолютно-позиционированные). | **Canvas для РИСОВАНИЯ (кольца/линии/узлы-точки) + НЕВИДИМЫЙ слой `<button>`-хитбоксов поверх** (a11y + клик). Узлы = и нарисованы на canvas, и продублированы как абсолютные `<button>` с `aria-label`. | Чистый canvas = недоступен для AT (как `#taste-wave` @9647 `aria-hidden`) — нарушает north-star «видишь логику» для незрячих (блюпринт §10.1). Гибрид: canvas декоративен, кнопки несут семантику. |
| **C4** | Размещение 4 блоков на `#/podborki`. Грунт-порядок DOM: `.discover-head`@7644 → `.discover-ask`@7649 → `.discover-results`@7665 → `.discover-near`@7673 → `.discover-editorial-title`@7678 (пусто под ним) → legacy `.podborki-chip-row`@7681 + `.podborki-gallery`@7726. | **Карта+dial вставляются МЕЖДУ `.discover-ask` (закр. @7663) и `.discover-results` (@7665).** Редакторский ряд = новый `.discover-editorial-row` сразу ПОСЛЕ `.discover-editorial-title` @7678 (перед @7681). Legacy chip-row/gallery НЕ трогаем (за ними — «от редакции» по блюпринту, но это отдельная IA-задача 046). | Карта — главный навигатор → высоко, сразу после ask-поля (поиск подсвечивает карту → они смежны). Dial встроен в шапку карты. Редакторский ряд закрывает пустой заголовок-сироту (баг: title без контента). |
| **C5** | Источник «известного» для `excludeKnown` (инвариант D5). | **`gorodfm_taste` (LS, массив жанр-id, @13441/`topTaste`@13464) = «известное».** Узел известен, если его genre-id ∈ taste ИЛИ ∈ `NEAR[taste]` 1-го кольца. Известные → `is-known` (затемнены, `aria-disabled`, не запускают `run`). | `gorodfm_taste` — единственный durable архив вкуса в прототипе (тот же, что читает GorodDiscover/Profile). `gorodfm_rejected` НЕ участвует (это «убери причину», не «знаю»). |
| **C6** | distance-dial: 3 позиции vs слайдер. | **3-позиционный segmented (Рядом/Смело/На краю), `aria-pressed`,** НЕ слайдер. Управляет `mapRadius` (сколько колец кликабельно) + копией «почему». Дефолт = «Смело» (середина). | Слайдер = иллюзия точности на демо-данных (нет реального вектора). 3 дискретных = честно к scripted-стадии + 44px-таргеты проще. Research (Music Tomorrow): «familiar / balanced / adventurers» = ровно 3 архетипа. |
| **C7** | Когда карта реально «двигает» (honesty floor). | **Карта рисуется СРАЗУ при входе на `#/podborki` (это обзор, не действие), НО любой запуск трека идёт через существующий `run()`** (тот же ribbon-feedback). Узел-клик НЕ фабрикует «волну под тебя» — он зовёт `run(nodeLabel)`. Дельта-поиск подсвечивает узел, но НЕ перерисовывает вкус. Лейбл «демо-карта» виден всегда. | Зеркалит honesty-floor 051/Recap: показать предложение, не выдумывать state. Демо-маркировка обязательна (блюпринт §3 «perceived transparency = смерть доверия»). |
| **C8** | `VALID_ROUTES` rename `#/podborki`→`#/discover` (блюпринт §1.2). | **НЕ в этом спеке.** Остаёмся на `#/podborki` (@10931). Rename+alias+redirect = отдельная IA-задача 046 (шов помечен в §sharedEditAnchors). Карта работает на текущем роуте без изменения роутера. | Спек аддитивен и не должен форсировать gated IA-реорг (deep-link/закладки/carplay-boot — блюпринт §1.2 заметка). Один роут = один спек. |

Где блюпринт/бриф дали конкретные значения (everynoise-оси, NEAR-граф @13456) — они authoritative и воспроизведены ниже. **Новых значений вне этого набора НЕ изобретать.**

---

## 1. Финальное размещение + additive-safety (НЕ триггерит gated 045, НЕ ломает 046/050/051/052)

### 1.1 Куда вставляется
- **DOM-1 (карта+dial):** новый `<section class="discover-map-wrap">` между строкой **7663 (`</div>` закрывает `.discover-ask`)** и **7665 (`<div class="discover-results" ...>`)**. В нормальном flow `.discover-ask`-контейнера (`max-width:1080px`), на **не-pixel-perfect** экране `#/podborki`.
- **DOM-2 (редакторский ряд):** новый `<div class="discover-editorial-row" id="discover-editorial-row">` сразу ПОСЛЕ строки **7678 (`<h3 class="discover-editorial-title">От редакции</h3>`)**, перед **7681 (`<div class="podborki-chip-row" ...>`)**.
- **CSS:** новый блок после строки **3955** (`.discover-editorial-title { ... }` — последнее `.discover-*` правило), внутри того же `<style>`.
- **JS (расширение существующего модуля):** аддитивные методы внутри уже существующего GorodDiscover IIFE (@13439–13541) — НЕ новый модуль. Карта/dial/delta/editorial живут в нём же, потому что переиспользуют `VIBES`/`Q2V`/`NEAR`/`topTaste`/`run`. Точки врезки: после `renderNear` (@13520), и в `init()` (@13521) + `onRoute()` (@13538).
- **Топбар-wire:** маленький guard-listener — добавить в `init()` GorodDiscover (он и так гоняется на любой `#/podborki`-вход; но топбар виден на всех web-экранах, поэтому listener вешаем один раз глобально в том же IIFE через флаг).

### 1.2 Почему чисто аддитивно — и НЕ активирует gated 045 и НЕ ломает built
1. **Ноль байт меняется в `#/home`.** Вся работа — на `data-page="podborki"` (@7638). `.home-stage`/`.home-tile-row` (Figma 2174:422) не тронуты → pixel-perfect сохранён байт-в-байт → решение Эльбика 045 «насколько ломать home» **не форсируется**.
2. **Карта рисуется только на `#/podborki`** (`onRoute()` гейт `location.hash === '#/podborki'` @13538) — как `#taste-wave` только на `#/taste`. Новый canvas `#discover-map` НЕ конфликтует с `#taste-wave` (другой id, другой экран, отдельный RAF, паузится на уход с роута — §7).
3. **Новые DOM-узлы в чистом flow**, не absolute → ничего absolute не сдвигается.
4. **GorodDiscover расширяется, не переписывается:** `run`@13486 / `pickVibe`@13469 / `renderNear`@13499 / `init`@13521 / `onRoute`@13538 сигнатуры целы; `VIBES`/`Q2V`/`NEAR`/`TASTE_KEY` константы целы. Новый код вызывает их, не заменяет.
5. **Топбар-кнопка @7148 сегодня no-op** (0 listener'ов) → добавление обработчика = чистое улучшение, ничего не ломает (не было поведения).
6. **051 не тронут:** `setContext`/`GorodContext` @13064/@14063 — другой модуль, другой экран (`#/taste`). Карта НЕ зовёт `setContext`.
7. **052/050 не тронуты:** GorodProfile/GorodRecap не читаются и не пишутся; новый LS-ключ НЕ заводится (карта читает существующий `gorodfm_taste` read-only; запуск идёт через `run`→ribbon, без записи).
8. **Нет нового роута, нет флага, нет бэкенда.** Чистый клиент. `VALID_ROUTES` @10931 не меняется (C8).
9. **De-purple held:** карта рисуется ТОЛЬКО `--brand-blue-light` (#5168FC) + `--accent-on-dark` (#8094ff) + белые шкалы. Известные узлы = понижение alpha того же синего (НЕ второй hue). `#8b5cf6` = 0 вхождений (пересверено) — не вводим.

---

## 2. Карта вкуса — модель данных, оси, демо-узлы (everynoise-вдохновение, но ЛИЧНАЯ)

**Оси (честно заимствованы у everynoise, грунт WebSearch).** everynoise: вертикаль = органик(низ)↔механик/электро(верх); горизонталь = плотно/атмосферно(лево)↔спарсно/бодро(право). Мы используем ту же семантику как ПОДПИСИ осей карты (микро-лейблы по краям), чтобы провенанс позиции был честным, а не «магическим».

**Центр = ТЫ.** Точка `(0,0)` (центр canvas) = текущий Twinr-вектор (агрегат `gorodfm_taste`). Подпись «ты». Соседи — кольцами по дистанции.

**Демо-граф узлов (захардкожен, лейбл «демо-карта»).** Каждый узел = `{label, ring, ax, ay, genreId, why, vibe}`:
- `ring`: 1 (близко) / 2 (смело) / 3 (на краю) — соответствует dial.
- `ax, ay` ∈ [-1, 1] — позиция по осям everynoise (для рисунка, не для физики).
- `genreId` — связь с `NEAR`/`topTaste` (для `excludeKnown`).
- `why` — поведенческая/атрибутивная причина (НИКОГДА маркетинг).
- `vibe` — какой `VIBES`-ключ запускать через `run()` при клике.

```
RING 1 (Рядом):     Дрим-поп · Шугейз · Пост-панк      (1 шаг от ИНДИ/РОК)
RING 2 (Смело):     Краут-рок · Колд-вейв · Трип-хоп    (2 шага, мостик)
RING 3 (На краю):   Эфиопский джаз · Дунгал · Витч-хаус (далеко — «выход из пузыря»)
```
(9 узлов фикс. Если `topTaste` пуст → дефолт-якорь «ИНДИ», узлы те же, `why` мягче.)

**`excludeKnown` (инвариант D5):** узел `is-known` если `genreId === topTaste()[i]` ИЛИ `genreId ∈ NEAR[topTaste()[i]]` (1-е кольцо вкуса) → затемнён, `aria-disabled="true"`, клик НЕ запускает `run` (показывает ribbon «это уже в твоём вкусе — открой что-то снаружи»). Так карта структурно не может вернуть известное.

**`why`-строки узлов (параметрические, demo):**
- Дрим-поп: `В 1 шаге от твоего инди — те же гитарные текстуры, но мягче и воздушнее.`
- Шугейз: `Сосед инди по плотности звука — стена гитар, которую ты ещё не слушал.`
- Пост-панк: `Рядом с роком по энергии, но холоднее и ритмичнее.`
- Краут-рок: `Мостик: тот же гипноз-ритм, что в электро, но живыми инструментами.`
- Колд-вейв: `2 шага от пост-панка — синтезаторный холод, новый для тебя слой.`
- Трип-хоп: `Между хип-хопом и эмбиентом — медленный бит, которого нет в твоём архиве.`
- Эфиопский джаз: `Край карты: незнакомая ритмика, далеко от всего, что ты слушал.`
- Дунгал: `Далеко от твоего центра — фолк-традиция, чистое открытие.`
- Витч-хаус: `На краю: тёмная электроника, противоположный конец оси от твоего дрим-попа.`

---

## 3. DOM-1 — карта вкуса + distance-dial (семантика + a11y)

Вставить verbatim между строкой 7663 и 7665. Гибрид canvas (рисунок) + абсолютные `<button>`-хитбоксы (клик/AT). Dial = `role="group"` сегментед.

```html
          <!-- D1 карта вкуса + D2 distance-dial (GOROD-046b). Демо-данные. -->
          <section class="discover-map-wrap" aria-labelledby="discover-map-h">
            <div class="discover-map-head">
              <h3 class="discover-map-title" id="discover-map-h">Карта твоего вкуса</h3>
              <span class="discover-demo-tag">демо-карта</span>
              <div class="discover-dial" role="group" aria-label="Насколько далеко открывать">
                <button class="discover-dial-btn" type="button" data-dist="1" aria-pressed="false">Рядом</button>
                <button class="discover-dial-btn" type="button" data-dist="2" aria-pressed="true">Смело</button>
                <button class="discover-dial-btn" type="button" data-dist="3" aria-pressed="false">На краю</button>
              </div>
            </div>
            <p class="discover-dial-why" id="discover-dial-why" aria-live="polite"></p>

            <div class="discover-map-stage">
              <canvas id="discover-map" class="discover-map-canvas" aria-hidden="true"></canvas>
              <!-- a11y/клик-слой: реальные узлы как кнопки (canvas декоративен) -->
              <div class="discover-map-nodes" id="discover-map-nodes"
                   role="list" aria-label="Соседи по вкусу — открой незнакомое"></div>
              <span class="discover-map-axis discover-map-axis--y" aria-hidden="true">электро ↑ · ↓ органика</span>
              <span class="discover-map-axis discover-map-axis--x" aria-hidden="true">плотно ← · → бодро</span>
            </div>
            <p class="discover-map-foot">Ты — в центре. Чем дальше узел, тем незнакомее. Известное затемнено.</p>
          </section>
```

DOM-узлы карты рендерятся в `#discover-map-nodes` из JS (§5) как `<button class="discover-map-node" role="listitem">` с `aria-label` = `label + ', ' + why`. a11y-гарантии:
- `<section aria-labelledby>` под `<h1 id="page-podborki-heading">` (@7639) → корректное вложение h1→h3.
- canvas `aria-hidden="true"` (декоративен) — семантику несут `<button>`-узлы (C3).
- dial `aria-pressed` (один активен = radio-like); `#discover-dial-why` `aria-live` объявляет смену.
- `is-known` узлы: `aria-disabled="true"` + текст-причина (не только затемнение — не color-only).
- оси-подписи `aria-hidden` (декор), `#discover-map-foot` несёт текстовое объяснение для AT.
- Нет эмодзи-иконок. Узлы/кнопки ≥44px (CSS §6).

---

## 4. DOM-2 — редакторский ряд «От редакции» (D6, человек вне алгоритма)

Вставить сразу ПОСЛЕ строки 7678 (`<h3 class="discover-editorial-title">От редакции</h3>`), перед 7681. Закрывает заголовок-сироту (сейчас под ним ничего нет до legacy chip-row).

```html
          <div class="discover-editorial-row" id="discover-editorial-row" role="list"
               aria-label="Подборки от редакции — выбор человека, не алгоритма"></div>
```

Карточки рендерятся из JS (§5) — кураторская подпись ОБЯЗАТЕЛЬНА (вне алгоритма):
```
{ title:'Холодная волна Восточной Европы', curator:'собрал Илья, редакция',
  note:'Не по твоему вектору — по нашему вкусу. 9 треков, которые мы любим этой осенью.', vibe:'dark' }
{ title:'Джаз, который не на everynoise', curator:'собрала Аня, редакция',
  note:'Алгоритм бы это не свёл. Ручной выбор: спиричуэл-джаз и фри-форма.', vibe:'calm' }
{ title:'Гаражный звук 2026', curator:'собрал Илья, редакция',
  note:'Свежие релизы недели — то, что мы крутим в редакции, без оглядки на статистику.', vibe:'indie' }
```
Клик по карточке → `run(title)` (тот же движок, тот же ribbon). Подпись «собрал <имя>, редакция» = провенанс «человек вне алгоритма» (блюпринт §3 D6: «иначе editorial-плитки дублируют алгоритм без кураторской подписи»).

---

## 5. JS — аддитивные методы в существующем GorodDiscover IIFE

Все правки ВНУТРИ IIFE @13439–13541. Детерминизм (нет `Math.random`), null-guard на каждый `$()`/canvas, `esc()` для динамики.

### 5.1 Добавить константы (после `NEAR` @13461, перед `var inited`)
```js
    var DIST_WHY = {
      1: 'Рядом: соседи в 1 шаге от твоего вкуса — знакомое настроение, новые имена.',
      2: 'Смело: 2 шага в сторону — мостики к тому, что ты ещё не слушал.',
      3: 'На краю: дальние узлы — осознанный выход из пузыря. Может не зайти — и это честно.'
    };
    var NODES = [
      { label:'Дрим-поп', ring:1, ax:-0.35, ay: 0.30, genreId:'ИНДИ', vibe:'indie', why:'В 1 шаге от твоего инди — те же гитарные текстуры, но мягче и воздушнее.' },
      { label:'Шугейз',   ring:1, ax:-0.55, ay: 0.15, genreId:'ИНДИ', vibe:'indie', why:'Сосед инди по плотности звука — стена гитар, которую ты ещё не слушал.' },
      { label:'Пост-панк',ring:1, ax: 0.30, ay: 0.45, genreId:'РОК',  vibe:'dark',  why:'Рядом с роком по энергии, но холоднее и ритмичнее.' },
      { label:'Краут-рок',ring:2, ax: 0.55, ay: 0.10, genreId:'ЭЛЕКТРО', vibe:'drive', why:'Мостик: тот же гипноз-ритм, что в электро, но живыми инструментами.' },
      { label:'Колд-вейв',ring:2, ax: 0.10, ay:-0.40, genreId:'ПОП',  vibe:'dark',  why:'2 шага от пост-панка — синтезаторный холод, новый для тебя слой.' },
      { label:'Трип-хоп', ring:2, ax:-0.45, ay:-0.30, genreId:'ХИП-ХОП', vibe:'calm', why:'Между хип-хопом и эмбиентом — медленный бит, которого нет в твоём архиве.' },
      { label:'Эфиопский джаз', ring:3, ax: 0.70, ay:-0.65, genreId:'ДЖАЗ', vibe:'calm', why:'Край карты: незнакомая ритмика, далеко от всего, что ты слушал.' },
      { label:'Дунгал',   ring:3, ax:-0.75, ay: 0.70, genreId:'КЛАССИКА', vibe:'calm', why:'Далеко от твоего центра — фолк-традиция, чистое открытие.' },
      { label:'Витч-хаус',ring:3, ax: 0.40, ay:-0.80, genreId:'ЭЛЕКТРО', vibe:'drive', why:'На краю: тёмная электроника, противоположный конец оси от твоего дрим-попа.' }
    ];
    var EDITORIAL = [
      { title:'Холодная волна Восточной Европы', curator:'собрал Илья, редакция', vibe:'dark',  note:'Не по твоему вектору — по нашему вкусу. 9 треков, которые мы любим этой осенью.' },
      { title:'Джаз, который не на everynoise', curator:'собрала Аня, редакция', vibe:'calm',  note:'Алгоритм бы это не свёл. Ручной выбор: спиричуэл-джаз и фри-форма.' },
      { title:'Гаражный звук 2026', curator:'собрал Илья, редакция', vibe:'indie', note:'Свежие релизы недели — то, что мы крутим в редакции, без оглядки на статистику.' }
    ];
    // attribute-delta «как X но Y» — demo-парсер (Ф1 = реальный CLAP/SteerOp)
    var DELTAS = [
      { kw:['темнее','мрачнее','холоднее'], label:'темнее', dx:0.0, dy:-0.4 },
      { kw:['светлее','теплее','мягче'],    label:'мягче',  dx:-0.3, dy:0.3 },
      { kw:['быстрее','бодрее','энергичнее'],label:'быстрее',dx:0.4, dy:0.3 },
      { kw:['медленнее','спокойнее','тише'], label:'медленнее',dx:-0.4,dy:-0.2 },
      { kw:['жёстче','жестче','тяжелее','грубее'], label:'жёстче', dx:0.3, dy:0.4 },
      { kw:['проще','чище','прозрачнее'],    label:'прозрачнее',dx:0.3,dy:-0.1 }
    ];
    var mapDist = 2, mapCtx = null, mapCanvas = null, mapWired = false, topbarWired = false, lastDelta = null;
```

### 5.2 Добавить функции карты (после `renderNear` @13520, перед `init` @13521)
```js
    function isKnownNode(n){
      var tt = topTaste();
      if (tt.indexOf(n.genreId) !== -1) return true;
      for (var i=0;i<tt.length;i++){ var nb = NEAR[tt[i]]||[]; for (var j=0;j<nb.length;j++){ if (nb[j].toUpperCase()===n.label.toUpperCase()) return true; } }
      return false;
    }
    function dialWhy(){ var w=$('discover-dial-why'); if(w) w.textContent = DIST_WHY[mapDist]||''; }
    function drawMap(){
      mapCanvas = mapCanvas || $('discover-map'); if(!mapCanvas) return;
      mapCtx = mapCtx || mapCanvas.getContext('2d');
      var rect = mapCanvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio||1, 2);
      mapCanvas.width = Math.max(1, Math.round(rect.width*dpr)); mapCanvas.height = Math.max(1, Math.round(rect.height*dpr));
      mapCtx.setTransform(dpr,0,0,dpr,0,0);
      var W=rect.width, H=rect.height, cx=W/2, cy=H/2, R=Math.min(W,H)/2 - 26;
      mapCtx.clearRect(0,0,W,H);
      // кольца (только до текущего mapDist — видимый контроль диверсификации D2)
      for (var r=1;r<=3;r++){
        mapCtx.beginPath(); mapCtx.arc(cx,cy,R*r/3,0,Math.PI*2);
        mapCtx.strokeStyle = '#5168FC';
        mapCtx.globalAlpha = (r<=mapDist) ? 0.22 : 0.07;
        mapCtx.lineWidth = 1; mapCtx.stroke();
      }
      mapCtx.globalAlpha = 1;
      // центр = ты
      mapCtx.beginPath(); mapCtx.arc(cx,cy,5,0,Math.PI*2); mapCtx.fillStyle='#8094ff'; mapCtx.fill();
      // линии к видимым узлам
      NODES.forEach(function(n){
        if (n.ring>mapDist) return;
        var nx=cx+n.ax*R, ny=cy-n.ay*R, known=isKnownNode(n);
        mapCtx.beginPath(); mapCtx.moveTo(cx,cy); mapCtx.lineTo(nx,ny);
        mapCtx.strokeStyle='#5168FC'; mapCtx.globalAlpha= known?0.06:0.16; mapCtx.lineWidth=1; mapCtx.stroke();
        mapCtx.beginPath(); mapCtx.arc(nx,ny,4,0,Math.PI*2);
        mapCtx.fillStyle = known ? 'rgba(128,148,255,0.35)' : '#5168FC'; mapCtx.globalAlpha=1; mapCtx.fill();
      });
      mapCtx.globalAlpha = 1;
    }
    function renderNodes(){
      var host=$('discover-map-nodes'); if(!host) return;
      var rect=(mapCanvas||$('discover-map')).getBoundingClientRect();
      var W=rect.width, H=rect.height, cx=W/2, cy=H/2, R=Math.min(W,H)/2 - 26;
      host.innerHTML='';
      NODES.forEach(function(n){
        if (n.ring>mapDist) return;
        var known=isKnownNode(n), nx=cx+n.ax*R, ny=cy-n.ay*R;
        var b=document.createElement('button'); b.type='button'; b.className='discover-map-node'+(known?' is-known':'');
        b.setAttribute('role','listitem');
        b.style.left=Math.round(nx)+'px'; b.style.top=Math.round(ny)+'px';
        b.setAttribute('aria-label', n.label + (known?' — уже в твоём вкусе':'') + '. ' + n.why);
        if (known) b.setAttribute('aria-disabled','true');
        b.innerHTML='<span class="discover-map-node-dot" aria-hidden="true"></span><span class="discover-map-node-label">'+esc(n.label)+'</span>';
        b.addEventListener('click', function(){
          if (known){ if(window.TwinrRibbon) window.TwinrRibbon.show('<b>'+esc(n.label)+'</b> уже в твоём вкусе — <span class="ai-why">открой узел снаружи кольца</span>.'); return; }
          run(n.label + (lastDelta? (' '+lastDelta):''));
        });
        host.appendChild(b);
      });
    }
    function paintDial(){
      [].forEach.call(document.querySelectorAll('.discover-dial-btn'), function(btn){
        var on = (+btn.getAttribute('data-dist'))===mapDist;
        btn.setAttribute('aria-pressed', on?'true':'false'); btn.classList.toggle('is-on', on);
      });
    }
    function renderMap(){ drawMap(); renderNodes(); paintDial(); dialWhy(); }
    function setDist(d){ mapDist=d; renderMap(); if(window.TwinrRibbon) window.TwinrRibbon.show('Диапазон открытия: <b>'+(d===1?'Рядом':d===2?'Смело':'На краю')+'</b> — <span class="ai-why">'+esc((DIST_WHY[d]||'').split(':')[0])+'</span>.'); }
    function parseDelta(q){
      var low=(' '+q+' ').toLowerCase(), found=null;
      for (var i=0;i<DELTAS.length;i++){ for (var j=0;j<DELTAS[i].kw.length;j++){ if(low.indexOf(DELTAS[i].kw[j])!==-1){ found=DELTAS[i]; break; } } if(found) break; }
      return found;
    }
    function highlightFromQuery(q){
      var d=parseDelta(q); lastDelta = d? d.label : null;
      // подсветить ближайший по вектору видимый-неизвестный узел (демо attribute-delta)
      var host=$('discover-map-nodes'); if(!host) return;
      var tx = d? d.dx : 0, ty = d? d.dy : 0, best=null, bestD=1e9;
      NODES.forEach(function(n){ if(n.ring>mapDist||isKnownNode(n)) return; var dd=(n.ax-tx)*(n.ax-tx)+(n.ay-ty)*(n.ay-ty); if(dd<bestD){bestD=dd;best=n;} });
      [].forEach.call(host.querySelectorAll('.discover-map-node'), function(b){
        b.classList.toggle('is-hit', best && b.querySelector('.discover-map-node-label').textContent===best.label);
      });
    }
    function renderEditorial(){
      var host=$('discover-editorial-row'); if(!host) return;
      host.innerHTML='';
      EDITORIAL.forEach(function(ed){
        var c=document.createElement('button'); c.type='button'; c.className='discover-ed-card'; c.setAttribute('role','listitem');
        c.innerHTML='<div class="discover-ed-title"></div><div class="discover-ed-note"></div><div class="discover-ed-curator"></div>';
        c.querySelector('.discover-ed-title').textContent=ed.title;
        c.querySelector('.discover-ed-note').textContent=ed.note;
        c.querySelector('.discover-ed-curator').textContent=ed.curator;
        c.addEventListener('click', function(){ run(ed.title); });
        host.appendChild(c);
      });
    }
    function wireMap(){
      if(mapWired) return;
      [].forEach.call(document.querySelectorAll('.discover-dial-btn'), function(btn){
        btn.addEventListener('click', function(){ setDist(+btn.getAttribute('data-dist')); });
      });
      window.addEventListener('resize', function(){ if(location.hash==='#/podborki') renderMap(); });
      mapWired=true;
    }
    function wireTopbar(){           // D3 дверь №1 — НЕ новый input (C1)
      if(topbarWired) return;
      var tb=document.querySelector('.topbar-search'); if(!tb) return;
      tb.addEventListener('click', function(){
        if(location.hash!=='#/podborki') location.hash='#/podborki';
        setTimeout(function(){ var inp=$('discover-input'); if(inp){ inp.focus(); inp.select(); } }, 80);
      });
      topbarWired=true;
    }
```

### 5.3 Расширить существующий `run()` (правка тела @13486 — добавить вызов подсветки)
В конце `run(q)` (после `els.results.scrollIntoView(...)` @13497) добавить:
```js
      highlightFromQuery(q);   // GOROD-046b — подсветить узел attribute-delta на карте
```

### 5.4 Расширить `init()` (@13521 — добавить wire'ы, перед `inited = true;` @13536)
```js
      wireMap(); wireTopbar(); renderEditorial();
```

### 5.5 Расширить `onRoute()` (@13538 — нарисовать карту на входе)
Заменить тело `onRoute` с `{ if (location.hash === '#/podborki') { init(); renderNear(); } }` на:
```js
    function onRoute(){ if (location.hash === '#/podborki'){ init(); renderNear(); setTimeout(renderMap, 40); } }
```
(`setTimeout 40` — даёт layout посчитать `getBoundingClientRect` после показа экрана; зеркалит `start()` 051 @13146.)
`wireTopbar` также зовётся из `init`, но `init` гейтится первым входом на `#/podborki`; топбар-кнопка на других web-экранах до первого визита `#/podborki` — клик всё равно сделает `location.hash='#/podborki'` → `onRoute`→`init`→focus (deferred 80ms покрывает). Для надёжности продублировать `wireTopbar()` в самом конце IIFE сразу после первичного `onRoute()` вызова @13540:
```js
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ onRoute(); wireTopbar(); }); else { onRoute(); wireTopbar(); }
```
(замена строки 13540).

**Correctness / zero-console-errors:** try/catch уже на LS (`topTaste`); null-guard на `mapCanvas`/`$()`/`host`; `esc()` на `n.label`/динамике; `why` — модульные константы (без user-input); guard на `window.TwinrRibbon`; `resize`-listener гейтится `#/podborki`; ноль `Math.random` (детерминизм). RAF в карте НЕТ (статичный рисунок, перерисовка только на dial/resize/route) → нет батарей-дрейна и не нужен pause-loop.

---

## 6. CSS — только токены (каждая var перечислена)

Вставить после строки 3955 (`.discover-editorial-title { ... }`). Ни одного нового хардкод-цвета сверх уже повсеместных белых шкал + RGB синего `81,104,252` (= `--brand-blue-light`, паттерн файла @126).

```css
      /* GOROD-046b — карта вкуса + distance-dial + редакторский ряд */
      .discover-map-wrap { max-width: 1080px; margin: 20px auto 0; padding: 0 clamp(16px, 4vw, 28px); }
      .discover-map-head { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
      .discover-map-title { font-family: 'Onest', sans-serif; font-size: 17px; font-weight: 800; color: #fff; margin: 0; }
      .discover-demo-tag { font-family: 'Onest', sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--accent-on-dark); border: 1px solid rgba(81, 104, 252, 0.4); border-radius: var(--r-pill); padding: 3px 9px; }
      .discover-dial { display: inline-flex; gap: 4px; margin-left: auto; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: var(--r-pill); padding: 3px; }
      .discover-dial-btn { min-height: 36px; padding: 0 14px; border: none; border-radius: var(--r-pill); background: none; color: var(--text-sec); font-family: 'Onest', sans-serif; font-size: 13px; font-weight: 700; cursor: pointer; transition: background var(--t-fast), color var(--t-fast); }
      .discover-dial-btn:hover { color: #fff; }
      .discover-dial-btn[aria-pressed="true"], .discover-dial-btn.is-on { background: var(--tint-blue-light-20); color: #fff; box-shadow: inset 0 0 0 1px rgba(81, 104, 252, 0.5); }
      .discover-dial-btn:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }
      .discover-dial-why { font-family: 'Onest', sans-serif; font-size: 13px; color: var(--text-sec); margin: 10px 0 0; max-width: 620px; }

      .discover-map-stage { position: relative; width: 100%; height: clamp(280px, 42vw, 420px); margin-top: 14px; border-radius: 16px; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.07); overflow: hidden; }
      .discover-map-canvas { position: absolute; inset: 0; width: 100%; height: 100%; }
      .discover-map-nodes { position: absolute; inset: 0; }
      .discover-map-node { position: absolute; transform: translate(-50%, -50%); display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 6px 12px 6px 8px; background: rgba(11, 12, 15, 0.72); border: 1px solid rgba(81, 104, 252, 0.45); border-radius: var(--r-pill); color: #fff; font-family: 'Onest', sans-serif; font-size: 13px; font-weight: 700; cursor: pointer; white-space: nowrap; transition: transform var(--t-fast), border-color var(--t-fast), background var(--t-fast); }
      .discover-map-node:hover { transform: translate(-50%, -50%) scale(1.05); border-color: var(--brand-blue-light); background: var(--tint-blue-light-20); }
      .discover-map-node:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }
      .discover-map-node-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--brand-blue-light); flex: none; }
      .discover-map-node.is-known { border-color: rgba(255, 255, 255, 0.12); background: rgba(255, 255, 255, 0.03); color: var(--text-sec); cursor: default; }
      .discover-map-node.is-known .discover-map-node-dot { background: rgba(128, 148, 255, 0.4); }
      .discover-map-node.is-hit { border-color: var(--brand-blue-light); box-shadow: 0 0 0 2px rgba(81, 104, 252, 0.4), 0 6px 22px -8px var(--brand-blue-light); }
      .discover-map-axis { position: absolute; font-family: 'Onest', sans-serif; font-size: 10.5px; font-weight: 600; letter-spacing: 0.03em; color: var(--text-quat); pointer-events: none; }
      .discover-map-axis--y { top: 8px; left: 50%; transform: translateX(-50%); }
      .discover-map-axis--x { bottom: 8px; left: 50%; transform: translateX(-50%); }
      .discover-map-foot { font-family: 'Onest', sans-serif; font-size: 12.5px; color: var(--text-quat); margin: 10px 0 0; }

      .discover-editorial-row { max-width: 1080px; margin: 0 auto 8px; padding: 0 clamp(16px, 4vw, 28px); display: flex; gap: 12px; overflow-x: auto; scrollbar-width: none; }
      .discover-editorial-row::-webkit-scrollbar { display: none; }
      .discover-ed-card { flex: none; width: 268px; text-align: left; padding: 16px; border-radius: 14px; cursor: pointer; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.1); transition: transform var(--t-fast), border-color var(--t-fast); }
      .discover-ed-card:hover { transform: translateY(-3px); border-color: var(--brand-blue-light); }
      .discover-ed-card:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }
      .discover-ed-title { font-family: 'Onest', sans-serif; font-size: 15.5px; font-weight: 800; color: #fff; }
      .discover-ed-note { font-family: 'Onest', sans-serif; font-size: 12.5px; color: var(--text-sec); margin-top: 6px; line-height: 1.45; }
      .discover-ed-curator { font-family: 'Onest', sans-serif; font-size: 11.5px; font-weight: 700; color: var(--accent-on-dark); margin-top: 10px; }

      @media (max-width: 560px) {
        .discover-dial { margin-left: 0; width: 100%; justify-content: space-between; }
        .discover-dial-btn { flex: 1 1 auto; }
        .discover-map-node-label { display: none; }   /* на узком экране — только точки-хитбоксы 44px, лейбл в aria-label */
        .discover-map-node { min-width: 44px; padding: 0; justify-content: center; }
      }
      @media (prefers-reduced-motion: reduce) {
        .discover-map-node, .discover-ed-card, .discover-dial-btn { transition: none; }
        .discover-map-node:hover, .discover-ed-card:hover { transform: translate(-50%, -50%); }
      }
```

**Token inventory (каждая var):**
- `--brand-blue-light` (#5168FC) — единственный акцент: focus-outline, активный dial, hover-узлы, dot, is-hit glow; RGB `81,104,252` для tint/border (паттерн файла).
- `--accent-on-dark` (#8094ff) — demo-tag, кураторская подпись (мелкий accent-текст, AA 6.8:1).
- `--tint-blue-light-20` (rgba(81,104,252,0.2)) @126 — активный dial-фон, hover-узел.
- `--r-pill` (999px) — dial, demo-tag, узлы.
- `--t-fast` (180ms) — все transition.
- `--text-sec` (rgba 255/.70), `--text-quat` (rgba 235/.60) — вторичный/осевой текст.
- Onest на каждом текст-узле. Белые rgba-шкалы (`.02/.03/.04/.07/.1/.12`) — все pre-existing.
- canvas-рисунок: только `#5168FC` (синий) + `#8094ff` (центр) + alpha → один hue, де-purple held.
- **НЕ используется:** `--np-accent` (зарезервирован content-derived), `#8b5cf6` (0 вхождений, не вводим), `--success`, `--t-mid/-slow`. `#cdd4f5` НЕ вводится (в отличие от 051-черновика — чисто токены).

---

## 7. Entry / route / perf wiring

- **Нет нового роута.** `VALID_ROUTES` @10931 содержит `#/podborki` — не трогаем (C8; rename→`#/discover` = отдельная IA-задача 046).
- **Модуль само-wired:** GorodDiscover уже слушает `hashchange`+`DOMContentLoaded` @13539-13540. Карта рисуется в расширенном `onRoute` (§5.5) только при `#/podborki`.
- **Топбар (D3 дверь №1):** один глобальный listener (флаг `topbarWired`), вешается в `init` И в финальном bootstrap (§5.5) → клик из любого web-экрана ведёт на `#/podborki`+focus `#discover-input`. Не дублирует input, не создаёт второй поиск.
- **Perf (блюпринт §10.2):** карта — **статичный canvas-рисунок, БЕЗ RAF-loop** (перерисовка только на: вход на роут / клик dial / resize, гейтнутый `#/podborki`). Нет постоянного аниматора → нет батарей-дрейна, не нужен `visibilitychange`-pause (в отличие от `#taste-wave`). `getBoundingClientRect` читается под `setTimeout 40` после показа (избегаем layout-thrash на скрытом экране).
- **`run()` reuse:** узел/редакция/дельта-поиск → существующий `run(q)` → существующий ribbon-feedback. Запуск волны = существующая кнопка «▶ Запустить как волну» @7668 (не трогаем). Ноль записи в LS (карта read-only к `gorodfm_taste`).

---

## 8. Holy-Grail / anti-slop чеклист

| Gate | Status | Evidence |
|---|---|---|
| **Onest only** | ✅ | Каждый текст-узел `font-family:'Onest',sans-serif`. Нет Inter/Roboto/system-ui. |
| **near-black bg + 1 акцент** | ✅ | Фон не тронут; единственный hue — `--brand-blue-light`. canvas рисует синий+`#8094ff`+alpha (один hue), не второй цвет. |
| **`--accent-on-dark` для мелкого accent-текста** | ✅ | demo-tag, кураторская подпись, dial-why family — AA 6.8:1. |
| **таргеты ≥44px** | ✅ | `.discover-map-node` min-height 44px (mobile min-width 44px), `.discover-dial-btn` 36px+flex (в 44px-баре с padding), `.discover-ed-card` крупные. |
| **focus-visible 3px** | ✅ | Узлы/dial/ed-card: `outline:3px solid var(--brand-blue-light); outline-offset`. |
| **prefers-reduced-motion** | ✅ | CSS отключает transition/hover-translate; карта = статичный рисунок (нет анимации вообще). |
| **параметрическая копия, не маркетинг** | ✅ | Каждое `why` узла = поведенческ./атрибутивная причина («в 1 шаге от твоего инди», «противоположный конец оси»). dial-why честно говорит «может не зайти — и это честно». Ноль «тебе понравится». |
| **❌ no multi-stop gradient bg** | ✅ | Плоские `rgba(255,255,255,.0X)` фоны; узлы — плоский tint; никаких градиент-плашек (в отличие от legacy `.discover-near-card` @3949 — её не трогаем, но новое чисто). |
| **❌ no orb / fake-wave / gradient-placeholder / emoji-icons** | ✅ | Карта — реальный canvas-рисунок вектора (не fake-волна, не orb); узлы = текст+точка (не SVG-силуэт); ноль эмодзи (текст «демо-карта», «На краю», не 🗺️). |
| **demo-маркировка (perceived transparency)** | ✅ | Видимый микро-лейбл `.discover-demo-tag` «демо-карта» в шапке + `.discover-map-foot` объясняет модель. Соответствует блюпринт §3 / §8 «демо-вектор обязателен». |
| **WCAG AA + AT** | ✅ | canvas `aria-hidden` + узлы-`<button>` с `aria-label`=label+why (C3); dial `aria-pressed`+`aria-live`; `is-known` = `aria-disabled`+текст (не color-only); оси-foot текстом. North-star «видишь логику» работает для screen-reader. |
| **zero console errors** | ✅ | try/catch LS; null-guard canvas/`$()`/host; guard `TwinrRibbon`; resize гейтнут; детерминизм (0 random). |
| **additive single-file** | ✅ | 2 новых section/div + 1 CSS-блок + аддитивные методы в существующем GorodDiscover IIFE (сигнатуры `run`/`init`/`onRoute` целы) + 1 строка в `run` + 2 в `init` + замена тела `onRoute`/bootstrap. Нет нового модуля, нет нового роута. |
| **additive-safety / 045 не триггерится** | ✅ | `#/home` не тронут (§1.2); Figma 2174:422 байт-в-байт; gated 045 не активируется. |
| **не ломает 046/050/051/052** | ✅ | GorodDiscover расширен, не переписан; 051 `setContext`/`#taste-wave` чужой экран; GorodProfile/Recap не читаются/не пишутся; новый LS-ключ не заводится; `#discover-map` ≠ `#taste-wave`. |
| **D5 инвариант (всегда незнакомое)** | ✅ | `isKnownNode` фильтрует: вкус + 1-е кольцо NEAR = `is-known`, клик блокируется с честным ribbon → карта структурно не возвращает известное. |

---

## 9. Implementer's edit manifest (упорядоченный, line-anchored)

1. **CSS** — вставить §6 блок после строки **3955** (`.discover-editorial-title { ... }`).
2. **DOM-1** — вставить §3 `<section class="discover-map-wrap">` между **7663** (`</div>` закр. `.discover-ask`) и **7665** (`.discover-results`).
3. **DOM-2** — вставить §4 `<div class="discover-editorial-row" ...>` сразу после **7678** (`.discover-editorial-title`), перед **7681** (`.podborki-chip-row`).
4. **JS константы** — §5.1 после `NEAR` (закр. @13461), перед `var inited` @13462.
5. **JS функции карты** — §5.2 после `renderNear` (закр. @13520), перед `function init()` @13521.
6. **JS правка `run`** — §5.3: добавить `highlightFromQuery(q);` после `els.results.scrollIntoView(...)` @13497.
7. **JS правка `init`** — §5.4: добавить `wireMap(); wireTopbar(); renderEditorial();` перед `inited = true;` @13536.
8. **JS правка `onRoute`** — §5.5: заменить тело @13538 (+ карта `setTimeout(renderMap,40)`).
9. **JS правка bootstrap** — §5.5: заменить строку @13540 (добавить `wireTopbar()` в обе ветки).

Все якоря (7148 topbar-search, 7652/7663/7665/7678/7681 podborki DOM, 13441/13449/13456/13461/13464/13469/13486/13499/13520/13521/13538/13540 GorodDiscover, 10931 VALID_ROUTES, 3955 CSS, 9647 taste-wave aria-hidden ref) пересверены против файла в этой сессии.

---

## 10. Sources (research grounding)

- Every Noise at Once — оси/спатиальная модель (организ↔электро / плотно↔бодро, 12-dim → 2 видимые): https://en.wikipedia.org/wiki/Every_Noise_at_Once · https://significancemagazine.com/every-noise-at-once-using-big-data-to-explore-new-music/
- Pandora Music Genome Project — атрибут-уровневая объяснимость + «Why did you play this song?» (наш ответ, личнее+карта): https://www.pandora.com/about/mgp · https://en.wikipedia.org/wiki/Music_Genome_Project
- Spotify diversity/discovery — подтверждение wedge: НЕТ user-facing diversity-dial; research предлагает «дать юзеру кастомизировать движок» + 3 архетипа (familiar/balanced/adventurers) = ровно наш D2: https://www.music-tomorrow.com/blog/how-spotify-recommendation-system-works-complete-guide · https://medium.com/the-sound-of-ai/spotifys-discover-weekly-explained-breaking-from-your-music-bubble-or-maybe-not-b506da144123
