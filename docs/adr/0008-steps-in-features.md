# 0008. Шаги build/level-up — в фичах

## Статус
Принято

## Контекст
Изначально шаги FSM жили в `SpellStrategyDefinition` — только у кастеров.
Но варвар тоже level-up делает. Паладин тоже. Значит, шаги — не про кастеров.

## Решение
- `FeatureDefinition.build_steps() -> list[BuildActions]`
- `FeatureDefinition.levelup_steps() -> list[LevelupActions]`
- `StepCollector` собирает шаги из всех новых фич + дедупликация.
- Универсальные шаги (CALCULATE, RECALCULATE_HP) — добавляет сервис.

## Последствия
**Проще:**
- Build и LevelUp симметричны.
- Варвар, плут, паладин — все через один механизм.
- Новая фича с шагами — не трогает сервис.

**Сложнее:**
- `deduplicate` шагов.
- Универсальные шаги отдельно.