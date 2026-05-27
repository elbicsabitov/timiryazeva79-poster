# Resume Design — Активация сессии

## ⚡ ACTIVE WORK (2026-05-27): Город ФМ HTML SPA — v1 built, ждём заказчика

`designs/gorod-fm.html` (10258 lines) + `designs/gorod-fm-standalone.html` shipped via 13 atomic commits on master. 7 routes, full Player overlay, Tweaks panel (theme/surface/A-B home variant/hide-flow-map). Holy Grail compliant.

Pending: client feedback (GOROD-017), real assets when client provides (GOROD-016), Next.js handoff after approval (GOROD-018). Optional: final WCAG verification pass (GOROD-019).

При `resume design`:
1. `cd ~/Desktop/design-project` · `git fetch && git pull` · `git log --oneline -10` (verify Город ФМ commits on top)
2. Read `docs/superpowers/HANDOFF-gorod-fm.md` + `docs/superpowers/REVIEW-gorod-fm-2026-05-27.md` (review findings)
3. Read `.claude-memory/session_2026_05_27_gorod_fm_v1.md` (build session log)
4. If client has provided feedback or assets → apply via new fix wave on master, atomic commits per change
5. If no feedback yet → check DEBT.md other client items (Twinr Phase 4, bootstrap-port resume, etc)

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
Выведи таблицу:
| Параметр | Значение |
|----------|----------|
| Экранов готово | X / 13 |
| Тем готово | X / 6 |
| Открытый долг | X items |
| Последний коммит | дата + описание |

### 6. Continue Work
Продолжай работу автономно. Не жди подтверждения.
