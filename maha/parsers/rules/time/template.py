__all__ = ["TimeExpression", "TimeShift", "TimeResult"]

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from regex.regex import Match

from maha.parsers.rules.numeral.template import NumeralExpression
from maha.parsers.rules.time import rule
from maha.parsers.templates.rule import Rule
from maha.rexy import ExpressionResult


@dataclass
class TimeShift:
    years: Optional[float] = None
    months: Optional[float] = None
    days: Optional[float] = None
    hours: Optional[float] = None
    minutes: Optional[float] = None
    seconds: Optional[float] = None

    @classmethod
    def now(cls) -> "TimeShift":
        return cls(years=0, months=0, days=0, hours=0, minutes=0, seconds=0)


@dataclass
class TimeResult:
    years: Optional[float] = None
    months: Optional[float] = None
    days: Optional[float] = None
    hours: Optional[float] = None
    minutes: Optional[float] = None
    seconds: Optional[float] = None

    def to_datetime(self) -> datetime:
        return datetime(
            year=int(self.years or 0),
            month=int(self.months or 0),
            day=int(self.days or 0),
            hour=int(self.hours or 0),
            minute=int(self.minutes or 0),
            second=int(self.seconds or 0),
        )


class TimeExpression(NumeralExpression):
    def parse(self, match: Match, text: str):
        start, end = match.span()

        groups = match.capturesdict()
        values = groups.get("value")
        units = groups.get("unit")
        multipliers = groups.get("multiplier")
        numerals = groups.get("numeral_value")
        bounds = groups.get("bound")

        return ExpressionResult(
            start=start,
            end=end,
            value=match.group(),
            expression=self,
        )

    def apply_rules(self, text, *rule_names: str) -> bool:
        return bool(Rule.get_rules_with_names(*rule_names).apply(text))

    def get_unit(self, text: str):
        return None

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
