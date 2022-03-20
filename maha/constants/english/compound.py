"""List of English constant definitions."""

from __future__ import annotations

from .simple import *

ENGLISH_SMALL_LETTERS: list[str] = [
    SMALL_A,
    SMALL_B,
    SMALL_C,
    SMALL_D,
    SMALL_E,
    SMALL_F,
    SMALL_G,
    SMALL_H,
    SMALL_I,
    SMALL_J,
    SMALL_K,
    SMALL_L,
    SMALL_M,
    SMALL_N,
    SMALL_O,
    SMALL_P,
    SMALL_Q,
    SMALL_R,
    SMALL_S,
    SMALL_T,
    SMALL_U,
    SMALL_V,
    SMALL_W,
    SMALL_X,
    SMALL_Y,
    SMALL_Z,
]
""" List of all small English letters"""

ENGLISH_CAPITAL_LETTERS: list[str] = [
    A,
    B,
    C,
    D,
    E,
    F,
    G,
    H,
    I,
    J,
    K,
    L,
    M,
    N,
    O,
    P,
    Q,
    R,
    S,
    T,
    U,
    V,
    W,
    X,
    Y,
    Z,
]
""" List of all capital English letters"""

ENGLISH_LETTERS: list[str] = ENGLISH_CAPITAL_LETTERS + ENGLISH_SMALL_LETTERS
""" List of all English letters"""

ENGLISH_NUMBERS: list[str] = [
    ZERO,
    ONE,
    TWO,
    THREE,
    FOUR,
    FIVE,
    SIX,
    SEVEN,
    EIGHT,
    NINE,
]
""" List of western Arabic numerals, a.k.a Arabic numerals"""

ENGLISH_PUNCTUATIONS: list[str] = [
    EXCLAMATION_MARK,
    QUOTATION_MARK,
    NUMBER_SIGN,
    DOLLAR_SIGN,
    PERCENT_SIGN,
    AND_SIGN,
    APOSTROPHE,
    LEFT_PARENTHESIS,
    RIGHT_PARENTHESIS,
    ASTERISK,
    PLUS_SIGN,
    COMMA,
    MINUS_SIGN,
    DOT,
    SLASH,
    COLON,
    SEMICOLON,
    LESSTHAN_SIGN,
    EQUAL_SIGN,
    GREATERTHAN_SIGN,
    QUESTION_MARK,
    AT_SIGN,
    LEFT_BRACKET,
    BACKSLASH,
    RIGHT_BRACKET,
    EXPONENT_SIGN,
    UNDERSCORE,
    GRAVE_ACCENT,
    LEFTCURLY_BRACKET,
    VERTICAL_BAR,
    RIGHTCURLY_BRACKET,
    TILDE,
]
""" List of English punctuations"""

ENGLISH: list[str] = ENGLISH_LETTERS + ENGLISH_NUMBERS + ENGLISH_PUNCTUATIONS
""" Common ENGLISH characters """
