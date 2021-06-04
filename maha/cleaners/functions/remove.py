"""
Functions that operate on a string and remove specific characters.
"""
import re


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

    return re.sub(" " * max_spaces + "+", " " * max_spaces, text)
