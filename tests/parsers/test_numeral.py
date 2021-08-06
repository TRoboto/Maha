import random
from itertools import chain
from typing import List

import pytest

from maha.parsers.functions.parse import parse_expression
from maha.parsers.interfaces.expressions import ExpressionGroup, ExpressionResult
from maha.parsers.numeral.rule import *
from maha.parsers.numeral.utils import get_value

random.seed(0)


def assert_expression_output(output, expected):
    assert len(output) == 1
    output = output[0]

    assert isinstance(output.value, (float, int))
    assert pytest.approx(output.value, 0.0001) == expected


def get_value_positions(*text: str):
    positions = [
        ("{}."),
        ("{}"),
        (" {} "),
        (" {}"),
        (",{}"),
        (",{},"),
        ("{},"),
        ("و{}"),
        ("و {}"),
        ("{}"),
    ]
    for t in text:
        yield random.choice(positions).format(t)


def get_integer_forms(number1: str, number2: str):
    yield from [
        number1,
        number2,
        f"{number1}٫٠",
        f"{number1}.0",
        f"{number2}٫٠",
        f"{number2}.0",
    ]


def get_value_with_integer(ar_int: str, en_int: str, values: List[str]):
    for v in chain(get_value_positions(*values), get_integer_forms(ar_int, en_int)):
        yield v, int(en_int)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("٠", "0", ["صفر"]),
        get_value_with_integer("١", "1", ["واحدة", "واحده", "واحد"]),
        get_value_with_integer(
            "٢", "2", ["اتنين", "اثنين", "إثنان", "إثنين", "اثنتين", "إثنتان"]
        ),
        get_value_with_integer("٣", "3", ["تلات", "ثلاث", "ثلاثة", "تلاتة", "تلاته"]),
        get_value_with_integer("٤", "4", ["اربعه", "أربع", "اربعة"]),
        get_value_with_integer("٥", "5", ["خمسة", "خمسه", "خمس"]),
        get_value_with_integer("٦", "6", ["ست", "سته", "ستة"]),
        get_value_with_integer("٧", "7", ["سبعه", "سبعة", "سبع"]),
        get_value_with_integer(
            "٨", "8", ["ثمانية", "ثمانيه", "ثماني", "ثمنية", "تمنيه", "تماني"]
        ),
        get_value_with_integer("٩", "9", ["تسعة", "تسعه", "تسع"]),
    ),
)
def test_ones(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("١٠", "10", ["عشرة", "عشره", "عشر"]),
        get_value_with_integer(
            "١١",
            "11",
            ["احدعشر", "احدعش", "أحد عشرة", "احد عشر", "حدعشر", "حداشر", "إحدى عشر"],
        ),
        get_value_with_integer(
            "١٢",
            "12",
            ["اطنعش", "اثني عشر", "إثنتي عشر", "إتناشر", "اطناعشر", "إثنى عشرة"],
        ),
        get_value_with_integer(
            "١٣",
            "13",
            ["ثلتعش", "ثلاثة عشر", "ثلاثه عشر", "تلتعشر", "ثلثطعشر", "ثلاثة عشرة"],
        ),
        get_value_with_integer(
            "١٤",
            "14",
            [
                "اربعتاشر",
                "اربعة عشر",
                "اربع عشر",
                "اربعه عشره",
                "أربعطعش",
                "أربعة عشرة",
            ],
        ),
        get_value_with_integer(
            "١٥",
            "15",
            ["خمسطعش", "خمسة عشر", "خمسه عشر", "خمستاشر", "خمس عشر", "خمسة عشرة"],
        ),
        get_value_with_integer(
            "١٦",
            "16",
            ["ستاشر", "ستة عشر", "سته عشر", "ستطعش", "ست عشر", "ستة عشرة"],
        ),
        get_value_with_integer(
            "١٧",
            "17",
            ["سبعتاشر", "سبعة عشر", "سبعه عشر", "سبعطعش", "سبع عشر", "سبعة عشرة"],
        ),
        get_value_with_integer(
            "١٨",
            "18",
            [
                "تمنتاشر",
                "ثمانية عشر",
                "تمنية عشر",
                "ثمنطعش",
                "ثماني عشر",
                "تمانية عشرة",
            ],
        ),
        get_value_with_integer(
            "١٩",
            "19",
            [
                "تسعتاشر",
                "تسعة عشر",
                "تسعه عشر",
                "تسعطعشر",
                "تسع عشر",
                "تسعة عشرة",
            ],
        ),
    ),
)
def test_tens(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("١٠", "10", ["عشر", "عشرة", "عشره"]),
        get_value_with_integer("٢٠", "20", ["عشرون", "عشرين"]),
        get_value_with_integer("٣٠", "30", ["ثلاثين", "ثلاثون", "تلاتين"]),
        get_value_with_integer("٤٠", "40", ["أربعين", "أربعون", "اربعين"]),
        get_value_with_integer("٥٠", "50", ["خمسين", "خمسون", "نص مئة", "نصف مئة"]),
        get_value_with_integer("٦٠", "60", ["ستين", "ستون"]),
        get_value_with_integer("٧٠", "70", ["سبعين", "سبعون"]),
        get_value_with_integer("٨٠", "80", ["ثمانين", "ثمانون", "تمنين", "تمانون"]),
        get_value_with_integer("٩٠", "90", ["تسعين", "تسعون"]),
    ),
)
def test_perfect_tens(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer(
            "٢١", "21", ["واحد وعشرين", "واحد وعشرون", "واحدة وعشرون"]
        ),
        get_value_with_integer(
            "٣٢", "32", ["اثنين وثلاثين", "اتنين وتلاتين", "إثنان وثلاثون"]
        ),
        get_value_with_integer(
            "٤٣", "43", ["ثلاثة وأربعين", "ثلاث وأربعون", "تلاته واربعون"]
        ),
        get_value_with_integer(
            "٤٤", "44", ["أربعة واربعون", "اربع واربعون", "اربعة وأربعين"]
        ),
        get_value_with_integer(
            "٥٤", "54", ["أربعة وخمسين", "اربع وخمسون", "اربعة وخمسون"]
        ),
        get_value_with_integer("٦٥", "65", ["خمسة وستين", "خمس وستون", "خمسه وستين"]),
        get_value_with_integer("٧٦", "76", ["ستة وسبعين", "ست وسبعون", "سته وسبعين"]),
        get_value_with_integer(
            "٨٧", "87", ["سبعة وتمانين", "سبع وتمانون", "سبعه وثمانين"]
        ),
        get_value_with_integer(
            "٩٨", "98", ["ثمانية وتسعين", "ثماني وتسعون", "تمنية وتسعين"]
        ),
        get_value_with_integer("٩٩", "99", ["تسعة وتسعين"]),
        get_value_with_integer("٩١", "91", ["واحد وتسعين"]),
        get_value_with_integer("٦٦", "66", ["ستة وستين"]),
        get_value_with_integer("٢٦", "26", ["ستة وعشرين"]),
        get_value_with_integer("٢٥", "25", ["خمسة و عشرون", "ربع مية"]),
        get_value_with_integer("٧٥", "75", ["خمسة وسبعين", "مية الا ربع"]),
        get_value_with_integer("٢٢", "22", ["إثنتين و عشرون"]),
    ),
)
def test_combines_tens(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer(
            "١٠٠", "100", ["مية", "ميه", "مائة", "مائه", "مئة", "مئه", "نص ميتين"]
        ),
        get_value_with_integer("٢٠٠", "200", ["ميتين", "مئتين", "مئتان"]),
        get_value_with_integer(
            "٣٠٠",
            "300",
            ["ثلاثمية", "ثلاث مئة", "ثلاثة مائة", "تلاتمية", "ثلاثمئه"],
        ),
        get_value_with_integer(
            "٤٠٠",
            "400",
            ["أربعمية", "أربع مئة", "أربعة مائة", "اربعمية", "اربعمئه"],
        ),
        get_value_with_integer(
            "٥٠٠",
            "500",
            ["خمسمية", "خمسة مئة", "خمس مائة", "خمسميه", "خمسه مئة"],
        ),
        get_value_with_integer(
            "٦٠٠",
            "600",
            ["ستمية", "ستة مئة", "ست مائة", "ستميه", "ستمائة"],
        ),
        get_value_with_integer(
            "٧٠٠",
            "700",
            ["سبعمية", "سبعة مئة", "سبع مائة", "سبعميه", "سبعمائة"],
        ),
        get_value_with_integer(
            "٨٠٠",
            "800",
            ["ثمنمية", "ثماني مئة", "ثمان مائة", "تمنميه", "ثمانمائة"],
        ),
        get_value_with_integer(
            "٩٠٠",
            "900",
            ["تسعمية", "تسعة مئة", "تسع مائة", "تسعميه", "تسعمائة"],
        ),
    ),
)
def test_perfect_hundreds(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("١٩١", "191", ["مية وواحد وتسعين"]),
        get_value_with_integer("١٢٤", "124", ["مائة واربعة وعشرين"]),
        get_value_with_integer("٢١٥", "215", ["مئتين وخمسه عشر"]),
        get_value_with_integer("٣٠٦", "306", ["ثلاثمية وستة"]),
        get_value_with_integer("٠٤١٠", "0410", ["اربعمية وعشرة"]),
        get_value_with_integer("٥٢٠", "520", ["خمس مائة وعشرين"]),
        get_value_with_integer("٦٠٦", "606", ["ستمية وستة"]),
        get_value_with_integer("٧٨٠", "780", ["سبعة مائة وثمانون"]),
        get_value_with_integer("٨٧٧", "877", ["ثمنمية وسبعة وسبعين"]),
        get_value_with_integer("٩٩٩", "999", ["تسع مية وتسعه وتسعين"]),
    ),
)
def test_hundreds(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("١٠٠٠", "1000", ["الف", "ألف"]),
        get_value_with_integer("٢٠٠٠", "2000", ["ألفين", "الفين", "ألفان"]),
        get_value_with_integer("٣٠٠٠", "3000", ["ثلاث آلاف", "ثلاثة الاف"]),
        get_value_with_integer("٤٠٠٠", "4000", ["اربع الاف", "أربعة الوف"]),
        get_value_with_integer("٥٠٠٠", "5000", ["خمس آلاف", "خمسة ألاف"]),
        get_value_with_integer("٦٠٠٠", "6000", ["ست آلاف", "ستة آلاف"]),
        get_value_with_integer("٧٠٠٠", "7000", ["سبع آلاف", "سبعة الاف"]),
        get_value_with_integer("٨٠٠٠", "8000", ["ثماني آلاف", "ثمانية الاف"]),
        get_value_with_integer("٩٠٠٠", "9000", ["تسع آلاف", "تسعة الاف"]),
    ),
)
def test_perfect_thousands(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("١٢٠٠", "1200", ["الف ومئتين"]),
        get_value_with_integer("٣٢٢٠", "3220", ["ثلاثة الاف ومئتان وعشرين"]),
        get_value_with_integer("٤٠٠١٠", "40010", ["أربعين الف وعشرة"]),
        get_value_with_integer(
            "٥٥٣٢٥", "55325", ["خمسة وخمسين الف وثلاثمية وخمسة وعشرين"]
        ),
        get_value_with_integer(
            "٢٢٢٢٢", "22222", ["اثنين وعشرين الف ومئتين واثنين وعشرين"]
        ),
        get_value_with_integer("١٠٤٦٥", "10465", ["عشرة الاف واربعمئة وخمسة وستين"]),
        get_value_with_integer("١٠٣٠", "1030", ["الف وثلاثين"]),
        get_value_with_integer("٩٠٠٠١", "90001", ["تسعين الف وواحد"]),
        get_value_with_integer("١٧١٠٠", "17100", ["سبعطعشر الف ومية"]),
    ),
)
def test_perfect_thousands(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)
