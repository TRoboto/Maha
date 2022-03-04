from __future__ import annotations

import random
from itertools import chain

import pytest

from maha.parsers.functions import parse_dimension
from maha.parsers.rules.duration import *
from maha.parsers.rules.duration.template import DurationUnit, DurationValue, ValueUnit
from maha.parsers.templates import Dimension

S = DurationUnit.SECONDS
MIN = DurationUnit.MINUTES
H = DurationUnit.HOURS
D = DurationUnit.DAYS
W = DurationUnit.WEEKS
MON = DurationUnit.MONTHS
Y = DurationUnit.YEARS


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


def get_other_values(*text: str):
    positions = [
        (0.75, "{} الا ربع"),
        (0.75, "{} إلا ربع"),
        (0.25, "ربع {}"),
        (0.5, "نص {}"),
        (0.3333, "ثلث {}"),
    ]
    for t in text:
        out = random.choice(positions)
        yield (out[0], out[1].format(t))


def assert_expression_output(output, expected, unit):
    assert len(output) == 1
    output = output[0]

    assert isinstance(output.value, DurationValue)
    assert len(output.value) == 1
    assert isinstance(output.value[0], ValueUnit)
    assert pytest.approx(output.value[0].value, 0.0001) == expected
    assert output.value[0].unit == unit


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("ثانيه", "ثانية"),
        get_dual_values("ثانيتان", "ثانيتين"),
        get_numeric_values("ثانية", "ثانيه", "ثواني"),
    ),
)
def test_seconds_expression(expected, input):
    output = list(RULE_DURATION_SECONDS(input))
    assert_expression_output(output, expected, DurationUnit.SECONDS)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("دقيقة", "دقيقه"),
        get_dual_values("دقيقتين", "دقيقتان"),
        get_numeric_values("دقايق", "دقائق", "دقيقه", "دقيقة"),
    ),
)
def test_minutes_expression(expected, input):
    output = list(RULE_DURATION_MINUTES(input))
    assert_expression_output(output, expected, DurationUnit.MINUTES)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("ساعه", "ساعة"),
        get_dual_values("ساعتين", "ساعتان"),
        get_numeric_values("ساعات", "ساعه", "ساعة"),
    ),
)
def test_hours_expression(expected, input):
    output = list(RULE_DURATION_HOURS(input))
    assert_expression_output(output, expected, DurationUnit.HOURS)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("يوم"),
        get_dual_values("يومين", "يومان"),
        get_numeric_values("يوم", "يوما", "أيام", "ايام", "إيام"),
    ),
)
def test_days_expression(expected, input):
    output = list(RULE_DURATION_DAYS(input))
    assert_expression_output(output, expected, DurationUnit.DAYS)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("أسبوع", "اسبوع", "إسبوع"),
        get_dual_values("اسبوعان", "أسبوعين"),
        get_numeric_values("اسبوع", "أسبوع,", "إسبوعا", "اسابيع", "أسابيع"),
    ),
)
def test_weeks_expression(expected, input):
    output = list(RULE_DURATION_WEEKS(input))
    assert_expression_output(output, expected, DurationUnit.WEEKS)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("شهر"),
        get_dual_values("شهران", "شهرين"),
        get_numeric_values("اشهر", "أشهر", "شهور", "شهرا", "شهر"),
    ),
)
def test_months_expression(expected, input):
    output = list(RULE_DURATION_MONTHS(input))
    assert_expression_output(output, expected, DurationUnit.MONTHS)


@pytest.mark.parametrize(
    "expected,input",
    chain(
        get_singular_values("سنة", "عام", "سنه"),
        get_dual_values("عامين", "عامان", "سنتان", "سنتين"),
        get_numeric_values("أعوام", "اعوام", "سنين", "سنوات", "سنة", "عام", "سنه"),
    ),
)
def test_years_expression(expected, input):
    output = list(RULE_DURATION_YEARS(input))
    assert_expression_output(output, expected, DurationUnit.YEARS)


@pytest.mark.parametrize(
    "input",
    [
        ("اشهر"),
        ("ايام"),
        ("اسابيع"),
        ("ربع"),
        ("نص"),
        ("اسبوعات"),
        ("يومها"),
        ("3 اسنة"),
        ("دقائق واعود"),
    ],
)
def test_negative_simple_values(input: str):
    output = parse_dimension(input, duration=True)
    assert output == []


to_sec = {
    DurationUnit.SECONDS: 1,
    DurationUnit.MINUTES: 60,
    DurationUnit.HOURS: 60 * 60,
    DurationUnit.DAYS: 60 * 60 * 24,
    DurationUnit.WEEKS: 60 * 60 * 24 * 7,
    DurationUnit.MONTHS: 60 * 60 * 24 * 30,
    DurationUnit.YEARS: 60 * 60 * 24 * 365,
}


def assert_combined_expression_one_output(
    output: list[Dimension], expected: list[float], units: list[DurationUnit]
):
    """
    Asserts that the output of a combined expression is the same as the expected one.
    Only one output is expected.

    Parameters
    ----------
    output: List[:class:`Dimension`]
        The output of the combined expression.
    expected: List[float]
        The expected value of each :class:`ValueUnit`.
    units: List[DurationUnit]
        The unit of each :class:`ValueUnit`.
    """
    assert len(output) == 1
    result = output[0]

    assert isinstance(result.value, DurationValue)
    assert len(result.value) == len(units)
    normalized = 0
    for i, item in enumerate(result.value.values):
        assert isinstance(item.unit, DurationUnit)
        assert item.unit == units[i]
        assert pytest.approx(item.value, 0.001) == expected[i]
        normalized += item.value * to_sec[item.unit]

    assert result.value.normalized_value.value == normalized


@pytest.mark.parametrize(
    "expected, input",
    [
        ([10, 20], "10 دقائق و20 ثانية"),
        ([2, 1], "دقيقتين وثانية"),
        ([2, 2], "دقيقتان وثانيتان"),
        ([20, 1], "20 دقيقه وثانيه"),
        ([1, 20], "دقيقة و20 ثانية"),
        ([1, 0.5], "دقيقة ونصف ثانية"),
        ([2, 0.25], "دقيقتان وربع ثانية"),
    ],
)
def test_parse_with_combined_minutes(input: str, expected: list[float]):
    output = parse_dimension(input, duration=True)
    assert_combined_expression_one_output(
        output, expected, [DurationUnit.MINUTES, DurationUnit.SECONDS]
    )


@pytest.mark.parametrize(
    "expected,units,input,",
    [
        ([3, 10], [H, MIN], "3 ساعات و10 دقايق"),
        ([2, 1], [H, MIN], "ساعتين ودقيقة"),
        ([2, 2], [H, MIN], "ساعتان ودقيقتان"),
        ([1, 0.5], [H, MIN], "ساعة ونصف دقيقة"),
        ([1, 20], [H, MIN], "ساعة و20 دقيقة"),
        ([3, 10], [H, S], "3 ساعات و10 ثواني"),
        ([2, 1], [H, S], "ساعتين و ثانيه"),
        ([2, 2], [H, S], "ساعتان و ثانيتين"),
        ([1, 20], [H, S], "ساعة و20 ثانية"),
        ([2, 0.25], [H, S], "ساعتان وربع ثانية"),
        ([20, 1], [H, S], "20 ساعه وثانيه"),
        ([3, 30, 10], [H, MIN, S], "3 ساعات ، و 30 دقيقة و10 ثواني"),
        ([2, 10, 1], [H, MIN, S], "ساعتين و10 دقايق  و ثانيه"),
    ],
)
def test_parse_with_combined_hours(
    input: str, expected: list[float], units: list[DurationUnit]
):
    output = parse_dimension(input, duration=True)
    assert_combined_expression_one_output(output, expected, units)


@pytest.mark.parametrize(
    "expected, units, input",
    [
        ([10, 20], [D, H], "10 يوم و20 ساعات"),
        ([2, 1], [D, H], "يومين وساعة"),
        ([2, 0.75], [D, H], "يومين وساعة الا ربع"),
        ([2, 2], [D, H], "يومان وساعتان"),
        ([20, 1], [D, H], "20 يوما وساعة"),
        ([1, 20, 1], [D, H, S], "يوم و20 ساعة وثانية"),
        ([1, 0.5, 30, 2], [D, H, MIN, S], "يوم ونصف ساعة و 30 دقيقة وثانيتين"),
        ([2, 0.25, 30], [D, H, MIN], "يومين، ربع ساعة و 30 دقيقه"),
        ([3, 30, 30], [D, H, S], "3 أيام و 30 ساعة و 30 ثانية"),
        ([2, 20], [D, MIN], "يومان و 20 دقيقة"),
        ([2, 1, 40], [D, MIN, S], "يومان ودقيقة و40 ثانية"),
        ([1, 1], [D, S], "يوم وثانية"),
    ],
)
def test_parse_with_combined_days(
    input: str, expected: list[float], units: list[DurationUnit]
):
    output = parse_dimension(input, duration=True)
    assert_combined_expression_one_output(output, expected, units)


@pytest.mark.parametrize(
    "expected, units, input",
    [
        ([10, 20], [W, D], "10 اسابيع و20 يوم"),
        ([2, 1], [W, D], "أسبوعين ويوم"),
        ([2, 2], [W, D], "أسبوعان ويومان"),
        ([20, 2, 3, 40], [W, D, H, MIN], "20 اسبوع ويومين و3 ساعات و40 دقيقة"),
        (
            [20, 2, 3, 40, 1],
            [W, D, H, MIN, S],
            "20 اسبوع ويومين و3 ساعات و40 دقيقة وثانية",
        ),
        ([1, 20], [W, H], "اسبوع و20 ساعة"),
        ([1000450, 20], [W, H], "مليون واربع مئة وخمسين اسبوع و20 ساعة"),
        ([1, 0.5, 30, 50], [W, D, MIN, S], " اسبوع ونص يوم و30 دقيقة و50 ثانية"),
        ([1, 2, 50], [W, MIN, S], " اسبوع و دقيقتين و50 ثانية"),
        ([1, 2, 50], [W, H, S], " اسبوع و ساعتين و50 ثانية"),
        ([1, 2, 50], [W, D, MIN], " اسبوع و يومين و50 دقيقة"),
        ([2, 0.25], [W, H], "اسبوعان وربع ساعة"),
        ([2, 3, 0.333], [W, D, H], "أسبوعين و 3 ايام وثلث ساعة"),
    ],
)
def test_parse_with_combined_weeks(
    input: str, expected: list[float], units: list[DurationUnit]
):
    output = parse_dimension(input, duration=True)
    assert_combined_expression_one_output(output, expected, units)


@pytest.mark.parametrize(
    "expected, units, input",
    [
        ([10, 20], [MON, W], "10 اشهر و20 اسبوع"),
        ([2, 1], [MON, W], "شهرين واسبوع"),
        ([2, 2], [MON, W], "شهران واسبوعان"),
        ([20, 1], [MON, W], "20 شهرا واسبوعا"),
        ([1, 20], [MON, W], "شهر و20 أسبوع"),
        ([1, 0.5], [MON, W], "شهر ونص اسبوع"),
        ([2, 0.25], [MON, W], "شهران وربع أسبوع"),
        ([10, 20], [MON, D], "10 اشهر و20 يوم"),
        ([2, 1], [MON, D], "شهرين ويوم"),
        ([2, 2], [MON, D], "شهرين ويومان"),
        ([1500, 2], [MON, D], "الف وخمسمئة شهر ويومان"),
        ([20, 1], [MON, D], "20 شهر ويوما"),
        ([1, 20], [MON, D], "شهر و20 يوم"),
        ([3, 10, 20], [MON, W, D], "3 اشهر و10 اسابيع و20 يوم"),
        ([3, 2, 1], [MON, W, D], " 3 اشهر وأسبوعين ويوم"),
        ([11, 2, 2], [MON, W, D], "١١ شهر و أسبوعان ويومان"),
        ([1.1, 2, 2], [MON, W, D], "١.١ شهر، وأسبوعان ويومان"),
        (
            [300, 20, 2, 3, 40],
            [MON, W, D, H, MIN],
            "300 شهر، 20 اسبوع ويومين و3 ساعات و40 دقيقة",
        ),
        (
            [1, 20, 2, 3, 40, 1],
            [MON, W, D, H, MIN, S],
            "شهر و20 اسبوع ويومين و3 ساعات و40 دقيقة وثانية",
        ),
        ([3, 1, 20], [MON, W, H], "3 شهور واسبوع و20 ساعة"),
        (
            [100.564, 1, 0.5, 30, 50],
            [MON, W, D, MIN, S],
            "100.564 شهور واسبوع ونص يوم و 30 دقيقة و50 ثانية",
        ),
        ([1, 2, 50], [MON, MIN, S], " شهر و دقيقتين و50 ثانية"),
        ([1, 2, 50], [MON, H, S], " شهر و ساعتين و50 ثانية"),
        ([1, 2, 50], [MON, D, MIN], " شهر و يومين و50 دقيقة"),
        ([2, 0.25], [MON, H], "شهرين وربع ساعة"),
        ([2, 3, 0.333], [MON, D, H], "شهران و 3 ايام وثلث ساعة"),
    ],
)
def test_parse_with_combined_months(
    input: str, expected: list[float], units: list[DurationUnit]
):
    output = parse_dimension(input, duration=True)
    assert_combined_expression_one_output(output, expected, units)


@pytest.mark.parametrize(
    "expected, units, input",
    [
        ([10, 20], [Y, MON], "10 سنين و20 شهر"),
        ([1, 1], [Y, MON], "عام وشهر"),
        ([2, 1], [Y, MON], "سنتين وشهر"),
        ([2, 2], [Y, MON], "سنتان وشهرين"),
        ([177, 2], [Y, MON], "مئة وسبعة وسبعين عام وشهرين"),
        ([3, 1], [Y, MON], "3 أعوام وشهر"),
        ([20, 2], [Y, MON], "20 عام وشهران"),
        ([1, 20], [Y, D], "سنه و20 يوم"),
        ([1, 0.5], [Y, S], "سنة ونص ثانية"),
        (
            [2360, 1, 154, 0.5],
            [Y, MON, MIN, S],
            "الفين وثلاثمية وستين سنة وشهر ومية واربعة وخمسين دقيقة ونص ثانية",
        ),
        (
            [1002165, 550, 101, 10],
            [Y, W, MIN, S],
            "مليون و2 الف ومية وخمسة وستين سنة وربع الف و3 مية اسبوع ومية وواحد دقيقة وعشرة ثانية",
        ),
        ([2, 0.25], [Y, MON], "سنتين وربع شهر"),
        ([3, 0.5], [Y, MIN], "3 سنين ونصف دقيقة"),
        ([3, 3, 4, 2], [Y, MON, D, H], "3 سنين ، 3 شهور ،4 أيام وساعتين"),
        ([3, 3, 4, 2], [Y, W, D, H], "3 سنين ، 3 اسابيع ، 4 ايام ، وساعتين"),
        ([3, 3, 4], [Y, W, D], "3 سنين ، 3 اسابيع ، 4 ايام "),
    ],
)
def test_parse_with_combined_years(
    input: str, expected: list[float], units: list[DurationUnit]
):
    output = parse_dimension(input, duration=True)
    assert_combined_expression_one_output(output, expected, units)


@pytest.mark.parametrize(
    "expected, units, input",
    [
        ([1, 3], [Y, MON], "3 اشهر وسنة"),
        ([5, 5, 4], [Y, MON, S], "شهرين وثلاثة اشهر وخمسة سنين واربع ثواني"),
        ([2.5, 1], [Y, MON], "سنتين وشهر ونص سنة"),
        ([2, 2], [Y, MON], "سنتان وشهرين"),
        ([179, 5], [Y, MON], "مئة وسبعة وسبعين عام وعامين وثلاثة اشهر وشهرين"),
    ],
)
def test_parse_combination(
    input: str, expected: list[float], units: list[DurationUnit]
):
    output = parse_dimension(input, duration=True)
    assert_combined_expression_one_output(output, expected, units)
