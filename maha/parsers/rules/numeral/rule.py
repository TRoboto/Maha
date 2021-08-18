__all__ = [
    "RULE_NUMERAL",
    "RULE_NUMERAL_DECIMALS",
    "RULE_NUMERAL_INTEGERS",
    "RULE_NUMERAL_ONES",
    "RULE_NUMERAL_TENS",
    "RULE_NUMERAL_HUNDREDS",
    "RULE_NUMERAL_THOUSANDS",
    "RULE_NUMERAL_MILLIONS",
    "RULE_NUMERAL_BILLIONS",
    "RULE_NUMERAL_TRILLIONS",
]

import itertools as it

from maha.expressions import EXPRESSION_DECIMAL, EXPRESSION_INTEGER, EXPRESSION_SPACE
from maha.parsers.expressions import HALF, QUARTER, THIRD, THREE_QUARTERS, WAW_CONNECTOR
from maha.parsers.helper import *
from maha.parsers.rules.templates.rule import Rule
from maha.parsers.templates import DimensionType, NumeralType
from maha.rexy import ExpressionGroup, named_group, non_capturing_group

from .expression import *
from .template import NumeralExpression

multiplier_group = lambda v: named_group("multiplier", v)
numeral_value = lambda v: named_group("numeral_value", v)


def get_numeral_value_without_multiplier(expression):
    return numeral_value(expression) + multiplier_group("")


def get_fractions_pattern(multiplier: str) -> str:
    """
    Returns the fractions of a multiplier.


    Parameters
    ----------
    multiplier: str
        The multiplier text.

    Returns
    -------
    str
        Pattern for the fractions of the multiplier.
    """

    return non_capturing_group(
        *[
            "{multiplier}{space}{three_quarter}",
            "{half}{space}{multiplier}",
            "{third}{space}{multiplier}",
            "{quarter}{space}{multiplier}",
        ]
    ).format(
        half=numeral_value(HALF),
        third=numeral_value(THIRD),
        quarter=numeral_value(QUARTER),
        three_quarter=numeral_value(THREE_QUARTERS),
        space=EXPRESSION_SPACE,
        multiplier=multiplier_group(multiplier),
    )


class NumeralRule(Rule):
    """Rule to extract a numeral."""

    def __init__(self, *types: NumeralType) -> None:
        """Returns a combined expression for the given types."""
        combined_patterns = self.combine_patterns(*types)
        expression = NumeralExpression(combined_patterns, pickle=True)
        super().__init__(expression, DimensionType.NUMERAL)

    def get_single(self, numeral: NumeralType) -> "Expression":
        return globals()[(f"EXPRESSION_OF_{numeral.name[:-1]}")]

    def get_dual(self, numeral: NumeralType) -> "Expression":
        return globals()[f"EXPRESSION_OF_TWO_{numeral.name}"]

    def get_plural(self, numeral: NumeralType) -> "Expression":
        return globals()[f"EXPRESSION_OF_{numeral.name}"]

    def get_pattern(self, numeral: NumeralType) -> str:
        if numeral == NumeralType.TENS:
            pattern = get_numeral_value_without_multiplier(
                RULE_NUMERAL_TENS_ONLY.join()
            )
        elif numeral == NumeralType.ONES:
            pattern = get_numeral_value_without_multiplier(
                RULE_NUMERAL_ONES_ONLY.join()
            )
        elif numeral == NumeralType.DECIMALS:
            pattern = get_numeral_value_without_multiplier(RULE_DECIMALS)
        elif numeral == NumeralType.INTEGERS:
            pattern = get_numeral_value_without_multiplier(RULE_INTEGERS)
        else:
            pattern = self._get_pattern(numeral)
        return pattern

    def _get_pattern(self, numeral: NumeralType) -> str:

        single = str(self.get_single(numeral))
        dual = str(self.get_dual(numeral))
        plural = str(self.get_plural(numeral))

        # order matters
        _pattern = [
            "{decimal}{space}{multiplier_single_plural}",
            "{integer}{space}{multiplier_single_plural}",
            "{tens}{space}{multiplier_single_plural}",
            "{ones}{space}{multiplier_single_plural}",
            get_fractions_pattern(single),
            get_fractions_pattern(dual),
            "{val}{multiplier_dual}",
            "{val}{multiplier_single}",
        ]
        # # Account for no spaces in the hundreds pattern (ثلاثمائة)
        if numeral == NumeralType.HUNDREDS:
            _pattern.insert(
                2,
                get_numeral_value_without_multiplier(
                    RULE_NUMERAL_PERFECT_HUNDREDS.join()
                ),
            )

        pattern = non_capturing_group(*_pattern).format(
            decimal=numeral_value(RULE_DECIMALS),
            integer=numeral_value(RULE_INTEGERS),
            space=EXPRESSION_SPACE,
            multiplier_single_plural=multiplier_group("|".join([single, plural])),
            multiplier_single=multiplier_group(single),
            multiplier_dual=multiplier_group(dual),
            val=numeral_value(""),
            tens=numeral_value(RULE_NUMERAL_TENS_ONLY.join()),
            ones=numeral_value(RULE_NUMERAL_ONES_ONLY.join()),
        )
        return pattern


def get_combinations(*patterns: str):
    for (a, b) in it.combinations_with_replacement(patterns, 2):
        yield a + EXPRESSION_OF_FASILA + b
        if a != b:
            yield b + EXPRESSION_OF_FASILA + a


# 0 1 2 3 4 5 6 7 8 9
RULE_NUMERAL_ONES_ONLY = ExpressionGroup(
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
RULE_NUMERAL_PERFECT_TENS = ExpressionGroup(
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
RULE_NUMERAL_COMBINED_TENS = Expression(
    RULE_NUMERAL_ONES_ONLY.join() + WAW_CONNECTOR + RULE_NUMERAL_PERFECT_TENS.join()
)
# 10 11 12 13 14 ... 95 96 97 98 99
RULE_NUMERAL_TENS_ONLY = ExpressionGroup(
    RULE_NUMERAL_PERFECT_TENS,
    RULE_NUMERAL_COMBINED_TENS,
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
RULE_NUMERAL_PERFECT_HUNDREDS = ExpressionGroup(
    EXPRESSION_OF_THREE_HUNDREDS,
    EXPRESSION_OF_FOUR_HUNDREDS,
    EXPRESSION_OF_FIVE_HUNDREDS,
    EXPRESSION_OF_SIX_HUNDREDS,
    EXPRESSION_OF_SEVEN_HUNDREDS,
    EXPRESSION_OF_EIGHT_HUNDREDS,
    EXPRESSION_OF_NINE_HUNDREDS,
)

RULE_INTEGERS = EXPRESSION_INTEGER
RULE_DECIMALS = Expression(
    non_capturing_group(
        str(EXPRESSION_DECIMAL),
        *list(
            get_combinations(
                str(RULE_INTEGERS),
                RULE_NUMERAL_TENS_ONLY.join(),
                RULE_NUMERAL_ONES_ONLY.join(),
            )
        ),
    )
)

RULE_NUMERAL_DECIMALS = NumeralRule(NumeralType.DECIMALS)
RULE_NUMERAL_INTEGERS = NumeralRule(NumeralType.INTEGERS)
RULE_NUMERAL_ONES = NumeralRule(NumeralType.ONES)
RULE_NUMERAL_TENS = NumeralRule(
    NumeralType.TENS,
    NumeralType.ONES,
)
RULE_NUMERAL_HUNDREDS = NumeralRule(
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)
RULE_NUMERAL_THOUSANDS = NumeralRule(
    NumeralType.THOUSANDS,
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)
RULE_NUMERAL_MILLIONS = NumeralRule(
    NumeralType.MILLIONS,
    NumeralType.THOUSANDS,
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)
RULE_NUMERAL_BILLIONS = NumeralRule(
    NumeralType.BILLIONS,
    NumeralType.MILLIONS,
    NumeralType.THOUSANDS,
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)
RULE_NUMERAL_TRILLIONS = NumeralRule(
    NumeralType.TRILLIONS,
    NumeralType.BILLIONS,
    NumeralType.MILLIONS,
    NumeralType.THOUSANDS,
    NumeralType.HUNDREDS,
    NumeralType.TENS,
    NumeralType.ONES,
)

RULE_NUMERAL = NumeralRule(
    NumeralType.TRILLIONS,
    NumeralType.BILLIONS,
    NumeralType.MILLIONS,
    NumeralType.THOUSANDS,
    NumeralType.HUNDREDS,
    NumeralType.DECIMALS,
    NumeralType.TENS,
    NumeralType.ONES,
    NumeralType.INTEGERS,
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
    RULE_NUMERAL_PERFECT_HUNDREDS,
    RULE_NUMERAL_TENS_ONLY,
    RULE_NUMERAL_ONES_ONLY,
    THREE_QUARTERS,
    HALF,
    QUARTER,
    THIRD,
)
""" The order of which the expressions are evaluated. """
