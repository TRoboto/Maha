""" Module contains functions that help organize common regex patterns """

__all__ = [
    "non_capturing_group",
    "positive_lookbehind",
    "positive_lookahead",
    "named_group",
]


from typing import Any


def non_capturing_group(*patterns: Any):
    """Returns a non capturing groups of patterns."""
    return "(?:{})".format("|".join(str(p) for p in patterns))


def positive_lookbehind(*patterns: Any):
    """Returns a positive lookbehind pattern."""
    return "(?<={})".format("|".join(str(p) for p in patterns))


def positive_lookahead(*patterns: Any):
    """Returns positive lookahead pattern"""
    return "(?={})".format("|".join(str(p) for p in patterns))


def named_group(name: str, pattern: str):
    """Returns named pattern group"""
    return f"(?P<{name}>{pattern})"
