import random
from itertools import chain
from typing import List

import pytest

from maha.parsers.functions import parse_dimension
from maha.parsers.rules.numeral import *
from maha.parsers.templates import Dimension, DimensionType

random.seed(0)


def assert_expression_output(output: List[Dimension], expected):
    assert len(output) == 1
    assert isinstance(output[0], Dimension)
    dim = output[0]

    assert dim.dimension_type == DimensionType.ORDINAL
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


def get_value(exprected: int, values: List[str]):
    for v in get_value_positions(*values):
        yield v, exprected


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value(1, ["أول", "الاولى", "الأول", "اول"]),
        get_value(2, ["الثاني", "التاني", "الثانية", "التانيه", "تاني", "ثاني"]),
        get_value(3, ["التالت", "الثالثة", "ثالث"]),
        get_value(4, ["الرابع", "الرابعه", "رابع"]),
        get_value(5, ["الخامس", "خامس", "الخامسه", "خامسة"]),
        get_value(6, ["السادس", "سادس", "سادسة"]),
        get_value(7, ["السابع", "سابع", "السابعه"]),
        get_value(8, ["الثامن", "التامن", "التامنة", "ثامن", "تامن"]),
        get_value(9, ["التاسع", "التاسعه", "تاسعة", "تاسع"]),
    ),
)
def test_ones(input, expected):
    assert_expression_output(parse_dimension(input, ordinal=True), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value(10, ["العاشر", "عاشر", "العاشرة"]),
        get_value(
            11, ["حادي عشر", "الاحدعشر", "الحادي عشرة", "الأحد عشر", "الإحدى عشره"]
        ),
        get_value(
            12, ["الثاني عشر", "التانى عشره", "الإثنتي عشر", "الإثني عشر", "ثاني عشرة"]
        ),
        get_value(
            13,
            ["الثالث عشرة", "الثالثة عشرة", "التالته عشر", "الثالث عشره", "ثالث عشر"],
        ),
        get_value(
            14,
            ["الرابع عشر", "الرابعة عشر", "رابع عشر", "الرابعه عشره", "رابع عشرة"],
        ),
        get_value(15, ["الخامس عشر", "خامس عشر", "الخامسة عشرة", "الخامس عشره"]),
        get_value(16, ["السادس عشر", "السادسة عشر", "سادسه عشره"]),
        get_value(17, ["السابع عشر", "السابعة عشره", "سابع عشر", "السابعه عشرة"]),
        get_value(18, ["التامن عشر", "ثامن عشر", "الثامنة عشر", "الثامنه عشره"]),
        get_value(19, ["التاسع  عشر", "تاسع عشرة", "التاسعة عشره"]),
    ),
)
def test_tens(input, expected):
    assert_expression_output(parse_dimension(input, ordinal=True), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value(10, ["العاشر", "العاشرة", "العاشره"]),
        get_value(20, ["العشرون", "العشرين"]),
        get_value(30, ["الثلاثين", "الثلاثون", "التلاتين"]),
        get_value(40, ["الأربعين", "الأربعون", "الاربعين"]),
        get_value(50, ["الخمسين", "الخمسون"]),
        get_value(60, ["الستين", "الستون"]),
        get_value(70, ["السبعين", "السبعون"]),
        get_value(80, ["الثمانين", "الثمانون", "التمنين", "التمانون"]),
        get_value(90, ["التسعين", "التسعون"]),
    ),
)
def test_perfect_tens(input, expected):
    assert_expression_output(parse_dimension(input, ordinal=True), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value(21, ["الواحد والعشرين", "الواحد والعشرون", "الواحدة والعشرون"]),
        get_value(32, ["الثاني والثلاثين", "الثاني والتلاتين", "الثانية والثلاثون"]),
        get_value(43, ["الثالثة والأربعين", "الثالث والأربعون"]),
        get_value(44, ["الرابع والاربعون", "الرابع والاربعون"]),
        get_value(54, ["الرابع والخمسين", "الرابع والخمسون"]),
        get_value(65, ["الخامس والستين", "الخامس والستون"]),
        get_value(76, ["السادس والسبعين", "السادس والسبعون"]),
        get_value(87, ["السابع والتمانين", "السابع والتمانون"]),
        get_value(98, ["الثامن والتسعين", "التامن والتسعون"]),
        get_value(99, ["التاسع والتسعين"]),
        get_value(91, ["الواحد والتسعين"]),
        get_value(66, ["السادس والستين"]),
        get_value(26, ["السادس والعشرين"]),
        get_value(25, ["الخامس و العشرون"]),
        get_value(75, ["الخامس والسبعين"]),
        get_value(22, ["الثاني و العشرون"]),
        get_value(22, ["التانية و العشرون"]),
    ),
)
def test_combines_tens(input, expected):
    assert_expression_output(parse_dimension(input, ordinal=True), expected)


@pytest.mark.parametrize(
    "input, expected",
    chain(
        get_value(100, ["المية", "الميه", "المائة", "المائه", "المئة", "المئه"]),
        get_value(200, ["الميتين", "المئتين", "المئتان"]),
        get_value(
            300,
            ["الثلاثمية", "الثلاثة مائة", "التلاتمية", "الثلاثمئه"],
        ),
        get_value(
            400,
            ["الأربعمية", "الأربعة مائة", "الاربعمية", "الاربعمئه"],
        ),
        get_value(
            500,
            ["الخمسمية", "الخمسة مئة", "الخمس مائة", "الخمسميه", "الخمسه مئة"],
        ),
        get_value(
            600,
            ["الستمية", "الستة مئة", "الست مائة", "الستميه", "الستمائة"],
        ),
        get_value(
            700,
            ["السبعمية", "السبعة مئة", "السبع مائة", "السبعميه", "السبعمائة"],
        ),
        get_value(
            800,
            ["الثمنمية", "الثماني مئة", "الثمان مائة", "التمنميه", "الثمانمائة"],
        ),
        get_value(
            900,
            ["التسعمية", "التسعة مئة", "التسع مائة", "التسعميه", "التسعمائة"],
        ),
    ),
)
def test_perfect_hundreds(input, expected):
    assert_expression_output(parse_dimension(input, ordinal=True), expected)


# @pytest.mark.parametrize(
#     "input, expected",
#     chain(
#         get_value(191, ["مية وواحد وتسعين"]),
#         get_value(124, ["مائة واربعة وعشرين"]),
#         get_value(215, ["مئتين وخمسه عشر"]),
#         get_value(306, ["ثلاثمية وستة"]),
#         get_value(410, ["اربعمية وعشرة"]),
#         get_value(520, ["خمس مائة وعشرين"]),
#         get_value(606, ["ستمية وستة"]),
#         get_value(780, ["سبعة مائة وثمانون"]),
#         get_value(877, ["ثمنمية وسبعة وسبعين"]),
#         get_value(999, ["تسع مية وتسعه وتسعين"]),
#     ),
# )
# def test_hundreds(input, expected):
#     assert_expression_output(parse_dimension(input, ordinal=True), expected)


# @pytest.mark.parametrize(
#     "input, expected",
#     chain(
#         get_value(1000, ["الف", "ألف"]),
#         get_value(2000, ["ألفين", "الفين", "ألفان"]),
#         get_value(3000, ["ثلاث آلاف", "ثلاثة الاف"]),
#         get_value(4000, ["اربع الاف", "أربعة الوف"]),
#         get_value(5000, ["خمس آلاف", "خمسة ألاف"]),
#         get_value(6000, ["ست آلاف", "ستة آلاف"]),
#         get_value(7000, ["سبع آلاف", "سبعة الاف"]),
#         get_value(8000, ["ثماني آلاف", "ثمانية الاف"]),
#         get_value(9000, ["تسع آلاف", "تسعة الاف"]),
#     ),
# )
# def test_perfect_thousands(input, expected):
#     assert_expression_output(parse_dimension(input, ordinal=True), expected)


# @pytest.mark.parametrize(
#     "input, expected",
#     chain(
#         get_value(20000, ["عشرين الف"]),
#         get_value(1200, ["الف ومئتين"]),
#         get_value(3220, ["ثلاثة الاف ومئتان وعشرين"]),
#         get_value(40010, ["أربعين الف وعشرة"]),
#         get_value(55325, ["خمسة وخمسين الف وثلاثمية وخمسة وعشرين"]),
#         get_value(22222, ["اثنين وعشرين الف ومئتين واثنين وعشرين"]),
#         get_value(10465, ["عشرة الاف واربعمئة وخمسة وستين"]),
#         get_value(1030, ["الف وثلاثين"]),
#         get_value(90001, ["تسعين الف وواحد"]),
#         get_value(17100, ["سبعطعشر الف ومية"]),
#     ),
# )
# def test_thousands(input, expected):
#     assert_expression_output(parse_dimension(input, ordinal=True), expected)


# @pytest.mark.parametrize(
#     "input, expected",
#     [
#         ("10,000.0", 10000),
#         ("١٠٬٠٠٠٫٠٠٠", 10000),
#         ("-10,000", -10000),
#         ("1٬000 000", 1000000),
#         ("1 000 000", 1000000),
#         ("-١٬٠٠٠٬٠٠٠", -1000000),
#         ("+١ ٠٠٠ ٠٠٠", +1000000),
#         ("١٬٠٠٠٬٠٠٠", 1000000),
#         (".1", 0.1),
#         ("٫٠١", 0.01),
#         ("١%", 0.01),
#         ("0.01%", 0.0001),
#         (".01%", 0.0001),
#         ("20.0%", 0.2),
#         ("200%", 2),
#     ],
# )
# def test_numbers(input, expected):
#     assert_expression_output(parse_dimension(input, ordinal=True), expected)


# @pytest.mark.parametrize(
#     "expected, input",
#     [
#         (0.1, "صفر فاصلة عشرة"),
#         (0.1, "صفر فاصلة واحد"),
#         (3.4, "ثلاث فاصل اربع"),
#         (10.7, "عشرة فاصلة سبعة"),
#         (10.7, "10 فاصلة سبعة"),
#         (10.5, "10 فاصله 5"),
#         (33.3, "ثلاثة وثلاثين فاصلة ثلاثة"),
#         (100 / 3, "ثلث مية"),
#     ],
# )
# def test_fasila_numbers(input, expected):
#     assert_expression_output(parse_dimension(input, ordinal=True), expected)


# @pytest.mark.parametrize(
#     "input, expected",
#     chain(
#         get_value(1000000, ["مليون"]),
#         get_value(2000000, ["مليونين", "مليونان"]),
#         get_value(3000000, ["ثلاث ملايين", "ثلاثة مليون"]),
#         get_value(4000000, ["اربع ملايين", "أربعة مليون"]),
#         get_value(5000000, ["خمس ملايين", "خمسة مليون"]),
#         get_value(6000000, ["ست ملايين", "ستة ملايين"]),
#         get_value(7000000, ["سبع ملايين", "سبعة ملايين"]),
#         get_value(8000000, ["ثماني ملايين", "ثمانية ملايين"]),
#         get_value(9000000, ["تسع ملايين", "تسعة ملايين"]),
#     ),
# )
# def test_perfect_millions(input, expected):
#     assert_expression_output(parse_dimension(input, ordinal=True), expected)


# @pytest.mark.parametrize(
#     "input, expected",
#     chain(
#         get_value(20000000, ["عشرين مليون"]),
#         get_value(1001200, ["مليون والف ومئتين"]),
#         get_value(3022000, ["ثلاثة مليون واثنين وعشرين الف"]),
#         get_value(40000010, ["أربعين مليون وعشرة"]),
#         get_value(
#             55007325,
#             ["خمسة وخمسين مليون وسبع الاف وثلاثمية وخمسة وعشرين"],
#         ),
#         get_value(2022222, ["مليونين واثنين وعشرين الف ومئتين واثنين وعشرين"]),
#         get_value(10010465, ["عشرة مليون وعشر الاف واربعمئة وخمسة وستين"]),
#         get_value(3001030, ["ثلاث ملايين والف وثلاثين"]),
#         get_value(90090001, ["تسعين مليون وتسعين الف وواحد"]),
#         get_value(17000100, ["سبعطعشر مليون ومية"]),
#     ),
# )
# def test_millions(input, expected):
#     assert_expression_output(parse_dimension(input, ordinal=True), expected)


@pytest.mark.parametrize(
    "input",
    [
        ("واحد"),
        ("عشرين"),
        ("عشرة"),
        ("مئة"),
        ("الفتياني"),
        ("المليونير"),
        ("ولسادس"),
        ("وواثنين"),
    ],
)
def test_negative_simple_values(input: str):
    output = parse_dimension(input, ordinal=True)
    assert output == []
