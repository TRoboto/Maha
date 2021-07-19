"""
Functions that return shared expressions.
"""
from maha.constants import ARABIC_NUMBERS, ENGLISH_NUMBERS

INTEGER_EXPRESSION: str = "([{}]+)".format("".join(ARABIC_NUMBERS + ENGLISH_NUMBERS))
DECIMAL_EXPRESSION: str = "([{}].[{}]+)".format(
    "".join(ARABIC_NUMBERS + ENGLISH_NUMBERS)
)
SPACE_EXPRESSION: str = r"\s+"


def get_number_followed_by_string(expression: str) -> str:
    return get_words_separated_by_space(INTEGER_EXPRESSION, expression)


def get_decimal_followed_by_string(expression: str) -> str:
    return get_words_separated_by_space(DECIMAL_EXPRESSION, expression)


def get_words_separated_by_space(*words: str):
    """
    Returns a regex that matches words separated by spaces.
    """
    return get_word(SPACE_EXPRESSION.join(words))


def get_word(word: str) -> str:
    """
    Returns a regex that matches a complete word.
    """
    return r"\b{}\b".format(word)
