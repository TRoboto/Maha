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
