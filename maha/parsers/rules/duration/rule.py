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

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from maha.parsers.rules.numeral.rule import RULE_NUMERAL, parse_numeral
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


def merge_same_units(values: List[ValueUnit]) -> List[ValueUnit]:
    """Merge values with same units from the input ``values``."""
    newvalues: Dict[Unit, ValueUnit] = {}
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


@dataclass
class DurationParsedValue:
    name: str
    text: str
    index: int
    values: Dict[str, List]

    def __init__(self, name, text, index) -> None:
        self.name = name
        self.text = text
        self.index = index
        self.values = defaultdict(list)

    def capturesdict(self):
        return self.values


class IndexPriorityList:
    def __init__(self):
        self.items: List[DurationParsedValue] = []

    def add_item(self, name, text, index):
        self.items.append(DurationParsedValue(name, text, index))
        self.items.sort(key=lambda i: i.index)

    def add_value(self, name, value, index) -> None:
        for item in self.items:
            if index < item.index:
                item.values[name].append(value)
                break


def parse_duration(match):
    """Parse duration."""
    groups = match.capturesdict()
    groups_keys = list(groups)
    collection = IndexPriorityList()
    for key in ["seconds", "minutes", "hours", "days", "weeks", "months", "years"]:
        if key not in groups:
            continue
        for i, t in enumerate(match.starts(groups_keys.index(key) + 1)):
            collection.add_item(key, groups[key][i], t)

    for key in [
        "trillions",
        "billions",
        "millions",
        "thousands",
        "hundreds",
        "decimals",
        "tens",
        "ones",
        "integers",
    ]:
        for i, t in enumerate(match.starts(groups_keys.index(key) + 1)):
            collection.add_value(key, groups[key][i], t)

    values = []
    for item in collection.items:
        numeral = parse_numeral(item)
        valueunit = get_matched_value(item.text)
        if numeral:
            valueunit.value = numeral
        values.append(valueunit)
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
