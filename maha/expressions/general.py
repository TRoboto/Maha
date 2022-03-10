""" Regular expersion patterns """


__all__ = [
    "EXPRESSION_HASHTAGS",
    "EXPRESSION_MENTIONS",
    "EXPRESSION_LINKS",
    "EXPRESSION_EMAILS",
    "EXPRESSION_EMOJIS",
    "EXPRESSION_ALL_SPACES",
    "EXPRESSION_INTEGER",
    "EXPRESSION_DECIMAL",
    "EXPRESSION_SPACE",
    "EXPRESSION_SPACE_OR_NONE",
]

import re

from maha.constants import (
    AND_SIGN,
    ARABIC_COMMA,
    ARABIC_DECIMAL_SEPARATOR,
    ARABIC_NUMBERS,
    ARABIC_THOUSANDS_SEPARATOR,
    AT_SIGN,
    COMMA,
    ENGLISH_NUMBERS,
    HASHTAG,
    PUNCTUATIONS,
    SPACE,
    UNDERSCORE,
)
from maha.rexy import Expression

EXPRESSION_HASHTAGS = Expression(
    r"(?<=\s|^|\n|{})(#[\w-]+)\b".format(
        "|".join(
            [
                re.escape(pun)
                for pun in PUNCTUATIONS
                if pun not in [AT_SIGN, AND_SIGN, UNDERSCORE]
            ]
        ),
    )
)
""" Expression that matches hashtags """


EXPRESSION_MENTIONS = Expression(EXPRESSION_HASHTAGS.pattern.replace(HASHTAG, AT_SIGN))
""" Expression that matches mentions """

# Adopted from https://gist.github.com/gruber/8891611
EXPRESSION_LINKS = Expression(
    r"""
(?xi)
\b
(							# Capture 1: entire matched URL
  (?:
    https?:				# URL protocol and colon
    (?:
      /{1,3}						# 1-3 slashes
      |								#   or
      [a-z0-9%]						# Single letter or digit or '%'
      								# (Trying not to match e.g. "URI::Escape")
    )
    |							#   or
    							# looks like domain name followed by a slash:
    [a-z0-9.\-]+[.]
    (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
    /
  )
  (?:							# One or more:
    [^\s()<>{}\[\]]+						# Run of non-space, non-()<>{}[]
    |								#   or
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
    |
    \([^\s]+?\)							# balanced parens, non-recursive: (…)
  )+
  (?:							# End with:
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\)  # balanced parens, one level deep: (…(…)…)
    |
    \([^\s]+?\)							# balanced parens, non-recursive: (…)
    |									#   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]		# not a space or one of these punct chars
  )
  |					# OR, the following to match naked domains:
  (?:
  	(?<!@)			# not preceded by a @, avoid matching foo@_gmail.com_
    [a-z0-9]+
    (?:[.\-][a-z0-9]+)*
    [.]
    (?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj| Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)
    \b
    /?
    (?!@)			# not succeeded by a @, avoid matching "foo.na" in "foo.na@example.com"
  )
)
"""
)
""" Liberal, Accurate Regex Expression for Matching Web URLs """

# Adopted from https://emailregex.com/
EXPRESSION_EMAILS = Expression(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
""" Expression that matches emails """

# Adopted from https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
# TODO: Validate that all of these are valid emojis
EXPRESSION_EMOJIS = Expression(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0000FDEF"
    "\U0000FDFE-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "]+"
)
""" Expression that matches emojis """

EXPRESSION_ALL_SPACES = Expression(
    r"[\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000\uFEFF]"
)
"""
Expression that matches space variations. Normal space is not included.
Taken from: https://jkorpela.fi/chars/spaces.html
"""

EXPRESSION_INTEGER = Expression(
    r"[+-]?(?:[{}](?:{})?)+%?".format(
        "".join(ARABIC_NUMBERS + ENGLISH_NUMBERS),
        "|".join([ARABIC_THOUSANDS_SEPARATOR, ARABIC_COMMA, COMMA, r"\s+\d"]),
    )
)
""" Expression that matches Arabic and English integers """

EXPRESSION_DECIMAL = Expression(
    r"[+-]?(?:[{0}](?:{1})?)*[.{2}](?:[{0}](?:{1})?)+%?".format(
        "".join(ARABIC_NUMBERS + ENGLISH_NUMBERS),
        "|".join([ARABIC_THOUSANDS_SEPARATOR, ARABIC_COMMA, COMMA, r"\s+\d"]),
        ARABIC_DECIMAL_SEPARATOR,
    )
)
""" Expression that matches Arabic and English decimals """

EXPRESSION_SPACE = Expression(r"\s+")
""" Expression that matches at least one whitespace """

EXPRESSION_SPACE_OR_NONE = Expression(r"\s*")
""" Expression that matches zero or more whitespaces """
