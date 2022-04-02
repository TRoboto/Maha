from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE

import maha.parsers.rules.numeral.values as numvalues
from maha.constants import ARABIC_COMMA, COMMA, LAM, WAW, arabic, english
from maha.expressions import EXPRESSION_SPACE, EXPRESSION_SPACE_OR_NONE
from maha.parsers.rules.duration.values import (
    ONE_DAY,
    ONE_HOUR,
    ONE_MINUTE,
    ONE_MONTH,
    ONE_WEEK,
    ONE_YEAR,
    SEVERAL_DAYS,
    SEVERAL_HOURS,
    SEVERAL_MINUTES,
    SEVERAL_MONTHS,
    SEVERAL_WEEKS,
    SEVERAL_YEARS,
    TWO_DAYS,
    TWO_HOURS,
    TWO_MINUTES,
    TWO_MONTHS,
    TWO_WEEKS,
    TWO_YEARS,
)
from maha.parsers.rules.numeral.rule import (
    RULE_NUMERAL_INTEGERS,
    RULE_NUMERAL_ONES,
    RULE_NUMERAL_TENS,
    RULE_NUMERAL_THOUSANDS,
    TEN,
    eleven_to_nineteen,
)
from maha.parsers.rules.ordinal.rule import (
    RULE_ORDINAL_ONES,
    RULE_ORDINAL_TENS,
    RULE_ORDINAL_THOUSANDS,
)
from maha.parsers.rules.ordinal.values import ALEF_LAM, ONE_PREFIX
from maha.parsers.templates import FunctionValue, Value
from maha.parsers.templates.value_expressions import MatchedValue
from maha.rexy import (
    Expression,
    ExpressionGroup,
    named_group,
    non_capturing_group,
    optional_non_capturing_group,
)

from ..common import (
    AFTER,
    AFTER_NEXT,
    ALL_ALEF,
    BEFORE,
    BEFORE_PREVIOUS,
    ELLA,
    FRACTIONS,
    IN_FROM_AT,
    NEXT,
    PREVIOUS,
    get_fractions_of_pattern,
    spaced_patterns,
)
from .template import TimeValue


def value_group(value):
    return named_group("value", value)


def parse_value(value: dict) -> TimeValue:
    return TimeValue(**value)


lam_lam_group = named_group("to_time", LAM + LAM)

ALEF_LAM_OR_DOUBLE_LAM = non_capturing_group(ALEF_LAM, lam_lam_group)
ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL = optional_non_capturing_group(ALEF_LAM_OR_DOUBLE_LAM)

START_OF = Value(1, "بداي[ةه]")
AFTER = optional_non_capturing_group("[إا]لل?ي" + EXPRESSION_SPACE) + "بعد"
BEFORE = optional_non_capturing_group("[إا]لل?ي" + EXPRESSION_SPACE) + "[أاق]بل"
PREVIOUS = (
    non_capturing_group("الماضي?", "السابق", "المنصرم", "الفا[يئ]ت")
    + numvalues.TEH_OPTIONAL_SUFFIX
)
NEXT = (
    non_capturing_group("الجاي", "القادم", "التالي?", "ال[اآ]تي?", "المقبل")
    + numvalues.TEH_OPTIONAL_SUFFIX
)
AFTER_NEXT = spaced_patterns(AFTER, NEXT)
BEFORE_PREVIOUS = spaced_patterns(BEFORE, PREVIOUS)
IN_FROM_AT = non_capturing_group(
    "في", "من", "خلال", "الموافق", "عند", "قراب[ةه]", "على"
)
FROM = Expression(non_capturing_group("من"))
TO = Expression(
    optional_non_capturing_group(WAW)
    + EXPRESSION_SPACE_OR_NONE
    + non_capturing_group(
        "[اإ]لى",
        "حتى",
        "لل?",
    )
)
THIS = optional_non_capturing_group(
    IN_FROM_AT + EXPRESSION_SPACE
) + non_capturing_group("ها?ذ[ياه]", "ه[اذ]ي", "هاد")

CURRENT = ALEF_LAM + non_capturing_group("حالي?", "حالي[ةه]?")
LAST = non_capturing_group("[آأا]خر", "ال[أا]خير")

HIJRIAH = Expression("هجري[ةه]?")
HIJRIATAN = Expression("هجريت?[اي]ن")

TIME_WORD_SEPARATOR = Expression(
    non_capturing_group(
        f"{EXPRESSION_SPACE_OR_NONE}{non_capturing_group(COMMA, ARABIC_COMMA)}",
        EXPRESSION_SPACE + "ب?و?ع?",
        EXPRESSION_SPACE + IN_FROM_AT + EXPRESSION_SPACE,
    )
    + non_capturing_group(r"\b", EXPRESSION_SPACE_OR_NONE)
)

ordinal_ones_tens = ExpressionGroup(
    RULE_ORDINAL_TENS, RULE_ORDINAL_ONES, ONE_PREFIX, START_OF
)
numeral_ones_tens = ExpressionGroup(
    RULE_NUMERAL_TENS, RULE_NUMERAL_ONES, RULE_NUMERAL_INTEGERS
)
numeral_hours = ExpressionGroup(
    eleven_to_nineteen,
    TEN,
    RULE_NUMERAL_ONES,
    RULE_NUMERAL_INTEGERS,
)

# region NOW
AT_THE_MOMENT = Value(
    TimeValue(years=0, months=0, days=0, hours=0, minutes=0, seconds=0),
    non_capturing_group(
        "ال[أآا]ن",
        spaced_patterns(THIS, non_capturing_group("الوقت", "اللح[زضظ][ةه]")),
        "هس[اةه]",
        "في الحال",
        "حالا",
        spaced_patterns(non_capturing_group("الوقت", "اللح[زضظ][ةه]"), CURRENT),
    ),
)
# endregion

# region YEARS
# ----------------------------------------------------
# YEARS
# ----------------------------------------------------
numeral_thousands = ExpressionGroup(
    RULE_NUMERAL_THOUSANDS,
    FunctionValue(lambda match: int(match.group()), r"\d{4}"),
)
ordinal_thousands = ExpressionGroup(RULE_ORDINAL_THOUSANDS)
alhijri_group = named_group("hijri", ALEF_LAM + HIJRIAH)
alhijri_optional_group = optional_non_capturing_group(alhijri_group + EXPRESSION_SPACE)
hijri_group = named_group("hijri", HIJRIAH)
hijriatan_group = named_group("hijri", HIJRIATAN)

NUMERAL_YEAR = FunctionValue(
    lambda match: parse_value(
        {
            "year": list(numeral_thousands.parse(match.group("value")))[0].value,
            "hijri": True if match.group("hijri") else None,
        }
    ),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_YEAR,
        value_group(numeral_thousands.join())
        + optional_non_capturing_group(
            EXPRESSION_SPACE
            + non_capturing_group(hijriatan_group, hijri_group, alhijri_group)
        ),
    ),
)
ORDINAL_YEAR = FunctionValue(
    lambda match: parse_value(
        {
            "year": list(ordinal_thousands.parse(match.group("value")))[0].value,
            "hijri": True if match.group("hijri") else None,
        }
    ),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_YEAR,
        value_group(ordinal_thousands.join())
        + optional_non_capturing_group(
            EXPRESSION_SPACE
            + non_capturing_group(hijriatan_group, hijri_group, alhijri_group)
        ),
    ),
)


def years_with_hijri(match, years):
    return TimeValue(years=years, hijri=True if match.group("hijri") else None)


THIS_YEAR = FunctionValue(
    lambda match: years_with_hijri(match, 0),
    optional_non_capturing_group(THIS + EXPRESSION_SPACE)
    + ALEF_LAM_OR_DOUBLE_LAM
    + ONE_YEAR
    + alhijri_optional_group
    + optional_non_capturing_group(EXPRESSION_SPACE + CURRENT),
)
LAST_YEAR = FunctionValue(
    lambda match: years_with_hijri(match, -1),
    non_capturing_group(
        spaced_patterns(
            BEFORE,
            ONE_YEAR + optional_non_capturing_group(EXPRESSION_SPACE + hijri_group),
        ),
        spaced_patterns(
            ALEF_LAM_OR_DOUBLE_LAM + ONE_YEAR,
            alhijri_optional_group + PREVIOUS,
        ),
    ),
)
LAST_TWO_YEARS = FunctionValue(
    lambda match: years_with_hijri(match, -2),
    non_capturing_group(
        spaced_patterns(
            ALEF_LAM_OR_DOUBLE_LAM + ONE_YEAR,
            alhijri_optional_group + BEFORE_PREVIOUS,
        ),
        spaced_patterns(
            BEFORE,
            TWO_YEARS
            + optional_non_capturing_group(EXPRESSION_SPACE + hijriatan_group),
        ),
    ),
)
NEXT_YEAR = FunctionValue(
    lambda match: years_with_hijri(match, 1),
    non_capturing_group(
        spaced_patterns(
            ALEF_LAM_OR_DOUBLE_LAM + ONE_YEAR,
            alhijri_optional_group + NEXT,
        ),
        spaced_patterns(
            AFTER,
            ONE_YEAR + optional_non_capturing_group(EXPRESSION_SPACE + hijri_group),
        ),
    ),
)
NEXT_TWO_YEARS = FunctionValue(
    lambda match: years_with_hijri(match, 2),
    non_capturing_group(
        spaced_patterns(
            ALEF_LAM_OR_DOUBLE_LAM + ONE_YEAR,
            alhijri_optional_group + AFTER_NEXT,
        ),
        spaced_patterns(
            AFTER,
            TWO_YEARS
            + optional_non_capturing_group(EXPRESSION_SPACE + hijriatan_group),
        ),
    ),
)

AFTER_N_YEARS = FunctionValue(
    lambda match: parse_value(
        {
            "years": list(numeral_ones_tens.parse(match.group("value")))[0].value,
            "hijri": True if match.group("hijri") else None,
        }
    ),
    spaced_patterns(
        AFTER,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_YEAR, SEVERAL_YEARS),
    )
    + optional_non_capturing_group(EXPRESSION_SPACE + hijri_group),
)
BEFORE_N_YEARS = FunctionValue(
    lambda match: parse_value(
        {
            "years": -1 * list(numeral_ones_tens.parse(match.group("value")))[0].value,
            "hijri": True if match.group("hijri") else None,
        }
    ),
    spaced_patterns(
        BEFORE,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_YEAR, SEVERAL_YEARS)
        + optional_non_capturing_group(EXPRESSION_SPACE + hijri_group),
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
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "يناير",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "كانون الثاني",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.ONE, arabic.ARABIC_ONE, english.ONE),
        ),
    ),
)
FEBRUARY = Value(
    TimeValue(month=2),
    non_capturing_group(
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "فبراير",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "شباط",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.TWO, arabic.ARABIC_TWO, english.TWO),
        ),
    ),
)
MARCH = Value(
    TimeValue(month=3),
    non_capturing_group(
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "مارس",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "[اأآ]ذار",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.THREE, arabic.ARABIC_THREE, english.THREE),
        ),
    ),
)
APRIL = Value(
    TimeValue(month=4),
    non_capturing_group(
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "نيسان",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + f"{ALL_ALEF}بريل",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.FOUR, arabic.ARABIC_FOUR, english.FOUR),
        ),
    ),
)
MAY = Value(
    TimeValue(month=5),
    non_capturing_group(
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "مايو",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "[أا]يار",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.FIVE, arabic.ARABIC_FIVE, english.FIVE),
        ),
    ),
)
JUNE = Value(
    TimeValue(month=6),
    non_capturing_group(
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "يونيو",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "حزيران",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.SIX, arabic.ARABIC_SIX, english.SIX),
        ),
    ),
)
JULY = Value(
    TimeValue(month=7),
    non_capturing_group(
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "يوليو",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "تموز",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.SEVEN, arabic.ARABIC_SEVEN, english.SEVEN),
        ),
    ),
)
AUGUST = Value(
    TimeValue(month=8),
    non_capturing_group(
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "[اأآ]غسطس",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "[أاآ]ب",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.EIGHT, arabic.ARABIC_EIGHT, english.EIGHT),
        ),
    ),
)
SEPTEMBER = Value(
    TimeValue(month=9),
    non_capturing_group(
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "سبتمبر",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "[اأ]يلول",
        spaced_patterns(
            ONE_MONTH,
            non_capturing_group(numvalues.NINE, arabic.ARABIC_NINE, english.NINE),
        ),
    ),
)
OCTOBER = Value(
    TimeValue(month=10),
    non_capturing_group(
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "[اأ]كتوبر",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "تشرين ال[اأ]ول",
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
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "نوفمبر",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "تشرين ال[تث]اني",
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
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "ديسمبر",
        optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "كانون ال[اأ]ول",
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

# -----------------------------------------------------------
# HIJRI MONTHS
# -----------------------------------------------------------
MUHARRAM = Value(
    TimeValue(month=1, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "محرم",
)
SAFAR = Value(
    TimeValue(month=2, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "صفر",
)
RABI_AL_AWWAL = Value(
    TimeValue(month=3, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "ربيع ال[اآأ]ول",
)
RABI_AL_ATHANI = Value(
    TimeValue(month=4, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE)
    + "ربيع "
    + non_capturing_group("ال[اآأ]خر", "الثاني")
    + "[ةه]?",
)
JUMADA_AL_AWWAL = Value(
    TimeValue(month=5, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE)
    + "جماد[ىي] ال[اآأ]ول[ىي]?",
)
JUMADA_AL_ATHANI = Value(
    TimeValue(month=6, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE)
    + "جماد[ىي] "
    + non_capturing_group("ال[اآأ]خر", "الثاني")
    + "[ةه]?",
)
RAJAB = Value(
    TimeValue(month=7, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "رجب",
)
SHABAN = Value(
    TimeValue(month=8, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "شعبان",
)
RAMADAN = Value(
    TimeValue(month=9, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "رمضان",
)
SHAWWAL = Value(
    TimeValue(month=10, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "شوال",
)
DHU_AL_QIDAH = Value(
    TimeValue(month=11, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "ذو القعد[ةه]",
)
DHU_AL_HIJJAH = Value(
    TimeValue(month=12, hijri=True),
    optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE) + "ذو الحج[ةه]",
)

_months = ExpressionGroup(
    OCTOBER,
    NOVEMBER,
    DECEMBER,
    JANUARY,
    FEBRUARY,
    MARCH,
    APRIL,
    MAY,
    JUNE,
    JULY,
    AUGUST,
    SEPTEMBER,
    MUHARRAM,
    SAFAR,
    RABI_AL_AWWAL,
    RABI_AL_ATHANI,
    JUMADA_AL_AWWAL,
    JUMADA_AL_ATHANI,
    RAJAB,
    SHABAN,
    RAMADAN,
    SHAWWAL,
    DHU_AL_QIDAH,
    DHU_AL_HIJJAH,
)

THIS_MONTH = Value(
    TimeValue(months=0),
    optional_non_capturing_group(THIS + EXPRESSION_SPACE)
    + ALEF_LAM_OR_DOUBLE_LAM
    + ONE_MONTH
    + optional_non_capturing_group(EXPRESSION_SPACE + CURRENT),
)
LAST_MONTH = Value(
    TimeValue(months=-1),
    non_capturing_group(
        spaced_patterns(BEFORE, ONE_MONTH),
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_MONTH, PREVIOUS),
    ),
)
LAST_TWO_MONTHS = Value(
    TimeValue(months=-2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_MONTH, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_MONTHS),
    ),
)
NEXT_MONTH = Value(
    TimeValue(months=1),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_MONTH, NEXT),
        spaced_patterns(AFTER, ONE_MONTH),
    ),
)
NEXT_TWO_MONTHS = Value(
    TimeValue(months=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_MONTH, AFTER_NEXT),
        spaced_patterns(AFTER, TWO_MONTHS),
    ),
)

AFTER_N_MONTHS = FunctionValue(
    lambda match: parse_value(
        {"months": list(numeral_ones_tens.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        AFTER,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_MONTH, SEVERAL_MONTHS),
    ),
)
BEFORE_N_MONTHS = FunctionValue(
    lambda match: parse_value(
        {"months": -1 * list(numeral_ones_tens.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        BEFORE,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_MONTH, SEVERAL_MONTHS),
    ),
)


def get_matched_month(text):
    return _months.get_matched_expression(text).value  # type: ignore


SPECIFIC_MONTH = MatchedValue(_months, _months.join())
NEXT_SPECIFIC_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "next_month": get_matched_month(match.group("value")).month,
            "hijri": get_matched_month(match.group("value")).hijri,
        }
    ),
    non_capturing_group(
        spaced_patterns(ONE_MONTH, value_group(_months.join()), NEXT),
        spaced_patterns(value_group(_months.join()), NEXT),
    ),
)
PREVIOUS_SPECIFIC_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "prev_month": get_matched_month(match.group("value")).month,
            "hijri": get_matched_month(match.group("value")).hijri,
        }
    ),
    non_capturing_group(
        spaced_patterns(ONE_MONTH, value_group(_months.join()), PREVIOUS),
        spaced_patterns(value_group(_months.join()), PREVIOUS),
    ),
)
AFTER_SPECIFIC_NEXT_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "next_month": get_matched_month(match.group("value")).month,
            "hijri": get_matched_month(match.group("value")).hijri,
            "years": 1,
        }
    ),
    non_capturing_group(
        spaced_patterns(ONE_MONTH, value_group(_months.join()), AFTER_NEXT),
        spaced_patterns(value_group(_months.join()), AFTER_NEXT),
    ),
)
BEFORE_SPECIFIC_PREVIOUS_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "prev_month": get_matched_month(match.group("value")).month,
            "hijri": get_matched_month(match.group("value")).hijri,
            "years": -1,
        }
    ),
    non_capturing_group(
        spaced_patterns(ONE_MONTH, value_group(_months.join()), BEFORE_PREVIOUS),
        spaced_patterns(value_group(_months.join()), BEFORE_PREVIOUS),
    ),
)
# endregion

# region WEEKS
# ----------------------------------------------------
# WEEKS
# ----------------------------------------------------

THIS_WEEK = Value(
    TimeValue(weeks=0),
    optional_non_capturing_group(THIS + EXPRESSION_SPACE)
    + ALEF_LAM_OR_DOUBLE_LAM
    + ONE_WEEK
    + optional_non_capturing_group(EXPRESSION_SPACE + CURRENT),
)
LAST_WEEK = Value(
    TimeValue(weeks=-1),
    non_capturing_group(
        spaced_patterns(BEFORE, ONE_WEEK),
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_WEEK, PREVIOUS),
    ),
)
LAST_TWO_WEEKS = Value(
    TimeValue(weeks=-2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_WEEK, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_WEEKS),
    ),
)
NEXT_WEEK = Value(
    TimeValue(weeks=1),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_WEEK, NEXT),
        spaced_patterns(AFTER, ONE_WEEK),
    ),
)
NEXT_TWO_WEEKS = Value(
    TimeValue(weeks=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_WEEK, AFTER_NEXT),
        spaced_patterns(AFTER, TWO_WEEKS),
    ),
)

AFTER_N_WEEKS = FunctionValue(
    lambda match: parse_value(
        {"weeks": list(numeral_ones_tens.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        AFTER,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_WEEK, SEVERAL_WEEKS),
    ),
)
BEFORE_N_WEEKS = FunctionValue(
    lambda match: parse_value(
        {"weeks": -1 * list(numeral_ones_tens.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        BEFORE,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_WEEK, SEVERAL_WEEKS),
    ),
)

# endregion

# region DAYS
# ----------------------------------------------------
# DAYS
# ----------------------------------------------------
SUNDAY = Value(SU, ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + "[أا]حد")
MONDAY = Value(MO, ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + "[إا][تث]نين")
TUESDAY = Value(TU, ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + "[ثت]لا[ثت]اء?")
WEDNESDAY = Value(WE, ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + "[أا]ربعاء?")
THURSDAY = Value(TH, ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + "خميس")
FRIDAY = Value(FR, ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + "جمع[ةه]")
SATURDAY = Value(SA, ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + "سبت")
_days = ExpressionGroup(SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY)

WEEKDAY = FunctionValue(
    lambda match: TimeValue(
        weekday=_days.get_matched_expression(match.group("value")).value  # type: ignore
    ),
    optional_non_capturing_group(ONE_DAY + EXPRESSION_SPACE)
    + non_capturing_group(
        ALEF_LAM_OR_DOUBLE_LAM + value_group(_days[:2].join()),
        value_group(_days[2:].join()),
    ),
)
THIS_DAY = Value(
    TimeValue(days=0),
    optional_non_capturing_group(THIS + EXPRESSION_SPACE)
    + ALEF_LAM_OR_DOUBLE_LAM
    + ONE_DAY
    + optional_non_capturing_group(EXPRESSION_SPACE + CURRENT),
)
YESTERDAY = Value(
    TimeValue(days=-1),
    non_capturing_group(
        "[اإ]?مبارح",
        ALEF_LAM_OR_DOUBLE_LAM + "بارح[ةه]",
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + "[أا]مس",
        spaced_patterns(BEFORE, ONE_DAY),
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_DAY, PREVIOUS),
    ),
)
BEFORE_YESTERDAY = Value(
    TimeValue(days=-2),
    non_capturing_group(
        spaced_patterns(non_capturing_group("[أا]ول", str(BEFORE)), YESTERDAY),
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_DAY, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_DAYS),
    ),
)
TOMORROW = Value(
    TimeValue(days=1),
    non_capturing_group(
        optional_non_capturing_group(ONE_DAY + EXPRESSION_SPACE)
        + ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL
        + "غدا?",
        "بكر[ةه]",
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_DAY, NEXT),
        spaced_patterns(AFTER, ONE_DAY),
    ),
)
AFTER_TOMORROW = Value(
    TimeValue(days=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_DAY, AFTER_NEXT),
        spaced_patterns(AFTER, TOMORROW),
        spaced_patterns(AFTER, TWO_DAYS),
    ),
)

AFTER_N_DAYS = FunctionValue(
    lambda match: parse_value(
        {"days": list(numeral_ones_tens.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        AFTER,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_DAY, SEVERAL_DAYS),
    ),
)
BEFORE_N_DAYS = FunctionValue(
    lambda match: parse_value(
        {"days": -1 * list(numeral_ones_tens.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        BEFORE,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_DAY, SEVERAL_DAYS),
    ),
)
NEXT_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {
            "days": 1,
            "weekday": _days.get_matched_expression(match.group("value")).value(1),  # type: ignore
        }
    ),
    non_capturing_group(
        spaced_patterns(ONE_DAY, value_group(_days.join()), NEXT),
        spaced_patterns(value_group(_days.join()), NEXT),
    ),
)
PREVIOUS_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {
            "days": -1,
            "weekday": _days.get_matched_expression(match.group("value")).value(-1),  # type: ignore
        }
    ),
    non_capturing_group(
        spaced_patterns(ONE_DAY, value_group(_days.join()), PREVIOUS),
        spaced_patterns(value_group(_days.join()), PREVIOUS),
    ),
)
AFTER_NEXT_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {
            "days": 1,
            "weekday": _days.get_matched_expression(match.group("value")).value(2),  # type: ignore
        }
    ),
    non_capturing_group(
        spaced_patterns(ONE_DAY, value_group(_days.join()), AFTER_NEXT),
        spaced_patterns(value_group(_days.join()), AFTER_NEXT),
    ),
)
BEFORE_PREVIOUS_WEEKDAY = FunctionValue(
    lambda match: parse_value(
        {
            "days": -1,
            "weekday": _days.get_matched_expression(match.group("value")).value(-2),  # type: ignore
        }
    ),
    non_capturing_group(
        spaced_patterns(ONE_DAY, value_group(_days.join()), BEFORE_PREVIOUS),
        spaced_patterns(value_group(_days.join()), BEFORE_PREVIOUS),
    ),
)
LAST_DAY = Value(
    parse_value({"day": 31}),
    non_capturing_group(
        spaced_patterns(LAST, ONE_DAY),
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_DAY, LAST),
    ),
)
LAST_SPECIFIC_DAY = FunctionValue(
    lambda match: parse_value(
        {
            "day": 31,
            "weekday": _days.get_matched_expression(match.group("day")).value(-1),  # type: ignore
        }
    ),
    non_capturing_group(
        LAST
        + EXPRESSION_SPACE
        + optional_non_capturing_group(ONE_DAY + EXPRESSION_SPACE)
        + named_group("day", _days.join()),
        optional_non_capturing_group(ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_DAY)
        + EXPRESSION_SPACE
        + named_group("day", _days.join())
        + LAST,
    ),
)
ORDINAL_SPECIFIC_DAY = FunctionValue(
    lambda match: parse_value(
        {
            "day": 1,
            "weekday": _days.get_matched_expression(match.group("day")).value(  # type: ignore
                list(ordinal_ones_tens.parse(match.group("ordinal")))[0].value
            ),
        }
    ),
    non_capturing_group(
        spaced_patterns(
            named_group("ordinal", ordinal_ones_tens.join()),
            optional_non_capturing_group(
                ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_DAY + EXPRESSION_SPACE
            )
            + named_group("day", _days.join()),
        ),
        spaced_patterns(
            optional_non_capturing_group(
                ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_DAY + EXPRESSION_SPACE
            )
            + named_group("day", _days.join()),
            named_group("ordinal", ordinal_ones_tens.join()),
        ),
    ),
)
# endregion

# region LAST DAY OF MONTH
# ----------------------------------------------------
# LAST DAY OF MONTH
# ----------------------------------------------------
_optional_month_start = optional_non_capturing_group(
    EXPRESSION_SPACE + ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_MONTH
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
        + EXPRESSION_SPACE
        + LAST
        + EXPRESSION_SPACE
        + IN_FROM_AT,
    )
    + _optional_month_start
)

LAST_SPECIFIC_DAY_OF_SPECIFIC_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "weekday": _days.get_matched_expression(match.group("day")).value(-1),  # type: ignore
            "day": 31,
        }
    )
    + get_matched_month(match.group("month")),
    spaced_patterns(_start_of_last_day, named_group("month", _months.join())),
)
# endregion

# region HOURS
# -----------------------------------------------
# HOURS
# -----------------------------------------------
NUMERAL_HOUR = FunctionValue(
    lambda match: parse_value(
        {
            "microsecond": 0,
            "second": 0,
            "minute": 0,
            "hour": list(numeral_hours.parse(match.group("value")))[0].value,
        }
    ),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_HOUR,
        value_group(numeral_hours.join()),
    ),
)

ORDINAL_HOUR = FunctionValue(
    lambda match: parse_value(
        {
            "microsecond": 0,
            "second": 0,
            "minute": 0,
            "hour": list(ordinal_ones_tens.parse(match.group("value")))[0].value,
        }
    ),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_HOUR,
        value_group(ordinal_ones_tens.join()),
    ),
)

THIS_HOUR = Value(
    TimeValue(hours=0),
    optional_non_capturing_group(THIS + EXPRESSION_SPACE)
    + ALEF_LAM_OR_DOUBLE_LAM
    + ONE_HOUR
    + optional_non_capturing_group(EXPRESSION_SPACE + CURRENT),
)
LAST_HOUR = Value(
    TimeValue(hours=-1),
    non_capturing_group(
        spaced_patterns(BEFORE, ONE_HOUR),
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_HOUR, PREVIOUS),
    ),
)
LAST_TWO_HOURS = Value(
    TimeValue(hours=-2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_HOUR, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_HOURS),
    ),
)
NEXT_HOUR = Value(
    TimeValue(hours=1),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_HOUR, NEXT),
        spaced_patterns(AFTER, ONE_HOUR),
    ),
)
NEXT_TWO_HOURS = Value(
    TimeValue(hours=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_HOUR, AFTER_NEXT),
        spaced_patterns(AFTER, TWO_HOURS),
    ),
)

AFTER_N_HOURS = FunctionValue(
    lambda match: parse_value(
        {"hours": list(numeral_hours.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        AFTER,
        value_group(numeral_hours.join()),
        non_capturing_group(ONE_HOUR, SEVERAL_HOURS),
    ),
)
BEFORE_N_HOURS = FunctionValue(
    lambda match: parse_value(
        {"hours": -1 * list(numeral_hours.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        BEFORE,
        value_group(numeral_hours.join()),
        non_capturing_group(ONE_HOUR, SEVERAL_HOURS),
    ),
)
# endregion

# region MINUTES
# ----------------------------------------------------
# MINUTES
# ----------------------------------------------------
NUMERAL_MINUTE = FunctionValue(
    lambda match: parse_value(
        {
            "microsecond": 0,
            "second": 0,
            "minute": list(numeral_ones_tens.parse(match.group("value")))[0].value,
        }
    ),
    non_capturing_group(
        spaced_patterns(
            ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_MINUTE,
            value_group(numeral_ones_tens.join()),
        ),
        spaced_patterns(
            value_group(numeral_ones_tens.join()),
            non_capturing_group(ONE_MINUTE, SEVERAL_MINUTES),
        ),
    ),
)

ORDINAL_MINUTE = FunctionValue(
    lambda match: parse_value(
        {
            "microsecond": 0,
            "second": 0,
            "minute": list(ordinal_ones_tens.parse(match.group("value")))[0].value,
        }
    ),
    non_capturing_group(
        spaced_patterns(
            ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_MINUTE,
            value_group(ordinal_ones_tens.join()),
        ),
        spaced_patterns(
            value_group(ordinal_ones_tens.join()),
            non_capturing_group(ONE_MINUTE, SEVERAL_MINUTES),
        ),
    ),
)

THIS_MINUTE = Value(
    TimeValue(minutes=0),
    optional_non_capturing_group(THIS + EXPRESSION_SPACE)
    + ALEF_LAM_OR_DOUBLE_LAM
    + ONE_MINUTE
    + optional_non_capturing_group(EXPRESSION_SPACE + CURRENT),
)
LAST_MINUTE = Value(
    TimeValue(minutes=-1),
    non_capturing_group(
        spaced_patterns(BEFORE, ONE_MINUTE),
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_MINUTE, PREVIOUS),
    ),
)
LAST_TWO_MINUTES = Value(
    TimeValue(minutes=-2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_MINUTE, BEFORE_PREVIOUS),
        spaced_patterns(BEFORE, TWO_MINUTES),
    ),
)
NEXT_MINUTE = Value(
    TimeValue(minutes=1),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_MINUTE, NEXT),
        spaced_patterns(AFTER, ONE_MINUTE),
    ),
)
NEXT_TWO_MINUTES = Value(
    TimeValue(minutes=2),
    non_capturing_group(
        spaced_patterns(ALEF_LAM_OR_DOUBLE_LAM + ONE_MINUTE, AFTER_NEXT),
        spaced_patterns(AFTER, TWO_MINUTES),
    ),
)

AFTER_N_MINUTES = FunctionValue(
    lambda match: parse_value(
        {"minutes": list(numeral_ones_tens.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        AFTER,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_MINUTE, SEVERAL_MINUTES),
    ),
)
BEFORE_N_MINUTES = FunctionValue(
    lambda match: parse_value(
        {"minutes": -1 * list(numeral_ones_tens.parse(match.group("value")))[0].value}
    ),
    spaced_patterns(
        BEFORE,
        value_group(numeral_ones_tens.join()),
        non_capturing_group(ONE_MINUTE, SEVERAL_MINUTES),
    ),
)
# endregion

# region AM PM
# ----------------------------------------------------
# AM PM
# ----------------------------------------------------
PM = Value(
    TimeValue(am_pm="PM"),
    non_capturing_group(
        optional_non_capturing_group(
            AFTER + EXPRESSION_SPACE,
            THIS + EXPRESSION_SPACE,
            BEFORE + EXPRESSION_SPACE,
        )
        + ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL
        + non_capturing_group(
            "مساء?ا?",
            "مغرب",
            "عشاء?ا?",
            "عصرا?",
            "ليل[اةه]?",
        ),
        spaced_patterns(AFTER, ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + "ظهرا?"),
    ),
)
AM = Value(
    TimeValue(am_pm="AM"),
    non_capturing_group(
        optional_non_capturing_group(
            BEFORE + EXPRESSION_SPACE, THIS + EXPRESSION_SPACE, AFTER + EXPRESSION_SPACE
        )
        + ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL
        + non_capturing_group(
            "صبا?حا?",
            "فجرا?",
        ),
        optional_non_capturing_group(BEFORE + EXPRESSION_SPACE, THIS + EXPRESSION_SPACE)
        + ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL
        + "ظهرا?",
    ),
)

# endregion

# region YEARS + MONTHS
# ----------------------------------------------------
# YEARS + MONTHS
# ----------------------------------------------------
YEAR_WITH_MONTH = FunctionValue(
    lambda match: parse_value(
        {"year": list(numeral_thousands.parse(match.group("value")))[0].value}
    )
    + get_matched_month(match.group("month")),
    spaced_patterns(
        named_group("month", _months.join()), value_group(numeral_thousands.join())
    ),
)
MONTH_YEAR_FORM = FunctionValue(
    lambda match: parse_value(
        {
            "month": int(match.group("month")),
            "year": int(match.group("year")),
        }
    ),
    named_group("month", r"\d{1,2}")
    + non_capturing_group("/", "-")
    + named_group("year", r"\d{4}"),
)
# endregion

# region DAY + MONTH
# ----------------------------------------------------
# DAY WITH MONTH
# ----------------------------------------------------
_optional_middle = optional_non_capturing_group(
    IN_FROM_AT + EXPRESSION_SPACE
) + optional_non_capturing_group(ONE_MONTH + EXPRESSION_SPACE)

_optional_start = (
    optional_non_capturing_group(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_DAY + EXPRESSION_SPACE
    )
    + optional_non_capturing_group(_days.join() + EXPRESSION_SPACE)
    + optional_non_capturing_group(IN_FROM_AT + EXPRESSION_SPACE)
)
months_expressions = ExpressionGroup(
    AFTER_N_MONTHS,
    BEFORE_N_MONTHS,
    AFTER_SPECIFIC_NEXT_MONTH,
    LAST_TWO_MONTHS,
    NEXT_TWO_MONTHS,
    LAST_MONTH,
    NEXT_MONTH,
    NEXT_SPECIFIC_MONTH,
    PREVIOUS_SPECIFIC_MONTH,
    BEFORE_SPECIFIC_PREVIOUS_MONTH,
    THIS_MONTH,
    SPECIFIC_MONTH,
)
ORDINAL_AND_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "day": (list(ordinal_ones_tens.parse(match.group("ordinal")))[0].value),
        }
    )
    + list(months_expressions.parse(match.group("value")))[0].value,
    non_capturing_group(
        spaced_patterns(
            _optional_start + named_group("ordinal", ordinal_ones_tens.join()),
            _optional_middle + value_group(months_expressions.join()),
        ),
        spaced_patterns(
            named_group("ordinal", ordinal_ones_tens.join()),
            ONE_DAY,
            _optional_middle + value_group(months_expressions.join()),
        ),
        spaced_patterns(
            _optional_middle + value_group(_months.join()),
            named_group("ordinal", ordinal_ones_tens.join()),
        ),
    ),
)
NUMERAL_AND_MONTH = FunctionValue(
    lambda match: parse_value(
        {
            "day": (list(numeral_ones_tens.parse(match.group("numeral")))[0].value),
        }
    )
    + list(months_expressions.parse(match.group("value")))[0].value,
    non_capturing_group(
        spaced_patterns(
            _optional_start + named_group("numeral", numeral_ones_tens.join()),
            _optional_middle + value_group(months_expressions.join()),
        ),
        spaced_patterns(
            _optional_middle + value_group(months_expressions.join()),
            named_group("numeral", numeral_ones_tens.join()),
        ),
    ),
)

DAY_MONTH_FORM = FunctionValue(
    lambda match: parse_value(
        {
            "day": int(match.group("day")),
            "month": int(match.group("month")),
        }
    ),
    named_group("day", r"\d{1,2}")
    + non_capturing_group("/", "-")
    + named_group("month", r"\d{1,2}"),
)
# endregion

# region DAY + MONTH + YEAR
# ----------------------------------------------------
# DAY + MONTH + YEAR
# ----------------------------------------------------
DAY_MONTH_YEAR_FORM = FunctionValue(
    lambda match: parse_value(
        {
            "day": int(match.group("day")),
            "month": int(match.group("month")),
            "year": int(match.group("year")),
        }
    ),
    named_group("day", r"\d{1,2}")
    + non_capturing_group("/", "-")
    + named_group("month", r"\d{1,2}")
    + non_capturing_group("/", "-")
    + named_group("year", r"\d{4}"),
)
# endregion

# region HOURS + MINUTES
# ----------------------------------------------------
# HOURS AND MINUTES
# ----------------------------------------------------
def parse_time_fraction(match, expression, am_pm=None):
    ella = ELLA.search(match.group("value"))
    splits = match.group("value").split(" ")
    if ella:
        hour_text, fraction_text = " ".join(splits[:-2]), " ".join(splits[-2:])
    else:
        hour_text, fraction_text = " ".join(splits[:-1]), splits[-1]
    fraction = list(FRACTIONS.parse(fraction_text))[0].value
    minute = int(60 * fraction)
    hour = list(expression.parse(hour_text))[0].value
    if ella:
        hour = hour - 1 if hour > 0 else 23
    time = {"microsecond": 0, "second": 0, "minute": minute, "hour": hour}
    if am_pm:
        time["am_pm"] = am_pm
    return parse_value(time)


NUMERAL_FRACTION_HOUR_MINUTE = FunctionValue(
    lambda match: parse_time_fraction(match, numeral_ones_tens),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_HOUR,
        value_group(get_fractions_of_pattern(numeral_ones_tens.join())),
    ),
)
ORDINAL_FRACTION_HOUR_MINUTE = FunctionValue(
    lambda match: parse_time_fraction(match, ordinal_ones_tens),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_HOUR,
        value_group(get_fractions_of_pattern(ordinal_ones_tens.join())),
    ),
)
HOUR_MINUTE_FORM = FunctionValue(
    lambda match: parse_value(
        {
            "microsecond": 0,
            "second": 0,
            "hour": int(match.group("hour")),
            "minute": int(match.group("minute")),
        }
    ),
    optional_non_capturing_group(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_HOUR + EXPRESSION_SPACE
    )
    + named_group("hour", r"\d{1,2}")
    + ":"
    + named_group("minute", r"\d{1,2}"),
)
# endregion

# region HOUR + MINUTES + SECONDS
# ----------------------------------------------------
# HOUR + MINUTES + SECONDS
# ----------------------------------------------------
HOUR_MINUTE_SECOND_FORM = FunctionValue(
    lambda match: parse_value(
        {
            "hour": int(match.group("hour")),
            "minute": int(match.group("minute")),
            "second": int(match.group("second")),
            "microsecond": 0,
        }
    ),
    optional_non_capturing_group(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + ONE_HOUR + EXPRESSION_SPACE
    )
    + named_group("hour", r"\d{1,2}")
    + ":"
    + named_group("minute", r"\d{1,2}")
    + ":"
    + named_group("second", r"\d{1,2}"),
)
# endregion

# region HOUR + AM/PM
# ----------------------------------------------------
# HOUR + AM/PM
# ----------------------------------------------------
NUMERAL_HOUR_PM = FunctionValue(
    lambda match: parse_value(
        {
            "microsecond": 0,
            "second": 0,
            "minute": 0,
            "am_pm": "PM",
            "hour": list(numeral_hours.parse(match.group("value")))[0].value,
        }
    ),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + value_group(numeral_hours.join()),
        PM,
    ),
)
NUMERAL_HOUR_AM = FunctionValue(
    lambda match: parse_value(
        {
            "microsecond": 0,
            "second": 0,
            "minute": 0,
            "am_pm": "AM",
            "hour": list(numeral_hours.parse(match.group("value")))[0].value,
        }
    ),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL + value_group(numeral_hours.join()),
        AM,
    ),
)
NUMERAL_FRACTION_HOUR_AM = FunctionValue(
    lambda match: parse_time_fraction(match, numeral_hours, "AM"),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL
        + value_group(get_fractions_of_pattern(numeral_hours.join())),
        AM,
    ),
)
NUMERAL_FRACTION_HOUR_PM = FunctionValue(
    lambda match: parse_time_fraction(match, numeral_hours, "PM"),
    spaced_patterns(
        ALEF_LAM_OR_DOUBLE_LAM_OPTIONAL
        + value_group(get_fractions_of_pattern(numeral_hours.join())),
        PM,
    ),
)
ORDINAL_HOUR_PM = FunctionValue(
    lambda match: parse_value(
        {
            "microsecond": 0,
            "second": 0,
            "minute": 0,
            "am_pm": "PM",
            "hour": list(ordinal_ones_tens.parse(match.group("value")))[0].value,
        }
    ),
    spaced_patterns(value_group(ordinal_ones_tens.join()), PM),
)
ORDINAL_HOUR_AM = FunctionValue(
    lambda match: parse_value(
        {
            "microsecond": 0,
            "second": 0,
            "minute": 0,
            "am_pm": "AM",
            "hour": list(ordinal_ones_tens.parse(match.group("value")))[0].value,
        }
    ),
    spaced_patterns(value_group(ordinal_ones_tens.join()), AM),
)
ORDINAL_FRACTION_HOUR_AM = FunctionValue(
    lambda match: parse_time_fraction(match, ordinal_ones_tens, "AM"),
    spaced_patterns(
        value_group(get_fractions_of_pattern(ordinal_ones_tens.join())), AM
    ),
)
ORDINAL_FRACTION_HOUR_PM = FunctionValue(
    lambda match: parse_time_fraction(match, ordinal_ones_tens, "PM"),
    spaced_patterns(
        value_group(get_fractions_of_pattern(ordinal_ones_tens.join())), PM
    ),
)
# endregion
