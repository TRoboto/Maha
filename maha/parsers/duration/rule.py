"""
Expressions to extract duration.
"""

__all__ = [
    "EXPRESSION_DURATION_SECONDS",
    "EXPRESSION_DURATION_MINUTES",
    "EXPRESSION_DURATION_HOURS",
    "EXPRESSION_DURATION_DAYS",
    "EXPRESSION_DURATION_WEEKS",
    "EXPRESSION_DURATION_MONTHS",
    "EXPRESSION_DURATION_YEARS",
    "EXPRESSION_DURATION",
]

from maha.constants import PATTERN_SPACE
from maha.parsers.helper import (
    get_fractions_of_unit_pattern,
    get_unit_group,
    get_value_group,
)
from maha.parsers.numeral import EXPRESSION_NUMERAL
from maha.rexy import ExpressionGroup

from ..constants import EXPRESSION_START, NUMERAL_WORD_SEPARATOR
from ..interfaces import DurationUnit
from .constants import *
from .interface import DurationExpression


def _get_pattern(unit: DurationUnit):
    single = str(globals()[f"EXPRESSION_OF_{unit.name[:-1]}"])
    dual = str(globals()[f"EXPRESSION_OF_TWO_{unit.name}"])
    plural = str(globals()[f"EXPRESSION_OF_{unit.name}"])

    pattern = (
        "(?:"
        + "|".join(
            [
                "{numeral}{space}{unit_single_plural}",
                get_fractions_of_unit_pattern(single),
                get_fractions_of_unit_pattern(dual),
                "{val}{unit_dual}",
                "{val}{unit_single}",
            ]
        ).format(
            numeral=EXPRESSION_NUMERAL.join(),
            space=PATTERN_SPACE,
            unit_single_plural=get_unit_group("|".join([single, plural])),
            unit_single=get_unit_group(single),
            unit_dual=get_unit_group(dual),
            val=get_value_group(""),
        )
        + ")"
    )
    return pattern


def _get_combined_expression(*unit: DurationUnit) -> DurationExpression:
    patterns = []
    for i, u in enumerate(unit):
        pattern = _get_pattern(u)
        if i == 0:
            pattern = EXPRESSION_START + pattern
        else:
            pattern = f"{non_capturing_group(NUMERAL_WORD_SEPARATOR + pattern)}?"
        patterns.append(pattern + r"\b")
    return DurationExpression(f"".join(patterns), pickle=True)


EXPRESSION_DURATION_SECONDS = _get_combined_expression(DurationUnit.SECONDS)

EXPRESSION_DURATION_MINUTES = _get_combined_expression(DurationUnit.MINUTES)

EXPRESSION_DURATION_HOURS = _get_combined_expression(DurationUnit.HOURS)

EXPRESSION_DURATION_DAYS = _get_combined_expression(DurationUnit.DAYS)

EXPRESSION_DURATION_WEEKS = _get_combined_expression(DurationUnit.WEEKS)

EXPRESSION_DURATION_MONTHS = _get_combined_expression(DurationUnit.MONTHS)

EXPRESSION_DURATION_YEARS = _get_combined_expression(DurationUnit.YEARS)

EXPRESSION_DURATION = ExpressionGroup(
    _get_combined_expression(
        DurationUnit.YEARS,
        DurationUnit.MONTHS,
        DurationUnit.WEEKS,
        DurationUnit.DAYS,
        DurationUnit.HOURS,
        DurationUnit.MINUTES,
        DurationUnit.SECONDS,
    ),
    _get_combined_expression(
        DurationUnit.MONTHS,
        DurationUnit.WEEKS,
        DurationUnit.DAYS,
        DurationUnit.HOURS,
        DurationUnit.MINUTES,
        DurationUnit.SECONDS,
    ),
    _get_combined_expression(
        DurationUnit.WEEKS,
        DurationUnit.DAYS,
        DurationUnit.HOURS,
        DurationUnit.MINUTES,
        DurationUnit.SECONDS,
    ),
    _get_combined_expression(
        DurationUnit.DAYS,
        DurationUnit.HOURS,
        DurationUnit.MINUTES,
        DurationUnit.SECONDS,
    ),
    _get_combined_expression(
        DurationUnit.HOURS,
        DurationUnit.MINUTES,
        DurationUnit.SECONDS,
    ),
    _get_combined_expression(
        DurationUnit.MINUTES,
        DurationUnit.SECONDS,
    ),
    _get_combined_expression(
        DurationUnit.SECONDS,
    ),
    smart=True,
)
