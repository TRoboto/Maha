"""List of Arabic constant definitions."""

from __future__ import annotations

from .simple import *

ARABIC_LETTERS: list[str] = [
    ALEF,
    BEH,
    TEH,
    THEH,
    JEEM,
    HAH,
    KHAH,
    DAL,
    THAL,
    REH,
    ZAIN,
    SEEN,
    SHEEN,
    SAD,
    DAD,
    TAH,
    ZAH,
    AIN,
    GHAIN,
    FEH,
    QAF,
    KAF,
    LAM,
    MEEM,
    NOON,
    HEH,
    WAW,
    YEH,
    ALEF_MAKSURA,
    TEH_MARBUTA,
    ALEF_MADDA_ABOVE,
    ALEF_HAMZA_ABOVE,
    ALEF_HAMZA_BELOW,
    HAMZA,
    HAMZA_WAW,
    HAMZA_YA,
]
""" List of Arabic letters """

SIMPLE_HARAKAT: list[str] = [
    FATHA,
    DAMMA,
    KASRA,
    SUKUN,
]
""" Harakat that can be written anywhere in a word"""

TANWEN: list[str] = [
    FATHATAN,
    DAMMATAN,
    KASRATAN,
]
""" Harakat that are written at the end of a word """

HARAKAT: list[str] = [SHADDA] + SIMPLE_HARAKAT + TANWEN
""" Common Harakat """

ALEF_VARIATIONS: list[str] = [
    ALEF,
    ALEF_HAMZA_ABOVE,
    ALEF_HAMZA_BELOW,
    ALEF_MADDA_ABOVE,
    ALEF_HAMZA_ABOVE_WAVY,
    ALEF_HAMZA_BELOW_WAVY,
    ALEF_WASLA,
]
""" Variations of the letter ALEF """

LAM_ALEF_VARIATIONS: list[str] = [
    LAM_ALEF,
    LAM_ALEF_HAMZA_ABOVE,
    LAM_ALEF_HAMZA_BELOW,
    LAM_ALEF_MADDA_ABOVE,
]
""" Variations of the one-letter LAM_ALEF """

LAM_ALEF_VARIATIONS_NORMALIZED: list[str] = [
    LAM + ALEF,
    LAM + ALEF_HAMZA_ABOVE,
    LAM + ALEF_HAMZA_BELOW,
    LAM + ALEF_MADDA_ABOVE,
]
""" Normalized variations of the one-letter LAM_ALEF """

WAW_VARIATIONS: list[str] = [
    WAW,
    SMALL_WAW,
    HAMZA_WAW,
]
""" Variations of the letter WAW """

YEH_VARIATIONS: list[str] = [
    YEH,
    ALEF_MAKSURA,
    HAMZA_YA,
    SMALL_YEH,
]
""" Variations of the letter YEH """

ARABIC_NUMBERS: list[str] = [
    ARABIC_ZERO,
    ARABIC_ONE,
    ARABIC_TWO,
    ARABIC_THREE,
    ARABIC_FOUR,
    ARABIC_FIVE,
    ARABIC_SIX,
    ARABIC_SEVEN,
    ARABIC_EIGHT,
    ARABIC_NINE,
]
""" List of eastern Arabic numerals, a.k.a Indic numerals  """

ARABIC_PUNCTUATIONS: list[str] = [
    ARABIC_COMMA,
    ARABIC_SEMICOLON,
    ARABIC_QUESTION_MARK,
    TRIPLE_DOT,
    STAR,
    ARABIC_FULL_STOP,
    DATE_SEPARATOR,
    ARABIC_DECIMAL_SEPARATOR,
    ARABIC_THOUSANDS_SEPARATOR,
    END_OF_AYAH,
    MISRA_SIGN,
    POETIC_VERSE_SIGN,
    SAJDAH,
    HIZB_START,
    ORNATE_LEFT_PARENTHESIS,
    ORNATE_RIGHT_PARENTHESIS,
]
""" Arabic punctuations. """

ARABIC_LIGATURES: list[str] = [
    LIGATURE_SALLA_KORANIC,
    LIGATURE_QALA,
    LIGATURE_ALLAH,
    LIGATURE_AKBAR,
    LIGATURE_MOHAMMAD,
    LIGATURE_SALAM,
    LIGATURE_RASOUL,
    LIGATURE_ALAYHE,
    LIGATURE_WASALLAM,
    LIGATURE_SALLA,
    LIGATURE_SALLALLAHOU,
    LIGATURE_JALLAJALALOUHOU,
    LIGATURE_RIAL,
    LIGATURE_BISMILLAH,
]
""" Arabic word ligatures. """

ARABIC_LIGATURES_NORMALIZED: list[str] = [
    "صلى",
    "قلى",
    "الله",
    "اكبر",
    "محمد",
    "صلى الله عليه وسلم",
    "رسول",
    "عليه",
    "وسلم",
    "صلى",
    "صلى الله عليه وسلم",
    "جل جلاله",
    "ريال",
    "بسم الله الرحمن الرحيم",
]
""" Arabic normalized word ligatures. """

SMALL_HARAKAT: list[str] = [
    SMALL_TAH,
    SMALL_LAM_ALEF_YEH,
    SMALL_ZAIN,
    SMALL_FATHA,
    SMALL_DAMMA,
    SMALL_KASRA,
    SMALL_LAM_ALEF_HIGH,
    SMALL_JEEM_HIGH,
    SMALL_THREE_DOTS_HIGH,
    SMALL_MEEM_HIGH_ISOLATED,
    SMALL_MEEM_HIGH_INITIAL,
    SMALL_MEEM_LOW,
    SMALL_SEEN_LOW,
    SMALL_SEEN_HIGH,
    SMALL_ZERO_ROUNDED_HIGH,
    SMALL_ZERO_RECTANGULAR_HIGH,
    SMALL_DOTLESS_HEAD_HIGH,
    SMALL_MADDA,
    SMALL_YEH_HIGH,
    SMALL_NOON,
    SMALL_V,
    SMALL_V_INVERTED,
    SMALL_LIGATURE_SALLA_KORANIC,
    SMALL_LIGATURE_QALA,
]
""" Small harakat """

OTHER_HARAKAT: list[str] = [
    SAD_SIGN,
    AIN_SIGN,
    RAHMATULLAH_SIGN,
    RADI_SIGN,
    TAKHALLUS,
    MADDAH_ABOVE,
    HAMZA_ABOVE,
    HAMZA_BELOW,
    ALEF_SUBSCRIPT,
    ALEF_SUPERSCRIPT,
    DAMMA_INVERTED,
    NOON_MARK,
    ZWARAKAY,
    DOT_BELOW,
    DAMMA_REVERSED,
    PERCENTAGE_ABOVE,
    HAMZA_BELOW_WAVY,
    LOW_STOP,
    HIGH_STOP,
    HIGH_STOP_FILLED,
]
""" Other harakat """

ALL_HARAKAT = HARAKAT + SMALL_HARAKAT + OTHER_HARAKAT
""" All harakat from the unicode block 0600–06FF """

ARABIC: list[str] = ARABIC_LETTERS + ALL_HARAKAT + ARABIC_NUMBERS + ARABIC_PUNCTUATIONS
""" Common Arabic characters """

ARABIC_DOTLESS_MAP: dict[str, str] = {
    BEH: DOTLESS_BEH,
    TEH: DOTLESS_TEH,
    THEH: DOTLESS_THEH,
    JEEM: DOTLESS_JEEM,
    KHAH: DOTLESS_KHAH,
    THAL: DOTLESS_THAL,
    ZAIN: DOTLESS_ZAIN,
    SHEEN: DOTLESS_SHEEN,
    DAD: DOTLESS_DAD,
    ZAH: DOTLESS_ZAH,
    GHAIN: DOTLESS_GHAIN,
    FEH: DOTLESS_FEH,
    QAF: DOTLESS_QAF,
    NOON: DOTLESS_TEH,
    YEH: DOTLESS_YEH,
    TEH_MARBUTA: DOTLESS_TEH_MARBUTA,
}
""" Mapping between Arabic dotted and dotless letters """
