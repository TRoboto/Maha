__all__ = ["Dimension", "Expression"]

from dataclasses import dataclass, field
from typing import Optional

from .types import DimensionType, Unit


@dataclass
class Expression:
    __slots__ = ["pattern", "is_confident", "output"]

    pattern: str
    """Regular expersion(s) to match"""
    is_confident: bool
    """Whether the extracted value 100% belongs to the selected dimension. Some patterns
    may match for values that normally belong to the dimension but not always."""
    output: Optional[str]
    """
    Whether a simple exp or captured groups (\1\2...). Expressions with captured groups
    are also supported. For instance, the following pattern: ``\1 + \2`` will sum up
    the values of the captured groups.

    When ``output`` is set to ``None``, the value is extracted from text
    """

    def __init__(
        self, pattern: str, is_confident: bool = False, output: Optional[str] = None
    ):
        self.pattern = pattern
        self.is_confident = is_confident
        self.output = output

    def __repr__(self):
        out = f"Expression(pattern={self.pattern}, is_confident={self.is_confident}"
        if self.output:
            return out + f", output={self.output})"
        return out + ")"


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
    start: int
    """Start index of the value in the text"""
    end: int
    """End index of the value in the text"""
    dimension_type: DimensionType
    """Dimension type."""
    unit: Optional[Unit]
    """Unit of the dimension"""

    def __init__(
        self,
        matched_expression: Expression,
        value: str,
        start: int,
        end: int,
        dimension_type: DimensionType,
        unit: Optional[Unit] = None,
    ):
        self.matched_expression = matched_expression
        self.value = value
        self.start = start
        self.end = end
        self.dimension_type = dimension_type
        self.unit = unit

    def __repr__(self):
        out = (
            f"Dimension(matched_expression={self.matched_expression}, "
            f"value={self.value}, start={self.start}, end={self.end}, "
            f"dimension_type={self.dimension_type}"
        )
        if self.unit:
            return out + f", unit={self.unit})"
        return out + ")"
