import pytest

from maha.cleaners.functions import (
    remove,
    remove_all_harakat,
    remove_characters,
    remove_english,
    remove_extra_spaces,
    remove_harakat,
    remove_numbers,
    remove_punctuations,
)
from maha.constants import (
    ALL_HARAKAT,
    ARABIC,
    ARABIC_LETTERS,
    ARABIC_NUMBERS,
    ARABIC_PUNCTUATIONS,
    ENGLISH,
    ENGLISH_CAPITAL_LETTERS,
    ENGLISH_LETTERS,
    ENGLISH_NUMBERS,
    ENGLISH_PUNCTUATIONS,
    ENGLISH_SMALL_LETTERS,
    HARAKAT,
    NUMBERS,
    PUNCTUATIONS,
)
from tests.utils import list_not_in_string


def test_remove_with_arabic(simple_text_input: str):
    processed_text = remove(text=simple_text_input, arabic=True)
    assert processed_text == "1. In the name of Allah,Most Gracious, Most Merciful."
    assert list_not_in_string(ARABIC, processed_text)


def test_remove_with_english(simple_text_input: str):
    processed_text = remove(text=simple_text_input, english=True)
    assert processed_text == "بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    assert list_not_in_string(ENGLISH, processed_text)


def test_remove_english(simple_text_input: str):
    processed_text = remove_english(text=simple_text_input)
    assert processed_text == "بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    assert list_not_in_string(ENGLISH, processed_text)


def test_remove_with_false_use_space(simple_text_input: str):
    processed_text = remove(
        text=simple_text_input,
        english=True,
        punctuations=True,
        harakat=True,
        use_space=False,
    )
    assert processed_text == "بسمالله الرحمٰن الرحيم"
    assert list_not_in_string(ENGLISH + PUNCTUATIONS + HARAKAT, processed_text)


def test_remove_with_random_true_inputs(simple_text_input: str):
    processed_text = remove(
        text=simple_text_input,
        english=True,
        punctuations=True,
        all_harakat=True,
    )
    assert processed_text == "بسم الله الرحمن الرحيم"
    assert list_not_in_string(ENGLISH + PUNCTUATIONS + ALL_HARAKAT, processed_text)


def test_remove_with_arabic_letters(simple_text_input: str):
    processed_text = remove(text=simple_text_input, arabic_letters=True)
    assert (
        processed_text
        == "1. ِ ْ ِ، َّ ِ َّ ْ َٰ ِ َّ ِ ِ In the name of Allah,Most Gracious, Most Merciful."
    )
    assert list_not_in_string(ARABIC_LETTERS, processed_text)


def test_remove_with_english_letters(simple_text_input: str):
    processed_text = remove(text=simple_text_input, english_letters=True)

    assert processed_text == "1. بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ , , ."
    assert list_not_in_string(ENGLISH_LETTERS, processed_text)


def test_remove_with_english_small_letters(simple_text_input: str):
    processed_text = remove(text=simple_text_input, english_small_letters=True)
    assert (
        processed_text == "1. بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ I A ,M G , M M ."
    )
    assert list_not_in_string(ENGLISH_SMALL_LETTERS, processed_text)


def test_remove_with_english_capital_letters(simple_text_input: str):
    processed_text = remove(text=simple_text_input, english_capital_letters=True)
    assert (
        processed_text
        == "1. بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ n the name of llah, ost racious, ost erciful."
    )
    assert list_not_in_string(ENGLISH_CAPITAL_LETTERS, processed_text)


def test_remove_with_english_capital_letters_false_use_space(simple_text_input: str):
    processed_text = remove(
        text=simple_text_input, english_capital_letters=True, use_space=False
    )
    assert (
        processed_text
        == "1. بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ n the name of llah,ost racious, ost erciful."
    )
    assert list_not_in_string(ENGLISH_CAPITAL_LETTERS, processed_text)


def test_remove_with_numbers(simple_text_input: str):
    processed_text = remove(text=simple_text_input, numbers=True)
    assert (
        processed_text
        == ". بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In the name of Allah,Most Gracious, Most Merciful."
    )
    assert list_not_in_string(NUMBERS, processed_text)


def test_remove_numbers(simple_text_input: str):
    processed_text = remove_numbers(text=simple_text_input)
    assert (
        processed_text
        == ". بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In the name of Allah,Most Gracious, Most Merciful."
    )
    assert list_not_in_string(NUMBERS, processed_text)


def test_remove_with_harakat(simple_text_input: str):
    processed_text = remove(text=simple_text_input, harakat=True)
    assert (
        processed_text
        == "1. بسم،الله الرحمٰن الرحيم In the name of Allah,Most Gracious, Most Merciful."
    )
    assert list_not_in_string(HARAKAT, processed_text)


def test_remove_harakat(simple_text_input: str):
    processed_text = remove_harakat(text=simple_text_input)
    assert (
        processed_text
        == "1. بسم،الله الرحمٰن الرحيم In the name of Allah,Most Gracious, Most Merciful."
    )
    assert list_not_in_string(HARAKAT, processed_text)


def test_remove_all_harakat(simple_text_input: str):
    processed_text = remove_all_harakat(text=simple_text_input)
    assert (
        processed_text
        == "1. بسم،الله الرحمن الرحيم In the name of Allah,Most Gracious, Most Merciful."
    )
    assert list_not_in_string(ALL_HARAKAT, processed_text)


def test_remove_with_punctuations(simple_text_input: str):
    processed_text = remove(text=simple_text_input, punctuations=True)
    assert (
        processed_text
        == "1 بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In the name of Allah Most Gracious Most Merciful"
    )
    assert list_not_in_string(PUNCTUATIONS, processed_text)


def test_remove_punctuations(simple_text_input: str):
    processed_text = remove_punctuations(text=simple_text_input)
    assert (
        processed_text
        == "1 بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In the name of Allah Most Gracious Most Merciful"
    )
    assert list_not_in_string(PUNCTUATIONS, processed_text)


def test_remove_with_arabic_numbers(simple_text_input: str):
    processed_text = remove(text=simple_text_input, arabic_numbers=True)
    assert processed_text == simple_text_input.strip()
    assert list_not_in_string(ARABIC_NUMBERS, processed_text)


def test_remove_with_english_numbers(simple_text_input: str):
    processed_text = remove(text=simple_text_input, english_numbers=True)
    assert (
        processed_text
        == ". بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In the name of Allah,Most Gracious, Most Merciful."
    )
    assert list_not_in_string(ENGLISH_NUMBERS, processed_text)


def test_remove_with_arabic_punctuations(simple_text_input: str):
    processed_text = remove(text=simple_text_input, arabic_punctuations=True)
    assert (
        processed_text
        == "1. بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In the name of Allah,Most Gracious, Most Merciful."
    )
    assert list_not_in_string(ARABIC_PUNCTUATIONS, processed_text)


def test_remove_with_english_punctuations(simple_text_input: str):
    processed_text = remove(text=simple_text_input, english_punctuations=True)
    assert (
        processed_text
        == "1 بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In the name of Allah Most Gracious Most Merciful"
    )
    assert list_not_in_string(ENGLISH_PUNCTUATIONS, processed_text)


def test_remove_with_custom_characters(simple_text_input: str):
    processed_text = remove(text=simple_text_input, custom_chars="test")
    assert (
        processed_text
        == "1. بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In h nam of Allah,Mo Graciou , Mo M rciful."
    )
    assert list_not_in_string(list("test"), processed_text)


def test_remove_with_hashtags_simple(simple_text_input: str):
    processed_text = remove(text=simple_text_input, hashtags=True)
    assert processed_text == simple_text_input.strip()


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("test", "test"),
        ("# test", "# test"),
        ("#test", ""),
        ("#هاشتاق", ""),
        ("test hashtag #hashtag_mid in middle ", "test hashtag in middle"),
        ("تجربة #هاشتاق3 في النصف", "تجربة في النصف"),
        ("#hashtag_start at start ", "at start"),
        ("#هاشتاق في البداية", "في البداية"),
        ("#hashtag #hashtag more than #hashtag one #hashtag", "more than one"),
        ("#هايشتاقhashtag في البداية", "في البداية"),
        ("#هاشتاق #هاشتاق اكثر من  #هاشتاق واحد #هاشتاق", "اكثر من واحد"),
        ("test at end #hashtag_end3 3 ", "test at end 3"),
        ("في النهاية #هاشتاق3", "في النهاية"),
        ("test at end #34hashtag-end123", "test at end"),
        ("test at endline #hashtag\ntest", "test at endline \ntest"),
        ("#123", ""),
    ],
)
def test_remove_with_hashtag(input_text: str, expected: str):
    processed_text = remove(text=input_text, hashtags=True)
    assert processed_text == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("test", "test"),
        ("# test", "# test"),
        ("#test", ""),
        ("#هاشتاق", "#هاشتاق"),
        ("test hashtag #hashtag_mid in middle ", "test hashtag in middle"),
        ("تجربة #هاشتاق3 في النصف", "تجربة #هاشتاق3 في النصف"),
        ("#hashtag_start at start ", "at start"),
        ("#هاشتاق في البداية", "#هاشتاق في البداية"),
        ("#hashtag #hashtag more than #hashtag one #hashtag", "more than one"),
        ("#هايشتاقhashtag في البداية", "#هايشتاقhashtag في البداية"),
        ("test at end #hashtag_end3 3 ", "test at end 3"),
        ("في النهاية #هاشتاق3", "في النهاية #هاشتاق3"),
        ("test at end #34hashtag-end123", "test at end"),
        ("test at endline #hashtag\ntest", "test at endline \ntest"),
        ("#123", ""),
    ],
)
def test_remove_with_english_hashtag(input_text: str, expected: str):
    processed_text = remove(text=input_text, english_hashtags=True)
    assert processed_text == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("test", "test"),
        ("# test", "# test"),
        ("#test", "#test"),
        ("#منشن", ""),
        ("test hashtag #hashtag_mid in middle ", "test hashtag #hashtag_mid in middle"),
        ("تجربة #هاشتاق3 في النصف", "تجربة في النصف"),
        (
            "#hashtag #hashtag more than #hashtag one #hashtag",
            "#hashtag #hashtag more than #hashtag one #hashtag",
        ),
        ("#هاشتاق #هاشتاق اكثر من  #هاشتاق واحد #هاشتاق", "اكثر من واحد"),
        ("#hashtag_start at start ", "#hashtag_start at start"),
        ("#هاشتاق في البداية", "في البداية"),
        ("#هاشتاقhashtag في البداية", "#هاشتاقhashtag في البداية"),
        ("test at end #hashtag_end3 3 ", "test at end #hashtag_end3 3"),
        ("في النهاية #هاشتاق3", "في النهاية"),
        ("test at end #34hashtag-end123", "test at end #34hashtag-end123"),
        ("test at endline #hashtag\ntest", "test at endline #hashtag\ntest"),
        ("#123", "#123"),
    ],
)
def test_remove_with_arabic_hashtag(input_text: str, expected: str):
    processed_text = remove(text=input_text, arabic_hashtags=True)
    assert processed_text == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("test", "test"),
        ("@ test", "@ test"),
        ("@test", ""),
        ("@منشن", ""),
        ("email@web.com", "email@web.com"),
        ("test mention @mention_mid in middle ", "test mention in middle"),
        ("تجربة @منشن3 في النصف", "تجربة في النصف"),
        ("@mention_start at start ", "at start"),
        ("@منشن في البداية", "في البداية"),
        ("@هايشتاقmention في البداية", "في البداية"),
        ("test at end @mention_end3 3 ", "test at end 3"),
        ("@منشن @منشن اكثر من  @منشن واحد @منشن", "اكثر من واحد"),
        ("في النهاية @منشن3", "في النهاية"),
        ("test at end @34mention-end123", "test at end"),
        ("test at endline @mention\ntest", "test at endline \ntest"),
        ("@123", ""),
        ("@mention @mention more than @mention one @mention", "more than one"),
        ("@منشن @منشن اكثر من  @منشن واحد @منشن", "اكثر من واحد"),
    ],
)
def test_remove_with_mentions(input_text: str, expected: str):
    processed_text = remove(text=input_text, mentions=True)
    assert processed_text == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("test", "test"),
        ("@ test", "@ test"),
        ("@test", ""),
        ("@منشن", "@منشن"),
        ("test mention @mention_mid in middle ", "test mention in middle"),
        ("تجربة @منشن3 في النصف", "تجربة @منشن3 في النصف"),
        ("@mention_start at start ", "at start"),
        ("@منشن في البداية", "@منشن في البداية"),
        ("@mention @mention more than @mention one @mention", "more than one"),
        ("@هايشتاقmention في البداية", "@هايشتاقmention في البداية"),
        ("test at end @mention_end3 3 ", "test at end 3"),
        ("في النهاية @منشن3", "في النهاية @منشن3"),
        ("test at end @34mention-end123", "test at end"),
        ("test at endline @mention\ntest", "test at endline \ntest"),
        ("@123", ""),
    ],
)
def test_remove_with_english_mentions(input_text: str, expected: str):
    processed_text = remove(text=input_text, english_mentions=True)
    assert processed_text == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("test", "test"),
        ("@ test", "@ test"),
        ("@test", "@test"),
        ("@منشن", ""),
        ("email@web.com", "email@web.com"),
        ("test mention @mention_mid in middle", "test mention @mention_mid in middle"),
        ("تجربة @منشن3 في النصف", "تجربة في النصف"),
        ("@mention_start at start", "@mention_start at start"),
        ("@منشن في البداية", "في البداية"),
        ("@هايشتاقmention في البداية", "@هايشتاقmention في البداية"),
        ("test at end @mention_end3 3", "test at end @mention_end3 3"),
        ("@منشن @منشن اكثر من  @منشن واحد @منشن", "اكثر من واحد"),
        ("في النهاية @منشن3", "في النهاية"),
        ("test at end @34mention-end123", "test at end @34mention-end123"),
        ("test at endline @mention\ntest", "test at endline @mention\ntest"),
        ("@123", "@123"),
        ("@منشن @منشن اكثر من  @منشن واحد @منشن", "اكثر من واحد"),
    ],
)
def test_remove_with_arabic_mentions(input_text: str, expected: str):
    processed_text = remove(text=input_text, arabic_mentions=True)
    assert processed_text == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("test", "test"),
        ("@test", "@test"),
        ("email@web.com", ""),
        ("email123-d@web-1.edu.jo", ""),
        ("email@web.co.uk", ""),
        ("email@web", "email@web"),
    ],
)
def test_remove_with_emails(input_text: str, expected: str):
    processed_text = remove(text=input_text, emails=True)
    assert processed_text == expected


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("test", "test"),
        (".test.", ".test."),
        ("web.com", ""),
        ("web-1.edu.jo", ""),
        ("web.co.uk", ""),
        ("www.web.edu.jo", ""),
        ("http://web.edu.jo", ""),
        ("http://www.web.edu.jo", ""),
        ("https://web.edu.jo", ""),
        ("https://www.web.edu.jo", ""),
        ("https://www.web.cooiuty.noo", ""),
        ("www.web.notwebsite.noo", "www.web.notwebsite.noo"),
        ("www.web.website.com", ""),
    ],
)
def test_remove_with_links(input_text: str, expected: str):
    processed_text = remove(text=input_text, links=True)
    assert processed_text == expected


def test_remove_should_raise_valueerror(simple_text_input: str):
    with pytest.raises(ValueError):
        remove("", arabic=True)

    with pytest.raises(ValueError):
        remove(simple_text_input)


def test_remove_with_random_input(simple_text_input: str):
    processed_text = remove(
        simple_text_input, arabic_letters=True, all_harakat=True, punctuations=True
    )
    assert processed_text == "1 In the name of Allah Most Gracious Most Merciful"
    assert list_not_in_string(
        ARABIC_LETTERS + ALL_HARAKAT + PUNCTUATIONS, processed_text
    )


@pytest.mark.parametrize(
    "expected, chars_to_remove, use_space",
    [
        ("بِسْمِاللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", ENGLISH + PUNCTUATIONS, False),
        ("1. In the name of Allah,Most Gracious, Most Merciful.", ARABIC, True),
        ("1.    In the name of Allah,Most Gracious, Most Merciful.", ARABIC, False),
    ],
)
def test_remove_characters(
    simple_text_input: str, chars_to_remove: str, expected: str, use_space: bool
):
    assert remove_characters(simple_text_input, chars_to_remove, use_space) == expected


def test_remove_characters_raise_valueerror(simple_text_input: str):
    with pytest.raises(ValueError):
        remove_characters(simple_text_input, "")


@pytest.mark.parametrize(
    "input, expected, max_keep",
    [
        ("", "", 1),
        ("   ", "  ", 2),
        ("test remove extra spaces", "test remove extra spaces", 1),
        ("  test   remove extra  spaces  ", " test remove extra spaces ", 1),
        ("   test    remove extra  spaces ", "   test    remove extra  spaces ", 5),
    ],
)
def test_remove_extra_spaces(input: str, expected: str, max_keep: int):
    assert remove_extra_spaces(input, max_keep) == expected


def test_remove_extra_spaces_raise_valueerror():
    with pytest.raises(ValueError):
        remove_extra_spaces("", -5)

    with pytest.raises(ValueError):
        remove_extra_spaces("", 4.5)

    with pytest.raises(ValueError):
        remove_extra_spaces("", 0)
