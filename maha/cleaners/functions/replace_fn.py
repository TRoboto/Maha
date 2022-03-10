"""
Functions that operate on a string and replace specific characters with others.
"""
from __future__ import annotations

__all__ = [
    "replace",
    "replace_except",
    "replace_pairs",
    "replace_expression",
    "arabic_numbers_to_english",
    "connect_single_letter_word",
]


from typing import Callable

# To enjoy infinite width lookbehind
import regex as re

from maha.constants import (
    ARABIC_LETTERS,
    ARABIC_NUMBERS,
    BEH,
    EMPTY,
    ENGLISH_NUMBERS,
    FEH,
    KAF,
    LAM,
    SPACE,
    TEH,
    WAW,
)
from maha.rexy import Expression, ExpressionGroup


def connect_single_letter_word(
    text: str,
    waw: bool | None = None,
    feh: bool | None = None,
    beh: bool | None = None,
    lam: bool | None = None,
    kaf: bool | None = None,
    teh: bool | None = None,
    all: bool | None = None,
    custom_strings: list[str] | str | None = None,
):
    """Connects single-letter word with the letter following it.

    Parameters
    ----------
    text : str
        Text to process
    waw : bool, optional
        Connect :data:`.WAW` letter, by default None
    feh : bool, optional
        Connect :data:`.FEH` letter, by default None
    beh : bool, optional
        Connect :data:`.BEH` letter, by default None
    lam : bool, optional
        Connect :data:`.LAM` letter, by default None
    kaf : bool, optional
        Connect :data:`.KAF` letter, by default None
    teh : bool, optional
        Connect :data:`.TEH` letter, by default None
    all : bool, optional
        Connect all letter except the ones set to False, by default None
    custom_strings : Union[List[str], str], optional
        Include any other string(s) to connect, by default None
    """
    letters = []
    if isinstance(custom_strings, str):
        custom_strings = [custom_strings]

    if waw or (all and waw is not False):
        letters.append(WAW)
    if feh or (all and feh is not False):
        letters.append(FEH)
    if beh or (all and beh is not False):
        letters.append(BEH)
    if lam or (all and lam is not False):
        letters.append(LAM)
    if kaf or (all and kaf is not False):
        letters.append(KAF)
    if teh or (all and teh is not False):
        letters.append(TEH)
    if custom_strings:
        letters.extend(re.escape(s) for s in custom_strings)

    chars = "|".join(letters)
    return replace_expression(text, rf"(\b)({chars})(?:\s)(?=.)", r"\1\2")


def arabic_numbers_to_english(text: str):
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
    .. code:: pycon

        >>> from maha.cleaners.functions import arabic_numbers_to_english
        >>> text = "٣"
        >>> arabic_numbers_to_english(text)
        '3'

    .. code:: pycon

        >>> from maha.cleaners.functions import arabic_numbers_to_english
        >>> text = "١٠"
        >>> arabic_numbers_to_english(text)
        '10'
    """
    return replace_pairs(text, ARABIC_NUMBERS, ENGLISH_NUMBERS)


def replace_expression(
    text: str,
    expression: Expression | ExpressionGroup | str,
    with_value: Callable[..., str] | str,
) -> str:
    """Matches characters from the input text using the given ``expression``
    and replaces all matched characters with the given value.

    Parameters
    ----------
    text : str
        Text to process
    expression :
        Pattern/Expression used to match characters from the text
    with_value :
        Value to replace the matched characters with

    Returns
    -------
    str
        Processed text

    Examples
    --------
    .. code:: pycon

        >>> from maha.cleaners.functions import replace_expression
        >>> text = "ولقد حصلت على ١٠ من ١٠ "
        >>> replace_expression(text, "١٠", "عشرة")
        'ولقد حصلت على عشرة من عشرة '

    .. code:: pycon

        >>> from maha.cleaners.functions import replace_expression
        >>> text = "ذهبت الفتاه إلى المدرسه"
        >>> replace_expression(text, "ه( |$)", "ة ").strip()
        'ذهبت الفتاة إلى المدرسة'
    """
    if isinstance(expression, str):
        expression = Expression(expression)

    if isinstance(expression, ExpressionGroup):
        expression = Expression(expression.join())

    return expression.sub(with_value, text)


def replace(text: str, strings: list[str] | str, with_value: str) -> str:
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
    .. code:: pycon

        >>> from maha.cleaners.functions import replace
        >>> text = "حصل الولد على معدل 50%"
        >>> replace(text, "%", " بالمئة")
        'حصل الولد على معدل 50 بالمئة'

    .. code:: pycon

        >>> from maha.cleaners.functions import replace
        >>> text = "ولقد كلف هذا المنتج 100 $"
        >>> replace(text, "$", "دولار")
        'ولقد كلف هذا المنتج 100 دولار'
    """
    # convert list to str
    if isinstance(strings, list):
        strings = "|".join(str(re.escape(c)) for c in strings)
    else:
        strings = str(re.escape(strings))

    return replace_expression(text, f"({strings})", with_value)


def replace_except(text: str, strings: list[str] | str, with_value: str) -> str:
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
    .. code:: pycon

        >>> from maha.cleaners.functions import replace_except
        >>> from maha.constants import ARABIC_LETTERS, SPACE, EMPTY
        >>> text = "لَيتَ الذينَ تُحبُّ العيّنَ رؤيَتهم"
        >>> replace_except(text, ARABIC_LETTERS + [SPACE], EMPTY)
        'ليت الذين تحب العين رؤيتهم'
    """
    # convert list to str
    if isinstance(strings, list):
        strings = "|".join(str(re.escape(c)) for c in strings)
    else:
        strings = str(re.escape(strings))

    # To include the end
    strings += "|$"

    return replace_expression(
        text,
        f"(.*?)({strings})",
        lambda m: with_value + m.groups()[1] if m.groups()[0] else m.groups()[1],
    )


def replace_pairs(text: str, keys: list[str], values: list[str]) -> str:
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
    ..  code:: pycon

        >>> from maha.cleaners.functions import replace_pairs
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

    return replace_expression(text, pattern, func)
