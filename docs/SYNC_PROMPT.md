# Sync Design — Сохранение сессии

## Шаги

### 1. Git Commit
```bash
git add -A
git commit -m "тип: описание"
git push
```
Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`

### 2. Update Memory
- `.claude-memory/MEMORY.md` — добавь запись о сессии
- Создай `.claude-memory/session_YYYY_MM_DD.md` с:
  - Что было сделано
  - Какие решения приняты
  - Что дальше

### 3. Update DEBT.md
- Закрой выполненные пункты
- Добавь новые (если появились)

### 4. Report
Выведи:
- Что сделано за сессию
- Что закоммичено
- Что осталось в DEBT.md
