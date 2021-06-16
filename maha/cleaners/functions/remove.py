"""
Functions that operate on a string and remove certain characters.
"""

__all__ = [
    "remove",
    "remove_characters",
    "remove_extra_spaces",
    "remove_punctuations",
    "remove_english",
    "remove_all_harakat",
    "remove_harakat",
    "remove_numbers",
    "remove_patterns",
]

from typing import List, Union

# To enjoy infinite width lookbehind
import regex as re

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
    PATTERN_ARABIC_HASHTAGS,
    PATTERN_ARABIC_MENTIONS,
    PATTERN_EMAILS,
    PATTERN_ENGLISH_HASHTAGS,
    PATTERN_ENGLISH_MENTIONS,
    PATTERN_HASHTAGS,
    PATTERN_LINKS,
    PATTERN_MENTIONS,
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
    arabic_hashtags: bool = False,
    arabic_mentions: bool = False,
    emails: bool = False,
    english_hashtags: bool = False,
    english_mentions: bool = False,
    hashtags: bool = False,
    links: bool = False,
    mentions: bool = False,
    use_space: bool = True,
    custom_chars: Union[List[str], str] = [],
    custom_patterns: List[str] = [],
):

    """Removes certain characters from the given text.

    To add a new parameter, make sure that its name is the same as the corresponding
    constant. For the patterns, only remove the prefix PATTERN_ from the parameter name

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
    arabic_hashtags : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_ARABIC_HASHTAGS`,
        by default False
    arabic_mentions : bool, optional
        Remove Arabic mentions using the pattern :data:`~.PATTERN_ARABIC_MENTIONS`,
        by default False
    emails : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_EMAILS`,
        by default False
    english_hashtags : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_ENGLISH_HASHTAGS`,
        by default False
    english_mentions : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_ENGLISH_MENTIONS`,
        by default False
    hashtags : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_HASHTAGS`,
        by default False
    links : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_LINKS`,
        by default False
    mentions : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_MENTIONS`,
        by default False
    use_space : bool, optional
        False to not replace with space, check :func:`~.remove_characters`
        for more information, by default True
    custom_chars : Union[List[str], str], optional
        Include any other unicode character, by default empty list ``[]``
    custom_patterns : List[str], optional
        Include any other regular expression patterns, by default empty list ``[]``

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

    # characters to remove
    chars_to_remove = []
    chars_to_remove.extend(list(custom_chars))
    # patterns to remove
    patterns_to_remove = []
    patterns_to_remove.extend(custom_patterns)

    #
    # Since each argument has the same name as the corresponding constant
    # (But, patterns should be prefixed with "PATTERN_" to match the actual pattern.)
    # Looping through all arguments and appending constants that correspond to the
    # True arguments can work
    # TODO: Maybe find a good pythonic way to do this
    for arg, value in current_arguments.items():
        const = constants.get(arg.upper())
        if const and value is True:
            chars_to_remove += const
            continue
        # check for pattern
        pattern = constants.get("PATTERN_" + arg.upper())
        if pattern and value is True:
            patterns_to_remove.append(pattern)

    if not (chars_to_remove or patterns_to_remove):
        raise ValueError("At least one argument should be True")

    output = text
    # remove using patterns
    if patterns_to_remove:
        output = remove_patterns(output, patterns_to_remove)
    # remove duplicates
    if chars_to_remove:
        chars_to_remove = list(set(chars_to_remove))
        output = remove_characters(output, chars_to_remove, use_space)
    return output


def remove_hash_keep_tag(text: str):
    pass


def remove_hashtags_at_end(text: str):
    pass


def remove_emails(text: str) -> str:
    """Removes emails using pattern :data:`~.PATTERN_EMAILS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with emails removed.
    """
    return remove_patterns(text, PATTERN_EMAILS)


def remove_hashtags(text: str) -> str:
    """Removes hashtags (strings that start with # symbol) using pattern
    :data:`~.PATTERN_HASHTAGS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with hashtags removed.
    """
    return remove_patterns(text, PATTERN_HASHTAGS)


def remove_links(text: str) -> str:
    """Removes links using pattern :data:`~.PATTERN_LINKS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with links removed.
    """
    return remove_patterns(text, PATTERN_LINKS)


def remove_mentions(text: str) -> str:
    """Removes mentions (strings that start with @ symbol) using pattern
    :data:`~.PATTERN_MENTIONS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with mentions removed.
    """
    return remove_patterns(text, PATTERN_MENTIONS)


def remove_punctuations(text: str) -> str:
    """Removes all punctuations :data:`~.PUNCTUATIONS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with punctuations removed.
    """
    return remove_characters(text, PUNCTUATIONS)


def remove_english(text: str) -> str:
    """Removes all english characters :data:`~.ENGLISH` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with english removed.
    """
    return remove_characters(text, ENGLISH)


def remove_all_harakat(text: str) -> str:
    """Removes all harakat :data:`~.ALL_HARAKAT` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with all harakat removed.
    """
    return remove_characters(text, ALL_HARAKAT)


def remove_harakat(text: str) -> str:
    """Removes common harakat :data:`~.HARAKAT` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with common harakat removed.
    """
    return remove_characters(text, HARAKAT)


def remove_numbers(text: str) -> str:
    """Removes all numbers :data:`~.NUMBERS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with numbers removed.
    """
    return remove_characters(text, NUMBERS)


def remove_patterns(
    text: str, patterns: Union[List[str], str], remove_spaces: bool = True
) -> str:
    """Removes matched characters from the given text ``text`` using input
    patterns ``patterns``

    .. note::
        Use lookahead/lookbehind when substrings should not be captured or removed.

    Parameters
    ----------
    text : str
        Text to process
    patterns : Union[List[str], str]
        Pattern(s) to use
    remove_spaces : bool, optional
        False to keep extra spaces, defaults to True

    Returns
    -------
    str
        Text with matched characters removed.

    Raises
    ------
    ValueError
        If no ``chars`` are provided
    """

    if not patterns:
        raise ValueError("'chars' cannot be empty.")

    # convert list to str
    patterns = "|".join(patterns)

    output_text = re.sub(patterns, EMPTY, text)

    if remove_spaces:
        output_text = remove_extra_spaces(output_text)

    return output_text.strip()


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
