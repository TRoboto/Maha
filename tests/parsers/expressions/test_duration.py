import pytest

from maha.parsers.expressions.duration import (
    EXPRESSION_DURATION,
    EXPRESSION_DURATION_DAYS,
    EXPRESSION_DURATION_HOURS,
    EXPRESSION_DURATION_MINUTES,
    EXPRESSION_DURATION_MONTHS,
    EXPRESSION_DURATION_SECONDS,
    EXPRESSION_DURATION_WEEKS,
    EXPRESSION_DURATION_YEARS,
)
from maha.parsers.templates import DurationUnit
from maha.parsers.templates.expressions import ExpressionGroup


@pytest.mark.parametrize(
    "expected, input",
    [
        (1, "ثانية"),
        (1, "ثانيه"),
        (2, "ثانيتين"),
        (2, "وثانيتان"),
        (4, "4 ثواني"),
        (30, "30 ثانية"),
        (4.5, "4 ثواني ونص"),
        (3.25, "3 ثانيه و ربع"),
        (4.5, "4.5 ثانية"),
        (13.33, "13 ثانيه وثلث"),
        (2.25, "ثانيتين وربع"),
        (2.33, "ثانيتان و ثلث"),
        (2.5, "وثانيتان ونصف"),
        (2.5, "ثانيتين ونص"),
        (1.5, "ثانيه ونصف"),
        (1.25, "ثانيه وربع"),
        (1.33, "ثانية وثلث"),
        (0.75, "ثانية الا ربع"),
        (0.25, "ربع ثانيه"),
        (0.5, "نص ثانيه"),
        (0.33, "ثلث ثانيه"),
    ],
)
def test_parse_seconds_with_simple_values(input: str, expected: float):
    output = list(EXPRESSION_DURATION_SECONDS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert pytest.approx(output.value, 0.1) == expected
    assert output.expression.unit == DurationUnit.SECONDS


@pytest.mark.parametrize(
    "expected, input",
    [
        (1, "دقيقة"),
        (1, "دقيقة واعود"),
        (1, "دقيقه"),
        (2, "دقيقتين"),
        (2, "ودقيقتان"),
        (4, "4 دقايق"),
        (30, "30 دقيقة"),
        (3, "3 دقائق"),
        (4.5, "4 دقائق ونص"),
        (3.25, "3 دقيقه و ربع"),
        (4.5, "4.5 دقيقة"),
        (13 + 1 / 3, "13 دقيقه وثلث"),
    ],
)
def test_parse_minutes_with_simple_values(input: str, expected: float):
    output = list(EXPRESSION_DURATION_MINUTES.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.MINUTES


@pytest.mark.parametrize(
    "expected, input",
    [
        (135, "دقيقتين وربع"),
        (140, "دقيقتان و ثلث"),
        (150, "ودقيقتين ونصف"),
        (150, "دقيقتين ونص"),
        (90, "دقيقه ونصف"),
        (75, "دقيقه وربع"),
        (80, "دقيقة وثلث"),
        (45, "دقيقة الا ربع"),
        (15, "ربع دقيقه"),
        (30, "نص دقيقه"),
        (20, "ثلث دقيقه"),
    ],
)
def test_parse_minutes_with_more_simple_values(expected: float, input: str):
    output = list(EXPRESSION_DURATION_MINUTES.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.SECONDS


@pytest.mark.parametrize(
    "expected, input",
    [
        (1, "ساعة"),
        (1, "ساعه"),
        (2, "ساعتين"),
        (2, "وساعتان"),
        (4, "4 ساعات"),
        (30, "30 ساعة"),
        (30, "30 ساعه"),
        (3, "3 ساعات"),
        (4.5, "4 ساعات ونص"),
        (3.25, "3 ساعات وربع"),
        (4.5, "4.5 ساعة"),
        (13 + 1 / 3, "13 ساعة وثلث"),
    ],
)
def test_parse_hours_with_simple_values(input: str, expected: float):
    output = list(EXPRESSION_DURATION_HOURS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.HOURS


@pytest.mark.parametrize(
    "expected, input",
    [
        (135, "ساعتين وربع"),
        (140, "ساعتان و ثلث"),
        (150, "ساعتين ونص"),
        (150, "وساعتان ونصف"),
        (90, "ساعة ونص"),
        (75, "ساعة وربع"),
        (80, "ساعة وثلث"),
        (45, "وساعة الا ربع"),
        (15, "ربع ساعه"),
        (30, "نص ساعه"),
        (20, "ثلث ساعه"),
    ],
)
def test_parse_hours_with_more_simple_values(expected: float, input: str):
    output = list(EXPRESSION_DURATION_HOURS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.MINUTES


@pytest.mark.parametrize(
    "expected, input",
    [
        (1, "يوم"),
        (2, "يومين"),
        (2, "ويومين"),
        (2, "يومان اثنان"),
        (4, "4 ايام"),
        (30, "30 يوم"),
        (3, "3 أيام"),
        (20, "و20 يوما"),
    ],
)
def test_parse_days_with_simple_values(input: str, expected: float):
    output = list(EXPRESSION_DURATION_DAYS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.DAYS


@pytest.mark.parametrize(
    "expected, input",
    [
        (54, "يومين وربع"),
        (56, "يومين و ثلث"),
        (60, "يومين ونص"),
        (36, "يوم ونص"),
        (30, "يوم وربع"),
        (32, "يوم وثلث"),
        (18, "يوم الا ربع"),
        (6, "ربع يوم"),
        (12, "نص يوم"),
        (8, "ثلث يوم"),
    ],
)
def test_parse_days_with_more_simple_values(expected: float, input: str):
    output = list(EXPRESSION_DURATION_DAYS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.HOURS


@pytest.mark.parametrize(
    "expected, input",
    [
        (1, "أسبوع"),
        (1, "اسبوع"),
        (2, "اسبوعين"),
        (2, "وأسبوعان"),
        (4, "4 اسابيع"),
        (30, "30 أسبوع"),
        (3, "3 أسابيع"),
        (20, "و20 اسبوعا"),
    ],
)
def test_parse_weeks_with_simple_values(input: str, expected: float):
    output = list(EXPRESSION_DURATION_WEEKS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.WEEKS


@pytest.mark.parametrize(
    "expected, input",
    [
        (15.75, "أسبوعين وربع"),
        (16.33, "اسبوعين و ثلث"),
        (17.5, "اسبوعان ونص"),
        (10.5, "أسبوع ونص"),
        (8.75, "اسبوع وربع"),
        (9.33, "اسبوع وثلث"),
        (5.25, "اسبوع الا ربع"),
        (1.75, "ربع اسبوع"),
        (3.5, "نص اسبوع"),
        (2.33, "ثلث أسبوع"),
    ],
)
def test_parse_weeks_with_more_simple_values(expected: float, input: str):
    output = list(EXPRESSION_DURATION_WEEKS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert pytest.approx(output.value, 0.1) == expected
    assert output.expression.unit == DurationUnit.DAYS


@pytest.mark.parametrize(
    "expected, input",
    [
        (1, "شهر"),
        (1, "1 شهر"),
        (2, "شهرين"),
        (2, "وشهران"),
        (4, "4 أشهر"),
        (30, "30 شهر"),
        (3, "3 اشهر"),
        (20, "و20 شهرا"),
    ],
)
def test_parse_months_with_simple_values(input: str, expected: float):
    output = list(EXPRESSION_DURATION_MONTHS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.MONTHS


@pytest.mark.parametrize(
    "expected, input",
    [
        (9, "شهرين وربع"),
        (9.33, "شهرين و ثلث"),
        (10, "شهران ونص"),
        (6, "شهر ونص"),
        (5, "وشهر وربع"),
        (5.33, "شهر وثلث"),
        (3, "شهر الا ربع"),
        (1, "ربع شهر"),
        (2, "نص شهر"),
        (1.33, "ثلث شهر"),
    ],
)
def test_parse_months_with_more_simple_values(expected: float, input: str):
    output = list(EXPRESSION_DURATION_MONTHS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert pytest.approx(output.value, 0.1) == expected
    assert output.expression.unit == DurationUnit.WEEKS


@pytest.mark.parametrize(
    "expected, input",
    [
        (1, "سنة"),
        (1, "سنه"),
        (1, "عام"),
        (1, "1 عام"),
        (2, "عامين"),
        (2, "وعامان"),
        (2, "سنتان"),
        (2, "وسنتين"),
        (4, "4 سنوات"),
        (30, "30 عام"),
        (30, "30 عاما"),
        (3, "3 أعوام"),
        (3, "3 اعوام"),
        (4, "4 سنين"),
        (20, "و20 عام"),
    ],
)
def test_parse_years_with_simple_values(input: str, expected: float):
    output = list(EXPRESSION_DURATION_YEARS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.YEARS


@pytest.mark.parametrize(
    "expected, input",
    [
        (27, "عامين وربع"),
        (28, "عامان و ثلث"),
        (30, "سنتين ونص"),
        (18, "سنة ونص"),
        (15, "وعام وربع"),
        (16, "سنه وثلث"),
        (9, "سنة الا ربع"),
        (3, "ربع عام"),
        (6, "نص سنة"),
        (4, "ثلث سنه"),
    ],
)
def test_parse_years_with_more_simple_values(expected: float, input: str):
    output = list(EXPRESSION_DURATION_YEARS.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.MONTHS


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
    output = list(EXPRESSION_DURATION.parse(input))
    assert output == []


@pytest.mark.parametrize(
    "expected, input",
    [
        (620, "10 دقائق و20 ثانية"),
        (121, "دقيقتين وثانية"),
        (122, "دقيقتان وثانيتان"),
        (1201, "20 دقيقه وثانيه"),
        (80, "دقيقة و20 ثانية"),
        (60.5, "دقيقة ونصف ثانية"),
        (120.25, "دقيقتان وربع ثانية"),
    ],
)
def test_parse_combined_expressions_with_seconds(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.SECONDS


@pytest.mark.parametrize(
    "expected, input",
    [
        (190, "3 ساعات و10 دقايق"),
        (121, "ساعتين ودقيقة"),
        (122, "وساعتان ودقيقتان"),
        (80, "ساعة و20 دقيقة"),
    ],
)
def test_parse_combined_expressions_with_hours_and_minutes(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.MINUTES


@pytest.mark.parametrize(
    "expected, input",
    [
        (10810, "3 ساعات و10 ثواني"),
        (7201, "ساعتين و ثانيه"),
        (7202, "وساعتان و ثانيتين"),
        (3620, "ساعة و20 ثانية"),
        (7200.25, "ساعتان وربع ثانية"),
        (72001, "20 ساعه وثانيه"),
        (3630, "ساعة ونصف دقيقة"),
    ],
)
def test_parse_combined_expressions_with_hours_and_seconds(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.SECONDS


@pytest.mark.parametrize(
    "expected, input",
    [
        (260, "10 يوم و20 ساعات"),
        (49, "يومين وساعة"),
        (56, "يومين وثلث"),
        (50, "يومان وساعتان"),
        (481, "20 يوما وساعة"),
        (44, "يوم و20 ساعة"),
    ],
)
def test_parse_combined_expressions_with_days_and_hours(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.HOURS


@pytest.mark.parametrize(
    "expected, input",
    [
        (1470, "يوم ونصف ساعة"),
        (2895, "يومين وربع ساعة"),
        (2900, "يومان و ثلث ساعة"),
    ],
)
def test_parse_combined_expressions_with_days_and_minutes(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.MINUTES


@pytest.mark.parametrize(
    "expected, input",
    [
        (90, "10 اسابيع و20 يوم"),
        (15, "وأسبوعين ويوم"),
        (17.5, "اسبوعين ونص"),
        (16, "أسبوعان ويومان"),
        (141, "20 اسبوع ويوما"),
        (27, "اسبوع و20 يوم"),
    ],
)
def test_parse_combined_expressions_with_weeks_and_days(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.DAYS


@pytest.mark.parametrize(
    "expected, input",
    [
        (180, "اسبوع ونص يوم"),
        (342, "اسبوعان وربع يوم"),
        (344, "أسبوعين و ثلث يوم"),
    ],
)
def test_parse_combined_expressions_with_weeks_and_hours(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.HOURS


@pytest.mark.parametrize(
    "expected, input",
    [
        (60, "10 اشهر و20 اسبوع"),
        (9, "وشهرين واسبوع"),
        (10, "شهرين ونص"),
        (10, "شهران واسبوعان"),
        (81, "20 شهرا واسبوعا"),
        (24, "شهر و20 أسبوع"),
    ],
)
def test_parse_combined_expressions_with_months_and_weeks(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.WEEKS


@pytest.mark.parametrize(
    "expected, input",
    [
        (33.5, "شهر ونص اسبوع"),
        (61.75, "شهران وربع أسبوع"),
        (320, "10 اشهر و20 يوم"),
        (61, "وشهرين ويوم"),
        (62, "شهرين ويومان"),
        (601, "20 شهر ويوما"),
        (50, "شهر و20 يوم"),
    ],
)
def test_parse_combined_expressions_with_months_and_days(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.DAYS


@pytest.mark.parametrize(
    "expected, input",
    [
        (140, "10 سنين و20 شهر"),
        (13, "عام وشهر"),
        (25, "وسنتين وشهر"),
        (30, "عامان ونصف"),
        (26, "سنتان وشهرين"),
        (37, "3 أعوام وشهر"),
        (242, "20 عام وشهران"),
        (32, "سنه و20 شهر"),
    ],
)
def test_parse_combined_expressions_with_years_and_months(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.MONTHS


@pytest.mark.parametrize(
    "expected, input",
    [
        (50, "سنة ونص شهر"),
        (97, "سنتين وربع شهر"),
        (146, "3 سنين ونصف شهر"),
    ],
)
def test_parse_combined_expressions_with_years_and_weeks(input: str, expected: float):
    output = list(EXPRESSION_DURATION.parse(input))
    assert len(output) == 1
    output = output[0]

    assert output.value == expected
    assert output.expression.unit == DurationUnit.WEEKS


def test_parse_with_confident_first():
    NEW_EXPRESSIONS = ExpressionGroup(
        *EXPRESSION_DURATION_YEARS.expressions[::-1], confident_first=True, smart=True
    )
    output = list(NEW_EXPRESSIONS.parse("20 سنة"))
    assert len(output) == 1
    output = output[0]

    assert output.value == 20
    assert output.expression.unit == DurationUnit.YEARS


def test_parse_with_confident_not_first():
    NEW_EXPRESSIONS = ExpressionGroup(
        *EXPRESSION_DURATION_YEARS.expressions[::-1], smart=True
    )
    output = list(NEW_EXPRESSIONS.parse("20 سنة"))
    assert len(output) == 2

    assert output[0].value == 1
    assert output[1].value == 20


def test_parse_with_smart_off():
    NEW_EXPRESSIONS = ExpressionGroup(
        *EXPRESSION_DURATION.expressions, confident_first=True
    )
    output = list(NEW_EXPRESSIONS.parse("10 سنين و20 شهر"))
    assert len(output) == 4

    for i, val in enumerate([140, 10, 20, 1]):
        assert output[i].value == val
