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
    arabic_punctuations: bool = False,
    english_punctuations: bool = False,
    use_space: bool = True,
    custom_chars: List[str] = [],
):
    """Keeps only the provided characters in the given text and removes everything else.

    Parameters
    ----------
    text : str
        Text to be processed
    arabic : bool, optional
        keep :data:`~.ARABIC` characters, by default False
    english : bool, optional
        keep :data:`~.ENGLISH` characters, by default False
    arabic_letters : bool, optional
        keep :data:`~.ARABIC_LETTERS` characters, by default False
    english_letters : bool, optional
        keep :data:`~.ENGLISH_LETTERS` characters, by default False
    english_small_letters : bool, optional
        keep :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
    english_capital_letters : bool, optional
        keep :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
    numbers : bool, optional
        keep :data:`~.NUMBERS` characters, by default False
    harakat : bool, optional
        keep :data:`~.HARAKAT` characters, by default False
    all_harakat : bool, optional
        keep :data:`~.ALL_HARAKAT` characters, by default False
    punctuations : bool, optional
        keep :data:`~.PUNCTUATIONS` characters, by default False
    arabic_numbers : bool, optional
        keep :data:`~.ARABIC_NUMBERS` characters, by default False
    english_numbers : bool, optional
        keep :data:`~.ENGLISH_NUMBERS` characters, by default False
    arabic_punctuations : bool, optional
        keep :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
    english_punctuations : bool, optional
        keep :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
    use_space : bool, optional
        False to not replace with space, check :func:`~.keep_characters`
        for more information, by default True
    custom_chars : List[str], optional
        Include any other unicode character, by default empty list ``[]``

    Returns
    -------
    str
        Processed text

    Raises
    ------
    ValueError
        When input text is empty or no argument is set to True
    """

    if not text:
        raise ValueError("Text cannot be empty")

    # current function arguments
    current_arguments = locals()

    # characters to keep
    chars_to_keep = custom_chars

    # Since each argument has the same name as the corresponding constant.
    # Looping through all arguments and appending constants that correspond to the
    # True arguments can work
    # TODO: Maybe find a good pythonic way to do this
    for arg, value in current_arguments.items():
        const = globals().get(arg.upper())
        if const and value is True:
            chars_to_keep += const

    if not chars_to_keep:
        raise ValueError("At least one argument should be True")

    # remove duplicates
    chars_to_keep = list(set(chars_to_keep))

    return keep_characters(text, chars_to_keep, use_space)


def keep_arabic(text: str) -> str:
    """Keeps Arabic characters :data:`~.ARABIC_LETTERS` only.

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
