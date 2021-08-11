"""
Helper functions.
"""

__all__ = [
    "get_fractions_of_unit_pattern",
    "get_value_group",
    "get_unit_group",
]


import maha.rexy as rx
from maha.constants import PATTERN_SPACE

from .constants import HALF, QUARTER, THIRD, THREE_QUARTERS


def get_value_group(pattern: str):
    """Returns a group named "value" of the input ``pattern``"""
    return rx.get_named_group("value", pattern)


def get_unit_group(pattern: str):
    """Returns a group named "unit" of the input ``pattern``"""
    return rx.get_named_group("unit", pattern)


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

    return "|".join(
        [
            "{unit}{space}{three_quarter}",
            "{half}{space}{unit}",
            "{third}{space}{unit}",
            "{quarter}{space}{unit}",
        ]
    ).format(
        half=get_value_group(str(HALF)),
        third=get_value_group(str(THIRD)),
        quarter=get_value_group(str(QUARTER)),
        three_quarter=get_value_group(str(THREE_QUARTERS)),
        space=PATTERN_SPACE,
        unit=get_unit_group(unit),
    )
