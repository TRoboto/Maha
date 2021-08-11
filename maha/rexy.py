""" Module contains functions that help organize common regex patterns """


def get_non_capturing_group(*words: str):
    """
    Returns a non capturing groups of words without word boundaries.
    """
    return "(?:{})".format("|".join(words))


def get_named_group(name: str, pattern: str):
    """
    Returns named pattern group
    """
    return "(?P<{}>{})".format(name, pattern)
