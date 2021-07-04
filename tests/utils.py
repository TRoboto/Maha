from typing import Any, List

from maha.constants import SPACE


def list_in_string(char_list: List[str], text: str):
    """Returns true if all input characters are in the given text"""
    return all(c in text for c in char_list)


def list_only_in_string(char_list: List[str], text: str, include_space=True):
    """Returns true if the given text only contains characters from the input list
    of chars
    """
    if include_space:
        char_list += SPACE
    return all(c in char_list for c in text)


def list_not_in_string(char_list: List[str], text: str):
    """Returns true if all input characters are not in the given text"""
    return all(c not in text for c in char_list)


def is_true(expression: Any):
    """Returns true if the input expression evaluates to true"""
    return expression is True


def is_false(expression: Any):
    """Returns true if the input expression evaluates to false"""
    return expression is False
