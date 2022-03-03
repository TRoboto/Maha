from __future__ import annotations

from .arabic import ARABIC_NUMBERS, ARABIC_PUNCTUATIONS
from .english import ENGLISH_NUMBERS, ENGLISH_PUNCTUATIONS

SPACE: str = " "
""" Space character """
EMPTY: str = ""
""" Empty character """
PUNCTUATIONS: list[str] = ARABIC_PUNCTUATIONS + ENGLISH_PUNCTUATIONS
""" Arabic and English punctuations """
NUMBERS: list[str] = ARABIC_NUMBERS + ENGLISH_NUMBERS
""" Arabic and English numbers """
