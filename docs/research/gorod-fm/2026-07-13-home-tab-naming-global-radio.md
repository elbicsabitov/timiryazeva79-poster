# Как называют первую вкладку в радио/live-audio продуктах

**Дата:** 2026-07-13
**Вопрос:** первая вкладка в радио-first продуктах — генерическая («Home») или по содержимому («Radio», «Live», «Listen»)?
**Контекст:** «Город ФМ» — радио-витрина РМГ. Центр главной = ЖИВОЙ ЭФИР (не плейлист). Соседи: «Мой вкус», «Открыть». «Волна» забронирована, «Эфир» отклонён владельцем. Интерфейс русский.

> **Метод / дисциплина источников.** Каждая подпись ниже прочитана из источника, открытого в этой сессии: живой DOM веб-приложения (через браузер, с self-check `location.href` в каждом чтении — чтения с несовпавшим URL отбрасывались), официальный help-центр, либо страница стора. Ничего не восстановлено по памяти. Где источник не найден — стоит **NOT VERIFIED**, а не правдоподобная догадка.

---

## 1. Таблица: подпись первой вкладки

| Продукт | Первая вкладка (verbatim) | Вкладка «живого» контента | Источник + что увидел | Confidence |
|---|---|---|---|---|
| **radio.net** (app) | **`Radio`** | та же — `Radio` и есть первая | [help-центр, «Introduction to the app»](https://radio.zendesk.com/hc/en-us/articles/226539568-Introduction-to-the-app) — дословно: *«The app is divided into five main sections: Radio, Podcast, Prime, Favorites, and Search.»* | **high** |
| **radio.net** (web) | **`Radio`** | та же | DOM главного меню radio.net: `Radio · Podcasts · Live sports · World Cup 2026 · Near you` | **high** |
| **TuneIn** (app) | **`Home`** | отдельно: `Browse` → **`Local Radio`** | [help «What is Home?»](https://help.tunein.com/en/support/solutions/articles/151000172073-what-is-home-): *«The Home section shows you content you've recently played…»*; [«What do the menu items under "Browse" mean?»](https://help.tunein.com/en/support/solutions/articles/151000172224-what-do-the-menu-items-under-browse-mean-) → `Premium Content, Local Radio, Trending, Music, Sports, News, Talk, Podcasts, By Location, By Language`; [Custom URL](https://help.tunein.com/en/support/solutions/articles/151000172207-what-is-a-custom-url-): *«go to the "Library" tab»* | **high** |
| **TuneIn** (web, EN) | **`Listen Now`** | она же | tunein.com, верхнее меню: `Listen Now · Audiobooks · Sports · Music · News & Talk · Podcasts` | **medium-high** |
| **TuneIn** (web, **RU-локализация**) | **«Слушать»** | она же | DOM tunein.com (ru): `Слушать` → href **`/radio/home/`**, далее `Аудиокниги · Спорт · Музыка · Новости и разговорное · Подкасты`. Т.е. официальная русская локализация «домашней» вкладки радио-продукта = глагол **«Слушать»**, не «Главная». | **high** |
| **Radio Garden** | **`Explore`** | она же (глобус = продукт) | Живой DOM + скриншот radio.garden: строка `Explore · Favorites · Browse · Search · Settings`; дефолтный экран — глобус, *«Press play to start Radio Garden»* | **high** |
| **Radioplayer (UK)** | **NOT VERIFIED** | NOT VERIFIED | radioplayer.co.uk — корпоративный сайт (`About · How to listen · Radio stations · For broadcasters · News`), не таб-бар приложения. В [App Store](https://apps.apple.com/gb/app/radioplayer-radio-podcast/id6443602613) подписи вкладок не названы (есть лишь оборот *«directly on the homepage»*). | **low** |
| **Apple Music** (RU) — *для контраста, streaming-first* | **«Главная»** | отдельная вкладка **«Радио»** | DOM music.apple.com/ru (`lang=ru`): `Поиск · Главная · Радио` | **high** |

<!-- PENDING: iHeartRadio, Audacy, SiriusXM, BBC Sounds, Twitch, YouTube, Kick -->

---

## 2. Паттерн сегмента

*(заполняется)*

## 3. Что применимо к «Городу ФМ»

*(заполняется)*
