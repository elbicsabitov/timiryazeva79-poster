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
| PST-004 | Утвердить цвет с мамой | done (forest) |
| PST-005 | Файл для типографии | done (HTML референс + ТЗ) |
| PST-006 | Отправить заказ в типографию | done (20000₸, 3 раб.дня, ждём реквизиты) |
| PST-007 | Уведомление через eOtinish | pending |
| PST-008 | Фото перспективы фасада | pending |

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
