# HANDOFF — Город ФМ AI-product (передача в след. сессию)

**Создано:** 2026-06-02 (effort max). **Branch:** master — **ВСЁ ЗАКОММИЧЕНО И ЗАПУШЕНО** на `origin` (`github.com/elbicsabitov/timiryazeva79-poster`), HEAD `d4479a3`.
**Предшественники:** `HANDOFF-gorod-fm-v2-pixel-perfect.md` (v2 Figma), `VISION-gorod-fm-ai-driven.md`, `ARCHITECTURE-gorod-fm-nextgen.md`, `UX-DIRECTION-gorod-fm.md`, `UI-AUDIT-gorod-fm.md`.

---

## TL;DR (прочитать первым)

Город ФМ из «pixel-perfect радио-сайта» развернулся в **AI-музыкальную платформу** (визия Эльбика 27.05, которую прошлая сессия потеряла). За эту сессию построен весь AI-product слой + 10 Karpathy-ресёрч-брифов + 4 синтез-дока. Прототип = `designs/gorod-fm.html` (single-file SPA). Демо локально работает.

**🎯 Рынок = МОСКВА** (не Казахстан — Эльбик уточнил). Следствие: локальность-как-moat исчезает (домашка Яндекса), wedge = **прозрачность + редактируемый вкус + объяснимость**.

---

## Что построено (всё на master + pushed)

| Маршрут / фича | Что | Commit |
|---|---|---|
| `#/home` Главная v2 | pixel-perfect Figma 2174:422, чёрная | `afd072a` |
| `#/onboarding` | пузыри Apple-Music: тап→рекурсивный genre-coherent bloom безлимит, full-bleed, safe-zone | `6c8e802`·`ef483a4` |
| Twinr AI чат | collapsible dock, живой профиль, explainable/steerable/tours/ads | `38d334a` |
| Native AI в плеере | «✨ почему?» pill + steer-кнопка (→ диалы) | `8ec5e4a` |
| `#/taste` «Мой вкус» | живая canvas-волна + редактируемый вкус-вектор (Жанры/Настроения/Артисты/Эпохи, ±/pin) | `a745802` |
| 3-tab IA | сайдбар → Волна / Мой вкус / Открыть | `4ecb562` |
| Wave-диалы | Настроение/Занятие/Характер из плеера → 1 вектор | `4ecb562` |
| Tech-modern restyle | нейтрал near-black фон `#0B0C0F` + 1 акцент `#5168FC` (anti-slop) | `fa5ed45` |
| Between-track лента | ambient «now→next» нарратив, budget 4/сессию | `92f8079` |
| Audio-reactive волна | opt-in «Озвучить волну» → WebAudio pad → AnalyserNode → волна реагирует на FFT | `92f8079` |

---

## Архитектура прототипа (НЕ сломать)

`designs/gorod-fm.html` — один файл. Основное приложение = большой IIFE (routing `activatePage`/`hashchange`, `VALID_ROUTES`, плеер, tweaks). **AI-слой = отдельные decoupled trailing `<script>` IIFE** в конце `<body>`, каждый со своим `window.*` API и своим hashchange-хуком — НЕ трогают основной IIFE:
- `window.GorodOnboarding {start,stop}` — физика пузырей (rAF), route-gated на `#/onboarding`.
- `window.TwinrChat {open,greetFromOnboarding,ask}` — чат-док (scripted intents: why/different/more/tour/ads).
- `window.TwinrWave {start,stop,bump}` + audio (`initAudio`/`startAudio`/`stopAudio`/`toggleSonify`) — canvas-волна на `#/taste`, `bump()` пульс на стир.
- `window.WaveDials {open,close}` — lazy steering popover, пишет в `sel` вектор.
- `window.TwinrRibbon {show,hide}` — between-track лента, budget=4.
- Связки: онбординг «Продолжить» → `TwinrChat.greetFromOnboarding(picks)`; плеер «почему?» → `TwinrChat.ask('why')`; плеер steer → `WaveDials.open()`; диалы apply → `TwinrWave.bump()` + `TwinrRibbon.show()`; «Мой вкус» правки → `TwinrWave.bump()`.
- Вкус из онбординга сохраняется в `localStorage['gorodfm_taste']`, читается чатом и «Мой вкус».
- CSS: `@layer reset/tokens/base/layout/components/surfaces/utilities`. Токен `--bg-base` = нейтрал near-black (рестайл). `--brand-blue-light #5168FC` = единственный акцент.
- Все маршруты: `['#/map','#/home','#/lives','#/podborki','#/library','#/artist','#/track','#/favorites','#/onboarding','#/taste']`. `#/map` = internal flow-map (footer), может редиректить на home при hide-flow-map tweak.

---

## Стратегия (из ресёрча, для разговора с Эльбиком)

- **Позиционирование:** НЕ «первый AI-стриминг» (уже неправда — Spotify AI DJ + Yandex «Моя волна»). → **«музыка, которая твоя — видишь/правишь вкус, знаешь почему играет каждый трек.»** Wedge = видимый редактируемый **Twinr-профиль** + AI-экскурсы + объяснимость.
- **Рынок:** Москва/Россия. Конкуренция head-on с Яндексом на его поле → дифференциация резкая и видимая (прозрачность). Без KZ-локальности/орнамента.
- **Узкое горло №1 = ЛИЦЕНЗИРОВАНИЕ.** Нельзя стримить мажор-каталог без прав. Путь: 7digital MaaS (реальный) + Spotify Web Playback SDK (демо/инвесторам) + свой CC/инди seed. Начинать переговоры + IP-юриста НЕМЕДЛЕННО, параллельно билду.
- Технологии (детали в `ARCHITECTURE-gorod-fm-nextgen.md`): CLAP-вектор · BaRT explore-exploit-explain бандит · multi-vector Twinr (slow EMA + SASRec session) · CTRL-Rec стиринг <50ms · retrieval-first/LLM-last объяснения + NLI gate · Yandex Yambda bootstrap · pgvector→Qdrant.

---

## 🔒 Решения Эльбика (gate — НЕ Claude'у)

1. **GOROD-029** — принять разворот позиционирования (Москва, «музыка которая твоя», не «первый AI»). Юр-риск ложного «первый».
2. **GOROD-030** — лицензирование: старт 7digital/Spotify-SDK + найм KZ/RU IP-юриста.
3. **GOROD-017** (v1) — показ клиенту/инвестору (когда готов).

---

## Следующая сессия — опции (выбрать с Эльбиком)

- **A) Добить v2 Figma-экраны (GOROD-021):** Медиатека `2385:2924`, Раздел Избранное `2535:11151`, Страница артиста `2537:14090`. Re-fetch Figma contexts (URLs протухают 7д), assets уже скачаны в `designs/assets/gorod-fm/`. Под нейтрал-рестайл.
- **B) Standalone для инвесторов (GOROD-032):** `tools/build_gorod_fm_standalone.py` инлайнит 87 assets base64. Скрипт предшествует новым роутам/скриптам — проверить что инлайнит всё; пересобрать. Даёт самодостаточный файл для шеринга без сервера.
- **C) Полировка стиля (UI-AUDIT рекомендации):** унификация акцента (focus-ring `--brand-cyan`→`#5168FC`), ретема Warm/Light под нейтраль, тонкая волна за мини-плеером, Apple-style микро-моушн на смене трека.
- **D) Дальше AI-product:** реальный бэкенд (по ARCHITECTURE) — но это Ф1+, не прототип.

**Рекомендация:** сначала B (standalone — чтобы Эльбик мог показывать), потом A (полнота экранов) или C (лоск).

---

## Демо (как запустить)

```bash
cd ~/Desktop/design-project/designs
python -m http.server 8765        # сервер
```
Открыть: `http://127.0.0.1:8765/gorod-fm.html#/onboarding` (пузыри) · `#/home` (плеер: «✨ почему?», steer→диалы; ждать ~5с — всплывёт between-track лента) · `#/taste` (живая волна + «Мой вкус» + «Озвучить волну») · сайдбар = Волна/Мой вкус/Открыть.

---

## Carry-over hygiene (Holy Grail — не ломать)

Onest only (no Inter/Roboto/slop) · хит-таргеты ≥44px · focus-visible 3px · `prefers-reduced-motion` (волна/пузыри/лента это уважают) · zero console errors (смоук: 8/8 routes ✓, все модули живы) · atomic commits master-direct · anti-slop gate (нейтрал near-black + 1 акцент `#5168FC` + цвет от контента; ❌ multi-stop градиент-фоны, ❌ декор-glow, ❌ orb-аватар, ❌ >1 акцент).

## Известные нюансы
- Tweaks-панель мигает открытой при загрузке (init-flash, авто-скрывается) — это transient в скриншотах, не баг.
- Audio-pad в «Озвучить волну» = demo (нет реального каталога); AnalyserNode готов под реальный стрим в проде.
- `localStorage['gorodfm_taste']` может накопить много пиков от тестов → «Мой вкус» капит 8 пиков / 6 строк на группу.
