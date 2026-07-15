# NEXT — design-project
<!-- Single source of truth for "where to start next". Read FIRST on resume.
     Keep ## NEXT <= ~8 lines; it POINTS, detail stays in STATE/docs.
     ⚠️ Файл ветвится: эта версия — ветка feat/rutv-showcase-v2 (RU.TV трек).
     Gorod/Twinr-версия живёт на feat/gorod-home-rmg-storefront. -->
_updated: 2026-07-15_

## NEXT
▶ RU.TV showcase v2 (АКТИВНЫЙ трек) — ветка `feat/rutv-showcase-v2`, HEAD `980f025`, НЕ запушена. Редизайн по ТЗ Эльбика ДОСТАВЛЕН: розовый #E40087 + официальный лого с ru.tv · hero эфира + промо 300×600 · 6 подканалов · меню Главная/Премия/Новости+Афиша/Программы(9)/Видео/Витрина подарков · PiP вместо нижнего плеера · one-click эфир · баллы за просмотр (Twitch-механика). Standalone пересобран, офлайн-чист (0 assets-запросов, консоль 0). Файл: `designs/showcase-aggregator.html` (+standalone 11.4MB).
- ЗА ЗАКАЗЧИКОМ: RUTV-121 (URL лендинга Премии) · RUTV-122 (ведущие: состав/фото) · RUTV-123 (реальная сетка программ) · RUTV-125 (сверка розового/лого с брендбуком) · RUTV-126 (наполнение подканалов).
- OPEN: RUTV-124 (мобильный формат промо 300×250) · RUTV-127 (прод-тайминги баллов — демо ×5) · RUTV-128 (мобильное меню: сайдбар <900px скрыт).
- Ассеты: `designs/assets/rutv/rutv-logo-official.svg` + `rutv-mark-official.svg` (скачаны с ru.tv 15.07).
- ВТОРОЙ ТРЕК — Город ФМ: ветка `feat/gorod-home-rmg-storefront` (HEAD `21c45d2`, там свой NEXT.md). Twinr — `feat/twinr-tg-audit`.
- Долги всех треков: `DEBT.md` (RU.TV v2 = RUTV-121..128).

## DECISIONS
- 2026-07-15 — Брендовый розовый RU.TV = **#E40087** (из официального favicon.svg на ru.tv; в CSS-бандлах сайта hex-акцентов нет — favicon единственный первоисточник цвета). Логотип = `logo.e3ca789.svg` из шапки ru.tv, одноцветный → инлайн с currentColor (белый на тёмных темах, розовый на светлой). Сверка с брендбуком — RUTV-125.
- 2026-07-15 — Нижний sticky-плеер (радийный паттерн) заменён PiP мини-плеером: у видеосервиса «эфир всегда рядом» = плавающее окно (YouTube miniplayer/Twitch persistent player), а не аудио-бар. Tweaks-панель переехала влево.
- 2026-07-15 — Баллы зрителя по механике Twitch channel points: +10 за 5 мин просмотра, бонус-сундук +50 раз в 15 мин, множитель за серию дней. В демо тайминги ×5 быстрее (60/90 сек) — вернуть в проде (RUTV-127).
<!-- dated, newest first, append-only -->

## JOURNAL
- 2026-07-15 — 📦 v2.1 ДОСТАВЛЕНО: правки owner'а (сайдбар БЕЗ мини-виджета эфира — чисто лого+меню; Супер 20 на главной = топ-10, полная двадцатка по переходу «Вся двадцатка →» на страницу #chart вне меню) · commit `af89612` · офлайн-смоук из чистой папки 0/0 · zip `rutv-showcase-v2.1-standalone-2026-07-15.zip` (8.34MB) → Saved Messages **msg 602424**, без подписи. АКТУАЛЬНЫЙ = 602424 (602408 устарел — там ещё виджет и чарт×20 на главной).
- 2026-07-15 — 📦 ДОСТАВЛЕНО: zip `deliverables/2026-07-15/rutv-showcase-v2-standalone-2026-07-15.zip` (8.74MB, внутри `rutv-showcase-v2-standalone.html`) → Telegram Saved Messages **msg 602408**, БЕЗ подписи (директива owner'а «чисто zip»). Рельса: `.scratch/rutv2/send_zip_to_saved.py` (telethon-сессия mama-helper read-only, force_document).
- 2026-07-15 — RU.TV showcase v2: розовый ребрендинг (все 3 темы) + официальный лого/фавикон с ru.tv · hero+промо 300×600 (IAB) с ротацией креативов · 6 подканалов с переключением эфира · новое меню + страницы Новости(+Афиша)/Программы(9 плиток)/Видео/Витрина подарков · PiP-миниплеер + one-click эфир · баллы+сундук+обмен подарков · скриншот-верификация 3 темы × desktop/mobile, все страницы · standalone 11.4MB офлайн-чист · commit `980f025`
<!-- dated one-liners, newest first; prune older than ~5 sessions -->
