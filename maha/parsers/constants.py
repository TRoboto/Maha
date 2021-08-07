from maha.constants import (
    ALEF_VARIATIONS,
    ARABIC_COMMA,
    COMMA,
    PATTERN_SPACE,
    PATTERN_SPACE_OR_NONE,
    WAW,
)

from .helper import get_non_capturing_group

THIRD = "[ثت]ل[ثت]"
""" Pattern that matches the pronunciation of third in Arabic """
QUARTER = "ربع"
""" Pattern that matches the pronunciation of quarter in Arabic """
HALF = "نصف?"
""" Pattern that matches the pronunciation of half in Arabic """
THREE_QUARTERS = f"[إا]لا {QUARTER}"
""" Pattern that matches the pronunciation of three quarters in Arabic """
WAW_CONNECTOR = PATTERN_SPACE + WAW + PATTERN_SPACE_OR_NONE
""" Pattern that matches WAW as a connector between two words """
NUMERAL_WORD_SEPARATOR = f"(?:{COMMA}|{ARABIC_COMMA})?{PATTERN_SPACE_OR_NONE}{WAW}"
""" Pattern that matches the word separator between numerals in Arabic """

ALL_ALEF = "".join(ALEF_VARIATIONS)
""" Pattern that matches all possible forms of the ALEF in Arabic """


TWO_SUFFIX = get_non_capturing_group("ين", "ان")
SUM_SUFFIX = get_non_capturing_group("ين", "ون")
