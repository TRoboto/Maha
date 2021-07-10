"""Functions that extracts values from text"""

__all__ = ["parse"]

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
from maha.parsers.templates.dimensions import Dimension
from maha.parsers.templates.enums import DimensionType


def parse(
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
    custom_strings: Union[List[str], str] = None,
    custom_patterns: Union[List[str], str] = None,
) -> Union[List[Dimension], Dict[str, List[Dimension]]]:

    """Extracts certain characters/patterns from the given text.

    To add a new parameter, make sure that its name is the same as the corresponding
    constant. For the patterns, only remove the prefix PATTERN_ from the parameter name

    Parameters
    ----------
    text : str
        Text to be processed
    arabic : bool, optional
        Extract :data:`~.ARABIC` characters, by default False
    english : bool, optional
        Extract :data:`~.ENGLISH` characters, by default False
    arabic_letters : bool, optional
        Extract :data:`~.ARABIC_LETTERS` characters, by default False
    english_letters : bool, optional
        Extract :data:`~.ENGLISH_LETTERS` characters, by default False
    english_small_letters : bool, optional
        Extract :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
    english_capital_letters : bool, optional
        Extract :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
    numbers : bool, optional
        Extract :data:`~.NUMBERS` characters, by default False
    harakat : bool, optional
        Extract :data:`~.HARAKAT` characters, by default False
    all_harakat : bool, optional
        Extract :data:`~.ALL_HARAKAT` characters, by default False
    tatweel : bool, optional
        Extract :data:`~.TATWEEL` character, by default False
    punctuations : bool, optional
        Extract :data:`~.PUNCTUATIONS` characters, by default False
    arabic_numbers : bool, optional
        Extract :data:`~.ARABIC_NUMBERS` characters, by default False
    english_numbers : bool, optional
        Extract :data:`~.ENGLISH_NUMBERS` characters, by default False
    arabic_punctuations : bool, optional
        Extract :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
    english_punctuations : bool, optional
        Extract :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
    arabic_ligatures : bool, optional
        Extract :data:`~.ARABIC_LIGATURES` words, by default False
    arabic_hashtags : bool, optional
        Extract Arabic hashtags using the pattern :data:`~.PATTERN_ARABIC_HASHTAGS`,
        by default False
    arabic_mentions : bool, optional
        Extract Arabic mentions using the pattern :data:`~.PATTERN_ARABIC_MENTIONS`,
        by default False
    emails : bool, optional
        Extract Arabic hashtags using the pattern :data:`~.PATTERN_EMAILS`,
        by default False
    english_hashtags : bool, optional
        Extract Arabic hashtags using the pattern :data:`~.PATTERN_ENGLISH_HASHTAGS`,
        by default False
    english_mentions : bool, optional
        Extract Arabic hashtags using the pattern :data:`~.PATTERN_ENGLISH_MENTIONS`,
        by default False
    hashtags : bool, optional
        Extract Arabic hashtags using the pattern :data:`~.PATTERN_HASHTAGS`,
        by default False
    links : bool, optional
        Extract Arabic hashtags using the pattern :data:`~.PATTERN_LINKS`,
        by default False
    mentions : bool, optional
        Extract Arabic hashtags using the pattern :data:`~.PATTERN_MENTIONS`,
        by default False
    emojis : bool, optional
        Extract emojis using the pattern :data:`~.PATTERN_EMOJIS`,
        by default False
    custom_strings : Union[List[str], str], optional
        Include any other string(s), by default None
    custom_patterns , optional
        Include any other regular expression patterns, by default None

    Returns
    -------
    Union[List[:class:`~.Dimension`], Dict[str, List[:class:`~.Dimension`]]]
        * If one argument is set to True, a list of dimensions is returned. Can be
        empty if no match found.
        * If more than one argument is set to True, a dictionary is returned where
        keys are the True passed arguments and the corresponding values are
        list of dimensions, any of which can be empty if no match found.

    Raises
    ------
    ValueError
        If no argument is set to True
    """
    if not text:
        return []

    custom_strings = custom_strings or []
    custom_patterns = custom_patterns or []

    # current function arguments
    current_arguments = locals()
    constants = globals()

    if isinstance(custom_strings, str):
        custom_strings = [custom_strings]

    if isinstance(custom_patterns, str):
        custom_patterns = [custom_patterns]

    output = {}

    # Since each argument has the same name as the corresponding constant
    # (But, patterns should be prefixed with "PATTERN_" to match the actual pattern.)
    # Looping through all arguments and appending constants that correspond to the
    # True arguments can work
    # TODO: Maybe find a good pythonic way to do this
    for arg, value in current_arguments.items():
        const = constants.get(arg.upper())
        if const and value is True:
            parsed = parse_patterns(text, f"[{''.join(const)}]+")
            # change dimension
            for dim in parsed:
                dim.dimension = DimensionType[arg.upper()]
                dim.is_confident = True
            output[arg] = parsed
            continue
        # check for pattern
        pattern = constants.get("PATTERN_" + arg.upper())
        if pattern and value is True:
            parsed = parse_patterns(text, pattern)
            # change dimension
            for dim in parsed:
                dim.dimension = DimensionType[arg.upper()]
                dim.is_confident = True
            output[arg] = parsed

    if custom_strings:
        output["custom_strings"] = parse_strings(text, custom_strings)
    if custom_patterns:
        output["custom_patterns"] = parse_patterns(text, custom_patterns)

    if not output:
        raise ValueError("At least one argument should be True")

    if len(output) == 1:
        output = list(output.values())[0]

    return output


def parse_patterns(text: str, patterns: Union[List[str], str]) -> List[Dimension]:
    """Extract matched strings in the given ``text`` using the input ``patterns``

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
    List[Dimension]
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
    print(patterns)
    output = []
    for m in re.finditer(patterns, text):
        start = m.start(0)
        end = m.end(0)
        value = text[start:end]
        dim = Dimension(start=start, end=end, value=value)
        output.append(dim)

    return output


def parse_strings(text: str, strings: Union[List[str], str]) -> List[Dimension]:
    """Extract the input ``strings`` in the given ``text``

    Parameters
    ----------
    text : str
        Text to check
    strings : Union[List[str], str]
        String or list of strings to extract

    Returns
    -------
    List[:class:`~.Dimension`]
        List of extracted dimensions

    Raises
    ------
    ValueError
        If no ``strings`` are provided
    """

    if not strings:
        raise ValueError("'strings cannot be empty.")

    # convert list to str
    if isinstance(strings, list):
        strings = "|".join(str(re.escape(c)) for c in strings) + "+"
    else:
        strings = str(re.escape(strings))
    output = []
    for m in re.finditer(strings, text):
        start = m.start(0)
        end = m.end(0)
        value = text[start:end]
        dim = Dimension(
            start=start,
            end=end,
            value=value,
            is_confident=True,
        )
        output.append(dim)

    return output
