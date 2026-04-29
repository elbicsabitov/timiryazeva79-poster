# CLAUDE.md — Twinr Design System (Рекламный кабинет Большой Цифровой)

## 🔑 HOLY GRAIL — обязательное чтение перед любой работой

**ПЕРЕД любым действием в этом проекте прочитать:**
1. `docs/DESIGN_PROTOCOL.md` — наш операционный протокол (10 частей)
2. `docs/references/anthropic_claude_design_prompt.md` — first-source Anthropic Claude Design System Prompt

**Принцип:** при любом дизайн-вопросе которого нет в нашем протоколе — сверяться с anthropic prompt. Если их подход лучше — берём оттуда + обновляем `DESIGN_PROTOCOL.md`. Это поведение по умолчанию, не спрашивать разрешения.

**Hard gates** (перед `done`/коммитом/отправкой заказчику):
- ❌ Запрещены шрифты: Inter, Roboto, Arial, Helvetica, Fraunces, system-ui (если нет brand guidelines exception)
- ❌ Запрещены: aggressive multi-stop gradient backgrounds, rounded card + left-border accent, SVG-drawn imagery вместо placeholder, эмодзи вне brand
- ✅ 3+ вариаций как Tweaks в одном файле, не N отдельных файлов
- ✅ Brief Questions Gate (10+ вопросов) для нового клиента / >=3 новых экранов
- ✅ Verifier через `compound-engineering:design:design-implementation-reviewer` agent (не вручную скриншоты)
- ✅ Antigallusinatsiya pass — каждый факт сверен с source
- ✅ Полный чек-лист: `docs/DESIGN_PROTOCOL.md` Часть 9

## Project

UI/UX дизайн-система для рекламного кабинета "Большой Цифровой" — модуль платформы Twinr (AIGate). Аналитика радиорекламы: рекламодатели, кампании, ролики, статистика прослушиваний, Wordstat, ИИ-аналитика.

**Owner:** elbics (solo designer + developer)
**Branch:** `master` (direct push)

## Stack

| Layer | Tech | Purpose |
|-------|------|---------|
| Prototypes | **HTML/CSS/JS** | Standalone SPA-прототипы (single-file) |
| Design System | **CSS Custom Properties** | Токены для dark/light тем |
| Target | **Next.js + shadcn/ui** | Будущая реализация |
| Figma | **FigMCP** | Дизайн-макеты, темы, компоненты |
| API | **MicroIT** | Данные по радиорекламе |

## Architecture

```
designs/
├── twinr-full.html        ← Победитель (indigo, 13 экранов, dark/light toggle)
├── themes/                ← 6 цветовых тем (полные SPA-копии)
│   ├── theme-pearl-violet.html    (light-first, лавандовый)
│   ├── theme-warm-parchment.html  (light-first, янтарь)
│   ├── theme-fog-glass.html       (light-first, slate navy)
│   ├── theme-warm-luxury.html     (dark-first, чёрное золото)
│   ├── theme-arctic-cyan.html     (dark-first, неон голубой)
│   └── theme-ink-rose.html        (dark-first, hot pink)
└── archive/               ← Ранние варианты (Linear, Vercel, Sentry, etc.)
```

## Экраны (13 штук)

| # | Экран | Роль | ID в SPA |
|---|-------|------|----------|
| 0 | Промо-лендинг | Все (до логина) | page-promo |
| 1 | Регистрация | Все | page-register |
| 2 | Логин | Все | page-login |
| 3 | Статистика — кампании + KPI | User/Admin | page-stats |
| 4 | Ролики кампании | User/Admin | page-stats-clips |
| 5 | Детали ролика (10 колонок) | User/Admin | page-stats-detail |
| 6 | Рекламодатели — список | Admin | page-advertisers |
| 7 | Добавить рекламодателя | Admin | page-add-advertiser |
| 8 | Карточка рекламодателя (3 вкладки) | Admin | page-advertiser-details |
| 9 | Создание кампании | Admin | page-create-campaign |
| 10 | Привязка ролика | Admin | page-bind-clip |
| 11 | Wordstat (placeholder) | Все | page-wordstat |
| 12 | ИИ (placeholder) | Все | page-ai |

## Дизайн-система (Twinr Native)

### Dark Theme (default)
| Token | Value |
|-------|-------|
| bg-page | #0F1113 |
| bg-card | #1a1c1f |
| bg-sidebar | #0a0c0e |
| border | #2e3238 |
| text-primary | #ffffff |
| text-secondary | #9ca3af |
| accent | #6366F1 (indigo) |
| accent-hover | #818CF8 |
| success | #34d399 |
| warning | #fbbf24 |
| danger | #f87171 |

### Light Theme
| Token | Value |
|-------|-------|
| bg-page | #F5F6F8 |
| bg-card | #FFFFFF |
| bg-sidebar | #FFFFFF |
| border | #E2E4E9 |
| text-primary | #111827 |
| text-secondary | #6B7280 |
| accent | #6366F1 |
| accent-hover | #4F46E5 |

## Sidebar

- 64px свёрнут → 240px overlay на hover
- Иконки всегда видны, подписи появляются при раскрытии
- Не сдвигает контент (position: fixed, z-index: 100)
- Пункты зависят от роли (Admin видит "Рекламный кабинет")
- Переключатель тем (sun/moon) в sidebar

## Бизнес-логика (из ТЗ docx)

### Рекламодатели (Admin)
- Добавление по ИНН (DaData автоподгрузка)
- Поля: Название*, ИНН*, КПП*, ОГРН, Расч.счёт*, Орг.форма*, Адрес, Телефон, Email
- Фильтры по орг.форме (ООО, АО, ЗАО, ИП, НКО, АНО)
- Карточка: 3 вкладки (Реквизиты, Кампании, Ролики)

### Рекламные кампании
- Создание: Название* + Описание
- Сроки — автоматически из дат выхода роликов (MicroIT API)
- Статусы: Активна / Запланирована / Завершена (автоматически по датам)
- Привязка роликов по ID (подтягивается из API)

### Статистика (User + Admin)
- Шаг 1: Выбор периода
- Шаг 2: Список кампаний с фильтрами + суммарные прослушивания
- Шаг 3: Список роликов кампании
- Шаг 4: Детальная статистика ролика (по выходам)
- Данные: прослушивания, уникальные, дослушали до конца, изменение %
- Пагинация по 50

### Wordstat + ИИ (future)
- Транскрипция роликов
- Ключевые слова
- Графики и рекомендации

## Figma

Файл: `dev` (FigMCP подключен)
- Экраны РК: 4406:333 — 4406:758 (10 экранов, белая тема, устаревшие)
- Темы Twinr: 4412:322 — 4412:506 (10 цветовых тем)
- Компоненты: Sidebar, TopBar, Tabs, Cards, Tables

## Session Protocol

### resume design / подхвати дизайн

1. **cd** в `~/Desktop/design-project`
2. **git pull** + check status
3. **Load:** CLAUDE.md, .claude-memory/MEMORY.md
4. **Read DEBT.md** — что висит
5. **Продолжай работу** — не жди подтверждения

### sync design / сохрани дизайн

1. **Commit** all changes
2. **Update** .claude-memory/ (session log, knowledge base)
3. **Update DEBT.md**
4. **Push**
5. **Report** — что сделано, что дальше

## Security (Design Context)

### Безопасные инструменты
- FigMCP getNodes/viewNode/getStyles (read-only)
- design-implementation-reviewer (read-only)
- frontend-patterns (чистые паттерны)
- Свой DESIGN.md (контролируемый)

### С осторожностью
- figma-design-sync (пишет в Figma — только свои файлы)
- design-iterator (только свои скриншоты)
- Внешние DESIGN.md — только из проверенных источников (52K+ stars)

### Запрещено
- Внешние DESIGN.md из неизвестных репо
- MCP серверы < 1K stars
- upsertNodes на чужих файлах

## ISOLATION RULE

This project is COMPLETELY SEPARATE from paws-kz and stalker-extraction.
- NEVER read/write files from other projects
- NEVER load other project CLAUDE.md or memory
- Each project = its own universe
