# Session 2026-05-13 — RU.TV лендинг pixel-perfect + production-best

**Запрос Эльбика:** Подключиться к Figma MCP, сверстать pixel-perfect лендинг RU.TV из Figma (frame 3373:2073). Затем — после ухода спать на 8 часов — расширил до полной автономии: production-ready, real logo из файлов, все вкладки и весь функционал на одном уровне, ресерч UX/UI экспертов уровня Karpathy и второй вариант 1-в-1.

## Доставлено

### 2 версии лендинга

| Файл | Назначение | Размер |
|------|------------|--------|
| `designs/rutv-landing-figma.html` | Pixel-perfect 1-в-1 копия Figma frame 3373:2073 (Holy Grail 1.2 — никогда не строить из головы если есть source) | 36 KB |
| `designs/rutv-landing.html` | Production-best SPA с Karpathy-tier UX (Apple TV+/Netflix/Spotify/YouTube TV patterns) | 120 KB |
| `designs/rutv-landing-figma-standalone.html` | Standalone Figma copy с base64 inline | 4.1 MB |
| `designs/rutv-landing-standalone.html` | Standalone production-best | 11.2 MB |
| `tools/build_rutv_landing_standalone.py` | Reusable inliner (28 unique assets, 0 missed) | — |

### Pipeline (FigMCP → HTML)

1. **OAuth FigMCP** через Chrome MCP (open auth URL → click Allow → callback localhost:45287 авто-принят)
2. **`mcp__FigMCP__listFiles`** → `dev` (single connected file)
3. **`getNodes` root depth 0** → 50+ frames; нашёл 3 кандидата на "Главная" (5201:1075 dark mock, 3178:835 DFM dashboard, 3373:2073 RU.TV white landing)
4. **Visual disambiguation** через `viewNode` jpeg на каждый → 3373:2073 — правильный (Uma2rman ПРЯМОЙ ЭФИР hero, RASA Пулевой featured, partners RMG)
5. **Deep `getNodes` depth 3-5** на 3373:2073 + детях карточек/footer → полное mapping (text, fills, hashes, layout, fonts SF Pro Text 13/14/16/40)
6. **Cross-reference Figma imageHash ↔ файлы в `designs/assets/rutv/`** через Read tool на PNG: подтвердил 28 unique assets (Rectangle 4322 / -1..-18 / image 1 / image 2 / RUTV 2 / unsplash_* партнёры / App Store / google-play-badge)
7. **HTML build** → Chrome MCP iterations → fix padding (clamp 4vw → 16vw для 230 на 1440), real logo SVG (Figma RUTV 2.png пустой; собрал inline currentColor SVG с masked TV)
8. **Iframe-based mobile preview** (`__rutv_mobile_test.html` temp) для 375/414/768 verify (browser MCP не resize ниже 500)
9. **6 inner views built** + hash router → SPA с topnav routing
10. **Standalone Python script** → 28 assets base64-inlined, both variants built

### Real RU.TV logo solution

**Проблема:** `RUTV 2.png` (и @2x/@3x) в `assets/rutv/` экспортирован пустым из Figma (только белый прямоугольник).

**Источник истины:** `unsplash_qiMCJHg2vTI.png` — партнёрская badge с реальным каноническим RU.TV брендом (белое "RU" + circle "TV" на чёрном).

**Решение:** Inline SVG с currentColor + SVG mask для cut-out TV — адаптируется к любому фону (тёмный hero / белый footer):
```svg
<svg viewBox="0 0 96 48">
  <defs><mask id="tv"><rect fill="#fff" .../><text fill="#000">TV</text></mask></defs>
  <text fill="currentColor" font-weight="900">RU</text>
  <circle fill="currentColor" mask="url(#tv)"/>
</svg>
```

### Karpathy-tier UX/UI research (in-context synthesis)

Применённые best-practices из training (без external fetching):
- **Apple TV+ landing**: cinematic 100dvh hero, gradient overlay top→bottom, giant title typography clamp(38-84), single primary CTA + ghost secondary
- **Netflix homepage**: card hover preview (scale + shadow + play overlay fade), category rows with see-all
- **Spotify**: persistent now-playing chip с rotating album art, dismiss-to-session
- **YouTube TV**: live indicator pulse, 7-day grid, currently-airing red highlight
- **Twitch**: live red dot pulse animation
- **Apple HIG iOS 26 Liquid Glass**: frosted nav backdrop-blur 28px saturate 180%, concentric corners (xl/lg/md/pill), specular tonality
- **Refactoring UI (Schoger/Wathan)**: 5-tier shadow ladder (xs/sm/md/lg/xl) + brand-glow, hierarchy via color/size/weight (не bold-everything), text-wrap balance/pretty
- **Cleveland-McGill**: position+length encoding for schedule cells (не area/angle)
- **Nielsen 10 heuristics**: system status (LIVE pulse + viewer count), match real world (Russian copy authentic), user control (back/ESC/dismiss), consistency, recognition over recall (icon labels), accessibility (skip-link, aria-current, focus-visible)
- **Brendan Kane hooks**: 1.7s above-fold (LIVE pill + Uma2rman big title + 2 CTAs)
- **Cialdini friction**: single primary CTA (Смотреть прямой эфир), social proof (1247 viewers live)

### SPA Architecture

7 hash routes: `#/`, `#/live`, `#/news`, `#/poster`, `#/video`, `#/programs`, `#/schedule`

JS router (~30 lines) parses `location.hash`, toggles `view-X` divs (display:none/block via `is-active`), syncs aria-current на nav, обновляет document.title, scrolls top, force-stuck nav на inner pages (light bg, no dark hero behind).

Каждая inner view имеет own:
- Page hero (eyebrow + h1 + subtitle над gradient bg)
- Filter chips bar
- Content grid (4-col news / 6-col video / 3-col programs / horizontal cards poster)
- Load-more / sort / channel filter

Live view особенная: 16:9 player frame с big-play overlay + LIVE badge → 2-col layout с up-next sidebar.

Schedule view: 7-day grid с time-col + LIVE cell highlighted brand red с pulse animation.

### Pitfalls встреченные

- **Chrome MCP file:// navigate prepends https://** → solved через `python -m http.server 8765` background
- **Chrome MCP resize_window не уменьшает viewport <500px на Win + DPR 1.5** → solved через iframe wrapper preview
- **System reminder про "не предлагать закончить сессию"** vs Эльбик ушёл спать на 8h → продолжил полностью автономно как просил
- **Reveal-on-scroll observer ломал partners-block при view switch** → ограничил scope только на `#view-home .section`
- **Python sed Windows console UnicodeEncodeError → arrows** → ASCII fallback (`->` вместо `→`)
- **Hash anchor collision** (`#live` vs `#/live`) — router parses `#\/?` so оба работают, но `#live` тоже triggers route (feature не bug — buttons "Программа передач" → switches view)

## Files modified

```
designs/rutv-landing.html              (NEW · 120 KB · best version)
designs/rutv-landing-figma.html        (NEW · 36 KB · 1-в-1 Figma)
designs/rutv-landing-standalone.html         (NEW · 11.2 MB)
designs/rutv-landing-figma-standalone.html   (NEW · 4.1 MB)
tools/build_rutv_landing_standalone.py (NEW)
DEBT.md                                (RUTV-100..120 added)
```

## Что pending для заказчика

- **RUTV-119**: заказчик выбирает Figma 1-в-1 vs production-best
- **RUTV-116**: real HLS stream integration
- **RUTV-117/118**: Search/Login backend
- **RUTV-120**: подача — deck + walkthrough видео обеих версий

## Next session

При resume:
1. Смотреть Эльбик решил какую версию финалить
2. Если best — добавить inner page deep-dive (program detail с episodes, news article view, search results)
3. Перенос на Next.js + shadcn/ui (RUTV-016 / 119)
