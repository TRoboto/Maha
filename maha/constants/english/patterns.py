""" Regular expersion patterns for English """

import re

from ..general import PUNCTUATIONS
from .compound import ENGLISH_LETTERS, ENGLISH_NUMBERS
from .simple import AND_SIGN, AT_SIGN, HASHTAG, UNDERSCORE

PATTERN_ENGLISH_HASHTAGS: str = r"(?<=\s|^|\n|{})(#(?:[{}_]-?)+)\b".format(
    "|".join(
        [
            re.escape(pun)
            for pun in PUNCTUATIONS
            if pun not in [AT_SIGN, AND_SIGN, UNDERSCORE]
        ]
    ),
    "".join(ENGLISH_LETTERS + ENGLISH_NUMBERS),
)
""" Pattern that matches English hashtags """
PATTERN_ENGLISH_MENTIONS: str = PATTERN_ENGLISH_HASHTAGS.replace(
    AT_SIGN, HASHTAG
).replace(HASHTAG, AT_SIGN)
""" Pattern that matches English mentions """
