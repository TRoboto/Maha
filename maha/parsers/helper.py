"""
Helper functions.
"""
from typing import Union

from maha.constants import (
    ARABIC_COMMA,
    ARABIC_DECIMAL_SEPARATOR,
    ARABIC_THOUSANDS_SEPARATOR,
    COMMA,
    DOT,
    EMPTY,
    PERCENT_SIGN,
    SPACE,
)


def get_non_capturing_group(*words: str):
    """
    Returns a non capturing groups of words without word boundaries.
    """
    return "(?:{})".format("|".join(words))


def convert_to_number_if_possible(value: str) -> Union[str, int, float]:
    """
    Converts the given value to number if possible.

    Parameters
    ----------
    value: str
        The value to convert.

    Returns
    -------
    Union[str, int, float]
        The converted value.
    """
    # Replace arabic decimals with dot.
    modified_value = value.replace(ARABIC_DECIMAL_SEPARATOR, DOT)
    # Remove arabic thousands separator and commas if any.
    for separator in (ARABIC_THOUSANDS_SEPARATOR, COMMA, ARABIC_COMMA, SPACE):
        modified_value = modified_value.replace(separator, EMPTY)

    multiplier = 1
    if PERCENT_SIGN in modified_value:
        modified_value = modified_value.replace(PERCENT_SIGN, EMPTY)
        multiplier = 0.01
    try:
        return int(modified_value) * multiplier
    except ValueError:
        try:
            return round(float(modified_value) * multiplier, 10)
        except ValueError:
            return value
