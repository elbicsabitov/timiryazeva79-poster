# DESIGN_PROTOCOL.md — Holy Grail рабочий протокол

> **Источник истины:** `docs/references/anthropic_claude_design_prompt.md` (полный системник Anthropic Claude Design, 422 строки).
> Этот файл — наша адаптация. **При любом расхождении наших правил с Anthropic — пере-проверь и возьми оттуда, если их подход лучше.** Это правило по умолчанию.
>
> **Обязательное чтение перед началом любой дизайн-работы.** Загружается автоматически в `resume design`.

---

## Ключевой принцип

Anthropic Design System Prompt = best-in-class методология для дизайн-артефактов на HTML. Их подход лучше там, где они спорят с нами. Наши локальные правила (FigMCP, chrome MCP, `tools/build_*_standalone.py`, `.claude-memory/`) — это инфраструктура; их правила — это **методология**. Сочетаем.

---

## Часть 1 — Workflow (как начинать любую дизайн-задачу)

### 1.1 Brief Questions Gate (обязательно для нового клиента / нового экрана >= 3 в существующем)

Перед написанием хоть одной строки HTML — задать **минимум 10 вопросов**. Цель: убрать угадывание.

**Обязательные блоки:**

1. **Output / Fidelity** — что именно нужно: статичный layout / hi-fi clickable prototype / animated video / deck / wireframe?
2. **Дизайн-контекст** — есть ли UI kit / design system / Figma / live URL / codebase / скриншоты? Если нет — попросить перед стартом. **Старт с нуля = LAST RESORT** (Anthropic явно).
3. **Brand assets** — лого, фотографии, цвета, шрифты — что уже есть, что нужно достать?
4. **Variations dimensions** — сколько вариаций и по каким осям: визуал? интеракция? копирайт? анимация? layout?
5. **Novelty appetite** — by-the-book paws-style или взрывные novel решения, или mix?
6. **Audience** — кто увидит первым? Заказчик / B2B презентация / конечный пользователь?
7. **Mobile-first** — нужен responsive сразу или desktop-first ок?
8. **WCAG bar** — AA Normal / AA Large / AAA?
9. **Real content vs lorem** — есть ли реальный контент, копирайт, цены, кейсы?
10. **Deadline + формат deliverable** — standalone HTML / GitHub Pages / Next.js handoff / PPTX / PDF?

Плюс **минимум 4 вопроса специфичных к задаче**.

**Когда МОЖНО пропустить:** мелкий tweak, follow-up на уже утверждённый дизайн, или пользователь дал всё нужное в первом сообщении.

### 1.2 Acquire design context

Прежде чем писать HTML:
- `list_files` → `designs/`, `designs/assets/`, `.claude-memory/`
- Если клиент существующий — прочитать предыдущие сессии в `.claude-memory/session_*.md`
- Если есть Figma — `FigMCP getStyles()` + `getNodes(root)` чтобы вытащить tokens
- Если есть live URL — `chrome MCP` + JS extraction (как делали с `paws.kz`, `my-dog.kz`)
- Если есть Telegram-бриф — Telethon (как `tools/read_obuchenie.py`)

**Никогда не строить «из головы» если можно достать реальные tokens.**

### 1.3 Plan + assumptions

Начать HTML-файл с блока «Assumptions / Context / Design reasoning» как junior показывающий manager'у. Placeholder'ы для секций. Показать заказчику РАНО, до полировки.

---

## Часть 2 — Anti-slop checklist (HARD GATE перед `done`)

Перед коммитом / отправкой заказчику пройти ВЕСЬ список. Каждый ❌ — блокер.

### 2.1 Шрифты (запрещены)

| ❌ Запрещено | ✅ Альтернатива |
|--------------|-----------------|
| Inter | Geist Sans, IBM Plex Sans, Söhne (комм.), Söhne Mono |
| Roboto / Roboto Bold | Onest, PT Root UI, Manrope, Aeonik (комм.) |
| Arial / Helvetica / system-ui | Söhne, Neue Haas Grotesk, GT Walsheim |
| Fraunces | Söhne Breit, Editorial New, Migra (комм.) |

Исключение: брендбук клиента явно требует. Тогда документируем в session log «использован Inter — требование brand guidelines файла X».

### 2.2 Визуальные тропы (запрещены)

- ❌ **Aggressive gradient backgrounds** (на всю секцию hero, переход через 3+ цвета)
- ❌ **Rounded card + left-border accent color** (коричневый код-блок паттерн)
- ❌ **Drawing imagery via SVG** когда нет реального ассета. Используй placeholder + попроси у заказчика реальный материал
- ❌ **Emoji** если бренд их не использует. Лучше placeholder
- ❌ **Data slop** — числа/иконки/статистика ради заполнения, без аналитической нагрузки
- ❌ **Filler content** — секции «лишь бы было». Anthropic: "1000 no's per yes"

### 2.3 Размеры

- Slide 1920×1080: текст **никогда меньше 24px**, идеально больше
- Print: минимум 12pt
- Mobile hit target: минимум **44px** (Apple HIG)

### 2.4 CSS правила

- ✅ `text-wrap: pretty` на параграфах, `text-wrap: balance` на заголовках
- ✅ CSS Grid для сложных layouts (не flexbox-водопровод)
- ✅ `oklch()` для harmony color если выходим за brand
- ✅ Concentric corners (внешний `r-xl 28` → внутренний `r-pill 999`)

### 2.5 Контент

- ✅ Перед добавлением новой секции — **спросить пользователя**, а не накидывать
- ✅ Убрать любой блок который не несёт смысла (декоративный progress-bar, fake stats)
- ✅ Антигаллюцинация pass — каждый факт сверить с источником (как делали с фамилией Сундеева)

---

## Часть 3 — Variations strategy

### 3.1 Когда делать N вариаций

**Цель:** дать заказчику mix-and-match, не «1 из 1».

- **3+ вариаций** на каждой релевантной оси (визуал / интеракция / layout / копирайт)
- **Mix by-the-book + novel:** первая вариация = классика, последняя = exotic. Между ними — нарастающая смелость
- Эксперименты с: scale, fills, texture, visual rhythm, layering, type treatments, новые метафоры

### 3.2 КАК хранить вариации (важно — Anthropic нас спорит)

Anthropic правило: **один main HTML файл с Tweaks**, НЕ N файлов под каждую вариацию.

**Почему:** заказчик не может смешать (paws-hero × glass-tariffs × material-FAQ если файлы разные). Любой fix = править N раз. Дрейф версий неизбежен.

**Наш текущий fail:** `themes/theme-pearl-violet.html`, `theme-warm-parchment.html`, `theme-fog-glass.html`, `theme-warm-luxury.html`, `theme-arctic-cyan.html`, `theme-ink-rose.html` — **6 файлов под одну дизайн-задачу**.

**Целевой паттерн:** один `twinr-full.html` + Tweaks panel (как Liquid Glass Customizer на `#page-guide` уже работает).

**Когда отдельные файлы оправданы:**
- Принципиально разные дизайн-системы (paws vs glass vs material — это 3 разных языка, не вариации одного)
- Разные клиенты в одном repo (kinolog ≠ twinr ≠ crm-glass)

### 3.3 Tweaks pattern

Floating panel в bottom-right (или sidebar) с переключателями:
- material / tint / shape / texture (как наш Customizer)
- сравнение тем
- live переключение копирайта (RU/EN)

**Persistence на диск (новое — берём у Anthropic):**

```js
const TWEAKS = /*EDITMODE-BEGIN*/{
  "primaryColor": "#FF9500",
  "fontSize": 16,
  "dark": false
}/*EDITMODE-END*/;
```

Скрипт `tools/persist_tweaks.py` (TODO) — читает текущее `localStorage` дамп и переписывает блок между маркерами в .html. Reload → выбор сохранён НА ДИСКЕ, не только в браузере заказчика.

---

## Часть 4 — Starter Components библиотека

**Принцип:** не рисуем bezels / shells / dropzones / sidebars руками каждый раз. Вытаскиваем из существующего в `starter/` и переиспользуем.

### 4.1 Что уже можно вытащить (TODO build)

| Component | Source | Назначение |
|-----------|--------|------------|
| `starter/lg-shell.html` | twinr-liquid-glass + crm-glass | Sidebar 64→240px overlay + topbar + routing |
| `starter/lg-modal.js` | twinr | Overlay+luminance-lift панель (Apple HIG) |
| `starter/lg-customizer.js` | twinr `#page-guide` | Material/tint/intensity panel + 6 пресетов |
| `starter/dropzone.js` | twinr (Турбо AI) | Drag-enter feedback (scale + glow) |
| `starter/sub-nav-chiprow.js` | twinr (AI hub) | Slide-morph indicator + group separators |
| `starter/deck-stage.js` | NEW (port из Anthropic) | 1920×1080 letterbox + keyboard nav + speaker notes |
| `starter/device-frame.js` | NEW | iOS / Android / browser bezels |
| `starter/lg-tokens.css` | twinr/crm | Liquid Glass design tokens (materials × tints × dim levels) |

### 4.2 Когда использовать

- Новый клиент в Liquid Glass стиле → `starter/lg-*` (не переписывать с нуля)
- Презентация для инвесторов / питч / Bereke KP → `starter/deck-stage.js` (не SPA на чистом hash-routing)
- Mobile mockup → `starter/device-frame.js`

### 4.3 Когда писать с нуля

- Принципиально новая дизайн-система (Material 3, Vercel-style, Linear-style — не наш LG)
- Эксперимент / спайк / sketch

---

## Часть 5 — Verification (verifier-agent flow)

### 5.1 Не делать самому

❌ **Не тратить контекст основного автора на скриншоты + WCAG проверки + console-probe.**

### 5.2 Использовать subagent

После завершения работы — вызвать `compound-engineering:design:design-implementation-reviewer`:
- Скриншоты всех экранов
- WCAG contrast audit
- Layout / typography / spacing проверки
- Console errors
- Mobile breakpoints (375 / 768 / 1024)

Возвращается отчёт. Чинить найденное. Не звать второй раз пока не пофикшено.

### 5.3 Direct check для конкретного запроса

Если заказчик / Эльбик просит «проверь spacing на hero» — звать `design-implementation-reviewer` с focused task, не делать chrome MCP screenshot вручную.

---

## Часть 6 — Specialized formats

### 6.1 Decks / презентации (Silkway pitch, Bereke KP, инвесторы)

**Сейчас:** обычные SPA на hash-routing — нет speaker notes, нет print-to-PDF, scaling костыли.

**Целевой паттерн (Anthropic):**
- Fixed canvas 1920×1080 + `transform: scale()` + letterbox на чёрном
- prev/next контролы **снаружи** scaled элемента (чтобы работали на маленьких экранах)
- `<deck-stage>` web component (portable starter)
- Speaker notes:
  ```html
  <script type="application/json" id="speaker-notes">
    ["Slide 0 notes...", "Slide 1 notes...", ...]
  </script>
  ```
- `data-screen-label="01 Title"` на каждом slide для navigation overlay (1-indexed!)
- localStorage persist текущего slide
- Print-to-PDF (один slide = одна страница)

### 6.2 Animated content (видео / motion)

Anthropic использует свой `animations.jsx` (Stage + Sprite + scrubber + Easing + interpolate).

Наша альтернатива: **Popmotion** (`https://unpkg.com/popmotion@11.0.5/dist/popmotion.min.js`) или CSS transitions. Если задача motion-heavy — порт стартера в `starter/animations.jsx`.

### 6.3 Standalone HTML (single-file для заказчика)

Уже работает — `tools/build_*_standalone.py` инлайнит base64. Anthropic подтверждает: "Save as standalone HTML — Single self-contained file that works offline" — наш паттерн правильный.

### 6.4 PPTX / PDF handoff

Anthropic skills: «Export as PPTX (editable)», «Save as PDF». У нас сейчас вручную через print → PDF. TODO: добавить `tools/html_to_pptx.py` (через `python-pptx`, с extraction text/shapes из наших HTML).

---

## Часть 7 — React + JSX гигиена (когда уйдём в Next.js)

Anthropic правила (применять на handoff в `INT-002` / `CRM-022` / `KIN-018`):

### 7.1 Style object naming

❌ **Никогда** `const styles = {...}` — collisions при импорте >1 компонента.
✅ `const terminalStyles = {...}` — unique-prefixed по имени компонента, или inline styles.

### 7.2 Pinned versions для React + Babel

Для inline JSX в HTML использовать **именно эти script tags с integrity hashes** (см. anthropic_claude_design_prompt.md строки 65-69):
```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
```

### 7.3 Cross-script scope

Каждый `<script type="text/babel">` = свой scope. Чтобы делиться компонентами:
```js
Object.assign(window, { Terminal, Line, Spacer, ... });
```

### 7.4 Не использовать

- ❌ `scrollIntoView` — может ломать препрев
- ❌ `type="module"` на script imports — ломает Babel
- ❌ Файлы > 1000 строк — split на отдельные .jsx + import в main

---

## Часть 8 — Что мы НЕ берём (и почему)

Не всё применимо к нашей среде. Документируем deviations:

| Anthropic feature | Почему не берём |
|-------------------|-----------------|
| `questions_v2` tool | Их платформенный tool. У нас — обычный диалог в чате с Эльбиком, brief-questions в виде checklist'а |
| `done` / `fork_verifier_agent` системные | У нас — `compound-engineering:design:design-implementation-reviewer` agent (наш аналог) |
| `copy_starter_component` tool | У нас — папка `starter/` + `cp` руками |
| `EDITMODE-BEGIN/END` host writeback | Хост этого нет — пишем `tools/persist_tweaks.py` вручную |
| `window.claude.complete` | Доступно только в их песочнице. Для live AI demo используем Anthropic SDK через бэк (как paws-helper) |
| `<mentioned-element>` blocks | У нас комментарии живут в Telegram / голосовом — не в DOM |
| `snip` tool для context management | У нас — `/compact`, естественные паузы, ручной reset |

---

## Часть 9 — Чек-лист перед `done` (gate)

Перед тем как сказать «готово, вот файл заказчику»:

- [ ] Brief Questions пройден (для нового / >3 экранов)
- [ ] Дизайн-контекст загружен (FigMCP / chrome MCP / Figma file / live URL)
- [ ] Anti-slop checklist (часть 2) — все ❌ устранены
- [ ] Шрифты: НЕ Inter/Roboto/Arial/Fraunces (или есть документация исключения)
- [ ] Variations: 3+ если применимо, в виде Tweaks (не отдельных файлов)
- [ ] Hit targets ≥ 44px (mobile), text ≥ 24px (slide), ≥ 12pt (print)
- [ ] WCAG: AA Normal минимум, проверено через design-implementation-reviewer или JS contrast script
- [ ] Антигаллюцинация: каждый факт/цена/имя сверен с source (telegram-чат, Figma, live URL)
- [ ] Standalone собран если делаем для заказчика (`tools/build_*_standalone.py`)
- [ ] `localStorage` для UI state (last-route, last-tab, customizer)
- [ ] Speaker notes если deck (формат Anthropic)
- [ ] design-implementation-reviewer agent вызван и его findings закрыты

---

## Часть 10 — Принцип «when in doubt, check Anthropic»

Если возник дизайн-вопрос которого нет в этом протоколе — **сначала** проверь `docs/references/anthropic_claude_design_prompt.md`, **потом** действуй. Их методология победит наши инстинкты в 80% случаев.

Если Anthropic явно лучше — обнови этот протокол + сделай как они.

Если наш подход обоснованно лучше (например `tools/build_*_standalone.py` vs их Save-as-standalone skill) — задокументируй deviation в Часть 8.

---

**Last updated:** 2026-04-29
**Source:** [Anthropic Claude Design System Prompt](https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/Claude-Design-Sys-Prompt.txt) (vendored as `docs/references/anthropic_claude_design_prompt.md`)
