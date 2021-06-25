import pytest

from maha.cleaners.functions import (
    contain_strings,
    contains,
    contains_patterns,
    contains_repeated_substring,
)
from maha.constants import PATTERN_EMAILS
from tests.utils import is_false, is_true


def test_contains_with_arabic(simple_text_input: str):
    assert is_true(contains(simple_text_input, arabic=True))


def test_contains_with_english(simple_text_input: str):
    assert is_true(contains(simple_text_input, english=True))


def test_contains_with_arabic_letters(simple_text_input: str):
    assert is_true(contains(simple_text_input, arabic_letters=True))


def test_contains_with_english_letters(simple_text_input: str):
    assert is_true(contains(simple_text_input, english_letters=True))


def test_contains_with_english_small_letters(simple_text_input: str):
    assert is_true(contains(simple_text_input, english_small_letters=True))


def test_contains_with_english_capital_letters(simple_text_input: str):
    assert is_true(contains(simple_text_input, english_capital_letters=True))


def test_contains_with_numbers(simple_text_input: str):
    assert is_true(contains(simple_text_input, numbers=True))


def test_contains_with_harakat(simple_text_input: str):
    assert is_true(contains(simple_text_input, harakat=True))


def test_contains_with_all_harakat(simple_text_input: str):
    assert is_true(contains(simple_text_input, all_harakat=True))


def test_contains_with_tatweel(simple_text_input: str):
    assert is_false(contains(simple_text_input, tatweel=True))
    assert is_true(contains("تطويــل", tatweel=True))


def test_contains_with_lam_alef(simple_text_input: str):
    assert is_false(contains(simple_text_input, lam_alef=True))
    assert is_true(contains("هﻻ", lam_alef=True))
    assert is_false(contains("هﻷ", lam_alef=True))


def test_contains_with_lam_alef_variations(simple_text_input: str):
    assert is_false(contains(simple_text_input, lam_alef_variations=True))
    assert is_true(contains("هﻻ", lam_alef_variations=True))
    assert is_true(contains("هﻷ", lam_alef_variations=True))


def test_contains_with_punctuations(simple_text_input: str):
    assert is_true(contains(simple_text_input, punctuations=True))


def test_contains_with_arabic_numbers(simple_text_input: str):
    assert is_false(contains(simple_text_input, arabic_numbers=True))


def test_contains_with_english_numbers(simple_text_input: str):
    assert is_true(contains(simple_text_input, english_numbers=True))


def test_contains_with_arabic_punctuations(simple_text_input: str):
    assert is_true(contains(simple_text_input, arabic_punctuations=True))


def test_contains_with_english_punctuations(simple_text_input: str):
    assert is_true(contains(simple_text_input, english_punctuations=True))


def test_contains_with_arabic_ligatures(simple_text_input: str):
    assert is_false(contains(simple_text_input, arabic_ligatures=True))


def test_contains_with_persian(simple_text_input: str):
    assert is_false(contains(simple_text_input, persian=True))
    assert is_true(contains(simple_text_input + "گ", persian=True))
    assert is_true(contains("۱", persian=True))


def test_contains_with_arabic_hashtags(simple_text_input: str):
    assert is_false(contains(simple_text_input, arabic_hashtags=True))


def test_contains_with_arabic_mentions(simple_text_input: str):
    assert is_false(contains(simple_text_input, arabic_mentions=True))


def test_contains_with_emails(simple_text_input: str):
    assert is_false(contains(simple_text_input, emails=True))


def test_contains_with_english_hashtags_simple(simple_text_input: str):
    assert is_false(contains(simple_text_input, english_hashtags=True))


def test_contains_with_english_hashtags():
    assert is_true(contains("#hi", english_hashtags=True))


def test_contains_with_english_mentions(simple_text_input: str):
    assert is_false(contains(simple_text_input, english_mentions=True))


def test_contains_with_hashtags(simple_text_input: str):
    assert is_false(contains(simple_text_input, hashtags=True))


def test_contains_with_links(simple_text_input: str):
    assert is_false(contains(simple_text_input, links=True))


def test_contains_with_mentions(simple_text_input: str):
    assert is_false(contains(simple_text_input, mentions=True))


def test_contains_with_emojis(simple_text_input: str):
    assert is_false(contains(simple_text_input, emojis=True))


def test_contains_repeated_substring_simple(simple_text_input: str):
    assert is_false(contains_repeated_substring(simple_text_input))


@pytest.mark.parametrize(
    "input,expected,min_repeated",
    [
        ("", False, 1),
        ("Hellllo", True, 4),
        ("Hellllo", False, 5),
        ("Hi hihihi", True, 3),
        ("هاهاها مضحك", True, 3),
    ],
)
def test_contains_repeated_substring(input: str, expected: bool, min_repeated: int):
    assert contains_repeated_substring(input, min_repeated) is expected


def test_contains_repeated_substring_raise_value_error():
    with pytest.raises(ValueError):
        contains_repeated_substring("", min_repeated=0)


@pytest.mark.parametrize(
    "input, chars, expected",
    [
        ("Hello", "l", True),
        ("Hello", "d", False),
        ("مرحبا", "ر", True),
        ("مرحبا", "ل", False),
    ],
)
def test_contains_with_custom_char(input: str, chars, expected: bool):
    assert contains(input, custom_strings=chars) == expected


@pytest.mark.parametrize(
    "pattern, expected",
    [
        ("[A-F]", True),
        (["[A-F]"], True),
        (PATTERN_EMAILS, False),
        ([PATTERN_EMAILS], False),
    ],
)
def test_contains_with_custom_patterns(
    simple_text_input: str, pattern: str, expected: bool
):
    assert contains(simple_text_input, custom_patterns=pattern) == expected


def test_contains_pattern():
    assert is_true(contains_patterns("email@web.com", PATTERN_EMAILS))
    assert is_false(contains_patterns("web.com", PATTERN_EMAILS))


def test_contain_strings(simple_text_input: str):
    assert is_true(contain_strings(simple_text_input, "Most"))
    assert is_false(contain_strings(simple_text_input, ["most", "J"]))


def test_contains_with_multiple_inputs(simple_text_input: str):
    output = contains(
        simple_text_input, arabic=True, harakat=True, arabic_hashtags=True
    )

    assert type(output) is dict
    assert len(output) == 3
    assert is_true(output["arabic"])
    assert is_true(output["harakat"])
    assert is_false(output["arabic_hashtags"])
