# HANDOFF — Город ФМ (continuation, 2026-06-02 · cont-9)

**Branch:** master — всё закоммичено локально, push отложен до явного `sync` (HEAD `9537540`).

## cont-9 — FULL-DESIGN BUILD: 6/11 шагов DONE (autonomous, по таймеру)
Директива: «чисто дизайн всех экранов + структуры с ресёрчей». Spec-workflow `w7jr5nat0` → 7 per-surface спеков + `docs/superpowers/specs/SPEC-00-foundation-and-integration.md` (build-order). Реализация ПОСЛЕДОВАТЕЛЬНАЯ в main loop (single-file) + Chrome MCP визуал-проверка + атомарные коммиты.
- ✅ **6/11 DONE** (HEAD `9537540`): Foundation `57b5b41` (cyan retire+openPlayer мост) · W6 `3769cc1` (TwinrModel канон, вставлен РАНО) · home-045 `6aff252` (3-зонное радио, Figma→toggle) · taste+saved `5b3b0f6` (Сохранённое+стрик+AT-вектор) · discover-046b `2e7c45a` (карта вкуса+dial+редакция) · track-047a `c62c451` (explainability, оставил view «cover») · standalone `9537540` (2.52MB).
- ⏳ **ОСТАЛОСЬ 5** (спеки готовы, порядок SPEC-00 §5): **artist-047b** (SPEC-artist, REPLACE 3 диапазона top-down, GorodArtist; W6-канон+мост готовы) → **onboarding** (SPEC-onboarding AUGMENT, RK-4 goHome) → **recap+profile finish** (R1-R3/P1, TwinrModel стоит) → **Integrate-A** (redirect library/favorites→taste, retire tabbar Медиа) → **Integrate-B** (ручной cyan-свап + Grep=0).
- **ДИСЦИПЛИНА:** re-grep якоря перед каждым edit (дрейфуют); trailing-IIFE перед `</body>`; демо-лейблы; `?v=N` cache-bust (:8770 жив); PUSH при sync. Детали → `docs/RESUME_PROMPT.md` cont-9.

---

## cont-8 (предыдущий) — блюпринт доведён + de-purple + GOROD-051 + W1

## cont-8 — БЛЮПРИНТ ДОВЕДЁН (ship) + de-purple + GOROD-051 + W1 fidelity-петля
**Резюм cont-7 → исполнение.** Всё верифицировано Chrome MCP (:8770) + 13/13 `node --check` + 0 console errors. 5 атомарных коммитов на master (НЕ запушено).
- ✅ **Блюпринт ДОВЕДЁН** → `docs/superpowers/BLUEPRINT-gorod-fm-full-service.md` (build-ready master, §0–§10). Синтез-workflow: до-исследованы 2 недостающих измерения (IA, legacy) → 9 dims + AUDIT + стратег-доки → синтез → **adversarial completeness-critic (verdict `ship`)** → финал. Критик подтвердил мой код построчно + поймал 4 grounding-ошибки синтеза (search уже есть / resume-import уже built / ложный warmth-claim про #8b5cf6 / ложный CarPlay-guard) → пофикшены, +§10 perf/a11y. **Директива «лучший сервис» ИСПОЛНЕНА.** (Supersedes `BLUEPRINT-research-dimensions-partial.md`.)
- ✅ **de-purple** `5355db8`: #8b5cf6 (wave LAYERS + 8 градиентов) → синяя семья (#8094ff/`--accent-on-dark`). 0 violet.
- ✅ **GOROD-051** `9788ae9`: контекст-старты на #/taste (`GorodContext` + `TwinrWave.setContext`, аддитивно, **НЕ триггерит 045**, honesty-floor suggest-only; + fidelity-фикс: pressed только при applied-today).
- ✅ **W1 fidelity-петля** `18d8816`: GorodTaste читает `gorodfm_rejected` (был live баг — `#/taste` игнорировал, хотя Profile/Recap читают) → совпавшие грани struck+понижены (Егор Крид 62→12%) + карточка «Отклонено в плеере» (все reject'ы видны, matched=accent / reason-only=plain); убран `Math.random@seed` (детерминизм). Замыкает explain→reject→see-in-vector.
- ✅ standalone 2.41 MB `d884221`.
- **Next (блюпринт §7 ВОЛНА-0 остаток, порядок):** GOROD-055-lite reason_tag-эмиттер (is_synthetic) → W2 steering-provenance → DEFAULT_ROUTE 3-фикс → 047a Трек. 🔒 gate: 045/046/047b/029/030. Отложено информированно: legacy cyan (§5, много на legacy-экранах под IA-реорг). **PUSH отложен — всё локально на master.**

---

## cont-7 — ДВА РЕСЁРЧА захвачены (директива «делаем лучший сервис»), блюпринт прерван оператором
Эльбик: «продумай фулл структуру, все страницы, UX/UI ресёрч, архитектуру — Карпати-уровень, лучший сервис» → затем «прерывай что есть, делай передачу».
- ✅ **`SPEC-gorod-051-context-starts.md`** — полный build-ready спек контекст-стартов (модуль `GorodContext` на #/taste + `TwinrWave.setContext`, аддитивно, НЕ триггерит 045, honesty-floor suggest-only, `getHours` дефолт, `gorodfm_context`). **Готов к билду.**
- ⚠️ **`BLUEPRINT-research-dimensions-partial.md`** — 7/9 измерений (workflow `w1lo7vxfi`/`wf_dc2f3a03-be5` прерван ДО синтеза+критика): core-радио · discovery · wedge · habit · AI-архитектура · дизайн-система + 1 тонкий. НЕ дошли ~2 из {IA · legacy-rework · монетизация} — покрыты `AUDIT...§1/§2/§4/§7`. **🐛 находка дизайн-агента:** фиолетовый `#8b5cf6` в `LAYERS` волны (`gorod-fm.html:12927`) нарушает «один акцент» — заменить на синий-оттенок.
- **Next:** (A) доделать блюпринт — перезапустить скрипт `gorod-full-service-blueprint-wf_dc2f3a03-be5.js` ИЛИ синтезировать `BLUEPRINT-gorod-fm-full-service.md` из 7 partial + AUDIT; (B) или сразу строить GOROD-051 по SPEC. Детали → `docs/RESUME_PROMPT.md` cont-7.

---

**Read-first order:** этот файл → `docs/superpowers/AUDIT-gorod-fm-screens-and-service.md` §8 (forward-план GOROD-040..057) → `VISION-gorod-fm-ai-driven.md` (продуктовая визия).
**Предшественник:** `HANDOFF-gorod-fm-ai-product.md` (AI-pivot). **Session log:** `.claude-memory/session_2026_06_02_gorod_fm_resume_cont.md` (содержит cont-2…cont-5).

---

## TL;DR

AI-радио доведено до **рабочего wedge на каждой ключевой поверхности**, Karpathy-аудит сервиса исполняется по приоритетам. North star (из аудита): *«ты видишь свою логику и можешь её поправить — даже реклама твоя»*; доверие = **fidelity** (объяснение = реальный вектор).

**🎯 Где остановились (cont-6):** + **P2 `050` еженедельный Twinr-recap + 9:16 шеринг-карточка** (`#/recap`, `window.GorodRecap`) — done, **2-линзовое review (ship)**, 4 находки пофикшены, **pushed**, standalone пересобран (2.4 MB). Дальше: 045/047 (Эльбик-gate) ИЛИ автономно P2 остаток (**051/053/054** — 050 закрыт).

### cont-6 деталь (`GOROD-050`)
Новый экран `#/recap` = «доказательство роста» прозрачной модели. **HERO = детерминированная слово-идентичность** (`buildIdentity`: top-2 facets → mood×temperature→identity-noun + genitive-grain; heat остывает от реального `tempo`-reject; **NO rng/Date в идентичности** ⇒ одинаковый localStorage = байт-идентичная фраза = fidelity). Genre-**bloom** SVG (`buildPetals`: лепесток-длина=вес, dominant=белый узел + green grow-ring; flat single-hue accent, НЕ градиент). Поведенческие **+/− дельты** (`buildDeltas`: «−» строго из реального `gorodfm_rejected`, пусто ⇒ нет «−»). 1 **открытие** (adjacency-canon по lowest-weight mood). **defense-receipt** в `--accent-on-dark`. НЕ vanity-числа. Вход = бывшая заглушка `#taste-share` → `location.hash='#/recap'`. Honest share = `copySummary` копирует ТЕКСТ (no Web Share API, no PNG render). **Cold-профиль гейт** `hasRealSignal()` (нет picks И нет rejections) → честный empty-state (НЕ FALLBACK-карточка с выдуманным «дослушиваешь до конца»). Данные (`facets`/`FALLBACK`/`REJ_LABELS`) **байт-идентичны GorodProfile** ⇒ views не расходятся. Token-fix: `--success #34d399` промотан из var()-fallback в реальный `:root`-токен. a11y-fix: bloom-svg `aria-hidden` (wrapper несёт `role=img`+aria-label — нет двойного role=img). bloom viewBox расширен (`-85 -8 490 320`) → кириллич-лейблы не клипаются на mobile. **Модули НЕ ломать:** `TwinrTransition`/`GorodProfile`/`GorodRecap` — последние 3 trailing-script IIFE. `#/recap` в `VALID_ROUTES`. НЕ 4-я вкладка (IA: recap ∈ «Мой вкус»).

| Commit | Что (cont-6) |
|--------|-----|
| `77f4fad` | **feat: `GOROD-050` — weekly Twinr-recap + 9:16 share card** (`window.GorodRecap` + `#/recap` + entry-wire). |
| `cecbeaa` | chore: rebuild standalone с GOROD-050 (2.4 MB) + gitignore `.scratch/`. |

**Carry-over TD (app-wide, не блокер):** FALLBACK top-up даёт поведенческий провенанс («усилено: дослушиваешь до конца») и partial-history юзерам (та же про-форма в `GorodProfile` 052). Recap-гейт ловит только полный cold-start; полный фикс = в общей модели профиля (вне scope 050).

---

## Что построено (master, pushed) — арка 2026-06-02

| Commit | Что |
|--------|-----|
| `14d0426` | Standalone-оптимизация (downscale+WebP): 71 MB → 2.1 MB. |
| `2c07d3d`+`0ff6cda` | Resume→music flagship (VISION #7) + z-index фикс. |
| `b3be4db` | #9 Taste-based sponsor-tile (explainable steerable ad на `#/taste`). |
| `340882c` | **Karpathy-tier АУДИТ** (6 агентов) → `AUDIT-...md` (план GOROD-040..057). |
| `783695c` | P0: always-on «почему» (L1) + «Исправь причину» (L2, `TwinrWhy`). |
| `c6f1583` | P0: цвет-от-обложки (`NowPlayingTint`) + slop-kill now-playing→Слеза/Егор Крид. |
| `7520cb2` | P1: «Открыть» rebuild (`GorodDiscover`: разговор + taste-adjacency). |
| `188336e` | **P1 `048` transition-card + `049` edge-glow & motion-токены.** |
| `e8da327` | docs: review-verdict 048/049 (ship-ready 7/7). |
| `d9c4081` | **P2 `052` «Открытый профиль» pitch-экран (`#/profile`).** |
| `c1a14b2` | **Standalone пересобран с 048/049/052 (2.36 MB, инвестор-ready).** |

**VISION 1-9 + UX A-H — все построены.** Аудит исполняется (P0✓, P1 «Открыть»✓ + safe✓, P2 «Открытый профиль»✓).

---

## НОВОЕ в cont-4/cont-5 (детально)

### `048` — between-track transition card (`TwinrTransition`)
«DJ объявляет следующий трек + почему» вместо мёртвого спиннера. Раньше `#btn-next`/`#btn-prev`/`#player-full-next` = no-op — **теперь wired**. На next/prev → центр-карточка (overline «Дальше в эфире»+spark · крупный title · artist · поведенческая «почему» над hairline · «нажмите чтобы перейти сразу») → авто-commit now-playing (мини-плеер title/artist/reason + home hero) → fade ~1.6с; tap/scrim = перейти сразу. **Asset-wall честно:** near-black + ОДИН content-derived `--np-accent` (красный от обложки), НЕ slop-градиент/несоответствующая обложка; cover-картинка остаётся. `FLOW` стартует Любимка·Niletto (канон тёплый-поп), каждое «почему» = реальное поведение.

### `049` — Twinr edge-glow + motion-токены
Убран always-on `ai-pulse` shimmer-ринг лончера (audit §5: орб-с-shimmer = 2023). Заменён на state-driven **краевое свечение** `.is-speaking` (`@keyframes twinr-breathe`/`twinr-breathe-dock`, дыхание `--dur-breathe` 1.6с) на лончере+доке — горит ТОЛЬКО пока Twinr говорит (драйв из `aiSay` typing→message + `TwinrChat.pulse()` для transition-card). Тишина = спокойно. reduced-motion → статичный glow. Motion-токены добавлены **additively** (`--ease-standard/-emphasized/-exit`, `--dur-breathe/-announce`); `--t-fast/mid/slow` НЕ тронуты (0 регрессий).

### `052` — «Открытый профиль» pitch-экран (`GorodProfile`, роут `#/profile`)
Питч-аргумент против «Яндекс делает то же»: показываем то, что конкуренты прячут. Читает live `gorodfm_taste`+`gorodfm_rejected` (fidelity). Контент: **контраст** «чёрный ящик (Яндекс/Spotify — grayscale+blur+lock, мёртвый) vs открытый профиль (alive+accent)» · реальный вектор (5 граней) с **провенансом** по каждой · **1 live-правка** «меньше» → видимая квитанция + `TwinrWave.bump` · секция «Что ты оспорил» (rejected или empty-state→плеер) · «даже реклама — твоя» · moat-caption. Вход с `#/taste` («Открытый профиль →») + прямой URL. НЕ 4-я вкладка (3-tab IA цела). **WCAG-фикс:** токен `--accent-on-dark #8094ff` (~7:1) для мелкого accent-текста (бренд `#5168FC` = 4.25:1 < AA).

---

## Состояние прототипа (`designs/gorod-fm.html`, single-file, 13k строк)

| Route | Состояние |
|---|---|
| `#/onboarding` | ✅ Пузыри + резюме→музыка flagship |
| `#/home` Волна | ✅ AI-хаб. Плеер: реал-обложка + цвет-от-обложки + always-on «почему» + «Исправь причину» + steer + **next/prev → transition-card (048)**. ⬜ Не переделан в 3-зоны (`045`, 🔒 gate) |
| `#/taste` Мой вкус | ✅ Редактируемый вектор + волна + taste-ad + **CTA «Открытый профиль →» (052)** |
| `#/profile` **Открытый профиль** | ✅ **NEW (052)** — pitch-экран: контраст + вектор с провенансом + live-правка + moat |
| `#/podborki` = Открыть | ✅ Rebuilt: разговор + taste-adjacency + «От редакции» |
| `#/library`·`#/favorites`·`#/artist`·`#/track` | ⚠️ Legacy generic + slop. Аудит: Медиатека+Избранное → в «Мой вкус»; Артист/Трек → deep-dive (`047`, 🔒 нужны обложки/realign) |

---

## Архитектура (decoupled trailing-script модули — НЕ ломать)

Каждый = свой `window.*` + route/event-hook, не трогает основной IIFE:
- `GorodOnboarding` (пузыри) · `onResumeDemo`→resume-модалка (`deriveTaste`)
- `TwinrChat` (чат; **+`setSpeaking`/`pulse()` для edge-glow 049**) · `TwinrWave` (`.bump()`) · `WaveDials` (steer) · `TwinrRibbon` (between-track лента, budget 4)
- `TwinrWhy` (L2 «Исправь причину»; `gorodfm_rejected`) · `NowPlayingTint` (canvas color→`--np-accent`) · `GorodDiscover` («Открыть»)
- `GorodTaste` (#/taste вектор + `matchSponsor`)
- **`TwinrTransition` (NEW 048** — between-track card; wires next/prev; `FLOW` playlist; commit now-playing**)**
- **`GorodProfile` (NEW 052** — `#/profile`; reads `gorodfm_taste`+`gorodfm_rejected`; provenance + live-правка**)**

**localStorage:** `gorodfm_taste` (вектор) · `gorodfm_rejected` (отвергнутые причины: ids `artist`/`vocal`/`tempo`) · `gorodfm_ad_less`.
**Токены:** Onest · near-black `#0B0C0F` + 1 акцент `#5168FC`; `--np-accent` (цвет-от-обложки) · **`--accent-on-dark #8094ff`** (мелкий accent-текст на тёмном, AA) · motion: `--t-fast/mid/slow` + `--ease-standard/-emphasized/-exit` + `--dur-breathe/-announce`.
**Edge-glow keyframes:** `twinr-breathe` (лончер ::after opacity) · `twinr-breathe-dock` (док box-shadow). Старый `ai-pulse` УДАЛЁН.

---

## Forward-план (AUDIT §8) — что дальше

### 🔒 Эльбик-gate / realign (НЕ Claude — нужен ввод)
- `GOROD-045` **Волна 3-зоны** (audit §3: context-карусель / artwork+ambient-волна / «почему» / Стир) — **ломает pixel-perfect home, решение Эльбика «насколько ломать».**
- `GOROD-047` **Артист/Трек deep-dive + slop-kill + «почему тебе»** — нужен realign на реал-ассеты (как плеер) ИЛИ реальные обложки от Эльбика. **Asset-wall:** прототип без per-track обложек.

### 🟢 Можно брать автономно (P2 loops остаток, audit §6)
- `GOROD-050` weekly Twinr-recap shareable-карточка 9:16 · `GOROD-051` контекст-старты «Утро/Работа/Вечер» · `GOROD-053` стрики «Дней с Волной» + freeze · `GOROD-054` cold-start импорт-seed.
- (`052` «открытый профиль» уже сделан.)

### P3 — backend/бизнес (Ф1+)
`GOROD-055` reason_tag pipeline (= moat) · `GOROD-056` 🔒 лицензии CC→MERLIN→мажоры · `GOROD-057` B2B taste-segment pitch.

### Backlog TD
- `TD-GOROD-CTA-AA` — primary-кнопка white-on-`#5168FC` = **4.43:1** (чуть <AA 4.5, 14px/700). Конвенция ВСЕХ кнопок (не введено в 052). Reviewer: accept-not-block. App-wide фикс: фон `#4A5FE8` (→~5.1:1) ИЛИ текст ≥18.66px.

---

## Как запустить / демо
```bash
cd ~/Desktop/design-project/designs && python -m http.server 8765
```
- `#/onboarding` → «Заполнить примером» → «Прочитать» → «Собрать радио» (резюме→музыка)
- `#/home` → плеер: реал-обложка + «почему» + «не моё»; **жми next (⏭) → transition-card «Дальше в эфире: Любимка…»** → now-playing меняется
- открой Twinr-чат (✦ лончер) → **док «дышит» синим пока печатает** (edge-glow), спокоен в тишине
- `#/taste` → вектор + волна + спонсор-тайл + **«Открытый профиль →»**
- `#/profile` → **контраст чёрный-ящик-vs-открытый** + вектор с провенансом + жми «меньше» → квитанция
- `#/podborki` (Открыть) → запрос/чип → explained results

**Standalone:** `designs/gorod-fm-standalone.html` (self-contained 2.36 MB, для инвесторов; содержит 048/049/052).

---

## Известные нюансы / constraints
- **Visual QA = Chrome MCP** (расширение Эльбика; сервер `:8765` — его). Капризы: скрин-масштаб (док/мини-плеер у краёв клипятся в скрине — проверять computed-styles/JS-probe); window-resize в расширении НЕ ужимает CSS-viewport (mobile проверять через `@media`/matchMedia/`data-surface='mobile'`). Tweaks-панель может перекрывать правый край при скрине — это её открытое состояние, не баг.
- **`node --check` всех `<script>` блоков** = быстрый syntax-гейт (**11 блоков** сейчас). Хелпер: `.scratch/check_scripts.py` (gitignored).
- **Asset wall:** прототип без per-track обложек → 048 transition использует `--np-accent` (не fake-обложку); `047` блокирован до обложек/realign.
- **`#/home` `#home-track-title`** может быть null на текущем home-варианте → 048 commit обновляет его guarded-но-op (мини-плеер = основная now-playing поверхность, обновляется корректно). Не баг.
- Standalone собирается `python tools/build_gorod_fm_standalone.py` (downscale+WebP).
- Remote origin = `github.com/elbicsabitov/timiryazeva79-poster.git` (так называется git-remote этого репо).

## Carry-over hygiene (Holy Grail)
Onest only · near-black + 1 акцент `#5168FC` (или `--np-accent` от контента; мелкий accent-текст на тёмном → `--accent-on-dark`) · ≥44px · focus-visible 3px · `prefers-reduced-motion` · **«почему» всегда поведенческая, не маркетинг** · zero console errors (смоук каждый коммит) · **node --check 11 блоков** · atomic commits master-direct · **верифицировать визуально каждый шаг + design-implementation-reviewer (hard-gate для новых экранов)** · anti-slop (❌ мульти-стоп градиент-фоны, ❌ orb-аватар, ❌ fake-волна, ❌ gradient-плейсхолдеры вместо реал-контента, ❌ эмодзи-как-иконки).
