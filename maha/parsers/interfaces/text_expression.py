__all__ = ["TextExpression"]

from regex.regex import Match

from .expression import Expression
from .expression_result import ExpressionResult


class TextExpression(Expression):
    """
    Expression that returns the matched text as value
    """

    def parse(self, match: Match, text: str) -> "ExpressionResult":
        return ExpressionResult(
            match.start(), match.end(), text[match.start() : match.end()], self
        )
