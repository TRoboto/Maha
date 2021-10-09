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
