---
title: "SPEC-00 — Foundation & Integration (single-file build orchestrator)"
spec_id: SPEC-00-foundation-and-integration
date: 2026-06-02
surface: "designs/gorod-fm.html (ВСЕ экраны) — общие швы перед последовательной реализацией 7 экран-спеков"
role: "Первый документ цепочки. Сводит :root-токены, VALID_ROUTES/nav, cyan-retirement, anchor-коллизии. Реализуется ПЕРЕД любым экран-спеком."
status: build-ready
blueprint: docs/superpowers/BLUEPRINT-gorod-fm-full-service.md (§1 IA, §5 дизайн-система, §9 конфликты)
inputs:
  - SPEC-home.md (GOROD-045)
  - SPEC-taste_saved.md (taste «дом роста модели»)
  - SPEC-discover.md (GOROD-046b)
  - SPEC-track.md (GOROD-047a)
  - SPEC-artist.md (GOROD-047b)
  - SPEC-onboarding.md (GOROD-ONB)
  - SPEC-recap_profile.md (R1-R3/P1/W6)
---

# SPEC-00 — Foundation & Integration

> **Что это.** 7 экран-спеков пересверяли живой файл независимо. Каждый помечал «shared seams → Integrate». Этот документ — фаза Integrate, сведённая в один **build-order контракт**. Он (1) фиксирует единый набор новых :root-токенов (их почти нет — это хорошо), (2) сводит изменения VALID_ROUTES/nav, (3) даёт **план ретайра cyan** (1-строчный токен-свап + список ручных hardcoded-свапов, размеченных «умрёт при перестройке» vs «нужен ручной свап»), (4) разрешает anchor-коллизии (где ≥2 спека пишут в одну область), (5) задаёт BUILD ORDER.
>
> **Все числа пересверены Read/Grep живого `designs/gorod-fm.html` (≈14.1k строк) в этой сессии.** Ключевые факты: `VALID_ROUTES @10931`, `DEFAULT_ROUTE='#/map' @10932`, `--brand-cyan: rgb(56,140,180) @88`, `--player-accent: var(--brand-cyan) @122`, `--brand-blue-light:#5168FC @125`, `--accent-on-dark:#8094ff @128`, `--np-accent @127`, `--tint-blue-light-20 @126`, `--success:#34d399 @129`, `--r-base:10px @104`, `--r-pill:999px @106`, `--t-fast @142`, `--t-mid @143`. **Cyan-инвентарь: 119 вхождений (НЕ ~70 — см. §3), #0ea8e8: 3 (artist+favorites), #8b5cf6: 0.**

---

## 0. Executive summary (что реализатор должен знать за 30 сек)

1. **Новых :root-токенов почти нет.** Все 7 спеков сходятся на УЖЕ существующих токенах. Единственная foundation-правка токенов = **ретайр `--brand-cyan` в синюю семью** (1 строка @88) + явное переопределение `--player-accent` @122. Локальные per-instance vars (`--home-np`, `--track-tint`) — НЕ :root, объявляются в своих CSS-блоках.
2. **VALID_ROUTES: все 7 спеков НЕ трогают роутер.** Каждый явно отложил route-aliases в Integrate. Foundation добавляет **redirect-слой** `#/library`+`#/favorites`→`#/taste` (опц. `#/podborki`-alias) — НО только ПОСЛЕ постройки `#/taste`+saved (иначе redirect ведёт на полупустой экран).
3. **Cyan = настоящий блокер чистоты, НЕ блокер билда.** 119 вхождений. ~60% умрут сами при перестройке track/artist. Остальные — token-свап (var) + ручной список hardcoded.
4. **Anchor-коллизия №1 (КРИТИЧНО): хвост `</body>` @14142.** 4 спека (home, track, artist + taste_saved/onboarding/recap опираются на соседние) вставляют trailing-IIFE «после последнего модуля». Порядок вставки строго задан в §4.
5. **Anchor-коллизия №2: `window.openPlayer` мост.** home + artist оба полагаются на глобальный `openPlayer`. Мост ставится ОДИН раз в foundation.
6. **Anchor-коллизия №3: `gorodfm_rejected` REJ_LABELS канон.** track (`mood`) + artist (`art_arena`/`art_vocal_m`) дописывают новые reason-id. Канон расширяется ОДИН раз (W6 TwinrModel).

---

## 1. Foundation tokens (единый список — без дублей/конфликтов)

### 1.1 Новые :root-токены — ИХ НЕТ
Сведение `newTokens` всех 7 спеков:

| Спек | newTokens (заявлено) | Реальность |
|---|---|---|
| home | `--home-np` | **НЕ :root** — per-instance var на `.home-radio` (`--home-np: var(--np-accent)`). Локальный. |
| track | `--track-tint`, `.demo-tag` | `--track-tint` — **НЕ :root** (local var на `.track-cover`). `.demo-tag` — CSS-класс, не токен. |
| taste_saved | — | нет |
| discover | — | нет |
| artist | — | нет (использует `--np-accent` + локальный `tintFor` hsl) |
| onboarding | — | нет |
| recap_profile | — | нет (новые CSS-классы, «Новых :root-токенов НЕТ» явно) |

**Вывод:** дизайн-система уже полная. Foundation НЕ добавляет ни одного :root-токена. Это сильный сигнал консистентности — все 7 спеков честно живут на `--brand-blue-light`/`--accent-on-dark`/`--np-accent`/`--tint-blue-light-20`/`--success`/`--r-*`/`--t-*`.

### 1.2 Единственная foundation-правка токенов: ретайр cyan (см. §3)
`@88` и `@122` — переопределение `--brand-cyan` и `--player-accent`. Это и есть «foundation tokens» работа. Детали в §3.

### 1.3 Локальные (per-instance) vars — НЕ конфликтуют, реализуются в своих спеках
- `.home-radio { --home-np: var(--np-accent); }` (home §6)
- `.track-cover { --track-tint: var(--brand-blue-light); }` (track §6.2)
- artist `tintFor()` возвращает inline `hsl(215..255°)` (НЕ var, детерминир. от имени)
- taste_saved `tint()` возвращает inline `hsl(218..253°)` gradient (НЕ var)
Все четыре — изолированы scope'ом, имён не делят. ✅ No collision.

---

## 2. Routes / nav (сведение)

### 2.1 VALID_ROUTES — текущее (@10931, не менять в экран-спеках)
```js
const VALID_ROUTES = ['#/map', '#/home', '#/lives', '#/podborki', '#/library', '#/artist', '#/track', '#/favorites', '#/onboarding', '#/taste', '#/profile', '#/recap'];
const DEFAULT_ROUTE = '#/map';   // @10932
```

### 2.2 Сводная таблица route/nav-изменений (все отложены спеками → решаются ЗДЕСЬ)

| Изменение | Источник-спеки | Решение foundation | Когда применять |
|---|---|---|---|
| `#/library` → redirect `#/taste` | taste_saved §5.1, discover | **Применить в `routeFromHash` @10954** (redirect-map, не удаление из VALID_ROUTES — deep-link/carplay-boot-guard @11023/12183 цел) | **ПОСЛЕ** taste+saved построен (Integrate-A, см. §5) |
| `#/favorites` → redirect `#/taste` | taste_saved §5.1, discover, track (косвенно) | то же | то же |
| `#/podborki` → `#/discover` rename + alias | discover §C8 (явно отложил) | **НЕ делать в v1.** Карта работает на `#/podborki`. Rename = косметика, риск deep-link. Оставить `#/podborki`. | Отложено (post-build, опц.) |
| `#/map`, `#/lives` за флаг / `DEFAULT_ROUTE` cold-start | home §7 (явно отложил), onboarding (`gorodfm_onboarded` создаёт) | **Отдельная задача ВОЛНА-0.** onboarding ПИШЕТ `gorodfm_onboarded`, но cold-start-резолв (`DEFAULT_ROUTE` → `#/home`/`#/onboarding` по наличию `gorodfm_taste`+`gorodfm_onboarded`) = пост-build. | Отложено (ВОЛНА-0) |

### 2.3 Nav-изменения (3-tab + deep-dives)

Блюпринт целевой nav = 3 первичных: **Волна (`#/home`) · Мой вкус (`#/taste`) · Открыть (`#/podborki`)**; deep-dives (`#/track`, `#/artist`, `#/profile`, `#/recap`) = push/overlay из контента, НЕ в tabbar.

| Nav-правка | Источник | Решение | Когда |
|---|---|---|---|
| Retire tabbar-плитка «Медиа» (`data-route="#/library"` @10691) | taste_saved §5.2 | Применить (после redirect-слоя) | Integrate-A |
| Плитка «Избранное» @10704 (ведёт на `#/artist`, legacy-quirk) | taste_saved §5.2 | Перенацелить → `#/taste` (или убрать) | Integrate-A |
| promo/discover-карточки `href="#/library"` @7343, `href="#/favorites"` @7417/8354 | taste_saved §5.2 | Перенацелить → `#/taste` | Integrate-A |
| topbar-search @7148 (no-op стаб) → wire на `#/podborki`+focus | discover §C1 (D3 «дверь №1») | **Делает discover-спек сам** (в его scope, не foundation) | при build discover |
| home in-page toggle радио⇄плитки | home §C5 | **Делает home-спек сам** (gorodfm_home_view) | при build home |

> **Важно:** redirect-слой и nav-retire (Integrate-A) — это shared-seam код, который НЕ должен ставить ни один экран-спек в одиночку (иначе один экран глобально ломает nav до того, как цель построена). Foundation применяет их ОДНИМ проходом ПОСЛЕ `#/taste`.

---

## 3. CYAN-RETIREMENT PLAN (blueprint §5 «один акцент»)

**Инвентарь (Grep, пересверено): 119 вхождений `--brand-cyan` / `#56afd7` / `rgba(86,175,215)` / `rgb(56,140,180)`.** Дополнительно `#0ea8e8` ×3 (artist track @8420, artist album @8527, favorites thumb @9339). `#8b5cf6` = 0 (purple уже выведен — не вводить).

### 3.1 Шаг 1 — token-свап (1 строка чинит ВСЕ `var(--brand-cyan)`)

`@88`:
```css
/* было */ --brand-cyan: rgb(56, 140, 180);
/* стало */ --brand-cyan: #5168FC;   /* RETIRED → blue family (= --brand-blue-light). Legacy alias kept so var(--brand-cyan) refs resolve to blue. */
```
`@122` (chains через cyan — переопределить явно в синюю семью):
```css
/* было */ --player-accent: var(--brand-cyan);
/* стало */ --player-accent: var(--brand-blue-light);
```
Это мгновенно переводит **все `var(--brand-cyan)` вхождения** (≈58 из 119) в синий, на ЛЮБОМ экране, включая те, что не перестраиваются (map, lives, generic CSS, library, favorites). Токен `--brand-cyan` оставляем определённым (как alias) — чтобы не плодить 58 правок и не ловить undefined-var.

> Альтернатива (чище, но дороже): переименовать все `var(--brand-cyan)`→`var(--brand-blue-light)` и удалить токен. **НЕ делаем в foundation** — alias-свап безопаснее и атомарнее. Полное переименование = опц. follow-up.

### 3.2 Шаг 2 — hardcoded cyan (НЕ ловится token-свапом): классификация по экранам

`#56afd7` / `rgba(86,175,215)` / `#0ea8e8` — литералы, токен-свап их НЕ трогает. Классификация «умрёт при перестройке» (ребилд-спек удалит узел/правило) vs «нужен ручной свап» (на экране, который НЕ перестраивается):

**A. УМРУТ ПРИ ПЕРЕСТРОЙКЕ — НЕ трогать руками (ребилд-спек удалит):**
| Строки (hardcoded cyan) | Экран | Кто перестраивает |
|---|---|---|
| 5181,5182,5281,5282,5405,5423,5591,5749,5758 (+ `var` 5186,5283,5325,5337,5391,5562,5592,5762,5840,5106,5225) | track CSS (5363–5887 + смежн.) | **SPEC-track §6** (REPLACE in-place) |
| 8844, 9047, 9104, 9152 | track DOM (8646–9182) | **SPEC-track §3** (REPLACE) |
| 4172,4173,4240,4241,4249,4305,4306,4336,4351,4489,4495 (+ `var` 4177,4215,4219,4312,4346,4433,4519,4577,4595,4630,4635,4640,4661,4674,4726,4827,4905,4913) | artist CSS (4462–4934) | **SPEC-artist §5** (REPLACE) |
| 8242,8244,8245,8247,8298, 8372, 8499, 8527(#0ea8e8), 8420(#0ea8e8) | artist DOM (8281–8642) | **SPEC-artist §3** (REPLACE) |

> Примечание: 4172–4351 захватывают `.discover-near-card`/смежные generic-правила, которые физически ВЫШЕ artist-CSS-блока (4462). Перепроверить при реализации: если строка <4462 — она НЕ в artist-replace-диапазоне → переходит в категорию B (ручной свап). Grep показал кластер 4172–4351 — это generic discover/near CSS, **частично вне artist scope** → пометить для ручной проверки (см. §6 open-risk).

**B. ВЫЖИВУТ — нужен ручной свап (экраны НЕ перестраиваются этой цепочкой):**
| Строки | Контекст | Действие |
|---|---|---|
| 606 (#56afd7) | player CSS (`.player-*`) | ручной свап → `var(--brand-blue-light)` / `rgba(81,104,252,…)` |
| 1226 (`var`), 1466,1468,1544,1550,1638,1648,1659 | home tile / featured / halo CSS (Figma 2174:422 wrapper) | token-свап чинит `var`; hardcoded 1550 (rgba 86,175,215) → ручной свап. **ОСТОРОЖНО: внутри Figma 2174:422 pixel-perfect зоны** — home-спек оборачивает её в `.home-tiles[hidden]`, НЕ редактирует. Свап цвета меняет вид плиток. **Решение: отложить до post-home; плитки скрыты по умолчанию (gorodfm_home_view='radio'), cyan там не виден на дефолте.** |
| 3201,3216,3222,3312,3314,3319,3333,3392,3440,3550,3596,3683,3703–3715 | generic CSS (legacy `.home-hero`/`.home-stations`/`.discover-near`/podborki) | token-свап чинит `var`; hardcoded `#56afd7`/`rgba(86,175,215)` (3216,3222,3314,3440,3596,3704,3705,3714) → ручной свап ИЛИ умрут если discover-спек/IA-046 ретайрит legacy podborki-плитки (discover §C4 оставляет legacy chip-row — НЕ умрут в v1) |
| 3899,4008,4095 (`var`) | generic | token-свап чинит |
| 6081,6182 (`var`) | responsive generic | token-свап чинит |
| 7298,7323,7351,7376,7428,7469 (rgba 86,175,215) | home promo/discover cards DOM (`data-page="home"` зона выше .home-stage) | **ручной свап** — это видимые карточки на home. НЕ в Figma 2174:422 (отдельные promo). home-спек их не трогает (вставляет .home-radio выше). → ручной свап в Integrate-B. |
| 7962, 8046, 8047, 8125(#56afd7), 8128, 8179(#56afd7), 8182 | library DOM (7911–9240) | library редиректится (§2.2), физически остаётся в DOM но скрыт из nav → cyan не виден. **Отложить** (умрёт если IA-чистка удалит DOM; иначе невидим). |
| 9047,9104,9152,9291(#56afd7),9339(#0ea8e8) | favorites DOM (9241+) | favorites редиректится → cyan невидим. **Отложить.** ⚠️ 9047/9104/9152 ВНУТРИ track-диапазона по номеру — перепроверить: если 9047>9182 это favorites, если <9182 это track. Grep-кластер 9047–9152 пограничный → §6 open-risk. |
| 10345 (#56afd7) | JS/inline (router/legacy) | ручной свап или dead → проверить контекст |
| 11508 (#56afd7) | JS `setActiveStation` (мёртвый код, home §1.2 п.8) | dead-code → удалить с legacy-блоком или игнор |

### 3.3 Итог cyan-плана
1. **Foundation (этот спек, шаг 1):** свап @88 + @122 → ~58 `var(--brand-cyan)` мгновенно синие. **Делать ПЕРВЫМ.**
2. **Авто-смерть:** ~40 hardcoded в track/artist → исчезнут при build track/artist (НЕ трогать руками).
3. **Integrate-B (ручной свап, ПОСЛЕ всех экранов):** ~15 выживших hardcoded на home-promo (7298–7469), player (606), generic legacy (3216–3714). Список выше.
4. **Отложено (невидимы):** library/favorites cyan (редирект скрывает), Figma-плитки cyan (toggle скрывает), dead-code 11508.

**HARD GATE финал:** после всех фаз — Grep `#56afd7|rgba(86,175,215)|#0ea8e8` должен вернуть 0 на ВИДИМЫХ-по-дефолту поверхностях (home-radio, taste, podborki, track, artist, recap, profile, onboarding). Скрытые legacy (library/favorites/Figma-tiles) — допустимый долг до IA-чистки.

---

## 4. ANCHOR-COLLISIONS + resolutions

### 4.1 КОЛЛИЗИЯ №1 (критичная) — trailing `<script>` хвост перед `</body>` @14142
**Кто пишет сюда:**
- home: `window.GorodHomeRadio` «после 14118 / после последнего модуля»
- track: `window.GorodTrack` «после 14140, перед </body> 14142»
- artist: `window.GorodArtist` «после 14140»
- onboarding: правки ВНУТРИ GorodOnboarding IIFE (НЕ хвост) — не коллизирует, но опирается на стабильные номера
- taste_saved: `GorodSaved` «после GorodContext `})();`» (≈14138)
- recap_profile: `window.TwinrModel` IIFE «ПЕРЕД @13660» (НЕ хвост — перед GOROD-052)

**Проблема:** каждый спек ссылается на «14118 / 14138 / 14140 / 14142» как на «конец последнего модуля». Но КАЖДАЯ вставка нового trailing-IIFE СДВИГАЕТ эти номера для следующего спека. Якоря по абсолютным строкам станут невалидны после первой же вставки.

**Резолюция (binding):**
1. **Не доверять абсолютным номерам хвоста.** При вставке любого trailing-IIFE — якорить по УНИКАЛЬНОЙ строке `})();` закрывающего `<script>` ПОСЛЕДНЕГО существующего модуля + `</body>`. Grep `</body>` непосредственно перед вставкой.
2. **Фиксированный порядок вставки trailing-модулей** (каждый следующий ищет реальный текущий хвост):
   - (foundation) `window.TwinrModel` — вставить ПЕРЕД GOROD-052 (@~13660, якорь = коммент `<!-- ---- GOROD-052`). **ПЕРВЫМ.**
   - GorodHomeRadio → GorodSaved → GorodTrack → GorodArtist — каждый перед `</body>`, в порядке build-order (§5).
3. **Перед КАЖДОЙ trailing-вставкой:** Read последние ~30 строк файла, найди реальную позицию `</body>`, вставь перед ней. Номера в экран-спеках (14118/14140) считать ОРИЕНТИРОМ, не истиной.

### 4.2 КОЛЛИЗИЯ №2 — `window.openPlayer` мост
**Кто полагается:** home (§5 hero-тап `window.openPlayer()`, §9 шаг 6 «добавить `window.openPlayer = openPlayer;`»), artist (§6 `typeof openPlayer==='function'` guard).
**Проблема:** `openPlayer()` объявлена в главном router-IIFE (@11041), НЕ глобальна. home хочет мост; artist хочет guard+fallback.
**Резолюция (binding):** Foundation ставит мост **ОДИН раз**: в главном IIFE сразу после `function openPlayer() {…}` (@~11041) добавить `window.openPlayer = openPlayer;`. Тогда home-hero работает, artist-guard срабатывает (`typeof window.openPlayer==='function'`). Один мост обслуживает оба. **Делать в foundation** (до home/artist build). Grep подтвердил `openPlayer` сейчас local-only (0 `window.openPlayer`).

### 4.3 КОЛЛИЗИЯ №3 — `gorodfm_rejected` REJ_LABELS канон
**Кто пишет новые reason-id:** track (`mood`), artist (`art_arena`, `art_vocal_m`).
**Кто читает канон:** GorodTaste @13131, GorodProfile @13670, GorodRecap @13767 (после W6 — все через `window.TwinrModel.REJ_LABELS`).
**Проблема:** новые id пишутся в общий массив, но без лейбла в каноне рендерятся как unknown (graceful matched:false — НЕ падает, но reject не виден человеко-понятно на Profile/Recap).
**Резолюция (binding):** W6 (recap_profile) вводит `window.TwinrModel` с единым `REJ_LABELS`. **Foundation/W6 расширяет канон ОДИН раз:**
```js
var REJ_LABELS = {
  artist: 'Егор Крид', vocal: 'Тёплый поп-вокал', tempo: 'Темп ~95 BPM',  // existing
  mood: 'Настроение «спокойно»',                                          // + track (047a)
  art_arena: 'Арена-рок', art_vocal_m: 'Мужской вокал'                    // + artist (047b)
};
```
Тогда track/artist reject отражается на Profile/Recap сразу. **Делать в W6-шаге** (TwinrModel определяется там). track/artist build идёт ПОСЛЕ W6 → канон уже расширен.

### 4.4 КОЛЛИЗИЯ №4 — `--np-accent` read-coupling (NowPlayingTint)
**Кто читает:** home (расширяет `NowPlayingTint.paintHero()` @13398–13432 + читает `--np-accent`), track (read-only `getComputedStyle --np-accent`), artist (hero `background:var(--np-accent)` + JS `tintFor` override).
**Проблема:** home РЕДАКТИРУЕТ модуль NowPlayingTint (добавляет paintHero); track/artist только ЧИТАЮТ `--np-accent`.
**Резолюция:** home — единственный, кто правит NowPlayingTint (аддитивно, paintHero null-guarded). track/artist read-only — не конфликтуют. **Порядок: home раньше track/artist** (build-order §5 уже это даёт). После home `--np-accent` остаётся семантически тем же → track/artist читают как раньше. ✅

### 4.5 КОЛЛИЗИЯ №5 — `.demo-tag` класс (track) vs demo-маркеры (discover/artist/taste/onboarding)
**Кто вводит `.demo-tag`:** track §6.3 (полноценный CSS-класс).
**Кто вводит свои demo-классы:** discover `.discover-demo-tag`, artist `.artist-why-demo`, taste `.taste-saved-demo`/`.taste-streak-demo`, onboarding inline.
**Проблема:** дубль семантики (демо-маркер) под разными именами.
**Резолюция (не блокер):** оставить как есть в v1 (каждый scope'нут под свой экран, имена разные → no CSS-collision). **Opt follow-up:** свести в один `.demo-tag` (track-версия — кандидат-канон). НЕ обязательно для build.

### 4.6 НЕ коллизирует (проверено)
- `gorodfm_liked` (home) — новый изолированный ключ, никто не делит.
- `gorodfm_home_view` (home) — изолирован.
- `gorodfm_onboarded` (onboarding) — изолирован, потребитель = будущий W0.
- `#home-wave` (home) vs `#taste-wave` (built) vs `#discover-map` (discover) — три РАЗНЫХ canvas-id на трёх разных экранах. Home-wave = свой RAF; discover-map = без RAF; taste-wave = built RAF. Изолированы.
- `initArtist` @11958–12060 → artist-спек заменяет на stub В ТОМ ЖЕ диапазоне (не сдвигает соседние initFavorites@12064). ✅

---

## 5. BUILD ORDER (для main loop — последовательная реализация)

> Принцип: **foundation первым** (токены+cyan-token-swap+openPlayer-мост+redirect-слой ОТЛОЖЕН до после-taste). Затем экраны по зависимости: shared-model (W6) → home → taste+saved → discover → track → artist → onboarding → recap-finish. cyan-ручной-свап + nav-retire ПОСЛЕДНИМИ (когда цели существуют).

### Фаза 0 — FOUNDATION (этот спек)
- [ ] **F1. Cyan token-swap** @88 (`--brand-cyan:#5168FC`) + @122 (`--player-accent:var(--brand-blue-light)`). effort: trivial. Не ломает (alias). **Pixel-perfect:** меняет цвет акцента в плеере/legacy на синий — это и есть «один акцент», ожидаемо.
- [ ] **F2. `window.openPlayer` мост** @~11041 (`window.openPlayer = openPlayer;`). effort: trivial. Грунт перед home/artist.
- [ ] (W6 TwinrModel идёт в Фазе 1 вместе с recap-зависимостью, т.к. это shared-model для recap/profile/taste — но определяется ДО потребителей. См. ниже.)

### Фаза 1 — SHARED MODEL (recap_profile W6, БЕЗ R1-R3/P1 пока)
- [ ] **B1. `window.TwinrModel` IIFE** перед GOROD-052 @~13660 + расширенный REJ_LABELS-канон (§4.3: +mood +art_arena +art_vocal_m). + переключить GorodProfile/GorodRecap/GorodTaste REJ-часть на делегацию (W6-b/c/d). effort: med (рефактор-без-смены-поведения, byte-identical verify). depends: foundation. breaksPixelPerfect: **false**. **Делать рано** — track/artist/recap зависят от канона.

### Фаза 2 — ЭКРАНЫ (по риску/зависимости)

Build-list (упорядоченный):

1. **home (GOROD-045)** — effort: **high** — depends: foundation (F2 openPlayer-мост; F1 cyan). **breaksPixelPerfect: TRUE (авторизовано)** — дефолт home меняется на радио; Figma 2174:422 сохранён в `.home-tiles[hidden]`, откат = 1 LS-строка `gorodfm_home_view='tiles'`. Самый рискованный (новый canvas+RAF, MutationObserver на плеер, мост). Делать первым из экранов чтобы рано поймать regressions.
2. **taste+saved** — effort: **med** — depends: B1 (TwinrModel REJ для EDIT-4 не строго, но канон полезен). breaksPixelPerfect: false. Аддитивно (3 блока + 1 micro-edit GorodTaste render). Строить ДО redirect-слоя (redirect ведёт сюда → цель должна существовать).
3. **discover (GOROD-046b)** — effort: **med** — depends: foundation. breaksPixelPerfect: false. Расширяет GorodDiscover IIFE + wire topbar-search (nav-affordance). Не зависит от home/taste. Carta без RAF (perf).
4. **track (GOROD-047a)** — effort: **med** — depends: B1 (mood в REJ_LABELS-каноне), foundation (F1 cyan auto-die в track CSS). breaksPixelPerfect: false. REPLACE-in-place 4 узла + GorodTrack IIFE. Убивает ~13 hardcoded cyan.
5. **artist (GOROD-047b)** — effort: **high** — depends: B1 (art_arena/art_vocal_m канон), foundation, F2 (openPlayer guard). breaksPixelPerfect: false. REPLACE 3 диапазона (CSS 4462–4934 + 6764–6878, DOM 8281–8642) + initArtist→stub + GorodArtist IIFE. Самый большой diff. Убивает ~25 hardcoded cyan. **Применять диапазоны строго сверху-вниз.**
6. **onboarding (GOROD-ONB)** — effort: **med** — depends: foundation (нет cyan/route deps). breaksPixelPerfect: false. AUGMENT внутри GorodOnboarding IIFE (Model+Import под-модули) + overlay + footer-кнопка. Создаёт `gorodfm_onboarded`.
7. **recap+profile finish (R1/R2/R3/P1)** — effort: **low** — depends: B1 (TwinrModel уже стоит). breaksPixelPerfect: false. Дельта-герой reorder + honest PNG Canvas-2D + micro-CTA + reject-провенанс. Самый лёгкий (всё аддитивно поверх built).

### Фаза 3 — INTEGRATE-A (route/nav, ПОСЛЕ taste построен)
- [ ] **I-A1. redirect-слой** в `routeFromHash` @10954: `#/library`/`#/favorites` → return `#/taste`. effort: low. depends: taste+saved (#2).
- [ ] **I-A2. nav-retire:** убрать tabbar «Медиа» @10691; перенацелить «Избранное» @10704 + promo-карточки @7343/7417/8354 на `#/taste`. effort: low. depends: I-A1.

### Фаза 4 — INTEGRATE-B (cyan ручной свап, ПОСЛЕДНИМ)
- [ ] **I-B1. Ручной hardcoded-cyan свап** на выживших видимых: home-promo 7298–7469, player 606, generic legacy 3216–3714 (см. §3.2-B). effort: low-med. depends: все экраны (чтобы не свапать то, что уже умерло). Grep-verify финал.

### Фаза 5 — ОТЛОЖЕНО (post-build, не в этой цепочке)
- DEFAULT_ROUTE cold-start (ВОЛНА-0): `#/map` → resolve `#/onboarding`/`#/home` по `gorodfm_taste`+`gorodfm_onboarded`. depends: onboarding (#6).
- `#/podborki`→`#/discover` rename + alias (косметика).
- library/favorites DOM физическое удаление (после redirect стабилен).
- `.demo-tag` унификация (§4.5).
- Полное переименование `var(--brand-cyan)`→`var(--brand-blue-light)` + удаление токена.

---

## 6. Open risks / blockers

**BLOCKERS (требуют решения до/во время build):**
- **BR-1 (anchor-drift, КРИТИЧНО):** trailing-IIFE абсолютные номера (14118/14138/14140/14142) НЕВАЛИДНЫ после первой вставки. **Mitigation §4.1: якорить по `</body>` + уникальной `})();`, Read хвост перед каждой вставкой.** Это не блокирует build, но требует дисциплины — НЕ применять trailing-вставки по числам вслепую.
- **BR-2 (cyan-кластеры пограничные):** строки 4172–4351 (artist vs generic-discover boundary @4462) и 9047–9152 (track vs favorites boundary @9182). **Перед удалением — Read контекст этих строк, подтвердить какой селектор/экран.** Если вне rebuild-диапазона → ручной свап (Integrate-B), не «умрёт сам». Риск: реализатор посчитает их «умрут» и оставит cyan.

**RISKS (известны, mitigated):**
- **RK-1 home breaksPixelPerfect:** авторизовано (045). Откат = `gorodfm_home_view='tiles'`. Подтвердить с Эльбиком, что делегирование context-card → #/taste (смена контекста только на taste) = принятый UX (home §C1/риск-флаг).
- **RK-2 W6 byte-identical:** дедуп ОБЯЗАН не менять вывод facets(). Verify: Profile/Recap/Taste рендерятся идентично до/после на одинаковом localStorage. Если разойдётся — дедуп сам станет fidelity-багом.
- **RK-3 redirect timing:** если I-A1 применить ДО taste-build → `#/library` ведёт на полупустой `#/taste`. **Mitigation: redirect строго в Фазе 3 (после #2).**
- **RK-4 onboarding RISK-1:** `onContinue` @12712 перехват — реальный #/home-handoff ОБЯЗАН переехать в `goHome()`, иначе онбординг зависает на overlay. Высокий impact, mitigated в спеке.
- **RK-5 track view-state rename `cover`→`why`:** persisted `LS trackView='cover'` у вернувшегося юзера → setTrackView отвергнет невалид, дефолт через CSS. Verify при track-build.
- **RK-6 MutationObserver coupling (home):** home paintWhy слушает `#player-track-reason` структуру. Если будущий спек реструктурирует узел — mirror тихо устаревает (guarded, no error).
- **RK-7 demo-маркеры (fidelity HARD):** discover/track/artist/taste/onboarding — захардкоженные демо-данные держатся ТОЛЬКО видимым лейблом «демо-X». Реализатор НЕ снимает лейбл (perceived-transparency = смерть доверия, blueprint §8).
- **RK-8 Figma-tiles cyan (1466–1659,1550):** внутри pixel-perfect зоны. НЕ свапать (меняет вид плиток); скрыт toggle'ом → невидим на дефолте. Долг до IA-чистки.

**NON-BLOCKERS (подтверждено безопасно):**
- Новых :root-токенов нет → нет конфликта значений.
- VALID_ROUTES не трогается ни одним экран-спеком → нет race.
- Все LS-ключи изолированы (liked/home_view/onboarded/saved-нет-своего/track-нет-своего).
- 3 разных canvas-id, 0 пересечений RAF.
