# DEBT — Дизайн-долг

> **Status legend** (added 2026-05-27 evening): `done` = работа выполнена. `🔒 Эльбик-gate` = всё что в нашей власти сделано, дальше ждём внешнего ввода (показ клиенту, ответы, реквизиты, выбор направления, утверждение, реализация после approval). `pending` (без замка) = ещё в работе или ждёт следующей сессии. Цель: ноль настоящих `pending` на Claude'е.

## ⚡ Monte Carlo (РМГ) — промо-блок на главной montecarlo.ru (2026-06-10 вечер)

НОВЫЙ клиентский трек: Figma `Monte-Carlo` (`l38kZVrZXzdNlBIIOLFX4g`), чат «DFM» (Stas Skalaban, Alexei Shelest). Вся работа в клиентской фигме, в репо только session log + `.scratch/dfm/` (gitignored). Полная история: `.claude-memory/session_2026_06_10_montecarlo_promo.md` + shared memory `project_design_montecarlo_rmg.md`.

| ID | Задача | Статус |
|----|--------|--------|
| MC-001 | Промо-блок 3×16:9 из реальных баннеров montecarlo.ru/news — 8 итераций размещения по фидбеку чата | done (фреймы в клиентской фигме) |
| MC-002 | Футер 1:1 с прода: 6 векторных лого холдинга + ссылки + © + 12+ + бейджи сторов + стекло-плашка (live-токены из их CSS) | done (внутри фреймов «полная страница» `4096:1820`/`4099:1878`) |
| MC-003 | Карпати-ресёрч размещения (4 агента: плеер-интерфейсы / anchored+ротация / luxury / fixed-viewport) → 7 концептов построено | done |
| MC-004 | Жизненный цикл промо-дока: язычок `4106:1729` ↔ peek 90px `4105:1700` ↔ развёрнут `4126:1932`; ротатор `4106:1918` (фаворит); luxury-ряд `4114:1787`; орнамент `4115:1816`; в плеер: этаж `4122:1845` / хвост `4123:1874` / companion `4123:2064` | done |
| MC-005 | Выбор концепта клиентом + ответ в чат DFM + удаление непринятых фреймов | 🔒 Эльбик-gate |
| MC-006 | Маркировка платных баннеров (Пионер): «Реклама» + erid через ОРД | 🔒 Эльбик-gate (юр.) |
| MC-007 | P5 companion-угол: уточнить у Алексея, не претендует ли Яндекс-слот на угол под новостями | 🔒 Эльбик-gate |
| TD-MC-01 | Мобильная главная с промо — не просили; всплывёт при имплементации | backlog |
| TD-MC-02 | Node-ids в клиентской фигме протухают при перестройке канваса клиентом — перед reuse инвентаризация (см. session log «Грабли») | note |

## ⚡ Twinr — чат-раздел: редизайн под fit-in-viewport (правки Татьяны, 2026-06-17)

Бриф = чат Татьяны 06-17 (3 скрина прода `.scratch/ktv/msg_592182.jpg` топбар / `msg_592193.jpg` плашка-✕ + «Новый чат» / `msg_592194.jpg` меню) + Эльбик «да, думаю норм» на удаление топбара. Karpathy-ресёрч (3 агента → синтез → adversarial-критик «ship-with-fixes», `.scratch/wf_twinr_chat_research.js`). Всё в `designs/twinr-liquid-glass.html`, Chrome-MCP verified (0 console err). Session log `.claude-memory/session_2026_06_17_twinr_chat_redesign.md`.

| ID | Задача | Статус |
|----|--------|--------|
| KTV-016 | Глобальный топбар удалён ради верт. места (Эльбик одобрил); аккаунт+колокольчик → `.sidebar-footer` (collapsed=аватар, hover-reveal; `.nav` scroll-on-hover чтобы подвал не обрезался при низком вьюпорте); крошки убраны | done |
| KTV-017 | ⌘K-поиск был нерабочей бутафорией (нет keydown-listener, span декоративный) — убран вместе с топбаром (не регрессия); реальную command-palette строить отдельно если попросят | done |
| KTV-018 | Чат промоутнут в отдельный nav-item «Чат» (после Статистики, data-route="chat"); убран из AI_TOOLS + routeToNav['page-chat']→'chat'. **Декапл ДО удаления плашки** — иначе injectAiSubnav (fallback firstElementChild) инжектит ИИ-чипы в чат-сетку | done |
| KTV-019 | Плашка `.section-hero` «Чат» удалена (✕ Татьяны) + слово «Чат» снято; `sr-only <h1>` + routeToTitle сохранены для a11y/document.title; CSS-правило `.section-hero` НЕ трогал (используют 10+ др. страниц) | done |
| KTV-020 | «Новый чат» под спойлер (button[aria-expanded]+region, grid-rows 1fr↔0fr анимация + prefers-reduced-motion); кнопка-триггер всегда видна (старт в 1 клик), форма свёрнута по умолч., раскрыта на пустом состоянии | done |
| KTV-021 | Чат влезает в экран целиком: `#page-chat.active` = сетка `calc(100dvh - var(--chat-vpad,48px))`; скроллятся только `.chat-history`+`.chat-stream`; композер закреплён снизу (flex:none); min-height/min-width:0 на всех flex/grid-детях; `html:has(#page-chat.active){overflow:hidden}` гасит фантом-скролл смонтированных страниц (LG-008); `.chat-stream p{max-width:820px}` для читабельности | done |
| KTV-022 | Вкладки Личные/Общие через существующий `.tabs[data-tabs-group]`/`[data-panel]` handler (zero new JS); вертикальная история с бейджами модели; тред-бар (имя+чип модели, default Deepseek как в старом select); композер (textarea авто-рост + Отправить) | done |
| KTV-023 | Standalone пересобран (`tools/build_twinr_crm_standalone.py`, 1.70 MB) → zip `deliverables/2026-06-17/` отправлен Татьяне (файл без подписи, команда Эльбика) | done |
| TD-KTV-05 | Мобайл-бургер (≤920px плавающая `.nav-burger-float`, тот же #navBurger + drawer-JS) — логика проверена, чистый моб-скрин не снят (тест-окружение DPR 1.65 ломало ресайз); проверить на реальном узком экране | backlog |
| TD-KTV-06 | Мёртвый CSS от удалённого топбара (`.topbar`/`.crumbs`/`.search`/`.search-key` в @media-блоках) оставлен — безвреден (нет элементов), вычистить при случае | backlog |

## ⚡ Twinr — «Хранилище»: отдельный раздел + MD-конвертер (2026-06-11)

Бриф = чат Татьяны 11.06 15:05–15:13 (текст + 2 скрина прода) + команда Эльбика «вынеси в отдельную вкладку». Их прод: бывш. «ИИ — Документы» переделан в самостоятельный раздел «Хранилище» (upload-карточка «Файл не выбран»/«Название (опционально)»/«Загрузить»/«Максимальный размер: 20 МБ» + таблица Название/Размер/Загружено/Теги, per-row «Изменить теги»+«Удалить», без чекбоксов/пагинации). ТЗ конвертера (msg 590107): «конвертор-преобразователь md. После преобразования пусть пользователь сам выбирает — сохранить md файл в хранилище или отправить в раздел Документы в один из своих проектов (выпадающий список — выбрать проект)». Скрины: `.scratch/ktv/msg_590113.jpg` (пустое) + `msg_590130.jpg` (наполненное). Их прод-кнопка «Изменить теги» у них «поломалась» (msg 590131) — наша модалка тегов как референс осталась.

| ID | Задача | Статус |
|----|--------|--------|
| KTV-010 | Twinr: перестройка `#page-docs` под прод-структуру «Хранилище» — upload-карточка (file-picker со скрепкой + live-имя файла, название, «Загрузить», лимит 20 МБ) + таблица с её скринов 1:1 (Документ.pdf 281,8 КБ / 14 АГ Фест mp3 / Картиночка.png + docx-демо «Сценарий ролика_АГ»), coral-ссылки имён, сорт-стрелки (Загружено ↓ active), per-row «Изменить теги» (coral-soft, → modal-tag-select) + «Удалить»; rename Документы→Хранилище (sh-title, routeToTitle, гайд g-docs + TOC) | done |
| KTV-011 | Twinr: «Хранилище» вынесено из ИИ-сабнава в **отдельную вкладку сайдбара** (nav-item data-route="storage", archive-иконка, между ИИ и Руководством; убран из AI_TOOLS → чипы/aiToolHub/crumb «Twinr / Хранилище» подстроились сами; guard twinr-last-ai-tool не ломается) — как у них на проде | done |
| KTV-012 | Twinr: **MD-конвертер** — per-row кнопка «В Markdown» (только PDF/DOCX; mp3/png без неё) → модалка `modal-md-convert`: бейджи PDF→MD + имя .md, «Преобразовать» (спиннер .btn-spinner 0.9с) → mint-плашка «Готово» + «Куда сохранить результат?»: карточки «В хранилище» / «В проект» (aria-pressed, coral-выделение) + дропдаун проектов (Аудио Метрика / Большой Цифровой / CRM Турбо); «Сохранить в хранилище» → строка `.md` первой в таблице (размер ~5%/33% от исходника, тег MD, mint-флеш) / «Отправить в проект» → подтверждение «Отправлено: …» + автозакрытие. Chrome-MCP verified: desktop 1440 / mobile 390 (стек, стрелка ↓) / обе ветки / console 0 err | done |
| KTV-013 | Отправка Татьяне ВЫПОЛНЕНА: zip `deliverables/2026-06-11/twinr-updates-2026-06-11.zip` (standalone с фиксом KTV-014 + twinr-brand/ + twinr-icons/) — **msg 590167**, файлом без подписи, через СЕРВЕРНУЮ telethon-сессию `/opt/mama-helper` (локальная была занята JRE-аплоадом) | done |
| KTV-014 | Фикс по ревью Эльбика («как открыть в этом флоу загрузку в md, чет не открывается» → «пофикси прежде чем ей скидывать»): **«Загрузить» был мёртвый** — теперь живой флоу загрузка→конвертация: выбранный файл добавляется строкой (имя из пикера или «Название»+авторасширение, реальный размер, дата; PDF/DOC/DOCX получают «В Markdown»), валидация >20 МБ и «сначала выберите файл» инлайн в caption (coral), форма сбрасывается; **.md теперь открывается**: имя-ссылка + кнопка «Скачать» = настоящий data:text/markdown download (демо-контент). Real-click verified в standalone (upload→convert→save→download, console 0 err). Урок: same-URL navigate в Chrome MCP = no-op hash-nav, после ребилда standalone нужен `reload ignoreCache` | done |
| KTV-015 | Фидбек Татьяны 16:20 («надо чтобы без загрузки в хранилище, а вот результат уже в хранилище или в один из проектов»): добавлена карточка **«Преобразовать в Markdown»** — файл берётся прямо с компьютера (accept .pdf/.doc/.docx), исходник в хранилище НЕ сохраняется, по кнопке модалка открывается с автостартом конвертации → выбор назначения как раньше; валидация типа/20 МБ инлайн; per-row «В Markdown» оставлен для уже загруженных файлов; общий вход отрефакторен в `mdcOpenWith(name, sizeKb, autostart)`; гайд обновлён. Verified в standalone: docx→хранилище (исходник в таблицу НЕ попал) · mp3 отбит · pdf→«CRM Турбо» confirm+автозакрытие · per-row жив · console 0. **Отправлено ей msg 590213** (файлом без подписи, локальная сессия) | done |
| TD-KTV-04 | twinr: модалки в dawn-теме — тёмная панель + тёмный текст (low contrast); pre-existing у ВСЕХ модалок (проверено на modal-tag-select), не регрессия конвертера; прод Татьяны на тёмной теме → не блокер | backlog |

## ⚡ Twinr + CRM Турбо — клиентские правки Татьяны @k_t_v_23 (2026-06-10)

Бриф = скрины в её TG-чате 08–09.06 (всё, что после `twinr-icons.zip`). **Два проекта, НЕ путать:** Twinr = `designs/twinr-liquid-glass.html` (их прод живёт на нашем Liquid Glass), CRM Турбо = `designs/crm-glass.html`. Коммиты `698dade` / `54a2eee` / `8e0df6f`; design-implementation-reviewer пройден (1 HIGH + 3 MED → все закрыты, re-verified). Пакеты для Татьяны: `deliverables/2026-06-10/twinr-updates-2026-06-10.zip` + `crm-updates-2026-06-10.zip` (gitignored). Она деплоится 10.06 — Эльбик обещал прислать до конца дня.

| ID | Задача | Статус |
|----|--------|--------|
| KTV-001 | Twinr: 2 иконки «копировать»/«удалить» → `twinr-icons.zip` | done (отправлен 08.06, до сессии) |
| KTV-002 | Twinr: **моб-адаптив** всех 23 страниц (приоритет №1) — off-canvas sidebar+бургер+скрим, компакт-топбар, сетки в 1 кол (вкл. inline-grids через minmax(0,1fr)), таблицы скроллятся в картах, модалка-шит, тач-таргеты ≥40px, LG-008 phantom-scroll пофикшен | done (`698dade`+`8e0df6f`) |
| KTV-003 | Twinr: фавиконка + лого сайдбар-плитки (twin-panes на coral→amber; Twinr = «AI based teams collaboration platform») + `assets/twinr-brand/` svg+png | done (`698dade`) |
| KTV-004 | ~~CRM~~ **TWINR** (перенос 10.06 вечером — Эльбик поправил мою ошибку проекта: плитка «CRM Glass» на скрине = их переиспользованный шелл): раздел **«Аудио Метрика»** — nav-пункт (eq-bars), отчёт `#page-audio-metrics` (станция dfm-afrovibes.microit + период + 5 фильтров + «Сформировать отчёт» + таблица 15с/60с с группированным thead, данные 1:1 со скринов) + `#page-audio-track` «Выходы трека в эфир» (клик по строке); nav-пункт СЛЕДОМ ЗА «Статистика» | done (`54a2eee`→перенос `b4adcc6`) |
| KTV-005 | CRM: кебаб ресурса «Создание ~~материала~~»→«Создание», «~~Дублировать~~»→«Медиа» (3 вхождения) | done (`54a2eee`) |
| KTV-006 | CRM: подложка «как на Твинере» — УЖЕ в прототипе (тот же sunset на всех экранах, видна на Ресурсах); их вёрстка фон не взяла → просто забрать из standalone | done (подтверждено скринами) |
| KTV-007 | Иконки для их nav: `audio-metrika` + `sluzhebnye-tg` (svg+png 512, стиль twinr-icons: lucide stroke-2 тёмный глиф) в `assets/twinr-icons/` (перенесено из crm-icons — иконки для их twinr-nav) | done (`54a2eee`+`b4adcc6`) |
| KTV-008 | Отправка Татьяне ВЫПОЛНЕНА (всё файлами без подписи, команды Эльбика): twinr-zip v1 14:42 (msg 589650, устаревший) → **CRM-zip 15:01 (msg 589661)** → **twinr-zip v2 15:05 (msg 589663 — актуальный: +Аудио Метрика, +twinr-icons/, моб-адаптив, Wordstat-графики, favicon/лого)** | done |
| KTV-009 | Twinr: **Wordstat «Графики»** — её коммент 10.06 13:36 («Графики Вордстат очень выбиваются из стиля», dev.twinr.ru/cms/wordstat/…/graphs; Эльбик 🫡): placeholder `#page-wordstat` → дизайн вкладки «Графики» анализа «Активный гражданин»: 3 glass-карточки (по дням / по неделям / по месяцам), coral-бары + amber-пик, подписи с пиками, табы Данные(disabled)/Графики, responsive SVG (ок на 375) | done |
| TD-KTV-01 | twinr: file-wide a11y — 37 полей без label/id (pre-existing, reviewer LOW) | backlog |
| TD-KTV-02 | crm: sticky thead латентно не работает внутри `.t-wrap` скроллера (все таблицы CRM; всплывёт на длинных отчётах) | backlog |
| TD-KTV-03 | push master — выполнен при sync 10.06 (12 коммитов) | done |

## ⚡ Город ФМ — v1 SHIPPED · v2 в работе · AI-product pivot + Karpathy research (2026-06-02)

**Update 2026-06-03 (cont-16) — light deferred-sweep ANALYSIS done, build PAUSED, then SYNCED+PUSHED:** Эльбик: «как агенты дойдут — пауза без потерь». 6-агентный read-only аудит light-theme дыр на ВСЕХ вторичных роутах (workflow `woi5kyh7a`, 537k токенов) → **build-ready override-спек** в `docs/superpowers/HANDOFF-gorod-fm-cont-16.md` + verbatim raw `docs/superpowers/cont-16-light-sweep-analysis.json`. **`gorod-fm.html` НЕ тронут** (билд отложен на след. сессию — execute Step 0 seam + Step 1 override-блоки). Находки: (a) **#/podborki gallery = DEAD CODE** (live=«Открыть» discover-surface, почти весь пропатчен); (b) **#/artist latent-баг** track-cover inline `var(--surface-1)`=бел-на-бел в light → фикс inline на `var(--brand-blue-light)`; (c) #/profile closed-box остаётся тёмным (cont-15 «faux→ink» = ложь, правила нет); (d) #/recap карточка остаётся тёмной (WYSIWYG с PNG O3); (e) seam = удалить `--cover-mix-base` из dark `:root` L179 + wire 12 сайтов на `var(--cover-mix-base,#orig)` (dark byte-identical). 🟡 1 решение Эльбика: chrome strategy light-glass (дефолт) vs dark-rail. **TD-GFM-LIGHT-SWEEP** = pending (next session). Этот sync запушил cont-12→16.

**Update 2026-06-03 (cont-14/15) — `done` LOCAL, PUSH HELD:** «доделай все долги». #/taste «Облако вкуса» weight-cloud (`09704df`) · light theme v1 Apple-grade additive dev-gated, dark byte-identical (`36a688e`) · ЛК account-sheet thin/demo (`ca20b28`) · 4-lens review fixes (`b2bb18f`) · standalone regen 3.07 MB (`8199bed`). «Сохранённое»+#/artist verified already-shipped. Full handoff: `docs/superpowers/HANDOFF-gorod-fm-cont-15.md`. **DEFERRED (honest):** (1) light per-surface sweep on secondary routes #/track/#/profile/#/recap/#/artist/podborki-gallery/#/lives (~1 session; wire `--cover-mix-base` seam); (2) standalone GorodTasteSeed-aware photo inline (~38 runtime-concat refs → offline flat-fallback); (3) #/artist real content = Ф1+ needs-assets; (4) light FOUC/PNG-light = O7-public only. **PUSH all 6 commits at `sync`.**

**Update 2026-06-03 (cont-11) — `done`, PUSHED:** Мини-плеер (нижний бар) переделан research-first (PRIORITY #1) + play/pause fidelity-баг исправлен + **весь AUDIT-apple-polish backlog закрыт** (G2 cyan→0 · G7 focus/active/44px · G6 anti-slop · DEFAULT_ROUTE cold-start · 8 per-surface волн) + **плеер locked calm-blue** (Variant A: color-from-art glows retired, §0.5). standalone пересобран. ~15 атомар-коммитов, node --check 0, 0 console errors на 8 роутах. Детали: `docs/superpowers/HANDOFF-gorod-fm-cont-11.md` + `docs/RESUME_PROMPT.md` cont-11. Грунт-инвентарь: `docs/superpowers/REMAINING-cont11-debt-plan.md`. Информированно отложено (low-value/risk): scaleX бренд-вордмарк + dead labels · chrome sidebar-geometry/tabbar-indicator · recap glyph→SVG · render-identical токенизации.

**Update 2026-06-02:** Эльбик дал большую продуктовую визию (AI-driven music streaming) → pivot за пределы pixel-perfect. Сделано: Главная v2 закоммичена (была uncommitted после краша прошлой сессии), **онбординг-пузыри Apple-Music-style** (`#/onboarding`), **Twinr AI чат** (explainable+steerable+живой профиль), **native AI в плеере** («почему?» + steer). + **10 Karpathy-ресёрч брифов** (`docs/research/gorod-fm/01-10`) → **3 синтез-дока** (`ARCHITECTURE-gorod-fm-nextgen.md`, `UX-DIRECTION-gorod-fm.md`, `VISION-gorod-fm-ai-driven.md`). 🔑 Ресёрч-вывод: «первый AI» уже неправда (Spotify/Yandex), разворот на «музыка, которая твоя: видишь/правишь вкус, знаешь почему» + KZ/СНГ локальность; узкое горло = лицензирование.

**Update 2026-05-27 night:** v2 pixel-perfect rebuild from 5 newly-discovered Figma nodes (GOROD-021). Full handoff: `docs/superpowers/HANDOFF-gorod-fm-v2-pixel-perfect.md`. v1 base shipped at HEAD `77ee5c1`.

Новый клиент — онлайн-радио платформа. `designs/gorod-fm.html` (10258 lines) + `designs/gorod-fm-standalone.html` shipped via 13 atomic commits on master. 7 маршрутов, Player overlay, Tweaks (cinema/warm/light + surface + A-B home + hide-flow-map). Holy Grail compliant. Figma `ODcQ2ERWYi3w504Z86TOy3` (Город ФМ) + `l38kZVrZXzdNlBIIOLFX4g` (Monte Carlo player reference). **Полный handoff: `docs/superpowers/HANDOFF-gorod-fm.md`.** NO paws data.

| ID | Задача | Статус |
|----|--------|--------|
| GOROD-001 | Figma context acquired (gorod-fm 2384:6054 + Monte Carlo 3314:13423 + 3407:2224) | done |
| GOROD-002 | Brand tokens extracted (cinema gradient + glass-20 + tile-tr-60 + Monte Carlo backdrop-blur 30px + Onest substitute) | done |
| GOROD-003 | Handoff `docs/superpowers/HANDOFF-gorod-fm.md` + session log + memory entry + RESUME swap | done |
| GOROD-004 | Write `designs/gorod-fm.html` skeleton — `<head>` (meta + Onest fonts + inline CSS @layer reset/tokens/base/layout/components/surfaces/utilities) + `<body>` scaffold (bg-layers ×2 + topbar + sidebar + main + player-mini + player-full + mobile-tabbar + tweaks) | done |
| GOROD-005 | Build Flow Map (`#/map` index hub — карточки всех экранов) | done |
| GOROD-006 | Build Главная (`#/home` — stations grid + filter chips + center cover + 2 варианта corner-FAB/sidebar-drawer Tweak) | done |
| GOROD-007 | Build Подборки (`#/podborki` — gallery tiles по Figma 2384:6054, 245/299/310/309/373 widths, tile-tr-60 + label rotated -90°) | done |
| GOROD-008 | Build Медиатека (`#/library` — 2-row grid + ad slot, mobile single col) | done |
| GOROD-009 | Build Избранное (артист profile + раздел list) | done |
| GOROD-010 | Build Страница трека (Monte Carlo desktop + mobile carousel + lyrics + история, adapt warm → cinema tokens) | done |
| GOROD-011 | Build Player overlay (mini bar bottom + full-screen Monte-Carlo-style overlay) | done |
| GOROD-012 | Mobile responsive 375/414/768 — fix gallery (заказчик: «стремно») + Monte Carlo mobile player | done |
| GOROD-013 | Adaptable surface architecture (`data-surface="web/mobile/tv/carplay"`) | done |
| GOROD-014 | Anti-slop + WCAG AA pass via `compound-engineering:design:design-implementation-reviewer` (Holy Grail Часть 9) | done (review.md committed; fix wave applied 2 commits) |
| GOROD-015 | Standalone build script `tools/build_gorod_fm_standalone.py` | done |
| GOROD-016 | Real assets Город ФМ (album covers + station artwork + artist photos) — PARTIALLY SUPERSEDED: оказалось ассеты есть в Figma `ODcQ2ERWYi3w504Z86TOy3`, скачиваются в GOROD-021. Остаются только реальные станционные обложки если клиент пришлёт отдельно | 🔒 partially superseded by GOROD-021 |
| GOROD-017 | Показ заказчику + фидбек по варианту (cinema / warm / light Tweaks) | 🔒 Эльбик-gate (Эльбик показывает клиенту) |
| GOROD-018 | После утверждения: Next.js + shadcn/ui dev-handoff | 🔒 Эльбик-gate (после approval GOROD-017) |
| GOROD-019 | WCAG: gradient darkened (cyan rgb(56,140,180), blue rgb(20,80,170)) + text-shadow на hero text · `--text-quat` остаётся <AA Normal на средне-цикловой части градиента — рекомендация для финального показа: добавить `rgba(0,0,0,0.20)` слой за блоками с длинным телом текста, если заказчик flagнет | done (фикс-волны 2: 5d58e43 darken+shadow + 9e58cbf pixel-perfect) |
| GOROD-020 | Pixel-perfect фикс (2026-05-27 evening): dedup топбар логотипа + sidebar vertical icon-over-text + Подборки tile labels read bottom-to-top per Figma 2384:6054 | done (commit 9e58cbf) |
| GOROD-021 | **v2 pixel-perfect rebuild from 5 Figma nodes**. ✅ Главная `2174:422` (commit `afd072a`, чёрная как Figma), ✅ Подборки `2384:6054` real photos (`b4edbed`), 87 assets скачаны. ⬜ Остаются: Медиатека `2385:2924`, Раздел Избранное `2535:11151`, Страница артиста `2537:14090` + standalone rebuild. | partial — 3 экрана + standalone остаются |
| GOROD-022 | `--brand-blue-light: #5168FC` + blue-tinted active (chips + player на `#/home`) | done (`b4edbed`) |
| GOROD-023 | `#/lives` placeholder route (Figma sidebar item) | done (`b4edbed`) |
| GOROD-024 | **AI-product визия зафиксирована** — `docs/superpowers/VISION-gorod-fm-ai-driven.md` (12 сообщений Эльбика 27.05, которые прошлая сессия потеряла) | done (`6c8e802`) |
| GOROD-025 | **Онбординг-пузыри `#/onboarding`** — Apple-Music-style: тап = выбор + рекурсивный bloom (жанр→артисты, артист→похожие), genre-coherent, безлимит, во весь экран, safe-zone (не на текст/кнопки) | done (`6c8e802` + `ef483a4`) |
| GOROD-026 | **Twinr AI чат** — collapsible dock, живой профиль (мутирует при стиринге), explainable «почему», AI-экскурс Imagine Dragons, вкусовая реклама, free-text | done (`38d334a`) |
| GOROD-027 | **Native AI в плеере** — «✨ почему?» reason-pill + Twinr steer-кнопка → открывают чат к ответу (AI = слой, не угловой виджет) | done (`8ec5e4a`) |
| GOROD-028 | **Karpathy ресёрч ×10** (`docs/research/gorod-fm/01-10`) + 2 синтез-дока: `ARCHITECTURE-gorod-fm-nextgen.md` (recsys/CLAP/BaRT/steering/licensing/MVP-roadmap) + `UX-DIRECTION-gorod-fm.md` (native AI, 3-tab IA, wave-identity) | done (`commits research` + `UX docs`) |
| GOROD-029 | **Стратегический разворот позиционирования** — «первый AI» → «музыка, которая твоя: видишь/правишь вкус, знаешь почему». 🆕 рынок = **МОСКВА** (Эльбик 06-02), НЕ KZ → локальность-как-moat ИСЧЕЗАЕТ (домашка Яндекса), wedge = только прозрачность+редактируемый вкус+объяснимость. | 🔒 Эльбик-gate (принять позиционирование) |
| GOROD-030 | **Лицензирование** (узкое горло №1): 7digital MaaS demo-переговоры + Spotify SDK для демо + свой KZ/CC seed + найм KZ IP-юриста. Старт НЕМЕДЛЕННО параллельно билду. | 🔒 Эльбик-gate (внешний/легал) |
| GOROD-031 | **UX-волна** (из `UX-DIRECTION`) — ✅ ВСЁ: живая «волна» (`a745802`) · экран «Мой вкус» `#/taste` · in-player wave-диалы (`4ecb562`) · 3-tab IA Волна/Мой вкус/Открыть (`4ecb562`) · between-track «now→next» лента (budget 4, `92f8079`) · AnalyserNode audio-reactive волна (opt-in «Озвучить волну», WebAudio pad→FFT, `92f8079`). ⬜ Опц. остаток: ретемизация Warm/Light под нейтраль; реал-аудио вместо demo-pad (Ф1+) | done (6/6) |
| GOROD-033 | **Tech-modern UI restyle** (Эльбик: «супер технологично и современно»): keystone — нейтрализован cyan/blue градиент-фон → near-black `#0B0C0F` + 1 сдержанный `#5168FC` glow (anti-slop). Аудит + рекомендации `docs/superpowers/UI-AUDIT-gorod-fm.md`. | done (commit restyle) |
| GOROD-032 | **Standalone для инвесторов собран** — `designs/gorod-fm-standalone.html` (self-contained, 2.12 MB). 🔧 Build-script `tools/build_gorod_fm_standalone.py` получил **image-optimization pass** (downscale + WebP q82, source-originals не трогаются): наивный инлайн давал **71 MB** (discach-90 4096×2731=10.9 MB ×2, bg-particles 4000×3000=4.4 MB) → нешерабельно. Теперь 19 refs (12 уник.) → −97% / 31.4 MB saved. Verify: 0 leftover asset-refs, contact-sheet визуально investor-grade, struct identical (6 script, 5 AI-модулей, 10 routes). ⚠️ Onest остаётся внешним (Google Fonts CDN) → офлайн fallback на system-font; опц. будущее: инлайн woff2 + dedup идентичных тайлов (12<19). Пересобрать после добавления 3 экранов GOROD-021. | done (2026-06-02) |
| GOROD-034 | **Resume→music flagship (VISION #7) построен** — был bare stub (текст-ссылка `onResumeDemo` авто-выбирала 5 хардкод-имён). Теперь полноценный концепт-демо: модалка (drop/paste/«Заполнить примером») → scripted «AI читает» theater → **explainable** вывод (keyword→вкус через `deriveTaste`: 15 правил → реальные bubble-имена + «почему» по каждому + era-insight по году) → seeds bubble-поле (toggle byName, гарант ≥5) → handoff `onContinue`→#/home+greet. On-device, ничего не грузится. Holy-Grail: Onest, нейтрал+#5168FC, ≥44px, focus-visible 3px, ESC/click-out/backdrop, `prefers-reduced-motion`, dialog/chip-токены 1:1 с wave-dials. Verify: node --check 6/6 scripts ✓, `deriveTaste` юнит-тест 4 входа (designer/dev/finance/empty) → все ≥5 picks + era ✓, IDs+wiring ✓, standalone rebuilt 2.25 MB. Visual QA ✅ (Chrome reconnected): прогнал onboarding→«Заполнить примером»→«Прочитать»(theater echoes matched kw)→explainable result(7 picks+era)→«Собрать радио» selects bubbles+saves taste+#/home+Twinr greets с профилем; 0 console errors. 🐞 нашёл+пофиксил **z-index баг** (`0ff6cda`): модалка была невидима за onboarding `<section>` z-200 → modal z-140→**250**. | done + visual-QA ✓ |
| GOROD-035 | **Taste-based sponsor tile (VISION #9) построен** — монетизация, «куда должен развиваться сервис». Нативная explainable steerable карточка на `#/taste`: читает живой taste-вектор → weighted tag-overlap match (5 спонсоров) → «Спонсор · по вкусу» + бренд/оффер + **«Почему вам:»** (прозрачно, referencing реальный вкус) + **«Меньше рекламы»** steer (set flag, dismiss, ack в delta) + re-match LIVE при правках вектора (+/−). Holy-Grail токены, монограм-лого (no emoji/slop), AA, focus-visible. Visual QA ✅: Яндекс-Афиша заматчилась на rock/metal вкус, «почему вам: Imagine Dragons и МЕТАЛЛ…», steer→«✓ учту», 0 console errors, node --check ✓. | done + visual-QA ✓ |
| GOROD-039 | **Karpathy-tier UX/UI + service АУДИТ** — `docs/superpowers/AUDIT-gorod-fm-screens-and-service.md`. 6 параллельных best-practices-агентов (Волна/Открыть/Explainability+Steering/Визуал+Motion/Онбординг+Habit/Архитектура+Монетизация) + grounded current-state аудит всех экранов (Chrome MCP). Вывод: 2 класса экранов (AI-поверхности сильны / legacy стриминг generic+slop). Конвергенция 3/6: честная «почему»-строка под каждым треком. Уникальная механика: «Исправь причину» (seamful reject — steering через объяснение). IA-решение: «Открыть»=неизвестное, «Мой вкус» впитывает архив. Moat=reason_tag corpus. План **GOROD-040..057** (P0 quick wins → P3 backend). | done — план готов |
| GOROD-040 | **Always-on «почему»-строка на плеере (L1)** — поведенческая, всегда видна («Ты дослушал Imagine Dragons до конца 3 раза»), не маркетинг. `.player-mini-reason` + bump `--player-mini-h` 72→84. Visual QA ✅. | done + visual-QA ✓ |
| GOROD-041 | **«Исправь причину» L2-popover (`TwinrWhy`)** — категорийно-определяющая механика: 3 честных атрибута, каждый rejectable «не моё» → strikethrough + status «✓ Убрал «X» — пересчитываю волну» + persist `gorodfm_rejected` + wave.bump + ribbon-receipt. Steering ЧЕРЕЗ объяснение. «почему?»-pill репойнтнут с чата→popover (L1→L2→L3-чат progressive disclosure). Visual QA ✅ e2e (reject→strike+status+persist+ribbon, fits viewport, 0 errors, node --check 7/7). | done + visual-QA ✓ |
| GOROD-042 | **Цвет-от-обложки** (опция A) — self-contained canvas-сэмплер `NowPlayingTint` (НЕ Vibrant.js → single-file clean; data-URI/same-origin не тейнтят canvas → работает и в standalone). Извлекает vibrant-цвет из cover → `--np-accent` → прогресс-бар + glow обложки. Visual QA ✅: Слеза-обложка → `rgb(235,74,70)` красный, прогресс+glow перекрашены. | done + visual-QA ✓ |
| GOROD-043 | **Slop-kill на плеере** — мульти-стоп градиент-плейсхолдер мини-плеера → **реал-обложка** (`home-featured-egor-krid.png`, 60×60 object-fit). Now-playing realigned **Слеза/Егор Крид** (когерентно с featured); чат-нарратив now-playing обновлён (greet/why/ribbon/backradio), музыка-тур «Путь к Imagine Dragons» сохранён как отд. экскурс. «Почему» нейтрально-поведенческая. Остаток slop (Трек/Медиатека/Избранное/Артист-силуэт) → GOROD-047 deep-dive. | done (плеер) · остальное в GOROD-047 |
| GOROD-044 | behavioral-anchoring copy — принцип уже применён в 040/041 (вся новая копирайт поведенческая). Остаток: sweep по app на «тебе понравится». | mostly done |
| GOROD-046 | **«Открыть» rebuild — conversational + taste-adjacency discovery** (P1, audit §2 #1-move). `#/podborki`: добавлен discovery-слой сверху → **РАЗГОВОР** (поле + 6 контекст-чипов → `GorodDiscover` mood-парсер → 4 результата с **«почему»**, taste-anchored) + **«Рядом с твоим вкусом»** (читает `gorodfm_taste` → соседние кластеры «в 1 шаге от твоего X») + «▶ Запустить как волну». Старая галерея → ряд «От редакции» (сохранена). Pixel-perfect HOME НЕ тронут (Эльбик-gate respected). Visual QA ✅: «тёмный вечер» → Молчат Дома/Buerak/Цой с объяснениями; адjacency Пост-панк/Гранж/Синтвейв из РОК+ЭЛЕКТРО; node --check 9/9; 0 console errors. | done + visual-QA ✓ |
| GOROD-048 | **Between-track transition card** (P1, audit §3/§5) — «DJ объявляет следующий трек + почему» вместо мёртвого спиннера. Новый модуль `TwinrTransition`: на «next»/«prev» (раньше no-op `#btn-next`/`#btn-prev`/`#player-full-next`) показывает центр-карточку (overline «Дальше в эфире»+spark · крупный title · artist · поведенческая «почему» над hairline · «нажмите чтобы перейти сразу») → авто-commit now-playing (мини-плеер title/artist/reason + home hero) → fade (~1.6с). Anti-slop: near-black + ОДИН content-derived `--np-accent` (НЕ slop-градиент/несоответствующая обложка — asset-wall честно), top-hairline (не left-border), tap-to-skip, `role=status aria-live=polite`, reduced-motion ок, `color-mix` с фолбэками. FLOW стартует Любимка·Niletto (канон тёплый-поп вектор), каждое «почему» = реальное поведение. Visual QA ✅ (Chrome :8765): next→«Любимка/Niletto» + «Тёплый поп ~95 BPM, как «Слеза» — дослушал 3 раза» (accent красный от обложки), commit→мини-плеер=Любимка; node --check 10/10; 0 console errors. **design-implementation-reviewer ✓ SHIP-READY (7/7 PASS, WCAG-AA).** ⚠️ accent-overline 4.96:1 = contrast-floor — НЕ темнить `--np-accent` <4.5:1 (GOROD-042 brightening частично страхует). | done + visual-QA + reviewer ✓ |
| GOROD-049 | **Twinr edge-glow вместо орб-пульса + motion-токены** (P1, audit §5 #4). Убран always-on `ai-pulse` shimmer-ринг лончера (орб-с-shimmer = 2023; audit: motion должен ЗНАЧИТЬ). Заменён на state-driven **краевое свечение** `.is-speaking` (`@keyframes twinr-breathe`/`twinr-breathe-dock`, «дыхание» `--dur-breathe` 1.6с) на лончере+доке — горит ТОЛЬКО пока Twinr говорит (драйв из `aiSay` typing→message + `TwinrChat.pulse()` для transition-card), гаснет в тишине. reduced-motion: статичный glow (сигнал сохранён). Motion-токены формализованы additively (`--ease-standard/-emphasized/-exit`, `--dur-breathe/-announce`); `--t-*` не тронуты (0 регрессий). Visual QA ✅: dock+launcher `is-speaking` toggle на greet, computed `animationName=twinr-breathe(-dock)`, glow box-shadow рендерится; node --check 10/10; 0 errors. | done + visual-QA ✓ |
| GOROD-052 | **«Открытый профиль» pitch-экран** (P2, audit §7 — убивает «Яндекс делает то же»; питч-аргумент №1). Новый роут `#/profile` (НЕ 4-я вкладка — 3-tab IA цела; вход с `#/taste` «Открытый профиль →» + прямой URL). Модуль `GorodProfile` читает live `gorodfm_taste`+`gorodfm_rejected` (fidelity — показанное = реальный профиль). Контент: **контраст «чёрный ящик (Яндекс/Spotify — grayscale+blur+lock, мёртвый) vs открытый профиль (alive, accent)»** · реальный вектор с провенансом по каждой грани («из онбординга — ты выбрал сам» / «усилено: дослушиваешь до конца») · 1 live-правка «меньше» → видимая квитанция + wave.bump · секция «Что ты оспорил» (читает rejected, иначе empty-state→плеер) · «даже реклама — твоя» strip · moat-caption. **WCAG-фикс:** новый токен `--accent-on-dark #8094ff` для мелкого accent-текста (бренд `#5168FC` = 4.25:1 < AA; новый = 6.7–7.1:1). Verify: node --check 11/11; live QA (5 граней, правка РОК 84→72%, квитанция «профиль слушается тебя», 0 errors); **design-implementation-reviewer ✓ SHIP-READY** (WCAG-AA весь текст, anti-slop clean, mobile 2-кол→1-кол без overflow, 0 errors). | done + visual-QA + reviewer ✓ |
| TD-GOROD-CTA-AA | App-wide: primary-кнопка white-on-`#5168FC` = **4.43:1** (чуть <AA 4.5 для 14px/700). Конвенция ВСЕХ кнопок (taste-sponsor-cta, ai-launcher, profile-cta) — не вводил в 052, унаследовано. Не блокер (UI-контрол + рядом ghost-дубль; reviewer: accept). Строгий AA-фикс app-wide: затемнить фон до `#4A5FE8` (→~5.1:1) ИЛИ текст ≥18.66px. | backlog |
| GOROD-045·047·050·051·053·054..057 | P1/P2/P3 остаток: Волна 3-зоны (🔒 pixel-perfect gate) · Артист/Трек deep-dive + slop-kill (🔒 нужен realign как плеер ИЛИ реал-обложки) · P2 loops остаток (`050` recap-карточка 9:16 · `051` контекст-старты Утро/Работа/Вечер · `053` стрики · `054` cold-start seed) · P3 backend (`055` reason_tag pipeline, 🔒`056` лицензирование CC→MERLIN, `057` B2B taste-ads). Детали → AUDIT §8. | pending |

---

## ⏸️ Bootstrap-порт (2026-05-19) — ПАУЗА (Эльбик-gated)

Liquid Glass → Bootstrap 5.3 dev-handoff порт. **Полный трекер: `docs/superpowers/HANDOFF-bootstrap-port.md`.** Paused 2026-05-27 — фокус на Город ФМ (новый клиент). Вернуться когда Эльбик попросит.

| Проект | Статус |
|--------|--------|
| `crm-bootstrap/` (CRM, 29 экр.) | ✅ ГОТОВ + отдан Эльбику (2026-05-20) |
| `twinr-bootstrap/` (Twinr, 21 стр. + AI + Customizer) | ⬜ Phase 0-3 done · NEXT = Phase 4 (Customizer) — на паузе |

Ветка `feat/bootstrap-port` (worktree `.worktrees/feat-bootstrap-port`), не запушена/не смержена. Открытый пункт CRM (решение Эльбика): токен `--ds-ink-4` контраст ~3.5–4.1:1 < WCAG AA — взят из утверждённого прототипа, см. `crm-bootstrap/docs/ACCEPTANCE.md`.

## Экраны

| ID | Задача | Статус |
|----|--------|--------|
| SC-001 | Промо-лендинг — все 7 вариантов | done |
| SC-002 | Логин — все 7 вариантов | done |
| SC-003 | Регистрация — все 7 вариантов | done |
| SC-004 | Статистика — кампании + KPI | done |
| SC-005 | Статистика — ролики кампании | done |
| SC-006 | Статистика — детали ролика | done |
| SC-007 | Рекламодатели — список | done |
| SC-008 | Добавить рекламодателя | done |
| SC-009 | Карточка рекламодателя (3 вкладки) | done |
| SC-010 | Создание кампании | done |
| SC-011 | Привязка ролика | done |
| SC-012 | Wordstat — полный дизайн | 🔒 Эльбик-gate (ждём ТЗ + MicroIT API спецификацию) |
| SC-013 | ИИ-аналитика — полный дизайн | 🔒 Эльбик-gate (ждём ТЗ + примеры реал-tier данных) |

## Компоненты

| ID | Задача | Статус |
|----|--------|--------|
| CP-001 | DESIGN.md — полная дизайн-система в markdown | 🔒 Эльбик-gate (gate on RC approval — финальная тема определяет токены) |
| CP-002 | Responsive адаптация (mobile/tablet) | 🔒 Эльбик-gate (применяется к Twinr/CRM после approval) |
| CP-003 | Перенос в Figma (обновить РК экраны в тёмной теме) | 🔒 Эльбик-gate (после approval финальной темы) |
| CP-004 | shadcn/ui component mapping | 🔒 Эльбик-gate (часть INT-002 Next.js этапа) |

## Интеграция

| ID | Задача | Статус |
|----|--------|--------|
| INT-001 | Выбор финальной темы с заказчиком | 🔒 Эльбик-gate (показ + фидбек) |
| INT-002 | Next.js проект на базе выбранной темы | 🔒 Эльбик-gate (после INT-001) |
| INT-003 | MicroIT API интеграция | 🔒 Эльбик-gate (после INT-002 — нужна реализация) |
| INT-004 | DaData API для ИНН | 🔒 Эльбик-gate (после INT-002 — нужна реализация) |

## Liquid Glass Redesign (2026-04-18)

| ID | Задача | Статус |
|----|--------|--------|
| LG-001 | Liquid Glass токены (Apple iOS 26 grey-tinted) | done |
| LG-002 | Photo backdrop (Matterhorn + clouds, Unsplash CC0) | done |
| LG-003 | 13 экранов по оригинальной иерархии twinr-full.html | done |
| LG-004 | Hash-routing + localStorage | done |
| LG-005 | Мок-данные радио-тематики (ООО Медиа Групп, ROL-XXX) | done |
| LG-006 | Single-file standalone версия (base64 embed) для заказчика | done |
| LG-007 | Apple-ревью через FigMCP (8002:114 Liquid Glass Effect) | done |
| LG-008 | Backdrop-filter performance fix (страницы remain mounted) | done |
| LG-009 | **Показ заказчику + фидбек/одобрение** | 🔒 Эльбик-gate |
| LG-010 | Responsive адаптация (mobile/tablet breakpoints) | 🔒 Эльбик-gate |
| LG-011 | Light theme (dawn) — опционально | 🔒 Эльбик-gate |
| LG-012 | Figma перенос новой темы (обновить РК экраны) | 🔒 Эльбик-gate |
| LG-013 | Backdrop picker (midnight / ocean / desert как варианты) | 🔒 Эльбик-gate |
| LG-014 | Next.js + shadcn/ui реализация на базе утверждённой темы | 🔒 Эльбик-gate |

## Турбо AI-модуль (2026-04-18 evening)

Расширение прототипа экранами Турбо-перформанс из Figma — интеграция в existing Liquid Glass дизайн-систему, без нарушения структуры 13 оригинальных экранов.

| ID | Задача | Статус |
|----|--------|--------|
| TURBO-001 | 9 AI-экранов (Источники/Промпты/Рерайтинг/Чат/Транскрибация/Документы/Видео/Wordstat/Работа с источником) | done |
| TURBO-002 | 5 модалок (edit group, sources selector, prompt editor, tags, keywords) | done |
| TURBO-003 | Discovery Hub на странице ИИ: 4 группы × карточки tools | done |
| TURBO-004 | Sub-nav chip-row с slide-morph indicator + group separators | done |
| TURBO-005 | Apple HIG fixes: aria-current, sidebar tooltips, destructive confirm, button loading, dropzone drag-enter | done |
| TURBO-006 | Modal luminance lift (панель светлее dimmed фона) | done |
| TURBO-007 | Страница «Руководство»: long-form reading с sticky TOC + scroll-spy | done |
| TURBO-008 | Standalone обновлён (1.6 MB, base64 backdrop inline) | done |
| TURBO-009 | **Показ заказчику новых 9 экранов + Guide** | 🔒 Эльбик-gate |
| TURBO-010 | Real data (MOS.RU, RUSSPASS и т.д. из Figma) вместо lorem ipsum | 🔒 Эльбик-gate |
| TURBO-011 | Empty states для zero-data scenarios (пустая история, нет источников и т.п.) | 🔒 Эльбик-gate |
| TURBO-012 | Mobile/tablet responsive для AI-модуля (chip-row → scroll, 2col → stack) | 🔒 Эльбик-gate |
| TURBO-013 | Dynamic glass reactivity (саmtop-filter saturate on scroll) | 🔒 Эльбик-gate |
| TURBO-014 | VoiceOver pass + контраст audit (WCAG AA) | 🔒 Эльбик-gate |

## Liquid Glass Customizer (2026-04-18 night)

Фулл-аудит Apple Liquid Glass HIG + iOS 26 skill + текущих токенов. Разбиение страницы «Руководство» на 38 droplet-капель + плавающая панель кастомайзера (фактура/оттенок/насыщенность/затемнение/форма/текстура + 6 пресетов). SVG-фильтры для frosted/grain + data-URI noise для линии/призмы.

| ID | Задача | Статус |
|----|--------|--------|
| CUST-001 | Research Apple HIG Liquid Glass (materials, variants, tints, Reduce Transparency) | done |
| CUST-002 | Audit current prototype: 5-tier material scale, blur/border/specular/ink tokens | done |
| CUST-003 | SVG filter defs (lg-frosted, lg-grain, lg-crystal) — inline в body | done |
| CUST-004 | CSS: 6 materials + 12 Apple system tints + 5 intensity steps + 4 dim levels + 4 shapes + 5 textures | done |
| CUST-005 | Droplet primitive — `.droplet` с tint/dim pseudo-overlay + texture overlay | done |
| CUST-006 | Split Guide content: 38 droplets (lead + headings dr-heading + para/list/callout/faq) | done |
| CUST-007 | Customizer panel: sticky sidebar, segment buttons, colour swatches, slider, preset chips | done |
| CUST-008 | 6 пресетов: Apple iOS 26 / Sunset / Ocean / Forest / Mono / A11y | done |
| CUST-009 | JS: data-attr control, localStorage persist, copy-CSS, reset, collapse | done |
| CUST-010 | Standalone пересобран (1.7 MB) с base64 backdrop | done |
| CUST-011 | Показ кастомайзера заказчику для выбора финальной фактуры/оттенка | 🔒 Эльбик-gate |
| CUST-012 | После утверждения — зафиксировать глобальные glass-* токены на выбранной комбинации | 🔒 Эльбик-gate |
| CUST-013 | Применить утверждённые токены ко ВСЕМ экранам (не только Руководство) | 🔒 Эльбик-gate |
| CUST-014 | Figma sync: обновить компоненты в Figma на утверждённую фактуру | 🔒 Эльбик-gate |
| CUST-015 | Удалить кастомайзер из production-сборки (оставить только для internal review) | 🔒 Эльбик-gate |

## Постер Тимирязева 79

| ID | Задача | Статус |
|----|--------|--------|
| PST-001 | Ресерч законов наружной рекламы Алматы | done |
| PST-002 | Дизайн постера 130×56 см (4 варианта) | done |
| PST-003 | GitHub Pages деплой | done |
| PST-004 | Утвердить цвет с мамой | done (forest — фактически фон #0a1810 чёрный + gold #c8a86e + forest accent #163522) |
| PST-005 | Файл для типографии | done (HTML референс + ТЗ) |
| PST-006 | Отправить заказ в типографию | done (20000₸, 3 раб.дня, ждём реквизиты) |
| PST-007 | Уведомление через eOtinish / egov | разбит ниже |
| PST-008 | Фото перспективы фасада | 🔒 Эльбик-gate |

### PST-007 Согласование с акиматом — детализация (ресёрч 2026-04-24)

Законы проверены: Закон РК «О рекламе» 508-II ст. 11 п. 1-1 (объявления «продаётся» НЕ входят в список исключений из рекламы), Правила наружной рекламы Алматы V23R0001724 (нет цветовых ограничений, согласование эскиза обязательно), Дизайн-код V23R0001751 п.6 (нет запрета на чёрный, но оценочная норма «несвойственных архитектурному стилю» — риск отказа по цвету).

**Услуга:** egov.kz → «Согласование размещения объектов наружной (визуальной) рекламы … областного и районного значения». Орган: Управление городского планирования и урбанистики Алматы (пр. Абая 90), через подразделение акимата Бостандыкского района.

**Плата:** 1 МРП/мес = 4 325 ₸ (площадь < 2 м²). КБК 105402. До подачи — оплатить первый месяц, далее — до 25 числа каждого месяца.

**Штрафы за размещение без согласования (физлицо, мама):** ст. 455 КоАП — 15–25 МРП (64 875 – 108 125 ₸); ст. 505 КоАП — 20 МРП (86 500 ₸); плюс демонтаж за свой счёт и доначисление платы. Первое нарушение часто — предупреждение, но на Тимирязева «любят кошмарить» (слова Арины).

| ID | Задача | Статус |
|----|--------|--------|
| PST-007a | Подготовить технический эскиз (PDF с размерами 1300×560 мм, HEX/Pantone, mock-up на фасаде) | 🔒 Эльбик-gate |
| PST-007b | Оплата 4 325 ₸ через Kaspi → КБК 105402 (Бостандыкский район) | 🔒 Эльбик-gate |
| PST-007c | Подать заявление на egov.kz под ЭЦП мамы (приложить эскиз + правоустанавливающий + чек) | 🔒 Эльбик-gate |
| PST-007d | Ждать 5 рабочих дней, получить письмо-согласование | 🔒 Эльбик-gate |
| PST-007e | При отказе — переделать эскиз (бежевый/серый вместо чёрного если причина п.6 дизайн-кода) | 🔒 Эльбик-gate |
| PST-007f | Ежемесячная уплата 4 325 ₸ до 25 числа пока висит баннер | 🔒 Эльбик-gate |

## RMG Smartwatch (5 станций)

| ID | Задача | Статус |
|----|--------|--------|
| SW-001 | Базовый прототип (5 тем, плеер, карусель) | done |
| SW-002 | Убрать историю эфира | done |
| SW-003 | Треки вместо подписей станций | done |
| SW-004 | Увеличить мелкие тексты для реальных часов | done |
| SW-005 | Подкасты: навигация подкаст→эпизоды→плеер | done |
| SW-006 | Избранное на подкастах/эпизодах | done |
| SW-007 | Ревью Stas/Alexei | 🔒 Эльбик-gate |
| SW-008 | Остальные станции по брендбукам (PDF скачаны) | 🔒 Эльбик-gate |

## Лендинг «Обучение кинологов» (2026-04-24)

Новый клиент под брендом Paws.kz — курс Анастасии Сундеевой. 3 варианта прототипа: paws-основной / Liquid Glass + paws / Material 3 + paws. Контент вытащен из Telegram-чата «Обучение» через Telethon (`tools/read_obuchenie.py`), стиль paws.kz — через FigMCP (файл `dev`, Paint/Text/Effect styles).

**Артефакты:**
- `designs/kinolog-paws.html` + `-standalone.html` (125 KB)
- `designs/kinolog-glass.html` + `-standalone.html` (851 KB, с Matterhorn backdrop)
- `designs/kinolog-material.html` + `-standalone.html` (133 KB)
- `.claude-memory/kinolog_landing_brief.md` — выжимка ТЗ из чата
- `.claude-memory/paws_figma_tokens.md` — токены из FigMCP
- `.claude-memory/kinolog_landing_audit.md` — визуал + UX + WCAG + hallucination audit

| ID | Задача | Статус |
|----|--------|--------|
| KIN-001 | Telethon-скрипт чтения чата «Обучение» + фильтр ключевых слов | done |
| KIN-002 | FigMCP OAuth через chrome MCP + getStyles → токены paws.kz | done |
| KIN-003 | Бриф: 48 блоков ТЗ выжаты из чата | done |
| KIN-004 | Paws-вариант: hero/segments/objections/5 модулей/3 тарифа/автор/FAQ/CTA | done |
| KIN-005 | Glass-вариант с белым лого и Matterhorn backdrop | done |
| KIN-006 | Material 3-вариант (M3 tokens + paws accent на CTA) | done |
| KIN-007 | Реальный контент: лого paws.kz, фото Анастасии с my-dog.kz | done |
| KIN-008 | WCAG-фикс: белый на `#EB6400→#FF9500` (AA Large), eyebrow `#B85A00` | done |
| KIN-009 | Антигаллюцинация pass: фамилия Сундеева, убран LIFE, «2-3 площадки» → «несколько» | done |
| KIN-010 | Семантика: убран прогресс-бар без смысла, seg-tag → реальные `<a>` ссылки | done |
| KIN-011 | Standalone сборка через `tools/build_kinolog_standalone.py` | done |
| KIN-012 | **Показ заказчику — Серёга/Татьяна/Настя** | 🔒 Эльбик-gate |
| KIN-013 | Дождаться ответов Насти на 7 уточнений (статистика, IAABC, кейсы) | 🔒 Эльбик-gate |
| KIN-014 | Подключить реальные CTA — форма заявки / Telegram | 🔒 Эльбик-gate |
| KIN-015 | Добавить дату старта потока когда будет известна | 🔒 Эльбик-gate |
| KIN-016 | Блок отзывов/кейсов когда получим от Насти | 🔒 Эльбик-gate |
| KIN-017 | Mobile-тест на 375/768px | 🔒 Эльбик-gate |
| KIN-018 | Реализация в Next.js после выбора финального варианта | 🔒 Эльбик-gate |

## RU.TV — Showcase Aggregator (2026-04-29)

Сайт-витрина для **RU.TV** (Russian Media Group): TV+радио+клипы+чарт+расписание+новости. Один main HTML с переключателем стилей **Liquid Glass ↔ Apple** (Holy Grail Часть 3.2 compliant). Реальные ассеты RU.TV из `~/Desktop/export rutv/` (171 файл, ~9MB stand-alone), русские артисты (SHAMAN, Полина Гагарина, JONY, MIYAGI, Macan и т.д.), партнёры РМГ (Русское Радио, DFM, MAXIMUM, Monte Carlo, Хит FM).

**Артефакты:**
- `designs/showcase-aggregator.html` — primary
- `designs/showcase-aggregator-standalone.html` — standalone 9.7 MB с base64 inlined assets
- `designs/assets/rutv/` — 87 PNG + 17 JPG real assets из export rutv
- `tools/build_showcase_standalone.py` — extends pattern matcher на JS-data ссылки на assets
- `designs/screenshots/showcase/v3_*` — final visual verify

**Структура (Главная page):**
- Sidebar: RU.TV красно-белый oval logo + mini-player (image 1, LIVE) + nav (Прямой эфир / Каналы / Станции / Чарт / Плей-листы / Расписание / Клипы / Новости / Избранное / Настройки)
- TopBar: search + notifications + avatar
- Hero carousel (4 cards): «Прямой эфир RU.TV», «Звёзды Хайпа · LIVE Арена», «Полевой — премьера», «Статус: В сети»
- Chip-row категорий (9): Все · Музыка · Сериалы · Спорт · Новости · Подкасты · Развлечения · Детям · Документальное
- Row Каналы (6): RU.TV, Русское Радио ТВ, DFM TV, Maximum TV, Monte Carlo TV, Хит FM TV — реальные image overlays
- Row Радиостанции (8): real artwork
- Row Сейчас слушают (6): SHAMAN, Григорий Лепс, Полина Гагарина, Дима Билан, Валерий Меладзе, JONY
- Чарт RU.TV top-10 list-style с большими розовыми цифрами 01-10 + trend indicators
- Жанры (7): Поп-Хиты, Шансон, Танцы, Рок, Ретро, Дискотека 80-х, Лирика
- Исполнители (8 round avatars с real artwork)
- DJ (6): DJ Smash, DJ Грув, Слава Марлоу, Артур Пирожков, Filatov & Karas, Леонид Руденко
- Музыка по настроению (6): Энергия, Релакс, Романтика, Фокус, Вечеринка, Утро
- Клипы недели (7): SHAMAN, JONY, Полина Гагарина, MIYAGI, Macan, Артур Пирожков, Слава Марлоу
- Главные новости (6): real promo banners
- Расписание RU.TV — 7 дней × 7 часов = 49 cells цветной grid с программами
- Russian Media Group партнёры (5)
- Footer: Головной офис RU.TV / Связь + bottom links
- Sticky bottom radio player (Spotify-pattern)
- Tweaks panel (Glass / Apple switcher) — bottom-right floating

**Anti-slop pass:** шрифт Onest (НЕ Inter/Roboto), hit-targets ≥44px, AA Normal на текстах, real assets вместо SVG illustration, focus-visible boost для TV (1920+).

| ID | Задача | Статус |
|----|--------|--------|
| RUTV-001 | Brief Questions Gate | done (через carte blanche от заказчика) |
| RUTV-002 | FigMCP подключён, Figma структура изучена (DFM-style витрина РМГ) | done |
| RUTV-003 | Real assets из export rutv интегрированы (104 PNG/JPG, ~9MB) | done |
| RUTV-004 | Single-file Glass + Apple через Tweaks (Holy Grail compliant) | done |
| RUTV-005 | Chrome MCP visual verify (real backdrop-filter) | done |
| RUTV-006 | Mobile responsive (414×1200) | done |
| RUTV-007 | TV viewport check (1920×1080) | done |
| RUTV-008 | Standalone build с extended assets pattern matching | done |
| RUTV-009 | **Показ заказчику + фидбек на направление** | 🔒 Эльбик-gate |
| RUTV-010 | Apple-style fidelity audit live (apple.com/tv-pr) | 🔒 Эльбик-gate |
| RUTV-011 | Smart TV app mode (10ft viewing, remote control focus) | 🔒 Эльбик-gate |
| RUTV-012 | Замена «РМГ» partner plates на реальные SVG лого | 🔒 Эльбик-gate |
| RUTV-013 | Реальные portrait фото артистов вместо клиповых artwork | 🔒 Эльбик-gate |
| RUTV-014 | Inner pages: Каналы list / Чарт top-100 / Расписание полное | 🔒 Эльбик-gate |
| RUTV-015 | Реальные video player integration (HLS stream RU.TV) | 🔒 Эльбик-gate |
| RUTV-016 | Next.js + shadcn/ui реализация после утверждения стиля | 🔒 Эльбик-gate |

### v4 Production polish (2026-04-29 evening)

| ID | Задача | Статус |
|----|--------|--------|
| RUTV-040 | Spacing rhythm: row-section 38→56px, content padding-bottom 96px, hero overlay 44/52, sidebar item min-height 44px | done |
| RUTV-041 | Mini-player UX fix: убрал always-visible big play, теперь hover-only overlay | done |
| RUTV-042 | Apple sidebar active: subtle white tint + 3px красный marker bar (НЕ pink pill как Glass) | done |
| RUTV-043 | Hero card: solid bg + ::before pseudo для consistent overlay, hero title text-shadow | done |
| RUTV-044 | Apple Dark подтянут: sidebar/cards более solid (rgba 0.55→0.78 / 0.7→0.95) | done |
| RUTV-045 | Light theme добавлен (3-й variant): Apple Music Light HIG, white sidebar, brand red accent, все text colors переопределены | done |
| RUTV-046 | Bug fix Light: hero CTA остаётся white-on-dark (не overrid'ить под dark на dark) | done |
| RUTV-047 | Live badge: brand-coloured glow + tighter padding | done |
| RUTV-048 | Chart rows: subtle dividers + hover state | done |
| RUTV-049 | Footer/Partners spacing: 32→48 gap, edge-to-edge cleanup | done |

### v5 Cinematic вариант + media backdrop (2026-04-29 night)

| ID | Задача | Статус |
|----|--------|--------|
| RUTV-050 | Создать `showcase-cinematic.html` — Apple TV+ landing вайб (рядом с dashboard) | done |
| RUTV-051 | Off-canvas drawer sidebar с overlay backdrop blur, выезжает по burger | done |
| RUTV-052 | Full-screen hero 100dvh с image 1.png + cinematic typography clamp(44-96px) | done |
| RUTV-053 | Top-nav transparent → solid backdrop при scroll (Apple TV+ pattern) | done |
| RUTV-054 | Reveal-on-scroll fade-in (IntersectionObserver) для секций | done |
| RUTV-055 | Bento layout каналов: 1 featured + 5 regular grid | done |
| RUTV-056 | Chart top-3 portrait cards с 96px цифрами + остальные top-10 в clean list | done |
| RUTV-057 | Artists horizontal carousel с 280px round avatars (Apple Music style) | done |
| RUTV-058 | Bento mosaic жанров: wide tiles + regular grid | done |
| RUTV-059 | Apple-style CTA «Скачать приложение» с radial gradient backdrop + App Store/Google Play badges | done |
| RUTV-060 | Active nav-tab подсвечивается при scroll (waypoint-style) | done |
| RUTV-061 | Все 3 темы в cinematic (Apple Dark default / Glass / Light) | done |
| RUTV-062 | Glass backdrop в обоих файлах: убран Matterhorn → image 1.png концертный кадр (по теме music TV) | done |
| RUTV-063 | Carousels paddings: scroll-padding-left/right на row-track / chip-row / hero-track / artists-track | done |
| RUTV-064 | Build script extended VARIANTS = [aggregator, cinematic] | done |
| RUTV-017 | Mobile responsive deep audit обоих вариантов (375/414/768) | 🔒 Эльбик-gate |
| RUTV-018 | Финальная brand check от RU.TV (шрифты, font-faces, real RU.TV brand guidelines) | 🔒 Эльбик-gate |
| RUTV-019 | Performance audit (10 MB standalone — на slow connection долго грузится. WebP optimization) | 🔒 Эльбик-gate |
| RUTV-020 | Apple HIG fidelity audit на cinematic (apple.com/tv-pr live audit через chrome MCP) | 🔒 Эльбик-gate |
| RUTV-021 | Заказчик выбирает: cinematic vs dashboard direction → дальнейший development идёт в выбранном направлении | 🔒 Эльбик-gate |

### v6 Landing — Figma 1-в-1 + Karpathy-tier UX/UI best (2026-05-13)

Эльбик попросил «свёрстать pixel-perfect лендинг RU.TV из Figma». FigMCP подключён через Chrome OAuth, найден frame `3373:2073` "Главная" (1440×3975 white-bg). Выкачана структура: top-nav 5 items с SF Pro Symbols glyphs, hero Uma2rman + image1, 5 афиш (Анна Семенович МК / Звёзды Хайпа / Лёгкое знакомство / placeholder / Masters of the Air), RASA Пулевой featured + image2 + white CTA, 6 клипов 236×236 (Артём Качер / Сергей Зверев / MIA BOYKA / INSTASAMKA / Нина Фокина / Авраам Руссо), 5 новостей (Гарик / Влад Топалов ×2 / Виктория Боня), 5 программ (СТАТУС:В СЕТИ / ДЕНЬГИ / СУПЕР 20 / ТЕМА), partners (Русское Радио / RU.TV / MAXIMUM / RADIO MONTE CARLO / ХИТ FM), footer с контактами + App Store/Google Play badges.

Все ассеты mapping подтверждён через Read PNG: Rectangle 4322 series + image1/image2 + unsplash_* партнёрки + RUTV 2 (пустой) → реальный лого собран как inline SVG (currentColor RU + masked TV badge).

Сделаны **2 версии** (Эльбик: «лучший сайт что возможен И версию что 1в1 тоже оставь как 2 вариант»):

**Артефакты:**
- `designs/rutv-landing.html` (production-best, 120 KB) + `-standalone.html` (11.2 MB)
- `designs/rutv-landing-figma.html` (Figma 1-в-1, 36 KB) + `-standalone.html` (4.1 MB)
- `tools/build_rutv_landing_standalone.py` — base64-инлайнер для обеих версий

**Production-best спецификация (Karpathy-tier UX-research applied):**
- **SPA hash-router** 7 views (home / live / news / poster / video / programs / schedule)
- **Sticky nav** с frosted backdrop-blur (Apple HIG iOS 26 Liquid Glass), transparent over hero → solid on scroll
- **Cinematic hero** 100dvh с Ken Burns анимацией bg image, gradient top→bottom (НЕ flat 40%), LIVE pulse pill (Twitch-style) с auto-changing viewer count, eyebrow + giant title clamp(38-84px) + meta row + 2 CTAs (Apple TV+ pattern)
- **Now-playing chip** Spotify-style fixed bottom-right с rotating album art + dismiss
- **Category chips row** sticky под navom (Apple Music)
- **Card hover preview** Netflix-pattern: scale 1.02 + shadow-xl + play overlay fade-in
- **Featured premiere** RASA Пулевой как floating card с rounded corners + hover scale
- **Schedule grid** YouTube TV pattern: 7 days × time slots, currently-airing red highlight с LIVE pulse
- **Subscribe banner** brand red gradient с decorative glow
- **6 inner views** production-quality (Live player с up-next sidebar, News с featured + 12 cards + filter, Poster с date-cards + венs, Video grid 12 clips + sort, Programs с stats + episodes, Schedule full week × time)
- **Modal video player** с overlay backdrop-blur, ESC + click-outside close
- **Mobile bottom nav** с frosted backdrop (5 icons sync with route)
- **Dark mode** auto via prefers-color-scheme
- **Accessibility**: skip-link / aria-current / aria-live / focus-visible / role landmarks / keyboard nav
- **SEO**: title, description, og:* full set, twitter:card, JSON-LD WebSite + Organization
- **Performance**: preload hero image, lazy load all cards, critical CSS inline
- **Typography**: Onest 400-900 + SF Pro fallback (HG-compliant, НЕ Inter/Roboto)
- **Refactoring UI**: 5-tier shadow ladder, brand-glow shadow, concentric corners (radius xl→pill)
- **Reduced motion**: prefers-reduced-motion respect (kills Ken Burns + reveal animations)

**Real RU.TV logo:** Inline SVG с маской — белый "RU" + circle с "TV" вырезанным (currentColor для адаптации к фону). Original RUTV 2.png в Figma экспорте — пустой; реальный канонический бренд воссоздан из `unsplash_qiMCJHg2vTI.png` партнёрской badge.

| ID | Задача | Статус |
|----|--------|--------|
| RUTV-100 | FigMCP OAuth через Chrome MCP подключение | done |
| RUTV-101 | Figma frame 3373:2073 "Главная" mapping (depth 5+) — 8 sections + footer + 19 unique images | done |
| RUTV-102 | Cross-reference Figma image hashes ↔ designs/assets/rutv/ files via Read PNG (28 unique) | done |
| RUTV-103 | rutv-landing-figma.html — pixel-perfect 1-в-1 Figma copy (white bg, top-nav, padding 230px, SF Pro fallback) | done |
| RUTV-104 | Real RU.TV logo SVG (currentColor, masked TV badge) — replaces empty RUTV 2.png | done |
| RUTV-105 | rutv-landing.html — production-best с Karpathy UX research (Apple TV+/Netflix/Spotify/YT TV patterns) | done |
| RUTV-106 | SPA hash router (#/home, #/live, #/news, #/poster, #/video, #/programs, #/schedule) | done |
| RUTV-107 | Live view: player frame + LIVE badge + up-next sidebar (7 items) + actions (like/share/quality) | done |
| RUTV-108 | News view: filter chips + featured news + 12-card grid + load-more | done |
| RUTV-109 | Poster view: 5 horizontal event-cards с date column + meta + CTAs | done |
| RUTV-110 | Video view: filter + sort + 12 квадратных clips grid | done |
| RUTV-111 | Programs view: 6 program cards с stats (episodes/schedule/rating) | done |
| RUTV-112 | Schedule view: full week × 7 time slots grid с today highlight + LIVE cell | done |
| RUTV-113 | Mobile responsive (375/414/768) с bottom nav, hero 100dvh, stacked cards, snap-x carousels | done |
| RUTV-114 | Standalone build script для обеих версий (rutv-landing-standalone 11MB / figma-standalone 4MB) | done |
| RUTV-115 | Chrome MCP visual verify: home/live/news/poster/video/programs/schedule × desktop/mobile/iPad | done |
| RUTV-116 | Real video stream integration (HLS placeholder → реальный) | 🔒 Эльбик-gate |
| RUTV-117 | Search функция (search bar в topnav пока inactive) | 🔒 Эльбик-gate |
| RUTV-118 | User auth flow (Войти кнопка пока без backend) | 🔒 Эльбик-gate |
| RUTV-119 | Заказчик выбирает: Figma 1-в-1 vs production-best → выбранный → Next.js + shadcn/ui | 🔒 Эльбик-gate |
| RUTV-120 | Подача RU.TV: deck + walkthrough видео обеих версий | 🔒 Эльбик-gate |

### Showcase v2 — розовый ребрендинг + новая структура (2026-07-15, ветка `feat/rutv-showcase-v2`, commits 980f025 → af89612 (без сайдбар-виджета, Супер 20=топ-10+страница) → da35e57 (хедер без надписи раздела); поставлено в Saved msg 602428)

По ТЗ Эльбика (фото с красной обводкой): розовый #E40087 с живого ru.tv + официальный лого (SVG из шапки сайта, `designs/assets/rutv/rutv-logo-official.svg` + mark), hero эфира + рекламный слот 300×600 с ротацией, 6 подканалов (клик переключает эфир), меню Главная/Премия/Новости+Афиша/Программы(9 плиток)/Видео/Витрина подарков, PiP мини-плеер вместо нижнего радио-бара (паттерн YouTube/Twitch), one-click эфир из топбара, баллы за просмотр (Twitch channel points: +10/5 мин, сундук +50/15 мин). Верифицировано скриншотами: 3 темы × desktop/mobile, все 5 страниц, standalone офлайн из чистой папки (0 assets-запросов, консоль 0).

| ID | Задача | Статус |
|----|--------|--------|
| RUTV-121 | Вставить реальный URL лендинга Премии RU.TV в `#sbPremia` (сейчас href="#" + toast) | 🔒 заказчик |
| RUTV-122 | Ведущие: реальный состав и фото (сейчас 6 имён-плейсхолдеров с монограммами) | 🔒 заказчик |
| RUTV-123 | Программы: реальная сетка (9 демо-плиток; «Супер 20» и «Стол заказов» — реальные бренды RU.TV) | 🔒 заказчик |
| RUTV-124 | Мобильный рекламный формат: на <1100px слот скрыт — нужен креатив 300×250 или нативный. + v2.6.1: слот у hero стал fluid-колонкой (высота = плееру); продаваемая IAB 300×600 гарантирована при ≥1500px, на 1100–1500 высота слота 450-600 — при продаже внешней рекламы там тоже 300×250 | open |
| RUTV-125 | Сверить розовый и лого с брендбуком RU.TV (#E40087 взят из favicon.svg ru.tv; лого из logo.e3ca789.svg их шапки) | 🔒 заказчик |
| RUTV-126 | Подканалы: названия/наполнение потоков подтвердить (2026-07-28: по правке Марго на главной остались 2 рубрики — 80-е · 2000-е; «Детям» исключена целиком) | 🔒 заказчик |
| RUTV-127 | Прод-тайминги баллов: в демо ускорено ×5 (60с/90с вместо 300с/900с) — вернуть при интеграции | open |
| RUTV-128 | Мобильное меню: сайдбар на <900px скрыт, разделы недоступны | done (v2.7: единый drawer-бургер на всех ширинах — правка Марго «меню прячем» закрыла и мобилку) |

### Showcase v2.8.1 — промоблоки, волна DFM 30.07 (msgs 608247-608263; zip в Saved msg 608769)

Волна 30.07 разобрана по слову: (а) фон страницы — Стас 608247 попросил убрать, но сам снял вопрос в 608255 («это не трогай, я разобрался — там можно тему выбрать») → НЕ тронут; (б) боковой промоблок у эфира — Стас 608251-252 «а это точно 300×600?» + owner-уточнение в сессии («одним фоном, без картинки, чтобы было понятно, что рекламный блок») → ротация постеров-креативов удалена целиком (promos/renderPromo/CSS слайдов), слот = одна статичная тем-панель (glass-bg-strong) со знаком RU.TV + «Реклама на RU.TV» + ad@ru.tv · +7 499 579-77-99 (контакт из подвала); колонка по-прежнему тянется к плееру, кромки бит-в-бит (edgeDiff 0 @1920/@1280). Промежуточная итерация «честный креатив 300×600 + брендированный добор» (коммит 19009fc) откатана уточнением owner'а в 46d72d1 — в Saved остался её zip 608762 (устарел, актуален 608769); (в) карусель баннеров под эфиром — Марго 608253 «шире по высоте» + Стас 608254 «по 3 штуки видимых» → 3 в ряд (было 4), aspect 2.35:1→2:1 (590×295 @1920), типографика подросла (title 21px). Верифицировано: слот без единой картинки числом (0 img/bg-image), 3 темы, 1920/1280/mobile, консоль 0, офлайн-смоук standalone 0 asset-запросов. Полотна light/dark(glass) в Saved 608770/608771 + dark-без-фона (Apple Dark) 608776. Standalone полегчал 9.3→8.2MB (ушли постеры ротации). **Приёмка 30.07 днём: Марго 608782 «мне нравится» (+ «блоки больше не делать») и Стас 608784 «класс, отправим коллегам»; по просьбе Марго 608785 редакции отдан standalone-HTML одним файлом (Saved 608787).**

### Showcase v2.7 — правки Марго 27.07 (чат DFM msg 606696; zip в Saved msg 607537)

Все правки внесены за одну сессию (2026-07-28): (1) меню слева спрятано — off-canvas drawer с бургером в шапке, лого переехало в topbar (инлайн-дубликат вектора: use/symbol на file:// Chromium не красит — «Unsafe attempt to load URL»); (3) карусель баннеров сразу под окном прямого эфира; (4-6) порядок главной: Программы → Свежие новости → Супер-20, дальше 80-е/2000-е/Новые клипы; «Ведущие»/«Артисты»/«Каналы» с главной сняты и живут отдельными пунктами меню (свои страницы-сетки channels/artists/hosts); из эфирных рубрик исключена «Детям» (поток+карусель) — «абсолютно точно исключаем „Дети“» (в блоке «Каналы» детского канала и не было). Нумерация оригинала без п.2 — так в сообщении. Бонус: drawer закрыл RUTV-128 (мобильное меню). Верифицировано: 3 темы × 1920 + 390, порядок секций и состав меню сняты DOM-аудитом числом, консоль 0, офлайн-смоук standalone из чистой папки (0 assets-запросов).

### Showcase v2.3 — 14 правок редакции RU.TV (2026-07-16, чат DFM/Стас msg 602707; поставлено в Saved msg 602743)

Все 14 правок редакции внесены за одну сессию: (1) лого розовым во всех темах; (2) колокольчик убран, «Прямой эфир» слева на уровне hero; (3) «Премия РУ.ТВ» кириллицей + вниз меню; (4) «Видео» под «Главная»; (5) плитки страницы Программ компактнее (auto-fill 170px); (6) миниатюры новостей 1:1; (7) «Свежие новости»; (8) ведущие без привязки к программам; (9) соцсети только ВК/ОК/MAX; (10) колонка «Контакты» в подвале; (11) рег. текст Роскомнадзора; (12) маркировка 16+; (13) бейджи App Store/Google Play (вектор с прода montecarlo) + RuStore (нарисован); (14) колонка «Выдача призов». Верифицировано: 3 темы × desktop/mobile, консоль 0, офлайн-смоук из чистой папки (0 assets-запросов).

| ID | Задача | Статус |
|----|--------|--------|
| RUTV-129 | Возрастная маркировка: поставлено «16+» (публичного первоисточника нет — Wikipedia/сайт не отдают) — значение сверить с редакцией | 🔒 заказчик |
| RUTV-130 | RuStore бейдж нарисован по мотивам официального (чёрная плашка + синий знак-стопка) — заменить на официальный из брендбука RuStore при имплементации | open |
| RUTV-131 | «Выдача призов»: график/адрес/почта — демо-текст, реальные условия пришлёт редакция | 🔒 заказчик |
| RUTV-132 | Аспект зоны эфира (вопрос Алексея DFM 602828 + Стас 602829 «попробуем на разных экранах»): hero фикс-600px → аспект плавает 1.43:1@1366…3.71:1@2560, реальный 16:9-стрим будет кропиться на широких (≤1100px уже 16/9; layout НЕ режется — прогон 1280–2560 в session_2026_07_16_rutv_v24_sidebar.md). Решение: cap ширины контента ~1680px (реко) vs честный aspect-ratio 16/9; сначала ответ в чат (драфт ждёт OK) | **done 2026-07-22** — Алексей сам дал директиву (DFM 605302-305: «всё что видео — 1920×1080… Шамана кропнем и нас кропнут») → экран эфира = честный `aspect-ratio: 16/9` на всех ширинах (ar 1.778 проверен 1280/1920), hero выше промо 300×600 (слот top-aligned); драфт ответа в чат не нужен |

### Showcase v2.5 — пакет правок Эльбика из Saved Messages 07-17 (msg 603079-603096; поставлено в Saved msg 603105)

11 правок внесено за сессию: (1) 603080 — «Каналы» подняты на место плиток подканалов + заголовок «Каналы — сейчас в онлайне»; (2) 603093 — промо-полоса из 4 широких баннеров (Премия/концерт/приложение/витрина) после блока каналов; (3) 603081-84 — плитки подканалов развёрнуты в 3 рубрики-карусели «Детям»/«80-е»/«2000-е»: LIVE-поток первым + клипы по тегу + ссылки «Всё детское →» и т.п. (механика тегов: новый материал с тегом сам попадает в карусель); (4) 603079 — «Свежие новости»: 3 карточки в ряду (было 4-5) + подзаголовок-лид; (5) 603086 — «лесенка» устранена: bleed каруселей за контент убран, правый край всех секций = 1860px бит-в-бит; (6) 603087 — переключатель тем перенесён в низ сайдбара (на мобиле ≤900px — прежняя плавающая пилюля); (7) 603088 — полоса брендов РМГ (ХИТ FM · РУ.ТВ · MAXIMUM · Monte Carlo · DFM · РМГ) над подвалом; (8) 603090 — «Контакты» и «Выдача призов» в нижней строке подвала после MAX; (9) 603091 — белая подложка под прорезными буквами «ТВ» лого (белые буквы в розовом круге, все темы); (10) 603092 — рамки градиентных плиток переведены с border на inset box-shadow (не рвутся на скруглениях); (11) 603096 — кнопка «Прямой эфир» из шапки удалена (вход в эфир: hero, PiP, LIVE-плитки). Верифицировано: 3 темы × desktop 1920 + mobile 390, консоль 0, h-overflow 0, офлайн-смоук из чистой папки 0 assets-запросов.

| ID | Задача | Статус |
|----|--------|--------|
| RUTV-133 | Полоса брендов РМГ: официальные вектора | **done 2026-07-17** — SVG взяты из футера rusradio.ru (owner дал источник), перекрашены в currentColor; состав: Русское Радио · ХИТ FM · MAXIMUM · Monte Carlo · DFM · RMG, РУ.ТВ убран (мы на сайте РУ.ТВ) |
| RUTV-134 | Рубрики Детям/80-е/2000-х: клипы и обложки — демо (градиенты + реальные названия треков); реальное наполнение придёт из тегов материалов (603084) | 🔒 заказчик |
| RUTV-135 | Стандарт ассетов (Алексей DFM 605302-305): всё видео = 1920×1080 (16:9), персоны и треки = 1000×1000 (1:1, скругление ок), новости — на наш выбор (оставлен квадрат 1:1 — согласуется с правкой редакции №6). Внесено: hero-экран 16:9 · чарт-превью Супер 20 80×45 (клипы) · ведущие 1/1.15→1/1; уже были 16:9: каналы/рубрики/клипы/видео/PiP; артисты 1:1 | **done 2026-07-22** |
| RUTV-136 | SHAMAN остался в superseded-файлах: `showcase-cinematic.html` + `showcase-cinematic-standalone.html` (v1, апрель) и `smartwatch-rmg.html` (v2.6.2 вычистил только актуальный агрегатор + его standalone). Файлы никуда не отправляются | 🔒 Эльбик-gate — чистить только по слову owner'а |
| RUTV-137 | Телепрограмма на «Программах» (правка Марго 12.08, #614227): сетка — демо, вечерний прайм собран из заявленных времён программ; реальную программу передач пришлёт редакция | 🔒 заказчик |
| RUTV-138 | Соцсети у эфира (правка Марго 12.08): глифы VK/OK/MAX набраны типографикой в кругах — заменить официальными знаками при имплементации (та же рельса, что RUTV-133); ссылки на сообщества пришлёт редакция | open |
| RUTV-139 | «Ностальгия» — рабочее название вкладки подборок по годам (Марго 12.08: «нужно подумать, как она может называться. Давай назовем ее пока „Ностальгия“») | 🔒 заказчик |
| RUTV-140 | PiP-окошко: перенос в углы работает мышью и пальцем (pointer events); свайп-жест с инерцией как в VK Видео — при имплементации на реальном плеере | open |

**v2.6.2 (2026-07-22, Saved 605435/605436)** — SHAMAN исключён полностью (owner): демо-слот №1 = Сергей Лазарев «Шёпотом» (9 текстовых вхождений: hero/PiP/канал/клипы/чарт №1/артисты/новость/видео; dur 3:01), hero/PiP/backdrop-кадр `image 1.png` (кадр «Я русский») → `assets/rutv/hero-lazarev-shepotom.jpg` (кадр @85s официального клипа «Шепотом»); все остальные ассеты аудированы поштучно — Шамана на них нет. Standalone пересобран чистым. Коммит `8349d92`.

**v2.5.1 (2026-07-17, Saved msg 603106)** — доводка по фидбеку owner'а: (а) LIVE-карточка рубрики приведена к структуре клип-карточек (обложка 16:9 + подписи снизу; отличие — плашка LIVE + розовое кольцо), дизбаланс структур убран; (б) «лесенка» уточнена: bleed каруселей под край экрана — НОРМА (возвращён), выравнивание = единый ШАГ крупных рядов (Каналы/Промо/Рубрики/Новые клипы — 4 колонки, швы 284/682/1080/1478 бит-в-бит; Новости — 3 крупно); (в) RUTV-133 закрыт официальными векторами с rusradio.ru.

### Maximum — иконка «Магазин» для сайдбара (2026-07-16, чат DFM msg 602062 + бамп 602712; поставлено в Saved msg 602744 превью + 602745 SVG-пак)

Сайдбар maximum.ru декодирован с прода: иконки = Font Awesome 6 Solid (circle-play/compact-disc/heart/comment…), актив #FFD60A, покой #8E8E93 (fill-system-gray), фон #2C2C2E, атрибуты кнопок из SidebarButton.tsx. Сделаны 4 варианта той же FA-серии: A fa-bag-shopping (рекомендация) · B fa-store · C fa-cart-shopping · D fa-basket-shopping; превью в контексте сайдбара (место: между «Избранное» и «Контакты», ссылка shop.maximum.ru). Артефакты: `.scratch/rutv3/maximum_shop_icon_preview.html` + `maximum_shop_icons.png` + `maximum-shop-icons.zip`.

| ID | Задача | Статус |
|----|--------|--------|
| MXM-001 | 4 варианта иконки «Магазин» в стиле прода + превью + SVG-пак → Saved 602744/602745 | done |
| MXM-002 | Эльбик выбирает вариант и отвечает Стасу в DFM (Стас бампал 07-16: «А тут ничего не нашел?») | 🔒 Эльбик-gate |

Редизайн CMS dev.turbo-performance.ru в Liquid Glass стиле — для заказчика «Турбо Перформанс» (отдельный клиент от Twinr, пересобран стилевой язык 1-в-1 с Twinr LG). Single-file HTML + base64 standalone.

**Артефакты:**
- `designs/crm-glass.html` — primary, 230 KB
- `designs/crm-glass-standalone.html` — для заказчика, 934 KB (base64 backdrop)

| ID | Задача | Статус |
|----|--------|--------|
| CRM-001 | Аудит CMS: 4 раздела, 15+ экранов, rich-data таблица с 17 колонками | done |
| CRM-002 | Liquid Glass дизайн-система портирована (sunset backdrop тот же) | done |
| CRM-003 | Home dashboard: 4 KPI + activity feed (6 событий) + presence + quick actions | done |
| CRM-004 | Проекты: list + detail × 4 вкладки (Общая/Опции/Документы/Права) + edit | done |
| CRM-005 | Организации: list + detail × 3 вкладки (Реквизиты/Сотрудники/Документы) + new/edit | done |
| CRM-006 | Опции: list + new/edit | done |
| CRM-007 | Ресурсы опции — rich-data (17 колонок, 6 фильтров, column-toggle, bulk-actions, sort) | done |
| CRM-008 | Ресурс: new/edit (сложная форма с auto-compute ₽+НДС, radio-toggle Хронометраж/Символы) | done |
| CRM-009 | Ресурс: Создание материала + Файлы + Эфирные справки | done |
| CRM-010 | Библиотека: list (8 справочников) + item detail (Ресурсы с inline-add) + edit | done |
| CRM-011 | Документы (global) + Файлы опции + Справки опции (empty states) | done |
| CRM-012 | Права доступа: list + new (5 типов + cascade org→employee) | done |
| CRM-013 | Сотрудники: new + empty state | done |
| CRM-014 | Dropdowns: user-menu · notifications (5 шт, 3 unread) · kebab-меню | done |
| CRM-015 | Action column перемещена влево (после чекбокса) по UX | done |
| CRM-016 | Базовый стиль `.cell-link` (glob.) — тонкое coral-подчёркивание вместо браузерного default | done |
| CRM-017 | Standalone rebuild с inline base64 backdrop | done |
| CRM-018 | Показ заказчику — ждём первый фидбек | 🔒 Эльбик-gate |
| CRM-019 | Ревью: покрытие всех CMS-экранов, особенно empty states | 🔒 Эльбик-gate |
| CRM-020 | Responsive адаптация (mobile/tablet breakpoints) | 🔒 Эльбик-gate |
| CRM-021 | Тёмный/светлый переключатель темы (если попросят) | 🔒 Эльбик-gate |
| CRM-022 | Реализация в Next.js на базе утверждённой темы | 🔒 Эльбик-gate |
| CRM-023 | Интеграция с реальным API turbo-performance.ru | 🔒 Эльбик-gate |
