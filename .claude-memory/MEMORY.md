# Memory — Twinr Design

## Sessions

- [session_2026_04_15.md](session_2026_04_15.md) — Первая сессия: полный дизайн РК "Большой Цифровой"
- [session_2026_04_16.md](session_2026_04_16.md) — Постер «Продаётся» Тимирязева 79: ресерч законов, дизайн, GitHub Pages
- [session_2026_04_18.md](session_2026_04_18.md) — Liquid Glass редизайн РК: Apple iOS 26 через FigMCP, photo backdrop, 13 экранов по структуре оригинала
- [session_2026_04_18_turbo.md](session_2026_04_18_turbo.md) — Турбо AI-модуль: 9 экранов из Figma + Discovery Hub + Guide + Apple HIG refinement
- [session_2026_04_18_customizer.md](session_2026_04_18_customizer.md) — Liquid Glass Customizer: 38 droplet-капель на Руководстве + plug-in panel (material/tint/intensity/dim/shape/texture + 6 presets)
- [session_2026_04_20.md](session_2026_04_20.md) — Cross-project: чтение фидбека Harvid для bereke-kp через Telethon, TODO сохранён в paws-kp, аудит SYNC_PROMPT (5 гэпов)

## Current Design Iteration

**Active prototype:** `designs/twinr-liquid-glass.html` (~267 KB, ~4990 строк, **22 страницы** + 5 модалок + **Liquid Glass Customizer** на #page-guide)
**Client-facing standalone:** `designs/twinr-liquid-glass-standalone.html` (**1.7 MB**, base64 backdrop inline, открывается двойным кликом без сервера)

**Sidebar — 4 пункта (Apple HIG):**
1. Рекламный кабинет (admin) — `page-advertisers` + вложенные (add, details, campaign, bind)
2. Статистика — `page-stats` + `page-stats-clips` + `page-stats-detail`
3. Wordstat — `page-wordstat` (placeholder)
4. ИИ — hub для 9 AI-инструментов через chip-row sub-nav
5. Руководство — `page-guide` (long-form docs)

**ИИ-модуль (внутри одной вкладки):**
Discovery Hub на `#page-ai` (4 группы × карточки). Под-навигация chip-row на каждой AI-странице со slide-morph indicator, group separators между Контент/Генерация/Медиа/Анализ.

9 AI-инструментов:
- Контент: `page-sources`, `page-prompts`
- Генерация: `page-source-work`, `page-rewrite`, `page-chat`
- Медиа: `page-transcribe`, `page-video-gen`
- Анализ: `page-docs`, `page-keywords`

**Плюс промо/auth**: `page-promo`, `page-login`, `page-register` (оригинал, не тронуты).

**Эстетика:** Apple iOS 26 Liquid Glass — translucent grey glass `#333333 @ 0.28-0.50`, heavy backdrop-blur 16-48px, gradient border white `0.4→0.32`, uniform top rim specular `inset 0 1px 0 rgba(255,255,255,0.4)`, **coral accent `#FF8A6E`** (НЕ розовый из Figma — сознательно сохранена сессия #18 палитра), warm photo backdrop (Matterhorn + clouds + sunset from Unsplash CC0).

**Customizer (page-guide):** Live-preview переключатель material (clear/ultra/thin/regular/thick/chrome) × 12 Apple system tints × intensity 0-32% × dim 0-40% × shape (pill/rounded/squircle/organic) × texture (smooth/frosted/grain/linen/prism). 6 пресетов (Apple/Sunset/Ocean/Forest/Mono/A11y). State в `localStorage: twinr.lg.customizer`. Copy-CSS кнопка экспортит актуальные glass-tokens. **38 droplet-капель** вместо одного монолитного контейнера — каждый параграф/список/callout = свой backdrop-filter слой.

**Модалки:** overlay `rgba(10,4,18,0.42)` + **luminance lift** на panel (gradient 14%→3% white over glass-regular + strong specular top rim) — панель СВЕТЛЕЕ dimmed фона (Apple HIG).

**Apple HIG features:**
- Slide-morph indicator в sub-nav (translateX + width, 380ms glass ease)
- Sidebar tooltips на свёрнутом состоянии
- Destructive confirm dialog (red btn + cancel glass)
- Button loading state (spinner 1100ms) для primary CTAs
- Dropzone drag-enter feedback (scale + glow)
- aria-current, aria-label, role="alertdialog"
- Hit-targets ≥32px (Apple min)
- Concentric corners (outer r-xl 28 → inner r-pill 999)

**Предыдущие итерации:**
- `designs/twinr-full.html` — индиго/SaaS baseline (оригинал заказчика, до Liquid Glass)
- `designs/themes/theme-*.html` (6 цветовых вариантов) — explore до Liquid Glass
- Начальная Liquid Glass версия без AI-модуля (в session_2026_04_18.md)

**Backdrop assets:**
- `designs/assets/sunset-backdrop.jpg` — primary (Matterhorn above clouds, 525 KB)
- `designs/assets/dusk-lake.jpg` — backup alt (327 KB)

**Routing:** hash-based (`#page-X`), localStorage для last-route + last-ai-tool. Детали в `docs/RESUME_PROMPT.md` и `docs/SYNC_PROMPT.md`.

## Правила sync

См. `docs/SYNC_PROMPT.md` (расширенный протокол): 8 шагов, обязательная пересборка standalone при изменении primary, структурированный conventional commit, summary для клиента.
