__all__ = ["OrdinalExpression"]


from regex.regex import Match

from maha.parsers.expressions import WAW_CONNECTOR
from maha.parsers.rules.ordinal import rule

from ..numeral.template import NumeralExpression


class OrdinalExpression(NumeralExpression):
    def _get_matched_numeral(self, ordinal: str) -> int:
        for exp in rule.ORDERED_ORDINALS:
            if exp.match(ordinal):
                return exp.value  # type: ignore
        return 0

    def _get_value(self, text: str) -> float:

        waw = WAW_CONNECTOR.search(text)
        if waw:
            ones, tens = text.split(waw.group(0))
            output = self._get_matched_numeral(ones) + self._get_matched_numeral(tens)
            return output

        output = self._get_matched_numeral(text)
        return output
