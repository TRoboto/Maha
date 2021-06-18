"""
Functions that operate on a string and replace specific characters with others.
"""
__all__ = [
    "replace_characters",
    "replace_characters_except",
    "replace_pairs",
    "replace_pattern",
]

from typing import List

# To enjoy infinite width lookbehind
import regex as re


def replace_pattern(text: str, pattern: str, with_value: str) -> str:
    """Matches characters from the input text using the given ``pattern``
    and replaces all matched characters with the given value.

    Parameters
    ----------
    text : str
        Text to process
    pattern :
        Pattern used to match characters from the text
    with_value :
        Value to replace the matched characters with

    Returns
    -------
    str
        Processed text
    """
    return re.sub(pattern, with_value, text)


def replace_characters(text: str, characters: str, with_value: str) -> str:
    """Replaces the input ``characters`` in the given text with the given value

    Parameters
    ----------
    text : str
        Text to process
    characters :
        Characters to replace
    with_value :
        Value to replace the input characters with

    Returns
    -------
    str
        Processed text
    """
    characters = str(re.escape(characters))
    return replace_pattern(text, f"[{characters}]", with_value)


def replace_characters_except(text: str, characters: str, with_value: str) -> str:
    """Replaces everything except the input ``characters`` in the given text
    with the given value

    Parameters
    ----------
    text : str
        Text to process
    characters :
        Characters to preserve (not replace)
    with_value :
        Value to replace all other characters with.

    Returns
    -------
    str
        Processed text
    """
    characters = str(re.escape(characters))
    return replace_pattern(text, f"[^{characters}]", with_value)


def replace_pairs(text: str, keys: List[str], values: List[str]) -> str:
    """Replaces each key with its corresponding value in the given text

    Parameters
    ----------
    text : str
        Text to process
    keys : Iterable[str]
        Characters to be replaced
    values : Iterable[str]
        Characters to be replace with

    Returns
    -------
    str
        Processed text
    """

    pattern = "|".join(map(re.escape, keys))

    def func(match):
        return values[keys.index(match.group(0))]

    return replace_pattern(text, pattern, func)
