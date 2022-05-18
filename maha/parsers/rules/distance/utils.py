from __future__ import annotations

from maha.parsers.templates import DistanceUnit

__all__ = ["convert_between_distances"]


from ..common import ValueUnit

DISTANCE_CONVERSION_MAP: dict[DistanceUnit, dict[DistanceUnit, float]] = {
    DistanceUnit.METERS: {
        DistanceUnit.METERS: 1,
        DistanceUnit.KILOMETERS: 1000,
        DistanceUnit.DECIMETERS: 0.1,
        DistanceUnit.CENTIMETERS: 0.01,
        DistanceUnit.MILLIMETERS: 0.001,
        DistanceUnit.MILES: 1609.34,
        DistanceUnit.YARDS: 0.9144,
        DistanceUnit.FEET: 0.3048,
        DistanceUnit.INCHES: 0.0254,
    },
    DistanceUnit.KILOMETERS: {
        DistanceUnit.METERS: 0.001,
        DistanceUnit.KILOMETERS: 1,
        DistanceUnit.DECIMETERS: 0.0001,
        DistanceUnit.CENTIMETERS: 1e-05,
        DistanceUnit.MILLIMETERS: 1e-06,
        DistanceUnit.MILES: 1.60934,
        DistanceUnit.YARDS: 0.0009144,
        DistanceUnit.FEET: 0.0003048,
        DistanceUnit.INCHES: 2.54e-05,
    },
    DistanceUnit.DECIMETERS: {
        DistanceUnit.METERS: 10,
        DistanceUnit.KILOMETERS: 10000,
        DistanceUnit.DECIMETERS: 1,
        DistanceUnit.CENTIMETERS: 0.1,
        DistanceUnit.MILLIMETERS: 0.01,
        DistanceUnit.MILES: 16093.4,
        DistanceUnit.YARDS: 9.144,
        DistanceUnit.FEET: 3.048,
        DistanceUnit.INCHES: 0.254,
    },
    DistanceUnit.CENTIMETERS: {
        DistanceUnit.METERS: 100,
        DistanceUnit.KILOMETERS: 100000,
        DistanceUnit.DECIMETERS: 10,
        DistanceUnit.CENTIMETERS: 1,
        DistanceUnit.MILLIMETERS: 0.1,
        DistanceUnit.MILES: 160934,
        DistanceUnit.YARDS: 91.44,
        DistanceUnit.FEET: 30.48,
        DistanceUnit.INCHES: 2.54,
    },
    DistanceUnit.MILLIMETERS: {
        DistanceUnit.METERS: 1000,
        DistanceUnit.KILOMETERS: 1000000,
        DistanceUnit.DECIMETERS: 100,
        DistanceUnit.CENTIMETERS: 10,
        DistanceUnit.MILLIMETERS: 1,
        DistanceUnit.MILES: 1609340,
        DistanceUnit.YARDS: 914.4,
        DistanceUnit.FEET: 304.8,
        DistanceUnit.INCHES: 25.4,
    },
    DistanceUnit.MILES: {
        DistanceUnit.METERS: 0.000621371,
        DistanceUnit.KILOMETERS: 0.621371,
        DistanceUnit.DECIMETERS: 6.21371e-05,
        DistanceUnit.CENTIMETERS: 6.21371e-06,
        DistanceUnit.MILLIMETERS: 6.21371e-07,
        DistanceUnit.MILES: 1,
        DistanceUnit.YARDS: 0.000568182,
        DistanceUnit.FEET: 0.000189394,
        DistanceUnit.INCHES: 1.57828e-05,
    },
    DistanceUnit.YARDS: {
        DistanceUnit.METERS: 1.09361,
        DistanceUnit.KILOMETERS: 1093.61,
        DistanceUnit.DECIMETERS: 0.109361,
        DistanceUnit.CENTIMETERS: 0.0109361,
        DistanceUnit.MILLIMETERS: 0.00109361,
        DistanceUnit.MILES: 1760,
        DistanceUnit.YARDS: 1,
        DistanceUnit.FEET: 0.333333,
        DistanceUnit.INCHES: 0.0277778,
    },
    DistanceUnit.FEET: {
        DistanceUnit.METERS: 3.28084,
        DistanceUnit.KILOMETERS: 3280.84,
        DistanceUnit.DECIMETERS: 0.328084,
        DistanceUnit.CENTIMETERS: 0.0328084,
        DistanceUnit.MILLIMETERS: 0.00328084,
        DistanceUnit.MILES: 5280,
        DistanceUnit.YARDS: 3,
        DistanceUnit.FEET: 1,
        DistanceUnit.INCHES: 0.0833333,
    },
    DistanceUnit.INCHES: {
        DistanceUnit.METERS: 39.3701,
        DistanceUnit.KILOMETERS: 39370.1,
        DistanceUnit.DECIMETERS: 3.93701,
        DistanceUnit.CENTIMETERS: 0.393701,
        DistanceUnit.MILLIMETERS: 0.0393701,
        DistanceUnit.MILES: 63360,
        DistanceUnit.YARDS: 36,
        DistanceUnit.FEET: 12,
        DistanceUnit.INCHES: 1,
    },
}


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
