"""
Functions that operate on a string and remove all but certain characters.
"""
from __future__ import annotations

__all__ = [
    "keep",
    "keep_strings",
    "keep_arabic_letters",
    "keep_arabic_characters",
    "keep_arabic_with_english_numbers",
    "keep_arabic_letters_with_harakat",
]

import maha.cleaners.functions as functions
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
    custom_strings: list[str] | str | None = None,
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
        False to not replace with space, check :func:`~.keep_strings`
        for more information, by default True
    custom_strings : List[str], optional
        Include any other string(s), by default None

    Returns
    -------
    str
        Processed text

    Raises
    ------
    ValueError
        If no argument is set to True

    Example
    -------

    .. code:: pycon

        >>> from maha.cleaners.functions import keep
        >>> text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
        >>> keep(text, arabic_letters=True)
        'بسم الله الرحمن الرحيم'
    """

    if not text:
        return EMPTY

    custom_strings = custom_strings or []

    # current function arguments
    current_arguments = locals()
    constants = globals()
    # characters to keep
    chars_to_keep = []

    if isinstance(custom_strings, str):
        custom_strings = [custom_strings]
    chars_to_keep.extend(list(custom_strings))

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

    return keep_strings(text, chars_to_keep, use_space)


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

    Example
    -------

    .. code:: pycon

        >>> from maha.cleaners.functions import keep_arabic_letters
        >>> text = " 1 يا أحلى mathematicians في العالم"
        >>> keep_arabic_letters(text)
        'يا أحلى في العالم'
    """
    return keep_strings(text, ARABIC_LETTERS)


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

    Example
    -------

    .. code:: pycon

        >>> from maha.cleaners.functions import keep_arabic_characters
        >>> text = "أَلمَانِيَا (بالألمانية: Deutschland) رسمِيّاً جُمهُورِيَّة أَلمَانِيَا الاِتِّحَاديَّة"
        >>> keep_arabic_characters(text)
        'أَلمَانِيَا بالألمانية رسمِيّاً جُمهُورِيَّة أَلمَانِيَا الاِتِّحَاديَّة'
    """
    return keep_strings(text, ARABIC)


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

    Example
    -------

    .. code:: pycon

        >>> from maha.cleaners.functions import keep_arabic_with_english_numbers
        >>> text = "تتكون من 16 ولاية تُغطي مساحة 357,021 كيلومتر Deutschland"
        >>> keep_arabic_with_english_numbers(text)
        'تتكون من 16 ولاية تُغطي مساحة 357 021 كيلومتر'
    """
    return keep_strings(text, ARABIC + ENGLISH_NUMBERS)


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

    Example
    -------

    .. code:: pycon

        >>> from maha.cleaners.functions import keep_arabic_letters_with_harakat
        >>> text = "إنّ في التّركِ قوة…"
        >>> keep_arabic_letters_with_harakat(text)
        'إنّ في التّركِ قوة'
    """
    return keep_strings(text, ARABIC_LETTERS + HARAKAT)


def keep_strings(text: str, strings: list[str] | str, use_space: bool = True) -> str:

    """Keeps only the input strings ``strings`` in the given text ``text``

    By default, this works by replacing all strings except the input ``strings`` with
    a space, which means space is kept. This is to help separate texts when unwanted
    strings are present without spaces. For example, 'end.start' will be converted to
    'end start' if English letters :data:`~.ENGLISH_LETTERS` are passed to ``strings``.
    To disable this behavior, set ``use_space`` to False.

    .. note::
        Extra spaces (more than one space) are removed by default if ``use_space`` is
        set to True.

    Parameters
    ----------
    text : str
        Text to be processed
    strings : Union[List[str], str]
        list of strings to keep
    use_space :
        False to not replace with space, defaults to True

    Returns
    -------
    str
        Text that contains only the input strings.

    Raises
    ------
    ValueError
        If no ``strings`` are provided

    Example
    -------

    .. code:: pycon

        >>> from maha.cleaners.functions import keep_strings
        >>> text = "لا حول ولا قوة إلا بالله"
        >>> keep_strings(text, "الله")
        'الله'
    """

    if not strings:
        raise ValueError("'strings' cannot be empty.")

    # convert str to list
    if isinstance(strings, str):
        strings = [strings]

    if use_space:
        # remove all not included harakat first or tatweel
        # (to fix extra spacing between characters)
        not_included_harakat = [h for h in ALL_HARAKAT + [TATWEEL] if h not in strings]

        output_text = text
        # replace harakat with empty character
        if not_included_harakat:
            output_text = functions.replace(text, not_included_harakat, EMPTY)

        output_text = functions.replace_except(output_text, strings, SPACE)
        output_text = functions.remove_extra_spaces(output_text)
    else:
        output_text = functions.replace_except(text, strings, EMPTY)

    return output_text.strip()
