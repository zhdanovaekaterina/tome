# 0003. Машина состояний с Memento для rollback

## Статус
Принято

## Контекст
Build и LevelUp — пошаговые процессы. Пользователь может ошибиться
и захотеть вернуться на шаг назад. Reset: новый персонаж → в начало build,
завершённый → в Play.

Event Sourcing — оверкилл для пет-проекта. Нужно простое решение.

## Решение
`StateMachine` + `HistoryManager` + `Memento`:
- Перед каждым изменением — `snapshot()` персонажа.
- `history.push(snapshot)`.
- `rollback()` — `history.pop()` + восстановление.
- `reset()` — по `is_build_complete()`.

## Последствия
**Проще:**
- Rollback на любом шаге бесплатно.
- Без Event Sourcing сложности.

**Сложнее:**
- Snapshot всего `CharacterModel` — память.
- В Redis — обрезать history до последнего snapshot.