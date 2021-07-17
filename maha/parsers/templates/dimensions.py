__all__ = ["Dimension", "Expression"]

from dataclasses import dataclass
from typing import Callable, Optional

from .types import DimensionType, Unit


@dataclass
class Expression:
    __slots__ = ["pattern", "is_confident", "output", "unit"]

    pattern: str
    """Regular expersion(s) to match"""
    is_confident: bool
    """Whether the extracted value 100% belongs to the selected dimension. Some patterns
    may match for values that normally belong to the dimension but not always."""
    output: Callable[..., str]
    """
    A function to operate on the extracted value.

    When ``output`` is set to ``None``, the extracted value is returned as-is.
    """
    unit: Optional[Unit]
    """Unit of the dimension"""

    def __init__(
        self,
        pattern: str,
        is_confident: bool = False,
        output: Callable[..., str] = None,
        unit: Optional[Unit] = None,
    ):
        self.pattern = pattern
        self.is_confident = is_confident
        self.unit = unit
        if output is None:
            self.output = lambda *args: "".join(args)

    def __repr__(self):
        out = f"Expression(pattern={self.pattern}, is_confident={self.is_confident})"
        return out

    def format(self, format_spec: str):
        self.pattern = self.pattern.format(format_spec)
        return self

    def set_unit(self, unit: Unit):
        self.unit = unit
        return self


@dataclass
class Dimension:
    """Template for the parsed item"""

    __slots__ = [
        "matched_expression",
        "value",
        "start",
        "end",
        "dimension_type",
        "unit",
    ]

    matched_expression: Expression
    """Expression(s) to match"""
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
        matched_expression: Expression,
        value: str,
        start: int,
        end: int,
        dimension_type: DimensionType,
    ):
        self.matched_expression = matched_expression
        self.value = value
        self.start = start
        self.end = end
        self.dimension_type = dimension_type
        self.unit = self.matched_expression.unit

    def __repr__(self):
        out = (
            f"Dimension(matched_expression={self.matched_expression}, "
            f"value={self.value}, unit={self.unit}, start={self.start}, "
            f"end={self.end}, dimension_type={self.dimension_type}"
        )
        return out
