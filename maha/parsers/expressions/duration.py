"""
Expressions to extract duration.
"""
from maha.constants import ALEF_VARIATIONS

from ..templates import DurationUnit, Expression, ExpressionGroup
from ..utils.duration import (
    convert_between_durations,
    get_words_separated_by_waw,
    merge_two_durations,
)
from ..utils.general import (
    get_decimal_followed_by_string,
    get_integer_followed_by_string,
    get_non_capturing_group,
    get_word_with_optional_waw_prefix,
    get_words_separated_by_space_and_optional_waw_prefix,
)

TWO_SUFFIX = get_non_capturing_group("ين", "ان")
SUM_SUFFIX = get_non_capturing_group("ين", "ون")

NAME_OF_SECOND = get_non_capturing_group("ثاني[ةه]", "لح[زضظ]")
NAME_OF_TWO_SECONDS = get_non_capturing_group(
    "ثانيت" + TWO_SUFFIX, "لح[زضظ]ت" + TWO_SUFFIX
)
NAME_OF_SECONDS = get_non_capturing_group("ثواني", "لح[زضظ]ات")
NAME_OF_MINUTE = "دقيق[ةه]"
NAME_OF_TWO_MINUTES = "دقيقت" + TWO_SUFFIX
NAME_OF_MINUTES = "دقا[يئ]ق"
NAME_OF_HOUR = "ساع[ةه]"
NAME_OF_TWO_HOURS = "ساعت" + TWO_SUFFIX
NAME_OF_HOURS = "ساعات"
NAME_OF_DAY = "يوم"
NAME_OF_TWO_DAYS = NAME_OF_DAY + TWO_SUFFIX
NAME_OF_DAYS = get_non_capturing_group("[اأ]يام", NAME_OF_DAY + "ا?")
NAME_OF_WEEK = "[اأ]سبوع"
NAME_OF_TWO_WEEKS = NAME_OF_WEEK + TWO_SUFFIX
NAME_OF_WEEKS = "[{}]سابيع".format("".join(ALEF_VARIATIONS))
NAME_OF_MONTH = "شهر"
NAME_OF_TWO_MONTHS = NAME_OF_MONTH + TWO_SUFFIX
NAME_OF_MONTHS = get_non_capturing_group("شهور", "[أا]شهر")
NAME_OF_YEAR = get_non_capturing_group("سن[ةه]", "عام")
NAME_OF_TWO_YEARS = get_non_capturing_group("سنت" + TWO_SUFFIX, "عام" + TWO_SUFFIX)
NAME_OF_YEARS = get_non_capturing_group("سنوات", "سنين", "[أا]عوام")

THIRD = "[ثت]ل[ثت]"
QUARTER = "ربع"
HALF = "نصف?"


def get_number_followed_by_duration(text: str):
    return Expression(
        get_integer_followed_by_string(text),
        is_confident=True,
    )


def get_decimal_followed_by_duration(text: str):
    return Expression(
        get_decimal_followed_by_string(text),
        is_confident=True,
    )


def get_quarter_duration(text: str, output: float = 15):
    return Expression(
        get_words_separated_by_space_and_optional_waw_prefix(QUARTER, text),
        is_confident=True,
        output=output,
    )


def get_third_duration(text: str, output: float = 20):
    return Expression(
        get_words_separated_by_space_and_optional_waw_prefix(THIRD, text),
        is_confident=True,
        output=output,
    )


def get_half_duration(text: str, output: float = 30):
    return Expression(
        get_words_separated_by_space_and_optional_waw_prefix(HALF, text),
        is_confident=True,
        output=output,
    )


def get_three_quarters_duration(text: str, output: float = 45):
    return ExpressionGroup(
        Expression(
            get_words_separated_by_space_and_optional_waw_prefix(
                text, f"[إا]لا {QUARTER}"
            ),
            is_confident=True,
            output=output,
        ),
        Expression(
            get_words_separated_by_space_and_optional_waw_prefix(
                "[ثت]لا؟[ثت][ةه]؟", "[أا]رباع", "ال" + text
            ),
            is_confident=True,
            output=output,
        ),
    )


def get_duration_and_quarter(text: str, output: float):
    return Expression(
        get_words_separated_by_waw(text, QUARTER),
        is_confident=True,
        output=output,
    )


def get_duration_and_third(text: str, output: float):
    return Expression(
        get_words_separated_by_waw(text, THIRD),
        is_confident=True,
        output=output,
    )


def get_duration_and_half(text: str, output: float):
    return Expression(
        get_words_separated_by_waw(text, HALF),
        is_confident=True,
        output=output,
    )


def get_shared_expression(unit: DurationUnit):
    single = globals()[f"NAME_OF_{unit.name[:-1]}"]
    two = globals()[f"NAME_OF_TWO_{unit.name}"]
    plural = globals()[f"NAME_OF_{unit.name}"]

    exps = ExpressionGroup(
        get_decimal_followed_by_duration(get_non_capturing_group(plural, single)),
        get_number_followed_by_duration(get_non_capturing_group(plural, single)),
        smart=True,
    ).set_unit(unit)
    if unit == DurationUnit.SECONDS:
        exps += ExpressionGroup(
            get_duration_and_quarter(two, 2.25),
            get_duration_and_third(two, 2.33),
            get_duration_and_half(two, 2.5),
            get_duration_and_quarter(single, 1.25),
            get_duration_and_third(single, 1.33),
            get_duration_and_half(single, 1.5),
            get_quarter_duration(single, 0.25),
            get_third_duration(single, 0.33),
            get_half_duration(single, 0.5),
            get_three_quarters_duration(single, 0.75),
        ).set_unit(unit)
    else:
        # This is for better readability
        newunit = DurationUnit(unit.value - 1)
        to_newunit = lambda v: convert_between_durations((v, unit), to_unit=newunit)
        exps += ExpressionGroup(
            get_duration_and_quarter(two, to_newunit(2.25)),
            get_duration_and_third(two, to_newunit(2 + 1 / 3)),
            get_duration_and_half(two, to_newunit(2.5)),
            get_duration_and_quarter(single, to_newunit(1.25)),
            get_duration_and_third(single, to_newunit(1 + 1 / 3)),
            get_duration_and_half(single, to_newunit(1.5)),
            get_quarter_duration(single, to_newunit(0.25)),
            get_third_duration(single, to_newunit(1 / 3)),
            get_half_duration(single, to_newunit(0.5)),
            get_three_quarters_duration(single, to_newunit(0.75)),
        ).set_unit(newunit)

    exps += ExpressionGroup(
        Expression(
            get_word_with_optional_waw_prefix(two),
            is_confident=True,
            output=2,
        ),
        Expression(get_word_with_optional_waw_prefix(single), output=1),
    ).set_unit(unit)
    return exps


EXPRESSION_DURATION_SECONDS = get_shared_expression(DurationUnit.SECONDS)

EXPRESSION_DURATION_MINUTES = get_shared_expression(DurationUnit.MINUTES)

EXPRESSION_DURATION_HOURS = get_shared_expression(DurationUnit.HOURS)

EXPRESSION_DURATION_DAYS = get_shared_expression(DurationUnit.DAYS)

EXPRESSION_DURATION_WEEKS = get_shared_expression(DurationUnit.WEEKS)

EXPRESSION_DURATION_MONTHS = get_shared_expression(DurationUnit.MONTHS)

EXPRESSION_DURATION_YEARS = get_shared_expression(DurationUnit.YEARS)

EXPRESSION_DURATION = ExpressionGroup(
    merge_two_durations(EXPRESSION_DURATION_YEARS, EXPRESSION_DURATION_MONTHS),
    merge_two_durations(EXPRESSION_DURATION_MONTHS, EXPRESSION_DURATION_WEEKS),
    merge_two_durations(EXPRESSION_DURATION_MONTHS, EXPRESSION_DURATION_DAYS),
    merge_two_durations(EXPRESSION_DURATION_WEEKS, EXPRESSION_DURATION_DAYS),
    merge_two_durations(EXPRESSION_DURATION_DAYS, EXPRESSION_DURATION_HOURS),
    merge_two_durations(EXPRESSION_DURATION_HOURS, EXPRESSION_DURATION_MINUTES),
    merge_two_durations(EXPRESSION_DURATION_HOURS, EXPRESSION_DURATION_SECONDS),
    merge_two_durations(EXPRESSION_DURATION_MINUTES, EXPRESSION_DURATION_SECONDS),
    EXPRESSION_DURATION_YEARS,
    EXPRESSION_DURATION_MONTHS,
    EXPRESSION_DURATION_WEEKS,
    EXPRESSION_DURATION_DAYS,
    EXPRESSION_DURATION_HOURS,
    EXPRESSION_DURATION_MINUTES,
    EXPRESSION_DURATION_SECONDS,
    smart=True,
)
