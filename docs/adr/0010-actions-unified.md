# 0010. Actions - унифицированы

## Статус
Принято

## Контекст
Build, LevelUp, Combat, Exploration — все действия.
Изначально думали об отдельных иерархиях (BuildAction, CombatAction).
Но LearnSpellsAction общий для Build и LevelUp.

## Решение
Один Action ABC.
Разные реестры: BUILD_STEP_REGISTRY, LEVELUP_STEP_REGISTRY, COMBAT_REGISTRY.
Разные контексты: StepContext, CombatContext, ExplorationContext.
ActionType — метка (ACTION, BONUS_ACTION, REACTION, FREE, PASSIVE).
ActionEconomy — только в CombatContext.

## Последствия
**Проще:**
Одна инфраструктура.
Action может использоваться в разных контекстах.
Фича даёт actions через granted_action_keys().

**Сложнее:**
Actions знают про контекст (isinstance).
Три реестра.