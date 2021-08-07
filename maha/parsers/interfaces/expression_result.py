__all__ = ["ExpressionResult"]

from dataclasses import dataclass
from typing import Any

import maha.parsers.interfaces as interfaces


@dataclass
class ExpressionResult:
    """
    A result of a single expression.
    """

    __slots__ = ["start", "end", "value", "expression"]

    start: int
    """Start index of the matched text"""
    end: int
    """End index of the matched text"""
    value: Any
    """Extracted value"""
    expression: interfaces.Expression
    """The expression that was used to find the value"""
