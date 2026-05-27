# Resume Design — Активация сессии

## ⚡ ACTIVE WORK (2026-05-27 night → next session): Город ФМ v2 pixel-perfect rebuild from Figma

**v1 SHIPPED** (16 commits, HEAD `77ee5c1`, file `designs/gorod-fm.html` 10,274 lines). v1 covered все 7 routes + Player overlay + Tweaks panel. Holy Grail compliant.

**v2 NEEDED** — user feedback 2026-05-27 night: «доведи все до pixel perfect с фигмы». Discovered 5 fuller Figma designs we missed:

| Figma node | Screen | Status |
|---|---|---|
| `2174:422` | Главная (dark black, 9 tiles + featured CTA card) | ❌ наш сильно отличается |
| `2384:6054` | Подборки (с РЕАЛЬНЫМИ фото artists) | ⚠️ структура OK, нет реальных картинок |
| `2385:2924` | Медиатека (Search+ABC+artist grid) | ❌ |
| `2535:11151` | Раздел Избранное (DJ/Группы/Исполнители rows) | ❌ |
| `2537:14090` | Страница артиста (photo card + lyrics + tracks) | ❌ |

**Полный handoff v2:** `docs/superpowers/HANDOFF-gorod-fm-v2-pixel-perfect.md` — READ FIRST.

При `resume design`:

1. `cd ~/Desktop/design-project` · `git fetch && git pull` · `git log --oneline -10` (verify HEAD `77ee5c1` Город ФМ commits on top)
2. **Read `docs/superpowers/HANDOFF-gorod-fm-v2-pixel-perfect.md`** — strategy, 5 Figma nodes, new brand tokens, sidebar nav decisions, file pointers
3. Read `.claude-memory/session_2026_05_27_gorod_fm_v2_handoff.md` (this session's transcript)
4. **Phase 1:** re-fetch all 5 Figma design contexts in parallel (URLs from previous session expired). Download & dedupe assets to `designs/assets/gorod-fm/`.
5. **Phase 2:** rewrite each screen sequentially. Order: Подборки (smallest delta) → Главная → Медиатека → Раздел Избранное → Страница артиста. Atomic commit per screen.
6. **Phase 3:** visual verify via Chrome MCP at `http://127.0.0.1:8765/gorod-fm.html`.
7. **Phase 4:** standalone rebuild (assets will be inlined as base64 by `tools/build_gorod_fm_standalone.py`).
8. Close GOROD-021 in DEBT.md; update session log + memory.

Продолжай автономно — не жди подтверждения. Holy Grail Часть 9 чек-лист перед `done`.

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
