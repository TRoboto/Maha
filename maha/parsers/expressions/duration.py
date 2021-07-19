"""
Expressions to extract duration.
"""

from ..templates import DurationUnit, Expression, ExpressionGroup
from .helper import (
    get_decimal_followed_by_string,
    get_number_followed_by_string,
    get_word,
    get_words_separated_by_space,
)

NAME_OF_SECONDS = "ثاني[ةه]"
NAME_OF_MINUTES = "دقيق[ةه]"
NAME_OF_HOUR = "ساع[ةه]"

THIRD = "[ثت]ل[ثت]"
QUARTER = "ربع"
HALF = "نصف?"

SUM_SUFFIX = "(ان|ين)"


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


def get_quarter_duration(text: str, output: str = "15"):
    return Expression(
        get_words_separated_by_space(QUARTER, text),
        is_confident=True,
        output=lambda x: output,
    )


def get_third_duration(text: str, output: str = "20"):
    return Expression(
        get_words_separated_by_space(THIRD, text),
        is_confident=True,
        output=lambda x: output,
    )


def get_half_duration(text: str, output: str = "30"):
    return Expression(
        get_words_separated_by_space(HALF, text),
        is_confident=True,
        output=lambda x: output,
    )


def get_three_quarters_duration(text: str, output: str = "45"):
    return ExpressionGroup(
        Expression(
            get_words_separated_by_space(text, f"[إا]لا {QUARTER}"),
            is_confident=True,
            output=lambda x: output,
        ),
        Expression(
            get_words_separated_by_space("[ثت]لا؟[ثت][ةه]؟", "[أا]رباع", "ال" + text),
            is_confident=True,
            output=lambda x: output,
        ),
    )


def get_duration_and_quarter(text: str, output: str):
    return Expression(
        get_words_separated_by_space(text, QUARTER),
        is_confident=True,
        output=lambda x: output,
    )


def get_duration_and_third(text: str, output: str):
    return Expression(
        get_words_separated_by_space(text, THIRD),
        is_confident=True,
        output=lambda x: output,
    )


def get_duration_and_half(text: str, output: str):
    return Expression(
        get_words_separated_by_space(text, HALF),
        is_confident=True,
        output=lambda x: output,
    )


EXPRESSION_DURATION_SECONDS = ExpressionGroup(
    get_number_followed_by_duration(f"(?:ثواني|{NAME_OF_SECONDS})"),
    get_decimal_followed_by_duration(f"(?:ثواني|{NAME_OF_SECONDS})"),
    get_three_quarters_duration(NAME_OF_SECONDS, "0.75"),
    get_duration_and_quarter(NAME_OF_SECONDS, "1.25"),
    get_duration_and_third(NAME_OF_SECONDS, "1.33"),
    get_duration_and_half(NAME_OF_SECONDS, "1.5"),
    get_quarter_duration(NAME_OF_SECONDS, "0.25"),
    get_third_duration(NAME_OF_SECONDS, "0.33"),
    get_half_duration(NAME_OF_SECONDS, "0.5"),
    Expression(get_word("ثانيت" + SUM_SUFFIX), is_confident=True, output=lambda x: "2"),
    Expression(
        get_word("لح[زضظ]ت" + SUM_SUFFIX), is_confident=True, output=lambda x: "2"
    ),
    Expression(get_word(NAME_OF_SECONDS), output=lambda x: "1"),
    Expression(get_word("لح[زضظ]"), output=lambda x: "1"),
    smart=True,
).set_unit(DurationUnit.SECONDS)
