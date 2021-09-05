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
        ("هاي السنة"),
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


@pytest.mark.parametrize(
    "expected_month,input",
    [
        (3, "بعد ثلاث اشهر"),
        (2, "بعد شهرين"),
        (1, "بعد شهر"),
        (-8, "قبل ثمان اشهر"),
        (-2, "قبل شهرين"),
        (-1, "قبل شهر"),
        (1, "الشهر الجاي"),
        (-1, "الشهر الماضي"),
        (2, "الشهر بعد الجاي"),
        (-2, "الشهر قبل الماضي"),
    ],
)
def test_n_months(expected_month, input):
    output = list(RULE_TIME_MONTHS(input))
    assert_expression_output(output, datetime(2021, 9 + expected_month, 1))
    assert output[0].value == TimeValue(months=expected_month)


def test_after_30_months():
    output = list(RULE_TIME_MONTHS("بعد 30 شهر"))
    assert_expression_output(output, datetime(2024, 3, 1))
    assert output[0].value == TimeValue(months=30)


@pytest.mark.parametrize(
    "expected_month,input",
    [
        (12, "شهر كانون الأول"),
        (12, "كانون الأول"),
        (12, "ديسمبر"),
        (1, "شهر 1"),
        (2, "شهر 2"),
        (2, "شباط"),
        (2, "فبراير"),
    ],
)
def test_specific_month(expected_month, input):
    output = list(RULE_TIME_MONTHS(input))
    assert_expression_output(output, datetime(2021, expected_month, 1))
    assert output[0].value == TimeValue(month=expected_month)


@pytest.mark.parametrize(
    "expected_month,input",
    [
        (11, "شهر نوفمبر القادم"),
        (11, "شهر 11 القادم"),
        (11, "شهر حدعشر القادم"),
        (11, "تشرين الثاني الجاي"),
        (12, "شهر 12 الجاي"),
        (10, "اكتوبر القادم"),
        (10, "تشرين الاول الجاي"),
        (12, "شهر كانون الاول الآتي"),
        (12, "كانون الاول الآتي"),
    ],
)
def test_next_specific_month_same_year(expected_month, input):
    output = list(RULE_TIME_MONTHS(input))
    assert_expression_output(output, datetime(2021, expected_month, 1))
    assert output[0].value == TimeValue(years=0, month=expected_month)


@pytest.mark.parametrize(
    "expected_month,input",
    [
        (11, "شهر نوفمبر بعد القادم"),
        (11, "شهر 11 بعد الجاي"),
        (10, "اكتوبر بعد التالي"),
        (2, "شباط المقبل"),
        (3, "آذار الجاي"),
        (3, "أذار الجاي"),
    ],
)
def test_next_specific_month_next_year(expected_month, input):
    output = list(RULE_TIME_MONTHS(input))
    assert_expression_output(output, datetime(2022, expected_month, 1))
    assert output[0].value == TimeValue(years=1, month=expected_month)


@pytest.mark.parametrize(
    "expected_month,input",
    [
        (11, "شهر نوفمبر الماضي"),
        (11, "شهر 11 الماضي"),
        (11, "شهر حدعشر الماض"),
        (11, "تشرين الثاني الفايت"),
        (12, "شهر 12 السابق"),
        (10, "اكتوبر الماضي"),
        (2, "شباط قبل الماضي"),
        (10, "تشرين الاول الفايت"),
        (12, "كانون الاول المنصرم"),
    ],
)
def test_previous_specific_month_previous_year(expected_month, input):
    output = list(RULE_TIME_MONTHS(input))
    assert_expression_output(output, datetime(2020, expected_month, 1))
    assert output[0].value == TimeValue(years=-1, month=expected_month)


@pytest.mark.parametrize(
    "expected_month,input",
    [
        (9, "شهر تسعة الماضي"),
        (2, "شباط الماضي"),
    ],
)
def test_previous_specific_month_same_year(expected_month, input):
    output = list(RULE_TIME_MONTHS(input))
    assert_expression_output(output, datetime(2021, expected_month, 1))
    assert output[0].value == TimeValue(years=0, month=expected_month)


@pytest.mark.parametrize(
    "input",
    [
        ("هذا الشهر"),
        ("الشهر هذا"),
        ("خلال هذا الشهر "),
    ],
)
def test_previous_this_month(input):
    output = list(RULE_TIME_MONTHS(input))
    assert_expression_output(output, datetime(2021, 9, 1))
    assert output[0].value == TimeValue(months=0)
