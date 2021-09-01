from datetime import datetime

from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE

import maha.parsers.rules.numeral.values as numvalues
from maha.constants import ARABIC_COMMA, COMMA, arabic, english
from maha.expressions import EXPRESSION_SPACE, EXPRESSION_SPACE_OR_NONE
from maha.parsers.rules.duration.values import (
    ONE_DAY,
    ONE_MONTH,
    ONE_WEEK,
    SEVERAL_DAYS,
    SEVERAL_MONTHS,
    SEVERAL_WEEKS,
    TWO_DAYS,
    TWO_MONTHS,
    TWO_WEEKS,
)
from maha.parsers.rules.numeral.rule import (
    RULE_NUMERAL,
    RULE_NUMERAL_INTEGERS,
    RULE_NUMERAL_ONES,
    RULE_NUMERAL_TENS,
)
from maha.parsers.rules.numeral.values import TEH_OPTIONAL_SUFFIX
from maha.parsers.rules.ordinal.rule import RULE_ORDINAL_ONES, RULE_ORDINAL_TENS
from maha.parsers.rules.ordinal.values import ALEF_LAM, ALEF_LAM_OPTIONAL
from maha.parsers.templates import FunctionValue, Value
from maha.parsers.templates.value_expressions import MatchedValue
from maha.rexy import (
    Expression,
    ExpressionGroup,
    named_group,
    non_capturing_group,
    optional_non_capturing_group,
)

from ..common import ALL_ALEF, spaced_patterns
from .template import TimeValue


def value_group(value):
    return named_group("value", value)


def parse_value(value: dict) -> TimeValue:
    return TimeValue(**value)


TIME_WORD_SEPARATOR = Expression(
    non_capturing_group(
        f"{EXPRESSION_SPACE_OR_NONE}{non_capturing_group(COMMA, ARABIC_COMMA)}",
        str(EXPRESSION_SPACE),
    )
    + non_capturing_group(r"\b", str(EXPRESSION_SPACE_OR_NONE))
)

THIS = non_capturing_group("ها?ذ[ياه]", "ه[اذ]ي")
AFTER = optional_non_capturing_group("[إا]لل?ي" + EXPRESSION_SPACE) + "بعد"
BEFORE = optional_non_capturing_group("[إا]لل?ي" + EXPRESSION_SPACE) + "[أاق]بل"
PREVIOUS = non_capturing_group("الماضي?", "السابق", "المنصرم", "الفا[يئ]ت")
NEXT = (
    non_capturing_group("الجاي", "القادم", "التالي?", "ال[اآ]تي?", "المقبل")
    + TEH_OPTIONAL_SUFFIX
)
AFTER_NEXT = spaced_patterns(AFTER, NEXT)
BEFORE_PREVIOUS = spaced_patterns(BEFORE, PREVIOUS)
IN_FROM_AT = non_capturing_group("في", "من", "خلال", "الموافق")
IN_FROM_AT_THIS = spaced_patterns(IN_FROM_AT + "?", THIS)
LAST = non_capturing_group("[آأا]خر", "ال[أا]خير")

# region this time
AT_THE_MOMENT = Value(
    TimeValue(years=0, months=0, days=0, hours=0, minutes=0, seconds=0),
    non_capturing_group(
        "ال[أآا]ن",
        THIS
        + non_capturing_group(
            "الوقت",
            "اللح[زضظ][ةه]",
        ),
        "هس[ةه]",
        "في الحال",
    ),
)
# endregion

# region DAYS
# ----------------------------------------------------
# DAYS
# ----------------------------------------------------
SUNDAY = Value(SU, ALEF_LAM_OPTIONAL + "[أا]حد")
MONDAY = Value(MO, ALEF_LAM_OPTIONAL + "[إا][تث]نين")
TUESDAY = Value(TU, ALEF_LAM_OPTIONAL + "[ثت]لا[ثت]اء")
WEDNESDAY = Value(WE, ALEF_LAM_OPTIONAL + "[أا]ربعاء")
THURSDAY = Value(TH, ALEF_LAM_OPTIONAL + "خميس")
FRIDAY = Value(FR, ALEF_LAM_OPTIONAL + "جمع[ةه]")
SATURDAY = Value(SA, ALEF_LAM_OPTIONAL + "سبت")
_days = ExpressionGroup(SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY)

WEEKDAY = FunctionValue(
    lambda match: TimeValue(
        weekday=_days.get_matched_expression(match.group("value")).value  # type: ignore
    ),
    non_capturing_group(
        spaced_patterns(ONE_DAY, named_group("value", _days.join())),
        named_group("value", _days.join()),
    ),
)
THIS_DAY = Value(
    TimeValue(days=0),
    non_capturing_group("اليوم", spaced_patterns(IN_FROM_AT_THIS, "اليوم")),
)
YESTERDAY = Value(
    TimeValue(days=-1),
    non_capturing_group(
        "[اإ]?مبارح",
        ALEF_LAM + "بارح[ةه]",
        ALEF_LAM_OPTIONAL + "[أا]مس",
        spaced_patterns(BEFORE, ONE_DAY),
        spaced_patterns(ALEF_LAM + ONE_DAY, PREVIOUS),
    ),
)
BEFORE_YESTERDAY = Value(
    TimeValue(days=-2),
    non_capturing_group(
        spaced_patterns(non_capturing_group("[أا]ول", str(BEFORE)), YESTERDAY),
        spaced_patterns(ALEF_LAM + ONE_DAY, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_DAYS),
    ),
)
TOMORROW = Value(
    TimeValue(days=1),
    non_capturing_group(
        ALEF_LAM_OPTIONAL + "غدا?",
        "بكر[ةه]",
        spaced_patterns(ALEF_LAM + ONE_DAY, NEXT),
        spaced_patterns(AFTER, ONE_DAY),
    ),
)
AFTER_TOMORROW = Value(
    TimeValue(days=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_DAY, AFTER_NEXT),
        spaced_patterns(AFTER, TOMORROW),
        spaced_patterns(AFTER, TWO_DAYS),
    ),
)

AFTER_N_DAYS = FunctionValue(
    lambda match: parse_value({"days": list(RULE_NUMERAL(match.group("value")))[0]}),
    spaced_patterns(AFTER, value_group(RULE_NUMERAL), SEVERAL_DAYS),
)
BEFORE_N_DAYS = FunctionValue(
    lambda match: parse_value({"days": list(RULE_NUMERAL(match.group("value")))[0]}),
    spaced_patterns(BEFORE, value_group(RULE_NUMERAL), SEVERAL_DAYS),
)
NEXT_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {"weekday": _days.get_matched_expression(match.group("value")).value(1)}  # type: ignore
    ),
    non_capturing_group(
        spaced_patterns(ONE_DAY, value_group(_days.join()), NEXT),
        spaced_patterns(value_group(_days.join()), NEXT),
    ),
)
PREVIOUS_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {"weekday": _days.get_matched_expression(match.group("value")).value(-1)}  # type: ignore
    ),
    non_capturing_group(
        spaced_patterns(ONE_DAY, value_group(_days.join()), PREVIOUS),
        spaced_patterns(value_group(_days.join()), PREVIOUS),
    ),
)
AFTER_NEXT_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {"weekday": _days.get_matched_expression(match.group("value")).value(2)}  # type: ignore
    ),
    non_capturing_group(
        spaced_patterns(ONE_DAY, value_group(_days.join()), AFTER_NEXT),
        spaced_patterns(value_group(_days.join()), AFTER_NEXT),
    ),
)
BEFORE_PREVIOUS_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {"weekday": _days.get_matched_expression(match.group("value")).value(-2)}  # type: ignore
    ),
    non_capturing_group(
        spaced_patterns(ONE_DAY, value_group(_days.join()), BEFORE_PREVIOUS),
        spaced_patterns(value_group(_days.join()), BEFORE_PREVIOUS),
    ),
)
# endregion

# region MONTHS
# -----------------------------------------------------------
# MONTHS
# -----------------------------------------------------------
JANUARY = Value(
    TimeValue(month=1),
    non_capturing_group(
        "يناير",
        "كانون الثاني",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.ONE, arabic.ARABIC_ONE, english.ONE),
        ),
    ),
)
FEBRUARY = Value(
    TimeValue(month=2),
    non_capturing_group(
        "فبراير",
        "شباط",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.TWO, arabic.ARABIC_TWO, english.TWO),
        ),
    ),
)
MARCH = Value(
    TimeValue(month=3),
    non_capturing_group(
        "مارس",
        "[اأآ]ذار",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.THREE, arabic.ARABIC_THREE, english.THREE),
        ),
    ),
)
APRIL = Value(
    TimeValue(month=4),
    non_capturing_group(
        "نيسان",
        f"{ALL_ALEF}بريل",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.FOUR, arabic.ARABIC_FOUR, english.FOUR),
        ),
    ),
)
MAY = Value(
    TimeValue(month=5),
    non_capturing_group(
        "مايو",
        "أيار",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.FIVE, arabic.ARABIC_FIVE, english.FIVE),
        ),
    ),
)
JUNE = Value(
    TimeValue(month=6),
    non_capturing_group(
        "يونيو",
        "حزيران",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.SIX, arabic.ARABIC_SIX, english.SIX),
        ),
    ),
)
JULY = Value(
    TimeValue(month=7),
    non_capturing_group(
        "يوليو",
        "تموز",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.SEVEN, arabic.ARABIC_SEVEN, english.SEVEN),
        ),
    ),
)
AUGUST = Value(
    TimeValue(month=8),
    non_capturing_group(
        "[اأآ]غسطس",
        "[أاآ]ب",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.EIGHT, arabic.ARABIC_EIGHT, english.EIGHT),
        ),
    ),
)
SEPTEMBER = Value(
    TimeValue(month=9),
    non_capturing_group(
        "سبتمبر",
        "[اأ]يلول",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.NINE, arabic.ARABIC_NINE, english.NINE),
        ),
    ),
)
OCTOBER = Value(
    TimeValue(month=10),
    non_capturing_group(
        "[اأ]كتوبر",
        "تشرين الأول",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(
                numvalues.TEN,
                arabic.ARABIC_ONE + arabic.ARABIC_ZERO,
                english.ONE + english.ZERO,
            ),
        ),
    ),
)
NOVEMBER = Value(
    TimeValue(month=11),
    non_capturing_group(
        "نوفمبر",
        "تشرين الثاني",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(
                numvalues.ELEVEN,
                arabic.ARABIC_ONE + arabic.ARABIC_ONE,
                english.ONE + english.ONE,
            ),
        ),
    ),
)
DECEMBER = Value(
    TimeValue(month=12),
    non_capturing_group(
        "ديسمبر",
        "كانون الأول",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(
                numvalues.TWELVE,
                arabic.ARABIC_ONE + arabic.ARABIC_TWO,
                english.ONE + english.TWO,
            ),
        ),
    ),
)


_months = ExpressionGroup(
    JANUARY,
    FEBRUARY,
    MARCH,
    APRIL,
    MAY,
    JUNE,
    JULY,
    AUGUST,
    SEPTEMBER,
    OCTOBER,
    NOVEMBER,
    DECEMBER,
)

THIS_MONTH = Value(
    TimeValue(months=0),
    non_capturing_group("الشهر", spaced_patterns(IN_FROM_AT_THIS, "الشهر")),
)
LAST_MONTH = Value(
    TimeValue(months=-1),
    non_capturing_group(
        spaced_patterns(BEFORE, ONE_MONTH),
        spaced_patterns(ALEF_LAM + ONE_MONTH, PREVIOUS),
    ),
)
LAST_TWO_MONTHS = Value(
    TimeValue(months=-2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_MONTH, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_MONTHS),
    ),
)
NEXT_MONTH = Value(
    TimeValue(months=1),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_MONTH, NEXT),
        spaced_patterns(AFTER, ONE_MONTH),
    ),
)
NEXT_TWO_MONTHS = Value(
    TimeValue(months=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_MONTH, AFTER_NEXT),
        spaced_patterns(AFTER, TWO_MONTHS),
    ),
)

AFTER_N_MONTHS = FunctionValue(
    lambda match: parse_value({"months": list(RULE_NUMERAL(match.group("value")))[0]}),
    spaced_patterns(AFTER, value_group(RULE_NUMERAL), SEVERAL_MONTHS),
)
BEFORE_N_MONTHS = FunctionValue(
    lambda match: parse_value({"months": list(RULE_NUMERAL(match.group("value")))[0]}),
    spaced_patterns(BEFORE, value_group(RULE_NUMERAL), SEVERAL_MONTHS),
)


def specific_month(match, next_month=False, years=0):
    month = _months.get_matched_expression(match.group("value")).value.month  # type: ignore
    current_month = datetime.now().month
    if next_month:
        years += 1 if month <= current_month else 0
    else:
        years += 0 if month <= current_month else -1
    return parse_value(
        {
            "month": month,
            "years": years,
        }
    )


SPECIFIC_MONTH = MatchedValue(_months, _months.join())
NEXT_SPECIFIC_MONTH = FunctionValue(
    lambda match: specific_month(match, next_month=True),
    non_capturing_group(
        spaced_patterns(ONE_MONTH, value_group(_months.join()), NEXT),
        spaced_patterns(value_group(_months.join()), NEXT),
    ),
)
PREVIOUS_SPECIFIC_MONTH = FunctionValue(
    lambda match: specific_month(match, next_month=False),
    non_capturing_group(
        spaced_patterns(ONE_MONTH, value_group(_months.join()), PREVIOUS),
        spaced_patterns(value_group(_months.join()), PREVIOUS),
    ),
)
AFTER_SPECIFIC_NEXT_MONTH = FunctionValue(
    lambda match: specific_month(match, next_month=True, years=1),
    non_capturing_group(
        spaced_patterns(ONE_MONTH, value_group(_months.join()), AFTER_NEXT),
        spaced_patterns(value_group(_months.join()), AFTER_NEXT),
    ),
)
BEFORE_SPECIFIC_PREVIOUS_MONTH = FunctionValue(
    lambda match: specific_month(match, years=-1),
    non_capturing_group(
        spaced_patterns(ONE_MONTH, value_group(_months.join()), BEFORE_PREVIOUS),
        spaced_patterns(value_group(_months.join()), BEFORE_PREVIOUS),
    ),
)
# endregion

# region DAY WITH MONTH
# ----------------------------------------------------
# DAY WITH MONTH
# ----------------------------------------------------
ordinal_ones_tens = ExpressionGroup(RULE_ORDINAL_TENS, RULE_ORDINAL_ONES)
numeral_ones_tens = ExpressionGroup(
    RULE_NUMERAL_TENS, RULE_NUMERAL_ONES, RULE_NUMERAL_INTEGERS
)

_optional_middle = optional_non_capturing_group(
    IN_FROM_AT + EXPRESSION_SPACE
) + optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE)

_optional_start = (
    optional_non_capturing_group(ONE_DAY + EXPRESSION_SPACE)
    + optional_non_capturing_group(ALEF_LAM + ONE_DAY + EXPRESSION_SPACE)
    + optional_non_capturing_group(_days.join() + EXPRESSION_SPACE)
    + optional_non_capturing_group(IN_FROM_AT + EXPRESSION_SPACE)
)
ORDINAL_AND_SPECIFIC_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "month": _months.get_matched_expression(match.group("value")).value.month,  # type: ignore
            "day": (list(ordinal_ones_tens.parse(match.group("ordinal")))[0].value),
        }
    ),
    non_capturing_group(
        spaced_patterns(
            _optional_start + named_group("ordinal", ordinal_ones_tens.join()),
            _optional_middle + value_group(_months.join()),
        ),
        spaced_patterns(
            named_group("ordinal", ordinal_ones_tens.join()),
            ONE_DAY,
            _optional_middle + value_group(_months.join()),
        ),
    ),
)
ORDINAL_AND_THIS_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "months": 0,
            "day": (list(ordinal_ones_tens.parse(match.group("ordinal")))[0].value),
        }
    ),
    non_capturing_group(
        spaced_patterns(
            _optional_start + named_group("ordinal", ordinal_ones_tens.join()),
            _optional_middle + THIS_MONTH,
        ),
        spaced_patterns(
            named_group("ordinal", ordinal_ones_tens.join()),
            ONE_DAY,
            _optional_middle + THIS_MONTH,
        ),
    ),
)
NUMERAL_AND_SPECIFIC_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "month": _months.get_matched_expression(match.group("value")).value.month,  # type: ignore
            "day": (list(numeral_ones_tens.parse(match.group("numeral")))[0].value),
        }
    ),
    spaced_patterns(
        _optional_start + named_group("numeral", numeral_ones_tens.join()),
        _optional_middle + value_group(_months.join()),
    ),
)
NUMERAL_AND_THIS_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "month": 0,
            "day": (list(numeral_ones_tens.parse(match.group("numeral")))[0].value),
        }
    ),
    spaced_patterns(
        _optional_start + named_group("numeral", numeral_ones_tens.join()),
        _optional_middle + THIS_MONTH,
    ),
)
# endregion

# region WEEKS
# ----------------------------------------------------
# WEEKS
# ----------------------------------------------------

THIS_WEEK = Value(
    TimeValue(weeks=0),
    non_capturing_group(
        ALEF_LAM + ONE_WEEK, spaced_patterns(IN_FROM_AT_THIS, ALEF_LAM + ONE_WEEK)
    ),
)
LAST_WEEK = Value(
    TimeValue(weeks=-1),
    non_capturing_group(
        spaced_patterns(BEFORE, ONE_WEEK),
        spaced_patterns(ALEF_LAM + ONE_WEEK, PREVIOUS),
    ),
)
LAST_TWO_WEEKS = Value(
    TimeValue(weeks=-2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_WEEK, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_WEEKS),
    ),
)
NEXT_WEEK = Value(
    TimeValue(weeks=1),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_WEEK, NEXT),
        spaced_patterns(AFTER, ONE_WEEK),
    ),
)
NEXT_TWO_WEEKS = Value(
    TimeValue(weeks=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM + ONE_WEEK, AFTER_NEXT),
        spaced_patterns(AFTER, TWO_WEEKS),
    ),
)

AFTER_N_WEEKS = FunctionValue(
    lambda match: parse_value({"weeks": list(RULE_NUMERAL(match.group("value")))[0]}),
    spaced_patterns(AFTER, value_group(RULE_NUMERAL), SEVERAL_WEEKS),
)
BEFORE_N_WEEKS = FunctionValue(
    lambda match: parse_value({"weeks": list(RULE_NUMERAL(match.group("value")))[0]}),
    spaced_patterns(BEFORE, value_group(RULE_NUMERAL), SEVERAL_WEEKS),
)

# endregion

# region LAST DAY OF MONTH
# ----------------------------------------------------
# LAST DAY OF MONTH
# ----------------------------------------------------
_optional_month_start = optional_non_capturing_group(
    EXPRESSION_SPACE + ALEF_LAM_OPTIONAL + ONE_MONTH
)
_start_of_last_day = (
    non_capturing_group(
        LAST
        + EXPRESSION_SPACE
        + optional_non_capturing_group(ONE_DAY + EXPRESSION_SPACE)
        + named_group("day", _days.join())
        + EXPRESSION_SPACE
        + IN_FROM_AT,
        optional_non_capturing_group(ONE_DAY + EXPRESSION_SPACE)
        + named_group("day", _days.join())
        + LAST
        + EXPRESSION_SPACE
        + IN_FROM_AT,
    )
    + _optional_month_start
)

LAST_SPECIFIC_DAY_OF_SPECIFIC_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "month": _months.get_matched_expression(match.group("month")).value.month  # type: ignore
            + 1
            if _months.get_matched_expression(match.group("month")).value.month  # type: ignore
            + 1
            <= 12
            else 1,
            "weekday": _days.get_matched_expression(match.group("day")).value(-1),  # type: ignore
        }
    ),
    spaced_patterns(_start_of_last_day, named_group("month", _months.join())),
)
LAST_SPECIFIC_DAY_OF_NEXT_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "months": 1,
            "weekday": _days.get_matched_expression(match.group("day")).value(-1),  # type: ignore
        }
    ),
    spaced_patterns(_start_of_last_day, NEXT),
)
LAST_SPECIFIC_DAY_OF_LAST_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "months": -1,
            "weekday": _days.get_matched_expression(match.group("day")).value(-1),  # type: ignore
        }
    ),
    spaced_patterns(_start_of_last_day, LAST),
)
LAST_DAY_OF_SPECIFIC_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "month": _months.get_matched_expression(match.group("month")).value.month,  # type: ignore
            "day": 31,
        }
    ),
    spaced_patterns(LAST, ONE_DAY)
    + spaced_patterns(_optional_month_start, named_group("month", _months.join())),
)
LAST_DAY_OF_LAST_MONTH = FunctionValue(
    lambda _: parse_value(
        {
            "months": -1,
            "day": 31,
        }
    ),
    spaced_patterns(LAST, ONE_DAY) + spaced_patterns(_optional_month_start, LAST),
)
LAST_DAY_OF_NEXT_MONTH = FunctionValue(
    lambda _: parse_value(
        {
            "months": 1,
            "day": 31,
        }
    ),
    spaced_patterns(LAST, ONE_DAY, IN_FROM_AT)
    + spaced_patterns(_optional_month_start, NEXT),
)
# endregion
