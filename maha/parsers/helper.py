"""
Helper functions.
"""
from typing import Union


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
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value
