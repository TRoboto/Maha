import pytest

from maha.constants import (
    ALEF_SUPERSCRIPT,
    ARABIC,
    ARABIC_NUMBERS,
    BEH,
    EMPTY,
    FATHA,
    KASRA,
)
from maha.parsers.functions import parse
from maha.parsers.templates import Dimension, DimensionType
from maha.rexy import Expression, ExpressionGroup
from tests.utils import list_only_in_string


def test_parse_with_no_arguments(simple_text_input):
    with pytest.raises(ValueError):
        parse(simple_text_input)


def test_parse_with_empty_text():
    result = parse(EMPTY, english=True, numbers=True)
    assert result == []


def test_parse_with_return_type(simple_text_input):
    result = parse(simple_text_input, english=True)
    assert isinstance(result, list)
    assert all(isinstance(c, Dimension) for c in result)


def test_parse_correct_return_values(simple_text_input):
    result = parse(simple_text_input, arabic=True)
    assert isinstance(result, list)
    assert list_only_in_string(list("[]+") + ARABIC, result[0].expression.pattern)
    assert len(result) == 3
    assert result[1].start == 19
    assert result[1].end == 31
    assert result[2].dimension_type == DimensionType.ARABIC


def test_parse_with_one_argument(simple_text_input):
    result = parse(simple_text_input, arabic=True)
    assert isinstance(result, list)


def test_parse_with_more_than_one_argument(simple_text_input):
    result = parse(simple_text_input, arabic=True, english=True, emojis=True)
    assert isinstance(result, dict)
    assert len(result) == 3


def test_parse_with_english(simple_text_input):
    result = parse(simple_text_input, english=True)
    assert len(result) == 9


def test_parse_with_arabic_letters(simple_text_input):
    result = parse(simple_text_input, arabic_letters=True)
    assert len(result) == 12
    assert isinstance(result, list)
    assert result[0].value == BEH


def test_parse_with_english_letters(simple_text_input):
    result = parse(simple_text_input, english_letters=True)
    assert len(result) == 9
    assert isinstance(result, list)
    assert result[0].value == "In"


def test_parse_with_english_small_letters(simple_text_input):
    result = parse(simple_text_input, english_small_letters=True)
    assert len(result) == 9
    assert isinstance(result, list)
    assert result[0].value == "n"


def test_parse_with_english_capital_letters(simple_text_input):
    result = parse(simple_text_input, english_capital_letters=True)
    assert len(result) == 6
    assert isinstance(result, list)
    assert result[0].value == "I"


def test_parse_with_numbers(simple_text_input):
    result = parse(simple_text_input, numbers=True)
    assert len(result) == 1
    assert isinstance(result, list)
    assert result[0].value == "1"


def test_parse_with_harakat(simple_text_input):
    result = parse(simple_text_input, harakat=True)
    assert len(result) == 12
    assert isinstance(result, list)
    assert result[0].value == KASRA


def test_parse_with_all_harakat(simple_text_input):
    result = parse(simple_text_input, all_harakat=True)
    assert len(result) == 12
    assert isinstance(result, list)
    assert result[7].value == FATHA + ALEF_SUPERSCRIPT


def test_parse_with_tatweel(simple_text_input):
    result = parse(simple_text_input, tatweel=True)
    assert len(result) == 0


def test_parse_with_punctuations(simple_text_input):
    result = parse(simple_text_input, punctuations=True)
    assert len(result) == 5


def test_parse_with_arabic_numbers(simple_text_input):
    result = parse(simple_text_input, arabic_numbers=True)
    assert len(result) == 0


def test_parse_with_english_numbers(simple_text_input):
    result = parse(simple_text_input, english_numbers=True)
    assert len(result) == 1


def test_parse_with_arabic_punctuations(simple_text_input):
    result = parse(simple_text_input, arabic_punctuations=True)
    assert len(result) == 1


def test_parse_with_english_punctuations(simple_text_input):
    result = parse(simple_text_input, english_punctuations=True)
    assert len(result) == 4


def test_parse_with_arabic_ligatures(multiple_tweets):
    result = parse(multiple_tweets, arabic_ligatures=True)
    assert len(result) == 1


def test_parse_with_arabic_hashtags(multiple_tweets):
    result = parse(multiple_tweets, arabic_hashtags=True)
    assert len(result) == 2


def test_parse_with_arabic_mentions(multiple_tweets):
    result = parse(multiple_tweets, arabic_mentions=True)
    assert len(result) == 0


def test_parse_with_emails(multiple_tweets):
    result = parse(multiple_tweets, emails=True)
    assert len(result) == 0
    result = parse("a@gmail.com", emails=True)
    assert len(result) == 1


def test_parse_with_english_hashtags(multiple_tweets):
    result = parse(multiple_tweets, english_hashtags=True)
    assert len(result) == 4


def test_parse_with_english_mentions(multiple_tweets):
    result = parse(multiple_tweets, english_mentions=True)
    assert len(result) == 0


def test_parse_with_hashtags(multiple_tweets):
    result = parse(multiple_tweets, hashtags=True)
    assert len(result) == 6


def test_parse_with_links(multiple_tweets):
    result = parse(multiple_tweets, links=True)
    assert len(result) == 0
    result = parse("google.com", links=True)
    assert len(result) == 1


def test_parse_with_mentions(multiple_tweets):
    result = parse(multiple_tweets, mentions=True)
    assert len(result) == 0


def test_parse_with_emojis(multiple_tweets):
    result = parse(multiple_tweets, emojis=True)
    assert len(result) == 5


def test_parse_with_custom_expressions(multiple_tweets):
    exp = r"الساع[ةه] ([{}]+)".format("".join(ARABIC_NUMBERS))
    result = parse(multiple_tweets, custom_expressions=Expression(exp))
    assert len(result) == 1
    assert isinstance(result, list)
    assert result[0].value == "١"
    assert result[0].expression.pattern == exp


def test_parse_with_mutiple_expressions(multiple_tweets):
    exp1 = r"الساع[ةه] ([{}]+)".format("".join(ARABIC_NUMBERS))
    exp2 = r"(\d+) days"
    result = parse(
        multiple_tweets,
        custom_expressions=ExpressionGroup(Expression(exp1), Expression(exp2)),
    )
    assert len(result) == 2
    assert isinstance(result, list)
    assert result[0].value == "١"
    assert result[1].value == "10"


def test_parse_raises_value_error_with_invalid_expression():
    with pytest.raises(ValueError):
        parse("test", custom_expressions=Expression(""))


def test_dimesion_output():
    d = Dimension(Expression(" test "), "test", 1, 10, 17, DimensionType.GENERAL)
    assert str(d) == (
        "Dimension(body=test, value=1, start=10, end=17, "
        "dimension_type=DimensionType.GENERAL)"
    )
