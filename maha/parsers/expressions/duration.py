"""
Expressions to extract duration.
"""

from ..templates import DurationUnit, Expression, ExpressionGroup
from .helper import (
    get_decimal_followed_by_string,
    get_non_capturing_group,
    get_number_followed_by_string,
    get_word,
    get_words_separated_by_space,
)

TWO_SUFFIX = get_non_capturing_group("ين", "ان")
SUM_SUFFIX = get_non_capturing_group("ين", "ون")

NAME_OF_SECONDS = "ثاني[ةه]"
NAME_OF_TWO_SECONDS = "ثانيت" + TWO_SUFFIX
NAME_OF_MULTI_SECONDS = "ثواني"
NAME_OF_MINUTES = "دقيق[ةه]"
NAME_OF_TWO_MINUTES = "دقيقت" + TWO_SUFFIX
NAME_OF_MULTI_MINUTES = "دقا[يئ]ق"
NAME_OF_HOUR = "ساع[ةه]"
NAME_OF_TWO_HOURS = "ساعت" + TWO_SUFFIX
NAME_OF_MULTI_HOURS = "ساعات"

THIRD = "[ثت]ل[ثت]"
QUARTER = "ربع"
HALF = "نصف?"


def get_duration_expressions():
    """
    Return a list of expressions to extract duration, where high-priority expressions
    come first.
    """
    pass


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
        get_words_separated_by_space(QUARTER, text),
        is_confident=True,
        output=output,
    )


def get_third_duration(text: str, output: float = 20):
    return Expression(
        get_words_separated_by_space(THIRD, text),
        is_confident=True,
        output=output,
    )


def get_half_duration(text: str, output: float = 30):
    return Expression(
        get_words_separated_by_space(HALF, text),
        is_confident=True,
        output=output,
    )


def get_three_quarters_duration(text: str, output: float = 45):
    return ExpressionGroup(
        Expression(
            get_words_separated_by_space(text, f"[إا]لا {QUARTER}"),
            is_confident=True,
            output=output,
        ),
        Expression(
            get_words_separated_by_space("[ثت]لا؟[ثت][ةه]؟", "[أا]رباع", "ال" + text),
            is_confident=True,
            output=output,
        ),
    )


def get_duration_and_quarter(text: str, output: float):
    return Expression(
        get_words_separated_by_space(text, QUARTER),
        is_confident=True,
        output=output,
    )


def get_duration_and_third(text: str, output: float):
    return Expression(
        get_words_separated_by_space(text, THIRD),
        is_confident=True,
        output=output,
    )


def get_duration_and_half(text: str, output: float):
    return Expression(
        get_words_separated_by_space(text, HALF),
        is_confident=True,
        output=output,
    )


EXPRESSION_DURATION_SECONDS = ExpressionGroup(
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
    get_three_quarters_duration(NAME_OF_MINUTES, 45),
    get_quarter_duration(NAME_OF_MINUTES, 15),
    get_third_duration(NAME_OF_MINUTES, 20),
    get_half_duration(NAME_OF_MINUTES, 30),
    # SECONDS
    get_duration_and_quarter(NAME_OF_TWO_SECONDS, 2.25),
    get_duration_and_third(NAME_OF_TWO_SECONDS, 2.33),
    get_duration_and_half(NAME_OF_TWO_SECONDS, 2.5),
    get_duration_and_quarter(NAME_OF_SECONDS, 1.25),
    get_duration_and_third(NAME_OF_SECONDS, 1.33),
    get_duration_and_half(NAME_OF_SECONDS, 1.5),
    get_three_quarters_duration(NAME_OF_SECONDS, 0.75),
    get_quarter_duration(NAME_OF_SECONDS, 0.25),
    get_third_duration(NAME_OF_SECONDS, 0.33),
    get_half_duration(NAME_OF_SECONDS, 0.5),
    Expression(get_word(NAME_OF_TWO_SECONDS), is_confident=True, output=2),
    Expression(get_word("لح[زضظ]ت" + TWO_SUFFIX), is_confident=True, output=2),
    Expression(get_word(NAME_OF_SECONDS), output=1),
    Expression(get_word("لح[زضظ]"), output=1),
    smart=True,
).set_unit(DurationUnit.SECONDS)


EXPRESSION_DURATION_MINUTES = ExpressionGroup(
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
    get_three_quarters_duration(NAME_OF_HOUR, 45),
    get_quarter_duration(NAME_OF_HOUR, 15),
    get_third_duration(NAME_OF_HOUR, 20),
    get_half_duration(NAME_OF_HOUR, 30),
    # MINUTES
    Expression(get_word(NAME_OF_TWO_MINUTES), is_confident=True, output=2),
    Expression(get_word(NAME_OF_MINUTES), output=1),
    smart=True,
).set_unit(DurationUnit.MINUTES)
