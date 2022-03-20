from __future__ import annotations

__all__ = ["convert_between_durations"]

from maha.parsers.templates import DurationUnit

from ..common import ValueUnit

DURATION_CONVERSION_MAP: dict[DurationUnit, dict[DurationUnit, float]] = {
    DurationUnit.SECONDS: {
        DurationUnit.SECONDS: 1,
        DurationUnit.MINUTES: 60,
        DurationUnit.HOURS: 60 * 60,
        DurationUnit.DAYS: 60 * 60 * 24,
        DurationUnit.WEEKS: 60 * 60 * 24 * 7,
        DurationUnit.MONTHS: 60 * 60 * 24 * 30,
        DurationUnit.YEARS: 60 * 60 * 24 * 365,
    },
    DurationUnit.MINUTES: {
        DurationUnit.SECONDS: 1 / 60,
        DurationUnit.MINUTES: 1,
        DurationUnit.HOURS: 60,
        DurationUnit.DAYS: 60 * 24,
        DurationUnit.WEEKS: 60 * 24 * 7,
        DurationUnit.MONTHS: 60 * 24 * 30,
        DurationUnit.YEARS: 60 * 24 * 365,
    },
    DurationUnit.HOURS: {
        DurationUnit.SECONDS: 1 / (60 * 60),
        DurationUnit.MINUTES: 1 / 60,
        DurationUnit.HOURS: 1,
        DurationUnit.DAYS: 24,
        DurationUnit.WEEKS: 24 * 7,
        DurationUnit.MONTHS: 24 * 30,
        DurationUnit.YEARS: 24 * 365,
    },
    DurationUnit.DAYS: {
        DurationUnit.SECONDS: 1 / (60 * 60 * 24),
        DurationUnit.MINUTES: 1 / (60 * 24),
        DurationUnit.HOURS: 1 / 24,
        DurationUnit.DAYS: 1,
        DurationUnit.WEEKS: 7,
        DurationUnit.MONTHS: 30,
        DurationUnit.YEARS: 365,
    },
    DurationUnit.WEEKS: {
        DurationUnit.SECONDS: 1 / (60 * 60 * 24 * 7),
        DurationUnit.MINUTES: 1 / (60 * 24 * 7),
        DurationUnit.HOURS: 1 / (24 * 7),
        DurationUnit.DAYS: 1 / 7,
        DurationUnit.WEEKS: 1,
        DurationUnit.MONTHS: 4,
        DurationUnit.YEARS: 48,
    },
    DurationUnit.MONTHS: {
        DurationUnit.SECONDS: 1 / (60 * 60 * 24 * 30),
        DurationUnit.MINUTES: 1 / (60 * 24 * 30),
        DurationUnit.HOURS: 1 / (24 * 30),
        DurationUnit.DAYS: 1 / 30,
        DurationUnit.WEEKS: 1 / 4,
        DurationUnit.MONTHS: 1,
        DurationUnit.YEARS: 12,
    },
    DurationUnit.YEARS: {
        DurationUnit.SECONDS: 1 / (60 * 60 * 24 * 365),
        DurationUnit.MINUTES: 1 / (60 * 24 * 365),
        DurationUnit.HOURS: 1 / (24 * 365),
        DurationUnit.DAYS: 1 / 365,
        DurationUnit.WEEKS: 1 / 48,
        DurationUnit.MONTHS: 1 / 12,
        DurationUnit.YEARS: 1,
    },
}


def convert_between_durations(
    *durations: ValueUnit, to_unit: DurationUnit
) -> ValueUnit:
    """
    Converts a list of durations to another unit using the mapping
    :data:`~.DURATION_CONVERSION_MAP`.

    Parameters
    ----------
    *durations:
        List of durations to convert.
    to_unit:
        The unit to convert to.

    Returns
    -------
    float
        The converted value.
    """

    table = DURATION_CONVERSION_MAP[to_unit]
    output_value = 0.0
    for duration in durations:
        assert isinstance(duration.unit, DurationUnit)
        output_value += table[duration.unit] * duration.value
    if output_value.is_integer():
        output_value = int(output_value)
    return ValueUnit(output_value, to_unit)
