import random
from itertools import chain
from typing import List

import pytest

from maha.parsers.functions.parse import parse_expression
from maha.parsers.interfaces.expressions import ExpressionGroup, ExpressionResult
from maha.parsers.numeral.rule import *
from maha.parsers.numeral.utils import get_value

# random.seed(0)


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
