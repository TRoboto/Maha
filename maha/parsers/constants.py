from maha.constants import (
    ALEF_VARIATIONS,
    ARABIC_COMMA,
    COMMA,
    SPACE_EXPRESSION,
    SPACE_OR_NONE_EXPRESSION,
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
WAW_CONNECTOR = SPACE_EXPRESSION + WAW + SPACE_OR_NONE_EXPRESSION
""" Pattern that matches WAW as a connector between two words """
WORD_SEPARATOR = (
    f"(?:{SPACE_EXPRESSION}|\\b)"
    f"(?:{COMMA}|{ARABIC_COMMA})?{SPACE_OR_NONE_EXPRESSION}{WAW}?"
    f"(?:{SPACE_OR_NONE_EXPRESSION}|\\b)"
)
""" Pattern that matches the word separator in Arabic """

ALL_ALEF = "".join(ALEF_VARIATIONS)
""" Pattern that matches all possible forms of the ALEF in Arabic """
