# Session 2026-04-29 — RU.TV витрина + Holy Grail + 2 варианта layout

## Контекст

Большая сессия с двумя крупными блоками:

**Блок 1 (Holy Grail)**: Эльбик скинул Anthropic Claude Design System Prompt (https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/Claude-Design-Sys-Prompt.txt) и попросил аудит наших методик + интеграцию как «holy grail». Я vendored полный 422-строчный системник + написал наш `docs/DESIGN_PROTOCOL.md` в 10 частях (brief questions / anti-slop / variations / starters / verifier / decks / React / deviations / gates) и зашил в `CLAUDE.md` + `RESUME_PROMPT.md` чтоб resume загружал автоматически.

**Блок 2 (RU.TV showcase)**: Эльбик попросил собрать HTML-витрину медиа-агрегатора в 2 версиях (стеклянной и Apple современной) на основе Figma + аудита Apple. Изначально я думал DFM (на основе Figma структуры с DFM mini-player), но Эльбик уточнил что **сайт для RU.TV** (Russian Music TV, часть РМГ) и есть **104 реальных ассета** в `~/Desktop/export rutv/` (image 1/2 hero shots, Rectangle 4322-{1..35} promo banners, unsplash files = логотипы партнёров, App Store/Google Play badges).

Прошли эволюцию от mock-content KZ-каналов (v1) → DFM брендинг с РМГ артистами (v2) → RU.TV красно-белый oval с реальными RU.TV ассетами и русскими артистами (v3) → production-ready polish + Light theme третий variant (v4) → второй файл-вариант **cinematic Apple-landing** (v5).

## Что сделано

### Holy Grail integration (commit 1398819)
- Vendored: `docs/references/anthropic_claude_design_prompt.md` (полный 422 строки, не редактируется)
- `docs/DESIGN_PROTOCOL.md` — 10 частей нашей адаптации
- `CLAUDE.md` — блок «🔑 HOLY GRAIL» с hard gates (запрет Inter/Roboto/Arial/Fraunces/system-ui, запрет aggressive gradients, запрет SVG-illustration, 3+ Tweaks вариаций в одном файле, brief questions для нового клиента, verifier subagent)
- `docs/RESUME_PROMPT.md` — оба файла обязательны на resume
- `.claude-memory/MEMORY.md` — pinned ссылки наверху
- Global memory `project_design_protocol.md` — переживёт смены сессий

### RU.TV Showcase v1 (commit 7b88eaa)
- `designs/showcase-aggregator.html` — single main HTML с переключателем стилей (Liquid Glass ↔ Apple) — Holy Grail compliant Часть 3.2
- Mock контент KZ-каналов (Хабар, Astana TV, КТК, 31 канал, Almaty, Qazaqstan, Евразия) + РМГ радио (Хит FM, Авторадио, Европа Плюс)
- Sticky bottom radio player (Spotify-pattern), sidebar 64→240 overlay, 4 row sections, hero, chip-row
- Anti-slop pass: шрифт Onest (НЕ Inter/Roboto), AA Normal, hit-targets ≥44px, focus-visible boost для TV
- Standalone 753 KB
- Headless screenshots verify через bash chrome.exe (chrome MCP не отвечал)
- Hero overflow fix (aspect-ratio 21/9 → 21/8 + max-height)

### RU.TV Showcase v3 — pivot на real RU.TV (commit 1c539e0)
- Эльбик уточнил: «делаем для RU.TV» + дал access к 104 ассетам в export rutv/
- Скопировал 87 PNG + 17 JPG в `designs/assets/rutv/`
- Бренд RU.TV: красно-белый oval `#E30033`, не абстрактный
- Hero carousel × 4: «Прямой эфир RU.TV» / «Звёзды Хайпа · LIVE Арена» / «Полевой» / «Статус: В сети» — все с реальными RU.TV promo images
- Каналы: RU.TV приоритет + Русское Радио ТВ + DFM TV + Maximum TV + Monte Carlo TV + Хит FM TV
- Радиостанции 8 + Сейчас слушают 6 = 14 cards
- **Чарт RU.TV top-10** русская сцена: SHAMAN, JONY, MIYAGI, Macan, HammAli, Полина Гагарина, Артур Пирожков, Слава Марлоу, Светлана Лобода, Дима Билан с реальными artwork и trend ▲▼
- 7 жанров, 8 артистов, 6 DJ, 6 mood gradients
- 7 клипов, 6 новостных карточек с real images
- **Расписание RU.TV** 7×7 = 49 цветных pill-cells (РМГ palette)
- Партнёры РМГ: 5 plates
- Footer с реальными адресами/телефонами RU.TV
- Build script extended: pattern matcher на JS-data ссылки
- Standalone 9.7 MB
- Visual verify через chrome MCP (real backdrop-filter работает)

### RU.TV Showcase v4 — production polish + Light theme (commit 0fa1f99)
Эльбик сказал «глянь все отступы и тему apple она будто вообще странная, в общем фулл аудит и сделай production ready топовый UX везде и UI» + позже «и сделай аудит белой темы что в фигме».

**Spacing rhythm fixes (через `tools/polish_v4.py`, 30/31 replacements):**
- row-section margin 38→56px (более air) + last 32px
- content padding-bottom 60→96px (не оверлапит player)
- hero overlay padding 36/44 → 44/52 (mobile 32/28)
- sidebar item 11/14 → 12/16 + min-height 44px
- topbar gap 18→20, padding 18→20px top
- chart-row 10→14px + subtle dividers между rows
- carousel scroll-padding для лучшего snap
- schedule cells 44→48 + text-shadow + box-shadow on hover
- footer gap 32→48, padding 24→32px top

**UX bugs fixed:**
- Sidebar mini-player: убрал always-visible pink play button → hover-only overlay
- Apple sidebar active: subtle white tint (rgba 0.10) вместо красного pill + 3px красный marker bar (Apple HIG)
- Hero card: solid bg + ::before pseudo для consistent overlay (z-index 2 на content)
- Hero title text-shadow для contrast поверх любого image
- Player shadow: 0.4→0.32 (subtle)
- Live badge: brand-coloured glow + tighter padding

**Apple Dark подтянут:**
- Sidebar более solid (rgba 0.55→0.78 + saturate(1.4))
- Cards solid bg (rgba 0.7→0.95)
- Active item: white tint + красный marker (НЕ розовый pill как Glass)

**Light theme добавлен (3-й вариант через `tools/add_light_theme.py`):**
- Apple Music Light style: bg `#f5f5f7`, cards `#ffffff`, text `#1d1d1f / #515154 / #86868b`
- White sidebar с subtle blur, active item: pink-tinted pill + 3px красный marker
- Topbar gradient белый, search/icon-btn rgba(0,0,0,0.05)
- Channel logos на white cards: dark `#1d1d1f` bg для readability
- Player text-primary dark, station mark accent красный
- Все text colors переопределены на dark на light bg (chart, news, schedule, footer, sidebar items)
- Tweaks теперь: Glass / Apple Dark / Light — три полноценных дизайн-системы в одном файле

**Bug fix Light theme:** удалил override `.btn-primary { background: dark }` для light — hero CTA должен оставаться white-on-dark (поверх hero overlay), иначе сливался с dark image.

### RU.TV Showcase v5 — cinematic второй вариант + media backdrop (commit 48fa5a1)

Эльбик: «сделай еще чтоб слева меню было изначально сложено и контент во весь экран как в Figma, в общем больше синематогрофичности и игры контентом как на сайтах продающих apple и что менюшка выезжала, хотя эти варианты тоже сохрани, в общем сделай 2».

Создан второй файл `designs/showcase-cinematic.html` — Apple TV+ landing вайб (рядом с dashboard, не replacement):

**Cinematic file спецификация:**
- Top-nav transparent → solid backdrop-filter при scroll (Apple TV+ pattern)
- **Off-canvas DRAWER sidebar** с overlay backdrop blur — выезжает по burger, ESC/overlay click закрывает
- **Full-screen hero 100dvh** с image 1.png (силуэт музыканта) bg
- Cinematic typography clamp(44-96px) на hero title
- Sections с reveal-on-scroll (IntersectionObserver fade-in transform)
- **Bento layout** для каналов: 1 featured огромный (grid 2/3, row 1/3) + 5 regular
- **Chart top-3** = portrait cards 1:1.15 с **96px цифрами 01-03** + остальные top-10 в clean list ниже
- **Artists horizontal carousel** с 280px round avatars (Apple Music style)
- **Bento mosaic** для жанров: wide tiles + regular grid
- Расписание week × hours c цветными pill-cells
- **Apple-style CTA** «Скачать приложение» с radial gradient backdrop + App Store / Google Play badges
- Footer 4-col grid (brand / platform / contact / social) + partners row + bottom-links
- Active nav-tab подсвечивается при scroll
- Все 3 темы: **Apple Dark default** / Glass / Light
- localStorage persist style: `showcase-cinematic.style`

**Изменения в обоих файлах (cinematic + dashboard):**
- Glass backdrop: убран Matterhorn sunset (горы) → `assets/rutv/image 1.png` (концертный кадр силуэт музыканта) — по теме music TV брендинга
- Carousels paddings: scroll-padding-left/right на row-track / chip-row / hero-track / artists-track — items больше не «прилипают» к краям
- Glass overlay сильнее (0.5/0.78/0.94 → 0.55/0.82/0.94) для контраста на новом dark backdrop

Build script extended: VARIANTS = [aggregator, cinematic]
Standalones: dashboard 10.3 MB, cinematic 4.5 MB.

## Решения и компромиссы

**Один main + Tweaks vs два отдельных файла** — Holy Grail Часть 3.2 говорит «один main + Tweaks», но это для **вариаций одного дизайна** (тёмная/светлая/coral). У меня 2 принципиально разных **layout philosophy**:
- Dashboard = постоянная sidebar + sticky player + dense rows
- Cinematic = full-bleed hero + scroll-driven sections + drawer
Это deviation per Часть 8 — оправдано, потому что переключение между ними одной кнопкой = два разных продукта.

**3 темы внутри каждого файла = compliance с Holy Grail** (Glass / Apple Dark / Light в Tweaks).

**FigMCP auth через chrome MCP trick** — изначально OAuth flow не работал ручной вставкой (state lost). Решение: navigate в auth URL через chrome MCP → Figma уже залогинен → авто-Authorize → localhost ловит callback → grab URL через `window.history.back()` → передаю в `mcp__FigMCP__complete_authentication`. Чисто отрабатывает.

**Chrome MCP ext не отвечал в начале сессии** — пришлось делать headless screenshots через bash `chrome.exe --headless --screenshot=...`. Это working альтернатива но не рендерит `backdrop-filter` (frosted glass blur невидим). Когда chrome MCP подключился — visual verify через real Chrome instance показал что backdrop-filter работает корректно.

**RU.TV vs DFM брендинг pivot** — изначально по Figma структуре «Главная» (mini-player + DFM logo + sidebar) я предположил что это DFM. Но Эльбик уточнил RU.TV (другой channel в РМГ). Вернул всё на красно-белый RU.TV oval, заменил artists на русскую сцену (SHAMAN top-1).

**Светлая тема не из Figma** — в Figma я нашёл только `component/header-view-white` (не page), все pages были dark. Поэтому Light theme сделал **best-in-class по Apple Music Light HIG**: bg `#f5f5f7`, text `#1d1d1f`, cards #ffffff с subtle shadow, brand red accent остаётся.

**Cinematic vs Dashboard — заказчик выбирает** — оба файла committed, оба собраны как standalone, оба читаются. Эльбик может выбрать после показа клиенту: dashboard для daily use vs cinematic для marketing/pitch. Можем потом combinate если надо.

**Footer-партнёры — простые text plates** (не SVG лого) — потому что на момент сессии я не вытащил отдельные SVG-лого из Figma. Текстовые plates читаются хорошо, но в финальной production версии нужно заменить на real лого партнёров (RUTV-012 в DEBT.md).

**Артисты используют клиповые artwork (Rectangle 4322-{16-26})** вместо отдельных портретов — потому что unsplash_*.png в export rutv оказались **логотипами партнёров** (Хит FM plate), не портретами артистов. Клиповые artworks выглядят музыкально и идентифицируемо. RUTV-013 — заменить на реальные portrait фото когда заказчик пришлёт.

**Onest шрифт vs Inter** — Holy Grail запрещает Inter/Roboto. Onest имеет полную кириллицу и характер. На случай если бренд RU.TV имеет brand guidelines с Inter (или другим шрифтом) — поменяем после уточнения у заказчика.

## Файлы (новые / модифицированные)

| Файл | Размер | Что |
|------|--------|-----|
| `docs/references/anthropic_claude_design_prompt.md` | 24 KB | Vendored Anthropic Design System Prompt (422 строки) |
| `docs/DESIGN_PROTOCOL.md` | 12 KB | Наш операционный протокол в 10 частях |
| `designs/showcase-aggregator.html` | 90 KB | **Dashboard** primary (3 темы Glass/Apple/Light) |
| `designs/showcase-aggregator-standalone.html` | 10.3 MB | Dashboard standalone (104 assets inlined) |
| `designs/showcase-cinematic.html` | 61 KB | **Cinematic** primary (3 темы) |
| `designs/showcase-cinematic-standalone.html` | 4.5 MB | Cinematic standalone |
| `designs/assets/rutv/` | ~9 MB total | 87 PNG + 17 JPG real RU.TV ассеты |
| `tools/build_showcase_standalone.py` | 3 KB | Build script (extended JS pattern matcher, 2 variants) |
| `tools/polish_v4.py` | 8 KB | Production polish одноразовый script |
| `tools/add_light_theme.py` | 5 KB | Light theme injection script |
| `designs/screenshots/showcase/v3_*` | ~2 MB | v3 verify (4 screenshots) |
| `designs/screenshots/showcase/v4_*` | ~3 MB | v4 verify (2 screenshots) |
| `designs/screenshots/showcase/cinematic_*` | ~2 MB | Cinematic verify (2 screenshots) |
| `designs/screenshots/showcase/v5_dashboard_glass_media_bg.png` | 691 KB | Dashboard glass с new media bg |
| `~/.claude/projects/.../memory/project_design_protocol.md` | 2 KB | Global memory entry |

## Что дальше

**Open RUTV-009..016 + новые items в DEBT.md:**

1. **RUTV-009** — Показ заказчику обоих вариантов + фидбек на направление (cinematic vs dashboard)
2. **RUTV-010** — Apple-style fidelity audit live (apple.com/tv-pr / Apple Music)
3. **RUTV-011** — Smart TV app mode (10ft viewing distance, focus-visible на всех cards, remote control)
4. **RUTV-012** — Замена «партнёров текст-plates» на реальные SVG лого (RU.TV, Русское Радио, DFM, MAXIMUM, Monte Carlo)
5. **RUTV-013** — Реальные portrait фото артистов вместо клиповых artwork (unsplash_*.png в export не подошли)
6. **RUTV-014** — Inner pages: Каналы list / Чарт top-100 / Полное расписание / Профиль артиста / Карточка клипа
7. **RUTV-015** — Реальный video player integration (HLS stream RU.TV) + audio player для радио
8. **RUTV-016** — Next.js + shadcn/ui реализация после утверждения стиля
9. **RUTV-017** — Mobile responsive deep audit (cinematic + dashboard на 375/414/768)
10. **RUTV-018** — Финальная brand check от RU.TV (шрифты, font-faces, real RU.TV brand guidelines)
11. **RUTV-019** — Performance audit (10 MB standalone — на slow connection долго грузится. WebP вместо PNG/JPG для assets)
12. **RUTV-020** — Apple HIG fidelity audit на cinematic (apple.com/tv-pr live audit через chrome MCP)

**Schedule predictive follow-ups:**
- через 1 неделю — узнать какой вариант выбрал заказчик
- по результату — Tier 2 development (inner pages, real video, brand guidelines integration)
