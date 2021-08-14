""" Regular expersion patterns for English """

__all__ = ["EXPRESSION_ENGLISH_HASHTAGS", "EXPRESSION_ENGLISH_MENTIONS"]

import re

from maha.constants import (
    AND_SIGN,
    AT_SIGN,
    ENGLISH_LETTERS,
    ENGLISH_NUMBERS,
    HASHTAG,
    PUNCTUATIONS,
    UNDERSCORE,
)
from maha.rexy import Expression

EXPRESSION_ENGLISH_HASHTAGS = Expression(
    r"(?<=\s|^|\n|{})(#(?:[{}_]-?)+)\b".format(
        "|".join(
            [
                re.escape(pun)
                for pun in PUNCTUATIONS
                if pun not in [AT_SIGN, AND_SIGN, UNDERSCORE]
            ]
        ),
        "".join(ENGLISH_LETTERS + ENGLISH_NUMBERS),
    )
)
""" Expression that matches English hashtags """

EXPRESSION_ENGLISH_MENTIONS = Expression(
    EXPRESSION_ENGLISH_HASHTAGS.pattern.replace(HASHTAG, AT_SIGN)
)
""" Expression that matches English mentions """
