"""
Functions that operate on a string and remove all but certain characters.
"""

__all__ = [
    "keep",
    "keep_arabic",
    "keep_characters",
]

import re
from typing import List, Union

from ...constants import (
    ALL_HARAKAT,
    ARABIC,
    ARABIC_LETTERS,
    ARABIC_NUMBERS,
    ARABIC_PUNCTUATIONS,
    EMPTY,
    ENGLISH,
    ENGLISH_CAPITAL_LETTERS,
    ENGLISH_LETTERS,
    ENGLISH_NUMBERS,
    ENGLISH_PUNCTUATIONS,
    ENGLISH_SMALL_LETTERS,
    HARAKAT,
    NUMBERS,
    PUNCTUATIONS,
    SPACE,
)
from .remove import remove_extra_spaces


def keep(
    text: str,
    arabic: bool = False,
    english: bool = False,
    arabic_letters: bool = False,
    english_letters: bool = False,
    english_small_letters: bool = False,
    english_capital_letters: bool = False,
    numbers: bool = False,
    harakat: bool = False,
    all_harakat: bool = False,
    punctuations: bool = False,
    arabic_numbers: bool = False,
    english_numbers: bool = False,
    arabic_punctuation: bool = False,
    english_punctuation: bool = False,
    use_space: bool = True,
):
    if not text:
        raise ValueError("Text cannot be empty")

    # characters to keep
    chars_to_keep = []
    if arabic:
        chars_to_keep += ARABIC
    if english:
        chars_to_keep += ENGLISH
    if arabic_letters:
        chars_to_keep += ARABIC_LETTERS
    if harakat:
        chars_to_keep += HARAKAT
    if all_harakat:
        chars_to_keep += ALL_HARAKAT
    if english_letters:
        chars_to_keep += ENGLISH_LETTERS
    if english_small_letters:
        chars_to_keep += ENGLISH_SMALL_LETTERS
    if english_capital_letters:
        chars_to_keep += ENGLISH_CAPITAL_LETTERS
    if numbers:
        chars_to_keep += NUMBERS
    if arabic_numbers:
        chars_to_keep += ARABIC_NUMBERS
    if punctuations:
        chars_to_keep += PUNCTUATIONS
    if english_numbers:
        chars_to_keep += ENGLISH_NUMBERS
    if arabic_punctuation:
        chars_to_keep += ARABIC_PUNCTUATIONS
    if english_punctuation:
        chars_to_keep += ENGLISH_PUNCTUATIONS

    if not chars_to_keep:
        raise ValueError("At least one argument should be True")

    # remove duplicates
    chars_to_keep = list(set(chars_to_keep))

    return keep_characters(text, chars_to_keep, use_space)


def keep_arabic(text: str) -> str:
    """Keeps Arabic characters :const:`~constants.arabic.compound.ARABIC_CHARS` only.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text contains Arabic characters only.
    """
    return keep_characters(text, ARABIC_LETTERS)


def keep_characters(
    text: str, chars: Union[List[str], str], use_space: bool = True
) -> str:

    """Keeps only the input characters ``chars`` in the given text ``text``

    This works by replacing all characters except the input ``chars`` with a space,
    which means space is kept. This is to help separate texts when unwanted characters
    are present without spaces such as 'end.start', which will be converted to
    'end start' if English characters are to be kept.

    Parameters
    ----------
    text : str
        Text to be processed
    chars : Union[List[str], str]
        list of characters to keep
    use_space :
        False to not replace with space, defaults to True

    Returns
    -------
    str
        Text that contains only the input characters.

    Raises
    ------
    ValueError
        When ``chars`` is empty
    """

    if not chars:
        raise ValueError("'chars' cannot be empty.")

    # convert list to str
    chars = "".join(chars)
    chars = re.escape(chars)

    if use_space:
        # remove space character if included
        chars = chars.replace(SPACE, EMPTY)
        # remove all not included harakat first
        # (to fix extra spacing between characters)
        not_included_harakat = "".join([h for h in ALL_HARAKAT if h not in chars])
        output_text = re.sub(f"[{not_included_harakat}]", EMPTY, text)

        output_text = re.sub(f"[^{chars}]", SPACE, output_text)
        output_text = remove_extra_spaces(output_text)
    else:
        output_text = re.sub(f"[^{chars}]", EMPTY, text)

    return output_text.strip()
