__all__ = ["Dimension"]

from dataclasses import dataclass
from typing import Any

from maha.rexy import Expression

from .enums import DimensionType


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
    ]

    expression: Expression
    """The expression that was used to find the value"""
    body: str
    """Text from the input that was matched by the expression."""
    value: Any
    """Extracted value"""
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
        value: Any,
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

    def __repr__(self):
        out = (
            f"Dimension(body={self.body}, value={self.value}, start={self.start}, "
            f"end={self.end}, dimension_type={self.dimension_type})"
        )
        return out
