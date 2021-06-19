import pytest

from maha.cleaners.functions import normalize, normalize_lam_alef
from maha.constants import ALEF, ALEF_VARIATIONS, EMPTY, SPACE


def test_normalize_with_alef():
    processedtext = normalize("".join(ALEF_VARIATIONS), alef=True)
    assert processedtext == "".join([ALEF] * len(ALEF_VARIATIONS))


@pytest.mark.parametrize(
    "input,expected",
    [
        ("السﻻم", "السلام"),
        ("اﻵن", "الان"),
        ("اﻷحد", "الاحد"),
        ("اﻹسﻻم", "الاسلام"),
    ],
)
def test_normalize_with_lam_alef(input: str, expected: str):
    processedtext = normalize(input, lam_alef=True)
    assert processedtext == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("مؤمن", "مومن"),
        ("ورق", "ورق"),
    ],
)
def test_normalize_with_waw(input: str, expected: str):
    processedtext = normalize(input, waw=True)
    assert processedtext == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("على", "علي"),
        ("قارئ", "قاري"),
        ("رأي", "رأي"),
    ],
)
def test_normalize_with_yeh(input: str, expected: str):
    processedtext = normalize(input, yeh=True)
    assert processedtext == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("مدرسة", "مدرسه"),
        ("الله", "الله"),
    ],
)
def test_normalize_with_teh_marbuta(input: str, expected: str):
    processedtext = normalize(input, teh_marbuta=True)
    assert processedtext == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("﷽", "بسم الله الرحمن الرحيم"),
        ("ﷳ", "اكبر"),
        ("ﷺ", "صلى الله عليه وسلم"),
        ("ﷲ", "الله"),
        ("ﷴ ﷶ ﷲ ﷻ", "محمد رسول الله جل جلاله"),
        ("ﷹ ﷲ ﷷ ﷸ", "صلى الله عليه وسلم"),
        ("﷼", "ريال"),
        ("ﷵ", "صلى الله عليه وسلم"),
    ],
)
def test_normalize_with_ligatures(input: str, expected: str):
    processedtext = normalize(input, ligatures=True)
    assert processedtext == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("test", "test"),
        ("\u00A0", SPACE),
        ("\u1680\u2000\u2005\u200B\u202F\u205F\u3000\uFEFF", "".join([SPACE] * 8)),
    ],
)
def test_normalize_with_spaces(input: str, expected: str):
    processedtext = normalize(input, spaces=True)
    assert processedtext == expected


def test_normalize_should_raise_valueerror(simple_text_input: str):
    with pytest.raises(ValueError):
        normalize(EMPTY, ligatures=True)
    with pytest.raises(ValueError):
        normalize(simple_text_input)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("السﻻم", "السلام"),
        ("اﻵن", "الآن"),
        ("اﻷحد", "الأحد"),
    ],
)
def test_normalize_lam_alef(input: str, expected: str):
    processedtext = normalize_lam_alef(input)
    assert processedtext == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("السﻻم", "السلام"),
        ("اﻵن", "الان"),
        ("اﻷحد", "الاحد"),
    ],
)
def test_normalize_lam_alef_no_hamza(input: str, expected: str):
    processedtext = normalize_lam_alef(input, keep_hamza=False)
    assert processedtext == expected
