__all__ = ["DurationValue", "DurationResult", "DurationExpression"]


from dataclasses import dataclass
from typing import List, Optional

from regex.regex import Match

import maha.parsers.rules.duration.utils as utils
from maha.parsers.templates import DurationUnit, Rule
from maha.parsers.templates.unit_expression import UnitExpression, ValueUnit
from maha.rexy import ExpressionResult


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

    def apply_rules(self, text, *rule_names: str) -> bool:
        return bool(Rule.get_rules_with_names(*rule_names).apply(text))

    def get_unit(self, text: str) -> Optional[DurationUnit]:
        if self.apply_rules(text, "one_second", "two_seconds", "several_seconds"):
            return DurationUnit.SECONDS
        if self.apply_rules(text, "one_minute", "two_minutes", "several_minutes"):
            return DurationUnit.MINUTES
        if self.apply_rules(text, "one_hour", "two_hours", "several_hours"):
            return DurationUnit.HOURS
        if self.apply_rules(text, "one_day", "two_days", "several_days"):
            return DurationUnit.DAYS
        if self.apply_rules(text, "one_week", "two_weeks", "several_weeks"):
            return DurationUnit.WEEKS
        if self.apply_rules(text, "one_month", "two_months", "several_months"):
            return DurationUnit.MONTHS
        if self.apply_rules(text, "one_year", "two_years", "several_years"):
            return DurationUnit.YEARS

    def get_value(self, text: str) -> Optional[float]:
        if self.apply_rules(
            text,
            "two_seconds",
            "two_minutes",
            "two_hours",
            "two_days",
            "two_weeks",
            "two_months",
            "two_years",
        ):
            return 2
        if self.apply_rules(
            text,
            "one_second",
            "one_minute",
            "one_hour",
            "one_day",
            "one_week",
            "one_month",
            "one_year",
        ):
            return 1
        return super().get_value(text)
