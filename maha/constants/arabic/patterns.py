""" Regular expersion patterns for Arabic """

import re

from ..english import AND_SIGN, AT_SIGN, ENGLISH_NUMBERS, HASHTAG, UNDERSCORE
from ..general import PUNCTUATIONS
from .compound import ALL_HARAKAT, ARABIC_LETTERS, ARABIC_NUMBERS
from .simple import TATWEEL

PATTERN_ARABIC_HASHTAGS: str = r"(?<=\s|^|\n|{})(#(?:[{}_][-{}]?)+)\b".format(
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
""" Pattern that matches Arabic hashtags """

PATTERN_ARABIC_MENTIONS = PATTERN_ARABIC_HASHTAGS.replace(AT_SIGN, HASHTAG).replace(
    HASHTAG, AT_SIGN
)
""" Pattern that matches Arabic mentions """
