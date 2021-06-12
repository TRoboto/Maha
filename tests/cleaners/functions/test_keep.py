import pytest

from maha.cleaners.functions import (
    keep,
    keep_arabic_characters,
    keep_arabic_letters,
    keep_arabic_letters_with_harakat,
    keep_arabic_with_english_numbers,
    keep_characters,
)
from maha.constants import ARABIC_LETTERS, ARABIC_NUMBERS, BEH, DOT, SEEN, SPACE


def test_keep_with_arabic(simple_text_input: str):
    assert (
        keep(text=simple_text_input, arabic=True)
        == "بِسْمِ،اللَّهِ الرَّحْمَنِ الرَّحِيمِ"
    )


def test_keep_with_english(simple_text_input: str):
    assert (
        keep(text=simple_text_input, english=True)
        == "1. In the name of Allah,Most Gracious, Most Merciful."
    )


def test_keep_with_arabic_letters(simple_text_input: str):
    assert keep(text=simple_text_input, arabic_letters=True) == "بسم الله الرحمن الرحيم"


def test_keep_with_english_letters(simple_text_input: str):
    assert (
        keep(text=simple_text_input, english_letters=True)
        == "In the name of Allah Most Gracious Most Merciful"
    )


def test_keep_with_english_letters_and_false_use_space(simple_text_input: str):
    assert (
        keep(
            text=simple_text_input,
            english_letters=True,
            custom_chars=SPACE,
            use_space=False,
        )
        == "In the name of AllahMost Gracious Most Merciful"
    )


def test_keep_with_english_small_letters(simple_text_input: str):
    assert (
        keep(text=simple_text_input, english_small_letters=True)
        == "n the name of llah ost racious ost erciful"
    )


def test_keep_with_english_capital_letters(simple_text_input: str):
    assert keep(text=simple_text_input, english_capital_letters=True) == "I A M G M M"


def test_keep_with_numbers(simple_text_input: str):
    assert keep(text=simple_text_input, numbers=True) == "1"


def test_keep_with_harakat(simple_text_input: str):
    assert keep(text=simple_text_input, harakat=True) == "ِ ْ ِ َّ ِ َّ ْ َ ِ َّ ِ ِ"


def test_keep_with_all_harakat(simple_text_input: str):
    assert (
        keep(text=simple_text_input, all_harakat=True) == "ِ ْ ِ َّ ِ َّ ْ َٰ ِ َّ ِ ِ"
    )


def test_keep_with_punctuations(simple_text_input: str):
    assert keep(text=simple_text_input, punctuations=True) == ". ، , , ."


def test_keep_with_arabic_numbers(simple_text_input: str):
    assert keep(text=simple_text_input, arabic_numbers=True) == ""


def test_keep_with_english_numbers(simple_text_input: str):
    assert keep(text=simple_text_input, english_numbers=True) == "1"


def test_keep_with_arabic_punctuations(simple_text_input: str):
    assert keep(text=simple_text_input, arabic_punctuations=True) == "،"


def test_keep_with_english_punctuations(simple_text_input: str):
    assert keep(text=simple_text_input, english_punctuations=True) == ". , , ."


def test_keep_with_custom_characters(simple_text_input: str):
    assert keep(text=simple_text_input, custom_chars=list("l3g")) == "ll l"


def test_keep_should_raise_valueerror(simple_text_input: str):
    with pytest.raises(ValueError):
        keep("", arabic=True)

    with pytest.raises(ValueError):
        keep(simple_text_input)


def test_keep_with_arabic_letters_and_harakat(simple_text_input: str):
    assert (
        keep(simple_text_input, arabic_letters=True, harakat=True)
    ) == "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"


def test_keep_with_english_letters_and_english_numbers_and_dot(simple_text_input: str):
    assert (
        keep(
            simple_text_input,
            english_letters=True,
            english_numbers=True,
            custom_chars=DOT,
        )
    ) == "1. In the name of Allah Most Gracious Most Merciful."


def test_keep_arabic_letters(simple_text_input: str):
    assert keep_arabic_letters(text=simple_text_input) == "بسم الله الرحمن الرحيم"


def test_keep_arabic_characters(simple_text_input: str):
    assert (
        keep_arabic_characters(text=simple_text_input)
        == "بِسْمِ،اللَّهِ الرَّحْمَنِ الرَّحِيمِ"
    )


def test_keep_arabic_with_english_numbers(simple_text_input: str):
    assert (
        keep_arabic_with_english_numbers(text=simple_text_input)
        == "1 بِسْمِ،اللَّهِ الرَّحْمَنِ الرَّحِيمِ"
    )


def test_keep_arabic_letters_with_harakat(simple_text_input: str):
    assert (
        keep_arabic_letters_with_harakat(simple_text_input)
    ) == "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ"


@pytest.mark.parametrize(
    "expected, keep_chars, use_space",
    [
        ("بسمالله الرحمن الرحيم", ARABIC_LETTERS + [SPACE], False),
        ("بسم الله الرحمن الرحيم", ARABIC_LETTERS, True),
        ("بسماللهالرحمنالرحيم", ARABIC_LETTERS, False),
        ("", ARABIC_NUMBERS, True),
        ("ب", BEH, True),
        ("ب", BEH, False),
        ("بس", BEH + SEEN, False),
    ],
)
def test_keep_characters(
    simple_text_input: str, keep_chars: str, expected: str, use_space: bool
):
    assert keep_characters(simple_text_input, keep_chars, use_space) == expected


def test_keep_characters_raise_valueerror(simple_text_input: str):
    with pytest.raises(ValueError):
        keep_characters(simple_text_input, "")
