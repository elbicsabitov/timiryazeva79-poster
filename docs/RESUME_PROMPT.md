# Resume Design — Активация сессии

## ⚡ ACTIVE WORK (2026-05-27): Город ФМ HTML SPA — kickoff

Новый клиент — **онлайн-радио «Город ФМ»**. Hi-fi clickable single-file HTML SPA, 7 экранов + Monte Carlo-style player overlay + flow map, адаптивный к web/mobile/TV/CarPlay. По образцу design-project's `twinr-liquid-glass.html` / `showcase-aggregator.html` (НЕ paws — только pattern). При `resume design` выполни:

1. `cd ~/Desktop/design-project` · `git fetch && git pull` · `git log --oneline -5` (kickoff commit должен быть на топе)
2. **Прочитай ПЕРВЫМ:** `docs/superpowers/HANDOFF-gorod-fm.md` — единый источник истины: figma URLs/node IDs, tokens, screen list, persistent components, adaptable surface architecture, NEXT, carry-forward.
3. **Прочитай:** `.claude-memory/session_2026_05_27_gorod_fm_kickoff.md` — что было в kickoff-сессии, что НЕ написано.
4. **Скриншоты Figma** preserved в `.scratch/gorod-fm-research/` (3 PNG: gorod-home + MC-desktop + MC-mobile). Photo reference: `~/Desktop/photo_2026-05-27_17-27-05.jpg`.
5. **Master direct** convention (НЕ feature branch). Atomic commits per screen.
6. Invoke `superpowers:subagent-driven-development`. **One implementer at a time** (shared git index — не параллелить). TaskList state в HANDOFF — entry point task #4 (tokens write в файл) → #5 Flow Map → #6 Главная → ... → #15 standalone.
7. **Carry-forward (полностью в HANDOFF):** NO paws data; Onest substitute for SF Pro/Gilroy/Actay Wide (Holy Grail compliant, fake-wide через `scaleX(1.05)`); asset placeholder V1 (Figma URLs expire 7d); Tweaks single-file (не N тематических); themes dual (cinema/warm) + light Phase 2; `data-surface="web|mobile|tv|carplay"`; round-button-UX «не додумали» → 2 Tweak варианта.

Продолжай автономно — не жди подтверждения. Holy Grail Часть 9 чек-лист перед `done`/коммитом/отправкой заказчику.

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
