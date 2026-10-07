"""Shared value objects.

The lowest layer of the architecture: it must not depend on any other layer
(``API -> Domain -> Reference -> Shared``), while everything else may depend on it.
"""

from shared.dice import DiceRoll, DiceType
from shared.enums import Ability
from shared.ids import ClassId, SubclassId
from shared.levels import CellLevel, ClassLevel

__all__ = [
    "Ability",
    "CellLevel",
    "ClassId",
    "ClassLevel",
    "DiceRoll",
    "DiceType",
    "SubclassId",
]
