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

from maha.expressions import EXPRESSION_SPACE
from maha.parsers.expressions import (
    EXPRESSION_END,
    EXPRESSION_START,
    WORD_SEPARATOR,
)
from maha.parsers.helper import (
    get_fractions_of_unit_pattern,
    get_unit_group,
    get_value_group,
)
from maha.parsers.interfaces import DurationUnit
from maha.parsers.rules.numeral import RULE_NUMERAL
from maha.rexy import ExpressionGroup

from .expressions import *
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
            numeral=RULE_NUMERAL.join(),
            space=EXPRESSION_SPACE,
            unit_single_plural=get_unit_group("|".join([single, plural])),
            unit_single=get_unit_group(single),
            unit_dual=get_unit_group(dual),
            val=get_value_group(""),
        )
        + ")"
    )
    return pattern


def _get_combined_expression(*units: DurationUnit) -> DurationExpression:
    all_expressions = non_capturing_group(*[_get_pattern(unit) for unit in units])
    patterns = [EXPRESSION_START + all_expressions + EXPRESSION_END]

    for u in units[1:]:
        pattern = (
            non_capturing_group(WORD_SEPARATOR + _get_pattern(u) + EXPRESSION_END) + "?"
        )
        patterns.append(pattern)
    return DurationExpression(f"".join(patterns), pickle=True)


RULE_DURATION_SECONDS = _get_combined_expression(DurationUnit.SECONDS)

RULE_DURATION_MINUTES = _get_combined_expression(DurationUnit.MINUTES)

RULE_DURATION_HOURS = _get_combined_expression(DurationUnit.HOURS)

RULE_DURATION_DAYS = _get_combined_expression(DurationUnit.DAYS)

RULE_DURATION_WEEKS = _get_combined_expression(DurationUnit.WEEKS)

RULE_DURATION_MONTHS = _get_combined_expression(DurationUnit.MONTHS)

RULE_DURATION_YEARS = _get_combined_expression(DurationUnit.YEARS)

RULE_DURATION = ExpressionGroup(
    _get_combined_expression(
        DurationUnit.YEARS,
        DurationUnit.MONTHS,
        DurationUnit.WEEKS,
        DurationUnit.DAYS,
        DurationUnit.HOURS,
        DurationUnit.MINUTES,
        DurationUnit.SECONDS,
    ),
    smart=True,
)
