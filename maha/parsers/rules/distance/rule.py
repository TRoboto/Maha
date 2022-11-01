"""Rules to extract distance."""
from __future__ import annotations

__all__ = [
    "RULE_DISTANCE_KILOMETERS",
    "RULE_DISTANCE_CENTIMETERS",
    "RULE_DISTANCE_MILLIMETERS",
    "RULE_DISTANCE_DECIMETERS",
    "RULE_DISTANCE_METERS",
    "RULE_DISTANCE_FEET",
    "RULE_DISTANCE_INCHES",
    "RULE_DISTANCE_YARDS",
    "RULE_DISTANCE_MILES",
    "RULE_DISTANCE",
]

from maha.parsers.rules.numeral.rule import RULE_NUMERAL, parse_numeral
from maha.parsers.templates import FunctionValue
from maha.rexy import ExpressionGroup, named_group, non_capturing_group

from ..common import (FRACTIONS, combine_patterns,
                      get_fractions_of_unit_pattern, spaced_patterns,
                      wrap_pattern)
from .template import DistanceValue
from .values import *


def get_pattern(singular_frac_group, singular, all_units, dual=None):
    """Get regex pattern for distance."""
    if dual:
        return non_capturing_group(
            spaced_patterns(RULE_NUMERAL, all_units),
            named_group(
                "fractions", get_fractions_of_unit_pattern(singular_frac_group)
            ),
            dual,
            singular,
        )

    return non_capturing_group(
        spaced_patterns(RULE_NUMERAL, all_units),
        named_group("fractions", get_fractions_of_unit_pattern(singular_frac_group)),
        singular,
    )


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


UnitsGroup = ExpressionGroup(
    SEVERAL_KILOMETERS,
    SEVERAL_CENTIMETERS,
    SEVERAL_MILLIMETERS,
    SEVERAL_DECIMETERS,
    SEVERAL_METERS,
    SEVERAL_FEET,
    SEVERAL_INCHES,
    SEVERAL_YARDS,
    SEVERAL_MILES,
    TWO_METERS,
    TWO_FEET,
    TWO_INCHES,
    TWO_MILES,
    ONE_KILOMETER,
    ONE_CENTIMETER,
    ONE_MILLIMETER,
    ONE_DECIMETER,
    ONE_METER,
    ONE_FOOT,
    ONE_INCH,
    ONE_YARD,
    ONE_MILE,
)


def get_matched_value(matched_text) -> ValueUnit:
    exp_val = UnitsGroup.get_matched_expression(matched_text).value  # type: ignore
    return ValueUnit(value=exp_val.value, unit=exp_val.unit)


def get_groups():
    return [
        "meters",
        "feet",
        "inches",
        "yards",
        "miles",
        "kilometers",
        "centimeters",
        "millimeters",
        "decimeters",
    ]


def parse_distance(match):
    """Parse distance."""
    groups = match.capturesdict()

    distance_groups = get_groups()
    if groups.get("fractions"):
        value = get_unit_fraction_value(groups.get("fractions")[0])
        return DistanceValue(value)

    matched_group = [
        groups.get(group)[0] for group in distance_groups if groups.get(group)
    ][0]
    valueunit = get_matched_value(matched_group)
    numeral = parse_numeral(match)
    if numeral:
        valueunit.value = numeral
    return DistanceValue(valueunit)


_meters = named_group(
    "meters", non_capturing_group(ONE_METER, TWO_METERS, SEVERAL_METERS)
)
_kilometers = named_group(
    "kilometers", non_capturing_group(ONE_KILOMETER, SEVERAL_KILOMETERS)
)
_centimeters = named_group(
    "centimeters", non_capturing_group(ONE_CENTIMETER, SEVERAL_CENTIMETERS)
)
_millimeters = named_group(
    "millimeters", non_capturing_group(ONE_MILLIMETER, SEVERAL_MILLIMETERS)
)
_decimeters = named_group(
    "decimeters", non_capturing_group(ONE_DECIMETER, SEVERAL_DECIMETERS)
)
_feet = named_group("feet", non_capturing_group(ONE_FOOT, TWO_FEET, SEVERAL_FEET))
_inches = named_group(
    "inches", non_capturing_group(ONE_INCH, TWO_INCHES, SEVERAL_INCHES)
)
_yards = named_group("yards", non_capturing_group(ONE_YARD, SEVERAL_YARDS))
_miles = named_group("miles", non_capturing_group(ONE_MILE, TWO_MILES, SEVERAL_MILES))

all_units = non_capturing_group(
    _meters,
    _kilometers,
    _centimeters,
    _millimeters,
    _decimeters,
    _feet,
    _inches,
    _yards,
    _miles,
)
dual_units = non_capturing_group(
    named_group("meters", TWO_METERS),
    named_group("feet", TWO_FEET),
    named_group("inches", TWO_INCHES),
    named_group("miles", TWO_MILES),
)
singular_units = non_capturing_group(
    named_group("meters", ONE_METER),
    named_group("kilometers", ONE_KILOMETER),
    named_group("centimeters", ONE_CENTIMETER),
    named_group("millimeters", ONE_MILLIMETER),
    named_group("decimeters", ONE_DECIMETER),
    named_group("feet", ONE_FOOT),
    named_group("inches", ONE_INCH),
    named_group("yards", ONE_YARD),
    named_group("miles", ONE_MILE),
)

RULE_DISTANCE_KILOMETERS = FunctionValue(
    parse_distance,
    combine_patterns(
        get_pattern(
            ONE_KILOMETER,
            named_group("kilometers", ONE_KILOMETER),
            _kilometers,
        )
    ),
)
RULE_DISTANCE_CENTIMETERS = FunctionValue(
    parse_distance,
    combine_patterns(
        get_pattern(
            ONE_CENTIMETER,
            named_group("centimeters", ONE_CENTIMETER),
            _centimeters,
        )
    ),
)
RULE_DISTANCE_MILLIMETERS = FunctionValue(
    parse_distance,
    combine_patterns(
        get_pattern(
            ONE_MILLIMETER,
            named_group("millimeters", ONE_MILLIMETER),
            _millimeters,
        )
    ),
)
RULE_DISTANCE_DECIMETERS = FunctionValue(
    parse_distance,
    combine_patterns(
        get_pattern(
            ONE_DECIMETER,
            named_group("decimeters", ONE_DECIMETER),
            _decimeters,
        )
    ),
)
RULE_DISTANCE_METERS = FunctionValue(
    parse_distance,
    combine_patterns(
        get_pattern(
            ONE_METER,
            named_group("meters", ONE_METER),
            _meters,
            named_group("meters", TWO_METERS),
        )
    ),
)
RULE_DISTANCE_FEET = FunctionValue(
    parse_distance,
    combine_patterns(
        get_pattern(
            ONE_FOOT,
            named_group("feet", ONE_FOOT),
            _feet,
            named_group("feet", TWO_FEET),
        )
    ),
)
RULE_DISTANCE_INCHES = FunctionValue(
    parse_distance,
    combine_patterns(
        get_pattern(
            ONE_INCH,
            named_group("inches", ONE_INCH),
            _inches,
            named_group("inches", TWO_INCHES),
        )
    ),
)
RULE_DISTANCE_YARDS = FunctionValue(
    parse_distance,
    combine_patterns(
        get_pattern(
            ONE_YARD,
            named_group("yards", ONE_YARD),
            _yards,
        )
    ),
)
RULE_DISTANCE_MILES = FunctionValue(
    parse_distance,
    combine_patterns(
        get_pattern(
            ONE_MILE,
            named_group("miles", ONE_MILE),
            _miles,
            named_group("miles", TWO_MILES),
        )
    ),
)
RULE_DISTANCE = FunctionValue(
    parse_distance,
    wrap_pattern(
        get_pattern(
            non_capturing_group(
                ONE_KILOMETER,
                ONE_CENTIMETER,
                ONE_MILLIMETER,
                ONE_DECIMETER,
                ONE_METER,
                ONE_FOOT,
                ONE_INCH,
                ONE_YARD,
                ONE_MILE,
            ),
            singular_units,
            all_units,
            dual_units,
        ),
    ),
)
