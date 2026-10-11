# 0009. Шаги — enum в Reference, actions — в Domain

## Статус
Принято

## Контекст
Шаги FSM и их выполнение — разные слои.
Reference знает «бывает шаг LEARN_SPELLS».
Domain знает «как выполнить LEARN_SPELLS».

## Решение
- `BuildActions`, `LevelupActions` — enum в Reference.
- `Action` — ABC в Domain с полем `step`.
- `BUILD_STEP_REGISTRY`, `LEVELUP_STEP_REGISTRY` — `dict[enum, type[Action]]`.
- FSM: `dispatch(character, action, context)` — проверяет `action.step == current_step`.

## Последствия
**Проще:**
- Reference — данные (enum). Domain — поведение (Action).
- UI знает шаги (enum), не знает actions.
- Сериализация FSM — список enum + индекс.

**Сложнее:**
- Два реестра.
- Actions общие между build и level-up (LearnSpellsAction).