# SPEC — Светлая тема (Apple-grade) · Город ФМ

> Источник: research-workflow `w2h1wh4da` (4 параллельных ресёрча → синтез → adversarial-критик), 2026-06-03 cont-12.
> Статус: **BUILD-READY**. Критик-вердикт = REVISE → правки в §8 ОБЯЗАТЕЛЬНЫ (в т.ч. 2 a11y-бага: невидимый focus-ring на синей play-кнопке + label-на-синем AA-fail). НЕ реализовано — спека для следующей build-сессии.
> Дисциплина cont-12: re-grep якоря перед edit (строки дрейфуют), `?v=N` cache-bust, :8770, зеркалить в standalone.

---

# Светлая тема (Apple-grade) — Build-Ready Spec · Город ФМ

> Файл: `C:/Users/elbics/Desktop/design-project/designs/gorod-fm.html` (+ зеркало `gorod-fm-standalone.html`). Параллельная тема через `data-theme="day"`. Тёмная `cinema` остаётся дефолтом в проде. Номера строк дрейфуют — **re-grep якоря перед каждым edit** (дисциплина cont-12).

---

## 1. Тезис — что делает НАШУ белую тему премиальной (не generic SaaS white)

**Одна организующая идея: «тёплая бумага + слоистая мягкая тень + одна сдержанная синяя».**

Generic-SaaS-white проваливается тремя способами, и мы избегаем всех трёх:

1. **Тёплая нейтральная «бумага», а не стерильный `#fff`.** База = warm-neutral off-white `#FAFAF7` (на 1 тёплый тик от белого), карточки = чистый `#FFFFFF` плывут НА базе. Это эппловский паттерн `systemGroupedBackground` (#F2F2F7 серый фон + белые карточки), но мы сдвигаем хью на ~2–4° в **тёплую** сторону вместо эпловского cool blue-grey. Тёплое поле + холодный синий акцент = классическое премиальное напряжение, которого нет у all-cool палитры Apple. Это «или лучше уровня Apple».
2. **Тень — основной сигнал глубины, а не бордеры.** В dark-режиме глубину давали более светлые `--surface-*` поверх тёмной базы. На белом «светлее белого» не бывает → **двухслойная мягкая тень с сине-чёрным подтоном (`rgb(20,22,40)`)** несёт глубину; hairline-бордеры демотированы до вторичной роли. Чёрные ambient-тени из dark на белом читаются как грязные смазы — их НЕЛЬЗЯ переносить.
3. **Одна синяя, дисциплина сохранена.** Цвет — это глагол (interactive/selected/focus), не декор. Никакого dynamic-cover-recolor (Яндекс.Музыка — dark-only, перегружено; Apple Music adaptive — жалобы на слепящий экран). Мы это уже выиграли в cont-11 — light-тема сохраняет.

**Сверх-Apple ход (опционально, Move-3):** whisper-grain на статичной базе (1–2% `feTurbulence`) + настоящий translucent material на хроме (плеер/sheet/topbar) — даёт бумаге материальность, убивает «мёртвый цифровой белый». Только на базе, никогда на тексте/карточках.

---

## 2. Token block — финальный dark→light mapping (AA-verified)

Вставить **сразу после** закрывающей `}` блока `:root` (L177), внутри `@layer tokens`. Имена переменных НЕ меняем (zero call-site edits) — меняем только значения per-theme. Ratios измерены против `--bg-base #FAFAF7` (и/или `#FFFFFF` где указано).

| Token | DARK (текущее) | LIGHT `data-theme="day"` | AA-ratio (на light) | Note |
|---|---|---|---|---|
| `--bg-base` | `#0B0C0F` | **`#FAFAF7`** | — | тёплая бумага-сцена, НЕ `#fff`, НЕ cool `#F2F2F7` |
| `--home-bg-base` | `#0C0B0B` | **`#F4F4F1`** | — | home чуть глубже базы |
| `--brand-black` | `#0C0B0B` | **`#FFFFFF`** | — | `html` bg-fallback (L189 `background:var(--brand-black)`) |
| `--surface-0` | `#111318` | **`#FFFFFF`** | pri 17.0:1 | карточки плывут НАД базой (инверсия dark) |
| `--surface-1` | `#15171D` | **`#FFFFFF`** | pri 17.0:1 | |
| `--surface-2` | `#1B1E26` | **`#F4F4F1`** | pri 16.3:1 | recessed wells / inputs |
| `--surface-3` | `#23262F` | **`#EBEBE6`** | pri 14.3:1 | глубокий well / pressed |
| `--text-pri` | `#FFFFFF` | **`#1A1C1F`** | **16.3:1** | warm near-black, НЕ pure `#000` |
| `--text-sec` | `rgba(255,255,255,.62)` | **`rgba(0,0,0,.60)`** | **5.7:1** | AA ✅ (НЕ зеркалить opacity вслепую) |
| `--text-ter` | `rgba(255,255,255,.40)` | **`rgba(0,0,0,.40)`** | 2.83:1 | ⚠️ decorative-only (тот же контракт, что dark .40 — никогда essential text) |
| `--text-quat` | `rgba(235,235,245,.60)` | **`rgba(0,0,0,.55)`** | ~3.8:1 | legacy alias (мигрирует в sec/ter) |
| `--brand-blue-light` | `#5168FC` | **`#5168FC`** (без изм.) | fill, не текст | большие заливки/кнопки ТОЛЬКО (см. §3) |
| `--brand-blue-hover` | `#6477ff` | **`#3346C4`** | 7.1:1 | darken-on-hover (light-конвенция) |
| `--accent-on-dark` | `#8094ff` (6.8:1 dark) | **`#3A4ED0`** | **6.31:1** на bg / 5.99 на surface-2 | имя сохранено → ВСЕ ≤14px accent-текст + focus-ring; AA-safe |
| `--tint-blue-light-20` | `rgba(81,104,252,.2)` | **`rgba(81,104,252,.12)`** | чёрн.текст 14.7:1 | active chip + home player bar |
| `--np-accent` | `var(--brand-blue-light)` | `var(--brand-blue-light)` | — | хью монограммы (JS color-from-art ретайрнут L13394 ✓) |
| `--player-accent` | `var(--brand-blue-light)` | `var(--brand-blue-light)` | — | |
| `--success` | `#34d399` | **`#0A7A53`** | **5.1:1** | `#34d399` = 1.84:1 невидимо на белом → темнее, MANDATORY |
| `--hairline` | `rgba(255,255,255,.08)` | **`rgba(0,0,0,.09)`** | structural | свет требует чуть больше веса |
| `--divider` | `rgba(255,255,255,.06)` | **`rgba(0,0,0,.07)`** | structural | |
| `--border-strong` | `rgba(255,255,255,.14)` | **`rgba(0,0,0,.14)`** | 1.32:1 visible | |
| `--inset-top` | `inset 0 1px 0 rgba(255,255,255,.05)` | **`inset 0 1px 0 rgba(255,255,255,.9)`** | — | top-light highlight = real light-depth |
| `--surf-hover` | `rgba(255,255,255,.10)` | **`rgba(0,0,0,.04)`** | — | |
| `--surf-active` | `rgba(255,255,255,.16)` | **`rgba(0,0,0,.07)`** | — | |
| `--featured-cta-bg` | `rgba(11,12,15,.72)` | **`rgba(255,255,255,.78)`** | — | translucent material бар |
| `--tile-darkening` | `rgba(3,3,3,.35)` | **`rgba(0,0,0,.06)`** | — | row-darken мягче на белом |
| **NEW** `--accent-text` | _(добавить в dark = `var(--accent-on-dark)`)_ | **`#3A4ED0`** | 6.31:1 | seam-токен для «почему»/demo (см. §6) |
| **NEW** `--cover-mix-base` | _(добавить в dark = `#111318`)_ | **`#FFFFFF`** | — | floor для art-tint `color-mix` (см. §6) |

### Shadow scale (свету нужны НАСТОЯЩИЕ мягкие тени; сине-чёрный подтон `rgb(20,22,40)`, не серый/грязный)

| Token | DARK | LIGHT |
|---|---|---|
| `--sh-1` | `0 1px 2px rgba(0,0,0,.30)` | **`0 1px 2px rgba(20,22,40,.06), 0 1px 1px rgba(20,22,40,.04)`** |
| `--sh-2` | `0 4px 12px rgba(0,0,0,.35)` | **`0 4px 12px -2px rgba(20,22,40,.10), 0 2px 4px rgba(20,22,40,.05)`** |
| `--sh-3` | `0 12px 32px -8px rgba(0,0,0,.45)` | **`0 12px 28px -8px rgba(20,22,40,.14), 0 4px 8px -4px rgba(20,22,40,.07)`** |
| `--sh-4` | `0 24px 56px -16px rgba(0,0,0,.50)` | **`0 24px 56px -16px rgba(20,22,40,.18), 0 8px 16px -8px rgba(20,22,40,.08)`** |

### Drop-in CSS block

```css
/* === LIGHT "day" theme — parallel override (Apple-grade) === */
/* Вставить сразу после :root{} на L177, внутри @layer tokens */
html[data-theme="day"] {
  /* Backgrounds — тёплая бумага, НЕ стерильный #fff */
  --bg-base:#FAFAF7; --home-bg-base:#F4F4F1; --brand-black:#FFFFFF;
  --featured-cta-bg:rgba(255,255,255,.78);
  --bg-overlay:linear-gradient(-88.75deg, rgba(250,250,247,0) 70%, rgba(250,250,247,.45) 88%, rgba(250,250,247,.8) 100%);
  --tile-shade:linear-gradient(124.4deg, rgba(0,0,0,0) 40%, rgba(0,0,0,.12) 66%, rgba(0,0,0,.12) 80%);
  --tile-darkening:rgba(0,0,0,.06);

  /* Surfaces — elevation ЛИНЕЙКОЙ светлоты + тенью (инверсия dark) */
  --surface-0:#FFFFFF; --surface-1:#FFFFFF; --surface-2:#F4F4F1; --surface-3:#EBEBE6;

  /* Text ramp (AA-verified) */
  --text-pri:#1A1C1F; --text-sec:rgba(0,0,0,.60); --text-ter:rgba(0,0,0,.40); --text-quat:rgba(0,0,0,.55);

  /* Accent — ОДНА синяя, split по роли (критический AA-фикс) */
  --brand-blue-light:#5168FC;          /* большие заливки/кнопки ONLY */
  --brand-blue-hover:#3346C4;          /* darken-on-hover */
  --accent-on-dark:#3A4ED0;            /* имя сохранено → ВСЕ ≤14px accent-текст + focus; 6.31:1 AA */
  --accent-text:#3A4ED0;               /* NEW seam-токен (= accent-on-dark здесь) */
  --tint-blue-light-20:rgba(81,104,252,.12);
  --cover-mix-base:#FFFFFF;            /* NEW: light floor для art-tint */

  /* Green growth "+" — #34d399 невидим на белом → темнее */
  --success:#0A7A53;

  /* Hairlines / borders (свету нужен чуть больший вес) */
  --hairline:rgba(0,0,0,.09); --divider:rgba(0,0,0,.07); --border-strong:rgba(0,0,0,.14);
  --inset-top:inset 0 1px 0 rgba(255,255,255,.9);
  --surf-hover:rgba(0,0,0,.04); --surf-active:rgba(0,0,0,.07);

  /* Shadows — двухслойные, сине-чёрный подтон, НЕ серый */
  --sh-1:0 1px 2px rgba(20,22,40,.06), 0 1px 1px rgba(20,22,40,.04);
  --sh-2:0 4px 12px -2px rgba(20,22,40,.10), 0 2px 4px rgba(20,22,40,.05);
  --sh-3:0 12px 28px -8px rgba(20,22,40,.14), 0 4px 8px -4px rgba(20,22,40,.07);
  --sh-4:0 24px 56px -16px rgba(20,22,40,.18), 0 8px 16px -8px rgba(20,22,40,.08);
}
html[data-theme="day"]{ background:var(--bg-base); color:var(--text-pri); }

/* ДОБАВИТЬ в dark :root (чтобы call-sites были theme-agnostic): */
/*   --accent-text: var(--accent-on-dark);  --cover-mix-base: #111318;  */
```

---

## 3. Accent on light — разрешённая стратегия синего (контраст-математика)

**Корневой факт: `--brand-blue-light #5168FC` ПРОВАЛИВАЕТ AA для текста на светлом — 4.24:1 на `#FAFAF7`, 4.43:1 на чистом белом (AA нужно ≥4.5).** Это зеркало dark-проблемы (там `#5168FC` = 4.25:1 на `#111318`, поэтому мелкий текст использует `#8094ff`). Решение — **split по роли**, точная инверсия dark-логики:

| Роль | Токен | Значение | Контраст | Вердикт |
|---|---|---|---|---|
| Большие заливки, play-кнопка, taste-vector бары, CTA-фон | `--brand-blue-light` | `#5168FC` | UI-компонент 3:1 ✅ ; белый label = 4.43:1 | OK для **≥18.66px / 24px-bold** и иконок |
| ≤14px accent-ТЕКСТ («почему», demo-labels, ссылки, open-profile, facet-%) | `--accent-on-dark` → `#3A4ED0` | `#3A4ED0` | **6.31:1** на `#FAFAF7` | ✅ AA |
| Hover-fill | `--brand-blue-hover` | `#3346C4` | 7.1:1 | ✅ |
| Focus-ring (L215, ~30 `:focus-visible`) | `--accent-on-dark` → `#3A4ED0` | `#3A4ED0` | 6.31:1 (≥3 UI) | ✅ |

⚠️ **Решение-блокер (§ open decisions O2):** `#5168FC` + белый label = **4.43:1** — проходит для ≥18.66px/24px-bold, но **ПРОВАЛИВАЕТ 4.5:1 для normal-weight 14–15px label кнопки**. Для play-кнопки (иконка, крупная) — ок. Для любой кнопки с мелким текстом-на-синем: либо bump label ≥16px/600, либо resting-fill = `--brand-blue-hover #3346C4`.

Зелёный «+»: `#34d399` = **1.84:1** на белом (невидим) → `--success #0A7A53` (5.1:1) — **обязательно**, не опционально.

---

## 4. Per-surface notes (защищённые wedge-поверхности — должны пережить тему)

| Поверхность | Где | Что ломается на белом | Фикс |
|---|---|---|---|
| **Taste WAVE canvas** | JS `LAYERS` L12966–68, `#home-wave` L14407; strokes хардкод `#5168FC`/`#8094ff` alpha .30–.55; warm-branch `L.color==='#8094ff'` L12999/L14417 | На белом `#8094ff @ .42` почти невидим, `#5168FC` истончается; string-match цвета не переживёт свап | **JS-ветка по теме:** читать `document.documentElement.getAttribute('data-theme')` внутри draw; на `day` — stroke = `#3A4ED0` (или `var(--brand-blue)` rgb(20,80,170)), **alpha ↑ ~0.7–0.9**, lineWidth сохранить (свету нужен ink-вес). Перестать string-match-ить литерал — читать цвет из state. |
| **Recap share-card + petal bloom** | (a) on-screen SVG `.recap-screen-bloom` — CSS, theme-able ✓; (b) **PNG-экспорт `drawCanvasPNG()` L14118** — 100% хардкод dark (`#0B0C0F` L14122, `#ffffff`, petals `rgba(128,148,255)`/`rgba(81,104,252)`, `html2canvas backgroundColor:'#0B0C0F'` L14188) | Canvas **игнорирует CSS** → экспортнёт тёмную карточку даже в light | **Решение O3:** share-card по умолчанию **остаётся тёмным** (тёмная карточка на белом IG = интенционально). Если theme-following — `drawCanvasPNG` нужна theme-ветка: bg `#FFFFFF`, текст→`#1A1C1F`, petals→`#5168FC`, radial→faint-blue-on-white, green→`#0A7A53`. |
| **Profile redacted competitor strip** | `.profile-faux-*` L3144–51 (бары `rgba(255,255,255,.22/.13)`); `.profile-box--closed filter:grayscale(1)` L3142 | Белые бары на белом **исчезают**; grayscale на near-white = «пусто», не «заперто» | Бары → `rgba(0,0,0,.18)/.10` (dark-on-light). Blur + lock-глиф = primary «locked»-cue (переживают любой bg). Опц.: `repeating-linear-gradient` штриховка для «locked» через текстуру. Box bg чуть **темнее** страницы (`--surface-2`) чтобы читался как inert. |
| **Cover art-tint + Onest монограммы** | `color-mix(in oklab, var(--np-accent) X%, #111318)` L5588; `#191C24` L5624; **9× inline `#15171D`** L8790–8917 | Mix-floor = **хардкод-dark** → тёмные чипы на белом | Floor → токен `--cover-mix-base` (= `#FFFFFF` в day). `--np-accent` остаётся brand-blue ✓. Доб. inset-ring на cover (защита от white-cover-on-white): `box-shadow: inset 0 0 0 1px rgba(0,0,0,.08)`. Монограмма-буква = `--text-pri`; проверить per-tint что tint ≥ светлый чтобы тёмная буква прошла. |
| **Behavioral «почему» blue text** | `.home-radio-why-text b` L2141, `.artist-why-text b` L4943, `.profile-facet-pct` L3158 — все `--accent-on-dark` | `#8094ff` fail AA на белом | Через свап `--accent-on-dark → #3A4ED0` (6.31:1) — **load-bearing фикс**. `.track-why-text b` L5601 хардкодит `#fff` → перевести на `--text-pri`. |
| **«демо-» honesty labels** | `.discover-demo-tag` L4290, `.demo-tag` L5616 — `--accent-on-dark` + `rgba(81,104,252,.12)` bg + border alpha | Border/bg alpha-синие переживут; только текст fail | Текст `#3A4ED0` на tint `rgba(58,78,208,.08)`→`#EFF1FB` = 5.86:1 ✅. Система честности цела. |
| **72px mini-player + full sheet** | `.player-mini background:var(--surface-0)` L572; play-fill L592 `--brand-blue-light` | Тёмный бар →белый, но теряет «float» который dark давал контрастом | `--surface-0 #FFFFFF` + `--sh-3` (тень даёт float) + 1px top-hairline. Play-btn fill `#5168FC` ✓. Опц. material: `rgba(255,255,255,.78)` + `backdrop-filter:blur(22px) saturate(180%)`. |
| **Shadows / depth** | `--sh-1..4` ambient-black; `--inset-top` white-line | Чёрные тени .30–.50 = грязные смазы на белом | Свап на двухслойные `rgb(20,22,40)`-тинт (§2). `--inset-top` → `rgba(255,255,255,.9)` (top-light highlight = настоящий light-depth-cue). |

---

## 5. Mechanism — как добавить параллельную тему БЕЗ форка

**Критический факт:** `data-theme` сейчас — **висячий хук**. `applyTheme()` (L11107–11110) пишет атрибут в `<html>` + персистит `lsSet(LS_KEYS.theme)`, но **НИ ОДНОГО `[data-theme=...]` селектора в CSS нет** (grep: 0 matches). Ретайрнутая «warm» работала через `.bg-warm` opacity-слои, не токены. Тоггл L11211 сейчас флипает `cinema ↔ warm` (warm мёртв). → **Наш `[data-theme="day"]` блок будет ПЕРВЫМ реальным потребителем атрибута — нет legacy-каскада, с которым драться.** Вся dark-палитра живёт в одном `:root` (L85–177); второй `:root` (L6442) — только `@media(max-width:768px) --sidebar-w:0`, не тема.

**План (5 шагов):**

1. **Доб. sibling-override** `html[data-theme="day"]{…}` сразу после `:root` (§2 CSS-блок). Первый потребитель — каскада нет.
2. **Доб. 2 seam-токена в dark `:root`** чтобы call-sites стали theme-agnostic: `--accent-text: var(--accent-on-dark);` и `--cover-mix-base: #111318;`. Затем рефактор call-sites с сырых значений на эти токены (основной объём — см. §6).
3. **Тоггл:** `applyTheme()` уже флипает атрибут + персистит. Поменять L11211 `'warm'` → `'day'` (и/или добавить `'day'` как значение в Tweaks-группу `theme` L11190). Sidebar-иконка sun/moon (L11210).
4. **JS-canvas-ветки (CSS не достаёт):** wave `L.color==='#8094ff'` L12999/14417 + PNG `drawCanvasPNG` L14122/14188 — читать `getAttribute('data-theme')` внутри функций и ветвить (§4).
5. **Тоггл dev-gated в проде** — ровно как ретайрнутая warm (через Tweaks-панель). Persist уже работает (`lsGet(LS_KEYS.theme,'cinema')` L11871–72).

**Поверхности переживают тему ⟺ читают токены.** Token-clean → работают сразу. Нужна ручная работа: §6.

---

## 6. Hardcoded-dark reskin-debt (тонизировать ПЕРВЫМ — это то, что ломается на белом)

Grep-тоталы по файлу: **487× `rgba(255,255,255,…)`/`rgba(0,0,0,…)`/`#fff`** комбинированно. ~80% схлопываются в горстку токен-ретайрментов; load-bearing — ручные.

**A. Dark-hex как background (худшее — молча тёмное):**
- `#111318` background: **L3069** (`.profile-screen-bg`-class), **L3138 `.profile-box`**, **L3171 `.profile-panel`**, **L3179 `.profile-ad-strip`** → тёмные карточки на белом. → `var(--surface-0)`.
- `color-mix(…, #111318)` **L5588** (`.track-neighbor`) + `#191C24` **L5624** → mix-floor тёмный. → `var(--cover-mix-base)`.
- **9× inline `#15171D`** в `.track-history-cover style=` **L8790–8917** → inline art-tint floor, не тонизируется вообще. → класс + `var(--cover-mix-base)`.

**B. Хардкод white text** (`#fff`/`#ffffff`/`color:white`) — на белом **невидимы**: напр. `.track-why-text b` L5601, `.wave-dials-title`, `.profile-title`, `.profile-box-label`, `.profile-facet-name`, `.profile-ad-text b`. → `var(--text-pri)`.

**C. Хардкод `rgba(255,255,255,…)`** — бордеры/hover/fill baked inline (напр. `.profile-faux-*` L3147–48, `.profile-box` бордеры L3138/3171/3179). White-on-dark → инверт/невидимо на белом. → `--hairline`/`--surf-hover`/`--divider`.

**D. Хардкод `rgba(0,0,0,…)`** — ambient-shadows + `.profile-box--open` тень L3152. Слишком тяжело на белом. → `--sh-*`.

**E. JS, игнорирует CSS-тему (отдельный класс фикса):**
- **Recap PNG `drawCanvasPNG()`** L14122 `#0B0C0F`, L14133 `#ffffff`, L14130/14149 `#8094ff`, petals L14169–72, `html2canvas backgroundColor` L14188.
- **Wave `LAYERS`** hex L12966–68 + `L.color==='#8094ff'` L12999/14417.
- **Taste-map canvas** L13543/13549–50 `#5168FC` strokes + `rgba(128,148,255,.35)` — alpha .06–.22 кольца под dark, near-invisible на белом.

**Приоритет:** (1) 2 seam-токена + их рефактор; (2) A-список dark-hex backgrounds (×4 `#111318`, ×9 `#15171D`, `#191C24`); (3) profile faux-bar alpha-flip; (4) 2 JS-canvas ветки. Длинный хвост C/D — один проход token-retire.

---

## 7. Build order + open decisions

**Build order:**
1. **Doc-gate:** прочитать `DESIGN_PROTOCOL.md` + `anthropic_claude_design_prompt.md` (HOLY GRAIL).
2. Доб. 2 seam-токена в dark `:root` (`--accent-text`, `--cover-mix-base`) — НЕ ломает dark.
3. Вставить `html[data-theme="day"]` блок (§2).
4. Рефактор A-debt: `#111318`×4 → `--surface-0`; `color-mix` floor → `--cover-mix-base`; 9× `#15171D` → класс. (re-grep якоря!)
5. Рефактор «почему»/demo текст → `--accent-text`; хардкод `#fff` текст → `--text-pri`.
6. Profile faux-bar alpha-flip + cover inset-ring.
7. JS-ветки: wave (читать data-theme, alpha↑, stroke `#3A4ED0`) + PNG (решение O3).
8. Хвост C/D token-retire одним проходом.
9. Wire тоггл (L11211 `'warm'`→`'day'`, Tweaks-группа).
10. **Verify:** Chrome-проверка `?v=N` cache-bust на :8770; per-surface contrast-pass КАЖДОЙ wedge-поверхности на `#FAFAF7` (wave/petal/redacted-strip/монограммы — highest-risk); design-implementation-reviewer agent.
11. Зеркалить в `gorod-fm-standalone.html` (CSS/JS чисто; структурные tile-правки дивергируют).

**Open decisions для Эльбика:**
- **O1 — Имя темы:** `data-theme="day"` (этот spec) vs `"paper"` vs `"cinema-light"`. Влияет на тоггл-строку + Tweaks-значение. Дефолт: `day`.
- **O2 — Кнопка-label на синем:** `#5168FC` + белый 14–15px label = 4.43:1 (fail). Bump label ≥16px/600, ИЛИ resting-fill `#3346C4`? (play-кнопка-иконка ок как есть).
- **O3 — Share-card PNG:** остаётся тёмным по дефолту (тёмная карта на белом IG = интенционально, рекомендую) ИЛИ following-theme (нужна `drawCanvasPNG` ветка)?
- **O4 — Sub-AA `--text-ter` (2.83:1):** зеркалит dark `.40` контракт (decorative-only). Оставить как есть (рекомендую, нет регрессии vs dark) или поднять до AA-floor `#767676` (4.5:1)?
- **O5 — Сверх-Apple Move-3 (grain + material chrome):** включать whisper-grain (`feTurbulence` 1–2% на базе) + translucent material на плеере/sheet/topbar в v1, или отложить на polish-pass?
- **O6 — Тёплая база `#FAFAF7` vs cool Apple `#F2F2F7`:** spec ставит на тёплую (дифференциатор «или лучше»). Подтвердить, что тёплый тон не конфликтует с холодным синим в реальном рендере (Chrome-проверка решит).
- **O7 — Тоггл в проде:** dev-gated (как warm) или public sun/moon в sidebar? (Дефолт: dev-gated, как сейчас.)

**Релевантные файлы (абсолютные):**
- `C:/Users/elbics/Desktop/design-project/designs/gorod-fm.html` — главный (все якоря; re-grep перед edit, строки дрейфуют).
- `C:/Users/elbics/Desktop/design-project/designs/gorod-fm-standalone.html` — base64-inlined близнец (зеркалить токены/CSS/JS-ветки).
- `C:/Users/elbics/Desktop/design-project/docs/DESIGN_PROTOCOL.md` + `docs/references/anthropic_claude_design_prompt.md` — HOLY GRAIL doc-gate.
- `C:/Users/elbics/Desktop/design-project/docs/superpowers/HANDOFF-gorod-fm-cont-12.md` — cont-12 дисциплина (re-grep / `?v=N` / :8770).

---

# §8. Adversarial review (критик) — ОБЯЗАТЕЛЬНЫЕ правки поверх §2–§7

# VERDICT: REVISE (small, high-leverage fixes — not a rewrite)

This is a strong, genuinely build-ready spec. The grounding is real, not hallucinated: every landmine I spot-checked exists at the cited lines (`#111318` at L3069/3138/3171/3179, `color-mix(...,#111318)` L5588, `#191C24` L5624, 9× inline `#15171D` L8790–8917, wave `L.color==='#8094ff'` L12999, PNG hardcode L14122/14188, dead `cinema↔warm` toggle L11211, zero `[data-theme=]` selectors). The AA math is not vibes — I recomputed all of it and it lands to two decimals (`#5168FC`=4.24/4.43 fail, `#3A4ED0`=6.31 pass, `--text-sec` .60=5.67 pass, success `#0A7A53`=5.35, old `#34d399`=1.92 invisible). The single-accent discipline is preserved: the blue is split by *role*, not by introducing a second hue. The mechanism is a true `data-theme` var-swap, not a fork, and it correctly identifies that CSS can't reach the two JS canvases. It does NOT default to sterile flat-white — the warm-paper + blue-shadow + material thesis is a real differentiator. But there are 7 concrete problems, two of them genuine accessibility bugs the spec's own framing missed.

## Required fixes

1. **Focus-ring on the blue play-button is INVISIBLE (real a11y bug, unflagged).** The spec routes `:focus-visible` (L215, ~30 call-sites) to `--accent-on-dark → #3A4ED0`. But the resting play-fill is `--brand-blue-light #5168FC`. A `#3A4ED0` ring around a `#5168FC` fill = **1.49:1** — the keyboard-focus indicator on the single most important control vanishes (WCAG 2.4.11/1.4.11 fail). The dark theme dodges this because `#8094ff` on `#5168FC` is also low but the ring sits on the dark *page*, not the fill. **Fix:** give focus a two-tone ring — `outline: 2px solid #FFFFFF; box-shadow: 0 0 0 4px #3A4ED0;` (white inner against blue fill = 4.43:1, blue outer against paper = 6.31:1). The codebase already uses this exact double-ring pattern at L2360 (`0 0 0 4px var(--brand-blue-light)`), so it's a known idiom, not a new invention.

2. **Wave alpha lower-bound (0.7) fails; needs ≥0.8.** Spec says "alpha ↑ ~0.7–0.9." At `#3A4ED0 @ 0.7` on paper = **3.36:1**; at 0.8 = 4.18; at 0.9 = 5.15. The wave is a data-bearing wedge surface (the taste vector), not décor, so the lower-bound choice matters. **Fix:** pin the floor at **0.82**, not 0.7, and state the target ratio explicitly (≥4:1) so the implementer doesn't pick the cheap end.

3. **`--text-quat` is mis-stated AND should just be retired, not kept.** Spec maps `rgba(0,0,0,.55)` and annotates "~3.8:1" — actual is **4.74:1** (it passes AA). The error is harmless on safety but signals the one token that wasn't recomputed. More importantly: the dark `:root` comment already says quat is a "legacy alias (migrating to sec/ter)." Carrying a fourth opacity into the *new* theme entrenches dead debt. **Fix:** correct the number to 4.74, and explicitly map quat → `--text-sec` (.60) in light so the migration completes instead of forking the legacy alias into both themes.

4. **Redacted faux-bars at .18 are too faint to read as "data was here."** Spec proposes `rgba(0,0,0,.18)` on a `--surface-2 #F4F4F1` well = **1.52:1** vs the well — that's a whisper, and the whole point of the redacted competitor strip is that you can *see* there's withheld signal (the honesty wedge: "we have this, it's locked"). On dark the bars were `.22/.13` on near-black, which pop harder. **Fix:** bump the solid bar to `rgba(0,0,0,.26)` (≈1.9:1, matches the dark surface's perceived weight) and keep blur+lock-glyph as the primary "locked" cue. The spec's instinct (blur is the real cue) is right; the bar value is just too timid.

5. **O2 (button label on blue) is left as an open decision but it's an AA *fail*, not a taste call.** White 14–15px normal-weight label on `#5168FC` = **4.43:1 < 4.5** — that's a hard fail for any non-icon button with small text. Leaving it "open" risks shipping a fail. **Fix (decide it in the spec):** resting fill for *text* buttons = `--brand-blue-hover #3346C4` (white label = **7.46:1**), and reserve `#5168FC` for icon-only / ≥18.66px fills. This costs nothing (the hover token already exists) and removes the only fail in the blue system. Don't punt it.

6. **PNG share-card "stays dark" (O3) silently breaks the duplication promise.** The goal is "the WHOLE design duplicated in white via one switch." A recap that exports a dark card while the app is light is a visible seam, and it's the one surface a user *shares publicly*. The "dark card on white IG is intentional" rationale is plausible but it's a product decision dressed as a default. **Fix:** still recommend dark-default IF you want it, but the spec must ship the `drawCanvasPNG` theme-branch as *built* (bg `#FFFFFF`, text `#1A1C1F`, petals `#5168FC`, green `#0A7A53`, `html2canvas backgroundColor` swapped) so following-theme is a one-line flip, not future work. Half-built = the seam ships.

7. **No mention of `prefers-color-scheme`, and the persisted-theme default could strand light users in dark on first paint.** `applyTheme(lsGet(LS_KEYS.theme,'cinema'))` hard-defaults dark. If light ever goes public (O7), there's no OS-preference respect and a FOUC risk (paper flashes to dark or vice-versa before JS runs, since `html` bg-fallback is `--brand-black`). **Fix:** add a tiny inline pre-paint script in `<head>` that reads `localStorage` (or `matchMedia('(prefers-color-scheme: light)')` when no stored value) and sets `data-theme` before first paint — standard anti-FOUC. Note it even if toggle stays dev-gated for v1.

## 2–3 ideas to amplify (these are what push it past "good light mode" toward "or better than Apple")

- **Make the shadow tint *inherit the cover art*, subtly.** The spec's best move is the blue-black shadow (`rgb(20,22,40)`) — but Apple's white surfaces are famously *flat-shadowed* and generic. Drive the now-playing card / mini-player shadow tint from `--np-accent` at very low saturation (e.g. `color-mix(in oklab, var(--np-accent) 12%, rgb(20,22,40))`). The card the user is *listening to* casts a faintly warmer/cooler shadow than the rest — depth that *means something*, single-accent-clean, and impossible to get from a static palette. This is the "or better" differentiator and it survives theming because it's a token.

- **Tie the "whisper-grain" (Move-3) to the music, not the static base.** A 1–2% `feTurbulence` on paper is nice but inert. Anchor its `baseFrequency` or opacity to the wave's existing `ctxState` energy (already computed every frame for the taste vector). The paper "breathes" almost imperceptibly with playback — material that responds to the product's core verb. Gate it behind `prefers-reduced-motion` and keep it OFF text/cards (spec already says base-only — good).

- **Use the cover inset-ring (already specced for white-cover-on-white) as a system-wide "edge ink" primitive.** On dark, edges were free (lighter surface on dark base). On light you lose that, and the spec recovers it per-surface ad hoc. Promote `inset 0 0 0 1px rgba(0,0,0,.08)` to a token (`--edge-ink`) applied to every floating white card, so the whole white theme has a consistent hairline-of-ink at every surface boundary — this is precisely the detail that separates Apple's `systemGroupedBackground` from a flat-white SaaS dashboard, and it makes the warm-paper concept legible at the pixel edge.

**Net:** the depth/drama is recovered correctly (shadows + material carry what surface-lightness carried in dark — not lost to flatness), single-accent holds, the wedges survive honestly. Fix the focus-ring collision (#1) and the punted button-label fail (#5) — those are real and shippable-breaking — tighten the wave/bar values, finish the quat migration and the PNG branch, and this is SHIP. The spec is ~90% there; the missing 10% is two contrast collisions its own role-split framing happened to skip.