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
    try:
        return int(modified_value)
    except ValueError:
        try:
            return float(modified_value)
        except ValueError:
            return value
