from datetime import datetime

import pytest

from maha.parsers.functions import parse_dimension
from maha.parsers.rules import (
    RULE_TIME_DAYS,
    RULE_TIME_HOURS,
    RULE_TIME_MINUTES,
    RULE_TIME_MONTHS,
    RULE_TIME_YEARS,
)
from maha.parsers.rules.time.template import TimeValue

NOW = datetime(2021, 9, 1)


def assert_expression_output(output, expected):
    assert len(output) == 1
    output = output[0]

    assert isinstance(output.value, TimeValue)
    assert NOW + output.value == expected


@pytest.mark.parametrize(
    "input",
    [
        ("هذي السنة"),
        ("هاي السنة"),
        ("هذا العام"),
        ("العام"),
        ("السنة هاي"),
    ],
)
def test_current_year(input):
    output = list(RULE_TIME_YEARS(input))
    assert_expression_output(output, datetime(2021, 9, 1))
    assert output[0].value == TimeValue(years=0)


@pytest.mark.parametrize(
    "input",
    [
        (" السنة السابقة"),
        ("السنة الماضية"),
        ("السنة الماضيه"),
        ("العام الماضي"),
        ("العام الفائت"),
        ("قبل سنه"),
        ("قبل  1 عام"),
    ],
)
def test_previous_year(input):
    output = list(RULE_TIME_YEARS(input))
    assert_expression_output(output, datetime(2020, 9, 1))
    assert output[0].value == TimeValue(years=-1)


@pytest.mark.parametrize(
    "input",
    [
        (" السنة الجاي"),
        ("السنة القادمة"),
        ("السنة القادمه"),
        ("العام القادم"),
        ("العام المقبل"),
        ("بعد سنه"),
        ("بعد عام"),
        ("بعد 1 سنه"),
        ("بعد  1 عام"),
    ],
)
def test_next_year(input):
    output = list(RULE_TIME_YEARS(input))
    assert_expression_output(output, datetime(2022, 9, 1))
    assert output[0].value == TimeValue(years=1)


@pytest.mark.parametrize(
    "expected_year,input",
    [
        (3, "بعد ثلاث سنين"),
        (3, "بعد ثلاث سنوات"),
        (5, "بعد 5 سنوات"),
        (20, "بعد ٢٠ عام"),
        (-100, "قبل 100 عام"),
        (-20, "قبل عشرين عام"),
        (-10, "قبل عشر عام"),
        (-25, "قبل خمسة وعشرين سنة"),
    ],
)
def test_after_before_years(expected_year, input):
    output = list(RULE_TIME_YEARS(input))
    assert_expression_output(output, datetime(expected_year + 2021, 9, 1))
    assert output[0].value == TimeValue(years=expected_year)


@pytest.mark.parametrize(
    "input",
    [
        (" السنة بعد الجاي"),
        ("العام  بعد الجاية"),
        ("السنة اللي بعد الجاي"),
        ("بعد سنتين"),
        ("بعد سنتان"),
        ("بعد عامان"),
        ("بعد عامين"),
        ("بعد  2 عام"),
    ],
)
def test_next_two_years(input):
    output = list(RULE_TIME_YEARS(input))
    assert_expression_output(output, datetime(2023, 9, 1))
    assert output[0].value == TimeValue(years=2)


@pytest.mark.parametrize(
    "input",
    [
        (" السنة قبل المنصرمة"),
        ("العام  قبل  الماضي"),
        ("السنة اللي قبل السابقة"),
        ("قبل سنتين"),
        ("قبل سنتان"),
        ("قبل عامان"),
        ("قبل عامين"),
        ("قبل 2 عام"),
    ],
)
def test_previous_two_years(input):
    output = list(RULE_TIME_YEARS(input))
    assert_expression_output(output, datetime(2019, 9, 1))
    assert output[0].value == TimeValue(years=-2)


@pytest.mark.parametrize(
    "input",
    [
        ("العام الحالي"),
        ("هذا العام"),
        ("العام"),
        ("السنة الحالية"),
        ("عام 2021"),
        ("عام الفين وواحد وعشرين"),
        ("العام الألفان والواحد والعشرون"),
    ],
)
def test_this_year(input):
    output = list(RULE_TIME_YEARS(input))
    assert_expression_output(output, datetime(2021, 9, 1))
    assert output[0].value == TimeValue(years=0) or output[0].value == TimeValue(
        year=2021
    )


# @pytest.mark.parametrize(
#     "expected_year,input",
#     [
#         (0, ""),
#     ],
# )
# def test_numeral_years(expected_year, input):
#     output = list(RULE_TIME_YEARS(input))
#     assert_expression_output(output, datetime(2021 + expected_year, 9, 1))
#     assert output[0].value == TimeValue(years=expected_year)
