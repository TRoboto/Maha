__all__ = ["Value", "MatchedValue", "FunctionValue"]

from typing import Any, Callable

from regex.regex import Match

from maha.rexy import Expression, ExpressionGroup, ExpressionResult


class Value(Expression):
    """Expression that returns a predefined value if the pattern matches."""

    __slots__ = ["value"]
    value: Any

    def __init__(self, value: Any, pattern: str, pickle: bool = False):
        self.value = value
        super().__init__(pattern, pickle)

    def _parse(self, match: Match, _: str) -> ExpressionResult:
        return ExpressionResult(match.start(), match.end(), self.value, self)


class MatchedValue(Value):
    """
    Expression that returns a predefined value of a matched expression from the input
    expressions

    Parameters
    ----------
    expressions : ExpressionGroup
        The expressions to match
    pattern : str
        The pattern to match

    Returns
    -------
    ExpressionResult
        The result of the expression
    """

    def __init__(self, expressions: ExpressionGroup, pattern: str):
        super().__init__(expressions, pattern)

    def _parse(self, match: Match, _: str) -> ExpressionResult:
        matched_text = match.group(0)
        value = self.value.get_matched_expression(matched_text).value
        return ExpressionResult(match.start(), match.end(), value, self)


class FunctionValue(Value):
    """
    Expression that returns the output value of an input function when matched.

    Parameters
    ----------
    function : Callable
        The function to be called when the pattern matches.
    pattern : str
        The pattern to be matched.

    Returns
    -------
    ExpressionResult
        The result of the expression.
    """

    def __init__(self, function: Callable[..., Any], pattern: str, pickle: bool = True):
        super().__init__(function, pattern, pickle)

    def _parse(self, match: Match, _: str) -> ExpressionResult:
        value = self.value(match)
        return ExpressionResult(match.start(), match.end(), value, self)
