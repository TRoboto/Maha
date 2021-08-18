__all__ = ["NumeralExpression"]

from typing import Optional

from regex.regex import Match

import maha.parsers.rules.numeral.rule as rule
from maha.parsers.expressions import WAW_CONNECTOR
from maha.parsers.utils import convert_to_number_if_possible
from maha.rexy import Expression, ExpressionResult


class NumeralExpression(Expression):
    def parse(self, match: Match, text: Optional[str]) -> "ExpressionResult":

        start, end = match.span()
        groups = match.capturesdict()

        values = groups.get("numeral_value")
        multiplier = groups.get("multiplier")

        output = 0
        for value, multiplier in zip(values, multiplier):
            output += self.get_numeral_value(value, multiplier)

        return ExpressionResult(start, end, output, self)

    def get_numeral_value(self, value: str, multiplier: str) -> float:
        """
        Returns the value of the numeral.

        Parameters
        ----------
        value : str
            The value of the numeral.
        multiplier : str
            The multiplier of the numeral.

        Returns
        -------
        float
            The value of the numeral.
        """
        # if not multiplier, then it's ones or tens
        if not multiplier:
            return self._get_value(value)

        output = self._get_matched_numeral(multiplier)
        if value:
            output *= self._get_value(value)
        return output

    def _get_matched_numeral(self, numeral) -> int:  # type: ignore
        for exp in rule.ORDERED_NUMERALS:
            if exp.match(numeral):
                return exp.value  # type: ignore

    def _handle_fasila(self, text) -> float:
        """
        Handle fasila in the numeral expression

        Parameters
        ----------
        text : str
            Numeral text with fasila.

        Returns
        -------
        float
            Decimal number.
        """
        fasila = rule.EXPRESSION_OF_FASILA.search(text)
        before, after = text.split(fasila.group(0))  # type: ignore
        before = self._get_value(before)
        after = self._get_value(after)
        output = float(f"{before}.{after}")
        return output

    def _get_value(self, text: str) -> float:
        """
        Returns the value in the text.

        Parameters
        ----------
        text : str
            The numeral text only.

        Returns
        -------
        float
            The value of the numeral.
        """
        output = convert_to_number_if_possible(text)
        if not isinstance(output, str):
            return output

        if rule.EXPRESSION_OF_FASILA.search(text):
            return self._handle_fasila(text)

        waw = WAW_CONNECTOR.search(text)
        if waw:
            ones, tens = text.split(waw.group(0))
            output = self._get_matched_numeral(ones) + self._get_matched_numeral(tens)
            return output

        output = self._get_matched_numeral(text)
        return output
