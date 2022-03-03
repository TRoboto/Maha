__all__ = ["TextExpression"]

from regex.regex import Match

from maha.rexy import Expression, ExpressionResult


class TextExpression(Expression):
    """Expression that returns the matched text as value"""

    def _parse(self, match: Match, text: str) -> ExpressionResult:
        return ExpressionResult(
            match.start(), match.end(), text[match.start() : match.end()], self
        )
