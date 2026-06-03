# HANDOFF — Город ФМ · cont-13 (2026-06-03) — Discover taste-cloud, carousel polish, popular bubbles, genre photos

> READ-FIRST. Self-contained. Все коммиты ЛОКАЛЬНЫ на `master`, **PUSH ДЕРЖИТСЯ до явного `sync`**.
> File: `designs/gorod-fm.html` (~15.2k строк, single-file SPA). Server :8770 serves from `designs/`.
> Disc: re-grep anchors (дрейфуют); `?v=N` cache-bust; чистить `gorodfm_*` LS-ключи после probe.

## HEAD = `933187d`. Коммиты cont-13 (поверх cont-12 `bd55c6d`):
1. `e236265` — **Discover taste-cloud** в Медиатеке (#/podborki). Форк `GorodTasteCloud` + `window.GorodTasteSeed` (копия онбординг-сида; онбординг IIFE НЕ тронут). Genres+8 артист-фото, tap=select+bloom+пишет РЕАЛЬНЫЙ `gorodfm_taste` (UNCAPPED+verbatim merge, сохраняет non-cloud entries — data-loss-safe), счётчик «Твоя модель за N сигналов». Заменил старый genre-ФИЛЬТР (`activeGenre` удалён). Cross-surface event `gorodfm-taste-changed` синкает cloud↔grid.
2. `6aa5be9` — **Карусель**: Apple-Music edge-fades + circular arrows (`.shelf-viewport`, 3 шелфа) + **фикс выравнивания тайлов** (`.shelf-row{align-items:flex-start}` — `<button>` центрировал контент → тайлы съезжали на 8px). Стрелка `scrollBy({behavior:'smooth'})` + instant fallback.
3. `e795346` — **«ПОПУЛЯРНО СЕЙЧАС»** (6: ЭЛЕКТРО/ХИП-ХОП/ПОП/Егор Крид/Макс Корж/Linkin Park, `pop:true`, seeded first) hue-free ▲ trend-chip + eyebrow + **anti-clog «graduate-out»** (tap→bloom→~800ms→fade off-canvas, вкус persists) + MAX 24→16 + ensureRoom skip-popular + «Обновить подборку» reshuffle + счётчик «N в твоём вкусе →» роутит на #/taste. **Флаг `GRADUATE=true`** (легко выключить, чтобы пики ОСТАВАЛИСЬ на canvas).
4. `933187d` — **Реальные фото ВСЕМ genre-шарикам** (онбординг + cloud). 12 Unsplash-фото (free license, verified), wired через `img` в обоих сидах + фикс `makeBubble` genre-derivation `(d.img?null:d.t)→d.t` (genre-root с фото резолвит свой POOL). `genre-credits.json`. Группы/артисты уже на real-assets (репо).

**ВСЁ verified Chrome (:8770, 0 console errors).** 🔴 ЛАГ ИСПРАВЛЕН (оператор подтвердил): `focusin→stop()` гейт останавливал rAF при тапе (клик фокусит кнопку) → соседи не реагировали; убрал focus-pause + per-bubble focus-freeze, вернул онбординг-физику (DAMP .965/VCLAMP 2.6/BOUNCE -.55). Эти лаг-фиксы — **прямые Edit'ы в `gorod-fm.html`, НЕ в `.scratch/build_tcloud.py`** (скрипт СТАЛЫЙ — перезапуск вернёт лаг!).

---

## 🔴 НЕ ДОДЕЛАНО / NEXT SESSION (порядок)

### A. **B: #/taste weight-cloud** (НЕ построен; spec ГОТОВ)
`docs/superpowers/SPEC-gorod-fm-taste-weight-cloud.md` (verdict=**revise**). Концепт: «steppy-resize» — размер пузыря = вес интереса, −/+ stepper (5 нотчей), `role=slider`, диаметр ∝ √weight (area-honest). **ЧИНИТ РЕАЛЬНЫЙ БАГ:** текущий −/+ редактор не persist'ит веса (пересобирает из pick-order `90−i*3` каждый load) → ввести `gorodfm_weights` store. **Критик-blocking фиксы (применить при билде):**
- `window.TwinrModel.hasRealSignal()` берёт **0 аргументов** (глобальный bool readPicks||readRej), НЕ per-facet. Спека зовёт `hasRealSignal(r.n)` → пометит ВСЕ demo-грани как 'heard' (ложь). Per-facet real-signal источника НЕТ → 'heard' нельзя честно повесить.
- `updateVectorSr` (L~13070) печатает `r.n+' '+r.w+'%'` для demo-граней → SR озвучивает фейк-%, пока cloud их прячет. Синхронизировать SR/visual честность.
- `GorodTaste` НЕТ `selfDispatch`-гарда (в отличие от GorodTasteCloud) → `persistWeight`→dispatch→свой listener→re-seed/render loop + потеря фокуса. Добавить гард.
- `#taste-delta` (L~9434) живёт в `.taste-hero`, его же пишет `wireSponsor` (sponsor-dismiss) → не затирать друг друга.

### B. **Standalone mirror** (`gorod-fm-standalone.html`)
Сейчас там ТОЛЬКО cont-12 Fix #1. **ВЕСЬ cont-13 (taste-cloud, carousel fade/arrow+align, popular, genre-фото) НЕ зеркалён.** Нужно: (1) ⚠️ build_tcloud.py СТАЛЫЙ (без лаг-фиксов) — НЕ перезапускать как есть; скопировать `GorodTasteCloud` IIFE + CSS + seed из dev-файла; (2) base64-инлайн 12 `genre-*.jpg` (standalone embeds covers inline); (3) перенести carousel/popular правки. `.scratch/rebuild_standalone_full.py` — прежний rebuilder (обновить под cont-13).

### C. Backlog cont-12 (не тронут): #/artist enrich (real hero/tracks/lyrics), «Сохранённое» группировка DJ/Группы/Артисты, ЛК account-sheet (`BLUEPRINT-gorod-fm-sections-integration.md`), **light theme** (`SPEC-gorod-fm-light-theme.md` готов), sections-integration.

### D. **PUSH** всё при `sync` (≥6 коммитов cont-13 локально).

---

## 🟡 Решения за Эльбиком
- **graduate-out** (F): пики ИСЧЕЗАЮТ с canvas после тапа (улетают в #/taste). Если хочешь чтобы ОСТАВАЛИСЬ видимыми — `GRADUATE=false` (1 строка в GorodTasteCloud). Спросить/показать.
- Genre-фото: взяты из интернета (Unsplash) т.к. в Figma-файле только cover-картинка 540×320, genre-кадров нет. Если найдётся Figma с genre-имиджери — заменить.
- GOROD-029 онбординг-eyebrow «ПЕРВЫЙ AI» (позиционирование) · GOROD-030 лицензии.

## Артефакты cont-13
- Specs: `SPEC-gorod-fm-discover-taste-cloud.md`, `SPEC-gorod-fm-cloud-popular-and-scale.md`, `SPEC-gorod-fm-taste-weight-cloud.md` (все verdict-проверены критиком).
- Build-скрипты (`.scratch/`, gitignored): `build_tcloud.py` (⚠️стал.), `build_popular.py`, `build_genre_photos.py`.
- `designs/assets/gorod-fm/genre-*.jpg` (12) + `genre-credits.json`.
- Workflows (5 спек-воркфлоу прогнаны: discover/popular/taste; taste 2× флакнул на StructuredOutput → убрал schema у research/ground агентов → прошёл).
