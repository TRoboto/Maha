from maha.constants import (
    ALEF_VARIATIONS,
    ARABIC_COMMA,
    COMMA,
    PATTERN_SPACE,
    PATTERN_SPACE_OR_NONE,
    WAW,
)
from maha.parsers.interfaces import Expression, ValueExpression
from maha.rexy import non_capturing_group

THIRD = ValueExpression(1 / 3, "[ثت]ل[ثت]")
""" Pattern that matches the pronunciation of third in Arabic """
QUARTER = ValueExpression(1 / 4, "ربع")
""" Pattern that matches the pronunciation of quarter in Arabic """
HALF = ValueExpression(1 / 2, "نصف?")
""" Pattern that matches the pronunciation of half in Arabic """
THREE_QUARTERS = ValueExpression(3 / 4, f"[إا]لا {QUARTER}")
""" Pattern that matches the pronunciation of three quarters in Arabic """
WAW_CONNECTOR = Expression(PATTERN_SPACE + WAW + PATTERN_SPACE_OR_NONE)
""" Pattern that matches WAW as a connector between two words """
NUMERAL_WORD_SEPARATOR = Expression(
    f"(?:{PATTERN_SPACE_OR_NONE}(?:{COMMA}|{ARABIC_COMMA}))?"
    f"(?:{PATTERN_SPACE}{WAW})?"
    f"(?:{PATTERN_SPACE_OR_NONE}|\\b)"
)
""" Pattern that matches the word separator between numerals in Arabic """

ALL_ALEF = Expression(f'[{"".join(ALEF_VARIATIONS)}]')
""" Pattern that matches all possible forms of the ALEF in Arabic """

TWO_SUFFIX = Expression(non_capturing_group("ين", "ان"))
""" Pattern that matches the two-suffix of words in Arabic """

SUM_SUFFIX = Expression(non_capturing_group("ين", "ون"))
""" Pattern that matches the sum-suffix of words in Arabic """

EXPRESSION_START = Expression(non_capturing_group("^", r"\W", r"\b"))
