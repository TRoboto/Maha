"""Rules to extract duration."""
from __future__ import annotations

__all__ = [
    "RULE_DURATION_SECONDS",
    "RULE_DURATION_MINUTES",
    "RULE_DURATION_HOURS",
    "RULE_DURATION_DAYS",
    "RULE_DURATION_WEEKS",
    "RULE_DURATION_MONTHS",
    "RULE_DURATION_YEARS",
    "RULE_DURATION",
    "parse_duration",
]


from maha.parsers.rules.numeral.rule import (
    EXPRESSION_NUMERAL_MAP,
    RULE_NUMERAL,
    _parse_numeral,
)
from maha.parsers.templates import FunctionValue, Unit
from maha.rexy import ExpressionGroup, named_group, non_capturing_group

from ..common import (
    FRACTIONS,
    combine_patterns,
    get_fractions_of_unit_pattern,
    spaced_patterns,
)
from .template import *
from .values import *


def get_pattern(singular_frac_group, singular, dual, all_units):
    """Get regex pattern for duration."""

    return non_capturing_group(
        spaced_patterns(RULE_NUMERAL, all_units),
        named_group("fractions", get_fractions_of_unit_pattern(singular_frac_group)),
        dual,
        singular,
    )


def merge_same_units(values: list[ValueUnit]) -> list[ValueUnit]:
    """Merge values with same units from the input ``values``."""
    newvalues: dict[Unit, ValueUnit] = {}
    for value in values:
        unit = value.unit
        if unit in newvalues:
            newvalues[unit].value += value.value
        else:
            newvalues[unit] = value
    return list(newvalues.values())


def get_unit_fraction_value(matched_text):
    val1, val2 = matched_text.split(" ", 1)
    fraction = FRACTIONS.get_matched_expression(val1)
    if not fraction:
        fraction = FRACTIONS.get_matched_expression(val2)
        value = get_matched_value(val1)
    else:
        value = get_matched_value(val2)
    value.value = fraction.value  # type: ignore
    return value


def _parse(matched_text, singular=None, plural=None):
    if singular and plural:
        multiplier = plural.search(matched_text) or singular.search(matched_text)
        matched_text = matched_text.replace(multiplier.group(0), "").strip()

    fraction = FRACTIONS.get_matched_expression(matched_text)
    value = ValueUnit(0, singular.value.unit)
    if fraction is not None:
        value.value = fraction.value  # type: ignore
    else:
        value.value = list(RULE_NUMERAL(matched_text))[0].value

    return value


UnitsGroup = ExpressionGroup(
    SEVERAL_SECONDS,
    SEVERAL_MINUTES,
    SEVERAL_HOURS,
    SEVERAL_DAYS,
    SEVERAL_WEEKS,
    SEVERAL_MONTHS,
    SEVERAL_YEARS,
    TWO_SECONDS,
    TWO_MINUTES,
    TWO_HOURS,
    TWO_DAYS,
    TWO_WEEKS,
    TWO_MONTHS,
    TWO_YEARS,
    ONE_SECOND,
    ONE_MINUTE,
    ONE_HOUR,
    ONE_DAY,
    ONE_WEEK,
    ONE_MONTH,
    ONE_YEAR,
)


def get_matched_value(matched_text) -> ValueUnit:
    exp_val = UnitsGroup.get_matched_expression(matched_text).value  # type: ignore
    return ValueUnit(value=exp_val.value, unit=exp_val.unit)


def get_groups():
    return [
        "seconds",
        "minutes",
        "hours",
        "days",
        "weeks",
        "months",
        "years",
    ]


def parse_duration(match):
    """Parse duration."""
    groups = match.capturesdict()
    groups_keys = list(groups)

    duration_groups = get_groups()
    sorted_values = {}
    for group in list(EXPRESSION_NUMERAL_MAP) + duration_groups:
        if group not in groups_keys:
            continue
        for i, value in enumerate(groups.get(group)):
            index = match.starts(groups_keys.index(group) + 1)[i]
            sorted_values[index] = {"group": group, "value": value}

    sorted_values = dict(sorted(sorted_values.items()))

    # holds numeral values before a unit
    temp_dict = {}
    values = []
    for index, item in sorted_values.items():
        group = item["group"]
        if group not in duration_groups:
            temp_dict[index] = item
            continue
        numeral = _parse_numeral(temp_dict)
        valueunit = get_matched_value(item["value"])
        if numeral:
            valueunit.value = numeral
        values.append(valueunit)
        temp_dict = {}

    for item in groups.get("fractions", []):
        values.append(get_unit_fraction_value(item))

    values = merge_same_units(values)
    values.sort(key=lambda v: v.unit.value, reverse=True)
    return DurationValue(values)


_seconds = named_group(
    "seconds", non_capturing_group(ONE_SECOND, TWO_SECONDS, SEVERAL_SECONDS)
)
_minutes = named_group(
    "minutes", non_capturing_group(ONE_MINUTE, TWO_MINUTES, SEVERAL_MINUTES)
)
_hours = named_group("hours", non_capturing_group(ONE_HOUR, TWO_HOURS, SEVERAL_HOURS))
_days = named_group("days", non_capturing_group(ONE_DAY, TWO_DAYS, SEVERAL_DAYS))
_weeks = named_group("weeks", non_capturing_group(ONE_WEEK, TWO_WEEKS, SEVERAL_WEEKS))
_months = named_group(
    "months", non_capturing_group(ONE_MONTH, TWO_MONTHS, SEVERAL_MONTHS)
)
_years = named_group("years", non_capturing_group(ONE_YEAR, TWO_YEARS, SEVERAL_YEARS))

all_units = non_capturing_group(
    _seconds, _minutes, _hours, _days, _weeks, _months, _years
)
dual_units = non_capturing_group(
    named_group("seconds", TWO_SECONDS),
    named_group("minutes", TWO_MINUTES),
    named_group("hours", TWO_HOURS),
    named_group("days", TWO_DAYS),
    named_group("weeks", TWO_WEEKS),
    named_group("months", TWO_MONTHS),
    named_group("years", TWO_YEARS),
)
singular_units = non_capturing_group(
    named_group("seconds", ONE_SECOND),
    named_group("minutes", ONE_MINUTE),
    named_group("hours", ONE_HOUR),
    named_group("days", ONE_DAY),
    named_group("weeks", ONE_WEEK),
    named_group("months", ONE_MONTH),
    named_group("years", ONE_YEAR),
)

RULE_DURATION_SECONDS = FunctionValue(
    parse_duration,
    combine_patterns(
        get_pattern(
            ONE_SECOND,
            named_group("seconds", ONE_SECOND),
            named_group("seconds", TWO_SECONDS),
            _seconds,
        )
    ),
)
RULE_DURATION_MINUTES = FunctionValue(
    parse_duration,
    combine_patterns(
        get_pattern(
            ONE_MINUTE,
            named_group("minutes", ONE_MINUTE),
            named_group("minutes", TWO_MINUTES),
            _minutes,
        )
    ),
)
RULE_DURATION_HOURS = FunctionValue(
    parse_duration,
    combine_patterns(
        get_pattern(
            ONE_HOUR,
            named_group("hours", ONE_HOUR),
            named_group("hours", TWO_HOURS),
            _hours,
        )
    ),
)
RULE_DURATION_DAYS = FunctionValue(
    parse_duration,
    combine_patterns(
        get_pattern(
            ONE_DAY,
            named_group("days", ONE_DAY),
            named_group("days", TWO_DAYS),
            _days,
        )
    ),
)
RULE_DURATION_WEEKS = FunctionValue(
    parse_duration,
    combine_patterns(
        get_pattern(
            ONE_WEEK,
            named_group("weeks", ONE_WEEK),
            named_group("weeks", TWO_WEEKS),
            _weeks,
        )
    ),
)
RULE_DURATION_MONTHS = FunctionValue(
    parse_duration,
    combine_patterns(
        get_pattern(
            ONE_MONTH,
            named_group("months", ONE_MONTH),
            named_group("months", TWO_MONTHS),
            _months,
        )
    ),
)
RULE_DURATION_YEARS = FunctionValue(
    parse_duration,
    combine_patterns(
        get_pattern(
            ONE_YEAR,
            named_group("years", ONE_YEAR),
            named_group("years", TWO_YEARS),
            _years,
        )
    ),
)


RULE_DURATION = FunctionValue(
    parse_duration,
    combine_patterns(
        get_pattern(
            non_capturing_group(
                ONE_SECOND, ONE_MINUTE, ONE_HOUR, ONE_DAY, ONE_WEEK, ONE_MONTH, ONE_YEAR
            ),
            singular_units,
            dual_units,
            all_units,
        ),
        combine_all=True,
    ),
)
