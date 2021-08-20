__all__ = ["UnitExpression", "ValueUnit"]

from dataclasses import dataclass
from typing import List

from regex.regex import Match

from maha.parsers.expressions import HALF, QUARTER, THIRD, THREE_QUARTERS
from maha.parsers.rules.numeral.template import NumeralExpression
from maha.rexy import ExpressionResult

from .enums import Unit


@dataclass
class ValueUnit:
    """Represents a value with unit."""

    value: float
    unit: Unit


class UnitExpression(NumeralExpression):
    """Expression that matches a numeric value followed by a unit."""

    def parse(self, match: Match, text: str) -> "ExpressionResult":
        """Extract the value from the input ``text`` and return it.

        .. warning::
            This method is called by :meth:`__call__` to extract the value from
            the input ``text``. You should not call this method directly.


        Parameters
        ----------
        match : :class:`regex.Match`
            Matched object.
        text : str
            Text in which the match was found.

        Returns
        -------
        :class:`ExpressionResult`
            Extracted value.
        """
        raise NotImplementedError

    def extract_value_unit(self, match: Match) -> List[ValueUnit]:
        """Extract the value and unit from the input ``match``."""
        groups = match.capturesdict()

        values = groups.get("value")
        units = groups.get("unit")
        multipliers = groups.get("multiplier")
        numerals = groups.get("numeral_value")

        units_spans = match.spans("unit")
        numerals_spans = match.spans("numeral_value")

        output_values = []
        value_pointer = 0
        numeral_pointer = 0
        for i, unit_span in enumerate(units_spans):
            unit = units[i]
            extracted_unit = self.get_unit(unit)

            extracted_numeral = 0
            for numeral, multiplier in zip(
                numerals[numeral_pointer:], multipliers[numeral_pointer:]
            ):
                if numerals_spans[numeral_pointer][0] > unit_span[1]:
                    break

                numeral_pointer += 1
                extracted_numeral += self.get_numeral_value(numeral, multiplier)

            if not extracted_numeral:
                extracted_numeral = self.get_value(values[value_pointer] or unit)
                value_pointer += 1

            output_values.append(ValueUnit(extracted_numeral, extracted_unit))

        return output_values

    def get_unit(self, text: str):
        """Get the unit from the input ``text``."""
        raise NotImplementedError

    def get_value(self, text: str) -> float:  # type: ignore
        """Get the value from the input ``text``."""
        if HALF.match(text):
            return 1 / 2
        if THIRD.match(text):
            return 1 / 3
        if QUARTER.match(text):
            return 1 / 4
        if THREE_QUARTERS.match(text):
            return 3 / 4
