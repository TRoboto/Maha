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

from ..interfaces import ExpressionGroup
from ..utils.general import (
    DECIMAL_EXPRESSION,
    HALF,
    INTEGER_EXPRESSION,
    QUARTER,
    SPACE_EXPRESSION,
    THIRD,
    THREE_QUARTERS,
)
from .constants import *
from .interface import DurationExpression
from .utils import DurationUnit


def _get_pattern(unit: DurationUnit):
    single = globals()[f"NAME_OF_{unit.name[:-1]}"]
    dual = globals()[f"NAME_OF_TWO_{unit.name}"]
    plural = globals()[f"NAME_OF_{unit.name}"]

    _get_value_group = lambda v: f"(?P<value>{v})"
    _get_unit_group = lambda v: f"(?P<unit>{v})"

    pattern = (
        "(?:"
        + "|".join(
            [
                "{decimal}{space}{unit_single_plural}",
                "{integer}{space}{unit_single_plural}",
                "{unit_dual}{space}{three_quarter}",
                "{half}{space}{unit_dual}",
                "{third}{space}{unit_dual}",
                "{quarter}{space}{unit_dual}",
                "{unit_single}{space}{three_quarter}",
                "{half}{space}{unit_single}",
                "{third}{space}{unit_single}",
                "{quarter}{space}{unit_single}",
                "{val}{unit_dual}",
                "{val}{unit_single}",
            ]
        ).format(
            decimal=_get_value_group(DECIMAL_EXPRESSION),
            integer=_get_value_group(INTEGER_EXPRESSION),
            space=SPACE_EXPRESSION,
            half=_get_value_group(HALF),
            third=_get_value_group(THIRD),
            quarter=_get_value_group(QUARTER),
            three_quarter=_get_value_group(THREE_QUARTERS),
            unit_single_plural=_get_unit_group("|".join([single, plural])),
            unit_single=_get_unit_group(single),
            unit_dual=_get_unit_group(dual),
            unit=unit.name,
            val=_get_value_group(""),
        )
        + ")"
    )
    return pattern


def _get_combined_expression(*unit: DurationUnit) -> DurationExpression:
    patterns = []
    for i, u in enumerate(unit):
        pattern = f"(?:{WORD_SEPARATOR}{_get_pattern(u)})"
        if i == 0:
            patterns.append(pattern + "\\b")
        else:
            patterns.append(f"{pattern}?\\b")
    return DurationExpression(f"".join(patterns))


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