"""Constrained level value objects."""

from dataclasses import dataclass

from shared.const import MAX_CLASS_LEVEL, MAX_SLOT_LEVEL, MIN_CLASS_LEVEL, MIN_SLOT_LEVEL

__all__ = ["CellLevel", "ClassLevel"]


@dataclass(frozen=True, slots=True)
class CellLevel:
    """A spell-slot level, from 1 to 9."""

    value: int

    def __post_init__(self) -> None:
        if not MIN_SLOT_LEVEL <= self.value <= MAX_SLOT_LEVEL:
            msg = f"CellLevel must be between {MIN_SLOT_LEVEL} and {MAX_SLOT_LEVEL}, got {self.value}"
            raise ValueError(msg)

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class ClassLevel:
    """A class level, from 1 to 20."""

    value: int

    def __post_init__(self) -> None:
        if not MIN_CLASS_LEVEL <= self.value <= MAX_CLASS_LEVEL:
            msg = f"ClassLevel must be between {MIN_CLASS_LEVEL} and {MAX_CLASS_LEVEL}, got {self.value}"
            raise ValueError(msg)

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)
