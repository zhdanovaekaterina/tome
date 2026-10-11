# 0007. Классификация фич

## Статус
Принято

## Контекст
`FeatureDefinition` с 30 полями — God object.
Rage (тратит ресурс, даёт resistance) и Expertise (пассивно) — разные.

## Решение
10 типов фич:
1. `ResourceManagementFeature` — даёт ресурс (Rage, Ki).
2. `SkillEnhancementFeature` — усиливает навыки (Expertise).
3. `CombatModifierFeature` — боевые бонусы (Fighting Style).
4. `CantripFeature` — заговоры.
5. `LeveledSpellFeature` — заклинания 1+.
6. `ResistanceFeature` — сопротивления.
7. `MovementFeature` — движение.
8. `ActiveAbilityFeature` — активируемые (Channel Divinity).
9. `PassiveAbilityFeature` — пассивные (Danger Sense).
10. `ProficiencyFeature` — владения.
11. `AbilityScoreImprovementFeature` — ASI (фича-выбор).
12. `NarrativeFeature` — нарративные (Shelter of the Faithful).

Domain работает через `isinstance` — полиморфно.

## Последствия
**Проще:**
- Каждый тип — свои поля.
- Новый тип — новый класс.
- Тесты на каждый тип отдельно.

**Сложнее:**
- Больше классов.
- `isinstance` в Domain.