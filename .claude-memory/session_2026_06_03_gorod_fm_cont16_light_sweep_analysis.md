# Session 2026-06-03 — Город ФМ cont-16 — Light theme deferred-sweep ANALYSIS (build paused) + sync

## Контекст
- `resume gorod fm` (design-project). cont-15 оставил 13→14 коммитов локально (HEAD `c6a192d`), PUSH held: light theme v1 (dark `cinema` byte-identical, dev-gated, prod forces cinema), weight-cloud, ЛК, standalone 3.07 MB.
- cont-15 NEXT item **B** = light per-surface sweep на вторичных роутах (#/track/#/profile/#/artist/#/podborki/#/lives, +#/recap), wire `--cover-mix-base` seam. Это и взял автономно.
- Mid-session директива Эльбика: **«как агенты дойдут сделай паузу без потерь, продолжим через пару часов»** → остановился ДО билда, захватил анализ durable. Затем `sync`.

## Что сделано
- **Заземление**: подтвердил seam-структуру (`--cover-mix-base` dark `:root` L179 = #111318, light L209 = #FFFFFF, unwired), 3 cover-mix call-сайта (L5790 `#111318`, L5826 `#191C24`, L8941+ ×9 inline `#15171D`), light-override блок L7323-7397 (покрывает только main flows). Прочитал render-контексты #/track (paper-page, не immersive), #/profile (closed-box=намеренно тёмный), #/recap (карточка=shareable, PNG dark O3).
- **6-агентный read-only workflow** `woi5kyh7a` (537k токенов, 6 параллельных агентов, по 1 на роут + shared-chrome safety-net) → структурированный override-спек (selectors/declarations/rationale/lineHint + coverMixSites + inlineStyleIssues + leaveWhite + openQuestions). Schema-forced StructuredOutput.
- **Durable-захват без потерь**: скопировал volatile temp-вывод в repo `docs/superpowers/cont-16-light-sweep-analysis.json` (75 KB, валидный JSON, verbatim). Написал build-ready `docs/superpowers/HANDOFF-gorod-fm-cont-16.md`. Обновил RESUME (cont-16 наверху), DEBT (cont-16 строка).
- **sync**: закоммитил cont-16 docs, **запушил cont-12→16** (снял PUSH-held).
- **TaskCreate ×5** (seam / #/track / #/profile+#/artist / #/podborki+lives+recap-chrome+shared / verify+review+standalone) — pending для next session.

## Решения (locked, все reversible, все держат dark byte-identical)
1. **seam byte-identity**: УДАЛИТЬ `--cover-mix-base:#111318` из dark `:root` L179 → wire каждый сайт на `var(--cover-mix-base, #own-orig-hex)`. Dark → fallback на свой оригинальный hex (byte-identical), light → `#FFFFFF` (flip). Player-scope `--cover-mix-base:#111318` (L7395) КЕЕП (immersive covers). Почему: общий dark-def #111318 на всех сайтах сдвинул бы `#191C24`/`#15171D` → нарушил byte-identity.
2. **#/profile**: `.profile-box--closed` остаётся ТЁМНЫМ (намеренный «мёртвый чёрный ящик»). Все text-флипы scoped на `.profile-box--open`. Агент поймал: cont-15 заметка «faux→ink» — ЛОЖЬ (правила нет, не нужно т.к. closed тёмный).
3. **#/recap**: 9:16 карточка остаётся ТЁМНОЙ (WYSIWYG с PNG-экспортом O3) — pin dark-палитру в `.recap-card` scope (как player chrome). Флипается только chrome + screen-level дельты/discovery-panel.
4. **#/track lyrics = paper-ink** (inactive→`--text-ter`, active→`--text-pri`). Страница = paper, immersive только арт-обложка.
5. **#/artist track-cover = синий fill**: JS задаёт cover bg inline `var(--surface-1)` (L15182) = бел-на-бел в light (latent-баг!) → fix inline на `var(--brand-blue-light)`.
6. **chrome strategy = light-glass repaint** (Apple-day дефолт, Apple Music light = светлый chrome). 🟡 Эльбик может выбрать dark-rail (re-assert dark на topbar/sidebar/tabbar) — open question.

## Находки агентов (важные course-corrections)
- **#/podborki gallery = МЁРТВЫЙ КОД**: `initPodborki()` ищет ID (`podborki-chip-row`/`-gallery-desktop`/`-mobile`/`-row-1/2`) которых НЕТ в разметке. Live `#/podborki` = «Открыть» discover-surface (`.discover-*`/`.shelf-*`/`.mediateka-*`/`.tcloud-*`), почти весь пропатчен cont-15. Осталось 3 правила: `.discover-input` typed-text #fff, `.discover-track-why b` #cdd4f5, `.discover-map-node.is-known` rgba-white. (`.discover-ask-go:focus-visible` — VERIFY vs существующий L7365, возможно дубль.)
- **latent-баги light-only** (prod forces cinema → не client-visible, но чиним): #/artist track-cover бел-на-бел; #/track history-row L9054 (`var(--surface-1)` cover + rgba-white mono).
- **immersive-dark self-paint surfaces leave-white** (тема корректна): why-pop, ai-dock, ai-launcher (blue fill), ai-ribbon, np-transition/TwinrTransition (flat #111318, НЕ color-mix → не seam-кандидат), account-backdrop.
- **canvas** `<canvas id="discover-map">` рисуется JS dark-RGB → может нужен JS-side light-палитра (out of CSS-scope, flagged).

## Блокеры / компромиссы
- **Билд НЕ начат** — пауза по директиве Эльбика ДО любого edit `gorod-fm.html` (0 diff). Это намеренно, не блокер.
- `--text-ter` lyrics ≈3.0:1 на paper — ок для decorative 36px de-emph; bump→`--text-sec` если нужен AA-as-content.
- #/lives `#ff3b30` red pill — НЕ ломается в light (бел-на-красном ок), retint на синий = отдельный single-accent pass, out of scope.

## Файлы
- `docs/superpowers/HANDOFF-gorod-fm-cont-16.md` (новый, 15 KB) — build-ready спек.
- `docs/superpowers/cont-16-light-sweep-analysis.json` (новый, 75 KB) — verbatim 6-агентный аудит.
- `docs/RESUME_PROMPT.md` (mod) — cont-16 блок наверху.
- `DEBT.md` (mod) — cont-16 строка.
- `designs/gorod-fm.html` — **НЕ тронут** (0 diff).
- standalone — **не пересобирал** (primary не менялся; current = cont-15 `8199bed`).

## Что дальше (next session execute)
START = `docs/superpowers/HANDOFF-gorod-fm-cont-16.md`. Порядок: Step 0 (seam delete L179 + wire 12 cover-mix + 1 artist inline) → Step 1 (append 6 override-блоков после player-chrome L7397) → `node .scratch/check_scripts.cjs` → Chrome :8770 `?dev=1` light-walk 6 роутов + подтвердить dark byte-identical → adversarial multi-lens review (dark-regression/light-completeness/honesty) → fold → standalone regen `tools/build_gorod_fm_standalone.py` → DEBT/RESUME. НЕ перезапускать `woi5kyh7a` (анализ в JSON). 🟡 Эльбик: chrome light-glass vs dark-rail · GOROD-029/030.
