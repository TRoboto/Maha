__all__ = ["Dimension"]

from dataclasses import dataclass
from typing import Optional

from .expressions import Expression
from .types import DimensionType, Unit


@dataclass
class Dimension:
    """Template for the parsed item"""

    __slots__ = [
        "expression",
        "value",
        "start",
        "end",
        "dimension_type",
        "unit",
    ]

    expression: Expression
    """The expression that was used to find the value"""
    value: str
    """Extracted value"""
    unit: Optional[Unit]
    """Unit of the dimension"""
    start: int
    """Start index of the value in the text"""
    end: int
    """End index of the value in the text"""
    dimension_type: DimensionType
    """Dimension type."""

    def __init__(
        self,
        expression: Expression,
        value: str,
        start: int,
        end: int,
        dimension_type: DimensionType,
    ):
        self.expression = expression
        self.value = value
        self.start = start
        self.end = end
        self.dimension_type = dimension_type
        self.unit = self.expression.unit

    def __repr__(self):
        out = (
            f"Dimension(value={self.value}, unit={self.unit}, start={self.start}, "
            f"end={self.end}, dimension_type={self.dimension_type}"
        )
        return out
