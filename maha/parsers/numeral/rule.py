from maha.constants import PATTERN_DECIMAL, PATTERN_INTEGER, PATTERN_SPACE

from ..constants import (
    HALF,
    QUARTER,
    SUM_SUFFIX,
    THIRD,
    THREE_QUARTERS,
    WAW_CONNECTOR,
    WORD_SEPARATOR,
)
from ..interfaces import ExpressionGroup, NumeralType
from .constants import *
from .interface import NumeralExpression

_get_unit_group = lambda v: f"(?P<unit>{v})"
_get_value_group = lambda v: f"(?P<value>{v})"


def _get_pattern(numeral: NumeralType):
    single = globals()[f"NAME_OF_{numeral.name[:-1]}"]
    dual = globals()[f"NAME_OF_TWO_{numeral.name}"]
    plural = globals()[f"NAME_OF_{numeral.name}"]

    pattern = (
        "(?:"
        + "|".join(
            [
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
        ).format(
            decimal=_get_value_group(PATTERN_DECIMAL),
            integer=_get_value_group(PATTERN_INTEGER),
            space=PATTERN_SPACE,
            half=_get_value_group(HALF),
            third=_get_value_group(THIRD),
            quarter=_get_value_group(QUARTER),
            three_quarter=_get_value_group(THREE_QUARTERS),
            unit_single_plural=_get_unit_group("|".join([single, plural])),
            unit_single=_get_unit_group(single),
            unit_dual=_get_unit_group(dual),
            val=_get_value_group(""),
            tens=EXPRESSION_NUMERAL_TENS.pattern,
            ones=EXPRESSION_NUMERAL_ONES.pattern,
        )
        + ")"
    )
    return pattern


def _get_combined_expression(*numerals: NumeralType) -> NumeralExpression:
    patterns = []
    for i, u in enumerate(numerals):
        pattern = f"(?:{WORD_SEPARATOR}{{}})"
        if u == NumeralType.TENS:
            pattern = pattern.format(
                EXPRESSION_NUMERAL_TENS.pattern.strip(r"\b") + _get_unit_group("")
            )
        elif u == NumeralType.ONES:
            pattern = pattern.format(
                EXPRESSION_NUMERAL_ONES.pattern.strip(r"\b") + _get_unit_group("")
            )
        else:
            pattern = pattern.format(_get_pattern(u))
        if i == 0:
            patterns.append(pattern + "\\b")
        else:
            patterns.append(f"{pattern}?\\b")
    return NumeralExpression(f"".join(patterns))


def get_simple_expression(*words: str):
    return r"\b" + _get_value_group("|".join(words)) + r"\b"


EXPRESSION_NUMERAL_ONES = NumeralExpression(
    get_simple_expression(
        NAME_OF_ZERO,
        NAME_OF_ONE,
        NAME_OF_TWO,
        NAME_OF_THREE,
        NAME_OF_FOUR,
        NAME_OF_FIVE,
        NAME_OF_SIX,
        NAME_OF_SEVEN,
        NAME_OF_EIGHT,
        NAME_OF_NINE,
    )
)

# 20 30 40 50 60 70 80 90
_PATTERN_NUMERAL_PERFECT_TENS = (
    get_non_capturing_group(
        PREFIX_OF_TEN,
        PREFIX_OF_THREE,
        PREFIX_OF_FOUR,
        PREFIX_OF_FIVE,
        PREFIX_OF_SIX,
        PREFIX_OF_SEVEN,
        PREFIX_OF_EIGHT,
        PREFIX_OF_NINE,
    )
    + SUM_SUFFIX
)

# 21 22 23 24 ... 96 97 98 99
_PATTERN_NUMERAL_COMBINED_TENS = (
    get_non_capturing_group(
        NAME_OF_ZERO,
        NAME_OF_ONE,
        NAME_OF_TWO,
        NAME_OF_THREE,
        NAME_OF_FOUR,
        NAME_OF_FIVE,
        NAME_OF_SIX,
        NAME_OF_SEVEN,
        NAME_OF_EIGHT,
        NAME_OF_NINE,
    )
    + WAW_CONNECTOR
    + _PATTERN_NUMERAL_PERFECT_TENS
)

EXPRESSION_NUMERAL_TENS = NumeralExpression(
    get_simple_expression(
        NAME_OF_TEN,
        NAME_OF_ELEVEN,
        NAME_OF_TWELVE,
        NAME_OF_THIRTEEN,
        NAME_OF_FOURTEEN,
        NAME_OF_FIFTEEN,
        NAME_OF_SIXTEEN,
        NAME_OF_SEVENTEEN,
        NAME_OF_EIGHTEEN,
        NAME_OF_NINETEEN,
        _PATTERN_NUMERAL_PERFECT_TENS,
        _PATTERN_NUMERAL_COMBINED_TENS,
    )
)

EXPRESSION_NUMERAL_HUNDREDS = _get_combined_expression(NumeralType.HUNDREDS)
EXPRESSION_NUMERAL_THOUSANDS = _get_combined_expression(NumeralType.THOUSANDS)
EXPRESSION_NUMERAL_MILLIONS = _get_combined_expression(NumeralType.MILLIONS)
EXPRESSION_NUMERAL_BILLIONS = _get_combined_expression(NumeralType.BILLIONS)
EXPRESSION_NUMERAL_TRILLIONS = _get_combined_expression(NumeralType.TRILLIONS)

EXPRESSION_NUMERAL = ExpressionGroup(
    _get_combined_expression(
        NumeralType.TRILLIONS,
        NumeralType.BILLIONS,
        NumeralType.MILLIONS,
        NumeralType.THOUSANDS,
        NumeralType.HUNDREDS,
        NumeralType.TENS,
        NumeralType.ONES,
    ),
    _get_combined_expression(
        NumeralType.BILLIONS,
        NumeralType.MILLIONS,
        NumeralType.THOUSANDS,
        NumeralType.HUNDREDS,
        NumeralType.TENS,
        NumeralType.ONES,
    ),
    _get_combined_expression(
        NumeralType.MILLIONS,
        NumeralType.THOUSANDS,
        NumeralType.HUNDREDS,
        NumeralType.TENS,
        NumeralType.ONES,
    ),
    _get_combined_expression(
        NumeralType.THOUSANDS,
        NumeralType.HUNDREDS,
        NumeralType.TENS,
        NumeralType.ONES,
    ),
    _get_combined_expression(
        NumeralType.HUNDREDS,
        NumeralType.TENS,
        NumeralType.ONES,
    ),
    _get_combined_expression(
        NumeralType.TENS,
        NumeralType.ONES,
    ),
    _get_combined_expression(
        NumeralType.ONES,
    ),
    smart=True,
)
