"""
Functions that operate on a string and check for values contained in it
"""

__all__ = [
    "contains",
    "contains_patterns",
    "contain_strings",
    "contains_repeated_substring",
    "contains_single_letter_word",
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
    LAM_ALEF,
    LAM_ALEF_VARIATIONS,
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
    PERSIAN,
    PUNCTUATIONS,
    SPACE,
    TATWEEL,
)
from maha.utils import check_positive_integer


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
    lam_alef_variations: bool = False,
    lam_alef: bool = False,
    punctuations: bool = False,
    arabic_numbers: bool = False,
    english_numbers: bool = False,
    arabic_punctuations: bool = False,
    english_punctuations: bool = False,
    arabic_ligatures: bool = False,
    persian: bool = False,
    arabic_hashtags: bool = False,
    arabic_mentions: bool = False,
    emails: bool = False,
    english_hashtags: bool = False,
    english_mentions: bool = False,
    hashtags: bool = False,
    links: bool = False,
    mentions: bool = False,
    emojis: bool = False,
    custom_strings: Union[List[str], str] = None,
    custom_patterns: Union[List[str], str] = None,
    operator: str = None,
) -> Union[Dict[str, bool], bool]:

    """Check for certain characters, strings or patterns in the given text.

    To add a new parameter, make sure that its name is the same as the corresponding
    constant. For the patterns, only remove the prefix PATTERN_ from the parameter name

    Parameters
    ----------
    text : str
        Text to check
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
    lam_alef_variations : bool, optional
        Check for :data:`~.LAM_ALEF_VARIATIONS` characters, by default False
    lam_alef : bool, optional
        Check for :data:`~.LAM_ALEF` character, by default False
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
    persian : bool, optional
        Check for :data:`~.PERSIAN` characters, by default False
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
    custom_strings : Union[List[str], str], optional
        Include any other string(s), by default None
    custom_patterns : Union[List[str], str], optional
        Include any other regular expression patterns, by default None
    operator : bool, optional
        When multiple arguments are set to True, this operator is used  to combine
        the output into a boolean. Takes 'and' or 'or', by default None

    Returns
    -------
    Union[Dict[str, bool], bool]
        * If one argument is set to True, a boolean value is returned. True if the text
        contains it, False otherwise.
        * If ``operator`` is set and more than one argument is set to True, a boolean
        value that combines the result with the "and/or" operator is returned.
        * If more than one argument is set to True, a dictionary is returned where
        keys are the True passed arguments and the corresponding values are
        booleans. True if the text contains the argument, False otherwise.


    Raises
    ------
    ValueError
        If no argument is set to True

    Examples
    --------

    .. code-block:: pycon

        >>> text = "مقاييس أداء النماذج في التعلم الآلي Machine Learning ... 🌺"
        >>> contains(text, english=True, emails=True, emojis=True)
        {'english': True, 'emails': False, 'emojis': True}

    .. code-block:: pycon

        >>> text = "قال رسول اللهﷺ إن خير أيامكم يوم الجمعة فأكثروا عليَّ من الصلاة فيه"
        >>> contains(text, english=True)
        False
    """
    if not text:
        return False

    if operator is not None and operator not in ["or", "and"]:
        raise ValueError("`operator` can only take 'and' or 'or'")

    custom_strings = custom_strings or []
    custom_patterns = custom_patterns or []

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
            output[arg] = contain_strings(text, const)
            continue
        # check for pattern
        pattern = constants.get("PATTERN_" + arg.upper())
        if pattern and value is True:
            output[arg] = contains_patterns(text, pattern)

    if custom_strings:
        output["custom_strings"] = contain_strings(text, custom_strings)
    if custom_patterns:
        output["custom_patterns"] = contains_patterns(text, custom_patterns)

    if not output:
        raise ValueError("At least one argument should be True")

    if len(output) == 1:
        output = list(output.values())[0]
    elif operator == "and":
        output = all(list(output.values()))
    elif operator == "or":
        output = any(list(output.values()))

    return output


def contains_repeated_substring(text: str, min_repeated: int = 3) -> bool:
    """Check for consecutive substrings that are repeated at least ``min_repeated``
    times. For example with the default arguments, the text 'hhhhhh' should return True

    Parameters
    ----------
    text : str
        Text to check
    min_repeated : int, optional
        Minimum number of consecutive repeated substring to consider, by default 3

    Returns
    -------
    bool
        True if the input text contains consecutive substrings, otherwise False

    Raises
    ------
    ValueError
        If non positive integer is passed

    Example
    -------

    .. code-block:: pycon

        >>> text = "كانت اللعبة حللللللللوة جداً"
        >>> contains_repeated_substring(text)
        True
    """
    check_positive_integer(min_repeated, "min_repeated")

    pattern = r"(.+?)\1{}".format(f"{{{min_repeated-1},}}")
    return contains_patterns(text, pattern)


def contains_single_letter_word(
    text: str,
    arabic_letters: bool = False,
    english_letters: bool = False,
):
    """Check for a single-letter word. For example, "how r u" should return True if
    ``english_letters`` is set to True because it contains two single-letter word,
    "r" and "u".

    Parameters
    ----------
    text : str
        Text to check
    arabic_letters : bool, optional
        Check for all :data:`~.ARABIC_LETTERS`, by default False
    english_letters : bool, optional
        Check for all :data:`~.ENGLISH_LETTERS`, by default False

    Returns
    -------
    bool
        True if the input text contains single-letter word, False otherwise

    Raises
    ------
    ValueError
        If no argument is set to True

    Example
    -------

    .. code-block:: pycon

        >>> text = "cu later my friend, ك"
        >>> contains_single_letter_word(text, arabic_letters=True, english_letters=True)
        True
    """
    letters = []
    if arabic_letters:
        letters += ARABIC_LETTERS
    if english_letters:
        letters += ENGLISH_LETTERS

    if not letters:
        raise ValueError("At least one argument should be True")

    pattern = r"\b[{}]\b".format("".join(letters))
    return contains_patterns(text, pattern)


def contains_patterns(text: str, patterns: Union[List[str], str]) -> bool:
    r"""Check for matched strings in the given ``text`` using the input ``patterns``

    .. note::
        Use lookahead/lookbehind when substrings should not be captured or removed.

    Parameters
    ----------
    text : str
        Text to check
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

    Example
    -------

    .. code-block:: pycon

        >>> text = "علم الهندسة (Engineering)"
        >>> contains_patterns(text, r"\([A-Za-z]+\)")
        True
    """

    if not patterns:
        raise ValueError("'chars' cannot be empty.")

    # convert list to str
    if isinstance(patterns, list):
        patterns = "|".join(patterns)

    return bool(re.search(patterns, text))


def contain_strings(text: str, strings: Union[List[str], str]) -> bool:
    """Check for the input ``strings`` in the given ``text``

    Parameters
    ----------
    text : str
        Text to check
    strings : Union[List[str], str]
        String or list of strings to check for

    Returns
    -------
    bool
        True if the input string(s) are found in the text, False otherwise

    Raises
    ------
    ValueError
        If no ``strings`` are provided

    Example
    -------

    .. code-block:: pycon

        >>> text = "الله أكبر، الحمد لله رب العالمين"
        >>> contain_strings(text, "الله")
        True
    """

    if not strings:
        raise ValueError("'strings cannot be empty.")

    # convert list to str
    if isinstance(strings, list):
        strings = "|".join(str(re.escape(c)) for c in strings)
    else:
        strings = str(re.escape(strings))

    return contains_patterns(text, f"({strings})")
