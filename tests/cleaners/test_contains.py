import pytest

from maha.cleaners.functions import (
    contain_strings,
    contains,
    contains_expressions,
    contains_repeated_substring,
    contains_single_letter_word,
)
from maha.constants import EMPTY
from maha.expressions import EXPRESSION_EMAILS
from maha.rexy import Expression, ExpressionGroup
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


def test_contains_with_operator_and(simple_text_input: str):
    assert is_false(
        contains(simple_text_input, punctuations=True, hashtags=True, operator="and")
    )


def test_contains_with_operator_or(simple_text_input: str):
    assert is_true(
        contains(simple_text_input, punctuations=True, hashtags=True, operator="or")
    )


def test_contains_with_operator_raises_valueerror(simple_text_input: str):
    with pytest.raises(ValueError):
        contains(simple_text_input, hashtags=True, operator="xor")
    with pytest.raises(ValueError):
        contains(simple_text_input, punctuations=True, hashtags=True, operator="")


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
    "expression, expected",
    [
        (Expression("[A-F]"), True),
        (ExpressionGroup(Expression("[A-F]")), True),
        (EXPRESSION_EMAILS, False),
        (ExpressionGroup(EXPRESSION_EMAILS), False),
    ],
)
def test_contains_with_custom_expressions(
    simple_text_input: str, expression, expected: bool
):
    assert contains(simple_text_input, custom_expressions=expression) == expected


def test_contains_with_multiple_inputs(simple_text_input: str):
    output = contains(
        simple_text_input, arabic=True, harakat=True, arabic_hashtags=True
    )

    assert type(output) is dict
    assert len(output) == 3
    assert is_true(output["arabic"])
    assert is_true(output["harakat"])
    assert is_false(output["arabic_hashtags"])


def test_contains_with_empty_string():
    assert contains(EMPTY) == False


def test_contains_raises_value_error(simple_text_input: str):
    with pytest.raises(ValueError):
        contains(simple_text_input)


def test_contains_expressions():
    assert is_true(contains_expressions("email@web.com", EXPRESSION_EMAILS))
    assert is_false(contains_expressions("web.com", EXPRESSION_EMAILS))


def test_contains_expressions_raises_value_error(simple_text_input: str):
    with pytest.raises(ValueError):
        contains_expressions(simple_text_input, True)  # type: ignore


@pytest.mark.parametrize(
    "input, expected",
    [
        ("a", True),
        ("و", True),
        ("ك ", True),
        (" و", True),
        ("محمد و احمد", True),
        ("محمد و", True),
        ("how r u", True),
        ("how r you", True),
        ("how are u", True),
        ("number 1", False),
        ("how are yo", False),
        ("محمد واحمد", False),
        ("ﷺ", False),
    ],
)
def test_contains_single_letter_word_with_arabic_and_english_letters(
    input: str, expected: bool
):
    assert (
        contains_single_letter_word(input, arabic_letters=True, english_letters=True)
        == expected
    )


@pytest.mark.parametrize(
    "input, expected",
    [
        ("a", False),
        ("و", True),
        ("ك ", True),
        (" و", True),
        ("محمد و احمد", True),
        ("محمد و", True),
        ("how r u", False),
        ("how are u", False),
        ("محمد واحمد", False),
    ],
)
def test_contains_single_letter_word_with_arabic_letters(input: str, expected: bool):
    assert contains_single_letter_word(input, arabic_letters=True) == expected


def test_contains_single_letter_word_raises_valueerror():
    with pytest.raises(ValueError):
        contains_single_letter_word("")


@pytest.mark.parametrize(
    "input, expected",
    [
        ("I", True),
        ("I ", True),
        (" I", True),
        ("محمد و احمد", False),
        ("محمد و", False),
        ("how r u", True),
        ("how r you", True),
        ("how are u", True),
        ("number 1", False),
        ("how are yo", False),
    ],
)
def test_contains_single_letter_word_with_english_letters(input: str, expected: bool):
    assert contains_single_letter_word(input, english_letters=True) == expected


def test_contain_strings(simple_text_input: str):
    assert is_true(contain_strings(simple_text_input, "Most"))
    assert is_false(contain_strings(simple_text_input, ["most", "J"]))


def test_contain_strings_raises_value_error(simple_text_input: str):
    with pytest.raises(ValueError):
        contain_strings(simple_text_input, EMPTY)
