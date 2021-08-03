from typing import Optional

from regex.regex import Match

from ..interfaces import Expression, ExpressionResult
from .utils import get_value


class NumeralExpression(Expression):
    def parse(self, match: Match, text: Optional[str]) -> "ExpressionResult":

        start, end = match.span()
        groups = match.capturesdict()

        values = groups.get("value")
        units = groups.get("unit")

        # if not units, then it's ones or tens
        if not units:
            return ExpressionResult(start, end, get_value(values[0]), self)

        for value, unit in zip(values, units):
            pass
