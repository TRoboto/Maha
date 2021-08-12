""" Module contains functions that help organize common regex patterns """

__all__ = [
    "non_capturing_group",
    "positive_lookbehind",
    "named_group",
]


def non_capturing_group(*patterns: str):
    """Returns a non capturing groups of patterns."""
    return "(?:{})".format("|".join(str(p) for p in patterns))


def positive_lookbehind(*patterns: str):
    """Returns a positive lookbehind pattern."""
    return "(?<={})".format("|".join(str(p) for p in patterns))


def named_group(name: str, pattern: str):
    """Returns named pattern group"""
    return f"(?P<{name}>{pattern})"
