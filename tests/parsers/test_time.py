from datetime import datetime

import pytest
from dateutil.relativedelta import MO, SA, TU
from hijri_converter import Gregorian, Hijri

from maha.parsers.functions import parse_dimension
from maha.parsers.rules.time import constants
from maha.parsers.rules.time.template import TimeInterval, TimeValue

DATE = datetime(2021, 9, 1)
NOW = DATE.replace(hour=10, minute=38, second=4)
HIJRI_DATE = Gregorian.fromdate(DATE).to_hijri()


def assert_expression_output(output, expected):
    assert len(output) == 1
    output = output[0]

    assert isinstance(output.value, TimeValue)
    assert NOW + output.value == expected


def assert_hijri_expression_output(output, expected: Hijri):
    assert len(output) == 1
    output = output[0]

    assert isinstance(output.value, TimeValue)
    result = DATE + output.value
    assert Gregorian(result.year, result.month, result.day).to_hijri() == expected


def assert_expression_date_output(output, expected):
    assert len(output) == 1
    output = output[0]

    assert isinstance(output.value, TimeValue)
    assert DATE + output.value == expected


@pytest.mark.parametrize(
    "input",
    [
        ("هذي السنة"),
        ("هاي السنة"),
        ("هذا العام"),
        ("هاد العام"),
        ("العام"),
        ("السنة هاي"),
    ],
)
def test_current_year(input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 9, 1))
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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2020, 9, 1))
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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2022, 9, 1))
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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(expected_year + 2021, 9, 1))
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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2023, 9, 1))
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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2019, 9, 1))
    assert output[0].value == TimeValue(years=-2)


@pytest.mark.parametrize(
    "input",
    [
        ("العام الحالي"),
        ("هذا العام"),
        ("هاد العام"),
        ("العام"),
        ("السنة الحالية"),
        ("عام 2021"),
        ("هاي السنة"),
        ("عام الفين وواحد وعشرين"),
        ("العام الألفان والواحد والعشرون"),
    ],
)
def test_this_year(input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 9, 1))
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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 9 + expected_month, 1))
    assert output[0].value == TimeValue(months=expected_month)


def test_after_30_months():
    output = parse_dimension("بعد 30 شهر", time=True)
    assert_expression_date_output(output, datetime(2024, 3, 1))
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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, expected_month, 1))
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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, expected_month, 1))


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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2022, expected_month, 1))


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
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2020, expected_month, 1))


@pytest.mark.parametrize(
    "expected_month,input",
    [
        (9, "شهر تسعة الماضي"),
        (2, "شباط الماضي"),
    ],
)
def test_previous_specific_month_same_year(expected_month, input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, expected_month, 1))


@pytest.mark.parametrize(
    "input",
    [
        ("هذا الشهر"),
        ("هاد الشهر"),
        ("الشهر هذا"),
        ("خلال هذا الشهر "),
    ],
)
def test_previous_this_month(input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 9, 1))
    assert output[0].value == TimeValue(months=0)


@pytest.mark.parametrize(
    "expected_week,expected_date,input",
    [
        (3, DATE.replace(day=19), "بعد ثلاث اسابيع"),
        (2, DATE.replace(day=12), "بعد اسبوعين"),
        (1, DATE.replace(day=5), "بعد أسبوع"),
        (1, DATE.replace(day=5), "الأسبوع الجاي"),
        (2, DATE.replace(day=12), "الأسبوع بعد  القادم"),
        (0, DATE.replace(day=1), "هذا الأسبوع"),
        (0, DATE.replace(day=1), " الأسبوع"),
    ],
)
def test_next_weeks(expected_week, expected_date, input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, expected_date)
    assert output[0].value == TimeValue(weeks=expected_week)


@pytest.mark.parametrize(
    "expected_week,expected_date,input",
    [
        (-1, DATE.replace(month=8, day=22), "قبل إسبوع"),
        (-1, DATE.replace(month=8, day=22), "الإسبوع الماضي"),
        (-1, DATE.replace(month=8, day=22), "الاسبوع السابق"),
        (-2, DATE.replace(month=8, day=15), "الأسبوع قبل الماضي"),
        (-4, DATE.replace(month=8, day=1), "قبل اربعة أسابيع"),
        (-2, DATE.replace(month=8, day=15), "قبل  أسبوعان"),
    ],
)
def test_previous_weeks(expected_week, expected_date, input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, expected_date)
    assert output[0].value == TimeValue(weeks=expected_week)


@pytest.mark.parametrize(
    "expected_day,input",
    [
        (3, "بعد ثلاث ايام"),
        (3, "بعد 3 أيام"),
        (3, "بعد تلاتة أيام"),
        (21, "بعد واحد وعشرين يوم"),
        (1, "بعد يوم"),
        (2, "بعد يومان"),
        (1, "بكرة"),
        (1, "بكره"),
        (1, "الغد"),
        (1, "غدا"),
        (2, "بعد بكرة"),
        (1, "اليوم الجاي"),
        (2, "اليوم بعد  القادم"),
        (0, "هذا اليوم"),
        (0, "هاد اليوم"),
        (0, " اليوم"),
    ],
)
def test_next_days(expected_day, input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 9, 1 + expected_day))
    assert output[0].value == TimeValue(days=expected_day)


@pytest.mark.parametrize(
    "expected_day,input",
    [
        (-1, "قبل يوم"),
        (-1, "اليوم المنصرم"),
        (-1, "اليوم الماضي"),
        (-1, "البارحة"),
        (-1, "مبارح"),
        (-1, "امبارح"),
        (-2, "اول مبارح"),
        (-2, "اليوم قبل الماضي"),
        (-20, "قبل عشرين يوم"),
        (-10, "قبل عشرة يوم"),
        (-10, "قبل عشر يوم"),
        (-10, "قبل 10 يوم"),
        (-1, "قبل 1 يوم"),
        (-2, "قبل  يومين"),
    ],
)
def test_previous_days(expected_day, input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 8, 32 + expected_day))
    assert output[0].value == TimeValue(days=expected_day)


@pytest.mark.parametrize(
    "expected_day,input",
    [
        (7, "يوم الثلاثاء الجاي"),
        (1, "الأربعا "),
        (1, "هذا الأربعاء"),
        (2, "الخميس"),
        (2, "هذا الخميس"),
        (2, "الخميس القادم "),
        (5, "يوم الأحد"),
        (5, "يوم الأحد القادم"),
        (5, "الاحد الجاي"),
        (6, "الاثنين"),
        (7, "الثلاثا"),
        (7, "ثلاثاء"),
        (8, "الأربعاء القادم "),
        (15, "الاربعا بعد الجاي "),
        (9, "الخميس بعد القادم"),
        (9, "يوم الخميس بعد الجاي"),
    ],
)
def test_specific_next_weekday(expected_day, input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 9, expected_day))


@pytest.mark.parametrize(
    "expected_day,input",
    [
        (31, "يوم الثلاثاء الماضي"),
        (25, "الأربعا الماض"),
        (26, "الخميس السابق "),
        (29, "يوم الأحد الماضي"),
        (27, "الجمعة الماضية"),
        (28, "السبت الماضي"),
        (30, "الإثنين الماضي"),
        (18, "الاربعا قبل المنصرم "),
        (24, "الثلاثاء قبل الماضي"),
        (23, "يوم الإثنين قبل المنصرم"),
    ],
)
def test_specific_previous_weekday(expected_day, input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 8, expected_day))


@pytest.mark.parametrize(
    "expected_hour,input",
    [
        (3, "الساعة ثلاثة "),
        (3, "الساعة 3 "),
        (3, "الساعة الثالثة "),
        (5, "الساعة الخامسة "),
        (1, "الساعة الأولى "),
        (1, "الساعة الواحدة "),
        (1, "الساعة 1 "),
        (10, "الساعة 10 "),
        (2, "الساعة الثانية "),
        (12, "الساعة الثانية عشرة "),
        (12, "الساعة 12 "),
        (12, "الساعة اطنعش "),
    ],
)
def test_specific_hour(expected_hour, input):
    output = parse_dimension(input, time=True)
    assert_expression_output(output, datetime(2021, 9, 1, expected_hour))
    assert output[0].value == TimeValue(
        hour=expected_hour, minute=0, second=0, microsecond=0
    )


@pytest.mark.parametrize(
    "expected_hour,input",
    [
        (5, "بعد خمسة ساعات"),
        (6, "بعد 6 ساعات"),
        (13, "بعد ثلاثة عشر ساعات"),
        (1, "بعد ساعة"),
        (1, "بعد ساعة واحدة"),
        (2, "بعد ساعتين "),
        (2, "بعد ساعتان "),
        (2, "الساعة بعد الجاي"),
        (1, "الساعة الجاي"),
        (1, "الساعة الجاية"),
        (1, "الساعة المقبله"),
        (1, "الساعة القادمة"),
        (0, "الساعة "),
        (0, "هذه الساعة "),
        (0, "هذي الساعة "),
    ],
)
def test_after_hours(expected_hour, input):
    output = parse_dimension(input, time=True)
    assert_expression_output(output, NOW.replace(hour=NOW.hour + expected_hour))
    assert output[0].value == TimeValue(hours=expected_hour)


@pytest.mark.parametrize(
    "expected_hour,input",
    [
        (-5, "قبل خمسة ساعات"),
        (-6, "قبل 6 ساعات"),
        (-10, "قبل عشر ساعات"),
        (-1, "قبل ساعة"),
        (-1, "قبل ساعة واحدة"),
        (-2, "قبل ساعتين "),
        (-2, "قبل ساعتان "),
        (-2, "الساعة قبل الماضية"),
        (-1, "الساعة الماضية"),
        (-1, "الساعة السابقة"),
        (-1, "الساعة الفائتة"),
    ],
)
def test_before_hours(expected_hour, input):
    output = parse_dimension(input, time=True)
    assert_expression_output(output, NOW.replace(hour=NOW.hour + expected_hour))
    assert output[0].value == TimeValue(hours=expected_hour)


@pytest.mark.parametrize(
    "expected_minute,input",
    [
        (3, "الدقيقة ثلاثة "),
        (3, "ثلاث دقائق"),
        (10, "عشرة دقايق"),
        (3, "الدقيقة 3 "),
        (3, "الدقيقة الثالثة "),
        (5, "الدقيقة الخامسة "),
        (1, "الدقيقة الأولى "),
        (1, "الدقيقة الواحدة "),
        (1, "الدقيقة 1 "),
        (10, "الدقيقة 10 "),
        (59, "الدقيقة 59 "),
        (59, "الدقيقة تسعة وخمسين "),
        (59, " تسعة وخمسين دقيقة"),
        (2, "الدقيقة الثانية "),
        (12, "12 دقيقه"),
        (12, "الدقيقة الثانية عشرة "),
        (12, "الدقيقة 12 "),
        (12, "الدقيقة اطنعش "),
    ],
)
def test_specific_minute(expected_minute, input):
    output = parse_dimension(input, time=True)
    assert_expression_output(output, datetime(2021, 9, 1, NOW.hour, expected_minute))
    assert output[0].value == TimeValue(minute=expected_minute, second=0, microsecond=0)


@pytest.mark.parametrize(
    "expected_minute,input",
    [
        (5, "بعد خمسة دقائق"),
        (6, "بعد 6 دقائق"),
        (21, "بعد واحد وعشرين دقائق"),
        (1, "بعد دقيقه"),
        (1, "بعد دقيقه واحدة"),
        (2, "بعد دقيقتين "),
        (2, "بعد دقيقتان "),
        (2, "الدقيقه بعد الجاي"),
        (1, "الدقيقه الجاي"),
        (1, "الدقيقه الجاية"),
        (1, "الدقيقه المقبله"),
        (1, "الدقيقه القادمة"),
        (0, "الدقيقه "),
        (0, "هذه الدقيقه "),
        (0, "هذي الدقيقه "),
    ],
)
def test_after_minutes(expected_minute, input):
    output = parse_dimension(input, time=True)
    assert_expression_output(output, NOW.replace(minute=NOW.minute + expected_minute))
    assert output[0].value == TimeValue(minutes=expected_minute)


@pytest.mark.parametrize(
    "expected_minute,input",
    [
        (-5, "قبل خمسة دقايق"),
        (-30, "قبل 30 دقيقة"),
        (-21, "قبل واحد وعشرين دقايق"),
        (-1, "قبل دقيقة"),
        (-1, "قبل دقيقة واحدة"),
        (-2, "قبل دقيقتين "),
        (-2, "قبل دقيقتان "),
        (-2, "الدقيقة قبل الماضية"),
        (-1, "الدقيقة الماضية"),
        (-1, "الدقيقة السابقة"),
        (-1, "الدقيقة الفائتة"),
    ],
)
def test_before_minutes(expected_minute, input):
    output = parse_dimension(input, time=True)
    assert_expression_output(output, NOW.replace(minute=NOW.minute + expected_minute))
    assert output[0].value == TimeValue(minutes=expected_minute)


@pytest.mark.parametrize(
    "input",
    [
        ("قبل الظهر"),
        ("الفجر"),
        ("الظهر"),
        ("الصبح"),
        ("في الصباح"),
        ("صباحا"),
        ("ظهرا"),
        ("فجرا"),
        ("بعد الفجر"),
        ("فجر"),
    ],
)
def test_am(input):
    output = parse_dimension(input, time=True)
    assert output[0].value == TimeValue(am_pm="AM")


@pytest.mark.parametrize(
    "input",
    [
        ("بعد الظهر"),
        ("العصر"),
        ("المغرب"),
        ("العشاء"),
        ("بعد العشا"),
        ("قبل المغرب"),
        ("في الليل"),
        ("الليلة"),
        ("الليله"),
        ("المسا"),
        ("مساء"),
        ("مساءا"),
    ],
)
def test_pm(input):
    output = parse_dimension(input, time=True)
    assert output[0].value == TimeValue(am_pm="PM")


@pytest.mark.parametrize(
    "input",
    [
        ("حالا"),
        ("في الحال"),
        ("هسة"),
        ("هسا"),
        ("الآن"),
        ("هاي اللحظة"),
        ("هذا الوقت"),
        ("هاد الوقت"),
    ],
)
def test_now(input):
    output = parse_dimension(input, time=True)
    assert output[0].value == TimeValue(
        years=0, months=0, days=0, hours=0, minutes=0, seconds=0
    )


@pytest.mark.parametrize(
    "input",
    [
        ("خلال اول شهر 9"),
        ("اول شهر سبتمبر"),
        ("اول  سبتمبر"),
        ("1  سبتمبر"),
        ("الأول من ايلول"),
        ("الأول من شهر ايلول"),
        ("1/9"),
    ],
)
def test_first_day_and_month(input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 9, 1))


@pytest.mark.parametrize(
    "input",
    [
        ("شهر 9 2021"),
        ("  سبتمبر 2021"),
        (" شهر سبتمبر عام الفين وواحد وعشرين"),
        ("9/2021"),
    ],
)
def test_month_and_year(input):
    output = parse_dimension(input, time=True)
    assert_expression_date_output(output, datetime(2021, 9, 1))


@pytest.mark.parametrize(
    "expected,input",
    [
        (DATE.replace(day=2, hour=17), "بكرة على الخمسة العصر"),
        (NOW.replace(day=16), "الخميس الموافق السادس عشر من هذا الشهر"),
        (NOW.replace(day=16), "الخميس الموافق 16 من هذا الشهر"),
        (NOW.replace(day=16), "الخميس بعد اسبوعين"),
        (NOW.replace(day=16, month=10), "الخميس الموافق السادس عشر من شهر 10"),
        (NOW.replace(day=4, month=11), "بعد شهرين يوم الخميس "),
        (NOW.replace(day=6, month=8), "الجمعة 6/8"),
        (NOW.replace(day=9, month=10), "السبت 9 اكتوبر"),
        (NOW.replace(day=13, month=2), "شباط 13"),
        (NOW.replace(day=14, month=2), "شباط الرابع عشر"),
        (NOW.replace(month=2, day=2), "الثاني من شباط"),
        (NOW.replace(month=10, day=14), "14 الشهر الجاي"),
        (NOW.replace(month=7, day=11), "الحادي عشر من الشهر قبل الماضي"),
        (NOW.replace(year=2022, month=2, day=3), "3 شباط القادم"),
        (NOW.replace(month=2, day=10), "العاشر من شهر شباط"),
        (NOW.replace(month=3, day=10), "10 اذار"),
        (NOW.replace(month=8, day=25), "الأربعا الأسبوع الماضي"),
        (DATE.replace(day=4, hour=1, minute=30), "السبت هذا الأسبوع الساعة 1 ونص"),
        (DATE.replace(hour=4, minute=30), "الساعة اربعة ونص"),
        (NOW.replace(day=31, month=10), "آخر يوم بالشهر الجاي"),
        (NOW.replace(day=30), "آخر يوم من  الشهر الحالي"),
        (NOW.replace(day=28), "آخر ثلاثا"),
        (NOW.replace(day=4, month=8), "اول اربعا من الشهر الماضي"),
        (NOW.replace(day=25, month=8), "اخر اربعا من الشهر الماضي"),
        (NOW.replace(day=3, month=2, year=2022), "ثالث يوم من شهر 2 السنة الجاي"),
        (NOW.replace(day=15, month=5, year=2020), "ثالث جمعة من شهر 5 السنة الماضية"),
        (DATE.replace(hour=7, minute=10, month=8, day=31), "الساعة 7 وعشر دقايق مبارح"),
        (DATE.replace(hour=15, minute=15), "الساعة 3 و15 دقيقة العصر"),
        (DATE.replace(hour=15, minute=20), "الساعة 3 وثلث مساءا"),
        (DATE.replace(hour=2, minute=45), "الساعة 3 الا ربع الفجر"),
        (DATE.replace(hour=12, minute=30), "12 ونص مساء"),
        (DATE.replace(hour=12, minute=30), "الثانية عشرة والنصف مساء"),
        (DATE.replace(hour=12, minute=49), "الساعة الثانية عشر وتسعة واربعون دقيقة"),
        (DATE.replace(hour=5, minute=50), "الساعة خمسة وخمسين دقيقة"),
        (NOW.replace(year=1040), "في العام الف واربعين"),
        (
            DATE.replace(day=5, hour=16),
            "الأسبوع القادم يوم الأحد الساعة 4 العصر",
        ),
        (
            NOW.replace(day=20),
            "بعد 3 اسابيع يوم الإثنين",
        ),
        (
            NOW.replace(month=8, day=25, hour=9),
            "الأسبوع الماضي يوم الأربعاء قبل ساعة",
        ),
        (
            NOW.replace(day=15),
            "هذا الوقت بعد اسبوعين",
        ),
        (
            NOW.replace(day=15),
            "هذا الوقت بعد اسبوعين يوم الأربعاء",
        ),
        (
            NOW.replace(day=16),
            "هذا الوقت بعد اسبوعين يوم الخميس",
        ),
        (
            DATE.replace(year=2061, day=21, month=11, hour=2),
            "بعد اربعين سنة الموافق 21/11 خلال الساعة الثانية فجرا",
        ),
        (
            DATE.replace(day=3, hour=20, minute=40),
            "بعد الغد عند الساعه تسعة الا ثلث في الليل",
        ),
        (DATE.replace(hour=3, minute=20), "3:20"),
        (
            DATE.replace(hour=11, minute=2, second=40, month=8, day=30),
            "اول مبارح الساعة 11:2:40",
        ),
        (NOW, "1/9/2021"),
        (
            DATE.replace(day=11, month=10, hour=13, minute=15),
            "الاثنين 11/10 الساعة الواحدة والربع بعد الظهر",
        ),
        (
            DATE.replace(day=4, hour=13, minute=30),
            "السبت الأسبوع الحالي الساعة 1 ونص بعد الظهر",
        ),
    ],
)
def test_time(expected, input):
    output = parse_dimension(input, time=True)
    assert_expression_output(output, expected)


@pytest.mark.parametrize(
    "expected,input",
    [
        (NOW.replace(day=30), "آخر خميس من شهر 9"),
        (NOW.replace(day=29), "آخر اربعاء من شهر 9"),
        (NOW.replace(day=22, month=2), "آخر اثنين من شهر شباط"),
        (NOW.replace(day=28, month=2), "آخر احد من شهر شباط"),
    ],
)
def test_last_specific_day_of_specific_month(expected, input):
    output = parse_dimension(input, time=True)
    assert_expression_output(output, expected)


@pytest.mark.parametrize(
    "expected,input",
    [
        (Hijri(1443, 5, 2), "أول اثنين من شهر جمادى الأول من عام 1443"),
        (Hijri(1443, 6, 29), "أخر يوم من شهر جمادى الآخرة من العام الحالي"),
        (Hijri(1443, 4, HIJRI_DATE.day), "بعد ثلاث اشهر من شهر محرم"),
        (Hijri(1443, 1, HIJRI_DATE.day), "شهر محرم"),
        (Hijri(1444, 1, HIJRI_DATE.day), "شهر محرم القادم"),
        (Hijri(1442, 1, HIJRI_DATE.day), "شهر محرم قبل الماضي"),
        (Hijri(1400, 5, 10), "10 شهر جمادى الأول من عام 1400 "),
        (Hijri(1400, HIJRI_DATE.month, HIJRI_DATE.day), "عام 1400 هجري"),
        (Hijri(HIJRI_DATE.year, 8, 10), "بعد تسعة وثلاثين يوم من اول رجب"),
        (Hijri(1443, 9, 1), "بداية رمضان القادم"),
        (Hijri(HIJRI_DATE.year - 1, 9, 1), "بداية رمضان الماضي"),
        (
            Hijri(HIJRI_DATE.year + 3, HIJRI_DATE.month, HIJRI_DATE.day),
            "بعد ثلاث سنوات هجرية",
        ),
        (
            Hijri(HIJRI_DATE.year + 1, HIJRI_DATE.month, HIJRI_DATE.day),
            "بعد سنة هجرية",
        ),
        (
            Hijri(HIJRI_DATE.year + 1, HIJRI_DATE.month, HIJRI_DATE.day),
            "العام الهجري القادم",
        ),
        (
            Hijri(HIJRI_DATE.year + 1, HIJRI_DATE.month, HIJRI_DATE.day),
            "السنة الهجرية القادمة",
        ),
        (
            Hijri(HIJRI_DATE.year + 2, HIJRI_DATE.month, HIJRI_DATE.day),
            "السنة الهجرية بعد القادمة",
        ),
        (
            Hijri(HIJRI_DATE.year + 2, HIJRI_DATE.month, HIJRI_DATE.day),
            "بعد عامين هجريين",
        ),
        (
            Hijri(HIJRI_DATE.year + 2, HIJRI_DATE.month, HIJRI_DATE.day),
            "بعد سنتان هجريتان",
        ),
        (
            Hijri(HIJRI_DATE.year - 1, HIJRI_DATE.month, HIJRI_DATE.day),
            "السنة الهجرية السابقة",
        ),
        (
            Hijri(HIJRI_DATE.year - 2, HIJRI_DATE.month, HIJRI_DATE.day),
            "السنة الهجرية قبل الماضية",
        ),
        (
            Hijri(HIJRI_DATE.year, 4, HIJRI_DATE.day + 3),
            "بعد ثلاث ايام في شهر ربيع الثاني",
        ),
    ],
)
def test_hijri_date(expected, input):
    output = parse_dimension(input, time=True)
    assert_hijri_expression_output(output, expected)


def test_class_retains_values():
    out = parse_dimension("26 من شهر محرم من عام 1443", time=True)
    assert_hijri_expression_output(out, Hijri(1443, 1, 26))
    assert out == parse_dimension("26 من شهر محرم من عام 1443", time=True)


@pytest.mark.parametrize(
    "sow,expected,input",
    [
        (MO, NOW.replace(day=12), "الأسبوع القادم يوم الأحد"),
        (MO, NOW.replace(day=6), "الأسبوع القادم"),
        (MO, NOW.replace(day=6), "الأسبوع القادم يوم الإثنين"),
        (SA, NOW.replace(day=5), "الأسبوع القادم يوم الأحد"),
        (TU, NOW.replace(day=7), "الأسبوع القادم"),
        (MO, NOW.replace(month=8, day=29), "الأسبوع الماضي يوم الأحد"),
        (TU, NOW.replace(month=8, day=24), "الأسبوع الماضي يوم الثلاثاء"),
        (TU, NOW.replace(month=8, day=30), "الأسبوع الماضي يوم الاثنين"),
        (TU, NOW.replace(month=8, day=30), "الأسبوع الماضي يوم الاثنين"),
    ],
)
def test_different_start_of_week(sow, expected, input, monkeypatch):
    monkeypatch.setattr(constants, "START_OF_WEEK", sow.weekday)
    output = parse_dimension(input, time=True)
    assert_expression_output(output, expected)


@pytest.mark.parametrize(
    "expected,input",
    [
        (
            DATE.replace(day=11, month=10, hour=1),
            "يوم الاثنين 11-10-2021 الساعه الواحدة ظهرا",
        ),
        (
            NOW.replace(day=21, month=11, year=2010),
            "يوم الأحد 21-11-2010 ",
        ),
        (
            NOW.replace(day=28, month=11, year=2010),
            "يوم الأحد 25-11-2010 ",
        ),
    ],
)
def test_full_date_with_specific_day(expected, input):
    output = parse_dimension(input, time=True)
    assert_expression_output(output, expected)


def assert_interval_output(output, start_time, end_time):
    assert len(output) == 1
    output = output[0]

    value = output.value
    assert isinstance(value, TimeInterval)

    if start_time is not None:
        assert isinstance(value.start, TimeValue)
        assert NOW + value.start == start_time
    else:
        assert value.start is None
    if end_time is not None:
        assert isinstance(value.end, TimeValue)
        assert NOW + value.end == end_time
    else:
        assert value.end is None


@pytest.mark.parametrize(
    "start_time,end_time,input",
    [
        (
            NOW,
            NOW.replace(year=2022),
            "من سنة 2021 الى سنة 2022",
        ),
        (
            NOW.replace(hour=4, minute=30, second=0),
            None,
            "من الساعة 4 ونص",
        ),
        (
            NOW.replace(hour=16, minute=50, second=0),
            NOW.replace(hour=17, minute=50, second=0),
            "من الساعة 4 وخمسين دقيقة مساء للساعة خمسة وخمسين دقيقة",
        ),
        (
            NOW.replace(hour=16, minute=30, second=0),
            NOW.replace(hour=17, minute=0, second=0),
            "من الساعة 4 ونص  للخمسة بعد العصر",
        ),
        (
            NOW.replace(day=5, hour=21, minute=0, second=0),
            NOW.replace(day=5, hour=23, minute=0, second=0),
            "الأحد من الساعة 9 الى 11 مساء",
        ),
        (
            NOW.replace(hour=7, minute=45, second=0),
            NOW.replace(hour=11, minute=15, second=0),
            "من الساعة الثامنة الا ربع وحتى الساعة الحادية عشر وربع صباحا",
        ),
        (
            NOW.replace(hour=8, minute=15, second=0),
            NOW.replace(hour=23, minute=0, second=0),
            "الساعة الثامنة والربع صباحا الى 11 مساء",
        ),
        (
            None,
            NOW.replace(hour=22, minute=45, second=0),
            "حتى الساعة الحادية عشر الا ربع مساء",
        ),
        (
            NOW.replace(hour=19, minute=0, second=0),
            NOW.replace(day=2, hour=5, minute=20, second=0),
            "من السابعة مساء الى الخامسة والثلث صباحا يوم غد",
        ),
        (
            NOW.replace(day=2, hour=14, minute=45, second=0),
            NOW.replace(day=2, hour=17, minute=0, second=0),
            "غدا من الساعة الثالثة الا ربع الى الخامسة مساء",
        ),
        (
            NOW,
            NOW.replace(day=31, month=10),
            "من الآن لآخر يوم بشهر 10",
        ),
        (
            NOW.replace(day=13, month=2),
            NOW.replace(day=15, month=7),
            "من شباط 13 الى 15 تموز",
        ),
        (
            NOW.replace(month=3),
            NOW.replace(day=15, month=3, year=2022),
            "من شهر ثلاث السنة الحالية الى 15 آذار السنة القادمة",
        ),
        (
            NOW.replace(hour=11),
            NOW.replace(hour=15, minute=30, second=0),
            "من بعد ساعة الى الساعة 3 ونصف مساء",
        ),
        (
            None,
            NOW.replace(year=2025),
            "الى سنة 2025",
        ),
        (
            NOW.replace(year=2021),
            NOW.replace(year=2023),
            "من العام الحالي للعام بعد القادم",
        ),
        (
            NOW.replace(year=2021, month=10),
            NOW.replace(year=2022),
            "من شهر 10 سنة 2021 الى سنة 2022",
        ),
    ],
)
def test_time_interval(start_time, end_time, input):
    output = parse_dimension(input, time=True)
    assert_interval_output(output, start_time, end_time)


@pytest.mark.parametrize(
    "start_time,end_time,input",
    [
        (
            NOW.replace(hour=16, minute=0, second=0),
            NOW.replace(hour=17, minute=0, second=0),
            "من الأربعة للخمسة بعد العصر",
        ),
        (
            NOW.replace(hour=6, minute=0, second=0),
            NOW.replace(hour=7, minute=0, second=0),
            "من الستة للسبعة",
        ),
        (
            NOW.replace(hour=4, minute=30, second=0),
            NOW.replace(hour=5, minute=0, second=0),
            "من الأربعة ونص للخمسة",
        ),
        (
            NOW.replace(hour=4, minute=0, second=0),
            NOW.replace(hour=5, minute=15, second=0),
            "من الأربعة للخمسة وربع صباحا",
        ),
        (
            NOW.replace(hour=10, minute=20, second=0),
            NOW.replace(hour=11, minute=0, second=0),
            "من العشرة وعشرين دقيقة لل11 الصبح",
        ),
        (
            NOW.replace(hour=9, minute=20, second=0),
            NOW.replace(hour=9, minute=45, second=0),
            "من 9 وعشرين دقيقة لل عشرة الا ربع الصبح",
        ),
        (
            NOW.replace(day=2, hour=16, minute=0, second=0),
            NOW.replace(day=2, hour=17, minute=0, second=0),
            "بكرة من الاربعة العصر للخمسة",
        ),
        (
            NOW.replace(hour=16, minute=0, second=0),
            NOW.replace(day=2, hour=17, minute=0, second=0),
            "من الاربعة العصر للخمسة بكرة",
        ),
    ],
)
def test_predefined_time_intervals(start_time, end_time, input):
    output = parse_dimension(input, time=True)
    assert_interval_output(output, start_time, end_time)


@pytest.mark.parametrize(
    "input",
    [
        ("11"),
        ("الحادي عشر"),
        ("احد عشر"),
        ("اثنين"),
        ("ثلاثة"),
        ("يوم"),
        ("اربعة وخمسين ساعة"),
        ("جمع"),
        ("السبتت"),
        ("الثانية عشر"),
        ("الثانية والنصف"),
    ],
)
def test_negative_cases(input):
    output = parse_dimension(input, time=True)
    assert output == []
