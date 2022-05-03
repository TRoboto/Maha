from __future__ import annotations

from maha.parsers.templates import DistanceUnit

__all__ = ["convert_between_distances"]


from ..common import ValueUnit

DISTANCE_CONVERSION_MAP: dict[DistanceUnit, dict[DistanceUnit, float]] = {}


def convert_between_distances(
    *distances: ValueUnit, to_unit: DistanceUnit
) -> ValueUnit:
    """
    Converts a list of distances to another unit using the mapping
    :data:`~.DISTANCE_CONVERSION_MAP`.

    Parameters
    ----------
    *distances:
        List of distances to convert.
    to_unit:
        The unit to convert to.

    Returns
    -------
    float
        The converted value.
    """

    table = DISTANCE_CONVERSION_MAP[to_unit]
    output_value = 0.0
    for distance in distances:
        assert isinstance(distance.unit, DistanceUnit)
        output_value += table[distance.unit] * distance.value
    if output_value.is_integer():
        output_value = int(output_value)
    return ValueUnit(output_value, to_unit)
