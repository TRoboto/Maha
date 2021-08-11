""" Module contains functions that help organize common regex patterns """


def non_capturing_group(*words: str):
    """
    Returns a non capturing groups of words without word boundaries.
    """
    return "(?:{})".format("|".join(words))


def named_group(name: str, pattern: str):
    """
    Returns named pattern group
    """
    return f"(?P<{name}>{pattern})"
