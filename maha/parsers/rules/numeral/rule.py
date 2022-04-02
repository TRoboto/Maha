from __future__ import annotations

__all__ = [
    "RULE_NUMERAL_ONES",
    "RULE_NUMERAL_TENS",
    "RULE_NUMERAL_HUNDREDS",
    "RULE_NUMERAL_THOUSANDS",
    "RULE_NUMERAL_MILLIONS",
    "RULE_NUMERAL_BILLIONS",
    "RULE_NUMERAL_TRILLIONS",
    "RULE_NUMERAL_INTEGERS",
    "RULE_NUMERAL",
]

from functools import reduce

from maha.expressions import EXPRESSION_DECIMAL, EXPRESSION_INTEGER, EXPRESSION_SPACE
from maha.parsers.rules.ordinal.values import ALEF_LAM
from maha.parsers.templates import FunctionValue
from maha.parsers.utils import convert_to_number_if_possible
from maha.rexy import (
    ExpressionGroup,
    named_group,
    non_capturing_group,
    optional_non_capturing_group,
)

from ..common import (
    HALF,
    QUARTER,
    THIRD,
    THREE_QUARTERS,
    TWO_THIRDS,
    WAW_CONNECTOR,
    combine_patterns,
    spaced_patterns,
)
from .values import *

NUMERAL_VALUES_GROUP_NAME = "numeral_values"
MULTIPLIERS_GROUP_NAME = "multipliers"
DECIMAL_PART_GROUP_NAME = "decimal_part"


def numeral_group(pattern):
    return named_group(NUMERAL_VALUES_GROUP_NAME, pattern)


def _construct_numeral(sorted_values) -> float:
    output = [0] * len(sorted_values)
    last_numeral_index = 0
    multiply = False
    is_perfect_hundred = False
    for i, (_, dict_value) in enumerate(sorted_values.items()):
        group = dict_value["group"]
        exp = EXPRESSION_NUMERAL_MAP[group].get_matched_expression(dict_value["value"])
        assert exp is not None
        value = next(iter(exp(dict_value["value"]))).value
        if group == NUMERAL_VALUES_GROUP_NAME:
            if not is_perfect_hundred:
                last_numeral_index = i
            if multiply:
                output[last_numeral_index] *= value
                multiply = False
            else:
                output[last_numeral_index] += value
        elif group == "before_fractions":
            output[i + 1] = value
            multiply = True
        elif group == MULTIPLIERS_GROUP_NAME:
            output[last_numeral_index] *= value
        elif group == "after_fraction":
            output[last_numeral_index] *= value

        is_perfect_hundred = bool(
            perfect_hundreds.get_matched_expression(dict_value["value"])
        )

    total = sum(output)
    # to int if possible
    if total == int(total):
        total = int(total)
    return total


def _parse_numeral(sorted_values):
    decimal_part_index = 0
    for k, v in sorted_values.items():
        if DECIMAL_PART_GROUP_NAME == v["group"]:
            decimal_part_index = k
    if decimal_part_index:
        integer = _construct_numeral(
            {k: v for k, v in sorted_values.items() if k < decimal_part_index}
        )

        # check if decimal ends with a multiplier
        decimal_values = {
            k: v for k, v in sorted_values.items() if k > decimal_part_index
        }
        multipliers = [1, 1]
        for k, v in reversed(list(decimal_values.items())):
            if MULTIPLIERS_GROUP_NAME == v["group"]:
                multipliers.append(
                    MULTIPLIERS.get_matched_expression(v["value"]).value  # type: ignore
                )
                decimal_values.pop(k)
            else:
                break

        decimal = _construct_numeral(decimal_values)
        # check if decimal is already a float
        if int(decimal) != decimal:
            output = integer + decimal
        else:
            output = integer + decimal / 10 ** len(str(decimal))
        output *= reduce(lambda x, y: x * y, multipliers)
        if output.is_integer():
            output = int(output)
        return output
    return _construct_numeral(sorted_values)


def parse_numeral(match):
    groups = match.capturesdict()
    groups_keys = list(groups)

    if not groups_keys:
        return

    sorted_values = {}
    for group in EXPRESSION_NUMERAL_MAP:
        if group not in groups_keys:
            continue
        for i, value in enumerate(groups.get(group)):
            index = match.starts(groups_keys.index(group) + 1)[i]
            sorted_values[index] = {"group": group, "value": value}
    # sort by index
    sorted_values = dict(sorted(sorted_values.items()))

    return _parse_numeral(sorted_values)


ones = ExpressionGroup(ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE)
perfect_tens = ExpressionGroup(
    TWENTY, THIRTY, FORTY, FIFTY, SIXTY, SEVENTY, EIGHTY, NINETY
)
eleven_to_nineteen = ExpressionGroup(
    ELEVEN, TWELVE, THIRTEEN, FOURTEEN, FIFTEEN, SIXTEEN, SEVENTEEN, EIGHTEEN, NINETEEN
)

COMBINED_TENS = FunctionValue(
    lambda match: ones.get_matched_expression(match.group("ones")).value  # type: ignore
    + perfect_tens.get_matched_expression(match.group("tens")).value,  # type: ignore
    named_group("ones", ones.join())
    + WAW_CONNECTOR
    + named_group("tens", perfect_tens.join()),
)
TENS = ExpressionGroup(
    perfect_tens,
    COMBINED_TENS,
    eleven_to_nineteen,
    TEN,
)
perfect_hundreds = ExpressionGroup(
    ONE_HUNDRED,
    TWO_HUNDREDS,
    THREE_HUNDREDS,
    FOUR_HUNDREDS,
    FIVE_HUNDREDS,
    SIX_HUNDREDS,
    SEVEN_HUNDREDS,
    EIGHT_HUNDREDS,
    NINE_HUNDREDS,
)
RULE_NUMERAL_INTEGERS = FunctionValue(
    lambda match: convert_to_number_if_possible(str(match.group())),
    str(EXPRESSION_INTEGER),
)
RULE_NUMERAL_DECIMALS = FunctionValue(
    lambda match: convert_to_number_if_possible(str(match.group())),
    str(EXPRESSION_DECIMAL),
)
SINGLE_MULTIPLIERS = ExpressionGroup(
    ONE_HUNDRED,
    ONE_THOUSAND,
    ONE_MILLION,
    ONE_BILLION,
    ONE_TRILLION,
)
MULTIPLIERS = ExpressionGroup(
    SINGLE_MULTIPLIERS,
    SEVERAL_HUNDREDS,
    SEVERAL_THOUSANDS,
    SEVERAL_MILLIONS,
    SEVERAL_BILLIONS,
    SEVERAL_TRILLIONS,
)
NUMERAL_COMMON_VALUES = ExpressionGroup(
    COMBINED_TENS,
    perfect_tens,
    eleven_to_nineteen,
    TEN,
    ones,
    RULE_NUMERAL_DECIMALS,
    RULE_NUMERAL_INTEGERS,
)
NUMERAL_VALUES = ExpressionGroup(
    TWO_HUNDREDS,
    TWO_THOUSANDS,
    TWO_MILLIONS,
    TWO_BILLIONS,
    TWO_TRILLIONS,
    perfect_hundreds,
    # ONE_HUNDRED, Already defined in perfect_hundreds
    ONE_THOUSAND,
    ONE_MILLION,
    ONE_BILLION,
    ONE_TRILLION,
    COMBINED_TENS,
    perfect_tens,
    eleven_to_nineteen,
    TEN,
    ones,
    RULE_NUMERAL_DECIMALS,
    RULE_NUMERAL_INTEGERS,
)
multiplier_fraction_group = named_group(
    "multiplier",
    non_capturing_group(*MULTIPLIERS.expressions, TEN)
    + non_capturing_group(
        EXPRESSION_SPACE + non_capturing_group(*MULTIPLIERS.expressions, TEN)
    )
    + "*",
)
MULTIPLIERS_FRACTION = FunctionValue(
    lambda match: (
        1
        / reduce(
            lambda a, b: a * b,
            [
                a.value
                for a in ExpressionGroup(MULTIPLIERS, TEN).parse(
                    match.group("multiplier")
                )
            ],
        )
    ),
    non_capturing_group(
        non_capturing_group("في" + EXPRESSION_SPACE, "ب")
        + ALEF_LAM
        + multiplier_fraction_group,
        spaced_patterns("من", multiplier_fraction_group),
    ),
)
BEFORE_FRACTIONS = ExpressionGroup(HALF, THIRD, QUARTER)
AFTER_FRACTION = ExpressionGroup(THREE_QUARTERS, TWO_THIRDS, MULTIPLIERS_FRACTION)
before_fractions_group = named_group("before_fractions", BEFORE_FRACTIONS.join())
after_fraction_group = named_group("after_fraction", AFTER_FRACTION.join())


def get_pattern(
    numeral_exp_group: ExpressionGroup, multipliers_exp_group: ExpressionGroup
) -> str:
    pattern = non_capturing_group(
        optional_non_capturing_group(before_fractions_group + EXPRESSION_SPACE)
        + named_group(NUMERAL_VALUES_GROUP_NAME, numeral_exp_group.join())
        + non_capturing_group(
            WAW_CONNECTOR
            + named_group(NUMERAL_VALUES_GROUP_NAME, numeral_exp_group.join())
        )
        + "*"
        + optional_non_capturing_group(EXPRESSION_SPACE + after_fraction_group)
        + non_capturing_group(
            EXPRESSION_SPACE
            + named_group(MULTIPLIERS_GROUP_NAME, multipliers_exp_group.join())
        )
        + "*"
    )
    return pattern


RULE_NUMERAL_ONES = FunctionValue(
    parse_numeral, named_group(NUMERAL_VALUES_GROUP_NAME, ones.join())
)
RULE_NUMERAL_TENS = FunctionValue(
    parse_numeral, named_group(NUMERAL_VALUES_GROUP_NAME, TENS.join())
)
RULE_NUMERAL_HUNDREDS = FunctionValue(
    parse_numeral,
    combine_patterns(
        get_pattern(
            ExpressionGroup(TWO_HUNDREDS, perfect_hundreds),
            ExpressionGroup(SEVERAL_HUNDREDS, ONE_HUNDRED),
        ),
        RULE_NUMERAL_TENS,
        RULE_NUMERAL_ONES,
    ),
)
RULE_NUMERAL_THOUSANDS = FunctionValue(
    parse_numeral,
    combine_patterns(
        get_pattern(
            ExpressionGroup(TWO_THOUSANDS, ONE_THOUSAND),
            ExpressionGroup(SEVERAL_THOUSANDS, ONE_THOUSAND),
        ),
        get_pattern(
            ExpressionGroup(TWO_HUNDREDS, perfect_hundreds),
            ExpressionGroup(SEVERAL_HUNDREDS, ONE_HUNDRED),
        ),
        RULE_NUMERAL_TENS,
        RULE_NUMERAL_ONES,
    ),
)
RULE_NUMERAL_MILLIONS = FunctionValue(
    parse_numeral,
    combine_patterns(
        get_pattern(
            ExpressionGroup(TWO_MILLIONS, ONE_MILLION),
            ExpressionGroup(SEVERAL_MILLIONS, ONE_MILLION),
        ),
        get_pattern(
            ExpressionGroup(
                TWO_HUNDREDS, perfect_hundreds, TWO_THOUSANDS, ONE_THOUSAND
            ),
            ExpressionGroup(
                SEVERAL_HUNDREDS, ONE_HUNDRED, SEVERAL_THOUSANDS, ONE_THOUSAND
            ),
        ),
        RULE_NUMERAL_TENS,
        RULE_NUMERAL_ONES,
    ),
)
RULE_NUMERAL_BILLIONS = FunctionValue(
    parse_numeral,
    combine_patterns(
        get_pattern(
            ExpressionGroup(TWO_BILLIONS, ONE_BILLION),
            ExpressionGroup(SEVERAL_BILLIONS, ONE_BILLION),
        ),
        get_pattern(
            ExpressionGroup(
                TWO_HUNDREDS,
                perfect_hundreds,
                TWO_THOUSANDS,
                ONE_THOUSAND,
                TWO_MILLIONS,
                ONE_MILLION,
            ),
            ExpressionGroup(
                SEVERAL_HUNDREDS,
                ONE_HUNDRED,
                SEVERAL_THOUSANDS,
                ONE_THOUSAND,
                SEVERAL_MILLIONS,
                ONE_MILLION,
            ),
        ),
        RULE_NUMERAL_TENS,
        RULE_NUMERAL_ONES,
    ),
)
RULE_NUMERAL_TRILLIONS = FunctionValue(
    parse_numeral,
    combine_patterns(
        get_pattern(
            ExpressionGroup(TWO_TRILLIONS, ONE_TRILLION),
            ExpressionGroup(SEVERAL_TRILLIONS, ONE_TRILLION),
        ),
        get_pattern(
            ExpressionGroup(
                TWO_HUNDREDS,
                perfect_hundreds,
                TWO_THOUSANDS,
                ONE_THOUSAND,
                TWO_MILLIONS,
                ONE_MILLION,
                TWO_BILLIONS,
                ONE_BILLION,
            ),
            ExpressionGroup(
                SEVERAL_HUNDREDS,
                ONE_HUNDRED,
                SEVERAL_THOUSANDS,
                ONE_THOUSAND,
                SEVERAL_MILLIONS,
                ONE_MILLION,
                SEVERAL_BILLIONS,
                ONE_BILLION,
            ),
        ),
        RULE_NUMERAL_TENS,
        RULE_NUMERAL_ONES,
    ),
)

_numeral_numeral_pattern = get_pattern(NUMERAL_VALUES, MULTIPLIERS)
_all_numeral_numeral_pattern = combine_patterns(
    _numeral_numeral_pattern, seperator=WAW_CONNECTOR
)
RULE_NUMERAL = FunctionValue(
    parse_numeral,
    _all_numeral_numeral_pattern
    + optional_non_capturing_group(
        named_group(
            DECIMAL_PART_GROUP_NAME,
            EXPRESSION_SPACE
            + spaced_patterns(EXPRESSION_OF_FASILA, _all_numeral_numeral_pattern),
        )
    ),
)

EXPRESSION_NUMERAL_MAP = {
    "before_fractions": BEFORE_FRACTIONS,
    "after_fraction": AFTER_FRACTION,
    NUMERAL_VALUES_GROUP_NAME: NUMERAL_VALUES,
    MULTIPLIERS_GROUP_NAME: MULTIPLIERS,
    DECIMAL_PART_GROUP_NAME: ExpressionGroup(),
}
