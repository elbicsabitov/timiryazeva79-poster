# BLUEPRINT — Интеграция 5 легаси-секций в AI-first сервис · Город ФМ

> Источник: research-workflow `wuh68eajr` (5 per-section ресёрчей → синтез → adversarial-критик), 2026-06-03 cont-12. Figma-фреймы: ЛК / Подборки / Медиатека / Профиль артиста / Избранное.
> Статус: **BUILD-READY intent**. Критик-вердикт = REVISE → §8 содержит ОБЯЗАТЕЛЬНЫЕ grounding-правки (блюпринт местами критикует «призраков» и молча отменяет залоченные спеки — исправить ДО исполнения). НЕ реализовано.
> Главный результат: **3 таба остаются, 0 новых роутов**; ЛК=sheet; галерея=RETIRE (резолюция B1/B2). Дисциплина cont-12: re-grep якоря (НЕ по номерам строк — §8 п.4), `?v=N`, зеркалить в standalone.

---

# BLUEPRINT — Интеграция 5 легаси-«отделов» в AI-first сервис Город ФМ

> **Статус:** build-ready synthesis. Сводит 5 per-section research-выводов (ЛК · Подборки · Медиатека · Профиль артиста/трека · Избранное/Сохранённое) в один контракт интеграции. Grounded против `BLUEPRINT-gorod-fm-full-service.md` (§1 IA, §5 дизайн-система, §9 конфликты), `SPEC-00-foundation-and-integration.md` (build-order, cyan-retirement, anchor-collisions) и `HANDOFF-gorod-fm-cont-12.md` (живой gallery-restyle блокер).
> **Главный результат:** ни одной из 5 секций не нужен 4-й таб и ни одного нового роута. Все 5 либо уже впитаны существующими спеками, либо впитываются в них. Этот документ **не противоречит** SPEC-00 — он его продолжение для последних 5 легаси-фреймов.

---

## 1. Тезис (организующий принцип)

**Каждый из пяти легаси-«отделов» — это каталог-парадигма, переодетая в разные UI. AI-first сервис складывает их не как пять разделов, а как пять проекций ОДНОЙ петли доверия (`explain → reject → edit → steer → newExplain`): всё «известное тебе» сворачивается под МОЙ ВКУС как _причинный леджер роста модели_, всё «неизвестное» живёт в ОТКРЫТЬ как _объяснённое неизвестное_, идентичность/настройки уходят в _тонкий лист_ под тем же МОЙ ВКУС, а артист/трек остаются _deep-dive-листьями_ из любой карточки.** Принцип кристально простой и не-пересматриваемый: **известное → Мой вкус, неизвестное → Открыть, радио — не каталог.** Любой A-Z, любая «витрина обложек», любой счётчик слушателей, любое «фанаты также» — это каталог-клон, и мы его не строим; мы **EDIT for value**, и единственная честная замена каталогу — поиск→deep-dive и видимый-редактируемый вектор. Тройная ошибка Sonos (3 дублирующие browse-вкладки = ~$500M) — наш anti-pattern №1: мы не плодим вторую/третью поверхность «смотреть всё».

---

## 2. Единая IA-развилка

### Вердикт: **3-таба ОСТАЮТСЯ. Никакого 4-го таба. Никаких новых роутов.** ЛК = тонкий **sheet** (не таб), открываемый из шапки МОЙ ВКУС.

Это прямое следствие BLUEPRINT §1.1 («железное правило: 3 вкладки») и SPEC-00 §2.3. 4-й таб «Профиль/Настройки» был бы повторением Sonos-ошибки: настройки — самая чёрно-ящичная поверхность стриминга, и давать ей вес таба = ре-центрировать продукт на конфигурации вместо волны.

### Финальное IA-дерево (после интеграции всех 5 секций)

```
Город ФМ — 3 первичных таба + deep-dives + 1 sheet
│
├─ ВОЛНА  (#/home)                        ← радио, пассив-Я. Сюда уходит "lean-back/LIVE"-инстинкт
│   • now-playing + поведенческое «почему» + ❤/Steer/skip (skip вторичен)
│   • (никаких live-station-плиток — волна И ЕСТЬ эфир)
│
├─ МОЙ ВКУС  (#/taste)                     ← известное, актив-Я. ДОМ РОСТА МОДЕЛИ
│   • редактируемый вектор (читает gorodfm_rejected после W1)
│   • контекст-старты (051 ✓)  • стрик  • вход в #/recap
│   • ▸ «Сохранённое» <details>           ← ИЗБРАННОЕ + МЕДИАТЕКА слиты сюда
│   │     фильтры: Все/Треки/Артисты/Плейлисты/Станции
│   │     каждая строка = «что добавил в вкус» (причинный леджер) + «волна отсюда»
│   └─ ⚙/avatar в шапке → ▸ «Аккаунт» sheet ← ЛК сюда (тонкий, не таб)
│         идентичность (Twinr-ID) · 1× тема (3-way) · «смотри/правь вектор →»
│         · скачать мои данные · история/приватная сессия · удалить · Выйти
│
├─ ОТКРЫТЬ  (#/podborki, canonical #/discover)  ← неизвестное, актив-МИР
│   • разговорный «как X но Y» поиск (built → rework)
│   • «Карта твоего вкуса» + dial Рядом/Смело/На краю  ← ЖАНРЫ как узлы карты
│   • «От редакции» (кураторская подпись)    ← ВЫБОР РЕДАКЦИИ из легаси-Подборок
│   • [DELETE] легаси .podborki-gallery + .podborki-chip-row  ← ПОДБОРКИ-витрина РЕТАЙР
│
├─ deep-dives (push/overlay, НЕ табы — из любой карточки трека):
│   ├─ #/artist   ← «Профиль артиста» (фрейм splits сюда): реал-фото hero + поведенческое L1
│   ├─ #/track    ← «Профиль трека» (фрейм splits сюда): «Почему играет» + синк-текст + соседи-по-звучанию
│   ├─ #/recap    (из Мой вкус)
│   └─ #/profile  («Открытый профиль» — pitch; ЛИНКуется из Аккаунт-sheet)
│
└─ legacy routes (в VALID_ROUTES для deep-link/закладок/carplay-boot, БЕЗ nav-плитки):
    #/library  → redirect #/taste      (Медиатека)
    #/favorites→ redirect #/taste      (Избранное)
    #/map, #/lives → за флаг (dev-only)
```

### Разрешение наложений (явно, чтобы не пере-litigate)

| Наложение | Резолюция |
|---|---|
| **Подборки-легаси-хаб vs новый #/podborki discover** | Хаб НЕ становится красивее — он **растворяется**. Новый discover (поиск+карта+dial+«От редакции») = финал таба. Легаси-галерея **удаляется**, не рестайлится (см. §6, B1/B2). |
| **Избранное vs Сохранённое** | Одна поверхность: `GorodSaved`-аккордеон в `#/taste` (уже ~90% built, SPEC-taste_saved). Легаси `#/favorites` body — **мёртвый**, редиректит. Группы DJ/ГРУППЫ/ИСПОЛНИТЕЛИ → фильтр-чипы. |
| **Медиатека vs Избранное (дубль-архив)** | Сливаются в ОДНО «Сохранённое». Альбомы/подкасты Медиатеки НЕ тащим (generic-каталог, 0 wedge, SPEC-taste_saved C6). A-Z остаётся только как progressive-disclosure letter-jump по СВОИМ артистам. |
| **Медиатека-каталог vs radio-not-catalog** | A-Z-каталог = **CUT** (самое жёсткое противоречие тезиса). Честная замена «найти артиста» = поиск→#/artist + карта вкуса. |
| **ЛК vs 4-й таб** | ЛК = sheet под МОЙ ВКУС. Не таб, не роут-как-первичная-навигация. |
| **«Личностные настройки» (ЛК) vs видимый вектор (#/taste)** | Настройки НЕ дублируют вектор тумблерами — они **указывают НА** него («твой профиль не спрятан, правь его →»). Настройки point at transparency. |

---

## 3. Per-section вердикт-таблица

| Секция | Вердикт | Где живёт | Самое лучшее (взять из Figma) | Главное (выбросить) |
|---|---|---|---|---|
| **ЛК (Личный кабинет)** | **REFRAME** | Тонкий **sheet «Аккаунт»** под `#/taste` (открыть из ⚙/avatar). Никакого нового таба. | Email-link сброс пароля + интент единой 3-way темы (`Светлая/Тёмная/Как в системе`) — становится реальной заменой dev-gated theme-toggle. | Оба тумблера темы (→ один контрол), тройной Д/М/Г-пикер, дубль-ссылка «Смена пароля», и **весь маркетинг-футер** (nav/телефон/соцсети). |
| **Подборки (browse-хаб)** | **CUT (хаб) / FOLD (1 ряд)** | `#/podborki`. Хаб растворяется в built-механиках (поиск+карта+dial). | **ВЫБОР РЕДАКЦИИ** → уже свёрнут в «От редакции» (обязательная подпись куратора «собрал Илья, редакция»). ЖАНРЫ → узлы карты вкуса. | Вся 9-рядная витрина: `.podborki-gallery` + `.podborki-chip-row` + мёртвый `console.log`-фильтр + повёрнутые 900-вес подписи + СЕЙЧАС СЛУШАЮТ (collaborative=BANNED) + DJ/ГРУППЫ/ИСПОЛНИТЕЛИ/ВИДЕО. |
| **Медиатека (A-Z каталог)** | **CUT (каталог) / FOLD (residue)** | Не своя поверхность. Residue → фильтр «Артисты» в «Сохранённом» (`#/taste`). | Реал-фото-карточка артиста + letter-jump (но ТОЛЬКО по СВОИМ сохранённым артистам, не по глобальному каталогу). | A-Z-как-первичная-IA, «ИСПОЛНИТЕЛИ А»/«МЕДИАТЕКА»-обрамление, all-catalog scope, SVG-винил-обложки, синий градиент. |
| **Профиль артиста/трека** | **REFRAME** | Splits across два built deep-dive: `#/artist` + `#/track` (из любой карточки). | Реал-фото в hero (`#/artist`) + lyrics-как-first-class (`#/track`) + честное release-обрамление «Сингл · 2019». | **`· 6 345 245 слушателей`** (канонический vanity anti-pattern) + синий градиент + per-page genre-chips+search + «фанаты также» (любой намёк). |
| **Избранное/Сохранённое** | **REFRAME** | `GorodSaved`-аккордеон в `#/taste`, прямо под вектором. ~90% уже built. | Type-grouping → фильтр-чипы + round(person)/square(band) визуальная грамматика как art-tint+монограмма. | Standalone-страница/таб, синий градиент, cover-sampled заливки, и сам **bookmark-wall mental model** (→ причинный леджер). |

---

## 4. Как wedge переосмысляет каждую секцию (конкретно)

**ЛК → настройки, которые УКАЗЫВАЮТ на прозрачность, а не прячут её.** Generic settings — самая чёрно-ящичная поверхность стриминга. Wedge инвертирует: блок «персонализация» — не тумблеры, а deep-link на видимый+редактируемый вектор («твой профиль не спрятан — смотри и правь →»). Контрол «История/Приватная сессия» **называет своё поведенческое последствие** («Выключишь историю → волна перестаёт учиться на том, что ты дослушиваешь; грань-карта `#/recap` не соберётся») — это честнее Apple (у них «no history = no Replay» спрятано) и Spotify (у них профиль, на который влияет тумблер, не виден). «Скачать мои данные» рендерит **точно тот** `gorodfm_taste`/`gorodfm_rejected`-вектор, что крутит волну (через `window.TwinrModel`) — GDPR-экспорт становится не compliance-театром, а буквальным доказательством «не чёрный ящик». Демо-поля помечены «демо-».

**Подборки → 9-рядный хаб ЕСТЬ тот A-Z-каталог, ради отказа от которого мы существуем.** RADIO-NOT-CATALOG = весь ответ: 95% CUT. ЖАНРЫ перестают быть browse-сеткой и становятся именованными координатами на карте прозрачности (узел = позиция по everynoise-осям + поведенческое «почему» + `excludeKnown()`-инвариант: карта структурно возвращает только НЕИЗВЕСТНОЕ). ВЫБОР РЕДАКЦИИ → «От редакции» с обязательной человеческой подписью + честной нотой («не по твоему вектору — по нашему вкусу») = объяснимость через прозрачного человека. Мёртвый `console.log`-чип-фильтр = honesty-violation (fake affordance) → удалить. СЕЙЧАС СЛУШАЮТ = collaborative-сигнал → BANNED. (Apple убил Browse→New в iOS 18; Яндекс публично отрёкся «мы больше не утилитарный сервис с каталогом» — фронтир уже бросил эту парадигму.)

**Медиатека → A-Z-каталог = CUT как каталог; честная версия = поиск→#/artist.** Алфавитный индекс говорит «вот всё, иди сам найди» — это и есть чёрно-ящичная инверсия: вместо модели, которая объясняет и рулит, ты получаешь картотеку, которая абдицирует. У A-Z нет per-item «почему», а единственное «почему», которое каталог мог бы подделать (collaborative «фанаты также»), wedge запрещает. HONESTY делает хуже: каталог намекает на полноту, которую Stage-0 (CC/Jamendo) честно не покрывает → «perceived-catalog» = сиблинг vanity-«6M слушателей». Единственный wedge-legal residue: список СОХРАНЁННЫХ артистов, где letter-jump = навигация по МАЛЕНЬКОМУ собственному набору, и каждая строка несёт причинный тег («↳ открыл пост-панк», «↳ дослушал 12 треков») — мёртвая стена каталога становится **леджером роста модели** (BLUEPRINT §3).

**Профиль артиста/трека → HONESTY убивает vanity-счётчик.** `· 6 345 245 слушателей` — учебниковый anti-pattern (один 31-сек плей считается как суперфан); CUT и замена на поведенческий L1-чип про ТЕБЯ («★ дослушал до конца 3 раза», «играл по пятницам вечером») — никогда reach-число, никогда «тебе понравится». Lyrics → синк + tap-to-seek + честная behavioral-аннотация (вакантная пост-Genius «Behind the Lyrics»-полоса, привязана к реальному вектору трека через L2 «исправить причину»). «Станции по этому треку» регенерятся как ATTRIBUTE-seeded радио («станция по звучанию: 112 BPM · женский вокал · меланхолия»), НЕ popularity/collaborative-сетка, НЕ A-Z-дискография — «станции, не альбомы».

**Избранное → из bookmark-wall в ЛЕДЖЕР СИГНАЛОВ, построивших видимый вектор.** Per-item причинная строка «fed» («Молчат Дома → открыл пост-панк») = честная видимая версия того, что Apple/Yandex/YouTube делают невидимо (у всех лайк = скрытый training-сигнал; мы рендерим стрелку сигнал→эффект на экране). RADIO-NOT-CATALOG: секция никогда не становится A-Z-стеной обложек — это компактный type-фильтрованный леджер с главным глаголом «играть волну отсюда», не «открыть альбом». Новая интеракция «jump-to-cause»: тап по fed-строке подсвечивает соответствующий вектор-бар выше = замыкает петлю explain→edit (north-star).

---

## 5. Design-system reskin (blue-gradient → near-black flat)

Все 5 фреймов = СТАРАЯ эстетика (синий градиент). Целевое (BLUEPRINT §5, locked Holy-Grail):

| Что | Из (Figma-легаси) | В (locked система) |
|---|---|---|
| Фон | blue-gradient / cover-sampled glow | `#0B0C0F` near-black + radial-glow 12% `#5168FC` сверху |
| Акцент | cyan/violet/multi-stop | ОДИН `#5168FC` (или content-derived `--np-accent` от обложки); accent-текст ≤14px → `#8094ff` (AA 6.8:1) |
| Шрифт | (varies) | **Onest ONLY** |
| Обложки/тайлы | cover-photo glow + повёрнутые **900-вес** uppercase-подписи (`rotate(-90deg)`) | art-tint + монограмма (hue 218–253°, синяя семья); реал-фото где ассет есть в `assets/gorod-fm/`; **0 rotate, 0 scaleX, ≤700-вес, горизонтальные подписи** |
| Аватары | fetched-фото / градиент-плейсхолдеры | round (person: артист/DJ) / rounded-square (band/playlist) art-tint+монограмма |

**Конкретные правила-выноса (hard-gate перед commit):**
- **Vanity-числа OUT.** `· 6 345 245 слушателей` удалить с artist-line. Никаких «N слушателей/просмотров» нигде (сиблинг — «perceived-catalog» Медиатеки).
- **Collaborative-копи OUT.** «фанаты также слушают» / «for fans of Y» / СЕЙЧАС СЛУШАЮТ — запрещены везде (BANNED, AUDIT §4 «жутко»). Любое «почему» — behavioral («дослушал 3×»), не marketing, не collaborative.
- **Rotated 900-weight tile-labels OUT.** `.podborki-tile-label` (`rotate(-90deg) scaleX(1.05); font-weight:900; font-size:36px`) — тройное нарушение GDS-19. Не рестайлить — удалить вместе с тайлами.
- **Real photos OK, но tamed.** Реал-фото артиста в hero — да (честнее SVG-силуэта/монограммы), но в `#0B0C0F`-рамке, без cover-sampled glow, без градиент-ореола на обложке.
- **SVG-фейк-имагери OUT.** SVG-винил/стек-обложки `#/library`, SVG-дуги hero трека, ID-силуэт артиста — все → art-tint+монограмма или реал-фото.
- **Cyan-инвентарь:** уже в плане SPEC-00 §3 (119 вхождений). Этот документ НЕ дублирует ручной свап — `#/library`/`#/favorites`-cyan скрыт редиректом (отложен), `.podborki`-cyan **умирает при удалении галереи** (а не свапается). Демо-данные на ВСЕХ выживших — обязательный «демо-»-лейбл (perceived-transparency = смерть доверия).

---

## 6. Build order (с разрешением B1/B2)

> Этот порядок **встраивается в существующий BUILD ORDER из SPEC-00 §5** — не заменяет его. 5 секций распределены по уже-запланированным фазам. Дисциплина: **re-grep якоря перед каждым edit** (файл ~14.7k строк, дрейфует), `?v=N` cache-bust, зеркалить в `gorod-fm-standalone.html` (base64-inline → не доверять номерам строк, re-grep).

| Шаг | Что | Тип | Зависит от | Effort |
|---|---|---|---|---|
| **0** | (уже built) `GorodSaved`-аккордеон, `#/favorites`+`#/library` redirect — **Избранное+Медиатека residue уже ~90% есть** | done | — | — |
| **1** | **#/podborki: УДАЛИТЬ легаси-галерею** (B1/B2 resolved — см. ниже) | DELETE | Integrate-046 (additive-safe slice) | low |
| **2** | **#/artist + #/track REFRAME** (vanity-out, реал-фото, синк-lyrics, attribute-станции) | REPLACE-in-place | SPEC-00 Фаза-2 #4/#5 (track→artist), B1 TwinrModel | med→high |
| **3** | **«Сохранённое»: довести фильтр «Артисты»** (реал-фото-карточка + причинная строка + опц. letter-jump) | additive | SPEC-taste_saved built | low |
| **4** | **«Аккаунт» sheet (ЛК)** — новый sheet под `#/taste` (идентичность + 3-way тема + wedge-handoff + export/delete + Выйти) | new module | foundation, #/taste built | med |
| **5** | **jump-to-cause** в Сохранённом (тап fed-строки → flash вектор-бара) | additive | #/taste вектор | low |
| **6** | Integrate-A (nav-retire + redirect-слой) + Integrate-B (ручной cyan-свап) | per SPEC-00 §5 Фаза 3-4 | все экраны | low-med |

### Разрешение pending gallery-restyle (HANDOFF cont-12, B1/B2)

**Решение: НЕ рестайлить (ни Вариант 1, ни Вариант 2) — РЕТАЙР (удалить).**

Обоснование (синтез research «Подборки» + cont-12 контекст): любой рестайл всё равно оставляет **каталог-сетку**, которая воюет с radio-not-catalog. Вариант 1 (де-ротация, фото kept) чинит только GDS-19-нарушение, но сохраняет 9-рядный browse-хаб = тот самый паттерн, что Apple/Яндекс бросили. Вариант 2 (flatten под `.discover-ed-card`) **избыточен** — ряд «От редакции» УЖЕ существует (3 кураторские карточки), галерея его дублирует. Поэтому:

- **DELETE** `.podborki-gallery` (9 тайлов @~7875), `.podborki-chip-row` (@~7830), мёртвый `console.log`-фильтр-handler (@~11565), CSS `.podborki-tile*` (@4360–4441, включая rotated-900 `.podborki-tile-label` @4426).
- **DELETE** mobile/TV-overrides (@6567–6702) и mobile 2-row-restructure JS (@11599/@11654) — иначе бросят на отсутствующем `#podborki-gallery-desktop` (zero-console-errors gate).
- **KEEP** `.discover-editorial-row` («От редакции») — единственный выживший ряд.
- Чистое удаление (CSS+подписи+узлы) → если структура тайла не трогается частично, а удаляется целиком, dev/standalone расходятся минимально; **re-grep + зеркалить аккуратно**, standalone base64-фон уходит вместе с узлом.
- **Scope-note:** rename `#/podborki`→`#/discover` + redirect-половина = GATED GOROD-046 (решение Эльбика «сколько ломать легаси»). Удаление галереи = additive-safe slice, **делать отдельным edit'ом**, не форсить rename в том же.

---

## 7. Открытые решения для Эльбика

1. **GOROD-029 (позиционирование, gate).** Затрагивает: онбординг-eyebrow «ПЕРВЫЙ AI-МУЗЫКАЛЬНЫЙ СТРИМИНГ», тон копи «От редакции», hero-микрокопи артиста/трека, и силу CUT'а Медиатеки (если продукт когда-нибудь пивотит в «найди любого артиста в каталоге» — CUT слабеет). Пока тезис = «AI-радио, что объясняет+рулит» — все 5 вердиктов держатся. **Копи держать positioning-нейтральной до решения.**

2. **GOROD-030 (лицензирование, gate).** Затрагивает: (а) A-Z-каталог Медиатеки визуально обещает полноту, которую Stage-0/1 каталог честно не покрывает → ещё причина FOLD-не-browse; (б) реал-фото артиста (Артур Пирожков = мейджор-лейбл) и синк-lyrics требуют прав → в прототипе ТОЛЬКО демо-лейбл, один трек, ничего не намекать на full-catalog; (в) легал-доки в Аккаунт-sheet (Политика/Соглашение) + копи «данные, что мы держим» должны совпадать с реальностью продукта (honesty-wedge) — placeholder-legalese, который over/under-claim'ит = anti-fidelity-риск.

3. **Identity ownership (GOROD-029-adjacent).** Город ФМ владеет name/email/password, или идентичность живёт в shared **Twinr-ID / Большой-Цифровой**-аккаунте (как Яндекс Музыка делегирует Yandex ID)? Если shared — блок идентичности в Аккаунт-sheet становится тонким указателем «управляется в Twinr-ID →», и большинство Figma-полей профиля CUT. **Не строить bespoke auth-империю спекулятивно.**

4. **«Integrate» Медиатеки = FOLD, не ship-as-tab.** Эльбик явно просил ИНТЕГРИРОВАТЬ фрейм; ответ = CUT-scope + FOLD-residue (фото-карточка+letter-jump в «Сохранённое»), а НЕ standalone A-Z-страница. Нужен явный sign-off, что «интегрировать» = «свернуть в Сохранённое».

5. **Light-тема перед shipping 3-way контрола.** Приложение dark-first; полу-готовая светлая тема хуже её отсутствия. Подтвердить token-покрытие light-mode (см. `SPEC-gorod-fm-light-theme.md`) — иначе шипнуть «Тёмная + Как в системе», отложив «Светлая».

6. **Like-collision (BLUEPRINT §1.2).** Сердце теперь значит И «сохранить сущность» (Сохранённое) И «поднять волну» (TwinrWhy steer). Если оба пишут один like — архив и steering-сигнал конфлейтятся. Решить: сохранение = explicit/сильный like в архив, wave-heart = эфемерный steer? RENAME в «Сохранённое» частично смягчает, но два write-path надо специфицировать до бэкенда.

7. **Export/delete (ЛК) = пост-прототип бэкенд.** «Скачать мои данные»/«Удалить аккаунт» подразумевают реальный auth/persistence/GDPR-erasure, которых нет в single-file. В прототипе — ЧЕСТНЫЕ демо-affordances (export рендерит реальный localStorage-вектор; delete чистит local state с «демо-»-лейблом), никогда faked compliance. Флаг: реальное удаление/экспорт = пост-прототип.

---

**Файлы-источники (абсолютные):** `C:/Users/elbics/Desktop/design-project/designs/gorod-fm.html` (+ `gorod-fm-standalone.html`), `C:/Users/elbics/Desktop/design-project/docs/superpowers/BLUEPRINT-gorod-fm-full-service.md`, `.../specs/SPEC-00-foundation-and-integration.md`, `.../specs/SPEC-taste_saved.md`, `.../HANDOFF-gorod-fm-cont-12.md`. Этот блюпринт позволяет следующей build-сессии исполнять без пере-litigation IA: 3 таба, 0 новых роутов, ЛК=sheet, галерея=ретайр.

---

# §8. Adversarial review (критик) — ОБЯЗАТЕЛЬНЫЕ grounding-правки

VERDICT: **REVISE**

The blueprint's *thesis* (known→Мой вкус, unknown→Открыть, radio-not-catalog, ЛК=sheet not 4th tab) is correct and well-aligned with the locked specs and the north-star. But it is **stale against the live file in several load-bearing places**, and its single biggest concrete decision (RETIRE the gallery) is argued from a premise that is partly false. It would ship cleanly as *intent*, but several "required fixes" target ghosts while real violations go unmentioned. Fix the grounding before any of this is executed.

---

## Required fixes (problem → fix)

**1. The canonical vanity-counter it tells you to CUT no longer exists; the real one is on a surface it ignores.**
Problem: §3 + §5 make `· 6 345 245 слушателей` on `#/artist` the headline honesty-fix ("учебниковый anti-pattern, CUT"). The live file (@8442) already reads `Американский альт-рок · в твоей волне с весны` — behavioral, no count. The cont-12 audit confirms the same. Meanwhile the *actual* surviving vanity numbers — `4 832 слушателя`, `6 102 слушателя`, etc. (@8967–9002) — sit on `#/lives`, which the blueprint waves off as a flag-gated placeholder and never touches.
Fix: Delete the artist-counter task (already done). Re-point the §5 "vanity OUT" hard-gate at `#/lives` @8967–9002 (and the `103.5 FM · N слушателя` station-meta pattern) — either reskin those to behavioral/contextual lines or confirm `#/lives` is truly dev-gated and invisible-by-default before calling vanity "enforced." Right now the blueprint claims "никаких N слушателей нигде" while six live vanity strings ship.

**2. "СЕЙЧАС СЛУШАЮТ = collaborative, BANNED" — that block does not exist in the file.**
Problem: §3 and §6 list "СЕЙЧАС СЛУШАЮТ" among the things to DELETE from the gallery as a collaborative-signal violation. Grep returns **zero** matches for "слушают/сейчас слуша/фанаты также" anywhere in `gorod-fm.html`. The gallery tiles are genre/show labels (POP GOLD 2010s, K-POP, ДИСКАЧ 90-Х, DJ PITKIN…), not a "now listening" row.
Fix: Strike the "СЕЙЧАС СЛУШАЮТ" and "фанаты также" deletions from the gallery scope — they're phantom targets. Keep the collaborative-copy ban as a *standing rule* for new content, but stop attributing nonexistent nodes to the live file. This is the same fidelity sin the blueprint itself warns against ("нельзя продавать показанное=реальное, будучи неточным к прототипу").

**3. The "dead console.log filter" is alive and wired — and so is a duplicate-discovery problem the blueprint underplays.**
Problem: §6 calls the gallery's filter handler a "мёртвый `console.log`-фильтр (fake affordance)." It's not dead: @11565–11596 wires `#podborki-chip-row` chips and tile clicks with live listeners (they log, but they fire and are attached). More importantly, grep proves `.discover-editorial-row` (@7826, the new "От редакции") and the legacy `.podborki-gallery` (@7875) **already co-exist in the live DOM** — the discover spec was partially built on top of the legacy without removing it. That is exactly the Sonos triple-browse duplication the blueprint names as anti-pattern #1, and it's live *right now*, not hypothetical.
Fix: Reframe the gallery decision around the real state: "От редакции" is built and renders; the gallery is a genuine *duplicate discovery surface* below it. That strengthens the RETIRE call — but say so accurately (duplicate-surface, not "dead console.log"). And note the chip-row/tile JS (@11565–11596, @11599–11711) must be removed *with* the DOM or it will throw on the missing `#podborki-gallery-desktop`/`#podborki-chip-row` (the zero-console-errors gate from cont-12).

**4. Anchor line numbers are stale by ~900 lines — the build steps will hit wrong code.**
Problem: §6 cites `.podborki-gallery @~7875`, `chip-row @~7830`, `console.log @~11565`, CSS `.podborki-tile* @4360–4441`. Some happen to still match, but the blueprint elsewhere cites a "~14.7k-line" file while SPEC-00 was grounded at ~14.1k — the file has drifted, and the cont-12 handoff explicitly warns "анкеры дрейфуют — re-grep перед каждым edit, НЕ по номерам." The blueprint hands a build session hard line numbers anyway.
Fix: Replace every absolute line number in §6 with a grep-anchor (unique selector / class string), exactly as SPEC-00 §4.1 mandates for trailing-IIFE inserts. The DELETE list should key off `.podborki-gallery`, `.podborki-chip-row`, `.podborki-tile-label`, and the `getElementById('podborki-gallery-desktop')` JS block — not coordinates.

**5. The gallery decision quietly contradicts the two specs the blueprint claims to "продолжать."**
Problem: §6 declares "DELETE the gallery" as resolved. But SPEC-discover **C4 explicitly says** "Legacy chip-row/gallery НЕ трогаем … это отдельная IA-задача 046," and SPEC-00 §3.2-B lists the podborki cyan as "discover-спек оставляет legacy chip-row — НЕ умрут в v1." The blueprint asserts it "не противоречит SPEC-00" while overturning a binding C-resolution in two child specs. It also self-gates the rename under GOROD-046 but treats the deletion as ungated — yet deletion is the more destructive half.
Fix: Either (a) formally supersede SPEC-discover C4 / SPEC-00 §3.2-B with a one-line "CHANGED: gallery now RETIRE, not keep" and update both, or (b) demote the deletion to the same GOROD-046 gate as the rename. Don't claim continuity while silently reversing a locked decision — that's precisely the cross-spec drift SPEC-00 exists to prevent.

**6. ЛК "История/Приватная сессия" copy invents a behavioral consequence that isn't wired — a fidelity violation inside the honesty section.**
Problem: §4 prescribes copy: "Выключишь историю → волна перестаёт учиться … грань-карта `#/recap` не соберётся." In the prototype there is no history toggle and no learning loop — recap is gated on `hasRealSignal()` scripted state, not on a history switch. Shipping that sentence states a causal mechanism that does not exist = "perceived transparency," the exact death-of-trust the blueprint bans elsewhere.
Fix: For the prototype, the Аккаунт sheet must carry a "демо-" label and describe behavior in the conditional/future ("в полной версии: …") or omit the causal claim. Don't let the honesty pitch itself over-claim a mechanism. (Same applies to "Скачать мои данные рендерит точно тот вектор" — fine only if it literally reads `gorodfm_taste`/`gorodfm_rejected`; spec it as such or label it demo.)

**7. The like-collision is flagged but punted to "post-prototype backend" — it bites in the single-file prototype now.**
Problem: §7-item-6 correctly identifies that ❤ now means both "save to Сохранённое" and "raise the wave," then defers resolution to "до бэкенда." But `gorodfm_liked` is a live LS key (SPEC-00 §4.6) and Сохранённое reads/writes archive state client-side. If the heart writes one key for both meanings, the archive and the steering signal conflate *in the prototype*, corrupting the reason_tag ledger the whole wedge depends on.
Fix: Specify the two write-paths now (e.g., archive = explicit/long-press strong-save; wave-heart = ephemeral steer, distinct key or distinct `action` field in `logEvent`). This is a prototype-level data-model decision, not a backend one — it must precede building Сохранированное's "fed" ledger (§4), or the ledger shows fabricated causality.

**8. Under-integration: "А-Z letter-jump по своим артистам" is still a catalog reflex bolted onto the wedge.**
Problem: §3/§4 keep an optional letter-jump in Сохранённое "по СВОИМ сохранённым артистам." With a realistically small saved set (the spec's own mock counts are tens of items), an alphabetical index is catalog-think surviving in miniature — it adds a browse affordance to a surface whose whole point is the causal ledger ("что добавил в вкус"). It's the catalog mental-model leaking back in under a size limit.
Fix: Drop letter-jump from v1. Default the archive sort to **recency-of-signal or causal-impact** ("последнее, что сдвинуло вкус" / "сильнее всего повлияло"), which reinforces the ledger framing. Letter-jump only earns its place if a user's saved set crosses a threshold (hundreds) — and even then it's a utility, not a wedge feature; gate it as a follow-up, don't spec it as core.

---

## Strong ideas worth amplifying

**A. "Архив как причинный леджер роста модели," with jump-to-cause closing the loop.** Turning the dead bookmark-wall into per-item "fed" rows ("Молчат Дома → открыл пост-панк") and the tap-fed-row → flash-the-vector-bar interaction (§4, §6 step-5) is the single best idea here. It literally renders the explain→edit loop that the master blueprint §0 calls "the best service," on a surface every other streamer leaves as a black box. This is the wedge made tangible — build it, and make the flash bidirectional (tap a vector bar → highlight which saved signals built it).

**B. ЛК that *points at* transparency instead of duplicating it with toggles.** The reframe — settings as a thin sheet whose "персонализация" block is a deep-link to the visible/editable vector, not a parallel set of switches — is exactly right and resists the over-integration trap. It correctly identifies that a plain account utility (email, theme, logout) should stay plain (fixing fix #6's copy makes this fully sound). This is the rare case where the blueprint *doesn't* force the wedge where it doesn't belong.

**C. Editorial row with a mandatory human signature + honest "не по твоему вектору" note.** Keeping "От редакции" as the one survivor of the Подборки collapse, with "собрал Илья, редакция" + "по нашему вкусу, не твоему," is the only honest way to keep a curation surface without it becoming an algorithm-dupe. It's explainability-via-transparent-human — a genuinely distinct lane from the behavioral "почему," and it gives the discover tab a reason to exist beyond the map. Amplify by making the curator a real, returning persona (consistency builds the "human outside the algorithm" trust the §3-D6 note is reaching for).

Source files grounding this critique (absolute): `C:/Users/elbics/Desktop/design-project/designs/gorod-fm.html` (artist behavioral line @8442; live `#/lives` vanity counters @8967–9002; co-existing `.discover-editorial-row` @7826 + `.podborki-gallery` @7875; live gallery JS @11565–11711), `C:/Users/elbics/Desktop/design-project/docs/superpowers/BLUEPRINT-gorod-fm-full-service.md`, `.../specs/SPEC-00-foundation-and-integration.md` (§3.2-B, §4.1), `.../specs/SPEC-discover.md` (C4, C8), `.../specs/SPEC-taste_saved.md` (C1–C9), `.../HANDOFF-gorod-fm-cont-12.md` (gallery anchors drift, zero-console-errors gate).