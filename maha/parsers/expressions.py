""" Module for expressions used across the parsers. """

__all__ = [
    "THIRD",
    "QUARTER",
    "HALF",
    "THREE_QUARTERS",
    "WAW_CONNECTOR",
    "WORD_SEPARATOR",
    "ALL_ALEF",
    "TWO_SUFFIX",
    "SUM_SUFFIX",
    "EXPRESSION_START",
    "EXPRESSION_END",
]

from maha.constants import ALEF_VARIATIONS, ARABIC_COMMA, COMMA, LAM, WAW
from maha.expressions import EXPRESSION_SPACE, EXPRESSION_SPACE_OR_NONE
from maha.parsers.templates import ValueExpression
from maha.rexy import (
    Expression,
    non_capturing_group,
    positive_lookahead,
    positive_lookbehind,
)

THIRD = ValueExpression(1 / 3, "[ثت]ل[ثت]")
""" Pattern that matches the pronunciation of third in Arabic """
QUARTER = ValueExpression(1 / 4, "ربع")
""" Pattern that matches the pronunciation of quarter in Arabic """
HALF = ValueExpression(1 / 2, "نصف?")
""" Pattern that matches the pronunciation of half in Arabic """
THREE_QUARTERS = ValueExpression(3 / 4, f"[إا]لا {QUARTER}")
""" Pattern that matches the pronunciation of three quarters in Arabic """
WAW_CONNECTOR = Expression(EXPRESSION_SPACE + WAW + EXPRESSION_SPACE_OR_NONE)
""" Pattern that matches WAW as a connector between two words """
WORD_SEPARATOR = Expression(
    non_capturing_group(
        f"{EXPRESSION_SPACE_OR_NONE}{non_capturing_group(COMMA, ARABIC_COMMA)}"
        f"(?:{EXPRESSION_SPACE}{WAW})?",
        f"{EXPRESSION_SPACE}{WAW}",
    )
    + non_capturing_group(r"\b", str(EXPRESSION_SPACE_OR_NONE))
)
""" Pattern that matches the word separator between numerals in Arabic """

ALL_ALEF = Expression(f'[{"".join(ALEF_VARIATIONS)}]')
""" Pattern that matches all possible forms of the ALEF in Arabic """

TWO_SUFFIX = Expression(non_capturing_group("ين", "ان"))
""" Pattern that matches the two-suffix of words in Arabic """

SUM_SUFFIX = Expression(non_capturing_group("ين", "ون"))
""" Pattern that matches the sum-suffix of words in Arabic """

EXPRESSION_START = Expression(
    positive_lookbehind("^", r"\W", r"\b", r"\b" + WAW, r"\b" + LAM)
)
""" Pattern that matches the start of a rule expression in Arabic """

EXPRESSION_END = Expression(positive_lookahead("$", r"\W", r"\b"))
""" Pattern that matches the end of a rule expression in Arabic """
