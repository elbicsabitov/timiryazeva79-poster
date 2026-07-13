# Как называют ПЕРВУЮ ВКЛАДКУ в глобальных радио / live-audio продуктах

**Дата:** 2026-07-13
**Ключевой вопрос:** в радио-first продуктах первая вкладка называется генерически («Home») или по содержимому («Radio», «Live», «Listen»)?
**Контекст:** «Город ФМ» — радио-витрина РМГ. Центр главной = ЖИВОЙ ЭФИР (не плейлист). Соседи: «Мой вкус», «Открыть». «Волна» забронирована, «Эфир» отклонён владельцем. Интерфейс русский.

> **Дисциплина источников.** Каждая подпись ниже прочитана из источника, открытого в этой сессии: живой DOM (браузер, с self-check `location.href` в каждом чтении — чтения с несовпавшим URL отбрасывались), официальный help-центр, скриншот в сторе или Wayback-снимок. Ничего не восстановлено по памяти. Где источник не найден — стоит **NOT VERIFIED**, а не правдоподобная догадка.
>
> **Две ловушки, которые пришлось обойти** (иначе записали бы мусор):
> 1. **`iheart.com` из Казахстана отдаёт гео-урезанную оболочку** (`Your Library · Podcasts · News`) — живое радио гео-залочено на США. Наивный фетч даёт НЕ тот навбар. Обошли: Wayback US-краул + скриншоты US-стора.
> 2. **iHeart переделал веб-навигацию между апрелем и июлем 2026.** Знакомый сайдбар `For You / Live Radio / Artist Radio` — это **старый**, он уже заменён.
> 3. **`bbc.co.uk/sounds` из Казахстана редиректит на `bbc.com/audio`** — BBC Sounds доступен только из UK, а `bbc.com/audio` это ДРУГОЙ продукт с другой навигацией. Живой сайт как источник по BBC Sounds непригоден. Обошли: UK-краул Wayback.

---

## 1. Таблица: подпись первой вкладки

### Радио / live-audio

| Продукт | Первая вкладка (verbatim) | Где живёт ЖИВОЕ радио | Источник + что увидел | Conf. |
|---|---|---|---|---|
| **radio.net** | **`Radio`** | **= первая вкладка** | [help «Introduction to the app»](https://radio.zendesk.com/hc/en-us/articles/226539568-Introduction-to-the-app), дословно: *«The app is divided into five main sections: Radio, Podcast, Prime, Favorites, and Search.»* Секция `Radio` = недавние станции + рекомендации по региону + редподборки. Веб-меню: `Radio · Podcasts · Live sports · World Cup 2026 · Near you` | **high** |
| **Radio Garden** | **`Explore`** | **= первая вкладка** (глобус) | Живой DOM + скриншот radio.garden: `Explore · Favorites · Browse · Search · Settings`. Дефолт — глобус, *«Press play to start Radio Garden»* | **high** |
| **TuneIn** (app) | **`Home`** | отдельно: `Browse` → **`Local Radio`** | [«What is Home?»](https://help.tunein.com/en/support/solutions/articles/151000172073-what-is-home-); [«What do the menu items under "Browse" mean?»](https://help.tunein.com/en/support/solutions/articles/151000172224-what-do-the-menu-items-under-browse-mean-) → `Premium Content, Local Radio, Trending, …`; [Custom URL](https://help.tunein.com/en/support/solutions/articles/151000172207-what-is-a-custom-url-): *«go to the "Library" tab»* | **high** |
| **TuneIn** (web, EN) | `Listen Now` | она же | tunein.com: `Listen Now · Audiobooks · Sports · Music · News & Talk · Podcasts` | med-high |
| **TuneIn** (web, **RU-локализация**) | **«Слушать»** | она же | DOM tunein.com (ru): **«Слушать» → href `/radio/home/`**, далее `Аудиокниги · Спорт · Музыка · Новости и разговорное · Подкасты`. Официальная русская локализация «домашней» вкладки радио-продукта = **глагол**, не «Главная». | **high** |
| **iHeartRadio** (app) | **`Home`** | отдельная 3-я вкладка **`Radio`** | Скриншот US Google Play + iPad-скрин App Store: `Home · Search · Radio · Podcasts · Playlists` | **high** |
| **iHeartRadio** (web, текущий) | **`Home`** | отдельный пункт **`Radio`** (`/radio`) | [Wayback, US-краул 2026-07-09](https://web.archive.org/web/20260709123405id_/https://www.iheart.com/): `Home · Search · Radio · Podcasts · Playlists · Your Library`. `/radio/` = *«Listen to the Best Live Radio in the United States…»* | **high** |
| **iHeartRadio** (web, ≤апр 2026 — **устарело**) | `For You` | отдельный пункт **`Live Radio`** (`/live/`) | [Wayback 2026-04-01](https://web.archive.org/web/20260401001232id_/https://www.iheart.com/): `For You · Your Library · Live Radio · Podcasts · Artist Radio · …` | high |
| **Audacy** (app) | **`Home`** | **вкладки живого радио НЕТ** | Скриншот App Store: `Home · Search · My Audio`. Станции — внутри Home и в `Search → Stations` | **high** |
| **Audacy** (web) | **`For you`** | нет отдельной | Живой DOM audacy.com, прочитан **дважды двумя независимыми способами — сошлось**: `For you · Music · Podcasts · Sports · News` | **high** |
| **SiriusXM** (app, v7.29.2) | **`Discover`** | **отдельная 2-я вкладка `Channels`** — live-лайнап по номерам каналов | Скриншоты App Store `id317951436` (Card_10 = экран «Channels»: чипы `All/Music/Talk/Sports/In Library`, строки `CH 2 SiriusXM Hits 1`, `CH 3 Unwell Music`…). Бар: **`Discover · Channels · Search · Library`**. Help [«recently-played-channels»](https://www.siriusxm.com/help/recently-played-channels): *«select the Dog/"**Discover**" icon in the **bottom navigation**»*. Внутри Discover верхняя лента: `For You · Music · Talk & Podcasts · Sports · Howard` | **high** |
| ~~SiriusXM (по KC-2383)~~ | ~~`Channels`~~ | | ⚠️ **ОФИЦИАЛЬНЫЙ HELP-ДОК ОКАЗАЛСЯ ПРОТУХШИМ.** [KC-2383](https://listenercare.siriusxm.com/prweb/autoredirect/app/ExternalKM/help/SupportCenter/article/KC-2383/What-is-the-Navigation-Bar) описывает *«the **blue** bar… Channels, Recent, Search, **Me**, and **Favorites**»* — это **легаси-приложение** (KC-2439 подтверждает: Library заменил Favorites). Я на нём обжёгся; ловится только скриншотами. | **ОТВЕРГНУТО** |
| **BBC Sounds** (app) | **`Home`** | **вкладки нет.** На Home — круглый **station dial** с бейджем **LIVE** + кнопка «Stations & schedules» | Скриншоты App Store GB `id1380676511` (`04_iPhone_6.5inch_Browse.jpg` — Home подсвечен). Бар: **`Home · Explore · My Sounds · ⌕`**. Help: *«look through the content in the '**Explore**' tab»*; *«On the homepage, use the **station dial**…»* | **high** |
| **BBC Sounds** (web, UK) | **`Home`** | **вкладки нет**; **вторая `<h2>` на Home — `Listen Live`** + второй дом `/sounds/stations` | [Wayback UK-краул 2026-05-31](https://web.archive.org/web/20260531203945/https://www.bbc.co.uk/sounds): `<nav id="sounds-nav">` → `Home · Music · Podcasts · My Sounds`. Заголовки: *«Your world of Sounds» → **«Listen Live»** → «Discover Podcasts» → «Music You'll Love» → «Editor's Picks»…*; карточки с бейджем **LIVE** + что идёт сейчас + слот `21:00 - 23:00`. 🦴 **Ископаемое:** ссылка Home несёт атрибут `data-bbc-content-label="**listen**"` — когда-то вкладка была названа по содержимому и её **генерифицировали**. | **high** |
| **Radioplayer (UK)** | **NOT VERIFIED** | NOT VERIFIED | radioplayer.co.uk — корпоративный сайт (`About · How to listen · Radio stations · For broadcasters · News`), не таб-бар. В [App Store](https://apps.apple.com/gb/app/radioplayer-radio-podcast/id6443602613) вкладки не названы (лишь оборот *«directly on the homepage»*). Догадку не пишу. | **low** |
| *Apple Music (RU) — **контраст**, streaming-first* | **«Главная»** | **отдельная вкладка «Радио»** | DOM music.apple.com/ru (`lang=ru`): `Поиск · Главная · Радио` | **high** |

### Live-first НЕ из аудио (для сравнения)

| Продукт | Первая вкладка | Где живёт LIVE | Источник + что увидел | Conf. |
|---|---|---|---|---|
| **Twitch** (моб. приложение) | **`Home`** — открывается на **live discovery feed** | = Home | [help.twitch.tv «Twitch Mobile App»](https://help.twitch.tv/s/article/mobile?language=en_US): *«The app opens on the discovery feed»*; `Home · Browse · ➕ · Activity · Profile` | **high** |
| **Twitch** (**мобильный веб**) 🔥 | **`Live`** — дефолтная вкладка; **слова «Home» в баре НЕТ вообще** | = `Live` | m.twitch.tv @390×844: два `role="tab"`: `Following` → `/directory/following`; **`Live` → `/` с `aria-selected="true"`** | **high** |
| **Twitch** (веб) | `Browse` — единственный текстовый пункт | сайдбар-полка `Live Channels` | twitch.tv: `Home` существует только как `aria-label` логотипа | high |
| **YouTube** | **`Home`** | **`Live` — НЕ вкладка**, вложен в `Explore` | InnerTube guide API (`/youtubei/v1/guide`): сайдбар `Home · Shorts · Subscriptions … Explore{Music, **Live**, Gaming…}`; моб. таб-бар `Home · Shorts · Library` — вкладки Live нет | **high** |
| **Kick** | **`Home`** | `Browse` → **`Livestreams`** | [help.kick.com «A tour of the KICK homepage»](https://help.kick.com/en/articles/14994615-understanding-kick-com-s-homepage-and-finding-content): `1. Home → 2. Browse → 3. Following`; полка `Top Live Categories` | **high** |

> Оговорка: веб-наблюдения Twitch/Kick сделаны **разлогиненными** — отсутствие «Following» в вебе может быть артефактом.

---

## 2. Паттерн сегмента — и он НЕ тот, что кажется

> ⚠️ **ЭТОТ РАЗДЕЛ ПЕРЕПИСАН.** Первая версия правила («Home ⟺ у живого есть второй дом») была **опровергнута** собственными же данными: у Audacy и BBC Sounds первая вкладка `Home`, а отдельной вкладки для живого **нет вообще** — оно лежит ВНУТРИ Home. Правило подгоняло данные под красивый вывод. Ниже — версия, которая выдерживает всю выборку.

**Честный подсчёт: доминирует НЕЙТРАЛЬНЫЙ лейбл.**
`Home`: TuneIn (app), iHeartRadio (app+web), Audacy (app), BBC Sounds (app+web), Twitch (app), YouTube, Kick. `Discover`: SiriusXM.
Содержательный: **radio.net → `Radio`**, **Radio Garden → `Explore`**, **Twitch моб. веб → `Live`**, TuneIn web → `Listen Now`/«Слушать», Audacy web → `For you`.
Счёт примерно **8:5 в пользу нейтрального**. Гипотеза «радио-first зовёт первую вкладку по содержимому» — **неверна**.

**Но раскол не случайный. Настоящий разделитель — не «радио vs не-радио», а вот этот:**

> ### Вкладку называют нейтрально (`Home`/`Discover`/`For You`) тогда, когда её содержимое НЕЛЬЗЯ НАЗВАТЬ — потому что это алгоритмический МИКС РАЗНЫХ ФОРМАТОВ.
> ### Когда вкладка = одна конкретная поверхность контента, её называют по содержимому.

| Продукт | 1-я вкладка | Что на ней лежит | Формат продукта |
|---|---|---|---|
| TuneIn | `Home` | микс: recents + подкасты + рекомендации | радио + подкасты + аудиокниги + спорт |
| iHeartRadio | `Home` | микс | радио + подкасты + плейлисты + artist radio |
| **BBC Sounds** | `Home` | микс: Listen Live + Podcasts + Music + Editor's Picks | «**Music. Radio. Podcasts.**» + аудиокниги, спорт, новости |
| Audacy | `Home` | микс | радио + подкасты + спорт + новости |
| **SiriusXM** | `Discover` | микс (внутри лента `For You · Music · Talk & Podcasts · Sports · Howard`) | музыка + ток + подкасты + спорт |
| YouTube / Kick / Twitch (app) | `Home` | микс-фид | видео/стримы разных типов |

| Продукт | 1-я вкладка | Почему НАЗВАЛИ по содержимому |
|---|---|---|
| **radio.net** | **`Radio`** | таб-бар = таксономия ФОРМАТОВ (`Radio · Podcast · Prime · Favorites · Search`). Вкладка `Radio` — это радио-формат. |
| **Radio Garden** | **`Explore`** | продукт моноформатный: только живые станции |
| **Twitch, моб. веб** | **`Live`** | 2 слота — назвать нечем, кроме содержимого; `Home` в баре нет вообще |

### 🔑 Главное наблюдение, которое выдерживает ВСЮ выборку (0 исключений)

**radio.net — убийственный контрпример к «микс ⇒ Home».** Его секция `Radio` — это ТОЖЕ микс (дословно из help: *«recently played stations, recommendations based on your region, and editorial picks»*). Микс! И всё равно называется **`Radio`** — потому что микс идёт **внутри одного формата**. Вывод: **микс сам по себе не заставляет звать вкладку «Home». Заставляет только микс РАЗНЫХ ФОРМАТОВ.**

И второе, тоже без исключений:

> **Ни один продукт в выборке не прячет живое полностью.** Слово `Radio`/`Live`/`Channels`/`Stations` есть ВЕЗДЕ — вкладкой (`Radio` у iHeart, `Channels` у SiriusXM), пунктом 2-го уровня (`Local Radio`, `Livestreams`, `Explore → Live`) или **именованной полкой на главной** (`Listen Live` у BBC + круглый station dial с бейджем LIVE).

### 🦴 И ископаемое, которое рассказывает всю историю

У BBC ссылка `Home` до сих пор несёт аналитический атрибут **`data-bbc-content-label="listen"`**. То есть вкладка **когда-то называлась по содержимому — и её генерифицировали**, когда BBC разросся из радио в «Music. Radio. Podcasts. + аудиокниги + спорт».

**Генерификация — это следствие расширения ассортимента, а не стартовая позиция.** Сначала продукт называет вкладку тем, что он есть. «Home» он заслуживает потом — когда перестаёт быть одной вещью.

**Twitch — самый чистый эксперимент в выборке.** Один продукт, две оболочки. Где 5 слотов — первая вкладка `Home`. Где 2 слота и надо сказать, что здесь главное, — **`Live`**, и слова `Home` в баре нет вообще. Вывод: **«Home» — это не выбор смысла, это роскошь широкого таб-бара у мультиформатного продукта.**

**Что «Home» даёт пользователю:** контейнерное обещание «начни отсюда, мы сами решим, что показать». Плата — низкий *information scent*: по [NN/g](https://www.nngroup.com/articles/information-scent/) (Budiu, 2020) — *«If the link name is too obscure and vague, people might miss a good source of information»*; общие лейблы кликают неохотно, потому что не знают, куда попадут ([NN/g про имена категорий](https://www.nngroup.com/articles/category-names-suck/)). Выгода — свобода менять начинку, не переименовывая вкладку. Это разумный размен **для мультиформатного агрегатора** (радио + подкасты + аудиокниги + плейлисты), где «Home» честно значит «микс всего».

**Что даёт содержательный лейбл:** высокий scent + он сообщает, ЧТО ЭТО ЗА ПРОДУКТ. Мотив Twitch формулирует сам, в своём FAQ: *«The live feed will remain as the default land of the mobile app because it has been successful in helping our streamers grow by quickly helping viewers find new streamers to watch»* — работа первой вкладки — **дискавери живого**, а не «личный кабинет».

---

## 3. Что применимо к «Городу ФМ»

### Сначала — САМЫЙ СИЛЬНЫЙ ДОВОД ПРОТИВ меня

Честно: индустрия против «Радио», счёт 8:5. И главное — **BBC Sounds структурно почти вы** (живые станции + витрина + подборки), и он зовёт первую вкладку **`Home`**. Более того, ваша тройка ложится на его бар почти один в один:

| «Город ФМ» | BBC Sounds |
|---|---|
| **[?]** | `Home` (микс: Listen Live + полки) |
| «Мой вкус» | `My Sounds` |
| «Открыть» | `Explore` |

Если это отображение верно — **[?] = «Главная»**, и спор окончен. Этот довод надо разбить, а не обойти.

### Чем он разбивается

**Разница ровно одна, и она решающая: ассортимент.**
BBC — мультиформатный: *«Music. Radio. Podcasts.»* + аудиокниги + спорт + новости (это его собственный слоган и его собственные сабтабы в `Explore`). **Его `Home` нельзя назвать содержимым — потому что содержимого там 6 разных сортов.** Ни одно слово их не покрывает. «Home» там — не выбор, а вынужденность.

**У «Города ФМ» на первой вкладке лежит РОВНО ОДИН сорт: радио и музыка.** Никаких подкастов, аудиокниг, спорта, ток-шоу. Слово, покрывающее всё содержимое, **существует** — и это «Радио».

**А что микс (эфир + полки витрины)? Микс не мешает** — и это доказано:
> **radio.net.** Его секция называется **`Radio`**, а внутри неё, дословно из help-дока: *«recently played stations, recommendations based on your region, and editorial picks»*. Недавние + рекомендации + редподборки — **это ТОТ ЖЕ микс, что у вас** (эфир + витрина). И он всё равно **`Radio`**.

Микс внутри одного формата → зовётся по формату. Микс разных форматов → зовётся `Home`. Вы — первый случай.

**И ископаемое BBC добивает:** их `Home` до сих пор носит `data-bbc-content-label="**listen**"` — вкладка была содержательной и **генерифицировалась при расширении ассортимента**. BBC пришёл к «Home» — он с него не начинал. Копировать его конечную точку, не пройдя его путь, — карго-культ.

### Остальные аргументы (после того, как главный довод разобран)

1. **Низкий scent** (NN/g) — «Главная» не сообщает ничего, а вы — новый бренд, которому нужно СКАЗАТЬ, что он живое радио, а не очередной плейлист-апп. У BBC такой проблемы нет: за 100 лет никто не путается, есть ли у BBC радио.
2. **Выброшенный дифференциатор.** Живой эфир в центре — единственное, чем вы не Spotify. Лейбл вкладки — самое дешёвое место это заявить.
3. **Сломанный параллелизм.** `Главная / Мой вкус / Открыть` — контейнер + два содержательных. `Радио / Мой вкус / Открыть` — три содержательных, триада читается одним сканом.
4. **Узкий бар.** У вас 3 слота. Twitch на 5 слотах пишет `Home`, на 2 слотах — **`Live`**. «Home» — роскошь широкого бара.

### Рекомендация (одно мнение): **«Радио»**

| Кандидат | Вердикт |
|---|---|
| **«Радио»** | ✅ **Берём.** Высший scent на слове, которое отличает вас от Spotify. Прецедент radio.net (verbatim help-док). Честно масштабируется: появятся подкасты — станет `Радио · Подкасты`, как у radio.net, переименовывать не надо. Уже стоит в прототипе — исследование это **подтверждает**, а не переделывает. |
| **«Слушать»** | 🥈 Сильный второй. Прецедент — **официальная RU-локализация TuneIn** (`Слушать` → `/radio/home/`). Минус: конфликт регистра с «Открыть» (два глагола подряд), и «слушать» описывает то, что делаешь во всём приложении, — вкладку не различает. |
| «Главная» | ❌ Низкий scent. Оправдана ТОЛЬКО когда на вкладке микс РАЗНЫХ форматов (BBC, iHeart, SiriusXM) — у вас один формат, и слово для него есть. Плюс: вы новый бренд, вам надо СКАЗАТЬ, что вы живое радио. |
| «Эфир» | ⛔ Отклонено владельцем. (Был бы точный аналог `Live`.) |
| «Волна» | ⛔ Забронировано. |
| «Станции» | ❌ Недо-обещание: на главной ещё и витрина (полки, чарты), не только станции. |

### Бонус: у BBC и SiriusXM надо украсть ПОЛКУ, а не вкладку

Оба — мультиформатные, оба оставили нейтральную первую вкладку, **и оба всё равно вынесли живое в ИМЕНОВАННУЮ поверхность:**
- **BBC Sounds:** первая полка на Home — **`Listen Live`** (вторая `<h2>` страницы, выше подкастов и музыки); карточка станции = бейдж **LIVE** + что играет сейчас + слот `21:00 - 23:00`; в приложении — круглый **station dial** с бейджем LIVE.
- **SiriusXM:** отдельная вкладка **`Channels`** — лайв-лайнап по номерам каналов.

Для «Города ФМ»: **вкладка «Радио» + первая полка «В эфире сейчас»** — бейдж «В ЭФИРЕ», текущий трек/шоу, слот времени. Два уровня сигнала «живое»: в лейбле вкладки и в шапке героя. Слово «эфир» отклонено как имя ВКЛАДКИ — но в заголовке полки и на бейдже карточки оно работает и ни с чем не конфликтует.

### Когда «Главная» станет ПРАВИЛЬНОЙ (честный триггер)

Я рекомендую против индустриального большинства (8:5) — значит, обязан назвать условие, при котором большинство право, и оно точное:

> **Как только на первой вкладке окажется микс РАЗНЫХ ФОРМАТОВ** (подкасты / аудиокниги / спорт / ток), — назвать её одним содержательным словом станет невозможно, и «Главная» станет верной. Тогда форма iHeart/SiriusXM: **«Главная» (микс-фид) + отдельная вкладка «Радио»**.

Ровно этот путь прошёл BBC: `listen` → `Home`. **Но он прошёл его ПОСЛЕ расширения, а не до.** Пока «Город ФМ» — это радио и музыка, вкладка обязана называться «Радио».

### Негативный контроль (метрика, которая умеет ПАДАТЬ)

Чтобы это не осталось красивой прозой — 5-секундный first-click тест на 5 живых людях.
Показать таб-бар **[Радио | Мой вкус | Открыть]** против **[Главная | Мой вкус | Открыть]**, вопрос: *«Где послушать живой эфир Русского Радио?»*
**Если «Главная» выигрывает или сравнивается — моя рекомендация неверна и подлежит замене.** Ожидание: «Радио» собирает первый клик заметно чаще.

---

## 4. Методологические ловушки (переиспользовать в след. ресёрчах)

Из 11 продуктов **четыре** нельзя прочитать наивно. Каждая ловушка отдаёт **правдоподобный, но неверный** ответ — то есть молча портит вывод.

| # | Ловушка | Что отдаёт наивный метод | Как ловить |
|---|---|---|---|
| 1 | **Гео-редирект `iheart.com`** | из KZ: `Your Library · Podcasts · News` — подкаст-оболочка вместо US-навбара | Wayback US-краул; скриншоты US-стора |
| 2 | **Гео-редирект `bbc.co.uk/sounds`** | из KZ: редирект на `bbc.com/audio` — **другой продукт** с другой навигацией | Wayback UK-краул; `curl` без JS отдаёт настоящий UK-HTML |
| 3 | 🔥 **ПРОТУХШИЙ ОФИЦИАЛЬНЫЙ HELP-ДОК** | SiriusXM KC-2383 («the **blue** bar… `Channels, Recent, Search, Me, Favorites`») — это **легаси-приложение**. Я на нём **обжёгся и опубликовал неверную строку.** | Официальность ≠ актуальность. **Проверять help-док скриншотом стора** (там дата обновления билда) |
| 4 | **Скрейп картинок с Google Play** | со страницы SiriusXM прилетают скриншоты **Pandora и iHeart** — Play подмешивает «related apps» | Тянуть только из App Store по `id`; глазами смотреть, что на картинке тот самый продукт |

**Урок №3 — главный.** Официальный help-центр вендора выглядит как источник высшей пробы, и именно поэтому его не перепроверяют. Он **отставал от продукта на целый редизайн**. Единственное, что его поймало, — независимая проверка скриншотами. Правило на будущее: **подпись вкладки считается подтверждённой, только если её видно на пикселях; help-док — вторичное подтверждение, не первичное.**

---

## Источники (все открыты 2026-07-13)

- **radio.net:** https://radio.zendesk.com/hc/en-us/articles/226539568-Introduction-to-the-app · живой DOM radio.net
- **TuneIn:** [What is Home?](https://help.tunein.com/en/support/solutions/articles/151000172073-what-is-home-) · [Browse](https://help.tunein.com/en/support/solutions/articles/151000172224-what-do-the-menu-items-under-browse-mean-) · [Custom URL](https://help.tunein.com/en/support/solutions/articles/151000172207-what-is-a-custom-url-) · живой DOM tunein.com (EN + RU)
- **iHeart:** Wayback US [2026-07-09](https://web.archive.org/web/20260709123405id_/https://www.iheart.com/) · [2026-04-01](https://web.archive.org/web/20260401001232id_/https://www.iheart.com/) · скриншоты US Google Play / App Store
- **Audacy:** живой DOM audacy.com · [App Store](https://apps.apple.com/us/app/audacy-radio-sports-talk/id323701765) · [support.audacy.com](https://support.audacy.com/hc/en-us/articles/39574866804123-How-can-I-share-my-location-with-the-Audacy-app)
- **Radio Garden:** живой DOM + скриншот radio.garden
- **Twitch:** [help.twitch.tv/s/article/mobile](https://help.twitch.tv/s/article/mobile?language=en_US) · живой DOM twitch.tv + m.twitch.tv
- **YouTube:** InnerTube `/youtubei/v1/guide` · [support.google.com/youtube/answer/2398242](https://support.google.com/youtube/answer/2398242)
- **Kick:** [help.kick.com — tour of the homepage](https://help.kick.com/en/articles/14994615-understanding-kick-com-s-homepage-and-finding-content) · живой DOM kick.com
- **SiriusXM:** скриншоты App Store `id317951436` (Card_10 = экран Channels) · [help «recently-played-channels»](https://www.siriusxm.com/help/recently-played-channels) · KC-2437. ⚠️ **KC-2383 — ПРОТУХШИЙ, не использовать.**
- **BBC Sounds:** скриншоты App Store GB `id1380676511` · [Wayback UK-краул 2026-05-31](https://web.archive.org/web/20260531203945/https://www.bbc.co.uk/sounds) (живой сайт из KZ редиректит на bbc.com/audio — непригоден)
- **Apple Music RU:** живой DOM music.apple.com/ru
- **NN/g:** [Information Scent](https://www.nngroup.com/articles/information-scent/) (Budiu, 2020) · [5 Tips for Avoiding Confusing Category Names](https://www.nngroup.com/articles/category-names-suck/)
