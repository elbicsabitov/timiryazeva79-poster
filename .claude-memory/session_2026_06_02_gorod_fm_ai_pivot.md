# Session 2026-06-02 — Город ФМ: AI-product pivot + Karpathy research

**Entry:** `resume gorod fm`. **Branch:** master (не запушено). **Effort:** max.

## Что нашёл на старте
- Прошлая сессия (27.05 ночь) **упала, не закоммитив готовую Главную** (687-строчный uncommitted diff `gorod-fm.html`) и **не записав session log**.
- В дампе всплыли **12 сообщений Эльбика 27.05** (продуктовая визия AI-музыкального стриминга), которые прошлая сессия проигнорировала/потеряла.

## Сделано (всё закоммичено на master)
| Commit | Что |
|--------|-----|
| `afd072a` | **Главная v2** pixel-perfect Figma 2174:422 — добил чёрный фон (override bg-layers на `#/home`), залочил uncommitted работу |
| `6c8e802` | **Онбординг-пузыри `#/onboarding`** Apple-Music-style (физика rAF, gravity+repulsion) + VISION-док |
| `ef483a4` | Онбординг fix: bubbles в safe-zone (не на текст/кнопки), full-bleed fixed inset:0 |
| `38d334a` | **Twinr AI чат** — collapsible, живой профиль, explainable/steerable/tours/ads |
| research+arch | 6 backend брифов (`01-06`) + `ARCHITECTURE-gorod-fm-nextgen.md` |
| ux+`8ec5e4a` | 4 UX брифа (`07-10`) + `UX-DIRECTION-gorod-fm.md` + **native AI в плеере** |

## Итерации по требованиям Эльбика (в реальном времени)
1. «при нажатии на шарик появляются ещё, как Apple Music» → рекурсивный bloom (жанр→артисты, артист→похожие).
2. «на каждый bloom-шарик тоже ещё, безлимит» → genre-tagged POOL fallback + depth-cap снят + pruning (cap 80).
3. «во весь экран без лишних элементов» → fixed inset:0, скрыл chrome/player/tweaks.
4. «шарики в кликабельной зоне, не на кнопки/надписи» → dynamic safe-band (measure header/footer).
5. «AI присущим сайту + Karpathy UI/UX ресёрч» → 4 UX-агента + native-AI в плеере (демоут углового чата).

## Karpathy ресёрч (10 параллельных best-practices агентов)
**Backend (01-06):** hybrid 2-stage funnel · CLAP-вектор · Spotify BaRT explore-exploit-**explain** бандит · multi-vector Twinr (slow EMA + SASRec session) · Yandex Yambda bootstrap · CTRL-Rec стиринг (<50ms) · embed-then-decay онбординг · retrieval-first/LLM-last объяснения + NLI gate · **лицензирование = бизнес** (7digital MaaS / Spotify SDK demo / CC seed) · разворот «первый AI»→transparency+локальность.
**UX (07-10):** AI = слой не окно (Spotify-AI-DJ-в-плеере) · 3-tab IA (Волна/Мой вкус/Открыть) · why-чип progressive disclosure · диалы+текст один session-вектор · Twinr = редактируемый экран · ОДНА audio-reactive «волна» = идентичность · Twinr = ambient edge-aura не orb · koshkar-muiz геометрия для локальности.

## 🔑 Решения Эльбику (gate)
- **GOROD-029** принять разворот позиционирования.
- **GOROD-030** лицензирование — старт переговоров + IP-юрист (узкое горло №1).
- Прочее автономно.

## Следующая сессия
- GOROD-021: Медиатека/Избранное/Артист (Figma 2385:2924 / 2535:11151 / 2537:14090) + standalone rebuild.
- GOROD-031: следующая UX-волна (живая волна, экран «Мой вкус», mood-диалы, between-track лента, 3-tab IA).
- Standalone для инвесторов (GOROD-032).

**Демо локально:** `python -m http.server 8765` в `designs/` → `http://127.0.0.1:8765/gorod-fm.html#/onboarding` и `#/home` (кнопка «Twinr AI» + «почему?» в плеере).
