"""
Expressions to extract duration.
"""
from maha.constants import ALEF_VARIATIONS

from ..templates import DurationUnit, Expression, ExpressionGroup
from ..utils.duration import get_words_separated_by_waw, merge_two_durations
from ..utils.general import (
    get_decimal_followed_by_string,
    get_non_capturing_group,
    get_number_followed_by_string,
    get_word_with_optional_waw_prefix,
    get_words_separated_by_space_and_optional_waw_prefix,
)

TWO_SUFFIX = get_non_capturing_group("ين", "ان")
SUM_SUFFIX = get_non_capturing_group("ين", "ون")

NAME_OF_SECONDS = get_non_capturing_group("ثاني[ةه]", "لح[زضظ]")
NAME_OF_TWO_SECONDS = get_non_capturing_group(
    "ثانيت" + TWO_SUFFIX, "لح[زضظ]ت" + TWO_SUFFIX
)
NAME_OF_MULTI_SECONDS = get_non_capturing_group("ثواني", "لح[زضظ]ات")
NAME_OF_MINUTES = "دقيق[ةه]"
NAME_OF_TWO_MINUTES = "دقيقت" + TWO_SUFFIX
NAME_OF_MULTI_MINUTES = "دقا[يئ]ق"
NAME_OF_HOUR = "ساع[ةه]"
NAME_OF_TWO_HOURS = "ساعت" + TWO_SUFFIX
NAME_OF_MULTI_HOURS = "ساعات"
NAME_OF_DAY = "يوم"
NAME_OF_TWO_DAYS = NAME_OF_DAY + TWO_SUFFIX
NAME_OF_MULTI_DAYS = "[اأ]يام"
NAME_OF_WEEK = "[اأ]سبوع"
NAME_OF_TWO_WEEKS = NAME_OF_WEEK + TWO_SUFFIX
NAME_OF_MULTI_WEEKS = "[{}]سابيع".format("".join(ALEF_VARIATIONS))
NAME_OF_MONTH = "شهر"
NAME_OF_TWO_MONTHS = NAME_OF_MONTH + TWO_SUFFIX
NAME_OF_MULTI_MONTHS = get_non_capturing_group("شهور", "[أا]شهر")
NAME_OF_YEAR = get_non_capturing_group("سن[ةه]", "عام")
NAME_OF_TWO_YEARS = get_non_capturing_group("سنت" + TWO_SUFFIX, "عام" + TWO_SUFFIX)
NAME_OF_MULTI_YEARS = get_non_capturing_group("سنوات", "سنين", "[أا]عوام")

THIRD = "[ثت]ل[ثت]"
QUARTER = "ربع"
HALF = "نصف?"


def get_number_followed_by_duration(text: str):
    return Expression(
        get_number_followed_by_string(text),
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


EXPRESSION_DURATION_SECONDS = ExpressionGroup(
    # Number followed by seconds
    get_decimal_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_SECONDS, NAME_OF_SECONDS)
    ),
    get_number_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_SECONDS, NAME_OF_SECONDS)
    ),
    # MINUTES
    get_duration_and_quarter(NAME_OF_TWO_MINUTES, 135),  # 2 * 60 + 15
    get_duration_and_third(NAME_OF_TWO_MINUTES, 140),  # 2 * 60 + 20
    get_duration_and_half(NAME_OF_TWO_MINUTES, 150),  # 2 * 60 + 30
    get_duration_and_quarter(NAME_OF_MINUTES, 75),  # 60 + 15
    get_duration_and_third(NAME_OF_MINUTES, 80),  # 60 + 20
    get_duration_and_half(NAME_OF_MINUTES, 90),  # 60 + 30
    get_quarter_duration(NAME_OF_MINUTES, 15),
    get_third_duration(NAME_OF_MINUTES, 20),
    get_half_duration(NAME_OF_MINUTES, 30),
    get_three_quarters_duration(NAME_OF_MINUTES, 45),
    # SECONDS
    get_duration_and_quarter(NAME_OF_TWO_SECONDS, 2.25),
    get_duration_and_third(NAME_OF_TWO_SECONDS, 2.33),
    get_duration_and_half(NAME_OF_TWO_SECONDS, 2.5),
    get_duration_and_quarter(NAME_OF_SECONDS, 1.25),
    get_duration_and_third(NAME_OF_SECONDS, 1.33),
    get_duration_and_half(NAME_OF_SECONDS, 1.5),
    get_quarter_duration(NAME_OF_SECONDS, 0.25),
    get_third_duration(NAME_OF_SECONDS, 0.33),
    get_half_duration(NAME_OF_SECONDS, 0.5),
    get_three_quarters_duration(NAME_OF_SECONDS, 0.75),
    Expression(
        get_word_with_optional_waw_prefix(NAME_OF_TWO_SECONDS),
        is_confident=True,
        output=2,
    ),
    Expression(get_word_with_optional_waw_prefix(NAME_OF_SECONDS), output=1),
    smart=True,
).set_unit(DurationUnit.SECONDS)


EXPRESSION_DURATION_MINUTES = ExpressionGroup(
    # Number followed by minutes
    get_decimal_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_MINUTES, NAME_OF_MINUTES)
    ),
    get_number_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_MINUTES, NAME_OF_MINUTES)
    ),
    # HOURS
    get_duration_and_quarter(NAME_OF_TWO_HOURS, 135),  # 2 * 60 + 15
    get_duration_and_third(NAME_OF_TWO_HOURS, 140),  # 2 * 60 + 20
    get_duration_and_half(NAME_OF_TWO_HOURS, 150),  # 2 * 60 + 30
    get_duration_and_quarter(NAME_OF_HOUR, 75),  # 60 + 15
    get_duration_and_third(NAME_OF_HOUR, 80),  # 60 + 20
    get_duration_and_half(NAME_OF_HOUR, 90),  # 60 + 30
    get_quarter_duration(NAME_OF_HOUR, 15),
    get_third_duration(NAME_OF_HOUR, 20),
    get_half_duration(NAME_OF_HOUR, 30),
    get_three_quarters_duration(NAME_OF_HOUR, 45),
    # MINUTES
    Expression(
        get_word_with_optional_waw_prefix(NAME_OF_TWO_MINUTES),
        is_confident=True,
        output=2,
    ),
    Expression(get_word_with_optional_waw_prefix(NAME_OF_MINUTES), output=1),
    smart=True,
).set_unit(DurationUnit.MINUTES)

EXPRESSION_DURATION_HOURS = ExpressionGroup(
    # Number followed by hours
    get_decimal_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_HOURS, NAME_OF_HOUR)
    ),
    get_number_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_HOURS, NAME_OF_HOUR)
    ),
    # DAYS
    get_duration_and_quarter(NAME_OF_TWO_DAYS, 54),  # 2 * 24 + 24 / 4
    get_duration_and_third(NAME_OF_TWO_DAYS, 56),  # 2 * 24 + 24 / 3
    get_duration_and_half(NAME_OF_TWO_DAYS, 60),  # 2 * 24 + 24 / 2
    get_duration_and_quarter(NAME_OF_DAY, 30),  # 24 + 24 / 4
    get_duration_and_third(NAME_OF_DAY, 32),  # 24 + 24 / 3
    get_duration_and_half(NAME_OF_DAY, 36),  # 24 + 24 / 2
    get_quarter_duration(NAME_OF_DAY, 6),  # 24 / 4
    get_third_duration(NAME_OF_DAY, 8),  # 24 / 3
    get_half_duration(NAME_OF_DAY, 12),  # 24 / 2
    get_three_quarters_duration(NAME_OF_DAY, 18),  # 24 * 3 / 4
    # HOURS
    Expression(
        get_word_with_optional_waw_prefix(NAME_OF_TWO_HOURS),
        is_confident=True,
        output=2,
    ),
    Expression(get_word_with_optional_waw_prefix(NAME_OF_HOUR), output=1),
    smart=True,
).set_unit(DurationUnit.HOURS)


EXPRESSION_DURATION_DAYS = ExpressionGroup(
    # Number followed by days
    get_decimal_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_DAYS, NAME_OF_DAY)
    ),
    get_number_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_DAYS, NAME_OF_DAY)
    ),
    # MONTHS
    get_duration_and_quarter(NAME_OF_TWO_MONTHS, 67.5),  # 2 * 30 + 30 / 4
    get_duration_and_third(NAME_OF_TWO_MONTHS, 70),  # 2 * 30 + 30 / 3
    get_duration_and_half(NAME_OF_TWO_MONTHS, 75),  # 2 * 30 + 30 / 2
    get_duration_and_quarter(NAME_OF_MONTH, 37.5),  # 30 + 30 / 4
    get_duration_and_third(NAME_OF_MONTH, 40),  # 30 + 30 / 3
    get_duration_and_half(NAME_OF_MONTH, 45),  # 30 + 30 / 2
    get_quarter_duration(NAME_OF_MONTH, 7.5),  # 30 / 4
    get_third_duration(NAME_OF_MONTH, 10),  # 30 / 3
    get_half_duration(NAME_OF_MONTH, 15),  # 30 / 2
    get_three_quarters_duration(NAME_OF_MONTH, 22.5),  # 30 * 3 / 4
    # WEEKS
    get_duration_and_quarter(NAME_OF_TWO_WEEKS, 15.75),  # 2 * 7 + 7 / 4
    get_duration_and_third(NAME_OF_TWO_WEEKS, 16.33),  # 2 * 7 + 7 / 3
    get_duration_and_half(NAME_OF_TWO_WEEKS, 17.5),  # 2 * 7 + 7 / 2
    get_duration_and_quarter(NAME_OF_WEEK, 8.75),  # 7 + 7 / 4
    get_duration_and_third(NAME_OF_WEEK, 9.33),  # 7 + 7 / 3
    get_duration_and_half(NAME_OF_WEEK, 10.5),  # 7 + 7 / 2
    get_three_quarters_duration(NAME_OF_WEEK, 5.25),  # 7 * 3 / 4
    get_quarter_duration(NAME_OF_WEEK, 1.75),  # 7 / 4
    get_third_duration(NAME_OF_WEEK, 2.33),  # 7 / 3
    get_half_duration(NAME_OF_WEEK, 3.5),  # 7 / 2
    # DAYS
    Expression(
        get_word_with_optional_waw_prefix(NAME_OF_TWO_DAYS), is_confident=True, output=2
    ),
    Expression(get_word_with_optional_waw_prefix(NAME_OF_DAY), output=1),
    smart=True,
).set_unit(DurationUnit.DAYS)

EXPRESSION_DURATION_WEEKS = ExpressionGroup(
    # Number followed by weeks
    get_decimal_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_WEEKS, NAME_OF_WEEK)
    ),
    get_number_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_WEEKS, NAME_OF_WEEK)
    ),
    # WEEKS
    Expression(
        get_word_with_optional_waw_prefix(NAME_OF_TWO_WEEKS),
        is_confident=True,
        output=2,
    ),
    Expression(get_word_with_optional_waw_prefix(NAME_OF_WEEK), output=1),
    smart=True,
).set_unit(DurationUnit.WEEKS)


EXPRESSION_DURATION_MONTHS = ExpressionGroup(
    # Number followed by months
    get_decimal_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_MONTHS, NAME_OF_MONTH)
    ),
    get_number_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_MONTHS, NAME_OF_MONTH)
    ),
    # YEARS
    get_duration_and_quarter(NAME_OF_TWO_YEARS, 27),  # 2 * 12 + 12 / 4
    get_duration_and_third(NAME_OF_TWO_YEARS, 28),  # 2 * 12 + 12 / 3
    get_duration_and_half(NAME_OF_TWO_YEARS, 30),  # 2 * 12 + 12 / 2
    get_duration_and_quarter(NAME_OF_YEAR, 15),  # 12 + 12 / 4
    get_duration_and_third(NAME_OF_YEAR, 16),  # 12 + 12 / 3
    get_duration_and_half(NAME_OF_YEAR, 18),  # 12 + 12 / 2
    get_quarter_duration(NAME_OF_YEAR, 3),  # 12 / 4
    get_third_duration(NAME_OF_YEAR, 4),  # 12 / 3
    get_half_duration(NAME_OF_YEAR, 6),  # 12 / 2
    get_three_quarters_duration(NAME_OF_YEAR, 9),  # 12 * 3 / 4
    # MONTHS
    Expression(
        get_word_with_optional_waw_prefix(NAME_OF_TWO_MONTHS),
        is_confident=True,
        output=2,
    ),
    Expression(get_word_with_optional_waw_prefix(NAME_OF_MONTH), output=1),
    smart=True,
).set_unit(DurationUnit.MONTHS)


EXPRESSION_DURATION_YEARS = ExpressionGroup(
    # Number followed by years
    get_decimal_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_YEARS, NAME_OF_YEAR)
    ),
    get_number_followed_by_duration(
        get_non_capturing_group(NAME_OF_MULTI_YEARS, NAME_OF_YEAR)
    ),
    # YEARS
    Expression(
        get_word_with_optional_waw_prefix(NAME_OF_TWO_YEARS),
        is_confident=True,
        output=2,
    ),
    Expression(get_word_with_optional_waw_prefix(NAME_OF_YEAR), output=1),
    smart=True,
).set_unit(DurationUnit.YEARS)

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
