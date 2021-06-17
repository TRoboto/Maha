"""
Functions that operate on a string and remove all but certain characters.
"""

__all__ = [
    "keep",
    "keep_characters",
    "keep_arabic_letters",
    "keep_arabic_characters",
    "keep_arabic_with_english_numbers",
    "keep_arabic_letters_with_harakat",
]

import re
from typing import List, Union

from maha.constants import (
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
    TATWEEL,
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
    custom_chars: Union[List[str], str] = [],
):
    """Keeps only certain characters in the given text and removes everything else.

    To add a new parameter, make sure that its name is the same as the corresponding
    constant.

    Parameters
    ----------
    text : str
        Text to be processed
    arabic : bool, optional
        Keep :data:`~.ARABIC` characters, by default False
    english : bool, optional
        Keep :data:`~.ENGLISH` characters, by default False
    arabic_letters : bool, optional
        Keep :data:`~.ARABIC_LETTERS` characters, by default False
    english_letters : bool, optional
        Keep :data:`~.ENGLISH_LETTERS` characters, by default False
    english_small_letters : bool, optional
        Keep :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
    english_capital_letters : bool, optional
        Keep :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
    numbers : bool, optional
        Keep :data:`~.NUMBERS` characters, by default False
    harakat : bool, optional
        Keep :data:`~.HARAKAT` characters, by default False
    all_harakat : bool, optional
        Keep :data:`~.ALL_HARAKAT` characters, by default False
    punctuations : bool, optional
        Keep :data:`~.PUNCTUATIONS` characters, by default False
    arabic_numbers : bool, optional
        Keep :data:`~.ARABIC_NUMBERS` characters, by default False
    english_numbers : bool, optional
        Keep :data:`~.ENGLISH_NUMBERS` characters, by default False
    arabic_punctuations : bool, optional
        Keep :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
    english_punctuations : bool, optional
        Keep :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
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
        If input text is empty or no argument is set to True
    """

    if not text:
        raise ValueError("Text cannot be empty")

    # current function arguments
    current_arguments = locals()
    constants = globals()
    # characters to keep
    chars_to_keep = []
    chars_to_keep.extend(list(custom_chars))

    # Since each argument has the same name as the corresponding constant.
    # Looping through all arguments and appending constants that correspond to the
    # True arguments can work
    # TODO: Maybe find a good pythonic way to do this
    for arg, value in current_arguments.items():
        const = constants.get(arg.upper())
        if const and value is True:
            chars_to_keep += const

    if not chars_to_keep:
        raise ValueError("At least one argument should be True")

    # remove duplicates
    chars_to_keep = list(set(chars_to_keep))

    return keep_characters(text, chars_to_keep, use_space)


def keep_arabic_letters(text: str) -> str:
    """Keeps only Arabic letters :data:`~.ARABIC_LETTERS` in the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text contains Arabic letters only.
    """
    return keep_characters(text, ARABIC_LETTERS)


def keep_arabic_characters(text: str) -> str:
    """Keeps only common Arabic characters :data:`~.ARABIC` in the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text contains the common Arabic characters only.
    """
    return keep_characters(text, ARABIC)


def keep_arabic_with_english_numbers(text: str) -> str:
    """Keeps only common Arabic characters :data:`~.ARABIC` and English numbers
    :data:`~.ENGLISH_NUMBERS` in the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text contains the common Arabic characters and English numbers only.
    """
    return keep_characters(text, ARABIC + ENGLISH_NUMBERS)


def keep_arabic_letters_with_harakat(text: str) -> str:
    """Keeps only Arabic letters :data:`~.ARABIC_LETTERS` and HARAKAT :data:`~.HARAKAT`
    in the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text contains Arabic letters with harakat only.
    """
    return keep_characters(text, ARABIC_LETTERS + HARAKAT)


def keep_characters(
    text: str, chars: Union[List[str], str], use_space: bool = True
) -> str:

    """Keeps only the input characters ``chars`` in the given text ``text``

    By default, this works by replacing all characters except the input ``chars`` with a space,
    which means space is kept. This is to help separate texts when unwanted characters
    are present without spaces. For example, 'end.start' will be converted to
    'end start' if English letters :data:`~.ENGLISH_LETTERS` are passed to ``chars``.
    To disable this behavior, set ``use_space`` to False.

    .. note::
        Extra spaces (more than one space) are removed by default if ``use_space`` is
        set to True.

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
        If no ``chars`` are provided
    """

    if not chars:
        raise ValueError("'chars' cannot be empty.")

    # convert list to str
    chars = "".join(chars)
    chars = re.escape(chars)

    if use_space:
        # remove all not included harakat first or tatweel
        # (to fix extra spacing between characters)
        not_included_harakat = "".join(
            [h for h in ALL_HARAKAT + [TATWEEL] if h not in chars]
        )

        output_text = text
        # replace harakat with empty character
        if not_included_harakat:
            output_text = re.sub(f"[{not_included_harakat}]", EMPTY, text)

        output_text = re.sub(f"[^{chars}]", SPACE, output_text)
        output_text = remove_extra_spaces(output_text)
    else:
        output_text = re.sub(f"[^{chars}]", EMPTY, text)

    return output_text.strip()
