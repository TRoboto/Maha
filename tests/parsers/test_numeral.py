from __future__ import annotations

import random
from itertools import chain

import pytest

from maha.parsers.functions import parse_dimension
from maha.parsers.rules.numeral import *
from maha.parsers.templates import Dimension, DimensionType

random.seed(0)


def assert_expression_output(output: list[Dimension], expected):
    assert len(output) == 1
    assert isinstance(output[0], Dimension)
    dim = output[0]

    assert dim.dimension_type == DimensionType.NUMERAL
    assert isinstance(dim.value, (float, int))
    assert pytest.approx(dim.value, 0.0001) == expected


def get_value_positions(*text: str):
    positions = [
        ("${}."),
        ("@{}"),
        ("!{}."),
        (".{} "),
        (",{}"),
        ("({},"),
        ("{},"),
        ("&{}"),
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


def get_value_with_integer(ar_int: str, en_int: str, values: list[str]):
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
    assert_expression_output(parse_dimension(input, numeral=True), expected)


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
    assert_expression_output(parse_dimension(input, numeral=True), expected)


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
    assert_expression_output(parse_dimension(input, numeral=True), expected)


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
        get_value_with_integer("٢٢", "22", ["إثنتين و عشرون"]),
    ),
)
def test_combines_tens(input, expected):
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer(
            "١٠٠", "100", ["مية", "ميه", "مائة", "مائه", "مئة", "مئه"]
        ),
        get_value_with_integer("٢٠٠", "200", ["ميتين", "مئتين", "مئتان"]),
        get_value_with_integer(
            "٣٠٠",
            "300",
            ["ثلاثمية", "ثلاث ميات", "ثلاثة مائة", "تلاتمية", "ثلاثمئه"],
        ),
        get_value_with_integer(
            "٤٠٠",
            "400",
            ["أربعمية", "أربع مئات", "أربعة مائة", "اربعمية", "اربعمئه"],
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
    assert_expression_output(parse_dimension(input, numeral=True), expected)


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
    assert_expression_output(parse_dimension(input, numeral=True), expected)


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
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("٢٠٠٠٠", "20000", ["عشرين الف"]),
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
def test_thousands(input, expected):
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "input, expected",
    [
        ("10,000.0", 10000),
        ("١٠٬٠٠٠٫٠٠٠", 10000),
        ("-10,000", -10000),
        ("1٬000 000", 1000000),
        ("1 000 000", 1000000),
        ("-١٬٠٠٠٬٠٠٠", -1000000),
        ("+١ ٠٠٠ ٠٠٠", +1000000),
        ("١٬٠٠٠٬٠٠٠", 1000000),
        (".1", 0.1),
        ("٫٠١", 0.01),
        ("١%", 0.01),
        ("0.01%", 0.0001),
        (".01%", 0.0001),
        ("20.0%", 0.2),
        ("200%", 2),
    ],
)
def test_numbers(input, expected):
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "expected, input",
    [
        (0.1, "صفر فاصلة عشرة"),
        (0.1, "صفر فاصلة واحد"),
        (3.4, "ثلاث فاصل اربع"),
        (10.7, "عشرة فاصلة سبعة"),
        (10.7, "10 فاصلة سبعة"),
        (1000530.2704, "مليون وخمسمية وثلاثين فاصلة الفين وسبعمية واربعة"),
        (10.5, "10 فاصله 5"),
        (33.3, "ثلاثة وثلاثين فاصلة ثلاثة"),
        (100 / 3, "ثلث مية"),
        (1025, "الف وربع مية"),
        (2070, "الفين وعشرين ونص مية"),
    ],
)
def test_fasila_numbers(input, expected):
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("١٠٠٠٠٠٠", "1000000", ["مليون"]),
        get_value_with_integer("٢٠٠٠٠٠٠", "2000000", ["مليونين", "مليونان"]),
        get_value_with_integer("٣٠٠٠٠٠٠", "3000000", ["ثلاث ملايين", "ثلاثة مليون"]),
        get_value_with_integer("٤٠٠٠٠٠٠", "4000000", ["اربع ملايين", "أربعة مليون"]),
        get_value_with_integer("٥٠٠٠٠٠٠", "5000000", ["خمس ملايين", "خمسة مليون"]),
        get_value_with_integer("٦٠٠٠٠٠٠", "6000000", ["ست ملايين", "ستة ملايين"]),
        get_value_with_integer("٧٠٠٠٠٠٠", "7000000", ["سبع ملايين", "سبعة ملايين"]),
        get_value_with_integer("٨٠٠٠٠٠٠", "8000000", ["ثماني ملايين", "ثمانية ملايين"]),
        get_value_with_integer("٩٠٠٠٠٠٠", "9000000", ["تسع ملايين", "تسعة ملايين"]),
    ),
)
def test_perfect_millions(input, expected):
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value_with_integer("٢٠٠٠٠٠٠٠", "20000000", ["عشرين مليون"]),
        get_value_with_integer("١٠٠١٢٠٠", "1001200", ["مليون والف ومئتين"]),
        get_value_with_integer("٣٠٢٢٠٠٠", "3022000", ["ثلاثة مليون واثنين وعشرين الف"]),
        get_value_with_integer("٤٠٠٠٠٠١٠", "40000010", ["أربعين مليون وعشرة"]),
        get_value_with_integer(
            "٥٥٠٠٧٣٢٥",
            "55007325",
            ["خمسة وخمسين مليون وسبع الاف وثلاثمية وخمسة وعشرين"],
        ),
        get_value_with_integer(
            "٢٠٢٢٢٢٢", "2022222", ["مليونين واثنين وعشرين الف ومئتين واثنين وعشرين"]
        ),
        get_value_with_integer(
            "١٠٠١٠٤٦٥", "10010465", ["عشرة مليون وعشر الاف واربعمئة وخمسة وستين"]
        ),
        get_value_with_integer("٣٠٠١٠٣٠", "3001030", ["ثلاث ملايين والف وثلاثين"]),
        get_value_with_integer(
            "٩٠٠٩٠٠٠١", "90090001", ["تسعين مليون وتسعين الف وواحد"]
        ),
        get_value_with_integer("١٧٠٠٠١٠٠", "17000100", ["سبعطعشر مليون ومية"]),
    ),
)
def test_millions(input, expected):
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "expected, input",
    [
        (9120, "الف والفين والف وخمسة الاف ومية وعشرين"),
        (1000110, "مئة وعشرة ومليون"),
        (45, "اربعين وخمسة"),
        (1000036000, "ثلاثة وثلاثين الف و3 الاف وبليون"),
        (2991, "واحد وتسعين وتسعمية والفين"),
    ],
)
def test_combinations(input, expected):
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "expected, input",
    [
        (100_000, "مئة الف"),
        (100_000_000_000, "مئة الف مليون"),
        (2_000_000, "عشرين مئة الف"),
        (300_000, "ثلاثمئة الف"),
        (200_500_000, "مئتين مليون وخمس مئة الف"),
        (4_000_000_000_000, "اربع الاف مليار"),
        (2_100_000.100_01, "واحد وعشرين مئة الف فاصلة مئة الف وعشرة"),
        (3_300_000, "ثلاثة وثلاثين مئة الف"),
    ],
)
def test_hierarchical_parsing(input, expected):
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "expected, input",
    [
        (0.001, "واحد في الألف"),
        (0.001, "واحد بالالف"),
        (0.05, "خمسة في المية"),
        (0.00002, "عشرين في المليون"),
        (0.1, "مئة بالألف"),
        (0.01, "واحد في المئة"),
        (0.33, "ثلاثة وثلاثين بالمية"),
    ],
)
def test_multiplier_fraction_parsing(input, expected):
    assert_expression_output(parse_dimension(input, numeral=True), expected)


@pytest.mark.parametrize(
    "input",
    [
        ("الواحد"),
        ("العشرين"),
        ("العشرة"),
        ("المئة"),
        ("الفتياني"),
        ("المليونير"),
        ("ولست"),
        ("وواثنين"),
    ],
)
def test_negative_simple_values(input: str):
    output = parse_dimension(input, numeral=True)
    assert output == []
