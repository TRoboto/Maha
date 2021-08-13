__all__ = ["ValueExpression", "ValueUnit"]

from dataclasses import dataclass
from typing import List, Optional

from regex.regex import Match

from maha.constants import EMPTY
from maha.parsers.expressions import HALF, QUARTER, THIRD, THREE_QUARTERS
from maha.parsers.numeral.interface import NumeralExpression
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

        multiplier_pointer = 0
        output_values = []
        for i, value in enumerate(values):
            extracted_unit = self.get_unit(units[i])
            # if the value is empty, it's either singular or plural.
            if value is EMPTY:
                extracted_value = self.get_value(units[i])
            else:
                extracted_value = self.get_value(value)
                # if the extracted_value is empty, it's a numeral value.
                if extracted_value is None:
                    extracted_value = self.get_numeral_value(
                        value, multipliers[multiplier_pointer]
                    )
                    multiplier_pointer += 1
            output_values.append(ValueUnit(extracted_value, extracted_unit))
        return output_values

    def get_unit(self, text: str):
        """Get the unit from the input ``text``."""
        raise NotImplementedError

    def get_value(self, text: str) -> Optional[float]:
        """Get the value from the input ``text``."""
        if HALF.match(text):
            return 1 / 2
        if THIRD.match(text):
            return 1 / 3
        if QUARTER.match(text):
            return 1 / 4
        if THREE_QUARTERS.match(text):
            return 3 / 4
