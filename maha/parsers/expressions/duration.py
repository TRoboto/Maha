"""
Expressions to extract duration.
"""
from maha.constants import ALEF_VARIATIONS

from ..templates import DurationUnit, Expression, ExpressionGroup
from .helper import (
    get_decimal_followed_by_string,
    get_number_followed_by_string,
    get_words_separated_by_space,
)

NAME_OF_SECONDS = "ثاني[ةه]"
NAME_OF_MINUTES = "دقيق[ةه]"
NAME_OF_HOUR = "ساع[ةه]"


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
        get_words_separated_by_space("ربع", text),
        is_confident=True,
        output=lambda x: output,
    )


def get_third_duration(text: str, output: str = "20"):
    return Expression(
        get_words_separated_by_space("[ثت]ل[ثت]", text),
        is_confident=True,
        output=lambda x: output,
    )


def get_half_duration(text: str, output: str = "30"):
    return Expression(
        get_words_separated_by_space("نصف?", text),
        is_confident=True,
        output=lambda x: output,
    )


def get_three_quarters_duration(text: str, output: str = "45"):
    return ExpressionGroup(
        Expression(
            get_words_separated_by_space(text, "[إا]لا ربع"),
            is_confident=True,
            output=lambda x: output,
        ),
        Expression(
            get_words_separated_by_space("[ثت]لا؟[ثت][ةه]؟", "[أا]رباع", "ال" + text),
            is_confident=True,
            output=lambda x: output,
        ),
    )


EXPRESSION_DURATION_SECONDS = ExpressionGroup(
    get_number_followed_by_duration(f"(?:ثواني|{NAME_OF_SECONDS})"),
    get_decimal_followed_by_duration(f"(?:ثواني|{NAME_OF_SECONDS})"),
    get_quarter_duration(NAME_OF_SECONDS, "0.25"),
    get_third_duration(NAME_OF_SECONDS, "0.33"),
    get_half_duration(NAME_OF_SECONDS, "0.5"),
    get_three_quarters_duration(NAME_OF_SECONDS, "0.75"),
    smart=True,
).set_unit(DurationUnit.SECONDS)
