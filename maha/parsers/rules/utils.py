__all__ = ["get_unit_pattern"]

from maha.expressions import EXPRESSION_SPACE
from maha.parsers.helper import (
    get_fractions_of_unit_pattern,
    get_unit_group,
    get_value_group,
)
from maha.parsers.templates import Rule
from maha.rexy import non_capturing_group


def get_unit_pattern(singular: Rule, dual: Rule, plural: Rule) -> str:
    """
    Returns the regex pattern that matches a numeric followed by a unit.

    Parameters
    ----------
    singular:
        The singular form of the unit.
    dual:
        The dual form of the unit.
    plural:
        The plural form of the unit.
    """
    pattern = non_capturing_group(
        *[
            "{numeral}{space}{unit_single_plural}",
            get_fractions_of_unit_pattern(singular.pattern),
            get_fractions_of_unit_pattern(dual.pattern),
            "{val}{unit_dual}",
            "{val}{unit_single}",
        ]
    ).format(
        numeral=Rule.get("numeral").expression,
        space=EXPRESSION_SPACE,
        unit_single_plural=get_unit_group("|".join([singular.pattern, plural.pattern])),
        unit_single=get_unit_group(singular.pattern),
        unit_dual=get_unit_group(dual.pattern),
        val=get_value_group(""),
    )
    return pattern
