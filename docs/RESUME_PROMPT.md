# Resume Design — Активация сессии

## ⚡ LATEST (2026-06-10 вечер) — Monte Carlo (РМГ): промо-блок на главной, 7 концептов в клиентской фигме, ждём выбор клиента

**Новый трек:** редизайн montecarlo.ru, чат «DFM» (Stas Skalaban, Alexei Shelest; читать telethon'ом mama-helper — `scripts/_read_dfm_chat.py`). Figma `Monte-Carlo` key `l38kZVrZXzdNlBIIOLFX4g`, страница «Adaptive», рабочая главная = `3895:1991` (⚠️ Эльбик перестраивает канвас — node-ids протухают, перед работой инвентаризация).

**Сделано (всё в клиентской фигме, в репо кода нет):** промо-блок 3×16:9 из реальных баннеров прода → 8 итераций по фидбеку чата → футер 1:1 (векторные лого холдинга, ссылки, ©, 12+, бейджи сторов, live-токены `#96A0AA26`+blur25) → карпати-ресёрч (4 агента) → 7 концептов: **жизненный цикл дока** язычок `4106:1729` ↔ peek 90px `4105:1700` ↔ развёрнут `4126:1932` · **ротатор-фаворит** `4106:1918` · luxury-ряд `4114:1787` · орнамент `4115:1816` · в плеер: этаж `4122:1845` / хвост `4123:1874` / companion `4123:2064` · полные страницы `4096:1820`/`4099:1878`. Констрейнты чата: в центре максимум 1 баннер (Alexei) · плеер не перекрывать · ниже фолда не работает · справа Яндекс-слот · «чтобы немного показывался» (Stas) · скрываемость с язычком (Alexei).

**🔒 NEXT = гейты Эльбика:** выбор концепта + ответ в чат (в чат сами НЕ пишем) → удалить непринятые фреймы; маркировка «Реклама»+erid для платных; вопрос Алексею про P5-угол vs Яндекс. Полная история: `.claude-memory/session_2026_06_10_montecarlo_promo.md` + DEBT.md «Monte Carlo» (MC-001..007) + shared `project_design_montecarlo_rmg.md`.

---

## ⚡ PREV (2026-06-10) — Twinr + CRM Турбо: правки Татьяны (@k_t_v_23) СДЕЛАНЫ И ДОСТАВЛЕНЫ, SYNCED+PUSHED

Бриф снят telethon'ом из её чата (после `twinr-icons.zip` 08.06). Сделано+reviewer-verified (1 HIGH+3 MED закрыты): **Twinr** — моб-адаптив (off-canvas+бургер, рейл на мобиле скрыт; LG-008 phantom-scroll закрыт) · favicon/лого twin-panes (`assets/twinr-brand/`) · **Wordstat «Графики»** (3 glass-чарта «Активный гражданин») · **«Аудио Метрика»** (отчёт+«Выходы трека», nav СЛЕДОМ ЗА Статистикой; иконки `assets/twinr-icons/`). **CRM** — кебаб «Создание»/«Медиа»; подложка уже была. Полный трекер: DEBT.md «Twinr + CRM Турбо… 2026-06-10» (KTV-001..009 done) + session log `.claude-memory/session_2026_06_10_twinr_crm_katya.md`.

🚨 **Урок сессии:** «Аудио Метрика» сначала ошибочно строилась в CRM — плитка «CRM Glass / turbo-performance.ru» на скринах Татьяны = переиспользованный их вёрсткой ШЕЛЛ, не признак проекта. Их живой Twinr (dev.twinr.ru) выглядит как наш CRM-шелл. **Проект определять по семантике данных** (радиостанции/прослушивания=Twinr; ресурсы/эфирные справки=CRM). Перенос `b4adcc6`.

**Доставлено ей файлами без текста (команды Эльбика):** CRM-zip msg 589661 (15:01) · twinr-zip v2 msg 589663 (15:05, актуальный; v1 589650 устарел). Архивы: `deliverables/2026-06-10/`.

**🔴 NEXT:** только backlog — TD-KTV-01 (a11y labels twinr, 37 полей) · TD-KTV-02 (sticky thead в .t-wrap) · ждать фидбек Татьяны после деплоя («запущу тебя посмотреть, может что-то надо будет поправить»).

---

## ⚡ PREV (2026-06-03 cont-16) — Light theme **deferred secondary-route sweep**: 6-агентный read-only АУДИТ ГОТОВ, билд НА ПАУЗЕ (Эльбик: «как агенты дойдут — пауза без потерь, продолжим через пару часов»). **`gorod-fm.html` НЕ тронут, рабочее дерево чистое, 13 коммитов локально ahead (HEAD `c6a192d`), PUSH ДЕРЖИТСЯ.**

**📖 START NEXT: `docs/superpowers/HANDOFF-gorod-fm-cont-16.md`** — build-ready спек (Step 0 seam+inline edits · Step 1 готовые CSS-блоки по роутам · locked-решения · open-questions · execution order). **Raw аудит (НЕ перезапускать workflow — 537k токенов): `docs/superpowers/cont-16-light-sweep-analysis.json`** (6 роутов, каждое правило + rationale + line-hints).

**✅ СДЕЛАНО cont-16 (только анализ + durable-захват, БЕЗ кода):** 6 параллельных агентов прошли #/track · #/profile · #/artist · #/podborki · #/lives+#/recap · shared-chrome → структурированный override-спек. Ключевые находки: (1) **#/podborki gallery = DEAD CODE** (live-роут = «Открыть» discover-surface, почти весь уже пропатчен; осталось 3 правила); (2) **#/artist latent-баг** — track-cover bg задаётся inline `var(--surface-1)` (L15182) = бел-на-бел в light → фикс inline на `var(--brand-blue-light)`; (3) **#/profile** подтверждён closed-box-остаётся-тёмным, а cont-15 заметка «faux→ink» ЛОЖНА (правила нет, не нужно); (4) **#/recap** карточка остаётся тёмной (WYSIWYG с PNG O3), флипается только chrome; (5) **chrome strategy** = light-glass repaint (Apple-day дефолт, reversible) — 🟡 Эльбик может выбрать dark-rail.

**🔴 NEXT (execute spec из cont-16 handoff):** Step 0 (удалить `--cover-mix-base` из dark `:root` L179 + wire 12 cover-mix сайтов на `var(--cover-mix-base, #orig)` → dark byte-identical + 1 artist inline) → Step 1 (append 6 override-блоков) → `node .scratch/check_scripts.cjs` → Chrome `?dev=1` light-walk + dark-byte-identity → adversarial review → standalone regen → DEBT/RESUME. **PUSH держится до `sync`.**

---

## ⚡ PREV (2026-06-03 cont-15) — «ДОДЕЛАЙ ВСЕ ДОЛГИ»: light theme v1 + ЛК + standalone-regen + weight-cloud. **6 коммитов локально (`0aae4c1`..`8199bed`), PUSH ДЕРЖИТСЯ до `sync`.**

**📖 ПОЛНЫЙ хендофф: `docs/superpowers/HANDOFF-gorod-fm-cont-15.md`** (всё + NEXT + deferred + Эльбик-решения).

**✅ СДЕЛАНО (committed, verified Chrome 0-errors):** weight-cloud `09704df` (cont-14) · **light theme v1** `36a688e` (Apple-grade, ADDITIVE, dev-gated — dark `cinema` BYTE-IDENTICAL; `html[data-theme="light"]` token-блок + unlayered per-surface overrides + 2 canvas-ветки + toggle; имя `light`; прод форсит cinema → клиент не видит; все 7 §8 критик-фиксов) · **ЛК account-sheet** `ca20b28` (топбар «Личный кабинет» → модалка: Twinr-ID pointer + theme-pills + demo-labeled История/Export/Delete/Logout) · **review-фиксы** `b2bb18f` (4-линзовый wf `w5iwcj491`: закрыты light-дыры на main-flows taste-saved/discover-results/cloud-strip; Светлая-pill dev-only в проде; setTheme CarPlay+wave) · **standalone** `8199bed` 3.07 MB (regen из dev, Pillow). **«Сохранённое»+#/artist — verified already-shipped** (реал-контент артиста = Ф1+ needs-assets, НЕ фабрикую).

**🔴 NEXT:** **A.** PUSH @ `sync`. **B.** light deferred sweep вторичных роутов (#/track/#/profile/#/recap/#/artist/podborki-gallery/#/lives — hardcoded dark surfaces/white text; wire `--cover-mix-base` seam). **C.** standalone GorodTasteSeed-aware inline (cloud-фото runtime-concat, ~38 refs не заинлайнены → офлайн flat-fallback). **D.** backlog #/artist real-content (Ф1+). Детали → `HANDOFF-gorod-fm-cont-15.md`.

---

## ⚡ PREV (2026-06-03 cont-14) — #/taste **«Облако вкуса»** weight-editable bubble cloud DONE + 5-линзовый adversarial review + verified Chrome. **Коммит `09704df` локально (поверх cont-13), PUSH ДЕРЖИТСЯ до `sync`.**

**✅ СДЕЛАНО (committed `09704df`, verified :8770 0-errors):** Заменил row-stack редактор #/taste на **packed-bubble облако** где РАЗМЕР шарика = вес интереса (diameter ∝ √weight, area-honest). Тап → docked `[− pips +]` stepper (5 нотчей); радиус анимируется, форк discover-физики reflow-ит соседей. **РОВ-фикс: веса PERSIST в новый `gorodfm_weights`** (раньше пересобирались из pick-order каждый load → правки умирали = control-theater). Честный per-facet provenance: **you** (задал: точное n/4 + синее кольцо) / **pick** (в твоих выборах: «по выбору») / **demo** (DEFAULT: «демо» pill) / **rejected** (lock+min, struck). Segmented control (Жанры/Артисты/Настроения/Эпохи, ≤6), артист-фото, «Списком» fallback + reduced-motion static, full a11y (role=slider/aria-labelledby/valuetext/keyboard). **4 критик-фикса все применены** (no fabricated «heard»; SR % только src=you; re-entrancy safe — persistWeight МОЛЧИТ; #taste-delta не клоббер). **5-линзовый ревью → фиксы:** matchSponsor исключает rejected (держит обещание reject-card «волна избегает»); SR digest you-set first; убран latent фейк «за неделю» из HTML; closeStrip flush; cStart retry cancellable; dead PIN/cByName удалены. **Девиации от спека (все к честности):** убран no-op 📌 pin (theater без eviction), docked strip вместо floating (избегает cont-13 focus↔physics лага), area ∝ реальный вес вместо квантованного level. Поймал+пофиксил баг load-order (ARTIST_IMG строился до GorodTasteSeed) + strict-mode ReferenceError (stray cByName).

**🔴 NEXT:** **A.** **Standalone mirror** — `gorod-fm-standalone.html` НЕ зеркалит cont-13 (taste-cloud/carousel/popular/genre-фото) НИ cont-14 (weight-cloud). Нужно: скопировать IIFE+CSS из dev, base64-инлайн genre-*.jpg + artist .png. `.scratch/rebuild_standalone_full.py` стал. **B.** backlog cont-12: #/artist enrich · «Сохранённое» группировка · ЛК account-sheet · light-theme (`SPEC-gorod-fm-light-theme.md` готов). **C.** **PUSH всё при `sync`** (cont-13 6 коммитов + cont-14 `09704df`).

**🟡 Эльбик-gate:** GOROD-029 онбординг-eyebrow «ПЕРВЫЙ AI» · GOROD-030 лицензии. Артефакты cont-14: спек `docs/superpowers/SPEC-gorod-fm-taste-weight-cloud.md` (реализован с 4 фиксами); review-workflow `wuobrjxae`.

---

## ⚡ PREV (2026-06-03 cont-13) — Discover taste-cloud + carousel polish + popular bubbles + genre-фото. **коммиты локально, PUSH ДЕРЖИТСЯ до `sync`.**

**📖 ПОЛНЫЙ хендофф: `docs/superpowers/HANDOFF-gorod-fm-cont-13.md`** (всё сделанное + NEXT + решения за Эльбиком).

**✅ СДЕЛАНО (committed, verified Chrome 0-errors):** (1) cont-12 ОТКРЫТЬ rebuild + 2 player-фикса залочены; (2) **Discover taste-cloud** (build+bloom+honest counter, форк GorodTasteCloud/GorodTasteSeed, онбординг не тронут); 🔴 **ЛАГ ИСПРАВЛЕН** (был `focusin→stop()` rAF-гейт; убран, физика=онбординг); (3) **карусель** Apple-fade+arrows + фикс выравнивания тайлов; (4) **«ПОПУЛЯРНО СЕЙЧАС»** 6 hue-free trend-chip + anti-clog **graduate-out** (флаг `GRADUATE`) + reshuffle + counter→#/taste; (5) **реальные фото ВСЕМ genre-шарикам** (12 Unsplash, онбординг+cloud, group/artist уже на real-assets).

**🔴 NEXT:** **A.** #/taste weight-cloud (spec `SPEC-gorod-fm-taste-weight-cloud.md` готов, verdict=revise — 4 критик-фикса: hasRealSignal()=0-арг / SR-% leak / selfDispatch-loop / #taste-delta clobber). **B.** Standalone mirror (ВЕСЬ cont-13 НЕ зеркалён; ⚠️ `.scratch/build_tcloud.py` СТАЛЫЙ — без лаг-фиксов, копировать IIFE из dev). **C.** backlog: artist-enrich/Сохранённое/ЛК/light-theme/sections. **D.** PUSH при `sync`.

**🟡 Эльбик-gate:** graduate-out (пики исчезают с canvas → #/taste; `GRADUATE=false` если оставлять) · Figma имеет только cover 540×320 (genre-фото взяты из инета) · GOROD-029/030.

---

## ⚡ PREV (2026-06-03 cont-12) — ВИЗУАЛЬНЫЙ АУДИТ всего сайта (Chrome MCP) + 2 фикса плеера → залочено в cont-13 `5d43896`/`d2e6939`

🎯 Эльбик: (1) «визуальный аудит всего сайта через mcp chrome — соответствует ли плану» → (2) «внизу странная полуобрезанная Believer-плашка — не пофиксили на норм плеер?» → (3) «галерею переоформи + рассинхрон пофикси, потом пушни и комить» → **прервано до завершения**.

**📖 ПОЛНЫЙ хендофф: `docs/superpowers/HANDOFF-gorod-fm-cont-12.md`** (аудит + детали фиксов + анкеры + план).

**Аудит — ГОТОВ. Вердикт: сайт СИЛЬНО соответствует плану cont-9→cont-11** ✅ (все 8 экранов + плеер сверены с per-surface спеками через 10-агентный workflow; единый синий акцент 0 cyan/violet/red, Onest, плоский анти-слоп, поведенч. «почему» везде, demo-честность, 0 console errors, TWEAKS/#/map gated).

**🟢 СДЕЛАНО (working tree, НЕ закоммичено):**
1. **Мини-плеер был перекрыт — ФИКС ВЕРИФИЦИРОВАН (Chrome), в ОБОИХ файлах.** `#home-bottom-sheet` (легаси шторка, z65, h480, якорь bottom:72px) закрытым `translateY(100%)` оставлял 72px-полоску поверх `.player-mini` (z60) = «обрезанная Believer-плашка». Фикс: `transform: translateY(calc(100% + var(--player-mini-h)))` (CSS `.home-bottom-sheet` ~L4059 в `gorod-fm.html`+`gorod-fm-standalone.html`). Низ всех роутов теперь = `#player-mini`.
2. **Рассинхрон now-playing — ФИКС ТОЛЬКО dev, НЕ верифицирован, НЕ в standalone.** мини=Слеза/Егор Крид vs полный плеер=Believer/Imagine Dragons (оба статик-HTML). Добавлен `syncFullPlayerFromMini()` (`gorod-fm.html` ~L10865) — копирует title/artist/cover мини→полный (`#player-full-title/-artist`, карусель-центр, реальная обложка вместо концентр-плейсхолдера); зовётся на клик мини-бара+tabbar (НЕ трогает artist/track-radio флоу).

**🔴 NEXT (в порядке):** **A.** Gallery-restyle `#/podborki` (НЕ НАЧАТ): ядро = `.podborki-tile-label` CSS **L4426** `font-weight:900; font-size:36px; uppercase; transform:rotate(-90deg) scaleX(1.05)` (повёрнутые/растянутые подписи, наруш. GDS-19). Галерея `.podborki-gallery` L~7875, тайлы `.podborki-tile` L7883+/CSS L4360 (h628), чипы `.podborki-chip` L4193. Развилка: В1 де-ротация (горизонт. label 700/≤24px, фото kept) | В2 flatten в `.discover-ed-card`-стиль. Discover-редизайн задумывал галерею→«От редакции» (уже есть). **РЕШИТЬ с Эльбиком.** · **B.** Верифицировать Фикс #2 в Chrome · **C.** Зеркалить Фикс #2(+gallery) в standalone · **D.** Commit + push ВСЁ.

**🟡 Прочее (не блокеры):** онбординг eyebrow «ПЕРВЫЙ AI» = GOROD-029 gate; профиль показывает дефолт-вектор как «ТВОЁ» без demo-лейбла пока recap честно гейтит.

**git:** working tree грязное (`gorod-fm.html` + `gorod-fm-standalone.html` изменены, НЕ закоммичено — файлы на диске сохранены). Сервер :8770 был запущен.

---

## ⚡ PREV (2026-06-03 cont-11) — МИНИ-ПЛЕЕР ПЕРЕДЕЛАН (PRIORITY #1) + play/pause fidelity-баг + **ВЕСЬ AUDIT-backlog ЗАКРЫТ** (G2/G6/G7/route + 8 per-surface волн) + **плеер locked calm-blue (Variant A — color-from-art retired)** + standalone. **ЗАПУШЕНО origin/master** (~15 коммитов cont-11, HEAD `42d1902`+)

🎯 **Эльбик cont-10 флаг (×2): «плашка внизу как плеер — UX/UI ресёрч Карпати-уровня».** Сделано research-first.

**Процесс:** grounded живой код (анкеры дрейфанули) → Karpathy-workflow `wa8ncwxs9` (4 параллельных best-practices-researcher: Apple Music mini / Spotify+YT+Яндекс «Моя волна» / иерархия-progressive-disclosure / web-impl-a11y → synthesis-спек → **adversarial critic verdict=revise с 8 fix-ами**, все вплавлены) → **AskUserQuestion: Эльбик выбрал Вариант A «минимум»** → билд atomic-splice (`.scratch/apply_minibar.py`, 21 замен, assert count==1) → Chrome-проба (JS computed-styles, не только скрин) + 0 console errors → коммит `298010e`.

**Что сделано (мини-бар `.player-mini`, web — главная поверхность):**
- 84→**72px**, материал `rgba(11,12,15,.72)+blur28 saturate1.2`+top `--hairline`; обложка 60→**48px** `--r-sm`; title 15→**14/600**, artist 13/400 (+line-height 1.15 — честный vertical-fit).
- **Двойное «почему» → ОДНА строка-кнопка** `.player-mini-reason` (`<div>`→`<button>`, tier-1 content не pill-chrome; тап → существующий `#why-pop` reject-loop). **Wedge прозрачности СОХРАНЁН** (3 поверхности→1, не удалён). Critic подтвердил.
- Транспорт = **play (залит синий 32px круг, ЛЕВЫЙ/главный) + next (ghost)**; **prev/steer/share/volume УБРАНЫ с бара** (не осиротели: prev→full-sheet, steer→home/discover dials, share→full-player action-row `data-tab="share"`, volume→OS). Apple-конвенция play-слева (отклонился от synthesis «play-rightmost» — обосновано).
- 🐛 **play/pause fidelity-баг ИСПРАВЛЕН** (был: mini=▶triangle vs full=⏸bars, оба БЕЗ хендлера): ОДИН `playerState.isPlaying` → `renderPlay()` driver на `#btn-play`+`#player-full-play`+`#track-page-play` через `aria-pressed`+dual-glyph swap. Проверено: все 3 синхронны до/после клика. Bridge `{next,prev,toggle,setPlaying,isPlaying}` (убрал коллизию `play`=advance).
- a11y: APG toggle (статичный label + aria-pressed), 44px hit через `::before{inset:-6px}`, focus-visible `--accent-on-dark`, `@supports`/`prefers-reduced-transparency` opaque-fallback, **web-scoped** `env(safe-area-inset-bottom)` (critic: не дабл-каунтить на mobile над tabbar).

**Дисциплина/находки:** web-surface override `html[data-surface="web"] .player-mini` (L7156) перебивал base padding → правил отдельно (0 20px + safe-area). Mobile-surface `[data-surface="mobile"] .player-ctrl-btn` (вкл. pre-existing min-height:44 L6140) **НЕ применяется** даже с `!important` — глубокий pre-existing cascade-quirk в том блоке; но oval-проблемы НЕТ (min-height не берётся → кнопки 32px square + 44px hit через ::before). Не копал дальше (dev-only surface). Артефакты: `apply_minibar.py` (.scratch, gitignored), research-output в task `wa8ncwxs9`.

**✅ ВЕСЬ AUDIT-backlog ЗАКРЫТ** (директива «доделай все долги»). 13 атомар-коммитов, каждый node --check 0 + Chrome. Грунт-инвентарь: `docs/superpowers/REMAINING-cont11-debt-plan.md` (parallel-workflow `w9js8v96c`, 108 items → 12 волн). **Done:**
- **G2** `--brand-cyan` 42→**0** (alias-токен удалён) — refs→`--brand-blue-light`, малый текст→`--accent-on-dark`.
- **G7** все focus-rings→`--accent-on-dark` (3px blue-light 47→**0**, 62 unified, AA) + reduced-motion `:active{scale(.98)}` на интерактив-семьях + 44px hit-area (`::before{inset:-6px/-9px}`) на sub-44 (discover/ai/taste controls).
- **G6** anti-slop: LIVE flat (taste saved-tint hsl 2-stop→flat · ai-dock violet→синий · artist row-orb→top-light · 9 track-history covers→flat `--np-accent`) + dead neutralized (16 favorites + 6 library thumbs, #1ecfe0 leak killed) + 3 mini-art placeholder gradients удалены. linear-gradient 86→50.
- **DEFAULT_ROUTE** cold-start (нет onboarded&taste)→`#/onboarding`; returning→`#/home`; deep-links целы — 3 пути verified в Chrome.
- **8 per-surface волн:** home (hero cover-glow→neutral, удалён home-only mini-bar tint, skip/Like/Steer hierarchy, hero token+dvh-clamp) · taste (2nd blue CTA «Открытый профиль»→ghost, streak-pulse off, delta green→neutral) · discover (ASCII ▶→SVG, ask-field hover/focus-ring, curator/section-title) · track (lyric `#545454`→`rgba(255,255,255,.45)`, cover-shimmer удалён) · artist (per-row tintFor→flat covers, AA metadata) · onboarding (neon-ring→clean, vec-fill solid, count AA) · recap/profile (`#6d80ff`→token, clear-player padding 120) · chrome (topbar `filter:brightness`→bg).
- **standalone** пересобран со всеми волнами (`e12a58b`, 34 webp inline, cyan=0) — rebuild = `python .scratch/rebuild_standalone_full.py` (ре-применяет wave_*.py к standalone, retarget path).
- **🎨 Wave M — плеер locked calm-blue** (`42d1902`, Эльбик Variant A): «цвет-от-обложки» (--np-accent/GOROD-042) сэмплил красный с обложки Крида → красный progress + red glow-ореол на #/track. Локнул `--np-accent`=#5168FC (стоп сэмплинг), убрал цветные glow-ореолы (track cover + np-transition, §0.5), progress=фикс синий. **0 красного, один синий акцент.** dev + standalone.

**Информированно отложено (low-value/risk, НЕ prod-visible):** `scaleX` ×12 = бренд-вордмарк ГОРОД.FM (intentional Actay-Wide-стретч, НЕ трогать) + dead hidden-tile/dev labels · chrome sidebar-row-geometry + tabbar split-indicator + topbar contextual-title (med-risk, низкая ценность) · recap glyph→SVG (✓▲−→) · P2 render-identical токенизации (raw hex == token value) · dead library/favorites CSS-rule блок-deletion (градиенты уже neutralized) · taste saved-rows interactivity (honesty — текст-claim можно убрать).
**PUSH при `sync`.** 🔒 Эльбик-gate (НЕ Claude): GOROD-029 позиционирование · GOROD-030 лицензии.

---

## ⚡ PREV (2026-06-02 cont-10) — FULL-DESIGN BUILD 11/11 ЗАВЕРШЁН + APPLE-POLISH PASS (player+tweaks complaints RESOLVED). Всё локально (master), PUSH отложен

🎯 **Эльбик cont-10:** «делаем чисто дизайн всех экранов/структуры с ресёрчей» (→ доделал build 5 шагов), потом mid-session: **«сделай аудит всех модулей + карпати-ресёрч UI/UX, доведи каждую страницу до идеала, стандарт apple; плеер выглядит страшно; артефакт tweaks остался»**.

**A) BUILD 11/11 ЗАВЕРШЁН** (5 коммитов): artist `8607e9a` (#/artist deep-dive: art-tint hero+поведенч.«почему»+reject→общий corpus) · onboarding `ac4e053` (модель за N сигналов + import-seed) · recap+profile `e15612f` (R1 дельта-герой/R2 honest PNG Canvas-2D/R3 причинная CTA/P1 reject-провенанс) · Integrate-A `807f235` (#/library+#/favorites→#/taste redirect + tabbar 3-tab) · Integrate-B `59689be` (cyan 55→0, single accent). Каждый: 18-19 JS node--check ✓ + 0 console errors + Chrome-probe.

**B) APPLE-POLISH PASS** (17-агентный workflow `wxpohqba5` → `docs/superpowers/AUDIT-apple-polish-plan.md` = build-ready Apple design-system §0 + per-surface P0/P1/P2 + execution order). Исполнено (7 коммитов + standalone):
1. `08b2cf1` tokens §0 (type-scale/8pt/nested-radius/surfaces/shadow/motion, text-sec .70→.62, bg-base FLAT) + **warm theme RETIRED** (§G3) → убрал оранжевый «мир» плеера.
2. `55709ac` **dev-gate §G4** — TWEAKS-панель + theme-toggle + internal #/map скрыты в проде; reveal `?dev=1` (sticky)/`?dev=0`/`Ctrl|Cmd+Shift+D`; дефолт-роут → #/home (не internal map); «Карта флоу» из nav убрана. **complaint #2 RESOLVED.**
3. `cec1679` **player redesign §1A** — flat cover (был purple→magenta gradient), inset rounded window (был full-bleed + harsh .4 white border), blue scrubber (был orange/red), solid-blue 64px play, title/actions БЕЗ overlap, sentence-case artist. **complaint #1 «страшно» RESOLVED.**
4. `8344ab1` P0 batch1 — nav active = blue left-rail · onboarding genre-bubbles flat (был full-hue gradient) · artist avatar circle+blue-ring→rounded-square+hairline, name 56/900/CAPS→48/700 mixed-case.
5. `1004f0e` P0 batch2 — profile neon-glow→border · home white-orb halo→subtle brand radial · featured-CTA purple #2d2d5d→neutral.
6. `cabe496` taste 📌-emoji→blue inset-accent · discover «Рядом» gradient cards→flat+hairline.
7. `77db4d0` standalone 2.55 MB пересобран.

**KEPT by design (override audit P0):** «демо-вектор/демо-карта/демо-архив» fidelity-лейблы — north-star (никогда не выдавать демо за реальное) > visual-declutter.

**🎯 NEXT-SESSION ПРИОРИТЕТ #1 — нижняя закреплённая плашка (мини-плеер `.player-mini`):** Эльбик флагнул отдельно (cont-10) — переделан только ПОЛНЫЙ плеер (§1A full), **мини-бар НЕ доведён**. Сейчас 84px, перегружен: always-on `.player-mini-reason` строка-причина + **ДУБЛЬ «почему?»** (pill + `.player-why-pill`) + cover + title/artist + 3 transport + Steer + volume + share в одном баре. **Мандат: Карпати-уровня UX/UI ресёрч now-playing-bar (Apple Music mini / premium mobile-first) → редизайн по AUDIT-plan §1A «Mini bar»** (72px, убрать reason-строку → ОДИН «почему?»-pill, play=синий 32px круг, prev/next ghost, stateful play/pause sync mini↔full). **Research-first.** Детали grounded → `docs/superpowers/HANDOFF-gorod-fm-cont-10-apple-polish.md` (раздел NEXT-SESSION PRIORITY #1).

**REMAINING (backlog, всё в `docs/superpowers/AUDIT-apple-polish-plan.md` §2):** G6 полный slop-sweep (mini-art placeholders L619-621, остаточные gradient-covers, map thumbs) · G7 global focus/active/44px pass · per-surface P1/P2 (discover map axis-labels/nodes, track lyrics-контраст #545454 + hero-cover cap, taste радиусы/2 синих CTA, recap/profile token-migration, **map/lives под dev-gate** — #/lives dead cards + #ff3b30 red, copy-register «вы») · **DEFAULT_ROUTE cold-start→#/onboarding** (ВОЛНА-0) · 42 latent `var(--brand-cyan)` alias-рефа (рендерят синим; G2 полный rename→0). Порядок: AUDIT-plan §3.

**Дисциплина:** `?dev=1` для просмотра TWEAKS/map; re-grep якоря перед edit (дрейфуют); `?v=N` cache-bust; :8770 жив; PUSH отложен до `sync`; `gorodfm_*`/`gorod-fm.*` LS-ключи чистить после probe. START следующей сессии = этот блок + AUDIT-plan §2/§3.

---

## ⚡ PREV (2026-06-02 cont-9) — FULL-DESIGN BUILD: 6/11 шагов DONE (3 главные вкладки + deep-dive Трек). Всё локально (master), PUSH отложен

🎯 **Директива Эльбика (таймер 1ч10м → автономный мультипоточный билд):** «делаем чисто дизайн всех экранов и всей структуры что с ресёрчей вернулась». Мультипоточный spec-workflow (`w7jr5nat0`) выдал 7 per-surface спеков + **`SPEC-00-foundation-and-integration.md`** (build-order orchestrator). Реализую ПОСЛЕДОВАТЕЛЬНО в main loop (single-file → нельзя параллельно писать) + Chrome MCP визуал-проверка каждого. Каждый верифицирован (node --check + 0 console errors + browser-probe) + атомарный коммит.

**✅ СДЕЛАНО (6/11, HEAD `9537540`):**
1. Foundation `57b5b41` — cyan token-swap (`--brand-cyan`→#5168FC, 56 var-refs синие) + `window.openPlayer` мост.
2. W6 `3769cc1` — `window.TwinrModel` единый REJ_LABELS-канон (6 ключей +mood/art_arena/art_vocal_m), 3 потребителя делегируют. **Вставлен РАНО (перед wave-IIFE)** — спека @13660 сломала бы GorodTaste.
3. home 045 `6aff252` — 3-зонное РАДИО (контекст-карта + hero+ambient #home-wave + ❤/Steer primary/skip secondary); Figma-плитки в `.home-tiles[hidden]` через toggle (откат=1 LS).
4. taste+saved `5b3b0f6` — Сохранённое-аккордеон (GorodSaved) + стрик (053-lite детерм.) + AT-вектор (§10.1).
5. discover 046b `2e7c45a` — карта вкуса (canvas+узлы) + distance-dial (3/6/9) + topbar-search wire + редакторский ряд.
6. track 047a `c62c451` — explainability: art-tint cover + «Почему играет» L2 (reject→общий gorodfm_rejected) + вектор bar-meter + attribute-соседи. **Оставил view-state «cover» (без рефактора контроллера).**
+ standalone `9537540` (2.52 MB, 0 violet).

**⏳ ОСТАЛОСЬ (5 шагов, спеки готовы в `docs/superpowers/specs/`, порядок по SPEC-00 §5):**
7. **artist 047b** (`SPEC-artist.md`) — REPLACE 3 диапазона + initArtist→stub + GorodArtist IIFE (самый большой diff; применять диапазоны СТРОГО сверху-вниз; зависит W6-канон art_arena/art_vocal_m уже готов + openPlayer мост готов).
8. **onboarding** (`SPEC-onboarding.md`) — AUGMENT в GorodOnboarding (Model «7 треков» + Import) + overlay. RK-4: onContinue-handoff → goHome().
9. **recap+profile finish** (`SPEC-recap_profile.md` R1-R3/P1) — дельта-герой + Canvas-2D PNG + provenance reject-чипам. TwinrModel уже стоит (W6).
10. **Integrate-A** — redirect #/library+#/favorites→#/taste в `routeFromHash` (ПОСЛЕ taste — готово); retire tabbar «Медиа»; promo-cards→#/taste.
11. **Integrate-B** — ручной свап выживших hardcoded cyan (home-promo 7298-7469, player, generic) + финальный Grep `#56afd7|rgba(86,175,215)`=0 на видимых.

**ДИСЦИПЛИНА (BR-1/BR-2):** якоря в спеках ДРЕЙФУЮТ — ВСЕГДА re-grep живой файл перед edit, НЕ по номерам строк. Trailing-IIFE вставлять перед `</body>` (не по номеру). Демо-контент → обязательный лейбл «демо-X». Dev-сервер кеширует → `?v=N` cache-bust для визуал-проверки (сервер :8770 жив). PUSH отложен до `sync`. `gorodfm_*` тест-ключи чистить после probe.

---

## ⚡ PREV (2026-06-02 cont-8) — БЛЮПРИНТ ДОВЕДЁН (ship) + de-purple + GOROD-051 + W1 fidelity-петля. Всё закоммичено локально (master), PUSH отложен

🎯 Резюм cont-7 → исполнение. **HEAD `d884221`, 5 коммитов локально на master; PUSH ждёт явного `sync`.** Всё верифицировано Chrome MCP (:8770) + 13/13 `node --check` + zero console errors.

1. ✅ **Блюпринт ДОВЕДЁН** (директива «лучший сервис» ИСПОЛНЕНА): `docs/superpowers/BLUEPRINT-gorod-fm-full-service.md` — build-ready master-план (§0 one-page · §1 IA все роуты · §2 flows · §3 per-surface · §4 AI/recsys · §5 дизайн-система · §6 монетизация · §7 roadmap · §8 gated · §9 конфликты · §10 perf/a11y). Синтез-workflow: до-исследованы 2 недостающих измерения (IA+legacy) → 9 dims + AUDIT + стратег-доки → синтез → **adversarial completeness-critic (verdict=ship)** → finalize. Критик проверил мой код построчно (de-purple реально сделан, warmth жива/корректна, 051 wired, все 12 роутов) + поймал 4 grounding-ошибки синтеза (search уже есть / resume-import уже built / ложный warmth-claim / ложный CarPlay-guard) → пофикшены + добавлено §10.
2. ✅ **de-purple** `5355db8` — violet #8b5cf6 (wave LAYERS + 8 градиентов) → синяя семья (#8094ff / var(--accent-on-dark)). 0 violet (anti-slop P0).
3. ✅ **GOROD-051 контекст-старты** `9788ae9` — `GorodContext` + `TwinrWave.setContext` на #/taste (Утро/День/Вечер/Ночь + Тренировка/Дорога), аддитивно, **НЕ триггерит 045**, honesty-floor suggest-only. + fidelity-фикс сверх спека: pressed-state только при applied-today.
4. ✅ **W1 fidelity-петля** `18d8816` — GorodTaste теперь ЧИТАЕТ `gorodfm_rejected` (был live fidelity-баг): совпавшие грани struck+понижены (Егор Крид 62→12%), все reject'ы в карточке «Отклонено в плеере»; + убран `Math.random` в seed (детерминизм). Замыкает explain→reject→see-in-vector.
5. ✅ standalone 2.41 MB `d884221`.

**СЛЕД. СЕССИЯ (блюпринт §7, ВОЛНА 0 остаток — порядок):**
- 🟢 **GOROD-055-lite reason_tag-эмиттер** (is_synthetic + schema_v): headless append-only лог (track,reason,action,surface,session_vec,ts) на scripted-данных — единственный незаменимый ров.
- 🟢 **W2 steering-provenance**: «следующее почему ссылается на твою последнюю правку» (last_steer key; TwinrWhy dynamic first-reason).
- 🟢 **DEFAULT_ROUTE 3-фикс**: DEFAULT→#/home; cold-start (нет taste И нет onboarded)→#/onboarding ДО savedRoute; #/map,#/lives за флаг (router @~12165).
- Затем 047a Трек deep-dive (effort med; demo-вектор+соседи с лейблом «демо-вектор»).
- 🔒 Эльбик-gate: 045 Волна-3-зоны · 046 IA-реорг (Медиатека/Избранное→Сохранённое) · 047b Артист · 029/030/056.
- ⚠️ Отложено информированно: legacy cyan retirement (`--brand-cyan`/`#56afd7`/`rgba(86,175,215)`) — по блюпринту §5; много на legacy-экранах под IA-реорг.
- **PUSH**: всё локально на master — запушить при `sync`.

---

## ⚡ PREV (2026-06-02 cont-7) — ДВА РЕСЁРЧА (директива «делаем лучший сервис»). Блюпринт-workflow прерван оператором; всё захвачено в durable-доки

🎯 **Эльбик directive cont-7:** «продумай фулл структуру, все страницы и UX/UI ресёрч и по архитектуре на Карпати-уровне — делаем ЛУЧШИЙ сервис». Затем «прерывай что есть и делай передачу».

**Что захвачено (durable, в repo):**
1. ✅ **`docs/superpowers/SPEC-gorod-051-context-starts.md`** — ПОЛНЫЙ build-ready спек GOROD-051 (контекст-старты Утро/День/Вечер/Ночь + Тренировка/Дорога). Модуль `window.GorodContext` на **#/taste** (аддитивно, рядом с волной) + backward-compatible `TwinrWave.setContext` (детерм. amp/speed/энергия/оттенок по контексту; bump/audio не тронуты). time-aware дефолт `getHours()`. **Honesty-floor:** не вести волну без тапа (suggest-only, как GorodRecap). **Доказано НЕ триггерит gated 045** (#/home pixel-perfect не тронут — волна живёт только на #/taste, единственная честная поверхность). localStorage `gorodfm_context`. Вставка: новая `<section class="ctx-strip">` между `</header>` taste-hero (стр. 9632) и `.taste-body` (9634). **→ ГОТОВ К БИЛДУ как есть.**
2. ⚠️ **`docs/superpowers/BLUEPRINT-research-dimensions-partial.md`** — 7/9 Karpathy-измерений full-service блюпринта (workflow `w1lo7vxfi` ПРЕРВАН до синтеза). Захвачены: **core-радио/Волна** (045-phasing + steering), **Открыть/discovery** (karta-vkusa не существует, search=keywords), **wedge/профиль** (wedge = «3 разрозненных острова» TwinrWhy/GorodTaste/GorodProfile — НЕ связаны), **habit/онбординг/recap/social**, **AI/recsys-архитектура** (reason_tag moat, MVP→scale), **дизайн-система** (🐛 нашёл РЕАЛЬНЫЙ баг: один-акцент нарушен — фиолетовый `#8b5cf6` в волне `designs/gorod-fm.html:12927`) + 1 тонкий выход. **НЕ дошли** ~2 из {IA/навигация, legacy-rework Артист-Трек-Медиатека, монетизация} — но они УЖЕ покрыты `AUDIT-gorod-fm-screens-and-service.md` (§2 IA · §1/§4 legacy · §7 монетизация). Синтез + completeness-критик НЕ запускались.

**СЛЕД. СЕССИЯ (START HERE):**
- **A) Доделать блюпринт:** перезапустить сохранённый скрипт `…/workflows/scripts/gorod-full-service-blueprint-wf_dc2f3a03-be5.js` (Workflow({scriptPath})) для полного мастер-дока, ИЛИ синтезировать `docs/superpowers/BLUEPRINT-gorod-fm-full-service.md` из 7 partial-измерений + AUDIT (покрывает 2 недостающих). Структура синтеза — в скрипте (фазы synth/review).
- **B) Или сразу строить GOROD-051** по готовому SPEC (самодостаточен, не ждёт блюпринта).
- **Быстрофикс из ресёрча (можно сразу):** дизайн-агент флагнул фиолетовый `#8b5cf6` в `LAYERS` волны (стр. 12927) — нарушение «один акцент»; заменить на `--brand-blue-light`/оттенок синего (anti-slop).
- Доки-пойнтеры выше = **содержимое ресёрчей**; этот блок = **выводы**.

---

## ⚡ cont-6 (2026-06-02) — AI-радио: P2 **`GOROD-050` еженедельный Twinr-recap + 9:16 шеринг-карточка** DONE + 2-линзовое review (**ship**) + 4 находки пофикшены + PUSHED + standalone пересобран (2.4 MB)

📖 Эта сессия (cont-6): построен новый экран **`#/recap`** (модуль `window.GorodRecap`, decoupled trailing-script). HERO = **детерминированная слово-идентичность** из реального вектора (`buildIdentity`: mood×temp→noun + genitive grain; NO rng/Date в идентичности → fidelity) · genre-**bloom** SVG (лепесток=вес, dominant=белый узел + green grow-ring) · поведенческие **+/− дельты** («−» ТОЛЬКО из реального `gorodfm_rejected`) · 1 неожиданное **открытие** · **defense-receipt** (`--accent-on-dark`). НЕ vanity-числа (ошибка Wrapped). Вход = бывшая заглушка `#taste-share` («Поделиться карточкой») → `#/recap`. Honest share = копирует ТЕКСТ (no fake API). **Cold-профиль** (нет picks И нет rejections) → честный empty-state (без выдуманного провенанса — `hasRealSignal()` гейт). Данные байт-идентичны `GorodProfile` → views не могут разойтись. Commits: `77f4fad` (feat) + `cecbeaa` (standalone+gitignore .scratch). Karpathy-research-workflow + 2-lens review-workflow. 12 `<script>`-блоков `node --check` ✓, zero console errors.

**Следующий автономный P2-остаток:** `GOROD-051` контекст-старты Утро/Работа/Вечер (частично entangled с gated 045) · `GOROD-053` стрики «Дней с Волной» + freeze · `GOROD-054` cold-start импорт-seed. 🔒 Gate: `045` Волна-3-зоны · `047` Артист/Трек (нужны обложки/realign). Carry-over TD (app-wide, не блокер): FALLBACK top-up даёт поведенческий провенанс и для partial-history юзеров (та же про-форма в `GorodProfile` 052) — фиксить в общей модели профиля, не в recap.

## ⚡ PREV (2026-06-02 cont-5) — AI-радио: P1 (048 transition-card · 049 edge-glow) + P2 (052 «Открытый профиль») DONE + reviewer-verified + PUSHED; дальше 045/047 (Эльбик-gate) или P2 loops остаток

📖 **READ FIRST: `docs/superpowers/HANDOFF-gorod-fm-cont-2026-06-02.md`** — полный хендофф (что построено, архитектура модулей, forward-план, gates, демо, constraints). Потом `AUDIT-gorod-fm-screens-and-service.md` §8 (план GOROD-040..057).

🧭 **Эльбик-steer:** строить **AI-радио по VISION** (не legacy-completion). Доверие = fidelity (объяснение = реальный вектор). **«Почему» всегда поведенческая** («дослушал 3×»), не маркетинг. Визуально верифицировать каждый шаг (Chrome MCP).

**Сделано (master, всё PUSHED):** standalone-opt 71→2.1 MB · resume→music flagship · #9 taste-ad · **6-агентный Karpathy АУДИТ** · **P0 5/5** (`040` always-on «почему» · `041` «Исправь причину» L2 · `042` цвет-от-обложки `NowPlayingTint` · `043` slop-kill+realign now-playing→Слеза/Егор Крид · `044` behavioral-copy) · **P1 `046` «Открыть» rebuild** (`GorodDiscover`: разговор+explained-results + taste-adjacency) · **P1 safe-остаток `048` transition-card (`TwinrTransition`: DJ-announce next + поведенческое «почему», accent от обложки) + `049` Twinr edge-glow (заменил always-on орб-пульс → светится только когда говорит) + motion-токены** · **P2 `052` «Открытый профиль» pitch-экран** (`#/profile`: контраст чёрный-ящик-vs-открытый + реальный вектор с провенансом + live-правка с квитанцией + moat-caption; reviewer SHIP-READY; вход с `#/taste`). VISION 1-9 + UX A-H все built.

**Next:** P1 (`048`+`049`) + P2 `052` «Открытый профиль» ВЫПОЛНЕНЫ (reviewer ✓, PUSHED, standalone пересобран). Осталось:
- 🔒 **Gate/realign (нужен Эльбик):** `GOROD-045` **Волна 3-зоны** (audit §3 — ломает pixel-perfect home, **решение Эльбика «насколько ломать»**) · `GOROD-047` Артист/Трек deep-dive + slop-kill (нужен realign на реал-ассеты как плеер, ИЛИ обложки от Эльбика).
- 🟢 **Можно брать автономно:** P2 loops остаток `050`/`051`/`053`/`054` (weekly recap-карточка 9:16 · контекст-старты Утро/Работа/Вечер · стрики «Дней с Волной» + заморозка · cold-start импорт-seed) → P3 backend (`055` reason_tag pipeline = moat · 🔒`056` лицензии CC→MERLIN · `057` B2B taste-ads).
- ⚠️ **TD-GOROD-CTA-AA (backlog, app-wide):** primary-кнопка white-on-`#5168FC` = 4.43:1 (чуть <AA 4.5) — конвенция всех кнопок, не блокер; app-wide фикс `#4A5FE8`.

**Эльбик-gates:** GOROD-029 позиционирование · GOROD-030 лицензии · IA/pixel-perfect (GOROD-045). **Asset wall:** прототип без per-track обложек → GOROD-047 нужен realign/ассеты.

---

## ⚡ ACTIVE WORK (2026-06-02 → next session): Город ФМ AI-product (pivot done, ЗАПУШЕНО)

Город ФМ развернулся в **AI-музыкальную платформу** (визия Эльбика). Весь AI-product слой ПОСТРОЕН + 10 Karpathy-брифов + синтез-доки. **ВСЁ ЗАКОММИЧЕНО И ЗАПУШЕНО** (`origin/master`, HEAD `d4479a3`+).

**📖 READ FIRST: `docs/superpowers/HANDOFF-gorod-fm-ai-product.md`** — полное состояние, архитектура decoupled-модулей (window.GorodOnboarding/TwinrChat/TwinrWave/WaveDials/TwinrRibbon), стратегия (Москва, разворот, лицензирование), open-gates, опции, как запустить демо.

**Готово:** Главная v2 `#/home` · онбординг-пузыри `#/onboarding` (Apple-style рекурс) · Twinr AI чат (explainable/steerable/живой профиль) · native-AI плеер («почему?»+steer) · живая волна + «Мой вкус» `#/taste` · 3-tab IA (Волна/Мой вкус/Открыть) · wave-диалы · between-track лента · audio-reactive волна · **tech-modern restyle** (нейтрал near-black `#0B0C0F` + 1 акцент `#5168FC`). UX-волна **6/6 done**.

🎯 **Рынок = МОСКВА** (не Казахстан). Wedge = прозрачность + редактируемый вкус + объяснимость (не локальность — домашка Яндекса).

При `resume design`:
1. `cd ~/Desktop/design-project` · `git pull` · `git log --oneline -8` (HEAD `d4479a3`+ на top)
2. **Read `docs/superpowers/HANDOFF-gorod-fm-ai-product.md`** (главный артефакт) + `.claude-memory/session_2026_06_02_gorod_fm_ai_pivot.md`
3. Демо: `cd designs && python -m http.server 8765` → `http://127.0.0.1:8765/gorod-fm.html#/onboarding` · `#/home` · `#/taste`
4. **Опции (выбрать с Эльбиком):** (A) добить 3 Figma-экрана GOROD-021 (Медиатека 2385:2924 / Избранное 2535:11151 / Артист 2537:14090) под нейтрал-рестайл · (B) standalone-сборка для инвесторов GOROD-032 · (C) полировка стиля (UI-AUDIT: унификация акцента, ретема, волна за плеером) · (D) реальный бэкенд (Ф1+, по ARCHITECTURE). **Рекомендация: B → A/C.**
5. 🔒 **Эльбик-gate (НЕ Claude):** GOROD-029 принять позиционирование · GOROD-030 лицензирование (7digital/Spotify-SDK + IP-юрист, узкое горло №1).

v2 pixel-perfect (GOROD-021): Главная+Подборки ✅; 3 экрана остаются (старый `HANDOFF-gorod-fm-v2-pixel-perfect.md` валиден для них).

Продолжай автономно — не жди подтверждения. Holy Grail Часть 9 + anti-slop gate перед `done`.

---

## v1 Predecessor — Город ФМ HTML SPA (built 2026-05-27)

v1 site shipped via 16 atomic commits ending `77ee5c1`. 7 routes, Player overlay, Tweaks panel (theme/surface/A-B home variant/hide-flow-map). Standalone: `designs/gorod-fm-standalone.html`. Holy Grail compliant. Full v1 handoff: `docs/superpowers/HANDOFF-gorod-fm.md`. v1 review findings: `docs/superpowers/REVIEW-gorod-fm-2026-05-27.md`. Session log: `.claude-memory/session_2026_05_27_gorod_fm_v1.md`.

v1 pending Эльбик-gate items (still gated, NOT closable by Claude): GOROD-016 (real assets from client — partially superseded since we now have Figma assets), GOROD-017 (показ заказчику), GOROD-018 (Next.js handoff after approval).

---

## ⏸️ Paused work (Эльбик-gated to resume)

**Bootstrap-port** (CRM `crm-bootstrap/` DONE 2026-05-20 + отдан в Telegram; Twinr `twinr-bootstrap/` Phase 0-3 done, **Phase 4 (Customizer) NEXT**). Worktree `.worktrees/feat-bootstrap-port`, branch `feat/bootstrap-port`, **не запушена / не смержена** — preserved as-is. HANDOFF: `docs/superpowers/HANDOFF-bootstrap-port.md`. Twinr Phase 4 не блокирует Город ФМ; вернёмся когда Эльбик попросит.

---

## Общий протокол (для дизайн-работы вне активных HANDOFF)

### 1. Verify Location
```bash
cd ~/Desktop/design-project
```

### 2. Git Sync
```bash
git fetch && git pull
git log --oneline -5
```

### 3. Load Context
Параллельно прочитай (ВСЕ обязательны):
- `CLAUDE.md` — архитектура, экраны, дизайн-токены
- `docs/DESIGN_PROTOCOL.md` — **HOLY GRAIL операционный протокол** (10 частей: brief questions, anti-slop, variations, starters, verifier, decks, deviations, gates)
- `docs/references/anthropic_claude_design_prompt.md` — first-source Anthropic Claude Design System Prompt (всегда сверяться при сомнениях)
- `.claude-memory/MEMORY.md` — история сессий
- `DEBT.md` — что висит

**Принцип после загрузки контекста:** если в любой задаче возникает дизайн-вопрос которого нет в `DESIGN_PROTOCOL.md` — сверять с anthropic prompt и брать их подход если он лучше. Не спрашивать разрешения.

### 4. Check Current State
```bash
ls designs/          # основной прототип
ls designs/themes/   # варианты тем
```

### 5. Status Report
Выведи таблицу с метриками + последний коммит.

### 6. Continue Work
Продолжай работу автономно. Не жди подтверждения.
