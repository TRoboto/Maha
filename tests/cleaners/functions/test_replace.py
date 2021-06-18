from maha.cleaners.functions import (
    replace_characters,
    replace_characters_except,
    replace_pairs,
    replace_pattern,
)
from maha.constants import (
    ARABIC_FOUR,
    ARABIC_NUMBERS,
    ARABIC_ONE,
    ARABIC_TWO,
    EMPTY,
    ENGLISH_CAPITAL_LETTERS,
    ENGLISH_NUMBERS,
    ENGLISH_SMALL_LETTERS,
)
from tests.utils import list_not_in_string, list_only_in_string


def test_replace_pairs(simple_text_input: str):
    processedtext = replace_pairs(
        simple_text_input, ENGLISH_SMALL_LETTERS, ENGLISH_CAPITAL_LETTERS
    )
    assert list_not_in_string(ENGLISH_SMALL_LETTERS, processedtext)
    assert (
        replace_pairs("142", ENGLISH_NUMBERS, ARABIC_NUMBERS)
        == ARABIC_ONE + ARABIC_FOUR + ARABIC_TWO
    )


def test_replace_pattern(simple_text_input: str):
    processedtext = replace_pattern(simple_text_input, "[^A-Z]", EMPTY)
    assert list_only_in_string(ENGLISH_CAPITAL_LETTERS, processedtext)


def test_replace_characters(simple_text_input: str):
    processedtext = replace_characters(simple_text_input, "Mma", "REPLACE")
    assert list_not_in_string(list("Mma"), processedtext)
    assert "REPLACE" in processedtext


def test_replace_characters_except(simple_text_input: str):
    processedtext = replace_characters_except(simple_text_input, "Mma", EMPTY)
    assert list_only_in_string(list("Mma"), processedtext)
