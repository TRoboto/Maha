from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable


def get_unicode(text: str) -> bytes:
    """Returns the unicode for input text

    Parameters
    ----------
    text : str
        Text to encode

    Returns
    -------
    bytes
        Text with characters encoded in raw unicode.
    """
    return text.encode("raw_unicode_escape")


def check_positive_integer(value: float, var_name: str):
    """Raises ValueError if the input value is not a positive integer.

    Parameters
    ----------
    value : float
        Input value
    var_name : str
        Variable name to include it in the error message

    Raises
    ------
    ValueError
        if the input value is not a positive integer.
    """
    if value < 1:
        raise ValueError(f"'{var_name}' should be greater than 0")

    if value != int(value):
        raise ValueError(f"Cannot assign a float value to '{var_name}'")


def negate(f):
    """Negates a function"""

    @wraps(f)
    def g(*args, **kwargs):
        return not f(*args, **kwargs)

    return g


@dataclass
class ObjectGet:
    """Used with get function in :class:`BaseProcessor`"""

    # function to use
    func: Callable
    # initial value
    prev: Any
    # name of the operation (argument name)
    name: str
    # Function to apply at end
    # Defaults for post_fn, return the input
    post_fn: Callable = lambda input: input
