__all__ = [
    "get_fractions_of_unit_pattern",
    "wrap_pattern",
    "spaced_patterns",
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

from dataclasses import dataclass

from maha.constants import ALEF_VARIATIONS, ARABIC_COMMA, COMMA, LAM, WAW
from maha.expressions import EXPRESSION_SPACE, EXPRESSION_SPACE_OR_NONE
from maha.parsers.templates import Unit, Value
from maha.rexy import (
    Expression,
    ExpressionGroup,
    non_capturing_group,
    positive_lookahead,
    positive_lookbehind,
)

THIRD = Value(1 / 3, "[ثت]ل[ثت]")
""" Pattern that matches the pronunciation of third in Arabic """
QUARTER = Value(1 / 4, "ربع")
""" Pattern that matches the pronunciation of quarter in Arabic """
HALF = Value(1 / 2, "نصف?")
""" Pattern that matches the pronunciation of half in Arabic """
THREE_QUARTERS = Value(3 / 4, f"[إا]لا {QUARTER}")
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

FRACTIONS = ExpressionGroup(THREE_QUARTERS, QUARTER, HALF, THIRD)


@dataclass
class ValueUnit:
    """Represents a value with unit."""

    value: float
    unit: Unit


def get_fractions_of_unit_pattern(unit: str) -> str:
    """
    Returns the fractions of a unit pattern.

    Parameters
    ----------
    unit: str
        The unit pattern.

    Returns
    -------
    str
        Pattern for the fractions of the unit.
    """

    return non_capturing_group(
        spaced_patterns(unit, THREE_QUARTERS),
        spaced_patterns(HALF, unit),
        spaced_patterns(THIRD, unit),
        spaced_patterns(QUARTER, unit),
    )


def wrap_pattern(pattern: str) -> str:
    """Adds start and end expression to the pattern."""
    return EXPRESSION_START + pattern + EXPRESSION_END


def spaced_patterns(*patterns) -> str:
    """
    Returns a regex pattern that matches any of the given patterns,
    separated by spaces.

    Parameters
    ----------
    patterns
        The patterns to match.
    """
    return non_capturing_group(str(EXPRESSION_SPACE).join(str(p) for p in patterns))


def combine_patterns(
    *patterns: str, seperator: Expression = None, combine_all=False
) -> str:
    """
    Intelligently combine following input patterns.

    Parameters
    ----------
    patterns :
        The patterns to combine.
    seperator :
        The seperator to use. If None, the default seperator :data:`WORD_SEPARATOR`
        is used.
    combine_all :
        If True, the start matches any of the input patterns. If False, the start
        matches the first pattern only, followed by any combination of all other
        patterns including the first pattern.


    Returns
    -------
    str
        The combined pattern.
    """
    if seperator is None:
        seperator = WORD_SEPARATOR

    start_group = non_capturing_group(*[str(p) for p in patterns])
    pattern = wrap_pattern(
        (start_group if combine_all else patterns[0])
        + non_capturing_group(seperator + start_group)
        + "*"
    )

    return pattern