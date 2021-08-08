__all__ = [
    "EXPRESSION_NUMERAL",
    "EXPRESSION_NUMERAL_DECIMALS",
    "EXPRESSION_NUMERAL_INTEGERS",
    "EXPRESSION_NUMERAL_ONES",
    "EXPRESSION_NUMERAL_TENS",
    "EXPRESSION_NUMERAL_HUNDREDS",
    "EXPRESSION_NUMERAL_THOUSANDS",
    "EXPRESSION_NUMERAL_MILLIONS",
    "EXPRESSION_NUMERAL_BILLIONS",
    "EXPRESSION_NUMERAL_TRILLIONS",
]

import itertools as it

from maha.constants import PATTERN_DECIMAL, PATTERN_INTEGER, PATTERN_SPACE

from ..constants import HALF, QUARTER, THIRD, THREE_QUARTERS, WAW_CONNECTOR
from ..interfaces import ExpressionGroup, NumeralType
from .constants import *
from .interface import NumeralExpression

_get_unit_group = lambda v: f"(?P<unit>{v})"
_get_value_group = lambda v: f"(?P<value>{v})"


def _get_pattern(numeral: NumeralType):
    single = str(globals()[f"EXPRESSION_OF_{numeral.name[:-1]}"])
    dual = str(globals()[f"EXPRESSION_OF_TWO_{numeral.name}"])
    plural = str(globals()[f"EXPRESSION_OF_{numeral.name}"])

    # order matters
    _pattern = [
        "{decimal}{space}{unit_single_plural}",
        "{integer}{space}{unit_single_plural}",
        "{tens}{space}{unit_single_plural}",
        "{ones}{space}{unit_single_plural}",
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

    # # Account for no spaces in the hundreds pattern (ثلاثمائة)
    if numeral == NumeralType.HUNDREDS:
        _pattern.insert(
            2, get_group_value_without_unit(EXPRESSION_NUMERAL_PERFECT_HUNDREDS.join())
        )

    pattern = (
        "(?:"
        + "|".join(_pattern).format(
            decimal=_get_value_group(str(EXPRESSION_DECIMALS)),
            integer=_get_value_group(PATTERN_INTEGER),
            space=PATTERN_SPACE,
            half=_get_value_group(str(HALF)),
            third=_get_value_group(str(THIRD)),
            quarter=_get_value_group(str(QUARTER)),
            three_quarter=_get_value_group(str(THREE_QUARTERS)),
            unit_single_plural=_get_unit_group("|".join([single, plural])),
            unit_single=_get_unit_group(single),
            unit_dual=_get_unit_group(dual),
            val=_get_value_group(""),
            tens=_get_value_group(EXPRESSION_NUMERAL_TENS_ONLY.join()),
            ones=_get_value_group(EXPRESSION_NUMERAL_ONES_ONLY.join()),
        )
        + ")"
    )
    return pattern


def get_group_value_without_unit(expression: str):
    return _get_value_group(expression) + _get_unit_group("")


def get_pattern(numeral: NumeralType):
    if numeral == NumeralType.TENS:
        pattern = get_group_value_without_unit(EXPRESSION_NUMERAL_TENS_ONLY)
    elif numeral == NumeralType.ONES:
        pattern = get_group_value_without_unit(EXPRESSION_NUMERAL_ONES_ONLY)
    elif numeral == NumeralType.DECIMALS:
        pattern = get_group_value_without_unit(str(EXPRESSION_DECIMALS))
    elif numeral == NumeralType.INTEGERS:
        pattern = get_group_value_without_unit(PATTERN_INTEGER)
    else:
        pattern = _get_pattern(numeral)
    return pattern


def get_combined_expression(*numerals: NumeralType) -> NumeralExpression:
    patterns = []
    for i, u in enumerate(numerals):
        pattern = get_pattern(u)
        if i == 0:
            pattern = f"(?:^|\\W|{PATTERN_SPACE_OR_NONE}|\\b){pattern}"
        else:
            pattern = f"(?:{WAW_CONNECTOR}{pattern})?"
        if u not in [NumeralType.DECIMALS, NumeralType.INTEGERS]:
            pattern += r"\b"
        patterns.append(pattern)
    return NumeralExpression("".join(patterns))


def get_simple_expression(*words: str):
    return r"\b" + _get_value_group("|".join(words)) + r"\b"


def get_combinations(*patterns: str):
    for (a, b) in it.combinations_with_replacement(patterns, 2):
        yield a + EXPRESSION_OF_FASILA + b
        if a != b:
            yield b + EXPRESSION_OF_FASILA + a


# 0 1 2 3 4 5 6 7 8 9
EXPRESSION_NUMERAL_ONES_ONLY = ExpressionGroup(
    EXPRESSION_OF_ZERO,
    EXPRESSION_OF_ONE,
    EXPRESSION_OF_TWO,
    EXPRESSION_OF_THREE,
    EXPRESSION_OF_FOUR,
    EXPRESSION_OF_FIVE,
    EXPRESSION_OF_SIX,
    EXPRESSION_OF_SEVEN,
    EXPRESSION_OF_EIGHT,
    EXPRESSION_OF_NINE,
)

# 20 30 40 50 60 70 80 90
EXPRESSION_NUMERAL_PERFECT_TENS = ExpressionGroup(
    EXPRESSION_OF_TWENTY,
    EXPRESSION_OF_THIRTY,
    EXPRESSION_OF_FORTY,
    EXPRESSION_OF_FIFTY,
    EXPRESSION_OF_SIXTY,
    EXPRESSION_OF_SEVENTY,
    EXPRESSION_OF_EIGHTY,
    EXPRESSION_OF_NINETY,
)
# 21 22 23 24 ... 96 97 98 99
EXPRESSION_NUMERAL_COMBINED_TENS = Expression(
    EXPRESSION_NUMERAL_ONES_ONLY.join()
    + WAW_CONNECTOR
    + EXPRESSION_NUMERAL_PERFECT_TENS.join()
)
# 10 11 12 13 14 ... 95 96 97 98 99
EXPRESSION_NUMERAL_TENS_ONLY = ExpressionGroup(
    EXPRESSION_NUMERAL_PERFECT_TENS,
    EXPRESSION_NUMERAL_COMBINED_TENS,
    EXPRESSION_OF_ELEVEN,
    EXPRESSION_OF_TWELVE,
    EXPRESSION_OF_THIRTEEN,
    EXPRESSION_OF_FOURTEEN,
    EXPRESSION_OF_FIFTEEN,
    EXPRESSION_OF_SIXTEEN,
    EXPRESSION_OF_SEVENTEEN,
    EXPRESSION_OF_EIGHTEEN,
    EXPRESSION_OF_NINETEEN,
    EXPRESSION_OF_TEN,
)

# 300 400 500 600 700 800 900
EXPRESSION_NUMERAL_PERFECT_HUNDREDS = ExpressionGroup(
    EXPRESSION_OF_THREE_HUNDREDS,
    EXPRESSION_OF_FOUR_HUNDREDS,
    EXPRESSION_OF_FIVE_HUNDREDS,
    EXPRESSION_OF_SIX_HUNDREDS,
    EXPRESSION_OF_SEVEN_HUNDREDS,
    EXPRESSION_OF_EIGHT_HUNDREDS,
    EXPRESSION_OF_NINE_HUNDREDS,
)

EXPRESSION_DECIMALS = Expression(
    get_non_capturing_group(
        (PATTERN_DECIMAL),
        *list(
            get_combinations(
                PATTERN_INTEGER,
                EXPRESSION_NUMERAL_TENS_ONLY.join(),
                EXPRESSION_NUMERAL_ONES_ONLY.join(),
            )
        ),
    )
)

EXPRESSION_NUMERAL_DECIMALS = get_combined_expression(NumeralType.DECIMALS)
EXPRESSION_NUMERAL_INTEGERS = get_combined_expression(NumeralType.INTEGERS)
EXPRESSION_NUMERAL_ONES = get_combined_expression(NumeralType.ONES)
EXPRESSION_NUMERAL_TENS = get_combined_expression(
    NumeralType.TENS,
    NumeralType.ONES,
)
EXPRESSION_NUMERAL_HUNDREDS = get_combined_expression(
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)
EXPRESSION_NUMERAL_THOUSANDS = get_combined_expression(
    NumeralType.THOUSANDS,
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)
EXPRESSION_NUMERAL_MILLIONS = get_combined_expression(
    NumeralType.MILLIONS,
    NumeralType.THOUSANDS,
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)
EXPRESSION_NUMERAL_BILLIONS = get_combined_expression(
    NumeralType.BILLIONS,
    NumeralType.MILLIONS,
    NumeralType.THOUSANDS,
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)
EXPRESSION_NUMERAL_TRILLIONS = get_combined_expression(
    NumeralType.TRILLIONS,
    NumeralType.BILLIONS,
    NumeralType.MILLIONS,
    NumeralType.THOUSANDS,
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)

EXPRESSION_NUMERAL = ExpressionGroup(
    EXPRESSION_NUMERAL_DECIMALS,
    EXPRESSION_NUMERAL_INTEGERS,
    EXPRESSION_NUMERAL_TRILLIONS,
    EXPRESSION_NUMERAL_BILLIONS,
    EXPRESSION_NUMERAL_MILLIONS,
    EXPRESSION_NUMERAL_THOUSANDS,
    EXPRESSION_NUMERAL_HUNDREDS,
    EXPRESSION_NUMERAL_TENS,
    EXPRESSION_NUMERAL_ONES,
    smart=True,
)


ORDERED_NUMERALS = ExpressionGroup(
    EXPRESSION_OF_TWO_HUNDREDS,
    EXPRESSION_OF_TWO_THOUSANDS,
    EXPRESSION_OF_TWO_MILLIONS,
    EXPRESSION_OF_TWO_BILLIONS,
    EXPRESSION_OF_TWO_TRILLIONS,
    EXPRESSION_OF_HUNDRED,
    EXPRESSION_OF_HUNDREDS,
    EXPRESSION_OF_THOUSANDS,
    EXPRESSION_OF_THOUSAND,
    EXPRESSION_OF_MILLIONS,
    EXPRESSION_OF_MILLION,
    EXPRESSION_OF_BILLIONS,
    EXPRESSION_OF_BILLION,
    EXPRESSION_OF_TRILLIONS,
    EXPRESSION_OF_TRILLION,
    EXPRESSION_NUMERAL_PERFECT_HUNDREDS,
    EXPRESSION_NUMERAL_TENS_ONLY,
    EXPRESSION_NUMERAL_ONES_ONLY,
    THREE_QUARTERS,
    HALF,
    QUARTER,
    THIRD,
)
""" The order of which the expressions are evaluated. """
