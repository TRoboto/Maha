__all__ = ["Dimension", "UnitDimension", "DimensionPattern", "UnitDimensionPattern"]

from dataclasses import dataclass
from typing import List, NamedTuple, Union

from .types import DimensionType, Unit


@dataclass
class Dimension:
    """Template for the parsed item"""

    __slots__ = [
        "expression",
        "value",
        "start",
        "end",
        "is_confident",
        "dimension",
    ]

    expression: Union[List[str], str]
    """Regular expersion(s) to match"""
    value: str
    """Extracted value"""
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

    __slots__ = ["unit"]
    unit: Unit
    """Unit of the dimension"""


@dataclass(init=False)
class DimensionPattern(Dimension):
    """Dimension with pattern"""

    __slots__ = ["output"]

    output: str
    """
    Whether a simple exp or captured groups (\1\2...). Expressions with captured groups
    are also supported. For instance, the following pattern: ``\1 + \2`` will sum up
    the values of the captured groups.
    """

    def __init__(self):
        pass


@dataclass(init=False)
class UnitDimensionPattern(DimensionPattern):
    """Dimension with unit"""

    __slots__ = ["unit"]
    unit: Unit
    """Unit of the dimension"""
