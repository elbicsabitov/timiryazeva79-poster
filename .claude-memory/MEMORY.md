# Memory — Twinr Design

## 🔑 Holy Grail (всегда читать первым)

- `docs/DESIGN_PROTOCOL.md` — наш операционный протокол по дизайну (10 частей)
- `docs/references/anthropic_claude_design_prompt.md` — first-source Anthropic Claude Design System Prompt (vendored 2026-04-29)
- При сомнениях — сверяться с anthropic prompt, брать оттуда если лучше

## Sessions

- [session_2026_04_15.md](session_2026_04_15.md) — Первая сессия: полный дизайн РК "Большой Цифровой"
- [session_2026_04_16.md](session_2026_04_16.md) — Постер «Продаётся» Тимирязева 79: ресерч законов, дизайн, GitHub Pages
- [session_2026_04_18.md](session_2026_04_18.md) — Liquid Glass редизайн РК: Apple iOS 26 через FigMCP, photo backdrop, 13 экранов по структуре оригинала
- [session_2026_04_18_turbo.md](session_2026_04_18_turbo.md) — Турбо AI-модуль: 9 экранов из Figma + Discovery Hub + Guide + Apple HIG refinement
- [session_2026_04_18_customizer.md](session_2026_04_18_customizer.md) — Liquid Glass Customizer: 38 droplet-капель на Руководстве + plug-in panel (material/tint/intensity/dim/shape/texture + 6 presets)
- [session_2026_04_20.md](session_2026_04_20.md) — Cross-project: чтение фидбека Harvid для bereke-kp через Telethon, TODO сохранён в paws-kp, аудит SYNC_PROMPT (5 гэпов)
- [session_2026_04_22.md](session_2026_04_22.md) — **CRM Glass**: полный прототип CMS dev.turbo-performance.ru в Liquid Glass стиле (29 экранов, 230 KB + 934 KB standalone)
- [session_2026_04_24.md](session_2026_04_24.md) — **PST-007 ресёрч**: процедура eOtinish/egov для постера Тимирязева 79, факт-чек 3 законов, штрафы, разбивка на 6 подзадач + скрипт `tools/read_arina.py`
- [session_2026_04_24_kinolog.md](session_2026_04_24_kinolog.md) — **Лендинг «Обучение кинологов»**: 3 варианта (paws / glass / material) для курса Анастасии Сундеевой под брендом Paws.kz. Контент из Telegram-чата через Telethon, стиль из FigMCP, 48 блоков ТЗ сверены, WCAG AA Large, standalone-файлы собраны
- [session_2026_04_29_rutv_cinematic.md](session_2026_04_29_rutv_cinematic.md) — **Holy Grail integration + RU.TV showcase v1→v5**: Anthropic Design System Prompt vendored + DESIGN_PROTOCOL.md в 10 частях; RU.TV витрина-агрегатор с 104 реальными ассетами, чарт top-10 русской сцены, расписание week×hours, 3 темы (Glass/Apple Dark/Light) + cinematic второй вариант (Apple TV+ landing с full-screen hero, off-canvas drawer, bento layouts, scroll reveal). 2 файла на руках: dashboard 10MB + cinematic 4.5MB

## Current Design Iteration

### Клиент: RU.TV (Russian Media Group) — 2026-04-29 ⭐ ACTIVE

**Два production-ready варианта на руках, заказчик выбирает направление:**

**Dashboard (для daily use):**
- `designs/showcase-aggregator.html` (90 KB, 11 секций)
- `designs/showcase-aggregator-standalone.html` (10.3 MB, 104 ассета inlined)
- Sidebar 256px постоянно видим, sticky bottom radio player
- Sections: Hero / Каналы / Радио / Сейчас слушают / Чарт top-10 / Жанры / Артисты / DJ / Mood / Клипы / Новости / Расписание / Партнёры / Footer

**Cinematic (для marketing/pitch):**
- `designs/showcase-cinematic.html` (61 KB)
- `designs/showcase-cinematic-standalone.html` (4.5 MB)
- Off-canvas drawer sidebar (выезжает по burger), top-nav transparent → solid при scroll
- Full-screen hero 100dvh с Apple TV+ typography (clamp 44-96px)
- Bento layouts (channels + genres), portrait chart top-3 с 96px цифрами, artists carousel 280px round
- Apple-style CTA «Скачать приложение» с radial gradient
- Scroll-driven reveal-on-view fade-in

**3 темы в обоих файлах** (Holy Grail compliant — Tweaks panel переключатель):
- **Glass** — concert dark backdrop (image 1.png силуэт, НЕ горы), grey-tinted glass с blur, brand red accent, sunset removed
- **Apple Dark** — pure black `#000`, dynamic blur от hero artwork, white CTA, max contrast `#f5f5f7`
- **Light** — Apple Music Light style: `#f5f5f7` bg, `#ffffff` cards, `#1d1d1f` text, brand red accent, subtle shadows

**Бренд:** RU.TV красно-белый oval `#E30033` + 1.5px white inner ring, Onest шрифт (НЕ Inter/Roboto per Holy Grail).

**Контент (real RU.TV):**
- Каналы: RU.TV приоритет, Русское Радио ТВ, DFM TV, Maximum TV, Monte Carlo TV, Хит FM TV
- Радио РМГ: Русское Радио, RU.TV Music, DFM, Maximum, Monte Carlo, Хит FM, Русское Ретро, Радио Шансон
- Чарт RU.TV top-10: SHAMAN #1, JONY #2, MIYAGI&Andy Panda #3, Macan, HammAli&Navai, Полина Гагарина, Артур Пирожков, Слава Марлоу, Светлана Лобода, Дима Билан
- Жанры: Поп-Хиты, Шансон, Танцы, Рок, Дискотека 80-х, Ретро, Лирика
- Расписание 7 дней × 7 часов = 49 цветных pill-cells
- Партнёры РМГ: 5 plates с подписями
- Footer: реальные адреса/телефоны RU.TV, Russian Media Group bottom

**Real assets** в `designs/assets/rutv/` — 104 файла из `~/Desktop/export rutv/` (image 1.png hero силуэт музыканта, image 2.png сериал «Полевой», Rectangle 4322-{1..35} promo banners + клиповые artwork, App Store/Google Play badges, RUTV 2 logo).

**Build script:** `tools/build_showcase_standalone.py` extended pattern matcher на JS-data ссылки, VARIANTS = [aggregator, cinematic] — одна команда собирает оба standalone.

**Verified через chrome MCP** (real backdrop-filter работает): все 3 темы в обоих файлах, drawer cinematic с overlay backdrop blur, scroll reveal, mobile/TV viewports.

### Клиент: Twinr (Большой Цифровой)
**Active prototype:** `designs/twinr-liquid-glass.html` (~267 KB, ~4990 строк, **22 страницы** + 5 модалок + **Liquid Glass Customizer** на #page-guide)
**Client-facing standalone:** `designs/twinr-liquid-glass-standalone.html` (**1.7 MB**, base64 backdrop inline, открывается двойным кликом без сервера)

### Клиент: Paws.kz / курс кинологов (Лендинг) — 2026-04-24
**Active prototypes:**
- `designs/kinolog-paws.html` (40 KB, 125 KB standalone) — основной paws-брендинг с оранжевым градиентом
- `designs/kinolog-glass.html` (42 KB, 851 KB standalone с Matterhorn backdrop) — Liquid Glass + paws accent, белое лого
- `designs/kinolog-material.html` (48 KB, 133 KB standalone) — Material 3 + paws accent CTA

**Клиент:** Paws.kz (наш проект). Курс ведёт **Анастасия Сундеева** (@AnastassiyaSun, не «Солнышкина» как я изначально написал — галлюцинация). 9 лет практики с 2016, IAABC Member, Ассоциация Гуманных Кинологов, DogScienceClub, KZ+USA. Её действующий персональный сайт: `my-dog.kz` (оттуда вытащил фото и настоящую фамилию). Гуманный подход, современные исследования.

**3 тарифа:**
- Теория 200 000 ₸ (для зоопомощников Paws — 180 000 ₸)
- Теория + Практика 400 000 ₸ (350 000 ₸)
- Индивидуальный 750 000 ₸

**Структура лендинга (9 секций, все согласованы с чатом «Обучение»):**
1. Hero: «Обучение кинологов — теория онлайн, практика в Алматы»
2. 3 сегмента аудитории (Понять свою собаку / Освоить профессию / Углубиться)
3. 6 карточек возражений («А мне подходит?»)
4. 5 модулей программы (accordion): Знания специалиста / Базовая работа / Методы / Работа с клиентом / Поведение и дрессировка
5. Тарифы (3 карточки, средняя featured)
6. Автор (Анастасия + фото + 4 бейджа IAABC/Ассоциация/DogScience/KZ+USA)
7. FAQ (8 вопросов)
8. Финальный CTA
9. Footer

**Источники данных:**
- `.claude-memory/obuchenie_kinolog.txt` — приватный дамп Telegram-чата «Обучение», gitignored, 610 сообщений, 106 матчей
- `.claude-memory/kinolog_landing_brief.md` — структурированный бриф (48 блоков сверены с чатом)
- `.claude-memory/paws_figma_tokens.md` — полный design system из Figma (paints/text/effects/grid)
- `.claude-memory/kinolog_landing_audit.md` — финальный аудит (визуал/UX/WCAG/галлюцинации/логика)

**Инструменты:**
- `tools/read_obuchenie.py` — Telethon скрипт, заимствует auth у mama-helper
- `tools/build_kinolog_standalone.py` — инлайнит assets в base64 для standalone

**FigMCP токены Paws.kz (из файла `dev`):**
- Primary orange `#FF9500`, gradient `#FF9500→#FFBF66` @196°
- Full tonal scale, 6 gradients, 3 alerts, gray scale 1-9
- Inter для всего, Roboto Bold для H2
- Shadow button: `4px 8px 24px rgba(255,149,0,.25)`

**WCAG фикс:** `#FF9500` vs white = 2.43 (fail). Заменено на `#EB6400→#FF9500` gradient + text-shadow = AA Large. Eyebrow `#FF9500` на peach = 1.87 → заменено на `#B85A00` = AA Normal.

**Assets:**
- `designs/assets/paws/logo.png` — настоящий логотип с paws.kz
- `designs/assets/paws/logo-glass.png` — белая версия с ~/Desktop/paws logo glass/
- `designs/assets/paws/anastasia.webp` — фото Анастасии с my-dog.kz

### Клиент: Turbo Performance (CRM Glass) — 2026-04-22
**Active prototype:** `designs/crm-glass.html` (230 KB, 4306 строк, **29 экранов** + 4 модалки)
**Client-facing standalone:** `designs/crm-glass-standalone.html` (934 KB, base64 backdrop inline)
**Sidebar:** 5 пунктов (Главная · Проекты · Организации · Документы · Библиотека) + Выйти в footer
**Разделы (29 экранов):**
- Home: KPI x4 + activity feed (6 событий) + presence + quick actions + pinned
- Проекты: list + detail × 4 вкладки (Общая/Опции/Документы/Права) + edit + delete-modal
- Опции: list + new + edit (+удаление)
- Ресурсы опции: rich-data таблица 17 колонок (вкл. checkbox + actions слева), column-toggle, 6 фильтров, sort, bulk-bar, total row
- Ресурс: new/edit (auto-compute ₽ с НДС, radio Хронометраж/Символы)
- Ресурс: Создание материала (dropzone) + Файлы + Эфирные справки
- Опция: Общая таблица файлов + Справок
- Организации: list + detail × 3 вкладки + new + edit
- Сотрудник: new (ФИО/Должность/Email/Телефон)
- Документы global: empty
- Библиотека: list (8 справочников) + item detail (inline-add) + edit элемента
- Права доступа: list + new (5 типов + cascade org→employee)
**Эстетика:** тот же Liquid Glass — sunset backdrop (Matterhorn + clouds), coral/amber/rose акценты, grey-tinted glass (НЕ фиолетовый), pill/squircle radii (iOS 26 concentric), spec-rim specular highlights. Adapted 1-в-1 с Twinr.
**Dropdowns:** user-menu (Профиль/Настройки/Помощь/Выйти), notifications (5 шт с coral pulse на unread), kebab ⋮ на rows (Создание/Файлы/Справки/Дублировать/Удалить).
**Routing:** hash-based `#page-X`, localStorage persist `crm-glass.last-route`.

**Sidebar — 4 пункта (Apple HIG):**
1. Рекламный кабинет (admin) — `page-advertisers` + вложенные (add, details, campaign, bind)
2. Статистика — `page-stats` + `page-stats-clips` + `page-stats-detail`
3. Wordstat — `page-wordstat` (placeholder)
4. ИИ — hub для 9 AI-инструментов через chip-row sub-nav
5. Руководство — `page-guide` (long-form docs)

**ИИ-модуль (внутри одной вкладки):**
Discovery Hub на `#page-ai` (4 группы × карточки). Под-навигация chip-row на каждой AI-странице со slide-morph indicator, group separators между Контент/Генерация/Медиа/Анализ.

9 AI-инструментов:
- Контент: `page-sources`, `page-prompts`
- Генерация: `page-source-work`, `page-rewrite`, `page-chat`
- Медиа: `page-transcribe`, `page-video-gen`
- Анализ: `page-docs`, `page-keywords`

**Плюс промо/auth**: `page-promo`, `page-login`, `page-register` (оригинал, не тронуты).

**Эстетика:** Apple iOS 26 Liquid Glass — translucent grey glass `#333333 @ 0.28-0.50`, heavy backdrop-blur 16-48px, gradient border white `0.4→0.32`, uniform top rim specular `inset 0 1px 0 rgba(255,255,255,0.4)`, **coral accent `#FF8A6E`** (НЕ розовый из Figma — сознательно сохранена сессия #18 палитра), warm photo backdrop (Matterhorn + clouds + sunset from Unsplash CC0).

**Customizer (page-guide):** Live-preview переключатель material (clear/ultra/thin/regular/thick/chrome) × 12 Apple system tints × intensity 0-32% × dim 0-40% × shape (pill/rounded/squircle/organic) × texture (smooth/frosted/grain/linen/prism). 6 пресетов (Apple/Sunset/Ocean/Forest/Mono/A11y). State в `localStorage: twinr.lg.customizer`. Copy-CSS кнопка экспортит актуальные glass-tokens. **38 droplet-капель** вместо одного монолитного контейнера — каждый параграф/список/callout = свой backdrop-filter слой.

**Модалки:** overlay `rgba(10,4,18,0.42)` + **luminance lift** на panel (gradient 14%→3% white over glass-regular + strong specular top rim) — панель СВЕТЛЕЕ dimmed фона (Apple HIG).

**Apple HIG features:**
- Slide-morph indicator в sub-nav (translateX + width, 380ms glass ease)
- Sidebar tooltips на свёрнутом состоянии
- Destructive confirm dialog (red btn + cancel glass)
- Button loading state (spinner 1100ms) для primary CTAs
- Dropzone drag-enter feedback (scale + glow)
- aria-current, aria-label, role="alertdialog"
- Hit-targets ≥32px (Apple min)
- Concentric corners (outer r-xl 28 → inner r-pill 999)

**Предыдущие итерации:**
- `designs/twinr-full.html` — индиго/SaaS baseline (оригинал заказчика, до Liquid Glass)
- `designs/themes/theme-*.html` (6 цветовых вариантов) — explore до Liquid Glass
- Начальная Liquid Glass версия без AI-модуля (в session_2026_04_18.md)

**Backdrop assets:**
- `designs/assets/sunset-backdrop.jpg` — primary (Matterhorn above clouds, 525 KB)
- `designs/assets/dusk-lake.jpg` — backup alt (327 KB)

**Routing:** hash-based (`#page-X`), localStorage для last-route + last-ai-tool. Детали в `docs/RESUME_PROMPT.md` и `docs/SYNC_PROMPT.md`.

## Правила sync

См. `docs/SYNC_PROMPT.md` (расширенный протокол): 8 шагов, обязательная пересборка standalone при изменении primary, структурированный conventional commit, summary для клиента.
