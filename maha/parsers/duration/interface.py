__all__ = ["DurationValue", "DurationResult", "DurationExpression"]


from dataclasses import dataclass
from typing import List

from regex.regex import Match

import maha.parsers.duration.utils as utils
from maha.parsers.interfaces.unit_expression import UnitExpression, ValueUnit
from maha.rexy import ExpressionResult

from ..interfaces import DurationUnit
from .expressions import (
    DAYS,
    DUAL_DURATIONS,
    HOURS,
    MINUTES,
    MONTHS,
    SECONDS,
    SINGULAR_DURATIONS,
    WEEKS,
    YEARS,
)


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
        """Returns the value with unit normalized."""
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


class DurationExpression(UnitExpression):
    def parse(self, match: Match, text: str) -> DurationResult:
        start, end = match.span()
        output_values = self.extract_value_unit(match)
        value = DurationValue(output_values)
        return DurationResult(start, end, value, self)

    def get_unit(self, text: str) -> DurationUnit:
        if SECONDS.match(text):
            return DurationUnit.SECONDS
        if MINUTES.match(text):
            return DurationUnit.MINUTES
        if HOURS.match(text):
            return DurationUnit.HOURS
        if DAYS.match(text):
            return DurationUnit.DAYS
        if WEEKS.match(text):
            return DurationUnit.WEEKS
        if MONTHS.match(text):
            return DurationUnit.MONTHS
        if YEARS.match(text):
            return DurationUnit.YEARS

    def get_value(self, text: str) -> float:
        if DUAL_DURATIONS.match(text):
            return 2
        if SINGULAR_DURATIONS.match(text):
            return 1
        return super().get_value(text)
