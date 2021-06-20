"""
Functions that operate on a string and check for values contained in it
"""

__all__ = [
    "contains",
    "contains_patterns",
    "contains_characters",
]
from typing import Dict, List, Union

import regex as re

from maha.constants import (
    ALL_HARAKAT,
    ARABIC,
    ARABIC_LETTERS,
    ARABIC_LIGATURES,
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
    PATTERN_EMOJIS,
    PATTERN_ENGLISH_HASHTAGS,
    PATTERN_ENGLISH_MENTIONS,
    PATTERN_HASHTAGS,
    PATTERN_LINKS,
    PATTERN_MENTIONS,
    PUNCTUATIONS,
    SPACE,
    TATWEEL,
)


def contains(
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
    tatweel: bool = False,
    punctuations: bool = False,
    arabic_numbers: bool = False,
    english_numbers: bool = False,
    arabic_punctuations: bool = False,
    english_punctuations: bool = False,
    arabic_ligatures: bool = False,
    arabic_hashtags: bool = False,
    arabic_mentions: bool = False,
    emails: bool = False,
    english_hashtags: bool = False,
    english_mentions: bool = False,
    hashtags: bool = False,
    links: bool = False,
    mentions: bool = False,
    emojis: bool = False,
    custom_chars: Union[List[str], str] = [],
    custom_patterns: List[str] = [],
) -> Union[Dict[str, bool], bool]:

    """Check for certain characters or patterns in the given text.

    To add a new parameter, make sure that its name is the same as the corresponding
    constant. For the patterns, only remove the prefix PATTERN_ from the parameter name

    Parameters
    ----------
    text : str
        Text to be processed
    arabic : bool, optional
        Check for :data:`~.ARABIC` characters, by default False
    english : bool, optional
        Check for :data:`~.ENGLISH` characters, by default False
    arabic_letters : bool, optional
        Check for :data:`~.ARABIC_LETTERS` characters, by default False
    english_letters : bool, optional
        Check for :data:`~.ENGLISH_LETTERS` characters, by default False
    english_small_letters : bool, optional
        Check for :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
    english_capital_letters : bool, optional
        Check for :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
    numbers : bool, optional
        Check for :data:`~.NUMBERS` characters, by default False
    harakat : bool, optional
        Check for :data:`~.HARAKAT` characters, by default False
    all_harakat : bool, optional
        Check for :data:`~.ALL_HARAKAT` characters, by default False
    tatweel : bool, optional
        Check for :data:`~.TATWEEL` character, by default False
    punctuations : bool, optional
        Check for :data:`~.PUNCTUATIONS` characters, by default False
    arabic_numbers : bool, optional
        Check for :data:`~.ARABIC_NUMBERS` characters, by default False
    english_numbers : bool, optional
        Check for :data:`~.ENGLISH_NUMBERS` characters, by default False
    arabic_punctuations : bool, optional
        Check for :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
    english_punctuations : bool, optional
        Check for :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
    arabic_ligatures : bool, optional
        Check for :data:`~.ARABIC_LIGATURES` words, by default False
    arabic_hashtags : bool, optional
        Check for Arabic hashtags using the pattern :data:`~.PATTERN_ARABIC_HASHTAGS`,
        by default False
    arabic_mentions : bool, optional
        Check for Arabic mentions using the pattern :data:`~.PATTERN_ARABIC_MENTIONS`,
        by default False
    emails : bool, optional
        Check for Arabic hashtags using the pattern :data:`~.PATTERN_EMAILS`,
        by default False
    english_hashtags : bool, optional
        Check for Arabic hashtags using the pattern :data:`~.PATTERN_ENGLISH_HASHTAGS`,
        by default False
    english_mentions : bool, optional
        Check for Arabic hashtags using the pattern :data:`~.PATTERN_ENGLISH_MENTIONS`,
        by default False
    hashtags : bool, optional
        Check for Arabic hashtags using the pattern :data:`~.PATTERN_HASHTAGS`,
        by default False
    links : bool, optional
        Check for Arabic hashtags using the pattern :data:`~.PATTERN_LINKS`,
        by default False
    mentions : bool, optional
        Check for Arabic hashtags using the pattern :data:`~.PATTERN_MENTIONS`,
        by default False
    emojis : bool, optional
        Check for emojis using the pattern :data:`~.PATTERN_EMOJIS`,
        by default False
    custom_chars : Union[List[str], str], optional
        Include any other unicode character, by default empty list ``[]``
    custom_patterns : List[str], optional
        Include any other regular expression patterns, by default empty list ``[]``

    Returns
    -------
    Union[Dict[str, bool], bool]
        * If one argument is set to True, a boolean value is returned. True if the text
        contains it, False otherwise.
        * If more than one argument is set to True, a dictionary is returned where
        the keys are the True passed arguments and the corresponding values are
        booleans. True if the text contains the argument, False otherwise.


    Raises
    ------
    ValueError
        If input text is empty, no argument is set to True
    """
    if not text:
        raise ValueError("Text cannot be empty")

    # current function arguments
    current_arguments = locals()
    constants = globals()

    output = {}
    # Since each argument has the same name as the corresponding constant
    # (But, patterns should be prefixed with "PATTERN_" to match the actual pattern.)
    # Looping through all arguments and checking for constants that correspond to the
    # True arguments can work
    # TODO: Maybe find a good pythonic way to do this
    for arg, value in current_arguments.items():
        const = constants.get(arg.upper())
        if const and value is True:
            output[arg] = contains_characters(text, const)
            continue
        # check for pattern
        pattern = constants.get("PATTERN_" + arg.upper())
        if pattern and value is True:
            output[arg] = contains_patterns(text, pattern)

    if custom_chars:
        output["custom_chars"] = contains_characters(text, custom_chars)
    if custom_patterns:
        output["custom_patterns"] = contains_patterns(text, custom_patterns)

    if not output:
        raise ValueError("At least one argument should be True")

    if len(output) == 1:
        output = list(output.values())[0]

    return output


def contains_patterns(text: str, patterns: Union[List[str], str]) -> bool:
    """Check for matched characters in the given text ``text`` using the input
    patterns ``patterns``

    .. note::
        Use lookahead/lookbehind when substrings should not be captured or removed.

    Parameters
    ----------
    text : str
        Text to process
    patterns : Union[List[str], str]
        Pattern(s) to use

    Returns
    -------
    bool
        True if the pattern is found in the given text, False otherwise.

    Raises
    ------
    ValueError
        If no ``patterns`` are provided
    """

    if not patterns:
        raise ValueError("'chars' cannot be empty.")

    # convert list to str
    if isinstance(patterns, list):
        patterns = "|".join(patterns)

    return bool(re.search(patterns, text))


def contains_characters(text: str, chars: Union[List[str], str]) -> str:

    """Check for the input characters ``chars`` in the given text ``text``

    Parameters
    ----------
    text : str
        Text to be processed
    chars : Union[List[str], str]
        list of characters to check for

    Returns
    -------
    bool
        True if the input characters are found in the text, False otherwise

    Raises
    ------
    ValueError
        If no ``chars`` are provided
    """

    if not chars:
        raise ValueError("'chars' cannot be empty.")

    # convert list to str
    if isinstance(chars, list):
        chars = "".join(chars)

    return contains_patterns(text, f"[{chars}]")
