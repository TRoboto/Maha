"""List of Persian constant definitions."""

from __future__ import annotations

from .simple import *

PERSIAN_NUMBERS: list[str] = [
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

PERSIAN_UNIQUE_LETTERS: list[str] = [
    PERSIAN_PE,
    PERSIAN_CE,
    PERSIAN_ZE,
    PERSIAN_KAF,
    PERSIAN_GAF,
    PERSIAN_YE,
    PERSIAN_EYE,
]
""" List of Persian unique letters """

PERSIAN: list[str] = PERSIAN_NUMBERS + PERSIAN_UNIQUE_LETTERS
""" List of Persian unique characters """
