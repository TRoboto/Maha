__all__ = ["ValueUnit", "DurationValue", "DurationResult", "DurationExpression"]


from dataclasses import dataclass
from typing import List

from regex.regex import Match

import maha.parsers.duration.utils as utils
from maha.constants import EMPTY

from ..helper import convert_to_number_if_possible
from ..interfaces import DurationUnit, Expression, ExpressionResult, Unit


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


class DurationExpression(Expression):
    def parse(self, match: Match, text: str) -> DurationResult:
        start, end = match.span()
        groups = match.capturesdict()

        values = groups.get("value")
        units = groups.get("unit")

        output_values = []
        for value, unit in zip(values, units):
            extracted_unit = utils.get_unit(unit)

            if value is EMPTY:
                value = utils.get_value(unit)
            else:
                # if value is number, then assign it to the value
                number = convert_to_number_if_possible(value)
                if not isinstance(number, str):
                    value = number
                else:
                    value = utils.get_value(value)

            output_values.append(ValueUnit(value, extracted_unit))

        value = DurationValue(output_values)
        return DurationResult(start, end, value, self)
