__all__ = ["Dimension"]

from dataclasses import dataclass
from typing import Optional, Union

from .expressions import Expression
from .types import DimensionType, Unit


@dataclass
class Dimension:
    """Template for the parsed item"""

    __slots__ = [
        "expression",
        "body",
        "value",
        "start",
        "end",
        "dimension_type",
        "unit",
    ]

    expression: Expression
    """The expression that was used to find the value"""
    body: str
    """Text from the input that was matched by the expression."""
    value: Union[float, str]
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
        body: str,
        value: Union[float, str],
        start: int,
        end: int,
        dimension_type: DimensionType,
    ):
        self.expression = expression
        self.body = body
        self.value = value
        self.start = start
        self.end = end
        self.dimension_type = dimension_type
        self.unit = self.expression.unit

    def __repr__(self):
        out = (
            f"Dimension(body={self.body}, value={self.value}, unit={self.unit}, start={self.start}, "
            f"end={self.end}, dimension_type={self.dimension_type}"
        )
        return out
