__all__ = ["ValueExpression"]

from dataclasses import dataclass
from typing import Any

from regex.regex import Match

from .expression import Expression
from .expression_result import ExpressionResult


@dataclass
class ValueExpression(Expression):
    """
    Expression that returns a predefined value if the pattern matches.
    """

    __slots__ = ["value"]
    value: Any

    def __init__(self, pattern, value: Any):
        self.value = value
        super().__init__(pattern)

    def parse(self, match: Match, _: str) -> "ExpressionResult":
        return ExpressionResult(match.start(), match.end(), self.value, self)
