# Resume Design — Активация сессии

## ⚡ ACTIVE WORK (2026-05-20): Liquid Glass → Bootstrap 5.3 порт

Текущая активная работа — порт утверждённых Liquid Glass прототипов на Bootstrap 5.3 (формат dev-handoff). При `resume design` выполни:

1. `cd ~/Desktop/design-project` · `git fetch && git pull` · `git log --oneline -5`
2. **Прочитай ПЕРВЫМ:** `docs/superpowers/HANDOFF-bootstrap-port.md` — единый источник истины: статус, NEXT, carry-forward, протокол исполнения, commit ledger.
3. **CRM-проект (`crm-bootstrap/`) ПОЛНОСТЬЮ ГОТОВ и отдан** (2026-05-20: все 29 экранов + styleguide + standalone + acceptance pass; архив отправлен Эльбику в Telegram). Не трогать без явного запроса.
4. **NEXT = Twinr-проект (`twinr-bootstrap/`)** — Phase 4 (Liquid Glass Customizer: SCSS + JS + page-stats/page-guide) → Phase 5 (PORT-MAPPING + 19 страниц, per-screen fidelity-гейт) → Phase 6 (styleguide + standalone + acceptance). План: `docs/superpowers/plans/2026-05-19-twinr-bootstrap-port.md`.
5. Работа в git-worktree `~/Desktop/design-project/.worktrees/feat-bootstrap-port`, ветка `feat/bootstrap-port` (не запушена, не смержена — merge gated на завершении Twinr, Эльбик-gated).
6. Invoke `superpowers:subagent-driven-development`. Пересоздай TaskList по Twinr-плану (задачи T18–T44). Продолжай subagent-driven: **один implementer за раз** (общий git-index — не параллелить), 2-stage review (fidelity → code-quality). Прототип = ground truth: `designs/twinr-liquid-glass.html`.
7. Ключевой carry-forward (полностью — в HANDOFF): AI-модуль = **9 инструментов**, не 11; `main.scss` уже корректен — не переписывать из плана; Customizer-значения брать из `tokens/_customizer.scss` (prototype-wins), не из плана; **CRM-паттерны копировать в Twinr** — `.btn-ghost`/`.btn-glass`/`.btn-primary`, glass только через `glass()` mixin, ноль inline `style=`/`on*=`, делегированные JS-модули (toast+form-preventDefault, counter, bulk, dynamic breadcrumb), responsive + a11y фиксы.

Продолжай автономно — не жди подтверждения.

---

## Общий протокол (для дизайн-работы вне bootstrap-порта)

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
Выведи таблицу:
| Параметр | Значение |
|----------|----------|
| Экранов готово | X / 13 |
| Тем готово | X / 6 |
| Открытый долг | X items |
| Последний коммит | дата + описание |

### 6. Continue Work
Продолжай работу автономно. Не жди подтверждения.
