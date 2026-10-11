# Архитектура

## Слои

```
┌─────────────────────────────────────┐
│ API (FastAPI) │ ← delivery
│ - routers, schemas, deps │
└─────────────┬───────────────────────┘
│
┌─────────────▼───────────────────────┐
│ Application │ ← use cases (оркестрация)
│ - BuildService, LevelUpService │
│ - CastService, RestService │
│ - SpellListService, CharacterFactory│
└─────────────┬───────────────────────┘
│
┌─────────────▼───────────────────────┐
│ Domain │ ← бизнес-логика персонажа
│ - CharacterModel, StateMachine │
│ - CharacterSpells, CharacterSlots │
│ - Actions, HistoryManager, Memento │
└─────────────┬───────────────────────┘
│
┌─────────────▼───────────────────────┐
│ Reference │ ← справочники
│ - SpellData, ClassData │
│ - LevelProfile, SlotCalculator │
│ - SpellStrategyDefinition, Features │
└─────────────┬───────────────────────┘
│
┌─────────────▼───────────────────────┐
│ Shared │ ← value-objects
│ - DiceRoll, Ability, SpellId │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Identity │ ← auth (параллельно)
│ - AuthService, TokenService │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Infra │ ← реализации портов
│ - SqlAlchemy, Redis, Bcrypt, JWT │
└─────────────────────────────────────┘
```

## Правило зависимостей

```
API → Application → Domain → Reference → Shared
API → Identity
Application → Domain, Reference, Shared, Identity (только UserId)
Domain → Reference, Shared
Reference → Shared
Identity → Shared
Infra → (реализует порты всех слоёв)
```



**Запрещено:**

- Reference → Domain.
- Reference → Application.
- Shared → что угодно из проекта.
- Domain → API.
- Domain → Application.
- Domain → Infra (только через Protocol).
- Application → API.
- Application → Infra (только через Protocol).
- Identity → Domain, Application, Reference.

## Что где живёт

| Слой | Что | Примеры |
|---|---|---|
| **Shared** | value-objects, enum'ы | `DiceRoll`, `Ability`, `SpellId`, `ClassId`, `RestKind` |
| **Reference** | справочники | `SpellData`, `ClassData`, `LevelProfile`, `FeatureDefinition`, `SpellStrategyDefinition` |
| **Domain** | состояние персонажа + FSM + actions | `CharacterModel`, `StateMachine`, `Action`, `CharacterSpells`, `CharacterSlots` |
| **Application** | use cases, оркестрация | `BuildService`, `LevelUpService`, `CastService`, `RestService`, `SpellListService`, `CharacterFactory`, `CharacterService` |
| **Identity** | аутентификация | `UserModel`, `AuthService`, `TokenService` |
| **Infra** | реализации портов | `SqlAlchemySpellRepository`, `RedisDraftRepository`, `BcryptHasher`, `JwtIssuer` |
| **API** | FastAPI + DTO | routers, Pydantic schemas, mappers, DI |

## Связь Identity и Domain

**Только через `UserId`** (value-object). `CharacterModel.user_id: UserId`.
Domain **не знает** о `UserModel`. Application получает `user_id` от API и передаёт в domain.

## Связь Domain и Reference

**Только через ID** (`SpellId`, `ClassId`, `SubclassId`).
Domain **не хранит** `SpellData` внутри. Application резолвит через `SpellRepository` на границе.

## Связь Application и Domain

- Application **вызывает** методы Domain-моделей (`character.spells.add(...)`).
- Application **не** содержит бизнес-логику — только **оркестрацию**.
- Domain **не знает** про Application.
- Application **не возвращает** DTO. DTO — только в API.

## Связь Application и Infra

- Application зависит от **портов** (`Protocol`): `CharacterRepository`, `SpellRepository`, `ClassRepository`.
- Application **не знает** про SQLAlchemy, Redis, bcrypt.
- Реализации портов — в Infra. Инжектятся в `api/main.py`.

## Схема стыка (ID vs объект)

```python
# Domain — хранит только ID
class CharacterSpell:
    id: SpellId          # ← не SpellData
    sources: list[SpellSourceRecord]

# Application (CastService) — резолвит через репозиторий
class CastService:
    def cast(self, character: CharacterModel, spell_id: SpellId, slot_level: CellLevel) -> CastResult:
        spell_data = self.spell_repo.find(spell_id)
        ...
```

## Схема стыка (модель → DTO)

```python
# API — маппинг модель → DTO
@router.get("/characters/{id}/status")
def get_status(id: CharacterId, facade: CharacterFacade = Depends(...)) -> CharacterStatusDTO:
    character = facade.get_character(id)
    return CharacterStatusDTO.from_domain(character, spell_repo)
```

DTO только в API. Ни Application, ни Domain не знают про Pydantic.