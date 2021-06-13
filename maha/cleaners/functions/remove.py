"""
Functions that operate on a string and remove certain characters.
"""

__all__ = [
    "remove",
    "remove_characters",
    "remove_extra_spaces",
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
)


def remove(
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

    """Removes certain characters from the given text.

    To add a new parameter, make sure that its name is the same as the corresponding
    constant.

    Parameters
    ----------
    text : str
        Text to be processed
    arabic : bool, optional
        Remove :data:`~.ARABIC` characters, by default False
    english : bool, optional
        Remove :data:`~.ENGLISH` characters, by default False
    arabic_letters : bool, optional
        Remove :data:`~.ARABIC_LETTERS` characters, by default False
    english_letters : bool, optional
        Remove :data:`~.ENGLISH_LETTERS` characters, by default False
    english_small_letters : bool, optional
        Remove :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
    english_capital_letters : bool, optional
        Remove :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
    numbers : bool, optional
        Remove :data:`~.NUMBERS` characters, by default False
    harakat : bool, optional
        Remove :data:`~.HARAKAT` characters, by default False
    all_harakat : bool, optional
        Remove :data:`~.ALL_HARAKAT` characters, by default False
    punctuations : bool, optional
        Remove :data:`~.PUNCTUATIONS` characters, by default False
    arabic_numbers : bool, optional
        Remove :data:`~.ARABIC_NUMBERS` characters, by default False
    english_numbers : bool, optional
        Remove :data:`~.ENGLISH_NUMBERS` characters, by default False
    arabic_punctuations : bool, optional
        Remove :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
    english_punctuations : bool, optional
        Remove :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
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
    chars_to_remove = []
    chars_to_remove.extend(list(custom_chars))

    # Since each argument has the same name as the corresponding constant.
    # Looping through all arguments and appending constants that correspond to the
    # True arguments can work
    # TODO: Maybe find a good pythonic way to do this
    for arg, value in current_arguments.items():
        const = constants.get(arg.upper())
        if const and value is True:
            chars_to_remove += const

    if not chars_to_remove:
        raise ValueError("At least one argument should be True")

    # remove duplicates
    chars_to_remove = list(set(chars_to_remove))

    return remove_characters(text, chars_to_remove, use_space)


def remove_characters(
    text: str, chars: Union[List[str], str], use_space: bool = True
) -> str:

    """Removes the input characters ``chars`` in the given text ``text``

    This works by replacing all input characters ``chars`` with a space,
    which means space cannot be removed. This is to help separate texts when unwanted
    characters are present without spaces. For example, 'end.start' will be converted
    to 'end start' if dot :data:`~.DOT` is passed to ``chars``.
    To disable this behavior, set ``use_space`` to False.

    .. note::
        Extra spaces (more than one space) are removed by default if ``use_space`` is
        set to True.

    Parameters
    ----------
    text : str
        Text to be processed
    chars : Union[List[str], str]
        list of characters to remove
    use_space :
        False to not replace with space, defaults to True

    Returns
    -------
    str
        Text with input characters removed.

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
        # remove space character if included
        chars = chars.replace(SPACE, EMPTY)
        # remove all included harakat first
        # (to fix extra spacing between characters)
        included_harakat = "".join([h for h in ALL_HARAKAT if h in chars])

        output_text = text
        # replace harakat with empty character
        if included_harakat:
            output_text = re.sub(f"[{included_harakat}]", EMPTY, text)

        output_text = re.sub(f"[{chars}]", SPACE, output_text)
        output_text = remove_extra_spaces(output_text)
    else:
        output_text = re.sub(f"[{chars}]", EMPTY, text)

    return output_text.strip()


def remove_extra_spaces(text: str, max_spaces: int = 1) -> str:
    """Keeps a maximum of ``max_spaces`` number of spaces when extra spaces are present
    (more than one space)

    Parameters
    ----------
    text : str
        Text to be processed
    max_spaces : int, optional
        Maximum number of spaces to keep, by default 1

    Returns
    -------
    str
        Text with extra spaces removed

    Raises
    ------
    ValueError
        When a negative or float value is assigned to ``max_spaces``
    """
    if max_spaces < 1:
        raise ValueError("'max_spaces' should be greater than 0")

    if max_spaces != int(max_spaces):
        raise ValueError("Cannot assign a float value to 'max_spaces'")

    return re.sub(SPACE * max_spaces + "+", SPACE * max_spaces, text)
