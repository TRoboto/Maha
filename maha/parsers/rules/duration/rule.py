"""
Expressions to extract duration.
"""

__all__ = [
    "RULE_DURATION_SECONDS",
    "RULE_DURATION_MINUTES",
    "RULE_DURATION_HOURS",
    "RULE_DURATION_DAYS",
    "RULE_DURATION_WEEKS",
    "RULE_DURATION_MONTHS",
    "RULE_DURATION_YEARS",
    "RULE_DURATION",
]


from maha.parsers.rules.templates import UnitRule
from maha.parsers.templates import DimensionType, DurationUnit

from .expression import *
from .template import DurationExpression


class DurationRule(UnitRule):
    """Rule to extract a duration."""

    def __init__(self, *units: DurationUnit) -> None:
        """Returns a combined expression for the given units."""
        combined_patterns = self.combine_patterns(*units)
        expression = DurationExpression(combined_patterns, pickle=True)
        super().__init__(expression, DimensionType.DURATION)

    def get_single(self, unit: DurationUnit) -> "Expression":
        return globals()[(f"EXPRESSION_OF_{unit.name[:-1]}")]

    def get_dual(self, unit: DurationUnit) -> "Expression":
        return globals()[(f"EXPRESSION_OF_TWO_{unit.name}")]

    def get_plural(self, unit: DurationUnit) -> "Expression":
        return globals()[(f"EXPRESSION_OF_{unit.name}")]


RULE_DURATION_SECONDS = DurationRule(DurationUnit.SECONDS)

RULE_DURATION_MINUTES = DurationRule(DurationUnit.MINUTES)

RULE_DURATION_HOURS = DurationRule(DurationUnit.HOURS)

RULE_DURATION_DAYS = DurationRule(DurationUnit.DAYS)

RULE_DURATION_WEEKS = DurationRule(DurationUnit.WEEKS)

RULE_DURATION_MONTHS = DurationRule(DurationUnit.MONTHS)

RULE_DURATION_YEARS = DurationRule(DurationUnit.YEARS)

RULE_DURATION = DurationRule(
    DurationUnit.YEARS,
    DurationUnit.MONTHS,
    DurationUnit.WEEKS,
    DurationUnit.DAYS,
    DurationUnit.HOURS,
    DurationUnit.MINUTES,
    DurationUnit.SECONDS,
)
