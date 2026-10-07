"""Shared enums for the project."""

from enum import StrEnum

__all__ = ["Ability"]


class Ability(StrEnum):
    """The six ability scores of a creature."""

    STR = "strength"
    DEX = "dexterity"
    CON = "constitution"
    INT = "intelligence"
    WIS = "wisdom"
    CHA = "charisma"
