# DEBT — Дизайн-долг

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
| SC-012 | Wordstat — полный дизайн | pending |
| SC-013 | ИИ-аналитика — полный дизайн | pending |

## Компоненты

| ID | Задача | Статус |
|----|--------|--------|
| CP-001 | DESIGN.md — полная дизайн-система в markdown | pending |
| CP-002 | Responsive адаптация (mobile/tablet) | pending |
| CP-003 | Перенос в Figma (обновить РК экраны в тёмной теме) | pending |
| CP-004 | shadcn/ui component mapping | pending |

## Интеграция

| ID | Задача | Статус |
|----|--------|--------|
| INT-001 | Выбор финальной темы с заказчиком | pending |
| INT-002 | Next.js проект на базе выбранной темы | pending |
| INT-003 | MicroIT API интеграция | pending |
| INT-004 | DaData API для ИНН | pending |

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
| LG-009 | **Показ заказчику + фидбек/одобрение** | pending |
| LG-010 | Responsive адаптация (mobile/tablet breakpoints) | pending |
| LG-011 | Light theme (dawn) — опционально | pending |
| LG-012 | Figma перенос новой темы (обновить РК экраны) | pending |
| LG-013 | Backdrop picker (midnight / ocean / desert как варианты) | pending |
| LG-014 | Next.js + shadcn/ui реализация на базе утверждённой темы | pending |

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
| TURBO-009 | **Показ заказчику новых 9 экранов + Guide** | pending |
| TURBO-010 | Real data (MOS.RU, RUSSPASS и т.д. из Figma) вместо lorem ipsum | pending |
| TURBO-011 | Empty states для zero-data scenarios (пустая история, нет источников и т.п.) | pending |
| TURBO-012 | Mobile/tablet responsive для AI-модуля (chip-row → scroll, 2col → stack) | pending |
| TURBO-013 | Dynamic glass reactivity (саmtop-filter saturate on scroll) | pending |
| TURBO-014 | VoiceOver pass + контраст audit (WCAG AA) | pending |

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
| CUST-011 | Показ кастомайзера заказчику для выбора финальной фактуры/оттенка | pending |
| CUST-012 | После утверждения — зафиксировать глобальные glass-* токены на выбранной комбинации | pending |
| CUST-013 | Применить утверждённые токены ко ВСЕМ экранам (не только Руководство) | pending |
| CUST-014 | Figma sync: обновить компоненты в Figma на утверждённую фактуру | pending |
| CUST-015 | Удалить кастомайзер из production-сборки (оставить только для internal review) | pending |

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
| PST-008 | Фото перспективы фасада | pending |

### PST-007 Согласование с акиматом — детализация (ресёрч 2026-04-24)

Законы проверены: Закон РК «О рекламе» 508-II ст. 11 п. 1-1 (объявления «продаётся» НЕ входят в список исключений из рекламы), Правила наружной рекламы Алматы V23R0001724 (нет цветовых ограничений, согласование эскиза обязательно), Дизайн-код V23R0001751 п.6 (нет запрета на чёрный, но оценочная норма «несвойственных архитектурному стилю» — риск отказа по цвету).

**Услуга:** egov.kz → «Согласование размещения объектов наружной (визуальной) рекламы … областного и районного значения». Орган: Управление городского планирования и урбанистики Алматы (пр. Абая 90), через подразделение акимата Бостандыкского района.

**Плата:** 1 МРП/мес = 4 325 ₸ (площадь < 2 м²). КБК 105402. До подачи — оплатить первый месяц, далее — до 25 числа каждого месяца.

**Штрафы за размещение без согласования (физлицо, мама):** ст. 455 КоАП — 15–25 МРП (64 875 – 108 125 ₸); ст. 505 КоАП — 20 МРП (86 500 ₸); плюс демонтаж за свой счёт и доначисление платы. Первое нарушение часто — предупреждение, но на Тимирязева «любят кошмарить» (слова Арины).

| ID | Задача | Статус |
|----|--------|--------|
| PST-007a | Подготовить технический эскиз (PDF с размерами 1300×560 мм, HEX/Pantone, mock-up на фасаде) | pending |
| PST-007b | Оплата 4 325 ₸ через Kaspi → КБК 105402 (Бостандыкский район) | pending |
| PST-007c | Подать заявление на egov.kz под ЭЦП мамы (приложить эскиз + правоустанавливающий + чек) | pending |
| PST-007d | Ждать 5 рабочих дней, получить письмо-согласование | pending |
| PST-007e | При отказе — переделать эскиз (бежевый/серый вместо чёрного если причина п.6 дизайн-кода) | pending |
| PST-007f | Ежемесячная уплата 4 325 ₸ до 25 числа пока висит баннер | pending |

## RMG Smartwatch (5 станций)

| ID | Задача | Статус |
|----|--------|--------|
| SW-001 | Базовый прототип (5 тем, плеер, карусель) | done |
| SW-002 | Убрать историю эфира | done |
| SW-003 | Треки вместо подписей станций | done |
| SW-004 | Увеличить мелкие тексты для реальных часов | done |
| SW-005 | Подкасты: навигация подкаст→эпизоды→плеер | done |
| SW-006 | Избранное на подкастах/эпизодах | done |
| SW-007 | Ревью Stas/Alexei | pending |
| SW-008 | Остальные станции по брендбукам (PDF скачаны) | pending |

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
| KIN-012 | **Показ заказчику — Серёга/Катя/Настя** | pending |
| KIN-013 | Дождаться ответов Насти на 7 уточнений (статистика, IAABC, кейсы) | pending |
| KIN-014 | Подключить реальные CTA — форма заявки / Telegram | pending |
| KIN-015 | Добавить дату старта потока когда будет известна | pending |
| KIN-016 | Блок отзывов/кейсов когда получим от Насти | pending |
| KIN-017 | Mobile-тест на 375/768px | pending |
| KIN-018 | Реализация в Next.js после выбора финального варианта | pending |

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
| RUTV-009 | **Показ заказчику + фидбек на направление** | pending |
| RUTV-010 | Apple-style fidelity audit live (apple.com/tv-pr) | pending |
| RUTV-011 | Smart TV app mode (10ft viewing, remote control focus) | pending |
| RUTV-012 | Замена «РМГ» partner plates на реальные SVG лого | pending |
| RUTV-013 | Реальные portrait фото артистов вместо клиповых artwork | pending |
| RUTV-014 | Inner pages: Каналы list / Чарт top-100 / Расписание полное | pending |
| RUTV-015 | Реальные video player integration (HLS stream RU.TV) | pending |
| RUTV-016 | Next.js + shadcn/ui реализация после утверждения стиля | pending |

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
| RUTV-017 | Mobile responsive deep audit обоих вариантов (375/414/768) | pending |
| RUTV-018 | Финальная brand check от RU.TV (шрифты, font-faces, real RU.TV brand guidelines) | pending |
| RUTV-019 | Performance audit (10 MB standalone — на slow connection долго грузится. WebP optimization) | pending |
| RUTV-020 | Apple HIG fidelity audit на cinematic (apple.com/tv-pr live audit через chrome MCP) | pending |
| RUTV-021 | Заказчик выбирает: cinematic vs dashboard direction → дальнейший development идёт в выбранном направлении | pending |

## CRM Glass — Turbo Performance CMS (2026-04-22)

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
| CRM-018 | Показ заказчику — ждём первый фидбек | pending |
| CRM-019 | Ревью: покрытие всех CMS-экранов, особенно empty states | pending |
| CRM-020 | Responsive адаптация (mobile/tablet breakpoints) | pending |
| CRM-021 | Тёмный/светлый переключатель темы (если попросят) | pending |
| CRM-022 | Реализация в Next.js на базе утверждённой темы | pending |
| CRM-023 | Интеграция с реальным API turbo-performance.ru | pending |
