""" Module contains functions that help organize common regex patterns """
from __future__ import annotations

__all__ = [
    "optional_non_capturing_group",
    "non_capturing_group",
    "positive_lookbehind",
    "positive_lookahead",
    "named_group",
    "capture_group",
]


from maha.rexy.templates import Expression


def non_capturing_group(*patterns: Expression | str):
    """Returns a non capturing groups of patterns."""
    return "(?:{})".format("|".join(str(p) for p in patterns))


def optional_non_capturing_group(*patterns: Expression | str):
    """Returns an optional non capturing group of patterns."""
    return "(?:{})?".format("|".join(str(p) for p in patterns))


def positive_lookbehind(*patterns: Expression | str):
    """Returns a positive lookbehind pattern."""
    return "(?<={})".format("|".join(str(p) for p in patterns))


def positive_lookahead(*patterns: Expression | str):
    """Returns positive lookahead pattern"""
    return "(?={})".format("|".join(str(p) for p in patterns))


def named_group(name: str, pattern: Expression | str):
    """Returns named pattern group"""
    return f"(?P<{name}>{pattern})"


def capture_group(*patterns: Expression | str):
    """Returns a capturing group pattern"""
    return "({})".format("|".join(str(p) for p in patterns))
