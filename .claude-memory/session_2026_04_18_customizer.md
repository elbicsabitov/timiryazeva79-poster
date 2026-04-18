# Session 2026-04-18 (ночь) — Liquid Glass Customizer

## Контекст

После сборки Турбо AI-модуля (predecessor session) заказчик не определился с финальной фактурой и оттенком стекла. Вместо того, чтобы перебирать комбинации в голове — Элбик попросил:

1. **Фулл-аудит** standalone-файла (`twinr-liquid-glass-standalone.html`) и iOS-26 Liquid Glass библиотеки/гайдлайнов.
2. На странице «Руководство» — **разбить параграфы текста на отдельные блюр-капли** (droplets).
3. **Кастомайзер** для теста: переключатель фактуры блюра, оттенков стекла, уровней затемнения. Живой preview — «всё в экосистеме Эпла, можно выбирать сочетания и смотреть как читается текст».
4. Всё — по гайдлайнам Apple iOS 26 Liquid Glass.

## Research — Apple iOS 26 Liquid Glass

### Источники
- **Local skill:** `liquid-glass-design` (ECC) — SwiftUI/UIKit/WidgetKit API, `GlassEffectContainer`, `.regular/.clear`, `.tint()`, `.interactive()`, `glassEffectID` morphing.
- **Apple newsroom 2025-06:** translucent + adapts light/dark + specular highlights + reflects/refracts surroundings + colorful tints + elegant clear look.
- **Apple Developer doc:** Liquid Glass overview (материалы без конкретных числовых спецификаций публично).
- **Apple Materials (classic, still applies):** 5 levels — `ultraThinMaterial`, `thinMaterial`, `regularMaterial`, `thickMaterial`, `chromeMaterial`.
- **nikdelvin/liquid-glass:** web recreation через CSS + SVG `feDisplacementMap` + `feGaussianBlur` + `feColorMatrix`, depth 10, strength 100, blur/chromaticAberration adjustable.

### Что взяли в систему

| Параметр | Apple HIG | Реализация у нас |
|----------|-----------|------------------|
| Материалы | 5 (ultraThin/thin/regular/thick/chrome) + clear | 6 (все 5 + clear) |
| Tint palette | systemBlue/Indigo/Teal/Mint/Green/Yellow/Orange/Pink/Purple/Red/Gray | 12 (11 system + coral brand) |
| Tint intensity | auto (adapts) | manual 5 ступеней (0/7/14/22/32%) |
| Reduce Transparency | iOS accessibility setting | manual dim (none/soft/medium/strong = 0/14/26/40% black) |
| Shape | concentric corners | 4 варианта (pill/rounded/squircle/organic) |
| Specular rim | top-edge highlight | `inset 0 1px 0 rgba(255,255,255,0.35-0.50)` по уровням |
| Saturation | implicit | `saturate(140-190%)` с blur |

## Audit — текущий прототип

`designs/twinr-liquid-glass.html` токены (до изменений):

| Token | Значение |
|-------|----------|
| `--glass-ultrathin` | `rgba(51,51,51,0.18)` |
| `--glass-thin` | `rgba(51,51,51,0.28)` |
| `--glass-regular` | `rgba(51,51,51,0.38)` |
| `--glass-thick` | `rgba(51,51,51,0.5)` |
| `--glass-chrome` | `rgba(51,51,51,0.42)` |
| `--blur-ultrathin...thick` | `blur(16/24/36/48px)` + `saturate(140/160/180/200%)` |
| `--glass-border` | `rgba(255,255,255,0.18)` / strong `0.30` |
| `--spec-rim` | `inset 0 1px 0 rgba(255,255,255,0.4)` + fading bottom |
| `--ink-1..4` | `rgba(255,255,255, 1 / 0.85 / 0.66 / 0.46)` |
| `--coral` | `#FF8A6E` (session brand, keep) |

Структура соответствует Apple. Решил **не переделывать глобальные токены** — кастомайзер scoped только к `.guide-layout` через data-attr + CSS-вар.

## Что сделано

### 1. SVG filter defs (body top)
```
<svg class="lg-svg-defs" aria-hidden="true">
  <filter id="lg-frosted">  <!-- fractalNoise 0.85 / 2 octaves -->
  <filter id="lg-grain">    <!-- fractalNoise 2.4 / 1 octave -->
  <filter id="lg-crystal">  <!-- turbulence + feDisplacementMap scale 8 -->
```

### 2. CSS — data-attr switching на `.guide-layout`
Каждая ось управляется через data-attribute. Пример material:
```css
.guide-layout[data-material="regular"] {
  --dr-bg: rgba(51,51,51,0.34);
  --dr-blur: blur(32px) saturate(180%);
  --dr-border: rgba(255,255,255,0.22);
  --dr-rim: inset 0 1px 0 rgba(255,255,255,0.44);
}
```
6 materials × 12 tints × 5 intensity × 4 dim × 4 shape × 5 texture = 28800 комбинаций.

### 3. Droplet primitive
```css
.droplet {
  background: var(--dr-bg);
  backdrop-filter: var(--dr-blur);
  border: 1px solid var(--dr-border);
  border-radius: 22px;  /* overridden by [data-shape] */
  /* ::before — texture overlay (mix-blend-mode: overlay) */
  /* ::after  — tint + dim combined overlay */
}
```
Варианты:
- `.dr-lead` — первая большая капля (26px 32px padding, 19px font)
- `.dr-heading` — пилюля с coloured dot (inline-flex, auto-width, max-content)
- `.dr-para` — стандартный параграф
- `.dr-list` — список (padding-left 46px)
- `.dr-callout` — совет/важно с цветным border-left
- `.dr-faq` — h3+p пара

### 4. Guide content restructure
- `<article class="guide-article dr-mode">` — теряет opaque фон (прозрачный контейнер)
- Original h2/h3 hidden (`display: none`)
- Каждый логический блок обёрнут в `<div class="droplet dr-X">`
- 38 droplets total (1 lead + 9 headings + 21 para/list + 2 callouts + 6 faq + 1 footer)

### 5. Customizer panel (right sidebar, sticky)
Grid: `.guide-layout.has-customizer { grid-template-columns: 1fr 220px 296px; }`

Контролы:
- **Фактура** (segmented): 6 materials → label показывает числовые spec
- **Оттенок** (12 swatches): 12 цветов круглыми пилюлями, активный 2.5px ring
- **Насыщенность** (range slider): 0..4 → 0/7/14/22/32% с readout под slider
- **Затемнение** (segmented): none/soft/medium/strong (симулирует Reduce Transparency)
- **Форма** (segmented): pill/rounded/squircle/organic (асимметричные радиусы через nth-child)
- **Текстура** (segmented): smooth/frosted/grain/linen/prism (все через data URIs + conic-gradient для призмы)
- **Пресеты** (6 chips): Apple iOS 26 / Sunset / Ocean / Forest / Mono / A11y
- **Actions**: Копировать CSS (clipboard API) + Сбросить
- **Collapse**: chevron → сворачивает в 54px пилюлю

### 6. JS (persistent customizer)
- Load from localStorage key `twinr.lg.customizer` на старте
- Apply → обновление data-attrs + label text + active states
- Save → на каждое изменение (включая collapse state)
- Copy CSS → собирает актуальные CSS-переменные `--dr-bg/--dr-blur/--dr-border/--dr-rim` + sidecar коммент со state

### 7. Standalone rebuild
Python one-liner:
```py
for name in ['sunset-backdrop.jpg', 'dusk-lake.jpg']:
    with open(f'assets/{name}', 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    html = html.replace(f"url('assets/{name}')", f"url('data:image/jpeg;base64,{b64}')")
```
Результат: **1704013 bytes** (1.7 MB) — standalone открывается двойным кликом.

## Решения (и почему)

1. **Scoped customizer, не глобальный** — не хотел ломать 13 оригинальных экранов, пока заказчик не утвердил. Финальная фаза (CUST-012/013) — применить утверждённые токены глобально.
2. **CSS-вар через data-attr, не via style=""** — декларативно, дешёво переключается, хорошо для transitions, никакого inline-CSS.
3. **38 отдельных `backdrop-filter` слоёв** — perf риск. Тестил на 1440×900 — работает гладко за счёт GPU-композитинга. Если попадёт в prod с 100+ droplets на других страницах — надо мониторить.
4. **SVG filter как `filter:` на `::before`, не как `backdrop-filter: url()`** — Safari поддерживает backdrop-filter url, но cross-browser надёжнее data-URI с уже готовым noise-pattern.
5. **6 presets** — покрывают design-пространство: neutral Apple baseline / current sunset / альтернативы (ocean/forest) / контрастный mono / accessibility-first a11y.
6. **Copy CSS, не Copy tokens** — клиент хочет готовый CSS snippet для дизайнера, а не JSON.

## Блокеры / компромиссы

- **Clipboard API** в test показал `unknown` — promise не успел разрешиться до return. Реальный клик — работает (подтверждено визуальной сменой кнопки на «Скопировано»).
- **Organic shape** на мелких droplets визуально subtle — разница между `22px` и `28px 44px` маленькая. Можно будет усилить после фидбека заказчика.
- **Inter font** — единственная внешняя зависимость standalone (Google Fonts). Без инета fall back на `-apple-system, SF Pro`.
- **Prism texture** использует conic-gradient — выглядит как мыльный пузырь. Красиво но может быть слишком «decorative». Оставил как опцию.

## Файлы

| Файл | Размер | Изменения |
|------|--------|-----------|
| `designs/twinr-liquid-glass.html` | 267 KB (~4990 строк) | +945/-158 (customizer + droplet rewrite guide) |
| `designs/twinr-liquid-glass-standalone.html` | 1.7 MB | пересобран с base64 backdrop |
| `DEBT.md` | — | +15 строк (CUST-001..015 новый блок) |
| `.claude-memory/session_2026_04_18_customizer.md` | — | этот файл |
| `.claude-memory/MEMORY.md` | — | +1 session pointer, обновлён Current Design Iteration |

## Что дальше

**Ближайшее:**
- **CUST-011** — показать заказчику customizer (кастомизатор открывается на #page-guide, sticky справа)
- Собрать фидбек: какая комбинация нравится? Может быть неочевидная — например `thin + teal + squircle + frosted` или `thick + graphite + rounded + linen` (A11y-friendly)

**После утверждения фактуры:**
- CUST-012 — зафиксировать выбор как глобальные `--glass-*` токены (обновить :root)
- CUST-013 — применить к всем 22 экранам (не только Guide)
- CUST-014 — sync с Figma-файлом `dev` (обновить компоненты)
- CUST-015 — убрать customizer из production сборки (оставить feature flag для internal review)

**Уже в очереди:**
- TURBO-009 (показ 9 AI-экранов заказчику) — можно комбинировать с CUST-011 в одной сессии
- LG-010/TURBO-012 — responsive pass (после утверждения темы, чтобы не переделывать дважды)
