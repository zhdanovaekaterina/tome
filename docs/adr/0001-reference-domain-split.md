# 0001. Разделение на Reference / Domain / Identity

## Статус
Принято

## Контекст
Проект — помощник для НРИ (D&D 5e). Домен сложный:
справочники (заклинания, классы, расы), состояние персонажа
(характеристики, слоты, prepared), аутентификация.

Нужно: менять справочники независимо от логики,
тестировать ядро без БД, добавлять новые системы (Pathfinder).

## Решение
Три слоя с правилом зависимостей:

- **Shared** — value-objects (DiceRoll, Ability, SpellId).
- **Reference** — справочники (SpellData, ClassData, LevelProfile).
- **Domain** — состояние и логика (CharacterModel, StateMachine, Actions).
- **Identity** — аутентификация (AuthService).

Зависимости: `API → Domain → Reference → Shared`. Domain → Identity только через `UserId`.

## Последствия
**Проще:**
- Справочники меняются без пересборки Domain.
- Domain тестируется без БД и API.
- Новые системы (Pathfinder) — новый модуль рядом.

**Сложнее:**
- Больше классов и интерфейсов.
- Резолв ID → объект (SpellId → SpellData) на границе API.