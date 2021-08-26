__all__ = ["Value", "MatchedValue"]

from dataclasses import dataclass
from typing import Any, List

from regex.regex import Match

from maha.rexy import Expression, ExpressionGroup, ExpressionResult


@dataclass
class Value(Expression):
    """Expression that returns a predefined value if the pattern matches."""

    __slots__ = ["value"]
    value: Any

    def __init__(self, value: Any, pattern: str):
        self.value = value
        super().__init__(pattern)

    def parse(self, match: Match, _: str) -> "ExpressionResult":
        return ExpressionResult(match.start(), match.end(), self.value, self)

    def __hash__(self):
        return hash(self.pattern + str(self.value))


class MatchedValue(Value):
    """Expression that returns a predefined value of a matched expression from the input
    expressions"""

    def __init__(self, expressions: List[ExpressionGroup], pattern: str):
        super().__init__(expressions, pattern)

    def parse(self, match: Match, _: str) -> "ExpressionResult":
        value = self.value.get_matched_expression().value
        return ExpressionResult(match.start(), match.end(), value, self)
