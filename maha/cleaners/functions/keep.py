"""
Functions that operate on a string and remove all but certain characters.
"""

__all__ = [
    "keep",
    "keep_arabic",
    "keep_characters",
]

import re
from typing import List, Union

from maha.constants.general import EMPTY, SPACE

from ...constants import ALL_HARAKAT, ARABIC_CHARS, ARABIC_NUMBERS
from .remove import remove_extra_spaces


def keep(
    text: str,
    arabic=False,
    english=False,
):
    pass


def keep_arabic(text: str) -> str:
    return keep_characters(text, ARABIC_CHARS)


def keep_characters(
    text: str, chars: Union[List[str], str], use_space: bool = True
) -> str:

    """Keeps only the input characters ``chars`` in the given text ``text``

    This works by replacing all characters except the input ``chars`` with a space,
    which means space is kept. This is to help separate texts when unwanted characters
    are present without spaces such as 'end.start', which will be converted to
    'end start' if English characters are to be kept.

    Parameters
    ----------
    text : str
        Text to be processed
    chars : Union[List[str], str]
        list of characters to keep
    use_space :
        False to not replace with space, defaults to True

    Returns
    -------
    str
        Text that contains only the input characters.

    Raises
    ------
    ValueError
        When ``chars`` is empty
    """

    if not chars:
        raise ValueError("'chars' cannot be empty.")

    # convert list to str
    chars = "".join(chars)
    chars = re.escape(chars)

    if use_space:
        # remove space character if included
        chars = chars.replace(SPACE, EMPTY)
        # remove all not included harakat first
        # (to fix extra spacing between characters)
        not_included_harakat = "".join([h for h in ALL_HARAKAT if h not in chars])
        output_text = re.sub(f"[{not_included_harakat}]", EMPTY, text)

        output_text = re.sub(f"[^{chars}]", SPACE, output_text)
        output_text = remove_extra_spaces(output_text)
    else:
        output_text = re.sub(f"[^{chars}]", EMPTY, text)

    return output_text.strip()
