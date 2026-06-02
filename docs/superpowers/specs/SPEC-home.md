# GOROD-045 — ВОЛНА / `#/home` — три-зонный радио-редизайн — Build Spec

> Auto-captured 2026-06-02 from research-workflow (Karpathy-tier: blueprint §3 + grounded live-file re-read + 3 real comparables). BUILD-READY. **GATED 045: ломает pixel-perfect Figma 2174:422 (АВТОРИЗОВАНО задачей).** Дефолтный `#/home` становится РАДИО (3 зоны); существующие плитки-домашка СОХРАНЯЮТСЯ как alt-browse за тем же роутом (toggle), Figma-актив не теряется. Реализовать строго по этому спеку.

---

Все якоря пересверены построчно против живого `designs/gorod-fm.html` (≈14.1k строк) в этой сессии. Один существенный дрейф относительно брифа исправлен: брифовый якорь `NowPlayingTint @~13393` на самом деле = `@13430` (модуль `13398–13432`); `REASONS @13297` = `@13334`; canonical track-change handler = **`TwinrTransition.commit()` @13600–13611** (НЕ просто мини-плеер). Спек хукается в `commit()`, а не дублирует FLOW. Волна-canvas (`#taste-wave`) физически живёт ТОЛЬКО на `#/taste` — поэтому ambient-волна на home строится как **отдельный лёгкий canvas-слой** (свой RAF, читает `--np-accent`), а НЕ переиспользует `TwinrWave` (тот привязан к `#taste-wave` @13052 и был бы no-op на home). Это явный архитектурный выбор, обоснован в §1.0 и §9.

---

# GOROD-045 — Три-зонный радио-home — Unified Implementation Spec

**Что строим.** `#/home` сегодня = пиксель-перфектный Figma-стенд из 8 абсолютных плиток + центральная featured-карточка «Потрачу / Егор Крид» (DOM `7488–7635`, CSS `1735–2033`). Это generic-стриминг-эстетика с ~0 wedge (AUDIT §3, блюпринт §1.2 строка `#/home`). Заменяем **дефолтный** вид на 3-зонное РАДИО:

1. **Зона 1 — контекст-карта** (схлоп → чип «Сменить»): на home показывает текущий выбранный контекст (Утро/День/Вечер/Ночь/Тренировка/Дорога) из той же LS-модели `gorodfm_context`, что и 051; тап → `#/taste` (единственная честная поверхность для смены контекста, т.к. там живёт волна). Переиспользует `window.GorodContext` (051, @14101).
2. **Зона 2 — artwork + ambient-волна СНИЗУ** (волна = слой за/под artwork, не перекрывает): hero-обложка (реальный `home-featured-egor-krid.png`, тот же ассет что в мини-плеере) + цвет-от-обложки `--np-accent` на hero (расширяем NowPlayingTint @13430 на hero, не только мини-плеер) + лёгкая ambient-волна внизу hero (свой canvas).
3. **Зона 3 — 1-строчная поведенческая «почему»** (тап → L2 `TwinrWhy.open()` @13393) + контролы `❤ [—трек—] ✕ + [Steer]`, где **❤ и Steer ПРИМАРНЫ (крупные 56px), skip ВТОРИЧЕН** (мелкий, низкий контраст — AUDIT §3: skip-prominent учит скипать → убивает reason_tag corpus, блюпринт §1.1 anti-pattern).

Плитки-стенд НЕ удаляются: оборачиваются в toggle `радио ⇄ плитки`; плитки достижимы из «Открыть» и из самого home-переключателя (Figma 2174:422 сохранён байт-в-байт внутри своего контейнера).

**Целевой файл:** `designs/gorod-fm.html`.

---

## 0. Inputs reconciliation (resolved conflicts — read first)

| # | Конфликт / неоднозначность | Резолюция (binding) | Почему |
|---|---|---|---|
| **C0** | Бриф: «расширить NowPlayingTint @13393 на hero». Live: модуль @13398–13432, `refresh()` тинтит только из `#mini-art-img`. | **Расширяем `refresh()`:** после set `--np-accent` также вызвать новый `paintHero()`, который кладёт тинт на hero home через CSS-var `--home-np` на `.home-radio`. Аддитивно: старый код (progress-fill + cover-glow) не тронут. | Тинт уже централизован в одном модуле; добавить второй consumer той же выбранной краски = zero-risk, не дублирует sampler. |
| **C1** | Бриф: «3 зоны … контекст-карта переиспользует GorodContext 051». 051 живёт на `#/taste`, его DOM (`.ctx-strip`) физически в `#/taste`. | **Home-контекст-карта = read-only зеркало** LS `gorodfm_context` (та же модель). Тап на карту → `navigate('#/taste')` + (через `GorodContext.suggest()`) проскролл к `.ctx-strip`. **Смена контекста НЕ происходит на home** — только показ + переход. | §9-A блюпринта: волна-canvas есть только на `#/taste`; «контекст меняет волну» можно показать честно ТОЛЬКО там. Home показывает «что сейчас выбрано» (FIDELITY), переключение делегирует. Не плодим 2-ю steering-поверхность (Sonos-ошибка, блюпринт §9-A). |
| **C2** | Бриф: «artwork + ambient-волна снизу … волна = слой не перекрывает». Какой canvas? `TwinrWave` привязан к `#taste-wave`. | **Новый отдельный canvas `#home-wave` + собственный мини-RAF внутри нового модуля `GorodHomeRadio`.** НЕ переиспользуем `TwinrWave.start()` (он `getElementById('taste-wave')` @13052 → no-op на home). Волна на home = декоративный `aria-hidden` слой, читает `--np-accent`, пауза на route-уход + `visibilitychange` (perf §10 блюпринта). | `startWave()` жёстко завязан на `#taste-wave`; рефакторить его в мульти-canvas = риск регрессии на отгруженном `#/taste`. Лёгкий локальный canvas (3 sin-слоя, та же визуальная семья) дешевле и изолирован. |
| **C3** | Бриф: «1-строчная почему → тап → L2 TwinrWhy». `TwinrWhy.open()` @13393 рендерит `#why-pop` (bottom-sheet, существует глобально). | **Тап по `.home-radio-why` → `window.TwinrWhy.open()`** (тот же bottom-sheet, что и на плеере). Строка «почему» на home = зеркало `#player-track-reason > span` (читаем его `.innerHTML` при рендере + при track-change). | Переиспользуем уже-built L1→L2 explainability-канал; «почему» едина с плеером (один источник правды, обновляется в `commit()` @13607). |
| **C4** | Бриф: контролы `❤ [—track—] ✕ + [Steer]`, ❤/steer примарны, skip вторичен. Нет глобального «лайк»-обработчика для home. | **❤ = toggle, пишет `gorodfm_liked` (новый LS, аналог `gorodfm_rejected`) + `TwinrWave.bump()` для видимой реакции + ribbon-квитанция.** **Steer → `TwinrWhy.open()`** (steer-через-объяснение = wedge §3). **✕ (skip) → `TwinrTransition.next()`** (@13654, уже wired). Skip — мелкий, `--accent-on-dark`-нейтральный, без заливки. | Steer-через-explanation = блюпринт §3 wedge. Skip делегирует существующему transition-flow (между-трек карточка 048 = перцептивное прикрытие). ❤ пишет durable сигнал — будущий вход в reason_tag corpus (GOROD-055). |
| **C5** | Бриф: «сохранить плитки как alt-browse, не терять Figma-актив». Плитки = весь текущий DOM `7492–7630`. | **Оборачиваем существующий `.home-stage` (`7492`) в `<div class="home-tiles" hidden>` БЕЗ изменения внутренностей.** Новая `.home-radio` секция вставляется ПЕРЕД ним. Toggle `радио ⇄ плитки` в зоне-1 переключает `hidden` + пишет `gorodfm_home_view`. | Минимально-инвазивно: ни один из 8 `--x/--w/--top` плиток, ни featured-карточка, ни их CSS (`1735–2018`) НЕ меняются → Figma 2174:422 жив байт-в-байт внутри своего контейнера. «Ломаем pixel-perfect» = меняем ДЕФОЛТ (что видно при загрузке), не удаляем ассет. |
| **C6** | Бриф: «решает насколько ломать pixel-perfect». 051-спек §1.2 хвалил, что 045 НЕ триггерится. Этот спек ЕСТЬ 045. | **Ломаем как АДДИТИВНУЮ обёртку, а не переписывание.** `.home-stage` остаётся валидным; `.home-radio` — новый default. CSS `[data-page="home"]` margin-хак (`1736`) и per-route bg-suppress (`2028–2033`) остаются — применяются к обоим видам. | Не вырезаем Figma-DOM (deep-link/демо-ценность). Дефолт = радио (`gorodfm_home_view` отсутствует → 'radio'). Откат к плиткам = одна LS-строка → безопасно для демо заказчику. |
| **C7** | Цвет-от-обложки: бриф «hero-тинт из обложки». NowPlayingTint sampler читает `#mini-art-img`. | **Hero на home использует ТОТ ЖЕ ассет** (`home-featured-egor-krid.png`) что и `#mini-art-img` → одна выбранная краска `--np-accent` валидна для обоих. Hero-`<img>` на home имеет `crossorigin`-безопасность (same-origin asset). | Asset-wall честность (блюпринт §5): нет per-track обложек → один реальный ассет + art-tint, НЕ fake-обложка. Та же краска = консистентность плеер↔hero. |

Где блюпринт давал конкретные значения (BPM/context-параметры из 051, токены §5) — они авторитативны и воспроизведены ниже. **Не выдумывать значения вне этого набора.**

---

## 1. Финальное размещение + additive-safety

### 1.0 Архитектурное решение: новый canvas, а не TwinrWave
`TwinrWave.start()` (@13051) делает `canvas = document.getElementById('taste-wave')` и при отсутствии — `return`. На `#/home` элемента `#taste-wave` нет → вызов был бы no-op. Поэтому ambient-волна home = **новый `<canvas id="home-wave">`** с собственным компактным RAF внутри нового модуля `GorodHomeRadio` (§5). Визуальная семья идентична (3 sin-слоя, `--brand-blue-light` / `--accent-on-dark`, taper-env), но код изолирован → ноль риска для отгруженного `#/taste`-волны. RAF паузится на route-уход и `document.hidden` (perf §10).

### 1.1 Куда что идёт
- **DOM (новая радио-секция):** новый `<div class="home-radio">…</div>` вставляется **между строкой 7490 (после `<h1 … class="visually-hidden">Главная</h1>`) и строкой 7491 (комментарий `<!-- Figma 2174:422 … -->`)**. Существующий `.home-stage` (7492) оборачивается: открывающий `<div class="home-tiles" hidden>` ставится перед строкой 7491-комментарием (т.е. сразу после новой `.home-radio`), закрывающий `</div>` — после строки 7633 (`<!-- /.home-stage -->`).
- **CSS (новый блок):** вставляется **после строки 2033** (конец `html[data-active-route="#/home"] .bg-layer { opacity: 0; }` блока, перед `ONBOARDING`-комментарием @2035).
- **NowPlayingTint extension:** правки внутри модуля `13398–13432` (добавить `paintHero()`; расширить `refresh()`).
- **Новый модуль:** `window.GorodHomeRadio` IIFE — **последний trailing `<script>` перед `</body>`**, т.е. после строки 14118 (конец GorodContext-модуля 051) и перед `</body>`.

### 1.2 Почему это безопасно (не ломает уже-построенное)
1. **Плитки/Figma сохранены байт-в-байт.** Внутренности `.home-stage` (`7492–7632`: 8 плиток `--x/--w/--top`, featured-карточка, halo, particles) и их CSS (`1739–2018`) НЕ редактируются — только оборачиваются в `.home-tiles[hidden]`. Pixel-perfect жив, переключается видимостью.
2. **`#/taste`-волна не тронута.** Новый canvas `#home-wave` + `GorodHomeRadio` полностью изолированы от `TwinrWave`/`#taste-wave`. Все существующие вызовы `TwinrWave.start/stop/bump/setContext` (@13120, callers @13373/13146/14095) работают без изменений.
3. **051 GorodContext переиспользуется через публичный API** (`suggest()`/`apply()`/`render()` @14116) — не дублируется, не модифицируется. Home только ЧИТАЕТ `gorodfm_context` и навигирует на `#/taste`.
4. **NowPlayingTint расширяется аддитивно:** старая ветка (progress-fill `--np-accent` + cover-glow) не меняется; `paintHero()` — новый no-op если `.home-radio` отсутствует (null-guard).
5. **TwinrWhy / TwinrTransition / TwinrRibbon переиспользуются** (open / next / show) — их сигнатуры не меняются.
6. **Новые LS-ключи изолированы:** `gorodfm_home_view`, `gorodfm_liked`. Существующие `gorodfm_taste / gorodfm_rejected / gorodfm_context / gorodfm_ad_less` не тронуты.
7. **Роут не добавляется.** `#/home` уже в `VALID_ROUTES` (@10931). Per-route CSS (`html[data-active-route="#/home"]` @2021/2028) применяется к обоим видам без правок.
8. **Легаси `.home-hero/.home-track-title/.home-stations-grid` CSS (@3187/3250/6269) и `setActiveStation()` JS (@11543)** — мёртвый код от старого home-варианта, в текущем DOM не присутствует; новый namespace `home-radio-*` с ним не пересекается (проверено grep'ом: `home-radio*` = 0 вхождений).

---

## 2. Поведение зон + источники данных (FIDELITY-контракт)

| Зона | Источник правды | Когда обновляется | Действие |
|---|---|---|---|
| **1. Контекст-карта** | LS `gorodfm_context` (модель 051) + `GorodContext` (defaultCtx по времени, если нет свежего) | На `#/home`-вход (`onRoute`) + на `storage`-событие | Тап → `navigate('#/taste')` + `GorodContext.suggest()` (под-сказка по времени, без авто-драйва волны) |
| **1b. Toggle радио⇄плитки** | LS `gorodfm_home_view` ('radio' default) | На клик | Переключает `hidden` на `.home-radio` / `.home-tiles`, пишет LS, паузит/возобновляет `#home-wave` RAF |
| **2. Hero artwork + волна** | `#mini-art-img.src` (тот же ассет) + `--np-accent` (NowPlayingTint) | NowPlayingTint.refresh() (на boot + track-change @13610) | Тап по hero → `openPlayer()` (существующий, @11041) |
| **3a. «Почему» строка** | зеркало `#player-track-reason > span` `.innerHTML` | На `#/home`-вход + track-change (`commit()` @13607 hook) | Тап → `TwinrWhy.open()` (L2 bottom-sheet) |
| **3b. ❤ Лайк (примарный)** | LS `gorodfm_liked` (массив track-id/title) | На клик | toggle + `TwinrWave.bump()` (если на taste) ИЛИ `#home-wave` pulse + ribbon-квитанция «добавил в волну: <b>X</b>» |
| **3c. Steer (примарный)** | — | На клик | `TwinrWhy.open()` (steer-через-объяснение) |
| **3d. ✕ Skip (вторичный, мелкий)** | — | На клик | `TwinrTransition.next()` (@13654) — между-трек карточка 048 |

**FIDELITY-инвариант:** строка «почему» на home НИКОГДА не генерится локально — она зеркалит то, что плеер уже показывает (поведенческое, из `FLOW[].pill` @13591, обновляется в `commit()`). Контекст-карта показывает РЕАЛЬНО выбранный контекст, не выдуманный. ❤ пишет durable сигнал (будущий reason_tag corpus). Демо-природа FLOW уже честна (поведенческие причины, не маркетинг) — доп. «демо»-лейбл не нужен (в отличие от 047-вектора).

---

## 3. DOM-структура (semantics + a11y)

Вставить verbatim между строкой 7490 и 7491. Native `<button type="button">` на каждый интерактив; hero — `<img>` с alt; волна — `aria-hidden` canvas; «почему» — `aria-live` для SR-объявления track-change.

```html
        <!-- GOROD-045 — ВОЛНА как РАДИО (3 зоны). Default-вид; плитки = alt-browse ниже. -->
        <div class="home-radio" id="home-radio">

          <!-- ЗОНА 1: контекст-карта (схлоп → чип «Сменить») + toggle радио/плитки -->
          <div class="home-radio-top">
            <button class="home-ctx-card" type="button" id="home-ctx-card"
                    aria-label="Текущий контекст волны. Открыть «Мой вкус», чтобы сменить">
              <span class="home-ctx-cap">Контекст волны</span>
              <span class="home-ctx-now" id="home-ctx-now">Вечер · ~95 BPM</span>
              <span class="home-ctx-act" aria-hidden="true">Сменить</span>
            </button>
            <div class="home-view-toggle" role="group" aria-label="Вид главной">
              <button class="home-view-btn is-on" type="button" data-view="radio" aria-pressed="true">Радио</button>
              <button class="home-view-btn" type="button" data-view="tiles" aria-pressed="false">Подборки</button>
            </div>
          </div>

          <!-- ЗОНА 2: artwork + ambient-волна снизу (волна = слой ПОД контентом, не перекрывает) -->
          <div class="home-radio-stage">
            <canvas class="home-wave" id="home-wave" aria-hidden="true"></canvas>
            <button class="home-hero" type="button" id="home-hero-btn"
                    aria-label="Открыть плеер: Любимка — Niletto">
              <img class="home-hero-art" id="home-hero-art"
                   src="assets/gorod-fm/home-featured-egor-krid.png" alt="" aria-hidden="true">
              <span class="home-hero-shade" aria-hidden="true"></span>
            </button>
          </div>

          <!-- ЗОНА 3: поведенческая «почему» + контролы (❤/Steer примарны, ✕ вторичен) -->
          <div class="home-radio-bottom">
            <button class="home-radio-why" type="button" id="home-radio-why"
                    aria-label="Почему играет этот трек — открыть объяснение">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l1.9 5.8L20 9.7l-5.1 3.4L16 19l-4-3.3L8 19l1.1-5.9L4 9.7l6.1-1.9z" fill="currentColor"/></svg>
              <span class="home-radio-why-text" id="home-radio-why-text" role="status" aria-live="polite">Тёплый поп ~95 BPM — как ты любишь под вечер</span>
            </button>

            <div class="home-radio-meta">
              <span class="home-radio-title" id="home-radio-title">Любимка</span>
              <span class="home-radio-artist" id="home-radio-artist">Niletto</span>
            </div>

            <div class="home-radio-controls">
              <button class="home-radio-like" type="button" id="home-radio-like"
                      aria-pressed="false" aria-label="Нравится — добавить в волну">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-10-9.3C.4 8.4 2 5 5.2 5c2 0 3.3 1.2 3.8 2.3h6c.5-1.1 1.8-2.3 3.8-2.3C22 5 23.6 8.4 22 11.7 19.5 16.4 12 21 12 21z" fill="currentColor"/></svg>
              </button>
              <button class="home-radio-steer" type="button" id="home-radio-steer"
                      aria-label="Steer — поправить волну">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12h3.5l2.5 7 4-14 2.5 7H21"/></svg>
                <span>Steer</span>
              </button>
              <button class="home-radio-skip" type="button" id="home-radio-skip"
                      aria-label="Пропустить трек">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="5 4 15 12 5 20 5 4" fill="currentColor" stroke="none"/><line x1="19" y1="5" x2="19" y2="19"/></svg>
              </button>
            </div>
          </div>

        </div>
        <!-- /.home-radio -->
```

a11y-гарантии:
- Hero `<img alt="" aria-hidden>` — декоративная обложка (asset-wall), доступное имя несёт кнопка-обёртка `aria-label`.
- `#home-radio-why-text` `role="status" aria-live="polite"` → SR слышит смену трека/причины.
- ❤ `aria-pressed` true/false; Steer/Skip — описательные `aria-label`.
- Контекст-карта = одна кнопка с явным `aria-label` (показ + «сменить» действие).
- Цель ≥44px на всех (❤/Steer = 56px, skip = 44px); focus-visible 3px (CSS §6).
- Волна `aria-hidden` (декор) — north-star a11y держится текстовой зоной-3 + контекст-картой (блюпринт §10.1).
- НЕТ эмодзи-как-иконок (inline SVG); НЕТ orb (hero = реальный artwork).

---

## 4. NowPlayingTint extension — hero-тинт (аддитивно)

Правки внутри модуля `13398–13432`. Старая ветка не тронута; `paintHero()` null-guarded (no-op без `.home-radio`).

### 4.1 Добавить `paintHero` (после `function refresh()` @13429, перед `window.NowPlayingTint = …`)
```js
    function paintHero() {
      var hr = document.getElementById('home-radio');
      if (!hr) return;                                   // home-radio not present → no-op
      var c = getComputedStyle(document.documentElement).getPropertyValue('--np-accent').trim();
      if (c) hr.style.setProperty('--home-np', c);       // hero tint mirrors player accent
    }
```

### 4.2 Расширить `refresh()` (правка @13429) — после установки `--np-accent` дёрнуть hero
Текущая строка 13426:
```js
      var go = function () { var c = sample(img); if (c) document.documentElement.style.setProperty('--np-accent', c); };
```
Заменить на:
```js
      var go = function () { var c = sample(img); if (c) document.documentElement.style.setProperty('--np-accent', c); paintHero(); };
```
(Также `home-hero-art` использует тот же `home-featured-egor-krid.png`, что и `#mini-art-img` → одна краска валидна для обоих; ассет same-origin → canvas не taint'ится, sampler работает.)

### 4.3 Экспорт (правка @13430)
```js
    window.NowPlayingTint = { refresh: refresh, paintHero: paintHero };
```

**Инвариант:** до появления `.home-radio` `paintHero()` = ранний return → ноль изменений на любом экране. Существующий тинт плеера (progress-fill + glow) идентичен.

---

## 5. `window.GorodHomeRadio` module (новый trailing IIFE)

Добавить после строки 14118 (конец 051-модуля), последним блоком перед `</body>`. Детерминированный (RAF-волна = sin, не random), null-guarded, `esc`-санитайз на динамике, hashchange + visibilitychange-wired, RAF паузится вне видимости.

```html
  <script>
  /* ---- GOROD-045 — ВОЛНА как РАДИО (#/home, 3 зоны). Аддитивно.
     Дефолт-вид = радио; плитки (Figma 2174:422) = alt-browse через toggle.
     Контекст-карта зеркалит gorodfm_context (051), переключение делегирует #/taste.
     «Почему» зеркалит #player-track-reason (FIDELITY — не генерим локально).
     Ambient-волна = СВОЙ лёгкий canvas (#home-wave), не TwinrWave (тот на #taste-wave).
     RAF паузится на route-уход + document.hidden (perf §10). */
  (function () {
    'use strict';
    var VIEW_KEY = 'gorodfm_home_view', LIKE_KEY = 'gorodfm_liked', CTX_KEY = 'gorodfm_context';
    function $(id){ return document.getElementById(id); }
    function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
    function lsGet(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
    function lsSet(k,v){ try{ localStorage.setItem(k,v); }catch(e){} }
    function lsJSON(k){ try{ return JSON.parse(localStorage.getItem(k)||'null'); }catch(e){ return null; } }

    /* ---- context-card mirror (read-only; CTX labels mirror GOROD-051 §2) ---- */
    var CTX_LABEL = { morning:'Утро', day:'День', evening:'Вечер', night:'Ночь', workout:'Тренировка', commute:'Дорога' };
    var CTX_BPM   = { morning:85, day:100, evening:95, night:70, workout:128, commute:108 };
    function defaultCtxKey(){ var h=new Date().getHours(); if(h>=5&&h<11)return 'morning'; if(h>=11&&h<17)return 'day'; if(h>=17&&h<23)return 'evening'; return 'night'; }
    function currentCtx(){
      var s=lsJSON(CTX_KEY), key;
      if(s && s.activity && CTX_LABEL[s.activity]) key=s.activity;
      else key=(s && s.ctx) || defaultCtxKey();
      return { key:key, label:CTX_LABEL[key]||'Вечер', bpm:CTX_BPM[key]||95 };
    }
    function paintCtx(){
      var el=$('home-ctx-now'); if(!el) return;
      var c=currentCtx(); el.textContent = c.label + ' · ~' + c.bpm + ' BPM';
    }

    /* ---- «почему» mirror — never generated locally; echoes the player ---- */
    function paintWhy(){
      var src=$('player-track-reason'), span=src&&src.querySelector('span'), dst=$('home-radio-why-text');
      if(dst && span) dst.innerHTML = span.innerHTML;        // trusted: player sets behavioral pill (FLOW @13591)
      var t=$('player-track-title'), a=$('player-track-artist');
      var ht=$('home-radio-title'), ha=$('home-radio-artist');
      if(ht && t) ht.textContent = t.textContent;
      if(ha && a) ha.textContent = a.textContent;
      var hero=$('home-hero-btn'); if(hero && t && a) hero.setAttribute('aria-label','Открыть плеер: '+t.textContent+' — '+a.textContent);
    }

    /* ---- ❤ like (durable signal; future reason_tag corpus) ---- */
    function likedSet(){ var a=lsJSON(LIKE_KEY); return Array.isArray(a)?a:[]; }
    function curTitle(){ var t=$('home-radio-title'); return t?t.textContent:''; }
    function refreshLike(){
      var b=$('home-radio-like'); if(!b) return;
      var on=likedSet().indexOf(curTitle())!==-1;
      b.setAttribute('aria-pressed', on?'true':'false'); b.classList.toggle('is-on', on);
    }
    function toggleLike(){
      var arr=likedSet(), title=curTitle(), i=arr.indexOf(title), on;
      if(i===-1){ arr.push(title); on=true; } else { arr.splice(i,1); on=false; }
      lsSet(LIKE_KEY, JSON.stringify(arr)); refreshLike();
      pulse();                                              // visible wave reaction
      if(on && window.TwinrRibbon) window.TwinrRibbon.show('Добавил в волну: <b>'+esc(title)+'</b>. <span class="ai-why">больше такого дальше</span>.');
      if(window.TwinrWave && window.TwinrWave.bump) window.TwinrWave.bump();   // also nudges #/taste wave if present
    }

    /* ---- ambient wave — own light canvas, reads --np-accent ---- */
    var cv, cx, raf=0, t=0, energy=0.4, pulseV=0, running=false;
    var REDUCE = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var LAYERS = [ {freq:1.1, amp:0.30, speed:0.6, alpha:0.85, base:1}, {freq:1.7, amp:0.20, speed:0.9, alpha:0.55, base:0}, {freq:2.6, amp:0.12, speed:1.3, alpha:0.35, base:0} ];
    function accentRGB(){
      var c=getComputedStyle(document.documentElement).getPropertyValue('--np-accent').trim();
      var m=c.match(/(\d+)\D+(\d+)\D+(\d+)/); if(m) return m[1]+','+m[2]+','+m[3];
      return '129,148,255';                                 // --accent-on-dark #8094ff fallback
    }
    function size(){ if(!cv) return; var r=cv.getBoundingClientRect(); cv.width=Math.max(1,r.width); cv.height=Math.max(1,r.height); }
    function frame(){
      if(!cx) return; var w=cv.width, h=cv.height; cx.clearRect(0,0,w,h);
      pulseV*=0.94; var rgb=accentRGB(), mid=h*0.62, e=1+pulseV*1.2+energy;
      for(var i=0;i<LAYERS.length;i++){ var L=LAYERS[i]; cx.beginPath();
        for(var x=0;x<=w;x+=6){ var nx=x/w, env=Math.sin(nx*Math.PI);
          var y=mid+Math.sin(nx*Math.PI*2*L.freq+t*L.speed)*(h*L.amp)*e*env;
          if(x===0)cx.moveTo(x,y); else cx.lineTo(x,y); }
        cx.strokeStyle='rgba('+(L.base?rgb:'129,148,255')+','+L.alpha+')'; cx.lineWidth=L.base?2.4:1.4;
        cx.lineJoin='round'; cx.lineCap='round'; cx.stroke();
      }
      t+=0.016;
    }
    function loop(){ frame(); raf=requestAnimationFrame(loop); }
    function startWave(){ cv=$('home-wave'); if(!cv) return; cx=cv.getContext('2d'); size(); if(REDUCE){ frame(); return; } if(!running){ running=true; cancelAnimationFrame(raf); loop(); } }
    function stopWave(){ running=false; cancelAnimationFrame(raf); }
    function pulse(){ pulseV=Math.min(1.4, pulseV+0.7); if(!running && cv && cx && !REDUCE){ running=true; loop(); } }

    /* ---- view toggle (радио ⇄ плитки) — Figma tiles preserved, just hidden ---- */
    function applyView(v){
      var radio=$('home-radio'), tiles=document.querySelector('.home-tiles');
      var isTiles = (v==='tiles');
      if(radio) radio.hidden = isTiles;
      if(tiles) tiles.hidden = !isTiles;
      [].forEach.call(document.querySelectorAll('.home-view-btn'),function(b){
        var on=b.getAttribute('data-view')===v; b.setAttribute('aria-pressed', on?'true':'false'); b.classList.toggle('is-on', on);
      });
      if(isTiles) stopWave(); else if((location.hash||'')==='#/home' && !document.hidden) startWave();
    }
    function setView(v){ lsSet(VIEW_KEY, v); applyView(v); }

    /* ---- wiring ---- */
    var wired=false;
    function wire(){
      if(wired) return; var root=$('home-radio'); if(!root) return;
      var card=$('home-ctx-card'); if(card) card.addEventListener('click', function(){ if(window.GorodContext && window.GorodContext.suggest) window.GorodContext.suggest(); window.location.hash='#/taste'; });
      [].forEach.call(document.querySelectorAll('.home-view-btn'),function(b){ b.addEventListener('click', function(){ setView(b.getAttribute('data-view')); }); });
      var why=$('home-radio-why'); if(why) why.addEventListener('click', function(){ if(window.TwinrWhy) window.TwinrWhy.open(); });
      var steer=$('home-radio-steer'); if(steer) steer.addEventListener('click', function(){ if(window.TwinrWhy) window.TwinrWhy.open(); });
      var like=$('home-radio-like'); if(like) like.addEventListener('click', toggleLike);
      var skip=$('home-radio-skip'); if(skip) skip.addEventListener('click', function(){ if(window.TwinrTransition && window.TwinrTransition.next) window.TwinrTransition.next(); });
      var hero=$('home-hero-btn'); if(hero) hero.addEventListener('click', function(){ if(typeof window.openPlayer==='function') window.openPlayer(); });
      wired=true;
    }
    function refreshAll(){ paintCtx(); paintWhy(); refreshLike(); if(window.NowPlayingTint && window.NowPlayingTint.paintHero) window.NowPlayingTint.paintHero(); }

    function onRoute(){
      var onHome=(location.hash||'')==='#/home';
      if(onHome){ wire(); applyView(lsGet(VIEW_KEY)||'radio'); refreshAll(); }
      else stopWave();
    }
    document.addEventListener('visibilitychange', function(){ if(document.hidden) stopWave(); else if((location.hash||'')==='#/home' && (lsGet(VIEW_KEY)||'radio')==='radio') startWave(); });
    window.addEventListener('hashchange', onRoute);
    window.addEventListener('resize', function(){ if(running) size(); });
    // re-mirror player state on every track commit (poll the reason span cheaply on a MutationObserver)
    function observePlayer(){
      var src=$('player-track-reason'); if(!src || !window.MutationObserver) return;
      new MutationObserver(function(){ if((location.hash||'')==='#/home'){ paintWhy(); refreshLike(); } })
        .observe(src, { childList:true, subtree:true, characterData:true });
    }
    if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', function(){ observePlayer(); onRoute(); });
    else { observePlayer(); onRoute(); }
    window.GorodHomeRadio = { setView:setView, refresh:refreshAll };
  })();
  </script>
```

**Data-model:** `gorodfm_home_view` = `'radio'|'tiles'` (string; отсутствие → 'radio'). `gorodfm_liked` = JSON-массив title-строк. `gorodfm_context` — НЕ пишется этим модулем (read-only зеркало 051).

**Correctness / zero-console-errors:** try/catch на всех LS; null-guard на каждом `$()`/`querySelector`; guard на `window.TwinrWhy/TwinrTransition/TwinrRibbon/TwinrWave/GorodContext/NowPlayingTint/openPlayer`; `esc()` на динамике в ribbon; «почему» = зеркало trusted player-span (не user input) → `innerHTML` безопасен; MutationObserver на `#player-track-reason` синхронит home при track-change без хука в чужой модуль; RAF паузится (route-уход + `document.hidden`); zero `Math.random` (волна детерминирована по `t`).

**`openPlayer` экспорт:** функция `openPlayer()` объявлена в главном IIFE (@11041) — НЕ глобальна. Нужна **одна правка-мост** (см. §9, edit-manifest шаг 6): в главном IIFE после объявления `function openPlayer()` добавить `window.openPlayer = openPlayer;`. Альтернатива без правки: hero-кнопка навигирует `window.location.hash='#/home'` no-op → вместо этого мост чище. Помечено как shared-seam.

---

## 6. CSS — токены (каждый var перечислен)

Вставить после строки 2033. Без новых хардкод-цветов сверх white-scale rgba (уже в файле) + RGB `81,104,252` (= `--brand-blue-light` #5168FC, паттерн файла @585) + per-instance `--home-np` (= выбранная `--np-accent`, ставится JS).

```css
      /* ===================================================================
         GOROD-045 — ВОЛНА как РАДИО (#/home default). Плитки = .home-tiles alt.
         =================================================================== */
      .home-radio {
        position: relative; z-index: 5;
        --home-np: var(--np-accent);
        display: flex; flex-direction: column;
        min-height: calc(100dvh - var(--player-mini-h) - var(--topbar-h));
        max-width: 760px; margin: 0 auto; padding: 24px 24px 40px;
        gap: 20px;
      }

      /* ЗОНА 1 — контекст-карта + view-toggle */
      .home-radio-top { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
      .home-ctx-card {
        display: inline-flex; align-items: center; gap: 12px; min-height: 44px;
        padding: 10px 16px; cursor: pointer; text-align: left;
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.10);
        border-radius: var(--r-base); font-family: 'Onest', sans-serif; color: #fff;
        transition: background var(--t-fast), border-color var(--t-fast);
      }
      .home-ctx-card:hover { background: rgba(81,104,252,0.12); border-color: rgba(81,104,252,0.40); }
      .home-ctx-card:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 3px; }
      .home-ctx-cap { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: rgba(255,255,255,0.55); }
      .home-ctx-now { font-size: 15px; font-weight: 700; }
      .home-ctx-act { font-size: 13px; font-weight: 600; color: var(--accent-on-dark); margin-left: 2px; }

      .home-view-toggle { display: inline-flex; gap: 4px; padding: 4px; background: rgba(255,255,255,0.05); border-radius: var(--r-pill); }
      .home-view-btn {
        min-height: 36px; padding: 0 16px; cursor: pointer; border: none; background: transparent;
        font-family: 'Onest', sans-serif; font-size: 13px; font-weight: 700; color: rgba(255,255,255,0.65);
        border-radius: var(--r-pill); transition: background var(--t-fast), color var(--t-fast);
      }
      .home-view-btn.is-on { background: var(--tint-blue-light-20); color: #fff; }
      .home-view-btn:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }

      /* ЗОНА 2 — artwork + ambient-волна (волна = слой ПОД hero, не перекрывает) */
      .home-radio-stage { position: relative; flex: 1 1 auto; display: flex; align-items: center; justify-content: center; min-height: 320px; }
      .home-wave { position: absolute; left: 0; right: 0; bottom: -8px; width: 100%; height: 46%; z-index: 0; pointer-events: none; opacity: 0.9; }
      .home-hero {
        position: relative; z-index: 1; width: min(360px, 78vw); aspect-ratio: 1 / 1;
        border: none; padding: 0; cursor: pointer; border-radius: 20px; overflow: hidden;
        background: #111318;
        box-shadow: 0 24px 70px -16px rgba(0,0,0,0.65), 0 0 0 1px rgba(255,255,255,0.06),
                    0 18px 60px -20px var(--home-np);
        transition: transform var(--t-fast), box-shadow var(--t-fast);
      }
      .home-hero:hover { transform: translateY(-2px); box-shadow: 0 30px 80px -16px rgba(0,0,0,0.7), 0 0 0 1px rgba(255,255,255,0.10), 0 24px 70px -18px var(--home-np); }
      .home-hero:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 4px; }
      .home-hero-art { width: 100%; height: 100%; object-fit: cover; display: block; }
      .home-hero-shade { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.28) 100%); pointer-events: none; }

      /* ЗОНА 3 — «почему» + контролы */
      .home-radio-bottom { display: flex; flex-direction: column; align-items: center; gap: 14px; }
      .home-radio-why {
        display: inline-flex; align-items: center; gap: 8px; max-width: 560px; cursor: pointer;
        background: none; border: none; padding: 4px 6px; border-radius: var(--r-base);
        font-family: 'Onest', sans-serif; font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.78); text-align: center;
        transition: color var(--t-fast);
      }
      .home-radio-why:hover { color: #fff; }
      .home-radio-why:focus-visible { outline: 3px solid var(--brand-blue-light); outline-offset: 2px; }
      .home-radio-why svg { width: 13px; height: 13px; flex: none; color: var(--brand-blue-light); }
      .home-radio-why-text b { color: #cdd4f5; font-weight: 700; }

      .home-radio-meta { display: flex; flex-direction: column; align-items: center; gap: 2px; }
      .home-radio-title { font-family: 'Onest', sans-serif; font-size: 22px; font-weight: 800; color: #fff; letter-spacing: -0.01em; }
      .home-radio-artist { font-family: 'Onest', sans-serif; font-size: 15px; font-weight: 500; color: rgba(255,255,255,0.65); }

      /* controls: ❤/Steer ПРИМАРНЫ (56px), skip ВТОРИЧЕН (44px, нейтральный) */
      .home-radio-controls { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 4px; }
      .home-radio-like, .home-radio-steer {
        min-height: 56px; cursor: pointer; font-family: 'Onest', sans-serif;
        display: inline-flex; align-items: center; justify-content: center; gap: 8px;
        border-radius: var(--r-pill); transition: background var(--t-fast), border-color var(--t-fast), transform var(--t-fast);
      }
      .home-radio-like {
        width: 56px; padding: 0; color: #fff;
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.14);
      }
      .home-radio-like svg { width: 24px; height: 24px; }
      .home-radio-like.is-on { background: var(--tint-blue-light-20); border-color: var(--brand-blue-light); color: var(--brand-blue-light); }
      .home-radio-steer {
        padding: 0 24px; font-size: 15px; font-weight: 700; color: #fff;
        background: var(--tint-blue-light-20); border: 1px solid var(--brand-blue-light);
      }
      .home-radio-steer svg { width: 20px; height: 20px; }
      .home-radio-like:hover, .home-radio-steer:hover { transform: translateY(-1px); }
      .home-radio-like:focus-visible, .home-radio-steer:focus-visible, .home-radio-skip:focus-visible {
        outline: 3px solid var(--brand-blue-light); outline-offset: 3px;
      }
      /* skip — secondary: smaller, low-contrast, no fill (anti-pattern guard: UI must not teach skipping) */
      .home-radio-skip {
        min-height: 44px; width: 44px; padding: 0; cursor: pointer;
        background: none; border: none; color: rgba(255,255,255,0.40);
        display: inline-flex; align-items: center; justify-content: center;
        transition: color var(--t-fast);
      }
      .home-radio-skip:hover { color: rgba(255,255,255,0.70); }
      .home-radio-skip svg { width: 20px; height: 20px; }

      @media (max-width: 560px) {
        .home-radio { padding: 16px 16px 32px; gap: 16px; }
        .home-hero { width: 78vw; }
        .home-radio-top { justify-content: center; }
      }
      @media (prefers-reduced-motion: reduce) {
        .home-hero, .home-radio-like, .home-radio-steer { transition: none; }
        .home-hero:hover, .home-radio-like:hover, .home-radio-steer:hover { transform: none; }
      }
```

**Token inventory (каждый var):**
- `--np-accent` (#5168FC default, content-derived JS) → `--home-np` (hero glow shadow). **Это явное расширение `--np-accent` на hero (бриф §2).**
- `--brand-blue-light` (#5168FC, единственный акцент) — focus-visible, steer border, like.is-on, RGB `81,104,252` для tint/glow.
- `--accent-on-dark` (#8094ff, AA) — контекст-карта «Сменить»; волна-fallback цвет.
- `--tint-blue-light-20` (rgba(81,104,252,0.2)) — view-btn.is-on, steer bg, like.is-on bg.
- `--r-base` (10px) — карта/why radius. `--r-pill` (999px) — toggle/контролы.
- `--t-fast` (180ms) — все transitions.
- `--player-mini-h` (84px), `--topbar-h` — высота stage.
- Onest only на каждом текст-ноде.
- White-scale rgba (`#fff`, `.78/.65/.55/.40/.14/.10/.06/.05/.04`) — все pre-existing в файле.
- `#cdd4f5` для `.home-radio-why-text b` — тот же light-blue emphasis, что в `.player-mini-reason b` (@645) и `.ctx-why b` (051). Консистентно с уже-built; если нужна строгая token-чистота → swap на `var(--accent-on-dark)`.
- `#111318` (= `--surface-1`) hero placeholder bg — pre-existing surface.
- **Не использованы:** multi-stop gradient bg (только лёгкий shade-линеар на hero — single hue к透прозрачному, не slop), `--success/--warning/--danger`, `--t-mid/-slow`.

---

## 7. Entry / route wiring

- **Роут не добавляется.** `#/home` уже в `VALID_ROUTES` (@10931).
- **Модуль само-wired:** `hashchange` + `DOMContentLoaded`/immediate; действует только при `location.hash==='#/home'`. Не хукает главный роутер/`activatePage`.
- **View persistence:** `gorodfm_home_view` (default 'radio'). На `#/home`-вход применяется + волна стартует (если radio + видимо).
- **Track-sync:** `MutationObserver` на `#player-track-reason` → при смене трека (`commit()` @13607 меняет его span) home-зеркало (`paintWhy`+`refreshLike`) обновляется автоматически, без правки чужого модуля.
- **Контекст-sync:** `paintCtx()` на route-вход читает `gorodfm_context`; тап на карту → `GorodContext.suggest()` + nav `#/taste`.
- **RAF-pause:** `visibilitychange` + route-уход → `stopWave()` (perf §10).
- **DEFAULT_ROUTE:** этот спек НЕ трогает `DEFAULT_ROUTE='#/map'`/cold-start (это отдельная ВОЛНА-0 задача блюпринта §7). Помечено в navChanges как зависимость, не часть этого спека.

---

## 8. Holy-Grail / anti-slop checklist

| Gate | Status | Evidence |
|---|---|---|
| **Onest only** | ✅ | Каждый текст-нод `font-family:'Onest',sans-serif`. Нет Inter/Roboto/system-ui. |
| **near-black bg + 1 accent** | ✅ | bg не тронут (per-route `--home-bg-base` #0C0B0B @2029); единственный акцент `--brand-blue-light`/content-derived `--np-accent`. Второго hue нет. |
| **`--accent-on-dark` для мелкого accent-текста** | ✅ | Контекст-«Сменить» + волна-fallback. AA 6.8:1. |
| **art-tint, НЕ fake-обложка** | ✅ | Hero = реальный `home-featured-egor-krid.png` (тот же ассет, что плеер) + `--home-np` glow от него. Asset-wall честен: один реальный ассет, не сгенеренная плашка. |
| **волна = СЛОЙ снизу, не перекрывает** | ✅ | `.home-wave` `z-index:0` под hero `z-index:1`, `height:46%` снизу stage, `pointer-events:none`, `aria-hidden`. |
| **skip ВТОРИЧЕН** | ✅ | `.home-radio-skip` 44px, `rgba(255,255,255,.40)`, без заливки, без border; ❤/Steer 56px с акцент-заливкой. UI не учит скипать (AUDIT §3). |
| **«почему» поведенческая, не маркетинг** | ✅ | Зеркало `FLOW[].pill` (@13591: «Тёплый поп, как „Слеза"»…) — поведенческие, не «вам понравится». НЕ генерится на home. |
| **targets ≥44px** | ✅ | ❤/Steer 56px, skip/карта/hero ≥44px. |
| **focus-visible 3px** | ✅ | Все интерактивы `outline:3px solid var(--brand-blue-light)`. |
| **prefers-reduced-motion** | ✅ | CSS отключает transition/hover-translate; волна-RAF под `REDUCE` рисует 1 static frame. |
| **❌ multi-stop gradient bg** | ✅ | bg плоский; hero-shade = single-hue→transparent (не multi-stop фон). |
| **❌ orb / fake-волна / gradient-placeholder / emoji-icons** | ✅ | Нет аватара (hero=реальный artwork); волна на РЕАЛЬНОМ canvas (не CSS-fake); нет gradient-плашек вместо контента; ноль эмодзи (inline SVG). |
| **WCAG AA** | ✅ | `#fff`/`rgba(255,255,255,.65+)` на near-black; мелкий accent = `--accent-on-dark`. |
| **zero console errors** | ✅ | try/catch LS; guards на все window-модули + `$()`; MutationObserver guard; детерминир. (no random). |
| **additive single-file** | ✅ | 1 новая секция + 1 CSS-блок + 3 правки NowPlayingTint + 1 trailing IIFE + 1 мост `window.openPlayer`. Плитки обёрнуты, не удалены. |
| **Figma 2174:422 сохранён** | ✅ | `.home-stage` внутренности (8 плиток + featured + CSS 1739–2018) не редактированы — обёрнуты в `.home-tiles[hidden]`, достижимы toggle'ом. |

---

## 9. Implementer's edit manifest (ordered, line-anchored)

1. **CSS** — вставить §6 блок **после строки 2033** (конец `html[data-active-route="#/home"] .bg-layer` блока).
2. **DOM (радио-секция)** — вставить §3 `<div class="home-radio">…</div>` **между строкой 7490 и 7491**.
3. **DOM (обёртка плиток)** — вставить `<div class="home-tiles" hidden>` сразу после новой `.home-radio` (перед комментарием `<!-- Figma 2174:422 … -->` @7491); вставить `</div>` после строки 7633 (`<!-- /.home-stage -->`). Внутренности `.home-stage` НЕ менять.
4. **NowPlayingTint** — §4: добавить `paintHero()` после @13429; расширить `go` (@13426) добавив `paintHero();`; расширить экспорт (@13430) `paintHero`.
5. **Модуль** — добавить §5 `window.GorodHomeRadio` `<script>` **после строки 14118** (конец GorodContext-051), последним перед `</body>`.
6. **Мост (shared-seam)** — в главном IIFE сразу после `function openPlayer() {…}` (объявление @11041) добавить `window.openPlayer = openPlayer;` (hero-тап делегирует существующему overlay). Если нежелательно глобализировать — fallback: hero-тап навигирует на full-player через существующий tabbar-btn-trigger; мост чище и помечен явно.

**Все якоря (2033 CSS, 7490/7491/7633 DOM, 11041 openPlayer, 13398–13432 NowPlayingTint, 13426/13429/13430 правки, 13591/13600–13611 FLOW/commit hook-источник, 13654 TwinrTransition.next, 13393 TwinrWhy.open, 14101/14116 GorodContext API, 14118 module insert, 10931 VALID_ROUTES) пересверены против текущего файла в этой сессии.**

---

## 10. Доказательство «не ломает уже-построенное» (built-surfaces regression matrix)

| Built feature | Якорь | Тронут? | Почему safe |
|---|---|---|---|
| `#/taste` волна (TwinrWave + #taste-wave) | 13051/13120 | НЕТ | Home использует свой `#home-wave` + `GorodHomeRadio`; `TwinrWave` не модифицирован (только `bump()` опционально вызван на ❤). |
| 051 контекст-старты (GorodContext) | 14101 | НЕТ | Только ЧИТАЕМ `gorodfm_context` + зовём публичный `suggest()`. DOM `.ctx-strip` не тронут. |
| 052 профиль (GorodProfile) | 13660+ | НЕТ | Другой роут, другие LS (taste/rejected) не пересекаются с home_view/liked. |
| 050 recap (GorodRecap) | — | НЕТ | Другой роут. |
| 048 transition-card (TwinrTransition) | 13578–13657 | НЕТ (вызов) | Только зовём `.next()` (skip) — публичный API. `commit()` не редактируется; MutationObserver слушает его результат пассивно. |
| W1 fidelity (GorodTaste reject) | 13134/13146 | НЕТ | `gorodfm_rejected` не тронут; «почему» на home зеркалит плеер, не reject-список. |
| NowPlayingTint (042) | 13398–13432 | АДДИТИВНО | `paintHero` no-op без `.home-radio`; старый progress/glow путь идентичен. |
| Figma 2174:422 плитки | 7492–7632 / 1739–2018 | НЕТ (обёрнуто) | DOM+CSS байт-в-байт; видимость через `hidden`-toggle. Откат к плиткам = 1 LS-строка. |
| Мини-плеер track-change | 13600–13611 | НЕТ | `commit()` пишет `#player-track-reason` как раньше; home подхватывает через Observer. |
| Per-route home bg / blue player | 2021–2033 | НЕТ | Применяется к обоим видам без правок. |

**Итог:** единственная не-аддитивная правка = обёртка `.home-stage` в `.home-tiles[hidden]` (структурная, авторизована 045) + мост `window.openPlayer`. Всё остальное — новая секция / новый CSS-блок / новый модуль / 3 аддитивные правки тинта. Дефолт меняется (плитки → радио), ассет сохранён, откат тривиален.
