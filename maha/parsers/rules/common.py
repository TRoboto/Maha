__all__ = ["get_fractions_of_unit_pattern", "wrap_pattern", "spaced_patterns"]

from dataclasses import dataclass

from maha.expressions import EXPRESSION_SPACE
from maha.parsers.expressions import (
    EXPRESSION_END,
    EXPRESSION_START,
    HALF,
    QUARTER,
    THIRD,
    THREE_QUARTERS,
)
from maha.parsers.templates import Unit
from maha.rexy import Expression, ExpressionGroup, non_capturing_group


@dataclass
class ValueUnit:
    """Represents a value with unit."""

    value: float
    unit: Unit


FRACTIONS = ExpressionGroup(THREE_QUARTERS, QUARTER, HALF, THIRD)


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
        from maha.parsers.expressions import WORD_SEPARATOR

        seperator = WORD_SEPARATOR

    from maha.parsers.rules.common import wrap_pattern

    start_group = non_capturing_group(*[str(p) for p in patterns])
    pattern = wrap_pattern(
        (start_group if combine_all else patterns[0])
        + non_capturing_group(seperator + start_group)
        + "*"
    )

    return pattern
