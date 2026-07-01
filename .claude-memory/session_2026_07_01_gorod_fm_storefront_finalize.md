# Session 2026-07-01 — Город ФМ home storefront: finalize + images + card actions

## Контекст
Резюм `feat/gorod-home-rmg-storefront` (storefront-редизайн главной: карусель РМГ + витрина + поиск + чат-рейл). Директива: «гоу фулл, всё доделаем, мультипоточно». Затем 2 добавки: «заполни всё картинками по теме как в онбординге + сделай 2-ю версию, обе открой в Chrome»; «везде добавь чтоб можно было сердечко нажать и плюсик».

## Что сделано
- **Все 10 owner-feedback/deferred пунктов** (см. HANDOFF top-block): (1) центр-карта карусели ♥/⏸/⏭ → TwinrTransition, синхрон с мини-плеером; (2) карусель — отступ/центрирование/фокус; (3) друзья → ▶/＋ иконки; (4) 122-элем витрина, eager-render; (5) убрать AI-хром на #/home (scoped `html[data-active-route]`); (6) **починен overlay поиска** (был 0-height внутри `.topbar` c backdrop-filter → в `<body>`) + моб-вход + in-overlay input; (7) моб-shell через `matchMedia` `data-surface`; (8) **чат-рейл «Общий эфир» восстановлен** (Option A 3-track grid, порт из `feat/gorod-chat-layer`); (9) честная монограмма-обложка мини-плеера; (10) adversarial-ревью → 6 фиксов (H1/M2-M5/L9).
- **Две версии по картинкам:** `gorod-fm.html` (монограммы, дефолт) + `gorod-fm-images.html` (фото; флаг `window.GOROD_PHOTOS`/`?art=photos`). Пул `window.GOROD_ART` реюзит онбординговые ассеты (genre/artist/tile).
- **♥/＋ на каждой карточке** (122): overlay на вертикальных, inline на рядах; друзья = ▶♥＋. Toggle aria-pressed (сердце заливается, ＋→✓).
- Standalone пересобран (Pillow webp-inline, 5.19 MB).

## Решения (и почему)
- **Чат-рейл = Option A (global 3-track grid)**, а не home-only: JS — это REPLACE старого Twinr-дока (тот становится инертным), значит рейл — единственная AI-chat поверхность → должен быть на всех роутах (как было в chat-layer). Другие роуты идентичны master.
- **Home-рейл ведёт с «Всем · Общий эфир» (community), не Twinr-AI** (review M3): owner-locked «главная = не-AI». Twinr в один тап. 🟡 owner-confirm.
- **Картинки = реюз онбординговых ассетов**, не новый фетч («как в онбординге»). Демо-лейблы держат честность (лицо может не совпадать с именем — всё «демо»).
- **Моб-shell через surface-flip**, не через борьбу с каскадом `[data-surface="web"]` (там unlayered + !important рулы перебивали).
- **Vertical card `<button>`→`<div>`** чтобы ♥/＋ (кнопки) вкладывались валидно (у карточки не было клик-действия).

## Блокеры / компромиссы
- ♥/＋ и ▶ у друзей — **визуальные** (toggle/hooks), не привязаны к реальному плейлисту/бэкенду (демо).
- Реальные РМГ-ассеты (лого/частоты/стримы) — owner-gated.
- eager-render 122 карточки синхронно (M6) — ок для демо.

## Файлы
- `designs/gorod-fm.html` (~20.2k строк) — все правки.
- `designs/gorod-fm-images.html` (1.01 MB, генерится `.scratch/gorod2/gen_images_version.cjs`).
- `designs/gorod-fm-standalone.html` (5.19 MB, `.scratch/gorod2/regen_standalone.py`).
- `docs/superpowers/HANDOFF-gorod-fm-home-storefront.md` (session-2 top-block).

## Что дальше
- 🟡 owner-confirm: home-рейл default (community vs Twinr) · рейл global vs home-only.
- Привязать ♥/＋/▶ к реальному сохранению («Мой вкус»/избранное).
- Реальные РМГ-ассеты · «Моя волна» AI-таб (relocate `#home-radio`).
- **Push: сделан на sync (feature-branch).**
