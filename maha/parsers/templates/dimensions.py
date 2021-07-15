__all__ = ["Dimension", "UnitDimension"]

from dataclasses import dataclass
from typing import List, Union

from .types import DimensionType, Unit


@dataclass
class Dimension:
    """Template for the parsed item"""

    expression: Union[List[str], str]
    """Regular expersion(s) to match"""
    value: str
    r"""Extracted value, whether a simple exp or captured groups (\1\2...)"""
    start: int
    """Start index of the value in the text"""
    end: int
    """End index of the value in the text"""
    is_confident: bool
    """Whether the extracted value 100% belongs to the selected dimension. Some patterns
    may match for values that normally belong to the dimension but not always."""
    dimension: DimensionType
    """Dimension type."""


@dataclass
class UnitDimension(Dimension):
    """Dimension with unit"""

    unit: Unit
    """Unit of the dimension"""
