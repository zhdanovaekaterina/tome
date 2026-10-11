# 0012. Использование ABC и Protocol в интерфейсах

## Статус
Принято

## Контекст
Protocol — структурная типизация. Но не даёт гарантии реализации.
ABC — даёт гарантию при создании.

## Решение
ABC — для своих классов (FeatureContainer, FeatureDefinition, SpellStrategyDefinition).
Protocol — для портов (SpellRepository, CharacterRepository).
mypy strict в CI — обязательно.
@runtime_checkable — только на границах.

## Последствия
**Проще:**
Свои классы — гарантия реализации.
Чужие классы — структурно подходят.

**Сложнее:**
Два механизма.
Нужен mypy в CI.