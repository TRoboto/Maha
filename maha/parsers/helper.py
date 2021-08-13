"""
Helper functions.
"""

__all__ = [
    "get_fractions_of_unit_pattern",
    "get_value_group",
    "get_unit_group",
]


from typing import Callable

import maha.rexy as rx
from maha.expressions import EXPRESSION_SPACE

from .constants import HALF, QUARTER, THIRD, THREE_QUARTERS


def get_value_group(pattern: str):
    """Returns a group named "value" of the input ``pattern``"""
    return rx.named_group("value", pattern)


def get_unit_group(pattern: str):
    """Returns a group named "unit" of the input ``pattern``"""
    return rx.named_group("unit", pattern)


def get_fractions_of_unit_pattern(
    unit: str, group_fn: Callable = get_unit_group
) -> str:
    """
    Returns the fractions of a unit pattern.

    Parameters
    ----------
    unit: str
        The unit pattern.
    group_fn: Callable
        The group function to use with unit pattern.

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
        half=get_value_group(HALF),
        third=get_value_group(THIRD),
        quarter=get_value_group(QUARTER),
        three_quarter=get_value_group(THREE_QUARTERS),
        space=EXPRESSION_SPACE,
        unit=group_fn(unit),
    )
