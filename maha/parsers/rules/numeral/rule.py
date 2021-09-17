__all__ = [
    "RULE_NUMERAL_ONES",
    "RULE_NUMERAL_TENS",
    "RULE_NUMERAL_HUNDREDS",
    "RULE_NUMERAL_THOUSANDS",
    "RULE_NUMERAL_MILLIONS",
    "RULE_NUMERAL_BILLIONS",
    "RULE_NUMERAL_TRILLIONS",
    "RULE_NUMERAL_INTEGERS",
    "RULE_NUMERAL_DECIMALS",
    "RULE_NUMERAL",
    "parse_numeral",
]

import itertools as it
from typing import Optional

from maha.expressions import EXPRESSION_DECIMAL, EXPRESSION_INTEGER
from maha.parsers.templates import FunctionValue
from maha.parsers.utils import convert_to_number_if_possible
from maha.rexy import ExpressionGroup, named_group, non_capturing_group

from ..common import (
    FRACTIONS,
    WAW_CONNECTOR,
    combine_patterns,
    get_fractions_of_unit_pattern,
    spaced_patterns,
)
from .values import *


def get_combined_value(groups, multiplier="") -> float:

    singular = globals().get("ONE_" + multiplier[:-1].upper())
    dual = globals().get("TWO_" + multiplier.upper())
    plural = globals().get("SEVERAL_" + multiplier.upper())
    value = 0
    for group in groups:
        mul = get_matched_value(group, singular, dual)
        if mul:
            value += mul
        else:
            value += parse_combined(group, singular, plural)
    return value


def get_matched_value(matched_text, dual, singular):
    if not (dual or singular):
        return
    if dual.fullmatch(matched_text):
        return dual.value
    if singular.fullmatch(matched_text):
        return singular.value


def parse_ones(text):
    exp = ones.get_matched_expression(text)
    if exp:
        return exp.value  # type: ignore


def parse_tens(matched_text):
    waw = WAW_CONNECTOR.search(matched_text)
    if waw:
        _ones, _tens = matched_text.split(waw.group(0))
        value = (
            ones.get_matched_expression(_ones).value  # type: ignore
            + perfect_tens.get_matched_expression(_tens).value  # type: ignore
        )
        return value
    exp = perfect_tens.get_matched_expression(matched_text)
    if not exp:
        exp = eleven_to_nineteen.get_matched_expression(matched_text)
    if not exp and TEN.match(matched_text):
        return TEN.value

    if exp:
        return exp.value  # type: ignore


def parse_fasila(matched_text: str) -> Optional[float]:
    """
    Handle fasila in the numeral expression

    Parameters
    ----------
    matched_text : str
        Numeral text with fasila.

    Returns
    -------
    Optional[float]
        Float number.
    """
    if isinstance(matched_text, list):
        for group in matched_text:
            return parse_fasila(group)

    fasila = EXPRESSION_OF_FASILA.search(matched_text)
    if not fasila:
        return None
    before, after = matched_text.split(fasila.group(0))
    before = parse_combined(before)
    after = parse_combined(after)
    output = float(f"{before}.{after}")
    return output


def parse_combined(matched_text, singular=None, plural=None):
    value = 1
    if singular and plural:
        multiplier = plural.search(matched_text) or singular.search(matched_text)
        matched_text = matched_text.replace(multiplier.group(0), "").strip()
        value = singular.value

    number = EXPRESSION_DECIMAL.fullmatch(matched_text) or EXPRESSION_INTEGER.fullmatch(
        matched_text
    )
    if number is not None:
        number = convert_to_number_if_possible(number.group())
    tens = parse_tens(matched_text)
    ones = parse_ones(matched_text)
    fraction = FRACTIONS.get_matched_expression(matched_text)
    if number is not None:
        value *= number
    elif tens is not None:
        value *= tens
    elif ones is not None:
        value *= ones
    elif fraction is not None:
        value *= fraction.value  # type: ignore
    return value


def parse_numeral(match):
    groups = match.capturesdict()
    _trillions = groups.get("trillions")
    _billions = groups.get("billions")
    _millions = groups.get("millions")
    _thousands = groups.get("thousands")
    _hundreds = groups.get("hundreds")
    _tens = groups.get("tens")
    _ones = groups.get("ones")
    _decimals = groups.get("decimals")
    _integers = groups.get("integers")
    value = 0

    if _trillions:
        value += get_combined_value(_trillions, "trillions")
    if _billions:
        value += get_combined_value(_billions, "billions")
    if _millions:
        value += get_combined_value(_millions, "millions")
    if _thousands:
        value += get_combined_value(_thousands, "thousands")
    if _hundreds:
        value += get_combined_value(_hundreds, "hundreds")
    if _tens:
        value += get_combined_value(_tens)
    if _ones:
        value += get_combined_value(_ones)
    if _decimals:
        v = parse_fasila(_decimals)
        if v is not None:
            value += v
        else:
            value += get_combined_value(_decimals)
    if _integers:
        value += get_combined_value(_integers)

    return value


def get_combinations(*patterns: str):
    for (a, b) in it.combinations_with_replacement(patterns, 2):
        yield a + str(EXPRESSION_OF_FASILA) + b
        if a != b:
            yield b + str(EXPRESSION_OF_FASILA) + a


def get_patterns(one, two, several):
    return non_capturing_group(
        spaced_patterns(EXPRESSION_DECIMAL, non_capturing_group(one, several)),
        spaced_patterns(EXPRESSION_INTEGER, non_capturing_group(one, several)),
        spaced_patterns(tens, non_capturing_group(one, several)),
        spaced_patterns(ones.join(), non_capturing_group(one, several)),
        get_fractions_of_unit_pattern(str(one)),
        two,
        one,
    )


ones = ExpressionGroup(ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE)
perfect_tens = ExpressionGroup(
    TWENTY, THIRTY, FORTY, FIFTY, SIXTY, SEVENTY, EIGHTY, NINETY
)
combined_tens = ones.join() + WAW_CONNECTOR + perfect_tens.join()
eleven_to_nineteen = ExpressionGroup(
    ELEVEN, TWELVE, THIRTEEN, FOURTEEN, FIFTEEN, SIXTEEN, SEVENTEEN, EIGHTEEN, NINETEEN
)
tens = non_capturing_group(
    perfect_tens.join(),
    combined_tens,
    eleven_to_nineteen.join(),
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
ones_group = named_group("ones", ones.join())
tens_group = named_group("tens", tens)
hundreds_group = named_group(
    "hundreds",
    non_capturing_group(
        perfect_hundreds[2:].join(),
        get_patterns(ONE_HUNDRED, TWO_HUNDREDS, SEVERAL_HUNDREDS),
    ),
)
thousands_group = named_group(
    "thousands", get_patterns(ONE_THOUSAND, TWO_THOUSANDS, SEVERAL_THOUSANDS)
)
millions_group = named_group(
    "millions", get_patterns(ONE_MILLION, TWO_MILLIONS, SEVERAL_MILLIONS)
)
billions_group = named_group(
    "billions", get_patterns(ONE_BILLION, TWO_BILLIONS, SEVERAL_BILLIONS)
)
trillions_group = named_group(
    "trillions", get_patterns(ONE_TRILLION, TWO_TRILLIONS, SEVERAL_TRILLIONS)
)

integer_group = named_group("integers", str(EXPRESSION_INTEGER))
decimal_group = named_group(
    "decimals",
    non_capturing_group(
        str(EXPRESSION_DECIMAL),
        *list(get_combinations(str(EXPRESSION_INTEGER), tens, ones.join())),
    ),
)

RULE_NUMERAL_ONES = FunctionValue(parse_numeral, ones_group)
RULE_NUMERAL_TENS = FunctionValue(parse_numeral, tens_group)
RULE_NUMERAL_HUNDREDS = FunctionValue(
    parse_numeral, combine_patterns(hundreds_group, tens_group, ones_group)
)
RULE_NUMERAL_THOUSANDS = FunctionValue(
    parse_numeral,
    combine_patterns(thousands_group, hundreds_group, tens_group, ones_group),
)
RULE_NUMERAL_MILLIONS = FunctionValue(
    parse_numeral,
    combine_patterns(
        millions_group, thousands_group, hundreds_group, tens_group, ones_group
    ),
)
RULE_NUMERAL_BILLIONS = FunctionValue(
    parse_numeral,
    combine_patterns(
        billions_group,
        millions_group,
        thousands_group,
        hundreds_group,
        tens_group,
        ones_group,
    ),
)
RULE_NUMERAL_TRILLIONS = FunctionValue(
    parse_numeral,
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
RULE_NUMERAL_INTEGERS = FunctionValue(parse_numeral, integer_group)
RULE_NUMERAL_DECIMALS = FunctionValue(parse_numeral, decimal_group)

RULE_NUMERAL = FunctionValue(
    parse_numeral,
    combine_patterns(
        trillions_group,
        billions_group,
        millions_group,
        thousands_group,
        hundreds_group,
        decimal_group,
        tens_group,
        ones_group,
        integer_group,
        combine_all=True,
    ),
)
