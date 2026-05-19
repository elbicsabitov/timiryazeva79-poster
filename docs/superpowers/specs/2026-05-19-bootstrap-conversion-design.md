# Spec: Liquid Glass → Bootstrap 5.3 — точный порт, dev-handoff (×2 проекта)

**Дата:** 2026-05-19
**Статус:** APPROVED (design), awaiting plan
**Клиенты:** Turbo Performance (CRM) · Twinr «Большой Цифровой»
**Источник:** brainstorming + 2 Karpathy-tier ресёрча + полное картирование прототипов

---

## 1. Контекст и цель

Заказчик просит переписать два утверждённых HTML/CSS-прототипа **на Bootstrap**, в формате «можно передать программисту», с Karpathy-tier методологией «как правильно закодить».

**Цель:** каждый прототип воспроизведён **пиксель-в-пиксель**, но разметка пересобрана на Bootstrap 5.3 (grid / utilities / JS-плагины = структурный субстрат), Liquid Glass дизайн-система живёт **над** Bootstrap через CSS `@layer` + `--bs-*`-перехваты. Поставка = чистый Vite-проект на SCSS-исходниках, расширяемый командой заказчика, + single-file standalone для превью клиенту.

**Принцип (инверсия):** не «бутстрапизируем дизайн», а делаем Bootstrap субстратом под неизменным стеклянным слоем. Шов в шов с оригиналом, DOM идиоматичен.

## 2. Объём

| Дизайн | Файл-источник | Экранов | Особенности |
|---|---|---|---|
| **CRM** Turbo Performance | `designs/crm-glass.html` (242 KB, 4549 строк) | **29** + модалки | dark-only, нет кастомайзера |
| **Twinr** «Большой Цифровой» | `designs/twinr-liquid-glass.html` (261 KB, 5462 строки) | **21** + AI-модуль (11 инструментов) + Liquid Glass Customizer + `#page-guide` | темы sunset/dawn, кастомайзер |

`twinr-liquid-glass.html` подтверждён как **последняя** версия Twinr (vs `twinr-full.html` — 13 стр., без AI/кастомайзера; standalone — лишь build-артефакт того же исходника).

### Не входит (YAGNI / границы)
- RU.TV (`rutv-landing*`, `showcase-*`), Kinolog, themes/ — **вне объёма**.
- Никаких новых экранов, редизайна, изменения контента/цифр (verbatim из прототипов).
- Никаких React/Next/Vue, Storybook, SSR, бэкенда.
- Без скоуп-крипа: оригинальные прототипы = GROUND TRUTH визуала.

## 3. Зафиксированные решения

| # | Решение | Обоснование |
|---|---|---|
| D1 | **2 отдельных проекта** `crm-bootstrap/` + `twinr-bootstrap/` | Разные заказчики (Holy Grail Часть 3.2); чистая передача 2 командам; ложится на параллельные worktree-агенты |
| D2 | **Onest вместо Inter** (self-hosted) | Inter — hard-gate запрет (DESIGN_PROTOCOL Часть 2.1); Onest визуально близок (метрики), уже в RU.TV-работах. Документируется как осознанная замена в session log |
| D3 | **Bootstrap 5.3.8** (exact pin), SCSS-исходники (не CDN) | Кастомизация Sass-переменных/карт; tree-shake; стабильность handoff |
| D4 | **Vite ^6** (не 7/rolldown) | Стабильный `rollupOptions.input`, HMR, MPA; Vite 7/rolldown ещё стабилизируется |
| D5 | **Рантайм остаётся hash-SPA** (не настоящий MPA) | Верность оригиналу (один файл со всеми экранами) + условие single-file standalone. Nunjucks собирает один `index.html` из partials на билде; в браузере — прежний hash-routing + localStorage |
| D6 | **`sass ~1.99` pin + `silenceDeprecations`** | Bootstrap 5.3 ещё на `@import`; Dart Sass deprecations — upstream, подтверждено twbs#41558 |

## 4. Архитектура (идентична для обоих проектов)

```
<project>/                         # crm-bootstrap/ | twinr-bootstrap/
├── package.json                   # bootstrap 5.3.8 (exact), vite ^6, sass ~1.99 (pinned)
├── package-lock.json              # коммитится; инструкция npm ci
├── vite.config.js                 # MPA-вход через glob; css.preprocessorOptions.scss.silenceDeprecations
├── postcss.config.js              # autoprefixer
├── .nvmrc .browserslistrc .editorconfig .stylelintrc.json .prettierrc.json .gitignore
├── README.md  CONTRIBUTING.md     # «где что лежит», как добавить экран/компонент, Sass-deprecation нота
├── src/
│   ├── pages/                     # один .njk на экран, сгруппировано
│   │   └── (CRM: 29 · Twinr: 21 + AI-tools + guide)
│   ├── templates/
│   │   ├── layouts/base.njk       # <html><head>, линки ассетов — каркас 1 раз
│   │   ├── layouts/<shell>.njk    # sidebar+topbar shell
│   │   ├── partials/              # sidebar, topbar, theme-toggle, icons
│   │   └── macros/ui.njk          # переиспользуемая разметка карточек/таблиц
│   ├── scss/                      # 7-1 + tokens/ (SSOT) + themes/
│   │   ├── main.scss              # единственная точка входа (Bootstrap «Option B» порядок)
│   │   ├── tokens/                # colors, typography, glass, space-radii, maps
│   │   ├── abstracts/             # mixins (glass(), focus-ring())
│   │   ├── base/ layout/ components/ pages/ themes/
│   │   └── vendor/
│   ├── js/
│   │   ├── main.js                # импорт scss + selective Bootstrap JS
│   │   ├── bootstrap.js           # только используемые плагины
│   │   ├── theme.js               # data-bs-theme toggle + localStorage
│   │   └── modules/               # customizer, slide-morph, table-sort, scroll-reveal, ai-subnav, router
│   └── assets/ img/ icons/ fonts/ # backdrops вынесены из base64; Onest self-hosted
└── styleguide/index.njk           # kitchen-sink витрина токенов/компонентов (НЕ Storybook)
```

### 4.1 CSS-каскад — линчпин (без `!important`-войн)

Одна декларация порядка слоёв, загружается первой:

```
@layer reset, bootstrap, tokens, glass, widgets, utilities;
```

| Слой | Ответственность |
|---|---|
| `reset` | reboot/normalize (или внутрь bootstrap) |
| `bootstrap` | скомпилированное ядро — **только используемые компоненты** (tree-shake в `main.scss`) |
| `tokens` | `:root` / `[data-bs-theme=*]` переопределение `--bs-*` + наши `--ds-*` |
| `glass` | материал: `backdrop-filter` (+`-webkit-`), спекуляр-псевдоэлементы, концентрические радиусы, фото-подложка, переодевание компонентов |
| `widgets` | Customizer, slide-morph индикатор, sortable/column-toggle таблицы, scroll-reveal, AI chip-nav |
| `utilities` | Bootstrap utility API **наверху** — всегда побеждает без `!important` |

Реализация: Sass с нативными `@layer`-блоками (Option B порядок импортов внутри `@layer bootstrap`, utilities в `@layer utilities`). Компоненты переодеваются через их же `--bs-card-bg`/`--bs-modal-bg`/`--bs-dropdown-bg`/`--bs-offcanvas-bg`/`--bs-table-bg`/… (нулевая добавочная специфичность); стекло докладывается слоем `glass`. Резервный фолбэк для legacy: только `--bs-*`-паттерн без слоёв.

### 4.2 Токены — единый источник истины

Извлечь `:root` из прототипов → SCSS-карты в `tokens/`. Карты кормят `$theme-colors`/`$utilities`/`$spacers` Bootstrap **и** эмитят `--ds-*` CSS-переменные для рантайма. Тёмная/светлая — нативно через `data-bs-theme`:
- **CRM** — dark-only (`[data-bs-theme="dark"]`, тема не переключается).
- **Twinr** — sunset (актив) + dawn (light), переключатель в topbar → `data-bs-theme`.

Порядок импортов `main.scss` (Bootstrap «Option B», verbatim из офиц. документации): `functions` → **наши override-переменные + tokens/** → `variables` + `variables-dark` → **tokens/maps (map-merge)** → `maps` → `mixins` → `root` → **только нужные компоненты** → `utilities/api` (последним) → кастомный 7-1 слой.

Извлечённые токены прототипов (общие для обоих, из картирования):

```
Typography (iOS scale): --t-large-title 34 / --t-title-1 28 / --t-title-2 22 /
  --t-title-3 20 / --t-headline 17 / --t-body 17 / --t-callout 16 /
  --t-subhead 15 / --t-footnote 13 / --t-caption-1 12 / --t-caption-2 11
Glass material: --glass-ultrathin rgba(51,51,51,.18) / --glass-thin .28 /
  --glass-regular .38 / --glass-thick .50 / --glass-chrome .42
Backdrop blur: --blur-ultrathin blur(16) sat(140%) / --blur-thin 24/160 /
  --blur-regular 36/180 / --blur-thick 48/200
Specular rim: --spec-rim (inset 0 1px 0 rgba(255,255,255,.4) … ) / --spec-rim-strong
Glass border: --glass-border rgba(255,255,255,.18) / --glass-border-strong .30
Ink: --ink-1 #fff / --ink-2 .85 / --ink-3 .66 / --ink-4 .46 (rgba 235,235,245)
Accents: --coral #FF8A6E (+glow .4) / --amber #FFC171 / --rose #FF7D9D /
  --gold #FFD98A / --peach #FFB088
Status: --success #7DD3A8 / --warning #FFC171 / --danger #FF8A8A
Shadows: --shadow-1 / -soft / -card / -hover / -button (coral-tinted)
Radii: --r-xl 28 / --r-lg 22 / --r-md 16 / --r-sm 12 / --r-xs 8 / --r-pill 999
Timing: --ease-glass cubic-bezier(.32,.72,0,1) / --ease-spring / --ease-out-quart /
  --duration-fast 180ms / --duration-glass 380ms (Twinr +--duration-slow 600ms)
Layout: --sidebar-w 72px / --sidebar-expanded 248px
Twinr-only: --glass-highlight .32 / -strong .48 ; [data-theme="dawn"] инверсия;
  Customizer control-токены: data-material/-tint/-tint-intensity/-dim/-shape/-texture
  → --dr-bg/--dr-blur/--dr-border/--dr-rim/--dr-tint-rgb/--dr-tint-a/--dr-dim-a
```

Точные значения переносятся из прототипов 1-в-1 на этапе исполнения (план разложит по файлам).

### 4.3 Порт разметки и JS-паритет

| Оригинал | Bootstrap-идиома |
|---|---|
| Fixed sidebar 72→248px hover | `<aside class="position-fixed">`, ширина через `--sidebar-w`; на <lg — Offcanvas (тот же markup), `.offcanvas-lg` |
| Sticky topbar | `.sticky-top`; z-index **ниже** offcanvas (twbs#40575) |
| CSS Grid формы/KPI/two-col | `.row/.col`; точные px-шаги через расширенную карту `$spacers` (`map-merge`), не inline-стили |
| Модалки / дропдауны / табы / collapse / toast | **Bootstrap-плагины** (focus-trap, ESC, ARIA, scroll-lock бесплатно); `bootstrap.bundle.min.js` (Popper внутри); стекло через `--bs-*` + слой `glass` |
| Customizer / slide-morph nav / sortable+column-toggle таблицы / scroll-reveal / AI chip-nav | **Кастомный JS остаётся**, монтируется на Bootstrap-разметку; хуки на past-participle события (`shown.bs.*`/`hidden.bs.*`); `getOrCreateInstance` чтобы не дублировать инстансы; никогда не вешать кастом и `data-bs-*` на один элемент |
| Hash-routing SPA + localStorage | **Сохраняется** (D5). Ключи: CRM `crm-glass.last-route`; Twinr `twinr-last-route`, `twinr-last-ai-tool`, `twinr-lg-state`, `twinr-theme` |
| Customizer (Twinr) | Перевешивается на `el.style.setProperty('--ds-…' / '--dr-…')` — редактирует те же швы, что слой `glass`; точная математика интенсивности тинта сохраняется 1-в-1; Copy-CSS, пресеты, collapse, reset, persist в `twinr-lg-state` |

### 4.4 Пайплайн ассетов
- base64-подложки **вынести** в `src/assets/img/` (кешируемость, читаемые диффы); мелкие иконки — пусть Vite сам решает по `assetsInlineLimit`.
- Onest — self-hosted в `assets/fonts/`, `@font-face` + `font-display:swap`, preload критического веса.
- SVG noise-текстуры Twinr (`feTurbulence` ripple/subtle) — сохранить как data-URL фон, проверить рендер в Safari/Firefox.
- `npm run build:standalone` — **отдельный** скрипт (vite-plugin-singlefile или существующий Python-инлайнер по `dist/`), даёт один кликабельный .html на проект (все экраны через hash). Не в дефолтном `build`. Документировать что standalone ≠ исходник.

### 4.5 Dev-handoff DX
- `README.md`: что/зачем, prereqs (`.nvmrc`, `npm ci`), таблица npm-скриптов, карта директорий, «где что лежит» (токены → `scss/tokens/`; glass → 3 именованных файла; добавить экран = копия .njk + extends layout), Sass-deprecation нота (upstream, twbs#41558), политика пина Bootstrap.
- `CONTRIBUTING.md`: нейминг (BEM-lite `.ds-*`, никогда не переопределять `.card` напрямую — модификатор), «не править `node_modules/bootstrap`», lint/format гейт, browser target.
- Lint: `stylelint` + `stylelint-config-twbs-bootstrap` + Prettier (`stylelint-config-prettier-scss` последним в extends).
- `styleguide/index.njk`: свотчи цветов (из `$theme-colors`), типошкала, все `.ds-*` в состояниях, glass-карты на «шумном» фоне, формы, живой theme-toggle.

## 5. Реестр рисков и митигации

| Риск | Митигация |
|---|---|
| **backdrop-root clipping** (блюр «мёртвый») | Фото-подложка в `body::before` вне backdrop-root предков; не вешать `opacity/filter/transform` на shell-обёртку с glass-панелями |
| Bootstrap modal backdrop | Блюрить `.modal-backdrop.show` (`--bs-backdrop-opacity` ~.25 + `backdrop-filter`), не только диалог; диалог — тяжёлое стекло через `--bs-modal-bg` |
| navbar-blur ломает offcanvas (twbs#40575) | z-index offcanvas > блюр-navbar; либо снимать блюр navbar на `show.bs.offcanvas` |
| `overflow:hidden`+radius режет фильтр (Chrome); Firefox sticky+overflow+radius | `mask-image` вместо `clip-path`; `border-radius`+`isolation:isolate`; не комбинировать sticky-glass с rounded overflow-clipped предком |
| Перф: много блюр-слоёв | Блюрить только контейнеры (sidebar/topbar/modal/panel); внутренним повторяющимся элементам — полупрозрачный сплошной фон без `backdrop-filter`; `will-change` точечно; blur ≤24px |
| Safari `backdrop-filter` | Всегда `-webkit-backdrop-filter` + `backdrop-filter` |
| **Customizer Twinr** (самый тяжёлый) | 6 материалов × 12 тинтов × intensity × dim — точная математика `--dr-tint-a` 1-в-1; отдельный модуль; верификация скриншот-диффом по пресетам |
| AI chip-nav (динамическая инъекция) | Сохранить логику инъекции/видимости на смене роута; смонтировать на Bootstrap `.nav` |
| Onest≠Inter | Метрики близкие; верификация WCAG + скриншот-дифф; задокументировать замену |
| `!important` на glass+utilities одновременно | Запрещено — ломает порядок слоёв; обе группы без флага |
| Dart Sass deprecations | `silenceDeprecations` + pin `sass ~1.99`; нота в README |

## 6. Верификация (Holy Grail Часть 5)

Эталон визуала = **сами прототипы** (`crm-glass.html`, `twinr-liquid-glass.html`). После порта — агент `compound-engineering:design:design-implementation-reviewer`:
- скриншот-дифф **каждого** экрана: порт ↔ оригинал (1:1 fidelity);
- WCAG AA Normal минимум;
- breakpoints 375 / 768 / 1024;
- console errors; Twinr customizer — по пресетам.

Контекст основного автора на ручные скриншоты не тратится. Повторный прогон только после закрытия findings. Anti-slop чек-лист (Часть 2) и Часть 9 gate перед `done`.

## 7. Параллельное исполнение

2 worktree-агента (CRM / Twinr), паттерн S49/S50 + `feedback_worktree_parallel_agents`:
- изолированные git-worktree на проект;
- архитектура идентична → общий glass-метод вендорится копией `_glass-core.scss` (не общий пакет — D1);
- `npm run build` + `stylelint` + `format-check` зелёные между мержами;
- sequential merge train в `master`.

Детальная разбивка задач — в плане реализации (следующий навык writing-plans).

## 8. Критерии приёмки (Definition of Done)

1. `crm-bootstrap/` и `twinr-bootstrap/` собираются `npm ci && npm run build` без ошибок (Sass-deprecations засайленсены).
2. Каждый из 29 + 21 экранов визуально совпадает с оригиналом (design-implementation-reviewer: нет HIGH-findings).
3. Bootstrap = структурный субстрат: grid/utilities/JS-плагины используются идиоматично; glass через `@layer`+`--bs-*`, **ноль** `!important` для победы над Bootstrap.
4. Onest self-hosted; Inter отсутствует; hard-gate шрифтов пройден.
5. Twinr: AI-модуль (11 инструментов), chip-nav, Customizer (материал/тинт/интенсивность/dim/пресеты/Copy-CSS/collapse), sunset/dawn, hash-routing + 4 localStorage-ключа — функционально 1-в-1.
6. CRM: 29 экранов, модалки, sortable/column-toggle таблицы, hash-routing + localStorage — 1-в-1.
7. `npm run build:standalone` даёт один кликабельный .html на проект (все экраны).
8. README/CONTRIBUTING/styleguide присутствуют; lint/format/pin настроены; `package-lock.json` закоммичен.
9. WCAG AA Normal; breakpoints 375/768/1024 не ломаются.
10. Замена Inter→Onest задокументирована в session log (исключение Holy Grail Часть 2.1).

## 9. Источники (Karpathy-tier ресёрч)

- Bootstrap 5.3: Sass customization & import order; CSS variables `--bs-*`; Color modes `data-bs-theme`; Options `$enable-*`; Card/Modal CSS vars; Contents; JavaScript; Optimize.
- MDN: `@layer` (cascade layers); `backdrop-filter` (backdrop roots, Safari prefix).
- CSS-Tricks: CSS Cascade Layers (utilities-last).
- twbs/bootstrap #40575 (navbar-blur×offcanvas), #41558 / #40962 (Dart Sass deprecations).
- twbs/examples `sass-js` (package.json scripts/deps); Sass Guidelines 7-1; Vite build/MPA; Sass `@import` breaking change; stylelint-config-twbs-bootstrap.

---

**Next:** spec self-review → user review gate → `superpowers:writing-plans`.
