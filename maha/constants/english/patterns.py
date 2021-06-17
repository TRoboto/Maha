""" Regular expersion patterns for English """

PATTERN_ENGLISH_HASHTAGS: str = r"(?<=\s|^|\*|\n)(#\w[-a-zA-Z0-9_][-\w_]*)(?=\s| |$)"
""" Pattern that matches English hashtags """
PATTERN_ENGLISH_MENTIONS: str = r"(?<=\s|^|\*|\n)(@\w[-a-zA-Z0-9_][-\w_]*)(?=\s| |$)"
""" Pattern that matches English mentions """
