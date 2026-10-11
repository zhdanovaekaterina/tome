# 0002. Композиция вместо наследования для заклинаний

## Статус
Принято

## Контекст
Заклинания имеют разные оси: как разрешается (attack/save/auto),
что делает (damage/heal/control), как усиливается (upcast),
на кого (one/multiple/area).

Иерархия `SpellType <|-- Damage <|-- AttackRoll` не выражает:
- Ice Storm — два эффекта (damage + control).
- Scorching Ray — три атаки, три эффекта.
- Magic Missile — auto, но с целями по upcast.

## Решение
Две независимые оси списками:
- `SpellData.resolutions: List[Resolution]` — как разрешается.
- `SpellData.effects: List[Effect]` — что делает.
- `Effect.upcast: Upcast | None` — усиление.

## Последствия
**Проще:**
- Любое заклинание выражается без хаков.
- Новые эффекты — новый `EffectKind`, не новый класс.

**Сложнее:**
- Множественные эффекты требуют логики в Domain (какой эффект при каком resolution).