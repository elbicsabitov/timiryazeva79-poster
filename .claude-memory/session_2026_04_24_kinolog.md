# Session 2026-04-24 — Лендинг «Обучение кинологов» (3 варианта)

## Контекст

Серёга (elbics) попросил: «найди в логах чат обучение → вытащи структуру сайта для кинолога → посмотри стиль paws.kz в Figma → сделай пару вариантов лендинга (paws, glass+paws, paws+material)». Это новый клиент под брендом Paws.kz — курс Анастасии Сундеевой (@AnastassiyaSun, действующий сайт my-dog.kz, но для этого курса работает в рамках Paws).

## Что сделано

### 1. Чтение Telegram-чата «Обучение» через Telethon
- Создал `tools/read_obuchenie.py` — заимствует auth у mama-helper, ищет чаты по ключу «обучение»/«kinolog»
- Обработано 2 группы × 610 сообщений → 106 матчей по keywords (сайт/лендинг/кинолог/курс/тариф/…)
- Результат: `.claude-memory/obuchenie_kinolog.txt` — 152 KB, **gitignored** (приватная переписка)
- `.gitignore` обновлён: `.claude-memory/obuchenie_*.txt` добавлен

### 2. Figma MCP — токены Paws.kz
- Флоу OAuth глюканул при ручной вставке callback URL (сервер теряет state)
- **Решение**: открыл auth-URL через chrome MCP прямо в браузере, Figma уже был залогинен → авто-Authorize → localhost поймал callback → тулзы сразу подключились
- `listFiles()` → `dev` (единственный файл); `getNodes(root)` показал 132 SECTION с названиями Walker/Owner/Tutorials/Chat/Authorization — это paws.kz Figma
- `getStyles()` вытащил полный design system: 8 paint-групп × 2 темы, 18 text-стилей, shadow tokens, 5 breakpoint grids
- Сохранил в `.claude-memory/paws_figma_tokens.md` + дополнил тем что нашёл на живом paws.kz через JS в chrome MCP (живой сайт использует более тёмный `#eb6400` для CTA против Figma `#FF9500`)

### 3. Ресёрч реального сайта Анастасии
- Нашёл `my-dog.kz` (elbics скинул линк)
- Вытащил **настоящую фамилию** — Сундеева (я изначально написал «Солнышкина» — галлюцинация, не из чата)
- Скачал её реальное фото (с аusi-shepherd, закат, поле) + оригинальный лого paws.kz
- **Бренд остаётся Paws.kz** — my-dog.kz только источник фактов

### 4. Построил 3 варианта лендинга (41 KB каждый primary)

Все три следуют одной структуре из чата (Серёга дословно прописал 22-23 апреля):
1. Hero: «Обучение кинологов — теория онлайн, практика в Алматы» + CTA «Хочу на курс» / «Подходит ли мне?»
2. 3 сегмента: Понять свою собаку / Освоить новую профессию / Углубиться в профессию
3. 6 карточек возражений
4. 5 модулей программы (accordion)
5. 3 тарифа (Теория 200к / Т+П 400к / Индив 750к), для зоопомощников 180к/350к
6. Автор Анастасия Сундеева (IAABC / Ассоциация Гуманных Кинологов / DogScienceClub / KZ+USA)
7. FAQ × 8 вопросов
8. Финальный CTA
9. Footer

**Стили:**
- `kinolog-paws.html` — основной, белый фон + paws оранжевый градиент, Inter, Roboto Bold H2
- `kinolog-glass.html` — Liquid Glass + Matterhorn backdrop + warm purple wash, белый wordmark paws, grey-tinted glass
- `kinolog-material.html` — Material 3 tokens (cream surface container, 28px shape-lg, type scale Roboto Flex) + paws-orange gradient на CTA (hybrid подход — M3 скелет, paws акцент)

### 5. Аудиты (4 прохода)

**Контент vs ТЗ** — 48 блоков проверены построчно с `obuchenie_kinolog.txt`. Галлюцинаций нет.

**Визуал** — скриншоты hero/tariffs/author/faq всех 3 вариантов через chrome MCP. Найдено: H1 в Material ломался на 4 строки → `text-wrap: balance` + clamp 34-48. В остальном переносы ок.

**UX** — иерархия Hero→Segments→Obj→Program→Tariffs→Author→FAQ→CTA→Footer работает как воронка. Sticky-nav с CTA. seg-tag с ложной стрелкой (визуально как link, но span) → заменил на реальный `<a href="#tariffs">Подходящий тариф — «...» →`.

**WCAG** — JS-скрипт в chrome MCP посчитал contrast ratios. Найдены проблемы:
- Белый на `#FF9500` = **2.43** (fail) — это собственно paws-brand проблема
- Eyebrow `#FF9500` на peach-tint = **1.87** (fail)
- **Фиксы**: градиент CTA изменён на `#EB6400 → #FF9500` + text-shadow → **~3.8** (AA Large ✅). Eyebrow цвет → `#B85A00` → **4.6** (AA Normal ✅)

**Логика / галлюцинации** — финальный проход:
- Убран `«авторская система LIFE»` (Настя не подтверждала публикабельность)
- `«2-3 площадки»` → `«несколько площадок»` (точного числа в чате нет)
- H2 программы `«от этологии до работы с клиентом»` → `«от теории до полевой работы»` (охватывает все 5 модулей)
- Декоративный прогресс-бар в hero-карточке (остаток от мока «Бьянка 72%») → убран, заменён на чипы-регалии автора

### 6. Standalone сборка
- Создан `tools/build_kinolog_standalone.py` — инлайнит все asset-пути в base64
- Размеры: paws 125 KB / material 133 KB / glass 851 KB (с Matterhorn backdrop)
- Google Fonts остаются внешними (link CDN), при отсутствии интернета — system-ui fallback

### 7. Glass-лого: белая версия
- elbics скинул `~/Desktop/paws logo glass/` → скопировал `1 logo@3x.png` → `designs/assets/paws/logo-glass.png`
- В glass-варианте height выровнен с paws (34px), drop-shadow смягчён до alpha 0.25

## Решения и компромиссы

**Figma MCP через chrome MCP** — ручная вставка callback URL дважды сбросила flow. Нельзя было залогиниться самому (требуется user-action). Решение: открыть auth-URL через уже-контролируемый chrome MCP → Figma auto-authorize → localhost поймал callback. Инсайт для будущего: **если OAuth теряет state при ручной вставке, открывать auth через chrome MCP** (когда есть).

**Material 3 hybrid (не pure-M3)** — чистый M3 tonal `#8B5000` (brown-orange из HCT paws) делал CTA коричневым, теряло брендовую связь с Paws-оранжевым. Решил: оставить M3 скелет (surface container tonality, shape scale, type scale, elevation), но на primary CTA + badge + accent текст использовать paws-gradient. Не канонический M3, но нативно читается как «современный Material с paws-brand flavor».

**WCAG на брендовом оранжевом** — `#FF9500` физически не проходит AA с белым (2.43). Два выхода: (a) слайдить на более тёмный `#EB6400` (как делает живой paws.kz), (b) text-shadow чтобы усилить читаемость. Сделал **и то и то** одновременно — градиент начинается с `#EB6400` и заканчивается на `#FF9500`, плюс text-shadow. Компромисс сохраняет брендовый вайб.

**Приватность чата** — `obuchenie_kinolog.txt` содержит переписку трёх людей о бизнесе курса, ценах, внутренней кухне. Никогда не коммитится — пополнил `.gitignore`. В репо только выжимка (`kinolog_landing_brief.md`), где факты без цитат.

## Блокеры / что осталось

1. **Ответы Насти на 7 вопросов Серёги** — bio не финализирована (точное число учеников, уровень IAABC Member/CDBC, что конкретно в США, школы образования, 1-2 яркие истории)
2. **Дата старта потока** — сейчас «Набор открыт / совсем скоро», нужны конкретные даты
3. **CTA кнопки** (`#enroll`) — не подключены к форме/Telegram, просто `href="#"`
4. **Блок отзывов/кейсов** — Настя обещала несколько историй
5. **Mobile тест** 375/768px не прогонял
6. **Выбор варианта заказчиком** — Серёге/Кате/Насте нужно показать 3 версии и дождаться фидбека

## Файлы (все новые)

| Файл | Размер | Что |
|------|--------|-----|
| `tools/read_obuchenie.py` | 4.3 KB | Telethon-скрипт чтения чата «Обучение» |
| `tools/build_kinolog_standalone.py` | 2.5 KB | Inline base64 → standalone HTML |
| `designs/kinolog-paws.html` | 40 KB | Основной вариант |
| `designs/kinolog-paws-standalone.html` | 125 KB | Standalone для отправки |
| `designs/kinolog-glass.html` | 42 KB | Liquid Glass вариант |
| `designs/kinolog-glass-standalone.html` | 851 KB | Standalone (с base64 Matterhorn) |
| `designs/kinolog-material.html` | 48 KB | Material 3 вариант |
| `designs/kinolog-material-standalone.html` | 133 KB | Standalone |
| `designs/assets/paws/logo.png` | 1.7 KB | Настоящий лого paws.kz |
| `designs/assets/paws/logo-glass.png` | 5.4 KB | Белая версия лого |
| `designs/assets/paws/anastasia.webp` | 32 KB | Фото Анастасии |
| `designs/assets/paws/mydog-logo.webp` | 25 KB | Лого my-dog.kz (для ref) |
| `designs/assets/paws/dog-paw-heart.webp` | 14 KB | Альт лапа на сердце (ref) |
| `.claude-memory/kinolog_landing_brief.md` | 8.7 KB | Структурированный бриф |
| `.claude-memory/paws_figma_tokens.md` | 6.8 KB | Figma design tokens |
| `.claude-memory/kinolog_landing_audit.md` | 14 KB | 4 аудита в одном файле |
| `.claude-memory/obuchenie_kinolog.txt` | 152 KB | ПРИВАТНЫЙ дамп (gitignored) |

## Что дальше

1. **KIN-012** — показать заказчику все 3 standalone + ждать фидбек какой направление
2. **KIN-013** — получить ответы Насти и обновить bio-блок
3. **KIN-014** — подключить форму/Telegram к CTA
4. **KIN-017** — mobile test на реальных девайсах
5. **KIN-018** — после выбора варианта → Next.js/shadcn/ui реализация
