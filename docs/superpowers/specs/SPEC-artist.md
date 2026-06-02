# GOROD-047b — Артист deep-dive (#/artist) — Build Spec

> Auto-captured 2026-06-02 from per-surface build assignment (Артист / 047b, gated 047, авторизовано). BUILD-READY. Перестраивает `#/artist` из legacy-slop (SVG-силуэт-аватар + gradient-обложки + collaborative-«фанаты также») в deep-dive по blueprint §3 «Артист» + §1.2 row + §8 (047 ставка) + AUDIT §4 («фанаты также слушают = жутко»). Implement per this spec.
>
> **Target file:** `C:/Users/elbics/Desktop/design-project/designs/gorod-fm.html` — все line-anchors ниже пересверены через Read/Grep живого файла в этой сессии (файл ~14.1k строк, `</body>`@14142).
>
> **Grounded scope-correction (читать первым).** Бриф говорил «силуэт-аватар» — подтверждено: hero@8290 = три `<circle>/<path>` SVG-силуэт. Но бриф недооценил масштаб slop: **весь экран** на legacy. Реальные нарушения Holy Grail, найденные построчно:
> 1. **SVG-силуэт-портрет** hero@8290–8299 (head circle + shoulders path + hair path) — прямой ❌ «SVG-силуэты».
> 2. **10 gradient-плашек top-track** @8372/8384/.../8480 (`linear-gradient(135deg,#1a3a6e,#56afd7)` и пр., многие multi-hue: `#2d1a6e→#c43a6e` фиолет→малина, `#3d0047→#9c27b0` фиолет) — ❌ «gradient-плейсхолдеры вместо реал-контента» + ❌ «один акцент» (purple/magenta вне синей семьи).
> 3. **6 gradient-обложек альбомов + SVG-арт внутри** @8499/8513/.../8568 — те же два нарушения.
> 4. **`--brand-cyan` (rgb(56,140,180))** ~30 вхождений в `.artist-*` CSS (overline@4519, photo glow@4495, primary-btn bg@4577, все focus-outline, secondary aria-pressed, eq-icon@4913) — ❌ LEGACY cyan, нарушает «один акцент» (blueprint §5: retire в синюю семью).
> 5. **`.artist-photo` сам gradient** @4489 `linear-gradient(135deg,#3d0080 0%,#1a4fa0 40%,#56afd7 100%)` — purple→cyan multi-stop = ❌ multi-stop gradient bg.
> 6. **IA-привязка к старому миру:** overline «АРТИСТ · ИЗБРАННОЕ»@8305, `h1`«Избранное — Артист»@8282, «Открыть весь список»→`#/favorites`@8354, секция «Альбомы» (каталожная, не радио) — 0 wedge, тянет в legacy-IA.
> 7. **Wedge = 0:** нет ни одного «почему тебе этот артист», нет reject, нет fidelity-петли. Это generic-стриминг-страница.
>
> **assets/gorod-fm/ НЕ существует** (Glob: No files found) → реал-фото в прототипе нет → HERO = art-tint+монограмма (blueprint §8: «art-tint+инициалы дефолт + 2–3 реал-пресс-фото для демо целевого вида»; реал-фото-пайплайн = Ф1+, asset-decision Эльбика). Спек строит **fallback-путь как дефолт** + оставляет `data-artist-photo` seam под реал-фото без рефактора.

---

## 0. Inputs reconciliation (resolved conflicts — read first)

| # | Конфликт / неоднозначность | Резолюция (binding) | Почему |
|---|---|---|---|
| **C1** | Бриф: «реал-фото если есть в assets/, иначе art-tint+монограмма». assets/ пуст. | **art-tint+монограмма = дефолтный рендер**, реал-фото = опциональный апгрейд через `data-artist-photo="<url>"` на hero-node (если атрибут есть и картинка грузится → `<img>`, иначе fallback). v1 строит fallback, seam под фото оставлен. | Asset-wall mandатит цвет-от-контента; blueprint §8 явно: art-tint дефолт сейчас, реал-фото Ф1+. Seam = zero-рефактор когда Эльбик решит asset-пайплайн. |
| **C2** | Бриф: «станции артиста (on-brand для РАДИО, не каталог)» vs legacy имеет секцию «Альбомы». | **Удалить «Альбомы» целиком. Заменить на «Станции с этим артистом» (уже есть @8584, переработать) + «Топ треков» row.** Финальный порядок секций: HERO → «Почему тебе этот артист» → «Топ треков» (row art-tint) → «Станции с этим артистом». | Blueprint §3 Артист перечисляет ровно: HERO + «почему» + топ-треки row + станции. «Альбомы» = каталожная метафора (Apple Music «Essential Albums») — мы РАДИО, не магазин обложек (тот же нарратив, что в «Сохранённое» §3). AUDIT: каталог обложек = generic-стриминг. Альбом как объект остаётся в `data-track-album` метаданных трека, не как сетка. |
| **C3** | «Почему тебе этот артист»: L1→L2 + «Это не про меня». Какой data-model для reject? | **Переиспользовать существующий `gorodfm_rejected` corpus** (TwinrWhy@13339 пишет, GorodTaste@13130/Profile@13668/Recap читают). Reject-причины артиста = НОВЫЕ facet-id с префиксом `art_`: `art_arena` (арена-рок 80%), `art_vocal_m` (мужской вокал). Лейблы добавляются в общий REJ_LABELS-канон (см. §6 shared-seam). | Единственный незаменимый ров = reason_tag corpus (blueprint §4/§6). Reject артиста ОБЯЗАН писать в тот же store, иначе создаём 4-й остров (тот самый анти-паттерн §0 блюпринта). Префикс `art_` не коллизирует с `artist`/`vocal`/`tempo` (player-level). |
| **C4** | Бриф: «attribute-честное "почему", НЕ "фанаты также слушают" (AUDIT §4=жутко)». Legacy не имеет «фанаты также», но имеет collaborative-намёк через "В избранное"/share. | **Bind: НИ ОДНОГО collaborative-сигнала.** Никаких «фанатам также нравится», «похожие слушатели», «X%共». Каждый буллет «почему» = ЛИБО твоё поведение («12 треков дослушал»), ЛИБО attribute-match твоего вектора («арена-рок 80% — совпадает с твоим профилем»). | AUDIT §4 прямо: collaborative-«фанаты также» = «жутко» (creepy social proof). Web-research подтвердил: Spotify «Fans Also Like» прямо ПИТАЕТ «Artist Radio» — это ровно тот чёрный ящик, против которого мы строим. Наш wedge = attribute-provenance. |
| **C5** | Демо-данные (вектор-match %, причины) — как маркировать? | **Обязательный микро-лейбл «демо-вектор»** на блоке «почему» (как мандатит §0 брифа + blueprint §3 Трек/§8). Inline `.artist-why-demo` бейдж. | Без маркировки красивый ненастоящий вектор = «perceived transparency» = смерть доверия (blueprint §8 «Демо-вектор»). Тот же принцип, что 047a Трек. |
| **C6** | `--brand-cyan` retire — в этой задаче или отложить (W-cyan глобальный)? | **Retire cyan ТОЛЬКО внутри `.artist-*` scope** (этот экран). Глобальный retire (~70 вхождений) = отдельная Integrate-фаза. Все новые `.artist-*` правила и все переписываемые используют `--brand-blue-light`/`--accent-on-dark`. | Спеки реализуются по-экранно (ограничение одного файла §3 задачи). Этот спек делает свой экран cyan-free; общий шов вынесен в §10 sharedEditAnchors для Integrate. Частичный retire не ломает другие экраны (cyan-токен остаётся определён). |
| **C7** | «Слушать радио артиста» — что делает, fidelity-честно? | **Открывает плеер с radio-сессией артиста (переиспользует существующий `openArtistPlayer`@11961) + пишет provenance в `#player-track-reason`**: «Радио по артисту: арена-рок + мужской вокал — грани твоего вектора». Не fake-«играет». | Honest: кнопка реально меняет now-playing meta (как сейчас@11977). Добавляем provenance-строку (как 051 reflectPlayer@14114-стиль) — каждое действие объяснено. |
| **C8** | Hero photo сейчас `aria-hidden` декоративный. Имя артиста = `IMAGINE DRAGONS`. | **Сохранить IMAGINE DRAGONS как демо-артиста** (консистентно с top-tracks/`#/track` Believer@8667 и Card 4 nav@7368). Монограмма = «ID» (первые буквы двух слов). | Минимум новых демо-данных; экран уже весь про Imagine Dragons (треки, `#/track` Believer). Менять артиста = лишний diff без ценности. |

Где бриф/blueprint дали конкретику (проценты, причины, BPM) — она authoritative и воспроизведена verbatim ниже. **Не выдумывать значения вне этого набора.**

---

## 1. Финальное размещение + additive-safety (НЕ ломает built; 045/pixel-perfect не триггерится)

### 1.1 Что меняется (3 зоны, все внутри уже-существующего `#/artist`)
- **DOM** — секция `<section data-page="artist">` @8281–8642 переписывается **целиком** (replace-in-place, тот же `data-page="artist"` контракт). Граница строго: открывающий тег @8281 … закрывающий `</section>`@8642 + comment@8643. Ничего вне этих строк не трогается.
- **CSS** — блок `[data-page="artist"]` + `.artist-*` @4462–4934 переписывается in-place (тот же диапазон). Responsive @6764–6878 переписывается in-place (тот же диапазон, cyan→blue + новые классы).
- **JS** — `initArtist()` IIFE @11958–12060 переписывается in-place (тот же диапазон).
- **Новый trailing-модуль** `window.GorodArtist` — appended после строки 14140 (`</script>` закрытия GorodContext-модуля), последний блок перед `</body>`@14142 (зеркалит GorodContext/GorodProfile/GorodRecap pattern).
- **Shared seam (Integrate-фаза, НЕ в этом спеке):** добавить `art_arena`/`art_vocal_m` в REJ_LABELS-канон GorodProfile@13670 + GorodRecap + GorodTaste@13131, чтобы reject артиста читался человеко-понятно на тех экранах. См. §10.

### 1.2 Почему это безопасно и НЕ активирует gated 045
1. **`#/home` не тронут ни байтом.** Все правки строго внутри `#/artist` DOM-границ (8281–8643), `.artist-*` CSS (4462–4934 / 6764–6878), `initArtist` (11958–12060), и нового trailing-IIFE. `data-page="home"` (7443+), `.home-stage`, абсолютные плитки (Figma 2174:422) — вне всех диапазонов → pixel-perfect сохранён байт-в-байт → решение Эльбика «насколько ломать home» (045) **не форсируется**.
2. **Замена in-place, не insertion в flow.** `#/artist` — push-deep-dive (blueprint §1.1), не таб, открывается из карточки (Card 4@7368, и из любой track-row через `#/artist` nav). Замена контента секции не сдвигает ничего absolute-positioned (секция сама в normal page-flow router'а).
3. **Route не меняется.** `VALID_ROUTES`@10931 уже содержит `#/artist` — не трогаем. `#/track`@8645 (соседняя секция) вне диапазона.
4. **LS-ключи изолированы.** Новый код пишет в существующий `gorodfm_rejected` (тот же массив-схема, новые id `art_*`) — не пересоздаёт ключ. `gorodfm_taste` читается read-only для match-демо. Никаких новых LS-ключей.
5. **`navigate()` уже в scope** initArtist (используется @12004/12056) — переиспользуем, не объявляем заново.
6. **`openPlayer`/`openArtistPlayer` сохранены** — radio CTA и track-row продолжают открывать плеер тем же путём (@11970/11977).
7. **`TwinrWave.bump()` опционально** — guard `if(window.TwinrWave)`; reject артиста дёргает bump для видимого эффекта (как TwinrWhy@13373), но модуль не падает если волны нет (волна только на `#/taste`).
8. **Не дублирует другие экраны:** `#/track`@8645 = per-track explainability (047a, отдельный спек); `#/profile` = pitch-вектор; `#/artist` = artist-level «почему тебе этот артист» + radio. Разные объекты, разные id-схемы (`art_*` vs player-level `artist`/`vocal`/`tempo`).

---

## 2. Контент-модель — артист, причины, треки, станции (реальные значения)

**Артист (демо):** `IMAGINE DRAGONS`, монограмма `ID`, art-tint hue = синяя семья (детерминированный от имени, см. §5 `tintFor`).

**«Почему тебе этот артист» — L1 (свёрнуто) → L2 (раскрыто).** Каждый L2-буллет = поведение ИЛИ attribute-match, НИКОГДА collaborative. Маркировка «демо-вектор».

| Уровень | Текст (verbatim) |
|---|---|
| **L1** (видно сразу) | `Ты дослушал <b>12 треков</b> этого артиста до конца — больше, чем у 9 из 10 в твоей волне.` |
| **L2 буллет 1** (поведение) | `12 треков дослушано до конца` · provenance `твоё поведение за месяц` |
| **L2 буллет 2** (attribute-match, reject-able `art_arena`) | `Арена-рок — <b>80%</b> совпадает с твоим вектором` · provenance `грань твоего профиля` |
| **L2 буллет 3** (attribute-match, reject-able `art_vocal_m`) | `Мужской вокал, мощный припев — совпадает с тем, что ты усиливал` · provenance `ты поднимал эту грань` |
| **L2 буллет 4** (поведение) | `Не пропустил ни один трек этого артиста на «Городе»` · provenance `0 скипов` |

**Reject («Это не про меня»):** уровень-артист toggle, пишет `gorodfm_rejected`. + per-bu/llet «не моё» на reject-able буллетах (буллет 2 → `art_arena`, буллет 3 → `art_vocal_m`). Reject-квитанция: `Убрал «<label>» — следующее радио артиста меньше опирается на эту грань.`

**Топ треков (row, art-tint, верхние 5 — НЕ 10; row не grid):** Believer/03:38, Thunder/03:08, Radioactive/03:07, Demons/02:58, Whatever It Takes/03:21 (из legacy@8370–8425, альбом-метаданные сохраняем в `data-track-album`). Каждый row: ранг + art-tint(40px)+монограмма + title + album-line + dur. Клик → `openArtistPlayer(title, 'IMAGINE DRAGONS')` (как сейчас @12014).

**Станции с этим артистом (on-brand радио):** ГОРОД РОК 103.5 / ГОРОД ХИТ 89.0 / DFM CHILL 104.5 / Z. CITY SHOW 105.0 (из legacy@8589–8635). Сохранить EQ-bar icon (не эмодзи, не силуэт — это вектор-полоски, on-brand). Клик → `navigate('#/home')` (как сейчас @12056). Cyan eq-icon → `--accent-on-dark`.

---

## 3. DOM structure (semantics + a11y) — replace 8281–8642 verbatim

```html
      <!-- Page: Артист — deep-dive (#/artist) · GOROD-047b -->
      <section data-page="artist" aria-labelledby="page-artist-heading">
        <h1 id="page-artist-heading" class="visually-hidden">Артист — Imagine Dragons</h1>

        <!-- ---- Hero band: art-tint + монограмма (НЕ силуэт) ---------------- -->
        <div class="artist-hero" aria-label="Профиль артиста">
          <!-- art-tint avatar; data-artist-photo seam under real foto (Ф1+) -->
          <div class="artist-photo" id="artist-photo" data-artist-photo="" aria-hidden="true">
            <span class="artist-photo-mono" id="artist-photo-mono">ID</span>
          </div>

          <div class="artist-hero-text">
            <p class="artist-overline" aria-hidden="true">Артист · Город ФМ</p>
            <h2 class="artist-name" id="artist-name-heading">IMAGINE DRAGONS</h2>
            <p class="artist-stats">Американский альт-рок · в твоей волне с весны</p>

            <div class="artist-action-row" role="group" aria-label="Действия с артистом">
              <button class="artist-action-primary" type="button" id="artist-btn-radio"
                aria-label="Слушать радио Imagine Dragons">Слушать радио артиста</button>
              <button class="artist-action-secondary" type="button" id="artist-btn-fav"
                aria-pressed="false" aria-label="Добавить артиста в избранное">
                <svg aria-hidden="true" viewBox="0 0 24 24">
                  <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
                </svg>В избранное</button>
            </div>
          </div>
        </div>
        <!-- /.artist-hero -->

        <!-- ---- Почему тебе этот артист (L1 → L2 + reject) ----------------- -->
        <section class="artist-section artist-why" aria-labelledby="artist-why-h">
          <div class="artist-why-head">
            <h2 id="artist-why-h" class="artist-section-heading">Почему тебе этот артист</h2>
            <span class="artist-why-demo" title="Вектор в прототипе — демонстрационный">демо-вектор</span>
          </div>

          <p class="artist-why-l1" id="artist-why-l1">Ты дослушал <b>12 треков</b> этого артиста до конца — больше, чем у 9 из 10 в твоей волне.</p>

          <button class="artist-why-toggle" type="button" id="artist-why-toggle"
            aria-expanded="false" aria-controls="artist-why-list">Показать, на чём это держится</button>

          <ul class="artist-why-list" id="artist-why-list" hidden>
            <!-- injected by GorodArtist.render() — поведение/attribute, never collaborative -->
          </ul>

          <div class="artist-why-foot">
            <button class="artist-why-not" type="button" id="artist-why-not"
              aria-pressed="false">Это не про меня</button>
            <p class="artist-why-receipt" id="artist-why-receipt" role="status" aria-live="polite"></p>
          </div>
        </section>

        <!-- ---- Топ треков (row, art-tint) -------------------------------- -->
        <section class="artist-section" aria-labelledby="artist-tracks-heading">
          <h2 id="artist-tracks-heading" class="artist-section-heading">Топ треков</h2>
          <div class="artist-tracks" id="artist-tracks" role="list" aria-label="Топ треков Imagine Dragons">
            <!-- 5 rows injected by GorodArtist.render() from TRACKS -->
          </div>
        </section>

        <!-- ---- Станции с этим артистом (on-brand радио, НЕ каталог) ------ -->
        <section class="artist-section" aria-labelledby="artist-stations-heading">
          <h2 id="artist-stations-heading" class="artist-section-heading">Станции с этим артистом</h2>
          <p class="artist-stations-sub">Где Imagine Dragons звучит чаще — это радио, не плейлист.</p>
          <div class="artist-stations" role="list" aria-label="Станции, играющие Imagine Dragons">

            <button class="artist-station-chip" type="button" role="listitem"
              data-station-id="rok" aria-label="ГОРОД РОК 103.5 FM">
              <svg class="artist-station-eq" aria-hidden="true" viewBox="0 0 18 14">
                <rect x="1"  y="4" width="2.5" height="10" rx="1.25" fill="currentColor"/>
                <rect x="5"  y="1" width="2.5" height="13" rx="1.25" fill="currentColor"/>
                <rect x="9"  y="5" width="2.5" height="9"  rx="1.25" fill="currentColor"/>
                <rect x="13" y="2" width="2.5" height="12" rx="1.25" fill="currentColor"/>
              </svg>
              <span class="artist-station-name">ГОРОД РОК</span>
              <span class="artist-station-freq">103.5 FM</span>
            </button>

            <button class="artist-station-chip" type="button" role="listitem"
              data-station-id="hit" aria-label="ГОРОД ХИТ 89.0 FM">
              <svg class="artist-station-eq" aria-hidden="true" viewBox="0 0 18 14">
                <rect x="1"  y="6" width="2.5" height="8"  rx="1.25" fill="currentColor"/>
                <rect x="5"  y="2" width="2.5" height="12" rx="1.25" fill="currentColor"/>
                <rect x="9"  y="4" width="2.5" height="10" rx="1.25" fill="currentColor"/>
                <rect x="13" y="3" width="2.5" height="11" rx="1.25" fill="currentColor"/>
              </svg>
              <span class="artist-station-name">ГОРОД ХИТ</span>
              <span class="artist-station-freq">89.0 FM</span>
            </button>

            <button class="artist-station-chip" type="button" role="listitem"
              data-station-id="chill" aria-label="DFM CHILL 104.5 FM">
              <svg class="artist-station-eq" aria-hidden="true" viewBox="0 0 18 14">
                <rect x="1"  y="8" width="2.5" height="6"  rx="1.25" fill="currentColor"/>
                <rect x="5"  y="5" width="2.5" height="9"  rx="1.25" fill="currentColor"/>
                <rect x="9"  y="3" width="2.5" height="11" rx="1.25" fill="currentColor"/>
                <rect x="13" y="6" width="2.5" height="8"  rx="1.25" fill="currentColor"/>
              </svg>
              <span class="artist-station-name">DFM CHILL</span>
              <span class="artist-station-freq">104.5 FM</span>
            </button>

            <button class="artist-station-chip" type="button" role="listitem"
              data-station-id="cityshow" aria-label="Z. CITY SHOW 105.0 FM">
              <svg class="artist-station-eq" aria-hidden="true" viewBox="0 0 18 14">
                <rect x="1"  y="3" width="2.5" height="11" rx="1.25" fill="currentColor"/>
                <rect x="5"  y="7" width="2.5" height="7"  rx="1.25" fill="currentColor"/>
                <rect x="9"  y="1" width="2.5" height="13" rx="1.25" fill="currentColor"/>
                <rect x="13" y="5" width="2.5" height="9"  rx="1.25" fill="currentColor"/>
              </svg>
              <span class="artist-station-name">Z. CITY SHOW</span>
              <span class="artist-station-freq">105.0 FM</span>
            </button>

          </div>
        </section>

      </section>
      <!-- /#/artist -->
```

**a11y гарантии:**
- `h1#page-artist-heading` (visually-hidden) landmark → 4 `<section>` с `aria-labelledby` h2. Корректная вложенность.
- HERO `.artist-photo` `aria-hidden` (декоративный art-tint); имя артиста в `h2` несёт смысл для AT (не в картинке).
- «почему»-toggle: `aria-expanded` + `aria-controls`, список `hidden` пока свёрнут (не color-only).
- reject-кнопки: `aria-pressed` true/false (текстовое состояние, не цвет).
- `#artist-why-receipt` `role="status" aria-live="polite"` → AT слышит «убрал X — пересчитал».
- EQ-icon = `aria-hidden` SVG-полоски (вектор, on-brand), станция-смысл в `.artist-station-name`/`aria-label`.
- Hit-targets ≥44px (см. §5). focus-visible 3px. Без эмодзи-икон, без силуэтов.

---

## 4. Удаляемые/переписываемые элементы (явный diff legacy → new)

| Legacy (удаляется) | Замена |
|---|---|
| SVG-силуэт hero @8290–8299 | `.artist-photo-mono` «ID» на art-tint плашке |
| overline «АРТИСТ · ИЗБРАННОЕ» @8305 | «Артист · Город ФМ» (снимает legacy-IA) |
| `h1` «Избранное — Артист» @8282 | «Артист — Imagine Dragons» |
| `.artist-bio` 4-строчный маркетинг-блёрб @8308 | удалён (заменён behavioral «почему») |
| share-кнопка @8333–8349 | удалена (не wedge; fav остаётся) |
| «Открыть весь список»→`#/favorites` @8353 | удалён (legacy-IA tie) |
| `.artist-tracks-grid` 2-col, 10 gradient-плашек @8366–8489 | `.artist-tracks` single-col row, 5 art-tint @§5 |
| вся секция «Альбомы» @8492–8582 (6 gradient + SVG-арт) | удалена (C2 — каталог не радио) |
| `--brand-cyan` во всех `.artist-*` | `--brand-blue-light` / `--accent-on-dark` |

---

## 5. CSS — replace 4462–4934 + 6764–6878 (tokens only, cyan-free)

**Новый блок (вставить вместо 4462–4934).** Без новых хардкод-цветов кроме white-scale rgba (уже в файле) и RGB синего `81,104,252` (= `--brand-blue-light` #5168FC, паттерн файла @585). art-tint hue = синяя семья.

```css
      /* =========================================================================
         ARTIST PAGE — deep-dive: art-tint hero + «почему» + tracks + stations
         GOROD-047b · cyan retired → blue family · no SVG silhouette
         ========================================================================= */
      [data-page="artist"] { padding-bottom: 80px; }

      /* ---- Hero band -------------------------------------------------------- */
      .artist-hero {
        display: flex; flex-direction: row; align-items: center; gap: 48px;
        min-height: 320px; padding: 48px 40px;
        background: rgba(0,0,0,0.12);
        border-bottom: 1px solid var(--surf-glass-12);
        margin-bottom: 40px;
      }
      /* art-tint avatar (NOT silhouette): flat blue-family tint + монограмма */
      .artist-photo {
        position: relative; width: 220px; height: 220px; border-radius: 50%;
        flex-shrink: 0; display: flex; align-items: center; justify-content: center;
        overflow: hidden;
        background: var(--np-accent);            /* content-derived hue (set by JS tintFor) */
        box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 3px rgba(81,104,252,0.30);
      }
      /* tint wash so the flat fill reads as a surface, not a flat block */
      .artist-photo::after {
        content:""; position:absolute; inset:0; border-radius:50%;
        background: radial-gradient(120% 120% at 30% 25%, rgba(255,255,255,0.18), rgba(0,0,0,0.28));
      }
      .artist-photo-mono {
        position: relative; z-index: 1; font-family:'Onest',sans-serif;
        font-size: 72px; font-weight: 900; letter-spacing: 0.02em; color: #fff;
        line-height: 1; text-shadow: 0 2px 12px rgba(0,0,0,0.35);
      }
      /* real-photo seam (Ф1+): when JS sets <img>, it covers the mono */
      .artist-photo > img { position:absolute; inset:0; z-index:2; width:100%; height:100%; object-fit:cover; }

      .artist-hero-text { display:flex; flex-direction:column; gap:14px; max-width:560px; min-width:0; }
      .artist-overline {
        font-family:'Onest',sans-serif; font-size:11px; font-weight:700;
        letter-spacing:0.10em; text-transform:uppercase;
        color: var(--accent-on-dark); margin:0; line-height:1;
      }
      .artist-name {
        font-family:'Onest',sans-serif; font-size:56px; font-weight:900;
        letter-spacing:0.03em; line-height:1.0; color:var(--text-pri);
        text-wrap:balance; margin:0;
      }
      .artist-stats { font-family:'Onest',sans-serif; font-size:16px; color:var(--text-sec); margin:0; line-height:1.4; }

      .artist-action-row { display:flex; align-items:center; flex-wrap:wrap; gap:12px; margin-top:4px; }
      .artist-action-primary {
        display:inline-flex; align-items:center; justify-content:center;
        padding:14px 28px; min-height:44px; border-radius:var(--r-pill);
        background:var(--brand-blue-light); color:#fff;
        font-family:'Onest',sans-serif; font-size:14px; font-weight:700;
        letter-spacing:0.04em; cursor:pointer; border:none;
        transition: filter var(--t-fast); white-space:nowrap;
      }
      .artist-action-primary:hover { filter:brightness(1.12); }
      .artist-action-primary:focus-visible { outline:3px solid var(--brand-blue-light); outline-offset:3px; }

      .artist-action-secondary {
        display:inline-flex; align-items:center; gap:8px; padding:14px 22px; min-height:44px;
        border-radius:var(--r-pill); background:var(--surf-glass-12); color:var(--text-pri);
        font-family:'Onest',sans-serif; font-size:14px; font-weight:500; cursor:pointer;
        border:1px solid rgba(255,255,255,0.12); transition:background var(--t-fast); white-space:nowrap;
      }
      .artist-action-secondary:hover { background:var(--surf-glass-20); }
      .artist-action-secondary:focus-visible { outline:3px solid var(--brand-blue-light); outline-offset:3px; }
      .artist-action-secondary svg { width:16px; height:16px; fill:none; stroke:currentColor; stroke-width:1.8; flex-shrink:0; }
      .artist-action-secondary[aria-pressed="true"] { color:var(--accent-on-dark); border-color:rgba(81,104,252,0.45); }
      .artist-action-secondary[aria-pressed="true"] svg { fill:var(--accent-on-dark); stroke:none; }

      /* ---- Section wrapper -------------------------------------------------- */
      .artist-section { padding:0 40px 40px; max-width:920px; margin:0 auto; }
      .artist-section-heading {
        font-family:'Onest',sans-serif; font-size:24px; font-weight:700;
        color:var(--text-pri); text-wrap:balance; margin:0 0 16px;
      }

      /* ---- «Почему тебе этот артист» ---------------------------------------- */
      .artist-why { }
      .artist-why-head { display:flex; align-items:center; gap:12px; margin-bottom:14px; }
      .artist-why-head .artist-section-heading { margin:0; }
      .artist-why-demo {
        font-family:'Onest',sans-serif; font-size:10px; font-weight:700;
        text-transform:uppercase; letter-spacing:0.06em; color:var(--accent-on-dark);
        background:rgba(81,104,252,0.12); border:1px solid rgba(81,104,252,0.30);
        padding:3px 8px; border-radius:var(--r-pill); cursor:default;
      }
      .artist-why-l1 {
        font-family:'Onest',sans-serif; font-size:17px; font-weight:500; line-height:1.5;
        color:var(--text-pri); margin:0 0 14px; max-width:620px;
      }
      .artist-why-l1 b { color:var(--accent-on-dark); font-weight:800; }
      .artist-why-toggle {
        font-family:'Onest',sans-serif; font-size:14px; font-weight:600; color:var(--accent-on-dark);
        background:none; border:none; padding:8px 0; min-height:44px; cursor:pointer;
        text-align:left; transition:opacity var(--t-fast);
      }
      .artist-why-toggle:hover { opacity:0.78; }
      .artist-why-toggle:focus-visible { outline:3px solid var(--brand-blue-light); outline-offset:2px; border-radius:var(--r-base); }

      .artist-why-list { list-style:none; margin:8px 0 0; padding:0; display:flex; flex-direction:column; gap:10px; }
      .artist-why-item {
        display:flex; align-items:flex-start; gap:12px; padding:12px 16px;
        background:var(--surf-glass-12); border-radius:var(--r-base);
        border:1px solid rgba(255,255,255,0.06);
      }
      .artist-why-dot { flex-shrink:0; width:8px; height:8px; margin-top:7px; border-radius:50%; background:var(--brand-blue-light); }
      .artist-why-body { flex:1; min-width:0; display:flex; flex-direction:column; gap:2px; }
      .artist-why-text { font-family:'Onest',sans-serif; font-size:15px; font-weight:500; color:var(--text-pri); line-height:1.4; }
      .artist-why-text b { color:var(--accent-on-dark); font-weight:800; }
      .artist-why-prov { font-family:'Onest',sans-serif; font-size:12px; color:var(--text-quat); }
      .artist-why-item.is-rejected { opacity:0.5; }
      .artist-why-item.is-rejected .artist-why-text { text-decoration:line-through; }
      .artist-why-reject {
        flex-shrink:0; font-family:'Onest',sans-serif; font-size:12px; font-weight:600;
        color:var(--text-quat); background:none; border:1px solid rgba(255,255,255,0.14);
        border-radius:var(--r-pill); padding:6px 12px; min-height:32px; cursor:pointer;
        transition:color var(--t-fast), border-color var(--t-fast);
      }
      .artist-why-reject:hover { color:var(--text-pri); border-color:rgba(255,255,255,0.30); }
      .artist-why-reject:focus-visible { outline:3px solid var(--brand-blue-light); outline-offset:2px; }

      .artist-why-foot { display:flex; align-items:center; gap:16px; flex-wrap:wrap; margin-top:18px; }
      .artist-why-not {
        font-family:'Onest',sans-serif; font-size:13px; font-weight:600; color:var(--text-sec);
        background:none; border:1px solid rgba(255,255,255,0.14); border-radius:var(--r-pill);
        padding:10px 18px; min-height:44px; cursor:pointer; transition:color var(--t-fast), border-color var(--t-fast);
      }
      .artist-why-not:hover { color:var(--text-pri); border-color:rgba(255,255,255,0.30); }
      .artist-why-not[aria-pressed="true"] { color:var(--accent-on-dark); border-color:rgba(81,104,252,0.45); background:rgba(81,104,252,0.10); }
      .artist-why-not:focus-visible { outline:3px solid var(--brand-blue-light); outline-offset:2px; }
      .artist-why-receipt { font-family:'Onest',sans-serif; font-size:13px; color:var(--accent-on-dark); margin:0; min-height:18px; flex:1; min-width:200px; }

      /* ---- Top tracks (row, art-tint) --------------------------------------- */
      .artist-tracks { display:flex; flex-direction:column; }
      .artist-track-row {
        display:flex; align-items:center; gap:14px; padding:10px 12px; min-height:56px;
        border-radius:var(--r-base); border:none; background:none; cursor:pointer;
        font:inherit; color:inherit; text-align:left; width:100%; transition:background var(--t-fast);
      }
      .artist-track-row:hover { background:var(--surf-glass-12); }
      .artist-track-row:focus-visible { outline:3px solid var(--brand-blue-light); outline-offset:2px; }
      .artist-track-rank {
        font-family:'Onest',sans-serif; font-size:24px; font-weight:900; color:var(--text-quat);
        min-width:30px; text-align:right; flex-shrink:0; line-height:1; font-variant-numeric:tabular-nums;
      }
      /* art-tint cover + монограмма (NOT gradient placeholder) */
      .artist-track-cover {
        position:relative; width:44px; height:44px; border-radius:8px; flex-shrink:0;
        display:flex; align-items:center; justify-content:center; overflow:hidden;
        background:var(--brand-blue-light);
      }
      .artist-track-cover::after { content:""; position:absolute; inset:0; background:radial-gradient(110% 110% at 30% 25%, rgba(255,255,255,0.16), rgba(0,0,0,0.28)); }
      .artist-track-mono { position:relative; z-index:1; font-family:'Onest',sans-serif; font-size:15px; font-weight:800; color:#fff; }
      .artist-track-meta { flex:1; min-width:0; display:flex; flex-direction:column; gap:2px; }
      .artist-track-title { font-family:'Onest',sans-serif; font-size:15px; font-weight:600; color:var(--text-pri); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
      .artist-track-album { font-family:'Onest',sans-serif; font-size:13px; color:var(--text-quat); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
      .artist-track-dur { font-family:'Onest',sans-serif; font-size:13px; color:var(--text-quat); flex-shrink:0; font-variant-numeric:tabular-nums; }

      /* ---- Stations (on-brand радио) ---------------------------------------- */
      .artist-stations-sub { font-family:'Onest',sans-serif; font-size:14px; color:var(--text-sec); margin:0 0 16px; line-height:1.45; }
      .artist-stations { display:flex; flex-wrap:wrap; gap:12px; }
      .artist-station-chip {
        display:inline-flex; align-items:center; gap:12px; width:260px; min-height:56px;
        padding:12px 18px; border-radius:var(--r-pill); background:var(--surf-glass-12);
        border:1px solid rgba(255,255,255,0.12); color:var(--text-sec); font:inherit; cursor:pointer;
        transition:background var(--t-fast), color var(--t-fast);
      }
      .artist-station-chip:hover { background:var(--surf-glass-20); color:var(--text-pri); }
      .artist-station-chip:focus-visible { outline:3px solid var(--brand-blue-light); outline-offset:2px; }
      .artist-station-eq { width:18px; height:14px; flex-shrink:0; color:var(--accent-on-dark); opacity:0.85; }
      .artist-station-name { font-family:'Onest',sans-serif; font-size:15px; font-weight:600; color:var(--text-pri); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; flex:1; }
      .artist-station-freq { font-family:'Onest',sans-serif; font-size:13px; color:var(--text-quat); flex-shrink:0; }

      @media (prefers-reduced-motion: reduce) {
        .artist-action-primary:hover, .artist-track-row:hover { transform:none; }
      }
```

**Новый responsive-блок (вставить вместо 6764–6878).** Сохраняет surface-варианты (mobile/tv), все cyan→blue:

```css
      /* ---- Artist page: responsive ------------------------------------------ */
      @media (max-width: 920px) {
        .artist-hero { gap:28px; padding:36px 24px; min-height:0; }
        .artist-photo { width:150px; height:150px; }
        .artist-photo-mono { font-size:52px; }
        .artist-name { font-size:40px; }
        .artist-section { padding:0 24px 36px; }
      }
      @media (max-width: 560px) {
        .artist-hero { flex-direction:column; align-items:flex-start; text-align:left; }
        .artist-name { font-size:34px; }
        .artist-station-chip { width:100%; }
        .artist-why-foot { gap:10px; }
      }
      [data-surface="mobile"] .artist-hero { flex-direction:column; align-items:flex-start; gap:24px; padding:28px 20px; }
      [data-surface="mobile"] .artist-photo { width:140px; height:140px; }
      [data-surface="mobile"] .artist-photo-mono { font-size:48px; }
      [data-surface="mobile"] .artist-name { font-size:34px; }
      [data-surface="mobile"] .artist-section { padding:0 20px 32px; }
      [data-surface="mobile"] .artist-station-chip { width:100%; }
      [data-surface="tv"] .artist-name { font-size:72px; }
      [data-surface="tv"] .artist-hero { padding:64px 56px; gap:56px; }
      [data-surface="tv"] .artist-photo { width:300px; height:300px; }
      [data-surface="tv"] .artist-photo-mono { font-size:96px; }
      [data-surface="tv"] .artist-action-primary,
      [data-surface="tv"] .artist-action-secondary { font-size:18px; padding:18px 32px; min-height:56px; }
      [data-surface="tv"] .artist-section { max-width:1200px; padding:0 56px 56px; }
```

**Token inventory (каждая var):** `--brand-blue-light` (#5168FC, single accent — кнопки/focus/dots/glow + RGB 81,104,252 для tint/border), `--accent-on-dark` (#8094ff AA — overline/demo-бейдж/«почему» цифры/prov-акцент/eq-icon/quitтанции), `--np-accent` (content-derived hero hue, JS-set), `--surf-glass-12/-20` (chip/row bg), `--text-pri/-sec/-quat` (текст-иерархия), `--r-base` (10px), `--r-pill` (999px), `--t-fast` (180ms), Onest на каждом text-node. **НЕ используется:** `--brand-cyan` (retired в этом scope). White-scale rgba — все pre-existing.

---

## 6. `window.GorodArtist` (new trailing IIFE) — append после 14140

Append после `</script>`@14140 (закрытие GorodContext), последний блок перед `</body>`@14142. Детерминированный, null-guarded, esc-санитизация, hashchange-wired. Reject пишет в общий `gorodfm_rejected`.

```html
  <script>
  /* ---- GOROD-047b — Артист deep-dive: «почему тебе этот артист» (поведенческое,
     НЕ collaborative), reject в общий gorodfm_rejected corpus (тот же ров, что
     TwinrWhy/GorodTaste/Profile/Recap), art-tint hero + монограмма (НЕ силуэт),
     топ-треки row, станции (on-brand радио). Аддитивный trailing-модуль. */
  (function () {
    'use strict';
    var REJ_KEY = 'gorodfm_rejected', TASTE_KEY = 'gorodfm_taste';
    // Artist-level reject facets (prefix art_ — no collision with player-level artist/vocal/tempo).
    // Human labels MUST also be mirrored into REJ_LABELS canon of GorodProfile/Recap/Taste (Integrate seam §10).
    var ART_LABELS = { art_arena: 'Арена-рок', art_vocal_m: 'Мужской вокал' };

    // «Почему» — каждый пункт = ПОВЕДЕНИЕ или ATTRIBUTE-MATCH, никогда collaborative.
    var WHY = [
      { id:null,          t:'12 треков дослушано до конца',                              prov:'твоё поведение за месяц' },
      { id:'art_arena',   t:'Арена-рок — <b>80%</b> совпадает с твоим вектором',          prov:'грань твоего профиля' },
      { id:'art_vocal_m', t:'Мужской вокал, мощный припев — совпадает с тем, что ты усиливал', prov:'ты поднимал эту грань' },
      { id:null,          t:'Не пропустил ни один трек этого артиста на «Городе»',         prov:'0 скипов' }
    ];
    var TRACKS = [
      { t:'Believer',          al:'Night Visions',   d:'03:38' },
      { t:'Thunder',           al:'Evolve',          d:'03:08' },
      { t:'Radioactive',       al:'Night Visions',   d:'03:07' },
      { t:'Demons',            al:'Night Visions',   d:'02:58' },
      { t:'Whatever It Takes', al:'Evolve',          d:'03:21' }
    ];
    var ARTIST = 'IMAGINE DRAGONS';

    function $(id){ return document.getElementById(id); }
    function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
    function getRej(){ try { return JSON.parse(localStorage.getItem(REJ_KEY)||'[]'); } catch(e){ return []; } }
    function setRej(a){ try { localStorage.setItem(REJ_KEY, JSON.stringify(a)); } catch(e){} }
    function mono(s){ var p=String(s||'').trim().split(/\s+/); return ((p[0]||' ')[0]+((p[1]||'')[0]||'')).toUpperCase().slice(0,2); }
    // deterministic blue-family hue from name (no random) — for track-cover/hero tint variety within blue
    function tintFor(s){ var h=0,i; for(i=0;i<String(s).length;i++){ h=(h*31+s.charCodeAt(i))>>>0; } var hue=215+(h%40); return 'hsl('+hue+',62%,'+(34+(h%14))+'%)'; }

    function renderWhy(){
      var list=$('artist-why-list'); if(!list) return;
      var rej=getRej();
      list.innerHTML='';
      WHY.forEach(function(w){
        var li=document.createElement('li'); li.className='artist-why-item';
        var isRej = w.id && rej.indexOf(w.id)!==-1;
        if(isRej) li.classList.add('is-rejected');
        var btn = w.id
          ? '<button class="artist-why-reject" type="button" data-rej="'+esc(w.id)+'" aria-pressed="'+(isRej?'true':'false')+'">'+(isRej?'вернуть':'не моё')+'</button>'
          : '';
        li.innerHTML =
          '<span class="artist-why-dot" aria-hidden="true"></span>'+
          '<span class="artist-why-body"><span class="artist-why-text">'+w.t+'</span>'+
          '<span class="artist-why-prov">'+esc(w.prov)+'</span></span>'+ btn;   // w.t = trusted literal with <b>%</b>
        list.appendChild(li);
      });
    }
    function renderTracks(){
      var box=$('artist-tracks'); if(!box) return;
      box.innerHTML='';
      TRACKS.forEach(function(tr,i){
        var b=document.createElement('button'); b.type='button'; b.className='artist-track-row'; b.setAttribute('role','listitem');
        b.setAttribute('data-track-title', tr.t); b.setAttribute('data-track-artist', ARTIST);
        b.setAttribute('aria-label', tr.t+', '+tr.d);
        b.innerHTML =
          '<span class="artist-track-rank" aria-hidden="true">'+(i+1)+'</span>'+
          '<span class="artist-track-cover" aria-hidden="true" style="background:'+tintFor(tr.t)+'"><span class="artist-track-mono">'+esc(mono(tr.t))+'</span></span>'+
          '<span class="artist-track-meta"><span class="artist-track-title">'+esc(tr.t)+'</span>'+
          '<span class="artist-track-album">'+esc(tr.al)+'</span></span>'+
          '<span class="artist-track-dur tabular" aria-label="длительность '+esc(tr.d)+'">'+esc(tr.d)+'</span>';
        box.appendChild(b);
      });
    }
    function paintNot(){
      var btn=$('artist-why-not'); if(!btn) return;
      var rej=getRej(), off = rej.indexOf('art_arena')!==-1 && rej.indexOf('art_vocal_m')!==-1;
      btn.setAttribute('aria-pressed', off?'true':'false');
      btn.textContent = off ? 'Артист скрыт — вернуть' : 'Это не про меня';
    }
    function setHeroTint(){
      var ph=$('artist-photo'), m=$('artist-photo-mono'); if(!ph) return;
      var url = ph.getAttribute('data-artist-photo');
      if(url){ var img=new Image(); img.alt=''; img.onload=function(){ ph.appendChild(img); }; img.src=url; } // real-photo seam (Ф1+)
      ph.style.background = tintFor(ARTIST);
      if(m) m.textContent = mono(ARTIST);
    }
    function receipt(msg){ var r=$('artist-why-receipt'); if(r) r.textContent=msg; }

    function rejectFacet(id){
      if(!id) return;
      var rej=getRej(), i=rej.indexOf(id), nowRej;
      if(i===-1){ rej.push(id); nowRej=true; } else { rej.splice(i,1); nowRej=false; }
      setRej(rej); renderWhy(); paintNot();
      var label = ART_LABELS[id] || id;
      receipt(nowRej
        ? ('Убрал «'+label+'» — следующее радио артиста меньше опирается на эту грань.')
        : ('Вернул «'+label+'» в основания.'));
      if(window.TwinrWave) window.TwinrWave.bump();           // visible effect if wave present
    }
    function toggleArtist(){
      var rej=getRej(), off = rej.indexOf('art_arena')!==-1 && rej.indexOf('art_vocal_m')!==-1;
      ['art_arena','art_vocal_m'].forEach(function(id){
        var k=rej.indexOf(id);
        if(off){ if(k!==-1) rej.splice(k,1); }       // currently off → turn back on (remove rejects)
        else  { if(k===-1) rej.push(id); }           // turn off (reject both)
      });
      setRej(rej); renderWhy(); paintNot();
      receipt(off ? 'Вернул артиста в волну.' : 'Убрал «'+ARTIST+'» — реже в твоём радио. Можно вернуть.');
      if(window.TwinrWave) window.TwinrWave.bump();
    }

    function render(){ setHeroTint(); renderWhy(); renderTracks(); paintNot(); }

    var wired=false;
    function wire(){
      if(wired) return;
      var sect=document.querySelector('[data-page="artist"]'); if(!sect) return;

      var toggle=$('artist-why-toggle'), list=$('artist-why-list');
      if(toggle && list){
        toggle.addEventListener('click', function(){
          var open = toggle.getAttribute('aria-expanded')==='true';
          toggle.setAttribute('aria-expanded', open?'false':'true');
          list.hidden = open;
          toggle.textContent = open ? 'Показать, на чём это держится' : 'Свернуть основания';
        });
      }
      var listEl=$('artist-why-list');
      if(listEl){ listEl.addEventListener('click', function(e){
        var b=e.target.closest('.artist-why-reject'); if(!b) return;
        rejectFacet(b.getAttribute('data-rej'));
      }); }
      var notBtn=$('artist-why-not'); if(notBtn) notBtn.addEventListener('click', toggleArtist);

      // radio CTA — honest now-playing meta + provenance line (reuses player chrome)
      var radio=$('artist-btn-radio');
      if(radio) radio.addEventListener('click', function(){
        var t=$('player-track-title'), a=$('player-track-artist'),
            ft=$('player-full-title'), fa=$('player-full-artist'),
            rs=$('player-track-reason'), span=rs&&rs.querySelector('span');
        if(t) t.textContent='Радио '+ARTIST; if(a) a.textContent=ARTIST;
        if(ft) ft.textContent='Радио '+ARTIST; if(fa) fa.textContent=ARTIST;
        if(span) span.innerHTML='Радио по артисту: <b>арена-рок + мужской вокал</b> — грани твоего вектора';
        if(typeof openPlayer==='function') openPlayer();        // openPlayer in router scope (initArtist used it)
      });

      var fav=$('artist-btn-fav');
      if(fav) fav.addEventListener('click', function(){
        var p=fav.getAttribute('aria-pressed')==='true'; fav.setAttribute('aria-pressed', p?'false':'true');
      });

      // track rows (delegated) — open player; keyboard via native <button>
      var tracks=$('artist-tracks');
      if(tracks) tracks.addEventListener('click', function(e){
        var row=e.target.closest('.artist-track-row'); if(!row) return;
        var t=$('player-track-title'), a=$('player-track-artist'),
            ft=$('player-full-title'), fa=$('player-full-artist');
        var title=row.getAttribute('data-track-title')||'Трек';
        if(t) t.textContent=title; if(a) a.textContent=ARTIST;
        if(ft) ft.textContent=title; if(fa) fa.textContent=ARTIST;
        if(typeof openPlayer==='function') openPlayer();
      });

      // stations → #/home (navigate in router scope)
      var stations=document.querySelector('[data-page="artist"] .artist-stations');
      if(stations) stations.addEventListener('click', function(e){
        var chip=e.target.closest('.artist-station-chip'); if(!chip) return;
        if(typeof navigate==='function') navigate('#/home');
        else location.hash='#/home';
      });
      wired=true;
    }
    function onRoute(){ if((location.hash||'')==='#/artist'){ wire(); render(); } }
    window.addEventListener('hashchange', onRoute);
    if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', onRoute); else onRoute();
    window.GorodArtist = { render:render };
  })();
  </script>
```

**Замечание о `openPlayer`/`navigate` scope.** Старый `initArtist`@11958 — IIFE внутри главного router-скрипта, где `openPlayer`/`navigate` видны как функции этого скрипта. Новый `GorodArtist` — отдельный trailing-IIFE (как GorodContext); `openPlayer`/`navigate` там НЕ в лексическом scope. Поэтому: (а) `initArtist`@11958–12060 переписывается до тонкого no-op-стаба ИЛИ удаляется и его обязанности переходят в `GorodArtist` через `window.*`-мост. **Резолюция (binding):** удалить тело `initArtist` (заменить на пустой комментарий-стаб в диапазоне 11958–12060, чтобы не сдвигать строки соседнего кода), а `GorodArtist` использует `typeof openPlayer/navigate==='function'` guard + `location.hash` fallback. Это устраняет дубль-wiring (двойные listeners) и держит модуль decoupled как остальные Gorod*-модули. Если `openPlayer` недоступен глобально — radio/track всё равно меняют meta (honest), просто плеер не разворачивается; не падает.

**Correctness:** try/catch на всех LS; guard на каждый `$()`/`querySelector`; `esc()` на динамике; `w.t` строки = module-константы (trusted `<b>%</b>` литералы, не user-input) → `innerHTML` безопасен; delegated listeners (переживают re-render); zero `Math.random` (детерминизм: `tintFor` хешит имя); `if(window.TwinrWave)` guard.

---

## 7. Edit manifest (ordered, line-anchored — все пересверены в этой сессии)

1. **CSS hero/sections/why/tracks/stations** — заменить строки **4462–4934** на §5 первый блок (`[data-page="artist"]` … `.artist-station-freq` + reduced-motion). Старый блок начинается `[data-page="artist"] { padding-bottom: 80px; }`@4462, заканчивается `.artist-station-freq {…}`@4934 (перед `/* === LIVES PAGE */`@4936).
2. **CSS responsive** — заменить строки **6764–6878** (от `/* ---- Artist page: responsive */`@6764 до конца `[data-surface="tv"] .artist-section`@6876+закрытие) на §5 второй блок. Граница: следующий не-artist селектор после 6878.
3. **DOM** — заменить строки **8281–8642** (`<section data-page="artist"…>`@8281 … закрывающий `</section>`@8642) на §3 verbatim. Comment `<!-- /#/artist -->`@8643 сохранить/воспроизвести.
4. **JS initArtist** — заменить тело **11958–12060** (`(function initArtist() {`@11958 … `})(); /* end initArtist */`@12060) на пустой стаб: `/* GOROD-047b: Артист-wiring перенесён в trailing-модуль window.GorodArtist (decoupled, как GorodContext). */` — сохранить как самостоятельный комментарий вместо IIFE, чтобы не плодить дубль-listeners.
5. **Module** — append §6 `<script>window.GorodArtist</script>` после строки **14140** (`</script>` закрытия GorodContext-IIFE@14139–14140), последним блоком перед `</body>`@14142.
6. **(Integrate-фаза, НЕ здесь)** — REJ_LABELS-канон: добавить `art_arena:'Арена-рок', art_vocal_m:'Мужской вокал'` в GorodProfile@13670, GorodRecap (REJ_LABELS), GorodTaste@13131 — чтобы reject артиста читался на тех экранах. Без этого reject пишется корректно, но на Profile/Recap не показывается человеко-понятным лейблом (фильтруется как unknown id — не ломает, просто не виден там).

Все anchor-пары пересверены: 4462/4934 (CSS), 6764/6878 (responsive), 8281/8642/8643 (DOM), 11958/12060 (initArtist), 14139/14140 (GorodContext end), 14142 (`</body>`), 10931 (VALID_ROUTES — не трогаем), 13339 (TwinrWhy gorodfm_rejected writer — схема), 13670/13131 (REJ_LABELS canon — Integrate).

---

## 8. Holy-Grail / anti-slop checklist

| Gate | Status | Evidence |
|---|---|---|
| **Onest only** | ✅ | Каждый text-node `font-family:'Onest',sans-serif`. |
| **near-black + 1 accent** | ✅ | bg unchanged; единственный акцент `--brand-blue-light`; малый accent-текст `--accent-on-dark`. Cyan retired в scope. |
| **`--accent-on-dark` для малого accent-текста** | ✅ | overline, demo-бейдж, «почему» цифры, prov-акцент, eq-icon, квитанции (AA 6.8:1). |
| **art-tint вместо fake-обложки** | ✅ | Hero = art-tint+монограмма «ID» (НЕ силуэт); track-cover = art-tint+монограмма (НЕ gradient-плашка). `tintFor` синяя семья. |
| **❌ SVG-силуэт** | ✅ | Удалён hero@8290–8299; единственные SVG = EQ-полоски станций (вектор, on-brand) + heart-icon. |
| **❌ gradient-плейсхолдеры** | ✅ | 10 track-gradient + 6 album-gradient + photo multi-stop удалены; flat tint + radial wash (surface-эффект, не multi-stop bg). |
| **❌ multi-stop gradient bg** | ✅ | `.artist-photo` flat `--np-accent`; `::after` = subtle radial wash (тень/блик), не цветной градиент. |
| **❌ collaborative «фанаты также»** | ✅ | Ни одного social-сигнала; каждый «почему»-буллет = поведение или attribute-match (C4, AUDIT §4). |
| **демо-маркировка** | ✅ | `.artist-why-demo` бейдж «демо-вектор» на блоке «почему» (§0 mandate). |
| **fidelity-петля (reject в общий corpus)** | ✅ | Reject пишет `gorodfm_rejected` (тот же ров, что TwinrWhy/Profile/Recap/Taste) — не 4-й остров. |
| **targets ≥44px** | ✅ | primary/secondary/not/toggle 44px; row 56px; station 56px; reject-chip 32px (вторичный, не основной — соответствует §1.1 «skip вторичен»; основные действия ≥44). |
| **focus-visible 3px** | ✅ | Все интерактивы `outline:3px solid var(--brand-blue-light); outline-offset`. |
| **prefers-reduced-motion** | ✅ | hover-transform отключён; нет авто-анимаций. |
| **parametric copy, не маркетинг** | ✅ | «12 треков дослушал», «80% совпадает», «0 скипов» — конкретно/поведенчески. bio-блёрб удалён. |
| **zero console errors** | ✅ | try/catch LS; guards $/querySelector/TwinrWave; delegated listeners; esc на динамике; детерминизм (no random). |
| **additive single-file** | ✅ | In-place replace 3 диапазонов + 1 trailing-IIFE; route не добавлен; LS-ключ переиспользован; neutral на других экранах. |
| **045/pixel-perfect не триггерится** | ✅ | `#/home` (7443+, Figma 2174:422) вне всех диапазонов (§1.2). |
| **on-brand радио (не каталог)** | ✅ | «Альбомы» удалены; станции с под-текстом «радио, не плейлист». |

---

## 9. Additive-safety / не-ломает-built (доказательство)

- **GorodTaste W1-петля (built)** — НЕ тронута: спек только ДОПИСЫВАЕТ в `gorodfm_rejected` новые id `art_*`. GorodTaste@13130 читает массив и матчит свои facet-id (`artist`/`vocal`/`tempo`) — unknown `art_*` id просто игнорируются её фильтром (как Profile@13717 `.filter(REJ_LABELS[id])`). Никакого расхождения модели фактов: тот же массив, разные пространства id. После Integrate (§7.6) `art_*` станут видимы и на Profile/Recap.
- **TwinrWhy (built, @13339)** — пишет тот же ключ той же схемой (массив id). Параллельная запись из GorodArtist не конфликтует (read-modify-write весь массив, последний writer выигрывает по facet — но id-пространства не пересекаются, так что взаимного затирания нет).
- **051 GorodContext (built, @14101)** — отдельный модуль/ключ (`gorodfm_context`); GorodArtist appended ПОСЛЕ него, не трогает. Оба self-wire на свой `location.hash`.
- **052 GorodProfile / 050 GorodRecap (built)** — читают `gorodfm_rejected` read-only; новые `art_*` id фильтруются их REJ_LABELS до Integrate → не ломаются, просто не показывают artist-reject (graceful).
- **042 NowPlayingTint / `--np-accent` (built)** — hero использует `--np-accent` как content-derived hue; JS перезаписывает `.style.background` через `tintFor` (детерминированно), не конфликтует с глобальным `--np-accent` (локальный inline-style на одном node).
- **Player chrome (`#player-track-reason`, `openPlayer`)** — radio/track CTA пишут meta тем же путём, что built `openArtistPlayer`@11961; `#player-track-reason` provenance-строка = transient (как 051 C5 — перезатрётся плеером на смене трека; honest echo, не source of truth).
- **Route/back-history** — `#/artist` в `VALID_ROUTES`@10931 не тронут; Card 4@7368 и track-row nav продолжают вести сюда; back+mini-player (blueprint §1.1 «без тупиков») сохранён router'ом.
- **`initArtist` stub** — замена тела на комментарий в том же диапазоне 11958–12060 не сдвигает строки соседних IIFE (initFavorites@12064 и далее), значит остальные line-anchored правки в edit-manifest остаются валидны при последовательном применении (применять сверху-вниз: CSS → DOM → JS, чтобы ранние правки не сдвигали поздние anchor'ы — все диапазоны не-перекрывающиеся и в возрастающем порядке).
