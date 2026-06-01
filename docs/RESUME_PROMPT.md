# Resume Design — Активация сессии

## ⚡ ACTIVE WORK (2026-06-02 → next session): Город ФМ AI-product (pivot done, ЗАПУШЕНО)

Город ФМ развернулся в **AI-музыкальную платформу** (визия Эльбика). Весь AI-product слой ПОСТРОЕН + 10 Karpathy-брифов + синтез-доки. **ВСЁ ЗАКОММИЧЕНО И ЗАПУШЕНО** (`origin/master`, HEAD `d4479a3`+).

**📖 READ FIRST: `docs/superpowers/HANDOFF-gorod-fm-ai-product.md`** — полное состояние, архитектура decoupled-модулей (window.GorodOnboarding/TwinrChat/TwinrWave/WaveDials/TwinrRibbon), стратегия (Москва, разворот, лицензирование), open-gates, опции, как запустить демо.

**Готово:** Главная v2 `#/home` · онбординг-пузыри `#/onboarding` (Apple-style рекурс) · Twinr AI чат (explainable/steerable/живой профиль) · native-AI плеер («почему?»+steer) · живая волна + «Мой вкус» `#/taste` · 3-tab IA (Волна/Мой вкус/Открыть) · wave-диалы · between-track лента · audio-reactive волна · **tech-modern restyle** (нейтрал near-black `#0B0C0F` + 1 акцент `#5168FC`). UX-волна **6/6 done**.

🎯 **Рынок = МОСКВА** (не Казахстан). Wedge = прозрачность + редактируемый вкус + объяснимость (не локальность — домашка Яндекса).

При `resume design`:
1. `cd ~/Desktop/design-project` · `git pull` · `git log --oneline -8` (HEAD `d4479a3`+ на top)
2. **Read `docs/superpowers/HANDOFF-gorod-fm-ai-product.md`** (главный артефакт) + `.claude-memory/session_2026_06_02_gorod_fm_ai_pivot.md`
3. Демо: `cd designs && python -m http.server 8765` → `http://127.0.0.1:8765/gorod-fm.html#/onboarding` · `#/home` · `#/taste`
4. **Опции (выбрать с Эльбиком):** (A) добить 3 Figma-экрана GOROD-021 (Медиатека 2385:2924 / Избранное 2535:11151 / Артист 2537:14090) под нейтрал-рестайл · (B) standalone-сборка для инвесторов GOROD-032 · (C) полировка стиля (UI-AUDIT: унификация акцента, ретема, волна за плеером) · (D) реальный бэкенд (Ф1+, по ARCHITECTURE). **Рекомендация: B → A/C.**
5. 🔒 **Эльбик-gate (НЕ Claude):** GOROD-029 принять позиционирование · GOROD-030 лицензирование (7digital/Spotify-SDK + IP-юрист, узкое горло №1).

v2 pixel-perfect (GOROD-021): Главная+Подборки ✅; 3 экрана остаются (старый `HANDOFF-gorod-fm-v2-pixel-perfect.md` валиден для них).

Продолжай автономно — не жди подтверждения. Holy Grail Часть 9 + anti-slop gate перед `done`.

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
