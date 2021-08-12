__all__ = ["ValueUnit", "DurationValue", "DurationResult", "DurationExpression"]


from dataclasses import dataclass
from typing import List

from regex.regex import Match

import maha.parsers.duration.utils as utils
from maha.constants import EMPTY
from maha.parsers.numeral.interface import NumeralExpression

from ..interfaces import DurationUnit, ExpressionResult, Unit
from ..utils import convert_to_number_if_possible


@dataclass
class ValueUnit:
    """
    Represents a value with unit.
    """

    value: float
    unit: Unit


@dataclass(init=False)
class DurationValue:
    __slots__ = ("values", "normalized_unit")

    values: List[ValueUnit]
    normalized_unit: DurationUnit

    def __init__(self, values: List[ValueUnit], normalized_unit=DurationUnit.SECONDS):
        self.values = values
        self.normalized_unit = normalized_unit

    @property
    def normalized_value(self) -> ValueUnit:
        """
        Returns the value with unit normalized.
        """
        return utils.convert_between_durations(
            *self.values, to_unit=self.normalized_unit
        )

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, item) -> ValueUnit:
        return self.values[item]


@dataclass
class DurationResult(ExpressionResult):
    value: DurationValue


class DurationExpression(NumeralExpression):
    def parse(self, match: Match, text: str) -> DurationResult:
        start, end = match.span()
        groups = match.capturesdict()

        values = groups.get("value")
        units = groups.get("unit")
        multipliers = groups.get("multiplier")

        multiplier_pointer = 0
        output_values = []
        for i, value in enumerate(values):
            extracted_unit = utils.get_unit(units[i])
            # if the value is empty, it's either singular or plural.
            if value is EMPTY:
                extracted_value = utils.get_value(units[i])
            else:
                extracted_value = utils.get_value(value)
                # if the extracted_value is empty, it's a numeral value.
                if extracted_value is None:
                    extracted_value = self.get_numeral_value(
                        value, multipliers[multiplier_pointer]
                    )
                    multiplier_pointer += 1
            output_values.append(ValueUnit(extracted_value, extracted_unit))

        value = DurationValue(output_values)
        return DurationResult(start, end, value, self)
