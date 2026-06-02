# HANDOFF — Город ФМ · cont-10 (2026-06-02) — BUILD 11/11 + Apple-polish pass

> **READ-FIRST для следующей сессии.** Самодостаточный. Подробный backlog — в `AUDIT-apple-polish-plan.md`.
> Файл: `designs/gorod-fm.html` (~14.75k строк, single-file SPA). Standalone: `designs/gorod-fm-standalone.html` (2.55 MB).
> Ветка `master`, **26 коммитов впереди origin, PUSH ОТЛОЖЕН** → запушить по команде `sync`.

## Состояние: ЗАВЕРШЕНО в этой сессии
1. **FULL-DESIGN BUILD 11/11** (было 6/11): artist `8607e9a` · onboarding `ac4e053` · recap+profile `e15612f` · Integrate-A `807f235` · Integrate-B `59689be`.
2. **Apple-polish pass** — обе претензии Эльбика закрыты:
   - **Плеер «страшно» → исправлен** (`cec1679`, `08b2cf1`): убрана warm-тема (оранжевый «мир»), плоская обложка вместо purple→magenta gradient, inset-окно, синий скраббер, solid-blue play, нет наложений.
   - **TWEAKS-артефакт → убран** (`55709ac`): dev-панель/theme-toggle/internal-#/map скрыты в проде; дефолт → `#/home`. Reveal: `?dev=1` / `?dev=0` / `Ctrl|Cmd+Shift+D`.
   - Per-surface P0: `8344ab1` (nav rail, onboarding flat bubbles, artist avatar/name) · `1004f0e` (profile glow, home halo, CTA) · `cabe496` (taste emoji, discover cards).
   - Standalone пересобран `77db4d0`.

## Как запустить / проверить
```bash
# dev-сервер (если не жив):
cd designs && python -m http.server 8770
```
- Прод-вид: `http://127.0.0.1:8770/gorod-fm.html` (откроется на «Волна», без TWEAKS).
- Dev-вид (TWEAKS + «Карта флоу» + темы): `…/gorod-fm.html?v=1&dev=1`.
- Проверка JS (все inline `<script>` через `node --check`): `python .scratch/check_scripts_v2.py` → «0 failures».
- Визуал: Chrome MCP, `?v=N` cache-bust обязателен (dev-сервер кеширует).

## Ключевые артефакты
- `docs/superpowers/AUDIT-apple-polish-plan.md` — **главный план полиша** (Apple дизайн-система §0 + per-surface P0/P1/P2 §2 + порядок исполнения §3). 17-агентный аудит.
- `docs/superpowers/specs/SPEC-*.md` — 7 build-спеков экранов + SPEC-00 orchestrator (build завершён по ним).
- `docs/RESUME_PROMPT.md` cont-10 — выводы сессии.

## REMAINING (backlog — продолжать по `AUDIT-apple-polish-plan.md` §3)
Порядок: G6 → G7 → per-surface P0-остаток → P1 → P2.
- **G6 slop-sweep:** mini-art placeholders (`.player-mini-art-placeholder--1/2/3` ~L619-621 gradient), остаточные gradient-covers (home saved-rows, track-history, queue-covers), map thumbs.
- **G7 global pass:** focus-visible → `--accent-on-dark` везде; `:active{scale(.98)}`; hit-targets ≥44px.
- **Per-surface P1/P2:** discover (map axis-labels/nodes, секц-заголовки) · track (lyrics #545454→.32 контраст, hero-cover cap 360, eyebrow) · taste (радиусы→§0, 2 синих CTA → 1 primary, saved-rows реальные/убрать) · recap+profile (token-migration сырых hex/radii, кол-во колонок) · **map/lives под dev-gate уже скрыты**, но если разгейтить — #/lives dead cards (нет хендлера) + хардкод `#ff3b30` red.
- **DEFAULT_ROUTE cold-start → #/onboarding** (ВОЛНА-0): сейчас прод-гейт шлёт на `#/home`; нужно: нет `gorodfm_taste` И нет `gorodfm_onboarded` → `#/onboarding`.
- **G2 финал:** 42 latent `var(--brand-cyan)` (рендерят синим) → полный rename `--brand-blue-light`, удалить алиас-токен.
- **Эльбик-gate (НЕ Claude):** GOROD-029 позиционирование (бейдж «первый AI-стриминг» уже неправда — Spotify AI DJ) · GOROD-030 лицензии.

## Дисциплина / learnings (важно для следующей сессии)
- **Anchor-drift:** номера строк в спеках/плане ДРЕЙФУЮТ (файл рос 14.1k→14.75k). ВСЕГДА re-grep живой файл перед edit. Паттерн который сработал: python-splice с `assert count==1` (абортит без записи) — `.scratch/apply_*.py`.
- **Демо-лейблы СОХРАНЕНЫ намеренно** («демо-вектор/демо-карта/демо-архив») — north-star (не выдавать демо за реальное) > visual-declutter. Аудит флагнул P0 на удаление — НЕ удалять.
- **Single accent:** hardcoded cyan = 0; warm-тема удалена. Любой новый цвет вне синей семьи (+ green только для роста) = регрессия.
- **Дизайн-токены §0** уже в `:root` — НОВЫЕ компоненты должны жить на `--fs-*`/`--s*`/`--r-xl/lg/md/sm`/`--surface-*`/`--sh-*`/`--d-*`, не на сырых значениях.
- LS-ключи чистить после probe: `gorodfm_*` + `gorod-fm.*`.
- `.scratch/*.py` — gitignored (apply-скрипты + check_scripts_v2.py).

## START следующей сессии
1. `cd ~/Desktop/design-project`, dev-сервер :8770.
2. Прочитать этот HANDOFF + `AUDIT-apple-polish-plan.md` §2/§3.
3. Продолжить полиш с G6 (или по запросу Эльбика). Каждый шаг: re-grep якоря → edit → `node --check` → Chrome `?v=N` → атомар-коммит.
4. PUSH — только по `sync`.
