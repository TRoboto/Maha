"""
Functions that operate on a string and replace specific characters with others.
"""
__all__ = [
    "replace",
    "replace_except",
    "replace_pairs",
    "replace_pattern",
    "convert_arabic_numbers_to_english",
]

from typing import Callable, List, Union

# To enjoy infinite width lookbehind
import regex as re

from maha.constants import ARABIC_LETTERS, ARABIC_NUMBERS, ENGLISH_NUMBERS, EMPTY, SPACE



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
        >>> replace_pattern(text, 'ه( |$)' , ' ة').strip()
        'ذهبت الفتاة إلى المدرسة'
    """
    return re.sub(pattern, with_value, text)


def replace(text: str, strings: Union[List[str], str], with_value: str) -> str:
    """Replaces the input ``strings`` in the given text with the given value

    Parameters
    ----------
    text : str
        Text to process
    strings :
        Strings to replace
    with_value :
        Value to replace the input strings with

    Returns
    -------
    str
        Processed text

    Examples
    --------
    .. code-block:: python

        >>> text = 'حصل الولد على معدل 50%'
        >>> replace(text, '%' , ' بالمئة')
        'حصل الولد على معدل 50 بالمئة'

    .. code-block:: python

        >>> text = 'ولقد كلف هذا المنتج 100 $'
        >>> replace(text, '$','دولار')
        'ولقد كلف هذا المنتج 100 دولار'
    """
    # convert list to str
    if isinstance(strings, list):
        strings = "|".join(str(re.escape(c)) for c in strings)
    else:
        strings = str(re.escape(strings))

    return replace_pattern(text, f"({strings})", with_value)


def replace_except(text: str, strings: Union[List[str], str], with_value: str) -> str:
    """Replaces everything except the input ``strings`` in the given text
    with the given value

    Parameters
    ----------
    text : str
        Text to process
    strings :
        Strings to preserve (not replace)
    with_value :
        Value to replace all other strings with.

    Returns
    -------
    str
        Processed text

    Example
    -------
    .. code-block:: python

        >>> text = 'لَيتَ الذينَ تُحبُّ العيّنَ رؤيَتهم'
        >>> replace_except(text, ARABIC_LETTERS + [SPACE] , EMPTY)
        'ليت الذين تحب العين رؤيتهم'
    """
    # convert list to str
    if isinstance(strings, list):
        strings = "|".join(str(re.escape(c)) for c in strings)
    else:
        strings = str(re.escape(strings))

    # To include the end
    strings += "|$"

    return replace_pattern(
        text,
        f"(.*?)({strings})",
        lambda m: with_value + m.groups()[1] if m.groups()[0] else m.groups()[1],
    )


def replace_pairs(text: str, keys: List[str], values: List[str]) -> str:
    """Replaces each key with its corresponding value in the given text

    Parameters
    ----------
    text : str
        Text to process
    keys :
        Strings to be replaced
    values :
        Strings to be replaced with

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

        >>> text = 'شلونك يا محمد؟'
        >>> replace_pairs(text, ['شلونك'] , ['كيف حالك'])
        'كيف حالك يا محمد؟'
    """

    if len(keys) != len(values):
        raise ValueError("'keys' and 'values' should have the same length")

    escaped = [str(re.escape(c)) for c in keys]
    pattern = "|".join(escaped)

    def func(match):
        return values[keys.index(match.group(0))]

    return replace_pattern(text, pattern, func)
