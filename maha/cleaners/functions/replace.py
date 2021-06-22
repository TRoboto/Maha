"""
Functions that operate on a string and replace specific characters with others.
"""
__all__ = [
    "replace_characters",
    "replace_characters_except",
    "replace_pairs",
    "replace_pattern",
    "convert_arabic_numbers_to_english",
]

from typing import Callable, List, Union

# To enjoy infinite width lookbehind
import regex as re

from maha.constants import ARABIC_LETTERS, ARABIC_NUMBERS, ENGLISH_NUMBERS


def convert_arabic_numbers_to_english(text: str):
    """Converts Arabic numbers :data:`~.ARABIC_NUMBERS` to the corresponding English
    numbers :data:`~.ENGLISH_NUMBERS`

    Parameters
    ----------
    text : str
        Text to process

    Returns
    -------
    str
        Processed text with all occurrences of Arabic numbers converted
        to English numbers

    Examples
    --------
    .. code-block:: python

        >>> text = '٣'
        >>> convert_arabic_numbers_to_english(text)
        '3'
    
    .. code-block:: python

        >>> text = '١٠'
        >>> convert_arabic_numbers_to_english(text)
        '10'
    """
    return replace_pairs(text, ARABIC_NUMBERS, ENGLISH_NUMBERS)


def replace_pattern(
    text: str, pattern: str, with_value: Union[Callable[..., str], str]
) -> str:
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
    
    Examples
    --------
    .. code-block:: python 

        >>> text = 'ولقد حصلت على ١٠ من ١٠ '
        >>> replace_pattern(text, '١٠', 'عشرة')
        'ولقد حصلت على عشرة من عشرة '

    .. code-block:: python 

        >>> text = "ذهبت الفتاه إلى المدرسه"
        >>> replace_pattern(text, 'ه( |$)' , 'ة')
        'ذهبت الفتاةإلى المدرسة'
    """
    return re.sub(pattern, with_value, text)


def replace_characters(
    text: str, characters: Union[List[str], str], with_value: str
) -> str:
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

    Examples
    --------
    .. code-block:: python

        >>> text = 'حصل الولد على معدل 50%'
        >>> replace_characters(text, '%' , ' بالمئة')
        'حصل الولد على معدل 50 بالمئة'

    .. code-block:: python

        >>> text = 'ولقد كلف هذا المنتج 100 $'
        >>> replace_characters(text, '$','دولار')
        'ولقد كلف هذا المنتج 100 دولار'
    """
    characters = str(re.escape(characters))
    return replace_pattern(text, f"[{characters}]", with_value)


def replace_characters_except(
    text: str, characters: Union[List[str], str], with_value: str
) -> str:
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

    Example
    -------
    .. code-block:: python

        >>> text = 'لَيتَ الذينَ تُحبُّ العيّنَ رؤيَتهم'
        >>> replace_characters_except(text, ARABIC_LETTERS + [' '] ,'')
        'ليت الذين تحب العين رؤيتهم'
    """
    characters = str(re.escape(characters))
    return replace_pattern(text, f"[^{characters}]", with_value)


def replace_pairs(text: str, keys: List[str], values: List[str]) -> str:
    """Replaces each key with its corresponding value in the given text

    Parameters
    ----------
    text : str
        Text to process
    keys :
        Characters to be replaced
    values :
        Characters to be replaced with

    Returns
    -------
    str
        Processed text

    Raises
    ------
    ValueError
        If keys and values are of different lengths
    
    Example
    -------
    ..  code-block:: python 

        >>> text = 'وقال مؤمن هذا أمر مؤقت'
        >>> replace_pairs(text, ['ؤ'] ,['و'])
        'وقال مومن هذا أمر موقت'
    """

    if len(keys) != len(values):
        raise ValueError("'keys' and 'values' should have the same length")

    escaped = [str(re.escape(c)) for c in keys]
    pattern = "|".join(escaped)

    def func(match):
        return values[keys.index(match.group(0))]

    return replace_pattern(text, pattern, func)
