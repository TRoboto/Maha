""" Regular expersion patterns for Arabic """

__all__ = ["EXPRESSION_ARABIC_HASHTAGS", "EXPRESSION_ARABIC_MENTIONS"]
import re

from maha.constants import (
    ALL_HARAKAT,
    AND_SIGN,
    ARABIC_LETTERS,
    ARABIC_NUMBERS,
    AT_SIGN,
    ENGLISH_NUMBERS,
    HASHTAG,
    PUNCTUATIONS,
    TATWEEL,
    UNDERSCORE,
)
from maha.rexy import Expression

EXPRESSION_ARABIC_HASHTAGS = Expression(
    r"(?<=\s|^|\n|{})(#(?:[{}_][-{}]?)+)\b".format(
        "|".join(
            [
                re.escape(pun)
                for pun in PUNCTUATIONS
                if pun not in [AT_SIGN, AND_SIGN, UNDERSCORE]
            ]
        ),
        "".join(ARABIC_LETTERS + ALL_HARAKAT + ARABIC_NUMBERS) + TATWEEL,
        "".join(ENGLISH_NUMBERS),
    )
)
""" Expression that matches Arabic hashtags """

EXPRESSION_ARABIC_MENTIONS = Expression(
    EXPRESSION_ARABIC_HASHTAGS.pattern.replace(HASHTAG, AT_SIGN)
)
""" Expression that matches Arabic mentions """
