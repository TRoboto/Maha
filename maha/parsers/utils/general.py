"""
Functions that return shared expressions.
"""
from typing import List, Union

from maha.constants import ARABIC_NUMBERS, ENGLISH_NUMBERS

INTEGER_EXPRESSION: str = "([{}]+)".format("".join(ARABIC_NUMBERS + ENGLISH_NUMBERS))
DECIMAL_EXPRESSION: str = "([{0}].[{0}]+)".format(
    "".join(ARABIC_NUMBERS + ENGLISH_NUMBERS)
)
SPACE_EXPRESSION: str = r"\s+"
SPACE_OR_NONE_EXPRESSION: str = r"\s*"
WAW_SEPARATOR = SPACE_EXPRESSION + "و" + SPACE_OR_NONE_EXPRESSION


def get_integer_followed_by_string(expression: str) -> str:
    return get_words_separated_by_space_and_optional_waw_prefix(
        INTEGER_EXPRESSION, expression
    )


def get_decimal_followed_by_string(expression: str) -> str:
    return get_words_separated_by_space_and_optional_waw_prefix(
        DECIMAL_EXPRESSION, expression
    )


def get_non_capturing_group(*words: str):
    """
    Returns a non capturing groups of words without word boundaries.
    """
    return "(?:{})".format("|".join(words))


def get_words_separated_by_space(*words: str):
    """
    Returns a regex that matches words separated by spaces.
    """
    return get_word(SPACE_EXPRESSION.join(words))


def get_words_separated_by_space_and_optional_waw_prefix(*words: str):
    """
    Returns a regex that matches words separated by spaces and optional waw prefix.
    """
    return get_words_separated_by_space("و?" + words[0], *words[1:])


def get_words_separated_by_waw(*words: str):
    """
    Returns a regex that matches words separated by waw.
    """
    return get_word(WAW_SEPARATOR.join(words))


def get_word(word: str) -> str:
    """
    Returns a regex that matches a complete word.
    """
    return r"\b{}\b".format(word)


def get_word_with_optional_waw_prefix(word: str):
    """
    Returns a regex that matches a complete word with optional waw prefix.
    """
    return get_word("و?" + word)


def convert_to_number_if_possible(values: List[str]) -> List[Union[str, int, float]]:
    """
    Converts the given values to numbers if possible.

    Parameters
    ----------
    values: List[str]
        The values to convert.

    Returns
    -------W
    List[Union[str, int, float]]
        The converted values.
    """
    output = []
    for value in values:
        try:
            output.append(int(value))
        except ValueError:
            try:
                output.append(float(value))
            except ValueError:
                output.append(value)
    return output
