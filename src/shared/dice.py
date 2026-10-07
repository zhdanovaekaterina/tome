"""Dice value objects: die types and dice-roll expressions."""

from dataclasses import dataclass
from enum import IntEnum

__all__ = ["DiceRoll", "DiceType"]


class DiceType(IntEnum):
    """A die type.

    The enum value is the number of faces of the die, so ``DiceType.D6 == 6``
    and ``DiceType.D20.sides == 20``.
    """

    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D100 = 100

    @property
    def sides(self) -> int:
        """The number of faces of the die."""
        return int(self)


@dataclass(frozen=True, slots=True)
class DiceRoll:
    """A frozen dice expression such as ``2d6``.

    The source diagram declares the operators as ``__add__`` and
    ``__multiply__``; multiplication is realised through the idiomatic Python
    operator pair ``__mul__`` / ``__rmul__``.
    """

    dice_count: int
    dice_type: DiceType

    def __post_init__(self) -> None:
        if self.dice_count < 1:
            msg = f"dice_count must be >= 1, got {self.dice_count}"
            raise ValueError(msg)

    def __str__(self) -> str:
        """Render the classic dice notation, e.g. ``"2d6"``."""
        return f"{self.dice_count}d{self.dice_type.sides}"

    def __add__(self, other: object) -> DiceRoll:
        """Combine two rolls of the same die type: ``2d6 + 1d6 == 3d6``."""
        if not isinstance(other, DiceRoll):
            return NotImplemented
        if self.dice_type is not other.dice_type:
            msg = f"cannot add dice rolls of different types: d{self.dice_type.sides} and d{other.dice_type.sides}"
            raise ValueError(msg)
        return DiceRoll(self.dice_count + other.dice_count, self.dice_type)

    def __mul__(self, factor: object) -> DiceRoll:
        """Scale the number of dice: ``2d6 * 3 == 6d6``."""
        if not isinstance(factor, int):
            return NotImplemented
        if factor < 1:
            msg = f"factor must be >= 1, got {factor}"
            raise ValueError(msg)
        return DiceRoll(self.dice_count * factor, self.dice_type)

    def __rmul__(self, factor: object) -> DiceRoll:
        """Support the reflected form ``3 * 2d6``."""
        return self.__mul__(factor)
