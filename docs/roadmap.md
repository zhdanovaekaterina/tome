# Roadmap

## Принципы

1. **Каждая версия — работающий продукт.** Не «половина ядра». Не «в разработке».
2. **Публикация с первого дня.** GitHub, README, скриншоты.
3. **Инкрементально.** Один класс → три класса → все. 20 заклинаний → 40 → 500.
4. **Combat — не в MVP.** Справка по actions + каст. Полный бой — позже.
5. **Другие системы — в конце.** D&D 5e сначала. Pathfinder, Cyberpunk — потом.
6. **Мобильный — в конце.** PWA. Native — только если нужно.
7. **Слои — фиксированы с 1.0.0.** `shared` → `reference` → `domain` → `application` → `api`, `identity` и `infra` рядом. Расширение — добавление данных и стратегий, не переделка слоёв.

---

## 0.x — До MVP (внутренние версии)

### 0.1.0 — Shared готов
- Value-objects (`DiceRoll`, `Ability`, `SpellId`, `ClassId`, ...).
- Enum'ы (`RestKind`, `ActivationCost`, `SpellSource`, ...).
- **Публикация:** GitHub, README, ADR.

### 0.2.0 — Reference готов
- `SpellData`, `Resolution`, `Effect`, `Upcast`.
- `SpellStrategyDefinition` (Known / Prepared / Spellbook).
- `LevelProfile`, `SlotTable`, `SlotCalculator`.
- `FeatureDefinition` + подтипы.
- `FeatureContainer` + `ClassData`, `SubclassData`, ...
- `GuideService`.
- Seed 20 заклинаний + 1 класс (wizard) + 1 подкласс (Evocation).

### 0.3.0 — Domain готов
- `CharacterModel`, `CharacterAbilities`, `CharacterClass`.
- `CharacterSpells`, `CharacterSpell`, `SpellSourceRecord`.
- `CharacterSlots`, `CharacterResource`, `CharacterProficiencies`.
- `StateMachine`, `HistoryManager`, `Memento`.
- 14 Actions + реестры.
- Порты: `CharacterRepository` (Protocol).
- **`domain` не содержит сервисов.** Только модели, FSM, actions, порты.

### 0.4.0 — Application готов
- 7 use cases (сервисы):
  - `CharacterFactory`
  - `CharacterService`
  - `BuildService`
  - `LevelUpService`
  - `SpellListService`
  - `CastService`
  - `RestService`
- Application **оркестрирует** domain + reference + порты.
- Application **не содержит** бизнес-логики — только последовательность вызовов.
- **ADR 0017** — `application-layer.md`.

### 0.5.0 — Identity готов
- `UserModel`, `AuthService`, `TokenService`.
- JWT access + refresh.
- Порты: `UserRepository`, `SessionRepository`.

### 0.6.0 — Infra готов
- SQLAlchemy модели + Alembic.
- Реализации репозиториев.
- Redis для черновиков.
- Docker Compose.

### 0.7.0 — API готов
- FastAPI роутеры: auth, characters, guide.
- JWT-мидлварь.
- structlog, /health.
- CORS, security headers.
- **DTO и маппинг** — только в `api/mappers.py`.
- Роутеры вызывают **только** `application`. Не лезут в `domain`.

### 0.8.0 — E2E работает
- Полный сценарий: register → build wizard → cast fireball → long rest → logout.
- README, ADR, CHANGELOG.
- CI: pytest + mypy + ruff.
- Диаграмма слоёв в README.

---

## 1.0.0 — MVP для портфолио

**Цель:** показать middle+ компетенции. Работающий помощник для волшебника 1-5 уровня.

### Что входит
- **Класс:** волшебник.
- **Уровни:** 1-5.
- **Заклинаний:** 20.
- **Подкласс:** Evocation.
- **Use cases:** build, level-up, cast, short rest, long rest.
- **Play:** справка по actions + каст заклинаний.
- **API:** FastAPI + OpenAPI.
- **БД:** Postgres (постоянные) + Redis (черновики).
- **Auth:** JWT.

### Слои
- `shared` — 4 модуля.
- `reference` — модели заклинаний, классов, фич, стратегий, `GuideService`.
- `domain` — модели персонажа, FSM, 14 actions, порты.
- `application` — 7 use cases.
- `identity` — auth.
- `infra` — SQLAlchemy, Redis.
- `api` — FastAPI, DTO, маппинг.

### Что показывает
- DDD-границы (Shared / Reference / Domain / Application / Identity).
- **Application слой** — оркестрация без бизнес-логики.
- TDD на ядре (без БД).
- Композиция над наследованием.
- FSM с rollback (Memento).
- Порты и адаптеры.
- FastAPI + SQLAlchemy + Alembic.
- Docker Compose.
- CI/CD.

### Что НЕ входит
- Combat (бой).
- Concentration, Conditions, Death Saves.
- Другие классы.
- Уровни 6-20.
- Мультикласс.
- Frontend.

### Срок
- **~3 месяца** при 15 ч/нед.
- **~5-6 месяцев** при 7-10 ч/нед (реалистично в декрете).

### Публикация
- GitHub + README + ADR + CHANGELOG.
- Deploy.
- Скриншоты Swagger.
- Диаграмма слоёв.

---

## 1.1.0 — Клирик

**Цель:** второй класс, другая модель заклинаний (prepared + domain spells).

### Что входит
- **Класс:** клирик.
- **Домен:** Life.
- **Заклинаний:** +20.
- **Always-prepared** заклинания от домена.
- **Prepared** из полного списка класса (не из книги).
- Channel Divinity (базовая).
- **Level-up с выбором домена.**

### Что меняется в слоях
- `reference` — новый `ClassData`, `SubclassData`, `PreparedSpellStrategy`, +20 заклинаний.
- `domain` — **без изменений** (стратегия уже поддержана).
- `application` — **без изменений** (use cases те же).
- `api` — новый эндпоинт выбора домена при level-up.

### Что показывает
- Стратегии реально разные (spellbook vs prepared + always-prepared).
- Работа **без рефакторинга** ядра — только новые данные и стратегия.
- Domain spells как отдельный список.

### Срок
- **~1 месяц**.

---

## 1.2.0 — Бард

**Цель:** третий класс, known-модель + CHANGE_SPELL.

### Что входит
- **Класс:** бард.
- **Коллегия:** Lore.
- **Заклинаний:** +20.
- **Known** заклинания (фиксированный список).
- **CHANGE_SPELL** на level-up.
- Bardic Inspiration (базовая).

### Что меняется в слоях
- `reference` — новый `ClassData`, `SubclassData`, `KnownSpellStrategy`, +20 заклинаний.
- `domain` — новая `ChangeSpellAction`.
- `application` — обновление `LevelUpService` (добавить шаг `CHANGE_SPELL`).
- `api` — новый эндпоинт замены заклинания.

### Что показывает
- Третья модель кастера (known + swap).
- CHANGE_SPELL в FSM.
- Все три модели работают через одну инфраструктуру.

### Срок
- **~1 месяц**.

---

## 1.3.0 — Полный справочник заклинаний

**Цель:** все заклинания PHB (и SRD) для трёх классов.

### Что входит
- **~200 заклинаний** для волшебника, клирика, барда.
- Парсер open5e / 5esrd.
- Все подклассы для трёх классов.
- Расширенные списки заклинаний.

### Что меняется в слоях
- `reference` — только данные.
- Остальные слои — **без изменений**.

### Срок
- **~2-3 недели**.

---

## 1.4.0 — Уровни 6-20

**Цель:** полный диапазон уровней для трёх классов.

### Что входит
- Таблицы `LevelProfile` для уровней 6-20.
- Заклинания уровней 4-9.
- Features на высоких уровнях.
- ASI на 8, 12, 16, 19.
- Spell Mastery (Wizard 18), Signature Spells (Wizard 20).

### Что меняется в слоях
- `reference` — данные.
- `domain` — новые actions для высокоуровневых фич (**если** появятся).
- `application` — обновление сборки шагов.

### Срок
- **~1 месяц**.

---

## 1.5.0 — Combat MVP

**Цель:** базовый трекер боя.

### Что входит
- `CombatContext` с action economy.
- `CombatStateMachine` (turn loop).
- Actions: Attack, Dash, Dodge, Disengage, Help, Hide, Ready, Search.
- Initiative.
- HP tracking для бойцов.
- Conditions (15 состояний PHB).
- Concentration (проверка при уроне).
- Death Saves.

### Что меняется в слоях
- `domain` — `CombatContext`, `CombatStateMachine`, новые actions, `Condition`, `Concentration`.
- `application` — новый `CombatService` (оркестрация боя).
- `api` — эндпоинты боя.
- `reference` — данные монстров, оружия, доспехов.

### Что показывает
- Расширение модели **без переделки** существующего.
- Разные контексты для одного `Action`.
- Работа с состоянием боя.

### Срок
- **~2 месяца**.

---

## 1.6.0 — DM Tools: Encounter Builder + Bestiary

**Цель:** инструменты мастера.

### Что входит
- Бестиарий (SRD монстры).
- Encounter builder: выбрать монстров, посчитать CR.
- Оценка сложности боя.
- Экспорт энкаунтера.

### Что меняется в слоях
- `reference` — бестиарий (монстры).
- `application` — `EncounterService`, `BestiaryService`.
- `api` — эндпоинты мастера.
- `domain` — если нужен `EncounterModel` (агрегат).

### Срок
- **~1.5 месяца**.

---

## 1.7.0 — Monte Carlo симулятор

**Цель:** анализ заклинаний и боёв.

### Что входит
- Симуляция боёв (100k+ итераций).
- Сравнение заклинаний.
- Оценка DPR.
- Баланс энкаунтеров.

### Что меняется в слоях
- `application` — `SimulationService`.
- `infra` — C++ через pybind11.
- `api` — эндпоинт симуляции.

### Что показывает
- Работа с C++ через pybind11.
- Производительность и оптимизация.
- Реальный инструмент для DM.

### Срок
- **~1 месяц**.

---

## 1.8.0 — DM Tools: Campaign Planner

**Цель:** ведение кампании.

### Что входит
- Создание кампании.
- NPC, локации, квесты.
- Заметки между сессиями.
- Timeline событий.
- Связь с персонажами игроков.

### Что меняется в слоях
- `domain` — новый агрегат `CampaignModel`.
- `application` — `CampaignService`.
- `reference` — если нужны справочники.
- `api` — эндпоинты кампании.
- **`application` тут оправдан полностью** — координация между `CampaignModel` и `CharacterModel`.

### Срок
- **~2 месяца**.

---

## 1.9.0 — Мультикласс

**Цель:** поддержка мультикласса в UI и API.

### Что входит
- `MulticlassSlotCalculator` (PHB p.164-165).
- Level-up с выбором нового класса.
- Pact magic отдельно (Warlock).
- Расчёт слотов по комбинации классов.

### Что меняется в слоях
- `reference` — `MulticlassSlotCalculator` (замена `SingleClassSlotCalculator`).
- `domain` — `CharacterModel` уже поддерживает `list[CharacterClass]`.
- `application` — обновление `LevelUpService`.
- `api` — эндпоинт выбора нового класса.

### Срок
- **~3 недели**.

---

## 1.10.0 — PWA (Mobile)

**Цель:** мобильный веб-клиент.

### Что входит
- React / Vue PWA.
- Лист персонажа.
- Каст заклинаний.
- Level-up через UI.
- Оффлайн-режим (снапшоты).
- Push-уведомления (заготовка).

### Что меняется в слоях
- Только `frontend/` + возможно `api/` (новые эндпоинты для PWA).
- Ядро — **без изменений**.

### Срок
- **~2-3 месяца**.

---

## 2.0.0 — Все классы D&D 5e

**Цель:** полное покрытие PHB.

### Что входит
- **13 классов:** barbarian, bard, cleric, druid, fighter, monk, paladin, ranger, rogue, sorcerer, warlock, wizard, artificer.
- **~100 подклассов.**
- **Все фичи** (Rage, Wild Shape, Ki, Superiority Dice, Metamagic, Eldritch Invocations, ...).
- **Полный справочник** заклинаний.
- **Feats.**

### Что меняется в слоях
- `reference` — **основная работа** (все данные).
- `domain` — новые actions для классовых фич.
- `application` — расширение use cases (например, `RageService`).
- `api` — новые эндпоинты для активации фич.

### Что показывает
- Архитектура выдержала **все** классы D&D.
- Модель фич, ресурсов, стратегий работает универсально.
- Расширение через добавление данных, не переделка.

### Срок
- **~6-9 месяцев.**

---

## 2.1.0 — Другие системы: Pathfinder 2e

**Цель:** поддержка второй системы.

### Что входит
- `RuleSystem` — абстракция над системами.
- `systems/pathfinder2e/` — отдельный модуль.
- Характеристики, фичи, заклинания Pathfinder.
- Общий Core (dice, auth, persistence) переиспользуется.

### Что меняется в слоях
- **`systems/`** — новый уровень модуля.
  - `systems/dnd5e/` — существующий код переезжает.
  - `systems/pathfinder2e/` — новый.
- `shared/` — общий.
- `application/` — общий.
- `api/` — роутеры с префиксом `/systems/{system}/...`.
- `identity`, `infra` — общие.

### Что показывает
- Правильные границы Core vs Systems.
- Абстракция **выяснилась** на **втором** потребителе.
- Реальная **расширяемость**.

### Срок
- **~3-4 месяца.**

---

## 2.2.0 — Cyberpunk RED / другие системы

**Цель:** третья система.

### Что меняется в слоях
- Новый `systems/cyberpunk_red/`.
- Остальное — переиспользуется.

### Срок
- **~3 месяца.**

---

## 2.3.0 — Shared Play (мультиплеер)

**Цель:** совместная игра.

### Что входит
- WebSocket для real-time.
- Multi-user сессии.
- DM видит персонажей игроков.
- Игроки видят броски друг друга.
- Чат в сессии.

### Что меняется в слоях
- `application` — `SessionService`, `BroadcastService`.
- `infra` — WebSocket, pub/sub (Redis).
- `api` — WebSocket-эндпоинты.
- `domain` — если нужен `SessionModel`.

### Что показывает
- Real-time инфраструктура.
- Coordination между пользователями.
- Event Sourcing (если понадобится для undo).

### Срок
- **~4-6 месяцев.**

---

## 2.4.0 — Homebrew Content

**Цель:** свои заклинания, классы, расы.

### Что входит
- Редактор заклинаний.
- Редактор фич.
- Экспорт / импорт homebrew пакетов.
- Публикация в community.

### Что меняется в слоях
- `reference` — расширение (user-defined контент).
- `application` — `HomebrewService`.
- `api` — эндпоинты редактора.
- `infra` — возможно, отдельная схема в БД.

### Срок
- **~3 месяца.**

---

## 2.5.0 — Map Editor (DM Tools)

**Цель:** редактор карт для боёв.

### Что входит
- Grid-based карты.
- Токены.
- Туман войны.
- Экспорт / импорт.
- Связь с Combat Tracker.

### Что меняется в слоях
- `domain` — `MapModel`.
- `application` — `MapService`.
- `infra` — storage для карт.
- `api` — эндпоинты редактора.
- Frontend — основной объём.

### Срок
- **~6 месяцев.**

---

## 3.0.0 — Полноценный помощник для D&D

**Цель:** всё в одном.

### Что входит
- **Все системы** (D&D 5e, Pathfinder 2e, Cyberpunk RED, ...).
- **Все классы** и подклассы.
- **Combat** с картами.
- **DM Tools** полностью.
- **Mobile** (PWA + native).
- **Shared Play** для групп.
- **Homebrew** для community.
- **Monte Carlo** для анализа.

### Что показывает
- Полноценный продукт.
- Годы работы.
- Архитектура, которая выдержала всё.

### Срок
- **Годы.**

---

## Приоритеты

### Обязательно (для найма)
- 1.0.0 — MVP.
- 1.1.0 — клирик.
- 1.2.0 — бард.

### Сильно желательно
- 1.3.0 — полный справочник.
- 1.4.0 — уровни 6-20.
- 1.5.0 — combat MVP.
- 1.9.0 — мультикласс.

### Для удовольствия (после найма)
- 1.6.0 — DM Tools.
- 1.7.0 — Monte Carlo.
- 1.8.0 — кампания.
- 1.10.0 — PWA.

### Долгосрочно
- 2.0.0 — все классы.
- 2.1.0+ — другие системы.
- 2.3.0 — shared play.
- 3.0.0 — полноценный помощник.

---

## Что НЕ входит в roadmap

- **VTT** (виртуальный стол с картами в реальном времени, как Roll20) — **отдельный** продукт.
- **Игра** (графика, анимации, 3D) — **отдельный** жанр.
- **Мобильные native apps** (iOS / Android) — **только** если PWA не хватит.
- **Монетизация** — **не** цель.
- **Сообщество** — **не** цель.

---

## Сроки (реалистично)

| Версия | При 15 ч/нед | При 7-10 ч/нед |
|---|---|---|
| 1.0.0 — MVP | 3 месяца | 5-6 месяцев |
| 1.1.0 — клирик | +1 месяц | +1.5 месяца |
| 1.2.0 — бард | +1 месяц | +1.5 месяца |
| 1.3.0 — справочник | +3 недели | +1 месяц |
| 1.4.0 — уровни 6-20 | +1 месяц | +1.5 месяца |
| 1.5.0 — combat MVP | +2 месяца | +3 месяца |
| 1.6.0 — bestiary | +1.5 месяца | +2 месяца |
| 1.7.0 — Monte Carlo | +1 месяц | +1.5 месяца |
| 1.8.0 — campaign | +2 месяца | +3 месяца |
| 1.9.0 — мультикласс | +3 недели | +1 месяц |
| 1.10.0 — PWA | +2-3 месяца | +4 месяца |
| 2.0.0 — все классы | +6-9 месяцев | +12 месяцев |

**До версии 1.5.0** (combat): **~1 год** при 15 ч/нед. **~1.5-2 года** при 7-10 ч/нед.

**До версии 2.0.0** (все классы): **~2.5 года** при 15 ч/нед. **~4 года** при 7-10 ч/нед.

---

## Что важно помнить

1. **Каждая версия — релиз.** Tag, CHANGELOG, публикация.
2. **Публикация с 1.0.0.** Не жди версии 3.0.0.
3. **Найм — на 1.0.0.** Остальное — **после** работы.
4. **Расширение — добавление данных и стратегий.** Не переделка.
5. **Combat — не приоритет.** Справка + каст достаточно для MVP.
6. **Другие системы — в конце.** D&D 5e сначала.
7. **Мобильный — PWA.** Не native.
8. **Порядок приоритетов:** найм → удовольствие → полнота.

---

## Одна фраза

**MVP → три класса → полный справочник → combat → DM Tools → все классы → другие системы → полноценный помощник.** Каждый шаг — работающий продукт. Первый — для найма. Остальное — для удовольствия.