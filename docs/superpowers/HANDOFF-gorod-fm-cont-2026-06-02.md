# HANDOFF — Город ФМ (continuation session, 2026-06-02)

**Branch:** master — **ВСЁ ЗАКОММИЧЕНО И ЗАПУШЕНО** (`origin`, HEAD `7520cb2`).
**Read-first order:** этот файл → `docs/superpowers/AUDIT-gorod-fm-screens-and-service.md` (forward-план GOROD-040..057) → `VISION-gorod-fm-ai-driven.md` (продуктовая визия).
**Предшественник:** `HANDOFF-gorod-fm-ai-product.md` (AI-pivot session). **Session log:** `.claude-memory/session_2026_06_02_gorod_fm_resume_cont.md`.

---

## TL;DR

Эта сессия: добил AI-radio до **рабочего wedge на каждой ключевой поверхности** + провёл **Karpathy-tier аудит всего сервиса** и начал его исполнять. North star (из аудита): *«ты видишь свою логику и можешь её поправить — даже реклама твоя»*; доверие = **fidelity** (объяснение = реальный вектор).

**🎯 Где остановились:** P0 quick-wins (5/5) + P1 «Открыть» — done+pushed+visual-QA. Дальше = остаток P1 (часть за Эльбик-gate).

---

## Что построено в этой сессии (master, pushed)

| Commit | Что |
|--------|-----|
| `14d0426` | **Standalone-оптимизация** — build-script downscale+WebP: 71 MB → **2.1 MB** (originals не тронуты). |
| `2c07d3d`+`0ff6cda` | **Resume→music flagship (VISION #7)** — модалка drop/paste/пример → «AI читает» theater → explainable `deriveTaste` → seeds bubbles → handoff. +z-index фикс (была невидима за onboarding z-200). |
| `b3be4db` | **#9 Taste-based sponsor-tile** — нативный explainable steerable ad на `#/taste` («Почему вам» + «Меньше рекламы»). |
| `340882c` | **Karpathy-tier АУДИТ** — 6 параллельных best-practices-агентов + grounded current-state → `AUDIT-...md` (план GOROD-040..057). |
| `783695c` | **P0: «почему»-строка (L1) + «Исправь причину» (L2)** — `TwinrWhy`. Always-on поведенческая причина на плеере; popover с rejectable-атрибутами (reject → strike+persist+wave.bump+ribbon). Категорийно-определяющая механика. |
| `c6f1583` | **P0: цвет-от-обложки + slop-kill (плеер)** — `NowPlayingTint` (self-contained canvas-сэмплер). Now-playing realigned **Слеза/Егор Крид** (реал-обложка). |
| `7520cb2` | **P1: «Открыть» rebuild** — `GorodDiscover`: разговорный поиск (→ explained results) + «Рядом с твоим вкусом» (taste-adjacency). Галерея → «От редакции». |

**VISION 1-9 + UX A-H — все построены.** Аудит — исполняется.

---

## Состояние прототипа (`designs/gorod-fm.html`, single-file)

| Route | Состояние |
|---|---|
| `#/onboarding` | ✅ Пузыри + **резюме→музыка** flagship |
| `#/home` Волна | ✅ AI-хаб. Плеер: реал-обложка + **цвет-от-обложки** + **always-on «почему»** + **«Исправь причину»** + steer. ⬜ Не переделан в 3-зоны (audit §3, 🔒 pixel-perfect gate) |
| `#/taste` Мой вкус | ✅ Редактируемый вектор + волна + **taste-ad** |
| `#/podborki` = Открыть | ✅ **Rebuilt**: разговор + taste-adjacency + «От редакции» |
| `#/library`·`#/favorites`·`#/artist`·`#/track` | ⚠️ Legacy generic + slop (gradient-обложки / силуэт-аватар). Аудит: Медиатека+Избранное → впитать в «Мой вкус»; Артист/Трек → deep-dive (GOROD-047) |

---

## Архитектура (decoupled trailing-script модули — НЕ ломать)

Каждый = свой `window.*` + route/event-hook, не трогает основной IIFE:
- `GorodOnboarding` (пузыри) · **`onResumeDemo`→resume-модалка** (`deriveTaste`, 15 правил)
- `TwinrChat` (чат, scripted intents) · `TwinrWave` (canvas-волна, `.bump()`) · `WaveDials` (steer-popover) · `TwinrRibbon` (between-track лента, budget 4)
- **`TwinrWhy`** (NEW — L2 «Исправь причину» popover; `gorodfm_rejected`) · **`NowPlayingTint`** (NEW — canvas color-from-cover → `--np-accent`) · **`GorodDiscover`** (NEW — «Открыть» разговор+adjacency)
- GorodTaste (#/taste вектор + sponsor `matchSponsor`)

**localStorage:** `gorodfm_taste` (вектор), `gorodfm_rejected` (отвергнутые причины), `gorodfm_ad_less` (меньше рекламы).
**Токены:** Onest, near-black `#0B0C0F` + 1 акцент `#5168FC`; **`--np-accent`** = цвет-от-обложки (JS override). anti-slop.

### Ключевые технические решения этой сессии
1. **Now-playing realigned Believer/Imagine Dragons → Слеза/Егор Крид** — чтобы был РЕАЛ-cover (`home-featured-egor-krid.png`) для цвет-от-обложки + убить gradient-плейсхолдер. Обновлены now-playing-референсы в чате (greet/why/ribbon/backradio); **музыка-тур «Путь к Imagine Dragons» оставлен** как отдельный экскурс.
2. **Color-from-art = self-contained canvas-сэмплер** (НЕ Vibrant.js) → работает и в standalone (data-URI не тейнтит canvas).
3. **«Почему» всегда поведенческая** («ты дослушал 3×»), не маркетинг. Прогрессив: L1 строка → L2 popover (+reject) → L3 чат.

---

## Forward-план (AUDIT §8) — что дальше

### P1 остаток — ДВА вида
- **Safe (без gate, могу делать сразу):** `GOROD-048` transition-card («DJ объявляет следующий + почему») · `GOROD-049` Twinr **edge-glow** (вместо орба) + motion-токены.
- **Нужен Эльбик-gate / realign:**
  - `GOROD-045` **Волна 3-зоны** (audit §3: context-карусель / artwork+ambient-волна / «почему» / Стир) — **🔒 ломает pixel-perfect home, решение Эльбика «насколько ломать».**
  - `GOROD-047` Артист/Трек **deep-dive + slop-kill + «почему тебе»** — нужен realign на реал-ассеты (как сделали плеер) ИЛИ реальные обложки от Эльбика.

### P2 — loops/identity (audit §6)
`GOROD-050` weekly Twinr-recap shareable-карточка 9:16 · `GOROD-051` контекст-старты «Утро/Работа/Вечер» · `GOROD-052` «открытый профиль» demo-экран (питч) · `GOROD-053` стрики «Дней с Волной» + freeze · `GOROD-054` cold-start импорт-seed.

### P3 — backend/бизнес (Ф1+, audit §7)
`GOROD-055` **reason_tag pipeline** (= moat; лог `(track,reason,vector)`) · `GOROD-056` 🔒 лицензии CC→MERLIN→мажоры · `GOROD-057` B2B taste-segment pitch.

---

## 🔒 Эльбик-gate (НЕ Claude)
- `GOROD-029` принять позиционирование (Москва, «музыка которая твоя»).
- `GOROD-030/056` лицензирование (CC→MERLIN→мажоры + IP-юрист — узкое горло №1).
- **IA / pixel-perfect:** насколько ломать legacy pixel-perfect home ради Волна-3-зоны (GOROD-045).
- `GOROD-017` показ инвестору/клиенту (когда готов; standalone `designs/gorod-fm-standalone.html` = 2.3 MB, шерабельно).

---

## Как запустить / демо
```bash
cd ~/Desktop/design-project/designs && python -m http.server 8765
```
- `#/onboarding` → «Заполнить примером» → «Прочитать» → «Собрать радио» (резюме→музыка)
- `#/home` → плеер: реал-обложка + красный (цвет-от-Слеза) прогресс + «почему»-строка; «почему?» → popover → «не моё» (Исправь причину)
- `#/taste` → вектор + волна + спонсор-тайл (scroll вниз)
- `#/podborki` (Открыть) → набери запрос / тапни чип → explained results; «Рядом с твоим вкусом»

**Standalone:** `designs/gorod-fm-standalone.html` (self-contained 2.3 MB, для инвесторов).

---

## Известные нюансы / constraints
- **Visual QA = Chrome MCP** (расширение Эльбика). Капризы: DPR/screenshot-масштаб (1512×807 vs viewport 1745×931 — мини-плеер у нижнего края не влезает в скрин, проверял computed-styles + zoom); вкладки Эльбик закрывает (бери `tabs_context_mcp` заново); сервер :8765 — его. design-implementation-reviewer agent доступен когда расширение подключено.
- **Asset wall:** прототип НЕ имеет per-track обложек (только gradient-плейсхолдеры + несколько реал-фото плиток/featured). → цвет-от-обложки/slop-kill требуют realign на существующий реал-ассет (как плеер) ИЛИ реальные обложки. Это блокирует GOROD-047 до решения.
- **node --check** всех `<script>` блоков = быстрый syntax-гейт (9 блоков). `deriveTaste`/`matchSponsor` юнит-тестируемы в node (чистые функции).
- Standalone собирается `python tools/build_gorod_fm_standalone.py` (downscale+WebP, инлайнит 19 реф. ассетов).

## Carry-over hygiene (Holy Grail)
Onest only · near-black + 1 акцент `#5168FC` (или `--np-accent` от контента) · ≥44px · focus-visible 3px · `prefers-reduced-motion` · **«почему» всегда поведенческая, не маркетинг** · zero console errors (смоук каждый коммит) · atomic commits master-direct · **верифицировать визуально каждый шаг** (Эльбик это ценит) · anti-slop (❌ мульти-стоп градиент-фоны, ❌ orb-аватар, ❌ fake-волна не от FFT, ❌ gradient-плейсхолдеры вместо реал-контента).
