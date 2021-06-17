""" Regular expersion patterns for Arabic """

PATTERN_ARABIC_HASHTAGS: str = (
    r"(?<=\s|^|\*|\n)(#[0-9_أ-ي][-أ-ي_][-0-9أ-ي_]*)(?=\s| |$)"
)
""" Pattern that matches Arabic hashtags """

PATTERN_ARABIC_MENTIONS = r"(?<=\s|^|\*|\n)(@[0-9_أ-ي][-أ-ي_][-0-9أ-ي_]*)(?=\s| |$)"
""" Pattern that matches Arabic mentions """
