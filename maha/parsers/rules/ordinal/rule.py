from __future__ import annotations

__all__ = [
    "RULE_ORDINAL_ONES",
    "RULE_ORDINAL_TENS",
    "RULE_ORDINAL_HUNDREDS",
    "RULE_ORDINAL_THOUSANDS",
    "RULE_ORDINAL_MILLIONS",
    "RULE_ORDINAL_BILLIONS",
    "RULE_ORDINAL_TRILLIONS",
    "RULE_ORDINAL",
    "parse_ordinal",
]


from maha.parsers.templates import FunctionValue
from maha.rexy import (
    Expression,
    ExpressionGroup,
    named_group,
    non_capturing_group,
    optional_non_capturing_group,
)

from ..common import (
    AFTER,
    WAW_CONNECTOR,
    combine_patterns,
    spaced_patterns,
    wrap_pattern,
)
from .values import *


def match_tens(match):
    matched_text = match.group(0)
    return parse_tens(matched_text)


def parse_tens(matched_text):
    waw = WAW_CONNECTOR.search(matched_text)
    if waw:
        _ones, _tens = matched_text.split(waw.group(0))
        value = (
            ones_prefix.get_matched_expression(_ones).value  # type: ignore
            + perfect_tens.get_matched_expression(_tens).value  # type: ignore
        )
        return value
    exp = perfect_tens.get_matched_expression(matched_text)
    if not exp:
        exp = eleven_to_nineteen.get_matched_expression(matched_text)
    return exp.value  # type: ignore


def parse_ordinal(match):
    groups = match.capturesdict()
    _trillions = groups.get("trillions")
    _billions = groups.get("billions")
    _millions = groups.get("millions")
    _thousands = groups.get("thousands")
    _hundreds = groups.get("hundreds")
    _tens = groups.get("tens")
    _ones = groups.get("ones")
    _after_value = groups.get("after_value")
    value = 0

    def get_value(groups, expressions: list[ExpressionGroup | Expression]) -> int:
        exp_group = ExpressionGroup(*expressions)
        value = 0
        for group in groups:
            value += exp_group.get_matched_expression(group).value  # type: ignore
        return value

    if _trillions:
        value += get_value(_trillions, [ONE_TRILLION, TWO_TRILLIONS])
    if _billions:
        value += get_value(_billions, [ONE_BILLION, TWO_BILLIONS])
    if _millions:
        value += get_value(_millions, [ONE_MILLION, TWO_MILLIONS])
    if _thousands:
        value += get_value(_thousands, [ONE_THOUSAND, TWO_THOUSANDS])
    if _hundreds:
        value += get_value(_hundreds, [perfect_hundreds, ONE_HUNDRED, TWO_HUNDREDS])
    if _tens:
        value += parse_tens(_tens[0])
    if _ones:
        value += get_value(_ones, [ones])
    if _after_value:
        value += get_value(_after_value, [after_values])

    return value


after_values = ExpressionGroup(
    ONE_HUNDRED,
    ONE_THOUSAND,
    ONE_MILLION,
    ONE_BILLION,
    ONE_TRILLION,
)
ones = ExpressionGroup(ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN)
ones_prefix = ExpressionGroup(
    ONE_PREFIX,
    TWO_PREFIX,
    THREE_PREFIX,
    FOUR_PREFIX,
    FIVE_PREFIX,
    SIX_PREFIX,
    SEVEN_PREFIX,
    EIGHT_PREFIX,
    NINE_PREFIX,
)
perfect_tens = ExpressionGroup(
    TEN, TWENTY, THIRTY, FORTY, FIFTY, SIXTY, SEVENTY, EIGHTY, NINETY
)
combined_tens = ones_prefix.join() + WAW_CONNECTOR + perfect_tens[1:].join()  # type: ignore
eleven_to_nineteen = ExpressionGroup(
    ELEVEN, TWELVE, THIRTEEN, FOURTEEN, FIFTEEN, SIXTEEN, SEVENTEEN, EIGHTEEN, NINETEEN
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

# 10 11 12 13 14 ... 95 96 97 98 99
tens = non_capturing_group(
    perfect_tens.join(),
    combined_tens,
    eleven_to_nineteen.join(),
)

tens_group = named_group("tens", tens)
ones_group = named_group("ones", ones.join())
hundreds_group = named_group(
    "hundreds",
    non_capturing_group(
        perfect_hundreds.join(),
        spaced_patterns(tens, ONE_HUNDRED),
        spaced_patterns(ones_prefix.join(), ONE_HUNDRED),
    ),
)
thousands_group = named_group(
    "thousands",
    non_capturing_group(
        spaced_patterns(tens, ONE_THOUSAND),
        spaced_patterns(ones_prefix.join(), ONE_THOUSAND),
        str(TWO_THOUSANDS),
        str(ONE_THOUSAND),
    ),
)
millions_group = named_group(
    "millions",
    non_capturing_group(
        spaced_patterns(tens, ONE_MILLION),
        spaced_patterns(ones_prefix.join(), ONE_MILLION),
        str(TWO_MILLIONS),
        str(ONE_MILLION),
    ),
)
billions_group = named_group(
    "billions",
    non_capturing_group(
        spaced_patterns(tens, ONE_BILLION),
        spaced_patterns(ones_prefix.join(), ONE_BILLION),
        str(TWO_BILLIONS),
        str(ONE_BILLION),
    ),
)
trillions_group = named_group(
    "trillions",
    non_capturing_group(
        spaced_patterns(tens, ONE_TRILLION),
        spaced_patterns(ones_prefix.join(), ONE_TRILLION),
        str(TWO_TRILLIONS),
        str(ONE_TRILLION),
    ),
)


RULE_ORDINAL_ONES = FunctionValue(parse_ordinal, combine_patterns(ones_group))
RULE_ORDINAL_TENS = FunctionValue(parse_ordinal, combine_patterns(tens_group))
RULE_ORDINAL_HUNDREDS = FunctionValue(
    parse_ordinal, combine_patterns(hundreds_group, tens_group, ones_group)
)
RULE_ORDINAL_THOUSANDS = FunctionValue(
    parse_ordinal,
    combine_patterns(thousands_group, hundreds_group, tens_group, ones_group),
)
RULE_ORDINAL_MILLIONS = FunctionValue(
    parse_ordinal,
    combine_patterns(
        millions_group, thousands_group, hundreds_group, tens_group, ones_group
    ),
)
RULE_ORDINAL_BILLIONS = FunctionValue(
    parse_ordinal,
    combine_patterns(
        billions_group,
        millions_group,
        thousands_group,
        hundreds_group,
        tens_group,
        ones_group,
    ),
)
RULE_ORDINAL_TRILLIONS = FunctionValue(
    parse_ordinal,
    combine_patterns(
        trillions_group,
        billions_group,
        millions_group,
        thousands_group,
        hundreds_group,
        tens_group,
        ones_group,
    ),
)

RULE_ORDINAL = FunctionValue(
    parse_ordinal,
    wrap_pattern(
        non_capturing_group(
            trillions_group,
            billions_group,
            millions_group,
            thousands_group,
            combine_patterns(hundreds_group, tens_group, ones_group),
            tens_group,
            ones_group,
        )
        + optional_non_capturing_group(
            EXPRESSION_SPACE
            + spaced_patterns(
                AFTER,
                named_group("after_value", after_values.join()),
            ),
        ),
    ),
)
