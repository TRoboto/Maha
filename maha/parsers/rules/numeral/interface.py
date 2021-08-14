__all__ = ["NumeralExpression"]

from typing import Optional

from regex.regex import Match

from maha.rexy import Expression, ExpressionResult

from .utils import get_matched_numeral, get_value


class NumeralExpression(Expression):
    def parse(self, match: Match, text: Optional[str]) -> "ExpressionResult":

        start, end = match.span()
        groups = match.capturesdict()

        values = groups.get("value")
        multiplier = groups.get("multiplier")

        output = 0
        for value, multiplier in zip(values, multiplier):
            output += self.get_numeral_value(value, multiplier)

        return ExpressionResult(start, end, output, self)

    def get_numeral_value(self, value: str, multiplier: str) -> int:
        # if not multiplier, then it's ones or tens
        if not multiplier:
            return get_value(value)

        output = get_matched_numeral(multiplier)
        if value:
            output *= get_value(value)
        return output