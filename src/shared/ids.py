"""Typed identifiers shared across the layers."""

from typing import NewType

__all__ = ["ClassId", "SubclassId"]


ClassId = NewType("ClassId", str)
SubclassId = NewType("SubclassId", str)
