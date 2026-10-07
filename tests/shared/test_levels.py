"""Tests for the level value objects (:mod:`core.shared.levels`)."""

import pytest

from shared.levels import CellLevel, ClassLevel


class TestCellLevel:
    """``CellLevel`` is a frozen value object constrained to 1..9."""

    @pytest.mark.parametrize("value", [1, 5, 9])
    def test_valid_values(self, value: int) -> None:
        assert CellLevel(value).value == value

    @pytest.mark.parametrize("value", [0, 10])
    def test_out_of_range_raises(self, value: int) -> None:
        with pytest.raises(ValueError, match="between 1 and 9"):
            CellLevel(value)


class TestClassLevel:
    """``ClassLevel`` is a frozen value object constrained to 1..20."""

    @pytest.mark.parametrize("value", [1, 10, 20])
    def test_valid_values(self, value: int) -> None:
        assert ClassLevel(value).value == value

    @pytest.mark.parametrize("value", [0, 21])
    def test_out_of_range_raises(self, value: int) -> None:
        with pytest.raises(ValueError, match="between 1 and 20"):
            ClassLevel(value)
