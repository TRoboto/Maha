"""Rules to extract duration."""

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

from typing import List

from maha.parsers.rules.numeral.rule import RULE_NUMERAL
from maha.parsers.templates import FunctionValue
from maha.rexy import named_group, non_capturing_group

from ..common import (
    FRACTIONS,
    combine_patterns,
    get_fractions_of_unit_pattern,
    spaced_patterns,
)
from .template import *
from .values import *


def get_pattern(name: str):
    """Get regex pattern for duration."""
    singular = globals()["ONE_" + name[:-1].upper()]
    dual = globals()["TWO_" + name.upper()]
    plural = globals()["SEVERAL_" + name.upper()]

    return non_capturing_group(
        spaced_patterns(RULE_NUMERAL, non_capturing_group(singular, plural)),
        get_fractions_of_unit_pattern(singular),
        dual,
        singular,
    )


def merge_values(values: List[ValueUnit]) -> ValueUnit:
    """Merge the values from the input ``values``."""
    unit = values[0].unit
    assert all(value.unit == unit for value in values)
    return ValueUnit(sum(value.value for value in values), unit)


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


def get_combined_value(groups, unit) -> ValueUnit:

    singular = globals()["ONE_" + unit[:-1].upper()]
    dual = globals()["TWO_" + unit.upper()]
    plural = globals()["SEVERAL_" + unit.upper()]
    values = []
    for group in groups:
        unit = get_matched_value(group, singular, dual)
        if unit:
            values.append(unit)
        else:
            values.append(_parse(group, singular, plural))
    return merge_values(values)


def get_matched_value(matched_text, singular, dual):
    if not (dual or singular):
        return
    if dual.fullmatch(matched_text):
        return dual.value
    if singular.fullmatch(matched_text):
        return singular.value


def parse_duration(match):
    """Parse duration."""
    groups = match.capturesdict()
    _seconds = groups.get("seconds")
    _minutes = groups.get("minutes")
    _hours = groups.get("hours")
    _days = groups.get("days")
    _weeks = groups.get("weeks")
    _months = groups.get("months")
    _years = groups.get("years")

    value = []
    if _years:
        value.append(get_combined_value(_years, "years"))
    if _months:
        value.append(get_combined_value(_months, "months"))
    if _weeks:
        value.append(get_combined_value(_weeks, "weeks"))
    if _days:
        value.append(get_combined_value(_days, "days"))
    if _hours:
        value.append(get_combined_value(_hours, "hours"))
    if _minutes:
        value.append(get_combined_value(_minutes, "minutes"))
    if _seconds:
        value.append(get_combined_value(_seconds, "seconds"))

    return DurationValue(value)


seconds_group = named_group("seconds", get_pattern("seconds"))
minutes_group = named_group("minutes", get_pattern("minutes"))
hours_group = named_group("hours", get_pattern("hours"))
days_group = named_group("days", get_pattern("days"))
weeks_group = named_group("weeks", get_pattern("weeks"))
months_group = named_group("months", get_pattern("months"))
years_group = named_group("years", get_pattern("years"))

RULE_DURATION_SECONDS = FunctionValue(parse_duration, combine_patterns(seconds_group))
RULE_DURATION_MINUTES = FunctionValue(parse_duration, combine_patterns(minutes_group))
RULE_DURATION_HOURS = FunctionValue(parse_duration, combine_patterns(hours_group))
RULE_DURATION_DAYS = FunctionValue(parse_duration, combine_patterns(days_group))
RULE_DURATION_WEEKS = FunctionValue(parse_duration, combine_patterns(weeks_group))
RULE_DURATION_MONTHS = FunctionValue(parse_duration, combine_patterns(months_group))
RULE_DURATION_YEARS = FunctionValue(parse_duration, combine_patterns(years_group))


RULE_DURATION = FunctionValue(
    parse_duration,
    combine_patterns(
        years_group,
        months_group,
        weeks_group,
        days_group,
        hours_group,
        minutes_group,
        seconds_group,
        combine_all=True,
    ),
)
