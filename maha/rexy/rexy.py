""" Module contains functions that help organize common regex patterns """

__all__ = [
    "optional_non_capturing_group",
    "non_capturing_group",
    "positive_lookbehind",
    "positive_lookahead",
    "named_group",
]


from typing import Union

from maha.rexy.templates import Expression


def non_capturing_group(*patterns: Union[Expression, str]):
    """Returns a non capturing groups of patterns."""
    return "(?:{})".format("|".join(str(p) for p in patterns))


def optional_non_capturing_group(*patterns: Union[Expression, str]):
    """Returns an optional non capturing group of patterns."""
    return "(?:{})?".format("|".join(str(p) for p in patterns))


def positive_lookbehind(*patterns: Union[Expression, str]):
    """Returns a positive lookbehind pattern."""
    return "(?<={})".format("|".join(str(p) for p in patterns))


def positive_lookahead(*patterns: Union[Expression, str]):
    """Returns positive lookahead pattern"""
    return "(?={})".format("|".join(str(p) for p in patterns))


def named_group(name: str, pattern: Union[Expression, str]):
    """Returns named pattern group"""
    return f"(?P<{name}>{pattern})"


def capture_group(pattern: Union[Expression, str]):
    """Returns a capturing group pattern"""
    return f"({pattern})"
