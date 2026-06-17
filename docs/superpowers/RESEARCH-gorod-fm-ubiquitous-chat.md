# RESEARCH → BUILD SPEC: Город ФМ — вездесущий чат-слой (per-station + global + AI/human toggle)

> Синтез 7 web-grounded, adversarially-verified досье в ОДНУ opinionated, build-ready интеграционную спеку.
> Grounded в реальный прототип `designs/gorod-fm.html` (single-file scripted SPA, 12 routes, `.ai-dock` = Twinr AI, `#ai-ribbon`, `--brand-blue-light:#5168FC`, Onest-only, cinema default + dev-gated light, a11y load-bearing).
> Дата: 2026-06-17. Все «must_fix» из верификации применены; всё помеченное overstated/wrong/unverifiable — отброшено или захеджировано прямо в тексте.

---

## 1. EXECUTIVE SUMMARY — тезис

Город ФМ позиционируется как **первый AI-driven music streaming**, чей wedge — НЕ чёрный ящик: радио **объясняет** каждый трек («почему этот трек»), принимает голос/текст-правки («сделай по-другому») и показывает **живой Twinr-профиль**. Запрос владельца («чат почти на каждом экране · на каждом радио/канале свой чат + общий · тумблер ЛЮДЯМ/AI в одном composer») может либо усилить этот wedge, либо превратить продукт в дженерик-соцсеть. **Граница ровно одна:**

> **AI-слой = вездесущий (он дешёвый: приватный, скриптованный, ноль модерации/нотификаций). Человеческий чат = сфокусированный там, где есть реальное синхронное со-слушание.** Тумблер ЛЮДЯМ/AI — это и есть мост между ними, но он **беспрецедентен** (ни один продукт не отгрузил user-flipped human/AI send-target toggle — см. §5), поэтому он самый высокорисковый элемент и проектируется fail-safe.

Почему это **усиливает** «explainable AI radio», а не размывает:

1. **Объяснение становится социальным топливом.** Шапка комнаты = now-playing + строка «почему» из существующего движка. Никто из конкурентов (Spotify Jam, Stationhead, Spotify Group Session/Blend) не выводит обоснование выбора как общий объект разговора — Spotify AI DJ озвучивает rationale, но не делает его темой комнаты. Это и есть defensible edge (не сам caption, а **редактируемый живой профиль + двунаправленные правки вкуса**).
2. **Реакция-тап лёгкого зрителя** — слабый implicit-сигнал, агрегируется/дебаунсится, любое изменение профиля **видимо и обратимо** (никаких per-tap мутаций — это противоречило бы transparency-обещанию).
3. **Тумблер сохраняет один глагол «отправить»**, меняя только получателя — но т.к. mis-send (приватный промпт «поставь грустное про бывшую» → в публичную комнату) социально дороже, чем неверный формат ответа в поиске, защита от mode-error усилена структурно.

**Anti-thesis (skeptic-линза, применена):** соц-слои на музыке — кладбище (Spotify Friend Activity → opt-out-by-default 2017; Spotify Live/Greenroom закрыт 30 апр 2023; Discord Clyde закрыт 1 дек 2023; Apple Music = ноль чата и в топ-2). Урок НЕ «не строй чат», а «чат — фича на НЕКОТОРЫХ экранах, не ambient-слой на ВСЕХ». Поэтому: human-чат **гейтится** к `#/lives` (+ контекстные комнаты `#/track`/`#/artist` как фильтр родительской), `#/onboarding`/`#/recap`/`#/map` — **никогда** не несут соц-чат, а tV/CarPlay — голос-первичен, текст-чат подавлен.

---

## 2. СИНТЕЗ 7 ИЗМЕРЕНИЙ — что украсть / чего избегать

### D1 · Live-audio & per-station social chat (`live-audio-social`)
- **Steal:** компактный **now-playing strip наверху каждой комнаты** (трек/арт/elapsed-dot) + однострочное «почему» — общий референт. Reaction-rail (🔥❤️🎧😮 + brand-spark) с optimistic-UI; presence = «🟢 N слушают» + 5–7 avatar pile, без roster. Virtualized auto-scroll + «Новые ↓» pill + slow-mode.
- **Avoid:** чат, оторванный от аудио (дженерик-DM); «X печатает» при толпе; full roster; floating-hearts без reduced-motion fallback.
- **Verify-фиксы применены:** ✗ «Spotify Hangout» не существует → используем Jam/Group Session/Blend; ✗ Super Chat $→цвет→длительность специфика — только качественный паттерн (цвет-тиры + pinned + viewer count); ✗ Twitch emote-wall/combo = third-party overlays, не native; ✗ «Amp умер от пустых комнат» — хедж, причина = низкий traction; 90-9-1 — эвристика, не закон; reaction→профиль = агрегировать/дебаунсить, видимо/обратимо, в прототипе помечать scripted.
- *Sources: stationhead.com; billboard.com/pro/stationhead-…; newsroom.spotify.com (Jam 2023-09-26, Request-to-Jam 2026-01-07); hypebot Turntable/Hangout 2024-08; getstream.io/blog/7-ux-best-practices-for-livestream-chat; nngroup participation-inequality; nts.live.*

### D2 · Per-room vs global IA & navigation (`room-vs-global-ia`)
- **Steal:** строгая 3-tier IA **Surface → station-list (`#/lives`) → room chat**; **закреплённый «Общий эфир»** наверху списка (Telegram General — pinned/special, НЕ «undeletable» — admins могут скрыть). Two-tier unread: тихая brand-blue точка (активность) vs counted warm-accent pill (тебя @-упомянули). Twitch Shared-Chat **merge-but-attribute** — per-message station-chip в глобале. Stable hash-deep-links (`#/lives/:stationId/chat`, `#/chat/global`); per-room scroll+draft persist; смена музыки НЕ переключает комнату (chip «перейти в чат станции?»).
- **Avoid:** разбухший #general; авто-switch комнаты при смене станции; «Также в общий» по умолчанию ON; full-width Discord-panel-модель wholesale (у Discord чат = ВСЁ приложение; у нас player первичен).
- **Verify-фиксы:** ✗ Slack-AI «никогда не делит composer» overstated (Slack-боты постят в канал) — citируем Slack только для ephemeral-REPLY; per-station merge-engine + crosspost — premature для scripted demo (downscope до attribution-thumbnails + toggle «Все станции/По станциям»); «Twinr завершил действие» НЕ мешать с human @-mention.
- *Sources: discord.com/blog/how-discord-made-android-…; such.chat/blog/telegram-topics; help.twitch.tv/s/article/shared-chat; community.zapier (Slack also-send); docs.slack.dev/ai; guilded support.*

### D3 · AI + humans в ОДНОМ surface — toggle (CRUX) (`ai-human-toggle`)
- **Steal:** `@Twinr` inline-mention + `/twinr` как **always-on fallback** к toggle; AI-ответы в комнате **приватны по умолчанию** («видно только вам» + «Поделиться с чатом»); composer **меняет всё состояние** по режиму; target-в-placeholder («Написать всем в «LoFi»…»); undo-toast после human-send; disclosure = transparency-фича.
- **Avoid:** молчаливый/sticky toggle с неизменным placeholder; AI авто-встревание (Character.AI Talkativeness) в человеческой комнате; полагаться только на текст-disclosure.
- **Verify-фиксы (КРИТИЧНО):** ⚠ **wrong:** ни WhatsApp/Snapchat/Discord/Teams НЕ реализуют user-flipped human/AI toggle — он **беспрецедентен и highest-risk**, его надо mode-error-тестить, не «валидировать». Adjacent-механизмы: WhatsApp=@mention-routing, Snapchat=отдельный AI-тред, Discord=bot-set ephemeral + slash, Teams=slash+chips. ✗ «sees only this message» противоречит «живому профилю» → scope-note различает «чужой чат комнаты (исключён)» vs «твоя накопленная история вкуса (намеренно хранится)». ✗ private-by-default в shared-комнате = backend-enforced → в scripted SPA это **UI-affordance, не доставленное свойство**. Slash на TV/CarPlay неюзабелен.
- *Sources: faq.whatsapp.com/203220822537614; telegram.org/blog/ai-bot-revolution-11-new-features; discordjs.guide/slash-commands/response-methods; help.openai.com release-notes; medium product.police wrong-whatsapp-group; malaymail Messenger-unsend.*

### D4 · Composer & input affordances + voice (`composer-affordances`)
- **Steal:** target **виден в момент набора И снова на кнопке send** (LinkedIn pill / X Circle); segmented control с **icon+слово** на каждом сегменте (читается в grayscale); restate на send-button («Спросить Twinr» vs «Отправить в #LoFi»); `/` = единственный accelerator; voice **наследует активный lane** (push-to-talk, live-транскрипт перед send).
- **Avoid:** color-only сигнал режима; `role=tablist` (roving arrows — неверная семантика); voice-commit без видимого транскрипта; перегруз composer (toggle+mic+/+checkbox → 44px budget).
- **Verify-фиксы:** не мешать `aria-current` (single-select) с `aria-pressed` (independent) — **выбрать ОДНО**: 2-state mutually-exclusive lane = single-select (radiogroup ИЛИ aria-current segmented). ⚠ **Rec5 governs Rec1:** composer у человеческой комнаты дефолтит в **ЛЮДЯМ**, surface-based AI-default только на AI-only surface (`#/taste`, dock). Undo-toast = Gmail send-delay паттерн, НЕ Messenger «remove for everyone». Streaming-транскрипт НЕ лить per-token в aria-live (флуд screen-reader) — announce по stabilized-chunks/on-stop. «Транскрипт перед send» = safety-practice, НЕ WCAG-требование. STT в scripted SPA = mock/future, не shippable. Mic конфликтует с играющим плеером → ducking/pause.
- *Sources: searchenginejournal LinkedIn audience; techcrunch Twitter-Circle; socialtradia IG-close-friends; docs.slack.dev chat.postMessage reply_broadcast; zapier Notion-AI; primer.style segmented-control/accessibility; a11y-collective aria-selected; engadget/completeaitraining ChatGPT-voice-inline.*

### D5 · Moderation, presence, trust & safety at scale (`moderation-presence`)
- **Steal:** **friction-by-default** = per-room chat-state strip с именем режима по-русски («Медленный режим · 5 сек» / «Только подписчики» / «Проверенные»), глобал тяжелее станций; per-message report/mute/block (mute = client-side, работает без backend); legible identity (handle + Twinr-chip + verified-glyph); presence «1 240 слушают · 18 пишут» (не путать слушателей с пишущими); scope-isolation (per-station сдерживает blast-radius).
- **Avoid:** wide-open zero-friction глобал; скрытый режим; ban/timeout у обычных юзеров; молча исчезающие сообщения.
- **Verify-фиксы:** ✗ Twitch «2s default» = на самом деле 30s; «followers 10-30 мин» = конфигурируемо 0мин–3мес — числа выбросить. ✗ Stationhead «400k / 5.4M / Butter» — unverifiable, только качественно (Stationhead host-broadcast-centric, не 400k-way чат). ✗ **152-FZ НЕ «align»** — сбор телефонов **УВЕЛИЧИВАЕТ** обязанности (согласие, 242-FZ локализация на РФ-серверах, регистрация оператора); Roskomnadzor messenger-ID применимость к music-чату **неясна** → всё legal = «flag for counsel», не established. 18+ gate для music-чата возможно непропорционален. ⚠ **prototype-honesty:** «AI-модерация включена» / «Сообщение скрыто (нарушение)» / presence-числа — привязать к documented demo/seed, НЕ фабриковать случайно (иначе moderation-theater / deceptive-affordance).
- *Sources: help.twitch.tv moderation; support.google.com/youtube 9826490/10888907; discord.com/safety/auto-moderation; nngroup participation-inequality; denuo.legal RF-messenger; secureprivacy 152-FZ.*

### D6 · AI как social glue / ambient host (`ai-social-glue`)
- **Steal:** **earned-interjection announcer** (Spotify AI DJ дисциплина: AI говорит только на границе трека или когда спросили; каждая проактивная строка несёт конкретную причину из профиля; default minimal/off); inbound taste-redirect из composer (voice+text, мгновенный видимый diff); one-click room-recap «Что я пропустил?» (pull-based, scoped к unread); group-aware «вкус комнаты» (Blend-style, с атрибуцией «кто добавил»); mandatory persistent AI-disclosure.
- **Avoid:** AI болтает чтобы заполнить тишину (Amp-failure-mode); авто-инжект recap в стрим; «вкус комнаты» не должен раскрывать индивидуальные приваты; AI неотличим от человека.
- **Verify-фиксы:** ✗ «единственный catastrophic failure» — нет (есть silent-toggle mode-error, AI-mistaken-for-human, галлюцинации «причины», safety несовершеннолетних). ✗ voice «from day one» — в scripted SPA без STT = mock/defer, text-first. ✗ «real-time» анимация профиля = scripted + нужен reduced-motion fallback (instant). ✗ «вкус комнаты — никто не занимает» — Blend (taste-match score) + Jam («кто добавил») уже есть; новизна узкая = привязка к чат-комнатам + AI room-level объяснения. ✗ disclosure «обычно повышает доверие» — смешанные данные (AI-aversion); CA SB 243 = companion-chatbot закон (в силе 1 янв 2026), EU AI Act Art.50 scoped/phased — badge ≠ автоматический compliance. ✗ «Amp умер от always-on hosting» — хедж (broader traction/monetization).
- *Sources: techcrunch/musically Spotify-AI-DJ (voice май 2025, text окт 2025); slack.com Slack-AI recaps; discordsummarybot; newsroom.spotify Blend 2021/Jam 2023; blog.character.ai group-chat; conferbot AI-disclosure; artificialintelligenceact.eu Art.50.*

### D7 · Anti-patterns / when-NOT-to / cognitive load & a11y (`anti-patterns-a11y`)
- **Steal:** social-music graveyard урок (player sacred, social = opt-in/peripheral); kill-the-toggle-split-the-surface как fallback (две визуально разные поверхности); **no-chat zones**; phase the social cost (один shared «Эфир» сначала, notifications default-OFF, slow-mode/report/mute/kill-switch с v1); instrument-before-expanding.
- **Avoid:** chat на «почти каждом» как ambient human-слой; assertive aria-live для чата; reaction-burst без reduced-motion; чат над mini-player на mobile; текст-чат на TV/CarPlay.
- **Verify-фиксы:** ⚠ Rec «single-room/AI-only» **молча переопределяет** verbatim-scope владельца (per-station + global) → подавать как phased default, **owner-gated**, не settled. ✗ Discord Clyde убит как sunset-эксперимент, НЕ доказано mode-error — пример иллюстративный, mode-error-аргумент стоит на HCI-merits сам. ✗ push-числа (52%/43%/46-63) = vendor-stats, хедж. ✗ NN/g clutter не запрещает collapsed-dock affordance везде — аргумент за collapse-by-default, не blanket-ban. a11y precision: transcript = `role="log"` (implies polite); `aria-atomic` default false; **44px = WCAG 2.2 AAA (2.5.5)**, AA-минимум (2.5.8) = 24px — превышать ок, но не звать 44px «минимумом WCAG». **CarPlay/driving = hard safety blocker** (Apple HIG запрещает free-form чат за рулём). ✗ «#/lives — единственный синхронный surface» не факт (`#/home` Волна тоже continuous; синхронность в scripted прото unverifiable) — обосновывать концентрацию чата cost/moderation, не co-listening.
- *Sources: community.spotify Friend-Activity; techcrunch/musically Spotify-Live-shutdown; decrypt Clyde; sarasoueidan aria-live; w3.org WAI-ARIA dialog-modal & WCAG C39; nngroup minimize-cognitive-load; getstream live-content-moderation; apple.com/apple-music.*

---

## 3. РЕКОМЕНДОВАННАЯ АРХИТЕКТУРА — одна когерентная конструкция

**Принцип:** существующий единственный `.ai-dock` (Twinr AI, ~380px, bottom-right) — это **shell**, который эволюционирует в **chat host**. Он остаётся каноничным toggle-free 1:1 AI-домом ВЕЗДЕ (safety-net, как «отдельный тред»), и **дополнительно** умеет монтировать комнату в scope активного route.

```
┌─────────────────────────────────────── ОДИН Twinr-shell (.ai-dock) ───────────┐
│  СЛОЙ 1 (везде, toggle-free): приватный AI-директор — почему/сделай по-другому │
│  СЛОЙ 2 (только где есть комната): scoped room (станция / Общий) с composer-   │
│          тумблером ЛЮДЯМ↔Twinr, now-playing-шапкой, reaction-rail, presence    │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Форм-фактор по surface:**

| Surface | Чат как… | Поведение |
|---|---|---|
| **Web (desktop)** | **Docked right-rail panel** = существующий ~380px `.ai-dock` над плеером. | Комната рендерится ВНУТРИ dock. Никакого нового лейаута — расширяем dock контентом. Now-playing-шапка НАД списком (chat не оверлеит арт). |
| **Mobile** | **Full pushed route / bottom swipe-up sheet** из `#/lives`, НЕ floating overlay. | Sheet сидит **под/рядом** с now-playing-карточкой, не над ней (примирение D1↔D6: чат не прячет якорь). Никогда не делит нижнюю кромку (thumb-zone) с активным mini-player. Focus-trapped dialog. |
| **TV** | **Read-only ambient** (presence + now-playing «почему»), без ввода текста. | Голос («почему?»/«сделай по-другому») = первичный ввод. Сегмент-toggle и `/` неюзабельны — не показывать. |
| **CarPlay** | **Подавлен (hard block)** для текст-чата. | Только голос-lane к AI, lane-видимость объявляется аудио. Free-form human-чат запрещён за рулём (Apple HIG, safety). |

**Почему dock-panel, а не per-screen rail или новый full-route шелл:** (1) переиспользует уже существующий `.ai-dock` (ноль нового primary-лейаута, player остаётся sacred); (2) один источник правды для AI-состояния — invoking AI из room-composer и из dock идут через **один Twinr-pipeline** (иначе расходящиеся истории ассистента, риск из D2); (3) collapse-by-default держит cognitive-load низким (D7-фикс: collapsed affordance везде ≠ clutter).

---

## 4. SCOPE-МОДЕЛЬ — глобал ↔ per-station ↔ (опц.) per-track/artist

### Иерархия
```
Surface (Волна/Медиатека/…) 
  └─ Station list = #/lives (room-list canonical surface)
       ├─ 📌 «Общий эфир»  (global, pinned наверху, special — не удаляется юзером)
       ├─ #LoFi Ночь      (per-station room)
       ├─ #Синтвейв        (per-station room)
       └─ …
  └─ Twinr dock = 4-й ортогональный слой (ассистент), НЕ внутри room-иерархии
```

- **GLOBAL «Общий эфир»** — всегда доступная якорная комната. **Prototype-honesty (D2/D5-фикс):** не утверждать «всегда населён» — либо явно scripted/seeded demo-контент, помеченный как демо, либо честный empty-state. НЕ фабриковать «живость».
- **PER-STATION** — каждая плитка `#/lives` + каждый радио-канал = своя комната, независимый slow-mode/state.
- **PER-TRACK / PER-ARTIST (scope-into, НЕ ghost-channel):** `#/track`/`#/artist` **наследуют родительскую станцию/артист-комнату с фильтром по треку**, а не плодят приватный пустой канал на URL. Тонкая страница инherits живую толпу. Это и есть правильное прочтение «чат почти на каждом экране» = **scope-into-shared-room**, не private empty channel.
- **«Волна» (`#/home`)** — комната scoped к твоей персональной адаптивной Волне; `#/home` continuous-listening, но human-чат там НЕ ambient — см. §6 (там dock = AI-lane, человеческая комната не дефолтит).

### Переключение комнат и смена станции/трека
- Header **segmented control: `[Эта станция] [Общий]`** — scope всегда виден над composer (юзер не misfire-ит в неверную комнату).
- **Смена музыки НЕ переключает комнату** (D2-фикс, load-bearing): меняешь станцию на `#/home` → открытая комната остаётся; показываем **non-destructive chip** «Сейчас играет: <станция> · перейти в её чат?» — авто-switch запрещён («сменил музыку — потерял контекст» = failure).
- **Per-room scroll + draft persist** в client-state (без backend); deep-links `#/lives/:stationId/chat`, `#/chat/global`.
- **Reset на ROOM-change, не на каждый screen-change** (D7-фикс): юзер в середине social-разговора, ушедший на `#/track` глянуть текст и вернувшийся, не должен молча флипнуться в AI.

### Unread / presence (two-tier, D2/D5)
| Tier | Сигнал | Триггер | a11y |
|---|---|---|---|
| Тихий | brand-blue **точка** (`#5168FC`) | любая активность комнаты (опционально) | НЕ в aria-live |
| Срочный | counted **warm-accent pill** (НЕ синий) | (a) тебя @-упомянул человек; (b) Twinr завершил **запрошенное** действие — *в прототипе детерминирован, «срочность» частично синтетическая, держать отдельным под-affordance от human-@* | **только этот tier** → `aria-live="polite"` |
- Mute-per-station **подавляет счётчик**, не только звук. Presence «🟢 1 240 слушают · 18 пишут» в шапке (не путать listeners↔chatters). В прототипе — seeded/документированные числа, не случайные.

---

## 5. THE COMPOSER TOGGLE — центрепис

### Рекомендованный паттерн: **сегментированный single-select toggle ВНУТРИ composer + `@Twinr`/`/` как вторичный fallback**

**Почему сегмент-toggle, а не @mention-only / dedicated-tab / slash-only:**
- Toggle убирает трение печатать handle каждое сообщение — идеально для нескольких подряд AI-ходов (taste-tuning) ИЛИ нескольких social-ходов; «отправить» остаётся константой, меняется только получатель (низкая cognitive-load, Google AI-Mode — **единственный реальный precedent** для one-input/two-target).
- Но т.к. сам toggle **беспрецедентен и mode-error-prone** (D3 verify = wrong: никто его не валидировал), он fail-safe-проектируется и **дополняется** `@Twinr` (muscle-memory из WhatsApp/Telegram) и `/` (power-user), чтобы dangerous default (broadcast людям) всегда был deliberate.

> **Семантика (D4-фикс, load-bearing):** 2-state mutually-exclusive lane = **single-select**, реализуется как **radiogroup ИЛИ aria-current segmented control — НЕ два независимых `aria-pressed` toggle, НЕ `role=tablist`** (нет roving-arrow). Выбрать ОДНУ модель и держать консистентно.

### Tradeoff-таблица (рекомендация + 2 альтернативы)

| Паттерн | Плюсы | Минусы | Вердикт |
|---|---|---|---|
| **A. Segmented toggle + @/`/` fallback (РЕКОМЕНДОВАНО)** | Без трения для серий ходов; «send» константа; реальный precedent (Google AI-Mode); fallback убирает «застрял» | Беспрецедентен → mode-error риск; нужен сильный визуальный/структурный сигнал | **SHIP.** Fail-safe: дефолт ЛЮДЯМ в human-комнате, reset на room-change, undo-toast, private-AI-reply |
| **B. @mention-only (`@Twinr …`)** | Self-documenting (цель в тексте), ноль mode-state, degrade-gracefully на TV/voice, чистая privacy-граница | Трение каждое сообщение; плохо для серии AI-правок; discoverability ниже для casual | Fallback внутри A, не primary |
| **C. Dedicated-tab «Эфир / Twinr» (две поверхности)** | Mode-error структурно невозможен (нет общего composer); самый безопасный | Тяжелее лейаут; теряет «один composer» интент владельца; на mobile конкурирует за место | **Mandated-fallback:** если owner-тест A провалит mode-error — откат на C внутри `#/lives` |

### Что делает активную цель **unmissable + reversible** (D3+D4+D5)
Связать **ВСЁ** состояние composer с режимом (НЕ только цвет — color-only fail WCAG 1.4.1):
1. **Слово + icon** на каждом сегменте: 👥 «Всем» · ✦ «Twinr» (читается в grayscale).
2. **Placeholder = имя цели в поле:** `Написать всем в «LoFi Ночь»…` ↔ `Спросите Twinr…` (Medium wrong-group-fix: цель в point-of-action).
3. **Send-button restate:** `Отправить в #LoFi` ↔ `Спросить Twinr`.
4. **`#ai-ribbon`** echoes armed-destination как persistent banner («Сообщение в #LoFi» / «Говорите с Twinr»).
5. **Цвет** = `#5168FC` fill **только как redundant-decorative** поверх filled-vs-outline shape (проверить 3:1 non-text contrast в cinema И light, WCAG 1.4.11).
6. **Mode-объявление через role-state** (`aria-current`/radio-checked), НЕ re-announcing aria-live на статичном composer.

### Mis-send guardrails
- **Дефолт = ЛЮДЯМ** в любой человеческой комнате; **AI-default только** на AI-only surface (`#/taste`, dock). **Reset на ROOM-change** (не screen-change). Fresh «Общий» → reset в ЛЮДЯМ независимо от прошлой persistence.
- **Undo-toast после human-send** («Отправлено в «LoFi» · Отменить», ~5–10s, focusable, `aria-live="polite"`) — это **Gmail send-delay паттерн** (D4-фикс), защищает необратимый публичный broadcast (людей нельзя «развидеть»). НЕ confirm-dialog на каждый send (трение убивает social).
- `@Twinr` mid-human-message и `/` — **определить collision-поведение:** если toggle уже «Twinr», `@Twinr` no-op; `/` в начале пустой строки открывает Twinr-меню, в середине — литерал. Reskin alone недостаточен против muscle-memory → ribbon + send-confirmation несут нагрузку.

### «Только вам» — приватный AI-reply в публичной комнате
- AI-ответ в station/global рендерится **inline, помечен `Twinr · видно только вам`** + явная кнопка **`Поделиться с чатом`** (Discord ephemeral-reply паттерн).
- **Prototype-honesty (D3-фикс):** в scripted backend-less SPA это **UI-affordance, не доставленное серверное свойство** — подавать как демо-аффорданс, не обещать enforced-приватность.
- `Поделиться с чатом` — **confirm/preview gate**, шарит ТОЛЬКО выбранный AI-ответ, **никогда исходный промпт юзера** (D4-фикс privacy); публичные комнаты нуждаются в модерации от спама/галлюцинаций.

### ASCII-мокап composer

```
РЕЖИМ «ВСЕМ» (human, дефолт в комнате):
┌──────────────────────────────────────────────────────────────┐
│ #ai-ribbon ▸ Сообщение в #LoFi Ночь            🟢 1 240 · 18  │
├──────────────────────────────────────────────────────────────┤
│  🎵 LoFi Ночь — «Midnight Tape» · ──●───── 1:12               │
│     почему: ночное настроение под твой late-night вкус        │
├──────────────────────────────────────────────────────────────┤
│  ( ● 👥 Всем )( ○ ✦ Twinr )   🔥 ❤️ 🎧 😮                     │
│  ┌────────────────────────────────────────────┐  🎙  ┌──────┐ │
│  │ Написать всем в «LoFi Ночь»…               │      │Отпр.→│ │
│  └────────────────────────────────────────────┘      └──────┘ │
└──────────────────────────────────────────────────────────────┘

РЕЖИМ «TWINR» (AI, синий accent + outline-flip + ✦):
┌──────────────────────────────────────────────────────────────┐
│ #ai-ribbon ▸ Говорите с Twinr (видно только вам)              │
├──────────────────────────────────────────────────────────────┤
│  ✦ Twinr · музыкальный директор                              │
│  чипы: [Почему этот трек?] [Сделать по-другому] [Спокойнее]   │
├──────────────────────────────────────────────────────────────┤
│  ( ○ 👥 Всем )( ● ✦ Twinr )                                  │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  🎙 ┌───────┐│
│  ┃ Спросите Twinr…                            ┃     │Спрос.✦││  ← #5168FC border (redundant)
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛     └───────┘│
└──────────────────────────────────────────────────────────────┘
(grayscale-test: ✦-glyph + filled-radio + placeholder + send-label несут режим БЕЗ цвета)
```

---

## 6. WHERE CHAT LIVES — per-route таблица (все 12 routes)

| Route | Chat? | Scope | Treatment |
|---|---|---|---|
| **#/home** (Волна) | ✅ AI везде · 🟡 human opt-in | dock=AI (default); комната scoped к персональной Волне | Dock = Twinr-lane default. `почему`/`сделай по-другому` chip в `#ai-ribbon` на смене трека. Human-комната **не дефолтит** — открывается осознанно. |
| **#/taste** (Мой вкус) | ✅ только AI | dock=AI only | `сделай по-другому` = приватная мутация профиля. **Никакого human-чата** (активное редактирование bubble-cloud нужен фокус). AI-default ок (AI-only surface). |
| **#/podborki** (Открыть) | 🟡 AI only (minimal) | dock=AI | Поиск/discover — AI-ассистент ок; human-чат не нужен (нет shared stream). |
| **#/library** (Медиатека) | 🟡 AI only | dock=AI | Личная — AI-помощь да, social нет. |
| **#/artist** | ✅ | наследует **artist-room** (фильтр), не ghost-channel | Breadcrumb «#Артист: Земфира». `@Twinr почему?` = social-эквивалент in-player кнопки. |
| **#/track** | ✅ | наследует **parent station/artist-room** с track-фильтром | Капли в контексте трека; тонкая страница инherits живую толпу. |
| **#/favorites** | 🟡 AI only | dock=AI | Личная коллекция; AI-курация да, social нет. |
| **#/lives** (LIVE GRID) | ✅ **PRIMARY human surface** | per-station rooms + 📌 Общий | Каноничный room-list. Каждая плитка → комната с now-playing-шапкой + state-strip + reaction-rail + presence. Тумблер ЛЮДЯМ/AI здесь load-bearing. |
| **#/onboarding** | ❌ **НЕТ** | — | Single-goal taste-picker; чат tank-ит completion. Прототип уже скрывает `.ai-dock` на `#/onboarding` (`html[data-active-route="#/onboarding"] .ai-dock`). |
| **#/profile** | 🟡 AI only + настройки | dock=AI | Здесь живут: per-room «тихий режим», global AI opt-out, mute-настройки, «Правила чата». |
| **#/recap** (9:16 card) | ❌ **НЕТ** | — | Export-clean surface: chat-панель загрязнит скриншот/экспорт shareable-карточки. |
| **#/map** (internal review) | ❌ **НЕТ** | — | Внутренний; ноль social-ценности. |

**Явно:** `#/onboarding`, `#/recap`, `#/map` НЕ несут social-чат (single-goal / capture-clean / internal). AI-only-доступ через dock сохраняется везде, КРОМЕ `#/onboarding`/`#/recap`/`#/map`.

---

## 7. AI CO-PRESENCE — Twinr внутри человеческой комнаты

- **Announcer (earned-interjection, Spotify-DJ дисциплина):** Twinr получает «ход» **только на смене трека или когда явно спросили**. На смене — одна тихая авто-исчезающая micro-card в `#ai-ribbon` с **конкретной причиной из профиля** («поставил X — ты часто слушаешь меланхоличное инди»). Проактивный голос/нарратив **default minimal/off** (Amp-урок — хедж: always-on hosting утомляет).
- **Summarizer:** каждая комната → кнопка **«Что я пропустил?»** (AI-side), summary только unread/last-session ЭТОЙ комнаты, **pull-based** (не авто-инжект в стрим). Recap — явный AI-артефакт, отделён от human-сообщений; recap может галлюцинировать → пометка «summary может быть неточным».
- **Group-aware «вкус комнаты»:** лёгкий collective Twinr-bubble-cloud (sibling к личному `#/taste`), Twinr ссылается при объяснении picks на room-уровне («эта волна тяготеет к X»). Human-suggestions атрибутированы (Jam «кто добавил»). **Новизна узкая** (D6-фикс): привязка к ad-hoc чат-комнатам + room-level AI-объяснения; collective-taste-as-object сам по себе уже у Blend/Jam. Агрегировать/анонимизировать — не раскрывать индивидуальные приваты.
- **Disclosure + opt-out (trust-primitive, не compliance-overhead):** каждое AI-авторское сообщение несёт persistent тег **`AI`/`Twinr`** + Twinr-accent (никогда не путается с человеком). Per-room **«тихий режим»** (AI только когда @-обращаются) + global opt-out в `#/profile`. **Legal-хедж (D6-фикс):** CA SB 243 = companion-chatbot закон (1 янв 2026), EU AI Act Art.50 scoped/phased — badge ≠ авто-compliance; AI-disclosure-эффект на доверие смешанный. Делать как brand-фичу «не чёрный ящик», не как «легально обязательный badge».
- **Связь с in-player кнопками:** `почему?` / `сделай по-другому` в плеере = AI-mode shortcuts — deep-link в dock, pre-set в Twinr-lane, dock авто-раскрывается показать ответ. Визуально привязаны к AI-accent чтобы два канала не смешивались. Один Twinr-pipeline для in-player, dock и room-composer (единый источник истины).
- **scope-note (D3-фикс, разрешение противоречия):** «Twinr видит из этой комнаты только твоё сообщение — НЕ чужой чат участников. Твоя история вкуса хранится намеренно (живой профиль).» НЕ копировать backend-enforced WhatsApp-гарантию в scripted прото.

---

## 8. MODERATION & TRUST MVP — минимум для прототипа СЕЙЧАС

Показать в UI **сигнал** правдоподобной safety-модели (не backend), привязанный к documented demo-state:

1. **Per-room chat-state strip** над composer, режим по-русски: «Медленный режим · 5 сек» / «Только подписчики» / «Проверенные». Глобал тяжелее («· 10 сек»). Тонкая полоса в `#5168FC`, `aria-live="polite"`, 44px (i)-glyph → «Правила чата».
2. **Per-message overflow-меню** (hover/long-press): **Пожаловаться / Заглушить / Заблокировать**. **Mute = client-side** (работает без backend). Ban/timeout НЕ давать обычным юзерам.
3. **Legible identity:** handle + маленький Twinr-profile-chip (ссылка на read-only срез `#/taste`: «любит синтипоп · 3 года в Городе ФМ») + verified-glyph. НЕ форсить real-name.
4. **Presence** «N слушают · M пишут» (seeded, не случайные).
5. **Один shared «Эфир» сначала** (не per-station на старте), notifications **opt-in/default-OFF**, slow-mode + report/mute + per-room kill-switch с v1. Per-station комнаты — только после moderation-бюджета/тулинга.
6. **Prototype-honesty (NON-NEGOTIABLE):** «AI-модерация включена» / «Сообщение скрыто (нарушение правил)» / presence-числа — **только привязанные к documented seed-данным**, НИКОГДА не фабриковать случайные «нарушения» (moderation-theater / deceptive-affordance противоречит anti-black-box-позиционированию).
7. **Legal = flag-for-counsel** (НЕ design-justification): RU identity/age — захеджировано, 152-FZ **увеличивает** обязанности при сборе телефонов; 18+ gate для music-чата возможно непропорционален.

---

## 9. ACCESSIBILITY MUST-HAVES + ANTI-PATTERNS

### Must-haves (a11y load-bearing — наследуется из существующих констрейнтов прото)
- **Transcript = `role="log"`** (implies polite), НЕ ad-hoc live-region. `aria-live="polite"` + `aria-atomic="false"` (atomic default false — reinforcement). **НИКОГДА `assertive`** для чата.
- **High-velocity coalescing:** «Анна и ещё 3 написали» вместо каждой строки + **pause-incoming control** (focusable 44px «Новые ↓» pill). Виртуализация + aria-live могут терять SR-объявления → тестировать доставку под виртуализацией.
- **Focus management:** панель = `role="dialog"`/`aria-modal`, focus-in на open, **focus-RETURN на trigger** (`#/lives`) на close, Escape закрывает.
- **Reduced-motion:** ВСЕ reaction/emoji-bursts + toggle-slide + profile-diff-анимация за `@media (prefers-reduced-motion: reduce)` с **instant/static fallback** (floating-hearts → инкремент-счётчик; profile-change → мгновенно).
- **Voice:** транскрипт по **stabilized-chunks/on-stop**, НЕ per-token в aria-live (флуд). Mic **ducking/pause** играющего плеера; lane виден в момент открытия mic.
- **Hit targets:** ≥44px на send/toggle/reaction/«Новые»/(i) (это WCAG 2.2 **AAA 2.5.5**; AA-минимум 2.5.8 = 24px — превышаем осознанно). `focus-visible` 3px ring.
- **Non-color mode-signal** (icon+слово+placeholder+role-state); `#5168FC` проверить 3:1 (1.4.11) в cinema И light.

### ANTI-PATTERNS — явный «НЕ делать»
- ❌ НЕ ставить human-чат на «почти каждый» экран как ambient-слой (Spotify Friend-Activity churn).
- ❌ НЕ молчаливый/sticky toggle с неизменным placeholder/цветом (catastrophic mis-send).
- ❌ НЕ `role=tablist` для toggle; НЕ мешать `aria-current` + `aria-pressed`.
- ❌ НЕ `aria-live="assertive"` для чата; НЕ авто-scroll-and-announce каждое сообщение.
- ❌ НЕ floating-hearts/reaction-burst без reduced-motion fallback.
- ❌ НЕ оверлеить чат на now-playing-арт (прячет якорь); НЕ над mini-player на mobile.
- ❌ НЕ текст-чат на TV/CarPlay (CarPlay = hard safety blocker за рулём).
- ❌ НЕ фабриковать случайные «нарушения»/presence/«всегда населён» (deceptive-affordance).
- ❌ НЕ авто-switch комнаты при смене станции; НЕ потерять draft/scroll.
- ❌ НЕ AI авто-встревание в человеческую комнату (только toggle/@/`/`).
- ❌ НЕ шарить исходный промпт юзера при «Поделиться с чатом» (только выбранный ответ).
- ❌ НЕ копировать backend-enforced privacy/legal-copy в scripted прото.

---

## 10. STAGED BUILD PLAN (под single-file scripted SPA) + OPEN DECISIONS

**Везде явно: что fake/scripted на каждом этапе.** Реальный per-room human-чат, global-чат, STT, cross-room AI-broadcast — backend/realtime-фичи; в SPA они **mocked/seeded affordances, не working backend**.

| Этап | Что строим | Что fake/scripted |
|---|---|---|
| **S0 · Toggle-prototype в dock** | Расширить `.ai-dock`: single-select toggle [Всем/Twinr], full-state reskin (icon+слово+placeholder+send-label+ribbon), `#5168FC` redundant + outline-flip, role-state. AI-lane = существующий scripted music-director. | Human-lane сообщения = local-state echo (не отправляются никуда). Mode-error-тест с Эльбиком ДО всего. |
| **S1 · #/lives комнаты + now-playing-шапка** | Каждая плитка → комната: now-playing-strip + «почему»-caption + state-strip + header `[Эта станция][Общий]`. Reaction-rail (optimistic-UI + reduced-motion). | Сообщения/presence/reactions = seeded demo-данные, помечены scripted. «Общий» = seeded или честный empty-state. |
| **S2 · Scope + persistence + deep-links** | Hash-routes `#/lives/:id/chat`, `#/chat/global`; per-room scroll+draft persist (client-state); chip «перейти в чат станции?» при смене музыки; reset-on-room-change; two-tier unread. | Unread/«Twinr завершил» — детерминированные seed-события. |
| **S3 · AI co-presence в комнате** | Announcer micro-card на смене трека; «Что я пропустил?» recap; private-AI-reply «видно только вам» + «Поделиться» (confirm/preview); persistent AI-tag; per-room «тихий режим». | Recap/announcer = scripted из seed-транскрипта; «private» = UI-affordance не enforced. |
| **S4 · Moderation/trust MVP** | State-strip режимы; overflow report/mute(client-side)/block; identity-chip+verified-glyph; «Правила чата»; presence. | Модерация = signaled, не enforced; числа seeded; legal — pending counsel. |
| **S5 · Multi-surface** | Mobile sheet под now-playing (focus-trap); TV read-only ambient + voice; CarPlay text-block. Voice mic в dock (lane-inherit, transcript-before-send). | STT = mock/Wizard-of-Oz-stub, помечен non-functional; voice deferred как working-фича. |
| **S6 · Instrument-before-expand** | Гейтить расширение чата за `#/lives` за engagement/report-rate метрики. | — (продакшн-gate, после прототипа). |

### OPEN DECISIONS — Эльбику решить ДО кода
1. **Identity: anon-handle vs profile-linked (Twinr-chip)?** Влияет на verified-tier, RU-legal exposure (152-FZ при сборе телефонов = больше обязанностей), и на presence-модель. Рекомендация: profile-chip lightweight, без real-name.
2. **Per-track/per-artist threads — в scope?** Рекомендация: НЕ отдельные комнаты, а **scope-into** родительской station/artist-комнаты с фильтром (избегаем ghost-channels). Подтвердить.
3. **Default composer mode + stickiness.** Рекомендация: ЛЮДЯМ в человеческой комнате, AI только на AI-only surface, **reset на room-change** (не sticky-across-rooms). Тестировать reset-vs-persist на mode-error.
4. **Чат opt-in или on-by-default?** Рекомендация: AI-dock везде on (collapse-by-default); human-чат **opt-in**, notifications **default-OFF**. Подтвердить.
5. **Scope-override gate (D7):** verbatim-интент = per-station + global. Рекомендация фазит **один shared «Эфир» сначала** (moderation/notification combinatorics). Это **переопределяет** заявленный scope → **нужно явное «гоу» Эльбика** на фазинг или на full per-station-сразу.
6. **Toggle vs split-surface fallback (B/C):** если owner-mode-error-тест A провалит — откат на dedicated-tab внутри `#/lives`? Подтвердить fallback заранее.
7. **TV/CarPlay паритет:** подтвердить voice-first / text-block (CarPlay safety hard-block) и read-only TV.
8. **Legal:** RU identity/age-gate — отдать юристу (152-FZ/Roskomnadzor применимость к music-чату неясна; 18+ возможно непропорционален).

---

## CONSOLIDATED SOURCES

**Live-audio / social-audio:** stationhead.com · billboard.com/pro/stationhead-social-audio-streams-listening-parties · hypebot Swifties-1M / Turntable-Hangout-2024-08 · newsroom.spotify.com (Jam 2023-09-26; Request-to-Jam Messages 2026-01-07; Blend 2021-08-31) · bandwagon.asia social-audio-room-apps · nts.live · musicbusinessworldwide/cnbc Amp-shutdown.
**IA / navigation:** discord.com/blog/how-discord-made-android-in-app-navigation-easier · support.discord.com muted-channel-unread · such.chat/blog/telegram-topics · help.twitch.tv/s/article/shared-chat · community.zapier Slack-also-send · eesel.ai Slack-split-view · slack.com/help AI-apps & huddles · blog.fastbots.ai Telegram-business · support.guilded.gg Groups/Chat-Channels · docs.slack.dev/ai.
**AI/human toggle & composer:** faq.whatsapp.com/203220822537614 · snopes/eff WhatsApp-AI-privacy · telegram.org/blog/ai-bot-revolution-11-new-features · poe.com/blog/multi-bot-chat · blog.character.ai group-chat · docs.sillytavern.app groupchats · support-apps.discord.com Ephemeral-FAQ · discordjs.guide slash-commands/response-methods · help.openai.com release-notes · medium product.police wrong-whatsapp-group · boredpanda cringy-private-text · malaymail Messenger-unsend · en.wikipedia.org/wiki/AI_Mode · zapier google-ai-mode & how-to-use-notion-ai · slack.com/blog slackbot & docs.slack.dev bolt ai-chatbot · support.microsoft.com Teams-Copilot · mc.merill.net MC952888 · pluggedin/techpoint Snapchat-My-AI · 9to5google Assistant-Gemini-2026 · searchenginejournal LinkedIn-audience · techcrunch Twitter-Circle-gone · socialtradia/socialboosting IG-green-circle · docs.slack.dev chat.postMessage & reply_broadcast · primer.style segmented-control/accessibility · a11y-collective aria-selected · developer.mozilla.org aria-selected · engadget/completeaitraining/help.openai ChatGPT-voice-inline.
**Moderation / trust / legal:** help.twitch.tv moderation & dev.twitch.tv/docs/chat/moderation · support.google.com/youtube 9826490 & 10888907 · discord.com/safety/auto-moderation & support.discord.com raids-101 / AutoMod-FAQ · bettermode one-percent-rule · denuo.legal RF-messenger · gorodissky.com RF-messaging-providers · secureprivacy.ai 152-FZ · getstream.io live-content-moderation · aws.amazon.com IVS-chat-moderation.
**AI social glue:** techcrunch/blog.push.fm/musically Spotify-AI-DJ · musictech Amp-shutdown · slack.com/blog & help Slack-AI · discordsummarybot.com & discord.com/discovery Summary-Bot · support.character.ai group-chat-FAQ · getailicia.com / frostytools ai_licia-Twitch · conferbot AI-disclosure-laws · artificialintelligenceact.eu Article-50.
**Anti-patterns / a11y:** community.spotify Friend-Activity · techcrunch/musically Spotify-Live-shutdown · techcrunch Greenroom-fund · en.wikipedia Spotify_Live · decrypt/engadget Clyde-shutdown · sarasoueidan accessible-notifications-aria-live · developer.mozilla ARIA-SR-implementors · w3.org WAI-ARIA dialog-modal & WCAG21 C39 · dequeuniversity 2.3.3-animations · nngroup minimize-cognitive-load & participation-inequality · contextsdk push-fatigue · appbot push-2026 · getstream live-content-moderation · apple.com/apple-music.
**Grounding:** `designs/gorod-fm.html` (`.ai-dock`, `#ai-ribbon`, `data-active-route`, `--brand-blue-light:#5168FC`, Onest, `@media (prefers-reduced-motion: reduce)`, aria-live).
