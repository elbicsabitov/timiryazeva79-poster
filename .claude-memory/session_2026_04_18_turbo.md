# Session 2026-04-18 (evening) — Турбо AI-модуль + Apple HIG refinement + Guide

Продолжение дневной сессии (см. `session_2026_04_18.md` — Liquid Glass редизайн РК).

## Контекст

Заказчик дал 2 новых запроса:
1. Есть Figma с экранами продукта «Турбо перформанс» (9 AI-инструментов) — нужно адаптировать их в наш Liquid Glass стиль, не трогая существующие 13 экранов «Большой Цифровой»
2. Всё это должно жить внутри вкладки «ИИ» в sidebar — единый модуль, по Apple HIG

Плюс финальные штрихи:
- Отдельная страница «Руководство» с длинным текстом и идеальной читаемостью
- Максимально подробный sync + пересобранный standalone для показа

## Что сделано

### Интеграция 9 экранов из Figma

Figma file: `dev`, секции `Библиотека источников`, `Библиотека промптов`, `Транскрибация`, `Работа с источником`, `Wordstat`, `Documents`, `Генерация видео`, `Рерайтинг по источникам`, `Чат`.

Все 9 экранов реализованы в `designs/twinr-liquid-glass.html`:

| Экран | `id` | Особенности |
|-------|------|-------------|
| Библиотека источников | `page-sources` | Форма нового источника + group-tabs с edit/delete + checkbox grid 4col + bulk actions + pagination |
| Библиотека промптов | `page-prompts` | Left aside: тип+название+текст. Right: 4 type-tabs (анализ/отбор/обработка/служебный) + chip list |
| Работа с источником | `page-source-work` | 3 input modes (Ручной/Документ/Ссылка) + история chips + output |
| Рерайтинг | `page-rewrite` | Форма + модалка источников + модалка промпта + таблица результатов |
| Транскрибация | `page-transcribe` | Left: dropzone 340px. Right: file history chips + output text + copy btn |
| Чат | `page-chat` | Form: название+модель+запрос+отправить. Right: chat history chips с trash icon |
| Генерация видео | `page-video-gen` | Textarea + video-placeholder (16:9 coral dashed) с play button и timer |
| Документы | `page-docs` | Full-width t-table 6 cols + tag-cell (pills + add) + модалка тегов |
| Ключевые слова | `page-keywords` | filter-strip (period pills) + 2 tabs (Данные/Графики) + 3 модалки kw + bar-chart-v |

### 5 модалок (overlay + panel)

- `modal-edit-group` — переименование группы источников
- `modal-rewrite-sources` — выбор источников для батч-рерайтинга (tabs групп + cbgrid)
- `modal-rewrite-prompt` — выбор/редактирование отборочного промпта
- `modal-tag-select` — 12 тегов с pagination + add + delete
- `modal-keywords` — 2 режима (Ручной ввод / Анализ аудио-видео) + dropzone

Общие паттерны:
- Overlay `rgba(10,4,18,0.42)` + backdrop-blur (мягко, не агрессивно)
- Panel **luminance lift**: gradient 14%→3% white поверх `--glass-regular` + strong specular rim top
- ESC + click-outside закрывают
- Focus auto на primary action при открытии

### Apple HIG refactor (sidebar = 4 пункта, ИИ как hub)

Первая версия добавила 9 items в sidebar под Турбо section — перегруз. Отрефакторил:
- Sidebar вернулся к 4 items (Рекламный кабинет / Статистика / Wordstat / ИИ)
- Все 9 AI-экранов доступны через sub-nav chip-row внутри ИИ-модуля
- Sidebar-клик по ИИ запоминает последний открытый инструмент через `localStorage['twinr-last-ai-tool']`
- `routeToNav`: все AI pages мапятся на `'ai'` → sidebar ИИ подсвечивается на любом AI-экране
- Breadcrumb динамический: «Twinr / ИИ — Источники», «Twinr / ИИ — Рерайтинг» и т.д.

### Discovery Hub на странице ИИ

Landing ИИ-модуля. 4 семантические группы × карточки:

- **Контент**: Источники · Промпты (2)
- **Генерация**: Работа с источником · Рерайтинг · Чат (3)
- **Медиа**: Транскрибация · Генерация видео (2)
- **Анализ**: Документы · Ключевые слова (2)

Карточка: coral-tinted icon 44px + title (17px headline) + desc (13px ink-3) + arrow-чиплет на hover. Hover — translateY(-3px) scale(1.005) с glass-thick + stronger shadow.

Вместо плоских 9 чипов теперь 4 визуальных кластера. Apple HIG: max 5-7 сегментов на уровне.

### Sub-nav (chip-row) — iOS 26 GlassEffectContainer pattern

- `.tabs.tabs-wide` — full-width контейнер с horizontal scroll, чипы inside
- **Slide-morph indicator**: абсолютно-позиционированный `.chip-indicator` физически скользит между активными чипами через `translateX + width` transition 380ms glass ease
- **Group separators** `.chip-sep` (1px vertical line, rgba(255,255,255,0.14)) между 4 группами
- ResizeObserver пересчитывает позицию индикатора при ресайзе окна
- `aria-current="page"` на активном чипе → screen reader корректно объявляет

### Дополнительные Apple HIG улучшения

1. **Sidebar tooltips**: custom glass-popover появляется справа от иконки при hover на свёрнутом sidebar. Delay 350ms (iOS-native). `data-tooltip` attribute.
2. **Destructive confirm dialog**: `askConfirm({title, message, confirmText})` создаёт ленивую модалку с `btn-danger` (red gradient) + `btn-glass` cancel. ESC + click-outside закрывают. Focus auto на OK.
3. **Button loading state**: при клике на `.btn.btn-primary` добавляется `.is-loading` + вставляется `.btn-spinner` на 1100ms (симуляция async).
4. **Dropzone drag-enter**: `.is-over` class на dragenter/dragover — scale 1.005, coral border 2px, outer glow shadow 5px.
5. **Hit-targets**: `.tc-edit` в Документах увеличен с 22×22 до 32×32 (Apple min).
6. **aria-label** на `<nav>` и модалках.

### Страница «Руководство» — long-form reading

5-й пункт sidebar (иконка книги). `page-guide`.

**Типографика по Apple HIG для чтения:**
- Body 17px / line-height 1.7 / letter-spacing -0.003em / max-width 64ch
- Lead 19px bold ink-1 с border-bottom separator
- h2 26px / 1.22 / -0.024em, margin 56/18
- h3 19px / 1.32 / -0.016em, margin 34/10
- ordered list: coral marker ::marker pseudo

**Компоненты:**
- **Glass reading panel** (как Safari Reader / Apple Books): `glass-regular` + `blur-regular` + border + shadow — backdrop не просвечивает через текст
- **Callout boxes** (Совет / Важно): coral-tinted left-border accent 3px + icon box + label uppercase + body ink-1
- **kbd** элементы: monospace pill с dark bg + inset shadow bottom
- **Sticky TOC** справа 248px: 9 секций, scroll-spy через `getBoundingClientRect` + `requestAnimationFrame`, активная секция — `.is-active` с coral left-border + light bg
- **Smooth-scroll** по клику TOC (НЕ меняет hash → не триггерит route())
- Responsive <1080px: TOC прячется, article 700px max

Content: 9 секций × параграфы про использование каждого модуля. Реальный helpful текст, не lorem ipsum.

### Standalone (1.6 MB)

Пересобран через Python: `sunset-backdrop.jpg` (525 KB) encoded в base64, оба вхождения `url('assets/...')` заменены на `url('data:image/jpeg;base64,...')`. 0 внешних зависимостей (только Google Fonts CDN для Inter).

## Ключевые решения и почему

### Sidebar 4 items vs 12 items
Первая итерация добавила Турбо как отдельную section (9 items). Это нарушало Apple HIG (3-7 top-level destinations). Вернул 4 items → ИИ стал hub с внутренней sub-навигацией. Паттерн Apple Settings / iOS Shortcuts.

### 9 tools как 4 группы vs 9 плоских чипов
9 плоских сегментов = overload. Apple HIG: max 5-7 сегментов в segmented control. Кластеризация по назначению (Контент/Генерация/Медиа/Анализ) даёт парсинг 4 групп вместо 9 items.

### Slide-morph indicator vs class toggle
Обычный class toggle на active — статичный web-чекбокс. Apple iOS 26 segmented control физически сдвигает highlight между segments. Реализовано через absolute `.chip-indicator` с `translateX + width` transitions. Ощущение премиум.

### Chip-row на всех AI-страницах vs только на ИИ
Chip-row injected JS-ом после section-hero на каждой AI-странице (включая сам ИИ-hub). Это даёт contextual persistence: пользователь всегда видит где в модуле он находится + может быстро переключиться.

### Luminance lift для модалок
Первоначально модалки были темнее фона (overlay 62% + panel glass-thick 50% = двойное затемнение). Apple HIG: модалки *светлее* dimmed фона (feel lit from above). Заменил panel bg на gradient 14%→3% white over glass-regular + bright specular rim top.

### Guide как glass panel vs прозрачный text
Текст поверх Matterhorn фото нечитабелен даже через backdrop-filter. Обернул article в glass-regular панель — читается как Safari Reader. Max-width 64ch внутри панели — идеальная длина строки.

### Standalone через Python vs ручная замена
Python script надёжнее (не пропустить occurrence), воспроизводим, auto-checks. Это зафиксировано в расширенном SYNC_PROMPT.md как обязательный шаг.

## Файлы

| Файл | Размер до | Размер после | Дельта |
|------|-----------|--------------|--------|
| `designs/twinr-liquid-glass.html` | ~175 KB (2445 строк) | ~305 KB (4675 строк) | +74% |
| `designs/twinr-liquid-glass-standalone.html` | 1.5 MB | 1.6 MB | +100 KB |
| `docs/SYNC_PROMPT.md` | 39 строк | ~180 строк | расширенный протокол |
| `DEBT.md` | 83 строки | ~108 строк | +Турбо блок |
| `.claude-memory/MEMORY.md` | 22 строки | ~25 строк (после sync) | +session ref |

## Что дальше

- **TURBO-009**: Показ заказчику — отправить standalone + список новых экранов в виде чеклиста (см. Discovery Hub карточки для быстрой демонстрации)
- **TURBO-010**: Заменить mock-контент (lorem ipsum) на реальные новости из Figma (Chertanovo Football, MOS.RU и т.д.)
- **TURBO-012**: Mobile breakpoints для AI-модуля (сейчас <1280px — table overflow, chip-row scrolls, 2col stacks)
- **TURBO-014**: Accessibility audit — VoiceOver pass + WCAG AA contrast на coral/ink-2 парах

Все pending pending → проверять с заказчиком после показа.

## Инструменты сессии

- Claude Code (primary — Opus 4.7 с 1M context)
- FigMCP (9 секций + все варианты экранов + модалки)
- claude-in-chrome MCP (live preview + visual audit 15+ screenshots)
- Python (standalone rebuild)
- skill: `everything-claude-code:liquid-glass-design` (Apple HIG reference)
- skill: `superpowers:using-superpowers`
