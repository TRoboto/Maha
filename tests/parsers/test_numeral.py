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


def get_value_with_integer(int1: str, int2: str, expected: float, values: List[str]):
    for v in chain(get_value_positions(*values), get_integer_forms(int1, int2)):
        yield v, expected


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("٠", "0", 0, ["صفر"]),
        get_value_with_integer("١", "1", 1, ["واحدة", "واحده", "واحد"]),
        get_value_with_integer(
            "٢", "2", 2, ["اتنين", "اثنين", "إثنان", "إثنين", "اثنتين", "إثنتان"]
        ),
        get_value_with_integer(
            "٣", "3", 3, ["تلات", "ثلاث", "ثلاثة", "تلاتة", "تلاته"]
        ),
        get_value_with_integer("٤", "4", 4, ["اربعه", "أربع", "اربعة"]),
        get_value_with_integer("٥", "5", 5, ["خمسة", "خمسه", "خمس"]),
        get_value_with_integer("٦", "6", 6, ["ست", "سته", "ستة"]),
        get_value_with_integer("٧", "7", 7, ["سبعه", "سبعة", "سبع"]),
        get_value_with_integer(
            "٨", "8", 8, ["ثمانية", "ثمانيه", "ثماني", "ثمنية", "تمنيه", "تماني"]
        ),
        get_value_with_integer("٩", "9", 9, ["تسعة", "تسعه", "تسع"]),
    ),
)
def test_ones(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("١٠", "10", 10, ["عشرة", "عشره", "عشر"]),
        get_value_with_integer(
            "١١",
            "11",
            11,
            ["احدعشر", "احدعش", "أحد عشرة", "احد عشر", "حدعشر", "حداشر", "إحدى عشر"],
        ),
        get_value_with_integer(
            "١٢",
            "12",
            12,
            ["اطنعش", "اثني عشر", "إثنتي عشر", "إتناشر", "اطناعشر", "إثنى عشرة"],
        ),
        get_value_with_integer(
            "١٣",
            "13",
            13,
            ["ثلتعش", "ثلاثة عشر", "ثلاثه عشر", "تلتعشر", "ثلثطعشر", "ثلاثة عشرة"],
        ),
        get_value_with_integer(
            "١٤",
            "14",
            14,
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
            15,
            ["خمسطعش", "خمسة عشر", "خمسه عشر", "خمستاشر", "خمس عشر", "خمسة عشرة"],
        ),
        get_value_with_integer(
            "١٦",
            "16",
            16,
            ["ستاشر", "ستة عشر", "سته عشر", "ستطعش", "ست عشر", "ستة عشرة"],
        ),
        get_value_with_integer(
            "١٧",
            "17",
            17,
            ["سبعتاشر", "سبعة عشر", "سبعه عشر", "سبعطعش", "سبع عشر", "سبعة عشرة"],
        ),
        get_value_with_integer(
            "١٨",
            "18",
            18,
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
            19,
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
        get_value_with_integer("١٠", "10", 10, ["عشر", "عشرة", "عشره"]),
        get_value_with_integer("٢٠", "20", 20, ["عشرون", "عشرين"]),
        get_value_with_integer("٣٠", "30", 30, ["ثلاثين", "ثلاثون", "تلاتين"]),
        get_value_with_integer("٤٠", "40", 40, ["أربعين", "أربعون", "اربعين"]),
        get_value_with_integer("٥٠", "50", 50, ["خمسين", "خمسون"]),
        get_value_with_integer("٦٠", "60", 60, ["ستين", "ستون"]),
        get_value_with_integer("٧٠", "70", 70, ["سبعين", "سبعون"]),
        get_value_with_integer("٨٠", "80", 80, ["ثمانين", "ثمانون", "تمنين", "تمانون"]),
        get_value_with_integer("٩٠", "90", 90, ["تسعين", "تسعون"]),
    ),
)
def test_perfect_tens(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer(
            "٢١", "21", 21, ["واحد وعشرين", "واحد وعشرون", "واحدة وعشرون"]
        ),
        get_value_with_integer(
            "٣٢", "32", 32, ["اثنين وثلاثين", "اتنين وتلاتين", "إثنان وثلاثون"]
        ),
        get_value_with_integer(
            "٤٣", "43", 43, ["ثلاثة وأربعين", "ثلاث وأربعون", "تلاته واربعون"]
        ),
        get_value_with_integer(
            "٤٤", "44", 44, ["أربعة واربعون", "اربع واربعون", "اربعة وأربعين"]
        ),
        get_value_with_integer(
            "٥٤", "54", 54, ["أربعة وخمسين", "اربع وخمسون", "اربعة وخمسون"]
        ),
        get_value_with_integer(
            "٦٥", "65", 65, ["خمسة وستين", "خمس وستون", "خمسه وستين"]
        ),
        get_value_with_integer(
            "٧٦", "76", 76, ["ستة وسبعين", "ست وسبعون", "سته وسبعين"]
        ),
        get_value_with_integer(
            "٨٧", "87", 87, ["سبعة وتمانين", "سبع وتمانون", "سبعه وثمانين"]
        ),
        get_value_with_integer(
            "٩٨", "98", 98, ["ثمانية وتسعين", "ثماني وتسعون", "تمنية وتسعين"]
        ),
        get_value_with_integer("٩٩", "99", 99, ["تسعة وتسعين"]),
        get_value_with_integer("٩١", "91", 91, ["واحد وتسعين"]),
        get_value_with_integer("٦٦", "66", 66, ["ستة وستين"]),
        get_value_with_integer("٢٦", "26", 26, ["ستة وعشرين"]),
        get_value_with_integer("٢٢", "22", 22, ["إثنتين و عشرون"]),
    ),
)
def test_combines_tens(input, expected):
    assert_expression_output(parse_expression(input, EXPRESSION_NUMERAL), expected)
