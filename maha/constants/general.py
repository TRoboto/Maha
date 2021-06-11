from typing import List

from .arabic import ARABIC_NUMBERS, ARABIC_PUNCTUATIONS
from .english import ENGLISH_NUMBERS, ENGLISH_PUNCTUATIONS

SPACE: str = " "
""" Space character """
EMPTY: str = ""
""" Empty character """
PUNCTUATIONS: List[str] = ARABIC_PUNCTUATIONS + ENGLISH_PUNCTUATIONS
""" Arabic and English punctuations """
NUMBERS: List[str] = ARABIC_NUMBERS + ENGLISH_NUMBERS
""" Arabic and English numbers """
