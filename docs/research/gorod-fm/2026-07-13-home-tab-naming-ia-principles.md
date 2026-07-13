# Именование первой вкладки навигации — принципы и решение

**Проект:** Город ФМ (RU-интерфейс, рынок Москва) — радио-витрина холдинга РМГ
**Дата:** 2026-07-13
**Задача:** выбрать подпись первой вкладки в IA из трёх: `[?]` / «Мой вкус» / «Открыть»
**Кандидаты:** «Главная», «Радио», «Слушать», «Сейчас», «Дом», «Обзор»
**Ограничения:** «Волна» забронирована под будущую «Моя волна» (AI); «Эфир» отклонён владельцем

---

## 0. Дисциплина источников

Каждый тезис ниже опирается на страницу, которую я **открыл**. Цитаты — дословные.
Там, где я не нашёл подтверждения, я это прямо пишу. Раздел «Чего я НЕ нашёл» (§7) — обязателен к прочтению: он показывает, где мнение опирается на конвенцию, а не на замер.

---

## 1. Что говорят исследования: генерическая подпись vs содержательная

### 1.1. Общее правило для КАТЕГОРИЙ: содержательность побеждает

NN/g, [Menu-Design Checklist: 17 UX Guidelines](https://www.nngroup.com/articles/menu-design/) (Page Laubheimer, 7 июня 2024), Guideline 7 «Use Clear, Specific, and Familiar Wording for Link Labels»:

> «Figure out what users are looking for and use category labels that are familiar and relevant.»
> «Menus are **not** the place to get cute with made-up words, internal jargon, or abstract high-level categorization.»
> «Stick to terminology that clearly describes your content, features, or resources.»

NN/g, [5 Tips for Avoiding Confusing Category Names](https://www.nngroup.com/articles/category-names-suck/) (Hoa Loranger, Taylor Dykes; 15.12.2013, обновлено 11.10.2024). Пять правил дословно:

1. «Be Descriptive and Relatable»
2. «Avoid Made-Up Terms»
3. «Check for Overlapping Categories»
4. «Categorize Based on Users' Mental Models»
5. «Don't Rely on Instincts»

> «Descriptive category names that people understand are better than made-up words or internal jargon.»

И ключевое наблюдение про слабый запах:

> Пользователи «skip a category name with weak information scent, even though that link leads to the item they are looking for».

NN/g, [3 Common IA Mistakes (that Are All Due to Low Information Scent)](https://www.nngroup.com/articles/3-ia-mistakes/) (Page Laubheimer, 16.04.2023):

> «Vague verbs (such as *Explore, Discover, Learn, Partner*, etc.) are not effective category names.»
> «The link label must give users a clear sense of what they're going to find when clicking.»
> Пользователи «won't click on a category unless it's clear where they will go, *before* they click»; многие «ignore vague link names entirely».

**Промежуточный вывод:** для КАТЕГОРИИ, конкурирующей за клик среди равных, — содержательность обязательна, а вагоны-глаголы (Explore/Discover) прямо запрещены.

### 1.2. НО первая вкладка — не категория. Это якорь ориентации

Это принципиальный разрыв, который и решает наш спор.

NN/g, [Homepage Links Remain a Necessity](https://www.nngroup.com/articles/homepage-links/) (Hoa Loranger, 23.07.2017, обновлено 25.10.2024):

> «In general, it's best to name the link to a website's homepage *Home*.»

То есть NN/g — те же самые люди, что требуют содержательности от категорий — для домашней ссылки **явно рекомендуют генерическое слово**. Противоречия нет: у «Home» другая работа.

NN/g, [Homepage Design: 5 Fundamental Principles](https://www.nngroup.com/articles/homepage-design-principles/) (Huei-Hsin Wang, 15.03.2024):

> «People commonly rely on the homepage to orient themselves, even when they arrive at an interior page via a search engine.»
> «The homepage is often considered the "front door" of a website, serving as a primary entry point and a vital anchor for visitors.»

Работа «Home» — **ориентация и сброс** («я потерялся → верни меня в начало»), а не «пообещай мне конкретный контент». Поэтому к ней применяется другой критерий: **узнаваемость конвенции**, а не информационный запах.

### 1.3. Конвенция как источник правоты

NN/g, [Jakob's Law of Internet User Experience](https://www.nngroup.com/videos/jakobs-law-internet-ux/):

> «Users spend most of their time on other sites. This means that users prefer your site to work the same way as all the other sites they already know.»
> «Design for patterns for which users are accustomed.»

NN/g, [Maintain Consistency and Adhere to Standards (Usability Heuristic #4)](https://www.nngroup.com/articles/consistency-and-standards/) (Rachel Krause, 10.01.2021):

> «Users should not have to wonder whether different words, situations, or actions mean the same thing. **Follow platform and industry conventions.**»
> «**External consistency** refers to established conventions in an industry or on the web at large, beyond one application or family of applications.»

Microsoft, [Navigation basics for Windows apps](https://learn.microsoft.com/en-us/windows/apps/design/basics/navigation-basics) (обн. 2026-06-27):

> «**Consistency:** Meet user expectations.»
> «Navigation should be consistent with user expectations. Using standard controls that users are familiar with and **following standard conventions** for icons, location, and styling will make navigation predictable and intuitive for users.»

**Итого по вопросу 1:** генерическая подпись работает **ровно в одном месте** — в слоте домашней/первой вкладки, и работает она *за счёт конвенции*, а не за счёт запаха. Во всех остальных слотах побеждает содержательность. Наши три вкладки: слот 1 = якорь (конвенция), слоты 2–3 = категории (содержательность). Это разные правила, и смешивать их — ошибка.

---

## 2. «Ярлык отвечает на вопрос "что я здесь найду"» — как применить к вкладке, где и эфир, и витрина

Правило верное, но у него есть **носитель**. Запах может нести (а) подпись, (б) иконка, (в) первый экран. NN/g явно допускает перенос нагрузки на визуал.

NN/g, [Menu-Design Checklist](https://www.nngroup.com/articles/menu-design/), Guideline 10:

> «Images, icons, and limited use of color may help with comprehension… of unfamiliar options and aid scannability.»

NN/g, [Icon Usability](https://www.nngroup.com/articles/icon-usability/) (Aurora Harley, 27.07.2014):

> «To help overcome the ambiguity that almost all icons face, **a text label must be present alongside an icon** to clarify its meaning in that particular context.»
> «Icon labels should be visible at all times, without any interaction from the user.»

Apple HIG, [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) (получено через `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/tab-bars.json`):

> «**Include tab labels to help with navigation.** A tab label appears beneath or beside a tab bar icon, and can aid navigation by **clearly describing the type of content or functionality the tab contains**.»

NN/g, [Homepage Design: 5 Fundamental Principles](https://www.nngroup.com/articles/homepage-design-principles/) — принцип 3 дословно: «**Reveal Content Through Examples**».

**Разрешение парадокса «эфир + витрина»:**
Одно слово физически не может пообещать И живой эфир, И жанры/чарты/подборки/редакцию/исполнителей. Любая попытка — либо ложь (сужает: «Радио», «Сейчас»), либо пустота («Главная»). Поэтому:

> **Запах переносится с ПОДПИСИ на ПЕРВЫЙ ЭКРАН и ИКОНКУ.**
> Подпись = якорь. Иконка = домен («это радио»). Первый экран = обещание («6 станций в эфире» блоком №1, витрина ниже).

Это не отговорка — это ровно то, что предписывает принцип «Reveal Content Through Examples». Пользователь узнаёт, что там эфир *и* витрина, за 0,5 сек после открытия, а не из семи букв в подписи.

---

## 3. Русская локализация: «Главная» — конвенция или миф?

Я искал **исследования** по RU-локали и не нашёл (см. §7). Поэтому ниже — **проверенные факты конвенции**: что реально написано в интерфейсах, которые формируют привычку москвича.

### 3.1. Яндекс Музыка — «Главное» (проверено дословно)

Яндекс, [инструкция Яндекс Музыки на Android для незрячих](https://inclusion.yandex.ru/tutorials/music-android) — это официальный текст Яндекса, перечисляющий таб-бар как его читает скринридер:

> «"Главное", вкладка 1 из 4. "Подкасты и книги", вкладка 2 из 4. "Детям", вкладка 3 из 4. "Коллекция", вкладка 4 из 4.»

Яндекс, [инструкция для веба](https://inclusion.yandex.ru/tutorials/music-web) — тот же набор:

> «По щелчку. Текущая страница. Ссылка "Главное"» → далее «Подкасты и книги», «Детям», «Коллекция».

**Три вывода, критичных для нас:**
1. Крупнейший RU-музсервис ставит на слот 1 **генерическое** «Главное». Не «Музыка», не «Слушать».
2. В его основной навигации **нет вкладки «Радио»** вообще.
3. **«Моя волна» — НЕ вкладка**, а фича внутри главного экрана: [Яндекс, «Моя волна»](https://yandex.ru/support/music/ru/new-library/my-wave) описывает её как рекомендательный продукт, отображаемый «цветными интерактивными волнами» на главном экране; там же появился раздел «Что послушать» — «персональная музыкальная витрина».

Пункт 3 — прямая подсказка нам: **«Моя волна» отлично живёт внутри первой вкладки**, а не отнимает слот.

### 3.2. Apple Music RU — «Главная» (проверено, средняя надёжность)

[Руководство пользователя Apple Music (ru-ru)](https://support.apple.com/ru-ru/guide/music-web/welcome/web): в скриншотах интерфейса руководства фигурируют вкладки «**Главная**» и «**Медиатека**».
⚠️ Честная оговорка: это извлечено из скриншотов/оглавления руководства, а не из строки-инструкции вида «коснитесь "Главная"». Надёжность — средняя, но согласуется с §3.1.

### 3.3. Что это даёт

В RU-локали конвенция первой вкладки — кластер «**Главная / Главное**». Обе формы засвидетельствованы: Apple → «Главная», Яндекс → «Главное».
Для Города ФМ рекомендую «**Главная**» (согласование с «вкладка/страница»; форма Apple; шире распространена).
«**Дом**» — калька, не конвенция: в русском «дом» = здание/жильё, а не «домашний экран». Ни в одном из проверенных RU-интерфейсов я его не встретил.

---

## 4. Риск семантического пересечения — главный аргумент против «Радио»

### 4.1. Правило

NN/g, [5 Tips…](https://www.nngroup.com/articles/category-names-suck/), правило №3 дословно: «**Check for Overlapping Categories**».

Microsoft, [Navigation basics](https://learn.microsoft.com/en-us/windows/apps/design/basics/navigation-basics) — плоскую структуру верхнего уровня рекомендуют, когда:

> «The pages are **clearly distinct from each other** and don't have an obvious parent/child relationship.»

### 4.2. Замер: как индустрия УЖЕ научила пользователя читать слово «Радио»

Apple, [Play Apple Music radio in Apple Music on Windows](https://support.apple.com/guide/music-windows/play-apple-music-radio-mus0456fe22c/windows). Разделы боковой навигации Apple Music: **Home, Library, Radio, Search**. Инструкция дословно:

> «Select **Radio** in the sidebar.»

Что лежит в Radio — дословно:

> «Apple Music features six world-class radio stations (Apple Music 1, Apple Music Hits, Apple Music Country, Apple Music Club, Apple Música Uno, and Apple Music Chill), as well as a collection of stations based on different genres.»

**Это и есть прибор.** Apple — самый растиражированный музыкальный интерфейс в мире — держит **«Home» и «Radio» СОСЕДЯМИ**, где «Radio» = *только станции/эфир*, а вся витрина (новинки, чарты, жанры, редакция) живёт в других вкладках. У пользователя уже установлена модель:

> **Радио ⊂ музыкальное приложение**, а не **Радио ⊇ музыкальная витрина**.

Значит, назвав первую вкладку «Радио», мы просим пользователя вывернуть наизнанку модель, которую ему поставила Apple (а также вся категория «музыкальных» приложений). Он прочитает «Радио» как «6 станций в прямом эфире» и **не пойдёт туда за жанрами, чартами, подборками и исполнителями** — а они там. Это классический промах запаха из [3 Common IA Mistakes](https://www.nngroup.com/articles/3-ia-mistakes/): пользователи «won't click on a category unless it's clear where they will go».

⚠️ Тонкость: у нас продукт **радио**-витрина, а не музыкальный сервис с радио-разделом. Аргумент «у нас Радио = всё» логичен со стороны бизнеса. Но IA проектируется под установленную модель пользователя, а не под оргструктуру. Это ровно то, от чего предостерегает правило №4 «Categorize Based on Users' Mental Models».

### 4.3. Симметричный риск: «Главная» пустая

Да, «Главная» ничего не обещает. NN/g про генерические термины: слабый запах → пропуск.
**Но:** этот риск действует, только когда ярлык *конкурирует за клик*. Первая вкладка **не конкурирует**: она открыта по умолчанию. Пользователь попадает на неё, не выбирая. Значит, цена «пустоты» ≈ 0 при входе, и остаётся только польза — узнаваемый якорь «вернуться в начало».

Асимметрия решает спор:
- **«Главная»** пустая → но её всё равно откроют (она дефолтная) → пустота компенсируется первым экраном.
- **«Радио»** сужающая → её тоже откроют (она дефолтная), **но** остальные две вкладки («Мой вкус», «Открыть») перетянут на себя ожидание «музыка/витрина», и пользователь, ища жанры и чарты, **уйдёт из первой вкладки искать их в других** — и не найдёт. Ошибка ложится на витрину, а витрина — наш основной актив.

**Цена ошибки «Главная» — ноль. Цена ошибки «Радио» — спрятанная витрина.**

### 4.4. «Обзор» и «Слушать» — почему выбывают

- «**Обзор**» = Browse. Прямо пересекается с третьей вкладкой «**Открыть**» (Discover). Две из трёх вкладок означали бы примерно одно («полистать чужое»). Нарушает правило №3 (Overlapping Categories) и MS-требование «clearly distinct from each other». Плюс «Обзор» — из семьи, которую NN/g маркирует как вагон-глаголы (*Explore/Discover*).
- «**Слушать**» = глагол. Не различает: слушать можно во **всех трёх** вкладках, запах нулевой. Плюс Apple HIG, [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars): «**Use a tab bar to support navigation, not to provide actions.**» Глагол в таб-баре читается как действие.
- «**Сейчас**» — обещает временнóе («что идёт прямо сейчас») ⇒ то же сужение, что и «Радио», только слабее и без конвенции. Худшее из двух миров: и сужает, и незнакомо.

### 4.5. Про параллелизм — его НЕ требуется соблюдать

Соблазн: «раз "Открыть" — глагол, пусть и первая будет глаголом ("Слушать")». NN/g, [3 Common IA Mistakes](https://www.nngroup.com/articles/3-ia-mistakes/), ошибка №2 «Forced Parallel Language»:

> «Parallel language is **not** necessary for a usable, understandable information architecture.»

Значит связка «**Главная** / **Мой вкус** / **Открыть**» (прилагательное-субстантив / существительное / глагол) — **легальна**. Не ломайте IA ради грамматической симметрии.

---

## 5. Форма подписи: что предписывают HIG / Material / MS

| Источник | Дословно | Следствие |
|---|---|---|
| Apple HIG, [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) | «Include tab labels… **Use single words whenever possible.**» | 1 слово. «Главная» ✅ |
| Apple HIG, там же | «**Use a tab bar to support navigation, not to provide actions.**» | Существительное > глагол. «Слушать» ❌ |
| Apple HIG, там же | «Use the appropriate number of tabs… it's generally easier to navigate among **fewer tabs**.» | 3 вкладки — ок |
| NN/g, [Tabs, Used Right](https://www.nngroup.com/articles/tabs-used-right/) (Evan Sunwall, 02.08.2024) | «Tab labels should usually be **1-2 words**. Short labels are more scannable; if you need longer labels, it's a sign that the choices are too complicated for tabs.» | «Мой вкус» (2 слова) — на границе, ок |
| Material / Android, [Navigation bar (Compose)](https://developer.android.com/develop/ui/compose/components/navigation-bar) | «**Three to five destinations of equal importance**»; параметр `label`: «Displays text within the item. **Optional.**» | 3 вкладки ✅; «equal importance» ⚠️ см. §6 |
| Material Components Android, [BottomNavigation.md](https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/BottomNavigation.md) | «Navigation bars can have three to five destinations.»; `app:labelMaxLines` по умолчанию `1` | Подпись в одну строку, без переносов |
| NN/g, [Basic Patterns for Mobile Navigation](https://www.nngroup.com/articles/mobile-navigation-patterns/) (Raluca Budiu, 15.11.2015) | «Note that the icons are **labeled**… a recommended best practice in most cases.»; «If your site has more than 5 options, it's hard to fit them in a tab or navigation bar and still keep an optimum touch-target size.» | Иконка + подпись обязательно |
| NN/g, [Icon Usability](https://www.nngroup.com/articles/icon-usability/) | «A text label **must** be present alongside an icon.» | Иконка одна — не носитель смысла |
| Microsoft, [Navigation basics](https://learn.microsoft.com/en-us/windows/apps/design/basics/navigation-basics) | «Destinations are **clearly labeled** so users know where they are.»; «Fewer navigation items simplify decision making.» | Подпись = «где я», не «что делать» |

**Все три платформы сходятся:** короткое (1 слово), существительное, иконка + подпись, мало вкладок, вкладки различимы между собой.

---

## 6. ПРИНЦИПЫ (7 штук)

1. **Первая вкладка — якорь, а не категория.** У неё работа «верни меня в начало», а не «пообещай контент». Поэтому к ней применяют критерий *узнаваемости*, а не *информационного запаха*.
   ← NN/g [Homepage Links](https://www.nngroup.com/articles/homepage-links/): «In general, it's best to name the link to a website's homepage *Home*»; [Homepage Design](https://www.nngroup.com/articles/homepage-design-principles/): «People commonly rely on the homepage to orient themselves».

2. **Для якоря конвенция бьёт содержательность.** Пользователь принёс модель с других сайтов; отклонение = налог на обучение без выгоды.
   ← NN/g [Jakob's Law](https://www.nngroup.com/videos/jakobs-law-internet-ux/); [Heuristic #4](https://www.nngroup.com/articles/consistency-and-standards/): «Follow platform and industry conventions»; MS [Navigation basics](https://learn.microsoft.com/en-us/windows/apps/design/basics/navigation-basics): «following standard conventions… will make navigation predictable».

3. **Для остальных вкладок — наоборот: содержательность, без вагонов-глаголов.**
   ← NN/g [Menu-Design](https://www.nngroup.com/articles/menu-design/) G7; [3 IA Mistakes](https://www.nngroup.com/articles/3-ia-mistakes/): «Vague verbs (Explore, Discover, Learn…) are not effective category names».

4. **Вкладки обязаны быть взаимно различимы.** Пересечение смыслов — дефект IA, а не стилистика.
   ← NN/g [5 Tips](https://www.nngroup.com/articles/category-names-suck/) правило №3 «Check for Overlapping Categories»; MS: «pages are clearly distinct from each other».

5. **Нельзя сужать ярлыком то, что шире ярлыка.** Если вкладка = эфир + витрина, то «Радио»/«Сейчас» отрежут витрину в голове пользователя. Установленная моделью Apple семантика: Radio = станции, сосед Home.
   ← Apple [Music: Radio](https://support.apple.com/guide/music-windows/play-apple-music-radio-mus0456fe22c/windows) (Home/Library/Radio/Search; Radio = 6 станций + жанровые станции); NN/g [5 Tips](https://www.nngroup.com/articles/category-names-suck/) правило №4 «Categorize Based on Users' Mental Models».

6. **Если подпись не может нести запах — перенеси его на иконку и первый экран.** Это законный ход, а не отговорка.
   ← NN/g [Homepage Design](https://www.nngroup.com/articles/homepage-design-principles/) принцип 3 «Reveal Content Through Examples»; [Menu-Design](https://www.nngroup.com/articles/menu-design/) G10; [Icon Usability](https://www.nngroup.com/articles/icon-usability/); Apple HIG: подпись + иконка вместе «clearly describing the type of content».

7. **Форма: одно слово, существительное, иконка+подпись, 3–5 вкладок. Грамматический параллелизм НЕ требуется.**
   ← Apple HIG [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars): «Use single words whenever possible», «navigation, not… actions»; NN/g [Tabs](https://www.nngroup.com/articles/tabs-used-right/): «1-2 words»; [Material/Android](https://developer.android.com/develop/ui/compose/components/navigation-bar): «three to five destinations»; NN/g [3 IA Mistakes](https://www.nngroup.com/articles/3-ia-mistakes/): «Parallel language is not necessary».

---

## 7. Чего я НЕ нашёл (честный отчёт о пробелах)

Это важнее, чем то, что нашёл — потому что показывает предел доказательности.

1. **НЕ нашёл контролируемого эксперимента (A/B или количественного юзабилити-теста), напрямую сравнивающего генерическую подпись («Главная»/«Home») с содержательной («Радио»/«Listen Now») в позиции первой вкладки.** Ни у NN/g, ни у Baymard. Рекомендации NN/g по неймингу категорий — **качественные/наблюдательные**; в [5 Tips](https://www.nngroup.com/articles/category-names-suck/) конкретных цифр/контрольных условий не приводится. ⇒ Моё решение опирается на (а) конвенцию + внешнюю консистентность, (б) правило непересечения, (в) установленную моделью Apple семантику слова «Радио» — но **не** на прямой замер. Если владелец хочет замер — это tree-test / first-click test на 3 вариантах, 20–30 респондентов, метрика: «где будешь искать чарты/жанры?».

2. **Baymard: не подтвердил.** В поисковой выдаче фигурировал тезис «broad labels like *Shop* or *Products* won't help users» — но при открытии [research/homepage-and-category-usability](https://baymard.com/research/homepage-and-category-usability) и [blog/ecommerce-navigation-best-practice](https://baymard.com/blog/ecommerce-navigation-best-practice) **этого текста на страницах нет**. Поэтому **не цитирую**. Из открытого подтвердилась только методология: «25 rounds of qualitative usability testing with 4,400+ test subject/site sessions», «900+ usability-related issues», «13,000+ homepage and category navigation elements manually reviewed». К неймингу первой вкладки Baymard, судя по открытым страницам, прямо не высказывается (их домен — e-commerce).

3. **Material Design 3 — не смог прочитать напрямую.** Страницы [m3.material.io/components/navigation-bar/guidelines](https://m3.material.io/components/navigation-bar/guidelines) и `/overview` рендерятся JS, отдают только заголовок. Дословную формулировку M3 про длину подписи **не нашёл**. Заменил на официальные Google-источники, которые читаются: [Android Compose Navigation bar](https://developer.android.com/develop/ui/compose/components/navigation-bar) и [Material Components Android](https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/BottomNavigation.md).

4. **RU-локаль: исследований не нашёл.** Ни у Яндекса, ни у VK, ни у Apple нет публичного гайдлайна/исследования, обосновывающего «Главная». Всё, что у меня есть по RU, — **конвенция**, проверенная в двух продуктах (Яндекс Музыка → «Главное»; Apple Music RU → «Главная»). Заявлять «Главная — стандарт де-факто в RU» на основании двух продуктов — **растяжка**; честная формулировка: *«"Главная/Главное" — доминирующая форма в двух крупнейших проверенных RU-музсервисах; контрпримеров среди них не найдено»*.

5. **Радио-first продукты (TuneIn, iHeartRadio) — не верифицировал.** Поиск дал только вторичные пересказы; авторитетную страницу с перечнем их вкладок не открыл. ⇒ **не цитирую**. Если это важно для решения — нужен отдельный заход (скриншоты App Store / открыть их веб-приложения).

6. **Apple Music RU — средняя надёжность.** «Главная» извлечена из скриншотов/оглавления [ru-ru руководства](https://support.apple.com/ru-ru/guide/music-web/welcome/web), а не из строки-инструкции. Страницы Apple support рендерятся JS и часто отдавали только сайдбар. (HIG удалось взять дословно только через JSON-эндпоинт `developer.apple.com/tutorials/data/...`.)

---

## 8. РЕШЕНИЕ

# → «Главная»

**Одно мнение, без меню.**

### Почему

1. **Слот 1 — якорь, а не категория** (принцип 1). Его задача — «начало / вернуться», и NN/g для этой задачи прямо рекомендует генерическое слово: «*it's best to name the link to a website's homepage Home*».
2. **Он открыт по умолчанию ⇒ «пустота» подписи ничего не стоит.** Ярлык не конкурирует за клик. Единственный реальный риск генерики (пропуск из-за слабого запаха) в этом слоте **не срабатывает**.
3. **«Радио» активно вредит** (принцип 5). Apple установила модель «Radio = станции, сосед Home». Назвав так вкладку, где лежит вся витрина, мы прячем витрину — свой главный актив. Ошибка асимметрична: у «Главной» цена ≈ 0, у «Радио» цена = потерянная витрина.
4. **Конвенция RU подтверждена** (принцип 2, §3): Яндекс Музыка → «Главное», Apple Music RU → «Главная». Москвич уже обучен.
5. **Форма идеальна** (принцип 7): одно слово, существительное, влезает в таб-бар, `labelMaxLines=1`.
6. **Запах переносится на иконку + первый экран** (принцип 6): иконка радиоволны/антенны + первым блоком «6 станций в эфире», витрина ниже. Пользователь узнаёт всё за полсекунды — без семи букв-обещаний.
7. **Бонус: освобождает «Волну».** Яндекс держит «Мою волну» **внутри** главного экрана, а не вкладкой ([Яндекс](https://yandex.ru/support/music/ru/new-library/my-wave)). Значит, будущая AI-«Моя волна» органично встанет **блоком на «Главной»** — и бронь слова остаётся нетронутой, а четвёртая вкладка не нужна.

Итоговая связка: **«Главная» / «Мой вкус» / «Открыть»**.
Параллелизм не нужен (принцип 7, [3 IA Mistakes](https://www.nngroup.com/articles/3-ia-mistakes/)).

### Что сделать, чтобы «Главная» не осталась пустой (обязательные условия)

Без этого рекомендация недействительна:
- **Иконка** = радиоволна/антенна (не «домик»). Домик = «сайт вообще»; волна = «это радио». Носитель домена — иконка.
- **Первый экран, блок №1** = «В эфире сейчас» с 6 станциями (живая метка + что играет). Это `Reveal Content Through Examples`.
- **Блок №2+** = витрина (жанры, подборки, чарты, редакция, исполнители). Витрина обязана быть **видна со скроллом ≤1 экрана**, иначе она не существует.
- Плашку/лейбл «Радио» **не выбрасывать** — использовать как заголовок первого блока и как фильтр внутри. Слово живёт, но не в роли ярлыка вкладки.

---

## 9. Чем рискуем при каждом финалисте

| Кандидат | Главный риск | Величина | Основание |
|---|---|---|---|
| **«Главная»** ✅ | Ничего не обещает; вся нагрузка запаха ложится на иконку и первый экран. Если первый экран сверстают плохо (витрина ниже 1,5 скролла) — витрину всё равно не найдут. | **Низкая.** Вкладка открыта по умолчанию ⇒ пропуска по слабому запаху не будет. Риск переносится в вёрстку, где он управляем. | NN/g [Homepage Links](https://www.nngroup.com/articles/homepage-links/), [Homepage Design](https://www.nngroup.com/articles/homepage-design-principles/) |
| **«Радио»** | Читается как «только прямой эфир» ⇒ **прячет витрину**. Пользователь пойдёт искать жанры/чарты в «Открыть» и «Мой вкус», не найдёт, решит, что их нет. Плюс тавтология: в радио-приложении вкладка «Радио» — как в почте вкладка «Почта». | **Высокая.** Бьёт по главному активу. | Apple [Music: Home/Library/**Radio**/Search](https://support.apple.com/guide/music-windows/play-apple-music-radio-mus0456fe22c/windows); NN/g [5 Tips](https://www.nngroup.com/articles/category-names-suck/) №4 |
| **«Обзор»** | **Дублирует «Открыть»** (Browse ≈ Discover). Две из трёх вкладок про одно. Пользователь не сможет предсказать, что где. | **Высокая.** Прямое нарушение «Check for Overlapping Categories». | NN/g [5 Tips](https://www.nngroup.com/articles/category-names-suck/) №3; MS «clearly distinct from each other» |
| **«Слушать»** | Глагол, не различает (слушать можно во всех трёх). Читается как **действие**, а таб-бар — навигация. Ноль запаха при нулевой конвенции. | **Средне-высокая.** | Apple HIG: «Use a tab bar to support navigation, **not to provide actions**»; NN/g про вагоны-глаголы |
| **«Сейчас»** | Сужает во времени («что идёт прямо сейчас») ⇒ тот же промах, что «Радио», **плюс** незнакомая конвенция. Худшее из двух миров. | **Высокая.** | NN/g [Jakob's Law](https://www.nngroup.com/videos/jakobs-law-internet-ux/) + принцип 5 |
| **«Дом»** | Калька с Home. В русском «дом» = здание. Не является RU-конвенцией (ни в одном проверенном RU-интерфейсе не встретился). Выглядит как плохой перевод ⇒ бьёт по доверию к продукту. | **Средняя** (не ломает findability, ломает восприятие качества). | §3; отсутствие в Яндекс/Apple RU |

---

## 10. Как проверить меня за 1 день (если владелец хочет замер, а не мнение)

Моё решение опирается на конвенцию и на модель Apple, но **не на прямой эксперимент** (§7.1). Дешёвая проверка — **first-click / tree test**:

- 3 варианта дерева: `Главная|Мой вкус|Открыть`, `Радио|Мой вкус|Открыть`, `Слушать|Мой вкус|Открыть`.
- Задачи: «Где найдёшь **чарт** самых популярных треков?», «Где послушаешь **Русское Радио** прямо сейчас?», «Где найдёшь подборку в жанре **рок**?».
- Метрика: доля первых кликов в правильную вкладку. 20–30 респондентов, Москва, слушатели радио.
- **Негативный контроль (обязателен):** подмешать вариант-пустышку `Раздел 1|Раздел 2|Раздел 3`. Если тест **не** покажет на нём падения — тест сломан, и его результатам верить нельзя.

Гипотеза, которую я готов проиграть: на варианте «Радио» задачи «чарт» и «жанр рок» просядут (клики уйдут в «Открыть»), а задача «Русское Радио сейчас» — нет.

---

## Источники (все открыты и процитированы)

**NN/g**
- [Menu-Design Checklist: 17 UX Guidelines](https://www.nngroup.com/articles/menu-design/) — Page Laubheimer, 07.06.2024
- [5 Tips for Avoiding Confusing Category Names](https://www.nngroup.com/articles/category-names-suck/) — Loranger & Dykes, 15.12.2013 / обн. 11.10.2024
- [3 Common IA Mistakes (Low Information Scent)](https://www.nngroup.com/articles/3-ia-mistakes/) — Page Laubheimer, 16.04.2023
- [Homepage Links Remain a Necessity](https://www.nngroup.com/articles/homepage-links/) — Hoa Loranger, 23.07.2017 / обн. 25.10.2024
- [Homepage Design: 5 Fundamental Principles](https://www.nngroup.com/articles/homepage-design-principles/) — Huei-Hsin Wang, 15.03.2024
- [Tabs, Used Right](https://www.nngroup.com/articles/tabs-used-right/) — Evan Sunwall, 02.08.2024
- [Basic Patterns for Mobile Navigation](https://www.nngroup.com/articles/mobile-navigation-patterns/) — Raluca Budiu, 15.11.2015
- [Icon Usability](https://www.nngroup.com/articles/icon-usability/) — Aurora Harley, 27.07.2014
- [Consistency and Standards (Heuristic #4)](https://www.nngroup.com/articles/consistency-and-standards/) — Rachel Krause, 10.01.2021
- [Jakob's Law of Internet UX](https://www.nngroup.com/videos/jakobs-law-internet-ux/)

**Apple**
- [HIG: Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) (дословно получено через `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/tab-bars.json`)
- [Play Apple Music radio (Windows guide)](https://support.apple.com/guide/music-windows/play-apple-music-radio-mus0456fe22c/windows) — состав навигации Home/Library/Radio/Search
- [Руководство Apple Music, ru-ru](https://support.apple.com/ru-ru/guide/music-web/welcome/web) — «Главная», «Медиатека» (средняя надёжность)

**Google / Material**
- [Navigation bar — Android Compose](https://developer.android.com/develop/ui/compose/components/navigation-bar)
- [Material Components Android — BottomNavigation.md](https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/BottomNavigation.md)
- ❌ [M3 navigation-bar guidelines](https://m3.material.io/components/navigation-bar/guidelines) — **не прочитано** (JS-рендер)

**Microsoft**
- [Navigation basics for Windows apps](https://learn.microsoft.com/en-us/windows/apps/design/basics/navigation-basics)
- [NavigationView](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/navigationview)

**RU-конвенция**
- [Яндекс Музыка на Android — инструкция для незрячих](https://inclusion.yandex.ru/tutorials/music-android) — дословный таб-бар: «Главное» (1 из 4)
- [Яндекс Музыка на web — инструкция для незрячих](https://inclusion.yandex.ru/tutorials/music-web)
- [Яндекс: «Моя волна»](https://yandex.ru/support/music/ru/new-library/my-wave) — «Моя волна» живёт НА главном экране, не вкладкой

**Baymard** (методология подтверждена, тезис про broad labels — НЕ подтверждён, не цитируется)
- [E-Commerce Homepage & Category Navigation](https://baymard.com/research/homepage-and-category-usability)
- [Homepage & Navigation UX Best Practices](https://baymard.com/blog/ecommerce-navigation-best-practice)
