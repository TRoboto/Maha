import pytest

from maha.cleaners.functions import (
    reduce_repeated_substring,
    remove,
    remove_all_harakat,
    remove_arabic_letter_dots,
    remove_emails,
    remove_english,
    remove_expressions,
    remove_extra_spaces,
    remove_harakat,
    remove_hash_keep_tag,
    remove_hashtags,
    remove_links,
    remove_mentions,
    remove_numbers,
    remove_punctuations,
    remove_strings,
    remove_tatweel,
)
from maha.constants import (
    ALL_HARAKAT,
    ARABIC,
    ARABIC_LETTERS,
    ARABIC_LIGATURES,
    ARABIC_NUMBERS,
    ARABIC_PUNCTUATIONS,
    BEH,
    DAD,
    DOTLESS_BEH,
    DOTLESS_DAD,
    DOTLESS_FEH,
    DOTLESS_GHAIN,
    DOTLESS_JEEM,
    DOTLESS_KHAH,
    DOTLESS_NOON_GHUNNA,
    DOTLESS_QAF,
    DOTLESS_SHEEN,
    DOTLESS_TEH,
    DOTLESS_TEH_MARBUTA,
    DOTLESS_THAL,
    DOTLESS_THEH,
    DOTLESS_YEH,
    DOTLESS_ZAH,
    DOTLESS_ZAIN,
    EMPTY,
    ENGLISH,
    ENGLISH_CAPITAL_LETTERS,
    ENGLISH_LETTERS,
    ENGLISH_NUMBERS,
    ENGLISH_PUNCTUATIONS,
    ENGLISH_SMALL_LETTERS,
    FEH,
    GHAIN,
    HARAKAT,
    JEEM,
    KHAH,
    NOON,
    NUMBERS,
    PUNCTUATIONS,
    QAF,
    SHEEN,
    TATWEEL,
    TEH,
    TEH_MARBUTA,
    THAL,
    THEH,
    YEH,
    ZAH,
    ZAIN,
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


def test_remove_with_custom_character(simple_text_input: str):
    processed_text = remove(text=simple_text_input, custom_strings=list("test"))
    assert (
        processed_text
        == "1. بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In h nam of Allah,Mo Graciou , Mo M rciful."
    )
    assert list_not_in_string(list("test"), processed_text)


@pytest.mark.parametrize("strings", ["test", ["test"]])
def test_remove_with_custom_characters_not_found(simple_text_input: str, strings):
    processed_text = remove(text=simple_text_input, custom_strings=strings)
    assert processed_text == simple_text_input.strip()


@pytest.mark.parametrize("pattern", ["[A-Za-z]"])
def test_remove_with_custom_patterns(simple_text_input: str, pattern):
    processed_text = remove(text=simple_text_input, custom_expressions=pattern)
    assert processed_text == "1. بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ , , ."
    assert list_not_in_string(ENGLISH_LETTERS, processed_text)


def test_remove_with_tatweel(simple_text_input: str):
    processed_text = remove(text=simple_text_input, tatweel=True)
    assert processed_text == simple_text_input.strip()
    processed_text = remove(text="تطويــــل", tatweel=True)
    assert TATWEEL not in processed_text


def test_remove_tatweel():
    text = "تطويــــل"
    processed_text = remove_tatweel(text=text)
    assert processed_text == "تطويل"
    assert TATWEEL not in processed_text


def test_reduce_repeated_substring_default():
    processed_text = reduce_repeated_substring(text="heeeeey")
    assert processed_text == "heey"


def test_reduce_repeated_substring_raises_valueerror():
    with pytest.raises(ValueError):
        reduce_repeated_substring("heeeeey", min_repeated=3, reduce_to=10)

    with pytest.raises(ValueError):
        reduce_repeated_substring("heeeeey", min_repeated=3.5)  # type: ignore

    with pytest.raises(ValueError):
        reduce_repeated_substring("heeeeey", reduce_to=3.5)  # type: ignore

    with pytest.raises(ValueError):
        reduce_repeated_substring("heeeeey", min_repeated=-1)

    with pytest.raises(ValueError):
        reduce_repeated_substring("heeeeey", reduce_to=-5)


@pytest.mark.parametrize(
    "input, expected, min_repeated, reduce_to",
    [
        ("h hhhhh hh", "h hh hh", 3, 2),
        ("heheh hehehehehe he", "heh he he", 2, 1),
        ("ههههههههههه", "هه", 3, 2),
        ("heeellloooooooo", "helo", 2, 1),
        ("heeelloooooooo", "hello", 3, 1),
    ],
)
def test_reduce_repeated_substring(
    input: str, expected: str, min_repeated: int, reduce_to: int
):
    processed_text = reduce_repeated_substring(
        text=input, min_repeated=min_repeated, reduce_to=reduce_to
    )
    assert processed_text == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("ولقد حقق #الأردن أول ميدالية ذهبية", "ولقد حقق الأردن أول ميدالية ذهبية"),
        ("#الورد هو أجمل شئ في الحياة", "الورد هو أجمل شئ في الحياة"),
        ("يا جماعة بدنا #طبيب_doctor", "يا جماعة بدنا طبيب_doctor"),
        ("أكثر من #50 دورة من Google", "أكثر من 50 دورة من Google"),
        ("يجب علينا إدارة # الوقت بشكل جيد", "يجب علينا إدارة # الوقت بشكل جيد"),
        (".#كرة القدم", ".كرة القدم"),
        ("@#برمجة", "@#برمجة"),
        ("_#جمعة_مباركة", "_#جمعة_مباركة"),
        ("&#مسابقة_القرآن_الكريم", "&#مسابقة_القرآن_الكريم"),
        ("#11111رسول_الله", "11111رسول_الله"),
        ("#مسألة_رقم_1111", "مسألة_رقم_1111"),
        ("#Hello", "Hello"),
        ("#مرحبا", "مرحبا"),
        ("#لُقِّب", "لُقِّب"),
        ("&#رمضان", "&#رمضان"),
        ("_#العيد", "_#العيد"),
        ("^#التعليم_للجميع", "^التعليم_للجميع"),
        (":#الرياضة", ":الرياضة"),
    ],
)
def test_remove_hash_keep_tag(input: str, expected: str):
    assert remove_hash_keep_tag(input) == expected


def test_remove_with_ligtures():
    text = "ﷲ اكبر"
    processed_text = remove(text=text, arabic_ligatures=True)
    assert processed_text == "اكبر"
    assert list_not_in_string(ARABIC_LIGATURES, processed_text)


def test_remove_with_hashtags_simple(simple_text_input: str):
    processed_text = remove(text=simple_text_input, hashtags=True)
    assert processed_text == simple_text_input.strip()


def test_remove_with_hashtags_with_arabic(simple_text_input: str):
    simple_text_input += " #hashtag"
    processed_text = remove(text=simple_text_input, hashtags=True, arabic=True)
    assert list_not_in_string(ARABIC, processed_text)


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
        # Edge cases
        ("_#جمعة_مباركة", "_#جمعة_مباركة"),
        ("&#مسابقة_القرآن_الكريم", "&#مسابقة_القرآن_الكريم"),
        ("11111#رسول_الله", "11111#رسول_الله"),
        (".#Good", "."),
        ("@#test", "@#test"),
        ("#لُقِّب", ""),
        ("AB#CD", "AB#CD"),
    ],
)
def test_remove_with_hashtags(input_text: str, expected: str):
    processed_text = remove(text=input_text, hashtags=True)
    assert processed_text == expected


def test_remove_hashtags():
    assert remove_hashtags("#test") == EMPTY
    assert remove_hashtags("#هاشتاق") == EMPTY


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
        ("#لُقِّب", ""),
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
        # Edge cases
        ("_@جمعة_مباركة", "_@جمعة_مباركة"),
        ("&@مسابقة_القرآن_الكريم", "&@مسابقة_القرآن_الكريم"),
        ("11111@رسول_الله", "11111@رسول_الله"),
        (".@Good", "."),
        ("@لُقِّب", ""),
        ("AB@CD", "AB@CD"),
        ("#@test", "#@test"),
    ],
)
def test_remove_with_mentions(input_text: str, expected: str):
    processed_text = remove(text=input_text, mentions=True)
    assert processed_text == expected


def test_remove_mentions():
    assert remove_mentions("@test") == EMPTY
    assert remove_mentions("@منشن") == EMPTY


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
        ("@لُقِّب", ""),
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


def test_remove_emails():
    assert remove_emails("email@web.com") == EMPTY


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
        ("https://www.web.notwebsite.noo", ""),
        ("www.web.notwebsite.noo", "www.web.notwebsite.noo"),
        ("www.web.website.com", ""),
    ],
)
def test_remove_with_links(input_text: str, expected: str):
    processed_text = remove(text=input_text, links=True)
    assert processed_text == expected


def test_remove_with_empty_string():
    processed_text = remove(text=EMPTY, links=True)
    assert processed_text == EMPTY


def test_remove_links():
    assert remove_links("web.com") == EMPTY


def test_remove_should_raise_valueerror(simple_text_input: str):
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


def test_remove_with_emojis(simple_text_input: str):
    processed_text = remove(simple_text_input, emojis=True)
    assert processed_text == simple_text_input.strip()
    assert remove("😎", emojis=True) == EMPTY


@pytest.mark.parametrize(
    "expected, chars_to_remove, use_space",
    [
        ("بِسْمِاللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", ENGLISH + PUNCTUATIONS, False),
        ("1. In the name of Allah,Most Gracious, Most Merciful.", ARABIC, True),
        ("1.    In the name of Allah,Most Gracious, Most Merciful.", ARABIC, False),
    ],
)
def test_remove_strings(
    simple_text_input: str, chars_to_remove: str, expected: str, use_space: bool
):
    assert remove_strings(simple_text_input, chars_to_remove, use_space) == expected


def test_remove_strings_raise_valueerror(simple_text_input: str):
    with pytest.raises(ValueError):
        remove_strings(simple_text_input, "")


def test_remove_patterns(simple_text_input: str):
    processed_text = remove_expressions(simple_text_input, "[\u0600-\u06FF]+")
    assert processed_text == "1. In the name of Allah,Most Gracious, Most Merciful."
    assert list_not_in_string(ARABIC, processed_text)


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
        remove_extra_spaces("", 4.5)  # type: ignore

    with pytest.raises(ValueError):
        remove_extra_spaces("", 0)


@pytest.mark.parametrize(
    "input, expected",
    [
        (BEH, DOTLESS_BEH),
        (TEH, DOTLESS_TEH),
        (THEH, DOTLESS_THEH),
        (JEEM, DOTLESS_JEEM),
        (KHAH, DOTLESS_KHAH),
        (THAL, DOTLESS_THAL),
        (ZAIN, DOTLESS_ZAIN),
        (SHEEN, DOTLESS_SHEEN),
        (DAD, DOTLESS_DAD),
        (ZAH, DOTLESS_ZAH),
        (GHAIN, DOTLESS_GHAIN),
        (FEH, DOTLESS_FEH),
        (QAF, DOTLESS_QAF),
        (NOON, DOTLESS_NOON_GHUNNA),
        (YEH, DOTLESS_YEH),
        (TEH_MARBUTA, DOTLESS_TEH_MARBUTA),
    ],
)
def test_remove_arabic_letter_dots_with_individual_letters(input: str, expected: str):
    assert remove_arabic_letter_dots(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("باب", "ٮاٮ"),
        ("تل", "ٮل"),
        ("ثروة", "ٮروه"),
        ("جمل", "حمل"),
        ("خو", "حو"),
        ("ذوق", "دوٯ"),
        ("زيادة", "رىاده"),
        ("شمس", "سمس"),
        ("ضوء", "صوء"),
        ("ظلام", "طلام"),
        ("غيم", "عىم"),
        ("فوق", "ڡوٯ"),
        ("قلب", "ٯلٮ"),
        ("نور", "ٮور"),
        ("يوم", "ىوم"),
    ],
)
def test_remove_arabic_letter_dots_with_dots_begin(input: str, expected: str):

    assert remove_arabic_letter_dots(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("ربو", "رٮو"),
        ("وتر", "وٮر"),
        ("وثب", "وٮٮ"),
        ("وجل", "وحل"),
        ("مخدر", "محدر"),
        ("حذر", "حدر"),
        ("وزر", "ورر"),
        ("حشد", "حسد"),
        ("وضوء", "وصوء"),
        ("حظر", "حطر"),
        ("صغى", "صعى"),
        ("افلام", "اڡلام"),
        ("وقى", "وٯى"),
        ("سنة", "سٮه"),
        ("سليم", "سلىم"),
    ],
)
def test_remove_arabic_letter_dots_with_dots_mid(input: str, expected: str):

    assert remove_arabic_letter_dots(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("صب", "صٮ"),
        ("ست", "سٮ"),
        ("حث", "حٮ"),
        ("حرج", "حرح"),
        ("مخ", "مح"),
        ("عوذ", "عود"),
        ("وز", "ور"),
        ("رش", "رس"),
        ("وضوء", "وصوء"),
        ("وعظ", "وعط"),
        ("صمغ", "صمع"),
        ("وفى", "وڡى"),
        ("حق", "حٯ"),
        ("سن", "سں"),
        ("مي", "مى"),
        ("صلاة", "صلاه"),
    ],
)
def test_remove_arabic_letter_dots_with_dots_end(input: str, expected: str):

    assert remove_arabic_letter_dots(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("البنيان", "الٮٮىاں"),
        ("البنيانُ قوي", "الٮٮىاںُ ٯوى"),
        ("البنيان قوي", "الٮٮىاں ٯوى"),
        ("البنيان\nقوي", "الٮٮىاں\nٯوى"),
        ("البنيان.", "الٮٮىاں."),
        ("البنيان.", "الٮٮىاں."),
        ("البنيان؟", "الٮٮىاں؟"),
        ("البنْيان😊", "الٮٮْىاں😊"),
        ("البنْيانُ،", "الٮٮْىاںُ،"),
    ],
)
def test_remove_arabic_letter_dots_with_edge_case(input: str, expected: str):

    assert remove_arabic_letter_dots(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "‏احذروا الدنيا فإنها تغُرُّ وتضُرُّ وتمُرُّ.",
            "‏احدروا الدٮىا ڡإٮها ٮعُرُّ وٮصُرُّ وٮمُرُّ.",
        ),
        (
            "المتسلسلات و طرق إيجاد قواعدها أو حدودها والجمع",
            "المٮسلسلاٮ و طرٯ إىحاد ٯواعدها أو حدودها والحمع",
        ),
    ],
)
def test_remove_arabic_letter_dots_general(input: str, expected: str):

    assert remove_arabic_letter_dots(input) == expected


def test_remove_list_input(simple_text_input: str):
    list_ = ["بِسْمِ", "the", "ال(?=ر)"]
    processed_text = remove(text=simple_text_input, custom_expressions=list_)
    assert (
        processed_text
        == "1. ،اللَّهِ رَّحْمَٰنِ رَّحِيمِ In name of Allah,Most Gracious, Most Merciful."
    )
