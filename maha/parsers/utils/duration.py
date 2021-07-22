from typing import Tuple

from ..templates import DurationUnit, Expression, ExpressionGroup
from .general import get_words_separated_by_waw

DURATION_CONVERSION_MAP = {
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
    *durations: Tuple[float, DurationUnit], to_unit: DurationUnit
) -> float:
    """
    Converts a list of durations to another unit using the mapping
    :data:`~.DURATION_CONVERSION_MAP`.

    Parameters
    ----------
    *durations: List[Tuple[float, DurationUnit]]
        List of durations to convert.
    to_unit
        The unit to convert to.

    Returns
    -------
    float
        The converted value.
    """

    table = DURATION_CONVERSION_MAP[to_unit]
    output_value = 0
    for duration in durations:
        output_value += table[duration[1]] * duration[0]
    return output_value


def merge_two_durations(
    group1: ExpressionGroup,
    group2: ExpressionGroup,
) -> ExpressionGroup:
    """
    Merge expressions from ``group1`` and ``group2``. The output pattern is constructed
    by appending all patterns from ``group2`` to all patterns in ``group1`` using the
    provided ``separator``.
    """
    result = []

    def get_output(*values: Tuple[float, DurationUnit], to_unit: DurationUnit):
        return convert_between_durations(*values, to_unit=to_unit)

    # Take the smaller unit.
    unit = DurationUnit(min(group1.get_unit().value, group2.get_unit().value))
    for exp in group1.expressions:
        for exp2 in group2.expressions:
            new_exp = Expression(
                get_words_separated_by_waw(
                    exp.pattern.strip(r"\b"), exp2.pattern.strip(r"\b")
                ),
                is_confident=exp.is_confident and exp2.is_confident,
                unit=unit,
                disable_sanity_check=True,
            )
            # If the output is None, the value is extracted from the captured group.
            # If the output is not None, it holds a number.
            # Output functions are not used with durations.
            if exp.output is None and exp2.output is None:
                new_exp.output = (
                    lambda v, u1=exp.unit, u2=exp2.unit, unit=unit: get_output(
                        (v[0], u1), (v[1], u2), to_unit=unit
                    )
                )
            elif exp2.output is None:
                new_exp.output = lambda v, exp=exp, exp2=exp2, unit=unit: get_output(
                    (exp.output, exp.unit), (v, exp2.unit), to_unit=unit
                )
            elif exp.output is None:
                new_exp.output = lambda v, exp=exp, exp2=exp2, unit=unit: get_output(
                    (v, exp.unit), (exp2.output, exp2.unit), to_unit=unit
                )
            else:
                new_exp.output = lambda v, exp=exp, exp2=exp2, unit=unit: get_output(
                    (exp.output, exp.unit), (exp2.output, exp2.unit), to_unit=unit
                )
            result.append(new_exp)

    return ExpressionGroup(
        *result,
        confident_first=group1.confident_first and group2.confident_first,
        smart=group1.smart and group2.smart,
    )
