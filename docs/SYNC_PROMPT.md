# Sync Design — Сохранение сессии (extended protocol)

Цель: каждый sync оставляет проект в состоянии «через полгода кто угодно (в т.ч. я сам) откроет и поймёт что было и почему». И standalone-файл всегда актуален для заказчика.

## 0. Pre-sync audit (5 мин)

```bash
# Что изменилось
git status -s
git diff --stat HEAD

# Branch check (должен быть master)
git branch --show-current

# Remote reachable?
git remote -v
```

**Стоп-флаги:**
- Не-master branch → подтвердить у elbics, нужен ли push туда
- Unexpected untracked файлы → проверить что не забыл .gitignore
- Diff > 500 строк → серьёзная сессия, нужна особенно детальная фиксация

## 1. Rebuild artefacts (если изменился primary prototype)

Если изменился `designs/twinr-liquid-glass.html` — **ОБЯЗАТЕЛЬНО** пересобрать standalone с inline base64:

```bash
cd ~/Desktop/design-project/designs && python -c "
import base64
with open('assets/sunset-backdrop.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('ascii')
with open('twinr-liquid-glass.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace(\"url('assets/sunset-backdrop.jpg')\", f\"url('data:image/jpeg;base64,{b64}')\")
with open('twinr-liquid-glass-standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('standalone ok:', len(html) // 1024, 'KB')
"
```

Проверить что standalone открывается двойным кликом (без HTTP-сервера) — это файл для заказчика.

## 2. Verify (проверка что прототип работает)

Быстрый smoke-test:
- Open http://localhost:8765/designs/twinr-liquid-glass.html (или прямо file://)
- Check console — 0 errors
- Click через 3-4 ключевых экрана
- Test любой модалки (open + close)
- Responsive: ресайз до 1280 и 1024px — layout не ломается

Если нашёл баг — чини его в этой же сессии до sync.

## 3. Update DEBT.md

Структура (обязательно):
- Закрыть все выполненные пункты: статус `done`
- Добавить новые пункты появившиеся в сессии (с понятным ID)
- Новая секция если большой блок работы (напр. `## Турбо AI-модуль (2026-04-XX)`)
- Для pending пунктов — приоритет если известен

Пример нового блока:
```md
## Турбо AI-модуль (2026-04-18)

| ID | Задача | Статус |
|----|--------|--------|
| TURBO-001 | 9 AI-экранов из Figma в Liquid Glass | done |
| TURBO-002 | Discovery Hub с 4 группами | done |
| TURBO-003 | Показ заказчику | pending |
```

## 4. Create session log

Файл: `.claude-memory/session_YYYY_MM_DD_topic.md` (topic если в день несколько сессий).

**Обязательные секции:**
- **Контекст** — с чем начали, что попросил заказчик
- **Что сделано** — bulleted list (фичи, фиксы, решения)
- **Решения** — ключевые архитектурные выборы и ПОЧЕМУ
- **Блокеры / компромиссы** — что не сделали и почему
- **Файлы** — какие модифицированы с размерами
- **Что дальше** — open debt pointers

## 5. Update MEMORY.md

Обязательно:
1. Добавить запись о новой сессии в раздел `## Sessions`
2. Обновить `## Current Design Iteration`:
   - Active prototype (путь + размер KB/MB, количество страниц)
   - Эстетика (если изменилась — описать чем)
   - Список предыдущих итераций если появилась новая
   - Актуальные backdrop assets

Типичное обновление:
```md
**Active prototype:** `designs/twinr-liquid-glass.html` (280 KB, 22 страницы)
+ `designs/twinr-liquid-glass-standalone.html` (1.6 MB, base64 embed)
```

## 6. Commit (structured conventional)

Формат:
```
<type>: <короткая суть, ≤70 chars>

<абзац описания — что и почему, 1-3 предложения>

Changes:
- <фича 1> (пара слов о где/как)
- <фича 2>
- <фикс 1>

<Optional sections: Breaking / Notes / Refs>
```

Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `style`, `perf`.

Через HEREDOC:
```bash
git add -A
git commit -m "$(cat <<'EOF'
feat: Турбо AI-модуль — 9 экранов + Discovery Hub + Guide

Расширен прототип дополнительными экранами из Figma (...) всё в Liquid Glass.

Changes:
- 9 AI-инструментов (Источники, Промпты, Рерайтинг, ...)
- 5 модалок (edit group, sources, prompt, tags, keywords)
- Discovery Hub: 4 группы × карточки tools
- Sub-nav chip-row с slide-morph indicator
- Руководство: long-form reading с sticky TOC
- Apple HIG fixes: aria-current, tooltips, confirm, loading states

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

## 7. Push + verify

```bash
git push origin master
git log --oneline -3  # подтвердить что последний коммит ушёл
```

## 8. Report (для elbics)

**Что ушло:**
- Commit hash + message
- Size delta (+X lines, -Y lines)
- N новых экранов / модалок

**Для заказчика (если применимо):**
- Путь standalone файла (одна строка)
- 1-строчное описание что нового
- Что показать в первую очередь (deep-link в конкретный экран)

**Что в DEBT остаётся:**
- Pending items по приоритету
- Ближайший next step

---

## Антипаттерны (чего НЕ делать)

- ❌ `git add .` без проверки status — может затянуть .env / credentials
- ❌ Commit с `--no-verify` без явной причины
- ❌ Push в master без pre-verify
- ❌ Забыть пересобрать standalone → заказчик получит стаую версию
- ❌ «chore: sync» как commit message — не информативно
- ❌ Session log из одной строчки — через месяц не поймёшь что было
