"""List of Persian constant definitions."""

from typing import List

from .simple import *

PERSIAN_NUMBERS: List[str] = [
    PERSIAN_ZERO,
    PERSIAN_ONE,
    PERSIAN_TWO,
    PERSIAN_THREE,
    PERSIAN_FOUR,
    PERSIAN_FIVE,
    PERSIAN_SIX,
    PERSIAN_SEVEN,
    PERSIAN_EIGHT,
    PERSIAN_NINE,
]
"""
List of Persian numerals.
They have different unicodes from :data:`~.ARABIC_NUMBERS`
"""

PERSIAN_UNIQUE_LETTERS: List[str] = [
    PERSIAN_PE,
    PERSIAN_CE,
    PERSIAN_ZE,
    PERSIAN_KAF,
    PERSIAN_GAF,
    PERSIAN_YE,
    PERSIAN_EYE,
]
""" List of Persian unique letters """

PERSIAN: List[str] = PERSIAN_NUMBERS + PERSIAN_UNIQUE_LETTERS
""" List of Persian unique characters """
