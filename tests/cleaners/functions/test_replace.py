import pytest

from maha.cleaners.functions import (
    convert_arabic_numbers_to_english,
    replace,
    replace_except,
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


def test_replace_pairs_simple(simple_text_input: str):
    processedtext = replace_pairs(
        simple_text_input, ENGLISH_SMALL_LETTERS, ENGLISH_CAPITAL_LETTERS
    )
    assert list_not_in_string(ENGLISH_SMALL_LETTERS, processedtext)


def test_replace_pairs():
    processedtext = replace_pairs("142", ENGLISH_NUMBERS, ARABIC_NUMBERS)
    assert processedtext == ARABIC_ONE + ARABIC_FOUR + ARABIC_TWO


def test_replace_pairs_raises_valueerror():
    with pytest.raises(ValueError):
        replace_pairs("142", ["A", "B"], ["C"])


def test_convert_arabic_numbers_to_english():
    processedtext = convert_arabic_numbers_to_english(
        "".join(ARABIC_NUMBERS) + " simple"
    )
    assert processedtext == "".join(ENGLISH_NUMBERS) + " simple"


def test_replace_pattern(simple_text_input: str):
    processedtext = replace_pattern(simple_text_input, "[^A-Z]", EMPTY)
    assert list_only_in_string(ENGLISH_CAPITAL_LETTERS, processedtext)


def test_replace(simple_text_input: str):
    processedtext = replace(simple_text_input, "Most", "REPLACE")
    assert "REPLACE" in processedtext
    assert "Most" not in processedtext


def test_replace_with_list(simple_text_input: str):
    processedtext = replace(simple_text_input, list("Mma"), "REPLACE")
    assert list_not_in_string(list("Mma"), processedtext)
    assert "REPLACE" in processedtext


def test_replace_except(simple_text_input: str):
    processedtext = replace_except(simple_text_input, "Mma", EMPTY)
    assert list_only_in_string(list("Mma"), processedtext)


def test_replace_except_with_list(simple_text_input: str):
    processedtext = replace_except(simple_text_input, list("Mma"), EMPTY)
    assert list_only_in_string(list("Mma"), processedtext)
