# BACKLOG — Twinr Design System / design-project
<!-- DURABLE open-work registry. The single source of truth for ALL open/deferred work.
     APPEND-ONLY. Never auto-pruned. IDs (Bnnn) are monotonic and never reused.
     STATUS: OPEN -> WIP -> DONE | DROPPED(reason). Nothing is EVER removed silently.
     DEBT.md archives session scratch; THIS FILE DOES NOT. If an item lives only in DEBT
     or a session note, it is NOT tracked — put it here.
     Resume greps OPEN/WIP only (stays lean). Move DONE to BACKLOG_ARCHIVE.md only if >40KB.
     Convergence: project is "finished" when OPEN+WIP = 0 (GATED items excepted). -->
_updated: 2026-06-29 (sync — rusradio гео added; feat/gorod-chat-layer pushed)_ · _next id: B052_

---

## DECISIONS-PENDING — owner/client must choose to unblock
<!-- These cannot be started until someone makes a call. Nothing here is buildable yet. -->
- **B001** `OPEN` — **Twinr (Большой Цифровой): выбор финальной темы** — 7 вариантов на руках (Twinr Native indigo / Pearl Violet / Warm Parchment / Fog Glass / Warm Luxury / Arctic Cyan / Ink Rose), заказчик не выбрал _(src: DEBT INT-001 · gate: клиент)_
- **B002** `OPEN` — **Twinr LG: показ заказчику Liquid Glass + фидбек** — LG-редизайн (21 экран + AI-модуль + Customizer + standalone 1.7 MB) готов, заказчик не видел, одобрение не получено _(src: DEBT LG-009 · gate: клиент)_
- **B003** `OPEN` — **Turbo Перформанс CRM: первый показ заказчику** — `designs/crm-glass.html` (29 экранов, 230 KB + 934 KB standalone) ждёт фидбека _(src: DEBT CRM-018 · gate: клиент Turbo)_
- **B004** `OPEN` — **RU.TV: показ заказчику + выбор направления** — два production-ready файла готовы (dashboard aggregator 10 MB + cinematic 4.5 MB; 3 темы; Figma 1-в-1 + Karpathy-best), заказчик не выбрал ни одно из трёх решений (RUTV-009/RUTV-021/RUTV-119) _(src: DEBT RUTV-009/021/119 · gate: заказчик RU.TV)_
- **B005** `OPEN` — **Лендинг кинологов (Настя/Paws): показ Серёге/Кате/Насте** — 3 варианта (paws / glass / material, standalone) готовы; 7 открытых уточнений от Насти (статистика, IAABC, кейсы, дата старта, CTA) _(src: DEBT KIN-012/013 · gate: Серёга/Катя/Настя)_
- **B006** `OPEN` — **Smartwatch RMG: ревью Stas/Alexei** — 5 станций готовы (treки, подкасты, избранное, плеер) _(src: DEBT SW-007 · gate: Stas/Alexei RMG)_
- **B007** `OPEN` — **Город ФМ (cont-17): merge-or-keep ветки** — ✅ push DONE на sync 2026-06-29 (`feat/gorod-chat-layer` на origin со всеми local-коммитами 18d375d/90adb11/b12ff6d); остаётся owner-call merge-or-keep в master (репо шарен → держать изолированной) _(src: HANDOFF-gorod-fm-cont-17 · gate: Эльбик merge-decision)_
- **B008** `OPEN` — **Город ФМ: GOROD-030 лицензии** — #1 bottleneck, standing gate из предыдущих сессий _(src: HANDOFF-gorod-fm-cont-17 / cont-16 · gate: внешнее/юридическое)_
- **B009** `OPEN` — **Город ФМ: GOROD-029 позиционирование** — standing gate _(src: HANDOFF-gorod-fm-cont-17 · gate: owner)_
- **B010** `OPEN` — **Bootstrap port: merge `feat/bootstrap-port` → master** — CRM DONE, Twinr pending Phase 4-6; мерж-поезд Эльбик-gated _(src: HANDOFF-bootstrap-port · gate: Эльбик, после завершения Twinr)_
- **B051** `OPEN` — **rusradio (РМГ): показ гео-подсказки в DFM + выбор варианта** — 4 десктоп + мобайл готовы в Figma «Русское Радио - солянка» (`XxJR3WmxhUxaQE9NlYGHU7` node 1460:218); клиент выбирает стекло (свет/тёмн) · текст (кратко/с городом) · размещение (поповер/плашка); после выбора — доработка + домобилить _(src: DEBT RR-005/006 · gate: клиент DFM)_

---

## DESIGN — buildable now (no pending client gate)
- **B011** `OPEN` — **Twinr SC-012: Wordstat — полный дизайн** (сейчас placeholder `page-wordstat`) _(src: DEBT SC-012 · gate: нет)_
- **B012** `OPEN` — **Twinr SC-013: ИИ-аналитика — полный дизайн** (сейчас placeholder `page-ai`) _(src: DEBT SC-013 · gate: нет)_
- **B013** `OPEN` — **Twinr CP-001: DESIGN.md** — полная дизайн-система в markdown (токены, компоненты, правила) для AI-агентов _(src: DEBT CP-001 · gate: нет)_
- **B014** `OPEN` — **Twinr CP-002: responsive адаптация** (mobile/tablet breakpoints для `twinr-full.html` и тем) _(src: DEBT CP-002 · gate: нет)_
- **B015** `OPEN` — **Twinr CP-003: перенос в Figma** — обновить РК экраны (4406:333–758) в выбранной тёмной теме _(src: DEBT CP-003 · gate: нет, но логично после B001)_
- **B016** `OPEN` — **Twinr CP-004: shadcn/ui component mapping** _(src: DEBT CP-004 · gate: нет)_
- **B017** `OPEN` — **RU.TV: brand + performance audit** — финальная brand check от RU.TV (шрифты, brand guidelines), performance audit (10 MB standalone — WebP оптимизация) _(src: DEBT RUTV-018/019 · gate: нет)_
- **B018** `OPEN` — **Smartwatch RMG: остальные станции по брендбукам** — PDF брендбуки скачаны _(src: DEBT SW-008 · gate: нет)_
- **B019** `OPEN` — **Город ФМ: track-file "Следующие в эфире" queue** — статическая демо-очередь (Thunder/Enemy/Radioactive/Demons), owner решает: оставить demo vs wire taste-aware (Ф1+) _(src: HANDOFF-gorod-fm-cont-17 §Open/known #1 · gate: owner design-judgment)_
- **B020** `OPEN` — **Город ФМ: rail profile-tags scroll affordance** — hidden-scroll strip last-tag cut, 3 опции: keep / right-edge fade / 2-line layout / cap+N _(src: HANDOFF-gorod-fm-cont-17 §Open/known #2 · gate: owner design-judgment)_

---

## GATED ON CLIENT DECISION — unlocks after Bnnn above
<!-- Cannot start until parent item reaches DONE. IDs track the dependency. -->

### Twinr (после B001 — выбор темы)
- **B021** `OPEN` — INT-002: Next.js + shadcn/ui проект на базе выбранной темы _(src: DEBT INT-002 · gate: B001)_
- **B022** `OPEN` — INT-003/004: MicroIT API + DaData API интеграции _(src: DEBT INT-003/004 · gate: B021)_

### Twinr LG + AI-модуль + Customizer (после B002 — одобрение)
- **B023** `OPEN` — LG-010/011/013: responsive (mobile/tablet) + light theme (dawn, optional) + backdrop picker variants _(src: DEBT LG-010/011/013 · gate: B002)_
- **B024** `OPEN` — LG-012: Figma перенос Liquid Glass темы — обновить РК экраны _(src: DEBT LG-012 · gate: B002)_
- **B025** `OPEN` — LG-014: Next.js + shadcn/ui реализация на базе утверждённой LG темы _(src: DEBT LG-014 · gate: B002 + B021)_
- **B026** `OPEN` — TURBO-010/011/012/013/014: real data вместо lorem ipsum · empty states · mobile/tablet responsive AI · dynamic glass reactivity · VoiceOver + контраст WCAG _(src: DEBT TURBO-010…014 · gate: B002 или B003 клиент одобряет направление)_
- **B027** `OPEN` — CUST-012/013/014/015: зафиксировать glass-* токены → применить ко ВСЕМ экранам → Figma sync компонентов → удалить кастомайзер из production-сборки _(src: DEBT CUST-012…015 · gate: B002)_

### CRM Glass (после B003 — фидбек)
- **B028** `OPEN` — CRM-019/020/021/022/023: ревью покрытия · responsive · dark/light toggle · Next.js реализация · API turbo-performance.ru _(src: DEBT CRM-019…023 · gate: B003)_

### RU.TV (после B004 — выбор направления)
- **B029** `OPEN` — Dashboard-направление: RUTV-010 Apple HIG fidelity audit · RUTV-011 Smart TV mode (10ft) · RUTV-012 SVG лого партнёров · RUTV-013 portrait фото · RUTV-014 inner pages · RUTV-015 HLS video · RUTV-016 Next.js _(src: DEBT RUTV-010…016 · gate: B004)_
- **B030** `OPEN` — Landing-направление (Figma→production-best): RUTV-116 real video stream · RUTV-117 search · RUTV-118 auth flow · RUTV-120 deck + walkthrough видео _(src: DEBT RUTV-116…120 · gate: B004)_
- **B031** `OPEN` — RUTV-017: mobile responsive deep audit обоих вариантов (375/414/768) _(src: DEBT RUTV-017 · gate: нет, делаем сейчас)_

### Кинологи (после B005 — показ + уточнения от Насти)
- **B032** `OPEN` — KIN-014/015/016/017/018: реальные CTA (форма заявки/Telegram) · дата старта · блок отзывов/кейсов · mobile-тест 375/768px · Next.js реализация _(src: DEBT KIN-014…018 · gate: B005)_

---

## BOOTSTRAP PORT — Twinr (worktree `feat/bootstrap-port`)
<!-- CRM 100% done + delivered. Twinr: Phase 0-3 done; Phase 4-6 remain. -->
- **B033** `OPEN` — **Phase 4** (T18-T20): Liquid Glass Customizer SCSS (`widgets/_customizer.scss`) + Customizer JS (`modules/customizer.js`, intensity math 1:1 с прототипом; dim key = `strong`) + first rendered pages (`page-stats` default + `page-guide` с customizer; replace index.html stub) _(src: HANDOFF-bootstrap-port §NEXT · gate: нет, buildable now)_
- **B034** `OPEN` — **Phase 5** (T40-T41): lock `twinr-bootstrap/docs/PORT-MAPPING.md` + портировать 19 оставшихся экранов (1 screen = 1 commit = 1 fidelity gate; screenshot-diff vs `twinr-liquid-glass.html`) _(src: HANDOFF-bootstrap-port §NEXT · gate: B033)_
- **B035** `OPEN` — **Phase 6** (T42-T44): styleguide kitchen-sink · standalone build (`npm run build:standalone`) · full acceptance pass; затем `crm+twinr-bootstrap-handoff-2026-XX-XX.zip` → Telegram _(src: HANDOFF-bootstrap-port §NEXT · gate: B034, затем B010 мерж)_

---

## LEGAL / EXTERNAL — Постер Тимирязева 79 (мама)
<!-- Процедура egov.kz по Закону «О рекламе», V23R0001724, V23R0001751 — детали в session_2026_04_24.md. -->
- **B036** `OPEN` — PST-008: фото перспективы фасада Тимирязева 79 (нужно для mock-up при подаче) _(src: DEBT PST-008 · gate: физически выйти)_
- **B037** `OPEN` — PST-007a: технический эскиз PDF (1300×560 мм, HEX/Pantone, mock-up на фасаде) _(src: DEBT PST-007a · gate: нет, взять poster-forest-final.html как референс)_
- **B038** `OPEN` — PST-007b: оплата 4 325 ₸ → Kaspi → КБК 105402, Бостандыкский район (до подачи) _(src: DEBT PST-007b · gate: B037)_
- **B039** `OPEN` — PST-007c: подать заявление на egov.kz под ЭЦП мамы (эскиз + правоустанавливающий + чек) _(src: DEBT PST-007c · gate: B037+B038)_
- **B040** `OPEN` — PST-007d/e/f: ждать 5 раб. дней → получить согласование; при отказе по п.6 (цвет) — переделать эскиз (беж/серый); ежемесячная уплата 4 325 ₸ до 25 числа _(src: DEBT PST-007d/e/f · gate: B039)_

---

## DONE (closed — kept for audit trail)
- **D-CRM-BOOTSTRAP** `DONE` — CRM Glass → Bootstrap 5.3: all 29 screens ported + verified, kitchen-sink styleguide, standalone, README/CONTRIBUTING/ACCEPTANCE. Delivered `crm-bootstrap-handoff-2026-05-20.zip` commit `306166d` _(closed 2026-05-20)_
- **D-RU-TV-V6** `DONE` — RU.TV landing v6: Figma frame 3373:2073 mapped + real SVG logo + 2 versions (`rutv-landing.html` Karpathy-best 7-hash-route SPA · `rutv-landing-figma.html` 1-в-1 Figma) _(closed 2026-05-13)_
- **D-GOROD-CONT17** `DONE` — Город ФМ cont-17: ubiquitous chat-layer + glass skin + shared radio (13 commits `f1a5663→18d375d`); 2 bugs fixed (IMAGINE DRAGONS typo + B2 track-file desync); branch `feat/gorod-chat-layer` on origin, local 2 commits unpushed _(closed/verified 2026-06-24)_
- **D-TWINR-AI** `DONE` — Twinr AI-модуль: 9 AI-экранов (Источники/Промпты/Рерайтинг/Чат/Транскрибация/Документы/Видео/Wordstat/Работа с источником) + Discovery Hub + Customizer (38 droplets + panel 6 presets) + standalone 1.7 MB _(closed 2026-04-18)_
- **D-CRM-GLASS** `DONE` — CRM Glass (Turbo Performance): 29 экранов + rich-data (17 колонок, 6 фильтров, column-toggle, bulk) + 4 модалки + standalone 934 KB _(closed 2026-04-22)_
- **D-RU-TV-V1-V5** `DONE` — RU.TV showcase v1→v5: dashboard aggregator (104 real assets, chart, schedule, 3 themes) + cinematic (Apple TV+ hero, bento, off-canvas, scroll reveal) _(closed 2026-04-29)_
- **D-KINOLOG** `DONE` — Лендинг кинологов: 3 варианта (paws/glass/material) + WCAG AA fix + anti-hallucination pass + standalone _(closed 2026-04-24)_
- **D-POSTER-DESIGN** `DONE` — Постер Тимирязева 79: дизайн 130×56 см (4 варианта) → forest утверждён → файл для типографии → заказ 20 000 ₸, 3 раб. дня _(closed 2026-04-16)_
- **D-TWINR-FULL** `DONE` — Twinr РК: полный SPA 13 экранов (`twinr-full.html`) + 6 цветовых тем; Twinr Native (indigo) выбран заказчиком _(closed 2026-04-15)_
