import pytest

from maha.cleaners.functions import keep_characters
from maha.constants import ARABIC_CHARS, ARABIC_NUMBERS, BEH, SPACE


@pytest.mark.parametrize(
    "expected, keep_chars, use_space",
    [
        ("بسمالله الرحمن الرحيم", ARABIC_CHARS + [SPACE], False),
        ("بسم الله الرحمن الرحيم", ARABIC_CHARS, True),
        ("بسماللهالرحمنالرحيم", ARABIC_CHARS, False),
        ("", ARABIC_NUMBERS, True),
        ("ب", BEH, True),
        ("ب", BEH, False),
    ],
)
def test_keep_characters(
    simple_text_input: str, keep_chars: str, expected: str, use_space: bool
):
    assert keep_characters(simple_text_input, keep_chars, use_space) == expected
