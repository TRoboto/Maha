""" Regular expersion patterns """

from .arabic import (
    ARABIC_COMMA,
    ARABIC_DECIMAL_SEPARATOR,
    ARABIC_NUMBERS,
    ARABIC_THOUSANDS_SEPARATOR,
)
from .english import COMMA, ENGLISH_NUMBERS
from .general import SPACE

PATTERN_HASHTAGS: str = r"(?<=\s|^|\*|\n)(#[\wأ-ي-]+)"
""" Pattern that matches Arabic and English hashtags """

PATTERN_MENTIONS: str = r"(?<=\s|^|\*|\n)(@[\wأ-ي-]+)"
""" Pattern that matches Arabic and English mentions """
# Old: (?:\s|^|\*|\n)(@[\wأ-ي][-أ-يa-zA-Z0-9_][-\wأ-ي_]*)

# Adopted from https://gist.github.com/gruber/8891611
PATTERN_LINKS: str = r"""
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
""" Liberal, Accurate Regex Pattern for Matching Web URLs """

# Adopted from https://emailregex.com/
PATTERN_EMAILS: str = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
""" Pattern that matches emails """

# Adopted from https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
# TODO: Validate that all of these are valid emojis
# TODO: Remove Arabic Ligatures from the list
PATTERN_EMOJIS: str = (
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
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
""" Pattern that matches emojis """

PATTERN_ALL_SPACES: str = r"[\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000\uFEFF]"
"""
Pattern that matches space variations. Normal space is not included.
Taken from: https://jkorpela.fi/chars/spaces.html
"""

PATTERN_INTEGER: str = r"[+-]?(?:[{0}](?:{1})?)+\%?".format(
    "".join(ARABIC_NUMBERS + ENGLISH_NUMBERS),
    "|".join([ARABIC_THOUSANDS_SEPARATOR, ARABIC_COMMA, COMMA, SPACE]),
)
""" Pattern that matches Arabic and English integers """

PATTERN_DECIMAL: str = r"[+-]?(?:[{0}](?:{1})?)*[.{2}](?:[{0}](?:{1})?)+\%?".format(
    "".join(ARABIC_NUMBERS + ENGLISH_NUMBERS),
    "|".join([ARABIC_THOUSANDS_SEPARATOR, ARABIC_COMMA, COMMA, SPACE]),
    ARABIC_DECIMAL_SEPARATOR,
)
""" Pattern that matches Arabic and English decimals """

PATTERN_SPACE: str = r"\s+"
""" Pattern that matches at least one whitespace """

PATTERN_SPACE_OR_NONE: str = r"\s*"
""" Pattern that matches zero or more whitespaces """
