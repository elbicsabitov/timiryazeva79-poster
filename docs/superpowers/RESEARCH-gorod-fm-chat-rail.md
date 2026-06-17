# RESEARCH — Город ФМ: персистентный док-рейл чата (Twitch-style), интеграция в shell

> **Раунд:** FORM FACTOR + multi-page integration.
> **Дополняет** (НЕ дублирует): `docs/superpowers/RESEARCH-gorod-fm-ubiquitous-chat.md` — там уже зафиксированы IA, семантика комнат, AI/human-toggle, модерация-MVP, per-route таблица присутствия чата. Здесь — ТОЛЬКО форм-фактор док-рейла и его проводка в существующий app-shell.
> **Решение владельца (supersedes the bubble):** плавающий пузырь `.ai-dock` ОТКЛОНЁН. Чат — постоянная, видимая на каждой странице, сворачиваемая КОЛОНКА справа (как Twitch). Глобальный «Общий эфир» + per-station комнаты с самого старта. Сегментированный composer-toggle `[✦ Twinr / 👥 Всем]`. Анонимные хэндлы `guest_NNNN`.
> **Grounding-файл:** `designs/gorod-fm.html` (проверено живьём — все номера строк/токены ниже сверены).

---

## 0. Поправки к дослье (что в исследовании было неверно — и как здесь исправлено)

Шесть дослье прошли adversarial-верификацию против кода. Применяю каждый `must_fix`, выбрасываю выдуманную точность:

| Заявлено в дослье | Факт в `gorod-fm.html` | Что делаем |
|---|---|---|
| `.ai-dock` на строке 719, 384px | стр. 719 = `.why-pop` (поповер «Почему играет»). Реальный `.ai-dock` — **стр. 2840, width 388px, height 560px, z 96** | Трогаем стр. 2840. `.why-pop` НЕ трогаем |
| grid уже «как Twitch sibling» | grid = `var(--sidebar-w) 1fr` (стр. 277); sidebar **`position:fixed`** над gutter (стр. 348/451), не in-flow трек | Рейл — НОВЫЙ настоящий третий grid-трек. «main reflows» сегодня НЕ бесплатно |
| sidebar collapse 240→72px | у gorod sidebar нет 72px-режима (240px фикс). 64→240px — это ДРУГОЙ продукт (twinr ad-cabinet) | НЕ сворачиваем sidebar в 72px. При тесноте сворачиваем РЕЙЛ |
| breakpoints 1280/1100/600 | реальные: **1280/1024/768/640/560/480/360**; `.ai-dock` mobile-рестайл на **480px** (стр. 3132) | Ключим состояния к 1024 / 640 |
| rail-width «340px (Twitch-validated)» | Twitch — переменная/resizable ~300–360px, не константа. Текущий dock = 388px | 360px — НАШЕ дизайн-решение (не «потому что Twitch») |
| `--miniplayer-h` | реальный токен **`--player-mini-h: 72px`** (стр. 138); sidebar уже `calc(100dvh - var(--player-mini-h))` (стр. 452) | Зеркалим существующую идиому |
| #5168FC как акцент-текст | стр. 128: `#5168FC` = 4.25:1 на near-black → **НЕ для текста**; токен текста = `--accent-on-dark #8094ff` (6.8:1), light = `#3A4ED0` | #5168FC только нетекстовая полоса/индикатор; весь Twinr-текст → `--accent-on-dark` |
| message-list = `aria-live=polite` | в файле уже **~15 polite-регионов** («почему»-чеки, taste-delta, np-transition, ai-ribbon, сам `.ai-msgs`) | `role=log` + управляемая politeness, НЕ наивный always-on polite (см. §9) |
| collapse-to-bar / theater-overlay «как Twitch» | Twitch сворачивает в тонкий edge-handle и прячет колонку; «Cinema» у нас = ТЁМНАЯ ТЕМА, не видео-театр | Collapse-to-spine — НАШЕ требование владельца («всегда виден»), не Twitch-факт. Никакого video-overlay |
| port logic «verbatim» | `.ai-dock` — модалка: focus-trap, Escape-close, launcher, breathe-on-speak | Логика данных/composer/toggle/undo переносится; контейнер-семантика ПЕРЕПИСЫВАется (не модалка на desktop) |
| ЛЮДЯМ | в коде и в брифе — **`👥 Всем`** (стр. ~13022) | Везде `Всем` |

---

## 1. Executive summary — тезис

**Постоянный Twitch-style рейл справа на каждой контентной странице — это не «социалка поверх музыки», а витрина позиционирования «не чёрный ящик».** Город ФМ обещает объяснимое радио («почему этот трек»), правки вкуса голосом/текстом и живой Twinr-профиль. Если Twinr живёт в плавающем пузыре, который надо нажать, — он невидим, и обещание «прозрачности» опровергается самим UI. Если Twinr живёт в **постоянной колонке**, где `[✦ Twinr / 👥 Всем]` всегда на виду, а каждый ответ ИИ помечен бейджем и несёт конкретную причину из профиля, — прозрачность становится физически наблюдаемой на каждом экране. Рейл превращает «почему этот трек» в общий социальный референт: люди в «Общем эфире» и per-station комнатах обсуждают то же now-playing, что объясняет Twinr.

**Но рынок честно говорит: always-EXPANDED чат в listening-app отвлекает.** Spotify к янв 2026 выпустил Messages + групп-чаты до 10 + live Friend Activity (~40M юзеров / 340M сообщений) — и всё равно держит это как OPT-IN инбокс, в который ВХОДЯТ, а не колонку на каждом экране. Apple Music чата не имеет вовсе. Character.AI в 2025 УБРАЛ human-in-room (mixed always-on чат деградирует). Отсюда честная позиция: **строим рейл ровно как хочет владелец (постоянный, не пузырь), но по умолчанию EXPANDED только на социальных якорях (`#/lives`, `#/home`), а на остальных контентных маршрутах — свёрнут в видимый spine.** «Видимый на каждой странице» соблюдён (spine виден всегда), внимание слушателя защищено, wedge не разбавлен.

**Главный интеграционный риск, уникальный для Город ФМ (которого нет у Twitch):** рейл (вертикальный персистентный chrome) и mini-player (горизонтальный персистентный chrome) перпендикулярны и дерутся за низ экрана. Рейл ОБЯЗАН заканчиваться над mini-player (`height: calc(100dvh - var(--player-mini-h))`), как уже делает `.sidebar`. Это #1 интеграционная задача.

---

## 2. Дистилляция 6 измерений (steal / avoid)

### 2.1 Анатомия рейла (rail-anatomy) — Twitch/Discord/Slack/YouTube
- **STEAL:** фиксированная по ширине колонка-СИБЛИНГ (не overlay); контент reflows уже, а не прячется за пузырём. Универсальная 3-зонная анатомия: sticky header / flex-grow scroll-список (единственный скроллер, auto-pin к низу + «N новых» pill) / sticky composer.
- **AVOID:** не переиспользовать плавающий `.ai-dock`; не `position:absolute`/overlay в открытом состоянии (перекрывает now-playing/визуализатор на `#/home`); не давать всему рейлу скроллиться единым блоком (теряются composer/toggle).
- Источники: FrankerFaceZ #819, SirStendec «Twitch New Channel Layout», Twitch channel-page guide, Discord collapsible panes, Stationhead live-room, Kick moderation.

### 2.2 Персистентность через multi-page shell (multipage-persistence)
- **STEAL:** рейл рендерится как СИБЛИНГ `#app`, НИКОГДА внутри swap-нутого `[data-page]`. Один инстанс на весь lifecycle. Collapse-by-WIDTH (анимировать grid-track к 0/spine), НЕ by-unmount. Room-switch = swap ДАННЫХ в один инстанс (как YouTube miniplayer грузит новое видео в тот же плеер), не re-key.
- **AVOID:** не оборачивать рейл в контейнер, который route-код `innerHTML`-ит; не `repeat()` в анимируемом grid; не забыть юнит на 0-треке; не плодить второй mobile-инстанс.
- Источники: React Router nested-layout, Slack/Teams shell, YouTube miniplayer, react-activation keep-alive, CSS-Tricks animating-grid, LinkedIn/Messenger dock (REJECTED bubble — украсть только инженерию персистентности).

### 2.3 Responsive collapse (responsive-collapse)
- **STEAL:** desktop — фикс-ширина + collapse-to-edge; Material 3 list-detail (aside фиксирован, MAIN — гибкая панель); mobile (<640px по нашим брейкам) — чат становится TAB/ROUTE, не squeezed-колонка и не bottom-sheet, дерущийся с mini-player; TV — read-only ambient + voice; CarPlay — текст hard-block (app-category модель Apple), voice-only.
- **AVOID:** не держать колонку на телефоне; не overlay чата на now-playing (landscape-overlay — задокументированная жалоба Twitch-юзеров); composer НЕ под mini-player; не M3-«forbids» как закон (это nav-rail гайд, не chat-panel).
- Источники: M3 window-size-classes/nav-rail/panes/bottom-sheets, Twitch/YouTube/Discord mobile, Spotify mini-player (защищённая transport-зона), coder/mux #271 (hysteresis), CarPlay app-category.

### 2.4 Scope switching Общий ↔ per-station (scope-switching)
- **STEAL:** SLACK/DISCORD-гибрид — switcher ВНУТРИ рейла: кликабельный header-row с именем активной комнаты (единый source of truth для composer) → dropdown-список `📌 Общий эфир` (pinned) + per-station с two-tier unread. Активная комната STICKY и decoupled от route И от играющей станции. При расхождении — недеструктивный chip «перейти в чат станции?», НЕ auto-swap. Per-room scroll+draft. Сегмент `[Эта станция | Общий]` — только для бинарного in-context флипа.
- **AVOID:** не Twitch-модель (навигация re-scope-ит — потеряет draft/scroll); не tab-strip как primary (не масштабируется); не auto-switch ни на route, ни на play/skip/track.
- Источники: Twitch (page=switcher, REJECTED модель), Slack header/quick-switcher, Discord channel-list, Telegram folder/topic tabs (REJECT как primary), Ant Design Sider collapse.

### 2.5 Twinr-лейн + AI-co-presence (ai-in-rail)
- **STEAL:** AI-лейн внутри ОДНОГО рейла через сегмент-toggle (одна кнопка send, меняется адресат). Приватный ответ Twinr inline с persistent-тегом `✦ Twinr · видно только вам` (Discord ephemeral-паттерн) + «Поделиться с чатом» (делится ТОЛЬКО ответом, не промптом). Per-line бейдж на КАЖДОЙ AI-строке. Earned-interjection (Spotify AI DJ): одна авто-исчезающая микро-карточка на смену трека с конкретной причиной; pull-based «Что я пропустил?» (Slack-дисциплина, не auto-inject). In-player «почему?»/«сделай по-другому» deep-link-ят в рейл, флипают composer в Twinr, разворачивают рейл, стримят ответ — ОДИН Twinr-pipeline для player + rail + announcer.
- **AVOID:** color-only mode (1.4.1); sticky toggle между комнатами; auto-inject ИИ в человеческий поток (Character.AI walk-back); AI-строка без бейджа; обещать enforced-приватность в backend-less SPA (это UI-аффорданс, помечать как demo).
- Источники: Google AI Mode (слабый precedent для one-input/two-target), Slack split-view/summarize, Discord ephemeral (flag 64), Spotify AI DJ, Character.AI group-chat removal.

### 2.6 Density / a11y / anti-patterns always-on (density-a11y-antipatterns)
- **STEAL:** один always-mounted список с DOM-node-cap (~50–200 строк + буфер; НЕ React-virtualization — файл vanilla single-file); sticky-bottom follow только в пороге низа; на scroll-up — заморозка + фокусируемый pill «Новые ↓» (≥44px); под флудом — smooth→instant + коалесинг. РОВНО один `role=log` (polite, atomic=false), пустой до раскрытия, тихий при collapse, не переанонсит backlog на навигации. Presence и moderation-strip — НЕ в live-region.
- **AVOID:** unbounded DOM на 12 маршрутах; append-and-auto-scroll безусловно (yank читателя, cline «bouncy scroll»); несколько конкурирующих polite-регионов; Twitch-trap (auto-hide + спрятать expand-control).
- Источники: WAI-ARIA `role=log`, Sara Soueidan/A11Y-Collective live-regions, React-Virtuoso (поведенческий референс порогов), TanStack Virtual, cline #4780, Spotify/Apple Music market-verdict, Twitch UserVoice 41456605, GitLab #16183.

---

## 3. RECOMMENDED LAYOUT — точная app-shell сетка

### 3.1 Решение
Добавить **третий настоящий grid-трек** в `.app-shell`. Сегодня (стр. 277): `grid-template-columns: var(--sidebar-w) 1fr;` плюс `padding-bottom: var(--player-mini-h)` (стр. 280). Sidebar — `position:fixed` над gutter (трек 1 — резерв, не in-flow nav). Рейл делаем in-flow сиблингом `#app`.

```css
:root{
  --rail-w: 360px;          /* НАШЕ решение (Onest 14–15px Cyrillic + reaction-rail); не Twitch-константа */
  --rail-w-spine: 52px;     /* свёрнутый spine: 44px target + паддинг + unread-dot */
}
.app-shell{
  grid-template-columns: var(--sidebar-w) 1fr var(--rail-w);
  transition: grid-template-columns var(--t-slow);   /* за prefers-reduced-motion */
}
/* состояние «свёрнут в spine» */
.app-shell[data-rail="spine"]{ grid-template-columns: var(--sidebar-w) 1fr var(--rail-w-spine); }
/* рейл скрыт целиком (route-suppress) */
.app-shell[data-rail="off"]  { grid-template-columns: var(--sidebar-w) 1fr; }

.chat-rail{
  grid-column: 3;
  height: calc(100dvh - var(--player-mini-h));   /* зеркалит .sidebar стр. 452 — НИКОГДА не под mini-player */
  position: sticky; top: 0;
  z-index: 40;                                    /* НИЖЕ mini-player (player-mini z, стр. 593) */
  display: flex; flex-direction: column;
}
@media (prefers-reduced-motion: reduce){ .app-shell{ transition: none; } }   /* snap, не slide */
```

**Бюджет ширины (честная математика):** на 1280px → 240 (sidebar) + 360 (rail) = 600px chrome → MAIN ≈ 680px. Это терпимо для now-playing/`#/lives`, но НА ГРАНИ. Поэтому при <1280px рейл по умолчанию свёрнут в spine (52px), а не в полную колонку (см. §6). Mini-player — full-width ПОД всеми тремя зонами.

### 3.2 ASCII — полный shell (desktop ≥1280, рейл expanded)

```
┌──────────┬───────────────────────────────────────┬──────────────────┐
│ TOPBAR: [поиск.................]      [Личный кабинет] [💬 unread •]   │  ← topbar, full-width
├──────────┼───────────────────────────────────────┼──────────────────┤
│ SIDEBAR  │  MAIN  (#/route — router outlet)        │  CHAT RAIL 360px │
│ 240px    │                                         │  ┌────────────┐  │
│ fixed    │   #/home  Волна — now-playing + почему  │  │ header      │  │
│          │   #/lives Live-grid                      │  │ switcher ▾  │  │
│ Волна    │   #/taste Мой вкус …                     │  │────────────│  │
│ Мой вкус │                                         │  │ now-playing │  │
│ Открыть  │   (MAIN сужается когда рейл открыт —     │  │ «почему»    │  │
│          │    reflow, НЕ overlay)                   │  │────────────│  │
│ [☀/☾]    │                                         │  │ message log │  │
│          │                                         │  │ (role=log)  │  │
│          │                                         │  │   ↑ «N нов» │  │
│          │                                         │  │────────────│  │
│          │                                         │  │ presence    │  │
│          │                                         │  │ composer    │  │
│          │                                         │  │ [✦|👥][▷]   │  │
│          │                                         │  └────────────┘  │
├──────────┴───────────────────────────────────────┴──────────────────┤
│ MINI-PLAYER 72px (--player-mini-h) — full-width ПОД всеми тремя       │  ← рейл кончается ВЫШЕ
│ ◁ ▷  ░░ now-playing ░░  «почему?» · «сделай по-другому»               │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.3 Свёрнутый spine (то же, рейл = 52px)

```
…  MAIN (шире) …                    │ 💬 │   ← spine 52px: иконка комнаты
                                    │ •5 │     + unread-dot, expand-chevron
                                    │ ›  │     всегда виден (нет Twitch-trap)
```

---

## 4. RAIL ANATOMY — сверху вниз

Три зоны, скроллится ТОЛЬКО средняя. Логика переносится из `.ai-dock` (seeded `ROOM_NAME='Общий эфир'`, `data-mode` composer, undo-toast Gmail-delay, `@Twinr`/`/`), контейнер-семантика переписывается (не модалка: нет focus-trap, нет Escape-close, нет launcher, нет breathe-on-speak open-анимации — это были свойства openable-пузыря).

1. **HEADER (sticky)** — кликабельный room-title row (Slack channel-header) = единый source of truth «куда я пишу»: `📌 Общий эфир ▾` + collapse-chevron (≥44px, focus-visible 3px). Клик → dropdown: pinned «Общий эфир», divider, per-station комнаты с two-tier unread. Опционально под title — сегмент `[Эта станция | Общий]` когда есть station-контекст.
2. **NOW-PLAYING CONTEXT (статичная, НЕ live-region)** — обложка-полоска + `«почему»`-caption для станции АКТИВНОЙ КОМНАТЫ (может отличаться от играющей — подписываем чья это комната). Это wedge как социальный референт.
3. **MESSAGE LOG (flex:1, overflow-y:auto)** — `role="log"` (implicit polite, atomic=false), пустой до раскрытия. DOM-node-cap ~50–200 строк + буфер (НЕ virtualization-движок — файл vanilla). Sticky-bottom follow только в пороге ~100px от низа; на scroll-up — заморозка + фокусируемый pill **«Новые ↓»** (≥44px, фон `--brand-blue-light` как нетекстовый, цифра белая). Анон-хэндлы `guest_NNNN` без аватара/ссылки на профиль. AI-строки — левый Twinr-акцент-бар (#5168FC нетекстовый) + per-line бейдж `✦ Twinr` (текст бейджа — `--accent-on-dark`).
4. **PRESENCE (статичная)** — `🟢 1 240 слушают · 18 пишут` + moderation-strip `Медленный режим · 5 сек`. НЕ в live-region (анонс только при явном изменении). Seeded/demo — помечать честно.
5. **COMPOSER (sticky, над mini-player)** — порядок сверху-вниз: `#ai-ribbon` armed-destination → сегмент-toggle `[✦ Twinr | 👥 Всем]` (role=radiogroup, single-select, icon+слово, не color-only) → `[textarea] [🎙] [▷ send ≥44px]`. Placeholder и send переформулируются по mode: `Спросите Twinr…` / `Спросить Twinr` ↔ `Написать всем в «LoFi»…` / `Отправить в #LoFi`. Undo-toast (Gmail-delay) — без изменений. Twinr-mode: input-border #5168FC (нетекстовый OK), любой Twinr-ТЕКСТ → `--accent-on-dark`.

### 4.1 ASCII — рейл (expanded)

```
┌────────────────────────────────┐
│ 📌 Общий эфир            ▾  ‹  │  HEADER: switcher + collapse
│ [ Эта станция | ✓ Общий ]      │  опц. бинарный сегмент
├────────────────────────────────┤
│ ▶ LoFi Ночь · «меланхоличное   │  NOW-PLAYING (статич.)
│   инди — ты часто слушаешь»     │
├────────────────────────────────┤
│ guest_4471  привет, что за трек │
│ guest_0192  огонь 🔥            │  MESSAGE LOG (role=log)
│ ▏✦ Twinr · видно только вам     │  приватный AI-ответ inline
│ ▏ Поставил X — под твой вечер.  │
│ ▏ [ Поделиться с чатом ]        │
│ guest_8830  +                   │
│            … ↑ [ Новые ↓ · 3 ]  │  pill при scroll-up
├────────────────────────────────┤
│ 🟢 1 240 слушают · 18 пишут     │  PRESENCE (статич.)
│ Медленный режим · 5 сек         │  moderation-strip
├────────────────────────────────┤
│ ✦ Поставил X — почему?          │  #ai-ribbon armed-dest.
│ [ ✦ Twinr ][ 👥 Всем ]          │  toggle (radiogroup)
│ [ Спросите Twinr…    ][🎙][ ▷ ] │  composer
└────────────────────────────────┘
        ↑ кончается ВЫШЕ mini-player (72px)
```

---

## 5. SCOPE SWITCHING — Общий ↔ per-station

- **Где живёт switcher:** в HEADER рейла (Slack-паттерн), как dropdown-СПИСОК (не tab-strip — не масштабируется). `📌 Общий эфир` всегда pinned-top. Per-station комнаты ниже (канон-список также на `#/lives`). Имя активной комнаты постоянно видно = единый source of truth для composer.
- **Активная комната STICKY и decoupled** от двух вещей: (1) `#/route`-навигации, (2) играющей станции. Один инстанс рейла сиблинг `#app` → смена `#/route` НЕ трогает комнату автоматически (см. §2.2). Смена играющей станции/трека — тоже НЕ трогает.
- **Правило расхождения (no context loss):** когда играющая станция ≠ комната рейла — недеструктивный chip **`Сейчас играет: <станция> · перейти в её чат?`**. Никогда auto-swap (это канонический mis-send / lost-draft). Per-room scroll + draft персистят в client-store `roomId → {messages, scrollTop, draft, mode}`.
- **Смена комнаты происходит ТОЛЬКО через:** (1) выбор из dropdown, (2) принятие chip-а, (3) deep-link `#/lives/:id/chat` или `#/chat/global`. Composer-toggle ресетится в `👥 Всем` на смене КОМНАТЫ, не на смене экрана.
- **Default-scope по маршруту:** «Общий эфир» по умолчанию везде; на `#/lives` и когда станция активно играет — рейл ПРЕДЛАГАЕТ (chip, не авто) комнату этой станции; на `#/artist`/`#/track` — scope-INTO родительской станции/артиста с фильтром (не призрак-канал).

> **Открытое: «следовать за станцией».** Для station-centric радио многие юзеры ОЖИДАЮТ, что чат идёт за тем, что слушают. Decoupling-by-default правильный (защищает draft), но сверить с prior-research room-vs-global и как минимум дать опт-ин «следовать за играющей станцией» (см. §10 Open Decisions).

---

## 6. RESPONSIVE — Web / Mobile / TV / CarPlay

Ключим к РЕАЛЬНЫМ брейкам файла (1280/1024/768/640/480), не к выдуманным 1100/600. Один DOM-инстанс, рестайл по media-query (не второй компонент).

| Брейк | Поведение рейла |
|---|---|
| **≥1280px** | Полная колонка `--rail-w 360px`. Default EXPANDED на `#/lives`/`#/home`, иначе spine (см. §8) |
| **1024–1280px** | Колонка УЗКАЯ (chrome-бюджет): по умолчанию **spine 52px** (защищает MAIN); клик → expand как overlay/push 360px. Если MAIN зажат — сворачиваем РЕЙЛ (sidebar в 72px НЕ умеет) |
| **640–1024px** | Spine по умолчанию; expand → overlay 360px над MAIN (не push) |
| **<640px (mobile)** | НЕ колонка. Чат = full-height ROUTE/таб из левого sidebar-нав (пункт «Чат») или one-tap из now-playing. role=dialog с focus-trap + Escape + focus-return (мобильный лист — модальный, в отличие от desktop-рейла). Сидит МЕЖДУ topbar и mini-player |

- **Desktop collapse/resize:** ОДИН chevron в header → анимирует grid-track 360↔52↔(0 только при route-suppress). State персистится в localStorage (per route-class). Spine ВСЕГДА показывает expand-аффорданс (избегаем Twitch-trap, где expand-control исчезает на узких окнах). Hysteresis (если делаем авто-collapse при resize) — это JS-state-tracking, НЕ pure-CSS media-query; флагнуть риск flash-of-wrong-state.
- **Composer+toggle на телефоне:** порядок topbar/room-chips → log (role=log) → `#ai-ribbon` → сегмент-toggle → composer+🎙+send → **[MINI-PLAYER, нетронут]**. Composer докуется НАД mini-player, никогда не накрывает transport-бар (правило проекта «НЕ над mini-player»). Все цели ≥44px.
- **Конфликт с mini-player:** жёсткий пол. Рейл `height: calc(100dvh - var(--player-mini-h))`, z НИЖЕ player-mini. Мобильный лист — над mini-player, не bottom-sheet, дерущийся за thumb-zone. Не Material modal bottom-sheet (он dim-ит/накрывает mini-player).
- **TV (10-foot):** read-only ambient — presence + now-playing «почему» + медленный read-only фид «Общего эфира». НЕТ composer/toggle/`/`. Голос — единственный input («почему?»/«сделай по-другому»).
- **CarPlay:** текст-чат hard-block. App-category модель Apple исключает third-party free-text клавиатуру → человеческий лейн `👥 Всем` и весь текст-input скрыты. Только voice-to-Twinr (как Spotify Android Auto «Talk to DJ»), статус лейна — аудио-анонс.

> **Surface-honesty:** в `gorod-fm.html` есть только `data-surface='web'`. TV/CarPlay-разметки нет — это FORWARD-guidance, не интеграция в текущий shell.

---

## 7. AI В РЕЙЛЕ — Twinr-лейн без пузыря

- **Twinr внутри ОДНОГО рейла**, не отдельной поверхности. Сегмент `[✦ Twinr | 👥 Всем]` в composer — один send, меняется адресат. Default `👥 Всем` в человеческих комнатах; `✦ Twinr` на `#/home`/AI-only surface. Ресет в `Всем` на смене КОМНАТЫ. `@Twinr` и `/` — fallback-акселераторы.
- **Приватный ответ «видно только вам»:** Twinr рендерит ответ inline в логе, визуально отличный (левый Twinr-акцент-бар #5168FC нетекстовый + persistent-тег `✦ Twinr · видно только вам`), с чипом **«Поделиться с чатом»**, который делится ТОЛЬКО ответом, НИКОГДА промптом. В backend-less SPA это UI-аффорданс, не доставленное серверное свойство — помечать как demo (anti-black-box: не обманывать).
- **Disclosure:** per-line бейдж `✦ Twinr` на КАЖДОЙ AI-строке (текст бейджа `--accent-on-dark`, не #5168FC). Подаём как brand-фичу «не чёрный ящик», не как юр-комплаенс. (Twitch-bot-badge как «June 2025 norm» — выброшен как непроверяемая выдумка; обоснование — прозрачность + SR-различение авторства.)
- **Co-presence — earned, не ambient (Spotify AI DJ-дисциплина):** на смену трека — ОДНА авто-исчезающая `#ai-ribbon` микро-карточка с КОНКРЕТНОЙ причиной из профиля («поставил X — ты часто слушаешь меланхоличное инди»), не больше. `Что я пропустил?` — pull-based кнопка per-room (Slack summarize-дисциплина, НЕ auto-inject в поток), помечена «summary может быть неточным». Per-room «тихий режим» (Twinr только при @-обращении).
- **In-player → рейл (один pipeline):** кнопки `«почему?»`/`«сделай по-другому»` в mini-player deep-link-ят: флипают composer в `✦ Twinr`, разворачивают рейл если свёрнут, стримят ответ inline. ОДИН Twinr-pipeline обслуживает in-player + rail-composer + announcer (это уже частично есть: in-player аффорданс открывает AI-surface и флипает mode — стр. ~13358).

---

## 8. ГДЕ ЖИВЁТ ЧАТ — per-route таблица (все 12 маршрутов)

Mounted ≠ expanded ≠ present. «Видимый на каждой странице» владельца соблюдается тем, что spine виден на всех контентных маршрутах; полное скрытие — только там, где чат вредит задаче/экспорту.

| # | Route | Поверхность | Рейл по умолчанию | Почему |
|---|---|---|---|---|
| 1 | `#/home` (Волна) | adaptive radio + now-playing | **EXPANDED** (Twinr-лейн) | Главный AI-якорь; «почему» = соц-референт |
| 2 | `#/lives` (Live-grid) | станции/каналы | **EXPANDED** (`Всем`) | Первичная co-listening поверхность |
| 3 | `#/taste` (Мой вкус) | живой профиль | **SPINE** | Фокус-задача редактирования; default-toggle пересмотреть (фокус) |
| 4 | `#/podborki` (Открыть) | discover | **SPINE** | — |
| 5 | `#/library` | библиотека | **SPINE** | — |
| 6 | `#/artist` | артист | **SPINE** (scope-into) | Фильтр в родительскую комнату |
| 7 | `#/track` | трек | **SPINE** (scope-into) | Scope-into, не призрак-канал |
| 8 | `#/favorites` | избранное | **SPINE** | — |
| 9 | `#/profile` | профиль | **SPINE** | — |
| 10 | `#/onboarding` | taste picker | **OFF** (ни рейла, ни spine) | Single-goal; чат рушит completion. Уже скрыт через `html[data-active-route="#/onboarding"]` (стр. 2235) |
| 11 | `#/recap` | 9:16 export-карточка | **OFF** | Скриншот должен быть чистым |
| 12 | `#/map` | внутренний | **OFF** | Zero соц-ценности, internal review |

- **OFF-маршруты** рендерят `data-rail="off"` (grid → 2 колонки). Для `#/onboarding` механизм уже есть; для `#/recap` и `#/map` правила нужно ДОБАВИТЬ (не «переиспользовать» — их сейчас нет).
- **Супер­сессия prior-research:** дефолт SPINE (а не «AI-only dock») на personal-маршрутах и per-station-комнаты-с-старта — сознательные override бриф-ом владельца поверх «AI-only on personal surfaces» / «один Эфир сначала». Незакрытый trade-off модерации/seed-presence — несём дальше как флаг (§10).

---

## 9. COLLAPSE DEFAULT + a11y must-haves + ANTI-PATTERNS

### 9.1 Collapse default
- **Web ≥1280px:** EXPANDED только на `#/home`/`#/lives`; SPINE на остальных контентных; OFF на `#/onboarding`/`#/recap`/`#/map`.
- **Никогда не collapse-to-nothing** на Web — spine (52px) с unread-dot + expand-chevron всегда виден (требование владельца, НЕ Twitch-поведение). State персистится per route-class в localStorage.

### 9.2 A11y must-haves (load-bearing — в файле уже ~15 polite-регионов)
- **Управляемая politeness:** message log = `role="log"` (implicit polite, atomic=false), пустой до первого раскрытия. **НЕ** наивный always-on polite — иначе флуд SR на каждой странице + коллизия с «почему»-чеками. Анонсировать ТОЛЬКО когда фокус в рейле ИЛИ через default-OFF тоггл «озвучивать новые»; гейтить, пока говорят now-playing/«почему»-регионы; primary-сигнал = pill «Новые ↓». Только ОДИН разговорный live-stream говорит одновременно.
- **Тихо при collapse:** свёрнутый spine не анонсит (только неанонсируемый unread-dot).
- **Не переанонсить backlog** на смене `#/route` (инстанс один, переживает навигацию).
- **Флуд-коалесинг:** `Анна и ещё 3 написали` под high-velocity; smooth→instant follow под burst.
- **Никогда `aria-live=assertive`** для чата.
- **Presence/moderation-strip — НЕ live-region** (статичны; анонс только при явном изменении).
- **Focus:** desktop-рейл — персистентный регион, НЕ модалка (без app-wide focus-trap, без focus-steal на mount, без Escape-как-модаль). Мобильный лист — `role=dialog` + focus-trap + Escape + focus-return на триггер.
- **Hit targets ≥44px**, focus-visible 3px (`--accent-on-dark`), `prefers-reduced-motion` → snap (grid-transition off), reaction-burst → мгновенный инкремент счётчика.
- **Контраст:** `#5168FC` ТОЛЬКО нетекстовый (бар/индикатор/border); весь текст Twinr-mode → `--accent-on-dark` (#8094ff dark / #3A4ED0 light).

### 9.3 ANTI-PATTERNS — НЕ делать
- ❌ НЕ оставлять плавающий `.ai-dock`-пузырь / launcher как default (отклонено владельцем).
- ❌ НЕ `position:absolute`/overlay для open-состояния на desktop (перекрывает now-playing/визуализатор).
- ❌ НЕ рендерить рейл внутри `[data-page]` / re-key/unmount на hash-change (flicker + dropped messages + lost scroll).
- ❌ НЕ под mini-player (composer/send/toggle) — рейл кончается над 72px-баром.
- ❌ НЕ auto-switch комнату на смене route/станции/трека — chip, не swap.
- ❌ НЕ tab-strip как primary switcher; НЕ collapse-to-nothing; НЕ прятать expand-control на узких окнах (Twitch-trap).
- ❌ НЕ naive aria-live=polite на лог; НЕ assertive; НЕ несколько конкурирующих polite одновременно.
- ❌ НЕ color-only для mode-toggle; НЕ #5168FC для текста ≤14px.
- ❌ НЕ выдавать seeded presence/«видно только вам»/moderation за доставленные backend-свойства — помечать demo.
- ❌ НЕ video-theater-overlay («Cinema» = тёмная тема, видео нет).
- ❌ НЕ держать 360px-колонку на телефоне; НЕ Material modal bottom-sheet (накрывает mini-player).

---

## 10. STAGED BUILD PLAN (замена `.ai-dock` на док-рейл) + OPEN DECISIONS

Каждая стадия — что scripted/seeded. Логика данных/composer/toggle/undo/private-reply переносится из `.ai-dock`; контейнер-семантика переписывается.

- **Стадия 0 — Grid-каркас.** В `.app-shell` (стр. 277) добавить третий трек `var(--rail-w)` + токены `--rail-w/--rail-w-spine`; `data-rail` атрибут (`expanded`/`spine`/`off`) на `.app-shell`. `.chat-rail` = in-flow сиблинг `#app`, `height: calc(100dvh - var(--player-mini-h))`, z НИЖЕ player-mini. Пустой контейнер, grid-transition за reduced-motion. *Scripted: ничего; только layout.*
- **Стадия 1 — Перенос анатомии.** Перенести из `.ai-dock` (стр. 2840) в `.chat-rail`: 3-зонную структуру, seeded `ROOM_NAME='Общий эфир'`, `data-mode` composer (стр. 3051+), undo-toast (стр. 3108), `@Twinr`/`/`. УДАЛИТЬ: focus-trap, Escape-close, launcher-кнопку, breathe-on-speak open-анимацию (стр. 2825/2858). `.ai-msgs` → `role=log`, пустой до раскрытия. *Seeded: стартовый «Общий эфир» с demo-сообщениями, помечены.*
- **Стадия 2 — Collapse/spine + персист.** Chevron в header → grid 360↔52; localStorage per route-class; spine с unread-dot + expand-chevron (всегда виден). *Scripted: unread-счётчик из seeded-дрипа.*
- **Стадия 3 — Header-switcher + scope.** Dropdown `📌 Общий эфир` + per-station; client-store `roomId→{messages,scrollTop,draft,mode}`; chip «перейти в чат станции?» при расхождении; per-room scroll/draft. *Seeded: 2–3 demo-станции-комнаты.*
- **Стадия 4 — Live-feed дисциплина.** DOM-node-cap; sticky-bottom follow + порог; pill «Новые ↓» (≥44px); seeded-дрип через ту же follow-логику (доказать механику); коалесинг под флудом. *Scripted: таймер-дрип сообщений, помечен demo.*
- **Стадия 5 — Twinr-лейн + co-presence.** Приватный inline-ответ + тег + «Поделиться» (только ответ); per-line бейдж; `#ai-ribbon` earned-interjection на смену трека; pull «Что я пропустил?»; deep-link in-player «почему?»/«сделай по-другому» → флип composer + expand + стрим. *Scripted: Twinr-ответы из seeded-причин профиля.*
- **Стадия 6 — A11y-проход.** Управляемая politeness (focus-gated/toggle-off), гейт против «почему»-регионов, не-переанонс backlog, presence/moderation вне live-region, reduced-motion snap, 44px/3px-аудит. *Verify: Chrome-MCP + ручной SR-проход.*
- **Стадия 7 — Responsive.** 1024/640 рестайл одного инстанса; <640px → full-route чат из sidebar + role=dialog лист над mini-player; route-suppress `#/recap`/`#/map` (добавить, как `#/onboarding`). *Scripted: эмуляция брейков в Chrome-MCP.*

### OPEN DECISIONS (владельцу)
1. **Default EXPANDED — где?** Подтвердить `#/home`+`#/lives` expanded, остальное spine. При 1280px MAIN≈680px — ОК для now-playing? Или default-expanded только ≥1440px?
2. **«Следовать за играющей станцией»** — давать ли опт-ин (station-centric mental model) или жёсткий decoupling-by-default? Сверить с prior room-vs-global.
3. **`#/taste` toggle-default** — `Всем` или сохранять фокус (spine + no auto-announce)?
4. **Rail-width** — 360px ок для Cyrillic Onest + reaction-rail, или 340/380? Resizable — v1 или позже?
5. **Модерация per-station-с-старта** — анон `guest_NNNN` + always-visible глобал = увеличенная abuse-поверхность; объём slow-mode/report/mute defaults и кто модерирует? (RU 152-ФЗ — territory юриста, не дизайна.)
6. **Spine vs полное скрытие на personal-маршрутах** — устраивает ли «видимый spine везде» как трактовка «на каждой странице»?

---

## SOURCES (консолидировано)

**Grounding:** `designs/gorod-fm.html` — grid стр. 277 (`var(--sidebar-w) 1fr`), `--sidebar-w:240px` стр. 136, `--player-mini-h:72px` стр. 138, `.sidebar height: calc(100dvh - var(--player-mini-h))` стр. 452, `.ai-dock` стр. 2840 (388px/560px/z96), `.why-pop` стр. 717 (НЕ трогать), `data-mode` composer стр. 3051+, undo-toast стр. 3108, `.ai-ribbon` стр. 3178/10357, `.ai-dock` mobile-рестайл стр. 3132 (480px), `#/onboarding` suppress стр. 2235, контраст-нота `#5168FC` 4.25:1 стр. 128, `--accent-on-dark #8094ff` стр. 128 (light `#3A4ED0` стр. 206), focus 3px стр. 258, реальные брейки 1280/1024/768/640/560/480/360. · `docs/superpowers/RESEARCH-gorod-fm-ubiquitous-chat.md` (IA/scope/toggle/модерация/per-route — НЕ дублировать).

**Анатомия/layout:** FrankerFaceZ #819 · medium.com/@SirStendec «Twitch New Channel Layout» · help.twitch.tv channel-page-guide · hardreset.info collapse-stream-chat · YouTube Live Chat Wide Layout (Chrome Web Store) · support.google.com/youtube 252650382 · Discord support (collapsible panes / sidebar / member-list width) · BetterDiscord DiscordNight (240px) · Stationhead (screensdesign / tiffanyhughes) · Kick moderation-features-guide.

**Персистентность:** medium.com/@jackpritomsoren (Outlet sibling) · react.wiki/router/nested-routes · dev.to/milescrighton (wrapPageElement) · Slack help 16764236868755 + blog simpler-streamlined-sidebar · YouTube Miniplayer support 9162927 · dev.to/serifcolakel (keep-alive) · websocket.org/guides/frameworks/react · github.com/haixc/react-router-cache-route · css-tricks animating-css-grid · LinkedIn help a569449/a563389 (REJECTED bubble) · neowin.net Feb-2024 Messenger-stuck.

**Responsive:** m3.material.io layout/scaffold-panes/nav-rail/bottom-sheets · developer.android.com canonical-layouts · browserstack responsive-breakpoints · Twitch blog 2024/07/29 mobile + uservoice 41456605 (expand-trap) + landscape-overlay complaint · maestra.ai YouTube-mobile-chat · discord.com/blog android-navigation · beebom Spotify mini-player · github.com/coder/mux #271 (hysteresis) · CarPlay: discussions.apple.com 256065569 / app-category model.

**Scope:** Slack help 212596808 (header/resize) · Telegram folders/tour + topic-tabs (alternativeto 2025/6) + bugs.telegram.org 56581 · Ant Design Layout (Sider collapse) · OSM rails-dev #4130 (key off screen width).

**AI:** 9to5google 2025/05/02 + blog.google AI-Mode (one-input/two-target, weak) · Slack split-view docs + summarize · Discord ephemeral (dpp.dev flag 64; discordjs.guide) · Spotify Newsroom 2025-05-13 AI-DJ-voice + TechCrunch + MBW text-input · Character.AI group-chat (blog) + human-removal (support Sept-2025) · clarification: Amazon Music Maestro = AI-плейлист, НЕ chat-overlay.

**Density/a11y:** w3.org/WAI ARIA23 (`role=log`) + MDN ARIA log role · sarasoueidan.com accessible-notifications p1 · a11y-collective.com/blog/aria-live · virtuoso.dev (поведенческий референс follow-output, НЕ движок для vanilla-файла) + discussions #1079 / issue #317 · TanStack Virtual #195 · cline #4780 (bouncy-scroll) · Spotify Messages (billboard / MBW / business-standard Jan-2026 / musically opt-in) · apple.com/apple-music (zero chat) · Twitch uservoice 41456605 · GitLab #16183/#23298.
