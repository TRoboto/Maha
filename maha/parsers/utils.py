from __future__ import annotations

__all__ = ["convert_to_number_if_possible"]


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


def convert_to_number_if_possible(value: str) -> int | float | None:
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

    if PERCENT_SIGN in modified_value:
        modified_value = modified_value.replace(PERCENT_SIGN, EMPTY)
        multiplier = 0.01
    else:
        multiplier = 1
    try:
        return int(modified_value) * multiplier
    except ValueError:
        try:
            return round(float(modified_value) * multiplier, 10)
        except ValueError:
            return None
