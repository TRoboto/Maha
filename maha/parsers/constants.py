from maha.constants import (
    ALEF_VARIATIONS,
    ARABIC_COMMA,
    COMMA,
    PATTERN_SPACE,
    PATTERN_SPACE_OR_NONE,
    WAW,
)

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
WORD_SEPARATOR = (
    f"(?:^|\\W)"
    f"(?:{COMMA}|{ARABIC_COMMA})?{PATTERN_SPACE_OR_NONE}{WAW}?"
    f"(?:{PATTERN_SPACE_OR_NONE}|\\b)"
)
""" Pattern that matches the word separator in Arabic """

ALL_ALEF = "".join(ALEF_VARIATIONS)
""" Pattern that matches all possible forms of the ALEF in Arabic """
