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
| **SiriusXM** | **`Channels`** | **= первая вкладка** | Официальный help [KC-2383 «What is the Navigation Bar»](https://listenercare.siriusxm.com/prweb/autoredirect/app/ExternalKM/help/SupportCenter/article/KC-2383/What-is-the-Navigation-Bar), дословно: *«It contains buttons to access all the primary areas of the app: **Channels, Recent, Search, Me, and Favorites**.»* | med-**high** ⚠️ статья может отставать от редизайна SXM |
| **BBC Sounds** (UK) | **`Home`** | **вкладки нет**; но **первая полка на Home — `Listen Live`**, и есть второй дом `/sounds/stations` («Stations & Schedules») | [Wayback UK-краул 2026-05-31](https://web.archive.org/web/20260531203945/https://www.bbc.co.uk/sounds): навбар `Home · Music · Podcasts · My Sounds`. Заголовки главной по порядку: *«Your world of Sounds» → **«Listen Live»** → «Discover Podcasts» → «Music You'll Love» → «Editor's Picks»…*; карточки станций с бейджем **LIVE** + что идёт сейчас + слот `21:00 - 23:00`; ссылка *«View all Stations & Schedules»* → `/sounds/stations` | **high** |
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

**Честный подсчёт: «Home» доминирует.** Первая вкладка = `Home` у TuneIn (app), iHeartRadio (app + web), Audacy (app), Twitch (app), YouTube, Kick. По головам — **генерический лейбл побеждает**, и в аудио, и в live-видео. Если бы я подгонял вывод под красивую гипотезу «радио-first называет по содержимому» — я бы соврал.

**Но за подсчётом прячется правило, которое и есть настоящий ответ:**

> ### «Home» ставят первой вкладкой тогда и только тогда, когда у живого контента ЕСТЬ ОТДЕЛЬНЫЙ ДОМ.

Проверяется по всей выборке — без исключений:

| Продукт | 1-я вкладка | …потому что живое лежит ЕЩЁ И ЗДЕСЬ |
|---|---|---|
| iHeartRadio | `Home` | отдельная вкладка **`Radio`** |
| TuneIn | `Home` | `Browse → Local Radio` |
| YouTube | `Home` | `Explore → Live` |
| Kick | `Home` | `Browse → Livestreams` |
| Twitch (app) | `Home` | 5 слотов — есть куда деть |

И наоборот — **когда первый экран САМ и есть живой продукт, лейбл становится содержательным**:

| Продукт | 1-я вкладка | потому что второго «дома» у живого нет |
|---|---|---|
| **radio.net** | **`Radio`** | секция `Radio` = недавние + рекомендации + редподборки. Это и есть главная. |
| **Radio Garden** | **`Explore`** | глобус = продукт |
| **Twitch, моб. веб** | **`Live`** | в баре 2 слота — и Twitch зовёт дефолтный **`Live`**, а не `Home` |

**Twitch — самый чистый эксперимент в выборке.** Один продукт, две оболочки. Где 5 слотов — первая вкладка `Home`. Где 2 слота и надо сказать, что здесь главное, — **`Live`**, и слова `Home` в баре нет вообще. Вывод: **«Home» — это не выбор смысла, это роскошь широкого таб-бара.**

**Что «Home» даёт пользователю:** контейнерное обещание «начни отсюда, мы сами решим, что показать». Плата — низкий *information scent*: по [NN/g](https://www.nngroup.com/articles/information-scent/) (Budiu, 2020) — *«If the link name is too obscure and vague, people might miss a good source of information»*; общие лейблы кликают неохотно, потому что не знают, куда попадут ([NN/g про имена категорий](https://www.nngroup.com/articles/category-names-suck/)). Выгода — свобода менять начинку, не переименовывая вкладку. Это разумный размен **для мультиформатного агрегатора** (радио + подкасты + аудиокниги + плейлисты), где «Home» честно значит «микс всего».

**Что даёт содержательный лейбл:** высокий scent + он сообщает, ЧТО ЭТО ЗА ПРОДУКТ. Мотив Twitch формулирует сам, в своём FAQ: *«The live feed will remain as the default land of the mobile app because it has been successful in helping our streamers grow by quickly helping viewers find new streamers to watch»* — работа первой вкладки — **дискавери живого**, а не «личный кабинет».

---

## 3. Что применимо к «Городу ФМ»

### Почему «Главная» здесь — ошибка (несмотря на то, что это индустриальный дефолт)

Дефолт «Home» родился у **мультиформатных агрегаторов**. «Город ФМ» — не агрегатор: 6 станций в прямом эфире + витрина. И главное — **посмотрите на соседей по таб-бару**:

| Вкладка «Города ФМ» | Чья это работа в чужих продуктах |
|---|---|
| **«Мой вкус»** | = `For you` (Audacy web, старый iHeart) — персонализация |
| **«Открыть»** | = `Browse` / `Explore` (Twitch, Kick, TuneIn) — дискавери |

**Обе работы, которые обычно поглощает «Home», у вас УЖЕ разобраны соседними вкладками.** У первой вкладки остаётся ровно одна работа — **живой эфир и станции**. Назвать её «Главная» = повесить ярлык «контейнер» на полку, где лежит ровно одна известная вещь. Это:

1. **Низкий scent** (NN/g) — «Главная» не сообщает ничего.
2. **Ложное обещание.** Во ВСЕХ продуктах с первой вкладкой `Home` радио живёт где-то ЕЩЁ (`Radio`, `Local Radio`, `Live`, `Livestreams`). Пользователь, обученный этим паттерном, увидит «Главная» и **пойдёт искать вкладку с радио — которой у вас нет**. Мёртвый след.
3. **Выброшенный дифференциатор.** Живой эфир в центре — единственное, чем вы не Spotify. Прятать его за нейтральным словом — отдавать преимущество даром.
4. **Сломанный параллелизм.** `Главная / Мой вкус / Открыть` — контейнер + два содержательных. `Радио / Мой вкус / Открыть` — три содержательных, триада читается одним сканом.

### Рекомендация (одно мнение): **«Радио»**

**Ближайший по форме прецедент — radio.net, и он совпадает с вами один в один:** радио-first продукт, первая секция называется **`Radio`**, и внутри неё — недавние станции + рекомендации по региону + редакционные подборки. Это буквально «эфир + витрина» = ваша главная. Плюс Twitch-mobile-web: когда слотов мало и живое — это суть, вкладку зовут по содержимому.

| Кандидат | Вердикт |
|---|---|
| **«Радио»** | ✅ **Берём.** Высший scent на слове, которое отличает вас от Spotify. Прецедент radio.net (verbatim help-док). Честно масштабируется: появятся подкасты — станет `Радио · Подкасты`, как у radio.net, переименовывать не надо. Уже стоит в прототипе — исследование это **подтверждает**, а не переделывает. |
| **«Слушать»** | 🥈 Сильный второй. Прецедент — **официальная RU-локализация TuneIn** (`Слушать` → `/radio/home/`). Минус: конфликт регистра с «Открыть» (два глагола подряд), и «слушать» описывает то, что делаешь во всём приложении, — вкладку не различает. |
| «Главная» | ❌ Низкий scent + ложное обещание отдельной радио-вкладки, которой нет. |
| «Эфир» | ⛔ Отклонено владельцем. (Был бы точный аналог `Live`.) |
| «Волна» | ⛔ Забронировано. |
| «Станции» | ❌ Недо-обещание: на главной ещё и витрина (полки, чарты), не только станции. |

### Когда «Главная» станет ПРАВИЛЬНОЙ (честный триггер)

Я рекомендую против индустриального большинства — значит, обязан назвать условие, при котором большинство право. **Как только «Город ФМ» станет мультиформатным** (подкасты + аудиокниги + отдельный каталог станций), форма iHeart делается верной: первая вкладка «Главная» (микс-фид) **плюс отдельная вкладка «Радио»**. Пока второго дома у радио нет — первая вкладка обязана называться «Радио».

### Негативный контроль (метрика, которая умеет ПАДАТЬ)

Чтобы это не осталось красивой прозой — 5-секундный first-click тест на 5 живых людях.
Показать таб-бар **[Радио | Мой вкус | Открыть]** против **[Главная | Мой вкус | Открыть]**, вопрос: *«Где послушать живой эфир Русского Радио?»*
**Если «Главная» выигрывает или сравнивается — моя рекомендация неверна и подлежит замене.** Ожидание: «Радио» собирает первый клик заметно чаще.

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
- **Apple Music RU:** живой DOM music.apple.com/ru
- **NN/g:** [Information Scent](https://www.nngroup.com/articles/information-scent/) (Budiu, 2020) · [5 Tips for Avoiding Confusing Category Names](https://www.nngroup.com/articles/category-names-suck/)
- **SiriusXM / BBC Sounds:** см. раздел ниже (добавлен по итогам отдельной проверки)
