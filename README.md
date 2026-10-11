# Tome

> Бэкенд помощника для игровых сессий в настольных ролевых играх: лист персонажа, управление заклинаниями и ресурсами для D&D 5e.

[![python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/)
[![license](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![changelog](https://img.shields.io/badge/changelog-orange)](./CHANGELOG.md)
[![roadmap](https://img.shields.io/badge/roadmap-violet)](./docs/roadmap.md)

---

## Что это

**Tome** — это **интерактивный рулбук и лист персонажа** для игровых сессий в НРИ.

Помогает игрокам:
- отслеживать состояние персонажа, ресурсы и ячейки заклинаний,
- управлять заклинаниями (изучать, подготавливать, кастовать, усиливать ячейкой),
- повышать уровень по правилам (ASI, заговоры, книга заклинаний, доменные заклинания).

Проект задуман как **полноценный помощник для сессий** — и для игроков, и для мастера:
- трекер боя, бестиарий, конструктор энкаунтеров (инструменты мастера),
- планировщик кампании, редактор карт,
- поддержка других систем (Pathfinder 2e, Cyberpunk RED).

**Статус:** в разработке. Начинаем с **D&D 5e**, одного класса (волшебник), уровни 1–5. Без мультикласса.

---

## Зачем

- **Нет русскоязычного аналога** D&D Beyond.
- **Универсальность** — не привязан к одной системе.
- **Симуляция Монте-Карло** для анализа заклинаний и боёв (в планах).
- **Инструменты мастера** в одном месте с инструментами игрока (в планах).

---

## Стек

| Слой | Технология |
|---|---|
| Язык | Python 3.14 |
| API | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Миграции | Alembic |
| БД | PostgreSQL 16 |
| Кеш / черновики | Redis 7 |
| Тесты | pytest |
| Линт / типы | ruff, mypy (strict) |
| CI | GitHub Actions |
| Логирование | structlog |

---

## Архитектура

```
┌─────────────────────────────────────┐
│ API (FastAPI)                       │ ← delivery
│ routers, schemas, deps              │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│ Application                         │ ← use cases, оркестрация
│ BuildService, LevelUpService,       │
│ CastService, RestService,           │
│ SpellListService, CharacterFactory  │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│ Domain                              │ ← бизнес-логика персонажа
│ CharacterModel, StateMachine,       │
│ Actions, CharacterSpells            │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│ Reference                           │ ← справочники
│ SpellData, ClassData,               │
│ LevelProfile, SpellStrategy         │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│ Shared                              │ ← value-objects
│ DiceRoll, Ability, SpellId          │
└─────────────────────────────────────┘

Identity (аутентификация) — отдельный, параллельный слой.
Infrastructure реализует порты, объявленные в слоях выше.
```

**Правило зависимостей:** `API → Application → Domain → Reference → Shared`. Циклов нет.
Domain не знает про Application, Application не знает про API, Reference не знает про Domain.

---

## Структура проекта

```
src/
├── api                 # FastAPI роутеры, схемы, DI
├── application         # сервисы, use cases
├── domain              # CharacterModel, StateMachine
├── identity            # аутентификация (AuthService, TokenService)
├── infrastructure      # SQLAlchemy, Redis, реализации портов
├── reference           # справочники (SpellData, ClassData, LevelProfile)
└── shared              # value-objects (DiceRoll, Ability, SpellId)
tests/
docs/                   # архитектура, ADR, доменная модель
```

---

## Scope (MVP)

**Входит:**
- Класс: волшебник (spellbook)
- Уровни 1–5
- 20 заклинаний
- Use cases: build, level-up, cast, short rest, long rest
- JWT-аутентификация (register, login, logout, refresh)
- Postgres для постоянного хранения, Redis для черновиков
- Docker Compose

**Не входит (пока):**
- Другие классы (воин, друид, монах, ...)
- Уровни 6–20
- Полный справочник заклинаний
- Инструменты мастера (трекер боя, бестиарий, кампания)
- Мобильное / веб-приложение
- Другие системы (Pathfinder, Cyberpunk)

---

## Ключевые архитектурные решения

- `0001` — Разделение на Reference / Domain / Identity
- `0002` — Композиция вместо наследования для заклинаний (`Resolution` + `Effect`)
- `0003` — Машина состояний с Memento для откатов
- `0004` — Learn и Prepare как разные оси
- `0005` — Черновики персонажей в Redis, завершённые — в Postgres

---

## Правовая информация

- Используется контент **SRD 5.1**, лицензированный под **CC BY 4.0**.
- Проект не связан с Wizards of the Coast и не одобрен ими.
- «Dungeons & Dragons» и «D&D» — торговые марки Wizards of the Coast.
- Код проекта лицензирован под **MIT** (см. [`LICENSE`](./LICENSE)).

---

## Лицензия

MIT — см. [`LICENSE`](./LICENSE).

---

## Автор

Екатерина Жданова — zhdanova.ekaterina.95@yandex.ru — https://t.me/oxyiramus

Если ты играешь в D&D и хочешь попробовать Tome — напиши. Обратная связь приветствуется.