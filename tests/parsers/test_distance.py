from __future__ import annotations

import random
from itertools import chain

import pytest

from maha.parsers.functions import parse_dimension
from maha.parsers.rules.distance import *
from maha.parsers.rules.distance.template import DistanceValue, ValueUnit
from maha.parsers.templates import Dimension, DistanceUnit

M = DistanceUnit.METERS
KM = DistanceUnit.KILOMETERS
DM = DistanceUnit.DECIMETERS
CM = DistanceUnit.CENTIMETERS
MM = DistanceUnit.MILLIMETERS
MI = DistanceUnit.MILES
YD = DistanceUnit.YARDS
FT = DistanceUnit.FEET
IN = DistanceUnit.INCHES


def get_singular_values(*text: str):
    positions = [
        (1, "{}."),
        (1, "{}"),
        (1, " {} "),
        (1, " {}"),
        (1, ",{}"),
        (1, ",{},"),
        (1, "{},"),
        (1, "{}"),
    ]
    for t in text:
        out = random.choice(positions)
        yield (out[0], out[1].format(t))


def get_dual_values(*text: str):
    positions = [
        (2, "{}"),
        (2, "{}."),
        (2, " {} "),
        (2, " {}"),
        (2, ",{}"),
        (2, ",{},"),
        (2, "{},"),
    ]

    for t in text:
        out = random.choice(positions)
        yield (out[0], out[1].format(t))


def get_numeric_values(*text: str):
    positions = [
        (1, "1 {}"),
        (1, "+1 {}"),
        (-1, "-1 {}"),
        (1, "1.0 {}"),
        (1, "1.0 {}"),
        (1.1, "1.1 {}"),
        (100000, "100 000 {}"),
        (24, "٢٤٫٠ {}"),
        (100000, "١٠٠٬٠٠٠٫٠ {}"),
        (1.1, "1.١ {}"),
        (101.12, "101.١2 {}"),
        (1564.00, "1564.00 {}"),
        (1.1, "01.1 {}"),
        (1.1, "١.١ {}"),
        (1, "١.٠ {}"),
    ]
    for t in text:
        out = random.choice(positions)
        yield (out[0], out[1].format(t))


def assert_expression_output(output, expected, unit):
    assert len(output) == 1
    output = output[0]

    assert isinstance(output.value, DistanceValue)
    assert pytest.approx(output.value.value, 0.0001) == expected
    assert output.value.unit == unit


def assert_normalized_value(output: list[Dimension], expected: float):
    assert len(output) == 1
    result = output[0]

    assert isinstance(result.value, DistanceValue)
    assert pytest.approx(result.value.normalized_value.value, 0.01) == expected


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("متر"),
        get_dual_values("متران", "مترين"),
        get_numeric_values("أمتار", "امتار", "متر", "مترا"),
    ),
)
def test_meters_expression(expected, input):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, M)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("كيلومتر", "كيلو متر", "كم"),
        get_numeric_values("كيلو متر", "كيلو مترات", "كيلومترات", "كم"),
    ),
)
def test_kilometers_expression(expected, input):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, KM)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("سنتيمتر", "سنتي متر", "سم"),
        get_numeric_values("سنتيمتر", "سنتي متر", "سم", "سنتي مترات", "سنتيمترات"),
    ),
)
def test_centimeters_expression(expected, input):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, CM)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("ديسيمتر", "ديسي متر", "دسم"),
        get_numeric_values("ديسيمتر", "ديسي متر", "دسم", "ديسي مترات", "ديسيمترات"),
    ),
)
def test_decimeters_expression(expected, input):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, DM)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("مليمتر", "ملي متر", "مم"),
        get_numeric_values("مليمتر", "ملي متر", "مم", "ملي مترات", "مليمترات"),
    ),
)
def test_millimeters_expression(expected, input):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, MM)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("ميل", "ميلا"),
        get_dual_values("ميلين", "ميلان"),
        get_numeric_values("ميل", "ميلا", "اميال", "أميال", "ميول"),
    ),
)
def test_miles_expression(expected, input):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, MI)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("ياردة", "ياردا"),
        get_numeric_values("ياردة", "يارده", "ياردا", "ياردات"),
    ),
)
def test_yards_expression(expected, input):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, YD)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("قدم", "قدما"),
        get_dual_values("قدمين", "قدمان"),
        get_numeric_values("قدم", "قدما", "أقدام", "اقدام"),
    ),
)
def test_feet_expression(expected, input):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, FT)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("بوصة", "بوصه", "إنش", "انشا"),
        get_dual_values("إنشين", "انشان", "بوصتين", "بوصتان"),
        get_numeric_values("بوصة", "بوصه", "إنش", "انشا", "انشات", "بوصات"),
    ),
)
def test_inches_expression(expected, input):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, IN)


@pytest.mark.parametrize(
    "expected, input",
    [
        (0.5, "نصف كيلو متر"),
        (0.25, "ربع كيلو متر"),
    ],
)
def test_fractions(input, expected):
    output = parse_dimension(input, distance=True)
    assert_expression_output(output, expected, KM)


@pytest.mark.parametrize(
    "expected, input",
    [
        (500, "نصف كيلو متر"),
        (250, "ربع كيلو متر"),
        (1000, "كيلو متر"),
        (1, "متر"),
        (0.5, "نصف متر"),
        (0.25, "ربع متر"),
        (91.44, "100 ياردة"),
        (2.54, "100 انش"),
        (30.48, "100 قدم"),
        (160934, "100 ميل"),
        (3218.69, "ميلين"),
    ],
)
def test_normalized_value_in_meters(input, expected):
    output = parse_dimension(input, distance=True)
    assert_normalized_value(output, expected)


@pytest.mark.parametrize(
    "input",
    [
        ("مترات"),
        ("أميال"),
        ("كيلو مترات"),
        ("ياردات"),
        ("ربع"),
        ("نص"),
        ("40 مترو"),
    ],
)
def test_negative_simple_values(input: str):
    output = parse_dimension(input, distance=True)
    assert output == []
