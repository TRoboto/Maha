__all__ = [
    "RULE_ORDINAL",
    "RULE_ORDINAL_ONES",
    "RULE_ORDINAL_TENS",
    "RULE_ORDINAL_HUNDREDS",
    "RULE_ORDINAL_THOUSANDS",
    "RULE_ORDINAL_MILLIONS",
    "RULE_ORDINAL_BILLIONS",
    "RULE_ORDINAL_TRILLIONS",
]


from maha.expressions import EXPRESSION_SPACE
from maha.parsers.expressions import WAW_CONNECTOR
from maha.parsers.rules.templates.rule import Rule
from maha.parsers.templates import DimensionType, OrdinalType
from maha.rexy import ExpressionGroup, named_group, non_capturing_group

from .expression import *
from .template import OrdinalExpression

multiplier_group = lambda v: named_group("multiplier", v)
numeral_value = lambda v: named_group("numeral_value", v)


def get_numeral_value_without_multiplier(expression: str):
    return numeral_value(expression) + multiplier_group("")


class OrdinalRule(Rule):
    """Rule to extract a numeral."""

    def __init__(self, *types: OrdinalType) -> None:
        """Returns a combined expression for the given types."""
        combined_patterns = self.combine_patterns(*types)
        expression = OrdinalExpression(combined_patterns, pickle=True)
        super().__init__(expression, DimensionType.ORDINAL)

    def get_single(self, numeral: OrdinalType) -> "Expression":
        return globals()[(f"EXPRESSION_OF_{numeral.name[:-1]}")]

    def get_dual(self, numeral: OrdinalType) -> "Expression":
        return globals()[(f"EXPRESSION_OF_TWO_{numeral.name}")]

    def get_pattern(self, numeral: OrdinalType) -> str:
        if numeral == OrdinalType.TENS:
            pattern = get_numeral_value_without_multiplier(
                EXPRESSION_ORDINAL_TENS_ONLY.join()
            )
        elif numeral == OrdinalType.ONES:
            pattern = get_numeral_value_without_multiplier(
                EXPRESSION_ORDINAL_ONES_ONLY.join()
            )
        else:
            pattern = self._get_pattern(numeral)
        return pattern

    def _get_pattern(self, numeral: OrdinalType) -> str:

        single = str(self.get_single(numeral))
        dual = str(self.get_dual(numeral))

        # order matters
        _pattern = [
            "{tens}{space}{multiplier_single_plural}",
            "{ones}{space}{multiplier_single_plural}",
            "{val}{multiplier_dual}",
            "{val}{multiplier_single}",
        ]
        # # Account for no spaces in the hundreds pattern (الثلاثمائة)
        if numeral == OrdinalType.HUNDREDS:
            _pattern.insert(
                2,
                get_numeral_value_without_multiplier(
                    EXPRESSION_ORDINAL_PERFECT_HUNDREDS.join()
                ),
            )

        pattern = non_capturing_group(*_pattern).format(
            space=EXPRESSION_SPACE,
            multiplier_single_plural=multiplier_group(single),
            multiplier_single=multiplier_group(single),
            multiplier_dual=multiplier_group(dual),
            val=numeral_value(""),
            tens=numeral_value(EXPRESSION_ORDINAL_TENS_ONLY.join()),
            ones=numeral_value(EXPRESSION_ORDINAL_ONES_ONLY.join()),
        )
        return pattern


# 1 2 3 4 5 6 7 8 9
EXPRESSION_ORDINAL_ONES_ONLY = ExpressionGroup(
    EXPRESSION_OF_ONE_ONLY,
    EXPRESSION_OF_TWO_ONLY,
    EXPRESSION_OF_THREE_ONLY,
    EXPRESSION_OF_FOUR_ONLY,
    EXPRESSION_OF_FIVE_ONLY,
    EXPRESSION_OF_SIX_ONLY,
    EXPRESSION_OF_SEVEN_ONLY,
    EXPRESSION_OF_EIGHT_ONLY,
    EXPRESSION_OF_NINE_ONLY,
)

_EXPRESSION_ORDINAL_ONES = ExpressionGroup(
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
EXPRESSION_ORDINAL_PERFECT_TENS = ExpressionGroup(
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
EXPRESSION_ORDINAL_COMBINED_TENS = Expression(
    _EXPRESSION_ORDINAL_ONES.join()
    + WAW_CONNECTOR
    + EXPRESSION_ORDINAL_PERFECT_TENS.join()
)
# 10 11 12 13 14 ... 95 96 97 98 99
EXPRESSION_ORDINAL_TENS_ONLY = ExpressionGroup(
    EXPRESSION_ORDINAL_PERFECT_TENS,
    EXPRESSION_ORDINAL_COMBINED_TENS,
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
EXPRESSION_ORDINAL_PERFECT_HUNDREDS = ExpressionGroup(
    EXPRESSION_OF_THREE_HUNDREDS,
    EXPRESSION_OF_FOUR_HUNDREDS,
    EXPRESSION_OF_FIVE_HUNDREDS,
    EXPRESSION_OF_SIX_HUNDREDS,
    EXPRESSION_OF_SEVEN_HUNDREDS,
    EXPRESSION_OF_EIGHT_HUNDREDS,
    EXPRESSION_OF_NINE_HUNDREDS,
)


RULE_ORDINAL_ONES = OrdinalRule(OrdinalType.ONES)
RULE_ORDINAL_TENS = OrdinalRule(
    OrdinalType.TENS,
    OrdinalType.ONES,
)
RULE_ORDINAL_HUNDREDS = OrdinalRule(
    OrdinalType.HUNDREDS,
    OrdinalType.TENS,
    OrdinalType.ONES,
)
RULE_ORDINAL_THOUSANDS = OrdinalRule(
    OrdinalType.THOUSANDS,
    OrdinalType.HUNDREDS,
    OrdinalType.TENS,
    OrdinalType.ONES,
)
RULE_ORDINAL_MILLIONS = OrdinalRule(
    OrdinalType.MILLIONS,
    OrdinalType.THOUSANDS,
    OrdinalType.HUNDREDS,
    OrdinalType.TENS,
    OrdinalType.ONES,
)
RULE_ORDINAL_BILLIONS = OrdinalRule(
    OrdinalType.BILLIONS,
    OrdinalType.MILLIONS,
    OrdinalType.THOUSANDS,
    OrdinalType.HUNDREDS,
    OrdinalType.TENS,
    OrdinalType.ONES,
)
RULE_ORDINAL_TRILLIONS = OrdinalRule(
    OrdinalType.TRILLIONS,
    OrdinalType.BILLIONS,
    OrdinalType.MILLIONS,
    OrdinalType.THOUSANDS,
    OrdinalType.HUNDREDS,
    OrdinalType.TENS,
    OrdinalType.ONES,
)

RULE_ORDINAL = RULE_ORDINAL_TRILLIONS


ORDERED_ORDINALS = ExpressionGroup(
    EXPRESSION_OF_TWO_HUNDREDS,
    EXPRESSION_OF_TWO_THOUSANDS,
    EXPRESSION_OF_TWO_MILLIONS,
    EXPRESSION_OF_TWO_BILLIONS,
    EXPRESSION_OF_TWO_TRILLIONS,
    EXPRESSION_OF_HUNDRED,
    EXPRESSION_OF_HUNDREDS,
    EXPRESSION_OF_THOUSAND,
    EXPRESSION_OF_MILLION,
    EXPRESSION_OF_BILLION,
    EXPRESSION_OF_TRILLION,
    EXPRESSION_ORDINAL_PERFECT_HUNDREDS,
    EXPRESSION_ORDINAL_TENS_ONLY,
    EXPRESSION_ORDINAL_ONES_ONLY,
    _EXPRESSION_ORDINAL_ONES,
)
""" The order of which the expressions are evaluated. """
