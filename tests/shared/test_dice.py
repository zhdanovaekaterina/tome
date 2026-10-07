"""Tests for the dice value objects (:mod:`core.shared.dice`)."""

import pytest

from shared.dice import DiceRoll, DiceType


class TestDiceRollConstruction:
    """Building and describing a :class:`DiceRoll`."""

    def test_dice_count_must_be_positive(self) -> None:
        with pytest.raises(ValueError):
            DiceRoll(dice_count=-1, dice_type=DiceType.D6)

    def test_equality(self) -> None:
        assert DiceRoll(2, DiceType.D6) == DiceRoll(2, DiceType.D6)
        assert DiceRoll(2, DiceType.D6) != DiceRoll(3, DiceType.D6)
        assert DiceRoll(2, DiceType.D6) != DiceRoll(2, DiceType.D8)


class TestDiceRollAdd:
    """``DiceRoll.__add__``."""

    def test_add_same_type_sums_counts(self) -> None:
        assert DiceRoll(2, DiceType.D6) + DiceRoll(3, DiceType.D6) == DiceRoll(
            5,
            DiceType.D6,
        )

    def test_add_different_types_raises(self) -> None:
        with pytest.raises(ValueError):
            DiceRoll(1, DiceType.D6) + DiceRoll(1, DiceType.D8)

    def test_add_non_dice_roll_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            DiceRoll(1, DiceType.D6) + 5


class TestDiceRollMul:
    """``DiceRoll.__mul__`` / ``__rmul__``."""

    def test_mul_scales_count(self) -> None:
        assert DiceRoll(2, DiceType.D6) * 3 == DiceRoll(6, DiceType.D6)

    def test_rmul_scales_count(self) -> None:
        assert 3 * DiceRoll(2, DiceType.D6) == DiceRoll(6, DiceType.D6)

    def test_mul_factor_must_be_positive(self) -> None:
        with pytest.raises(ValueError):
            DiceRoll(2, DiceType.D6) * -1

    def test_mul_non_int_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            DiceRoll(2, DiceType.D6) * "2"
