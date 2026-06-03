# HANDOFF — Город ФМ · cont-12 (2026-06-03) — Визуальный аудит + 2 фикса плеера (ПРЕРВАНО, НЕ закоммичено)

> **READ-FIRST.** Self-contained. Сессия прервана оператором («прерви без потерь, передача в след сессию») ПОСЛЕ аудита + 2 фиксов, ДО завершения gallery-restyle и до commit/push.
> Файл: `designs/gorod-fm.html` (~14.7k строк, single-file SPA). Standalone: `designs/gorod-fm-standalone.html`.
> Ветка `master`. **Working tree ГРЯЗНОЕ, НЕ закоммичено, НЕ запушено.** Файлы на диске сохранены (без потерь).

---

## Контекст сессии
Эльбик: (1) «сделай визуальный аудит всего сайта через mcp chrome — соответствует ли плану». Затем по ходу: (2) «внизу странная полуобрезанная Believer-плашка — не пофиксили на норм плеер?» → диагностировал+пофиксил. Затем (3) «галерею переоформи + рассинхрон пофикси, потом пушни и комить» → **прервано до завершения**.

---

## 1. ВИЗУАЛЬНЫЙ АУДИТ — ГОТОВ. Вердикт: сайт СИЛЬНО соответствует плану cont-9→cont-11 ✅

Метод: Chrome MCP по всем 8 экранам + плеер + dev-роуты, сверка с per-surface спеками. Параллельный 10-агентный workflow (`wg0ms16pa`) вытащил из спеков (cont-9 SPEC-*, cont-10 AUDIT-apple-polish-plan, cont-11 handoff) конкретные чек-листы «что должно быть» — аудит шёл против них.

| Экран | Статус |
|---|---|
| Онбординг | ✅ «Соберём ваш вкус», плоские пузыри, импорт-seed (Last.fm·Яндекс·ВК, без Spotify) |
| Главная | ✅ 3-зонное радио, поведенческое «почему», синяя ambient-волна, иерархия ❤/Steer/skip, нет красного ореола на красной обложке |
| Мой вкус | ✅ «не чёрный ящик», 1 синяя CTA (2-я→ghost), контекст-старты, редактируемые вектор-бары (solid blue) |
| Открыть (#/podborki) | ✅ разговорный поиск, «Карта вкуса»+«ДЕМО-КАРТА», dial Рядом/Смело/На краю, синяя карта, «От редакции» (кураторы) — **НО см. находку A (легаси-галерея)** |
| Трек | ✅ ЕК-монограмма (не фото/градиент/SVG-дуги), «Почему играет»+«исправить причину», «Вектор трека»/«ДЕМО-ВЕКТОР» (4 синих бара), «Рядом по звучанию» по атрибутам |
| Артист | ✅ ID-монограмма (не силуэт), «Почему тебе этот артист»+поведенч. L1, 5 топ-треков рядами, станции (не альбомы), EQ-иконки |
| Recap | ✅ честный empty-state + (при сигнале) слово-идентичность «Размах с синтезатором» + зелёная +дельта + синий petal-bloom + «ОТКРЫТИЕ НЕДЕЛИ» |
| Профиль | ✅ чёрный-ящик vs открытый, redacted-полоса конкурентов, грани с провенансом + «меньше» |
| Плеер мини | ✅ точно по спеке cont-11 (после фикса перекрытия, см. ниже) |

**Глобально:** единый синий акцент (0 cyan/violet/red — проверено визуально на всех экранах), Onest, плоский анти-слоп, demo-честность сохранена, **0 console errors** на всех роутах (проверено `read_console_messages`), TWEAKS-панель и `#/map` корректно gated в проде (deep-link `#/map` редиректит на `#/home`).

---

## 2. 🟢 СДЕЛАНО (в working tree, НЕ закоммичено)

### Фикс #1 — мини-плеер был перекрыт легаси-шторкой ✅ ВЕРИФИЦИРОВАН (Chrome), в ОБОИХ файлах
**Симптом (жалоба Эльбика):** внизу «странная полуобрезанная Believer-плашка», а не норм. плеер.
**Причина (замерено):** `#home-bottom-sheet` — легаси домашняя шторка now-playing (очередь Thunder/Enemy/Radioactive/Demons, открывается через `home-fab`), `position:fixed`, height 480px, **z-index 65**, якорь `bottom: var(--player-mini-h)` (72px). В закрытом состоянии `transform: translateY(100%)` опускал её лишь на её высоту (480px), но из-за нижнего отступа 72px **верхняя полоска 72px оставалась в вьюпорте поверх нового `.player-mini` (z60)**. Шторку не убрали в cont-11 при редизайне мини-бара.
**Фикс (CSS `.home-bottom-sheet`, ~L4059 в `gorod-fm.html` И `gorod-fm-standalone.html`):**
```css
transform: translateY(calc(100% + var(--player-mini-h)));  /* было: translateY(100%) */
```
Якорь/высота не тронуты; открытие шторки (`[data-open]`→translateY(0)) не тронуто.
**Проверено:** на всех роутах низ = `#player-mini` (hit-test), `#home-bottom-sheet` уехал на top:816 (полностью за экран). Мини показывает Слеза/Егор Крид + «★ Ты дослушал Егора Крида до конца 3 раза», синий play, ghost next.

### Фикс #2 — рассинхрон now-playing мини↔полный ⚠️ ТОЛЬКО dev, НЕ верифицирован, НЕ в standalone
**Симптом:** мини-бар = **Слеза / Егор Крид**, но тап по нему открывал полный плеер с **Believer / Imagine Dragons** (замерено: `miniTitle:"Слеза"` vs `fullTitle:"Believer"`). Оба — статик-HTML (мини L9954, полный L10173); `openPlayer()` их не синхронизировал. Обложка полного плеера = пустой концентр-плейсхолдер (`.player-full-cover-desktop`, SVG).
**Фикс (JS, `gorod-fm.html` ТОЛЬКО):** добавлена `function syncFullPlayerFromMini()` (~L10865, перед `if (playerMini)`). Копирует из мини в полный: `#player-full-title`←`#player-track-title`, `#player-full-artist`←`#player-track-artist`, карусель-центр (`[aria-label="Текущий трек"]`), и подставляет реальную обложку (`#mini-art-img` src) в `.player-full-cover-desktop` вместо плейсхолдера. Вызывается на клик `playerMini` (L~10866) + `tabbarPlayerBtn` (L~10885). **НЕ трогает** artist/track-radio флоу (они сами ставят `#player-full-title` и зовут `openPlayer()` напрямую, минуя mini-click).
**⚠️ ОСТОРОЖНО:** НЕ протестирован в браузере. NEXT: верифицировать (тап мини → полный = Слеза + реальная обложка), и только потом зеркалить в standalone.

---

## 3. 🔴 НЕ ДОДЕЛАНО — план next session (в порядке)

### A. Gallery-restyle `#/podborki` (НЕ НАЧАТ — это была текущая задача в момент прерывания)
Легаси `.podborki`-галерея рендерится В ПОЛНЫЙ РОСТ под новым discover-редизайном: жанр-чипы (РОК/ДИСКО/ПОП/ХИП-ХОП/ЕЩЁ) + фото-плитки с повёрнутыми вертикальными 900-вес подписями (POP GOLD 2010s / K-POP / CHILL / ДИСКАЧ 90-Х / Z. CITY SHOW) на ярких мульти-цветных фото.

**Ядро нарушения (анти-слоп GDS-19 «no rotated 900-weight tile labels / scaleX»):**
- `.podborki-tile-label` CSS **L4426**: `font-family:Onest; font-weight:900; font-size:36px; text-transform:uppercase; transform: rotate(-90deg) scaleX(1.05);`

**Якоря (живые, перепроверить grep'ом — дрейфуют):**
- HTML: `.podborki-page` L~7767, чип-ряд `.podborki-chip-row` L~7830, галерея `.podborki-gallery` L~7875, тайлы `.podborki-tile` L~7883+ — каждый = `.podborki-tile-bg`(`background-image:url(assets/gorod-fm/podborki-tile-*.png)`) + `.podborki-tile-shade` + `.podborki-tile-label-wrap`>`.podborki-tile-label`.
- CSS: `.podborki-tile` L4360 (height 628px, `border-top-right-radius:var(--r-tile-tr)`), `.podborki-tile-bg` L4386, `.podborki-tile-shade` L4401 (`background:var(--tile-shade)`), `.podborki-tile-label-wrap` L4410 (bottom-right, width56/height480, rotated), `.podborki-tile-label` L4426, `.podborki-chip` L4193 (focus уже `--accent-on-dark`, focus 4226). Mobile/TV overrides L6567-6702.

**Рекомендация (решить с Эльбиком — это дизайн-развилка):**
- **Вариант 1 (де-ротация, photos kept):** подпись → горизонтальная внизу-слева, Onest **700**, ≤22-24px, без `scaleX`, normal/sentence case (или маленький uppercase-eyebrow); усилить `--tile-shade` до нижнего linear-gradient для легибельности; уменьшить height 628→~280-340; радиус → `--r-lg`; фото оставить (легит. «browse-категории», не градиент-плейсхолдеры). Минимальный, чинит именно нарушение.
- **Вариант 2 (flatten под единый акцент):** убрать фото, тайлы → плоские карточки в стиле `.discover-ed-card` (rgba white .04 + hairline, горизонт. Onest-заголовок). Максимально консистентно с редизайном (calm/single-blue/anti-slop), но теряет фото-ассеты.
- **Контекст:** discover-редизайн задумывал старую галерею → плоский ряд **«От редакции»** (он УЖЕ есть, 3 кураторские карточки). Т.е. галерея отчасти избыточна; Вариант 2 (или вовсе demote/убрать) ближе к исходному замыслу. Я склонялся к Варианту 1 (наименее разрушительно), но не успел спросить.
- Зеркалить в standalone: фон-фото в standalone = base64-inline → если менять только CSS/подписи (не `img src`), строки идентичны и зеркалятся чисто. Если менять структуру тайла — дев/standalone разойдутся (там base64), нужна аккуратность.

### B. Верифицировать Фикс #2 в Chrome (тап мини → полный показывает Слеза + реальную обложку; и на mobile-surface карусель-центр).
### C. Зеркалить Фикс #2 (+ gallery после A) в `gorod-fm-standalone.html` (он code-identical; Фикс #1 уже там). Анкоры desync в standalone те же (`if (playerMini)` блок + `tabbarPlayerBtn` блок — pre-edit код идентичен дев'у).
### D. Commit + push ВСЁ (Эльбик: «потом пушни все и комить»). Сервер :8770 был запущен для проверок.

---

## 4. Прочие находки аудита (🟡 не блокеры, на усмотрение)
- Онбординг eyebrow «ПЕРВЫЙ AI-МУЗЫКАЛЬНЫЙ СТРИМИНГ» = старое позиционирование → **GOROD-029 (Эльбик-gate)**, не баг.
- Профиль (#/profile) показывает дефолт/демо-вектор как «ОТКРЫТО · ТВОЁ» с провенанс-строками без demo-лейбла, тогда как recap честно гейтит на реальный сигнал (`hasRealSignal()`) — лёгкая нестыковка честности (профиль = always-on pitch, демо-данные как реальные). Рассмотреть demo-лейбл или гейт на профиле.

---

## 5. Дисциплина / артефакты
- **Анкеры дрейфуют** — re-grep живой файл перед каждым edit (НЕ по номерам строк выше).
- Cache-bust `?v=N` для визуал-проверки (сервер кеширует). 0 console errors было подтверждено.
- Чек-листы аудита (10 поверхностей) — в выводе workflow `wg0ms16pa` (`...tasks/wg0ms16pa.output`, если жив) — это «что должно быть» по спекам.
- Тест-ключи `gorodfm_*` чистил после probe (seed для populated-recap удалён).
- START next session = RESUME cont-12 блок + этот файл.

---

## CONT-12 BUILD — ОТКРЫТЬ redesign (real Figma content) — STATE + NEXT

**Operator overrides this session:** Медиатека = KEEP (search+improve-taste, НЕ cut). Подборки = карусели РАЗНОГО дизайна как Figma (НЕ грид с тег-фильтром, «не прячь в теги»). Real Figma content/visuals везде. Collections = Figma tile-form (высокие, РАЗНОЙ ШИРИНЫ, вертикальная подпись). + floating genre «шарики» в Медиатеке. UX: AI не потерять + красивые подборки видно сразу.

### ✅ DONE (dev `gorod-fm.html`, VERIFIED Chrome, 0 console errors; НЕ закоммичено; НЕ зеркалено в standalone)
ОТКРЫТЬ (#/podborki) полностью пересобран, порядок:
1. **AI-ask** наверху (conversational «как X но Y» kept — AI не потерян).
2. **«Подборки» карусель-герой** сразу под аском: высокие тайлы РАЗНОЙ ШИРИНЫ (208–300px, Figma-форма) + full-bleed реал-covers (`podborki-tile-*`) + ВЕРТИКАЛЬНАЯ подпись (writing-mode, Onest 700, uppercase, БЕЗ scaleX-900-slop) + синяя строка-связь с вектором. Клик → startWave (openPlayer + синк now-playing).
3. **«Карта твоего вкуса»** (AI map) — kept high.
4. Рядом · **«Исполнители»** (круг.аватары `favs-artist-*`: Akon/Дима Билан/Макс Корж/Мия Бойка/Рамиль/Rem Digga) · **«Группы»** (квадраты `favs-group-*`: Linkin Park/Ludovico Einaudi/Bernhoft/Crystal Castles/My Darkest Days) · **«От редакции»**.
5. **«Медиатека»** (найди и улучшай вкус): 18 реал-артистов (`library-artist-*`) + поиск + **«+ в вкус» РЕАЛЬНО пишет `gorodfm_taste`** + **floating genre «шарики»** (8 жанров, CSS-float, фильтр). Verified: Рок→[Аквариум,Алиса].
Легаси rotated-label `.podborki`-галерея УДАЛЕНА (заменена). Мёртвые `.podborki-*` CSS/`initPodborki` JS остались (null-guard, 0 errors).

Build-scripts (`.scratch/`, gitignored): **`build_discover2.py`** (главный: карусели+Медиатека+reorder), **`build_tiles_form.py`** (Figma-форма тайлов), **`build_bubbles.py`** (шарики). Superseded: build_collections.py, build_mediateka.py. Backups: `gorod-fm.bak.html` (pre-build, С фиксами cont-12), bak2/bak3.

### 🔴 NEXT SESSION — что НЕ доделали
1. **🎯 Шарики ИНТЕРЕСНЕЕ (оператор флагнул отдельно):** сейчас 8 жанр-фильтр-шариков (статичный float). Нужно как в ОНБОРДИНГЕ — облако жанров **И артистов**, выбираешь → строит вкус (select-to-build-taste, живая раскладка). Reuse механику `#/onboarding` (GorodOnboarding bubble cloud: genre+artist bubbles, tap-select, «модель за N сигналов»). Применить тот же интерактив к discover-поиску.
2. **#/artist enrich** (тот же паттерн): реал-фото hero (`artist-hero-arthur.png`) + треки (`artist-track-cover-*`) + lyrics.
3. **«Сохранённое»** (#/taste): реальные `favs-dj-*`/`favs-group-*`/`favs-artist-*` с группировкой DJ/Группы/Артисты.
4. **ЛК** account-sheet (per `BLUEPRINT-gorod-fm-sections-integration.md`).
5. **Зеркалить ВСЁ в `gorod-fm-standalone.html`:** сейчас там ТОЛЬКО home-bottom-sheet фикс. Весь ОТКРЫТЬ-rebuild + desync-фикс + tiles + bubbles НЕ зеркалены. (standalone = base64 covers inline; covers `podborki-tile-*`+`library-artist-*`+`favs-*` нужны inline — re-encode или re-apply build на standalone-базе.)
6. **Верифицировать desync-фикс** (Fix #2 mini↔full) в Chrome.
7. **Light theme** build — `SPEC-gorod-fm-light-theme.md` (готов, AA + критик-правки §8).
8. **Sections** остаток — `BLUEPRINT-gorod-fm-sections-integration.md`.
9. **Commit + push** ВСЁ (Эльбик: «пушни и комить» — ПОСЛЕ доделки+проверки+зеркала).

### State / discipline
- git working tree ГРЯЗНОЕ (`gorod-fm.html` сильно изменён + standalone home-bottom-sheet фикс + 4 docs). НЕ закоммичено.
- Re-grep якоря (НЕ номера строк); `?v=N` cache-bust; :8770. **Чистить `gorodfm_taste`/`gorodfm_rejected` тест-ключи** (Медиатека «+в вкус» их пишет!).
- 87 реал-Figma-ассетов в `designs/assets/gorod-fm/` (Figma file ODcQ2ERWYi3w504Z86TOy3; node-ids: ЛК 2245-2149, Подборки 2384-4999, Медиатека 2385-2924, Профиль артиста 2537-14090, Избранное 2535-11151).
