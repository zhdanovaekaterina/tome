# 0005. Черновики персонажей в Redis

## Статус
Принято

## Контекст
Незавершённый персонаж (Build / LevelUp) — временный. Завершённый (Play) — постоянный.
Хранить всё в Postgres — дорого по запросам. Хранить всё в Redis — потеря при падении.

## Решение
- **Redis** — черновики (mode=BUILD / LEVEL_UP), TTL 7 дней.
- **Postgres** — завершённые (mode=PLAY).
- `CharacterRepository` (один порт) — реализация `HybridCharacterRepository` маршрутизирует.
- Переход: сначала Postgres, потом удаление из Redis.

## Последствия
**Проще:**
- Быстрое сохранение черновика.
- Ядро не знает о Redis.

**Сложнее:**
- Сериализация `CharacterModel` (data + state machine).
- Optimistic locking через `version`.